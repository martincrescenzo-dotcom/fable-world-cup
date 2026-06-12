"""PRODUCTION match-pick pipeline (points game, Rule A + rarity bonus + X2 tracking).

Usage: edit MATCHES below, run. Per match you can supply:
  rewards   [home, draw, away]            REQUIRED
  bookie    {"1-0":6.5, "2-0":7.0, ...}   optional Winamax/Betclic score-exact odds (any subset)
  overlay   (dATT_h, dDEF_h, dATT_a, dDEF_a)  optional injury/suspension overlay (log units)
  flags     free-text motivation notes (dead rubber, rotation risk...)

Pipeline per match:
 1. v6 probabilities (att/def -> gamma=1.5 -> NB r=9.5) + overlay.
 2. Outcome EV = p*reward -> outcome pick (argmax of TOTAL EV incl. best score bonus).
 3. Crowd model: plausibility = de-vigged bookie grid if supplied (recreational players anchor
    on displayed odds) else model probs; crowd ∝ plaus^beta * salience^sal_strength (params from
    crowd_params.json, calibrated by register_bonus.py).
 4. Band-robust bonus EV: tier evaluated at crowd*0.7 / *1.0 / *1.43; expected over scenarios;
    BOUNDARY flag when scenarios disagree.
 5. Score pick = argmax robust bonus EV within picked outcome.
 6. X2 evaluation: E_total >= X2_THRESHOLD and no motivation flags -> candidate (logged).
"""
import json, numpy as np
from scipy.stats import nbinom

# ------------------------------------------------------------------ inputs
MATCHES = [
 dict(home='Canada', away='Bosnia and Herzegovina', rewards=[65,117,125], date='2026-06-12',
      overlay=(-0.08,-0.02,0,0), flags=''),   # Davies OUT (partially priced), Flores
 dict(home='United States', away='Paraguay', rewards=[74,113,115], date='2026-06-12'),
 dict(home='Qatar', away='Switzerland', rewards=[172,141,33], date='2026-06-13'),
 dict(home='Brazil', away='Morocco', rewards=[55,122,140], date='2026-06-13',
      overlay=(-0.13,-0.08,0,-0.06), flags=''),  # Neymar doubt+Rodrygo/Estevao/Militao; Aguerd out (MAR)
 dict(home='Haiti', away='Scotland', rewards=[154,131,44], date='2026-06-13'),
 dict(home='Germany', away='Curacao', rewards=[15,179,222], date='2026-06-14'),
 dict(home='Australia', away='Turkey', rewards=[126,115,66], date='2026-06-14'),
 dict(home='Netherlands', away='Japan', rewards=[74,115,113], date='2026-06-14',
      overlay=(-0.08,-0.10,-0.12,0)),  # NL: Simons/DeLigt/Timber; JPN: Mitoma
 dict(home='Ivory Coast', away='Ecuador', rewards=[108,101,85], date='2026-06-14'),
 dict(home='Sweden', away='Tunisia', rewards=[72,110,122], date='2026-06-14'),
]
X2_THRESHOLD = 45.0
CONTRARIAN_EDGE = 1.15      # model/implied ratio that marks a contrarian X2 profile
WINAMAX_VALID_THROUGH = '2026-06-14'   # covered by 'until 14th' CSV (ingested 2026-06-12-v2):
                                       # valid through Sunday-night matches; raise on next fresh CSV
VAR_TIEBREAK_EV = 1.5       # rank strategy (230k/1M, dense top): among scores within this EV of the
                            # best, prefer the LOWER-crowd one — rarer points shared with fewer rivals

