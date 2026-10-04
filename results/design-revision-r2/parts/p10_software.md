## 10. Software

### 10.1 Build plan

The build is done by agents in parallel. Each agent owns the files listed
for it, works to the interfaces of 10.2, and must not read what is listed in
the last column. The lead writes `odybench/model.py`, the shared types,
first, and it is frozen as the contract. Code inside the package runs as
`py -m odybench.x`, never as `py odybench/x.py`, because the file would
then shadow the standard library's `calendar` [acq §4].

| agent | owns | depends on | must not read |
|---|---|---|---|
| A0 lead | `odybench/model.py`; `data/prereg/sites.json` (with a span and a column set per site), `windows.json`, `seeds.json`, `deltat_models.json`, `verdict_rule.json`, `almagest_regimes.json` | this design | — |
| A1 sky | `odybench/sky.py`, `odybench/events.py`, `tools/build_sky.py`, `tools/build_events.py`, `tools/validate_events.py` (I5, I6, I12), `tools/fetch_horizons_rts.py` | `model.py`, `ephem.py`, `calendar.py` | — |
| A2 eclipses | `odybench/eclipses.py`, `odybench/lunar.py`, `odybench/deltat_mix.py`, `data/prereg/eclipse_hit.json`, `tools/build_eclipses.py`, `tools/validate_eclipses.py` (I2, I4), `tools/fetch_lecat.py`, `tests/test_eclipses.py`, `tests/test_lunar.py` | `model.py`, `ephem.py`, `data/jsex/` | the truth files (I2b runs through the harness) |
| A3 clues | `odybench/prereg_io.py`, `odybench/clues.py`, `odybench/search.py`, the controls sections of `data/prereg/operational_map.json`, a draft of its negatives section, `tools/make_redraft_brief.py`, `tests/test_clues.py`, `tests/test_prereg_io.py` | A1 and A2 interfaces | `*_truth*`, `results/controls-*`, `check_truth*` |
| A4 garden | `odybench/readings.py`, `odybench/pools.py`, `odybench/reach.py` (I9), `odybench/evidence.py`, `data/prereg/garden.json`, `readings.json`, `rates.py`, `coincidence.py`, `garden.py`, `windows.py` | A3 | `*_truth*` |
| A5 epics and PC-S | `odybench/epic.py`, `odybench/pcs.py`, `data/prereg/epic_grammar.json`, `randomepic.py`, `synthetic.py` (I10, I10b) | A3, A4 | `*_truth*` |
| A6 harness and verdict | `odybench/harness.py`, `tools/build_truth_index.py`, `controls.py`, `almagest.py`, `negatives.py`, `heldout.py`, `data/prereg/heldout.json`, `odybench/verdict_rule.py`, `verdict.py`, `read.py`, `odybench/stats.py`, `odybench/prereg.py`, `tools/freeze.py`, `tests/test_verdict.py` (I14), `data/prereg/verdict_synthetic/` | all | — |
| A7 second implementation | `tests/bm_reference.py` (I7) | `ephem.py`, `calendar.py`, section 3.2 of this design | every other bench module |
| A8 unexposed re-drafter | `data/prereg/pcr_redraft.json` | `data/prereg/pcr_redraft_brief.json` only | everything else in the repository (6.3.4) |
| A9 second reader of the negatives | the review of the negatives section of `operational_map.json`; the interval forks and caps; the literal pins and the X-class decision (6.5); the replay script of its edits | `negatives.json`, `data/text/` | — |
| A10 reproduction and ΔT | `reproduce.py`, `deltat.py`, `odybench/s2.py`, `tests/test_t0.py` | A1, A2 | — |
| A11 ΔT-fit reader | `data/prereg/deltat_circular.json` (6.3.3), with page locators into SMH2016 and the 2020 Addendum | the two papers and their supplementary tables | the truth files |

### 10.2 Module interfaces

All times are JD floats with a named scale, and all calendar work goes
through `odybench.calendar`. Arrays are numpy. Files are NPZ (numeric) or
JSON (UTF-8, `ensure_ascii=False`).

**`odybench/model.py`** (the contract)

