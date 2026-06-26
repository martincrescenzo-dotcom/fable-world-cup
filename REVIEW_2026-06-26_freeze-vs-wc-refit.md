# RED-TEAM REVIEW 2026-06-26 — "Freeze v6 through KO; don't refit on WC data"

**Trigger:** user asked whether to update team figures (att/def) with end-of-group-stage data, and explicitly
asked "are the data available? do red team agree?" Load-bearing (deploy/freeze decision on the hash-verified
core) → Tier-1 three-agent review (statistician + strategist + data-integrity), each recomputing independently.

## VERDICT
**FREEZE CONFIRMED — no lens could break it.** But this is a "numbers/decision right, stated INFERENCE partly
wrong" outcome (the recurring project failure mode). Two of my three original arguments were hand-waved or
mis-aimed; the data fact is solid; and the deepest finding is that **the entire refit thread is low-leverage
displacement** from the levers that actually move rank.

## DATA AVAILABILITY (data-integrity lens, all PASS)
- StatsBomb free open-data `competitions.json` (fetched live, 80 records): FIFA World Cup seasons =
  {1958,1962,1970,1974,1986,1990,**2018, 2022**}. **No 2026 season anywhere.** Local SB corpus = 314 matches,
  newest 2024-07; **zero 2026.** → **a faithful goals+xG refit is BLOCKED** (the xG leg is load-bearing in
  `fit_attack_defense.py`, weight 1.3, not optional).
- `goals_records.json` = 4568 matches, max real-scored date **2026-06-10**, **no WC-2026 results.** NUANCE the
  audit surfaced: `intl_results.csv` holds 72 WC-2026 rows but all `NA–NA` (pre-loaded fixtures); the local CSV
  is a stale Jun-11 snapshot. A **fresh** martj42 re-pull WOULD now carry real WC-2026 *scores* (goals only, no
  xG). So "the data isn't there" is true for the local files and for xG everywhere free; goals-only is
  obtainable upstream but (see below) provably inert.
- Engine integrity: blend = 0.4 model + 0.6 market (matchday.py L233), BONUS_MODE='coarse', preflight GREEN,
  `attdef.json` SHA256 matches manifest. All confirmed.

## WHY THE REFIT IS WORTHLESS — the CORRECTED argument (statistician lens)
My original "n=3 games per team is too noisy" was **imprecise and half-wrong**. Reparametrising the ridge into
**strength S=ATT+DEF** (prior precision 2·ρ_str+ρ_ad = 68) and **split Δ=ATT−DEF** (precision ρ_ad = 8), the
posterior weight on 3 new matches is:

| direction | w(n=3) | controls |
|-----------|--------|----------|
| strength S | **0.10** | win/draw/loss (supremacy, what γ recalibrates) |
| split Δ | **0.48** | total goals / score grid |

From `predict_v6.py` `lam_pair`: **outcome probability depends ONLY on strength S.** So a WC refit moves the
outcome layer by ~10% of a 3-game (mostly-noise) signal, then ×0.4 blend ⇒ **~4% of a noise signal reaches the
pick** — near-inert on the only layer that feeds the EV. It moves the *score grid* a lot (w=0.48) — but that's
the validated "mechanical sideshow" (modal-score rule), where n=3 = pure overfitting. **Both layers say don't
refit, for opposite reasons.** This is the real proof; "n=3 too noisy" was the right intuition aimed at the
wrong direction.

**The proposed round-3 backtest (n≈48) is severely UNDERPOWERED — drop it.** Monte-Carlo'd exact-score logloss
diff: sd_diff ≈ 0.53 nats/match → SE over 48 = 0.077 → MDE@80% = 0.22 nats/match. Realistic refit gain
(v-ladder OOS scale) ≈ 0.02–0.03 ⇒ **power ≈ 6%.** A null would be uninformative, not exculpatory. Historical
v-ladder gains were measured over thousands of CV folds, not 48. Outcome-Brier doesn't rescue it (true outcome
effect ≈ 0 by construction). **So I must NOT claim "we could validate it with a backtest" — we can't, mid-tournament.**

