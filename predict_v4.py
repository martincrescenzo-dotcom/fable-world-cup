"""v4 predictions from the 2-D attack/defence model. All 72 group scores + tables."""
import json, numpy as np
from scipy.stats import poisson
rng=np.random.default_rng(4)
AD=json.load(open('attdef.json')); WC=json.load(open('wc_data.json'))
W2C=json.load(open('wc_to_canon.json'))
mug=AD['_meta']['mu_goals']; RHO=-0.08; MAXG=10
HOSTS={'Mexico','Canada','United States'}
def AT(t): return AD[W2C[t]]['ATT'];
def DF(t): return AD[W2C[t]]['DEF']
def lambdas(th,ta):  # neutral venue; host edge already in prior-anchored strength
    lh=np.exp(mug+AD[W2C[th]]['ATT']-AD[W2C[ta]]['DEF'])
    la=np.exp(mug+AD[W2C[ta]]['ATT']-AD[W2C[th]]['DEF'])
    return float(np.clip(lh,0.1,6)),float(np.clip(la,0.1,6))
def smatrix(lh,la):
    x=poisson.pmf(np.arange(MAXG+1),lh);y=poisson.pmf(np.arange(MAXG+1),la);M=np.outer(x,y)
    M[0,0]*=1-lh*la*RHO;M[0,1]*=1+lh*RHO;M[1,0]*=1+la*RHO;M[1,1]*=1-RHO;M/=M.sum();return M
def msum(th,ta):
    lh,la=lambdas(th,ta);M=smatrix(lh,la)
    ph=np.tril(M,-1).sum();pd=np.trace(M);pa=np.triu(M,1).sum()
    f=sorted(((M[a,b],a,b) for a in range(MAXG+1) for b in range(MAXG+1)),reverse=True)
    return dict(ph=ph,pd=pd,pa=pa,xa=lh,xb=la,ml=(f[0][1],f[0][2],f[0][0]),tot=lh+la)
FIX=[(0,1),(2,3),(0,2),(3,1),(3,0),(1,2)];MD=[1,1,2,2,3,3]
def lam2(ra,rb): return None
def simfull(teams,N):
    pts=np.zeros((N,4));gf=np.zeros((N,4));ga=np.zeros((N,4))
    for a,b in FIX:
        lh,la=lambdas(teams[a],teams[b]);ga_=rng.poisson(lh,N);gb_=rng.poisson(la,N)
        gf[:,a]+=ga_;ga[:,a]+=gb_;gf[:,b]+=gb_;ga[:,b]+=ga_
        wa=ga_>gb_;wb=gb_>ga_;dr=~(wa|wb);pts[wa,a]+=3;pts[wb,b]+=3;pts[dr,a]+=1;pts[dr,b]+=1
    gd=gf-ga;key=pts*1e6+gd*1e3+gf+rng.random((N,4))*1e-3
    order=np.argsort(-key,axis=1);rank=np.empty((N,4),int)
    for r in range(4): rank[np.arange(N),order[:,r]]=r
    return pts,gd,gf,rank
N=200000; groups=sorted(WC); pos={};exp_pts={};tp=[];tgd=[];tgf=[];tt=[]
for g in groups:
    teams=[t['team'] for t in WC[g]]
    pts,gd,gf,rank=simfull(teams,N)
    for i,t in enumerate(teams): pos[t]=np.bincount(rank[:,i],minlength=4)/N; exp_pts[t]=pts[:,i].mean()
    thi=np.argmax(rank==2,axis=1);ix=np.arange(N)
    tp.append(pts[ix,thi]);tgd.append(gd[ix,thi]);tgf.append(gf[ix,thi]);tt.append([teams[k] for k in thi])
tp=np.array(tp).T;tgd=np.array(tgd).T;tgf=np.array(tgf).T;tt=np.array(tt).T
key3=tp*1e6+tgd*1e3+tgf+rng.random((N,12))*1e-3;o3=np.argsort(-key3,axis=1)[:,:8]
a3={t:0 for t in pos}
for k in range(8):
    nm=tt[np.arange(N),o3[:,k]]
    for t in set(nm.tolist()): a3[t]+=int((nm==t).sum())
advance={t:pos[t][0]+pos[t][1]+a3[t]/N for t in pos}

def lab(t): return t+(" \U0001F3E0" if t in HOSTS else "")
L=["# FIFA World Cup 2026 — Group-Stage SCORE Predictions (v4: 2-D attack/defence)",""]
L.append("**Engine v4:** unified attack/defence generative model. Each team has separate ATT & DEF "
         "ratings fit jointly on recent international **goals** (all 48 teams) + **StatsBomb xG** (precision); "
         "overall strength anchored to the market-calibrated prior, the att/def split & scoring level learned "
         "from data. Scoreline = Dixon-Coles bivariate Poisson. This breaks the 1-D ceiling: total goals now "
         "depends on the *profiles*, not just the gap.")
L.append("")
allm=[]
for g in groups:
    teams=[t['team'] for t in WC[g]]
    L.append(f"## Group {g}\n")
    L.append("| MD | Match | Predicted | Prob | Left W / D / Right W | xG (λ) | Total |")
    L.append("|----|-------|-----------|------|----------------------|--------|-------|")
    for (a,b),md in zip(FIX,MD):
        ta,tb=teams[a],teams[b];m=msum(ta,tb);sa,sb,sp=m['ml']
        L.append(f"| {md} | **{lab(ta)}** vs **{lab(tb)}** | **{sa}–{sb}** | {sp*100:.0f}% | "
                 f"{m['ph']*100:.0f}% / {m['pd']*100:.0f}% / {m['pa']*100:.0f}% | {m['xa']:.2f}–{m['xb']:.2f} | {m['tot']:.2f} |")
        allm.append((g,md,ta,tb,sa,sb,sp,m['tot']))
    L.append("")
    L.append("| Team | xPts | Win% | Top-2% | Advance% |")
    L.append("|------|------|------|--------|----------|")
    for t in sorted(teams,key=lambda x:-advance[x]):
        pc=pos[t]; L.append(f"| {lab(t)} | {exp_pts[t]:.2f} | {pc[0]*100:.0f}% | {(pc[0]+pc[1])*100:.0f}% | {advance[t]*100:.0f}% |")
    L.append("")
open('PREDICTIONS_v4.md','w',encoding='utf-8').write('\n'.join(L))
json.dump({'advance':advance,'pos':{t:pos[t].tolist() for t in pos}},open('qualification_v4.json','w'))
# show how total-goals now varies (the new capability)
print('Highest & lowest predicted-total matches (new 2-D capability):')
allm.sort(key=lambda x:-x[7])
for g,md,ta,tb,sa,sb,sp,tot in allm[:5]+allm[-5:]:
    print(f'  {ta:>14} vs {tb:<14} pred {sa}-{sb}  total {tot:.2f}')
print('\nTop advancers v4:')
for t,p in sorted(advance.items(),key=lambda x:-x[1])[:10]:
    print(f'  {t:<14} adv {p*100:3.0f}%  win {pos[t][0]*100:3.0f}%')
print('wrote PREDICTIONS_v4.md')
