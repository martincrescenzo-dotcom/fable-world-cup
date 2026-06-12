"""Structure test on the SCORELINE DISTRIBUTION (the literal exact-score target).
Per fold: fit 2-D att/def on train goals -> lambdas; then fit DC-correlation rho
and negative-binomial dispersion r on train; compare held-out exact-score log-loss for:
  P-indep | P-DC(-0.08 incumbent) | P-DC(fit) | NB(fit)-indep | NB(fit)+DC(fit)
Decision rule: adopt a variant only if it beats the incumbent out-of-sample (CI)."""
import json, numpy as np
from scipy.optimize import minimize, minimize_scalar
from scipy.stats import poisson, nbinom
rng=np.random.default_rng(0)
G=json.load(open('goals_records.json')); MAXG=10; RIDGE=8.0
teams=sorted({r['h'] for r in G}|{r['a'] for r in G}); idx={t:i for i,t in enumerate(teams)}; T=len(teams)
H=np.array([idx[r['h']] for r in G]); A=np.array([idx[r['a']] for r in G])
HG=np.array([r['hg'] for r in G]); AG=np.array([r['ag'] for r in G])
HF=np.array([0.0 if r['neutral'] else 1.0 for r in G]); WG=np.array([r['w'] for r in G])

def fit_ad(tr):
    h,a,hg,ag,hf,w=H[tr],A[tr],HG[tr],AG[tr],HF[tr],WG[tr]
    sc=np.concatenate([h,a]); cc=np.concatenate([a,h]); y=np.concatenate([hg,ag])
    hm=np.concatenate([hf,np.zeros_like(hf)]); ww=np.concatenate([w,w])
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
    return p[0],p[1],p[2:2+T],p[2+T:]

def lams(mu,hgm,att,dff,tr):
    lh=np.exp(np.clip(mu+att[H[tr]]-dff[A[tr]]+hgm*HF[tr],-4,4))
    la=np.exp(np.clip(mu+att[A[tr]]-dff[H[tr]],-4,4))
    return np.clip(lh,0.05,7),np.clip(la,0.05,7)

def tau(h,a,lh,la,rho):
    t=np.ones_like(lh)
    m=(h==0)&(a==0); t[m]=1-lh[m]*la[m]*rho
    m=(h==0)&(a==1); t[m]=1+lh[m]*rho
    m=(h==1)&(a==0); t[m]=1+la[m]*rho
    m=(h==1)&(a==1); t[m]=1-rho
    return np.clip(t,1e-6,None)

def nb_pmf(k,mu,r):
    p=r/(r+mu); return nbinom.pmf(k,r,p)

def cell_ll(hg,ag,lh,la,dist,rho,r):
    hg=np.minimum(hg,MAXG); ag=np.minimum(ag,MAXG)
    if dist=='P': ph=poisson.pmf(hg,lh); pa=poisson.pmf(ag,la)
    else: ph=nb_pmf(hg,lh,r); pa=nb_pmf(ag,la,r)
    j=ph*pa
    if rho is not None: j=j*tau(hg,ag,lh,la,rho)
    return -np.log(np.clip(j,1e-12,None))

def fit_rho(hg,ag,lh,la,dist,r):
    f=lambda rho: cell_ll(hg,ag,lh,la,dist,rho,r).sum()
    return minimize_scalar(f,bounds=(-0.18,0.18),method='bounded').x
def fit_r(hg,ag,lh,la):
    f=lambda lr: (cell_ll(hg,ag,lh,la,'NB',None,np.exp(lr))).sum()
    return np.exp(minimize_scalar(f,bounds=(np.log(2),np.log(200)),method='bounded').x)

N=len(G); order=rng.permutation(N); K=5; folds=[order[i::K] for i in range(K)]
variants=['P-indep','P-DC(-0.08)','P-DC(fit)','NB-indep','NB+DC(fit)']
LL={v:[] for v in variants}; rhos=[]; rs=[]
for f in range(K):
    te=folds[f]; tr=np.concatenate([folds[i] for i in range(K) if i!=f])
    mu,hgm,att,dff=fit_ad(tr)
    lh_tr,la_tr=lams(mu,hgm,att,dff,tr); lh_te,la_te=lams(mu,hgm,att,dff,te)
    hg_tr,ag_tr=HG[tr],AG[tr]; hg_te,ag_te=HG[te],AG[te]
    rho_p=fit_rho(hg_tr,ag_tr,lh_tr,la_tr,'P',None)
    r_nb=fit_r(hg_tr,ag_tr,lh_tr,la_tr)
    rho_nb=fit_rho(hg_tr,ag_tr,lh_tr,la_tr,'NB',r_nb)
    rhos.append(rho_p); rs.append(r_nb)
    LL['P-indep']  += list(cell_ll(hg_te,ag_te,lh_te,la_te,'P',None,None))
    LL['P-DC(-0.08)']+=list(cell_ll(hg_te,ag_te,lh_te,la_te,'P',-0.08,None))
    LL['P-DC(fit)']+= list(cell_ll(hg_te,ag_te,lh_te,la_te,'P',rho_p,None))
    LL['NB-indep'] += list(cell_ll(hg_te,ag_te,lh_te,la_te,'NB',None,r_nb))
    LL['NB+DC(fit)']+=list(cell_ll(hg_te,ag_te,lh_te,la_te,'NB',rho_nb,r_nb))

print(f'fitted rho (mean) = {np.mean(rhos):+.3f}   NB dispersion r (mean) = {np.mean(rs):.1f}  (r->inf = Poisson)')
print(f"\n{'variant':<14}{'exact-score logloss':>22}")
base=np.array(LL['P-DC(-0.08)'])
for v in variants:
    a=np.array(LL[v]); print(f'{v:<14}{a.mean():>22.5f}')
print('\nvs incumbent P-DC(-0.08), paired bootstrap (positive = better than incumbent):')
for v in variants:
    if v=='P-DC(-0.08)': continue
    d=base-np.array(LL[v]); bs=[np.mean(rng.choice(d,len(d))) for _ in range(3000)]
    flag='  <-- improves' if np.percentile(bs,2.5)>0 else ('  (ns)' if np.percentile(bs,97.5)>0 else '  WORSE')
    print(f'  {v:<14} {d.mean():+.5f}  95% CI [{np.percentile(bs,2.5):+.5f},{np.percentile(bs,97.5):+.5f}]{flag}')
