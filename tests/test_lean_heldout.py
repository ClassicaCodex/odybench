"""
Tests of odybench/lean/heldout.py (agent L2; LEAN.md, DESIGN 7.1-7.3, I15(a)).

    cd C:\\Projects\\odybench && py tests/test_lean_heldout.py [--fast]

(no pytest on this machine; the file is also collectable by pytest.)

1. The rank test on synthetic pools: the design-stage lattice of 7.2,
   cell by cell against results/design-revision-v8/verdict_trace.py's
   independent p_pool; ties against the target; membership; Q_record and
   Q_contra from hand-built disclosure tables; exactness under
   exchangeability by simulation; Q_exch's six tests; the mask.
2. The predicates on real dates far from the target: every spring new moon of
   -700..-600 (Day 0 its UT+2 civil date).  H3 and H4 against an independent
   scalar reference written here from 7.1's text: the Sun's and the
   planet's altitude from ephem's topocentric apparent RA/Dec of date by
   spherical trigonometry (not skyfield's altaz), rises by brentq, the
   conjunction from skyfield's own ecliptic_latlon(epoch='date') (IAU
   obliquity, not the module's Vondrak one) by brentq, and the separation by
   the spherical cosine formula.  Flags must agree outside I15's tie bands
   (0.1 d, 0.1 deg of Sun altitude, 0.1 deg of separation); margins to
   0.01 deg, 0.001 d and 0.001 deg.  H1, H2 and H5 against the same reference
   on a few dates.
No predicate is evaluated within years of the target; the target guard is
only checked to raise.
"""
import importlib.util
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from odybench import calendar as cal  # noqa: E402
from odybench import ephem as E  # noqa: E402
from odybench.lean import heldout as H  # noqa: E402

DESIGN_POOLS = {"P_BM": (76, 14, 1, 1), "P_MWRA": (43, 8, 1, 0),
                "P_BM_E": (49, 9, 1, 1), "P_MWRA_E": (28, 6, 1, 0)}       # n; H3 only, H4 only, both
DESIGN_LATTICE = {"both": (0.026, 0.023, 0.040, 0.034, 0.040),
                  "h4": (0.039, 0.045, 0.060, 0.069, 0.069),
                  "h3": (0.221, 0.227, 0.240, 0.276, 0.276),
                  "none": (1.0, 1.0, 1.0, 1.0, 1.0)}
FAST = "--fast" in sys.argv


# ------------------------------------------------------------- synthetic

def _pool_from_counts(n, a3, a4, ab, y_lo, y_hi, seed=0):
    """A pool with the given counts; Day 0 dates are arbitrary 1 Apr JDNs
    spread over [y_lo, y_hi], the passes shuffled over them (no sky is
    evaluated)."""
    h3 = np.array([True] * ab + [True] * a3 + [False] * a4 + [False] * (n - ab - a3 - a4))
    h4 = np.array([True] * ab + [False] * a3 + [True] * a4 + [False] * (n - ab - a3 - a4))
    perm = np.random.default_rng(seed).permutation(n)
    years = np.round(np.linspace(y_lo, y_hi, n)).astype(int)
    jdn = np.array([cal.jdn_from_julian(int(y), 4, 1) for y in years])
    return H.structured(jdn, H3=h3[perm], H4=h4[perm])


def design_pools():
    out = {}
    for k, (P, (n, a3, a4, ab)) in enumerate(DESIGN_POOLS.items()):
        lo, hi = (-1870, -480) if P.endswith("_E") else (-1990, 190)
        out[P] = _pool_from_counts(n, a3, a4, ab, lo, hi, seed=k)
    return out


