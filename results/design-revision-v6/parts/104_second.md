### 10.4 Independent second implementations

Issue 13 asked which code paths get an independent check, against what, and
at what tolerance. Every derived quantity the verdict rests on has one.
Since revision 6 that includes the control searches that produce the gate
counts (I16) [r1v5 N6]. The tolerances are those of 6.1, each set against
its reference's measured accuracy, or against an accuracy that is measured
before the comparison is read [r2 R2-4; r1v5 N4]. The Standish
low-precision code is no longer a reference anywhere: its elements were
typed from memory, and it has no Mars and no stars (6.1).

| code path | independent implementation | cross-check | tolerance | check |
|---|---|---|---|---|
| `sky.py` rise and set | JPL Horizons observer tables (airless, fractional seconds, Horizons' own ΔT); the 0.01-s rise finder of `results/critique-design/check_mwra.py` | 1,000 events; 2,000 events | 1 s + (\|ΔGMST\| + 20″)/(15.04″ s⁻¹), at most 7.6 s; the sum of the two convergence tolerances plus 0.01 s (0.12 s for Mercury, 1.02 s otherwise) | I5 |
| `events.py` rise-azimuth extrema | `tests/mwra_reference.py` (A7), on the review's 0.01-s rises | 152 S2 years | the same civil date outside a 0.0005° tie band; vertex within 0.02 d, or 0.5 d at flat maxima | I6(a) |
| `events.py` stations, GWE, inferior conjunctions | `results/bm2008-reconcile/check_mwra.py` (daily samples) | 152 S2 years | within the reference's civil day ± 1 d | I6(a) |
| `events.py` stations, greatest elongations, oppositions | Horizons geocentric tables, 6-hourly, interpolated by the check | 200 events | 0.01 d | I6(b) |
| `events.py` heliacal phases, B&M's spring limits, Arcturus' rising | `docs/research_visibility_calc.py`; `results/design-revision-r2/ranc_season.py` | −1177, −700, −1130 | 1 d | I6(c) |
| `events.py` first crescent | the Yallop code of `research_visibility_calc.py` | 500 lunations | ≥ 495 equal | I12 |
| `eclipses.py` | NASA's `program.js` in Node (`data/jsex/sites/`); `results/critique-design/check_bessel.py` | 5 sites × 5,486; four totality windows | smag (NASA's magnitude, section 0) 0.0005, 0.002 h; 6 s | I2 |
| `lunar.py` | NASA LEcat5 | every lunar eclipse of the 23 century pages −1999..+300, about 5,500 [r1v5 N15b] | 0.02; 3 min; type tie band at magnitude 0; the convention checked first on three pages | I4 |
| `deltat_mix.py` | `ephem.delta_t` and `ephem.delta_t_sigma` evaluated directly, and a 10⁶-draw Monte Carlo of the mixture | P(total) for 1178 and 1131 BC on NASA's elements against the 2.3 table | 0.005 | I2(c) |
| the B&M reading through `clues.py`, `readings.py`, `search.py` | `tests/bm_reference.py` (A7) | every T0 cell; 300 random years; (a) masked, (b) the target | identical flags outside the tie bands of 6.1 | I7 |
| `heldout.py` (H3, H4) | `tests/heldout_reference.py` (A7) on `ephem` positions; Horizons geocentric tables for every member | every member of P_BM, which contains the other three pools; (b) the target | identical flags outside the tie bands of 6.1; 0.01 d and 0.001° against Horizons | I15 |
| `heldout.p_pool` and the max over the four pools | `results/design-revision-v6/verdict_trace.py`'s `p_pool`, an independent transcription of 7.2 | every cell of the lattice, on the design-stage and the measured counts | exact | I14 |
| the control searches: `search.py` and `harness.score` | `tests/control_reference.py` (A7, public tier), with `program.js` for solar circumstances, its own lunar-shadow geometry and its own ΔT mixture | every counted set and leg, and the regime-SL, regime-BM and held-out runs; 21 random background windows per set (null-side stage) and the gates' own windows (controls stage) | identical per-row flags and f(c) outside the tie bands of 6.1; identical seen and strict flags | I16 |
| `reach.py` reach | brute-force sliding windows | 10,000 synthetic sets | 0.0002 | I9(a) |
| `reach.G` interval (gamma and block bootstrap) | coverage on synthetic cores built from real 243-year blocks | 2,000 cores | each side's coverage ≥ 0.975 − 3 SE, about 0.965 [r1v5 N14] | I9(b) |
| `pools.py` and `readings.py` together | the identity G(𝒢_BM*, T) = (n_A(v)/n_T) G(𝒢_BM*, T_A(v)) for v1–v5 | the real tables, masked | exact | I9(c) |
| the PC-S generator | Horizons for the Sun, Moon and planets; the Meeus-based star routines of `research_visibility_calc.py` | 200 truths | recall 1.000 | I10 (reported) |
| `evidence.lr_slot` | end-to-end simulation in `pcs.science` | every core truth of T_C per noise cell, accepted by A(t, δ) | within the simulation interval in ≥ 11 of 12 cells | I10b (reported) |
| `calendar.py` | exhaustive day counting; the Horizons calendar | −1999..+500 | exact | I8 (done) |
| `prereg_io.py` | the licence checkers' dump scripts; A9's review; the brief's leak scan | every row | exact | I13 |
| `almagest_regimes.json` (projection, held-out rows) | `results/design-revision-v6/alm_rows.py`, a transcription of 6.4's rules written before the file | every row of the 12 sets | identical lists | I13(f) |
| `pcr_projection.json` | `results/design-revision-v6/pcr_rows.py`, a transcription of 6.3's rule written before the file | every row of the 9 sets | identical lists | I13(f) |
| `tools/public_design.py` and `tools/export_public.py` (the build agents' copy and texts) | the truth files, read by A6's leak scan, with minus signs normalised and year-only forms matched | every accepted date and year | none present outside the frozen allowlist | I13(h) |
| `verdict_rule.py` | the synthetic sets as traced by `results/design-revision-v6/verdict_trace.py`; the structural constraints; the rerun with the measured null side | 21 sets; 11 constraints | exact | I14 |

