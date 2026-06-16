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

User #10/13 (374), gap 284 to #2 line (658), ~88 left → behind ⇒ DECORRELATE (not EV-max-follow). Preflight GREEN; Winamax 20260616 ingested. **Real WC: Group I openers + Arg-Alg opener.**
**⚠ NO POLYMARKET (no slugs for these fixtures) → independent market-confirmed VETO is degraded; applied MANUALLY via reward-implied probs. Outcome picks = model + reward-implied only (lower confidence than a PM-confirmed slate).**

| # | Match | OUTCOME | SCORE | Rationale (two-axis) |
|---|-------|---------|-------|----------------------|
| 1 | France–Senegal | **Draw** | **0-0** | EV-MAX + AXIS-B: field 88% France crushes France reward (46) → Draw is blend-EV-max (29.2), field-underpicked (9%), market-confirmed (model 24%≈impl 22%). Free decorrelation. |
| 2 | Iraq–Norway | **Draw** | **0-0** | EV-max + AXIS-B: field 91% Norway crushes Norway reward (30) → Draw blend-EV-max (22.8>21.9), field 6%, confirmed (17%≈15%). HIGH variance (Norway 73% fav) — flagged. |
| 3 | Argentina–Algeria | **Argentina** | **2-0** | AXIS-A follow: Argentina blend-EV-max (28.9), reward 43 not crushed enough for a draw edge. DEF overlay −0.05 (Dibu/Molina/Montiel/Balerdi out, halved/priced). No Axis-B avail. |
| 4 | Austria–Jordan | **Draw** | **0-0** | Raw EV-max = Jordan (28.4) but **VETOED**: model 21% vs reward-impl 15% on an away-underdog WIN = the model-overrating failure mode (Ecuador), no PM to confirm. Draw is next + better-confirmed (22%≈18%), blend-EV 26.7, field 14%. |
| 5 | Portugal–DR Congo | **Portugal** | **2-0** | AXIS-A follow: Portugal blend-EV-max (25.4); Draw excluded — separation vs bloc is NEGATIVE (Por 75%, reward 34 not crushed enough). EV-max favourite. |

**Portfolio note (honest):** 3 draws + 2 favourites = a HIGH-VARIANCE, decorrelated slate, and it's also the EV-MAX slate (expected base ~143 vs ~128 for following the bloc — decorrelation is FREE here). Downside: if favourites win across the board (they're 57–75%), I score only Arg+Por and fall further behind the bloc this matchday. That variance is the point — from 10th, EV-max-follow can't close 284; these +EV decorrelated draws are the climbing engine. Each draw is +EV individually (crushed-favourite rewards), not −EV gambling.
**X2: HELD.** No candidate ≥45 (max totalEV 36.7 Argentina; all low-K crushed-chalk matches). Reserve for a higher-E field-underpicked + market-confirmed spot (likely a more even match / knockout).

*Pending from user: realized TIERS for these 5 + the 6/14 backlog; results; updated leaderboard. For MD4+: pull `fetch_pm_matches.py` if slugs exist so the independent-market veto engages.*
