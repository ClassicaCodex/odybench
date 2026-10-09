"""
Tests of odybench/lean/sky.py and the conjunction finder of candidates.py
(DESIGN 0, 3.2, 4.3, 4.5; LEAN.md instrument check I6(a)).

    cd C:\\Projects\\odybench && py tests/test_lean_sky.py

Real-sky checks run only on dates away from the target: no quantity of the
sky of 7 Mar - 18 Apr -1177 is computed here (the S2 rows are used without
the 1178 BC row, and the C_rel calibration returns only h_A and h_P, which
DESIGN 2.9 publishes).  About 2 minutes.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from odybench import calendar as cal, ephem  # noqa: E402
from odybench.lean import sky  # noqa: E402
from odybench.lean import candidates as Cn  # noqa: E402

MON = {m: i + 1 for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split())}
MN = {v: k for k, v in MON.items()}
FORBIDDEN = (cal.jdn_from_julian(-1177, 3, 7), cal.jdn_from_julian(-1177, 4, 18))


def _s2_rows():
    with open(ROOT / "data" / "bm2008-a" / "table_s2.tsv", encoding="utf-8") as f:
        L = [ln.rstrip("\n") for ln in f if ln.strip() and not ln.startswith("#")]
    h = L[0].split("\t")
    rows = []
    for ln in L[1:]:
        c = ln.split("\t")
        c += [""] * (len(h) - len(c))
        rows.append(dict(zip(h, c)))
    return [r for r in rows if r["year"] != "1178"]


def _jdn(ya, s):
    d, m = s.split("-")
    return cal.jdn_from_julian(ya, MON[m], int(d))


def _far(days):
    d = np.asarray(days)
    assert not np.any((d >= FORBIDDEN[0] - 70) & (d <= FORBIDDEN[1] + 10)), "test touches the target's sky"
    return d


def test_sites_and_constants():
    assert sky.site("ithaki")[:2] == (38.37, 20.72) and sky.site("bm")[:2] == (38.4, 20.7)
    assert sky.H0_SUN == -0.8333 and sky.H0_PLANET == -0.5667 and sky.BM_CLOCK_DT == 27602.7
    assert sky.DE431_SPLIT_JD == 1721425.5 and sky.TOL_S["mercury"] == 0.1


def test_rise_precision_and_day():
    """Every rising brackets h0 within its tolerance, and is the first rising of
    the window found independently on a 1-min grid."""
    rng = np.random.default_rng(1)
    lat, lon, _ = sky.site("ithaki")
    years = (-1900, -1600, -900, -400, 0, 150)
    days = _far(np.array([cal.jdn_from_julian(y, int(m), int(d)) for y in years
                          for m, d in zip(rng.integers(1, 6, 4), rng.integers(1, 28, 4))]))
    for body, win in (("sun", (0, 14)), ("venus", (0, 14)), ("mercury", (0, 14)), ("mars", (0, 24))):
        r = sky.crossing(body, days, lat, lon, window_h=win)
        tol = sky.TOL_S.get(body, 1.0) / 86400.0
        ok = np.isfinite(r["jd_ut"])
        h0 = sky.h0_of(body)
        a = sky.altaz((body,), r["jd_ut"][ok] - tol, lat, lon)[body][0]
        b = sky.altaz((body,), r["jd_ut"][ok] + tol, lat, lon)[body][0]
        assert np.all(a < h0) and np.all(b >= h0), body
        assert np.nanmax(r["bracket_s"]) <= sky.TOL_S.get(body, 1.0)
        # independent: first upward crossing on a 1-minute grid over the window
        g = sky.day_start_ut(days, sky.UT2)[:, None] + (win[0] * 60 + np.arange(int((win[1] - win[0]) * 60) + 1))[None, :] / 1440.0
        alt = sky.altaz((body,), g.ravel(), lat, lon)[body][0].reshape(g.shape)
        c = (alt[:, :-1] < h0) & (alt[:, 1:] >= h0)
        has = c.any(axis=1)
        assert np.array_equal(has, ok), body
        first = g[np.arange(len(days)), np.argmax(c, axis=1)]
        assert np.all(np.abs(r["jd_ut"][ok] - first[ok]) <= 1.0 / 1440.0 + 1e-9), body


def test_A2_venus_on_s2_without_1178():
    rows = _s2_rows()
    lat, lon, _ = sky.site("bm")
    ti = np.array([_jdn(1 - int(r["year"]), r["Ti"]) for r in rows])
    lv = sky.rise_lead(_far(ti - 5), lat, lon, body="venus", dt=sky.BM_CLOCK_DT)
    vpass = {int(r["year"]) for r, ld in zip(rows, lv["lead_min"]) if ld >= 90.0}
    s2v = {int(r["year"]) for r in rows if r["c_diff"] == "O"}
    assert vpass == s2v and len(s2v) == 24

    def secs(t):
        p = list(map(int, t.split(":"))) + [0]
        return p[0] * 3600 + p[1] * 60 + p[2]
    dl = np.array([secs(r["diff"]) / 60 - ld for r, ld in zip(rows, lv["lead_min"]) if r["diff"]])
    off = np.array([secs(r["sunrise"]) / 60 - cal.julian_from_jd(s, 2.0)[3] * 60
                    for r, s in zip(rows, lv["sun_rise"]) if r["sunrise"]])
    assert dl.std() <= 3.0 and abs(off.mean()) < 0.5 and off.std() < 2.0, (dl.std(), off.mean(), off.std())
    print(f"    S2 lead - DE441 lead: sd {dl.std():.2f} min; S2 sunrise - DE441 (UT+2): {off.mean():+.2f} "
          f"sd {off.std():.2f} min, n {off.size}")


def test_I6a_mwra_against_check_mwra():
    """I6(a): the bench's Mercury rise-azimuth maxima against
    results/bm2008-reconcile/check_mwra.py (its .json) on the S2 years other
    than -1177: the discrete maximum nearest S2's MWRA."""
    rows = _s2_rows()
    ref = json.loads((ROOT / "results" / "bm2008-reconcile" / "check_mwra.json").read_text(encoding="utf-8"))
    lat, lon, _ = sky.site("bm")
    segs, keys = [], []
    for r in rows:
        ya = 1 - int(r["year"])
        j0 = cal.jdn_from_julian(ya, 1, 1)
        segs.append(_far(np.arange(j0, j0 + 140)))
        keys.append((r["year"], _jdn(ya, r["mwra"])))
    D = np.concatenate(segs)
    res = sky.crossing("mercury", D, lat, lon, dt=sky.BM_CLOCK_DT, window_h=(0, 14), with_elong=True)
    agree, bad, off = 0, [], 0
    for (yb, s2), seg in zip(keys, segs):
        sl = slice(off, off + seg.size)
        off += seg.size
        mx = sky.azimuth_maxima(seg, res["jd_ut"][sl], res["az"][sl], res["elong"][sl])
        near = mx[np.argmin(np.abs(mx["day_jdn"] - s2))]
        y, m, d = cal.julian_from_jdn(int(near["day_jdn"]))
        mine = (f"{d}-{MN[m]}", int(near["day_jdn"] - s2))
        theirs = tuple(ref[yb]["az_max"][:2])
        if mine == theirs:
            agree += 1
        else:
            bad.append((yb, mine, theirs, float(near["margin"])))
    print(f"    I6(a): {agree}/{len(rows)} maxima on check_mwra's date; the others: {bad}")
    assert agree >= 140, agree
    for yb, mine, theirs, margin in bad:          # one day apart, at a flat-ish maximum
        assert abs(mine[1] - theirs[1]) == 1 and margin < 0.02, (yb, mine, theirs, margin)


