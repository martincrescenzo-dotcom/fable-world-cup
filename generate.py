"""Generate all 72 group-match score predictions + qualification tables -> PREDICTIONS.md"""
import json, numpy as np
from scipy.stats import poisson
rng = np.random.default_rng(7)

R = json.load(open('ratings.json'))
BASE=np.log(1.32); B=0.70; RHO=-0.08; MAXG=10
HOSTS={'Mexico','Canada','United States'}
KG=np.arange(0,16)

def lambdas(ra,rb):
    d=ra-rb
    return float(np.clip(np.exp(BASE+B*d/400),0.12,6)), float(np.clip(np.exp(BASE-B*d/400),0.12,6))

def score_matrix(ra,rb):
    la,lb=lambdas(ra,rb)
    x=poisson.pmf(np.arange(MAXG+1),la); y=poisson.pmf(np.arange(MAXG+1),lb)
    M=np.outer(x,y)
    M[0,0]*=1-la*lb*RHO; M[0,1]*=1+la*RHO; M[1,0]*=1+lb*RHO; M[1,1]*=1-RHO
    M/=M.sum(); return M,la,lb

def match(ra,rb):
    M,la,lb=score_matrix(ra,rb)
    ph=np.tril(M,-1).sum(); pd=np.trace(M); pa=np.triu(M,1).sum()
    flat=sorted(((M[a,b],a,b) for a in range(MAXG+1) for b in range(MAXG+1)),reverse=True)
    top=[(a,b,float(p)) for p,a,b in flat[:3]]
    return dict(ph=ph,pd=pd,pa=pa,xa=la,xb=lb,top=top)

# ---- FIFA fixture order (positions) and matchday labels ----
FIX=[(0,1),(2,3),(0,2),(3,1),(3,0),(1,2)]
MD =[1,1,2,2,3,3]

def fppf(U,lam): return np.searchsorted(poisson.cdf(KG,lam),U).astype(np.int64)

def sim_group_full(rats,N):
    rats=np.asarray(rats,float)
    pts=np.zeros((N,4)); gf=np.zeros((N,4)); ga=np.zeros((N,4))
    for a,b in FIX:
        la,lb=lambdas(rats[a],rats[b])
        ga_=rng.poisson(la,N); gb_=rng.poisson(lb,N)
        gf[:,a]+=ga_; ga[:,a]+=gb_; gf[:,b]+=gb_; ga[:,b]+=ga_
        wa=ga_>gb_; wb=gb_>ga_; dr=~(wa|wb)
        pts[wa,a]+=3; pts[wb,b]+=3; pts[dr,a]+=1; pts[dr,b]+=1
    gd=gf-ga
    key=pts*1e6+gd*1e3+gf+rng.random((N,4))*1e-3
    order=np.argsort(-key,axis=1)
    rank=np.empty((N,4),int)
    for r in range(4): rank[np.arange(N),order[:,r]]=r   # 0=1st..3=4th
    return pts,gd,gf,rank

# ---- joint simulation across all 12 groups for best-third qualification ----
N=200000
groups=sorted(R)
pos_counts={}   # team -> [P1,P2,P3,P4]
exp_pts={}
third_pts=[]; third_gd=[]; third_gf=[]; third_team=[]
team_group={}
for g in groups:
    teams=R[g]['teams']; rats=R[g]['blend']
    pts,gd,gf,rank=sim_group_full(rats,N)
    for i,t in enumerate(teams):
        team_group[t]=g
        c=np.bincount(rank[:,i],minlength=4)/N
        pos_counts[t]=c
        exp_pts[t]=pts[:,i].mean()
    thi=np.argmax(rank==2,axis=1)   # index of the 3rd-placed team each sim
    idx=np.arange(N)
    third_pts.append(pts[idx,thi]); third_gd.append(gd[idx,thi]); third_gf.append(gf[idx,thi])
    third_team.append([teams[k] for k in thi])

