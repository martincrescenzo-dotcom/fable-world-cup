# Live Tournament Updates — results, model-blind events, pick log

**Last scanned: 2026-06-12.** Update this every model run (see CLAUDE.md → "Model-blind scan").
The deployed model (v6) is fit on historical data and is BLIND to: injuries, suspensions,
lineups, and results after the data cutoff. This file is the manual overlay layer.

## Results log
| Date | Match | Score | vs model | Notes |
|------|-------|-------|----------|-------|
| 2026-06-11 | Mexico 2–0 South Africa | Mexico W | consistent (model 73%) | 3 red cards (1 Mex, 2 RSA) |
| 2026-06-11 | South Korea 2–1 Czechia | Korea W | consistent (model 41%; contrarian value pick hit) | Korea comeback |

## Pick performance (points game: base reward + rarity bonus, X2 held)
| Match | Outcome pick | Score submitted | Result | Base pts | Rarity bonus |
|-------|--------------|-----------------|--------|----------|--------------|
| Mexico–S.Africa | Mexico | 2–0 | 2–0 | ✅ 49 | **+20** (>30% crowd — obs #1) |
| S.Korea–Czechia | South Korea | 1–0 (as recommended) | 2–1 | ✅ 96 | — (score missed) |
| Canada–Bosnia | Canada | 3–0 | SUBMITTED | | |
| USA–Paraguay | Draw | 0–0 | SUBMITTED | | |
| Qatar–Switzerland | Switzerland | 0–3 | SUBMITTED | | |
| Brazil–Morocco | Draw | 0–0 | SUBMITTED | | |
| Haiti–Scotland | Scotland | 1–3 | SUBMITTED | | |
| Germany–Curaçao | Germany | 5–0 | SUBMITTED | | |
| Australia–Turkey | Turkey | 1–3 | SUBMITTED | | |
| Netherlands–Japan | Draw | 0–0 | SUBMITTED | | |
| Ivory Coast–Ecuador | Ecuador | 0–2 | SUBMITTED | | |
| Sweden–Tunisia | Draw | 0–0 | SUBMITTED | | |

**Running total: 165 pts (145 base + 20 bonus).**
**NB:** realized bonus tiers are observable even for scores we didn't pick (obs #2 = Korea 2–1 earned +20 for whoever had it → >30% crowd). User to report the realized tier of EVERY played match → ~1 calibration obs per match.
**Crowd calibration:** obs #2 VIOLATED the prior (est 26.8% vs realized >30%) → early refit: **beta 1.25→1.6, sal_strength 1.0→1.5** (crowd herds harder on iconic scores than assumed). Post-refit: Mexico OK (35.2%), Korea 29.0% — still 1pt below band edge; coarse-grid residual, expect resolution at obs #3. Strategic effect: iconic scores even MORE crowded → rare-score arbitrage (3-0/3-1 type, 50/70 tiers) STRONGER.

**X2 status: HELD** (usable anytime incl. KO — bar raised accordingly). Candidates auto-flagged by `matchday.py`.
**Standing (2026-06-12):** ~230,000th / >1M with 2nd-best-possible score (165) → top is dense; rare-score
bonuses = primary climbing instrument (VAR_TIEBREAK active). 1st ex-aequo (of 4) in friends league.
**Obs#2 provenance confirmed:** organizer email (first-party). Crowd params beta=1.6/sal=1.5 de-flagged.

## MD1 counterfactual selector ledger (pre-committed 2026-06-12 — score all three as results land)
| Match | pure-v6 pick | pure-market pick | SUBMITTED (maximin) |
|-------|--------------|------------------|---------------------|
| Canada–Bosnia | Canada | Canada | Canada |
| USA–Paraguay | Paraguay | USA | Draw |
| Qatar–Suisse | Switzerland | Switzerland | Switzerland |
| Brazil–Morocco | Morocco | Brazil | Draw |
| Haiti–Scotland | Scotland | Draw | Scotland |
| Germany–Curaçao | Germany | Germany | Germany |
| Australia–Turkey | Turkey | Turkey | Turkey |
| NL–Japan | Japan | Netherlands | Draw |
| CIV–Ecuador | Ecuador | Draw | Ecuador |
| Sweden–Tunisia | Tunisia | Sweden | Draw |

**Pre-commitments:** (1) NO parameter/strategy change on any single result; ledger adjudicates selectors
at ~15+ matches. (2) Tiers update crowd model only; results update ledger only. (3) Overlay errors
(e.g. Neymar plays) attribute to the OVERLAY layer, not the engine. (4) RESOLVED 2026-06-12: rules confirmed — bonus population = "% of players among those who got the
match winner right", NO temporal condition (tier model correctly specified). Tiers CONFIRMED accessible
for all matches (uncensored calibration stream). Both test-invalidators eliminated.

## Suspensions (model-blind, single-match)
| Player | Team | Misses | Model impact |
|--------|------|--------|--------------|
| **César Montes** | Mexico | vs South Korea (MD2) | starting CB out → Mexico DEF weaker THAT match (overlay −0.10 DEF) |
| Themba Zwane | South Africa | vs Czechia (MD2) | key attacking mid → RSA ATT weaker (−0.10 ATT) |
| Sphephelo Sithole | South Africa | vs Czechia (MD2) | midfielder (−0.05) |

## Injuries (model-blind, tournament-long) — DISCOUNT model "value" on these teams
| Team | Out | Severity | Overlay (ATT/DEF in log units; DEF higher=better) |
|------|-----|----------|---------------------------------------------------|
| Brazil | Rodrygo (ACL), Militão, Estêvão | moderate | −0.10 ATT, −0.08 DEF |
| Netherlands | Xavi Simons (ACL), De Ligt, Timber | moderate | −0.08 ATT, −0.10 DEF |
| Japan | Mitoma (hamstring) | significant | −0.12 ATT |
| Canada | Marcelo Flores (ACL) | minor | −0.05 ATT |
| France | Ekitiké | negligible | none (squad depth) |
| Germany | Gnabry, Karl | negligible | none |

## Overlay guidance (conservative — judgment, NOT a fitted model; player-leg failed validation)
- Key attacker out → −0.10 to −0.15 team ATT. Key defender/keeper out → reduce team DEF 0.08–0.12.
- Rotation/squad player → ignore.
- **Halve the overlay if the market / reward table already moved** (pre-tournament injuries are mostly
  priced in; in-tournament suspensions are usually priced by the game-maker too).
- Core use: when comparing model vs a reward table, an apparent model "value" on an injury-hit team may
  just be model-blindness — discount it.