def _verdict_trace():
    p = ROOT / "results" / "design-revision-v8" / "verdict_trace.py"
    spec = importlib.util.spec_from_file_location("verdict_trace_v8", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_target_jdn():
    assert H.TARGET_JDN == cal.jdn_from_julian(-1177, 4, 16) == 1291264
    assert cal.jd_from_julian(-1177, 4, 16) == 1291263.5        # DESIGN 0: JD 1291263.5 at 0 h
    assert set(H.GUARDED_JDNS) == {1291264, 1291263}


def test_guard_raises_without_evaluating():
    for j in (1291264, 1291263):
        for fn in (H.flags, H.evaluate):
            try:
                fn(np.array([cal.jdn_from_julian(-650, 4, 1), j]), "seq")
            except ValueError as e:
                assert "target" in str(e)
            else:
                raise AssertionError("the target guard did not raise")
    try:                                    # the off-by-one is refused even in the target stage
        H.flags(np.array([1291263]), "seq", allow_target=True)
    except ValueError as e:
        assert "15 Apr -1177" in str(e)
    else:
        raise AssertionError("JDN 1291263 was accepted")


def test_count_validation():
    for bad in ("sequential", "", "x"):
        try:
            H.flags(np.array([cal.jdn_from_julian(-650, 4, 1)]), bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"count {bad!r} accepted")
    try:
        H.flags(np.array([1.5]), "seq")
    except ValueError:
        pass
    else:
        raise AssertionError("a non-integer JDN was accepted")


def test_design_lattice_and_floor():
    pools = design_pools()
    ns = H.null_side(pools, determined={"H3": None, "H4": "fail"})
    for i, P in enumerate(H.POOLS):
        n, a3, a4, ab = DESIGN_POOLS[P]
        c = ns["pools"][P]
        assert (c["n"], c["h3_only"], c["h4_only"], c["both"]) == (n, a3, a4, ab), (P, c)
        assert abs(c["floor"] - (1 + ab) / (1 + n)) < 1e-15
    assert abs(ns["p_H_min"] - 0.04) < 0.0005 and ns["p_H_min_pool"] == "P_BM_E"
    assert ns["Q_attain"] is False
    for pat, ref in DESIGN_LATTICE.items():
        got = [ns["lattice"][pat]["p"][P] for P in H.POOLS] + [ns["lattice"][pat]["p_H"]]
        assert all(abs(round(g, 3) - r) < 1e-9 for g, r in zip(got, ref)), (pat, got, ref)
    assert abs(ns["lattice"]["both"]["p_H"] - ns["p_H_min"]) < 1e-15
    assert ns["Q_record"] is True                       # H4 = fail: H3 only (0.276) and neither (1)
    assert set(ns["Q_record_consistent_patterns"]) == {"h3", "none"}
    ns2 = H.null_side(pools, determined={"H3": None, "H4": None})
    assert ns2["Q_record"] is False                     # "both" reaches 0.040
    ns3 = H.null_side(pools, determined={"H3": "fail", "H4": None})
    assert ns3["Q_record"] is True                      # H4 only: 0.069
    assert abs(ns["reported"]["floor_H3_alone"]["P_BM"] - 16 / 77) < 1e-12


def test_against_verdict_trace():
    vt = _verdict_trace()
    pools = design_pools()
    for P, (n, a3, a4, ab) in DESIGN_POOLS.items():
        cnt = dict(n=n, h3=a3, h4=a4, both=ab)
        h3, h4 = pools[P]["H3"], pools[P]["H4"]
        for pat in H.PATTERNS:
            t3, t4 = pat in ("both", "h3"), pat in ("both", "h4")
            mine = H.p_pool(h3, h4, t3, t4)["p"]
            theirs = vt.p_pool(cnt, pat)
            assert mine == theirs, (P, pat, mine, theirs)
            assert H.p_pool(h3, h4, t3, t4, member=False)["p"] == 1.0
    # random pools too
    rng = np.random.default_rng(11)
    for _ in range(300):
        n = int(rng.integers(1, 60))
        h3 = rng.random(n) < rng.random()
        h4 = rng.random(n) < rng.random()
        cnt = dict(n=n, h3=int((h3 & ~h4).sum()), h4=int((h4 & ~h3).sum()), both=int((h3 & h4).sum()))
        for pat in H.PATTERNS:
            t3, t4 = pat in ("both", "h3"), pat in ("both", "h4")
            assert H.p_pool(h3, h4, t3, t4)["p"] == vt.p_pool(cnt, pat), (cnt, pat)
    assert vt.q_record(vt.NULL["pools"], vt.NULL["determined"]) is True


def test_ties_count_against_target():
    # q3 == q4 over pool + target: an H3-only target ties every H4-only member
    h3 = np.array([False, False, False, False])
    h4 = np.array([True, False, False, False])
    r = H.p_pool(h3, h4, True, False)                   # x3 = 1 (the target), x4 = 1
    assert abs(r["w3"] - r["w4"]) < 1e-15
    assert r["x"] == 1 and r["p"] == 2 / 5
    h3 = np.array([True, False, True, False, False])
    h4 = np.array([False, True, False, True, False])
    r = H.p_pool(h3, h4, True, False)                   # x3 = 3, x4 = 2: H3 is commoner
    assert r["w4"] > r["w3"] and r["x"] == 4 and r["p"] == 5 / 6
    # a target passing neither ties the whole pool
    assert H.p_pool(h3, h4, False, False)["p"] == 1.0
    # weights over pool + target: a predicate nobody else passes
    r = H.p_pool(np.zeros(9, bool), np.zeros(9, bool), True, False)
    assert abs(r["q3"] - 0.1) < 1e-15 and r["p"] == 0.1


def test_p_value_membership_and_contra():
    pools = design_pools()
    det = {"H3": None, "H4": "fail"}
    allm = {P: True for P in H.POOLS}
    r = H.p_value(pools, {"H3": True, "H4": True}, allm, determined=det)
    assert abs(r["p_H"] - 0.040) < 0.0005 and r["Q_contra"] is True and r["contra_flags"] == ["H4"]
    r = H.p_value(pools, {"H3": True, "H4": False}, allm, determined=det)
    assert abs(r["p_H"] - 0.276) < 0.0005 and r["Q_contra"] is False
    mem = dict(allm, P_MWRA=False, P_MWRA_E=False)
    r = H.p_value(pools, {"H3": True, "H4": True}, mem, determined=det)
    assert r["p"]["P_MWRA"] == 1.0 and r["p_H"] == 1.0                # S12
    try:
        H.p_value(pools, {"H3": True, "H4": True}, None, determined=det)
    except ValueError:
        pass
    else:
        raise AssertionError("membership must be an input")
    r = H.p_value(pools, {"H3": True, "H4": True, "member": allm}, determined=det)
    assert abs(r["p_H"] - 0.040) < 0.0005
    # per-pool flags (H4's count differing by pool)
    tf = {P: {"H3": True, "H4": P != "P_MWRA"} for P in H.POOLS}
    r = H.p_value(pools, tf, allm, determined=det)
    assert r["pattern"]["P_MWRA"] == "h3" and r["pattern"]["P_BM"] == "both"
    assert abs(r["p"]["P_MWRA"] - 0.227) < 0.0005
    q, d = H.q_contra({"H3": False, "H4": False}, {"H3": "pass", "H4": "fail"})
    assert q and d == ["H3"]
    assert H.load_determined() == {"H3": None, "H4": "fail"}        # the frozen table


def test_exact_under_exchangeability():
    """P(p_P <= alpha) <= alpha when target and members are i.i.d."""
    rng = np.random.default_rng(2026)
    for n, a, b in ((30, 0.2, 0.05), (45, 0.5, 0.3), (12, 0.1, 0.1)):
        sims = 6000
        ps = np.empty(sims)
        for k in range(sims):
            h3 = rng.random(n + 1) < a
            h4 = rng.random(n + 1) < b
            ps[k] = H.p_pool(h3[1:], h4[1:], h3[0], h4[0])["p"]
        for alpha in (0.05, 0.1, 0.25, 0.5):
            frac = float((ps <= alpha).mean())
            se = math.sqrt(alpha * (1 - alpha) / sims)
            assert frac <= alpha + 3.5 * se, (n, a, b, alpha, frac)


def test_q_exch_and_mask():
    pools = design_pools()
    ns = H.null_side(pools, determined={"H3": None, "H4": "fail"})
    assert ns["Q_exch_complete"] is False and ns["P10_heldout_part"] == "not computed"
    assert len(ns["Q_exch_tests"]) == 6
    # a strong drift of H3 inside the band fires Q_exch
    n = 40
    jdn = np.array([cal.jdn_from_julian(-1870 + 35 * i, 4, 1) for i in range(n)])
    years = np.array([cal.julian_from_jdn(int(j))[0] for j in jdn])
    h3 = years < -1177
    drift = dict(pools, P_BM_E=H.structured(jdn, H3=h3, H4=np.zeros(n, bool)))
    ns = H.null_side(drift, determined={"H3": None, "H4": "fail"})
    fired = [t["test"] for t in ns["Q_exch_tests"] if t["fires"]]
    assert ns["Q_exch"] is True and any("drift H3 in P_BM_E" in f for f in fired), fired
    # P10 on P_spring with an eclipse field
    m = 400
    jdn = np.array([cal.jdn_from_julian(-1990 + 5 * i, 4, 1) for i in range(m)])
    ecl = np.arange(m) % 5 == 0
    sp = H.structured(jdn, H3=ecl.copy(), H4=np.zeros(m, bool), eclipse=ecl)
    ns = H.null_side(dict(pools, P_spring=sp), determined={"H3": None, "H4": "fail"})
    assert ns["Q_exch_complete"] is True and ns["Q_exch"] is True
    sp_null = H.structured(jdn, H3=(np.arange(m) % 3 == 0), H4=np.zeros(m, bool), eclipse=ecl)
    ns = H.null_side(dict(pools, P_spring=sp_null), determined={"H3": None, "H4": "fail"})
    assert ns["Q_exch"] is False
    # the mask: a pool holding the target is refused
    bad = dict(pools)
    j = np.array([H.TARGET_JDN] + [cal.jdn_from_julian(-1500, 4, 1)])
    bad["P_BM"] = H.structured(j, H3=np.array([True, False]), H4=np.array([False, False]))
    try:
        H.null_side(bad, determined={"H3": None, "H4": "fail"})
    except ValueError:
        pass
    else:
        raise AssertionError("a pool holding the target was accepted")
    # an epoch pool must lie in the band
    bad = dict(pools)
    bad["P_MWRA_E"] = H.structured(np.array([cal.jdn_from_julian(-300, 4, 1)]), H3=np.array([True]),
                                   H4=np.array([False]))
    try:
        H.null_side(bad, determined={"H3": None, "H4": "fail"})
    except ValueError:
        pass
    else:
        raise AssertionError("an epoch pool outside -1877..-477 was accepted")



def _load_script(name):
    spec = importlib.util.spec_from_file_location(f"{name}_script", ROOT / f"{name}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_script_plumbing_without_sky():
    """heldout.py's run() on a hand-built attain.json, with the target's flags
    stubbed (no sky is evaluated: the pools carry H1, H2 and H5 too)."""
    import json
    import tempfile
    hs = _load_script("heldout")
    pools = design_pools()
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        cols = {}
        for P, a in pools.items():
            cols[P] = {"day0_jdn_ut2": a["day0_jdn_ut2"].tolist(), "year": a["year"].tolist(),
                       "H3": a["H3"].tolist(), "H4": a["H4"].tolist(),
                       "H1": [False] * len(a), "H2": [True] * len(a), "H5": (a["H3"] & ~a["H4"]).tolist(),
                       "count": ["both"] * len(a)}
        ns = H.null_side(pools)
        att = {"heldout": {"pools": cols, "null_side": {k: ns[k] for k in ("p_H_min", "Q_record", "Q_exch",
                                                                             "Q_attain")}}}
        (td / "attain.json").write_text(json.dumps(att), encoding="utf-8")
        info = {"stage": "target", "T0_pass": True,
                "heldout_target": {P: {"member": P != "P_MWRA_E", "count": "seq" if P != "P_MWRA_E" else None}
                                   for P in H.POOLS}}          # reproduce.py's shape
        (td / "t0.json").write_text(json.dumps(info), encoding="utf-8")
        stub = {"seq": {"H1": False, "H2": True, "H3": True, "H4": False, "H5": True,
                        "H3_vis_margin": -1.0, "H3_conj_offset_d": 0.5, "H3_conj_margin_d": 2.5,
                        "H4_min_sep_deg": 30.0, "H4_min_day": -6, "H5_vis_margin": -2.0,
                        "H1_night_a_h": 11.5, "H1_night_b_h": 11.3, "H2_share": 0.1}}
        hs.target_flags = lambda info: stub
        res = hs.run(td / "attain.json", td / "t0.json", td / "out")
        out = json.loads((td / "out" / "heldout.json").read_text(encoding="utf-8"))
        assert (td / "out" / "heldout.out.txt").exists()
        assert out["p"]["P_MWRA_E"] == 1.0 and out["p_H"] == 1.0          # not a member there
        assert abs(out["p"]["P_BM"] - 17 / 77) < 1e-12                       # H3 only: 0.221
        assert out["Q_contra"] is False and out["Q_record"] is True
        assert all(c["agree"] for c in out["null_side_checks"]) and len(out["null_side_checks"]) == 4
        assert out["base_rates"]["P_BM"]["source"] == "attain.json"
        assert res["pattern"]["P_BM"] == "h3"
        # refusal without target info
        try:
            hs.run(td / "attain.json", td / "missing.json", td / "out2")
        except SystemExit as e:
            assert "membership" in str(e)
        else:
            raise AssertionError("ran without the target's membership")


# ---------------------------------------------------- real dates, -700..-600

LAT, LON = H.LAT, H.LON


def spring_day0(y0=-700, y1=-600):
    out = set()
    for y in range(y0, y1 + 1):
        for c in E.new_moons(cal.jd_from_julian(y, 3, 1), cal.jd_from_julian(y, 5, 31)):
            ut = c - float(E.delta_t(E.julian_epoch(c), "smh2020")) / 86400.0
            out.add(int(cal.jdn_of_instant(ut, 2.0)))
    d = np.array(sorted(out))
    assert np.all(np.abs(d - H.TARGET_JDN) > 365 * 400)
    return d


def ref_alt(body, jd_ut, de431=False):
    """Topocentric airless altitude (deg) by spherical trigonometry from ephem's
    apparent RA/Dec of date and the Time's apparent sidereal time."""
    def go():
        t = E.time_ut(np.atleast_1d(np.asarray(jd_ut, float)), "smh2020")
        ra, de = E.radec_of_date(body, t, LAT, LON)
        ha = np.radians(np.asarray(t.gast) * 15.0 + LON - np.asarray(ra))
        phi, d = math.radians(LAT), np.radians(de)
        return np.degrees(np.arcsin(np.sin(phi) * np.sin(d) + np.cos(phi) * np.cos(d) * np.cos(ha)))
    if de431:
        with E.use_ephemeris(E.EPHEM_DIR / "de431"):
            return go()
    return go()


def ref_events(body, jdn, kind, h0, de431=False):
    from scipy.optimize import brentq
    start = jdn - 0.5 - LON / 360.0
    grid = start + np.arange(49) / 48.0
    f = ref_alt(body, grid, de431) - h0
    out = []
    for i in range(48):
        up = f[i] < 0 <= f[i + 1]
        dn = f[i] >= 0 > f[i + 1]
        if (kind == "rise" and up) or (kind == "set" and dn):
            out.append(brentq(lambda x: float(ref_alt(body, x, de431)[0]) - h0, grid[i], grid[i + 1], xtol=1e-8))
    return out


def ref_vis_margin(body, jdn, side, av):
    ev = ref_events(body, jdn, "rise" if side == "morning" else "set", H.H0_PLANET)
    return max((-av - float(ref_alt("sun", t)[0]) for t in ev), default=-np.inf)


def ref_lon_diff(jd_tt):
    t = E.time_tt(np.atleast_1d(np.asarray(jd_tt, float)), 0.0)
    lm = E.apparent("mercury", t).ecliptic_latlon(epoch="date")[1].degrees
    ls = E.apparent("sun", t).ecliptic_latlon(epoch="date")[1].degrees
    return (np.asarray(lm) - np.asarray(ls) + 180.0) % 360.0 - 180.0


def ref_h3(jdn):
    from scipy.optimize import brentq
    vis = max(ref_vis_margin("mercury", d, s, H.AV_MERCURY) for d in (jdn, jdn + 1) for s in ("morning", "evening"))
    noon = jdn - 2.0 / 24.0
    tt = lambda u: u + float(E.delta_t(E.julian_epoch(u), "smh2020")) / 86400.0
    w0, w1 = tt(noon - 3.0), tt(noon + 4.0)
    g = np.arange(w0 - 1.0, w1 + 1.0 + 1e-9, 0.5)
    d = ref_lon_diff(g)
    best = -np.inf
    for i in range(len(g) - 1):
        if d[i] * d[i + 1] < 0 and abs(d[i]) + abs(d[i + 1]) < 60:
            c = brentq(lambda x: float(ref_lon_diff(x)[0]), g[i], g[i + 1], xtol=1e-9)
            best = max(best, min(c - w0, w1 - c))
    return dict(vis=vis, conj_margin=best, H3=(vis < 0) and best >= 0)


def ref_h4(jdn, count):
    days = {"seq": range(-10, -3), "par": range(-9, -2), "both": range(-10, -2)}[count]
    jd = np.array([jdn + k - 0.5 + 3.5 / 24.0 for k in days])
    t = E.time_ut(jd, "smh2020")
    ra1, d1 = (np.radians(np.asarray(x)) for x in E.radec_of_date("venus", t))
    ra2, d2 = (np.radians(np.asarray(x)) for x in E.radec_of_date("mars", t))
    c = np.sin(d1) * np.sin(d2) + np.cos(d1) * np.cos(d2) * np.cos(ra1 - ra2)
    sep = np.degrees(np.arccos(np.clip(c, -1, 1)))
    return dict(min_sep=float(sep.min()), H4=bool(sep.min() <= 5.0))


_CACHE = {}


def _evaluated():
    if "r" not in _CACHE:
        d0 = spring_day0(-700, -600) if not FAST else spring_day0(-700, -680)
        _CACHE["d0"] = d0
        _CACHE["r"] = H.evaluate(d0, "both", predicates=("H3", "H4"))
    return _CACHE["d0"], _CACHE["r"]


def test_h3_h4_against_reference():
    d0, r = _evaluated()
    # the subset: every H3 or H4 pass, the 12 closest to a tie band, and every 15th member
    idx = set(np.nonzero(r["H3"] | r["H4"])[0])
    closeness = np.minimum.reduce([np.abs(r["H3_vis_margin"]), np.abs(np.nan_to_num(r["H3_conj_margin_d"], neginf=9)),
                                   np.abs(r["H4_min_sep_deg"] - 5.0)])
    idx |= set(np.argsort(closeness)[:12])
    idx |= set(range(0, d0.size, 15))
    idx = sorted(idx)
    tie, worst = [], dict(vis=0.0, conj=0.0, sep=0.0)
    n3 = n4 = 0
    for i in idx:
        j = int(d0[i])
        a = ref_h3(j)
        b = ref_h4(j, "both")
        in_tie3 = abs(a["vis"]) < 0.1 or (np.isfinite(a["conj_margin"]) and abs(a["conj_margin"]) < 0.1)
        in_tie4 = abs(b["min_sep"] - 5.0) < 0.1
        if in_tie3 or in_tie4:
            tie.append(j)
        if not in_tie3:
            assert bool(r["H3"][i]) == a["H3"], (j, cal.julian_from_jdn(j), r["H3_vis_margin"][i], a)
        if not in_tie4:
            assert bool(r["H4"][i]) == b["H4"], (j, r["H4_min_sep_deg"][i], b)
        if np.isfinite(a["vis"]):
            worst["vis"] = max(worst["vis"], abs(a["vis"] - r["H3_vis_margin"][i]))
        if np.isfinite(a["conj_margin"]) and np.isfinite(r["H3_conj_margin_d"][i]) and a["conj_margin"] > -0.9:
            worst["conj"] = max(worst["conj"], abs(a["conj_margin"] - r["H3_conj_margin_d"][i]))
        worst["sep"] = max(worst["sep"], abs(b["min_sep"] - r["H4_min_sep_deg"][i]))
        n3 += a["H3"]
        n4 += b["H4"]
    print(f"    reference on {len(idx)} of {d0.size} spring new moons of -700..-600: H3 passes {n3}, H4 passes {n4}; "
          f"worst |diff|: Sun altitude {worst['vis']:.4f} deg, conjunction {worst['conj'] * 86400:.2f} s, "
          f"separation {worst['sep'] * 3600:.3f} arcsec; tie-band members {tie}")
    assert worst["vis"] < 0.01 and worst["conj"] < 1e-3 and worst["sep"] < 1e-3, worst
    assert n3 >= 5 and (FAST or n4 >= 3)


def test_h4_counts():
    d0, r = _evaluated()
    i = np.nonzero(r["H4"])[0]
    if i.size == 0:
        return
    j = d0[i[:4]]
    rs = H.evaluate(j, "seq", predicates=("H4",))
    rp = H.evaluate(j, "par", predicates=("H4",))
    rb = H.evaluate(j, np.array(["both"] * j.size), predicates=("H4",))
    assert np.array_equal(rb["H4"], rs["H4"] | rp["H4"])
    for k, jj in enumerate(j):
        assert rs["H4"][k] == ref_h4(int(jj), "seq")["H4"] and rp["H4"][k] == ref_h4(int(jj), "par")["H4"]
    assert np.all(rs["H4_min_day"] <= -4) and np.all(rs["H4_min_day"] >= -10)
    assert np.all(rp["H4_min_day"] <= -3) and np.all(rp["H4_min_day"] >= -9)


def test_h1_h2_h5_against_reference():
    d0, r = _evaluated()
    # one date with H5 passing (Mars near conjunction) and one with it failing, plus one more
    r5 = H.evaluate(d0[:60], "seq", predicates=("H5",))
    pas = np.nonzero(r5["H5"])[0]
    fail = np.nonzero(~r5["H5"])[0]
    pick = [int(d0[pas[0]])] if pas.size else []
    pick += [int(d0[fail[np.argmin(np.abs(r5["H5_vis_margin"][fail]))]])]
    pick += [int(d0[3])]
    pick = np.array(sorted(set(pick)))
    got = H.evaluate(pick, "seq", predicates=("H1", "H2", "H5"))
    for k, j in enumerate(pick):
        # H5
        m = max(ref_vis_margin("mars", j + o, s, H.AV_MARS) for o in range(-34, 1) for s in ("morning", "evening"))
        assert abs(m - got["H5_vis_margin"][k]) < 0.01, (j, m, got["H5_vis_margin"][k])
        if abs(m) > 0.1:
            assert (m < 0) == bool(got["H5"][k])
        # H1: night of Day -7 (seq) and of Day -3
        for night, key in ((j - 7, "H1_night_a_h"), (j - 3, "H1_night_b_h")):
            s = ref_events("sun", night, "set", H.H0_SUN)[0]
            ri = ref_events("sun", night + 1, "rise", H.H0_SUN)[0]
            assert abs((ri - s) * 24 - got[key][k]) < 1e-4, (j, key)
        # H2: the night after Day -5, by event times instead of samples
        n = j - 5
        noon = n - 0.5 - LON / 360.0 + 0.5
        dk_a = [t for t in _ref_cross("sun", noon, H.DARK_SUN_ALT, de431=True)]
        up = _ref_cross("moon", noon, H.H0_SUN, de431=True, with_dir=True)
        share = _overlap_share(noon, dk_a, up)
        assert abs(share - got["H2_share"][k]) < 0.02, (j, share, got["H2_share"][k])
    print(f"    H1, H2, H5 on {pick.tolist()}: H5 {got['H5'].tolist()}, H2 shares {np.round(got['H2_share'], 3).tolist()}")


def _ref_cross(body, noon, h0, de431=False, with_dir=False):
    from scipy.optimize import brentq
    grid = noon + np.arange(97) / 96.0
    f = ref_alt(body, grid, de431) - h0
    out = []
    for i in range(96):
        if (f[i] < 0) != (f[i + 1] < 0):
            t = brentq(lambda x: float(ref_alt(body, x, de431)[0]) - h0, grid[i], grid[i + 1], xtol=1e-8)
            out.append((t, f[i + 1] > f[i]) if with_dir else t)
    return out


def _overlap_share(noon, dark_edges, moon_cross):
    """Dark: Sun below -12 deg between its evening and morning crossings.
    Moon up: from each upward crossing to the next downward one."""
    d0, d1 = dark_edges[0], dark_edges[-1]
    ivs, cur = [], None
    t0 = noon
    alt0 = float(ref_alt("moon", noon, True)[0]) > H.H0_SUN
    if alt0:
        cur = t0
    for t, rising in moon_cross:
        if rising:
            cur = t
        elif cur is not None:
            ivs.append((cur, t))
            cur = None
    if cur is not None:
        ivs.append((cur, noon + 1.0))
    up = sum(max(0.0, min(b, d1) - max(a, d0)) for a, b in ivs)
    return up / (d1 - d0)


if __name__ == "__main__":
    import time
    fails = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            t0 = time.time()
            try:
                fn()
                print(f"PASS {name} ({time.time() - t0:.1f} s)")
            except Exception as exc:          # noqa: BLE001
                fails += 1
                import traceback
                traceback.print_exc()
                print(f"FAIL {name}: {exc!r}")
    print("all passed" if not fails else f"{fails} failed")
    sys.exit(1 if fails else 0)
