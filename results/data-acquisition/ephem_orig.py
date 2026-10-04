"""
odybench.ephem -- positions of the Sun, Moon, Mercury, Venus and bright stars
for the late Bronze Age (about 1320-1030 BC), solar-eclipse local
circumstances, and Delta-T models with their stated uncertainties.

Conventions (used everywhere in this module and its callers)
-------------------------------------------------------------
* Years are ASTRONOMICAL (1178 BC = -1177).  Calendar dates are PROLEPTIC
  JULIAN unless a function says otherwise.
* jd_tt  : Julian Date on Terrestrial Time (TT; = TD/TDT of the eclipse canons;
           TDB differs by < 2 ms, ignored).
* jd_ut  : Julian Date on UT1 (mean solar time of Greenwich).
* Delta-T = TT - UT1, seconds.  Every UT-dependent function takes `dt`, which
  is a number (seconds, held constant) or the name of a model below, or a
  callable year -> seconds.
* Local apparent solar time (LAT) = 12 h + hour angle of the true Sun.
* Longitudes east-positive, geodetic WGS84 latitudes, heights in metres.

Stack (versions recorded in docs/research-ephemeris.md)
--------------------------------------------------------
* JPL DE441 (Park et al. 2021, AJ 161:105) excerpts in data/ephem/, read by
  skyfield / jplephem.  Light-time, aberration and solar light deflection by
  skyfield (Jupiter/Saturn deflection omitted, as in JPL Horizons).
* Precession: default 'vondrak' = Vondrak, Capitaine & Wallace 2011 (A&A 534,
  A22; corrigendum A&A 541, C1) long-term precession+bias matrix via ERFA
  eraLtpb, with an Earth-rotation (sidereal time) made consistent with it by
  integrating the CIO locator s along the long-term pole path.  'iau2006' =
  skyfield's own IAU 2006 (P03) precession and GMST, which are polynomials fitted
  for a few centuries around J2000.  The difference at -1177 is quantified in
  tools/validate_ephem.py.
* Nutation: IAU 2000A (skyfield).
* Refraction (only on request): skyfield's Bennett-type formula (earthlib.refract,
  iterated from the true altitude), 10 C, 1010 mbar.
* Lunar ephemeris and Delta-T go together.  The Stephenson-Morrison-Hohenkerk
  Delta-T was derived with DE430 / analytical j=2 (n-dot -25.82 / -26.00
  "/cy^2).  DE441's Moon differs from DE431's (= DE430 lunar model) by about
  +0.0034" T^3 (T in centuries from J2000): ~ -108" (188 s of eclipse time) at
  -1177.  For Delta-T-sensitive eclipse work pair SMH Delta-T with DE431:
      with use_ephemeris(EPHEM_DIR / "de431"): ...
  See docs/research-ephemeris.md sect. 5.

This module writes nothing; it reads data/ephem/*.bsp.
"""
from __future__ import annotations

import functools
import math
from pathlib import Path

import numpy as np
import erfa
from scipy.integrate import cumulative_simpson
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq, minimize_scalar

from skyfield.api import Star, load_file, wgs84
from skyfield.earthlib import earth_rotation_angle, refract as _refract
from skyfield.functions import load_bundled_npy, mxm
from skyfield.timelib import Timescale

ROOT = Path(__file__).resolve().parents[1]
EPHEM_DIR = ROOT / "data" / "ephem"

J2000 = 2451545.0
DAY_S = 86400.0
ASEC = math.pi / 180.0 / 3600.0
AU_KM = 149597870.7
EARTH_EQ_RADIUS_KM = 6378.137          # WGS84 / IERS 2010
# Solar and lunar radii as used by Espenak & Meeus (Five Millennium Canon;
# NASA Besselian-element pages list k1, k2): solar semidiameter 959.63" at 1 au,
# lunar radius k1 = 0.272488 Earth radii for penumbral contacts / magnitude,
# k2 = 0.272281 for umbral contacts (totality).
SUN_SD_1AU_ARCSEC = 959.63
SUN_RADIUS_KM = SUN_SD_1AU_ARCSEC * ASEC * AU_KM
K_PENUMBRA = 0.272488
K_UMBRA = 0.272281

# ---------------------------------------------------------------- calendar


def jd_from_julian(year: int, month: int, day: float, hour: float = 0.0) -> float:
    """JD of a PROLEPTIC JULIAN calendar date (astronomical year).

    Meeus, Astronomical Algorithms (2nd ed.) eq. 7.1 with B = 0.
    jd_from_julian(-1177, 4, 16) == 1291263.5.
    """
    y, m = year, month
    if m <= 2:
        y -= 1
        m += 12
    return (math.floor(365.25 * (y + 4716)) + math.floor(30.6001 * (m + 1))
            + day - 1524.5 + hour / 24.0)


def julian_from_jd(jd: float):
    """(year, month, day, hours) in the PROLEPTIC JULIAN calendar."""
    z = math.floor(jd + 0.5)
    f = jd + 0.5 - z
    b = z + 1524
    c = math.floor((b - 122.1) / 365.25)
    d = math.floor(365.25 * c)
    e = math.floor((b - d) / 30.6001)
    day = b - d - math.floor(30.6001 * e)
    month = e - 1 if e < 14 else e - 13
    year = c - 4716 if month > 2 else c - 4715
    return int(year), int(month), int(day), f * 24.0


_MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


def fmt_jd(jd: float, scale: str = "UT") -> str:
    """'-1177-04-16 10:00:58 UT (16 Apr 1178 BC, proleptic Julian)'."""
    y, m, d, h = julian_from_jd(jd)
    s = round(h * 3600.0)
    if s >= 86400:          # rounding spill-over
        y, m, d, h = julian_from_jd(math.floor(jd + 0.5) + 0.5)
        s -= 86400
    hh, rem = divmod(int(s), 3600)
    mm, ss = divmod(rem, 60)
    era = f"{1 - y} BC" if y <= 0 else f"AD {y}"
    return (f"{y:+05d}-{m:02d}-{d:02d} {hh:02d}:{mm:02d}:{ss:02d} {scale} "
            f"({d} {_MONTHS[m - 1]} {era}, proleptic Julian)")


