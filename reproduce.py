"""
reproduce.py -- T0: B&M's search recomputed with DE441 at B&M's clock
(DESIGN 3.2-3.5; LEAN.md step T0).  Agent L1.

TARGET SIDE.  T0 reads 16 Apr 1178 BC (-1177), so the full run belongs to
LEAN.md stage 5, after the second freeze.  It refuses to run unless the git
tag prereg-2 exists (override: --no-freeze-check, for the integrator only).

  py reproduce.py --run              T0b, the T0 grid, T0_pass, R/RE/NR, A1-A5,
                                     the M sensitivity; then r_Ody, the unmasked
                                     G_BM(v) (reported beside) and the target's
                                     held-out pool membership ("heldout_target"
                                     for heldout.py), from the unmasked pool
  py reproduce.py --s2-replay        the replay of Table S2 on every row except
                                     1178 BC (A1-A3 without the target row; no
                                     candidate set, survivor set or reach): an
                                     instrument check allowed before the freeze
  py reproduce.py --selftest         synthetic tables only

T0b (3.2), exactly:
 1. candidates: every geocentric apparent-longitude conjunction (DE441, Moon
    included) whose UT+2 instant lies in [-1249 Jan 1 00:00, -1113 Jan 1
    00:00) UT+2, UT = TT - 27,602.7 s;  2. Ti = its UT+2 civil date;
 3. C fixed Julian: Ti-29 >= 17 Feb and Ti-12 <= 4 Apr of Ti's year;
 4. V: on Ti-5 Venus rises >= 90.0 min before the Sun;
 5. M: Mercury's rising azimuth every morning over Ti-34 +- 60 d (risings
    bisected to 0.1 s); MWRA_vtx = the vertex of the least-squares parabola
    through the 7 mornings centred on the discrete local maximum nearest
    Ti-34, Delta = (rising instant on Ti-34) - (vertex instant), pass
    |Delta| <= 1.5 d (1, 2.5, 3.5 reported); MWRA_int = that maximum's date,
    Delta = (Ti-34) - MWRA_int, equidistant maxima resolve to the earlier,
    pass |Delta| <= 1 (2, 3 reported); curvature, margin and the flat flag;
    visibility on Ti-34 three ways: off, AV 10 (Sun <= -10 deg at Mercury's
    rising), PLSV (AV = 10.5 + 1.4 m at a 1 deg critical altitude);
 6. E reported: 1 Apr <= Ti-11 <= 4, 5 or 6 Apr, and the computed equinox;
 7. the parallel reckoning (-28/-11, -4, -33, -10) reported;
 8-10. the S2-shaped table, the comparison with S2, the M sensitivity.
Site `bm` (38.4 N, 20.7 E), airless, h0 -0.8333 / -0.5667 deg, Vondrak
precession.  The MWRA of T0b takes the nearest maximum whatever Mercury's
side of the Sun (3.2 says no more); the morning-only maximum (the event of
G_BM*'s readings) is reported beside it.
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import numpy as np  # noqa: E402

from odybench import calendar as cal  # noqa: E402
from odybench.lean import TARGET_JDN, TARGET_YMD  # noqa: E402
from odybench.lean import sky  # noqa: E402

OUT = ROOT / "results" / "t0"
S2_TSV = ROOT / "data" / "bm2008-a" / "table_s2.tsv"
JSEX = ROOT / "data" / "jsex"
DT_BM = sky.BM_CLOCK_DT
WINDOW = ((-1249, 1, 1), (-1114, 12, 31))
SEARCH_D = 60                       # Ti-34 +- 60 d
HALF7 = 3                           # 7-morning parabola
C_LO, C_HI = (2, 17), (4, 4)
E_HI = {4: (4, 4), 5: (4, 5), 6: (4, 6)}
OFFS = {"seq": dict(c=(-29, -12), v=-5, m=-34, e=-11), "par": dict(c=(-28, -11), v=-4, m=-33, e=-10)}
VTX_TOLS = (1.0, 1.5, 2.5, 3.5)
INT_TOLS = (1, 2, 3)
PRIMARY = dict(e=5, vis="off", mwra="vtx")
MON = {m: i + 1 for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split())}
MN = {v: k for k, v in MON.items()}


def lab(jdn):
    y, m, d = cal.julian_from_jdn(int(jdn))
    return f"{d}-{MN[m]}"


def hm(jd_ut, zone=2.0):
    if not np.isfinite(jd_ut):
        return ""
    h = cal.julian_from_jd(float(jd_ut), zone)[3]
    s = int(round(h * 3600))
    return f"{s // 3600}:{(s % 3600) // 60:02d}:{s % 60:02d}"


def freeze_tag_exists(tag):
    try:
        out = subprocess.run(["git", "-C", str(ROOT), "tag", "-l", tag], capture_output=True, text=True,
                             timeout=20).stdout
        return tag in out.split()
    except Exception:                       # noqa: BLE001
        return False


# --------------------------------------------------------------- sky

def mercury_daily(days, lat, lon, dt=DT_BM, h0=None, refraction=False):
    """Daily Mercury risings (UT+2 civil days) and the maxima of the series."""
    days = np.unique(np.asarray(days, dtype=np.int64))
    r = sky.crossing("mercury", days, lat, lon, zone_h=sky.UT2, h0=h0, dt=dt, eph="de441",
                     window_h=sky.morning_window("mercury"), refraction=refraction, with_elong=True)
    mx = sky.azimuth_maxima(days, r["jd_ut"], r["az"], r["elong"])
    return days, r, mx


def mwra(md, days, r, mx, side="any"):
    """For each Mercury day md: the discrete local maximum nearest md (within
    +-SEARCH_D, equidistant -> earlier) and its vertex.  Returns a dict of
    arrays: max_jdn, delta_int (days, md - max), delta_vtx (rising on md -
    vertex), curv, margin, flat, morning, az_vtx."""
    md = np.asarray(md, dtype=np.int64)
    sel = mx if side == "any" else mx[mx["morning"]]
    n = md.size
    out = {k: np.full(n, np.nan) for k in ("delta_vtx", "curv", "margin", "az_vtx", "vtx_jd")}
    out.update(max_jdn=np.full(n, -1, dtype=np.int64), delta_int=np.full(n, np.nan),
               flat=np.zeros(n, dtype=bool), morning=np.zeros(n, dtype=bool))
    if sel.size == 0:
        return out
    dd = sel["day_jdn"]
    order = np.argsort(dd, kind="stable")
    dd, sel = dd[order], sel[order]
    k = np.searchsorted(dd, md)
    lo = np.clip(k - 1, 0, dd.size - 1)
    hi = np.clip(k, 0, dd.size - 1)
    take_hi = np.abs(dd[hi] - md) < np.abs(md - dd[lo])        # ties -> the earlier (lo)
    j = np.where(take_hi, hi, lo)
    ok = np.abs(dd[j] - md) <= SEARCH_D
    jm = np.clip(np.searchsorted(days, md), 0, len(days) - 1)
    rise_md = np.where(days[jm] == md, r["jd_ut"][jm], np.nan)
    out["max_jdn"] = np.where(ok, dd[j], -1)
    out["delta_int"] = np.where(ok, (md - dd[j]).astype(float), np.nan)
    out["delta_vtx"] = np.where(ok, rise_md - sel["jd_ut"][j], np.nan)
    out["vtx_jd"] = np.where(ok, sel["jd_ut"][j], np.nan)
    for f in ("curv", "margin"):
        out[f] = np.where(ok, sel[f][j], np.nan)
    out["az_vtx"] = np.where(ok, sel["az"][j], np.nan)
    out["flat"] = ok & sel["flat"][j]
    out["morning"] = ok & sel["morning"][j]
    return out


def t0b_candidates(dt=DT_BM):
    a_ut, b_ut = cal.span_bounds(*WINDOW, offset_hours=2)
    from odybench.lean.candidates import conjunctions
    tt = conjunctions(a_ut + dt / 86400 - 0.01, b_ut + dt / 86400 + 0.01, eph="de441")
    ut = tt - dt / 86400.0
    keep = (ut >= a_ut) & (ut < b_ut)
    tt, ut = tt[keep], ut[keep]
    ti = np.asarray(cal.jdn_of_instant(ut, 2.0), dtype=np.int64)
    return tt, ut, ti


def t0b_table(ti, ut=None, lat=None, lon=None, dt=DT_BM, plsv=True):
    """Every quantity of 3.2 steps 2-7 for Day-0 dates ti (UT+2 JDN)."""
    if lat is None:
        lat, lon, _ = sky.site("bm")
    ti = np.asarray(ti, dtype=np.int64)
    y = np.asarray(cal.julian_from_jdn(ti)[0], dtype=np.int64)
    T = dict(ti=ti, year=y)
    if ut is not None:
        T["conj_ut"] = np.asarray(ut, dtype=float)
    lo = np.asarray(cal.jdn_from_julian(y, *C_LO), dtype=np.int64)
    hi = np.asarray(cal.jdn_from_julian(y, *C_HI), dtype=np.int64)
    apr1 = np.asarray(cal.jdn_from_julian(y, 4, 1), dtype=np.int64)
    days_all = np.unique(np.concatenate([np.arange(t - 34 - SEARCH_D - HALF7 - 2, t - 33 + SEARCH_D + HALF7 + 3)
                                         for t in ti]))
    days, r, mx = mercury_daily(days_all, lat, lon, dt)
    for cnt, o in OFFS.items():
        T[f"C_{cnt}"] = (ti + o["c"][0] >= lo) & (ti + o["c"][1] <= hi)
        T[f"C_margin_{cnt}"] = np.minimum(ti + o["c"][0] - lo, hi - (ti + o["c"][1]))
        lv = sky.rise_lead(ti + o["v"], lat, lon, body="venus", dt=dt, eph="de441", zone_h=sky.UT2)
        T[f"lead_{cnt}"] = lv["lead_min"]
        T[f"venus_rise_{cnt}"] = lv["body_rise"]
        T[f"sunrise_{cnt}"] = lv["sun_rise"]
        md = ti + o["m"]
        for side in ("any", "morning"):
            w = mwra(md, days, r, mx, side)
            for k, v in w.items():
                T[f"mw_{side}_{k}_{cnt}"] = v
        j = np.searchsorted(days, md)
        T[f"merc_rise_{cnt}"] = r["jd_ut"][j]
        T[f"merc_sun_alt_{cnt}"] = r["sun_alt"][j]
        T[f"vis_av10_{cnt}"] = r["sun_alt"][j] <= -10.0
        if plsv:
            pv = sky.plsv_morning(md, lat, lon, dt=dt, eph="de441")
            T[f"vis_plsv_{cnt}"] = pv["visible"]
            T[f"plsv_margin_{cnt}"] = -pv["av"] - pv["sun_alt"]
        T[f"e_day_{cnt}"] = ti + o["e"]
        for n, md_ in E_HI.items():
            T[f"E{n}_{cnt}"] = (ti + o["e"] >= apr1) & (ti + o["e"] <= np.asarray(cal.jdn_from_julian(y, *md_)))
    return T


def equinox_ut2(years, dt=DT_BM):
    tt = sky.march_equinox(years, "de441")
    return tt - dt / 86400.0


# --------------------------------------------------------- T0 grid

def m_pass(T, cnt, mwra_def, tol=None, vis="off", side="any"):
    if mwra_def == "vtx":
        p = np.abs(T[f"mw_{side}_delta_vtx_{cnt}"]) <= (1.5 if tol is None else tol)
    else:
        p = np.abs(T[f"mw_{side}_delta_int_{cnt}"]) <= (1 if tol is None else tol)
    if vis == "av10":
        p = p & T[f"vis_av10_{cnt}"]
    elif vis == "plsv":
        p = p & T[f"vis_plsv_{cnt}"]
    return p


def ncvm(T, cnt="seq", mwra_def="vtx", vis="off", tol=None, side="any"):
    return T[f"C_{cnt}"] & (T[f"lead_{cnt}"] >= 90.0) & m_pass(T, cnt, mwra_def, tol, vis, side)


def classify(T, target_jdn=TARGET_JDN, e=5, vis="off", mwra_def="vtx", cnt="seq"):
    """R / RE / NR for one cell of the T0 grid (3.5)."""
    is_t = T["ti"] == target_jdn
    base = ncvm(T, cnt, mwra_def, vis)
    with_e = base & T[f"E{e}_{cnt}"]
    t_base = bool(np.any(base & is_t))
    surv = [int(x) for x in T["ti"][base]]
    surv_e = [int(x) for x in T["ti"][with_e]]
    if t_base and len(surv) == 1:
        res = "R"
    elif bool(np.any(with_e & is_t)) and len(surv_e) == 1:
        res = "RE"
    else:
        res = "NR"
    out = dict(result=res, target_passes_NCVM=t_base, survivors_NCVM=[lab_y(x) for x in surv],
               survivors_NCVME=[lab_y(x) for x in surv_e])
    if res == "NR":
        out["failing"] = failing(T, target_jdn, e, vis, mwra_def, cnt)
    return out


def lab_y(jdn):
    y, m, d = cal.julian_from_jdn(int(jdn))
    return f"{d} {MN[m]} {cal.historical_year(y)}"


def failing(T, target_jdn, e, vis, mwra_def, cnt):
    """The target's failing criteria with their margins (positive = passes)."""
    i = np.nonzero(T["ti"] == target_jdn)[0]
    if i.size == 0:
        return {"N": "the target is not a candidate"}
    i = int(i[0])
    f = {}
    if not T[f"C_{cnt}"][i]:
        f["C"] = f"margin {int(T[f'C_margin_{cnt}'][i])} d"
    if not T[f"lead_{cnt}"][i] >= 90.0:
        f["V"] = f"lead {T[f'lead_{cnt}'][i]:.1f} min (needs 90.0)"
    if mwra_def == "vtx":
        dv = T[f"mw_any_delta_vtx_{cnt}"][i]
        if not abs(dv) <= 1.5:
            f["M"] = f"|Delta_vtx| {abs(dv):.2f} d (needs <= 1.5)"
    else:
        di = T[f"mw_any_delta_int_{cnt}"][i]
        if not abs(di) <= 1:
            f["M"] = f"|Delta_int| {abs(di):.0f} d (needs <= 1)"
    if vis == "av10" and not T[f"vis_av10_{cnt}"][i]:
        f["vis"] = f"Sun at Mercury's rising {T[f'merc_sun_alt_{cnt}'][i]:.2f} deg (needs <= -10)"
    if vis == "plsv" and not T[f"vis_plsv_{cnt}"][i]:
        f["vis"] = f"PLSV margin {T[f'plsv_margin_{cnt}'][i]:.2f} deg"
    if not T[f"E{e}_{cnt}"][i]:
        f["E"] = f"Ti{OFFS[cnt]['e']} = {lab(T[f'e_day_{cnt}'][i])} (needs 1 Apr..{E_HI[e][1]} Apr)"
    base = ncvm(T, cnt, mwra_def, vis)
    others = [lab_y(x) for x in T["ti"][base] if x != target_jdn]
    if others:
        f["not_unique"] = others
    return f


