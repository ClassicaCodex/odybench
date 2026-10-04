"""Reconciliation check 2: what is Table S2's 'MWRA' (maximum western rise
azimuth) numerically?  For every S2 year, compute with DE441 (odybench.ephem,
Delta-T 27,602.7 s, site 38.4N 20.7E, airless altitude, rising at h0 = -0.5667 deg):
  az_max : local maxima of Mercury's rising azimuth (from N through E), i.e.
           southernmost rising point
  az_min : local minima of rising azimuth (northernmost rising point)
  stat_d : stationary points in geocentric apparent ecliptic longitude
           (retrograde->direct)   stat_r : direct->retrograde
  gwe    : greatest western elongation (morning)
  infc   : inferior conjunction (longitude)
and compare each with S2's printed MWRA date.  Dates are UT+2 civil dates,
proleptic Julian."""
import sys, math, json
sys.path.insert(0, '.')
import numpy as np
from odybench import ephem as E

DT = 27602.7; LAT, LON = 38.4, 20.7; H0 = -0.5667; Z = 2.0
MON = {m: i+1 for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split())}
MN = {v: k for k, v in MON.items()}
def load():
    with open('data/bm2008-a/table_s2.tsv', encoding='utf-8') as f:
        L = [l.rstrip('\n') for l in f if l.strip() and not l.startswith('#')]
    h = L[0].split('\t'); out = []
    for l in L[1:]:
        c = l.split('\t'); c += [''] * (len(h) - len(c)); out.append(dict(zip(h, c)))
    return out
def jdd(ya, s):
    d, m = s.split('-'); return E.jd_from_julian(ya, MON[m], int(d))
def lab(jd0h):
    y, m, d = E.julian_from_jd(jd0h)[:3]; return f"{int(d)}-{MN[m]}"
def civ0(jd_ut):  # 0h of the UT+2 civil date containing jd_ut
    return math.floor(jd_ut + Z/24 - 0.5) + 0.5

def ecl_lon(name, jd_tt):
    t = E.time_tt(jd_tt, 0.0)
    k = E.kernel(t.tt, ('sun', 'earth', 'mercury'))
    v = k['earth'].at(t).observe(k[E.BODY_NAMES[name]]).apparent(deflectors=(10,)).xyz.au
    x, y, z = np.einsum('ij...,j...->i...', t.M, v)
    eps = E.mean_obliquity(t.tt) + t._nutation_angles_radians[1]
    return np.degrees(np.arctan2(y*np.cos(eps) + z*np.sin(eps), x)) % 360

out = {}
rows = load()
for r in rows:
    yb = int(r['year']); ya = 1 - yb
    j0 = E.jd_from_julian(ya, 1, 1) - Z/24          # 00:00 UT+2 on 1 Jan, as UT
    n = 140
    g = j0 + np.arange(0, n * 144) / 144.0
    alt, az = E.altaz('mercury', g, LAT, LON, dt=DT)
    up = np.nonzero((alt[:-1] < H0) & (alt[1:] >= H0))[0]
    rise = []
    for i in up:
        f = (H0 - alt[i]) / (alt[i+1] - alt[i])
        jr = g[i] + f / 144.0
        a = az[i] + f * (az[i+1] - az[i])
        rise.append((civ0(jr), a))
    rd = np.array([x[0] for x in rise]); ra = np.array([x[1] for x in rise])
    azmax = [rd[i] for i in range(1, len(ra)-1) if ra[i] >= ra[i-1] and ra[i] > ra[i+1]]
    azmin = [rd[i] for i in range(1, len(ra)-1) if ra[i] <= ra[i-1] and ra[i] < ra[i+1]]
    # daily geocentric quantities at 00:00 UT+2 (TT = UT + DT)
    dd = j0 + np.arange(0, n)
    tt = dd + DT / 86400
    lm = ecl_lon('mercury', tt); ls = ecl_lon('sun', tt)
    dl = (np.diff(lm) + 180) % 360 - 180
    stat_d = [civ0(dd[i+1]) for i in range(len(dl)-1) if dl[i] < 0 and dl[i+1] >= 0]
    stat_r = [civ0(dd[i+1]) for i in range(len(dl)-1) if dl[i] > 0 and dl[i+1] <= 0]
    el = (lm - ls + 180) % 360 - 180              # negative = west of Sun (morning)
    gwe = [civ0(dd[i]) for i in range(1, n-1) if el[i] < 0 and el[i] <= el[i-1] and el[i] < el[i+1]]
    infc = [civ0(dd[i+1]) for i in range(n-1) if el[i] > 0 and el[i+1] <= 0 and abs(el[i]) < 10]
    s2 = jdd(ya, r['mwra'])
    tgt = jdd(ya, r['Ti']) - 34
    rec = {'s2_mwra': r['mwra'], 'Ti': r['Ti']}
    for name, L in (('az_max', azmax), ('az_min', azmin), ('stat_d', stat_d), ('stat_r', stat_r), ('gwe', gwe), ('infc', infc)):
        if L:
            near_s2 = min(L, key=lambda q: abs(q - s2))
            near_t = min(L, key=lambda q: abs(q - tgt))
            rec[name] = (lab(near_s2), int(round(near_s2 - s2)), lab(near_t))
        else:
            rec[name] = None
    # azimuth flatness: az at S2 date and at our max
    out[yb] = rec
    print(yb, r['mwra'], {k: v for k, v in rec.items() if k not in ('s2_mwra', 'Ti')}, flush=True)
json.dump(out, open('results/bm2008-reconcile/check_mwra.json', 'w'), indent=1)
print()
for name in ('az_max', 'az_min', 'stat_d', 'stat_r', 'gwe', 'infc'):
    d = [v[name][1] for v in out.values() if v[name] is not None]
    d = np.array(d)
    print(f'{name:7s}: n={len(d)} exact={np.sum(d==0)} within1={np.sum(abs(d)<=1)} within2={np.sum(abs(d)<=2)} median={np.median(d):+.1f} (event - S2 MWRA, days)')
