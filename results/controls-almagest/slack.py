"""
Observer slack of the Almagest records against DE441 (odybench.ephem).

For every record in records.py: the instant the words imply, then what DE441
says about the stated phenomenon (greatest elongation, opposition, conjunction,
lunar position, eclipse, equinox) and how far, in days, the stated date lies
from the true event.  Writes slack.json and prints the tables to stdout
(captured as slack.out.txt).

    cd C:\\Projects\\odybench && py results/controls-almagest/slack.py > results/controls-almagest/slack.out.txt

DE441 excerpts for AD 120-145 and 296-224 BC are in results/controls-almagest/ephem/
(fetch_ephem_almagest.py); Hipparcos stars in stars.json (fetch_stars.py) are
ADDED IN MEMORY to ephem.HIP_STARS (ephem.py itself is not modified).
Delta-T: 'smh2020' (Morrison et al. 2021 spline; ephem.dt_smh2020).
"""
import json, math, sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
from odybench import ephem as E          # noqa: E402
import records as RC                      # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
DT = "smh2020"
EDIR = HERE / "ephem"
STARS = json.loads((HERE / "stars.json").read_text(encoding="utf-8"))["stars"]
for k, v in STARS.items():
    E.HIP_STARS.setdefault(k, tuple(v))
CHALDEAN = {"IX.7.15", "IX.7.16", "XI.7.2"}     # Chaldean-calendar records: Babylon assumed for local quantities
H0_SUN, H0_PT = -0.8333, -0.5667


def wrap(x):
    return (np.asarray(x) + 180.0) % 360.0 - 180.0


def site_of(r):
    return RC.BABYLON if r["id"] in CHALDEAN else RC.ALEXANDRIA


# ------------------------------------------------------------- coordinates
def ecl(name, jd_ut, site=None):
    """Apparent ecliptic longitude/latitude of date (deg) and distance (au); topocentric if site."""
    jd_ut = np.asarray(jd_ut, dtype=float)
    t = E.time_ut(jd_ut, DT)
    lat, lon = (None, None) if site is None else site
    a = E.apparent(name, t, lat, lon)
    v = a.xyz.au
    x, y, z = np.einsum("ij...,j...->i...", t.M, v)
    eps = E.mean_obliquity(t.tt) + t._nutation_angles_radians[1]
    yl = y * np.cos(eps) + z * np.sin(eps)
    zl = -y * np.sin(eps) + z * np.cos(eps)
    lam = np.degrees(np.arctan2(yl, x)) % 360.0
    bet = np.degrees(np.arctan2(zl, np.hypot(x, yl)))
    return lam, bet, np.sqrt(x * x + y * y + z * z)


def sep(name1, name2, jd_ut, site=None):
    jd_ut = np.asarray(jd_ut, dtype=float)
    t = E.time_ut(jd_ut, DT)
    lat, lon = (None, None) if site is None else site
    a = E.apparent(name1, t, lat, lon)
    b = E.apparent(name2, t, lat, lon)
    return a.separation_from(b).degrees


def mean_sun(jd_ut):
    """Meeus (1998) eq. 25.2 geometric mean longitude of the Sun, mean equinox of date (deg)."""
    jd_tt = np.asarray(jd_ut) + E.delta_t(E.julian_epoch(jd_ut), DT) / 86400.0
    T = (jd_tt - 2451545.0) / 36525.0
    return (280.46646 + 36000.76983 * T + 0.0003032 * T * T) % 360.0


def alt(name, jd_ut, site):
    return np.asarray(E.altaz(name, jd_ut, site[0], site[1], dt=DT)[0])


def lat_hours(jd_ut, site):
    return float(E.local_apparent_solar_time(jd_ut, site[0], site[1], dt=DT))


# --------------------------------------------------------------- instants
def civil_noon_ut(r, month=None, day=None):
    """UT JD of local (mean) noon of the civil day the words point to."""
    jd = RC.nab_jd_noon(r["nab"], month or r["month"], day or r["day"]) + RC.civil_day_offset(r["part"])
    return jd - site_of(r)[1] / 360.0


