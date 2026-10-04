"""Round-2 review of DESIGN.md rev 3: a rough, independent estimate of the rule
quantity G_BM = G(G_BM*; T_A; W = 136 yr) and of what it implies for outcome 1,
before any bench code exists.

Why: G_BM is a property of the garden G_BM* and of Ithaca's sky alone. It does
not depend on whether 16 Apr -1177 passes anything (that target is excluded).
So its size is fixed before the bench runs, and the rule's thresholds
(outcome 1 needs G_BM,hi <= 0.05; outcome 2 needs G_BM,lo >= 0.20) are either
already met or already missed. This script estimates it from the sky.

What it builds (DESIGN rev 3 sections 3.2, 4.2, 4.5, 5.3):
  * conjunctions (DE431-free here: ephem.new_moons on DE441, SMH2020 Delta-T),
    Day 0 = UT+2 civil date (F2 (a));
  * C_rel: A(y) = first evening Arcturus >= h_A at the end of evening nautical
    twilight (Sun -12 deg), P(y) = last evening Alcyone >= h_P; h_A, h_P are
    calibrated so that A(-1177) = 17 Feb and P(-1177) = 4 Apr (midpoints);
    sequential C: Ti-29 >= A, Ti-12 <= P; parallel: Ti-28 >= A, Ti-11 <= P;
  * the 36 readings of G_BM*: day count {seq: V on -5, M on -34; par: -4, -33}
    x Mercury event {rise-azimuth maximum, greatest western elongation,
    morning station} x tolerance {1.5, 2.5, 3.5} d (continuous) x visibility
    {off, Sun <= -10 deg at Mercury's rising}; V = Venus rises >= 90 min
    before the Sun;
  * T_A: daylight conjunctions (Sun's centre above -0.8333 deg at Ithaki) in
    T_C (C_rel seq or par) whose Venus slot (Venus rises before the Sun with
    the Sun <= -7 deg) and Mercury slot (within 6.0 d of a morning event of
    the three kinds, or visible at AV 10) hold on the same day count;
  * reach_136 of every T_A target as |union of I_r(t)| / W, and G with the
    Fay-Feuer gamma interval exactly as DESIGN 5.3 writes it.
Approximations (each stated in the output):
  * rises from a 3-min altitude grid, linear interpolation (as r1);
  * Mercury events from a daily series at 03:30 UT: rise azimuth from the
    declination, cos A = (sin d - sin phi sin h0)/(cos phi cos h0), whose
    extremum is the declination extremum; vertex of a 3-point parabola;
    station from the zero of the daily longitude change, interpolated;
  * one site (Ithaki 38.37 N, 20.72 E), sea level, airless.
Span: conjunctions -1760..-640; targets in -1623..-777 (136-yr margins).
Run: cd C:/Projects/odybench && py results/critique-design-r2/check_gbm.py
"""
import sys
import json
import numpy as np
from multiprocessing import Pool

sys.path.insert(0, ".")
from odybench import ephem, calendar as cal  # noqa: E402

LAT, LON = 38.37, 20.72
H0_SUN, H0_PL = -0.8333, -0.5667
Y0, Y1 = -1760, -640
CORE = None   # (first, last) target years; default: 136-yr margins
import os
if os.environ.get("GBM_FULL"):
    Y0, Y1, CORE = -1999, 200, (-1748, -51)
W_YR = 136
W = W_YR * 365.25
LMT_H = LON / 15.0
OUT = "results/critique-design-r2/check_gbm" + ("_full" if os.environ.get("GBM_FULL") else "")


def dt_s(jd_tt):
    return float(ephem.delta_t(cal.julian_epoch(jd_tt), "smh2020"))


# ---------------------------------------------------------------- conjunctions
def nm_chunk(args):
    a, b = args
    return ephem.new_moons(a, b)


