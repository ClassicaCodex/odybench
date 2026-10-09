"""
almagest.py -- gate 3b and Q_BM of the lean run (LEAN.md; DESIGN 6.4, 9.1):
the Almagest control of B&M's own clue types.  Writes results/alm/alm.json
and results/alm/alm.out.txt.

    py almagest.py --selftest           # synthetic sets only (allowed at any stage)
    py almagest.py                      # the run (LEAN stage 3, after Freeze 1)
    py almagest.py --workers 14 --no-null

LEAN.md stage 1 computes no control search on the real sky.  The run
therefore refuses to start before the git tag prereg-1 exists, unless
--before-freeze is given (and then says so in its output).

The computation is odybench.lean.almagest.run(); attain.py may call it
directly.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "results" / "alm"


def _jsonable(x):
    if isinstance(x, dict):
        return {str(k): _jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    if isinstance(x, np.ndarray):
        return [_jsonable(v) for v in x.tolist()]
    if isinstance(x, (np.bool_,)):
        return bool(x)
    if isinstance(x, np.integer):
        return int(x)
    if isinstance(x, np.floating):
        v = float(x)
        return None if v != v else v
    if isinstance(x, float) and x != x:
        return None
    return x


def freeze_tag_exists(tag: str = "prereg-1") -> bool:
    try:
        r = subprocess.run(["git", "tag", "-l", tag], cwd=ROOT, capture_output=True, text=True, timeout=30)
        return r.stdout.strip() == tag
    except (OSError, subprocess.SubprocessError):
        return False


def _b(x):
    return "yes" if x else "no"


def report(res: dict) -> str:
    """The readable summary written to alm.out.txt."""
    from odybench.lean import almagest as A
    L = []
    w = L.append
    w("odybench lean run: the Almagest control of B&M's clue types (gate 3b, Q_BM; DESIGN 6.4)")
    w(f"stage: {res.get('stage_note', '')}")
    w("")
    w("== Gate 3b (regime SL, leave-one-set-out ceilings; frozen meaning of same_apparition) ==")
    w("leg        seen_ALM_SL  seen_ALM_SL_side  N_narrow_3b  seen among narrowable")
    for leg in A.LEGS:
        nn = res.get("N_narrow_3b", {}).get(leg, "-")
        sn = res.get("seen_among_narrowable", {}).get(leg, "-")
        w(f"{leg:<10} {res['seen_ALM_SL'][leg]:>11}  {res['seen_ALM_SL_side'][leg]:>16}  {nn!s:>11}  {sn!s:>21}")
    g = res["gate_3b"]
    w(f"gate 3b fires (some leg < 6): {_b(g['fires'])}; under the side-only meaning: {_b(g['fires_side'])}; "
      f"Q_score3b: {_b(g['Q_score3b'])}; Q_attain3b: {_b(g.get('Q_attain3b'))}")
    for ln, v in g["lines"].items():
        w(f"  with the line at {float(ln) * 100:g}%: " + ", ".join(f"{k} {n}" for k, n in v["seen_ALM_SL"].items())
          + f"; fires: {_b(v['fires'])}")
    w(f"strict recall in regime SL (no narrowing): {res['strict_recall_SL']}")
    w("")
    w("== Regime BM (B&M's tolerances) ==")
    n_counted = sum(1 for v in res["per_set"].values() if v["counted"])
    w(f"rec_ALM_BM = {res['rec_ALM_BM']} of {n_counted} (strict recall and |S0| <= 5%); Q_BM: {_b(res['Q_BM'])}; "
      f"strict recall without narrowing: {res['strict_recall_BM']}")
    w("")
    w("== Per set, gate window (S0 / B / N_cand; f(truth); seen st, bf; uncovered days) ==")
    for sid, ps in res["per_set"].items():
        tag = "counted" if ps["counted"] else "reported only"
        w(f"{sid} ({tag})")
        for name in [f"SL:{s}" for s in A.STEPS] + [f"SL_side:{s}" for s in A.STEPS] + ["BM"]:
            sc = ps["runs"][name]
            fails = [c for c, r in ps["rows"][name].items() if r["fails"]]
            narrow = res.get("narrowable_3b", {})
            nb = ""
            if name.startswith("SL:") and narrow and ps["counted"]:
                st = name.split(":")[1]
                nb = f" narrowable st/bf {_b(narrow['st:' + st].get(sid))}/{_b(narrow['bf:' + st].get(sid))};"
            w(f"  {name:<15} S0 {sc['S0']:>6} B {sc['B']:>6} N {sc['N_cand']:>6} ({100 * sc.get('frac_S0', 0):.2f}%)"
              f" f(truth) {sc.get('f_truth')!s:>4} rank {sc.get('rank')!s:>5} seen st {_b(sc.get('seen_st'))}"
              f" bf {_b(sc.get('seen_bf'))};{nb} uncovered {sc['n_uncovered']}"
              f"{'' if sc.get('robust_st', True) else ' (seen flag NOT robust to them)'}"
              f"{'; truth fails ' + ', '.join(fails) if fails else ''}")
        sw = ps.get("sensitivity_windows", {})
        if sw:
            w("  20 further windows, fraction seen (st/bf): " + "; ".join(
                f"{k} {v['seen_st']:.2f}/{v['seen_bf']:.2f}" for k, v in sw.items()))
        sens = [k for k in ps["runs"] if k.startswith("sens:")]
        if sens:
            w("  reported sensitivities (gate window): " + "; ".join(
                f"{k[5:]} S0 {ps['runs'][k]['S0']} seen st {_b(ps['runs'][k].get('seen_st'))}" for k in sens))
    w("")
    st = res.get("slack_table")
    if st:
        w("== Observer-slack table recomputed with bench code (truth-side) ==")
        if "error" in st:
            w(f"not computed: {st['error']}")
        else:
            w(f"ceilings agree with almagest_regimes.json: {_b(st['ceilings_agree_with_regime_file'])}")
            w("bench minus drafter, max |difference|: " + "; ".join(
                f"{k} {v['max_abs']:.3f} (n {v['n']})" for k, v in st["bench_minus_drafter"].items()
                if v["max_abs"] is not None))
            for body, vals in st["ge_summary_abs_days"].items():
                w(f"|record - true GE|, {body}: " + ", ".join(f"{k} {v:.1f}" for k, v in
                                                            sorted(vals.items(), key=lambda t: t[1])))
    w("")
    w("== Coverage ==")
    w(json.dumps(res.get("coverage"), default=str))
    w("")
    w("== Deviations from DESIGN 6.4, and why ==")
    for d in res["deviations"]:
        w(f"- {d}")
    w("== Not built ==")
    for d in res["not_built"]:
        w(f"- {d}")
    w(f"elapsed {res.get('elapsed_s')} s")
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Gate 3b and Q_BM: the Almagest control (DESIGN 6.4).")
    ap.add_argument("--selftest", action="store_true", help="synthetic sets only")
    ap.add_argument("--no-real-sky-selftest", action="store_true", help="selftest without the ephemeris part")
    ap.add_argument("--before-freeze", action="store_true",
                    help="run on the real sky although the prereg-1 tag does not exist (LEAN stage 1 forbids it)")
    ap.add_argument("--workers", type=int, default=None)
    ap.add_argument("--no-null", action="store_true", help="skip the 21 null windows (narrowable)")
    ap.add_argument("--no-sensitivity", action="store_true", help="skip the 20 further window positions")
    ap.add_argument("--no-slack", action="store_true", help="skip the observer-slack table")
    ap.add_argument("--no-babylon", action="store_true")
    ap.add_argument("--no-cache", action="store_true")
    ap.add_argument("--out", default=str(OUT_DIR))
    a = ap.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    from odybench.lean import almagest as A
    if a.selftest:
        return 0 if A.selftest(verbose=True, real_sky=not a.no_real_sky_selftest) else 1
    frozen = freeze_tag_exists()
    if not frozen and not a.before_freeze:
        print("refusing: LEAN.md stage 1 computes no control search on the real sky, and the tag prereg-1 does not "
              "exist yet. Freeze first (LEAN.md 'Stages'), or pass --before-freeze deliberately.")
        return 2
    res = A.run(workers=a.workers, null_side=not a.no_null, sensitivity=not a.no_sensitivity,
                babylon=not a.no_babylon, slack=not a.no_slack, cache=not a.no_cache)
    res["stage_note"] = ("after Freeze 1 (tag prereg-1 exists)" if frozen else
                         "RUN BEFORE FREEZE 1 with --before-freeze: LEAN.md stage 1 does not allow this run")
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "alm.json").write_text(json.dumps(_jsonable(res), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    txt = report(res)
    (out / "alm.out.txt").write_text(txt, encoding="utf-8")
    print(txt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
