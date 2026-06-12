"""Unified 2-D attack/defence rating model (the keystone for SCORE prediction).
Two observation streams of the same latent ATT_i, DEF_i:
  GOALS (martj42, all 48 teams, recency+importance weighted, home effect fit)
  xG    (StatsBomb, ~38 teams, lower-variance precision signal)
Overall strength (ATT+DEF) anchored to the market-calibrated v1 prior;
the att/def SPLIT and TOTAL-GOALS level are learned from data.
Output: attdef.json"""
import json, numpy as np
from datetime import date
from scipy.optimize import minimize

goals=json.load(open('goals_records.json'))
sbxg=json.load(open('sb_xg.json'))
RAT=json.load(open('ratings.json'))
WC2CANON=json.load(open('wc_to_canon.json'))
HALF=2.5; TODAY=date(2026,6,11); B=0.70
RHO_STR=30.0    # strength anchor to prior (keep overall strength near market-calibrated value)
RHO_AD=8.0      # ridge on att/def level+split
XG_W=1.3        # per-obs weight for cleaner xG stream

# SB name -> canonical(martj42)
SB2C={"Côte d'Ivoire":'Ivory Coast','Congo DR':'DR Congo','Cape Verde Islands':'Cape Verde',
      'China PR':'China PR','Korea Republic':'South Korea','IR Iran':'Iran','Czech Republic':'Czech Republic'}
def sbc(n): return SB2C.get(n,n)

# ---- assemble observations: (scorer_idx, conceder_idx, y, home, weight, stream) ----
teams=set()
for r in goals: teams.add(r['h']); teams.add(r['a'])
for m in sbxg.values(): teams.add(sbc(m['home'])); teams.add(sbc(m['away']))
teams=sorted(teams); idx={t:i for i,t in enumerate(teams)}; T=len(teams)

sc=[]; cc=[]; Y=[]; HM=[]; WT=[]; ST=[]   # ST: 0=goals,1=xg
for r in goals:
    h,a=idx[r['h']],idx[r['a']]; hf=0.0 if r['neutral'] else 1.0
    sc+= [h,a]; cc+= [a,h]; Y+= [r['hg'],r['ag']]; HM+= [hf,0.0]; WT+= [r['w'],r['w']]; ST+= [0,0]
for m in sbxg.values():
    y,mo,d=map(int,m['date'].split('-')); age=(TODAY-date(y,mo,d)).days/365.25
    w=0.5**(age/HALF)*XG_W
    h,a=idx[sbc(m['home'])],idx[sbc(m['away'])]
    sc+= [h,a]; cc+= [a,h]; Y+= [max(m['hxg'],1e-3),max(m['axg'],1e-3)]; HM+= [0.0,0.0]; WT+= [w,w]; ST+= [1,1]
sc=np.array(sc); cc=np.array(cc); Y=np.array(Y,float); HM=np.array(HM); WT=np.array(WT); ST=np.array(ST)

# ---- strength anchor s_prior for the 48 (in log-goal units) ----
prior48={};
for g in RAT:
    for i,t in enumerate(RAT[g]['teams']):
        prior48[WC2CANON[t]]=RAT[g]['blend'][i]
pm=np.mean(list(prior48.values())); Bc=B/200.0
s_prior=np.zeros(T); has_prior=np.zeros(T)
for t,p in prior48.items():
    s_prior[idx[t]]=Bc*(p-pm); has_prior[idx[t]]=1.0

# params: [mu_goals, mu_xg, h_g, ATT(T), DEF(T)]
def unpack(p): return p[0],p[1],p[2],p[3:3+T],p[3+T:]
def nll(p):
    mug,mux,hg,att,dff=unpack(p)
    mu=np.where(ST==0,mug,mux)
    eta=mu+att[sc]-dff[cc]+hg*HM
    lam=np.exp(np.clip(eta,-4,4))
    S=att+dff
    val=(np.sum(WT*(lam-Y*np.log(lam)))
         + RHO_STR*np.sum(has_prior*(S-s_prior)**2)
         + RHO_AD*(att@att+dff@dff))
    r=WT*(lam-Y)
    g=np.zeros_like(p)
    g[0]=np.sum(r*(ST==0)); g[1]=np.sum(r*(ST==1)); g[2]=np.sum(r*HM)
    np.add.at(g,3+sc,r);            # dATT from scoring
    np.add.at(g,3+T+cc,-r)          # dDEF from conceding (enters as -DEF)
    dS=2*RHO_STR*has_prior*(S-s_prior)
    g[3:3+T]+= dS + 2*RHO_AD*att
    g[3+T:] += dS + 2*RHO_AD*dff
    return val,g

p0=np.zeros(3+2*T); p0[0]=np.log(1.35); p0[1]=np.log(1.25)
res=minimize(nll,p0,jac=True,method='L-BFGS-B',options=dict(maxiter=800))
mug,mux,hg,att,dff=unpack(res.x)
print('converged',res.success,'nit',res.nit)
print(f'mu_goals={mug:.3f} (={np.exp(mug):.2f} g) mu_xg={mux:.3f} home_adv h_g={hg:.3f} (={np.exp(hg):.2f}x goals)')

out={'_meta':dict(mu_goals=float(mug),mu_xg=float(mux),h_g=float(hg),
                  rho_str=RHO_STR,rho_ad=RHO_AD)}
for t in teams:
    i=idx[t]; out[t]=dict(ATT=float(att[i]),DEF=float(dff[i]))
json.dump(out,open('attdef.json','w'),indent=2)

# ---- demonstrate the new capability for the 48 ----
# expected goals FOR and AGAINST vs an average team (att=def=0)
print('\n  team                     ATT   DEF   lam_for lam_ag  total(vs avg)')
recs=[]
for t in [WC2CANON[x['team']] for g in json.load(open('wc_data.json')).values() for x in g]:
    i=idx[t]; lf=np.exp(mug+att[i]-0); la=np.exp(mug+0-dff[i]); recs.append((lf+la,t,att[i],dff[i],lf,la))
for tot,t,a,d,lf,la in sorted(recs,reverse=True):
    print(f'  {t:<22} {a:+.2f} {d:+.2f}   {lf:.2f}   {la:.2f}    {tot:.2f}')
