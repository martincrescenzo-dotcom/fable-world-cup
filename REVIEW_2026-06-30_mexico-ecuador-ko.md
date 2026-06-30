# REVIEW 2026-06-30 — Mexico–Ecuador R32 pick (Tier-1 3-agent red-team)

## DECISION UNDER TEST
Mexico vs Ecuador, 2026 WC Round-of-32, knockout scored on the 120' line (pens ignored).
Mechanical blend-EV-max pipeline output = **ECUADOR** (EV 43.0 vs Mexico 34.9). Question: submit
Ecuador, Mexico, or Draw? User pre-fenced the documented Ecuador-overrating flag pending this review.

## VERDICT: **MEXICO** (modal 120' score 1–0). The mechanical Ecuador output is OVERTURNED.
Signature project failure mode again: **numbers all correct, inference wrong.** Data-integrity gave a
clean 12/12 PASS; the error was entirely at the framing/inference layer.

## WHY ECUADOR FALLS (three independent lenses, same conclusion)

1. **The "+8.1 EV edge" is not significant — it's a dead heat.** Using the project's own rule
   (σ_p=|p_model−p_market|/2, σ_EV=reward·σ_p): σ_diff ≈ 10.9, 2·σ_diff ≈ 21.8, gap = 8.1 →
   **0.73·σ_diff**, far inside model-market noise. Unlike NL-Morocco (where model≈market made the σ-test
   near-circular), here model and market **diverge hard**, so the test has full teeth and still says NOT
   SIGNIFICANT. There is no statistically distinguishable EV favourite between Ecuador and Mexico.

2. **The blend PROBABILITY favours Mexico (41.6 vs 35.2).** Only the EV favours Ecuador, purely via the
   reward asymmetry (122 vs 84) × the model rating Ecuador the favourite (43.6%) while the sharp market
   makes it a 20-pt underdog (29.6%). Both flipping ingredients are the suspect ones; at pure-market the
   pick is Mexico (40.3 > 36.1), so reward asymmetry *alone* does not flip it — the **model inflation does**.

3. **The one POWERED fact points at Mexico.** 9/9 clean divergences v6 over-weighted the market's weaker
   side (one-sided binomial p=0.00195). This is **team-agnostic** → it justifies a calibrated shrink toward
   market on ANY clean divergence **without invoking the fenced Ecuador-specific flag**. Flip threshold
   w_model* = 0.139; at the doctrine's honest market weight for a clean divergence (market 0.6–0.85 →
   w_model 0.15–0.40) Ecuador's lead is only +0.3 to +1.9 EV (tie), and at market 0.85 it is a dead heat
   (Ecuador 38.7 vs Mexico 38.3). Ecuador survives as "EV-max" only at exactly the 0.6 blend and below —
   i.e. only if you decline to apply a powered directional finding on a textbook instance of it. That is the
   2026-06-28 over-trusting error run in **reverse** (mirror of the over-veto error).

4. **It is NOT a decorrelation play — fails the market-confirmed clause [FATAL].** Reset doctrine: take the
   field-thin outcome (Ecuador, field 10%) only when it is EV-max **AND market-confirmed**. The sharp market
   **contradicts** Ecuador (29.6%, clear underdog). This is a model-driven contrarian the market opposes —
   the exact thing the two-axis rule forbids dressing as decorrelation. Structurally identical to the reset's
   own worked veto example (MD12 DR Congo: model 39% vs market 12% Uzbekistan → veto). A veto situation, not
   a follow.

5. **Draw rejected.** EV: model 26.6 / market 24.1 / blend 25.1 — below both alternatives in every weighting.
   edge = 0.74 < 1 (the fixed line over-prices the draw; reward-implied 31.5% vs market 22.3%). KO ET
   re-allocation re-prices draws DOWN. Field-thin (15%) but not EV-max → not a sanctioned decorrelation.

## DATA-INTEGRITY: clean 12/12 PASS
All numbers reproduce to stated precision two independent ways (pipeline run + from-scratch recompute).
Script == deployed engine (byte-identical lam_pair/nbvec/transform120; mug=0.19786, R=9.50398, GAMMA=1.5,
PHI=0.635). ET transform conserves probability (Σ=1.0), draws fall / wins rise / mass higher = correct KO
direction. No silent overlay (OVR empty for this match). EV/edge vectorized identically across outcomes (the
historical per-strategy-logic bug is absent).
- [MINOR] wshare s_home split is the documented chalk-biased one (model-derived, flatters Ecuador) but the
  pick is robust to it across s_home∈[0,1] — reward-driven, not margin-driven.
- [MINOR] market 90' line hand-entered (standard workflow). Confirmed it is the **90' regulation /
  ET-excl-pens** line (ESPN/DraftKings/FanDuel moneylines + Kalshi explicit regulation-time market), NOT the
  "to-advance" line — so the leg is correct per [[ko-scoring-120-minutes]] and the strategist's halt-condition
  does not trigger.

## DECISION RULE (pre-registerable, adds nothing new — instantiates existing doctrine)
> When a clean model-vs-market divergence makes the model rate the **sharp market's weaker side as the
> favourite** (the powered 9/9 pattern) AND the blend-EV gap to the market's favourite is **within 2·σ_diff**
> (not significant), the "blend-EV-max" label is a disagreement artifact, not an edge. Apply the calibrated
> artifact-shrink toward market (weight 0.6→0.85, NOT a full veto — no double-count). Take the
> field-thin/high-reward outcome only if it survives as EV-max at ~0.85 market AND is market-confirmed.
> Otherwise default to the sharp-market favourite, modal score within it.

Ecuador fails both prongs (loses EV-max by ~0.85 market; market contradicts it) → **MEXICO, modal 1–0**.

## HONEST RESIDUALS
- The 9/9 finding is **mild/directional**, and v6 wins ~1/9 of divergences (Türkiye 3-2). Ecuador is not
  *impossible* — it is simply **not the disciplined pick**. The burden was on Ecuador to clear the gate; it
  fails the market-confirmed clause with nothing to offset it.
- Yesterday's Paraguay (field 1% vs Germany, drew 1-1, pick lost) is the same generating pattern but n=1
  variance — a feather, not a brick. The brick is the powered 9/9 + the in-noise EV gap.
- The fenced Ecuador-specific flag was NOT needed and was NOT used — the generic finding + the
  market-confirmed clause carry the verdict, exactly as the user required.
