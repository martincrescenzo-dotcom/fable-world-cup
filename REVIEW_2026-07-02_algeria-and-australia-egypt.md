# REVIEW 2026-07-02 — Tier-1 red-team: Switzerland–Algeria & Australia–Egypt (R32 slate)

Lenses run: A statistician (complete), C data-integrity (complete, 21/21 PASS — every pipeline number
reproduces exactly on the frozen engine, no arithmetic errors). Lens B strategist was stopped by the user
mid-run; its attack lines (bonus-EV asymmetry, probability-vs-EV policing, Amoura option value) were covered
by lens A's recomputation + synthesizer adjudication below. "Numbers right, inference contested" again — the
fight was entirely at the inference layer.

## VERDICT 1 — Switzerland–Algeria: **ALGERIA 0-1 STANDS**, rationale REWRITTEN

- [SERIOUS, fixed] The "2.7σ" I computed is inferentially EMPTY (σ_p=|model−mkt|/2 measures model-market
  agreement between ~60%-correlated estimators, not uncertainty about the true probability). STRUCK from the
  rationale — do not cite it.
- The pick survives on the honest propagation instead: **EV(Alg) > EV(Sui) in 44/44 corners** (book range
  SUI .46–.51 × rho CI [0.564,0.732] × s_home 0.4–0.8 × both draw-alloc conventions), min gap **+3.2** at the
  worst corner, and survives FULL shrink-to-market (+8.7 at w_model=0). Powered basis: the corner grid, not a
  significance heuristic.
- [SERIOUS, fixed] "Model and market agree" over-claimed: at 90' the model has Algeria +5.6pts on the weaker
  side (the 9/9 divergence class, mild). It doesn't bite ONLY because full shrink keeps Algeria EV-max — log
  as "survives full shrink," not "agreement."
- MECHANISM (new, structural — the real finding): **the house reward line is 90'-SHAPED but pays on 120'
  outcomes.** Reward-implied draw tracks the 90' market draw in 8/9 slate matches; at 120' the draw prob falls
  ~35% ⇒ ALL NINE draw edges ≤0.69 (structurally over-priced) and BOTH win sides inherit +EV (mean edge
  inflation +0.12; 9/9 market favourites pass edge>1). Consequences: (a) never take a KO draw off reward-EV
  without this correction; (b) a KO edge>1 on a win side is weak pick-vs-alternative evidence — the
  PROPAGATION is the load-bearing test. Algeria is the slate's extreme case of this mispricing (house implied
  21.6% vs mkt120 27%).
- Belgium-Iran analogy: correct in mechanism (fixed-line mispricing, market-confirmed), wrong in detail
  (that was a draw at 90' rules; this is a win side at 120').
- Amoura (unconfirmed doubt): worst corner already prices SUI at the .51 book end and still gives +3.2 —
  a confirmed absence does not flip the pick on current information. Re-check only if the line moves past
  SUI .51 / Alg <.20 before lock.

## VERDICT 2 — Australia–Egypt: **AUSTRALIA 1-0 STANDS** — lens A's Egypt overturn is itself the
## documented OVER-VETO error; adjudicated against it. Honest label: NEAR-EV-TIE, not "EV-max edge 1.17".

Lens A findings accepted as numbers, rejected as verdict:
- ACCEPTED [FATAL-as-labeled]: the "pure-market still favours Australia (+1.1)" tiebreak I quoted was
  CIRCULAR — the market leg routes broken-draw mass by the MODEL's s_home=0.594; with the market-consistent
  split (0.433) pure-market flips to Egypt (−2.6). That specific supporting claim is STRUCK.
- ACCEPTED: gap = 1.22σ by the project metric = NOT significant (and must be reported, not omitted while
  Claim 1 advertised its σ). Blend PROBABILITY favours Egypt for w_model<0.27.
- REJECTED — the Egypt verdict. Lens A's own decontaminated flip surface: with the market-consistent split,
  **Australia is EV-max for ALL w_model > 0.084** (gap +1.3…+11.3 across every corner at w=0.15; +9.1…+16.5
  at the deployed 0.4). The doctrine's honest weight range on a clean divergence is w_model 0.15–0.40
  (artifact-veto review 2026-06-28: full veto on an UNFLAGGED team = double-counting; honest market weight
  0.6–0.85, NOT 1.0). Choosing Egypt requires w_model<0.084 ≈ the killed over-veto. The Mexico–Ecuador
  signature is ABSENT at deployed weights: there, blend-prob favoured the market side (Mexico 41.6 vs 35.2)
  AND edge(pick)<1 (0.85) — two pre-registered veto conditions. Here blend-prob favours Australia (41.2 vs
  37.8) and edge(Aus)=1.17>1 (with the 120'-inflation caveat above). Lens A's remaining Egypt tiebreaks
  (market probability-max, field%) import the killed highest-probability criterion and a rank lever (G1 OFF).
- The 9/9 weaker-side prior (p≈0.002, sign-only) is CONSUMED by the shrink inside 0.15–0.40; it cannot also
  mandate w=0. "Market wins every time" remains unpowered (8/9, CI [0.52,0.997]).
- Salah game-time doubt: priced (lines post-date the scan); a confirmed START would strengthen Egypt — if the
  line moves to Egypt ≥.45 (90') before lock, the corner math changes; re-check then, else submit as is.
- HONEST LABEL for the ledger: near-EV-tie on a hard divergence, decided by the deployed blend at its
  sanctioned weight range; Australia by +1.3…+16.5 EV (≤1.2σ) across w_model 0.15–0.40 with either split;
  NOT a decorrelation play (field 14% is incidental; G1 OFF); modal 1-0 (17.0%) also the grid's fattest cell.

## Slate disposition (all 9)
USA 1-0 · Spain 2-0 · Portugal 1-0 · **ALGERIA 0-1** (mispricing EV-max, 44/44 corners) ·
**AUSTRALIA 1-0** (near-tie, deployed-blend call) · Argentina 3-0 · Colombia 2-0 · Morocco 0-1 · France 0-1.
The 7 uncontested picks: blend-EV argmax = blend-prob argmax simultaneously, edges 1.13–1.54, verified 21/21.

## Process notes
- Two self-inflicted rationale defects caught before shipping (empty 2.7σ; circular pure-market tiebreak) —
  the gate keeps paying at the inference layer, never yet at the arithmetic layer.
- NEW STRUCTURAL FINDING to carry: 90'-shaped house line at 120' scoring ⇒ KO draws house-over-priced
  slate-wide, KO win-edges>1 near-automatic. Added to memory (reward-asymmetry note).
- Deploy caveat unchanged: the market-leg 120' mapping inherits model rho/s_home; pin against a real
  "after-ET" draw price when liquid (open validation debt).
