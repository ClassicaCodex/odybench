"""
odybench.lean.almagest -- gate 3b and Q_BM of the lean run: the *Almagest*
control of B&M's own clue types (LEAN.md; DESIGN 6.4, 6.3.2, 9.1, 10.3).

The question: given real, independently dated planetary records of B&M's
kinds from the *Almagest*, with only the day intervals the text states, does a
B&M-style window search keep the true date while narrowing the window?

* regime BM, B&M's own tolerances: rec_ALM_BM = the counted sets with strict
  recall and |S0| <= 5% of the candidates; Q_BM holds if rec_ALM_BM < 6;
* regime SL, observer slack calibrated leave-one-set-out:
  seen_ALM_SL[leg] for leg in {bf, st} x {fine, mid, coarse}; gate 3b fires
  if any leg is below 6; seen_ALM_SL_side[leg] reads `same_apparition` as
  "on that side of the Sun" only (Q_score3b);
* narrowable[3b][leg][set] and N_narrow[3b][leg] on 21 null windows per set
  (Q_attain3b, printed only beside a gate that fires).

Who reads what (DESIGN 6.3.1, 6.4, 10.1; I13(c))
------------------------------------------------
* The SEARCH reads the operational fields of controls_almagest.json only
  (`operational_view`: clue_id, set, kind, record, day_offset and each
  option's name, primary flag and operational dict -- never a statement,
  licence, ref or note), the regime file almagest_regimes.json (options,
  parameters, and each row's body, side and instant, which
  tools/build_regimes.py reads off the statements by fixed rules), sites.json
  and the sky.  It is given window bounds, never a date of a record.
* `_Harness` is the only reader of controls_almagest_truth.json.  It places
  each set's window (the anchor's accepted date at a uniformly random
  position, seeds.json) and scores the search's output (6.3.2).
* `slack_table` recomputes the drafter's observer-slack table with this
  module's sky code.  It reads the truth-side record instants of
  results/controls-almagest/slack.json, and nothing else reads that file.

Stage (LEAN.md "Stages")
------------------------
Stage 1 computes no control search on the real sky.  `run()` is the null-side
step of LEAN stage 3 (attain.py calls it after Freeze 1); the top-level script
almagest.py refuses a real run before the tag prereg-1 exists unless told
otherwise.  Selftests use synthetic sets only.

Conventions (DESIGN 0, 6.4, 10.3)
---------------------------------
* Candidates: every civil day (local mean time at the site; a JDN is the JD
  of its noon) whose JDN lies in the window [a, a + 136 x 365.25), each as
  Day 0, with each row at Day 0 + its day offset (a record's crux interval
  row governs all of that record's rows).
* Instants: the row's stated equinoctial hour as local apparent time; a
  stated seasonal hour of the night at its middle; otherwise the Sun 8 deg
  below the horizon on the row's side (dawn or evening).
* Rise and set: the airless topocentric altitude of the centre crosses h0 =
  -0.8333 deg (Sun) or -0.5667 deg (planets), by Newton iteration on the
  hour angle to 1e-7 deg (well under 0.01 s).  Rise lead = sunrise - rise
  (minutes), set lag = set - sunset, on the row's civil day.
* Greatest elongation: the extremum of the geocentric Sun-planet angle on
  the row's side (east = evening), from the true Sun; conjunctions in
  apparent ecliptic longitude; the spring equinox at apparent solar
  longitude 0.  Planets and the Sun from DE441, the Moon (phase rows) from
  DE431 (the pairing rule of DESIGN 0).
* Delta-T: the four-model mixture of deltat_models.json (each model in the
  n-dot -25.82 frame; Espenak-Meeus converted from -25.858).  The sky is
  computed once at the mixture mean.  A row passes if P_mix >= 0.5.  Every
  row outcome is a set of linear constraints in Delta-T; where none lies
  within the mixture's span (6 sigma) of its bound, P_mix is exactly 0 or 1;
  otherwise P_mix is the Gaussian mass of the passing Delta-T interval,
  integrated exactly (DESIGN 6.3.3, 10.3).
* The DE441 excerpt ends at +241 Jan 1.  A candidate whose rows need sky
  beyond the data is "uncovered": it is left out of N_cand, S0 and B, the
  count is reported per window, and each seen flag is also reported with the
  uncovered days counted as all failing and as all passing (`robust`).

API for the integrator: `run(...) -> dict` (see its docstring).
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
from scipy.special import ndtr

from odybench import calendar as C
from odybench import ephem as E

ROOT = Path(__file__).resolve().parents[2]
PREREG = ROOT / "data" / "prereg"
CLUES = PREREG / "controls_almagest.json"
REGIMES = PREREG / "almagest_regimes.json"
SITES = PREREG / "sites.json"
SEEDS = PREREG / "seeds.json"
WINDOWS = PREREG / "windows.json"
TRUTH = PREREG / "controls_almagest_truth.json"          # _Harness only
SLACK_TRUTH = ROOT / "results" / "controls-almagest" / "slack.json"   # slack_table only (truth-side)
SLACK_NOTE = ROOT / "docs" / "controls-almagest.md"      # its Summary: the GE records (slack_table only)
CACHE_DIR = ROOT / "data" / "cache" / "alm"

STEPS = ("fine", "mid", "coarse")
SCORINGS = ("bf", "st")
LEGS = tuple(f"{sc}:{st}" for sc in SCORINGS for st in STEPS)
W_YEARS = 136
W_DAYS = 365.25 * W_YEARS
NARROW = 0.05
LINES = (0.04, 0.05, 0.06)
GATE_MIN = 6                       # 3b fires if a leg is below 6 of 11; Q_BM if rec_ALM_BM < 6
NARROW_MAJORITY = 11               # narrowable: in at least 11 of the 21 null windows
N_NULL = 21
N_SENS = 20
CLUSTER_DAYS = 3

H0_SUN = -0.8333
H0_PLANET = -0.5667
SIDEREAL = 360.98564736629         # deg per day
SOLAR = 360.0
DE431_SPLIT = 1721425.5            # no DE431 request may straddle it (ephem.kernel)
MIX_SPAN_SIGMA = 6.0
P_PASS = 0.5
P_REPORTED = (0.05, 0.95)
SAME_APP_OPTIONS = ("ge_after_same_apparition", "ge_before_same_apparition")
NOT_EVALUATED = ("structural", "none", "as_printed", "mean_sun_emended")

# the keys of the clue file the search may read (6.4: "the searcher reads only the operational fields")
ROW_KEYS = ("clue_id", "set", "kind", "record", "day_offset", "fork_options")
OPTION_KEYS = ("option", "primary", "operational")


# =============================================================== inputs

def _json(path: Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def operational_view(doc: dict) -> dict:
    """{set: {"set", "rows": [row]}} with only the operational keys of each row
    and option (ROW_KEYS, OPTION_KEYS).  Statements, licences, refs, notes and
    the sets' prose never reach the search."""
    sets = {s["set"]: {"set": s["set"], "rows": []} for s in doc["sets"]}
    for c in doc["clues"]:
        r = {k: c[k] for k in ROW_KEYS if k in c and k != "fork_options"}
        r["fork_options"] = [{k: o.get(k) for k in OPTION_KEYS} for o in (c.get("fork_options") or [])]
        sets[c["set"]]["rows"].append(r)
    return sets


def site(key: str) -> tuple[float, float]:
    s = _json(SITES)["sites"][key]
    return float(s["lat"]), float(s["lon"])


def _wrap180(x):
    return (np.asarray(x, dtype=float) + 180.0) % 360.0 - 180.0


# =============================================================== Delta-T

_FRAME = -25.82        # SMH's n-dot; the frame every model is put in (DESIGN 0, deltat_models.json)


def _sigma_em(y):
    y = np.asarray(y, dtype=float)
    return np.where(y < -500.0, E.sigma_huber(y), E.sigma_ms2004(y))


_DT_MODELS = (("smh2020", E.dt_smh2020, E.sigma_smh2020, -25.82),
              ("smh2020_parabola", E.dt_smh2020_parabola, E.sigma_parabola, -25.82),
              ("smh2016_parabola", E.dt_smh2016_parabola, E.sigma_parabola, -25.82),
              ("em_canon", E.dt_em2006_canon, _sigma_em, -25.858))


def dt_models(y):
    """(mu, sigma), each shaped (4,) + shape(y), seconds: the four models of the
    mixture at Julian epoch y, in the -25.82 frame."""
    y = np.asarray(y, dtype=float)
    mu = np.stack([np.asarray(f(y), dtype=float) + E.ndot_correction(y, _FRAME, fr) for _, f, _, fr in _DT_MODELS])
    sg = np.stack([np.broadcast_to(np.asarray(s(y), dtype=float), y.shape) for _, _, s, _ in _DT_MODELS])
    return mu, sg


def dt_ref(y):
    """The mixture mean (s) at Julian epoch y: the Delta-T the sky is computed at.
    A module-level function, so ephem.timescale caches one Timescale for it."""
    mu, _ = dt_models(y)
    out = mu.mean(axis=0)
    return out[()] if np.ndim(out) == 0 else out


def dt_band(y):
    """Half-width (s) of the mixture's span around dt_ref: max over the models of
    |mu - ref| + 6 sigma.  A row whose margin exceeds |slope| x band cannot
    change outcome anywhere the mixture has mass."""
    mu, sg = dt_models(y)
    return np.max(np.abs(mu - mu.mean(axis=0)) + MIX_SPAN_SIGMA * sg, axis=0)


def p_mix_interval(y, lo, hi):
    """The mixture's probability that Delta-T lies in [lo, hi] (absolute seconds,
    +-inf allowed), at Julian epoch y; equal weights, exact Gaussian masses."""
    mu, sg = dt_models(y)
    lo = np.asarray(lo, dtype=float)
    hi = np.asarray(hi, dtype=float)
    p = ndtr((hi - mu) / sg) - ndtr((lo - mu) / sg)
    return np.where(hi > lo, p.mean(axis=0), 0.0)


def _epoch_of_jd(jd):
    return C.julian_epoch(np.asarray(jd, dtype=float))


# =============================================================== sky: positions

def _time_ut(jd_ut, dt=None):
    return E.time_ut(np.asarray(jd_ut, dtype=float), dt_ref if dt is None else dt)


def _time_tt(jd_tt):
    return E.time_tt(np.asarray(jd_tt, dtype=float), dt_ref)


def _radec_topo(body, jd_ut, lat, lon, dt=None):
    """Apparent topocentric RA, Dec of date and the local apparent sidereal time (deg)."""
    t = _time_ut(jd_ut, dt)
    a = E.apparent(body, t, lat, lon)
    ra, dec, _ = a.radec(epoch="date")
    return (np.asarray(ra._degrees, dtype=float), np.asarray(dec.degrees, dtype=float),
            np.asarray(t.gast, dtype=float) * 15.0 + lon)


def _crossing(body, guess_ut, h0, rising, lat, lon, dt=None, iters=10, tol_deg=1e-7):
    """UT of the crossing of altitude h0 nearest the guess (rising or setting),
    by Newton iteration on the hour angle; NaN where the body does not cross."""
    t = np.array(guess_ut, dtype=float, copy=True)
    ok = np.isfinite(t)
    t[~ok] = np.nanmean(t) if ok.any() else 2000000.0
    phi = math.radians(lat)
    sh0 = math.sin(math.radians(h0))
    bad = ~ok
    for _ in range(iters):
        ra, dec, last = _radec_topo(body, t, lat, lon, dt)
        d = np.radians(dec)
        cosH0 = (sh0 - math.sin(phi) * np.sin(d)) / (math.cos(phi) * np.cos(d))
        H0 = np.degrees(np.arccos(np.clip(cosH0, -1.0, 1.0)))
        target = -H0 if rising else H0
        dH = _wrap180(target - _wrap180(last - ra))
        t = t + dH / SIDEREAL
        if np.nanmax(np.abs(dH)) < tol_deg:
            break
    bad |= np.abs(cosH0) > 1.0
    t[bad] = np.nan
    return t


def _altaz(body, jd_ut, lat, lon, dt=None):
    """Airless topocentric altitude and azimuth (N through E), deg; NaN in, NaN out."""
    jd = np.array(jd_ut, dtype=float, copy=True)
    ok = np.isfinite(jd)
    jd[~ok] = np.nanmean(jd) if ok.any() else 2000000.0
    ra, dec, last = _radec_topo(body, jd, lat, lon, dt)
    H = np.radians(last - ra)
    d = np.radians(dec)
    phi = math.radians(lat)
    alt = np.degrees(np.arcsin(math.sin(phi) * np.sin(d) + math.cos(phi) * np.cos(d) * np.cos(H)))
    az = np.degrees(np.arctan2(-np.cos(d) * np.sin(H), np.sin(d) * math.cos(phi) - np.cos(d) * np.cos(H) * math.sin(phi)))
    alt[~ok] = np.nan
    az = az % 360.0
    az[~ok] = np.nan
    return alt, az


