"""Coverage-aware hybrid: blend prior (Elo x market) with bottom-up xG strength,
weighted by per-team data confidence. Regenerate predictions + diff vs v1."""
import json, numpy as np
from scipy.stats import poisson
rng=np.random.default_rng(11)

PRIOR=json.load(open('ratings.json'))          # blend = Elo x market
XG=json.load(open('xg_ratings.json'))
BASE=np.log(1.32); B=0.70; RHO=-0.08; MAXG=10
WMAX=0.35; KCONF=6.0
ELO_PER_STR=200.0/B                              # self-consistent: log-xG-ratio -> Elo points (=286)
HOSTS={'Mexico','Canada','United States'}

# WC name -> StatsBomb name (only data teams need correct alias)
ALIAS={'Ivory Coast':"Côte d'Ivoire",'Cape Verde':'Cape Verde Islands','DR Congo':'Congo DR'}
def sbname(t): return ALIAS.get(t,t)

# gather data-rich WC teams
S={}; EFF={}
for g in PRIOR:
    for i,t in enumerate(PRIOR[g]['teams']):
        r=XG.get(sbname(t))
        if r and r.get('eff_n',0)>0:
            S[t]=r['strength']; EFF[t]=r['eff_n']

# centering anchors (eff-weighted over data-rich WC teams)
ts=list(S); wv=np.array([EFF[t] for t in ts]); sv=np.array([S[t] for t in ts])
priors=[]
for g in PRIOR:
    for i,t in enumerate(PRIOR[g]['teams']):
        if t in S: priors.append(PRIOR[g]['blend'][i])
Pbar=np.average([PRIOR[g]['blend'][i] for g in PRIOR for i,t in enumerate(PRIOR[g]['teams']) if t in S],
                weights=[EFF[t] for g in PRIOR for t in PRIOR[g]['teams'] if t in S])
Sbar=np.average(sv,weights=wv)

def conf(eff): return WMAX*eff/(eff+KCONF)

# build hybrid ratings
H={}; diff=[]
for g in PRIOR:
    teams=PRIOR[g]['teams']; pr=PRIOR[g]['blend']; hyb=[]
    for i,t in enumerate(teams):
        if t in S:
            xgElo=Pbar+ELO_PER_STR*(S[t]-Sbar)
            w=conf(EFF[t])
            h=(1-w)*pr[i]+w*xgElo
        else:
            xgElo=float('nan'); w=0.0; h=pr[i]
        hyb.append(h)
        diff.append((t,g,pr[i],xgElo,EFF.get(t,0.0),w,h,h-pr[i]))
    H[g]=dict(teams=teams,prior=pr,hybrid=hyb)
json.dump(H,open('hybrid_ratings.json','w'),indent=2)

# ---------- scoreline + sim machinery ----------
KG=np.arange(0,16)
def lambdas(ra,rb):
    d=ra-rb
    return float(np.clip(np.exp(BASE+B*d/400),0.12,6)),float(np.clip(np.exp(BASE-B*d/400),0.12,6))
def smatrix(ra,rb):
    la,lb=lambdas(ra,rb)
    x=poisson.pmf(np.arange(MAXG+1),la);y=poisson.pmf(np.arange(MAXG+1),lb);M=np.outer(x,y)
    M[0,0]*=1-la*lb*RHO;M[0,1]*=1+la*RHO;M[1,0]*=1+lb*RHO;M[1,1]*=1-RHO;M/=M.sum();return M,la,lb
def msum(ra,rb):
    M,la,lb=smatrix(ra,rb)
    ph=np.tril(M,-1).sum();pd=np.trace(M);pa=np.triu(M,1).sum()
    f=sorted(((M[a,b],a,b) for a in range(MAXG+1) for b in range(MAXG+1)),reverse=True)
    return dict(ph=ph,pd=pd,pa=pa,xa=la,xb=lb,ml=(f[0][1],f[0][2],f[0][0]))
FIX=[(0,1),(2,3),(0,2),(3,1),(3,0),(1,2)];MD=[1,1,2,2,3,3]
def simfull(rats,N):
    rats=np.asarray(rats,float);pts=np.zeros((N,4));gf=np.zeros((N,4));ga=np.zeros((N,4))
    for a,b in FIX:
        la,lb=lambdas(rats[a],rats[b]);ga_=rng.poisson(la,N);gb_=rng.poisson(lb,N)
        gf[:,a]+=ga_;ga[:,a]+=gb_;gf[:,b]+=gb_;ga[:,b]+=ga_
        wa=ga_>gb_;wb=gb_>ga_;dr=~(wa|wb);pts[wa,a]+=3;pts[wb,b]+=3;pts[dr,a]+=1;pts[dr,b]+=1
    gd=gf-ga;key=pts*1e6+gd*1e3+gf+rng.random((N,4))*1e-3
    order=np.argsort(-key,axis=1);rank=np.empty((N,4),int)
    for r in range(4): rank[np.arange(N),order[:,r]]=r
    return pts,gd,gf,rank

