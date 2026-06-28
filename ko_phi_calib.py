"""Ground phi against an empirical anchor: P(still level after ET | level at 90') ~ 0.5
(roughly half of matches level at 90' in major KOs go to penalties). For each phi, compute
the MODEL-implied conditional draw-survival, averaged over the R32 slate's at-90 draw cells,
and see which phi reproduces ~0.46-0.50."""
import json, numpy as np
from scipy.stats import nbinom, poisson
AD=json.load(open('attdef.json')); W2C=json.load(open('wc_to_canon.json')); Q=json.load(open('qualification_v5.json'))
mug=AD['_meta']['mu_goals']; R=Q['r']; MAXG=12; GAMMA=1.5
def AT(t): return AD[W2C[t]]['ATT']
def DF(t): return AD[W2C[t]]['DEF']
def lam_pair(th,ta):
    lh=np.exp(mug+AT(th)-DF(ta)); la=np.exp(mug+AT(ta)-DF(th))
    M=0.5*(np.log(lh)+np.log(la)); D=0.5*(np.log(lh)-np.log(la))
    return float(np.exp(M+GAMMA*D)), float(np.exp(M-GAMMA*D))
def nbvec(lam):
    p=R/(R+lam); v=nbinom.pmf(np.arange(MAXG+1),R,p); return v/v.sum()
def joint90(th,ta):
    lh,la=lam_pair(th,ta); Mx=np.outer(nbvec(lh),nbvec(la)); Mx/=Mx.sum(); return Mx,lh,la

def survive_draw(lh,la,phi):
    """P(ET adds equal increment to both | started level) = P(still level after ET)."""
    n=MAXG+1
    le,lr=lh*(1/3)*phi, la*(1/3)*phi
    eh=poisson.pmf(np.arange(n),le); eh/=eh.sum()
    ea=poisson.pmf(np.arange(n),lr); ea/=ea.sum()
    return float(sum(eh[d]*ea[d] for d in range(n)))

def resolve(t):
    if t in W2C: return t
    al={'DR Congo':['DR Congo','Congo DR'],'Cape Verde':['Cape Verde','Cabo Verde'],
        "Cote d'Ivoire":["Cote d'Ivoire",'Ivory Coast'],'United States':['United States','USA']}
    for c in al.get(t,[]):
        if c in W2C: return c
    return None

games=[('South Africa','Canada'),('Brazil','Japan'),('Germany','Paraguay'),('Netherlands','Morocco'),
 ("Cote d'Ivoire",'Norway'),('France','Sweden'),('Mexico','Ecuador'),('England','DR Congo'),
 ('Belgium','Senegal'),('United States','Bosnia and Herzegovina'),('Spain','Austria'),('Portugal','Croatia'),
 ('Switzerland','Algeria'),('Australia','Egypt'),('Argentina','Cape Verde'),('Colombia','Ghana')]

print("Empirical anchor: ~0.46-0.50 of post-90' draws end still level (-> penalties).\n")
print(f"{'phi':>5} {'mean P(still level|drew@90)':>28} {'SA-Can P(still level)':>22}")
for phi in [0.5,0.6,0.7,0.8,0.9,1.0]:
    svs=[]; sa=None
    for th,ta in games:
        rh,rr=resolve(th),resolve(ta)
        if rh is None or rr is None: continue
        Mx,lh,la=joint90(rh,rr)
        # weight by the at-90 drawn mass distribution across cells -> use lh,la directly (dominant draw is 0-0/1-1)
        s=survive_draw(lh,la,phi); svs.append(s)
        if th=='South Africa': sa=s
    print(f"{phi:>5.1f} {np.mean(svs)*100:>26.1f}% {sa*100:>21.1f}%")
