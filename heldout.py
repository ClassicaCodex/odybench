"""
heldout.py -- the held-out test at the target (LEAN.md stage 5; DESIGN 7.1-7.3,
9.1).  Agent L2.

Target stage only.  It refuses to run unless results/attain/attain.json (the
null side, written by attain.py with the target masked) and the marker
results/attain/FROZEN (written by the integrator at the second freeze) both
exist.  It then:

1. reads the four held-out pools (and P_spring if present) with their members'
   H3/H4 flags from attain.json, and recomputes the null side with
   odybench.lean.heldout.null_side (p_H,min, the lattice, Q_record, Q_exch),
   comparing it with the values attain.json stored;
2. reads the target's membership of each pool and the day count on which it
   passes a defining reading (--target-info; see TARGET INFO below);
3. evaluates H1-H5 at 16 Apr -1177 (allow_target=True) with their margins;
4. computes p_P for each pool, p_H and Q_contra (odybench.lean.heldout.p_value);
5. reports H1, H2 and H5 with their base rates over the pools (7.3);
6. writes results/heldout/heldout.json and heldout.out.txt.

ATTAIN.JSON, the pools.  Looked up at attain["heldout"]["pools"], then
attain["heldout_pools"], then attain["pools"].  Each pool is either a dict of
equal-length columns or a list of member records, with at least
day0_jdn_ut2 (int), H3 and H4 (bool); optional year, count ('seq' | 'par' |
'both'), eclipse (bool, P_spring), H1, H2, H5.  Names: P_BM, P_MWRA, P_BM_E,
P_MWRA_E (P_spring optional).  The stored null side, if any, is read from
attain["heldout"]["null_side"] (the dict null_side() returns) or from the
flat keys p_H_min, Q_record, Q_exch.

TARGET INFO.  A JSON file (default: results/t0/t0.json, key
"heldout_target"; or the file given by --target-info, either that key or the
whole file) of the form
    {"P_BM": {"member": true, "count": "seq"}, "P_MWRA": {...}, "P_BM_E": {...},
     "P_MWRA_E": {...}}
"member": the target passes a reading that defines the pool (7.2);
"count": the day count of such a reading ('both' if it passes on both).
Without it the script stops: membership is an input, never assumed.

  py heldout.py                       # target stage, after the second freeze
  py heldout.py --target-info FILE
  py heldout.py --selftest            # synthetic pools; evaluates no sky
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from odybench import calendar as cal  # noqa: E402
from odybench.lean import heldout as H  # noqa: E402

ATTAIN = ROOT / "results" / "attain" / "attain.json"
FROZEN = ROOT / "results" / "attain" / "FROZEN"
T0_JSON = ROOT / "results" / "t0" / "t0.json"
OUT = ROOT / "results" / "heldout"


# ------------------------------------------------------------------ input

def _to_structured(name, pool):
    if isinstance(pool, dict) and "members" in pool:
        pool = pool["members"]
    if isinstance(pool, list):
        cols = {}
        for rec in pool:
            for k, v in rec.items():
                cols.setdefault(k, []).append(v)
        pool = cols
    if not isinstance(pool, dict):
        raise ValueError(f"pool {name}: expected a dict of columns or a list of records")
    for k in ("day0_jdn_ut2", "H3", "H4"):
        if k not in pool:
            raise ValueError(f"pool {name}: missing field {k}")
    jdn = np.asarray(pool["day0_jdn_ut2"], dtype=np.int64)
    fields = {}
    for k in ("H1", "H2", "H3", "H4", "H5", "eclipse"):
        if k in pool:
            fields[k] = np.asarray(pool[k], dtype=bool)
    if H.GWE_FIELD in pool:
        fields[H.GWE_FIELD] = np.asarray(pool[H.GWE_FIELD], dtype=float)
    a = H.structured(jdn, **fields)
    if "year" in pool:
        given = np.asarray(pool["year"], dtype=np.int64)
        if not np.array_equal(given, a["year"]):
            raise ValueError(f"pool {name}: 'year' disagrees with the Julian year of day0_jdn_ut2")
    count = np.asarray(pool["count"], dtype=object) if "count" in pool else None
    return a, count


def load_pools(attain):
    for path in (("heldout", "pools"), ("heldout_pools",), ("pools",)):
        d = attain
        try:
            for k in path:
                d = d[k]
        except (KeyError, TypeError):
            continue
        if isinstance(d, dict) and all(P in d for P in H.POOLS):
            pools, counts = {}, {}
            for name, pool in d.items():
                if name in H.POOLS or name == H.SPRING_POOL:
                    pools[name], counts[name] = _to_structured(name, pool)
            return pools, counts, ".".join(path)
    raise SystemExit("attain.json holds no held-out pools (looked at heldout.pools, heldout_pools, pools)")


def stored_null(attain):
    d = attain.get("heldout", {}).get("null_side") if isinstance(attain.get("heldout"), dict) else None
    if d:
        return d
    keys = ("p_H_min", "Q_record", "Q_exch", "Q_attain")
    flat = {k: attain[k] for k in keys if k in attain}
    return flat or None


def _find_key(d, key, depth=0):
    if not isinstance(d, dict) or depth > 3:
        return None
    if key in d:
        return d[key]
    for v in d.values():
        r = _find_key(v, key, depth + 1)
        if r is not None:
            return r
    return None


def load_target_info(path=None):
    cands = [Path(path)] if path else [T0_JSON]
    for p in cands:
        if not p.exists():
            continue
        d = json.loads(p.read_text(encoding="utf-8"))
        info = _find_key(d, "heldout_target") or d
        if all(P in info for P in H.POOLS):
            out = {}
            for P in H.POOLS:
                rec = info[P]
                if not isinstance(rec, dict) or "member" not in rec or "count" not in rec:
                    raise SystemExit(f"{p}: {P} needs 'member' and 'count'")
                if rec["count"] is None:
                    if rec["member"]:
                        raise SystemExit(f"{p}: {P}: a member needs the count of its defining reading")
                    out[P] = dict(member=False, count=None)     # p = 1 there; the count is moot
                    continue
                c = str(rec["count"]).lower()
                c = "both" if c == "either" else c
                if c not in H.COUNTS:
                    raise SystemExit(f"{p}: {P} count {rec['count']!r}")
                out[P] = dict(member=bool(rec["member"]), count=c)
            return out, str(p)
    raise SystemExit("no target info: the target's membership of each pool and its day count are inputs "
                     f"(7.2). Give --target-info FILE, or put key 'heldout_target' in {T0_JSON}.")


# ------------------------------------------------------------------- run

def _jsonable(o):
    if isinstance(o, dict):
        return {str(k): _jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_jsonable(v) for v in o]
    if isinstance(o, np.ndarray):
        return [_jsonable(v) for v in o.tolist()]
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating, float)):
        f = float(o)
        return f if np.isfinite(f) else (None if np.isnan(f) else ("inf" if f > 0 else "-inf"))
    return o


def target_flags(info):
    """H1-H5 with margins at 16 Apr -1177, for each count the pools need."""
    out = {}
    for c in sorted({info[P]["count"] for P in H.POOLS if info[P]["count"]} or {"both"}):
        r = H.evaluate(np.array([H.TARGET_JDN]), c, allow_target=True)
        out[c] = {k: (v[0].item() if hasattr(v[0], "item") else v[0]) for k, v in r.items()}
        out[c]["tie_bands"] = H.tie_band(r)
    return out


def base_rates(pools, counts):
    """H1, H2, H5 rates over each pool (7.3); computed for the members when
    attain.json did not store them (null-side members, not the target)."""
    rates = {}
    for P in H.POOLS:
        pool = pools[P]
        names = pool.dtype.names
        have = all(h in names for h in ("H1", "H2", "H5"))
        if have:
            f = {h: pool[h] for h in ("H1", "H2", "H5")}
            src = "attain.json"
        else:
            cnt = counts.get(P)
            cnt = cnt if cnt is not None else np.full(len(pool), "both", dtype=object)
            f = H.flags(pool["day0_jdn_ut2"], cnt, predicates=("H1", "H2", "H5"))
            src = "computed here" + ("" if counts.get(P) is not None else " (count 'both': attain.json gave none)")
        rates[P] = {h: dict(x=int(np.sum(f[h])), n=int(len(pool))) for h in ("H1", "H2", "H5")}
        rates[P]["source"] = src
    return rates


def run(attain_path=ATTAIN, info_path=None, out=OUT):
    attain = json.loads(Path(attain_path).read_text(encoding="utf-8"))
    pools, counts, where = load_pools(attain)
    det = H.load_determined()
    ns = H.null_side(pools, determined=det)
    stored = stored_null(attain)
    checks = []
    if stored:
        for k in ("p_H_min", "Q_record", "Q_exch", "Q_attain"):
            if k in stored:
                a, b = stored[k], ns[k]
                same = (abs(float(a) - float(b)) < 1e-12) if k == "p_H_min" else (bool(a) == bool(b))
                checks.append(dict(key=k, attain=a, recomputed=b, agree=same))
    info, info_src = load_target_info(info_path)
    tf = target_flags(info)
    fallback = sorted(tf)[0]                                   # a non-member pool: its p is 1 whatever
    per_pool = {P: {"H3": bool(tf[info[P]["count"] or fallback]["H3"]),
                    "H4": bool(tf[info[P]["count"] or fallback]["H4"])} for P in H.POOLS}
    membership = {P: info[P]["member"] for P in H.POOLS}
    pv = H.p_value(pools, per_pool, membership, determined=det)
    rates = base_rates(pools, counts)
    res = dict(
        stage="target (after the second freeze)",
        target=dict(date="16 Apr -1177 (1178 BC)", day0_jdn_ut2=H.TARGET_JDN),
        site=dict(lat=H.LAT, lon=H.LON),
        attain=dict(path=str(Path(attain_path).relative_to(ROOT)) if Path(attain_path).is_relative_to(ROOT)
                    else str(attain_path), sha256=hashlib.sha256(Path(attain_path).read_bytes()).hexdigest(),
                    pools_at=where),
        target_info=dict(source=info_src, per_pool=info),
        target_flags=tf,
        flags_per_pool=per_pool,
        p=pv["p"], p_H=pv["p_H"], weights=pv["weights"], x=pv["x"], n=pv["n"], member=pv["member"],
        pattern=pv["pattern"],
        determined=det, Q_contra=pv["Q_contra"], contra_flags=pv["contra_flags"],
        Q_record=ns["Q_record"], Q_attain=ns["Q_attain"], Q_exch=ns["Q_exch"], p_H_min=ns["p_H_min"],
        null_side=ns, null_side_checks=checks,
        base_rates=rates,
        label_1_leg=dict(p_H_le_0_05=bool(pv["p_H"] <= H.P_MAX)),
    )
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "heldout.json").write_text(json.dumps(_jsonable(res), indent=1, ensure_ascii=False), encoding="utf-8")
    txt = report(res)
    (out / "heldout.out.txt").write_text(txt, encoding="utf-8")
    print(txt)
    return res


def _f(x, nd=4):
    return "-" if x is None else (f"{x:.{nd}f}" if isinstance(x, float) else str(x))


def report(res):
    L = []
    p = L.append
    p("Held-out test at the target, 16 Apr -1177 (DESIGN 7.1-7.3; LEAN.md)")
    p(f"site Ithaki {res['site']['lat']} N {res['site']['lon']} E; target info from {res['target_info']['source']}")
    p("")
    p("Predicates at the target (H3, H4 counted; H1, H2, H5 reported only):")
    for c, f in res["target_flags"].items():
        p(f"  count {c}:")
        p(f"    H3 {f.get('H3')}: Mercury visibility margin {_f(f.get('H3_vis_margin'), 3)} deg "
          f"(>= 0 visible); conjunction {_f(f.get('H3_conj_offset_d'), 3)} d from noon UT+2 of Day 0, "
          f"window margin {_f(f.get('H3_conj_margin_d'), 3)} d")
        p(f"    H4 {f.get('H4')}: least Venus-Mars separation {_f(f.get('H4_min_sep_deg'), 3)} deg on Day "
          f"{f.get('H4_min_day')} (threshold 5)")
        p(f"    H1 {f.get('H1')}: nights {_f(f.get('H1_night_a_h'), 2)} h and {_f(f.get('H1_night_b_h'), 2)} h (>= 12.0)")
        p(f"    H2 {f.get('H2')}: Moon up {_f(f.get('H2_share'), 3)} of the dark hours (< 0.25)")
        p(f"    H5 {f.get('H5')}: Mars visibility margin {_f(f.get('H5_vis_margin'), 3)} deg (H5 needs < 0)")
        p(f"    I15 tie bands the target lies in: {f.get('tie_bands') or 'none'}")
    p("")
    p("Pools (n; H3 only, H4 only, both; floor) and the target's p:")
    for P in H.POOLS:
        c = res["null_side"]["pools"][P]
        p(f"  {P:9s} n {c['n']:4d}; {c['h3_only']:3d} {c['h4_only']:3d} {c['both']:3d}; floor {c['floor']:.4f}; "
          f"member {res['member'][P]}, count {res['target_info']['per_pool'][P]['count']}, pattern "
          f"{res['pattern'][P]}, x {res['x'][P]}, p {res['p'][P]:.4f}")
    p(f"p_H = {res['p_H']:.4f} (label 1 needs <= 0.05); p_H,min = {res['p_H_min']:.4f} (Q_attain if > 0.05)")
    p("lattice (p_BM / p_MWRA / p_BM,E / p_MWRA,E -> p_H), from the null side:")
    for pat, v in res["null_side"]["lattice"].items():
        p(f"  {pat:5s} " + " / ".join(f"{v['p'][P]:.4f}" for P in H.POOLS) + f" -> {v['p_H']:.4f}")
    p("")
    p(f"disclosure table, determined: {res['determined']}")
    p(f"Q_record {res['Q_record']}   Q_contra {res['Q_contra']} {res['contra_flags']}   "
      f"Q_attain {res['Q_attain']}   Q_exch {res['Q_exch']}"
      + ("" if res["null_side"]["Q_exch_complete"] else " (P10's held-out part not computed)"))
    if res["null_side_checks"]:
        p("null side recomputed against attain.json: " + "; ".join(
            f"{c['key']} {'agrees' if c['agree'] else 'DIFFERS'}" for c in res["null_side_checks"]))
    p("")
    rep = res["null_side"].get("reported", {})
    g = rep.get("H3_given_D4", {})
    p("H3 given D4 (7.3): " + (f"{g['x']}/{g['n']} ({g['rule']})" if "x" in g else f"not computed: {g.get('reason')}"))
    for t in rep.get("R20", []) + rep.get("R21", []):
        p(f"  {t['test']}: {t['a_pass']}/{t['a_n']} vs {t['b_pass']}/{t['b_n']}, Fisher p {_f(t['fisher_p'], 3)}")
    p("")
    p("Base rates of the uncounted predicates over the pools (7.3):")
    for P, r in res["base_rates"].items():
        p(f"  {P:9s} " + "  ".join(f"{h} {r[h]['x']}/{r[h]['n']}" for h in ("H1", "H2", "H5")) + f"  ({r['source']})")
    return "\n".join(L) + "\n"


# --------------------------------------------------------------- selftest

def selftest():
    """Synthetic pools at the design-stage counts of 7.2; synthetic target
    patterns.  No sky is evaluated."""
    def pool(n, a3, a4, ab, lo, hi, seed):
        h3 = np.array([True] * ab + [True] * a3 + [False] * a4 + [False] * (n - ab - a3 - a4))
        h4 = np.array([True] * ab + [False] * a3 + [True] * a4 + [False] * (n - ab - a3 - a4))
        perm = np.random.default_rng(seed).permutation(n)
        years = np.round(np.linspace(lo, hi, n)).astype(int)
        return H.structured(np.array([cal.jdn_from_julian(int(y), 4, 1) for y in years]), H3=h3[perm], H4=h4[perm])
    counts = {"P_BM": (76, 14, 1, 1), "P_MWRA": (43, 8, 1, 0), "P_BM_E": (49, 9, 1, 1), "P_MWRA_E": (28, 6, 1, 0)}
    pools = {P: pool(*c, *((-1870, -480) if P.endswith("_E") else (-1990, 190)), k)
             for k, (P, c) in enumerate(counts.items())}
    det = H.load_determined()
    ns = H.null_side(pools, determined=det)
    ok = True
    print("selftest: design-stage counts (7.2)")
    print(f"  p_H,min {ns['p_H_min']:.4f} (7.2: 0.040); Q_attain {ns['Q_attain']}; Q_record {ns['Q_record']} "
          f"(determined {det}); Q_exch {ns['Q_exch']} (P10 part {ns['P10_heldout_part']})")
    expect = {"both": 0.040, "h4": 0.069, "h3": 0.276, "none": 1.0}
    for pat, v in ns["lattice"].items():
        good = abs(round(v["p_H"], 3) - expect[pat]) < 1e-9
        ok &= good
        print(f"  {pat:5s} " + " / ".join(f"{v['p'][P]:.4f}" for P in H.POOLS) + f" -> {v['p_H']:.4f} "
              f"(7.2: {expect[pat]:.3f}) {'ok' if good else 'MISMATCH'}")
    allm = {P: True for P in H.POOLS}
    for t3, t4 in ((True, True), (False, True), (True, False), (False, False)):
        pv = H.p_value(pools, {"H3": t3, "H4": t4}, allm, determined=det)
        print(f"  target H3 {t3!s:5s} H4 {t4!s:5s}: p_H {pv['p_H']:.4f}  Q_contra {pv['Q_contra']}")
        ok &= pv["Q_contra"] == t4                      # determined H4 = fail
    ok &= ns["Q_record"] is True and abs(ns["p_H_min"] - 0.04) < 5e-4
    print("selftest", "PASS" if ok else "FAIL")
    return ok


def main(argv=None):
    ap = argparse.ArgumentParser(description="the held-out test at the target (DESIGN 7.2)")
    ap.add_argument("--attain", default=str(ATTAIN))
    ap.add_argument("--target-info")
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return 0 if selftest() else 1
    attain = Path(a.attain)
    if not attain.exists() or not FROZEN.exists():
        print(f"refusing to run: the target stage needs {ATTAIN} and the second-freeze marker {FROZEN} "
              f"(present: attain {attain.exists()}, FROZEN {FROZEN.exists()})")
        return 2
    run(attain, a.target_info, a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