N=200000
groups=sorted(H)
pos={};exp_pts={};tp=[];tgd=[];tgf=[];tt=[];tg={}
for g in groups:
    pts,gd,gf,rank=simfull(H[g]['hybrid'],N)
    for i,t in enumerate(H[g]['teams']):
        tg[t]=g;pos[t]=np.bincount(rank[:,i],minlength=4)/N;exp_pts[t]=pts[:,i].mean()
    thi=np.argmax(rank==2,axis=1);ix=np.arange(N)
    tp.append(pts[ix,thi]);tgd.append(gd[ix,thi]);tgf.append(gf[ix,thi]);tt.append([H[g]['teams'][k] for k in thi])
tp=np.array(tp).T;tgd=np.array(tgd).T;tgf=np.array(tgf).T;tt=np.array(tt).T
key3=tp*1e6+tgd*1e3+tgf+rng.random((N,12))*1e-3;o3=np.argsort(-key3,axis=1)[:,:8]
advthird={t:0 for t in tg}
for k in range(8):
    nm=tt[np.arange(N),o3[:,k]]
    for t in set(nm.tolist()): advthird[t]+=int((nm==t).sum())
advthird={t:v/N for t,v in advthird.items()}
advance={t:pos[t][0]+pos[t][1]+advthird[t] for t in tg}

# ---------- diff report (console) ----------
diff.sort(key=lambda x:-abs(x[7]))
print('Biggest hybrid moves vs prior (Elo x market):')
print(f"  {'team':<20}{'grp':>4}{'prior':>7}{'xgElo':>7}{'eff_n':>6}{'w':>6}{'hybrid':>8}{'delta':>7}")
for t,g,pr,xe,ef,w,h,dl in diff[:18]:
    xes=f'{xe:7.0f}' if xe==xe else '    n/a'
    print(f"  {t:<20}{g:>4}{pr:7.0f}{xes}{ef:6.1f}{w:6.2f}{h:8.0f}{dl:+7.0f}")

# ---------- write PREDICTIONS_v2.md ----------
L=["# FIFA World Cup 2026 — Group-Stage Predictions (v2: + bottom-up xG leg)",""]
L.append("**Engine v2:** three-signal hybrid — World-Football-Elo x Polymarket (top-down prior) "
         "blended with an opponent-adjusted, recency-weighted **StatsBomb shot-xG** attack/defence model "
         "(bottom-up), weighted per team by event-data confidence. Scorelines via Dixon-Coles bivariate "
         "Poisson; 200k-run Monte-Carlo for qualification incl. best-third race.")
L.append(f"*xG from 314 matches across WC2018/22, Euro2020/24, AFCON2023, Copa2024 (recency half-life 2.5y). "
         f"Conversion {ELO_PER_STR:.0f} Elo-pts per log-xG unit; max data weight {WMAX:.0%}.*")
L.append("")
def lab(t): return t+(" \U0001F3E0" if t in HOSTS else "")
for g in groups:
    teams=H[g]['teams'];rats=H[g]['hybrid']
    L.append(f"## Group {g}\n")
    L.append("| MD | Match | Predicted | Prob | Left W / D / Right W | xG |")
    L.append("|----|-------|-----------|------|----------------------|-----|")
    for (a,b),md in zip(FIX,MD):
        ta,tb=teams[a],teams[b];m=msum(rats[a],rats[b]);sa,sb,sp=m['ml']
        L.append(f"| {md} | **{lab(ta)}** vs **{lab(tb)}** | **{sa}–{sb}** | {sp*100:.0f}% | "
                 f"{m['ph']*100:.0f}% / {m['pd']*100:.0f}% / {m['pa']*100:.0f}% | {m['xa']:.2f}–{m['xb']:.2f} |")
    L.append("")
    order=sorted(teams,key=lambda t:-advance[t])
    L.append("| Team | xPts | Win% | Top-2% | Advance% |")
    L.append("|------|------|------|--------|----------|")
    for t in order:
        pc=pos[t]
        L.append(f"| {lab(t)} | {exp_pts[t]:.2f} | {pc[0]*100:.0f}% | {(pc[0]+pc[1])*100:.0f}% | {advance[t]*100:.0f}% |")
    L.append("")
open('PREDICTIONS_v2.md','w',encoding='utf-8').write('\n'.join(L))
json.dump({'advance':advance,'pos':{t:pos[t].tolist() for t in pos},'exp_pts':exp_pts},
          open('qualification_v2.json','w'),indent=2)
print('\nwrote PREDICTIONS_v2.md, hybrid_ratings.json, qualification_v2.json')
print('Top advancers v2:')
for t,p in sorted(advance.items(),key=lambda x:-x[1])[:12]:
    print(f'  {t:<20} adv {p*100:4.0f}%  win {pos[t][0]*100:3.0f}%')
