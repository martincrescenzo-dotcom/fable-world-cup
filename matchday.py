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
MATCHES = [   # MD6 slate 2026-06-19 (fieldpct=[H,D,A]=Repartition from user; rewards=Cotes from user).
 # market=[H,D,A]=INDEPENDENT de-vigged 1X2 from sharp books via WebSearch 2026-06-19 (DraftKings/FanDuel/BetOnline).
 # Model-blind scan 2026-06-19: Pulisic OUT (USA, calf) -> USA ATT -0.07 (halved; mkt likely priced). Brazil tourn
 # injuries (Rodrygo/Militao/Estevao) -0.05/-0.04 halved. Paraguay Caballero+Sosa out -> Paraguay ATT -0.05.
 dict(home='United States', away='Australia', rewards=[58,119,153], date='2026-06-19', fieldpct=[.75,.18,.07],
      market=[.601,.217,.182], overlay=(-0.07,0,0,0)),
 dict(home='Scotland', away='Morocco', rewards=[99,112,91], date='2026-06-19', fieldpct=[.04,.16,.79],
      market=[.173,.264,.563]),
 dict(home='Brazil', away='Haiti', rewards=[21,167,198], date='2026-06-19', fieldpct=[.95,.04,.01],
      market=[.868,.087,.045], overlay=(-0.05,-0.04,0,0)),
 dict(home='Turkey', away='Paraguay', rewards=[84,113,126], date='2026-06-19', fieldpct=[.56,.33,.11],
      market=[.492,.281,.227], overlay=(0,0,-0.05,0)),
]
X2_THRESHOLD = 45.0
CONTRARIAN_EDGE = 1.15      # model/implied ratio that marks a contrarian X2 profile
WINAMAX_VALID_THROUGH = '2026-06-16'   # fresh CSV ingested 2026-06-16 (France-Senegal slate)
                                       # (Belgium/SaudiArabia/Iran matches); raise on next fresh CSV
VAR_TIEBREAK_EV = 1.5       # rank strategy: among scores within this EV of the best, prefer LOWER-crowd
LEAGUE_MODE = True          # objective = TOP-2 of 13-person league over ~100 remaining matches.
DIFF_BAND_FRAC = 0.05      # AUDIT 2026-06-16: CORRECTED from 0.0. league_sim2 (which set 0.0) was BROKEN:
                          # (a) ran on STALE standings (user #8 / 115-deficit; actually #10 / 284-deficit),
                          # (b) modeled the 13 rivals as INDEPENDENT pickers, not the correlated favourite-
                          #     herd they demonstrably are (top-5 data: 5/5 agreement on 7 matches, 4/5 on
                          #     most) -> a strawman that erased the value of decorrelation.
                          # future_sim.py (current standings, rivals=herd, 88-match horizon, P(top-2)
                          # objective) shows differentiation ~TRIPLES top-2 odds (3.9%->~10%); break-even
                          # EV cost ~7%. RULE: take field-underpicked + MARKET-CONFIRMED decorrelation up to
                          # ~5% of per-match EV; never pay more. The 0.6 market lean below is the market-
                          # confirmed VETO (a model-only contrarian like Ecuador falls outside the band).
                          # NB this is the AXIS-B lever (you vs the field's picks). AXIS-A (you vs market) =
                          # FOLLOW the market; no maximin hedges (they cost USA + Haiti winners in MD1).
