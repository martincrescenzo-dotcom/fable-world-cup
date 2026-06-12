"""Fork: EV-maximising pick for a points game.
Reward ~ C/prob (risky outcomes pay more). With a calibrated model, optimal pick =
argmax(p_model * reward). Edge = p_model / p_implied (where p_implied ∝ 1/reward)."""
import json, numpy as np
from scipy.stats import nbinom
AD=json.load(open('attdef.json')); W2C=json.load(open('wc_to_canon.json')); Q=json.load(open('qualification_v5.json'))
mug=AD['_meta']['mu_goals']; R=Q['r']; MAXG=12; GAMMA=1.5
def AT(t): return AD[W2C[t]]['ATT']
def DF(t): return AD[W2C[t]]['DEF']
def lam_pair(th,ta):
    lh=np.exp(mug+AT(th)-DF(ta)); la=np.exp(mug+AT(ta)-DF(th))
    M=0.5*(np.log(lh)+np.log(la)); D=0.5*(np.log(lh)-np.log(la))
    return float(np.exp(M+GAMMA*D)), float(np.exp(M-GAMMA*D))
def nbvec(lam):
    p=R/(R+lam); v=nbinom.pmf(np.arange(MAXG+1),R,p); return v/v.sum()
def wdl(th,ta):
    lh,la=lam_pair(th,ta); Mx=np.outer(nbvec(lh),nbvec(la)); Mx/=Mx.sum()
    return np.tril(Mx,-1).sum(), np.trace(Mx), np.triu(Mx,1).sum(), lh, la

# (home, away, [reward_home, reward_draw, reward_away])
games=[
 ('Mexico','South Africa',[49,125,148]),
 ('South Korea','Czech Republic',[96,107,91]),
 ('Canada','Bosnia and Herzegovina',[65,117,125]),
]
out=[]
for th,ta,rew in games:
    ph,pd,pa,lh,la=wdl(th,ta)
    pm=[ph,pd,pa]
    imp=np.array([1/r for r in rew]); imp=imp/imp.sum()           # game's implied probs
    ev=[pm[i]*rew[i] for i in range(3)]                            # expected points
    edge=[pm[i]/imp[i] for i in range(3)]                         # model vs game
    labels=[th,'Draw',ta]
    pick=int(np.argmax(ev))
    out.append((th,ta,labels,pm,imp,rew,ev,edge,pick,lh,la))

print(f"{'match':<34}{'outcome':<16}{'model':>7}{'implied':>8}{'reward':>7}{'EV':>7}{'edge':>6}")
for th,ta,labels,pm,imp,rew,ev,edge,pick,lh,la in out:
    for i in range(3):
        star=' <== PICK' if i==pick else ''
        mt=f'{th[:14]} v {ta[:10]}' if i==0 else ''
        print(f"{mt:<34}{labels[i]:<16}{pm[i]*100:>6.1f}%{imp[i]*100:>7.1f}%{rew[i]:>7}{ev[i]:>7.1f}{edge[i]:>6.2f}{star}")
    print()
# strategy summary
print('PICKS (max expected points):')
tot_ev=0
for th,ta,labels,pm,imp,rew,ev,edge,pick,lh,la in out:
    tot_ev+=ev[pick]
    safe=int(np.argmax(pm))
    note='value underdog/draw' if pick!=safe else 'favourite (still best EV)'
    print(f"  {th} v {ta:<22}-> {labels[pick]:<16} EV {ev[pick]:.1f} pts  (model {pm[pick]*100:.0f}%, reward {rew[pick]}, edge {edge[pick]:.2f})  [{note}]")
print(f"  total expected points over the 3 sample picks: {tot_ev:.1f}")
json.dump([{'home':th,'away':ta,'pick':labels[pick],'ev':ev[pick],'model_wdl':pm,'implied':list(imp),'reward':rew}
           for th,ta,labels,pm,imp,rew,ev,edge,pick,lh,la in out], open('forkbet_out.json','w'),indent=2)
