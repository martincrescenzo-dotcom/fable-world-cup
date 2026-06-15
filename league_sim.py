"""Q6 — friends-league (13p) rank-EV sim. Objective: WIN the league.
Uses REAL field outcome-pick % (rivals modeled from it) + validated crowd model (score shares)
+ reward tables, over the 8 unresolved MD1 matches. Compares user strategies:
 LOCKED (submitted) | EVMAX | MARKET-follow | DIFF (max differentiation).
Truth: outcome ~ 0.5*v6 + 0.5*market; score ~ v6 NB | outcome. Crude but grounded."""
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

# 8 unresolved MD1 matches: home,away,rewards[h,d,a],fieldpct[h,d,a],locked(outcome_idx,score),overlay
MATCHES=[
 ('Qatar','Switzerland',[172,141,33],[.06,.07,.87],(2,(0,3)),(0,0,0,0)),
 ('Brazil','Morocco',[55,122,140],[.53,.29,.18],(1,(0,0)),(-.13,-.08,0,-.06)),
 ('Haiti','Scotland',[154,131,44],[.04,.09,.87],(2,(1,3)),(0,0,0,0)),
 ('Germany','Curacao',[15,179,222],[.97,.02,.01],(0,(5,0)),(0,0,0,0)),
 ('Australia','Turkey',[126,115,66],[.09,.22,.69],(2,(1,3)),(0,0,0,0)),
 ('Netherlands','Japan',[74,115,113],[.61,.25,.13],(1,(0,0)),(-.08,-.10,-.12,0)),
 ('Ivory Coast','Ecuador',[108,101,85],[.44,.41,.14],(2,(0,2)),(0,0,0,0)),
 ('Sweden','Tunisia',[72,110,122],[.63,.27,.11],(1,(0,0)),(0,0,0,0)),
]
def region(oi):
    if oi==0: return [(a,b) for a in range(MAXG+1) for b in range(MAXG+1) if a>b]
    if oi==1: return [(a,a) for a in range(MAXG+1)]
    return [(a,b) for a in range(MAXG+1) for b in range(MAXG+1) if a<b]

# precompute per match: truth outcome probs, score matrix, crowd shares+tiers per region, strategy picks
pre=[]
for h,a,rew,fp,lk,ov in MATCHES:
    fp=[x/sum(fp) for x in fp]
    lh,la=lam(h,a,ov); M=np.outer(nbv(lh),nbv(la)); M/=M.sum()
    v6=[float(np.tril(M,-1).sum()),float(np.trace(M)),float(np.triu(M,1).sum())]
    key=f'{h}|{a}'
    if key in PM: s=PM[key][-1]; mk=[s['h'],s['d'],s['a']]
    else: mk=v6
    truth=[0.5*v6[i]+0.5*mk[i] for i in range(3)]; truth=[t/sum(truth) for t in truth]
    # crowd shares + tier per cell per region
    crowd={}; tiers={}
    for oi in range(3):
        cells=region(oi); pl=np.array([M[x,y] for x,y in cells])
        cr=(pl**BETA)*np.array([sal(x,y) for x,y in cells]); cr/=cr.sum()
        for k,(x,y) in enumerate(cells): crowd[(x,y)]=cr[k]; tiers[(x,y)]=tier(cr[k])
    # strategy outcome picks
    ev_v6=[v6[i]*rew[i] for i in range(3)]; ev_mk=[mk[i]*rew[i] for i in range(3)]
    s_evmax=int(np.argmax(ev_v6)); s_mkt=int(np.argmax(ev_mk))
    s_diff=int(np.argmin([fp[i] if v6[i]>=0.15 else 9 for i in range(3)]))  # rarest field pick w/ p>=15%
    def modal_score(oi):
        cells=region(oi); return max(cells,key=lambda c:M[c])
    def best_bonus_score(oi):  # lowest-crowd among top-ebonus (our deployed logic, simplified)
        cells=region(oi); rows=sorted(cells,key=lambda c:-(M[c]*np.mean([tier(crowd[c]*f) for f in (.7,1,1.43)])))
        near=[c for c in rows if M[c]>=0.5*M[rows[0]]]; return min(near,key=lambda c:crowd[c])
    strat_pick={'LOCKED':lk,'EVMAX':(s_evmax,best_bonus_score(s_evmax)),
                'MARKET':(s_mkt,modal_score(s_mkt)),'DIFF':(s_diff,best_bonus_score(s_diff))}
    pre.append(dict(h=h,a=a,rew=rew,fp=fp,truth=truth,M=M,crowd=crowd,tiers=tiers,strat=strat_pick))

