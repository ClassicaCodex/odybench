"""Design revision 4 scratch: a rough, design-stage estimate of whether the
held-out leg of outcome 1 is ATTAINABLE (critique-design-r2 R2-1 fix 4).

Null side only.  The target, 16 Apr -1177 (Day 0 UT+2), is removed from every
pool BEFORE anything is computed, so no held-out predicate is ever evaluated
on it.  This script never prints or computes a target-side value.

Pools (from r2's candidate rows, results/critique-design-r2/check_gbm_full.rows.json,
which hold every C_rel spring conjunction of -1999..+200 at Ithaki with the
slot and B&M quantities r2 computed; read-only use):
  * P_BM  : candidates (day or night) passing at least one reading of G_BM*
            (C on the day count; Venus lead >= 90 min on Day -5/-4; a morning
            Mercury event within 3.5 d on Day -34/-33);
  * T_A   : daylight candidates satisfying revision 3's slots (Venus AV 7;
            Mercury event <= 6 d or visible), same day count;
  * T_A_doc: daylight candidates with Venus AV 7 and Mercury event <= 6 d AND
            visible (B&M's "named turning point, visible").
Held-out predicates (DESIGN rev 1 H3 and H4, unchanged in substance):
  * H3: Mercury within +-3 d of a geocentric conjunction in longitude with the
        Sun on Day 0 or Day +1 (conjunction instant in [Day -3 noon,
        Day +4 noon], UT+2), and elongation < 10 deg on Day 0 and Day +1
        (rough proxy for "not visible at AV 10").
  * H4: Venus-Mars geocentric separation <= 5 deg on some day in Day -10..-3
        (covers seq Day -7 +- 3 and par Day -6 +- 3), at 03:30 UT.
Statistic: score s = sum_i pass_i * (-log10 q_i); the most extreme possible
observation is "passes both", so p_H,min = (1 + x_both) / (1 + n).
Approximations: geocentric, no visibility model, DE441, SMH2020 Delta-T.
Run: cd C:/Projects/odybench && py results/design-revision-r3/heldout_attain.py
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
    # H3: daily at 10:00 UT (12:00 UT+2), Day -4 .. +5
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
    # H4: Day -10 .. -3 at 03:30 UT
    days4 = np.arange(-10, -2)
    t4 = ephem.time_ut(jdn - 0.5 + 3.5 / 24.0 + days4)
    sep = ephem.apparent("venus", t4).separation_from(ephem.apparent("mars", t4)).degrees
    h4 = bool(np.min(sep) <= 5.0)
    return jdn, h3, h4


def main():
    rows = [r for r in json.load(open(ROWS, encoding="utf-8")) if r["jdn"] != T_S]
    print(f"rows (target removed before any computation): {len(rows)}")

    def f(r, k):
        return r[k]
    pools = {"P_BM": [], "T_A": [], "T_A_doc": []}
    for r in rows:
        bm = False
        sa = sd = False
        for c, vd, md in ((r["cs"], -5, -34), (r["cp"], -4, -33)):
            if not c:
                continue
            ev = min(r[f"d_mwra{md}"], r[f"d_gwe{md}"], r[f"d_station{md}"])
            if r[f"lead{vd}"] >= 90.0 and ev <= 3.5:
                bm = True
            if r[f"vslot{vd}"] and (ev <= 6.0 or r[f"mvis{md}"]):
                sa = True
            if r[f"vslot{vd}"] and (ev <= 6.0 and r[f"mvis{md}"]):
                sd = True
        if bm:
            pools["P_BM"].append(r["jdn"])
        if r["day"] and sa:
            pools["T_A"].append(r["jdn"])
        if r["day"] and sd:
            pools["T_A_doc"].append(r["jdn"])
    allj = sorted(set(pools["P_BM"]) | set(pools["T_A"]) | set(pools["T_A_doc"]))
    assert T_S not in allj
    with Pool(14) as p:
        res = {j: (h3, h4) for j, h3, h4 in p.map(held, allj, chunksize=4)}
    out = {}
    for name, js in pools.items():
        n = len(js)
        h3 = np.array([res[j][0] for j in js])
        h4 = np.array([res[j][1] for j in js])
        both = int((h3 & h4).sum())
        q3, q4 = h3.mean(), h4.mean()
        pmin = (1 + both) / (1 + n)
        out[name] = dict(n=n, q3=round(float(q3), 4), q4=round(float(q4), 4), x_both=both,
                         x_h3=int(h3.sum()), x_h4=int(h4.sum()), p_H_min=round(pmin, 4),
                         p_if_only_h4=round((1 + int(h4.sum())) / (1 + n), 4),
                         p_if_only_h3=round((1 + int(h3.sum())) / (1 + n), 4))
        print(f"{name:8s} n {n:4d}  q3 {q3:.3f} ({int(h3.sum())})  q4 {q4:.3f} ({int(h4.sum())})  "
              f"both {both}  p_H,min = (1+{both})/(1+{n}) = {pmin:.4f}  "
              f"[p if only H4 passed {out[name]['p_if_only_h4']:.3f}; only H3 {out[name]['p_if_only_h3']:.3f}]")
    json.dump(out, open("results/design-revision-r3/heldout_attain.json", "w"), indent=1)


if __name__ == "__main__":
    main()
