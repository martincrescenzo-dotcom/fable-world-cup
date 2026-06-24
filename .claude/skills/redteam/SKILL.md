---
name: redteam
description: Run the Tier-1 three-agent adversarial red-team (statistician + strategist + data-integrity) on a specific claim, conclusion, or decision before it ships. Use when a claim would change deployed doctrine/picks/params, when a number drives an irreversible decision (X2, a slate, a refit), when the user challenges a conclusion or says "test it / are you sure / is it still true", or before writing "validated/falsified/proven/no gap/at ceiling". Args = the claim to attack (free text); if omitted, red-team the most recent substantive claim in the conversation.
---

# /redteam — Tier-1 adversarial review

You are running the **Tier-1 gate** from `RED_TEAM_PROTOCOL.md`. Goal: try to BREAK the claim before it
becomes doctrine, not to confirm it. Read `RED_TEAM_PROTOCOL.md` first if not already in context.

## Steps
1. **State the target precisely.** Write the exact CLAIM(S) under review, the OBJECTIVE they serve (for this
   project: RANK via reward-weighted points), and the DATA/FILES needed to check them. If args are empty,
   use the most recent substantive claim/answer in the conversation.
2. **Spawn the three lenses as INDEPENDENT parallel agents** (one message, three `Agent` calls, so they run
   concurrently). Use the canonical templates at the bottom of `RED_TEAM_PROTOCOL.md`, filling
   `{CLAIM}`/`{FILES}`/`{OBJECTIVE}`. Mandates:
   - **A. Statistician** — recompute every stat; power/CI; underpowered-null & benchmark/denominator traps.
   - **B. Strategist** — maximand vs objective; proxy divergence; sample-specific vs structural; rank dynamics.
   - **C. Data-integrity** — re-derive every number from raw files; PASS/FAIL table; flag assumptions.
   Each agent MUST recompute, not trust the stated numbers, and label findings [FATAL]/[SERIOUS]/[MINOR].
3. **Synthesize.** Lead with the verdict. Reconcile collisions (structural argument beats one-sample
   inference). State explicitly if the pattern is "numbers correct, inference wrong." Give the corrected
   conclusion.
4. **Persist & propagate.** Write `REVIEW_<YYYY-MM-DD>_<topic>.md`; update CLAUDE.md + memory + the relevant
   ledger if the verdict changes anything; commit with the review file (auto-push per CLAUDE.md).

## Guardrails
- Do NOT soften the agents' mandate to be "balanced" — their job is to find flaws. Praise is not a finding.
- If all three lenses pass cleanly, say so plainly (a clean pass is a real result) — but only after they
  genuinely tried to break it.
- Scale the spawn to the stakes: a doctrine change merits all three; a routine number can be a single
  data-integrity recheck. Don't burn three agents on something Tier-0 already settles.