```
BODIES = ("sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn")
GRAMMAR_STARS = ("alcyone", "arcturus", "sirius", "aldebaran", "betelgeuse",
                 "rigel", "dubhe")           # extras from data/stars.json allowed
DT_MODELS = ("smh2020", "smh2020_parabola", "smh2016_parabola", "em_canon")
@dataclass Site(key, lat, lon, elev_m, source, span: tuple[int, int],
                columns: tuple[str, ...])                    # span: Julian years, inclusive
POOL_DTYPE = [("jd_ut","f8"), ("jd_tt","f8"),
              ("day0_jdn_ut2","i8"), ("day0_jdn_lmt","i8"),  # one Day-0 date per clock
              ("kind","U12"), ("cat_idx","i8"), ("daylight","?")]
@dataclass Predicate(type: str, params: dict, day: int | tuple[int,int] | None,
                     quant: str = "any", site: dict | None = None,
                     dt_rule: str = "mixture_p50")            # how a ΔT-dependent row passes
@dataclass Option(name: str, primary: bool, predicate: Predicate | None,
                  grid: dict[str, list])                      # None = the clue is dropped
@dataclass ClueRow(clue_id, event_id, day_offset, options: list[Option])
@dataclass ClueSet(set_id, role, anchor_kind, events, links, rows, site_rule,
                   window_widths, counted: bool)
@dataclass Reading(choice: dict[str, tuple[str, dict]])     # clue_id -> (option, grid values)
@dataclass SearchResult(pool, fails: np.ndarray[int16], strict: np.ndarray[int64],
                        best: np.ndarray[int64], n_cand: int, clusters: int)
@dataclass GStat(value: float, lo: float, hi: float, n: int, k: int,
                 garden: str, pool: str, widths: tuple[int, ...])
```

**`odybench/sky.py`** [r1 N12]

```
build(site: str, y0: int, y1: int, *, dt_model: str | float = "smh2020",
      refraction: bool = False, bodies=BODIES, stars=GRAMMAR_STARS,
      columns: tuple[str, ...] | None = None, workers=14,
      out_dir="data/cache") -> Path
load(path) -> SkyTable        # NPZ, n = number of LMT civil days y0-01-01 .. y1-12-31
```

- **The ΔT argument.** A float `dt_model` is a constant ΔT in seconds. That
  is T0b's clock (27,602.7 s).
- **Refraction.** `refraction=True` adds standard refraction for T0b's M
  sensitivity. The default is airless, as in the S2 reproduction.
- **SkyTable arrays** (nb bodies, ns stars, n days):

  | arrays | type | content |
  |---|---|---|
  | `jdn` | i8[n] | civil day |
  | `jd0_ut` | f8[n] | local midnight |
  | `rise_ut`, `set_ut` | f8[nb, n] | NaN if there is none that day |
  | `rise_az`, `set_az` | f8[nb, n] | azimuth from north through east; f8 because Mercury's rise-azimuth maxima are resolved to 0.0001° |
  | `sun_alt_at_rise`, `sun_alt_at_set`, `mag_at_rise`, `mag_at_set` | f4[nb, n] | |
  | `elong`, `lat_ecl` | f4[nb, n] | at local midnight; signed elongation, east positive |
  | `lon_ecl` | f8[nb, n] | at local midnight; apparent of date, geocentric |
  | `twl_eve_ut`, `twl_morn_ut` | f8[3, n] | Sun at −6°, −12° and −18° |
  | `star_alt_eve12`, `star_alt_morn12` | f4[ns, n] | |
  | `star_rise_ut`, `star_set_ut` | f8[ns, n] | |
  | `sun_alt_at_star_rise`, `sun_alt_at_star_set` | f4[ns, n] | |
  | `moon_frac_midnight`, `moon_up_frac_dark`, `night_len_h` | f4[n] | |
  | `meta` | JSON string | site, ΔT model, ephemeris file hashes, h0 values, refraction flag, code tree hash |

- **Rise** is the topocentric altitude of the centre crossing h0 = −0.8333°
  (Sun, Moon) or −0.5667° (planets, stars). It is found by Meeus' iterated
  hour angle and bisected to 0.1 s for Mercury and to 1 s otherwise.
- **Ephemerides.** Lunar quantities use DE431 and SMH2020 ΔT, in yearly
  chunks that never straddle JD 1721425.5. Planets and stars use DE441.
- **Size.** Every column over the full margins (−2060..+241, 840,000 days)
  takes about 0.9 GB. Only Ithaki is built so. Every other site has the span
  and column set of `sites.json` [r1 N12 fix 3].

