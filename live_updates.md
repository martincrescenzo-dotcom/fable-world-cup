# Live Tournament Updates — results, model-blind events, pick log

## ════ MODEL vs DE-VIGGED WINAMAX — score-prediction validation (2026-06-18, 19 matches) ════
Cross-checked v6 (pure) score grids vs de-vigged Winamax exact-score côtes for all 19 stored matches.
**SHAPE: excellent** — mean cell-corr 0.96 (median 0.97, min 0.85 US-Par), mean abs err 0.96%/cell; 1X2
divergences concentrate in the already-flagged matches (US-Par, Ecuador, Qatar-Swiss, Canada) = rediscovers
known divergences, no new ones. **PREDICTIVE (log-loss on the REALIZED score, all 19 played):** Winamax 2.83 <
model 3.13 (lower=better); model better on only 4/19. BUT decompose: NON-tail (11) model 2.65 ≈ winx 2.55
(TIED within noise — strong for a model vs market); TAIL realized>=4g (8) model 3.79 >> winx 3.22 — the model
LOSES on high-scoring games. This tournament ran a FAT tail (Ger 7-1, Swe 5-1, USA 4-1, Eng 4-2, Iraq 1-4) and
v6's tail is too thin -> under-priced all of them. **Caveats:** the tail gap is partly MY artifact (3 Autre
scores got handed the whole Autre mass — Germany 7-1 alone ~0.12 of the 0.30 gap; corrected gap is smaller, the
bulk-TIE is the honest headline); n=19; single-bookie 150% vig de-vig is imprecise (doesn't strip longshot
shading -> inflates market tail). **FLAG (contradiction):** CLAUDE.md 'known fact' says model tail FATTER than
market; this measurement + realized results show model tail THINNER (under-called the tail). Reconcile, don't
trust the old note. **Strategic implication: NONE for picks** — model can't call the tail, which is exactly why
we take the MODAL low-scoring score and don't gamble on rare high exacts. Thin tail is documented + OOS-unfixable
(dispersion fix overfit). Calibration finding, not a doctrine change.
## ═══════════════════════════════════════════════════════════════════════════════════════════