def crossing(name, jd0, jd1, h0, site, rising):
    g = np.linspace(jd0, jd1, 241)
    a = alt(name, g, site) - h0
    idx = np.nonzero((a[:-1] < 0) & (a[1:] >= 0))[0] if rising else np.nonzero((a[:-1] >= 0) & (a[1:] < 0))[0]
    if len(idx) == 0:
        return None
    i = idx[0] if rising else idx[-1]
    f = lambda x: float(alt(name, x, site)) - h0
    return brentq(f, g[i], g[i + 1], xtol=1e-6)


def instant(r, month=None, day=None):
    s = site_of(r)
    noon = civil_noon_ut(r, month, day)
    part = r["part"]
    if part == "evening":            # Sun 8 deg below the horizon after sunset (my convention for 'evening')
        return crossing("sun", noon + 0.1, noon + 0.45, -8.0, s, rising=False)
    if part == "morning":            # Sun 8 deg below the horizon before sunrise (my convention for 'dawn')
        return crossing("sun", noon - 0.45, noon - 0.1, -8.0, s, rising=True)
    target = {"h_before_midnight": 24 - r.get("hours", 0), "h_after_midnight": r.get("hours", 0),
              "h_after_noon": 12 + r.get("hours", 0), "h_before_noon": 12 - r.get("hours", 0), "noon": 12.0}[part]
    jd = noon + (target - 12.0) / 24.0
    for _ in range(4):
        d = (lat_hours(jd, s) - target + 12.0) % 24.0 - 12.0
        jd -= d / 24.0
    return jd


def rise_set_offsets(name, r, jd_obs):
    """Morning: (sunrise - body rise) in min; evening: (body set - sunset) in min, on that civil day."""
    s = site_of(r)
    noon = civil_noon_ut(r)
    if r.get("side") == "W" or r["part"] in ("morning", "h_after_midnight"):
        tb = crossing(name, noon - 0.5, noon, H0_PT, s, True)
        ts = crossing("sun", noon - 0.5, noon, H0_SUN, s, True)
        return "rise lead", None if (tb is None or ts is None) else (ts - tb) * 1440.0
    tb = crossing(name, noon, noon + 0.5, H0_PT, s, False)
    ts = crossing("sun", noon, noon + 0.5, H0_SUN, s, False)
    return "set lag", None if (tb is None or ts is None) else (tb - ts) * 1440.0


# ------------------------------------------------------------ elongations
def signed_elong(name, jd):
    e = sep(name, "sun", jd)
    lp, _, _ = ecl(name, jd)
    ls, _, _ = ecl("sun", jd)
    return np.where(wrap(lp - ls) >= 0, e, -e)


def mean_elong(name, jd):
    lp, _, _ = ecl(name, jd)
    return wrap(lp - mean_sun(jd))


def nearest_extreme(func, jd_obs, side, span=100.0):
    """Nearest local extreme (max of +f for side E, min of f for side W) of func to jd_obs, refined; returns (jd, value)."""
    g = jd_obs + np.arange(-span, span + 0.5, 1.0)
    v = np.asarray(func(g)) * (1 if side == "E" else -1)
    cand = [i for i in range(1, len(g) - 1) if v[i] >= v[i - 1] and v[i] >= v[i + 1] and v[i] > 0]
    if not cand:
        return None, None
    i = min(cand, key=lambda k: abs(g[k] - jd_obs))
    ref = g[i]
    res = minimize_scalar(lambda h: -float(np.asarray(func(ref + h / 24.0))) * (1 if side == "E" else -1),
                          bounds=(-36, 36), method="bounded", options={"xatol": 1e-3})
    jd = ref + res.x / 24.0
    return jd, float(np.asarray(func(jd)))


def plateau(func, jd_ge, val, side, tol):
    g = jd_ge + np.arange(-60, 60.5, 1.0)
    v = np.asarray(func(g)) * (1 if side == "E" else -1)
    m = abs(val)
    inside = v >= m - tol
    # contiguous run around the max
    c = 60
    lo = c
    while lo > 0 and inside[lo - 1]:
        lo -= 1
    hi = c
    while hi < len(g) - 1 and inside[hi + 1]:
        hi += 1
    return int(hi - lo + 1)