**`odybench/events.py`**

```
conjunctions(jd_tt0, jd_tt1, ephemeris="de431") -> f8[k]      # yearly chunks; "de441" for T0b
full_moons(jd_tt0, jd_tt1, ephemeris="de431") -> f8[k]
stations(body, jd_tt0, jd_tt1) -> rec[("jd_tt","f8"), ("kind","U1")]   # R, D
greatest_elongations(body, jd_tt0, jd_tt1, sun="true"|"mean")
    -> rec[("jd_tt","f8"), ("side","U1"), ("elong","f8")]
oppositions(body, jd_tt0, jd_tt1, sun="true"|"mean") -> f8[k]
azimuth_extrema(sky, body, which="rise"|"set")
    -> rec[("jd_ut","f8"), ("kind","U3"), ("az","f8"), ("curv","f8"),
           ("margin","f8"), ("flat","?")]                      # parabola vertex, 7 days
visibility(sky, body, side, av: float | "plsv", crit_alt=0.0) -> bool[n]
star_phases(sky, star, av) -> rec per year: heliacal rising and setting,
    acronychal rising, cosmical setting (JDN)
season_bounds(sky, h_A, h_P) -> rec per year: A(y), P(y) (JDN)   # C_rel
equinoxes(jd_tt0, jd_tt1) -> rec[("jd_tt","f8"), ("kind","U2")]  # VE AE SS WS
first_crescent(sky, conj_jd_tt, criterion="yallop_B") -> i8     # JDN of the evening
```

**`odybench/deltat_mix.py`** (the four-model mixture, 0 and 6.3.3)

```
grid(jd_tt, frame="canon"|"de431", n=41) -> (dt_s: f8[4, n], w: f8[4, n])  # ±4σ per model, Gaussian weights, models equal
p_pass(fn: Callable[[float], bool], jd_tt, frame, sigma_scale=1.0) -> float
```

**`odybench/eclipses.py`**

```
catalogue(y0=-1999, y1=300) -> rec[idx, jd_td, dt_canon, gamma, type, saros, file, row]
local(ecl, lat, lon, dt_s, elev_m=0.0) -> dict(smag, obsc, central, duration_s,
      t_max_ut, sun_alt, lat_h, c1_ut, c2_ut, c3_ut, c4_ut)
totality_window(ecl, lat, lon) -> (dt_lo, dt_hi) | None      # canon frame
hit_strength(ecl, site, models=DT_MODELS, frame="canon", sigma_scale=1.0)
      -> dict(h_tot, h_09, h_06, by_model: {model: (p_tot, p_09, p_06)})
site_table(site) -> NPZ cached in data/cache/eclipses_<site>.npz
local_de431(ecl, site, dt_s) -> dict                         # ephem.local_circumstances on DE431
```

**`odybench/lunar.py`**

```
catalogue(y0, y1) -> rec[jd_tt, umag, pmag, type, gamma, lat_sign,
      p1, u1, u2, u3, u4, p4]                                 # contacts, JD TT; NaN if none
local(lecl, lat, lon, dt_s) -> dict(moon_alt at each contact, moonrise_ut,
      moonset_ut, seasonal night hour of each contact, mid_LAT_offset_h)
```

**`odybench/prereg_io.py`, `clues.py`, `search.py`**

```
load_controls_real() / load_controls_almagest(regime="SL"|"BM") / load_negatives()
      -> list[ClueSet]     # through operational_map.json and almagest_regimes.json; unknown key -> error
load_odyssey() -> (ClueSet, garden)                           # readings.json, garden.json
evaluate(pred: Predicate, pool, ctx) -> bool[len(pool)]       # dt_rule applied inside
evaluate_p(pred: Predicate, pool, ctx) -> f8[len(pool)]       # P_mix(pass), for reports
evaluate_rows(clueset, reading, pool, ctx) -> bool[n_rows, len(pool)]
search(clueset, reading, window: (jd0, jd1), ctx, scoring="strict"|"bestfit")
      -> SearchResult
make_redraft_brief(rows=("T1-DARK","T2-SEASON","T-INT-12","D-ECL","L4-DARK"))
      -> writes data/prereg/pcr_redraft_brief.json             # tools/make_redraft_brief.py
```

