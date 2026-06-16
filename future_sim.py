"""Forward rank simulator — fixes league_sim2's three flaws:
 (1) CURRENT standings (user #10, 374; deficit 284 to the #2 line), not the stale #8/165.
 (2) Rivals modeled as a CORRELATED HERD via a common-factor (Gaussian) copula, not 13
     mutually-independent random pickers. This is the realistic structure: the field piles
     onto favourites together, so beating the field requires decorrelating from the BLOC.
 (3) ~88 distinct remaining matches (the real horizon), not 8 matches replayed 12x.

Design choice for honesty: per-match points use ONE empirical marginal for EVERYONE
(equal forward skill). That FREEZES the current point gaps in expectation, so the ONLY way
the user climbs is VARIANCE that decorrelates from the field. This isolates the question
"does differentiation help when behind?" cleanly. We then stress-test rival skill +/-.

Knobs:
 rho_field : rivals' mutual correlation (herd strength). Sensitivity-tested.
 rho_user  : USER's correlation to the field common factor = the DIFFERENTIATION knob.
             high = pick like the field (EV-max chalk, DIFF_BAND=0); low = differentiated.
 user_edge : multiplier on user's per-match mean (real skill edge), to find the regime
             where EV-max (high rho) beats differentiation (low rho).
"""
import numpy as np
rng = np.random.default_rng(7)

# --- CURRENT standings (live_updates.md, post-MD2 2026-06-16) -------------------
# #1..#9 then USER(#10) then 3 unknowns below user (set plausibly; ~irrelevant to top-2).
standings = np.array([1113, 658, 609, 557, 436, 419, 411, 405, 389,  374,  350, 320, 290], float)
USER = 9                      # user is index 9 (the 10th entry)
NRIV = len(standings)         # 13 players total
N    = 40000                  # Monte Carlo paths
H    = 88                     # remaining matches

# --- per-match points marginal: user's realized 16-match ledger (equal-skill baseline) --
# hits: Mexico 69, Korea 96, Brazil-draw 122, Germany 15, Sweden 72 ; 11 zeros.
EMP = np.array([69, 96, 122, 15, 72] + [0]*11, float)   # mean 23.4, std ~40, zero-inflated
EMP_sorted = np.sort(EMP)

def empirical_quantile(u):
    """inverse-CDF of EMP via interpolation on the sorted sample (u in (0,1))."""
    idx = np.clip(u * len(EMP_sorted), 0, len(EMP_sorted) - 1e-9)
    lo = np.floor(idx).astype(int)
    return EMP_sorted[lo]

def sim(rho_field, rho_user, user_edge=1.0, rival_edge=1.0, verbose=False):
    """Returns P(user top-2), P(user top-1). user_edge/rival_edge scale per-match means."""
    user_tot  = np.full(N, standings[USER])
    rival_tot = np.tile(standings[None, :], (N, 1)).copy()  # (N,13)
    rivals = [j for j in range(NRIV) if j != USER]

    for _ in range(H):
        # common match factor (shared "did chalk/iconic hit this match")
        F = rng.standard_normal(N)
        # rivals: latent = sqrt(rho_field)*F + sqrt(1-rho_field)*eps  -> correlated herd
        for j in rivals:
            eps = rng.standard_normal(N)
            lat = np.sqrt(rho_field) * F + np.sqrt(1 - rho_field) * eps
            u = 0.5 * (1 + erf_approx(lat / np.sqrt(2)))
            rival_tot[:, j] += empirical_quantile(u) * rival_edge
        # user: rho_user controls correlation to the SAME field factor F
        eps = rng.standard_normal(N)
        lat = np.sqrt(rho_user) * F + np.sqrt(1 - rho_user) * eps
        u = 0.5 * (1 + erf_approx(lat / np.sqrt(2)))
        user_tot += empirical_quantile(u) * user_edge

    above = (rival_tot > user_tot[:, None]).sum(1)
    return float(np.mean(above <= 1)), float(np.mean(above == 0))

def erf_approx(x):
    # Abramowitz-Stegun 7.1.26 vectorized
    s = np.sign(x); x = np.abs(x)
    t = 1/(1+0.3275911*x)
    y = 1-(((((1.061405429*t-1.453152027)*t)+1.421413741)*t-0.284496736)*t+0.254829592)*t*np.exp(-x*x)
    return s*y

print(f"Forward sim: user #10 @374, deficit 284 to #2 line (658). H={H} matches, N={N}.")
print("Equal forward skill (everyone draws the same marginal) unless edge noted.\n")

print("== A. Differentiation knob (rho_user), rivals herd at rho_field=0.5, equal skill ==")
print(f"{'rho_user':>10}{'P(top2)':>10}{'P(top1)':>10}")
for ru in [0.05, 0.2, 0.4, 0.6, 0.8]:
    p2, p1 = sim(0.5, ru)
    print(f"{ru:>10.2f}{p2*100:>9.1f}%{p1*100:>9.1f}%")

print("\n== B. Robustness to herd strength (rho_field): compare differentiate vs follow ==")
print(f"{'rho_field':>10}{'diff(ru=.1)':>14}{'follow(ru=.7)':>15}")
for rf in [0.3, 0.5, 0.7]:
    pd, _ = sim(rf, 0.1); pf, _ = sim(rf, 0.7)
    print(f"{rf:>10.2f}{pd*100:>13.1f}%{pf*100:>14.1f}%")

print("\n== C. When does EV-max (follow) beat differentiate? vary USER skill edge ==")
print(f"{'user_edge':>10}{'diff(ru=.1)':>14}{'follow(ru=.7)':>15}")
for ue in [0.9, 1.0, 1.1, 1.25, 1.5]:
    pd, _ = sim(0.5, 0.1, user_edge=ue); pf, _ = sim(0.5, 0.7, user_edge=ue)
    print(f"{ue:>10.2f}{pd*100:>13.1f}%{pf*100:>14.1f}%")

print("\n== D. If rivals are actually STRONGER forward (rival_edge=1.15), equal user ==")
print(f"{'rho_user':>10}{'P(top2)':>10}")
for ru in [0.1, 0.4, 0.7]:
    p2, _ = sim(0.5, ru, rival_edge=1.15)
    print(f"{ru:>10.2f}{p2*100:>9.1f}%")

print("\n== E. The real DIFF_BAND question: does differentiation help if it COSTS EV? ==")
print("   (lower rho_user but also lower user_edge -> pricing the EV sacrifice)")
print(f"{'posture':>28}{'rho_u':>7}{'edge':>7}{'P(top2)':>10}")
cases = [("EV-max follow (DIFF_BAND=0)", 0.7, 1.00),
         ("differentiate, EV-free",     0.1, 1.00),
         ("differentiate, -2% EV",      0.1, 0.98),
         ("differentiate, -5% EV",      0.1, 0.95),
         ("differentiate, -10% EV",     0.1, 0.90),
         ("differentiate, -20% EV",     0.1, 0.80)]
for name, ru, ue in cases:
    p2, _ = sim(0.5, ru, user_edge=ue)
    print(f"{name:>28}{ru:>7.2f}{ue:>7.2f}{p2*100:>9.1f}%")