# ------------------------------------------------------------------ engine (v6, frozen)
AD=json.load(open('attdef.json')); W2C=json.load(open('wc_to_canon.json'))
DP=json.load(open('deployed_params.json')); CP=json.load(open('crowd_params.json'))
mug=AD['_meta']['mu_goals']; R=DP['R']; MAXG=DP['MAXG']; GAMMA=DP['GAMMA']
BETA=CP['beta']; SSTR=CP['sal_strength']
SAL={(1,0):1.5,(2,0):1.5,(2,1):1.6,(3,0):1.0,(3,1):0.75,(4,0):0.45,(4,1):0.4,(3,2):0.5,
     (1,1):1.7,(0,0):0.55,(2,2):0.9,(3,3):0.3}
def sal(a,b):
    s=SAL.get((a,b),SAL.get((b,a),0.25 if (a+b)>=5 else 0.6))
    return s**SSTR
def tier(share):
    if share>0.30: return 20
    if share>0.20: return 30
    if share>0.05: return 50
    if share>0.005: return 70
    return 100
def lam_pair(th,ta,ov=(0,0,0,0)):
    lh=np.exp(mug+AD[W2C[th]]['ATT']-AD[W2C[ta]]['DEF'])
    la=np.exp(mug+AD[W2C[ta]]['ATT']-AD[W2C[th]]['DEF'])
    M=0.5*(np.log(lh)+np.log(la)); D=0.5*(np.log(lh)-np.log(la))
    lh,la=np.exp(M+GAMMA*D),np.exp(M-GAMMA*D)
    lh*=np.exp(ov[0]-ov[3]); la*=np.exp(ov[2]-ov[1])   # my ATT up / their DEF down etc.
    return float(np.clip(lh,0.08,6)),float(np.clip(la,0.08,6))
def nbv(lam):
    p=R/(R+lam); v=nbinom.pmf(np.arange(MAXG+1),R,p); return v/v.sum()

import re
def parse_bookie(bk):
    """de-vig a (possibly partial) score-exact odds dict -> prob dict.
    Robust to French/typed input: '1-0' '1 - 0' '1:0' '2–1' keys; '6,5' comma-decimal odds."""
    if not bk: return None
    out={}
    for k,o in bk.items():
        nums=re.findall(r'\d+', str(k))
        if len(nums)!=2:
            raise ValueError(f"bookie score key {k!r} unparseable — expected like '1-0'")
        odds=float(str(o).replace(',','.').strip())
        if odds<1.01: raise ValueError(f"bookie odds {o!r} for {k!r} implausible (<1.01) — typo?")
        out[(int(nums[0]),int(nums[1]))]=1.0/odds
    return out

def load_winamax(th,ta):
    """latest Winamax snapshot for this match, if ingested (winamax_ingest.py)."""
    import os
    if not os.path.exists('winamax_snapshots.json'): return None
    sn=json.load(open('winamax_snapshots.json'))
    key=f'{th}|{ta}'
    if key not in sn: return None
    s=sn[key][-1]
    print(f"  [winamax snapshot {s['snap_date']} loaded as plausibility base]")
    return {sc:o for sc,o in s['odds'].items() if sc!='Autre'}

