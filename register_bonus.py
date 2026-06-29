"""Register realized bonus points -> calibrate the crowd model.
Each time the user hits an exact score, the awarded bonus reveals the BAND of the true
crowd share of that score (among correct-outcome pickers):
  +20 -> (0.30, 1.0] | +30 -> (0.20, 0.30] | +50 -> (0.05, 0.20] | +70 -> (0.005, 0.05] | +100 -> (0, 0.005]
Usage: edit NEW_OBS, run. With >=3 observations it grid-fits (beta, sal_strength) to put
estimated shares inside realized bands; otherwise it just checks consistency."""
import json, numpy as np
from scipy.stats import nbinom

NEW_OBS = [
    dict(match='Germany-Curacao', date='2026-06-14', home='Germany',
         away='Curacao', actual_score=(7,1), bonus_awarded=100),
    dict(match='Netherlands-Japan', date='2026-06-14', home='Netherlands',
         away='Japan', actual_score=(2,2), bonus_awarded=20),
    dict(match='Ivory Coast-Ecuador', date='2026-06-14', home='Ivory Coast',
         away='Ecuador', actual_score=(1,0), bonus_awarded=30),
    dict(match='Spain-Cape Verde', date='2026-06-15', home='Spain',
         away='Cape Verde', actual_score=(0,0), bonus_awarded=50),
    dict(match='Sweden-Tunisia', date='2026-06-14', home='Sweden',
         away='Tunisia', actual_score=(5,1), bonus_awarded=100),
    dict(match='Belgium-Egypt', date='2026-06-15', home='Belgium',
         away='Egypt', actual_score=(1,1), bonus_awarded=20),
    dict(match='Saudi Arabia-Uruguay', date='2026-06-15', home='Saudi Arabia',
         away='Uruguay', actual_score=(1,1), bonus_awarded=20),
    dict(match='Iran-New Zealand', date='2026-06-15', home='Iran',
         away='New Zealand', actual_score=(2,2), bonus_awarded=50),
    dict(match='Iraq-Norway', date='2026-06-16', home='Iraq',
         away='Norway', actual_score=(1,4), bonus_awarded=70),
    dict(match='Argentina-Algeria', date='2026-06-16', home='Argentina',
         away='Algeria', actual_score=(3,0), bonus_awarded=50),
    dict(match='Austria-Jordan', date='2026-06-16', home='Austria',
         away='Jordan', actual_score=(3,1), bonus_awarded=50),
    dict(match='France-Senegal', date='2026-06-16', home='France',
         away='Senegal', actual_score=(3,1), bonus_awarded=30),
    dict(match='Ghana-Panama', date='2026-06-17', home='Ghana',
         away='Panama', actual_score=(1,0), bonus_awarded=20),
    dict(match='Uzbekistan-Colombia', date='2026-06-17', home='Uzbekistan',
         away='Colombia', actual_score=(1,3), bonus_awarded=50),
    dict(match='Portugal-DR Congo', date='2026-06-16', home='Portugal',
         away='DR Congo', actual_score=(1,1), bonus_awarded=20),
    dict(match='England-Croatia', date='2026-06-17', home='England',
         away='Croatia', actual_score=(4,2), bonus_awarded=70),
    dict(match='Mexico-South Korea', date='2026-06-18', home='Mexico',
         away='South Korea', actual_score=(1,0), bonus_awarded=50),
    dict(match='Czechia-South Africa', date='2026-06-18', home='Czech Republic',
         away='South Africa', actual_score=(1,1), bonus_awarded=20),
    dict(match='Scotland-Morocco', date='2026-06-19', home='Scotland',
         away='Morocco', actual_score=(0,1), bonus_awarded=50),
    dict(match='Brazil-Haiti', date='2026-06-19', home='Brazil',
         away='Haiti', actual_score=(3,0), bonus_awarded=20),
    dict(match='Turkey-Paraguay', date='2026-06-19', home='Turkey',
         away='Paraguay', actual_score=(0,1), bonus_awarded=20),
    dict(match='USA-Australia', date='2026-06-19', home='United States',
         away='Australia', actual_score=(2,0), bonus_awarded=30),
    # MD7 (2026-06-20/21) realized tiers
    dict(match='Germany-Ivory Coast', date='2026-06-20', home='Germany',
         away='Ivory Coast', actual_score=(2,1), bonus_awarded=30),
    dict(match='Ecuador-Curacao', date='2026-06-20', home='Ecuador',
         away='Curacao', actual_score=(0,0), bonus_awarded=30),
    dict(match='Tunisia-Japan', date='2026-06-20', home='Tunisia',
         away='Japan', actual_score=(0,4), bonus_awarded=70),
    dict(match='Spain-Saudi Arabia', date='2026-06-21', home='Spain',
         away='Saudi Arabia', actual_score=(4,0), bonus_awarded=50),
    dict(match='Belgium-Iran', date='2026-06-21', home='Belgium',
         away='Iran', actual_score=(0,0), bonus_awarded=50),
    dict(match='Uruguay-Cape Verde', date='2026-06-21', home='Uruguay',
         away='Cape Verde', actual_score=(2,2), bonus_awarded=50),
    dict(match='New Zealand-Egypt', date='2026-06-21', home='New Zealand',
         away='Egypt', actual_score=(1,3), bonus_awarded=50),
    # MD8 (2026-06-22) realized tiers
    dict(match='Argentina-Austria', date='2026-06-22', home='Argentina',
         away='Austria', actual_score=(2,0), bonus_awarded=30),
    dict(match='France-Iraq', date='2026-06-22', home='France',
         away='Iraq', actual_score=(3,0), bonus_awarded=20),
    dict(match='Norway-Senegal', date='2026-06-22', home='Norway',
         away='Senegal', actual_score=(3,2), bonus_awarded=50),
    dict(match='Jordan-Algeria', date='2026-06-22', home='Jordan',
         away='Algeria', actual_score=(1,2), bonus_awarded=30),
    # MD9 (2026-06-23) realized tiers — first 3 (Switzerland-Canada, Bosnia-Qatar pending)
    dict(match='England-Ghana', date='2026-06-23', home='England',
         away='Ghana', actual_score=(0,0), bonus_awarded=50),
    dict(match='Panama-Croatia', date='2026-06-23', home='Panama',
         away='Croatia', actual_score=(0,1), bonus_awarded=50),
    dict(match='Colombia-DR Congo', date='2026-06-23', home='Colombia',
         away='DR Congo', actual_score=(1,0), bonus_awarded=50),
    # MD10 (2026-06-25) realized tiers — 6 of 8 (Norway-France, Senegal-Iraq pending)
    dict(match='Ecuador-Germany', date='2026-06-25', home='Ecuador',
         away='Germany', actual_score=(2,1), bonus_awarded=20),
    dict(match='Curacao-Ivory Coast', date='2026-06-25', home='Curacao',
         away='Ivory Coast', actual_score=(0,2), bonus_awarded=20),
    dict(match='Tunisia-Netherlands', date='2026-06-25', home='Tunisia',
         away='Netherlands', actual_score=(1,3), bonus_awarded=50),
    dict(match='Japan-Sweden', date='2026-06-25', home='Japan',
         away='Sweden', actual_score=(1,1), bonus_awarded=20),
    dict(match='Turkey-United States', date='2026-06-25', home='Turkey',
         away='United States', actual_score=(3,2), bonus_awarded=70),
    dict(match='Paraguay-Australia', date='2026-06-25', home='Paraguay',
         away='Australia', actual_score=(0,0), bonus_awarded=50),
    # MD10 tail + MD11 (2026-06-26) realized tiers (organizer emails)
    dict(match='Norway-France', date='2026-06-26', home='Norway',
         away='France', actual_score=(1,4), bonus_awarded=70),
    dict(match='Senegal-Iraq', date='2026-06-26', home='Senegal',
         away='Iraq', actual_score=(5,0), bonus_awarded=100),
    dict(match='Uruguay-Spain', date='2026-06-26', home='Uruguay',
         away='Spain', actual_score=(0,1), bonus_awarded=70),
    dict(match='Cape Verde-Saudi Arabia', date='2026-06-26', home='Cape Verde',
         away='Saudi Arabia', actual_score=(0,0), bonus_awarded=30),
    dict(match='New Zealand-Belgium', date='2026-06-26', home='New Zealand',
         away='Belgium', actual_score=(1,5), bonus_awarded=100),
    dict(match='Egypt-Iran', date='2026-06-26', home='Egypt',
         away='Iran', actual_score=(1,1), bonus_awarded=20),
    # R32 KO (2026-06-28) — bonus on the 120' scoreline, pens ignored
    dict(match='South Africa-Canada (R32)', date='2026-06-28', home='South Africa',
         away='Canada', actual_score=(0,1), bonus_awarded=50),
]

