# Live Tournament Updates — results, model-blind events, pick log

## ════ CURRENT STATE SNAPSHOT (2026-06-15) — read this first; rows below are edit history ════
**Objective:** TOP-2 of 13-person friends league. **User: 9th/13, 374 pts** (5 winners, 1 exact). 
**Friends league full MD1 standings (12 matches played):**
 #1 997 (10W/3E) | #2 542 (7W/2E) | #3 493 (7W/1E) | #4 441 (6W/1E) | #5 436 (6W/1E) | #6 411 (6W/2E) | #7 405 (5W/1E) | #8 389 (6W/1E) | **#9 USER 374 (5W/1E)** | #10-13 unknown.
**Gaps:** to #8: 15 | to #7: 31 | to #6: 37 | to #5: 62 | to #4: 67 | to #3: 119 | to #2: 168. ~92 matches remain.
**MD1 fully resolved (12 matches):** 5/12 correct outcomes, 1/12 exact score (Mexico 2-0). 
 5 hits: Mexico✅+20 | Korea✅ | Brazil-Morocco Draw✅ | Germany✅ | Sweden✅
 7 misses: Canada | USA | Qatar-Swiss | Haiti-Scotland | Australia-Turkey | NL-Japan | CIV-Ecuador
**Running total: 374 pts** (69 Mexico + 96 Korea + 122 Brazil-Morocco + 15 Germany + 72 Sweden).
**Sweden-Tunisia tier: +100** (5-1, model est 0.2% → OK; we picked 1-0 so bonus not ours — calibration only).
**Strategy (settled):** pure blend-EV-max — LEAGUE_MODE, **DIFF_BAND=0**, COARSE scores (modal/highest-p, step off 1-1 only).
**X2 boost: HELD.** Use only on SIGNIFICANT + model-market-AGREED high-E match. Anytime incl. knockouts.
**PENDING (ask user):** (1) Sweden-Tunisia tier; (2) MD2 reward tables + fresh Winamax/Polymarket.
**OPEN LOOSE ENDS:** (1) Blend weight ½/½ unvalidated. (2) Crowd model 13 obs / 6 violations — accumulate to 15 for refit. First DIRECT 0-0 obs (Spain-CV) landed at +50, model est 17.8% OK → 0-0 tier-50 thesis gets its first support. Sweden 5-1 +100 (est 0.2% OK) = 2nd tail obs nailed.

## CHALLENGE AGENDA — stress-test assumptions as evidence accumulates; surface proactively at each trigger
**1. Crowd model refit — trigger: ≥15 obs (currently 13)**
6/11 violations; beta/sal near-unidentified on a misfit form. At 15 obs: refit once, then test whether
`plausibility^β × salience` can structurally fit the data or needs a richer form (per-score-type effects).
Known failure modes: draw scores (1-1, 2-2) under-estimated; home-win 1-0 over-estimated.

**2. Blend weight ½/½ model-market — trigger: ~30-40 match results on ledger**
Currently a prior, not fit. Method: per-match log-loss of v6 / market / blend on running results ledger.
Flag if ledger shows consistent direction (toward 0.4/0.6 or 0.3/0.7). Report range + robust vs fragile
conclusions. Note: ~100 WC matches won't tightly identify weight (need ~500); stay honest about CI width.

**3. Outcome selector ledger — trigger: ≥15 contested flips (currently ~10)**
2-2 so far (Korea/Brazil-Draw correct; USA/Haiti wrong). At 15+: adjudicate v6 vs market vs maximin vs LEAGUE.
No strategy change before threshold regardless of small-sample noise.

**4. v6 overrating audit — trigger: ongoing, flag per match**
Ecuador confirmed overrated (CIV 1-0). As more flagged teams resolve, update the diagnostic and blend weight
reasoning. Do NOT refit engine mid-tournament.

**5. #1 hit-rate tracking — trigger: each matchday**
Currently 10/12 = 83%. If sustained through MD2, understand the strategy (chalk? luck?).
Relevant for variance mode calibration if trailing late.
## ═══════════════════════════════════════════════════════════════════════════════════════════