def _lat_instant(midnight_ut, hours, lat, lon, iters=4):
    """UT at which local apparent solar time is `hours`, on the civil day that
    starts at midnight_ut (LMT)."""
    t = np.asarray(midnight_ut, dtype=float) + hours / 24.0
    target = _wrap180((hours - 12.0) * 15.0)
    for _ in range(iters):
        ra, _, last = _radec_topo("sun", t, lat, lon)
        dH = _wrap180(target - _wrap180(last - ra))
        t = t + dH / SOLAR
    return t


def _geo_unit_lon(bodies, t):
    """{body: (unit vector of date (3, n), apparent ecliptic longitude of date)}, geocentric."""
    need = tuple(sorted(set(bodies) | {"sun", "earth"}))
    k = E.kernel(t.tt, need)
    e = k["earth"].at(t)
    eps = E.mean_obliquity(t.tt) + t._nutation_angles_radians[1]
    out = {}
    for b in bodies:
        v = e.observe(k[E.BODY_NAMES[b]]).apparent(deflectors=(10,)).xyz.au
        x, y, z = np.einsum("ij...,j...->i...", t.M, v)
        r = np.sqrt(x * x + y * y + z * z)
        yl = y * np.cos(eps) + z * np.sin(eps)
        out[b] = (np.stack([x / r, y / r, z / r]), np.degrees(np.arctan2(yl, x)) % 360.0)
    return out


def _signed_elong_dlon(body, jd_tt):
    """(signed elongation, wrap180(lambda_body - lambda_sun)), deg, geocentric, true Sun.
    East (evening side) positive."""
    t = _time_tt(jd_tt)
    g = _geo_unit_lon((body, "sun"), t)
    ub, lb = g[body]
    us, ls = g["sun"]
    dot = np.sum(ub * us, axis=0)
    crs = np.linalg.norm(np.cross(ub.T, us.T), axis=-1) if ub.ndim == 2 else np.linalg.norm(np.cross(ub, us))
    sep = np.degrees(np.arctan2(crs, dot))
    dl = _wrap180(lb - ls)
    return np.where(dl >= 0.0, sep, -sep), dl


def _sun_lon(jd_tt):
    t = _time_tt(jd_tt)
    return _geo_unit_lon(("sun",), t)["sun"][1]


def _moon_elong(jd_ut):
    """(lambda_moon - lambda_sun) mod 360 (deg), geocentric apparent, at UT jd_ut:
    DE431 (the lunar pairing of DESIGN 0), in pieces that never straddle its split."""
    jd = np.array(jd_ut, dtype=float, copy=True)
    out = np.full(jd.shape, np.nan)
    ok = np.isfinite(jd)
    if not ok.any():
        return out
    tt = jd + dt_ref(_epoch_of_jd(jd)) / 86400.0
    m_lo, m_hi = _de431_span()
    ok &= (tt > m_lo) & (tt < m_hi)                       # outside DE431: NaN, so the row is uncovered
    with E.use_ephemeris(E.EPHEM_DIR / "de431"):
        for part in (ok & (tt < DE431_SPLIT), ok & (tt >= DE431_SPLIT)):
            if part.any():
                t = _time_ut(jd[part])
                g = _geo_unit_lon(("moon", "sun"), t)
                out[part] = (g["moon"][1] - g["sun"][1]) % 360.0
    return out


# =============================================================== sky: day tables

def _day_chunk(args):
    """Worker: the per-civil-day columns for days [j0, j1) at (lat, lon)."""
    lat, lon, j0, j1, needs = args
    jdn = np.arange(j0, j1, dtype=np.int64)
    m0 = jdn - 0.5 - lon / 360.0                          # UT of local mean midnight starting the civil day
    out = {"jdn": jdn}
    out["sun_rise"] = _crossing("sun", m0 + 0.25, H0_SUN, True, lat, lon)
    out["sun_set"] = _crossing("sun", m0 + 0.75, H0_SUN, False, lat, lon)
    out["dawn8"] = _crossing("sun", out["sun_rise"] - 0.02, -8.0, True, lat, lon)
    out["dusk8"] = _crossing("sun", out["sun_set"] + 0.02, -8.0, False, lat, lon)
    for h in needs["lat_hours"]:
        out[f"lat:{h:g}"] = _lat_instant(m0, float(h), lat, lon)
    for b in needs["horizon_bodies"]:
        rise = _crossing(b, out["sun_rise"], H0_PLANET, True, lat, lon)
        sett = _crossing(b, out["sun_set"], H0_PLANET, False, lat, lon)
        out[f"{b}:rise"] = rise
        out[f"{b}:lead"] = (out["sun_rise"] - rise) * 1440.0
        out[f"{b}:lag"] = (sett - out["sun_set"]) * 1440.0
        if b in needs["rise_az_bodies"]:
            out[f"{b}:rise_az"] = _altaz(b, rise, lat, lon)[1]
    inst = {k: out[k] for k in out if k.startswith("lat:")}
    inst["sun-8:morning"] = out["dawn8"]
    inst["sun-8:evening"] = out["dusk8"]
    for b, key in needs["alts"]:
        out[f"alt:{b}@{key}"] = _altaz(b, inst[key], lat, lon)[0]
    for key in needs["moon_keys"]:
        out[f"moonE@{key}"] = _moon_elong(inst[key])
    return out


def _bisect_cross(func, lo, hi, iters=40):
    """Vectorised bisection of func(t) = 0 on brackets [lo, hi] with func(lo) < 0 <= func(hi)."""
    lo = np.array(lo, dtype=float, copy=True)
    hi = np.array(hi, dtype=float, copy=True)
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        f = func(mid)
        neg = f < 0.0
        lo = np.where(neg, mid, lo)
        hi = np.where(neg, hi, mid)
    return 0.5 * (lo + hi)


def _refine_max(func, tc, steps=(1.0, 0.3, 0.1, 0.02, 0.004, 0.001)):
    """Vectorised parabolic refinement of local maxima of func near tc."""
    tc = np.array(tc, dtype=float, copy=True)
    for h in steps:
        a, b, c = func(tc - h), func(tc), func(tc + h)
        den = a - 2.0 * b + c
        with np.errstate(divide="ignore", invalid="ignore"):
            d = np.where(den < 0.0, 0.5 * h * (a - c) / den, 0.0)
        tc = tc + np.clip(d, -h, h)
    return tc


def _geo_chunk(args):
    """Worker: geocentric events with TT instants in [t0, t1): greatest
    elongations east and west and conjunctions of Mercury and Venus, and spring
    equinoxes.  The daily grid runs 3 days past each end."""
    t0, t1, bodies = args
    grid = np.arange(math.floor(t0) - 3.0, math.ceil(t1) + 4.0, 1.0)
    out = {}
    for b in bodies:
        se, dl = _signed_elong_dlon(b, grid)
        for side, s in (("east", 1.0), ("west", -1.0)):
            v = s * se
            i = np.nonzero((v[1:-1] > v[:-2]) & (v[1:-1] >= v[2:]) & (v[1:-1] > 0.0))[0] + 1
            if len(i):
                f = lambda x, b=b, s=s: s * _signed_elong_dlon(b, x)[0]
                tg = _refine_max(f, grid[i])
                val = f(tg)
                keep = (tg >= t0) & (tg < t1) & (val > 0.0)
                out[f"ge:{b}:{side}"] = tg[keep]
                out[f"ge:{b}:{side}:val"] = val[keep]
            else:
                out[f"ge:{b}:{side}"] = np.zeros(0)
                out[f"ge:{b}:{side}:val"] = np.zeros(0)
        i = np.nonzero((np.sign(dl[:-1]) != np.sign(dl[1:])) & (np.abs(dl[:-1] - dl[1:]) < 90.0))[0]
        if len(i):
            lo, hi = grid[i], grid[i + 1]
            sgn = np.where(dl[i] < 0.0, 1.0, -1.0)           # make func(lo) < 0
            f = lambda x, b=b, lo=lo, sgn=sgn: sgn * _signed_elong_dlon(b, x)[1]
            tc = _bisect_cross(f, lo, hi)
            out[f"conj:{b}"] = tc[(tc >= t0) & (tc < t1)]
        else:
            out[f"conj:{b}"] = np.zeros(0)
    ls = _wrap180(_sun_lon(grid))
    i = np.nonzero((ls[:-1] < 0.0) & (ls[1:] >= 0.0) & (ls[1:] - ls[:-1] < 90.0))[0]
    if len(i):
        te = _bisect_cross(lambda x: _wrap180(_sun_lon(x)), grid[i], grid[i + 1])
        out["equinox"] = te[(te >= t0) & (te < t1)]
    else:
        out["equinox"] = np.zeros(0)
    return out


class SkyTable:
    """Per-civil-day sky columns at one site for JDNs jdn0 .. jdn0 + n - 1, and
    geocentric event lists (TT) complete inside [ev_lo, ev_hi)."""

    def __init__(self, site_key, lat, lon, jdn0, cols, events, ev_lo, ev_hi, needs):
        self.site_key, self.lat, self.lon = site_key, float(lat), float(lon)
        self.jdn0 = int(jdn0)
        self.cols = cols
        self.n = len(cols["jdn"])
        self.events = events
        self.ev_lo, self.ev_hi = float(ev_lo), float(ev_hi)
        self.needs = needs
        self.epoch = _epoch_of_jd(self.cols["jdn"].astype(float))
        self._derived()

    def _derived(self):
        c = self.cols
        prev_set = np.concatenate([[np.nan], c["sun_set"][:-1]])
        night = c["sun_rise"] - prev_set
        for h in range(1, 13):                         # middle of seasonal night hour h (sunset .. sunrise)
            c[f"night:{h}:middle"] = prev_set + night * (h - 0.5) / 12.0
        self.mwra = _mwra_columns(c["mercury:rise_az"], c["mercury:rise"]) if "mercury:rise_az" in c else None

    def instant_ut(self, key):
        return {"sun-8:morning": self.cols["dawn8"], "sun-8:evening": self.cols["dusk8"]}.get(key, self.cols.get(key))

    def to_npz(self, path):
        arrs = {f"col::{k}": v for k, v in self.cols.items() if not k.startswith("night:")}
        arrs.update({f"ev::{k}": v for k, v in self.events.items()})
        meta = {"site": self.site_key, "lat": self.lat, "lon": self.lon, "jdn0": self.jdn0,
                "ev_lo": self.ev_lo, "ev_hi": self.ev_hi, "needs": self.needs}
        arrs["meta"] = np.frombuffer(json.dumps(meta).encode("utf-8"), dtype=np.uint8)
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        np.savez(path, **arrs)

    @classmethod
    def from_npz(cls, path):
        z = np.load(path)
        meta = json.loads(bytes(z["meta"]).decode("utf-8"))
        cols = {k[5:]: z[k] for k in z.files if k.startswith("col::")}
        ev = {k[4:]: z[k] for k in z.files if k.startswith("ev::")}
        return cls(meta["site"], meta["lat"], meta["lon"], meta["jdn0"], cols, ev, meta["ev_lo"], meta["ev_hi"],
                   meta["needs"])


