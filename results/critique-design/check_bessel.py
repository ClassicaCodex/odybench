# Independent local-circumstances solver from NASA polynomial Besselian elements.
# Written from the textbook formulation (Explanatory Supplement 1992 ch. 8; Meeus, Elements of Solar Eclipses),
# not ported from NASA program.js or from odybench code.
import math, re, sys
D2R = math.pi/180
F = 1/298.257223563
def load_jsex(path):
    txt = open(path, encoding="utf-8").read()
    out = {}
    for m in re.finditer(r"//(-?\d+)\s+(\d+)\s+(\d+)\s*\n(.*?)(?=//-?\d+\s+\d+\s+\d+|\)\s*\))", txt, re.S):
        nums = [float(v) for v in re.findall(r"-?\d+\.\d+(?:e[-+]\d+)?", m.group(4))]
        out[(int(m.group(1)), int(m.group(2)), int(m.group(3)))] = nums
    return out
def elems(e):
    jd, t0, tmin, tmax, dT = e[0], e[1], e[2], e[3], e[4]
    x = e[6:10]; y = e[10:14]; d = e[14:17]; mu = e[17:20]; l1 = e[20:23]; l2 = e[23:26]; tf1, tf2 = e[26], e[27]
    return dict(jd=jd, t0=t0, dT=dT, x=x, y=y, d=d, mu=mu, l1=l1, l2=l2, tf1=tf1, tf2=tf2, tmin=tmin, tmax=tmax)
def poly(c, t): return sum(ci * t**i for i, ci in enumerate(c))
def local(E, lat, lon_e, dT, t):
    phi = lat*D2R
    u1 = math.atan((1-F)*math.tan(phi))
    rs = (1-F)*math.sin(u1); rc = math.cos(u1)   # rho sin phi', rho cos phi' at sea level
    x, y = poly(E['x'], t), poly(E['y'], t)
    d = poly(E['d'], t)*D2R
    mu = poly(E['mu'], t)
    H = (mu + lon_e - 0.00417807*dT) * D2R
    xi = rc*math.sin(H)
    eta = rs*math.cos(d) - rc*math.sin(d)*math.cos(H)
    zeta = rs*math.sin(d) + rc*math.cos(d)*math.cos(H)
    L1 = poly(E['l1'], t) - zeta*E['tf1']
    L2 = poly(E['l2'], t) - zeta*E['tf2']
    m = math.hypot(x-xi, y-eta)
    # sun altitude: sin h = sin d sin phi + cos d cos phi cos H (geocentric approx)
    alt = math.asin(math.sin(d)*math.sin(phi) + math.cos(d)*math.cos(phi)*math.cos(H))/D2R
    return m, L1, L2, alt
def maxecl(E, lat, lon_e, dT):
    best = None
    t = -4.0
    while t <= 4.0:
        m, L1, L2, alt = local(E, lat, lon_e, dT, t)
        if best is None or m < best[0]: best = (m, t)
        t += 0.002
    # refine
    lo, hi = best[1]-0.004, best[1]+0.004
    for _ in range(60):
        a = lo + (hi-lo)/3; b = hi - (hi-lo)/3
        if local(E, lat, lon_e, dT, a)[0] < local(E, lat, lon_e, dT, b)[0]: hi = b
        else: lo = a
    t = (lo+hi)/2
    m, L1, L2, alt = local(E, lat, lon_e, dT, t)
    mag = (L1 - m)/(L1 + L2)
    total = (L2 < 0) and (m < -L2)
    ut_h = E['t0'] + t - dT/3600.0
    return dict(t=t, m=m, L1=L1, L2=L2, mag=mag, total=total, alt=alt, ut=ut_h)
def hm(h):
    h = h % 24; return "%02d:%02d" % (int(h), int(round((h-int(h))*60)) if int(round((h-int(h))*60))<60 else 59)
def window(E, lat, lon_e, lo=20000, hi=40000, step=10):
    tot = [dt for dt in range(lo, hi, step) if maxecl(E, lat, lon_e, dt)['total']]
    return (min(tot), max(tot)) if tot else None
if __name__ == "__main__":
    base = "C:/Projects/odybench/data/refs/nasa/"
    ITH = (38.367, 20.717)
    cases = [("JSEX-SEm1199.js", (-1177,4,16)), ("JSEX-SEm1199.js", (-1130,9,30)), ("JSEX-SEm1399.js", (-1311,6,24)), ("JSEX-SEm1199.js", (-1182,1,12))]
    for f, key in cases:
        EL = load_jsex(base + f)
        e = EL.get(key)
        if e is None: print("missing", key); continue
        E = elems(e)
        r = maxecl(E, *ITH, E['dT'])
        lmt = r['ut'] + ITH[1]/15
        print(key, "canon dT", E['dT'], "mag %.4f" % r['mag'], "total" if r['total'] else "partial", "max UT", hm(r['ut']), "LMT", hm(lmt), "Sun alt %.1f" % r['alt'])
        w = window(E, *ITH, lo=int(E['dT'])-3000, hi=int(E['dT'])+3000, step=5)
        print("   totality window (dT, s):", w, " offsets vs canon:", (w[0]-E['dT'], w[1]-E['dT']) if w else None)
    # 1178 at B&M's dT and the canon dT, magnitude
    E = elems(load_jsex(base+"JSEX-SEm1199.js")[(-1177,4,16)])
    for dt in (27602.7, 28543, 28590, 28907, 29263):
        r = maxecl(E, *ITH, dt); print("1178 BC dT", dt, "mag %.3f" % r['mag'], "UT", hm(r['ut']), "LMT", hm(r['ut']+ITH[1]/15), "total" if r['total'] else "")