def t0_grid(T, target_jdn=TARGET_JDN):
    grid = {}
    for e in (4, 5, 6):
        for vis in ("off", "av10", "plsv"):
            for m in ("vtx", "int"):
                grid[f"E<={e}Apr/vis={vis}/MWRA_{m}"] = classify(T, target_jdn, e, vis, m)
    prim = grid[f"E<={PRIMARY['e']}Apr/vis={PRIMARY['vis']}/MWRA_{PRIMARY['mwra']}"]
    return grid, prim


# ----------------------------------------------------------- Table S2

def load_s2():
    with open(S2_TSV, encoding="utf-8") as f:
        L = [ln.rstrip("\n") for ln in f if ln.strip() and not ln.startswith("#")]
    h = L[0].split("\t")
    rows = []
    for ln in L[1:]:
        c = ln.split("\t")
        c += [""] * (len(h) - len(c))
        rows.append(dict(zip(h, c)))
    return rows


def _s2_date(ya, s):
    d, m = s.split("-")
    return cal.jdn_from_julian(ya, MON[m], int(d))


def _secs(t):
    p = list(map(int, t.split(":"))) + [0]
    return p[0] * 3600 + p[1] * 60 + p[2]


def s2_compare(exclude_target=False, dt=DT_BM):
    """A1-A3 and the S2 comparison of 3.2 step 9 on S2's own rows."""
    rows = load_s2()
    if exclude_target:
        rows = [r for r in rows if r["year"] != "1178"]
    lat, lon, _ = sky.site("bm")
    ya = np.array([1 - int(r["year"]) for r in rows])
    ti_s2 = np.array([_s2_date(y, r["Ti"]) for y, r in zip(ya, rows)], dtype=np.int64)
    # A1: the DE441 conjunction nearest each S2 Ti, by zone
    from odybench.lean.candidates import conjunctions
    match = {"UT+2": 0, "UT": 0, "LMT": 0}
    ti_de = np.zeros(len(rows), dtype=np.int64)
    for i, t in enumerate(ti_s2):
        a = cal.jd_from_julian(*cal.julian_from_jdn(int(t))) - 3 + dt / 86400
        cj = conjunctions(a, a + 6, eph="de441")
        u = cj - dt / 86400.0
        if u.size == 0:
            continue
        u = u[np.argmin(np.abs(u - (t - 0.5)))]
        ti_de[i] = cal.jdn_of_instant(u, 2.0)
        match["UT+2"] += int(ti_de[i] == t)
        match["UT"] += int(cal.jdn_of_instant(u, 0.0) == t)
        match["LMT"] += int(cal.jdn_of_instant(u, lon / 15.0) == t)
    # A2: Venus on S2's own Ti-5
    lv = sky.rise_lead(ti_s2 - 5, lat, lon, body="venus", dt=dt, eph="de441", zone_h=sky.UT2)
    vpass = set(int(r["year"]) for r, ld in zip(rows, lv["lead_min"]) if ld >= 90.0)
    s2v = set(int(r["year"]) for r in rows if r["c_diff"] == "O")
    dl = [(_secs(r["diff"]) / 60.0 - ld) for r, ld in zip(rows, lv["lead_min"]) if r["diff"]]
    offs = [(_secs(r["sunrise"]) / 60.0 - cal.julian_from_jd(sr, 2.0)[3] * 60.0)
            for r, sr in zip(rows, lv["sun_rise"]) if r["sunrise"]]
    # A3: MWRA (integer definition) on S2's own Ti-34
    md = ti_s2 - 34
    days_all = np.unique(np.concatenate([np.arange(t - SEARCH_D - HALF7 - 2, t + SEARCH_D + HALF7 + 3) for t in md]))
    days, r, mx = mercury_daily(days_all, lat, lon, dt)
    w = mwra(md, days, r, mx, "any")
    s2m = np.array([_s2_date(y, row["mwra"]) for y, row in zip(ya, rows)], dtype=np.int64)
    # A3 as measured [bm 5 M; check_mwra.py]: the DE441 maximum nearest S2's printed MWRA date
    near_s2 = mwra(s2m, days, r, mx, "any")["max_jdn"]
    exact = int(np.sum(near_s2 == s2m))
    within1 = int(np.sum(np.abs(near_s2 - s2m) <= 1))
    exact_t = int(np.sum(w["max_jdn"] == s2m))
    within1_t = int(np.sum(np.abs(w["max_jdn"] - s2m) <= 1))
    # Delta agreement and leap-day effects
    s2_delta = np.array([int(row["delta"]) for row in rows])
    true_delta_on_s2 = md - s2m
    leap = int(np.sum(true_delta_on_s2 != s2_delta))
    mpass_de = set(int(rr["year"]) for rr, d in zip(rows, w["delta_int"]) if abs(d) <= 1)
    n = len(rows)
    out = dict(
        rows=n, excluded_target_row=exclude_target,
        A1=dict(ti_match_ut2=match["UT+2"], ti_match_ut=match["UT"], ti_match_lmt=match["LMT"],
                need=">= 134 of 152", passes=(match["UT+2"] >= (134 if not exclude_target else 133))),
        A2=dict(venus_pass_set_equal=(vpass == s2v), sym_diff=sorted(vpass ^ s2v),
                lead_diff_sd_min=float(np.std(dl)), lead_diff_mean_min=float(np.mean(dl)),
                clock_offset_mean_min=float(np.mean(offs)), clock_offset_sd_min=float(np.std(offs)),
                n_timed=len(offs), passes=(vpass == s2v and float(np.std(dl)) <= 3.0)),
        A3=dict(exact=exact, within_1d=within1, need=">= 124 exact and >= 138 within 1 d of 152",
                definition="the DE441 rise-azimuth maximum nearest S2's printed MWRA date (as check_mwra.py measured it)",
                passes=(exact >= (124 if not exclude_target else 123) and within1 >= (138 if not exclude_target else 137)),
                nearest_to_Ti_minus_34=dict(exact=exact_t, within_1d=within1_t,
                                            note="B&M's own rule; reported beside")),
        delta_agreement=dict(s2_delta_vs_true_julian_on_s2_mwra_differ=leap,
                             note="S2 prints 365-day arithmetic; rows where true Julian arithmetic differs"),
        M_pass_on_s2_ti_de441_int=sorted(mpass_de, reverse=True),
    )
    return out