def _mwra_columns(az, rise_ut):
    """For each day: the vertex instant of the discrete local maximum of
    Mercury's rising azimuth nearest that day (ties: the earlier), from a
    least-squares parabola through the 7 mornings centred on it (DESIGN 3.2
    step 5, MWRA_vtx), and the day's distance to that maximum."""
    n = len(az)
    a = np.asarray(az, dtype=float)
    i = np.arange(1, n - 1)
    ismax = (a[i] > a[i - 1]) & (a[i] >= a[i + 1]) & np.isfinite(a[i - 1]) & np.isfinite(a[i + 1])
    M = i[ismax]
    M = M[(M >= 3) & (M <= n - 4)]
    vert = np.full(len(M), np.nan)
    x = np.arange(-3, 4, dtype=float)
    if len(M):
        Y = np.stack([a[M + k] for k in range(-3, 4)], axis=1)
        good = np.all(np.isfinite(Y), axis=1)
        V = np.vander(x, 3)                               # columns x^2, x, 1
        coef = np.linalg.lstsq(V, Y[good].T, rcond=None)[0]
        c2, c1 = coef[0], coef[1]
        xv = np.where(c2 < 0.0, -c1 / (2.0 * np.where(c2 < 0.0, c2, -1.0)), 0.0)
        xv = np.clip(xv, -3.0, 3.0)
        fi = M[good] + xv
        vert[good] = np.interp(fi, np.arange(n, dtype=float), rise_ut)
    nearest = np.full(n, -1, dtype=np.int64)
    dist = np.full(n, np.inf)
    if len(M):
        j = np.arange(n)
        k = np.searchsorted(M, j)
        lo = np.clip(k - 1, 0, len(M) - 1)
        hi = np.clip(k, 0, len(M) - 1)
        dlo = np.abs(j - M[lo])
        dhi = np.abs(M[hi] - j)
        pick = np.where(dhi < dlo, hi, lo)                # ties: the earlier maximum
        nearest = pick
        dist = np.minimum(dlo, dhi).astype(float)
    vt = np.where(nearest >= 0, vert[np.clip(nearest, 0, max(len(M) - 1, 0))] if len(M) else np.nan, np.nan)
    return {"vertex_ut": vt, "dist_days": dist}


def needs_from_regimes(reg: dict) -> dict:
    """The sky columns the regime file's rows need: LAT hours, horizon bodies,
    (body, instant) altitudes and the Moon's elongation instants."""
    lat_hours, alts, moon = set(), set(), set()
    for s in reg["sets"].values():
        for cid, p in s["row_predicates"].items():
            key = instant_key(p["instant"])
            if key.startswith("lat:"):
                lat_hours.add(float(key[4:]))
            if p["body"] == "moon":
                moon.add(key)
            if p["body"] in ("mars", "jupiter", "saturn", "mercury", "venus"):
                alts.add((p["body"], key))
    return {"lat_hours": sorted(lat_hours), "horizon_bodies": ["mercury", "venus"], "rise_az_bodies": ["mercury"],
            "alts": sorted(a for a in alts if a[0] in ("mars", "jupiter")), "moon_keys": sorted(moon)}


def _merge_needs(a: dict, b: dict) -> dict:
    return {"lat_hours": sorted(set(a["lat_hours"]) | set(b["lat_hours"])),
            "horizon_bodies": sorted(set(a["horizon_bodies"]) | set(b["horizon_bodies"])),
            "rise_az_bodies": sorted(set(a["rise_az_bodies"]) | set(b["rise_az_bodies"])),
            "alts": sorted({tuple(x) for x in a["alts"]} | {tuple(x) for x in b["alts"]}),
            "moon_keys": sorted(set(a["moon_keys"]) | set(b["moon_keys"]))}


def canonical_needs(reg: dict | None = None) -> dict:
    """The columns of the frozen regime file, merged with those of `reg` (the
    same file in a real run), so that every run reads one table."""
    base = needs_from_regimes(_json(REGIMES)) if REGIMES.exists() else None
    mine = needs_from_regimes(reg) if reg is not None else None
    if base is None:
        return mine
    return base if mine is None else _merge_needs(base, mine)


def canonical_span() -> tuple[int, int]:
    """Civil days from 10 days before the null-window range (windows.json) to the
    end of the ephemeris: every window of the run lies inside it."""
    y0 = _json(WINDOWS)["spans"]["null_window_range"]["years"][0]
    return int(C.jdn_from_julian(y0, 1, 1)) - 10, ephemeris_days()[1]


def instant_key(inst: dict) -> str:
    if inst["kind"] == "lat":
        return f"lat:{float(inst['hours']):g}"
    if inst["kind"] == "sun_alt":
        if float(inst["deg"]) != -8.0:
            raise ValueError(f"unknown twilight instant {inst}")
        return f"sun-8:{inst['part']}"
    if inst["kind"] == "night_hour":
        return f"night:{int(inst['hour'])}:{inst['point']}"
    raise ValueError(f"unknown instant {inst}")


def ephemeris_days() -> tuple[int, int]:
    """The civil days (JDN) the DE441 excerpts can serve for every body this
    module needs, with a day's margin at each end (ephem.coverage)."""
    need = {10, 199, 299, 301, 399, 4, 5}
    # ephem.kernel serves a request from ONE excerpt, so the span is that of the longest excerpt holding
    # every body (today de441_m2060_p0241.bsp); an extension to +300 should come as one excerpt too
    spans = [(jd1 - jd0, jd0, jd1) for _, jd0, jd1, t in E.coverage() if need <= set(t)]
    _, lo, hi = max(spans)
    return int(math.ceil(lo)) + 2, int(math.floor(hi)) - 2


def _de431_span() -> tuple[float, float]:
    """TT span of the DE431 lunar excerpts (Sun, Moon, Earth); its two long pieces
    meet at the split, which _moon_elong never straddles."""
    spans = [(jd0, jd1) for _, jd0, jd1, t in E.coverage(E.EPHEM_DIR / "de431") if {10, 301, 399} <= set(t)]
    return min(s[0] for s in spans) + 1.0, max(s[1] for s in spans) - 1.0


def build_table(site_key, jdn_lo, jdn_hi, needs, workers=None, cache=True, chunk=1500, ev_margin=420,
                progress=None) -> SkyTable:
    """The SkyTable for civil days [jdn_lo, jdn_hi] at the site, clipped to the
    ephemeris; event lists over the same span +- ev_margin days (clipped)."""
    lat, lon = site(site_key)
    e_lo, e_hi = ephemeris_days()
    j0, j1 = max(int(jdn_lo), e_lo), min(int(jdn_hi), e_hi)
    if j1 <= j0:
        raise ValueError("the requested span lies outside the ephemeris")
    key = hashlib.sha256(json.dumps([site_key, lat, lon, j0, j1, needs, ev_margin, _CODE_VERSION],
                                    sort_keys=True).encode()).hexdigest()[:16]
    path = CACHE_DIR / f"sky_{site_key}_{j0}_{j1}_{key}.npz"
    if cache and path.exists():
        return SkyTable.from_npz(path)
    t_start = time.time()
    tasks = [(lat, lon, a, min(a + chunk, j1 + 1), needs) for a in range(j0, j1 + 1, chunk)]
    # the event grids run 4 days past each end of their span: keep them inside the data
    ev_lo = max(j0 - ev_margin, e_lo + 6) - 0.5
    ev_hi = min(j1 + ev_margin, e_hi - 6) - 0.5
    step = 3000.0
    gtasks = [(a, min(a + step, ev_hi), ["mercury", "venus"]) for a in np.arange(ev_lo, ev_hi, step)]
    workers = workers or max(1, (os.cpu_count() or 2) - 2)
    if workers > 1 and len(tasks) + len(gtasks) > 2:
        # one BLAS thread per worker process (spawned children read these at numpy import);
        # skyfield's nutation series is a large matrix product and oversubscribes otherwise
        for var in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
            os.environ.setdefault(var, "1")
        with ProcessPoolExecutor(max_workers=workers) as ex:
            parts = list(ex.map(_day_chunk, tasks))
            gparts = list(ex.map(_geo_chunk, gtasks))
    else:
        parts = [_day_chunk(t) for t in tasks]
        gparts = [_geo_chunk(t) for t in gtasks]
    cols = {k: np.concatenate([p[k] for p in parts]) for k in parts[0]}
    events = {k: np.sort(np.concatenate([g[k] for g in gparts])) for k in gparts[0] if not k.endswith(":val")}
    for k in gparts[0]:
        if k.endswith(":val"):
            base = k[:-4]
            t_all = np.concatenate([g[base] for g in gparts])
            v_all = np.concatenate([g[k] for g in gparts])
            events[k] = v_all[np.argsort(t_all)]
    tab = SkyTable(site_key, lat, lon, j0, cols, events, ev_lo, ev_hi, needs)
    if progress:
        progress(f"sky table {site_key} {j0}..{j1} ({tab.n} days) built in {time.time() - t_start:.0f} s")
    if cache:
        tab.to_npz(path)
    return tab


_CODE_VERSION = "alm-sky-2"


# =============================================================== row predicates

def _p_from_constraints(cons, fail, cov, y):
    """P_mix per element from linear constraints m + s x >= 0, x = Delta-T - ref (s).
    cons: list of (m, s) arrays; fail: certain failures; cov: covered mask; y: epoch.
    Returns (p, inband): p is 0/1 outside the band and the exact mass inside."""
    n = len(cov)
    band = dt_band(y)
    p = np.ones(n)
    certain_fail = fail.copy()
    uncertain = np.zeros(n, dtype=bool)
    for m, s in cons:
        m = np.asarray(m, dtype=float)
        s = np.broadcast_to(np.asarray(s, dtype=float), (n,))
        reach = np.abs(s) * band
        with np.errstate(invalid="ignore"):
            certain_fail |= ~(m + reach >= 0.0)
            uncertain |= (m - reach < 0.0) & (m + reach >= 0.0)
    p[certain_fail] = 0.0
    todo = uncertain & ~certain_fail & cov
    if todo.any():
        idx = np.nonzero(todo)[0]
        L = np.full(len(idx), -np.inf)
        U = np.full(len(idx), np.inf)
        empty = np.zeros(len(idx), dtype=bool)
        for m, s in cons:
            mm = np.asarray(m, dtype=float)[idx]
            ss = np.broadcast_to(np.asarray(s, dtype=float), (n,))[idx]
            pos, neg, zer = ss > 0, ss < 0, ss == 0
            with np.errstate(divide="ignore", invalid="ignore"):
                L = np.where(pos, np.maximum(L, -mm / np.where(pos, ss, 1.0)), L)
                U = np.where(neg, np.minimum(U, -mm / np.where(neg, ss, 1.0)), U)
            empty |= zer & (mm < 0.0)
        ref = dt_ref(y[idx])
        pm = p_mix_interval(y[idx], ref + L, ref + U)
        p[idx] = np.where(empty, 0.0, pm)
    p[~cov] = np.nan
    return p, todo


def _nearest_event(ev, t):
    """(nearest event time, ok) for each t; ok is False where ev is empty."""
    if len(ev) == 0:
        return np.full(np.shape(t), np.nan), np.zeros(np.shape(t), dtype=bool)
    k = np.searchsorted(ev, t)
    lo = ev[np.clip(k - 1, 0, len(ev) - 1)]
    hi = ev[np.clip(k, 0, len(ev) - 1)]
    pick = np.where(np.abs(hi - t) < np.abs(t - lo), hi, lo)
    return pick, np.isfinite(t)


DT_FD = 600.0             # s: the finite-difference step of the in-band slopes


def _dt_plus(y):
    return dt_ref(y) + DT_FD


def _dt_minus(y):
    return dt_ref(y) - DT_FD


def _lead_slope(tab, body, side, jdn):
    """d(lead or lag)/d(Delta-T), min per s, by central differences (+-600 s),
    vectorised over the days; the instants are recomputed at each Delta-T."""
    lat, lon = tab.lat, tab.lon
    m0 = np.asarray(jdn, dtype=float) - 0.5 - lon / 360.0
    vals = []
    for dt in (_dt_minus, _dt_plus):
        if side == "morning":
            sr = _crossing("sun", m0 + 0.25, H0_SUN, True, lat, lon, dt=dt)
            br = _crossing(body, sr, H0_PLANET, True, lat, lon, dt=dt)
            vals.append((sr - br) * 1440.0)
        else:
            ss = _crossing("sun", m0 + 0.75, H0_SUN, False, lat, lon, dt=dt)
            bs = _crossing(body, ss, H0_PLANET, False, lat, lon, dt=dt)
            vals.append((bs - ss) * 1440.0)
    return (vals[1] - vals[0]) / (2.0 * DT_FD)


def _alt_slope(tab, body, key, idx):
    """d(altitude)/d(Delta-T) at the row's instant, deg per s; a twilight instant is
    recomputed at each Delta-T (a LAT instant moves by well under a second)."""
    lat, lon = tab.lat, tab.lon
    m0 = tab.cols["jdn"][idx].astype(float) - 0.5 - lon / 360.0
    vals = []
    for dt in (_dt_minus, _dt_plus):
        if key.startswith("sun-8:"):
            morning = key.endswith("morning")
            g = (tab.cols["sun_rise"][idx] - 0.02) if morning else (tab.cols["sun_set"][idx] + 0.02)
            inst = _crossing("sun", g, -8.0, morning, lat, lon, dt=dt)
        else:
            inst = tab.instant_ut(key)[idx]
        vals.append(_altaz(body, inst, lat, lon, dt=dt)[0])
    del m0
    return (vals[1] - vals[0]) / (2.0 * DT_FD)


