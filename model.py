"""
Fable World Cup 2026 — group-stage score predictor.
Ensemble: World Football Elo  x  Polymarket-implied strength
Scoreline engine: Dixon-Coles-adjusted bivariate Poisson + Monte-Carlo group sim.
"""
import json, numpy as np
from scipy.stats import poisson
from scipy.optimize import minimize

rng = np.random.default_rng(20260611)

ELO  = json.load(open('wc_data.json'))
MKT  = json.load(open('market.json'))

# ---------- model constants ----------
BASE   = np.log(1.32)   # exp(BASE) = goals per team at rating parity (~WC average)
B      = 0.70           # Elo->goals sensitivity (supremacy ~2.0 goals at 400 Elo gap)
RHO    = -0.08          # Dixon-Coles low-score correlation
W_MKT  = 0.60           # ensemble weight on market-implied strength (vs Elo)
MAXG   = 10            # goals truncation for scoreline matrix

# ---------- name matching: market groupItemTitle -> our team name ----------
ALIAS = {
 'turkiye':'Turkey','türkiye':'Turkey','czechia':'Czech Republic','usa':'United States',
 'congo dr':'DR Congo','dr congo':'DR Congo','curacao':'Curacao','curaçao':'Curacao',
 'ivory coast':'Ivory Coast','south korea':'South Korea','south africa':'South Africa',
 'cape verde':'Cape Verde','saudi arabia':'Saudi Arabia','new zealand':'New Zealand',
 'bosnia and herzegovina':'Bosnia and Herzegovina',
}
def norm(name, group_teams):
    key = name.strip().lower()
    if key in ALIAS: return ALIAS[key]
    for t in group_teams:
        if t.lower() == key: return t
    for t in group_teams:               # fuzzy contains
        if key in t.lower() or t.lower() in key: return t
    raise KeyError(name)

# ---------- Dixon-Coles scoreline matrix ----------
def lambdas(ra, rb):
    d = ra - rb
    la = np.exp(BASE + B*d/400.0)
    lb = np.exp(BASE - B*d/400.0)
    return np.clip(la, 0.12, 6.0), np.clip(lb, 0.12, 6.0)

def score_matrix(ra, rb):
    la, lb = lambdas(ra, rb)
    x = poisson.pmf(np.arange(MAXG+1), la)
    y = poisson.pmf(np.arange(MAXG+1), lb)
    M = np.outer(x, y)
    # Dixon-Coles low-score correction
    M[0,0] *= 1 - la*lb*RHO
    M[0,1] *= 1 + la*RHO
    M[1,0] *= 1 + lb*RHO
    M[1,1] *= 1 - RHO
    M /= M.sum()
    return M, la, lb

def match_summary(ra, rb):
    M, la, lb = score_matrix(ra, rb)
    ph = np.tril(M, -1).sum()          # home (a) more goals -> below diagonal
    pd = np.trace(M)
    pa = np.triu(M, 1).sum()
    i, j = np.unravel_index(M.argmax(), M.shape)
    # top 3 scorelines
    flat = [((a, b), M[a, b]) for a in range(MAXG+1) for b in range(MAXG+1)]
    flat.sort(key=lambda z: -z[1])
    return dict(pa=ph, pd=pd, pb=pa, exa=la, exb=lb,
               ml=(int(i), int(j), float(M[i, j])),
               top=[(int(a), int(b), float(p)) for (a, b), p in flat[:4]])

# ---------- vectorised group Monte-Carlo (independent Poisson; DC negligible for standings) ----------
# FIFA fixture pattern over positions (0,1,2,3): (0,1)(2,3)(0,2)(3,1)(3,0)(1,2)
FIX = [(0,1),(2,3),(0,2),(3,1),(3,0),(1,2)]
_KGRID = np.arange(0, 16)
def fppf(U, lam):                 # fast Poisson inverse-CDF via searchsorted (CRN-friendly)
    cdf = poisson.cdf(_KGRID, lam)
    return np.searchsorted(cdf, U).astype(np.int64)
