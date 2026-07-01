import json, numpy as np
from scipy.stats import nbinom, poisson
AD=json.load(open('attdef.json')); W2C=json.load(open('wc_to_canon.json')); DP=json.load(open('deployed_params.json'))
# R/GAMMA from deployed_params.json = single source of truth (2026-07-01 audit: was qualification_v5.json,
# a regenerable output). MAXG=14 (vs group 12) is DELIBERATE: ET goals extend the 120' grid.
mug=AD['_meta']['mu_goals']; R=DP['R']; MAXG=14; GAMMA=DP['GAMMA']; PHI=0.635
# --- conservative model-blind overlays (halved where market already moved) ---
def adj(team,datt=0.0,ddef=0.0):
    c=W2C[team]; AD[c]['ATT']+=datt; AD[c]['DEF']+=ddef
# 2026-07-02 slate: NO overlays — nothing confirmed+unpriced (Salah doubt & Morocco/Paraguay 120'-fatigue
# are in the post-news lines; Amoura/Partey/Spain-wingers unconfirmed at run time). Stakes protocol (b).
def AT(t): return AD[W2C[t]]['ATT']
def DF(t): return AD[W2C[t]]['DEF']
def lam_pair(th,ta):
    lh=np.exp(mug+AT(th)-DF(ta)); la=np.exp(mug+AT(ta)-DF(th))
    M=0.5*(np.log(lh)+np.log(la)); D=0.5*(np.log(lh)-np.log(la))
    return float(np.exp(M+GAMMA*D)), float(np.exp(M-GAMMA*D))
def nbvec(lam):
    p=R/(R+lam); v=nbinom.pmf(np.arange(MAXG+1),R,p); return v/v.sum()
def joint90(th,ta):
    lh,la=lam_pair(th,ta); Mx=np.outer(nbvec(lh),nbvec(la)); return Mx/Mx.sum(),lh,la
def transform120(Mx,lh,la,phi=PHI):
    n=Mx.shape[0]; le,lr=lh/3*phi, la/3*phi
    eh=poisson.pmf(np.arange(n),le); ea=poisson.pmf(np.arange(n),lr); eh/=eh.sum(); ea/=ea.sum()
    ET=np.outer(eh,ea); out=np.array(Mx)
    for k in range(n):
        m=Mx[k,k]
        if m<=0: continue
        out[k,k]-=m
        for dh in range(n-k):
            for da in range(n-k):
                out[k+dh,k+da]+=m*ET[dh,da]
    return out/out.sum()
def wdl(M): return np.array([float(np.tril(M,-1).sum()), float(np.trace(M)), float(np.triu(M,1).sum())])
def modal_in(M,out):  # out: 0 home(i>j),1 draw,2 away(i<j)
    n=M.shape[0]; best=(-1,None)
    for i in range(n):
        for j in range(n):
            reg = 0 if i>j else (1 if i==j else 2)
            if reg==out and M[i,j]>best[0]: best=(M[i,j],(i,j))
    return f'{best[1][0]}-{best[1][1]}', best[0]

