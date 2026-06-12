"""Re-fetch recent-tournament StatsBomb events; extract per-player attacking output
(xG + expected-assists) and minutes, plus each match's starting XI per team.
Scope: WC2022, Euro2024, AFCON2023, Copa2024. Restartable cache."""
import requests, json, os, time
from concurrent.futures import ThreadPoolExecutor, as_completed
B='https://raw.githubusercontent.com/statsbomb/open-data/master/data/'
H={'User-Agent':'Mozilla/5.0'}
RECENT={('FIFA World Cup','2022'),('UEFA Euro','2024'),
        ('African Cup of Nations','2023'),('Copa America','2024')}
matches={m['mid']:m for m in json.load(open('sb_matches.json'))
         if (m['comp'],m['season']) in RECENT}
print('recent matches:',len(matches))
CACHE='player_stats.json'
done=json.load(open(CACHE)) if os.path.exists(CACHE) else {}

def parse(mid):
    for at in range(3):
        try: ev=requests.get(f'{B}events/{mid}.json',headers=H,timeout=40).json(); break
        except Exception:
            if at==2: raise
            time.sleep(1.5)
    m=matches[mid]
    # match duration from max period
    maxp=max((e.get('period',1) for e in ev), default=2)
    D=120 if maxp>=3 else 90
    pass_player={}     # pass id -> passer name
    starters={}        # team -> [names]
    team_of={}         # player -> team
    minutes={}         # player -> minutes
    xg={}; xa={}; teamxg={}
    # first pass: lineups + pass map
    for e in ev:
        tn=e.get('type',{}).get('name')
        if tn=='Starting XI':
            tm=e['team']['name']; lst=[p['player']['name'] for p in e.get('tactics',{}).get('lineup',[])]
            starters[tm]=lst
            for nm in lst: team_of[nm]=tm; minutes[nm]=D
        elif tn=='Pass':
            pass_player[e['id']]=e.get('player',{}).get('name')
    # subs
    for e in ev:
        if e.get('type',{}).get('name')=='Substitution':
            mnt=e.get('minute',0)+e.get('second',0)/60.0
            off=e.get('player',{}).get('name'); on=e.get('substitution',{}).get('replacement',{}).get('name')
            tm=e['team']['name']
            if off: minutes[off]=min(minutes.get(off,D),mnt)
            if on: minutes[on]=D-mnt; team_of[on]=tm
    # shots -> xg to shooter, xa to key-passer
    for e in ev:
        if e.get('type',{}).get('name')!='Shot' or e.get('period')==5: continue
        sh=e.get('shot',{}); x=sh.get('statsbomb_xg',0.0) or 0.0
        shooter=e.get('player',{}).get('name'); tm=e['team']['name']
        xg[shooter]=xg.get(shooter,0.0)+x; teamxg[tm]=teamxg.get(tm,0.0)+x
        kp=sh.get('key_pass_id')
        if kp and kp in pass_player and pass_player[kp]:
            ap=pass_player[kp]; xa[ap]=xa.get(ap,0.0)+x
    recs=[]
    allp=set(minutes)|set(xg)|set(xa)
    for nm in allp:
        recs.append(dict(team=team_of.get(nm,''),player=nm,min=round(minutes.get(nm,0),1),
                         xg=round(xg.get(nm,0.0),3),xa=round(xa.get(nm,0.0),3)))
    return mid,dict(date=m['date'],comp=m['comp'],home=m['home'],away=m['away'],
                    teamxg={k:round(v,3) for k,v in teamxg.items()},
                    starters=starters,players=recs)

todo=[mid for mid in matches if str(mid) not in done]
print('todo',len(todo))
t0=time.time(); n=0
with ThreadPoolExecutor(max_workers=12) as ex:
    futs={ex.submit(parse,mid):mid for mid in todo}
    for f in as_completed(futs):
        try: mid,res=f.result(); done[str(mid)]=res; n+=1
        except Exception as e: print('FAIL',futs[f],e)
        if n%25==0: json.dump(done,open(CACHE,'w')); print(n,'/',len(todo),round(time.time()-t0),'s')
json.dump(done,open(CACHE,'w'))
print('DONE',len(done),'matches in',round(time.time()-t0),'s')
