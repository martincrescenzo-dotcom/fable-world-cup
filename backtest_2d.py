"""Decisive test: does the 2nd dimension (separate ATT/DEF) improve SCORE prediction
out-of-sample? Nested models on identical goals data:
  1-D : ATT_i = DEF_i = c_i      (total goals = fixed fn of rating gap -> the ceiling)
  2-D : ATT_i, DEF_i free
5-fold CV. Metrics: exact-score log-loss, total-goals MAE, total-goals calibration
(corr of predicted vs actual total), 1X2 RPS."""
import json, numpy as np
from scipy.optimize import minimize
from scipy.stats import poisson
rng=np.random.default_rng(0)
G=json.load(open('goals_records.json'))
RHO=-0.08; MAXG=10; RIDGE=8.0

teams=sorted({r['h'] for r in G}|{r['a'] for r in G}); idx={t:i for i,t in enumerate(teams)}; T=len(teams)
H=np.array([idx[r['h']] for r in G]); A=np.array([idx[r['a']] for r in G])
HG=np.array([r['hg'] for r in G]); AG=np.array([r['ag'] for r in G])
HF=np.array([0.0 if r['neutral'] else 1.0 for r in G]); WG=np.array([r['w'] for r in G])

def fit(tr, two):
    h,a,hg,ag,hf,w=H[tr],A[tr],HG[tr],AG[tr],HF[tr],WG[tr]
    sc=np.concatenate([h,a]); cc=np.concatenate([a,h]); y=np.concatenate([hg,ag])
    hm=np.concatenate([hf,np.zeros_like(hf)]); ww=np.concatenate([w,w])
    if two:
        def nll(p):
            mu,hgm=p[0],p[1]; att=p[2:2+T]; dff=p[2+T:]
            lam=np.exp(np.clip(mu+att[sc]-dff[cc]+hgm*hm,-4,4))
            val=np.sum(ww*(lam-y*np.log(lam)))+RIDGE*(att@att+dff@dff)
            r=ww*(lam-y); g=np.zeros_like(p); g[0]=r.sum(); g[1]=(r*hm).sum()
            np.add.at(g,2+sc,r); g[2:2+T]+=2*RIDGE*att
            np.add.at(g,2+T+cc,-r); g[2+T:]+=2*RIDGE*dff
            return val,g
        p0=np.zeros(2+2*T); p0[0]=np.log(1.3)
        p=minimize(nll,p0,jac=True,method='L-BFGS-B',options=dict(maxiter=600)).x
        return ('2',p[0],p[1],p[2:2+T],p[2+T:])
    else:
        def nll(p):
            mu,hgm=p[0],p[1]; c=p[2:]
            lam=np.exp(np.clip(mu+c[sc]-c[cc]+hgm*hm,-4,4))
            val=np.sum(ww*(lam-y*np.log(lam)))+RIDGE*2*(c@c)
            r=ww*(lam-y); g=np.zeros_like(p); g[0]=r.sum(); g[1]=(r*hm).sum()
            np.add.at(g,2+sc,r); np.add.at(g,2+cc,-r); g[2:]+=4*RIDGE*c
            return val,g
        p0=np.zeros(2+T); p0[0]=np.log(1.3)
        p=minimize(nll,p0,jac=True,method='L-BFGS-B',options=dict(maxiter=600)).x
        return ('1',p[0],p[1],p[2:],p[2:])

def lam_of(model,h,a,hf):
    _,mu,hgm,att,dff=model
    lh=np.exp(mu+att[h]-dff[a]+hgm*hf); la=np.exp(mu+att[a]-dff[h])
    return np.clip(lh,0.05,7),np.clip(la,0.05,7)
def dc(lh,la):
    x=poisson.pmf(np.arange(MAXG+1),lh);y=poisson.pmf(np.arange(MAXG+1),la);M=np.outer(x,y)
    M[0,0]*=1-lh*la*RHO;M[0,1]*=1+lh*RHO;M[1,0]*=1+la*RHO;M[1,1]*=1-RHO;M/=M.sum();return M

N=len(G); order=rng.permutation(N); K=5; folds=[order[i::K] for i in range(K)]
out={m:{'sll':[],'terr':[],'pt':[],'at':[],'rps':[]} for m in ['1','2']}
for f in range(K):
    te=folds[f]; tr=np.concatenate([folds[i] for i in range(K) if i!=f])
    for two in (False,True):
        mdl=fit(tr,two); tag=mdl[0]
        for k in te:
            lh,la=lam_of(mdl,H[k],A[k],HF[k]); M=dc(lh,la)
            hh,aa=min(HG[k],MAXG),min(AG[k],MAXG)
            out[tag]['sll'].append(-np.log(max(M[hh,aa],1e-12)))
            pt=lh+la; out[tag]['terr'].append(abs(pt-(HG[k]+AG[k])))
            out[tag]['pt'].append(pt); out[tag]['at'].append(HG[k]+AG[k])
            Ph,Pd,Pa=np.tril(M,-1).sum(),np.trace(M),np.triu(M,1).sum()
            o=0 if HG[k]>AG[k] else (1 if HG[k]==AG[k] else 2); oi=np.eye(3)[o]
            out[tag]['rps'].append(np.sum((np.cumsum([Ph,Pd,Pa])-np.cumsum(oi))**2)/2)

print(f"{'model':<6}{'score logloss':>14}{'total-goal MAE':>16}{'pred-total corr':>17}{'1X2 RPS':>10}")
for m in ['1','2']:
    sll=np.mean(out[m]['sll']); mae=np.mean(out[m]['terr'])
    corr=np.corrcoef(out[m]['pt'],out[m]['at'])[0,1]; rps=np.mean(out[m]['rps'])
    name='1-D (gap only)' if m=='1' else '2-D (att/def)'
    print(f"{name:<6}{sll:>14.4f}{mae:>16.4f}{corr:>17.4f}{rps:>10.4f}")
# paired bootstrap on score-logloss improvement
d=np.array(out['1']['sll'])-np.array(out['2']['sll'])
bs=[np.mean(rng.choice(d,len(d))) for _ in range(3000)]
print(f"\nScore-logloss improvement 2-D vs 1-D: {d.mean():+.4f}  95% CI [{np.percentile(bs,2.5):+.4f},{np.percentile(bs,97.5):+.4f}]  (n={len(d)})")
ptv=np.std(out['1']['pt']),np.std(out['2']['pt'])
print(f"Std-dev of predicted totals: 1-D={ptv[0]:.3f}  2-D={ptv[1]:.3f}  (actual totals std={np.std(out['2']['at']):.3f})")