def test_published_1189_azimuths():
    """DESIGN 2.2: 12 Feb 120.48066 and 13 Feb 120.48110 deg (-1188, bm, 27,602.7 s), bisected to 0.01 s."""
    lat, lon, _ = sky.site("bm")
    d = _far(np.array([cal.jdn_from_julian(-1188, 2, 12), cal.jdn_from_julian(-1188, 2, 13)]))
    r = sky.crossing("mercury", d, lat, lon, dt=sky.BM_CLOCK_DT, window_h=(0, 14))
    assert abs(r["az"][0] - 120.48066) < 2e-5 and abs(r["az"][1] - 120.48110) < 2e-5, r["az"]


def test_azimuth_maxima_synthetic():
    days = np.arange(1000, 1030)
    x = days - 0.75 + 0.001 * np.sin(days)               # rising instants
    az = 110.0 - 0.03 * (x - 1012.3) ** 2                # exact parabola, vertex at 1012.3
    el = np.where(x < 1020, -20.0, 5.0)
    mx = sky.azimuth_maxima(days, x, az, el)
    assert mx.size == 1 and mx["complete"][0] and abs(mx["jd_ut"][0] - 1012.3) < 1e-9
    assert abs(mx["curv"][0] + 0.06) < 1e-9 and mx["morning"][0] and not mx["flat"][0]
    flat = 110.0 - 0.0005 * (x - 1012.3) ** 2            # curvature 0.001 deg/d^2 < 0.002
    assert sky.azimuth_maxima(days, x, flat)["flat"][0]
    # a maximum 2 days from the series' end has no complete 7-day window
    mx = sky.azimuth_maxima(days, x, 110.0 - 0.03 * (x - 1027.2) ** 2)   # discrete maximum on day 1028
    assert mx.size == 1 and not mx["complete"][0] and mx["day_jdn"][0] == 1028
    # two runs of days are never joined
    d2 = np.concatenate([days[:10], days[15:]])
    assert all(m["day_jdn"] not in (1009, 1010, 1014, 1015) for m in
               sky.azimuth_maxima(d2, np.concatenate([x[:10], x[15:]]), np.concatenate([az[:10], az[15:]])))


