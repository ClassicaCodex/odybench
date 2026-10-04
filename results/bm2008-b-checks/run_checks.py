"""Independent checks of Baikouzis & Magnasco (2008) Table 2 / Table S2 (extraction b).

Everything here is "computed by me" with low-precision tools, NOT the paper's software:
  - ephem.py   : Standish (JPL) Keplerian elements, Table 2a (3000 BC-3000 AD), J2000 ecliptic,
                 IAU 1976 precession (Meeus ch. 21), GMST (Meeus 12.4). No nutation/aberration.
  - newmoon.py : Meeus, Astronomical Algorithms 2nd ed., ch. 49 (new-moon times, TT).
Delta-T is fixed at B&M's Starry Night value 27,602.7 s. Site: Ithaca, 38.4 N, 20.7 E.
Calendar: proleptic Julian, astronomical years (1178 BC = -1177).

Run:  py results/bm2008-b-checks/run_checks.py   (from C:\\Projects\\odybench)
"""
import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ephem import julian_jd, rise, altaz, ecl_lon_date, radec_date
import newmoon

LAT, LON, DT = 38.4, 20.7, 27602.7
S2 = os.path.join(HERE, '..', '..', 'data', 'sources', 'bm2008-b', 'table_s2.tsv')
MON = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5}
rows = list(csv.DictReader(open(S2, encoding='utf-8'), delimiter='\t'))


def hms(h):
    h %= 24
    H = int(h); M = int((h - H) * 60); S = int(round(((h - H) * 60 - M) * 60))
    return f'{H:02d}:{M:02d}:{S:02d}'


def jd2s(jd):
    y, m, d = newmoon.jd_to_julian_cal(jd)
    return f'{int(d)}-{["", "Jan", "Feb", "Mar", "Apr", "May", "Jun"][m]}'


print('== 1. Clock convention: Venus rise / sunrise on Ti-5 vs B&M Table 2 ==')
for y, m, d, paper in [(-1177, 4, 11, '4:39:45 / 6:22:41 / 1:42:56'),
                       (-1249, 3, 28, '4:45:55 / 6:49:20 / 2:03:25'),
                       (-1169, 3, 14, '4:51:24 / 7:08:31 / 2:17:07')]:
    jd0 = julian_jd(y, m, d) - LON / 360
    jv = rise('venus', jd0, DT, LAT, LON, -0.5667)
    js = rise('sun', jd0, DT, LAT, LON, -0.8333)
    for tag, off in (('LMT', LON / 15), ('UT+2', 2.0)):
        hv = ((jv + 0.5) % 1) * 24 + off; hs = ((js + 0.5) % 1) * 24 + off
        print(f'  {1-y} BC {m}/{d} {tag:5s} Venus {hms(hv)} Sun {hms(hs)} diff {hms(hs-hv)}   paper {paper}')

print('\n== 2. MWRA = local maximum of Mercury rising azimuth (from N through E)? ==')
for r in rows:
    ybc = int(r['year_bc'])
    if ybc not in (1250, 1247, 1236, 1233, 1224, 1223, 1203, 1191, 1190, 1189, 1178, 1177,
                   1170, 1157, 1145, 1144, 1143, 1132, 1111, 1100):
        continue
    y = 1 - ybc
    dd, mm = r['MWRA'].split('-')
    target = julian_jd(y, MON[mm], int(dd))
    start = julian_jd(y, 1, 1) - 40
    vals = []
    for i in range(170):
        jd0 = start + i - LON / 360
        noon = jd0 + 0.5 + DT / 86400
        el = (ecl_lon_date('mercury', noon) - ecl_lon_date('sun', noon) + 180) % 360 - 180
        jm = rise('mercury', jd0, DT, LAT, LON, -0.5667)
        vals.append((jd0 + 0.5, altaz('mercury', jm, DT, LAT, LON)[1], el))
    mx = [v for i, v in enumerate(vals[1:-1], 1) if v[1] >= vals[i-1][1] and v[1] > vals[i+1][1]]
    me = [v for i, v in enumerate(vals[1:-1], 1) if v[2] <= vals[i-1][2] and v[2] < vals[i+1][2]]
    a = min(mx, key=lambda v: abs(v[0] - target)); e = min(me, key=lambda v: abs(v[0] - target))
    print(f"  {ybc} S2 MWRA {r['MWRA']:7s} rise-az max {jd2s(a[0]):7s} ({a[0]-target:+.0f} d)"
          f"  | max W elongation {jd2s(e[0]):7s} ({e[0]-target:+.0f} d, {e[2]:.1f} deg)")

