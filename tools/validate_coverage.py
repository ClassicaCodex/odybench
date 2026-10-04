"""
Validate the ephemeris coverage added on 2026-10-04 (data-acquisition task)
and show that adding it changed no computed value.

    cd C:\\Projects\\odybench && py tools/validate_coverage.py > results/data-acquisition/validate_coverage.out.txt

Sections
  1. Coverage of every excerpt, in the order odybench.ephem.kernel() prefers them.
  2. kernel() choice: the new rule (shortest covering excerpt) picks the same
     file as the old rule (first covering file by name) for every request the
     old excerpts could serve.
  3. Record identity: each narrow excerpt's Chebyshev records are bit-identical
     to the matching slice of the long excerpt of the same ephemeris.
  4. Position identity: every segment evaluated from the narrow and the long
     excerpt at 2,000 random instants gives bit-identical vectors.
  5. Before/after: a battery of odybench.ephem results computed with the
     module as it was before this task (results/data-acquisition/ephem_orig.py)
     and as it is now: altaz, elongations, Besselian elements, greatest
     eclipse, local circumstances, a DE431 totality window, new moons and the
     four Hipparcos stars.  Required: identical floats.
  6. DE441 vs DE431 over the new span: the Moon's along-track difference
     follows the published-in-the-dossier law +0.00335" T^3 (research-ephemeris
     sect. 5.3), which shows the long DE431 excerpts are DE431 and the long
     DE441 excerpt is DE441.
  7. JPL Horizons spot checks for the Sun, Moon, Venus and Mercury at four
     dates spread over -1999..+200 (topocentric Ithaki, airless, Horizons'
     own TDB-UT used as Delta-T; responses cached in data/ephem/horizons/).
     Tolerances fixed before the comparison: astrometric Sun/Venus/Mercury
     < 0.01"; elongation < 1"; Moon astrometric < 3" and az/el < |GMST82 -
     GMST(Vondrak)| + 20" (Horizons uses the IAU 1982 sidereal time; the
     difference is printed and is the expected az/el residual).
  8. Calendar: JPL Horizons' own calendar dates for 300 random UT instants in
     -1999..+500 against odybench.calendar (cached).
  9. Stars: data/stars.json reproduces ephem.HIP_STARS for the four legacy
     stars, and every key in stars.json can be observed.
"""
from __future__ import annotations

import math
import sys
import time
import types
import urllib.parse
import urllib.request
from pathlib import Path

import erfa
import numpy as np
from jplephem.spk import SPK

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from odybench import ephem as E          # noqa: E402
from odybench import calendar as C       # noqa: E402

HZ = ROOT / "data" / "ephem" / "horizons"
T0 = time.time()
CHECKS = []
rng = np.random.default_rng(20261004)


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    return ok