def julian_epoch(jd):
    """Julian epoch (years of 365.25 d from J2000.0) -- the 'decimal year'
    used as the argument of every Delta-T model here.  For a proleptic-Julian
    calendar date it runs about 0.034 yr (13 d) ahead of 'year + (month-0.5)/12';
    at -1177 that changes Delta-T by < 1 s."""
    return 2000.0 + (np.asarray(jd, dtype=float) - J2000) / 365.25


# ------------------------------------------------------------------ Delta-T
#
# All functions take a decimal year y (scalar or array) and return seconds.
# Provenance is given per function; docs/research-ephemeris.md has the tables.


def dt_em2006(y):
    """Espenak & Meeus (2006), Five Millennium Canon, polynomial expressions
    for Delta-T (NASA page 'Polynomial Expressions for Delta T',
    eclipse.gsfc.nasa.gov/SEcat5/deltatpoly.html).  Before -500 this is the
    Morrison & Stephenson (2004) parabola -20 + 32 u^2, u = (y-1820)/100.
    Assumes lunar n-dot = -26"/cy^2.  Valid -1999..+3000."""
    y = np.asarray(y, dtype=float)
    out = np.empty_like(y)
    u = (y - 1820) / 100
    out[...] = -20 + 32 * u ** 2                                   # < -500, > 2150
    m = (y >= -500) & (y < 500)
    u = y / 100
    out[m] = (10583.6 - 1014.41 * u + 33.78311 * u ** 2 - 5.952053 * u ** 3
              - 0.1798452 * u ** 4 + 0.022174192 * u ** 5 + 0.0090316521 * u ** 6)[m]
    m = (y >= 500) & (y < 1600)
    u = (y - 1000) / 100
    out[m] = (1574.2 - 556.01 * u + 71.23472 * u ** 2 + 0.319781 * u ** 3
              - 0.8503463 * u ** 4 - 0.005050998 * u ** 5 + 0.0083572073 * u ** 6)[m]
    m = (y >= 1600) & (y < 1700)
    t = y - 1600
    out[m] = (120 - 0.9808 * t - 0.01532 * t ** 2 + t ** 3 / 7129)[m]
    m = (y >= 1700) & (y < 1800)
    t = y - 1700
    out[m] = (8.83 + 0.1603 * t - 0.0059285 * t ** 2 + 0.00013336 * t ** 3 - t ** 4 / 1174000)[m]
    m = (y >= 1800) & (y < 1860)
    t = y - 1800
    out[m] = (13.72 - 0.332447 * t + 0.0068612 * t ** 2 + 0.0041116 * t ** 3 - 0.00037436 * t ** 4
              + 0.0000121272 * t ** 5 - 0.0000001699 * t ** 6 + 0.000000000875 * t ** 7)[m]
    m = (y >= 1860) & (y < 1900)
    t = y - 1860
    out[m] = (7.62 + 0.5737 * t - 0.251754 * t ** 2 + 0.01680668 * t ** 3
              - 0.0004473624 * t ** 4 + t ** 5 / 233174)[m]
    m = (y >= 1900) & (y < 1920)
    t = y - 1900
    out[m] = (-2.79 + 1.494119 * t - 0.0598939 * t ** 2 + 0.0061966 * t ** 3 - 0.000197 * t ** 4)[m]
    m = (y >= 1920) & (y < 1941)
    t = y - 1920
    out[m] = (21.20 + 0.84493 * t - 0.076100 * t ** 2 + 0.0020936 * t ** 3)[m]
    m = (y >= 1941) & (y < 1961)
    t = y - 1950
    out[m] = (29.07 + 0.407 * t - t ** 2 / 233 + t ** 3 / 2547)[m]
    m = (y >= 1961) & (y < 1986)
    t = y - 1975
    out[m] = (45.45 + 1.067 * t - t ** 2 / 260 - t ** 3 / 718)[m]
    m = (y >= 1986) & (y < 2005)
    t = y - 2000
    out[m] = (63.86 + 0.3345 * t - 0.060374 * t ** 2 + 0.0017275 * t ** 3
              + 0.000651814 * t ** 4 + 0.00002373599 * t ** 5)[m]
    m = (y >= 2005) & (y < 2050)
    t = y - 2000
    out[m] = (62.92 + 0.32217 * t + 0.005589 * t ** 2)[m]
    m = (y >= 2050) & (y < 2150)
    out[m] = (-20 + 32 * ((y - 1820) / 100) ** 2 - 0.5628 * (2150 - y))[m]
    return out[()] if out.ndim == 0 else out


def ndot_correction(y, ndot_to, ndot_from):
    """Change in Delta-T when the lunar ephemeris' tidal acceleration n-dot
    ("/cy^2) is ndot_to instead of ndot_from: -0.91072 (ndot_to - ndot_from) T^2,
    T = (y - 1955)/100.  Morrison & Stephenson 2004 via Espenak & Meeus
    (NASA deltatpoly page gives c = -0.000012932 (y-1955)^2 for -26 -> -25.858);
    coefficient 0.91072 as in Y. T. Liu's DeltaT.py.  Zero for 1955-2005 is NOT
    applied here (irrelevant for antiquity)."""
    T = (np.asarray(y, dtype=float) - 1955.0) / 100.0
    return -0.91072 * (ndot_to - ndot_from) * T * T


def dt_em2006_canon(y):
    """Delta-T exactly as used in the NASA Five Millennium Canon tables:
    Espenak-Meeus polynomial plus c = -0.000012932 (y-1955)^2 (n-dot -25.858,
    ELP-2000/82 as used by the Canon).  Reproduces the Canon's 28590 s for
    the -1177 Apr 16 eclipse."""
    y = np.asarray(y, dtype=float)
    c = np.where((y >= 1955) & (y <= 2005), 0.0, -0.000012932 * (y - 1955) ** 2)
    out = dt_em2006(y) + c
    return out[()] if np.ndim(out) == 0 else out