BONUS_MODE = 'coarse'      # 2026-06-14: crowd model unconverged at n=8 -> RETIRE fine E[bonus] opt (noise+thrash).
                          # Score = MODAL (highest-p) within outcome = max hit-prob; step off 1-1 ONLY (the one
                          # cell with rock-solid >30% over-herding, 3/3 obs). Model-free; ignores fine tier rank.

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
        # hit probability, prefer the rarer (lower-crowd) score.
        # NOTE: this extra rarity bias is for the MEGA-FIELD (1M) — in a 13-person league the bonus
        # TIER already prices rarity, and shaving crowd 6%->3% buys ~0 rank vs 12 rivals. So under
        # LEAGUE_MODE we DISABLE it and just take max E[bonus]. (Audit finding 2026-06-13.)
        if len(rows)>1 and not LEAGUE_MODE:
            # tiers list order = [optimistic(crowd*0.7), mid, pessimistic(crowd*1.43)]
            pess=lambda x: x['p']*x['tiers'][2]
            near=[x for x in rows if rows[0]['ebonus']-x['ebonus']<=VAR_TIEBREAK_EV
                  and x['p']>=0.5*rows[0]['p'] and pess(x)>=pess(rows[0])]
            if near:
                pick0=min(near,key=lambda x:x['crowd'])
                if pick0 is not rows[0]:
                    rows.remove(pick0); rows.insert(0,pick0)
        if BONUS_MODE=='coarse' and len(rows)>1:
            # Layer-1 only: take the modal (highest-p) score = max hit-probability, the one reliably-
            # validated lever (score model OOS-validated; crowd model is NOT). 2026-06-17 UPDATE: the
            # 1-1 STEP-OFF IS REMOVED. score_rule_backtest.py (20 obs, true-outcome-conditioned, LOO):
            # pure modal (keep 1-1) earned 190 realized bonus vs 130 for the step-off rule (+60 = +3/match)
            # -- 1-1 is the single most FREQUENT score, and a likely +20 beats chasing a 0-0 (tier 50) that
            # lands rarely. The SAME backtest REJECTED the rare-score E[bonus] optimizer (130 = tied modal-
            # step -> no realized edge; the expected edge is model-internal, swamped by exact-hit variance
            # at n=20). Caveat: sample is draw-heavy (8/20=40% vs ~28% normal) so the 1-1-FREQUENCY edge is
            # sample-dependent; the tier-20-on-1-1 part is solid (5/5). Revisit if draw rate regresses.
            by_p=sorted(rows,key=lambda r:-r['p']); pick_s=by_p[0]
            if pick_s is not rows[0]:
                rows.remove(pick_s); rows.insert(0,pick_s)
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
    # LEAGUE MODE: re-select outcome to maximise P(win league) = disciplined differentiation.
    # blend-EV (0.4 model + 0.6 market = AXIS-A lean-to-market + market-confirmed veto); among outcomes
    # within DIFF_BAND_FRAC*emax (~5% EV) of max, take least field-crowded (AXIS-B free decorrelation).
    res['league']=None
    fp=m.get('fieldpct')
    if LEAGUE_MODE and fp:
        mkt=m.get('market') or (res['pm_check']['p'] if res.get('pm_check') else pm)  # independent market: manual Kalshi/book line > Polymarket > model fallback
        res['market_used']=('manual' if m.get('market') else ('polymarket' if res.get('pm_check') else 'NONE(model-fallback)'))
        blend=[0.4*pm[i]+0.6*mkt[i] for i in range(3)]
        bev=[blend[i]*rew[i] for i in range(3)]
        emax=max(bev)
        band=DIFF_BAND_FRAC*emax
        cand=[i for i in range(3) if bev[i]>=emax-band]
        lpick=min(cand,key=lambda i: fp[i])
        res['league']=dict(blend_ev=bev,cand=cand,fieldpct=fp,prev=pick,pick=lpick,
                           differentiated=(lpick!=int(np.argmax(bev))))
        res['pick']=lpick
    # X2 evaluation
    o=res['outcomes'][pick]
    edge=pm[pick]/imp[pick]
    fp_pick=fp[pick] if (LEAGUE_MODE and fp) else None
    contrarian=(edge>=CONTRARIAN_EDGE and pick!=int(np.argmax(imp)))
    # PRIME X2 (audit 2026-06-16): high E_total + FIELD-UNDERPICKED + market-confirmed = max rank separation
    # (the Alexandre NL-Japan-draw profile, +115). A low-reward lock (Germany 15) is the OPPOSITE — never X2 it.
    prime=(o['total_ev']>=X2_THRESHOLD and fp_pick is not None and fp_pick<0.35 and o['base_ev']>=30)
    res['x2']=dict(candidate=(o['total_ev']>=X2_THRESHOLD and not m.get('flags')),
                   e_total=o['total_ev'],contrarian=contrarian,edge=float(edge),
                   field_pct=fp_pick,prime=prime)
    return res

