"""
Markdown table of every solar eclipse of 1300-1050 BC (astronomical -1299..-1049)
whose magnitude at Ithaki (Vathy, 38.367 N, 20.717 E) exceeds 0.8 at the NASA
5MCSE value of Delta T, or could exceed 0.8 within +-2 sigma (Huber) of it.
Dates are the UT calendar date of local maximum, proleptic Julian.
"""
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eclipse_local as E          # noqa: E402
import ionian_eclipses as I        # noqa: E402


def jd_to_julian(jd):
    z = math.floor(jd + 0.5)
    f = jd + 0.5 - z
    a = z
    b = a + 1524
    c = math.floor((b - 122.1) / 365.25)
    d = math.floor(365.25 * c)
    e = math.floor((b - d) / 30.6001)
    day = b - d - math.floor(30.6001 * e) + f
    mon = e - 1 if e < 14 else e - 13
    yr = c - 4716 if mon > 2 else c - 4715
    return yr, mon, int(day)


MON = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


def main(lo=-1299, hi=-1049):
    lat, lon = E.SITES["Ithaki (Vathy)"]
    print("| UT date (Julian) | BC | type at Ithaki | mag | obsc. | max UT | max LMT | Sun alt | mag range +-2 sigma | P(mag>0.8) | P(total) |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for lab, el in E.load((lo, hi)):
        y = lab[0] + (lab[1] - 0.5) / 12
        s = I.huber_sigma(y)
        z = np.linspace(-2, 2, 81)
        dTs = el[5] + s * z
        mag, typ, _, _ = I.grid_mag(el, lat, lon, dTs)
        w = np.exp(-0.5 * z ** 2)
        r = E.local(el, lat, lon, step_h=1 / 3600)
        if r["mag"] <= 0.8 and mag.max() <= 0.8:
            continue
        # local max time in TT hours from t0 -> JD(UT)
        t_ut = r["ut"]
        day0 = math.floor(el[0] + 0.5) - 0.5          # 0h TT of the day of greatest eclipse
        jd_tt = day0 + (el[1]) / 24.0
        # find t (TT offset) from ut
        t_tt_hours = (t_ut + el[5] / 3600.0)
        # choose the TT day so that it is within 12 h of t0
        jd_tt_local = day0 + t_tt_hours / 24.0
        while jd_tt_local - jd_tt > 0.5:
            jd_tt_local -= 1
        while jd_tt - jd_tt_local > 0.5:
            jd_tt_local += 1
        jd_ut = jd_tt_local - el[5] / 86400.0
        yy, mm, dd = jd_to_julian(jd_ut)
        pg = float(np.sum(w * (mag > 0.8)) / np.sum(w))
        pt = float(np.sum(w * (typ == 3)) / np.sum(w))
        lmt = (t_ut + lon / 15.0) % 24
        print(f"| {yy} {MON[mm-1]} {dd:02d} | {1-yy} | {'PAT'['PAT'.index(r['type'])] if r['type'] in 'PAT' else '-'} "
              f"| {r['mag']:.3f} | {r['obsc']:.3f} | {E.hms(t_ut)} | {E.hms(lmt)} | {r['alt']:.0f} "
              f"| {mag.min():.2f}-{mag.max():.2f} | {pg:.2f} | {pt:.2f} |")


if __name__ == "__main__":
    main()