SLOPE_LEAD_MAX = 3e-4      # min per s of Delta-T: a bound for the band test of lead rows (Mercury's
#                            relative RA and Dec motion gives at most about 2.5e-4); in-band days are measured
SLOPE_ALT_MAX = 1e-4       # deg per s: a bound for altitude rows at a fixed local instant (about 3e-5 at most)


def evaluate_row(tab: SkyTable, option: str, params: dict, pred: dict, side_only: bool = False):
    """P_mix(row passes) for every table day as the row's civil day.
    Returns (p, cov, inband): p in [0, 1] (NaN where not covered)."""
    n = tab.n
    y = tab.epoch
    key = instant_key(pred["instant"])
    inst_ut = tab.instant_ut(key)
    body, side = pred["body"], pred["side"]
    cov = np.isfinite(inst_ut)
    t_tt = inst_ut + dt_ref(y) / 86400.0
    fail = np.zeros(n, dtype=bool)
    cons = []
    sec = 1.0 / 86400.0
    if option in ("ge_true_k", "bm_k_1d"):
        k = float(params["k_days"])
        ev = tab.events[f"ge:{body}:{'east' if side == 'evening' else 'west'}"]
        g, ok = _nearest_event(ev, t_tt)
        cov &= ok & (t_tt - k - 1.0 >= tab.ev_lo) & (t_tt + k + 1.0 < tab.ev_hi)
        off = t_tt - g
        cons += [(k - off, -sec), (k + off, sec)]
    elif option in SAME_APP_OPTIONS or option.endswith("_within_j"):
        side_name = "east" if side == "evening" else "west"
        conj = tab.events[f"conj:{body}"]
        ge = tab.events[f"ge:{body}:{side_name}"]
        kc = np.searchsorted(conj, t_tt, side="right")
        has = (kc > 0) & (kc < len(conj))
        cprev = conj[np.clip(kc - 1, 0, len(conj) - 1)]
        cnext = conj[np.clip(kc, 0, len(conj) - 1)]
        cov &= has & (cprev > tab.ev_lo) & (cnext < tab.ev_hi)
        after = option.startswith("ge_after")
        if option.endswith("_within_j"):
            j = float(params["j_days"])
            if after:
                kg = np.searchsorted(ge, t_tt)
                gnext = ge[np.clip(kg, 0, len(ge) - 1)]
                fail |= kg >= len(ge)
                cov &= t_tt + j + 1.0 < tab.ev_hi
                cons += [(gnext - t_tt, -sec), (j - (gnext - t_tt), sec)]
            else:
                kg = np.searchsorted(ge, t_tt) - 1
                gprev = ge[np.clip(kg, 0, len(ge) - 1)]
                fail |= kg < 0
                cov &= t_tt - j - 1.0 >= tab.ev_lo
                cons += [(t_tt - gprev, sec), (j - (t_tt - gprev), -sec)]
        else:
            kg = np.searchsorted(ge, cprev, side="right")
            g = ge[np.clip(kg, 0, len(ge) - 1)]
            inside = (kg < len(ge)) & (g < cnext)
            fail |= ~inside
            cons += [(t_tt - cprev, sec), (cnext - t_tt, -sec)]
            cons += [(g - t_tt, -sec)] if after else [(t_tt - g, sec)]
            if not side_only:
                vis = tab.cols[f"{body}:lead"] if side == "morning" else tab.cols[f"{body}:lag"]
                cov &= np.isfinite(vis)
                cons += [(vis - float(params["visible_min_minutes"]), SLOPE_LEAD_MAX * np.sign(1.0))]
    elif option in ("visible_only", "bm_venus_lead"):
        vis = tab.cols[f"{body}:lead"] if (side == "morning" or option == "bm_venus_lead") else tab.cols[f"{body}:lag"]
        lim = float(params["min_minutes_between_body_and_sun_horizon_crossings"]) if option == "visible_only" \
            else float(params["lead_min"])
        cov &= np.isfinite(vis)
        cons += [(vis - lim, SLOPE_LEAD_MAX)]
    elif option == "visible_before_sunrise":
        alt = tab.cols[f"alt:{body}@{key}"]
        cov &= np.isfinite(alt)
        cons += [(alt - float(params["min_altitude_deg"]), SLOPE_ALT_MAX)]
    elif option == "phase_class":
        Ecol = tab.cols[f"moonE@{key}"]
        cov &= np.isfinite(Ecol)
        rate = 16.0 / 86400.0                             # deg per s of Delta-T: a bound (the rate is 10-15 deg/day);
        #                                                   in-band days get their measured rate below
        cls = params["class"]
        tol = float(params.get("tolerance_days", 0.0) or 0.0)
        e180 = _wrap180(Ecol)
        if cls == "young_crescent":
            cons += [(e180, rate), (45.0 - e180, -rate)]
        elif cls == "waxing_crescent":
            cons += [(e180, rate), (90.0 - e180, -rate)]
        elif cls == "waning_crescent":
            cons += [(-e180, -rate), (e180 + 90.0, rate)]
        elif cls == "near_full":
            cons += [(Ecol - 150.0, rate), (210.0 - Ecol, -rate)]
        elif cls in ("first_quarter", "last_quarter", "full"):
            c0 = {"first_quarter": 90.0, "last_quarter": 270.0, "full": 180.0}[cls]
            w = 12.2 * tol
            d = Ecol - c0
            cons += [(w - d, -rate), (w + d, rate)]
        else:
            raise ValueError(f"unknown phase class {cls!r}")
    elif option == "equinox_tol":
        tol = float(params["tolerance_days"])
        q, ok = _nearest_event(tab.events["equinox"], t_tt)
        cov &= ok & (t_tt - tol - 1.0 >= tab.ev_lo) & (t_tt + tol + 1.0 < tab.ev_hi)
        off = t_tt - q
        cons += [(tol - off, -sec), (tol + off, sec)]
    elif option == "bm_mwra_k":
        if body != "mercury" or tab.mwra is None:
            raise ValueError("bm_mwra_k is defined for Mercury's rising only")
        k = float(params["k_days"])
        rise = tab.cols["mercury:rise"]
        dlt = rise - tab.mwra["vertex_ut"]
        jj = np.arange(n)
        cov &= np.isfinite(dlt) & (jj >= 8) & (jj < n - 8)
        # the azimuth series moves with TT, so Delta grows with Delta-T at about 1 s per s (linearised)
        cons += [(k - dlt, -sec), (k + dlt, sec)]
    else:
        raise ValueError(f"no predicate for option {option!r}")
    p, inband = _p_from_constraints(cons, fail, cov, y)
    # refine the in-band rows whose slope was only bounded: leads, altitudes, the Moon's rate
    if inband.any() and option in ("visible_only", "bm_venus_lead", "visible_before_sunrise", "phase_class") \
            or (inband.any() and option in SAME_APP_OPTIONS and not side_only):
        p = _refine_inband(tab, option, params, pred, cons, fail, cov, y, inband, p, side_only)
    return p, cov, inband


def _refine_inband(tab, option, params, pred, cons, fail, cov, y, inband, p, side_only):
    """Re-evaluate in-band rows with measured slopes instead of bounds."""
    idx = np.nonzero(inband)[0]
    body, side = pred["body"], pred["side"]
    key = instant_key(pred["instant"])
    new_cons = []
    for m, s in cons:
        s_arr = np.array(np.broadcast_to(np.asarray(s, dtype=float), (tab.n,)), dtype=float)
        if option in ("visible_only", "bm_venus_lead") or (option in SAME_APP_OPTIONS and abs(s_arr[0]) == SLOPE_LEAD_MAX):
            sd = "morning" if (side == "morning" or option == "bm_venus_lead") else "evening"
            s_arr[idx] = _lead_slope(tab, body, sd, tab.cols["jdn"][idx])
        elif option == "visible_before_sunrise":
            s_arr[idx] = _alt_slope(tab, body, key, idx)
        elif option == "phase_class":
            inst = tab.instant_ut(key)
            e1 = _moon_elong(inst[idx] - 0.01)
            e2 = _moon_elong(inst[idx] + 0.01)
            rate = (_wrap180(e2 - e1) / 0.02) / 86400.0
            s_arr[idx] = np.sign(s_arr[idx]) * np.abs(rate)
        new_cons.append((m, s_arr))
    p2, _ = _p_from_constraints(new_cons, fail, cov, y)
    out = p.copy()
    out[idx] = p2[idx]
    return out


# =============================================================== runs of a set

def _row_index(rows):
    return {r["clue_id"]: r for r in rows}


def record_offsets(rows, crux="as_printed") -> dict:
    """{record: day offset}: each row's own day_offset, except that a record whose
    interval row carries a crux fork takes that fork's day_offset (the file's
    convention: the fork governs all rows of the record)."""
    out = {}
    for r in rows:
        out.setdefault(r.get("record"), int(r["day_offset"]))
    for r in rows:
        if r["kind"] != "interval":
            continue
        names = {o["option"]: o for o in r["fork_options"]}
        if crux in names and names[crux].get("operational") and "day_offset" in names[crux]["operational"]:
            out[r.get("record")] = int(names[crux]["operational"]["day_offset"])
    return out


def run_rows(set_ops: dict, reg_set: dict, regime: str, step: str | None = None, overrides: dict | None = None):
    """[(clue_id, option, params)] of the rows a run evaluates (structural,
    none and interval-fork rows dropped), from the regime file."""
    if regime == "SL":
        table = reg_set["regimes"]["SL"][step]
    elif regime == "BM":
        table = reg_set["regimes"]["BM"]
    else:
        raise ValueError(regime)
    entries = {cid: dict(e) for cid, e in table.items()}
    for cid, e in (overrides or {}).items():
        entries[cid] = dict(e)
    out = []
    rows = _row_index(set_ops["rows"])
    for cid, e in entries.items():
        if e["option"] in NOT_EVALUATED:
            continue
        if cid not in rows:
            raise KeyError(f"{cid}: in the regime file but not in the clue file")
        names = {o["option"] for o in rows[cid]["fork_options"]}
        if e["option"] not in names:
            raise KeyError(f"{cid}: option {e['option']} is not one of the row's options (I13(f))")
        out.append((cid, e["option"], e["params"]))
    return out


def f_array(tab: SkyTable, set_ops: dict, reg_set: dict, rows, crux="as_printed", side_only=False,
            thresholds=(P_PASS,) + P_REPORTED, cache=None):
    """For every table day as Day 0: the number of rows failed (at each P_mix
    threshold) and whether every row is covered.  Returns (f: {thr: int array},
    cov: bool array, detail: {clue_id: (offset, p array)})."""
    n = tab.n
    offs = record_offsets(set_ops["rows"], crux)
    rid = _row_index(set_ops["rows"])
    f = {thr: np.zeros(n, dtype=np.int16) for thr in thresholds}
    cov = np.ones(n, dtype=bool)
    detail = {}
    for cid, opt, params in rows:
        pred = reg_set["row_predicates"][cid]
        ck = (cid, opt, json.dumps(params, sort_keys=True), side_only and opt in SAME_APP_OPTIONS)
        if cache is not None and ck in cache:
            p, c, inband = cache[ck]
        else:
            p, c, inband = evaluate_row(tab, opt, params, pred, side_only=side_only)
            if cache is not None:
                cache[ck] = (p, c, inband)
        off = offs[rid[cid].get("record")]
        ps = np.full(n, np.nan)
        cs = np.zeros(n, dtype=bool)
        if 0 <= off < n:
            ps[: n - off] = p[off:]
            cs[: n - off] = c[off:]
        elif -n < off < 0:
            ps[-off:] = p[: n + off]
            cs[-off:] = c[: n + off]
        cov &= cs
        for thr in thresholds:
            with np.errstate(invalid="ignore"):
                f[thr] += ~(ps >= thr)
        detail[cid] = (off, ps, int(inband.sum()))
    return f, cov, detail


# =============================================================== windows

def _rng(purpose: str, key: str):
    return np.random.default_rng(int(_json(SEEDS)["purposes"][purpose]["seeds"][key]))


def window_jdns(a: float) -> np.ndarray:
    """The candidate Day-0 JDNs of the window [a, a + 136 x 365.25)."""
    lo = int(math.ceil(a))
    hi = int(math.ceil(a + W_DAYS))
    return np.arange(lo, hi, dtype=np.int64)


