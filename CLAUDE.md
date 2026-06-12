# CLAUDE.md — Fable World Cup 2026 Score-Prediction Project

Context/handoff doc. Read this first if the conversation was cleared.

## What this project is
Predict scores of the 2026 FIFA World Cup (48 teams, 12 groups A–L; hosts USA/Mexico/Canada;
tournament opened 2026-06-11). Built a world-class group-stage **score** model through 6 validated
iterations. Now forked to serve a **points-prediction game**.

## ACTIVE TASK — points game (this is the live workflow)
User plays a prediction game: competes in a **large field of French recreational players**, accumulates points.
**Scoring (confirmed):** submit a scoreline per match → base reward if result correct (Rule A: wrong
score + right result still pays base), **plus a RARITY BONUS if the exact score hits**, tiered by the
share of correct-outcome pickers who chose that score:
`>30%:+20 | 20–30%:+30 | 5–20%:+50 | 0.5–5%:+70 | <0.5%:+100`.
**X2 boost: ONE per tournament, usable ANYTIME incl. knockouts** — doubles a chosen prediction's total
points (incl. rarity bonus) if the outcome is correct. Policy: HOLD through groups; bar = must beat the
expected best knockout opportunity (~E_total ≥ 45+, no dead-rubber/rotation flags, prefer contrarian).

**FIELD CONTEXT (2026-06-12):** >1M players; user ranked ~230,000th holding the SECOND-BEST POSSIBLE
score (165/185) ⇒ ~23% of field near-perfect after MD1 ⇒ **chalk cannot climb; rare-score bonuses are
the primary separating instrument.** Encoded as VAR_TIEBREAK rule in matchday.py: among scores within
1.5 EV of best AND ≥50% of its hit prob, prefer lowest-crowd (p-floor stops drift into the unvalidated
deep tail). User also 1st ex-aequo in a 4-person friends league; same picks serve both for now. User
updates rank as it evolves → adjust variance mode.
**POLYMARKET MATCH LAYER:** `fetch_pm_matches.py` pulls per-match 1X2 (slugs `fifwc-xxx-yyy-date`,
~0.5% vig, liquid) → timestamped `polymarket_matches.json`; re-run each matchday for movement.
matchday.py auto-runs a DUAL-EV robustness check: if market-p flips the pick → explicit decision needed
(market stays OUT of p — visible check, not blend). Known divergences (2026-06-12): **USA-Paraguay
v6 27/29/44 vs PM 47/30/24 (20pts! v6 has Paraguay favourite, every market says USA — robust flag WILL
fire)**; Ecuador now 39.7% on PM = 4th independent source vs v6's 55%; v6 also hot Canada (62v53), cold
Brazil (50v59)/Sweden (42v51)/NL (40v48). Match dates discovered: 6/12 Canada-Bosnia & USA-Paraguay;
6/13 Qatar-Suisse, Brazil-Morocco, Haiti-Scotland; 6/14 CIV-Ecuador, Sweden-Tunisia, Australia-Turkey,
NL-Japan. Winamax pct confirmed MATURE money (matches ≤48h away) → 0-0 longshot spikes are a stable
bettor trait, strengthening the two-population model.
**Winamax freshness gate:** WINAMAX_VALID_THROUGH in matchday.py (currently 2026-06-13 per user — early
money unreliable for later matches); every match needs date=; raise the constant when fresh CSVs arrive.
**Calibration stream source confirmed:** realized tiers come from ORGANIZER EMAILS (first-party; obs#2
Korea +20 confirmed sound). User CONFIRMED (2026-06-12): tiers accessible for ALL matches (uncensored),
and rules confirmed = share among correct-winner pickers, NO temporal condition. Ask user for the
realized tier of every played match.

**Per-match pick procedure → run `matchday.py` (edit its MATCHES list):**
-1. **`python preflight.py` (mandatory gate — must print GREEN).** Verifies deployed-engine
   integrity (SHA256 of attdef.json/wc_to_canon.json vs `deployed_params.json` manifest), file
   parses, 48-team resolution, obs dedup, engine smoke test. On artifact hash FAIL: restore with
   `copy frozen\<file> <file>` — the frozen/ dir holds canonical backups. NEVER re-run upstream
   pipeline scripts (model.py, fit_attack_defense.py, predict_v5.py...) mid-competition: they
   overwrite the deployed engine. `deployed_params.json` is the single source of truth for
   R/GAMMA/MAXG (matchday.py & register_bonus.py read it — not the regenerable output files).
