# FIFA World Cup 2026 — Points-Game Predictions (fork of v6)

**Objective forked.** The v1–v6 model optimised *calibration* (honest probabilities).
This fork optimises *expected points* in a reward game where correct picks score, and
risky (less likely) outcomes pay more.

**Method.** The rewards encode the game-maker's implied probabilities: `reward ≈ C / p_implied`,
so `p_implied ∝ 1/reward` (normalised). With a *calibrated* model, the optimal pick maximises
**expected points = p_model × reward**. Equivalently: bet the outcome where my probability most
exceeds the game's implied probability (**edge = p_model / p_implied > 1**). This is why the
session's calibration work matters — EV is only trustworthy if `p_model ≈ p_true`.

Engine: v6 (2-D attack/defence on goals+xG → negative-binomial scoreline → supremacy
recalibration γ=1.5). Validated out-of-sample; favourite-win frequencies are calibrated.

---

**Format:** accumulate points while competing against a field. Scoring: correct result =
base reward; **exact score = double** (assumed Rule A — predicting a score keeps the base
points on a correct result and adds the bonus on an exact hit; confirm if it's actually
"exact-or-nothing").

## Picks (maximise expected points)

| Match | **OUTCOME pick** | Model | Implied | Reward | Exp.pts | Edge | **Score to predict (the double)** |
|-------|------------------|-------|---------|--------|---------|------|-----------------------------------|
| Mexico vs South Africa | **Mexico** | 72.9% | 58.0% | 49 | 35.7 | 1.26 | **2–0** (or 1–0), ~15% |
| South Korea vs Czech Rep. | **South Korea** | 41.1% | 33.9% | 96 | 39.4 | 1.21 | **1–0**, ~10% ⚠ contrarian |
| Canada vs Bosnia & Herz. | **Canada** | 62.0% | 48.2% | 65 | 40.3 | 1.29 | **1–0** (or 2–0), ~15% |

Under Rule A the outcome pick is unchanged by the doubling — you append the most-likely
scoreline *within* your chosen outcome to harvest the bonus for free. **Total expected base
points ≈ 115**, plus exact-score upside.

### Why not the "risky" high-reward outcomes
The reward scheme tempts you toward South Africa (148) and Bosnia (125), but the model's
probabilities don't justify them: South Africa EV 12.8 vs Mexico 35.7. **Risk only pays when
your probability beats the implied price — and here it doesn't for the underdogs.** The value
is in the chalk being underpriced, not in the long shots.

### The one bet against the house
**Korea–Czech** is the genuine edge play: the game prices Czechia as the slight favourite
(reward 91 < 96), but my model has **Korea ahead, 41% vs 34%**. If the model is right, this is
the highest-value disagreement on the board.

---

## Strategy for a field competition

1. **Edge is the steady weapon.** The field picks by gut and leans favourites; a calibrated model
   that takes the best-EV side every match compounds a small per-game edge into a higher total
   over 72 games. Apply the EV-optimal outcome consistently — that's how you out-accumulate.
2. **The exact-score double is the separator.** Matching the field's EV won't *win* a leaderboard.
   At ~15% per favourite-mismatch you'll nail several scorelines across the tournament — each one
   doubles while winner-only players get base. That's where you pull ahead. Under Rule A it's free,
   so always submit a scoreline.
3. **Variance is a function of your standing (dynamic):**
   - *Mid-tournament / level:* pure EV-max (these picks).
   - *Trailing late:* deliberately take +variance with positive edge — value underdogs, draws,
     lower-probability exact scores — to leapfrog. Tell me you're behind and I'll re-pick for variance.
   - *Leading late:* play safe — favourites + modal scores — to protect the lead.
4. **Model-risk flag:** Mexico 72.9% vs game 58% is the biggest disagreement here. South Africa is
   genuinely weak (Elo 1517) so it's plausible, but it's where I'm most exposed if γ over-sharpens
   this specific mismatch.

## Workflow — add reward tables progressively
The model (v6) is built and frozen; each match's reward table is a ~10-second computation. **Drip-feed
matches matchday by matchday** — that's actually better (fresher, effort only on games you're playing).
Matches without a reward table still have a straight prediction in `PREDICTIONS_v6.md`; the reward
table just upgrades them to value-optimised picks.

---

# MD1 full slate — submitted picks (computed 2026-06-12, engine v6 + crowd/rarity layer)

