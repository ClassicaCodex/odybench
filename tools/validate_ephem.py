"""
Validate odybench.ephem against independent references and print every
number beside its reference value.

    cd C:\\Projects\\odybench && py tools/validate_ephem.py > results/validate_ephem.txt

References (all cached in data/ref or data/ephem/horizons after first run):
  * Vondrak, Capitaine & Wallace 2011, A&A 534 A22, App. A.5 test case.
  * HMNAO LVM tables (Addendum 2020 Delta-T, untimed-eclipse bounds S10).
  * NASA Five Millennium Canon (Espenak & Meeus 2006) catalogue rows and
    Besselian elements (VSOP87 / ELP-2000/82, n-dot -25.858).
  * NASA Six Millennium Catalog of Phases of the Moon (Espenak, Meeus' algorithms).
  * JPL Horizons API (DE441, IAU76/80 + Owen precession, its own Delta-T).
  * ERFA (pyerfa) eraPmsafe for stellar space motion.
"""
from __future__ import annotations

import math
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from odybench import ephem as E  # noqa: E402

REF = ROOT / "data" / "ref"
HZ = ROOT / "data" / "ephem" / "horizons"
ASEC = E.ASEC
T_START = time.time()
CHECKS = []          # (name, ok, detail)


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    return ok


def hdr(s):
    print()
    print("=" * 78)
    print(s)
    print("=" * 78)


def hms(jd):
    h = ((jd + 0.5) % 1.0) * 24
    s = round(h * 3600)
    return f"{s // 3600:02d}:{(s % 3600) // 60:02d}:{s % 60:02d}"


def dhms(seconds):
    sgn = "-" if seconds < 0 else "+"
    s = abs(seconds)
    return f"{sgn}{int(s // 3600)}h{int(s % 3600 // 60):02d}m{s % 60:04.1f}s"


SITES = {
    # name: (lat N, lon E) -- modern reference points, stated in the doc
    "Ithaki (Vathy)": (38.37, 20.72),
    "Kefalonia (Argostoli)": (38.18, 20.49),
    "Lefkada (town)": (38.83, 20.71),
}

# ======================================================================
hdr("0. Software and data")
import skyfield, jplephem, erfa, scipy  # noqa: E402
print(f"python {sys.version.split()[0]}  numpy {np.__version__}  scipy {scipy.__version__}")
print(f"skyfield {skyfield.__version__}  jplephem {jplephem.__version__}  "
      f"pyerfa {erfa.__version__} (ERFA {erfa.version.erfa_version})")
for jd0, jd1, targets, name, k in E._kernels():
    p = E.EPHEM_DIR / name
    print(f"{name:32s} {p.stat().st_size / 1e6:7.2f} MB  JD {jd0:.1f}..{jd1:.1f} "
          f"({E.julian_from_jd(jd0)[0]}..{E.julian_from_jd(jd1)[0]})  targets {sorted(targets)}")

# ======================================================================
hdr("1. Delta-T")
y1177 = float(E.julian_epoch(E.jd_from_julian(-1177, 4, 16)))
print(f"decimal year (Julian epoch) of -1177 Apr 16 = {y1177:.4f}")
print(f"{'model':22s} {'-1300':>9s} {'-1177.29':>9s} {'-1100':>9s} {'-1050':>9s}   sigma(-1177) [source of sigma]")
sig_src = {"smh2020": "HMNAO epsilon table", "smh2020_parabola": "+-0.6 tau^2 (eq. 5.1)",
           "smh2016_parabola": "+-0.6 tau^2 (eq. 4.1)", "em2006": "Huber 2000 (NASA page)",
           "em2006_canon": "Huber 2000 (NASA page)"}
for m in E.DT_MODELS:
    vals = [float(E.delta_t(y, m)) for y in (-1300, y1177, -1100, -1050)]
    print(f"{m:22s} " + " ".join(f"{v:9.0f}" for v in vals)
          + f"   {float(E.delta_t_sigma(y1177, m)):6.0f}  [{sig_src[m]}]")
print(f"{'skyfield builtin':22s} " + " ".join(f"{float(E.dt_skyfield(y)):9.0f}" for y in (-1300, y1177, -1100, -1050))
      + "   (no sigma)")
print(f"{'MS2004 0.8u^2 sigma':22s} {'':9s} {float(E.sigma_ms2004(y1177)):9.0f}   (formula stated for 1000 BC-AD 1200)")
print(f"n-dot correction -25.82 -> -25.858 at -1177: {float(E.ndot_correction(y1177, -25.858, -25.82)):+.1f} s;"
      f"  -26.00 -> -25.82: {float(E.ndot_correction(y1177, -25.82, -26.00)):+.1f} s")

print("\n1a. HMNAO extrapolated Delta-T table -2000..-800 (hours, 1 decimal) vs dt_smh2020:")
hm = {-2000: 12.8, -1900: 12.1, -1800: 11.4, -1700: 10.8, -1600: 10.2, -1500: 9.7, -1400: 9.1,
      -1300: 8.6, -1200: 8.1, -1100: 7.6, -1000: 7.1, -900: 6.6, -800: 6.1}
n_ceil = n_round = 0
for y, h in hm.items():
    v = float(E.dt_smh2020(y)) / 3600
    c = math.ceil(v * 10 - 1e-9) / 10
    r = round(v, 1)
    n_ceil += c == h
    n_round += abs(r - h) < 1e-9
    print(f"  {y:6d}  HMNAO {h:5.1f} h   ours {v:8.4f} h  rounded {r:5.1f}  rounded-up {c:5.1f}")
print(f"  entries reproduced: rounded-up {n_ceil}/13, rounded-nearest {n_round}/13")
check("HMNAO -2000..-800 table reproduced (rounded up)", n_ceil == 13, f"{n_ceil}/13")

print("\n1b. HMNAO spline table -720..+1600 (seconds, nearest 10) vs dt_smh2020:")
hm2 = {-720: 20370, -700: 20050, -600: 18470, -500: 16940, -400: 15470, -300: 14080, -200: 12770,
       -100: 11560, 0: 10440, 100: 9410, 200: 8420, 300: 7480, 400: 6540, 500: 5590, 600: 4650,
       700: 3760, 800: 2940, 900: 2230, 1000: 1650, 1100: 1220, 1200: 910, 1300: 680, 1400: 480,
       1500: 290, 1600: 110}
worst = max(abs(float(E.dt_smh2020(y)) - v) for y, v in hm2.items())
for y in (-720, -700, -600, -100, 1000, 1600):
    print(f"  {y:6d}  HMNAO {hm2[y]:6d}  ours {float(E.dt_smh2020(y)):9.1f}")
print(f"  max |ours - HMNAO| over 25 epochs = {worst:.1f} s (table rounded to 10 s)")
check("HMNAO -720..1600 spline table reproduced", worst <= 5.0, f"{worst:.1f} s")

s15 = (REF / "Table-S15.2020.txt").read_text()
rows = [list(map(float, r.split()[1:])) for r in s15.splitlines() if re.match(r"\s+\d+\s+-?\d+\.\d\s+-?\d+\.\d\s", r)]
k0, k1, a3, a2, a1, a0 = E._s15()
mism = 0
for i, r in enumerate(rows):
    K0, K1, A0, A1, A2, A3 = r
    mism += not np.allclose([K0, K1, A0, A1, A2, A3], [k0[i], k1[i], a0[i], a1[i], a2[i], a3[i]])
