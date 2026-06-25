# RED-TEAM REVIEW 2026-06-25 — "Take Ecuador over Germany as a +EV-variance rank play"

## Verdict: **FALSIFIED. Follow Germany.** (3 lenses converge; numbers correct, inference wrong.)

I recommended picking **Ecuador** (away underdog) over following Germany on MD10, on the basis that the
independent market (Ecuador 22% / draw 21% / Germany 59%) makes Ecuador market-EV-max (0.22×145 = **31.9** >
draw 27.1 > Germany 24.8), edge 1.23, field only 3% → "hard-gated +EV decorrelation, the rank lever." A
Tier-1 three-agent red-team (statistician + strategist + data-integrity, each recomputing) **broke it.**

## What each lens found
- **Data-integrity (numbers PASS):** reward-implied 17.9/20.2/61.9; market-EV 31.9/27.1/24.8; edge 1.23; blend-EV
  Ecuador 37.9 — all reproduce. BUT: (a) **edge>1 is non-discriminating** — the draw also clears it (1.04); the
  pick rests on blend-EV-max, not edge. (b) the "de-vigged" market sums to 1.02, not 1.0. (c) the load-bearing
  inputs — "Germany rotates," "market 22% prices it correctly" — are **ASSUMED, not measured.**
- **Statistician (inference FAILS):** EV-max is **fragile to a −3.3pt swing** in Ecuador's prob (the binding rival
  is the **draw**, not Germany; Ecuador stops being EV-max below 18.7%). Under a strong-Germany-XI counterfactual
  (Ecuador ~12-14%) Ecuador is **last**, not second. Decisive: modeling the bunched pack, Ecuador **raises expected
  rank ~0.9 places even in its own best-case 22% world** — P(worsen)=62% vs P(improve)=22% — because the field's
  88%-Germany bloc banks +42 on the 78% miss. **EV-positive but rank-negative = optimizing the wrong maximand.**
- **Strategist (structural FAIL):** the project's realized decorrelation/Axis-B ledger is **≈2/13 (~15%)**
  (Brazil-Morocco ✓, Belgium-Iran ✓; USA/Haiti/Ecuador-MD1/France/Austria/Panama/Mexico/Ger-CIV/Ecuador-MD7/
  Senegal-X2/Croatia all ✗). Ecuador is the **same profile as the losers, not a higher bar** — and it is the
  single most-documented model artifact in the project (cost the user twice already: MD1, MD7). The "we lean on
  market not model" defense fails: 22% is an ordinary underdog number that only looks juicy because reward 145 is
  large (reward ≈ inverse-true-prob); the 1.23 "edge" is the house's compression, **table-stakes EV, not rank
  separation.** Crucially the **rank asymmetry inverts the claim**: the user is **atop a tight bunch with a cushion
  below** (today: #8 @1857; #7 +11, #6 +53 above; #9 −81, #10 −147 below), not below a cluster needing to leapfrog.
  Variance helps a chaser; it is rank-destructive for someone defending a bunched position — a miss cedes the
  head-to-head to the rivals who took the chalk and lets #9 close. And one un-boosted hit (X2 spent) closes the
  top-5 gap to ~88, still short of #5 — so the realistic best case is "pass the bunch into #7," modal case (78%)
  is "fall behind it." Bad risk/reward.

## Corrected conclusion
**Follow Germany; follow the whole chalk slate.** This was a textbook repeat of the "high reward + field-thin =
take it" trap that lost on Panama and burned the X2 on Senegal — pattern-matched onto the project's worst artifact
team. The rank lever on an all-chalk slate is **NOT outcome decorrelation** (no clean separator exists this slate)
— it is **exact-score accuracy on the confident follows** (the documented real separator: climbers carry 7-11
exacts vs user 4; the user's single best move was a Colombia 1-0 EXACT +127 on a straight follow).

## Standing-rule reinforcement (this is the 3rd time an inference outran its sample/maximand here)
Before taking ANY off-chalk pick: (1) **maximand check** — am I above or below the rivals I'd separate from?
Variance only helps when chasing a bloc *above*; it is rank-negative when *defending* a bunched position from
below. (2) **artifact check** — is the contrarian spot landing on a team the model is known to misrate? Be MORE
suspicious, not less. (3) **ledger check** — does this clear a genuinely higher bar than the 2/13 that lost, or
is it the same profile? See [[two-axis-differentiation]].
