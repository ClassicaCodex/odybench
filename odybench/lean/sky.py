"""
odybench.lean.sky -- the astronomy of the lean run (LEAN.md; DESIGN 0, 3.2, 4.3, 4.5).

What it computes, vectorised over many days at once:

* rise and set instants and azimuths of the Sun, Venus, Mercury and Mars at a
  site, with the Sun's altitude at the instant (the arcus visionis of a
  planet's rising);
* geocentric apparent ecliptic longitude and latitude of date, and the signed
  geocentric elongation (east positive);
* Mercury's events: the rise-azimuth maxima by the vertex of a least-squares
  parabola through 7 mornings (DESIGN 3.2 step 5), with curvature, margin and
  the flatness flag; greatest western elongations; stations;
* the end of evening nautical twilight, star altitudes then, and the season
  bounds C_rel (DESIGN 4.5): A(y), P(y) with h_A, h_P calibrated at -1177;
* the March equinox (apparent solar longitude 0 deg);
* Mercury's visual magnitude (Mallama & Hilton 2018) and the PLSV visibility
  test of DESIGN 3.2 (AV = 10.5 + 1.4 m at a 1 deg critical altitude).

Conventions (DESIGN 0, 3.2, 10.2):

* Positions come from odybench.ephem (validated DE441/DE431, Vondrak 2011
  precession, IAU 2000A nutation).  Planets, the Sun and stars use DE441;
  lunar-timed quantities (conjunctions) use DE431 with SMH2020 Delta-T, in
  chunks that never straddle JD 1721425.5 (`de431_guard`).  T0b uses DE441
  throughout with B&M's clock Delta-T, 27,602.7 s (`BM_CLOCK_DT`).
* `dt` is anything ephem accepts: seconds (constant), a model name, or a
  callable year -> seconds.
* Rise: the topocentric altitude of the centre crosses h0 = -0.8333 deg (Sun)
  or -0.5667 deg (planets, stars), airless (geometric) unless
  refraction=True.  A coarse altitude grid brackets the first crossing in a
  window of the civil day; the bracket is then BISECTED until it is narrower
  than tol_s (0.1 s for Mercury, 1 s otherwise), and the instant is the linear
  interpolation of the altitude inside the final bracket.  (DESIGN 10.2 names
  Meeus' iterated hour angle for the first guess; a coarse grid is used
  instead because it cannot pick the wrong day; the bisection and its
  tolerances are DESIGN's.)
* Days are civil days (JDN = the JD of their noon) in a zone `zone_h` hours
  ahead of UT: UT+2 (`UT2`) for B&M's clock, lon/15 for LMT.
* With refraction=True the altitude is the refracted (apparent) altitude
  (skyfield's Bennett-type formula, 10 C, 1010 mbar) and the same h0 is
  used: the T0b M-sensitivity reading of "refraction on" (DESIGN 3.2 step
  10); this is a choice, recorded in the T0 output.

All calendar arithmetic goes through odybench.calendar.  Nothing here writes
files.
"""
from __future__ import annotations

import contextlib
import functools
import json
import math

import numpy as np

from odybench import calendar as cal
from odybench import ephem
from odybench.lean import PREREG_DIR

H0_SUN = -0.8333
H0_PLANET = -0.5667
BM_CLOCK_DT = 27602.7                # s; T0b's clock only (DESIGN 0, 3.2)
DE431_SPLIT_JD = 1721425.5           # DE431 excerpts meet here (DESIGN 0)
UT2 = 2.0                            # B&M's clock: zone time on 30 deg E
DAY_S = 86400.0

TOL_S = {"mercury": 0.1}             # bisection tolerance, s (DESIGN 10.2); default 1 s
INFERIOR = ("sun", "mercury", "venus")


# ------------------------------------------------------------------ sites

@functools.lru_cache(maxsize=None)
def _sites():
    return json.loads((PREREG_DIR / "sites.json").read_text(encoding="utf-8"))["sites"]


def site(key: str = "ithaki"):
    """(lat, lon, elev_m) of a row of data/prereg/sites.json (DESIGN 0)."""
    s = _sites()[key]
    return float(s["lat"]), float(s["lon"]), float(s.get("elev_m", 0.0))


def h0_of(body: str) -> float:
    return H0_SUN if body in ("sun", "moon") else H0_PLANET


# -------------------------------------------------------------- ephemeris