BAND={20:(0.30,1.0),30:(0.20,0.30),50:(0.05,0.20),70:(0.005,0.05),100:(0.0,0.005)}
obs=json.load(open('crowd_obs.json'))
seen={(o['match'],tuple(o['actual_score'])) for o in obs}
for o in NEW_OBS:
    key=(o['match'],tuple(o['actual_score']))
    if key in seen:
        print(f'SKIP duplicate: {key} already registered (re-run protection)')
        continue
    o['share_band']=list(BAND[o['bonus_awarded']])
    obs.append(o); seen.add(key)
json.dump(obs,open('crowd_obs.json','w'),indent=2)
print(f'{len(obs)} observation(s) total.')

AD=json.load(open('attdef.json')); W2C=json.load(open('wc_to_canon.json')); DP=json.load(open('deployed_params.json'))
mug=AD['_meta']['mu_goals']; R=DP['R']; MAXG=DP['MAXG']; GAMMA=DP['GAMMA']
SAL={(1,0):1.5,(2,0):1.5,(2,1):1.6,(3,0):1.0,(3,1):0.75,(4,0):0.45,(4,1):0.4,(3,2):0.5,
     (1,1):1.7,(0,0):0.55,(2,2):0.9,(3,3):0.3}
def lam_pair(th,ta):
    lh=np.exp(mug+AD[W2C[th]]['ATT']-AD[W2C[ta]]['DEF']); la=np.exp(mug+AD[W2C[ta]]['ATT']-AD[W2C[th]]['DEF'])
    M=0.5*(np.log(lh)+np.log(la)); D=0.5*(np.log(lh)-np.log(la))
    return np.exp(M+GAMMA*D),np.exp(M-GAMMA*D)