print('\n== 3. Mercury around 1178 BC (daily, local mean noon) ==')
for day in range(0, 45, 1):
    jd0 = julian_jd(-1177, 2, 15) + day - LON / 360
    noon = jd0 + 0.5 + DT / 86400
    el = (ecl_lon_date('mercury', noon) - ecl_lon_date('sun', noon) + 180) % 360 - 180
    rate = (ecl_lon_date('mercury', noon + .5) - ecl_lon_date('mercury', noon - .5) + 180) % 360 - 180
    jm = rise('mercury', jd0, DT, LAT, LON, -0.5667); js = rise('sun', jd0, DT, LAT, LON, -0.8333)
    print(f'  {jd2s(jd0+0.5):7s} elong {el:7.2f}  dlon/dt {rate:6.3f}  rise-az {altaz("mercury", jm, DT, LAT, LON)[1]:7.2f}'
          f'  rises {(js-jm)*1440:5.1f} min before Sun')

print('\n== 4. Ti in Table S2 vs Meeus ch.49 conjunction date (LMT 20.7E) ==')
k0 = round((-1251 - 2000) * 12.3685) - 30
nm = []
for k in range(k0, k0 + 12 * 160):
    y, m, d = newmoon.jd_to_julian_cal(newmoon.jde_newmoon(k) - DT / 86400 + LON / 360)
    nm.append((y, m, int(d), (d % 1) * 24))
bad = 0
for r in rows:
    ybc = int(r['year_bc']); dd, mm = r['Ti'].split('-')
    c = [(m, d, h) for (y, m, d, h) in nm if y == 1 - ybc and m in (3, 4)]
    if not any(m == MON[mm] and d == int(dd) for m, d, h in c):
        bad += 1
        print(f"  {ybc} S2 Ti {r['Ti']:7s}  Meeus LMT: " + ', '.join(f'{d}/{m} {h:.1f}h' for m, d, h in c))
print(f'  {bad} of {len(rows)} rows differ')

print('\n== 5. Table S2 survivor counts ==')
def mins(s):
    p = [int(x) for x in s.split(':')]
    return p[0] * 60 + p[1] + (p[2] / 60 if len(p) > 2 else 0)
for lab, sel in (('1250-1115 BC', lambda y: 1115 <= y <= 1250), ('all S2 rows 1251-1100 BC', lambda y: True)):
    R = [r for r in rows if sel(int(r['year_bc']))]
    morn = [r for r in R if r['diff']]
    v90 = [r for r in morn if mins(r['diff']) >= 90]
    dl = lambda r: abs(int(r['delta']))
    print(f'  {lab}: rows {len(R)}; Venus morning {len(morn)}; Venus>=90min {len(v90)};'
          f' |d|<=1 {sum(dl(r)<=1 for r in R)}; |d|<=3 {sum(dl(r)<=3 for r in R)};'
          f' equinox flag {sum(bool(r["before"]) for r in R)}')
    print('    Venus>=90 & |d|<=1:', [r['year_bc'] for r in v90 if dl(r) <= 1],
          '  Venus>=60 & |d|<=3:', [r['year_bc'] for r in morn if mins(r['diff']) >= 60 and dl(r) <= 3])

print('\n== 6. 1178 BC spot checks ==')
f = lambda t: (ecl_lon_date('sun', t) + 180) % 360 - 180
a, b = julian_jd(-1177, 3, 25), julian_jd(-1177, 4, 9)
for _ in range(60):
    m = (a + b) / 2
    a, b = (m, b) if f(m) < 0 else (a, m)
y, mo, d = newmoon.jd_to_julian_cal(a - DT / 86400 + 2 / 24)
print(f'  vernal equinox: {int(d)}/{mo} {hms((d%1)*24)} UT+2   (paper: 1 April 3:24 p.m.)')
k0 = round((-1177.25 - 2000) * 12.3685)
for k in range(k0 + 6, k0 + 8):
    y, mo, d = newmoon.jd_to_julian_cal(newmoon.jde_newmoon(k) - DT / 86400 + 2 / 24)
    print(f'  new moon {int(d)}/{mo} {hms((d%1)*24)} UT+2')
jd0 = julian_jd(-1177, 3, 18) - 2 / 24
prev = None
for i in range(12 * 60, 24 * 60):
    alt = altaz('sun', jd0 + i / 1440, DT, LAT, LON)[0]
    if prev is not None and prev > -12 >= alt:
        print(f'  Sun at -12 deg, evening 18 Mar: {i//60:02d}:{i%60:02d} UT+2   (paper Fig. 2: 7:38 p.m.)'); break
    prev = alt
