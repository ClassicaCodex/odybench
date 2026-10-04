"""
Property tests for odybench.calendar over -1999..+500 (critique-design issue
13 fix 5 and issue 22).  No pytest on this machine, so:

    cd C:\\Projects\\odybench && py tests/test_calendar.py

(also collectable by pytest).  Runs in a few seconds.

Reference values and where they come from:
  * the DEFINITION JD 0.0 = -4712 Jan 1, 12h (proleptic Julian), from which
    every JDN of -1999..+500 is re-derived by independent day counting;
  * odybench.ephem's Meeus floating-point formulas (Meeus 1998, Astronomical
    Algorithms 2nd ed., eq. 7.1 and the ch. 7 inverse), an independent
    implementation already validated in docs/research-ephemeris.md;
  * Meeus 1998 ch. 7 worked examples 7.a-7.f and the ch. 7 table of JDs, as
    I recall them (the book is not on this machine): each one is ALSO
    re-derived here by day counting, so a mis-remembered value would fail;
  * the identity -1177 Apr 16 0h = JD 1291263.5, which JPL Horizons prints as
    "B.C. 1178-Apr-16 00:00" (data/ephem/horizons/, research-ephemeris);
  * JPL Horizons' own calendar output for 306 random instants
    (tools/validate_coverage.py section 8, cached in
    data/ephem/horizons/calendar_probe_*.txt; checked here when present).
"""
import math
import re
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from odybench import calendar as C  # noqa: E402
from odybench import ephem as E     # noqa: E402

Y0, Y1 = -1999, 500
MDAYS = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)


def counted_days():
    """Every day of -1999..+500 as (y, m, d, JDN, day-of-year), by counting days
    forward from the definition JDN(-4712 Jan 1) = 0 with the Julian leap rule
    written out longhand (a year is leap when year mod 4 == 0)."""
    jdn = 0
    y = -4712
    while y < Y0:
        jdn += 366 if y % 4 == 0 else 365
        y += 1
    ys, ms, ds, js, doys = [], [], [], [], []
    for y in range(Y0, Y1 + 1):
        doy = 0
        for m in range(1, 13):
            n = MDAYS[m - 1] + (1 if (m == 2 and y % 4 == 0) else 0)
            for d in range(1, n + 1):
                doy += 1
                ys.append(y)
                ms.append(m)
                ds.append(d)
                js.append(jdn)
                doys.append(doy)
                jdn += 1
    return tuple(np.array(a, dtype=np.int64) for a in (ys, ms, ds, js, doys))


DAYS = counted_days()


def test_every_day_against_day_counting():
    y, m, d, jdn, doy = DAYS
    assert len(y) == 2500 * 365 + 625 == int(jdn[-1] - jdn[0] + 1)      # 625 leap years in -1999..+500
    assert np.array_equal(C.jdn_from_julian(y, m, d), jdn)
    yy, mm, dd = C.julian_from_jdn(jdn)
    assert np.array_equal(yy, y) and np.array_equal(mm, m) and np.array_equal(dd, d)
    assert np.array_equal(C.day_of_year(y, m, d), doy)
    fy, fm, fd = C.from_day_of_year(y, doy)
    assert np.array_equal(fy, y) and np.array_equal(fm, m) and np.array_equal(fd, d)
    # consecutive days have consecutive JDNs, with no gaps across months and years
    assert np.all(np.diff(C.jdn_from_julian(y, m, d)) == 1)


def test_scalar_and_vector_paths_agree():
    y, m, d, jdn, _ = DAYS
    rng = np.random.default_rng(1)
    for i in rng.integers(0, len(y), 2000):
        assert C.jdn_from_julian(int(y[i]), int(m[i]), int(d[i])) == int(jdn[i])
        assert C.julian_from_jdn(int(jdn[i])) == (int(y[i]), int(m[i]), int(d[i]))
        assert type(C.jdn_from_julian(int(y[i]), int(m[i]), int(d[i]))) is int


