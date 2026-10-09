"""
attain.py -- the null side of the lean run (LEAN.md stage 3; DESIGN 12.3, 9.1).
Agent L1.

Every pool is built with 16 Apr -1177 masked (candidates.load(mask_target=
True) removes it before any predicate is evaluated).  Computes and writes to
results/attain/attain.json (keys of DESIGN 9.1) and attain.out.txt:

  N1, N5 (part)          rates.n1, rates.n5
  n_T, n_TC, n_A(v)      the target pools (4.2), core -1748..-51
  G_BM[v] for v0..v5     G(G_BM*; T_A(v); W = 136) with the interval of 5.3
                         {value, lo, hi, n_A, k_A, lo_gamma, hi_gamma, lo_boot,
                          hi_boot, lo_boot243, hi_boot243, G_any}
  G_BM_u                 G(G_BM*; T; 136) with its interval; the identity
                         G_BM_u = (n_A(v)/n_T) G_BM(v) for v1..v5 is checked
                         (I9(c)), and reached targets outside T_A(v) counted
  reported beside        G over T_C; G on each half of the core; G of the T0b
                         reading alone and the look-elsewhere factor
  heldout                the four held-out pools P_BM, P_MWRA, P_BM_E, P_MWRA_E
                         (7.2) and P_spring (P10), each member with Day 0 (UT+2
                         JDN), year, the count(s) it passes on and the readings
                         it passes; H1-H5 from odybench.lean.heldout.flags (L2)
                         and null_side() (p_H_min, x_max, n, Q_attain, Q_record,
                         Q_exch ...), copied to flat keys
  almagest               odybench.lean.almagest.run() (L3), if present
  checks                 the second implementation (LEAN.md): the T0b
                         reading's survivor set against
                         results/critique-design-r2/check_gbm_full.rows.json,
                         and G over that file's own T_A

It refuses a real run unless the git tag prereg-1 exists (override
--no-freeze-check, for the integrator).  It never reads the target.

  py attain.py --run
  py attain.py --selftest      synthetic pool, synthetic held-out flags
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import numpy as np  # noqa: E402

from odybench import calendar as cal  # noqa: E402
from odybench.lean import TARGET_JDN, TargetMasked  # noqa: E402
from odybench.lean import candidates as Cn  # noqa: E402
from odybench.lean import reach as Rc  # noqa: E402
from odybench.lean import readings as Rd  # noqa: E402
import rates  # noqa: E402

OUT = ROOT / "results" / "attain"
SLOTS = ("v0", "v1", "v2", "v3", "v4", "v5")
W136 = 136 * Rc.YEAR_D
CHECK_GBM = ROOT / "results" / "critique-design-r2" / "check_gbm_full.rows.json"
HELD_POOLS = ("P_BM", "P_MWRA", "P_BM_E", "P_MWRA_E")


def _seeds():
    return json.loads((ROOT / "data" / "prereg" / "seeds.json").read_text(encoding="utf-8"))["purposes"]


def git_state():
    def g(*a):
        try:
            return subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True, timeout=20).stdout.strip()
        except Exception:               # noqa: BLE001
            return ""
    return dict(commit=g("rev-parse", "HEAD"), tree=g("rev-parse", "HEAD^{tree}"),
                dirty=bool(g("status", "--porcelain")), tags=g("tag", "--points-at", "HEAD").split())


def freeze_tag_exists(tag):
    try:
        out = subprocess.run(["git", "-C", str(ROOT), "tag", "-l", tag], capture_output=True, text=True,
                             timeout=20).stdout
        return tag in out.split()
    except Exception:                   # noqa: BLE001
        return False


# ------------------------------------------------------------------- G

def g_stats(pool, surv, seeds, core=Cn.CORE):
    """G_BM(v) for v0..v5, G_BM_u, and what is reported beside them."""
    pool.guard("G")
    T = pool.T(core)
    rT = Rc.reach(pool.jd_tt[T], surv, W136)
    yT = pool.year[T]
    out = dict(n_T=int(T.sum()), n_TC=int(pool.T_C(core).sum()))
    gu = Rc.G(rT, yT, core, pool="T", seeds=seeds)
    out["G_BM_u"] = dict(gu, n_T=gu["n"])
    reached_T = np.zeros(len(pool), dtype=bool)
    reached_T[np.nonzero(T)[0][rT > 0]] = True
    G_BM, n_A, ident = {}, {}, {}
    for v in SLOTS:
        ta = pool.T_A(v, core)
        rv = Rc.reach(pool.jd_tt[ta], surv, W136)
        g = Rc.G(rv, pool.year[ta], core, pool="T_A", slot=v, seeds=seeds)
        G_BM[v] = dict(value=g["value"], lo=g["lo"], hi=g["hi"], n_A=g["n"], k_A=g["k"],
                       lo_gamma=g["lo_gamma"], hi_gamma=g["hi_gamma"], lo_boot=g["lo_boot"], hi_boot=g["hi_boot"],
                       lo_boot243=g["lo_boot243"], hi_boot243=g["hi_boot243"], G_any=g["G_any"])
        n_A[v] = g["n"]
        outside = int(np.sum(reached_T & ~ta))
        scaled = (g["n"] / out["n_T"]) * g["value"] if out["n_T"] else float("nan")
        ident[v] = dict(reached_outside_T_A=outside, G_BM_u_from_v=scaled,
                        abs_diff=abs(scaled - gu["value"]),
                        holds=(outside == 0 and abs(scaled - gu["value"]) < 1e-12) if v != "v0" else None)
        # halves of the core (stationarity, reported)
        mid = (core[0] + core[1]) // 2
        halves = {}
        for lab, (a, b) in (("first", (core[0], mid)), ("second", (mid + 1, core[1]))):
            sel = (pool.year[ta] >= a) & (pool.year[ta] <= b)
            y, lo, hi = Rc.gamma_interval(rv[sel])
            halves[lab] = dict(years=[a, b], value=y, lo_gamma=lo, hi_gamma=hi, n=int(sel.sum()),
                               k=int(np.sum(rv[sel] > 0)))
        G_BM[v]["halves_reported"] = halves
    out["G_BM"] = G_BM
    out["n_A"] = n_A
    out["identity_I9c"] = ident
    # reported beside: G over T_C, the T0b reading alone, the look-elsewhere factor
    tc = pool.T_C(core)
    rc = Rc.reach(pool.jd_tt[tc], surv, W136)
    y, lo, hi = Rc.gamma_interval(rc)
    out["G_T_C_reported"] = dict(value=y, lo_gamma=lo, hi_gamma=hi, n=int(tc.sum()), k=int(np.sum(rc > 0)))
    t0b = [surv[Rd.T0B_INDEX]]
    lef = {}
    for v in SLOTS:
        ta = pool.T_A(v, core)
        r0 = Rc.reach(pool.jd_tt[ta], t0b, W136)
        p_u = float(r0.mean()) if r0.size else float("nan")
        lef[v] = dict(p_fix_unique=p_u, G_BM=G_BM[v]["value"],
                      factor=(G_BM[v]["value"] / p_u) if p_u > 0 else None)
    out["look_elsewhere_reported"] = lef
    return out


# ------------------------------------------------------------- held-out

def nasa_eclipse_jd():
    """JD (TD) of greatest eclipse of every solar eclipse in NASA's Five
    Millennium Canon elements (data/jsex/SE*.js), -1999..+300."""
    import re
    head = re.compile(r"^//\s*(-?\d+)\s+(\d+)\s+(\d+)\s*$")
    out = []
    for p in sorted((ROOT / "data" / "jsex").glob("SE*.js")):
        lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
        for i, ln in enumerate(lines):
            if head.match(ln.strip()) and i + 1 < len(lines):
                try:
                    out.append(float(lines[i + 1].split(",")[0]))
                except ValueError:
                    pass
    return np.array(sorted(out))


def _count_str(s, p):
    return np.where(s & p, "both", np.where(s, "seq", np.where(p, "par", "")))


def heldout_pools(pool, mem):
    """Members of the four held-out pools and P_spring (no flags yet)."""
    pool.guard("heldout pools")
    bg = pool.in_years(*Cn.BACKGROUND)
    band = pool.in_years(*Cn.EPOCH_BAND)
    sel = {"P_BM": mem["P_BM"] & bg, "P_MWRA": mem["P_MWRA"] & bg}
    sel["P_BM_E"] = sel["P_BM"] & band
    sel["P_MWRA_E"] = sel["P_MWRA"] & band
    cnt = {"P_BM": _count_str(mem["bm_seq"], mem["bm_par"]),
           "P_MWRA": _count_str(mem["mwra_seq"], mem["mwra_par"])}
    cnt["P_BM_E"], cnt["P_MWRA_E"] = cnt["P_BM"], cnt["P_MWRA"]
    sp = pool.P_spring() & bg
    sel["P_spring"] = sp
    cnt["P_spring"] = _count_str(pool.C("seq"), pool.C("par"))
    out = {}
    for P, m in sel.items():
        idx = np.nonzero(m)[0]
        bits = mem["bits"][idx]
        out[P] = dict(idx=idx, day0_jdn_ut2=pool.day0[idx].astype(np.int64), year=pool.year[idx].astype(np.int64),
                      jd_tt=pool.jd_tt[idx], count=cnt[P][idx],
                      readings=[[Rd.READINGS[i].key for i in range(36) if (int(b) >> i) & 1] for b in bits])
    return out


def add_flags(hp, flags_fn, eclipse_jd=None):
    """Attach H1-H5 (H3, H4 only for P_spring) from flags_fn(day0, count,
    allow_target=False, predicates=...)."""
    for P, d in hp.items():
        preds = ("H3", "H4") if P == "P_spring" else ("H1", "H2", "H3", "H4", "H5")
        if d["day0_jdn_ut2"].size == 0:
            for h in preds:
                d[h] = np.zeros(0, dtype=bool)
            continue
        try:
            f = flags_fn(d["day0_jdn_ut2"], d["count"], allow_target=False, predicates=preds)
        except TypeError:
            f = flags_fn(d["day0_jdn_ut2"], d["count"], allow_target=False)
        for h in preds:
            d[h] = np.asarray(f[h], dtype=bool)
        if P == "P_spring" and eclipse_jd is not None:
            k = np.searchsorted(eclipse_jd, d["jd_tt"])
            lo = eclipse_jd[np.clip(k - 1, 0, eclipse_jd.size - 1)]
            hi = eclipse_jd[np.clip(k, 0, eclipse_jd.size - 1)]
            d["eclipse"] = (np.abs(d["jd_tt"] - lo) < 1.0) | (np.abs(hi - d["jd_tt"]) < 1.0)
    return hp


def structured(d):
    fields = [("day0_jdn_ut2", "i8"), ("year", "i8"), ("jd_tt", "f8"), ("count", "U4")]
    for h in ("H1", "H2", "H3", "H4", "H5", "eclipse"):
        if h in d:
            fields.append((h, "?"))
    a = np.zeros(d["day0_jdn_ut2"].size, dtype=fields)
    for f, _ in fields:
        a[f] = d[f]
    return a


def heldout_side(pool, mem, H=None, flags_fn=None, null_fn=None, eclipse_jd=None):
    """Build the pools, attach flags, call L2's null_side."""
    hp = heldout_pools(pool, mem)
    if H is not None:
        flags_fn = flags_fn or H.flags
        null_fn = null_fn or H.null_side
    if flags_fn is None:
        return hp, dict(note="odybench.lean.heldout not available: flags and null side not computed")
    add_flags(hp, flags_fn, eclipse_jd)
    arrays = {P: structured(d) for P, d in hp.items()}
    ns = null_fn(arrays) if null_fn is not None else dict(note="null_side not available")
    return hp, ns