print(f"\n1c. skyfield-bundled S15 v2020 vs HMNAO file: {len(rows)} rows compared, {mism} mismatches")
check("S15 v2020 coefficients identical to HMNAO file", mism == 0 and len(rows) == 58, f"{len(rows)} rows")

print("\n1d. NASA Canon Delta-T (Espenak-Meeus with n-dot correction) vs dt_em2006_canon:")
for (y, m, d), ref in (((-1177, 4, 16), 28590.0), ((-762, 6, 15), 21210.6), ((-584, 5, 28), 18383.9),
                        ((-135, 4, 15), 11968.9), ((-708, 7, 17), 20330.0)):
    yy = y + (m - 0.5) / 12        # NASA's decimal year convention
    v = float(E.dt_em2006_canon(yy))
    print(f"  {y:5d}-{m:02d}-{d:02d}  Canon {ref:8.1f}  ours {v:8.1f}  diff {v - ref:+5.1f} s")
    check(f"Canon Delta-T {y}", abs(v - ref) < 1.0, f"{v - ref:+.1f} s")
print(f"  NASA phase table prints 07h59m for -1177; dt_em2006 (no n-dot corr.) = {dhms(float(E.dt_em2006(-1177 + 0.5 / 12)))}")


# ---------------------------------------------------------------- Horizons
def horizons(tag, params):
    """Cached Horizons API call; returns text."""
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
    f.write_text(url + "\n" + txt, encoding="utf-8")
    return txt


def hz_rows(txt):
    body = txt.split("$$SOE")[1].split("$$EOE")[0]
    return [[c.strip() for c in ln.split(",")] for ln in body.strip().splitlines()]


print("\n1e. JPL Horizons' own TDB-UT (quantity 30) at sample epochs:")
probe_years = [-2000, -1500, -1300, -1177, -1100, -1050, -800, -722, -700, -500]
probe_jd = [E.jd_from_julian(y, 1, 1) for y in probe_years]
txt = horizons("deltat_probe", {"COMMAND": "'10'", "CENTER": "'500@399'",
                                "TLIST": " ".join(f"'{j:.1f}'" for j in probe_jd), "TLIST_TYPE": "JD",
                                "QUANTITIES": "'30'"})
hz_dt = {}
for y, r in zip(probe_years, hz_rows(txt)):
    hz_dt[y] = float(r[-2])
J1825 = 2387627.5   # 1825 Jan 1.0 (Gregorian)
for y, j in zip(probe_years, probe_jd):
    T = (j - J1825) / 36525
    man = 65.62 + 31.351922682 * T * T
    print(f"  {y:6d}  Horizons {hz_dt[y]:9.1f}   manual formula(T from 1825.0) {man:9.1f}"
          f"   smh2020 {float(E.dt_smh2020(E.julian_epoch(j))):9.1f}")
ys = np.array([E.julian_epoch(j) for y, j in zip(probe_years, probe_jd) if y < -721], dtype=float)
vs = np.array([hz_dt[y] for y in probe_years if y < -721])
# fit v = a + b (y - y0)^2 with y0 free: linear least squares in (1, y, y^2)
A = np.vstack([np.ones_like(ys), ys, ys * ys]).T
c0, c1, c2 = np.linalg.lstsq(A, vs, rcond=None)[0]
y0 = -c1 / (2 * c2)
a_fit = c0 - c2 * y0 * y0
resid = vs - A @ np.array([c0, c1, c2])
print(f"  quadratic fit to Horizons before -721: {a_fit:.2f} + {c2 * 1e4:.6f} ((y - {y0:.2f})/100)^2,"
      f" max resid {np.max(np.abs(resid)):.3f} s")

# ======================================================================
hdr("2. Precession: Vondrak et al. 2011 (ERFA) vs paper, and vs IAU 2006")
epj = -1373.5959534565
ref_pecl = np.array([+0.00041724785764001342, -0.40495491104576162693, +0.91433656053126552350])
ref_pequ = np.array([-0.29437643797369031532, -0.11719098023370257855, +0.94847708824082091796])
ref_rp = np.array([[+0.68473390570729557360, +0.66647794042757610444, +0.29486714516583357655],
                   [-0.66669482609418419936, +0.73625636097440967969, -0.11595076448202158534],
                   [-0.29437643797369031532, -0.11719098023370257855, +0.94847708824082091796]])
ref_rpb = np.array([[+0.68473392912753224372, +0.66647788221176470103, +0.29486722236305384992],
                    [-0.66669476463873305255, +0.73625641199831485100, -0.11595079385100924091],
                    [-0.29437652267952261218, -0.11719099075396051880, +0.94847706065103424635]])


def ltpecl_py(epj, c7=198.296701):
    """Port of ERFA eraLtpecl (Vondrak 2011 Table 1 / corrigendum) with the
    Q_A coefficient C7 selectable: 198.296701 (corrigendum, ERFA) or
    198.296071 (the typo printed in the 2011 paper AND in its Fortran, which
    the paper's test values were computed with -- A&A 541, C1)."""
    pq = [[5851.607687, -0.1189000, -0.00028913, 0.000000101],
          [-1600.886300, 1.1689818, -0.00000020, -0.000000437]]
    per = [(708.15, -5486.751211, -684.661560, 667.666730, -5523.863691),
           (2309.00, -17.127623, 2446.283880, -2354.886252, -549.747450),
           (1620.00, -617.517403, 399.671049, -428.152441, -310.998056),
           (492.20, 413.442940, -356.652376, 376.202861, 421.535876),
           (1183.00, 78.614193, -186.387003, 184.778874, -36.776172),
           (622.00, -180.732815, -316.800070, 335.321713, -145.278396),
           (882.00, -87.676083, c7, -185.138669, -34.744450),
           (547.00, 46.140315, 101.135679, -120.972830, 22.885731)]
    t = (epj - 2000.0) / 100.0
    p = q = 0.0
    for P, a, b, c, d in per:
        w = 2 * math.pi * t / P
        p += math.cos(w) * a + math.sin(w) * c
        q += math.cos(w) * b + math.sin(w) * d
    for i in range(4):
        p += pq[0][i] * t ** i
        q += pq[1][i] * t ** i
    p *= ASEC
    q *= ASEC
    w = math.sqrt(max(0.0, 1 - p * p - q * q))
    e0 = 84381.406 * ASEC
    return np.array([p, -q * math.cos(e0) - w * math.sin(e0), -q * math.sin(e0) + w * math.cos(e0)])


def ltp_from_poles(peq, pec):
    eqx = np.cross(peq, pec)
    eqx /= np.linalg.norm(eqx)
    return np.array([eqx, np.cross(peq, eqx), peq])


def bias(rp):
    dx, de, dr = -0.016617 * ASEC, -0.0068192 * ASEC, -0.0146 * ASEC
    out = np.empty((3, 3))
    for i in range(3):
        out[i, 0] = rp[i, 0] - rp[i, 1] * dr + rp[i, 2] * dx
        out[i, 1] = rp[i, 0] * dr + rp[i, 1] + rp[i, 2] * de
        out[i, 2] = -rp[i, 0] * dx - rp[i, 1] * de + rp[i, 2]
    return out


