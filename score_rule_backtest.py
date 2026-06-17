"""Backtest: does an EMPIRICAL-tier E[bonus] score-optimizer beat the deployed MODAL rule
in REALIZED bonus points? Design (Verify-Std #2: hold everything else identical):
 - condition on the TRUE outcome (score rule only matters when outcome is already right);
 - each rule picks ONE score within that outcome region from the v6 model distribution;
 - realized bonus = the KNOWN realized tier of the actual score IFF pick == actual, else 0
   (base reward is outcome-determined and identical across rules -> excluded).
 - empirical tier table built LEAVE-ONE-OUT (exclude the match being scored) -> no self-grading.
Rules compared:
   MODAL-STEP  deployed: argmax p(s); if (1,1) step to next-highest-p.
   MODAL-RAW   argmax p(s) including 1-1.
   EMP         argmax p(s) * tier_hat(archetype(s))  [the thing the user proposes].
"""
import json, numpy as np
from scipy.stats import nbinom
AD=json.load(open('attdef.json')); W2C=json.load(open('wc_to_canon.json')); DP=json.load(open('deployed_params.json'))
mug=AD['_meta']['mu_goals']; R=DP['R']; MAXG=DP['MAXG']; GAMMA=DP['GAMMA']
def lam_pair(th,ta):
    lh=np.exp(mug+AD[W2C[th]]['ATT']-AD[W2C[ta]]['DEF']); la=np.exp(mug+AD[W2C[ta]]['ATT']-AD[W2C[th]]['DEF'])
    M=0.5*(np.log(lh)+np.log(la)); D=0.5*(np.log(lh)-np.log(la))
    return float(np.clip(np.exp(M+GAMMA*D),0.08,6)),float(np.clip(np.exp(M-GAMMA*D),0.08,6))
def nbv(lam):
    p=R/(R+lam); v=nbinom.pmf(np.arange(MAXG+1),R,p); return v/v.sum()

# (home, away, actual_score, realized_tier)  -- the 20 calibration obs
OBS=[('Mexico','South Africa',(2,0),20),('South Korea','Czech Republic',(2,1),20),
 ('Canada','Bosnia and Herzegovina',(1,1),20),('United States','Paraguay',(4,1),100),
 ('Qatar','Switzerland',(1,1),20),('Brazil','Morocco',(1,1),20),('Haiti','Scotland',(0,1),50),
 ('Germany','Curacao',(7,1),100),('Australia','Turkey',(2,0),50),('Netherlands','Japan',(2,2),20),
 ('Ivory Coast','Ecuador',(1,0),30),('Sweden','Tunisia',(5,1),100),('Spain','Cape Verde',(0,0),50),
 ('Belgium','Egypt',(1,1),20),('Saudi Arabia','Uruguay',(1,1),20),('Iran','New Zealand',(2,2),50),
 ('Iraq','Norway',(1,4),70),('Argentina','Algeria',(3,0),50),('Austria','Jordan',(3,1),50),
 ('France','Senegal',(3,1),30)]

def region(score):
    a,b=score
    return 0 if a>b else (1 if a==b else 2)

def archetype(score):
    """coarse score class for empirical tiering (kept simple; n=20)."""
    a,b=score; mar=abs(a-b); tot=a+b
    if a==b:
        return f'draw-{a}{b}' if tot<=4 else 'draw-hi'
    if tot>=5 or mar>=3: return 'tail'         # 4-1,5-1,7-1,1-4,3-0(mar3)...
    if mar==2: return 'win-2gap'               # 2-0,3-1
    return 'win-1gap'                          # 1-0,2-1

def emp_tier(arch, exclude_idx):
    """LOO mean realized tier for an archetype, excluding match exclude_idx.
    Fallback to global mean if archetype unseen elsewhere."""
    ts=[t for j,(_,_,s,t) in enumerate(OBS) if j!=exclude_idx and archetype(s)==arch]
    if ts: return float(np.mean(ts))
    allt=[t for j,(_,_,_,t) in enumerate(OBS) if j!=exclude_idx]
    return float(np.mean(allt))

