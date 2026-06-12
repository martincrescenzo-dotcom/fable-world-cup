"""v7 = v6 + explicit HOST home-field advantage for Mexico/USA/Canada.
Restores the empirically-estimated home effect (h_g, ~+0.3 goals scoring) that the
neutral-venue att/def + gamma layers had stripped. Applied to the host's scoring in
its (all-home) group matches; validated against the market's host-inclusive odds.
NOT applied: altitude/heat/travel (advised against — thin, market-captured)."""
import json, numpy as np
from scipy.stats import nbinom
rng=np.random.default_rng(7)
AD=json.load(open('attdef.json')); WC=json.load(open('wc_data.json'))
W2C=json.load(open('wc_to_canon.json')); Q=json.load(open('qualification_v5.json')); MK=json.load(open('market.json'))
mug=AD['_meta']['mu_goals']; R=Q['r']; MAXG=12; GAMMA=1.5
HOSTS={'Mexico','Canada','United States'}
HB=0.26   # host scoring boost (log). h_g=0.318 generic home adv, nudged down slightly (WC neutral-ish crowds vs club)
def AT(t): return AD[W2C[t]]['ATT']
def DF(t): return AD[W2C[t]]['DEF']
def lam_pair(th,ta):
    lh=np.exp(mug+AT(th)-DF(ta)); la=np.exp(mug+AT(ta)-DF(th))
    M=0.5*(np.log(lh)+np.log(la)); D=0.5*(np.log(lh)-np.log(la))
    lh,la=np.exp(M+GAMMA*D),np.exp(M-GAMMA*D)          # v6 recalibration
    if th in HOSTS: lh*=np.exp(HB)                      # host home advantage
    if ta in HOSTS: la*=np.exp(HB)
    return float(np.clip(lh,0.08,6)),float(np.clip(la,0.08,6))
def nbvec(lam):
    p=R/(R+lam); v=nbinom.pmf(np.arange(MAXG+1),R,p); return v/v.sum()
def msum(th,ta):
    lh,la=lam_pair(th,ta); M=np.outer(nbvec(lh),nbvec(la)); M/=M.sum()
    ph=np.tril(M,-1).sum();pd=np.trace(M);pa=np.triu(M,1).sum()
    f=sorted(((M[a,b],a,b) for a in range(MAXG+1) for b in range(MAXG+1)),reverse=True)
    return dict(ph=ph,pd=pd,pa=pa,xa=lh,xb=la,ml=(f[0][1],f[0][2],f[0][0]),tot=lh+la)
FIX=[(0,1),(2,3),(0,2),(3,1),(3,0),(1,2)];MD=[1,1,2,2,3,3]
def nbsample(lam,N): return rng.negative_binomial(R,R/(R+lam),N)
def simfull(teams,N):
    pts=np.zeros((N,4));gf=np.zeros((N,4));ga=np.zeros((N,4))
    for a,b in FIX:
        lh,la=lam_pair(teams[a],teams[b]);ga_=nbsample(lh,N);gb_=nbsample(la,N)
        gf[:,a]+=ga_;ga[:,a]+=gb_;gf[:,b]+=gb_;ga[:,b]+=ga_
        wa=ga_>gb_;wb=gb_>ga_;dr=~(wa|wb);pts[wa,a]+=3;pts[wb,b]+=3;pts[dr,a]+=1;pts[dr,b]+=1
    gd=gf-ga;key=pts*1e6+gd*1e3+gf+rng.random((N,4))*1e-3
    order=np.argsort(-key,axis=1);rank=np.empty((N,4),int)
    for r in range(4): rank[np.arange(N),order[:,r]]=r
    return pts,gd,gf,rank
N=200000; groups=sorted(WC); pos={};exp_pts={};tp=[];tgd=[];tgf=[];tt=[]
for g in groups:
    teams=[t['team'] for t in WC[g]]; pts,gd,gf,rank=simfull(teams,N)
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
L=["# FIFA World Cup 2026 — Group-Stage SCORE Predictions (v7, + host advantage)",""]
L.append(f"**Engine v7:** v6 (2-D att/def + NB + supremacy recalibration gamma={GAMMA}) plus an explicit "
         f"**host home-field advantage** (+{HB:.2f} log scoring, ~+0.3 goals) for Mexico/USA/Canada in their "
         f"group matches — restoring the empirically-fit home effect that the neutral-venue layers had stripped. "
         f"Altitude/heat/travel deliberately NOT modelled (thin signal, already market-captured).")
L.append("")
for g in groups:
    teams=[t['team'] for t in WC[g]]
    L.append(f"## Group {g}\n")
    L.append("| MD | Match | Predicted | Prob | Left W / D / Right W | xG (λ) | Total |")
    L.append("|----|-------|-----------|------|----------------------|--------|-------|")
    for (a,b),md in zip(FIX,MD):
        ta,tb=teams[a],teams[b];m=msum(ta,tb);sa,sb,sp=m['ml']
        L.append(f"| {md} | **{lab(ta)}** vs **{lab(tb)}** | **{sa}–{sb}** | {sp*100:.0f}% | "
                 f"{m['ph']*100:.0f}% / {m['pd']*100:.0f}% / {m['pa']*100:.0f}% | {m['xa']:.2f}–{m['xb']:.2f} | {m['tot']:.2f} |")
    L.append("")
    L.append("| Team | xPts | Win% | Top-2% | Advance% |")
    L.append("|------|------|------|--------|----------|")
    for t in sorted(teams,key=lambda x:-advance[x]):
        pc=pos[t]; L.append(f"| {lab(t)} | {exp_pts[t]:.2f} | {pc[0]*100:.0f}% | {(pc[0]+pc[1])*100:.0f}% | {advance[t]*100:.0f}% |")
    L.append("")
open('PREDICTIONS_v7.md','w',encoding='utf-8').write('\n'.join(L))
json.dump({'advance':advance,'pos':{t:pos[t].tolist() for t in pos},'host_boost':HB},open('qualification_v7.json','w'))
print(f"host boost HB={HB} (exp={np.exp(HB):.2f}x scoring). Host win% vs market:")
hh={'Mexico':'A','Canada':'B','United States':'D'}; mn={'United States':'USA'}
for t,gg in hh.items():
    mr=MK[gg]['prices']; s=sum(mr.values()); mm=mr.get(mn.get(t,t),0)/s*100
    print(f"  {t:<14} v7 win {pos[t][0]*100:4.1f}%   market {mm:4.1f}%   gap {pos[t][0]*100-mm:+5.1f}   advance {advance[t]*100:.0f}%")
print('wrote PREDICTIONS_v7.md')