pecl_typo = ltpecl_py(epj, 198.296071)
rp_typo = ltp_from_poles(erfa.ltpequ(epj), pecl_typo)
print(f"  {'routine':16s} {'ERFA (corrected) - paper':>26s} {'typo-C7 port - paper':>22s}")
for nm, got, typo, ref in (("ltp_PECL (A.1)", erfa.ltpecl(epj), pecl_typo, ref_pecl),
                           ("ltp_PEQU (A.2)", erfa.ltpequ(epj), erfa.ltpequ(epj), ref_pequ),
                           ("ltp_PMAT (A.3)", erfa.ltp(epj), rp_typo, ref_rp),
                           ("ltp_PBMAT (A.4)", erfa.ltpb(epj), bias(rp_typo), ref_rpb)):
    d = float(np.max(np.abs(np.asarray(got) - ref)))
    d2 = float(np.max(np.abs(np.asarray(typo) - ref)))
    print(f"  {nm:16s} {d:12.2e} ({d / ASEC * 1e3:6.3f} mas) {d2:12.2e} ({d2 / ASEC * 1e3:6.4f} mas)")
    check(f"Vondrak test case {nm} (typo-C7 port reproduces paper to double precision)", d2 < 1e-14, f"{d2:.1e}")
    check(f"Vondrak test case {nm} (ERFA within corrigendum effect)", d < 5e-9, f"{d:.1e}")
d_port = float(np.max(np.abs(ltpecl_py(epj) - erfa.ltpecl(epj))))
print(f"  port with corrected C7 vs ERFA eraLtpecl: {d_port:.1e}")
print("  (test epoch -1374 May 3 (Gregorian) 13:52:19.2 TT = JD 1219339.078; paper sect. A.5. The paper's test"
      " values were made with the C7 = 198.296071 typo that the 2012 corrigendum fixes; ERFA uses 198.296701."
      " The difference is < 1 mas.)")

print("\n2a. CIO locator s: quadrature along the IAU 2006 pole path + first-order nutation term, vs ERFA eraS06a")
print("    (full IAU 2006/2000A series).  Neglected: a 2.6 mas 18.6-yr term and the 3.8 mas/cy cross term.")
for y in (1700.0, 1800.0, 1900.0, 2000.0, 2100.0, 2200.0):
    jd = E.J2000 + (y - 2000) * 365.25
    s_int = float(E.cio_locator(y, "iau2006", erfa.pnm06a(jd, 0.0)))
    s_ref = float(erfa.s06a(jd, 0.0))
    print(f"  {y:7.1f}  ours {s_int / ASEC * 1e3:10.3f} mas   eraS06a {s_ref / ASEC * 1e3:10.3f} mas"
          f"   diff {(s_int - s_ref) / ASEC * 1e3:+.3f} mas")
    check(f"s vs eraS06a at {y} (< 20 mas)", abs(s_int - s_ref) / ASEC < 0.02, f"{(s_int - s_ref) / ASEC * 1e3:+.1f} mas")
print("  (1 s of Delta-T = 15 000 mas of Earth rotation; these residuals are irrelevant here.)")

print("\n2b. IAU 2006 (P03) vs Vondrak 2011 at selected epochs:")
print(f"  {'epoch':>9s} {'pole sep':>9s} {'rotation':>9s} {'EO V-P03':>9s} {'EO P03 int-poly':>15s} {'obl V-P03':>9s}  (arcsec)")
for y in (1000, 0, -500, -1000, -1177, -1300, -2000):
    jd = E.J2000 + (y - 2000) * 365.25
    pc = E.precession_compare(jd)
    print(f"  {y:9d} {pc['pole_sep_arcsec']:9.3f} {pc['rotation_arcsec']:9.3f} {pc['eo_diff_arcsec']:+9.3f}"
          f" {pc['eo_iau2006_integrated_arcsec'] - pc['eo_iau2006_poly_arcsec']:+15.3f}"
          f" {pc['obliquity_vondrak_arcsec'] - pc['obliquity_iau2006_arcsec']:+9.3f}")
pc1177 = E.precession_compare(E.jd_from_julian(-1177, 4, 16))
print(f"  -> at -1177 the hour-angle (sidereal time) difference is {pc1177['eo_diff_arcsec']:+.2f}\" "
      f"= {pc1177['eo_diff_arcsec'] / 15:+.3f} s of time; 1 s of Delta-T = 15.04\".")

print("\n2c. Mean sidereal time at -1177 Apr 16 10:00 UT1 (Delta-T 28417.6 s as Horizons), three formulations:")
jd_u = E.jd_from_julian(-1177, 4, 16, 10.0)
jd_t = jd_u + 28417.6 / 86400
g82 = float(erfa.gmst82(jd_u, 0.0))
g06 = float(erfa.gmst06(jd_u, 0.0, jd_t, 0.0))
tv = E.time_ut(jd_u, 28417.6, "vondrak")
era = 2 * math.pi * float(E.earth_rotation_angle(tv.whole, tv.ut1_fraction))
eov = float(erfa.eors(erfa.ltpb(float(E.julian_epoch(jd_t))), E.cio_locator(float(E.julian_epoch(jd_t)), "vondrak")))
gV = (era - eov) % (2 * math.pi)
dd = lambda a, b: ((a - b + math.pi) % (2 * math.pi) - math.pi) / ASEC
print(f"  GMST(IAU 1982, eraGmst82; used by Horizons and, presumably, the NASA Canon) - GMST(Vondrak-consistent) = {dd(g82, gV):+.1f}\"")
print(f"  GMST(IAU 2006, eraGmst06; skyfield)                                          - GMST(Vondrak-consistent) = {dd(g06, gV):+.1f}\"")
print("  (15\" = 1 s of time.  The IAU 1982 expression is a UT1 polynomial tied to IAU 1976 precession.)")

# ======================================================================
hdr("3. Stars: Hipparcos 2007 + space motion to -1177, both precession models")
jd_star = E.jd_from_julian(-1177, 3, 18, 18.0)      # an evening, UT
t_v = E.time_ut(jd_star, "smh2020", "vondrak")
t_i = E.time_ut(jd_star, "smh2020", "iau2006")
k = E.kernel(t_v.tt, ("sun", "earth", "venus"))
from skyfield.positionlib import Barycentric  # noqa: E402
ssb_at = Barycentric([0.0, 0.0, 0.0], [0.0, 0.0, 0.0], t=t_v)   # observer at the SSB
hip97 = {"alcyone": (19.35, -43.11, 8.87), "arcturus": (-1093.45, -1999.40, 88.85),
         "eps_boo": (-50.65, 20.00, 15.55), "eta_boo": (-60.95, -358.10, 88.17)}
lat, lon = SITES["Ithaki (Vathy)"]
print(f"epoch {E.fmt_jd(jd_star)}; Delta-T smh2020 {float(t_v.delta_t):.0f} s; site Ithaki {lat}N {lon}E")
print(f"{'star':10s} {'mu tot':>8s} {'shift':>7s} {'sky-ERFA':>9s} {'RV eff':>7s} {'HIP97':>7s} "
      f"{'RA date':>10s} {'Dec date':>10s} {'dRA*':>7s} {'dDec':>7s} {'alt':>8s} {'dAlt':>6s} {'dAz':>6s}")
