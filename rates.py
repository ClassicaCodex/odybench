"""
rates.py -- N1, how often B&M's criteria pass by chance (DESIGN 5.1), and N5's
rate curves (5.5, the part LEAN.md runs).  Agent L1.

NULL SIDE: the pool is built with 16 Apr -1177 masked (candidates.load).  The
real run belongs to LEAN.md stage 3, after the first freeze; it refuses to run
unless the git tag prereg-1 exists (override --no-freeze-check).  attain.py
calls n1() and n5() itself; this script exists to run them alone.

  py rates.py --run          real sky, target masked -> results/rates/rates.json
  py rates.py --selftest     synthetic pool

N1 (5.1), with the B&M reading = B&M's criteria on the sequential count:
C (C_rel, and the fixed Julian bounds beside), V (Venus lead >= 90 min on
Day -5), M (a morning rise-azimuth maximum, vertex, within 1.5 d of Mercury's
rising on Day -34: the G_BM* member (seq, mwra, 1.5, off); the maximum
whatever Mercury's side, T0b's literal MWRA, is reported beside), E (E_rel,
n = 3, 4, 5), SMH2020 Delta-T, site ithaki.
  2. lambda per century (22 centuries of background), exact Poisson interval,
     for N C V M and N C V M E;
  3. against B&M's printed 0.048 per century (R19) and their arithmetic at
     +-1 d, 0.88 per century (R13); the +-1.0 d continuous tolerance beside;
  4. lambda for each of the 22 centuries, relative and fixed bounds;
  5. P(>= 1) and the mean count over windows of 50..900 years slid by one year,
     beside the Poisson values;
  6. p_fix|C (primary: the C-passing candidates of the sequential count, V and
     M on that count; P_spring with either count reported beside) and p_fix
     over P_all;
  7. the V-M dependence ratio P(V M)/(P(V) P(M)) on P_spring, against 10,000
     permutations of the Venus outcome within 7-day bins of Day 0's day of
     year (the "same Ti day of year +- 3 d" of 5.1 item 7, as a partition);
  8. "without N" (Day 0 any day) is not run: it needs the sky of every day in
     each season, including the target's own clue days (LEAN.md lists N1's
     outputs without it).
N5 (part): survivors per century for every reading of G_BM*, P(>= 1) as a
curve over W = 50..900 years, and the survivors of each named window.
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import numpy as np  # noqa: E402

from odybench import calendar as cal  # noqa: E402
from odybench.lean import candidates as Cn  # noqa: E402
from odybench.lean import reach as Rc  # noqa: E402
from odybench.lean import readings as Rd  # noqa: E402

OUT = ROOT / "results" / "rates"
CENTURY_D = 100 * Rc.YEAR_D
BM_PRINTED = 0.048          # per century, E on [B&M; rev #5]
BM_ARITH_1D = 0.88          # per century, E off, B&M's arithmetic at +-1 d [rev #5]


def _seeds():
    return json.loads((ROOT / "data" / "prereg" / "seeds.json").read_text(encoding="utf-8"))["purposes"]


def background_bounds_tt(pool, years=Cn.BACKGROUND):
    """[b0, b1) of the background as TT instants (UT+2 midnights + Delta-T)."""
    a_ut, b_ut = cal.span_bounds((years[0], 1, 1), (years[1], 12, 31), offset_hours=2)
    if pool.meta.get("synthetic"):
        return a_ut + 0.33, b_ut + 0.33
    from odybench.lean import sky
    return float(sky.tt_of_ut(a_ut)), float(sky.tt_of_ut(b_ut))


def lam(mask, centuries):
    k = int(np.sum(mask))
    r, lo, hi = Rc.poisson_rate(k, centuries)
    return dict(k=k, per_century=r, lo=lo, hi=hi)


def centuries_table(pool, mask, years=Cn.BACKGROUND):
    out = []
    for c0 in range(years[0], years[1] + 1, 100):
        sel = pool.in_years(c0, c0 + 99)
        out.append(dict(years=[c0, c0 + 99], k=int(np.sum(mask & sel))))
    return out


def window_curve(jd, b0, b1, widths):
    return {int(w): dict(zip(("empirical", "poisson", "mean"), Rc.p_at_least_one(jd, w * Rc.YEAR_D, b0, b1)))
            for w in widths}


def permutation_dependence(V, M, doy, n_perm, seed, bin_days=7):
    """Observed joint V-M count against permutations of V within day-of-year bins."""
    V = np.asarray(V, bool)
    M = np.asarray(M, bool)
    n = V.size
    pv, pm, pvm = V.mean(), M.mean(), (V & M).mean()
    ratio = pvm / (pv * pm) if pv * pm > 0 else float("nan")
    rng = np.random.default_rng(seed)
    bins = (np.asarray(doy) - 1) // bin_days
    groups = [np.nonzero(bins == b)[0] for b in np.unique(bins)]
    obs = int(np.sum(V & M))
    joint = np.empty(n_perm, dtype=np.int64)
    Vp = V.copy()
    for k in range(n_perm):
        for g in groups:
            if g.size > 1:
                Vp[g] = V[g][rng.permutation(g.size)]
        joint[k] = int(np.sum(Vp & M))
    return dict(n=n, P_V=float(pv), P_M=float(pm), P_VM=float(pvm), ratio=float(ratio), joint_obs=obs,
                joint_perm_mean=float(joint.mean()),
                p_upper=float((1 + np.sum(joint >= obs)) / (1 + n_perm)),
                p_lower=float((1 + np.sum(joint <= obs)) / (1 + n_perm)),
                n_perm=n_perm, bins_days=bin_days)


def n1(pool, n_perm=10000, seed=None, years=Cn.BACKGROUND):
    pool.guard("N1")
    if seed is None:
        seed = _seeds()["n1_permutation"]["seeds"]["venus_mercury"]
    bg = pool.in_years(*years)
    nc = (years[1] - years[0] + 1) / 100.0
    b0, b1 = background_bounds_tt(pool, years)
    out = dict(centuries=nc, n_P_all=int(bg.sum()))
    for ck in ("rel", "fix"):
        base = Rd.bm_reading(pool, c_kind=ck) & bg
        d = dict(NCVM=lam(base, nc))
        for n in (3, 4, 5):
            d[f"NCVME_n{n}"] = lam(Rd.bm_reading(pool, c_kind=ck, e_n=n, e_kind=ck) & bg, nc)
        d["NCVM_tol1.0"] = lam(Rd.bm_reading(pool, c_kind=ck, tol=1.0) & bg, nc)
        d["NCVM_mwra_any_side"] = lam(Rd.bm_reading(pool, c_kind=ck, event="mwra_any") & bg, nc)
        d["by_century_NCVM"] = centuries_table(pool, base, years)
        d["by_century_NCVME_n4"] = centuries_table(pool, Rd.bm_reading(pool, c_kind=ck, e_n=4, e_kind=ck) & bg,
                                                   years)
        d["windows_NCVM"] = window_curve(pool.jd_tt[base], b0, b1, Cn.windows()["widths"]["n1_sliding"])
        d["windows_NCVME_n4"] = window_curve(pool.jd_tt[Rd.bm_reading(pool, c_kind=ck, e_n=4, e_kind=ck) & bg],
                                             b0, b1, Cn.windows()["widths"]["n1_sliding"])
        d["survivors_NCVM"] = [_lab(j) for j in pool.day0[base]]
        out[f"C_{ck}"] = d
    rel = out["C_rel"]
    out["R19_vs_BM_printed"] = {f"n{n}": dict(lambda_=rel[f"NCVME_n{n}"]["per_century"], printed=BM_PRINTED,
                                              ratio=rel[f"NCVME_n{n}"]["per_century"] / BM_PRINTED)
                                for n in (3, 4, 5)}
    out["R13_vs_BM_arith"] = dict(lambda_=rel["NCVM"]["per_century"], arith=BM_ARITH_1D,
                                  ratio=rel["NCVM"]["per_century"] / BM_ARITH_1D,
                                  lambda_tol1=rel["NCVM_tol1.0"]["per_century"])
    # p_fix
    cs = Rd.C(pool, "seq") & bg
    vm = Rd.V(pool, "seq") & Rd.M(pool, "seq", "mwra", 1.5)
    sp = pool.P_spring() & bg
    vm_any = np.zeros(len(pool), dtype=bool)
    for cnt in ("seq", "par"):
        vm_any |= Rd.C(pool, cnt) & Rd.V(pool, cnt) & Rd.M(pool, cnt, "mwra", 1.5)
    out["p_fix_given_C"] = dict(value=float((cs & vm).sum() / max(1, cs.sum())), k=int((cs & vm).sum()),
                                n=int(cs.sum()), pool="C_rel on the sequential count")
    out["p_fix_given_C_P_spring"] = dict(value=float((sp & vm_any).sum() / max(1, sp.sum())),
                                         k=int((sp & vm_any).sum()), n=int(sp.sum()),
                                         pool="P_spring, V and M on a count on which C holds")
    out["p_fix"] = dict(value=float((cs & vm).sum() / max(1, bg.sum())), k=int((cs & vm).sum()),
                        n=int(bg.sum()), pool="P_all")
    out["VM_dependence"] = permutation_dependence(Rd.V(pool, "seq")[sp], Rd.M(pool, "seq", "mwra", 1.5)[sp],
                                                  pool.cols["doy"][sp], n_perm, seed)
    out["VM_dependence"]["pool"] = "P_spring; the B&M reading's V (Day -5) and M (Day -34)"
    out["without_N"] = "not run: needs every day's sky in each season, the target's clue days included (LEAN.md N1)"
    return out


def _lab(jdn):
    y, m, d = cal.julian_from_jdn(int(jdn))
    return f"{y}-{m:02d}-{d:02d}"


def n5(pool, pass_array=None, years=Cn.BACKGROUND):
    pool.guard("N5")
    pa = Rd.passes(pool) if pass_array is None else pass_array
    bg = pool.in_years(*years)
    nc = (years[1] - years[0] + 1) / 100.0
    b0, b1 = background_bounds_tt(pool, years)
    per_reading = {r.key: dict(k=int((pa[i] & bg).sum()), per_century=float((pa[i] & bg).sum() / nc))
                   for i, r in enumerate(Rd.READINGS)}
    bm = Rd.bm_reading(pool) & bg
    bme = Rd.bm_reading(pool, e_n=4) & bg
    widths = list(range(50, 901, 10))
    curve = dict(NCVM=window_curve(pool.jd_tt[bm], b0, b1, widths),
                 NCVME_n4=window_curve(pool.jd_tt[bme], b0, b1, widths),
                 any_G_BM_reading=window_curve(pool.jd_tt[pa.any(axis=0) & bg], b0, b1, widths))
    named = {}
    for name, w in Cn.windows()["named"].items():
        sel = pool.in_years(*w["years"])
        named[name] = dict(years=w["years"], NCVM=[_lab(j) for j in pool.day0[bm & sel]],
                           NCVME_n4=[_lab(j) for j in pool.day0[bme & sel]],
                           per_reading={r.key: int((pa[i] & sel).sum()) for i, r in enumerate(Rd.READINGS)})
    return dict(per_reading=per_reading, curve=curve, named_windows=named,
                note="survivor lists are null-side (16 Apr -1177 masked); eclipse new moons per window are L2's")


def freeze_tag_exists(tag):
    try:
        out = subprocess.run(["git", "-C", str(ROOT), "tag", "-l", tag], capture_output=True, text=True,
                             timeout=20).stdout
        return tag in out.split()
    except Exception:                       # noqa: BLE001
        return False


def selftest():
    p = Cn.synthetic(n_years=800, y0=-1500, seed=11)
    yrs = (-1500, -701)
    a = n1(p, n_perm=500, seed=1, years=yrs)
    b = n5(p, years=yrs)
    k = a["C_rel"]["NCVM"]["k"]
    assert abs(a["C_rel"]["NCVM"]["per_century"] - k / 8.0) < 1e-12
    assert sum(c["k"] for c in a["C_rel"]["by_century_NCVM"]) == k
    for w, v in a["C_rel"]["windows_NCVM"].items():
        if w <= yrs[1] - yrs[0] + 1:
            assert 0 <= v["empirical"] <= 1 and v["mean"] >= 0, (w, v)
        else:
            assert math.isnan(v["empirical"]), (w, v)        # a window wider than the span
    assert a["C_rel"]["NCVME_n4"]["k"] <= k
    # an independent V and M give a dependence ratio near 1 and a large permutation p
    assert 0.5 < a["VM_dependence"]["ratio"] < 2.0, a["VM_dependence"]
    assert b["per_reading"]["seq/mwra/1.5/novis"]["k"] == int((Rd.passes(p)[Rd.T0B_INDEX] & p.in_years(*yrs)).sum())
    print(f"[rates selftest] lambda(NCVM) {a['C_rel']['NCVM']['per_century']:.3f}/cy "
          f"[{a['C_rel']['NCVM']['lo']:.3f}, {a['C_rel']['NCVM']['hi']:.3f}], "
          f"P(>=1, 136 y) {a['C_rel']['windows_NCVM'][136]['empirical']:.3f} vs Poisson "
          f"{a['C_rel']['windows_NCVM'][136]['poisson']:.3f}; V-M ratio {a['VM_dependence']['ratio']:.2f}")
    print("[rates selftest] PASS")


def _js(o):
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.floating):
        return float(o)
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError(type(o))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--no-freeze-check", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        selftest()
    elif a.run:
        if not (a.no_freeze_check or freeze_tag_exists("prereg-1")):
            sys.exit("rates.py is null-side: run it after the first freeze (git tag prereg-1), "
                     "or pass --no-freeze-check")
        pool = Cn.load(mask_target=True)
        res = dict(N1=n1(pool), N5=n5(pool), masked=True, code_sha256=Cn.code_hash())
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / "rates.json").write_text(json.dumps(res, indent=1, ensure_ascii=False, default=_js),
                                        encoding="utf-8")
        print(json.dumps({k: res["N1"][k] for k in ("R19_vs_BM_printed", "R13_vs_BM_arith", "p_fix_given_C",
                                                     "p_fix", "VM_dependence")}, indent=1, default=_js))
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