@contextlib.contextmanager
def ephemeris(name: str = "de441"):
    """Select the SPK excerpts: 'de441' (default directory) or 'de431'."""
    if name == "de441":
        yield
    elif name == "de431":
        with ephem.use_ephemeris(ephem.EPHEM_DIR / "de431"):
            yield
    else:
        raise ValueError(name)


def de431_guard(jd_tt) -> None:
    """Refuse a DE431 request that straddles JD 1721425.5 (DESIGN 0)."""
    a = np.asarray(jd_tt, dtype=float)
    if a.size and float(a.min()) < DE431_SPLIT_JD < float(a.max()):
        raise ValueError("DE431 request straddles JD 1721425.5; split it (DESIGN 0)")


def delta_t_s(jd_tt, dt="smh2020"):
    """Delta-T (s) at TT instant(s) under `dt` (seconds, model name or callable)."""
    if isinstance(dt, (int, float, np.floating)):
        return np.full(np.shape(jd_tt), float(dt))[()] if np.ndim(jd_tt) else float(dt)
    fn = ephem.DT_MODELS[dt][0] if isinstance(dt, str) else dt
    return fn(cal.julian_epoch(jd_tt))


def ut_of_tt(jd_tt, dt="smh2020"):
    """UT1 JD of a TT instant (Delta-T evaluated at the TT instant; calendar.ut_from_tt)."""
    return cal.ut_from_tt(jd_tt, delta_t_s(jd_tt, dt))


def tt_of_ut(jd_ut, dt="smh2020"):
    """TT JD of a UT1 instant, by two fixed-point steps (Delta-T changes < 1 s/day)."""
    jd_ut = np.asarray(jd_ut, dtype=float)
    tt = jd_ut + delta_t_s(jd_ut, dt) / DAY_S
    tt = jd_ut + delta_t_s(tt, dt) / DAY_S
    return tt[()] if tt.ndim == 0 else tt


# ------------------------------------------------------------ positions

def _refract(alt):
    from skyfield.earthlib import refract
    return refract(np.asarray(alt, dtype=float), 10.0, 1010.0)


def _ecliptic_of_date(t, xyz_au):
    """Apparent GCRS vector(s) -> (lon, lat) deg on the true ecliptic and
    equinox of date (t.M carries ephem's Vondrak precession + nutation)."""
    x, y, z = np.einsum("ij...,j...->i...", t.M, xyz_au)
    eps = ephem.mean_obliquity(t.tt) + t._nutation_angles_radians[1]
    yl = y * np.cos(eps) + z * np.sin(eps)
    zl = -y * np.sin(eps) + z * np.cos(eps)
    return np.degrees(np.arctan2(yl, x)) % 360.0, np.degrees(np.arctan2(zl, np.hypot(x, yl)))


def _geo(name, t):
    k = ephem.kernel(t.tt, ("sun", "earth") + ((name,) if name in ephem.BODY_NAMES and name != "sun" else ()))
    return k["earth"].at(t).observe(ephem._target(name, k)).apparent(deflectors=(10,))


def geo_ecliptic(bodies, jd_tt, eph="de441"):
    """{body: (lon_deg, lat_deg)}: geocentric apparent ecliptic coordinates of
    date at TT instant(s).  Independent of Delta-T."""
    jd = np.atleast_1d(np.asarray(jd_tt, dtype=float))
    if eph == "de431":
        de431_guard(jd)
    out = {}
    with ephemeris(eph):
        t = ephem.time_tt(jd, 0.0)
        for b in bodies:
            out[b] = _ecliptic_of_date(t, _geo(b, t).xyz.au)
    return out


def _signed_elong_from(t, body):
    """Signed geocentric elongation (deg, east positive; sign of the wrapped
    longitude difference) and the body's ecliptic longitude, at Time t."""
    a = _geo(body, t)
    s = _geo("sun", t)
    sep = a.separation_from(s).degrees
    lb, _ = _ecliptic_of_date(t, a.xyz.au)
    ls, _ = _ecliptic_of_date(t, s.xyz.au)
    dl = (lb - ls + 180.0) % 360.0 - 180.0
    return np.where(dl < 0, -sep, sep), lb


def signed_elongation(body, jd_tt, eph="de441"):
    """(signed elongation deg, ecliptic longitude deg) of `body` at TT instant(s)."""
    jd = np.atleast_1d(np.asarray(jd_tt, dtype=float))
    with ephemeris(eph):
        t = ephem.time_tt(jd, 0.0)
        return _signed_elong_from(t, body)


