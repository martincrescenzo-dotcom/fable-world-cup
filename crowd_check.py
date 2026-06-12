"""Validation 1: v6 NB score probabilities vs de-vigged Winamax exact-score odds (shape check
of the plausibility anchor). Validation 2: bettor-share/odds decomposition diagnostic
(perceived-prob proxy; early-money caveat applies)."""
import json, numpy as np
from scipy.stats import nbinom
AD=json.load(open('attdef.json')); W2C=json.load(open('wc_to_canon.json')); DP=json.load(open('deployed_params.json'))
SN=json.load(open('winamax_snapshots.json'))
mug=AD['_meta']['mu_goals']; R=DP['R']; G=DP['GAMMA']; MAXG=DP['MAXG']
def lam_pair(th,ta):
    lh=np.exp(mug+AD[W2C[th]]['ATT']-AD[W2C[ta]]['DEF']); la=np.exp(mug+AD[W2C[ta]]['ATT']-AD[W2C[th]]['DEF'])
    M=0.5*(np.log(lh)+np.log(la)); D=0.5*(np.log(lh)-np.log(la))
    return float(np.exp(M+G*D)),float(np.exp(M-G*D))
def nbv(lam):
    p=R/(R+lam); v=nbinom.pmf(np.arange(MAXG+1),R,p); return v/v.sum()

print(f"{'match':<30}{'corr':>6}{'meanAD':>8}  notable cell gaps (model% vs bookie%)")
agg00=[]; aggfav=[]
for key,snaps in SN.items():
    th,ta=key.split('|'); s=snaps[-1]
    lh,la=lam_pair(th,ta); M=np.outer(nbv(lh),nbv(la)); M/=M.sum()
    inv={sc:1.0/o for sc,o in s['odds'].items()}
    Z=sum(inv.values())
    q={sc:v/Z for sc,v in inv.items()}                  # de-vigged, incl 'Autre'
    listed=[sc for sc in q if sc!='Autre']
    cells=[(int(a),int(b)) for a,b in (sc.split('-') for sc in listed)]
    pmod=np.array([M[a,b] if a<=MAXG and b<=MAXG else 0 for a,b in cells])
    pmod_autre=1-pmod.sum()
    qv=np.array([q[sc] for sc in listed])
    corr=np.corrcoef(pmod,qv)[0,1]
    mad=np.mean(np.abs(pmod-qv))
    gaps=sorted(zip(listed,pmod,qv),key=lambda x:-abs(x[1]-x[2]))[:3]
    gs='; '.join(f'{sc}: {p*100:.0f} vs {qq*100:.0f}' for sc,p,qq in gaps)
    print(f'{th[:14]+" v "+ta[:12]:<30}{corr:>6.2f}{mad*100:>7.1f}%  {gs}  | Autre: {pmod_autre*100:.0f} vs {q.get("Autre",0)*100:.0f}')
    if '0-0' in q: agg00.append((M[0,0],q['0-0']))
    # favourite biggest-win listed cell sanity
print()
a=np.array(agg00)
print(f'0-0 systematic: model mean {a[:,0].mean()*100:.1f}% vs bookie mean {a[:,1].mean()*100:.1f}%  (n={len(a)})')
print()
print('Bettor-share/odds decomposition (perceived-prob proxy = pct/odds, normalised; EARLY MONEY):')
for key,snaps in list(SN.items())[:3]:
    s=snaps[-1]
    ratio={sc:s['pct'][sc]/s['odds'][sc] for sc in s['odds'] if s['pct'].get(sc,0)>0}
    Z=sum(ratio.values())
    top=sorted(ratio.items(),key=lambda x:-x[1])[:4]
    print(f"  {key:<32} "+', '.join(f'{sc} {v/Z*100:.0f}%' for sc,v in top))
