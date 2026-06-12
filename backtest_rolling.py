"""Q1: rolling-origin validation of the deployed temper (gamma=1.5).
At each origin t: fit att/def on matches < t (recency weights rel. to t, no peeking),
pick gamma* on train grid, evaluate 1X2 logloss on the following 6 months.
Question: does gamma~1.5 transfer through time, or was it an artifact of k-fold time-mixing?"""
import csv, json, numpy as np
from datetime import date
from scipy.optimize import minimize
from scipy.stats import nbinom
R_NB=9.5; MAXG=12; RIDGE=8.0; HALF=2.5
rows=list(csv.DictReader(open('intl_results.csv',encoding='utf-8')))
recs=[]
def imp(t):
    t=t.lower()
    if 'friendly' in t: return 0.6
    if any(k in t for k in ['world cup','euro','copa am','cup of nations','nations cup']) and 'qualif' not in t: return 1.2
    return 1.0
for r in rows:
    if r['date']<'2021-01-01' or r['home_score'] in ('NA','') : continue
    try: hs,as_=int(r['home_score']),int(r['away_score'])
    except: continue
    recs.append((r['date'],r['home_team'],r['away_team'],hs,as_,r['neutral'].upper()=='TRUE',imp(r['tournament'])))
teams=sorted({x[1] for x in recs}|{x[2] for x in recs}); idx={t:i for i,t in enumerate(teams)}; T=len(teams)
D=np.array([x[0] for x in recs]); H=np.array([idx[x[1]] for x in recs]); A=np.array([idx[x[2]] for x in recs])
HG=np.array([x[3] for x in recs]); AG=np.array([x[4] for x in recs])
HF=np.array([0. if x[5] else 1. for x in recs]); IW=np.array([x[6] for x in recs])

def age_w(dates,origin):
    o=date(*map(int,origin.split('-')))
    return np.array([0.5**((((o-date(*map(int,d.split('-')))).days)/365.25)/HALF) for d in dates])

def fit_ad(mask,w):
    h,a,hg,ag,hf=H[mask],A[mask],HG[mask],AG[mask],HF[mask]
    sc=np.concatenate([h,a]);cc=np.concatenate([a,h]);y=np.concatenate([hg,ag]).astype(float)
    hm=np.concatenate([hf,np.zeros_like(hf)]);ww=np.concatenate([w,w])
    def nll(p):
        mu,hgm=p[0],p[1];att=p[2:2+T];dff=p[2+T:]
        lam=np.exp(np.clip(mu+att[sc]-dff[cc]+hgm*hm,-4,4))
        val=np.sum(ww*(lam-y*np.log(lam)))+RIDGE*(att@att+dff@dff)
        r=ww*(lam-y);g=np.zeros_like(p);g[0]=r.sum();g[1]=(r*hm).sum()
        np.add.at(g,2+sc,r);g[2:2+T]+=2*RIDGE*att;np.add.at(g,2+T+cc,-r);g[2+T:]+=2*RIDGE*dff
        return val,g
    p0=np.zeros(2+2*T);p0[0]=np.log(1.3)
    return minimize(nll,p0,jac=True,method='L-BFGS-B',options=dict(maxiter=500)).x

KG=np.arange(MAXG+1)
def ll_1x2(p,mask,gamma):
    mu,hgm=p[0],p[1];att=p[2:2+T];dff=p[2+T:]
    lh=np.clip(np.exp(mu+att[H[mask]]-dff[A[mask]]+hgm*HF[mask]),0.05,7)
    la=np.clip(np.exp(mu+att[A[mask]]-dff[H[mask]]),0.05,7)
    Mm=0.5*(np.log(lh)+np.log(la)); Dd=0.5*(np.log(lh)-np.log(la))
    lh,la=np.exp(Mm+gamma*Dd),np.exp(Mm-gamma*Dd)
    out=[]
    hg,ag=HG[mask],AG[mask]
    for i in range(len(lh)):
        vh=nbinom.pmf(KG,R_NB,R_NB/(R_NB+lh[i])); vh/=vh.sum()
        va=nbinom.pmf(KG,R_NB,R_NB/(R_NB+la[i])); va/=va.sum()
        Mx=np.outer(vh,va)
        ph,pd,pa=np.tril(Mx,-1).sum(),np.trace(Mx),np.triu(Mx,1).sum()
        o=ph if hg[i]>ag[i] else (pd if hg[i]==ag[i] else pa)
        out.append(-np.log(max(o,1e-12)))
    return np.array(out)

GRID=[1.0,1.15,1.3,1.45,1.6,1.75]
origins=[('2024-07-01','2025-01-01'),('2025-01-01','2025-07-01'),('2025-07-01','2026-01-01'),('2026-01-01','2026-06-11')]
print(f"{'origin':<12}{'n_tr':>6}{'n_te':>6}{'g*train':>9}{'g*test':>8}   test-LL @ g=1.0 / 1.5 / g*train")
summ=[]
for o,end in origins:
    tr=(D<o)&(D>='2021-06-01'); te=(D>=o)&(D<end)
    w=age_w(D[tr],o)*IW[tr]
    p=fit_ad(tr,w)
    tr_ll={g:ll_1x2(p,tr,g).mean() for g in GRID}      # train-optimal (in-sample for gamma only)
    gstar_tr=min(tr_ll,key=tr_ll.get)
    te_ll={g:ll_1x2(p,te,g).mean() for g in GRID}
    gstar_te=min(te_ll,key=te_ll.get)
    summ.append((o,gstar_tr,gstar_te,te_ll))
    print(f"{o:<12}{tr.sum():>6}{te.sum():>6}{gstar_tr:>9.2f}{gstar_te:>8.2f}   "
          f"{te_ll[1.0]:.4f} / {te_ll[1.45]:.4f} / {te_ll[gstar_tr]:.4f}")
# aggregate: average test logloss by gamma across origins
print('\naggregate test 1X2 logloss by gamma (mean over 4 origins):')
for g in GRID:
    print(f'  gamma={g:<5} {np.mean([s[3][g] for s in summ]):.4f}')