STAR_NOTE = []
for key, (hip, name, ra, de, plx, pmra, pmde, rv) in E.HIP_STARS.items():
    st = E.star(key)
    mu = math.hypot(pmra, pmde) / 1000
    a_ssb = ssb_at.observe(st)
    ra_s, de_s, _ = a_ssb.radec()
    # ERFA independent space motion (eraPmsafe): pmr is d(RA)/dt, not mu_alpha*
    ra2, de2, *_ = erfa.pmsafe(math.radians(ra), math.radians(de),
                               pmra / 1000 * ASEC / math.cos(math.radians(de)), pmde / 1000 * ASEC,
                               plx / 1000, rv, E.HIP_EPOCH_JD_TT, 0.0, t_v.tdb, 0.0)
    u1 = np.array([math.cos(ra_s.radians) * math.cos(de_s.radians), math.sin(ra_s.radians) * math.cos(de_s.radians), math.sin(de_s.radians)])
    u2 = np.array([math.cos(ra2) * math.cos(de2), math.sin(ra2) * math.cos(de2), math.sin(de2)])
    d_erfa = math.degrees(math.atan2(np.linalg.norm(np.cross(u1, u2)), u1 @ u2)) * 3600
    u0 = np.array([math.cos(math.radians(ra)) * math.cos(math.radians(de)),
                   math.sin(math.radians(ra)) * math.cos(math.radians(de)), math.sin(math.radians(de))])
    shift = math.degrees(math.atan2(np.linalg.norm(np.cross(u0, u1)), u0 @ u1))
    st0 = E.Star(ra_hours=ra / 15, dec_degrees=de, ra_mas_per_year=pmra, dec_mas_per_year=pmde,
                 parallax_mas=plx, radial_km_per_s=0.0, epoch=E.HIP_EPOCH_JD_TT)
    r0, d0, _ = ssb_at.observe(st0).radec()
    p97 = hip97[key]
    st97 = E.Star(ra_hours=ra / 15, dec_degrees=de, ra_mas_per_year=p97[0], dec_mas_per_year=p97[1],
                  parallax_mas=p97[2], radial_km_per_s=rv, epoch=E.HIP_EPOCH_JD_TT)
    r97, d97, _ = ssb_at.observe(st97).radec()
    sep = lambda r1, dd1, r2, dd2: math.degrees(math.acos(min(1, math.sin(dd1.radians) * math.sin(dd2.radians)
                                                             + math.cos(dd1.radians) * math.cos(dd2.radians) * math.cos(r1.radians - r2.radians)))) * 3600
    rv_eff = sep(ra_s, de_s, r0, d0)
    h97 = sep(ra_s, de_s, r97, d97)
    obs = E.observer(lat, lon, 0.0, k)
    av = obs.at(t_v).observe(st).apparent(deflectors=(10,))
    ai = obs.at(t_i).observe(st).apparent(deflectors=(10,))
    rav, dev, _ = av.radec(epoch="date")
    rai, dei, _ = ai.radec(epoch="date")
    altv, azv, _ = av.altaz()
    alti, azi, _ = ai.altaz()
    dra = (rav._degrees - rai._degrees) * 3600 * math.cos(dev.radians)
    print(f"{key:10s} {mu:7.3f}\" {shift:6.3f}d {d_erfa:8.3f}\" {rv_eff:6.2f}\" {h97:6.2f}\" "
          f"{rav._degrees:10.4f} {dev.degrees:+10.4f} {dra:+7.2f} {(dev.degrees - dei.degrees) * 3600:+7.2f} "
          f"{altv.degrees:8.3f} {(altv.degrees - alti.degrees) * 3600:+6.2f} {(azv.degrees - azi.degrees) * 3600:+6.2f}")
    # expected skyfield-ERFA difference: ERFA (eraStarpm) adds the change of light time
    # as the star's distance changes (Roemer delay), skyfield's linear space motion does not
    yrs = (t_v.tdb - E.HIP_EPOCH_JD_TT) / 365.25
    lt_days = rv * yrs * 365.25 * 86400 / 299792.458 / 86400
    expect = mu * abs(lt_days) / 365.25
    STAR_NOTE.append(f"  {key}: light-time change over {yrs:.0f} yr = {lt_days:+.1f} d -> expected {expect:.3f}\", found {d_erfa:.3f}\"")
    check(f"star {key}: skyfield vs ERFA pmsafe (= Roemer light-time term)", abs(d_erfa - expect) < 0.01, f"{d_erfa:.3f}\" vs {expect:.3f}\"")
print("columns: total proper motion (\"/yr); angular shift J1991.25 -> -1177 (deg); skyfield vs ERFA eraPmsafe"
      " (\"); effect of radial velocity (\"); HIP1997 vs HIP2007 (\"); apparent RA/Dec of date (deg, Vondrak);"
      " dRA*=dRA cos dec and dDec, Vondrak - IAU2006 (\"); airless altitude (deg) at Ithaki and its"
      " Vondrak - IAU2006 difference in alt and az (\").")
for line in STAR_NOTE:
    print(line)

# ======================================================================
hdr("4. Solar eclipses vs NASA Five Millennium Canon (VSOP87/ELP-2000/82)")


def parse_bessel(path):
    t = path.read_text(encoding="utf-8")
    g = lambda pat: re.search(pat, t).group(1)
    el = dict(ge_tt=g(r"Instant of\s+(\d+:\d+:\d+) TDT"), ge_ut=g(r"\(=(\d+:\d+:\d+) UT\)"),
              gamma=float(g(r"Gamma = ([\d.\-]+)")), mag=float(g(r"Eclipse Magnitude = ([\d.]+)")),
              dt=float(g(r"T = ([\d.]+) s")), t0=float(g(r"([\d.]+) TDT  \(=t0\)")),
              tanf1=float(g(r"tan f1 = ([\d.]+)")), tanf2=float(g(r"tan f2 = ([\d.]+)")),
              lat=g(r"Latitude:\s+([\d.]+° [NS])"), lon=g(r"Longitude:\s+([\d.]+° [EW])"),
              alt=float(g(r"Altitude:\s+([\d.]+)")), az=float(g(r"Azimuth:\s+([\d.]+)")),
              dur=g(r"Central Duration = (\S+)"), width=float(g(r"Path Width = ([\d.]+)")))
    lines = t.splitlines()
    i = [n for n, ln in enumerate(lines) if re.match(r"\s+n\s+x\s+y", ln)][0]
    coef = []
    for ln in lines[i + 1:i + 5]:
        nums = [float(v) for v in ln.split()[1:]]
        coef.append(nums)
    names = ["x", "y", "d", "l1", "l2", "mu"]
    el["poly"] = {nm: [coef[n][j] if j < len(coef[n]) else 0.0 for n in range(4)] for j, nm in enumerate(names)}
    return el


def bes_eval(el, t_h):
    return {k: sum(c * t_h ** n for n, c in enumerate(v)) for k, v in el["poly"].items()}


