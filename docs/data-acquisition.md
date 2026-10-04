# Data acquisition and validation (2026-10-04)

Task: extend the ephemeris to −2060..+240, fetch the DE431 excerpts and the
NASA Canon elements the eclipse work needs, fetch and verify the star data,
and write an exact calendar module. The plan is DESIGN §7.3. The review
issues addressed are critique-design issues 10 (background to −1999),
13 (calendar property tests, no `datetime`), 22 (calendar and epoch
conventions) and 25 (HIP numbers, Sirius proper motion).

Tags: **[eph]** docs/research-ephemeris.md; **[DESIGN]**; **[crit]**
docs/critique-design.md; **[me: script]** computed by me with the named
script, whose output is in `results/data-acquisition/`. Years are
astronomical (1178 BC = −1177). Calendar dates are proleptic Julian
unless marked otherwise.

## 0. Summary

1. **Ephemeris.** One DE441 excerpt now covers −2060-01-01 to +241-01-01
   (Julian) with the same 11 bodies as before: 237.9 MB in a single
   Range-request excerpt, which is under the 300 MB limit.
   * DE431 Sun, Earth and Moon now cover the same span in two pieces,
     because NAIF splits DE431 at AD 1 Jan 3.
   * There are new DE431 ±60-day excerpts for −1339 Jan 8 and −647 Apr 6.
   * `ephem.kernel()` now prefers the shortest excerpt that covers a
     request, so every request the old excerpts served still goes to
     the same file.
   * The long excerpts hold bit-identical Chebyshev records for those
     dates.
   * Rerunning `validate_ephem.py` gives 55/55 and the same output line
     for line, except the new file listing and the run time.
     `test_ephem.py` gives 10/10.
   * 68 module results computed before and after the change are equal
     to the last bit.
   * Spot checks against JPL Horizons at four dates over −1999..+200
     pass: astrometric Sun, Venus and Mercury agree to ≤ 0.0022″.
2. **Eclipse elements.** NASA Five Millennium Canon Besselian elements
   are on disk for −1999..+300: 23 century files, 5,486 eclipses.
   * They are checked against NASA's catalogue pages: every eclipse
     matches, with gamma ≤ 0.00005, time ≤ 0.5 s and ΔT ≤ 0.5 s.
   * Site catalogues for Ithaca, Kefalonia, Lefkada, Corfu and Zakynthos
     span the whole range. Over −1499..−600 they reproduce the earlier
     window catalogue row for row.
3. **Stars.** 21 stars are in `data/stars.json`: the 9 grammar stars and
   12 extras for the Hyades, Orion and Boötes.
   * **Every HIP number was read from SIMBAD's identifier list and checked
     against the Hipparcos row.** All five numbers that DESIGN gave from
     memory are correct: Sirius 32349, Aldebaran 21421, Betelgeuse 27989,
     Rigel 24436, Dubhe 54061.
   * **Sirius:** the Hipparcos solution for HIP 32349 is already an
     orbital solution referred to the **centre of mass**. Its proper motion
     is therefore already orbit-corrected and barycentric, and that is the
     value adopted.
   * Had a photocentre motion been used, Sirius would have been
     **24.2′** off at −1177; this is the error critique issue 25 warned
     about.
   * The long-baseline FK5 motion differs from the adopted value by
     **0.99′** at −1177. Re-referring the Hipparcos value to the modern
     orbit of Bond et al. 2017 moves it by 1.02′.
4. **Calendar.** `odybench/calendar.py` handles the proleptic Julian
   calendar and JD conversions, the leap rule, day of year, UT+2, LMT and
   LAT civil dates, and time-scale helpers. It uses no `datetime`.
   * `tests/test_calendar.py`: 11 tests pass.
   * Every day of −1999..+500 (913,125 days) is checked against
     independent day counting from the definition of JD 0.
   * Meeus examples 7.a–7.f and the Meeus ch. 7 table pass.
   * The identity −1177-04-16 0h = JD 1291263.5 holds.
   * 306/306 calendar dates printed by Horizons are reproduced.
   * A mutation check confirmed that the tests can fail.

## 1. Ephemeris excerpts

### 1.1 What was fetched

Everything was fetched by `py tools/fetch_ephem.py` (extended), from
`https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/`:
* only the byte ranges needed, by HTTP Range requests of at most 8 MB, with
  retries;
* no single excerpt over 300 MB;
* about 408 MB downloaded in all, in about 71 s [me: fetch_ephem.out.txt].

JD bounds are 0h TDB. "Julian" dates are proleptic Julian.

