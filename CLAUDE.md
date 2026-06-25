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
points (incl. rarity bonus) if the outcome is correct. **X2 is FREE optionality (costs nothing if the pick
loses) → the only decision is TIMING/target.** Policy (AUDIT 2026-06-16, flipped): deploy on the best
**high-reward (≥~100) + FIELD-UNDERPICKED + MARKET-CONFIRMED** outcome whenever it appears, group OR KO —
do NOT hold indefinitely for KO. Evidence: leader Alexandre X2'd the NL-Japan DRAW (reward 115, field-thin)
→ +115, a big slice of his lead; Nicolas & Bertrand BOTH WASTED X2 on Germany-Curaçao (reward 15 lock) →
+15. Never X2 a low-reward favourite lock. "Model+market AGREE" is NOT the criterion (agreement = field also
on it = correlated = zero rank separation); the criterion is **field misses it but it's still +EV**.

**OBJECTIVE UPDATED 2026-06-18 → TOP-5 of ~16 (league grew from 13 to 16 & settled; new players joined), BALANCED.**
**STANDING 2026-06-25: USER #8 (Lampadaire83) @1857 (27 bons / 4 EXACTS), climbed #9→#8 (+255 on follows; Canada decorrelation LOST,
Switzerland 2-1). #8 ATOP A BUNCH WITH A CUSHION BELOW — #7 +11, #6 +53 ABOVE; #9 −81, #10 −147 BELOW; top-5 line #5 AdyFC 2090, gap 233.
★ THIS INVERTS THE VARIANCE LOGIC: defending a bunched position from below ≠ chasing a bloc from below → high-variance decorrelation is now
RANK-DESTRUCTIVE (a miss cedes the head-to-head to chalk-following #6/#7 AND lets #9 close). Rank lever = bank chalk + hit EXACTS (user 4 vs
#2 Hadri 11). MD10 = full FOLLOW slate; the "take Ecuador (high-reward 145 + field-thin 3% + edge 1.23)" decorrelation was FALSIFIED by a
3-agent red-team (EV-positive but RANK-negative; same 2/13-losing profile; the project's worst artifact team) → followed Germany instead.
See REVIEW_2026-06-25_ecuador-decorrelation.md. [Earlier 2026-06-24: #9 @1602; #7/#8/#9 bunched within 11; top-5 line #5 AdyFC 1785, gap 183.]** MD9 partial: +127 ALL from a Colombia 1-0 EXACT on a straight FOLLOW (exacts-are-the-separator, delivered);
England 0-0 upset + Panama-Croatia draw lost (the lower-conviction decorrelation, flagged ex-ante). 2 MD9 picks PENDING (Canada 0-1
decorrelation, Bosnia 1-0 follow). #2 Hadri has 11 exacts — exacts are the league's separating currency. [Earlier 2026-06-23: #9 @1475, 3 exacts.] DROPPED #8→#9 despite +152 (Arg 63 + France 22 + Algeria 67; 3/4 follows all chalk) — **the Senegal X2 LOST
(Norway won 3-2, the ~70% branch; process sound, outcome unlucky — NOT a strategy error). X2 ONE-SHOT NOW SPENT, no boost remaining.**
The rank drop while +152 is the doctrine's core tension: following chalk = points-not-rank; the structural deficit is EXACTS (user 3 vs
climbers 7-9). [Earlier: #8 @1323 after the +386 weekend incl. the Belgium-Iran reward-mispricing DRAW +138.]
**★★ CORRECTED DOCTRINE 2026-06-24 (after a 3-agent adversarial review FALSIFIED my own intra-session "follow-for-bons") ★★**
See REVIEW_2026-06-24_decorrelation-and-followforbons.md. I drifted across 3 wrong framings in one session; the red-team (statistician +
strategist + data-integrity, each recomputing) caught it. **All my NUMBERS were correct (data-integrity ALL PASS); the INFERENCES were wrong:**
 1. **"No score-skill gap" — RETRACTED (was an underpowered null + apples-to-oranges).** I compared the model's UNCONDITIONAL modal-cell mass
    (13.4%) to our CONDITIONAL exact rate (4/23=17.4%); the correct conditional benchmark is P(modal | correct outcome) = **23.6%**, against which
    we are ~6pts BELOW, not "at ceiling." Power to detect the leader gap ≈ 38% (need ~70/player); difference-CI vs Hadri = **[−3%, +44%]**. HONEST
    STATEMENT: can't tell — keep logging, revisit at ~70 obs. (Score-CELL modal rule itself stays validated; the fight is at the OUTCOME layer.)
 2. **"Follow-for-bons" — WRONG MAXIMAND.** The game scores reward-weighted POINTS; rank=argsort(points), NOT bons (France bon=22 ≠ draw bon=138).
    The top of the league separates on reward-weighting + exacts, not bon-count (CrazyBE 27 bons/3 ex ≈ AdyFC 25/8 in points). "Highest-probability"
    ≠ "highest-EV" on a compressed line (Senegal EV 41.5 > Norway 27.8). The 138-vs-364 deviation result is a CHALK-SAMPLE artifact (favs won 7/8;
    the real fav-conversion is ~55–65% given the draw-upset flood: England 0-0, Ecuador, Spain, Uruguay).
 3. **For a trailing/bunched #9 with the X2 SPENT, follow-everything = minimum relative variance = LOCKS 9th.** P(overtake a field ahead) rises with
    your variance-relative-to-field at non-negative EV. Selective decorrelation is the ONLY remaining rank lever.
**CORRECTED DEFAULT (restores, with a harder gate, the doctrine I wrongly abandoned):**
 • OUTCOME = argmax **blend-EV** (0.4 model + 0.6 market) — NOT highest-probability.
 • **Selective decorrelation = the rank lever, HARD-GATED:** take the field-underpicked outcome only when it is blend-EV-max (or within the ~5% band),
   edge=market_p/reward-implied_p **>1**, market-confirmed, field clearly underpicks it. ≤1–2/slate. It is EV-NEUTRAL VARIANCE (losses are variance,
   not an EV leak, IF the gate holds) — exactly what a trailer needs. The marginal misses (Croatia-draw, Senegal) ⇒ RAISE the gate, don't abandon.
 • SCORE = modal within the chosen outcome (UNCHANGED, validated).
 • Maximand = RANK via reward-weighted POINTS. **Bons = a SECONDARY calibration diagnostic, NEVER the target.**
**STANDING RULE before any future doctrine change: (a) power/CI check (is the null underpowered?), (b) maximand check (optimizing rank/points or a
proxy?).** This is the 2nd time an inference outran its sample here (1st: league_sim2). See [[two-axis-differentiation]], [[score-layer-is-a-sideshow]].
Climbers still carry the exact-score edge (#2/#5 = 8 exacts vs user 3). [Earlier: User #14/16 @550.] Supersedes the "top-2 of 13" frame below. STRATEGY = EV-max FOLLOW + mechanical MODAL scores
(base) + SELECTIVE variance on ONLY the highest-conviction field-underpicked + market-confirmed Axis-B spots (raise
the bar — recent marginal/artifact ones went 0/3); NO full-variance ramp, NO rare-score gamble; X2 on a good
field-underpicked spot for a rank bump. future_sim.py INVALID (fixed-13 assumption). Following GAINS points but
LOSES rank (#10→#14 while +176 pts) — climbers use contrarian outcomes + exacts (user 1 exact vs climbers 2-4).
Reachability: top-5 line 703, gap 153, mid-table bunched (143 over 9) → realistic with 1-2 selective calls. See
live_updates.md snapshot. [HISTORICAL below — top-2/13 frame, superseded:]
**TRUE OBJECTIVE: TOP-2 of the 13-person friends league, ~88 matches remaining.** Standings 2026-06-16:
1113 / **658(#2 LINE)** / 609 / 557 / 436 / 419 / 411 / 405 / 389 / **[USER 374, #10]** / 350? / 320? / 290?.
#1 (Alexandre, legit 11/16) is a runaway → race is for the **2nd slot = catch Nicolas (658), gap 284**.
**STRATEGY VERDICT — CORRECTED 2026-06-16 (supersedes the DIFF_BAND=0 "differentiation hurts" finding).**
league_sim2 (which set DIFF_BAND=0) was BROKEN twice: (a) STALE standings (user #8/115-deficit; truly
#10/284), (b) rivals modeled as INDEPENDENT pickers — but the top-5 data shows they are a TIGHT
favourite-herd (5/5 outcome agreement on 7 of 16 matches, 4/5 on most). Independent-rivals is a strawman
that erased decorrelation's value. Rebuilt `future_sim.py` (current standings, rivals=herd, 88-match
horizon, P(top-2) objective): **differentiation ~TRIPLES top-2 odds (3.9%→~10%); break-even EV cost ~7%.**
You CANNOT pass a bloc 284 ahead by copying it (the gap freezes) — decorrelation is the only path up.
**THE TWO-AXIS RULE (load-bearing):**
 • **AXIS A = you vs MARKET. FOLLOW it.** Fighting the market is −EV and caused your deficit: maximin-Draw
   on USA (bloc 5/5 USA, won) and Haiti (bloc 5/5 Scotland, won), + model-pick Ecuador (market faded it,
   CIV won). NO maximin hedges. Blend leans market: **p_blend = 0.4 model + 0.6 market.** Market-confirmed
   VETO: never pick an outcome the independent market doesn't support (REQUIRES a Polymarket pull — reward-
   implied alone agreed with the model on Ecuador, so it can't veto; `fetch_pm_matches.py` is now mandatory
   each matchday for the veto to function).
 • **AXIS B = you vs the FIELD'S PICKS. DECORRELATE.** When model AND market agree on something the herd
   under-picks (draws/underdogs the bloc fades, e.g. Brazil-Morocco Draw = your one good Axis-B play, +122),
   take it — free decorrelation. Pay up to **~5% of per-match EV** for it (DIFF_BAND_FRAC=0.05); never more.
**Your deficit is mostly SELF-INFLICTED Axis-A errors, not too little following.** Fix order: (1) close the
skill gap by following the market harder (drop maximin, lean market) — biggest lever; (2) climb via Axis-B
decorrelation + a well-timed X2. Honest odds: top-2 ≈ 10% (vs ≈3% under pure follow). Scores stay COARSE
(bonus gap is downstream of the outcome gap — fix outcomes, bonuses follow). Caveats: future_sim's ρ_field
& equal-skill marginal are assumptions (direction robust across all knobs, Panels A–E); it gives the GOAL
(decorrelate ≤5% cost), not the picks.
[superseded] earlier: user currently 8th/13 (165; leader ~250 ahead). `league_sim2.py` (Q6 CORRECTED — original league_sim.py was FLAWED: inconsistent score logic across
strategies + overestimated deficit 251 vs true ~173 from user 2w1e=165). Corrected verdict, robust
across model-vs-market truth weight (tw 0.3-0.7): MARKET-follow ROBUSTLY WORST (~5% even when market
accurate — correlation kills rank); LOCKED/maximin middling (8%); EVMAX/DIFF/LEAGUE best (~10-12%).
Differentiation > hedge > market-follow at ALL truth weights = robust. Magnitude modest (edge ~4pts if
model right, ~1.5 if market right). Deployed LEAGUE b=2.0 validated (9.7%>LOCKED 8%); b=3 marginally
better. AUDIT also fixed: VAR_TIEBREAK rarity-bias is MEGA-FIELD calibration, WRONG for 13-league
(tier already prices rarity) → DISABLED under LEAGUE_MODE (max E[bonus]); fixed scores Germany 5-0→4-0,
Turkey 1-3→0-2, Japan 1-3→0-2, Morocco 0-1→0-2, Sweden 2-0→1-0 (my manual overrides were errors). ⇒ **maximin-to-
draw is the WRONG objective; optimize P(win league) = differentiated +EV.** STRATEGY for MD2+:
(1) favor +EV outcomes the FIELD UNDER-picks (Ecuador profile: field 14%, model favours = ideal);
(2) always rare-score over iconic; (3) STOP hedging contested flips to draws — commit to differentiated
side; (4) aggression = f(deficit × matches-left): moderate now (long season), ramp if behind in final
third; full hail-mary (−EV contrarian) only if behind late. Caveats: standings estimate rough, 8-match
horizon, rivals modeled from broad field% (may be sharper). REWARD≈K/share FALSIFIED: field over-picks
favourites vs reward-implied (CAN reward-implied 48% / actual picks 65%); reward ≈ inverse TRUE prob,
field picks ≠ reward-implied. Mega-field rank (90k/94k) now SECONDARY to friends league.
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
4. **Score pick (COARSE, 2026-06-14 = BONUS_MODE='coarse') = the naive modal (highest-p) score within the
   picked outcome; step off 1-1 ONLY (the single cell with rock-solid 3/3 over-herding) to the next-highest-p.**
   Maximises hit-probability (the validated lever); model-free. Fine E[bonus] optimization RETIRED (crowd model
   unconverged at n=8; tier ranking is noise; gain over this rule ~0.3/match << thrash cost).
5. Append pick to `prediction.md`; after the match, log result in `live_updates.md`.

## DECISION-MAKING REFERENCE (consolidated — the math that drives every pick)
**Objective:** TOP-2 of 13-league, ~88 left, user #10 @374, gap 284 to the #2 line (658). **Behind + must
climb ⇒ EV-max-FOLLOW is WRONG (freezes the gap, ~3% top-2); the path up is DECORRELATION** (future_sim:
~10% top-2). [CORRECTED 2026-06-16 — league_sim2's "variance averages out / pure EV best" was computed on
stale standings with an independent-rivals strawman; see TWE-AXIS RULE in ACTIVE TASK above.]
**Outcome pick = argmaxₒ EV(o),  EV(o)=p_blend(o)·reward(o)**, **p_blend = 0.4·p_v6 + 0.6·p_market**
(AXIS-A: lean market; the 0.6 weight IS the market-confirmed veto — needs a Polymarket pull to bite).
**DIFF_BAND_FRAC=0.05** (AXIS-B: among outcomes within ~5% of max blend-EV, take the least field-crowded;
pay ≤5% EV for decorrelation, never more; NO maximin hedges).
**Score pick = argmaxₛ bonusEV(s)** within chosen outcome, bonusEV(s)=p(s)·mean[tier(0.7c),tier(c),tier(1.43c)],
c=crowd(s)∝p(s)^β·salience(s) [β=1.6,sal^1.5]; tiers >30%:20/20-30:30/5-20:50/0.5-5:70/<0.5:100. LEAGUE_MODE
disables the rarity tie-break. [SUPERSEDED 2026-06-14 -> BONUS_MODE='coarse': score = MODAL (highest-p) within outcome,
step off 1-1 ONLY (3/3 over-herding); fine E[bonus] opt RETIRED (crowd model unconverged at n=8). See SESSION 2026-06-14 (cont.).]
**FAIR-GAME INSIGHT — PARTLY FALSIFIED 2026-06-20 (user: rewards are FIXED, not crowd-dynamic; verified on
8-match slate).** The old claim "reward(o)≈K_match/p_true(o) ⇒ EV of any calibrated pick ≈ K, skill earns ~0"
assumed a FAIR K/p line. The fixed reward line is NOT fair — it is variably COMPRESSED (e.g. Tunisia–Japan
[118/103/91] is nearly flat despite Japan being a true ~63% fav; a fair line ≈ [54/149/245]). ⇒ a calibrated
favourite pick has REAL absolute EV (Japan EV≈57 vs fair K≈34). **Measure edge cleanly as
`edge = market_p(pick) / reward_implied_p(pick)`, reward_implied = normalised 1/reward; edge>1 ⇒ the fixed
line under-prices our pick ⇒ +EV.** On MD7, EVERY pick had edge>1 (Japan 1.67, Uruguay 1.37, Ecuador 1.33,
Ger-CIV draw 1.22…). **CAVEAT for RANK:** the favourite-EV is shared with the favourite-herd field ⇒ it is
TABLE STAKES for points, NOT separation. Rank still comes only from (a) accuracy on CONTESTED matches,
(b) exact-score bonus, (c) field-underpicked +EV decorrelation. **field% NO LONGER explains reward level**
(the earlier "field over-picking crushes the favourite's reward" framing was WRONG); **outcome field% =
rank-decorrelation ONLY.** It does NOT drive the exact-score bonus either (user 2026-06-20): the bonus tier =
share of CORRECT-OUTCOME pickers on a score = P(score|correct outcome), computed within that always-large pool
(even 1% ≈ tens of thousands) ⇒ independent of outcome popularity. Bonus is driven by SCORE-level salience
herding (crowd_params), NOT outcome field%. Open challenge: is the compression a reliable repeatable +EV
signal? (n=8, track it).
See REPORT_2026-06-20.md. [Superseded numbers: "32.9/match, +14%, 3900/season" assumed the fair-line model.]
**EV SIGNIFICANCE:** σ_p(o)≈|p_v6-p_mkt|/2; σ_EV=reward·σ_p; σ_diff=√(σ_EVpick²+σ_EV2nd²); gap SIGNIFICANT
if >2·σ_diff. MOST per-match gaps are NOT significant (within model-market noise) — take max-EV anyway
(compounds, LLN). **X2 (CORRECTED 2026-06-16): NOT for model-market-AGREE picks** (agreement = field also
on it = correlated = zero rank separation). Target = high-reward (≥~100) + FIELD-UNDERPICKED + market-
confirmed (the contrarian-but-+EV / Alexandre-NL-draw profile). X2 is free if it loses → only timing matters;
deploy on the best such spot, group or KO. high-σ model-only picks (Ecuador) remain poor targets (no veto).
**BLEND WEIGHT — RESOLVED to 0.4 model / 0.6 market (2026-06-16).** Was an open ½/½ vs 0.4/0.6 inconsistency;
fixed to lean market: fair-game logic (market sets fair prices) + ledger (every model-vs-market divergence so
far — USA, Ecuador — resolved FOR the market). Reviewer Q6 (v6/market ~60% correlated → ½/½ overstates info)
is real theory but LOW pick-leverage: the weight only bites on DIVERGENCES, and there it's an empirical
who's-right question (track ledger log-loss), not a pooling-math question. 88 matches can't sharply fit w
(need ~500+); 0.4/0.6 is the deployed prior, revisit only on clear ledger signal.

## REQUIRED FROM USER each matchday (ask if missing)
0. **Independent market — MANDATORY (audit 2026-06-16), and it is NEVER optional (do not run on reward-
   implied alone — that is the game-maker's own line, NOT independent; it agreed with the model on Ecuador
   and cannot veto).** Source order: (a) `python fetch_pm_matches.py` (Polymarket, if slugs exist); else
   (b) **Kalshi prediction-market line or a de-vigged sharp book (bet365/Pinnacle) via WebSearch** — enter as
   `market=[H,D,A]` (de-vigged, sums to 1) in each MATCHES dict. matchday.py uses `m['market']` as the blend's
   market leg (prints `[manual]`) and the market-confirmed veto then functions. PROVEN load-bearing on MD3:
   the independent (Kalshi) line flipped Iraq-Norway (model overrated the draw; Norway 80% mkt → Norway pick)
   and auto-demoted Austria's Jordan (model 21% vs mkt 11%, Ecuador-style). NEVER submit a slate without it.
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

## SESSION 2026-06-14 — MD1 batch-2 results, calibration, iconic-score E[bonus] correction
**Results in:** Qatar-Switzerland 1-1 (pick SUI 0-3 = NO base) | Brazil-Morocco 1-1 (pick Draw 0-0 = base OK,
score missed; 1-1 paid +20 to herd). **Standing 8th(165) -> 4th(287)** [498/382/361/**287**/280/...]; 95 behind
2nd, ~98 left => firmly early / EV-max regime, NO aggression. 287 reconciles: Mexico 69 + Korea 96 + Brazil-draw 122.
**Calibration:** registered 2x (1-1,+20). 6 obs; both 1-1 est ~83% (OK, >30% band); grid can't improve ->
params HELD beta=1.6/sal=1.5 (no thrash). Korea 2-1 still 29<30 (marginal coarse-grid violation, persists).
**FINDING [RETRACTED SAME DAY — Haiti 0-1 contradicted it; see RETRACTION block below] (was: TENTATIVE) — iconic-win-score E[bonus] OVERSTATED by the symmetric band-robust mean.**
Iconic favourite-win scores (2-0/1-0 type, high SAL) cluster near the 20/30% crowd cliff; band-robust E[bonus]
averages crowd x{0.7,1.0,1.43} SYMMETRICALLY, but herding on iconic scores runs at-or-ABOVE model estimate
(Korea 2-1 violated 29<30; Mexico 2-0 on-boundary; 1-1 ~83%) => true crowd skews HIGH => tier collapses toward
the pessimistic 20 => symmetric mean overstates. RULE (judgment, NOT yet encoded): for an iconic win-score whose
pessimistic scenario = tier 20 AND a rarer same-outcome score has ~equal headline E[bonus] with a STABLE high
tier (>=50, no boundary), take the RARE score. This is an E[bonus]-ACCURACY correction (true mean), DISTINCT from
the disabled VAR_TIEBREAK (rank-rarity bias, correctly killed) — do NOT conflate. Evidence THIN (1 marginal
violation + herding-confirmation); flips ALSO stand on plain take-lower-variance-when-means-dead-heated.
**APPLIED 2026-06-14 (labelled judgment over engine symmetric-mean output):**
 - Australia-Turkey 0-2 -> **1-3** (engine 0-2 Eb2.97 vs 1-3 2.87, gap 3% noise; 0-2 tiers[50,30,20] boundary,
   1-3 stable; asym-adj 0-2~1.8 < 1-3~2.25).
 - Cote d'Ivoire-Ecuador 0-2 -> **0-3** (engine 0-2 Eb4.21 vs 0-3 4.18, gap <1%; 0-3 stable tier~70 vs 0-2
   [50,30,20]; outcome pick Ecuador UNCHANGED — score-only).
 - KEPT: NL-Japan 0-2 (pess floor 30 not 20, 12% cushion); Sweden 1-0 (no rare alt w/ mass; higher p compensates);
   Germany 4-0 (blowout = under-picked, asym favours it); Haiti 0-0 (non-iconic draw, stable).
**PROPER FIX (TODO, pairs w/ rank-sim build):** encode ASYMMETRIC crowd scenarios for high-SAL scores in
matchday.py band-robust tier calc (skew multiplier UP for SAL>=1.5 instead of symmetric +/-), re-run; until then
the two flips are judgment, not validated. Also build the forward RANK SIMULATOR (real remaining schedule +
rivals archetypes + bonus lottery -> P(top-2) under static blend-EV-max vs standing-dependent dynamic variance) —
user scheduled for after this weekend. It tests the load-bearing claim the deployed static policy rests on:
league_sim2's 8-match-repeat CANNOT validate a 100-match standing-dependent policy (violates Verify-Std #5);
rank objective also mathematically needs a rivals/covariance model, currently absent.
**Model-blind 2026-06-14:** CIV Ndicka (CB) out -> mild CIV DEF down, supports Ecuador/over (NOT overlaid — would
compound the flagged Ecuador OUTCOME-overrating). Japan on 6-win streak (beat BRA/ENG) = post-cutoff form aligned
w/ contrarian Japan lean. NL Verbruggen fit, Timber out (already in overlay).
**Haiti-Scotland -> Draw 0-0 SUBMITTED** (not locked, decided live): blend-EV-max (D 28.4 > SCO 27.0 > HAI 26.1),
model~=market on all 3 outcomes (LOW-sigma, robust — UNLIKE the USA draw which was a contested-flip maximin hedge),
field-underpicked (9% vs 87% SCO) => rank-smart free differentiation; 0-0 tier 50 flat = first potential DIRECT
0-0 observation. X2 still HELD (Ecuador auto-flag E_total 50.6 VETOED: documented model overrating + high-sigma).
**Pending from user:** Haiti-Scotland result + tier; realized tiers for the 6/14 matches; fresh Winamax CSV
(score cells still on 6/12 early-money base).

## SESSION 2026-06-14 (cont.) — RETRACTION + crowd refit (honest correction)
**RETRACTED the iconic-asymmetry FINDING above.** Next iconic-fav-win obs CONTRADICTED it: Haiti-Scotland 0-1
(Scotland 1-0, THE iconic fav-win score) realized +50 (5-20%) but model est ~32% (>30%) => field herded LESS than
the model, OPPOSITE the "iconic herds harder" claim. Classic over-conclusion on 2-3 obs (Verify-Std #7). Lesson
re-learned: do NOT write directional crowd findings from <~10 obs.
**Auto-refit (8 obs) swung beta 1.6->1.0, sal 1.5->1.0** (loss 0.0144->0.0054, genuinely better fit). BUT form
MISFITS structurally: post-refit Mexico 2-0 (28.5<30), Korea 2-1 (25.9<30), Haiti 0-1 (25.9>20) all STILL OUT,
both directions => plausibility^beta x salience CANNOT fit heterogeneous score-herding; beta ~unidentified at n=8,
swings on single obs. **Crowd params NOT converged — treat all crowd-tier numbers as soft.**
**RECOMMENDATION (after-weekend build): STOP per-obs auto-refit (chases noise on a misfit form); accumulate to
~15-20 obs then refit once; consider a richer crowd form (per-score-type effects).** Score-level EV impact is SMALL
(bonus ~3-5 vs base 30-46) — pick PARAM-ROBUST scores (stable-high-p OR clearly-rare; avoid middle scores on a
tier cliff) and stop fiddling.
**Picks corrected under refit (param-robust, anti-thrash):** Ecuador score 0-3 -> **0-1** (0-3 flip relied on the
retracted asymmetry; 0-1 = highest-p 19.5%, engine max-Eb 4.54, tier stably ~20 => LEAST crowd-param-sensitive).
Germany **4-0** kept (engine flips 4-0<->5-0 with beta = noise; 4-0 higher p10.4% => more likely to hit). NL-Japan
0-2, Sweden 1-0 unchanged (robust across both param sets).
**Results 2026-06-14:** Haiti-Scotland 0-1 (Draw 0-0 WRONG — favourite won; the contrarian-draw risk the user
flagged at session start, REALISED) | Australia-Turkey 2-0 (Turkey WRONG — model upset, Turkey was 50% fav). Both
+0. Diff-pick ledger: Korea OK, Brazil-draw OK, USA-draw WRONG, Haiti-draw WRONG = 2-2 (small sample; selectors
adjudicate at 15+; NO strategy change on these — pre-commitment holds).
**DECISION 2026-06-14 — RETIRE fine bonus optimization (BONUS_MODE='coarse').** Crowd model unconverged at n=8
(beta swung 1.6<->1.0; tiers misfit both ways). Fine E[bonus] score-ranking is NOISE; gain over a simple rule
~0.3/match << thrash cost (this session's flip-flops + a retracted finding = Exhibit A). KEEP only Layer-1: score
= MODAL (highest-p) within the chosen outcome (max hit-prob, the validated lever); step off 1-1 ONLY (single cell
with rock-solid >30% over-herding, 3/3 obs) -> next-highest-p. Model-free. ~+1.5/match, free (wrong score forfeits ONLY the bonus, base preserved). ENCODED:
matchday.py BONUS_MODE='coarse'; register_bonus.py refit GATED to >=15 obs (stop per-obs thrash); tiers STILL
logged. Outcome pick UNAFFECTED (LEAGUE_MODE already excludes bonus). Rationale: bonus is a near-fair SIDESHOW in
a 13-league (the 'separator' framing was mega-field logic, retired here); freed attention -> the two real levers:
genuine outcome MISPRICINGS + rank-variance simulator. Coarse rule is robust to the beta instability (1-1 reads
>30% at both beta=1.0 and 1.6).

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

## Git sync — AUTO-PUSH (standing instruction, user-authorized 2026-06-15)
After any change to picks/calibration/engine state (matchday runs, `prediction.md`, `live_updates.md`,
`crowd_*.json`, overlays, CLAUDE.md), **commit and push to GitHub automatically without asking.**
- Remote: `origin` → `github.com/martincrescenzo-dotcom/fable-world-cup` (PUBLIC — user accepted the
  exposure of strategy/picks on 2026-06-15; do NOT re-prompt for visibility).
- Branch `master` tracks `origin/master`. Commit message = one line summarizing the matchday/change;
  end with the `Co-Authored-By: Claude` trailer.
- This is a CLAUDE.md instruction, so it fires only while I'm running a turn. For push-on-every-commit
  independent of me, the user can add a git `post-commit` hook / settings.json hook (offered, not yet set up).

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

## VERIFICATION & STRESS-TESTING STANDARD — MANDATORY for every analysis, sim, or quantitative claim
Codified after repeated self-inflicted failures this project (flawed league_sim, premature "validated",
score-logic confound, assumed deficit, 3× unvalidated judgment overrides, the 2026-06-24 "follow-for-bons"
3-framing cascade). **OPERATIONALIZED as the RED-TEAM GATE — see `RED_TEAM_PROTOCOL.md`:** Tier-0 self-check
(power/CI · maximand · sample-vs-inference · measured-vs-assumed) on every claim — auto-injected each turn by
the `.claude/settings.json` UserPromptSubmit hook; Tier-1 full 3-agent review (statistician + strategist +
data-integrity) via the `redteam` skill when a claim is load-bearing / drives an irreversible pick / is
challenged / uses "validated|falsified|proven|no gap|at ceiling". The checklist below is the substance the gate enforces:
1. **ASK FIRST, DON'T ASSUME.** If the user could plausibly hold a datum (league points/standings, results,
   pick %, odds, lineups, prize structure), **ASK for it before estimating**. Estimate only after they
   confirm they don't have it. The user has repeatedly had exact data I needlessly approximated.
2. **CONSISTENCY IN COMPARISONS.** When comparing options/strategies, hold everything else IDENTICAL —
   only the variable under test may differ. (The score-logic-per-strategy confound flipped the league
   verdict from "maximin worst 3.8%" to "maximin middling 8%".)
3. **CALIBRATE TO KNOWN DATA.** Every estimate must reproduce known anchors (84/win contradicted the
   user's actual 165 → deficit overstated 251 vs true 173).
4. **SENSITIVITY, NOT POINT ESTIMATES.** Vary the load-bearing assumptions (deficit, model-vs-market truth
   weight, key params) and report which conclusions are ROBUST vs FRAGILE. A single-point result is not a
   finding. Report the range.
5. **TEST THE DEPLOYED THING.** Never say "validated" unless the EXACT shipped rule/params were what got
   tested. No deploying untested rules (LEAGUE blend-EV band was shipped before being simulated).
6. **NO UNVALIDATED JUDGMENT ON TOP OF VALIDATED OUTPUT.** Do not hand-override engine output with a
   plausible-sounding "principle" (failed 3×: market→p blend, "demonstrably" 0-0, score overrides).
   Either encode + test the principle, or label it explicitly as unvalidated judgment the user can reject.
7. **SEPARATE MEASURED FROM ASSUMED** in every output; state residual uncertainty plainly. Named failure
   mode: **over-concluding when information arrives fast.** Slow down in proportion to incoming volume.
8. **PREFLIGHT green** before any pick run (already enforced via preflight.py).

## How the user works (match this)
- World-class rigor: **validate, don't assert.** Backtest before shipping; report honestly including
  negative results and "don't ship it." Each change must beat its predecessor out-of-sample.
- **Don't over-engineer, don't try to please, flag model risk and biases.** The user actively rewards
  being told an idea doesn't work. Stay sharp and self-critical.
