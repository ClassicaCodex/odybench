"""Consistency checks on DESIGN.md (revision 3): escape sequences, dangling
section references, prediction and expectation references, instrument check
references, table cell counts, issue coverage in section 14.
Scratch script for the design revision task; reads DESIGN.md and the two
critiques only."""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
s = open("DESIGN.md", encoding="utf-8").read()
bs = chr(92)
print("literal backslash-u sequences:", re.findall(re.escape(bs) + "u[0-9a-fA-F]{4}", s)[:5])
secs = set(re.findall(r"^#+ (\d+(?:\.\d+)*)", s, re.M))
refs = set(re.findall(r"(?:section |sections |\(|, |; |in |see )(\d+\.\d+(?:\.\d+)?)\b", s))
refs = {r for r in refs if not re.match(r"^\d+\.\d{2,}$", r)}
missing = sorted(r for r in refs if r not in secs)
print("section refs not matching a heading:", missing)
pref = set(re.findall(r"\bP(\d+)\b", s))
pdef = set(re.findall(r"\*\*P(\d+)\.\*\*", s))
print("P defined:", len(pdef), sorted(map(int, pdef))[-1] if pdef else None,
      "referenced but undefined:", sorted(pref - pdef, key=int))
rref = set(re.findall(r"\bR(\d+)\b", s))
rdef = set(re.findall(r"^\| R(\d+) \|", s, re.M))
print("R defined:", sorted(rdef, key=int), "referenced but undefined:", sorted(rref - rdef, key=int))
iref = set(re.findall(r"\bI(\d+)", s))
idef = set(re.findall(r"^\| I(\d+)b? \|", s, re.M))
print("I defined:", sorted(idef, key=int), "referenced but undefined:", sorted(iref - idef, key=int))
sref = set(re.findall(r"\bS(\d+)\b", s))
sdef = set(re.findall(r"^\| \*{0,2}S(\d+)", s, re.M))
print("S sets defined:", sorted(sdef, key=int))
# issue coverage
t14 = s[s.index("## 14."):]
old = [int(x) for x in re.findall(r"^\| (\d+) \| (?:blocker|major|minor)", t14, re.M)]
new = re.findall(r"^\| (N\d+) \|", t14, re.M)
print("14.1 rows:", len(old), sorted(set(range(1, 26)) - set(old)))
print("14.2 rows:", len(new), sorted(set(f"N{i}" for i in range(1, 18)) - set(new), key=lambda x: int(x[1:])))
# tables
lines = s.split("\n")
def cells(line):
    t = line.strip()
    t = re.sub(r"\\|", "", t)
    t = re.sub(r"`[^`]*`", "", t)
    return t.count("|") - 1
in_code = False; header = None; bad = 0
for i, line in enumerate(lines, 1):
    if line.strip().startswith("```"):
        in_code = not in_code; continue
    if in_code: continue
    if line.strip().startswith("|"):
        n = cells(line)
        if header is None: header = n
        elif n != header:
            bad += 1; print(f"  table line {i}: {n} cells, header {header}: {line[:80]}")
    else:
        header = None
print("table rows with a cell-count mismatch:", bad)
print("old names still present:", [w for w in ("rec_PCS", "LR_real", "LR_fav", "LR_sf", "W_BM") if w in s])