| file | source | span | targets | bytes | SHA-256 |
|---|---|---|---|---|---|
| `data/ephem/de441_m2060_p0241.bsp` **new** | de441_part-1.bsp | JD 968642.5–1809083.5 = −2060-01-01 .. +241-01-01 Julian | 1,2,3,4,5,6,10,199,299,301,399 | 237,911,792 | 7c0028c6d24a85245e4f91167fabd1ad8d294d50343f7fd02f5e7dcc88a4861b |
| `data/ephem/de431/de431_m2060_p0001.bsp` **new** | de431_part-1.bsp | JD 968642.5–1721425.5 = −2060-01-01 .. +1-01-03 Julian (end of part-1) | 3,10,301,399 | 152,067,856 | ee7d778ba9c5568251e4ef2f608caad8b170919b3c2bf009d3bd1f4414a714a4 |
| `data/ephem/de431/de431_p0001_p0241.bsp` **new** | de431_part-2.bsp | JD 1721425.5–1809083.5 = +1-01-03 .. +241-01-01 | 3,10,301,399 | 17,711,696 | ccef82788fda2ddba14ee17269552a462a88d517e1dd2b2a65b442d6d77410ba |
| `data/ephem/de431/de431_m1339_eclipse.bsp` **new** | de431_part-1.bsp | −1339 Jan 8 ± 60 d (JD 1231935.5–1232055.5) | 3,10,301,399 | 30,032 | b74334404f2e812e90d0a339ad5aa90037139a43c15151d2cb9ef7a14d6161a6 |
| `data/ephem/de431/de431_m0647_eclipse.bsp` **new** | de431_part-1.bsp | −647 Apr 6 ± 60 d (JD 1484776.5–1484896.5) | 3,10,301,399 | 30,032 | d7bca73744765c63d4de38b761fb05a37abd44634e7f690f2670ae205f38885f |
| `data/ephem/de441_m1320_m1030.bsp` (2026-10-03) | de441_part-1.bsp | JD 1238939.5–1344860.5 | 11 bodies | 30,043,552 | a88827c54695d96e94274060013f7abe85641d3876b3c8d244fc9a8277864455 |
| `data/ephem/de431/de431_m1320_m1030.bsp` (2026-10-03) | de431_part-1.bsp | same | 1,2,3,10,199,299,301,399 | 27,758,048 | 076e0360f01c0a7829664ae319c0c82c743ffcd8e25620b7be8a7dedb54643c7 |

The +60-day eclipse excerpts from 2026-10-03 are unchanged. Their hashes are
in `data/SHA256SUMS`.

Choices and facts:

* **Span.** I took −2060..+240, as the task asked, wider than DESIGN
  §7.3's −1560..+230. That reaches the first NASA Canon year (−1999) with
  60 years of margin for the 40-day clue offsets and the ±60-day Mercury
  searches [crit issue 10, fix 2]. A Gregorian-free JD bound is used:
  `jd_from_julian(-2060, 1, 1)`.
* **Size.** The DE441 records for the span come to 237.8 MB [me:
  results/data-acquisition/probe_spk.py]. The Moon and Earth take 68.9 MB
  each and Mercury 37.0 MB. That is under 300 MB, so one excerpt, and
  requests never have to straddle a file boundary.
* **DE431 Sun/Earth/Moon only.** The planets (1, 2, 199, 299) would add
  45 MB. DE431 exists in the bench only for the eclipse and Delta-T pairing
  [eph §5.3], so they are left out. A DE431 request for Venus outside
  −1320..−1030 raises `LookupError`.
* **DE431 split.** NAIF's own merge log puts the end of
  `de431_part-1.bsp` at "1 A.D. JAN 01" (Gregorian), which is JD 1721425.5
  and AD 1 Jan 3 Julian [data/ephem/de431/de431_part-1_comments.txt; the
  segments read JD 1721425.5 in the remote file]. **No DE431 request may
  straddle that instant.** There is no solar eclipse within days of it, so
  the eclipse work is unaffected.
* **The −1339 and −647 excerpts** follow DESIGN §7.3: the Gainsford-list
  eclipse and Archilochus. The dates are the Canon's: −1339 Jan 8 is in
  `results/window/jsex/windows-out.txt`, and the −647 Apr 6 element has
  T0 JD 1484837.079 in SEm0699. Both are also inside the long DE431
  excerpt, and their records are bit-identical to it (1.3).

### 1.2 How `odybench.ephem` uses the new coverage

`kernel(jd, need)` used to return the first excerpt, in file-name order,
that covered the request. It now returns the one with the **shortest
span** among those that cover the request and hold the needed bodies;
ties go by name. `coverage(dir)` lists the excerpts in that order.
Consequences:

* Every request the pre-task excerpts could serve still goes to the same
  file: 4,500/4,500 random requests [me: validate_coverage.py §2].
* Requests outside them now succeed: 883 of 1,000 random one-day requests
  in −2050..+230 can only be served by the new files (DE441 and DE431
  directories together).
* No computed value changes. The two rules pick the same file for every
  old-coverage request, and the long excerpts hold the same records (1.3).
* Only the module docstring, `kernel()`, the new `coverage()` and the star
  loader (§3.4) were edited. Nothing else in `ephem.py` changed. The
  pre-task file is kept as `results/data-acquisition/ephem_orig.py`, with
  SHA-256 1b7b5667…ed0f05d.

### 1.3 Validation