# ----------------------------------------------------------- A4, A5

def a4_checks(T, ut, dt=DT_BM):
    lat, lon, _ = sky.site("bm")
    i = np.nonzero(T["ti"] == TARGET_JDN)[0]
    res = {}
    if i.size:
        i = int(i[0])
        lead = float(T["lead_seq"][i])
        res["venus_lead_min"] = dict(value=round(lead, 2), want="103.6 +- 1", passes=abs(lead - 103.6) <= 1.0)
        res["conj_16Apr_UT2"] = dict(value=hm(ut[i]), want="12:25", passes=abs(cal.julian_from_jd(ut[i], 2.0)[3] * 60 - (12 * 60 + 25)) <= 1.0)
    j = np.nonzero(T["ti"] == cal.jdn_from_julian(-1177, 3, 18))[0]
    if j.size:
        j = int(j[0])
        res["conj_18Mar_UT2"] = dict(value=hm(ut[j]), want="03:31", passes=abs(cal.julian_from_jd(ut[j], 2.0)[3] * 60 - (3 * 60 + 31)) <= 1.0)
    eq = float(equinox_ut2([-1177], dt)[0])
    hh = cal.julian_from_jd(eq, 2.0)
    res["equinox_UT2"] = dict(value=f"{hh[2]} Apr {hm(eq)}" if hh[1] == 4 else cal.fmt(eq, "UT", 2.0),
                              want="within 10 min of 15:24 (1 Apr)",
                              passes=(hh[1] == 4 and hh[2] == 1 and abs(hh[3] * 60 - (15 * 60 + 24)) <= 10))
    tw = sky.evening_twilight(np.array([cal.jdn_from_julian(-1177, 3, 18)]), lat, lon, -12.0, dt, "de441",
                              zone_h=2.0)[0]
    res["sun_minus12_18Mar_UT2"] = dict(value=hm(tw), want="within 5 min of 19:38",
                                        passes=abs(cal.julian_from_jd(tw, 2.0)[3] * 60 - (19 * 60 + 38)) <= 5)
    res["passes"] = all(v["passes"] for v in res.values() if isinstance(v, dict))
    return res