def sim_group(rats, N, U=None):
    rats = np.asarray(rats, float)
    pts = np.zeros((N,4)); gf = np.zeros((N,4)); ga = np.zeros((N,4))
    for mi,(a,b) in enumerate(FIX):
        la, lb = lambdas(rats[a], rats[b])
        if U is None:
            ga_ = rng.poisson(la, N); gb_ = rng.poisson(lb, N)
        else:
            ga_ = fppf(U[:,mi,0], la)
            gb_ = fppf(U[:,mi,1], lb)
        gf[:,a]+=ga_; ga[:,a]+=gb_; gf[:,b]+=gb_; ga[:,b]+=ga_
        wa = ga_>gb_; wb = gb_>ga_; dr=~(wa|wb)
        pts[wa,a]+=3; pts[wb,b]+=3; pts[dr,a]+=1; pts[dr,b]+=1
    gd = gf-ga
    # rank key: points, GD, GF, tiny random tiebreak
    key = pts*1e6 + gd*1e3 + gf + rng.random((N,4))*1e-3
    order = np.argsort(-key, axis=1)             # order[:,0] = winner pos
    win = order[:,0]
    winner_prob = np.bincount(win, minlength=4)/N
    # top2 and 3rd place
    top2 = np.zeros(4); third = np.zeros(4)
    for r in range(4):
        teams_at = order[:,r]
        if r<2:
            top2 += np.bincount(teams_at, minlength=4)
        if r==2:
            third += np.bincount(teams_at, minlength=4)
    return dict(winner=winner_prob, top2=top2/N, third=third/N,
                exp_pts=pts.mean(0), exp_gd=gd.mean(0))

# ---------- invert market -> per-group rating offsets (sum-zero, 3 free) ----------
def fit_offsets(base_rats, mkt_probs):
    base = np.asarray(base_rats, float)
    target = np.asarray(mkt_probs, float); target/=target.sum()
    Ufix = rng.random((60000,6,2))           # common random numbers -> smooth objective
    def loss(x):                              # x = 3 free offsets; 4th = -sum
        off = np.array([x[0],x[1],x[2], -(x[0]+x[1]+x[2])])
        w = sim_group(base+off, 60000, Ufix)['winner']
        return float(np.sum((w-target)**2))
    s = 80.0                                  # meaningful initial simplex step (rating points)
    simplex = np.array([[0,0,0],[s,0,0],[0,s,0],[0,0,s]], float)
    res = minimize(loss, np.zeros(3), method='Nelder-Mead',
                   options=dict(initial_simplex=simplex, xatol=3.0, fatol=2e-5, maxiter=300))
    x = res.x
    return np.array([x[0],x[1],x[2], -(x[0]+x[1]+x[2])])

# ================= run =================
out = {}
for g in sorted(ELO):
    teams = [t['team'] for t in ELO[g]]
    elo   = np.array([t['elo'] for t in ELO[g]], float)
    # market vector aligned to team order
    mk = MKT[g]['prices']
    mvec = np.zeros(4)
    for nm,p in mk.items():
        mvec[teams.index(norm(nm, teams))] = p
    mvec = mvec/ mvec.sum()
    # market-implied ratings, then ensemble blend
    off = fit_offsets(elo, mvec)
    mkt_rats = elo + off
    blend = elo + W_MKT*off
    out[g] = dict(teams=teams, elo=elo.tolist(), market=mvec.tolist(),
                  mkt_rats=mkt_rats.tolist(), blend=blend.tolist())

json.dump(out, open('ratings.json','w'), indent=2)
# quick check report
rep=[]
for g in sorted(out):
    o=out[g]
    sim = sim_group(o['blend'], 200000)
    rep.append(f"Group {g}")
    for i,t in enumerate(o['teams']):
        rep.append(f"  {t:<24} Elo {o['elo'][i]:6.0f}  blendR {o['blend'][i]:6.0f} "
                   f" mkt {o['market'][i]:.3f}  simWin {sim['winner'][i]:.3f} "
                   f" top2 {sim['top2'][i]:.3f}")
open('ratings_report.txt','w',encoding='utf-8').write('\n'.join(rep))
print("ratings built for groups:", list(out.keys()))
