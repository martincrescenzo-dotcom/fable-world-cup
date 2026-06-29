# Tier-1 Red-Team — Netherlands 1-0 Morocco (R32, 2026-06-29)

**Trigger:** user requested a full review of the live KO pick ("run the redteam… see if there's something interesting or just routine").
**Method:** 3 independent parallel agents (Statistician / Strategist / Data-integrity), each recomputing from raw files (`ko_build.py`, `attdef.json`, `wc_to_canon.json`, `qualification_v5.json`, `ko_et_dataset.md`). Synthesis below.

## VERDICT: PICK STANDS (Netherlands 1-0). No FATAL, no pick change.
All 9 quantitative claims reproduce **exactly** (data-integrity PASS table; statistician independent recompute matches to rounding). The interesting content is two **rationale over-claims** — both pick-neutral, one a standing-OUTPUT-GATE violation — now corrected in `prediction.md`/`live_updates.md`.

### Reproduced (independent): 
v6 90' NL 45.8/26.2/28.0 (modal 1-0); de-vig market 44.47/28.97/26.56 (overround 4.59%); ρ=86/132=0.652 (SE .041), φ=0.635@λ1.15, CI [0.44,0.88]; blend120 51.06/17.64/31.30; EV120 40.85/20.11/38.19; edge NL 1.205 / Mor 1.125; modal 120' 1-0 @14.04% (next 0-1 10.4%, 2-1 10.0%). φ-robust: pick=NL and margin +2.67/+2.66/+2.71 at φ={0.44,0.635,0.88}. SA-Canada(R32) obs registered (57 total), crowd_params byte-identical (no refit). preflight GREEN.

## FINDINGS

### [SERIOUS — fixed] "NL EV-max by +2.7" overstated → it is a NEAR-EV-TIE shaded to NL.
The +2.7 gap (40.8 vs 38.2) exists because of the **reward asymmetry**, not a probability edge: NL wins ~51% but pays 80; Morocco wins ~31% but pays 122 → EVs nearly equal. The project's σ_EV significance test (|p_model−p_market|/2 propagated) rubber-stamps this as ">2σ significant" — but that test is **near-circular when model≈market** (divergence-σ ≈ 0 by construction) and captures none of the decision-relevant uncertainty (60% shared model/market ancestry, single-bookline, φ identification). The gap also leans on the draw-reallocation's **un-attenuated supremacy split** (wshare=0.59 of freed draw mass → favourite NL), the same chalk-biased risk flagged in commit 567dfbb; if it over-attenuates, the true gap is tighter, possibly a dead heat. Honest framing: **Morocco is a genuine close alternative; NL wins the EV ranking robustly (it's max at 90' AND across the full φ band) but narrowly.** Morocco is rejected ONLY because it's −2.7 EV and 6.4% below max = **outside the 5% free-decorrelation band** — not vetoed.

### [SERIOUS — fixed, OUTPUT-GATE violation] "Field 39% under-backs NL" was noise dressed as signal, and backwards.
39% vs reward-implied 42% = 3pp with no CI, measured against the **game-maker's own line** (not an independent field-behavior measure) → statistically indistinguishable from zero. Worse: **39% is the PLURALITY field pick.** Picking the plurality outcome is **correlated with the pack, not decorrelated** — the claim "the EV-max pick is also the non-crowded one (no decorrelation tension)" inverts reality. Struck entirely; NL rests on EV alone.

### [MINOR] Blend-then-transform shortcut is legitimate HERE, not a general identity.
Statistician recomputed the "proper" way (transform model & market 90' separately, then blend the two 120' distributions): **identical** result (51.1/17.6/31.3). Holds because the transform is linear in diagonal mass for fixed retD/wshare AND model≈market. With a real divergence it would mis-split (applying the model's retD/wshare to a strength the market disputes). Flag as approximation, not identity.

### [MINOR] Market leg correct. 90' regulation 1X2 fed through the ET transform = right input. The to-advance line (NL −170/Mor +135 → de-vig 59.7/40.3) bakes in pens-winners (scored as draws under KO rules) → using it is a silent error; even if used it pushes NL UP → never flips. Caveat: single bookline (4.6% overround), thin as "independent market," low-stakes here only because model agrees.

### [MINOR] G1 endgame correctly NOT triggered (≈25 KO matches remain, N ≫ (gap/σ_d)²). Two notes: gaps (16 to #2, 37 to #4) are already within one-slate swing → rank is near-noise → REINFORCES pure EV-max (can't precision-target with invisible rival picks). Following-the-favourite here is the **variance-minimizing** move (defends lead over #4/#5, caps catch on #2) — consistent with the maximand (rank = scoreboard). **Re-evaluate G1 at QF (N≈7), where the horizon condition can flip.**

### [MINOR] Score modal 1-0 correct (pure-modal validated; do NOT step off for bonus upside = retired −EV rule). But a flat coin-flip distribution → 14% modal → thin exact chance. No separation available on this match in ANY dimension; that's fine — bank it.

### [not a flaw] Artifact-veto correctly NOT applied (model–market diverge ≤2.8pp). And Morocco is the weaker side, where v6 tends to OVER-weight → if anything v6 understates NL → no case to fade NL.

## CORE-TENSION ADJUDICATION (follow-the-favourite EV-max vs rank-separation for a bunched #3)
EV-max wins decisively and depends on nothing contested. Morocco fails every lens at once: −2.7 EV (and you eat a zero 73% of the time vs 55%); outside the 5% DIFF band; decorrelating 39%→31% field buys only 8pp of separation for a real cost; and mid-bunch outcome-variance is E[rank]-neutral-to-negative with invisible rival picks. A rank-aware #3 still rejects Morocco.

## ACTIONS TAKEN
- `prediction.md` R32 block + `live_updates.md` RESUME header: reframed to near-EV-tie; struck the field-underpick line.
- Pick UNCHANGED: **Netherlands 1-0.**
- Residual to verify if time permits: confirm the de-vig ML line post-dates Morocco's lineup confirmation (predating → small unpriced nudge toward Morocco, tightens tie, no flip).