# ------------------------------------------------ second implementation

def compare_check_gbm(pool, pa, surv, our_G_v1, path=CHECK_GBM, core=Cn.CORE):
    """LEAN.md's second implementation: check_gbm.py's rows (DE441
    conjunctions, 3-minute rise grid, declination-based MWRA; its stated
    approximations), with 16 Apr -1177 masked here too.  Compares the T0b
    reading's survivor sets (Day-0 dates) and G over its own T_A (its slot is
    v1's) with this bench's G_BM(v1)."""
    if not path.exists():
        return dict(note=f"{path.name} not found")
    rows = [r for r in json.loads(path.read_text(encoding="utf-8")) if int(r["jdn"]) != TARGET_JDN]
    f = lambda k: np.array([r[k] for r in rows])  # noqa: E731
    jdn, jt, yy, day = f("jdn"), f("jt"), f("y"), f("day")
    cs, cp = f("cs"), f("cp")
    dc = {"seq": (cs, -5, -34), "par": (cp, -4, -33)}
    ev = {"mwra": "mwra", "gwe": "gwe", "station": "station"}
    their = []
    for r in Rd.READINGS:
        c, vd, md = dc[r.count]
        p = c & (f(f"lead{vd}") >= 90.0) & (f(f"d_{ev[r.event]}{md}") <= r.tol)
        if r.vis:
            p = p & f(f"mvis{md}")
        their.append(p)
    their = np.vstack(their)
    bg = (yy >= Cn.BACKGROUND[0]) & (yy <= Cn.BACKGROUND[1])
    ours_t0b = set(int(x) for x in pool.day0[pa[Rd.T0B_INDEX] & pool.in_years(*Cn.BACKGROUND)])
    theirs_t0b = set(int(x) for x in jdn[their[Rd.T0B_INDEX] & bg])

    def lab(j):
        y, m, d = cal.julian_from_jdn(int(j))
        return f"{y}-{m:02d}-{d:02d}"
    only_ours = sorted(ours_t0b - theirs_t0b)
    only_theirs = sorted(theirs_t0b - ours_t0b)
    detail = []
    for j in only_ours + only_theirs:
        i = np.nonzero(pool.day0 == j)[0]
        k = np.nonzero(jdn == j)[0]
        detail.append(dict(day0=lab(j),
                           ours=(dict(C=bool(pool.cols["c_rel_seq"][i[0]]), lead=float(pool.cols["lead_m5"][i[0]]),
                                      d_mwra=float(pool.cols["d_mwra_m34"][i[0]])) if i.size else None),
                           theirs=(dict(C=bool(cs[k[0]]), lead=float(rows[k[0]]["lead-5"]),
                                        d_mwra=float(rows[k[0]]["d_mwra-34"])) if k.size else None)))
    # G over their own T_A (v1-like), with this bench's reach code and their survivors
    slotA = np.zeros(len(rows), dtype=bool)
    for cnt, (c, vd, md) in dc.items():
        merc = (f(f"d_mwra{md}") <= 6.0) | (f(f"d_gwe{md}") <= 6.0) | (f(f"d_station{md}") <= 6.0)
        slotA |= c & f(f"vslot{vd}") & (merc | f(f"mvis{md}"))
    core_m = (yy >= core[0]) & (yy <= core[1])
    ta = day & slotA & core_m
    their_surv = [np.sort(jt[p & bg]) for p in their]
    rv = Rc.reach(jt[ta], their_surv, W136)
    g, lo, hi = Rc.gamma_interval(rv)
    return dict(T0b_survivor_sets_equal=(ours_t0b == theirs_t0b), n_ours=len(ours_t0b), n_theirs=len(theirs_t0b),
                only_ours=[lab(j) for j in only_ours], only_theirs=[lab(j) for j in only_theirs], detail=detail,
                G_check_v1=dict(value=g, lo_gamma=lo, hi_gamma=hi, n_A=int(ta.sum()), k_A=int(np.sum(rv > 0))),
                G_bench_v1=our_G_v1, G_diff=abs(g - our_G_v1),
                needs_explanation=bool(abs(g - our_G_v1) > 0.01),
                note="check_gbm's approximations: 3-min rise grid, declination-based 3-point MWRA vertex, "
                     "DE441 conjunctions; its MWRA requires Mercury west of the Sun, as this bench's G_BM* readings do")