**Last scanned: 2026-06-15.** Update this every model run (see CLAUDE.md → "Model-blind scan").
**XI check 2026-06-15 (pre-KO, all 3 MD2 matches — NO change):** Belgium XI CONFIRMED (Courtois + Doku start, scare cleared; Ngoy/Mechele depth CBs = ignore; Egypt Salah starts = overlay already applied). Saudi-Uruguay + Iran-NZ still PREDICTED (sheets drop ~KO) but no surprise: **Uruguay near-full-strength (Valverde/Bentancur/Ugarte/Núñez/Viñas) — NOT resting starters → pick STRENGTHENED**; Iran expected XI (Taremi leads, Jahanbakhsh out per overlay). No outcome flip on any → Belgium 1-0 / Uruguay 0-1 / Iran 1-0 all HOLD. X2 HELD.
**Scan 2026-06-15 (MD2 slate Belgium/Saudi/Iran):** Belgium–Egypt: Egypt **Salah (hamstring) starting but not fully fit** → mild Egypt ATT −0.07 (halved, market-priced); Belgium Debast (CB) out = squad depth, ignore; Doku breathing scare, returned/fit. Saudi–Uruguay: Uruguay near full-strength; Saudi new coach (Renard sacked April), poor form — intangible, NO overlay. Iran–NZ: Iran missing **Jahanbakhsh (muscle) + Eckert + Torabi** → mild Iran ATT −0.05 (halved); NZ fully fit (Wood back since April). All overlays run WITH the market (no illusory value). PICKS: Belgium 1-0 / Uruguay 0-1 / Iran 1-0 — all EV-max favourites; Iran = free differentiation (field over-picks Draw 44%). X2 HELD.
**Scan 2026-06-14:** CIV Ndicka (starting CB) OUT for opener → mild CIV DEF downgrade, supports Ecuador/over (NOT applied as overlay — would compound the flagged Ecuador outcome-overrating; noted as qualitative de-risk only). Japan on 6-win streak (beat Brazil, England) = post-cutoff form aligned with our contrarian Japan lean. NL Verbruggen fit, Timber out (already in overlay). No score changes.
The deployed model (v6) is fit on historical data and is BLIND to: injuries, suspensions,
lineups, and results after the data cutoff. This file is the manual overlay layer.

## Results log
| Date | Match | Score | vs model | Notes |
|------|-------|-------|----------|-------|
| 2026-06-11 | Mexico 2–0 South Africa | Mexico W | consistent (model 73%) | 3 red cards (1 Mex, 2 RSA) |
| 2026-06-11 | South Korea 2–1 Czechia | Korea W | consistent (model 41%; contrarian value pick hit) | Korea comeback |
| 2026-06-14 | Germany 7–1 Curaçao | Germany W | consistent (blowout; model favoured Germany heavily) | historic scoreline; tier +100 |
| 2026-06-14 | Netherlands 2–2 Japan | Draw | MISS — model picked Japan W; market NL → we picked Japan (LEAGUE) | iconic draw; tier +20 |
| 2026-06-14 | Côte d'Ivoire 1–0 Ecuador | CIV W | MISS — we picked Ecuador W (4-source model flag; Ecuador overrated confirmed) | tier +30 |
| 2026-06-14 | Sweden 5–1 Tunisia | Sweden W | consistent (model+market favoured Sweden) | score missed (1-0 pick); tier **+100** (5-1, model est 0.2% OK) |
| 2026-06-15 | Spain 0–0 Cape Verde | Draw | **MAJOR UPSET** — model 93% Spain, market agreed; pick Spain 3-0 → base 0 | irreducible upset variance, NOT a model error (both sources lock Spain); 0-0 tier **+50** = FIRST DIRECT 0-0 obs |