def bes_local(el, lat, lon, dt, h_m=0.0):
    """Local circumstances from NASA's polynomial Besselian elements
    (Explanatory Supplement 1992 sect. 8.3 / Meeus 'Elements of Solar
    Eclipses'): independent of DE441 and of odybench.ephem's eclipse code."""
    phi = math.radians(lat)
    u = math.atan(0.99664719 * math.tan(phi))
    rs = 0.99664719 * math.sin(u) + h_m / 6378140 * math.sin(phi)
    rc = math.cos(u) + h_m / 6378140 * math.cos(phi)

    def geo(th):
        b = bes_eval(el, th)
        H = math.radians(b["mu"] + lon - 0.00417807 * dt)
        d = math.radians(b["d"])
        xi = rc * math.sin(H)
        eta = rs * math.cos(d) - rc * math.cos(H) * math.sin(d)
        zeta = rs * math.sin(d) + rc * math.cos(H) * math.cos(d)
        uu, vv = b["x"] - xi, b["y"] - eta
        L1 = b["l1"] - zeta * el["tanf1"]
        L2 = b["l2"] - zeta * el["tanf2"]
        return math.hypot(uu, vv), L1, L2, H, d
    from scipy.optimize import minimize_scalar, brentq
    hs = np.linspace(-4, 4, 961)
    m = [geo(h)[0] for h in hs]
    i = int(np.argmin(m))
    th = minimize_scalar(lambda h: geo(h)[0], bounds=(hs[max(i - 2, 0)], hs[min(i + 2, 960)]),
                         method="bounded", options={"xatol": 1e-8}).x
    mm, L1, L2, H, d = geo(th)
    mag = (L1 - mm) / (L1 + L2)
    total = L2 < 0 and mm < abs(L2)
    dur = 0.0
    if total:
        f = lambda h: geo(h)[0] - abs(geo(h)[2])
        dur = (brentq(f, th, th + 0.5) - brentq(f, th - 0.5, th)) * 3600
    alt = math.degrees(math.asin(math.sin(d) * math.sin(phi) + math.cos(d) * math.cos(H) * math.cos(phi)))
    jd_tt = E.jd_from_julian(*EV[el["key"]][:3]) + (el["t0"] + th) / 24.0
    return dict(jd_tt=jd_tt, jd_ut=jd_tt - dt / 86400, mag=mag, total=total, dur=dur, sun_alt=alt,
                margin=(abs(L2) - mm) if L2 < 0 else -1.0)


EV = {  # key: (y, m, d, NASA file stem)
    "-1177": (-1177, 4, 16, "-11770416"), "-762": (-762, 6, 15, "-07620615"),
    "-584": (-584, 5, 28, "-05840528"), "-135": (-135, 4, 15, "-01350415"), "-708": (-708, 7, 17, "-07080717")}
BES = {}
for key, (y, mo, d, stem) in EV.items():
    el = parse_bessel(REF / f"nasa_besselian_{stem}.txt")
    el["key"] = key
    BES[key] = el
    hh, mi, ss = map(int, el["ge_tt"].split(":"))
    jd_ge_ref = E.jd_from_julian(y, mo, d, hh + mi / 60 + ss / 3600)
    jge, b = E.greatest_eclipse(jd_ge_ref)
    b = E.besselian(jge, dt=el["dt"])
    t0 = E.jd_from_julian(y, mo, d, el["t0"])
    b0 = E.besselian(t0, dt=el["dt"])
    r0 = bes_eval(el, 0.0)
    # greatest-eclipse point: minimise topocentric Sun-Moon separation at jge
    from scipy.optimize import minimize
    tg = E.time_tt(jge, el["dt"])
    la0 = float(el["lat"].split("°")[0]) * (1 if "N" in el["lat"] else -1)
    lo0 = float(el["lon"].split("°")[0]) * (1 if "E" in el["lon"] else -1)
    res = minimize(lambda p: float(E._disc_geometry(tg, p[0], p[1], 0.0)[0]) / ASEC, [la0, lo0],
                   method="Nelder-Mead", options={"xatol": 1e-5, "fatol": 1e-5})
    lc = E.local_circumstances(res.x[0], res.x[1], jge, dt=el["dt"])
    dur_ref = el["dur"]
    dur_ref_s = int(dur_ref[:2]) * 60 + int(dur_ref[3:5])
    print(f"\n{key} {E.fmt_jd(jge, 'TT')}  (Canon Delta-T {el['dt']} s)")
    print(f"  greatest eclipse TT      ours {hms(jge)}   Canon {el['ge_tt']}   diff {(jge - jd_ge_ref) * 86400:+.0f} s")
    print(f"  gamma                    ours {float(b['gamma']):.4f}     Canon {el['gamma']:.4f}    diff {float(b['gamma']) - el['gamma']:+.4f}")
    print(f"  x, y at t0={el['t0']:.0f}h TT       ours {float(b0['x']):+.5f} {float(b0['y']):+.5f}   Canon {r0['x']:+.5f} {r0['y']:+.5f}")
    print(f"  d at t0 (deg)            ours {float(b0['d']):.5f}   Canon {r0['d']:.5f}")
    print(f"  mu at t0 (ephemeris HA)  ours {float(b0['mu_eph']):.4f}  Canon {r0['mu']:.4f}  diff {(float(b0['mu_eph']) - r0['mu']) * 3600:+.0f}\""
          f" = {(float(b0['mu_eph']) - r0['mu']) * 3600 / 15.041:+.1f} s of time")
    print(f"  GE point (Canon dT)      ours {res.x[0]:.2f}N {res.x[1]:.2f}E at {hms(float(tg.ut1))} UT   Canon {el['lat']} {el['lon']} at {el['ge_ut']} UT")
    print(f"  mag (ratio, k2) at GE    ours {lc['ratio']:.4f}     Canon {el['mag']:.4f}")
    print(f"  central duration at GE   ours {lc['duration_s']:.0f} s     Canon {dur_ref} ({dur_ref_s} s)")
    print(f"  Sun alt/az at GE         ours {lc['sun_alt_deg']:.1f} / {lc['sun_az_deg']:.1f}   Canon {el['alt']} / {el['az']}")
    check(f"{key} gamma vs Canon", abs(float(b['gamma']) - el['gamma']) < 0.003, f"{float(b['gamma']) - el['gamma']:+.4f}")
    check(f"{key} GE time vs Canon", abs(jge - jd_ge_ref) * 86400 < 300, f"{(jge - jd_ge_ref) * 86400:+.0f} s")
    check(f"{key} magnitude vs Canon", abs(lc['ratio'] - el['mag']) < 0.002, f"{lc['ratio'] - el['mag']:+.4f}")
    check(f"{key} duration vs Canon", abs(lc['duration_s'] - dur_ref_s) < 6, f"{lc['duration_s'] - dur_ref_s:+.0f} s")
    BES[key]["jge"] = jge

# ======================================================================
hdr("5. -1177 Apr 16: local circumstances at Ithaca, Kefalonia, Lefkada")
el = BES["-1177"]
jge = el["jge"]
print("5a. Same Delta-T (Canon 28590 s): ours (DE441, direct) vs NASA Besselian elements (independent algorithm)")
for nm, (la, lo) in SITES.items():
    lc = E.local_circumstances(la, lo, jge, dt=el["dt"])
    bl = bes_local(el, la, lo, el["dt"])
    print(f"  {nm:22s} max UT ours {hms(lc['jd_ut_max'])} NASA {hms(bl['jd_ut'])} ({(lc['jd_ut_max'] - bl['jd_ut']) * 86400:+.0f} s);"
          f" mag ours {lc['magnitude']:.4f} NASA {bl['mag']:.4f}; total {lc['total']}/{bl['total']};"
          f" Sun alt {lc['sun_alt_deg']:.1f}/{bl['sun_alt']:.1f}")

