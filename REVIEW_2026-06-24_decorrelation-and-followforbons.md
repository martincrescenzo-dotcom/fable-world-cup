# World-class adversarial review — 2026-06-24
## Subject: the session's "decorrelation falsified → follow-for-bons" conclusion

Method: three INDEPENDENT red-team agents, each re-deriving from the raw files (not trusting my numbers):
(1) a statistician attacking the inference, (2) a decision-theorist attacking the strategy/objective,
(3) a data-integrity auditor recomputing every quantity. Verdict below supersedes the intra-session
"follow-for-bons" doctrine. This document is the raise-the-bar audit the user asked for.

---

## TL;DR — the conclusion was WRONG; the numbers were RIGHT

Data-integrity audit: **every quantitative claim reproduced exactly** (44 obs; model modal-cell mean 13.5%;
realized actual==modal 6/44=13.6%; decorrelation 138 vs follow 364–484; favourites won 7/8; all point
reconciliations; the counterfactual modal scores Ghana 1-0 / Mexico 1-0 / Croatia 0-1 are ENGINE-VERIFIED,
not assumed). So the errors were in INFERENCE, not arithmetic — the most dangerous kind, because correct
numbers made wrong conclusions look solid.

The two substantive conclusions FAIL adversarial review:
- **"No score-skill gap / pure-modal at ceiling"** = an underpowered null built on an apples-to-oranges benchmark.
- **"Default = follow highest-probability outcome for bons"** = optimizing the wrong maximand (bons, not
  reward-weighted points/rank), conflating prob-max with EV-max, and overturning the correct
  "following = points-not-rank" insight on a chalk-sample artifact.

---

## 1. Statistical red-team (FATAL × 2)

**[FATAL] Apples-to-oranges benchmark.** I compared the model's *unconditional* mean modal-cell mass (13.4%)
to our *conditional-on-correct-outcome* exact rate (4/23 = 17.4%) and to the unconditional realized rate
(6/44 = 13.6%). Only the two unconditional numbers are comparable. The correct yardstick for a
conditional-on-correct-outcome rate is **P(modal cell | modal outcome correct) = 23.6%** (agent-computed,
per-match range 12–44%). Against THAT, our 17.4% is **~6 pts below**, not "at ceiling." The "at ceiling /
calibrated" framing borrowed an unconditional number to flatter a conditional rate.

**[FATAL] Underpowered equivalence dressed as a positive finding.** 95% CI on 6/44 = **[5.2%, 27.4%]** (a 5×
span) — consistent with calibration AND with a true rate half or double the model's. No equivalence test was
run. And the leader comparison: Fisher us 4/23 vs Hadri 11/29 p=0.13 (verified), but **power ≈ 38%** to
detect a 17%→38% gap at this n; you'd need **~70 per group**. The 95% CI on the Hadri−us conversion
difference is **[−3%, +44%]**. "p=0.13 → no gap" is backwards: the test was far too weak to find the gap even
if it is real and large. Pooling the top-3 (→ p=0.78) DILUTES the one candidate signal (Hadri) rather than
testing it.

**[SERIOUS] Conversion-by-outcome-type orderings not assertable.** draws 7/14 (50%), away-wins 4/9 (44%),
home-wins 19% — but CI half-widths are ±26% / ±33% / ±21%. The intervals overlap massively; "draws convert
better than home wins" is not supported at this n. (These are also *tournament score compositions*, not
conversion rates of our picks.)

**[KEPT — the one solid kernel] Exacts are mechanically downstream of outcome accuracy.** The model's modal
*outcome* matches the realized outcome only **52% (23/44)** of the time; when the outcome is wrong the exact
cannot hit. So a large share of exact-misses is outcome-driven — which argues for measuring conversion
CONDITIONALLY (the comparison I botched), not for "no score skill."

**Statistical verdict:** "No score-skill gap" is an underpowered null. Defensible statement: *"At n=23–44 we
have no power to detect a plausible-sized score-conversion gap (need ~70/group); our conditional exact rate
is ~17% with a CI consistent with anything from a real deficit to parity. Keep logging."*

---

## 2. Strategy red-team (FATAL × 2)