`prereg_io` refuses any path that matches `*_truth*` (I13). `ctx` holds the
sky tables, event lists and catalogues for the sites a clue set names.

**`odybench/pools.py`, `readings.py`, `reach.py`, `evidence.py`**

```
pools.targets(kind="T"|"T_C"|"T_A"|"T_A_E5", site="ithaki") -> rec[POOL_DTYPE]
pools.slot_A(pool, ctx) -> bool[len(pool)]                    # 4.2's Venus and Mercury slots
readings.garden(tier="BM"|"DOC"|"FULL", equinox=False, eclipse_compatible=False)
      -> Iterator[Reading]                                     # equinox=False: the rule gardens (F6 off)
readings.pinned(name) -> Reading        # "T0b", "BM", "R_anc", "R_anc_noecl"
readings.survivors(garden, pool, ctx) -> Iterator[(reading_index, f8[k] survivor JD_TT)]
reach.interval(t, s_prev, s_next, W_days) -> (lo, hi)         # empty if lo >= hi
reach.reach(targets: f8[m], survivor_sets, W_days) -> f8[m]   # |union| / W
reach.G(reach_values: f8[n], garden, pool, widths) -> GStat   # gamma interval of 5.3
reach.p_at_least_one(survivors, W_days, b0, b1, step_days=365.25) -> (empirical, poisson, mean)
evidence.bf(t_S, garden, pool, ctx, rho: float | dict) -> dict(bf, bf_max, p_r: f8[R], passes: bool[R])
evidence.lr_slot(garden, pool_TC, nu) -> dict(R_obs, G, P_A, P_wA, lr)   # exact reweighting, 5.7
```

Survivor sets are packed bit masks (uint64[ceil(n_pool/64)]) per option,
ANDed per reading in batches. A reading whose largest survivor gap is below
W contributes no reach and is skipped.

**`odybench/epic.py`, `pcs.py`, `harness.py`, `verdict_rule.py`, `prereg.py`**

```
epic.draw(n, variant, seed) -> list[ClueSet]
epic.garden_for(clueset, tier) -> list[Reading]
epic.enters(clueset, t_S, ctx) -> bool                        # categorical slots hold at Schoch's target (5.4)
pcs.instrument(truths, path="standish"|"horizons") -> list[ClueSet]
pcs.science(truths, nu, garden, ctx) -> rec per truth: recall per reading, reach, description
harness.place_window(set_id, width_years, k) -> (jd0, jd1)     # the only reader of truth_index.json
harness.score(set_id, result: SearchResult) -> dict(seen, strict_recall, f_truth, rank, resolution)
harness.exposure_audit(file="controls_real") -> list[dict(row, sibling, params, fails)]
verdict_rule.decide(q: dict, thresholds: dict) -> (set[str], set[str])
verdict_rule.check_structure(q: dict, n: dict) -> list[str]    # violated constraints of 9.4; [] if realisable
prereg.check_frozen() -> dict(commit, tree_hash, amendment)     # raises unless frozen
```

### 10.3 Canonical predicates and the translation of the prereg files

Three agents drafted the three prereg files, in three vocabularies.
`controls_real.json` and `controls_almagest.json` have machine-readable
`operational` dicts, while `negatives.json` has prose [pcr §5 item 2; lca
next-stage item 2; neg]. All three are translated into one set of canonical
predicates.