def opposition(name, jd_obs, mean=False):
    def f(j):
        lp, _, _ = ecl(name, j)
        ls = mean_sun(j) if mean else ecl("sun", j)[0]
        return float(wrap(lp - ls - 180.0))
    g = jd_obs + np.arange(-40, 41, 1.0)
    v = np.array([f(x) for x in g])
    idx = [i for i in range(len(g) - 1) if np.sign(v[i]) != np.sign(v[i + 1]) and abs(v[i] - v[i + 1]) < 30]
    if not idx:
        return None
    i = min(idx, key=lambda k: abs(g[k] - jd_obs))
    return brentq(f, g[i], g[i + 1], xtol=1e-6)


def horizon_azimuth_series(name, r, jd_obs, span=45, rising=True):
    """Daily azimuth (N through E) of `name` at its rising (or setting) on each civil day within +-span days."""
    s = site_of(r)
    noon0 = civil_noon_ut(r)
    days, az = [], []
    for k in range(-span, span + 1):
        noon = noon0 + k
        tb = crossing(name, noon - 0.5, noon, H0_PT, s, True) if rising else crossing(name, noon, noon + 0.5, H0_PT, s, False)
        if tb is None:
            continue
        days.append(k)
        az.append(float(E.altaz(name, tb, s[0], s[1], dt=DT)[1]))
    return np.array(days), np.array(az)


def azimuth_extrema(days, az):
    """Parabola vertices (day offset from the record's civil day) of the local maxima and minima of a daily series."""
    out = {"max": [], "min": []}
    for i in range(1, len(az) - 1):
        if days[i + 1] - days[i - 1] != 2:
            continue
        for kind, ok in (("max", az[i] >= az[i - 1] and az[i] >= az[i + 1]), ("min", az[i] <= az[i - 1] and az[i] <= az[i + 1])):
            if ok:
                y0, y1, y2 = az[i - 1], az[i], az[i + 1]
                den = y0 - 2 * y1 + y2
                x = 0.0 if den == 0 else 0.5 * (y0 - y2) / den
                out[kind].append(days[i] + x)
    return out


# --------------------------------------------------------------- positions
def tangent(name, star, jd, site=None):
    lp, bp, _ = ecl(name, jd, site)
    ls, bs, _ = ecl(star, jd)
    return float(wrap(lp - ls)) * math.cos(math.radians(float(bs))), float(bp - bs)


def line_dist(name, s1, s2, jd):
    """Signed distance (deg) of body from the line through stars s1, s2; positive toward increasing longitude."""
    px, py = tangent(name, s1, jd)
    bx, by = tangent(s2, s1, jd) if False else _star_offset(s2, s1, jd)
    L = math.hypot(bx, by)
    ux, uy = bx / L, by / L
    nx, ny = uy, -ux
    if nx < 0:
        nx, ny = -nx, -ny
    return px * nx + py * ny, (px * ux + py * uy), L


def _star_offset(s2, s1, jd):
    l2, b2, _ = ecl(s2, jd)
    l1, b1, _ = ecl(s1, jd)
    return float(wrap(l2 - l1)) * math.cos(math.radians(float(b1))), float(b2 - b1)


def closest_approach(name, star, jd_obs, span=30):
    g = jd_obs + np.arange(-span, span + 0.5, 0.5)
    d = sep(name, star, g)
    i = int(np.argmin(d))
    res = minimize_scalar(lambda h: float(sep(name, star, g[i] + h / 24.0)), bounds=(-18, 18), method="bounded",
                          options={"xatol": 1e-3})
    jd = g[i] + res.x / 24.0
    return jd, float(sep(name, star, jd))


def lon_conjunction(name, star, jd_obs, span=30):
    f = lambda j: float(wrap(ecl(name, j)[0] - ecl(star, j)[0]))
    g = jd_obs + np.arange(-span, span + 0.5, 1.0)
    v = np.array([f(x) for x in g])
    idx = [i for i in range(len(g) - 1) if np.sign(v[i]) != np.sign(v[i + 1]) and abs(v[i] - v[i + 1]) < 20]
    if not idx:
        return None
    i = min(idx, key=lambda k: abs(g[k] - jd_obs))
    return brentq(f, g[i], g[i + 1], xtol=1e-6)