def nbv(lam):
    p=R/(R+lam); v=nbinom.pmf(np.arange(MAXG+1),R,p); return v/v.sum()

import os
_SN=json.load(open('winamax_snapshots.json')) if os.path.exists('winamax_snapshots.json') else {}
def share_est(o,beta,sstr):
    """estimated crowd share of the actual score, on the SAME plausibility base matchday.py
    deploys: de-vigged Winamax snapshot when one exists for the match, else model probs."""
    th=o.get('home') or o['match'].split('-')[0]; ta=o.get('away') or o['match'].split('-')[1]
    a0,b0=o['actual_score']
    lh,la=lam_pair(th,ta); M=np.outer(nbv(lh),nbv(la)); M/=M.sum()
    if a0>b0: cells=[(a,b) for a in range(MAXG+1) for b in range(MAXG+1) if a>b]
    elif a0==b0: cells=[(a,a) for a in range(MAXG+1)]
    else: cells=[(a,b) for a in range(MAXG+1) for b in range(MAXG+1) if a<b]
    bk=None
    key=f'{th}|{ta}'
    if key in _SN:
        s_=_SN[key][-1]
        bk={tuple(map(int,sc.split('-'))):1.0/od for sc,od in s_['odds'].items() if sc!='Autre'}
    plaus=[]
    for a,b in cells:
        if bk and (a,b) in bk: plaus.append(bk[(a,b)])
        elif bk: plaus.append(M[a,b]*sum(bk.values())/(sum(M[x,y] for x,y in bk)))
        else: plaus.append(M[a,b])
    plaus=np.array(plaus)
    def s(a,b):
        v=SAL.get((a,b),SAL.get((b,a),0.25 if (a+b)>=5 else 0.6)); return v**sstr
    cr=(plaus**beta)*np.array([s(a,b) for a,b in cells]); cr/=cr.sum()
    return float(cr[cells.index((a0,b0))])

def loss(beta,sstr):
    L=0.0
    for o in obs:
        c=share_est(o,beta,sstr); lo,hi=o['share_band']
        if c<lo: L+=(lo-c)**2
        elif c>hi: L+=(c-hi)**2
    return L

cur=json.load(open('crowd_params.json'))
print(f"current params beta={cur['beta']} sal_strength={cur['sal_strength']}  loss={loss(cur['beta'],cur['sal_strength']):.5f}")
for o in obs:
    c=share_est(o,cur['beta'],cur['sal_strength']); lo,hi=o['share_band']
    ok='OK' if lo<=c<=hi else 'VIOLATED'
    print(f"  {o['match']} {o['actual_score']}: est {c*100:.1f}% vs band [{lo*100:.1f},{hi*100:.1f}]%  {ok}")
violated=any(not (o['share_band'][0]<=share_est(o,cur['beta'],cur['sal_strength'])<=o['share_band'][1]) for o in obs)
if len(obs)>=15:   # 2026-06-14: refit GATED to >=15 obs. Per-obs refit chased noise on a misfit form
                   # (beta swung 1.6<->1.0 on single results); coarse BONUS_MODE makes fine params ~irrelevant.
    grid_b=[1.0,1.1,1.25,1.4,1.6,1.8]; grid_s=[0.5,0.75,1.0,1.25,1.5]
    best=min(((loss(b,s),b,s) for b in grid_b for s in grid_s))
    if best[0]<loss(cur['beta'],cur['sal_strength'])-1e-9:
        cur['beta'],cur['sal_strength']=best[1],best[2]
        json.dump(cur,open('crowd_params.json','w'),indent=2)
        print(f"REFIT -> beta={best[1]} sal_strength={best[2]} (loss {best[0]:.5f}). matchday.py will use these.")
        for o in obs:
            c=share_est(o,cur['beta'],cur['sal_strength']); lo,hi=o['share_band']
            print(f"  post-refit {o['match']} {o['actual_score']}: est {c*100:.1f}% vs [{lo*100:.0f},{hi*100:.0f}]%  {'OK' if lo<=c<=hi else 'STILL OUT'}")
    else:
        print('grid cannot improve — params kept; flag persists.')
else:
    print(f'{len(obs)} obs logged. Refit GATED to >=15 obs + OOS validation (2026-06-14); coarse BONUS_MODE — fine params barely affect picks.')