| # | Match (date) | OUTCOME | SCORE | Rationale (1-line) |
|---|--------------|---------|-------|--------------------|
| 1 | Canada–Bosnia (12th) | **Canada** | **3-0** | model+market agree; rare-tilt over 2-0 (crowd 6% vs 27%), Davies/Flores overlay in |
| 2 | USA–Paraguay (12th) | **Draw** | **0-0** | model says PAR, market says USA → maximin = Draw; 0-0: p13%, crowd 13%, tier 50 all scenarios (Eb 6.5, best cell of slate) |
| 3 | Qatar–Switzerland (13th) | **Switzerland** | **0-3** | consensus pick; 0-4 was model-hot (div 1.54, fat-tail zone) → alt per protocol |
| 4 | Brazil–Morocco (13th) | **Draw** | **0-0** | Neymar doubt+Rodrygo out vs Aguerd out; model MAR / market BRA → maximin Draw; 0-0 tier 50 |
| 5 | Haiti–Scotland (13th) | **Scotland** | **1-3** | 3-way EV tie; Scotland = stable on both sources (62% hit), 1-3 rare (crowd 4%, tier 50-70) |
| 6 | Germany–Curaçao (14th) | **Germany** | **5-0** | chalk worth 15 pts only → value lives in the score; 5-0 p8%, crowd 2%, tier 70 |
| 7 | Australia–Turkey (14th) | **Turkey** | **1-3** | both sources Turkey; 1-3 rare-tilt survives pessimistic guard |
| 8 | Netherlands–Japan (14th) | **Draw** | **0-0** | both attacks injury-gutted; model JPN / market NL → maximin Draw |
| 9 | Ivory Coast–Ecuador (14th) | **Ecuador** | **0-2** | 4-source Ecuador-hot flag, BUT Ecuador is maximin-robust anyway (market-EV 33.7 ≈ best); X2 NOT used |
| 10 | Sweden–Tunisia (14th) | **Draw** | **0-0** | model TUN / market SWE → maximin Draw; 0-0 p~10%, tier 50 |

**X2: HELD.** Flagged candidates (Paraguay 54.3, Ecuador 50.6) are model-conviction plays the market
disputes — policy requires both-source-positive EV. No qualifying spot yet.

**The 0-0 cluster (4 picks) is deliberate:** the prono crowd under-picks 0-0 (confirmed salience bias),
locking it at tier +50 with p≈9–13% per match — the single most reliable rarity arbitrage we hold.
Across 4 matches: ~40% chance at least one lands (+50 each), every draw also pays base 110–122.

*Next inputs: realized TIERS from organizer emails (every match, esp. rare scores); fresh Winamax pull
+ 1N2 odds next matchday; rank updates.*

---

# MD2 slate 2026-06-15 (engine v6 + LEAGUE_MODE, DIFF_BAND=0, BONUS_MODE=coarse)

User 9th/13 (374 pts), ~92 matches left → EV-max regime, X2 HELD. Winamax 20260615 ingested; preflight GREEN.
Model & reward-implied market AGREE on the favourite in all 4 → picks market-robust (no Polymarket pull this slate).

| # | Match (date) | OUTCOME | SCORE | Rationale (1-line) |
|---|--------------|---------|-------|--------------------|
| 1 | Belgium–Egypt (15th) | **Belgium** | **1-0** | EV-max (totalEV 39.6); model 61% ≈ reward 53%; Salah half-fit overlay reinforces; 1-0 modal (coarse) — div flag noted, kept per rule |
| 2 | Saudi Arabia–Uruguay (15th) | **Uruguay** | **0-1** | EV-max (totalEV 39.9); model 67% ≈ reward 57%; field 81% (crowded, no diff available — take EV-max anyway); 0-1 modal |
| 3 | Iran–New Zealand (15th) | **Iran** | **1-0** | EV-max (totalEV 40.7) AND FREE differentiation: field over-picks Draw (44%) vs Iran 35%; 1-0 modal (model over-rates 1-0 herding → tier likely better than shown) |
| 4 | Spain–Cape Verde (15th) | **Spain** | **3-0** | model 93/6/2 near-lock; EV low (20.4 — 16 reward, heavy-fav fair-game) so value is in the bonus; 3-0 modal (xG 3.95-0.33), tier 50 stable. Yamal+N.Williams benched (token overlay). Score grid = 6/12 early money; rewards 16/166/217, field 88/10/2 (user supplied late). |

**BLEND ROBUSTNESS (no Polymarket this slate):** re-ran each pick with reward-implied market as the blend term (½ model + ½ reward-implied) → **outcome argmax UNCHANGED in all 4** (Bel H, Uru A, Iran H, Spa H). Blend narrows margins (Uru 33.5→31.1, Iran 37.8→34.4) but flips nothing. Picks robust to the missing PM layer; for future slates pull `fetch_pm_matches.py` so the deployed blend actually engages.

**X2: HELD.** No candidate (max E_total 40.7 < 45 threshold; all favourites, none contrarian). Reserve for high-E knockout where model+market agree.

*Pending from user: realized TIERS for the 6/14 matches + Sweden-Tunisia 5-1 tier (calibration backlog → 13 obs, refit gated at 15); results of these 3.*

---

# MD3 slate 2026-06-16 (engine v6 + LEAGUE_MODE, DIFF_BAND_FRAC=0.05, blend 0.4/0.6, COARSE) — FIRST slate under the AUDIT-corrected two-axis doctrine

User #10/13 (374), gap 284 to #2 line (658), ~88 left → behind ⇒ DECORRELATE where +EV. Preflight GREEN; Winamax 20260616 ingested. **Real WC: Group I openers + Arg-Alg opener.**
**INDEPENDENT MARKET = Kalshi 1X2 (x-checked bet365), entered as `market=[H,D,A]`. Blend = 0.4 model + 0.6 market; veto functions.** [REVISED from a reward-implied-only draft — user correctly rejected running without an independent market; the Kalshi line FLIPPED Iraq-Norway and cleaned up Austria.]
**TWO-MARKET CROSS-CHECK (Winamax 1X2 derived from the score grid the user supplied):** WMX France 60/24/16, Iraq-Nor 10/16/74, Arg 63/23/14, Aut-Jor 65/21/15, Por 70/19/11. Winamax reads the DRAW & UNDERDOG systematically higher (French-public longshot/0-0 bias — the two-population effect) → weight Kalshi/bet365 more for favourite magnitude. Picks UNCHANGED. Closest call = Iraq-Norway (WMX+model ~74% Norway vs Kalshi/bet365 ~80%; stay Norway — model under-rates a strong fav vs weak debutant). Winamax STRENGTHENS France-draw (24%).

