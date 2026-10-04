"""Rough post-freeze check of the accepted dates against the frozen clue file.

Written AFTER data/prereg/controls_real.json was hashed (see
clue_file_sha256.txt). Uses odybench.ephem (DE441, SMH2020 Delta-T).
The lunar-eclipse part is a quick geocentric Danjon-style model written here
(shadow enlargement factor 1.01, as in Espenak & Meeus' canon); it is NOT the
bench's lunar module (instrument check I4 has not been run), so its umbral
magnitudes are good to a few hundredths, and its times to a few minutes plus
the Delta-T uncertainty.

    cd C:\\Projects\\odybench && py results/controls-real-drafting/check_truth.py
"""
import math
import sys

import numpy as np
from scipy.optimize import brentq, minimize_scalar

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2]))
from odybench import ephem as E  # noqa: E402

R_EARTH = E.EARTH_EQ_RADIUS_KM
R_SUN = E.SUN_RADIUS_KM
R_MOON = 0.2725076 * R_EARTH


def ecl_lonlat(jd_tt, body):
    """Geocentric apparent ecliptic longitude/latitude of date (deg)."""
    t = E.time_tt(jd_tt, 0.0)
    k = E.kernel(t.tt, ("sun", "moon", "earth"))
    v = k["earth"].at(t).observe(k[body]).apparent(deflectors=(10,)).xyz.km
    x, y, z = np.einsum("ij...,j...->i...", t.M, v)
    eps = E.mean_obliquity(t.tt) + t._nutation_angles_radians[1]
    yl = y * np.cos(eps) + z * np.sin(eps)
    zl = -y * np.sin(eps) + z * np.cos(eps)
    lon = np.degrees(np.arctan2(yl, x)) % 360.0
    lat = np.degrees(np.arctan2(zl, np.hypot(x, yl)))
    return float(lon), float(lat), float(np.linalg.norm(v))


def shadow(jd_tt):
    """(sigma, rho_u, rho_p, s_moon) in degrees, geocentric."""
    t = E.time_tt(jd_tt, 0.0)
    k = E.kernel(t.tt, ("sun", "moon", "earth"))
    e = k["earth"].at(t)
    vs = e.observe(k["sun"]).apparent(deflectors=(10,)).xyz.km
    vm = e.observe(k["moon"]).apparent(deflectors=(10,)).xyz.km
    ds, dm = np.linalg.norm(vs), np.linalg.norm(vm)
    sig = math.degrees(math.acos(np.clip(np.dot(vm, -vs) / (ds * dm), -1, 1)))
    pm = math.degrees(math.asin(R_EARTH / dm))
    ps = math.degrees(math.asin(R_EARTH / ds))
    ss = math.degrees(math.asin(R_SUN / ds))
    sm = math.degrees(math.asin(R_MOON / dm))
    return sig, 1.01 * pm - ss + ps, 1.01 * pm + ss + ps, sm


def lunar(jd_guess_tt):
    """Greatest eclipse (min sigma) near guess; magnitudes and umbral contacts."""
    hrs = np.linspace(-30, 30, 241)
    s = [shadow(jd_guess_tt + h / 24)[0] for h in hrs]
    i = int(np.argmin(s))
    f = lambda h: shadow(jd_guess_tt + h / 24)[0]
    h0 = minimize_scalar(f, bounds=(hrs[max(i - 1, 0)], hrs[min(i + 1, 240)]),
                         method="bounded", options={"xatol": 1e-5}).x
    jg = jd_guess_tt + h0 / 24
    sig, ru, rp, sm = shadow(jg)
    umag = (ru + sm - sig) / (2 * sm)
    pmag = (rp + sm - sig) / (2 * sm)
    g = lambda h: (lambda q: q[0] - (q[1] + q[3]))(shadow(jg + h / 24))
    u1 = u4 = None
    if umag > 0:
        u1 = jg + brentq(g, -4, 0) / 24
        u4 = jg + brentq(g, 0, 4) / 24
    return dict(jd_tt=jg, umag=umag, pmag=pmag, u1=u1, u4=u4,
                moon_lat=ecl_lonlat(jg, "moon")[1], sun_lon=ecl_lonlat(jg, "sun")[0])


