# Executive summary — 2026-06-24

**State:** user = Lampadaire83, **#9 @1602** (23 bons / 4 exacts). Top-5 line #5 AdyFC **1785, gap 183**;
#7/#8/#9 bunched within **11 pts** (1613/1612/1602). X2 SPENT (Senegal, lost). MD9 picks stand (Canada 0-1,
Bosnia 1-0 pending; both already match corrected doctrine).

---

## LEARNED (new this session)
- **Meta-lesson (the big one):** in ONE session I shipped THREE wrong conclusions in a row — "decorrelation
  falsified on points" → "follow has an exact-conversion edge" → "follow-for-bons" — each corrected by the
  next. **All the arithmetic was correct; the INFERENCES were wrong.** Two named failure modes: (a)
  *underpowered null* (claiming "no difference" from `p>0.05` at n=23, power ~38%), (b) *wrong maximand*
  (optimizing bons when the objective is rank via reward-weighted points).
- **Decorrelation's realized record (1/8 hits; 138 vs a follow-counterfactual 364–484) is mostly VARIANCE,
  not proof** — favourites happened to win 7/8 in that window (a chalk artifact; the same period had a flood
  of favourite-draw upsets).
- **Exact-conversion by outcome type (measured, wide CIs):** draws ~50% (1-1), away-wins ~44% (0-1),
  home-favourite wins only ~19% (fat-tail dispersion). So following favourites has **no** exact-conversion edge.
- **Our exact rate vs the leaders is UNDERPOWERED — can't tell** (need ~70 obs/player; current p=0.13–0.78).
  The leaders' exact *lead* is driven mostly by more BONS (more correct outcomes), not proven better conversion.
- **The 3-agent adversarial review caught what single-context reasoning did not** — and is now worth running
  on any load-bearing claim.

## ADJUSTED (changed / reverted today)
- **Doctrine reverted to (with a harder gate):** OUTCOME = argmax **blend-EV** (0.4 model/0.6 market), **NOT**
  highest-probability; **selective HARD-GATED decorrelation kept as the rank lever** (blend-EV-max-or-within-5%,
  edge>1, market-confirmed, field clearly underpicked, ≤1–2/slate); SCORE = modal within outcome.
- **Maximand fixed:** RANK via reward-weighted POINTS. **Bons = secondary calibration diagnostic only.**
- **Retracted:** "decorrelation falsified", "follow-for-bons", "no score-skill gap / at ceiling", and the
  **fabricated ">35% hit-prob threshold"** (deleted — it was never derived or tested).
- **Built the RED-TEAM GATE** (institutionalized the review): `RED_TEAM_PROTOCOL.md` + `/redteam` skill
  (Tier-1 3-agent review) + a `UserPromptSubmit` hook injecting the Tier-0 self-check every turn.
- Calibration backlog cleared: crowd_obs 30 → 44 (MD7/MD8/MD9 tiers registered).

## KEPT (survived the challenge)
- **Score = modal within the chosen outcome** — validated at the score-cell level; the strategic fight is at
  the OUTCOME layer, not the score layer.
- **"Following = points, not rank"** — structural herd-competition truth; the session wrongly overturned it,
  now restored.
- **Decorrelation must be hard-gated**; the marginal ones (Croatia-draw, Senegal) were correctly flagged
  lower-conviction — the fix is a higher gate, not abandonment.
- **The X2-on-Senegal decision was process-sound** (clean PRIME spot; lost on the ~70% branch, not an error).
- **All session arithmetic** (138 vs 364–484, 7/8, 13.5% modal ceiling, every point reconciliation) — verified.

## OPEN (carry forward)
1. **Knockout scoring rule unknown** — does the game score the 90-minute result or the final result
   (incl. extra-time/penalties)? Decides whether draws remain a usable tool as favourites/underdogs converge.
   ASK the user.
2. **Do the leaders call CONTESTED matches better, or is their edge just bon-volume?** An outcome-model
   question (not a score question); needs ~70 obs to answer.
3. **Favourite/underdog convergence as the tournament advances** → model edge shrinks, lean market harder,
   expect lower per-match edges, variance rises (usable for a trailer, but gate hard).
