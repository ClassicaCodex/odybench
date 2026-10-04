"""Round-2 review: how G_BM over T_A scales with the slot definitions that
define T_A (DESIGN rev 3, 4.2). Reuses the rows of check_gbm.py (full
background, core -1748..-51). Because no target outside the slots is ever
reached by G_BM* (the identity of 4.2, checked in check_gbm.py: 0
violations), every alternative pool that still contains all of G_BM*'s
survivors gives G_alt = G_base * n_base / n_alt exactly.
Run: py results/critique-design-r2/check_slot_scaling.py
"""
import json
import numpy as np

rows = json.load(open("results/critique-design-r2/check_gbm_full.rows.json", encoding="utf-8"))
f = lambda k: np.array([r[k] for r in rows])
yy, day, cs, cp, jdn = f("y"), f("day"), f("cs"), f("cp"), f("jdn")
is_s = jdn == 1291264          # 16 Apr -1177 (JDN of the UT+2 date; JD 1291263.5 at 0 h)
core = (yy >= -1748) & (yy <= -51) & ~is_s
G_BASE, N_BASE = 0.1400, None


def pool(venus, merc):
    m = np.zeros(len(rows), bool)
    for c, vd, md in ((cs, -5, -34), (cp, -4, -33)):
        m |= c & venus(vd) & merc(md)
    return day & core & m


def ev(md, k):
    return (f(f"d_mwra{md}") <= k) | (f(f"d_gwe{md}") <= k) | (f(f"d_station{md}") <= k)


variants = {
    "design: Venus AV 7; Mercury event <= 6 d or visible": (lambda vd: f(f"vslot{vd}"), lambda md: ev(md, 6) | f(f"mvis{md}")),
    "Mercury event <= 6 d only (no 'or visible')": (lambda vd: f(f"vslot{vd}"), lambda md: ev(md, 6)),
    "Mercury event <= 4 d only": (lambda vd: f(f"vslot{vd}"), lambda md: ev(md, 4)),
    "Mercury event <= 6 d and visible": (lambda vd: f(f"vslot{vd}"), lambda md: ev(md, 6) & f(f"mvis{md}")),
    "Venus lead >= 60 min; Mercury as design": (lambda vd: f(f"lead{vd}") >= 60, lambda md: ev(md, 6) | f(f"mvis{md}")),
    "Venus lead >= 60 min; Mercury event <= 4 d": (lambda vd: f(f"lead{vd}") >= 60, lambda md: ev(md, 4)),
}
base = None
for lab, (v, m) in variants.items():
    n = int(pool(v, m).sum())
    if base is None:
        base = n
    g = G_BASE * base / n
    print(f"{lab:52s} n_A {n:4d}  G_BM {g:.3f}  (x{base / n:.2f})")

# Gamma intervals (DESIGN 5.3) for the same reached targets under each pool
# size: the 26 reach values printed by check_gbm.py (full run).
from scipy.stats import chi2
R = [0.096, 0.154, 0.257, 0.257, 0.257, 0.257, 0.258, 0.367, 0.434, 0.588, 0.765, 0.823, 0.823] + [1.0] * 13


def gamma_ci(r, n):
    r = np.asarray(r)
    y, v, w = r.sum() / n, ((r / n) ** 2).sum(), 1.0 / n
    hi = (v + w * w) / (2 * (y + w)) * chi2.ppf(0.975, 2 * (y + w) ** 2 / (v + w * w))
    lo = v / (2 * y) * chi2.ppf(0.025, 2 * y * y / v)
    return y, lo, hi


print()
for n in (131, 101, 87, 82, 66, 56):
    y, lo, hi = gamma_ci(R, n)
    print(f"n_A {n:4d}: G_BM {y:.3f}  [{lo:.3f}, {hi:.3f}]   label 2 (lo >= 0.20): {lo >= 0.20}")
