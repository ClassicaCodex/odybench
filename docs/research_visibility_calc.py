"""
Rough visibility base rates for the Odyssey sky clues (companion to
docs/research-visibility.md).

Run:  cd C:\\Projects\\odybench && py docs\\research_visibility_calc.py [section ...]
Sections: planets, mercury_events, moon, stars, all (default).
Writes results/research-visibility.json (merged per section).

Method (deliberately simple, stated so it can be checked):
 * Ephemeris: JPL DE441 excerpt data/ephem/de441_m1320_m1030.bsp via Skyfield 1.55,
   built-in Delta-T (about 28,800 s at -1177). Calendar: proleptic Julian.
 * Site: Ithaca, 38.37 N, 20.70 E, sea level. "Local date" = date in local mean
   time (UT + 1h22.8m).
 * Span for base rates: 1250-1115 BC (astronomical -1249 .. -1114), the span
   Baikouzis & Magnasco (2008) searched.
 * Planet visibility: classical arcus-visionis test (Ptolemy, Almagest XIII.7):
   a planet is seen at its morning rising if the Sun's (geometric) altitude at the
   moment of the planet's apparent rising is <= -AV. Bands of AV are taken from the
   literature (see the .md). Altitude-at-twilight tests are given as alternatives.
 * Fixed stars: own spherical astronomy (linear proper motion, IAU 2006 precession
   from Skyfield, low-precision solar theory of Meeus ch. 25) so that the same code
   can run at -700 (Hesiod) where the DE441 excerpt has no coverage; checked against
   Skyfield/DE441 at -1177.
 * Lunar crescent: Yallop (1997, NAO Technical Note 69) q-test at best time, plus the
   commonly quoted "age >= 24 h and lag >= 48 min" rule.
None of this is a precise visibility model; it is meant to bound base rates.
"""
import json
import math
import os
import sys
import time

import numpy as np
from skyfield import almanac
from skyfield.api import GREGORIAN_START, load, wgs84
from skyfield.framelib import ecliptic_frame
from skyfield.magnitudelib import planetary_magnitude
from skyfield.precessionlib import compute_precession

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EPH = os.path.join(ROOT, "data", "ephem", "de441_m1320_m1030.bsp")
OUT = os.path.join(ROOT, "results", "research-visibility.json")

LAT, LON = 38.37, 20.70
Y0, Y1 = -1249, -1114          # 1250 BC .. 1115 BC inclusive

ts = load.timescale(builtin=True)
ts.julian_calendar_cutoff = GREGORIAN_START
eph = load(EPH)
EARTH, SUN, MOON = eph["earth"], eph["sun"], eph["moon"]
VEN, MER = eph["venus"], eph["mercury"]
JUP, MARS = eph["jupiter barycenter"], eph["mars barycenter"]
SITE = wgs84.latlon(LAT, LON)
OBS = EARTH + SITE
T0 = ts.ut1(Y0, 1, 1, 0)
T1 = ts.ut1(Y1 + 1, 1, 1, 0)
LMT = LON / 360.0  # days


# ---------------------------------------------------------------- utilities
def jdn_local(t):
    """Local (LMT) civil-date Julian Day Number for skyfield Time(s)."""
    return np.floor(np.asarray(t.ut1) + 0.5 + LMT).astype(np.int64)