# ---------------------------------------------------------------- C_rel
def dusk_alts(y):
    """Arcturus and Alcyone altitude at the end of evening nautical twilight,
    for every evening 20 Jan .. 30 Apr of Julian year y. Returns (jdn[], arc[], alc[])."""
    j0 = cal.jdn_from_julian(y, 1, 20)
    j1 = cal.jdn_from_julian(y, 4, 30)
    jdns = np.arange(j0, j1 + 1)
    steps = np.arange(0, 211, 5) / 1440.0                      # 17:00 .. 20:30 LMT
    base = jdns - 0.5 + (17.0 - LMT_H) / 24.0
    grid = (base[:, None] + steps[None, :]).ravel()
    alt, _ = ephem.altaz("sun", grid, LAT, LON)
    alt = np.asarray(alt).reshape(len(jdns), len(steps))
    t12 = np.empty(len(jdns))
    for i in range(len(jdns)):
        a = alt[i]
        idx = np.nonzero((a[:-1] > -12.0) & (a[1:] <= -12.0))[0]
        k = idx[0]
        f = (a[k] + 12.0) / (a[k] - a[k + 1])
        t12[i] = base[i] + (steps[k] + f * (steps[k + 1] - steps[k]))
    arc, _ = ephem.altaz("arcturus", t12, LAT, LON)
    alc, _ = ephem.altaz("alcyone", t12, LAT, LON)
    return y, jdns, np.asarray(arc), np.asarray(alc)


# ---------------------------------------------------------------- per candidate
def morning_rise(body, jdn_ut2, h0):
    """(body rise UT, Sun rise UT, Sun alt at body rise) on UT+2 civil day jdn, 00-09 h UT+2."""
    jd0_ut = jdn_ut2 - 0.5 - 2.0 / 24.0
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
    return tb, ts, asun[i] + f * (asun[i + 1] - asun[i])


def ecl_lon_dec(body, jd_tt):
    jd_tt = np.atleast_1d(jd_tt)
    t = ephem.time_tt(jd_tt, 0.0)
    k = ephem.kernel(t.tt, ("sun", "earth", body))
    e = k["earth"].at(t)
    eps = ephem.mean_obliquity(t.tt) + t._nutation_angles_radians[1]
    v = e.observe(k[ephem.BODY_NAMES[body]]).apparent(deflectors=(10,)).xyz.au
    x, y, z = np.einsum("ij...,j...->i...", t.M, v)
    yl = y * np.cos(eps) + z * np.sin(eps)
    lon = np.degrees(np.arctan2(yl, x)) % 360.0
    dec = np.degrees(np.arctan2(z, np.hypot(x, y)))
    return lon, dec


def vertex(y, i):
    d = y[i - 1] - 2 * y[i] + y[i + 1]
    return 0.0 if d == 0 else 0.5 * (y[i - 1] - y[i + 1]) / d


def candidate(args):
    jt, ju, jdn = args
    dts = dt_s(jt)
    out = {"jt": jt, "jdn": jdn}
    out["day"] = bool(float(ephem.altaz("sun", ju, LAT, LON)[0]) > H0_SUN)
    for vd in (-5, -4):
        vr, sr, sa = morning_rise("venus", jdn + vd, H0_PL)
        lead = (sr - vr) * 1440.0 if (vr is not None and sr is not None) else -999.0
        out[f"lead{vd}"] = lead
        out[f"vslot{vd}"] = bool(vr is not None and lead > 0 and sa <= -7.0)
    for md in (-34, -33):
        mr, msr, sa = morning_rise("mercury", jdn + md, H0_PL)
        vis = bool(mr is not None and msr is not None and mr < msr and sa is not None and sa <= -10.0)
        out[f"mvis{md}"] = vis
        # instant of Mercury's rising on that day, in days since 00:00 UT+2 of Ti
        if mr is not None:
            out[f"mrise{md}"] = (mr + 2.0 / 24.0 + 0.5) - jdn
        else:
            out[f"mrise{md}"] = md + 5.5 / 24.0
    # daily Mercury series, days -52..-15, at 03:30 UT (05:30 UT+2)
    days = np.arange(-52, -14)
    frac = 5.5 / 24.0
    jd_ut = (jdn + days) - 0.5 - 2.0 / 24.0 + frac
    jd_tt = jd_ut + dts / 86400.0
    lm, dm = ecl_lon_dec("mercury", jd_tt)
    ls, _ = ecl_lon_dec("sun", jd_tt)
    el = (lm - ls + 180.0) % 360.0 - 180.0
    phi, h0 = np.radians(LAT), np.radians(H0_PL)
    cosA = (np.sin(np.radians(dm)) - np.sin(phi) * np.sin(h0)) / (np.cos(phi) * np.cos(h0))
    az = np.degrees(np.arccos(np.clip(cosA, -1, 1)))
    dlon = (np.diff(lm) + 180.0) % 360.0 - 180.0
    ev = {"mwra": [], "gwe": [], "station": []}
    for i in range(1, len(days) - 1):
        if el[i] < 0 and az[i] >= az[i - 1] and az[i] > az[i + 1]:
            ev["mwra"].append(days[i] + frac + vertex(az, i))
        if el[i] < 0 and el[i] <= el[i - 1] and el[i] < el[i + 1]:
            ev["gwe"].append(days[i] + frac + vertex(el, i))
    for i in range(len(dlon) - 1):
        if np.sign(dlon[i]) != np.sign(dlon[i + 1]) and el[i + 1] < 0:
            # dlon[i] is the change from day i to i+1, centred at i+0.5
            f = dlon[i] / (dlon[i] - dlon[i + 1])
            out_t = days[i] + 0.5 + f + frac
            ev["station"].append(out_t)
    for md in (-34, -33):
        t_m = out[f"mrise{md}"]
        for k, lst in ev.items():
            out[f"d_{k}{md}"] = min((abs(t_m - x) for x in lst), default=99.0)
    return out


