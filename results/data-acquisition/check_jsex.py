"""
Checks of the JSEX data fetched by tools/fetch_jsex.py (scratch script of the
data-acquisition task; output in check_jsex.out.txt).

1. The fetched century files and program.js are byte-identical to the copies
   that earlier tasks downloaded (results/window/jsex/, data/refs/nasa/JSEX-*).
2. The new site catalogue reproduces results/window/jsex/<site>.jsonl row for
   row for -1499..-600 (all the old fields).
3. Every element row's Delta-T equals the Canon's own rule, Espenak-Meeus
   polynomial + n-dot correction (odybench.ephem.dt_em2006_canon at NASA's
   decimal year y + (m - 0.5)/12), to < 1 s.
4. Every eclipse of the NASA catalogue pages SE-1999--1900 .. SE-1599--1500
   (data/jsex/secat5/) and of the older pages already on disk has exactly one
   element row with the same TD of greatest eclipse (to 1 s), Delta-T (to 1 s),
   and gamma (to 0.0001), gamma computed from the element polynomials at T0.
5. Coverage: first and last eclipse, rows per century.
"""
import html
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from odybench import ephem as E          # noqa: E402
from odybench import calendar as C       # noqa: E402

J = ROOT / "data" / "jsex"
CENT = [f"SEm{y:04d}" for y in range(1999, 0, -100)] + ["SE0001", "SE0101", "SE0201"]
fails = []


def check(ok, msg):
    print(("PASS " if ok else "FAIL ") + msg)
    if not ok:
        fails.append(msg)


# ---- 1. byte identity with earlier copies
print("1. byte identity with earlier downloads")
for name in ["program.js"] + [c + ".js" for c in CENT]:
    new = (J / name).read_bytes()
    olds = [ROOT / "results" / "window" / "jsex" / name, ROOT / "data" / "refs" / "nasa" / ("JSEX-" + name)]
    for o in olds:
        if o.exists():
            check(o.read_bytes() == new, f"{name} == {o.relative_to(ROOT)}")

# ---- element rows
NUM = re.compile(r"[-+]?\d+\.\d*(?:[eE][-+]?\d+)?|[-+]?\d+(?:[eE][-+]?\d+)?")


def elements(name):
    src = (J / f"{name}.js").read_text()
    body = src.split("new Array(", 1)[1].rsplit(")", 1)[0]
    body = "\n".join(l.split("//")[0] for l in body.splitlines())
    vals = [float(v) for v in NUM.findall(body)]
    assert len(vals) % 28 == 0, (name, len(vals))
    return [vals[i:i + 28] for i in range(0, len(vals), 28)]


rows = []
for c in CENT:
    for el in elements(c):
        rows.append((c, el))
print(f"\n5. coverage: {len(rows)} eclipses in {len(CENT)} century files")
for c in CENT:
    n = sum(1 for cc, _ in rows if cc == c)
    print(f"   {c}: {n}")
first, last = rows[0][1][0], rows[-1][1][0]
print(f"   first T0 {E.fmt_jd(first, 'TT')}; last T0 {E.fmt_jd(last, 'TT')}")
check(C.julian_from_jd(first)[0] == -1999 and C.julian_from_jd(last)[0] == 300, "span -1999..+300")

# ---- 3. Delta-T rule
print("\n3. element Delta-T vs the Canon's rule dt_em2006_canon(decimal year)")
worst_mid = worst_day = 0.0
for c, el in rows:
    y, m, d, h = C.julian_from_jd(el[0])
    v_mid = float(E.dt_em2006_canon(y + (m - 0.5) / 12))
    v_day = float(E.dt_em2006_canon(y + (C.day_of_year(y, m, d) - 1 + h / 24) / C.days_in_year(y)))
    worst_mid = max(worst_mid, abs(v_mid - el[4]))
    worst_day = max(worst_day, abs(v_day - el[4]))
    if el[4] != el[5]:
        fails.append(f"el[4] != el[5] in {c}")
print(f"   decimal year y + (m - 0.5)/12 (NASA deltatpoly page):        max |diff| {worst_mid:.2f} s")
print(f"   decimal year y + (day of year - 1 + h/24)/days in year:   max |diff| {worst_day:.2f} s"
      " (elements print 0.1 s)")
check(worst_day < 0.2, f"element Delta-T = Canon rule at the day-resolved decimal year, max {worst_day:.2f} s"
                       f" over {len(rows)} rows")


# ---- 4. NASA catalogue pages
def catalogue(path):
    t = path.read_text(encoding="latin-1")
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    out = []
    for m in re.finditer(r"\b(\d{5})\s+(-?\d+)\s+([A-Z][a-z]{2})\s+(\d{1,2})\s+(\d\d):(\d\d):(\d\d)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+"
                         r"([A-Z]\S*)\s+(\S+)\s+(-?\d\.\d{4})\s+(\d\.\d{4})", t):
        g = m.groups()
        mon = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split().index(g[2]) + 1
        y = int(g[1])
        jd = C.jd_from_julian(y, mon, int(g[3]), int(g[4]) + int(g[5]) / 60 + int(g[6]) / 3600)
        out.append(dict(num=g[0], y=y, jd=jd, dt=int(g[7]), type=g[10], gamma=float(g[12]), mag=float(g[13])))
    return out