def ut(jd_tt):
    return float(E.time_tt(jd_tt).ut1)


def sun_events(lat, lon, jd_ut_mid):
    """Sunset before and sunrise after jd_ut_mid (UT JD), airless -0.833 deg."""
    grid = jd_ut_mid + np.arange(-16 * 60, 16 * 60 + 1, 2) / 1440.0
    alt = np.array([E.altaz("sun", x, lat, lon)[0] for x in grid]) + 0.833
    ss = sr = None
    for j in range(len(grid) - 1):
        if alt[j] > 0 >= alt[j + 1] and grid[j] <= jd_ut_mid:
            ss = grid[j]
        if alt[j] <= 0 < alt[j + 1] and grid[j] >= jd_ut_mid and sr is None:
            sr = grid[j]
    return ss, sr


def moonrise_before(lat, lon, jd_ut):
    grid = jd_ut + np.arange(-14 * 60, 1, 2) / 1440.0
    alt = np.array([E.altaz("moon", x, lat, lon)[0] for x in grid]) + 0.833
    r = None
    for j in range(len(grid) - 1):
        if alt[j] <= 0 < alt[j + 1]:
            r = grid[j]
    return r


def fmt_h(x):
    return "None" if x is None else f"{x:+.2f} h"


SITES = {"Babylon": (32.54, 44.42), "Alexandria": (31.20, 29.92), "Syracuse": (37.07, 15.29),
         "Athens": (37.97, 23.72), "Arbela": (36.19, 44.01), "TigrisCamp": (36.5, 43.0),
         "Pydna": (40.37, 22.60), "Rome": (41.89, 12.49), "Cumae": (40.85, 14.05),
         "Sardinia(Carales)": (39.22, 9.11), "Pherae": (39.5, 22.6), "Boeotia": (38.5, 22.85),
         "Larisa": (39.64, 22.42)}


def report_lunar(label, y, m, d, sites):
    jg = E.jd_from_julian(y, m, d, 0.0)
    L = lunar(jg)
    print(f"\n== {label}: greatest {E.fmt_jd(L['jd_tt'], 'TT')}  UT {E.fmt_jd(ut(L['jd_tt']))}")
    print(f"   umag {L['umag']:.3f}  pmag {L['pmag']:.3f}  Moon ecl. lat {L['moon_lat']:+.3f} deg  "
          f"Sun lon {L['sun_lon']:.2f} deg")
    for s in sites:
        la, lo = SITES[s]
        jm = ut(L["jd_tt"])
        lat_mid = E.local_apparent_solar_time(jm, la, lo)
        ss, sr = sun_events(la, lo, jm)
        night = (sr - ss) * 24 if (ss and sr) else None
        def hrs_after_sunset(j):
            return None if (j is None or ss is None) else (ut(j) - ss) * 24 if isinstance(j, float) and j > 1e6 else None
        alt_mid = E.altaz("moon", jm, la, lo)[0]
        out = [f"   {s}: mid LAT {lat_mid:5.2f} h (from midnight {((lat_mid + 12) % 24) - 12:+.2f} h); "
               f"Moon alt at mid {alt_mid:5.1f}"]
        if ss and sr:
            seas = 12.0 / night
            mid_after = (jm - ss) * 24
            out.append(f"night {night:.2f} h; mid {mid_after:.2f} h after sunset = seasonal hour "
                       f"{mid_after * seas + 1:.2f}")
            if L["u1"]:
                u1a, u4a = (ut(L["u1"]) - ss) * 24, (ut(L["u4"]) - ss) * 24
                a1 = E.altaz("moon", ut(L["u1"]), la, lo)[0]
                a4 = E.altaz("moon", ut(L["u4"]), la, lo)[0]
                out.append(f"U1 {u1a:.2f} h after sunset (seasonal {u1a * seas + 1:.2f}, Moon alt {a1:.1f}); "
                           f"U4 {u4a:.2f} h (seasonal {u4a * seas + 1:.2f}, Moon alt {a4:.1f})")
                mr = moonrise_before(la, lo, ut(L["u1"]))
                if mr:
                    out.append(f"moonrise {(ut(L['u1']) - mr) * 24:.2f} h before U1")
        print("; ".join(out))
    return L