def sigma_ms2004(y):
    """Morrison & Stephenson (2004) standard error 0.8 u^2 s, u=(y-1820)/100,
    as quoted by Espenak (NASA 'Uncertainty in Delta T' page); stated valid
    1000 BC - AD 1200 (i.e. y >= -999)."""
    u = (np.asarray(y, dtype=float) - 1820) / 100
    return 0.8 * u * u


def sigma_huber(y):
    """Huber (2000) Brownian-motion-plus-drift standard error, as quoted on the
    NASA 'Uncertainty in Delta T' page: sigma = 365.25 N sqrt((N Q/3)(1+N/M))/1000
    with N = years from the calibration epoch (-500 for the past), M = 2500,
    Q = 0.058 ms^2/yr."""
    y = np.asarray(y, dtype=float)
    N = np.where(y < -500, -500 - y, np.where(y > 2005, y - 2005, 0.0))
    return 365.25 * N * np.sqrt((N * 0.058 / 3.0) * (1 + N / 2500.0)) / 1000.0


def dt_smh2016_parabola(y):
    """Stephenson, Morrison & Hohenkerk 2016, Proc. R. Soc. A 472:20160404,
    eq. (4.1): -320.0 + (32.5 +- 0.6) tau^2, tau = (y-1825)/100."""
    tau = (np.asarray(y, dtype=float) - 1825) / 100
    return -320.0 + 32.5 * tau * tau


def dt_smh2020_parabola(y):
    """Morrison, Stephenson, Hohenkerk & Zawilski 2021 (Addendum 2020),
    Proc. R. Soc. A 477:20200776, eq. (5.1): -10 + (31.4 +- 0.6) tau^2."""
    tau = (np.asarray(y, dtype=float) - 1825) / 100
    return -10.0 + 31.4 * tau * tau


def sigma_parabola(y):
    """+-0.6 tau^2: the stated 1-sigma of the quadratic coefficient in both
    SMH2016 eq. 4.1 and Addendum 2020 eq. 5.1, propagated (constant term's
    uncertainty is not stated)."""
    tau = (np.asarray(y, dtype=float) - 1825) / 100
    return 0.6 * tau * tau


# Addendum 2020 spline (HMNAO 'Table S15 v2020': K_i, K_i+1, a0, a1, a2, a3;
# Delta-T = a0 + a1 t + a2 t^2 + a3 t^3, t = (y-K_i)/(K_i+1 - K_i)).  The same
# table is bundled with skyfield (data/delta_t.npz, 'Table-S15.2020.txt'); we
# read it from there and verify it against the HMNAO file in validate_ephem.py.
@functools.lru_cache(maxsize=None)
def _s15():
    tab = load_bundled_npy("delta_t.npz")["Table-S15.2020.txt"]
    return tuple(np.array(r, dtype=float) for r in tab)   # k0,k1,a3,a2,a1,a0


def _lod_integral(y):
    """Integral of the Addendum-2020 / HMNAO long-term lod function
    lod = +1.72 t - 3.5 sin(2 pi (t+0.75)/14) ms, t = (y-1825)/100,
    as Delta-T without its integration constant (seconds)."""
    t = (np.asarray(y, dtype=float) - 1825.0) / 100.0
    return (36.525 * 1.72 / 2.0 * t * t
            + 36.525 * 3.5 * 14.0 / (2 * math.pi) * np.cos(2 * math.pi * (t + 0.75) / 14.0))


def _s15_eval(y):
    k0, k1, a3, a2, a1, a0 = _s15()
    y = np.asarray(y, dtype=float)
    i = np.clip(np.searchsorted(k0, y, side="right") - 1, 0, len(k0) - 1)
    t = (y - k0[i]) / (k1[i] - k0[i])
    return a0[i] + t * (a1[i] + t * (a2[i] + t * a3[i]))


@functools.lru_cache(maxsize=None)
def _lod_constants():
    k0, k1, *_ = _s15()
    c_past = float(_s15_eval(k0[0]) - _lod_integral(k0[0]))
    end = k1[-1]
    c_future = float(_s15_eval(end - 1e-9) - _lod_integral(end))
    return c_past, c_future, float(k0[0]), float(end)


def dt_smh2020(y):
    """The SMH/Addendum-2020 Delta-T as published by its authors:
    * -720 .. 2019: the Addendum 2020 cubic spline (Table S15 v2020);
    * before -720: the HMNAO extrapolation 'by integration using the long term
      lod function lod = +1.72 t - 3.5 sin(2 pi (t+0.75)/14)' (HMNAO LVM page,
      section 'Delta-T and lod from -2000 to -800'), integration constant fixed
      by continuity with the spline at -720 (C = +1.0077 s; same value as
      Y. T. Liu's DeltaT.py).  The HMNAO table (hours, 1 decimal) is reproduced
      if its entries are read as rounded UP -- see validate_ephem.py;
    * after 2019: same lod integral, continuous at 2019.0.
    Lunar n-dot implicit: -25.82"/cy^2 (SMH2016 sect. 3a; the HMNAO page says
    -25.85 for DE430)."""
    y = np.asarray(y, dtype=float)
    c_past, c_future, y0, y1 = _lod_constants()
    out = np.where(y < y0, _lod_integral(y) + c_past,
                   np.where(y > y1, _lod_integral(y) + c_future, _s15_eval(y)))
    return out[()] if out.ndim == 0 else out


