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
