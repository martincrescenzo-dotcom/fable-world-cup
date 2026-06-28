import json, numpy as np
from scipy.stats import nbinom, poisson
AD=json.load(open('attdef.json')); W2C=json.load(open('wc_to_canon.json')); Q=json.load(open('qualification_v5.json'))
mug=AD['_meta']['mu_goals']; R=Q['r']; MAXG=14; GAMMA=1.5; PHI=0.635
# --- conservative model-blind overlays (halved where market already moved) ---
def adj(team,datt=0.0,ddef=0.0):
    c=W2C[team]; AD[c]['ATT']+=datt; AD[c]['DEF']+=ddef
adj('Germany',ddef=-0.05)   # Schlotterbeck out + flagged frailty, MED, halved (market saw Ecuador loss)
adj('Japan',datt=-0.05)     # Kubo likely out, LOW, halved (conflicting reports)
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

games=[
 ('South Africa','Canada',[141,121,64],[0.173,0.272,0.555],[0.10,0.15,0.75]),
 ('Brazil','Japan',        [65,121,141],[0.556,0.254,0.190],[0.77,0.12,0.11]),
 ('Germany','Paraguay',    [45,140,169],[0.70,0.19,0.11],   [0.95,0.04,0.01]),
]
for th,ta,rew,mkt,field in games:
    rew=np.array(rew,float); mkt=np.array(mkt,float); field=np.array(field,float)
    Mx,lh,la=joint90(th,ta); m120=transform120(Mx,lh,la)
    v90=wdl(Mx); v120=wdl(m120)
    # outcome-level transform mapping derived from the MODEL, applied to market:
    rho_m=v120[1]/v90[1]; broken=v90[1]-v120[1]
    s_home=(v120[0]-v90[0])/broken if broken>1e-9 else 0.5   # share of broken draw -> home
    mkt120=np.array([mkt[0]+broken_mkt_h, 0,0]) if False else None
    bm=mkt[1]*(1-rho_m)  # market broken draw mass
    mkt120=np.array([mkt[0]+bm*s_home, mkt[1]*rho_m, mkt[2]+bm*(1-s_home)])
    blend90=0.4*v90+0.6*mkt; blend120=0.4*v120+0.6*mkt120
    impl=(1/rew)/np.sum(1/rew)
    ev=blend120*rew; edge=blend120/impl
    pick=int(np.argmax(ev)); lab=[th,'Draw',ta]
    sc,scp=modal_in(m120,pick)
    print(f"\n=== {th} v {ta} ===  rewards {rew.astype(int)}  field% {(field*100).astype(int)}")
    print(f"  v6  90': {np.round(v90*100,1)}   ->120': {np.round(v120*100,1)}   (model rho_match={rho_m:.3f}, broken->home share {s_home:.2f})")
    print(f"  mkt 90': {np.round(mkt*100,1)}   ->120': {np.round(mkt120*100,1)}")
    print(f"  BLEND120 (0.4/0.6): {np.round(blend120*100,1)}   reward-implied {np.round(impl*100,1)}")
    print(f"  EV: {np.round(ev,1)}   edge(blend/impl): {np.round(edge,2)}")
    print(f"  -> OUTCOME PICK: {lab[pick]}  (EV {ev[pick]:.1f}, edge {edge[pick]:.2f}, field {field[pick]*100:.0f}%)")
    print(f"  -> MODAL 120' SCORE in {lab[pick]}: {sc}  (p={scp*100:.1f}%)   | P(120 draw)={v120[1]*100:.1f}% vs field draw {field[1]*100:.0f}%")

print("\n\n===== MODAL 120' SCORE DETAIL (top cells) for the DISCIPLINED picks =====")
def topcells(M,out,n=4):
    cells=[]
    for i in range(M.shape[0]):
        for j in range(M.shape[0]):
            reg=0 if i>j else (1 if i==j else 2)
            if reg==out: cells.append((M[i,j],f'{i}-{j}'))
    cells.sort(reverse=True); return cells[:n]
forced=[('South Africa','Canada',2),('Brazil','Japan',0),('Germany','Paraguay',0)]
for th,ta,pk in forced:
    Mx,lh,la=joint90(th,ta); m120=transform120(Mx,lh,la)
    lab=[th,'Draw',ta]
    print(f"  {th} v {ta} -> pick {lab[pk]}: top scores {[(s,round(p*100,1)) for p,s in topcells(m120,pk)]}")