games=[   # 2026-07-02 slate: 7 R32 + 2 R16. market = de-vigged 90' 1X2 (Kalshi regulation-time / PM moneyline /
          # sharp-book mid, all pulled 2026-07-02; NOT to-advance). field = Repartition from user.
 ('United States','Bosnia and Herzegovina',[52,132,157],[0.675,0.209,0.116],[0.85,0.09,0.06]),
 ('Spain','Austria',        [41,140,182], [0.730,0.175,0.095],[0.95,0.04,0.01]),
 ('Portugal','Croatia',     [73,114,133], [0.537,0.271,0.192],[0.55,0.28,0.17]),
 ('Switzerland','Algeria',  [61,122,148], [0.483,0.294,0.224],[0.65,0.19,0.16]),
 ('Australia','Egypt',      [113,106,92], [0.290,0.330,0.380],[0.14,0.27,0.59]),
 ('Argentina','Cape Verde', [25,165,213], [0.830,0.120,0.050],[0.89,0.06,0.04]),
 ('Colombia','Ghana',       [66,114,139], [0.642,0.234,0.124],[0.76,0.15,0.08]),
 ('Canada','Morocco',       [137,118,68], [0.190,0.280,0.530],[0.09,0.14,0.78]),   # R16
 ('Paraguay','France',      [202,161,28], [0.050,0.130,0.820],[0.00,0.00,0.00]),   # R16; field not yet populated
]
picked=[]
for th,ta,rew,mkt,field in games:
    rew=np.array(rew,float); mkt=np.array(mkt,float); field=np.array(field,float)
    Mx,lh,la=joint90(th,ta); m120=transform120(Mx,lh,la)
    v90=wdl(Mx); v120=wdl(m120)
    # outcome-level transform mapping derived from the MODEL, applied to market:
    rho_m=v120[1]/v90[1]; broken=v90[1]-v120[1]
    s_home=(v120[0]-v90[0])/broken if broken>1e-9 else 0.5   # share of broken draw -> home
    bm=mkt[1]*(1-rho_m)  # market broken draw mass
    mkt120=np.array([mkt[0]+bm*s_home, mkt[1]*rho_m, mkt[2]+bm*(1-s_home)])
    blend90=0.4*v90+0.6*mkt; blend120=0.4*v120+0.6*mkt120
    impl=(1/rew)/np.sum(1/rew)
    ev=blend120*rew
    # edge = MARKET_p / reward-implied_p (doctrine metric, CLAUDE.md 2026-06-20). AUDIT FIX 2026-07-01:
    # was blend/impl — the blend leg let the MODEL's contrarian lean inflate the edge past 1 exactly on
    # reward-asymmetric model-vs-market divergences (Germany-Paraguay: blend-edge 1.11 vs market-edge 0.80
    # = auto-reject; the Paraguay draft lost). Market-based edge is the gate with teeth.
    edge=mkt120/impl; edge_blend=blend120/impl
    pick=int(np.argmax(ev)); lab=[th,'Draw',ta]
    sc,scp=modal_in(m120,pick)
    print(f"\n=== {th} v {ta} ===  rewards {rew.astype(int)}  field% {(field*100).astype(int)}")
    print(f"  v6  90': {np.round(v90*100,1)}   ->120': {np.round(v120*100,1)}   (model rho_match={rho_m:.3f}, broken->home share {s_home:.2f})")
    print(f"  mkt 90': {np.round(mkt*100,1)}   ->120': {np.round(mkt120*100,1)}")
    print(f"  BLEND120 (0.4/0.6): {np.round(blend120*100,1)}   reward-implied {np.round(impl*100,1)}")
    print(f"  EV: {np.round(ev,1)}   edge(mkt/impl): {np.round(edge,2)}   [blend/impl: {np.round(edge_blend,2)}]")
    rej='  !! edge<1 = AUTO-REJECT (market says the reward line over-prices this pick) — do NOT submit without a red-team override' if edge[pick]<1 else ''
    print(f"  -> OUTCOME PICK: {lab[pick]}  (EV {ev[pick]:.1f}, edge {edge[pick]:.2f}, field {field[pick]*100:.0f}%){rej}")
    print(f"  -> MODAL 120' SCORE in {lab[pick]}: {sc}  (p={scp*100:.1f}%)   | P(120 draw)={v120[1]*100:.1f}% vs field draw {field[1]*100:.0f}%")
    picked.append((th,ta,pick))

print("\n\n===== MODAL 120' SCORE DETAIL (top cells) for the picks =====")
def topcells(M,out,n=4):
    cells=[]
    for i in range(M.shape[0]):
        for j in range(M.shape[0]):
            reg=0 if i>j else (1 if i==j else 2)
            if reg==out: cells.append((M[i,j],f'{i}-{j}'))
    cells.sort(reverse=True); return cells[:n]
for th,ta,pk in picked:
    Mx,lh,la=joint90(th,ta); m120=transform120(Mx,lh,la)
    lab=[th,'Draw',ta]
    print(f"  {th} v {ta} -> pick {lab[pk]}: top scores {[(s,round(p*100,1)) for p,s in topcells(m120,pk)]}")