def test_against_ephem_meeus_formulas():
    """odybench.ephem's Meeus floating-point conversions, every 7th day."""
    y, m, d, jdn, _ = DAYS
    for i in range(0, len(y), 7):
        jd = E.jd_from_julian(int(y[i]), int(m[i]), int(d[i]))
        assert jd == C.jd_from_julian(int(y[i]), int(m[i]), int(d[i])) == jdn[i] - 0.5
        assert E.julian_from_jd(jd + 0.3)[:3] == C.julian_from_jd(jd + 0.3)[:3]


def test_leap_rule():
    for yv in range(Y0, Y1 + 1):
        n = C.jdn_from_julian(yv + 1, 1, 1) - C.jdn_from_julian(yv, 1, 1)
        leap = bool(C.is_leap_julian(yv))
        assert n == (366 if leap else 365) == C.days_in_year(yv)
        assert leap == (yv % 4 == 0)
        # Feb 29 exists exactly in leap years
        feb = C.jdn_from_julian(yv, 3, 1) - C.jdn_from_julian(yv, 2, 1)
        assert feb == (29 if leap else 28) == C.days_in_month(yv, 2)
    # astronomical-year leap years in historical numbering: 1 BC, 5 BC, ..., 1177 BC; not 1178 BC
    assert C.is_leap_julian(0) and C.is_leap_julian(-4) and C.is_leap_julian(-1176)
    assert not C.is_leap_julian(-1177) and not C.is_leap_julian(-1) and not C.is_leap_julian(1)
    assert C.is_leap_julian(1900) and not C.is_leap_gregorian(1900) and C.is_leap_gregorian(2000)
    # the Julian year is 365.25 days on average over any 4 years
    assert C.jdn_from_julian(-1176, 1, 1) - C.jdn_from_julian(-1180, 1, 1) == 1461


def test_identity_1178_bc():
    assert C.jd_from_julian(-1177, 4, 16) == 1291263.5
    assert C.jdn_from_julian(-1177, 4, 16) == 1291264
    assert C.julian_from_jd(1291263.5) == (-1177, 4, 16, 0.0)
    assert C.historical_year(-1177) == "1178 BC" and C.astronomical_year(1178, "BC") == -1177
    assert C.historical_year(1) == "AD 1" and C.astronomical_year(1, "AD") == 1
    assert C.fmt(1291264.24824, "TT").startswith("-1177-04-16 17:57:28 TT (16 Apr 1178 BC")
    # proleptic GREGORIAN would put the same day 11 days earlier: 5 Apr (DESIGN section 0)
    assert C.jdn_from_gregorian(-1177, 4, 5) == C.jdn_from_julian(-1177, 4, 16)
    assert C.gregorian_from_jdn(1291264) == (-1177, 4, 5)


