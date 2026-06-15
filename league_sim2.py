"""Self-audit rerun of Q6. Fixes vs league_sim.py:
 (1) tests the ACTUAL deployed rule (blend-EV within DIFF_BAND, min field%) — not a proxy.
 (2) standings calibrated to known data (user 2w1e=165 -> ~72/win, ~21/exact).
 (3) all strategies share the SAME score-selection (rare-tilt) -> isolates OUTCOME choice.
 (4) DIFF_BAND + truth-weight sensitivity."""
import json, numpy as np
from scipy.stats import nbinom
rng=np.random.default_rng(13)
AD=json.load(open('attdef.json')); W2C=json.load(open('wc_to_canon.json')); DP=json.load(open('deployed_params.json'))
CP=json.load(open('crowd_params.json')); PM=json.load(open('polymarket_matches.json'))
mug=AD['_meta']['mu_goals']; R=DP['R']; G=DP['GAMMA']; MAXG=8; BETA=CP['beta']; SS=CP['sal_strength']
SAL={(1,0):1.5,(2,0):1.5,(2,1):1.6,(3,0):1.0,(3,1):0.75,(4,0):0.45,(4,1):0.4,(3,2):0.5,(1,1):1.7,(0,0):0.55,(2,2):0.9,(3,3):0.3}
def sal(a,b): v=SAL.get((a,b),SAL.get((b,a),0.25 if (a+b)>=5 else 0.6)); return v**SS
def tier(c): return 20 if c>.30 else 30 if c>.20 else 50 if c>.05 else 70 if c>.005 else 100
def lam(th,ta,ov=(0,0,0,0)):
    lh=np.exp(mug+AD[W2C[th]]['ATT']-AD[W2C[ta]]['DEF']); la=np.exp(mug+AD[W2C[ta]]['ATT']-AD[W2C[th]]['DEF'])
    M=.5*(np.log(lh)+np.log(la));D=.5*(np.log(lh)-np.log(la))
    lh,la=np.exp(M+G*D),np.exp(M-G*D); lh*=np.exp(ov[0]-ov[3]); la*=np.exp(ov[2]-ov[1])
    return float(np.clip(lh,.08,6)),float(np.clip(la,.08,6))
def nbv(l): p=R/(R+l); v=nbinom.pmf(np.arange(MAXG+1),R,p); return v/v.sum()
def region(oi):
    if oi==0: return [(a,b) for a in range(MAXG+1) for b in range(MAXG+1) if a>b]
    if oi==1: return [(a,a) for a in range(MAXG+1)]
    return [(a,b) for a in range(MAXG+1) for b in range(MAXG+1) if a<b]

MATCHES=[
 ('Qatar','Switzerland',[172,141,33],[.06,.07,.87],(0,0,0,0),2),       # last = LOCKED outcome idx
 ('Brazil','Morocco',[55,122,140],[.53,.29,.18],(-.13,-.08,0,-.06),1),
 ('Haiti','Scotland',[154,131,44],[.04,.09,.87],(0,0,0,0),2),
 ('Germany','Curacao',[15,179,222],[.97,.02,.01],(0,0,0,0),0),
 ('Australia','Turkey',[126,115,66],[.09,.22,.69],(0,0,0,0),2),
 ('Netherlands','Japan',[74,115,113],[.61,.25,.13],(-.08,-.10,-.12,0),1),
 ('Ivory Coast','Ecuador',[108,101,85],[.44,.41,.14],(0,0,0,0),2),
 ('Sweden','Tunisia',[72,110,122],[.63,.27,.11],(0,0,0,0),1),
]
def rare_score(M,oi,crowd,tiers):  # deployed score logic: max Ebonus then VAR_TIEBREAK(<=1.5, p>=.5*best, min crowd, pess-guard)
    cells=region(oi)
    rows=[]
    for c in cells:
        ts=[tier(crowd[c]*f) for f in (.7,1,1.43)]; rows.append((c,M[c],float(M[c]*np.mean(ts)),ts))
    rows.sort(key=lambda r:-r[2])
    pess=lambda r: r[1]*r[3][2]
    near=[r for r in rows if rows[0][2]-r[2]<=1.5 and r[1]>=.5*rows[0][1] and pess(r)>=pess(rows[0])]
    if near:
        best=min(near,key=lambda r:crowd[r[0]])
        return best[0]
    return rows[0][0]

pre=[]
for h,a,rew,fp,ov,lk in MATCHES:
    fp=[x/sum(fp) for x in fp]
    lh,la=lam(h,a,ov); M=np.outer(nbv(lh),nbv(la)); M/=M.sum()
    v6=[float(np.tril(M,-1).sum()),float(np.trace(M)),float(np.triu(M,1).sum())]
    key=f'{h}|{a}'; mk=(lambda s:[s['h'],s['d'],s['a']])(PM[key][-1]) if key in PM else v6
    crowd={}; tiers={}
    for oi in range(3):
        cells=region(oi); pl=np.array([M[x,y] for x,y in cells]); cr=(pl**BETA)*np.array([sal(x,y) for x,y in cells]); cr/=cr.sum()
        for k,c in enumerate(cells): crowd[c]=cr[k]; tiers[c]=tier(cr[k])
    pre.append(dict(h=h,a=a,rew=rew,fp=fp,v6=v6,mk=mk,M=M,crowd=crowd,lk=lk))

