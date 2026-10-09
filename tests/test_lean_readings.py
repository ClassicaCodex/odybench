"""
Tests of odybench/lean/readings.py and the pool logic of candidates.py
(DESIGN 4.2, 5.3, 7.2, 12.3).  Synthetic pools and hand-built rows only: no
reading is evaluated on the real sky.

    cd C:\\Projects\\odybench && py tests/test_lean_readings.py
"""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from odybench import calendar as cal  # noqa: E402
from odybench.lean import TARGET_JDN, TargetMasked  # noqa: E402
from odybench.lean import candidates as Cn  # noqa: E402
from odybench.lean import readings as Rd  # noqa: E402


def _pool(seed=5, **kw):
    return Cn.synthetic(seed=seed, **kw)


def _with_target(pool):
    """A copy of the pool whose first row is moved onto 16 Apr -1177 (masked flag kept)."""
    p = pool.subset(np.ones(len(pool), dtype=bool))
    p.rec = p.rec.copy()
    p.rec["day0_jdn_ut2"][0] = TARGET_JDN
    return p


def test_target_jdn():
    assert TARGET_JDN == cal.jdn_from_julian(-1177, 4, 16) == 1291264
    assert cal.jd_from_julian(-1177, 4, 16) == 1291263.5


def test_36_readings():
    R = Rd.READINGS
    assert len(R) == 36 and len(set(R)) == 36
    assert {r.count for r in R} == {"seq", "par"}
    assert {r.event for r in R} == {"mwra", "gwe", "station"}
    assert {r.tol for r in R} == {1.5, 2.5, 3.5}
    assert {r.vis for r in R} == {False, True}
    assert Rd.T0B == Rd.Reading("seq", "mwra", 1.5, False) and R[Rd.T0B_INDEX] == Rd.T0B
    assert len(Rd.MWRA_INDICES) == 12 and all(R[i].event == "mwra" for i in Rd.MWRA_INDICES)
    assert Rd.pinned("T0b") == Rd.T0B
    # the day counts of 4.2 / slots.json
    sl = json.loads((ROOT / "data" / "prereg" / "slots.json").read_text(encoding="utf-8"))["day_counts"]
    for cnt, key in (("seq", "sequential"), ("par", "parallel")):
        assert list(Cn.COUNTS[cnt]["c"]) == sl[key]["C"]
        assert Cn.COUNTS[cnt]["v"] == sl[key]["venus"] and Cn.COUNTS[cnt]["m"] == sl[key]["mercury"]


def test_pass_arrays_by_hand():
    """Hand-built rows: each predicate's boundary."""
    p = _pool(n_years=50, y0=-1500)
    n = len(p)
    cols = p.cols
    for k in list(cols):
        if k.startswith(("lead_", "vsun_", "msun_", "d_")):
            cols[k] = np.full(n, np.nan)
    cols["c_rel_seq"][:] = False
    cols["c_rel_par"][:] = False
    i = 0
    cols["c_rel_seq"][i] = True
    cols["lead_m5"][i] = 90.0                   # exactly 90 min passes
    cols["d_mwra_m34"][i] = 1.5                 # exactly 1.5 d passes
    cols["msun_m34"][i] = -9.99                 # not visible at AV 10
    pa = Rd.passes(p)
    on = {Rd.READINGS[j] for j in np.nonzero(pa[:, i])[0]}
    assert on == {Rd.Reading("seq", "mwra", t, False) for t in (1.5, 2.5, 3.5)}, on
    cols["msun_m34"][i] = -10.0
    pa = Rd.passes(p)
    assert pa[:, i].sum() == 6
    cols["lead_m5"][i] = 89.99
    assert Rd.passes(p)[:, i].sum() == 0
    cols["lead_m5"][i] = 95.0
    cols["d_mwra_m34"][i] = 1.5001
    on = {Rd.READINGS[j] for j in np.nonzero(Rd.passes(p)[:, i])[0]}
    assert on == {Rd.Reading("seq", "mwra", t, v) for t in (2.5, 3.5) for v in (False, True)}
    # the parallel count reads Days -4 and -33, never -5 / -34
    cols["c_rel_par"][i] = True
    assert not Rd.passes(p)[[k for k, r in enumerate(Rd.READINGS) if r.count == "par"], i].any()
    cols["lead_m4"][i] = 91.0
    cols["d_gwe_m33"][i] = 0.2
    on = {Rd.READINGS[j] for j in np.nonzero(Rd.passes(p)[:, i])[0] if Rd.READINGS[j].count == "par"}
    # Mercury's visibility on Day -33 is unknown (NaN), so only the visibility-off readings pass
    assert on == {Rd.Reading("par", "gwe", t, False) for t in (1.5, 2.5, 3.5)}, on
    m = Rd.membership(p)
    assert m["P_BM"][i] and m["bm_seq"][i] and m["bm_par"][i] and m["mwra_seq"][i] and not m["mwra_par"][i]
    assert int(m["bits"][i]) >> Rd.READINGS.index(Rd.Reading("par", "gwe", 1.5, False)) & 1


def test_nesting_and_identity_on_synthetic():
    p = _pool(seed=9)
    pa = Rd.passes(p)
    for i, r in enumerate(Rd.READINGS):
        if r.tol < 3.5:
            j = Rd.READINGS.index(r._replace(tol=Rd.TOLS[Rd.TOLS.index(r.tol) + 1]))
            assert np.all(pa[j][pa[i]])
        if r.vis:
            assert np.all(pa[Rd.READINGS.index(r._replace(vis=False))][pa[i]])
    reached = pa.any(axis=0)
    for v in ("v1", "v2", "v3", "v4", "v5"):
        assert not np.any(reached & ~Cn.slot_A(p, v)), v