# HMNAO error estimates epsilon (seconds), LVM page (archived 2022-03-20):
# -2000..-800 in hours (0.3 / 0.2 / 0.1), -720..+1600 in seconds, 1600-1800.
_SMH_EPS = np.array([
    (-2000, 1080), (-1700, 1080), (-1600, 720), (-1000, 720), (-900, 360),
    (-800, 360), (-720, 180), (-700, 170), (-600, 160), (-500, 150),
    (-400, 130), (-300, 120), (-200, 110), (-100, 100), (0, 90), (100, 80),
    (200, 70), (300, 60), (400, 50), (500, 40), (600, 40), (700, 30),
    (800, 25), (900, 20), (1000, 15), (1600, 15), (1610, 15), (1620, 20),
    (1650, 20), (1660, 15), (1670, 10), (1680, 5), (1720, 5), (1730, 2),
    (1760, 2), (1770, 1), (1790, 1), (1800, 0.5), (1810, 0.5)], dtype=float)


def sigma_smh2020(y):
    """HMNAO's stated error estimate epsilon for the SMH/Addendum-2020 Delta-T,
    linearly interpolated between its tabulated epochs (-2000..1810).  Before
    -2000 (no published value) we extrapolate as Liu does, 0.74e-4 (y-1825)^2
    -- flagged as NOT a published number."""
    y = np.asarray(y, dtype=float)
    out = np.interp(y, _SMH_EPS[:, 0], _SMH_EPS[:, 1])
    out = np.where(y < -2000, 0.74e-4 * (y - 1825) ** 2, out)
    return out[()] if out.ndim == 0 else out


def dt_skyfield(y):
    """skyfield 1.55's built-in long-term Delta-T (for comparison only): S15
    v2020 spline back to -720, an 800-year hand-tuned cubic patch, then the
    SMH2016 parabola before -1520."""
    from skyfield.api import load
    ts = load.timescale()
    jd = J2000 + (np.asarray(y, dtype=float) - 2000.0) * 365.25
    return ts.delta_t_function(jd)


DT_MODELS = {
    "smh2020": (dt_smh2020, sigma_smh2020),
    "smh2020_parabola": (dt_smh2020_parabola, sigma_parabola),
    "smh2016_parabola": (dt_smh2016_parabola, sigma_parabola),
    "em2006": (dt_em2006, sigma_huber),
    "em2006_canon": (dt_em2006_canon, sigma_huber),
}


def delta_t(y, model: str = "smh2020"):
    """Delta-T in seconds for decimal year y under the named model."""
    return DT_MODELS[model][0](y)


def delta_t_sigma(y, model: str = "smh2020"):
    """The 1-sigma that the model's source states (see each function)."""
    return DT_MODELS[model][1](y)


# --------------------------------------------------------- time scales

@functools.lru_cache(maxsize=None)
def _leap():
    a = load_bundled_npy("iers.npz")
    return a["leap_dates"], a["leap_offsets"]


def _dt_function(dt):
    """Normalise dt (number | model name | callable(year)) to f(jd_tt)->s."""
    if isinstance(dt, (int, float, np.floating)):
        val = float(dt)
        return lambda tt: np.full(np.shape(tt), val)[()] if np.ndim(tt) else val
    if isinstance(dt, str):
        fn = DT_MODELS[dt][0]
    elif callable(dt):
        fn = dt
    else:
        raise TypeError("dt must be seconds, a model name or a callable")
    return lambda tt: fn(julian_epoch(tt))


@functools.lru_cache(maxsize=256)
def timescale(dt="smh2020") -> Timescale:
    """A skyfield Timescale whose TT-UT1 is `dt` (constant seconds, model name,
    or callable year->seconds).  Cached by dt."""
    leap_dates, leap_offsets = _leap()
    return Timescale(_dt_function(dt), leap_dates, leap_offsets)


# ------------------------------------------------- long-term precession

def _rnpb_erfa(epj):
    """Vondrak et al. 2011 precession + IAU 2006 frame bias (ERFA eraLtpb)."""
    return erfa.ltpb(epj)


@functools.lru_cache(maxsize=None)
def _cio_locator_spline(model: str = "vondrak", y0: float = -3000.0, y1: float = 2500.0,
                        step: float = 0.25):
    """CIO locator s(epoch) for the PRECESSION-ONLY pole path of `model`,
    by direct quadrature of the kinematic definition (Capitaine, Guinot &
    McCarthy 2000; IERS Conventions 2010 sect. 5.4.2):
        s(t) = -Int_{t0}^{t} (X dY/dt - Y dX/dt) / (1 + Z) dt  + s(t0),
    with t0 = J2000 and s(t0) from ERFA eraS06.  Returns a CubicSpline in
    Julian epoch.  model: 'vondrak' (eraLtpb) or 'iau2006' (eraPmat06)."""
    ep = np.arange(y0, y1 + step / 2, step)
    if model == "vondrak":
        R = erfa.ltpb(ep)
    else:
        jd = J2000 + (ep - 2000.0) * 365.25
        R = erfa.pmat06(jd, 0.0)
    X, Y, Z = R[:, 2, 0], R[:, 2, 1], R[:, 2, 2]
    sx, sy = CubicSpline(ep, X), CubicSpline(ep, Y)
    f = (X * sy(ep, 1) - Y * sx(ep, 1)) / (1.0 + Z)
    i0 = int(np.argmin(np.abs(ep - 2000.0)))
    cum = cumulative_simpson(f, x=ep, initial=0.0)
    s = -(cum - cum[i0])
    s += float(erfa.s06(J2000, 0.0, X[i0], Y[i0]))
    return CubicSpline(ep, s)


def cio_locator(epj, model: str = "vondrak", rnpb=None):
    """s (radians) for the full NPB matrix rnpb (ERFA layout (...,3,3)).
    Precession-only s from the quadrature, plus the first-order nutation
    term -(Xp dY - Yp dX)/(1+Zp) (integration by parts; neglected remainder is
    periodic and below 0.01").  If rnpb is None, precession-only."""
    sp = _cio_locator_spline(model)
    s = sp(epj)
    if rnpb is None:
        return s
    Rp = erfa.ltpb(epj) if model == "vondrak" else erfa.pmat06(J2000 + (np.asarray(epj) - 2000.0) * 365.25, 0.0)
    Xp, Yp, Zp = Rp[..., 2, 0], Rp[..., 2, 1], Rp[..., 2, 2]
    dX = rnpb[..., 2, 0] - Xp
    dY = rnpb[..., 2, 1] - Yp
    return s - (Xp * dY - Yp * dX) / (1.0 + Zp)


