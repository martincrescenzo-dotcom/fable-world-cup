"""Ingest Winamax exact-score CSV snapshots -> timestamped store (winamax_snapshots.json).
Keeps history (user sends updated figures pre-match; early vs late money differs).
CSV format: Match,Score,Cote,Pct_parieurs ('Autre' = bookie bucket for unlisted scores)."""
import csv, json, os, sys
from collections import defaultdict
from datetime import date

SRC='scores_exacts_winamax.csv'      # override: python winamax_ingest.py <snap_date> [<csv_path>]
SNAP_DATE=str(date.today())
if len(sys.argv)>1: SNAP_DATE=sys.argv[1]
if len(sys.argv)>2: SRC=sys.argv[2]

FR2EN={'Canada':'Canada','Bosnie-Herzegovine':'Bosnia and Herzegovina','Australie':'Australia',
 'Turquie':'Turkey','Allemagne':'Germany','Curacao':'Curacao','Pays-Bas':'Netherlands','Japon':'Japan',
 "Cote d'Ivoire":'Ivory Coast','Equateur':'Ecuador','Suede':'Sweden','Tunisie':'Tunisia',
 'Espagne':'Spain','Cap-Vert':'Cape Verde','Belgique':'Belgium','Egypte':'Egypt',
 'Arabie Saoudite':'Saudi Arabia','Uruguay':'Uruguay','Mexique':'Mexico','Coree du Sud':'South Korea',
 'Tchequie':'Czech Republic','Qatar':'Qatar','Suisse':'Switzerland','Bresil':'Brazil','Maroc':'Morocco',
 'Haiti':'Haiti','Ecosse':'Scotland','Etats-Unis':'United States','Paraguay':'Paraguay','France':'France',
 'Senegal':'Senegal','Irak':'Iraq','Norvege':'Norway','Argentine':'Argentina','Algerie':'Algeria',
 'Autriche':'Austria','Jordanie':'Jordan','Portugal':'Portugal','RD Congo':'DR Congo',
 'Ouzbekistan':'Uzbekistan','Colombie':'Colombia','Angleterre':'England','Croatie':'Croatia',
 'Ghana':'Ghana','Panama':'Panama','Afrique du Sud':'South Africa','Nouvelle-Zelande':'New Zealand',
 'Iran':'Iran','Egypte ':'Egypt'}

def en(team):
    t=team.strip()
    if t in FR2EN: return FR2EN[t]
    raise KeyError(f'unmapped French team name: {t!r} — add to FR2EN')

rows=list(csv.DictReader(open(SRC,encoding='utf-8-sig')))   # -sig: strip Excel BOM (else the Match column dies silently)
m=defaultdict(list)
for r in rows:
    if not r.get('Match'): continue
    m[r['Match']].append(r)
if rows and not m:
    raise SystemExit(f'{SRC}: parsed {len(rows)} rows but found NO "Match" column — header mismatch, nothing ingested')

store=json.load(open('winamax_snapshots.json')) if os.path.exists('winamax_snapshots.json') else {}
n=0
for fr_match,lines in m.items():
    h,a=[x.strip() for x in fr_match.split(' vs ')]
    key=f'{en(h)}|{en(a)}'
    entry={'snap_date':SNAP_DATE,'odds':{},'pct':{}}
    for r in lines:
        sc=r['Score'].strip()
        cote=r.get('Cote') or r.get('Cote_Winamax')   # accept either column header variant
        odds=float(str(cote).replace(',','.'))
        pct=float(str(r['Pct_parieurs']).replace(',','.')) if r['Pct_parieurs'] not in ('',None) else 0.0
        entry['odds'][sc]=odds; entry['pct'][sc]=pct
    prev=store.get(key,[])
    if prev and prev[-1]['odds']==entry['odds'] and prev[-1]['pct']==entry['pct']:
        continue   # identical re-ingest (dup protection — a 2026-06-12 CSV was double-ingested as '-v2')
    if prev and entry['snap_date']<prev[-1]['snap_date']:
        print(f'  !! {key}: snapshot {SNAP_DATE} is OLDER than stored {prev[-1]["snap_date"]} — consumers take [-1]; NOT appending')
        continue
    store.setdefault(key,[]).append(entry)
    n+=1
json.dump(store,open('winamax_snapshots.json','w'),indent=1)
print(f'ingested {n} matches as snapshot {SNAP_DATE}; store now has {len(store)} match keys')
for k in store: print(' ',k,f"({len(store[k])} snapshot(s))")
