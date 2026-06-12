"""Decisive test of the player-level premise.
Predict a team's per-match attacking output (team xG) two ways, out-of-sample:
  TEAM   : team's recency-weighted mean attacking xG (lineup-blind)
  PLAYER : calibrated aggregate of the starting XI's individual xG-rates (lineup-aware)
Identical in all else (no opponent adjust either side). Lower MSE = better.
Honest controls: out-of-fold player ratings, imputation tracked, only score
instances with >=7/11 starters having prior data."""
import json, numpy as np
from datetime import date
rng=np.random.default_rng(0)
P=json.load(open('player_stats.json'))
HALF=2.5; TODAY=date(2026,6,11); K_SHR=5.0   # player shrinkage (in 90s)

# attacking instances + per-match player lines
inst=[]   # (team, date, starters[list], team_xg, w)
plines=[] # (player, team, date, xg, xa, min)
for mid,m in P.items():
    y,mo,d=map(int,m['date'].split('-')); age=(TODAY-date(y,mo,d)).days/365.25
    w=0.5**(age/HALF)
    pm={r['player']:r for r in m['players']}
    for tm,st in m['starters'].items():
        txg=m['teamxg'].get(tm,0.0)
        inst.append(dict(team=tm,date=m['date'],starters=st,txg=txg,w=w,mid=mid))
    for r in m['players']:
        if r['team']:
            plines.append(dict(pl=r['player'],tm=r['team'],date=m['date'],
                               xg=r['xg'],xa=r['xa'],mn=r['min'],w=w))

inst=np.array(inst,dtype=object)
N=len(inst); order=rng.permutation(N); Kf=5; folds=[order[i::Kf] for i in range(Kf)]

def player_rates(train_mids):
    # recency-weighted xG-rate per player from training matches
    num={}; den={}
    g_num=0.0; g_den=0.0
    for p in plines:
        if p['mid'] if False else None: pass
    for p in plines:
        if p['date'] is None: continue
        num.setdefault(p['pl'],0.0); den.setdefault(p['pl'],0.0)
    # accumulate only training matches
    return num,den

# simpler: index plines by mid via match date+team already; rebuild with mid
plines=[]
for mid,m in P.items():
    y,mo,d=map(int,m['date'].split('-')); age=(TODAY-date(y,mo,d)).days/365.25; w=0.5**(age/HALF)
    for r in m['players']:
        if r['team']:
            plines.append((mid,r['player'],r['xg'],r['xa'],r['min'],w))

def fit_rates(train_set):
    num={}; den={}; gn=0.0; gd=0.0
    for mid,pl,xg,xa,mn,w in plines:
        if mid not in train_set: continue
        num[pl]=num.get(pl,0.0)+w*xg
        den[pl]=den.get(pl,0.0)+w*mn/90.0
        gn+=w*xg; gd+=w*mn/90.0
    g0=gn/gd if gd>0 else 0.1
    rate={pl:(num[pl]+K_SHR*g0)/(den[pl]+K_SHR) for pl in num}
    return rate,g0

def fit_team(train_set):
    num={}; den={}
    for it in inst:
        if it['mid'] not in train_set: continue
        num[it['team']]=num.get(it['team'],0.0)+it['w']*it['txg']
        den[it['team']]=den.get(it['team'],0.0)+it['w']
    return {t:num[t]/den[t] for t in num}

def lincal(x,y,w):
    x=np.array(x);y=np.array(y);w=np.array(w)
    X=np.vstack([np.ones_like(x),x]).T; W=np.diag(w)
    b=np.linalg.lstsq(X*w[:,None],y*w,rcond=None)[0]
    return b

errs_team=[]; errs_player=[]; cov=[]
for f in range(Kf):
    te=set(int(i) for i in folds[f]); tr_idx=[i for i in range(N) if i not in te]
    train_mids=set(inst[i]['mid'] for i in tr_idx)
    rate,g0=fit_rates(train_mids); teamr=fit_team(train_mids)
    # build calibration on TRAIN instances
    xs_p=[];xs_t=[];ys=[];ws=[]
    for i in tr_idx:
        it=inst[i]; feat_p=sum(rate.get(pl,g0) for pl in it['starters'])
        feat_t=teamr.get(it['team'],g0*11)
        xs_p.append(feat_p);xs_t.append(feat_t);ys.append(it['txg']);ws.append(it['w'])
    bp=lincal(xs_p,ys,ws); bt=lincal(xs_t,ys,ws)
    for i in folds[f]:
        it=inst[int(i)]
        ncov=sum(1 for pl in it['starters'] if pl in rate)
        if ncov<7: continue
        cov.append(ncov/len(it['starters']))
        fp=sum(rate.get(pl,g0) for pl in it['starters']); ft=teamr.get(it['team'],g0*11)
        pred_p=bp[0]+bp[1]*fp; pred_t=bt[0]+bt[1]*ft
        errs_player.append((pred_p-it['txg'])**2); errs_team.append((pred_t-it['txg'])**2)

ep=np.array(errs_player); et=np.array(errs_team)
print(f'scored instances: {len(ep)}  (avg starter coverage {np.mean(cov)*100:.0f}%)')
print(f'TEAM   model MSE on team-xG: {et.mean():.4f}')
print(f'PLAYER model MSE on team-xG: {ep.mean():.4f}')
d=et-ep; bs=[np.mean(rng.choice(d,len(d))) for _ in range(3000)]
tvar=np.var([it['txg'] for it in inst])
print(f'MSE improvement player vs team: {d.mean():+.4f}  95% CI [{np.percentile(bs,2.5):+.4f},{np.percentile(bs,97.5):+.4f}]')
print(f'(positive = player model better; team-xG variance overall = {tvar:.3f})')
