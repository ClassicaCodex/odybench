"""
Local circumstances of ancient solar eclipses at the Ionian islands, from the
Besselian elements of NASA's Five Millennium Canon of Solar Eclipses
(Espenak & Meeus 2006, NASA/TP-2006-214141), as distributed with NASA's
JavaScript Solar Eclipse Explorer (eclipse.gsfc.nasa.gov/JSEX/SEm1299.js etc.,
saved under data/refs/nasa/JSEX-SEm*.js).

The geometry is a Python port of the O'Byrne/Espenak Eclipse Explorer
(data/refs/nasa/JSEX-program.js): shadow coordinates (u, v), penumbral and
umbral radii L1', L2' on the observer's fundamental-plane parallel, and the
hour angle h = mu - lambda_west - 1.002738 * dT * 2*pi/86400.

Delta T enters ONLY through the hour angle, so changing dT slides every track
east-west without changing anything else; that is how the Delta-T
uncertainty is propagated here.

Usage:  py eclipse_local.py            (writes eclipse_ionian.csv beside itself)
Times are UT (= TT - dT); dates are proleptic Julian, astronomical years.
"""
import csv
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NASA = os.path.join(HERE, "..", "..", "data", "refs", "nasa")

# Sites (deg N, deg E).  Vathy is the modern capital of Ithaki; Nidri is
# Doerpfeld's Leukas-Ithaca; Argostoli and Paliki stand for Kefalonia and
# Bittlestone's Paliki-Ithaca.  They span ~0.6 deg, far less than the
# Delta-T uncertainty, so they are reported for completeness only.
SITES = {
    "Ithaki (Vathy)": (38.367, 20.717),
    "Lefkada (Nidri)": (38.707, 20.712),
    "Kefalonia (Argostoli)": (38.176, 20.489),
    "Paliki (Lixouri)": (38.200, 20.437),
}

K = 1.002738 * 2 * math.pi / 86400.0   # rad of Earth rotation per second of UT


def parse_jsex(path):
    """Yield (label, elements[28]) from a JSEX-SEm*.js file."""
    txt = open(path, encoding="utf-8").read()
    parts = re.split(r"^//\s*(-?\d+)\s+(\d+)\s+(\d+)\s*$", txt, flags=re.M)
    # parts = [preamble, y, m, d, body, y, m, d, body, ...]
    for i in range(1, len(parts), 4):
        y, m, d, body = int(parts[i]), int(parts[i + 1]), int(parts[i + 2]), parts[i + 3]
        nums = re.findall(r"[-+]?\d+\.\d*(?:[eE][-+]?\d+)?|[-+]?\d+(?:[eE][-+]?\d+)?", body)
        vals = [float(x) for x in nums[:28]]
        if len(vals) == 28:
            yield (y, m, d), vals


def state(el, t, lat, lon_west, dT):
    """Shadow geometry for observer at TT hour offset t from t0."""
    x = ((el[9] * t + el[8]) * t + el[7]) * t + el[6]
    y = ((el[13] * t + el[12]) * t + el[11]) * t + el[10]
    d = math.radians((el[16] * t + el[15]) * t + el[14])
    mu = math.radians((el[19] * t + el[18]) * t + el[17])
    l1 = (el[22] * t + el[21]) * t + el[20]
    l2 = (el[25] * t + el[24]) * t + el[23]
    tf1, tf2 = el[26], el[27]
    u_ = math.atan(0.99664719 * math.tan(lat))
    rs, rc = 0.99664719 * math.sin(u_), math.cos(u_)   # rho sin phi', rho cos phi'
    h = mu - lon_west - dT * K
    xi = rc * math.sin(h)
    eta = rs * math.cos(d) - rc * math.cos(h) * math.sin(d)
    zeta = rs * math.sin(d) + rc * math.cos(h) * math.cos(d)
    L1 = l1 - zeta * tf1
    L2 = l2 - zeta * tf2
    m = math.hypot(x - xi, y - eta)
    alt = math.asin(math.sin(d) * math.sin(lat) + math.cos(d) * math.cos(lat) * math.cos(h))
    return m, L1, L2, alt


def magnitude(m, L1, L2):
    """Eclipse magnitude (fraction of solar diameter covered); >=1 when total."""
    if m >= L1:
        return 0.0, "-"
    if m < abs(L2):
        ratio = (L1 - L2) / (L1 + L2)
        return ratio, ("T" if L2 < 0 else "A")
    return (L1 - m) / (L1 + L2), "P"