def altaz(bodies, jd_ut, lat, lon, dt="smh2020", eph="de441", refraction=False, elev_m=0.0):
    """{body: (alt_deg, az_deg)} topocentric at UT1 instant(s), sharing one
    Time.  Bodies may be planets, 'sun', 'moon' or star keys of ephem."""
    jd = np.atleast_1d(np.asarray(jd_ut, dtype=float))
    out = {}
    with ephemeris(eph):
        t = ephem.time_ut(jd, dt)
        if eph == "de431":
            de431_guard(t.tt)
        for b in bodies:
            alt, az, _ = ephem.apparent(b, t, lat, lon, elev_m).altaz()
            a = alt.degrees
            out[b] = (_refract(a) if refraction else a, az.degrees)
    return out


def sun_alt(jd_ut, lat, lon, dt="smh2020", eph="de441"):
    return altaz(("sun",), jd_ut, lat, lon, dt, eph)["sun"][0]


# ------------------------------------------------------------- crossings

def day_start_ut(day_jdn, zone_h):
    """UT JD of 0 h of civil day `day_jdn` in a zone zone_h hours ahead of UT."""
    return np.asarray(day_jdn, dtype=float) - 0.5 - np.asarray(zone_h, dtype=float) / 24.0


def crossing(body, day_jdn, lat, lon, *, zone_h=UT2, h0=None, rising=True, dt="smh2020",
             eph="de441", window_h=(0.0, 24.0), step_min=30.0, tol_s=None,
             refraction=False, elev_m=0.0, with_sun=True, with_elong=False):
    """The first rising (or setting) of `body` through altitude h0 in the
    window [window_h[0], window_h[1]) hours of each civil day `day_jdn` of the
    zone `zone_h`.

    Returns a dict of arrays (length n; NaN where there is no crossing in the
    window):
      jd_ut     the instant (UT1 JD), bisected to tol_s then interpolated;
      az        the body's azimuth then (deg, north through east);
      sun_alt   the Sun's altitude then (deg; with_sun, body != 'sun');
      elong, lon_ecl   the signed geocentric elongation and ecliptic
                longitude of date then (with_elong);
      bracket_s the width of the final bracket (s).
    """
    day = np.atleast_1d(np.asarray(day_jdn)).astype(np.int64)
    n = day.size
    h0 = h0_of(body) if h0 is None else float(h0)
    tol = TOL_S.get(body, 1.0) if tol_s is None else float(tol_s)
    t0 = day_start_ut(day, zone_h) + window_h[0] / 24.0
    k = int(round((window_h[1] - window_h[0]) * 60.0 / step_min))
    steps = np.arange(k + 1) * (step_min / 1440.0)
    grid = t0[:, None] + steps[None, :]
    sgn = 1.0 if rising else -1.0

    def f(jd):
        return sgn * (altaz((body,), jd, lat, lon, dt, eph, refraction, elev_m)[body][0] - h0)

    fg = f(grid.ravel()).reshape(n, k + 1)
    cross = (fg[:, :-1] < 0.0) & (fg[:, 1:] >= 0.0)
    has = cross.any(axis=1)
    i = np.argmax(cross, axis=1)
    rows = np.nonzero(has)[0]
    out = dict(jd_ut=np.full(n, np.nan), az=np.full(n, np.nan), bracket_s=np.full(n, np.nan))
    if with_sun and body != "sun":
        out["sun_alt"] = np.full(n, np.nan)
    if with_elong:
        out["elong"] = np.full(n, np.nan)
        out["lon_ecl"] = np.full(n, np.nan)
    if rows.size == 0:
        return out
    a = grid[rows, i[rows]].copy()
    b = grid[rows, i[rows] + 1].copy()
    fa = fg[rows, i[rows]].copy()
    fb = fg[rows, i[rows] + 1].copy()
    nsteps = max(0, int(math.ceil(math.log2(step_min * 60.0 / tol))))
    for _ in range(nsteps):
        m = 0.5 * (a + b)
        fm = f(m)
        left = fm < 0.0
        a = np.where(left, m, a)
        fa = np.where(left, fm, fa)
        b = np.where(left, b, m)
        fb = np.where(left, fb, fm)
    den = np.where(fb - fa == 0.0, 1.0, fb - fa)
    root = a + (-fa) * (b - a) / den
    root = np.clip(root, a, b)
    names = (body,) + (("sun",) if (with_sun and body != "sun") else ())
    with ephemeris(eph):
        t = ephem.time_ut(root, dt)
        for nm in names:
            alt, az, _ = ephem.apparent(nm, t, lat, lon, elev_m).altaz()
            if nm == body:
                out["az"][rows] = az.degrees
            else:
                aa = alt.degrees
                out["sun_alt"][rows] = _refract(aa) if refraction else aa
        if with_elong:
            el, lb = _signed_elong_from(t, body)
            out["elong"][rows] = el
            out["lon_ecl"][rows] = lb
    out["jd_ut"][rows] = root
    out["bracket_s"][rows] = (b - a) * DAY_S
    return out


