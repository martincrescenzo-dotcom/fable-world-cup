"""Does lambda-dependent NB dispersion beat the global r=9.5?
Market comparison says my tail is too fat in blowouts -> hypothesis: r should grow with lambda
(higher-scoring contexts closer to Poisson). Model: r(lam) = exp(a + c*log(lam)).
5-fold CV on 4,568 goals records; metric: held-out exact-score logloss + blowout-cell diagnostic."""
import json, numpy as np
from scipy.optimize import minimize
from scipy.stats import nbinom
rng=np.random.default_rng(0)
G=json.load(open('goals_records.json')); MAXG=12; RIDGE=8.0
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

def lams_of(p,kk):
    mu,hgm=p[0],p[1];att=p[2:2+T];dff=p[2+T:]
    lh=np.clip(np.exp(mu+att[H[kk]]-dff[A[kk]]+hgm*HF[kk]),0.05,7)
    la=np.clip(np.exp(mu+att[A[kk]]-dff[H[kk]]),0.05,7)
    return lh,la

def nb_ll(y,lam,r):
    p=r/(r+lam); return nbinom.logpmf(y,r,p)

def fit_disp(lam_tr,y_tr,w_tr,lam_dep):
    if lam_dep:
        def nll(x):
            a,c=x; r=np.exp(a+c*np.log(lam_tr)); r=np.clip(r,1.5,400)
            return -np.sum(w_tr*nb_ll(y_tr,lam_tr,r))
        res=minimize(nll,[np.log(9.5),0.0],method='Nelder-Mead',
                     options=dict(initial_simplex=[[np.log(9.5),0],[np.log(20),0],[np.log(9.5),1.0]],xatol=1e-3,fatol=1e-4))
        return res.x
    else:
        def nll(lr):
            r=np.exp(lr[0]); return -np.sum(w_tr*nb_ll(y_tr,lam_tr,np.full_like(lam_tr,r)))
        res=minimize(nll,[np.log(9.5)],method='Nelder-Mead')
        return res.x

N=len(G);order=rng.permutation(N);K=5;folds=[order[i::K] for i in range(K)]
LL={'global':[],'lamdep':[]}; LLblow={'global':[],'lamdep':[]}
pars=[]
for f in range(K):
    te=folds[f];tr=np.concatenate([folds[i] for i in range(K) if i!=f])
    p=fit_ad(tr)
    lh_tr,la_tr=lams_of(p,tr); lam_tr=np.concatenate([lh_tr,la_tr])
    y_tr=np.concatenate([HG[tr],AG[tr]]); w_tr=np.concatenate([WG[tr],WG[tr]])
    xg= fit_disp(lam_tr,y_tr,w_tr,False); rg=np.exp(xg[0])
    xl= fit_disp(lam_tr,y_tr,w_tr,True); a,c=xl
    pars.append((rg,a,c))
    lh_te,la_te=lams_of(p,te)
    for i,k in enumerate(te):
        hh,aa=min(HG[k],MAXG),min(AG[k],MAXG)
        for tag in ['global','lamdep']:
            if tag=='global':
                rh=rg; ra=rg
            else:
                rh=float(np.clip(np.exp(a+c*np.log(lh_te[i])),1.5,400))
                ra=float(np.clip(np.exp(a+c*np.log(la_te[i])),1.5,400))
            vh=nbinom.pmf(np.arange(MAXG+1),rh,rh/(rh+lh_te[i])); vh/=vh.sum()
            va=nbinom.pmf(np.arange(MAXG+1),ra,ra/(ra+la_te[i])); va/=va.sum()
            ll=-np.log(max(vh[hh]*va[aa],1e-12))
            LL[tag].append(ll)
            if HG[k]>=4 or AG[k]>=4: LLblow[tag].append(ll)

print('fold params (r_global | a,c of r=exp(a+c*ln lam)):')
for rg,a,c in pars: print(f'  r_glob={rg:5.1f} | a={a:5.2f} c={c:5.2f} -> r(0.8)={np.exp(a+c*np.log(0.8)):5.1f}  r(1.3)={np.exp(a+c*np.log(1.3)):5.1f}  r(2.5)={np.exp(a+c*np.log(2.5)):5.1f}  r(4.0)={np.exp(a+c*np.log(4.0)):5.1f}')
g=np.array(LL['global']); l=np.array(LL['lamdep'])
print(f'\\nexact-score logloss: global {g.mean():.5f}  lamdep {l.mean():.5f}')
d=g-l; bs=[np.mean(rng.choice(d,len(d))) for _ in range(3000)]
print(f'improvement lamdep: {d.mean():+.5f}  95% CI [{np.percentile(bs,2.5):+.5f},{np.percentile(bs,97.5):+.5f}]  n={len(d)}')
gb=np.array(LLblow['global']); lb=np.array(LLblow['lamdep'])
db=gb-lb; bsb=[np.mean(rng.choice(db,len(db))) for _ in range(3000)]
print(f'blowout matches (4+ goals by a side, n={len(db)}): improvement {db.mean():+.5f}  CI [{np.percentile(bsb,2.5):+.5f},{np.percentile(bsb,97.5):+.5f}]')
