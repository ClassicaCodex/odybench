import urllib.request, urllib.parse, os, re, math, json, hashlib, sys
sys.stdout.reconfigure(encoding='utf-8')
CACHE='C:/Projects/odybench/results/controls/hzcache/'
os.makedirs(CACHE, exist_ok=True)
def jd_julian(y, m, d):  # astronomical year, Julian calendar, d may be fractional
    if m <= 2: y -= 1; m += 12
    return math.floor(365.25*(y+4716)) + math.floor(30.6001*(m+1)) + d - 1524.5
def jd_to_julian(jd):
    jd += 0.5; Z = math.floor(jd); F = jd - Z; A = Z
    B = A + 1524; C = math.floor((B-122.1)/365.25); D = math.floor(365.25*C); E = math.floor((B-D)/30.6001)
    day = B - D - math.floor(30.6001*E) + F
    m = E-1 if E < 14 else E-13; y = C-4716 if m > 2 else C-4715
    return y, m, day
def horizons(body, lon, lat, jd0, jd1, step='2 m', quantities='2,4,13,30', ttype='UT'):
    p = dict(format='text', COMMAND=f"'{body}'", OBJ_DATA="'NO'", MAKE_EPHEM="'YES'", EPHEM_TYPE="'OBSERVER'",
             CENTER="'coord@399'", COORD_TYPE="'GEODETIC'", SITE_COORD=f"'{lon},{lat},0'",
             START_TIME=f"'JD {jd0:.6f}'", STOP_TIME=f"'JD {jd1:.6f}'", STEP_SIZE=f"'{step}'",
             QUANTITIES=f"'{quantities}'", TIME_TYPE=f"'{ttype}'", ANG_FORMAT="'DEG'", CAL_FORMAT="'JD'", EXTRA_PREC="'YES'")
    url = 'https://ssd.jpl.nasa.gov/api/horizons.api?' + urllib.parse.urlencode(p, safe="'@,:")
    key = hashlib.md5(url.encode()).hexdigest()
    f = CACHE + key + '.txt'
    if not os.path.exists(f):
        txt = urllib.request.urlopen(url, timeout=180).read().decode('utf-8', 'replace')
        open(f, 'w', encoding='utf-8').write(txt)
    txt = open(f, encoding='utf-8').read()
    m = re.search(r'\$\$SOE\n(.*?)\$\$EOE', txt, re.S)
    if not m: raise RuntimeError(txt[:3000])
    out = []
    for line in m.group(1).strip().splitlines():
        parts = line.split()
        # JD, [flags], ra, dec, az, el, angdiam, dT
        jd = float(parts[0])
        nums = [x for x in parts[1:] if re.match(r'^-?\d+(\.\d+)?$', x)]
        out.append((jd, *map(float, nums[-6:])))
    return out
if __name__ == '__main__':
    print(jd_julian(-430, 8, 3), jd_to_julian(jd_julian(-430,8,3)))
    r = horizons(10, 23.727, 37.972, jd_julian(-430,8,3.6), jd_julian(-430,8,3.62), step='10 m')
    print(r)
