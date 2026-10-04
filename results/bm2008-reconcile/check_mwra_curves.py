"""Rising-azimuth curves near the maximum for selected years, and the Mercury
delta recomputed with DE441 (nearest local max of rising azimuth to Ti-34,
true Julian day arithmetic, S2's own Ti)."""
import sys, math
sys.path.insert(0, '.'); sys.path.insert(0, 'results/bm2008-reconcile')
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
def lab(j):
    y, m, d = E.julian_from_jd(j)[:3]; return f"{int(d)}-{MN[m]}"
def risings(ya, mmin=1, n=140):
    j0 = E.jd_from_julian(ya, 1, 1) - Z/24
    g = j0 + np.arange(0, n*144)/144.0
    alt, az = E.altaz('mercury', g, LAT, LON, dt=DT)
    up = np.nonzero((alt[:-1] < H0) & (alt[1:] >= H0))[0]
    res = []
    for i in up:
        f = (H0 - alt[i])/(alt[i+1]-alt[i]); jr = g[i] + f/144
        res.append((math.floor(jr + Z/24 - 0.5) + 0.5, az[i] + f*(az[i+1]-az[i]), jr))
    return res
rows = load()
for yb in (1178, 1157, 1236, 1224, 1111):
    ya = 1 - yb
    R = risings(ya)
    i = max(range(1, len(R)-1), key=lambda k: R[k][1] if (R[k][1] >= R[k-1][1] and R[k][1] > R[k+1][1] and abs(R[k][0] - jdd(ya, next(r['mwra'] for r in rows if int(r['year'])==yb))) < 15) else -1)
    print(yb, 'rising azimuth (deg from N through E) around DE441 maximum:',
          ', '.join(f"{lab(R[k][0])} {R[k][1]:.3f}" for k in range(i-4, i+5)))
print()
M1 = []; M2 = []; M3 = []; table = []
for r in rows:
    yb = int(r['year']); ya = 1 - yb
    R = risings(ya)
    mx = [R[k][0] for k in range(1, len(R)-1) if R[k][1] >= R[k-1][1] and R[k][1] > R[k+1][1]]
    t34 = jdd(ya, r['Ti']) - 34
    near = min(mx, key=lambda q: abs(q - t34))
    d = int(round(t34 - near))
    table.append((yb, r['Ti'], lab(near), d, r['mwra'], r['delta']))
    if abs(d) <= 1: M1.append(yb)
    if abs(d) <= 2: M2.append(yb)
    if abs(d) <= 3: M3.append(yb)
inw = lambda L: [y for y in L if 1115 <= y <= 1250]
print('DE441 Mercury |delta|<=1 (all S2 years):', M1, ' in window:', inw(M1))
print('DE441 Mercury |delta|<=2:', M2)
print('DE441 Mercury |delta|<=3:', M3)
V = [int(r['year']) for r in rows if r['c_diff'] == 'O']
VY = [int(r['year']) for r in rows if r['c_diff'] in ('O', 'Y')]
print('S2-Venus orange & DE441 M<=1:', sorted(set(V) & set(M1)), '; Venus orange|yellow & DE441 M<=3:', sorted(set(VY) & set(M3)))
print('rows where DE441 delta differs from printed delta (yearBC, Ti, DE441 az-max, DE441 delta, S2 MWRA, S2 delta):')
for t in table:
    if str(t[3]) != t[5]: print('  ', t)
