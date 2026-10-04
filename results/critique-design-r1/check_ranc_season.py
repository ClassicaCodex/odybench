"""Round-1 review: is 30 Sep 1131 BC (-1130) inside R_anc's season bound
(apparent solar longitude on Day 0 in [180, 270) deg, DESIGN 5.3)?
Computes the Sun's geocentric apparent ecliptic longitude (true equinox of
date, Vondrak precession, DE441) at the conjunction of 30 Sep -1130 and the
date of the autumnal equinox of -1130.  Also 16 Apr -1177 and 30 Oct -1206.
Run: cd C:/Projects/odybench && py results/critique-design-r1/check_ranc_season.py
"""
import sys
import numpy as np
from scipy.optimize import brentq

sys.path.insert(0, ".")
from odybench import ephem, calendar as cal  # noqa: E402


def sun_lon(jd_tt):
    jd_tt = np.atleast_1d(jd_tt)
    t = ephem.time_tt(jd_tt, 0.0)
    k = ephem.kernel(t.tt, ("sun", "earth"))
    e = k["earth"].at(t)
    eps = ephem.mean_obliquity(t.tt) + t._nutation_angles_radians[1]
    v = e.observe(k["sun"]).apparent(deflectors=(10,)).xyz.au
    x, y, z = np.einsum("ij...,j...->i...", t.M, v)
    yl = y * np.cos(eps) + z * np.sin(eps)
    return np.degrees(np.arctan2(yl, x)) % 360.0


for (y, m, d) in [(-1130, 9, 30), (-1177, 4, 16), (-1206, 10, 30), (-1182, 1, 12)]:
    jd0 = cal.jd_from_julian(y, m, d)
    nm = ephem.new_moons(jd0 - 2, jd0 + 2)
    for jt in nm:
        dt = ephem.delta_t(cal.julian_epoch(jt), "smh2020")
        ju = jt - dt / 86400.0
        print(f"conjunction {ephem.fmt_jd(ju, 'UT')}  Sun apparent longitude {float(sun_lon(jt)[0]):.2f} deg")

# autumnal equinox of -1130 (apparent longitude 180)
jd_a = cal.jd_from_julian(-1130, 9, 15)
f = lambda x: ((float(sun_lon(x)[0]) - 180.0 + 180.0) % 360.0) - 180.0
grid = jd_a + np.arange(0, 40)
vals = [f(x) for x in grid]
for i in range(len(grid) - 1):
    if vals[i] < 0 <= vals[i + 1]:
        r = brentq(f, grid[i], grid[i + 1], xtol=1e-6)
        dt = ephem.delta_t(cal.julian_epoch(r), "smh2020")
        print("autumnal equinox -1130:", ephem.fmt_jd(r - dt / 86400.0, "UT"))