# current standings (estimate): points ~ 84*winners + 40*exacts; user(=#8) overridden to 165 actual
counts=[(4,2),(3,2),(3,0),(3,1),(3,1),(3,0),(2,1),(2,1),(2,1),(2,0),(2,0),(1,0),(1,0)]
base=np.array([84*w+40*e for w,e in counts],float); USER=7; base[USER]=165.0
N=40000
def score_pick(pre_m,oi,score,res_oi,res_score):
    pts=0.0
    if oi==res_oi: pts+=pre_m['rew'][oi]
    if score==res_score: pts+=pre_m['tiers'][score]   # exact (implies outcome right)
    return pts

# vectorised: simulate results once, share across strategies for paired comparison
RES_OI=np.empty((N,len(pre)),int); RES_SC=np.empty((N,len(pre)),object)
RIV=np.zeros((N,13))  # rival cumulative (12 rivals at indices !=USER; USER col filled per-strategy)
for mi,pm in enumerate(pre):
    res_oi=rng.choice(3,size=N,p=pm['truth'])
    RES_OI[:,mi]=res_oi
    # result scores
    for oi in range(3):
        idx=np.where(res_oi==oi)[0]
        if len(idx)==0: continue
        cells=region(oi); pv=np.array([pm['M'][c] for c in cells]); pv/=pv.sum()
        ch=rng.choice(len(cells),size=len(idx),p=pv)
        for kk,ii in zip(ch,idx): RES_SC[ii,mi]=cells[kk]
    # rivals: each of 12 rivals picks outcome~fp, score~crowd
    for j in range(13):
        if j==USER: continue
        roi=rng.choice(3,size=N,p=pm['fp'])
        add=np.zeros(N)
        for oi in range(3):
            m=roi==oi; nidx=np.where(m)[0]
            if len(nidx)==0: continue
            cells=region(oi); cw=np.array([pm['crowd'][c] for c in cells]); cw/=cw.sum()
            ch=rng.choice(len(cells),size=len(nidx),p=cw)
            base_pts=(oi==res_oi[nidx])*pm['rew'][oi]
            exact=np.array([cells[c]==RES_SC[ii,mi] for c,ii in zip(ch,nidx)])
            bonus=np.array([pm['tiers'][cells[c]] for c in ch])*exact
            add[nidx]=base_pts+bonus
        RIV[:,j]+=add
results={}
for strat in ['LOCKED','EVMAX','MARKET','DIFF']:
    upts=np.zeros(N)
    for mi,pm in enumerate(pre):
        oi,sc=pm['strat'][strat]
        base_pts=(RES_OI[:,mi]==oi)*pm['rew'][oi]
        exact=np.array([sc==RES_SC[n,mi] for n in range(N)])
        upts+=base_pts+exact*pm['tiers'][sc]
    tot=RIV+base[None,:]; tot[:,USER]=base[USER]+upts
    win=np.mean(tot[:,USER]>=tot.max(1)-1e-9)
    bl=np.mean(tot[:,USER]>tot[:,0])
    results[strat]=(win,upts.mean(),bl)

print(f"current: user #8/13 at 165pts; leader 416(est).  Sim over 8 MD1 matches, N={N}")
print(f"{'strategy':<10}{'E[user +pts]':>14}{'P(win league)':>16}{'P(pass leader)':>16}")
for s in ['LOCKED','EVMAX','MARKET','DIFF']:
    w,mp,bl=results[s]; print(f"{s:<10}{mp:>14.1f}{w*100:>15.1f}%{bl*100:>15.1f}%")
print("\nper-match LOCKED vs MARKET outcome pick (field% on our pick shows differentiation):")
for pm in pre:
    lo=pm['strat']['LOCKED'][0]; mo=pm['strat']['MARKET'][0]; do=pm['strat']['DIFF'][0]
    nm=['H','D','A']
    print(f"  {pm['h'][:11]+'-'+pm['a'][:9]:<22} LOCKED={nm[lo]}(field {pm['fp'][lo]*100:.0f}%) MARKET={nm[mo]} DIFF={nm[do]}(field {pm['fp'][do]*100:.0f}%)")