print("\n5b. Ithaki as a function of constant Delta-T (DE441, Vondrak precession):")
la, lo = SITES["Ithaki (Vathy)"]
print(f"  {'Delta-T':>8s} {'max UT':>9s} {'LAT':>6s} {'mag':>6s} {'obsc':>6s} {'total':>5s} {'dur s':>6s} {'Sun alt':>7s} {'Sun az':>7s}")
for dtv in range(26000, 32001, 500):
    lc = E.local_circumstances(la, lo, jge, dt=float(dtv))
    lat_h = lc["lat_hours"]
    print(f"  {dtv:8d} {hms(lc['jd_ut_max']):>9s} {int(lat_h):02d}:{int(lat_h % 1 * 60):02d} {lc['magnitude']:6.3f} {lc['obscuration']:6.3f}"
          f" {str(lc['total']):>5s} {lc['duration_s']:6.0f} {lc['sun_alt_deg']:7.1f} {lc['sun_az_deg']:7.1f}")

print("\n5c. Delta-T windows for TOTALITY (constant Delta-T, 0.5 s):")
WIN = {}
for nm, (la, lo) in SITES.items():
    w = E.totality_window(la, lo, jge, 24000.0, 33000.0, step=120.0)
    WIN[nm] = w
    # NASA-elements window for comparison
    from scipy.optimize import brentq
    f = lambda dtv: bes_local(el, la, lo, dtv)["margin"]
    grid = np.arange(24000.0, 33001.0, 120.0)
    vals = [f(g) for g in grid]
    nw = [brentq(f, grid[i], grid[i + 1], xtol=0.5) for i in range(len(grid) - 1) if (vals[i] > 0) != (vals[i + 1] > 0)]
    ws = ", ".join(f"[{a:.0f}, {b:.0f}] (width {b - a:.0f} s, mid {0.5 * (a + b):.0f})" for a, b in w) or "none"
    print(f"  {nm:22s} DE441: {ws}")
    print(f"  {'':22s} NASA elements: [{', '.join(f'{v:.0f}' for v in nw)}]")
print("  Delta-T models at -1177.29 (value +- stated 1 sigma):")
for m in E.DT_MODELS:
    v, s = float(E.delta_t(y1177, m)), float(E.delta_t_sigma(y1177, m))
    w = WIN["Ithaki (Vathy)"]
    if w:
        a, b = w[0]
        mid = 0.5 * (a + b)
        z = (mid - v) / s
        print(f"    {m:18s} {v:7.0f} +- {s:4.0f}   Ithaki window mid - model = {mid - v:+6.0f} s = {z:+.2f} sigma")
print(f"    {'Horizons TDB-UT':18s} {hz_dt[-1177]:7.0f} (at -1177 Jan 1)")

print("\n5d. Self-check: Delta-T change == longitude shift (exact in this formulation)")
lc_a = E.local_circumstances(la, lo, jge, dt=28000.0)
lc_b = E.local_circumstances(la, lo + 1.00273781191135448 * 15 * (28500.0 - 28000.0) / 3600, jge, dt=28500.0)
print(f"  mag {lc_a['magnitude']:.6f} vs {lc_b['magnitude']:.6f};  max TT diff {(lc_a['jd_tt_max'] - lc_b['jd_tt_max']) * 86400:+.3f} s")
check("Delta-T / longitude equivalence", abs(lc_a['magnitude'] - lc_b['magnitude']) < 1e-5, "")

print("\n5e. Which lunar ephemeris?  SMH's Delta-T is tied to DE430 / analytical j=2 (n-dot -25.82 / -26.00).")
print("    DE431 (same lunar model as DE430, long span) vs DE441, greatest-eclipse TT:")
offs = []
for key in ("-135", "-584", "-708", "-762", "-1177"):
    if key == "-584":
        continue           # no DE431 excerpt fetched for -584
    el_ = BES[key]
    j441 = el_["jge"]
    with E.use_ephemeris(E.EPHEM_DIR / "de431"):
        j431, b431 = E.greatest_eclipse(j441)
    b441 = E.besselian(j441)
    T = (float(E.julian_epoch(j441)) - 2000) / 100
    # relative Moon-Sun angular rate in apparent ecliptic longitude (arcsec/s):
    with E.use_ephemeris(E.EPHEM_DIR / "de431"):
        d1 = float(E._lon_diff_moon_sun(j441 + 0.01)) - float(E._lon_diff_moon_sun(j441 - 0.01))
    rate = d1 * 3600 / (0.02 * 86400)
    offs.append((T, (j441 - j431) * 86400, rate))
    print(f"  {key:6s} DE441 - DE431 = {(j441 - j431) * 86400:+7.1f} s   (Moon-Sun elongation rate {rate:.3f}\"/s ->"
          f" {(j441 - j431) * 86400 * rate:+6.1f}\" along-track);  gamma {float(b441['gamma']):.5f} vs {float(b431['gamma']):.5f}")
Ts = np.array([o[0] for o in offs])
dl = np.array([o[1] * o[2] for o in offs])
y_ = -dl        # Moon(DE441) - Moon(DE431) in elongation, arcsec (negative = DE441 Moon behind)
for lab, basis in (("0.5 b T^2", 0.5 * Ts ** 2), ("k T^3", Ts ** 3)):
    coef = float(np.dot(basis, y_) / np.dot(basis, basis))
    res_ = y_ - coef * basis
    print(f"  fit Moon(DE441) - Moon(DE431) = {lab}: coefficient {coef:+.5f}, residuals "
          + " ".join(f"{r_:+.1f}\"" for r_ in res_) + "  (T in Julian centuries from J2000)")
DT441_431 = {key: o[1] for key, o in zip(("-135", "-708", "-762", "-1177"), offs)}

print("\n5f. Totality windows at the three sites with DE431, and the chance of totality under each Delta-T model")
print("    (Gaussian with the model's stated sigma; window = constant Delta-T range giving totality):")
from math import erf
Phi = lambda z: 0.5 * (1 + erf(z / math.sqrt(2)))
WIN431 = {}
with E.use_ephemeris(E.EPHEM_DIR / "de431"):
    for nm, (la_, lo_) in SITES.items():
        WIN431[nm] = E.totality_window(la_, lo_, BES["-1177"]["jge"], 24000.0, 33000.0, step=120.0)
for nm in SITES:
    w1 = WIN[nm][0] if WIN[nm] else None
    w2 = WIN431[nm][0] if WIN431[nm] else None
    print(f"  {nm:22s} DE441 [{w1[0]:.0f}, {w1[1]:.0f}]   DE431 [{w2[0]:.0f}, {w2[1]:.0f}]   shift {w1[0] - w2[0]:+.0f}/{w1[1] - w2[1]:+.0f} s")
print(f"  {'P(total at site)':24s}" + "".join(f"{nm.split()[0] + ' ' + e:>17s}" for nm in SITES for e in ('441', '431')))
for m in E.DT_MODELS:
    v, s_ = float(E.delta_t(y1177, m)), float(E.delta_t_sigma(y1177, m))
    row = []
    for nm in SITES:
        for W in (WIN, WIN431):
            a, b = W[nm][0]
            row.append(Phi((b - v) / s_) - Phi((a - v) / s_))
    print(f"  {m:18s} {v:6.0f}+-{s_:4.0f}" + "".join(f"{p_:17.3f}" for p_ in row))
print("  (em2006/em2006_canon sigma is Huber's 1008 s; with MS2004's 0.8u^2 = 718 s the numbers change little)")

