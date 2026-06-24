# RED-TEAM GATE — standing adversarial-review protocol

Why this exists: twice in this project a deployed conclusion was wrong because an **inference outran its
sample / optimized a proxy** (league_sim2; the 2026-06-24 "follow-for-bons" cascade — 3 wrong framings in one
session). A 3-agent adversarial review caught the second one. This protocol makes that review a STANDING gate
instead of a one-off. See the worked example: `REVIEW_2026-06-24_decorrelation-and-followforbons.md` +
`CONVERSATION_LOG_2026-06-22_to_24.md`.

The gate is TIERED so it is cheap by default and only spends agents when a claim actually matters.

---

## TIER 0 — SELF-GATE (apply inline to EVERY affirmation / answer / number; ~free)
Before asserting a substantive claim or answering a decision question, run these four checks and state the
result if any is non-trivial:

1. **POWER / CI.** If the claim rests on data: what is n, the confidence interval, and the power? A "no
   effect / they're the same / it's at ceiling" claim REQUIRES an equivalence or power argument — `p>0.05`
   alone is the *absence of evidence*, not evidence of absence. (Failure mode: "no score-skill gap" at
   n=23, power ~38%.)
2. **MAXIMAND.** Name the true objective out loud (here: RANK via reward-weighted POINTS). Am I optimizing
   IT, or a convenient proxy (bons, hit-rate, EV, accuracy)? A proxy that diverges from the objective at the
   exact point that matters is a trap. (Failure mode: "maximize bons" when bons ≠ points ≠ rank.)
3. **SAMPLE vs INFERENCE.** Is the conclusion bigger than n supports? Am I generalizing a small/biased
   sample (e.g. a chalk run where favourites went 7/8)? Flag "over-concluding when info arrives fast."
4. **MEASURED vs ASSUMED.** Separate computed facts from assumptions/counterfactuals; state residual
   uncertainty. (Note: in the 2026-06-24 case the *numbers* were all correct — the *inferences* were wrong.
   Getting the arithmetic right does NOT protect you.)

If all four pass cleanly → proceed. If any is shaky AND the claim is load-bearing → escalate to Tier 1.

## TIER 1 — FULL 3-AGENT RED-TEAM (on trigger; via `/redteam`)
**Triggers (any one):**
- the claim would CHANGE deployed doctrine, a pick, or a parameter;
- a number drives an IRREVERSIBLE / costly decision (X2 deploy, a submitted slate, a refit);
- the user CHALLENGES a conclusion, or asks "is it still true / test it / are you sure";
- I'm about to write "validated / falsified / proven / no gap / at ceiling / always / never".

**The three lenses (run as INDEPENDENT parallel agents — they must RECOMPUTE, not trust my numbers):**

| Lens | Mandate | Standard attacks |
|------|---------|------------------|
| **A. Statistician** | attack the inference | recompute every stat; power & CI; is "no effect" an underpowered null? conditional vs unconditional benchmark; right denominator; multiple comparisons / pooling dilution; equivalence test |
| **B. Strategist / decision-theory** | attack the objective & logic | is the maximand the true objective? proxy divergence; EV vs probability; sample-specific vs structural; rank dynamics for a trailing/bunched player; circular reasoning; what does the answer DEPEND on |
| **C. Data-integrity** | recompute every number from raw files | re-derive each quantity independently; PASS/FAIL table; flag unstated assumptions & counterfactuals; check reconciliations & arithmetic |

Then SYNTHESIZE: label findings [FATAL]/[SERIOUS]/[MINOR], adjudicate collisions (structural argument beats
one-sample inference), and write the corrected conclusion. Persist a `REVIEW_<date>_<topic>.md`.

**Agent-prompt templates** (fill `{CLAIM}`, `{DATA/FILES}`, `{OBJECTIVE}`): see the three prompts used on
2026-06-24, preserved verbatim at the bottom of this file as the canonical templates.

---

## OUTPUT DISCIPLINE
- Lead with the verdict and the [FATAL]/[SERIOUS]/[MINOR] labels, not a narrative.
- "Numbers correct, inference wrong" is a valid and common outcome — say so explicitly when it happens.
- When two conclusions collide, the STRUCTURAL one (theory true regardless of this sample) beats the
  one-sample empirical one.
- Update CLAUDE.md + memory + the relevant ledger; commit with the review file.

---

## CANONICAL AGENT-PROMPT TEMPLATES (reuse for `/redteam`)

### Lens A — Statistician (adversarial)
> You are a world-class statistician doing an ADVERSARIAL review. Find every flaw in the inference below —
> RECOMPUTE independently from the data, don't trust the stated numbers. Be sharp, no politeness.
> CLAIM(S): {CLAIM}. DATA/FILES: {FILES}. For each claim: recompute it; then attack — power & CI (is a
> "no-difference/at-ceiling" claim an underpowered null? what n would be needed? what's the difference-CI?);
> conditional-vs-unconditional benchmark mismatches; wrong denominators; pooling/multiple-comparison
> artifacts; missing equivalence test. DELIVERABLE: prioritized [FATAL]/[SERIOUS]/[MINOR] list, each with the
> corrected number or the precise reason the inference fails, and a one-line verdict on whether the headline
> is defensible. Show the python you ran.

### Lens B — Strategist / decision-theory (adversarial)
> You are a world-class decision theorist doing an ADVERSARIAL review. The true OBJECTIVE is {OBJECTIVE}.
> CONCLUSION TO ATTACK: {CLAIM}. Read {FILES} for context. Attack: is the maximand the true objective or a
> proxy that diverges where it matters? EV vs probability conflation? is the empirical backbone
> sample-specific vs structural? does it contradict a previously-established structural insight without
> refuting it? rank dynamics for the actual standing/constraints? circularity? DELIVERABLE: prioritized
> [FATAL]/[SERIOUS]/[MINOR] list; adjudicate the core tension and state what the answer DEPENDS on; sharpest
> honest verdict.

### Lens C — Data-integrity (auditor)
> You are a meticulous reproducibility auditor. Independently RE-DERIVE every quantitative claim below from
> the raw files; run code. CLAIMS: {CLAIM}. FILES/ENGINE: {FILES}. DELIVERABLE: a PASS/FAIL table with your
> independently-computed value for each; flag any number that doesn't reproduce and any claim resting on an
> unstated assumption or counterfactual. Show key outputs.