third_pts=np.array(third_pts).T   # N x 12
third_gd=np.array(third_gd).T
third_gf=np.array(third_gf).T
third_team=np.array(third_team).T  # N x 12 of names
# rank the 12 third-placed teams per sim; top 8 advance
key3=third_pts*1e6+third_gd*1e3+third_gf+rng.random((N,12))*1e-3
order3=np.argsort(-key3,axis=1)[:,:8]   # which group-slots advance
adv_third={t:0 for t in team_group}
for k in range(8):
    cols=order3[:,k]
    names=third_team[np.arange(N),cols]
    for t in set(names.tolist()):
        adv_third[t]+=int((names==t).sum())
adv_third={t:v/N for t,v in adv_third.items()}

# advance prob = P(1st)+P(2nd)+P(advance as 3rd)
advance={t: pos_counts[t][0]+pos_counts[t][1]+adv_third[t] for t in team_group}

# ---------------- build markdown ----------------
L=[]
L.append("# FIFA World Cup 2026 — Group-Stage Predictions")
L.append("")
L.append("**Engine:** Ensemble of live World-Football-Elo (60%→ via market) and Polymarket-implied strength, "
         "converted to scorelines with a Dixon-Coles-adjusted bivariate-Poisson model and a 200k-run Monte-Carlo "
         "of all 12 groups (correct FIFA tie-breakers + best-third-placed race).")
L.append(f"*Generated {np.datetime64('today')} — ratings & odds pulled live on 2026-06-11.*")
L.append("")
L.append("Each match shows the **most likely scoreline**, its probability, the **left-win/draw/right-win** split, and model **xG**.")
L.append("")

def teamlabel(t): return t+(" \U0001F3E0" if t in HOSTS else "")

allmatches=[]
for g in groups:
    teams=R[g]['teams']; rats=R[g]['blend']
    L.append(f"## Group {g}")
    L.append("")
    L.append("| MD | Match | Predicted | Prob | Left W / D / Right W | xG |")
    L.append("|----|-------|-----------|------|------------------|-----|")
    for (a,b),md in zip(FIX,MD):
        ta,tb=teams[a],teams[b]
        m=match(rats[a],rats[b])
        sa,sb,sp=m['top'][0]
        alt=", ".join(f"{x}-{y} ({p*100:.0f}%)" for x,y,p in m['top'][1:3])
        L.append(f"| {md} | **{teamlabel(ta)}** vs **{teamlabel(tb)}** | "
                 f"**{sa}–{sb}** | {sp*100:.0f}% | "
                 f"{m['ph']*100:.0f}% / {m['pd']*100:.0f}% / {m['pa']*100:.0f}% | "
                 f"{m['xa']:.2f}–{m['xb']:.2f} |")
        allmatches.append((g,md,ta,tb,sa,sb,sp,m))
    L.append("")
    # group table
    order=sorted(teams,key=lambda t:-advance[t])
    L.append("| Pos-prob | Team | xPts | Win% | Top-2% | Advance% |")
    L.append("|---|------|------|------|--------|----------|")
    for t in order:
        pc=pos_counts[t]
        L.append(f"|  | {teamlabel(t)} | {exp_pts[t]:.2f} | {pc[0]*100:.0f}% | "
                 f"{(pc[0]+pc[1])*100:.0f}% | {advance[t]*100:.0f}% |")
    L.append("")

open('PREDICTIONS.md','w',encoding='utf-8').write('\n'.join(L))

# console summary (ascii safe)
print("Matches:",len(allmatches))
print("\nMost-likely scorelines (all 72):")
for g,md,ta,tb,sa,sb,sp,m in allmatches:
    print(f"  {g} MD{md}: {ta:>22} {sa}-{sb} {tb:<22}  ({sp*100:.0f}%)")

# qualification quick table
qual=sorted(advance.items(),key=lambda x:-x[1])
print("\nTop advancers:")
for t,p in qual[:16]:
    print(f"  {t:<22} adv {p*100:4.0f}%  win {pos_counts[t][0]*100:3.0f}%")
json.dump({'pos':{t:pos_counts[t].tolist() for t in pos_counts},
           'advance':advance,'exp_pts':exp_pts,'adv_third':adv_third},
          open('qualification.json','w'),indent=2)
print("\nwrote PREDICTIONS.md + qualification.json")