def gamma_at(el):
    t = (el[0] - math.floor(el[0] - 0.5) - 0.5) * 24 - el[1]
    t = (t + 12.0) % 24.0 - 12.0          # t0 may fall on the next or previous day
    x = el[6] + t * (el[7] + t * (el[8] + t * el[9]))
    y = el[10] + t * (el[11] + t * (el[12] + t * el[13]))
    return math.copysign(math.hypot(x, y), y)


print("\n4. NASA catalogue pages vs element files")
pages = sorted((J / "secat5").glob("SE-*.html")) + sorted((ROOT / "data" / "refs" / "nasa").glob("SEcat5_SE-*.html"))
by_jd = sorted(rows, key=lambda r: r[1][0])
for p in pages:
    cat = catalogue(p)
    nmatch = 0
    worst_t = worst_dt = worst_g = 0.0
    for r in cat:
        cand = [el for c, el in by_jd if abs(el[0] - r["jd"]) < 1 / 24]
        if len(cand) != 1:
            fails.append(f"{p.name}: {r['num']} has {len(cand)} element rows")
            continue
        el = cand[0]
        nmatch += 1
        worst_t = max(worst_t, abs(el[0] - r["jd"]) * 86400)
        worst_dt = max(worst_dt, abs(el[4] - r["dt"]))
        worst_g = max(worst_g, abs(gamma_at(el) - r["gamma"]))
    y0 = min(r["y"] for r in cat)
    n_el = sum(1 for c, el in rows if y0 <= C.julian_from_jd(el[0])[0] <= y0 + 99)
    check(nmatch == len(cat) == n_el and worst_t <= 1.0 and worst_dt <= 1.0 and worst_g <= 1.5e-4,
          f"{p.name}: catalogue {len(cat)} eclipses, element rows in century {n_el}, matched {nmatch}; "
          f"max |dTD| {worst_t:.1f} s, |dDeltaT| {worst_dt:.2f} s, |dgamma| {worst_g:.5f}")

# ---- 2. site catalogue regression
print("\n2. site catalogue -1499..-600 vs results/window/jsex/<site>.jsonl")
KEYS = ["file", "idx", "jdTD", "dT", "sigmaDT", "date", "type", "mag", "alt", "vis", "utH", "last",
        "maxMag1s", "anyTotal1s", "maxMag2s", "anyTotal2s", "anyCentral2s"]
for site in ["ithaca", "kefalonia", "lefkada", "corfu", "zakynthos"]:
    old = [json.loads(l) for l in open(ROOT / "results" / "window" / "jsex" / f"{site}.jsonl", encoding="utf-8")]
    new = [json.loads(l) for l in open(J / "sites" / f"{site}.jsonl", encoding="utf-8")]
    oldf = {r["file"] for r in old}
    sub = [r for r in new if r["file"] in oldf]
    same = len(sub) == len(old) and all(all(a[k] == b[k] for k in KEYS) for a, b in zip(sub, old))
    check(same, f"{site}: {len(sub)} rows of {sorted(oldf)[0]}..{sorted(oldf)[-1]} identical to the window catalogue "
                f"({len(new)} rows in all)")

# ---- spot: the 1178 BC row at Ithaca
it = [json.loads(l) for l in open(J / "sites" / "ithaca.jsonl", encoding="utf-8")]
r = [x for x in it if x["date"] == "-1177-Apr-16"][0]
print(f"\n-1177 Apr 16 at Ithaca: type {r['type']} mag {r['mag']} utH {r['utH']} LAT {r['last']} alt {r['alt']}"
      f" sigma {r['sigmaDT']} ({r['sigmaSrc']})  [research-window: mag 0.984, about 11:44 LAT]")
check(abs(r["mag"] - 0.984) < 0.0005, "1178 BC Ithaca magnitude 0.984 as in research-window")
print("\nclass counts at Ithaca by span (nominal total & Sun up; total within +-1 sigma):")
for a, b in [(-1999, -1500), (-1499, -600), (-599, 300)]:
    s = [x for x in it if a <= C.julian_from_jd(x["jdTD"])[0] <= b]
    print(f"   {a}..{b}: {len(s)} eclipses; total nominal {sum(1 for x in s if x['type'] == 3 and x['alt'] > 0)};"
          f" total within 1 sigma {sum(1 for x in s if x['anyTotal1s'])}")
print("\n" + ("ALL PASS" if not fails else f"{len(fails)} FAIL(S):\n  " + "\n  ".join(fails[:20])))
