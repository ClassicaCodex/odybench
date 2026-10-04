# Precise Mercury rising azimuth near the 1178 BC and 1189 BC MWRA dates (my own rise finder on ephem positions)
import sys, numpy as np
sys.path.insert(0, "C:/Projects/odybench")
from odybench import ephem as E
LAT, LON, H0, DT = 38.4, 20.7, -0.5667, 27602.7
def rise(jd0):
    # coarse 2-min grid over local night 00:00-08:00 UT+2 -> find upward crossing of H0, then bisect to 0.01 s
    g = jd0 - 2/24 + np.arange(0, 8*60, 2)/1440.0
    alt, az = E.altaz("mercury", g, LAT, LON, dt=DT)
    alt = np.asarray(alt)
    idx = np.where((alt[:-1] < H0) & (alt[1:] >= H0))[0]
    if len(idx) == 0: return None
    a, b = g[idx[0]], g[idx[0]+1]
    for _ in range(40):
        m = 0.5*(a+b)
        if float(E.altaz("mercury", m, LAT, LON, dt=DT)[0]) < H0: a = m
        else: b = m
    t = 0.5*(a+b)
    return t, float(E.altaz("mercury", t, LAT, LON, dt=DT)[1])
for (y, m, d0, n) in ((-1177, 3, 6, 14), (-1188, 2, 7, 13)):
    print("==", y, m)
    prev = None
    for k in range(n):
        jd0 = E.jd_from_julian(y, m, d0 + k)       # 0h UT of civil date (UT+2 date approx)
        r = rise(jd0)
        if r is None: print(d0+k, "no rise"); continue
        t, az = r
        h = ((t - jd0)*24 + 2) % 24
        print(f"{y} {m:02d}-{d0+k:02d}  rise {h:6.3f} h UT+2  az {az:9.5f}" + (f"  d={az-prev:+.5f}" if prev else ""))
        prev = az
