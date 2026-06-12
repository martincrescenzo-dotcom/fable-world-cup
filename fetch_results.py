"""Build recent international GOALS records from martj42 dataset.
Recency-decayed + match-importance weighted. Canonical names = martj42.
Output goals_records.json and report 48-team coverage + name maps."""
import csv, io, json
from datetime import date

rows=list(csv.DictReader(open('intl_results.csv',encoding='utf-8')))
TODAY=date(2026,6,11); HALF=2.5
def imp(t):
    t=t.lower()
    if 'friendly' in t: return 0.6
    if any(k in t for k in ['world cup','euro','copa am','cup of nations','nations cup']) and 'qualif' not in t: return 1.2
    return 1.0

recs=[]
for r in rows:
    if r['date']<'2022-01-01': continue
    if r['home_score'] in ('NA','') or r['away_score'] in ('NA',''): continue
    try: hs,as_=int(r['home_score']),int(r['away_score'])
    except ValueError: continue
    y,mo,d=map(int,r['date'].split('-'))
    age=(TODAY-date(y,mo,d)).days/365.25
    if age<0: continue
    w=0.5**(age/HALF)*imp(r['tournament'])
    recs.append(dict(h=r['home_team'],a=r['away_team'],hg=hs,ag=as_,
                     neutral=(r['neutral'].upper()=='TRUE'),w=round(w,4)))
json.dump(recs,open('goals_records.json','w'))

# ---- WC48 + SB alias resolution to martj42 canonical ----
WC=json.load(open('wc_data.json'))
wc48=[t['team'] for g in WC for t in WC[g]]
allnames=set(x['h'] for x in recs)|set(x['a'] for x in recs)
wc_alias={'Czech Republic':'Czechia','Turkey':'Turkey','Curacao':'Curaçao','DR Congo':'DR Congo',
          'Ivory Coast':'Ivory Coast','Cape Verde':'Cape Verde','South Korea':'South Korea','United States':'United States'}
def canon_wc(t):
    if t in allnames: return t
    if t in wc_alias and wc_alias[t] in allnames: return wc_alias[t]
    return None
miss=[t for t in wc48 if canon_wc(t) is None]
import collections
cnt=collections.Counter()
for x in recs: cnt[x['h']]+=1; cnt[x['a']]+=1
print('records:',len(recs))
print('WC48 unmatched to martj42:',miss)
print('WC48 recent-match counts:')
for t in wc48:
    c=canon_wc(t); print(f'  {t:<24} -> {str(c):<18} {cnt.get(c,0)}')
json.dump({t:canon_wc(t) for t in wc48},open('wc_to_canon.json','w'))
