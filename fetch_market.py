import requests, json

h = {'User-Agent': 'Mozilla/5.0'}
letters = ['a','b','c','d','e','f','g','h','i','j']
# Note: sources list groups a..j; groups k,l winner markets may use different slugs
extra = ['k','l']
market = {}

def fetch(slug):
    url = 'https://gamma-api.polymarket.com/events?slug=' + slug
    r = requests.get(url, headers=h, timeout=20)
    if r.status_code != 200:
        return None
    d = r.json()
    if not d:
        return None
    return d[0]

for L in letters + extra:
    slug = f'world-cup-group-{L}-winner'
    e = fetch(slug)
    if not e:
        market[L.upper()] = None
        continue
    rows = {}
    for m in e.get('markets', []):
        name = m.get('groupItemTitle') or m.get('question')
        prices = m.get('outcomePrices')
        outs = m.get('outcomes')
        try:
            prices = json.loads(prices) if isinstance(prices, str) else prices
            outs = json.loads(outs) if isinstance(outs, str) else outs
        except Exception:
            continue
        # find Yes price
        yes = None
        if outs and prices:
            for o, p in zip(outs, prices):
                if str(o).lower() == 'yes':
                    yes = float(p)
        if yes is not None:
            rows[name] = yes
    market[L.upper()] = {'volume': e.get('volume'), 'prices': rows}

json.dump(market, open('market.json', 'w'), indent=2)

rep = []
for g in sorted(market):
    rep.append(f'Group {g}:')
    v = market[g]
    if not v:
        rep.append('  (no market found)')
        continue
    pr = v['prices']
    s = sum(pr.values()) or 1
    for name, p in sorted(pr.items(), key=lambda x: -x[1]):
        rep.append(f'  {name:<26} raw={p:.3f}  norm={p/s:.3f}')
open('market_report.txt', 'w', encoding='utf-8').write('\n'.join(rep))
print('done; groups with market:', [g for g in market if market[g]])