def test_slot_family_by_hand():
    p = _pool(n_years=50, y0=-1500)
    n = len(p)
    for k in list(p.cols):
        if k.startswith(("lead_", "vsun_", "msun_", "d_")):
            p.cols[k] = np.full(n, np.nan)
    p.cols["c_rel_seq"][:] = False
    p.cols["c_rel_par"][:] = False
    i = 1
    p.cols["c_rel_seq"][i] = True
    p.cols["lead_m5"][i] = 30.0
    p.cols["vsun_m5"][i] = -7.0                  # AV 7 exactly
    p.cols["d_sta_m34"][i] = 5.9                 # event within 6 d, not within 4
    p.cols["msun_m34"][i] = -5.0                 # not visible
    got = {v: bool(Cn.slot_A(p, v)[i]) for v in ("v0", "v1", "v2", "v3", "v4", "v5")}
    assert got == dict(v0=False, v1=True, v2=True, v3=False, v4=False, v5=False), got
    p.cols["lead_m5"][i] = 60.0
    p.cols["msun_m34"][i] = -10.0
    got = {v: bool(Cn.slot_A(p, v)[i]) for v in ("v0", "v1", "v2", "v3", "v4", "v5")}
    assert got == dict(v0=True, v1=True, v2=True, v3=False, v4=True, v5=False), got
    # day counts are paired: Venus on the parallel day cannot complete a sequential C
    p.cols["lead_m5"][i] = np.nan
    p.cols["vsun_m5"][i] = np.nan
    p.cols["lead_m4"][i] = 100.0
    p.cols["vsun_m4"][i] = -15.0
    assert not any(Cn.slot_A(p, v)[i] for v in ("v0", "v1", "v2", "v3", "v4", "v5"))


def test_e_flags():
    p = _pool(n_years=50, y0=-1500)
    d0 = p.day0
    p.cols["eq_jdn"] = d0 - 11 - 4                # Ti-11 four days after the equinox
    assert np.all(Cn.e_flags(p, 4)) and np.all(Cn.e_flags(p, 5)) and not np.any(Cn.e_flags(p, 3))
    y = p.year
    apr1 = np.asarray(cal.jdn_from_julian(y, 4, 1))
    fixed = Cn.e_flags(p, 4, kind="fix")
    assert np.array_equal(fixed, (d0 - 11 >= apr1) & (d0 - 11 <= apr1 + 4))


def test_masked_target_raises_everywhere():
    p = _with_target(_pool())
    assert p.masked
    calls = [lambda: Rd.passes(p), lambda: Rd.survivors(p), lambda: Rd.membership(p),
             lambda: Rd.bm_reading(p), lambda: p.P_day(), lambda: p.P_spring(), lambda: p.T_A("v1"),
             lambda: Cn.slot_A(p, "v0"), lambda: Cn.e_flags(p, 4)]
    for c in calls:
        try:
            c()
        except TargetMasked:
            continue
        raise AssertionError("TargetMasked not raised")
    p.masked = False                              # the target side may evaluate it
    Rd.passes(p)


def test_synthetic_mask_removes_target_before_predicates():
    """synthetic() and build() drop 16 Apr -1177 when mask_target=True."""
    for seed in range(40):
        pu = Cn.synthetic(n_years=40, y0=-1200, seed=seed, mask_target=False)
        if np.any(pu.day0 == TARGET_JDN):
            pm = Cn.synthetic(n_years=40, y0=-1200, seed=seed, mask_target=True)
            assert not np.any(pm.day0 == TARGET_JDN) and len(pm) == len(pu) - 1
            return
    raise AssertionError("no synthetic seed placed a conjunction on 16 Apr -1177")


def test_build_masks_before_predicates_source():
    """In candidates.build the target is dropped right after Day 0 is
    computed, before daylight, C or any sky quantity (source order)."""
    src = (ROOT / "odybench" / "lean" / "candidates.py").read_text(encoding="utf-8")
    b = src.index("def build(")
    k_mask = src.index("keep &= d_ut2 != TARGET_JDN", b)
    for later in ('pool.rec["daylight"] =', "calibrate_crel(", "c_flags(pool.day0", "_sky_task, tasks"):
        assert src.index(later, b) > k_mask, later


def test_no_gregorian_datetime_in_lean_sources():
    """DESIGN 0: no Python date-time module or numpy 64-bit date-time type in
    L1's files (both are proleptic Gregorian)."""
    import re
    dt = "date" + "time"
    pat = re.compile(rf"^\s*(import\s+{dt}|from\s+{dt}\s+import)|{dt}64|astype\(\s*['\"]M8", re.M)
    mine = ["odybench/lean/__init__.py", "odybench/lean/sky.py", "odybench/lean/candidates.py",
            "odybench/lean/readings.py", "odybench/lean/reach.py", "reproduce.py", "rates.py", "attain.py",
            "tests/test_lean_sky.py", "tests/test_lean_reach.py", "tests/test_lean_readings.py"]
    hits = [f for f in mine if (ROOT / f).exists() and pat.search((ROOT / f).read_text(encoding="utf-8"))]
    assert not hits, hits


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
                print(f"FAIL {name}: {exc!r}")
    print("all passed" if not fails else f"{fails} failed")
    sys.exit(1 if fails else 0)
