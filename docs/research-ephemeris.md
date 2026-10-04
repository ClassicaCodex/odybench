# Ephemeris stack for odybench: sources, choices, validation

Task: a validated computation stack, on this machine, for the Sun, Moon, Mercury,
Venus and bright stars between 1300 and 1050 BC, plus solar-eclipse local
circumstances at Ithaca. This is the tool layer under the bench's reproduction
of Baikouzis & Magnasco (PNAS 2008). I did not read that paper for this task.
Here it only defines the target date, the -1177 Apr 16 eclipse.

Code: `odybench/ephem.py` (module), `tools/validate_ephem.py` (prints every
check beside its reference), `tools/fetch_ephem.py` (rebuilds the ephemeris
excerpts), `tests/test_ephem.py` (10 fast unit tests; run with
`py tests/test_ephem.py`). The full validation output is in section 10 and in
`results/validate_ephem.txt`. Result: **55/55 checks pass**, and every
non-zero residual has an identified cause.

## Conventions

* Every date gives the **astronomical year** and the historical year:
  -1177 = 1178 BC. Calendar dates are **proleptic Julian** unless marked
  otherwise. The NASA canon, the NASA phase tables and JPL Horizons also use
  Julian dates before 1582.
* Time scales: **TT** (= TD/TDT of the NASA canon; TDB-TT < 2 ms, ignored),
  **UT** = UT1, and **LAT** = local apparent solar time (12:00 = true noon).
  Delta-T = TT - UT1, in seconds.
* Longitudes are east-positive, latitudes geodetic (WGS84), and sites are at
  sea level.
* Sites (modern reference points I chose; the Homeric site is not known):
  Ithaki (Vathy) 38.37 N 20.72 E (as in the task brief); Kefalonia
  (Argostoli) 38.18 N 20.49 E; Lefkada (town) 38.83 N 20.71 E; Babylon
  32.54 N 44.42 E; Qufu 35.60 N 116.99 E; Assur 35.46 N 43.26 E; Nineveh
  36.36 N 43.15 E.
* Provenance tags: [SMH16] Stephenson, Morrison & Hohenkerk 2016 (PMC
  full text); [ADD20] Morrison, Stephenson, Hohenkerk & Zawilski 2021,
  Addendum 2020 (PDF via the Internet Archive); [HMNAO] HM Nautical Almanac
  Office LVM page (archived 2022-03-20); [EM06] Espenak & Meeus NASA pages;
  [V11] Vondrak, Capitaine & Wallace 2011 + corrigendum 2012; [HZ] JPL
  Horizons manual/API; [P21] Park et al. 2021 (DE440/441). "computed" means
  computed by me with odybench.ephem / ERFA, and the output is in section 10.

---

## Key findings (summary)

1. **The stack works and agrees with independent instruments.**
   * DE441 positions match JPL Horizons to 0.001" for Sun, Venus and Mercury
     (astrometric, topocentric Ithaki) and to 0.18" in elongation (computed;
     Horizons prints 0.36" steps).
   * Eclipse geometry matches the NASA Five Millennium Canon to within
     0.0008 in gamma, 0.0001 in magnitude and 0 s in central duration.
     Greatest eclipse comes 31-143 s later than the Canon, which is the
     difference between the two lunar ephemerides (computed).
