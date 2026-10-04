"""Reconciliation check 3: Table S2's Venus columns (rise of Venus and of the
Sun on Ti-5) recomputed with DE441 (odybench.ephem), Delta-T 27,602.7 s,
site 38.4N 20.7E (also 37.0N and 39.5N), airless altitude with standard
horizon h0 = -0.5667 deg (Venus) / -0.8333 deg (Sun, upper limb + refraction).
Reports the clock offset (S2 minus computed UT) and the Venus pass set."""
import sys, math
sys.path.insert(0, '.')
import numpy as np
from odybench import ephem as E
DT = 27602.7
MON = {m: i+1 for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split())}
def load():
    with open('data/bm2008-a/table_s2.tsv', encoding='utf-8') as f:
        L = [l.rstrip('\n') for l in f if l.strip() and not l.startswith('#')]
    h = L[0].split('\t'); out = []
    for l in L[1:]:
        c = l.split('\t'); c += [''] * (len(h) - len(c)); out.append(dict(zip(h, c)))
    return out
def secs(t):
    p = list(map(int, t.split(":"))) + [0]; return p[0]*3600 + p[1]*60 + p[2]   # 1176 BC prints "6:20"
def rise_ut(name, j0ut, lat, lon, h0):
    g = j0ut + np.arange(0, 1, 1/1440)       # 1-min grid over the UT day starting j0ut
    alt, _ = E.altaz(name, g, lat, lon, dt=DT)
    i = np.nonzero((alt[:-1] < h0) & (alt[1:] >= h0))[0]
    if len(i) == 0: return None
    i = i[0]; f = (h0 - alt[i])/(alt[i+1]-alt[i]); return g[i] + f/1440
rows = load()
for lat in (38.4, 37.0, 39.5):
    off_s, off_v, Vpass = [], [], []
    for r in rows:
        yb = int(r['year']); ya = 1 - yb
        d, m = r['Ti'].split('-')
        j = E.jd_from_julian(ya, MON[m], int(d)) - 5          # 0h UT of Ti-5
        j0 = j - 0.5 + 0.5 - 4/24                             # search from 20:00 UT previous day
        sr = rise_ut('sun', j0, lat, 20.7, -0.8333)
        vr = rise_ut('venus', j0, lat, 20.7, -0.5667)
        lead = (sr - vr)*1440 if (vr is not None and vr < sr) else None
        if r['sunrise']:
            off_s.append(secs(r['sunrise'])/60 - ((sr - math.floor(sr - 0.5) - 0.5)*1440))
            off_v.append(secs(r['venus_rise'])/60 - ((vr - math.floor(vr - 0.5) - 0.5)*1440))
        if lead is not None and lead >= 90: Vpass.append(yb)
        if lat == 38.4 and yb in (1178, 1189, 1157, 1111, 1250, 1170):
            print(yb, 'S2', r['venus_rise'], r['sunrise'], r['diff'], '| DE441 lead min', None if lead is None else round(lead, 1))
    off_s = np.array(off_s); off_v = np.array(off_v)
    print(f'lat {lat}: S2 sunrise - DE441 UT sunrise: mean {off_s.mean():.2f} min, sd {off_s.std():.2f}, n {len(off_s)}; '
          f'S2 Venus rise - DE441 UT: mean {off_v.mean():.2f}, sd {off_v.std():.2f}')
    if lat == 38.4:
        print('   DE441 Venus lead >= 90 min, all S2 rows:', sorted(Vpass, reverse=True), len(Vpass), '; in 1250-1115:', len([y for y in Vpass if 1115 <= y <= 1250]))
        S2V = sorted([int(r['year']) for r in rows if r['c_diff'] == 'O'], reverse=True)
        print('   S2 orange Venus:', S2V, len(S2V), '; symmetric difference:', sorted(set(S2V) ^ set(Vpass)))