# --------------------------------------------------------------- run

def run(pool, H=None, A=None, flags_fn=None, null_fn=None, eclipse_jd=None, compare=True, write=True,
        n_perm=10000, out_dir=OUT):
    t0 = time.time()
    if not pool.masked:
        raise TargetMasked("attain.py must run on the masked pool")
    pool.guard("attain")
    sd = _seeds()
    seeds = (sd["G_bootstrap"]["seeds"]["block_136"], sd["G_bootstrap"]["seeds"]["block_243"])
    pa = Rd.passes(pool)
    surv = Rd.survivors(pool, pass_array=pa)
    mem = Rd.membership(pool, pa)
    res = dict(stage="null", masked=True, target_masked="16 Apr -1177 (JDN 1291264) removed before any predicate")
    res["pool"] = dict(n_P_all=len(pool), n_P_day=int(pool.P_day().sum()), n_P_spring=int(pool.P_spring().sum()),
                       meta=pool.meta)
    res["N1"] = rates.n1(pool, n_perm=n_perm)
    res["N5"] = rates.n5(pool, pa)
    res.update(g_stats(pool, surv, seeds))
    hp, ns = heldout_side(pool, mem, H, flags_fn, null_fn, eclipse_jd)
    res["heldout"] = dict(pools={P: {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in d.items()
                                     if k != "idx"} for P, d in hp.items()},
                          n={P: int(d["day0_jdn_ut2"].size) for P, d in hp.items()},
                          null_side=ns)
    for k in ("p_H_min", "Q_attain", "Q_record", "Q_exch", "x_max", "lattice"):
        if isinstance(ns, dict) and k in ns:
            res[k] = ns[k]
    if A is not None:
        try:
            alm = _jsonable(A.run())
            res["almagest"] = alm
            for k in ("seen_ALM_SL", "seen_ALM_SL_side", "rec_ALM_BM", "N_narrow_3b", "held_ALM"):
                if isinstance(alm, dict) and k in alm:
                    res[k] = alm[k]
        except Exception as exc:        # noqa: BLE001
            res["almagest"] = dict(error=repr(exc))
    else:
        res["almagest"] = dict(note="odybench.lean.almagest not present: gate 3b not run here")
    if compare:
        res["checks"] = dict(second_implementation=compare_check_gbm(pool, pa, surv, res["G_BM"]["v1"]["value"]))
    res["runtime_s"] = round(time.time() - t0, 1)
    res["code_sha256"] = Cn.code_hash()
    h = hashlib.sha256()
    for p in ("attain.py", "rates.py", "odybench/lean/readings.py", "odybench/lean/reach.py"):
        h.update((ROOT / p).read_bytes())
    res["scripts_sha256"] = h.hexdigest()
    res["git"] = git_state()
    if write:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "attain.json").write_text(json.dumps(res, indent=1, ensure_ascii=False, default=_js),
                                            encoding="utf-8")
        (out_dir / "attain.out.txt").write_text(summary(res), encoding="utf-8")
    return res


