"""Parameter-uncertainty propagation for the v2 hybrid.
- xG-leg uncertainty: bootstrap the 314 matches, refit att/def (warm-started).
- prior uncertainty: Gaussian sigma derived from Elo-vs-market disagreement.
For each ensemble member: rebuild hybrid ratings -> run all 12 groups (match noise)
-> record win% / top2% / advance%. Aggregate -> mean + 90% bands.
Output: UNCERTAINTY.md"""
import json, numpy as np
from datetime import date
from scipy.optimize import minimize
from scipy.stats import poisson

xg=json.load(open('sb_xg.json'))
RAT=json.load(open('ratings.json'))      # elo, mkt_rats, blend (prior)
XGR=json.load(open('xg_ratings.json'))   # for eff_n + full-sample strength
TODAY=date(2026,6,11); HALF=2.5; RHO=-0.08; BASE=np.log(1.32); B=0.70; MAXG=10
WMAX=0.35; KCONF=6.0; ELO_PER_STR=200.0/B
ALIAS={'Ivory Coast':"Côte d'Ivoire",'Cape Verde':'Cape Verde Islands','DR Congo':'Congo DR'}
def sb(t): return ALIAS.get(t,t)
rng=np.random.default_rng(2026)
HOSTS={'Mexico','Canada','United States'}

# ---- match records for bootstrap ----
M=list(xg.values())
teams=sorted({m['home'] for m in M}|{m['away'] for m in M})
idx={t:i for i,t in enumerate(teams)}; T=len(teams)
H=np.array([idx[m['home']] for m in M]); A=np.array([idx[m['away']] for m in M])
HXG=np.clip([m['hxg'] for m in M],1e-3,None); AXG=np.clip([m['axg'] for m in M],1e-3,None)
W=np.array([0.5**(((TODAY-date(*map(int,m['date'].split('-')))).days/365.25)/HALF) for m in M])
nM=len(M); RHO_PEN=3.0

def fit(sel_w, p0):
    # sel_w: per-match multiplier (bootstrap counts) * recency
    ww=np.repeat(sel_w*W,2)
    ti=np.empty(2*nM,int); oi=np.empty(2*nM,int); y=np.empty(2*nM); hm=np.empty(2*nM)
    ti[0::2]=H; ti[1::2]=A; oi[0::2]=A; oi[1::2]=H
    y[0::2]=HXG; y[1::2]=AXG; hm[0::2]=1; hm[1::2]=0
    def nll(p):
        mu,gam=p[0],p[1]; att=p[2:2+T]; dff=p[2+T:]
        lam=np.exp(np.clip(mu+att[ti]-dff[oi]+gam*hm,-4,4))
        val=np.sum(ww*(lam-y*np.log(lam)))+RHO_PEN*(att@att+dff@dff)
        r=ww*(lam-y); g=np.zeros_like(p); g[0]=r.sum(); g[1]=(r*hm).sum()
        np.add.at(g,2+ti,r); g[2:2+T]+=2*RHO_PEN*att
        np.add.at(g,2+T+oi,-r); g[2+T:]+=2*RHO_PEN*dff
        return val,g
    return minimize(nll,p0,jac=True,method='L-BFGS-B',options=dict(maxiter=300)).x

p_full=fit(np.ones(nM),np.zeros(2+2*T))   # warm-start base

# ---- fixed pieces: prior, eff_n, sigma_prior, Pbar ----
prior={}; offset={}; effn={}
for g in RAT:
    for i,t in enumerate(RAT[g]['teams']):
        prior[t]=RAT[g]['blend'][i]; offset[t]=RAT[g]['mkt_rats'][i]-RAT[g]['elo'][i]
        effn[t]=XGR.get(sb(t),{}).get('eff_n',0.0)
sigma_prior={t:np.sqrt(25**2+(0.5*offset[t])**2) for t in prior}
datateams=[t for t in prior if effn[t]>0]
Pbar=np.average([prior[t] for t in datateams],weights=[effn[t] for t in datateams])
def wconf(e): return WMAX*e/(e+KCONF)

# ---- group sim machinery (vectorised match noise) ----
FIX=[(0,1),(2,3),(0,2),(3,1),(3,0),(1,2)]
def lambdas(ra,rb):
    d=ra-rb; return np.clip(np.exp(BASE+B*d/400),0.12,6),np.clip(np.exp(BASE-B*d/400),0.12,6)
def group_outcomes(rats,N):
    rats=np.asarray(rats,float); pts=np.zeros((N,4));gf=np.zeros((N,4));ga=np.zeros((N,4))
    for a,b in FIX:
        la,lb=lambdas(rats[a],rats[b]); ga_=rng.poisson(la,N);gb_=rng.poisson(lb,N)
        gf[:,a]+=ga_;ga[:,a]+=gb_;gf[:,b]+=gb_;ga[:,b]+=ga_
        wa=ga_>gb_;wb=gb_>ga_;dr=~(wa|wb);pts[wa,a]+=3;pts[wb,b]+=3;pts[dr,a]+=1;pts[dr,b]+=1
    gd=gf-ga; key=pts*1e6+gd*1e3+gf+rng.random((N,4))*1e-3
    order=np.argsort(-key,axis=1); rank=np.empty((N,4),int)
    for r in range(4): rank[np.arange(N),order[:,r]]=r
    return pts,gd,gf,rank