def null_windows(set_id: str, min_off: int, max_off: int, n=N_NULL) -> list[float]:
    """I16(a)'s null windows for a set: starts drawn uniformly so that the window
    lies in windows.json's null_window_range (-1000..+300) and redrawn until
    every row's day lies inside the control envelope (-1999..+300).  Reads no
    truth."""
    w = _json(WINDOWS)["spans"]
    y0, y1 = w["null_window_range"]["years"]
    e0, e1 = w["control_envelope"]["years"]
    lo = C.jd_from_julian(y0, 1, 1) + 0.5
    hi = C.jd_from_julian(y1 + 1, 1, 1) + 0.5
    elo = C.jd_from_julian(e0, 1, 1) + 0.5
    ehi = C.jd_from_julian(e1 + 1, 1, 1) + 0.5
    rng = _rng("null_windows_I16a", set_id)
    out = []
    while len(out) < n:
        a = lo + rng.random() * (hi - lo - W_DAYS)
        if a + min(min_off, 0) >= elo and a + W_DAYS + max(max_off, 0) <= ehi:
            out.append(float(a))
    return out


class _Harness:
    """The only reader of controls_almagest_truth.json (DESIGN 6.3.1, 6.4).
    It places windows and scores; the search never sees what it holds."""

    def __init__(self, path: Path = TRUTH):
        d = _json(path)
        self._day0 = {s["set"]: int(s["day0_civil_jd_noon"]) for s in d["sets"]}
        self.file_sha256 = _sha256(path)

    def gate_window(self, set_id: str) -> float:
        u = _rng("control_window", set_id).random()
        return self._day0[set_id] - u * W_DAYS

    def sensitivity_windows(self, set_id: str, n: int = N_SENS) -> list[float]:
        rng = _rng("control_window_sensitivity", set_id)
        t = self._day0[set_id]
        return [t - rng.random() * W_DAYS for _ in range(n)]

    def score(self, set_id, f, cov, jdn0, a, line=NARROW):
        """6.3.2's scoring of one window from the search's arrays (indexed by
        table day, jdn0 the table's first JDN), with the truth."""
        return score_window(f, cov, jdn0, a, self._day0[set_id], line)

    def truth_offsets(self) -> dict:
        """For slack_table's instant check only."""
        return dict(self._day0)


def _clusters(days: np.ndarray) -> int:
    if len(days) == 0:
        return 0
    return int(1 + np.sum(np.diff(np.sort(days)) > CLUSTER_DAYS))


def score_window(f, cov, jdn0, a, truth_jdn=None, line=NARROW) -> dict:
    """Scoring of one window (6.3.2).  f, cov are indexed by table day (JDN -
    jdn0).  Without truth_jdn only the narrowing is returned (null windows)."""
    days = window_jdns(a)
    n_full = len(days)
    idx = days - jdn0
    inside = (idx >= 0) & (idx < len(f))
    ii = idx[inside]
    c = np.zeros(n_full, dtype=bool)
    c[inside] = cov[ii]
    fv = np.full(n_full, -1, dtype=np.int64)
    fv[inside] = f[ii]
    n_unc = int((~c).sum())
    n_cand = n_full - n_unc
    out = {"window_start_jd": float(a), "n_days": n_full, "n_uncovered": n_unc, "N_cand": n_cand}
    if n_cand == 0:
        out.update({"S0": 0, "B": 0, "min_f": None, "narrow_st": False, "narrow_bf": False})
        if truth_jdn is not None:
            out.update({"truth_covered": False, "seen_st": False, "seen_bf": False, "strict_recall": False})
        return out
    fc = fv[c]
    dc = days[c]
    s0 = int((fc == 0).sum())
    mn = int(fc.min())
    bmask = fc == mn
    b = int(bmask.sum())
    lim = line * n_cand
    out.update({"S0": s0, "B": b, "min_f": mn, "frac_S0": s0 / n_cand, "frac_B": b / n_cand,
                "narrow_st": s0 <= lim, "narrow_bf": b <= lim,
                "clusters_B": _clusters(dc[bmask]), "clusters_S0": _clusters(dc[fc == 0])})
    out["unique_B"] = out["clusters_B"] == 1
    # the uncovered days counted as all failing or all passing
    lim_full = line * n_full
    out["narrow_st_bounds"] = [s0 <= lim_full, s0 + n_unc <= lim_full]
    if truth_jdn is not None:
        k = np.nonzero(days == truth_jdn)[0]
        if len(k) == 0:
            raise ValueError("the truth is not inside its own window")
        k = int(k[0])
        tc = bool(c[k])
        ft = int(fv[k]) if tc else None
        out["truth_covered"] = tc
        out["f_truth"] = ft
        out["strict_recall"] = tc and ft == 0
        out["in_S0"] = tc and ft == 0
        out["in_B"] = tc and ft == mn
        out["rank"] = (1 + int((fc < ft).sum())) if tc else None
        out["ties"] = int((fc == ft).sum()) if tc else None
        out["seen_st"] = out["in_S0"] and out["narrow_st"]
        out["seen_bf"] = out["in_B"] and out["narrow_bf"]
        out["seen_st_bounds"] = [out["in_S0"] and v for v in out["narrow_st_bounds"]]
        out["robust_st"] = len(set(out["seen_st_bounds"])) == 1 and out["seen_st_bounds"][0] == out["seen_st"]
    return out


# =============================================================== the run

def _span_of(starts, min_off, max_off):
    lo = min(int(math.ceil(a)) for a in starts) + min(min_off, 0)
    hi = max(int(math.ceil(a + W_DAYS)) for a in starts) + max(max_off, 0)
    return lo, hi


def _offset_range(set_ops):
    offs = [int(r["day_offset"]) for r in set_ops["rows"]]
    for r in set_ops["rows"]:
        for o in r["fork_options"]:
            op = o.get("operational") or {}
            if isinstance(op, dict) and "day_offset" in op:
                offs.append(int(op["day_offset"]))
    return min(offs), max(offs)


def _runs_for_set(set_ops, reg_set):
    """[(run name, regime, step, overrides, crux, side_only)] for one set: the
    gate's legs (SL x 3 steps, both meanings), regime BM, and the reported
    sensitivities that need no star row."""
    runs = []
    for st in STEPS:
        runs.append((f"SL:{st}", "SL", st, None, "as_printed", False))
        runs.append((f"SL_side:{st}", "SL", st, None, "as_printed", True))
    runs.append(("BM", "BM", None, None, "as_printed", False))
    sens = reg_set.get("sensitivities", {})
    for key in ("projection_rev7", "all_phase_rows", "bounded_primary"):
        if key in sens:
            rows = sens[key]["rows"]
            for st in STEPS:
                runs.append((f"sens:{key}:SL:{st}", "SL", st, {c: v["SL"][st] for c, v in rows.items()},
                             "as_printed", False))
            runs.append((f"sens:{key}:BM", "BM", None, {c: v["BM"] for c, v in rows.items()}, "as_printed", False))
    if "bm_k_1d" in sens:
        runs.append(("sens:bm_k_1d:BM", "BM", None, sens["bm_k_1d"]["rows"], "as_printed", False))
    if "cruxes_emended" in sens:
        for st in STEPS:
            runs.append((f"sens:cruxes_emended:SL:{st}", "SL", st, None, "mean_sun_emended", False))
        runs.append(("sens:cruxes_emended:BM", "BM", None, None, "mean_sun_emended", False))
    return runs


def run(workers=None, null_side=True, sensitivity=True, babylon=True, slack=True, cache=True,
        progress=print, clues_path=CLUES, regimes_path=REGIMES, truth_path=TRUTH, canonical_table=True) -> dict:
    """Gate 3b, Q_BM and their breakdowns (DESIGN 6.4, 9.1, 9.2).

    Returns a dict with, among others:
      seen_ALM_SL       {leg: int}, leg in LEGS ("bf:fine" ... "st:coarse")
      seen_ALM_SL_side  {leg: int}  (the side-only meaning of same_apparition)
      rec_ALM_BM        int;  Q_BM = rec_ALM_BM < 6
      gate_3b           {"fires", "fires_side", "Q_score3b", "Q_attain3b", "lines"}
      narrowable_3b     {leg: {set: bool}};  N_narrow_3b {leg: int}  (null side)
      per_set           {set: {"counted", "runs": {run: scoring of the gate window},
                               "rows": {run: rows and per-row truth flags},
                               "sensitivity_windows": {run: fraction seen}}}
      narrowing         {set: {run: S0 and B fractions in the gate and null windows}}
      slack_table       the observer-slack table recomputed (slack_table())
      deviations, not_built, coverage, inputs
    """
    t0 = time.time()
    say = progress or (lambda *a, **k: None)
    doc = _json(clues_path)
    ops = operational_view(doc)
    reg = _json(regimes_path)
    if reg.get("clue_file_sha256") != _sha256(clues_path):
        raise RuntimeError("almagest_regimes.json was built from a different clue file")
    counted = list(reg["counted_sets"])
    reported = list(reg["reported_sets"])
    needs = canonical_needs(reg)
    harness = _Harness(truth_path)
    # windows: the harness places the gate's and the sensitivity windows; the null windows read no truth
    offr = {sid: _offset_range(ops[sid]) for sid in ops}
    gate = {sid: harness.gate_window(sid) for sid in counted + reported}
    sensw = {sid: harness.sensitivity_windows(sid) for sid in counted + reported} if sensitivity else {}
    nullw = {sid: null_windows(sid, *offr[sid]) for sid in counted} if null_side else {}
    starts = [a for a in gate.values()] + [a for v in sensw.values() for a in v] + [a for v in nullw.values() for a in v]
    lo = min(_span_of([a], *offr[sid])[0] for sid in ops for a in [gate[sid]] + sensw.get(sid, []) + nullw.get(sid, []))
    hi = max(_span_of([a], *offr[sid])[1] for sid in ops for a in [gate[sid]] + sensw.get(sid, []) + nullw.get(sid, []))
    _check_not_target(lo, hi)
    # one canonical table (the null-window range to the end of the data) unless a window reaches outside it,
    # so that a table built from sky data alone is the one every run reads
    c_lo, c_hi = canonical_span() if canonical_table else (lo - 10, hi + 10)
    lo, hi = min(lo - 10, c_lo), max(hi + 10, c_hi)
    _check_not_target(lo, hi)
    say(f"almagest: sky table over JDN {lo}..{hi} ({len(starts)} windows)")
    tab = build_table("alexandria", lo, hi, needs, workers=workers, cache=cache, progress=say)
    tabs = {"alexandria": tab}
    if babylon and "ALM-K" in ops:
        blo, bhi = _span_of([gate["ALM-K"]], *offr["ALM-K"])
        tabs["babylon"] = build_table("babylon", blo - 10, bhi + 10, needs, workers=workers, cache=cache,
                                      progress=say)
    per_set, narrowing = {}, {}
    for sid in counted + reported:
        rs = reg["sets"][sid]
        so = ops[sid]
        res = {"counted": sid in counted, "runs": {}, "rows": {}, "sensitivity_windows": {}, "null": {}}
        rowcache = {}
        site_runs = [("alexandria", r) for r in _runs_for_set(so, rs)]
        if sid == "ALM-K" and "babylon" in tabs:
            site_runs += [("babylon", (f"sens:site_babylon:{name}",) + r[1:])
                          for name, r in [(r[0], r) for r in _runs_for_set(so, rs)] if not name.startswith("sens:")]
        for site_key, (name, regime, step, ovr, crux, side_only) in site_runs:
            tb = tabs[site_key]
            rows = run_rows(so, rs, regime, step, ovr)
            f, cov, detail = f_array(tb, so, rs, rows, crux=crux, side_only=side_only,
                                     cache=rowcache if site_key == "alexandria" else None)
            sc = harness.score(sid, f[P_PASS], cov, tb.jdn0, gate[sid])
            sc["lines"] = {f"{ln:g}": {k: harness.score(sid, f[P_PASS], cov, tb.jdn0, gate[sid], ln)[k]
                                       for k in ("seen_st", "seen_bf")} for ln in LINES if ln != NARROW}
            sc["p_thresholds"] = {f"{thr:g}": {k: harness.score(sid, f[thr], cov, tb.jdn0, gate[sid])[k]
                                               for k in ("seen_st", "seen_bf", "S0", "strict_recall")}
                                  for thr in P_REPORTED}
            res["runs"][name] = sc
            res["rows"][name] = _truth_rows(harness, sid, tb, detail, gate[sid], [(c, o) for c, o, _ in rows])
            if sensitivity and site_key == "alexandria" and sid in sensw and \
                    (name.startswith("SL") or name == "BM"):
                seen = [harness.score(sid, f[P_PASS], cov, tb.jdn0, a) for a in sensw[sid]]
                res["sensitivity_windows"][name] = {
                    "seen_st": float(np.mean([s["seen_st"] for s in seen])),
                    "seen_bf": float(np.mean([s["seen_bf"] for s in seen])),
                    "n_with_uncovered_days": int(sum(s["n_uncovered"] > 0 for s in seen))}
            if null_side and sid in nullw and site_key == "alexandria" and (name.startswith("SL") or name == "BM"):
                nl = [score_window(f[P_PASS], cov, tb.jdn0, a) for a in nullw[sid]]
                res["null"][name] = {
                    "n_narrow_st": int(sum(s["narrow_st"] for s in nl)),
                    "n_narrow_bf": int(sum(s["narrow_bf"] for s in nl)),
                    # the strict count with the uncovered days counted as all failing / all passing
                    "n_narrow_st_bounds": [int(sum(s.get("narrow_st_bounds", [False, False])[i] for s in nl))
                                           for i in (0, 1)],
                    "frac_S0": [s.get("frac_S0") for s in nl],
                    "frac_B": [s.get("frac_B") for s in nl],
                    "n_uncovered": [s["n_uncovered"] for s in nl]}
        per_set[sid] = res
        narrowing[sid] = {name: {"gate_frac_S0": sc.get("frac_S0"), "gate_frac_B": sc.get("frac_B"),
                                 "null_median_frac_S0": (float(np.median([x for x in res["null"][name]["frac_S0"]
                                                                          if x is not None]))
                                                         if name in res["null"] else None)}
                          for name, sc in res["runs"].items() if name.startswith("SL") or name == "BM"}
        say(f"almagest: {sid} done ({time.time() - t0:.0f} s)")
    out = aggregate(per_set, counted, null_side)
    out["per_set"] = per_set
    out["narrowing"] = narrowing
    out["windows"] = {sid: {"gate_start_jd": gate[sid], "n_sensitivity": len(sensw.get(sid, [])),
                            "n_null": len(nullw.get(sid, [])),
                            "null_starts_jd": nullw.get(sid, [])} for sid in counted + reported}
    out["coverage"] = {"ephemeris_days": ephemeris_days(), "table": {k: [t.jdn0, t.jdn0 + t.n - 1]
                                                                      for k, t in tabs.items()},
                       "events_tt": {k: [t.ev_lo, t.ev_hi] for k, t in tabs.items()}}
    out["inputs"] = {"clue_file_sha256": _sha256(clues_path), "regimes_sha256": _sha256(regimes_path),
                     "truth_sha256": harness.file_sha256, "code_version": _CODE_VERSION}
    out["deviations"] = DEVIATIONS
    out["not_built"] = NOT_BUILT
    if slack:
        try:
            out["slack_table"] = slack_table(reg)
        except Exception as exc:                          # reported, never silently dropped
            out["slack_table"] = {"error": repr(exc)}
    out["elapsed_s"] = round(time.time() - t0, 1)
    return out


