# Strategy Audit — Fable World Cup Prediction System
*Date: 2026-06-15 | Perspective: modeling, mathematical statistics, odds/market theory, operations*

---

## I. MODELING

**Q1 — Is γ=1.5 a constant or should it be match-adaptive?**
The supremacy recalibration multiplies the log-strength-gap by γ=1.5 uniformly across all matches. This is validated on OOS log-loss but fit globally. Germany vs Curaçao and Brazil vs France have entirely different variance structures. Best-in-class: fit γ as a function of the strength differential (or fit separate γ for strong/balanced/weak matches). The fact that v7 home-advantage "overshot" suggests the model is already at the edge of over-sharpening for lopsided matches — γ may be too high for those and not high enough for contested ones.
**Status: OPEN**

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
**Status: OPEN — flagged in CLAUDE.md as "unvalidated prior"; root cause (correlation) not yet addressed**

**Q7 — Does the "Fair Game" insight support EV-max over a finite 13-person league?**
The fair-game result (EV ≈ K_match for any calibrated pick) is mathematically correct in expectation. But in a finite 13-person competition over 104 matches, the *distribution* of outcomes matters as much as the mean. Two players making identical EV picks have similar expected total points, but their rank depends on the *covariance* of their picks with the field. The league_sim2 finding (pure EV-max = 45% top-2) is a necessary condition for EV-max to be right, but not sufficient: it also assumes the simulation correctly models field distribution, rivals' strategies, and score variance across 100 actual WC matches — not 8 repeated ones.
**Status: OPEN — conceptually valid but simulation support is limited**

**Q8 — Is the league_sim2 K=12 result robust to the repeat-match structure?**
The simulation repeats the same 8 matches 12.5 times. This creates a specific pathology: rank variance across strategies is artificially low because every player faces identical match sequences. In reality, across 100 different matches, some are coin-flips and some are foregone conclusions. The conclusion "differentiation monotonically hurts" may be an artifact of the specific 8-match sample chosen (which included extreme games like Germany-Curaçao), not a general property of the 100-match tournament. A proper forward simulator uses the actual remaining schedule with realistic score distributions per match. Has this been cross-validated on a different 8-match sample?
**Status: OPEN — explicitly flagged in CLAUDE.md as a caveat; load-bearing claim not yet validated on actual schedule**

**Q9 — Is the crowd model form structurally misidentifiable at any sample size?**
Current form: `crowd ∝ plausibility^β × salience^γ`. This already misfits structurally at n=11 (violations in both directions). The mixture-population alternative — fraction α of pickers use pure salience, (1-α) use plausibility — has different structural predictions and may fit better. At n=20, if violations persist in both directions, the form is wrong, not the parameters. The identifiability question should be resolved before investing further in parameter estimation.
**Status: OPEN — misspecification suspected, acknowledged in CLAUDE.md; alternative forms not yet tested**

---

## III. ODDS / MARKET THEORY

**Q10 — Are you using the right de-vig method for 3-way markets?**
Current method: `imp[i] = (1/reward[i]) / Σ(1/reward[j])` (additive de-vig). For 3-way markets with 108–115% overround, the additive method systematically over-assigns probability to favorites and under-assigns to longshots. Professional standard is the power de-vig (Vincentian method) or the Shin model. For reward tables like (home 15, draw 179, away 222), the additive method overstates the home-win probability, which biases the `edge` signal on home wins and suppresses the `contrarian` flag for lopsided favorites.
**Status: OPEN — currently using additive everywhere**

**Q11 — Is Polymarket calibrated for European football specifically?**
The USA-Paraguay divergence (v6 44% Paraguay, PM 24%) is documented. The conclusion "market more reliable" is applied to Polymarket as a whole. But Polymarket's user base is heavily skewed toward US and crypto-native users with documented patriotic bias for US outcomes. European sharp books (Pinnacle, Betclic) are more calibrated for this market. If blending market probabilities into outcome picks, the blend weight should be calibrated market-by-market. The current approach uses one market and assigns it equal weight with the model everywhere.
**Status: OPEN**

**Q12 — Is the X2 threshold (E_total ≥ 45) derived from rank-utility theory or heuristic?**
X2 doubles total points if correct. Its value in a rank competition depends on current standing relative to rivals, matches remaining, and the distribution of future scores — not just E_total on the individual pick. A trailing player should use X2 more aggressively (variance-increasing); a leading player should withhold (variance-decreasing). The threshold of 45 is not derived from rank-utility structure. Best practice: model X2 value as a function of rank deficit and matches remaining using a forward simulator, then use X2 when rank-utility(use now) > rank-utility(wait).
**Status: OPEN — "HOLD through groups" policy is conservative but heuristic; correct framework not yet built**