def moon_info(jd):
    e = float(sep("moon", "sun", jd))
    lm, _, _ = ecl("moon", jd)
    ls, _, _ = ecl("sun", jd)
    signed = e if float(wrap(lm - ls)) >= 0 else -e
    jd_tt = jd + float(E.delta_t(E.julian_epoch(jd), DT)) / 86400.0
    nms = E.new_moons(jd_tt - 32, jd_tt + 32)
    prev = max([x for x in nms if x <= jd_tt], default=None)
    nxt = min([x for x in nms if x > jd_tt], default=None)
    return dict(elong_signed=signed, illum=(1 - math.cos(math.radians(e))) / 2,
                age_d=None if prev is None else jd_tt - prev, to_next_d=None if nxt is None else nxt - jd_tt)


def eclipse_max(jd_obs):
    def d(j):
        lm, bm, _ = ecl("moon", j)
        ls, bs, _ = ecl("sun", j)
        return float(sep("moon", "sun", j))
    g = jd_obs + np.arange(-0.4, 0.401, 0.01)
    v = np.array([float(sep("moon", "sun", x)) for x in g])
    i = int(np.argmax(v))
    res = minimize_scalar(lambda h: -float(sep("moon", "sun", g[i] + h / 24.0)), bounds=(-0.5, 0.5), method="bounded",
                          options={"xatol": 1e-5})
    jd = g[i] + res.x / 24.0
    t = E.time_ut(jd, DT)
    m = E.apparent("moon", t)
    s = E.apparent("sun", t)
    dm, ds = m.distance().km, s.distance().km
    pm = math.asin(E.EARTH_EQ_RADIUS_KM / dm)
    ps = math.asin(E.EARTH_EQ_RADIUS_KM / ds)
    ss = math.asin(E.SUN_RADIUS_KM / ds)
    sm = math.asin(E.K_UMBRA * E.EARTH_EQ_RADIUS_KM / dm)
    rho = 1.02 * (pm + ps - ss)                                 # Chauvenet's 1/50 enlargement
    dist = math.radians(180.0 - float(sep("moon", "sun", jd)))
    mag = (rho + sm - dist) / (2 * sm)
    lm, bm, _ = ecl("moon", jd)
    ls, bs, _ = ecl("sun", jd)
    return jd, mag, float(bm + bs)          # Moon latitude relative to the antisolar point (deg; + = Moon north of shadow axis)


def equinox(jd_obs):
    f = lambda j: float(wrap(ecl("sun", j)[0]))
    return brentq(f, jd_obs - 5, jd_obs + 5, xtol=1e-7)