| check | reference | result | source |
|---|---|---|---|
| `tools/validate_ephem.py` rerun (55 checks, every date it tests) | its 2026-10-03 output `results/validate_ephem.txt` | **55/55, identical line for line** except the new file in the §0 listing and the run time (118 s against 188 s). Run with `PYTHONIOENCODING=utf-8`: a cp1252 console garbles the degree signs in §4 | `results/data-acquisition/validate_ephem.after.txt`, `validate_ephem.diff.txt` (2 differing lines) |
| `tests/test_ephem.py` rerun | its pre-change run | **10/10**, identical except timings | `test_ephem.before.txt`, `test_ephem.after.txt`, `test_ephem.diff.txt` |
| kernel choice | pre-task rule on pre-task files | 4,500/4,500 identical | validate_coverage §2 |
| Chebyshev records | each narrow excerpt vs the long excerpt of the same ephemeris (11 pairs, all segments) | all **bit-identical** (`np.array_equal`) | §3 |
| segment evaluation | 2,000 random instants per pair, all segments | max difference **0.000 km** | §4 |
| module results before/after | pre-task `ephem.py` vs current: 68 results covering altaz, elongation, Besselian elements, 5 greatest eclipses, local circumstances (DE441 and DE431), the −135 Babylon DE431 totality window, new moons and the 4 Hipparcos stars | **68/68 identical to the last bit** | §5 |
| DE441 is DE441 and DE431 is DE431 over the new span | the dossier's law Moon(DE441) − Moon(DE431) = +0.00335″ T³ [eph §5.3], fitted on −1177..−135 | conjunction shifts +374 s (−1999) .. +36 s (+200); along-track ratio to the law 0.85–1.03 at 7 epochs. The scatter is ≤ 15%, probably from periodic terms; the law was fitted on 4 eclipses. **PASS** (criterion 0.8–1.2) | §6 |
| JPL Horizons, Sun/Moon/Venus/Mercury at 4 dates (below) | Horizons API, DE441, topocentric Ithaki 38.37 N 20.72 E, airless; our run uses Horizons' own TDB−UT as ΔT | astrometric Sun/Venus/Mercury ≤ **0.0022″** (< 0.01″ required); Moon ≤ 0.524″ (< 3″); elongation ≤ 0.57″ (< 1″); az/el within the IAU 1982 vs Vondrak sidereal-time difference + 20″ at all 4 dates | §7 |
| calendar dates | Horizons' own calendar for 306 random UT instants in −1999..+500 | **306/306** | §8 |

Tolerances for the Horizons spot checks were fixed in the script before it
first ran: the astrometric and elongation limits are those of
`validate_ephem.py`. The az/el limit is |GMST82 − GMST(ours)| + 20″,
because Horizons uses the IAU 1982 sidereal time [eph §3]. The script
prints that difference for each date.

Horizons spot checks: worst residuals per date, ours − Horizons [me:
validate_coverage.py §7]:

| date (UT) | ΔT used (Horizons TDB−UT) | astrometric ICRF (Sun/Ven/Mer; Moon) | apparent RA*/Dec of date | az*/el | GMST82 − ours | elongation |
|---|---|---|---|---|---|---|
| −1999 Jun 12 02:30–03:30 (day of the Canon's first eclipse) | 46065.2 s | 0.002″; 0.52″ | 2.0–2.9″ | ≤ 78″ | +79.5″ | ≤ 0.57″ |
| −1450 Mar 20 04:00–05:00 | 33810.0 s | 0.000″; 0.06″ | 0.7–0.8″ | ≤ 44″ | +42.9″ | ≤ 0.18″ |
| −600 Sep 22 16:00–17:00 | 18526.1 s | 0.000″; 0.06″ | 2.6–2.7″ | ≤ 15″ | +11.8″ | ≤ 0.16″ |
| +200 Jan 15 05:00–06:00 | 8456.9 s | 0.000″; 0.006″ | 3.0″ | ≤ 4″ | +0.5″ | ≤ 0.17″ |

Readings, all my inference from these numbers:

* The positions agree. The az/el residual tracks the sidereal-time
  convention as expected: 78″ at −1999, 44″ at −1450, 15″ at −600 and 4″
  at +200. The convention costs 5 s of time at −1999 and is negligible
  next to ΔT (σ = 3,732 s there by Huber's formula [NASA uncertainty
  page]).
* The Moon's astrometric difference grows to 0.52″ at −1999. As at −1177
  [eph §7], this is that orientation difference seen through the lunar
  parallax.
* The apparent-of-date residuals (0.7–3.0″) come from Horizons' models
  (Owen's long-term precession at all four dates, which are before 1799,
  and IAU 1980 nutation) against ours (Vondrak and IAU 2000A), plus
  Horizons' stated equinox offset [eph §7]. They are not monotonic in
  time, which fits a mix of model differences (my inference).

Responses are cached in `data/ephem/horizons/`, with the request URL on
line 1: `spot_*.txt` (16 files) and `calendar_probe_*.txt` (6 files).

## 2. NASA Five Millennium Canon elements (JSEX)

### 2.1 Fetched