def report_solar(label, y, m, d, sites):
    jg = E.jd_from_julian(y, m, d, 12.0)
    nm = E.new_moons(jg - 2, jg + 2)
    if not nm:
        print(f"\n== {label}: no conjunction within 2 days of {y}-{m}-{d}")
        return
    j = nm[0]
    sl = ecl_lonlat(j, "sun")[0]
    print(f"\n== {label}: conjunction {E.fmt_jd(j, 'TT')}  Sun lon {sl:.2f} deg")
    for s in sites:
        la, lo = SITES[s]
        lc = E.local_circumstances(la, lo, j)
        if lc["magnitude"] <= 0:
            print(f"   {s}: no eclipse (min sep {lc['min_sep_arcsec']:.0f}\")")
            continue
        jm = lc["jd_ut_max"]
        grid = jm + np.arange(-16 * 60, 16 * 60 + 1, 2) / 1440.0
        alt = np.array([E.altaz("sun", x, la, lo)[0] for x in grid]) + 0.833
        rise = [grid[q] for q in range(len(grid) - 1) if alt[q] <= 0 < alt[q + 1] and grid[q] <= jm]
        sset = [grid[q] for q in range(len(grid) - 1) if alt[q] > 0 >= alt[q + 1] and grid[q] >= jm]
        if rise and sset:
            day = (sset[0] - rise[-1]) * 24
            print(f"   {s}: sunrise->max {(jm - rise[-1]) * 24:.2f} h, day {day:.2f} h, "
                  f"max in seasonal day hour {(jm - rise[-1]) * 24 * 12 / day + 1:.2f}")
        print(f"   {s}: mag {lc['magnitude']:.3f} total={lc['total']} annular={lc['annular']} "
              f"max LAT {lc['lat_hours']:.2f} h  Sun alt {lc['sun_alt_deg']:.1f}  "
              f"c1 LAT {E.local_apparent_solar_time(ut(lc['c1']), la, lo) if lc['c1'] else float('nan'):.2f}  "
              f"c4 LAT {E.local_apparent_solar_time(ut(lc['c4']), la, lo) if lc['c4'] else float('nan'):.2f}  "
              f"Sun alt c4 {E.altaz('sun', ut(lc['c4']), la, lo)[0] if lc['c4'] else float('nan'):.1f}")


if __name__ == "__main__":
    # Ptolemy, Babylonian triple
    report_lunar("PB E1", -720, 3, 19, ["Babylon"])
    report_lunar("PB E2", -719, 3, 8, ["Babylon"])
    report_lunar("PB E3", -719, 9, 1, ["Babylon"])
    # Ptolemy, Alexandrian triple
    report_lunar("PA H1", 133, 5, 6, ["Alexandria"])
    report_lunar("PA H2", 134, 10, 20, ["Alexandria"])
    report_lunar("PA H3", 136, 3, 5, ["Alexandria"])
    # Thucydides
    report_solar("T1 Thuc 2.28", -430, 8, 3, ["Athens"])
    report_solar("T2 Thuc 4.52 (Mar)", -423, 3, 21, ["Athens"])
    report_lunar("T3 Thuc 7.50", -412, 8, 27, ["Syracuse"])
    # Xenophon
    report_lunar("X1 Hell 1.6.1", -405, 4, 15, ["Athens"])
    report_solar("X2 Hell 2.3.4", -403, 9, 3, ["Athens", "Pherae"])
    report_solar("X3 Hell 4.3.10", -393, 8, 14, ["Boeotia"])
    # Arbela
    report_lunar("A1 Arbela", -330, 9, 20, ["Arbela", "TigrisCamp", "Syracuse"])
    # Pydna
    report_lunar("P1 Pydna", -167, 6, 21, ["Pydna"])
    # Diodorus
    report_solar("D1 Diod 20.5.5", -309, 8, 15, ["Syracuse"])
    # Livy
    report_solar("L1 Livy 22.1.9", -216, 2, 11, ["Rome", "Sardinia(Carales)"])
    report_solar("L2 Livy 30.38.8", -202, 5, 6, ["Cumae"])
    report_solar("L3 Livy 37.4.4", -189, 3, 14, ["Rome"])
    report_solar("L4 Livy 38.36.4", -187, 7, 17, ["Rome"])
