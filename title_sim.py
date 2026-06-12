"""20/80 title estimate: reuse v5 att/def + NB engine.
Random-draw single-elim over the modal 32-team field (marginalises over the unknown
exact bracket), then fold in each team's group-survival prob. Cross-check vs market."""
import json, numpy as np
from scipy.stats import nbinom
rng=np.random.default_rng(7)
AD=json.load(open('attdef.json')); WC=json.load(open('wc_data.json'))
W2C=json.load(open('wc_to_canon.json')); Q=json.load(open('qualification_v5.json'))
MKT=json.load(open('market_winner.json'))
mug=AD['_meta']['mu_goals']; R=Q['r']; MAXG=12
teams=[t['team'] for g in WC for t in WC[g]]
def AT(t): return AD[W2C[t]]['ATT']
def DF(t): return AD[W2C[t]]['DEF']
S={t:AT(t)+DF(t) for t in teams}

def nbvec(lam):
    p=R/(R+lam); v=nbinom.pmf(np.arange(MAXG+1),R,p); return v/v.sum()
def wdl(ti,tj):  # neutral
    lh=np.clip(np.exp(mug+AT(ti)-DF(tj)),0.1,6); la=np.clip(np.exp(mug+AT(tj)-DF(ti)),0.1,6)
    M=np.outer(nbvec(lh),nbvec(la))
    return np.tril(M,-1).sum(),np.trace(M),np.triu(M,1).sum()
def padv(ti,tj):  # P(i advances past j in a knockout)
    w,d,l=wdl(ti,tj); pen=float(np.clip(0.5+0.08*(S[ti]-S[tj]),0.3,0.7))
    return w+d*pen

# ---- modal 32-team field: top-2 per group + 8 best thirds ----
field=[]; thirds=[]
for g in WC:
    gt=[t['team'] for t in WC[g]]
    rank=sorted(gt,key=lambda t:-(Q['pos'][t][0]+Q['pos'][t][1]))
    field+=rank[:2]; thirds.append(rank[2])  # 3rd-best as candidate third
thirds=sorted(thirds,key=lambda t:-Q['advance'][t])[:8]
field+=thirds
assert len(field)==32, len(field)
fi={t:i for i,t in enumerate(field)}
Wf=np.array([[padv(a,b) if a!=b else 0.5 for b in field] for a in field])

# ---- vectorised random-bracket single elimination ----
N=300000
alive=np.argsort(rng.random((N,32)),axis=1)   # random order -> random bracket per sim
while alive.shape[1]>1:
    a=alive[:,0::2]; b=alive[:,1::2]
    pw=Wf[a,b]
    alive=np.where(rng.random(a.shape)<pw,a,b)
champ=alive[:,0]
ko=np.bincount(champ,minlength=32)/N   # P(win knockout | in field)

# fold in group survival: title ~ advance * ko, renormalised over field
raw={t:Q['advance'][t]*ko[fi[t]] for t in field}
Z=sum(raw.values()); title={t:raw[t]/Z for t in field}

print(f"{'team':<14}{'model title':>12}{'market':>9}{'edge':>8}")
mk={k:v for k,v in MKT.items()}
def mname(t): return {'United States':'USA','Turkey':'Türkiye','DR Congo':'Congo DR'}.get(t,t)
for t in sorted(field,key=lambda x:-title[x])[:16]:
    m=mk.get(mname(t),0.0)
    print(f"{t:<14}{title[t]*100:>11.1f}%{m*100:>8.1f}%{(title[t]-m)*100:>+7.1f}")
print(f"\n(model normalised over the 32-team field; market sum={sum(MKT.values()):.2f})")
