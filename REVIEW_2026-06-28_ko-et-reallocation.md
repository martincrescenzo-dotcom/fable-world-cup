# RED-TEAM REVIEW 2026-06-28 — KO Extra-Time Re-allocation (ko_build.py / ko_et_dataset.md)

**Verdict: numbers correct, several supporting claims over-reached. NO FATAL. The transform CODE is
sound and the SA-Canada pick (Canada) is safe to submit — but justify it by EV margin, not by the
"zero flips" test, and STRIP the over-claims from CLAIM A. The un-attenuated supremacy split is the
real unvalidated, possibly wrong-signed (toward chalk) modeling choice, and the proposed to-qualify
cross-check CANNOT validate it alone.**

3 independent lenses (statistician / strategist / data-integrity), each recomputed from raw files.
Data-integrity = full PASS (132 rows, 86 pens, ρ=0.6515, 0 internal-consistency violations, transform
conserves mass, no bugs). The fight is entirely at the inference/claims layer.

---

## FINDINGS (prioritized)

### [SERIOUS] The φ "sensitivity band [0.56,0.73]" is degenerate — false robustness (Lens A, C)
The calibration target Σ Poisson(λφ/3)² = ρ depends on λ and φ **only through their product**. Re-solving
φ at λ=0.8/1.0/1.15/1.3/1.6 gives φ=0.913/0.730/0.635/0.562/0.456 — but λ·φ ≡ **0.730** in every case
(per-team ET mean ≈ **0.243**). The three "band" lines `ko_build.py` prints are *one model wearing three
λ-labels*. The ONLY quantity ρ identifies is the even-match per-team ET rate ≈0.243; φ=0.635 is an artifact
of the arbitrary λ=1.15 anchor. The REAL parameter uncertainty (propagating ρ's CI at fixed λ=1.15) is
φ ∈ **[0.44, 0.90]**, ~3× wider than reported. → Stop reporting [0.56,0.73] as a sensitivity band; report
the identified rate (0.243) and the honest φ band.

### [SERIOUS] "Goals-vs-retention coincidence resolves the tension / obviates a state-dependent model" — circular + underpowered (all 3 lenses)
Poisson(mean 0.508)→P(level)=0.641 vs measured ρ=0.652 are **the same 132 matches**, and under independent
Poisson, P(level)=ΣPois(μ)² is near-algebraically tied to the goal mean. So 0.641≈0.652 tests only the
INDEPENDENCE assumption on one symmetric aggregate — it is an internal consistency check, NOT external
corroboration. The sample is conditioned on level-at-90' by construction → it has ZERO leverage on whether
ET intensity is state-dependent. "Obviates a state-dependent intensity model" is absence-of-evidence dressed
as evidence-of-absence. → Downgrade to the defensible core: "a static Poisson reproduces the level-retention
rate for even, level-start ET." It says nothing about the win-split.

### [SERIOUS] Un-attenuated ET supremacy is the real unvalidated choice — and likely ANTI-CONSERVATIVE toward chalk (Lens A, B)
ET reuses the full γ=1.5 90' λ-ratio (le,lr = lh/3·φ, la/3·φ). Two independent reads:
- Lens A: the data weakly shows supremacy IS real in ET (ET-decided matches 31:15 to the first-listed team,
  binom p≈0.03; ET goals 40:27) — so "leave it un-attenuated" is NOT the innocuous default it was framed as.
  CAVEAT: the 31:15 is **confounded by listing order** (TeamA = first-listed, not verified-favourite), so the
  SIGN of ET-supremacy is likely real but the MAGNITUDE is unidentified.
- Lens B: if real ET COMPRESSES supremacy (underdog bunkers, plays for pens), the model **over-prices the
  favourite win** and **under-prices both the draw and the underdog**. For this game that is the costly sign:
  it tilts toward the chalk favourite (shared with the herd = zero rank separation) and away from the
  field-thin draw/underdog — the doctrine's ONLY sanctioned separation lever.
- Synthesis: ET-supremacy sign ≈ real; magnitude unknown; whether the full 90'-ratio over- or under-states it
  is UNRESOLVED. The split (not the level φ) is the un-validated, decision-relevant, possibly wrong-signed part.
  Pre-register it as such; do not wave it through.

### [SERIOUS] The to-qualify cross-check CANNOT identify the split — proposed validation is partly a mirage (Lens B)
To-qualify ≈ W_h + Dr·q is ONE linear combination of (W_h, Dr, W_a). After the sum constraint there are two
free quantities — the LEVEL (Dr, set by ρ/φ) and the SPLIT (W_h/(W_h+W_a), set by supremacy); pen-skill q≠0.5
adds a third unknown. One equation can't pin both. A model with more-draw-plus-more-skew gives the same
to-qualify price as less-draw-plus-less-skew. → To identify the split you need a SECOND observable: the
"result after ET, excl. pens" 1X2 **draw price** (pins Dr), THEN to-qualify pins the split. Without the
ET-excl-pens line, the cross-check sanity-checks a combination but validates NEITHER knob.

### [SERIOUS] "Zero flips → not load-bearing" tested a PROXY, not the deployed decision (Lens B, C)
The flip test ran argmax(p120_model × reward_implied). The deployed decision is
argmax((0.4·p_model + 0.6·p_INDEPENDENT_market) × reward). Neither the prob input (no blend) nor the market
leg (reward-implied is the game-maker's own line, explicitly NOT the independent market the doctrine requires)
matches what actually picks — same class as league_sim2 / the score-logic confound (Verify-Std #2/#5).
MITIGATION: Lens B re-ran the real blend (reward-implied as market stand-in) → still 0 flips, and SA-Canada
keeps Canada with ~9.7 EV margin at 120'. So the CONCLUSION survives for SA-Canada (robust via LARGE MARGIN,
not via "zero model flips"), but **Mexico-Ecuador is a live flip-risk**: draw EV 35.2 @90' (Ecuador margin
only ~4) → transform drops draw to ~31 and widens Ecuador to ~10.6; under a draw-friendlier INDEPENDENT market
than reward-implied, the 90' pick could BE the draw and the transform would flip it to Ecuador. If real ET
attenuates supremacy, that flip could be an ERROR abandoning a field-thin +EV draw.

### [MINOR] Items to carry, not blockers
- ρ CI: ±0.081 is the 95% Wald half-width (=1.96·SE, SE=0.041) — fine, don't call it an SE. Exact
  Clopper-Pearson [0.564, 0.732].
- "Draws fall ~35%" (1−ρ=0.348, CI [0.268,0.436]) is statistically separable from naïve 50% (p=0.0006) and
  25% (p=0.012) — but cannot distinguish a 30% from a 43% fall. Point estimate good, precision modest.
- Poisson GOF: grouped χ² p=0.52 (not rejected, underpowered); 4-goal tail under-fit (obs 1 vs exp 0.22, n=1).
- ET-marginal independence essentially untested (only 6 both-score matches).
- Per-cell retention = ρ ONLY at the symmetric λ=1.15 calibration point; for asymmetric matchups it runs lower
  (SA-Canada 0.617 vs ρ 0.652) — directionally correct (lopsided ties less likely to survive ET).
- "16-match slate" → only 8 fixtures are in ko_build.py's games list; untested on the other 8.
- REGIME TRANSFER (all same-signed): WC-only ρ=0.679 > pooled 0.652; 48-team R32 admits more mismatches
  (underdog bunkers → rides to pens → higher conditional ρ); congested schedule → ET fatigue → fewer ET goals
  → higher ρ. All three say historical 0.652 if anything UNDER-states 2026 KO draw-retention — COMPOUNDS the
  supremacy bias (both under-price the KO draw).
- FIELD KO-draw share UNMEASURED. "Re-price draws down" is a TRUTH correction, NOT a standing "fade the draw."
  Pens-ignored scoring is counterintuitive → the recreational field may UNDER-pick the KO draw → the true
  13-25% 120' draw could sit ABOVE the field share = a prime field-thin +EV decorrelation BUY. Get the field
  share before treating the lower draw as a fade.
- SA-Canada 120' away% = 71.35 → prints **71**, not 72 (earlier over-round). Cosmetic.

---

## CORRECTED CONCLUSIONS

**CLAIM A — ship the CORE, strip the apparatus.** Deployable: ρ=0.652 (Clopper-Pearson [0.564,0.732]); the
identified even-match per-team ET rate ≈0.243; the transform mechanics (audited correct); "draws fall ~35%,
separable from 50%/25%." STRIKE: the [0.56,0.73] "sensitivity band" (degenerate — it's λ·φ that's fixed),
and "the goals-vs-retention coincidence resolves the tension / obviates a state-dependent model" (circular +
underpowered; the sample can't test state-dependence).

**CLAIM B — do NOT ship "not load-bearing" on the model-only test.** The SA-Canada pick (Canada) IS safe to
submit, justified by the LARGE EV margin (~9.7 at 120') under the real blend — NOT by "zero model-only flips."
Flag Mexico-Ecuador as the one R32 match where a draw-friendly INDEPENDENT line could make the transform
pivotal. "Leave ET supremacy un-attenuated" is an UNVALIDATED, possibly wrong-signed (toward chalk) assumption,
not a calibrated result, and the to-qualify cross-check ALONE cannot validate it.

**Ship status: directionally-correct v1.** Keep + apply the transform (free, correct, and re-pricing the KO
draw down is right). Pre-register two caveats: (i) ET supremacy is un-attenuated and possibly chalk-biased —
to discipline it, source the "result after ET, excl. pens" DRAW price (pins the level) PLUS to-qualify (pins
the split), not to-qualify alone; (ii) the lower KO draw is a truth correction, not an instruction to fade —
get the field's KO-draw share first. The real SA-Canada decision turns on the INDEPENDENT market (model Canada
65% vs reward-implied ~50%), not on this transform.
