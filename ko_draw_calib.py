"""
KO DRAW CALIBRATION TRACKER (read-only diagnostic — touches NO deployed params)
================================================================================
Purpose: pre-registered test of the watch-item raised 2026-06-30 — "is the ET
transform (phi=0.635) under-pricing 120' KO draws?" A 120' draw = the match level
after extra time (goes to pens; scored as the draw line in our game).

This script ONLY measures. It does not refit phi or anything else. It reads the
frozen engine deterministically, recomputes each live KO match's predicted 120'
draw probability (model120 AND deployed blend120), lines them up against the
observed outcome, and runs a Poisson-binomial calibration test (observed draws vs
the sum of per-match predicted draw probs — the correct expectation when each match
has a different draw prob).

PRE-REGISTERED DECISION RULE (set 2026-06-30, BEFORE power exists — n was 4):
  * Primary statistic: observed KO draws D vs E[D]=sum(blend120 draw prob).
  * Two-sided Poisson-binomial tail p-value.
  * DO NOT touch phi unless ALL of:
      (a) n >= 12 KO matches with results,
      (b) D materially exceeds E[D] (ratio > ~1.5),
      (c) two-sided p < 0.05,
      (d) a Tier-1 red-team validates the direction + a phi re-grid on KO data.
  * Until then this is a watch-only instrument. A single slate of draws is variance
    (at n=4, P(>=2 draws | p~0.20) ~ 0.18 — see CLAUDE.md / session 2026-06-30).
  * Symmetric guard: if D << E[D] (draws OVER-priced) the same gate applies in reverse.

Update protocol: append played KO matches to LEDGER with observed=0/1; re-run.
"""
import json, numpy as np
from scipy.stats import nbinom, poisson
AD=json.load(open('attdef.json')); W2C=json.load(open('wc_to_canon.json')); Q=json.load(open('qualification_v5.json'))
mug=AD['_meta']['mu_goals']; R=Q['r']; MAXG=14; GAMMA=1.5; PHI=0.635
def AT(t): return AD[W2C[t]]['ATT']
def DF(t): return AD[W2C[t]]['DEF']
def lam_pair(th,ta):
    lh=np.exp(mug+AT(th)-DF(ta)); la=np.exp(mug+AT(ta)-DF(th))
    M=0.5*(np.log(lh)+np.log(la)); D=0.5*(np.log(lh)-np.log(la))
    return float(np.exp(M+GAMMA*D)), float(np.exp(M-GAMMA*D))
def nbvec(lam):
    p=R/(R+lam); v=nbinom.pmf(np.arange(MAXG+1),R,p); return v/v.sum()
def joint90(th,ta):
    lh,la=lam_pair(th,ta); Mx=np.outer(nbvec(lh),nbvec(la)); return Mx/Mx.sum(),lh,la
def transform120(Mx,lh,la,phi=PHI):
    n=Mx.shape[0]; le,lr=lh/3*phi, la/3*phi
    eh=poisson.pmf(np.arange(n),le); ea=poisson.pmf(np.arange(n),lr); eh/=eh.sum(); ea/=ea.sum()
    ET=np.outer(eh,ea); out=np.array(Mx)
    for k in range(n):
        m=Mx[k,k]
        if m<=0: continue
        out[k,k]-=m
        for dh in range(n-k):
            for da in range(n-k):
                out[k+dh,k+da]+=m*ET[dh,da]
    return out/out.sum()
def wdl(M): return np.array([float(np.tril(M,-1).sum()), float(np.trace(M)), float(np.triu(M,1).sum())])
def market120_draw(v90,v120,mkt):
    rho=v120[1]/v90[1]; return mkt[1]*rho  # ET-transformed market draw (model rho)

# LEDGER: (home, away, market90 [H,D,A], observed_120_draw)  observed: 1=draw(went to ET/pens), 0=decided, None=unplayed
LEDGER=[
 # --- R32 (played) ---
 ('South Africa','Canada',[0.173,0.272,0.555], 0),   # Canada 0-1
 ('Brazil','Japan',       [0.556,0.254,0.190], 0),   # Brazil 2-1
 ('Germany','Paraguay',   [0.70,0.19,0.11],    1),   # 1-1 (to pens)
 ('Netherlands','Morocco',[0.445,0.290,0.266], 1),   # 1-1 (to pens)
 # --- R16 (priced 2026-06-30, results pending) ---
 ('Ivory Coast','Norway', [0.271,0.279,0.451], None),
 ('France','Sweden',      [0.751,0.162,0.087], None),
 ('Mexico','Ecuador',     [0.444,0.308,0.248], None),
 ('England','DR Congo',   [0.758,0.168,0.074], None),
]

print(f"{'match':28} {'mod120D':>8} {'mkt120D':>8} {'bl120D':>7} {'obs':>4}")
print('-'*60)
pred_blend=[]; obs=[]; pred_model=[]
for th,ta,mkt,o in LEDGER:
    Mx,lh,la=joint90(th,ta); m120=transform120(Mx,lh,la)
    v90=wdl(Mx); v120=wdl(m120)
    mkt=np.array(mkt,float); mD=market120_draw(v90,v120,mkt)
    blD=0.4*v120[1]+0.6*mD
    tag='-' if o is None else ('DRAW' if o==1 else 'dec')
    print(f"{th+'-'+ta:28} {v120[1]*100:7.1f}% {mD*100:7.1f}% {blD*100:6.1f}% {tag:>5}")
    if o is not None:
        pred_blend.append(blD); pred_model.append(v120[1]); obs.append(o)

pb=np.array(pred_blend); pm=np.array(pred_model); ob=np.array(obs)
n=len(ob); D=int(ob.sum()); E=pb.sum(); Em=pm.sum()
print('-'*60)
print(f"PLAYED n={n} | observed draws D={D} | E[D] blend={E:.2f} (model={Em:.2f})")
# Poisson-binomial pmf via DP for the two-sided tail p-value
def pb_pmf(ps):
    dist=np.array([1.0])
    for p in ps:
        dist=np.convolve(dist,[1-p,p])
    return dist
if n>0:
    dist=pb_pmf(pb); ks=np.arange(n+1)
    pmf_D=dist[D]
    two=float(dist[dist<=pmf_D+1e-12].sum())  # two-sided: all outcomes at least as unlikely
    # also the simple "P(>=D)" upper tail
    upper=float(dist[D:].sum())
    print(f"Poisson-binomial: P(exactly D)={pmf_D:.3f} | P(>=D)={upper:.3f} | two-sided p={two:.3f}")
    print(f"ratio D/E[D] = {D/E:.2f}" + ("  (draws over-running prediction)" if D>E else "  (draws under prediction)"))
    print("\nPRE-REGISTERED GATE: act on phi ONLY if n>=12 AND ratio>1.5 AND two-sided p<0.05 AND Tier-1 validates.")
    if n<12:
        print(f"  -> n={n} < 12: WATCH-ONLY. Underpowered. No action. (need {12-n} more KO results.)")