# ------------------------------------------------------------------- main
def analyse(r, month=None, day=None, tag="printed"):
    if month is not None:
        r = dict(r, month=month, day=day)
    out = dict(id=r["id"], ref=r["ref"], body=r["body"], reading=tag)
    s = site_of(r)
    jd = instant(r)
    out["jd_ut"] = jd
    out["date"] = E.fmt_jd(jd, "UT")
    out["site"] = "Babylon (assumed)" if r["id"] in CHALDEAN else "Alexandria"
    out["lat_hours"] = lat_hours(jd, s)
    out["sun_alt"] = float(alt("sun", jd, s))
    b = r["body"]
    if b in ("mercury", "venus", "mars", "jupiter", "saturn"):
        out["body_alt"] = float(alt(b, jd, s))
        out["elong_true"] = float(signed_elong(b, jd))
        out["elong_mean_sun"] = float(mean_elong(b, jd))
    if b in ("mercury", "venus") and r.get("side"):
        side = r["side"]
        out["side_ok"] = (out["elong_true"] > 0) == (side == "E")
        jge, vge = nearest_extreme(lambda j: signed_elong(b, j), jd, side)
        jgm, vgm = nearest_extreme(lambda j: mean_elong(b, j), jd, side)
        out["ge_true_jd"], out["ge_true_val"] = jge, vge
        out["ge_true_date"] = E.fmt_jd(jge, "UT") if jge else None
        out["off_ge_true_d"] = None if jge is None else jd - jge
        out["off_ge_mean_d"] = None if jgm is None else jd - jgm
        out["ge_mean_val"] = vgm
        out["deficit_deg"] = None if vge is None else abs(vge) - abs(out["elong_true"])
        out["plateau_0p5"] = plateau(lambda j: signed_elong(b, j), jge, vge, side, 0.5)
        out["plateau_1p0"] = plateau(lambda j: signed_elong(b, j), jge, vge, side, 1.0)
        kind, mins = rise_set_offsets(b, r, jd)
        out["rs_kind"], out["rs_min"] = kind, mins
        if b == "mercury":
            rising = side == "W"
            dd, az = horizon_azimuth_series(b, r, jd, rising=rising)
            ex = azimuth_extrema(dd, az)
            # offsets: record day (0) minus extremum day -> positive = record after the extremum
            out["az_kind"] = "rising" if rising else "setting"
            out["az_max_off_d"] = min((-x for x in ex["max"]), key=abs, default=None)
            out["az_min_off_d"] = min((-x for x in ex["min"]), key=abs, default=None)
    if r["phen"] == "opp":
        jo = opposition(b, jd)
        jm = opposition(b, jd, mean=True)
        out["opp_true_date"] = E.fmt_jd(jo, "UT") if jo else None
        out["off_opp_true_d"] = None if jo is None else jd - jo
        out["off_opp_mean_d"] = None if jm is None else jd - jm
    stars_out = []
    for st in r.get("stars", []):
        k = st["kind"]
        so = dict(kind=k, reading=st["reading"])
        if k == "offset":
            star = st["star"]
            dx, dy = tangent(b, star, jd)
            dx1, _ = tangent(b, star, jd + 1.0)
            so.update(star=star, sep=float(sep(b, star, jd)), dlon_c=dx, dlat_c=dy, dlon_rate=dx1 - dx,
                      dlon_s=st.get("dlon"), dlat_s=st.get("dlat"))
            if st.get("dlon") is not None and abs(dx1 - dx) > 1e-3:
                so["implied_day_offset"] = (dx - st["dlon"]) / (dx1 - dx)
        elif k == "line_east":
            d0, along, L = line_dist(b, st["star"], st["star2"], jd)
            d1, _, _ = line_dist(b, st["star"], st["star2"], jd + 1.0)
            so.update(star=st["star"], star2=st["star2"], dist_c=d0, dist_s=st["dist"], rate=d1 - d0,
                      implied_day_offset=(d0 - st["dist"]) / (d1 - d0) if abs(d1 - d0) > 1e-3 else None)
        elif k == "heads_line":
            d0, along, L = line_dist(b, st["star"], st["star2"], jd)
            # along: projection of body offset from Castor onto the Castor->Pollux direction
            beyond = along - L
            target = 2 * L - 1 / 6
            _, along1, _ = line_dist(b, st["star"], st["star2"], jd + 1.0)
            rate = (along1 - L) - beyond
            so.update(star=st["star"], star2=st["star2"], perp_c=d0, beyond_pollux_c=beyond, beyond_pollux_s=target,
                      castor_pollux_sep=L, rate=rate,
                      implied_day_offset=(beyond - target) / rate if abs(rate) > 1e-3 else None)
        elif k == "conj":
            star = st["star"]
            jc, smin = closest_approach(b, star, jd)
            jl = lon_conjunction(b, star, jd)
            so.update(star=star, sep=float(sep(b, star, jd)), closest_jd=jc, closest_sep=smin, off_closest_d=jd - jc,
                      off_lon_conj_d=None if jl is None else jd - jl)
        elif k == "nearest":
            ds = {c: float(sep(b, c, jd)) for c in st["candidates"]}
            c = min(ds, key=ds.get)
            dx, dy = tangent(b, c, jd)
            dx1, _ = tangent(b, c, jd + 1.0)
            so.update(star=c, seps=ds, dlon_c=dx, dlat_c=dy, dlon_s=st["dlon"],
                      implied_day_offset=(dx - st["dlon"]) / (dx1 - dx) if abs(dx1 - dx) > 1e-3 else None)
        stars_out.append(so)
    out["stars"] = stars_out
    if r.get("moon"):
        mo = r["moon"]
        dx, dy = tangent(b, "moon", jd, s) if False else _moon_rel(b, jd, s)
        dx1, _ = _moon_rel(b, jd + 1 / 24.0, s)
        m = dict(dlon_c=dx, dlat_c=dy, dlon_s=mo.get("dlon"), rate_per_h=dx1 - dx, sep=float(sep(b, "moon", jd, s)))
        if mo.get("dlon") is not None:
            m["implied_hours"] = (dx - mo["dlon"]) / (dx1 - dx)
        lm, _, _ = ecl("moon", jd, s)
        m["moon_app_lon_c"] = float(lm)
        m.update(moon_info(jd))
        out["moon"] = m
    if r.get("moonsun"):
        lm, _, _ = ecl("moon", jd, s)
        ls, _, _ = ecl("sun", jd, s)
        d = float(wrap(lm - ls))
        lm1, _, _ = ecl("moon", jd + 1 / 24.0, s)
        ls1, _, _ = ecl("sun", jd + 1 / 24.0, s)
        rate = float(wrap(lm1 - ls1)) - d
        st = r["moonsun"]["stated"]
        st = float(wrap(st))
        out["moonsun"] = dict(stated=st, computed=d, implied_hours=(d - st) / rate)
        out["moon"] = moon_info(jd)
    if r["phen"] == "ecl":
        je, mag, rel = eclipse_max(jd)
        out["eclipse"] = dict(jd_max=je, date=E.fmt_jd(je, "UT"), lat_hours=lat_hours(je, s), umbral_mag=mag,
                              moon_minus_axis_lat=rel, off_h=(jd - je) * 24.0)
    if r["phen"] == "equinox":
        jq = equinox(jd)
        out["equinox"] = dict(jd=jq, date=E.fmt_jd(jq, "UT"), off_d=jd - jq)
    return out