def rise(body, day_jdn, lat, lon, **kw):
    """crossing(rising=True); see crossing."""
    return crossing(body, day_jdn, lat, lon, rising=True, **kw)


def set_(body, day_jdn, lat, lon, **kw):
    """crossing(rising=False); see crossing."""
    return crossing(body, day_jdn, lat, lon, rising=False, **kw)


def morning_window(body):
    """The search window (hours of the UT+2 or LMT civil day) for a morning
    rising: every rising of the Sun, Mercury and Venus at 38 N falls in
    00:00-14:00 local (elongation <= 47 deg); other bodies use the whole day."""
    return (0.0, 14.0) if body in INFERIOR else (0.0, 24.0)


def rise_lead(day_jdn, lat, lon, body="venus", **kw):
    """Venus-type lead on civil day(s): (sunrise - body rise) in minutes,
    with both risings and the Sun's altitude at the body's rising.  Positive
    when the body rises before the Sun.  NaN where either rising is missing."""
    kw.setdefault("window_h", morning_window(body))
    b = crossing(body, day_jdn, lat, lon, rising=True, **kw)
    kw2 = dict(kw)
    kw2.pop("with_elong", None)
    s = crossing("sun", day_jdn, lat, lon, rising=True, **kw2)
    lead = (s["jd_ut"] - b["jd_ut"]) * 1440.0
    return dict(lead_min=lead, body_rise=b["jd_ut"], sun_rise=s["jd_ut"],
                sun_alt_at_body_rise=b.get("sun_alt"), body_az=b["az"])


# --------------------------------------------------------- Mercury events

AZMAX_DTYPE = [("day_jdn", "i8"), ("jd_ut", "f8"), ("az", "f8"), ("curv", "f8"),
               ("margin", "f8"), ("flat", "?"), ("complete", "?"), ("elong", "f8"),
               ("morning", "?")]
EVENT_DTYPE = [("jd_tt", "f8"), ("jd_ut", "f8"), ("kind", "U1"), ("value", "f8"),
               ("elong", "f8"), ("morning", "?")]

FLAT_MARGIN_DEG = 0.001          # DESIGN 3.2 step 5 [rev #12 fix 3]
FLAT_CURV_DEG_D2 = 0.002


def segments(day_jdn):
    """Index ranges [i0, i1) of runs of consecutive days in a sorted JDN array."""
    d = np.asarray(day_jdn, dtype=np.int64)
    if d.size == 0:
        return []
    br = np.nonzero(np.diff(d) != 1)[0] + 1
    starts = np.concatenate(([0], br))
    ends = np.concatenate((br, [d.size]))
    return list(zip(starts.tolist(), ends.tolist()))


def lsq_parabola(x, y):
    """Least-squares y = a x^2 + b x + c; returns (a, b, c)."""
    A = np.vstack([x * x, x, np.ones_like(x)]).T
    sol, *_ = np.linalg.lstsq(A, y, rcond=None)
    return sol


