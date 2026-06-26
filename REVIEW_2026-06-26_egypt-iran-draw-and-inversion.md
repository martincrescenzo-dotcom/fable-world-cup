# RED-TEAM REVIEW 2026-06-26 — Egypt-Iran Draw vs Egypt-follow + the "inversion" doctrine

**Trigger:** MD11 slate. After vetoing the engine's Iran pick (documented v6 artifact), the Egypt-vs-Draw call
is a clean EV-neutral field-underpicked decorrelation — exactly the take-vs-follow spot I committed (2026-06-25,
to the user + CLAUDE.md) to red-team rather than default. Resolves both the pick AND the standing inversion
doctrine. Tier-1, 3 lenses, each recomputing.

## VERDICT
**TAKE THE DRAW (Egypt-Iran, submit 1-1). The 2026-06-25 "inversion" call is NARROWED TO NEAR-DEAD.**
All three lenses converge on the Draw; the strategist and statistician independently kill the inversion logic.
Pattern: my *conclusion* (Draw) was right but TWO of my *justifications* were wrong (blend-EV-max = artifact
leakage; 0-0 score = retired rule). Corrected below.

## THE PICK — Egypt vs Iran
- v6 model [Egypt .27, Draw .27, Iran **.45**] reproduces exactly. The model makes a BIDIRECTIONAL artifact on
  this match: underrates Egypt 15pts (.27 vs market .42) AND overrates Iran 19pts (.45 vs market .26).
- **Iran VETO (clean):** edge = market/reward-implied = .26/.284 = **0.917 < 1** → the fixed line over-prices
  Iran; the engine's blendEV 41.4 + PRIME-X2 tag is the reward-artifact riding the model's Iran error. Same
  class as Ecuador/USA/Ghana-Panama, all of which resolved FOR the market. (X2 spent → PRIME flag moot anyway.)