def analyse(m):
    th,ta=m['home'],m['away']; rew=m['rewards']; ov=m.get('overlay',(0,0,0,0))
    used_bookie=bool(m.get('bookie'))
    if not used_bookie:
        mdate=m.get('date')
        if mdate is None:
            print('  !! match has no date= field — cannot check snapshot freshness; SKIPPING winamax auto-load')
        elif mdate>WINAMAX_VALID_THROUGH:
            print(f'  [winamax snapshot SKIPPED: match {mdate} beyond freshness cutoff {WINAMAX_VALID_THROUGH} — early money; awaiting fresh CSV]')
        else:
            wb=load_winamax(th,ta)
            if wb: m=dict(m,bookie=wb); used_bookie=True
    lh,la=lam_pair(th,ta,ov)
    M=np.outer(nbv(lh),nbv(la)); M/=M.sum()
    pm=[float(np.tril(M,-1).sum()),float(np.trace(M)),float(np.triu(M,1).sum())]
    imp=np.array([1/r for r in rew]); imp/=imp.sum()
    bk=parse_bookie(m.get('bookie'))
    regions={0:[(a,b) for a in range(MAXG+1) for b in range(MAXG+1) if a>b],
             1:[(a,a) for a in range(MAXG+1)],
             2:[(a,b) for a in range(MAXG+1) for b in range(MAXG+1) if a<b]}
    res={'pm':pm,'imp':imp.tolist(),'lams':(lh,la),'outcomes':{}}
    for oi in range(3):
        cells=regions[oi]
        # plausibility base for crowd: de-vigged bookie where available, model elsewhere
        plaus=[]
        for a,b in cells:
            if bk and (a,b) in bk: plaus.append(bk[(a,b)])
            elif bk: plaus.append(M[a,b]*sum(bk.values())/ (sum(M[x,y] for x,y in bk)))  # scale model into bookie units
            else: plaus.append(M[a,b])
        plaus=np.array(plaus)
        crowd=(plaus**BETA)*np.array([sal(a,b) for a,b in cells]); crowd/=crowd.sum()
        # p(score) for EV: PURE v6 model (validated OOS x3). Market enters the CROWD layer only —
        # keeps E[bonus]=p(truth)*tier(behavior) factorized with independent errors. Where model
        # and market diverge on a cell, FLAG it (visible caution), never silently blend.
        pmod=np.array([M[a,b] for a,b in cells]); pmod_n=pmod/pmod.sum()
        qn=plaus/plaus.sum() if bk else None
        rows=[]
        for k,(a,b) in enumerate(cells):
            tiers=[tier(crowd[k]*f) for f in (0.7,1.0,1.43)]
            eb=float(M[a,b]*np.mean(tiers))
            div=float(pmod_n[k]/qn[k]) if (qn is not None and qn[k]>1e-9) else None
            rows.append(dict(score=(a,b),p=float(M[a,b]),crowd=float(crowd[k]),
                             tiers=tiers,boundary=(len(set(tiers))>1),ebonus=eb,div=div))
        rows.sort(key=lambda r:-r['ebonus'])
        # rank-strategy tie-break: within VAR_TIEBREAK_EV of best AND keeping >=50% of the best's
        # hit probability, prefer the rarer (lower-crowd) score. The p-floor stops variance-chasing
        # from drifting into the unvalidated deep tail of the crowd curve.
        if len(rows)>1:
            # tiers list order = [optimistic(crowd*0.7), mid, pessimistic(crowd*1.43)]
            pess=lambda x: x['p']*x['tiers'][2]
            near=[x for x in rows if rows[0]['ebonus']-x['ebonus']<=VAR_TIEBREAK_EV
                  and x['p']>=0.5*rows[0]['p'] and pess(x)>=pess(rows[0])]
            if near:
                pick0=min(near,key=lambda x:x['crowd'])
                if pick0 is not rows[0]:
                    rows.remove(pick0); rows.insert(0,pick0)
        base_ev=pm[oi]*rew[oi]
        res['outcomes'][oi]=dict(base_ev=base_ev,total_ev=base_ev+rows[0]['ebonus'],rows=rows)
    pick=max(range(3),key=lambda oi:res['outcomes'][oi]['total_ev'])
    # warn if bonus chasing flipped the outcome vs pure base EV
    base_pick=max(range(3),key=lambda oi:res['outcomes'][oi]['base_ev'])
    res['pick']=pick; res['flip_warn']=(pick!=base_pick); res['used_bookie']=used_bookie
    # ROBUSTNESS view: liquid outcome market (Polymarket) as alternate p — flag if pick flips.
    # Market stays OUT of p (locked principle); this is a visible dual-EV check, not a blend.
    res['pm_check']=None
    try:
        import os
        if os.path.exists('polymarket_matches.json'):
            PM=json.load(open('polymarket_matches.json'))
            key=f'{th}|{ta}'
            if key in PM:
                s=PM[key][-1]; pmkt=[s['h'],s['d'],s['a']]
                ev_mkt=[pmkt[i]*rew[i] for i in range(3)]
                pick_mkt=int(np.argmax(ev_mkt))
                res['pm_check']=dict(p=pmkt,ev=ev_mkt,pick=pick_mkt,ts=s['ts'],
                                     flips=(pick_mkt!=pick),
                                     maxgap=float(max(abs(pm[i]-pmkt[i]) for i in range(3))))
    except Exception as e:
        print('  (pm_check failed:',repr(e)[:50],')')
    # X2 evaluation
    o=res['outcomes'][pick]
    edge=pm[pick]/imp[pick]
    res['x2']=dict(candidate=(o['total_ev']>=X2_THRESHOLD and not m.get('flags')),
                   e_total=o['total_ev'],contrarian=(edge>=CONTRARIAN_EDGE and pick!=int(np.argmax(imp))),
                   edge=float(edge))
    return res