def azimuth_maxima(day_jdn, jd_ut, az, elong=None, npts=7):
    """Rise-azimuth maxima of a daily rising series (DESIGN 3.2 step 5, 4.3).

    A discrete local maximum is a day i with az[i] >= az[i-1] and
    az[i] > az[i+1] (consecutive days).  Its vertex is that of the
    least-squares parabola through the `npts` (7) daily azimuths centred on
    day i, with the rising instants as abscissae; `complete` is False when the
    7 days are not all inside the series (then the vertex is not computed and
    jd_ut is the discrete maximum's rising instant).  curv = 2a (deg/d^2,
    negative at a maximum); margin = az[i] - max(az[i-1], az[i+1]); flat if
    margin < 0.001 deg or |curv| < 0.002 deg/d^2.  `elong` (signed, east
    positive) is interpolated at the vertex; morning = elong < 0 there."""
    d = np.asarray(day_jdn, dtype=np.int64)
    x = np.asarray(jd_ut, dtype=float)
    y = np.asarray(az, dtype=float)
    e = None if elong is None else np.asarray(elong, dtype=float)
    h = npts // 2
    rows = []
    for i0, i1 in segments(d):
        yy = y[i0:i1]
        for j in range(1, i1 - i0 - 1):
            if not (np.isfinite(yy[j - 1]) and np.isfinite(yy[j]) and np.isfinite(yy[j + 1])):
                continue
            if not (yy[j] >= yy[j - 1] and yy[j] > yy[j + 1]):
                continue
            i = i0 + j
            margin = yy[j] - max(yy[j - 1], yy[j + 1])
            lo, hi = i - h, i + h + 1
            complete = lo >= i0 and hi <= i1 and bool(np.all(np.isfinite(y[lo:hi])))
            if complete:
                xs = x[lo:hi] - x[i]
                a, b, c = lsq_parabola(xs, y[lo:hi])
                curv = 2.0 * a
                if a < 0:
                    xv = -b / (2.0 * a)
                    jv = x[i] + xv
                    azv = c - b * b / (4.0 * a)
                else:                       # not a maximum of the fit
                    jv, azv = x[i], y[i]
            else:
                curv, jv, azv = np.nan, x[i], y[i]
            flat = bool(margin < FLAT_MARGIN_DEG or (np.isfinite(curv) and abs(curv) < FLAT_CURV_DEG_D2))
            ev = np.nan
            if e is not None:
                lo2, hi2 = max(i0, i - h), min(i1, i + h + 1)
                ev = float(np.interp(jv, x[lo2:hi2], e[lo2:hi2]))
            rows.append((int(d[i]), float(jv), float(azv), float(curv), float(margin), flat,
                         bool(complete), ev, bool(ev < 0) if np.isfinite(ev) else False))
    return np.array(rows, dtype=AZMAX_DTYPE)


def _vertex3(x, y):
    """Vertex abscissa of the parabola through three points (vectorised)."""
    x0, x1, x2 = x
    y0, y1, y2 = y
    d0 = (y1 - y0) / (x1 - x0)
    d1 = (y2 - y1) / (x2 - x1)
    a = (d1 - d0) / (x2 - x0)
    b = d0 - a * (x0 + x1)
    with np.errstate(divide="ignore", invalid="ignore"):
        v = -b / (2.0 * a)
    return np.where(np.isfinite(v), v, x1)