groups=sorted(RAT); ENS=120; Ns=20000
win={t:[] for t in prior}; top2={t:[] for t in prior}; adv={t:[] for t in prior}

for b in range(ENS):
    # bootstrap xG strengths (skip resample on member 0 = point estimate)
    if b==0: p=p_full
    else:
        counts=rng.poisson(1.0,nM).astype(float)   # Poisson bootstrap weights
        p=fit(counts,p_full)
    att=p[2:2+T]; dff=p[2+T:]; strength={teams[i]:att[i]+dff[i] for i in range(T)}
    Sbar=np.average([strength[sb(t)] for t in datateams],weights=[effn[t] for t in datateams])
    # build perturbed hybrid ratings
    hyb={}
    for t in prior:
        h=prior[t]
        if effn[t]>0:
            xgElo=Pbar+ELO_PER_STR*(strength[sb(t)]-Sbar); w=wconf(effn[t])
            h=(1-w)*prior[t]+w*xgElo
        hyb[t]=h+rng.normal(0,sigma_prior[t])      # prior-uncertainty draw
    # sim all groups + best-third
    pos={}; tp=[];tgd=[];tgf=[];tt=[]
    for g in groups:
        ts=RAT[g]['teams']; pts,gd,gf,rank=group_outcomes([hyb[t] for t in ts],Ns)
        for i,t in enumerate(ts): pos[t]=np.bincount(rank[:,i],minlength=4)/Ns
        thi=np.argmax(rank==2,axis=1); ix=np.arange(Ns)
        tp.append(pts[ix,thi]);tgd.append(gd[ix,thi]);tgf.append(gf[ix,thi]);tt.append([ts[k] for k in thi])
    tp=np.array(tp).T;tgd=np.array(tgd).T;tgf=np.array(tgf).T;tt=np.array(tt).T
    key3=tp*1e6+tgd*1e3+tgf+rng.random((Ns,12))*1e-3; o3=np.argsort(-key3,axis=1)[:,:8]
    a3={t:0 for t in prior}
    for k in range(8):
        nm=tt[np.arange(Ns),o3[:,k]]
        for t in set(nm.tolist()): a3[t]+=int((nm==t).sum())
    for t in prior:
        win[t].append(pos[t][0]); top2[t].append(pos[t][0]+pos[t][1]); adv[t].append(pos[t][0]+pos[t][1]+a3[t]/Ns)
    if (b+1)%30==0: print('ensemble',b+1,'/',ENS)

def band(d): a=np.array(d); return a.mean(),np.percentile(a,5),np.percentile(a,95)

# ---- report ----
L=["# FIFA World Cup 2026 — Group-Stage Predictions with Honest Uncertainty (v3)",""]
L.append(f"**{ENS}-member ensemble** propagating xG-leg bootstrap + prior disagreement (sigma from |Elo-market|) "
         f"through match-level Monte-Carlo. Each cell = mean **[5th–95th percentile]** across ensemble. "
         f"Wide band = the model genuinely doesn't know.")
L.append("")
widths=[]
def lab(t): return t+(" \U0001F3E0" if t in HOSTS else "")
for g in groups:
    ts=RAT[g]['teams']
    L.append(f"## Group {g}\n")
    L.append("| Team | Win group | Top-2 | Advance (incl. 3rd) |")
    L.append("|------|-----------|-------|---------------------|")
    for t in sorted(ts,key=lambda x:-np.mean(adv[x])):
        wm,wl,wh=band(win[t]); t2m,_,_=band(top2[t]); am,al,ah=band(adv[t])
        widths.append((ah-al,g,t))
        L.append(f"| {lab(t)} | {wm*100:.0f}% [{wl*100:.0f}–{wh*100:.0f}] | {t2m*100:.0f}% | "
                 f"{am*100:.0f}% [{al*100:.0f}–{ah*100:.0f}] |")
    L.append("")
# uncertainty leaderboard
widths.sort(reverse=True)
L.append("## Where the model is least certain (widest advance bands)\n")
L.append("| Team | Group | Advance band width |")
L.append("|------|-------|--------------------|")
for w_,g,t in widths[:12]:
    am,al,ah=band(adv[t]); L.append(f"| {t} | {g} | {al*100:.0f}–{ah*100:.0f}% (±{w_*50:.0f}) |")
open('UNCERTAINTY.md','w',encoding='utf-8').write('\n'.join(L))

print('\nMost-certain qualifiers (narrow high bands):')
for t in sorted(prior,key=lambda x:-np.mean(adv[x]))[:8]:
    am,al,ah=band(adv[t]); wm,wl,wh=band(win[t])
    print(f'  {t:<14} adv {am*100:3.0f}% [{al*100:3.0f}-{ah*100:3.0f}]   win {wm*100:3.0f}% [{wl*100:3.0f}-{wh*100:3.0f}]')
print('\nWidest-uncertainty teams:')
for w_,g,t in widths[:8]:
    am,al,ah=band(adv[t]); print(f'  {t:<14} ({g}) advance {am*100:3.0f}% [{al*100:3.0f}-{ah*100:3.0f}]')
print('\nwrote UNCERTAINTY.md')