**[FATAL] "Maximize bons" optimizes the wrong quantity.** The game scores reward-weighted POINTS; rank =
argsort(points), never argsort(bons). A bon on France (22) ≠ a bon on a draw (138) — 6.3×. The vertical
spread at the TOP of the league is reward-weighting + exacts, not bon-volume (CrazyBE 27 bons/3 exacts ≈
AdyFC 25 bons/8 exacts in points; several players have bon-counts at/near the user's). The 364-vs-138
deviation result is real but SAMPLE-SPECIFIC: those were crushed-reward chalk matches (France 22, Croatia
36). On a compressed line a 30%-underdog at reward 137 (EV≈41) routinely beats a 60%-favourite at reward 65
(EV≈39) — so "highest-probability" ≠ "highest-EV," and the follow-default conflates them.

**[FATAL] Contradicts the load-bearing "following = points, not rank" insight without refuting it.** That
insight was independently re-derived ≥4× (MD6–MD9) and is basic herd-competition theory: a favourite's
reward is table-stakes (you + the herd + #5 all bank it together → rank-relevant variance ≈ 0). You cannot
pass a player 180 pts ahead by making the same EV they make. The session reframed the decorrelation *losses*
as "decorrelation costs bons" — selection on the dependent variable — while ignoring that the **single
biggest base of MD7 (+138) was a decorrelation** (Belgium-Iran draw) and the #12→#9 jump came from
exacts + contrarian calls. When two conclusions collide, the structural one (herd theory) beats the
one-sample inference.

**[SERIOUS] The 7/8 favourites-won backbone is a chalk artifact.** The same window logged a flood of
favourite-draw UPSETS (England 0-0 at mkt 81%, Ecuador 0-0, Spain 0-0, Uruguay 2-2, "THREE upsets" in MD7).
If favourites truly convert ~55–65%, the math inverts: each favourite-draw upset is the maximum
rank-separation event (whole herd takes 0, the decorrelator banks a high-reward base). Abandoning the lever
on an 8-match chalk run is overfitting to variance (Verify-Std #4/#7).

**[SERIOUS] For trailing/bunched/X2-spent #9, follow-everything is the one strategy that CANNOT reach top-5.**
P(overtake a bunched field ahead) is increasing in your variance relative to the field, conditional on
non-negative EV. Following = minimum relative variance = freezes rank. With the X2 spent, selective
decorrelation is the ONLY remaining rank lever. EV-neutral variance ≻ EV-neutral copying for a trailer.

**[SERIOUS] "Exacts are a byproduct of bons" is circular AND harvests the cheapest exacts.** The rare,
high-bonus tiers (+70/+100) live on non-modal, low-probability, high-reward scores (underdog wins, unusual
draws) — exactly what follow+modal never picks. Follow+modal systematically collects the +20 (2-0/1-0) tier
and never touches the fat tail.

**Strategy verdict:** Right default = **EV-max outcome (NOT highest-probability) + hard-gated selective
decorrelation (blend-EV-max within band, edge>1, market-confirmed, field clearly underpicked) + modal score
within the chosen outcome.** "Follow for bons" demotes to "the correct pick on the SUBSET where the favourite
is also blend-EV-max and no field-underpicked +EV alternative exists." The session threw out the mechanism
when it should have tightened the filter.

---

## 3. Data-integrity audit (ALL PASS)

| Claim | Result | Value |
|---|---|---|
| crowd_obs = 44; draws 14 {1-1:7,0-0:4,2-2:3}; home 21; away 9 | PASS | exact |
| model modal-cell mean / realized hit | PASS | 13.5% / 6 of 44 (0 name-resolution failures; "43" was a chosen denominator) |
| decorrelation 138 vs follow 364 (+3 exacts → 484) | PASS | 46+38+73+69+38+64+36=364; exacts Mexico +50/Ghana +20/Croatia +50 |
| counterfactual modal scores Ghana 1-0 / Mexico 1-0 / Croatia 0-1 | PASS (ENGINE-VERIFIED, not assumed) | argmax in favourite win-region |
| 7/8 favourites won; 23+7=30 ≈ leaders | PASS | |
| MD7 +386 / MD8 +152 / MD9 +127 reconciliations | PASS | exact |

Only correction: n=44 (I said 43 in places); immaterial.

---

## 4. CORRECTED DOCTRINE (replaces "follow-for-bons")

1. **Objective = RANK (top-5), via reward-weighted POINTS. Bons are a SECONDARY calibration diagnostic, never
   the maximand.**
2. **Outcome pick = argmax blend-EV (0.4 model + 0.6 market), NOT highest-probability.** On compressed reward
   lines these diverge; take EV-max.
3. **Selective decorrelation is the rank lever and stays** — but HARD-GATED: only when the field-underpicked
   outcome is blend-EV-max (or within the ~5% DIFF band), edge = market_p/reward-implied_p > 1,
   market-confirmed, and the field clearly underpicks it. ≤1–2 per slate. It is EV-neutral variance, which a
   trailing player needs; the losses are variance, not an EV leak (provided the gate holds).
4. **Score = modal within the chosen outcome (UNCHANGED — validated at the score-cell level).** The fight is
   at the OUTCOME layer, not the score layer.
5. **"No score-skill gap" → RETRACTED.** Replace with: underpowered (need ~70/player); our conditional exact
   ~17% may be BELOW the model-conditional-expected ~23.6%; keep logging, revisit at ~70 obs.
6. **Favourite-conversion is NOT 7/8** — treat it as ~55–65% with heavy draw-upset variance; this is what
   makes gated decorrelation +rank.

## 5. Process lesson (for the meta-log)
This is the SECOND time this project's deployed doctrine was wrong because an inference outran its sample
(first: league_sim2). The intra-conversation reasoning drifted across THREE framings in one session
("falsified on points" → "follow has exact-edge" → "follow-for-bons"), each corrected by the next. The
adversarial 3-agent review caught what single-context reasoning did not. STANDING RULE: before shipping any
doctrine change, run the power/CI check (is the null underpowered?) and the maximand check (am I optimizing
points/rank or a proxy?). See CLAUDE.md Verify-Std #4/#6/#7.