def geo_events(body, seg_tt, eph="de441", dt="smh2020"):
    """Greatest elongations and stations of `body` within daily TT grids.

    seg_tt: a list of 1-d arrays, each a run of consecutive daily TT instants
    (step 1 d).  An extremum of the signed geocentric elongation (west: a
    local minimum below 0, kind 'W'; east: local maximum above 0, kind 'E')
    or of the ecliptic longitude (kind 'D' where the motion turns direct, a
    longitude minimum; 'R' where it turns retrograde, a maximum) is located on
    the daily grid and refined twice by a 3-point parabola (daily, then at
    +-0.25 d).  Returns a record array EVENT_DTYPE with the elongation and the
    morning flag (elong < 0) at the event.

    The elongation is the geocentric ANGULAR separation from the true Sun,
    signed by the side (the sign of the longitude difference): "greatest
    western elongation" is the maximum of that angle west of the Sun, the
    usual modern definition.  (check_gbm.py used the longitude difference;
    the two instants differ by a fraction of a day when Mercury's latitude is
    large.)  A "morning station" is a station with Mercury west of the Sun,
    in practice the turn to direct motion after inferior conjunction."""
    segs = [np.asarray(s, dtype=float) for s in seg_tt if len(s) >= 3]
    if not segs:
        return np.zeros(0, dtype=EVENT_DTYPE)
    allt = np.concatenate(segs)
    el, lb = signed_elongation(body, allt, eph)
    cand = []                                   # (t_prev, t, t_next, kind)
    off = 0
    for s in segs:
        m = len(s)
        e = el[off:off + m]
        lu = np.degrees(np.unwrap(np.radians(lb[off:off + m])))
        for j in range(1, m - 1):
            if e[j] < 0 and e[j] <= e[j - 1] and e[j] < e[j + 1]:
                cand.append((s[j - 1], s[j], s[j + 1], "W"))
            if e[j] > 0 and e[j] >= e[j - 1] and e[j] > e[j + 1]:
                cand.append((s[j - 1], s[j], s[j + 1], "E"))
            if lu[j] <= lu[j - 1] and lu[j] < lu[j + 1]:
                cand.append((s[j - 1], s[j], s[j + 1], "D"))
            if lu[j] >= lu[j - 1] and lu[j] > lu[j + 1]:
                cand.append((s[j - 1], s[j], s[j + 1], "R"))
        off += m
    if not cand:
        return np.zeros(0, dtype=EVENT_DTYPE)
    t3 = np.array([[c[0], c[1], c[2]] for c in cand]).T
    kinds = np.array([c[3] for c in cand])
    is_el = np.isin(kinds, ["W", "E"])

    def series(tt):
        e2, l2 = signed_elongation(body, tt.ravel(), eph)
        return e2.reshape(tt.shape), l2.reshape(tt.shape)

    def value(e2, l2, ref):
        lu2 = ref[None, :] + ((l2 - ref[None, :] + 180.0) % 360.0 - 180.0)
        return np.where(is_el[None, :], e2, lu2)

    e3, l3 = series(t3)
    ref = l3[1]
    v1 = _vertex3(t3, value(e3, l3, ref))
    v1 = np.clip(v1, t3[0], t3[2])
    t3b = np.vstack([v1 - 0.25, v1, v1 + 0.25])
    e3b, l3b = series(t3b)
    v2 = _vertex3(t3b, value(e3b, l3b, ref))
    v2 = np.where(np.abs(v2 - v1) <= 0.5, v2, v1)
    ef, lf = signed_elongation(body, v2, eph)
    val = np.where(is_el, ef, lf)
    out = np.zeros(len(cand), dtype=EVENT_DTYPE)
    out["jd_tt"] = v2
    out["jd_ut"] = ut_of_tt(v2, dt)
    out["kind"] = kinds
    out["value"] = val
    out["elong"] = ef
    out["morning"] = ef < 0
    return out[np.argsort(v2, kind="stable")]


def nearest(t, events_t):
    """|t - nearest event instant| (days) for each t; inf if there is none.
    Equidistant events: the earlier (index returned is the earlier)."""
    t = np.atleast_1d(np.asarray(t, dtype=float))
    ev = np.sort(np.asarray(events_t, dtype=float))
    if ev.size == 0:
        return np.full(t.shape, np.inf), np.full(t.shape, -1)
    k = np.searchsorted(ev, t)
    lo = np.clip(k - 1, 0, ev.size - 1)
    hi = np.clip(k, 0, ev.size - 1)
    dlo = np.abs(t - ev[lo])
    dhi = np.abs(ev[hi] - t)
    take_hi = dhi < dlo
    d = np.where(take_hi, dhi, dlo)
    idx = np.where(take_hi, hi, lo)
    d = np.where(np.isfinite(t), d, np.inf)
    return d, idx


# ---------------------------------------------------- twilight and C_rel

def evening_twilight(day_jdn, lat, lon, depression=-12.0, dt="smh2020", eph="de441", zone_h=None):
    """UT instant at which the Sun's centre sinks through `depression` deg on
    the evening of civil day day_jdn (LMT at the site by default), searched in
    15:00-23:00 local, bisected to 1 s."""
    z = lon / 15.0 if zone_h is None else zone_h
    r = crossing("sun", day_jdn, lat, lon, zone_h=z, h0=depression, rising=False, dt=dt,
                 eph=eph, window_h=(15.0, 23.0), step_min=60.0, tol_s=1.0, with_sun=False)
    return r["jd_ut"]


def star_alt_at(star, jd_ut, lat, lon, dt="smh2020", eph="de441"):
    return altaz((star,), jd_ut, lat, lon, dt, eph)[star][0]


A_RANGE = ((1, 20), (3, 25))       # Julian (month, day) evenings searched for A(y)
P_RANGE = ((3, 10), (4, 30))       # and for P(y); A spans about 8 Feb..3 Mar and
                                   # P about 29 Mar..12 Apr over -1999..+200 (DESIGN 2.9 rates)


def _evenings(y, rng):
    a = cal.jdn_from_julian(y, *rng[0])
    b = cal.jdn_from_julian(y, *rng[1])
    return np.arange(a, b + 1, dtype=np.int64)


