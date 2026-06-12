"""Pull StatsBomb open event data -> per-match team xG (shots only, shootouts excluded).
Restartable: caches compact results to sb_xg.json keyed by match_id."""
import requests, json, os, time
from concurrent.futures import ThreadPoolExecutor, as_completed

B='https://raw.githubusercontent.com/statsbomb/open-data/master/data/'
H={'User-Agent':'Mozilla/5.0'}
matches={m['mid']:m for m in json.load(open('sb_matches.json'))}
CACHE='sb_xg.json'
done=json.load(open(CACHE)) if os.path.exists(CACHE) else {}
done={int(k):v for k,v in done.items()}

def extract(mid):
    for attempt in range(3):
        try:
            r=requests.get(f'{B}events/{mid}.json',headers=H,timeout=40)
            ev=r.json()
            break
        except Exception:
            if attempt==2: raise
            time.sleep(1.5)
    xg={}; sh={}
    for e in ev:
        if e.get('type',{}).get('name')!='Shot': continue
        if e.get('period')==5: continue            # exclude penalty shootout
        tm=e['team']['name']
        x=e.get('shot',{}).get('statsbomb_xg',0.0) or 0.0
        xg[tm]=xg.get(tm,0.0)+x
        sh[tm]=sh.get(tm,0)+1
    m=matches[mid]
    return mid, dict(home=m['home'],away=m['away'],comp=m['comp'],season=m['season'],
                     date=m['date'],hg=m['hg'],ag=m['ag'],
                     hxg=round(xg.get(m['home'],0.0),3),axg=round(xg.get(m['away'],0.0),3),
                     hsh=sh.get(m['home'],0),ash=sh.get(m['away'],0))

todo=[mid for mid in matches if mid not in done]
print('cached',len(done),'todo',len(todo))
t0=time.time(); n=0
with ThreadPoolExecutor(max_workers=12) as ex:
    futs={ex.submit(extract,mid):mid for mid in todo}
    for f in as_completed(futs):
        try:
            mid,res=f.result(); done[mid]=res; n+=1
        except Exception as e:
            print('FAIL',futs[f],e)
        if n%25==0:
            json.dump(done,open(CACHE,'w'))
            print(f'{n}/{len(todo)} {round(time.time()-t0)}s')
json.dump(done,open(CACHE,'w'))
print('DONE total cached',len(done),'in',round(time.time()-t0),'s')
