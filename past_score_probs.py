"""Table of v6 predicted score-probability distributions for all past matches.
Pure deployed engine (no overlays), score order = as played (home first)."""
import json, numpy as np
from predict_v6 import smatrix, msum, MAXG

# (home, away, actual_home, actual_away) ; None,None = result pending
MATCHES = [
    ("MD1", "Mexico", "South Africa", 2, 0),
    ("MD1", "South Korea", "Czech Republic", 2, 1),
    ("MD1", "Canada", "Bosnia and Herzegovina", 1, 1),
    ("MD1", "United States", "Paraguay", 4, 1),
    ("MD1", "Qatar", "Switzerland", 1, 1),
    ("MD1", "Brazil", "Morocco", 1, 1),
    ("MD1", "Haiti", "Scotland", 0, 1),
    ("MD1", "Germany", "Curacao", 7, 1),
    ("MD1", "Australia", "Turkey", 2, 0),
    ("MD1", "Netherlands", "Japan", 2, 2),
    ("MD1", "Ivory Coast", "Ecuador", 1, 0),
    ("MD1", "Sweden", "Tunisia", 5, 1),
    ("MD2", "Spain", "Cape Verde", 0, 0),
    ("MD2", "Belgium", "Egypt", 1, 1),
    ("MD2", "Saudi Arabia", "Uruguay", 1, 1),
    ("MD2", "Iran", "New Zealand", 2, 2),
    ("MD3", "France", "Senegal", None, None),
    ("MD3", "Iraq", "Norway", None, None),
    ("MD3", "Argentina", "Algeria", None, None),
    ("MD3", "Austria", "Jordan", None, None),
    ("MD3", "Portugal", "DR Congo", None, None),
]

def topscores(M, k=6):
    f = sorted(((M[a, b], a, b) for a in range(MAXG + 1) for b in range(MAXG + 1)), reverse=True)
    return f[:k]

L = ["# v6 Predicted Score-Probability Distributions - All Past Matches", ""]
L.append("Pure deployed engine (gamma=1.5, no injury overlays). Scores listed home-away as played.")
L.append("Prob(actual) = model probability the engine assigned to the score that actually occurred.")
L.append("")
print("=" * 78)
for md, h, a, ah, aa in MATCHES:
    M, lh, la = smatrix(h, a)
    m = msum(h, a)
    tops = topscores(M, 6)
    actual = f"{ah}-{aa}" if ah is not None else "pending"
    p_actual = (M[ah, aa] * 100) if ah is not None else None
    # console (ASCII)
    hdr = f"{md}  {h} vs {a}   [lam {lh:.2f}-{la:.2f}]  1X2 {m['ph']*100:.0f}/{m['pd']*100:.0f}/{m['pa']*100:.0f}"
    print(hdr)
    tline = "   ".join(f"{x[1]}-{x[2]} {x[0]*100:4.1f}%" for x in tops)
    print("   top: " + tline)
    if p_actual is not None:
        print(f"   ACTUAL {actual}: model p = {p_actual:.2f}%   modal = {tops[0][1]}-{tops[0][2]} ({tops[0][0]*100:.1f}%)")
    else:
        print(f"   modal = {tops[0][1]}-{tops[0][2]} ({tops[0][0]*100:.1f}%)")
    print("-" * 78)
    # markdown
    L.append(f"## {md} - {h} vs {a}")
    L.append(f"lambda {lh:.2f}-{la:.2f} | 1X2 (home/draw/away): {m['ph']*100:.0f}% / {m['pd']*100:.0f}% / {m['pa']*100:.0f}%")
    L.append("")
    L.append("| Rank | Score | Prob |")
    L.append("|------|-------|------|")
    for i, x in enumerate(tops, 1):
        star = " (ACTUAL)" if (ah is not None and x[1] == ah and x[2] == aa) else ""
        L.append(f"| {i} | {x[1]}-{x[2]}{star} | {x[0]*100:.2f}% |")
    if ah is not None:
        L.append("")
        rank_actual = next((i for i, x in enumerate(topscores(M, (MAXG+1)**2), 1)
                            if x[1] == ah and x[2] == aa), None)
        L.append(f"**Actual {actual}: model p = {p_actual:.2f}% (rank {rank_actual} of all scores)**")
    L.append("")

open("PAST_SCORE_PROBS.md", "w", encoding="utf-8").write("\n".join(L))
print("wrote PAST_SCORE_PROBS.md")