def season_altitudes(years, lat, lon, dt="smh2020", eph="de441"):
    """For each Julian year: (A evenings, Arcturus alt), (P evenings,
    Alcyone alt) at the end of evening nautical twilight (Sun -12 deg).
    Returns {y: (jdnA, altA, jdnP, altP)}."""
    years = [int(y) for y in np.atleast_1d(years)]
    ja = [_evenings(y, A_RANGE) for y in years]
    jp = [_evenings(y, P_RANGE) for y in years]
    alld = np.concatenate(ja + jp)
    tw = evening_twilight(alld, lat, lon, -12.0, dt, eph)
    alts = altaz(("arcturus", "alcyone"), tw, lat, lon, dt, eph)
    arc, alc = alts["arcturus"][0], alts["alcyone"][0]
    out, off = {}, 0
    for y, a in zip(years, ja):
        out[y] = [a, arc[off:off + len(a)]]
        off += len(a)
    for y, p in zip(years, jp):
        out[y] += [p, alc[off:off + len(p)]]
        off += len(p)
    return {y: tuple(v) for y, v in out.items()}


CREL_CAL_YEAR = -1177
CREL_CAL_A = (2, 17)               # B&M's applied bounds [bm 5 C]: A(-1177) = 17 Feb
CREL_CAL_P = (4, 4)                # P(-1177) = 4 Apr


def calibrate_crel(lat, lon, dt="smh2020", eph="de441"):
    """h_A, h_P (deg) such that A(-1177) = 17 Feb and P(-1177) = 4 Apr; where
    a range of values gives the date, its midpoint (DESIGN 4.5).  Only the two
    thresholds are returned (published, DESIGN 2.9: 2.04 and 0.92 deg)."""
    y = CREL_CAL_YEAR
    ja, aa, jp, ap = season_altitudes([y], lat, lon, dt, eph)[y]
    i = int(np.nonzero(ja == cal.jdn_from_julian(y, *CREL_CAL_A))[0][0])
    j = int(np.nonzero(jp == cal.jdn_from_julian(y, *CREL_CAL_P))[0][0])
    # A = first evening with alt >= h_A: alt[i-1] < h_A <= alt[i]
    # P = last evening with alt >= h_P:  alt[j+1] < h_P <= alt[j]
    if not (aa[i - 1] < aa[i] and ap[j + 1] < ap[j]):
        raise RuntimeError("C_rel calibration: altitudes not monotone at -1177")
    return 0.5 * (aa[i - 1] + aa[i]), 0.5 * (ap[j] + ap[j + 1])


def season_bounds_from(alts, h_A, h_P):
    """{y: (A_jdn, P_jdn, ok)} from season_altitudes output.  A(y) = first
    evening of A_RANGE with Arcturus >= h_A, P(y) = last evening of P_RANGE
    with Alcyone >= h_P; ok is False if the threshold is already met on the
    first A evening, or still met on the last P evening (range too short)."""
    out = {}
    for y, (ja, aa, jp, ap) in alts.items():
        ia = np.nonzero(aa >= h_A)[0]
        ip = np.nonzero(ap >= h_P)[0]
        ok = bool(len(ia) and ia[0] > 0 and len(ip) and ip[-1] < len(ap) - 1)
        A = int(ja[ia[0]]) if len(ia) else -1
        P = int(jp[ip[-1]]) if len(ip) else -1
        out[y] = (A, P, ok)
    return out


# --------------------------------------------------------------- equinox

def march_equinox(years, eph="de441"):
    """TT JD of the March equinox (apparent geocentric solar longitude of date
    0 deg) of each Julian year, bracketed on a daily grid 1 Mar..30 Apr and
    bisected to 0.1 s."""
    years = np.atleast_1d(np.asarray(years, dtype=np.int64))
    a0 = np.array([cal.jd_from_julian(int(y), 3, 1) for y in years])
    nd = 61
    grid = a0[:, None] + np.arange(nd)[None, :]
    lon = geo_ecliptic(("sun",), grid.ravel(), eph)["sun"][0].reshape(grid.shape)
    w = (lon + 180.0) % 360.0 - 180.0             # signed, crosses 0 upward
    cross = (w[:, :-1] < 0) & (w[:, 1:] >= 0)
    if not cross.any(axis=1).all():
        raise RuntimeError("equinox not bracketed in 1 Mar..30 Apr")
    i = np.argmax(cross, axis=1)
    r = np.arange(len(years))
    a, b = grid[r, i], grid[r, i + 1]
    for _ in range(int(math.ceil(math.log2(DAY_S / 0.1)))):
        m = 0.5 * (a + b)
        lm = geo_ecliptic(("sun",), m, eph)["sun"][0]
        neg = ((lm + 180.0) % 360.0 - 180.0) < 0
        a = np.where(neg, m, a)
        b = np.where(neg, b, m)
    return 0.5 * (a + b)