def canon_elements(ymd=TARGET_YMD):
    """The NASA Besselian elements row for a date, from data/jsex/SE*.js."""
    y, m, d = ymd
    tag = f"//{y:5d} {m:2d} {d:2d}"
    for p in sorted(JSEX.glob("SE*.js")):
        txt = p.read_text(encoding="utf-8", errors="replace")
        k = txt.find(tag)
        if k < 0:
            continue
        body = txt[k + len(tag):]
        nxt = body.find("//")
        nums = [float(x) for x in body[:nxt if nxt > 0 else None].replace("\n", " ").split(",") if x.strip()
                and x.strip()[0] in "-0123456789"]
        return nums[:28], p.name
    return None, None


def a5_check(ymd=TARGET_YMD):
    """A5: gamma, the TD instant and the point of greatest eclipse from NASA's
    elements (2.3: gamma 0.5187, 17:57:28 TD, 32.7 N 12.7 E, Delta-T 28,590 s).
    The catalogue number (01966) and Saros (39/31) are not in data/jsex/."""
    el, fname = canon_elements(ymd)
    if el is None:
        return dict(passes=False, note="no element row found")
    jd_ge = el[0]
    t0 = el[1]
    jd_t0 = math.floor(jd_ge - 0.5) + 0.5 + t0 / 24.0
    t = (jd_ge - jd_t0) * 24.0
    pol = lambda a, n: sum(a[i] * t ** i for i in range(n))  # noqa: E731
    x, yy = pol(el[6:10], 4), pol(el[10:14], 4)
    d = math.radians(pol(el[14:17], 3))
    mu = pol(el[17:20], 3)
    dts = el[4]
    gamma = math.copysign(math.hypot(x, yy), yy)
    e2 = 0.00669438
    rho1 = math.sqrt(1 - e2 * math.cos(d) ** 2)
    y1 = yy / rho1
    sd1 = math.sin(d) / rho1
    cd1 = math.sqrt(1 - e2) * math.cos(d) / rho1
    z1 = math.sqrt(max(0.0, 1 - x * x - y1 * y1))
    phi1 = math.asin(y1 * cd1 + z1 * sd1)
    theta = math.degrees(math.atan2(x, -y1 * sd1 + z1 * cd1))
    lon_e = ((theta - mu + 0.00417807 * dts) + 180.0) % 360.0 - 180.0
    lat = math.degrees(math.atan(math.tan(phi1) / math.sqrt(1 - e2)))
    hh = cal.julian_from_jd(jd_ge)[3]
    td = f"{int(hh):02d}:{int(hh * 60) % 60:02d}:{int(round(hh * 3600)) % 60:02d}"
    ok = abs(gamma - 0.5187) <= 0.0002 and abs(lat - 32.7) <= 0.15 and abs(lon_e - 12.7) <= 0.15 \
        and abs(dts - 28590.0) < 0.5 and abs(hh * 3600 - (17 * 3600 + 57 * 60 + 28)) <= 2
    return dict(file=fname, gamma=round(gamma, 4), td=td, ge_lat=round(lat, 2), ge_lon_e=round(lon_e, 2),
                delta_t=dts, passes=bool(ok),
                note="catalogue 01966 / Saros 39 member 31 not checkable offline (no secat5 page for -1199..-1100)")


