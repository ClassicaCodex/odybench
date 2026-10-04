"""
odybench.calendar -- exact calendar arithmetic for the whole bench.

Conventions (DESIGN section 0; critique-design issues 13 and 22)
------------------------------------------------------------------
* ASTRONOMICAL years: 1 BC = 0, 2 BC = -1, 1178 BC = -1177.  The historical
  BC year is 1 - y (historical_year()).  Year 0 exists.
* PROLEPTIC JULIAN calendar unless a function's name says gregorian.  The
  Julian leap rule is applied uniformly to every year (y divisible by 4,
  including 0, -4, -8, ...): this is the astronomers' proleptic calendar of
  Horizons and the NASA canons, not the irregular Roman practice of 45-9 BC.
* JD = Julian Date: days since -4712 Jan 1, 12h (proleptic Julian), on
  whatever time scale the instant is expressed in (UT, TT, ...).  The time
  scale is never implied: functions that need one say so.
* JDN = Julian Day Number of a calendar day = the JD of its noon (an
  integer).  The civil day with number N runs over JD [N - 0.5, N + 0.5).
* Civil dates of an instant are taken in a stated zone: UT, UT+2
  (offset +2 h), LMT at a longitude (offset lon/15 h, east positive) or LAT
  (LMT plus the equation of time, which the caller supplies).  Instants are
  resolved to 1 ms before the day is chosen, so floating-point noise in a
  JD cannot move an instant across midnight (a float JD near 1.3e6 only
  resolves about 20 microseconds anyway).
* Calendar dates are never handled through Python's date-time types or
  numpy's 64-bit date-time type: both are proleptic GREGORIAN and would be
  11 days off at -1177 (DESIGN section 0).  tests/test_calendar.py checks
  that no bench source file imports them.

All integer arithmetic is exact (floor division), for Python ints and numpy
integer arrays alike, so the functions vectorise: pass numpy arrays to
convert many days at once.

Sources: the JDN formulas are the standard integer forms (Fliegel & van
Flandern 1968 for the Gregorian calendar; the Julian variant drops the
century terms), see e.g. Richards in the Explanatory Supplement to the
Astronomical Almanac (3rd ed., 2013) ch. 15.  They are checked in
tests/test_calendar.py against (a) independent day counting from the
definition JD 0 = -4712 Jan 1.5 over every day of -1999..+500, (b)
odybench.ephem's Meeus (1998, ch. 7) floating-point formulas, (c) Meeus'
worked examples, and (d) JPL Horizons' own calendar output for random
dates.

Note on the module name: inside the package it is odybench.calendar and
does not shadow the standard library.  Do not run files inside odybench/
as scripts (py odybench/x.py); use py -m odybench.x.
"""
from __future__ import annotations

import math

import numpy as np

J2000 = 2451545.0                     # 2000 Jan 1.5 TT (Gregorian) = JD 2451545.0
MS_PER_DAY = 86_400_000
_MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
_MDAYS = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
GREGORIAN_REFORM_JDN = 2299161        # 1582 Oct 15 (Gregorian) = 1582 Oct 5 (Julian)


# ------------------------------------------------------------------ helpers

def _int(x):
    """Python int for scalars, int64 array for array-likes."""
    if isinstance(x, (int, np.integer)):
        return int(x)
    a = np.asarray(x)
    if a.ndim == 0:
        v = a.item()
        if float(v) != math.floor(float(v)):
            raise ValueError(f"integer expected, got {v!r}")
        return int(v)
    if not np.issubdtype(a.dtype, np.integer):
        if np.any(a != np.floor(a)):
            raise ValueError("integer array expected")
    return a.astype(np.int64)


# --------------------------------------------------------------- leap rule

def is_leap_julian(year):
    """Julian leap rule on astronomical years: divisible by 4 (0, -4, ... are leap)."""
    y = _int(year)
    return (y % 4) == 0


def is_leap_gregorian(year):
    y = _int(year)
    return ((y % 4) == 0) & (((y % 100) != 0) | ((y % 400) == 0))


def days_in_year(year):
    """365 or 366 (Julian calendar)."""
    return 365 + is_leap_julian(year) * 1


def days_in_month(year, month):
    """Length of a month of the Julian calendar."""
    y, m = _int(year), _int(month)
    base = np.asarray(_MDAYS)[np.asarray(m) - 1]
    out = base + ((np.asarray(m) == 2) & is_leap_julian(y)) * 1
    return int(out) if np.ndim(out) == 0 else out


# ------------------------------------------------------- Julian calendar

def jdn_from_julian(year, month, day):
    """Julian Day Number (integer JD of noon) of a proleptic Julian date."""
    y, m, d = _int(year), _int(month), _int(day)
    a = (14 - m) // 12
    yy = y + 4800 - a
    mm = m + 12 * a - 3
    return d + (153 * mm + 2) // 5 + 365 * yy + yy // 4 - 32083


