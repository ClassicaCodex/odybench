"""Design revision 7 scratch (revision 6 script, updated paths and patterns): leak scan of the public part of DESIGN.md (the text
above the Appendix T marker) and of the revision-6 scripts on the public
whitelist (alm_rows.py, pcr_rows.py, verdict_trace.py).

It reads the two truth files ONLY to build the list of accepted dates, as the
recheck's results/critique-design-r1/v5/scan_public_leaks.py does, and then:
  1. searches for every accepted date in its usual printed forms, with every
     minus sign and dash normalised first (U+2212, U+2013, hyphen-minus);
  2. lists year-only mentions of a control's year, for a human to judge
     (the allowlist below holds the known non-truth uses);
  3. runs revision 5's per-set truth-side patterns (scan_truthside.py).
Run: py results/design-revision-v7/scan_public.py
"""
import io
import json
import os
import re
import sys

sys.path.insert(0, "C:/Projects/odybench")
from odybench import calendar as cal  # noqa: E402

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
R = "C:/Projects/odybench/"
MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
MONFULL = ["January", "February", "March", "April", "May", "June", "July", "August",
           "September", "October", "November", "December"]


def norm(t):
    return t.replace("\u2212", "-").replace("\u2013", "-")


dates = []
real = json.load(open(R + "data/prereg/controls_real_truth.json", encoding="utf-8"))
pat_acc = re.compile(r"(\d{1,2})(?:/\d{1,2})? (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) "
                     r"(?:(\d{1,4}) BC|AD (\d{1,4}))")
for s in real["sets"]:
    for e in s.get("events", []):
        if not isinstance(e, dict) or not e.get("accepted"):
            continue
        m = pat_acc.search(e["accepted"])
        if not m:
            continue
        d = int(m.group(1)); mo = MON.index(m.group(2)) + 1
        y = 1 - int(m.group(3)) if m.group(3) else int(m.group(4))
        dates.append((y, mo, d, f"{s['set_id']}:{e['event_id']}"))
alm = json.load(open(R + "data/prereg/controls_almagest_truth.json", encoding="utf-8"))
for s in alm["sets"]:
    for r in s.get("records", []):
        cd = r.get("civil_date_julian")
        if not cd:
            continue
        m = re.match(r"([+-]\d{4})-(\d{2})-(\d{2})", cd)
        dates.append((int(m.group(1)), int(m.group(2)), int(m.group(3)), f"{s['set']}:{r['record']}"))
print(len(dates), "accepted dates")


def forms(y, mo, d):
    out = set()
    mon, monf = MON[mo - 1], MONFULL[mo - 1]
    ys = ("-" if y < 0 else "+") + f"{abs(y):04d}"
    out.add(f"{ys}-{mo:02d}-{d:02d}")
    if y < 0:
        out |= {f"-{abs(y)} {mon} {d}", f"-{abs(y)}-{mo:02d}-{d:02d}", f"-{abs(y):04d} {mon} {d}"}
    if y <= 0:
        bc = 1 - y
        for mn in (mon, monf):
            out |= {f"{d} {mn} {bc} BC", f"{mn} {d}, {bc} BC", f"{mn} {d} {bc} BC",
                    f"{bc} BC {mn} {d}", f"{bc} BC, {mn} {d}"}
    else:
        for mn in (mon, monf):
            out |= {f"{d} {mn} AD {y}", f"{mn} {d}, AD {y}", f"AD {y} {mn} {d}", f"{y} {mn} {d}",
                    f"+{y} {mn} {d}"}
    jdn = cal.jdn_from_julian(y, mo, d)
    out |= {str(jdn), str(jdn - 1), f"{jdn - 0.5:.1f}"}
    return out


texts = {}
design = open(R + "DESIGN.md", encoding="utf-8").read()
texts["DESIGN.md (public part)"] = norm(design[:design.index("<!-- APPENDIX-T")])
for f in ("results/design-revision-v6/alm_rows.py", "results/design-revision-v7/pcr_rows.py",
          "results/design-revision-v7/verdict_trace.py"):
    texts[f] = norm(open(R + f, encoding="utf-8").read())

hits = 0
for (y, mo, d, lab) in dates:
    for form in sorted(forms(y, mo, d)):
        for f, t in texts.items():
            for m in re.finditer(re.escape(form), t):
                a, b = m.start(), m.end()
                if (a > 0 and t[a - 1].isdigit()) or (b < len(t) and t[b].isdigit()):
                    continue
                ln = t.count("\n", 0, a) + 1
                print(f"HIT {lab} [{form}] {f}:{ln}: ...{t[max(0, a - 70):b + 50]!r}...")
                hits += 1
print("total date hits", hits)

ALLOW = {
    (-720, "SMH2020's spline epoch, or the HMNAO lod integral before it; not a control"),
}
allow_years = {y for y, _ in ALLOW}
print("\n--- year-only mentions of control years (allowlist:", sorted(ALLOW), ") ---")
years = sorted(set(y for (y, _, _, _) in dates))
n_year = 0
for f, t in texts.items():
    for y in years:
        pats = [f"{1 - y} BC"] if y <= 0 else [f"AD {y}"]
        pats += [f"-{abs(y)}"] if y < 0 else [f"+{y}"]
        for p in pats:
            for m in re.finditer(re.escape(p), t):
                a, b = m.start(), m.end()
                if (a > 0 and (t[a - 1].isdigit() or t[a - 1] in ".,")) or (b < len(t) and t[b].isdigit()):
                    continue
                tag = "allowlisted" if y in allow_years else "REVIEW"
                ln = t.count("\n", 0, a) + 1
                print(f"YEAR {y} [{p}] {tag} {f}:{ln}: ...{t[max(0, a - 60):b + 40]!r}...")
                n_year += 1
print("year-only mentions:", n_year)

print("\n--- revision 5's per-set truth-side patterns (scan_truthside.py) ---")
pats = [r"355\.3", r"6\.63", r"424 ?BC", r"431 ?BC", r"413 ?BC", r"394 ?BC", r"-309\b", r"-187\b",
        r"168 ?BC", r"310 ?BC", r"331 ?BC", r"188 ?BC", r"21 Jun", r"Gautschy", r"IX\.7\.5\b", r"5\.5 d",
        r"20\.6", r"AD 1[2-4]\d", r"2[4-7]\d BC", r"-2[2-7]\d\b", r"\+1[2-4]\d\b", r"-72[01]\b", r"721 BC",
        r"-856", r"\+27[27]", r"-407", r"0\.64 h", r"E2 about", r"ALM-G fails", r"ALM-H fails",
        r"15 Aug", r"Aug 15", r"26 Jun", r"0412", r"3 Aug", r"21 Mar 424", r"Pydna[^|]{0,60}solstice",
        r"1\.79", r"1\.32", r"0\.699", r"held_ALM ≤ 7", r"6 of (these )?7", r"-430", r"ALM-B.s truth", r"B.5", r"0.001°", r"ALM-[ABDEFL], B, D, E, F and L", r"keeps? (its|their) truth[^|]{0,40}ALM-B"]
main = texts["DESIGN.md (public part)"]
for i, l in enumerate(main.split("\n"), 1):
    for p in pats:
        if re.search(p, l):
            print(f"l.{i} [{p}] {l.strip()[:170]}")