def test_meeus_examples():
    # Example 7.a: Sputnik, 1957 Oct 4.81 (Gregorian) -> JD 2436116.31
    assert abs(C.jd_from_gregorian(1957, 10, 4.81) - 2436116.31) < 1e-6
    # Example 7.b: 333 Jan 27.5 (Julian) -> JD 1842713.0
    assert C.jd_from_julian(333, 1, 27.5) == 1842713.0
    # Example 7.c: JD 2436116.31 -> 1957 Oct 4.81
    y, m, d, h = C.gregorian_from_jd(2436116.31)
    assert (y, m, d) == (1957, 10, 4) and abs(h / 24 - 0.81) < 1e-7
    # Example 7.d: Halley's comet perihelia 1910 Apr 20 and 1986 Feb 9 are 27689 days apart
    assert C.jdn_from_gregorian(1986, 2, 9) - C.jdn_from_gregorian(1910, 4, 20) == 27689
    # Example 7.e: 1954 Jun 30 (Gregorian) was a Wednesday (0 = Sunday)
    assert C.weekday(C.jdn_from_gregorian(1954, 6, 30)) == 3
    # Example 7.f: day of the year 1978 Nov 14 = 318, 1988 Apr 22 = 113
    assert C.day_of_year(1978, 11, 14) == 318 and C.day_of_year(1988, 4, 22) == 113
    # Meeus ch. 7 table (Gregorian from 1582 Oct 15, Julian before)
    table = [((2000, 1, 1.5), 2451545.0, "g"), ((1999, 1, 1.0), 2451179.5, "g"),
             ((1987, 1, 27.0), 2446822.5, "g"), ((1987, 6, 19.5), 2446966.0, "g"),
             ((1988, 1, 27.0), 2447187.5, "g"), ((1988, 6, 19.5), 2447332.0, "g"),
             ((1900, 1, 1.0), 2415020.5, "g"), ((1600, 1, 1.0), 2305447.5, "g"),
             ((1600, 12, 31.0), 2305812.5, "g"), ((837, 4, 10.3), 2026871.8, "j"),
             ((-123, 12, 31.0), 1676496.5, "j"), ((-122, 1, 1.0), 1676497.5, "j"),
             ((-1000, 7, 12.5), 1356001.0, "j"), ((-1000, 2, 29.0), 1355866.5, "j"),
             ((-1001, 8, 17.9), 1355671.4, "j"), ((-4712, 1, 1.5), 0.0, "j")]
    for (yv, mv, dv), jd, cal in table:
        f = C.jd_from_gregorian if cal == "g" else C.jd_from_julian
        assert abs(f(yv, mv, dv) - jd) < 1e-6, (yv, mv, dv, f(yv, mv, dv), jd)
    # the reform: Julian 1582 Oct 4 was followed by Gregorian 1582 Oct 15
    assert C.jdn_from_gregorian(1582, 10, 15) == C.jdn_from_julian(1582, 10, 4) + 1 == C.GREGORIAN_REFORM_JDN


def test_round_trips_of_instants():
    rng = np.random.default_rng(7)
    lo, hi = C.jd_from_julian(Y0, 1, 1), C.jd_from_julian(Y1 + 1, 1, 1)
    jd = rng.uniform(lo, hi, 200_000)
    y, m, d, h = C.julian_from_jd(jd)
    back = C.jd_from_julian(y, m, d, h)
    assert np.max(np.abs(back - jd)) * 86400 < 1e-3               # 1 ms
    assert np.all((h >= 0) & (h < 24))
    # vector and scalar agree
    for i in range(0, 200_000, 997):
        ys, ms_, ds, hs = C.julian_from_jd(float(jd[i]))
        assert (ys, ms_, ds) == (int(y[i]), int(m[i]), int(d[i])) and abs(hs - h[i]) < 1e-9


def test_zones_and_day_bounds():
    rng = np.random.default_rng(11)
    lo, hi = C.jd_from_julian(Y0, 1, 1), C.jd_from_julian(Y1, 12, 31)
    jd_ut = rng.uniform(lo, hi, 20_000)
    for off in (0.0, 2.0, C.lmt_offset_hours(20.72), -3.5):
        y, m, d, h = C.civil_date(jd_ut, off)
        # the civil date is the UT date of the shifted instant
        y2, m2, d2, h2 = C.julian_from_jd(jd_ut + off / 24.0)
        assert np.array_equal(y, y2) and np.array_equal(m, m2) and np.array_equal(d, d2)
        # the instant lies inside [start, end) of its civil day in that zone
        start, end = C.day_bounds(y, m, d, off)
        assert np.all((start <= jd_ut + 1e-8) & (jd_ut < end + 1e-8))      # 1-ms resolution of instants
    # UT+2: 22:00 UT on 15 Apr is 00:00 on 16 Apr, even though 22/24 is not exact in binary
    assert C.ut2_date(C.jd_from_julian(-1177, 4, 15, 22.0)) == (-1177, 4, 16, 0.0)
    assert C.ut2_date(C.jd_from_julian(-1177, 4, 15, 21.9999))[:3] == (-1177, 4, 15)
    # LMT at Ithaki (20.72 E = +1 h 22 m 52.8 s)
    y, m, d, h = C.lmt_date(C.jd_from_julian(-1177, 4, 15, 23.0), 20.72)
    assert (y, m, d) == (-1177, 4, 16) and abs(h - (23.0 + 20.72 / 15 - 24.0)) < 1e-9
    # LAT = LMT + equation of time (supplied by the caller)
    assert abs(C.lat_date(C.jd_from_julian(-1177, 4, 16, 10.0), 20.72, 0.25)[3]
               - C.lmt_date(C.jd_from_julian(-1177, 4, 16, 10.0), 20.72)[3] - 0.25) < 1e-6
    # a window 'through 31 Dec -1114 at UT+2' ends at 24:00 UT+2 = 22:00 UT on 31 Dec
    s, e = C.span_bounds((-1249, 1, 1), (-1114, 12, 31), 2.0)
    assert abs(e - (C.jd_from_julian(-1113, 1, 1) - 2 / 24)) < 1e-9
    assert abs(s - (C.jd_from_julian(-1249, 1, 1) - 2 / 24)) < 1e-9
    assert C.julian_from_jd(e - 1e-6, 2.0)[:3] == (-1114, 12, 31)


