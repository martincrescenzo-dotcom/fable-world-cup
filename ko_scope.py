"""SCOPING (not a deployed pick): does the ET 90'->120' transform flip the EV pick?
Draft transform with a PRIOR phi (unvalidated). Model-only probs (no market blend) to
isolate the transform's effect. Reward layout = [V/home, N/draw, D/away]."""
import json, numpy as np
from scipy.stats import nbinom, poisson
AD=json.load(open('attdef.json')); W2C=json.load(open('wc_to_canon.json')); Q=json.load(open('qualification_v5.json'))
mug=AD['_meta']['mu_goals']; R=Q['r']; MAXG=12; GAMMA=1.5

def lam_pair(th,ta):
    lh=np.exp(mug+AT(th)-DF(ta)); la=np.exp(mug+AT(ta)-DF(th))
    M=0.5*(np.log(lh)+np.log(la)); D=0.5*(np.log(lh)-np.log(la))
    return float(np.exp(M+GAMMA*D)), float(np.exp(M-GAMMA*D))
def AT(t): return AD[W2C[t]]['ATT']
def DF(t): return AD[W2C[t]]['DEF']
def nbvec(lam):
    p=R/(R+lam); v=nbinom.pmf(np.arange(MAXG+1),R,p); return v/v.sum()

def joint90(th,ta):
    lh,la=lam_pair(th,ta); Mx=np.outer(nbvec(lh),nbvec(la)); Mx/=Mx.sum(); return Mx,lh,la

def transform120(Mx,lh,la,phi):
    """Keep decisive cells; convolve each draw cell k-k with independent Poisson ET
    increments at suppressed rates (1/3)*lambda*phi. Returns 120' joint."""
    n=Mx.shape[0]
    le,lr=lh*(1/3)*phi, la*(1/3)*phi
    eh=poisson.pmf(np.arange(n),le); ea=poisson.pmf(np.arange(n),lr)
    eh/=eh.sum(); ea/=ea.sum()
    ET=np.outer(eh,ea)                       # ET increment joint
    out=np.array(Mx);
    for k in range(n):
        m=Mx[k,k]
        if m<=0: continue
        out[k,k]-=m                          # remove the drawn mass, redistribute
        for dh in range(n-k):
            for da in range(n-k):
                out[k+dh,k+da]+=m*ET[dh,da]
    return out/out.sum()

def wdl(Mx):
    return np.tril(Mx,-1).sum(), np.trace(Mx), np.triu(Mx,1).sum()

# French reward table, mapped to engine names. [home, draw, away]
games=[
 ('South Africa','Canada',[141,121,64]),
 ('Brazil','Japan',[65,121,141]),
 ('Germany','Paraguay',[45,140,169]),
 ('Netherlands','Morocco',[80,114,122]),
 ("Cote d'Ivoire",'Norway',[123,119,75]),
 ('France','Sweden',[38,148,182]),
 ('Mexico','Ecuador',[84,108,122]),
 ('England','DR Congo',[39,144,181]),
 ('Belgium','Senegal',[80,112,123]),
 ('United States','Bosnia and Herzegovina',[52,132,157]),
 ('Spain','Austria',[41,140,182]),
 ('Portugal','Croatia',[73,114,133]),
 ('Switzerland','Algeria',[61,122,148]),
 ('Australia','Egypt',[113,106,92]),
 ('Argentina','Cape Verde',[25,165,213]),
 ('Colombia','Ghana',[66,114,139]),
]

def resolve(t):
    if t in W2C: return t
    # try a few aliases
    al={'DR Congo':['DR Congo','Congo DR','Democratic Republic of the Congo','Congo'],
        'Cape Verde':['Cape Verde','Cabo Verde'],
        "Cote d'Ivoire":["Cote d'Ivoire","Côte d'Ivoire",'Ivory Coast'],
        'United States':['United States','USA','United States of America'],
        'South Korea':['South Korea','Korea Republic','Korea']}
    for c in al.get(t,[]):
        if c in W2C: return c
    return None

phis=[0.6,0.7,0.8]
LB=lambda labels,i: labels[i]
print(f"{'match':<26}{'pick90':<9}{'P(D)90':>7} | "+ "".join([f"pick120@{p}  P(D)  ".ljust(20) for p in phis]))
flips=set()
for th,ta,rew in games:
    rh,rr=resolve(th),resolve(ta)
    if rh is None or rr is None:
        print(f"{th[:12]}-{ta[:10]:<12} UNRESOLVED  th={rh} ta={rr}"); continue
    Mx,lh,la=joint90(rh,rr); labels=[th,'Draw',ta]
    p90=np.array(wdl(Mx)); ev90=p90*rew; pk90=int(np.argmax(ev90))
    row=f"{(th[:12]+'-'+ta[:10]):<26}{labels[pk90][:8]:<9}{p90[1]*100:>6.1f}% | "
    for phi in phis:
        M120=transform120(Mx,lh,la,phi); p120=np.array(wdl(M120)); ev120=p120*rew; pk120=int(np.argmax(ev120))
        flag='*' if pk120!=pk90 else ' '
        if pk120!=pk90: flips.add((th,ta))
        row+=f"{labels[pk120][:7]:<7}{flag} {p120[1]*100:>5.1f}%   "
    print(row)
print(f"\nMatches where the transform FLIPS the EV pick (any phi): {len(flips)}")
for f in flips: print('  ', f[0],'-',f[1])
