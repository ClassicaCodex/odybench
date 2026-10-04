## 11. Data, run order and run times

### 11.1 Data still to acquire

| what | from | size | why |
|---|---|---|---|
| DE441 excerpt +241..+300, the same 11 bodies | NAIF `de441_part-1.bsp` by HTTP Range (`tools/fetch_ephem.py`) | about 6 MB [me: 238 MB per 2,301 years, scaled] | some control windows reach past +241 (4.1; [AppT 7]); the current excerpt ends at +241 [acq §1.1] |
| DE431 Sun, EMB, Earth, Moon +241..+300 | NAIF `de431_part-2.bsp` | about 4 MB [me: 17.7 MB per 240 years, scaled] | lunar-timed quantities for the same windows |
| NASA LEcat5 century pages −1999..+300 | eclipse.gsfc.nasa.gov/LEcat5 (`tools/fetch_lecat.py`) | about 23 × 60 kB; all 23 are fetched anew, because the 10 earlier copies sit in `results/controls/`, which is off the public whitelist (10.1) | I4; I16's type and magnitude cross-reference |
| **Horizons observer tables** for 1,000 rise and set events: QUANTITIES 4 and 30, airless, fractional seconds, 21 epochs per event | Horizons API (`tools/fetch_horizons_obs.py`), in TLIST batches by body and site; cached in `data/ephem/horizons/` with the request URL on line 1 | about 21,000 epochs; tens of requests | I5(a) [r1v5 N4] |
| **Horizons geocentric tables** (QUANTITIES 31 and 23, TT): 200 random events for I6(b), every P_BM member for I15(b), and 200 PC-S truths for I10 | the same tool | a few hundred requests | I6(b), I15(b), I10 [r1v5 N4] |
| solar local circumstances at the control sites, from NASA's `program.js` | `tools/jsex_sites.js`, run in Node by A7 for each control site of `controls_real.json` | small | I16 |
| the *Almagest* reference stars (δ Cap, β and ζ Tau, Castor, Pollux, ζ Gem, Spica, Regulus, Antares, α Lib, β and δ Sco, β, γ and η Vir, δ Cnc, λ, φ and ψ1–3 Aqr, the Pleiades) | `tools/fetch_stars.py` (SIMBAD identifiers and hip2 rows, as in [acq §3]). The drafter fetched them for its own run into `results/controls-almagest/stars.json`, in memory only [alm §1.5] | small | the full primary run of 6.4 and its held-out calibration, Q_H (the gate's projection does not use them) |
| SMH2016's full text with Table S4, and the 2020 Addendum's tables | the Royal Society and PMC pages (open access) | small | `deltat_circular_truth.json` (6.3.3), read by A11 |

Fetch with Python urllib or the PowerShell tool. Git Bash's curl carries a
2020 CA bundle, so an HTTPS failure there is local. There is no library
access beyond `py -m odybench.ccx`. Every new file's SHA-256 goes into
`data/SHA256SUMS`. The background of 4.1 needs no new data.

### 11.2 Run order and expected times

Measured on this machine (16 logical cores) [v1 §7.5; acq §1.3]:

- `ephem.altaz` runs at about 28,000–29,000 body-positions a second per
  core;
- `ephem.new_moons` takes 23.0 s per 136 years;
- `validate_ephem.py` takes 118–188 s.

The other figures are estimates from these. The run has three stages,
separated by the two freezes of 12.3:

- **pre-freeze:** code, data and the checks that need no null result;
- **null side:** the target masked;
- **target and controls.**

| # | stage | step | command | estimate | basis |
|---|---|---|---|---|---|
| 0 | pre-freeze | fetch | `py tools/fetch_ephem.py`, `py tools/fetch_lecat.py`, `py tools/fetch_horizons_obs.py` | 30–60 min | network; a few hundred Horizons requests |
| 1a | pre-freeze | **the access record first** [r1v5 N9]: `access.json`; the public copy and the export; the served-copy log | A0, A6 (10.1) | minutes | before any public-tier agent starts |
| 1 | pre-freeze | build code; unit tests | agents (10.1) | — | |
| 2 | pre-freeze | sky tables, events, catalogues | `py tools/build_sky.py --all`; `py tools/build_events.py`; `py tools/build_eclipses.py` | **3–5 h, once** [r1 N12] | see below |
| 3 | pre-freeze | instrument checks I1–I6, I8, I9(a), I13, I14(a, b), and the reported I3 and I12. I4 begins with its convention check on three pages | `py tools/validate_ephem.py`; `py tools/validate_events.py`; `py tools/validate_eclipses.py`; `py tests/test_*.py` | 30–60 min | |
| 4 | pre-freeze | the re-draft brief, then the re-draft (6.3.4), then I2b by `py tools/run_i2b.py` into `results/instrument/`; the negatives' second reading (6.5); the review of `operational_map.json`; `deltat_circular_truth.json` (6.3.3); `almagest_regimes.json` (6.4); `pcr_projection.json` (6.3); the disclosure scan and `heldout_disclosure.json` (7.1); `slots.json` (4.2); `sibling_pairs.json` (6.3.4); the builders retired (12.1); I13(h) and the access check on the served copy (10.1) | agents | — | |
| 5 | | **first freeze**, `prereg-1` | `py tools/freeze.py --stage 1` | seconds | 12.3 |
| 6 | null side | I7(a), I9(b, c), I11, I15(a, b) and I16(a) on the masked pool and on random background windows; then the null-side quantities: n_T, n_TC, n_A(v), G_BM(v), G_BM,u, G_DOC (reported); the four held-out pools with each pool's n, x_max and pass counts, q3, q4, p_H,min, Q_record, and the homogeneity, stationarity and "H3 given D4" tables; G_j for the 12 clean negatives; then I14(c) | `py attain.py` | 2–4 h | the 36 readings of 𝒢_BM* and 𝒢_DOC* over about 27,000 candidates; H3 and H4 on about 80 pool members; 2,000 bootstrap cores for I9(b); the negatives' gardens (up to a few thousand readings each after F5 expansion) as packed bit ANDs; I16(a) at 21 windows per counted set |
| 7 | | **second freeze**, `prereg-2`: commits `results/attain/` | `py tools/freeze.py --stage 2` | seconds | 12.3 |
| 8 | target and controls | I7(b), I15 on the target, I10, I10b | `py tests/bm_reference.py --target`; `py heldout.py --check`; `py synthetic.py --instrument` | 20 min | |
| 9 | target and controls | T0 | `py reproduce.py` | 5 min | |
| 10 | target and controls | N1, N2, N5 | `py rates.py`; `py coincidence.py`; `py windows.py` | 10–20 min | lookups on cached tables |
| 11 | target and controls | N6 | `py deltat.py` | 20–40 min | about 45 totality windows on DE431 |
| 12 | target and controls | N3 (r_Ody, the reported gardens, R_anc) and the evidential findings | `py garden.py` | 1–3 h | 𝒢_FULL* (767,232 readings) and the reported E-on gardens (up to 3.07 million) × about 27,000 candidates, as packed bit ANDs on 14 workers with the gap test of 10.2 |
| 13 | target and controls | held-out (p_H, Q_contra) | `py heldout.py` | 5 min | |
| 14 | target and controls | N4 | `py randomepic.py` | 1–3 h | epics drawn until 200 enter the stratum, per variant; the entering fraction may be 0.1 or less [r2 R2-8], so up to about 20,000 stratum epics with 36-reading gardens |
| 15 | target and controls | PC-S science mode | `py synthetic.py` | 20–40 min | the core's 892 truths of T_C × 12 noise cells × the BM and DOC tolerance forks |
| 16 | target and controls | PC-R and the *Almagest* control, with its held-out calibration; **I16(b) first**, on the gates' own windows, before any gate count is read | `py controls.py`; `py almagest.py` | 1–2 h | 21 windows per set; two projections and two scorings for PC-R, two scorings for 3b; the site-"none" shortcut (6.3.1); the mixture grid; I16(b) repeats the evaluation once |
| 17 | target and controls | negatives (hit_j) | `py negatives.py` | 20–40 min | 13 sets × gardens × 2 windows (plus 40 sensitivity windows); G_j is read from `attain.json` |
| 18 | | verdict | `py verdict.py` | seconds | |

**Step 2 in detail** [r1 N12].

- **Evaluations.** A full-column site needs about 310 evaluations a day:
  - 7 bodies × 2 events × about 4 iterations;
  - 6 twilights;
  - **21 stars × 2 events × about 4**;
  - star altitudes, and the Moon.
- **Ithaki.** Over 840,000 days that is about 260 million evaluations: 2.5 h
  on one core, about 12 min on 14.
- **Other sites.** About 10 negative-control sites, at a third of the
  columns over the background, take about 40 min on 14 cores. The control
  sites need their windows only.
- **Eclipses.** 5,486 eclipses × about 55 sites (36 of them rotated), with
  totality bisections, under the mixture grid.
- **Disk.** About 0.9 GB for Ithaki and 4–5 GB in all, in `data/cache/`.

After the first freeze, about 8–14 hours of computation remain. Most of it is
in steps 6, 12, 14 and 16. Step 2 is cached and runs once.