`py tools/fetch_jsex.py` fetched from `https://eclipse.gsfc.nasa.gov/JSEX/`:
* `program.js` (C. O'Byrne & F. Espenak, GPL);
* 23 century files `SEm1999.js` … `SEm0099.js`, `SE0001.js`, `SE0101.js`,
  `SE0201.js`. These are the Besselian elements of Espenak & Meeus 2006,
  NASA/TP-2006-214141.

All of them, −1999..+300, are in `data/jsex/`: 2.0 MB, 5,486 eclipses,
from −1999 Jun 12 to +300 Oct 29. Five catalogue pages
`SEcat5/SE-1999--1900.html` … `SE-1599--1500.html` are in
`data/jsex/secat5/` (532 kB). SHA-256 of every file is in
`data/SHA256SUMS`. The century files run 79,909–90,529 bytes, so DESIGN's
"about 85 kB per century" holds.

The task asked for −1999..−1500. I fetched all centuries to +300, because
the earlier copies stop at −600: `results/window/jsex/` holds
SEm1499–SEm0699 and `data/refs/nasa/` adds SEm0599 and SEm0499. One
directory holding the whole span is simpler for `eclipses.py`.

### 2.2 Checks [me: results/data-acquisition/check_jsex.py → check_jsex.out.txt, ALL PASS]

* **Byte identity with the earlier downloads.** All 18 comparisons are
  identical. They cover the century files present in
  `results/window/jsex/` or `data/refs/nasa/JSEX-*`, and `program.js`.
* **Against NASA's catalogue pages.** For each of the 5 new pages and the
  3 already on disk (SEcat5_SE-1299..-1000), every catalogue eclipse has
  exactly one element row.
  * Counts agree: 239, 253, 254, 230, 225 for −1999..−1500.
  * TD of greatest eclipse agrees to ≤ 0.5 s, and ΔT to ≤ 0.5 s; the page
    prints whole seconds.
  * Gamma, computed from the x and y polynomials at T0, agrees to
    ≤ 0.00005; the page prints 4 decimals.
* **ΔT in the elements is the Canon's rule.** The rule is
  `ephem.dt_em2006_canon`: Espenak–Meeus plus n-dot correction [eph §2].
  * Evaluated at a day-resolved decimal year, y + (day of year − 1 +
    h/24)/days in year, it matches all 5,486 rows to ≤ 0.15 s. The
    elements print 0.1 s.
  * At NASA's mid-month convention y + (m − 0.5)/12 the worst row is
    1.06 s off. Those rows fall on the first days of a month.
  * So the Canon evaluated ΔT at the actual date, not mid-month (my
    inference). It does not affect −1177 Apr 16, which reproduces 28590.0
    either way [eph §2.1, 1d].
* **Site catalogue.** `tools/jsex_sites.js` is
  `results/window/jsex/local.js` with two changes:
  * the element directory becomes an argument;
  * σ(ΔT) for years ≥ −500 is Morrison & Stephenson's 0.8u² s from NASA's
    uncertainty page [data/refs/nasa/SEcat5_uncertainty.html]. local.js
    returned 0 there, which made the ±σ envelope collapse after −500. A
    `sigmaSrc` field records which formula was used.

  The rows are in `data/jsex/sites/{ithaca,kefalonia,lefkada,corfu,
  zakynthos}.jsonl`, 5,486 eclipses each, in the same format plus
  `sigmaSrc`. **The 2,138 rows per site for −1499..−600 are identical,
  field for field, to the window catalogue** [results/window/jsex/*.jsonl].
  * The site coordinates were identified by reproducing those files
    exactly [me: jsex_sites_check.py]: Ithaca 38.37 N 20.72 E, Kefalonia
    38.18 20.49, Lefkada 38.83 **20.70**, Corfu 39.62 19.92, Zakynthos
    37.78 20.90.
  * Note: research-ephemeris uses 20.71 E for Lefkada [eph Conventions].
    The two earlier tasks disagree by 0.01°.
* **Spot check.** At Ithaca, −1177 Apr 16 is partial: magnitude 0.984,
  maximum 10:22 UT, LAT 11:44, Sun at 57.2°. Research-window reports the
  same [docs/research-window.md §7].

Counts at Ithaca by span, for information (not a bench result) [me]:

| span | eclipses | total at nominal ΔT, Sun up | total for some ΔT within ±1σ |
|---|---|---|---|
| −1999..−1500 | 1,201 | 0 | 7 (all partial at nominal ΔT; σ 2,000–3,700 s) |
| −1499..−600 | 2,138 | 6 | 10 (as in research-window) |
| −599..+300 | 2,147 | 3 | 4: −401 Jan 18, −309 Aug 15, −128 Nov 20, +174 Feb 19 |

**Caveat.** Huber's σ (before −500) and MS2004's σ (from −500) are
different models; I take both from NASA's uncertainty page. At −501 Huber
gives about 0 s and MS2004 at −500 gives 431 s, so the envelope is
discontinuous at −500. This matters only for σ-envelope classes near
−500. DESIGN's own ΔT for the bench (SMH2020 with the HMNAO ε) is
continuous [eph §2.2].

## 3. Stars

### 3.1 Method

`py tools/fetch_stars.py` builds `data/stars.json`. The raw responses are
cached in `data/refs/stars/`, 109 files with the request URL on line 1,
1.5 MB in all, including the Bond et al. 2017 PDF and the I/239 ReadMe.

For each star:

1. **SIMBAD TAP.** Its identifiers are read for the Bayer designation
   (e.g. `* alf CMa`), and **the HIP number is taken from that list**.
   Also read: ICRS J2000 position, proper motion and parallax with their
   bibcodes, V magnitude, and RV with error, quality and bibcode.
2. **VizieR I/311/hip2** (van Leeuwen 2007): the row of that HIP number.
   Also **I/239/hip_main** (ESA 1997), for the solution flags `AstroRef`
   and `MultFlag`.
3. **Verification.** The hip2 position is propagated to J2000 with ERFA
   `eraPmsafe` and must lie within 1″ of SIMBAD's; all agree to
   ≤ 0.038″. |Hp − V| must be under 0.6 mag; all are ≤ 0.37. Any HIP
   number stated earlier must equal the catalogue's.

`adopted` is: hip2 astrometry (ICRS, epoch J1991.25 = JD 2448349.0625 TT),
and SIMBAD's RV except for Sirius. For the four stars already in
`ephem.HIP_STARS` it reproduces their literal values exactly, astrometry
and RV [me: fetch_stars.out.txt; validate_coverage §9].

### 3.2 Results

| key | SIMBAD | HIP: stated before → catalogue | RA, Dec J1991.25 (deg) | plx (mas) | pmRA*, pmDE (mas/yr) | RV (km/s), bibcode | hip1 AstroRef/MultFlag; hip2 Sn | Hp−V |
|---|---|---|---|---|---|---|---|---|
| alcyone | * eta Tau | 17702 → 17702 confirmed | 56.87110081, +24.10524179 | 8.09 | 19.34, −43.67 | 5.4 (q B), 2006AstL...32..759G | –/–; 5 | −0.02 |
| arcturus | * alf Boo | 69673 → 69673 confirmed | 213.91811408, +19.18727046 | 88.83 | −1093.39, −2000.06 | −5.229 (A), 2018A&A...616A...7S | */C; 55 | +0.16 |
| eps_boo | * eps Boo | 72105 → 72105 confirmed | 221.24687848, +27.07417376 | 16.10 | −50.95, 21.07 | −16.6 (A), 1979IAUS...30...57E | A/C; 15 | +0.07 |
| eta_boo | * eta Boo | 67927 → 67927 confirmed | 208.67131829, +18.39858670 | 87.75 | −60.95, −356.29 | 5.77111 (A), 2020AJ....160..120J | +/O; 75 | +0.12 |
| **sirius** | * alf CMa | 32349 → 32349 confirmed | 101.28854105, −16.71314306 | 379.21 | −546.01, −1223.07 | **−8.47**, Bond et al. 2017 (system; see 3.3) | **+/O**; 0 | +0.37 |
| aldebaran | * alf Tau | 21421 → 21421 confirmed | 68.98000194, +16.50976158 | 48.94 | 63.45, −188.94 | 54.398 (A), 2018A&A...616A...7S | –/–; 1 | +0.14 |
| betelgeuse | * alf Ori | 27989 → 27989 confirmed | 88.79287149, +7.40703653 | 6.55 | 27.54, 11.30 | 21.91 (A), 2005A&A...430..165F | –/X; 1 | +0.08 |
| rigel | * bet Ori | 24436 → 24436 confirmed | 78.63446385, −8.20163958 | 3.78 | 1.31, 0.50 | 17.8 (A), 2006AstL...32..759G | –/–; 5 | +0.06 |
| dubhe | * alf UMa | 54061 → 54061 confirmed | 165.93265337, +61.75111903 | 26.54 | −134.11, −34.70 | −9.4 (A), 2006AstL...32..759G | A/C; 17 | +0.16 |
| gam_tau (Hyades) | * gam Tau | 20205 | 64.94805797, +15.62770010 | 20.19 | 115.46, −23.42 | 38.458 (A) | –/–; 5 | +0.16 |
| del01_tau (Hyades) | * del01 Tau | 20455 | 65.73344726, +17.54258445 | 20.96 | 106.56, −29.18 | 37.5875 (A) | –/–; 1 | +0.17 |
| eps_tau (Hyades) | * eps Tau | 20889 | 67.15388847, +19.18052103 | 22.24 | 106.19, −37.84 | 38.42 (A) | –/–; 5 | +0.17 |
| tet02_tau (Hyades) | * tet02 Tau | 20894 | 67.16531227, +15.87094681 | 21.69 | 108.42, −26.74 | 38.9 (A) | –/–; 1 | +0.05 |
| bellatrix | * gam Ori | 25336 | 81.28278339, +6.34973457 | 12.92 | −8.11, −12.88 | 17.31 (A) | –/–; 7 | −0.09 |
| mintaka | * del Ori | 25930 | 83.00166550, −0.29909343 | 4.71 | 0.64, −0.69 | 18.5 (A) | */C; 55 | −0.27 |
| alnilam | * eps Ori | 26311 | 84.05338544, −1.20191724 | 1.65 | 1.44, −0.78 | 27.3 (A) | –/–; 5 | −0.07 |
| alnitak | * zet Ori | 26727 | 85.18968667, −1.94257852 | 4.43 | 3.19, 2.03 | 18.5 (B) | A/C; 15 | −0.09 |
| saiph | * kap Ori | 27366 | 86.93911657, −9.66960181 | 5.04 | 1.46, −1.28 | 20.5 (B) | –/–; 5 | −0.05 |
| gam_boo | * gam Boo | 71075 | 218.01982423, +38.30788378 | 37.58 | −115.71, 151.16 | −32.4 (B) | –/–; 5 | +0.08 |
| bet_boo | * bet Boo | 73555 | 225.48663804, +40.39063698 | 14.48 | −40.15, −28.86 | −18.4 (A) | –/–; 5 | +0.13 |
| del_boo | * del Boo | 74666 | 228.87543250, +33.31510247 | 26.78 | 84.74, −111.58 | −12.29 (A) | –/–; 5 | +0.14 |

Notes:
* **The grammar stars.** The grammar's Hyades star is Aldebaran and its
  Orion stars are Betelgeuse and Rigel [DESIGN §3.1]. Aldebaran is a
  foreground star, not a member of the Hyades cluster (general knowledge,
  not checked here). The four brightest true members are therefore
  included as extras for a "which star stands for the Hyades" fork.
* **The other extras.** Orion's belt, Bellatrix and Saiph are extras for
  the same reason. γ, β and δ Boo are the other Boötes stars that
  `docs/research_visibility_calc.py` used.
* **Flags worth knowing.**
  * Betelgeuse's Hipparcos solution is stochastic (hip2 Sn = 1; hip1
    MultFlag X).
  * Arcturus is flagged as a component solution with the photocentre as
    reference (`*`/C).
  * η Boo, like Sirius, has an orbital solution referred to the centre
    of mass (+/O).
  * None of these matters at the arcminute level that heliacal phases
    need. That is my judgement, not a computation.

### 3.3 Sirius: which proper motion, and how much it matters at −1177

**What the catalogue says.** The Hipparcos 1997 entry for HIP 32349 has
`MultFlag = O`, an orbital solution in the Double and Multiple Systems
Annex, and `AstroRef = '+'`. The I/239 ReadMe defines '+' as "the centre
of mass" for the astrometric parameters in H3–4 and H8–30
[data/refs/stars/I_239_ReadMe.txt; vizier_hip1_32349.txt]. The DMSA/O row
gives:
* P = 18,295.4 d, T = JD 2440000 − 27,123.7, a0 = 2,490.40 mas,
  e = 0.5923, ω = 327.27°, i = 136.53°, Ω = 44.86°;
* status flags `111110000000`, meaning only the five astrometric
  parameters were estimated and **the orbit was held fixed** at its
  literature values [vizier_hip_dm_o_32349.txt; ReadMe "Note on flag"].

hip2 carries the solution over: Sn = 0, So = 4 ("orbital binary as
resolved in the published catalog"), pm −546.01/−1223.07 against hip1's
−546.01/−1223.08.

**Adopted: the Hipparcos centre-of-mass proper motion.** It is an
orbit-corrected barycentric proper motion, corrected by ESA with a fixed
literature orbit. The RV is the system velocity −8.47 km/s: Bond et al.
2017 §5.1 derive −7.70 km/s for the centre of mass from RVs of 1903–1995
and the relative orbit, then remove Sirius A's gravitational redshift.
SIMBAD's −5.5 km/s is for Sirius A.

**Alternatives, propagated to −1177 Apr 16 0h TT with ERFA `eraPmsafe`
from the same J1991.25 position** [me: tools/fetch_stars.py;
`stars.json` → `sirius.proper_motion_comparison_m1177`]:

| proper motion | pmRA*, pmDE (mas/yr) | Δμ from adopted (mas/yr) | **position difference at −1177** |
|---|---|---|---|
| adopted: Hipparcos centre of mass (hip2) | −546.01, −1223.07 | 0 | 0 |
| Hipparcos 1997 (hip1) | −546.01, −1223.08 | 0.01 | 0.001′ |
| **FK5, long-baseline ground-based** [VizieR I/149A; −3.847 s/cy and −120.53″/cy, central epochs 1932.58 and 1912.06; FK5 system, not rotated to ICRS] | −552.66, −1205.30 | 18.98 | **0.99′** |
| Hipparcos re-referred to Bond et al. 2017's orbit: the adopted value minus the least-squares slope of (Bond orbit − DMSA orbit) over the mission 1989.85–1993.21, which is (+0.59, −19.45) mas/yr | −546.60, −1203.62 | 19.46 | **1.02′** |
| Sirius A's instantaneous motion at J1991.25 (adopted + A's orbital velocity, 464.0 mas/yr from Bond et al. 2017 Tables 4–5; the DMSA orbit gives 480.1): what a single-star short-baseline fit would have measured | −230.49, −882.86 | 464.0 | **24.2′** |
| adopted pm with SIMBAD's RV −5.5 km/s | same | 0 | 0.25′ |
| adopted pm with RV −7.70 km/s (no redshift correction) | same | 0 | 0.07′ |

Reading, my inference from these numbers:

* **The critique's concern is real in size but does not apply to the
  catalogue value.** A photocentre motion would put Sirius 24′ (0.40°) off
  at −1177; the critique estimated 0.2–0.3°. The Hipparcos value was never
  a photocentre motion.
* **What remains is the orbit model.** Hipparcos held an older orbit
  fixed. Over the 3-year mission the fit cannot tell barycentric motion
  from orbital motion, so the older orbit's velocity error passes into the
  proper motion. Swapping in Bond et al.'s orbit moves the proper motion
  by 19 mas/yr.
* **FK5 agrees with the re-referred value.** The re-referred value lies
  within **6.3 mas/yr** of FK5's independent long-baseline value; the
  published value is 19 mas/yr from FK5. This is evidence that the
  re-referral is right and that the residual uncertainty at −1177 is
  about 1′.
* **I kept the published value as `adopted`.** It is traceable to a
  catalogue, and 1′ in Sirius' position changes its rising time by a few
  seconds, irrelevant for heliacal phases. The re-referred value is in
  `stars.json` if a sensitivity run wants it.
* **Orbit elements used.** Bond et al. 2017 Table 4, relative orbit:
  P 50.1284 yr, a 7.4957″, i 136.336°, Ω 45.400°, T0 1994.5715,
  e 0.59142, ω 149.161°. Table 5: a_A = 2.4761″. Source: arXiv:1703.10625v1,
  cached as `data/refs/stars/bond2017_arxiv1703.10625v1.pdf`.
* **Cross-check of the orbit code.** Both orbits give the same picture:
  A's velocity at J1991.25 is 464.0 mas/yr from Bond and 480.1 from DMSA
  [me: results/data-acquisition/sirius_orbit_check.py].

### 3.4 In `odybench.ephem`

`star(key)` now also accepts every key in `data/stars.json`, read through
`stars_catalogue()`; `star_keys()` lists them.
* The four `HIP_STARS` keep their literal values and take precedence, so
  no existing result changed (68/68, §1.3).
* For example, `E.altaz("sirius", jd, 38.37, 20.72)` now works.

## 4. Calendar module

`odybench/calendar.py` has no `datetime` and no numpy date-time type.
Integer floor division makes it exact for Python ints and for numpy int
arrays alike.

* Proleptic Julian:
  * `jdn_from_julian`, `julian_from_jdn`, `jd_from_julian(y, m, d[, hour])`
    (fractional days allowed);
  * `julian_from_jd(jd, offset_hours)`, which resolves instants to 1 ms
    before picking the day, so float noise cannot move an instant across
    midnight.
* Gregorian, for cross-checks only: `jdn_from_gregorian`,
  `gregorian_from_jdn`, `jd_from_gregorian`, `gregorian_from_jd`.
* Leap rule: `is_leap_julian`, which treats y mod 4 == 0 as leap, so 1 BC
  (0) and 1177 BC (−1176) are leap years and 1178 BC is not.
  `days_in_year` and `days_in_month` follow from it.
* Days: `day_of_year`, `from_day_of_year`, `weekday`.
* Civil dates of an instant: `civil_date(jd_ut, offset)`, `ut2_date`,
  `lmt_date(jd_ut, lon)` (offset lon/15) and `lat_date(jd_ut, lon, eot)`
  (LMT plus an equation of time supplied by the caller, since `ephem`
  owns the Sun).
* Windows: `day_bounds` and `span_bounds` give half-open [start, end) JD
  intervals of civil days in a zone. "Through 31 Dec −1114 at UT+2" ends
  at 22:00 UT on 31 Dec [crit issue 22, fix 1].
* Time scales and epochs:
  * `tt_from_ut` and `ut_from_tt`, with ΔT = TT − UT1 in seconds;
  * `julian_epoch(jd_tt) = 2000 + (JD_TT − 2451545)/365.25`. This is
    identical to `ephem.julian_epoch`, the argument of every ΔT model
    [crit issue 22].
  * `decimal_year_nasa = y + (m − 0.5)/12` and `calendar_year_fraction`.
* Labels: `historical_year`, `astronomical_year`, `fmt`.

`tests/test_calendar.py` (run `py tests/test_calendar.py`): **11/11 pass**,
in about 2 s.

| test | reference |
|---|---|
| every day of −1999..+500 (913,125 days = 2,500 × 365 + 625 leap days): JDN, inverse and day of year, vector path | independent day counting from the definition JDN(−4712 Jan 1) = 0 |
| scalar and vector paths agree (2,000 days) | each other |
| every 7th day | `ephem.jd_from_julian` / `julian_from_jd` (Meeus floating-point formulas [eph §9]) |
| leap rule for every year; Feb 29 exists only in leap years; 1461 days per 4 years | definition |
| −1177-04-16 0h = JD 1291263.5, JDN 1291264; 1178 BC labels; the same day is Gregorian −1177 Apr **5**, the 11-day shift DESIGN §0 warns about | Horizons "B.C. 1178-Apr-16 00:00" [eph; test_ephem] |
| Meeus examples 7.a–7.f: 1957 Oct 4.81 = 2436116.31; 333 Jan 27.5 = 1842713.0; the inverse; Halley 27,689 days; 1954 Jun 30 a Wednesday; day of year 318 and 113. Also the 16-entry ch. 7 JD table, e.g. −1000 Feb 29.0 = 1355866.5, −4712 Jan 1.5 = 0.0, and the 1582 reform | Meeus 1998, *Astronomical Algorithms* 2nd ed. ch. 7, **as I recall it** (the book is not on this machine). Every value also agrees with the exhaustive day count, so a mis-remembered value would have failed |
| 200,000 random instants: round trip to < 1 ms, hours in [0, 24), scalar = vector | itself |
| zones: civil date = UT date of the shifted instant; the instant lies in its civil day's bounds; 22:00 UT = 00:00 UT+2 of the next day exactly; LMT at 20.72 E; LAT = LMT + EoT; window end | definitions |
| TT↔UT round trip; Julian epoch = ephem's; it runs 0.02–0.05 yr (~13 d) ahead of y + (m − 0.5)/12 at −1177 [eph §2.2] | ephem |
| Horizons calendar output, 306 instants | `data/ephem/horizons/calendar_probe_*.txt` |
| no `import datetime`, no numpy date-time, no `astype('M8…')` in odybench/, tools/, tests/ or top-level scripts | critique issue 13, fix 5 |

**Instrument check** [me: results/data-acquisition/mutation_check_calendar.py].
Five deliberate bugs were each caught by 1–9 tests:
* a one-day shift in −500 March;
* the leap rule y mod 4 == 1;
* an off-by-one inverse for BC days;
* truncating instead of rounding instants;
* Gregorian in place of Julian.

The unmutated module passes everything.

`ephem.py` keeps its own `jd_from_julian` and the related functions, and
their results are unchanged. The tests show that the two modules agree
exactly for whole days. New bench code should use `odybench.calendar`.

**Module-name caveat.** Inside the package the module is
`odybench.calendar`, which shadows nothing. Do not run a file inside
`odybench/` as a script (`py odybench/x.py`), because then `calendar`
would shadow the standard library's; use `py -m odybench.x`.

## 5. Checksums

`data/SHA256SUMS` (180 lines; check with `sha256sum -c data/SHA256SUMS`
from the project root) lists:
* every `.bsp` in `data/ephem/` and `data/ephem/de431/`;
* `data/jsex/*.js`, `data/jsex/secat5/*.html` and
  `data/jsex/sites/*.jsonl`;
* `data/stars.json` and every file in `data/refs/stars/`;
* the new Horizons caches.

The key files:

| file | bytes | SHA-256 |
|---|---|---|
| data/ephem/de441_m2060_p0241.bsp | 237,911,792 | 7c0028c6d24a85245e4f91167fabd1ad8d294d50343f7fd02f5e7dcc88a4861b |
| data/ephem/de431/de431_m2060_p0001.bsp | 152,067,856 | ee7d778ba9c5568251e4ef2f608caad8b170919b3c2bf009d3bd1f4414a714a4 |
| data/ephem/de431/de431_p0001_p0241.bsp | 17,711,696 | ccef82788fda2ddba14ee17269552a462a88d517e1dd2b2a65b442d6d77410ba |
| data/ephem/de431/de431_m1339_eclipse.bsp | 30,032 | b74334404f2e812e90d0a339ad5aa90037139a43c15151d2cb9ef7a14d6161a6 |
| data/ephem/de431/de431_m0647_eclipse.bsp | 30,032 | d7bca73744765c63d4de38b761fb05a37abd44634e7f690f2670ae205f38885f |
| data/jsex/program.js | 36,759 | 9676f7922ced83c47fc088af5b8f53f7f51cc13563e527ee53910c54ed61c881 |
| data/jsex/SEm1999.js | 84,865 | d33e214a65eecebc936275edd5f67e2d08c4ddb7ff310a6b854ea3e49dba3483 |
| data/jsex/sites/ithaca.jsonl | (5,486 rows) | 16781ad62e971b6d63bfa5073f4a25448bc1633329f6a0acb7610e24d6110d71 |
| data/stars.json | | d9d5062eea270cf4d14f40002dec05399fdc4608754091597ee3cd01c0e6da8a |

## 6. Caveats and things the next stage must know

1. **DE431 split at JD 1721425.5** (AD 1 Jan 3, Julian). No DE431 request
   may span it, so split by year. DE441 has no split anywhere in
   −2060..+241.
2. **DE431 long excerpts hold the Sun, Earth and Moon only.** A DE431
   request for planets is only possible inside −1320..−1030.
3. **ΔT σ before −2000.** `ephem.sigma_smh2020` before −2000 is Liu's
   extrapolation, not a published number [ephem.py docstring]. That covers
   the excerpt's first 60 years, −2060..−2001. NASA's elements start at
   −1999.
4. **The site catalogue's σ switches models at −500**, from Huber to
   MS2004, both from NASA's page (§2.2).
5. **Lefkada is 20.70 E in the window and site catalogues and 20.71 E in
   research-ephemeris.** One of them should be chosen when `eclipses.py`
   is written.
6. **Sirius.** The adopted value is the published Hipparcos centre-of-mass
   proper motion. The residual orbit-model uncertainty is about 1′ at
   −1177 (§3.3). The bench must never substitute a photocentre or
   short-baseline Sirius motion: that would be 24′ off.
7. **Meeus values were recalled, not read.** The ch. 7 examples in
   `test_calendar.py` were recalled from memory. All agree with exhaustive
   day counting and with Horizons, so none can be wrong without the test
   failing.
8. **Before/after runs.** `results/validate_ephem.txt` (from 2026-10-03)
   was not overwritten. The reruns are in `results/data-acquisition/`.
9. **Not done here.** Rise and set times, stations and heliacal phases
   are still unvalidated against an independent source [crit issue 13,
   fixes 1–4]. That belongs to `sky.py` and `events.py`.

## 7. Files

Written by this task:
* `tools/fetch_ephem.py`, extended: new jobs, chunked Range reads with
  retries, no overwrite without `--force`, SHA-256 printout;
* `tools/fetch_jsex.py`, `tools/jsex_sites.js`, `tools/fetch_stars.py`,
  `tools/validate_coverage.py`;
* `odybench/calendar.py`; `odybench/ephem.py` (only `kernel()`,
  `coverage()`, the star loader and the docstring);
* `tests/test_calendar.py`;
* `data/stars.json`, `data/SHA256SUMS`;
* the data in §§1–3;
* `docs/data-acquisition.md`.

Scratch scripts and outputs are in `results/data-acquisition/`:
`probe_spk.py`, `fetch_ephem.out.txt`, `fetch_jsex.out.txt`,
`fetch_stars.out.txt`, `check_jsex.py`/`.out.txt`,
`jsex_sites_check.py`/`.txt`, `sirius_orbit_check.py`/`.out.txt`,
`mutation_check_calendar.py`/`.out.txt`, `validate_ephem.{before,after}.txt`,
`validate_ephem.diff.txt`, `test_ephem.{before,after}.txt`,
`validate_coverage.out.txt`, `test_calendar.out.txt`, `ephem_orig.py`,
and `bond2017.txt` (the PDF's extracted text).

## Sources

* NAIF generic kernels, `de441_part-1.bsp`, `de431_part-1.bsp`,
  `de431_part-2.bsp`:
  https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/
  (Last-Modified 2020-12-22 for de441_part-1). Park et al. 2021, AJ 161:105
  [eph].
* Espenak, F. & Meeus, J. 2006, *Five Millennium Canon of Solar Eclipses:
  −1999 to +3000*, NASA/TP-2006-214141. Elements and `program.js` from
  https://eclipse.gsfc.nasa.gov/JSEX/; catalogue from
  https://eclipse.gsfc.nasa.gov/SEcat5/; "Eclipse Predictions by Fred
  Espenak, NASA's GSFC". The uncertainty page is
  https://eclipse.gsfc.nasa.gov/SEcat5/uncertainty.html.
* van Leeuwen, F. 2007, A&A 474, 653 (VizieR I/311/hip2). ESA 1997,
  *The Hipparcos and Tycho Catalogues*, SP-1200 (VizieR I/239: hip_main,
  hip_dm_o, ReadMe). Fricke, W. et al. 1988, FK5 (VizieR I/149A).
  SIMBAD TAP, https://simbad.cds.unistra.fr/simbad/sim-tap.
* Bond, H. E. et al. 2017, *The Sirius System and its Astrophysical
  Puzzles*, ApJ 840:70, arXiv:1703.10625: Tables 4–5 and §5.1.
* JPL Horizons API, https://ssd.jpl.nasa.gov/api/horizons.api.
* Meeus, J. 1998, *Astronomical Algorithms*, 2nd ed., ch. 7 (as recalled;
  see §4).
