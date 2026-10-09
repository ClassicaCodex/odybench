"""
odybench.lean.candidates -- the candidate and target pools of the lean run
(DESIGN 4.1, 4.2, 4.5; LEAN.md "N3 (part)").

Pools (Ithaki unless a site is named):

  P_all     every geocentric apparent-longitude conjunction whose Day 0 (UT+2
            civil date) lies in the background -1999..+200, computed with DE431
            in chunks that never straddle JD 1721425.5 and SMH2020 Delta-T for
            UT.  One Day-0 date per clock: day0_jdn_ut2 (B&M's clock, F2 (a))
            and day0_jdn_lmt.
  P_day     conjunctions whose instant falls in daylight at the site (the
            Sun's centre above -0.8333 deg; DE441, SMH2020).
  P_spring  conjunctions passing C_rel (4.5) on the sequential or the parallel
            count, with Day 0 the UT+2 date (flags per count).
  T         P_day in the core -1748..-51; T_C = T and P_spring;
  T_A(v)    T_C targets whose Venus slot and Mercury slot of variant v
            (data/prereg/slots.json) hold on the same count as C (4.2).

The sky each spring candidate needs is computed per candidate (Venus and the
Sun on Days -5 and -4; Mercury's risings and events over Days -49..-18), not
as full daily tables.  Candidates passing the fixed Julian C bounds are given
the same sky, so that N1 can report both bounds (5.1 item 4).

**The masked target.**  `load(mask_target=True)` removes 16 Apr -1177 from
P_all immediately after the Day-0 dates are computed, before any predicate
(daylight, C, a sky quantity) is evaluated, and every evaluation function of
the lean run raises TargetMasked if it is handed that day while the pool is
masked (DESIGN 4.2, 12.3).  The masked and the unmasked pools are cached in
separate files under data/cache/.

Run as `py -m odybench.lean.candidates --selftest` (synthetic) or
`py -m odybench.lean.candidates --build [--unmasked]` (real sky: the null-side
stage only, LEAN.md stage 3).
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import sys
import time
from dataclasses import dataclass, field
from multiprocessing import Pool as _MPPool

import numpy as np

from odybench import calendar as cal
from odybench.model import POOL_DTYPE
from odybench.lean import (CACHE_DIR, PREREG_DIR, ROOT, TARGET_JDN, TargetMasked,
                           check_target_masked)
from odybench.lean import sky

BACKGROUND = (-1999, 200)
CORE = (-1748, -51)
EPOCH_BAND = (-1877, -477)
COUNTS = {
    "seq": dict(c=(-29, -12), v=-5, m=-34, e=-11),
    "par": dict(c=(-28, -11), v=-4, m=-33, e=-10),
}
FIXED_C = ((2, 17), (4, 4))            # Ti-29 >= 17 Feb, Ti-12 <= 4 Apr (T0b; 5.1 item 4)
FIXED_E_LO = (4, 1)                    # 1 Apr <= Ti-11 <= 4/5/6 Apr
MERC_MARGIN = 15                       # days of Mercury series beyond Days -34/-33
CACHE_VERSION = "lean-candidates-1"


def slots():
    return json.loads((PREREG_DIR / "slots.json").read_text(encoding="utf-8"))


def windows():
    return json.loads((PREREG_DIR / "windows.json").read_text(encoding="utf-8"))


POOL_CODE = ("odybench/lean/__init__.py", "odybench/lean/sky.py", "odybench/lean/candidates.py",
             "odybench/ephem.py", "odybench/calendar.py", "odybench/model.py")


def code_hash(files=POOL_CODE) -> str:
    """SHA-256 over the code a pool depends on (POOL_CODE); a cached pool
    built by other code is rebuilt."""
    h = hashlib.sha256()
    files = [ROOT / f for f in files]
    for p in files:
        h.update(p.name.encode())
        h.update(p.read_bytes())
    return h.hexdigest()


# ----------------------------------------------------------- conjunctions

def _lon_diff(jd_tt, eph):
    g = sky.geo_ecliptic(("moon", "sun"), jd_tt, eph)
    return (g["moon"][0] - g["sun"][0] + 180.0) % 360.0 - 180.0


def _conj_block(args):
    """Conjunctions in [a, b] (TT), one SPK request side of the DE431 split."""
    a, b, eph, step = args
    grid = np.arange(a, b, step)
    if grid.size == 0 or b - grid[-1] > 1e-9:
        grid = np.append(grid, b)
    d = _lon_diff(grid, eph)
    br = np.nonzero((d[:-1] < 0) & (d[1:] >= 0) & (np.abs(d[:-1]) < 90) & (np.abs(d[1:]) < 90))[0]
    lo, hi = grid[br], grid[br + 1]
    flo, fhi = d[br], d[br + 1]
    if lo.size == 0:
        return np.zeros(0)
    while np.max(hi - lo) > 1e-7:
        m = 0.5 * (lo + hi)
        fm = _lon_diff(m, eph)
        neg = fm < 0
        lo, flo = np.where(neg, m, lo), np.where(neg, fm, flo)
        hi, fhi = np.where(neg, hi, m), np.where(neg, fhi, fm)
    den = np.where(fhi - flo == 0, 1.0, fhi - flo)
    return np.clip(lo - flo * (hi - lo) / den, lo, hi)


def conjunctions(jd_tt0, jd_tt1, eph="de431", workers=1, block_days=365.25 * 25, step=2.0):
    """TT instants of the geocentric conjunctions (apparent ecliptic longitude
    of date of the Moon = the Sun's) in [jd_tt0, jd_tt1], bisected to 1e-7 d
    (ephem.new_moons' xtol).  For DE431 the span is cut at JD 1721425.5 so that
    no request straddles it (DESIGN 0)."""
    cuts = [jd_tt0, jd_tt1]
    if eph == "de431" and jd_tt0 < sky.DE431_SPLIT_JD < jd_tt1:
        cuts = [jd_tt0, sky.DE431_SPLIT_JD, jd_tt1]
    tasks = []
    for a, b in zip(cuts[:-1], cuts[1:]):
        x = a
        while x < b:
            y = min(x + block_days, b)
            tasks.append((x, y, eph, step))
            x = y
    if workers > 1 and len(tasks) > 1:
        with _MPPool(min(workers, len(tasks))) as p:
            res = p.map(_conj_block, tasks)
    else:
        res = [_conj_block(t) for t in tasks]
    out = np.sort(np.concatenate(res)) if res else np.zeros(0)
    if out.size > 1:                                   # a root found from both sides of a cut
        keep = np.concatenate(([True], np.diff(out) > 1e-5))
        out = out[keep]
    return out[(out >= jd_tt0) & (out <= jd_tt1)]


# ------------------------------------------------------------ the pool

@dataclass
class Pool:
    """A candidate pool: rec (model.POOL_DTYPE) plus per-row columns.

    masked: 16 Apr -1177 was removed before any predicate was evaluated;
    every evaluation function calls `self.guard()` first."""
    rec: np.ndarray
    cols: dict = field(default_factory=dict)
    masked: bool = True
    site: str = "ithaki"
    meta: dict = field(default_factory=dict)

    def __len__(self):
        return len(self.rec)

    def guard(self, what="pool"):
        check_target_masked(self.rec["day0_jdn_ut2"], self.masked, what)

    @property
    def day0(self):
        return self.rec["day0_jdn_ut2"]

    @property
    def jd_tt(self):
        return self.rec["jd_tt"]

    @property
    def year(self):
        return self.cols["year"]

    def subset(self, mask):
        mask = np.asarray(mask)
        return Pool(self.rec[mask], {k: v[mask] for k, v in self.cols.items()}, self.masked,
                    self.site, dict(self.meta))

    # -- pools --------------------------------------------------------------
    def in_years(self, y0, y1):
        return (self.year >= y0) & (self.year <= y1)

    def P_day(self):
        self.guard("P_day")
        return self.rec["daylight"].copy()

    def C(self, count, kind="rel"):
        self.guard("C")
        return self.cols[f"c_{kind}_{count}"].copy()

    def P_spring(self):
        return self.C("seq") | self.C("par")

    def T(self, core=CORE):
        return self.P_day() & self.in_years(*core)

    def T_C(self, core=CORE):
        return self.T(core) & self.P_spring()

    def T_A(self, v, core=CORE):
        return self.T(core) & slot_A(self, v)


def _year_of(jdn):
    y, _, _ = cal.julian_from_jdn(np.asarray(jdn, dtype=np.int64))
    return np.asarray(y, dtype=np.int64)


def _doy(jdn):
    jdn = np.atleast_1d(np.asarray(jdn, dtype=np.int64))
    return jdn - np.asarray(cal.jdn_from_julian(_year_of(jdn), 1, 1), dtype=np.int64) + 1


def _jdn_md(years, md):
    y = np.atleast_1d(np.asarray(years, dtype=np.int64))
    return np.asarray(cal.jdn_from_julian(y, md[0], md[1]), dtype=np.int64)


def c_flags(day0, year, A, P):
    """C on both counts for the given bounds (JDN arrays per row)."""
    out = {}
    for cnt, k in COUNTS.items():
        lo, hi = k["c"]
        out[cnt] = (day0 + lo >= A) & (day0 + hi <= P)
    return out


def fixed_bounds(year):
    return _jdn_md(year, FIXED_C[0]), _jdn_md(year, FIXED_C[1])


def e_flags(pool, n, kind="rel", count="seq"):
    """E on a count: Ti-11 (seq) or Ti-10 (par) in [eq(y), eq(y) + n] (E_rel,
    eq the UT+2 civil date of the March equinox), or in [1 Apr, 1 Apr + n]
    (fixed: <= 4, 5, 6 Apr for n = 3, 4, 5) (DESIGN 4.5, 3.2)."""
    pool.guard("E")
    d = pool.day0 + COUNTS[count]["e"]
    lo = pool.cols["eq_jdn"] if kind == "rel" else _jdn_md(pool.year, FIXED_E_LO)
    return (d >= lo) & (d <= lo + n)


# --------------------------------------------------------------- slots

def slot_A(pool, v):
    """4.2's slot family (data/prereg/slots.json), day counts paired: C_rel,
    the Venus slot and the Mercury slot hold on one count; a target is in
    T_A(v) if either count passes as a whole."""
    pool.guard("slot_A")
    sl = slots()
    var = sl["variants"].get(v) or sl["reported"].get(v)
    if var is None:
        raise KeyError(v)
    out = np.zeros(len(pool), dtype=bool)
    for cnt, k in COUNTS.items():
        c = pool.cols[f"c_rel_{cnt}"]
        vo, mo = -k["v"], -k["m"]
        lead = pool.cols[f"lead_m{vo}"]
        vr = var["venus"]
        if vr["rule"] == "rises_before_sun_visible":
            ven = (lead > 0) & (pool.cols[f"vsun_m{vo}"] <= vr["sun_alt_max_at_venus_rise_deg"])
        elif vr["rule"] == "rise_lead_min":
            ven = lead >= vr["lead_min"]
        else:
            raise NotImplementedError(f"Venus slot rule {vr['rule']} (v6 is reported only; not in the lean run)")
        mr = var["mercury"]
        kd = mr["k_days"]
        ev = np.zeros(len(pool), dtype=bool)
        for e in mr["events"]:
            col = {"rise_azimuth_max_vertex": "d_mwra", "greatest_western_elongation": "d_gwe",
                   "morning_station": "d_sta"}[e]
            ev |= pool.cols[f"{col}_m{mo}"] <= kd
        if mr["visibility"] is not None:
            vis = pool.cols[f"msun_m{mo}"] <= mr["visibility"]["sun_alt_max_at_mercury_rise_deg"]
        else:
            vis = np.zeros(len(pool), dtype=bool)
        comb = mr["combine"]
        merc = ev & vis if comb == "event_and_visible" else (ev | vis if comb == "event_or_visible" else ev)
        out |= c & ven & merc
    return out


# ---------------------------------------------------------- per-candidate sky

SKY_COLS_F = ["lead_m5", "lead_m4", "vsun_m5", "vsun_m4", "vrise_m5", "vrise_m4",
              "mrise_m34", "mrise_m33", "maz_m34", "maz_m33", "msun_m34", "msun_m33",
              "d_mwra_m34", "d_mwra_m33", "d_mwra_any_m34", "d_mwra_any_m33",
              "d_gwe_m34", "d_gwe_m33", "d_sta_m34", "d_sta_m33",
              "t_mwra_m34", "t_mwra_m33"]
SKY_COLS_B = ["flat_mwra_m34", "flat_mwra_m33"]


def candidate_sky(day0, lat, lon, dt="smh2020", eph="de441", margin=MERC_MARGIN):
    """The sky of each Day 0 (UT+2 JDN): Venus and the Sun on Days -5, -4;
    Mercury's rising (instant, azimuth, the Sun's altitude) on Days -34, -33;
    and the distance (days, continuous) from that rising instant to the
    nearest morning rise-azimuth maximum (vertex), greatest western
    elongation and morning station.  Returns a dict of arrays aligned with
    day0 (SKY_COLS_F, SKY_COLS_B)."""
    day0 = np.asarray(day0, dtype=np.int64)
    n = day0.size
    out = {c: np.full(n, np.nan) for c in SKY_COLS_F}
    out.update({c: np.zeros(n, dtype=bool) for c in SKY_COLS_B})
    if n == 0:
        return out
    # Venus and the Sun
    vdays = np.unique(np.concatenate([day0 - 5, day0 - 4]))
    lv = sky.rise_lead(vdays, lat, lon, body="venus", dt=dt, eph=eph, zone_h=sky.UT2)
    for o in (5, 4):
        j = np.searchsorted(vdays, day0 - o)
        out[f"lead_m{o}"] = lv["lead_min"][j]
        out[f"vsun_m{o}"] = lv["sun_alt_at_body_rise"][j]
        out[f"vrise_m{o}"] = lv["body_rise"][j]
    # Mercury
    mdays = np.unique(np.concatenate([np.arange(d - 34 - margin, d - 33 + margin + 1) for d in day0]))
    mr = sky.crossing("mercury", mdays, lat, lon, zone_h=sky.UT2, dt=dt, eph=eph,
                      window_h=sky.morning_window("mercury"), with_elong=True)
    mx = sky.azimuth_maxima(mdays, mr["jd_ut"], mr["az"], mr["elong"])
    segs = [sky.tt_of_ut(sky.day_start_ut(mdays[i0:i1], sky.UT2), dt) for i0, i1 in sky.segments(mdays)]
    ev = sky.geo_events("mercury", segs, eph, dt)
    mor = mx[mx["morning"]]
    gwe = ev[ev["kind"] == "W"]["jd_ut"]
    sta = ev[np.isin(ev["kind"], ["D", "R"]) & ev["morning"]]["jd_ut"]
    for o in (34, 33):
        j = np.searchsorted(mdays, day0 - o)
        t = mr["jd_ut"][j]
        out[f"mrise_m{o}"] = t
        out[f"maz_m{o}"] = mr["az"][j]
        out[f"msun_m{o}"] = mr["sun_alt"][j]
        d, idx = sky.nearest(t, mor["jd_ut"])
        out[f"d_mwra_m{o}"] = d
        if len(mor):
            out[f"t_mwra_m{o}"] = np.where(np.isfinite(d), mor["jd_ut"][idx], np.nan)
            out[f"flat_mwra_m{o}"] = np.where(np.isfinite(d), mor["flat"][idx], False)
        out[f"d_mwra_any_m{o}"] = sky.nearest(t, mx["jd_ut"])[0]
        out[f"d_gwe_m{o}"] = sky.nearest(t, gwe)[0]
        out[f"d_sta_m{o}"] = sky.nearest(t, sta)[0]
    return out


def _sky_task(args):
    day0, lat, lon, dt, eph = args
    return candidate_sky(day0, lat, lon, dt, eph)


# ------------------------------------------------------------ the build

def _cache_path(site, masked, years):
    tag = "masked" if masked else "UNMASKED"
    return CACHE_DIR / f"lean_pool_{site}_{years[0]}_{years[1]}_{tag}.npz"


def build(site="ithaki", years=BACKGROUND, mask_target=True, dt="smh2020", workers=14,
          verbose=True, sky_filter=None):
    """Build the pool from the real sky (see the module docstring).
    sky_filter: optional bool function of the Pool selecting the rows that get
    sky (default: C_rel or fixed C on either count)."""
    t_start = time.time()
    lat, lon, _ = sky.site(site)
    log = (lambda *a: print(*a, flush=True)) if verbose else (lambda *a: None)
    # 1. conjunctions (DE431, SMH2020), Day 0 per clock
    b0 = cal.jd_from_julian(years[0], 1, 1) - 2.0
    b1 = cal.jd_from_julian(years[1] + 1, 1, 1) + 2.0
    tt = conjunctions(b0, b1, eph="de431", workers=workers)
    ut = sky.ut_of_tt(tt, "smh2020")
    d_ut2 = np.asarray(cal.jdn_of_instant(ut, sky.UT2), dtype=np.int64)
    d_lmt = np.asarray(cal.jdn_of_instant(ut, lon / 15.0), dtype=np.int64)
    yr = _year_of(d_ut2)
    keep = (yr >= years[0]) & (yr <= years[1])
    n_found = int(keep.sum())
    has_target = bool(np.any(d_ut2[keep] == TARGET_JDN))
    if mask_target:
        keep &= d_ut2 != TARGET_JDN                    # masked BEFORE any predicate
    rec = np.zeros(int(keep.sum()), dtype=POOL_DTYPE)
    rec["jd_tt"], rec["jd_ut"] = tt[keep], ut[keep]
    rec["day0_jdn_ut2"], rec["day0_jdn_lmt"] = d_ut2[keep], d_lmt[keep]
    rec["kind"], rec["cat_idx"] = "conj", -1
    pool = Pool(rec, {"year": yr[keep]}, mask_target, site)
    pool.guard("build")
    log(f"[candidates] {n_found} conjunctions with Day 0 in {years[0]}..{years[1]}"
        f"{' (target removed)' if (mask_target and has_target) else ''}; {time.time() - t_start:.0f} s")
    # 2. daylight (DE441, SMH2020)
    pool.rec["daylight"] = sky.sun_alt(pool.rec["jd_ut"], lat, lon, "smh2020", "de441") > sky.H0_SUN
    # 3. C_rel and the fixed bounds
    h_A, h_P = sky.calibrate_crel(lat, lon, "smh2020", "de441")
    ys = np.arange(years[0], years[1] + 1)
    blocks = np.array_split(ys, max(1, min(len(ys), workers * 4)))
    with _MPPool(workers) as mp:
        alts = mp.starmap(sky.season_altitudes, [(b, lat, lon, "smh2020", "de441") for b in blocks])
    sb = {}
    for a in alts:
        sb.update(sky.season_bounds_from(a, h_A, h_P))
    bad = [y for y, v in sb.items() if not v[2]]
    if bad:
        raise RuntimeError(f"C_rel search range too short in years {bad[:5]}")
    A = np.array([sb[int(y)][0] for y in pool.year], dtype=np.int64)
    P = np.array([sb[int(y)][1] for y in pool.year], dtype=np.int64)
    cr = c_flags(pool.day0, pool.year, A, P)
    Af, Pf = fixed_bounds(pool.year)
    cf = c_flags(pool.day0, pool.year, Af, Pf)
    pool.cols.update(A_jdn=A, P_jdn=P, c_rel_seq=cr["seq"], c_rel_par=cr["par"],
                     c_fix_seq=cf["seq"], c_fix_par=cf["par"], doy=_doy(pool.day0))
    log(f"[candidates] C_rel: h_A {h_A:.2f}, h_P {h_P:.2f}; P_spring {int((cr['seq'] | cr['par']).sum())}; "
        f"{time.time() - t_start:.0f} s")
    # 4. the March equinox of each year (DE441), UT+2 civil date
    eq_tt = sky.march_equinox(ys, "de441")
    eq_jdn = np.asarray(cal.jdn_of_instant(sky.ut_of_tt(eq_tt, "smh2020"), sky.UT2), dtype=np.int64)
    pool.cols["eq_jdn"] = eq_jdn[pool.year - years[0]]
    # 5. per-candidate sky
    need = sky_filter(pool) if sky_filter else (cr["seq"] | cr["par"] | cf["seq"] | cf["par"])
    idx = np.nonzero(need)[0]
    for c in SKY_COLS_F:
        pool.cols[c] = np.full(len(pool), np.nan)
    for c in SKY_COLS_B:
        pool.cols[c] = np.zeros(len(pool), dtype=bool)
    pool.cols["sky"] = need.copy()
    chunks = [c for c in np.array_split(idx, max(1, min(len(idx), workers * 6))) if len(c)]
    tasks = [(pool.day0[c], lat, lon, dt, "de441") for c in chunks]
    with _MPPool(workers) as mp:
        res = mp.map(_sky_task, tasks)
    for c, r in zip(chunks, res):
        for k, v in r.items():
            pool.cols[k][c] = v
    pool.meta = dict(version=CACHE_VERSION, site=site, lat=lat, lon=lon, years=list(years),
                     dt=str(dt), conj_ephemeris="de431", sky_ephemeris="de441", h_A=h_A, h_P=h_P,
                     masked=mask_target, n_conj=n_found, code_sha256=code_hash(),
                     built_s=round(time.time() - t_start, 1))
    log(f"[candidates] sky for {len(idx)} candidates; total {time.time() - t_start:.0f} s")
    return pool


def save(pool, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(path, rec=pool.rec, meta=json.dumps(pool.meta),
                        **{f"col_{k}": v for k, v in pool.cols.items()})


def read(path):
    z = np.load(path, allow_pickle=False)
    meta = json.loads(str(z["meta"]))
    cols = {k[4:]: z[k] for k in z.files if k.startswith("col_")}
    return Pool(z["rec"], cols, bool(meta["masked"]), meta["site"], meta)


def load(mask_target=True, site="ithaki", years=BACKGROUND, rebuild=False, workers=14, verbose=True):
    """The pool, from data/cache/ if present and built by the same code
    (code_hash), else built and cached.  mask_target=True removes 16 Apr -1177
    before any predicate is evaluated; the masked and unmasked pools are
    separate files."""
    path = _cache_path(site, mask_target, years)
    if path.exists() and not rebuild:
        p = read(path)
        if p.meta.get("version") == CACHE_VERSION and p.masked == mask_target                 and p.meta.get("code_sha256") == code_hash():
            p.guard("load")
            return p
        if verbose:
            print(f"[candidates] {path.name} was built by other code or settings: rebuilding", flush=True)
    p = build(site, years, mask_target, workers=workers, verbose=verbose)
    save(p, path)
    return p


# ------------------------------------------------------------ synthetic

def synthetic(n_years=600, y0=-1400, seed=1, mask_target=True, rate_v=0.3, rate_m=0.08):
    """A synthetic pool with the real pools' shape and no sky: 12.37
    conjunctions a year, half in daylight, C windows as at -1177 drifting
    0.64 d per century, and Venus/Mercury columns drawn at rough rates.  For
    the --selftest modes; never a substitute for the real sky."""
    rng = np.random.default_rng(seed)
    syn = 29.530589
    jd0 = cal.jd_from_julian(y0, 1, 1) + rng.random() * syn
    jd1 = cal.jd_from_julian(y0 + n_years, 1, 1)
    base = np.arange(jd0, jd1, syn)
    tt = base + rng.normal(0, 0.3, size=base.size)
    ut = tt - 0.33
    d0 = np.asarray(cal.jdn_of_instant(ut, 2.0), dtype=np.int64)
    yr = _year_of(d0)
    keep = (yr >= y0) & (yr < y0 + n_years)
    if mask_target:
        keep &= d0 != TARGET_JDN
    rec = np.zeros(int(keep.sum()), dtype=POOL_DTYPE)
    rec["jd_tt"], rec["jd_ut"], rec["day0_jdn_ut2"], rec["day0_jdn_lmt"] = tt[keep], ut[keep], d0[keep], d0[keep]
    rec["kind"], rec["cat_idx"] = "conj", -1
    rec["daylight"] = rng.random(len(rec)) < 0.509
    yr = yr[keep]
    n = len(rec)
    drift = np.round((yr + 1177) * 0.0064).astype(np.int64)
    A = _jdn_md(yr, (2, 17)) + drift
    P = _jdn_md(yr, (4, 4)) + drift
    cr = c_flags(rec["day0_jdn_ut2"], yr, A, P)
    cf = c_flags(rec["day0_jdn_ut2"], yr, *fixed_bounds(yr))
    cols = dict(year=yr, A_jdn=A, P_jdn=P, c_rel_seq=cr["seq"], c_rel_par=cr["par"],
                c_fix_seq=cf["seq"], c_fix_par=cf["par"], doy=_doy(rec["day0_jdn_ut2"]),
                eq_jdn=_jdn_md(yr, (4, 1)) - np.round((yr + 1177) * 0.0078).astype(np.int64))
    need = cr["seq"] | cr["par"] | cf["seq"] | cf["par"]
    cols["sky"] = need
    for c in SKY_COLS_F:
        cols[c] = np.full(n, np.nan)
    for c in SKY_COLS_B:
        cols[c] = np.zeros(n, dtype=bool)
    m = int(need.sum())
    for o in (5, 4):
        lead = rng.normal(40, 70, m)
        cols[f"lead_m{o}"][need] = lead
        cols[f"vsun_m{o}"][need] = np.where(lead > 0, -0.17 * lead + rng.normal(0, 1, m), 5.0)
    for o in (34, 33):
        cols[f"mrise_m{o}"][need] = rec["jd_ut"][need] - o
        cols[f"msun_m{o}"][need] = rng.normal(-6, 6, m)
        for nm in ("d_mwra", "d_gwe", "d_sta"):
            cols[f"{nm}_m{o}"][need] = rng.exponential(1.0 / rate_m / 4, m)
        cols[f"d_mwra_any_m{o}"][need] = cols[f"d_mwra_m{o}"][need]
    return Pool(rec, cols, mask_target, "synthetic", dict(synthetic=True, seed=seed))


def _selftest():
    p = synthetic(seed=3)
    assert len(p) > 7000, len(p)
    assert not np.any(p.day0 == TARGET_JDN)
    # the target is removed before predicates, and guards fire if it is present
    pu = synthetic(seed=3, mask_target=False, n_years=600, y0=-1400)
    tgt = pu.day0 == TARGET_JDN
    if tgt.any():
        bad = Pool(pu.rec, pu.cols, True, "synthetic")
        for fn in (bad.P_day, bad.P_spring, lambda: slot_A(bad, "v1"), lambda: e_flags(bad, 4)):
            try:
                fn()
            except TargetMasked:
                pass
            else:
                raise AssertionError("TargetMasked not raised")
    for v in ("v0", "v1", "v2", "v3", "v4", "v5"):
        ta = p.T_A(v)
        assert np.all(p.T_C()[ta]), v
    n_tc = int(p.T_C().sum())
    n_a = {v: int(p.T_A(v).sum()) for v in ("v0", "v1", "v2", "v3", "v4", "v5")}
    assert n_a["v2"] <= n_a["v1"] and n_a["v0"] <= n_a["v2"] and n_a["v3"] <= n_a["v2"] and n_a["v5"] <= n_a["v4"]
    print(f"[candidates selftest] synthetic pool n {len(p)}, n_T {int(p.T().sum())}, n_TC {n_tc}, n_A {n_a}")
    print("[candidates selftest] PASS")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        _selftest()
    elif "--build" in sys.argv:
        load(mask_target="--unmasked" not in sys.argv, rebuild="--rebuild" in sys.argv)
    else:
        print(__doc__)