## Pick performance (points game: base reward + rarity bonus, X2 held)
| Match | Outcome pick | Score submitted | Result | Base pts | Rarity bonus |
|-------|--------------|-----------------|--------|----------|--------------|
| Mexico–S.Africa | Mexico | 2–0 | 2–0 | ✅ 49 | **+20** (>30% crowd — obs #1) |
| S.Korea–Czechia | South Korea | 1–0 (as recommended) | 2–1 | ✅ 96 | — (score missed) |
| Canada–Bosnia | Canada | 3–0 | **1–1** | ❌ 0 | tier(1-1)=+20 obs#3 |
| USA–Paraguay | Draw | 0–0 | **4–1** | ❌ 0 | tier(4-1)=+100 obs#4 (first tail obs!) |
| Qatar–Switzerland | Switzerland | 0–3 | SUBMITTED | | |
| Brazil–Morocco | **Draw** | **0–0** | HORIZON | | EV-max; Morocco was a small-EV-sacrifice diff, wrong for 100-match horizon |
| Haiti–Scotland | **Draw** | **0–0** | REVISED (league) | | was Scotland 1-3 |
| Germany–Curaçao | Germany | **4–0** | AUDIT | | score fixed 5-0→4-0 (de-rarified) |
| Australia–Turkey | Turkey | **0–2** | AUDIT | | score fixed 1-3→0-2 (de-rarified) |
| Netherlands–Japan | **Japan** | **0–2** | REVISED (league) | | was Draw 0-0 |
| Ivory Coast–Ecuador | Ecuador | 0–1 | **1-0 CIV ❌** | 0 | tier(1-0)=+30 obs#11 |
| Germany–Curaçao | Germany | 4–0 | **7-1 GER ✅** | base (ask reward) | tier(7-1)=+100 obs#9; score missed |
| Netherlands–Japan | Japan | 0–2 | **2-2 ❌** | 0 | tier(2-2)=+20 obs#10; outcome missed (draw) |
| Sweden–Tunisia | **Sweden** | **1–0** | **5-1 SWE ✅** | 72 | score missed; tier(5-1)=**+100** obs#13 (model est 0.2% OK) |
| Spain–Cape Verde | Spain | 3–0 | **0-0 DRAW ❌** | 0 | major upset (Spain 93%); tier(0-0)=+50 obs#12 — FIRST DIRECT 0-0, validates tier-50 thesis |

**REVISED 2026-06-13 under LEAGUE objective (picks unlocked):** 4 maximin draws dismantled → differentiated
+EV picks (Morocco/Japan = field-underpicked EV-competitive; Haiti-Draw = EV-max 9%-field; Sweden = EV-max
fav, draw was −3.8EV hedge). Principle: separate via outcome when underpicked side is +EV, else via rare
score. Engine now LEAGUE_MODE (matchday.py, DIFF_BAND=2.0). X2 still HELD (Ecuador E=50.6 flagged but
single-model-source contested — not used yet).

**Running total: 165 pts (145 base + 20 bonus).**
**NB:** realized bonus tiers are observable even for scores we didn't pick (obs #2 = Korea 2–1 earned +20 for whoever had it → >30% crowd). User to report the realized tier of EVERY played match → ~1 calibration obs per match.
**Crowd calibration:** obs #2 VIOLATED the prior (est 26.8% vs realized >30%) → early refit: **beta 1.25→1.6, sal_strength 1.0→1.5** (crowd herds harder on iconic scores than assumed). Post-refit: Mexico OK (35.2%), Korea 29.0% — still 1pt below band edge; coarse-grid residual, expect resolution at obs #3. Strategic effect: iconic scores even MORE crowded → rare-score arbitrage (3-0/3-1 type, 50/70 tiers) STRONGER.
**12 obs / 6 violations (2026-06-15):** model structurally misfit; params beta/sal near-unidentified. Notable new obs: Germany 7-1 → +100 (ultra-rare, model est 0.7% barely violates 0.5% ceiling); NL-Japan 2-2 → +20 (crowd herds hard on 2-2, model est only 17.4% vs >30% — draw iconic scores under-estimated); CIV-Ecuador 1-0 → +30 (model over-estimated 1-0 home win herding, 41.9% vs 20-30% actual). Pattern: draw scores (1-1, 2-2) dramatically under-estimated by model; home-win 1-0 over-estimated. Refit GATED to 15 obs.
**★ FIRST DIRECT 0-0 OBSERVATION (Spain-Cape Verde, obs#12, 2026-06-15):** 0-0 realized +50 (5-20% among Draw-pickers); model est 17.8% → **OK, inside band**. The 0-0 under-picking edge was INFERRED until now (zero direct obs, demoted 2026-06-12); this is its FIRST direct support — confirms 0-0 sits at tier-50 with our p-estimate well-calibrated, vindicating the MD1 0-0-cluster tier-50 assumption. NB single obs (Verify-Std #7): one point, not a validated finding — but it points the right way (unlike the iconic-draw 1-1/2-2 under-estimates). Note 0-0 here ALSO fits the "draws under-picked by crowd" pattern but model p was accurate, so no violation.

**X2 status: HELD** (usable anytime incl. KO — bar raised accordingly). Candidates auto-flagged by `matchday.py`.
**Standing (2026-06-12):** ~230,000th / >1M with 2nd-best-possible score (165) → top is dense; rare-score
bonuses = primary climbing instrument (VAR_TIEBREAK active). 1st ex-aequo (of 4) in friends league.
**Obs#2 provenance confirmed:** organizer email (first-party). Crowd params beta=1.6/sal=1.5 de-flagged.

## MD1 counterfactual selector ledger (pre-committed 2026-06-12 — score all three as results land)
| Match | pure-v6 pick | pure-market pick | SUBMITTED (maximin) | RESULT |
|-------|--------------|------------------|---------------------|--------|
| Canada–Bosnia | Canada | Canada | Canada | → **1-1: all 3 WRONG** (Canada upset draw, no differentiation) |
| USA–Paraguay | Paraguay | USA | Draw | → **4-1: MARKET RIGHT, v6+maximin WRONG** (USA blowout — contested flip, market wins R1) |
| Qatar–Suisse | Switzerland | Switzerland | Switzerland |
| Brazil–Morocco | Morocco | Brazil | Draw |
| Haiti–Scotland | Scotland | Draw | Scotland |
| Germany–Curaçao | Germany | Germany | Germany | → **7-1: all 3 CORRECT on outcome** (Germany blowout) |
| Australia–Turkey | Turkey | Turkey | Turkey | → **2-0 AUS: all 3 WRONG** (Turkey was model+market pick, upset) |
| NL–Japan | Japan | Netherlands | Draw | → **2-2: Draw CORRECT, v6+market WRONG** (maximin wins R2) |
| CIV–Ecuador | Ecuador | Draw | Ecuador | → **1-0 CIV: market(Draw) closest; v6+submitted(Ecuador) WRONG** |
| Sweden–Tunisia | Tunisia | Sweden | Draw | → **5-1: market(Sweden) CORRECT; v6+maximin WRONG** (Sweden blowout) |

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