print("\n5g. Where the central line crosses Ithaki's meridian (20.72E), DE441 and DE431, by Delta-T:")
from scipy.optimize import minimize_scalar


def central_lat(lon_, dtv):
    f = lambda la_: E.local_circumstances(la_, lon_, BES["-1177"]["jge"], dt=dtv)["min_sep_arcsec"]
    grid_ = np.arange(28.0, 48.01, 1.0)
    vals_ = [f(g) for g in grid_]
    i_ = int(np.argmin(vals_))
    r_ = minimize_scalar(f, bounds=(grid_[max(i_ - 1, 0)], grid_[min(i_ + 1, len(grid_) - 1)]), method="bounded",
                         options={"xatol": 1e-4})
    return r_.x, r_.fun


for dtv in (28543.0 - 720, 28543.0, 28543.0 + 720, 29314.0):
    la1, sep1 = central_lat(20.72, dtv)
    with E.use_ephemeris(E.EPHEM_DIR / "de431"):
        la2, sep2 = central_lat(20.72, dtv)
    print(f"  Delta-T {dtv:7.0f}: central line at {la1:6.2f}N (DE441), {la2:6.2f}N (DE431);"
          f" Ithaki is {(38.37 - la1) * 111.2:+6.0f} / {(38.37 - la2) * 111.2:+6.0f} km north of it (along the meridian)")

# ======================================================================
hdr("6. Historical eclipses with observations: totality windows vs published Delta-T")
HIST = [
    ("-135", "Babylon", 32.54, 44.42, (11220, 12140), "SMH Table S10 v2020 (total at Babylon)"),
    ("-708", "Qufu (Lu)", 35.60, 116.99, (20160, 21100), "SMH Table S10 v2020 (total, China)"),
    ("-762", "Assur", 35.46, 43.26, None, "Assyrian eponym chronicle (no totality stated)"),
    ("-762", "Nineveh", 36.36, 43.15, None, "Assyrian eponym chronicle (no totality stated)"),
]
for key, nm, la, lo, bounds, src in HIST:
    el = BES[key]
    jge = el["jge"]
    yy = float(E.julian_epoch(jge))
    w = E.totality_window(la, lo, jge, float(E.dt_smh2020(yy)) - 4000, float(E.dt_smh2020(yy)) + 4000, step=120.0)
    f = lambda dtv: bes_local(el, la, lo, dtv)["margin"]
    c = float(E.dt_smh2020(yy))
    grid = np.arange(c - 4000, c + 4001, 120.0)
    vals = [f(g) for g in grid]
    from scipy.optimize import brentq
    nw = [brentq(f, grid[i], grid[i + 1], xtol=0.5) for i in range(len(grid) - 1) if (vals[i] > 0) != (vals[i + 1] > 0)]
    print(f"\n{key} {nm} ({la}N {lo}E)  [{src}]")
    print(f"  totality window DE441 (ours):   " + (", ".join(f"[{a:.0f}, {b:.0f}]" for a, b in w) or "none"))
    print(f"  totality window NASA elements: [{', '.join(f'{v:.0f}' for v in nw)}]")
    if bounds:
        print(f"  published SMH bounds:           [{bounds[0]}, {bounds[1]}]")
        if w:
            print(f"  DE441 - SMH: lower {w[0][0] - bounds[0]:+.0f} s, upper {w[0][1] - bounds[1]:+.0f} s")
        with E.use_ephemeris(E.EPHEM_DIR / "de431"):
            w431 = E.totality_window(la, lo, jge, c - 4000, c + 4000, step=120.0)
        print(f"  totality window DE431:          " + (", ".join(f"[{a:.0f}, {b:.0f}]" for a, b in w431) or "none"))
        if w431:
            print(f"  DE431 - SMH: lower {w431[0][0] - bounds[0]:+.0f} s, upper {w431[0][1] - bounds[1]:+.0f} s")
            check(f"{key} {nm} DE431 totality window vs SMH (< 60 s)",
                  abs(w431[0][0] - bounds[0]) < 60 and abs(w431[0][1] - bounds[1]) < 60,
                  f"{w431[0][0] - bounds[0]:+.0f}/{w431[0][1] - bounds[1]:+.0f} s")
    print(f"  Delta-T models: smh2020 {float(E.dt_smh2020(yy)):.0f} +- {float(E.sigma_smh2020(yy)):.0f};"
          f" em2006 {float(E.dt_em2006(yy)):.0f}; em2006_canon {float(E.dt_em2006_canon(yy)):.0f}")

# ======================================================================
hdr("7. New moons (conjunctions in apparent ecliptic longitude) vs NASA phase catalogue")
txt = (REF / "nasa_phases_-1199_-1100.txt").read_text(encoding="utf-8")
nasa_nm = []
cur = None
for ln in txt.splitlines():
    m = re.match(r"^(-\d{4})\s", ln)
    if m:
        cur = int(m.group(1))
    if cur in (-1178, -1177):
        mm = re.match(r"^(?:-\d{4})?\s+([A-Z][a-z]{2})\s+(\d+)\s+(\d\d):(\d\d)", ln)
        if mm and len(ln) > 10 and ln[8:26].strip():
            mon = E._MONTHS.index(mm.group(1)) + 1
            nasa_nm.append(E.jd_from_julian(cur, mon, int(mm.group(2)), int(mm.group(3)) + int(mm.group(4)) / 60))
dt_nasa = 7 * 3600 + 59 * 60       # table's Delta-T column, 07h59m for both years
ours = E.new_moons(E.jd_from_julian(-1178, 1, 1), E.jd_from_julian(-1176, 1, 1))
diffs = []
for j in nasa_nm:
    jt = j + dt_nasa / 86400
    o = min(ours, key=lambda x: abs(x - jt))
    diffs.append((o - jt) * 1440)
print(f"  {len(nasa_nm)} NASA new moons in -1178/-1177 matched to ours (TT); NASA UT + 07h59m (their Delta-T column)")
print(f"  ours - NASA (minutes): mean {np.mean(diffs):+.1f}, sd {np.std(diffs):.1f}, min {min(diffs):+.1f}, max {max(diffs):+.1f}")
print("  (NASA times are rounded to 1 min and computed with Meeus' truncated series; Delta-T column rounded to 1 min)")
nm_apr = min(ours, key=lambda x: abs(x - E.jd_from_julian(-1177, 4, 16, 18)))
print(f"  conjunction nearest the eclipse: {E.fmt_jd(nm_apr, 'TT')}")
ge_ours = BES["-1177"]["jge"]
gap = (nm_apr - ge_ours) * 1440
hh, mi, ss = map(int, BES["-1177"]["ge_tt"].split(":"))
ge_canon = E.jd_from_julian(-1177, 4, 16, hh + mi / 60 + ss / 3600)
nasa_apr = min(nasa_nm, key=lambda x: abs(x - E.jd_from_julian(-1177, 4, 16, 10))) + dt_nasa / 86400
print(f"  instrument check: our conjunction comes {gap:+.1f} min after our greatest eclipse; applying the same gap to the")
print(f"  Canon's own greatest eclipse ({BES['-1177']['ge_tt']} TD) predicts a Canon-consistent conjunction at"
      f" {hms(ge_canon + gap / 1440)} TD, but the phase catalogue gives {hms(nasa_apr)} TD:")
