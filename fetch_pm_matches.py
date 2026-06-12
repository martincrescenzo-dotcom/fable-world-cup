"""Pull Polymarket per-match 1X2 prices (slug pattern fifwc-XXX-YYY-date) -> timestamped store
polymarket_matches.json. Re-run anytime for movement tracking. Liquid OUTCOME market:
the one evidence class where market>=model is established — used as divergence check on v6."""
import requests, json, os, sys
from datetime import datetime
H={'User-Agent':'Mozilla/5.0'}
SLUGS={  # match key -> slug (extend as fixtures are discovered)
 'Canada|Bosnia and Herzegovina':'fifwc-can-bih-2026-06-12',
 'United States|Paraguay':'fifwc-usa-par-2026-06-12',
 'Qatar|Switzerland':'fifwc-qat-che-2026-06-13',
 'Brazil|Morocco':'fifwc-bra-mar-2026-06-13',
 'Haiti|Scotland':'fifwc-hai-sco-2026-06-13',
 'Ivory Coast|Ecuador':'fifwc-civ-ecu-2026-06-14',
 'Sweden|Tunisia':'fifwc-swe-tun-2026-06-14',
 'Australia|Turkey':'fifwc-aus-tur-2026-06-14',
 'Netherlands|Japan':'fifwc-nld-jpn-2026-06-14',
}
store=json.load(open('polymarket_matches.json')) if os.path.exists('polymarket_matches.json') else {}
ts=datetime.now().strftime('%Y-%m-%d %H:%M')
for key,slug in SLUGS.items():
    try:
        d=requests.get('https://gamma-api.polymarket.com/events',headers=H,params={'slug':slug},timeout=15).json()
        if not d: print('MISS',slug); continue
        out={}
        for mk in d[0]['markets']:
            nm=mk.get('groupItemTitle') or mk.get('question')
            pr=mk.get('outcomePrices'); ou=mk.get('outcomes')
            pr=json.loads(pr) if isinstance(pr,str) else pr; ou=json.loads(ou) if isinstance(ou,str) else ou
            for o,p in zip(ou,pr):
                if str(o).lower()=='yes': out[nm]=float(p)
        # normalise to [home, draw, away] by name matching
        h,a=key.split('|')
        def find(label_part):
            for nm,p in out.items():
                if label_part.lower() in nm.lower(): return p
            return None
        ALIAS={'Ivory Coast':['ivoire','ivory'],'United States':['united states','usa'],
               'Bosnia and Herzegovina':['bosnia'],'Czech Republic':['czech'],'South Korea':['korea'],
               'Turkey':['turkey','rkiye'],'Switzerland':['switzerland','suisse']}
        def matches_team(nm,team):
            keys=ALIAS.get(team,[team.lower()[:6]])
            return any(k in nm.lower() for k in keys)
        draw=next((p for nm,p in out.items() if nm.lower().startswith('draw')),None)
        ph=next((p for nm,p in out.items() if not nm.lower().startswith('draw') and matches_team(nm,h)),None)
        pa=next((p for nm,p in out.items() if not nm.lower().startswith('draw') and matches_team(nm,a)),None)
        if None in (ph,draw,pa):
            print('PARSE-WARN',key,out); continue
        s=ph+draw+pa
        store.setdefault(key,[]).append({'ts':ts,'slug':slug,'h':ph/s,'d':draw/s,'a':pa/s,'raw_sum':round(s,4)})
        print(f'{key:<34} H {ph/s:.3f}  D {draw/s:.3f}  A {pa/s:.3f}  (vig {s:.3f})')
    except Exception as e:
        print('ERR',slug,repr(e)[:60])
json.dump(store,open('polymarket_matches.json','w'),indent=1)
print('stored snapshot',ts)
