"""Round-1 review of DESIGN.md rev 2: how often does a spring daylight new moon
have every slot the PC-S science-mode generator requires (DESIGN 6.2 step 2)?

Why: in science mode the poem's slots and stated offsets are the Odyssey's
for every accepted truth, so the readings' survivor sets are the Odyssey's and
R_obs = E[reach(t) | A(t)] over spring targets, while G = E[reach(t)].  Hence
LR = R_obs / G = E[reach * 1_A] / (P(A) E[reach]) <= 1 / P(A), whatever the
data.  This script estimates P(A) at zero jitter (j = 0, s_M = 0).

Slots, operationalised conservatively (each choice makes P(A) smaller, so the
cap 1/P(A) is if anything overstated):
  Venus  (Day -5, sequential landing day): Venus rises before the Sun and the
         Sun is at or below -7 deg when Venus rises (AV 7 deg).
  Mercury (Day -34): within 6 d of a MORNING event (rise-azimuth maximum,
         greatest western elongation, station while west of the Sun), or a
         visible morning object (Sun <= -10 deg at Mercury's rising).
  Season: true by construction for truths passing C (Pleiades and Bootes are
         co-visible at dusk on the raft nights inside the C bounds).
  Day 0: a conjunction.
Pool: conjunctions in -1499..-1000 (500 Julian years) whose UT+2 civil date
passes B&M's fixed C bounds (Ti-29 >= 17 Feb, Ti-12 <= 4 Apr, same Julian
year; the C_rel calibration makes these identical at -1177), at Ithaki
38.37 N 20.72 E, SMH2020 Delta-T; "daylight" = Sun's centre above -0.8333 deg
at the conjunction instant.
Also reported: B&M's own V (lead >= 90 min) and M (|Delta| <= 1 d to the
rise-azimuth maximum, approximated from the declination at 03:00 UT) pass
rates, to compare with the dossier's p_fix|C of about 0.008 [vis 5].

Approximations: rise azimuth extremum from the declination series (rise
azimuth = arccos(sin dec / cos lat)), good to about 1 d; rises from a 3-min
altitude grid with linear interpolation.  Neither matters at a 6-day
tolerance.  Run: cd C:/Projects/odybench && py results/critique-design-r1/check_lr_cap.py
"""
import sys
import numpy as np

sys.path.insert(0, ".")
from odybench import ephem, calendar as cal  # noqa: E402

LAT, LON = 38.37, 20.72
H0_SUN, H0_PL = -0.8333, -0.5667


def dt_s(jd_tt):
    return float(ephem.delta_t(cal.julian_epoch(jd_tt), "smh2020"))


def ecl_lon_dec(body, jd_tt):
    """Geocentric apparent ecliptic longitude (deg) and declination of date."""
    jd_tt = np.atleast_1d(jd_tt)
    t = ephem.time_tt(jd_tt, 0.0)
    k = ephem.kernel(t.tt, ("sun", "earth", body))
    e = k["earth"].at(t)
    eps = ephem.mean_obliquity(t.tt) + t._nutation_angles_radians[1]
    v = e.observe(k[ephem.BODY_NAMES[body]] if body in ephem.BODY_NAMES else k[body]).apparent(deflectors=(10,)).xyz.au
    x, y, z = np.einsum("ij...,j...->i...", t.M, v)
    yl = y * np.cos(eps) + z * np.sin(eps)
    lon = np.degrees(np.arctan2(yl, x)) % 360.0
    dec = np.degrees(np.arctan2(z, np.hypot(x, y)))
    return lon, dec


def morning_rise(body, jdn_ut2, h0):
    """Rise of `body` and of the Sun on the UT+2 civil day jdn (00-09 h UT+2).
    Returns (body_rise_ut, sun_rise_ut, sun_alt_at_body_rise)."""
    jd0_ut = jdn_ut2 - 0.5 - 2.0 / 24.0          # 00:00 UT+2 in UT
    grid = jd0_ut + np.arange(0, 9 * 60 + 1, 3) / 1440.0
    ab, _ = ephem.altaz(body, grid, LAT, LON)
    asun, _ = ephem.altaz("sun", grid, LAT, LON)
    ab, asun = np.asarray(ab), np.asarray(asun)

    def first_up(a, h):
        idx = np.nonzero((a[:-1] < h) & (a[1:] >= h))[0]
        if len(idx) == 0:
            return None, None
        i = idx[0]
        f = (h - a[i]) / (a[i + 1] - a[i])
        return grid[i] + f * (grid[i + 1] - grid[i]), (i, f)

    tb, ib = first_up(ab, h0)
    ts, _ = first_up(asun, H0_SUN)
    if tb is None or ts is None:
        return None, ts, None
    i, f = ib
    sun_at = asun[i] + f * (asun[i + 1] - asun[i])
    return tb, ts, sun_at