| # | Match | OUTCOME | SCORE | Rationale (two-axis, blend 0.4/0.6 w/ Kalshi market) |
|---|-------|---------|-------|----------------------|
| 1 | France–Senegal | **Draw** | **0-0** | AXIS-B: France is blend-EV-max (28.8) but Draw (28.3) is within 5% band & far less crowded (9% vs 88%) → take Draw, ~free decorrelation. Market draw 21%≈model 24%, confirmed. |
| 2 | Iraq–Norway | **Norway** | **0-2** | AXIS-A follow: market says Norway 80% (model 73% UNDER) → Draw is NOT EV-max; Norway blend-EV-max (23.2 > Draw 21.0). FLIPPED from the reward-implied draft's draw. Crowded (91%) but +EV; no Axis-B here. |
| 3 | Argentina–Algeria | **Argentina** | **2-0** | AXIS-A follow: Argentina blend-EV-max (31.0). DEF overlay −0.05 (Dibu/Molina/Montiel/Balerdi out, halved/priced). No +EV Axis-B (draw 23.7 << 31.0). |
| 4 | Austria–Jordan | **Draw** | **0-0** | AXIS-B: Draw is now blend-EV-max (26.1) — market demoted Jordan to 11% (model 21% = overrated, Ecuador-style), so the market auto-vetoed it. Draw field-underpicked (14%), confirmed (17%≈22%). |
| 5 | Portugal–DR Congo | **Portugal** | **2-0** | AXIS-A follow: Portugal blend-EV-max (25.5); market≈model (75/17/8); Draw (23.9) separation negative. EV-max favourite. |