# ------------------------------------------------------- M sensitivity

def m_sensitivity(T, lat0=None, lon0=None):
    """The M pass set (MWRA_vtx, +-1.5 d, seq) of the C-passing candidates
    under h0 +- 0.1 deg, latitude 38.2..38.6, refraction on/off and the clock
    Delta-T +- 720 s (3.2 step 10)."""
    if lat0 is None:
        lat0, lon0, _ = sky.site("bm")
    sel = T["C_seq"]
    ti = T["ti"][sel]
    md = ti - 34
    days_all = np.unique(np.concatenate([np.arange(t - 12, t + 13) for t in md]))
    variants = {"base": dict()}
    for dh in (-0.1, 0.1):
        variants[f"h0{dh:+.1f}"] = dict(h0=sky.H0_PLANET + dh)
    for la in (38.2, 38.3, 38.5, 38.6):
        variants[f"lat{la}"] = dict(lat=la)
    variants["refraction_on"] = dict(refraction=True)
    for dd in (-720, 720):
        variants[f"dT{dd:+d}"] = dict(dt=DT_BM + dd)
    out = {}
    for name, v in variants.items():
        days, r, mx = mercury_daily(days_all, v.get("lat", lat0), lon0, v.get("dt", DT_BM),
                                    h0=v.get("h0"), refraction=v.get("refraction", False))
        w = mwra(md, days, r, mx, "any")
        p = np.abs(w["delta_vtx"]) <= 1.5
        ncvm_ = p & (T["lead_seq"][sel] >= 90.0)
        out[name] = dict(M=[lab_y(x) for x in ti[p]], NCVM_with_base_V=[lab_y(x) for x in ti[ncvm_]],
                         target_M=bool(np.any(p & (ti == TARGET_JDN))))
    return out