LBL=lambda m:[m['home'],'Draw',m['away']]
if not MATCHES:
    print('No MATCHES configured — edit the MATCHES list at the top with this matchday slate.')
for m in MATCHES:
    r=analyse(m)
    pm=r['pm']; pick=r['pick']; o=r['outcomes'][pick]; best=o['rows'][0]
    lab=LBL(m)
    print(f"=== {m['home']} vs {m['away']} ===  model W/D/L {pm[0]*100:.0f}/{pm[1]*100:.0f}/{pm[2]*100:.0f}  (xG {r['lams'][0]:.2f}-{r['lams'][1]:.2f})")
    if m.get('overlay',(0,0,0,0))!=(0,0,0,0): print(f"  overlay applied: {m['overlay']}")
    if not r['used_bookie']: print('  (NO market data — crowd tiers on model-prob base; LOWER confidence)')
    for oi in range(3):
        oo=r['outcomes'][oi]; tag=' <== PICK' if oi==pick else ''
        print(f"  {lab[oi]:<24} baseEV {oo['base_ev']:5.1f}  totalEV {oo['total_ev']:5.1f}{tag}")
    if r['flip_warn']: print('  !! WARNING: bonus EV flipped the outcome pick vs pure base EV — review manually')
    a,b=best['score']
    bflag=' [BOUNDARY-tier risk]' if best['boundary'] else ''
    dflag=''
    if best.get('div') and (best['div']>1.3 or best['div']<0.77):
        dflag=f" [DIVERGENCE: model/market={best['div']:.2f} on this cell — model may be {'hot' if best['div']>1 else 'cold'}; consider alt]"
    print(f"  SCORE PICK: {a}-{b}  p={best['p']*100:.1f}%  crowd~{best['crowd']*100:.1f}%  tiers(opt/mid/pess) {best['tiers']}  EbonusEV={best['ebonus']:.2f}{bflag}{dflag}")
    alt=o['rows'][1]; a2,b2=alt['score']
    print(f"  alt: {a2}-{b2} p={alt['p']*100:.1f}% Ebonus={alt['ebonus']:.2f} | naive modal: {max(o['rows'],key=lambda x:x['p'])['score']}")
    pmc=r.get('pm_check')
    if pmc:
        gap=pmc['maxgap']
        if pmc['flips']:
            print(f"  !! ROBUSTNESS: Polymarket p={['%.2f'%v for v in pmc['p']]} FLIPS the pick to {lab[pmc['pick']]} "
                  f"(market EV {pmc['ev'][pmc['pick']]:.1f} vs our pick's market EV {pmc['ev'][pick]:.1f}) — decide explicitly")
        elif gap>0.10:
            print(f"  ~ pm divergence {gap*100:.0f}pts (PM {pmc['ts']}: {['%.2f'%v for v in pmc['p']]}) — pick unchanged but model heat noted")
    x=r['x2']
    if x['candidate']:
        print(f"  ** X2 CANDIDATE **  E_total={x['e_total']:.1f}{' CONTRARIAN (field misses it -> separation)' if x['contrarian'] else ''}")
    print()
