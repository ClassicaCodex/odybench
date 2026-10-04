"""Design revision 7 scratch: design-stage estimates of the two inputs of the new
qualifier Q_exch (recheck of revision 6, issue N9):

  (1) drift INSIDE the epoch band: the H3 and H4 pass rates of the epoch pools
      P_BM,E and P_MWRA,E (Day-0 year in -1877..-477) in the band's early half
      (-1877..-1178) against its late half (-1177..-477), with Fisher's exact p;
  (2) the held-out part of P10: H3 and H4 pass rates on eclipse and non-eclipse
      spring new moons (every C_rel spring candidate of r2's rough rows), with
      Fisher's exact p.  Eclipse status is a proxy for "h_tot > 0 at any of the
      five Ionian sites": an eclipse of NASA's site catalogues
      (data/jsex/sites/*.jsonl) within 1.5 d of the conjunction that is total at
      the site for some Delta-T within +-2 sigma (anyTotal2s) at any of the five
      sites; a broader class (visible at some site for some Delta-T within
      +-2 sigma, maxMag2s > 0) is reported beside it.

Null side only.  The target, 16 Apr -1177 (Day 0, UT+2 civil date), is removed
from the rows BEFORE anything is computed; revision 5's `held()` (imported
unchanged, through revision 6's practice) asserts that it is never evaluated.
No target-side value is computed or printed.

Input: r2's rough candidate rows (results/critique-design-r2/check_gbm_full.rows.json),
read-only; rough predicates exactly as revision 4's heldout_attain.py
(daily sampling; elongation < 10 deg as the invisibility proxy).
Run: cd C:/Projects/odybench && py results/design-revision-v7/heldout_exch.py
"""
import sys
import json
import importlib.util
from multiprocessing import Pool

from scipy.stats import fisher_exact

sys.path.insert(0, ".")
from odybench import calendar as cal  # noqa: E402

spec = importlib.util.spec_from_file_location(
    "hs5", "results/design-revision-v5/heldout_strata.py")
hs5 = importlib.util.module_from_spec(spec)
sys.modules["hs5"] = hs5
spec.loader.exec_module(hs5)

T_S = hs5.T_S
BAND = (-1877, -477)
SPLIT = -1177          # early half: -1877..-1178 ; late half: -1177..-477
SITES = ("ithaca", "kefalonia", "lefkada", "corfu", "zakynthos")
OUT = "results/design-revision-v7/heldout_exch"


def year_of(jdn):
    return cal.julian_from_jdn(int(jdn))[0]


def fisher(a_pass, a_n, b_pass, b_n):
    if a_n == 0 or b_n == 0:
        return float("nan")
    return float(fisher_exact([[a_pass, a_n - a_pass], [b_pass, b_n - b_pass]])[1])


def eclipse_status():
    """jdTD of eclipses total (anyTotal2s) or visible (maxMag2s > 0) at any site,
    and of every solar eclipse in NASA's catalogue (each site file lists all 5,486)."""
    tot, vis, anyw = [], [], []
    for s in SITES:
        for line in open(f"data/jsex/sites/{s}.jsonl", encoding="utf-8"):
            r = json.loads(line)
            anyw.append(r["jdTD"])
            if r.get("anyTotal2s"):
                tot.append(r["jdTD"])
            if (r.get("maxMag2s") or -1) > 0:
                vis.append(r["jdTD"])
    return sorted(set(tot)), sorted(set(vis)), sorted(set(anyw))


def near_any(jt, arr, tol=1.5):
    import bisect
    i = bisect.bisect_left(arr, jt - tol)
    return i < len(arr) and arr[i] <= jt + tol


def main():
    rows = [r for r in json.load(open(hs5.ROWS, encoding="utf-8")) if r["jdn"] != T_S]
    assert all(r["jdn"] != T_S for r in rows)
    lines = [f"rows (target removed before any computation): {len(rows)}"]
    jdns = [r["jdn"] for r in rows]
    with Pool(14) as p:
        res = {j: (h3, h4) for j, h3, h4 in p.map(hs5.held, jdns, chunksize=16)}
    out = {"n_rows": len(rows)}

    # (1) drift inside the epoch band
    classes = {r["jdn"]: hs5.classify(r) for r in rows}
    p_bm = sorted(j for j, c in classes.items() if c)
    p_mwra = sorted(j for j, c in classes.items() if "mwra" in c)
    for name, js in (("P_BM,E", p_bm), ("P_MWRA,E", p_mwra)):
        yrs = {j: year_of(j) for j in js}
        band = [j for j in js if BAND[0] <= yrs[j] <= BAND[1]]
        early = [j for j in band if yrs[j] < SPLIT]
        late = [j for j in band if yrs[j] >= SPLIT]
        a3 = sum(res[j][0] for j in early); b3 = sum(res[j][0] for j in late)
        a4 = sum(res[j][1] for j in early); b4 = sum(res[j][1] for j in late)
        rec = dict(n=[len(early), len(late)], H3=[int(a3), int(b3)], H4=[int(a4), int(b4)],
                   fisher_H3=round(fisher(a3, len(early), b3, len(late)), 4),
                   fisher_H4=round(fisher(a4, len(early), b4, len(late)), 4))
        out[name] = rec
        lines.append(f"{name:9s} band halves (-1877..-1178 | -1177..-477): n {len(early)}/{len(late)}  "
                     f"H3 {a3}/{len(early)} vs {b3}/{len(late)} (Fisher p {rec['fisher_H3']})  "
                     f"H4 {a4}/{len(early)} vs {b4}/{len(late)} (Fisher p {rec['fisher_H4']})")

    # (2) the held-out part of P10 on the spring candidates
    tot, vis, anyw = eclipse_status()
    for label, arr in (("any solar eclipse (NASA catalogue, anywhere on Earth)", anyw),
                       ("total-possible (anyTotal2s, any of 5 sites)", tot),
                       ("visible (maxMag2s > 0, any of 5 sites)", vis)):
        ecl = [r["jdn"] for r in rows if near_any(r["jt"], arr)]
        non = [r["jdn"] for r in rows if not near_any(r["jt"], arr)]
        e3 = sum(res[j][0] for j in ecl); n3 = sum(res[j][0] for j in non)
        e4 = sum(res[j][1] for j in ecl); n4 = sum(res[j][1] for j in non)
        rec = dict(n=[len(ecl), len(non)], H3=[int(e3), int(n3)], H4=[int(e4), int(n4)],
                   fisher_H3=round(fisher(e3, len(ecl), n3, len(non)), 4),
                   fisher_H4=round(fisher(e4, len(ecl), n4, len(non)), 4))
        out["P10 " + label] = rec
        lines.append(f"P10 {label}: eclipse n {len(ecl)}, non-eclipse n {len(non)}  "
                     f"H3 {e3}/{len(ecl)} vs {n3}/{len(non)} (Fisher p {rec['fisher_H3']})  "
                     f"H4 {e4}/{len(ecl)} vs {n4}/{len(non)} (Fisher p {rec['fisher_H4']})")
    out["note"] = ("rough rows of r2; predicates as revision 4's heldout_attain.py via revision 5's "
                   "heldout_strata.py; target removed before computation; null side only; eclipse "
                   "status is a catalogue proxy for h_tot > 0")
    print("\n".join(lines))
    open(OUT + ".out.txt", "w", encoding="utf-8").write("\n".join(lines) + "\n")
    json.dump(out, open(OUT + ".json", "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main()
