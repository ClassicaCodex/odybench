"""
Which solar eclipses of 1300-1050 BC (astronomical -1299 to -1049) reached a
large magnitude in the Ionian islands, and how robust is that to Delta T?

Uses NASA 5MCSE Besselian elements (data/refs/nasa/JSEX-SEm*.js) and the
geometry of eclipse_local.py (checked against NASA's own JavaScript Eclipse
Explorer: identical magnitudes to 3 decimals for every eclipse of -1199..-1100
at Ithaki).  Vectorised over a time grid and a Delta-T grid.

Delta-T prior: the canon's own value (Morrison & Stephenson 2004 parabola
-20+32u^2 plus the canon's ndot correction c = -0.000012932 (y-1955)^2), with
sigma from Huber's Brownian model as used by the canon
(sigma = 365.25 N sqrt((N Q/3)(1+N/M))/1000 s, N = |y+500|, Q = 0.058, M = 2500).
A second prior uses the HMNAO (Stephenson, Morrison & Hohenkerk 2016 / Morrison
et al. 2021) extrapolation, converted to the canon's ndot = -25.858"/cy^2,
with the HMNAO tabulated error (720 s for -1600..-901).

Output: ionian_eclipses.csv and printed summaries.  Times UT; dates are the
canon's (TT) calendar dates, proleptic Julian, astronomical years.
"""
import csv
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eclipse_local as E  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
K = E.K
HORIZON = -0.00524   # rad, NASA JSEX threshold (-0.3 deg)


def huber_sigma(y):
    N = abs(y + 500.0)
    return 365.25 * N * math.sqrt((N * 0.058 / 3) * (1 + N / 2500.0)) / 1000.0


def grid_mag(el, lat_deg, lon_e_deg, dTs, dt_min=1.0):
    """Max magnitude with Sun above horizon, for each dT in dTs (vectorised).
    Returns (mag[nd], type[nd] codes 0 none 1 P 2 A 3 T, t_of_max[nd], alt[nd])."""
    lat = math.radians(lat_deg)
    lonw = -math.radians(lon_e_deg)
    t = np.arange(el[2], el[3] + 1e-9, dt_min / 60.0)[:, None]          # (nt,1)
    dT = np.asarray(dTs, float)[None, :]                                # (1,nd)
    x = ((el[9] * t + el[8]) * t + el[7]) * t + el[6]
    y = ((el[13] * t + el[12]) * t + el[11]) * t + el[10]
    d = np.radians((el[16] * t + el[15]) * t + el[14])
    mu = np.radians((el[19] * t + el[18]) * t + el[17])
    l1 = (el[22] * t + el[21]) * t + el[20]
    l2 = (el[25] * t + el[24]) * t + el[23]
    u_ = math.atan(0.99664719 * math.tan(lat))
    rs, rc = 0.99664719 * math.sin(u_), math.cos(u_)
    h = mu - lonw - dT * K                                              # (nt,nd)
    xi = rc * np.sin(h)
    eta = rs * np.cos(d) - rc * np.cos(h) * np.sin(d)
    zeta = rs * np.sin(d) + rc * np.cos(h) * np.cos(d)
    L1 = l1 - zeta * el[26]
    L2 = l2 - zeta * el[27]
    m = np.hypot(x - xi, y - eta)
    alt = np.arcsin(np.sin(d) * math.sin(lat) + np.cos(d) * math.cos(lat) * np.cos(h))
    partial = (L1 - m) / (L1 + L2)
    central = m < np.abs(L2)
    ratio = (L1 - L2) / (L1 + L2)
    mag = np.where(central, ratio, np.where(m < L1, partial, 0.0))
    mag = np.where(alt > HORIZON, mag, 0.0)
    typ = np.where(mag <= 0, 0, np.where(central, np.where(L2 < 0, 3, 2), 1))
    i = np.argmax(mag, axis=0)
    cols = np.arange(mag.shape[1])
    return mag[i, cols], typ[i, cols], t[i, 0], np.degrees(alt[i, cols])


def total_window(el, lat, lon, dT0, half_width=4000.0, step=2.0):
    """Range of dT (s) for which the site sees totality (Sun up)."""
    dTs = np.arange(dT0 - half_width, dT0 + half_width + 1e-9, step)
    mag, typ, _, _ = grid_mag(el, lat, lon, dTs, dt_min=0.5)
    tot = dTs[typ == 3]
    if len(tot) == 0:
        return None
    return float(tot.min()), float(tot.max())