def _check_not_target(lo, hi):
    from odybench.lean import TARGET_JDN, TargetMasked
    if lo <= TARGET_JDN <= hi:
        raise TargetMasked("the Almagest control's sky span contains 16 Apr -1177")


def _truth_rows(harness, sid, tab, detail, a, rows):
    """The rows the truth fails, with each row's P_mix at the truth (scoring side)."""
    t = harness._day0[sid]
    j = t - tab.jdn0
    out = {}
    for cid, opt in rows:
        off, ps, nband = detail[cid]
        p = float(ps[j]) if 0 <= j < len(ps) and np.isfinite(ps[j]) else None
        out[cid] = {"option": opt, "p_truth": p, "fails": (p is not None and p < P_PASS), "n_inband_days": nband}
    return out


def aggregate(per_set, counted, null_side=True) -> dict:
    """The named quantities of 9.1 from the per-set scorings."""
    seen = {leg: 0 for leg in LEGS}
    seen_side = {leg: 0 for leg in LEGS}
    for sid in counted:
        r = per_set[sid]["runs"]
        for leg in LEGS:
            sc, st = leg.split(":")
            seen[leg] += int(r[f"SL:{st}"][f"seen_{sc}"])
            seen_side[leg] += int(r[f"SL_side:{st}"][f"seen_{sc}"])
    rec = sum(int(per_set[sid]["runs"]["BM"]["strict_recall"] and per_set[sid]["runs"]["BM"]["narrow_st"])
              for sid in counted)
    fires = min(seen.values()) < GATE_MIN
    fires_side = min(seen_side.values()) < GATE_MIN
    q_score = (fires and max(seen.values()) >= GATE_MIN) or (fires_side != fires)
    lines = {}
    for ln in LINES:
        if ln == NARROW:
            continue
        cnt = {leg: sum(int(per_set[sid]["runs"][f"SL:{leg.split(':')[1]}"]["lines"][f"{ln:g}"][
            f"seen_{leg.split(':')[0]}"]) for sid in counted) for leg in LEGS}
        lines[f"{ln:g}"] = {"seen_ALM_SL": cnt, "fires": min(cnt.values()) < GATE_MIN}
    out = {"gate3b_run": True, "seen_ALM_SL": seen, "seen_ALM_SL_side": seen_side, "rec_ALM_BM": rec,
           "Q_BM": rec < GATE_MIN,
           "gate_3b": {"fires": fires, "fires_side": fires_side, "Q_score3b": bool(q_score), "lines": lines}}
    out["strict_recall_SL"] = {st: sum(int(per_set[sid]["runs"][f"SL:{st}"]["strict_recall"]) for sid in counted)
                               for st in STEPS}
    out["strict_recall_BM"] = sum(int(per_set[sid]["runs"]["BM"]["strict_recall"]) for sid in counted)
    out["robust"] = {"all_seen_flags_robust_to_uncovered_days": all(
        per_set[sid]["runs"][f"SL:{st}"].get("robust_st", True) for sid in counted for st in STEPS)}
    if null_side:
        narrow = {leg: {} for leg in LEGS}
        for sid in counted:
            nl = per_set[sid]["null"]
            for leg in LEGS:
                sc, st = leg.split(":")
                narrow[leg][sid] = nl[f"SL:{st}"][f"n_narrow_{sc}"] >= NARROW_MAJORITY
        nn = {leg: sum(v.values()) for leg, v in narrow.items()}
        # strict legs: does a set's narrowability change if the uncovered days all fail or all pass?
        out["narrowable_st_not_robust"] = sorted(
            {f"{sid}:{st}" for sid in counted for st in STEPS
             if len({b >= NARROW_MAJORITY for b in per_set[sid]["null"][f"SL:{st}"].get("n_narrow_st_bounds", [])}
                    | {narrow[f"st:{st}"][sid]}) > 1})
        out["narrowable_3b"] = narrow
        out["N_narrow_3b"] = nn
        out["gate_3b"]["Q_attain3b"] = bool(fires and min(nn.values()) < GATE_MIN)
        out["seen_among_narrowable"] = {leg: sum(int(per_set[sid]["runs"][f"SL:{leg.split(':')[1]}"][
            f"seen_{leg.split(':')[0]}"]) for sid in counted if narrow[leg][sid]) for leg in LEGS}
    return out


# =============================================================== the observer-slack table

def _parse_ge_summary(text: str) -> tuple[dict, dict]:
    """({body: [record ids]}, {crux record: 'emended' | 'printed'}) from the
    note's Summary (its 'sorted:' lines and the readings it names), read as
    tools/build_regimes.py reads it."""
    import re
    i = text.index("**Summary: |record")
    block = text[i:i + 4000]
    out, cruxes = {}, {}
    for m in re.finditer(r"^- (\w+) \(n = (\d+); ([^)]*)\):.*?\n(?:  - .*\n)*?  - sorted: ([^\n]+)", block, re.M):
        ids = [t.strip().split()[0] for t in m.group(4).split(",") if t.strip()]
        if len(ids) != int(m.group(2)):
            raise ValueError(f"summary for {m.group(1)}: n = {m.group(2)} but {len(ids)} records")
        out[m.group(1)] = ids
        for part in m.group(3).split(","):
            pm = re.match(r"\s*([IVX]+\.[\w.]+) (?:at its (emended) date|as (printed))", part)
            if pm:
                cruxes[pm.group(1)] = pm.group(2) or pm.group(3)
    return out, cruxes


def _mean_sun(jd_tt):
    """Meeus (1998) eq. 25.2: geometric mean longitude of the Sun, mean equinox of date (deg)."""
    T = (np.asarray(jd_tt, dtype=float) - 2451545.0) / 36525.0
    return (280.46646 + 36000.76983 * T + 0.0003032 * T * T) % 360.0


def _planet_lon(body, jd_tt):
    return _geo_unit_lon((body,), _time_tt(jd_tt))[body][1]


def _nearest_extreme(func, t_obs, sgn, span=100.0):
    """Nearest local maximum of sgn*func (with sgn*func > 0) to t_obs; refined."""
    g = t_obs + np.arange(-span, span + 0.5, 1.0)
    v = sgn * np.asarray(func(g))
    i = np.nonzero((v[1:-1] >= v[:-2]) & (v[1:-1] >= v[2:]) & (v[1:-1] > 0.0))[0] + 1
    if len(i) == 0:
        return None, None
    k = i[np.argmin(np.abs(g[i] - t_obs))]
    tg = float(_refine_max(lambda x: sgn * np.asarray(func(x)), np.array([g[k]]))[0])
    return tg, float(np.asarray(func(np.array([tg])))[0])


def _zero_nearest(func, t_obs, span=40.0):
    g = t_obs + np.arange(-span, span + 0.5, 1.0)
    v = np.asarray(func(g))
    i = np.nonzero((np.sign(v[:-1]) != np.sign(v[1:])) & (np.abs(v[:-1] - v[1:]) < 30.0))[0]
    if len(i) == 0:
        return None
    k = i[np.argmin(np.abs(g[i] - t_obs))]
    s = 1.0 if v[k] < 0 else -1.0
    return float(_bisect_cross(lambda x: s * np.asarray(func(x)), np.array([g[k]]), np.array([g[k + 1]]))[0])


def slack_row(rec: dict, lat: float, lon: float) -> dict:
    """The bench's quantities for one record at its (truth-side) instant: the
    columns of the note's Tables 2, 3, 5 and 6 that need no star."""
    body = rec["body"]
    jd_ut = float(rec["jd_ut"])
    y = float(_epoch_of_jd(jd_ut))
    jd_tt = jd_ut + float(dt_ref(y)) / 86400.0
    out = {"id": rec["id"], "reading": rec["reading"], "body": body}
    if body in ("mercury", "venus"):
        sgn = 1.0 if rec.get("rs_kind") == "set lag" else -1.0      # the record's stated side
        se = lambda x: _signed_elong_dlon(body, np.asarray(x, dtype=float))[0]
        out["elong_true"] = float(se(np.array([jd_tt]))[0])
        tg, val = _nearest_extreme(se, jd_tt, sgn)
        out["ge_true_val"] = val
        out["off_ge_true_d"] = None if tg is None else jd_tt - tg
        me = lambda x: _wrap180(_planet_lon(body, np.asarray(x, dtype=float)) - _mean_sun(x))
        tm, _ = _nearest_extreme(me, jd_tt, sgn)
        out["off_ge_mean_d"] = None if tm is None else jd_tt - tm
        jdn = int(math.floor(jd_ut + 0.5 + lon / 360.0))
        m0 = jdn - 0.5 - lon / 360.0
        if sgn < 0:
            sr = _crossing("sun", np.array([m0 + 0.25]), H0_SUN, True, lat, lon)
            br = _crossing(body, sr, H0_PLANET, True, lat, lon)
            out["rs_kind"], out["rs_min"] = "rise lead", float(((sr - br) * 1440.0)[0])
        else:
            ss = _crossing("sun", np.array([m0 + 0.75]), H0_SUN, False, lat, lon)
            bs = _crossing(body, ss, H0_PLANET, False, lat, lon)
            out["rs_kind"], out["rs_min"] = "set lag", float(((bs - ss) * 1440.0)[0])
        if body == "mercury":
            out.update(_horizon_az_offsets(jdn, lat, lon, rising=sgn < 0))
    if body in ("mars", "jupiter", "saturn"):
        f_true = lambda x: _wrap180(_planet_lon(body, np.asarray(x)) - _sun_lon(np.asarray(x)) - 180.0)
        f_mean = lambda x: _wrap180(_planet_lon(body, np.asarray(x)) - _mean_sun(x) - 180.0)
        o1, o2 = _zero_nearest(f_true, jd_tt), _zero_nearest(f_mean, jd_tt)
        out["off_opp_true_d"] = None if o1 is None else jd_tt - o1
        out["off_opp_mean_d"] = None if o2 is None else jd_tt - o2
    if body == "sun":
        q = _zero_nearest(lambda x: _wrap180(_sun_lon(np.asarray(x))), jd_tt, span=200.0)
        out["equinox_off_d"] = None if q is None else jd_tt - q
    if body == "moon":
        t = _time_ut(np.array([jd_ut]))
        a_m = E.apparent("moon", t, lat, lon)
        a_s = E.apparent("sun", t, lat, lon)
        eps = E.mean_obliquity(t.tt) + t._nutation_angles_radians[1]
        lam = []
        for a in (a_m, a_s):
            x, yy, z = np.einsum("ij...,j...->i...", t.M, a.xyz.au)
            lam.append(np.degrees(np.arctan2(yy * np.cos(eps) + z * np.sin(eps), x)))
        out["moon_minus_sun_topo"] = float(_wrap180(lam[0] - lam[1])[0])
    return out