def test_conjunctions_vs_ephem_new_moons():
    for (y0, y1, eph) in ((-1500, -1498, "de431"), (-1, 1, "de431"), (150, 152, "de441")):
        a, b = cal.jd_from_julian(y0, 1, 1), cal.jd_from_julian(y1, 1, 1)
        mine = Cn.conjunctions(a, b, eph=eph)
        cuts = [a, b] if not (a < sky.DE431_SPLIT_JD < b) or eph != "de431" else [a, sky.DE431_SPLIT_JD, b]
        ref = []
        with sky.ephemeris(eph):
            for p, q in zip(cuts[:-1], cuts[1:]):
                ref += ephem.new_moons(p, q - 1.01 if q == sky.DE431_SPLIT_JD else q)
        ref = np.array(sorted(ref))
        assert mine.size == ref.size, (y0, mine.size, ref.size)
        assert np.max(np.abs(mine - ref)) * 86400 < 0.05, (y0, np.max(np.abs(mine - ref)) * 86400)


def test_de431_guard():
    try:
        sky.geo_ecliptic(("moon",), np.array([sky.DE431_SPLIT_JD - 1, sky.DE431_SPLIT_JD + 1]), "de431")
    except ValueError:
        pass
    else:
        raise AssertionError("a straddling DE431 request was not refused")
    # each side alone is served
    sky.geo_ecliptic(("moon",), np.array([sky.DE431_SPLIT_JD - 1, sky.DE431_SPLIT_JD]), "de431")
    sky.geo_ecliptic(("moon",), np.array([sky.DE431_SPLIT_JD, sky.DE431_SPLIT_JD + 1]), "de431")


def test_crel_calibration_and_published_bounds():
    """DESIGN 2.9: h_A = 2.04, h_P = 0.92; 11 Feb - 31 Mar at -1700, 22 Feb - 6 Apr at -700."""
    lat, lon, _ = sky.site("ithaki")
    hA, hP = sky.calibrate_crel(lat, lon)
    assert abs(hA - 2.04) < 0.01 and abs(hP - 0.92) < 0.01, (hA, hP)
    sb = sky.season_bounds_from(sky.season_altitudes([-1700, -700, -1999, 200], lat, lon), hA, hP)
    assert sb[-1700][:2] == (cal.jdn_from_julian(-1700, 2, 11), cal.jdn_from_julian(-1700, 3, 31))
    assert sb[-700][:2] == (cal.jdn_from_julian(-700, 2, 22), cal.jdn_from_julian(-700, 4, 6))
    assert all(v[2] for v in sb.values())              # the search ranges hold the bounds at both ends


