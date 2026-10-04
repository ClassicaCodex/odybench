"""Check the calendar tests can fail (scratch): each mutation must make at least one test fail."""
import importlib, re, sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tests"))
import test_calendar as T
from odybench import calendar as C
orig = {n: getattr(C, n) for n in ("jdn_from_julian", "julian_from_jdn", "is_leap_julian", "julian_from_jd", "jd_from_julian")}
def run():
    fails = []
    for n, f in vars(T).items():
        if n.startswith("test_") and callable(f):
            try: f()
            except Exception: fails.append(n)
    return fails
muts = {
 "one day shift in -500 Mar": ("jdn_from_julian", lambda y, m, d: orig["jdn_from_julian"](y, m, d) + ((np.asarray(y) == -500) & (np.asarray(m) == 3)) * 1),
 "leap rule y%4==1": ("is_leap_julian", lambda y: (C._int(y) % 4) == 1),
 "inverse off by one day for BC": ("julian_from_jdn", lambda j: orig["julian_from_jdn"](C._int(j) + (C._int(j) < 1721424) * 1)),
 "instant truncated not rounded": ("julian_from_jd", lambda jd, off=0.0: orig["julian_from_jd"](np.asarray(jd) - 1e-4, off)),
 "Gregorian used instead of Julian": ("jdn_from_julian", lambda y, m, d: C.jdn_from_gregorian(y, m, d)),
}
for label, (name, fn) in muts.items():
    setattr(C, name, fn); T.C = C
    print(f"{label:35s} -> failing tests: {run()}")
    setattr(C, name, orig[name])
print("unmutated ->", run())
pat = re.compile(r"^\s*(import\s+datetime|from\s+datetime\s+import)|datetime64|astype\(\s*['\"]M8|np\.datetime_as_string", re.M)
for s in ["import datetime", "from datetime import date", "x = np.datetime64('2000')", "a.astype('M8[D]')", "# no date-time here"]:
    print(repr(s), bool(pat.search(s)))