2. **With DE431 (the DE430 lunar model that SMH's Delta-T is tied to), my
   eclipse code reproduces SMH's published Delta-T bounds** for the
   -135 Babylon and -708 Qufu total eclipses to within 6-16 s (computed vs
   [ADD20] Table S10). This is the strongest validation of the Delta-T-window
   machinery the bench will use.
3. **The choice of lunar ephemeris matters at the 3-minute level.** Relative
   to DE431, DE441's Moon lags by about 0.00335" T^3 (T in centuries from
   J2000; residuals < 1"). At -1177 that is 108" of elongation and **+188 s**
   in eclipse time, which moves the Delta-T totality window by +161 s
   (computed). SMH Delta-T should be paired with DE431, or the offset carried
   as a systematic.
4. **Delta-T at -1177.3: the authors' own formulations disagree by 681 s, and
   their stated error is 720 s** (computed from [SMH16] eq. 4.1, [ADD20]
   eq. 5.1, and the [HMNAO] lod-integral extrapolation):

   | model | value | error |
   |---|---|---|
   | [HMNAO] extrapolation | 28543 s | +-720 s |
   | [ADD20] parabola | 28282 s | +-541 s |
   | [SMH16] parabola | 28963 s | +-541 s |
   | [EM06] | 28716 s | Huber sigma 1008 s |
   | [EM06] with Canon n-dot | 28589 s | Huber sigma 1008 s |
   | Horizons | 28418 s | none stated |
   | skyfield built-in | 28786 s | none stated |

   720 s of Delta-T is 3.0 deg of Earth rotation.
5. **Precession is not a problem at -1177.** IAU 2006 (skyfield) and the
   long-term Vondrak 2011 model differ by 1.4" in the pole, 2.1" in total
   rotation, and 1.6" (0.1 s of time) in sidereal time.
   * The IAU 1982 GMST formula used by Horizons (and apparently by the NASA
     Canon) differs by 30" (2 s). That explains the ~20-30" az/el
     differences against Horizons.
   * All of these are negligible next to Delta-T.
6. **The -1177 Apr 16 eclipse at Ithaca (computed):**
   * Totality on Ithaki needs a constant Delta-T in [28922, 29706] s with
     DE441, or [28761, 29545] s with DE431.
   * Under SMH2020 (28543 +- 720) the central line crosses Ithaki's
     meridian 260-330 km north of the island.
   * Ithaki sees a deep partial eclipse, magnitude 0.97-0.98, near true noon
     (LAT 11:44-11:49, Sun altitude 57 deg).
   * Treating the stated error as a Gaussian 1 sigma (my assumption),
     **P(total at Ithaki) is about 0.30 with DE431 (0.25 with DE441).**
     The other models give:

     | model | P(total at Ithaki) |
     |---|---|
     | [ADD20] parabola | 0.11-0.18 |
     | [SMH16] parabola | 0.45-0.51 |
     | [EM06] | 0.24-0.28 |

     Lefkada is about 0.04 higher, and Kefalonia is about the same as Ithaki.
7. **Several reference quirks surfaced and are documented** in sections 2-6:
   * the [V11] test values carry the coefficient typo that its corrigendum
     fixes;
   * the [HMNAO] -2000..-800 Delta-T table is the continuity-matched lod
     integral **rounded up**;
   * Horizons' actual pre-721 BC Delta-T does not follow its manual's
     formula;
   * NASA's phase catalogue is 15.8 min early relative to NASA's own Canon at
     -1177.

---

## 1. Software and data actually installed

| item | version / file | source |
|---|---|---|
| Python | 3.14.3 | machine |
| numpy, scipy | 2.5.0, 1.18.0 | machine |
| skyfield | 1.55 | `py -m pip install --user skyfield jplephem` (2026-10-03) |
| jplephem | 2.24 | same |
| sgp4 | 2.27 | skyfield dependency |
| pyerfa / ERFA | 2.0.1.5 / 2.0.1 | `py -m pip install --user pyerfa` (for eraLtpb, eraEors, eraPmsafe, eraGmst82...) |
| DE441 excerpt | `data/ephem/de441_m1320_m1030.bsp`, 30.0 MB, JD 1238939.5-1344860.5 (proleptic Gregorian -1320-01-01..-1030-01-01), targets 1,2,3,4,5,6,10,199,299,301,399; sha256 a88827c5... | NAIF `de441_part-1.bsp` via HTTP Range |
| DE441 eclipse excerpts | `de441_m0762/m0584/m0708/m0135_eclipse.bsp`, about 90 kB each, +-60 d, targets 3,10,301,399 | same |
| DE431 excerpts | `data/ephem/de431/de431_m1320_m1030.bsp` (27.8 MB, targets 1,2,3,10,199,299,301,399) and three +-60 d eclipse excerpts | NAIF `de431_part-1.bsp` |
| reference files | `data/ref/` (HMNAO S10/S15, NASA Besselian pages, Canon rows, phase table) and `data/ephem/horizons/` (cached API responses, URL on line 1) | see `data/ref/SOURCES.txt` |

Things I found while fetching (checked):

* `https://ssd.jpl.nasa.gov/ftp/eph/planets/bsp/de441_part-1.bsp` returns
  **HTTP 404**. The SSD directory has only the unsplit `de441.bsp`, while the
  split `part-1/part-2` files are on NAIF
  (`https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/`, listed at
  1.5 GB each). The Range-request excerpt fetched 30 MB in total, and no file
  over 300 MB was downloaded.
* **How `jplephem excerpt` takes BC dates:**
  * its `parse_date` takes `yyyy/mm/dd` in **astronomical years of the
    proleptic GREGORIAN calendar**, and negative years are allowed
    (`jplephem/calendar.py:compute_julian_date`);
  * argparse reads `-1320/1/1` as an option, so put a `--` before the
    positional arguments;
  * or call `jplephem.excerpter.write_excerpt` with Julian Dates directly,
    which is what `tools/fetch_ephem.py` does.
* Python's urllib (Windows certificate store) had no TLS problem with
  NAIF, JPL, CDS or NASA. The only certificate failure was
  `https://astro.ukho.gov.uk` (a local-issuer error), and HTTP to that host
  returned 503. I used Internet Archive copies of the HMNAO pages and files.
* DE441's header says it was "Integrated 25 June 2020" [P21].
  * DE441 covers -13,200 to +17,191.
  * Park et al. recommend DE441 for "historical data earlier than the
    modern range data" [P21 sect. 1].
  * They give **no explicit value** for the Moon's tidal acceleration. It is
    "implicit" in the tidal model [P21 sect. 3.3].
  * DE441 differs from DE440 in the lunar along-track direction over long
    spans [P21 Fig. 1].

## 2. Delta-T

### 2.1 What the sources say

* **[SMH16]** (Proc. R. Soc. A 472:20160404; PMC5247521, read in full text).
  * Eq. (4.1): Delta-T = -320.0 + (32.5 +- 0.6) tau^2 s, tau = (year - 1825)/100.
  * Sect. 3a: pre-telescopic observations were reduced with the analytical
    lunar ephemeris "j=2" with n-dot = -26.00"/cy^2. The JPL value implicit
    in DE430 is -25.82 +- 0.03"/cy^2. Their Fig. 1 puts the mean DE430/431
    minus j=2 longitude difference at about 10" in the ancient period, about
    20 s in Delta-T.
  * The derived Delta-T "should be used in conjunction with" DE430 or an
    ephemeris with n-dot close to -25.82.
  * Sect. 5a, eq. (5.1): lod = +1.78 t - 4.0 sin(2 pi t/15) ms. The authors
    call the oscillation's reality and the extrapolation "somewhat
    conjectural" (sect. 5a).
  * No uncertainty formula is given for dates before -720.
* **[ADD20]** (Proc. R. Soc. A 477:20200776; open-access PDF obtained from
  the Internet Archive because royalsocietypublishing.org returned 403).
  * Eq. (5.1): Delta-T = **-10 + (31.4 +- 0.6) tau^2** s. This corresponds
    to -4.59 +- 0.08 x 10^-22 rad s^-2 and +1.72 +- 0.03 ms/cy.
  * Sect. 8: a periodic fluctuation -3.5 sin(2 pi t) ms with
    t = (year - 1750)/1400. The Fig. 4 caption calls the 14-century
    fluctuation "speculative".
  * The new spline is Table S15 v2020 (-720..2019).
* **[HMNAO]** (astro.ukho.gov.uk/nao/lvm/, archived 2022-03-20).
  * For -2000..-800, Delta-T is "extrapolated backwards by integration using
    the long term lod function lod = +1.72 t - 3.5 sin(2 pi (t+0.75)/14)",
    with t in centuries from 1825.0.
  * The table is in hours to 0.1 h, with error estimate epsilon = **+-0.2 h**
    for -1600..-1000 (+-0.3 h at -2000..-1700 and +-0.1 h at -900/-800).
  * Example entries: -1200: 8.1 h; -1100: 7.6 h.
  * The page also says the values go with DE430/LE430, "in which the tidal
    acceleration of the Moon is -25.85"/cy^2". The paper says -25.82, so
    the two disagree by 0.03.
* **[EM06]** NASA "Polynomial Expressions for Delta T": before -500,
  Delta-T = -20 + 32 u^2, u = (y-1820)/100 (Morrison & Stephenson 2004).
  * It assumes n-dot = -26.
  * For the Canon (ELP-2000/82, n-dot -25.858), c = -0.000012932 (y-1955)^2
    is added.
  * Uncertainty (NASA "Uncertainty in Delta T" page): Morrison & Stephenson
    2004 give sigma = 0.8 t^2 s, stated for 1000 BCE to 1200 CE, so -1177
    is just outside its stated range (718 s). Huber 2000 gives
    sigma = 365.25 N sqrt((N Q/3)(1+N/M))/1000 with calibration year -500,
    M = 2500, Q = 0.058 ms^2/yr: 622 s at -1000, 1900 s at -1500, and
    **1008 s at -1177** (computed).
* **[HZ]** Horizons manual:
  * "9999 BC to 721 BC: 65.62 + 31.351922682 T^2 (cent. since JD1825)";
    after that, Stephenson/Morrison; references [SMH16] and [ADD20].
  * Measured with quantity 30 at 7 epochs before -721, the actual values fit
    **65.80 + 31.457566 ((y - 1825.44)/100)^2** exactly (residual < 1 ms),
    which is not the manual's formula. At -1177 Jan 1, Horizons gives
    28423.1 s, about 104 s above the manual's formula (computed).
* **skyfield 1.55** built-in:
  * the S15 v2020 spline back to -720;
  * an 800-year hand-tuned cubic patch (`timelib.build_delta_t`);
  * the SMH2016 parabola before -1520.
  * At -1177 it gives 28786 s. odybench never uses it implicitly, because
    every Time is built on an explicit Delta-T.

### 2.2 Implemented (odybench.ephem)

`dt_em2006`, `dt_em2006_canon`, `sigma_ms2004`, `sigma_huber`,
`dt_smh2016_parabola`, `dt_smh2020_parabola`, `sigma_parabola`,
`dt_smh2020` (S15 v2020 spline from -720 to 2019; before -720 the HMNAO
lod integral, with the integration constant C = +1.0077 s fixed by
continuity at -720, the same value as in Y. T. Liu's `DeltaT.py`),
`sigma_smh2020` (the HMNAO epsilon table, interpolated), `ndot_correction`,
`delta_t(y, model)` and `delta_t_sigma(y, model)`. The argument is the Julian
epoch. It runs 13 d ahead of "year + (month-0.5)/12" for proleptic-Julian
dates, which changes Delta-T by < 1 s at -1177.

Checks (section 10):

* `dt_smh2020` reproduces all 25 HMNAO spline-table epochs from -720 to
  +1600 to <= 5.0 s (the table is rounded to 10 s).
* skyfield's bundled S15 table is identical, all 58 rows, to the HMNAO file.
* `dt_em2006_canon` reproduces the Canon's Delta-T for all five test
  eclipses to <= 0.5 s.
* **HMNAO -2000..-800 table:** the continuity-matched integral reproduces all
  13 entries when they are read as **rounded up** to 0.1 h. Rounded to the
  nearest value, only 5/13 match. For example, -1200 is 8.046 h, printed
  as 8.1. A constant offset of +136..+221 s would also fit, but rounding up
  is the simpler explanation. This is my inference; the page does not say.
  It moves -1177 by at most 0.1 h, well inside epsilon.

### 2.3 Values (decimal year -1176.68 = -1177 Apr 16)

| model | -1300 | **-1177.29** | -1100 | -1050 | stated 1 sigma at -1177 | source of sigma |
|---|---|---|---|---|---|---|
| smh2020 (S15 + HMNAO lod integral) | 30800 | **28543** | 27153 | 26249 | 720 | HMNAO epsilon +-0.2 h |
| smh2020_parabola [ADD20 eq 5.1] | 30654 | **28282** | 26855 | 25944 | 541 | +-0.6 tau^2 |
| smh2016_parabola [SMH16 eq 4.1] | 31418 | **28963** | 27486 | 26543 | 541 | +-0.6 tau^2 |
| em2006 [EM06] | 31130 | **28716** | 27264 | 26338 | 1008 (718) | Huber (MS2004 0.8u^2) |
| em2006_canon (n-dot -25.858) | 30993 | **28589** | 27144 | 26221 | 1008 | Huber |
| skyfield 1.55 built-in | 31334 | **28786** | 27250 | 26270 | none | none |
| JPL Horizons TDB-UT | 30794 (Jan 1) | **28418** (Apr 16) | 26987 | 26075 | none | none |

The n-dot conversion -26.00 -> -25.82 is -161 s at -1177, and
-25.82 -> -25.858 is +34 s (computed with -0.91072 Delta-ndot T^2).

## 3. Precession and sidereal time at -1177

* **[V11]** test case (App. A.5, epoch JD 1219339.078 TT = -1374 May 3
  Gregorian):
  * ERFA `eraLtpequ` matches to 2.5e-15.
  * `eraLtpecl` and `eraLtp`/`eraLtpb` differ by 2.7e-9 and 3.9e-9 (0.56
    and 0.81 mas).
  * The 2012 corrigendum (A&A 541, C1) explains this: C7 for Q_A should be
    198.296701, not the printed 198.296071, and "the same error is present
    in the Fortran subroutine ltp_PECL".
  * My Python port of eraLtpecl **with the typo** reproduces the paper's
    vectors and matrices to 1e-16..6e-15 (computed). So the paper's test
    values were generated with the typo, and ERFA is right.
* **Sidereal time consistent with the long-term pole.** skyfield's GAST is
  the IAU 2006 polynomial. For the Vondrak option, the module sets the
  following on each Time:

  ```
  M = N(IAU2000A)·PB(eraLtpb)
  GAST = ERA(UT1) - EO,  EO = eraEors(M, s)
  ```

  * s is the CIO locator from direct quadrature of
    s = -∫(X dY - Y dX)/(1+Z) dt along the long-term pole path, from
    J2000, plus the first-order nutation term.
  * Check: the same quadrature along the IAU 2006 path agrees with ERFA
    `eraS06a` to <= 11.5 mas over 1700-2200. The neglected terms are a
    2.6 mas 18.6-yr term and a 3.8 mas/cy cross term.
  * The integrated EO agrees with the IAU 2006 GMST polynomial to 0.08" at
    -1177.
* **Measured differences, Vondrak minus IAU 2006 (P03), at -1177:**
  * mean-pole separation 1.43"
  * total rotation 2.14"
  * equation of the origins 1.58" (= 0.105 s of time)
  * obliquity -1.71"
  * at -2000: 4.1", 5.9", 3.9" and -4.7"

  [V11] (sect. 7, and the ERFA documentation) gives the model's own
  accuracy as "a few arcseconds throughout the historical period". The two
  models are therefore indistinguishable at this level, and either is fine
  for the bench. The module defaults to Vondrak.
* **IAU 1982 GMST** (`eraGmst82`, used by Horizons per its manual) minus
  the Vondrak-consistent GMST = **+30.1"** (2.0 s of time) at -1177; IAU
  2006 GMST minus Vondrak = +1.6". This one number explains two things:
  * the -31" difference in mu (ephemeris hour angle) against the NASA
    Canon's Besselian elements (-18", -14", -6" and -16" at -762, -584,
    -135 and -708);
  * the 17-32" az/el differences against Horizons.

## 4. Stars

Hipparcos new reduction (van Leeuwen 2007, VizieR I/311/hip2), epoch
J1991.25, ICRS, pmRA = mu_alpha*. Radial velocities and their bibcodes come
from SIMBAD TAP. All were fetched 2026-10-03.

| key | HIP | RA (deg) | Dec (deg) | plx (mas) | pmRA* | pmDE (mas/yr) | RV (km/s), bibcode |
|---|---|---|---|---|---|---|---|
| alcyone (eta Tau) | 17702 | 56.87110081 | +24.10524179 | 8.09 | 19.34 | -43.67 | +5.4 +-1.2 (2006AstL...32..759G) |
| arcturus (alpha Boo) | 69673 | 213.91811408 | +19.18727046 | 88.83 | -1093.39 | -2000.06 | -5.229 (2018A&A...616A...7S) |
| eps_boo | 72105 | 221.24687848 | +27.07417376 | 16.10 | -50.95 | 21.07 | -16.6 +-0.9 (1979IAUS...30...57E) |
| eta_boo | 67927 | 208.67131829 | +18.39858670 | 87.75 | -60.95 | -356.29 | +5.771 (2020AJ....160..120J) |

Computed (section 10.3):

* Arcturus' total proper motion is 2.279"/yr, which carries it **2.002 deg**
  between J1991.25 and -1177 (eta Boo 0.32 deg; Alcyone and eps Boo
  ~0.04 deg).
* The radial velocity adds 11.0" for Arcturus (perspective acceleration).
* The Hipparcos 1997 catalogue instead of 2007 changes positions by 1.8-5.8".
* skyfield's linear space motion vs ERFA `eraPmsafe`: 0.003-0.125". The
  difference matches, to 0.001", the light-time change as the star's
  distance changes (Arcturus: 20 d of light time x 2.28"/yr = 0.126"), which
  ERFA models and skyfield does not.
* Vondrak minus IAU 2006 in apparent place of date: <= 2.5"; in altitude and
  azimuth at Ithaki: <= 2.6".

Not checked against an independent ancient-epoch star reference; there is
none at this accuracy.

## 5. Solar eclipses

### 5.1 Method

`besselian()` computes x, y, d, mu (Greenwich and ephemeris hour angle) and
signed gamma from geocentric apparent DE441 positions on the true equator of
date. `greatest_eclipse()` minimises |gamma|.

`local_circumstances()` works directly from topocentric apparent Sun and Moon:
separation, semidiameters, and minimisation and root-finding for the maximum
and the contacts.
* Radii follow NASA: solar semidiameter 959.63" at 1 au, k1 = 0.272488
  (penumbra, magnitude), k2 = 0.272281 (umbra, totality).
* No lunar limb profile; NASA puts its effect on path edges at 1-2 km, a few
  seconds of Delta-T.
* No refraction (the Sun is at 57 deg).

`totality_window()` scans constant Delta-T and bisects the edges to 0.5 s.
Changing Delta-T is exactly equivalent to a longitude shift of
1.0027379 x 15"/s; self-check 5d agrees to 1e-6.

The independent check (section 10, 5a and 6) evaluates NASA's own polynomial
Besselian elements for local circumstances with the classical algorithm
(Explanatory Supplement 1992 ch. 8 / Meeus). It shares no code or ephemeris
with my path.

### 5.2 Side by side with the NASA Five Millennium Canon (VSOP87 / ELP-2000/82, n-dot -25.858)

| eclipse | quantity | ours (DE441) | Canon | diff |
|---|---|---|---|---|
| -1177 Apr 16 (1178 BC) | greatest eclipse TT | 17:59:51 | 17:57:28 TD | +143 s |
| | gamma | 0.5179 | 0.5187 | -0.0008 |
| | magnitude (k2 ratio) at GE | 1.0600 | 1.0599 | +0.0001 |
| | central duration at GE | 273 s | 04m33s | 0 s |
| | Sun alt/az at GE | 58.6/145.5 | 58.6/145.5 | 0 |
| | GE point (Canon Delta-T 28590 s) | 32.67N 12.19E, 10:03:21 UT | 32.7N 12.7E, 10:00:58 UT | GE comes later by 143 s |
| | mu at 18h TT (ephemeris HA) | 90.0791 | 90.0876 | -31" (IAU 1982 GMST) |
| -762 Jun 15 (763 BC) | GE TT; gamma; mag; duration | 14:09:09; 0.2720; 1.0596; 300 s | 14:07:32; 0.2715; 1.0596; 05m00s | +97 s; +0.0005; 0; 0 |
| -584 May 28 (585 BC) | same | 19:29:57; 0.3198; 1.0798; 364 s | 19:28:50; 0.3201; 1.0798; 06m04s | +67 s; -0.0003; 0; 0 |
| -135 Apr 15 (136 BC) | same | 09:27:39; 0.7118; 1.0527; 219 s | 09:27:08; 0.7119; 1.0527; 03m39s | +31 s; -0.0001; 0; 0 |
| -708 Jul 17 (709 BC) | same | 12:30:20; 0.4760; 1.0601; 265 s | 12:28:51; 0.4756; 1.0601; 04m25s | +89 s; +0.0004; 0; 0 |

* The Canon's Delta-T at -1177 is 28590 s = [EM06] 28716.8 + c(-126.8).
  This was computed and reproduces the Canon's figure to 0.0 s.
* The time offsets grow with antiquity because the lunar ephemerides
  differ: ELP-2000/82 with only n-dot corrected, against DE441.

### 5.3 The lunar ephemeris has to match the Delta-T (new; computed)

Greatest-eclipse time, DE441 minus DE431 (DE431 = the DE430 lunar model over
a long span):

| epoch | -135 | -708 | -762 | -1177 |
|---|---|---|---|---|
| DE441 - DE431 | +55.8 s | +115.2 s | +122.9 s | **+187.7 s** |

* In elongation this is Moon(DE441) - Moon(DE431) = **+0.00335" T^3**,
  with T in Julian centuries from J2000 and residuals <= 0.7". A pure
  0.5 b T^2 (constant n-dot) fit is worse, with residuals up to 12". That
  is consistent with DE441's different tidal model, not a constant-n-dot
  change; the mechanism is my inference.
* **SMH's untimed-eclipse bounds, my windows with DE431:**

  | site | DE431 window | SMH bounds | DE441 window |
  |---|---|---|---|
  | -135 Babylon | [11214, 12126] | [11220, 12140] | [11259, 12170] |
  | -708 Qufu | [20176, 21103] | [20160, 21100] | [20271, 21198] |

  So the DE431 pipeline reproduces the bounds SMH derived to 3-16 s, and
  DE441 is offset by the DE441-DE431 shift.
  * The remaining <= 16 s is within the ~20 s that [SMH16] Fig. 1 gives for
    DE431 vs j=2.
  * The site coordinates may also differ slightly; SMH's are not given in
    Table S10.
* **Consequence:** with SMH Delta-T, compute the Moon with DE431
  (`with E.use_ephemeris(E.EPHEM_DIR / "de431")`), or add about +160 to
  +190 s (at -1177) to Delta-T when using DE441. Neither ephemeris is
  "truth" at -1177. The empirical Delta-T absorbs the ephemeris it was
  reduced with, so the pairing is what matters.

### 5.4 The -1177 Apr 16 eclipse at Ithaca, Kefalonia, Lefkada

At the Canon's Delta-T (28590 s), against NASA's own elements:

| site | max (UT) | magnitude |
|---|---|---|
| Ithaki, ours (DE441) | 10:25:41 | 0.9751 |
| Ithaki, NASA elements | 10:22:24 | 0.9839 |

Neither is total. Kefalonia and Lefkada behave the same way. The 197 s and
0.009 differences are the ephemeris offset above.

**As a function of constant Delta-T**, Ithaki with DE441 (section 10, 5b):

| Delta-T | max UT | LAT | magnitude | total? | Sun alt |
|---|---|---|---|---|---|
| 26000 | 11:25 | 12:47 | 0.783 | no | 55.6 |
| 27000 | 11:02 | 12:24 | 0.856 | no | 56.9 |
| 28000 | 10:39 | 12:01 | 0.930 | no | 57.4 |
| 28500 | 10:28 | 11:49 | 0.968 | no | 57.3 |
| 29000 | 10:16 | 11:38 | 1.006 | yes, 162 s | 57.0 |
| 29500 | 10:05 | 11:26 | 1.016 | yes, 237 s | 56.5 |
| 30000 | 09:54 | 11:15 | 0.978 | no | 55.8 |
| 31000 | 09:31 | 10:53 | 0.903 | no | 54.0 |
| 32000 | 09:09 | 10:30 | 0.829 | no | 51.6 |

**At SMH2020 Delta-T 28543 +- 720 s:**

| Delta-T | ephemeris | Ithaki magnitude | LAT | Sun altitude | first to last contact (UT) |
|---|---|---|---|---|---|
| 28543 | DE441 | 0.972 | 11:49 | 57.3 deg | 09:10-11:45 |
| 28543 | DE431 | 0.984 | 11:44 | 57.2 deg | 09:06-11:41 |
| 27823 (-1 sigma) | DE441 | 0.917 | | | |
| 27823 (-1 sigma) | DE431 | 0.929 | | | |
| 29263 (+1 sigma) | DE441 | total, 268 s | | | |
| 29263 (+1 sigma) | DE431 | total, 259 s | | | |

Kefalonia is within 0.001 of Ithaki. Lefkada is 0.009 higher, at 0.981
(DE441) and 0.993 (DE431). All computed.

**Totality windows (constant Delta-T, s)**:

| site | DE441 | DE431 | NASA elements |
|---|---|---|---|
| Ithaki | [28922, 29706] | [28761, 29545] | [28801, 29585] |
| Kefalonia | [28916, 29697] | [28754, 29536] | [28794, 29576] |
| Lefkada | [28801, 29591] | [28640, 29430] | [28680, 29470] |

Where the central line crosses 20.72 E (computed):

| Delta-T | DE441 | DE431 | Ithaki relative to the line (DE441 / DE431) |
|---|---|---|---|
| 28543 | 41.30 N | 40.72 N | 326 / 262 km south |
| 27823 | 43.75 N | 43.24 N | 599 / 542 km south |
| 29263 | 38.58 N | 37.93 N | 23 km south / 49 km north |

As Delta-T grows, the path moves south over the Ionian islands.

**Chance of totality** treating each model's stated error as a Gaussian 1
sigma (my modelling choice, not the authors'):

| model (value +- sigma) | Ithaki DE441 | Ithaki DE431 | Kefalonia 441/431 | Lefkada 441/431 |
|---|---|---|---|---|
| smh2020 28543 +- 720 | 0.246 | 0.299 | 0.248/0.301 | 0.287/0.337 |
| smh2020_parabola 28282 +- 541 | 0.114 | 0.178 | 0.116/0.181 | 0.161/0.237 |
| smh2016_parabola 28963 +- 541 | 0.445 | 0.505 | 0.448/0.505 | 0.495/0.531 |
| em2006 28716 +- 1008 | 0.256 | 0.277 | 0.256/0.277 | 0.274/0.291 |
| em2006_canon 28589 +- 1008 | 0.237 | 0.261 | 0.237/0.261 | 0.257/0.278 |

Reading of these numbers (my inference): Delta-T cannot settle whether
Ithaca saw totality. What it does fix is a very deep partial or total
eclipse near local noon. Magnitude is >= 0.9 for constant Delta-T between
about 27,600 and 31,000 s, which is SMH2020 -1.3 sigma to +3.4 sigma; at
-2 sigma (about 27,100 s) the magnitude is about 0.86. Maximum falls between
LAT 10:30 and 12:47 across the whole 26,000-32,000 s range. The spread among
SMH's own formulas, 681 s, is about one stated sigma, so the bench should
marginalise over the Delta-T formulation rather than pick one.

### 5.5 Historical eclipses with recorded observations

* **-135 Apr 15 Babylon** and **-708 Jul 17 Qufu**: see 5.3. With DE431
  these reproduce SMH's Table S10 bounds to 3-16 s, the positive control for
  the window machinery.
* **-762 Jun 15 (763 BC, Assyrian eponym chronicle)**. The record states a
  solar eclipse, not totality. I relied on the general literature for that
  and did not read the text.
  * DE441 totality windows: Assur [22853, 24413], Nineveh [21910, 23705]
    (NASA elements: [22729, 24294] and [21781, 23585]).
  * smh2020 at -762 is 21093 +- 273, so under SMH the eclipse was **not
    total** at Assur or Nineveh. Totality at Nineveh needs Delta-T at least
    817 s (3.0 sigma) higher.
  * This is consistent with the text, but it gives no constraint.
* **-584 May 28 (585 BC)**: Canon comparison only (5.2). The observing site
  is not fixed by the source, so I computed no window.

## 6. New moons

`new_moons()` finds conjunctions in geocentric apparent ecliptic longitude
(true ecliptic of date; Vondrak obliquity) by bracketing on a 1-day grid and
refining with Brent's method. The conjunction nearest the eclipse is
**-1177-04-16 18:05:10 TT**, 5.3 min after greatest eclipse.

Compared with the 24 NASA phase-catalogue new moons of -1178/-1177 (UT +
their Delta-T column 07h59m):

* ours - NASA = **+18.7 min mean, sd 0.4 min**.
* The small scatter shows a pure secular offset.
* The instrument check shows the offset is mostly inside the reference.
  * NASA's phase table puts the conjunction at 17:47:00 TD.
  * NASA's Canon greatest eclipse (17:57:28) plus our 5.3-min gap gives
    18:02:46.
  * So NASA's two products disagree by -15.8 min at -1177.
* Ours minus the Canon-consistent conjunction is +2.4 min, the same
  ephemeris offset as in 5.2.
* The phase pages say they use Meeus' algorithms; that the n-dot treatment
  differs is my inference.

## 7. Planets, Sun and Moon against JPL Horizons

Horizons API, observer tables, topocentric Ithaki (20.72 E, 38.37 N, 0 km),
airless, quantities 1,2,4,20,23,30, `EXTRA_PREC=YES`. My computation used
Horizons' own TDB-UT for each row as Delta-T, so that only the models are
compared.
Horizons uses:
* DE441;
* IAU 1976 (Lieske) precession for 1799-2202 and Owen's long-term model
  outside that range;
* IAU 1980 nutation;
* the IAU 1982 GMST [HZ manual, "Precession Model", "Greenwich Mean
  Sidereal Time"].

| set (Ithaki) | astrometric ICRF | apparent RA*/Dec of date | az*/el | elongation |
|---|---|---|---|---|
| Venus and Mercury, -1177 Apr 10 03:00-04:00 UT (dawn) | 0.000" | +1.4"/+0.6" | -20..-23" / -21..-25" | <= 0.18" |
| Venus and Mercury, -1177 Mar 14 16:30-17:30 UT (dusk) | 0.000" | +1.4"/+0.5" | -17..-19" / +23..+25" | <= 0.14" |
| Venus and Mercury, -1210 Jun 1 02:30-03:30 UT (dawn) | <= 0.001" | +1.4"/-0.2..-0.3" | -22..-27" / -14..-20" | <= 0.17" |
| Sun and Moon, -1177 Apr 16 09:30-10:30 UT | Sun 0.000", Moon 0.175" | +1.5..1.6"/+0.4" | -29..-32" / -1..-12" | <= 0.17" |

* The positions themselves (astrometric, elongation) agree to the
  resolution of Horizons' output.
* Apparent of date (1.4-1.7") = Owen vs Vondrak precession plus IAU 1980
  vs 2000A nutation, plus Horizons' stated -53 mas equinox offset.
* Az/el (<= 32") is mostly the IAU 1982 GMST (+30"), see section 3.
* The Moon's 0.17" astrometric difference is the same Earth-orientation
  difference, seen through the lunar parallax (30" x R_earth/d_moon ~ 0.5"
  at most).
* Using smh2020 Delta-T instead of Horizons' (+125 s) moves Venus'
  altitude at dawn by -0.007 deg.

Example dawn values (Horizons and ours agree to <= 25"):

| -1177 Apr 10 (1178 BC), Ithaki | Venus | Mercury |
|---|---|---|
| elongation | 44.46 deg | 17.27 deg |
| altitude at 03:30 UT (LAT about 04:49) | 8.30 deg | -5.59 deg |

## 8. Caveats (all of them)

1. **Delta-T before -720 has no observations behind it.** Every value at
   -1177 is an extrapolation of a fitted trend, and the authors call the
   oscillatory part conjectural or speculative ([SMH16] sect. 5a, [ADD20]
   sect. 8, Fig. 4). HMNAO's epsilon is an estimate, and treating it as a
   Gaussian 1 sigma is my choice.
2. **SMH's formulations differ by 681 s at -1177**: [ADD20] parabola
   28282, HMNAO integral 28543, [SMH16] parabola 28963. The bench should
   carry this as model uncertainty.
3. **Ephemeris-Delta-T pairing**: DE441 vs DE431 is +188 s at -1177
   (5.3). SMH's own pre-telescopic reductions used j=2 (-26.00), about
   20 s off DE431 [SMH16 Fig. 1]. The HMNAO page (-25.85) and the paper
   (-25.82) disagree slightly on the DE430 n-dot. DE441's n-dot is not
   published [P21].
4. **Sidereal-time convention**: IAU 1982 vs IAU 2006/Vondrak differ by 30"
   = 2 s of time at -1177. Delta-T values reduced with one convention
   carry it, which is negligible.
5. **Precession**: Vondrak's stated accuracy is "a few arcseconds" in the
   historical period [V11]. IAU 2006 differs from it by about 2" at -1177,
   so neither can be preferred at that level.
6. **Nutation** (IAU 2000A) is applied 3,200 years outside its fit span.
   Its amplitude is <= 17", so errors in it are sub-arcsecond in practice;
   this is not checked against an independent reference.
7. **The CIO locator** omits a 2.6-mas periodic term and a 3.8-mas/cy cross
   term (2a), at most 0.01" at -1177.
8. **Stars**:
   * linear space motion over 3,168 years;
   * Hipparcos proper-motion errors (Arcturus +-0.44/0.39 mas/yr, so
     +-1.3" at -1177);
   * the Alcyone RV is quality B (+-1.2 km/s);
   * skyfield omits the light-time change that ERFA models (<= 0.13");
   * no ancient-epoch independent check.
9. **Eclipse radii and limb**: the radii are NASA's k1/k2 and solar 959.63".
   The lunar limb profile is ignored (path edges +-1-2 km). Observer height
   is 0 m. There is no refraction in the eclipse computations.
10. **Sites are modern towns.** The windows move by up to 120 s between
    Ithaki and Lefkada.
11. **New moon** means geocentric apparent conjunction in ecliptic
    longitude. First visibility of the crescent is a different, later
    quantity that this module does not compute.
12. **Horizons' ancient Delta-T** does not follow the formula in its own
    manual (2.1). Use its reported TDB-UT, not the manual's formula.
13. **skyfield's built-in long-term Delta-T** is a hand-tuned patch at
    -1177. The module never uses it implicitly.
14. **Calendars**: the `jplephem excerpt` CLI takes proleptic GREGORIAN
    dates. Everything else here is proleptic Julian.
15. **Secondary sources**:
    * The Morrison & Stephenson 2004 and Huber 2000 uncertainty formulas
      come from Espenak's NASA pages; I did not read the originals.
    * The [HMNAO] page, Table S15 and Table S10 came via the Internet
      Archive, because the UKHO host was down (503) and its HTTPS chain
      failed locally.
    * [ADD20] came via the Internet Archive PDF, because the publisher
      returned 403.

## 9. Module API (odybench/ephem.py)

| function | purpose |
|---|---|
| `jd_from_julian(y,m,d,h)`, `julian_from_jd(jd)`, `fmt_jd(jd, scale)`, `julian_epoch(jd)` | proleptic Julian calendar, astronomical years |
| `delta_t(y, model)`, `delta_t_sigma(y, model)`; models `smh2020` (default), `smh2020_parabola`, `smh2016_parabola`, `em2006`, `em2006_canon`; also `dt_*`, `sigma_*`, `ndot_correction`, `dt_skyfield` | Delta-T with stated uncertainty |
| `timescale(dt)`, `time_ut(jd_ut, dt, precession)`, `time_tt(jd_tt, dt, precession)` | skyfield Times with explicit Delta-T (number, model name or callable) and precession ('vondrak' default or 'iau2006') |
| `apply_precession`, `cio_locator`, `mean_obliquity`, `precession_compare` | long-term precession plus consistent sidereal time |
| `kernel(jd, need)`, `use_ephemeris(dir)` | SPK excerpt selection; switch to DE431 |
| `star(key)`, `HIP_STARS` | Hipparcos stars: alcyone, arcturus, eps_boo, eta_boo |
| `apparent(name, t, lat, lon)`, `altaz(name, jd_ut, lat, lon, dt=..., refraction=False)`, `radec_of_date`, `elongation`, `local_apparent_solar_time` | apparent positions of sun, moon, mercury, venus, mars/jupiter/saturn barycentres and the stars |
| `new_moons(jd_tt0, jd_tt1)` | conjunctions (TT) |
| `besselian(jd_tt, dt)`, `greatest_eclipse(jd_tt)`, `local_circumstances(lat, lon, jd_tt_guess, dt)`, `totality_window(lat, lon, jd_tt_guess, dt_lo, dt_hi)` | solar eclipses |

## 10. Validation output (`py tools/validate_ephem.py`, 2026-10-03, run time 188 s)

```

==============================================================================
0. Software and data
==============================================================================
python 3.14.3  numpy 2.5.0  scipy 1.18.0
skyfield 1.55  jplephem 2.24  pyerfa 2.0.1.5 (ERFA 2.0.1)
de441_m0135_eclipse.bsp             0.09 MB  JD 1671793.5..1671913.5 (-135..-135)  targets [3, 10, 301, 399]
de441_m0584_eclipse.bsp             0.09 MB  JD 1507839.5..1507959.5 (-584..-584)  targets [3, 10, 301, 399]
de441_m0708_eclipse.bsp             0.09 MB  JD 1462598.5..1462718.5 (-708..-708)  targets [3, 10, 301, 399]
de441_m0762_eclipse.bsp             0.09 MB  JD 1442842.5..1442962.5 (-762..-762)  targets [3, 10, 301, 399]
de441_m1320_m1030.bsp              30.04 MB  JD 1238939.5..1344860.5 (-1320..-1030)  targets [1, 2, 3, 4, 5, 6, 10, 199, 299, 301, 399]

==============================================================================
1. Delta-T
==============================================================================
decimal year (Julian epoch) of -1177 Apr 16 = -1176.6776
model                      -1300  -1177.29     -1100     -1050   sigma(-1177) [source of sigma]
smh2020                    30800     28543     27153     26249      720  [HMNAO epsilon table]
smh2020_parabola           30654     28282     26855     25944      541  [+-0.6 tau^2 (eq. 5.1)]
smh2016_parabola           31418     28963     27486     26543      541  [+-0.6 tau^2 (eq. 4.1)]
em2006                     31130     28716     27264     26338     1008  [Huber 2000 (NASA page)]
em2006_canon               30993     28589     27144     26221     1008  [Huber 2000 (NASA page)]
skyfield builtin           31334     28786     27250     26270   (no sigma)
MS2004 0.8u^2 sigma                    718   (formula stated for 1000 BC-AD 1200)
n-dot correction -25.82 -> -25.858 at -1177: +33.9 s;  -26.00 -> -25.82: -160.8 s

1a. HMNAO extrapolated Delta-T table -2000..-800 (hours, 1 decimal) vs dt_smh2020:
   -2000  HMNAO  12.8 h   ours  12.7318 h  rounded  12.7  rounded-up  12.8
   -1900  HMNAO  12.1 h   ours  12.0455 h  rounded  12.0  rounded-up  12.1
   -1800  HMNAO  11.4 h   ours  11.3889 h  rounded  11.4  rounded-up  11.4
   -1700  HMNAO  10.8 h   ours  10.7650 h  rounded  10.8  rounded-up  10.8
   -1600  HMNAO  10.2 h   ours  10.1739 h  rounded  10.2  rounded-up  10.2
   -1500  HMNAO   9.7 h   ours   9.6124 h  rounded   9.6  rounded-up   9.7
   -1400  HMNAO   9.1 h   ours   9.0753 h  rounded   9.1  rounded-up   9.1
   -1300  HMNAO   8.6 h   ours   8.5555 h  rounded   8.6  rounded-up   8.6
   -1200  HMNAO   8.1 h   ours   8.0464 h  rounded   8.0  rounded-up   8.1
   -1100  HMNAO   7.6 h   ours   7.5426 h  rounded   7.5  rounded-up   7.6
   -1000  HMNAO   7.1 h   ours   7.0408 h  rounded   7.0  rounded-up   7.1
    -900  HMNAO   6.6 h   ours   6.5413 h  rounded   6.5  rounded-up   6.6
    -800  HMNAO   6.1 h   ours   6.0470 h  rounded   6.0  rounded-up   6.1
  entries reproduced: rounded-up 13/13, rounded-nearest 5/13

1b. HMNAO spline table -720..+1600 (seconds, nearest 10) vs dt_smh2020:
    -720  HMNAO  20370  ours   20371.8
    -700  HMNAO  20050  ours   20050.1
    -600  HMNAO  18470  ours   18468.5
    -100  HMNAO  11560  ours   11557.7
    1000  HMNAO   1650  ours    1650.4
    1600  HMNAO    110  ours     109.1
  max |ours - HMNAO| over 25 epochs = 5.0 s (table rounded to 10 s)

1c. skyfield-bundled S15 v2020 vs HMNAO file: 58 rows compared, 0 mismatches

1d. NASA Canon Delta-T (Espenak-Meeus with n-dot correction) vs dt_em2006_canon:
  -1177-04-16  Canon  28590.0  ours  28590.0  diff  +0.0 s
   -762-06-15  Canon  21210.6  ours  21210.5  diff  -0.1 s
   -584-05-28  Canon  18383.9  ours  18384.4  diff  +0.5 s
   -135-04-15  Canon  11968.9  ours  11968.8  diff  -0.1 s
   -708-07-17  Canon  20330.0  ours  20330.1  diff  +0.1 s
  NASA phase table prints 07h59m for -1177; dt_em2006 (no n-dot corr.) = +7h58m41.6s

1e. JPL Horizons' own TDB-UT (quantity 30) at sample epochs:
   -2000  Horizons   46100.0   manual formula(T from 1825.0)   45934.7   smh2020   45833.5
   -1500  Horizons   34852.6   manual formula(T from 1825.0)   34726.5   smh2020   34604.1
   -1300  Horizons   30794.1   manual formula(T from 1825.0)   30682.1   smh2020   30799.3
   -1177  Horizons   28423.1   manual formula(T from 1825.0)   28319.4   smh2020   28548.2
   -1100  Horizons   26987.2   manual formula(T from 1825.0)   26888.6   smh2020   27152.6
   -1050  Horizons   26074.8   manual formula(T from 1825.0)   25979.4   smh2020   26248.8
    -800  Horizons   21748.8   manual formula(T from 1825.0)   21668.5   smh2020   21768.5
    -722  Horizons   20479.5   manual formula(T from 1825.0)   20403.8   smh2020   20405.8
    -700  Horizons   20124.6   manual formula(T from 1825.0)   20053.9   smh2020   20049.6
    -500  Horizons   17003.3   manual formula(T from 1825.0)   17012.8   smh2020   16939.1
  quadratic fit to Horizons before -721: 65.80 + 31.457566 ((y - 1825.44)/100)^2, max resid 0.000 s

==============================================================================
2. Precession: Vondrak et al. 2011 (ERFA) vs paper, and vs IAU 2006
==============================================================================
  routine            ERFA (corrected) - paper   typo-C7 port - paper
  ltp_PECL (A.1)       2.71e-09 ( 0.559 mas)     1.11e-16 (0.0000 mas)
  ltp_PEQU (A.2)       2.50e-15 ( 0.000 mas)     2.50e-15 (0.0000 mas)
  ltp_PMAT (A.3)       3.94e-09 ( 0.812 mas)     6.44e-15 (0.0000 mas)
  ltp_PBMAT (A.4)      3.94e-09 ( 0.812 mas)     6.44e-15 (0.0000 mas)
  port with corrected C7 vs ERFA eraLtpecl: 0.0e+00
  (test epoch -1374 May 3 (Gregorian) 13:52:19.2 TT = JD 1219339.078; paper sect. A.5. The paper's test values were made with the C7 = 198.296071 typo that the 2012 corrigendum fixes; ERFA uses 198.296701. The difference is < 1 mas.)

2a. CIO locator s: quadrature along the IAU 2006 pole path + first-order nutation term, vs ERFA eraS06a
    (full IAU 2006/2000A series).  Neglected: a 2.6 mas 18.6-yr term and the 3.8 mas/cy cross term.
   1700.0  ours  -1121.852 mas   eraS06a  -1131.922 mas   diff +10.070 mas
   1800.0  ours   -223.509 mas   eraS06a   -230.580 mas   diff +7.071 mas
   1900.0  ours    -49.039 mas   eraS06a    -48.196 mas   diff -0.843 mas
   2000.0  ours     -2.013 mas   eraS06a     -2.090 mas   diff +0.078 mas
   2100.0  ours     -7.392 mas   eraS06a     -0.991 mas   diff -6.401 mas
   2200.0  ours    366.565 mas   eraS06a    378.023 mas   diff -11.458 mas
  (1 s of Delta-T = 15 000 mas of Earth rotation; these residuals are irrelevant here.)

2b. IAU 2006 (P03) vs Vondrak 2011 at selected epochs:
      epoch  pole sep  rotation  EO V-P03 EO P03 int-poly obl V-P03  (arcsec)
       1000     0.031     0.052    +0.083          +0.036    +0.009
          0     0.212     0.370    +0.367          +0.061    -0.196
       -500     0.509     0.814    +0.695          +0.043    -0.579
      -1000     1.109     1.681    +1.282          -0.032    -1.325
      -1177     1.430     2.139    +1.582          -0.082    -1.710
      -1300     1.696     2.518    +1.825          -0.127    -2.022
      -2000     4.133     5.943    +3.947          -0.603    -4.676
  -> at -1177 the hour-angle (sidereal time) difference is +1.58" = +0.105 s of time; 1 s of Delta-T = 15.04".

2c. Mean sidereal time at -1177 Apr 16 10:00 UT1 (Delta-T 28417.6 s as Horizons), three formulations:
  GMST(IAU 1982, eraGmst82; used by Horizons and, presumably, the NASA Canon) - GMST(Vondrak-consistent) = +30.1"
  GMST(IAU 2006, eraGmst06; skyfield)                                          - GMST(Vondrak-consistent) = +1.6"
  (15" = 1 s of time.  The IAU 1982 expression is a UT1 polynomial tied to IAU 1976 precession.)

==============================================================================
3. Stars: Hipparcos 2007 + space motion to -1177, both precession models
==============================================================================
epoch -1177-03-18 18:00:00 UT (18 Mar 1178 BC, proleptic Julian); Delta-T smh2020 28544 s; site Ithaki 38.37N 20.72E
star         mu tot   shift  sky-ERFA  RV eff   HIP97    RA date   Dec date    dRA*    dDec      alt   dAlt    dAz
alcyone      0.048"  0.042d    0.003"   0.02"   1.77"    13.1418    +9.8009   -0.70   -2.54   12.174  -0.86  -2.60
arcturus     2.279"  2.002d    0.125"  10.96"   2.10"   177.0175   +37.7231   -1.39   +2.28   27.988  +1.21  -2.20
eps_boo      0.055"  0.048d    0.010"   0.16"   3.51"   185.5535   +43.0974   -1.19   +2.44   24.944  +1.25  -2.31
eta_boo      0.361"  0.319d    0.022"   1.90"   5.75"   169.5211   +35.9350   -1.54   +2.10   32.484  +1.18  -2.09
columns: total proper motion ("/yr); angular shift J1991.25 -> -1177 (deg); skyfield vs ERFA eraPmsafe ("); effect of radial velocity ("); HIP1997 vs HIP2007 ("); apparent RA/Dec of date (deg, Vondrak); dRA*=dRA cos dec and dDec, Vondrak - IAU2006 ("); airless altitude (deg) at Ithaki and its Vondrak - IAU2006 difference in alt and az (").
  alcyone: light-time change over -3168 yr = -20.8 d -> expected 0.003", found 0.003"
  arcturus: light-time change over -3168 yr = +20.2 d -> expected 0.126", found 0.125"
  eps_boo: light-time change over -3168 yr = +64.1 d -> expected 0.010", found 0.010"
  eta_boo: light-time change over -3168 yr = -22.3 d -> expected 0.022", found 0.022"

==============================================================================
4. Solar eclipses vs NASA Five Millennium Canon (VSOP87/ELP-2000/82)
==============================================================================

-1177 -1177-04-16 17:59:51 TT (16 Apr 1178 BC, proleptic Julian)  (Canon Delta-T 28590.0 s)
  greatest eclipse TT      ours 17:59:51   Canon 17:57:28   diff +143 s
  gamma                    ours 0.5179     Canon 0.5187    diff -0.0008
  x, y at t0=18h TT       ours -0.24818 +0.45460   Canon -0.22851 +0.46631
  d at t0 (deg)            ours 5.71695   Canon 5.71733
  mu at t0 (ephemeris HA)  ours 90.0791  Canon 90.0876  diff -31" = -2.0 s of time
  GE point (Canon dT)      ours 32.67N 12.19E at 10:03:21 UT   Canon 32.7° N 12.7° E at 10:0:58 UT
  mag (ratio, k2) at GE    ours 1.0600     Canon 1.0599
  central duration at GE   ours 273 s     Canon 04m33s (273 s)
  Sun alt/az at GE         ours 58.6 / 145.5   Canon 58.6 / 145.5

-762 -0762-06-15 14:09:09 TT (15 Jun 763 BC, proleptic Julian)  (Canon Delta-T 21210.6 s)
  greatest eclipse TT      ours 14:09:09   Canon 14:07:32   diff +97 s
  gamma                    ours 0.2720     Canon 0.2715    diff +0.0005
  x, y at t0=14h TT       ours -0.09180 +0.27051   Canon -0.07641 +0.27028
  d at t0 (deg)            ours 22.90269   Canon 22.90360
  mu at t0 (ephemeris HA)  ours 32.0653  Canon 32.0703  diff -18" = -1.2 s of time
  GE point (Canon dT)      ours 38.89N 53.93E at 08:15:38 UT   Canon 38.9° N 54.3° E at 8:14:1 UT
  mag (ratio, k2) at GE    ours 1.0596     Canon 1.0596
  central duration at GE   ours 300 s     Canon 05m00s (300 s)
  Sun alt/az at GE         ours 74.0 / 178.9   Canon 74.0 / 178.9

-584 -0584-05-28 19:29:57 TT (28 May 585 BC, proleptic Julian)  (Canon Delta-T 18383.9 s)
  greatest eclipse TT      ours 19:29:57   Canon 19:28:50   diff +67 s
  gamma                    ours 0.3198     Canon 0.3201    diff -0.0003
  x, y at t0=19h TT       ours -0.37639 +0.21310   Canon -0.36627 +0.21679
  d at t0 (deg)            ours 20.36410   Canon 20.36465
  mu at t0 (ephemeris HA)  ours 107.3403  Canon 107.3441  diff -14" = -0.9 s of time
  GE point (Canon dT)      ours 38.14N -45.28E at 14:23:33 UT   Canon 38.2° N 45.0° W at 14:22:26 UT
  mag (ratio, k2) at GE    ours 1.0798     Canon 1.0798
  central duration at GE   ours 364 s     Canon 06m04s (364 s)
  Sun alt/az at GE         ours 71.2 / 158.5   Canon 71.1 / 158.5

-135 -0135-04-15 09:27:39 TT (15 Apr 136 BC, proleptic Julian)  (Canon Delta-T 11968.9 s)
  greatest eclipse TT      ours 09:27:39   Canon 09:27:08   diff +31 s
  gamma                    ours 0.7118     Canon 0.7119    diff -0.0001
  x, y at t0=9h TT       ours -0.56618 +0.50588   Canon -0.56178 +0.50833
  d at t0 (deg)            ours 8.48565   Canon 8.48555
  mu at t0 (ephemeris HA)  ours 315.2716  Canon 315.2733  diff -6" = -0.4 s of time
  GE point (Canon dT)      ours 46.84N 58.80E at 06:08:10 UT   Canon 46.8° N 58.9° E at 6:7:39 UT
  mag (ratio, k2) at GE    ours 1.0527     Canon 1.0527
  central duration at GE   ours 219 s     Canon 03m39s (219 s)
  Sun alt/az at GE         ours 44.4 / 137.8   Canon 44.4 / 137.8

-708 -0708-07-17 12:30:20 TT (17 Jul 709 BC, proleptic Julian)  (Canon Delta-T 20330.0 s)
  greatest eclipse TT      ours 12:30:20   Canon 12:28:51   diff +89 s
  gamma                    ours 0.4760     Canon 0.4756    diff +0.0004
  x, y at t0=12h TT       ours -0.18015 +0.52827   Canon -0.16639 +0.52473
  d at t0 (deg)            ours 22.77526   Canon 22.77618
  mu at t0 (ephemeris HA)  ours 0.1978  Canon 0.2021  diff -16" = -1.0 s of time
  GE point (Canon dT)      ours 50.48N 86.57E at 06:51:30 UT   Canon 50.5° N 86.9° E at 6:50:1 UT
  mag (ratio, k2) at GE    ours 1.0601     Canon 1.0601
  central duration at GE   ours 265 s     Canon 04m25s (265 s)
  Sun alt/az at GE         ours 61.3 / 198.3   Canon 61.4 / 198.3

==============================================================================
5. -1177 Apr 16: local circumstances at Ithaca, Kefalonia, Lefkada
==============================================================================
5a. Same Delta-T (Canon 28590 s): ours (DE441, direct) vs NASA Besselian elements (independent algorithm)
  Ithaki (Vathy)         max UT ours 10:25:41 NASA 10:22:24 (+197 s); mag ours 0.9751 NASA 0.9839; total False/False; Sun alt 57.2/57.2
  Kefalonia (Argostoli)  max UT ours 10:25:03 NASA 10:21:46 (+197 s); mag ours 0.9755 NASA 0.9844; total False/False; Sun alt 57.4/57.3
  Lefkada (town)         max UT ours 10:26:23 NASA 10:23:06 (+196 s); mag ours 0.9845 NASA 0.9932; total False/False; Sun alt 56.8/56.7

5b. Ithaki as a function of constant Delta-T (DE441, Vondrak precession):
   Delta-T    max UT    LAT    mag   obsc total  dur s Sun alt  Sun az
     26000  11:25:11 12:47  0.783  0.738 False      0    55.6   201.1
     26500  11:13:38 12:35  0.819  0.784 False      0    56.4   196.2
     27000  11:02:07 12:24  0.856  0.831 False      0    56.9   191.0
     27500  10:50:37 12:12  0.893  0.878 False      0    57.2   185.8
     28000  10:39:10 12:01  0.930  0.925 False      0    57.4   180.5
     28500  10:27:44 11:49  0.968  0.971 False      0    57.3   175.2
     29000  10:16:21 11:38  1.006  1.000  True    162    57.0   170.0
     29500  10:05:01 11:26  1.016  1.000  True    237    56.5   164.9
     30000  09:53:43 11:15  0.978  0.982 False      0    55.8   160.0
     30500  09:42:28 11:04  0.940  0.938 False      0    55.0   155.3
     31000  09:31:15 10:53  0.903  0.891 False      0    54.0   150.8
     31500  09:20:06 10:41  0.866  0.843 False      0    52.9   146.6
     32000  09:09:00 10:30  0.829  0.797 False      0    51.6   142.5

5c. Delta-T windows for TOTALITY (constant Delta-T, 0.5 s):
  Ithaki (Vathy)         DE441: [28922, 29706] (width 784 s, mid 29314)
                         NASA elements: [28801, 29585]
  Kefalonia (Argostoli)  DE441: [28916, 29697] (width 782 s, mid 29306)
                         NASA elements: [28794, 29576]
  Lefkada (town)         DE441: [28801, 29591] (width 790 s, mid 29196)
                         NASA elements: [28680, 29470]
  Delta-T models at -1177.29 (value +- stated 1 sigma):
    smh2020              28543 +-  720   Ithaki window mid - model =   +771 s = +1.07 sigma
    smh2020_parabola     28282 +-  541   Ithaki window mid - model =  +1033 s = +1.91 sigma
    smh2016_parabola     28963 +-  541   Ithaki window mid - model =   +351 s = +0.65 sigma
    em2006               28716 +- 1008   Ithaki window mid - model =   +598 s = +0.59 sigma
    em2006_canon         28589 +- 1008   Ithaki window mid - model =   +725 s = +0.72 sigma
    Horizons TDB-UT      28423 (at -1177 Jan 1)

5d. Self-check: Delta-T change == longitude shift (exact in this formulation)
  mag 0.940154 vs 0.940154;  max TT diff +0.001 s

5e. Which lunar ephemeris?  SMH's Delta-T is tied to DE430 / analytical j=2 (n-dot -25.82 / -26.00).
    DE431 (same lunar model as DE430, long span) vs DE441, greatest-eclipse TT:
  -135   DE441 - DE431 =   +55.8 s   (Moon-Sun elongation rate 0.573"/s ->  +31.9" along-track);  gamma 0.71178 vs 0.71210
  -708   DE441 - DE431 =  +115.2 s   (Moon-Sun elongation rate 0.578"/s ->  +66.6" along-track);  gamma 0.47603 vs 0.47538
  -762   DE441 - DE431 =  +122.9 s   (Moon-Sun elongation rate 0.570"/s ->  +70.1" along-track);  gamma 0.27202 vs 0.27133
  -1177  DE441 - DE431 =  +187.7 s   (Moon-Sun elongation rate 0.575"/s -> +107.9" along-track);  gamma 0.51793 vs 0.51900
  fit Moon(DE441) - Moon(DE431) = 0.5 b T^2: coefficient -0.19251, residuals +11.9" +3.9" +3.4" -10.8"  (T in Julian centuries from J2000)
  fit Moon(DE441) - Moon(DE431) = k T^3: coefficient +0.00335, residuals +0.7" -0.1" +0.5" -0.5"  (T in Julian centuries from J2000)

5f. Totality windows at the three sites with DE431, and the chance of totality under each Delta-T model
    (Gaussian with the model's stated sigma; window = constant Delta-T range giving totality):
  Ithaki (Vathy)         DE441 [28922, 29706]   DE431 [28761, 29545]   shift +161/+161 s
  Kefalonia (Argostoli)  DE441 [28916, 29697]   DE431 [28754, 29536]   shift +161/+161 s
  Lefkada (town)         DE441 [28801, 29591]   DE431 [28640, 29430]   shift +161/+161 s
  P(total at site)               Ithaki 441       Ithaki 431    Kefalonia 441    Kefalonia 431      Lefkada 441      Lefkada 431
  smh2020             28543+- 720            0.246            0.299            0.248            0.301            0.287            0.337
  smh2020_parabola    28282+- 541            0.114            0.178            0.116            0.181            0.161            0.237
  smh2016_parabola    28963+- 541            0.445            0.505            0.448            0.505            0.495            0.531
  em2006              28716+-1008            0.256            0.277            0.256            0.277            0.274            0.291
  em2006_canon        28589+-1008            0.237            0.261            0.237            0.261            0.257            0.278
  (em2006/em2006_canon sigma is Huber's 1008 s; with MS2004's 0.8u^2 = 718 s the numbers change little)

5g. Where the central line crosses Ithaki's meridian (20.72E), DE441 and DE431, by Delta-T:
  Delta-T   27823: central line at  43.75N (DE441),  43.24N (DE431); Ithaki is   -599 /   -542 km north of it (along the meridian)
  Delta-T   28543: central line at  41.30N (DE441),  40.72N (DE431); Ithaki is   -326 /   -262 km north of it (along the meridian)
  Delta-T   29263: central line at  38.58N (DE441),  37.93N (DE431); Ithaki is    -23 /    +49 km north of it (along the meridian)
  Delta-T   29314: central line at  38.37N (DE441),  37.72N (DE431); Ithaki is     -0 /    +73 km north of it (along the meridian)

==============================================================================
6. Historical eclipses with observations: totality windows vs published Delta-T
==============================================================================

-135 Babylon (32.54N 44.42E)  [SMH Table S10 v2020 (total at Babylon)]
  totality window DE441 (ours):   [11259, 12170]
  totality window NASA elements: [11232, 12143]
  published SMH bounds:           [11220, 12140]
  DE441 - SMH: lower +39 s, upper +30 s
  totality window DE431:          [11214, 12126]
  DE431 - SMH: lower -6 s, upper -14 s
  Delta-T models: smh2020 11968 +- 103; em2006 12025; em2006_canon 11968

-708 Qufu (Lu) (35.6N 116.99E)  [SMH Table S10 v2020 (total, China)]
  totality window DE441 (ours):   [20271, 21198]
  totality window NASA elements: [20197, 21124]
  published SMH bounds:           [20160, 21100]
  DE441 - SMH: lower +111 s, upper +98 s
  totality window DE431:          [20176, 21103]
  DE431 - SMH: lower +16 s, upper +3 s
  Delta-T models: smh2020 20169 +- 174; em2006 20421; em2006_canon 20329

-762 Assur (35.46N 43.26E)  [Assyrian eponym chronicle (no totality stated)]
  totality window DE441 (ours):   [22853, 24413]
  totality window NASA elements: [22729, 24294]
  Delta-T models: smh2020 21093 +- 273; em2006 21305; em2006_canon 21210

-762 Nineveh (36.36N 43.15E)  [Assyrian eponym chronicle (no totality stated)]
  totality window DE441 (ours):   [21910, 23705]
  totality window NASA elements: [21781, 23585]
  Delta-T models: smh2020 21093 +- 273; em2006 21305; em2006_canon 21210

==============================================================================
7. New moons (conjunctions in apparent ecliptic longitude) vs NASA phase catalogue
==============================================================================
  24 NASA new moons in -1178/-1177 matched to ours (TT); NASA UT + 07h59m (their Delta-T column)
  ours - NASA (minutes): mean +18.7, sd 0.4, min +17.9, max +19.3
  (NASA times are rounded to 1 min and computed with Meeus' truncated series; Delta-T column rounded to 1 min)
  conjunction nearest the eclipse: -1177-04-16 18:05:10 TT (16 Apr 1178 BC, proleptic Julian)
  instrument check: our conjunction comes +5.3 min after our greatest eclipse; applying the same gap to the
  Canon's own greatest eclipse (17:57:28 TD) predicts a Canon-consistent conjunction at 18:02:46 TD, but the phase catalogue gives 17:47:00 TD:
  NASA's two products disagree by -15.8 min, i.e. most of the +18.7 min offset is internal to the reference (Meeus' phase series without the Canon's n-dot treatment), and ours - Canon-consistent = +2.4 min.

==============================================================================
8. Planets, Sun, Moon vs JPL Horizons (topocentric Ithaki, airless)
==============================================================================
body                       UT    dT_HZ |  astrom |  appRA*  appDec |     dAz     dEl | P03 dAz P03 dEl |    elong d elong |   el(HZ)   el smh
venus     -1177-04-10 03:00:0  28417.9 |   0.000 |   +1.39   +0.59 |  -20.58  -22.79 |  -21.47  -21.77 |  44.4636   +0.06 |    2.913    2.906
venus     -1177-04-10 03:30:0  28417.9 |   0.000 |   +1.39   +0.59 |  -21.51  -21.92 |  -22.35  -20.86 |  44.4613   -0.01 |    8.298    8.291
venus     -1177-04-10 04:00:0  28417.9 |   0.000 |   +1.39   +0.59 |  -22.58  -20.81 |  -23.37  -19.71 |  44.4590   -0.06 |   13.455   13.448
mercury   -1177-04-10 03:00:0  28417.9 |   0.000 |   +1.40   +0.55 |  -19.89  -24.50 |  -21.22  -22.65 |  17.2879   +0.08 |  -11.471  -11.479
mercury   -1177-04-10 03:30:0  28417.9 |   0.000 |   +1.40   +0.55 |  -19.90  -24.49 |  -21.23  -22.64 |  17.2702   +0.16 |   -5.593   -5.600
mercury   -1177-04-10 04:00:0  28417.9 |   0.000 |   +1.40   +0.55 |  -20.12  -24.32 |  -21.43  -22.45 |  17.2525   +0.18 |    0.265    0.257
venus     -1177-03-14 16:30:0  28419.3 |   0.000 |   +1.45   +0.51 |  -16.60  +24.94 |  -16.56  +25.14 |  46.1329   +0.05 |  -43.507  -43.499
venus     -1177-03-14 17:00:0  28419.3 |   0.000 |   +1.45   +0.51 |  -17.35  +24.42 |  -17.33  +24.62 |  46.1329   -0.08 |  -49.257  -49.249
venus     -1177-03-14 17:30:0  28419.3 |   0.000 |   +1.44   +0.51 |  -18.62  +23.47 |  -18.60  +23.67 |  46.1328   +0.14 |  -54.833  -54.826
mercury   -1177-03-14 16:30:0  28419.3 |   0.000 |   +1.39   +0.58 |  -16.77  +25.21 |  -15.89  +25.79 |  26.5246   -0.14 |  -25.994  -25.986
mercury   -1177-03-14 17:00:0  28419.3 |   0.000 |   +1.39   +0.58 |  -16.76  +25.21 |  -15.89  +25.79 |  26.5297   -0.03 |  -31.875  -31.867
mercury   -1177-03-14 17:30:0  28419.3 |   0.000 |   +1.39   +0.58 |  -17.02  +25.04 |  -16.15  +25.63 |  26.5348   -0.02 |  -37.736  -37.728
venus     -1210-06-01 02:30:0  29041.9 |   0.000 |   +1.45   -0.20 |  -25.17  -17.00 |  -26.25  -15.52 |  16.9794   -0.17 |  -15.729  -15.735
venus     -1210-06-01 03:00:0  29041.9 |   0.000 |   +1.45   -0.20 |  -23.79  -18.88 |  -24.98  -17.50 |  16.9850   +0.17 |  -11.716  -11.722
venus     -1210-06-01 03:30:0  29041.9 |   0.000 |   +1.45   -0.20 |  -22.43  -20.47 |  -23.72  -19.18 |  16.9908   -0.16 |   -7.310   -7.316
mercury   -1210-06-01 02:30:0  29041.9 |   0.001 |   +1.43   -0.29 |  -26.92  -13.91 |  -27.75  -12.73 |  26.2760   -0.06 |  -20.225  -20.230
mercury   -1210-06-01 03:00:0  29041.9 |   0.001 |   +1.43   -0.29 |  -25.58  -16.25 |  -26.52  -15.14 |  26.2775   -0.16 |  -16.878  -16.883
mercury   -1210-06-01 03:30:0  29041.9 |   0.001 |   +1.43   -0.29 |  -24.19  -18.25 |  -25.21  -17.22 |  26.2789   +0.05 |  -13.040  -13.046
sun       -1177-04-16 09:30:0  28417.6 |   0.000 |   +1.46   +0.43 |  -29.28  -11.91 |  -29.50   -9.25 |   0.0000   +0.00 |   53.872   53.868
sun       -1177-04-16 10:00:0  28417.6 |   0.000 |   +1.46   +0.43 |  -30.83   -6.96 |  -30.62   -4.30 |   0.0000   +0.00 |   56.222   56.220
sun       -1177-04-16 10:30:0  28417.6 |   0.000 |   +1.46   +0.43 |  -31.59   -1.19 |  -30.89   +1.39 |   0.0000   +0.00 |   57.302   57.302
moon      -1177-04-16 09:30:0  28417.6 |   0.169 |   +1.62   +0.39 |  -29.53  -11.75 |  -29.73   -9.05 |   0.4187   -0.02 |   53.761   53.760
moon      -1177-04-16 10:00:0  28417.6 |   0.174 |   +1.63   +0.39 |  -31.03   -6.88 |  -30.79   -4.19 |   0.2092   -0.17 |   56.151   56.155
moon      -1177-04-16 10:30:0  28417.6 |   0.175 |   +1.63   +0.40 |  -31.76   -1.21 |  -31.04   +1.40 |   0.0360   -0.04 |   57.331   57.340
columns: Horizons TDB-UT used as our Delta-T (s); |ours - HZ| astrometric ICRF position ("); apparent RA* and Dec of date, ours(Vondrak) - HZ ("); az* and el, ours(Vondrak) - HZ ("); the same with IAU 2006 precession; Horizons S-O-T elongation (deg) and ours - HZ (", HZ prints 4 decimals = 0.36"); HZ elevation (deg) and ours with smh2020 Delta-T instead of Horizons' (deg).
worst |diff|: astrometric 0.001" (Moon 0.175"), apparent of date 1.68", az/el 31.78", elongation 0.18"

==============================================================================
9. Summary of checks
==============================================================================
  [PASS] HMNAO -2000..-800 table reproduced (rounded up)  13/13
  [PASS] HMNAO -720..1600 spline table reproduced  5.0 s
  [PASS] S15 v2020 coefficients identical to HMNAO file  58 rows
  [PASS] Canon Delta-T -1177  +0.0 s
  [PASS] Canon Delta-T -762  -0.1 s
  [PASS] Canon Delta-T -584  +0.5 s
  [PASS] Canon Delta-T -135  -0.1 s
  [PASS] Canon Delta-T -708  +0.1 s
  [PASS] Vondrak test case ltp_PECL (A.1) (typo-C7 port reproduces paper to double precision)  1.1e-16
  [PASS] Vondrak test case ltp_PECL (A.1) (ERFA within corrigendum effect)  2.7e-09
  [PASS] Vondrak test case ltp_PEQU (A.2) (typo-C7 port reproduces paper to double precision)  2.5e-15
  [PASS] Vondrak test case ltp_PEQU (A.2) (ERFA within corrigendum effect)  2.5e-15
  [PASS] Vondrak test case ltp_PMAT (A.3) (typo-C7 port reproduces paper to double precision)  6.4e-15
  [PASS] Vondrak test case ltp_PMAT (A.3) (ERFA within corrigendum effect)  3.9e-09
  [PASS] Vondrak test case ltp_PBMAT (A.4) (typo-C7 port reproduces paper to double precision)  6.4e-15
  [PASS] Vondrak test case ltp_PBMAT (A.4) (ERFA within corrigendum effect)  3.9e-09
  [PASS] s vs eraS06a at 1700.0 (< 20 mas)  +10.1 mas
  [PASS] s vs eraS06a at 1800.0 (< 20 mas)  +7.1 mas
  [PASS] s vs eraS06a at 1900.0 (< 20 mas)  -0.8 mas
  [PASS] s vs eraS06a at 2000.0 (< 20 mas)  +0.1 mas
  [PASS] s vs eraS06a at 2100.0 (< 20 mas)  -6.4 mas
  [PASS] s vs eraS06a at 2200.0 (< 20 mas)  -11.5 mas
  [PASS] star alcyone: skyfield vs ERFA pmsafe (= Roemer light-time term)  0.003" vs 0.003"
  [PASS] star arcturus: skyfield vs ERFA pmsafe (= Roemer light-time term)  0.125" vs 0.126"
  [PASS] star eps_boo: skyfield vs ERFA pmsafe (= Roemer light-time term)  0.010" vs 0.010"
  [PASS] star eta_boo: skyfield vs ERFA pmsafe (= Roemer light-time term)  0.022" vs 0.022"
  [PASS] -1177 gamma vs Canon  -0.0008
  [PASS] -1177 GE time vs Canon  +143 s
  [PASS] -1177 magnitude vs Canon  +0.0001
  [PASS] -1177 duration vs Canon  -0 s
  [PASS] -762 gamma vs Canon  +0.0005
  [PASS] -762 GE time vs Canon  +97 s
  [PASS] -762 magnitude vs Canon  +0.0000
  [PASS] -762 duration vs Canon  +0 s
  [PASS] -584 gamma vs Canon  -0.0003
  [PASS] -584 GE time vs Canon  +67 s
  [PASS] -584 magnitude vs Canon  +0.0000
  [PASS] -584 duration vs Canon  +0 s
  [PASS] -135 gamma vs Canon  -0.0001
  [PASS] -135 GE time vs Canon  +31 s
  [PASS] -135 magnitude vs Canon  -0.0000
  [PASS] -135 duration vs Canon  -0 s
  [PASS] -708 gamma vs Canon  +0.0004
  [PASS] -708 GE time vs Canon  +89 s
  [PASS] -708 magnitude vs Canon  +0.0000
  [PASS] -708 duration vs Canon  -0 s
  [PASS] Delta-T / longitude equivalence  
  [PASS] -135 Babylon DE431 totality window vs SMH (< 60 s)  -6/-14 s
  [PASS] -708 Qufu (Lu) DE431 totality window vs SMH (< 60 s)  +16/+3 s
  [PASS] new moons: scatter vs NASA phases < 1 min (offset explained above)  sd 0.40 min
  [PASS] new moons: ours vs Canon-consistent conjunction < 5 min  +2.4 min
  [PASS] Horizons astrometric Sun/Venus/Mercury < 0.01"  0.001"
  [PASS] Horizons astrometric Moon < 0.5" (observer-orientation parallax)  0.175"
  [PASS] Horizons elongation < 1"  0.18"
  [PASS] Horizons az/el < 60" (model differences)  31.8"

55/55 passed; run time 188 s
```

## Sources

* Stephenson, F.R., Morrison, L.V., Hohenkerk, C.Y. 2016, Measurement of the Earth's rotation: 720 BC to AD 2015, Proc. R. Soc. A 472:20160404 - full text https://pmc.ncbi.nlm.nih.gov/articles/PMC5247521/ (eq. 4.1, 5.1; sect. 3a, 5a; Fig. 1).
* Morrison, L.V., Stephenson, F.R., Hohenkerk, C.Y., Zawilski, M. 2021, Addendum 2020 to 'Measurement of the Earth's rotation: 720 BC to AD 2015', Proc. R. Soc. A 477:20200776 - PDF via https://web.archive.org/web/20241009205824/https://royalsocietypublishing.org/doi/pdf/10.1098/rspa.2020.0776 (eq. 5.1, 5.2; sect. 6, 8; Fig. 4).
* HM Nautical Almanac Office, Earth Rotation - Delta-T & lod from -2000 to +2500, http://astro.ukho.gov.uk/nao/lvm/ (archived https://web.archive.org/web/20220320003423/http://astro.ukho.gov.uk/nao/lvm/), Table-S15.2020.txt, Table-S10.2020.txt.
* Espenak, F. & Meeus, J. (NASA GSFC): Polynomial Expressions for Delta T https://eclipse.gsfc.nasa.gov/SEcat5/deltatpoly.html ; Uncertainty in Delta T https://eclipse.gsfc.nasa.gov/SEcat5/uncertainty.html ; Five Millennium Catalog https://eclipse.gsfc.nasa.gov/SEcat5/SE-1199--1100.html (also -0799--0700, -0599--0500) ; Besselian elements https://eclipse.gsfc.nasa.gov/SEsearch/SEdata.php?Ecl=-11770416 (and -07620615, -05840528, -01350415, -07080717) ; Phases of the Moon -1199..-1100 https://eclipse.gsfc.nasa.gov/phase/phases-1199.html . "Eclipse Predictions by Fred Espenak, NASA's GSFC".
* Vondrak, J., Capitaine, N., Wallace, P. 2011, New precession expressions, valid for long time intervals, A&A 534, A22 (App. A.5 test case; sect. 6-7) and Corrigendum, A&A 541, C1 (2012) - PDFs via the Internet Archive copies of https://www.aanda.org/articles/aa/pdf/2011/10/aa17274-11.pdf and https://www.aanda.org/articles/aa/pdf/2012/05/aa17274e-11.pdf .
* ERFA (liberfa/erfa) source ltpecl.c, ltp.c, ltpb.c - https://github.com/liberfa/erfa ; pyerfa 2.0.1.5.
* Park, R.S., Folkner, W.M., Williams, J.G., Boggs, D.H. 2021, The JPL Planetary and Lunar Ephemerides DE440 and DE441, AJ 161:105 - https://ssd.jpl.nasa.gov/doc/Park.2021.AJ.DE440.pdf ; kernels https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/ (de441_part-1.bsp, de431_part-1.bsp).
* JPL Horizons manual https://ssd.jpl.nasa.gov/horizons/manual.html (sections Long-Term Ephemerides, Precession Model, Universal Time, GMST) and API https://ssd.jpl.nasa.gov/api/horizons.api (responses cached in data/ephem/horizons/).
* Hipparcos new reduction, van Leeuwen 2007, VizieR I/311/hip2; Hipparcos 1997, VizieR I/239/hip_main - https://vizier.cds.unistra.fr ; radial velocities from SIMBAD TAP https://simbad.cds.unistra.fr/simbad/sim-tap (bibcodes in section 4).
* Liu, Y.T., DeltaT (Python implementation of SMH2016/Addendum 2020 fits and the HMNAO error table) https://github.com/ytliu0/DeltaT - used only to cross-check the integration constant (+1.0077 s) and the epsilon table.
* skyfield 1.55 (Rhodes) source: timelib.build_delta_t, earthlib.sidereal_time, precessionlib.compute_precession, starlib.Star; jplephem 2.24 commandline.parse_date / excerpter.
