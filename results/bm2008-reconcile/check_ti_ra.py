"""Does an RA-conjunction or minimum-separation definition of 'New Moon'
reproduce Table S2's Ti better than ecliptic-longitude conjunction?
DE441 via odybench.ephem; Delta-T 27,602.7 s; dates in UT+2 and LMT 20.7E."""
import sys, math
sys.path.insert(0, '.')
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from odybench import ephem as E
sys.path.insert(0, 'results/bm2008-reconcile')
from check_ti import load_s2, dm, civil, DT_SN, nms   # reuses the longitude conjunctions
rows = load_s2()

def ra_diff(jd_tt):
    t = E.time_tt(jd_tt, 0.0)
    m = E.apparent('moon', t); s = E.apparent('sun', t)
    rm, _, _ = m.radec(epoch='date'); rs, _, _ = s.radec(epoch='date')
    return ((rm._degrees - rs._degrees + 180) % 360) - 180
def sep(jd_tt):
    t = E.time_tt(jd_tt, 0.0)
    return E.apparent('moon', t).separation_from(E.apparent('sun', t)).degrees

res = {'lon': {}, 'ra': {}, 'minsep': {}}
for r in rows:
    yb = int(r['year']); ya = 1 - yb
    d, m = dm(r['Ti'])
    jt = E.jd_from_julian(ya, m, d, 12.0) + DT_SN/86400
    x = min(nms, key=lambda q: abs(q - jt))
    xr = brentq(ra_diff, x - 0.6, x + 0.6, xtol=1e-6)
    xs = minimize_scalar(sep, bounds=(x - 0.6, x + 0.6), method='bounded', options={'xatol': 1e-5}).x
    for name, val in (('lon', x), ('ra', xr), ('minsep', xs)):
        res[name][yb] = (val, (m, d))
for name in res:
    for z, h in (('UT', 0.0), ('LMT', 20.7/15), ('UT+2', 2.0)):
        ok = sum(1 for yb, (v, md) in res[name].items() if (lambda c: (c[0][1], c[0][2]))(civil(v, h)) == md)
        print(f'{name:7s} {z:5s} matches {ok}/152')
print('\nrows where RA conjunction (UT+2) still mismatches:')
for yb, (v, md) in res['ra'].items():
    (y2, m2, d2), hr = civil(v, 2.0)
    if (m2, d2) != md:
        print('  ', yb, md, (m2, d2), round(hr, 2), 'lon-conj hr', round(civil(res['lon'][yb][0], 2.0)[1], 2))
