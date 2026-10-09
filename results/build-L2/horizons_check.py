"""Scratch check (agent L2), I15(b)-style, on dates far from the target
(-700..-600): JPL Horizons geocentric apparent ecliptic-of-date longitudes and
latitudes (QUANTITIES 31, TT) of Venus and Mars (barycentre 4: Horizons serves 499 only from AD 1600) at 03:30 UT, and of Mercury and
the Sun hourly around a conjunction, against odybench.lean.heldout's
separations and conjunction instants.  UT -> TT with SMH2020 Delta-T on both
sides.  Fetched files go to results/build-L2/horizons/ with the request URL on
line 1.

Run: cd C:/Projects/odybench && py results/build-L2/horizons_check.py
"""
import math
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from odybench import ephem as E  # noqa: E402
from odybench import calendar as cal  # noqa: E402
from odybench.lean import heldout as H  # noqa: E402

OUT = ROOT / "results" / "build-L2" / "horizons"
API = "https://ssd.jpl.nasa.gov/api/horizons.api"
H4_DATES = [(1471341, -10), (1472021, -6), (1474619, -9)]       # Day 0 JDN, day of least separation
H3_DATES = [1467295, 1468447, 1471696]                         # Day 0 JDN with a conjunction near Day 0


def tt_of_ut(jd_ut):
    return jd_ut + float(E.delta_t(E.julian_epoch(jd_ut), "smh2020")) / 86400.0


def fetch(body, jd_tt_list, name):
    path = OUT / f"{name}.txt"
    tl = " ".join(f"'{x:.8f}'" for x in jd_tt_list)
    params = dict(format="text", COMMAND=f"'{body}'", OBJ_DATA="'NO'", MAKE_EPHEM="'YES'", EPHEM_TYPE="'OBSERVER'",
                  CENTER="'500@399'", TLIST=tl, TIME_TYPE="'TT'", QUANTITIES="'31'", ANG_FORMAT="'DEG'",
                  EXTRA_PREC="'YES'", CSV_FORMAT="'YES'")
    url = API + "?" + urllib.parse.urlencode(params)
    if not path.exists():
        with urllib.request.urlopen(url, timeout=60) as r:
            txt = r.read().decode("utf-8")
        OUT.mkdir(parents=True, exist_ok=True)
        path.write_text(url + "\n" + txt, encoding="utf-8")
    txt = path.read_text(encoding="utf-8")
    body_txt = txt[txt.index("$$SOE") + 5: txt.index("$$EOE")]
    rows = []
    for line in body_txt.strip().splitlines():
        f = [x.strip() for x in line.split(",")]
        nums = [x for x in f if x and x.replace(".", "", 1).replace("-", "", 1).isdigit()]
        lon, lat = float(nums[-2]), float(nums[-1])
        rows.append((lon, lat))
    return rows


def sep(l1, b1, l2, b2):
    l1, b1, l2, b2 = map(math.radians, (l1, b1, l2, b2))
    c = math.sin(b1) * math.sin(b2) + math.cos(b1) * math.cos(b2) * math.cos(l1 - l2)
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))


def main():
    worst_sep = 0.0
    for j, k in H4_DATES:
        jd_ut = j + k - 0.5 + 3.5 / 24.0
        tt = tt_of_ut(jd_ut)
        v = fetch("299", [tt], f"venus_{j}_{k}")[0]
        m = fetch("4", [tt], f"mars_{j}_{k}")[0]
        hz = sep(v[0], v[1], m[0], m[1])
        mine = float(H._separation("venus", "mars", np.array([jd_ut]))[0])
        worst_sep = max(worst_sep, abs(hz - mine))
        print(f"Day0 {cal.julian_from_jdn(j)} Day {k}: Venus-Mars separation Horizons {hz:.6f} deg, "
              f"heldout {mine:.6f} deg, diff {abs(hz - mine) * 3600:.3f} arcsec")
    worst_conj = 0.0
    for j in H3_DATES:
        r = H.evaluate(np.array([j]), "both", predicates=("H3",))
        noon_tt = tt_of_ut(j - 2.0 / 24.0)
        c_mine = noon_tt + float(r["H3_conj_offset_d"][0])
        grid = [c_mine + h / 24.0 for h in range(-6, 7)]
        me = fetch("199", grid, f"mercury_{j}")
        su = fetch("10", grid, f"sun_{j}")
        d = [((a[0] - b[0] + 180) % 360) - 180 for a, b in zip(me, su)]
        root = None
        for i in range(len(grid) - 1):
            if d[i] * d[i + 1] <= 0:
                root = grid[i] + (grid[i + 1] - grid[i]) * d[i] / (d[i] - d[i + 1])
        worst_conj = max(worst_conj, abs(root - c_mine))
        print(f"Day0 {cal.julian_from_jdn(j)}: Mercury-Sun conjunction Horizons JD(TT) {root:.6f}, heldout "
              f"{c_mine:.6f}, diff {abs(root - c_mine) * 86400:.1f} s")
    print(f"worst: separation {worst_sep * 3600:.3f} arcsec (I15(b) 0.001 deg = 3.6 arcsec); conjunction "
          f"{worst_conj * 86400:.1f} s (I15(b) 0.01 d = 864 s)")
    ok = worst_sep < 0.001 and worst_conj < 0.01
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
