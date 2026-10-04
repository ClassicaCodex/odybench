"""Design revision 5 scratch: is the held-out null pool P_BM homogeneous in the
held-out pass rates across the Mercury event that admits each member?

Null side only.  The target, 16 Apr -1177 (Day 0, UT+2 civil date), is removed
from the rows BEFORE anything is computed, and `held()` asserts that it is never
evaluated.  No target-side value is computed or printed.

Why: the target passes only the MWRA readings of G_BM* (r2's estimate).  H3
(Mercury near conjunction with the Sun on Day 0/+1) may depend on which Mercury
event stood near Day -34 (MWRA, GWE or morning station), so the rank test's
exchangeability may need the pool matched on the event class.

Input: r2's rough candidate rows (results/critique-design-r2/check_gbm_full.rows.json,
every C_rel spring conjunction of -1999..+200 at Ithaki), read-only.
Predicates H3 and H4 exactly as results/design-revision-r3/heldout_attain.py
(rough: daily sampling, elongation < 10 deg as the invisibility proxy).

Pools:
  P_BM    : passes some reading of G_BM* (C on a count; Venus lead >= 90 min on
            that count's Venus day; a morning Mercury event within 3.5 d on that
            count's Mercury day)
  P_MWRA  : passes some MWRA reading of G_BM* (event = MWRA)
  P_GS    : passes some GWE or station reading, and no MWRA reading
Run: cd C:/Projects/odybench && py results/design-revision-v5/heldout_strata.py
"""
import sys
import json
import numpy as np
from multiprocessing import Pool

sys.path.insert(0, ".")
from odybench import ephem, calendar as cal  # noqa: E402

ROWS = "results/critique-design-r2/check_gbm_full.rows.json"
T_S = cal.jdn_from_julian(-1177, 4, 16)


def lon_of(body, jd_ut):
    t = ephem.time_ut(np.atleast_1d(jd_ut))
    a = ephem.apparent(body, t)
    lat, lon, _ = a.ecliptic_latlon(epoch="date")
    return np.asarray(lon.degrees)


def held(jdn):
    assert jdn != T_S, "target must never be evaluated"
    days = np.arange(-4, 6)
    jd = jdn - 0.5 + 10.0 / 24.0 + days
    lm = lon_of("mercury", jd)
    ls = lon_of("sun", jd)
    d = (lm - ls + 180.0) % 360.0 - 180.0
    tc = []
    for i in range(len(days) - 1):
        if np.sign(d[i]) != np.sign(d[i + 1]) and abs(d[i] - d[i + 1]) < 30:
            f = d[i] / (d[i] - d[i + 1])
            tc.append(days[i] + f)
    conj = any(-3.0 <= x <= 4.0 for x in tc)
    t = ephem.time_ut(np.array([jdn - 0.5 + 10.0 / 24.0, jdn + 0.5 + 10.0 / 24.0]))
    el = ephem.apparent("mercury", t).separation_from(ephem.apparent("sun", t)).degrees
    h3 = bool(conj and np.all(np.asarray(el) < 10.0))
    days4 = np.arange(-10, -2)
    t4 = ephem.time_ut(jdn - 0.5 + 3.5 / 24.0 + days4)
    sep = ephem.apparent("venus", t4).separation_from(ephem.apparent("mars", t4)).degrees
    h4 = bool(np.min(sep) <= 5.0)
    return jdn, h3, h4


def classify(r):
    """Return the set of Mercury event classes through which r passes G_BM*."""
    cls = set()
    for c, vd, md in ((r["cs"], -5, -34), (r["cp"], -4, -33)):
        if not c or r[f"lead{vd}"] < 90.0:
            continue
        for ev in ("mwra", "gwe", "station"):
            if r[f"d_{ev}{md}"] <= 3.5:
                cls.add(ev)
    return cls


def lattice(name, js, res):
    n = len(js)
    h3 = np.array([res[j][0] for j in js], bool)
    h4 = np.array([res[j][1] for j in js], bool)
    both = int((h3 & h4).sum())
    x3, x4 = int(h3.sum()), int(h4.sum())
    # p if the target passed both / H4 only / H3 only, with weights -log10 q over the pool
    q3, q4 = (x3 / n if n else 0), (x4 / n if n else 0)
    w3 = -np.log10(q3) if q3 > 0 else np.inf
    w4 = -np.log10(q4) if q4 > 0 else np.inf
    s = h3 * w3 + h4 * w4
    s = np.where(np.isnan(s), 0.0, s)
    def p_of(score):
        return (1 + int((s >= score - 1e-12).sum())) / (1 + n)
    out = dict(n=n, x3=x3, x4=x4, x_both=both, q3=round(q3, 4), q4=round(q4, 4),
               p_both=round(p_of(w3 + w4), 4), p_h4_only=round(p_of(w4), 4),
               p_h3_only=round(p_of(w3), 4))
    print(f"{name:8s} n {n:3d}  H3 {x3:3d} (q3 {q3:.3f})  H4 {x4:2d} (q4 {q4:.3f})  both {both}  "
          f"p_min {out['p_both']:.4f}  p(H4 only) {out['p_h4_only']:.4f}  p(H3 only) {out['p_h3_only']:.4f}")
    return out


def main():
    rows = [r for r in json.load(open(ROWS, encoding="utf-8")) if r["jdn"] != T_S]
    print(f"rows (target removed before any computation): {len(rows)}")
    classes = {r["jdn"]: classify(r) for r in rows}
    p_bm = sorted(j for j, c in classes.items() if c)
    p_mwra = sorted(j for j, c in classes.items() if "mwra" in c)
    p_gs = sorted(j for j, c in classes.items() if c and "mwra" not in c)
    assert T_S not in p_bm
    with Pool(14) as p:
        res = {j: (h3, h4) for j, h3, h4 in p.map(held, p_bm, chunksize=4)}
    out = {"P_BM": lattice("P_BM", p_bm, res),
           "P_MWRA": lattice("P_MWRA", p_mwra, res),
           "P_GS": lattice("P_GS", p_gs, res)}
    # Fisher-style 2x2 for H3 by class (MWRA vs not), rough homogeneity look
    a = sum(res[j][0] for j in p_mwra); b = len(p_mwra) - a
    c = sum(res[j][0] for j in p_gs); d = len(p_gs) - c
    from scipy.stats import fisher_exact
    orr, pf = fisher_exact([[a, b], [c, d]])
    print(f"H3 by class: MWRA {a}/{len(p_mwra)}, GWE/station-only {c}/{len(p_gs)}; Fisher p {pf:.3f}")
    a4 = sum(res[j][1] for j in p_mwra); c4 = sum(res[j][1] for j in p_gs)
    print(f"H4 by class: MWRA {a4}/{len(p_mwra)}, GWE/station-only {c4}/{len(p_gs)}")
    out["H3_by_class"] = dict(mwra=[int(a), len(p_mwra)], gs_only=[int(c), len(p_gs)], fisher_p=round(pf, 4))
    out["H4_by_class"] = dict(mwra=[int(a4), len(p_mwra)], gs_only=[int(c4), len(p_gs)])
    # counts per class and per day count, for the record
    seq_only = sum(1 for j in p_mwra if classes[j])
    out["note"] = "rough rows of r2; predicates as heldout_attain.py; target removed before computation"
    json.dump(out, open("results/design-revision-v5/heldout_strata.json", "w"), indent=1)


if __name__ == "__main__":
    main()