def obscuration(m, L1, L2):
    """Fraction of the solar disc area covered (O'Byrne/Espenak formula)."""
    if m >= L1:
        return 0.0
    if m <= -L2:            # total
        return 1.0
    ratio = (L1 - L2) / (L1 + L2)
    if m <= L2:             # annular, Moon wholly inside
        return ratio * ratio
    c = math.acos(max(-1, min(1, (L1 * L1 + L2 * L2 - 2 * m * m) / (L1 * L1 - L2 * L2))))
    b = math.acos(max(-1, min(1, (L1 * L2 + m * m) / m / (L1 + L2))))
    a = math.pi - b - c
    return ((ratio * ratio * a + b) - ratio * math.sin(c)) / math.pi


def local(el, lat_deg, lon_e_deg, dT=None, step_h=1 / 360.0, horizon=-0.00524):
    """Maximum magnitude seen with the Sun above the horizon (JSEX threshold
    -0.3 deg), plus its UT and solar altitude.  Brute-force time scan."""
    if dT is None:
        dT = el[5]
    lat = math.radians(lat_deg)
    lonw = -math.radians(lon_e_deg)
    best = (0.0, "-", None, None, 0.0)
    t = el[2]
    while t <= el[3]:
        m, L1, L2, alt = state(el, t, lat, lonw, dT)
        if alt > horizon:
            mag, typ = magnitude(m, L1, L2)
            if mag > best[0]:
                best = (mag, typ, t, math.degrees(alt), obscuration(m, L1, L2))
        t += step_h
    mag, typ, t, alt, obs = best
    if t is None:
        return dict(mag=0.0, type="-", ut=None, alt=None, obsc=0.0)
    ut = (el[1] + t - dT / 3600.0) % 24.0
    return dict(mag=mag, type=typ, ut=ut, alt=alt, obsc=obs)


def hms(h):
    if h is None:
        return ""
    s = int(round(h * 3600))
    return f"{s // 3600:02d}:{(s % 3600) // 60:02d}"


def julian_to_jd(y, m, d):
    if m <= 2:
        y -= 1
        m += 12
    return math.floor(365.25 * (y + 4716)) + math.floor(30.6001 * (m + 1)) + d - 1524.5


def jd_to_gregorian(jd):
    z = math.floor(jd + 0.5)
    a = math.floor((z - 1867216.25) / 36524.25)
    a = z + 1 + a - math.floor(a / 4)
    b = a + 1524
    c = math.floor((b - 122.1) / 365.25)
    d = math.floor(365.25 * c)
    e = math.floor((b - d) / 30.6001)
    day = b - d - math.floor(30.6001 * e)
    mon = e - 1 if e < 14 else e - 13
    yr = c - 4716 if mon > 2 else c - 4715
    return yr, mon, day


def load(years=(-1299, -1049)):
    out = []
    for f in ("JSEX-SEm1399.js", "JSEX-SEm1299.js", "JSEX-SEm1199.js", "JSEX-SEm1099.js"):
        p = os.path.join(NASA, f)
        if os.path.exists(p):
            for lab, el in parse_jsex(p):
                if years[0] <= lab[0] <= years[1]:
                    out.append((lab, el))
    return out


def main():
    sigma_huber = 1008.0     # s, 5MCSE/Huber model at -1177 (computed)
    rows = []
    for lab, el in load():
        dT0 = el[5]
        best_shift = []
        r0 = local(el, *SITES["Ithaki (Vathy)"])
        # magnitude at Ithaki if dT were shifted by -2..+2 sigma
        lo = local(el, *SITES["Ithaki (Vathy)"], dT=dT0 - 2 * sigma_huber, step_h=1 / 120)
        hi = local(el, *SITES["Ithaki (Vathy)"], dT=dT0 + 2 * sigma_huber, step_h=1 / 120)
        # best magnitude reachable anywhere in +-2 sigma (coarse scan)
        best = 0.0
        for k in range(-20, 21):
            r = local(el, *SITES["Ithaki (Vathy)"], dT=dT0 + k * 0.1 * sigma_huber, step_h=1 / 60)
            best = max(best, r["mag"])
        row = dict(year=lab[0], month=lab[1], day=lab[2], dT_canon=dT0,
                   mag_ithaki=round(r0["mag"], 3), type_ithaki=r0["type"],
                   ut_max=hms(r0["ut"]),
                   lmt_max=hms(None if r0["ut"] is None else (r0["ut"] + 20.717 / 15) % 24),
                   sun_alt=None if r0["alt"] is None else round(r0["alt"], 1),
                   obsc_ithaki=round(r0["obsc"], 3),
                   mag_minus2sig=round(lo["mag"], 3), mag_plus2sig=round(hi["mag"], 3),
                   best_mag_within_2sig=round(best, 3))
        for name, (la, lo_) in SITES.items():
            if name == "Ithaki (Vathy)":
                continue
            row["mag_" + name.split()[0].lower()] = round(local(el, la, lo_)["mag"], 3)
        rows.append(row)
    outp = os.path.join(HERE, "eclipse_ionian.csv")
    with open(outp, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(len(rows), "eclipses written to", outp)


if __name__ == "__main__":
    sys.exit(main())