# ------------------------------------------------- the target side (r_Ody)

def target_side_pool(seeds=None):
    """r_Ody, the unmasked G_BM(v) (reported beside the masked values), the
    target's T_A membership and its held-out pool membership.  Stage 5 only."""
    from odybench.lean import candidates as Cn, readings as Rd, reach as Rc
    pool = Cn.load(mask_target=False)
    W = 136 * Rc.YEAR_D
    pa = Rd.passes(pool)
    surv = Rd.survivors(pool, pass_array=pa)
    is_t = pool.day0 == TARGET_JDN
    if not is_t.any():
        return dict(error="the target is not in the unmasked P_all")
    t = pool.jd_tt[is_t]
    r_ody = float(Rc.reach(t, surv, W)[0])
    r_t0b = float(Rc.reach(t, [surv[Rd.T0B_INDEX]], W)[0])
    mem = Rd.membership(pool, pa)
    it = int(np.nonzero(is_t)[0][0])
    year_ok = Cn.EPOCH_BAND[0] <= int(pool.year[it]) <= Cn.EPOCH_BAND[1]

    def cnt(s, p):
        return "both" if (s and p) else ("seq" if s else ("par" if p else None))
    ht = {
        "P_BM": dict(member=bool(mem["P_BM"][it]), count=cnt(mem["bm_seq"][it], mem["bm_par"][it])),
        "P_MWRA": dict(member=bool(mem["P_MWRA"][it]), count=cnt(mem["mwra_seq"][it], mem["mwra_par"][it])),
    }
    ht["P_BM_E"] = dict(ht["P_BM"], member=ht["P_BM"]["member"] and year_ok)
    ht["P_MWRA_E"] = dict(ht["P_MWRA"], member=ht["P_MWRA"]["member"] and year_ok)
    readings_passed = [Rd.READINGS[i].key for i in range(36) if pa[i, it]]
    G_unmasked = {}
    sd = json.loads((ROOT / "data" / "prereg" / "seeds.json").read_text(encoding="utf-8"))["purposes"]["G_bootstrap"]["seeds"]
    for v in ("v0", "v1", "v2", "v3", "v4", "v5"):
        ta = pool.T_A(v) & ~is_t
        rv = Rc.reach(pool.jd_tt[ta], surv, W)
        g = Rc.G(rv, pool.year[ta], Cn.CORE, slot=v, seeds=(sd["block_136"], sd["block_243"]), masked=False)
        G_unmasked[v] = dict(value=g["value"], lo=g["lo"], hi=g["hi"], n_A=g["n"], k_A=g["k"],
                             target_in_T_A=bool(pool.T_A(v)[it]))
    return dict(r_Ody=r_ody, reach_T0b_reading=r_t0b, readings_passed_by_target=readings_passed,
                heldout_target=ht, G_BM_unmasked=G_unmasked,
                target_daylight=bool(pool.rec["daylight"][it]),
                target_C_rel=dict(seq=bool(pool.cols["c_rel_seq"][it]), par=bool(pool.cols["c_rel_par"][it])))


