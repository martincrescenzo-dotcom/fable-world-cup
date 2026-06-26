# RED-TEAM REVIEW 2026-06-26 — Team stakes/motivation: does the field price it? does Opta? + the veto-collision

**Trigger:** user challenged my just-stated stakes framing on three fronts (field DOES price stakes; does Opta
really; Türkiye-USA should have *tempered* the override, not justified following the market). Load-bearing
(changes stakes-handling for all remaining group + KO picks). Tier-1, 3 lenses.

## VERDICT
**All three user challenges LAND. My framing was wrong in three ways; the spine (follow a stakes-aware sharp
market; overlay only confirmed-unpriced, halved) survives.** Corrected doctrine = the 4 gates now in CLAUDE.md
model-blind section (source gate, overlay, veto-collision, refined field lever).

## Q1 — Does Opta price stakes? **NO (data-integrity, with methodology sources).**
Opta supercomputer = Elo-derived Power Rankings + betting-odds input, 25k-sim Monte Carlo; Opta's own caveat:
"can't predict the human factors — injuries, rotation, individual moments." **Structurally the same stakes-blind
class as v6.** ⇒ "books AND Opta agree" is NOT independent confirmation of a STAKES effect (Opta is stakes-blind
AND partly book-derivative → double-counting). Only **sharp BOOKS price stakes** (lines move on rotation/team-news;
confirmed PASS — USA/Argentina rotation examples in WC2026 book copy). **Operational fix: the market leg "carries
stakes" only if it's a stakes-aware sharp source; a sim/reward-implied line does NOT → treat stakes as unpriced.**

## Q2 — Does the FIELD price stakes? **PARTLY — narrower than the user's "definitely," and my "under-prices" was
also wrong (statistician, n=18 w/ both field% & market logged).**
- Field over-backs favourites EVERYWHERE (+10.7pts over sharp market baseline) = fame/longshot-aversion, NOT stakes.
- Over-backing GROWS in low-stakes-fav matches: **+24.7 vs +10.7 (Δ+14), Mann-Whitney p≈.03, BUT power .58, n=3
  clean (Ecuador-Ger +29, Türkiye-USA +16, Egypt-Iran +29) + 2 pending.** Directional hypothesis, NOT validated.
- **The field DOES price salient draw-incentive:** Paraguay-Australia field draw 43% = market draw 43% exactly
  (Australia visibly playing for a draw). So "field under-prices stakes" (universal) is FALSE.
- Reconciliation: field prices **salient/visible** stakes, is blind to **fame-masked** stakes (sees "USA"/"Egypt",
  backs the name, ignores rotation/cagey-draw). Strategist's seam: attacks A & C are in tension — C only bites
  because the field DID pile on rotating USA (63% vs mkt 47%), i.e. the field did NOT price that stakes. Both true:
  field read the Paraguay draw, missed the USA rotation. Sign depends on salience, not a fixed direction.

## Q3 — Türkiye-USA: point C is CORRECT (strategist). The override was a CONFOUNDED-VETO error.
Our own MD10 scan (pre-pick) said "DEAD RUBBER, USA rotates heavily" and we overrode engine→USA anyway on the
USA-underrating veto. The veto's premise = "engine's anti-USA lean is PURELY a rating artifact." FALSE here: a
confirmed unpriced stakes signal (USA B-team) made USA genuinely weaker → the engine's Türkiye lean was right for
a NON-artifact reason. The veto "corrected" the engine UP to market-USA, stepping on a signal that AGREED with the
engine. Türkiye won 3-2. **Re-filed: NOT "stakes reads are dangerous, follow the market" — it's "we applied a
confounded artifact-veto and killed a legitimate field-fade decorrelation."** Caveat: market was a weak 47% USA
plurality → near-coin-flip, EV cost modest, mostly variance; do NOT update the USA-veto STRENGTH off this 1 point
(ledger 3/1). The PROCESS error (confounded veto) is the lesson.
DATA FLAG: the "63% field on USA" figure is NOT in our files (user/caller-supplied) — direction robust (any
field >47% = over-back), magnitude unverified.

## CORRECTED RULE (now in CLAUDE.md model-blind §; supersedes my 3-part rule)
1. Default: a verified stakes-aware SHARP market prices stakes → FOLLOW, no overlay (don't double-count).
2. SOURCE GATE: sims (Opta, v6) are stakes-blind; sim/reward-implied line ⇒ stakes UNPRICED ⇒ overlay-eligible.
3. OVERLAY: only confirmed AND demonstrably unpriced, pre-registered sign+size, HALVED; falsifiability test.
4. VETO-COLLISION: artifact-veto SUSPENDS when a confirmed unpriced stakes signal agrees with the engine → drop to
   coin-flip → rank levers decide. Veto full-strength only when the engine's lean is otherwise unexplained.
5. FIELD LEVER (refined): field over-backs FAMOUS favourites irrespective of stakes; fade only when a stakes-aware
   sharp line makes it ≤coin-flip AND field piled on it AND edge≥1 (4/4 prior contrarian losses → gate stays hard).

## MD11 IMPACT — picks UNCHANGED, and Egypt-Iran draw is REINFORCED.
Egypt-Iran is the textbook refined-lever case: field piled 71% on famous Egypt (vs market 42%), blind to the
cagey-draw stakes; stakes-aware sharp market makes the draw live (31%, EV-tied with Egypt); the draw is the
field-underpicked side, edge 1.01. So the existing Draw pick is the field-fame-bias decorrelation — validated, not
weakened. Spain/Belgium follows = high-stakes motivated favourites (not low-stakes), follow stands. CV-Saudi draw
= field already priced it (50%) → crowded, not a separator (as already noted).

## DEPENDS ON / standing
- Provenance of the market leg knowable each matchday (sharp-stakes-aware vs sim/reward-implied). If unknown → treat unpriced.
- "Unpriced" verifiable (line didn't move on the news) else overlay is unfalsifiable → follow.
- Stakes CONFIRMED (lineup/presser), not rumoured. Small-sample honesty: field-stakes lever power .58 → keep logging.