def gamma_ci(reaches, n):
    from scipy.stats import chi2
    r = np.asarray(reaches, float)
    y = r.sum() / n
    v = ((r / n) ** 2).sum()
    w = 1.0 / n
    hi = (v + w * w) / (2 * (y + w)) * chi2.ppf(0.975, 2 * (y + w) ** 2 / (v + w * w))
    lo = 0.0 if y == 0 else v / (2 * y) * chi2.ppf(0.025, 2 * y * y / v)
    return y, lo, hi


def main():
    jd_a = cal.jd_from_julian(Y0, 1, 1) - 40
    jd_b = cal.jd_from_julian(Y1 + 1, 1, 1)
    chunks = []
    a = jd_a
    while a < jd_b:
        b = min(a + 365.25 * 20, jd_b)
        chunks.append((a, b))
        a = b
    with Pool(14) as pool:
        nm = pool.map(nm_chunk, chunks)
        conj = sorted(set(round(x, 6) for c in nm for x in c))
        print(f"conjunctions {Y0}..{Y1}: {len(conj)}", flush=True)
        years = list(range(Y0, Y1 + 1))
        sb = pool.map(dusk_alts, years)
    sbd = {y: (j, arc, alc) for y, j, arc, alc in sb}
    j, arc, alc = sbd[-1177]
    i17 = int(np.nonzero(j == cal.jdn_from_julian(-1177, 2, 17))[0][0])
    i4 = int(np.nonzero(j == cal.jdn_from_julian(-1177, 4, 4))[0][0])
    h_A = 0.5 * (arc[i17 - 1] + arc[i17])
    h_P = 0.5 * (alc[i4] + alc[i4 + 1])
    print(f"C_rel calibration at -1177: Arcturus {arc[i17-1]:.3f} -> {arc[i17]:.3f} deg (h_A {h_A:.3f}); "
          f"Alcyone {alc[i4]:.3f} -> {alc[i4+1]:.3f} deg (h_P {h_P:.3f})")
    A, P = {}, {}
    for y, (jj, ar, al) in sbd.items():
        ia = np.nonzero(ar >= h_A)[0]
        ip = np.nonzero(al >= h_P)[0]
        A[y] = int(jj[ia[0]]) if len(ia) else None
        # last evening (in March-April) with Alcyone >= h_P
        mar = jj >= cal.jdn_from_julian(y, 3, 1)
        ipm = np.nonzero((al >= h_P) & mar)[0]
        P[y] = int(jj[ipm[-1]]) if len(ipm) else None
    for y in (-1700, -1177, -700):
        print(f"  A({y}) = {cal.julian_from_jdn(A[y])}, P({y}) = {cal.julian_from_jdn(P[y])}")

    cands = []
    for jt in conj:
        ju = jt - dt_s(jt) / 86400.0
        jdn = int(cal.jdn_of_instant(ju, offset_hours=2.0))
        y, m, d = cal.julian_from_jdn(jdn)
        if not (Y0 <= y <= Y1) or A.get(y) is None or P.get(y) is None:
            continue
        cs = (jdn - 29 >= A[y]) and (jdn - 12 <= P[y])
        cp = (jdn - 28 >= A[y]) and (jdn - 11 <= P[y])
        if cs or cp:
            cands.append((jt, ju, jdn, y, cs, cp))
    print(f"spring candidates (C_rel seq or par): {len(cands)}", flush=True)
    with Pool(14) as pool:
        res = pool.map(candidate, [(c[0], c[1], c[2]) for c in cands], chunksize=8)
    rows = []
    for c, r in zip(cands, res):
        r["y"], r["cs"], r["cp"] = c[3], c[4], c[5]
        rows.append(r)
    with open(OUT + ".rows.json", "w", encoding="utf-8") as f:
        json.dump(rows, f)
    analyse(rows)


