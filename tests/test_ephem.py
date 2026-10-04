"""
Unit tests for odybench.ephem.  No pytest on this machine, so:

    cd C:\\Projects\\odybench && py tests/test_ephem.py

(also collectable by pytest if it is ever installed).  Runs in ~1 minute.
Reference values and their sources are documented in docs/research-ephemeris.md.
"""
import math
import sys
from pathlib import Path

import numpy as np
import erfa

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from odybench import ephem as E  # noqa: E402


def test_calendar():
    assert E.jd_from_julian(-1177, 4, 16) == 1291263.5          # Horizons: b1178-Apr-16 00:00 UT
    assert E.jd_from_julian(-4712, 1, 1, 12.0) == 0.0
    for jd in (1238939.5, 1291264.248, 1344860.25, 1442903.089, 2451545.0 - 13.0):
        y, m, d, h = E.julian_from_jd(jd)
        assert abs(E.jd_from_julian(y, m, d, h) - jd) < 1e-8
    assert E.fmt_jd(1291264.24800, "TT").startswith("-1177-04-16 17:57:07 TT (16 Apr 1178 BC")


def test_delta_t_models():
    y = -1177 + 3.5 / 12                                        # NASA's decimal-year convention
    assert abs(float(E.dt_em2006_canon(y)) - 28590.0) < 0.5      # Canon -1177 Apr 16
    assert abs(float(E.dt_smh2020(-720)) - 20371.848) < 1e-6     # S15 v2020 row 1 a0
    assert math.ceil(float(E.dt_smh2020(-1200)) / 360 - 1e-9) / 10 == 8.1   # HMNAO table, -1200
    assert float(E.sigma_smh2020(-1177)) == 720.0                # HMNAO epsilon +-0.2 h
    assert abs(float(E.dt_smh2020_parabola(-1176.68)) - 28282) < 2
    assert abs(float(E.dt_smh2016_parabola(-1176.68)) - 28963) < 2
    # continuity at the spline edge
    assert abs(float(E.dt_smh2020(-720 - 1e-6)) - float(E.dt_smh2020(-720 + 1e-6))) < 0.01


def test_vondrak_test_case():
    epj = -1373.5959534565
    pequ = np.array([-0.29437643797369031532, -0.11719098023370257855, +0.94847708824082091796])
    assert np.max(np.abs(erfa.ltpequ(epj) - pequ)) < 1e-14
    rpb = np.array([[+0.68473392912753224372, +0.66647788221176470103, +0.29486722236305384992],
                    [-0.66669476463873305255, +0.73625641199831485100, -0.11595079385100924091],
                    [-0.29437652267952261218, -0.11719099075396051880, +0.94847706065103424635]])
    # paper's values carry the C7 typo fixed in the 2012 corrigendum: < 1 mas
    assert np.max(np.abs(erfa.ltpb(epj) - rpb)) < 5e-9


def test_precession_models_agree_at_1177():
    pc = E.precession_compare(E.jd_from_julian(-1177, 4, 16))
    assert pc["pole_sep_arcsec"] < 5 and abs(pc["eo_diff_arcsec"]) < 5
    # quadrature EO along the IAU 2006 path agrees with the GMST06 polynomial
    assert abs(pc["eo_iau2006_integrated_arcsec"] - pc["eo_iau2006_poly_arcsec"]) < 0.5


def test_canon_eclipse_1177():
    jd = E.jd_from_julian(-1177, 4, 16, 17 + 57 / 60 + 28 / 3600)    # Canon greatest eclipse, TD
    jge, b = E.greatest_eclipse(jd)
    assert abs(float(b["gamma"]) - 0.5187) < 0.002
    assert abs(jge - jd) * 86400 < 300
    lc = E.local_circumstances(32.674, 12.192, jge, dt=28590.0)      # our greatest-eclipse point
    assert lc["total"] and abs(lc["ratio"] - 1.0599) < 0.002
    assert abs(lc["duration_s"] - 273) < 6                           # Canon 04m33s
    b0 = E.besselian(E.jd_from_julian(-1177, 4, 16, 18.0), dt=28590.0)
    assert abs(float(b0["mu_eph"]) - 90.087601) < 0.02                # Canon mu0 (ephemeris HA)


def test_dt_is_longitude_shift():
    jge = E.jd_from_julian(-1177, 4, 16, 18.0)
    a = E.local_circumstances(38.37, 20.72, jge, dt=28000.0)
    b = E.local_circumstances(38.37, 20.72 + 1.00273781191135448 * 15 * 500 / 3600, jge, dt=28500.0)
    assert abs(a["magnitude"] - b["magnitude"]) < 1e-6


def test_babylon_135_window_with_de431():
    jge = E.jd_from_julian(-135, 4, 15, 9.46)
    with E.use_ephemeris(E.EPHEM_DIR / "de431"):
        w = E.totality_window(32.54, 44.42, jge, 10800.0, 12600.0, step=200.0)
    assert len(w) == 1
    lo, hi = w[0]
    assert abs(lo - 11220) < 60 and abs(hi - 12140) < 60             # SMH Table S10 v2020


def test_new_moon_1177():
    nm = E.new_moons(E.jd_from_julian(-1177, 4, 10), E.jd_from_julian(-1177, 4, 22))
    assert len(nm) == 1
    assert abs(nm[0] - E.jd_from_julian(-1177, 4, 16, 18 + 5 / 60 + 10 / 3600)) * 86400 < 30


def test_venus_vs_horizons_cache():
    f = ROOT / "data" / "ephem" / "horizons" / "venus_mercury_m1177_04_10_dawn_299.txt"
    if not f.exists():
        return                                                       # run tools/validate_ephem.py first
    row = f.read_text().split("$$SOE")[1].split("$$EOE")[0].strip().splitlines()[0].split(",")
    jd, az, el, sot, dtb = float(row[0]), float(row[7]), float(row[8]), float(row[11]), float(row[13])
    alt, azm = E.altaz("venus", jd, 38.37, 20.72, dt=dtb)
    assert abs(alt - el) * 3600 < 60 and abs(azm - az) * 3600 < 60
    assert abs(E.elongation("venus", jd, 38.37, 20.72, dt=dtb) - sot) * 3600 < 1


def test_star_proper_motion():
    t = E.time_ut(E.jd_from_julian(-1177, 3, 18, 18.0))
    from skyfield.positionlib import Barycentric
    ra, de, _ = Barycentric([0.0, 0.0, 0.0], [0.0, 0.0, 0.0], t=t).observe(E.star("arcturus")).radec()
    # Arcturus moved ~2.0 deg since J1991.25 (2.28"/yr x 3168 yr)
    d = math.degrees(math.acos(math.sin(de.radians) * math.sin(math.radians(19.18727046))
                               + math.cos(de.radians) * math.cos(math.radians(19.18727046))
                               * math.cos(ra.radians - math.radians(213.91811408))))
    assert abs(d - 2.002) < 0.005


if __name__ == "__main__":
    import time
    fails = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            t0 = time.time()
            try:
                fn()
                print(f"PASS {name} ({time.time() - t0:.1f} s)")
            except Exception as exc:          # noqa: BLE001
                fails += 1
                print(f"FAIL {name}: {exc!r}")
    print("all passed" if not fails else f"{fails} failed")
    sys.exit(1 if fails else 0)
