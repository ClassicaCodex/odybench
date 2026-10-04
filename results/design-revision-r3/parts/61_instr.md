### 6.1 Instrument checks

Each check compares a code path with something that does not share its code
[rev #13].

**INSTR** is the conjunction of the checks that guard a rule input:

- I1, I2, I2b, I4, I5, I6, I7, I8, I9, I11, I13, I14 and I15;
- `verdict.py` refuses to run unless INSTR holds.

**Reported beside INSTR, not part of it** [r2 R2-4 fix 2]:

- I3, a calibration;
- I10 and I10b, PC-S, which feeds no rule;
- I12, the first crescent, which enters only the DOC and FULL gardens.

A failure of one of these is reported in `VERDICT.md`. It blocks nothing.

**Every pass criterion can be met by a correct implementation** [r2 R2-4]:

- **Tie bands.** Where a check compares flags at a continuous threshold,
  the flags may differ only for candidates whose margin to the threshold is
  below a stated ε. Those candidates are listed.
- **Convergence.** Where both sides converge numerically, the tolerance is
  at least the sum of their convergence tolerances.
- **Monte Carlo.** Where the check itself is a Monte Carlo estimate, the
  pass bound allows three standard errors.

A check marked "post-freeze" runs first after the freeze. The outputs it
guards are not opened until it passes, and a fix it forces is a dated
amendment (section 12).

| # | what is checked | compared against | pass | guards | when |
|---|---|---|---|---|---|
| I1 | ephemeris | Horizons; `validate_ephem.py`; `test_ephem.py`; `validate_coverage.py` | 55/55, 10/10, all coverage checks [acq §1.3] | everything | done; rerun pre-freeze |
| I2 | solar-eclipse local circumstances, `eclipses.py` (Python port of NASA's JavaScript, from `results/research-critiques/eclipse_local.py`) | (a) NASA's own `program.js` run in Node: `data/jsex/sites/*.jsonl`, 5 sites × 5,486 eclipses; (b) the review's independent Besselian solver `results/critique-design/check_bessel.py` [rev #13 fix 6]; (c) `deltat_mix.py` against the 2.3 table and a 10⁶-draw Monte Carlo | (a) **smag**, NASA's magnitude as defined in section 0, within 0.0005 of the catalogue's `mag` [r2 R2-7]; time of maximum within 0.002 h; Sun altitude within 0.05°; central flag identical, except where the site lies within 10⁻⁴ (in Earth radii) of the umbral or antumbral edge (tie band, listed). (b) Totality windows for 1178, 1131, 1312 and 1183 BC within 6 s, the review's 5-s grid plus 1 s. (c) P(total) per model and for the mixture within 0.005 | h_tot, hit_j, PC-R solar rows | pre-freeze |
| I2b | language-to-magnitude: local magnitudes for the dated eclipses of [ctl §3] | the values printed in [ctl §3], moved to the truth-side file `data/prereg/i2b_reference.json` | **like with like** [r2 R2-7; r1 N15]. The reference used the partial formula (r☉ + r☾ − sep)/(2r☉) [ctl §2.2], so the bench side is `smag_partial`. The bench side is `eclipses.local` on NASA's elements at the element row's canon ΔT. The reference side is Horizons DE441 geometry at NASA's catalogue ΔT, by the longitude-shift equivalence, which mixes frames by the DE441 − canon offset (about 90 s at −430). Pass: within 0.02, or within the change produced by ±100 s of ΔT if that is larger; above 0.95, the central flag agrees | PC-R solar rows | pre-freeze, after the re-draft of 6.3.4 |
| I3 | Hesiod's star calendar at 701 BC, 38.37°N | Hesiod's own numbers | **a calibration** [rev #20; r1 N15]: the Pleiades' AV is set so that they are hidden 40 days (*WD* 385–386); "Arcturus ≥ 5° at nautical dusk" is read off *WD* 564–567 | — (reported) | pre-freeze |
| I4 | lunar eclipses, `lunar.py` | NASA LEcat5 rows: every lunar eclipse in the PC-R and ALM truth centuries, and 300 drawn at random from −1999..+300 | type identical, except where umag or pmag lies within 0.002 of 0 (tie band, listed); umag and pmag within 0.02; greatest eclipse within 3 min after removing the ΔT difference | PC-R lunar rows, ALM-C | pre-freeze |
| I5 | rise, set and transit, `sky.py` | (a) JPL Horizons rise/transit/set output for 1,000 random events (Sun, Moon, Venus, Mercury, Jupiter, Sirius, Arcturus; Ithaki, Alexandria, Troy; −1999..+300; same h0, airless); (b) the dense-grid-plus-bisection rise finder of `results/critique-design/check_mwra.py`, on 2,000 events | (a) within 0.5 min after removing the documented sidereal-time convention difference (5 s at −1999 [acq §1.3]); (b) within the sum of the two convergence tolerances plus 0.01 s: 0.12 s for Mercury (0.1 s bench, 0.01 s reference) and 1.02 s otherwise | every sky clue | pre-freeze |
| I6 | derived events, `events.py` | (a) the event lists of `results/bm2008-reconcile/check_mwra.py` (rise-azimuth maxima and minima, stations, GWE, inferior conjunction) for all 152 S2 years; (b) the low-precision Standish-element code `results/bm2008-b-checks/ephem.py`, 500 random stations and greatest elongations; (c) heliacal star phases and B&M's spring limits from `docs/research_visibility_calc.py` at −1177 and −700; Arcturus' heliacal rising at −1177 and −1130 against `results/design-revision-r2/ranc_season.py` | (a) same UT+2 civil date in ≥ 150 of 152; vertex instants within 0.05 d for maxima not flagged flat, and within 0.5 d for flat ones, which are listed (the two codes fit different parabolas, and a flat maximum's vertex is ill-conditioned [rev #12]); (b) within 1 d; (c) within 1 d | M, H3, the ALM rows, C_rel | pre-freeze |
| I7 | B&M's reading through `clues.py`, `readings.py` and `search.py` | `tests/bm_reference.py`, a minimal second implementation written by a different agent from section 3.2's text alone, using only `ephem.altaz` and its own rise bisection [rev #13 fix 4] | identical pass flags (N, C, V, M, E, every T0 grid cell) for every candidate in 1250–1115 BC and in 300 random background years, **except** inside the tie bands [r2 R2-4 fix 3]: \|Δ\| within 0.01 d of a Mercury tolerance; Venus lead within 0.05 min of 90 min; an E or C bound decided by a star or equinox instant within 0.01 d of a civil-day boundary. Every tie-band candidate is listed with both values | T0_pass, G, P_BM | (a) null-side stage, on the masked pool (every candidate but the target), before any G is read; (b) the target's own flags after the second freeze, before any T0 output is read |
| I8 | calendar | `tests/test_calendar.py` | 11/11 [acq §4] | everything | done |
| I9 | reach, G and the pools | (a) a brute-force implementation that slides windows in 0.01-year steps, on 10,000 random synthetic survivor sets; (b) coverage of the G interval of 5.3 on **dependent** synthetic data: 2,000 synthetic cores, each built by concatenating randomly drawn 243-year blocks of the real candidate sequence with all their flags, so that real clustering is kept; the true G of the block population is computed on a 100,000-year synthetic background [r2 R2-6]; (c) the identity G(𝒢_BM*, T) = (n_A(v)/n_T) G(𝒢_BM*, T_A(v)) for v1–v5 on the real tables | (a) reach equal within 0.0002; (b) coverage of G_hi and of G_lo each at least 0.95 − 3 × its Monte Carlo standard error (about 0.935); (c) exact to float rounding | G_BM, G_BM,u, G_j, r_Ody | pre-freeze (a); null-side stage, before any G is read (b, c): (b) and (c) need the real survivor flags, which are null results |
| I11 | plumbing negatives (revision 1's NC4 and NC5 [rev #15 fix 4]) | (a) AEN-TROY's pinned R-ii-literal reading, conjunction on Day 0 with the Moon up after nightfall, which contradicts itself [neg §3.1]; (b) a synthetic set with Day 0 a conjunction and the Moon above the horizon at local midnight; (c) Hesiod's star calendar (*WD* 383–385, 564–567, 609–611, 615–621) as event clues around an arbitrary Day 0 | (a), (b) zero survivors in every window (a is known to hold at Troy in two windows, 2.6); (c) no unique survivor in any 136-year window | hit_j | post-freeze |
| I13 | prereg I/O | (a) every licence string present in its cited row, comparing raw characters without Unicode normalisation (the Ptolemy export mixes tonos and oxia, and prints the half-sign as the literal "U+2220") [lca; pcr §5]; (b) every fork option of every row translates to a canonical predicate (10.3), with exactly one primary per controls row; (c) no module but `harness.py` and `tools/build_truth_index.py` opens a `*_truth*` path or contains the Nabonassar epoch; (d) `operational_map.json` is reviewed by a second agent; (e) the re-draft brief of 6.3.4 contains no statement, option name or justification string of `controls_real.json`, and exactly the five briefed rows; (f) `almagest_regimes.json`, `slots.json`, `sibling_pairs.json` and `deltat_circular.json` parse, and every value they name exists in the clue files; (g) the target mask: with `mask_target=True`, evaluating any predicate on 16 Apr −1177 raises, and a static test finds no target-side call in `attain.py` | all pass | every control and the null-side stage | pre-freeze |
| I14 | the decision rule | (a) the synthetic input sets of 9.5; (b) the structural constraints of 9.4; (c) at the null-side stage, the sets rerun with every null-side field replaced by its measured value | (a) each returns its stated labels and qualifiers; (b) every set marked "realisable" satisfies every constraint, including C7; (c) recorded: which outcomes stay reachable with the measured null side, and Q_attain, Q_tol and Q_slot | the verdict | pre-freeze (a, b); null-side stage (c) |
| I15 | the held-out predicates H3 and H4, `heldout.py` (new) [r2 R2-1 fix 4] | (a) an independent implementation on the Standish low-precision code of `results/bm2008-b-checks/ephem.py`, with its own rise bisection, for every member of P_BM; (b) Horizons for 50 members drawn at random | identical flags except inside the tie bands: a conjunction instant within 0.1 d of the ±3-d bound; a Venus–Mars separation within 0.1° of 5°; a Sun altitude within 0.1° of −AV at a planet's rising or setting. Tie-band members are listed | p_H, p_H,min | null-side stage, on the masked pool, before p_H,min is read; the target's flags after the second freeze, before p_H is read |

Revision 1's NC4 (the Hymn to Hermes) is dropped: it misread *h.Herm.* 141,
where παννύχιος closes Hermes' clause [rev #15].

Reported checks, beside INSTR:

- **I10**, PC-S instrument mode: recall 1.000 on an independent path (6.2).
- **I10b**, the exact R_obs of 5.7 against an end-to-end simulation, with
  one estimand (6.2) [r2 R2-4 fix 1]. Pass: agreement within the
  simulation's 95% interval in at least 11 of the 12 noise cells. One cell
  in twelve may miss by chance.
- **I12**, the first-crescent evening against the Yallop implementation in
  `docs/research_visibility_calc.py`, over 500 lunations. Pass: the same
  evening in ≥ 495.