def jdn_to_julian(jdn):
    """Proleptic Julian calendar (astronomical year, month, day)."""
    jdn = np.asarray(jdn, dtype=np.int64)
    c = jdn + 32082
    d = (4 * c + 3) // 1461
    e = c - (1461 * d) // 4
    m = (5 * e + 2) // 153
    day = e - (153 * m + 2) // 5 + 1
    month = m + 3 - 12 * (m // 10)
    year = d - 4800 + m // 10
    return year, month, day


def datestr(jdn):
    y, m, d = jdn_to_julian(jdn)
    y, m, d = int(y), int(m), int(d)
    bc = f"{1 - y} BC" if y <= 0 else f"AD {y}"
    mon = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()[m - 1]
    return f"{d} {mon} {bc} (astr. {y})"


def doy_label(month, day):
    mon = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()[month - 1]
    return f"{day} {mon}"


def by_morning(t_sunrise, t_event):
    """For each sunrise, the event time nearest to it (within 12 h) or nan."""
    a = np.asarray(t_sunrise.ut1)
    b = np.asarray(t_event.ut1)
    i = np.searchsorted(b, a)
    i0 = np.clip(i - 1, 0, len(b) - 1)
    i1 = np.clip(i, 0, len(b) - 1)
    pick = np.where(np.abs(b[i0] - a) <= np.abs(b[i1] - a), i0, i1)
    out = b[pick]
    out = np.where(np.abs(out - a) < 0.5, out, np.nan)
    return out, pick


def save(section, payload):
    data = {}
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as f:
            data = json.load(f)
    data[section] = payload
    data["_meta"] = {
        "ephemeris": "JPL DE441 excerpt (data/ephem/de441_m1320_m1030.bsp) via Skyfield",
        "site": f"Ithaca {LAT} N {LON} E",
        "span": "1250-1115 BC (astronomical -1249..-1114), proleptic Julian",
        "script": "docs/research_visibility_calc.py",
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, default=float)


def frac(x):
    x = np.asarray(x, dtype=bool)
    return float(x.mean())


# ------------------------------------------------------------------ planets
def planet_mornings(body, label):
    """Per-morning table for a planet: lead of rising over sunrise, Sun altitude at
    the planet's rising, signed elongation, magnitude, altitude at dawn thresholds."""
    tsr, _ = almanac.find_risings(OBS, SUN, T0, T1)
    tpr, _ = almanac.find_risings(OBS, body, T0, T1)
    rise_ut, _ = by_morning(tsr, tpr)
    lead_min = (np.asarray(tsr.ut1) - rise_ut) * 1440.0
    ok = ~np.isnan(rise_ut)
    rt = ts.ut1_jd(np.where(ok, rise_ut, np.asarray(tsr.ut1)))
    # Sun altitude (geometric, topocentric) at planet's apparent rising
    alt_sun_at_rise = OBS.at(rt).observe(SUN).apparent().altaz()[0].degrees
    alt_sun_at_rise = np.where(ok, alt_sun_at_rise, np.nan)
    # magnitude and elongation at sunrise
    ap = OBS.at(tsr).observe(body).apparent()
    sp = OBS.at(tsr).observe(SUN).apparent()
    elong = ap.separation_from(sp).degrees
    lon_p = ap.frame_latlon(ecliptic_frame)[1].degrees
    lon_s = sp.frame_latlon(ecliptic_frame)[1].degrees
    dl = (lon_p - lon_s + 180.0) % 360.0 - 180.0
    signed = np.where(dl < 0, -elong, elong)   # negative = west of Sun = morning side
    try:
        mag = planetary_magnitude(OBS.at(tsr).observe(body))
    except Exception:
        mag = np.full(len(elong), np.nan)
    out = {"jdn": jdn_local(tsr), "sunrise_ut": np.asarray(tsr.ut1), "lead_min": lead_min,
           "alt_sun_at_rise": alt_sun_at_rise, "elong": signed, "mag": np.asarray(mag)}
    for dep in (6, 9, 12):
        tt, _ = almanac.find_risings(OBS, SUN, T0, T1, horizon_degrees=-dep)
        tw, _ = by_morning(tsr, tt)
        tw = ts.ut1_jd(np.where(np.isnan(tw), np.asarray(tsr.ut1), tw))
        alt = OBS.at(tw).observe(body).apparent().altaz(temperature_C=10.0, pressure_mbar=1010.0)[0].degrees
        out[f"alt_at_sun_m{dep}"] = alt
    print(f"  {label}: {len(lead_min)} mornings", flush=True)
    return out


def run_planets():
    t = time.time()
    V = planet_mornings(VEN, "Venus")
    M = planet_mornings(MER, "Mercury")
    J = planet_mornings(JUP, "Jupiter")
    A = planet_mornings(MARS, "Mars")
    np.savez_compressed(os.path.join(ROOT, "results", "research-visibility-mornings.npz"),
                        **{f"V_{k}": v for k, v in V.items()}, **{f"M_{k}": v for k, v in M.items()},
                        **{f"J_{k}": v for k, v in J.items()}, **{f"A_{k}": v for k, v in A.items()})
    print("planets computed in %.1fs" % (time.time() - t))
    return V, M, J, A


def load_mornings():
    p = os.path.join(ROOT, "results", "research-visibility-mornings.npz")
    if not os.path.exists(p):
        return run_planets()
    z = np.load(p)
    def grab(prefix):
        return {k[len(prefix):]: z[k] for k in z.files if k.startswith(prefix)}
    return grab("V_"), grab("M_"), grab("J_"), grab("A_")


def visible_av(P, av):
    """Seen at morning rising: rises before the Sun and Sun altitude <= -AV then."""
    return (P["lead_min"] > 0) & (P["alt_sun_at_rise"] <= -av)


def runs(mask):
    """Start/end indices of True runs."""
    m = np.concatenate([[False], np.asarray(mask, bool), [False]])
    d = np.diff(m.astype(int))
    return np.where(d == 1)[0], np.where(d == -1)[0] - 1


def venus_section():
    V, M, J, A = load_mornings()
    res = {}
    n = len(V["lead_min"])
    res["n_mornings"] = n
    west = V["elong"] < 0
    res["morning_side_geometric"] = frac(west)
    for e in (5, 10, 20, 30, 40):
        res[f"west_elong_ge_{e}"] = frac(V["elong"] <= -e)
    for av in (4, 5, 6.1, 7, 8.6, 10):
        res[f"visible_AV_{av}"] = frac(visible_av(V, av))
    for L in (30, 45, 60, 90, 120, 150, 180):
        res[f"lead_ge_{L}min"] = frac(V["lead_min"] >= L)
    for dep in (6, 9, 12):
        for h in (5, 10, 15, 20, 30):
            res[f"alt_ge_{h}_at_sun_m{dep}"] = frac(V[f"alt_at_sun_m{dep}"] >= h)
    # durations of morning-star apparitions and invisibility gaps (AV 5 and 7)
    for av in (5, 7):
        vis = visible_av(V, av) | ((V["elong"] > 0) & False)
        # evening visibility proxy: Venus sets after the Sun with Sun alt <= -AV at Venus setting
        s, e = runs(vis)
        lens = (e - s + 1)
        lens = lens[(s > 0) & (e < n - 1)]
        res[f"morning_apparition_days_AV{av}"] = {"mean": float(lens.mean()), "min": int(lens.min()),
                                                  "max": int(lens.max()), "n": int(len(lens))}
    # B&M check: lead >= 90 min on random days and by season
    y, mo, d = jdn_to_julian(V["jdn"])
    bymonth = {}
    for m in range(1, 13):
        sel = mo == m
        bymonth[m] = {"lead_ge_90": frac(V["lead_min"][sel] >= 90),
                      "visible_AV7": frac(visible_av(V, 7)[sel])}
    res["by_month"] = bymonth
    # magnitude range when morning-visible
    mags = V["mag"][visible_av(V, 7)]
    res["mag_when_visible"] = {"min": float(np.nanmin(mags)), "max": float(np.nanmax(mags)),
                               "median": float(np.nanmedian(mags))}
    # Who is the dawn herald? Venus visible (AV 7) / else Jupiter (AV 10, lead 30-240 min)
    # / else Mars bright (mag <= -1, AV 10) ; Sirius handled in stars section.
    ven = visible_av(V, 7)
    jup = visible_av(J, 10) & (J["lead_min"] >= 30) & (J["lead_min"] <= 240)
    jup_any = visible_av(J, 10)
    mar = visible_av(A, 10) & (A["mag"] <= -1.0)
    res["herald"] = {
        "venus_visible_AV7": frac(ven),
        "jupiter_visible_AV10": frac(jup_any),
        "jupiter_rises_30_240min_before_sun_visible": frac(jup),
        "not_venus_but_jupiter_30_240": frac(~ven & jup),
        "not_venus_but_jupiter_any": frac(~ven & jup_any),
        "mars_bright_mag_le_m1_visible": frac(mar),
        "venus_or_jupiter_30_240": frac(ven | jup),
        "neither_venus_nor_jupiter_any": frac(~ven & ~jup_any),
        "jupiter_mag_median_when_visible": float(np.nanmedian(J["mag"][jup_any])),
    }
    return res


def mercury_section():
    V, M, J, A = load_mornings()
    res = {}
    n = len(M["lead_min"])
    res["n_mornings"] = n
    res["morning_side_geometric"] = frac(M["elong"] < 0)
    for e in (10, 15, 18, 20, 22, 25):
        res[f"west_elong_ge_{e}"] = frac(M["elong"] <= -e)
    for av in (8, 10, 12):
        res[f"visible_AV_{av}"] = frac(visible_av(M, av))
        res[f"visible_AV_{av}_and_mag_le_1"] = frac(visible_av(M, av) & (M["mag"] <= 1.0))
    for dep in (6, 9):
        for h in (3, 5, 8, 10):
            res[f"alt_ge_{h}_at_sun_m{dep}"] = frac((M[f"alt_at_sun_m{dep}"] >= h) & (M["elong"] < 0))
    for L in (30, 45, 60, 90):
        res[f"lead_ge_{L}min"] = frac(M["lead_min"] >= L)
    y, mo, d = jdn_to_julian(M["jdn"])
    res["by_month_visible_AV10"] = {int(m): frac(visible_av(M, 10)[mo == m]) for m in range(1, 13)}
    res["by_month_alt5_at_sun_m6"] = {int(m): frac(((M["alt_at_sun_m6"] >= 5) & (M["elong"] < 0))[mo == m])
                                     for m in range(1, 13)}
    # morning apparitions: count and how many have zero visible days (omitted) -- per synodic period
    return res


# ---------------------------------------------------------- Mercury events
def mercury_events():
    """Daily geocentric series: GWE, stations, inferior conjunctions; rising azimuths."""
    days = np.arange(math.floor(T0.ut1) + 0.5, math.floor(T1.ut1) + 0.5, 1.0)  # 0h UT
    t = ts.ut1_jd(days)
    e = EARTH.at(t)
    mp = e.observe(MER).apparent()
    sp = e.observe(SUN).apparent()
    lm = mp.frame_latlon(ecliptic_frame)[1].degrees
    ls = sp.frame_latlon(ecliptic_frame)[1].degrees
    sep = mp.separation_from(sp).degrees
    dl = (lm - ls + 180.0) % 360.0 - 180.0
    se = np.where(dl < 0, -sep, sep)
    dlam = (np.diff(lm) + 180.0) % 360.0 - 180.0  # daily motion
    # greatest western elongation: local minima of se with se < -10
    i = np.arange(1, len(se) - 1)
    gwe = i[(se[i] < se[i - 1]) & (se[i] <= se[i + 1]) & (se[i] < -10)]
    gee = i[(se[i] > se[i - 1]) & (se[i] >= se[i + 1]) & (se[i] > 10)]
    # stations: sign change of daily motion. "western/morning station" = retrograde -> direct
    st_rd = np.where((dlam[:-1] < 0) & (dlam[1:] >= 0))[0] + 1
    st_dr = np.where((dlam[:-1] >= 0) & (dlam[1:] < 0))[0] + 1
    infc = np.where((se[:-1] > 0) & (se[1:] <= 0))[0] + 1
    jd_local = np.floor(days + 0.5 + LMT).astype(np.int64)
    return {"jdn": jd_local, "se": se, "gwe": jd_local[gwe], "gee": jd_local[gee],
            "station_ret_to_dir": jd_local[st_rd], "station_dir_to_ret": jd_local[st_dr],
            "inf_conj": jd_local[infc]}


def rising_azimuths(body):
    tr, _ = almanac.find_risings(OBS, body, T0, T1)
    az = OBS.at(tr).observe(body).apparent().altaz()[1].degrees
    return jdn_local(tr), az, np.asarray(tr.ut1)


def near_event_fraction(day_jdn, ev_jdn, k):
    ev = np.sort(np.asarray(ev_jdn))
    i = np.searchsorted(ev, day_jdn)
    d1 = np.abs(day_jdn - ev[np.clip(i - 1, 0, len(ev) - 1)])
    d2 = np.abs(day_jdn - ev[np.clip(i, 0, len(ev) - 1)])
    return np.minimum(d1, d2) <= k


def mercury_events_section():
    V, M, J, A = load_mornings()
    E = mercury_events()
    res = {}
    span = (E["jdn"][-1] - E["jdn"][0] + 1)
    res["n_gwe"] = int(len(E["gwe"]))
    res["mean_gwe_spacing_days"] = float(np.diff(E["gwe"]).mean())
    res["n_station_ret_to_dir"] = int(len(E["station_ret_to_dir"]))
    days = M["jdn"]
    visA = visible_av(M, 10)
    for k in (0, 1, 2, 3, 5, 7, 10):
        g = near_event_fraction(days, E["gwe"], k)
        s = near_event_fraction(days, E["station_ret_to_dir"], k)
        res[f"within_{k}d_of_GWE"] = frac(g)
        res[f"within_{k}d_of_GWE_and_visible_AV10"] = frac(g & visA)
        res[f"within_{k}d_of_morning_station"] = frac(s)
        res[f"within_{k}d_of_morning_station_and_visible_AV10"] = frac(s & visA)
    # morning first visibility (MF) dates under AV 10; omitted morning apparitions
    out_mf = {}
    for av in (8, 10, 12):
        vis = visible_av(M, av)
        s_idx, e_idx = runs(vis)
        mf = days[s_idx]
        # count GWE with no visible morning within +-15 d => "omitted"
        omitted = 0
        for g in E["gwe"]:
            j = np.searchsorted(days, g)
            if j < 15 or j > len(days) - 16:
                continue
            if not vis[j - 15:j + 16].any():
                omitted += 1
        out_mf[f"AV{av}"] = {"n_runs": int(len(s_idx)), "omitted_morning_apparitions": omitted,
                             "n_gwe": int(len(E["gwe"]))}
        for k in (1, 3, 5):
            out_mf[f"AV{av}"][f"within_{k}d_of_MF"] = frac(near_event_fraction(days, mf, k))
    res["morning_first"] = out_mf
    # rising azimuth extrema of Mercury, and of Mercury-minus-Sun
    jm, azm, _ = rising_azimuths(MER)
    js, azs, _ = rising_azimuths(SUN)
    # align by local date
    common, im, isn = np.intersect1d(jm, js, return_indices=True)
    azm_c, azs_c = azm[im], azs[isn]
    d = azm_c - azs_c
    i = np.arange(1, len(common) - 1)
    # azimuth measured from north through east; "westernmost" rising on the eastern horizon is
    # undefined literally; record local extrema of Mercury's rise azimuth and of (Mercury - Sun).
    max_az = common[i[(azm_c[i] > azm_c[i - 1]) & (azm_c[i] >= azm_c[i + 1])]]
    min_az = common[i[(azm_c[i] < azm_c[i - 1]) & (azm_c[i] <= azm_c[i + 1])]]
    max_d = common[i[(d[i] > d[i - 1]) & (d[i] >= d[i + 1])]]
    min_d = common[i[(d[i] < d[i - 1]) & (d[i] <= d[i + 1])]]
    res["rise_az_extrema_counts"] = {"max_az": int(len(max_az)), "min_az": int(len(min_az)),
                                     "max_az_minus_sun": int(len(max_d)), "min_az_minus_sun": int(len(min_d))}
    # Baikouzis & Magnasco's "westernmost rise-time azimuth" reproduces as a local maximum of
    # the rise azimuth measured from north through east (most southerly rising point) on
    # 12-13 Mar 1178 BC. Keep only extrema while Mercury is on the morning side and visible.
    mjd = M["jdn"]
    pos = np.searchsorted(mjd, max_az)
    pos = np.clip(pos, 0, len(mjd) - 1)
    keep = (mjd[pos] == max_az) & (M["elong"][pos] < 0) & visA[pos]
    azev = max_az[keep]
    res["rise_az_max_morning_visible_per_year"] = float(len(azev) / (Y1 - Y0 + 1))
    res["gwe_per_year"] = float(len(E["gwe"]) / (Y1 - Y0 + 1))
    for k in (1, 2, 3, 5):
        a = near_event_fraction(days, azev, k)
        res[f"within_{k}d_of_riseaz_max_morning_visible"] = frac(a)
        u = (near_event_fraction(days, E["gwe"], k) | near_event_fraction(days, E["station_ret_to_dir"], k)
             | a)
        res[f"within_{k}d_of_any_turning_point_GWE_station_riseaz"] = frac(u)
        res[f"within_{k}d_of_any_turning_point_and_visible_AV10"] = frac(u & visA)
    # spacing between the three candidate "turning points" in each morning apparition
    gaps = []
    for g in E["gwe"]:
        s = E["station_ret_to_dir"]
        s_near = s[np.argmin(np.abs(s - g))]
        a_near = azev[np.argmin(np.abs(azev - g))] if len(azev) else g
        if abs(s_near - g) < 40 and abs(a_near - g) < 40:
            gaps.append((g - s_near, g - a_near))
    gaps = np.array(gaps)
    res["gwe_minus_station_days"] = {"mean": float(gaps[:, 0].mean()), "min": int(gaps[:, 0].min()),
                                     "max": int(gaps[:, 0].max())}
    res["gwe_minus_riseazmax_days"] = {"mean": float(gaps[:, 1].mean()), "min": int(gaps[:, 1].min()),
                                       "max": int(gaps[:, 1].max()), "n": int(len(gaps))}
    # Events around Baikouzis & Magnasco's Day -34 = 13 Mar 1178 BC (astr. -1177)
    lo = int(jdn_local(ts.ut1(-1177, 2, 1, 12))[()]) if False else None
    t_lo = ts.ut1(-1177, 1, 15, 12)
    t_hi = ts.ut1(-1177, 5, 15, 12)
    jlo, jhi = int(np.floor(t_lo.ut1 + 0.5 + LMT)), int(np.floor(t_hi.ut1 + 0.5 + LMT))
    def inwin(a):
        return [datestr(x) for x in np.asarray(a) if jlo <= x <= jhi]
    win = {"GWE": inwin(E["gwe"]), "GEE": inwin(E["gee"]), "inferior_conj": inwin(E["inf_conj"]),
           "station_dir_to_ret": inwin(E["station_dir_to_ret"]),
           "station_ret_to_dir": inwin(E["station_ret_to_dir"]),
           "rise_az_local_max": inwin(max_az), "rise_az_local_min": inwin(min_az),
           "rise_az_minus_sun_local_max": inwin(max_d), "rise_az_minus_sun_local_min": inwin(min_d)}
    for av in (8, 10, 12):
        vis = visible_av(M, av)
        s_idx, e_idx = runs(vis)
        win[f"morning_visible_runs_AV{av}"] = [(datestr(days[a]), datestr(days[b]))
                                               for a, b in zip(s_idx, e_idx) if jlo <= days[a] <= jhi or jlo <= days[b] <= jhi]
    sel = (M["jdn"] >= jlo) & (M["jdn"] <= jhi)
    daily = []
    for j, el, lead, hs, mg, a6 in zip(M["jdn"][sel], M["elong"][sel], M["lead_min"][sel],
                                       M["alt_sun_at_rise"][sel], M["mag"][sel], M["alt_at_sun_m6"][sel]):
        y, mo, dd = jdn_to_julian(j)
        if (mo == 3 and 1 <= dd <= 31) or (mo == 4 and dd <= 20):
            ii = np.searchsorted(common, j)
            azv = float(azm_c[ii]) if ii < len(common) and common[ii] == j else float("nan")
            azsv = float(azs_c[ii]) if ii < len(common) and common[ii] == j else float("nan")
            daily.append({"date": datestr(j), "elong": round(float(el), 2), "lead_min": round(float(lead), 1),
                          "sun_alt_at_mercury_rise": round(float(hs), 2), "mag": round(float(mg), 2),
                          "alt_at_civil_dawn": round(float(a6), 2), "rise_az": round(azv, 2),
                          "sun_rise_az": round(azsv, 2)})
    win["daily_mar_apr"] = daily
    res["window_1178BC"] = win
    return res


# -------------------------------------------------------------- fixed stars
# J2000/ICRS (Hipparcos, via SIMBAD): ra, dec [deg], pmra*cos(dec), pmdec [mas/yr], V mag
STARS = {
    "Arcturus": (213.91530, 19.18241, -1093.39, -2000.06, -0.05),
    "Alcyone": (56.87115, 24.10514, 19.34, -43.67, 2.87),
    "Sirius": (101.28715, -16.71612, -546.01, -1223.07, -1.46),
    "eta Boo": (208.67116, 18.39772, -60.95, -356.29, 2.68),
    "eps Boo": (221.24674, 27.07422, -50.95, 21.07, 2.37),
    "gam Boo": (218.01947, 38.30825, -115.72, 151.31, 3.03),
    "bet Boo": (225.48651, 40.39057, -40.16, -28.86, 3.49),
    "del Boo": (228.87568, 33.31483, 83.61, -112.58, 3.47),
}
BOOTES = ["Arcturus", "eta Boo", "eps Boo", "gam Boo", "bet Boo", "del Boo"]


def star_radec_of_date(name, jd_tt):
    ra0, de0, pmra, pmde, _ = STARS[name]
    dt = (jd_tt - 2451545.0) / 365.25
    de = de0 + pmde * dt / 3.6e6
    ra = ra0 + pmra * dt / 3.6e6 / math.cos(math.radians(de0))
    v = np.array([math.cos(math.radians(de)) * math.cos(math.radians(ra)),
                  math.cos(math.radians(de)) * math.sin(math.radians(ra)),
                  math.sin(math.radians(de))])
    P = compute_precession(jd_tt)
    w = P @ v
    return math.degrees(math.atan2(w[1], w[0])) % 360.0, math.degrees(math.asin(w[2]))


def sun_radec_meeus(jd_tt):
    """Low-precision Sun (Meeus, Astronomical Algorithms ch. 25), mean equator/equinox of date."""
    T = (np.asarray(jd_tt) - 2451545.0) / 36525.0
    L0 = 280.46646 + 36000.76983 * T + 0.0003032 * T * T
    Mm = np.radians(357.52911 + 35999.05029 * T - 0.0001537 * T * T)
    C = ((1.914602 - 0.004817 * T - 0.000014 * T * T) * np.sin(Mm)
         + (0.019993 - 0.000101 * T) * np.sin(2 * Mm) + 0.000289 * np.sin(3 * Mm))
    lam = np.radians(L0 + C - 0.00569)
    eps = np.radians(23.4392911 - 0.0130041667 * T - 1.6389e-7 * T ** 2 + 5.0361e-7 * T ** 3)
    ra = np.degrees(np.arctan2(np.cos(eps) * np.sin(lam), np.cos(lam))) % 360.0
    de = np.degrees(np.arcsin(np.sin(eps) * np.sin(lam)))
    return ra, de, (np.degrees(lam) % 360.0)


def alt_deg(ra, de, lst_deg, lat=LAT):
    H = np.radians(lst_deg - ra)
    p, d = math.radians(lat), np.radians(de)
    return np.degrees(np.arcsin(np.sin(p) * np.sin(d) + np.cos(p) * np.cos(d) * np.cos(H)))


def refr(h):
    """Bennett refraction (deg) for an apparent-altitude correction of geometric h."""
    h = np.asarray(h, dtype=float)
    return np.where(h > -1.5, 1.0 / np.tan(np.radians(h + 7.31 / (h + 4.4))) / 60.0, 0.0)


def year_grid(year, step_min=2.0):
    """Nights of one Julian year at the site: arrays [day, sample] from local noon to local noon."""
    d0 = int(jdn_local(ts.ut1(year, 1, 1, 12))[()]) if np.ndim(jdn_local(ts.ut1(year, 1, 1, 12))) else int(jdn_local(ts.ut1(year, 1, 1, 12)))
    d1 = int(jdn_local(ts.ut1(year, 12, 31, 12)))
    days = np.arange(d0, d1 + 1)
    n = int(round(1440 / step_min))
    frac_ = np.arange(n) * step_min / 1440.0
    jd = days[:, None] - LMT + frac_[None, :]            # UT JD, starting at local noon
    t = ts.ut1_jd(jd.ravel())
    lst = (np.asarray(t.gmst) * 15.0 + LON).reshape(jd.shape)
    jd_tt = np.asarray(t.tt).reshape(jd.shape)
    sra, sde, slam = sun_radec_meeus(jd_tt)
    hsun = alt_deg(sra, sde, lst)
    mid_tt = float(np.asarray(t.tt)[len(t.tt) // 2])
    stars = {}
    for name in STARS:
        ra, de = star_radec_of_date(name, mid_tt)
        stars[name] = {"alt": alt_deg(ra, de, lst), "ra": ra, "dec": de}
    return {"days": days, "jd": jd, "hsun": hsun, "slam": slam, "stars": stars, "step": step_min}


def first_index(mask, axis=1):
    has = mask.any(axis=axis)
    return np.where(has, mask.argmax(axis=axis), -1)


def star_phases(G, name, av, h_app=0.0):
    """Annual phases of a star from a year grid, arcus visionis 'av' (Sun depression at the
    moment the star is at apparent altitude h_app, i.e. geometric ~ h_app - refraction).
    Returns local JDNs of: morning first (heliacal rising), evening last (heliacal setting),
    last visible evening rising (acronychal rising), first visible morning setting (cosmical)."""
    hs = G["hsun"]
    a = G["stars"][name]["alt"]
    a_app = a + refr(a)
    days = G["days"]
    noon_to_noon = hs.shape[1]
    # star crossing apparent altitude h_app (upward = rising, downward = setting)
    up = (a_app[:, 1:] >= h_app) & (a_app[:, :-1] < h_app)
    dn = (a_app[:, 1:] < h_app) & (a_app[:, :-1] >= h_app)
    hs_mid = hs[:, 1:]
    half = noon_to_noon // 2     # local midnight index
    idx = np.arange(noon_to_noon - 1)[None, :]
    morning = idx >= half
    evening = idx < half
    seen_rise_morning = (up & (hs_mid <= -av) & morning).any(axis=1)
    seen_set_evening = (dn & (hs_mid <= -av) & evening).any(axis=1)
    seen_rise_evening = (up & (hs_mid <= -av) & evening).any(axis=1)
    seen_set_morning = (dn & (hs_mid <= -av) & morning).any(axis=1)
    # visible at all in the dark part of the night (sun <= -av and star above h_app)
    dark_vis = ((a_app >= h_app + 0.0) & (hs <= -av))
    def first_after_gap(mask):
        out = []
        for i in range(1, len(mask)):
            if mask[i] and not mask[i - 1]:
                out.append(int(days[i]))
        return out
    def last_before_gap(mask):
        out = []
        for i in range(len(mask) - 1):
            if mask[i] and not mask[i + 1]:
                out.append(int(days[i]))
        return out
    return {
        "morning_first_heliacal_rising": first_after_gap(seen_rise_morning),
        "evening_last_heliacal_setting": last_before_gap(seen_set_evening),
        "evening_rising_last_visible_acronychal": last_before_gap(seen_rise_evening),
        "evening_rising_first_visible": first_after_gap(seen_rise_evening),
        "morning_setting_first_visible_cosmical": first_after_gap(seen_set_morning),
        "morning_setting_last_visible": last_before_gap(seen_set_morning),
        "never_visible_days": int((~dark_vis.any(axis=1)).sum()),
        "invisible_runs": [(int(days[s]), int(days[e])) for s, e in zip(*runs(~dark_vis.any(axis=1)))],
    }


def twilight_alt(G, name, dep, evening=True):
    """Apparent altitude of a star at the moment the Sun reaches -dep (evening or morning)."""
    hs = G["hsun"]
    n = hs.shape[1]
    half = n // 2
    if evening:
        seg = hs[:, :half]
        cross = (seg[:, 1:] <= -dep) & (seg[:, :-1] > -dep)
        i = first_index(cross) + 1
    else:
        seg = hs[:, half:]
        cross = (seg[:, 1:] >= -dep) & (seg[:, :-1] < -dep)
        i = first_index(cross)
        i = np.where(i >= 0, i + half, -1)
    a = G["stars"][name]["alt"]
    rows = np.arange(len(i))
    val = np.where(i >= 0, a[rows, np.clip(i, 0, n - 1)], np.nan)
    return val + refr(val)


def stars_section():
    out = {}
    # ---- check analytic Sun against DE441 at -1177
    tchk = ts.ut1(-1177, np.arange(1, 13), 15, 12)
    sp = EARTH.at(tchk).observe(SUN).apparent()
    ra_s, de_s, _ = sp.radec(epoch="date")
    ra_m, de_m, _ = sun_radec_meeus(np.asarray(tchk.tt))
    dra = ((ra_s._degrees - ra_m + 180) % 360 - 180) * np.cos(np.radians(de_m))
    out["meeus_sun_minus_de441_arcmin_max"] = float(np.max(np.hypot(dra, de_s.degrees - de_m)) * 60)
    # check star position against skyfield Star (DE441) at -1177
    from skyfield.api import Star
    chk = {}
    for name in ("Arcturus", "Alcyone"):
        ra0, de0, pmra, pmde, _ = STARS[name]
        st = Star(ra_hours=ra0 / 15, dec_degrees=de0, ra_mas_per_year=pmra, dec_mas_per_year=pmde)
        t = ts.ut1(-1177, 4, 1, 0)
        ra_k, de_k, _ = EARTH.at(t).observe(st).apparent().radec(epoch="date")
        ra_o, de_o = star_radec_of_date(name, float(t.tt))
        chk[name] = {"own_ra_dec": (ra_o, de_o), "skyfield_ra_dec": (ra_k._degrees, de_k.degrees),
                     "diff_arcmin": float(math.hypot((ra_o - ra_k._degrees) * math.cos(math.radians(de_o)),
                                                     de_o - de_k.degrees) * 60)}
    out["star_position_check_-1177"] = chk
    for year in (-1177, -700):
        G = year_grid(year)
        days = G["days"]
        Y = {"year": f"{1 - year} BC (astr. {year})"}
        Y["star_radec_of_date"] = {k: (round(v["ra"], 3), round(v["dec"], 3)) for k, v in G["stars"].items()}
        # solstices / equinox from the analytic Sun at local noon
        lam_noon = G["slam"][:, 0]
        def crossing(target):
            d = (lam_noon - target + 180) % 360 - 180
            i = np.where((d[:-1] < 0) & (d[1:] >= 0))[0]
            return [datestr(days[j + 1]) for j in i]
        Y["vernal_equinox"] = crossing(0.0)
        Y["summer_solstice"] = crossing(90.0)
        Y["winter_solstice"] = crossing(270.0)
        ws = None
        d = (lam_noon - 270 + 180) % 360 - 180
        i = np.where((d[:-1] < 0) & (d[1:] >= 0))[0]
        ws_prev = int(days[i[0] + 1]) - 365 if len(i) else None  # previous winter solstice
        ph = {}
        for name, avs in (("Arcturus", (8, 10, 12)), ("Alcyone", (12, 14, 16, 18)), ("Sirius", (8, 10, 12))):
            for av in avs:
                p = star_phases(G, name, av)
                pd = {k: ([datestr(x) for x in v] if isinstance(v, list) and v and not isinstance(v[0], tuple)
                          else v) for k, v in p.items() if k != "invisible_runs"}
                pd["invisible_runs"] = [(datestr(a), datestr(b), b - a + 1) for a, b in p["invisible_runs"]]
                if name == "Arcturus" and ws_prev is not None and p["evening_rising_last_visible_acronychal"]:
                    pd["acronychal_minus_prev_winter_solstice_days"] = [x - ws_prev for x in p["evening_rising_last_visible_acronychal"]]
                ph[f"{name}_AV{av}"] = pd
        Y["phases"] = ph
        # evening/morning co-visibility of Pleiades (Alcyone) and Arcturus
        cov = {}
        for dep in (9, 12, 15, 18):
            aA = twilight_alt(G, "Arcturus", dep, evening=True)
            aP = twilight_alt(G, "Alcyone", dep, evening=True)
            mA = twilight_alt(G, "Arcturus", dep, evening=False)
            mP = twilight_alt(G, "Alcyone", dep, evening=False)
            for h in (2, 5, 10):
                both_e = (aA >= h) & (aP >= h)
                both_m = (mA >= h) & (mP >= h)
                cov[f"evening_sun_m{dep}_alt_ge_{h}"] = {
                    "fraction_of_year": frac(both_e),
                    "runs": [(datestr(days[s]), datestr(days[e]), int(e - s + 1)) for s, e in zip(*runs(both_e))]}
                cov[f"morning_sun_m{dep}_alt_ge_{h}"] = {
                    "fraction_of_year": frac(both_m),
                    "runs": [(datestr(days[s]), datestr(days[e]), int(e - s + 1)) for s, e in zip(*runs(both_m))]}
            # B&M's two limits: first evening Arcturus up at dusk; last evening Pleiades up
            for h in (0, 2, 5):
                upA = aA >= h
                upP = aP >= h
                cov[f"BM_limits_sun_m{dep}_alt_ge_{h}"] = {
                    "Arcturus_up_at_dusk_runs": [(datestr(days[s]), datestr(days[e])) for s, e in zip(*runs(upA))],
                    "Pleiades_up_at_dusk_runs": [(datestr(days[s]), datestr(days[e])) for s, e in zip(*runs(upP))]}
        # both above h at the same moment sometime while Sun <= -12 (any time of night)
        hs = G["hsun"]
        A_ = G["stars"]["Arcturus"]["alt"]
        P_ = G["stars"]["Alcyone"]["alt"]
        for h in (5, 10, 20):
            m = ((A_ + refr(A_)) >= h) & ((P_ + refr(P_)) >= h) & (hs <= -12)
            anyn = m.any(axis=1)
            cov[f"both_ge_{h}_simultaneously_any_time_dark"] = {
                "fraction_of_year": frac(anyn),
                "runs": [(datestr(days[s]), datestr(days[e]), int(e - s + 1)) for s, e in zip(*runs(anyn))]}
        # each visible at some time in the same dark night (not necessarily simultaneously)
        for h in (5, 10):
            m1 = (((A_ + refr(A_)) >= h) & (hs <= -12)).any(axis=1)
            m2 = (((P_ + refr(P_)) >= h) & (hs <= -12)).any(axis=1)
            cov[f"each_ge_{h}_sometime_same_dark_night"] = {"fraction_of_year": frac(m1 & m2),
                "runs": [(datestr(days[s]), datestr(days[e]), int(e - s + 1)) for s, e in zip(*runs(m1 & m2))]}
        Y["pleiades_bootes"] = cov
        # "late-setting" Arcturus: setting time relative to the night
        n = hs.shape[1]
        a_app = A_ + refr(A_)
        dn = (a_app[:, 1:] < 0) & (a_app[:, :-1] >= 0)
        step_h = G["step"] / 60.0
        set_idx = first_index(dn) + 1                       # first setting after local noon
        dusk = first_index((hs[:, 1:] <= -12) & (hs[:, :-1] > -12)) + 1
        dawn = first_index((hs[:, 1:] >= -12) & (hs[:, :-1] < -12) & (np.arange(n - 1)[None, :] > n // 2)) + 1
        valid = (set_idx > 0) & (dusk > 0) & (dawn > 0)
        rel = np.where(valid, (set_idx - dusk) * step_h, np.nan)   # hours after nautical dusk
        night_len = np.where(valid, (dawn - dusk) * step_h, np.nan)
        late = {}
        late["sets_after_local_midnight_and_before_dawn"] = frac((set_idx >= n // 2) & (set_idx < dawn) & valid)
        late["sets_in_dark_more_than_half_night_after_dusk"] = frac((rel > night_len / 2) & (set_idx < dawn) & valid)
        late["visible_at_dusk_and_sets_after_dawn_or_never_sets_in_dark"] = frac((twilight_alt(G, "Arcturus", 12) >= 2)
                                                                               & ((set_idx >= dawn) | (set_idx <= dusk) | ~valid))
        late["sets_within_2h_after_dusk_while_visible_at_dusk"] = frac((rel >= 0) & (rel <= 2) & valid)
        def runs_of(mask):
            return [(datestr(days[s]), datestr(days[e]), int(e - s + 1)) for s, e in zip(*runs(mask))]
        late["runs_sets_after_midnight_before_dawn"] = runs_of((set_idx >= n // 2) & (set_idx < dawn) & valid)
        late["runs_visible_dusk_and_all_night"] = runs_of((twilight_alt(G, "Arcturus", 12) >= 2)
                                                         & ((set_idx >= dawn) | ~valid))
        late["runs_sets_within_2h_after_dusk"] = runs_of((rel >= 0) & (rel <= 2) & valid)
        # Bootes figure: time from first to last of its main stars rising / setting (hours)
        ra_dec = {k: (G["stars"][k]["ra"], G["stars"][k]["dec"]) for k in BOOTES}
        phi = math.radians(LAT)
        def semi_arc(dec):
            x = (math.sin(math.radians(-0.57)) - math.sin(phi) * math.sin(math.radians(dec))) / (
                math.cos(phi) * math.cos(math.radians(dec)))
            if x <= -1:
                return None            # circumpolar: never sets
            return math.degrees(math.acos(min(1, x)))
        circ = [k for k, (ra, de) in ra_dec.items() if semi_arc(de) is None]
        late["bootes_circumpolar_stars"] = circ
        late["bootes_star_decs"] = {k: round(de, 2) for k, (ra, de) in ra_dec.items()}
        rise_lst = {k: (ra - semi_arc(de)) for k, (ra, de) in ra_dec.items() if k not in circ}
        set_lst = {k: (ra + semi_arc(de)) for k, (ra, de) in ra_dec.items() if k not in circ}
        late["bootes_rising_span_hours_sidereal"] = (max(rise_lst.values()) - min(rise_lst.values())) / 15.0
        late["bootes_setting_span_hours_sidereal"] = (max(set_lst.values()) - min(set_lst.values())) / 15.0
        late["bootes_first_to_set"] = min(set_lst, key=set_lst.get)
        late["bootes_last_to_set"] = max(set_lst, key=set_lst.get)
        late["bootes_first_to_rise"] = min(rise_lst, key=rise_lst.get)
        late["bootes_last_to_rise"] = max(rise_lst, key=rise_lst.get)
        late["arcturus_hours_above_horizon"] = 2 * semi_arc(ra_dec["Arcturus"][1]) / 15.0
        late["alcyone_hours_above_horizon"] = 2 * semi_arc(G["stars"]["Alcyone"]["dec"]) / 15.0
        Y["late_setting"] = late
        # Sirius as a dawn herald: rises 30-240 min before sunrise and seen (AV 10)
        S_ = G["stars"]["Sirius"]["alt"]
        s_app = S_ + refr(S_)
        up = (s_app[:, 1:] >= 0) & (s_app[:, :-1] < 0)
        sunrise = first_index((hs[:, 1:] >= -0.83) & (hs[:, :-1] < -0.83) & (np.arange(n - 1)[None, :] > n // 2)) + 1
        r_idx = first_index(up & (np.arange(n - 1)[None, :] > n // 4)) + 1
        lead = np.where((r_idx > 0) & (sunrise > 0), (sunrise - r_idx) * G["step"], np.nan)
        hs_at = np.where(r_idx > 0, hs[np.arange(len(r_idx)), np.clip(r_idx, 0, n - 1)], np.nan)
        her = (lead >= 30) & (lead <= 240) & (hs_at <= -10)
        Y["sirius_herald"] = {"fraction_of_year": frac(her), "runs": runs_of(her)}
        out[str(year)] = Y
        print("  stars", year, "done", flush=True)
    return out


# --------------------------------------------------------------------- Moon
def geo_alt(t, body):
    """Geocentric (airless) altitude at the site, as Yallop's ARCV requires."""
    ra, de, _ = EARTH.at(t).observe(body).apparent().radec(epoch="date")
    lst = np.asarray(t.gast) * 15.0 + LON
    return alt_deg(ra._degrees, de.degrees, lst)


def yallop_q(t):
    """Yallop (1997) q at times t (crescent geometry)."""
    arcv = geo_alt(t, MOON) - geo_alt(t, SUN)
    m = OBS.at(t).observe(MOON).apparent()
    s = OBS.at(t).observe(SUN).apparent()
    arcl = m.separation_from(s).degrees
    dist_km = m.distance().km
    sd = np.degrees(np.arcsin(1737.4 / dist_km)) * 60.0          # topocentric semi-diameter, arcmin
    w = sd * (1.0 - np.cos(np.radians(arcl)))
    q = (arcv - (11.8371 - 6.3226 * w + 0.7319 * w ** 2 - 0.1018 * w ** 3)) / 10.0
    return q, arcv, arcl, w


def nearest_after(a, b, maxd):
    """For each time in a, the first time in b after it (within maxd days), else nan."""
    i = np.searchsorted(b, a)
    i = np.clip(i, 0, len(b) - 1)
    out = b[i]
    return np.where((out > a) & (out - a < maxd), out, np.nan)


def nearest_before(a, b, maxd):
    i = np.searchsorted(b, a) - 1
    i = np.clip(i, 0, len(b) - 1)
    out = b[i]
    return np.where((out < a) & (a - out < maxd), out, np.nan)


def moon_section():
    res = {}
    f = almanac.moon_phases(eph)
    tph, yph = almanac.find_discrete(T0, T1, f)
    tnm = tph[yph == 0]
    C = np.asarray(tnm.ut1)
    res["n_new_moons_1250_1115BC"] = int(len(C))
    pad0, pad1 = ts.ut1_jd(T0.ut1 - 8), ts.ut1_jd(T1.ut1 + 8)
    ss = np.asarray(almanac.find_settings(OBS, SUN, pad0, pad1)[0].ut1)
    sr = np.asarray(almanac.find_risings(OBS, SUN, pad0, pad1)[0].ut1)
    ms = np.asarray(almanac.find_settings(OBS, MOON, pad0, pad1)[0].ut1)
    mr = np.asarray(almanac.find_risings(OBS, MOON, pad0, pad1)[0].ut1)
    ss_j = np.floor(ss + 0.5 + LMT).astype(np.int64)
    sr_j = np.floor(sr + 0.5 + LMT).astype(np.int64)
    Dc = np.floor(C + 0.5 + LMT).astype(np.int64)
    ss_by = dict(zip(ss_j.tolist(), ss.tolist()))
    sr_by = dict(zip(sr_j.tolist(), sr.tolist()))
    # daylight conjunctions (solar eclipse would be visible in daytime at the site)
    sr_c = np.array([sr_by.get(int(j), np.nan) for j in Dc])
    ss_c = np.array([ss_by.get(int(j), np.nan) for j in Dc])
    day_conj = (C > sr_c) & (C < ss_c)
    res["fraction_conjunctions_in_local_daylight"] = frac(day_conj)
    K = 5
    crit_names = ["yallop_A", "yallop_B", "yallop_C", "age24_lag48"]
    first = {c: np.full(len(C), -1) for c in crit_names}
    last = {c: np.full(len(C), -1) for c in crit_names}
    age_first = {c: np.full(len(C), np.nan) for c in crit_names}
    # evenings
    E_s = np.array([[ss_by.get(int(j + k), np.nan) for k in range(K)] for j in Dc])
    E_m = nearest_after(E_s.ravel(), ms, 0.6).reshape(E_s.shape)
    lag = (E_m - E_s)
    tb = E_s + 4.0 / 9.0 * np.where(np.isnan(lag), 0, lag)
    q, arcv, arcl, w = yallop_q(ts.ut1_jd(np.where(np.isnan(tb), C[:, None], tb).ravel()))
    q = q.reshape(E_s.shape)
    age_h = (tb - C[:, None]) * 24.0
    lag_min = lag * 1440.0
    okgeo = (age_h > 0) & (lag_min > 0)
    vis_e = {"yallop_A": okgeo & (q > 0.216), "yallop_B": okgeo & (q > -0.014),
             "yallop_C": okgeo & (q > -0.160), "age24_lag48": okgeo & (age_h >= 24) & (lag_min >= 48)}
    # mornings (last visibility of the old crescent), k = 0 is the morning of the conjunction date
    M_r = np.array([[sr_by.get(int(j - k), np.nan) for k in range(K)] for j in Dc])
    M_m = nearest_before(M_r.ravel(), mr, 0.6).reshape(M_r.shape)
    lagm = (M_r - M_m)
    tbm = M_r - 4.0 / 9.0 * np.where(np.isnan(lagm), 0, lagm)
    qm, _, _, _ = yallop_q(ts.ut1_jd(np.where(np.isnan(tbm), C[:, None], tbm).ravel()))
    qm = qm.reshape(M_r.shape)
    agem_h = (C[:, None] - tbm) * 24.0
    lagm_min = lagm * 1440.0
    okm = (agem_h > 0) & (lagm_min > 0)
    vis_m = {"yallop_A": okm & (qm > 0.216), "yallop_B": okm & (qm > -0.014),
             "yallop_C": okm & (qm > -0.160), "age24_lag48": okm & (agem_h >= 24) & (lagm_min >= 48)}
    out = {}
    for c in crit_names:
        fe = np.where(vis_e[c].any(axis=1), vis_e[c].argmax(axis=1), -1)
        lm_ = np.where(vis_m[c].any(axis=1), vis_m[c].argmax(axis=1), -1)
        agef = np.array([age_h[i, fe[i]] if fe[i] >= 0 else np.nan for i in range(len(C))])
        agel = np.array([agem_h[i, lm_[i]] if lm_[i] >= 0 else np.nan for i in range(len(C))])
        hist_f = {int(k): frac(fe == k) for k in range(-1, K)}
        hist_l = {int(k): frac(lm_ == k) for k in range(-1, K)}
        hist_f_day = {int(k): frac(fe[day_conj] == k) for k in range(-1, K)}
        # invisible ("dark") calendar days between last morning sighting and first evening sighting:
        # dates strictly after the last-visibility morning date and up to (excluding) first-evening date
        # counted as whole local dates on which no crescent is seen at all
        dark = np.where((fe >= 0) & (lm_ >= 0), fe + lm_ - 1, -9)
        # the day with no crescent in either twilight: e.g. lm=1 (seen yesterday morning), fe=1
        # (seen tomorrow evening) -> dates D_c-0 .. only D_c itself unseen at morning, and D_c evening
        # unseen -> number of dates with neither sighting = fe + lm - 1 (when fe>=1, lm>=1)
        out[c] = {"first_evening_offset_days_hist": hist_f,
                  "first_evening_offset_hist_daylight_conjunctions": hist_f_day,
                  "last_morning_offset_days_hist": hist_l,
                  "age_at_first_sighting_h": {"min": float(np.nanmin(agef)), "median": float(np.nanmedian(agef)),
                                              "mean": float(np.nanmean(agef)), "max": float(np.nanmax(agef))},
                  "age_before_conj_at_last_sighting_h": {"min": float(np.nanmin(agel)), "median": float(np.nanmedian(agel)),
                                                         "max": float(np.nanmax(agel))},
                  "dates_with_no_crescent_hist": {int(k): frac(dark == k) for k in range(-1, 2 * K)},
                  "mean_first_offset": float(np.mean(fe[fe >= 0])),
                  "mean_last_offset": float(np.mean(lm_[lm_ >= 0]))}
        if c == "yallop_B":
            fe_B, lm_B = fe, lm_
    res["crescent"] = out
    # Night of Od. 14.457 (skotomenios): B&M Table 1 puts it after Day -5 (sequential) or -4
    # (parallel). Measure moonlight under Day 0 = conjunction date, and Day 0 = first-crescent
    # noumenia (daylight after the first-crescent evening, Greek sunset-to-sunset day).
    def night_moonlight(jdn_evening):
        """Fraction of the dark (Sun < -12) part of the night after local date jdn with the Moon up,
        and the Moon's illuminated fraction at local midnight."""
        jdn_evening = np.asarray(jdn_evening)
        steps = np.arange(0, 1.0, 10 / 1440.0)
        tt = (jdn_evening[:, None] - LMT + steps[None, :]).ravel()   # from local noon
        t = ts.ut1_jd(tt)
        hs = OBS.at(t).observe(SUN).apparent().altaz()[0].degrees.reshape(len(jdn_evening), -1)
        hm = OBS.at(t).observe(MOON).apparent().altaz()[0].degrees.reshape(len(jdn_evening), -1)
        dark = hs < -12
        up = (hm > 0) & dark
        fr_up = up.sum(axis=1) / np.maximum(dark.sum(axis=1), 1)
        tm = ts.ut1_jd(jdn_evening + 0.5 - LMT)
        illum = almanac.fraction_illuminated(eph, "moon", tm)
        return fr_up, np.asarray(illum)
    sko = {}
    for label, day0 in (("day0_conjunction_date", Dc),
                        ("day0_first_crescent_noumenia_yallopB", np.where(fe_B >= 0, Dc + fe_B + 1, Dc + 2))):
        for nm, off in (("night_after_day_-5", -5), ("night_after_day_-4", -4), ("night_after_day_-2", -2)):
            fu, il = night_moonlight(day0 + off)
            sko[f"{label}|{nm}"] = {"moon_up_fraction_of_dark_median": float(np.median(fu)),
                                    "moon_up_fraction_of_dark_range": (float(fu.min()), float(fu.max())),
                                    "illuminated_fraction_median": float(np.median(il))}
    # base rate: all nights in a sample of 20 years
    alln = np.arange(int(Dc[0]), int(Dc[0]) + 365 * 20)
    fu_all, il_all = night_moonlight(alln)
    idx_all = fu_all * il_all
    fu5, il5 = night_moonlight(Dc - 5)
    fu4, il4 = night_moonlight(Dc - 4)
    sko["base_rate_all_nights"] = {
        "moon_up_lt_10pct_of_dark": frac(fu_all < 0.10), "moon_up_lt_25pct": frac(fu_all < 0.25),
        "moon_up_lt_50pct": frac(fu_all < 0.50),
        "moonlight_index_le_day-5_median": frac(idx_all <= np.median(fu5 * il5)),
        "moonlight_index_le_day-4_median": frac(idx_all <= np.median(fu4 * il4)),
        "illum_lt_0.25": frac(il_all < 0.25)}
    res["skotomenios_14_457"] = sko
    return res


# ------------------------------------------- per-new-moon rates, B&M framing
def bm_rates_section():
    """Rates of each clue on the days B&M attach them to, per astronomical new moon
    (Day 0 = local date of conjunction). Rough: uses the per-morning tables above."""
    V, M, J, A = load_mornings()
    E = mercury_events()
    f = almanac.moon_phases(eph)
    tph, yph = almanac.find_discrete(T0, T1, f)
    C = np.asarray(tph[yph == 0].ut1)
    Dc = np.floor(C + 0.5 + LMT).astype(np.int64)
    jd0 = int(V["jdn"][0])
    def at(arr, jdn):
        i = jdn - jd0
        ok = (i >= 0) & (i < len(arr))
        return np.where(ok, arr[np.clip(i, 0, len(arr) - 1)], np.nan)
    y, mo, dd = jdn_to_julian(Dc)
    doy = np.array([int(j - int(jdn_to_julian_inv(int(yy), 1, 1))) for j, yy in zip(Dc, y)])
    # B&M star window: Ti-29 >= 17 Feb and Ti-12 <= 4 Apr  <=>  Ti in [18 Mar, 16 Apr] (Julian)
    start = np.array([jdn_to_julian_inv(int(yy), 3, 18) for yy in y])
    end = np.array([jdn_to_julian_inv(int(yy), 4, 16) for yy in y])
    star_ok = (Dc >= start) & (Dc <= end)
    eq_ok = (Dc - 11 >= np.array([jdn_to_julian_inv(int(yy), 4, 1) for yy in y])) & \
            (Dc - 11 <= np.array([jdn_to_julian_inv(int(yy), 4, 5) for yy in y]))
    res = {"n_new_moons": int(len(C)), "star_window_fraction": frac(star_ok),
           "star_window_per_year": float(star_ok.sum() / (Y1 - Y0 + 1)),
           "star_and_equinox_fraction": frac(star_ok & eq_ok),
           "years_per_star_and_equinox_moon": float((Y1 - Y0 + 1) / max(1, (star_ok & eq_ok).sum()))}
    for off in (-5, -4):
        lead = at(V["lead_min"], Dc + off)
        visV = (at(V["lead_min"], Dc + off) > 0) & (at(V["alt_sun_at_rise"], Dc + off) <= -7)
        for L in (60, 90, 120):
            res[f"venus_lead_ge_{L}_on_day{off}_all"] = frac(lead >= L)
            res[f"venus_lead_ge_{L}_on_day{off}_starwindow"] = frac((lead >= L)[star_ok])
        res[f"venus_visible_AV7_on_day{off}_all"] = frac(visV)
        res[f"venus_visible_AV7_on_day{off}_starwindow"] = frac(visV[star_ok])
    visA = (M["lead_min"] > 0) & (M["alt_sun_at_rise"] <= -10)
    for off in (-34, -33):
        d = Dc + off
        vis = at(visA.astype(float), d) > 0.5
        for k in (1, 2, 3, 5):
            g = near_event_fraction(d, E["gwe"], k)
            s = near_event_fraction(d, E["station_ret_to_dir"], k)
            res[f"mercury_day{off}_within_{k}_GWE_vis"] = frac(g & vis)
            res[f"mercury_day{off}_within_{k}_GWE_vis_starwindow"] = frac((g & vis)[star_ok])
            res[f"mercury_day{off}_within_{k}_GWE_or_station_vis_starwindow"] = frac(((g | s) & vis)[star_ok])
    # joint counts in 135 years for a few variants (no equinox, as in B&M's search)
    joint = {}
    for voff, moff in ((-5, -34), (-4, -33)):
        lead = at(V["lead_min"], Dc + voff)
        d = Dc + moff
        vis = at(visA.astype(float), d) > 0.5
        for L in (60, 90):
            for k in (2, 3):
                g = near_event_fraction(d, E["gwe"], k)
                s = near_event_fraction(d, E["station_ret_to_dir"], k)
                hit = star_ok & (lead >= L) & (g | s) & vis
                joint[f"venus_day{voff}_lead{L}_mercury_day{moff}_GWEorStation_pm{k}"] = [datestr(x) for x in Dc[hit]]
    # B&M's own Mercury test: Day -34 within a few days of the extremum of Mercury's rise azimuth
    # (reproduced as the local maximum of azimuth-from-north on 12-13 Mar 1178 BC), Mercury visible.
    jm, azm, _ = rising_azimuths(MER)
    i = np.arange(1, len(azm) - 1)
    azmax = jm[i[(azm[i] > azm[i - 1]) & (azm[i] >= azm[i + 1])]]
    azmin = jm[i[(azm[i] < azm[i - 1]) & (azm[i] <= azm[i + 1])]]
    for voff, moff in ((-5, -34), (-4, -33)):
        lead = at(V["lead_min"], Dc + voff)
        d = Dc + moff
        vis = at(visA.astype(float), d) > 0.5
        for L in (60, 90):
            for k in (2, 3):
                a = near_event_fraction(d, azmax, k)
                hit = star_ok & (lead >= L) & a & vis
                joint[f"venus_day{voff}_lead{L}_mercury_day{moff}_riseAzMax_pm{k}"] = [datestr(x) for x in Dc[hit]]
                a2 = a | near_event_fraction(d, azmin, k)
                hit2 = star_ok & (lead >= L) & a2 & vis
                joint[f"venus_day{voff}_lead{L}_mercury_day{moff}_riseAzAnyExtremum_pm{k}"] = [datestr(x) for x in Dc[hit2]]
        for k in (2, 3):
            res[f"mercury_day{moff}_within_{k}_riseAzMax_vis_starwindow"] = frac((near_event_fraction(d, azmax, k) & vis)[star_ok])
            res[f"mercury_day{moff}_within_{k}_riseAzAnyExtremum_vis_starwindow"] = frac(
                ((near_event_fraction(d, azmax, k) | near_event_fraction(d, azmin, k)) & vis)[star_ok])
            res[f"mercury_day{moff}_within_{k}_riseAzMax_vis_all"] = frac(near_event_fraction(d, azmax, k) & vis)
    # Day 0 moved off the conjunction date (feast on a first-crescent noumenia, +1..+3 days)
    for s in (1, 2, 3):
        D0 = Dc + s
        sw = (D0 >= start) & (D0 <= end)
        lead = at(V["lead_min"], D0 - 5)
        d = D0 - 34
        vis = at(visA.astype(float), d) > 0.5
        for k in (2, 3):
            a = near_event_fraction(d, azmax, k)
            hit = sw & (lead >= 90) & a & vis
            joint[f"DAY0=conj+{s}_venus_day-5_lead90_mercury_day-34_riseAzMax_pm{k}"] = [
                datestr(x) + f" [conj {datestr(x - s)}]" for x in D0[hit]]
            g = near_event_fraction(d, E["gwe"], k) | near_event_fraction(d, E["station_ret_to_dir"], k)
            hit2 = sw & (lead >= 90) & g & vis
            joint[f"DAY0=conj+{s}_venus_day-5_lead90_mercury_day-34_GWEorStation_pm{k}"] = [
                datestr(x) + f" [conj {datestr(x - s)}]" for x in D0[hit2]]
    res["joint_hits_1250_1115BC"] = joint
    # the 1178 BC case itself
    j = jdn_to_julian_inv(-1177, 4, 16)
    res["case_16Apr1178BC"] = {
        "conjunction_local_date": datestr(Dc[np.argmin(np.abs(Dc - j))]),
        "venus_lead_min_day-5": float(at(V["lead_min"], np.array([j - 5]))[0]),
        "venus_lead_min_day-4": float(at(V["lead_min"], np.array([j - 4]))[0]),
        "venus_mag_day-5": float(at(V["mag"], np.array([j - 5]))[0]),
        "mercury_elong_day-34": float(at(M["elong"], np.array([j - 34]))[0]),
        "in_star_window": bool(star_ok[np.argmin(np.abs(Dc - j))]),
        "in_equinox_window": bool(eq_ok[np.argmin(np.abs(Dc - j))]),
    }
    return res


def herald_section():
    """Monthly Mercury dawn altitudes and the 'brightest star heralding dawn' alternatives."""
    V, M, J, A = load_mornings()
    y, mo, d = jdn_to_julian(M["jdn"])
    out = {}
    for h in (5, 8, 10):
        out[f"mercury_alt_ge_{h}_at_civil_dawn_by_month"] = {
            int(m): frac(((M["alt_at_sun_m6"] >= h) & (M["elong"] < 0))[mo == m]) for m in range(1, 13)}
    # Sirius heralds dawn 27 Jul - 1 Sep (Julian) per the stars section for 1178 BC
    sir = ((mo == 7) & (d >= 27)) | (mo == 8) | ((mo == 9) & (d <= 1))
    ven = visible_av(V, 7)
    jup = visible_av(J, 10)
    mar = visible_av(A, 10) & (A["mag"] <= -1.0)
    out["any_herald_venus_jupiter_sirius_mars"] = frac(ven | jup | sir | mar)
    out["no_herald"] = frac(~(ven | jup | sir | mar))
    out["not_venus_but_other_herald"] = frac(~ven & (jup | sir | mar))
    out["venus_faintest_mag_when_visible"] = float(np.nanmax(V["mag"][ven]))
    out["jupiter_brightest_mag"] = float(np.nanmin(J["mag"]))
    out["venus_visible_AV5_by_month"] = {int(m): frac(visible_av(V, 5)[mo == m]) for m in range(1, 13)}
    return out


def jdn_to_julian_inv(y, m, d):
    """Julian calendar date (astronomical year) to JDN."""
    a = (14 - m) // 12
    yy = y + 4800 - a
    mm = m + 12 * a - 3
    return d + (153 * mm + 2) // 5 + 365 * yy + yy // 4 - 32083


if __name__ == "__main__":
    secs = sys.argv[1:] or ["all"]
    if "planets" in secs or "all" in secs:
        run_planets()
        save("venus", venus_section())
        save("mercury", mercury_section())
    if "venus" in secs:
        save("venus", venus_section())
    if "mercury" in secs:
        save("mercury", mercury_section())
    if "mercury_events" in secs or "all" in secs:
        save("mercury_events", mercury_events_section())
    if "stars" in secs or "all" in secs:
        save("stars", stars_section())
    if "moon" in secs or "all" in secs:
        save("moon", moon_section())
    if "bm_rates" in secs or "all" in secs:
        save("bm_rates", bm_rates_section())
    if "herald" in secs or "all" in secs:
        save("herald", herald_section())
    print("done")
