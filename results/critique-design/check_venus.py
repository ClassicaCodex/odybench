import sys, numpy as np
sys.path.insert(0, "C:/Projects/odybench")
from odybench import ephem as E
LAT, LON, DT = 38.4, 20.7, 27602.7
def rise(body, jd0, h0):
    g = jd0 - 2/24 + np.arange(0, 9*60, 2)/1440.0
    alt = np.asarray(E.altaz(body, g, LAT, LON, dt=DT)[0])
    i = np.where((alt[:-1] < h0) & (alt[1:] >= h0))[0][0]
    a, b = g[i], g[i+1]
    for _ in range(40):
        m = 0.5*(a+b)
        if float(E.altaz(body, m, LAT, LON, dt=DT)[0]) < h0: a = m
        else: b = m
    return 0.5*(a+b)
def hms(jd, jd0):
    h = (jd - jd0)*24 + 2
    s = round(h*3600); return "%d:%02d:%02d" % (s//3600, (s%3600)//60, s%60)
for (y,m,d) in ((-1177,4,11), (-1188,3,13)):
    jd0 = E.jd_from_julian(y, m, d)
    sr = rise("sun", jd0, -0.8333); vr = rise("venus", jd0, -0.5667)
    print(y, m, d, "sunrise UT+2", hms(sr, jd0), "Venus rise", hms(vr, jd0), "lead %.1f min" % ((sr-vr)*1440))
