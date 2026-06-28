import json, numpy as np
from scipy.stats import nbinom, poisson
AD=json.load(open('attdef.json')); W2C=json.load(open('wc_to_canon.json')); Q=json.load(open('qualification_v5.json'))
mug=AD['_meta']['mu_goals']; R=Q['r']; MAXG=14; GAMMA=1.5
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
def transform120(Mx,lh,la,phi):
    n=Mx.shape[0]; le,lr=lh/3*phi, la/3*phi
    eh=poisson.pmf(np.arange(n),le); ea=poisson.pmf(np.arange(n),lr); eh/=eh.sum(); ea/=ea.sum()
    ET=np.outer(eh,ea); out=np.array(Mx)
    for k in range(n):
        m=Mx[k,k];
        if m<=0: continue
        out[k,k]-=m
        for dh in range(n-k):
            for da in range(n-k):
                out[k+dh,k+da]+=m*ET[dh,da]
    return out/out.sum()
def wdl(M): return float(np.tril(M,-1).sum()), float(np.trace(M)), float(np.triu(M,1).sum())
def modal(M):
    i,j=np.unravel_index(np.argmax(M),M.shape); return f'{i}-{j}',M[i,j]

# --- ET goal-count distribution from the 132-match dataset (total ET goals per match) ---
cnt={0:82,1:37,2:10,3:2,4:1}; Ndata=sum(cnt.values()); meanET=sum(g*c for g,c in cnt.items())/Ndata
print(f'Mean ET goals/match (data) = {meanET:.3f}  over n={Ndata}')
print('  total-ET-goals dist  data vs Poisson(mean):')
for g in range(5):
    print(f'   {g}: data {cnt.get(g,0)/Ndata:.3f}   Poisson {poisson.pmf(g,meanET):.3f}')
# internal consistency: does Poisson(meanET) split reproduce rho?
mu=meanET/2; Plevel=sum(poisson.pmf(j,mu)**2 for j in range(12))
print(f'  -> Poisson model implied P(stay level) = {Plevel:.3f}   (data rho = 0.636)  [RESOLVES the goals-vs-retention tension]')

# --- calibrate phi on a canonical even ET matchup so model P(stay level)=0.636 ---
target=0.636
def Plevel_even(phi,lam):
    mu=lam/3*phi; return sum(poisson.pmf(j,mu)**2 for j in range(12))
import scipy.optimize as opt
for lam in (1.0,1.15,1.30):
    phi=opt.brentq(lambda p: Plevel_even(p,lam)-target,0.01,3.0)
    print(f'  canonical even match lambda/team={lam}: calibrated phi={phi:.3f}')
PHI=opt.brentq(lambda p: Plevel_even(p,1.15)-target,0.01,3.0)
print(f'\nDEPLOY phi={PHI:.3f} (canonical lambda=1.15). Sensitivity band phi in [{opt.brentq(lambda p:Plevel_even(p,1.30)-target,.01,3):.2f},{opt.brentq(lambda p:Plevel_even(p,1.0)-target,.01,3):.2f}]')

games=[('South Africa','Canada',[141,121,64]),('Netherlands','Morocco',[80,114,122]),
 ('Mexico','Ecuador',[84,108,122]),('Belgium','Senegal',[80,112,123]),
 ('Portugal','Croatia',[73,114,133]),('Switzerland','Algeria',[61,122,148]),
 ('Colombia','Ghana',[66,114,139]),('Australia','Egypt',[113,106,92])]
def res(t):
    al={'Cote dIvoire':"Cote d'Ivoire"}
    return t if t in W2C else al.get(t,t)
print(f"\n{'match':<22}{'  P90: W / D / L  modal':<30}{'  P120: W / D / L  modal':<30}{'P(D)90->120':<14}{'pick90->120 (model-only)'}")
for th,ta,rew in games:
    if th not in W2C or ta not in W2C: print(th,ta,'UNRESOLVED'); continue
    Mx,lh,la=joint90(th,ta); p90=wdl(Mx); m90=modal(Mx)
    M120=transform120(Mx,lh,la,PHI); p120=wdl(M120); m120=modal(M120)
    ev90=[p90[i]*rew[i] for i in range(3)]; ev120=[p120[i]*rew[i] for i in range(3)]
    lab=[th[:11],'Draw',ta[:11]]; pk90=int(np.argmax(ev90)); pk120=int(np.argmax(ev120))
    flip='  ***FLIP' if pk90!=pk120 else ''
    print(f"{(th[:10]+'-'+ta[:9]):<22}{p90[0]*100:4.0f}/{p90[1]*100:4.0f}/{p90[2]*100:4.0f}  {m90[0]:<6}      {p120[0]*100:4.0f}/{p120[1]*100:4.0f}/{p120[2]*100:4.0f}  {m120[0]:<6}    {p90[1]*100:4.1f}->{p120[1]*100:4.1f}%    {lab[pk90]}->{lab[pk120]}{flip}")
