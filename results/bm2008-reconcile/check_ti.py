"""Reconciliation check 1: is Table S2's Ti the civil date of a geocentric
conjunction, and in which time zone?  DE441 via odybench.ephem; Delta-T held at
B&M's Starry Night value 27,602.7 s (and SMH2020 for comparison).
Also: which years have a second new moon inside the stated constellation
window (Ti-29 >= 17 Feb and Ti-12 <= 4 Apr)?"""
import sys, math
sys.path.insert(0, '.')
from odybench import ephem as E

MON = {m: i+1 for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split())}
def load_s2(p='data/bm2008-a/table_s2.tsv'):
    rows = []
    with open(p, encoding='utf-8') as f:
        lines = [l.rstrip('\n') for l in f if l.strip() and not l.startswith('#')]
    hdr = lines[0].split('\t')
    for l in lines[1:]:
        c = l.split('\t'); c += [''] * (len(hdr) - len(c))
        rows.append(dict(zip(hdr, c)))
    return rows

def dm(s):
    d, m = s.split('-'); return int(d), MON[m]

rows = load_s2()
DT_SN = 27602.7
j0 = E.jd_from_julian(-1251, 1, 1); j1 = E.jd_from_julian(-1098, 1, 1)
nms = E.new_moons(j0, j1)
print('conjunctions found', len(nms))
# count in window 1 Jan 1250 BC .. 31 Dec 1115 BC inclusive, UT+2 civil dates
w0 = E.jd_from_julian(-1249, 1, 1) - 2/24 + DT_SN/86400   # 00:00 UT+2 1 Jan -1249, in TT
w1 = E.jd_from_julian(-1113, 1, 1) - 2/24 + DT_SN/86400
print('conjunctions 1 Jan 1250 BC - 31 Dec 1115 BC (UT+2 dates):', sum(1 for x in nms if w0 <= x < w1))

def civil(jd_tt, zone_h, dt=DT_SN):
    jl = jd_tt - dt/86400 + zone_h/24
    y, m, d = E.julian_from_jd(math.floor(jl - 0.5) + 0.5)[:3]
    frac = (jl - 0.5) % 1.0
    return (y, m, int(d)), frac*24

zones = {'UT': 0.0, 'LMT20.7E': 20.7/15, 'UT+2': 2.0, 'UT+3': 3.0}
match = {z: 0 for z in zones}
bad = []
for r in rows:
    yb = int(r['year']); ya = 1 - yb
    d, m = dm(r['Ti'])
    jt = E.jd_from_julian(ya, m, d, 12.0) + DT_SN/86400
    x = min(nms, key=lambda q: abs(q - jt))
    res = {}
    for z, h in zones.items():
        (y2, m2, d2), hr = civil(x, h)
        res[z] = ((m2, d2) == (m, d), hr, (m2, d2))
        if (m2, d2) == (m, d): match[z] += 1
    if not res['UT+2'][0]:
        bad.append((yb, r['Ti'], res['UT+2'][2], round(res['UT+2'][1], 2), res['UT'][0], round(res['UT'][1], 2)))
print('Ti == conjunction civil date, by zone:', match, 'of', len(rows))
print('rows not matching UT+2 date: (yearBC, Ti printed, UT+2 (m,d), UT+2 hour, matchesUT?, UT hour)')
for b in bad: print('  ', b)

# second qualifying new moon per year (common/leap aware): Ti-29 >= 17 Feb and Ti-12 <= 4 Apr, UT+2 civil date
print('years with two new moons satisfying Ti-29 >= 17 Feb and Ti-12 <= 4 Apr (UT+2 dates):')
two = []
for yb in range(1251, 1099, -1):
    ya = 1 - yb
    lo = E.jd_from_julian(ya, 2, 17) + 29; hi = E.jd_from_julian(ya, 4, 4) + 12
    q = []
    for x in nms:
        (y2, m2, d2), hr = civil(x, 2.0)
        if y2 != ya: continue
        jd = E.jd_from_julian(y2, m2, d2)
        if lo <= jd <= hi: q.append(f"{d2}-{'JanFebMarAprMay'[3*(m2-1):3*m2]}")
    if len(q) != 1: two.append((yb, q))
for t in two: print('  ', t)

print()
print('All rows with conjunction between 00:00 and 08:00 UT+2 (DE441, dT 27602.7 s): yearBC, Ti printed, conj UT+2 date/hour, S2 = same day?')
early = []
for r in rows:
    yb = int(r['year']); ya = 1 - yb
    d, m = dm(r['Ti'])
    jt = E.jd_from_julian(ya, m, d, 12.0) + DT_SN/86400
    x = min(nms, key=lambda q: abs(q - jt))
    (y2, m2, d2), hr = civil(x, 2.0)
    if hr < 8.0:
        early.append((round(hr, 2), yb, r['Ti'], (m2, d2), (m2, d2) == (m, d)))
for e in sorted(early): print('  ', e)

print()
print('Per year: new moons (DE441, UT+2 date) satisfying Ti-29 >= 17 Feb and Ti-12 <= 4 Apr, vs S2 Ti')
for r in rows:
    yb = int(r['year']); ya = 1 - yb
    lo = E.jd_from_julian(ya, 2, 17) + 29; hi = E.jd_from_julian(ya, 4, 4) + 12
    d, m = dm(r['Ti']); jti = E.jd_from_julian(ya, m, d)
    q = []
    for x in nms:
        (y2, m2, d2), hr = civil(x, 2.0)
        if y2 != ya: continue
        jd = E.jd_from_julian(y2, m2, d2)
        if lo <= jd <= hi: q.append(f"{d2}-{'JanFebMarAprMay'[3*(m2-1):3*m2]}")
    inwin = lo <= jti <= hi
    if len(q) != 1 or not inwin or q[0] != r['Ti']:
        print('  ', yb, 'S2 Ti', r['Ti'], 'S2 Ti in window' if inwin else 'S2 Ti OUTSIDE window', '| in-window NMs:', q)