def main():
    y0, y1 = -1499, -1000
    jd_a = cal.jd_from_julian(y0, 1, 1) - 40
    jd_b = cal.jd_from_julian(y1 + 1, 1, 1)
    conj_tt = []
    step = 365.25 * 50
    a = jd_a
    while a < jd_b:
        b = min(a + step, jd_b)
        conj_tt += ephem.new_moons(a, b)
        a = b
    conj_tt = sorted(set(round(x, 6) for x in conj_tt))
    rows = []
    for jt in conj_tt:
        ju = jt - dt_s(jt) / 86400.0
        jdn = cal.jdn_of_instant(ju, offset_hours=2.0)
        y, m, d = cal.julian_from_jdn(jdn)
        if not (y0 <= y <= y1):
            continue
        lo = cal.jdn_from_julian(y, 2, 17)
        hi = cal.jdn_from_julian(y, 4, 4)
        if not (jdn - 29 >= lo and jdn - 12 <= hi):
            continue
        rows.append((jt, ju, jdn, y, m, d))
    print(f"spring conjunctions (fixed C bounds) in {y0}..{y1}: {len(rows)}")

    out = []
    for jt, ju, jdn, y, m, d in rows:
        sun_alt_conj = float(ephem.altaz("sun", ju, LAT, LON)[0])
        day = sun_alt_conj > H0_SUN
        # Venus on Day -5
        vr, sr, sun_at_v = morning_rise("venus", jdn - 5, H0_PL)
        lead = (sr - vr) * 1440.0 if (vr is not None and sr is not None) else -999.0
        venus_vis = (vr is not None and lead > 0 and sun_at_v <= -7.0)
        bm_v = lead >= 90.0
        # Mercury series around Day -34 (daily at 03:00 UT)
        days = np.arange(-34 - 10, -34 + 11)
        jd_series_ut = (jdn + days) - 0.5 + 3.0 / 24.0
        jd_series_tt = jd_series_ut + dt_s(jt) / 86400.0
        lm, dm = ecl_lon_dec("mercury", jd_series_tt)
        ls, _ = ecl_lon_dec("sun", jd_series_tt)
        el = (lm - ls + 180.0) % 360.0 - 180.0            # east positive
        az = np.degrees(np.arccos(np.clip(np.sin(np.radians(dm)) / np.cos(np.radians(LAT)), -1, 1)))
        dlon = (np.diff(lm) + 180.0) % 360.0 - 180.0
        ev = []
        for i in range(1, len(days) - 1):
            west = el[i] < 0
            if west and az[i] >= az[i - 1] and az[i] > az[i + 1]:
                ev.append(("mwra", days[i]))
            if west and el[i] <= el[i - 1] and el[i] < el[i + 1]:
                ev.append(("gwe", days[i]))
        for i in range(len(dlon) - 1):
            if np.sign(dlon[i]) != np.sign(dlon[i + 1]) and el[i + 1] < 0:
                ev.append(("station", days[i + 1]))
        near6 = any(abs(dd + 34) <= 6 for _, dd in ev)
        bm_m = any(k == "mwra" and abs(dd + 34) <= 1 for k, dd in ev)
        mr, _, sun_at_m = morning_rise("mercury", jdn - 34, H0_PL)
        msr = morning_rise("sun", jdn - 34, H0_SUN)[0]
        merc_vis = (mr is not None and msr is not None and mr < msr and sun_at_m is not None and sun_at_m <= -10.0)
        merc_slot = near6 or merc_vis
        out.append((y, m, d, day, venus_vis, merc_slot, near6, merc_vis, bm_v, bm_m, lead))

    arr = np.array([(o[3], o[4], o[5], o[6], o[7], o[8], o[9]) for o in out], dtype=bool)
    dayc, vv, ms, n6, mv, bv, bmm = arr.T

    def rep(mask, label):
        n = int(mask.sum())
        A = vv & ms
        pa = (A & mask).sum() / n
        print(f"\n{label}: n = {n}")
        print(f"  Venus slot (visible morning star AV 7, Day -5): {(vv & mask).sum()/n:.3f}")
        print(f"  Mercury slot (6 d of morning event, or visible, Day -34): {(ms & mask).sum()/n:.3f}"
              f"   [event-only {(n6 & mask).sum()/n:.3f}; visible-only {(mv & mask).sum()/n:.3f}]")
        print(f"  P(A) = P(Venus slot and Mercury slot) = {pa:.3f}  ->  LR cap 1/P(A) = {1/pa:.1f}")
        se = np.sqrt(pa * (1 - pa) / n)
        print(f"  binomial 95% for P(A): [{pa-1.96*se:.3f}, {pa+1.96*se:.3f}] -> cap in [{1/(pa+1.96*se):.1f}, {1/max(pa-1.96*se,1e-9):.1f}]")
        print(f"  B&M V (lead >= 90 min): {(bv & mask).sum()/n:.3f};  B&M M approx (|D| <= 1 to MWRA): {(bmm & mask).sum()/n:.3f};"
              f"  V and M: {(bv & bmm & mask).sum()}/{n}")
        print(f"  share of B&M V-and-M passers that satisfy A: {((bv & bmm & A & mask).sum())}/{(bv & bmm & mask).sum()}")

    rep(np.ones(len(arr), bool), "all spring conjunctions")
    rep(dayc, "spring DAYLIGHT conjunctions (the pool of R_obs and G)")
    with open("results/critique-design-r1/check_lr_cap.rows.tsv", "w", encoding="utf-8") as f:
        f.write("year\tmonth\tday\tdaylight\tvenus_slot\tmercury_slot\tmerc_event6\tmerc_visible\tbm_V\tbm_M\tlead_min\n")
        for o in out:
            f.write("\t".join(str(x) for x in o[:10]) + f"\t{o[10]:.1f}\n")


if __name__ == "__main__":
    main()