def summary(res):
    L = ["attain.py -- the null side (16 Apr -1177 masked)", ""]
    p = res["pool"]
    L.append(f"P_all {p['n_P_all']}, P_day {p['n_P_day']}, P_spring {p['n_P_spring']}; n_T {res['n_T']}, n_TC {res['n_TC']}")
    n1 = res["N1"]["C_rel"]
    L.append(f"N1: lambda(NCVM) {n1['NCVM']['per_century']:.3f}/cy [{n1['NCVM']['lo']:.3f}, {n1['NCVM']['hi']:.3f}] "
             f"(k {n1['NCVM']['k']}); NCVME n=4 {n1['NCVME_n4']['per_century']:.3f}/cy (k {n1['NCVME_n4']['k']})")
    L.append(f"    p_fix|C {res['N1']['p_fix_given_C']['value']:.4f}; p_fix {res['N1']['p_fix']['value']:.5f}; "
             f"V-M ratio {res['N1']['VM_dependence']['ratio']:.2f} (p_upper {res['N1']['VM_dependence']['p_upper']:.3f})")
    for v in SLOTS:
        g = res["G_BM"][v]
        L.append(f"G_BM({v}) {g['value']:.4f} [{g['lo']:.4f}, {g['hi']:.4f}]  n_A {g['n_A']}, k_A {g['k_A']}  "
                 f"(gamma [{g['lo_gamma']:.4f}, {g['hi_gamma']:.4f}], block136 [{g['lo_boot']:.4f}, {g['hi_boot']:.4f}])")
    gu = res["G_BM_u"]
    L.append(f"G_BM_u {gu['value']:.5f} [{gu['lo']:.5f}, {gu['hi']:.5f}]  n_T {gu['n_T']}, k {gu['k']}")
    L.append("identity (I9(c)): " + ", ".join(f"{v}: outside {d['reached_outside_T_A']}" for v, d in res["identity_I9c"].items()))
    L.append("held-out pools: " + ", ".join(f"{P} {n}" for P, n in res["heldout"]["n"].items()))
    for k in ("p_H_min", "Q_attain", "Q_record", "Q_exch"):
        if k in res:
            L.append(f"{k}: {res[k]}")
    if "checks" in res:
        c = res["checks"]["second_implementation"]
        L.append(f"second implementation: {json.dumps({k: c.get(k) for k in ('T0b_survivor_sets_equal', 'only_ours', 'only_theirs', 'G_diff', 'needs_explanation')}, default=_js)}")
    L.append(f"runtime {res['runtime_s']} s")
    return "\n".join(L) + "\n"


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