0. **MODEL-BLIND SCAN (mandatory FIRST — see section below).**
1. Inputs from user (see checklist). Engine: v6 probs + overlays → outcome EV = p×reward.
2. Crowd model: plausibility (de-vigged bookie grid if supplied, else model probs) ^beta × salience,
   params from `crowd_params.json`. Band-robust tier (crowd ×0.7/1.0/1.43 scenarios; BOUNDARY flag).
3. **Outcome pick = argmax TOTAL EV (base + best bonus EV)**; warn if bonus flipped outcome vs base EV.
4. **Score pick = argmax robust bonus EV within the picked outcome** (NOT the naive modal score).
5. Append pick to `prediction.md`; after the match, log result in `live_updates.md`.

## REQUIRED FROM USER each matchday (ask if missing)
1. **Reward table** per match: `Home X / Draw Y / Away Z` — REQUIRED for EV picks.
2. **Winamax exact-score CSV update** (`scores_exacts_winamax.csv`, columns Match,Score,Cote,Pct_parieurs)
   → run `python winamax_ingest.py <date>` (timestamped store `winamax_snapshots.json`, history kept —
   user updates figures pre-match; early money is lumpy/longshot-biased, late money is the real signal).
   matchday.py AUTO-LOADS the latest snapshot as plausibility base.