def analyse(rows):
    n = len(rows)
    jt = np.array([r["jt"] for r in rows])
    yy = np.array([r["y"] for r in rows])
    jdn = np.array([r["jdn"] for r in rows])
    day = np.array([r["day"] for r in rows])
    cs = np.array([r["cs"] for r in rows])
    cp = np.array([r["cp"] for r in rows])
    t_s = cal.jdn_from_julian(-1177, 4, 16)
    is_s = jdn == t_s
    print(f"16 Apr -1177 present: {is_s.sum()}; C seq {cs[is_s]}, C par {cp[is_s]}")

    def f(key):
        return np.array([r[key] for r in rows])

    dc = {"seq": (cs, -5, -34), "par": (cp, -4, -33)}
    # slots, same day count
    slotA = np.zeros(n, bool)
    for name, (c, vd, md) in dc.items():
        merc_ev6 = (f(f"d_mwra{md}") <= 6.0) | (f(f"d_gwe{md}") <= 6.0) | (f(f"d_station{md}") <= 6.0)
        slotA |= c & f(f"vslot{vd}") & (merc_ev6 | f(f"mvis{md}"))
    readings = []
    for name, (c, vd, md) in dc.items():
        for ev in ("mwra", "gwe", "station"):
            for tol in (1.5, 2.5, 3.5):
                for vis in (False, True):
                    p = c & (f(f"lead{vd}") >= 90.0) & (f(f"d_{ev}{md}") <= tol)
                    if vis:
                        p = p & f(f"mvis{md}")
                    readings.append(((name, ev, tol, vis), p))
    # identity check: every survivor of every reading satisfies slot A
    viol = sum(int((p & ~slotA).sum()) for _, p in readings)
    print(f"survivors of any BM reading outside slot A (identity of DESIGN 4.2): {viol}")

    c0, c1 = CORE if CORE else (Y0 + W_YR + 1, Y1 - W_YR - 1)
    core = (yy >= c0) & (yy <= c1)
    TA = day & slotA & core & ~is_s
    TC = day & (cs | cp) & core & ~is_s
    span_core = c1 - c0 + 1
    print(f"core {c0}..{c1} ({span_core} yr): n_TC = {TC.sum()}, n_A = {TA.sum()}, "
          f"P(A|T_C) = {TA.sum()/TC.sum():.3f}")

    def reach_vec(sel_readings, targets_mask):
        idx_t = np.nonzero(targets_mask | is_s)[0]
        lo_hi = {i: [] for i in idx_t}
        for _, p in sel_readings:
            s = np.sort(jt[p])
            for i in idx_t:
                if not p[i]:
                    continue
                k = np.searchsorted(s, jt[i])
                sm = s[k - 1] if k > 0 else -np.inf
                sp = s[k + 1] if k + 1 < len(s) else np.inf
                lo = max(jt[i] - W, sm)
                hi = min(jt[i], sp - W)
                if hi > lo:
                    lo_hi[i].append((lo, hi))
        reach = np.zeros(n)
        for i, iv in lo_hi.items():
            if not iv:
                continue
            iv.sort()
            tot, cur_lo, cur_hi = 0.0, iv[0][0], iv[0][1]
            for lo, hi in iv[1:]:
                if lo > cur_hi:
                    tot += cur_hi - cur_lo
                    cur_lo, cur_hi = lo, hi
                else:
                    cur_hi = max(cur_hi, hi)
            tot += cur_hi - cur_lo
            reach[i] = tot / W
        return reach

    def report(label, sel):
        r = reach_vec(sel, TA)
        vals = r[TA]
        nA = int(TA.sum())
        g, lo, hi = gamma_ci(vals[vals > 0], nA)
        k = int((vals > 0).sum())
        print(f"{label:42s} G {g:.4f}  [{lo:.4f}, {hi:.4f}]  k {k:3d}/{nA}  G_any {k/nA:.3f}  "
              f"reach(16 Apr -1177) {r[is_s][0]:.4f}")
        return r

    print("\nG over T_A (W = 136 yr; Fay-Feuer gamma interval as DESIGN 5.3):")
    t0b = [x for x in readings if x[0] == ("seq", "mwra", 1.5, False)]
    report("T0b reading (seq, MWRA_vtx 1.5 d, vis off)", t0b)
    report("seq, MWRA, all tol and vis (6)", [x for x in readings if x[0][0] == "seq" and x[0][1] == "mwra"])
    report("seq, all events, tol and vis (18)", [x for x in readings if x[0][0] == "seq"])
    rBM = report("G_BM* (36 readings)", readings)
    mid = (c0 + c1) // 2
    for lab, msk in (("first half", yy <= mid), ("second half", yy > mid)):
        sub = TA & msk
        vals = rBM[sub]
        g, lo, hi = gamma_ci(vals[vals > 0], int(sub.sum()))
        print(f"  G_BM* on the {lab} of the core: G {g:.4f} [{lo:.4f}, {hi:.4f}], n {int(sub.sum())}, "
              f"k {int((vals > 0).sum())}")
    r_ody = rBM[is_s][0]
    vals = rBM[TA]
    print(f"  share of T_A targets with reach >= r_Ody ({r_ody:.4f}) under G_BM*: "
          f"{(vals >= r_ody).mean():.3f};  with reach > 0: {(vals > 0).mean():.3f}")
    print(f"  reach distribution of reached T_A targets: "
          f"{np.round(np.sort(vals[vals > 0]), 3).tolist()}")
    gT_C = rBM[TC].sum() / TC.sum()
    n_T_est = 12.3683 * 0.509 * span_core
    print(f"  G_BM* over T_C = {gT_C:.4f};  G_BM,u = (n_A/n_T) G_BM with n_T ~ {n_T_est:.0f}: "
          f"{TA.sum() / n_T_est * vals.sum() / TA.sum():.5f}")
    print("\nper reading: survivors per century (all candidates, day or night), passes in T_A, G alone")
    for key, p in readings:
        r = reach_vec([(key, p)], TA)
        vals = r[TA]
        g = vals.sum() / TA.sum()
        lam = p[(yy >= Y0) & (yy <= Y1)].sum() / ((Y1 - Y0 + 1) / 100.0)
        print(f"  {str(key):34s} lambda {lam:5.2f}/cy  pass(T_A) {int((p & TA).sum()):3d}  "
              f"G {g:.4f}  16 Apr -1177 passes {bool(p[is_s][0])}")
    # B&M V and M rates on P_spring (seq), p_fix|C and the V-M dependence ratio (P7, P8)
    ps = cs & (yy >= Y0) & (yy <= Y1)
    V = f("lead-5") >= 90.0
    M = f("d_mwra-34") <= 1.5
    pv, pm, pvm = (V & ps).sum() / ps.sum(), (M & ps).sum() / ps.sum(), (V & M & ps).sum() / ps.sum()
    print(f"\nP_spring (seq, all candidates) n = {ps.sum()}: P(V) {pv:.3f}, P(M vtx 1.5) {pm:.3f}, "
          f"p_fix|C = P(V and M) {pvm:.4f}, dependence ratio {pvm/(pv*pm):.2f}")
    # BF_BM(rho = 1) (DESIGN 5.7 item 2)
    nA = int(TA.sum())
    bf, bfmax = 0.0, 0.0
    for key, p in readings:
        pr = ((p & TA).sum() + 1) / (nA + 1)
        bfmax += (1 / 36) / pr
        if p[is_s][0]:
            bf += (1 / 36) / pr
    print(f"BF_BM(rho = 1) = {bf:.2f}; BF_max = {bfmax:.2f}")
    # P12: survivors of the T0b reading near 1178 BC
    p0 = t0b[0][1]
    near = np.nonzero(p0 & (yy >= -1260) & (yy <= -1040))[0]
    print("T0b-reading survivors in -1260..-1040 (Day 0, UT+2):",
          [cal.julian_from_jdn(int(jdn[i])) for i in near])
    # P22: mean reach (P(unique)) over T_A truths passing the T0b reading
    r0 = reach_vec(t0b, TA)
    sel = TA & p0
    print(f"P22: mean P(unique) of T0b-reading passers in T_A = {r0[sel].mean():.3f} (n {sel.sum()})")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--analyse":
        with open(OUT + ".rows.json", encoding="utf-8") as fh:
            analyse(json.load(fh))
    else:
        main()