def _jsonable(o):
    """Make another module's result JSON-safe (string keys, lists for tuples/sets, numpy scalars)."""
    if isinstance(o, dict):
        return {(k if isinstance(k, str) else (":".join(map(str, k)) if isinstance(k, tuple) else str(k))):
                _jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple, set)):
        return [_jsonable(v) for v in o]
    if isinstance(o, np.ndarray):
        return _jsonable(o.tolist())
    if isinstance(o, (np.integer, np.floating, np.bool_)):
        return o.item()
    if isinstance(o, (str, int, float, bool)) or o is None:
        return o
    return repr(o)


def _import(name):
    try:
        return __import__(f"odybench.lean.{name}", fromlist=[name])
    except ImportError:
        return None


# ------------------------------------------------------------ selftest

def selftest():
    pool = Cn.synthetic(n_years=2200, y0=-1999, seed=21)
    rng = np.random.default_rng(4)

    def fake_flags(day0, count, allow_target=False, predicates=("H1", "H2", "H3", "H4", "H5")):
        day0 = np.asarray(day0)
        if not allow_target and np.any(day0 == TARGET_JDN):
            raise ValueError("target")
        return {h: rng.random(day0.size) < (0.2 if h != "H4" else 0.05) for h in predicates}
    H = _import("heldout")
    null_fn = H.null_side if (H is not None and hasattr(H, "null_side")) else (lambda pools: dict(note="stub"))
    ecl = np.sort(pool.jd_tt[rng.random(len(pool)) < 0.03])
    class FakeAlmagest:                         # the shape of L3's result: nested, tuple keys, numpy values
        @staticmethod
        def run():
            return {"seen_ALM_SL": {("bf", "fine"): np.int64(9)}, "rec_ALM_BM": np.int64(4), "x": {1, 2}}
    res = run(pool, A=FakeAlmagest, flags_fn=fake_flags, null_fn=null_fn, eclipse_jd=ecl, compare=False,
              write=False, n_perm=200)
    assert res["rec_ALM_BM"] == 4 and res["seen_ALM_SL"] == {"bf:fine": 9}, res["almagest"]
    for v in ("v1", "v2", "v3", "v4", "v5"):
        assert res["identity_I9c"][v]["holds"], (v, res["identity_I9c"][v])
    for v in SLOTS:
        g = res["G_BM"][v]
        assert g["lo"] <= g["value"] <= g["hi"]
        assert g["lo"] == min(g["lo_gamma"], g["lo_boot"]) and g["hi"] == max(g["hi_gamma"], g["hi_boot"])
    hp = res["heldout"]["pools"]
    assert set(HELD_POOLS) <= set(hp)
    assert all(-1877 <= y <= -477 for y in hp["P_BM_E"]["year"])
    assert set(hp["P_MWRA"]["day0_jdn_ut2"]) <= set(hp["P_BM"]["day0_jdn_ut2"])
    assert all(c in ("seq", "par", "both") for c in hp["P_BM"]["count"])
    assert all(len(r) >= 1 for r in hp["P_BM"]["readings"])
    json.dumps(res, default=_js)
    # the second-implementation comparison, fed this pool in check_gbm's row format: it must agree exactly
    import tempfile
    sk = pool.cols["sky"] & (pool.cols["c_rel_seq"] | pool.cols["c_rel_par"])
    rows = []
    for i in np.nonzero(sk)[0]:
        c = pool.cols
        row = dict(jt=float(pool.jd_tt[i]), jdn=int(pool.day0[i]), y=int(pool.year[i]),
                   day=bool(pool.rec["daylight"][i]), cs=bool(c["c_rel_seq"][i]), cp=bool(c["c_rel_par"][i]))
        for o in (5, 4):
            row[f"lead-{o}"] = float(c[f"lead_m{o}"][i])
            row[f"vslot-{o}"] = bool(c[f"lead_m{o}"][i] > 0 and c[f"vsun_m{o}"][i] <= -7.0)
        for o in (34, 33):
            row[f"mvis-{o}"] = bool(c[f"msun_m{o}"][i] <= -10.0)
            row[f"mrise-{o}"] = 0.0
            for a, b in (("mwra", "d_mwra"), ("gwe", "d_gwe"), ("station", "d_sta")):
                row[f"d_{a}-{o}"] = float(c[f"{b}_m{o}"][i])
        rows.append(row)
    with tempfile.TemporaryDirectory() as td:
        fp = Path(td) / "rows.json"
        fp.write_text(json.dumps(rows), encoding="utf-8")
        pa = Rd.passes(pool)
        cmp = compare_check_gbm(pool, pa, Rd.survivors(pool, pass_array=pa), res["G_BM"]["v1"]["value"], path=fp)
    assert cmp["T0b_survivor_sets_equal"] and cmp["n_ours"] > 0, cmp
    assert cmp["G_diff"] < 1e-12 and cmp["G_check_v1"]["n_A"] == res["G_BM"]["v1"]["n_A"], cmp
    # NASA's elements: every solar eclipse -1999..+300 is read (the Canon holds about 2.38 a year)
    e = nasa_eclipse_jd()
    assert 5400 < e.size < 5600 and np.diff(e).min() > 29 and np.diff(e).max() < 200, e.size
    # the masked guard: a pool holding the target refuses to run
    pu = Cn.synthetic(n_years=2200, y0=-1999, seed=21, mask_target=False)
    if np.any(pu.day0 == TARGET_JDN):
        pu.masked = True
        try:
            run(pu, flags_fn=fake_flags, null_fn=null_fn, compare=False, write=False, n_perm=10)
        except TargetMasked:
            pass
        else:
            raise AssertionError("TargetMasked not raised")
    print(summary(res))
    print(f"[attain selftest] null_side from {'L2 heldout' if H is not None else 'stub'}; PASS")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--no-freeze-check", action="store_true")
    ap.add_argument("--rebuild", action="store_true", help="rebuild the masked pool cache")
    a = ap.parse_args(argv)
    if a.selftest:
        selftest()
    elif a.run:
        if not (a.no_freeze_check or freeze_tag_exists("prereg-1")):
            sys.exit("attain.py is the null-side stage: run it after the first freeze (git tag prereg-1), "
                     "or pass --no-freeze-check")
        pool = Cn.load(mask_target=True, rebuild=a.rebuild)
        H = _import("heldout")
        A = _import("almagest")
        res = run(pool, H=H, A=A, eclipse_jd=nasa_eclipse_jd())
        print(summary(res))
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