def _to_sky(R):
    """ERFA (...,3,3) -> skyfield (3,3[,n])."""
    R = np.asarray(R)
    return R if R.ndim == 2 else np.transpose(R, (1, 2, 0))


def _to_erfa(M):
    M = np.asarray(M)
    return M if M.ndim == 2 else np.transpose(M, (2, 0, 1))


def apply_precession(t, precession: str = "vondrak"):
    """Install the chosen precession model in a skyfield Time (in place) and
    return it.  'iau2006' leaves skyfield untouched.  'vondrak' sets
        t.M    = N(IAU 2000A) . PB(Vondrak 2011 + IAU 2006 bias)
        t.gast = ERA(UT1) - EO,  EO = eraEors(M, s)  with s from cio_locator,
    so the hour angles are consistent with the long-term pole path."""
    if precession == "iau2006":
        return t
    if precession != "vondrak":
        raise ValueError(precession)
    d = t.__dict__
    for k in ("M", "MT", "C", "CT", "gast"):
        if k in d:
            raise RuntimeError("apply_precession must run before the Time is used")
    epj = julian_epoch(t.tt)
    PB = _to_sky(erfa.ltpb(epj))
    M = mxm(t.nutation_matrix(), PB)
    Me = _to_erfa(M)
    s = cio_locator(epj, "vondrak", Me)
    eo = erfa.eors(Me, s)
    era = 2 * math.pi * earth_rotation_angle(t.whole, t.ut1_fraction)
    d["M"] = M
    d["gast"] = ((era - eo) / (2 * math.pi) * 24.0) % 24.0
    return t


def mean_obliquity(jd_tt, precession="vondrak"):
    """Mean obliquity of the ecliptic of date (radians).  'vondrak': angle
    between the long-term mean equator pole (eraLtpequ) and ecliptic pole
    (eraLtpecl); 'iau2006': eraObl06 polynomial."""
    if precession == "iau2006":
        return erfa.obl06(jd_tt, 0.0)
    epj = julian_epoch(jd_tt)
    c = np.sum(erfa.ltpequ(epj) * erfa.ltpecl(epj), axis=-1)
    return np.arccos(np.clip(c, -1.0, 1.0))


def time_tt(jd_tt, dt="smh2020", precession="vondrak"):
    """skyfield Time at TT Julian date(s) jd_tt, with Delta-T `dt`."""
    t = timescale(dt).tt_jd(jd_tt)
    return apply_precession(t, precession)


def time_ut(jd_ut, dt="smh2020", precession="vondrak"):
    """skyfield Time at UT1 Julian date(s) jd_ut, with Delta-T `dt`."""
    t = timescale(dt).ut1_jd(jd_ut)
    return apply_precession(t, precession)


# ------------------------------------------------------------ ephemerides

_ACTIVE_DIR = [EPHEM_DIR]


@functools.lru_cache(maxsize=None)
def _kernels(directory: Path = None):
    out = []
    for p in sorted(Path(directory or EPHEM_DIR).glob("*.bsp")):
        k = load_file(str(p))
        segs = k.spk.segments
        jd0 = max(s.start_jd for s in segs)
        jd1 = min(s.end_jd for s in segs)
        targets = {s.target for s in segs}
        out.append((jd0, jd1, targets, p.name, k))
    return out


class use_ephemeris:
    """Context manager: read SPK excerpts from another directory, e.g.
    `with use_ephemeris(EPHEM_DIR / 'de431'):` to repeat a computation with
    DE431 (lunar tidal acceleration -25.82"/cy^2, the DE430 value that the
    SMH Delta-T is tied to)."""
    def __init__(self, directory):
        self.directory = Path(directory)

    def __enter__(self):
        _ACTIVE_DIR.append(self.directory)
        return self

    def __exit__(self, *exc):
        _ACTIVE_DIR.pop()


def kernel(jd, need=("sun", "moon", "earth")):
    """The SPK excerpt (DE441 unless use_ephemeris is active) covering jd (TT)
    and the needed bodies."""
    codes = {"sun": 10, "moon": 301, "earth": 399, "mercury": 199, "venus": 299,
             "mars": 4, "jupiter": 5, "saturn": 6}
    want = {codes[n] for n in need}
    jd_lo = float(np.min(jd))
    jd_hi = float(np.max(jd))
    for jd0, jd1, targets, name, k in _kernels(_ACTIVE_DIR[-1]):
        if jd0 <= jd_lo and jd_hi <= jd1 and want <= targets:
            return k
    raise LookupError(f"no SPK excerpt in {_ACTIVE_DIR[-1]} covers JD {jd_lo}..{jd_hi} for {need}")


BODY_NAMES = {"sun": "sun", "moon": "moon", "mercury": "mercury", "venus": "venus",
              "mars": "mars barycenter", "jupiter": "jupiter barycenter",
              "saturn": "saturn barycenter"}

# ------------------------------------------------------------------ stars
# Hipparcos new reduction (van Leeuwen 2007; VizieR I/311/hip2), epoch J1991.25,
# ICRS.  pmRA is mu_alpha* (= mu_alpha cos dec).  Radial velocities from SIMBAD
# (bibcodes in docs).  Fetched 2026-10-03.
HIP_STARS = {
    # key: (HIP, name, ra_deg, dec_deg, plx_mas, pmra_mas_yr, pmde_mas_yr, rv_km_s)
    "alcyone": (17702, "eta Tau (Alcyone)", 56.87110081, 24.10524179, 8.09, 19.34, -43.67, 5.4),
    "arcturus": (69673, "alpha Boo (Arcturus)", 213.91811408, 19.18727046, 88.83, -1093.39, -2000.06, -5.229),
    "eps_boo": (72105, "epsilon Boo (Izar)", 221.24687848, 27.07417376, 16.10, -50.95, 21.07, -16.6),
    "eta_boo": (67927, "eta Boo (Muphrid)", 208.67131829, 18.39858670, 87.75, -60.95, -356.29, 5.77111),
}
HIP_EPOCH_JD_TT = 2448349.0625      # J1991.25


