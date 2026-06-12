"""Rarity-bonus optimizer for the points game.
E[total] = p(outcome)*base + p(score)*tier(crowd_share(score | outcome pickers)).
Crowd model (FRENCH recreational players, judgment layer — NOT validated):
  crowd(s) ∝ p_model(s)^BETA * salience(s), normalised within the outcome region.
  BETA>1: crowds concentrate harder than reality on modal scores.
  salience: iconic scores (2-1,1-0,2-0,1-1) over-picked; 0-0 and 'weird' scores under-picked.
Tiers: >30%:+20 | 20-30%:+30 | 5-20%:+50 | 0.5-5%:+70 | <0.5%:+100."""
import json, numpy as np
from scipy.stats import nbinom
AD=json.load(open('attdef.json')); W2C=json.load(open('wc_to_canon.json')); Q=json.load(open('qualification_v5.json'))
mug=AD['_meta']['mu_goals']; R=Q['r']; MAXG=8; GAMMA=1.5
BETA=1.25
SAL={(1,0):1.5,(2,0):1.5,(2,1):1.6,(3,0):1.0,(3,1):0.75,(4,0):0.45,(4,1):0.4,(3,2):0.5,
     (1,1):1.7,(0,0):0.55,(2,2):0.9,(3,3):0.3}
def sal(a,b):
    if (a,b) in SAL: return SAL[(a,b)]
    if (b,a) in SAL: return SAL[(b,a)]
    return 0.25 if (a+b)>=5 else 0.6
def tier(share):
    if share>0.30: return 20
    if share>0.20: return 30
    if share>0.05: return 50
    if share>0.005: return 70
    return 100
def AT(t): return AD[W2C[t]]['ATT']
def DF(t): return AD[W2C[t]]['DEF']
def lam_pair(th,ta):
    lh=np.exp(mug+AT(th)-DF(ta)); la=np.exp(mug+AT(ta)-DF(th))
    M=0.5*(np.log(lh)+np.log(la)); D=0.5*(np.log(lh)-np.log(la))
    return float(np.exp(M+GAMMA*D)), float(np.exp(M-GAMMA*D))
def nbv(lam):
    p=R/(R+lam); v=nbinom.pmf(np.arange(MAXG+1),R,p); return v/v.sum()

def analyse(th,ta,rew,overlay=(0,0,0,0)):
    """rew=[home,draw,away]; overlay=(dATTh,dDEFh,dATTa,dDEFa) from live_updates."""
    lh,la=lam_pair(th,ta)
    lh*=np.exp(overlay[0]+ -overlay[3]); la*=np.exp(overlay[2]+ -overlay[1])
    M=np.outer(nbv(lh),nbv(la)); M/=M.sum()
    ph,pd,pa=np.tril(M,-1).sum(),np.trace(M),np.triu(M,1).sum()
    pm=[ph,pd,pa]
    # outcome EV (base only)
    evb=[pm[i]*rew[i] for i in range(3)]
    regions={0:[(a,b) for a in range(MAXG+1) for b in range(MAXG+1) if a>b],
             1:[(a,a) for a in range(MAXG+1)],
             2:[(a,b) for a in range(MAXG+1) for b in range(MAXG+1) if a<b]}
    results={}
    for oi in range(3):
        cells=regions[oi]
        pmod=np.array([M[a,b] for a,b in cells])
        crowd=np.array([(M[a,b]**BETA)*sal(a,b) for a,b in cells]); crowd/=crowd.sum()
        rows=[]
        for k,(a,b) in enumerate(cells):
            t_=tier(crowd[k]); eb=pmod[k]*t_
            rows.append(dict(score=(a,b),p=float(pmod[k]),crowd=float(crowd[k]),tier=t_,ebonus=float(eb)))
        rows.sort(key=lambda r:-r['ebonus'])
        results[oi]=rows
    return dict(pm=pm,evb=evb,by_outcome=results,lams=(lh,la))

games=[('Mexico','South Africa',[49,125,148]),
       ('South Korea','Czech Republic',[96,107,91]),
       ('Canada','Bosnia and Herzegovina',[65,117,125])]
labels=lambda th,ta:[th,'Draw',ta]
for th,ta,rew in games:
    r=analyse(th,ta,rew)
    pm=r['pm']; evb=r['evb']
    # total EV per outcome = base EV + best score bonus EV
    print(f"=== {th} vs {ta}  (model W/D/L {pm[0]*100:.0f}/{pm[1]*100:.0f}/{pm[2]*100:.0f}) ===")
    best_total=[]
    for oi in range(3):
        rows=r['by_outcome'][oi]; b=rows[0]
        tot=evb[oi]+b['ebonus']
        best_total.append(tot)
        lab=labels(th,ta)[oi]
        print(f"  {lab:<16} baseEV {evb[oi]:5.1f} + bestBonusEV {b['ebonus']:4.1f} = {tot:5.1f}")
    pick=int(np.argmax(best_total))
    rows=r['by_outcome'][pick]
    print(f"  --> OUTCOME: {labels(th,ta)[pick]}")
    print(f"  score candidates within outcome (modal first 5 by bonus EV):")
    # also show the naive modal score for comparison
    naive=max(rows,key=lambda x:x['p'])
    for x in rows[:5]:
        a,b=x['score']; flag=' <== naive modal' if x is naive else ''
        print(f"    {a}-{b}: p={x['p']*100:4.1f}%  crowd~{x['crowd']*100:4.1f}%  tier +{x['tier']:<3} EbonusEV={x['ebonus']:4.2f}{flag}")
    print()
