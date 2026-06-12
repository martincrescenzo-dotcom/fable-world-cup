"""Fit pooled opponent-adjusted attack/defence ratings on StatsBomb shot-xG.
Weighted penalized (ridge) quasi-Poisson, recency-decayed. CV-tuned shrinkage.
Output: xg_ratings.json  (team -> att, def, strength, eff_n)"""
import json, numpy as np
from datetime import date
from scipy.optimize import minimize

xg = json.load(open('sb_xg.json'))
TODAY = date(2026,6,11)
HALF = 2.5  # recency half-life (years)

# ---- build long records: (team, opp, y=xg_for, home, weight) ----
teams=set()
recs=[]
for mid,m in xg.items():
    y,mo,d = map(int, m['date'].split('-'))
    age = (TODAY - date(y,mo,d)).days/365.25
    w = 0.5**(age/HALF)
    for side,opp,yf,h in [('home','away',m['hxg'],1),('away','home',m['axg'],0)]:
        t=m[side]; o=m[opp]
        teams.add(t); teams.add(o)
        recs.append((t,o,float(yf),h,w))
teams=sorted(teams); idx={t:i for i,t in enumerate(teams)}; T=len(teams)
ti=np.array([idx[r[0]] for r in recs]); oi=np.array([idx[r[1]] for r in recs])
y=np.array([r[2] for r in recs]); hm=np.array([r[3] for r in recs],float); w=np.array([r[4] for r in recs])
# floor tiny xG so log works; xG>=0
y=np.clip(y,1e-3,None)

def unpack(p):
    mu=p[0]; gam=p[1]; att=p[2:2+T]; dff=p[2+T:2+2*T]
    return mu,gam,att,dff
def nll(p,rho):
    mu,gam,att,dff=unpack(p)
    eta=mu+att[ti]-dff[oi]+gam*hm
    lam=np.exp(np.clip(eta,-4,4))
    val=np.sum(w*(lam-y*np.log(lam))) + rho*(att@att+dff@dff)
    # gradient
    r=w*(lam-y)
    g=np.zeros_like(p)
    g[0]=r.sum(); g[1]=(r*hm).sum()
    np.add.at(g,2+ti,r); g[2:2+T]+=2*rho*att
    np.add.at(g,2+T+oi,-r); g[2+T:]+=2*rho*dff
    return val,g

def fit(rho,mask=None):
    global ti,oi,y,hm,w
    p0=np.zeros(2+2*T); p0[0]=np.log(max(y.mean(),0.3))
    res=minimize(lambda p: nll(p,rho),p0,jac=True,method='L-BFGS-B',
                 options=dict(maxiter=500))
    return res.x

# ---- CV to choose rho (hold out whole matches) ----
rng=np.random.default_rng(0)
midlist=list(xg.keys());
# map each record to its match for fold holdout
recmid=[]
for mid,m in xg.items():
    recmid+= [mid,mid]
recmid=np.array(recmid)
def cv(rho,folds=4):
    order=rng.permutation(midlist)
    errs=[]
    for f in range(folds):
        test_m=set(order[f::folds])
        test=np.array([rm in test_m for rm in recmid])
        tr=~test
        # fit on train subset
        def nll_sub(p):
            mu,gam,att,dff=unpack(p)
            eta=mu+att[ti[tr]]-dff[oi[tr]]+gam*hm[tr]
            lam=np.exp(np.clip(eta,-4,4))
            val=np.sum(w[tr]*(lam-y[tr]*np.log(lam)))+rho*(att@att+dff@dff)
            r=w[tr]*(lam-y[tr]); g=np.zeros_like(p)
            g[0]=r.sum(); g[1]=(r*hm[tr]).sum()
            np.add.at(g,2+ti[tr],r); g[2:2+T]+=2*rho*att
            np.add.at(g,2+T+oi[tr],-r); g[2+T:]+=2*rho*dff
            return val,g
        p0=np.zeros(2+2*T); p0[0]=np.log(max(y.mean(),0.3))
        p=minimize(nll_sub,p0,jac=True,method='L-BFGS-B',options=dict(maxiter=500)).x
        mu,gam,att,dff=unpack(p)
        eta=mu+att[ti[test]]-dff[oi[test]]+gam*hm[test]
        lam=np.exp(np.clip(eta,-4,4))
        errs.append(np.mean((lam-y[test])**2))
    return np.mean(errs)

grid=[3,6,12,25,50]
cvres={r:cv(r) for r in grid}
best=min(cvres,key=cvres.get)
print('CV MSE by rho:',{k:round(v,4) for k,v in cvres.items()},'-> best',best)

p=fit(best)
mu,gam,att,dff=unpack(p)
# effective sample per team (sum of weights over its records as attacker+defender)
eff=np.zeros(T)
np.add.at(eff,ti,w); np.add.at(eff,oi,w)
strength=att+dff   # both att and def parameters: higher = better (def suppresses opp xG)
out={teams[i]:dict(att=float(att[i]),dff=float(dff[i]),strength=float(strength[i]),
                   eff_n=float(eff[i])) for i in range(T)}
out['_meta']=dict(mu=float(mu),gamma=float(gam),rho=best,half_life=HALF)
json.dump(out,open('xg_ratings.json','w'),indent=2)

# report top/bottom by strength (ascii)
ranked=sorted(((strength[i],teams[i],eff[i]) for i in range(T)),reverse=True)
print('\nHome xG advantage gamma=%.3f  mu=%.3f'%(gam,mu))
print('Top 12 by net xG strength:')
for s,t,e in ranked[:12]: print(f'  {t:<22} str {s:+.2f}  eff_n {e:4.1f}')
print('Bottom 6:')
for s,t,e in ranked[-6:]: print(f'  {t:<22} str {s:+.2f}  eff_n {e:4.1f}')