| type | parameters | used for |
|---|---|---|
| `anchor` | rule: conj_ut2, conj_lmt, conj_plus1, first_crescent, full_moon, day7, any_day, solar_eclipse, lunar_eclipse | Day 0 (F2; epics; controls) |
| `moon_phase` | class, tolerance (days) | phase rows. Classes are frozen by the Sun–Moon elongation E (east +): young crescent 0° < E ≤ 45°; waxing crescent 0° < E < 90°; first quarter \|E − 90°\| ≤ 12.2° × tol; near full 150°–210°; full \|E − 180°\| ≤ 12.2° × k; last quarter \|E − 270°\| ≤ 12.2° × tol; waning crescent 270° < E < 360° [me] |
| `moon_up` | interval of named instants, illuminated-fraction bounds, quantifier | negatives, PC-R |
| `moon_dark_share` | maximum share of the dark hours with the Moon up | H2 |
| `rise_lead`, `set_lag` | body, minutes | V; ALM visible_only (minutes between horizon crossings); `bm_venus_lead` |
| `visible` | body, side, AV (degrees or PLSV), critical altitude | F4, F5, H3, H5, the slots of T_A |
| `alt_at` | body or star, named instant, minimum altitude | ALM visible_before_sunrise (civil dawn), negatives |
| `turning_point` | body; event (greatest elongation from the true or mean Sun; station; rise- or set-azimuth extremum; first or last visibility; opposition to the true or mean Sun); side; k days (continuous); visibility required; displacement | M; ALM (`ge_true_k`, `ge_mean_k`, `bm_mwra_k`, `opp_*`); epics |
| `ge_relation` | body, side, before or after, j days or `same_apparition` | ALM A.1, B.1, I.1, J.4 |
| `star_covis` | stars, minimum altitude, twilight, span of nights, quantifier; or a season window (C_rel, autumn) | C; F3; epics |
| `star_phase` | star, phase, AV, k days | epics; negatives; R_anc's season bound |
| `rel_position` | body, reference (star, line through two stars, Moon's centre), offset or distance, tolerance, frame | ALM star and Moon rows; one branch per star candidate for F.4 |
| `sun_lon` | range (wrapping through 0°) | seasons in PC-R, R_anc |
| `equinox_offset` | event, offset range in days | E_rel; ALM-E.3 |
| `solar_eclipse` | smag range, central flag, minimum h_tot/h_09/h_06, timing (LAT of maximum, first contact after noon, last contact with the Sun up), site rule; `x_class` ∈ {X3, X4, X1–X4} mapped as in 6.3.3 and 6.5 | X; PC-R; negatives |
| `lunar_eclipse` | umag and pmag ranges, the Moon's latitude sign, timing (mid-eclipse offset from LAT midnight, first contact after moonrise, overlap or containment in seasonal night hours or a night quarter), the Moon's altitude at contacts, moonrise during the umbral phase at a site rule | PC-R; ALM-C |
| `interval` | from event, to event: exact nights, day range, or years ± tolerance | links |
| `calendar` | Egyptian (free epoch), Roman (named date, offset bound or free), Attic (month, lunation offset), report bounds | PC-R |
| `night_length`, `separation`, `herald`, `crescent`, `rise_azimuth` | as named | H1, H4, F4, F2(d), AEN-TROY's Ida rider |

**Translation rules.**

- **The two controls files.** Their keys map to these types by fixed rules
  in `prereg_io.py`. Their free-text values (relation strings such as
  "umbral phase overlaps hour", site names such as "Tigris camp") are listed
  in `operational_map.json`. An unknown key or value is an error, never a
  default.
- **The negatives.** Each `negatives.json` option gets a full canonical
  predicate in `operational_map.json`, drafted by A3 and checked against its
  prose by A9 (I13).
- **ΔT-dependent predicates** pass when P_mix ≥ 0.5 (`dt_rule="mixture_p50"`),
  with 0.05 and 0.95 as reported sensitivities (6.3.3).

### 10.4 Independent second implementations

Issue 13 asked which code paths get an independent check, against what, and
at what tolerance. Every derived quantity the verdict rests on has one:

| code path | independent implementation | cross-check | tolerance | check |
|---|---|---|---|---|
| `sky.py` rise and set | JPL Horizons rise/transit/set; the grid-plus-bisection finder of `results/critique-design/check_mwra.py` | 1,000 events; 2,000 events | 0.5 min; 0.1 s | I5 |
| `events.py` stations, greatest elongations, azimuth extrema | `results/bm2008-reconcile/check_mwra.py`; the Standish code of `results/bm2008-b-checks/` | 152 S2 years; 500 events | same civil date in ≥ 150/152 and 0.05 d; 1 d | I6 |
| `events.py` heliacal phases, B&M's spring limits, Arcturus' rising | `docs/research_visibility_calc.py`; `results/design-revision-r2/ranc_season.py` | −1177, −700, −1130 | 1 d | I6 |
| `events.py` first crescent | the Yallop code of `research_visibility_calc.py` | 500 lunations | ≥ 495 equal | I12 |
| `eclipses.py` | NASA's `program.js` in Node (`data/jsex/sites/`); `results/critique-design/check_bessel.py` | 5 sites × 5,486; four totality windows | smag 0.0005, 0.002 h; 5 s | I2 |
| `lunar.py` | NASA LEcat5 | the PC-R and ALM centuries, plus 300 random | 0.02; 3 min | I4 |
| `deltat_mix.py` | `ephem.delta_t` and `ephem.delta_t_sigma` evaluated directly, and a 10⁶-draw Monte Carlo of the mixture | P(total) for 1178 and 1131 BC on NASA's elements against the 2.3 table | 0.005 | I2 (added row) |
| the B&M reading through `clues.py`, `readings.py`, `search.py` | `tests/bm_reference.py` (A7) | every T0 cell; 300 random years | identical flags | I7 |
| `reach.py` reach | brute-force sliding windows | 10,000 synthetic sets | 0.0002 | I9(a) |
| `reach.G` interval | simulation of coverage | 10,000 reach vectors per cell | coverage ≥ 0.95 | I9(b) |
| `pools.py` and `readings.py` together | the identity G(𝒢_BM*, T) = (n_A/n_T) G(𝒢_BM*, T_A) | the real tables | exact | I9(c) |
| the PC-S generator | Standish code; Horizons subsample | 200 truths (50 via Horizons) | recall 1.000 | I10 |
| `evidence.lr_slot` | end-to-end simulation in `pcs.science` | 2,000 truths per noise cell | within the simulation interval | I10b |
| `calendar.py` | exhaustive day counting; the Horizons calendar | −1999..+500 | exact | I8 (done) |
| `prereg_io.py` | the licence checkers' dump scripts; A9's review; the brief's leak scan | every row | exact | I13 |
| `verdict_rule.py` | the hand-computed synthetic sets; the structural constraints | 12 sets; 6 constraints | exact | I14 |

### 10.5 Scripts (top level, as in labench)

| script | test | writes |
|---|---|---|
| `reproduce.py` | T0a, T0b, T0c | `results/t0/` |
| `rates.py` | N1 | `results/n1/` |
| `coincidence.py` | N2 | `results/n2/` |
| `garden.py` | N3, R_anc, the evidential findings of 5.7 | `results/n3/` |
| `randomepic.py` | N4 | `results/n4/` |
| `windows.py` | N5 | `results/n5/` |
| `deltat.py` | N6 | `results/n6/` |
| `synthetic.py` | PC-S (both modes) | `results/pcs/` |
| `controls.py` | I2b, PC-R, the exposure audit | `results/pcr/` |
| `almagest.py` | the *Almagest* control and its Bayes factors | `results/alm/` |
| `negatives.py` | the negatives, the Iliad comparison, I11 | `results/nc/` |
| `heldout.py` | section 7 | `results/heldout/` |
| `verdict.py` | section 9 | `results/VERDICT.md`, then the findings in `README.md` |
| `read.py` | a reader: `py read.py -1177-04-16` prints the sky of Days −40 to +1 beside each clue and held-out predicate, as labench's `read.py` prints a tablet | stdout |

Every script writes three kinds of output, each stamped with the commit and
code tree hash it ran under:

- a machine-readable `<name>.json`;
- a human-readable `<name>.out.txt`;
- `.tsv` tables, where useful.

**Tools.**

- New: `tools/fetch_ephem.py` (extended to +300), `tools/fetch_lecat.py`,
  `tools/fetch_horizons_rts.py`, `tools/build_sky.py`,
  `tools/build_events.py`, `tools/build_eclipses.py`,
  `tools/build_truth_index.py`, `tools/make_redraft_brief.py`,
  `tools/validate_events.py`, `tools/validate_eclipses.py`,
  `tools/freeze.py`.
- Existing: `validate_ephem.py`, `validate_coverage.py`, `fetch_jsex.py`,
  `jsex_sites.js`, `fetch_stars.py`.

**Tests**, each runnable as `py tests/test_x.py`:

| test | covers |
|---|---|
| `test_calendar.py`, `test_ephem.py` | exist |
| `test_t0.py` | S2 replay, A1–A5 |
| `test_reach.py` | I9 |
| `test_clues.py` | hand-built predicate cases, and the B&M reading on S2's rows |
| `bm_reference.py` | I7 |
| `test_eclipses.py` | I2 |
| `test_lunar.py` | I4 |
| `test_events.py` | I5, I6, I12 |
| `test_prereg_io.py` | I13 |
| `test_verdict.py` | I14 |

---