def julian_from_jdn(jdn):
    """(year, month, day) of the proleptic Julian date with this JDN."""
    j = _int(jdn)
    c = j + 32082
    d = (4 * c + 3) // 1461
    e = c - (1461 * d) // 4
    m = (5 * e + 2) // 153
    day = e - (153 * m + 2) // 5 + 1
    month = m + 3 - 12 * (m // 10)
    year = d - 4800 + m // 10
    return year, month, day


def jd_from_julian(year, month, day, hour=0.0):
    """JD of `hour` hours after 0h on a proleptic Julian date (the time scale
    is the caller's).  `day` may carry a fraction, as in Meeus' examples
    (333 Jan 27.5 = JD 1842713.0).  jd_from_julian(-1177, 4, 16) == 1291263.5."""
    if isinstance(day, (float, np.floating)) or (np.ndim(day) and not np.issubdtype(np.asarray(day).dtype, np.integer)):
        d = np.floor(np.asarray(day, dtype=float))
        frac = np.asarray(day, dtype=float) - d
        dint = _int(d)
    else:
        dint, frac = _int(day), 0.0
    out = (jdn_from_julian(year, month, dint) - 0.5) + frac + np.asarray(hour, dtype=float) / 24.0
    return float(out) if np.ndim(out) == 0 else out


def _split_ms(jd, offset_hours=0.0):
    """Instant jd (+ offset) as integer milliseconds since JD 0.0, rounded to 1 ms."""
    x = np.rint((np.asarray(jd, dtype=float) + np.asarray(offset_hours, dtype=float) / 24.0) * MS_PER_DAY)
    if np.ndim(x) == 0:
        return int(x)
    return x.astype(np.int64)


def jdn_of_instant(jd, offset_hours=0.0):
    """JDN of the civil day that contains instant jd in a zone `offset_hours`
    ahead of jd's scale (resolved to 1 ms)."""
    ms = _split_ms(jd, offset_hours)
    return (ms + MS_PER_DAY // 2) // MS_PER_DAY


def julian_from_jd(jd, offset_hours=0.0):
    """(year, month, day, hours) of instant jd in the proleptic Julian
    calendar, in the zone offset_hours ahead of jd's time scale; hours in
    [0, 24), resolved to 1 ms."""
    ms = _split_ms(jd, offset_hours) + MS_PER_DAY // 2
    jdn = ms // MS_PER_DAY
    y, m, d = julian_from_jdn(jdn)
    h = (ms - jdn * MS_PER_DAY) / 3_600_000.0
    return y, m, d, h


# ---------------------------------------------- Gregorian (cross-checks only)

def jdn_from_gregorian(year, month, day):
    """JDN of a proleptic GREGORIAN date (for modern dates and cross-checks
    with tools that use Gregorian dates, such as jplephem's excerpt CLI)."""
    y, m, d = _int(year), _int(month), _int(day)
    a = (14 - m) // 12
    yy = y + 4800 - a
    mm = m + 12 * a - 3
    return d + (153 * mm + 2) // 5 + 365 * yy + yy // 4 - yy // 100 + yy // 400 - 32045


def gregorian_from_jdn(jdn):
    j = _int(jdn)
    a = j + 32044
    b = (4 * a + 3) // 146097
    c = a - (146097 * b) // 4
    d = (4 * c + 3) // 1461
    e = c - (1461 * d) // 4
    m = (5 * e + 2) // 153
    day = e - (153 * m + 2) // 5 + 1
    month = m + 3 - 12 * (m // 10)
    year = 100 * b + d - 4800 + m // 10
    return year, month, day


def jd_from_gregorian(year, month, day, hour=0.0):
    if isinstance(day, (float, np.floating)):
        d = math.floor(day)
        frac = day - d
    else:
        d, frac = _int(day), 0.0
    out = (jdn_from_gregorian(year, month, d) - 0.5) + frac + np.asarray(hour, dtype=float) / 24.0
    return float(out) if np.ndim(out) == 0 else out


def gregorian_from_jd(jd, offset_hours=0.0):
    ms = _split_ms(jd, offset_hours) + MS_PER_DAY // 2
    jdn = ms // MS_PER_DAY
    y, m, d = gregorian_from_jdn(jdn)
    return y, m, d, (ms - jdn * MS_PER_DAY) / 3_600_000.0


# ------------------------------------------------------------ day of year

def day_of_year(year, month, day):
    """1 for Jan 1 ... 365/366 for Dec 31 (Julian calendar)."""
    return jdn_from_julian(year, month, day) - jdn_from_julian(year, 1, 1) + 1


def from_day_of_year(year, doy):
    """(year, month, day) of day-of-year `doy` (1-based) of a Julian year."""
    return julian_from_jdn(jdn_from_julian(year, 1, 1) + _int(doy) - 1)


def weekday(jdn):
    """0 = Sunday ... 6 = Saturday (Meeus ch. 7: (JD + 1.5) mod 7 at 0h)."""
    return (_int(jdn) + 1) % 7


# ------------------------------------------------------------- time zones

def lmt_offset_hours(lon_east_deg):
    """Local mean time minus UT, hours: longitude / 15 (east positive)."""
    return np.asarray(lon_east_deg, dtype=float) / 15.0 if np.ndim(lon_east_deg) else float(lon_east_deg) / 15.0


def civil_date(jd_ut, offset_hours):
    """(year, month, day, hours) of a UT instant in a zone `offset_hours`
    ahead of UT (proleptic Julian)."""
    return julian_from_jd(jd_ut, offset_hours)


def ut2_date(jd_ut):
    """Civil date and clock time at UT+2 (the zone B&M's dates are read in)."""
    return julian_from_jd(jd_ut, 2.0)


def lmt_date(jd_ut, lon_east_deg):
    """Civil date and local mean time at longitude lon_east_deg."""
    return julian_from_jd(jd_ut, lmt_offset_hours(lon_east_deg))


def lat_date(jd_ut, lon_east_deg, eot_hours):
    """Civil date and local APPARENT solar time: LMT + equation of time
    (apparent minus mean, hours; from odybench.ephem, which owns the Sun)."""
    return julian_from_jd(jd_ut, lmt_offset_hours(lon_east_deg) + np.asarray(eot_hours, dtype=float))


def day_bounds(year, month, day, offset_hours=0.0):
    """[start, end) of a civil day of the zone `offset_hours`, as JDs on the
    reference scale (UT for zone offsets from UT).  The end is 24:00 of the
    day = 0h of the next: windows written as 'through 31 Dec -1114 at UT+2'
    are the half-open interval [start of first day, end of last day)."""
    start = jd_from_julian(year, month, day) - np.asarray(offset_hours, dtype=float) / 24.0
    start = float(start) if np.ndim(start) == 0 else start
    return start, start + 1.0


def span_bounds(first, last, offset_hours=0.0):
    """[start, end) JDs of the civil days first..last INCLUSIVE, each given
    as (year, month, day), in the zone `offset_hours`."""
    return day_bounds(*first, offset_hours)[0], day_bounds(*last, offset_hours)[1]


# ------------------------------------------------------------ time scales

def tt_from_ut(jd_ut, delta_t_s):
    """JD(TT) = JD(UT1) + Delta-T/86400, Delta-T = TT - UT1 in seconds."""
    return np.asarray(jd_ut, dtype=float) + np.asarray(delta_t_s, dtype=float) / 86400.0


def ut_from_tt(jd_tt, delta_t_s):
    """JD(UT1) = JD(TT) - Delta-T/86400 (Delta-T evaluated by the caller at
    the instant; it changes by < 1 s per 4 days at -1177, so one evaluation
    at the TT instant suffices)."""
    return np.asarray(jd_tt, dtype=float) - np.asarray(delta_t_s, dtype=float) / 86400.0


def julian_epoch(jd_tt):
    """Julian epoch J = 2000 + (JD_TT - 2451545.0) / 365.25: the 'decimal
    year' argument of every Delta-T model in odybench.ephem (identical to
    ephem.julian_epoch).  For proleptic-Julian dates it runs about 13 days
    ahead of y + (m - 0.5)/12."""
    return 2000.0 + (np.asarray(jd_tt, dtype=float) - J2000) / 365.25


def decimal_year_nasa(year, month):
    """NASA's decimal-year convention for Delta-T polynomials: y + (m - 0.5)/12."""
    return np.asarray(year, dtype=float) + (np.asarray(month, dtype=float) - 0.5) / 12.0


def calendar_year_fraction(jd, offset_hours=0.0):
    """y + (days elapsed since 0h Jan 1 of y) / (days in y), Julian calendar."""
    y, m, d, h = julian_from_jd(jd, offset_hours)
    start = jd_from_julian(y, 1, 1)
    local = np.asarray(jd, dtype=float) + np.asarray(offset_hours, dtype=float) / 24.0
    return y + (local - start) / days_in_year(y)


# ---------------------------------------------------------------- labels

def historical_year(year):
    """'1178 BC' for -1177, 'AD 5' for 5."""
    y = int(year)
    return f"{1 - y} BC" if y <= 0 else f"AD {y}"


def astronomical_year(year, era):
    """astronomical_year(1178, 'BC') == -1177; ('AD', 5) -> 5."""
    era = era.upper().replace(".", "")
    if era in ("BC", "BCE"):
        return 1 - int(year)
    if era in ("AD", "CE"):
        return int(year)
    raise ValueError(era)


def fmt(jd, scale, offset_hours=0.0, zone=None):
    """'-1177-04-16 10:00:58 UT+2 (16 Apr 1178 BC, proleptic Julian)'.
    `scale` names jd's time scale; `zone` labels the offset (default
    scale+offset)."""
    # round the instant to the nearest second first, then split, so that 23:59:59.6 carries into the next day
    total_s = int(round((float(jd) + float(offset_hours) / 24.0) * 86400.0)) + 43200
    jdn, sod = divmod(total_s, 86400)
    y, m, d = julian_from_jdn(jdn)
    hh, rem = divmod(sod, 3600)
    mm, ss = divmod(rem, 60)
    if zone is None:
        zone = scale if offset_hours == 0 else f"{scale}{offset_hours:+g}"
    return (f"{y:+05d}-{m:02d}-{d:02d} {hh:02d}:{mm:02d}:{ss:02d} {zone} "
            f"({d} {_MONTHS[m - 1]} {historical_year(y)}, proleptic Julian)")
