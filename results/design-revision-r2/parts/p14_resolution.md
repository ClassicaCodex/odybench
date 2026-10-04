## 14. Resolution of the reviews

Two tables follow. The first gives the 25 issues of `docs/critique-design.md`
(the review of revision 1), the second the 17 new issues of
`docs/critique-design-r1.md` (the recheck of revision 2). Each row gives the
resolution and the sections it changed. Where a resolution departs from the
reviewer's proposed fix, the row says why, marked **Departure**.

### 14.1 The review of revision 1 (`critique-design.md`)

The recheck found 20 of these resolved by revision 2. It found #1, #16, #17
and #18 unresolved for reasons new to revision 2, and #3 resolved only in
part [r1 §1]. Revision 3 resolves those five through the new issues of 14.2,
as the rows say.

| # | severity | resolution in revision 3 | sections |
|---|---|---|---|
| 1 | blocker | **Now resolved.** The rule is a pure function of named quantities (9.1–9.2), and every condition names its garden and its target pool. Revision 2's unreachable NC condition stays replaced by the calibrated percentile pct_N4. Revision 2's outcome 1 was still unreachable, because its likelihood ratio was capped near 6.5 [r1 N1]. Revision 3 removes every likelihood ratio from the rule. Outcome 1 rests on T0 = R, on G over T_A with its gamma upper bound, on pct_N4, on the gates and on the negatives. The background is extended so that the pool is large enough for the upper bound to fall below 0.05 (4.1, 2.8). Twelve synthetic sets reach every outcome, the inconclusive verdict, each qualifier and the instrument block. Each set is checked against the structural constraints of 9.4 (I14b), so what is proved reachable is an outcome and not a code branch. `freeze.py` and Q_attain test attainability with the measured pool sizes. **Departure** (kept from revision 2): the percentile is taken on the reach of Schoch's target rather than on G, because G of a text with few clues falls to 0 whether or not it is dated | 1.3, 4.1, 5.3, 5.4, 5.7, 9, 12.1 |
| 2 | blocker | Resolved in revision 2 and confirmed by the recheck. `controls_real.json` was rebuilt from the texts, frozen before any accepted date was looked up, and licence-checked blind. Revision 3 closes the subtler leaks the recheck found. An unflagged answer-dependent primary (T2-SEASON) and a near-edge tolerance (T-INT-12) are re-drafted from a brief and audited against their sibling conventions (6.3.4). The ΔT models that were fitted to control eclipses are tested by Q_ΔT (6.3.3). The *Almagest* tolerances are no longer set at the truth's own maxima (6.4) | 2.6, 6.3, 6.4 |
| 3 | blocker | **Now resolved.** Outcome 3 stays split into 3a (PC-R) and 3b (the *Almagest* control) [rev #3]. The recheck found that 3b could not fire and that Q_BM was undefined [r1 N2, N3]. Revision 3 sets the observer slack leave-one-set-out, so that every set is scored as held out. It names B&M's option rule, and it removes the definitional PC-S recall from the gate. What the truth-side slack already decides is stated in 2.6: truth is retained in 9 of 11 sets, and Q_BM holds. Only narrowing remains open (P25) | 1.3, 2.6, 6.2, 6.4, 9 |
| 4 | major | Resolved and confirmed. The freeze is a local git commit of the design, the prereg files and all code. `PREREG.sha256` holds the commit hash, the git tree hashes and a git-independent code tree hash. Amendments are dated and state which outputs had been read. Unfrozen runs are stamped and refused by the verdict. Publishing the hash outside the machine is optional and needs Jon's explicit permission (12.5). Revision 3 updates only the file lists | 12 |
| 5 | major | Resolved and confirmed. Section 1.1 says that the 6 years is the C ∧ E rate. The two comparisons are P4 (0.88 per century, E off) and P5 (0.048 printed, E on) | 1.1, 2.4, 5.1, 8 |
| 6 | major | Resolved and confirmed: MacDonald was read, and both p_fix figures are reported with the frozen reason. Revision 3 applies the same reason uniformly, to V, M and E as well as C [r1 N6] | 1.1, 2.5, 5.1, 5.3 |
| 7 | major | Resolved and confirmed. The gardens are nested, with sources per option. The rule gardens leave out E: 𝒢_BM* 36, 𝒢_DOC* 35,964 and 𝒢_FULL* 767,232 readings, with revision 2's sizes reported for the E-on gardens. The greedy smallest fork set is reported, now up to G ≥ 0.20 over T_A | 5.3 |
| 8 | major | Resolved and confirmed: fork F1b, PC-S jitter of 0–3 d, and the decay of reach and recall | 5.3, 6.2 |
| 9 | major | Resolved and confirmed: C_rel and E_rel outside T0b, and λ per century under both kinds of bound. P9 is restated for the longer background | 4.5, 5.1, 8 |
| 10 | major | Resolved and confirmed. Hit strength comes from the mixture; the target is excluded from its own base rate; a site-rotated rate is computed; Schoch's 10–12 h rule is reported. The background now reaches +200 | 4.1, 4.4, 5.2 |
| 11 | major | Resolved. Base rates are conditional on the reading, and H1 and H5 are not counted. Revision 3 counts H3 once [r1 N14] | 7 |
| 12 | major | Resolved. MWRA is a vertex fit, rises converge below 0.1 s, flat maxima are flagged, and sensitivities and I6 are added. Revision 3 makes ±1.5 d, B&M's integer tolerance as a continuous one, the primary test [r1 N13] | 2.2, 3.2, 3.5, 6.1 |
| 13 | major | Resolved and confirmed: every derived quantity has a second path (10.4). Revision 3 adds the coverage check of the G interval and the pool identity (I9b, c), the exact-against-simulated check of R_obs (I10b), and a Monte Carlo check of the ΔT mixture | 6.1, 10.4 |
| 14 | major | Resolved. PC-S has an instrument mode (I10, recall 1.000) and a science mode. Revision 3 removes the definitional science-mode recall from gate 3b [r1 N2]; science mode is now a noise study that feeds no rule | 6.2 |
| 15 | major | Resolved and confirmed. The Iliad is a same-tradition comparison. Twelve clean negatives were drafted and licence-checked. Random poems are the main negative. NC4 and NC5 became I11, and I11(a) is known to hold at Troy (2.6) | 2.6, 6.1, 6.5 |
| 16 | major | **Now resolved.** The recheck showed that any ratio R_obs/G on the fixed poem is bounded by 1/P(A), and that T_C holds about 480 targets, not thousands [r1 N1, N8]. Revision 3 states the identity and reports the ceiling as a finding (5.7, 2.8). It takes every likelihood ratio out of the rule, gives every G a gamma interval, enlarges the pool by extending the background, computes R_obs exactly with one reach definition on both sides, and calibrates the reported Bayes factor on the *Almagest*. **Departure:** the review asked for the LR to be defined on one event (done in revision 2) and to decide outcomes 1 and 2. Revision 3 keeps it out of the rule, because on a fixed poem every such ratio is set by the observation model, not by the Odyssey [r1 N1] | 2.8, 4.1, 5.3, 5.7, 9 |
| 17 | major | **Now resolved.** Everything computable from known numbers is in section 2 with its numbers. That includes revision 2's settled predictions P23, P26, P30, P32, P34, P36, P41 and P42 (2.7), the recheck's numbers, and what they imply for the verdict (2.8). Section 8 separates regression expectations (R1–R12, not counted) from predictions that need new runs (P1–P35) | 2, 8 |
| 18 | major | **Now resolved.** R_anc's season comes from ancient definitions: the union of Hesiod's agricultural autumn and winter (from Arcturus' heliacal rising) and Geminus' astronomical seasons (to the spring equinox). Arcturus' rising was computed for −1130 (2.8). R_anc runs with and without the eclipse clue, and only the version without it gives a comparable coincidence, which is empty by arithmetic. The known part of revision 2's P23 moved to 2.8 and R11; P19 is the new prediction [r1 N7, N9] | 2.8, 5.3, 7, 8 |
| 19 | minor | Resolved and confirmed: one Espenak–Meeus model, four models in the mixture | 0, 2.3 |
| 20 | minor | Resolved. A1–A5 are regression tests. I3 is a calibration, now also left out of INSTR [r1 N15] | 3.4, 6.1, 9.1 |
| 21 | minor | Resolved and confirmed: the magnitude definitions are pinned, and I2b compares like with like, with both sides now named [r1 N15] | 0, 6.1 |
| 22 | minor | Resolved and confirmed: epoch −1176.68; the window is half-open, built with `span_bounds`; the count is expected (R6) | 0, 2.2, 3.2, 8 |
| 23 | minor | Resolved. The T0 grid covers E, visibility and the MWRA definition. T0b's reading (F6 off) is a member of 𝒢_BM* | 3.2, 3.5, 5.3 |
| 24 | minor | Resolved and confirmed: all six slips corrected. The recheck's new slip of the same kind is corrected too [r1 N17] | 1.1, 4.4, 5.3, 6.4, 7, 13 |
| 25 | minor | Resolved and confirmed: the HIP numbers were verified, and Sirius uses the barycentric proper motion | 2.1, 13 |

### 14.2 The recheck of revision 2 (`critique-design-r1.md`)

| # | severity | resolution in revision 3 | sections |
|---|---|---|---|
| N1 | blocker | **The identity is stated** in 5.7: on a fixed poem, LR_slot = P_w(A)/P(A) ≤ 1/P(A). P(A) = 0.154 and the ceiling of about 6.5 are in 2.8 as known numbers (fix 1). **Option (a) is taken** (fix 2): no likelihood ratio enters the rule, and the ceiling is printed with every verdict as a finding. Under revision 3's uniform conditioning, LR_slot over T_A is identically 1. The evidence that remains (B&M's tolerances beyond the categorical readings) is measured by G over T_A, and it is reported as a Bayes factor BF_BM under B&M's own encoding hypothesis, with its ceiling. Fix 3, an I14 assertion against LR thresholds, has nothing to assert, because the rule holds none. It is generalised: I14(b) checks every synthetic set against the structural constraints of 9.4, `freeze.py` refuses to freeze if outcome 1 is unattainable with the measured pool sizes, and Q_attain reports it at verdict time. The estimator is run on the *Almagest* sets (fix 4) | 1.3, 2.7, 2.8, 5.7, 6.1, 9, 12.1 |
| N2 | major | **SL tolerances are set leave-one-set-out** (fix 1), so every set is scored as held out (fix 2). **rec_PCS is removed** from the gate (fix 3). The regime values are recorded (fix 4). **Departure:** they go in a new frozen file, `almagest_regimes.json`, instead of an edit to the licence-checked clue file. The clue file then stays byte-identical to its recorded hash, and I13(f) ties the two together. What the truth-side slack already decides is stated in 2.6, and only narrowing remains open | 2.6, 6.2, 6.4, 9, 12.1 |
| N3 | major | **The option rule for regime BM is named:** B&M's proxy where the row offers it; else `ge_true_k` at 1.5 d; else the primary. Under it Q_BM is known to hold (rec_ALM_BM ≤ 5), so it is in 2.6 and is a regression expectation (R9) | 2.6, 6.4, 8 |
| N4 | major | Every ΔT-dependent control row is scored under the four-model mixture, P_mix ≥ 0.5 (fix 1). The circular controls (R-DIOD and L4 from Table S10 v2020; T1 and X3 from SMH2016, *secondary*) are listed (fix 2). Q_ΔT reports whether gate 3a changes when they are rescored, and the gate is also reported without them (fix 3). SMH2016's Table S4 and §4b, and the 2020 Addendum, are read before the freeze into `deltat_circular.json` (fix 4). **Departure:** the review suggested Espenak–Meeus for the rescoring. Revision 3 triples every model's σ instead, because Espenak–Meeus also rests on fits to ancient eclipses | 2.6, 6.3.3, 9, 12.1 |
| N5 | major | T2-SEASON and T-INT-12's tolerance join the re-draft (fix 1). A sibling-convention audit lists every row whose primary passes the truth while a sibling convention fails it, and gate 3a is recomputed with those rows (fixes 2–3). Q_exposure uses both. Section 6.3.4 says plainly that the re-draft controls exposure to files only (fix 4) | 2.6, 6.3.4, 9 |
| N6 | major | **The principle is applied uniformly** (fix 1). The categorical readings C, V and M are conditioned (pool T_A). G is reported under T_C and T_A, and with the E-on gardens (fix 2). T0 = RE does not count toward outcome 1 (fix 3). **Departure:** E is not conditioned on but left out of every rule garden. Conditioning on E would leave about 28 targets, too few for any interval to fall below 0.05, and E has no tolerance part that could survive conditioning. Leaving it out removes E's contribution from the Odyssey and the null alike | 1.1, 1.3, 2.8, 3.5, 4.2, 5.3, 5.4, 9 |
| N7 | major | P26, P30, P32, P34, P36, P41 and P42 are moved to section 2, either as settled (2.7) or as regression expectations (R7–R9) (fix 1). P23 is restated with an ancient season bound: its known part is in 2.8 and R11, and P19 is new (fix 2). P36 is settled by N3 (fix 3) | 2.7, 2.8, 8 |
| N8 | major | R_obs is computed exactly by reweighting over T_C and every δ (fix 1). Every G has a gamma interval, with the upper bound used in outcome 1 and the lower in outcome 2 (fix 2). One reach definition and one garden are used on both sides of every reported ratio (fix 3). Beyond the fixes, the background is extended to +200, so that n_A is about 139 and not 74 | 4.1, 4.2, 5.3, 5.7, 9 |
| N9 | minor | The season bound is sourced from ancient definitions (Hesiod's Arcturus and Pleiades phases, Geminus' equinoxes and solstices; their union is primary) (fix 1). R_anc is reported with and without the eclipse clue (fix 2) | 2.8, 5.3, 8 |
| N10 | minor | P25 (now P21) compares G_BM with Ē_N4, the mean reach over epics. pct_N4 stays in the rule as the percentile it is | 5.4, 8 |
| N11 | minor | `operational_map.json` records the X-class decision: "X1–X4" maps to h_06 ≥ 0.5 or h_tot ≥ 0.5, and X3 and X4 to their smag thresholds under the mixture (fix 1). QS-SACK-06:a is scored at its own day and site (fix 2, its second option) | 6.3.3, 6.5, 10.3 |
| N12 | minor | `events.conjunctions(…, ephemeris=)`, and `sky.build(…, dt_model=float, refraction=)` (fix 1). One Day-0 date per clock in `POOL_DTYPE` (fix 2). A span and a column set for each site in `sites.json` (fix 3). Step 2 is re-estimated at 3–5 h with the star events, and disk at 4–5 GB | 4.1, 4.2, 10.2, 11.2 |
| N13 | minor | The continuous vertex test at ±1.5 d is B&M's integer ±1 and is the primary (T0's primary cell, F5's BM tolerances 1.5/2.5/3.5, regime BM). ±1 is reported, and P3 predicts that the survivor set does not depend on the choice | 3.2, 3.5, 5.3, 6.4, 8 |
| N14 | minor | H3 is one predicate (H3a ∧ H3b) with a joint conditional base rate | 7, 8 |
| N15 | minor | I3 is left out of INSTR (fix 1). I2b names its ΔT and ephemeris on both sides, with a tolerance that allows for the frame difference (fix 2) | 6.1, 9.1 |
| N16 | minor | The re-drafter reads only a generated brief, which holds the conventions, the policies and the cited rows, with no options (fix 1). It reads nothing else in the repository, so §8 and §13–14 are excluded with the rest (fix 2). The test is stated to control file exposure only (fix 3) | 6.1, 6.3.4, 10.1 |
| N17 | minor | Corrected: Ptolemy names Alexandria for his own records and Babylon for the Babylonian eclipses (IV.6.3), which belong to R-PTOL-BAB | 6.4 |

---

## Sources

The dossier, in `docs/`:

- `research-bm2008.md` (with `research-bm2008-a.md` and `-b.md`), the
  reconciled spec of Baikouzis & Magnasco 2008; scripts in
  `results/bm2008-reconcile/`.
- `research-chronology.md`, the day count from the Greek and the 8-row grid.
- `research-textclues.md`, the 76-row clue inventory; scripts in
  `docs/textclues-scripts/`.
- `research-ephemeris.md`, the computation stack (`odybench/ephem.py`,
  `tools/validate_ephem.py`, `results/validate_ephem.txt`).
- `research-visibility.md`, chance rates for each clue reading;
  `docs/research_visibility_calc.py`, `results/research-visibility.json`.
- `research-controls.md`, positive, hard and negative controls;
  `results/controls/`.
- `research-critiques.md`, the responses since Schoch;
  `results/research-critiques/`.
- `research-window.md`, the window, Ithaca's eclipse base rates and window
  scaling; `results/window/jsex/`.
- `critique-design.md`, the adversarial review of revision 1;
  `results/critique-design/`.
- `critique-design-r1.md`, the recheck of revision 2;
  `results/critique-design-r1/`.
- `data-acquisition.md`, the ephemeris extension, NASA elements, stars and
  calendar; `results/data-acquisition/`.
- `controls-real-drafting.md` and `license-check-controls-real.md`, the real
  eclipse controls; `results/controls-real-drafting/`,
  `results/license-check-controls-real/`.
- `controls-almagest.md` and `license-check-almagest.md`, the *Almagest*
  control; `results/controls-almagest/`, `results/license-check-almagest/`.
- `negatives-drafting.md` and `license-check-negatives.md`, the negative
  controls; `results/negatives/`, `results/license-check-negatives/`.
- `research-unread-primaries.md`, on MacDonald, Schoch and Neugebauer,
  Papamarinopoulos, Henriksson and PLSV; `results/unread-primaries/`.
- `DESIGN-v1.md` and `DESIGN-v2.md`, revisions 1 and 2 of this design.

This revision's scratch scripts are in `results/design-revision-r2/`:

- `cp_bounds.py`: pool sizes, interval floors and garden sizes;
- `ranc_season.py`: Arcturus' heliacal rising at −1177 and −1130;
- `synth_sets.py`: the intervals of the synthetic sets;
- `alm_options.txt`: the options of the *Almagest* rows.

Each has its `.out.txt` beside it.

Primary items behind them, as the notes read them:

- **The paper.** Baikouzis & Magnasco, PNAS 105 (2008) 8823–8828,
  doi:10.1073/pnas.0803317105, with its Supporting Information and Table S2
  (`data/bm2008-a/`).
- **Earlier datings and their critics.**
  - Schoch, *The Observatory* 49 (1926) 19–21.
  - MacDonald, *JBAA* 77 (1967) 324–327.
  - Papamarinopoulos et al., *MAA* 12(1) (2012) 117–128.
  - Henriksson, *MAA* 12(1) (2012) 63–76.
  - Neugebauer & Schoch, *AN* 230 (1927) 57.
  - Gainsford, *TAPA* 142 (2012) 1–22 (*secondary* where it reports
    MacDonald).
- **Eclipse canons and ΔT.**
  - Espenak & Meeus, *Five Millennium Canon of Solar Eclipses* (NASA
    TP-2006-214141) and its JavaScript Explorer.
  - NASA's lunar eclipse catalogue (LEcat5).
  - Stephenson, Morrison & Hohenkerk 2016 and the Addendum 2020, with Table
    S10 v2020 (`data/ref/`).
- **Ephemerides and stars.**
  - JPL DE441 and DE431 (Park et al. 2021).
  - van Leeuwen 2007 (the Hipparcos new reduction), ESA 1997, and Bond et
    al. 2017 (Sirius).
- **Other.**
  - The PLSV 3.1 documentation (Lange & Swerdlow).
  - Fay & Feuer, *Statistics in Medicine* 16 (1997) 791–801, for the gamma
    interval (cited from memory, 13 row 37).
- **The ancient texts.** The Odyssey, the Iliad and their scholia; Ptolemy's
  *Syntaxis* (Heiberg); Geminus; Thucydides; Xenophon; Arrian; Plutarch;
  Curtius; Pliny; Livy; Diodorus; Virgil; Apollonius; Quintus Smyrnaeus;
  Valerius Flaccus; Hesiod; and Aratus. All were exported read-only from
  ClassicaCodex into `data/text/`.

The bench designs this one follows are `C:\Projects\labench\README.md` and
`C:\Projects\indusbench\DESIGN.md`.