- **Egypt vs Draw — the honest EV case (my first cut was wrong):**
  - ✗ DROP "deployed blend shows Draw EV-max (33.7 > 30.7)" — that 3pt gap is the SAME Egypt-underrating
    artifact I veto Iran for; can't distrust one end of the error and trust the other.
  - ✓ Pure-MARKET EV: Egypt .42×85 = **35.7** vs Draw .31×114 = **35.3** → gap 0.36, σ_diff ≈ 6.5 → **EV-tied**.
  - ✓ Truth-axis robustness: if MODEL true, Draw +7.9; if MARKET true, Egypt +0.4 (noise). **Draw weakly
    dominates; Egypt is never meaningfully ahead at any truth weight** — the EV-robust pick given a 15pt
    unresolved divergence.
  - ✓ Field-underpicked: field 24% draw vs market 31%; field OVER-picks Egypt (71% vs market 42%).
  - ✗ DROP "Egypt cagey → elevated draw" as an EV argument — already in the market's 31%; double-counts.
    Keep only as an unvalidated soft tiebreaker (Verify-Std #6/#7).
- **edge gate:** Egypt 1.02, Draw 1.01, Iran 0.92. Draw clears edge≥1 (barely) + field-underpicked +
  market-confirmed = the gated decorrelation profile.
- **SCORE = 1-1 (deployed pure-modal rule), NOT 0-0.** Data-integrity caught it: the 1-1 step-off was RETIRED
  2026-06-17 (`score_rule_backtest.py`: pure-modal 190 > step-off 130 realized). Egypt-Iran draw cells
  P(1-1)=11.7% > P(0-0)=11.3% → modal = **1-1**. CLAUDE.md prose still said "step off 1-1 → 0-0" = STALE;
  scrub it. (CV-Saudi draw modal IS 0-0, 15.5%, unaffected.) The 0-0-in-defensive-draws pattern stays a logged
  flag, not an override.

## THE DOCTRINE — 2026-06-25 "inversion" call NARROWED to near-dead
Inversion claim (2026-06-25): "for a player bunched & defending from BELOW, high-variance decorrelation is
RANK-DESTRUCTIVE (a miss cedes the head-to-head to chalk-followers above + lets #9 close) → bank chalk."

**Why it falls (strategist, structural — does NOT rest on the one MD10 slate):**
1. **Wrong maximand.** It minimized variance to defend the #8/#9 *local boundary*. The committed objective is
   **TOP-5, gap 227**. For a player 227 below target, the #8/#9 spot is nearly worthless to the objective —
   dropping to #9 barely changes P(top-5). This is the SAME rank-via-proxy error the 2026-06-24 review already
   caught, re-introduced as "rank-via-local-spot."
2. **Gap arithmetic.** Computed net swing vs a chalk rival per branch: Draw's gain-branch = **+86.6**, Egypt's
   best = **+24.6** (and rivals bank Egypt 71% of the time → realized net ≈ 0). Following FREEZES a 227 gap
   (E[net vs chalk] ≈ 0, capped upside). **Only field-underpicked up-variance (the +86.6 events) can close it.**
3. **Asymmetric decision tree.** The inversion priced "decorrelate→miss→cede to chalk above" but NEVER priced
   "follow→the field-underpicked thing hits→cede to VARIANCE players." MD10 realized the un-priced branch
   (user followed +263 = static #8; Chocho caught the upset cluster, #10→#7). Corroborating, not load-bearing.

**Nuance (don't over-rotate):** "field-underpicked" is the correct decorrelation proxy ONLY against a CHALK
bloc (this match: 71% Egypt = chalk → valid). Against an OFF-CHALK variance rival you may need the other side
of *his* variance, not the field's. And the inversion survives in ONE regime: when defending a local boundary
you genuinely care about AND the climb is dead. Per CLAUDE.md the climb (top-5) is LIVE → not that regime.

## CORRECTED RULE (supersedes 2026-06-25 inversion)
> **Your bunch is not your benchmark — your OBJECTIVE is.** With top-5 line 227 above and a chalk-heavy field,
> the user is a **trailing-must-climb** player. Following freezes the gap. So **take EV-neutral (edge ≥ 1, no EV
> leak) field-underpicked + market-confirmed up-variance on gated spots, ≤1–2/slate**, and stack
> exacts-on-follows on everything else. A miss that costs the local #8/#9 spot is immaterial to top-5; a
> field-underpicked hit is the only path to it. **edge ≥ 1 (not strict >1)** suffices for a must-climb trailer
> (up-variance IS the goal); edge <1 is an EV leak → still reject. Switches: top-5 live? (master) · field chalk
> vs the binding rival off-chalk? · horizon (≥~10 left → can afford variance; 1–2 left → collapse to defense).

## MD11 SLATE (final picks)
1. Uruguay-Spain → **Spain 0-1** (follow, blendEV 35.4, near-full XI, field 87% = no sep).
2. Cape Verde-Saudi Arabia → **Draw 0-0** (blend-EV-max 38.2, BUT field 50% on draw = crowded, NOT a separator).
3. New Zealand-Belgium → **Belgium 0-2** (follow, field 86% = no sep).
4. Egypt-Iran → **Draw 1-1** (OVERRIDE engine's Iran artifact; the one rank-lever decorrelation —
   EV-tied/robust + field-underpicked 24% + market-confirmed + edge 1.01). **NO X2 (spent).**
Portfolio: 2 follows + 1 EV-max-but-crowded draw + 1 gated rank-lever decorrelation. Disciplined (≤1-2 rule).

## STANDING-RULE COMPLIANCE
- Power/CI: EV gaps recomputed with σ (Egypt-Draw within noise; Draw robust across truth axis). 
- Maximand: corrected — objective is top-5 (227), NOT the #8/#9 boundary the inversion defended.
- Measured vs assumed: qualification-cagey tailwind labeled unvalidated, kept OUT of EV.