def _horizon_az_offsets(jdn, lat, lon, rising=True, span=45):
    """Record day minus the 3-point vertex of the nearest local max and min of
    Mercury's daily horizon azimuth (rising for morning, setting for evening),
    as in the note; and the bench's 7-point MWRA_vtx offset for mornings."""
    days = np.arange(jdn - span, jdn + span + 1)
    m0 = days - 0.5 - lon / 360.0
    if rising:
        sr = _crossing("sun", m0 + 0.25, H0_SUN, True, lat, lon)
        tb = _crossing("mercury", sr, H0_PLANET, True, lat, lon)
    else:
        ss = _crossing("sun", m0 + 0.75, H0_SUN, False, lat, lon)
        tb = _crossing("mercury", ss, H0_PLANET, False, lat, lon)
    az = _altaz("mercury", tb, lat, lon)[1]
    k = days - jdn
    res = {}
    for kind, sg in (("max", 1.0), ("min", -1.0)):
        v = sg * az
        i = np.nonzero((v[1:-1] >= v[:-2]) & (v[1:-1] >= v[2:]))[0] + 1
        if len(i) == 0:
            res[f"az_{kind}_off_d"] = None
            continue
        x = []
        for j in i:
            y0, y1, y2 = az[j - 1], az[j], az[j + 1]
            den = y0 - 2 * y1 + y2
            x.append(k[j] + (0.0 if den == 0 else 0.5 * (y0 - y2) / den))
        x = np.array(x)
        res[f"az_{kind}_off_d"] = float(-x[np.argmin(np.abs(x))])
    if rising:
        mw = _mwra_columns(az, tb)
        res["mwra_vtx_off_d"] = float(tb[span] - mw["vertex_ut"][span])
    return res


def _ceil_step(x, step):
    k = math.ceil(round(x / step, 9))
    nd = max(0, -int(math.floor(math.log10(step))) + 1)
    return round(k * step, nd)


def slack_table(reg: dict) -> dict:
    """The drafter's observer-slack table recomputed with this module's sky code
    (truth-side: it reads the record instants of results/controls-almagest/
    slack.json), with the greatest-elongation summary, the leave-one-set-out
    ceilings they imply, and their comparison with almagest_regimes.json."""
    recs = _json(SLACK_TRUTH)
    summary, cruxes = _parse_ge_summary(SLACK_NOTE.read_text(encoding="utf-8"))
    sites_ = {"Alexandria": site("alexandria"), "Babylon (assumed)": site("babylon")}
    rows = []
    for r in recs:
        lat, lon = sites_.get(r.get("site"), sites_["Alexandria"])
        b = slack_row(r, lat, lon)
        cmp = {}
        for k in ("off_ge_true_d", "off_ge_mean_d", "rs_min", "az_max_off_d", "az_min_off_d", "off_opp_mean_d"):
            if b.get(k) is not None and r.get(k) is not None:
                cmp[k] = b[k] - float(r[k])
        b["minus_drafter"] = cmp
        rows.append(b)
    # one row per record, at the reading the note's summary uses (the crux at its emended date for IX.7.11)
    by_id = {}
    for b in rows:
        want = cruxes.get(b["id"], "printed")
        if b["reading"].startswith(want):
            by_id[b["id"]] = b
    ge = {body: {rid: abs(by_id[rid]["off_ge_true_d"]) for rid in ids} for body, ids in summary.items()}
    ceilings, agree = {}, True
    for sid, s in reg["sets"].items():
        inset = set(_json(CLUES)["sets"][[x["set"] for x in _json(CLUES)["sets"]].index(sid)]["records"])
        ceilings[sid] = {}
        for body, vals in ge.items():
            outside = {k: v for k, v in vals.items() if k not in inset}
            mx = max(outside.values())
            c = {st: _ceil_step(mx, {"fine": 0.1, "mid": 0.5, "coarse": 1.0}[st]) for st in STEPS}
            reg_c = s["tolerances"]["greatest_elongation_days"].get(body)
            ceilings[sid][body] = {"bench": c, "regime_file": reg_c,
                                   "same": reg_c is None or all(reg_c[st] == c[st] for st in STEPS)}
            agree &= ceilings[sid][body]["same"]
    diffs = {}
    for k in ("off_ge_true_d", "off_ge_mean_d", "rs_min", "az_max_off_d", "az_min_off_d", "off_opp_mean_d"):
        v = [abs(b["minus_drafter"][k]) for b in rows if k in b["minus_drafter"]]
        diffs[k] = {"n": len(v), "max_abs": max(v) if v else None}
    return {"rows": rows, "ge_summary_abs_days": ge, "ceilings": ceilings,
            "ceilings_agree_with_regime_file": bool(agree), "bench_minus_drafter": diffs,
            "note": "truth-side: measured at the records' true instants (DESIGN AppT 1-2)"}


# =============================================================== recorded decisions

DEVIATIONS = [
    "Ephemeris coverage: the DE441 excerpt ends at +241 Jan 1 and DESIGN 11.1's +241..+300 extension has not been "
    "fetched. Candidates whose rows need sky past the data are left out of N_cand, S0 and B (neither passed nor "
    "failed); each window reports n_uncovered, and the strict seen flag with those days counted as all failing and "
    "as all passing ('robust_st'). The truths themselves lie inside the data (checked at scoring: truth_covered).",
    "truth_index.json and tools/build_truth_index.py do not exist yet (A6, deferred); the harness reads "
    "controls_almagest_truth.json directly, inside _Harness only, and only day0_civil_jd_noon.",
    "Body, side and instant of each row are read off the statements by tools/build_regimes.py (fixed rules, recorded "
    "in almagest_regimes.json 'row_predicates'), because operational_map.json (10.3) does not exist; the search reads "
    "operational fields and the regime file only.",
    "J.4's 'twelfth hour of the night' is evaluated at the middle of that seasonal hour; its projected options "
    "(same_apparition, bm_venus_lead) depend on the instant only through the bracketing conjunctions and the order of "
    "the greatest elongation, at day scale.",
    "Delta-T: the sky is computed once at the mixture mean; each row's P_mix is exact for its linear dependence on "
    "Delta-T (time offsets exactly; rise leads, altitudes and the Moon's elongation by finite-difference slopes, "
    "measured for every in-band day; the MWRA offset by the linearisation d(Delta)/d(Delta-T) = 1). All four models "
    "are put in the n-dot -25.82 frame for every row.",
    "The phase class of B.7 reads the geocentric apparent elongation (lambda_moon - lambda_sun) at the stated hour; "
    "the drafter's Table 5 is topocentric.",
]

NOT_BUILT = [
    "held_ALM and Q_H (the held-out rows: star positions, planet-Moon and Sun-Moon relations, the opposition): "
    "deferred with Q_H, which LEAN.md does not list among the lean run's qualifiers.",
    "The full primary run and the held-out list-value sensitivity (both need the star rows).",
    "6.3.2's 'each row moved to each alternative' and the fraction of fork readings making the truth unique.",
    "I16 (the independent second implementation of the control search) is A7's and not part of the lean run.",
]


# =============================================================== synthetic selftest

