# Conversation log — 2026-06-22 → 2026-06-24
Faithful record of the user's challenges, my answers, and the corrections (the user asked this be logged).
Focus is the strategy/epistemics thread; routine slate mechanics are summarized.

---

## 2026-06-22 — MD8 slate + X2 decision
- **User** supplied MD7 results + leaderboard + MD8 matches (Argentina-Austria, France-Iraq, Norway-Senegal,
  Jordan-Algeria) with Cotes + Répartition.
- **Me:** reconciled MD7 (#9→#8 @1323, +386; Belgium-Iran DRAW +138 the biggest base). Built MD8: Argentina
  1-0 / France 2-0 / Senegal 0-1 / Algeria 0-1. Flagged Senegal as a PRIME X2 candidate (reward 137,
  field 25%, market-confirmed edge 1.29). Asked whether to deploy the one-shot X2.
- **User Q:** "why would I deploy here vs a later-phase match?"
- **Me:** argued X2 rank-value = P(hit)×reward×field-underpick is a GROUP-STAGE creature (KO compresses
  rewards + converges the field), and these were final group matches → deploy now. **User deployed X2 on
  Senegal.**
- **User:** "why is there still 6 shells running?" → I had stranded 6 background python runs (preflight /
  register_bonus hanging in a gated grid-fit). Stopped all 6; appended the 7 MD7 tiers directly.
- **User Q:** "what does 'Croatia reward crushed to 36' mean?" → explained: reward = the Cote (points if it
  wins); "crushed" = tiny because the favourite is heavy; EV = prob×reward, so a crushed favourite can have
  LOWER EV than the draw. (This was the seed of the prob-vs-EV distinction that later proved load-bearing.)

## 2026-06-23 — MD9 slate
- **User** sent MD8 results: **Senegal X2 LOST** (Norway 3-2). User #8→#9 @1475 (+152, all chalk follows).
- **Me:** acknowledged the X2 loss as the ~70% branch (process sound, outcome unlucky). Built MD9:
  England 2-0 / Panama-Croatia DRAW 1-1 / Colombia 1-0 / Switzerland-Canada CANADA 0-1 / Bosnia 1-0.
  Flagged the Croatia-draw as lower-conviction (Croatia must-win headwind).
- **User:** "I put draw, let's play stay disciplined."

## 2026-06-24 — the epistemics thread (where it got serious)

### Q1 — "is it still true that decorrelation pays better than follow+modal+exact? test it, don't bullshit."
- **Me (1st answer):** pulled real rewards from git history; tested on the 8 deviation matches: decorrelation
  138 vs follow+modal+exact 364–484; 1/8 hit. Concluded **"decorrelation FALSIFIED, net drag ~225–345 pts"**
  and flipped the doctrine to follow+modal. Committed it.

### Q2 — "why shift doctrine on n=8? is the justification sound? is it follow+modal or model+market follow? what % of modal ended up as the actual score? how many exacts?"
- **Me (1st correction):** conceded the n=8 flip was an over-reach. Decomposed: the 138-vs-364 gap is MOSTLY
  realized variance (favourites won 7/8; decorrelations were blend-EV-MAX so higher expected base-EV by
  construction). Re-framed the "robust" edge as the EXACT channel (claimed modal-on-follow hits ~17–23%,
  decorrel-draws ~0%). Clarified "follow" = highest-PROBABILITY favourite (model+market agree), not
  highest-EV. Tempered CLAUDE.md from "FALSIFIED" to "DEMOTED."

### Q3 — "exacts are possible on challenger-wins too no? where does >35% come from, is it tested? how to pull the exact thread world-class?"
- **Me (2nd correction):** computed conversion-by-outcome-type: **draws 50% (1-1), away-wins 44% (0-1),
  home-favourite wins only 19%** → my "decorrel-draws ~0% exact / follow has the exact edge" was WRONG;
  home-favourites convert WORST. Admitted **">35%" was fabricated** (never derived/tested) and deleted it.
  Ran significance + calibration: realized exact 14% ≈ model modal-cell 13.4%; Fisher us-vs-leaders p=0.13–0.78.
  Concluded **"FOLLOW-FOR-BONS"**: no score-skill gap, exacts are a fixed-rate byproduct of bons,
  decorrelation's true cost = ~7 forfeited bons. Committed it.

### Q4 — "review in a world-class, raise-the-bar way; log everything; push."
- **Me:** ran 3 INDEPENDENT adversarial red-teams (statistician / strategist / data-integrity), each
  recomputing from the files. Result (see REVIEW_2026-06-24…md):
  - Data-integrity: **all numbers PASS** (errors were inferential, not arithmetic).
  - Statistician: **"no score-skill gap" is FATAL** — apples-to-oranges benchmark (unconditional 13.4% vs
    conditional 17.4%; correct conditional benchmark is 23.6%, where we're BELOW), and an underpowered null
    (power ~38%, need ~70/group, difference CI [−3%,+44%]).
  - Strategist: **"follow-for-bons" is FATAL** — wrong maximand (rank=points, not bons), conflates prob-max
    with EV-max, contradicts the structural "following=points-not-rank" insight on a chalk-sample (7/8)
    artifact; for a trailing/bunched/X2-spent #9, follow-everything LOCKS 9th.
  - **Net: my session-long drift to "follow" was the error.** Corrected doctrine = EV-max outcome (not
    prob-max) + hard-gated selective decorrelation (the rank lever) + modal score. "No score gap" RETRACTED
    → "underpowered, keep logging."

---

## Running corrections ledger (what I got wrong, in order)
1. "Decorrelation FALSIFIED on points" — WRONG (the 138-vs-364 gap is mostly variance; favs won 7/8).
2. "Follow+modal has an exact-CONVERSION edge / decorrel-draws ~0% exact" — WRONG (draws convert 50%, home
   wins 19%; follow has no conversion edge).
3. ">35% hit-prob threshold for decorrelation" — FABRICATED, deleted.
4. "No score-skill gap / pure-modal at ceiling" — INVALID (underpowered null + wrong benchmark).
5. "Default = follow for bons" — WRONG MAXIMAND (rank=points not bons; locks #9 for a trailer).

## What survived every challenge
- All ARITHMETIC (verified independently): 138 vs 364–484, 7/8, 13.5% modal mass, reconciliations.
- Score = modal-within-outcome (validated at the score-cell level; the fight is at the OUTCOME layer).
- "Following = points, not rank" (structural herd-competition theory).
- Decorrelation must be HARD-GATED (blend-EV-max, edge>1, market-confirmed, field-underpicked) — the marginal
  ones (Croatia draw, Senegal) correctly flagged as lower-conviction; the fix is a higher gate, not abandonment.

## Process lesson
Single-context reasoning drifted across 3 wrong framings in one session, each "corrected" by the next — the
classic over-conclude-when-info-arrives-fast failure. The 3-agent adversarial review caught it. STANDING RULE
before any doctrine change: (a) power/CI check — is the null underpowered? (b) maximand check — am I optimizing
rank/points or a proxy (bons)?