3. **Realized bonus TIER of the actual score for EVERY played match** (visible in the game even for
   scores user didn't pick) → `register_bonus.py`. ~1 crowd observation per match = the calibration stream.
4. Leaderboard standing when relevant (variance mode).

## Crowd model status & architecture (the live workstream)
Two distinct populations, opposite biases — do NOT conflate:
- **Prono pickers** (the game): herd onto iconic scores (hard obs: 2-0 >30%, 2-1 >30%). Current model:
  crowd ∝ plausibility^beta × salience^sal_strength, params `crowd_params.json` (beta=1.6, s=1.5 after
  violation-refit on 2 obs; Korea cell still 1pt out — coarse-grid residual).
- **Winamax bettors**: longshot/value bias (0-0 spikes 45-59% in early money). Their pct is NOT a prono
  proxy. But **pct/odds ≈ French-public perceived probability** (decomposition validated on liquid
  matches: Canada gives 1-0 26%, 1-1 22%, 2-1 22% — iconic shape). Upgrade path when tier obs ≥5-6:
  test prono ∝ (pct/odds-perceived)^delta vs salience-only; adopt only if it fits tiers better.
- **v6 engine validated at score-cell level vs de-vigged Winamax**: corr 0.92-0.99, meanAD 0.5-1.7%/cell.
  Known deviations: model tail FATTER than market (Autre); model hotter on Ecuador/Uruguay favourite
  cells (0-1 19 vs 13); 0-0 mildly high. matchday.py prints a [DIVERGENCE] flag when the picked score's
  model/market ratio is >1.3 or <0.77 — treat as caution, prefer the alt score.
- **ARCHITECTURAL PRINCIPLE (locked after a caught error):** Winamax data enters the CROWD layer ONLY
  (plausibility for crowd shares). p(score) in EV stays PURE v6 — the validated truth model. Never blend
  market into p: (a) single-bookie score odds w/ 143-152% overround ≠ the liquid outcome markets where
  "market≥model" was earned; (b) blending breaks E[bonus]=p(truth)×tier(behavior) error-independence;
  (c) any change to the validated core requires OOS validation, which is impossible for the blend.
  Divergences become visible FLAGS, never silent math.

## SESSION LOG 2026-06-12 afternoon — challenges absorbed, slate submitted
**Epistemics correction (user-driven):** "market right, model wrong" is NOT the default. Per-divergence
CHANNEL DIAGNOSIS: artifact channel (e.g. Ecuador = inflated Elo × global γ amplification → model likely
wrong) vs data channel (e.g. USA = genuinely poor goals/xG, the signal class markets historically
underweight → contested). Also: v6 agreeing with market is partly mechanical (60% ancestry) → weak
validation; v6 DISagreeing despite ancestry → divergence concentrated in independent components → more
informative, diagnose channel. Retracted: "evidence favors market" on USA.
**External review (13 Qs) disposition:** Q1 rolling-origin validation RUN → γ survives (test-optimal
1.45–1.75 at all 4 origins, basin bottoms 1.6, γ=1.0 worst; train-argmax 1.75 overfits → vindication
of not deploying in-sample optimum). Q3 β transfers across bases within one tier; rare cells stable.
Q5 Σ(1/reward)≈1/30 ±10% → consistent with reward≈K/share (uncensored crowd obs if confirmed; need
bookie 1N2 alongside future pulls to discriminate). Q12 tie-break design defended (all downstream uses
actually-played score). Q2 overlay-amplification claim FALSE (overlays applied post-γ in lam_pair).
Scheduled: Q6 crude rank-EV sim (after MD1 slate), Q9 market ledger (running), Q10 stream double-count
check (next refit window), Q8 KO X2 model (MD3), Q13 split condition defined (late + mega-field hopeless
+ friends contested). Q4 = USER: tiers from organizer emails for ALL matches.
**Pipeline fixes:** tiers list order is [optimistic, mid, pessimistic] (crowd×0.7 = FEWER pickers =
HIGHER bonus); label corrected. VAR_TIEBREAK now requires pessimistic-EV(candidate) ≥ pessimistic-EV(top)
(was promoting into unvalidated deep tail; corrected Haiti 1-4→1-3).
**FLIP PROTOCOL (operational):** when PM flips the pick, decide by MAXIMIN across model-p and market-p
EVs (incl. bonus). Result on MD1: 4 contested flips → Draw was maximin-stable each time, paired with 0-0
(crowd-thin, tier 50 all scenarios, p 9–13%).
**EPISTEMIC STATUS of 0-0 edge (user-challenged, demoted):** iconic-score herding is MEASURED (2 obs);
0-0 under-picking is INFERRED (measured herding strength + literature salience prior; ZERO direct 0-0
obs; Winamax bettors over-pick it but excluded as different population). Cushion: tier-50 loss needs
true 0-0 share >20% (~2× estimate, wrong direction); cost one tier (~-2 EV). First direct test = any
draw tier this weekend.
**MD1 SLATE SUBMITTED (10 matches, see prediction.md):** Canada 3-0 / Draw 0-0 (USA-PAR) / Suisse 0-3 /
Draw 0-0 (BRA-MAR) / Scotland 1-3 / Germany 5-0 / Turkey 1-3 / Draw 0-0 (NED-JPN) / Ecuador 0-2 /
Draw 0-0 (SWE-TUN). X2 HELD (flagged candidates were single-source EV only). Pending: results, tiers
(esp. any draw → first 0-0/1-1 share measurement), rank movement.

## Model-blind scan (MANDATORY each run)
v6 is fit on historical data and is BLIND to injuries, suspensions, lineups, and post-cutoff results.
Before every pick, for BOTH teams in the match:
1. Read `live_updates.md` (running record of results, suspensions, injuries, overlays, pick log).
2. Fresh `WebSearch` for: "<team> injury / suspension / lineup news June 2026", and any results since
   `Last scanned`. Update `live_updates.md` (+ bump its `Last scanned` date).
3. Apply conservative ATT/DEF overlays from `live_updates.md` to the affected team before computing the pick
   (key attacker out → −0.10/−0.15 ATT; key defender/keeper → reduce DEF 0.08–0.12; **halve if the reward
   table / market already moved**; rotation players → ignore). These are JUDGMENT overlays, NOT a refit
   (the player-leg failed validation — see below).
4. **Flag illusory value:** if the model shows an edge on an injury-hit team, it may just be model-blindness —
   discount it, say so in the pick.
Do NOT refit the model on trickling results (2-game samples = noise; overfitting risk).

Field strategy: edge (calibration) compounds you up the table; the exact-score double is the
separator. Variance is dynamic — mid/level = EV-max; **trailing late = take +edge variance**
(underdogs/draws/longer scores); **leading late = play safe**. Ask user's standing when tight.

## DEPLOYED MODEL = v6 (frozen)
Pipeline: **2-D attack/defence ratings (goals + xG) → negative-binomial scoreline → supremacy
recalibration γ=1.5.** For a neutral match between home `th`, away `ta`:
```
lh = exp(mu_goals + ATT[th] - DEF[ta]);  la = exp(mu_goals + ATT[ta] - DEF[th])
M=(ln lh+ln la)/2; D=(ln lh-ln la)/2;  lh,la = exp(M ± 1.5*D)   # gamma=1.5 recalibration
score ~ independent NegBinom(mean=lh/la, dispersion r=9.5)       # no Dixon-Coles (rho~0 for intl)
```
- Ratings: `attdef.json` (ATT/DEF per team; `_meta` has mu_goals≈0.20, h_g, etc.). r=9.5 in `qualification_v5.json`.
- Reference impl: `predict_v6.py` (→ `PREDICTIONS_v6.md`), `forkbet.py` (points picks).
- Host home advantage is **deliberately NOT applied** (tested in v7, it overshot — see below).

## Files / build order
- `sources_urls.md` — data sources (openfootball, statsbomb, soccerdata, fbref, polymarket).
- `build_data.py` → `wc_data.json` (Elo from eloratings.net `World.tsv`; groups A–L).
- `fetch_market.py` → `market.json` (Polymarket group-winner odds).
- `model.py` → `ratings.json` (Elo × market blended prior; used as strength anchor).
- `sb_fetch.py` → `sb_xg.json` (StatsBomb team xG, 314 matches).
- `fetch_results.py` → `goals_records.json` (martj42 intl results, 4568 matches since 2022, all 48 teams).
- `fit_attack_defense.py` → `attdef.json` (THE core model: pooled att/def on goals+xG, strength anchored to prior).
- `predict_v6.py` → deployed predictions. `forkbet.py` + `prediction.md` → points-game deliverable.

## Version ladder — validated vs REJECTED (do NOT redo dead ends)
Each shipped change beat its predecessor out-of-sample (5-fold; exact-score log-loss):
- v1 Elo×market → v2 +xG leg (thin, kept ≤0.26 weight) → v3 uncertainty bands → **v4 2-D att/def (+0.0267, big)**
  → **v5 NegBinom, dropped Dixon-Coles ρ (+0.0147)** → **v6 supremacy recalibration γ=1.5 (+0.0324, biggest)**.
- **REJECTED with evidence:** player-level model (`player_backtest.py`, MSE worse, CI crosses 0);
  generic host advantage (`predict_v7.py`, overshoots Mexico/Canada, worsens market fit); altitude/heat/travel
  (thin, market-captured; note South Africa is itself an altitude side); lambda-dependent NB dispersion
  (`backtest_disp.py` — tested as fix for the market-flagged fat tail: OOS logloss WORSE, -0.0024 CI[-0.0041,
  -0.0007], blowouts -0.039 — tail overfit; global r stays. Tail divergence vs Winamax remains a FLAG only).
- Ecuador outcome-level overrating: confirmed by 3 independent market sources (Elo-vs-Polymarket offset,
  group odds, Winamax grid: model 55% vs 40% away-win mass at CIV-Ecuador). Cell-level "hot" flags on 0-1
  were de-vig FLB artifact (within-region ratio 1.16). Treat CIV-Ecuador & similar with extra caution +
  thorough model-blind scan; do NOT silently adjust ratings.
- **Core lesson:** model STRUCTURE ≫ data SOURCE; market ≫ model for relative strength.
- Diagnostic backtests live in: `backtest_2d.py`, `score_struct_backtest.py`, `calib.py`, `recalibrate.py`.

## Known facts / flags
- Base model was UNDER-confident (favourites win more than predicted); γ=1.5 fixes it (calibrated 87%→88%).
- **USA = flagged model-vs-market disagreement** (model ~12–19% group win, market 37%). Likely Polymarket
  US-retail patriotic bias inflating the market. DON'T "fix" it by inflating USA.
- Most score variance is irreducible (predicted-total std ~0.5 vs actual ~1.8). Model gives frequencies,
  never the specific upset.

## Technical gotchas
- **Windows console can't print Unicode** (en-dash, emoji, accents) → write reports to UTF-8 files; don't print them.
- `scipy.stats.poisson.ppf` is ~1.5s/call → use `searchsorted(poisson.cdf(grid,λ), U)` instead (150× faster).
- Nelder-Mead from a zero start needs an explicit `initial_simplex` (~80-pt steps) or it won't move.
- f-strings: no backslash escapes inside `{}` — extract the value to a variable first.
- Env: Python 3.14, numpy/pandas/scipy/statsmodels present; **no sklearn/soccerdata**. eloratings codes ≠ ISO
  (Scotland=SQ, England=EN). StatsBomb/martj42 name aliases handled in the fetch scripts.

## How the user works (match this)
- World-class rigor: **validate, don't assert.** Backtest before shipping; report honestly including
  negative results and "don't ship it." Each change must beat its predecessor out-of-sample.
- **Don't over-engineer, don't try to please, flag model risk and biases.** The user actively rewards
  being told an idea doesn't work. Stay sharp and self-critical.