# ----------------------------------------------------- magnitude and PLSV

def mercury_magnitude(jd_tt, eph="de441", sun="true"):
    """Mercury's V magnitude, Mallama & Hilton (2018) (the formula of
    skyfield.magnitudelib), from the geocentric astrometric vectors of
    Mercury and the Sun (light-time of each).  sun='ssb' puts the Sun at the
    barycentre, as skyfield.magnitudelib does (for its test only)."""
    jd = np.atleast_1d(np.asarray(jd_tt, dtype=float))
    with ephemeris(eph):
        t = ephem.time_tt(jd, 0.0)
        k = ephem.kernel(t.tt, ("sun", "earth", "mercury"))
        e = k["earth"].at(t)
        obs = e.observe(k["mercury"])
        p = obs.xyz.au
        s = e.observe(k["sun"]).xyz.au if sun == "true" else -obs.center_barycentric.xyz.au
    sp = p - s
    r = np.linalg.norm(sp, axis=0)
    delta = np.linalg.norm(p, axis=0)
    cosph = np.sum(sp * p, axis=0) / (r * delta)
    ph = np.degrees(np.arccos(np.clip(cosph, -1.0, 1.0)))
    f = (6.3280e-02 * ph - 1.6336e-03 * ph ** 2 + 3.3644e-05 * ph ** 3 - 3.4265e-07 * ph ** 4
         + 1.6893e-09 * ph ** 5 - 3.0334e-12 * ph ** 6)
    return -0.613 + 5.0 * np.log10(r * delta) + f


def plsv_morning(day_jdn, lat, lon, dt="smh2020", eph="de441", zone_h=UT2, crit_alt=1.0):
    """PLSV visibility of Mercury on the morning of civil day day_jdn (DESIGN
    3.2 step 5): at the instant Mercury rises through the critical altitude
    1 deg (geometric), the Sun stands at or below -(10.5 + 1.4 m), m being
    Mercury's magnitude then.  Returns dict(visible, sun_alt, av, mag, jd_ut)."""
    r = crossing("mercury", day_jdn, lat, lon, zone_h=zone_h, h0=crit_alt, rising=True, dt=dt,
                 eph=eph, window_h=morning_window("mercury"), tol_s=1.0, with_sun=True)
    jd = r["jd_ut"]
    ok = np.isfinite(jd)
    mag = np.full(jd.shape, np.nan)
    if ok.any():
        mag[ok] = mercury_magnitude(tt_of_ut(jd[ok], dt), eph)
    av = 10.5 + 1.4 * mag
    vis = ok & (r["sun_alt"] <= -av)
    return dict(visible=vis, sun_alt=r["sun_alt"], av=av, mag=mag, jd_ut=jd)


def _selftest():
    """Synthetic checks only (no ephemeris): the 7-morning vertex, the flat
    flag, nearest-event ties, segments."""
    days = np.arange(1000, 1030)
    x = days - 0.75
    mx = azimuth_maxima(days, x, 110.0 - 0.03 * (x - 1012.3) ** 2, np.full(days.size, -20.0))
    assert mx.size == 1 and abs(mx["jd_ut"][0] - 1012.3) < 1e-9 and mx["morning"][0] and not mx["flat"][0]
    assert azimuth_maxima(days, x, 110.0 - 0.0005 * (x - 1012.3) ** 2)["flat"][0]
    d, i = nearest(np.array([5.0, 7.0]), np.array([4.0, 6.0, 9.0]))
    assert d.tolist() == [1.0, 1.0] and i.tolist() == [0, 1]          # ties -> the earlier event
    assert segments(np.array([1, 2, 3, 7, 8])) == [(0, 3), (3, 5)]
    print("[sky selftest] PASS")


if __name__ == "__main__":
    import sys as _sys
    if "--selftest" in _sys.argv:
        _selftest()
    else:
        print(__doc__)