## ════ LEARNINGS (2026-06-17, post score-rule backtest) — read first ════
Distilled from score_rule_backtest.py (20 obs), the 45%-modal-outcome count, and the MD3/MD4 results.
Separated ROBUST vs TENTATIVE (Verify-Std #4/#7).
**META (the load-bearing one):** the score/crowd/bonus layer is a CONVERGED SIDESHOW — stop mining it for
edge. Three sessions of crowd-model refits / iconic-asymmetry / rare-score optimization netted ~0 and
produced 2 retracted findings. Bonus is ~2-5 pts vs base 30-70. Spend attention on the 2 levers that move
RANK: (1) the mandatory independent-market pull, (2) honest variance-timing. Treat scores as a 1-line rule.
**ROBUST, ACTED ON:**
 1. SCORE = pure modal (highest-p), MECHANICAL. Backtest: pure-modal 190 realized bonus > step-off-1-1 130
    (+60); rare-score E[bonus] optimizer 130 = NO realized edge (REJECTED — expected edge is model-internal,
    swamped by exact-hit variance at n=20). ⇒ DEPLOYED: removed the 1-1 step-off in matchday.py (pure modal).
    Caveat: 1-1-frequency edge is sample-dependent (draw-heavy 8/20); tier-20-on-1-1 is solid (5/5).
 2. Independent-market pull is LOAD-BEARING, proven 2x (Iraq→Norway hit; caught Ghana/Panama artifact, like
    Ecuador). Relative-strength model-vs-market splits resolve FOR the market every time. NEVER skip it.
 3. Decorrelation target MOVED. The field now HERDS ON DRAWS (30-39% on MD4, post-draw-fever) → draws are no
    longer field-underpicked. Axis-B separation now lives in AWAY UNDERDOGS (Croatia 8%/Panama 7%/Bosnia 7%),
    NOT draws. Bonus: draws are also the model's weakest call (caught 1 of 8). Stop picking draws "to decorrelate".
**HONEST STRATEGIC READ:** 45% modal-outcome rate ≈ the CEILING of favourite-following on this draw-heavy run,
and it does NOT catch a 13/20 leader (you're 7/20; deviations cost the other 2). Following keeps you ~field-
average = ~12th while the bloc gains too (gap to #2 WIDENED 284→368 despite +73). Top-2 is now a genuine long
shot; the ONLY closer is correct contrarian outcomes (high-variance, went 0/2 MD3). ⇒ FORWARD RULE:
 • NOW (≥30 left): EV-max FOLLOW + mechanical modal scores. Take ZERO-cost Axis-B underdogs (in EV band, e.g.
   Panama); SKIP marginal ones (e.g. the England draw). Don't bleed EV on speculative decorrelation yet.
 • FINAL THIRD if still >300 behind: deliberately RAMP variance (+EV contrarian underdogs + deploy X2),
   accepting frequent losses — field-average finishes 12th; only variance finishes top-2.
**TENTATIVE / DON'T over-conclude:** draw rate 40% is likely a blip (regresses to ~28%) — NO permanent draw
overlay. Leader's 13/20 may be variance not skill (n=20). Blend weight ½/½... wait 0.4/0.6 still a prior — need
~30-40 more logged matches WITH market+field% (now captured) to fit it & measure if Axis-B actually pays.
## ═══════════════════════════════════════════════════════════════════════════════════════════

## ════ MD4 SLATE SUBMITTED (2026-06-17/18) — read first ════
Inputs: user Cotes (rewards) + Répartition (fieldpct); INDEPENDENT market = de-vigged sharp books via WebSearch
(bet365/FanDuel/DraftKings/1xbet, 2026-06-17). Preflight GREEN. matchday.py run, two judgment overrides:
 - **Uzbekistan–Colombia → Colombia 0-1** (FOLLOW; model=market identical 12/21/67; field 89% chalk, no sep).
 - **Czechia–South Africa → Czechia 1-0** (FOLLOW; blendEV 34.7; model 61 hot vs mkt 53, same side).
 - **Switzerland–Bosnia → Switzerland 2-0** (FOLLOW; blendEV 49.8; model 75 hot vs mkt 60, same side; field 70%).
 - **England–Croatia → England 1-0** (OVERRIDE engine's Axis-B Draw): field now DRAW-HERDS (39%) so Draw no
   longer underpicked → decorrelation premium gone; blend-EV-max is England anyway (31.2 vs 30.9). Lower variance.
 - **Ghana–Panama → Panama 0-1** (AXIS-B decorrelation, the one real separation spot): **MODEL ARTIFACT** — v6
   has Panama 63% but market+reward+field ALL favour Ghana (mkt 43/29/28). Ecuador-class; the engine's blendEV
   Panama 48.6 / X2-PRIME flag are ARTIFACT-INFLATED → IGNORED. On market-only it's a fair-game even match
   (Ghana 31.5 / Draw 32.5 / Panama 32.5 EV); Panama is least field-crowded (7%) in the EV band → doctrine pick
   even discarding the broken model. Honest: ~28% to hit, ~0 EV cost, real decorrelation. Alt = Ghana (follow).
**X2 HELD:** Switzerland flag = field 70% (correlated, no separation); Ghana-Panama PRIME flag = artifact (28%
Panama not confident enough for the one-shot). No genuine high-reward+underpicked+confirmed spot this slate.
**NEW KNOWN ARTIFACT (log to audit): GHANA underrated / PANAMA overrated by v6** (model Panama 63% vs market
Ghana 43%). Same class as Ecuador (attdef relative-strength artifact). Do NOT refit mid-tournament; market-veto
handles it. Watch the result — if Ghana wins, confirms artifact.
**Model-blind scan 2026-06-17 (light — picks are mostly chalk follows):** England-Croatia Group L opener (Dallas);
Switzerland & Bosnia both drew openers (1-1); Czechia lost 2-1 to Korea, SA lost 2-0 to Mexico (both must-win).
No material injury news surfaced in previews → overlays all ZERO. Ghana-Panama divergence is a RATING artifact,
not model-blindness.
## ════ POPULATION ASSUMPTION + DISCIPLINE CHECK (2026-06-18) — read first ════
**User challenge (correct, META-level): the per-match `fieldpct` (e.g. 52/34/15) is the MEGA-FIELD, not the
16-league split — which population proxies the league's crowding?** We do NOT observe the 15 rivals' per-match
picks (user confirmed not visible; only an early top-5 CSV showing a favourite-herd).
**RESOLUTION (stay true to doctrine — do NOT override it on unobservable inputs):**
 • mega-field is an imperfect but CONSERVATIVE proxy: a favourite-herd league underpicks underdogs/draws EVEN MORE
   than the mega-field, so decorrelating against mega-field UNDERSTATES the benefit — direction is safe. Keep it.
 • RETRACTED my earlier over-read "draws are now crowded" (that was a mega-field draw% read) — in a favourite-herd
   league the draw is likely UNDERpicked, which is why the engine correctly differentiates to it.
 • DISCIPLINE NOTE (self-correction): I let the population question cascade into OVERRIDING the engine pick twice
   (Mexico, then Korea) using a seat-sim built on ASSUMED rival splits — the exact "unvalidated judgment on
   validated output" the doctrine forbids (Verify-Std #6). REVERTED to the engine's straight output.
**Seat-sim = explored SANITY CHECK, NOT adopted as a rule** (it used unobservable splits). It did confirm the
deployed Axis-B direction: at #14, an in-band decorrelation (Draw +1.1 seats / ~20% top10) >> follow-favourite
(+0.3 / 0%), and Draw ≈ Korea on seats — so the IN-BAND disciplined pick (Draw) captures ~all the benefit without
breaking the 5% EV band. No doctrine change. Caveat retained: top-5 unreachable in 1 match (max 679 < 703 line).
## ═══════════════════════════════════════════════════════════════════════════════════════════

## ════ LEADERBOARD 2026-06-18 — LEAGUE GREW TO 16 (new players joining) — read first ════
**USER = #14/16 (Lampadaire83) 550 pts, 9 bons, 1 exact.** Points reconcile (447 + England 59 + Colombia 44 = 550).
 #1 Alexlastaaaaar 1335 (15/4) | #2 CrazyBE 942 (15/1) | #3 Nicolas 918 (14/2) | #4 AdyFC 721 (12/**3**) |
 #5 Ethan_prn 703 (13/1) | #6 Diane123 693 (9/2) | #7 Alexis#KGYJ 684 (12/2) | #8 Chocho_27 667 (11/1) |
 #9 Hadri02 655 (11/**3**) | #10 Cyrilpqt 650 (10/2) | #11 LMD92110 640 (11/2) | #12 Paulinho 602 (10/2) |
 #13 FredFUP 587 (8/1) | **#14 USER 550 (9/1)** | #15 Helene 475 (10/1) | #16 DealNonClosey 390 (6/**3**, joined late).
**STRUCTURAL CHANGE — this is NOT a fixed 13-person herd.** League is OPEN/GROWING (new players: Ethan, Alexis,
DealNonClosey...). future_sim's fixed-13-herd model is now INVALID. Objective "top-2 of 13" is obsolete — ASK USER
for the real target (see below). RANK TRAJECTORY: user #10→#12→#14 over 3 matchdays while points rose 374→550 —
**following GAINS points but LOSES rank** (field climbs faster; stronger new players entered above).
**HOW THE CLIMBERS CLIMB (the signal):** Diane123 jumped #9→#6 in ONE matchday with a +160 (called Ghana upset +
exact). The EXACTS column separates: #1=4, #4/#9/#16=3 exacts vs USER=1. Climbing happens via (a) contrarian
OUTCOMES the field misses (Ghana) + (b) EXACT-score bonuses (+50 to +160 swings). Pure following does neither.
**TENSION with this session's "score = sideshow / EV-max follow" conclusion:** that holds for EV/points, but the
leaderboard shows RANK is moved by VARIANCE (contrarian calls + rare exacts), which a trailing player needs. The
backtest only proved we can't engineer more POINTS via the score rule — it did NOT address rank-variance. If the
objective is top-few-or-bust, the rank-correct move is to RAMP VARIANCE NOW (contrarian +EV underdogs + pick RARER
scores for exact-bonus leaps, reversing 'modal'), NOT wait for the final third — because rank is sliding every MD.
**OBJECTIVE RESOLVED (user, 2026-06-18): TOP-5 of ~16 (league settled at 16), BALANCED.** Supersedes "top-2 of 13".
STRATEGY:
 • BASE = EV-max FOLLOW + mechanical MODAL scores (unchanged; backtest holds for EV).
 • LAYER = SELECTIVE variance: take ONLY the highest-conviction field-underpicked + market-confirmed Axis-B spots.
   The recent 0/3 (France/Austria draws, Panama) were MARGINAL/artifact-driven → RAISE the conviction bar (genuine
   +EV underdog the market backs AND the field clearly fades, not an ~even-EV coin-flip). Skip marginal decorrelation.
 • NO full-variance ramp, NO rare-score exact-gamble (those were the top-2-or-bust path — not chosen). Keep modal.
 • X2 = deploy on a good field-underpicked + market-confirmed spot for a RANK BUMP when it appears; don't hoard for KO.
**REACHABILITY:** top-5 line = #5 Ethan 703; user 550; gap 153. Mid-table bunched (#6 693…#14 550 = 143 over 9
players) → ~1-2 good selective calls + steady base accumulation = top-5 is REALISTIC, not a hail-mary. One bad
variance batch drops toward last, so SELECTIVITY (not volume) of contrarian picks is the discipline.
**future_sim.py is now INVALID** (assumed fixed 13-herd; league is 16, different rivals). Rank target = top-5 of 16.
## ═══════════════════════════════════════════════════════════════════════════════════════════

**MD4 RESULTS (3 of 5 in, 2026-06-17):** **2/3 outcomes.**
 - **England 4–2 Croatia → HIT** (pick England 1-0, OVERRODE engine Draw → base +59). **Override vindicated.** 4-2 tier +70.
 - **Uzbekistan 1–3 Colombia → HIT** (pick Colombia 0-1, follow chalk → base +44). 1-3 tier +50.
 - **Ghana 1–0 Panama → MISS** (pick Panama 0-1, Axis-B decorrelation). **ARTIFACT CONFIRMED — Ghana won as market said** (v6 Panama 63% was wrong). Market-veto vindicated; aggressive Axis-B underdog lost (now 0/3 incl MD3 draws). 1-0 tier +20.
 - Czechia–SA + Switzerland–Bosnia still pending (6/18, both follows).
**Net MD4 so far: +103 base** (England 59 + Colombia 44; no exact-score bonus — scores missed). Portugal-DRC (MD3#5) was +0.
**KEY CONFIRMATIONS this batch:** (1) independent-market layer is LOAD-BEARING — caught Ghana artifact, exactly
like Ecuador; (2) "draws now crowded → follow, don't decorrelate-to-draw" was RIGHT (England override won);
(3) aggressive Axis-B underdog/draw picks are 0/3 (France/Austria draws + Panama) — the differentiation cost is
REAL and recurring. Reinforces the forward rule: EV-max FOLLOW + mechanical modal scores now; ramp variance
only in the final third.
**PENDING (ask user):** Czechia–SA + Switzerland–Bosnia results + tiers; updated leaderboard (running ~550 projected).
## ═══════════════════════════════════════════════════════════════════════════════════════════

## ════ MD3 RESULTS IN (2026-06-17, Iraq-Norway score CORRECTED) — read first ════
**4 of 5 reported (Portugal–DR Congo still pending). We went 2/4 on outcomes:**
 - **Iraq 1–4 Norway → HIT** (pick Norway 0-2, Axis-A follow Kalshi 80% Norway). Base ✅ (ASK reward), score missed, 1-4 tier +70. **The MD3 flip-to-Norway was VINDICATED — Norway won big.**
 - **Argentina 3–0 Algeria → HIT** (pick Arg 2-0, Axis-A follow). Base ✅ (ASK reward), score missed, 3-0 tier +50.
 - France 3–1 Senegal → **MISS** (pick Draw 0-0, Axis-B decorrelation; favourite WON). 3-1 tier +30.
 - Austria 3–1 Jordan → **MISS** (pick Draw 0-0, Axis-B; favourite WON). 3-1 tier +50.
**HONEST STRATEGIC READ (do NOT over-conclude, small n — Verify-Std #6/#7):** clean split by axis this slate —
**AXIS-A (follow market) went 2/2** (Norway, Argentina both hit); **AXIS-B (decorrelation draws) went 0/2**
(France, Austria — favourites won). MD2 was 4/4 draws (helped draw-pickers); MD3 reversed (favourites won the
openers we drew). The DRAW-CLUSTER FLAG (item 6 below) did NOT generalise to MD3 — opening-match draw overlay
stays UNBUILT/unwarranted. Axis-B diff-draw ledger this slate: France✗ Austria✗. This is consistent with the
doctrine's own warning: differentiation has a REAL EV cost (≤5% budget) and it bit here; market-follow is the
skill lever and it worked. **No strategy change on one slate** (pre-commitment) — but the slate leans FOR
Axis-A-follow and AGAINST aggressive diff-draws. Bonuses calibration-only (no exact score hit). Score-prob
note: all 4 actual scores had 3+ goals for the winning side — engine modal scores (1-0/2-0/0-2) again undershot
realized totals (persistent fat-real-tail vs model).
**LEADERBOARD IN (2026-06-17, full 13):**
 #1 Alexlastaaaaar 1232 (13 bon/4 exact) | #2 Nicolas 815 (12/2) | #3 CrazyBE 766 (12/1) | #4 Cyrilpqt 606 (9/2) |
 #5 LMD92110 596 (10/2) | #6 FredFUP 587 (8/1) | #7 Chocho_27 550 (9/1) | #8 AdyFC 525 (9/2) | #9 Diane123 489 (7/1) |
 #10 Paulinho1204 465 (8/1) | #11 Hadri02 459 (8/2) | **#12 USER (Lampadaire83) 447 (7 bon/1 exact)** | #13 Helene12ln 431 (9/1).
**USER 374→447 (+73)** = the two MD3 base hits (Norway + Argentina; no exact → all base, no bonus). **But rank
DROPPED #10→#12** — the favourite-hitting field gained MORE on the same MD3 favourites slate. **TOP-2 GAP WIDENED
284→368** (#2 line jumped 658→815, Nicolas +157 vs user +73). New gaps: #11 12 | #9 (489) 42 | #5 (596) 149 |
#3 (766) 319 | **#2 (815, TOP-2 LINE) 368** | #1 785. ~83 matches remain.
**HARD READ:** following the favourites WITH the herd (MD3 Axis-A) earns points but does NOT separate — user
gained ~field-average and fell two spots. This is the doctrine's central tension made concrete: you can't
out-points a bloc by copying it (gap froze/widened), yet the one separation lever (Axis-B diff-draws) went 0/2
this slate and cost EV. Neither axis is climbing right now. **STILL EV-max regime** (83 matches = long; variance
ramp only in final third) but the top-2 target is drifting — needs either a hot exact-score bonus run or a
correct high-reward contrarian (the X2 spot). NO panic aggression yet; re-evaluate the variance trigger if the
gap is still >300 with <30 matches left.
**X2 STILL HELD** — none of MD3 was the profile (Norway/Argentina were market-agree favourites = correlated =
no separation; the diff-draws lost). Keep waiting for high-reward (≥100) + field-underpicked + market-confirmed.
**PENDING (ask user):** (1) Portugal–DR Congo result + tier (5th MD3 match); (2) split of the +73 (Norway base
vs Argentina base) if you want it logged per-match — not required, total reconciles.
## ═══════════════════════════════════════════════════════════════════════════════════════════

## ════ CURRENT STATE SNAPSHOT (2026-06-16) — read this first; rows below are edit history ════
**Objective:** TOP-2 of 13-person friends league. **User: was 9th/13, 374 pts** (pre-MD2). **MD2 went 0/4 — all four picks were favourites/Uruguay that DREW (Belgium 1-1, Saudi-Uruguay 1-1, Iran 2-2, Spain 0-0). +0 base, +0 bonus (none of our scores hit).** ⚠ ASK USER for updated leaderboard — standing likely dropped.
**Friends league standings POST-MD2 (2026-06-16, ~16 matches played):**
 #1 1113 (11W/3E) | #2 658 (8W/2E) | #3 609 (8W/1E) | #4 557 (7W/1E) | #5 436 (6W/1E) | #6 419 (5W/1E) | #7 411 (6W/2E) | #8 405 (5W/1E) | #9 389 (6W/1E) | **#10 USER 374 (5W/1E)** | #11-13 unknown.
**User dropped 9th→10th** (374 unchanged = MD2 0/4 confirmed; field's draw-pickers leapt — #2 +116 in MD2).
**Gaps:** to #9: 15 | to #8: 31 | to #7: 37 | to #6: 45 | to #5: 62 | to #4 (top-4): 183 | to #3: 235 | **to #2 (TOP-2 LINE): 284** | to #1: 739. ~88 matches remain.
**TOP-2 read:** target is the #2 line (658), gap 284 over ~88 matches. Leader 1113 is runaway (irrelevant for 2nd). #2–#4 bunched (658/609/557). Still LONG horizon → EV-max regime, NO aggression yet (variance ramps only if still trailing in final third).
**MD1 fully resolved (12 matches):** 5/12 correct outcomes, 1/12 exact score (Mexico 2-0). 
 5 hits: Mexico✅+20 | Korea✅ | Brazil-Morocco Draw✅ | Germany✅ | Sweden✅
 7 misses: Canada | USA | Qatar-Swiss | Haiti-Scotland | Australia-Turkey | NL-Japan | CIV-Ecuador
**Running total: 374 pts** (69 Mexico + 96 Korea + 122 Brazil-Morocco + 15 Germany + 72 Sweden).
**Sweden-Tunisia tier: +100** (5-1, model est 0.2% → OK; we picked 1-0 so bonus not ours — calibration only).
**Strategy (CORRECTED 2026-06-16 AUDIT — supersedes "pure EV-max / DIFF_BAND=0"):** behind + must climb ⇒
EV-max-FOLLOW freezes the 284 gap (~3% top-2); decorrelation is the path up (future_sim ~10%). **TWO-AXIS
RULE:** AXIS-A (vs market) = FOLLOW (blend 0.4 model/0.6 market, NO maximin, market-confirmed veto — needs
Polymarket pull); AXIS-B (vs field's picks) = DECORRELATE on field-underpicked + market-confirmed spots, pay
≤5% EV (DIFF_BAND_FRAC=0.05). Deficit is mostly self-inflicted Axis-A errors (USA/Haiti maximin, Ecuador
model-pick). COARSE scores unchanged. See CLAUDE.md ACTIVE TASK for full rationale + future_sim.py.
**X2 boost: HELD (criterion FLIPPED).** Deploy on high-reward (≥~100) + FIELD-UNDERPICKED + market-confirmed
spot, group OR KO (free if it loses → only timing matters). NOT model-market-agree (= correlated = no
separation). Evidence: Alexandre X2'd NL-Japan DRAW (115)→+115; Nicolas/Bertrand WASTED it on Germany lock→+15.
**TOP-5 RIVAL DATA (pronos_unifies_top_players_league.csv, 16 matches) — analysed 2026-06-16:**
 Totals reconcile EXACTLY to standings: Alexandre 1113(#1), Nicolas 658(#2), Bertrand 609(#3), Frederic
 557(#4), Gaspard 436(#5). Correct OUTCOMES: Alex 11/16, the rest 8/8/7/6 vs USER 5/16. **The field is a
 TIGHT favourite-herd** (5/5 outcome agreement on 7 of 16 matches, 4/5 on most; scores all iconic) → ρ_field
 HIGH → decorrelation MORE valuable. **User's outcome deficit is self-inflicted:** lost USA (bloc 5/5 USA,
 maximin-Draw), Haiti (bloc 5/5 SCO, maximin-Draw), Ecuador (model-pick, market+bloc on CIV). **X2 usage:**
 Alexandre +115 on NL-Japan DRAW (field-thin, reward 115); Nicolas & Bertrand BOTH wasted it on Germany lock
 (+15). Bonuses are all modal-iconic (downstream of outcome hit-rate). #1 is a runaway (legit 11/16) → race
 is for the 2nd slot (catch Nicolas 658). DON'T retro-fit a rival model on 16 feeling-based matches — these
 are the robust structural reads only.
**PENDING (ask user):** (1) **updated friends-league leaderboard after MD2** (standing likely dropped after 0/4); (2) MD3 reward tables + fresh Winamax/Polymarket (PM pull now MANDATORY — see CLAUDE.md).
**CROWD REFIT FIRED (2026-06-16, 16 obs ≥ 15 gate):** in-sample grid moved **sal_strength 1.0→0.75** (beta held 1.0); loss 0.0356→0.0311. BUT form STILL structurally misfit — 6/16 obs violate post-refit, BOTH directions (Mexico/Korea 1-0,2-1 under; Haiti/Germany/NL/Ecuador over). The 3 new MD2 obs (Bel 1-1, Saudi 1-1, Iran 2-2) all fit OK. **Near-irrelevant to picks** under BONUS_MODE='coarse' (score = modal within outcome). Honest read: `plaus^β × salience` cannot fit heterogeneous herding; needs richer form (per-score-type) — DON'T trust crowd-tier magnitudes. NB the script auto-refits in-sample without OOS validation (the doctrine wanted OOS too) — kept since it's marginal & coarse mode ignores it.
**OPEN LOOSE ENDS:** (1) Blend weight ½/½ unvalidated. (2) Crowd model 16 obs / 6 violations — refit fired but misfit persists (see above). 0-0 (Spain-CV +50, est 17.8% OK) + Sweden 5-1 +100 (est 0.2% OK) + Iran 2-2 +50 (est 11.8% OK) = tier-50/tail estimates holding; draw-iconic 1-1/2-2 high-tier obs all OK at current params.

## CHALLENGE AGENDA — stress-test assumptions as evidence accumulates; surface proactively at each trigger
**1. Crowd model refit — FIRED 2026-06-16 at 16 obs (sal 1.0→0.75, beta held 1.0; loss 0.0356→0.0311)**
Still 6/16 violations post-refit, BOTH directions → confirms `plausibility^β × salience` CANNOT structurally
fit heterogeneous herding. NEXT STEP (open): test a richer form (per-score-type effects) vs accept the misfit
and rely on coarse/modal scoring (current deployed stance — fine params barely affect picks). Persistent
failure modes: Mexico 2-0 / Korea 2-1 under-estimated (favourite-win iconic); Ecuador 1-0 / Germany 7-1 /
NL 2-2 over. Refit is in-sample only (no OOS gate in script) — treat magnitudes as soft.

**2. Blend weight ½/½ model-market — trigger: ~30-40 match results on ledger**
Currently a prior, not fit. Method: per-match log-loss of v6 / market / blend on running results ledger.
Flag if ledger shows consistent direction (toward 0.4/0.6 or 0.3/0.7). Report range + robust vs fragile
conclusions. Note: ~100 WC matches won't tightly identify weight (need ~500); stay honest about CI width.

**3. Outcome selector ledger — trigger: ≥15 contested flips (currently ~10)**
2-2 so far (Korea/Brazil-Draw correct; USA/Haiti wrong). At 15+: adjudicate v6 vs market vs maximin vs LEAGUE.
No strategy change before threshold regardless of small-sample noise.

**4. v6 overrating audit — trigger: ongoing, flag per match**
Ecuador confirmed overrated (CIV 1-0). As more flagged teams resolve, update the diagnostic and blend weight
reasoning. Do NOT refit engine mid-tournament.

**5. #1 hit-rate tracking — trigger: each matchday**
Now 11/16 = 69% (was 10/12 = 83%; leader took only +1 winner in MD2 → the draw cluster hammered HIM too, not
just us). Still high but the draw-fest compressed the field. Relevant for variance mode if trailing late.

**6. ⚠ DRAW-CLUSTER FLAG (new 2026-06-16) — HYPOTHESIS ONLY, do NOT refit**
MD2 went 4/4 DRAWS (Belgium 1-1, Saudi-Uru 1-1, Iran 2-2, Spain 0-0). P(4/4 | ~27% each, indep) ≈ 0.5% — very
unlikely as pure independent variance. Common factor: **all 4 were OPENING matches** for those teams (first
group game). Hypothesis: opening-round caution inflates draws AND the field over-picks favourites in openers →
Draw is systematically field-underpriced in opening matches = potential free-differentiation EV. Overall draw
rate 8/16 = 50% (MD1 was a normal 4/12 = 33%; MD2 is the outlier). **Status: WATCH, do not act.** Verify-Std #6/#7
(no refit on small samples, don't over-conclude when info arrives fast). Runway is limited anyway — only ~8 first-
round matches remain (24 opening matches total, 16 played). If the next few openers keep drawing, quantify a small
opening-match draw overlay; until then EV-max favourites stand.
## ═══════════════════════════════════════════════════════════════════════════════════════════

**Last scanned: 2026-06-16.** Update this every model run (see CLAUDE.md → "Model-blind scan").
**Scan 2026-06-16 (MD3: France-Senegal, Iraq-Norway, Argentina-Algeria, Austria-Jordan, Portugal-DRCongo — REAL WC Group I + Arg opener):**
 France full strength (Ekitiké out=depth, Saliba minor knock but available; XI Mbappé/Dembélé/Olise). Senegal strong (Mané/Koulibaly/Mendy/Gueye), no June injury. **Argentina: real defensive thinning for the opener — Dibu Martínez (GK, finger fracture) doubt, Molina+Montiel (RBs) muscle tears, Balerdi OUT; Messi/Álvarez/Romero fit → mild DEF overlay −0.05 (halved, priced; Arg still 80% fav).** Norway full strength (Haaland fit). Portugal full strength (Ronaldo's March hamstring healed). Austria/Jordan: light scan (blowout). All other teams no material overlay. **INDEPENDENT MARKET = Kalshi 1X2 (x-checked bet365), entered as market=[H,D,A]** (no Polymarket slugs) — flipped Iraq-Norway (Norway 80% mkt) & auto-vetoed Austria's Jordan (mkt 11% vs model 21%).
**XI check 2026-06-15 (pre-KO, all 3 MD2 matches — NO change):** Belgium XI CONFIRMED (Courtois + Doku start, scare cleared; Ngoy/Mechele depth CBs = ignore; Egypt Salah starts = overlay already applied). Saudi-Uruguay + Iran-NZ still PREDICTED (sheets drop ~KO) but no surprise: **Uruguay near-full-strength (Valverde/Bentancur/Ugarte/Núñez/Viñas) — NOT resting starters → pick STRENGTHENED**; Iran expected XI (Taremi leads, Jahanbakhsh out per overlay). No outcome flip on any → Belgium 1-0 / Uruguay 0-1 / Iran 1-0 all HOLD. X2 HELD.
**Scan 2026-06-15 (MD2 slate Belgium/Saudi/Iran):** Belgium–Egypt: Egypt **Salah (hamstring) starting but not fully fit** → mild Egypt ATT −0.07 (halved, market-priced); Belgium Debast (CB) out = squad depth, ignore; Doku breathing scare, returned/fit. Saudi–Uruguay: Uruguay near full-strength; Saudi new coach (Renard sacked April), poor form — intangible, NO overlay. Iran–NZ: Iran missing **Jahanbakhsh (muscle) + Eckert + Torabi** → mild Iran ATT −0.05 (halved); NZ fully fit (Wood back since April). All overlays run WITH the market (no illusory value). PICKS: Belgium 1-0 / Uruguay 0-1 / Iran 1-0 — all EV-max favourites; Iran = free differentiation (field over-picks Draw 44%). X2 HELD.
**Scan 2026-06-14:** CIV Ndicka (starting CB) OUT for opener → mild CIV DEF downgrade, supports Ecuador/over (NOT applied as overlay — would compound the flagged Ecuador outcome-overrating; noted as qualitative de-risk only). Japan on 6-win streak (beat Brazil, England) = post-cutoff form aligned with our contrarian Japan lean. NL Verbruggen fit, Timber out (already in overlay). No score changes.
The deployed model (v6) is fit on historical data and is BLIND to: injuries, suspensions,
lineups, and results after the data cutoff. This file is the manual overlay layer.

## Results log
| Date | Match | Score | vs model | Notes |
|------|-------|-------|----------|-------|
| 2026-06-11 | Mexico 2–0 South Africa | Mexico W | consistent (model 73%) | 3 red cards (1 Mex, 2 RSA) |
| 2026-06-11 | South Korea 2–1 Czechia | Korea W | consistent (model 41%; contrarian value pick hit) | Korea comeback |
| 2026-06-14 | Germany 7–1 Curaçao | Germany W | consistent (blowout; model favoured Germany heavily) | historic scoreline; tier +100 |
| 2026-06-14 | Netherlands 2–2 Japan | Draw | MISS — model picked Japan W; market NL → we picked Japan (LEAGUE) | iconic draw; tier +20 |
| 2026-06-14 | Côte d'Ivoire 1–0 Ecuador | CIV W | MISS — we picked Ecuador W (4-source model flag; Ecuador overrated confirmed) | tier +30 |
| 2026-06-14 | Sweden 5–1 Tunisia | Sweden W | consistent (model+market favoured Sweden) | score missed (1-0 pick); tier **+100** (5-1, model est 0.2% OK) |
| 2026-06-15 | Spain 0–0 Cape Verde | Draw | **MAJOR UPSET** — model 93% Spain, market agreed; pick Spain 3-0 → base 0 | irreducible upset variance, NOT a model error (both sources lock Spain); 0-0 tier **+50** = FIRST DIRECT 0-0 obs |
| 2026-06-15 | Belgium 1–1 Egypt | Draw | MISS — pick Belgium 1-0 (model 61% ≈ reward 53%) → base 0 | favourite drawn; 1-1 tier **+20** obs#14 (model est 67% OK) |
| 2026-06-15 | Saudi Arabia 1–1 Uruguay | Draw | MISS — pick Uruguay 0-1 (model 67% ≈ reward 57%) → base 0 | favourite drawn; 1-1 tier **+20** obs#15 (model est 67% OK) |
| 2026-06-15 | Iran 2–2 New Zealand | Draw | MISS — pick Iran 1-0 (model+free-diff vs field's Draw 44%) → base 0; **the field's Draw was right** | favourite drawn; 2-2 tier **+50** obs#16 (model est 11.8% OK) |
| 2026-06-16 | France 3–1 Senegal | France W | MISS — pick Draw 0-0 (Axis-B decorrelation, field 9%) → base 0; favourite WON | 3-1 tier **+30** obs#19 (model est 8.8%, VIOLATED — under-est draw-side score herding) |
| 2026-06-16 | Iraq 1–4 Norway | Norway W | **HIT** — pick Norway 0-2 (Axis-A: flipped to Kalshi 80% Norway) → base ✅, score missed | flip vindicated, Norway won big; 1-4 tier **+70** obs#17 (model est 0.9% OK) |
| 2026-06-16 | Argentina 3–0 Algeria | Argentina W | **HIT** — pick Argentina 2-0 (Axis-A follow) → base ✅, score missed | 3-0 tier **+50** obs#18 (model est 12.4% OK) |
| 2026-06-16 | Austria 3–1 Jordan | Austria W | MISS — pick Draw 0-0 (Axis-B, Kalshi-vetoed Jordan, field 14%) → base 0; favourite WON | 3-1 tier **+50** obs#20 (model est 8.4% OK) |
| 2026-06-16 | Portugal 1–1 DR Congo | Draw | MISS — pick Portugal 2-0 (MD3 #5, Axis-A follow) → base 0; favourite drawn | 1-1 tier **+20** obs#23 |
| 2026-06-17 | Ghana 1–0 Panama | Ghana W | MISS — pick Panama 0-1 (Axis-B decorrelation) → base 0; **MODEL ARTIFACT CONFIRMED** — Ghana won as market said (v6 had Panama 63%) | 1-0 tier **+20** obs#21; market-veto vindicated |
| 2026-06-17 | Uzbekistan 1–3 Colombia | Colombia W | **HIT** — pick Colombia 0-1 (follow chalk) → base ✅ (+44), score missed | 1-3 tier **+50** obs#22 |
| 2026-06-17 | England 4–2 Croatia | England W | **HIT** — pick England 1-0 (OVERRODE engine's Axis-B Draw) → base ✅ (+59), score missed; **override vindicated** | 4-2 tier **+70** obs#24 (model est 0.7% OK) |

## Pick performance (points game: base reward + rarity bonus, X2 held)
| Match | Outcome pick | Score submitted | Result | Base pts | Rarity bonus |
|-------|--------------|-----------------|--------|----------|--------------|
| Mexico–S.Africa | Mexico | 2–0 | 2–0 | ✅ 49 | **+20** (>30% crowd — obs #1) |
| S.Korea–Czechia | South Korea | 1–0 (as recommended) | 2–1 | ✅ 96 | — (score missed) |
| Canada–Bosnia | Canada | 3–0 | **1–1** | ❌ 0 | tier(1-1)=+20 obs#3 |
| USA–Paraguay | Draw | 0–0 | **4–1** | ❌ 0 | tier(4-1)=+100 obs#4 (first tail obs!) |
| Qatar–Switzerland | Switzerland | 0–3 | SUBMITTED | | |
| Brazil–Morocco | **Draw** | **0–0** | HORIZON | | EV-max; Morocco was a small-EV-sacrifice diff, wrong for 100-match horizon |
| Haiti–Scotland | **Draw** | **0–0** | REVISED (league) | | was Scotland 1-3 |
| Germany–Curaçao | Germany | **4–0** | AUDIT | | score fixed 5-0→4-0 (de-rarified) |
| Australia–Turkey | Turkey | **0–2** | AUDIT | | score fixed 1-3→0-2 (de-rarified) |
| Netherlands–Japan | **Japan** | **0–2** | REVISED (league) | | was Draw 0-0 |
| Ivory Coast–Ecuador | Ecuador | 0–1 | **1-0 CIV ❌** | 0 | tier(1-0)=+30 obs#11 |
| Germany–Curaçao | Germany | 4–0 | **7-1 GER ✅** | base (ask reward) | tier(7-1)=+100 obs#9; score missed |
| Netherlands–Japan | Japan | 0–2 | **2-2 ❌** | 0 | tier(2-2)=+20 obs#10; outcome missed (draw) |
| Sweden–Tunisia | **Sweden** | **1–0** | **5-1 SWE ✅** | 72 | score missed; tier(5-1)=**+100** obs#13 (model est 0.2% OK) |
| Spain–Cape Verde | Spain | 3–0 | **0-0 DRAW ❌** | 0 | major upset (Spain 93%); tier(0-0)=+50 obs#12 — FIRST DIRECT 0-0, validates tier-50 thesis |
| Belgium–Egypt | Belgium | 1–0 | **1-1 DRAW ❌** | 0 | favourite drawn; tier(1-1)=+20 obs#14 |
| Saudi Arabia–Uruguay | Uruguay | 0–1 | **1-1 DRAW ❌** | 0 | favourite drawn; tier(1-1)=+20 obs#15 |
| Iran–New Zealand | Iran | 1–0 | **2-2 DRAW ❌** | 0 | favourite drawn; field's Draw (44%) was right; tier(2-2)=+50 obs#16 |
| France–Senegal | **Draw** | **0–0** | MD3 SUBMITTED | | Axis-B: France blend-EV-max 28.8 but Draw 28.3 within band & far less crowded (9% vs 88%) → decorrelate. Kalshi mkt 66/21/13 |
| Iraq–Norway | **Norway** | **0–2** | MD3 SUBMITTED | | Axis-A: Kalshi mkt Norway 80% (model 73 under) → Norway blend-EV-max 23.2 > Draw 21.0. FLIPPED from draft-draw (model overrated draw) |
| Argentina–Algeria | Argentina | 2–0 | MD3 SUBMITTED | | Axis-A follow (blend-EV-max 31.0); DEF overlay −0.05 (Dibu/Molina/Montiel/Balerdi) |
| Austria–Jordan | **Draw** | **0–0** | MD3 SUBMITTED | | Axis-B: Draw blend-EV-max 26.1; Kalshi demoted Jordan to 11% (model 21 overrated) → auto-veto. Field 14% |
| Portugal–DR Congo | Portugal | 2–0 | MD3 SUBMITTED | | Axis-A follow (blend-EV-max 25.5; mkt≈model; draw separation negative) |
| England–Croatia | England | 1–0 | MD4 SUBMITTED | | FOLLOW (override engine Axis-B Draw; field draw-herds 39%) |
| Ghana–Panama | **Panama** | **0–1** | MD4 SUBMITTED | | **AXIS-B decorrelation** (field 7%); MODEL ARTIFACT (v6 Panama 63 vs mkt 28) — even-EV on market, real sep |
| Uzbekistan–Colombia | Colombia | 0–1 | MD4 SUBMITTED | | FOLLOW chalk (model=market 12/21/67); field 89% |
| Czechia–South Africa | Czechia | 1–0 | MD4 SUBMITTED | | FOLLOW (blendEV 34.7); both lost openers |
| Switzerland–Bosnia | Switzerland | 2–0 | MD4 SUBMITTED | | FOLLOW (blendEV 49.8); field 70%; X2 HELD (correlated) |
| Canada–Qatar | Canada | 2–0 | MD5 SUBMITTED | | FOLLOW chalk (blendEV 53.9; alts <16% out of band) |
| Mexico–South Korea | **Draw** | **1–1** | MD5 SUBMITTED | | Engine Axis-B differentiation (in-band, less crowded than Mexico). Montes(Mex CB) susp. NOT my Mexico/Korea overrides (reverted to doctrine) |

**REVISED 2026-06-13 under LEAGUE objective (picks unlocked):** 4 maximin draws dismantled → differentiated
+EV picks (Morocco/Japan = field-underpicked EV-competitive; Haiti-Draw = EV-max 9%-field; Sweden = EV-max
fav, draw was −3.8EV hedge). Principle: separate via outcome when underpicked side is +EV, else via rare
score. Engine now LEAGUE_MODE (matchday.py, DIFF_BAND=2.0). X2 still HELD (Ecuador E=50.6 flagged but
single-model-source contested — not used yet).

**Running total: 165 pts (145 base + 20 bonus).**
**NB:** realized bonus tiers are observable even for scores we didn't pick (obs #2 = Korea 2–1 earned +20 for whoever had it → >30% crowd). User to report the realized tier of EVERY played match → ~1 calibration obs per match.
**Crowd calibration:** obs #2 VIOLATED the prior (est 26.8% vs realized >30%) → early refit: **beta 1.25→1.6, sal_strength 1.0→1.5** (crowd herds harder on iconic scores than assumed). Post-refit: Mexico OK (35.2%), Korea 29.0% — still 1pt below band edge; coarse-grid residual, expect resolution at obs #3. Strategic effect: iconic scores even MORE crowded → rare-score arbitrage (3-0/3-1 type, 50/70 tiers) STRONGER.
**12 obs / 6 violations (2026-06-15):** model structurally misfit; params beta/sal near-unidentified. Notable new obs: Germany 7-1 → +100 (ultra-rare, model est 0.7% barely violates 0.5% ceiling); NL-Japan 2-2 → +20 (crowd herds hard on 2-2, model est only 17.4% vs >30% — draw iconic scores under-estimated); CIV-Ecuador 1-0 → +30 (model over-estimated 1-0 home win herding, 41.9% vs 20-30% actual). Pattern: draw scores (1-1, 2-2) dramatically under-estimated by model; home-win 1-0 over-estimated. Refit GATED to 15 obs.
**★ FIRST DIRECT 0-0 OBSERVATION (Spain-Cape Verde, obs#12, 2026-06-15):** 0-0 realized +50 (5-20% among Draw-pickers); model est 17.8% → **OK, inside band**. The 0-0 under-picking edge was INFERRED until now (zero direct obs, demoted 2026-06-12); this is its FIRST direct support — confirms 0-0 sits at tier-50 with our p-estimate well-calibrated, vindicating the MD1 0-0-cluster tier-50 assumption. NB single obs (Verify-Std #7): one point, not a validated finding — but it points the right way (unlike the iconic-draw 1-1/2-2 under-estimates). Note 0-0 here ALSO fits the "draws under-picked by crowd" pattern but model p was accurate, so no violation.

**X2 status: HELD** (usable anytime incl. KO — bar raised accordingly). Candidates auto-flagged by `matchday.py`.
**Standing (2026-06-12):** ~230,000th / >1M with 2nd-best-possible score (165) → top is dense; rare-score
bonuses = primary climbing instrument (VAR_TIEBREAK active). 1st ex-aequo (of 4) in friends league.
**Obs#2 provenance confirmed:** organizer email (first-party). Crowd params beta=1.6/sal=1.5 de-flagged.

## MD1 counterfactual selector ledger (pre-committed 2026-06-12 — score all three as results land)
| Match | pure-v6 pick | pure-market pick | SUBMITTED (maximin) | RESULT |
|-------|--------------|------------------|---------------------|--------|
| Canada–Bosnia | Canada | Canada | Canada | → **1-1: all 3 WRONG** (Canada upset draw, no differentiation) |
| USA–Paraguay | Paraguay | USA | Draw | → **4-1: MARKET RIGHT, v6+maximin WRONG** (USA blowout — contested flip, market wins R1) |
| Qatar–Suisse | Switzerland | Switzerland | Switzerland |
| Brazil–Morocco | Morocco | Brazil | Draw |
| Haiti–Scotland | Scotland | Draw | Scotland |
| Germany–Curaçao | Germany | Germany | Germany | → **7-1: all 3 CORRECT on outcome** (Germany blowout) |
| Australia–Turkey | Turkey | Turkey | Turkey | → **2-0 AUS: all 3 WRONG** (Turkey was model+market pick, upset) |
| NL–Japan | Japan | Netherlands | Draw | → **2-2: Draw CORRECT, v6+market WRONG** (maximin wins R2) |
| CIV–Ecuador | Ecuador | Draw | Ecuador | → **1-0 CIV: market(Draw) closest; v6+submitted(Ecuador) WRONG** |
| Sweden–Tunisia | Tunisia | Sweden | Draw | → **5-1: market(Sweden) CORRECT; v6+maximin WRONG** (Sweden blowout) |

**Pre-commitments:** (1) NO parameter/strategy change on any single result; ledger adjudicates selectors
at ~15+ matches. (2) Tiers update crowd model only; results update ledger only. (3) Overlay errors
(e.g. Neymar plays) attribute to the OVERLAY layer, not the engine. (4) RESOLVED 2026-06-12: rules confirmed — bonus population = "% of players among those who got the
match winner right", NO temporal condition (tier model correctly specified). Tiers CONFIRMED accessible
for all matches (uncensored calibration stream). Both test-invalidators eliminated.

## Suspensions (model-blind, single-match)
| Player | Team | Misses | Model impact |
|--------|------|--------|--------------|
| **César Montes** | Mexico | vs South Korea (MD2) | starting CB out → Mexico DEF weaker THAT match (overlay −0.10 DEF) |
| Themba Zwane | South Africa | vs Czechia (MD2) | key attacking mid → RSA ATT weaker (−0.10 ATT) |
| Sphephelo Sithole | South Africa | vs Czechia (MD2) | midfielder (−0.05) |

## Injuries (model-blind, tournament-long) — DISCOUNT model "value" on these teams
| Team | Out | Severity | Overlay (ATT/DEF in log units; DEF higher=better) |
|------|-----|----------|---------------------------------------------------|
| Brazil | Rodrygo (ACL), Militão, Estêvão | moderate | −0.10 ATT, −0.08 DEF |
| Netherlands | Xavi Simons (ACL), De Ligt, Timber | moderate | −0.08 ATT, −0.10 DEF |
| Japan | Mitoma (hamstring) | significant | −0.12 ATT |
| Canada | Marcelo Flores (ACL) | minor | −0.05 ATT |
| France | Ekitiké | negligible | none (squad depth) |
| Germany | Gnabry, Karl | negligible | none |

## Overlay guidance (conservative — judgment, NOT a fitted model; player-leg failed validation)
- Key attacker out → −0.10 to −0.15 team ATT. Key defender/keeper out → reduce team DEF 0.08–0.12.
- Rotation/squad player → ignore.
- **Halve the overlay if the market / reward table already moved** (pre-tournament injuries are mostly
  priced in; in-tournament suspensions are usually priced by the game-maker too).
- Core use: when comparing model vs a reward table, an apparent model "value" on an injury-hit team may
  just be model-blindness — discount it.
