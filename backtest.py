"""Backtest the core v2 premise: do xG-based att/def ratings predict held-out
actual MATCH RESULTS better than goals-based ratings? And does blending help?
Self-contained k-fold CV over the 314 StatsBomb matches. Metrics: RPS + log-loss on 1X2,
and log-loss on exact scoreline. Lower = better."""
import json, numpy as np
from datetime import date
from scipy.optimize import minimize
from scipy.stats import poisson

xg=json.load(open('sb_xg.json'))
TODAY=date(2026,6,11); HALF=2.5; RHO=-0.08; MAXG=10
rng=np.random.default_rng(0)

# build records once; response chosen later (goals vs xg)
teams=set(); rows=[]
for mid,m in xg.items():
    y,mo,d=map(int,m['date'].split('-')); age=(TODAY-date(y,mo,d)).days/365.25
    w=0.5**(age/HALF)
    teams.add(m['home']); teams.add(m['away'])
    rows.append(dict(mid=mid,h=m['home'],a=m['away'],hg=m['hg'],ag=m['ag'],
                     hxg=max(m['hxg'],1e-3),axg=max(m['axg'],1e-3),w=w))
teams=sorted(teams); idx={t:i for i,t in enumerate(teams)}; T=len(teams)

def fit(train, resp):
    # build long design from training matches
    ti=[];oi=[];y=[];hm=[];wt=[]
    for r in train:
        ti+=[idx[r['h']],idx[r['a']]]; oi+=[idx[r['a']],idx[r['h']]]
        if resp=='goals': y+=[r['hg'],r['ag']]
        else: y+=[r['hxg'],r['axg']]
        hm+=[1,0]; wt+=[r['w'],r['w']]
    ti=np.array(ti);oi=np.array(oi);y=np.clip(np.array(y,float),1e-3,None)
    hm=np.array(hm,float);wt=np.array(wt)
    rho=8.0
    def nll(p):
        mu,gam=p[0],p[1]; att=p[2:2+T]; dff=p[2+T:]
        eta=mu+att[ti]-dff[oi]+gam*hm; lam=np.exp(np.clip(eta,-4,4))
        val=np.sum(wt*(lam-y*np.log(lam)))+rho*(att@att+dff@dff)
        r=wt*(lam-y); g=np.zeros_like(p); g[0]=r.sum(); g[1]=(r*hm).sum()
        np.add.at(g,2+ti,r); g[2:2+T]+=2*rho*att
        np.add.at(g,2+T+oi,-r); g[2+T:]+=2*rho*dff
        return val,g
    p0=np.zeros(2+2*T); p0[0]=np.log(max(y.mean(),0.3))
    p=minimize(nll,p0,jac=True,method='L-BFGS-B',options=dict(maxiter=400)).x
    return p

def lam_pred(p,h,a):
    mu,gam=p[0],p[1]; att=p[2:2+T]; dff=p[2+T:]
    lh=np.exp(mu+att[idx[h]]-dff[idx[a]]+gam*1)
    la=np.exp(mu+att[idx[a]]-dff[idx[h]]+gam*0)
    return float(np.clip(lh,0.05,7)),float(np.clip(la,0.05,7))

def dcmatrix(lh,la):
    x=poisson.pmf(np.arange(MAXG+1),lh);y=poisson.pmf(np.arange(MAXG+1),la);M=np.outer(x,y)
    M[0,0]*=1-lh*la*RHO;M[0,1]*=1+lh*RHO;M[1,0]*=1+la*RHO;M[1,1]*=1-RHO;M/=M.sum();return M
def probs_1x2(M):
    return np.tril(M,-1).sum(),np.trace(M),np.triu(M,1).sum()  # H,D,A

def score_match(M,hg,ag):
    H,D,A=probs_1x2(M); eps=1e-12
    if hg>ag: out,oi_=0,np.array([1,0,0])
    elif hg==ag: out,oi_=1,np.array([0,1,0])
    else: out,oi_=2,np.array([0,0,1])
    p=np.array([H,D,A]); ll=-np.log(max(p[out],eps))
    # RPS for ordered 3-outcome
    cp=np.cumsum(p); co=np.cumsum(oi_); rps=np.sum((cp-co)**2)/2
    # exact score log-loss (cap indices)
    hh=min(hg,MAXG); aa=min(ag,MAXG); lle=-np.log(max(M[hh,aa],eps))
    return ll,rps,lle

# ---- k-fold ----
order=rng.permutation(rows); K=5
folds=[order[i::K] for i in range(K)]
res={m:{'ll':[],'rps':[],'lle':[]} for m in ['goals','xg','blend']}
for f in range(K):
    test=folds[f]; train=[r for i in range(K) if i!=f for r in folds[i]]
    pg=fit(train,'goals'); px=fit(train,'xg')
    for r in test:
        lhg,lag=lam_pred(pg,r['h'],r['a']); Mg=dcmatrix(lhg,lag)
        lhx,lax=lam_pred(px,r['h'],r['a']); Mx=dcmatrix(lhx,lax)
        Mb=(Mg+Mx)/2; Mb/=Mb.sum()
        for name,M in [('goals',Mg),('xg',Mx),('blend',Mb)]:
            ll,rps,lle=score_match(M,r['hg'],r['ag'])
            res[name]['ll'].append(ll);res[name]['rps'].append(rps);res[name]['lle'].append(lle)

# baseline: global base rates of H/D/A
base=np.zeros(3)
for r in rows:
    base[0 if r['hg']>r['ag'] else (1 if r['hg']==r['ag'] else 2)]+=1
base/=base.sum()
bll=[];brps=[]
for r in rows:
    out=0 if r['hg']>r['ag'] else (1 if r['hg']==r['ag'] else 2)
    bll.append(-np.log(base[out])); oi_=np.eye(3)[out]
    brps.append(np.sum((np.cumsum(base)-np.cumsum(oi_))**2)/2)

print(f"{'model':<8}{'1X2 logloss':>13}{'1X2 RPS':>10}{'score logloss':>15}")
print(f"{'base':<8}{np.mean(bll):>13.4f}{np.mean(brps):>10.4f}{'-':>15}")
for m in ['goals','xg','blend']:
    print(f"{m:<8}{np.mean(res[m]['ll']):>13.4f}{np.mean(res[m]['rps']):>10.4f}{np.mean(res[m]['lle']):>15.4f}")
n=len(res['goals']['ll'])
# paired improvement of blend & xg vs goals (RPS), with bootstrap CI
def boot(a,b):
    a=np.array(a);b=np.array(b);d=a-b;bs=[np.mean(rng.choice(d,len(d))) for _ in range(2000)]
    return np.mean(d),np.percentile(bs,2.5),np.percentile(bs,97.5)
for m in ['xg','blend']:
    md,lo,hi=boot(res['goals']['rps'],res[m]['rps'])
    print(f"RPS improvement {m} vs goals: {md:+.4f}  95% CI [{lo:+.4f},{hi:+.4f}]  (n={n})")