# ------------------------------------------------------------ outputs

def write_table(T, ut, path):
    cols = ["year_BC", "Ti", "conj_UT2", "C_seq", "venus_rise", "sunrise", "lead_min", "V",
            "MWRA_int", "delta_int", "delta_vtx", "curv", "margin", "flat", "MWRA_morning_int",
            "delta_vtx_morning", "merc_sun_alt", "vis_av10", "vis_plsv", "Ti-11", "E4", "E5", "E6",
            "C_par", "lead_par", "delta_vtx_par", "E5_par"]
    lines = ["\t".join(cols)]
    for i in range(T["ti"].size):
        y = int(T["year"][i])
        mi = T["mw_any_max_jdn_seq"][i]
        mm = T["mw_morning_max_jdn_seq"][i]
        lines.append("\t".join(str(x) for x in [
            1 - y, lab(T["ti"][i]), hm(ut[i]), int(T["C_seq"][i]), hm(T["venus_rise_seq"][i]),
            hm(T["sunrise_seq"][i]), f"{T['lead_seq'][i]:.1f}", int(T["lead_seq"][i] >= 90),
            lab(mi) if mi > 0 else "", f"{T['mw_any_delta_int_seq'][i]:.0f}", f"{T['mw_any_delta_vtx_seq'][i]:.3f}",
            f"{T['mw_any_curv_seq'][i]:.4f}", f"{T['mw_any_margin_seq'][i]:.5f}", int(T["mw_any_flat_seq"][i]),
            lab(mm) if mm > 0 else "", f"{T['mw_morning_delta_vtx_seq'][i]:.3f}",
            f"{T['merc_sun_alt_seq'][i]:.2f}", int(T["vis_av10_seq"][i]), int(T["vis_plsv_seq"][i]),
            lab(T["e_day_seq"][i]), int(T["E4_seq"][i]), int(T["E5_seq"][i]), int(T["E6_seq"][i]),
            int(T["C_par"][i]), f"{T['lead_par'][i]:.1f}", f"{T['mw_any_delta_vtx_par'][i]:.3f}",
            int(T["E5_par"][i])]))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(with_target_pool=True):
    t0 = time.time()
    OUT.mkdir(parents=True, exist_ok=True)
    tt, ut, ti = t0b_candidates()
    T = t0b_table(ti, ut)
    grid, prim = t0_grid(T)
    T0_pass = bool(prim["target_passes_NCVM"])
    res = dict(stage="target", T0_pass=T0_pass, T0=prim["result"], primary_cell=prim,
               n_candidates=int(ti.size), n_candidates_expected=1683, grid=grid)
    for cnt in ("par",):
        res["parallel_reckoning"] = {f"E<={e}Apr/MWRA_vtx": classify(T, TARGET_JDN, e, "off", "vtx", cnt) for e in (4, 5, 6)}
    res["MWRA_morning_only_beside"] = dict(
        NCVM=[lab_y(x) for x in T["ti"][ncvm(T, "seq", "vtx", "off", side="morning")]])
    years = np.unique(T["year"])
    eq = equinox_ut2(years)
    res["equinox_UT2"] = {int(y): cal.fmt(float(e), "UT", 2.0) for y, e in zip(years, eq)
                          if np.any(T["C_seq"][T["year"] == y])}
    res["regression"] = dict(S2=s2_compare(False), A4=a4_checks(T, ut), A5=a5_check())
    res["M_sensitivity"] = m_sensitivity(T)
    write_table(T, ut, OUT / "candidates.tsv")
    if with_target_pool:
        res.update(target_side_pool())
    res["runtime_s"] = round(time.time() - t0, 1)
    (OUT / "t0.json").write_text(json.dumps(res, indent=1, ensure_ascii=False, default=_js), encoding="utf-8")
    txt = [f"T0 (DESIGN 3.2-3.5), DE441, clock Delta-T {DT_BM} s, site bm",
           f"candidates {ti.size} (expected 1,683)",
           f"T0_pass = {T0_pass}; T0 (primary cell E<=5 Apr, vis off, MWRA_vtx +-1.5 d) = {prim['result']}"]
    for k, v in grid.items():
        txt.append(f"  {k:32s} {v['result']:3s}  NCVM {v['survivors_NCVM']}  NCVME {v['survivors_NCVME']}"
                   + (f"  failing {v.get('failing')}" if v["result"] == "NR" else ""))
    txt.append(f"A1-A3: {json.dumps(res['regression']['S2'], default=_js)}")
    txt.append(f"A4: {json.dumps(res['regression']['A4'], default=_js)}")
    txt.append(f"A5: {json.dumps(res['regression']['A5'], default=_js)}")
    if "r_Ody" in res:
        txt.append(f"r_Ody = {res['r_Ody']:.4f} (T0b reading alone {res['reach_T0b_reading']:.4f})")
    (OUT / "t0.out.txt").write_text("\n".join(txt) + "\n", encoding="utf-8")
    print("\n".join(txt))
    return res