print(f"  NASA's two products disagree by {(nasa_apr - ge_canon - gap / 1440) * 1440:+.1f} min, i.e. most of the"
      f" {np.mean(diffs):+.1f} min offset is internal to the reference (Meeus' phase series without the Canon's"
      f" n-dot treatment), and ours - Canon-consistent = {(nm_apr - ge_canon - gap / 1440) * 1440:+.1f} min.")
check("new moons: scatter vs NASA phases < 1 min (offset explained above)", np.std(diffs) < 1.0, f"sd {np.std(diffs):.2f} min")
check("new moons: ours vs Canon-consistent conjunction < 5 min", abs((nm_apr - ge_canon - gap / 1440) * 1440) < 5,
      f"{(nm_apr - ge_canon - gap / 1440) * 1440:+.1f} min")

# ======================================================================
hdr("8. Planets, Sun, Moon vs JPL Horizons (topocentric Ithaki, airless)")
la, lo = SITES["Ithaki (Vathy)"]
SETS = [
    ("venus_mercury_m1177_04_10_dawn", ["299", "199"], [E.jd_from_julian(-1177, 4, 10, h) for h in (3.0, 3.5, 4.0)]),
    ("venus_mercury_m1177_03_14_dusk", ["299", "199"], [E.jd_from_julian(-1177, 3, 14, h) for h in (16.5, 17.0, 17.5)]),
    ("venus_mercury_m1210_06_01_dawn", ["299", "199"], [E.jd_from_julian(-1210, 6, 1, h) for h in (2.5, 3.0, 3.5)]),
    ("sun_moon_m1177_04_16_eclipse", ["10", "301"], [E.jd_from_julian(-1177, 4, 16, h) for h in (9.5, 10.0, 10.5)]),
]
NAME = {"299": "venus", "199": "mercury", "10": "sun", "301": "moon"}
worst = {}
print(f"{'body':8s} {'UT':>20s} {'dT_HZ':>8s} | {'astrom':>7s} | {'appRA*':>7s} {'appDec':>7s} | {'dAz':>7s} {'dEl':>7s}"
      f" | {'P03 dAz':>7s} {'P03 dEl':>7s} | {'elong':>8s} {'d elong':>7s} | {'el(HZ)':>8s} {'el smh':>8s}")
for tag, bodies, jds in SETS:
    for code in bodies:
        txt = horizons(f"{tag}_{code}", {"COMMAND": f"'{code}'", "CENTER": "'coord@399'", "COORD_TYPE": "GEODETIC",
                                          "SITE_COORD": f"'{lo},{la},0'", "TLIST": " ".join(f"'{j:.9f}'" for j in jds),
                                          "TLIST_TYPE": "JD", "QUANTITIES": "'1,2,4,20,23,30'"})
        for r in hz_rows(txt):
            jd = float(r[0])
            ra_a, de_a, ra_p, de_p, az, el_, delta, deldot = map(float, r[3:11])
            try:
                sot = float(r[11])
            except ValueError:
                sot = float("nan")
            dtb = float(r[13])
            name = NAME[code]
            res = {}
            for prec in ("vondrak", "iau2006"):
                t = E.time_ut(jd, dtb, prec)
                kk = E.kernel(t.tt, ("sun", "earth", name))
                o = E.observer(la, lo, 0.0, kk).at(t)
                astro = o.observe(kk[E.BODY_NAMES[name]])
                app = astro.apparent(deflectors=(10,))
                ra1, de1, dist = astro.radec()
                ra2, de2, _ = app.radec(epoch="date")
                alt, azm, _ = app.altaz()
                sun = o.observe(kk["sun"]).apparent(deflectors=(10,))
                elo = app.separation_from(sun).degrees if name != "sun" else 0.0
                res[prec] = (ra1._degrees, de1.degrees, ra2._degrees, de2.degrees, azm.degrees, alt.degrees, elo, dist.au)
            v = res["vondrak"]
            p = res["iau2006"]
            cosd = math.cos(math.radians(de_a))
            d_ast = math.hypot((v[0] - ra_a) * cosd, v[1] - de_a) * 3600
            d_ra = (v[2] - ra_p) * 3600 * math.cos(math.radians(de_p))
            d_de = (v[3] - de_p) * 3600
            d_az = ((v[4] - az + 180) % 360 - 180) * 3600 * math.cos(math.radians(el_))
            d_el = (v[5] - el_) * 3600
            p_az = ((p[4] - az + 180) % 360 - 180) * 3600 * math.cos(math.radians(el_))
            p_el = (p[5] - el_) * 3600
            d_elo = (v[6] - sot) * 3600 if name != "sun" else 0.0
            # altitude with our preferred Delta-T instead of Horizons'
            alt_smh, _ = E.altaz(name, jd, la, lo, dt="smh2020")
            for kname, val in (("astrometric" if name != "moon" else "astrometric_moon", d_ast), ("apparent", math.hypot(d_ra, d_de)),
                               ("azel", math.hypot(d_az, d_el)), ("elong", abs(d_elo))):
                worst[kname] = max(worst.get(kname, 0), val)
            ut = E.fmt_jd(jd)[:19]
            print(f"{name:8s} {ut:>20s} {dtb:8.1f} | {d_ast:7.3f} | {d_ra:+7.2f} {d_de:+7.2f} | {d_az:+7.2f} {d_el:+7.2f}"
                  f" | {p_az:+7.2f} {p_el:+7.2f} | {sot:8.4f} {d_elo:+7.2f} | {el_:8.3f} {alt_smh:8.3f}")
print("columns: Horizons TDB-UT used as our Delta-T (s); |ours - HZ| astrometric ICRF position (\");"
      " apparent RA* and Dec of date, ours(Vondrak) - HZ (\"); az* and el, ours(Vondrak) - HZ (\");"
      " the same with IAU 2006 precession; Horizons S-O-T elongation (deg) and ours - HZ (\", HZ prints 4 decimals = 0.36\");"
      " HZ elevation (deg) and ours with smh2020 Delta-T instead of Horizons' (deg).")
print(f"worst |diff|: astrometric {worst['astrometric']:.3f}\" (Moon {worst['astrometric_moon']:.3f}\"), apparent of date {worst['apparent']:.2f}\","
      f" az/el {worst['azel']:.2f}\", elongation {worst['elong']:.2f}\"")
check("Horizons astrometric Sun/Venus/Mercury < 0.01\"", worst["astrometric"] < 0.01, f"{worst['astrometric']:.3f}\"")
# The Moon's topocentric direction depends on where the observer is in the GCRS, i.e. on the
# Earth-orientation model: ~30" of sidereal-time difference x (R_earth / d_moon ~ 1/60) ~ 0.5".
check("Horizons astrometric Moon < 0.5\" (observer-orientation parallax)", worst["astrometric_moon"] < 0.5,
      f"{worst['astrometric_moon']:.3f}\"")
check("Horizons elongation < 1\"", worst["elong"] < 1.0, f"{worst['elong']:.2f}\"")
check("Horizons az/el < 60\" (model differences)", worst["azel"] < 60, f"{worst['azel']:.1f}\"")

# ======================================================================
hdr("9. Summary of checks")
for name, ok, detail in CHECKS:
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}  {detail}")
print(f"\n{sum(ok for _, ok, _ in CHECKS)}/{len(CHECKS)} passed; run time {time.time() - T_START:.0f} s")
