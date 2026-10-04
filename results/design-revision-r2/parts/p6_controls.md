## 6. Controls

All clue sets, readings, windows, sites, seeds, regimes and thresholds for
the controls are in `data/prereg/` and are frozen with this document
(section 12) before any control is computed. Truth files are read only by
`odybench/harness.py`, to place windows, to score and to run the exposure
audit (6.3.4). The searcher never reads them, and a static test enforces
this (I13).

### 6.1 Instrument checks

Each check compares a code path with something that does not share its code
[rev #13]. **INSTR** holds when I1, I2, I2b and I4–I14 all pass. I3 is a
calibration with no pass criterion, so it is reported and is not part of
INSTR [r1 N15]. `verdict.py` refuses to run unless INSTR holds.

A check marked "post-freeze" runs first after the freeze. The outputs it
guards are not opened until it passes, and a fix it forces is a dated
amendment (section 12).

| # | what is checked | compared against | pass | when |
|---|---|---|---|---|
| I1 | ephemeris | Horizons; `validate_ephem.py`; `test_ephem.py`; `validate_coverage.py` | 55/55, 10/10, all coverage checks [acq §1.3] | done; rerun pre-freeze |
| I2 | solar-eclipse local circumstances, `eclipses.py` (Python port of NASA's JavaScript, from `results/research-critiques/eclipse_local.py`) | (a) NASA's own `program.js` run in Node: `data/jsex/sites/*.jsonl`, 5 sites × 5,486 eclipses; (b) the review's independent Besselian solver `results/critique-design/check_bessel.py` [rev #13 fix 6] | (a) smag within 0.0005, time of maximum within 0.002 h, Sun altitude within 0.05°, central flag identical; (b) totality windows for 1178, 1131, 1312 and 1183 BC within 5 s | pre-freeze |
| I2b | language-to-magnitude: local smag for the dated eclipses of [ctl §3] | the values printed in [ctl §3], moved to the truth-side file `data/prereg/i2b_reference.json` | **both sides named** [r1 N15]. The bench side is `eclipses.local` on NASA's elements at the element row's canon ΔT (ṅ −25.858). The reference side is Horizons DE441 geometry at NASA's catalogue ΔT, applied by the longitude-shift equivalence [ctl §2.2], which mixes frames by the DE441 − canon offset (about 90 s at −430 [acq §1.3; me: 0.00335″ T³]). Pass: smag within 0.02, or within the change produced by ±100 s of ΔT if that is larger; above 0.95, the central flag agrees | pre-freeze, after the re-draft of 6.3.4 |
| I3 | Hesiod's star calendar at 701 BC, 38.37°N | Hesiod's own numbers | **a calibration, not a validation, and not in INSTR** [rev #20; r1 N15]. The Pleiades' AV is set so that they are hidden 40 days (*WD* 385–386); "Arcturus ≥ 5° at nautical dusk" is read off *WD* 564–567. The phases are validated by I6(c) | pre-freeze |
| I4 | lunar eclipses, `lunar.py` | NASA LEcat5 rows: every lunar eclipse in the PC-R and ALM truth centuries, and 300 drawn at random from −1999..+300 | type identical; umag and pmag within 0.02; greatest eclipse within 3 min after removing the ΔT difference | pre-freeze |
| I5 | rise, set and transit, `sky.py` | (a) JPL Horizons rise/transit/set output for 1,000 random events (Sun, Moon, Venus, Mercury, Jupiter, Sirius, Arcturus; Ithaki, Alexandria, Troy; −1999..+300; same h0, airless); (b) the dense-grid-plus-bisection rise finder of `results/critique-design/check_mwra.py`, on 2,000 events | (a) within 0.5 min after removing the documented sidereal-time convention difference (5 s at −1999 [acq §1.3]); (b) within 0.1 s | pre-freeze |
| I6 | derived events, `events.py` | (a) the event lists of `results/bm2008-reconcile/check_mwra.py` (rise-azimuth maxima and minima, stations, GWE, inferior conjunction) for all 152 S2 years; (b) the low-precision Standish-element code `results/bm2008-b-checks/ephem.py`, 500 random stations and greatest elongations; (c) heliacal star phases and B&M's spring limits from `docs/research_visibility_calc.py` (its own spherical astronomy and Meeus' solar theory) at −1177 and −700; Arcturus' heliacal rising at −1177 and −1130 against `results/design-revision-r2/ranc_season.py` | (a) same UT+2 civil date in ≥ 150 of 152, vertex instants within 0.05 d; (b) within 1 d; (c) within 1 d | pre-freeze |
| I7 | B&M's reading through `clues.py`, `readings.py` and `search.py` | `tests/bm_reference.py`, a minimal second implementation written by a different agent from section 3.2's text alone, using only `ephem.altaz` and its own rise bisection [rev #13 fix 4] | identical pass flags (N, C, V, M, E and every T0 grid cell) for every candidate in 1250–1115 BC and in 300 random background years | post-freeze, before any T0 output is read |
| I8 | calendar | `tests/test_calendar.py` | 11/11 [acq §4] | done |
| I9 | reach, G and the pools | (a) a brute-force implementation that slides windows in 0.01-year steps, on 10,000 random synthetic survivor sets; (b) the coverage of the G interval of 5.3, on 10,000 synthetic reach vectors drawn at n = 100, 139 and 903 with true G from 0.001 to 0.3; (c) the identity G(𝒢_BM*, T) = (n_A/n_T) G(𝒢_BM*, T_A) on the real tables | (a) reach equal within 0.0002; (b) coverage of G_hi ≥ 0.95 and of G_lo ≥ 0.95 at every cell; (c) exact to float rounding | pre-freeze (c: post-freeze, first) |
| I10 | PC-S instrument mode (6.2) | descriptions generated by an independent code path | recall 1.000 | post-freeze, before PC-S science outputs are read |
| I10b | the exact R_obs of 5.7 | R_obs simulated end-to-end in PC-S science mode (generator and searcher, 2,000 truths per noise cell) | agreement within the simulation's 95% interval in every noise cell | post-freeze |
| I11 | plumbing negatives (revision 1's NC4 and NC5 [rev #15 fix 4]) | (a) AEN-TROY's pinned R-ii-literal reading, conjunction on Day 0 with the Moon up after nightfall, which contradicts itself [neg §3.1]; (b) a synthetic set with Day 0 a conjunction and the Moon above the horizon at local midnight; (c) Hesiod's star calendar (*WD* 383–385, 564–567, 609–611, 615–621) as event clues around an arbitrary Day 0 | (a), (b) zero survivors in every window (a is known to hold at Troy in two windows, 2.6); (c) no unique survivor in any 136-year window | post-freeze |
| I12 | first-crescent evening | the Yallop implementation in `docs/research_visibility_calc.py`, 500 lunations | same evening in ≥ 495 | pre-freeze |
| I13 | prereg I/O | (a) every licence string present in its cited row: the licence checkers' dump scripts are rerun, comparing raw characters without Unicode normalisation, because the Ptolemy export mixes tonos and oxia and prints the half-sign as the literal "U+2220" [lca next-stage item 7; pcr §5]; (b) every fork option of every row translates to a canonical predicate (10.3), with exactly one primary per controls row; (c) no module but `harness.py` and `tools/build_truth_index.py` opens a `*_truth*` path or contains the Nabonassar epoch; (d) `operational_map.json` is reviewed by a second agent; (e) the re-draft brief of 6.3.4 contains no statement, option name or justification string of `controls_real.json`, and exactly the five briefed rows; (f) `almagest_regimes.json` and `deltat_circular.json` parse, and every value they name exists in the clue files | all pass | pre-freeze |
| I14 | the decision rule | (a) the synthetic input sets of 9.5; (b) the structural constraints of 9.4 | (a) each returns its stated labels and qualifiers; (b) every synthetic set satisfies every structural constraint, so that what is proved reachable is an outcome and not a code branch [r1 N1 fix 3] | pre-freeze |

Revision 1's NC4 (the Hymn to Hermes) is dropped: it misread *h.Herm.* 141,
where παννύχιος closes Hermes' clause [rev #15].

### 6.2 PC-S: synthetic Odyssey-shaped clue sets

Revision 1's PC-S generated its clue sets with the same code it searched
with, and with a different grammar, so its "recall ≥ 0.99 or it is a bug"
was either built to fail or tautological [rev #14]. Revision 2 split it into
two modes. It also let one science-mode number, rec_PCS, into gate 3b. The
recheck showed that number to be definitional (about 0.68, because generator
and searcher share slot rules) [r1 N2], so **PC-S no longer enters any gate
or rule.**

**Truth pools** (seeded):

- (i) 2,000 daylight conjunctions drawn from T;
- (ii) every conjunction with h_tot ≥ 0.1 at any Ionian site;
- (iii) the targets of T_A.

**Instrument mode (I10).**

- **Generator.** Generator and searcher share B&M's grammar. For 200 truths
  from pool (i), the generator computes each truth's statements by an
  independent path: the Standish low-precision planetary code of
  `results/bm2008-b-checks/`, with its own rise bisection, for all 200, and
  Horizons for a 50-truth subsample.
- **Margins.** Statements are emitted with margins that hold under either
  ephemeris:
  - the lead threshold is the true lead minus 5 min, rounded down to 5 min;
  - the Mercury tolerance is \|Δ\| + 1 d, rounded up;
  - a season statement is made only if the truth lies at least 2 d inside
    its C_rel bounds.
- **Search.** The searcher is the bench's machinery with those parameters,
  on a window around the truth.
- **Pass: recall = 1.000.** A miss is a shared-code or conversion bug, found
  before any science number is read.

**Science mode: the noise study.** For each truth of pool (iii) and each
cell of the noise grid ν:

- **The noise grid.** Offset jitter j ∈ {0, 1, 2, 3} days applies
  independently to every clue offset. A displacement s_M ∈ {0, 3, 6} days
  moves Mercury's turning point from the stated day. There is no Venus
  slack: the *Almagest*'s 16–21-day Venus slack was measured on
  greatest-elongation records, while B&M's Venus clue is a rise-lead
  threshold that every *Almagest* Venus morning record passes with a large
  margin [alm §0 item 7, §5 item 3]. ν_real = (j = 1, s_M = 3).
- **The generator emits B&M-event statements** of the truth's own sky:
  - the Venus lead, rounded down to 5 min;
  - the nearest morning Mercury event, with its kind and offset;
  - the season class of the raft nights.

  All are stated at the stated offsets plus the noise.
- **The searcher applies every reading of 𝒢_BM*** and the DOC tolerance forks.

Recorded:

- recall and P(unique) of each reading, as curves over ν;
- **ρ_r(ν)**, the recall of reading r among the truths whose zero-noise sky
  passes r. It enters only BF_BM (5.7);
- the decay of reach and recall as the typical-number jitter grows from 0 to
  ±3 d [rev #8 fix 2–3];
- the generator's description of each truth's sky, to show which readings
  succeed and why.

There is no "bug" threshold in science mode. I10b checks the end-to-end
simulation of R_obs against its exact reweighting (5.7).

### 6.3 PC-R: real eclipse records with independently known dates (gate 3a)

**The clue file** is `data/prereg/controls_real.json` exactly as licensed
(SHA-256 `135fba67…83f8` [lcr]). The searcher reads only its operational
fields. Re-drafted rows are used only to measure exposure (6.3.4). Nine
sets:

| set | text | role |
|---|---|---|
| R-PTOL-BAB | *Almagest* IV.6, three Babylonian lunar eclipses | counted |
| R-PTOL-ALEX | *Almagest* IV.6, three Alexandrian lunar eclipses | counted |
| R-PTOL-CHAIN | the two triples joined by IV.7.1 (E2 to H2: 311,784 nights) | reported; it contains BAB and ALEX |
| R-THUC | Thucydides 2.28, 4.52, 7.50 | counted |
| R-XEN | *Hellenica* 1.6.1, 2.3.4 (linked); 4.3.10 (unlinked) | counted (the linked group) |
| R-ARBELA | Plutarch, Arrian, Curtius, Pliny on one lunar eclipse | counted |
| R-PYDNA | Livy 44.36–37; Plutarch *Aem.* 16–17 | counted |
| R-DIOD | Diodorus 20.5.5 | counted |
| H-LIVY | four prodigy notices | hard case, reported, not pass/fail [rev #2 fix 4] |

#### 6.3.1 The search

The harness reads the truth through `data/prereg/truth_index.json`, which
`tools/build_truth_index.py` builds from the two truth files. It places a
136-year window with the anchor event at a uniformly random position (seed
per set). It passes the searcher only the clue set, the window bounds and
the event catalogues.

- **Candidates** are every event of the anchor's kind in the window: solar
  eclipses from NASA's elements, and lunar eclipses (umbral and penumbral)
  from `lunar.py`.
- **Linked events** are found through the interval rows: exact night counts,
  war-years ± tolerance, year headings 1–3. For each anchor candidate, the
  linked event that fails fewest rows is taken. Unlinked events (R-XEN's X3,
  the H-LIVY notices) are separate searches, reported and not counted.
- **Calendars** follow the file's conventions:
  - Egyptian dates have a free epoch (intervals only);
  - Roman dates have a free offset (primary), with ±90 d and "naive" as
    reported alternatives that are never readings of the text;
  - Attic months go through the modern reconstruction with ±1 lunation. This
    is the one primary that rests on a calendar outside the text [lcr
    flagged item 1].
- **Sites**: a point; a box (the row passes if some site in the box
  satisfies it); a disc; or none. "None" means some site on Earth: for solar
  eclipses a 1° grid refined near the best point, and for lunar eclipses the
  Moon above the horizon somewhere.
- **ΔT**: the four-model mixture (6.3.3).

#### 6.3.2 Scoring and the gate

**Scoring** [pcr §5 problem 1; truth-file note]. For a reading, f(c) is the
number of clue rows that candidate c fails. Rows without options are
structural: they define the events and dates.

- **Strict survivors** S₀ = {c : f(c) = 0}: B&M's all-must-pass rule.
- **Best-fit set** B = {c : f(c) = min f}: the dates the record points to,
  allowing for errors in the record.
- **Seen** := the truth is in B, and \|B\| ≤ 0.05 × N_cand, where N_cand is
  the number of candidates in the window. The method keeps the true date
  while narrowing the window at least 20-fold (4.3 bits). Uniqueness is not
  required, because a weak record cannot be unique however good the method
  is. The gate asks whether the method loses the truth, and that is the
  failure "cannot see" names.
- **Resolution** := the number of clusters in B, where candidates within 3
  days of each other count as one cluster (this matters only for day-unit
  candidates in 6.4). **Unique** := one cluster.
- **Strict recall** := f(truth) = 0.

The **primary run** puts every row at its primary option. Also reported for
every set:

- f(truth), \|S₀\|, \|B\| and the truth's rank;
- the same with each row moved, one at a time, to each alternative;
- the fraction of readings that make the truth the unique strict survivor,
  over all fork combinations (sampled to 10,000 where there are more);
- as a sensitivity, the fraction of twenty further window positions per set
  in which the set is seen.

**The gate.** seen_PCR is the number of the 7 counted sets seen in the
primary run, and strict_PCR the number with strict recall.

- **3a fires if seen_PCR < 4** (fewer than half, rounded up).
- **Q_strict holds if strict_PCR < 4.**

The best-fit rule was chosen after the drafter's post-freeze check had
shown that the true dates fail some primary readings under a rough lunar
model (2.6). That choice is therefore not blind, and the strict count is
always reported beside it as Q_strict.

#### 6.3.3 ΔT for the controls, and the controls that helped fit it

**Every ΔT-dependent row is scored under the four-model mixture** of section
0 [r1 N4 fix 1]. This applies to solar smag, the LAT of maximum, the
contacts and the Sun's altitude, and to lunar contacts, seasonal hours and
the Moon's altitude.

- **Frames.** Solar rows use NASA's elements in the canon frame, each
  model's value converted to it. Lunar rows use DE431, each model converted
  to the DE431 frame.
- **Pass rule.** A row passes for a candidate if
  P_mix(row passes) ≥ 0.5. The probability is integrated over a 41-point
  ΔT grid spanning ±4σ of each model, weighting each model's Gaussian
  equally.
- **Mapping of the X classes.** The controls file's "X3 ≥ 0.95" and
  "X4 ≥ 0.60" become P_mix(smag ≥ 0.95) ≥ 0.5 and P_mix(smag ≥ 0.60 with
  the Sun ≥ 10° at maximum) ≥ 0.5 at the row's site rule (10.3).
- **Sensitivities.** Reported at thresholds of 0.05 and 0.95.

**Circular controls** [r1 N4 fix 2–4]. Some control eclipses entered the
data that fitted the ΔT models (2.6):

- R-DIOD (−309, Table S10 v2020);
- H-LIVY's L4 (−187, same table);
- R-THUC's T1 (431 BC) and R-XEN's X3 (394 BC), per SMH2016 §2b(iv)
  (*secondary*).

**A pre-freeze task** reads SMH2016's Table S4 and §4b and the 2020
Addendum's tables. It lists every control eclipse used in any fit, and
whether the *Almagest* timings are among them, in
`data/prereg/deltat_circular.json` with page locators (12.1).

**seen_PCR,noncirc** is the gate count with each circular set's ΔT-dependent
rows rescored under the mixture with every model's σ multiplied by 3. A
model fitted to a record cannot then constrain that record much.

- **Q_ΔT holds** if seen_PCR,noncirc falls on the other side of 4 from
  seen_PCR.
- Gate 3a is also reported with the circular sets removed, the threshold
  then being half the remaining counted sets, rounded up. That count is
  reported only.

The S10 interval for −309 is 3,860 s wide, so R-DIOD's pass is probably
robust. Q_ΔT tests that rather than assuming it.

#### 6.3.4 The drafter's exposure

The drafter had seen computed answers and flags three primaries as possibly
steered: T1-DARK, D-ECL and the ±1 h tolerance in L4-DARK [pcr §1]. The
recheck adds T2-SEASON, whose primary alone admits the truth, and
T-INT-12's ±0.5-year tolerance [r1 N5]. The gate uses `controls_real.json`
exactly as licensed. The exposure is measured beside the gate, two ways,
rather than edited away.

1. **An unexposed re-draft of the five rows** [r1 N5 fix 1; N16].
   - **The brief.** `tools/make_redraft_brief.py` (written by A3, who does
     not read truth files) writes `data/prereg/pcr_redraft_brief.json`. It
     holds:
     - the file-level conventions and policies of `controls_real.json`;
     - for each of T1-DARK, T2-SEASON, T-INT-12, D-ECL and L4-DARK, its set,
       its feature kind and its cited text rows, in full.

     It holds no statement, option, justification, note or licence-check
     field. I13(e) checks this.
   - **The re-drafter.** An agent that has read nothing else in the
     repository (no `DESIGN.md`, `docs/`, `results/`, `data/ref*`, and no
     other `data/prereg/` file) drafts the five rows from the brief alone,
     into `data/prereg/pcr_redraft.json`.
   - **seen_PCR,redraft** is the gate count with the re-drafted primaries in
     place of the drafter's.
2. **A sibling-convention audit** [r1 N5 fix 2–3]. It runs post-freeze, in
   `controls.py`, because it reads the truth.
   - Rows of the counted sets are grouped by feature kind (season, site,
     darkness or magnitude, time, interval tolerance) and by operational
     type.
   - For every row whose primary passes the truth, each sibling's primary
     parameters are transplanted into the row wherever the operational keys
     match. An example is T1-SEASON's [0°, 180°] into T2-SEASON.
   - Every row that some sibling convention makes fail is listed in
     `results/pcr/exposure_audit.json`.
   - **seen_PCR,sibling** is the gate count with each listed row at its
     failing sibling convention, all at once.

**Q_exposure holds** if seen_PCR,redraft or seen_PCR,sibling falls on the
other side of 4 from seen_PCR.

**What this controls, and what it does not.** It controls exposure to
files. It does not remove a language-model drafter's background knowledge
of famous dates (the eclipse of 424 BC is among the best known), and no
re-draft by such an agent can [r1 N5 fix 4]. As the recheck noted, a re-draft
of L4-DARK cannot move the gate, because H-LIVY is not counted. R-THUC is
expected unseen in any case, because its site primaries are "none". So
Q_exposure turns in practice on D-ECL and on what the audit finds.

#### 6.3.5 Decisions on the points the licence check left open

- **Unstated sites stay "none" in the primary run** [lcr Consequences]. The
  Odyssey's observer is placed by its narrative (Theoclymenus in Odysseus'
  hall), so the asymmetry with Thucydides 2.28 is real. A rule that "a
  historian's undated notice places its observer in the region of the
  narrative" would be the inference the file's policy 2 excludes. The box
  and point options are reported as the first alternatives, so the cost of
  the rule is visible.
- **IV.6.14 is counted once.** It is H2 of R-PTOL-ALEX (gate 3a), so ALM-C,
  which contains it, is excluded from gate 3b [alm §3].
- **R-PTOL-CHAIN** uses IV.7.1, the chapter after IV.6. It is reported and
  not counted, so the gate does not depend on that choice [pcr problems].
- **"naive" Roman options** are sensitivity runs only, and are never
  reported as readings [lcr flagged item 2].
- **Pliny's "apud Arbilam"** may name the battle rather than the site, so
  the Tigris-camp alternative is reported [lcr flagged item 4].
- **H-LIVY has no year links** between its notices, so each is searched
  alone [pcr §3].

### 6.4 The *Almagest* control: real records of B&M's own clue types (gate 3b)

B&M's search uses no eclipse. Its clues are a lunar phase, a star season, a
morning star and a Mercury turning point, and revision 1's "method can see"
gate contained none of these [rev #3].

**The clue file** is `data/prereg/controls_almagest.json` as licence-checked
[lca]. It holds 12 sets of dated records: Mercury and Venus elongations,
planet–star and planet–Moon relations, lunar phases, a lunar eclipse and an
equinox. The day intervals come from Ptolemy's own Egyptian dates, and the
date words themselves are withheld.

**Counted sets** are ALM-A, B and D–L (11). ALM-C is reported only (6.3.5).

**Windows** are 136 years, B&M's width. The harness draws a uniformly random
position for the anchor record's true date (seed per set), as in 6.3.1, and
twenty further positions are a sensitivity. The truth file
`controls_almagest_truth.json` is read only through `truth_index.json`.

**Candidates** are every civil day in the window as Day 0 (LMT at the
default site), with each row at its stated day offset. Each row is evaluated
at the drafter's instant convention: "evening" and "dawn" are the moments
the Sun is 8° below the horizon, and stated hours are local apparent time
[alm §1.5]. The convention moves continuous offsets by about ±0.1 d. The
two textual cruxes (A.6 and H.3) run at their primary, as printed, and the
emended intervals are reported. ΔT is the mixture, as in 6.3.3.

**The two Ptolemy files treat Egyptian dates differently.** This file
withholds them, while `controls_real.json` carries them with a free epoch
[alm §3; pcr §2]. Both are kept. With the epoch free, an Egyptian date fixes
only intervals, so the two are equivalent for the searcher, provided that
no bench code supplies the Nabonassar epoch (JD 1448638). I13 checks
statically that the number appears only in the truth files and the harness.
The `ref` of every *Almagest* row points at a text row that contains the
withheld date, so the searcher reads only the operational fields and never
the text at `ref` [lca item 6].

**Default site.** Horizon-dependent rows are evaluated at Alexandria,
31.20°N 29.92°E. That is the observing place Ptolemy names for his own
records (4.6.13, 9.10.3, 11.2.2). The *Almagest* also names Babylon, for the
Babylonian eclipses of IV.6.3 [r1 N17], but those are in R-PTOL-BAB, not in
the B&M-type sets. For sets whose rows leave the observer unstated the site
is an inference, flagged as such [lca item 5]. Babylon is a sensitivity for
ALM-K.

**The B&M-type projection.** The gate uses only rows of B&M's kinds:

- interval rows;
- moon-phase rows, phase-class options only;
- planet rows about greatest elongation, before or after greatest
  elongation, visibility, rise lead and the rising-azimuth proxy;
- the equinox row.

Star rows, planet–star and planet–Moon positional options, oppositions and
the eclipse row are set to none, because they are not in B&M's grammar. The
full primary run is reported beside.

**Two regimes, frozen in `data/prereg/almagest_regimes.json`** [r1 N2 fix 4;
N3 fix]. The licence-checked clue file stays byte for byte as it is (its
SHA-256 is recorded in 12.4). The regime file names, for every row of the
projection, the option and the parameter values each regime uses. I13(f)
checks that every named option exists.

| | regime SL (observer slack, leave-one-set-out) | regime BM (B&M's method as written) |
|---|---|---|
| option | the row's primary | B&M's own proxy where the row offers it (`bm_mwra_k`, `bm_venus_lead`); else, for a greatest-elongation row, `ge_true_k`; else the row's primary [r1 N3 fix] |
| Mercury and Venus greatest-elongation k | **leave-one-set-out**: the smallest value of the row's own list at or above the largest \|record − true greatest elongation\| (true Sun) among the records of that body *outside* the set, from alm Table 2 (records in no set included) [r1 N2 fix 1] | 1.5 d, B&M's ±1 integer day as a continuous tolerance [r1 N13]; 1 d reported |
| `bm_mwra_k` | — (not primary anywhere) | 1.5 d |
| `bm_venus_lead`, minimum lead | — | 90 min |
| opposition k (full run only) | leave-one-set-out over the oppositions in no set: listed value ≥ 0.42 d (mean Sun) = 1 d | middle value |
| every other list (j_days, tolerance_deg, tolerance_days, time_tol_h, minimum minutes, minimum altitude) | most lenient value | middle value (lower middle for an even count) |

Under leave-one-set-out, no set is scored with a tolerance taken from its
own records. **Gate 3b is therefore scored on held-out sets only** [r1 N2
fix 2]. The same records also calibrate the 6-d DOC option of F5 and the
Mercury slot of T_A (5.3), but those serve the Odyssey's garden. Neither
validates the method, so the training-and-testing overlap the recheck
found is broken [r1 N2]. Scoring follows 6.3.2: best-fit; seen := the truth
is in B and \|B\| ≤ 0.05 N_cand, N_cand being the days in the window.
Resolution and uniqueness are reported.

**The gate.**

- seen_ALM_SL is the number of the 11 counted sets seen in regime SL
  (projection, best-fit).
- rec_ALM_BM is the number with strict recall and \|S₀\| ≤ 0.05 N_cand in
  regime BM (projection, strict).
- **3b fires if seen_ALM_SL < 6** (fewer than half of 11, rounded up).
  PC-S no longer enters the gate [r1 N2 fix 3].
- **Q_BM holds if rec_ALM_BM < 6**: "B&M's tolerances cannot recover expert
  planetary records" [rev #3 fix 3]. It conditions every "no" about the
  Odyssey. It blocks outcome 1 unless G_DOC,hi ≤ 0.05 too (section 9).

**What is already known.** Under these frozen rules the truth-side slack
already decides much (2.6):

- truth is retained in 9 of 11 sets in regime SL, with ALM-G and ALM-H
  failing, and only narrowing remains open (P35);
- rec_ALM_BM is at most 5, so **Q_BM holds**, and the bench recomputes it as
  a regression check.

The harness must implement two pieces of new vocabulary: the bound
`same_apparition`, and ALM-F.4's `star_candidates`, with one garden branch
per candidate [lca].

### 6.5 Negative controls (outcome 4)

**The clue file** is `data/prereg/negatives.json` as licence-checked [lcn].
It holds 12 clean negatives (Virgil, Apollonius, Quintus Smyrnaeus, Valerius
Flaccus) and the Iliad as a same-tradition comparison [rev #15 fix 1–2; neg
§1]. Each clean negative is fiction or legend composed long after the events
it tells, drafted under the Odyssey's own selection rules, with no similes
and no lying tales. Its `operational` fields are prose, so each option is
translated into a canonical predicate in `data/prereg/operational_map.json`
before the freeze, and a second agent checks each translation against its
prose.

**Pre-freeze decisions and second reading** [neg §6; lcn §4]:

- **Counts and caps.** A second reader checks the interval forks and caps
  that rest on the drafter's own counts: ARG-CIUS n16/n17/n18, ARG-COLCHIS
  a3/a4, IL h12/h13/h15, VF-LEMNOS-01, and the caps free30, xfree, w60 and
  QS-SACK-06's 10 d.
- **"literal" means least inference.** Pinned literal readings that use an
  inferred or drafter-width option (AEN-CRETE-01 a60, ARG-RETURN-03 x0,
  ARG-COLCHIS-02 a3) are re-pinned by the second reader to the
  least-inference option of their row.
- **QS-SACK-03.** Its BM-analogue pin keeps option b in its new meaning (the
  Pleiades over the dark hours), and b-late stays in the garden.
- **Places and thresholds.** The same reader checks the place
  identifications against a gazetteer (Pleiades). In `operational_map.json`
  the reader flags the numeric thresholds that are the drafter's
  operationalisations [lcn §4.3; 13 rows 34–35].
- **The withdrawn eclipse classes** [r1 N11]. Several rows still cite
  revision 1's classes:
  - QS-SACK-06:a and IL-PATROCLUS-02's solar_am and solar_any require "a
    solar eclipse of class X1–X4 (DESIGN 3.1)";
  - `controls_real.json` cites "X3 ≥ 0.95, X4 ≥ 0.60".

  `operational_map.json` records one decision for all of them. "Class
  X1–X4" means X2 ∪ X3 ∪ X4 under revision 1's own definitions [v1 §3.1].
  In the bench's probabilistic terms that is h_06 ≥ 0.5 or h_tot ≥ 0.5 at
  the option's site and day. X3 and X4 alone map as in 6.3.3.

**Windows.** Each clean negative is searched in the Odyssey's own two
windows (reproduction, 136 years; primary, 251 years) at its own site. The
negatives tell events of the same legendary age, and these windows give
fiction exactly the chances the Odyssey had. Twenty further random positions
per width are a sensitivity.

**Gardens.** 𝒢_j is the full product of set j's fork options, with each F5
entry expanded into its tolerance and visibility variants [neg §1 item 6].
Its eclipse-compatible readings are those that contain a solar-eclipse or
Day-0-conjunction option listed in the set's `eclipse_compatible_options`.
Lunar-eclipse options are not solar eclipses and are excluded, as the file
says. The negatives' readings were drafted without any target, so their G
needs no conditioning (5.3).

**The test** [rev #1 fix 3]:

- **hit_j** holds when some eclipse-compatible reading of 𝒢_j has, in one of
  the two windows, a unique Day-0 survivor whose eclipse has h_tot ≥ M_Ody.
  Each option is evaluated at **its own day and its own site** [r1 N11 fix
  2]:
  - for a Day-0 option, at the set's first `observer_places` entry;
  - for QS-SACK-06:a, near Cape Caphereus on Day +2..+12 after the unique
    Day-0 survivor.
- **G_j** is the mean reach_136, under 𝒢_j, over all daylight conjunctions
  at the set's site in the core. Its interval is the gamma interval of 5.3.
- **Outcome 4 fires if some clean negative has hit_j and G_j,hi ≤ G_BM,u.**
  G_BM,u is the Odyssey's G under 𝒢_BM* over T, the same kind of
  unconditioned target set. It is the Odyssey's coincidence as B&M would
  present it, with every reading treated as blind, so the comparison
  favours B&M twice: 𝒢_j holds more readings than 𝒢_BM*, and the negative is
  taken at its upper bound.

Also reported per set:

- the survivors of each pinned reading (literal and BM-analogue; R-i, R-ii
  and R-ii-literal for AEN-TROY);
- survivors per century;
- the slot matrix of [neg §5].

**The Iliad** (IL-PATROCLUS) gets the same computations. It is reported as
the same-tradition comparison and is not used in the rule. Two consistency
checks run beside it:

- **Iliad against Odyssey.** If both carry real dates, the Iliad's (the
  tenth year of the war) must fall about 8–12 years before the Odyssey's
  (the return in the twentieth year [win §5]). For the pinned BM-analogue
  readings the bench reports the offset and its base rate: the chance that
  an unrelated survivor falls in a given 5-year band.
- **Cross-text competition.** The bench counts how many texts and readings
  the gardens attach to each eclipse with h_tot ≥ 0.1. 30 Oct 1207 BC and 30
  Sep 1131 BC have also been claimed for Joshua 10 [crit §0 item 7,
  *secondary*]. Joshua is outside the grammar and is not run.

---