## THE DEEPER FINDING — the thread is a low-leverage distraction (strategist lens)
The refit can only change a pick where **model DIVERGES from market** — which is exactly where the stale model
is *most likely wrong* and where the doctrine **already vetoes model→market** (Ecuador, USA 3/1, Ghana/Panama).
A refit re-estimates a leg we've already decided not to trust when it speaks up; its marginal rank value ≈
P({model diverges} ∩ {model right} ∩ {field on wrong side}), which a 3-game refit cannot identify.

**Lever ranking for the +227-to-top-5 path (refit is DEAD LAST):**
1. **Exact scores** — the documented separator (user 5 vs AdyFC 12 / Hadri 11; best results Colombia 1-0 +127,
   Paraguay 0-0 +50, both exacts on follows). Refit value = **0** (score = mechanical modal, already 0.96
   cell-corr vs Winamax).
2. **Field-underpicked +EV decorrelation** — needs field% + market, not a better model. Refit = 0.
3. **KO field-crowding / upset reads** — needs convergence reasoning + manual scan. Refit = 0.
4. **Contested-outcome accuracy** — the only lever a better model could touch; but the market prices contested
   majors and the model's divergence record is 0-for-the-ledger ⇒ marginal/negative.
5. **The refit** — below all of the above, and it risks the frozen core.

**KO makes freeze MORE right** (a KO refit would train on group-winner-survivors = selection bias toward
inflated attack, predicting a different opponent class; plus rotation/park-the-bus/ET/penalties the goals-model
can't capture). The original decision never reasoned about KO — it's accidentally-right there.

## THE ONE TRUE THING IN THE USER'S INSTINCT
WC form is genuinely *unpriced* in exactly one place: **low-liquidity minnow matches** (Curaçao, Iraq, Cape
Verde, Jordan) where the pre-tournament Elo anchor is stalest AND the market is thin/slow, so the 0.6 market
leg can't bail us out. But that is the **noisiest** possible spot for a 3-game refit — so the correct tool is a
**sharper manual overlay on illiquid-market matches**, not an engine refit. "Market prices form" is the
load-bearing reason to freeze, but it is precisely *not* true for minnows — route those to the overlay.

## CONSIDERED & REJECTED: a graded market-weight on divergences
Both the strategist's cleanest constructive idea (push market weight → 0.8/0.2 as |p_model−p_market| grows)
is theoretically sound (downweight the stale leg exactly when it's most likely wrong). **NOT adopted:** it
introduces a free threshold/curve we **cannot fit** at current n (same power wall that kills the backtest), and
the **existing binary market-veto already captures the benefit at the extreme**, where it matters most.
Replacing a robust binary veto with an unfittable graded curve would be trading one overfitting trap for
another. Keep the binary veto.

## ACTIONS
1. **Keep v6 FROZEN through the rest of group stage AND the KO round.** (Confirmed; preflight stays the gate.)
2. **Drop the round-3 backtest idea** — underpowered (~6%), can't validate mid-tournament. Do not cite it.
3. **No refit** — faithful goals+xG blocked (no 2026 xG); goals-only is obtainable but provably inert on
   outcomes and overfit on scores. Neither is worth touching the hash-verified core.
4. **Carry WC form through the existing channels**, with one sharpening: on **low-liquidity minnow matches**,
   lean harder on the manual model-blind overlay (that's the only genuinely unpriced signal).
5. **Redirect attention to the real rank levers:** exact-score accuracy on confident follows + KO
   field-crowding/decorrelation reads. Treat a future "should I refit?" impulse as a tell of displacement.

## STANDING-RULE COMPLIANCE
- Power/CI check: done (refit inert by shrinkage algebra; backtest power 6%). 
- Maximand check: done (rank via points; the model is not the separation lever — exacts/decorrelation are).
- This is the 3rd time the "more data / refit" impulse was correctly resisted (league_sim2, crowd-refits, now this).