def _js(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (np.bool_,)):
        return bool(o)
    raise TypeError(type(o))


# ------------------------------------------------------------ selftest

def selftest():
    """Synthetic T0 tables: the R / RE / NR logic, the tie rule of MWRA_int,
    the S2 parser and the canon element reader (no sky is computed)."""
    tj = TARGET_JDN
    other = cal.jdn_from_julian(-1188, 3, 18)
    third = cal.jdn_from_julian(-1150, 4, 2)

    def table(passes_e):
        ti = np.array([other, tj, third], dtype=np.int64)
        T = dict(ti=ti, year=np.asarray(cal.julian_from_jdn(ti)[0]))
        for cnt in OFFS:
            T[f"C_{cnt}"] = np.array([True, True, False])
            T[f"C_margin_{cnt}"] = np.array([1, 1, -3])
            T[f"lead_{cnt}"] = np.array([100.9, 103.6, 120.0])
            for side in ("any", "morning"):
                T[f"mw_{side}_delta_vtx_{cnt}"] = np.array([0.2, 0.7, 0.1])
                T[f"mw_{side}_delta_int_{cnt}"] = np.array([0.0, 1.0, 0.0])
            T[f"vis_av10_{cnt}"] = np.array([True, True, True])
            T[f"vis_plsv_{cnt}"] = np.array([True, False, True])
            T[f"plsv_margin_{cnt}"] = np.array([1.0, -0.5, 1.0])
            T[f"merc_sun_alt_{cnt}"] = np.array([-17.1, -13.2, -12.0])
            T[f"e_day_{cnt}"] = ti - 11
            for n in (4, 5, 6):
                T[f"E{n}_{cnt}"] = np.array([False, passes_e[n], False])
        return T
    T = table({4: False, 5: True, 6: True})
    g, prim = t0_grid(T)
    assert prim["result"] == "RE" and prim["target_passes_NCVM"], prim
    assert g["E<=4Apr/vis=off/MWRA_vtx"]["result"] == "NR"
    assert "E" in g["E<=4Apr/vis=off/MWRA_vtx"]["failing"]
    assert g["E<=5Apr/vis=plsv/MWRA_vtx"]["result"] == "NR"          # target fails PLSV
    T["C_seq"][0] = False                                              # make the target unique
    g, prim = t0_grid(T)
    assert prim["result"] == "R", prim
    # MWRA_int ties resolve to the earlier maximum
    mx = np.zeros(2, dtype=sky.AZMAX_DTYPE)
    mx["day_jdn"] = [100, 104]
    mx["jd_ut"] = [99.7, 103.7]
    days = np.arange(90, 115)
    r = dict(jd_ut=days - 0.3)
    w = mwra(np.array([102]), days, r, mx, "any")
    assert w["max_jdn"][0] == 100 and w["delta_int"][0] == 2.0, w
    rows = load_s2()
    assert len(rows) == 152 and rows[0]["year"] == "1251"
    el, fname = canon_elements()
    assert el is not None and len(el) == 28
    a5 = a5_check()
    print(f"[reproduce selftest] grid logic ok; S2 rows {len(rows)}; A5 from {fname}: gamma {a5['gamma']}, "
          f"GE {a5['ge_lat']} N {a5['ge_lon_e']} E at {a5['td']} TD -> {'pass' if a5['passes'] else 'FAIL'}")
    assert a5["passes"], a5
    print("[reproduce selftest] PASS")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--s2-replay", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--no-target-pool", action="store_true", help="skip r_Ody and the unmasked pool")
    ap.add_argument("--no-freeze-check", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        selftest()
    elif a.s2_replay:
        res = s2_compare(exclude_target=True)
        rec = ROOT / "results" / "build-L1"
        rec.mkdir(parents=True, exist_ok=True)
        (rec / "s2_replay_without_1178.json").write_text(json.dumps(res, indent=1, default=_js), encoding="utf-8")
        print(json.dumps(res, indent=1, default=_js))
    elif a.run:
        if not (a.no_freeze_check or freeze_tag_exists("prereg-2")):
            sys.exit("reproduce.py reads the target: run it after the second freeze (git tag prereg-2), "
                     "or pass --no-freeze-check")
        run(with_target_pool=not a.no_target_pool)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
