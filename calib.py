"""Does the model assign the RIGHT upset frequency? Out-of-sample calibration of the
favourite's win probability, with focus on the heavy-favourite tail (where Saudi-Argentina
type shocks live). If empirical < predicted in the top bins -> overconfident -> under-accounts
for upsets."""
import json, numpy as np
from scipy.optimize import minimize
from scipy.stats import nbinom
rng=np.random.default_rng(0)
G=json.load(open('goals_records.json')); MAXG=12; RIDGE=8.0; R=9.5
teams=sorted({r['h'] for r in G}|{r['a'] for r in G}); idx={t:i for i,t in enumerate(teams)}; T=len(teams)
H=np.array([idx[r['h']] for r in G]); A=np.array([idx[r['a']] for r in G])
HG=np.array([r['hg'] for r in G]); AG=np.array([r['ag'] for r in G])
HF=np.array([0.0 if r['neutral'] else 1.0 for r in G]); WG=np.array([r['w'] for r in G])

def fit_ad(tr):
    h,a,hg,ag,hf,w=H[tr],A[tr],HG[tr],AG[tr],HF[tr],WG[tr]
    sc=np.concatenate([h,a]);cc=np.concatenate([a,h]);y=np.concatenate([hg,ag])
    hm=np.concatenate([hf,np.zeros_like(hf)]);ww=np.concatenate([w,w])
    def nll(p):
        mu,hgm=p[0],p[1];att=p[2:2+T];dff=p[2+T:]
        lam=np.exp(np.clip(mu+att[sc]-dff[cc]+hgm*hm,-4,4))
        val=np.sum(ww*(lam-y*np.log(lam)))+RIDGE*(att@att+dff@dff)
        r=ww*(lam-y);g=np.zeros_like(p);g[0]=r.sum();g[1]=(r*hm).sum()
        np.add.at(g,2+sc,r);g[2:2+T]+=2*RIDGE*att;np.add.at(g,2+T+cc,-r);g[2+T:]+=2*RIDGE*dff
        return val,g
    p0=np.zeros(2+2*T);p0[0]=np.log(1.3)
    return minimize(nll,p0,jac=True,method='L-BFGS-B',options=dict(maxiter=600)).x
def nbv(lam):
    p=R/(R+lam);v=nbinom.pmf(np.arange(MAXG+1),R,p);return v/v.sum()
def wdl(lh,la):
    M=np.outer(nbv(lh),nbv(la));return np.tril(M,-1).sum(),np.trace(M),np.triu(M,1).sum()

N=len(G);order=rng.permutation(N);K=5;folds=[order[i::K] for i in range(K)]
pfav=[];wonfav=[]
for f in range(K):
    te=folds[f];tr=np.concatenate([folds[i] for i in range(K) if i!=f])
    p=fit_ad(tr);mu,hgm=p[0],p[1];att=p[2:2+T];dff=p[2+T:]
    for k in te:
        lh=np.clip(np.exp(mu+att[H[k]]-dff[A[k]]+hgm*HF[k]),0.05,7)
        la=np.clip(np.exp(mu+att[A[k]]-dff[H[k]]),0.05,7)
        ph,pd,pa=wdl(lh,la)
        if ph>=pa: pf=ph; won=HG[k]>AG[k]
        else: pf=pa; won=AG[k]>HG[k]
        pfav.append(pf);wonfav.append(won)
pfav=np.array(pfav);wonfav=np.array(wonfav).astype(float)

print(f"n={len(pfav)}  overall: mean predicted fav-win={pfav.mean():.3f}  empirical fav-win={wonfav.mean():.3f}")
print(f"\n{'pred fav-win bin':<18}{'n':>6}{'mean pred':>11}{'empirical':>11}{'gap':>8}")
bins=[(0.0,0.4),(0.4,0.5),(0.5,0.6),(0.6,0.7),(0.7,0.8),(0.8,0.9),(0.9,1.01)]
for lo,hi in bins:
    m=(pfav>=lo)&(pfav<hi);n=m.sum()
    if n<5: continue
    pm=pfav[m].mean();em=wonfav[m].mean()
    print(f"{f'{lo:.1f}-{hi:.1f}':<18}{n:>6}{pm:>11.3f}{em:>11.3f}{em-pm:>+8.3f}")
# heavy-favourite focus (Argentina-Saudi was ~0.85)
for thr in [0.75,0.80,0.85]:
    m=pfav>=thr
    print(f"\nfavourites with model prob >= {thr:.2f}:  n={m.sum()}  "
          f"model says they win {pfav[m].mean()*100:.0f}%, they actually won {wonfav[m].mean()*100:.0f}%  "
          f"-> real 'failed to win' rate {100-wonfav[m].mean()*100:.0f}% (model expected {100-pfav[m].mean()*100:.0f}%)")