def _moon_rel(b, jd, s):
    lp, bp, _ = ecl(b, jd, s)
    lm, bm, _ = ecl("moon", jd, s)
    return float(wrap(lp - lm)), float(bp - bm)


def main():
    RC.resolve()
    res = []
    with E.use_ephemeris(EDIR):
        for r in RC.R:
            res.append(analyse(r))
            if r.get("emend"):
                em = r["emend"]
                res.append(analyse(r, em["month"], em["day"], tag="emended: " + em["label"]))
    (HERE / "slack.json").write_text(json.dumps(res, indent=1, default=float), encoding="utf-8")
    f = lambda x, n=1: "   -  " if x is None else f"{x:+.{n}f}"
    print("== Inner planets: offsets (record instant minus DE441 event), days; elongations in deg")
    print(f"{'id':10s} {'reading':9s} {'date (UT, proleptic Julian)':44s} {'el.true':>8s} {'GE.true':>8s} {'off.GE':>7s} "
          f"{'off.GEmean':>10s} {'defic':>6s} {'pl.5':>4s} {'pl1':>4s} {'side':>4s} {'rise/set':>14s} {'Sun alt':>7s} {'body alt':>8s}")
    for o in res:
        if "ge_true_val" not in o:
            continue
        print(f"{o['id']:10s} {o['reading'][:9]:9s} {o['date']:44s} {o['elong_true']:+8.2f} {o['ge_true_val'] or 0:+8.2f} "
              f"{f(o['off_ge_true_d'])} {f(o['off_ge_mean_d']):>10s} {o['deficit_deg']:6.2f} {o['plateau_0p5']:4d} "
              f"{o['plateau_1p0']:4d} {'ok' if o['side_ok'] else 'BAD':>4s} {o['rs_kind']:>9s} {f(o['rs_min'], 0):>5s} "
              f"{o['sun_alt']:7.1f} {o['body_alt']:8.1f}")
    print("\n== Mercury horizon-azimuth extrema: record civil day minus the vertex of the nearest local max / min of the "
          "daily azimuth (N through E) at rising (morning records) or setting (evening records), days")
    for o in res:
        if "az_kind" in o:
            print(f"{o['id']:10s} {o['reading'][:9]:9s} {o['az_kind']:8s} az-max {f(o['az_max_off_d'])}  az-min {f(o['az_min_off_d'])}")
    print("\n== Oppositions (record instant minus DE441 opposition to the true / to the mean Sun), days")
    for o in res:
        if "off_opp_true_d" in o:
            print(f"{o['id']:10s} {o['date']:44s} true {f(o['off_opp_true_d'], 2)}  mean {f(o['off_opp_mean_d'], 2)}")
    print("\n== Planet-star relations")
    for o in res:
        for s in o.get("stars", []):
            k = s["kind"]
            if k == "offset":
                print(f"{o['id']:10s} {s['star']:10s} sep {s['sep']:6.2f}  dlon {s['dlon_c']:+6.2f} (stated {s['dlon_s']})  "
                      f"dlat {s['dlat_c']:+6.2f} (stated {s['dlat_s']})  rate {s['dlon_rate']:+.3f}/d  "
                      f"implied offset {f(s.get('implied_day_offset'))} d")
            elif k == "line_east":
                print(f"{o['id']:10s} line {s['star']}-{s['star2']}: dist east {s['dist_c']:+6.2f} (stated {s['dist_s']:+.2f})  "
                      f"rate {s['rate']:+.3f}/d  implied offset {f(s['implied_day_offset'])} d")
            elif k == "heads_line":
                print(f"{o['id']:10s} Castor-Pollux line: perp {s['perp_c']:+6.2f}; beyond Pollux {s['beyond_pollux_c']:+6.2f} "
                      f"(stated {s['beyond_pollux_s']:.2f}; C-P {s['castor_pollux_sep']:.2f})  rate {s['rate']:+.3f}/d  "
                      f"implied offset {f(s['implied_day_offset'])} d")
            elif k == "conj":
                print(f"{o['id']:10s} {s['star']:10s} sep at record {s['sep']:6.3f}; closest {s['closest_sep']:6.3f} "
                      f"(record - closest {s['off_closest_d']:+.2f} d); record - lon. conj {f(s['off_lon_conj_d'], 2)} d")
            elif k == "nearest":
                print(f"{o['id']:10s} nearest {s['star']} seps {json.dumps({a: round(b, 2) for a, b in s['seps'].items()})} "
                      f"dlon {s['dlon_c']:+.2f} (stated {s['dlon_s']:+.2f}) implied offset {f(s['implied_day_offset'])} d")
    print("\n== Moon relations (topocentric Alexandria)")
    for o in res:
        m = o.get("moon")
        if m and "dlon_c" in m:
            print(f"{o['id']:10s} {o['reading'][:9]:9s} body-Moon dlon {m['dlon_c']:+6.2f} (stated {m['dlon_s']}) dlat {m['dlat_c']:+5.2f} "
                  f"sep {m['sep']:5.2f} implied {f(m.get('implied_hours'))} h | Moon elong {m['elong_signed']:+6.1f} illum {m['illum']:.2f} "
                  f"age {m['age_d']:.2f} d, to next conj {m['to_next_d']:.2f} d")
        if o.get("moonsun"):
            ms = o["moonsun"]
            print(f"{o['id']:10s} Moon-Sun stated {ms['stated']:+7.2f} computed {ms['computed']:+7.2f} implied {ms['implied_hours']:+.2f} h"
                  f" | age {o['moon']['age_d']:.2f} d, to next conj {o['moon']['to_next_d']:.2f} d")
    print("\n== Eclipse / equinox")
    for o in res:
        if "eclipse" in o:
            e = o["eclipse"]
            print(f"{o['id']:10s} greatest {e['date']} LAT {e['lat_hours']:.2f} h; umbral mag {e['umbral_mag']:.2f}; "
                  f"Moon lat rel. axis {e['moon_minus_axis_lat']:+.2f}; record - computed {e['off_h']:+.2f} h")
        if "equinox" in o:
            q = o["equinox"]
            print(f"{o['id']:10s} DE441 equinox {q['date']}; record - DE441 {q['off_d']:+.2f} d")
    print("\n== Instants used")
    for o in res:
        print(f"{o['id']:10s} {o['reading'][:40]:40s} {o['date']}  LAT {o['lat_hours']:5.2f}  Sun {o['sun_alt']:+6.1f}  {o['site']}")


if __name__ == "__main__":
    main()