**Q13 — In a parimutuel-like structure, does max-EV pick maximize rank probability?**
The game's reward structure is approximately parimutuel (reward ≈ K/p_true). In true parimutuel betting, maximizing EV is equivalent to picking proportional to true probabilities. But maximizing RANK is NOT the same — it requires picks that are *differentially accurate* relative to opponents. The classical result (Hausch-Ziemba) is that in a parimutuel, when the field over-bets favorites, the rank-maximizing strategy picks longshots even at identical EV. DIFF_BAND=0 discards this: it takes max-EV and accepts free differentiation only when it happens to align. The question is whether EV-per-pick and rank-separating-variance are being correctly traded off, or conflated.
**Status: OPEN — conceptual tension between fair-game EV and rank-utility not fully resolved**

---

## IV. OPERATIONS & IMPLEMENTATION

**Q14 — Does the pick audit trail link submission to the exact parameter snapshot?**
Picks are written to `prediction.md` by hand after running `matchday.py`. There is no automated record of which `crowd_params.json`, `deployed_params.json`, or Winamax snapshot version was active at run time. If `register_bonus.py` writes new params between a draft run and a submission run, the submitted pick may not match the documented parameters. Professional systems log `{match, pick, params_hash, run_timestamp}` atomically at submission time.
**Status: OPEN — manual log only; silent parameter drift already occurred (Ecuador 0-3→0-1 flip)**

**Q15 — Is the Winamax freshness gate robust to accidental misconfiguration?**
`WINAMAX_VALID_THROUGH` is a hardcoded date string in `matchday.py` requiring manual editing per matchday. If forgotten, stale (early-money, longshot-biased) Winamax data enters the model silently without any warning. Better: compare `snap_date` against `match_date - threshold_hours` at runtime and fail loudly if the snapshot is older than N hours relative to kickoff.
**Status: OPEN — manual constant, silent failure mode**

**Q16 — Is the SAL dictionary a validated prior or a pure belief prior?**
The salience values (1-0: 1.5, 1-1: 1.7, 0-0: 0.55, etc.) are entirely judgment-based and drive a non-trivial part of the crowd model. At n=11, there is enough data to at least test whether the relative SAL ordering is consistent with observed tier distributions — i.e., do high-SAL scores systematically appear in higher-crowd tiers? A Spearman rank correlation between SAL priors and observed crowd fractions would tell you whether the ordering is directionally right, even if the magnitudes are off.
**Status: OPEN — never tested; n=11 is now sufficient for a directional check**

**Q17 — Is BONUS_MODE='coarse' actually model-free, or does it inherit v6 biases?**
"Take modal score = highest-p score" is described as model-free and robust. But highest-p score is exactly v6's output. If v6 systematically overrates certain scores (Ecuador 0-1 was flagged as model-overrated), the coarse rule faithfully executes the model's error. The coarse rule removes the *crowd model* as a source of noise — it does not remove the *score model* as a source of error. When v6 is flagged as overrating a team, the coarse rule's modal score is the modal score of the flagged distribution, which may be wrong in a systematic direction.
**Status: OPEN — correctly labeled "not crowd-model-sensitive" in CLAUDE.md; v6 bias inheritance not addressed**

---

## Summary: Five Highest-Leverage Open Questions

| Priority | Issue | Risk level |
|----------|-------|------------|
| 1 | Q6: v6 and market are correlated estimators — ½/½ blend overstates information | **High — affects every pick** |
| 2 | Q8: league_sim2 repeat structure doesn't validate 100-match policy | **High — load-bearing strategy claim** |
| 3 | Q10: Additive de-vig biases `imp` toward favorites | **Medium — affects edge detection** |
| 4 | Q11: Polymarket calibration for EU football is unverified | **Medium — affects blend quality** |
| 5 | Q14: No atomic pick audit trail | **Operational — silent errors already occurred** |

---

*The system is sophisticated and self-aware about most of its risks. The biggest gap is that the two load-bearing decisions — the ½/½ blend (Q6) and the DIFF_BAND=0 policy (Q8) — rest on unvalidated assumptions or on a simulation that does not reproduce the actual 100-match tournament structure. These two items matter more than any crowd-model parameter.*
