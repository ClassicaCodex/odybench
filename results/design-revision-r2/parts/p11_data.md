## 11. Data, run order and run times

### 11.1 Data still to acquire

| what | from | size | why |
|---|---|---|---|
| DE441 excerpt +241..+300, the same 11 bodies | NAIF `de441_part-1.bsp` by HTTP Range (`tools/fetch_ephem.py`) | about 6 MB [me: 238 MB per 2,301 years, scaled] | *Almagest* and PC-R windows reach +277 (4.1); the current excerpt ends at +241 [acq §1.1] |
| DE431 Sun, EMB, Earth, Moon +241..+300 | NAIF `de431_part-2.bsp` | about 1 MB | lunar-timed quantities for the same windows |
| NASA LEcat5 century pages −1999..+300 | eclipse.gsfc.nasa.gov/LEcat5 (`tools/fetch_lecat.py`) | about 23 × 60 kB; 10 are already in `results/controls/nasa/` | I4 |
| Horizons rise/transit/set for 1,000 events; positions for 50 PC-S truths | Horizons API (`tools/fetch_horizons_rts.py`), cached in `data/ephem/horizons/` with the request URL on line 1 | small | I5, I10 |
| the *Almagest* reference stars (δ Cap, β and ζ Tau, Castor, Pollux, ζ Gem, Spica, Regulus, Antares, α Lib, β and δ Sco, β, γ and η Vir, δ Cnc, λ, φ and ψ1–3 Aqr, the Pleiades) | `tools/fetch_stars.py` (SIMBAD identifiers and hip2 rows, as in [acq §3]). The drafter fetched them for its own run into `results/controls-almagest/stars.json`, in memory only [alm §1.5] | small | the full primary run of 6.4 (the gate's projection does not use them) |
| SMH2016's full text with Table S4, and the 2020 Addendum's tables | the Royal Society and PMC pages (open access) | small | `deltat_circular.json` (6.3.3), read by A11 |

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

The other figures are estimates from these.

| # | step | command | estimate | basis |
|---|---|---|---|---|
| 0 | fetch | `py tools/fetch_ephem.py`, `py tools/fetch_lecat.py`, `py tools/fetch_horizons_rts.py` | 10–20 min | network |
| 1 | build code; unit tests | agents (10.1) | — | |
| 2 | sky tables, events, catalogues (needed by the pre-freeze checks) | `py tools/build_sky.py --all`; `py tools/build_events.py`; `py tools/build_eclipses.py` | **3–5 h, once** [r1 N12] | about 310 evaluations a day for a full-column site (7 bodies × 2 events × about 4 iterations; 6 twilights; **21 stars × 2 events × about 4**; star altitudes; Moon). Ithaki over 840,000 days is about 260 million evaluations: 2.5 h on one core, about 12 min on 14. About 10 negative-control sites at a third of the columns, over the background, take about 40 min on 14 cores; the control sites take their windows only. Eclipses: 5,486 × about 55 sites (36 rotated) with totality bisections, under the mixture grid. Disk: about 0.9 GB for Ithaki and 4–5 GB in all in `data/cache/` |
| 3 | pre-freeze instrument checks I1–I6, I8, I9(a, b), I12–I14 | `py tools/validate_ephem.py`; `py tools/validate_events.py`; `py tools/validate_eclipses.py`; `py tests/test_*.py` | 30–60 min | |
| 4 | pre-freeze tasks: the re-draft brief, then the re-draft (6.3.4), then I2b; the negatives' second reading (6.5); the review of `operational_map.json`; `deltat_circular.json` (6.3.3); `almagest_regimes.json` (6.4); the builders retired (12.1) | agents | — | |
| 5 | **freeze** | `py tools/freeze.py` | seconds | section 12 |
| 6 | post-freeze instrument checks I7, I9(c), I10, I10b, I11 | `py tests/bm_reference.py`; `py garden.py --identity`; `py synthetic.py --instrument`; `py negatives.py --plumbing` | 20 min | |
| 7 | T0 | `py reproduce.py` | 5 min | |
| 8 | N1, N2, N5 | `py rates.py`; `py coincidence.py`; `py windows.py` | 10–20 min | lookups on cached tables, over a background 1.6 times longer |
| 9 | N6 | `py deltat.py` | 20–40 min | about 45 totality windows on DE431 |
| 10 | N3, R_anc and the evidential findings | `py garden.py` | 1–3 h | 𝒢_FULL* (767,232 readings) and the reported E-on gardens (up to 3.07 million) × about 27,000 candidates, as packed bit ANDs on 14 workers with the gap test of 10.2 |
| 11 | N4 | `py randomepic.py` | 30–60 min | 20,000 epics; stratum epic gardens |
| 12 | PC-S science mode | `py synthetic.py` | 20–40 min | 2,000 truths × 12 noise cells × the BM and DOC tolerance forks |
| 13 | PC-R and the *Almagest* control | `py controls.py`; `py almagest.py` | 30–60 min | 21 windows per set; site "none" grids; the mixture grid |
| 14 | negatives | `py negatives.py` | 20–40 min | 13 sets × gardens × 2 windows (plus 40 sensitivity windows) |
| 15 | held-out | `py heldout.py` | 5 min | |
| 16 | verdict | `py verdict.py` | seconds | |

After the freeze, about 5–9 hours of computation remain, most of it in steps
10–14. Step 2 is cached and runs once.

---

