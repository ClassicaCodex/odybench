"""Round-1 review: can instrument check I11(a) pass?

I11(a) (DESIGN 6.1) requires ZERO survivors, in every window, for AEN-TROY's
pinned reading R-ii-literal: AEN-TROY-02 ii-a (Day 0 is the conjunction date,
LMT at Troy) + AEN-TROY-04 a (the Moon is above the horizon at some instant
between the end of evening nautical twilight and the start of morning
nautical twilight of Night 0) + AEN-TROY-07 vis7 (Venus visible as a morning
object on Dawn +1, arcus visionis 7 deg).  DESIGN calls the reading
self-contradictory.  It is not, if the conjunction falls early on Day 0: by
the evening the Moon is up to ~24 h old and can still be above the horizon
when the Sun reaches -12 deg.

This counts, over 1250-1115 BC (-1249..-1114) and 1350-1100 BC, the
conjunctions whose Moon is above the horizon at the end of evening nautical
twilight of Day 0 at Troy (39.9575 N, 26.2389 E), and of those, the ones with
Venus a visible morning object on Dawn +1.  "Above the horizon" is tested two
ways: topocentric airless centre altitude > 0, and > -0.8333 deg (upper limb
with standard refraction).  Moon after the evening twilight cannot rise again
before morning twilight on a conjunction date (it is east of the Sun), so the
evening instant is the one that matters.
Run: cd C:/Projects/odybench && py results/critique-design-r1/check_i11a.py
"""
import sys
import numpy as np

sys.path.insert(0, ".")
from odybench import ephem, calendar as cal  # noqa: E402

LAT, LON = 39.9575, 26.2389
LMT_H = LON / 15.0


def dt_s(jd_tt):
    return float(ephem.delta_t(cal.julian_epoch(jd_tt), "smh2020"))


def evening_naut_end(jdn):
    """UT instant when the Sun's centre reaches -12 deg in the evening of LMT civil day jdn."""
    jd0 = jdn - 0.5 - LMT_H / 24.0                 # 00:00 LMT in UT
    grid = jd0 + (16 * 60 + np.arange(0, 7 * 60 + 1, 2)) / 1440.0
    a, _ = ephem.altaz("sun", grid, LAT, LON)
    a = np.asarray(a)
    idx = np.nonzero((a[:-1] > -12) & (a[1:] <= -12))[0]
    i = idx[0]
    f = (a[i] + 12) / (a[i] - a[i + 1])
    return grid[i] + f * (grid[i + 1] - grid[i])


def venus_vis7(jdn):
    """Venus rises before the Sun on LMT day jdn with the Sun <= -7 deg at Venus' rising."""
    jd0 = jdn - 0.5 - LMT_H / 24.0
    grid = jd0 + np.arange(0, 9 * 60 + 1, 3) / 1440.0
    av, _ = ephem.altaz("venus", grid, LAT, LON)
    asun, _ = ephem.altaz("sun", grid, LAT, LON)
    av, asun = np.asarray(av), np.asarray(asun)
    iv = np.nonzero((av[:-1] < -0.5667) & (av[1:] >= -0.5667))[0]
    isun = np.nonzero((asun[:-1] < -0.8333) & (asun[1:] >= -0.8333))[0]
    if len(iv) == 0 or len(isun) == 0 or iv[0] >= isun[0]:
        return False
    i = iv[0]
    f = (-0.5667 - av[i]) / (av[i + 1] - av[i])
    s_at = asun[i] + f * (asun[i + 1] - asun[i])
    return s_at <= -7.0


def run(y0, y1):
    a = cal.jd_from_julian(y0, 1, 1) - 2
    b = cal.jd_from_julian(y1 + 1, 1, 1) + 2
    conj = []
    while a < b:
        e = min(a + 365.25 * 40, b)
        conj += ephem.new_moons(a, e)
        a = e
    conj = sorted(set(round(x, 6) for x in conj))
    n = 0
    up0, upr = [], []
    for jt in conj:
        ju = jt - dt_s(jt) / 86400.0
        jdn = cal.jdn_of_instant(ju, offset_hours=LMT_H)
        y, m, d = cal.julian_from_jdn(jdn)
        if not (y0 <= y <= y1):
            continue
        n += 1
        te = evening_naut_end(jdn)
        alt, _ = ephem.altaz("moon", te, LAT, LON)
        alt = float(alt)
        age_h = (te - ju) * 24.0
        if alt > -0.8333:
            vis = venus_vis7(jdn + 1)
            rec = (y, m, d, round(age_h, 1), round(alt, 2), vis)
            upr.append(rec)
            if alt > 0:
                up0.append(rec)
    return n, up0, upr


for (y0, y1) in [(-1249, -1114), (-1349, -1099)]:
    n, up0, upr = run(y0, y1)
    print(f"\nwindow {y0}..{y1}: {n} conjunctions (Day 0 = LMT date at Troy)")
    print(f"  Moon centre above 0 deg at end of evening nautical twilight of Day 0: {len(up0)};"
          f" with Venus vis7 on Dawn +1 (R-ii-literal survivors): {sum(r[5] for r in up0)}")
    print(f"  Moon centre above -0.8333 deg: {len(upr)}; with Venus vis7: {sum(r[5] for r in upr)}")
    for r in upr:
        print("   ", r)
