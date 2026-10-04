"""Extra checks for docs/research-controls.md. Run from this folder: py run_extra.py"""
import sys, re, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
from local import solar_local, fmt_h
from hz import jd_julian, jd_to_julian
td = lambda h, m, s: (h + m/60 + s/3600)/24

print('== 1. Ithaca, -1177 Apr 16: local magnitude vs Delta T (DE441 via Horizons, dT emulated by longitude shift)')
d = 16 + td(17, 57, 28)
for dT in list(range(25000, 34001, 1000)) + list(range(28400, 29801, 200)):
    r = solar_local(20.72, 38.37, -1177, 4, d, 28590, dT_alt=dT, half_window_h=3 if 28400 <= dT <= 29800 else 5, step='1 m' if 28400 <= dT <= 29800 else '3 m')['alt']
    print(dT, f"{r['mag']:.4f}", 'TOTAL' if r['total'] else '', fmt_h(r['lmt_h']), f"{r['sun_el']:.1f}")

print('== 2. Almagest / Tarutius Egyptian dates -> Julian (Nabonassar epoch JD 1448638 = -746 Feb 26)')
EPOCH = 1448638
months = ['Thoth','Phaophi','Athyr','Choiak','Tybi','Mecheir','Phamenoth','Pharmouthi','Pachon','Payni','Epiphi','Mesore']
def nab(year, month, day): return EPOCH + (year-1)*365 + months.index(month)*30 + (day-1)
for label, y, m, dd in [('Mardokempad 1 Thoth 29/30 (Alm IV.6)', 27, 'Thoth', 29), ('Mardokempad 2 Thoth 18/19', 28, 'Thoth', 18),
        ('Mardokempad 2 Phamenoth 15/16', 28, 'Phamenoth', 15), ('Nab 366 Thoth 26/27 (Alm IV.11, Phanostratus)', 366, 'Thoth', 26),
        ('Nab 366 Phamenoth 24/25', 366, 'Phamenoth', 24), ('Hadrian 17 Payni 20/21 (Hadrian 1 = Nab 864)', 880, 'Payni', 20),
        ('Hadrian 19 Choiak 2/3', 882, 'Choiak', 2), ('Hadrian 20 Pharmouthi 19/20', 883, 'Pharmouthi', 19),
        ('Theon Venus, Hadrian 16 Pharmouthi 21/22 (Alm X.1)', 879, 'Pharmouthi', 21), ('Mercury, Hadrian 19 Athyr 14/15 (Alm IX.8)', 882, 'Athyr', 14),
        ('Tarutius conception Choiak 23 (Nab year -24)', -24, 'Choiak', 23)]:
    y_, m_, d_ = jd_to_julian(nab(y, m, dd))
    print(f'{label:55s} -> evening of {y_} {m_:02d} {d_:05.2f}')

print('== 3. Almagest planetary records vs true greatest elongation (Horizons geocentric S-O-T)')
def elong(body, jd0, jd1):
    p = dict(format='text', COMMAND=f"'{body}'", OBJ_DATA="'NO'", MAKE_EPHEM="'YES'", EPHEM_TYPE="'OBSERVER'",
             CENTER="'500@399'", START_TIME=f"'JD {jd0}'", STOP_TIME=f"'JD {jd1}'", STEP_SIZE="'1 d'", QUANTITIES="'23'", CAL_FORMAT="'JD'")
    t = urllib.request.urlopen('https://ssd.jpl.nasa.gov/api/horizons.api?' + urllib.parse.urlencode(p, safe="'@,:"), timeout=120).read().decode()
    b = re.search(r'\$\$SOE\n(.*?)\$\$EOE', t, re.S).group(1)
    return [(float(l.split()[0]), float(l.split()[-2]), l.split()[-1]) for l in b.strip().splitlines()]
for name, body, (y, m, dd) in (('Venus (Theon, Alm X.1)', 299, (132, 3, 8.5)), ('Mercury (Alm IX.8)', 199, (134, 10, 2.5))):
    jd = jd_julian(y, m, dd); E = elong(body, jd-25, jd+25)
    best = max(E, key=lambda e: e[1]); rec = [e for e in E if abs(e[0]-jd) < 0.6][0]
    print(f'{name}: record {y}-{m:02d}-{dd} elong {rec[1]:.2f}; true max {best[1]:.2f} {best[2]} on {jd_to_julian(best[0])} (offset {best[0]-jd:+.0f} d); days within 0.5 deg of max: {sum(1 for e in E if e[1] > best[1]-0.5)}')

print('== 4. Alternatives and portents at fixed sites (NASA catalogue dT)')
for lab, place, lon, lat, y, mo, dd, h, mi, s, dT in [
    ('Archilochus alt -710 Mar 14', 'Thasos', 24.71, 40.78, -710, 3, 14, 14, 25, 57, 20368),
    ('Archilochus alt -710 Mar 14', 'Paros', 25.15, 37.08, -710, 3, 14, 14, 25, 57, 20368),
    ('Ennius alt (Bennett) -404 Mar 20', 'Rome', 12.49, 41.89, -404, 3, 20, 19, 33, 16, 15518),
    ('Caesar death yr -43 Apr 18', 'Rome', 12.49, 41.89, -43, 4, 18, 20, 59, 8, 10972),
    ('Caesar death yr -43 Oct 12', 'Rome', 12.49, 41.89, -43, 10, 12, 1, 34, 43, 10967),
    ('Dio 41.14.3 / Lucan 1.540 cand -50 Mar 07', 'Rome', 12.49, 41.89, -50, 3, 7, 14, 46, 58, 11046),
    ('-49 Aug 21', 'Rome', 12.49, 41.89, -49, 8, 21, 10, 2, 16, 11031)]:
    r = solar_local(lon, lat, y, mo, dd + td(h, mi, s), dT, dT_alt=dT)['alt']
    mu = 'n/a' if r['magup'] is None else f"{r['magup']:.3f}"
    print(f"{lab:42s} {place:8s} max={r['mag']:.3f}{' TOTAL' if r['total'] else ''} sunUp={mu} LMT {fmt_h(r['lmt_h'])} sunEl={r['sun_el']:.1f}")
