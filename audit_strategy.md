# Strategy Audit — Fable World Cup Prediction System
*Date: 2026-06-15 | Perspective: modeling, mathematical statistics, odds/market theory, operations*

> **Review 2026-06-16 (post-MD2):** crowd obs now n=16 (#14–16 added), refit fired
> (`crowd_params.json` beta 1.6→1.0, sal 1.5→0.75). MD2 went 0/4 (4 favourites drew).
> Stale counts updated below (Q9, Q16); Q10 re-scoped (main market is ~0.5%-vig Polymarket,
> not a high-overround book); Q13 marked dependent on Q8; Q14 false example corrected.

---

## I. MODELING

**Q1 — Is γ=1.5 a constant or should it be match-adaptive?**
The supremacy recalibration multiplies the log-strength-gap by γ=1.5 uniformly across all matches. This is validated on OOS log-loss but fit globally. Germany vs Curaçao and Brazil vs France have entirely different variance structures. Best-in-class: fit γ as a function of the strength differential (or fit separate γ for strong/balanced/weak matches). The fact that v7 home-advantage "overshot" suggests the model is already at the edge of over-sharpening for lopsided matches — γ may be too high for those and not high enough for contested ones.
**Status: OPEN. Weak new signal (2026-06-16): MD2 went 0/4, all four favourites DREW — directionally consistent with γ over-sharpening contested matches, but n=4 is pure noise; do NOT act on it, log only.**

**Q2 — Is the attack/defense prior properly regularized?**
The Elo×market blend as a strength anchor is sensible, but how much weight does the prior get relative to the match-data likelihood? For teams with thin match history (Haiti, Curaçao, ~12 matches in `goals_records.json`), the anchor dominates — meaning predictions come from the prior, not data. Best practice: explicitly track posterior uncertainty per team as a function of data coverage; flag picks where the prior is doing >70% of the work.
**Status: OPEN**

**Q3 — Is independence of home/away goals validated for mismatch vs balanced games separately?**
Dixon-Coles ρ~0 is cited as a population-level validation. The joint model predicts score cells via `outer(nbv(lh), nbv(la))`, assuming each team's goal count is independent conditional on team strengths. For mismatch games (Germany-Curaçao), this assumption breaks: when one team dominates, the other's goal probability decreases (scoreline affects playing style). The 7-1 result is a case in point. Independence should be validated separately for balanced vs lopsided games.
**Status: OPEN**

**Q4 — Are the log-additive overlays (dATT, dDEF) on the right scale and validated?**
A −0.10 ATT overlay means the attack rate is multiplied by exp(−0.10) ≈ 0.905 — a 10% reduction. But the player-level model explicitly failed validation (`player_backtest.py`, MSE worse). The overlays are essentially a manual version of the failed model applied by judgment, with no held-out validation on suspensions or injuries. The same magnitude is applied regardless of whether the missing player contributes 5% or 30% of attacking output. Either (a) validate overlays on a suspension dataset, or (b) demote them to a qualitative confidence-discount flag rather than a quantitative λ adjustment.
**Status: OPEN — currently labeled "judgment, NOT fitted model" (CLAUDE.md) which is the right epistemic stance; quantitative application remains unvalidated**

**Q5 — Does the training data match the tournament context?**
The model is fit on `goals_records.json` (all results since 2022: qualifiers, friendlies, Nations League, tournaments). These populations have different goal rates, tactical profiles, and preparation contexts. Best-in-class tournament models apply competition-type weights or train exclusively on high-stakes international football. Has `mu_goals ≈ 0.20` been validated against World Cup group-stage distributions specifically?
**Status: OPEN**

---

## II. MATHEMATICS & STATISTICS

**Q6 — The ½/½ blend treats v6 and Polymarket as independent — are they?**
v6 anchors its attack/defense ratings partly to market group-winner odds (~60% common ancestry with the market). Blending two correlated estimators by averaging their point estimates underweights the correlation and overstates the information gain. The correct framework is a log-opinion pool or Bayesian combination: the optimal weight is proportional to each estimator's *independent* skill, not ½. The fix is not just "track log-loss until n=500" — it is to remove the correlated component from v6 before blending.
**Status: OPEN (TOP ITEM) — flagged in CLAUDE.md as "unvalidated prior"; root cause (correlation) not yet addressed. Note 2026-06-16: CLAUDE.md is now internally inconsistent — DECISION-MAKING REF prints p_blend=½/½ while OPEN CALIBRATION argues lean ~0.4 model/0.6 market. Reconcile, then address the correlation (remove the ~60% market-ancestry component from v6 before pooling).**

**Q7 — Does the "Fair Game" insight support EV-max over a finite 13-person league?**
The fair-game result (EV ≈ K_match for any calibrated pick) is mathematically correct in expectation. But in a finite 13-person competition over 104 matches, the *distribution* of outcomes matters as much as the mean. Two players making identical EV picks have similar expected total points, but their rank depends on the *covariance* of their picks with the field. The league_sim2 finding (pure EV-max = 45% top-2) is a necessary condition for EV-max to be right, but not sufficient: it also assumes the simulation correctly models field distribution, rivals' strategies, and score variance across 100 actual WC matches — not 8 repeated ones.
**Status: OPEN — conceptually valid but simulation support is limited**

**Q8 — Is the league_sim2 K=12 result robust to the repeat-match structure?**
The simulation repeats the same 8 matches 12.5 times. This creates a specific pathology: rank variance across strategies is artificially low because every player faces identical match sequences. In reality, across 100 different matches, some are coin-flips and some are foregone conclusions. The conclusion "differentiation monotonically hurts" may be an artifact of the specific 8-match sample chosen (which included extreme games like Germany-Curaçao), not a general property of the 100-match tournament. A proper forward simulator uses the actual remaining schedule with realistic score distributions per match. Has this been cross-validated on a different 8-match sample?
**Status: OPEN — explicitly flagged in CLAUDE.md as a caveat; load-bearing claim not yet validated on actual schedule. Note 2026-06-16: a real MD1+MD2 ledger now exists (~14 played matches with actual scores + crowd tiers) — the forward simulator should be backtested against THIS, not the 8-match repeat. The repeat-structure pathology Q8 describes is no longer the only option.**

**Q9 — Is the crowd model form structurally misidentifiable at any sample size?**
Current form: `crowd ∝ plausibility^β × salience^γ`. This already misfits structurally at n=16 — the 2026-06-16 refit (beta 1.6→1.0, sal 1.5→0.75) still leaves violations in BOTH directions (Mexico 2-0 28.5<30, Korea 2-1 25.9<30, Haiti 0-1 25.9>20), which is the diagnostic signature of a wrong functional form, not wrong parameters. The mixture-population alternative — fraction α of pickers use pure salience, (1-α) use plausibility — has different structural predictions and may fit better. **This question is now CONFIRMED, not suspected:** the form cannot fit heterogeneous score-herding (per CLAUDE.md). The identifiability question should be resolved before investing further in parameter estimation; meanwhile BONUS_MODE='coarse' correctly sidesteps it.
**Status: ESCALATED from OPEN — misspecification now confirmed (both-direction violations persist post-refit at n=16); alternative forms not yet tested. Bounded in impact by 'coarse' bonus mode.**

---

## III. ODDS / MARKET THEORY

**Q10 — Are you using the right de-vig method for 3-way markets?**
Current method: `imp[i] = (1/reward[i]) / Σ(1/reward[j])` (additive de-vig). For 3-way markets with 108–115% overround, the additive method systematically over-assigns probability to favorites and under-assigns to longshots. Professional standard is the power de-vig (Vincentian method) or the Shin model.
**Status (re-scoped 2026-06-16): LOW for outcome picks, residual for the crowd layer.** The market leg of the EV blend is Polymarket per-match 1X2 at **~0.5% vig** (`fetch_pm_matches.py`) — at that overround additive vs power/Shin de-vig differ by fractions of a percent, immaterial to edge/contrarian flags. The high-overround concern only touches (a) any de-vigged single-book 1X2 used as crowd *plausibility* and (b) Winamax score grids (143–152% overround) feeding the crowd layer — where shares are already soft + band-robustified, so the bias is second-order. Worth a power de-vig on the crowd layer for hygiene, but it is NOT a Medium-risk edge-detection problem as originally rated.**

**Q11 — Is Polymarket calibrated for European football specifically?**
The USA-Paraguay divergence (v6 44% Paraguay, PM 24%) is documented. The conclusion "market more reliable" is applied to Polymarket as a whole. But Polymarket's user base is heavily skewed toward US and crypto-native users with documented patriotic bias for US outcomes. European sharp books (Pinnacle, Betclic) are more calibrated for this market. If blending market probabilities into outcome picks, the blend weight should be calibrated market-by-market. The current approach uses one market and assigns it equal weight with the model everywhere.
**Status: OPEN**

**Q12 — Is the X2 threshold (E_total ≥ 45) derived from rank-utility theory or heuristic?**
X2 doubles total points if correct. Its value in a rank competition depends on current standing relative to rivals, matches remaining, and the distribution of future scores — not just E_total on the individual pick. A trailing player should use X2 more aggressively (variance-increasing); a leading player should withhold (variance-decreasing). The threshold of 45 is not derived from rank-utility structure. Best practice: model X2 value as a function of rank deficit and matches remaining using a forward simulator, then use X2 when rank-utility(use now) > rank-utility(wait).
**Status: OPEN — "HOLD through groups" policy is conservative but heuristic; correct framework not yet built**

**Q13 — In a parimutuel-like structure, does max-EV pick maximize rank probability?**
The game's reward structure is approximately parimutuel (reward ≈ K/p_true). In true parimutuel betting, maximizing EV is equivalent to picking proportional to true probabilities. But maximizing RANK is NOT the same — it requires picks that are *differentially accurate* relative to opponents. The classical result (Hausch-Ziemba) is that in a parimutuel, when the field over-bets favorites, the rank-maximizing strategy picks longshots even at identical EV. DIFF_BAND=0 discards this: it takes max-EV and accepts free differentiation only when it happens to align. The question is whether EV-per-pick and rank-separating-variance are being correctly traded off, or conflated.
**Status: OPEN — DEPENDENT ON Q8. Sharpened 2026-06-16: the Hausch-Ziemba precondition is actually MET here — CLAUDE.md confirms the field over-picks favourites vs reward-implied (CAN reward-implied 48% / actual picks 65%). Classical parimutuel theory then predicts a real longshot/contrarian RANK edge at equal EV — which directly CONTRADICTS league_sim2's "differentiation monotonically hurts." Both cannot be fully right. The contradiction resolves only when Q8's simulator is validated on the real schedule; until then DIFF_BAND=0 rests on a simulation that theory disputes. This is a genuine unresolved tension, elevated.**

---

## IV. OPERATIONS & IMPLEMENTATION

**Q14 — Does the pick audit trail link submission to the exact parameter snapshot?**
Picks are written to `prediction.md` by hand after running `matchday.py`. There is no automated record of which `crowd_params.json`, `deployed_params.json`, or Winamax snapshot version was active at run time. If `register_bonus.py` writes new params between a draft run and a submission run, the submitted pick may not match the documented parameters. Professional systems log `{match, pick, params_hash, run_timestamp}` atomically at submission time.
**Status: OPEN — but example CORRECTED 2026-06-16.** The original "silent parameter drift (Ecuador 0-3→0-1)" cite is WRONG: that flip was a documented, deliberate re-decision under the 8-obs refit (logged in CLAUDE.md SESSION 2026-06-14 cont. with full rationale) — not silent drift. Also, the audit understated existing controls: `preflight.py` already SHA256-verifies `attdef.json`/`wc_to_canon.json` against the `deployed_params.json` manifest before every run (catches *engine* drift). The genuine remaining gap is narrower than stated: no atomic `{match, pick, crowd_params_hash, winamax_snap_id, timestamp}` record bound to the SUBMITTED line. Worth adding (matchday.py append-on-submit), but no silent error has actually occurred — risk is Operational/Low, not "already happened."

**Q15 — Is the Winamax freshness gate robust to accidental misconfiguration?**
`WINAMAX_VALID_THROUGH` is a hardcoded date string in `matchday.py` requiring manual editing per matchday. If forgotten, stale (early-money, longshot-biased) Winamax data enters the model silently without any warning. Better: compare `snap_date` against `match_date - threshold_hours` at runtime and fail loudly if the snapshot is older than N hours relative to kickoff.
**Status: OPEN — manual constant, silent failure mode**

**Q16 — Is the SAL dictionary a validated prior or a pure belief prior?**
The salience values (1-0: 1.5, 1-1: 1.7, 0-0: 0.55, etc.) are entirely judgment-based and drive a non-trivial part of the crowd model. At n=16, there is enough data to test whether the relative SAL ordering is consistent with observed tier distributions — i.e., do high-SAL scores systematically appear in higher-crowd tiers? A Spearman rank correlation between SAL priors and observed crowd fractions would tell you whether the ordering is directionally right, even if the magnitudes are off.
**Status: OPEN — never tested; n=16 (was 11 at audit time) now comfortably sufficient for the directional Spearman check. Cheap, model-free, and would partially adjudicate Q9 (if even the ORDERING fails, the form is the problem, not just β). Recommend running this before any n=20 refit.**

**Q17 — Is BONUS_MODE='coarse' actually model-free, or does it inherit v6 biases?**
"Take modal score = highest-p score" is described as model-free and robust. But highest-p score is exactly v6's output. If v6 systematically overrates certain scores (Ecuador 0-1 was flagged as model-overrated), the coarse rule faithfully executes the model's error. The coarse rule removes the *crowd model* as a source of noise — it does not remove the *score model* as a source of error. When v6 is flagged as overrating a team, the coarse rule's modal score is the modal score of the flagged distribution, which may be wrong in a systematic direction.
**Status: OPEN — correctly labeled "not crowd-model-sensitive" in CLAUDE.md; v6 bias inheritance not addressed**

---

## Summary: Five Highest-Leverage Open Questions

*Re-prioritized 2026-06-16: Q10 demoted (main market is ~0.5%-vig PM), Q14 example corrected (no silent error occurred), Q9 promoted (misfit now confirmed), Q13 elevated (theory contradicts league_sim2).*

| Priority | Issue | Risk level |
|----------|-------|------------|
| 1 | Q6: v6 and market are correlated estimators — ½/½ blend overstates information (and CLAUDE.md now self-contradicts ½ vs 0.4/0.6) | **High — affects every pick** |
| 2 | Q8/Q13: league_sim2 repeat structure doesn't validate 100-match policy AND parimutuel theory (field over-bets favs) predicts the OPPOSITE of its "differentiation hurts" verdict | **High — load-bearing strategy claim, now with a theory conflict** |
| 3 | Q9: crowd functional form confirmed misspecified (both-direction violations persist post-refit at n=16) | **Medium — bounded by 'coarse' bonus mode** |
| 4 | Q11: Polymarket calibration for EU football is unverified | **Medium — affects blend quality** |
| 5 | Q16: SAL ordering never tested though n=16 now allows a cheap Spearman check | **Low — quick win, helps adjudicate Q9** |

*(Q10 demoted to Low: outcome EV uses ~0.5%-vig Polymarket, where de-vig method is immaterial. Q14 demoted to operational-hygiene: no silent error actually occurred; preflight already guards engine artifacts.)*

---

*The system is sophisticated and self-aware about most of its risks. The biggest gap is that the two load-bearing decisions — the ½/½ blend (Q6) and the DIFF_BAND=0 policy (Q8/Q13) — rest on unvalidated assumptions or on a simulation that does not reproduce the actual 100-match tournament structure. These two items matter more than any crowd-model parameter.*

*Review addendum 2026-06-16: this conclusion HOLDS and is reinforced — Q13 now shows parimutuel theory actively contradicts league_sim2's differentiation verdict (the field demonstrably over-bets favourites), so Q8 is not merely "unvalidated" but disputed by a competing model. Resolving the forward simulator (now backtestable on the real MD1+MD2 ledger, not the 8-match repeat) is the single highest-value build. The crowd-model items (Q9/Q16) are real but correctly contained by BONUS_MODE='coarse'; do not over-invest there. Two audit items were over-stated and have been demoted: Q10 (de-vig — main market is near-zero vig) and Q14 (no silent error actually occurred; the cited Ecuador flip was a logged deliberate decision).*