LBL=lambda m:[m['home'],'Draw',m['away']]

# ---- INPUT-COMPLETENESS GATE (2026-06-16) — never emit picks on partial inputs (a churn failure happened:
#      produced a slate before the independent market was in hand, then revised 3x as data trickled in).
#      Assemble ALL required inputs FIRST; this fails loud if any are missing. The market=[] requirement is
#      the load-bearing one: the AXIS-A market-confirmed veto does not function without an INDEPENDENT 1X2.
def _input_gate(matches):
    probs=[]
    for m in matches:
        miss=[k for k in ('rewards','fieldpct','market')
              if not (isinstance(m.get(k),(list,tuple)) and len(m[k])==3)]
        if not m.get('date'): miss.append('date')
        mk=m.get('market')
        if isinstance(mk,(list,tuple)) and len(mk)==3 and abs(sum(mk)-1)>0.06:
            miss.append('market-not-devigged(sum!=1)')
        if miss: probs.append(f"  {m.get('home','?')} vs {m.get('away','?')}: missing/invalid {miss}")
    if probs:
        print('INPUT GATE FAILED — do NOT emit a partial slate. Assemble every input first, then run once:')
        print(chr(10).join(probs))
        print('Required/match: rewards[H,D,A], fieldpct[H,D,A], date, market[H,D,A] = INDEPENDENT de-vigged')
        print('1X2 (Polymarket slugs / Kalshi / sharp book via web / Winamax-grid-derived). Also confirm (judgment,')
        print('not gated): model-blind scan done; standings if variance-relevant. ASK the user for what is missing.')
        raise SystemExit(1)

if not MATCHES:
    print('No MATCHES configured — edit the MATCHES list at the top with this matchday slate.')
else:
    _input_gate(MATCHES)
for m in MATCHES:
    r=analyse(m)
    pm=r['pm']; pick=r['pick']; o=r['outcomes'][pick]; best=o['rows'][0]
    lab=LBL(m)
    print(f"=== {m['home']} vs {m['away']} ===  model W/D/L {pm[0]*100:.0f}/{pm[1]*100:.0f}/{pm[2]*100:.0f}  (xG {r['lams'][0]:.2f}-{r['lams'][1]:.2f})")
    if m.get('market'): print(f"  market(indep) W/D/L {m['market'][0]*100:.0f}/{m['market'][1]*100:.0f}/{m['market'][2]*100:.0f}  [{r.get('market_used')}]")
    if m.get('overlay',(0,0,0,0))!=(0,0,0,0): print(f"  overlay applied: {m['overlay']}")
    if not r['used_bookie']: print('  (NO market data — crowd tiers on model-prob base; LOWER confidence)')
    lg=r.get('league')
    for oi in range(3):
        oo=r['outcomes'][oi]; tag=' <== PICK' if oi==pick else ''
        fpx=f"  field {lg['fieldpct'][oi]*100:.0f}%  blendEV {lg['blend_ev'][oi]:4.1f}" if lg else ''
        print(f"  {lab[oi]:<24} baseEV {oo['base_ev']:5.1f}  totalEV {oo['total_ev']:5.1f}{fpx}{tag}")
    if lg and lg['differentiated']:
        print(f"  >> LEAGUE: differentiated to {lab[lg['pick']]} (field {lg['fieldpct'][lg['pick']]*100:.0f}%) "
              f"over EV-max {lab[int(__import__('numpy').argmax(lg['blend_ev']))]} — within {DIFF_BAND_FRAC*100:.0f}% EV, less crowded (AXIS-B)")
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
        fpx=f"  field {x['field_pct']*100:.0f}%" if x['field_pct'] is not None else ''
        tag=' ** PRIME (field-underpicked + market-confirmed = max separation, DEPLOY-worthy)' if x['prime'] else (' CONTRARIAN (field misses it -> separation)' if x['contrarian'] else '')
        print(f"  ** X2 CANDIDATE **  E_total={x['e_total']:.1f}{fpx}{tag}")
    print()
