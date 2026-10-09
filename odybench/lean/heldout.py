"""
odybench.lean.heldout -- the held-out test of the lean run (LEAN.md; DESIGN
7.1-7.3, 9.1).

Three parts, each a pure function of its inputs:

* flags(day0_jdn_ut2, count, allow_target=False) -> {'H1'..'H5': bool[n]}
  the five held-out predicates of DESIGN 7.1, evaluated at Ithaki.
  H3 and H4 are counted; H1, H2 and H5 are reported only.  evaluate() returns
  the same flags with their margins (for the tie bands of I15 and the report
  of 7.3).
* null_side(pools) -> the null-side quantities of 7.2: per pool n, x_max,
  the pass counts and the floor; p_H,min; Q_attain; the lattice; Q_record
  (from the frozen disclosure table's `determined` field); Q_exch (the six
  Fisher tests); and the reported R20/R21 tables.
* p_value(pools, target_flags, membership) -> the exact rank test of 7.2 at
  the target: p_P per pool, p_H, the weights, and Q_contra.

Conventions (DESIGN 0, 10.2)
----------------------------
* Day 0 is given as the JDN of its UT+2 civil date (`day0_jdn_ut2`, the
  integer JD of that date's noon; odybench.calendar).  Day n is the civil
  date Day 0 + n.  Mornings and evenings are taken on the LMT civil day of
  that date at the site; "noon (UT+2)" of Day n is JD_UT = JDN - 2/24;
  "03:30 UT" of Day n is JD_UT = JDN - 0.5 + 3.5/24 (the same calendar date
  in UT, UT+2 and LMT).
* Site: data/prereg/sites.json's `ithaki`, 38.37 N, 20.72 E, sea level, the
  site DESIGN 0 names and the core (odybench.lean.sky) uses.  (Vathy,
  38.367, 20.717, is 0.3 km away; the difference moves a rising by about a
  second.  Changed from Vathy at integration, 2026-10-09, before any pool
  was evaluated.)
* Rise and set: the topocentric, airless altitude of the body's centre
  crossing h0 = -0.5667 deg (planets) or -0.8333 deg (Sun, Moon), as the sky
  tables of 10.2 define them.  Found on an hourly grid over the LMT civil
  day and bisected to 0.06 s.
* Visible (10.3 `visible`, critical altitude 0): on the morning of a day, the
  body rises during that LMT civil day with the Sun's centre at or below -AV
  (airless); on the evening, it sets during that day with the Sun at or below
  -AV.  AV = 10 deg for Mercury, 11.5 deg for Mars (7.1).
* Positions: odybench.ephem (DE441; Vondrak precession), SMH2020 Delta-T for
  every UT -> TT conversion (I15).  Ecliptic longitudes are geocentric,
  apparent, on the true ecliptic and equinox of date.  The Moon (H2) uses
  DE431 with SMH2020 Delta-T, as DESIGN 0 pairs them.

The predicates (DESIGN 7.1, frozen)
-----------------------------------
H1  (reported) night = sunset to next sunrise, Sun's centre below -0.833 deg,
    >= 12.0 h on the night of Day -7 (seq) / Day -6 (par) [11.373] AND on the
    night of Day -3 [15.392].  (7.1 states one threshold for "that night" and
    names two lines; this module requires both, and reports each length.)
H2  (reported) the Moon above the horizon (centre above -0.8333 deg) for
    < 25% of the dark hours (Sun below -12 deg) of the night after Day -5
    (seq) / Day -4 (par), sampled every 5 min from local noon to local noon.
H3  (counted) Mercury not visible (AV 10) on the mornings and evenings of
    Day 0 and Day +1, AND a geocentric conjunction of Mercury with the Sun in
    ecliptic longitude (inferior or superior) within +-3 d of noon (UT+2) on
    Day 0 or on Day +1, i.e. in [noon(Day 0) - 3 d, noon(Day 0) + 4 d].
H4  (counted) the geocentric Venus-Mars separation at 03:30 UT <= 5 deg on
    some day of Day -10..-4 (seq: Day -7 +- 3) or Day -9..-3 (par: Day -6
    +- 3).  The count is the one on which the member passes a reading that
    defines its pool; `count='both'` (either count will do) passes on the
    union.
H5  (reported) Mars not visible (AV 11.5) on any morning or evening from
    Day -34 to Day 0.

count: 'seq' | 'par' | 'both' ('either' is accepted for 'both').  For H1 and
H2 'both' passes if either count's night passes.

The target guard: flags() and evaluate() raise ValueError if Day 0 is
16 Apr -1177 unless allow_target=True.  calendar.jdn_from_julian(-1177, 4, 16)
is 1291264 (the integer JD of that day's noon; JD 1291263.5 is its 0 h).  The
lean brief wrote "JDN 1291263", so that number is refused too, always, even
with allow_target=True: it is 15 Apr -1177, which no pool member can have as
Day 0 (the target's lunation has Day 0 on 16 Apr in UT+2), so its presence can
only mean the off-by-one.

This module writes nothing.  Run package code as `py -m`, never as a path.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from odybench import calendar as cal
from odybench import ephem as E

ROOT = Path(__file__).resolve().parents[2]
DISCLOSURE = ROOT / "data" / "prereg" / "heldout_disclosure.json"
VERDICT_RULE = ROOT / "data" / "prereg" / "verdict_rule.json"

TARGET_JDN = cal.jdn_from_julian(-1177, 4, 16)          # 1291264
GUARDED_JDNS = (TARGET_JDN, TARGET_JDN - 1)              # 1291263: the brief's number

LAT, LON, ELEV = 38.37, 20.72, 0.0                       # sites.json ithaki (DESIGN 0)
UT2_H = 2.0                                              # B&M's zone, 30 deg E
DT_MODEL = "smh2020"
H0_PLANET = -0.5667
H0_SUN = -0.8333
AV_MERCURY = 10.0
AV_MARS = 11.5
NIGHT_MIN_H = 12.0
MOON_SHARE_MAX = 0.25
DARK_SUN_ALT = -12.0
SEP_MAX_DEG = 5.0
CONJ_HALF_D = 3.0
H4_INSTANT_UT_H = 3.5
COUNTS = ("seq", "par", "both")
H4_DAYS = {"seq": tuple(range(-10, -3)), "par": tuple(range(-9, -2))}
H1_NIGHT = {"seq": -7, "par": -6}
H1_NIGHT_B = -3
H2_NIGHT = {"seq": -5, "par": -4}
H5_DAYS = tuple(range(-34, 1))

POOLS = ("P_BM", "P_MWRA", "P_BM_E", "P_MWRA_E")
BAND_POOLS = ("P_BM_E", "P_MWRA_E")
BAND = (-1877, -477)                                     # +-700 years of -1177
BAND_SPLIT = -1177                                       # early -1877..-1178, late -1177..-477
HALF_SPLIT = -900                                        # R21: early -1999..-900, late -899..+200
SPRING_POOL = "P_spring"                                 # P10's held-out part (5.2)
PATTERNS = ("both", "h4", "h3", "none")
P_MAX = 0.05
FISHER_MAX = 0.05
PREDICATES = ("H1", "H2", "H3", "H4", "H5")
GWE_FIELD = "gwe_lead_d"                                 # days from the morning GE to Day 0 (7.3, "H3 given D4")
D4_LEAD = (26.0, 30.0)
TIE_BANDS = dict(conj_d=0.1, sun_alt_deg=0.1, sep_deg=0.1)    # I15 (6.1)

_CHUNK = 60000
_N_BISECT = 16                                           # 1 h / 2^16 = 0.055 s
_DE431_SPLIT_TT = 1721425.5


# ------------------------------------------------------------------ inputs

def _norm_count(count, n):
    c = np.asarray(count, dtype=object)
    if c.ndim == 0:
        c = np.full(n, c.item(), dtype=object)
    if c.shape != (n,):
        raise ValueError(f"count has shape {c.shape}, expected ({n},)")
    out = np.empty(n, dtype=object)
    for i, v in enumerate(c):
        v = str(v).strip().lower()
        v = "both" if v == "either" else v
        if v not in COUNTS:
            raise ValueError(f"count[{i}] = {v!r}; expected 'seq', 'par' or 'both'")
        out[i] = v
    return out


def _guard(day0, allow_target):
    if np.any(day0 == TARGET_JDN - 1):
        raise ValueError(
            f"Day 0 JDN {TARGET_JDN - 1} is 15 Apr -1177, which no pool member can have; the target, "
            f"16 Apr -1177, is JDN {TARGET_JDN} (calendar.jdn_from_julian(-1177, 4, 16)). Refused always.")
    hit = np.isin(day0, np.asarray(GUARDED_JDNS, dtype=np.int64))
    if hit.any() and not allow_target:
        raise ValueError(
            "the held-out predicates may not be evaluated at the target, 16 Apr -1177 "
            f"(Day 0 JDN {TARGET_JDN}; {TARGET_JDN - 1} is refused too), before the second freeze: "
            f"{int(hit.sum())} such member(s). Pass allow_target=True only in the target stage.")


def _jdn_array(day0_jdn_ut2):
    a = np.asarray(day0_jdn_ut2)
    if a.ndim == 0:
        a = a.reshape(1)
    if a.ndim != 1:
        raise ValueError("day0_jdn_ut2 must be one-dimensional")
    if a.size and not np.all(np.asarray(a, dtype=float) == np.round(np.asarray(a, dtype=float))):
        raise ValueError("day0_jdn_ut2 must hold integer JDNs")
    return a.astype(np.int64)


# -------------------------------------------------------------- positions

def _chunks(n, size=_CHUNK):
    for i in range(0, n, size):
        yield slice(i, min(n, i + size))


def _alt(bodies, jd_ut, ephemeris="de441"):
    """{body: airless topocentric altitude of the centre (deg)} at UT instants
    jd_ut (1-D), SMH2020 Delta-T.  ephemeris 'de431' reads data/ephem/de431
    (Sun and Moon only), in chunks on one side of its split at JD 1721425.5."""
    jd_ut = np.asarray(jd_ut, dtype=float).ravel()
    out = {b: np.full(jd_ut.size, np.nan) for b in bodies}
    if jd_ut.size == 0:
        return out
    groups = [np.arange(jd_ut.size)]
    if ephemeris == "de431":
        dt_s = np.asarray(E.delta_t(E.julian_epoch(jd_ut), DT_MODEL), dtype=float)
        tt = jd_ut + dt_s / 86400.0
        groups = [np.nonzero(tt < _DE431_SPLIT_TT)[0], np.nonzero(tt >= _DE431_SPLIT_TT)[0]]
    for idx in groups:
        if idx.size == 0:
            continue
        for sl in _chunks(idx.size):
            ii = idx[sl]
            if ephemeris == "de431":
                with E.use_ephemeris(E.EPHEM_DIR / "de431"):
                    _alt_fill(bodies, jd_ut, ii, out)
            else:
                _alt_fill(bodies, jd_ut, ii, out)
    return out


def _alt_fill(bodies, jd_ut, ii, out):
    t = E.time_ut(jd_ut[ii], DT_MODEL)
    for b in bodies:
        a = E.apparent(b, t, LAT, LON, ELEV)
        out[b][ii] = np.atleast_1d(a.altaz()[0].degrees)


def _ecl_lon(bodies, jd_tt):
    """{body: geocentric apparent ecliptic longitude (deg), true ecliptic and
    equinox of date} at TT instants jd_tt (1-D)."""
    jd_tt = np.asarray(jd_tt, dtype=float).ravel()
    out = {b: np.full(jd_tt.size, np.nan) for b in bodies}
    for sl in _chunks(jd_tt.size):
        t = E.time_tt(jd_tt[sl], 0.0)
        need = tuple(dict.fromkeys(("sun", "earth") + tuple(bodies)))
        k = E.kernel(t.tt, need)
        e = k["earth"].at(t)
        eps = E.mean_obliquity(t.tt) + t._nutation_angles_radians[1]
        for b in bodies:
            v = e.observe(k[E.BODY_NAMES[b]]).apparent(deflectors=(10,)).xyz.au
            x, y, z = np.einsum("ij...,j...->i...", t.M, v)
            yl = y * np.cos(eps) + z * np.sin(eps)
            out[b][sl] = np.degrees(np.arctan2(yl, x)) % 360.0
    return out


def _separation(b1, b2, jd_ut):
    """Geocentric apparent angular separation (deg) of two bodies at UT jd_ut."""
    jd_ut = np.asarray(jd_ut, dtype=float).ravel()
    out = np.full(jd_ut.size, np.nan)
    for sl in _chunks(jd_ut.size):
        t = E.time_ut(jd_ut[sl], DT_MODEL)
        a = E.apparent(b1, t)
        b = E.apparent(b2, t)
        out[sl] = np.atleast_1d(a.separation_from(b).degrees)
    return out


def _tt_of_ut(jd_ut):
    jd_ut = np.asarray(jd_ut, dtype=float)
    return jd_ut + np.asarray(E.delta_t(E.julian_epoch(jd_ut), DT_MODEL), dtype=float) / 86400.0


def lmt_day_start_ut(jdn):
    """JD (UT) of local mean midnight that starts the LMT civil day `jdn` at
    the site: the day runs over [start, start + 1)."""
    return np.asarray(jdn, dtype=float) - 0.5 - LON / 360.0


def events(body, jdn_days, kind, h0, ephemeris="de441"):
    """Rise ('rise') or set ('set') instants of `body` in the LMT civil days
    `jdn_days` (1-D int array) at the site: crossings of the airless
    topocentric altitude h0, found on an hourly grid and bisected.
    Returns (day_index, jd_ut): one entry per crossing (a day may hold 0, 1
    or, rarely, 2)."""
    jdn_days = np.asarray(jdn_days, dtype=np.int64).ravel()
    m = jdn_days.size
    if m == 0:
        return np.zeros(0, dtype=np.int64), np.zeros(0)
    start = lmt_day_start_ut(jdn_days)
    grid = start[:, None] + np.arange(25)[None, :] / 24.0
    f = _alt([body], grid.ravel(), ephemeris)[body].reshape(m, 25) - h0
    if kind == "rise":
        cross = (f[:, :-1] < 0) & (f[:, 1:] >= 0)
    elif kind == "set":
        cross = (f[:, :-1] >= 0) & (f[:, 1:] < 0)
    else:
        raise ValueError(kind)
    di, hi = np.nonzero(cross)
    lo, up = grid[di, hi].copy(), grid[di, hi + 1].copy()
    flo = f[di, hi].copy()
    for _ in range(_N_BISECT):
        if lo.size == 0:
            break
        mid = 0.5 * (lo + up)
        fm = _alt([body], mid, ephemeris)[body] - h0
        same = (fm < 0) == (flo < 0)
        lo = np.where(same, mid, lo)
        flo = np.where(same, fm, flo)
        up = np.where(same, up, mid)
    t = 0.5 * (lo + up)
    keep = t < start[di] + 1.0                                # half-open civil day
    return di[keep], t[keep]


def visibility_margin(body, jdn_days, side, av):
    """Per LMT civil day: max over the body's risings (side 'morning') or
    settings ('evening') that day of (-AV - Sun's altitude at that instant).
    >= 0 means visible (the Sun at or below -AV); -inf when there is none."""
    jdn_days = np.asarray(jdn_days, dtype=np.int64).ravel()
    kind = "rise" if side == "morning" else "set"
    di, t = events(body, jdn_days, kind, H0_PLANET)
    out = np.full(jdn_days.size, -np.inf)
    if t.size:
        sun = _alt(["sun"], t)["sun"]
        np.maximum.at(out, di, -av - sun)
    return out


def _sun_events(jdn_days, kind):
    di, t = events("sun", jdn_days, kind, H0_SUN)
    out = np.full(np.asarray(jdn_days).size, np.nan)
    out[di] = t                                               # one per day at 38 N
    return out


def mercury_sun_conjunctions(jd_tt_lo, jd_tt_hi, step=0.25):
    """Geocentric conjunctions of Mercury with the Sun in apparent ecliptic
    longitude of date, per row in [jd_tt_lo[i], jd_tt_hi[i]] (TT): returns a
    list of arrays of instants (TT), bisected to about 0.005 s."""
    lo = np.asarray(jd_tt_lo, dtype=float).ravel()
    hi = np.asarray(jd_tt_hi, dtype=float).ravel()
    n = lo.size
    span = hi - lo
    k = int(np.ceil(span.max() / step)) + 1 if n else 1
    grid = lo[:, None] + np.arange(k)[None, :] * step
    lon = _ecl_lon(["mercury", "sun"], grid.ravel())
    d = ((lon["mercury"] - lon["sun"] + 180.0) % 360.0 - 180.0).reshape(n, k)
    s = np.sign(d)
    cross = (s[:, :-1] * s[:, 1:] <= 0) & (np.abs(d[:, :-1]) + np.abs(d[:, 1:]) < 60.0) & (s[:, :-1] != 0)
    ri, ci = np.nonzero(cross)
    a, b = grid[ri, ci].copy(), grid[ri, ci + 1].copy()
    fa = d[ri, ci].copy()
    for _ in range(22):
        if a.size == 0:
            break
        mid = 0.5 * (a + b)
        lm = _ecl_lon(["mercury", "sun"], mid)
        fm = (lm["mercury"] - lm["sun"] + 180.0) % 360.0 - 180.0
        same = np.sign(fm) == np.sign(fa)
        a = np.where(same, mid, a)
        fa = np.where(same, fm, fa)
        b = np.where(same, b, mid)
    t = 0.5 * (a + b)
    out = [[] for _ in range(n)]
    for r, x in zip(ri, t):
        if lo[r] <= x <= hi[r]:
            out[r].append(float(x))
    return [np.array(sorted(set(v))) for v in out]


# -------------------------------------------------------------- predicates

def evaluate(day0_jdn_ut2, count, allow_target=False, predicates=PREDICATES):
    """flags() with the margins behind them.  Returns a dict:
      'H1'..'H5' (bool[n], the requested ones) and
      'H1_night_a_h', 'H1_night_b_h' (night of Day -7 seq / -6 par, of Day -3;
          for count 'both' the longer of -7 and -6);
      'H2_share' (moon-up share of the dark hours; 'both': the smaller);
      'H3_vis_margin' (max over the four apparitions of -AV - Sun alt; >= 0 is
          visible), 'H3_conj_offset_d' (the conjunction nearest the window,
          days from noon UT+2 of Day 0, NaN if none within 1 d of it),
          'H3_conj_margin_d' (signed distance of that conjunction inside the
          window, negative outside);
      'H4_min_sep_deg', 'H4_min_day' (offset of the day of the minimum);
      'H5_vis_margin'."""
    day0 = _jdn_array(day0_jdn_ut2)
    n = day0.size
    cnt = _norm_count(count, n)
    _guard(day0, allow_target)
    unknown = set(predicates) - set(PREDICATES)
    if unknown:
        raise ValueError(f"unknown predicates {sorted(unknown)}")
    out = {}
    if n == 0:
        for p in predicates:
            out[p] = np.zeros(0, dtype=bool)
        return out
    if "H3" in predicates:
        out.update(_h3(day0))
    if "H4" in predicates:
        out.update(_h4(day0, cnt))
    if "H5" in predicates:
        out.update(_h5(day0))
    if "H1" in predicates:
        out.update(_h1(day0, cnt))
    if "H2" in predicates:
        out.update(_h2(day0, cnt))
    return out


def flags(day0_jdn_ut2, count, allow_target=False, predicates=PREDICATES):
    """The held-out predicates of DESIGN 7.1 at Ithaki, one row per Day 0.

    day0_jdn_ut2: int array, the JDN of each member's UT+2 Day 0.
    count: array (or one string) of 'seq' / 'par' / 'both', the day count on
        which the member passes a reading that defines its pool (H4; also
        H1 and H2).
    allow_target: must be True to evaluate 16 Apr -1177 (target stage only);
        otherwise its presence raises ValueError.
    predicates: the subset to compute (default all five).
    Returns {'H1': bool[n], ..., 'H5': bool[n]}."""
    r = evaluate(day0_jdn_ut2, count, allow_target, predicates)
    return {p: np.asarray(r[p], dtype=bool) for p in predicates}


def _h3(day0):
    n = day0.size
    days = np.concatenate([day0, day0 + 1])
    vm = np.maximum(visibility_margin("mercury", days, "morning", AV_MERCURY),
                    visibility_margin("mercury", days, "evening", AV_MERCURY))
    vis_margin = np.maximum(vm[:n], vm[n:])
    not_visible = vis_margin < 0
    noon0_ut = day0 - UT2_H / 24.0
    w0 = _tt_of_ut(noon0_ut - CONJ_HALF_D)
    w1 = _tt_of_ut(noon0_ut + 1.0 + CONJ_HALF_D)
    conj = mercury_sun_conjunctions(w0 - 1.0, w1 + 1.0)
    off = np.full(n, np.nan)
    margin = np.full(n, -np.inf)
    noon0_tt = _tt_of_ut(noon0_ut)
    for i, c in enumerate(conj):
        if c.size == 0:
            continue
        m = np.minimum(c - w0[i], w1[i] - c)               # > 0 inside the window
        j = int(np.argmax(m))
        margin[i] = m[j]
        off[i] = c[j] - noon0_tt[i]
    has_conj = margin >= 0
    return {"H3": not_visible & has_conj, "H3_vis_margin": vis_margin,
            "H3_conj_offset_d": off, "H3_conj_margin_d": margin,
            "H3_not_visible": not_visible, "H3_conj": has_conj}


def _h4(day0, cnt):
    n = day0.size
    offs = np.arange(-10, -2)                                 # union of both counts
    jd = (day0[:, None] + offs[None, :]) - 0.5 + H4_INSTANT_UT_H / 24.0
    sep = _separation("venus", "mars", jd.ravel()).reshape(n, offs.size)
    use = np.zeros((n, offs.size), dtype=bool)
    for c, ds in H4_DAYS.items():
        sel = np.isin(offs, ds)
        use[(cnt == c) | (cnt == "both"), :] |= sel[None, :]
    s = np.where(use, sep, np.inf)
    j = np.argmin(s, axis=1)
    mn = s[np.arange(n), j]
    return {"H4": mn <= SEP_MAX_DEG, "H4_min_sep_deg": mn, "H4_min_day": offs[j]}


def _h5(day0):
    n = day0.size
    offs = np.asarray(H5_DAYS)
    days = (day0[:, None] + offs[None, :]).ravel()
    m = np.maximum(visibility_margin("mars", days, "morning", AV_MARS),
                   visibility_margin("mars", days, "evening", AV_MARS)).reshape(n, offs.size)
    mx = m.max(axis=1)
    return {"H5": mx < 0, "H5_vis_margin": mx}


def _night_hours(nights):
    """Night n: sunset of LMT day n to sunrise of day n + 1 (hours)."""
    nights = np.asarray(nights, dtype=np.int64)
    s = _sun_events(nights, "set")
    r = _sun_events(nights + 1, "rise")
    return (r - s) * 24.0


def _h1(day0, cnt):
    n = day0.size
    na = {c: _night_hours(day0 + d) for c, d in H1_NIGHT.items()}
    a = np.where(cnt == "seq", na["seq"], np.where(cnt == "par", na["par"],
                                                     np.fmax(na["seq"], na["par"])))
    b = _night_hours(day0 + H1_NIGHT_B)
    return {"H1": (a >= NIGHT_MIN_H) & (b >= NIGHT_MIN_H), "H1_night_a_h": a, "H1_night_b_h": b}


def moon_dark_share(nights):
    """Share of the dark hours (Sun below -12 deg) with the Moon's centre
    above -0.8333 deg, over the night after LMT day n (local noon to local
    noon, 5-min samples at interval midpoints); DE431 + SMH2020."""
    nights = np.asarray(nights, dtype=np.int64)
    k = 288
    noon = lmt_day_start_ut(nights) + 0.5
    jd = noon[:, None] + (np.arange(k)[None, :] + 0.5) / k
    alt = _alt(["sun", "moon"], jd.ravel(), ephemeris="de431")
    dark = (alt["sun"] < DARK_SUN_ALT).reshape(nights.size, k)
    up = (alt["moon"] > H0_SUN).reshape(nights.size, k) & dark
    return up.sum(axis=1) / np.maximum(dark.sum(axis=1), 1)


def _h2(day0, cnt):
    sh = {c: moon_dark_share(day0 + d) for c, d in H2_NIGHT.items()}
    s = np.where(cnt == "seq", sh["seq"], np.where(cnt == "par", sh["par"],
                                                     np.fmin(sh["seq"], sh["par"])))
    return {"H2": s < MOON_SHARE_MAX, "H2_share": s}


def tie_band(r, i=0):
    """Which of I15's tie bands row i of an evaluate() result lies in: a
    conjunction within 0.1 d of the window's bound, a Sun altitude within 0.1
    deg of -AV at a rising or setting, a Venus-Mars separation within 0.1 deg
    of 5 deg."""
    out = []
    if "H3_vis_margin" in r and abs(r["H3_vis_margin"][i]) < TIE_BANDS["sun_alt_deg"]:
        out.append("H3 visibility")
    if "H3_conj_margin_d" in r and np.isfinite(r["H3_conj_margin_d"][i]) and             abs(r["H3_conj_margin_d"][i]) < TIE_BANDS["conj_d"]:
        out.append("H3 conjunction")
    if "H4_min_sep_deg" in r and abs(r["H4_min_sep_deg"][i] - SEP_MAX_DEG) < TIE_BANDS["sep_deg"]:
        out.append("H4 separation")
    if "H5_vis_margin" in r and abs(r["H5_vis_margin"][i]) < TIE_BANDS["sun_alt_deg"]:
        out.append("H5 visibility")
    return out


# ------------------------------------------------------------- statistics

def load_determined(path=DISCLOSURE):
    """The frozen disclosure table's `determined` field (7.1): {'H3': None |
    'pass' | 'fail', 'H4': ...}."""
    d = json.loads(Path(path).read_text(encoding="utf-8"))["determined"]
    for k, v in d.items():
        if v not in (None, "pass", "fail"):
            raise ValueError(f"determined[{k}] = {v!r}")
    return dict(d)


def _field(arr, name):
    if isinstance(arr, np.ndarray) and arr.dtype.names:
        return np.asarray(arr[name]) if name in arr.dtype.names else None
    if isinstance(arr, dict):
        return np.asarray(arr[name]) if name in arr else None
    raise TypeError("a pool must be a structured array or a dict of arrays")


def _h34(pool):
    h3 = _field(pool, "H3")
    h4 = _field(pool, "H4")
    if h3 is None or h4 is None:
        raise ValueError("a pool needs boolean fields H3 and H4")
    return h3.astype(bool), h4.astype(bool)


def _years(pool):
    jdn = _field(pool, "day0_jdn_ut2")
    if jdn is None:
        y = _field(pool, "year")
        if y is None:
            raise ValueError("a pool needs day0_jdn_ut2 (or year)")
        return y.astype(int)
    y = np.array([cal.julian_from_jdn(int(j))[0] for j in jdn], dtype=int)
    given = _field(pool, "year")
    if given is not None and given.size and not np.array_equal(given.astype(int), y):
        bad = int((given.astype(int) != y).sum())
        raise ValueError(f"{bad} member(s) have a 'year' that differs from the Julian year of day0_jdn_ut2")
    return y


def _check_masked(pools):
    for name, pool in pools.items():
        jdn = _field(pool, "day0_jdn_ut2")
        if jdn is not None and np.isin(jdn, np.asarray(GUARDED_JDNS)).any():
            raise ValueError(f"pool {name} contains the target (16 Apr -1177); the null side is masked")


def pool_counts(h3, h4):
    n = int(h3.size)
    both = int((h3 & h4).sum())
    return dict(n=n, h3_only=int((h3 & ~h4).sum()), h4_only=int((h4 & ~h3).sum()), both=both,
                neither=int((~h3 & ~h4).sum()), x3=int(h3.sum()), x4=int(h4.sum()),
                q3=(float(h3.mean()) if n else None), q4=(float(h4.mean()) if n else None),
                x_max=both, floor=(1 + both) / (1 + n))


def p_pool(h3, h4, t3, t4, member=True):
    """The exact rank p of the target in one pool (DESIGN 7.2).

    Weights w_i = -log10 q_i with q_i the pass rate of H_i over pool + target
    (symmetric in every member, so the test is exact; w_i = 0 if q_i is 0 or
    1).  s(u) = sum_i pass_i(u) w_i.  p = (1 + #{u in P: s(u) >= s(t)})/(1 + n),
    ties against the target.  p = 1 if the target is not a member."""
    h3 = np.asarray(h3, dtype=bool)
    h4 = np.asarray(h4, dtype=bool)
    n = int(h3.size)
    x3 = int(h3.sum()) + int(bool(t3))
    x4 = int(h4.sum()) + int(bool(t4))
    q3, q4 = x3 / (n + 1), x4 / (n + 1)
    w3 = -math.log10(q3) if 0 < q3 < 1 else 0.0
    w4 = -math.log10(q4) if 0 < q4 < 1 else 0.0
    s = h3 * w3 + h4 * w4
    s_t = bool(t3) * w3 + bool(t4) * w4
    x = int((s >= s_t - 1e-12).sum())
    p = (1 + x) / (1 + n) if member else 1.0
    return dict(p=p, x=x, n=n, member=bool(member), q3=q3, q4=q4, w3=w3, w4=w4, score_target=s_t)


def _pattern_flags(pattern):
    return pattern in ("both", "h3"), pattern in ("both", "h4")


def lattice(pools):
    """p_P per pool and p_H for each pass pattern of the target (both, H4
    only, H3 only, neither), the target a member of every pool (7.2)."""
    out = {}
    for pat in PATTERNS:
        t3, t4 = _pattern_flags(pat)
        pp = {P: p_pool(*_h34(pools[P]), t3, t4)["p"] for P in POOLS}
        out[pat] = dict(p=pp, p_H=max(pp.values()))
    return out


def q_record(lat, determined):
    """Q_record (7.2): no pass pattern consistent with the table's determined
    values reaches p_H <= 0.05 on the lattice."""
    consistent = []
    for pat in PATTERNS:
        t = dict(zip(("H3", "H4"), _pattern_flags(pat)))
        if any(v is not None and (v == "pass") != t[h] for h, v in determined.items() if h in t):
            continue
        consistent.append(pat)
    reach = [pat for pat in consistent if lat[pat]["p_H"] <= P_MAX]
    return (not reach), consistent


def q_contra(target_flags, determined):
    """Q_contra (7.1): a measured flag of the target differs from a determined
    value of the disclosure table."""
    diff = [h for h, v in determined.items()
            if v is not None and h in target_flags and bool(target_flags[h]) != (v == "pass")]
    return bool(diff), diff


def fisher_two_sided(a_pass, a_n, b_pass, b_n):
    if a_n == 0 or b_n == 0:
        return float("nan")
    from scipy.stats import fisher_exact
    return float(fisher_exact([[a_pass, a_n - a_pass], [b_pass, b_n - b_pass]],
                              alternative="two-sided")[1])


def _rate_test(name, mask_a, mask_b, flag, label_a, label_b):
    a_n, b_n = int(mask_a.sum()), int(mask_b.sum())
    a_p, b_p = int((flag & mask_a).sum()), int((flag & mask_b).sum())
    p = fisher_two_sided(a_p, a_n, b_p, b_n)
    return dict(test=name, a=label_a, b=label_b, a_pass=a_p, a_n=a_n, b_pass=b_p, b_n=b_n,
                fisher_p=p, computed=not math.isnan(p), fires=(not math.isnan(p)) and p <= FISHER_MAX)


def null_side(pools, determined=None):
    """The null-side quantities of DESIGN 7.2 (target masked).

    pools: {name: structured array (or dict of arrays)} with fields
        day0_jdn_ut2, year, H3, H4 (and optionally H1, H2, H5, eclipse);
        the four rule pools P_BM, P_MWRA, P_BM_E, P_MWRA_E are required.
        P10's held-out part runs on pool 'P_spring' (every spring candidate,
        5.2) and needs its boolean field 'eclipse' (a solar eclipse anywhere
        at the conjunction).  Without it, that part is reported as not
        computed and Q_exch reads the four drift tests alone.
    determined: the disclosure table's `determined` (default: read the frozen
        file).
    Returns a JSON-ready dict."""
    missing = [P for P in POOLS if P not in pools]
    if missing:
        raise ValueError(f"missing pools {missing}")
    _check_masked(pools)
    determined = load_determined() if determined is None else dict(determined)
    per = {}
    for P in POOLS:
        h3, h4 = _h34(pools[P])
        per[P] = pool_counts(h3, h4)
        y = _years(pools[P])
        if P in BAND_POOLS and y.size and ((y < BAND[0]) | (y > BAND[1])).any():
            raise ValueError(f"{P} holds members outside the band {BAND}")
        per[P]["years"] = [int(y.min()), int(y.max())] if y.size else None
    floors = {P: per[P]["floor"] for P in POOLS}
    p_h_min = max(floors.values())
    lat = lattice(pools)
    qrec, consistent = q_record(lat, determined)

    tests = []
    notes = []
    if SPRING_POOL in pools and _field(pools[SPRING_POOL], "eclipse") is not None:
        sp = pools[SPRING_POOL]
        h3, h4 = _h34(sp)
        ecl = _field(sp, "eclipse").astype(bool)
        for h, f in (("H3", h3), ("H4", h4)):
            tests.append(_rate_test(f"P10 {h}: eclipse vs other spring new moons ({SPRING_POOL})",
                                    ecl, ~ecl, f, "eclipse", "no eclipse"))
        p10 = "computed"
    else:
        for h in ("H3", "H4"):
            tests.append(dict(test=f"P10 {h}: eclipse vs other spring new moons", computed=False,
                              fires=False, fisher_p=None,
                              reason=f"no pool '{SPRING_POOL}' with an 'eclipse' field was supplied"))
        p10 = "not computed"
        notes.append("P10's held-out part was not computed (no P_spring with an 'eclipse' field); "
                     "Q_exch reads the four drift tests only.")
    for P in BAND_POOLS:
        h3, h4 = _h34(pools[P])
        y = _years(pools[P])
        early, late = y < BAND_SPLIT, y >= BAND_SPLIT
        for h, f in (("H3", h3), ("H4", h4)):
            tests.append(_rate_test(f"drift {h} in {P}: -1877..-1178 vs -1177..-477",
                                    early, late, f, "early half", "late half"))
    q_exch = any(t["fires"] for t in tests)

    # reported beside the rule (7.3): R20, R21, P10's fallback, floors with H4 dropped
    rep = {}
    bm = pools["P_BM"]
    jdn_bm = _field(bm, "day0_jdn_ut2")
    jdn_mw = _field(pools["P_MWRA"], "day0_jdn_ut2")
    if jdn_bm is not None and jdn_mw is not None:
        is_mwra = np.isin(jdn_bm, jdn_mw)
        h3, h4 = _h34(bm)
        rep["R20"] = [_rate_test(f"R20 {h} in P_BM: MWRA class vs GWE-or-station class", is_mwra, ~is_mwra,
                                 f, "MWRA", "GWE or station") for h, f in (("H3", h3), ("H4", h4))]
    r21 = []
    for P in ("P_BM", "P_MWRA"):
        h3, h4 = _h34(pools[P])
        y = _years(pools[P])
        for h, f in (("H3", h3), ("H4", h4)):
            r21.append(_rate_test(f"R21 {h} in {P}: -1999..-900 vs -899..+200", y <= HALF_SPLIT,
                                  y > HALF_SPLIT, f, "early", "late"))
            inb = (y >= BAND[0]) & (y <= BAND[1])
            r21.append(_rate_test(f"R21 {h} in {P}: within +-700 y of -1177 vs the rest", inb, ~inb,
                                  f, "band", "rest"))
    rep["R21"] = r21
    if p10 == "not computed" and _field(bm, "eclipse") is not None:
        h3, h4 = _h34(bm)
        ecl = _field(bm, "eclipse").astype(bool)
        rep["P10_fallback_on_P_BM"] = [
            _rate_test(f"P10 {h} on P_BM (fallback; not a Q_exch input)", ecl, ~ecl, f, "eclipse", "no eclipse")
            for h, f in (("H3", h3), ("H4", h4))]
    rep["floor_H3_alone"] = {P: (1 + per[P]["x3"]) / (1 + per[P]["n"]) for P in POOLS}
    gwe = _field(pools["P_MWRA"], GWE_FIELD)
    if gwe is not None:
        h3, _ = _h34(pools["P_MWRA"])
        sel = (np.asarray(gwe, dtype=float) >= D4_LEAD[0]) & (np.asarray(gwe, dtype=float) <= D4_LEAD[1])
        rep["H3_given_D4"] = dict(x=int((h3 & sel).sum()), n=int(sel.sum()),
                                  rule=f"P_MWRA members whose morning greatest elongation falls {D4_LEAD[0]}-"
                                       f"{D4_LEAD[1]} d before Day 0 ({GWE_FIELD})")
    else:
        rep["H3_given_D4"] = dict(computed=False, reason=f"P_MWRA has no field '{GWE_FIELD}'")
    for h in ("H1", "H2", "H5"):
        rates = {}
        for P in POOLS:
            f = _field(pools[P], h)
            if f is not None:
                f = np.asarray(f, dtype=bool)
                rates[P] = dict(x=int(f.sum()), n=int(f.size))
        if rates:
            rep[f"{h}_rates"] = rates

    return dict(
        stage="null (target masked)",
        pools=per,
        floors=floors,
        p_H_min=p_h_min,
        p_H_min_pool=max(floors, key=floors.get),
        Q_attain=bool(p_h_min > P_MAX),
        lattice=lat,
        determined=determined,
        Q_record=bool(qrec),
        Q_record_consistent_patterns={pat: lat[pat]["p_H"] for pat in consistent},
        Q_exch=bool(q_exch),
        Q_exch_tests=tests,
        Q_exch_complete=(p10 == "computed"),
        P10_heldout_part=p10,
        reported=rep,
        thresholds=dict(p_max=P_MAX, fisher_p_max=FISHER_MAX),
        notes=notes,
    )


def p_value(pools, target_flags, membership=None, determined=None):
    """The exact rank test of DESIGN 7.2 at the target.

    pools: as for null_side (the four rule pools, target masked).
    target_flags: {'H3': bool, 'H4': bool} (one pattern for every pool), or
        {pool: {'H3': bool, 'H4': bool}} when H4's count differs by pool.
        A 'member' key {pool: bool} is read when `membership` is None.
    membership: {pool: bool}: whether the target passes a reading that defines
        the pool (an input; p_P = 1 if it does not).  Required.
    Returns dict(p={pool: p}, p_H, weights={pool: {q3, q4, w3, w4}},
        x={pool: count}, member, pattern, Q_contra, contra_flags)."""
    _check_masked(pools)
    if membership is None:
        membership = target_flags.get("member") if isinstance(target_flags, dict) else None
    if membership is None:
        raise ValueError("the target's membership of each pool is an input (7.2); none was given")
    missing = [P for P in POOLS if P not in membership]
    if missing:
        raise ValueError(f"membership missing for {missing}")
    determined = load_determined() if determined is None else dict(determined)

    def tf(P):
        if P in target_flags and isinstance(target_flags[P], dict):
            return target_flags[P]
        return target_flags

    res, pats, contra = {}, {}, {}
    for P in POOLS:
        f = tf(P)
        t3, t4 = bool(f["H3"]), bool(f["H4"])
        res[P] = p_pool(*_h34(pools[P]), t3, t4, bool(membership[P]))
        pats[P] = {(True, True): "both", (False, True): "h4", (True, False): "h3", (False, False): "none"}[(t3, t4)]
        contra[P] = q_contra({"H3": t3, "H4": t4}, determined)
    p = {P: res[P]["p"] for P in POOLS}
    # Q_contra reads the target's measured flags; H4's is the one on the count of a defining
    # reading, so only pools the target belongs to speak (all of them if it belongs to none)
    speak = [P for P in POOLS if membership[P]] or list(POOLS)
    contra = {P: contra[P] for P in speak}
    qc = any(c[0] for c in contra.values())
    return dict(
        stage="target",
        p=p,
        p_H=max(p.values()),
        weights={P: {k: res[P][k] for k in ("q3", "q4", "w3", "w4", "score_target")} for P in POOLS},
        x={P: res[P]["x"] for P in POOLS},
        n={P: res[P]["n"] for P in POOLS},
        member={P: bool(membership[P]) for P in POOLS},
        pattern=pats,
        determined=determined,
        Q_contra=bool(qc),
        contra_flags=sorted({h for c in contra.values() for h in c[1]}),
    )


def structured(day0_jdn_ut2, **fields):
    """Helper: a pool as a structured array (day0_jdn_ut2, year, then fields)."""
    jdn = np.asarray(day0_jdn_ut2, dtype=np.int64)
    years = np.array([cal.julian_from_jdn(int(j))[0] for j in jdn], dtype=np.int64)
    dt = [("day0_jdn_ut2", "i8"), ("year", "i8")]
    for k, v in fields.items():
        v = np.asarray(v)
        dt.append((k, "?" if v.dtype == bool else v.dtype.str))
    a = np.zeros(jdn.size, dtype=dt)
    a["day0_jdn_ut2"] = jdn
    a["year"] = years
    for k, v in fields.items():
        a[k] = v
    return a