def star(key: str) -> Star:
    _, name, ra, de, plx, pmra, pmde, rv = HIP_STARS[key]
    return Star(ra_hours=ra / 15.0, dec_degrees=de, ra_mas_per_year=pmra,
                dec_mas_per_year=pmde, parallax_mas=plx, radial_km_per_s=rv,
                epoch=HIP_EPOCH_JD_TT, names=(name,))


def _target(name, k):
    if name in HIP_STARS:
        return star(name)
    return k[BODY_NAMES[name]]


# ------------------------------------------------------------- positions

def observer(lat, lon, elev_m=0.0, k=None):
    return (k["earth"] + wgs84.latlon(lat, lon, elevation_m=elev_m))


def apparent(name, t, lat=None, lon=None, elev_m=0.0):
    """Apparent position (skyfield Apparent) of body or star `name` at Time t,
    topocentric if lat/lon given, else geocentric.  Solar light deflection and
    annual+diurnal aberration included."""
    need = ("sun", "earth") + ((name,) if name in BODY_NAMES and name != "sun" else ())
    k = kernel(t.tt, need)
    obs = k["earth"] if lat is None else observer(lat, lon, elev_m, k)
    return obs.at(t).observe(_target(name, k)).apparent(deflectors=(10,))


def altaz(name, jd_ut, lat, lon, elev_m=0.0, dt="smh2020", precession="vondrak",
          refraction=False, temperature_C=10.0, pressure_mbar=1010.0):
    """(altitude_deg, azimuth_deg) of `name` seen from (lat, lon) at UT1 jd_ut.
    Azimuth from north through east.  Airless unless refraction=True."""
    t = time_ut(jd_ut, dt, precession)
    a = apparent(name, t, lat, lon, elev_m)
    alt, az, _ = a.altaz()
    alt = alt.degrees
    if refraction:
        alt = float(_refract(np.asarray(alt, dtype=float), temperature_C, pressure_mbar))
    return alt, az.degrees


def radec_of_date(name, t, lat=None, lon=None, elev_m=0.0):
    """Apparent RA (deg), Dec (deg) on the true equator and equinox of date."""
    a = apparent(name, t, lat, lon, elev_m)
    ra, de, _ = a.radec(epoch="date")
    return ra._degrees, de.degrees


def elongation(name, jd_ut, lat=None, lon=None, dt="smh2020", precession="vondrak"):
    """Sun-observer-target angle (deg); frame-independent."""
    t = time_ut(jd_ut, dt, precession)
    a = apparent(name, t, lat, lon)
    s = apparent("sun", t, lat, lon)
    return a.separation_from(s).degrees


def local_apparent_solar_time(jd_ut, lat, lon, dt="smh2020", precession="vondrak"):
    """Local apparent solar time in hours (12 = true noon)."""
    t = time_ut(jd_ut, dt, precession)
    a = apparent("sun", t, lat, lon)
    ra, _, _ = a.radec(epoch="date")
    ha = (t.gast + lon / 15.0 - ra.hours) % 24.0
    return (ha + 12.0) % 24.0


# -------------------------------------------------------------- new moons

def _lon_diff_moon_sun(jd_tt, precession="vondrak"):
    """Geocentric apparent ecliptic longitude Moon minus Sun (deg, wrapped to
    (-180,180]) on the true ecliptic and equinox of date.  Independent of
    Delta-T."""
    t = time_tt(jd_tt, 0.0, precession)
    k = kernel(t.tt, ("sun", "moon", "earth"))
    e = k["earth"].at(t)
    eps = mean_obliquity(t.tt, precession) + t._nutation_angles_radians[1]
    out = []
    for body in ("moon", "sun"):
        v = e.observe(k[body]).apparent(deflectors=(10,)).xyz.au
        x, y, z = np.einsum("ij...,j...->i...", t.M, v)
        yl = y * np.cos(eps) + z * np.sin(eps)
        out.append(np.degrees(np.arctan2(yl, x)))
    return (out[0] - out[1] + 180.0) % 360.0 - 180.0


def new_moons(jd_tt_start, jd_tt_end, precession="vondrak"):
    """TT Julian dates of geocentric conjunctions (apparent ecliptic longitude
    of Moon = Sun) in [start, end]."""
    grid = np.arange(jd_tt_start, jd_tt_end + 1.0, 1.0)
    d = _lon_diff_moon_sun(grid, precession)
    out = []
    for i in np.nonzero((d[:-1] < 0) & (d[1:] >= 0))[0]:
        f = lambda x: float(_lon_diff_moon_sun(x, precession))
        out.append(brentq(f, grid[i], grid[i + 1], xtol=1e-7))
    return [x for x in out if jd_tt_start <= x <= jd_tt_end]


# --------------------------------------------------------------- eclipses

