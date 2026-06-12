import json

# ---- Parse eloratings code -> elo ----
code_elo = {}
for line in open('World_raw.tsv', encoding='utf-8').read().splitlines():
    f = line.split('\t')
    if len(f) < 4:
        continue
    code = f[2].strip()
    try:
        elo = float(f[3])
    except ValueError:
        continue
    code_elo[code] = elo

# ---- Parse code -> primary name ----
code_name = {}
name_code = {}
for line in open('teams_raw.tsv', encoding='utf-8').read().splitlines():
    f = line.split('\t')
    if len(f) < 2:
        continue
    code = f[0].strip()
    names = [n.strip() for n in f[1:] if n.strip()]
    if not names:
        continue
    code_name[code] = names[0]
    for n in names:
        name_code[n.lower()] = code

# ---- 48 WC teams by group (draw order = seeding pos 1..4) ----
groups = {
 'A': ['Mexico','South Africa','South Korea','Czech Republic'],
 'B': ['Canada','Bosnia and Herzegovina','Qatar','Switzerland'],
 'C': ['Brazil','Morocco','Haiti','Scotland'],
 'D': ['United States','Paraguay','Australia','Turkey'],
 'E': ['Germany','Curacao','Ivory Coast','Ecuador'],
 'F': ['Netherlands','Japan','Sweden','Tunisia'],
 'G': ['Belgium','Egypt','Iran','New Zealand'],
 'H': ['Spain','Cape Verde','Saudi Arabia','Uruguay'],
 'I': ['France','Senegal','Iraq','Norway'],
 'J': ['Argentina','Algeria','Austria','Jordan'],
 'K': ['Portugal','DR Congo','Uzbekistan','Colombia'],
 'L': ['England','Croatia','Ghana','Panama'],
}

# manual name -> eloratings code overrides
override = {
 'United States':'US','Czech Republic':'CZ','South Korea':'KR','South Africa':'ZA',
 'Bosnia and Herzegovina':'BA','Curacao':'CW','Ivory Coast':'CI','DR Congo':'CD',
 'Cape Verde':'CV','Turkey':'TR','Iran':'IR','New Zealand':'NZ','Saudi Arabia':'SA',
 'England':'EN','Scotland':'SQ','Wales':'WA',
}

def code_for(team):
    if team in override:
        return override[team]
    lc = team.lower()
    if lc in name_code:
        return name_code[lc]
    # try fuzzy contains
    for n, c in name_code.items():
        if n == lc:
            return c
    return None

data = {}
missing = []
for g, teams in groups.items():
    data[g] = []
    for t in teams:
        c = code_for(t)
        elo = code_elo.get(c) if c else None
        if elo is None:
            missing.append((t, c))
        data[g].append({'team': t, 'code': c, 'elo': elo})

json.dump(data, open('wc_data.json','w'), indent=2)

# report ascii-safe
rep = []
for g, teams in data.items():
    rep.append(f"Group {g}:")
    for x in teams:
        rep.append(f"  {x['team']:<26} {x['code']}  {x['elo']}")
rep.append("MISSING: " + str(missing))
open('data_report.txt','w').write('\n'.join(rep))
print("missing:", missing)
print("teams matched:", sum(1 for g in data for x in data[g] if x['elo']))