# ---- build the empirical table (full sample, for display) ----
from collections import defaultdict
tab=defaultdict(list)
for _,_,s,t in OBS: tab[archetype(s)].append(t)
print('=== EMPIRICAL TIER TABLE (realized, full sample) ===')
for k in sorted(tab):
    v=tab[k]; print(f'  {k:<9} n={len(v)}  tiers={sorted(v)}  mean={np.mean(v):5.1f}  sd={np.std(v):4.1f}')
print('  NOTE heterogeneity: same exact score, different realized tier (context-dependent):')
print('   2-0 Mexico=20 vs Australia=50 | 2-2 NL=20 vs Iran=50 | 3-1 Austria=50 vs France=30')
print()

def pick_modal(M, reg, step_11=True):
    cells=[(a,b) for a in range(MAXG+1) for b in range(MAXG+1) if region((a,b))==reg]
    cells.sort(key=lambda s:-M[s])
    if step_11 and cells[0]==(1,1) and len(cells)>1: return cells[1]
    return cells[0]

def pick_emp(M, reg, idx):
    cells=[(a,b) for a in range(MAXG+1) for b in range(MAXG+1) if region((a,b))==reg and M[(a,b)]>0.01]
    return max(cells, key=lambda s: M[s]*emp_tier(archetype(s), idx))

tot={'MODAL-STEP':0,'MODAL-RAW':0,'EMP':0}; hits={'MODAL-STEP':0,'MODAL-RAW':0,'EMP':0}
ebonus_model={'MODAL-STEP':0.0,'EMP':0.0}
print('=== PER-MATCH (conditioned on true outcome) ===')
print(f"{'match':<26}{'actual':>7}{'tier':>5} | {'MODAL-STEP':>11}{'MODAL-RAW':>11}{'EMP':>7}")
for idx,(h,a,act,tier) in enumerate(OBS):
    lh,la=lam_pair(h,a); M=np.outer(nbv(lh),nbv(la)); M=M/M.sum()
    M={(i,j):M[i,j] for i in range(MAXG+1) for j in range(MAXG+1)}
    reg=region(act)
    pms=pick_modal(M,reg,True); pmr=pick_modal(M,reg,False); pe=pick_emp(M,reg,idx)
    for nm,pk in [('MODAL-STEP',pms),('MODAL-RAW',pmr),('EMP',pe)]:
        if pk==act: tot[nm]+=tier; hits[nm]+=1
    # model-expected bonus the rule TARGETS (uses LOO emp tiers) -- not realized
    ebonus_model['MODAL-STEP']+=M[pms]*emp_tier(archetype(pms),idx)
    ebonus_model['EMP']+=M[pe]*emp_tier(archetype(pe),idx)
    mk=lambda pk:f"{pk[0]}-{pk[1]}{'*' if pk==act else ' '}"
    print(f"{h+'-'+a:<26}{str(act[0])+'-'+str(act[1]):>7}{tier:>5} | {mk(pms):>11}{mk(pmr):>11}{mk(pe):>7}")

n=len(OBS)
print()
print('=== TOTALS over',n,'matches (realized bonus; * = exact hit) ===')
for nm in ['MODAL-STEP','MODAL-RAW','EMP']:
    print(f"  {nm:<11} realized bonus = {tot[nm]:4d}   exact hits = {hits[nm]:2d}   avg/match = {tot[nm]/n:4.1f}")
print()
print('=== MODEL-EXPECTED bonus the rule TARGETS (LOO emp tiers; the non-realized view) ===')
for nm in ['MODAL-STEP','EMP']:
    print(f"  {nm:<11} sum E[bonus] = {ebonus_model[nm]:5.1f}   avg/match = {ebonus_model[nm]/n:4.2f}")