def besselian(jd_tt, dt="em2006_canon", precession="vondrak"):
    """Besselian-type quantities from DE441 at TT jd_tt (scalar or array):
    x, y (Earth equatorial radii, fundamental plane), d (deg, declination of
    the shadow axis), mu (deg, Greenwich hour angle of the axis; depends on
    Delta-T), gamma = sqrt(x^2+y^2) signed by y.  Geocentric apparent
    positions on the true equator of date (Explanatory Supplement 1992 ch. 8)."""
    t = time_tt(jd_tt, dt, precession)
    k = kernel(t.tt)
    e = k["earth"].at(t)
    vs = np.einsum("ij...,j...->i...", t.M, e.observe(k["sun"]).apparent(deflectors=(10,)).xyz.km)
    vm = np.einsum("ij...,j...->i...", t.M, e.observe(k["moon"]).apparent(deflectors=(10,)).xyz.km)
    g = vs - vm
    g = g / np.linalg.norm(g, axis=0)
    a = np.arctan2(g[1], g[0])
    dd = np.arcsin(g[2])
    rm = np.linalg.norm(vm, axis=0) / EARTH_EQ_RADIUS_KM
    am = np.arctan2(vm[1], vm[0])
    dm = np.arcsin(vm[2] / np.linalg.norm(vm, axis=0))
    x = rm * np.cos(dm) * np.sin(am - a)
    y = rm * (np.sin(dm) * np.cos(dd) - np.cos(dm) * np.sin(dd) * np.cos(am - a))
    mu = (t.gast * 15.0 - np.degrees(a)) % 360.0
    # 'ephemeris hour angle' (meridian 1.0027379 x 15 x DeltaT east of
    # Greenwich), the convention of the NASA Besselian-element pages.
    mu_eph = (mu + 1.00273781191135448 * 15.0 * t.delta_t / 3600.0) % 360.0
    gamma = np.sign(y) * np.hypot(x, y)
    return dict(x=x, y=y, d=np.degrees(dd), mu=mu, mu_eph=mu_eph, gamma=gamma)


def greatest_eclipse(jd_tt_guess, window_h=6.0):
    """TT of minimum |gamma| (the Canon's 'instant of greatest eclipse') and
    the Besselian quantities there.  Independent of Delta-T except mu."""
    # NB: optimise in HOURS from the guess -- scipy's bounded Brent adds a
    # relative tolerance sqrt(eps)*|x|, which is ~27 min at JD 1.3e6.
    hrs = np.linspace(-window_h, window_h, 121)
    b = besselian(jd_tt_guess + hrs / 24.0)
    i = int(np.argmin(np.hypot(b["x"], b["y"])))
    f = lambda h: float(np.hypot(*[besselian(jd_tt_guess + h / 24.0)[c] for c in ("x", "y")]))
    r = minimize_scalar(f, bounds=(hrs[max(i - 1, 0)], hrs[min(i + 1, len(hrs) - 1)]),
                        method="bounded", options={"xatol": 1e-6})
    j = jd_tt_guess + r.x / 24.0
    return j, besselian(j)


def _disc_geometry(t, lat, lon, elev_m):
    """Topocentric separation and semidiameters (radians) of Sun and Moon."""
    k = kernel(t.tt)
    o = observer(lat, lon, elev_m, k).at(t)
    s = o.observe(k["sun"]).apparent(deflectors=(10,))
    m = o.observe(k["moon"]).apparent(deflectors=(10,))
    sep = m.separation_from(s).radians
    ds = s.distance().km
    dm = m.distance().km
    r_sun = np.arcsin(SUN_RADIUS_KM / ds)
    r_moon_p = np.arcsin(K_PENUMBRA * EARTH_EQ_RADIUS_KM / dm)
    r_moon_u = np.arcsin(K_UMBRA * EARTH_EQ_RADIUS_KM / dm)
    return sep, r_sun, r_moon_p, r_moon_u, o, s


def _obscuration(sep, rs, rm):
    """Fraction of the solar disc's AREA covered (circle-circle overlap)."""
    sep, rs, rm = np.broadcast_arrays(np.asarray(sep, float), rs, rm)
    out = np.zeros(sep.shape)
    full = sep <= np.abs(rm - rs)
    out[full] = np.minimum(1.0, (rm[full] / rs[full]) ** 2)
    part = (~full) & (sep < rs + rm)
    d, r1, r2 = sep[part], rs[part], rm[part]
    a1 = r1 * r1 * np.arccos(np.clip((d * d + r1 * r1 - r2 * r2) / (2 * d * r1), -1, 1))
    a2 = r2 * r2 * np.arccos(np.clip((d * d + r2 * r2 - r1 * r1) / (2 * d * r2), -1, 1))
    a3 = 0.5 * np.sqrt(np.clip((-d + r1 + r2) * (d + r1 - r2) * (d - r1 + r2) * (d + r1 + r2), 0, None))
    out[part] = (a1 + a2 - a3) / (math.pi * r1 * r1)
    return out[()] if out.ndim == 0 else out


