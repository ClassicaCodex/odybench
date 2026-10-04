"""Reconciliation check 4: single-number checks for 1178 BC (-1177) with DE441
(odybench.ephem).  Site 38.4N 20.7E.  Times printed as UT+2 (B&M's clock, see
check_venus) unless stated.  Delta-T 27,602.7 s (Starry Night, B&M Method)
unless stated."""
import sys, math
sys.path.insert(0, '.')
import numpy as np
from scipy.optimize import brentq
from odybench import ephem as E
DT = 27602.7; LAT, LON = 38.4, 20.7
def hm(jd_ut, z=2.0):
    x = (jd_ut + z/24 - 0.5) % 1 * 24; return f"{int(x):02d}:{(x % 1)*60:04.1f}"
# conjunctions
for x in E.new_moons(E.jd_from_julian(-1177, 3, 10), E.jd_from_julian(-1177, 4, 25)):
    print('conjunction', E.fmt_jd(x, 'TT'), '| UT+2 with dT 27602.7 s:', hm(x - DT/86400), '| UT+2 with SMH2020:', hm(x - E.delta_t(-1177.25)/86400), f'(dT {E.delta_t(-1177.25):.0f} s)')
# equinox: apparent geocentric solar longitude = 0
def sunlon(jd_tt):
    t = E.time_tt(jd_tt, 0.0); k = E.kernel(t.tt, ('sun', 'earth'))
    v = k['earth'].at(t).observe(k['sun']).apparent(deflectors=(10,)).xyz.au
    x, y, z = np.einsum('ij...,j...->i...', t.M, v)
    eps = E.mean_obliquity(t.tt) + t._nutation_angles_radians[1]
    return (math.degrees(math.atan2(y*math.cos(eps) + z*math.sin(eps), x)) + 180) % 360 - 180
j = brentq(sunlon, E.jd_from_julian(-1177, 3, 28), E.jd_from_julian(-1177, 4, 5), xtol=1e-7)
print('vernal equinox', E.fmt_jd(j, 'TT'), '| UT+2 (dT 27602.7):', hm(j - DT/86400), 'B&M: 1 Apr 3:24 p.m.')
# nautical twilight 18 Mar evening
g = E.jd_from_julian(-1177, 3, 18, 15.0) + np.arange(0, 6*60)/1440
alt, _ = E.altaz('sun', g, LAT, LON, dt=DT)
i = np.nonzero((alt[:-1] > -12) & (alt[1:] <= -12))[0][0]
print('Sun at -12 deg (airless) on 18 Mar 1178 BC:', hm(g[i]), 'B&M Fig. 2: 7:38 p.m.')
# eclipse at Ithaca
for dtm in (DT, 'em2006_canon', 'smh2020'):
    c = E.local_circumstances(LAT, LON, E.jd_from_julian(-1177, 4, 16, 10.0) + 27602.7/86400, dt=dtm)
    print(f"eclipse at 38.4N 20.7E, dT={c['dt_s']:.0f} s: max {hm(c['jd_ut_max'])} UT+2 = {hm(c['jd_ut_max'], 20.7/15)} LMT, "
          f"LAT {c['lat_hours']:.2f} h, magnitude {c['magnitude']:.3f}, total {c['total']}, duration {c['duration_s']:.0f} s, Sun alt {c['sun_alt_deg']:.1f}")
# Mercury at morning rising: Sun altitude at the moment Mercury rises (h0=-0.5667), elongation, phase-angle magnitude
def merc_mag(jd_tt):
    t = E.time_tt(jd_tt, 0.0); k = E.kernel(t.tt, ('sun', 'earth', 'mercury'))
    e = k['earth'].at(t); m = e.observe(k['mercury']); s = e.observe(k['sun'])
    d = m.distance().au
    r = (k['mercury'] - k['sun']).at(t).distance().au
    R = s.distance().au
    i = math.degrees(math.acos((r*r + d*d - R*R)/(2*r*d)))
    # Mallama & Hilton (2018) Mercury V(1,i) polynomial
    v1 = -0.613 + 6.3280e-2*i - 1.6336e-3*i**2 + 3.3644e-5*i**3 - 3.4265e-7*i**4 + 1.6893e-9*i**5 - 3.0334e-12*i**6
    return v1 + 5*math.log10(r*d), i
for (ya, mo, dy, note) in ((-1177, 3, 11, '1178 Ti-36'), (-1177, 3, 12, '1178 Ti-35 (B&M: not visible)'), (-1177, 3, 13, '1178 Ti-34 (B&M: heliacal rising)'),
                          (-1177, 3, 14, '1178 Ti-33 (parallel)'), (-1188, 2, 12, '1189 Ti-35'), (-1188, 2, 13, '1189 Ti-34 = DE441 MWRA'),
                          (-1189, 2, 23, '1190 Ti-34'), (-1156, 2, 18, '1157 Ti-34'), (-1110, 2, 20, '1111 Ti-34')):
    g = E.jd_from_julian(ya, mo, dy) - 2/24 + np.arange(0, 12*60)/1440     # 00:00-12:00 UT+2
    alt, az = E.altaz('mercury', g, LAT, LON, dt=DT)
    i = np.nonzero((alt[:-1] < -0.5667) & (alt[1:] >= -0.5667))[0][0]
    salt, _ = E.altaz('sun', g[i], LAT, LON, dt=DT)
    el = float(E.elongation('mercury', g[i], dt=DT))
    mag, ph = merc_mag(g[i] + DT/86400)
    print(f'{note:38s} Mercury rises {hm(g[i])} UT+2, az {az[i]:.2f}, Sun alt then {float(salt):+.2f} deg, elongation {el:.1f}, V {mag:+.2f} (phase angle {ph:.0f})')
# Paliki (western Kefalonia, Bittlestone's Ithaca candidate; approx 38.25N 20.40E) and Schoch's Ithaca
for name, la, lo in (('Paliki ~38.25N 20.40E', 38.25, 20.40), ('Ithaca 38.37N 20.72E', 38.37, 20.72)):
    for dtm in (DT, 28590.0, 28907.0):
        c = E.local_circumstances(la, lo, E.jd_from_julian(-1177, 4, 16, 10.0) + 27602.7/86400, dt=dtm)
        print(f"{name}, dT={c['dt_s']:.0f} s: max {hm(c['jd_ut_max'])} UT+2, magnitude {c['magnitude']:.3f}, total {c['total']}, duration {c['duration_s']:.0f} s")
