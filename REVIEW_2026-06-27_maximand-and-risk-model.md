# RED-TEAM REVIEW 2026-06-27 — should the risk model change now that the user is #4 and wants to climb?

**Trigger:** user jumped #8→#4 (+568, 3 exacts); said they are not satisfied holding top-5, want to keep climbing;
explicitly asked to involve the red-team on whether to change the risk model. Load-bearing (maximand-level).

## My proposed verdict (the thing attacked)
(a) upgrade maximand P(top-5) → maximize E[rank]/P(top-2-3), top-5 a soft floor we'll risk; (b) KEEP hard-gated
selective-decorrelation as the climbing lever (bunch ahead = chalk bloc, copying freezes the gap); (c) allow 2-3
decorrelations/slate instead of 1-2; (d) lean harder into exacts-on-follows; (e) refuse gate-loosening & #1-chase.

## VERDICT: my verdict was substantially WRONG. Three lenses converged. Corrected below.

### [FATAL] The "chalk bloc ahead to decorrelate against" frame is dead — twice.
- **Unmeasurable:** we hold only cumulative (goods, exacts) scalars; "chalk follower" is a pick-correlation
  statement that CANNOT be recovered from a good-count under any n. 100% assumed.
- **Directionally wrong:** of the three 41-goods players I called "the bunch ahead," TWO are BELOW the user
  (#6 Alexis −55, #7 CrazyBE −83). Only #2 Nicolas (+73) is ahead. Real climb targets = Nicolas (+73) and Hadri
  (+1 = noise). Decorrelating "to pass the bunch" mostly targets players already being beaten — despite them
  having MORE goods (41 vs 36), i.e. more goods ≠ more points.

### [FATAL] The decorrelation=rank-lever doctrine was derived from BELOW the bunch; the user is now IN it.
Below the pack, EV-neutral variance is rank-CONVEX (a hit vaults through a stack, a miss barely moves you) — that
asymmetry is the entire reason it was E[rank]-positive. Mid-bunch (#4, cluster ~22 pts/rank, downside −55/−83
THICKER than upside +73/+1), the points→rank map is locally linear/symmetric ⇒ EV-neutral variance is
E[rank]-neutral-to-NEGATIVE. So (c) "more decorrelations" pushes variance the wrong way — the SAME class of error
the killed "inversion" doctrine was retired for, sign-flipped. **Reject (c).**

### [FATAL] Maximand upgrade is unanchored without the payoff convexity over rank.
Variance-seeking vs averse is set entirely by convexity of payoff(rank). Flat/floor-prize → protect floor, ~zero
variance. Convex podium → gamble. "User wants to climb" is a preference, not a payoff function. MUST be resolved
before (a)-(e). → ASKED the user.

### [SERIOUS] Wrong axis. Two variance axes are not equivalent.
Outcome-decorrelation risks the BASE reward = the floor. Score variance (rarer-but-live exact within a near-locked
outcome) forfeits only the bonus delta — floor-safe. For a must-climb-but-thin-cushion player, floor-safe variance
strictly dominates. And the rivals who actually stand between the user and #2-3 (Hadri 11 exacts, AdyFC 12) are
off-chalk exact-hunters — decorrelating against the FIELD's outcomes does nothing against THEM.

### [SERIOUS] My (d) was self-contradictory.
"exacts-on-FOLLOWS with MODAL scores": modal = most popular = low tier (+20) AND rivals are on it too → freezes
the gap on the score axis, exactly the critique leveled at outcome-following. Rank-productive exacts come from
clear-favourite margin-spread games where the modal cell is ALREADY a non-herd +50 score (Colombia 1-0 +127,
Paraguay 0-0 +50), not herd-modal draws. (Caveat: the project backtest still found pure-modal > step-off on realized
bonus, n=20 underpowered — so do NOT systematically abandon modal for rare cells; prefer modal, harvest it on clear
games.)

### [FATAL] +568 is a ~4σ, n=1 tail (P(≥568)≈0; P(≥3 exacts in 6)≈3.5%). Non-diagnostic. Do not update on it.

### Confirmed clean: (e) no #1-chase (354 ≈ unreachable w/o −EV gate-loosening), no contrarian gate-loosening (4/4
losses). Data-integrity: all leaderboard arithmetic PASSES; user is genuinely EV-efficient (points-per-good #2/9,
base-points-per-good #2/9 robust to bonus assumption) — but "exacts are THE separator" is underpowered at n=9
(r(exacts,rank)=−0.557 vs r(goods,rank)=−0.364; difference not significant). Directional, not proven.

## USER'S ANSWER (resolves the [FATAL] open dependency) — and it kills the bad half of the verdict for free
> "we proved we can do solid score prediction WITHOUT strategizing rank and chase topics … I want to see how far
> our approach can lead us, whether it is #6 or #1 … I would not like to be 6th, but I would even more not want to
> miss an occasion to continue building the model and the way we use it … I believe we can do good independently of rank."

**The maximand IS: maximize genuine predictive quality / EV via the disciplined model + process; rank is the
SCOREBOARD, an OUTCOME of good process, not the objective function.** This is NOT a convex rank-gamble.

## CORRECTED DOCTRINE (deployed)
1. **Maximand = disciplined EV-max prediction.** Rank is downstream; do not strategize toward a rank target, do not
   trade EV for variance to climb, do not trade EV for safety to defend. Falling to #6 is an acceptable byproduct;
   process integrity + model-building is the priority.
2. **Outcome = blend-EV-max (0.4 model + 0.6 market) FOLLOW.** Decorrelate ONLY when the field-underpicked outcome
   is ALSO EV-max (or within the ~5% band) — free differentiation, taken because it's the right pick, NOT to chase
   rank. Reject (c): NO raising the decorrelation count for rank reasons. Mid-bunch, outcome variance is the only
   axis that risks the floor AND is E[rank]-neutral-to-negative — so there is no rank reason to add it.
3. **Score = pure modal (validated).** Rank-bonus comes naturally from clear-favourite margin games where the modal
   cell is already a non-herd score; do not gamble rare cells.
4. **Veto model artifacts toward the independent market** (DR Congo/Uzbekistan-class) and apply stakes only through
   the gated 5-step protocol (user: keep stakes light, no freehand narrative).
5. **Keep BUILDING:** the unbuilt KO ET re-allocation (draws re-price down for 120-min KO scoring) is the next real
   model-building task when knockouts begin.

## What still CANNOT be inferred (state plainly): any rival's pick style/correlation/field%, per-player exact tiers,
the prize structure. All strategic claims about rivals' styles are assumption, not data.
