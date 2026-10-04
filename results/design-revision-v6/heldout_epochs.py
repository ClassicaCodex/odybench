"""Design revision 6 scratch: are the held-out pass rates stationary over the
2,200-year background?  (Recheck of revision 5, issue N11.)

Null side only.  The target, 16 Apr -1177 (Day 0, UT+2 civil date), is removed
from the rows BEFORE anything is computed; `held()` (revision 5's function,
imported unchanged) asserts that it is never evaluated.  No target-side value
is computed or printed.

Input: r2's rough candidate rows (results/critique-design-r2/check_gbm_full.rows.json),
read-only, through revision 5's script results/design-revision-v5/heldout_strata.py
(imported, not modified): the same pools (P_BM, P_MWRA), the same rough
predicates H3 and H4 (daily sampling; elongation < 10 deg as the invisibility
proxy).

Reported, per pool:
  - H3 and H4 rates in the early half (-1999..-900) and the late half
    (-899..+200) of the background, with Fisher's exact p;
  - the same within +-700 years of -1177 (-1877..-477) against outside it;
  - the floor p_min and the lattice on the +-700-year pool (a sensitivity);
  - the floor if H4 were dropped from the counted statistic (N2 fix 2a).
Run: cd C:/Projects/odybench && py results/design-revision-v6/heldout_epochs.py
"""
import sys
import json
import importlib.util
from multiprocessing import Pool

import numpy as np
from scipy.stats import fisher_exact

sys.path.insert(0, ".")
from odybench import calendar as cal  # noqa: E402

spec = importlib.util.spec_from_file_location(
    "hs5", "results/design-revision-v5/heldout_strata.py")
hs5 = importlib.util.module_from_spec(spec)
sys.modules["hs5"] = hs5          # so that worker processes can unpickle hs5.held
spec.loader.exec_module(hs5)

T_S = hs5.T_S
YEAR_SPLIT = -900          # early: -1999..-900 ; late: -899..+200
NEAR = (-1877, -477)       # within +-700 years of -1177


def year_of(jdn):
    y, m, d = cal.julian_from_jdn(int(jdn))
    return y


def fisher(a_pass, a_n, b_pass, b_n):
    if a_n == 0 or b_n == 0:
        return float("nan")
    return float(fisher_exact([[a_pass, a_n - a_pass], [b_pass, b_n - b_pass]])[1])


def floor_and_lattice(js, res):
    n = len(js)
    h3 = np.array([res[j][0] for j in js], bool)
    h4 = np.array([res[j][1] for j in js], bool)
    x3, x4, both = int(h3.sum()), int(h4.sum()), int((h3 & h4).sum())
    q3, q4 = (x3 / n if n else 0.0), (x4 / n if n else 0.0)
    w3 = -np.log10(q3) if q3 > 0 else np.inf
    w4 = -np.log10(q4) if q4 > 0 else np.inf
    s = np.where(h3, w3, 0.0) + np.where(h4, w4, 0.0)

    def p_of(score):
        return (1 + int((s >= score - 1e-12).sum())) / (1 + n)
    return dict(n=n, x3=x3, x4=x4, both=both,
                p_both=round(p_of(w3 + w4), 4), p_h4_only=round(p_of(w4), 4),
                p_h3_only=round(p_of(w3), 4),
                p_min_h3_alone=round((1 + x3) / (1 + n), 4))


def main():
    rows = [r for r in json.load(open(hs5.ROWS, encoding="utf-8")) if r["jdn"] != T_S]
    print(f"rows (target removed before any computation): {len(rows)}")
    classes = {r["jdn"]: hs5.classify(r) for r in rows}
    p_bm = sorted(j for j, c in classes.items() if c)
    p_mwra = sorted(j for j, c in classes.items() if "mwra" in c)
    assert T_S not in p_bm
    with Pool(14) as p:
        res = {j: (h3, h4) for j, h3, h4 in p.map(hs5.held, p_bm, chunksize=4)}
    out = {}
    for name, js in (("P_BM", p_bm), ("P_MWRA", p_mwra)):
        yrs = {j: year_of(j) for j in js}
        early = [j for j in js if yrs[j] <= YEAR_SPLIT]
        late = [j for j in js if yrs[j] > YEAR_SPLIT]
        near = [j for j in js if NEAR[0] <= yrs[j] <= NEAR[1]]
        far = [j for j in js if not (NEAR[0] <= yrs[j] <= NEAR[1])]
        rec = {}
        for lab, a, b in (("halves", early, late), ("near_vs_far", near, far)):
            a3 = sum(res[j][0] for j in a); b3 = sum(res[j][0] for j in b)
            a4 = sum(res[j][1] for j in a); b4 = sum(res[j][1] for j in b)
            rec[lab] = dict(n=[len(a), len(b)], H3=[int(a3), int(b3)], H4=[int(a4), int(b4)],
                            fisher_H3=round(fisher(a3, len(a), b3, len(b)), 4),
                            fisher_H4=round(fisher(a4, len(a), b4, len(b)), 4))
            print(f"{name:6s} {lab:12s} n {len(a):3d}/{len(b):3d}  H3 {a3}/{len(a)} vs {b3}/{len(b)} "
                  f"(Fisher p {rec[lab]['fisher_H3']})  H4 {a4}/{len(a)} vs {b4}/{len(b)} "
                  f"(Fisher p {rec[lab]['fisher_H4']})")
        rec["pool_all"] = floor_and_lattice(js, res)
        rec["pool_pm700"] = floor_and_lattice(near, res)
        print(f"{name:6s} whole pool : {rec['pool_all']}")
        print(f"{name:6s} +-700 pool : {rec['pool_pm700']}")
        out[name] = rec
    for key in ("pool_all", "pool_pm700"):
        pmin = max(out["P_BM"][key]["p_both"], out["P_MWRA"][key]["p_both"])
        p4 = max(out["P_BM"][key]["p_h4_only"], out["P_MWRA"][key]["p_h4_only"])
        p3 = max(out["P_BM"][key]["p_h3_only"], out["P_MWRA"][key]["p_h3_only"])
        h3a = max(out["P_BM"][key]["p_min_h3_alone"], out["P_MWRA"][key]["p_min_h3_alone"])
        print(f"rule (max over pools), {key}: p_H,min {pmin}; H4 only {p4}; H3 only {p3}; "
              f"floor if H4 were dropped {h3a}")
        out[f"rule_{key}"] = dict(p_H_min=pmin, p_h4_only=p4, p_h3_only=p3, floor_without_H4=h3a)
    out["note"] = ("rough rows of r2; predicates as revision 4's heldout_attain.py via revision 5's "
                   "heldout_strata.py; target removed before computation; null side only")
    json.dump(out, open("results/design-revision-v6/heldout_epochs.json", "w"), indent=1)


if __name__ == "__main__":
    main()