def pick_outcome(pm,strat,band=2.0,tw=0.5):
    v6,mk,fp,rew=pm['v6'],pm['mk'],pm['fp'],pm['rew']
    blend=[(1-tw)*v6[i]+tw*mk[i] for i in range(3)]
    if strat=='LOCKED': return pm['lk']
    if strat=='EVMAX': return int(np.argmax([v6[i]*rew[i] for i in range(3)]))
    if strat=='MARKET': return int(np.argmax([mk[i]*rew[i] for i in range(3)]))
    if strat=='DIFF': return int(np.argmin([fp[i] if v6[i]>=0.15 else 9 for i in range(3)]))
    if strat=='LEAGUE':
        bev=[blend[i]*rew[i] for i in range(3)]; emax=max(bev)
        cand=[i for i in range(3) if bev[i]>=emax-band]; return min(cand,key=lambda i:fp[i])

# REAL standings (user-supplied 2026-06-13). USER=#8.
base=np.array([376,280,240,239,239,219,190,165,143,123,123,96,49],float); USER=7
N=15000
def simulate(TRUTH_TW,K):
    """K = horizon multiplier: replay the 8-match slate K times (~8K matches of a similar season)."""
    UP=np.zeros((N,)); RIVtot=np.tile(base[None,:],(N,1)).astype(float); RIVtot[:,USER]=base[USER]
    user_picks={}  # cache per strategy filled by run()
    # accumulate rivals + store results for scoring user strategies
    RES_OI=np.empty((N,len(pre),K),int); RES_SC=np.empty((N,len(pre),K),object)
    for rep in range(K):
        for mi,pm in enumerate(pre):
            truth=[(1-TRUTH_TW)*pm['v6'][i]+TRUTH_TW*pm['mk'][i] for i in range(3)]; truth=[t/sum(truth) for t in truth]
            roi=rng.choice(3,size=N,p=truth); RES_OI[:,mi,rep]=roi
            for oi in range(3):
                idx=np.where(roi==oi)[0]
                if not len(idx): continue
                cells=region(oi); pv=np.array([pm['M'][c] for c in cells]); pv/=pv.sum()
                ch=rng.choice(len(cells),size=len(idx),p=pv)
                for kk,ii in zip(ch,idx): RES_SC[ii,mi,rep]=cells[kk]
            for j in range(13):
                if j==USER: continue
                rj=rng.choice(3,size=N,p=pm['fp'])
                for oi in range(3):
                    nidx=np.where(rj==oi)[0]
                    if not len(nidx): continue
                    cells=region(oi); cw=np.array([pm['crowd'][c] for c in cells]); cw/=cw.sum()
                    ch=rng.choice(len(cells),size=len(nidx),p=cw)
                    bp=(oi==roi[nidx])*pm['rew'][oi]
                    bn=np.array([tier(pm['crowd'][cells[c]]) if cells[c]==RES_SC[ii,mi,rep] else 0 for c,ii in zip(ch,nidx)])
                    RIVtot[nidx,j]+=bp+bn
    def run(strat,band=2.0):
        up=np.zeros(N)
        for mi,pm in enumerate(pre):
            oi=pick_outcome(pm,strat,band); sc=rare_score(pm['M'],oi,pm['crowd'],{})
            for rep in range(K):
                bp=(RES_OI[:,mi,rep]==oi)*pm['rew'][oi]
                bn=np.array([tier(pm['crowd'][sc]) if RES_SC[n,mi,rep]==sc else 0 for n in range(N)])
                up+=bp+bn
        tot=RIVtot.copy(); tot[:,USER]=base[USER]+up
        above=(tot> tot[:,USER:USER+1]).sum(1)  # rivals strictly above user
        return np.mean(above<=1), np.mean(above==0)  # P(top2), P(top1)
    return run

print(f"REAL standings: user #8=165; leader 376 (def 211), #2=280 (def 115), #7=190 (def 25). N={N}")
print("Objective = TOP 2. P(top2) [P(top1)] by strategy x horizon (K*8 matches), truth_tw=0.5:")
print(f"{'strategy':<12}{'K=1 (8m)':>16}{'K=12 (~100m)':>18}")
for K in (1,12): pass
r1=simulate(0.5,1); r12=simulate(0.5,12)
for s in ['LOCKED','MARKET','EVMAX','DIFF']:
    a=r1(s); b=r12(s); print(f"{s:<12}{a[0]*100:>9.1f}% [{a[1]*100:>3.0f}]{b[0]*100:>11.1f}% [{b[1]*100:>3.0f}]")
for bd in [0.0,1.0,2.0,3.0]:
    a=r1('LEAGUE',bd); b=r12('LEAGUE',bd); print(f"{'LEAGUE b'+str(bd):<12}{a[0]*100:>9.1f}% [{a[1]*100:>3.0f}]{b[0]*100:>11.1f}% [{b[1]*100:>3.0f}]")