**Portfolio (honest):** 2 EV-max draws (France, Austria) + 3 favourites (Norway, Argentina, Portugal). The draws are genuine Axis-B (within band, field-underpicked, market-confirmed) → free decorrelation; the favourites are where no +EV decorrelation exists (correct discipline — don't force −EV separation). Lower variance than the reward-implied draft (which wrongly had 3 draws incl. the model-overrated Iraq-Norway one). Expected base ~134.
**X2: HELD.** No candidate ≥45 (max totalEV 36.7 Argentina; all low-K crushed-chalk matches). Reserve for a higher-E field-underpicked + market-confirmed spot (more even match / knockout).

*Pending from user: realized TIERS for these 5 + the 6/14 backlog; results; updated leaderboard.*

---

# MD6 slate 2026-06-19 (engine v6 + LEAGUE_MODE, blend 0.4/0.6, COARSE) — Group C/D 2nd-round matches

User = **Lampadaire83, #12/16 @697** (climbed #14→#12, +147 via Switzerland + Canada base). Objective TOP-5, top-5 line
= #5 CrazyBE **1018, gap 321** (top herd #1–#5 = 1018–1482 with 16–17 goods, pulling away). Mid-table bunched
(#8 814 … #12 697 … #14 622). Preflight GREEN. INDEPENDENT MARKET = de-vigged DraftKings/FanDuel/BetOnline 1X2 via
WebSearch 2026-06-19. **Model-blind scan: Pulisic OUT (USA, calf) → USA ATT −0.07 halved; Brazil tourn injuries
−0.05/−0.04 halved; Paraguay Caballero+Sosa out → Paraguay ATT −0.05.**

| # | Match | OUTCOME | SCORE | Rationale (two-axis, blend 0.4/0.6) |
|---|-------|---------|-------|----------------------|
| 1 | USA–Australia | **USA** | **1-0** | **OVERRIDE engine's Australia pick** (model 28/27/45 → blend-EV-max Australia 44.1, PRIME X2 flag). This is the **documented v6 USA-UNDERRATING artifact** — same class as Ghana-Panama (artifact PRIME, ignored) & USA-Paraguay (model had PAR fav, USA won 4-1, resolved FOR market). MARKET-CONFIRMED VETO: sharp books say USA 60% / AUS 18% (post-Pulisic, post-AUS-beat-Turkey) → market does NOT support Australia. Follow market = USA. Field 75% (crowded, no separation) but disciplined. |
| 2 | Scotland–Morocco | **Morocco** | **0-1** | AXIS-A follow chalk: Morocco blend-EV-max 48.7 (model 49% ≈ market 56%). Field 79% Morocco (crowded). No Axis-B: Draw (29.9) & Scotland (19.6) far outside 5% band. |
| 3 | Brazil–Haiti | **Brazil** | **3-0** | AXIS-A follow: Brazil blend-EV-max 18.1 (model≈market 85/87). Reward only 21 (crushed chalk, field 95%) → low-EV match, everyone has it; Draw (15.4) just outside band. Modal blowout 3-0. |
| 4 | Türkiye–Paraguay | **Türkiye** | **1-0** | AXIS-A follow: Turkey blend-EV-max 40.6 (model 47 ≈ market 49). Draw field-OVER-picked (33%) = not a decorrel target; Paraguay (30.1, field 11%) outside band. Both teams lost openers (must-win). |

**Portfolio (honest):** 4 favourites, ZERO decorrelation. No high-conviction field-underpicked + market-confirmed
Axis-B spot exists on this slate (the one underpicked+long-reward spot, Australia 7%/153, is a MODEL ARTIFACT the
market fades → fails the criterion; taking it = the 0/4 aggressive-underdog trap). Disciplined all-follow. Expected
base if all hit ≈ 58+91+21+84 = 254, but the field also holds this chalk → **gains points, not rank** (the documented
tension). Top-5 (gap 321) not closable today; realistic near-term = pass bunched #8–#11 (749–814).
**X2: HELD.** The only PRIME flag (Australia, E_total 71.5, field 7%) is the USA-underrating artifact — exactly the
flag the doctrine says to IGNORE (Ghana-Panama precedent). No genuine high-reward + field-underpicked + MARKET-CONFIRMED
spot. Keep waiting.

*Pending from user: realized TIERS for these 4 + results; updated leaderboard.*

---

# MD7 slate 2026-06-20/21 (engine v6 + LEAGUE_MODE, blend 0.4/0.6, COARSE) — 8 matches, Group E/F/G/H 2nd round

User = **Lampadaire83, #9/16 @937** (jumped #12→#9, +240 via Morocco 0-1 EXACT +50, Brazil 3-0 EXACT +20, USA base 58 —
the **USA override was VINDICATED**, USA won 2-0; artifact resolved FOR market again). Objective TOP-5; line = #5 Alexis
**1232, gap 295**; cluster #2–#7 bunched 1190–1307; #8 Chocho 984 (only +47). Preflight GREEN. INDEPENDENT MARKET =
de-vigged bet365/FanDuel/DraftKings/BetOnline via WebSearch 2026-06-20.
**Model-blind scan 2026-06-20:** NL trio (Xavi Simons/De Ligt/Timber) −0.04/−0.05 halved-priced; Japan Mitoma ATT −0.06.
Fresh: Germany FULL strength (CIV Ndicka CB doubt, priced); Belgium near-full (DeBruyne/Doku/Courtois start, Lukaku bench,
Debast out=depth; Iran minor MF doubts). No new overlays — the draws stand on REWARD-MISPRICING + market, not injuries.

| # | Match | OUTCOME | SCORE | Rationale (two-axis, blend 0.4/0.6) |
|---|-------|---------|-------|----------------------|
| 1 | Netherlands–Sweden | **Netherlands** | **2-0** | FOLLOW: blend-EV-max 40.2; model 69% HOT vs market 54% (same side). Field 56%. |
| 2 | Germany–Ivory Coast | **Draw** | **1-1** | **AXIS-B = EV-MAX** (not a sacrifice): the FIXED reward line under-prices the draw — reward-implied 18% vs independent sharp market 22% (**edge 1.22**) → Draw blend-EV 29.6 > Ger 23.8 > CIV 25.7. INDEPENDENTLY field-underpicked (14%) + model-market AGREE on Ger strength (65/61). **X2 TARGET** (reward 137≥100, robust). [Rewards are FIXED, not crowd-dynamic — field% is decorrelation only.] |
| 3 | Ecuador–Curaçao | **Ecuador** | **2-0** | FOLLOW: blend-EV-max 34.9. Ecuador overrating-artifact IRRELEVANT (huge fav anyway; Curaçao conceded 7 to Germany). Field 81%. |
| 4 | Tunisia–Japan | **Japan** | **0-1** | FOLLOW: blend-EV-max 58.9. Japan chalk (field 71%). Mitoma overlay applied. Tunisia sacked coach (Renard interim). |
| 5 | Spain–Saudi Arabia | **Spain** | **3-0** | FOLLOW: blend-EV-max 27.7. Crushed chalk (field 94%, reward 31). Spain drew CV last (upset risk) but market 87%. Low value, no separation available. |
| 6 | Belgium–Iran | **Draw** | **1-1** | **AXIS-B** (OVERRIDE engine's Iran): Draw blend-EV 29.8 = highest; engine tie-broke to Iran (2% field) but Iran market-UNCONFIRMED (13%) → market veto. Draw market-confirmed (20%), field-underpicked (8%), ~0 EV cost. But only **edge 1.07** (fixed line barely under-prices the draw here) and Belgium likely underrated (model 52 vs mkt 67) → MARGINAL → take Draw but **NOT X2**. |
| 7 | Uruguay–Cape Verde | **Uruguay** | **1-0** | FOLLOW: blend-EV-max 47.0. Strong fav (field 76%). |
| 8 | New Zealand–Egypt | **Egypt** | **0-1** | FOLLOW (OVERRIDE engine's NZ): engine tie-broke to NZ (9% field) but NZ only IN-BAND not EV-max (Egypt 31.8 > NZ 30.7) AND market-unconfirmed (18%, NZ lowest-ranked team 85th vs Salah/Egypt unbeaten) → raised-bar + veto reject it. Egypt EV-max follow. Crushed chalk (field 70%, reward 59), no separation. |

**Portfolio:** 6 FOLLOWS + 2 EV-MAX DRAWS (Germany-CIV, Belgium-Iran). The draws are NOT the 0/5 sacrifice-draws — they are
EV-MAX/tied because the FIXED reward line under-prices the draw vs the independent sharp market (edge 1.22 / 1.07), AND they are
independently field-underpicked (14%/8%) → zero-EV-cost decorrelation, the correct rank-separation play for a trailing #9.
**[CORRECTION 2026-06-20: rewards are FIXED, not crowd-dynamic — my earlier "field crushed the favourite's reward" framing was
WRONG. The edge is sharp-market-vs-game-maker-line mispricing, decoupled from field%. ALSO: the fixed line is variably COMPRESSED
(Japan edge 1.67) → following calibrated favourites is genuinely +EV, overturning the old "skill earns ~0" claim. See
REPORT_2026-06-20.md.]** Two overrides reject engine tie-breaks into market-UNCONFIRMED underdogs (Iran 13%, NZ 18% — artifact class).
**X2 — HELD (user decision 2026-06-20).** Recommended Germany–CIV Draw, but user declined to deploy on the FIRST firing of a
new flag — wants to LOG both EV-max-draw spots and learn their realized hit-rate before committing the one-shot (we're <30% of
total matches in, not even half of group stage). Disciplined: validate the "reward-mispricing EV-max draw" profile across several
observations, THEN deploy the X2 on a future such spot with calibrated confidence. The 2 draw PICKS stand regardless (they're the
slate's blend-EV-max outcomes); the X2 is a separate lever. See X2-FLAG LEDGER in live_updates.md.

*Pending: realized TIERS for these 8 + results; X2 deploy confirmation; updated leaderboard.*

---

# MD8 slate 2026-06-22 (engine v6 + LEAGUE_MODE, blend 0.4/0.6, COARSE) — Group I/J FINAL group matches

User = **Lampadaire83, #8/15 @1323** (climbed #9→#8, **+386** — reconciles EXACTLY: NL 67 + Japan 91 + Spain 31 +
**Belgium-Iran DRAW 138** + Egypt 59; 5 base hits, 0 exacts; the **Axis-B reward-mispricing draw (Bel-Iran 0-0) was the
single biggest base, +138**). Objective TOP-5; **line = #5 AdyFC 1493, gap 170** — cluster #5–#8 bunched (1493/1457/1371/1323),
**top-5 genuinely reachable now** (gap was 295, now 170). Climbers still carry HIGH exacts (#2 Hadri 8, #5 AdyFC 8 vs user 3).
Preflight GREEN. INDEPENDENT MARKET = de-vigged FanDuel/DraftKings/ESPN 1X2 + Opta sim via WebSearch 2026-06-22.
**Model-blind scan 2026-06-22 (final-round group matches):** Argentina near-FULL XI (Messi starts, rested ~60' only if game
settled) → no overlay, market 62% prices it; France ROTATES but strong XI (Mbappé/Dembélé/Olise/Saliba/Upamecano/Maignan
start) → negligible, market 90% prices it; **Norway–Senegal BOTH full strength, NO injuries, both motivated (winner advances,
Senegal must-win)** → clean read; Jordan–Algeria no news. No overlays this slate.

| # | Match | OUTCOME | SCORE | Rationale (two-axis, blend 0.4/0.6) |
|---|-------|---------|-------|----------------------|
| 1 | Argentina–Austria | **Argentina** | **1-0** | FOLLOW: blend-EV-max 41.5 (model 72 ≈ mkt 62). Edge 1.29 (line under-prices Arg) but field 92% = table stakes, ZERO separation. 1-0 modal. |
| 2 | France–Iraq | **France** | **2-0** | FOLLOW: blend-EV-max 19.2. Crushed chalk (reward 22, field 98%) → low value, everyone has it, no separation. 2-0 modal. France rotates but wins. |
| 3 | Norway–Senegal | **Senegal** 🔥**X2 DEPLOYED** | **0-1** | **AXIS-A EV-MAX *and* AXIS-B both point to Senegal**: blend-EV-max 41.5 (reward 137 × live ~30% >> Norway 27.8/Draw 27.6) AND least field-crowded (25% vs Draw 42%). Market-confirmed edge **1.29** (mkt 29% vs reward-impl 22.5% — independent line lifts Senegal ABOVE the draw, NOT a model artifact). Genuine contested match, both full-strength. **X2 PRIME flag → DEPLOYED** (reward 137≥100 + field-underpicked + market-confirmed). 0-1 modal. |
| 4 | Jordan–Algeria | **Algeria** | **0-1** | FOLLOW: blend-EV-max 39.5 (model 53 ≈ mkt 63). Jordan baseEV 36.1 is the compressed-line illusion (reward 152 × low 24%/16% prob) → blend correctly demotes it. Field 77% Algeria = no separation. 0-1 modal. |

**Portfolio:** 3 FOLLOWS (Argentina, France, Algeria — all crushed/crowded chalk, points not rank) + **1 genuine rank lever
(Senegal)**. Senegal is the rare spot where EV-max and field-decorrelation ALIGN (no EV cost): it is blend-EV-max *and* the
least-crowded outcome *and* market-confirmed-above-reward-line. Exactly the field-underpicked + market-confirmed +EV underdog
the doctrine wants for a trailing #8 with a reachable top-5.
**X2 — DEPLOYED on Senegal (user decision 2026-06-22). ONE-SHOT NOW SPENT.** First clean PRIME *outcome* flag of the
tournament (high-reward 137 + field-underpicked 25% + market-confirmed edge 1.29 — the Alexandre-NL-draw-winning profile),
deployed with top-5 in range (gap 170) where a doubled Senegal win (~+280) vaults into the top 5; free if it loses (~70%).
Timing rationale (the decisive argument): the X2's RANK value = P(hit) × reward × field-underpick, and that profile is a
GROUP-STAGE creature — KO compresses rewards AND converges the field, so "wait for KO" gives a *lower*-separation spot, not a
higher one. These are the FINAL group matches → the supply of high-reward field-split underdogs is ending now. Counter logged:
~30% hit; if Senegal loses, the one-shot is gone (but EV-free). **If Senegal wins → 2× total points on a pick 75% of the field
missed = the single biggest rank lever available.**

*Pending: realized TIERS for these 4 + results; X2 deploy confirmation; updated leaderboard.*

---

# MD9 slate 2026-06-23 (engine v6 + LEAGUE_MODE, blend 0.4/0.6, COARSE) — more FINAL group matches (Groups B/K/L)

User = **Lampadaire83, #9/9-shown @1475** (DROPPED #8→#9 despite +152: Arg 63 + Fra 22 + Alg 67 = 152, 3/4 follows all chalk; **Senegal
X2 LOST** — Norway won 3-2, the ~70% branch). The drop is the doctrine's tension made concrete: **following chalk gains points but loses
rank** (the herd moves with you), and the one separation lever missed. Objective TOP-5; line = #5 CrazyBE **1633, gap 158**; cluster tight
(#6 AdyFC 1602 / #7 Ethan 1519 / #8 Cyril 1500 / user 1475). **STRUCTURAL DEFICIT = exacts: user 3 vs #2 Hadri 9, #6 AdyFC 8, #4 Alexis 7.**
Preflight GREEN (manifest intact). INDEPENDENT MARKET = de-vigged FanDuel/ESPN/BetOnline 1X2 via WebSearch 2026-06-23.
**Model-blind scan 2026-06-23:** England qualifying, may rotate but huge fav (mkt 81%) → no overlay. Croatia heavy fav + **must-win** vs
Panama (motivation headwind on the draw). Colombia unchanged, can seal qualification. **Canada: Koné (tibia) OUT + Davies (hamstring) MAY
rest** → ATT −0.05 (uncertain "may", mild); but Canada won 6-0 vs Qatar & tops group. Bosnia: Muharemović (CB) SUSPENDED → DEF −0.05 (minor;
Qatar weak + 2 Qatar suspensions). **X2 = SPENT (Senegal) — no boost available this slate.**

| # | Match | OUTCOME | SCORE | Rationale (two-axis, blend 0.4/0.6) |
|---|-------|---------|-------|----------------------|
| 1 | England–Ghana | **England** | **2-0** | FOLLOW: blend-EV-max 37.0 (model 89 ≈ mkt 81). Edge 1.31 but field 92% = table stakes, ZERO separation. 2-0 modal. |
| 2 | Panama–Croatia | **Draw** | **1-1** | **AXIS-B (lower-conviction): Draw blend-EV-max 27.2** (Croatia reward crushed to 36 → even at mkt 66% only ~23 EV), field-underpicked (9% vs Croatia herd 89%), market-confirmed edge 1.16. FREE decorrelation (it IS the EV-max). **Headwind:** Croatia must-win + heavy fav → real draw prob may be <22%. The weaker of the two decorrelations; downgrade to Croatia-follow if minimizing variance. 1-1 modal. |
| 3 | Colombia–DR Congo | **Colombia** | **1-0** | FOLLOW: blend-EV-max 51.0 (slate's best; model 71 ≈ mkt 63). Edge 1.46 (strong +EV). Field 58% = moderately crowded, limited separation. 1-0 modal. |
| 4 | Switzerland–Canada | **Canada** | **0-1** | **AXIS-B (cleaner): Canada blend-EV-max 35.0** (reward 129 × ~28%), field only 15% (field over-loves Draw 46% / Switzerland 39%), market-confirmed edge 1.19 (mkt 29% > reward-impl 24%). Same profile as Senegal but with EV margin. **Flag:** Davies-rest doubt (overlay −0.05 applied, still EV-max). 0-1 modal. |
| 5 | Bosnia–Qatar | **Bosnia** | **1-0** | FOLLOW: blend-EV-max 51.4. **Edge 1.65** — the fixed line badly under-prices Bosnia (reward-impl 39% vs mkt 64%) → strongest +EV of the slate. Field 59% (crowded). Both must-win. 1-0 modal. |

**Portfolio:** 3 strong +EV FOLLOWS (England, Colombia, Bosnia — all crushed/strong chalk the field also holds → points, not rank) + **2 FREE
EV-MAX decorrelations (Canada cleaner, Panama-Croatia draw marginal)** = the rank levers. Both are blend-EV-max (not sacrifices) + field-underpicked
(15%/9%) + market-confirmed → the disciplined optimizer output, not forced variance. **Honest base case:** the 3 follows land, both decorrelations
likely miss (~25%/~22% each → ~56% BOTH miss), modest rank-static day; upside is a Canada or draw hit (85-91% of field off them) = big jump. After the
Senegal X2 loss this is the correct profile for trailing #9 with a reachable top-5 — following is what dropped us; the Senegal loss was variance, not a
process error. **NO X2 (spent on Senegal).**

*Pending: realized TIERS for these 5 + results; updated leaderboard.*

---

# MD10 full slate — submitted picks (computed 2026-06-25, engine v6 + independent market veto + Tier-1 red-team)

**Standing:** USER = Lampadaire83 **#8 of 16 @1857** (27 bons / 4 exacts). Bunched: #7 Cyril 1868 (+11), #6 CrazyBE
1910 (+53) above; #9 Ethan 1776 (−81), #10 Chocho 1710 (−147) below. Top-5 line = #5 AdyFC 2090, gap **233**.
**X2 SPENT.** Final group matches (E/D/F/I). Independent market = de-vigged Kalshi/ESPN/FanDuel/DraftKings/Caesars
(WebSearch 2026-06-25). Preflight GREEN.

| # | Match | OUTCOME | SCORE | blendEV | Rationale (1-line) |
|---|-------|---------|-------|---------|--------------------|
| 1 | Ecuador–Germany | **Germany** | **0-1** | 21.2 | FOLLOW. ⚠ engine picked Ecuador (blendEV 37.9, PRIME flag) — 3-agent red-team FALSIFIED it: EV+ but RANK-negative for a player atop a bunch; v6 Ecuador artifact; 2/13 losing profile. See REVIEW_2026-06-25 |
| 2 | Curaçao–Ivory Coast | **Ivory Coast** | **0-1** | 41.3 | follow; CIV must-win for 2nd, mkt 84% |
| 3 | Tunisia–Netherlands | **Netherlands** | **0-1** | 46.4 | follow; NL 1st, strong XI named, mkt 90% |
| 4 | Japan–Sweden | **Japan** | **2-0** | 56.4 | follow + best EV on board; field underweights Japan (45%) vs the 42% draw-herd; edge 1.43 |
| 5 | Turkey–USA | **USA** | **0-1** | (mkt 43.7) | ⚠ engine picked Turkey = documented USA-underrating artifact (v6 58%); OVERRIDE → USA (mkt-EV-max, Turkey edge 0.97<1). Dead rubber, USA rotates but still mkt fav |
| 6 | Paraguay–Australia | **Draw** | **0-0** | 39.7 | blend-EV-max DRAW (Australia advances on a draw & plays for it; Paraguay missing Almirón). Field 43% also here → EV pick, not a separator |
| 7 | Norway–France | **France** | **0-1** | 35.4 | follow; both qualified, top-spot decider, France strong XI (Deschamps absent, off-field) |
| 8 | Senegal–Iraq | **Senegal** | **1-0** | 39.7 | follow; both 0pts must-win, Senegal heavy fav (mkt 79%) |

**STRATEGY: full FOLLOW slate (no clean separator exists — almost all chalk).** The two deviations from raw engine
output are both ARTIFACT CORRECTIONS toward the market (Ecuador→Germany de-escalates a falsified decorrelation;
Turkey→USA is the standard USA-underrating veto), NOT new contrarian bets. **The rank lever this slate is EXACT-SCORE
accuracy on the confident follows** (Senegal 1-0, NL 0-1, CIV 0-1, Japan 2-0 are the best exact chances) — the
documented real separator (climbers carry 7-11 exacts vs user 4; the user's best move to date was a Colombia 1-0
EXACT +127 on a straight follow). **NO X2 (spent).** Honest: a near-pure-chalk day = points-not-rank; rank moves only
if an exact lands or the favourite-herd takes an upset we dodged.

*Pending: realized TIERS for these 8 + results; updated leaderboard.*

---

# MD11 slate 2026-06-27 (engine v6 frozen + independent market veto + Tier-1 red-team) — FINAL group matches, Groups G & H

**Standing:** USER = Lampadaire83 **#8 of ~16 @2120** (30 good / 5 exacts). Top-5 line #5 AdyFC 2347, gap **227**;
#7 Chocho +40, #6 CrazyBE +151 above; #9 Cyril −39, #10 Ethan −271 below. **X2 SPENT.** Preflight GREEN.
Independent market = de-vigged bet365/FanDuel/ESPN/SportsLine + Opta supercomputer (WebSearch 2026-06-26).
**Group H** standings: Spain 4 / Uruguay 2 (2nd on goals) / Cape Verde 2 / Saudi 1. **Group G**: Egypt 4 / Iran 2 / Belgium 2 / NZ 1.

| # | Match | OUTCOME | SCORE | blendEV | Rationale (1-line) |
|---|-------|---------|-------|---------|--------------------|
| 1 | Uruguay–Spain | **Spain** | **0-1** | 35.4 | FOLLOW. Spain near-full XI (Yamal/Pedri/Rodri) wants to top group; mkt 59%. Crushed chalk, field 87% = no sep |
| 2 | Cape Verde–Saudi Arabia | **Draw** | **0-0** | 38.2 | blend-EV-max draw (reward 123); even 3-way. BUT field 50% on draw = crowded → EV pick, NOT a separator |
| 3 | New Zealand–Belgium | **Belgium** | **0-2** | 24.9 | FOLLOW. Belgium -500, Doku back, motivated; field 86% = no sep |
| 4 | Egypt–Iran | **Draw** | **1-1** | (mkt 35.3) | ★ OVERRIDE engine's IRAN (blendEV 41.4 + PRIME-X2) = v6 bidirectional artifact (Iran edge 0.92<1). The slate's ONE rank-lever: EV-tied w/ Egypt on pure market (35.7/35.3) + robust across truth axis + field-underpicked 24% vs mkt 31% + edge 1.01 |

**STRATEGY: 2 follows (Spain, Belgium) + 1 EV-max-but-crowded draw (CV-Saudi) + 1 GATED rank-lever decorrelation
(Egypt-Iran draw).** The Egypt-Iran draw is the disciplined Axis-B pick a **trailing-must-climb #8** should take:
EV-neutral (edge≥1, no leak) + field clearly underpicks it (24% vs the 71% Egypt-herd) + market-confirmed. A
3-agent red-team confirmed the take (and NARROWED the 2026-06-25 "inversion" call: the bunch is not the
benchmark — the live top-5 objective is, and only field-underpicked up-variance closes a 227 gap vs a chalk
field; following freezes it). **Iran VETOED** (documented artifact, edge<1 — Ecuador/USA class). **Score = deployed
pure-modal** (Egypt-Iran draw modal 1-1; CV-Saudi draw modal 0-0); the 1-1 step-off was retired by backtest.
**NO X2 (spent).** See REVIEW_2026-06-26_egypt-iran-draw-and-inversion.md.

*Pending: realized TIERS for these 4 + results; updated leaderboard.*

---

# MD12 slate 2026-06-27 (engine v6 frozen + independent market veto + Tier-1 red-team on the MAXIMAND) — FINAL group matches, Groups J/K/L

**Standing:** USER = Lampadaire83 **#4 of 9 shown @2688** (36 good / 8 exacts) — jumped #8→#4 (+568, 3 EXACTS: Spain 0-1,
Cape Verde 0-0, Egypt-Iran 1-1). Bunch: #1 Alex 3042 (+354 runaway) / #2 Nicolas 2761 (+73) / #3 Hadri 2689 (+1) /
**#4 USER 2688** / #5 AdyFC 2681 (−7) / #6 Alexis 2633 (−55) / #7 CrazyBE 2605 (−83). Preflight GREEN. X2 SPENT.
Independent market = de-vigged bet365/FOX/CBS/oddschecker (WebSearch 2026-06-27). South Africa–Canada EXCLUDED (user: predict later).

**★ MAXIMAND RESET (user 2026-06-27, Tier-1 red-team REVIEW_2026-06-27_maximand-and-risk-model.md):** the objective is
**disciplined EV-max prediction — keep improving the model & the way we use it; rank is the SCOREBOARD, not the objective
function.** NOT P(top-2-3), NOT a convex rank-gamble. ⇒ follow blend-EV-max, modal scores, decorrelate ONLY when the
field-thin pick is *also* EV-max (free differentiation), veto model artifacts toward the independent market. NO variance ramp.

| # | Match | OUTCOME | SCORE | Rationale (1-line) |
|---|-------|---------|-------|--------------------|
| 1 | Panama–England | **England** | **0-2** | FOLLOW, EV-max lock (mkt 80%, field 96%). England wants top spot |
| 2 | Croatia–Ghana | **Croatia** | **2-0** | FOLLOW, blend-EV-max (mkt 55%). Croatia must-win; model hot (81) but agrees direction — no veto |
| 3 | Colombia–Portugal | **Colombia** | **1-0** | **EV-MAX + field-thin** (mkt-EV 35.7 > Por 28.1; edge 1.22; field 7% vs Portugal-herd 72% on only 55 reward). Not a rank bet — the highest-EV pick, field just misses it |
| 4 | DR Congo–Uzbekistan | **DR Congo** | **1-0** | ★ VETO engine's UZBEKISTAN (model rates eliminated away Uzb 39% vs mkt 12%; edge 0.60≪1) = artifact; minnow low-liquidity match. Must-win DRC + dead-rubber Uzb stakes AGREE with market → follow DR Congo (mkt-EV 39.1) |
| 5 | Jordan–Argentina | **Argentina** | **0-2** | FOLLOW, lock. Argentina qualified → rotation, already priced (mkt 80% not 90%) |
| 6 | Algeria–Austria | **Draw** | **1-1** | ★ OVERRIDE engine's AUSTRIA (model overrates it 41 vs mkt 33). Independent-market DRAW is EV-max by ~10pts (45.3 vs 35.3); draw-incentive both ways (Austria advances w/ draw, Algeria's draw = live 3rd-place) |

**STRATEGY: 5 follows + 1 EV-max field-thin pick (Colombia).** Two engine corrections, BOTH toward the independent
market (DR Congo artifact-veto; Algeria-Austria model-overrating → market-EV draw) — zero contrarian rank-bets. Score
layer = pure modal (Colombia 1-0 = the +127 exact profile; clear-fav margin scores are floor-safe). **X2 spent. NO variance
ramp** — this is the disciplined-EV-max slate the new maximand prescribes; rank lands where it honestly lands.

*Pending: realized TIERS for these 6 + results; South Africa–Canada to predict; updated leaderboard.*