def local_circumstances(lat, lon, jd_tt_guess, dt="smh2020", elev_m=0.0,
                        precession="vondrak", window_h=4.0):
    """Solar-eclipse local circumstances at (lat, lon) for Delta-T `dt`.

    Returns dict: jd_tt_max, jd_ut_max, dt_s, magnitude (fraction of solar
    DIAMETER covered, penumbral k1), ratio (Moon/Sun apparent diameter, k2),
    obscuration (area), total (bool, k2), annular (bool), duration_s (central
    phase, k2), c1..c4 TT (None when absent), sun_alt_deg / sun_az_deg at
    maximum (airless), lat_hours (local apparent solar time at maximum),
    min_sep_arcsec."""
    ts_dt = dt
    grid = jd_tt_guess + np.linspace(-window_h, window_h, int(window_h * 60) + 1) / 24.0
    t = time_tt(grid, ts_dt, precession)
    sep, rs, rmp, rmu, _, _ = _disc_geometry(t, lat, lon, elev_m)
    i = int(np.argmin(sep))

    def sep_at(x):
        tt = time_tt(x, ts_dt, precession)
        return float(_disc_geometry(tt, lat, lon, elev_m)[0])

    # optimise in hours from grid[i] (see greatest_eclipse for why)
    ref = grid[i]
    hlo = (grid[max(i - 2, 0)] - ref) * 24.0
    hhi = (grid[min(i + 2, len(grid) - 1)] - ref) * 24.0
    hmax = minimize_scalar(lambda h: sep_at(ref + h / 24.0), bounds=(hlo, hhi),
                           method="bounded", options={"xatol": 1e-7}).x
    jmax = ref + hmax / 24.0
    tm = time_tt(jmax, ts_dt, precession)
    sep_m, rs_m, rmp_m, rmu_m, o, s_app = _disc_geometry(tm, lat, lon, elev_m)
    sep_m, rs_m, rmp_m, rmu_m = map(float, (sep_m, rs_m, rmp_m, rmu_m))
    mag = (rs_m + rmp_m - sep_m) / (2 * rs_m)
    total = (rmu_m > rs_m) and (sep_m <= rmu_m - rs_m)
    annular = (rmu_m < rs_m) and (sep_m <= rs_m - rmu_m)

    def contact(func, a, b):
        try:
            return brentq(func, a, b, xtol=1e-9)
        except ValueError:
            return None

    def outer(x):
        g = _disc_geometry(time_tt(x, ts_dt, precession), lat, lon, elev_m)
        return float(g[0] - (g[1] + g[2]))

    def inner(x):
        g = _disc_geometry(time_tt(x, ts_dt, precession), lat, lon, elev_m)
        return float(g[0] - abs(g[3] - g[1]))

    c1 = c4 = c2 = c3 = None
    if mag > 0:
        c1 = contact(outer, grid[0], jmax)
        c4 = contact(outer, jmax, grid[-1])
        if total or annular:
            c2 = contact(inner, jmax - 0.5 / 24, jmax)
            c3 = contact(inner, jmax, jmax + 0.5 / 24)
    alt, az, _ = s_app.altaz()
    ra, _, _ = s_app.radec(epoch="date")
    ha = (tm.gast + lon / 15.0 - ra.hours) % 24.0
    return dict(
        jd_tt_max=jmax, jd_ut_max=float(tm.ut1), dt_s=float(tm.delta_t),
        magnitude=mag, ratio=rmu_m / rs_m,
        obscuration=float(_obscuration(sep_m, rs_m, rmp_m)),
        total=bool(total), annular=bool(annular),
        duration_s=(c3 - c2) * DAY_S if (c2 is not None and c3 is not None) else 0.0,
        c1=c1, c2=c2, c3=c3, c4=c4,
        sun_alt_deg=float(alt.degrees), sun_az_deg=float(az.degrees),
        lat_hours=(ha + 12.0) % 24.0,
        min_sep_arcsec=sep_m / ASEC,
        central_margin_arcsec=(abs(rmu_m - rs_m) - sep_m) / ASEC,
    )


def totality_window(lat, lon, jd_tt_guess, dt_lo, dt_hi, elev_m=0.0,
                    precession="vondrak", step=60.0):
    """Range(s) of constant Delta-T (seconds) within [dt_lo, dt_hi] for which
    the eclipse is TOTAL at (lat, lon).  Scans in `step` s then bisects the
    edges to 0.5 s.  Returns list of (lo, hi)."""
    def margin(dtv):
        lc = local_circumstances(lat, lon, jd_tt_guess, float(dtv), elev_m, precession)
        if lc["ratio"] <= 1.0:
            return -1.0 - (1.0 - lc["ratio"])
        return lc["central_margin_arcsec"]
    grid = np.arange(dt_lo, dt_hi + step / 2, step)
    vals = np.array([margin(g) for g in grid])
    out = []
    inside = vals > 0
    for i in range(len(grid) - 1):
        if inside[i] != inside[i + 1]:
            out.append(brentq(margin, grid[i], grid[i + 1], xtol=0.5))
    edges = sorted(out)
    wins = []
    cur = grid[0] if inside[0] else None
    for e in edges:
        if cur is None:
            cur = e
        else:
            wins.append((cur, e))
            cur = None
    if cur is not None:
        wins.append((cur, grid[-1]))
    return wins


# ------------------------------------------------------------- precession

def precession_compare(jd_tt):
    """Differences between IAU 2006 (P03, skyfield/ERFA eraPmat06) and the
    Vondrak 2011 long-term model (eraLtpb) at jd_tt.  Returns dict with the
    angle between the two mean poles of date (arcsec), the difference in
    equation of the origins EO (arcsec; = hour-angle error of the polynomial
    sidereal time), and the full rotation angle between the two matrices."""
    epj = float(julian_epoch(jd_tt))
    Rv = erfa.ltpb(epj)
    Ri = erfa.pmat06(jd_tt, 0.0)
    pole = math.degrees(math.atan2(np.linalg.norm(np.cross(Rv[2], Ri[2])), float(np.dot(Rv[2], Ri[2])))) * 3600
    Rrel = Rv @ Ri.T
    ang = math.degrees(math.acos(max(-1.0, min(1.0, (np.trace(Rrel) - 1) / 2)))) * 3600
    sv = cio_locator(epj, "vondrak")
    eo_v = erfa.eors(Rv, sv) / ASEC
    # IAU 2006 mean sidereal time: GMST = ERA + poly(t) (eraGmst06), so the
    # precession-only equation of the origins is -poly(t).
    tc = (jd_tt - J2000) / 36525.0
    poly = (0.014506 + (4612.156534 + (1.3915817 + (-0.00000044 + (-0.000029956
            - 0.0000000368 * tc) * tc) * tc) * tc) * tc)
    eo_i_poly = -poly
    si = cio_locator(epj, "iau2006")
    eo_i_int = erfa.eors(Ri, si) / ASEC
    ob_v = float(mean_obliquity(jd_tt, "vondrak")) / ASEC
    ob_i = float(mean_obliquity(jd_tt, "iau2006")) / ASEC
    return dict(epoch=epj, pole_sep_arcsec=pole, rotation_arcsec=ang,
                eo_vondrak_arcsec=eo_v, eo_iau2006_poly_arcsec=eo_i_poly,
                eo_iau2006_integrated_arcsec=eo_i_int,
                eo_diff_arcsec=eo_v - eo_i_poly,
                obliquity_vondrak_arcsec=ob_v, obliquity_iau2006_arcsec=ob_i)