def hdr(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def load_orig():
    """The module as it was before this task, loaded under another name with
    ROOT pointing at the project (the copy lives in results/)."""
    src = (ROOT / "results" / "data-acquisition" / "ephem_orig.py").read_text(encoding="utf-8")
    src = src.replace("ROOT = Path(__file__).resolve().parents[1]", f"ROOT = Path(r'{ROOT}')")
    mod = types.ModuleType("ephem_orig")
    mod.__file__ = str(ROOT / "results" / "data-acquisition" / "ephem_orig.py")
    sys.modules["ephem_orig"] = mod
    exec(compile(src, mod.__file__, "exec"), mod.__dict__)
    return mod


# ======================================================================
hdr("1. Coverage (kernel() preference order: shortest span first)")
for d in (E.EPHEM_DIR, E.EPHEM_DIR / "de431"):
    print(f"{d.relative_to(ROOT)}:")
    for name, jd0, jd1, tg in E.coverage(d):
        y0, m0, d0, _ = C.julian_from_jd(jd0)
        y1, m1, d1, _ = C.julian_from_jd(jd1)
        print(f"  {name:28s} JD {jd0:10.1f}..{jd1:10.1f}  {y0:+05d}-{m0:02d}-{d0:02d}..{y1:+05d}-{m1:02d}-{d1:02d}"
              f" (Julian)  {(jd1 - jd0) / 365.25:7.1f} yr  targets {tg}")
long441 = [r for r in E.coverage(E.EPHEM_DIR) if r[0] == "de441_m2060_p0241.bsp"][0]
check("DE441 long excerpt covers -2060-01-01..+241-01-01 (Julian), 11 targets",
      long441[1] <= C.jd_from_julian(-2060, 1, 1) and long441[2] >= C.jd_from_julian(241, 1, 1)
      and long441[3] == [1, 2, 3, 4, 5, 6, 10, 199, 299, 301, 399])

# ======================================================================
hdr("2. kernel() choice, new rule vs old rule")


# the excerpts that existed before this task (research-ephemeris, 2026-10-03)
OLD_FILES = {"de441_m1320_m1030.bsp", "de441_m0762_eclipse.bsp", "de441_m0584_eclipse.bsp", "de441_m0708_eclipse.bsp",
             "de441_m0135_eclipse.bsp", "de431_m1320_m1030.bsp", "de431_m0762_eclipse.bsp", "de431_m0708_eclipse.bsp",
             "de431_m0135_eclipse.bsp"}


def old_choice(directory, jd_lo, jd_hi, want):
    """The pre-task rule (first covering file in name order) over the pre-task files."""
    for jd0, jd1, targets, name, k in E._kernels(directory):
        if name in OLD_FILES and jd0 <= jd_lo and jd_hi <= jd1 and want <= targets:
            return name
    return None


def new_choice(directory, jd_lo, jd_hi, want):
    best = None
    for jd0, jd1, targets, name, k in E._kernels(directory):
        if jd0 <= jd_lo and jd_hi <= jd1 and want <= targets:
            if best is None or (jd1 - jd0, name) < best[0]:
                best = ((jd1 - jd0, name), name)
    return best[1] if best else None


n_same = n_req = n_newonly = 0
for d in (E.EPHEM_DIR, E.EPHEM_DIR / "de431"):
    narrow = [(jd0, jd1, t, n) for jd0, jd1, t, n, _ in E._kernels(d) if n in OLD_FILES]
    for jd0, jd1, t, n in narrow:
        for _ in range(500):
            a = rng.uniform(jd0, jd1)
            b = min(jd1, a + rng.exponential(2.0))
            want = {3, 10, 301, 399} if len(t) <= 4 else set(rng.choice(sorted(t), size=3, replace=False).tolist())
            n_req += 1
            o, nw = old_choice(d, a, b, want), new_choice(d, a, b, want)
            n_same += (o == nw)
        # requests the old files cannot serve
    for _ in range(500):
        a = rng.uniform(C.jd_from_julian(-2050, 1, 1), C.jd_from_julian(230, 1, 1))
        want = {3, 10, 301, 399}
        if old_choice(d, a, a + 1, want) is None and new_choice(d, a, a + 1, want) is not None:
            n_newonly += 1
# also: E.kernel must agree with new_choice
k_ok = True
for jd in (C.jd_from_julian(-1177, 4, 16), C.jd_from_julian(-762, 6, 15), C.jd_from_julian(-1999, 6, 12),
           C.jd_from_julian(200, 1, 1)):
    k = E.kernel(jd)
    nm = new_choice(E.EPHEM_DIR, jd, jd, {3, 10, 301, 399})
    k_ok &= any(k is kk and n == nm for _, _, _, n, kk in E._kernels(E.EPHEM_DIR))
print(f"requests inside the old excerpts: {n_req}; same file chosen by both rules: {n_same}")
print(f"random 1-day requests in -2050..+230 that only the new excerpts can serve: {n_newonly} of 1000 (DE441 and DE431)")
check("kernel(): new rule picks the old file for every request the old files serve", n_same == n_req, f"{n_same}/{n_req}")
check("kernel() implements the shortest-span rule", k_ok)

# ======================================================================
hdr("3. Chebyshev records: narrow excerpts vs the long excerpt of the same ephemeris")
PAIRS = [(E.EPHEM_DIR / n, E.EPHEM_DIR / "de441_m2060_p0241.bsp") for n in
         ("de441_m1320_m1030.bsp", "de441_m0762_eclipse.bsp", "de441_m0584_eclipse.bsp",
          "de441_m0708_eclipse.bsp", "de441_m0135_eclipse.bsp")]
D431 = E.EPHEM_DIR / "de431"
PAIRS += [(D431 / n, D431 / "de431_m2060_p0001.bsp") for n in
          ("de431_m1320_m1030.bsp", "de431_m0762_eclipse.bsp", "de431_m0708_eclipse.bsp",
           "de431_m0135_eclipse.bsp", "de431_m1339_eclipse.bsp", "de431_m0647_eclipse.bsp")]
all_rec_ok = True
for narrow, long_ in PAIRS:
    sn, sl = SPK.open(str(narrow)), SPK.open(str(long_))
    segl = {(s.center, s.target): s for s in sl.segments}
    out = []
    for s in sn.segments:
        key = (s.center, s.target)
        if key not in segl:
            out.append(f"{s.target}:absent")
            continue
        i0, L0, c0 = s.load_array()
        i1, L1, c1 = segl[key].load_array()
        k = (i0 - i1) / L0
        ok = (L0 == L1 and k == int(k) and c1.shape[0] == c0.shape[0] and c1.shape[2] == c0.shape[2]
              and np.array_equal(c1[:, int(k):int(k) + c0.shape[1], :], c0))
        all_rec_ok &= ok
        out.append(f"{s.target}:{'same' if ok else 'DIFF'}({c0.shape[1]})")
    print(f"  {narrow.name:26s} vs {long_.name:24s} " + " ".join(out))
    sn.close()
    sl.close()
check("records of every narrow excerpt are bit-identical to the long excerpt's", all_rec_ok)

# ======================================================================
hdr("4. Segment evaluation at random instants: narrow vs long excerpt")
all_pos_ok = True
for narrow, long_ in PAIRS:
    sn, sl = SPK.open(str(narrow)), SPK.open(str(long_))
    segl = {(s.center, s.target): s for s in sl.segments}
    worst = 0.0
    for s in sn.segments:
        if (s.center, s.target) not in segl:
            continue
        jd = rng.uniform(s.start_jd, s.end_jd, 2000)
        whole = np.floor(jd)
        frac = jd - whole
        p0 = s.compute(whole, frac)
        p1 = segl[(s.center, s.target)].compute(whole, frac)
        worst = max(worst, float(np.max(np.abs(p0 - p1))))
    all_pos_ok &= worst == 0.0
    print(f"  {narrow.name:26s} max |difference| over all segments and 2,000 instants: {worst:.3e} km")
    sn.close()
    sl.close()
check("positions from narrow and long excerpts are bit-identical", all_pos_ok)

# ======================================================================
hdr("5. Before/after: odybench.ephem results with the pre-task module vs now")
O = load_orig()
pairs = []                                       # (label, old value, new value)
la, lo = 38.37, 20.72
for name, (y, m, d, hs) in {"venus": (-1177, 4, 10, (3.0, 3.5, 4.0)), "mercury": (-1177, 3, 14, (16.5, 17.0)),
                            "sun": (-1177, 4, 16, (9.5, 10.0, 10.5)), "moon": (-1177, 4, 16, (10.0,)),
                            "arcturus": (-1177, 3, 18, (18.0,)), "alcyone": (-1177, 3, 18, (18.0,)),
                            "eps_boo": (-1177, 3, 18, (18.0,)), "eta_boo": (-1177, 3, 18, (18.0,))}.items():
    for h in hs:
        jd = E.jd_from_julian(y, m, d, h)
        for dt in ("smh2020", 28417.9):
            for prec in ("vondrak", "iau2006"):
                pairs.append((f"altaz {name} {y}-{m}-{d} {h}h dt={dt} {prec}",
                              O.altaz(name, jd, la, lo, dt=dt, precession=prec),
                              E.altaz(name, jd, la, lo, dt=dt, precession=prec)))
        if name in ("venus", "mercury", "moon"):
            pairs.append((f"elongation {name}", O.elongation(name, jd, la, lo), E.elongation(name, jd, la, lo)))
jd = E.jd_from_julian(-1177, 4, 16, 18.0)
pairs.append(("besselian -1177", tuple(float(v) for v in O.besselian(jd, dt=28590.0).values()),
              tuple(float(v) for v in E.besselian(jd, dt=28590.0).values())))
for y, m, d, h in ((-1177, 4, 16, 17.958), (-762, 6, 15, 14.13), (-584, 5, 28, 19.48), (-135, 4, 15, 9.45),
                   (-708, 7, 17, 12.48)):
    g0 = O.greatest_eclipse(E.jd_from_julian(y, m, d, h))
    g1 = E.greatest_eclipse(E.jd_from_julian(y, m, d, h))
    pairs.append((f"greatest eclipse {y}", (g0[0], float(g0[1]["gamma"])), (g1[0], float(g1[1]["gamma"]))))
lc0 = O.local_circumstances(la, lo, jd, dt="smh2020")
lc1 = E.local_circumstances(la, lo, jd, dt="smh2020")
pairs.append(("local circumstances Ithaki -1177 smh2020", tuple(v for v in lc0.values() if v is not None),
              tuple(v for v in lc1.values() if v is not None)))
with O.use_ephemeris(O.EPHEM_DIR / "de431"):
    lc0 = O.local_circumstances(la, lo, jd, dt=28543.0)
    w0 = O.totality_window(32.54, 44.42, E.jd_from_julian(-135, 4, 15, 9.46), 10800.0, 12600.0, step=200.0)
with E.use_ephemeris(E.EPHEM_DIR / "de431"):
    lc1 = E.local_circumstances(la, lo, jd, dt=28543.0)
    w1 = E.totality_window(32.54, 44.42, E.jd_from_julian(-135, 4, 15, 9.46), 10800.0, 12600.0, step=200.0)
pairs.append(("local circumstances Ithaki -1177 DE431", tuple(v for v in lc0.values() if v is not None),
              tuple(v for v in lc1.values() if v is not None)))
pairs.append(("DE431 totality window Babylon -135", tuple(w0[0]), tuple(w1[0])))
pairs.append(("new moons -1177 Mar-May", tuple(O.new_moons(E.jd_from_julian(-1177, 3, 1), E.jd_from_julian(-1177, 5, 31))),
              tuple(E.new_moons(E.jd_from_julian(-1177, 3, 1), E.jd_from_julian(-1177, 5, 31)))))
n_id = 0
for label, a, b in pairs:
    same = np.array_equal(np.asarray(a, dtype=float), np.asarray(b, dtype=float))
    n_id += same
    if not same:
        print(f"  DIFFERENT: {label}: {a} vs {b}")
print(f"{n_id}/{len(pairs)} results identical to the last bit "
      f"(e.g. {pairs[0][0]}: {pairs[0][2]}; {pairs[-3][0]}: {pairs[-3][2]})")
check("pre-task and current odybench.ephem give identical results", n_id == len(pairs), f"{n_id}/{len(pairs)}")

# ======================================================================
hdr("6. DE441 - DE431 Moon over the new span (expected +0.00335\" T^3 in elongation, sect. 5.3)")


def elong_moon_sun(jd_tt):
    t = E.time_tt(jd_tt, 0.0)
    k = E.kernel(jd_tt)
    e = k["earth"].at(t)
    m = e.observe(k["moon"]).apparent(deflectors=(10,))
    s = e.observe(k["sun"]).apparent(deflectors=(10,))
    return m.separation_from(s).degrees * 3600


# (a) as the dossier measured it: the shift of the instant of conjunction, times the elongation rate
# (the law was fitted to greatest-eclipse times, i.e. conjunctions); (b) the Sun-Moon separation 7 days
# after conjunction, for information (a different lunar phase).
print("   epoch      T(cy)  conj. DE441-DE431 (s)  along-track (\")  0.00335 T^3 (\")  ratio | separation at +7 d (\")")
ratios = []
for y in (-1999, -1500, -1000, -500, -100, 100, 200):
    jd = C.jd_from_julian(y, 6, 1, 12.0)
    nm441 = E.new_moons(jd, jd + 31)[0]
    with E.use_ephemeris(E.EPHEM_DIR / "de431"):
        nm431 = E.new_moons(jd, jd + 31)[0]
    # rate of the apparent ecliptic elongation (Moon - Sun longitude) at the conjunction, "/s
    rate = float(E._lon_diff_moon_sun(nm441 + 0.01) - E._lon_diff_moon_sun(nm441 - 0.01)) * 3600 / (0.02 * 86400.0)
    dsec = (nm441 - nm431) * 86400.0
    along = -dsec * rate                       # a later conjunction = the DE441 Moon lags
    T = (nm441 - 2451545.0) / 36525.0
    law = 0.00335 * T ** 3
    a7 = elong_moon_sun(nm441 + 7.0)
    with E.use_ephemeris(E.EPHEM_DIR / "de431"):
        b7 = elong_moon_sun(nm441 + 7.0)
    ratios.append(along / law)
    print(f"   {y:+05d}   {T:7.2f}   {dsec:+10.1f}          {along:+9.1f}        {law:+9.1f}      {along / law:5.2f} |"
          f" {a7 - b7:+9.1f}")
check("DE441-DE431 Moon matches the dossier's 0.00335 T^3 law at conjunctions (ratio 0.8-1.2, -1999..+200)",
      all(0.8 < r < 1.2 for r in ratios), "ratios " + " ".join(f"{r:.2f}" for r in ratios))


# ======================================================================
hdr("7. JPL Horizons spot checks over -1999..+200 (topocentric Ithaki, airless)")


def horizons(tag, params):
    HZ.mkdir(parents=True, exist_ok=True)
    f = HZ / f"{tag}.txt"
    if f.exists():
        return f.read_text(encoding="utf-8").split("\n", 1)[1]
    base = {"format": "text", "OBJ_DATA": "NO", "MAKE_EPHEM": "YES", "EPHEM_TYPE": "OBSERVER",
            "ANG_FORMAT": "DEG", "CAL_FORMAT": "JD", "TIME_DIGITS": "SECONDS",
            "EXTRA_PREC": "YES", "CSV_FORMAT": "YES", "APPARENT": "AIRLESS"}
    base.update(params)
    url = "https://ssd.jpl.nasa.gov/api/horizons.api?" + urllib.parse.urlencode(base)
    txt = urllib.request.urlopen(url, timeout=180).read().decode("utf-8")
    f.write_text(url + "\n" + txt, encoding="utf-8", newline="\n")
    return txt


def hz_rows(txt):
    body = txt.split("$$SOE")[1].split("$$EOE")[0]
    return [[c.strip() for c in ln.split(",")] for ln in body.strip().splitlines()]


SPOT = [  # tag, (y, m, d, first UT hour) -- dates chosen to spread over -1999..+200
    ("spot_m1999_06_12", (-1999, 6, 12, 2.5)),     # day of the Canon's first eclipse (-1999 Jun 12)
    ("spot_m1450_03_20", (-1450, 3, 20, 4.0)),
    ("spot_m0600_09_22", (-600, 9, 22, 16.0)),
    ("spot_p0200_01_15", (200, 1, 15, 5.0)),
]
NAME = {"10": "sun", "301": "moon", "299": "venus", "199": "mercury"}
worst = {}
gm_diff = {}
print(f"{'body':8s} {'UT':>20s} {'dT_HZ':>8s} | {'astrom':>7s} | {'appRA*':>7s} {'appDec':>7s} | {'dAz':>8s} {'dEl':>8s}"
      f" | {'elong':>8s} {'d elong':>7s} | {'GMST82-ours':>11s}")
for tag, (y, m, d, h0) in SPOT:
    jds = [C.jd_from_julian(y, m, d, h0 + 0.5 * i) for i in range(3)]
    for code, name in NAME.items():
        txt = horizons(f"{tag}_{code}", {"COMMAND": f"'{code}'", "CENTER": "'coord@399'", "COORD_TYPE": "GEODETIC",
                                         "SITE_COORD": f"'{lo},{la},0'", "TLIST": " ".join(f"'{j:.9f}'" for j in jds),
                                         "TLIST_TYPE": "JD", "QUANTITIES": "'1,2,4,20,23,30'"})
        for r in hz_rows(txt):
            jd = float(r[0])
            ra_a, de_a, ra_p, de_p, az, el_ = map(float, r[3:9])
            try:
                sot = float(r[11])
            except ValueError:
                sot = float("nan")
            dtb = float(r[13])
            t = E.time_ut(jd, dtb)
            kk = E.kernel(t.tt, ("sun", "earth", name))
            o = E.observer(la, lo, 0.0, kk).at(t)
            astro = o.observe(kk[E.BODY_NAMES[name]])
            app = astro.apparent(deflectors=(10,))
            ra1, de1, _ = astro.radec()
            ra2, de2, _ = app.radec(epoch="date")
            alt, azm, _ = app.altaz()
            sun = o.observe(kk["sun"]).apparent(deflectors=(10,))
            elo = app.separation_from(sun).degrees if name != "sun" else 0.0
            cosd = math.cos(math.radians(de_a))
            d_ast = math.hypot((ra1._degrees - ra_a) * cosd, de1.degrees - de_a) * 3600
            d_ra = (ra2._degrees - ra_p) * 3600 * math.cos(math.radians(de_p))
            d_de = (de2.degrees - de_p) * 3600
            d_az = ((azm.degrees - az + 180) % 360 - 180) * 3600 * math.cos(math.radians(el_))
            d_el = (alt.degrees - el_) * 3600
            d_elo = (elo - sot) * 3600 if name != "sun" else 0.0
            # sidereal-time convention difference: IAU 1982 GMST (Horizons) - ours (Vondrak-consistent GMST)
            ut1_whole = math.floor(jd)
            g82 = erfa.gmst82(ut1_whole, jd - ut1_whole)
            # ours: GMST = our (Vondrak-consistent) GAST minus the equation of the equinoxes, taken from
            # skyfield's IAU 2006 Time at the same instant: GMST_ours = GAST_ours - (GAST_sf - GMST_sf).
            t_sf = E.timescale(dtb).ut1_jd(jd)
            gmst_ours = (t.gast - (t_sf.gast - t_sf.gmst)) * 15.0
            dg = ((math.degrees(g82) - gmst_ours + 180) % 360 - 180) * 3600
            gm_diff[tag] = dg
            kind = "astrometric_moon" if name == "moon" else "astrometric"
            for kname, val in ((kind, d_ast), ("apparent", math.hypot(d_ra, d_de)),
                               (f"azel_{tag}", math.hypot(d_az, d_el)), ("elong", abs(d_elo))):
                worst[kname] = max(worst.get(kname, 0.0), val)
            print(f"{name:8s} {C.fmt(jd, 'UT')[:19]:>20s} {dtb:8.1f} | {d_ast:7.3f} | {d_ra:+7.2f} {d_de:+7.2f} |"
                  f" {d_az:+8.2f} {d_el:+8.2f} | {sot:8.4f} {d_elo:+7.2f} | {dg:+11.1f}")
print("columns: Horizons TDB-UT used as our Delta-T (s); |ours - HZ| astrometric ICRF (\"); apparent RA*/Dec of date"
      " ours(Vondrak) - HZ (\"); az*/el ours - HZ (\"); HZ S-O-T elongation (deg) and ours - HZ (\");"
      " IAU 1982 GMST minus our Vondrak-consistent GMST (\").")
check("Horizons spot checks: astrometric Sun/Venus/Mercury < 0.01\"", worst["astrometric"] < 0.01,
      f"{worst['astrometric']:.4f}\"")
check("Horizons spot checks: Moon astrometric < 3\"", worst["astrometric_moon"] < 3.0, f"{worst['astrometric_moon']:.3f}\"")
check("Horizons spot checks: elongation < 1\"", worst["elong"] < 1.0, f"{worst['elong']:.2f}\"")
for tag, _ in SPOT:
    check(f"Horizons spot checks {tag}: az/el within |GMST82 - ours| + 20\"",
          worst[f"azel_{tag}"] < abs(gm_diff[tag]) + 20.0,
          f"{worst[f'azel_{tag}']:.1f}\" vs |dGMST| {abs(gm_diff[tag]):.1f}\"")
print(f"worst: astrometric {worst['astrometric']:.4f}\", Moon {worst['astrometric_moon']:.3f}\", apparent of date"
      f" {worst['apparent']:.2f}\", elongation {worst['elong']:.2f}\"")

# ======================================================================
hdr("8. Calendar: JPL Horizons' calendar dates vs odybench.calendar")
jdn = np.sort(rng.integers(C.jdn_from_julian(-1999, 1, 1), C.jdn_from_julian(500, 12, 31) + 1, 300))
probe = [float(j) - 0.25 for j in jdn]            # 06:00 UT on the day with JDN j
probe += [C.jd_from_julian(-1177, 4, 16, 6.0), C.jd_from_julian(-1176, 2, 29, 6.0), C.jd_from_julian(0, 2, 29, 6.0),
          C.jd_from_julian(-1, 12, 31, 6.0), C.jd_from_julian(1, 1, 1, 6.0), C.jd_from_julian(-1999, 1, 1, 6.0)]
MON = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
n_ok = 0
bad = []
rows = []
for i in range(0, len(probe), 51):                 # 6 requests of <= 51 instants (a 306-instant TLIST got HTTP 502)
    chunk = probe[i:i + 51]
    for attempt in range(4):
        try:
            txt = horizons(f"calendar_probe_{i // 51}", {"COMMAND": "'10'", "CENTER": "'500@399'",
                                                        "TLIST": " ".join(f"'{j:.4f}'" for j in chunk),
                                                        "TLIST_TYPE": "JD", "QUANTITIES": "'20'", "CAL_FORMAT": "BOTH"})
            break
        except Exception as exc:                   # noqa: BLE001
            print(f"  Horizons retry {attempt + 1}: {exc!r}")
            time.sleep(10 * (attempt + 1))
    rows += hz_rows(txt)
for r in rows:
    cal, jdv = r[0], float(r[1])
    bc = cal.startswith("b")
    ys, ms, rest = cal.lstrip("b").split("-", 2)
    ds, hms = rest.split()
    yv = (1 - int(ys)) if bc else int(ys)
    want = (yv, MON.index(ms) + 1, int(ds))
    got = C.julian_from_jd(jdv)
    ok = got[:3] == want and abs(got[3] - 6.0) < 1e-6
    n_ok += ok
    if not ok:
        bad.append((cal, jdv, got))
print(f"{n_ok}/{len(probe)} Horizons calendar dates reproduced (Julian calendar, astronomical years; Horizons prints"
      f" 'b' + historical BC year); mismatches: {bad[:5]}")
for r in rows[-6:]:
    print(f"   Horizons {r[0]} = JD {r[1]}  ->  odybench.calendar {C.fmt(float(r[1]), 'UT')}")
check("calendar: Horizons dates reproduced", n_ok == len(probe), f"{n_ok}/{len(probe)}")

# ======================================================================
hdr("9. Stars: data/stars.json")
cat = E.stars_catalogue()
same = all(cat[k][0] == v[0] and cat[k][2:] == v[2:] for k, v in E.HIP_STARS.items())
print(f"stars.json keys: {sorted(cat)}")
print(f"legacy HIP_STARS reproduced by stars.json (HIP, ra, dec, plx, pm, rv): {same}")
check("stars.json reproduces ephem.HIP_STARS", same)
t = E.time_ut(E.jd_from_julian(-1177, 4, 10, 3.0))
alts = {k: float(E.apparent(k, t, la, lo).altaz()[0].degrees) for k in E.star_keys()}
print("altitudes at Ithaki, -1177 Apr 10 03:00 UT: " + ", ".join(f"{k} {v:+.1f}" for k, v in alts.items()))
check("every star key can be observed", all(np.isfinite(v) for v in alts.values()))

# ======================================================================
hdr("10. Summary")
for name, ok, detail in CHECKS:
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}  {detail}")
print(f"\n{sum(ok for _, ok, _ in CHECKS)}/{len(CHECKS)} passed; run time {time.time() - T0:.0f} s")
sys.exit(0 if all(ok for _, ok, _ in CHECKS) else 1)
