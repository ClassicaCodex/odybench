"""Design revision 6 scratch: how many members the epoch-matched held-out pools
keep for several band widths around the target's year (-1177).  Membership
only: no predicate is evaluated, and the target is removed first.
Rows and pool definitions as revision 5's heldout_strata.py (imported).
Run: py results/design-revision-v6/band_counts.py
"""
import sys
import json
import importlib.util
sys.path.insert(0, ".")
spec = importlib.util.spec_from_file_location("hs5", "results/design-revision-v5/heldout_strata.py")
hs5 = importlib.util.module_from_spec(spec)
sys.modules["hs5"] = hs5
spec.loader.exec_module(hs5)
from odybench import calendar as cal  # noqa: E402

rows = [r for r in json.load(open(hs5.ROWS, encoding="utf-8")) if r["jdn"] != hs5.T_S]
cl = {r["jdn"]: hs5.classify(r) for r in rows}
bm = [j for j, c in cl.items() if c]
mw = [j for j, c in cl.items() if "mwra" in c]


def year(j):
    return cal.julian_from_jdn(int(j))[0]


for w in (350, 500, 700, 900):
    lo, hi = -1177 - w, -1177 + w
    nb = sum(1 for j in bm if lo <= year(j) <= hi)
    nm = sum(1 for j in mw if lo <= year(j) <= hi)
    print(f"+-{w} years: P_BM {nb}, P_MWRA {nm}; floor if no member passes both: "
          f"{1 / (nb + 1):.3f}, {1 / (nm + 1):.3f}")