def _synthetic_table(n=4000, jdn0=1500000, seed=1):
    """A SkyTable with synthetic columns and events (no ephemeris), for logic tests."""
    rng = np.random.default_rng(seed)
    jdn = np.arange(jdn0, jdn0 + n, dtype=np.int64)
    m0 = jdn - 0.5
    cols = {"jdn": jdn, "sun_rise": m0 + 0.25, "sun_set": m0 + 0.75, "dawn8": m0 + 0.22, "dusk8": m0 + 0.78,
            "lat:19.5": m0 + 19.5 / 24, "lat:4.75": m0 + 4.75 / 24, "lat:13": m0 + 13 / 24, "lat:6.75": m0 + 6.75 / 24,
            "lat:5": m0 + 5 / 24}
    ph = np.arange(n) * 2 * np.pi / 116.0
    cols["mercury:lead"] = -60.0 * np.sin(ph)          # morning-visible in the west apparition (58..116)
    cols["mercury:lag"] = 60.0 * np.sin(ph)            # evening-visible in the east apparition (0..58)
    cols["mercury:rise"] = cols["sun_rise"] - cols["mercury:lead"] / 1440.0
    cols["mercury:rise_az"] = 100.0 + 10.0 * np.sin(np.arange(n) * 2 * np.pi / 90.0)
    ph2 = np.arange(n) * 2 * np.pi / 584.0
    cols["venus:lead"] = -200.0 * np.sin(ph2)
    cols["venus:lag"] = 200.0 * np.sin(ph2)
    cols["venus:rise"] = cols["sun_rise"] - cols["venus:lead"] / 1440.0
    cols["alt:jupiter@lat:5"] = 20.0 * np.sin(np.arange(n) * 2 * np.pi / 399.0)
    cols["moonE@lat:6.75"] = (np.arange(n) * 360.0 / 29.53) % 360.0
    t = jdn0 - 0.5 + np.arange(-500, n + 500)
    events = {"ge:mercury:east": jdn0 + 29.0 + 116.0 * np.arange(-5, n // 116 + 5) + 0.3,
              "ge:mercury:west": jdn0 + 87.0 + 116.0 * np.arange(-5, n // 116 + 5) + 0.3,
              "conj:mercury": np.sort(np.concatenate([jdn0 + 0.0 + 116.0 * np.arange(-5, n // 116 + 5),
                                                      jdn0 + 58.0 + 116.0 * np.arange(-5, n // 116 + 5)])),
              "ge:venus:east": jdn0 + 146.0 + 584.0 * np.arange(-2, n // 584 + 2),
              "ge:venus:west": jdn0 + 438.0 + 584.0 * np.arange(-2, n // 584 + 2),
              "conj:venus": np.sort(np.concatenate([jdn0 + 584.0 * np.arange(-2, n // 584 + 2),
                                                    jdn0 + 292.0 + 584.0 * np.arange(-2, n // 584 + 2)])),
              "equinox": jdn0 + 80.25 + 365.2422 * np.arange(-2, n // 365 + 2)}
    del t, rng
    needs = {"lat_hours": [19.5, 4.75, 13, 6.75, 5], "horizon_bodies": ["mercury", "venus"],
             "rise_az_bodies": ["mercury"], "alts": [["jupiter", "lat:5"]], "moon_keys": ["lat:6.75"]}
    return SkyTable("synthetic", 31.2, 0.0, jdn0, cols, events, jdn0 - 400.0, jdn0 + n + 400.0, needs)


def selftest(verbose=True, real_sky=True) -> bool:
    """Synthetic checks: the scoring of 6.3.2, the windows, the Delta-T
    integral, the row predicates on a synthetic sky, and (real_sky) a synthetic
    set built from the real sky far from any control truth, recovered by the
    search and cross-checked against brute-force ephem scans."""
    ok = True

    def chk(c, msg):
        nonlocal ok
        if not c:
            ok = False
            print("SELFTEST FAIL:", msg)
        elif verbose:
            print("  ok:", msg)

    # --- scoring (6.3.2)
    f = np.array([3, 0, 0, 1, 2, 1, 1, 2, 2, 0] + [2] * 90, dtype=np.int16)
    sc = score_window(np.concatenate([f, np.full(49674, 2, dtype=np.int16)]), np.ones(49774, dtype=bool), 1000,
                      1000.5, truth_jdn=1002)
    chk(sc["N_cand"] == 49674 and sc["S0"] == 3 and sc["seen_st"] and sc["seen_bf"] and sc["strict_recall"],
        "strict survivors, seen, recall")
    chk(sc["clusters_S0"] == 2 and sc["clusters_B"] == 2 and sc["rank"] == 1, "clusters and rank")
    g = np.full(49800, 1, dtype=np.int16)
    g[10] = 0
    sc = score_window(g, np.ones(49800, dtype=bool), 0, 0.0, truth_jdn=11)
    chk(not sc["strict_recall"] and sc["in_B"] is False and sc["B"] == 1, "truth outside B")
    g = np.full(49800, 1, dtype=np.int16)
    sc = score_window(g, np.ones(49800, dtype=bool), 0, 0.0, truth_jdn=11)
    chk(sc["S0"] == 0 and sc["B"] == 49674 and not sc["seen_bf"], "best fit = everything when S0 is empty")
    cv = np.ones(49800, dtype=bool)
    cv[40000:] = False
    g = np.full(49800, 1, dtype=np.int16)
    g[5:400] = 0
    sc = score_window(g, cv, 0, 0.0, truth_jdn=11)
    chk(sc["n_uncovered"] == 49674 - 40000 and sc["N_cand"] == 40000 and sc["S0"] == 395
        and sc["seen_st"] and sc["robust_st"] is False, "uncovered days left out; robustness flag")
    chk(len(window_jdns(0.2)) == 49674 and len(window_jdns(0.0)) == 49674, "136 x 365.25 days per window")
    # --- Delta-T mixture
    y = np.array([150.0])
    mu, sg = dt_models(y)
    p_all = p_mix_interval(y, np.array([-1e9]), np.array([1e9]))
    chk(abs(float(p_all[0]) - 1.0) < 1e-12, "mixture integrates to 1")
    ref = dt_ref(y)
    half = p_mix_interval(y, np.array([-1e9]), ref)
    chk(0.2 < float(half[0]) < 0.8, "half the mass below the mean (roughly)")
    m = np.array([0.5 / 86400.0 * 1000.0, -5.0, 5.0])     # margins in days -> constraint k - off
    p, inb = _p_from_constraints([(np.array([0.001, -1.0, 1.0]), 1 / 86400.0)], np.zeros(3, dtype=bool),
                                 np.ones(3, dtype=bool), np.array([150.0, 150.0, 150.0]))
    del m
    chk(p[1] == 0.0 and p[2] == 1.0 and 0.0 < p[0] < 1.0 and inb[0] and not inb[1], "band rows integrated exactly")
    exp = float(p_mix_interval(np.array([150.0]), ref - 0.001 * 86400.0, np.array([np.inf]))[0])
    chk(abs(p[0] - exp) < 1e-12, "P_mix of a time-offset row equals the mixture mass")
    # --- predicates on a synthetic sky
    tab = _synthetic_table()
    pred_ev = {"body": "mercury", "side": "evening", "instant": {"kind": "sun_alt", "deg": -8.0, "part": "evening"}}
    p, c, inb = evaluate_row(tab, "ge_true_k", {"k_days": 1.5}, pred_ev)
    t_tt = tab.cols["dusk8"] + dt_ref(tab.epoch) / 86400.0
    near = np.abs(t_tt - _nearest_event(tab.events["ge:mercury:east"], t_tt)[0]) <= 1.5
    chk(c.sum() > 3000 and np.array_equal((p >= 0.5)[c & ~inb], near[c & ~inb]), "ge_true_k: |instant - GE| <= k")
    p, c, inb = evaluate_row(tab, "visible_only", {"min_minutes_between_body_and_sun_horizon_crossings": 30}, pred_ev)
    chk(np.array_equal((p >= 0.5)[c & ~inb], (tab.cols["mercury:lag"] >= 30.0)[c & ~inb]),
        "visible_only reads the set lag")
    pred_mo = {"body": "venus", "side": "morning", "instant": {"kind": "lat", "hours": 4.75}}
    p, c, _ = evaluate_row(tab, "ge_before_same_apparition", {"bound": "same_apparition", "visible_min_minutes": 30.0},
                           pred_mo)
    jj = np.nonzero((p >= 0.5) & c)[0]
    t_ok = True
    for j in jj[:: max(1, len(jj) // 50)]:
        t = tab.cols["lat:4.75"][j] + float(dt_ref(tab.epoch[j])) / 86400
        conj = tab.events["conj:venus"]
        cp, cn = conj[conj <= t].max(), conj[conj > t].min()
        gw = tab.events["ge:venus:west"]
        gin = gw[(gw > cp) & (gw < cn)]
        t_ok &= len(gin) == 1 and gin[0] < t and tab.cols["venus:lead"][j] >= 30.0
    chk(len(jj) > 0 and t_ok, "same_apparition: west GE already past inside the bracketing conjunctions, visible")
    p2, c2, _ = evaluate_row(tab, "ge_before_same_apparition", {"bound": "same_apparition", "visible_min_minutes": 30.0},
                             pred_mo, side_only=True)
    chk(np.all((p2 >= 0.5) | ~(p >= 0.5)), "the side-only meaning is never stricter")
    pred_q = {"body": "moon", "side": None, "instant": {"kind": "lat", "hours": 6.75}}
    p, c, inb = evaluate_row(tab, "phase_class", {"class": "last_quarter", "tolerance_days": 2}, pred_q)
    E_ = tab.cols["moonE@lat:6.75"]
    chk(np.array_equal((p >= 0.5)[c & ~inb], (np.abs(E_ - 270.0) <= 24.4)[c & ~inb]),
        "phase class last quarter, 12.2 deg per day")
    pred_s = {"body": "sun", "side": None, "instant": {"kind": "lat", "hours": 13.0}}
    p, c, _ = evaluate_row(tab, "equinox_tol", {"tolerance_days": 1}, pred_s)
    chk(int(((p >= 0.5) & c).sum()) >= 2 * 9, "equinox_tol passes about two days a year")
    pred_m = {"body": "mercury", "side": "morning", "instant": {"kind": "sun_alt", "deg": -8.0, "part": "morning"}}
    p, c, _ = evaluate_row(tab, "bm_mwra_k", {"k_days": 1.5}, pred_m)
    chk(((p >= 0.5) & c).sum() > 0, "MWRA proxy passes near the azimuth maxima")
    # --- the null windows read no truth and respect their ranges
    nw = null_windows("ALM-K", 0, 2902)
    w = _json(WINDOWS)["spans"]
    chk(len(nw) == 21 and all(a >= C.jd_from_julian(w["null_window_range"]["years"][0], 1, 1) for a in nw)
        and all(a + W_DAYS + 2902 <= C.jd_from_julian(301, 1, 1) + 0.5 for a in nw), "null windows inside the ranges")
    chk(null_windows("ALM-K", 0, 2902) == nw, "null windows reproducible from the seed")
    # --- operational view drops prose
    ov = operational_view(_json(CLUES))
    keys = {k for s in ov.values() for r in s["rows"] for k in r}
    chk(keys <= set(ROW_KEYS) and "statement" not in keys, "operational view: no statement, licence or ref")
    if real_sky:
        ok &= _selftest_real_sky(chk, verbose)
    if verbose:
        print("almagest selftest:", "PASS" if ok else "FAIL")
    return ok


def _selftest_real_sky(chk, verbose) -> bool:
    """A synthetic set built from the real sky in -850 (no control truth lies
    before -500), searched in a short window; and brute-force checks of the
    table's rise leads, LAT instants and greatest elongations."""
    lat, lon = site("alexandria")
    j0 = int(C.jdn_from_julian(-852, 1, 1))
    needs = {"lat_hours": [19.5, 4.75], "horizon_bodies": ["mercury", "venus"], "rise_az_bodies": ["mercury"],
             "alts": [["jupiter", "sun-8:morning"]], "moon_keys": ["lat:4.75"]}
    tab = build_table("alexandria", j0, j0 + 3 * 366, needs, workers=1, cache=False, chunk=400, ev_margin=420)
    ok0 = True
    # brute force: Venus rise lead on three days by an altitude scan with ephem.altaz
    from scipy.optimize import brentq
    for j in (100, 500, 900):
        d = tab.cols["jdn"][j]
        m0 = d - 0.5 - lon / 360.0

        def first_cross(body, h0, a, b):
            g = np.linspace(a, b, 721)
            al = np.asarray(E.altaz(body, g, lat, lon, dt=dt_ref)[0]) - h0
            i = np.nonzero((al[:-1] < 0) & (al[1:] >= 0))[0][0]
            return brentq(lambda x: float(E.altaz(body, x, lat, lon, dt=dt_ref)[0]) - h0, g[i], g[i + 1], xtol=1e-9)
        sr = first_cross("sun", H0_SUN, m0, m0 + 0.5)
        vr = first_cross("venus", H0_PLANET, m0, m0 + 0.5)
        lead = (sr - vr) * 1440.0
        chk(abs(lead - tab.cols["venus:lead"][j]) < 0.01, f"Venus rise lead day {j}: {lead:.3f} min (brute force)")
        lat_h = float(E.local_apparent_solar_time(tab.cols["lat:19.5"][j], lat, lon, dt=dt_ref))
        chk(abs(lat_h - 19.5) < 1e-5, "LAT 19:30 instant")
        a8 = float(E.altaz("sun", tab.cols["dawn8"][j], lat, lon, dt=dt_ref)[0])
        chk(abs(a8 + 8.0) < 1e-5, "dawn: the Sun at -8 deg")
    # brute force: one greatest eastern elongation of Mercury by a fine scan of ephem.elongation
    ge = tab.events["ge:mercury:east"]
    g0 = ge[(ge > tab.jdn0 + 200) & (ge < tab.jdn0 + 900)][0]
    grid = g0 + np.linspace(-1.0, 1.0, 2001)
    dtv = float(dt_ref(_epoch_of_jd(g0)))
    el = np.asarray(E.elongation("mercury", grid - dtv / 86400.0, dt=dt_ref))
    gb = grid[np.argmax(el)]
    chk(abs(gb - g0) < 0.002, f"Mercury greatest elongation {g0:.4f} vs scan {gb:.4f} TT")
    # a synthetic set from the real sky: Day 0 = the civil day of that GE (evening), and a Venus
    # morning-visibility row on the first later day with a lead of 60 min or more
    d0 = int(math.floor(g0 - dtv / 86400.0 + 0.5 + lon / 360.0))
    i0 = d0 - tab.jdn0
    later = np.nonzero(tab.cols["venus:lead"][i0 + 10:] >= 60.0)[0]
    off2 = int(later[0]) + 10 if len(later) else 20
    ops = {"set": "SYN-1", "rows": [
        {"clue_id": "SYN-1.1", "set": "SYN-1", "kind": "planet", "record": "R1", "day_offset": 0,
         "fork_options": [{"option": "ge_true_k", "primary": True, "operational": {"k_days": [1, 2]}}]},
        {"clue_id": "SYN-1.2", "set": "SYN-1", "kind": "interval", "record": "R2", "day_offset": off2,
         "fork_options": []},
        {"clue_id": "SYN-1.3", "set": "SYN-1", "kind": "planet", "record": "R2", "day_offset": off2,
         "fork_options": [{"option": "visible_only", "primary": True,
                           "operational": {"min_minutes_between_body_and_sun_horizon_crossings": [30, 60]}}]}]}
    reg_set = {"regimes": {"SL": {"coarse": {"SYN-1.1": {"option": "ge_true_k", "params": {"k_days": 1.5}},
                                             "SYN-1.2": {"option": "structural", "params": {}},
                                             "SYN-1.3": {"option": "visible_only", "params": {
                                                 "min_minutes_between_body_and_sun_horizon_crossings": 30}}}}},
               "row_predicates": {
                   "SYN-1.1": {"body": "mercury", "side": "evening",
                               "instant": {"kind": "sun_alt", "deg": -8.0, "part": "evening"}},
                   "SYN-1.3": {"body": "venus", "side": "morning",
                               "instant": {"kind": "sun_alt", "deg": -8.0, "part": "morning"}}}}
    rows = run_rows(ops, reg_set, "SL", "coarse")
    f, cov, _ = f_array(tab, ops, reg_set, rows)
    fz = f[P_PASS]
    chk(cov[i0] and fz[i0] == 0, "the synthetic truth passes every row (strict recall)")
    n_ok = int(((fz == 0) & cov).sum())
    chk(0 < n_ok < 0.2 * cov.sum(), f"the synthetic set narrows its span ({n_ok} of {int(cov.sum())} days)")
    return ok0


if __name__ == "__main__":
    import sys
    sys.exit(0 if selftest() else 1)