def test_evening_twilight_bruteforce():
    lat, lon, _ = sky.site("ithaki")
    days = _far(np.array([cal.jdn_from_julian(-1700, 2, 11), cal.jdn_from_julian(-700, 4, 6),
                          cal.jdn_from_julian(150, 3, 1), cal.jdn_from_julian(-1999, 1, 20)]))
    tw = sky.evening_twilight(days, lat, lon)
    for t in tw:
        g = t + np.arange(-3, 4) / 86400.0
        a = sky.sun_alt(g, lat, lon)
        assert a[1] > -12.0 >= a[5], a                 # within 2 s


def test_march_equinox():
    years = np.array([-1900, -900, 0, 200])
    tt = sky.march_equinox(years)
    lon = sky.geo_ecliptic(("sun",), tt)["sun"][0]
    assert np.all(np.minimum(lon, 360 - lon) < 2e-5), lon
    # Meeus (Astronomical Algorithms, 2nd ed., table 27.A, -1000..+1000): mean March equinox
    for y, t in zip(years[1:], tt[1:]):
        Y = y / 1000.0
        jde0 = 1721139.29189 + 365242.13740 * Y + 0.06134 * Y ** 2 + 0.00111 * Y ** 3 - 0.00071 * Y ** 4
        assert abs(t - jde0) < 0.1, (y, t - jde0)
    y, m, d, _ = cal.julian_from_jd(tt[-1])
    assert (m, d) in ((3, 20), (3, 21)), (m, d)


def test_geo_events_fine_grid():
    rng = np.random.default_rng(2)
    starts = [cal.jd_from_julian(int(y), 1, 15) for y in rng.choice(np.arange(-1990, 190), 6, replace=False)]
    segs = [s + np.arange(150) for s in starts]
    ev = sky.geo_events("mercury", segs)
    assert {"W", "E", "D", "R"} <= set(ev["kind"])
    for x in ev:
        g = x["jd_tt"] + np.arange(-100, 101) * 0.002
        el, lb = sky.signed_elongation("mercury", g)
        y = el if x["kind"] in "WE" else np.degrees(np.unwrap(np.radians(lb)))
        k = int(np.argmin(y) if x["kind"] in "WD" else np.argmax(y))
        assert abs(k - 100) <= 2, (x["kind"], (k - 100) * 0.002)
    # a morning station is a direct station (longitude minimum) west of the Sun
    assert np.all(ev[ev["kind"] == "W"]["elong"] < 0) and np.all(ev[ev["kind"] == "E"]["elong"] > 0)


def test_mercury_magnitude_vs_skyfield():
    from skyfield.magnitudelib import planetary_magnitude
    jd = cal.jd_from_julian(150, 3, 1) + np.arange(0, 120, 7.0)
    mine = sky.mercury_magnitude(jd)
    t = ephem.time_tt(jd, 0.0)
    k = ephem.kernel(t.tt, ("sun", "earth", "mercury"))
    ref = planetary_magnitude(k["earth"].at(t).observe(k["mercury"]))
    ssb = sky.mercury_magnitude(jd, sun="ssb")             # skyfield's Sun-at-barycentre convention
    assert np.nanmax(np.abs(ssb - ref)) < 1e-6, np.nanmax(np.abs(ssb - ref))
    # the true Sun moves the magnitude by the barycentre offset (<= about 0.01 au) only
    assert np.nanmax(np.abs(mine - ref)) < 0.15, np.nanmax(np.abs(mine - ref))


def test_plsv_and_av10_consistent():
    lat, lon, _ = sky.site("ithaki")
    days = _far(cal.jdn_from_julian(-1500, 7, 1) + np.arange(0, 180))   # autumn mornings favour Mercury
    pv = sky.plsv_morning(days, lat, lon)
    r = sky.crossing("mercury", days, lat, lon, window_h=(0, 14), with_elong=True)
    vis = pv["visible"]
    assert vis.any() and (~vis).any()
    # visible mornings have Mercury west of the Sun and a dark sky at its rising
    assert np.all(r["elong"][vis] < -8.0) and np.all(r["sun_alt"][vis] < -5.0)


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
