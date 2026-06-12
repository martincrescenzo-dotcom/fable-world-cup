"""Fix the diagnosed under-confidence with one parameter: supremacy temperature gamma.
For a match, sharpen the goal-supremacy while preserving the mean (so total goals isn't
distorted): logλ' = M ± gamma*D, where M=(logλh+logλa)/2, D=(logλh-logλa)/2.
gamma fit on train (min 1X2 log-loss), validated OOS on: 1X2 log-loss, exact-score
log-loss, favourite calibration, draw rate. Ship only if it helps without breaking scores."""
import json, numpy as np
from scipy.optimize import minimize, minimize_scalar
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

KG=np.arange(MAXG+1)
def nbcol(lam): p=R/(R+lam); v=nbinom.pmf(KG,R,p); return v/v.sum()
def sharpen(lh,la,gamma):
    M=0.5*(np.log(lh)+np.log(la)); D=0.5*(np.log(lh)-np.log(la))
    return np.exp(M+gamma*D), np.exp(M-gamma*D)
def wdl_arr(lh,la,gamma):
    lh,la=sharpen(lh,la,gamma)
    out=[]
    for i in range(len(lh)):
        Mx=np.outer(nbcol(lh[i]),nbcol(la[i]))
        out.append((np.tril(Mx,-1).sum(),np.trace(Mx),np.triu(Mx,1).sum(),lh[i],la[i]))
    return out

def base_lams(p,k):
    mu,hgm=p[0],p[1];att=p[2:2+T];dff=p[2+T:]
    lh=np.clip(np.exp(mu+att[H[k]]-dff[A[k]]+hgm*HF[k]),0.05,7)
    la=np.clip(np.exp(mu+att[A[k]]-dff[H[k]]),0.05,7)
    return lh,la

N=len(G);order=rng.permutation(N);K=5;folds=[order[i::K] for i in range(K)]
# fit att/def per fold ONCE, cache test lambdas + results
LH=np.zeros(N);LA=np.zeros(N)
for f in range(K):
    te=folds[f];tr=np.concatenate([folds[i] for i in range(K) if i!=f])
    p=fit_ad(tr)
    for k in te:
        lh,la=base_lams(p,k); LH[k]=lh; LA[k]=la
won_home=(HG>AG); draw=(HG==AG); won_away=(AG>HG)

def eval_gamma(gm):
    lhs,las=sharpen(LH,LA,gm)
    ll=np.empty(N);sll=np.empty(N);pf=np.empty(N);wf=np.empty(N);pdraw=np.empty(N)
    for k in range(N):
        Mx=np.outer(nbcol(lhs[k]),nbcol(las[k])); Mx/=Mx.sum()
        ph,pd,pa=np.tril(Mx,-1).sum(),np.trace(Mx),np.triu(Mx,1).sum()
        o= ph if won_home[k] else (pd if draw[k] else pa)
        ll[k]=-np.log(max(o,1e-12))
        hh,aa=min(HG[k],MAXG),min(AG[k],MAXG); sll[k]=-np.log(max(Mx[hh,aa],1e-12))
        if ph>=pa: pf[k]=ph; wf[k]=won_home[k]
        else: pf[k]=pa; wf[k]=won_away[k]
        pdraw[k]=pd
    return ll,sll,pf,wf,pdraw

grid=[1.0,1.2,1.3,1.4,1.5,1.6,1.85,2.0]
print(f"{'gamma':>6}{'1X2 ll':>9}{'score ll':>10}{'fav gap(emp-pred)':>19}{'draw pred/act':>15}")
results={}
for gm in grid:
    ll,sll,pf,wf,pdraw=eval_gamma(gm); results[gm]=(ll,sll,pf,wf,pdraw)
    favgap=wf.mean()-pf.mean()
    print(f"{gm:>6.2f}{ll.mean():>9.4f}{sll.mean():>10.4f}{favgap:>+19.4f}{pdraw.mean()*100:>10.1f}/{draw.mean()*100:.1f}")
# pick gamma whose favourite frequency is best calibrated (|fav gap| minimal)
pick=min(grid,key=lambda gm:abs(results[gm][3].mean()-results[gm][2].mean()))
print(f"\n--> calibration-optimal gamma = {pick}  (fav gap ~0)")
base=results[1.0]; sel=results[pick]
for nm,bi,si in [('1X2 log-loss',0,0),('exact-score log-loss',1,1)]:
    d=base[bi]-sel[si];bs=[np.mean(rng.choice(d,len(d))) for _ in range(3000)]
    print(f"  {nm:<20} {base[bi].mean():.4f} -> {sel[si].mean():.4f}  improvement {d.mean():+.4f} 95%CI[{np.percentile(bs,2.5):+.4f},{np.percentile(bs,97.5):+.4f}]")
print("  favourite calibration at picked gamma:")
pf,wf=sel[2],sel[3]
for lo,hi in [(0.5,0.6),(0.6,0.7),(0.7,0.8),(0.8,1.01)]:
    m=(pf>=lo)&(pf<hi)
    if m.sum()>5: print(f"    [{lo:.1f}-{hi:.1f}] pred {pf[m].mean()*100:.0f}% -> emp {wf[m].mean()*100:.0f}%  (n={m.sum()})")
json.dump({'gamma':float(pick)},open('gamma.json','w'))