def p_normal(lo, hi, mu, s):
    from math import erf, sqrt
    F = lambda z: 0.5 * (1 + erf((z - mu) / (s * sqrt(2))))
    return F(hi) - F(lo)


def hmnao_dT(y):
    """HMNAO long-term extrapolation (Morrison et al. 2021, via ytliu0/DeltaT),
    converted to ndot = -25.858 "/cy^2 (canon)."""
    t = 0.01 * (y - 1825)
    c1 = 1.007739546148514
    dt = c1 + 31.4115 * t * t + 284.8435805251424 * math.cos(0.4487989505128276 * (t + 0.75))
    T = 0.01 * y - 19.55
    dalpha = -25.858 - (-25.82)
    return dt - 0.91072 * dalpha * T * T


def main():
    vathy = E.SITES["Ithaki (Vathy)"]
    rows = []
    for lab, el in E.load((-1399, -1000)):
        yfrac = lab[0] + (lab[1] - 0.5) / 12.0
        dT0 = el[5]
        s = huber_sigma(yfrac)
        dTs = dT0 + s * np.linspace(-2, 2, 81)
        mag, typ, tmax, alt = grid_mag(el, *vathy, dTs)
        nominal = grid_mag(el, *vathy, [dT0], dt_min=0.1)
        p_gt08 = float(np.mean(mag > 0.8))   # crude: fraction of a uniform +-2 sigma grid
        # Gaussian-weighted probability that mag > 0.8
        w = np.exp(-0.5 * np.linspace(-2, 2, 81) ** 2)
        pg = float(np.sum(w * (mag > 0.8)) / np.sum(w))
        pt = float(np.sum(w * (typ == 3)) / np.sum(w))
        ut = (el[1] + nominal[2][0] - dT0 / 3600.0) % 24.0
        rows.append(dict(
            year=lab[0], bc=1 - lab[0], month=lab[1], day=lab[2],
            dT_canon=dT0, sigma_huber=round(s),
            mag_nominal=round(float(nominal[0][0]), 3),
            type_nominal="-PAT"[int(nominal[1][0])],
            ut_max=E.hms(ut) if nominal[0][0] > 0 else "",
            lmt_max=E.hms((ut + vathy[1] / 15.0) % 24) if nominal[0][0] > 0 else "",
            sun_alt=round(float(nominal[3][0]), 1) if nominal[0][0] > 0 else "",
            max_mag_2sig=round(float(mag.max()), 3),
            p_mag_gt_0p8=round(pg, 3), p_total=round(pt, 3),
        ))
    outp = os.path.join(HERE, "ionian_eclipses.csv")
    with open(outp, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print("wrote", outp, len(rows), "eclipses -1399..-1000")

    print("\n== Nominal (canon dT) magnitude > 0.8 at Ithaki (Vathy), 1300-1050 BC ==")
    for r in rows:
        if -1299 <= r["year"] <= -1049 and r["mag_nominal"] > 0.8:
            print(r)
    print("\n== Could exceed 0.8 within +-2 sigma (Huber) but nominal <= 0.8, 1300-1050 BC ==")
    for r in rows:
        if -1299 <= r["year"] <= -1049 and r["mag_nominal"] <= 0.8 and r["max_mag_2sig"] > 0.8:
            print(r)

    print("\n== -1177 Apr 16: Delta-T window for totality, by site ==")
    for lab, el in E.load((-1177, -1177)):
        if lab[1:] != (4, 16):
            continue
        dT0 = el[5]
        y = -1177 + 3.5 / 12
        s_h = huber_sigma(y)
        dT_hm = hmnao_dT(y)
        for name, (la, lo) in E.SITES.items():
            win = total_window(el, la, lo, dT0)
            if win:
                print(f"{name:24s} total for dT in [{win[0]:.0f}, {win[1]:.0f}] s "
                      f"(width {win[1]-win[0]:.0f} s); "
                      f"P(canon, sigma {s_h:.0f}) = {p_normal(*win, dT0, s_h):.3f}; "
                      f"P(HMNAO {dT_hm:.0f}, sigma 720) = {p_normal(*win, dT_hm, 720):.3f}; "
                      f"B&M dT 27602.7 inside? {win[0] <= 27602.7 <= win[1]}")
            else:
                print(name, "never total within +-4000 s")
        print(f"canon dT {dT0}, Huber sigma {s_h:.0f} s ({s_h*15*1.002738/3600:.2f} deg), "
              f"HMNAO dT (ndot -25.858) {dT_hm:.0f} s")


if __name__ == "__main__":
    main()
