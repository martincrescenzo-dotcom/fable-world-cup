"""PREFLIGHT — run BEFORE every matchday pick. Detects silent corruption of the deployed
engine and input-layer fragility. Exit code 0 = green; any FAIL = fix before picking.
Restore procedure on hash mismatch: copy the file back from frozen/ ."""
import json, os, sys, hashlib
fails=[]; warns=[]
def check(name,ok,fail_msg,warn=False):
    if ok: print(f'  PASS  {name}')
    else:
        print(f'  {"WARN" if warn else "FAIL"}  {name}: {fail_msg}')
        (warns if warn else fails).append(name)

print('=== preflight ===')
# 1. deployed params + artifact integrity
try:
    P=json.load(open('deployed_params.json'))
    check('deployed_params.json',True,'')
    for f,h in P['artifacts'].items():
        cur=hashlib.sha256(open(f,'rb').read()).hexdigest() if os.path.exists(f) else 'MISSING'
        check(f'artifact {f}',cur==h,f'hash mismatch or missing — deployed engine MUTATED. Restore: copy frozen/{f} over {f}')
except Exception as e:
    check('deployed_params.json',False,repr(e)); P=None

# 2. live files parse
for f in ['crowd_params.json','crowd_obs.json','wc_data.json']:
    try: json.load(open(f,encoding='utf-8')); check(f'parse {f}',True,'')
    except Exception as e: check(f'parse {f}',False,repr(e)[:60])

# 3. all 48 teams resolve
try:
    AD=json.load(open('attdef.json')); W2C=json.load(open('wc_to_canon.json')); WC=json.load(open('wc_data.json'))
    bad=[t['team'] for g in WC for t in WC[g] if W2C.get(t['team']) not in AD]
    check('48-team resolution',not bad,f'unresolved: {bad}')
except Exception as e:
    check('48-team resolution',False,repr(e)[:60])

# 4. obs duplicates
try:
    obs=json.load(open('crowd_obs.json'))
    keys=[(o['match'],tuple(o['actual_score'])) for o in obs]
    check('crowd_obs dedup',len(keys)==len(set(keys)),'duplicate observations — calibration biased; remove dups')
except Exception as e: check('crowd_obs dedup',False,repr(e)[:60])

# 5. engine smoke test (one fixture end-to-end)
try:
    import numpy as np
    from scipy.stats import nbinom
    R=P['R']; G=P['GAMMA']; mug=AD['_meta']['mu_goals']
    lh=np.exp(mug+AD[W2C['Spain']]['ATT']-AD[W2C['Cape Verde']]['DEF'])
    la=np.exp(mug+AD[W2C['Cape Verde']]['ATT']-AD[W2C['Spain']]['DEF'])
    M=0.5*(np.log(lh)+np.log(la)); D=0.5*(np.log(lh)-np.log(la))
    lh,la=np.exp(M+G*D),np.exp(M-G*D)
    p=R/(R+lh); v=nbinom.pmf(np.arange(P['MAXG']+1),R,p)
    ok=bool(0.5<lh<6 and 0.05<la<2 and abs(v.sum()-1)<0.05)
    check('engine smoke test',ok,f'lambdas {lh:.2f}/{la:.2f}, grid mass {v.sum():.3f} (truncation too tight? raise MAXG)')
except Exception as e: check('engine smoke test',False,repr(e)[:70])

# 6. consistency: R in params vs qualification_v5 (drift detector, warn only)
try:
    Q=json.load(open('qualification_v5.json'))
    check('R consistency (v5 file vs deployed)',abs(Q.get('r',-1)-P['R'])<1e-6,
          'qualification_v5.json regenerated with different r — deployed R unchanged (OK) but investigate',warn=True)
except Exception: pass

print(f'\\n{"GREEN — safe to pick." if not fails else "RED — fix FAILs before picking."} ({len(fails)} fail, {len(warns)} warn)')
sys.exit(1 if fails else 0)