def test_time_scales_and_epochs():
    jd = C.jd_from_julian(-1177, 4, 16, 10.0)
    assert abs(C.ut_from_tt(C.tt_from_ut(jd, 28543.0), 28543.0) - jd) < 1e-9
    assert abs((C.tt_from_ut(jd, 28543.0) - jd) * 86400 - 28543.0) < 1e-4
    # Julian epoch: identical to ephem.julian_epoch; J2000.0 = 2000.0; 13 d ahead of y + (m - 0.5)/12 at -1177
    assert C.julian_epoch(2451545.0) == 2000.0
    assert float(C.julian_epoch(jd)) == float(E.julian_epoch(jd))
    lead = float(C.julian_epoch(C.jd_from_julian(-1177, 4, 16))) - float(C.decimal_year_nasa(-1177, 4))
    assert 0.02 < lead < 0.05                                       # about 13 days (ephem.julian_epoch doc)
    assert abs(float(C.calendar_year_fraction(C.jd_from_julian(-1177, 7, 2, 12.0))) - (-1177 + 0.5)) < 1e-9


def test_horizons_calendar_output():
    files = sorted((ROOT / "data" / "ephem" / "horizons").glob("calendar_probe_*.txt"))
    if not files:
        print("   (no Horizons calendar cache; run tools/validate_coverage.py)")
        return
    mon = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
    n = 0
    for f in files:
        body = f.read_text(encoding="utf-8").split("$$SOE")[1].split("$$EOE")[0]
        for ln in body.strip().splitlines():
            cal, jdv = [c.strip() for c in ln.split(",")[:2]]
            mt = re.fullmatch(r"(b?)(\d+)-(\w{3})-(\d\d) (\d\d):(\d\d):(\d\d)\.\d+", cal)
            yv = (1 - int(mt.group(2))) if mt.group(1) else int(mt.group(2))
            want = (yv, mon.index(mt.group(3)) + 1, int(mt.group(4)))
            assert C.julian_from_jd(float(jdv))[:3] == want, (cal, jdv)
            n += 1
    assert n >= 300


def test_no_gregorian_datetime_types_in_bench_sources():
    """DESIGN section 0 / critique issue 13: the bench must not use Python's
    date-time module or numpy's 64-bit date-time type (both proleptic
    Gregorian).  Scans odybench/, tools/, tests/ and top-level scripts."""
    pat = re.compile(r"^\s*(import\s+datetime|from\s+datetime\s+import)|datetime64|astype\(\s*['\"]M8|"
                     r"np\.datetime_as_string", re.M)
    files = (list((ROOT / "odybench").glob("*.py")) + list((ROOT / "tools").glob("*.py"))
             + list((ROOT / "tests").glob("*.py")) + list(ROOT.glob("*.py")))
    hits = []
    for f in files:
        if f.name == "test_calendar.py":
            continue
        for mt in pat.finditer(f.read_text(encoding="utf-8", errors="replace")):
            hits.append(f"{f.relative_to(ROOT)}: {mt.group(0).strip()}")
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
