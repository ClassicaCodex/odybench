# odybench — design (revision 5)

A test bench for the claim that the sky clues in the Odyssey date the
slaughter of the suitors to 16 April 1178 BC. It is the fourth in the series
after vbench (Voynich), [labench](../labench/README.md) (Linear A) and
[indusbench](../indusbench/DESIGN.md) (Indus script), and it keeps their rule:
every test is run first on cases whose answer is known, so that a "no" about
the Odyssey means something.

Revision 5, written 2026-10-04. Revisions 1–4 are kept unchanged as
`docs/DESIGN-v1.md` to `docs/DESIGN-v4.md`.

**Why a fifth revision.** The redesign workflow was run a second time ("Try
again"). Its preparation stage re-ran two licence checks: a second
independent check of the *Almagest* control and one of the negatives. Both
changed their clue files after revision 4 was written. Revision 5 starts from
revision 4, translates those checks, and reviews revision 4 itself, which no
recheck had seen. Section 14 lists every issue with its resolution:

- **14.1:** the 25 issues of `docs/critique-design.md`, the review of revision
  1 (3 blockers, 15 major, 7 minor);
- **14.2:** N1–N17 of the recheck of revision 2, one a blocker;
- **14.3:** R2-1 to R2-12 of the recheck of revision 3, one a blocker:
  outcome 1 could not be reached for any data;
- **14.4:** issues 55–66, found by this revision in revision 4 and in the
  round-2 licence checks.

**What revision 5 changes.**

- **The held-out test is matched to the readings the target passes** (7.2).
  - Revision 4 compared 1178 BC with every candidate that passes some reading
    of 𝒢_BM*.
  - The target passes only B&M's applied Mercury event, the rise-azimuth
    maximum (MWRA). A candidate admitted through a greatest elongation or a
    station had Mercury at another point of its cycle on Day −34, and so
    possibly in another phase on Day 0, which is what the held-out clue H3
    is about.
  - The test now runs on two pools: P_BM as before, and P_MWRA, the
    candidates that pass an MWRA reading. The rule reads the **larger** of
    the two exact p-values, which stays valid if either pool is exchangeable
    with the target. The design-stage floor stays 0.026 (2.9).
- **The round-2 licence checks are translated** (6.4, 6.5, 12.4).
  - *Almagest:* the gate's lunar phases now come from words only; the
    before-or-after-elongation rows use their literal, unbounded options; the
    held-out rows of every set are named row by row; three counted sets
    have none, so held_ALM can be at most 8.
  - *Negatives:* the new Day-0 solar-eclipse reading of ARG-RETURN, AEN-TROY's
    reading R-iii, Ida as a landmark, and a dependence between two
    ARG-COLCHIS rows. A darkness the text attributes to a storm is weather,
    for fiction and for the Odyssey alike, so QS-SACK-06:a leaves the rule.
- **Truth-side facts move into Appendix T,** and the agents who translate or
  search the control files work from a copy of this design without it
  (10.1, I13(h)). Revision 4's refusal pattern `*_truth*` did not match its
  own `truth_index.json`. Every truth-side file now has "truth" in its name,
  and the pattern is `*truth*`.
- **Provenance.** Tags that pointed at reports since overwritten are
  repaired, and byte copies of the two rechecks are kept, because a re-run of
  the review loop reuses their file names (section 0).
- **One prediction withdrawn.** P4, the rate with the equinox clue against
  B&M's printed figure, expects about two survivors over the whole
  background, so Poisson noise would decide it; it is now a reported
  comparison (2.4, 8).

Revision 4's own summary follows, because every one of its changes stands.

Revision 4 answered the first three reviews. Its main changes were these:

- **"Yes" now rests on evidence formed blind to the target.** Outcome 1 reads
  the held-out clues of section 7: Hermes leading the suitors' souls, and
  Ares caught with Aphrodite. They are scored by an exact rank test against
  the candidates that B&M's own readings accept (revision 5 adds a second,
  matched pool). Whether that test could give p ≤ 0.05 is a null-side
  number. It is computed before any target-side number, and at the design
  stage it is about 0.026 (2.9).
- **B&M's own match is judged separately.** Label 2 says when it carries no
  weight. The qualifier Q_tol says in every verdict when B&M's readings could
  not have dated any target at 5% (2.10). That is expected, since G_BM is
  about 0.14.
- **The freeze has two stages.** Code, design and thresholds are committed
  before any null, control or held-out result. The null-side quantities (pool
  sizes, G, the held-out null) are then computed with the target masked, and
  committed before any target-side number (12).
- **The slots that define the conditioned pool form a frozen family** of six
  definitions. A G-based decision fires only if it fires under all six (4.2,
  9).
- **Smaller changes:**
  - label 2 has a "no match" form, and ties never decide it (5.4);
  - INSTR holds only the checks that guard rule inputs, each with a tie band
    (6.1);
  - `smag` is NASA's magnitude exactly (0);
  - leave-one-set-out tolerances are ceilings of the measured slack, not
    values from the drafter's grid (6.4);
  - sibling-convention transplants are restricted (6.3.4);
  - R_anc's four season bounds are reported alike (5.3);
  - a reading whose eclipse is not on Day 0 is mapped to its eclipse (6.5);
  - G's interval allows for clustered targets (5.3).

**Status.**
- **Built and validated:** `odybench/ephem.py`, `odybench/ccx.py`,
  `odybench/calendar.py` and the data in section 2.1.
- **Drafted and licence-checked, not frozen:**
  `data/prereg/controls_real.json` (one check), `controls_almagest.json`
  (two checks) and `negatives.json` (two checks). Their current hashes are in
  12.4.
- **Not yet built:** any other bench code.
- **Not yet run:** any null model, control search or held-out check.
- **Computed for revisions 4 and 5:** design-stage estimates of null-side
  quantities only. The target was removed before any computation (2.9).
- **Freezing:** everything in sections 3–9 is frozen in a local git commit
  before any of them runs (section 12).

Section 2 lists what is already known, including what the known numbers imply
for the verdict. Section 8 lists, with thresholds, only what needs new runs.

---

## 0. Conventions and tags

- **Years.** Historical BC with the astronomical year after it: 1178 BC
  (−1177).
- **Calendar.** Proleptic Julian throughout. 16 Apr 1178 BC is JD 1291263.5
  at 0 h, and 5 Apr in the proleptic Gregorian calendar [acq §4]. **All
  calendar arithmetic goes through `odybench.calendar`** (exact integer JDN
  arithmetic; half-open day and span bounds; UT+2, LMT and LAT civil dates).
  Python `datetime` and numpy `datetime64` are banned from `odybench/`,
  `tools/`, `tests/` and the top-level scripts; `tests/test_calendar.py`
  enforces the ban [acq §4]. Modules inside the package are run as
  `py -m odybench.x`, never `py odybench/x.py`, because the file would then
  shadow the standard library's `calendar` [acq §4].
- **Time scales.** TT (= TD of the eclipse canons); UT = UT1; ΔT = TT − UT.
  UT+2 is zone time on 30°E, the clock Baikouzis & Magnasco used [bm §3.2].
  LMT is local mean time (UT + longitude/15). LAT is local apparent solar
  time. "Hour n of the day (night)" is a seasonal hour, one twelfth of
  sunrise–sunset (sunset–sunrise); Ptolemy's hours are equinoctial hours of
  LAT [pcr §2]. Every clock time below names its scale.
- **Epoch.** The argument of every ΔT model is the Julian epoch of the TT
  instant, `calendar.julian_epoch(JD_TT) = 2000 + (JD_TT − 2451545)/365.25`,
  identical to `ephem.julian_epoch` [acq §4]. 16 Apr −1177 is epoch
  **−1176.68**. Revision 1 labelled its ΔT values "−1177.29", which was wrong
  [rev #22].
- **Days.** A civil day runs from local midnight to midnight (LMT at the
  site) unless a rule names UT+2. Day n is the civil date of the daylight of
  that day; Night n runs from sunset of Day n to sunrise of Day n+1; Dawn n+1
  is the morning twilight that ends Night n [neg conventions]. T0b and fork
  option F2 (a) use UT+2 civil dates, as B&M did.
- **Sites.** One table, `data/prereg/sites.json`, used by every module:

  | key | place | lat, lon (deg, E +) | role | source |
  |---|---|---|---|---|
  | `ithaki` | Ithaki (Vathy) | 38.37, 20.72 | primary Odyssey site | the coordinates that reproduce the NASA site catalogue [acq §2.2]; Vathy 38.367, 20.717 differs by 0.3 km |
  | `bm` | B&M's fitted site | 38.4, 20.7 | T0b only | the S2 clock fit [bm §3.2] |
  | `kefalonia` | Argostoli | 38.18, 20.49 | sensitivity | [acq §2.2] |
  | `lefkada` | Lefkada town | 38.83, 20.70 | sensitivity | [acq §2.2]. research-ephemeris used 20.71 [eph conventions]; **20.70 is adopted** so that the site catalogue reproduces |
  | `corfu` | Corfu town | 39.62, 19.92 | sensitivity | [acq §2.2] |
  | `zakynthos` | Zakynthos town | 37.78, 20.90 | sensitivity | [acq §2.2] |
  | negative-control and control sites | as given in `negatives.json`, `controls_real.json`, `controls_almagest.json` | | | each file's own `observer_place` entries |

  Each row also carries the site's span (Julian years) and the sky-table
  columns it needs. Only Ithaki needs every column over the whole span (4.1)
  [r1 N12].

  Revision 1's Paliki (Lixouri) is dropped: Lixouri lies about 0.05° from
  Argostoli [me: approximate coordinates 38.20°N 20.44°E, not checked
  against a gazetteer], and Kefalonia is already within 0.001 in magnitude of
  Ithaki for the 1178 BC eclipse [eph §5.4].
- **ΔT models.** Four, each with its stated 1σ [eph §2.2–2.3; rev #19]:
  SMH2020 (S15 spline plus the HMNAO lod integral before −720), the Addendum
  2020 parabola, the SMH2016 parabola, and Espenak–Meeus in its canon form
  (ṅ −25.858). Revision 1 counted Espenak–Meeus twice, in two ṅ frames; it is
  one model [rev #19]. The **equal-weight mixture** is over these four, each
  taken as a Gaussian with its stated σ (an assumption, stated every time it
  is used [eph §8 item 1]). Espenak–Meeus σ is Huber's before −500 and
  Morrison–Stephenson 2004's 0.8u² from −500, as on NASA's page; the envelope
  is discontinuous at −500 [acq §2.2], which matters only for controls near
  that year and is reported where it does. SMH2020's σ before −2000 is an
  extrapolation [acq §6 item 3]; no eclipse in the bench lies there. **Every
  ΔT-dependent quantity of a control row or a hit strength is scored under
  the mixture**, each model converted to the frame of the elements or
  ephemeris used (4.4, 6.3.3) [r1 N4]. B&M's 27,602.7 s is T0b's clock
  only.
- **ΔT travels with its lunar ephemeris.** SMH models pair with DE431 (the
  DE430 lunar model); Espenak–Meeus pairs with the NASA Besselian elements.
  A value is converted between ṅ frames (−25.82 ↔ −25.858: 34 s at −1177)
  before use in the other frame [eph §2.3, §5.3]. Lunar-timed quantities
  (conjunctions, full moons, lunar eclipses, Moon rise and set) are computed
  with DE431 and SMH2020 ΔT; planets and stars with DE441 [me, from eph §5.3].
  DE431 is split at JD 1721425.5 (AD 1 Jan 3, Julian); no DE431 request may
  straddle it, so all lunar code works in yearly chunks [acq §1.1].
- **Magnitudes.** One definition is pinned for each use [rev #21; r2 R2-7].
  - **`smag`** is NASA's magnitude at the site, at maximum, exactly as
    NASA's `program.js` prints it.
    - While the eclipse is partial at the site, it is the fraction of the
      Sun's diameter covered, (L1′ − m)/(L1′ + L2′) in Besselian terms.
    - While it is total or annular there, it is the Moon/Sun diameter ratio
      (L1′ − L2′)/(L1′ + L2′).
    - `program.js` computes the covered fraction as mid[37] and the ratio as
      mid[38] (line 361), then puts the ratio in mid[37] for total and
      annular eclipses (lines 534–537 of `data/jsex/program.js`). The site
      catalogues' `mag` is that final mid[37] [acq §2.2; r2 R2-7].
    - At an annular eclipse the ratio *is* the covered fraction of the
      diameter through both centres, so one definition serves every phase.
      Revision 3 wrongly called the partial formula alone "NASA's
      magnitude".
  - **`smag_partial`** is the partial formula at every phase (mid[37] before
    the override). It is used only to compare with references that use that
    formula (I2b).
  - **`obsc`** is the fraction of the Sun's area covered. A separate
    **central flag** (total, annular or none) carries the duration in
    seconds.
  - **Example.** For the 1131 BC eclipse at Ithaki, smag = 1.0486 (total;
    the ratio) and smag_partial = 1.0169 [rev #21; r2 R2-7].
  - **Thresholds.** X3 (smag ≥ 0.95), h_09 (≥ 0.9) and h_06 (≥ 0.6) read
    smag. An annular eclipse passes them by its diameter ratio, and a total
    one always passes.
  - **Lunar.** `umag` umbral and `pmag` penumbral magnitude in the
    convention of NASA's lunar canon, fixed by instrument check I4. One digit
    = 1/12 of the lunar diameter [pcr §2].

**Provenance tags.** A tag names the document and section that carries the
number and its primary source.

| tag | document |
|---|---|
| [bm §n] | `docs/research-bm2008.md`, the reconciled spec of the paper |
| [bm-a, clue X] | `docs/research-bm2008-a.md`, one of the two extractions merged into it, by clue |
| [chron §n] | `docs/research-chronology.md` |
| [txt §n] | `docs/research-textclues.md` |
| [eph §n] | `docs/research-ephemeris.md` |
| [vis §n] | `docs/research-visibility.md` |
| [ctl §n] | `docs/research-controls.md` |
| [win §n] | `docs/research-window.md` |
| [crit §n] | `docs/research-critiques.md` (the responses since Schoch) |
| [rev #n], [rev Vn] | `docs/critique-design.md`, issue n or verification row Vn |
| [acq §n] | `docs/data-acquisition.md` |
| [pcr §n] | `docs/controls-real-drafting.md` |
| [lcr] | `docs/license-check-controls-real.md` |
| [alm §n] | `docs/controls-almagest.md` (it holds the true dates; build agents do not read it, 10.1) |
| [lca1 …] | round 1 of the *Almagest* licence check. Its report was moved when round 2 replaced it, and is now `results/license-check-almagest/r2/license-check-almagest.r1.md` (SHA-256 `2a9b626e…75fd7`) |
| [lca2 …] | round 2 of the *Almagest* licence check: `docs/license-check-almagest.md` (SHA-256 `3254d63f…c6afd`; byte copy `results/design-revision-v5/license-check-almagest.round2.md`). Revision 4's "[lca]" tags meant round 1 |
| [neg §n] | `docs/negatives-drafting.md` |
| [lcn …] | round 1 of the negatives' licence check: `docs/license-check-negatives.md` |
| [lcn2 …] | round 2 of the negatives' licence check. Its agent could not write a report file. Its findings, relayed to the design stage as text, are recorded verbatim in `results/design-revision-v5/license-check-negatives-r2.relayed.md` ("finding n"); its per-row verdicts are the `license_check` fields of `negatives.json` |
| [unread §n] | `docs/research-unread-primaries.md` |
| [r1 Nn], [r1 §n] | the recheck of revision 2 (new issue Nn or section n), written 2026-10-04 as `docs/critique-design-r1.md`, SHA-256 `82308707…71b`. A byte copy is kept at `results/design-revision-v5/critique-design-r1.recheck-of-rev2.md`, because a re-run of the review loop writes its own round-1 recheck to the same name |
| [r1: script] | a script of that recheck in `results/critique-design-r1/`, with its `.out.txt` |
| [r2 R2-n], [r2 §n] | the recheck of revision 3 (new issue R2-n or section n), written as `docs/critique-design-r2.md`, SHA-256 `8db84b10…865c493`; byte copy `results/design-revision-v5/critique-design-r2.recheck-of-rev3.md`, for the same reason. It numbers the first review's issues 1–25 and r1's N1–N17 as 26–42; section 14 numbers its own R2-1 to R2-12 as 43–54 |
| [r2: script] | a script of that recheck in `results/critique-design-r2/`, with its `.out.txt` |
| [v1 §n] … [v4 §n] | `docs/DESIGN-v1.md` … `docs/DESIGN-v4.md` (revision 4: SHA-256 `bd828f14…f5db`) |
| [AppT n] | item n of Appendix T, the truth-side facts, at the end of this file (withheld from build agents, 10.1) |
| [B&M §X] | the paper: Baikouzis & Magnasco, PNAS 105 (2008) 8823–8828, by section heading; [SI], [S2] its Supporting Information |
| [Od. x.y] | Greek text, `data/text/odyssey-grc.tsv` |
| [me], [me: script] | reasoned or computed for this design; arithmetic is shown. Revision 3's scripts are in `results/design-revision-r2/`, revision 4's in `results/design-revision-r3/` and revision 5's in `results/design-revision-v5/`, each with its outputs; the path is given wherever it matters |

"B&M" is Baikouzis & Magnasco 2008 throughout. A statement a note made from
a secondary report keeps that status here and is marked *secondary*. The
hashes of every document cited above are in
`results/design-revision-v5/preserved_sha256.txt`.

---

## 1. The claim under test

### 1.1 What the paper says

B&M's abstract, paraphrased closely (full text local at
`data/bm2008-a/bm2008-pmc-fulltext.txt`):

- They take three overt astronomical references in the epic (Boötes and the
  Pleiades, Venus, the New Moon) and add a conjectural one, Hermes' trip to
  Ogygia read as the motion of the planet Mercury.
- They search every date in 1250–1115 BC (−1249 to −1114) for days matching
  these phenomena in the order and manner the text gives.
- In that span, in their words, "a single date closely matches our
  references": 16 April 1178 BC (−1177) [bm §9].
- They do not assume an eclipse; Theoclymenus' vision (Od. 20.351–357) is not
  a search criterion. They speculate afterwards that the references and the
  vision refer to the total solar eclipse of that day, which Schoch (1926)
  and P. V. Neugebauer (1929) had computed as total over the Ionian Islands
  [B&M abstract; bm §2, §11].

The body adds four claims the bench also tests [B&M §Intersecting,
§Historical Plausibility, §Conclusions; bm §2]:

1. The date satisfies all criteria as stated in the 135-year span, under both
   their sequential and parallel day counts, exactly under the sequential one.
2. The references can be matched exactly about one day in 2,000 years. The
   arithmetic is one candidate New Moon in 6 years × 3 (Venus) × 116 days
   (Mercury) ≈ 2,088 years [bm §10]. **The 6 years is the rate of the season
   clue C and the equinox clue E together** [B&M §Intersecting; vis §3.4],
   and E is the clue B&M listed but did not apply. The figure therefore
   describes five clues, not the four that were searched [rev #5, V2].
3. Two independent sets of verses (the eclipse lines and the other sky
   references) point to the same day; chance agreement of fictional
   references with the only eclipse of the century would be minute.
4. Supporting coincidences found afterwards: the eclipse near noon, early
   spring, Mars invisible except during the eclipse.

The search criteria, as reconciled from the primary text and the
transcriptions of Table S2 [bm §5]:

| clue | lines | criterion | day (sequential / parallel) |
|---|---|---|---|
| N, New Moon | Od. 14.161–162 = 19.306–307; 14.457; Apollo's feast 20.156, 20.276–278, 21.258–259 | Ti is the date of a New Moon (search unit) | 0 / 0 |
| C, Pleiades and late-setting Boötes | Od. 5.270–277 | Ti−29 ≥ 17 Feb and Ti−12 ≤ 4 Apr, so Ti in 18 Mar–16 Apr of a common year | −29 / −28 (all sailing nights to −12 / −11) |
| V, morning star | Od. 13.93–95 | Venus rises ≥ 90 min before the Sun | −5 / −4 |
| M, Hermes = Mercury | Od. 5.43–58, 5.97–103 | Ti−34 within a few days (S2: ≤ 1 to pass) of Mercury's maximum western rise azimuth (MWRA), Mercury visible | −34 / −33 |
| E, Poseidon = equinox | Od. 5.282 | 1 Apr ≤ Ti−11 ≤ 5 Apr in §References; "on or before 4 April" in §Intersecting; listed, **not applied** | −11 / −10 |
| X, the eclipse | Od. 20.345–357 | not used | 0 |

**Where the clues came from.** No clue in N ∧ C ∧ V ∧ M was formulated blind
to 1178 BC [unread §9 item 3]. Schoch found April *from* the eclipse,
searching −1240 to −1140 with no season constraint [unread §3.1]. Every
season reading before 1967 that MacDonald surveys is autumn or winter
(Finsler, Wilamowitz, Scott, Murray, and Schoch's own later "winter") [unread
§2.1, §2.4]. MacDonald 1967, the first spring reading of 5.272, already cites
the eclipse, shifts his timetable a week to meet it, and checks Venus in the
eclipse year; the equinox reading E is also his [unread §2]. Only M is B&M's
own, and B&M too knew the target.

**What follows for the bench.** N is the one partial exception: the
scholia already read 14.162 as the ἕνη καὶ νέα, the day of conjunction
[txt §5.1]. Even so, N adds nothing to the coincidence, because every target
is a new moon. The record therefore leaves no categorical reading of C, V, M
or E that was formed blind. A target's agreement with a reading formed for
it is not evidence, so the bench applies one rule to all four [r1 N6]:

- C, V and M are conditioned on: G is taken over targets whose sky
  satisfies them (5.3);
- E is left out of every garden the decision rule reads, and B&M's search
  is judged without it (3.5).

The same rule covers the clues B&M cited as support. B&M cite 14.457,
σκοτομήνιος, for their new moon [bm-a, clue N], and the dossier computed its
circumstances for 1178 BC before the bench wrote a predicate for it [txt
§5.2]. So H2 is not counted as evidence (7.1).

What remains as evidence is of two kinds:

- **B&M's tolerances.** Beyond the categorical readings, the tolerances may
  single out a target more often than chance. G prices that (5.3). The
  recheck's estimate shows that they cannot do so at 5% whatever the sky of
  1178 BC (2.9) [r2 R2-1].
- **The clues nobody fitted.** These are the held-out predicates H3 and H4,
  frozen in revision 1 and never evaluated at the target (section 7). They
  may agree with the target's sky.

Only the second kind can give a "yes" (1.3).

### 1.2 What the bench can and cannot establish

It can establish:

- whether B&M's computation reproduces with a modern ephemeris, and if not,
  which step fails (section 3);
- how often B&M's criteria, and criteria like them, are met by chance, per
  century and per window (N1, N5);
- how often a date picked out by such criteria would be an eclipse new moon
  if the clues had nothing to do with the eclipse (N2);
- how much the freedom to choose readings, thresholds, tolerances and windows
  inflates a match (N3), and how often a random poem of the same grammar
  "dates" itself to an eclipse as well (N4);
- how probable totality at Ithaca was, over the ΔT models now published (N6);
- whether the method recovers dates that are known, from real eclipse records
  and from real records of B&M's own clue types, and whether it "dates"
  fiction (section 6);
- whether sky clues B&M did not use agree with their date more often than
  chance (section 7).

It cannot establish:

- that the poet meant any line astronomically. Every reading is a fork
  (section 5.3); the bench prices forks, it does not choose between them.
- that Odysseus, the war or the return happened. B&M say the same [bm §2].
- the season of the poem, the meaning of λυκάβας, whether Hermes is Mercury,
  or whether Apollo's feast fell on the new moon. These are philological
  questions; the text and the ancient commentators do not settle them
  [txt §5; vis §3–4; crit §3].
- a posterior probability. The prior that a day-dated sky observation
  survived 400–600 years of oral transmission is not computable; the notes
  found no comparative case [win §10–11]. The bench reports
  look-elsewhere-corrected p-values, the evidential ceiling of the words and
  a Bayes factor under B&M's own hypothesis (5.7), and stops there.

**A bit budget, to fix ideas** [v1 §1.2; rev §1 confirms the arithmetic].
Singling out one New Moon among the 1,683 in B&M's window takes
log2(1683) = 10.7 bits. B&M's applied clues carry about C 3.6 bits (8.3% of
New Moons pass), V 2.7 bits (15.8% of spring Day −5s) and M 4.5 bits (6/136
rows pass with DE441): 10.8 bits in all, so about one chance survivor is
expected (1,683 × 0.083 × 0.158 × 0.044 = 0.97). The forks of section 5.3
could cost up to 5.2 bits (B&M's own forks, without the equinox), 15.1
bits (the documented garden) or 19.5 bits (the full garden) if the readings
were independent. They are not, and measuring how much of that cost is real
is the job of N3.

The record also shows that every categorical reading behind C, V and M was
formed with the target in view (1.1).

- **What conditioning removes.** Conditioning on those readings (5.3)
  removes C's 3.6 bits and the 2.7 bits of the slot event A (P(A) = 0.154
  [r1 N1]).
- **What remains.** By the first recheck's count about 3.0 bits remain: B&M's
  V ∧ M passes about 5 of the 41 targets that satisfy A [r1]. The per-clue
  figures do not add up exactly, because V, M and A overlap. Those bits are
  what the tolerances add, and they are what G over T_A prices.
- **Why that is too few.** A p-value of 0.05 needs 4.3 bits, and B&M's own
  forks spend up to 5.2. So the remaining bits cannot carry a "yes" [r2 R2-1].
  The recheck's G_BM of about 0.14 (2.9) says the same thing directly.
- **Where a "yes" could come from.** The held-out clues add bits that nobody
  fitted: at most log2(1/p_H,min) ≈ 5.3 bits at the design stage (2.9).

### 1.3 Outcomes

The verdict is a set of labels computed mechanically by `verdict.py` from
named quantities (section 9). Every condition names its garden and its target
pool. It also says whether its input is **null-side** (fixed by the sky and
the readings, with the target masked) or **target-side** (it reads 16 Apr
1178 BC) (9.1). Every interval is taken against the claim being made.

Revision 3's outcome 1 asked for G_BM,hi ≤ 0.05. G_BM is null-side, and the
recheck estimates it at about 0.14 (95%: 0.087–0.215). So no sky of 1178 BC
could have met that condition [r2 R2-1]. The same holds for revision 3's
other two "yes" conditions:

- **T0 = R** needs 18 Mar 1189 BC to fail B&M's criteria, and it passes them
  whatever the Odyssey encodes (2.2).
- **pct_N4,hi ≤ 0.05** is a reach percentile of the same kind as G (5.4).

A "yes" therefore has to rest on evidence that B&M did not fit, and whose
power to say "yes" can be checked before the target is looked at [r2 R2-1
fix 4]. The labels are these.

1. **The text dates the return.** All four must hold:
   - **T0_pass.** B&M's applied criteria (N, C, V and M, without the equinox
     clue) pass for 16 Apr 1178 BC with a modern ephemeris (3.5).
     - This is the part of B&M's reproduction that depends on the target's
       own sky.
     - Whether 1178 BC is also the only candidate in their window (T0 = R)
       depends on the other candidates' skies. It is reported, and it
       counts for nothing. Its weight is what G prices, under label 2.
   - **p_H ≤ 0.05.** The clues nobody fitted agree with that date. The
     held-out predicates H3 and H4 rank 1178 BC at p ≤ 0.05 by an exact rank
     test, among the candidates that B&M's own readings accept (P_BM) **and**
     among those that pass the Mercury event B&M applied (P_MWRA). p_H is the
     larger of the two p-values (section 7).
   - **No 3a and no 3b.** Both components of the method can see (section 6).
   - **No 4.** No clean negative dates itself.

   The held-out test has a null-side floor, p_H,min: the p-value that the
   most favourable possible target would earn, the larger of the two pools'
   floors. It is computed with the target masked, before any target-side
   number (9.4, 12). At the design stage it is about 0.026 (2.9), so outcome
   1 is attainable.
2. **B&M's match carries no weight.** The label takes one of two forms:
   - **No match.** No reading of 𝒢_BM* makes 1178 BC the unique survivor of
     any 136-year window containing it (r_Ody = 0) [r2 R2-3].
   - **Ordinary.** Either condition is enough:
     - B&M's own readings make a comparable target the unique match often
       (G_BM,lo ≥ 0.20 under every slot definition of 4.2);
     - at least half the random poems of the same specificity reach
       Schoch's target as well as the Odyssey does (pct_N4,lo ≥ 0.50, ties
       counted for the Odyssey).

   Label 2 judges B&M's fitted readings, and label 1 judges the clues nobody
   fitted. Both can hold at once. The verdict then says that the unfitted
   clues date the return, and that B&M's own match is not what shows it.
3. **The method cannot see**, split by component [rev #3]:
   - **3a, the eclipse component**: the method does not recover the dates of
     real eclipse records (PC-R, section 6.3).
   - **3b, the B&M-type component** (lunar phase, star season, morning star,
     Mercury turning point): the method does not recover the dates of real
     planetary and lunar records of B&M's own kinds, at observer slack
     calibrated on the *other* records (the *Almagest* control, section
     6.4).

   Every "no" about the Odyssey that depends on the failing component is
   reported as "could not have seen it".
4. **The method dates fiction.** A clean negative (fiction composed long
   after the events it tells) yields, under its own sourced readings, an
   eclipse match at least as strong as the Odyssey's (hit_j). Its
   significance must also be at least as great, even at the negative's
   least favourable bound (G_j,hi ≤ G_BM,u). That retires the method, not
   only the claim.

**Inconclusive** is reported when none of the labels applies, with every
quantity and threshold beside it. Labels 2, 3a, 3b and 4 can hold together.
Label 1 can hold with label 2, and excludes 3a, 3b and 4.

**Qualifiers** are reported whenever they hold:

| qualifier | meaning | inputs | section |
|---|---|---|---|
| Q_attain | outcome 1 could not have been reached by any target, because p_H,min > 0.05 (the larger of the two pools' floors). Every "no" about the dating is then a "could not have said yes" | null-side | 7, 9.4 |
| Q_tol | B&M's own readings could not have dated any target at 5%: G_BM,lo > 0.05 under every slot definition. Printed beside the words' ceiling 1/P(A) [r2 R2-1 fix 3] | null-side | 5.3, 5.7 |
| Q_slot | a G-based decision (label 2's G leg, or Q_tol) differs between slot definitions: "slot-dependent" [r2 R2-2 fix 3] | null-side | 4.2 |
| Q_BM | B&M's own tolerances and proxies cannot recover expert planetary records | controls | 6.4 |
| Q_H | the held-out rank test does not recover real records: fewer than 6 of the 11 counted *Almagest* sets give their true date p ≤ 0.05 on their own held-out rows. Three sets have no held-out row, so at most 8 can (6.4) | controls | 6.4 |
| Q_strict | an all-clues-must-pass rule rejects the true date of most real eclipse records | controls | 6.3 |
| Q_exposure | gate 3a changes when the possibly steered control rows are re-drafted blind, or set to a sourced sibling convention | controls | 6.3.4 |
| Q_ΔT | gate 3a changes when the controls whose eclipses helped fit the ΔT models are scored without that fit | controls | 6.3.3 |

**Standing findings** are printed with every verdict and never change a
label. They are:

- the evidential ceiling of the words: 1/P(A), and the Bayes factor BF_BM
  under B&M's own encoding hypothesis (5.7);
- the T0 grid, with R, RE or NR in each cell (3.5);
- the ancient reading R_anc under its four season bounds (5.3);
- the held-out clues in detail: each predicate at the target, the sensitivity
  pools, and the uncounted H1, H2 and H5 (7);
- the *Almagest* calibrations of the Bayes factor and of the held-out test
  (5.7, 6.4).

"What, if anything, the text can date" is reported in every case, at the
level the tests support:

- a relative chronology [chron §5];
- a month-turn on Day 0 under one reading [txt §5.1];
- a season the text does not determine [txt §5.6];
- a year only if outcome 1 holds.

---

## 2. What is already known, and so is not a prediction

These numbers exist before the freeze. They are listed so that nothing in
section 8 pretends to predict them. The facts measured at a control's true
date belong to this record too, but they are kept in Appendix T, so that the
agents who build the searcher never read them (2.6, 10.1). Where a number came from a rough model,
the row says so and the bench recomputes it, but its confirmation is not
counted as a success.

### 2.1 Instruments already built and validated

| item | result | source |
|---|---|---|
| Ephemeris coverage | one DE441 excerpt −2060-01-01..+241-01-01 Julian (JD 968642.5–1809083.5), 11 bodies, 237.9 MB; DE431 Sun/EMB/Earth/Moon over the same span in two pieces split at JD 1721425.5; DE431 ±60-day excerpts for −1339 Jan 8 and −647 Apr 6 | [acq §1.1] |
| `ephem.kernel()` | picks the shortest covering excerpt; 4,500/4,500 old requests unchanged; Chebyshev records bit-identical between narrow and long excerpts (11 pairs); 68/68 module results identical to the last bit | [acq §1.2–1.3] |
| Ephemeris validation | `validate_ephem.py` 55/55 (identical line for line to 2026-10-03 apart from the file list and run time; run with `PYTHONIOENCODING=utf-8`); `test_ephem.py` 10/10 | [acq §1.3; eph §10] |
| Horizons spot checks, −1999 to +200 | astrometric Sun/Venus/Mercury ≤ 0.0022″, Moon ≤ 0.524″, elongation ≤ 0.57″; az/el ≤ 78″ at −1999 falling to 4″ at +200, tracking the IAU 1982 vs Vondrák sidereal-time difference (+79.5″ at −1999); tolerances fixed before the run | [acq §1.3] |
| DE441 − DE431 lunar offset | follows the +0.00335″ T³ law over −1999..+200 at ratios 0.85–1.03; +187.7 s in greatest-eclipse time at −1177 | [acq §1.3; eph §5.3] |
| NASA Canon elements | 23 century files −1999..+300, 5,486 eclipses, byte-identical to earlier copies; every SEcat5 eclipse matches one element row (TD ≤ 0.5 s, ΔT ≤ 0.5 s, γ ≤ 0.00005); element ΔT = `dt_em2006_canon` at a day-resolved year to ≤ 0.15 s | [acq §2.2] |
| Site catalogues | Ithaca, Kefalonia, Lefkada, Corfu, Zakynthos, 5,486 rows each (NASA's JavaScript); identical field for field to the earlier window catalogue over −1499..−600 | [acq §2.2] |
| Stars | 21 stars in `data/stars.json`; every HIP number read from SIMBAD's identifier list and checked against hip2 (position ≤ 0.038″, \|Hp − V\| ≤ 0.37); the five numbers revision 1 gave from memory are confirmed (Sirius 32349, Aldebaran 21421, Betelgeuse 27989, Rigel 24436, Dubhe 54061) | [acq §3] |
| Sirius | the Hipparcos solution for HIP 32349 is an orbital solution referred to the centre of mass, so its proper motion is barycentric and is adopted, with system RV −8.47 km/s (Bond et al. 2017). At −1177: FK5 long-baseline motion differs by 0.99′, Bond-orbit re-referral by 1.02′, a photocentre motion would be 24.2′ off | [acq §3.3] |
| Calendar | `odybench/calendar.py`; `tests/test_calendar.py` 11/11, including every day of −1999..+500 against independent day counting, 306/306 Horizons calendar dates, and the `datetime` ban; a mutation check catches 5 deliberate bugs. The Meeus ch. 7 values in the test were recalled, not read, but each also agrees with exhaustive counting | [acq §4, §6 item 7] |

### 2.2 Reproduction

- **T0a is done.** Two independent transcriptions of Table S2 agree cell for
  cell (152 rows × 13 fields). The decoded colour rules on the 136 rows of
  1250–1115 BC give V 21, M (\|Δ\| ≤ 1) 4 (1236, 1224, 1178, 1157 BC), E 22
  (XXX) / 20 (1–5 Apr) / 17 (1–4 Apr), V ∧ M = {1178} [bm §8.1;
  `results/bm2008-reconcile/s2_counts.out.txt`].
- With Mercury recomputed by DE441 on S2's own Ti, M passes in 1236, 1224,
  1190, 1189, 1178 and 1144 BC; 1157 BC drops out (DE441 MWRA 22 Feb, Δ −3);
  **V ∧ M = {1178, 1189}** [bm §8.2].
- 18 Mar 1189 BC (−1188) passes N, C (Ti−29 = 18 Feb in a leap year), V
  (lead 100.9 min) and M (Δ 0), and fails E (Ti−11 = 7 Mar) [bm §8.2;
  rev V10].
- No visibility threshold separates the two: at Mercury's rising the Sun
  stood at −13.2° on 13 Mar 1178 BC and −17.1° on 13 Feb 1189 BC [bm §8.2].
- **The integer MWRA is ill-conditioned** [rev #12, V15]. Rises bisected to
  0.01 s give, for 1178 BC, 12 Mar 112.30419° and 13 Mar 112.29647° (vertex
  about 12.3 Mar, Δ about +0.7 d) and, for 1189 BC, 12 Feb 120.48066° and
  13 Feb 120.48110° (vertex about 12.5 Feb): the 1189 integer maximum is
  decided by 0.0004°. Minute-rounded rises put the series 0.1° off and make
  it non-monotonic [`results/bm2008-reconcile/check_extras.out.txt`].
- Venus leads on Ti−5: 103.6 min on 11 Apr 1178 BC (B&M 1:42:56) and
  100.9 min on 13 Mar 1189 BC [rev V10].
- Conjunctions 18 Mar 03:31 and 16 Apr 12:25 UT+2 (−1177, ΔT 27,602.7 s);
  equinox 1 Apr 15:31 UT+2 (B&M 15:24); Sun at −12° on 18 Mar at 19:34 UT+2
  (B&M 19:38) [bm §9].
- Under the parallel reckoning 1178 BC misses the Pleiades bound and the
  equinox bound by one day each [bm §9].
- Under B&M's ≤ 4 Apr equinox bound (§Intersecting), 1178 BC fails E,
  because Ti−11 = 5 Apr [rev #23].
- The candidate count over "1 Jan 1250 – 31 Dec 1115 BC" was 1,682 in the
  timing run (which ended at 0 h on 31 Dec), 1,683 in `check_ti` and 1,684
  in B&M [rev #22].
- Reach of 1178 BC under the T0b reading with E off: 1189 BC lies 11 years
  earlier, so reach_136 ≤ 11/136 = 0.081, and it is 0 if another survivor
  falls in −1176..−1052; that span has not been computed [rev #24c].

### 2.3 The eclipse

| eclipse | site | pairing | values | source |
|---|---|---|---|---|
| 16 Apr 1178 BC | — | canon | catalogue 01966, Saros 39 member 31, γ 0.5187, magnitude 1.0599, greatest eclipse 32.7°N 12.7°E at 17:57:28 TD = 10:00:58 UT, ΔT 28,590.0 s | [rev V4] |
| | Ithaki | NASA elements, canon ΔT | smag 0.984 at 10:22 UT = 11:45 LMT = 11:44 LAT, Sun 57.2°; total for constant ΔT 28,801–29,585 s (28,805–29,580 s on a 5-s grid) | [eph §5.4; rev V5] |
| | Ithaki | DE431 + SMH2020 28,543 ± 720 s | 0.984 at LAT 11:44; total for 28,761–29,545 s, i.e. +218 to +1,002 s above the central value (+0.3σ to +1.4σ) | [eph §5.4] |
| | Ithaki | DE441 + SMH2020 | 0.972 at LAT 11:49; total for 28,922–29,706 s | [eph §5.4] |
| | Ithaki | DE441 + B&M's 27,602.7 s | 0.900 at 12:48 UT+2, not total; mixes ephemerides, reported only to show it | [bm §3.3] |
| | Lefkada | DE441 / DE431, SMH2020 central | 0.981 / 0.993; Kefalonia within 0.001 of Ithaki | [eph §5.4] |
| 30 Sep 1131 BC | Ithaki | NASA, canon | total; 09:49 UT = 11:12 LMT; Sun 51.6°; total for 27,050–28,035 s (−641 to +344 s from canon); smag 1.0169, diameter ratio 1.0486 | [rev V6, #21] |
| 24 Jun 1312 BC | Ithaki | NASA, canon | 0.984 at 12:02 LMT (about 12:09 LAT); total for +539 to +1,449 s above canon | [rev V6; win §7.1] |

**P(total at Ithaki) per ΔT model**, each model's σ taken as Gaussian, in the
canon frame on NASA's elements (SMH values converted by +34 s) [rev #17;
`results/critique-design/check_p19.out.txt`, `check_mag09.out.txt`]:

| model (value ± σ at −1176.68) | P(total) 1178 BC | P(total) 1131 BC | joint, common offset | P(smag ≥ 0.9) 1178 BC |
|---|---|---|---|---|
| SMH2020 28,543 ± 720 | 0.294 | 0.494 | 0.047 | 0.932 |
| Addendum 2020 parabola 28,282 ± 541 | 0.173 | 0.641 | 0.052 | 0.934 |
| SMH2016 parabola 28,963 ± 541 | 0.498 | 0.443 | 0.108 | 0.997 |
| Espenak–Meeus, canon form 28,589 ± 1,008 | 0.252 | 0.412 | 0.049 | 0.849 |
| **equal-weight mixture of the four** | **0.304** | **0.498** | **0.064** | **0.928** |

[me: means of the rows above.] In the DE431 pairing the three SMH values are
0.299, 0.178 and 0.505 [eph §5.4]; with Espenak–Meeus on NASA's elements
(0.252) the mixture is 0.309 [me]. The 1178 and 1131 BC totality windows
overlap only near +220 to +340 s above canon ΔT, so at most one of the two
was likely total at Ithaca [win §7.1]. Magnitude ≥ 0.9 holds for constant ΔT
between about 27,600 and 31,000 s; maximum falls between LAT 10:30 and 12:47
over 26,000–32,000 s [eph §5.4].

**Base rates at Ithaca.** In −1499..−600: total at nominal ΔT 6 events;
total for some ΔT within ±1σ 10; the same and 10–14 h LAT 3 (1312, 1178,
1131 BC); smag ≥ 0.95 at nominal ΔT 15 [win §7.2]. Extended with the new
elements: total for some ΔT within ±1σ, 7 in −1999..−1500 (all partial at
nominal ΔT, σ 2,000–3,700 s) and 4 in −599..+300 [acq §2.2]. Under Schoch's
own rule (maximum 10 a.m.–noon) 1312 BC drops out, its maximum being after
noon [rev #10]. The new-moon base rate for "total within ±1σ" is p_e =
8.98 × 10⁻⁴, and for the near-noon subclass 2.70 × 10⁻⁴ [win §8c].

**B&M's own ΔT is uninterpretable.** Starry Night 6 Pro Plus used 29,300 s
at −1206 (Papamarinopoulos et al. 2012), the Espenak–Meeus parabola + 35 s;
B&M's Starry Night 6.0.4 used 27,602.7 s at −1177, the parabola − 1,114 s.
One smooth ΔT(t) cannot give both: the gap is 1,149 s [unread §7].

### 2.4 Rates and arithmetic

- Per-clue chance rates over 1250–1115 BC at Ithaca: C passes 8.3% of new
  moons (1.02 a year); V passes 15.8% of B&M's spring Day −5s (29.6% of all
  days); M (rise-azimuth maximum, visible) 5.0% at ±2 d and 7.9% at ±3 d of
  spring Day −34s; C ∧ E leaves one new moon per 6.2 years [vis §1.3, §2.3,
  §3.4].
- The rough joint expectation is 1.1 chance matches in 136 years; the
  single-target pass rate is about 0.8% given the spring window and about
  0.07% unconditionally [vis §5].
- B&M's own arithmetic redone at their stated ±1-day colour tolerance:
  1.02 × 1/3 × 3/116 ≈ 0.0088 a year = **0.88 per century** with E off, and
  **0.14 per century** with E on, against the 0.048 per century they printed
  [rev #5].
- **The E-on rate is too low to test.** Given C, E passes about 0.158 of new
  moons (1/6.2 a year out of 1.02 a year). T0b's reading has λ ≈ 0.55 per
  century with E off (2.9). So with E on, λ ≈ 0.55 × 0.158 ≈ **0.087 per
  century**, or about **1.9 survivors** over the 22 centuries of the
  background. That assumes E is independent of V and M given C [me]. A
  Poisson count with mean 1.9 is 0 or 1 with probability 0.43, so no
  threshold near B&M's 0.048 per century (1.06 survivors) can be decided by
  it. Revision 4's P4 is therefore withdrawn to a reported comparison, R19
  (8.1) [14.4 #66].
- Replacing B&M's clock ΔT by SMH2020 + 1σ moves UT by 1,660 s and flips the
  UT+2 date of about **1.9%** of conjunctions [rev #17].
- Window scaling: at criteria fixed in advance the expected double hit is
  10⁻⁵–10⁻³ per 135-year window [win §8c].
- Garden arithmetic of revision 1: 8 × 4 × 6 × 6 × 31 × 4 × 3 = 428,544
  readings (18.7 bits) [rev §1]. Revision 3's gardens are in section 5.3.
- The Mercury turning points are spread: the morning station precedes GWE by
  12–15 d; the rise-azimuth maximum falls 26 d after to 9 d before GWE; under
  "GWE or station within ±2–3 d" 1178 BC fails [vis §2.3, key finding 3].
- With Day 0 one day after the conjunction (Solon's noumenia), 1178 BC
  drops out of the joint test [vis §4.3].
- Given Day 0 a conjunction, the median Moon-up share of the night after
  Day −5 is 25%, so H2's "< 25%" passes about half the time; 24–31% of all
  nights are as dark [vis §4.5; rev #24b].

### 2.5 Sources now read

- **MacDonald, *JBAA* 77 (1967) 324–327** (4 pages, not 324–328) [unread
  §2]. He argues for **March** for the voyage, from Od. 5.270–277 ("late"
  read as lateness), with Neugebauer's star tables and Schoch's arcus
  visionis, plus a timetable reading Poseidon's return (5.282) as the
  equinox. He discusses the 1178 BC eclipse (16 April, 11.45 a.m. local
  time) and shifts his timetable a week to meet it. He gives Venus' greatest
  morning elongation "in 1176 B.C. on March 17"; DE441 has it on 16 Mar −1177
  and none in −1175, so "1176" is very probably a slip for 1178 [unread
  §2.5]. **Gainsford's "second half of May" misreads p. 327**, where
  MacDonald answers Schoch's "winter and not April" from the reaping match;
  Gainsford's locator ("217") and his "26 April 1178" are also wrong [unread
  §2.3].
- **Papamarinopoulos et al., *MAA* 12(1) (2012) 117–128** read the same star
  lines as autumn and reach 30 Oct 1207 BC (−1206) through a stated chain
  (64 → 14 → 5 → 1 eclipses). Their 16:00 "LT" is UT+2, i.e. 15:23 LMT at
  Vathy. Their canon ΔT is 29,136 s. The first author had endorsed 16 Apr
  1178 BC in 2008 [unread §4].
- **Henriksson, *MAA* 12(1) (2012) 63–76** is about the Iliad only; his
  eclipse is the canon's −1311 Jun 24 (Julian); his "Gregorian" labels run
  one day early [unread §5].
- **PLSV has no extinction model.** Visibility is an arcus visionis plus a
  "critical altitude" (default 0°); default AV = 10.5 + 1.4m (heliacal) and
  8.9 + 1.1m (acronychal and cosmical); fixed planetary values are Schoch's
  1928 (Mercury morning first 13°); its ΔT is Chapront-Touzé & Chapront 1991.
  B&M used version 3.0; the documentation read is 3.1 [unread §6].
- Neugebauer & Schoch, *AN* 230 (1927) 57: no Odyssey content; Schoch's 1926
  elements were revised within a year; Mercury heliacal AV values (morning
  first 13.8°) [unread §3.2].
- **Not read**: P. V. Neugebauer, *Astronomische Chronologie* (1929);
  Schoch, *Die Sterne* 6:88 and *Dichter-Finsternisse*; P.Oxy. 3710; Austin
  1975; de Jong 2001 App. A; Stanford 1959; the Oxford commentaries; Starry
  Night internals [unread §8].
- **Text facts found by the drafting agents.** *Aen.* 2.255 "silentia lunae"
  admits the conjunction reading (Pliny *NH* 16.190, local key 16.39.2), and
  2.340 "oblati per lunam", in the same night, contradicts it [neg §3.1].
  *Arg.* 1.1202 is a simile; the full Moon of 1.1231–1232 sits on the same
  night as the morning star of 1.1273 [neg §3.2]. An ancient scholiast
  already read Il. 17.366 as an eclipse, but the text confines that darkness
  to mist while the rest fought in bright sun (17.370–373) [neg §3.5]. The
  17-days-then-18th pair of Od. 5.278–279 recurs at 24.63–65; the
  nine-then-tenth pattern occurs 14 times; τρίτον ἦμαρ three times [rev #8;
  txt §3]. "ἀπ' οὐρανοῦ ἀστερόεντος" (20.113) is a stock epithet, used in
  daylight at Od. 9.527, and the scene follows the dawn at 20.91 [rev #24a].
- **The slot matrix of the negatives** [neg §5]: no clean negative fills all
  five Odyssey slots; the Mercury slot exists only in the Iliad (24.339–345)
  and in Virgil's imitation of Od. 5 (*Aen.* 4.238–258); the morning star in
  every poem closes a night of action; the poets' literal Moons are mostly
  lit, and a Day-0 conjunction is everywhere an inference.

### 2.6 Controls: what is already known about them

Facts measured at a control's true date are truth-side. Revision 5 keeps
them in Appendix T, which the agents who translate and search the control
files do not see (10.1). This section keeps the facts that need no truth,
and what the truth-side facts imply in aggregate.

**The *Almagest* records of B&M's own clue types** (`controls_almagest.json`)
[alm §0, §3; lca1; lca2]:

- **Two licence checks**, neither of which read a truth file. Round 1 edited
  43 rows. Round 2 re-checked all 72 and edited 24, removing no row and
  changing no primary option, option name or day offset [lca2 Result]. Every
  word licence is now an exact substring of its cited row, in text order
  [lca2 method 1]. File history: `e16c559d…37e9` (the builder's output),
  `758ee789…4c83` (round 1), `18b3ff01…b458` (round 2) (12.4).
- **Ptolemy's arithmetic, checked without the truth.**
  - His own solar tables reproduce his stated mean Sun for 32 of 34 records
    to ≤ 0.12° [alm §1.3].
  - The two failures are textual cruxes, carried as forks whose primary is
    "as printed": IX.7.11, one Egyptian month (ALM-H.3), and IX.9.4, three
    days (ALM-A.6) [alm §1.4].
  - Round 2 recomputed all 20 interval rows from the Greek alone, and again
    from Ptolemy's Sun. Every interval agrees within 0.3 d except the two
    cruxes, and Ptolemy's Sun confirms both emended intervals, +49 for A.6
    and +72 for H.3 [lca2 method 3].
- **Structure** [me: a dump of the file, `results/design-revision-v5/`
  notes]. 12 sets and 72 rows: 26 planet, 20 interval, 17 star, 7
  moon-phase, 1 lunar-eclipse and 1 season row.
  - ALM-E, ALM-F and ALM-G have no row outside the B&M-type projection whose
    primary is not "none" (F.4, their only star row, has primary "none").
    They therefore have no held-out row (6.4), and **held_ALM ≤ 8** by
    construction.
- **Two lunar phases rest on Ptolemy's numbers, not on his words** [lca2
  item 4; lca1 item 4]. A.10 and B.5 choose their phase class from
  longitudes stated in the row. The other phase rows (A.2, A.5, B.2, B.7,
  B.9) need no coordinates.
- **Four primaries carry a day bound the words do not give** [lca2 §D]. A.1
  and I.1 (`ge_after_within_j`) and B.1 and J.4 (`ge_before_within_j`) bound
  the greatest elongation to j = 7–60 days away. Each row also has the
  literal, unbounded option `ge_*_same_apparition` [lca1 item 2].
- **At the true dates** (truth-side; the tables are in [AppT 1–2]):
  - the observer slack of a "greatest elongation" record is a few days for
    Mercury and up to three weeks for Venus, and B&M's Mercury proxy (the
    MWRA) is a different event from greatest elongation;
  - in regime SL (6.4) the true date is retained in **9 of the 11 counted
    sets**. Whether those 9 also narrow their windows to 5% has not been
    computed; that is what gate 3b still tests (P21);
  - in regime BM the true date can pass in at most 5 counted sets, so
    **rec_ALM_BM ≤ 5 < 6, and Q_BM holds** whatever the narrowing. It is
    recomputed as a regression check, not predicted [r1 N3].

**The real eclipse records** (`controls_real.json`) [pcr §1, §5; lcr]:

- **Freeze and licence check.** The clue file was frozen before any accepted
  date was looked up (SHA-256 `eb1f0401…9256`, 2026-10-04 05:19 UTC). An
  agent blind to the truth then licence-checked it. That agent moved seven
  unstated-site primaries to "none" and made seven other edits
  (SHA-256 `135fba67…83f8`) [lcr]. The re-run of the workflow did not touch
  this file.
- **The drafting was not fully blind.**
  - The drafter had seen critique issue 2 and revision 1's I2b row, and flags
    three primaries as possibly steered: T1-DARK, D-ECL and the ±1 h in
    L4-DARK [pcr §1].
  - The recheck found a fourth that the drafter did not flag, T2-SEASON
    [r1 N5]. Its primary "early" spans solar longitude [330°, 60°], and its
    start and width are the drafter's. The same set's T1- and T3-SEASON use
    Thucydides' half-year, [0°, 180°] (5.20.3).
  - The recheck also named T-INT-12's ±0.5-year tolerance.
  - Why these two matter is truth-side [AppT 3].
- **A rough post-freeze check** by the drafter, with its own lunar model
  (not the bench's; I4 has not run), found that the accepted dates fail some
  primary reading in three of the seven counted sets and pass every primary
  in the other four [pcr §5; AppT 3]. Which rows fail stays on the truth
  side.
- **Four control eclipses appear in the data behind SMH's ΔT fits** [r1 N4]:
  R-DIOD's eclipse, H-LIVY's L4, R-THUC's T1 and R-XEN's X3. The table
  entries, their years and their bounds are truth-side [AppT 4]. Whether the
  *Almagest* lunar timings entered the fits is not settled: SMH2016's Table
  S4 and §4b have not been read (pre-freeze task, 12.1).
- **Moving the site primaries to "none"** weakens R-THUC and R-XEN in the
  primary run [lcr, Consequences].

**The negatives** (`negatives.json`) [neg; lcn; lcn2]:

- 13 sets: 12 clean negatives, and the Iliad as a same-tradition comparison.
- 70 clue rows and 34 excluded rows; 183 fork options after round 2 [lcn2
  finding 1].
- **Two licence checks**, neither of which read a truth file or
  `docs/research-controls.md`.
  - Round 1 edited 21 rows [lcn §3].
  - Round 2 edited 8 more rows and 5 sets, and kept every round-1 edit
    [lcn2 findings 1, 9]. Its report could not be written to `docs/`, so its
    text is kept as [lcn2], and its verdicts are in the file's
    `license_check` fields.
  - All 178 clue fragments and all 32 place and landmark fragments match
    their cited rows, and no date leaks [lcn2 finding 1].
  - File history: `405f78da…bebe` (the builder's output), `f4ae3b26…bb00`
    (round 1), `be4f511e…9c82` (round 2) (12.4).
- **What round 2 changed that the design must translate** (6.5): a new
  Day-0 solar-eclipse option, ARG-RETURN-04:d; a fourth reading of *Aen.*
  2.255 with its pin, AEN-TROY R-iii; Ida moved from the observer places to a
  new `landmarks` list; ARG-COLCHIS-01's night now set by ARG-COLCHIS-02's
  option [lcn2 findings 3–5, 8].
- I11(a), the contradictory AEN-TROY reading R-ii-literal, gives **zero
  survivors** at Troy among 1,683 conjunctions of 1250–1115 BC and 3,104 of
  1350–1100 BC. That holds by astronomy, not by logic [r1:
  check_i11a.py]. Round 2's R-iii keeps 2.340 and is not contradictory, so
  it is an ordinary pinned reading.

### 2.7 Predictions of earlier revisions that are now settled

| revision, prediction | status | numbers |
|---|---|---|
| v1 1–5 (T0) | largely implied by 2.2 | kept in section 8 as regression expectations, not counted |
| v1 18 (mixture P(total) 0.15–0.40; P(mag ≥ 0.9) ≥ 0.8) | **holds already** | mixture 0.304 (canon frame), 0.309 (pairing rule); P(smag ≥ 0.9) 0.928 (2.3) |
| v1 19 (1131 higher under every model; joint ≤ 0.05) | **fails as written** | the SMH2016 parabola gives 0.498 against 0.443; the joint 0.108 (SMH2016) and 0.052 (Addendum) exceed 0.05 [rev #17] |
| v1 20 (< 2% of dates flip) | sits on its threshold | about 1.9% [rev #17] |
| v1 21 (PC-S recall ≥ 0.99 at zero noise) | tautological as built | replaced by the two PC-S modes [rev #14] |
| v1 24 (NC4 zero survivors, NC5 never unique) | true by construction | moved to instrument check I11 [rev #15] |
| v2 P23 (R_anc's survivors include 1131 BC) | **fails as written** | v2's season bound [180°, 270°) excludes 30 Sep 1131 BC, when the Sun stood at 176.69° [r1 N7]. Restated with ancient season definitions (5.3); the known part is in 2.8 and 2.9 |
| v2 P26 (per-model P(total) orderings and joint bounds, DE431 frame) | **known** in the canon frame | the 2.3 table [r1 N7]. Only the move to the DE431 frame (about 40 s) is new, and 5.6 recomputes it as a regression expectation |
| v2 P30 (at ν_real the B&M reading recovers ≤ 70% of spring truths) | **near-certain** | B&M's V ∧ M passes 5 of 41 accepted truths at zero noise [r1: check_lr_cap.py] |
| v2 P32 (rec_PCS ≥ 0.5) | **definitional** | about 0.68 (28/41) by the overlap of generator and searcher [r1 N2]. rec_PCS is removed from the gate |
| v2 P34 (strict_PCR = 4) | confirms a rough known check | a regression expectation (8) |
| v2 P36 (rec_ALM_BM < 6) | **known** under the frozen option rule | 2.6 |
| v2 P41, P42 (LR_real,lo < 30; no outcome 1) | **follow from the ceiling** | LR ≤ 1/P(A) ≈ 6.5 [r1 N1]. Withdrawn with the LR (5.7) |
| v3 P4 (λ(N ∧ C ∧ V ∧ M) in [0.44, 1.76] per century) | **near its lower threshold** | 0.55 per century over −1999..+200, 0.71 over −1760..−640 [r2 R2-5; r2: check_gbm.py]. Now regression expectation R13, not counted |
| v3 P6 (≥ 10 survivors; P(≥ 1 in 136 years) ≥ 0.5) | **on its thresholds** | about 12 survivors; Poisson P(≥ 1) = 1 − e^−0.75 = 0.53 [r2 R2-5]. Now R14; the open question, clustering, is P6 |
| v3 P12 (reach_136 of 1178 BC under the T0b reading is 0) | **expected to fail** | no T0b-reading survivor in −1176..−1052, so the reach is 11/136 = 0.0815, unless the bench's exact vertex moves 26 Mar 1111 BC inside ±1.5 d [r2 R2-3, R2-5]. Now R15, with both branches |
| v3 P13 (G_BM ≥ 2 p_fix,unique) | **roughly settled** | 0.140 against 0.020 [r2 R2-5] |
| v3 P14 (G_BM in [0.05, 0.40]) | **roughly settled** | 0.140 (0.087–0.215) under revision 3's slots [r2 R2-1] |
| v3 P19 (R_anc with the eclipse clue has ≥ 2 survivors in the reproduction window) | **settled** | 9 survivors in NASA's Ithaca site catalogue at canon ΔT [r2: check_ranc_p19.py]. Now part of R11 |
| v3 P22 (P(unique) ≤ 0.6 among T_A truths passing the B&M reading) | **no power** | about 4 truths in the core; 0.647 on those 4 [r2 R2-5]. Dropped; the figure is reported with its n |
| v3 P30, P31 (held-out pass counts against base rates) | **superseded** | the held-out statistic is now the rank test p_H of section 7, a rule input. P31 compared survivors with a base rate taken from the survivors themselves, so it was empty by construction |
| v3 P32 (BF_BM(ρ = 1) < 5) | **near-certain** | about 2.6, with BF_max about 20.7 [r2: check_gbm.py]. Now R16 |
| v3 P33 (median *Almagest* BF ≥ 10 × BF_BM(1)) | **compares unlike numbers** | an unconditioned BF over day candidates against a BF conditioned on categorical readings [r2 R2-5]. Dropped; both are reported, the *Almagest* figure as a calibration only |
| v3 P34 (G_BM in the inconclusive band) | **roughly settled** | 0.087–0.215 under revision 3's slots [r2 R2-1] |
| v3 P35 ({inconclusive} or {2}, with Q_BM, no 3a, 3b or 4) | **near-certain** in its first clause | it covers both branches of the tie question [r2 R2-3, R2-5]. Replaced by 2.10 and by predictions on the open quantities |

### 2.8 Known from the recheck of revision 2

**The observation model's ceiling** [r1 N1; r1: check_lr_cap.py]:

- **The slot event A.** Over the 266 spring daylight new moons of
  −1499..−1000 at Ithaki (fixed C bounds, SMH2020 ΔT), A is defined on
  Day −5 and Day −34 (sequential count) as follows:
  - Venus is a visible morning star at AV 7°, which holds for **0.398** of
    the targets;
  - Mercury lies within 6 d of a morning rise-azimuth maximum, greatest
    western elongation or station, or is visible at AV 10°, which holds for
    **0.342** (event alone 0.241, visible alone 0.327).
- **The ceiling.** Both hold for **P(A) = 0.154** of the targets (binomial
  95%: 0.111–0.198). Hence LR ≤ 1/P(A) ≈ **6.5** (5.1–9.0). Over all 519
  spring conjunctions, P(A) = 0.148.
- **The components agree with the dossier.** Venus is a visible morning star
  on 43% of spring Day −5s [vis, table at l. 179]. With the dossier's
  stricter Mercury figure (17% within ±5 d of an event), P(A) ≈ 0.073 and
  the ceiling is about 14.
- **Among the 41 targets in A:**
  - B&M's V ∧ M (lead ≥ 90 min; \|Δ\| ≤ 1 d to the rise-azimuth maximum,
    approximated from declination) passes **5 of 41 = 0.12**;
  - 28 of 41 have a Mercury event within 6 d;
  - every one of the 5 targets that pass B&M's V and M satisfies A.
- **Consequence for the Bayes factor.** The Bayes factor that B&M's reading
  alone can give a target of T_A is at most about 41/5 ≈ 8 (5.7). That rests
  on r1's approximate M rule, so it is a rough figure.

**Pool sizes and attainable bounds** [me: `results/design-revision-r2/cp_bounds.py`,
`.out.txt`]:

- **Revision 2's pools.** Its core (−1748..−851, 898 years) holds about
  **478** spring daylight targets (r1 estimated about 480), and so about 74
  in T_A.
- **The floor.** With no target reached, the 95% upper bound on a G is
  3.69/n (the Fay–Feuer gamma interval and the Clopper–Pearson interval
  agree here, 5.3). For n = 74 that is **0.0499**, so a threshold of 0.05
  could be met only if not a single target were reached.
- **Revision 3's pools.** Its core (−1748..−51, 1,698 years, section 4.1)
  holds about **10,690** daylight conjunctions (T), **903** spring ones
  (T_C) and **139** in T_A (100–179 over P(A)'s interval). The floor for
  T_A is then **0.0265**. The second recheck measured 892 and 131 (2.9).
- **What these floors bound.** They bounded revision 3's outcome 1. That
  outcome needed G_BM,hi ≤ 0.05, and they showed only that the bound was not
  ruled out *when no target is reached*. The sky reaches about 26 targets,
  so the bound was ruled out after all [r2 R2-1]. Revision 4's outcome 1
  reads the held-out floor p_H,min instead (7.2).

**Other numbers already computed:**

- **The Sun's apparent longitude at four conjunctions** [r1:
  check_ranc_season.py]:
  - 16 Apr 1178 BC (10:09 UT): 14.28°;
  - 30 Sep 1131 BC (10:30 UT): **176.69°**;
  - 30 Oct 1207 BC (13:27 UT): 206.70°;
  - 12 Jan 1183 BC (07:46 UT): 282.20°.

  The autumnal equinox of −1130 fell on 3 Oct, 17:17 UT.
- **Arcturus' heliacal rising at Ithaki** (first morning on which Arcturus
  rises with the Sun at or below −AV; DE441, SMH2020) [me:
  `results/design-revision-r2/ranc_season.py`, `.out.txt`]:
  - in −1177: 9, 12 and 14 Sep at AV 8°, 10° and 12° (the dossier gives
    8–13 Sep [vis §3.3]);
  - in −1130: **10, 12 and 14 Sep**.

  30 Sep 1131 BC therefore lies 16–20 days after the vintage marker of
  Hesiod's farming calendar (*WD* 609–611) and 3 days before the astronomical autumn of
  Geminus. *Isagoge* 1.9 divides the year into four seasons at the
  equinoxes and solstices (the autumn clause sits in a lacuna), and 2.17
  says the seasons begin in the cardinal signs (local `geminus-grc.tsv`
  1.9.1, 2.17.1). It was total at Ithaki at canon ΔT, with the Sun
  at 51.6° (2.3).
- **I11(a)** holds at Troy (2.6).

### 2.9 Known from the recheck of revision 3, and from this revision's design-stage estimate

The recheck rebuilt the rule's pools and garden independently, with rough
methods [r2: check_gbm.py, check_slot_scaling.py, check_ranc_p19.py;
approximations in r2 §5]:

- rises on a 3-minute grid;
- Mercury's rise-azimuth maxima from the declination series, with a 3-point
  vertex;
- stations from the interpolated zero of the daily longitude change;
- conjunctions on DE441 with SMH2020 ΔT, at one site, Ithaki.

The bench recomputes every number below with its own code, and no
confirmation is counted.

**Pools and the C_rel calibration.**

- **C_rel calibration.** h_A = 2.04° and h_P = 0.92° reproduce A(−1177) =
  17 Feb and P(−1177) = 4 Apr. They give 11 Feb–31 Mar at −1700 and 22 Feb–6
  Apr at −700. h_P is a fit to B&M's printed bound, not a visibility: a star
  of magnitude 2.9 is not seen at 0.9° [r2 §1 #9].
- **Candidates.** 27,212 conjunctions in −1999..+200, of which 2,286 are
  spring candidates (C_rel on either count).
- **The core −1748..−51.**
  - n_TC = 892;
  - n_A = 131 under revision 3's slots, with the day counts paired;
  - so P(A | T_C) = 0.147.

  The design's estimates were 903, 139 and 0.154.
- **The identity of 4.2 holds.** No survivor of any of the 36 readings lies
  outside revision 3's slots.

**G over T_A** (W = 136 years, the Fay–Feuer interval of 5.3):

| readings | G | 95% interval | targets reached |
|---|---|---|---|
| T0b's reading alone (sequential, MWRA_vtx ±1.5 d, visibility off) | 0.020 | 0.004–0.061 | 4 / 131 |
| sequential MWRA, all tolerances (6) | 0.032 | 0.012–0.076 | 10 / 131 |
| sequential, all events (18) | 0.121 | 0.073–0.192 | 25 / 131 |
| **𝒢_BM*** (36) | **0.140** | **0.087–0.215** | 26 / 131 |

- **Stationarity.** The two halves of the core give 0.130 and 0.152; a
  shorter run, −1760..−640, gives 0.158 (0.082–0.277).
- **Shape.** Half of the reached targets have reach exactly 1.0.
- **What dominates.** The union is dominated by the GWE and station readings,
  which the recheck's method locates well.
- **The other pools.** G over T_C is 0.0206, and G_BM,u = (n_A/n_T) G_BM ≈
  **0.00172** with n_T ≈ 10,690.
- **What this means.** G_BM does not depend on any measurement of the
  Odyssey. Even T0b's single reading has an upper bound of 0.061, so no
  threshold of 0.05 on G over T_A can be met [r2 R2-1].

**The slot definitions set G_BM** [r2 R2-2; r2: check_slot_scaling.py]. The
same 26 targets are reached under every definition, so G scales as 1/n_A.
The variants are frozen as the family of 4.2:

| variant (4.2) | n_A | G_BM | 95% |
|---|---|---|---|
| v0 documented: Venus visible (AV 7°); Mercury event ≤ 6 d **and** visible | 82 | 0.224 | 0.139–0.344 |
| v1 revision 3: Venus AV 7°; Mercury event ≤ 6 d **or** visible | 131 | 0.140 | 0.087–0.215 |
| v2: Venus AV 7°; Mercury event ≤ 6 d | 87 | 0.211 | 0.131–0.324 |
| v3: Venus AV 7°; Mercury event ≤ 4 d | 66 | 0.278 | 0.172–0.427 |
| v4: Venus lead ≥ 60 min; Mercury as v1 | 101 | 0.182 | 0.112–0.279 |
| v5: Venus lead ≥ 60 min; Mercury event ≤ 4 d | 56 | 0.327 | **0.203**–0.504 |

The smallest lower bound is 0.087, under v1. Only v5 alone would fire
label 2's G leg (lower bound ≥ 0.20). Every variant gives the same G_BM,u,
0.00171–0.00172 [me: `results/design-revision-r3/synth_sets.py`, `.out.txt`].

**The target under 𝒢_BM*** [r2 R2-3].

- **Which readings it passes.** 16 Apr 1178 BC passes only the six
  sequential MWRA readings. It fails the GWE and station readings at
  ≤ 3.5 d: the station is on 5 Mar and GWE on 19 Mar, against Day −34 =
  13 Mar [vis §2.3]. It also fails every parallel reading.
- **Its reach.** The only survivors of the T0b reading in −1260..−1040 are
  18 Mar 1189 BC and 16 Apr 1178 BC. So r_Ody = 11/136 = **0.0815**, and
  19.8% of T_A targets reach at least that much.
- **The near misses** both survive the 2.5-d and 3.5-d readings. That is why
  the union reach equals the 1.5-d reach:
  - 26 Mar 1111 BC, lead 97 min, ΔMWRA 2.27 d;
  - 2 Apr 1098 BC, lead 108 min, ΔMWRA 2.49 d.
- **How firm it is.** The 1111 BC case lies within the recheck's accuracy
  of about 1 d at a flat maximum. At the bench's exact vertex r_Ody could be
  0, which is label 2's "no match" form. Both branches are reported (5.4).

**Rates and the Bayes factor** [r2: check_gbm.py]:

- **Survivors per century.** T0b's reading gives λ = 0.55 per century over
  −1999..+200 (0.71 over −1760..−640). That means about 12 survivors, and a
  Poisson P(≥ 1 in 136 years) of 0.53. The 36 readings give 0.27–1.77 per
  century each.
- **P_spring** (sequential, all candidates, n = 2,204):
  - P(V) = 0.198;
  - P(M, MWRA_vtx ±1.5 d) = 0.036;
  - p_fix|C = P(V ∧ M) = 0.0054;
  - the V–M dependence ratio is 0.76.
- **The Bayes factor.** BF_BM(ρ = 1) ≈ 2.6, with BF_max ≈ 20.7.
- **P(unique)** over the T0b-reading passers in T_A is 0.647, on n = 4.
- **The visibility fork never separates.** Among spring Day −34s within
  3.5 d of a morning event, every one is visible at AV 10°. So 18 of the 36
  readings duplicate the other 18 [r2 §1 #7].

**R_anc with the eclipse clue** [r2: check_ranc_p19.py]. In NASA's Ithaca
site catalogue at canon ΔT there are 9 conjunctions in −1249..−1114 between
12 Sep and 31 Mar with smag ≥ 0.6 and the Sun ≥ 10°:

- 20 Dec 1247 BC;
- 14 Mar 1232 BC;
- 5 Mar 1223 BC;
- 30 Oct 1207 BC;
- 9 Oct 1197 BC;
- 21 Jan 1192 BC;
- 23 Feb 1138 BC;
- 30 Sep 1131 BC;
- 14 Feb 1129 BC.

So R_anc dates nothing in B&M's window, even with its eclipse.

**Prereg files** [r2 §4]:

- every licence string occurs verbatim in its cited row: 125/125 in
  `controls_real.json` and 54/54 in `controls_almagest.json`;
- the only date-like strings outside licence words are the Roman calendar
  names that Livy gives;
- the three clue-file hashes matched revision 4's 12.4. The round-2 licence
  checks have since changed two of the files; their new hashes are in 12.4.

**The held-out null, estimated for revision 4 and extended in revision 5**
[me: `results/design-revision-r3/heldout_attain.py`, `.out.txt`, `.json`;
`results/design-revision-v5/heldout_strata.py`, `.out.txt`, `.json`].

- **How the target was kept out.** The script removes 16 Apr 1178 BC from
  r2's candidate rows before it computes anything, and asserts that no
  predicate is evaluated on it.
- **The predicates.** H3 and H4 are revision 1's: Mercury within ±3 d of a
  conjunction with the Sun around Day 0/+1 and not visible; Venus–Mars
  ≤ 5° within ±3 d of Day −7 (section 7).
- **Approximations.** Visibility is approximated by an elongation below 10°,
  sampling is daily, and the rows are r2's rough candidates.
- **What has not been done.** No note, review or design revision has
  evaluated H3 or H4 at the target. A search of `docs/` and `results/` finds
  no such computation.

| null pool (whole background, target excluded) | n | q3 (H3) | q4 (H4) | pass both | p_H,min = (1 + both)/(1 + n) | p if the target passed H4 only | p if H3 only |
|---|---|---|---|---|---|---|---|
| **P_BM**: candidates passing some reading of 𝒢_BM* (a rule pool, 7.2) | 76 | 0.197 | 0.026 | 1 | **0.026** | 0.039 | 0.221 |
| **P_MWRA**: candidates passing some MWRA reading of 𝒢_BM* (a rule pool, revision 5, 7.2) | 43 | 0.186 | 0.023 | 0 | **0.023** | 0.045 | 0.227 |
| **the rule, max over the two pools** | | | | | **0.026** | **0.045** | **0.227** |
| T_A under v1, daylight (sensitivity) | 169 | 0.237 | 0.041 | 1 | 0.012 | 0.047 | 0.241 |
| T_A under v0, daylight (sensitivity) | 108 | 0.222 | 0.037 | 0 | 0.009 | 0.046 | 0.229 |

The P_MWRA row and the "max" row are revision 5's [me:
`results/design-revision-v5/heldout_strata.py`, `.out.txt`, `.json`]. That
script is revision 4's `heldout_attain.py` with the pools split by Mercury
event. It removes the target before it computes anything, as revision 4's
did, and it uses the same rough rows and predicates. The "p if H3 only"
entries count the members that pass H4 alone, which outrank a target that
passes H3 alone: (1 + 15 + 1)/77 = 0.221 on P_BM and (1 + 8 + 1)/44 = 0.227
on P_MWRA. Revision 4's script printed 0.208 for P_BM because it left that
member out; revision 4's text already gave the right 0.221 [me].

**Is P_BM homogeneous?** Revision 5 asked whether H3 and H4 pass at
different rates among the candidates admitted through different Mercury
events. On the rough rows they do not [me: `heldout_strata.out.txt`]:

| class of P_BM member | n | H3 | H4 |
|---|---|---|---|
| passes some MWRA reading (= P_MWRA) | 43 | 8 (0.186) | 1 |
| passes only GWE or station readings | 33 | 7 (0.212) | 1 |

Fisher's exact test on H3 gives p = 0.78. The one member that passes both
predicates lies in the GWE/station class. The bench repeats this check with
its own code (R20) and reports it.

**The order of these choices is recorded.**

- Revision 4 defined the three pools of its table before its script ran.
- Revision 4 chose P_BM because it compares the target with candidates that
  pass the same readings [rev #11 fix 1]. Of its three pools it is the least
  favourable to a "yes".
- Revision 5 added P_MWRA, because the target passes only MWRA readings
  (2.9, "the target under 𝒢_BM*"). P_MWRA is literally issue 11's "same N,
  C, V and M". The rule reads the larger p of the two pools (7.2), so adding
  a pool can only make a "yes" harder. The decision was taken with the
  design-stage null of both pools in view, and with no target-side value of
  H3 or H4 computed by anyone.
- H3 and H4 have been frozen since revision 1 (2026-10-03). The score and
  P_BM date from revision 4, and P_MWRA and the max rule from revision 5.

### 2.10 What the known numbers already imply for the verdict

Nothing in this list is a prediction, and the bench recomputes every item
with its own code. The point of the list is that no reader should mistake
any of these items, when they come out as expected, for a finding of the
bench.

- **Outcome 1 is attainable.** p_H,min is about 0.026, the larger of the
  two rule pools' floors (P_BM 0.026, P_MWRA 0.023), and 0.009–0.012 on the
  sensitivity pools (2.9). The rule can say "yes" for a target whose sky
  matches the unfitted clues: by passing both, or H4 alone (p_H 0.045). The
  synthetic set S1 of 9.5 is built from these null-side estimates
  (constraint C7).
- **Outcome 1 is not expected for the Odyssey.** H4 is expected to fail at
  1178 BC. This is an inference from two documented facts, not a
  computation:
  - Venus stood 44.3° west of the Sun on 11 Apr −1177 [unread §2.5];
  - Mars was invisible through March and April 1178 BC except during the
    eclipse, B&M's own observation after the fact [bm §2]. That puts Mars
    near the Sun, more than 20° from Venus.

  If H4 fails, p_H is at best about 0.23 (H3 alone) and otherwise 1. H3 and
  H4 are first evaluated at the target after the second freeze (12).
- **T0_pass is expected to hold, and T0 is expected to be RE.** 16 Apr
  1178 BC passes N, C, V and M, and so does 18 Mar 1189 BC (2.2, 2.9).
- **Label 2's G leg is not expected to fire.** The smallest lower bound over
  the slot family is 0.087. It would fire under v5 alone, so **Q_slot is
  expected**. The pct_N4 leg is open. The "no match" form turns on the
  status of 26 Mar 1111 BC at the bench's exact vertex (2.9), and both
  branches are reported (5.4).
- **Q_tol is expected.** G_BM,lo exceeds 0.05 under every slot definition
  (the lowest is 0.087). So B&M's own readings could not have dated any
  target at 5%, whatever the sky of 1178 BC. In the recheck's words, they
  make about one conditioned spring target in five "unique".
- **Q_BM holds** (2.6).
- **Gate 3b** retains the truth in 9 of 11 sets (2.6). Only narrowing is
  open.
- **Q_H needs 6 of 8.** Three counted *Almagest* sets have no held-out row,
  so held_ALM ≤ 8 (2.6, 6.4).
- **Outcome 4 is attainable.** G_BM,u ≈ 0.0017 is above U0(10,690) =
  0.00035 [r2 §4].
- **The words' evidential ceiling** is about 6.5 for blind categorical
  readings. It is 1 once those readings are conditioned on, because the
  record shows that they were formed with the target in view (5.7).
- **So, on known numbers, the expected verdict is:**
  - no label 1;
  - label 2, or inconclusive, depending on pct_N4 and r_Ody;
  - 3a, 3b and 4 open;
  - Q_BM, Q_tol and Q_slot expected.

  This expectation is not a prediction, and it is never counted as a
  success.

---

## 3. T0: reproduction

### 3.1 T0a: replay of Table S2 (done)

T0a is complete (2.2). It becomes the regression test `tests/test_t0.py`,
which replays S2's printed values and colours, so that every later change to
the rules is checked against the published table.

### 3.2 T0b: B&M's search recomputed with DE441

T0b reproduces B&M's procedure as written, on DE441, with their clock. It uses
DE441 for the Moon as well, because that is the pairing on which the S2
agreement of 2.2 was measured; the bench proper uses the pairing rule of
section 0, and prediction P2 checks that the T0b survivor set does not move
under it. The steps:

1. **Candidates.** Every geocentric conjunction in apparent ecliptic
   longitude whose UT+2 instant falls in the half-open window
   [−1249 Jan 1 00:00 UT+2, −1113 Jan 1 00:00 UT+2), i.e. through 24:00 UT+2
   on 31 Dec −1114, computed as
   `calendar.span_bounds((-1249,1,1), (-1114,12,31), offset_hours=2)`.
   UT = TT − 27,602.7 s. Expected count 1,683 [rev #22; R6].
2. **Ti** is the UT+2 civil date of the conjunction.
3. **C (fixed Julian).** Ti−29 ≥ 17 Feb and Ti−12 ≤ 4 Apr of the same Julian
   year, with true Julian day arithmetic (29 Feb counted). Where two New
   Moons in a year pass, both are evaluated (S2 lists one by no consistent
   rule [bm §7]).
4. **V.** On Ti−5: Venus a morning object rising ≥ 90.0 min before the Sun.
5. **M.** Every morning over Ti−34 ± 60 d: Mercury's azimuth (north through
   east) at its rising instant, with rise times bisected until converged to
   better than 0.1 s [rev #12 fix 2]. Two definitions are computed:
   - **MWRA_vtx (primary):** the vertex of a least-squares parabola through
     the daily azimuths of the 7 mornings centred on the discrete local
     maximum nearest Ti−34; Δ = (Mercury's rising instant on Ti−34) − (vertex
     instant), continuous, in days [rev #12 fix 1].
   - **MWRA_int (B&M literal):** the civil date of that discrete maximum;
     Δ = (Ti−34) − MWRA_int in whole days; equidistant maxima resolve to the
     earlier.

   Pass if \|Δ\| ≤ 1.5 d for MWRA_vtx, B&M's integer tolerance of 1 day
   as a continuous one: a vertex lies within half a day of its discrete
   maximum [r1 N13]; ±1 d is reported beside it. Pass if \|Δ\| ≤ 1 for
   MWRA_int. Every maximum records its curvature (deg/d²) and its
   margin over the larger neighbouring day; it is flagged **flat** if the
   margin is below 0.001° or the curvature below 0.002°/d² [rev #12 fix 3].
   Mercury's visibility on Ti−34 is recorded three ways: Sun at Mercury's
   rising ≤ −10° (Ptolemy's AV [vis §2.2]); PLSV's AV = 10.5 + 1.4m at a 1°
   critical altitude (the defaults B&M's software used [unread §6]); and not
   required (S2 never tabulated it [bm §5 M]).
6. **E** (reported, not applied): 1 Apr ≤ Ti−11 ≤ 4, 5 or 6 Apr, and the
   computed equinox date.
7. **Parallel reckoning** (reported): steps 3–6 at −28/−12…−11, −4, −33,
   −10 [B&M Table 1].
8. **Output** an S2-shaped table for every candidate
   (`results/t0/candidates.tsv`), the survivor sets of every criterion and
   combination, and the 1178 BC row.
9. **Comparison with S2**: Ti agreement by zone, Venus pass-set equality,
   MWRA agreement (exact and ±1 d), Δ agreement, leap-day effects.
10. **M sensitivity** [rev #12 fix 4]: the M pass set under h0 ± 0.1°,
    latitude 38.2°–38.6° in 0.1° steps, refraction on and off, and the clock
    ΔT ± 720 s.

| parameter | value | source |
|---|---|---|
| planets, Sun, Moon | DE441, `data/ephem/de441_m2060_p0241.bsp` (the shortest covering excerpt is used, with bit-identical records) | [acq §1] |
| precession, sidereal time | Vondrák 2011 long-term model, module default | [eph §3] |
| site | `bm`: 38.4°N 20.7°E, sea level | S2 clock fit [bm §3.2] |
| clock | UT+2 | S2 sunrise − DE441 UT sunrise = +120.0 min, sd 1.6, n = 75 [bm §3.2] |
| ΔT (clock only) | 27,602.7 s, constant | [B&M §Method; bm §3.1] |
| rise definition | airless geometric altitude of the centre at h0 = −0.8333° (Sun) and −0.5667° (planets) | settings that reproduce S2 [bm §3.2] |
| New Moon | apparent ecliptic-longitude conjunction, UT+2 civil date | 136/152 [bm §5 N] |
| window | half-open UT+2 bounds above | [B&M §Method; rev #22] |
| C bounds | Ti−29 ≥ 17 Feb, Ti−12 ≤ 4 Apr (fixed Julian; T0b only) | [bm §5 C; rev #9] |
| V threshold | lead ≥ 90.0 min on Ti−5 | [B&M §References; bm §5 V] |
| M event | MWRA_vtx (primary), MWRA_int (literal) | [rev #12] |
| M tolerance | MWRA_vtx \|Δ\| ≤ 1.5 d (±1, ±2.5, ±3.5 reported); MWRA_int \|Δ\| ≤ 1 (2, 3 reported) | S2 colours [bm §5 M]; continuous equivalent [r1 N13] |
| M visibility | off, AV 10°, PLSV | [rev #23; unread §6] |
| day arithmetic | true Julian (`odybench.calendar`); S2's 365-day arithmetic reported beside it | [bm §5 M] |
| E | 1 Apr ≤ Ti−11 ≤ 4 / 5 / 6 Apr | [B&M §References, §Intersecting; rev #23] |
| offsets | sequential 0, −5, −11, −12, −29, −34 | [B&M Table 1] |

### 3.3 T0c: the eclipse statements

For 16 Apr 1178 BC (−1177) the bench computes local circumstances at the
five Ionian sites under each pairing and the constant-ΔT window for totality:

| pairing | why |
|---|---|
| NASA 5MCSE elements, canon ΔT 28,590 s | the canon B&M quote |
| DE431 + each SMH model (SMH2020, Addendum parabola, SMH2016 parabola) | SMH's ΔT is tied to the DE430 lunar model |
| NASA elements + Espenak–Meeus canon form | its own pairing |
| DE441 + SMH2020 | the bench's planetary ephemeris, reported beside |
| DE441 + 27,602.7 s | what B&M printed; mixes ephemerides, reported only to show it |

Values already known are in 2.3. The canon identity (catalogue 01966, Saros
39 member 31) is A5. On B&M's statement that Ithaca lay on the edge of
totality: **consistent** if Ithaki is total for some ΔT within 1σ of the
SMH2020 value in the DE431 pairing (known: +0.3σ to +1.4σ, so consistent);
B&M's own 27,602.7 s is **uninterpretable** for eclipse geometry (2.3).

### 3.4 Regression checks

These thresholds were set at values already measured, so they are labelled
what they are: **regression tests** that the code reproduces known numbers.
They do not test whether DE441 agrees with B&M's software [rev #20].

| check | pass | measured |
|---|---|---|
| A1 Ti | DE441 UT+2 conjunction dates match S2's Ti in ≥ 134 of 152 rows | 136 [bm §5 N] |
| A2 Venus | DE441 pass set on S2's own Ti equals S2's orange set; S2 lead times reproduced with sd ≤ 3 min | 25/25; sd 1.5 min [bm §3.2, §5 V] |
| A3 MWRA | ≥ 124/152 exact and ≥ 138/152 within ±1 d (integer definition) | 124 and 138 [bm §5 M] |
| A4 1178 BC values | Venus lead 103.6 ± 1 min; conjunctions 18 Mar 03:31 and 16 Apr 12:25 UT+2; equinox within 10 min of B&M's 15:24; Sun at −12° on 18 Mar within 5 min of B&M's 19:38 | 103.6; 03:31, 12:25; 15:31; 19:34 [bm §3.2, §9] |
| A5 canon identity | catalogue entry and greatest-eclipse point as in 2.3 | matched [rev V4] |

### 3.5 The T0 verdict

T0 is computed on a grid: E bound ∈ {≤ 4, ≤ 5, ≤ 6 Apr} × Mercury visibility
∈ {off, AV 10°, PLSV} × MWRA ∈ {vtx, int} [rev #23]. In every cell:

- **R, reproduced as stated:** 16 Apr 1178 BC passes N, C, V and M and is the
  only candidate that does.
- **RE, reproduced only with the equinox:** not R, and 1178 BC is the only
  candidate passing N, C, V, M and E.
- **NR, not reproduced:** neither; the report names the failing criterion
  and its margin.

The **primary cell** is E ≤ 5 Apr (B&M's §References), visibility off (S2's
table), MWRA_vtx at ±1.5 d. The whole grid is reported. Expected (R5): RE in
the primary cell, NR under E ≤ 4 Apr.

**T0_pass**, the quantity the decision rule reads, is true when 16 Apr
1178 BC passes N, C, V and M (E off) in the primary cell.

- **Why only the target's part counts.** T0_pass is the part of the
  reproduction that depends on the target's own sky.
  - Whether the target is also the only candidate (R or RE) depends on the
    other candidates' skies.
  - Its evidential value is what G prices (5.3), so it is reported, and it
    enters no rule.
- **Why revision 3's rule was changed.** Revision 3 required T0 = R for
  outcome 1 [r1 N6 fix 3]. That made outcome 1 unattainable on known facts
  alone: 18 Mar 1189 BC passes N, C, V and M whatever the Odyssey encodes
  (2.2) [r2 R2-1].
- **E still counts for nothing.** T0_pass uses no equinox clue, so the
  uniqueness that holds only with MacDonald's eclipse-fitted equinox reading
  (RE) still earns nothing [r1 N6 fix 3].
- **Expected:** T0_pass true and T0 = RE (2.10).

---

## 4. Shared machinery

### 4.1 Spans and coverage

- **Background** B = −1999-01-01 to +200-12-31 (2,200 Julian years).
  - It starts with the first year of NASA's elements [acq §2.1]. Every
    ephemeris, element and star file needed is already on disk (DE441 and
    DE431 to +241, NASA elements to +300 [acq §1.1, §2.1]).
  - Revision 2's background ended at −600. Its conditioned target pool would
    then hold about 74 targets (2.8) [r1 N8]. Extending the background to
    +200 nearly doubles every pool. That narrows G's interval and gives the
    held-out test null pools of about 76 and 43 candidates (7.2).
  - **The cost is stationarity.** Precession moves the star season about 31
    days against the equinox over 2,200 years. P8 tests the rates, and 5.3
    reports G on each half of the core.
- **Data margins** −2060..+241, covering the 40-day clue offsets and the
  ±60-day Mercury searches.
- **Target core** −1748..−51. Targets must lie at least 251 years inside B
  so that every window of every width lies inside it. One core serves all
  widths, so gardens of different widths share their targets. The core
  contains 1312, 1178 and 1131 BC.
- **Controls.** Every control window lies inside −1999..+300; the exact
  span each kind needs is truth-side [AppT 7]. DE441 and DE431 are extended
  to +300 before the controls run (11.1).
- **Per-site spans** are in `data/prereg/sites.json` [r1 N12]. Only Ithaki
  needs every column over the whole span. Each negative-control site needs
  the background, but only the columns its sets use. Each control site needs
  only the union of its 21 window positions.

### 4.2 Candidate pools and target pools (Ithaki unless a rule names another site)

**Candidate pools.**

- **P_all** holds every geocentric apparent-longitude conjunction, computed
  with DE431 in yearly chunks and SMH2020 ΔT for UT. Each candidate carries
  **one Day-0 date per clock**: `day0_jdn_ut2` (B&M's clock; F2 (a)) and
  `day0_jdn_lmt` (F2 (b), the negatives, R_anc) [r1 N12].
- **P_day** holds the conjunctions whose instant falls in daylight at the
  site (Sun's centre above −0.8333°). At Ithaca that is 50.9% of them [vis
  §4.2], and only these can give a visible solar eclipse.
- **P_spring** holds the conjunctions passing C_rel (4.5) on the sequential
  or the parallel count, with Day 0 the UT+2 date. The slots below use the
  same Day 0 and the same count, so that the identity at the end of this
  section is exact.
- **P_BM** holds the candidates of P_all, over the whole background, that
  pass at least one reading of 𝒢_BM*. It is a null pool of the held-out
  test (section 7).
- **P_MWRA** (revision 5) holds the candidates of P_BM that pass at least one
  of 𝒢_BM*'s twelve MWRA readings: the rise-azimuth maximum, the Mercury
  event B&M applied and the only one the target passes (2.9). It is the
  held-out test's second, matched null pool (7.2). Both pools are built from
  the masked pool at the null-side stage.

**The masked target.** In the null-side stage (12.3) every pool is built
without 16 Apr −1177. `pools.targets(..., mask_target=True)` removes it
before any predicate is evaluated, and `clues.evaluate` raises if asked to
evaluate it (I13(g)).

**Target pools.** Section 5.3 says which pool each G uses, and why.

| pool | definition | size in the core (estimate, 2.9) |
|---|---|---|
| T | P_day ∩ core | about 10,690 |
| T_C | T ∩ P_spring | 892 |
| T_A(v) | the targets in T_C whose sky satisfies the Venus slot and the Mercury slot of variant v, on the same day count as C | 56–131 by variant (table below) |

**The slot family** (`data/prereg/slots.json`) [r2 R2-2]. A slot defines the
*categorical* reading that the record shows was formed with the target in
view (5.3). The recheck showed that the slot definition sets G_BM through
1/n_A. Nothing in the record fixes a width, so the bench freezes a family and
uses it against the claim being made.

| key | Venus slot (Day −5 seq, −4 par) | Mercury slot (Day −34 seq, −33 par) | source | n_A (2.9) |
|---|---|---|---|---|
| v0, documented | Venus rises before the Sun, with the Sun at or below −7° at Venus' rising (a visible morning star, AV 7°) | Mercury within 6.0 d (continuous) of a morning rise-azimuth maximum (vertex, 4.3), a greatest western elongation, or a morning station, **and** visible (Sun at or below −10° at Mercury's rising) | V: MacDonald identifies the herald as Venus, the morning star of that spring [unread §2.1, §2.5], with de Jong's AV [vis §1.2]. M: B&M name the three events and require Mercury visible [B&M §References]; 6 d is the slack of Ptolemy's Mercury records, all 14 within 5.5 d [alm §4] | 82 |
| v1, revision 3 | as v0 | event within 6.0 d, **or** visible | [v3 §4.2] | 131 |
| v2 | as v0 | event within 6.0 d | | 87 |
| v3 | as v0 | event within 4.0 d (12 of the 14 *Almagest* records) | [alm §4] | 66 |
| v4 | Venus rises at least 60 min before the Sun | as v1 | the FULL-tier herald threshold [vis §1.3] | 101 |
| v5 | as v4 | as v3 | | 56 |

- **Pairing of the day counts** [r2 R2-2]. C, the Venus slot and the Mercury
  slot hold on one count: either the sequential count (−29/−12, −5, −34) or
  the parallel count (−28/−11, −4, −33). A target is in T_A(v) if either
  count passes as a whole. Revision 3's "either day count" let Day −5 mix
  with Day −33; that is withdrawn.
- **"Near greatest elongation" is not MacDonald's wording.** Revision 3
  wrote that MacDonald puts Venus "near morning elongation" [v3 §5.3], and
  the recheck took that as his categorical reading [r2 R2-2].
  - His p. 327 dates the greatest morning elongation, 17 March, and says no
    more [unread §2.1].
  - On 11 Apr −1177 Venus stood 44.3° west of the Sun. That was 1.84° below
    the apparition's maximum of 46.14°, and 26 days after it [unread §2.5].
  - A Venus slot narrower than that would exclude MacDonald's own case.
  - The variant "western elongation within 2° of the apparition's maximum"
    (v6) is reported. It is not in the rule family, because its width is set
    by the target's own value.
- **How the family is used.**
  - Label 2's G leg and Q_tol take the variant most favourable to B&M, the
    smallest G_BM,lo.
  - Q_slot is printed when a decision differs between variants.
  - The held-out test does not use T_A (section 7), so outcome 1 does not
    depend on the slots.

**One identity follows.** Every reading of 𝒢_BM* requires three things:

- C;
- a Venus lead of at least 90 min. That implies the Venus slots of every
  variant: at Ithaca's latitude the Sun sinks at least about 0.15° a minute
  near the horizon, so a 90-min lead puts it below −13° when Venus rises
  [me];
- a morning Mercury event within 3.5 d. That implies the Mercury slots of v1
  to v5.

So no target outside T_A(v) is ever reached, for v1 to v5, and

  G(𝒢_BM*, T) = (n_A(v) / n_T) · G(𝒢_BM*, T_A(v)) = G_BM,u

exactly, the same number for every such v. For v0 the visibility part is not
implied by the readings with visibility off. The recheck found no reached
target outside T_A(v0) [r2 R2-2], and the bench reports that count. I9(c)
checks the identity in the code, and I14 uses it as a realisability
constraint (9.4).

### 4.3 Sky tables and events

Every daily quantity the clues need is tabulated once per site over the
span, by `odybench/sky.py`, and the events derived from them by
`odybench/events.py` (interfaces in 10.2): rise and set times and azimuths
of the Sun, Moon, Mercury, Venus, Mars, Jupiter and Saturn; Sun altitude at
each planet's rising and setting; signed elongation; V magnitude; ecliptic
longitude and latitude; civil, nautical and astronomical twilight; the
altitudes of the grammar stars (Alcyone, Arcturus, Sirius, Aldebaran,
Betelgeuse, Rigel, Dubhe, and the Hyades, Orion and Boötes extras of
`data/stars.json`) at the end and start of nautical twilight, and their rise
and set times; the Moon's illuminated fraction and its share of the dark
hours above the horizon; night length. From these: stations, greatest
elongations (from the true and the mean Sun), oppositions, rise- and
set-azimuth extrema (parabola vertex, as in T0b), first and last visibility
at the AV values of the forks, heliacal star phases, equinoxes and
solstices, conjunctions, full moons, and the first-crescent evening by
Yallop's q-test [vis §4.2]. None of these derived events has yet been
validated against anything; instrument checks I5, I6 and I12 do that
[rev #13].

### 4.4 Eclipse hit strength (replaces the classes X1–X4)

Revision 1's binary classes were defined around the target and estimated
from it: in −1499..−600 its class X1 held three events, of which only the
target was a spring new moon [rev #10]. The bench now uses a probability.
For a conjunction u and a site s, h = 0 if u is not a solar eclipse; else:

- **h_tot(u, s)** = P(the eclipse is total at s, with maximum in daylight),
  under the four-model ΔT mixture, integrating each model's Gaussian over the
  totality window computed on NASA's elements in the canon frame;
- **h_09(u, s)** = mixture P(smag ≥ 0.9, Sun up at maximum);
- **h_06(u, s)** = mixture P(smag ≥ 0.6, Sun ≥ 10° at maximum), the darkness
  that the wording of Hdt. 9.10 and Plut. *Pel.* 31 went with [ctl §0 item 3].

**M_Ody** := h_tot(16 Apr −1177, ithaki), the Odyssey's own eclipse strength
(0.304 on the known numbers; recomputed by `eclipses.py`). Wherever the
decision rule asks for an eclipse "at least as strong as the Odyssey's", it
means h_tot ≥ M_Ody.

Reported beside, never in the rule: the time-of-day variants (maximum
10–12 h LAT, which is Schoch's rule [unread §3.1], and 10–14 h LAT), and
revision 1's envelope classes "total for some ΔT within ±0.5σ, ±1σ, ±2σ"
[rev #10 fix 4]. Base rates: p_e(m) is the fraction of P_day conjunctions in
the background with h_tot ≥ m, with **the target itself excluded** from every
base rate it is compared with [rev #10 fix 3], and a site-rotated estimate at
Ithaki's latitude over 36 longitudes, which does not depend on Ithaca's
particular eclipses [rev #10 fix 2].

### 4.5 Season and equinox bounds relative to each year's sky

B&M's fixed Julian cut-offs drift: the Julian year runs about 0.76 d per
century ahead of the equinox, and the star phases drift about 0.64 d per
century the other way [rev #9]. Outside T0b every season and equinox bound is
computed for each year:

- **C_rel (B&M-calibrated).** For each Julian year y, A(y) is the first
  evening on which Arcturus stands at least h_A high at the end of evening
  nautical twilight (Sun −12°), and P(y) the last evening on which Alcyone
  stands at least h_P high then. h_A and h_P are fixed once, so that
  A(−1177) = 17 Feb and P(−1177) = 4 Apr, B&M's applied bounds [bm §5 C]; if a
  range of values gives the date, its midpoint is taken. C_rel passes if
  Ti−29 ≥ A(y) and Ti−12 ≤ P(y). The calibration fits B&M's printed bounds,
  not a sky outcome, and it makes C_rel identical to the fixed bounds at
  −1177 (at 2° the Pleiades' last evening is 3 Apr, which would drop 1178 BC
  by a day [vis §3.3, §4.3]; that reading is fork F3(b)).
- **E_rel.** Ti−11 lies in [eq(y), eq(y) + n] days, eq(y) being the civil
  date of the computed March equinox (apparent solar longitude 0°), with
  n ∈ {3, 4, 5}, matching ≤ 4, 5 and 6 Apr at −1177, where the equinox falls
  on 1 Apr [bm §9].
- N1 reports λ per century under both the relative and the fixed bounds
  (P8).

### 4.6 Windows

In `data/prereg/windows.json`: reproduction 1250–1115 BC (−1249..−1114,
136 years, half-open UT+2 bounds); primary 1350–1100 BC (−1349..−1099,
251 years); Troy VIIa 1240–1150 BC (−1239..−1149, 91 years); strict
Eratosthenes return 1176–1172 BC (−1175..−1171); background as 4.1 [win §9].
A window of width W years is the half-open JD interval [a, a + 365.25 W).
Control window positions come from `data/prereg/seeds.json`.

---

## 5. Null models

### 5.1 N1: how often B&M's criteria pass by chance

1. Evaluate the **B&M reading** on every candidate in the background: B&M's
   criteria with C_rel and E_rel (4.5), MWRA_vtx at ±1.5 d, SMH2020 ΔT,
   site `ithaki`.
2. **Rate.** λ = survivors per century, with a Poisson 95% interval, for
   N ∧ C ∧ V ∧ M and for N ∧ C ∧ V ∧ M ∧ E (n = 3, 4, 5).
3. **Two comparisons with B&M** [rev #5]:
   - λ(N ∧ C ∧ V ∧ M ∧ E) against B&M's printed 0.048 per century: B&M as
     written (P4);
   - λ(N ∧ C ∧ V ∧ M) against B&M's own arithmetic redone at their stated
     ±1-day tolerance, 0.88 per century (R13; the known rate sits near the
     lower bound of a factor 2, so it is a regression expectation [r2
     R2-5]).
4. **Stationarity.** λ per century for each of the 22 centuries of the
   background, under C_rel and E_rel and under the fixed Julian bounds
   (P8).
5. **Windows.** Slide windows of W = 50, 91, 100, 136, 200, 251, 500 and 900
   years along the background one year at a time; report the empirical
   P(≥ 1 survivor) and the mean count beside the Poisson values. Venus' 8-year
   cycle and Mercury's 13- and 46-year near-repeats cluster survivors; the
   empirical figure includes that, and P5 predicts that it falls below the
   Poisson value.
6. **Per-target rates** [rev #6]. **p_fix|C** (primary) = the fraction of
   P_spring passing V and M: the chance that a target fixed in advance passes
   criteria fixed in advance, given the season. **p_fix** (unconditional) =
   P(C ∧ V ∧ M) over P_all, reported as the counterfactual "C independent of
   the target". The reason for making the conditional figure primary is
   frozen here: the spring reading of C first appears in MacDonald 1967, in a
   paper that already holds the eclipse and fits its timetable to it, and
   before Schoch every season reading was autumn or winter [unread §2.4];
   nothing documents an eclipse-blind spring reading. The same reason applies
   to V, M and E, and 5.3 applies it to all four [r1 N6].
7. **Independence.** B&M multiply marginal rates [bm §10]. The joint pass
   count of V and M on P_spring is compared with the product of the
   marginals; the null distribution permutes the Venus outcome among
   candidates with the same Ti day of year (± 3 d), 10,000 times.
8. **Without N.** Repeated with Day 0 any day, to show what N contributes.

### 5.2 N2: the eclipse coincidence

The question: if the criteria had nothing to do with eclipses, how often
would a date they pick be an eclipse new moon at least as strong as the
Odyssey's?

1. **Base rates** p_e(m) over P_day and P_spring, for m = M_Ody and as a
   curve over m (4.4). The pool is new moons, never days: an eclipse can
   only fall on one, and using days would inflate the coincidence about
   29.5-fold [v1 §3.3].
2. **Fixed reading, target first:** P(a target with h_tot ≥ M_Ody passes V and
   M | C) = p_fix|C, under the independence of item 4.
3. **Fixed reading, survivors first:** with s survivors in a window holding n
   candidates, P(≥ 1 survivor with h_tot ≥ m) by the hypergeometric tail, and
   its h-weighted analogue Σ over survivors of h_tot.
4. **Independence of clues and eclipse status.** No clue involves the lunar
   node, so V and M outcomes should not depend on eclipse status once the
   pool is spring new moons. N2 tests this: V and M pass rates on
   eclipse (h_tot > 0 at any of the five Ionian sites) and non-eclipse spring
   new moons, by permutation (P10). Every analytic shortcut below (5.4, 5.7)
   rests on this check.
5. **Background double hits:** survivors of the B&M reading with h_tot ≥ m
   at Ithaki, per century, beside the count expected from the site-rotated
   p_e (the sky clues are evaluated at Ithaki only; the rotation changes only
   which conjunctions are eclipses).

### 5.3 N3: forking paths

B&M's criteria were not fixed in advance (1.1). N3 counts the readings a
careful reader could defend, sorts them by who has defended them, and asks
how often *some* reading makes a given target the unique match.

**The forks.** Each option carries its source and its tier in
`data/prereg/garden.json`. "None" means the clue is dropped. Tier BM holds
the options B&M themselves raised. Tier DOC adds options with a named
published proponent for this passage, or the standard published
operationalisation of what such a proponent says. Tier FULL adds the rest
[rev #7]. Day tolerances are continuous: a vertex or event instant is
compared with the stated day's instant. B&M's integer tolerance of n days is
equivalent to n + 0.5 continuous days, because a vertex lies within half a
day of its discrete maximum [r1 N13].

| fork | option | tier | source |
|---|---|---|---|
| F1 day count | B&M sequential (34/29/5) and parallel (33/28/4) | BM | [B&M Table 1; chron §5.1] |
| | de Jong 2001 (33/28/5), Stanford 1959 (32/27/4) | DOC | [chron §0 item 4] |
| | the four inclusive-raft rows | FULL | [chron §5.1] |
| F1b typical numbers [rev #8] | off | BM | — |
| | every offset that depends on a typical-number joint (H→D "fourth/fifth", D→Σ "seventeen/eighteenth", Σ→L "two nights … third", "twentieth") uncertain by ±2 d; or by ±3 d | DOC | Gainsford's objection that the counts are formulaic [crit §3.3]; 5.278–279 = 24.63–65 [rev #8]; [txt §3] |
| | D→Σ replaced by another typical number, 9, 12 or 20 days | FULL | [rev #8 fix 1] |
| F2 Day 0 | (a) conjunction date, UT+2 | BM | [B&M] |
| | (c) the day after, Solon's noumenia; (d) the first-crescent day, Yallop B, day counted from sunset | DOC | Plut. *Sol.* 25.3; Geminus 8.11 [vis §4.1] |
| | (b) conjunction date, LMT | FULL | a clock convention, not a reading |
| F3 stars | (a′) C_rel, B&M-calibrated (4.5) | BM | [B&M; MacDonald 1967, unread §2] |
| | (e) autumn: every raft night inside the autumn co-visibility window (both stars ≥ 2° at the end of nautical twilight), recomputed each year; (f) none, "late-setting" as a permanent property | DOC | (e) Papamarinopoulos et al. 2012 [unread §4] and the scholia's season [txt §5.6]; (f) the scholion on 5.272 and Aratus 581–585 [vis §3.1] |
| | (b) both ≥ 2° on every raft night; (c) both ≥ 5°; (d) departure night only, ≥ 2°, either season | FULL | [vis §3.3–3.4] |
| F4 morning star | Venus rises ≥ 90 min before the Sun | BM | [B&M] |
| | Venus a visible morning star (AV 7°); none (a dawn time-marker) | DOC | MacDonald identifies the star as Venus, the morning star of that spring, and dates its greatest elongation [unread §2.1, §2.5] (revision 3's "near morning elongation" was not his wording, 4.2); AV from de Jong [vis §1.2]; Gainsford's formula argument [crit §3.3; txt §5.7; neg §5 item 3] |
| | ≥ 60 min; ≥ 120 min; any bright dawn herald (Venus, Jupiter, Sirius, Mars ≤ −1 mag) | FULL | [vis §1.3–1.4] |
| F5 Mercury | event MWRA (vertex), GWE or morning station × tolerance 1.5, 2.5, 3.5 d (B&M's 1, 2, 3 integer days) × visibility (AV 10°) required or not: 18 options | BM | B&M name all three events and require visibility; S2 never applied it [B&M §References; bm §5 M; rev #23; r1 N13] |
| | event "any of the three"; tolerance 6 d (the slack of Ptolemy's Mercury records, 14/14 within 5.5 d [alm §4]); morning first visibility (AV 10°) at 1.5, 2.5, 3.5 or 6 d; none | DOC | B&M call the events close in time; the *Almagest* records; B&M's "heliacal rising 13 Mar" [bm §9]; Gainsford, and the absence of any ancient Hermes–Mercury link before Plato [txt §5.9] |
| F6 equinox | off | BM (rule gardens) | B&M listed E and did not apply it [B&M §References, §Intersecting] |
| | E_rel with n = 3, 4, 5 | BM (reported gardens only) | MacDonald's reading, formed with the target in view (below) |
| F7 window width | 136 years | BM | [B&M] |
| | 91 (Troy VIIa) and 251 (primary) years | DOC | [win §4, §9] |

**The conditioning rule** [r1 N6; rev #6]. The record shows that every
categorical reading of the clues B&M used was formed by a reader who knew
the target [unread §2.4, §9 item 3]:

| clue | categorical reading | first formed by | the alternative | how the rule gardens treat it |
|---|---|---|---|---|
| N | Day 0 is the conjunction | the scholia on 14.162 (ancient; blind) | — | no conditioning needed: every target is a new moon |
| C | the raft nights are in **spring** | MacDonald 1967, with the eclipse in view; before him every reading was autumn or winter | autumn; none | **conditioned** (T_A(v) ⊂ T_C); 𝒢_DOC also holds options (e) and (f), and is conditioned too (below) |
| V | the herald star is **Venus**, a morning star | MacDonald, who checked Venus in the eclipse year | none (a dawn formula) | **conditioned** (Venus slot of T_A(v), 4.2) |
| M | Hermes' flight is **Mercury** | B&M, who knew the target | none | **conditioned** (Mercury slot of T_A(v), 4.2) |
| E | Poseidon's return marks the **equinox** | MacDonald, who fitted his timetable to the eclipse | none | **left out** of every rule garden (F6 = off); outcome 1 reads T0_pass, which uses no E (3.5) |

A target's agreement with a reading formed for it is not evidence.
Conditioning removes that agreement and keeps the evidence that remains:
whether B&M's *tolerances* (a 90-minute lead rather than any visible morning
star; a Mercury event within 1.5–3.5 d rather than within 6 d) single a
target out, as priced by B&M's own tolerance forks. The categorical
readings themselves have no single width in the record, so the slots form the
frozen family of 4.2 [r2 R2-2]. The same rule covers clues B&M cited as
support: H2 is not counted (7.1).

E is treated differently from C, V and M for two reasons:

- The text gives Poseidon's day and nothing else about the Sun, so E has no
  tolerance part that could survive conditioning.
- Conditioning on it (E_rel at n = 5) would leave about 28 targets
  (139 × about 0.2), too few for any G interval to be informative (2.8).

Leaving E out treats the Odyssey and the null alike: the target loses the
uniqueness E gave it, and so does every random target. G with E-on readings
is reported in two forms: union-priced over T_A, and conditioned over
T_A ∩ E_rel(5). Revision 2's G over T_C (season only) is reported too, so G
appears under both conditionings [r1 N6 fix 2].

The reported G_DOC uses the same pools, T_A(v), although 𝒢_DOC also holds
options that price C, V and M by union ("none", autumn). A union prices only
the choice to include a reading. It does not price the invention of a
reading that fits, which is what the record documents. The DOC options
still widen the tolerance forks (F1, F1b, F2, F4 visible, F5 at 6 d, F7)
for targets in T_A.

**Garden sizes** [me: `cp_bounds.py`; revision 2's sizes are reproduced by
r1 §3].

| garden | F1 | F1b | F2 | F3 | F4 | F5 | F6 | F7 | readings | bits | eclipse-compatible |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 𝒢_BM* (rule) | 2 | 1 | 1 | 1 | 1 | 18 | 1 | 1 | **36** | 5.2 | 36 |
| 𝒢_DOC* (rule) | 4 | 3 | 3 | 3 | 3 | 37 | 1 | 3 | **35,964** | 15.1 | 11,988 |
| 𝒢_FULL* (reported) | 8 | 6 | 4 | 6 | 6 | 37 | 1 | 3 | **767,232** | 19.5 | 383,616 |
| 𝒢_BM, 𝒢_DOC, 𝒢_FULL with F6 (reported) | | | | | | | 4 | | 144; 143,856; 3,068,928 | 7.2; 17.1; 21.6 | 144; 47,952; 1,534,464 |

F5's 37 in DOC and FULL is 4 events × 4 tolerances × 2 visibility settings,
plus first visibility at 4 tolerances, plus none. **T0b's own reading (in
its C_rel form, visibility off, F6 off) is a member of 𝒢_BM*** [rev #23].
Only F2 (a) and (b) put the conjunction on Day 0, where Theoclymenus speaks
[chron §4.H].

Two readings are left out because they cannot change the result: Day 0 as a
20-day window, and N dropped. Their candidates are days, a superset of the
conjunction dates, so they add no reach for any New Moon target [v1 §3.4;
rev §1 confirms].

**The statistic: reach.** For a reading r, let S_r be its survivors over the
background, each mapped to its conjunction (under F2 (c) and (d) a candidate
is mapped back). A target t ∈ S_r is the unique survivor of a W-year window
[a, a + W) placed at a uniformly random start a with t inside, exactly when
the window misses the neighbouring survivors s₋ and s₊. That is,
a ∈ I_r(t) = (max(t − W, s₋), min(t, s₊ − W)]; if t ∉ S_r, I_r(t) is empty.
Over a garden 𝒢, **reach_W(t; 𝒢) = |∪_{r∈𝒢} I_r(t)| / W**. For gardens with
several widths, reach(t) = max over W of reach_W(t), a lower bound on the
union [v1 §3.4]. Under T0b with E off, reach_136(1178 BC) is 11/136 = 0.081
on the recheck's numbers. It would be 0 if a survivor fell in −1176..−1052,
and the only candidate close to the edge is 26 Mar 1111 BC (2.9; R15)
[rev #24c; r2 R2-3].

**G and its interval.** For a garden 𝒢, a pool P and widths W:

- **G(𝒢; P; W)** = the mean of reach(t; 𝒢) over the targets t ∈ P, with
  16 Apr −1177 excluded. G is the look-elsewhere-corrected p-value of a
  coincidence whose target was fixed first, as Schoch's was: the chance that
  a target of the pool, fixed in advance and unrelated to the text, is made
  the unique match by some reading of 𝒢 in a window placed at random around
  it.
- **The interval** [G_lo, G_hi] is the 95% gamma interval of Fay & Feuer
  (1997) for a weighted sum of counts [r1 N8 fix 2]. Each target counts
  1, weighted by reach/n, and the largest possible weight is 1/n. Let
  y = G, v = Σ (reach/n)² and w = 1/n. Then
  G_hi = ((v + w²)/(2(y + w))) · χ²_{0.975}(2(y + w)²/(v + w²)) and
  G_lo = (v/(2y)) · χ²_{0.025}(2y²/v), with G_lo = 0 when y = 0.
  - With no target reached, G_hi = 3.69/n.
  - When every nonzero reach is 1, the interval is the exact Poisson one.
  - Unlike a binomial bound on the share of targets reached, it does not
    treat a reach of 0.2 as 1.

  The formula is given from memory. The implementer checks it against the
  paper, and I9 checks its coverage by simulation.
- **Dependence: the reported interval is the wider of two** [r2 R2-6]. The
  gamma interval treats each reached target as an independent count. Reaches
  are not independent:
  - neighbouring targets share survivor gaps;
  - Venus' 8-year cycle and Mercury's 13- and 46-year near-repeats cluster
    the passes;
  - half the reached targets have reach exactly 1 (2.9).

  So the bench also computes a **moving-block bootstrap** interval over the
  core. It resamples 136-year blocks of consecutive targets with their reach
  values, 10,000 times, and takes the percentile interval; 243-year blocks
  are reported beside. The rule's [G_lo, G_hi] is the wider of the two:
  G_lo is the smaller lower bound, and G_hi the larger upper bound. I9(b)
  checks the coverage of that combined interval on synthetic cores that keep
  the real clustering (6.1).
- **Rule quantities.** Each comes with its pool size n and the number k of
  targets with reach > 0. G_DOC has left the rule: revision 3 used it only in
  outcome 1, which no longer reads G (1.3).

  | quantity | garden | pool | W | used for |
  |---|---|---|---|---|
  | **G_BM(v)**, for each slot variant v0–v5 of 4.2 | 𝒢_BM* | T_A(v) | 136 | label 2's G leg (every variant ≥ 0.20 at the lower bound); Q_tol (every variant > 0.05); Q_slot |
  | **G_BM,u** | 𝒢_BM* | T | 136 | outcome 4: the Odyssey's coincidence as B&M would present it, every reading treated as blind, compared with fiction's blind readings |

  G_BM,u = (n_A(v)/n_T) G_BM(v) exactly, for v1–v5 (4.2). Each G_BM(v) is
  null-side: it is computed at the null-side stage with the target masked
  from every pool and survivor set (12.3). Masking can only lengthen a
  neighbour's survivor gap, so it can only raise G slightly. That works
  against B&M, and the unmasked value is reported beside it after the second
  freeze.
- **Reported beside, never in the rule:**
  - G_DOC(v) = G(𝒢_DOC*; T_A(v); max over 91, 136 and 251 years), and
    G_FULL*;
  - G over T_C (revision 2's season-only conditioning);
  - the E-on gardens over T_A and over T_A ∩ E_rel(5);
  - G_BM on each half of the core (stationarity);
  - G_BM under v6, the "near greatest elongation" Venus slot (4.2);
  - **G_any**, the fraction of the pool with reach > 0. B&M's window was
    itself drawn from the tradition that chose the eclipse [win §6];
  - **G_X**, the h_tot-weighted mean reach over the eclipse new moons of T,
    with 16 Apr −1177 excluded, compared with G_BM,u (spring eclipses
    alone are too few). If eclipse new moons are reached at the rate of
    other new moons (P13), the eclipse adds nothing beyond its rarity.

**Reported:**

1. reach(16 Apr 1178 BC) under the T0b reading, 𝒢_BM*, 𝒢_DOC*, 𝒢_FULL* and
   the E-on gardens.
2. Every G of the list above, with k, n and the interval.
3. **The smallest fork set that reaches G ≥ 0.20 over T_A(v1)**, built by greedy
   addition to 𝒢_BM* of the option that raises G most. The sequence and each
   option's source are printed [rev #7].
4. The look-elsewhere factor G_BM / p_fix,unique, where p_fix,unique is the
   same quantity for the T0b reading alone.
5. **Alternative datings.** Every eclipse new moon with h_tot ≥ 0.1 at any
   Ionian site that some eclipse-compatible reading makes unique, with the
   readings that do it. Four are listed whatever the result:
   - 30 Sep 1131 BC, total at Ithaki at canon ΔT and inside B&M's window
     [rev V6];
   - 24 Jun 1312 BC, the Iliad date of Henriksson 2012 [unread §5];
   - 30 Oct 1207 BC, from Papamarinopoulos et al. 2012 [unread §4];
   - 12 Jan 1183 BC (−1182), Schoch's rejected annular eclipse [unread §3.1].
     Research-window's "1182 BC" for the same catalogue row is a slip
     [win §7.2].
6. Survivors per century for every reading, so the strictness of each
   garden is visible.

**R_anc, the ancient reading** [rev #18; r1 N9]. This pinned reading was
formed without knowledge of any computed eclipse, from the scholia,
Heraclitus and Plutarch:

- **Day 0** is the conjunction date (LMT at Ithaki): the scholia's ἕνη καὶ
  νέα on 14.162, and Heraclitus [txt §5.1].
- **Season.** The scholia read the season as "autumnal, and already towards
  winter" (17.24) and as winter (6.305, 14.458) [txt §5.6]. Greek sources
  divide the year two ways:
  - Hesiod's farming calendar marks the vintage by Arcturus' morning rising
    (*WD* 609–611) and the ploughing, as winter comes on, by the Pleiades'
    morning setting (*WD* 615–617). Its autumn runs from the first to the
    second, and its winter from the second;
  - Geminus divides the year at the equinoxes and solstices (*Isagoge*
    1.9, 2.17).

  The two divisions disagree. R_anc is therefore reported under **four
  season bounds, with equal prominence** [r2 R2-11]. Every table gives all
  four side by side, and none is labelled primary:

  | key | bound on Day 0 | source |
  |---|---|---|
  | S-union | from Arcturus' heliacal rising (AV 10°, computed each year) to the spring equinox: autumn or winter on either division | Hesiod *WD* 609–617 or Geminus *Isagoge* 1.9, 2.17 |
  | S-Gem-aut | Geminus' autumn alone, [180°, 270°) of solar longitude (revision 2's bound) | Geminus |
  | S-Hes-aut | Hesiod's autumn alone, from Arcturus' heliacal rising to the Pleiades' morning setting | Hesiod |
  | S-Gem-aw | Geminus' autumn and winter, [180°, 360°) | Geminus |

  **The history is recorded** [r2 R2-11]. Revision 3 made S-union primary,
  citing the controls file's rule that the weakest reading both sources
  allow comes first [pcr §2]. It did so after the first recheck had computed
  the Sun's longitude at the conjunction of 30 Sep 1131 BC, 176.69°, three
  days before Geminus' autumn [r1 N7]. That choice was made with the result
  in view. Revision 4 therefore names no primary.
- **Eclipse.** Theoclymenus' vision is read as a solar eclipse on Day 0
  (Heraclitus; Plutarch, *De facie* 19 [crit §3.1]): h_06(u, ithaki) ≥ 0.5.
- **No planets and no stars**, because the scholia read 5.272 as
  slow-setting.

R_anc is run **with and without the eclipse clue** [r1 N9 fix 2]:

- **Without it**, the only clues are the conjunction and the season, so
  about six new moons a year survive. That version never has a unique
  survivor, so the ancient reading dates nothing without the eclipse. It is
  the only version whose "coincidence" could be compared with B&M's, and the
  comparison is empty by arithmetic.
- **With it**, R_anc is the ancient reading's own dating. Its survivors in
  each window, their h_tot, and whether one is unique are reported beside
  B&M's.

**What is already known** (2.8, 2.9):

- 30 Sep 1131 BC passes S-union and S-Hes-aut (16–20 days after Arcturus'
  heliacal rising), and fails S-Gem-aut and S-Gem-aw (3 days early).
- 16 Apr 1178 BC fails all four.
- With the eclipse clue, NASA's Ithaca site catalogue gives about 9
  survivors in the reproduction window for a season close to S-union. So
  R_anc dates nothing there (R11).

R_anc is not in the decision rule. The pass rates of the held-out predicates
among its survivors are reported (7.3).

### 5.4 N4: random epics, the main negative

N3 holds the poem fixed and varies its reading. N4 holds the reading
machinery fixed and varies the poem. Random poems of the Odyssey's grammar
are the main negative of the bench [rev #15 fix 3]. They set the percentile
that label 2 uses.

**The grammar** (`data/prereg/epic_grammar.json`, as in revision 1, except
that season clues are relative to each year's sky):

- **Day 0 anchor:** conjunction, full moon, the 7th day of the month
  (Apollo's day in Hesiod, *WD* 770–771 [txt §5.3]), or none.
- **Season clue:** a pair from the archaic star list (Pleiades, Hyades,
  Orion, Sirius, Arcturus [txt §5.8]). Either both stars are ≥ 2° at the end
  of evening or morning nautical twilight on one night or on a 17-night
  span, or one star's heliacal rising or setting falls within ±k days.
- **Planet clue:** Venus, Mercury, Mars, Jupiter or Saturn, in one of three
  forms:
  - a morning object with rise lead ≥ 60/90/120 min;
  - an evening object with set lag ≥ 60/90/120 min;
  - within ±1.5–3.5 days of a turning point (rise- or set-azimuth extremum,
    greatest elongation, station, opposition) or of first or last visibility
    (Ptolemy's AV: Venus 5°, Mercury 10°, Jupiter 10°, Mars 11.5°, Saturn
    11° [vis §1.2]).
- **Offsets.** Variant A ("B&M-shaped") puts a season clue on a span
  starting between −29 and −27, and two planet clues at −5 and −34, around a
  conjunction anchor; the clue types are drawn at random. Variant B draws
  the anchor, two or three sky clues and their offsets (−40 to −1) freely.

Epics are drawn per variant from a seeded stream (`seeds.json`), at site
`ithaki`, and evaluated over the background.

**Per epic:**

- p_c, its primary reading's per-candidate pass rate (its specificity);
- the survivor count in a 136-year window at a random position, and
  P(unique);
- **T_best ≥ T_obs.** Each date is scored by −log10 of the product of the
  per-clue base rates at the observed tightness (P(Venus lead ≥ observed),
  P(\|Δ\| ≤ observed), …). T_obs is that score for 1178 BC under the B&M
  reading. The statistic is P(T_best ≥ T_obs) over epics.

**The specificity stratum.** Epics whose p_c lies within a factor 2 of the
Odyssey's (B&M reading) form the stratum.

**Epic gardens** [r2 R2-8 fix 2]. Each stratum epic gets a BM-tier garden of
exactly 36 readings, the multiplicity of 𝒢_BM*: 2 day-count variants × 18
options for one planet clue, with every other clue at its primary reading.

- **Which clue is forked.** The forked clue is the one in Mercury's role:
  the clue at −34 in variant A, the earliest planet clue in variant B.
- **The 18 options, by clue type.** Every clue type gets 18:
  - a turning point: 3 events × 3 tolerances (1.5, 2.5, 3.5 d) × visibility
    required or not, as in 𝒢_BM*. The events are the azimuth extremum,
    greatest elongation and station for Mercury and Venus, and the azimuth
    extremum, station and opposition for Mars, Jupiter and Saturn;
  - a rise lead or a set lag: 3 thresholds (60, 90, 120 min) × 3 day
    tolerances (the stated day only, or within ±1 or ±2 days) × visibility
    at the body's AV required or not;
  - first or last visibility: 3 AV values (the body's Ptolemaic AV and that
    AV ± 2°) × 3 tolerances (1.5, 2.5, 3.5 d) × a critical altitude of 0° or
    1° (PLSV's convention [unread §6]).
- **The day-count variants** are the stated offsets, and the offsets shifted
  by one day towards Day 0. That shift mirrors B&M's parallel count.
- **Why.** Revision 3 defined the garden for turning-point clues only.
  Epics whose planet clues were rise-lead or set-lag clues got fewer
  readings and a smaller r_e, which biased pct_N4 towards the Odyssey
  [r2 R2-8].
- **The DOC-tier epic garden** adds the DOC fork types and is reported only.

**The calibrated percentile (target first).** Schoch's target was fixed
before any reading.

- **The quantities.** For each stratum epic, r_e = reach_136(16 Apr −1177;
  the epic's garden): the chance that this poem, read with the same freedom,
  makes Schoch's eclipse new moon the unique match of a window placed at
  random around it. r_Ody is the same quantity for the Odyssey under 𝒢_BM*.
- **Which epics enter.** Conditioning works as in 5.3: only epics whose
  categorical slots hold at Schoch's target enter. The season clue must hold,
  and each planet clue's body must be present in the stated role (a visible
  morning or evening object, or within 6 d of the named kind of event).
- **How many** [r2 R2-8 fix 1]. Epics are drawn until **at least 200
  entering stratum epics** exist, n_stratum ≥ 200, up to 10⁶ draws per
  variant. Revision 3 applied the size rule to the stratum and not to the
  entering subset. Entering is of order P(C) · P(A), about 0.1 or less, so
  that rule did not guarantee 200. If 10⁶ draws give fewer than 200, the
  report says so, and the Clopper–Pearson interval carries the small n.
- **No match** [r2 R2-3 fix 1]. If **r_Ody = 0**, no reading of 𝒢_BM* makes
  Schoch's target unique in any window. The bench outputs label 2 in its
  "no match" form. pct_N4 is not computed, because every epic would tie
  with the Odyssey at zero.
- **pct_N4, when r_Ody > 0** [r2 R2-3 fix 2]. Let x_gt be the number of
  entering epics with r_e > r_Ody, and x_eq the number with r_e = r_Ody.
  - **Point estimate:** the mid-p share, pct_N4 = (x_gt + ½ x_eq)/n_stratum.
  - **Lower bound:** pct_N4,lo is the Clopper–Pearson 2.5% bound on
    x_gt/n_stratum. It counts ties for the Odyssey, so ties alone can never
    fire label 2.
  - **Upper bound:** pct_N4,hi is the Clopper–Pearson 97.5% bound on
    (x_gt + x_eq)/n_stratum.
  - **What it is.** pct_N4 is the Odyssey's percentile among random poems
    of the same specificity [rev #1 fix 2]. It is a tail fraction, not a
    probability of the same kind as G [r1 N10].
- **What it may depend on.** The recheck's estimate puts r_Ody at 11/136.
  The case that decides between that value and 0 is 26 Mar 1111 BC
  (2.9). Both branches are reported, with that candidate's exact ΔMWRA and
  its flatness flag (R15).
- **Ē_N4** = the mean of r_e over the entering epics. This is the analogue
  of G with the poem varied rather than the target. P17 compares it with
  G_BM, and it never enters the rule [r1 N10 fix].

**The eclipse-match strength (survivors first; reported).** For a text with
garden 𝒢 in a window, M = the maximum, over eclipse-compatible readings r,
of h_tot(u_r, ithaki), where u_r is r's unique survivor in the window (0 if
there is none).

- For each stratum epic, M_e is computed in a window at a random position,
  and **p_N4** = the fraction with M_e ≥ M_Ody.
- If fewer than 20 epics reach M_Ody, p_N4 is computed analytically
  instead: the mean, over stratum epics, of K_e × p_e(M_Ody), where K_e is
  the number of distinct unique survivors across the epic's
  eclipse-compatible readings. That relies on N2's independence check [rev
  #16 fix 4].
- The direct count is reported beside it, with bootstrap intervals.

p_N4 credits the eclipse's rarity. That rarity would be evidence only if the
readings had been formed blind to the eclipse, and the record says they were
not (1.1). p_N4 is reported and enters no rule. Revision 2's ratio LR_sf is
withdrawn with the other likelihood ratios (5.7).

### 5.5 N5: window sensitivity

N1–N3 run in every window of 4.6. Reported: survivors per century, the
survivor list, the eclipse new moons in the window with their h_tot, and
P(≥ 1) as a function of W from 50 to 900 years. "The single date in the
window" is never reported without the rate beside it [win §9]. Two checks:

- **Strict Eratosthenes.** Eratosthenes put the sack in late spring 1183 BC
  (−1182); with at least 8 years of wandering [Od. 7.259–261, 10.467–470] the
  return falls in about 1175–1173 BC and 1178 BC is outside [win §5–6; rev
  V11]. The report gives the survivors, under each reading, compatible with
  each ancient sack date plus 8–11 years.
- **Gainsford's 1350–1250 BC extension**, which the primary window includes,
  and Henriksson's Iliad date (a sack about 1312 BC puts the return about
  1302 BC, outside B&M's window) [unread §5].

### 5.6 N6: ΔT and the eclipse at Ithaca

1. **Models and pairings** as in section 0: the three SMH models with DE431,
   Espenak–Meeus (canon form) with NASA's elements; DE441 reported beside with
   its offset (+188 s at −1177) [eph §5.3].
2. **Sites:** the five Ionian sites.
3. **Outputs:** magnitude and LAT of maximum as a function of constant ΔT
   from 26,000 to 32,000 s; totality windows; P(total) per model; the
   four-model mixture; P(smag ≥ 0.9); the same in the canon frame on NASA's
   elements. Known values are in 2.3; N6 recomputes them with `eclipses.py`,
   and the recomputation is an instrument check, not a prediction.
4. **30 Sep 1131 BC and 24 Jun 1312 BC** in the DE431 pairing, and joint
   probabilities under a common ΔT offset, per model. Revision 1's failed
   prediction 19 is restated per model [rev #17 fix 2]. Its canon-frame
   values are known (2.3), so the DE431-frame recomputation is regression
   expectation R7, not a prediction [r1 N7].
5. **ΔT and the clue tests.** Count the candidates whose civil conjunction
   date flips between 27,602.7 s and each model at ±1σ (known: about 1.9% for
   SMH2020 + 1σ), and rerun T0b at SMH2020 ± 1σ with DE431 conjunctions
   (P2).
6. **B&M's own value** is reported as uninterpretable (2.3) and is never
   converted into another frame.

### 5.7 Evidential weight: an identity, a ceiling and a Bayes factor

Revision 2's bottom line was a likelihood ratio, LR = R_obs/G. In it,
R_obs was the mean reach of a truth whose sky an observer had described.
The recheck showed that it can never pass about 6.5, whatever the data
[r1 N1]. The argument has four steps.

1. With the poem held fixed, every truth accepted in PC-S science mode
   carries the Odyssey's clue set at the Odyssey's offsets.
2. So the survivor sets are the Odyssey's, and R_obs and G are two
   weightings of one reach function: R_obs = E[reach · 1_A] / P(A) and
   G = E[reach], both over T_C.
3. Hence

   **LR_slot = P_w(A) / P(A) ≤ 1 / P(A)**, where P_w is the reach-weighted
   probability.
4. P(A) is 0.154, so the ceiling is about 6.5 (5.1–9.0) (2.8).

**The identity is a finding, not a bug.** An observer who records that a
bright star heralded the dawn and that Hermes flew can raise the odds of a
target by at most the inverse of how often a sky has those features. The
precision that B&M's criteria carry (90 minutes, ±1 day) belongs to the
reader, not to the text. Two consequences follow:

- under the conditioning of 5.3, where the categorical readings were formed
  with the target in view, LR_slot over T_A is identically 1;
- any rule threshold on such a ratio is decided by the observation model,
  not by the Odyssey.

**So no likelihood ratio enters the decision rule** [r1 N1 fix 2(a)].
Outcome 1 rests on T0_pass and on the exact held-out test of section 7.
Label 2 rests on r_Ody, G and pct_N4. Revision 2's R_obs/G, its curve over
noise and LR_sf are withdrawn as rule inputs. What is reported, as standing
findings beside the verdict:

1. **The ceiling.** P(A), with its interval, and 1/P(A), recomputed on the
   bench's sky tables over T_C. A is the slot event of variant v1 (4.2), the
   one the first recheck measured; the other variants are reported beside.
   **LR_slot(ν)** is also given as a curve over
   the noise grid of 6.2. Its numerator is computed exactly, not by
   sampling [r1 N8 fix 1]:

   R_obs(ν) = Σ_t Σ_δ reach(t) · 1[A(t, δ)] · w(δ) / Σ_t Σ_δ 1[A(t, δ)] · w(δ),

   - t runs over T_C;
   - δ runs over every vector of slot-day offsets in [−j, j], with weight
     w(δ) uniform, and with the Mercury displacement s_M applied to the slot
     tolerance;
   - reach is taken from the same garden and the same W as the denominator
     [r1 N8 fix 3].

   No new survivor sets are needed, because the poem is fixed.
2. **The Bayes factor of the residual fit under B&M's own hypothesis.**
   H1_BM says that the poet encoded the phenomena of some reading r of
   𝒢_BM*, each reading equally likely (π_r = 1/36). H0 says the clues are
   unrelated to the target. Under H1_BM, with probability ρ_r the target's
   sky passes reading r. Otherwise it is a sky drawn from T_A that fails r.
   For the target t_S = 16 Apr −1177,

   BF_BM(ρ) = Σ_r π_r [ ρ_r · 1{t_S passes r} / p_r + (1 − ρ_r) · 1{t_S fails r} / (1 − p_r) ],

   where p_r = (number of targets of T_A \ {t_S} passing r + 1)/(n_A + 1).
   This is the pass rate of reading r as a filter (survival, not uniqueness),
   with the add-one rule so that no p_r is 0. BF_BM is exact for the
   whole pass/fail vector of t_S under that model.
   - It is reported at ρ_r = 1, the model most favourable to B&M, and at
     ρ_r = the PC-S science-mode recall of r at ν_real (6.2).
   - Its ceiling is BF_max = Σ_r π_r/p_r, reached when t_S passes every
     reading.
   - p_r is taken over T_A(v0), the documented slots (4.2), and the other
     variants are reported beside.
   - From the first recheck's numbers, B&M's reading alone passes about 5 of
     41 targets of T_A, so it can contribute at most about 8 (2.8). The
     second recheck computed BF_BM(ρ = 1) ≈ 2.6 and BF_max ≈ 20.7 over the
     36 readings, on revision 3's slots (2.9; R16). Both figures are rough.
3. **The *Almagest* calibration** [r1 N1 fix 4]. The same estimator is
   applied to each counted *Almagest* set:
   - it gives the BF of the set's true date under the set's own garden (its
     fork options, at regime-SL tolerances);
   - p_r is the share of the civil days in the set's 21 window positions
     that pass reading r.

   This shows what truly observed records, whose statements carry their own
   precision, earn under the machinery that scores the Odyssey.
   - **It is not compared numerically with BF_BM.** The *Almagest* BF is
     unconditioned and taken over day candidates, while BF_BM is conditioned
     on readings formed with the target in view. They are not the same kind
     of number, so revision 3's P33 is dropped [r2 R2-5].
   - The held-out test has its own *Almagest* calibration (6.4, Q_H).
4. **The blind version of the words.** The words' ceiling if the categorical
   readings had been formed blind is 1/P(A), about 6.5. The bench prints it
   beside BF_BM as "what the words could carry if C, V and M had been
   proposed without the target".

The bench reports these figures, together with G, p_fix and the bit budget.
It does not multiply any of them by a prior.

---

## 6. Controls

All clue sets, readings, windows, sites, seeds, regimes and thresholds for
the controls are in `data/prereg/` and are frozen with this document
(section 12) before any control is computed.

**Truth-side files.** Every file in `data/prereg/` that holds or is derived
from a control's accepted date has "truth" in its name:
`controls_real_truth.json`, `controls_almagest_truth.json`,
`truth_index.json`, `i2b_truth.json` (6.1, I2b) and
`deltat_circular_truth.json` (6.3.3). Revision 4 called the last two
`i2b_reference.json` and `deltat_circular.json`, and its refusal pattern
`*_truth*` did not even match `truth_index.json`. The pattern is now
`*truth*`.

- **Outside `data/prereg/`.** The slack table that `tools/build_regimes.py`
  reads, `results/controls-almagest/slack.json`, is truth-side too; it sits
  in `results/`, which the public tier does not read (10.1).
- **One rule input derives from it.** `almagest_regimes.json` carries the
  leave-one-set-out tolerances computed from that table (6.4). It holds
  tolerances, never a date, and the searcher must read it, so it keeps its
  name.

- **Who reads them.** Only `odybench/harness.py` (to place windows, to
  score and to run the exposure audit, 6.3.4), `tools/build_truth_index.py`,
  `tools/build_regimes.py` (6.4) and the leak test of I13(h).
- **Who does not.** The searcher never reads them, and a static test
  enforces this (I13(c)).
- **This document.** Its truth-side facts are in Appendix T, and the agents
  who build the searcher and translate the clue files work from a copy
  without it (10.1, I13(h)).

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
| I2b | language-to-magnitude: local magnitudes for the dated eclipses of [ctl §3] | the values printed in [ctl §3], moved to the truth-side file `data/prereg/i2b_truth.json` | **like with like** [r2 R2-7; r1 N15]. The reference used the partial formula (r☉ + r☾ − sep)/(2r☉) [ctl §2.2], so the bench side is `smag_partial`. The bench side is `eclipses.local` on NASA's elements at the element row's canon ΔT. The reference side is Horizons DE441 geometry at NASA's catalogue ΔT, by the longitude-shift equivalence, which mixes frames by the DE441 − canon offset (about 90 s at −430). Pass: within 0.02, or within the change produced by ±100 s of ΔT if that is larger; above 0.95, the central flag agrees | PC-R solar rows | pre-freeze, after the re-draft of 6.3.4 |
| I3 | Hesiod's star calendar at 701 BC, 38.37°N | Hesiod's own numbers | **a calibration** [rev #20; r1 N15]: the Pleiades' AV is set so that they are hidden 40 days (*WD* 385–386); "Arcturus ≥ 5° at nautical dusk" is read off *WD* 564–567 | — (reported) | pre-freeze |
| I4 | lunar eclipses, `lunar.py` | NASA LEcat5 rows: every lunar eclipse of the 23 century pages −1999..+300 (about 5,500), so that the check names no century a control's truth lies in (revision 4 named "the PC-R and ALM truth centuries") | type identical, except where umag or pmag lies within 0.002 of 0 (tie band, listed); umag and pmag within 0.02; greatest eclipse within 3 min after removing the ΔT difference | PC-R lunar rows, ALM-C | pre-freeze |
| I5 | rise, set and transit, `sky.py` | (a) JPL Horizons rise/transit/set output for 1,000 random events (Sun, Moon, Venus, Mercury, Jupiter, Sirius, Arcturus; Ithaki, Alexandria, Troy; −1999..+300; same h0, airless); (b) the dense-grid-plus-bisection rise finder of `results/critique-design/check_mwra.py`, on 2,000 events | (a) within 0.5 min after removing the documented sidereal-time convention difference (5 s at −1999 [acq §1.3]); (b) within the sum of the two convergence tolerances plus 0.01 s: 0.12 s for Mercury (0.1 s bench, 0.01 s reference) and 1.02 s otherwise | every sky clue | pre-freeze |
| I6 | derived events, `events.py` | (a) the event lists of `results/bm2008-reconcile/check_mwra.py` (rise-azimuth maxima and minima, stations, GWE, inferior conjunction) for all 152 S2 years; (b) the low-precision Standish-element code `results/bm2008-b-checks/ephem.py`, 500 random stations and greatest elongations; (c) heliacal star phases and B&M's spring limits from `docs/research_visibility_calc.py` at −1177 and −700; Arcturus' heliacal rising at −1177 and −1130 against `results/design-revision-r2/ranc_season.py` | (a) same UT+2 civil date in ≥ 150 of 152; vertex instants within 0.05 d for maxima not flagged flat, and within 0.5 d for flat ones, which are listed (the two codes fit different parabolas, and a flat maximum's vertex is ill-conditioned [rev #12]); (b) within 1 d; (c) within 1 d | M, H3, the ALM rows, C_rel | pre-freeze |
| I7 | B&M's reading through `clues.py`, `readings.py` and `search.py` | `tests/bm_reference.py`, a minimal second implementation written by a different agent from section 3.2's text alone, using only `ephem.altaz` and its own rise bisection [rev #13 fix 4] | identical pass flags (N, C, V, M, E, every T0 grid cell) for every candidate in 1250–1115 BC and in 300 random background years, **except** inside the tie bands [r2 R2-4 fix 3]: \|Δ\| within 0.01 d of a Mercury tolerance; Venus lead within 0.05 min of 90 min; an E or C bound decided by a star or equinox instant within 0.01 d of a civil-day boundary. Every tie-band candidate is listed with both values | T0_pass, G, P_BM, P_MWRA | (a) null-side stage, on the masked pool (every candidate but the target), before any G is read; (b) the target's own flags after the second freeze, before any T0 output is read |
| I8 | calendar | `tests/test_calendar.py` | 11/11 [acq §4] | everything | done |
| I9 | reach, G and the pools | (a) a brute-force implementation that slides windows in 0.01-year steps, on 10,000 random synthetic survivor sets; (b) coverage of the G interval of 5.3 on **dependent** synthetic data: 2,000 synthetic cores, each built by concatenating randomly drawn 243-year blocks of the real candidate sequence with all their flags, so that real clustering is kept; the true G of the block population is computed on a 100,000-year synthetic background [r2 R2-6]; (c) the identity G(𝒢_BM*, T) = (n_A(v)/n_T) G(𝒢_BM*, T_A(v)) for v1–v5 on the real tables | (a) reach equal within 0.0002; (b) coverage of G_hi and of G_lo each at least 0.95 − 3 × its Monte Carlo standard error (about 0.935); (c) exact to float rounding | G_BM, G_BM,u, G_j, r_Ody | pre-freeze (a); null-side stage, before any G is read (b, c): (b) and (c) need the real survivor flags, which are null results |
| I11 | plumbing negatives (revision 1's NC4 and NC5 [rev #15 fix 4]) | (a) AEN-TROY's pinned R-ii-literal reading, conjunction on Day 0 with the Moon up after nightfall, which contradicts itself [neg §3.1]; (b) a synthetic set with Day 0 a conjunction and the Moon above the horizon at local midnight; (c) Hesiod's star calendar (*WD* 383–385, 564–567, 609–611, 615–621) as event clues around an arbitrary Day 0 | (a), (b) zero survivors in every window (a is known to hold at Troy in two windows, 2.6); (c) no unique survivor in any 136-year window | hit_j | post-freeze |
| I13 | prereg I/O | (a) every licence string present in its cited row, comparing raw characters without Unicode normalisation (the Ptolemy export mixes tonos and oxia, and prints the half-sign as the literal "U+2220") [lca1 method 1; lca2 method 1; pcr §5]; (b) every fork option of every row translates to a canonical predicate (10.3), with exactly one primary per controls row; (c) no module but `harness.py`, `tools/build_truth_index.py`, `tools/build_regimes.py` and the test of (h) opens a `*truth*` path or contains the Nabonassar epoch; (d) `operational_map.json` is reviewed by a second agent; (e) the re-draft brief of 6.3.4 contains no statement, option name or justification string of `controls_real.json`, and exactly the five briefed rows; (f) `almagest_regimes.json`, `slots.json`, `sibling_pairs.json` and `deltat_circular_truth.json` parse, every value they name exists in the clue files, and the projection and held-out rows of `almagest_regimes.json` equal those of the rules of 6.4 (as `results/design-revision-v5/alm_rows.py` transcribes them); (g) the target mask: with `mask_target=True`, evaluating any predicate on 16 Apr −1177 raises, and a static test finds no target-side call in `attain.py`; (h) the build agents' copy of the design: `tools/public_design.py` writes `build/DESIGN.public.md`, everything above Appendix T's marker line. It must contain no text below the marker, and no accepted date of a control in any form the truth files print it (A6 runs this part, because it reads the truth files). Every build agent's log lists each repository path it opened, and `tools/check_access.py` compares the lists with `data/prereg/access.json` (10.1) | all pass | every control and the null-side stage | pre-freeze |
| I14 | the decision rule | (a) the synthetic input sets of 9.5; (b) the structural constraints of 9.4; (c) at the null-side stage, the sets rerun with every null-side field replaced by its measured value | (a) each returns its stated labels and qualifiers; (b) every set marked "realisable" satisfies every constraint, including C7; (c) recorded: which outcomes stay reachable with the measured null side, and Q_attain, Q_tol and Q_slot | the verdict | pre-freeze (a, b); null-side stage (c) |
| I15 | the held-out predicates H3 and H4, `heldout.py` (new) [r2 R2-1 fix 4] | (a) an independent implementation on the Standish low-precision code of `results/bm2008-b-checks/ephem.py`, with its own rise bisection, for every member of P_BM (P_MWRA ⊂ P_BM); (b) Horizons for 50 members drawn at random | identical flags except inside the tie bands: a conjunction instant within 0.1 d of the ±3-d bound; a Venus–Mars separation within 0.1° of 5°; a Sun altitude within 0.1° of −AV at a planet's rising or setting. Tie-band members are listed | p_H, p_H,min | null-side stage, on the masked pool, before p_H,min is read; the target's flags after the second freeze, before p_H is read |

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
- (iii) **every target of T_C in the core** (892 at the recheck's count [r2],
  not "2,000"), each accepted in a noise cell only if its sky satisfies the
  slot event A(t, δ) at the jittered days. This is exactly the population
  over which the exact R_obs of 5.7 averages, so the simulation and the
  reweighting estimate one quantity [r2 R2-4 fix 1]. Revision 3 drew pool
  (iii) from T_A, at fixed slot days. Targets of T_C \ T_A that satisfy A at
  a jittered day then entered the exact denominator, but were never
  simulated.

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
simulation of R_obs against its exact reweighting (5.7), with every truth of
pool (iii) in every cell. Both are reported beside INSTR, not in it, because
PC-S feeds no rule (6.1) [r2 R2-4 fix 2]. The P(unique) of the B&M reading
over the truths that pass it is reported with its n. The first recheck's
figure was 0.647 on n = 4, which has no power, so revision 3's P22 is
dropped (2.7).

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
data that fitted the ΔT models (2.6): R-DIOD's eclipse and H-LIVY's L4
(SMH's Table S10 v2020), and R-THUC's T1 and R-XEN's X3 (SMH2016 §2b(iv),
*secondary*). Their table entries are truth-side [AppT 4].

**A pre-freeze task** reads SMH2016's Table S4 and §4b and the 2020
Addendum's tables. It lists every control eclipse used in any fit, and
whether the *Almagest* timings are among them, in
`data/prereg/deltat_circular_truth.json` with page locators (12.1). Matching
a table entry to a control needs the control's date, so that file is
truth-side, its writer (A11) works on the truth tier (10.1), and only the
harness reads it.

**seen_PCR,noncirc** is the gate count with each circular set's ΔT-dependent
rows rescored under the mixture with every model's σ multiplied by 3. A
model fitted to a record cannot then constrain that record much.

- **Q_ΔT holds** if seen_PCR,noncirc falls on the other side of 4 from
  seen_PCR.
- Gate 3a is also reported with the circular sets removed, the threshold
  then being half the remaining counted sets, rounded up. That count is
  reported only.

The width of R-DIOD's table interval suggests that its pass is robust
[AppT 4]. Q_ΔT tests that rather than assuming it.

#### 6.3.4 The drafter's exposure

The drafter had seen computed answers and flags three primaries as possibly
steered: T1-DARK, D-ECL and the ±1 h tolerance in L4-DARK [pcr §1]. The
recheck adds T2-SEASON, whose start (330°) and width are the drafter's, and
T-INT-12's ±0.5-year tolerance [r1 N5]. Why those two matter is truth-side
[AppT 3]. The gate uses `controls_real.json`
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
2. **A sibling-convention audit** [r1 N5 fix 2–3], restricted [r2 R2-10].
   The audit itself runs post-freeze, in `controls.py`, because it reads the
   truth. What it may transplant is fixed before the freeze, without the
   truth, in `data/prereg/sibling_pairs.json`:
   - **Only sourced conventions are transplanted.** A convention qualifies
     only if the clue file names an outside source for it, such as
     Thucydides' summer half-year (5.20.3), with summer as solar longitude
     [0°, 180°] [pcr §3]. The drafter's own choices are never transplanted:
     T2-SEASON's start at 330° is the drafter's (justified by εὐθύς), so it
     never moves into T1-SEASON or T3-SEASON.
   - **Only between rows whose licence words state the same feature.** An
     example is the same season word, θέρος, in T1, T2 and T3, or the same
     unit. The convention is applied to the receiving row's own words:
     - "at the start of the following summer" under the half-year
       convention is the half-year [0°, 180°], the weakest reading the
       convention allows;
     - a row that states only "summer" never receives a narrower "start of
       summer" span.
   - **Who decides.** A3 drafts the pair list from the clue file and the
     cited rows. A9, the second reader, checks it. Neither reads the truth.
     I13(f) checks that it parses.
   - **The excluded transplants are listed in the file**, each with its
     reason: unsourced, a different feature, or a stricter span on a weaker
     wording.
   - **The audit.** For every row whose primary passes the truth, each
     permitted transplant is applied. Every row that a permitted sourced
     convention makes fail is listed in `results/pcr/exposure_audit.json`.
   - **seen_PCR,sibling** is the gate count with each listed row at its
     failing convention, all at once.

   Revision 3's audit transplanted every matching sibling convention in
   both directions. That tested rows against conventions their words do not
   state, so seen_PCR,sibling and Q_exposure could flip without any
   exposure [r2 R2-10].

**Q_exposure holds** if seen_PCR,redraft or seen_PCR,sibling falls on the
other side of 4 from seen_PCR.

**What this controls, and what it does not.** It controls exposure to
files. It does not remove a language-model drafter's background knowledge
of famous dates (several of these eclipses are among the best known in
antiquity), and no re-draft by such an agent can [r1 N5 fix 4]. As the recheck noted, a re-draft
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
twice (SHA-256 `18b3ff01…b458`) [lca1; lca2]. It holds 12 sets of dated
records: Mercury and Venus elongations, planet–star and planet–Moon
relations, lunar phases, a lunar eclipse and an equinox. The day intervals
come from Ptolemy's own Egyptian dates, and the date words themselves are
withheld.

**Counted sets** are ALM-A, B and D–L (11). ALM-C is reported only (6.3.5).

**Windows** are 136 years, B&M's width. The harness draws a uniformly random
position for the anchor record's true date (seed per set), as in 6.3.1, and
twenty further positions are a sensitivity. The truth file
`controls_almagest_truth.json` is read only through `truth_index.json`.

**Candidates** are every civil day in the window as Day 0 (LMT at the
default site), with each row at its stated day offset.

- **Instants.** Each row is evaluated at the drafter's instant convention:
  "evening" and "dawn" are the moments the Sun is 8° below the horizon, and
  stated hours are local apparent time [alm §1.5]. The convention moves
  continuous offsets by about ±0.1 d.
- **Hourless records.** C.1, D.3, G.1, L.1 and L.4 state no hour. Their
  civil day comes from ἑῷος or ἑσπέριος (the morning or evening part of the
  dated night), and Ptolemy's own Sun figures confirm every such offset. The
  harness evaluates them at the "dawn" or "evening" instant accordingly
  [lca2 item 5].
- **Cruxes.** The two textual cruxes (A.6 and H.3) run at their primary, as
  printed, and the emended intervals are reported.
- **ΔT** is the mixture, as in 6.3.3.

**The two Ptolemy files treat Egyptian dates differently.** This file
withholds them, while `controls_real.json` carries them with a free epoch
[alm §3; pcr §2]. Both are kept. With the epoch free, an Egyptian date fixes
only intervals, so the two are equivalent for the searcher, provided that
no bench code supplies the Nabonassar epoch (JD 1448638). I13 checks
statically that the number appears only in the truth files and the harness.
The `ref` of every *Almagest* row points at a text row that contains the
withheld date, so the searcher reads only the operational fields and never
the text at `ref` [lca1 item 6; lca2 item 7].

**Default site.** Horizon-dependent rows are evaluated at Alexandria,
31.20°N 29.92°E. That is the observing place Ptolemy names for his own
records (4.6.13, 9.10.3, 11.2.2). The *Almagest* also names Babylon, for the
Babylonian eclipses of IV.6.3 [r1 N17], but those are in R-PTOL-BAB, not in
the B&M-type sets. For sets whose rows leave the observer unstated the site
is an inference, flagged as such: X.8.2 and IX.9.4 in ALM-A, IX.8.3 in
ALM-C, and the observer of every row of ALM-D to ALM-L [lca1 item 5; lca2
item 6]. Babylon is a sensitivity for ALM-K. ALM-K's prose hints (a
Mesopotamian archive, a Babylonian cubit) are not clues [lca2 item 6].

**The B&M-type projection.** The gate uses only rows of B&M's kinds, each
from its words alone, as the Odyssey's clues are:

- interval rows;
- moon-phase rows, at their phase-class option, **except A.10 and B.5**,
  which are set to "none". Their phase classes are chosen from longitudes
  Ptolemy states in the row, his mean Sun from his tables, not from words
  [lca2 item 4]. The Odyssey's phase clue is a phrase (14.161–162). A phase
  computed from a measured longitude is more precise than any phrase, so it
  would make the control easier than the thing it calibrates. A.2, A.5, B.2,
  B.7 and B.9 need no coordinates and stay [lca2 item 4]. The projection
  with A.10 and B.5 at their phase class is reported as a sensitivity;
- planet rows about greatest elongation, before or after greatest
  elongation, visibility, rise lead and the rising-azimuth proxy. **A.1,
  I.1, B.1 and J.4 use their literal, unbounded option**
  (`ge_after_same_apparition`, `ge_before_same_apparition`): their primary's
  bound of 7–60 days is the drafter's inference [lca2 §D], and an inferred
  day interval never enters a gate (critique issue 2). The bounded primary
  is reported as a sensitivity;
- the equinox row.

Star rows, planet–star and planet–Moon positional options, the measured
Sun–Moon distance (`elongation_tol`), oppositions and the eclipse row are set
to none, because they are not in B&M's grammar. They are the held-out rows
below. The full primary run is reported beside.
`results/design-revision-v5/alm_rows.py` transcribes these rules and lists
every set's projection and held-out rows [me: `alm_rows.out.txt`].

**Two regimes, frozen in `data/prereg/almagest_regimes.json`** [r1 N2 fix 4;
N3 fix]. The licence-checked clue file stays byte for byte as it is (its
SHA-256 is recorded in 12.4). The regime file names, for every row of the
projection, the option and the parameter values each regime uses. I13(f)
checks that every named option exists. `tools/build_regimes.py` (A0, 10.1)
writes it mechanically from these rules and from the slack table
[AppT 1]; nothing in it is chosen by hand.

**No regime takes its tolerances from the drafter's grids** [r2 R2-9]. The
lists are the drafter's grids, not licences, and the regime file records
each value as a decision [r1 N2 fix 4]. Regime BM's 1.5 d is not in the
lists. Regime SL's values are ceilings of measured slack:

- **Revision 3's rule is replaced.** It took the smallest listed value at or
  above the out-of-set maximum. That rule is undefined when no listed value
  covers the maximum.
- **The grid's history cannot be settled.** For Venus only the grid's top
  value covered the out-of-set maximum. The note itself calls Mercury 5 or 7
  d and Venus 21 d "the *Almagest* slack" [alm §5 item 1]. That suggests the
  list was written with the measured slack in view, but the file times
  cannot settle it [r2 R2-9].
- **The ceiling rule** depends on neither the list nor its history, and it is
  always defined.

| | regime SL (observer slack, leave-one-set-out) | regime BM (B&M's method as written) |
|---|---|---|
| option | the row's primary, with the two exceptions of the projection (A.10 and B.5 none; A.1, I.1, B.1 and J.4 at `ge_*_same_apparition`) | B&M's own proxy where the row offers it (`bm_mwra_k`, `bm_venus_lead`); else, for a greatest-elongation row, `ge_true_k`; else the row's primary, with the same two exceptions [r1 N3 fix] |
| Mercury and Venus greatest-elongation k | **leave-one-set-out ceiling**: the largest \|record − true greatest elongation\| (true Sun) among the records of that body *outside* the set, from alm Table 2 (records in no set included), rounded up to the next whole day [r1 N2 fix 1; r2 R2-9]. For Mercury this comes to 6 d in ten counted sets and 5 d in one; for Venus to 21 d in every set [AppT 2] | 1.5 d, B&M's ±1 integer day as a continuous tolerance [r1 N13]; 1 d reported |
| `bm_mwra_k` | — (not primary anywhere) | 1.5 d |
| `bm_venus_lead`, minimum lead | — | 90 min |
| opposition k (full run only) | leave-one-set-out ceiling over the oppositions in no set: 0.42 d (mean Sun) rounded up = 1 d | middle value |
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
  planetary records" [rev #3 fix 3]. It conditions every "no" that rests on
  B&M's tolerances: label 2's G leg, Q_tol and pct_N4. It no longer blocks
  outcome 1. Revision 3 used it to demand G_DOC there, but outcome 1 now
  rests on the exact held-out test, whose validity does not depend on
  anyone's tolerances being realistic (7.2).

**The held-out calibration (Q_H)** [r2 R2-1 fix 4]. Outcome 1 rests on a
rank test of unfitted clues at a date. The founding rule asks for that test
to be shown on records whose date is known.

- **The held-out rows**, named row by row (revision 4 left the moon-phase
  rows ambiguous; [me: `alm_rows.out.txt`]):
  - star rows, at their primary option (F.4's primary is "none", so F.4
    holds nothing out);
  - planet rows whose primary is a position or an opposition: A.4
    (`opp_mean_k`) and J.7 (`positional`);
  - moon-phase rows, at the option that states the record's own
    measurement: `positional` (the planet–Moon relation) for A.2, A.5, A.10,
    B.2 and B.5, and `elongation_tol` (the measured Sun–Moon distance) for
    B.7 and B.9.

  Per counted set: ALM-A A.2, A.4, A.5, A.10; ALM-B B.2, B.3, B.5, B.7, B.9;
  ALM-D D.4; ALM-H H.2, H.5, H.6, H.9; ALM-I I.2, I.3, I.5; ALM-J J.2, J.5,
  J.7; ALM-K K.2, K.5, K.8; ALM-L L.2, L.7. **ALM-E, ALM-F and ALM-G have
  none.** `almagest_regimes.json` lists them.
- **The null pool.** The candidate days of the set's window that pass every
  projection row in regime SL, with the true date excluded.
- **The score and the p-value.** The score is that of 7.2: each held-out row
  is weighted by −log10 of its pass rate over the pool plus the truth. The
  p-value is p = (1 + #{days with score ≥ the truth's})/(1 + n).
- **Tolerances.** Each held-out option takes the most lenient listed value,
  as in regime SL.
- **The count.** held_ALM is the number of the 11 counted sets whose truth
  has p ≤ 0.05. **Q_H holds if held_ALM < 6.** It conditions the held-out
  "no" ("the held-out test could not have seen it"), and it does not block a
  "yes", for the reason given under Q_BM.
- **Sets with nothing held out.** A set whose truth is not in the
  projection's pool, or which has no held-out row, counts as not recovered.
  That works against the test. Three counted sets have no held-out row, so
  **held_ALM ≤ 8** by construction, and Q_H needs 6 of the 8 that can
  qualify. That is demanding, and it is meant to be: the qualifier then
  speaks only when the machinery fails on records whose held-out rows are
  star positions, much sharper clues than the Odyssey's.

**What is already known** (2.6; the per-set facts are in [AppT 1–2]):

- in regime SL the true date is retained in 9 of the 11 counted sets, and
  only narrowing remains open (P21);
- rec_ALM_BM is at most 5, so **Q_BM holds**, and the bench recomputes it as
  a regression check;
- held_ALM ≤ 8 by construction, and it has not been computed. P24 predicts
  at least 6.

**New vocabulary the harness must implement** [lca1 item 2; lca2 item 3]:

- the bound `same_apparition` (A.1, B.1, I.1, J.4);
- F.4's `star_candidates`, with one garden branch per candidate;
- B.2's positional `relation`: (Moon's apparent centre − Venus) = 1.5 ×
  (Venus − β Sco), with Venus between the two. This is a held-out row;
- C.3's option `magnitude_and_side` with `eclipsed_limb: north`, and
  `umbral_mag_range` in `magnitude_and_time`. ALM-C is reported only, so
  these never reach the gate.

### 6.5 Negative controls (outcome 4)

**The clue file** is `data/prereg/negatives.json` as licence-checked twice
(SHA-256 `be4f511e…9c82`) [lcn; lcn2]. It holds 12 clean negatives (Virgil,
Apollonius, Quintus Smyrnaeus, Valerius Flaccus) and the Iliad as a
same-tradition comparison [rev #15 fix 1–2; neg §1]. Each clean negative is
fiction or legend composed long after the events it tells, drafted under the
Odyssey's own selection rules, with no similes and no lying tales. Its
`operational` fields are prose, so each option is translated into a
canonical predicate in `data/prereg/operational_map.json` before the freeze,
and a second agent checks each translation against its prose. Consumers of
the file read the top-level `license_check` block as `round_1` and `round_2`
[lcn2 finding 2].

**Pre-freeze decisions and second reading** [neg §6; lcn §4; lcn2 finding
13]:

- **Counts and caps.** A second reader checks the interval forks and caps
  that rest on the drafter's own counts: ARG-CIUS n16/n17/n18, ARG-COLCHIS
  a3/a4/afree, IL h12/h13/h15, VF-LEMNOS-01, and the caps free30, xfree, w60
  and QS-SACK-06's 10 d.
- **Rows whose day another row's fork sets** [lcn2 finding 5]. ARG-COLCHIS-01
  (the Arcturus storm) takes its night from ARG-COLCHIS-02's option: Night −7
  under a3, −8 under a4, any of −7 to −10 under afree (the row passes if it
  passes on one of them). Under ARG-COLCHIS-02's "none" the storm night is
  unplaced and row 01 is dropped from the reading, as the file says.
  ARG-CIUS-05 takes its night from ARG-CIUS-06's count (n16, n17, n18) in the
  same way. `readings.py` builds such pairs as joint options, so no reading
  pairs a row with a day its link row does not give.
- **"literal" means least inference.** Pinned literal readings that use an
  inferred or drafter-width option are re-pinned by the second reader to the
  least-inference option of their row: AEN-CRETE-01 a60, ARG-RETURN-03 x0,
  ARG-COLCHIS-02 a3, and, after round 2, VF-COLCHIS-01 vis7, whose
  least-inference reading of "serus … vesper" is now "none" [lcn §4.4; lcn2
  finding 13(6)].
- **QS-SACK-03.** Its BM-analogue pin keeps option b in its new meaning (the
  Pleiades over the dark hours), and b-late stays in the garden.
- **Places, landmarks and thresholds.** The same reader checks the place
  identifications against a gazetteer (Pleiades). Round 2 moved Mount Ida
  from AEN-TROY's `observer_places` to a set-level `landmarks` list, because
  the narrative puts no observer there [lcn2 finding 8]. A Day-0 option is
  evaluated at the set's first `observer_places` entry (Troy for AEN-TROY);
  the `ida` rider of AEN-TROY-07 is the bearing from Troy to the landmark. In
  `operational_map.json` the reader flags the numeric thresholds that are the
  drafter's operationalisations [lcn §4.3; 13 rows 34–35].
- **The withdrawn eclipse classes** [r1 N11]. Several rows still cite
  revision 1's classes:
  - QS-SACK-06:a, ARG-RETURN-04:d (round 2) and IL-PATROCLUS-02's solar_am
    and solar_any require "a solar eclipse of class X1–X4 (DESIGN 3.1)";
  - `controls_real.json` cites "X3 ≥ 0.95, X4 ≥ 0.60".

  `operational_map.json` records one decision for all of them. "Class
  X1–X4" means X2 ∪ X3 ∪ X4 under revision 1's own definitions [v1 §3.1].
  In the bench's probabilistic terms that is h_06 ≥ 0.5 or h_tot ≥ 0.5 at
  the option's site and day. X3 and X4 alone map as in 6.3.3.
- **Round 2's new options** [lcn2 findings 3–4]. AEN-TROY-02:iii (the Moon
  below the horizon at the end of evening nautical twilight of Night 0, any
  phase) is a negated `moon_up`, and it is not eclipse-compatible. It comes
  with the pinned reading R-iii (02:iii, 04:a, 05:none, 07:vis7).
  ARG-RETURN-04:d (a solar eclipse of class X1–X4 at the set's first site on
  Day 0, maximum at any time the Sun is up) is a `solar_eclipse` with
  `x_class` X1–X4, mapped as above. Round 2 marked it as the checker's
  inference and stated the case against it (the text calls the darkness
  night, says no star or Moon was seen, and makes it last to dawn).

**The storm rule** (revision 5) [lcn2 finding 13(1)]. A darkness that the
text attributes to a storm (storm clouds, rain or wind, in a storm
narrative) is weather. It is never eclipse-compatible in the rule's gardens.

- **Why.** The drafter already excluded *Aen.* 3.195–204 ("involvere diem
  nimbi") on that ground, and kept out Valerius 1.617 and 1.670 and *Arg.*
  2.1102–1105 [neg §3.1; lcn2 finding 13(1)]. QS-SACK-06:a, Athena's storm
  ("σὺν δʼ ἔχεεν νεφέλας … νὺξ δʼ ἐχύθη περὶ γαῖαν", Quintus 14.461–462),
  was the one storm darkness given a solar-eclipse option. Round 2 found the
  treatment uneven and left the choice to the design.
- **The same rule for the Odyssey.** Theoclymenus' darkness (Od. 20.351–357)
  is a seer's vision with no storm, so the rule does not touch it.
  ARG-RETURN-04's "pall" is not attributed to a storm either, so its
  eclipse option stays. The Iliad's mist at 17.366 is not a storm, and the
  Iliad is reported only.
- **Direction.** The rule removes a reading from fiction, so it works
  against outcome 4, the claim it guards.
- **QS-SACK-06:a** leaves the rule's eclipse-compatible readings. QS-SACK with
  it restored is reported as a sensitivity, scored at its own day and site as
  below.

**Typical-number parity** [lcn2 finding 13(2)]. Outcome 4 compares 𝒢_j with
𝒢_BM*, whose F1b is off, so neither side jitters its stated day counts.
Parity holds for the rule. In the reported comparisons with 𝒢_DOC* and
𝒢_FULL*, where the Odyssey's gardens carry F1b, the negatives'
narrator-stated counts get the same ±2-day and ±3-day jitter: ARG-CIUS-06's
three days and twelve days and nights, IL-PATROCLUS-09's twelfth dawn, and
ARG-RETURN-02's two nights.

**Windows.** Each clean negative is searched in the Odyssey's own two
windows (reproduction, 136 years; primary, 251 years) at its own site. The
negatives tell events of the same legendary age, and these windows give
fiction exactly the chances the Odyssey had. Twenty further random positions
per width are a sensitivity.

**Gardens.** 𝒢_j is the full product of set j's fork options, with each F5
entry expanded into its tolerance and visibility variants [neg §1 item 6].
Its **eclipse-compatible readings** are those that contain an option listed
in the set's `eclipse_compatible_options`, less two kinds:

- lunar-eclipse options, which are not solar eclipses, as the file says;
- storm-darkness options, by the storm rule.

For the clean negatives that leaves AEN-TROY-02:ii-a, AEN-TROY-02:ii-b and
AEN-TROY-05:conj; ARG-RETURN-04:b and ARG-RETURN-04:d; and QS-SACK-02:c. The
negatives' readings were drafted without any target, so their G needs no
conditioning (5.3).

**The test** [rev #1 fix 3]:

- **hit_j** holds when some eclipse-compatible reading of 𝒢_j has, in one of
  the two windows, a unique survivor whose eclipse has h_tot ≥ M_Ody. Each
  option is evaluated at **its own day and its own site** [r1 N11 fix 2]:
  - a Day-0 option (AEN-TROY-02:ii-a, AEN-TROY-05:conj, QS-SACK-02:c,
    ARG-RETURN-04:d) at the set's first `observer_places` entry, on Day 0;
  - an option that places a conjunction within ±k days of Night 0
    (AEN-TROY-02:ii-b, ±1.5 d; ARG-RETURN-04:b, ±2 d) at the same place, on
    the date of that conjunction;
  - in the sensitivity run only, QS-SACK-06:a near Cape Caphereus on Day
    +2..+12.
- **Mapping a survivor to its eclipse** [r2 R2-12; revision 5 generalises
  it]. Every survivor of an eclipse-compatible reading is mapped to the
  conjunction that its eclipse-compatible option names, as F2 (c) and (d)
  map a candidate back in 5.3:
  - for a Day-0 option, the survivor itself;
  - for a ±k-day option, the conjunction within those days of Night 0;
  - for an eclipse option on another day, the conjunction of that eclipse.

  Conjunctions are 29.5 days apart, so there is at most one. Reach is then
  computed on the mapped dates, so hit_j and G_j refer to the same eclipse
  event.
- **G_j** is the mean reach_136, under 𝒢_j, over the set's targets: every
  conjunction in the core that falls in daylight at one or more of the
  set's `observer_places`. Its interval is the interval of 5.3, the wider of
  the gamma and the block-bootstrap intervals. G over the eclipse-compatible
  readings alone is reported beside; the full 𝒢_j can only be larger, which
  works against outcome 4.
- **Outcome 4 fires if some clean negative has hit_j and G_j,hi ≤ G_BM,u.**
  G_BM,u is the Odyssey's G under 𝒢_BM* over T, the same kind of
  unconditioned target set. It is the Odyssey's coincidence as B&M would
  present it, with every reading treated as blind, so the comparison
  favours B&M twice: 𝒢_j holds more readings than 𝒢_BM*, and the negative is
  taken at its upper bound.

Also reported per set:

- the survivors of each pinned reading (literal and BM-analogue; R-i, R-ii,
  R-ii-literal and R-iii for AEN-TROY);
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

## 7. Clues B&M did not use

These come from the 76-row inventory [txt §4], and none is used to fit
anything. In revision 4 this section carries the only evidence that can give
a "yes" (1.3). So it says:

- which clues are blind;
- how they are scored, and against which pool;
- how the chance of a "yes" is computed before the target is looked at.

### 7.1 The clues, and which are blind

A clue counts only if it meets two tests:

- its reading was formed without the target in view;
- nobody has evaluated it at the target before its predicate was frozen.

That is the uniform rule of 1.1 and 5.3, applied to the clues B&M cited as
support as well as to those they searched with.

| # | clue (lines; day) | predicate (frozen) | status |
|---|---|---|---|
| H1 | "this night is very long" (11.373; Day −7 seq); "these nights are endless" (15.392; Day −3) | night (Sun's centre below −0.833°) ≥ 12.0 h on that night | **not counted** [rev #11]. The threshold was set after the nights of 1178 BC (11.5 h and 11.3 h, a fail) had been computed [txt §5.6], and it measures the season that C already fixes. Reported |
| H2 | σκοτομήνιος, the dark night (14.457; night of Day −5 seq / −4 par) | Moon above the horizon for < 25% of the dark hours | **not counted** (new in revision 4). It fails both tests (below). Reported with its conditional base rate |
| H3 | Hermes leads the suitors' souls past the gates of the Sun (24.1–14; night of Day 0/+1) | **one predicate** [r1 N14]: Mercury is not visible (AV 10°) on the mornings and evenings of Day 0 and Day +1, **and** a geocentric conjunction of Mercury with the Sun in ecliptic longitude (inferior or superior) falls within ±3 d of noon (UT+2) on Day 0 or on Day +1 | **counted** |
| H4 | Ares and Aphrodite caught together (Demodocus, 8.266–366; Day −7 seq / −6 par [chron §2.1, §3.1]) | the geocentric Venus–Mars separation at 03:30 UT is ≤ 5° on some day within ±3 d of Day −7 (sequential) or Day −6 (parallel). The count used is the one on which the candidate passes a reading that defines its pool (7.2), and either count will do if it passes on both | **counted** |
| H5 | Mars invisible in March–April 1178 BC except during the eclipse | Mars not visible (AV 11.5°) on any morning or evening from Day −34 to Day 0 | **not counted**: B&M found it after the date [bm §2]. Reported |
| H6 | the twentieth year (9 lines); a year with Circe and seven with Calypso | the year lies 8–11 years after one of the ancient sack dates (Duris 1334/3 to Ephorus 1135, as in [win §3]; Clement's list [unread §4]) | external check, reported per survivor; strict Eratosthenes alone excludes 1178 BC [win §6] |
| H7 | Theoclymenus at the δεῖπνον; supper "in the light" (20.390–394, 21.428–429) | eclipse maximum in daylight on Day 0 | consistency only, for eclipse-compatible readings; "noon" is not in the text [txt §5.10] |
| H9 | frost feared (5.467, 17.25); hearths and fires (6.305, 7.153, 18.307–311, 19.63–64) | — | weather, not sky. Reported qualitatively, with the five scholia that read autumn or winter [txt §5.6] |
| H10 | nightingale (19.519), swallows (21.411, 22.240), gadfly (22.301 = 18.367) | — | similes, so excluded [txt §5.4]. 18.366–370 is also a wish, read as winter, May or autumn by different advocates, and is used for nothing [unread §2.3] |
| H11 | much-flowering wood (14.353) | — | inside a lying tale, so excluded |
| H12 | Laertes digging round a plant (24.226–231; Day +1) | — | qualitative |
| H13 | Helios' complaint (12.374–390), Poseidon and Zeus (13.125–158) | — | no operational predicate is defensible; listed, not run |

**Why H2 is no longer counted.** It fails both tests:

- **B&M cite 14.457** in support of their new moon. Their text calls it
  "Night −2" [bm-a, clue N; B&M §Method, SI Table S1].
- **Its value at 1178 BC was known.** The dossier computed the Moon's
  circumstances for the night after Day −5 of 1178 BC (moonrise about
  03:48 LMT) [txt §5.2]. That was before revision 1 froze the 25% threshold.
- **It is weak anyway.** Given a Day 0 at conjunction it passes about half
  the time [vis §4.5].

**Why H3 and H4 are blind.**

- **Nobody fitted them.** B&M do not treat the second Hermes journey or the
  song of Ares; neither is among their clues [txt §4 row 70; bm §5].
  Gainsford lists such god-movements as
  what a consistent Hermes = Mercury rule must also accommodate [crit §3.3].
- **They were frozen early.** Revision 1 wrote both predicates on
  2026-10-03 as tests of that consistency [v1 §5].
- **Nobody has evaluated them at the target.** A search of `docs/` and
  `results/` finds no computation of Mercury on Day 0 or of the Venus–Mars
  separation for 1178 BC. This revision's estimate masked the target (2.9).
- **The inference to the contrary is not a computation.** One inference from
  documented numbers says H4 should fail (2.10). That inference is not a
  computation, and the predicate was not tuned to it.

**What H3 and H4 test.** They test B&M's own encoding hypothesis, that the
poet turned god-movements into planets. If the hypothesis is right, the
other god-movements of the same story should match the same sky. That is
the evidence a "yes" can rest on.

### 7.2 The counted statistic: an exact rank test on two pools (a rule input)

- **Two null pools** (4.2). Both are drawn from P_all over the whole
  background, −1999..+200. No core is needed, because no window is placed.
  - **P_BM**: the candidates that pass at least one reading of 𝒢_BM*
    (revision 4's pool).
  - **P_MWRA** (revision 5): the candidates that pass at least one of the
    twelve MWRA readings of 𝒢_BM*, that is, C on a day count, a Venus lead
    of at least 90 min on that count's Venus day, and a morning
    rise-azimuth maximum within 3.5 d of that count's Mercury day. P_MWRA ⊂
    P_BM.
- **Why two** [rev #11 fix 1]. The test must compare the target with
  candidates that pass the same N, C, V and M.
  - H3 depends on Mercury's phase, which M fixes. H4 depends on Venus'
    elongation, which V fixes.
  - The target passes only B&M's applied Mercury event, the MWRA (2.9, "the
    target under 𝒢_BM*"). A candidate admitted through a greatest elongation
    or a station has Mercury in another phase at Day −34, and so possibly on
    Day 0. P_MWRA is matched to the reading the target passes; P_BM is
    larger and so has a finer lattice.
  - On the rough rows the two classes of P_BM do not differ in H3 or H4
    (2.9), but the bench does not lean on that.
- **Neither pool depends on the slot definitions of 4.2,** so outcome 1 is
  free of R2-2's slot question. **Day and night conjunctions both enter,**
  because neither predicate depends on daylight, and taking both doubles
  the pools.
- **The score.** In each pool P, s(t) = Σ_{i ∈ {3, 4}} pass_i(t) · (−log10 q_i).
  - q_i is the pass rate of H_i over P ∪ {t_S}.
  - It is computed at the target-side stage, symmetrically in every member,
    so the test is exact.
  - A rarer predicate weighs more. The order of scores is then: passes both;
    passes the rarer predicate only; passes the commoner only; passes
    neither.
- **The p-value of a pool.** p_P = (1 + #{u ∈ P : s(u) ≥ s(t_S)}) / (1 + n_P).
  Ties count against the target.
  - **Membership.** The target must itself pass a reading that defines the
    pool, under the bench's conventions (4.2), or it is not exchangeable
    with the pool's members. If it fails every such reading, p_P is set
    to 1.
- **p_H := max(p_BM, p_MWRA).**
  - **Why it is exact.** Under H0, that the text is unrelated to the sky of
    1178 BC, suppose either pool is exchangeable with the target. Then that
    pool's p satisfies P(p_P ≤ α) ≤ α for every α, and p_H ≥ p_P. So
    P(p_H ≤ α) ≤ α, with no approximation and no interval, **if either pool
    is exchangeable**. A referee who doubts one pool's matching cannot fault
    the test on that ground.
  - **The cost.** Label 1 now needs both pools to agree. On the design-stage
    lattice the two give the same verdict in every cell (below).
  - **Exchangeability and the eclipse.** The target was chosen for its
    eclipse. Neither predicate involves the lunar node, so eclipse status
    should not change their rates. P10 tests that on P_spring, and R20
    tests the homogeneity of P_BM across Mercury events.
- **Attainability, a null-side quantity** [r2 R2-1 fix 4].
  p_H,min = max over the two pools of (1 + x_max,P)/(1 + n_P), where x_max,P
  is the number of members of P that pass both predicates. A target passing
  both earns exactly p_H,min.
  - **When.** p_H,min is computed at the null-side stage, with the target
    masked (12.3), before any target-side number.
  - **Design-stage values** [2.9; me: heldout_attain.py and
    heldout_strata.py]: P_BM n 76, x_max 1, floor 0.026; P_MWRA n 43,
    x_max 0, floor 0.023. So **p_H,min = 0.026**.
  - **The lattice** (p_BM / p_MWRA → p_H): passes both, 0.026 / 0.023 →
    **0.026**; H4 only, 0.039 / 0.045 → **0.045**; H3 only, 0.221 / 0.227
    → **0.227**; neither, 1.
  - **Q_attain** holds if the measured p_H,min exceeds 0.05.
- **In the rule.** Label 1 needs p_H ≤ 0.05 (9.2).

### 7.3 Reported beside the rule

- each predicate at the target, with its margin, and the target's
  membership of each pool;
- p_BM and p_MWRA separately, with each pool's n and lattice;
- H1, H2 and H5 at the target, with their base rates over both pools. These
  are never counted;
- **the homogeneity of P_BM** (R20): the H3 and H4 pass rates of its MWRA
  class and of its GWE-or-station class, with Fisher's exact p;
- **sensitivity pools.** The test is rerun on T_A(v) for every variant of
  4.2, over the whole background, in daylight. These pools are matched only
  on the categorical slots, so they are not the rule's pools. At the design
  stage their p_H,min values are 0.009–0.012 (2.9);
- the pass rates of H1–H5 among R_anc's survivors, the ancient autumn reading
  [rev #11 fix 3]. R_anc has no planets, so no rank test is run on it;
- **the *Almagest* calibration of the test.** The same rank test is applied
  to the true dates of real records, with their non-B&M rows held out (6.4;
  Q_H).

Power is low: two predicates, and pools of about 76 and 43. The lattice
shows that a target can reach p ≤ 0.05 only by passing H4. The report says
so.

---

## 8. Pre-registered predictions

Written 2026-10-04, before any null model, control search or held-out check
of the bench was run. Each prediction names its quantity, the script that
computes it and the threshold that decides it.

Revision 4 renumbers the list again [r2 R2-5]:

- The column "v3" gives revision 3's number.
- Revision 3's predictions that the recheck found settled or nearly settled
  have moved to section 2 (table 2.7). The ones that remain checkable are
  now regression expectations.
- The regression expectations are listed first. They need the full run to
  be confirmed, but they are implied by numbers already known, and a
  confirmation is not counted.

Revision 5 keeps the numbering and changes five entries:

- P4 is withdrawn to R19, because about two survivors are expected and the
  comparison has no power (2.4) [14.4 #66].
- R20 is new: the homogeneity of the held-out pool P_BM (2.9, 7.2).
- R12 and R18 now read the two-pool rule of 7.2.
- R8, R10 and P20 name their sets in Appendix T, because the per-set
  pattern is truth-side.

### 8.1 Regression expectations (implied by section 2; not counted)

| # | expectation | v3 | basis |
|---|---|---|---|
| R1 | Regression checks A1–A5 pass (`reproduce.py`) | R1 | 2.2, 3.4 |
| R2 | 16 Apr 1178 BC passes N, C, V and M in every cell of the T0 grid, so T0_pass is true | R2 | 2.2 |
| R3 | With E off, the N ∧ C ∧ V ∧ M survivors in 1250–1115 BC number at least 2 and include 18 Mar 1189 BC | R3 | 2.2 |
| R4 | With E ≤ 5 Apr and with E ≤ 6 Apr the survivor set is exactly {16 Apr 1178 BC}; with E ≤ 4 Apr it is empty | R4 | 2.2 |
| R5 | T0 is RE in the primary cell and in every cell with E ≤ 5 or ≤ 6 Apr, and NR in every cell with E ≤ 4 Apr | R5 | 2.2 |
| R6 | The half-open UT+2 window holds 1,683 conjunctions | R6 | 2.2 [rev #22] |
| R7 | In the DE431 pairing the per-model P(total) values move from the canon-frame table of 2.3 by the equivalent of about 40 s. The orderings (1131 above 1178 except under the SMH2016 parabola) and the joint bounds (≤ 0.06 for three models, ≥ 0.08 for SMH2016) are unchanged (`deltat.py`) | R7 | 2.3 [r1 N7] |
| R8 | strict_PCR = 4: the accepted dates fail a primary row in three counted sets, named in [AppT 6] (`controls.py`) | R8 | 2.6 |
| R9 | rec_ALM_BM ≤ 5, so Q_BM holds (`almagest.py`) | R9 | 2.6 |
| R10 | In regime SL, with the ceiling tolerances and the word-only projection of 6.4, the truth is in the best-fit set B of exactly 9 counted *Almagest* sets; the two exceptions are named in [AppT 6]. Revision 5's projection changes (A.10 and B.5 none; the literal `same_apparition` options) only loosen rows, so they cannot lose a retained truth (`almagest.py`) | R10 | 2.6, 6.4 |
| R11 | R_anc with the eclipse clue counts 30 Sep 1131 BC among its survivors in 1250–1115 BC under the Hesiod-or-Geminus bound, and not 16 Apr 1178 BC. It has about 9 survivors there, so it is not unique. Without the eclipse clue it has no unique survivor in any window (`garden.py`) | R11, P19 | 2.8, 2.9 |
| R12 | Label 1 does not fire, because H4 fails at 1178 BC and p_H is then at least about 0.23 (`heldout.py`) | — (replaces R12 of v3) | 2.10, an inference, not a computation |
| R13 | λ(N ∧ C ∧ V ∧ M) over the background lies in [0.44, 1.76] per century, near the lower bound | P4 | 2.9 |
| R14 | The background holds about 12 survivors of the T0b reading, and the Poisson P(≥ 1 in 136 years) is about 0.53 | P6 | 2.9 |
| R15 | r_Ody = 11/136 = 0.0815, unless the bench's vertex puts 26 Mar 1111 BC within ±1.5 d, in which case r_Ody = 0 and label 2 takes its "no match" form. Both branches are reported, with that candidate's ΔMWRA and flatness flag (`garden.py`) | P12 | 2.9 |
| R16 | BF_BM(ρ = 1) < 5 (about 2.6) | P32 | 2.9 |
| R17 | Under v1, G_BM lies in [0.05, 0.40] and is at least 2 × p_fix,unique. Over the slot family, label 2's G leg does not fire, and Q_tol and Q_slot hold (`garden.py`) | P13, P14, P34 | 2.9, 2.10 |
| R18 | p_H,min ≤ 0.05 on both held-out pools (design stage: P_BM 0.026, P_MWRA 0.023), so Q_attain does not hold (`attain.py`) | — | 2.9, 7.2 |
| R19 | λ(N ∧ C ∧ V ∧ M ∧ E_rel) at n = 3, 4 and 5 over the background, each with its exact Poisson 95% interval, beside B&M's printed 0.048 per century and their own arithmetic's 0.14. At n = 4 about 1.9 survivors are expected (0.087 per century), so the interval contains 0.048 unless the count reaches 4, which has probability about 0.13. Withdrawn from the counted list as revision 4's P4, because a count this small cannot decide a threshold near 0.048 (`rates.py`) | P5 (v4 P4) | 2.4 [rev #5] |
| R20 | H3 and H4 pass at the same rate in P_BM's MWRA class and in its GWE-or-station class: Fisher's exact p > 0.05 for each (rough: H3 8/43 against 7/33, p 0.78; H4 1/43 against 1/33) (`heldout.py`) | — | 2.9 |

### 8.2 Predictions (counted)

**Reproduction (T0; `reproduce.py`)**

- **P1.** With C_rel and E_rel in place of the fixed Julian bounds, the
  reproduction-window survivor sets of R3 and R4 are unchanged. (v3 P1)
- **P2.** The T0b survivor sets (E off; E ≤ 5 Apr) do not change when the
  clock ΔT is replaced by SMH2020, SMH2020 + 1σ and SMH2020 − 1σ with DE431
  conjunctions. (v3 P2)
- **P3.** The T0b survivor set with E off is the same under MWRA_vtx at
  ±1.5 d (primary), MWRA_vtx at ±1 d and MWRA_int at ±1 day [r1 N13]. (v3 P3)

**Rates (N1; `rates.py`)**

- **P4.** *Withdrawn in revision 5* to the reported comparison R19. It
  predicted λ(N ∧ C ∧ V ∧ M ∧ E_rel, n = 4) ≥ 0.07 per century, against
  B&M's printed 0.048. On known numbers the expected count is about 1.9
  over the whole background (2.4), so the outcome would be decided by
  Poisson noise, not by B&M's arithmetic [14.4 #66]. The number is kept so
  that no other prediction is renumbered. (v3 P5)
- **P5.** Survivors cluster: for the T0b reading, the empirical P(≥ 1
  survivor in a 136-year window), with windows slid one year at a time over
  the background, is below the Poisson value at the same mean count. The
  causes are Venus' 8-year cycle and Mercury's 13- and 46-year
  near-repeats. (new; replaces v3 P6, whose thresholds the known rate
  already sat on [r2 R2-5])
- **P6.** p_fix|C lies in [0.002, 0.02], and the unconditional p_fix in
  [0.0002, 0.002]. The recheck's rough p_fix|C, 0.0054, lies well inside;
  the exact value is new. (v3 P7)
- **P7.** The V–M dependence ratio on P_spring lies in [0.5, 2], with
  permutation p > 0.05 (rough value 0.76). (v3 P8)
- **P8.** Under C_rel, λ(N ∧ C ∧ V ∧ M) in the first and in the last 700
  years of the background agree within a factor 2. Under the fixed Julian
  bounds, fewer than 90% of the candidates that pass the fixed C in
  −1999..−1800 also pass C_rel. (v3 P9)

**The eclipse coincidence (N2; `coincidence.py`)**

- **P9.** p_e(M_Ody) over P_spring is within a factor 2 of p_e(M_Ody) over
  P_day, with 16 Apr −1177 excluded from both. (v3 P10)
- **P10.** V and M, and the held-out predicates H3 and H4, pass at the same
  rates on eclipse and on non-eclipse spring new moons (permutation p > 0.05
  for each). The exactness of p_H rests on this for H3 and H4 (7.2).
  (v3 P11, extended)

**Forking paths (N3; `garden.py`)**

- **P11.** Some reading of 𝒢_DOC*^X makes 30 Sep 1131 BC the unique survivor
  of a 136-year window containing it. (v3 P15)
- **P12.** Some reading of 𝒢_FULL*^X makes 24 Jun 1312 BC the unique
  survivor of a 251-year window containing it. (v3 P16)
- **P13.** G_X(𝒢_BM*) lies within a factor 2 of G_BM,u: eclipse dates are
  not specially reachable. (v3 P17)
- **P14.** The greedy smallest fork set that brings G over T_A(v1) to 0.20
  adds at most four options to 𝒢_BM*. (v3 P18)
- **P15.** G_DOC ≥ 2 × G_BM under v1. (v3 P14, second clause; its first
  clause is settled, 2.7)

**Random epics (N4; `randomepic.py`)**

- **P16.** For variant A epics, P(unique survivor in a 136-year window) lies
  in [0.2, 0.6], and P(T_best ≥ T_obs) ≥ 0.2. (v3 P20)
- **P17.** Ē_N4, the mean reach of Schoch's target over entering stratum
  epics, lies within a factor 3 of G_BM under v1. Varying the poem and
  varying the target give the same null mean [r1 N10]. (v3 P21)
- **P18.** If r_Ody > 0, pct_N4 lies in [0.05, 0.50]: the Odyssey's reach of
  Schoch's target is neither exceptional nor ordinary among random poems of
  its specificity. Among T_A targets, 19.8% reach at least r_Ody [r2], but
  epics are not targets, and the value is new. (new)

**PC-S (`synthetic.py`)**

- **P19.** The B&M reading's recall at j = 3 is at most half its recall at
  j = 0. (v3 P23)

**Controls (`controls.py`, `almagest.py`, `negatives.py`)**

- **P20.** seen_PCR ≥ 4, with the per-set pattern of seen and unseen sets
  written in [AppT 6]. Revision 4 printed the pattern here; it moved because
  part of its basis is truth-side. The prediction holds only if both the
  count and the pattern hold. (v3 P24)
- **P21.** seen_ALM_SL ≥ 6: at least 6 of the 9 sets that retain their truth
  (R10) also narrow their window to 5%. (v3 P25)
- **P22.** Q_ΔT does not hold. (v3 P26)
- **P23.** Q_exposure does not hold. (v3 P27)
- **P24.** Q_H does not hold: at least 6 of the 11 counted *Almagest* sets
  give their true date p ≤ 0.05 on their own held-out rows (6.4). Only 8
  sets have held-out rows, so this needs 6 of those 8. (v4)
- **P25.** No clean negative fires outcome 4, and at least one clean
  negative has a unique survivor of some kind in one of the two Odyssey
  windows. (v3 P28)
- **P26.** Some eclipse-compatible reading of IL-PATROCLUS makes an eclipse
  new moon with h_09 ≥ 0.5 at Troy the unique survivor of the 251-year
  primary window. (v3 P29)

**Bottom line (`verdict.py`)**

- **P27.** The verdict is exactly {inconclusive}. Its qualifiers are exactly
  Q_BM, Q_tol and Q_slot. This is the conjunction of P18, the first branch
  of R15, P20–P25 and the expectations R8, R9, R12 and R17. It fails if any
  of them fails, including when r_Ody = 0 gives label 2 its "no match" form.
  (replaces v3 P34 and P35, which were settled or covered both branches
  [r2 R2-5])

---

## 9. The decision rule

### 9.1 Named quantities

One script computes each quantity the rule reads, and writes it to one JSON
key stamped with the frozen code tree hash (section 12). The **stage** column
says when the quantity may first be computed (12.3):

- **null:** at the null-side stage, with the target masked;
- **target:** after the second freeze;
- **controls:** after the second freeze; the target is not involved.

| quantity | definition | stage | section | written by |
|---|---|---|---|---|
| INSTR | the instrument checks that guard rule inputs all pass: I1, I2, I2b, I4–I9, I11, I13–I15 | each check at its own stage | 6.1 | `results/instrument/summary.json` |
| T0_pass | 16 Apr 1178 BC passes N, C, V and M (E off) in the primary cell | target | 3.5 | `reproduce.py` |
| T0 (reported) | R, RE or NR in the primary cell | target | 3.5 | `reproduce.py` |
| p_H,min; n_P, x_max,P for P ∈ {P_BM, P_MWRA} | the floor of the held-out test: max over the two pools of (1 + x_max,P)/(1 + n_P) | null | 7.2 | `attain.py` |
| p_H; p_BM, p_MWRA; the target's membership of each pool | the held-out exact rank p-value of 1178 BC: max(p_BM, p_MWRA), a pool's p being 1 if the target fails every reading that defines it | target | 7.2 | `heldout.py` |
| G_BM(v), G_BM,lo(v), G_BM,hi(v); n_A(v), k_A(v), for v ∈ {v0, …, v5} | G(𝒢_BM*; T_A(v); W = 136) with the interval of 5.3 | null | 4.2, 5.3 | `attain.py` |
| G_BM,u; n_T | G(𝒢_BM*; T; W = 136); equal to (n_A(v)/n_T) G_BM(v) for v1–v5 | null | 5.3 | `attain.py` |
| r_Ody | reach_136(16 Apr −1177; 𝒢_BM*) | target | 5.3 | `garden.py` |
| pct_N4, pct_N4,lo, pct_N4,hi; x_gt, x_eq, n_stratum | the mid-p percentile of r_Ody among entering stratum epics, with bounds from the strict and weak counts; undefined when r_Ody = 0 | target | 5.4 | `randomepic.py` |
| seen_PCR, strict_PCR | of the 7 counted PC-R sets: seen; strict recall (ΔT mixture) | controls | 6.3.2–6.3.3 | `controls.py` |
| seen_PCR,redraft; seen_PCR,sibling | seen_PCR with the five re-drafted primaries; with every audited row at its failing sourced sibling convention | controls | 6.3.4 | `controls.py` |
| seen_PCR,noncirc | seen_PCR with the circular sets' ΔT σ tripled | controls | 6.3.3 | `controls.py` |
| seen_ALM_SL, rec_ALM_BM | of the 11 counted *Almagest* sets: seen in regime SL (ceiling tolerances, leave-one-set-out); strict recall with narrowing in regime BM | controls | 6.4 | `almagest.py` |
| held_ALM | of the 11 counted *Almagest* sets, the number whose true date has p ≤ 0.05 on the set's held-out rows | controls | 6.4 | `almagest.py` |
| hit_j, G_j, G_j,hi; n_j | for each of the 12 clean negatives | controls | 6.5 | `negatives.py` |

No likelihood ratio, Bayes factor, PC-S recall or G_DOC is a rule input.
They are reported (1.3, 5.3, 5.7, 6.2). The thresholds are in
`data/prereg/verdict_rule.json` and are frozen at the first freeze, before
any of these quantities is computed.

### 9.2 The rule

`odybench/verdict_rule.py` implements exactly this, as a pure function of the
quantities above:

```
if not INSTR:                                         return BLOCKED (no verdict is read)
labels, qualifiers = {}, {}

# gates and control qualifiers
if seen_PCR < 4:                                      labels += 3a
if seen_ALM_SL < 6:                                   labels += 3b
if rec_ALM_BM < 6:                                    qualifiers += Q_BM
if held_ALM < 6:                                      qualifiers += Q_H
if strict_PCR < 4:                                    qualifiers += Q_strict
side = (seen_PCR < 4)
if (seen_PCR_redraft < 4) != side or (seen_PCR_sibling < 4) != side:
                                                      qualifiers += Q_exposure
if (seen_PCR_noncirc < 4) != side:                    qualifiers += Q_dT

# null-side qualifiers (known at the second freeze)
p_H_min = max(p_min[P] for P in (P_BM, P_MWRA))       # (1 + x_max,P)/(1 + n_P), 7.2
if p_H_min > 0.05:                                    qualifiers += Q_attain
g2  = {v: G_BM_lo[v] >= 0.20 for v in SLOTS}           # SLOTS = v0..v5
tol = {v: G_BM_lo[v] >  0.05 for v in SLOTS}
if all(tol.values()):                                 qualifiers += Q_tol
if len(set(g2.values())) > 1 or len(set(tol.values())) > 1:
                                                      qualifiers += Q_slot

# 4: the method dates fiction
if any(hit_j and G_j_hi <= G_BM_u for j in clean_negatives):
                                                      labels += 4

# 2: B&M's match carries no weight
if r_Ody == 0:                                        labels += "2 (no match)"
elif all(g2.values()) or pct_N4_lo >= 0.50:           labels += "2 (ordinary)"

# 1: the text dates the return, by the clues nobody fitted
p_H = max(p[P] for P in (P_BM, P_MWRA))              # p[P] = 1 if the target is not a member of P
if T0_pass and p_H <= 0.05 and not ({3a, 3b, 4} & labels):
                                                      labels += 1

if labels is empty:                                   labels = {inconclusive}
return labels, qualifiers
```

U0(n) = 3.69/n is the gamma upper bound of a G with no target reached.
CP_hi(x, n) is the Clopper–Pearson 97.5% bound.

### 9.3 How to read it

- **Every rule names its garden, its pool and its stage** [rev #1 fix 1]:
  - 𝒢_BM* over T_A(v) prices B&M's tolerances (label 2's G leg, Q_tol).
  - 𝒢_BM* over T enters only the comparison with fiction, whose readings
    are blind (label 4).
  - P_BM, the candidates that 𝒢_BM* accepts, and P_MWRA, those that pass
    the Mercury event B&M applied, are the null pools of the held-out test
    (label 1); the rule reads the larger p.
  - The verdict recomputed with 𝒢_DOC* and 𝒢_FULL* in place of 𝒢_BM*, with
    the E-on gardens, and with revision 2's pool T_C, is printed beneath it
    as a sensitivity. It never replaces the verdict.
- **Why "yes" rests on the held-out test** [r2 R2-1]. Each of revision 3's
  three "yes" conditions was fixed by the sky before the Odyssey was
  measured:
  - G_BM is about 0.14 by the sky alone;
  - T0 = R needs 18 Mar 1189 BC to fail, and it passes;
  - pct_N4 ≤ 0.05 is a reach percentile of the same kind as G.

  A test whose most extreme possible observation cannot reach 5% has no
  power, and its "no" means nothing. The held-out test's floor p_H,min is
  computed before the target is looked at. Q_attain prints it with every
  verdict.
- **Why T0_pass and not T0 = R.** The uniqueness of 1178 BC in B&M's window
  is a property of the other candidates. Its weight is what G measures, and
  G shows it carries little (Q_tol).
- **G has one sense throughout**: a look-elsewhere-corrected p-value, small
  when the coincidence is notable.
  - Label 2 needs it large.
  - Q_tol says it cannot be small.
  - Outcome 4 asks whether fiction's is as small as the Odyssey's.
- **Bounds work against the claim being made** [r1 N8 fix 2]:
  - label 2's G leg and Q_tol use G_BM,lo under every slot variant, so the
    variant most favourable to B&M decides;
  - label 2's pct leg uses the lower bound from the strict count, so ties
    favour the Odyssey [r2 R2-3];
  - outcome 4 uses the negative's upper bound;
  - label 1's p_H is exact, ties count against the target, and it is the
    larger of two pools' p-values, so it stays valid if either pool is
    exchangeable with the target (7.2).
- **Why 0.05 and 0.20 over T_A.** These thresholds were written in revision
  3 (2026-10-04, file time 03:21 local), before the recheck estimated G_BM
  (its `check_gbm.py` ran from 03:35, and its report is timed 03:53).
  Revisions 4 and 5 keep them unchanged, and the order is recorded here [r2
  R2-1 fix 1]. They are frozen at the first freeze, before the bench
  computes any G.
  - Revision 2's thresholds, 0.01 and 0.05, were set for G over T_C. For
    𝒢_BM*, G over T_C is (n_A/n_TC) × G over T_A, about 0.147 × G over T_A
    [r2], because targets outside A are never reached (4.2).
  - Revision 2's 0.01 therefore corresponds to about 0.07 over T_A, and its
    0.05 to about 0.34.
- **Label combinations.** Labels 2, 3a, 3b and 4 can hold together, and 1
  can hold with 2. The headline leads with 3a or 3b when either holds,
  because they say which "no"s mean nothing. It then gives 1, 2 and 4, in
  that order.
- **When 1 and 2 hold together**, the headline reads: the clues nobody
  fitted date the return, and B&M's own match is not what shows it.

### 9.4 Structural constraints: what an input set must satisfy to be realisable

A synthetic input set proves an outcome reachable only if real data could
produce it. Revision 3's set S1 used G_BM = 0.0065 with three targets
reached. T0b's single reading already reaches four, and the whole garden
about 26, so S1 could not occur, and nothing in revision 3's constraints
caught it [r2 R2-1].

**Two kinds of input are therefore kept apart:**

- **Null-side fields** are fixed by the sky and the readings. A set that
  claims reachability must use the measured values. Until the null-side
  stage those are the design-stage estimates of 2.9.
- **Target-side and control fields** are free, subject to their lattices and
  intervals.

I14(b) checks every set against C1–C9. I14(c) reruns the sets at the
null-side stage with the measured values.

| # | constraint | why |
|---|---|---|
| C1 | 0 ≤ G_lo ≤ G ≤ G_hi ≤ 1 for every G, and G_hi ≥ U0(n) = 3.69/n with n its pool size | the interval of 5.3 |
| C2 | G_BM,u = (n_A(v)/n_T) · G_BM(v) for v1–v5, the same number for each | no target outside T_A(v) is reached by 𝒢_BM* (4.2) |
| C3 | if r_Ody = 0, pct_N4 is undefined; otherwise pct_N4,lo ≤ pct_N4 ≤ pct_N4,hi, each computed from integer counts x_gt, x_eq and n_stratum ≥ 200 as in 5.4 | 5.4 |
| C4 | if hit_j, then G_j > 0 and G_j,hi ≥ U0(n_j) | a unique survivor in the core has reach > 0 |
| C5 | the counts are integers: 0 ≤ seen_PCR, strict_PCR and the other PC-R counts ≤ 7; 0 ≤ seen_ALM_SL, rec_ALM_BM ≤ 11; 0 ≤ held_ALM ≤ 8 | definitions; three counted sets have no held-out row (6.4) |
| C6 (attainability) | outcome 1 is attainable only if p_H,min ≤ 0.05. Outcome 4 is attainable only if G_BM,u ≥ U0(n_j) | 7.2, C4 |
| C7 (the null side is fixed) [r2 R2-1 fix 2] | the null-side fields (n_T, n_A(v), G_BM(v) with bounds, G_BM,u; for each held-out pool its n, x_max and the counts of members passing H3 and H4; p_H,min) equal the design-stage estimates of 2.9, or after the null-side stage the measured values. A set that departs from them is marked **branch test**. It shows that a code branch works, and proves no outcome reachable | R2-1 |
| C8 | in each pool P, p_P = (1 + x)/(1 + n_P) for an integer x with x_max,P ≤ x ≤ n_P, x fixed by the target's pass pattern (both, H4 only, H3 only, neither) and the pool's counts; p_H = max(p_BM, p_MWRA) ≥ p_H,min. With the design-stage counts the attainable values of p_H are 0.026 (both), 0.045 (H4 only), 0.227 (H3 only) and 1 (neither) | 7.2 |
| C9 | T0 ∈ {R, RE} implies T0_pass | 3.5 |

**Known facts, not constraints.** Some target-side and control facts are
already known or inferred:

- T0_pass is true and T0 is RE;
- H4 is inferred to fail, so p_H ≥ 0.23 (2.10);
- the target passes MWRA readings, so it is a member of both pools (2.9);
- rec_ALM_BM ≤ 5;
- seen_ALM_SL ≤ 9;
- strict_PCR = 4 (rough).

A realisable set may contradict these, because the rule must also be shown to
work for data that differ from the Odyssey's. Each set that does is marked
in 9.5. What a realisable set may not contradict is the null side.

### 9.5 Synthetic input sets that prove every outcome reachable

`data/prereg/verdict_synthetic/*.json` holds these inputs.
`tests/test_verdict.py` asserts the stated output for each (I14a) and checks
it against 9.4 (I14b). `results/design-revision-v5/verdict_trace.py` is an
executable transcription of 9.2 and of C1–C9 for revision 5. It computes
each pool's p from the target's pass pattern and the pool's counts, with the
weights of 7.2 taken over pool and target, and it reproduces every label,
qualifier and realisability mark of the table below [me: the script and its
`.out.txt`]. Revision 4's sets are kept under their names, and S12 and S13
are new.

**The four outcomes, one set each** (with S0, inconclusive): **S1** reaches
outcome 1, **S2** outcome 2 (and S2nm its "no match" form), **S3a** and
**S3b** the two parts of outcome 3, and **S4** outcome 4. All five are
realisable: their null side is the design-stage estimate of 2.9.

**The base set, S0.** Every other set starts from it and lists only what
differs.

- **The rule:** INSTR true; T0_pass true, T0 RE.
- **The null side, at the design-stage estimates of 2.9:**
  - G_BM by variant: v0 0.224 [0.139, 0.344]; v1 0.140 [0.087, 0.215]; v2
    0.211 [0.131, 0.324]; v3 0.278 [0.172, 0.427]; v4 0.182 [0.112, 0.279];
    v5 0.327 [0.203, 0.504];
  - n_T 10,690; G_BM,u 0.00172;
  - P_BM: n 76; 14 members pass H3 only, 1 H4 only, 1 both. P_MWRA: n 43;
    8 pass H3 only, 1 H4 only, none both. p_H,min = max(0.0260, 0.0227) =
    0.026.
- **The target side:**
  - the target is a member of both pools and passes H3 only: p_BM 0.221,
    p_MWRA 0.227, so p_H = 0.227;
  - r_Ody 0.0815;
  - pct_N4: x_gt 30, x_eq 10 of n_stratum 200, giving 0.175 [0.104, 0.262].
- **The controls:**
  - seen_PCR 5, strict_PCR 4, redraft 5, sibling 5, noncirc 5;
  - seen_ALM_SL 7, rec_ALM_BM 3, held_ALM 8;
  - every negative: hit false, G_j 0.0006, hi 0.0012, n_j 10,690.

| set | differs from S0 | labels | qualifiers | null side (C7) | contradicts a known fact? |
|---|---|---|---|---|---|
| **S0** | — | **{inconclusive}** | Q_BM, Q_tol, Q_slot | realisable | none |
| **S1** | the target passes H3 and H4: p_BM 0.026, p_MWRA 0.023, so p_H 0.026 | **{1}** | Q_BM, Q_tol, Q_slot | realisable | H4 inferred to fail |
| S1b | H4 only: p_BM 0.039, p_MWRA 0.045, so p_H 0.045 | {1} | Q_BM, Q_tol, Q_slot | realisable | H4 inferred to fail |
| **S2** | pct_N4: x_gt 118, x_eq 12, giving 0.620 [0.518, 0.716] | **{2 (ordinary)}** | Q_BM, Q_tol, Q_slot | realisable | none |
| **S2nm** | r_Ody 0; pct_N4 undefined | **{2 (no match)}** | Q_BM, Q_tol, Q_slot | realisable | none (the branch R15 allows) |
| **S3a** | seen_PCR 2, redraft 2, sibling 2, noncirc 2 | **{3a}** | Q_BM, Q_tol, Q_slot | realisable | none |
| **S3b** | seen_ALM_SL 3 | **{3b}** | Q_BM, Q_tol, Q_slot | realisable | none |
| **S4** | AEN-TROY: hit true, G_j 0.00051, hi 0.00112 | **{4}** | Q_BM, Q_tol, Q_slot | realisable | none |
| S5 | as S1, but 4 members of P_BM pass both, so p_H,min = p_H = 0.0649 | {inconclusive} | Q_BM, Q_tol, Q_slot, **Q_attain** | **branch test** | — |
| S6 | as S1, with S2's pct_N4 | {1, 2 (ordinary)} | Q_BM, Q_tol, Q_slot | realisable | H4 inferred to fail |
| S6b | as S2, but seen_ALM_SL 3, held_ALM 4, strict_PCR 2, redraft 3, noncirc 3; AEN-TROY as S4 | {2 (ordinary), 3b, 4} | Q_BM, Q_H, Q_strict, Q_exposure, Q_ΔT, Q_tol, Q_slot | realisable | none |
| S7 | INSTR false | BLOCKED | — | realisable | — |
| S8 | as S1, but T0_pass false (T0 NR) | {inconclusive} | Q_BM, Q_tol, Q_slot | realisable | T0_pass expected true |
| S9 | as S1, but seen_PCR 3, redraft 3, sibling 3, noncirc 3 | {3a} | Q_BM, Q_tol, Q_slot | realisable | H4 inferred to fail |
| S10 | every variant at v5's values: G_BM 0.327 [0.203, 0.504], n_A 56 | {2 (ordinary)} | Q_BM, Q_tol (no Q_slot) | **branch test** | — |
| S11 | as S1, but rec_ALM_BM 7 and held_ALM 4 | {1} | Q_H, Q_tol, Q_slot | realisable | rec_ALM_BM ≥ 6 |
| S12 | as S1, but the target is not a member of P_MWRA, so p_MWRA = 1 and p_H = 1 | {inconclusive} | Q_BM, Q_tol, Q_slot | realisable | the target passes MWRA readings (2.9) |
| S13 | as S1b, but 2 members of P_MWRA pass H4 only: p_BM 0.039, p_MWRA 0.068, so p_H 0.068 | {inconclusive} | Q_BM, Q_tol, Q_slot | **branch test** | — |

**What each set shows:**

- **The four outcomes and the inconclusive verdict.** S1 reaches 1, S2 and
  S2nm reach 2 in both forms, S3a and S3b reach 3 in both parts, S4 reaches
  4, and S0 is inconclusive.
- **All of these are realisable.** Their null side is the design-stage
  estimate. The only known fact S1 contradicts is the inferred failure of
  H4, which is target-side.
- **Two ways to a "yes".** S1 passes both held-out predicates; S1b passes H4
  alone, and on the design-stage counts both pools still put it below 0.05.
- **What blocks label 1:** a gate (S9); T0_pass false (S8); a target outside
  one of the pools (S12); or one pool's p above 0.05 while the other's is
  below it (S13, a branch test, because on the design-stage counts the two
  pools agree in every cell).
- **What does not block it:** Q_BM and Q_H. S11 shows label 1 with Q_H and
  without Q_BM. Q_H conditions the held-out "no"s; a "yes" from the exact
  test is valid without it (7.2).
- **Co-occurrence.** S6 shows labels 1 and 2 together. S6b shows labels and
  every control qualifier together.
- **Branch tests.** S5 shows the Q_attain branch, S10 the label-2 G leg and
  S13 the max over the pools. Each needs null-side values that contradict
  2.9, so none proves an outcome reachable.
- **S7** shows the instrument block.

**At the null-side stage** (12.3), I14(c) replaces the null-side fields by
the measured values and reruns S0–S13. Each set keeps the target's pass
pattern (both, H4 only, H3 only, neither), and each pool's p is recomputed
with the measured counts. If S1 then no longer returns {1}, outcome 1 is
unattainable, and Q_attain says so in every verdict. If S1b no longer
returns {1}, a target passing H4 alone could not be dated, and the record
says so. Both are recorded at the second freeze, before any target-side
number exists.

---

## 10. Software

### 10.1 Build plan

The build is done by agents in parallel. Each agent owns the files listed
for it, works to the interfaces of 10.2, and reads only what its tier allows
(below). The lead writes `odybench/model.py`, the shared types, first, and
it is frozen as the contract. Code inside the package runs as
`py -m odybench.x`, never as `py odybench/x.py`, because the file would
then shadow the standard library's `calendar` [acq §4].

**Three reading tiers** (revision 5) [14.4 #57]. Revision 4 told the agents
which truth files not to open, but this design itself, several dossier notes
and every recheck carry the controls' accepted dates or facts measured at
them. An agent who translates a control's prose into a predicate, or builds
the code that searches it, could be steered by them.

- **Truth tier:** A0, A6 and A11. Their tasks need the truth or the
  measured slack. They read this file in full. Their outputs are either
  mechanical (A0's regime file, built by `tools/build_regimes.py` from the
  ceiling rule of 6.4) or truth-side by name (A11's
  `deltat_circular_truth.json`), or they are the harness that is allowed to
  read the truth (A6).
- **Public tier:** A1, A2, A3, A4, A5, A7, A9 and A10. They read
  `build/DESIGN.public.md`, this file without Appendix T
  (`tools/public_design.py`; I13(h)), and only the paths listed in
  `data/prereg/access.json`:
  - the code (`odybench/`, `tools/`, `tests/`);
  - `data/prereg/*.json` except `*truth*`, `data/text/`, `data/jsex/`,
    `data/ephem/` and `data/stars.json`;
  - these notes: `docs/research-bm2008*.md`, `research-chronology.md`,
    `research-textclues.md`, `research-ephemeris.md`,
    `research-visibility.md` with `research_visibility_calc.py`,
    `research-window.md`, `research-unread-primaries.md`,
    `data-acquisition.md`, `controls-real-drafting.md`,
    `license-check-controls-real.md`, `license-check-almagest.md` and its
    round-1 copy, `negatives-drafting.md`, `license-check-negatives.md` and
    [lcn2];
  - by name, the reference scripts of 10.4 and of I2 in `results/`:
    `critique-design/check_bessel.py` and `check_mwra.py`,
    `bm2008-reconcile/check_mwra.py`, `bm2008-b-checks/ephem.py`,
    `design-revision-r2/ranc_season.py`, `research-critiques/eclipse_local.py`
    (the source of the `eclipses.py` port), and `design-revision-v5/alm_rows.py`
    and `verdict_trace.py`. None of them holds a control's date [me: grep].

  Not on the list, because each carries a control's accepted date or a fact
  measured at it: `docs/research-controls.md`, `docs/controls-almagest.md`,
  `docs/research-critiques.md` (it dates two of Thucydides' eclipses),
  `docs/critique-design*.md`, `docs/DESIGN-v*.md`, `data/ref*/`, and the rest
  of `results/`. `data-acquisition.md` stays on the list: one of the four
  Ithaca totalities it tabulates for −599..+300 is a control's date, but the
  table names no control, so it tells an agent no more than the background
  knowledge a language model already has [AppT 8; 13 row 50].
- **Brief tier:** A8 reads `data/prereg/pcr_redraft_brief.json` and nothing
  else (6.3.4).

Each agent's log lists every repository path it opened, and
`tools/check_access.py` compares the lists with `access.json` (I13(h)). The
check cannot see what an agent remembers, only what it opened, and the
report says so.

| agent | tier | owns | depends on |
|---|---|---|---|
| A0 lead | truth | `odybench/model.py`; `data/prereg/sites.json` (with a span and a column set per site), `windows.json`, `seeds.json`, `deltat_models.json`, `slots.json` (4.2), `verdict_rule.json`, `access.json` (above); `tools/build_regimes.py` and its output `almagest_regimes.json` (6.4: options, parameters and each set's held-out rows, all by rule) | this design |
| A1 sky | public | `odybench/sky.py`, `odybench/events.py`, `tools/build_sky.py`, `tools/build_events.py`, `tools/validate_events.py` (I5, I6, I12), `tools/fetch_horizons_rts.py` | `model.py`, `ephem.py`, `calendar.py` |
| A2 eclipses | public | `odybench/eclipses.py`, `odybench/lunar.py`, `odybench/deltat_mix.py`, `data/prereg/eclipse_hit.json`, `tools/build_eclipses.py`, `tools/validate_eclipses.py` (I2, I4), `tools/fetch_lecat.py`, `tests/test_eclipses.py`, `tests/test_lunar.py` | `model.py`, `ephem.py`, `data/jsex/` (I2b runs through the harness) |
| A3 clues | public | `odybench/prereg_io.py`, `odybench/clues.py` (with the target mask, 4.2), `odybench/search.py`, the controls sections of `data/prereg/operational_map.json`, a draft of its negatives section (with round 2's new options, 6.5), a draft of `data/prereg/sibling_pairs.json` (6.3.4), `tools/make_redraft_brief.py`, `tests/test_clues.py`, `tests/test_prereg_io.py` | A1 and A2 interfaces |
| A4 garden | public | `odybench/readings.py` (with the joint options of 6.5), `odybench/pools.py` (slot family, P_BM, P_MWRA, the mask), `odybench/reach.py` (I9, with the block bootstrap), `odybench/evidence.py`, `data/prereg/garden.json`, `readings.json`, `attain.py` (the null-side stage, 12.3), `rates.py`, `coincidence.py`, `garden.py`, `windows.py` | A3; `odybench/heldout.py`'s interface |
| A5 epics and PC-S | public | `odybench/epic.py`, `odybench/pcs.py`, `data/prereg/epic_grammar.json`, `randomepic.py`, `synthetic.py` (I10, I10b) | A3, A4 |
| A6 harness and verdict | truth | `odybench/harness.py`, `tools/build_truth_index.py`, `tools/public_design.py`, `tools/check_access.py`, `controls.py`, `almagest.py`, `negatives.py`, `odybench/heldout.py` and the script `heldout.py` (7), `data/prereg/heldout.json`, `odybench/verdict_rule.py`, `verdict.py`, `read.py`, `odybench/stats.py`, `odybench/prereg.py`, `tools/freeze.py` (both stages), `tests/test_verdict.py` (I14), `tests/test_heldout.py`, `data/prereg/verdict_synthetic/` | all |
| A7 second implementations | public | `tests/bm_reference.py` (I7); `tests/heldout_reference.py` (I15(a), on the Standish code of `results/bm2008-b-checks/ephem.py`) | `ephem.py`, `calendar.py`, the Standish code, sections 3.2, 7.1 and 7.2 of the public copy; no other bench module |
| A8 unexposed re-drafter | brief | `data/prereg/pcr_redraft.json` | `data/prereg/pcr_redraft_brief.json` only (6.3.4) |
| A9 second reader | public | the review of the negatives section of `operational_map.json`; the interval forks, caps and joint options; the literal pins, the X-class decision and the storm rule (6.5); the replay script of its edits; the review of `sibling_pairs.json` (6.3.4) | `negatives.json`, `controls_real.json`, `data/text/` |
| A10 reproduction and ΔT | public | `reproduce.py`, `deltat.py`, `odybench/s2.py`, `tests/test_t0.py` | A1, A2 |
| A11 ΔT-fit reader | truth | `data/prereg/deltat_circular_truth.json` (6.3.3), with page locators into SMH2016 and the 2020 Addendum | the two papers and their supplementary tables; the truth files, to match a table entry to a control |

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
                 garden: str, pool: str, slot: str | None, widths: tuple[int, ...],
                 lo_gamma: float, hi_gamma: float, lo_boot: float, hi_boot: float,
                 masked: bool)                                 # lo, hi = the wider pair (5.3)
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
evaluate(pred: Predicate, pool, ctx) -> bool[len(pool)]       # dt_rule applied inside; raises
                                                              # TargetMasked if ctx.mask_target and
                                                              # the pool holds 16 Apr -1177 (I13(g))
evaluate_p(pred: Predicate, pool, ctx) -> f8[len(pool)]       # P_mix(pass), for reports
evaluate_rows(clueset, reading, pool, ctx) -> bool[n_rows, len(pool)]
search(clueset, reading, window: (jd0, jd1), ctx, scoring="strict"|"bestfit")
      -> SearchResult
make_redraft_brief(rows=("T1-DARK","T2-SEASON","T-INT-12","D-ECL","L4-DARK"))
      -> writes data/prereg/pcr_redraft_brief.json             # tools/make_redraft_brief.py
```

`prereg_io` refuses any path that matches `*truth*` (I13). `ctx` holds the
sky tables, event lists and catalogues for the sites a clue set names, and
the flag `mask_target` of the null-side stage (12.3).

**`odybench/pools.py`, `readings.py`, `reach.py`, `evidence.py`**

```
pools.targets(kind="T"|"T_C"|"T_A"|"T_A_E5"|"P_BM"|"P_MWRA", site="ithaki", slot="v0".."v6",
              span="core"|"background", mask_target: bool) -> rec[POOL_DTYPE]
pools.member(t_jd_tt: float, kind="P_BM"|"P_MWRA", ctx) -> bool   # target side only: does the
                                                              # target pass a reading defining the pool?
pools.slot_A(pool, ctx, slot="v0".."v6") -> bool[len(pool)]  # 4.2's slot family, day counts paired
readings.garden(tier="BM"|"DOC"|"FULL", equinox=False, eclipse_compatible=False)
      -> Iterator[Reading]                                     # equinox=False: the rule gardens (F6 off)
readings.pinned(name) -> Reading        # "T0b", "BM", "R_anc", "R_anc_noecl"
readings.survivors(garden, pool, ctx) -> Iterator[(reading_index, f8[k] survivor JD_TT)]
reach.interval(t, s_prev, s_next, W_days) -> (lo, hi)         # empty if lo >= hi
reach.reach(targets: f8[m], survivor_sets, W_days) -> f8[m]   # |union| / W
reach.G(reach_values: f8[n], target_years: i8[n], garden, pool, widths,
        n_boot=10000, block_years=136, seed) -> GStat             # wider of gamma and block bootstrap (5.3)
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
verdict_rule.check_structure(q: dict, null_side: dict) -> list[str]
      # violated constraints C1-C9 of 9.4; [] if realisable. null_side is
      # the design-stage estimates (2.9) or results/attain/attain.json
prereg.check_frozen(stage: int = 2) -> dict(commit, tree_hash, amendment, attain_sha256)
      # raises unless HEAD descends from prereg-<stage> with a clean tree
```

**`odybench/heldout.py`** (7.2) and **`attain.py`** (12.3)

```
heldout.predicates(pool, ctx) -> bool[len(pool), 2]           # H3, H4 (7.1); day count per member
heldout.uncounted(pool, ctx) -> bool[len(pool), 3]            # H1, H2, H5 (reported only)
heldout.floor(flags_null: dict[str, bool[n_P, 2]]) -> dict(per_pool={P: (n_P, x_max_P, p_min_P)},
      p_H_min)                                                # null side, target masked; max over pools
heldout.p_pool(flags_null: bool[n_P, 2], flags_target: bool[2], member: bool)
      -> dict(p, weights, x, n)                               # one pool; p = 1 if not member
      # weights -log10 q_i over pool + target (symmetric, exact); ties against the target
heldout.p_value(per_pool: dict[str, dict]) -> dict(p_H, p_BM, p_MWRA)   # p_H = max over the pools
heldout.homogeneity(flags_null_BM: bool[n, 2], is_mwra: bool[n]) -> dict(table, fisher_p)   # R20
heldout.almagest(set_id, regime_rows, pool_days, ctx) -> dict(p, n, held_rows)   # Q_H (6.4)
attain.run() -> writes results/attain/attain.json            # n_T, n_TC, n_A[v], G_BM[v] (GStat),
      # G_BM_u, G_DOC[v] (reported); per held-out pool n, x_max, the H3-only, H4-only and both
      # counts, q3, q4; p_H_min; the homogeneity table (R20); I7(a), I9(b, c), I15(a), I14(c)
```

`attain.json` is the only file the second freeze commits besides its text
output. Every target-side script reads the null-side values from it and
never recomputes them.

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
| `moon_up` | interval of named instants, illuminated-fraction bounds, quantifier, `negate` (AEN-TROY-02:iii: the Moon below the horizon at the end of evening nautical twilight) | negatives, PC-R |
| `moon_dark_share` | maximum share of the dark hours with the Moon up | H2 |
| `rise_lead`, `set_lag` | body, minutes | V; ALM visible_only (minutes between horizon crossings); `bm_venus_lead` |
| `visible` | body, side, AV (degrees or PLSV), critical altitude | F4, F5, H3, H5, the slots of T_A |
| `alt_at` | body or star, named instant, minimum altitude | ALM visible_before_sunrise (civil dawn), negatives |
| `turning_point` | body; event (greatest elongation from the true or mean Sun; station; rise- or set-azimuth extremum; first or last visibility; opposition to the true or mean Sun; **conjunction with the Sun, inferior or superior**); side; k days (continuous); visibility required; displacement | M; H3; ALM (`ge_true_k`, `ge_mean_k`, `bm_mwra_k`, `opp_*`); epics |
| `ge_relation` | body, side, before or after, j days or `same_apparition` (the literal option the projection uses, 6.4) | ALM A.1, B.1, I.1, J.4 |
| `star_covis` | stars, minimum altitude, twilight, span of nights, quantifier; or a season window (C_rel, autumn) | C; F3; epics |
| `star_phase` | star, phase, AV, k days | epics; negatives; R_anc's season bound |
| `rel_position` | body, reference (star, line through two stars, Moon's centre), offset or distance, tolerance, frame; or `relation`, a stated ratio of two offsets on one line (ALM-B.2: Moon's centre − Venus = 1.5 × (Venus − β Sco), Venus between) | ALM star and Moon rows (held-out rows, 6.4); one branch per star candidate for F.4 |
| `sun_lon` | range (wrapping through 0°) | seasons in PC-R, R_anc |
| `equinox_offset` | event, offset range in days | E_rel; ALM-E.3 |
| `solar_eclipse` | smag range, central flag, minimum h_tot/h_09/h_06, timing (LAT of maximum, first contact after noon, last contact with the Sun up), site rule; `x_class` ∈ {X3, X4, X1–X4} mapped as in 6.3.3 and 6.5 | X; PC-R; negatives |
| `lunar_eclipse` | umag and pmag ranges, the Moon's latitude sign or the eclipsed limb (ALM-C.3's `magnitude_and_side`: north), timing (mid-eclipse offset from LAT midnight, first contact after moonrise, overlap or containment in seasonal night hours or a night quarter), the Moon's altitude at contacts, moonrise during the umbral phase at a site rule | PC-R; ALM-C |
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
- **Linked rows** (6.5). A row whose day another row's option sets is built
  as a joint option with that row (ARG-COLCHIS-01 with -02; ARG-CIUS-05 with
  -06). A range of days passes if the row passes on one of them, and an
  unplaced row is dropped.
- **Filters the design applies to the files' own lists.** The rule's
  eclipse-compatible readings exclude lunar-eclipse options and
  storm-darkness options (6.5). The *Almagest* projection sets A.10 and B.5
  to "none" and uses the `same_apparition` options (6.4). Each filter is
  recorded in `operational_map.json` or `almagest_regimes.json`; the clue
  files stay byte for byte as licence-checked.

### 10.4 Independent second implementations

Issue 13 asked which code paths get an independent check, against what, and
at what tolerance. Every derived quantity the verdict rests on has one. The
tolerances are those of 6.1, where each is checked to be one that a correct
implementation can meet [r2 R2-4]:

| code path | independent implementation | cross-check | tolerance | check |
|---|---|---|---|---|
| `sky.py` rise and set | JPL Horizons rise/transit/set; the grid-plus-bisection finder of `results/critique-design/check_mwra.py` | 1,000 events; 2,000 events | 0.5 min; the sum of the two convergence tolerances plus 0.01 s (0.12 s for Mercury, 1.02 s otherwise) | I5 |
| `events.py` stations, greatest elongations, azimuth extrema | `results/bm2008-reconcile/check_mwra.py`; the Standish code of `results/bm2008-b-checks/` | 152 S2 years; 500 events | same civil date in ≥ 150/152; 0.05 d, or 0.5 d at flat maxima; 1 d | I6 |
| `events.py` heliacal phases, B&M's spring limits, Arcturus' rising | `docs/research_visibility_calc.py`; `results/design-revision-r2/ranc_season.py` | −1177, −700, −1130 | 1 d | I6 |
| `events.py` first crescent | the Yallop code of `research_visibility_calc.py` | 500 lunations | ≥ 495 equal | I12 |
| `eclipses.py` | NASA's `program.js` in Node (`data/jsex/sites/`); `results/critique-design/check_bessel.py` | 5 sites × 5,486; four totality windows | smag (NASA's magnitude, section 0) 0.0005, 0.002 h; 6 s | I2 |
| `lunar.py` | NASA LEcat5 | the PC-R and ALM centuries, plus 300 random | 0.02; 3 min; type tie band at magnitude 0 | I4 |
| `deltat_mix.py` | `ephem.delta_t` and `ephem.delta_t_sigma` evaluated directly, and a 10⁶-draw Monte Carlo of the mixture | P(total) for 1178 and 1131 BC on NASA's elements against the 2.3 table | 0.005 | I2 (added row) |
| the B&M reading through `clues.py`, `readings.py`, `search.py` | `tests/bm_reference.py` (A7) | every T0 cell; 300 random years; (a) masked, (b) the target | identical flags outside the tie bands of 6.1 | I7 |
| `heldout.py` (H3, H4) | `tests/heldout_reference.py` on the Standish code (A7); Horizons for 50 members | every member of P_BM, which contains P_MWRA; (b) the target | identical flags outside the tie bands of 6.1 | I15 |
| `heldout.p_pool` and the max over the pools | `results/design-revision-v5/verdict_trace.py`'s `p_pool`, an independent transcription of 7.2 | every cell of the lattice, on the design-stage and the measured counts | exact | I14 |
| `reach.py` reach | brute-force sliding windows | 10,000 synthetic sets | 0.0002 | I9(a) |
| `reach.G` interval (gamma and block bootstrap) | coverage on synthetic cores built from real 243-year blocks | 2,000 cores | coverage ≥ 0.95 − 3 SE | I9(b) |
| `pools.py` and `readings.py` together | the identity G(𝒢_BM*, T) = (n_A(v)/n_T) G(𝒢_BM*, T_A(v)) for v1–v5 | the real tables, masked | exact | I9(c) |
| the PC-S generator | Standish code; Horizons subsample | 200 truths (50 via Horizons) | recall 1.000 | I10 |
| `evidence.lr_slot` | end-to-end simulation in `pcs.science` | every core truth of T_C per noise cell, accepted by A(t, δ) | within the simulation interval in ≥ 11 of 12 cells | I10b (reported) |
| `calendar.py` | exhaustive day counting; the Horizons calendar | −1999..+500 | exact | I8 (done) |
| `prereg_io.py` | the licence checkers' dump scripts; A9's review; the brief's leak scan | every row | exact | I13 |
| `almagest_regimes.json` (projection and held-out rows) | `results/design-revision-v5/alm_rows.py`, a transcription of 6.4's rules written before the file | every row of the 12 sets | identical lists | I13(f) |
| `tools/public_design.py` (the build agents' copy) | the truth files, read by A6's check | every accepted date, in every form the truth files print it | none present | I13(h) |
| `verdict_rule.py` | the synthetic sets as traced by `results/design-revision-v5/verdict_trace.py`; the structural constraints; the rerun with the measured null side | 18 sets; 9 constraints | exact | I14 |

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
| `attain.py` | the null-side stage: pools with the target masked, G_BM per slot variant, G_BM,u, G_DOC (reported), the two held-out pools P_BM and P_MWRA with their counts, p_H,min and the homogeneity table (R20); I7(a), I9(b, c), I15(a), I14(c) | `results/attain/` (committed at the second freeze) |
| `heldout.py` | section 7: the target's membership of each pool, p_BM, p_MWRA and p_H, the uncounted H1, H2 and H5, the sensitivity pools; `--check` runs I15(b) | `results/heldout/` |
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
  `tools/freeze.py` (both stages), and revision 5's `tools/build_regimes.py`
  (6.4), `tools/public_design.py` and `tools/check_access.py` (10.1,
  I13(h)).
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
| `heldout_reference.py` | I15 |
| `test_heldout.py` | the rank test on hand-built pools: exactness under exchangeability by simulation, the lattice, ties against the target |
| `test_eclipses.py` | I2 |
| `test_lunar.py` | I4 |
| `test_events.py` | I5, I6, I12 |
| `test_prereg_io.py` | I13 |
| `test_verdict.py` | I14 |

---

## 11. Data, run order and run times

### 11.1 Data still to acquire

| what | from | size | why |
|---|---|---|---|
| DE441 excerpt +241..+300, the same 11 bodies | NAIF `de441_part-1.bsp` by HTTP Range (`tools/fetch_ephem.py`) | about 6 MB [me: 238 MB per 2,301 years, scaled] | some control windows reach past +241 (4.1; [AppT 7]); the current excerpt ends at +241 [acq §1.1] |
| DE431 Sun, EMB, Earth, Moon +241..+300 | NAIF `de431_part-2.bsp` | about 4 MB [me: 17.7 MB per 240 years, scaled] | lunar-timed quantities for the same windows |
| NASA LEcat5 century pages −1999..+300 | eclipse.gsfc.nasa.gov/LEcat5 (`tools/fetch_lecat.py`) | about 23 × 60 kB; all 23 are fetched anew, because the 10 earlier copies sit in `results/controls/`, which is off the public whitelist (10.1) | I4 |
| Horizons rise/transit/set for 1,000 events; positions for 50 PC-S truths | Horizons API (`tools/fetch_horizons_rts.py`), cached in `data/ephem/horizons/` with the request URL on line 1 | small | I5, I10 |
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
| 0 | pre-freeze | fetch | `py tools/fetch_ephem.py`, `py tools/fetch_lecat.py`, `py tools/fetch_horizons_rts.py` | 10–20 min | network |
| 1 | pre-freeze | build code; unit tests | agents (10.1) | — | |
| 2 | pre-freeze | sky tables, events, catalogues | `py tools/build_sky.py --all`; `py tools/build_events.py`; `py tools/build_eclipses.py` | **3–5 h, once** [r1 N12] | see below |
| 3 | pre-freeze | instrument checks I1–I6, I8, I9(a), I13, I14(a, b), and the reported I3 and I12 | `py tools/validate_ephem.py`; `py tools/validate_events.py`; `py tools/validate_eclipses.py`; `py tests/test_*.py` | 30–60 min | |
| 4 | pre-freeze | the re-draft brief, then the re-draft (6.3.4), then I2b; the negatives' second reading (6.5); the review of `operational_map.json`; `deltat_circular_truth.json` (6.3.3); `almagest_regimes.json` (6.4); `slots.json` (4.2); `sibling_pairs.json` (6.3.4); the builders retired (12.1); the public copy, I13(h) and the access logs (10.1) | agents | — | |
| 5 | | **first freeze**, `prereg-1` | `py tools/freeze.py --stage 1` | seconds | 12.3 |
| 6 | null side | I7(a), I9(b, c) and I15(a) on the masked pool; then the null-side quantities: n_T, n_TC, n_A(v), G_BM(v), G_BM,u, G_DOC (reported), the held-out pools P_BM and P_MWRA with each pool's n, x_max and pass counts, q3, q4, p_H,min and the homogeneity table; then I14(c) | `py attain.py` | 1–2 h | the 36 readings of 𝒢_BM* and 𝒢_DOC* over about 27,000 candidates; H3 and H4 on about 80 pool members (P_MWRA ⊂ P_BM); 2,000 bootstrap cores for I9(b) |
| 7 | | **second freeze**, `prereg-2`: commits `results/attain/` | `py tools/freeze.py --stage 2` | seconds | 12.3 |
| 8 | target and controls | I7(b), I15(b), I10, I10b, I11 | `py tests/bm_reference.py --target`; `py heldout.py --check`; `py synthetic.py --instrument`; `py negatives.py --plumbing` | 20 min | |
| 9 | target and controls | T0 | `py reproduce.py` | 5 min | |
| 10 | target and controls | N1, N2, N5 | `py rates.py`; `py coincidence.py`; `py windows.py` | 10–20 min | lookups on cached tables |
| 11 | target and controls | N6 | `py deltat.py` | 20–40 min | about 45 totality windows on DE431 |
| 12 | target and controls | N3 (r_Ody, the reported gardens, R_anc) and the evidential findings | `py garden.py` | 1–3 h | 𝒢_FULL* (767,232 readings) and the reported E-on gardens (up to 3.07 million) × about 27,000 candidates, as packed bit ANDs on 14 workers with the gap test of 10.2 |
| 13 | target and controls | held-out (p_H) | `py heldout.py` | 5 min | |
| 14 | target and controls | N4 | `py randomepic.py` | 1–3 h | epics drawn until 200 enter the stratum, per variant; the entering fraction may be 0.1 or less [r2 R2-8], so up to about 20,000 stratum epics with 36-reading gardens |
| 15 | target and controls | PC-S science mode | `py synthetic.py` | 20–40 min | the core's 892 truths of T_C × 12 noise cells × the BM and DOC tolerance forks |
| 16 | target and controls | PC-R and the *Almagest* control, with its held-out calibration | `py controls.py`; `py almagest.py` | 30–60 min | 21 windows per set; site "none" grids; the mixture grid |
| 17 | target and controls | negatives | `py negatives.py` | 20–40 min | 13 sets × gardens × 2 windows (plus 40 sensitivity windows) |
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

After the first freeze, about 6–11 hours of computation remain. Most of it is
in steps 6, 12 and 14. Step 2 is cached and runs once.

---

## 12. Freezing and amendments

Revision 1 hashed only `DESIGN.md` and `data/prereg/`, on a machine with no
version control, and it let every script run unfrozen. Nothing covered the
code, and nothing could refute a charge that thresholds or code had changed
after the results came in [rev #4]. The freeze is a local git commit, and
both rechecks found that resolved [r1 §1, #4; r2 §1, #4].

Revision 4 makes the freeze **two-stage** [r2 R2-1 fix 1]:

- **The first freeze, `prereg-1`.** It commits the design, the prereg files,
  the thresholds and all the code. It comes before any null, control or
  held-out result is computed.
- **The null-side stage.** The frozen code then computes only the null-side
  quantities, with the target masked.
- **The second freeze, `prereg-2`.** It commits those quantities. It comes
  before any target-side number is computed.

So the thresholds are frozen before the null side is known, as the recheck
asked. And the bench knows whether it could have said "yes" before it looks
at the target.

### 12.1 Before the first freeze (all must hold)

1. Every module of 10.2 exists and its unit tests pass.
2. The pre-freeze instrument checks pass: I1, I2, I4, I5, I6, I8, I9(a), I13
   and I14(a, b), with I2b after the re-draft (item 3). I3 and I12 have run
   and are reported (6.1).
3. **The re-draft** (6.3.4) is done, in order:
   - `tools/make_redraft_brief.py` has written
     `data/prereg/pcr_redraft_brief.json`, and I13(e) has passed on it;
   - the unexposed re-drafter has written `data/prereg/pcr_redraft.json`;
   - I2b has run after that, because I2b computes local magnitudes at the
     truth dates and must not run before the re-draft exists.
4. **The negatives' second reading** (6.5) is done. Its re-pinned readings
   (VF-COLCHIS-01 among them), the X-class decision, the joint options of
   the linked rows and the storm rule are in `negatives.json` and
   `operational_map.json` as recorded edits: a script that rebuilds from the
   licence-checked copy, like the licence checkers' own.
5. `data/prereg/operational_map.json` is complete and reviewed (I13).
6. **`data/prereg/deltat_circular_truth.json`** lists every control eclipse used in
   SMH2016's and the 2020 Addendum's fits, with page locators (6.3.3).
7. **`data/prereg/almagest_regimes.json`** names the option and parameter
   values of both regimes for every projected row (6.4). `tools/build_regimes.py`
   writes it by rule.
   - It shows the ceiling arithmetic of the leave-one-set-out tolerances.
   - It names each set's held-out rows, which must equal the lists of
     `results/design-revision-v5/alm_rows.out.txt` (I13(f)).
   - It reproduces the known consequences of 2.6 (R9, R10).
8. **`data/prereg/slots.json`** holds the six slot variants of 4.2 with their
   sources, and the reported v6.
9. **`data/prereg/sibling_pairs.json`** lists the sourced conventions and the
   row pairs that state the same feature, with the excluded transplants. It
   is built without the truth (6.3.4).
10. **The three builders are retired.** Each would silently undo the licence
    checks' edits if re-run [lcr; lca1 item 1; lca2 item 2; lcn §4.1; lcn2
    problem 3]:
    - `results/controls-real-drafting/build_controls_real.py`;
    - `results/controls-almagest/build_prereg.py`;
    - `results/negatives/build_negatives.py`.

    The frozen JSON files are the record. The builders are kept for
    provenance, and are marked "do not re-run" in their first line by their
    owners or, failing that, listed here as retired. `tools/freeze.py`
    refuses to freeze if any of the three clue files differs from the output
    of its recorded edit scripts. Those are the licence checkers' replays from
    their saved pre-edit copies, followed, for the negatives, by the second
    reader's script:
    - `controls_real.json`: `results/license-check-controls-real/apply_license_check.py`
      on `controls_real.before-license-check.json`;
    - `controls_almagest.json`: `results/license-check-almagest/apply_edits.py`
      on `controls_almagest.before.json` (round 1), then
      `results/license-check-almagest/r2/apply_edits_r2.py` on
      `r2/controls_almagest.pre_r2.json` (round 2);
    - `negatives.json`: `results/license-check-negatives/apply_edits.py` on
      `negatives.before.json` (round 1), then
      `results/license-check-negatives/r2/apply_edits_r2.py` on
      `r2/negatives.r2-before.json` (round 2), then the second reader's
      script.
11. The new prereg files exist: `sites.json`, `windows.json`, `seeds.json`,
    `deltat_models.json`, `slots.json`, `readings.json`, `garden.json`,
    `epic_grammar.json`, `heldout.json`, `eclipse_hit.json`,
    `verdict_rule.json`, `verdict_synthetic/`, `operational_map.json`,
    `pcr_redraft_brief.json`, `pcr_redraft.json`, `almagest_regimes.json`,
    `sibling_pairs.json`, `deltat_circular_truth.json`, `truth_index.json`,
    `i2b_truth.json` and `access.json`.
12. `data/SHA256SUMS` is extended to every file in `data/text/` and
    `data/refs/`, and to the new ephemeris and catalogue files.
13. **No null result exists.** No survivor set, reach, G, held-out pass rate,
    control search or negative search has been computed by bench code.
    `freeze.py` checks that `results/` holds no output of the scripts of
    10.5. The design-stage estimates of 2.9 were computed by reviewers and by
    the revisions' scratch scripts, not by bench code, and they are recorded
    as such.
14. **The public copy and the access record** (10.1). `tools/public_design.py`
    has written `build/DESIGN.public.md` from the frozen `DESIGN.md`, I13(h)
    has passed on it, and every public-tier agent's access log has been
    compared with `access.json`. The logs are committed with the code.

### 12.2 The repository

- **Where.** `git init` in `C:\Projects\odybench` makes a local repository
  with no remote. Commits use the machine's existing git identity, and
  nothing is pushed.
- **Committed:**
  - `DESIGN.md`, `docs/`, `odybench/`, `tools/`, `tests/` and the top-level
    scripts;
  - `data/prereg/`, truth files included. The searcher's isolation is
    enforced by code and test, not by hiding files;
  - `data/stars.json` and `data/SHA256SUMS`;
  - `build/DESIGN.public.md`, the build agents' copy, and `build/access/`,
    their access logs (10.1);
  - the scripts in `results/` with their own text outputs, which record
    what was known before the freeze;
  - after the null-side stage, `results/attain/`.
- **Hashed, not committed** (listed in `data/SHA256SUMS`):
  - the ephemeris `.bsp` files and `data/jsex/`;
  - `data/text/*.tsv`, exported from Jon's library, some of them in
    copyright;
  - `data/refs/` (PDFs and their extracted text) and `data/cache/`;
  - every large binary in `results/`;
  - every copy of a publication kept in `results/`. Examples are the
    extracted texts `results/data-acquisition/bond2017.txt` and
    `results/controls-real-drafting/gautschy-eclipsecitations.txt`, and the
    PDFs and HTML in `results/unread-primaries/`.

  Nothing copyrighted enters the repository, so a later decision to publish
  it cannot publish a text by accident.

### 12.3 The two freezes

**The first freeze.** `py tools/freeze.py --stage 1`, run on a clean working
tree, does four things:

1. It checks every hash in `data/SHA256SUMS` and the conditions of 12.1.
2. It commits everything listed in 12.2 as the **freeze commit**, and tags
   it `prereg-1`.
3. It writes `PREREG.sha256` at the repository root. That file holds:
   - the freeze commit hash;
   - the git tree hashes of `odybench/`, `tools/`, `tests/` and
     `data/prereg/` at that commit (`git rev-parse prereg-1:odybench` and so
     on);
   - the blob hashes of `DESIGN.md` and of each top-level script;
   - a git-independent **code tree hash**: the SHA-256 of the sorted lines
     "`<sha256>  <path>`" over every file in `odybench/`, `tools/`, `tests/`,
     `data/prereg/`, `DESIGN.md` and the top-level scripts.
4. It commits `PREREG.sha256` alone in the next commit, because a file cannot
   hold the hash of the commit that contains it.

**The null-side stage.** `py attain.py` refuses to run unless HEAD descends
from `prereg-1`, the working tree is clean and the code tree hash matches.

- **The mask.** It builds every pool with `mask_target=True`. 16 Apr −1177
  is removed before any predicate is evaluated, and `clues.evaluate` raises
  if asked for it. I13(g) has checked both statically and at run time.
- **The checks.** It runs I7(a), I9(b, c) and I15(a) first, and stops if any
  fails.
- **The quantities.** It computes the null-side quantities of 9.1 and writes
  `results/attain/attain.json` and `attain.out.txt`.
- **I14(c).** It reruns the synthetic sets with the measured null side, and
  records three things:
  - whether S1 still returns {1}, which is Q_attain;
  - Q_tol and Q_slot;
  - the measured p_H,min.

**The second freeze.** `py tools/freeze.py --stage 2` does three things:

- it commits `results/attain/` and tags the commit `prereg-2`;
- it appends to `PREREG.sha256`, in the next commit, the `prereg-2` commit
  hash and the SHA-256 of `attain.json`;
- it prints the null-side record:
  - is outcome 1 attainable?
  - Q_tol;
  - Q_slot.

**After the second freeze.** Every later analysis script calls
`prereg.check_frozen(stage=2)` at start, and stops unless three things hold:

- HEAD descends from `prereg-2`;
- the working tree is clean;
- the current code tree hash equals the frozen one, or the latest
  amendment's.

`--unfrozen` lets a script run, but it stamps every output EXPLORATORY in its
first line, and `verdict.py` refuses to read such outputs.

**If the null side shows that outcome 1 is unattainable,** Q_attain records
it, and the rule is not changed. Any change would be an amendment made with
null-side outputs read, and would be marked so (12.4).

### 12.4 Amendments

A change to any frozen file after either freeze, code included, is allowed
only as a dated amendment appended to 12.6 below. The amendment states:

- what changed;
- why;
- the hash of the diff;
- **which outputs had already been read** when it was made, null-side ones
  included, in the way indusbench recorded its correction to test 1
  [indusbench DESIGN §4].

The amendment is committed, and its new code tree hash is appended to
`PREREG.sha256` under the old lines, so the file keeps the whole history.

The clue files' own histories are recorded the same way:

- `controls_real.json` was drafted and frozen before any accepted date was
  looked up (`eb1f0401…9256`). An agent blind to the truth then
  licence-checked it (`135fba67…83f8`) [lcr]. The recheck verified the hash
  [r2 §4].
- `controls_almagest.json` was licence-checked twice. The builder wrote
  `e16c559d…37e9`; round 1 made `758ee789…4c83` [lca1], which revision 4
  recorded; round 2 made
  `18b3ff01915c91d7f424bb514e3cc3ec70e3b311dd257936df64b91faa39b458`
  [lca2 item 1].
- `negatives.json` was licence-checked twice. The builder wrote
  `405f78da…bebe` (round 1's pre-edit copy,
  `results/license-check-negatives/negatives.before.json`); round 1 made
  `f4ae3b26…bb00` [lcn], which revision 4 recorded; round 2 made
  `be4f511e63d130e07ae30877d546d516f81268bcaff6080eb27ac77490c49f82` [lcn2].

These are the hashes as of revision 5 [me: `sha256sum`, recorded in
`results/design-revision-v5/preserved_sha256.txt`]. The recheck of revision
3 confirmed the first three [r2 §4]; the two round-2 hashes are new. If a
pre-freeze task of 12.1 changes a file (the negatives' second reading),
`freeze.py` records the new hash with the script that made the change.

### 12.5 Publishing the hash

Publishing the hash outside the machine would give an outside timestamp. Two
ways to do it are:

- a public commit or gist under the research identity Jon uses for open work;
- an OpenTimestamps proof of `PREREG.sha256`.

Publishing is **optional and needs Jon's explicit permission**, for each of
the two freezes. The bench does not assume it. Until he gives it, the freeze
is verifiable only on this machine, and `VERDICT.md` says so in its first
lines.

### 12.6 Amendments made after the freeze

None yet.

---

## 13. What the dossier could not settle, and how each is handled

| # | open fact | why it is open | handling |
|---|---|---|---|
| 1 | What "Ti = New Moon" means operationally | no single rule reproduces S2's Ti column [bm §5 N] | T0b pins the UT+2 conjunction date (136/152); F2 carries LMT, +1 day and first crescent |
| 2 | Which New Moon when two qualify; S2's out-of-window Ti | S2 follows no consistent rule [bm §7] | T0b evaluates every qualifying New Moon; T0a replays S2 as printed |
| 3 | Why 14 S2 MWRA dates sit 4–8 days from DE441's maxima | Starry Night's Mercury theory, another horizon, or plot reading [bm §5 M] | DE441 vertex maxima are used; the integer replay is a regression check (A3) |
| 4 | Mercury's visibility on Ti−34 | never tabulated; **PLSV has no extinction model** (settled [unread §6]) | visibility off, AV 10°, and PLSV's AV formula at a 1° critical altitude, all in the T0 grid; a physical extinction model is an upgrade, not a prerequisite |
| 5 | The Pleiades and Arcturus cut-offs (17 Feb; 3, 4 or 5 Apr) | three dates in the paper and SI [bm §5 C] | T0b uses 17 Feb and 4 Apr; C_rel is calibrated to them at −1177; F3 carries 2°, 5°, autumn and none |
| 6 | The ṅ and ΔT formula of Starry Night 6.0.4 | unpublished; two published Starry Night values cannot come from one smooth ΔT(t) [unread §7] | 27,602.7 s is the T0b clock only and is never converted |
| 7 | ΔT at −1177 | SMH's own formulations span 681 s; every value before −720 is extrapolation [eph §8] | four models and their mixture, each σ taken as Gaussian (an assumption, stated) |
| 8 | The lunar ephemeris to pair with SMH | DE441's tidal model is unpublished; DE441 − DE431 = +188 s at −1177 [eph §5.3] | lunar-timed quantities on DE431, planets on DE441 (section 0) |
| 9 | Which island is Homeric Ithaca | modern dispute | Ithaki primary; four sensitivity sites; Paliki dropped (section 0) |
| 10 | Lefkada's coordinates | 20.70 in the site catalogue, 20.71 in research-ephemeris [acq §6 item 5] | 20.70 adopted (section 0) |
| 11 | The departure hour from Ogygia; Athena's night in Sparta | the Greek does not say [chron §4.B, §4.F] | F1's grid; F1b for the typical numbers |
| 12 | What Day 0 is; Apollo's feast on the new moon or the 7th | the text is silent; ancient sources split [txt §5.1, §5.3] | F2 (a)–(d); the 7th as an epic anchor in N4 |
| 13 | The Greek day boundary | not verified from a primary source [vis §6 item 4] | F2 (d) uses a sunset day, (c) a civil day |
| 14 | The meaning of "late-setting" Boötes | late, slow, or Aratus' autumn evenings [txt §5.8; vis §3.1] | F3 (a′)–(f) |
| 15 | Whether the morning star is Venus | Homer's names are separate [vis §1.4] | F4 includes any bright herald and none |
| 16 | The equinox bound | ≤ 4 Apr (§Intersecting), ≤ 5 Apr (§References), XXX = ≤ 6 Apr (S2) [bm §5 E; rev #23] | the T0 grid carries all three. **E is left out of every rule garden**, because its reading was formed with the target in view (5.3) |
| 17 | The window | text 1250–1115 BC, S2 1251–1100 BC; drawn from the tradition that chose the eclipse [bm §6; win §6] | the reproduction window as stated; N5 runs five; G_any is reported beside G |
| 18 | Which three lines schol. 14.162 suspects | commentaries not available [txt §10] | every result is conditional on 14.162 = 19.307 being read as a month-turn at all |
| 19 | Primary sources | **Read**: MacDonald 1967 (pp. 324–327), Papamarinopoulos et al. 2012, Henriksson 2012, the PLSV 3.1 documentation, Neugebauer & Schoch 1927 [unread §1]. **Still unread**: P. V. Neugebauer 1929 (paywalled; Jon could open the HathiTrust record himself); Schoch's *Die Sterne* 6:88 and *Dichter-Finsternisse*; P.Oxy. 3710 (papyri.info needs Jon's approval for the browser); Austin 1975; de Jong 2001 App. A; Stanford 1959; the Oxford commentaries; Starry Night internals | no computed number depends on them. MacDonald's March reading is documented as formed with the eclipse in view (1.1), which fixes the conditioning of 5.3 |
| 20 | Herwart von Hohenburg's 1612 date | known only through Fotheringham 1921 [crit §1.2] | historical note only |
| 21 | Arcus visionis models are crude | AV bands stand in for extinction; weather moves first and last dates by ±3 to ±15 d [vis §1.2, §6] | AV values are forks; the slack of real observers is measured on the *Almagest* (6.4) |
| 22 | Correlated ΔT errors of 1178 and 1131 BC | 47 years apart [win §7.1] | joint probabilities under a common offset (R7) |
| 23 | The prior for oral transmission of a dated sky | no comparative case [win §10–11] | not quantified; no likelihood ratio or Bayes factor is multiplied by a prior |
| 24 | Ephemeris coverage | settled to +241 [acq §1]; the controls need +300 | fetched in step 0 (11.1) |
| 25 | Ancient Troy dates | known through B&M, Wikipedia and Clement's list as reported by Papamarinopoulos et al. [win §3, §12; unread §4], not from FGrHist | used only for the primary window's envelope and H6; *secondary* |
| 26 | Hermes = Mercury, and whether any god-movement is astronomical | no ancient parallel before Plato [txt §5.9] | not adjudicated: F5 none; H3–H4 test the rule's consistency; the categorical reading is conditioned on (5.3) |
| 27 | ΔT σ before −2000; the σ discontinuity at −500 | extrapolation; Huber against MS2004 on NASA's page [acq §6 items 3–4] | no eclipse in the bench lies before −1999; the discontinuity is reported where a control sits near −500 |
| 28 | Sirius' orbit model | about 1′ at −1177 between the published and the re-referred proper motions [acq §3.3] | the published centre-of-mass motion is adopted; the re-referred one is a sensitivity; a photocentre motion is never used |
| 29 | The *Almagest* glosses and cruxes | the unit glosses (moon 0.5°, cubit 2°, finger 1/12°) and the star identifications are the drafter's; IX.7.11 and IX.9.4 are textual cruxes; Heiberg's apparatus and Toomer were not consulted [alm §6; lca1; lca2 item 8]. Round 2 confirmed both emended intervals from Ptolemy's own Sun [lca2 method 3] | crux intervals are forks (primary as printed); star rows are outside the gate's projection, and so are the glosses they need |
| 30 | Exposure of the PC-R drafter | the drafter had seen computed answers [pcr §1]; one unflagged row was found by the recheck [r1 N5] | an unexposed re-draft of five rows from a brief, and a sibling-convention audit (6.3.4); background knowledge of famous dates cannot be removed |
| 31 | Single words in the negatives | Eous (*Aen.* 3.588), vesper (VF 7.1), ἔκλιθεν (*Arg.* 3.1196), διχόμηνις (*Arg.* 1.1231); Servius and the Apollonius scholia are not in the library [neg §6 item 3] | forked, with none |
| 32 | The Meeus ch. 7 values in `test_calendar.py` | recalled, not read [acq §6 item 7] | each also agrees with exhaustive day counting and with Horizons, so a wrong one would fail |
| 33 | The accepted dates of the PC-R controls | taken from secondary sources: summaries of Toomer and Pedersen, Gautschy's citation list, NASA's historical-eclipse page. Toomer's translation was not consulted. Two date slips in those sources are recorded in [AppT 5] [pcr problems] | the drafter also recomputed every accepted date; the harness uses `truth_index.json` built from the truth file; the report marks the sources *secondary* |
| 34 | Coordinates of the negatives' places | Wikipedia coordinates; Giresun Island for the Island of Ares and Cape Sideros for Salmonis are modern identifications; representative points stand in for regions [neg §6 item 4; lcn §4.5] | used as recorded; a gazetteer check (Pleiades) is a pre-freeze task for the second reader of 6.5; site sensitivity is not expected to matter for star phases |
| 35 | Numeric thresholds in the negatives that are the drafter's but not marked as such (±1 d, ±7 or ±15 d, 2° and 5° altitudes, fraction ≤ 0.25, 2–3 h) | operationalisations of stated features [lcn §4.3] | kept; listed by the second reader in `operational_map.json` with a "drafter's threshold" flag |
| 36 | Whether SMH's fits used the control eclipses | Table S10 v2020 lists two of them, and SMH2016 §2b(iv) names two more (*secondary*); the entries are in [AppT 4]; Table S4 and §4b unread [r1 N4, §4] | the mixture scores every control; Q_ΔT tests the circular sets with σ tripled; `deltat_circular_truth.json` is a pre-freeze task (6.3.3) |
| 37 | The formula of the G interval | the Fay & Feuer (1997) gamma interval is given from memory | the implementer checks it against the paper; I9(b) checks its coverage by simulation |
| 38 | Stationarity over the 2,200-year background | precession moves the star season about 31 days against the equinox | P8 tests the rates; G is reported on each half of the core |
| 39 | The approximations behind P(A) = 0.154 and the second recheck's G_BM = 0.140 | both rechecks used a 3-minute rise grid and a declination-based rise-azimuth maximum (3-point vertex), good to about 1 d at a flat maximum [r1 §4; r2 §5] | the bench recomputes every null-side quantity at the null-side stage with its own code (12.3); the rough values are in 2.8 and 2.9 and are never counted |
| 40 | The slot widths that define T_A, and so G_BM | nothing in the record fixes a width; the recheck found G_BM moving from 0.14 to 0.33 across defensible definitions [r2 R2-2] | a frozen family of six (4.2); every G-based decision is taken against the claim across all six, and Q_slot reports a split. Label 1 does not use T_A |
| 41 | When the *Almagest* k_days list [1, 2, 3, 5, 7, 10, 16, 21] was written | its top value matches the measured Venus maximum; the note calls 5 or 7 and 21 "the *Almagest* slack" [alm §5 item 1]; file times cannot settle the order [r2 R2-9] | regime SL no longer reads the list: its tolerances are ceilings of the out-of-set maxima (6.4) |
| 42 | Whether H3 and H4 are truly blind | they were frozen in revision 1 (2026-10-03); a search of `docs/` and `results/` finds no evaluation of either at the target; but anyone who knew B&M's remark that Mars was invisible could infer that H4 fails (2.10) | the inference points to failure, so any bias it caused works against a "yes"; the predicates are not changed; R12 records the inference, and the bench computes the target's values only after the second freeze |
| 43 | Whether the target is exchangeable with the held-out pools under H0 | the target was chosen as an eclipse new moon | neither H3 nor H4 involves the lunar node; P10 tests the pass rates on eclipse and non-eclipse spring new moons. The matching on Mercury's event is row 48 |
| 44 | The masked target changes the null side slightly | removing 16 Apr −1177 can only lengthen a neighbour's survivor gap | it raises G slightly, against B&M; the unmasked G is reported after the second freeze (5.3) |
| 45 | The design-stage held-out estimate (P_BM: n 76, x_max 1; P_MWRA: n 43, x_max 0; p_H,min 0.026) | rough: r2's candidate rows, invisibility approximated by an elongation below 10°, daily sampling (2.9) | the bench recomputes it at the null-side stage; I15 checks the predicates; if the measured p_H,min exceeds 0.05, Q_attain says so in every verdict |
| 46 | "Freeze before any null result" against "compute the null side before the freeze" | the bench's freeze rule requires the first [rev #4]; the recheck's fix asks for the second [r2 R2-1 fix 1] | two freezes (12.3): code, design and thresholds first; the null side, computed by the frozen code with the target masked, second; the target side after both. The design-stage estimates in 2.9 come from reviewers and scratch scripts, not from bench code (12.1 item 13) |
| 47 | What MacDonald's Venus reading commits to | p. 327 dates the greatest morning elongation (17 Mar, "1176" a slip) and says nothing about nearness; on Day −5 Venus was 26 d past it and 1.84° below the maximum [unread §2.1, §2.5] | the documented Venus slot is "a visible morning star" (v0); the "within 2° of the maximum" variant (v6) is reported, not in the rule family, because its width is set by the target's value |
| 48 | Whether the held-out pools are exchangeable with the target | the target passes only MWRA readings; P_BM also admits candidates through a greatest elongation or a station, whose Mercury is in another phase near Day 0 | two pools, P_BM and P_MWRA, and the rule reads the larger p, which is valid if either pool is exchangeable (7.2); R20 reports P_BM's homogeneity (rough: H3 8/43 against 7/33, Fisher p 0.78) |
| 49 | Storm darkness in the negatives | round 2 found it treated unevenly: QS-SACK-06:a had a solar-eclipse option while other storm darknesses were excluded [lcn2 finding 13(1)] | the storm rule (6.5): weather is never eclipse-compatible, for fiction and for the Odyssey alike; QS-SACK-06:a is a sensitivity |
| 50 | The build agents' exposure to truth-side facts | this design, three dossier notes and every recheck carry accepted dates or facts measured at them; one date in `data-acquisition.md`'s table of Ithaca totalities is a control's date, unlabelled [AppT 8] | Appendix T, three reading tiers and access logs (10.1, I13(h)); what an agent remembers, as distinct from what it opened, cannot be audited, and the report says so |
| 51 | The round-2 report on the negatives is not in `docs/` | the harness refused that agent's write of a report file [lcn2 problem 1] | its findings are kept verbatim as [lcn2]; the per-row verdicts are in the file's `license_check` fields |
| 52 | Lunar phases computed from Ptolemy's coordinates | A.10 and B.5 choose their phase class from stated longitudes [lca2 item 4] | "none" in the gate's projection, so the gate reads words only; the coordinate version is reported (6.4) |

---

## 14. Resolution of the reviews

Four tables follow:

- 14.1 gives the 25 issues of `docs/critique-design.md`, the review of
  revision 1, with their resolution as of revision 5;
- 14.2 gives the 17 issues N1–N17 of the recheck of revision 2 [r1],
  numbered 26–42 as the later recheck numbers them;
- 14.3 gives the 12 issues R2-1 to R2-12 of the recheck of revision 3 [r2],
  numbered 43–54;
- 14.4 gives issues 55–66: what revision 5 found in revision 4, which no
  recheck saw, and in the round-2 licence checks.

Each row gives the resolution and the sections it changed. Where a
resolution departs from the reviewer's proposed fix, the row says why,
marked **Departure**.

### 14.1 The review of revision 1 (`critique-design.md`)

The recheck of revision 3 found 22 of these resolved, and #1, #17 and #21
unresolved [r2 §1]. Revision 4 resolved those three through the issues of
14.3. Revision 5 keeps every resolution, and the rows say what it added.

| # | severity | resolution, as of revision 5 | sections |
|---|---|---|---|
| 1 | blocker | **Resolved.** The rule is a pure function of named quantities (9.1–9.2). Every condition names its garden, its pool and its stage: null-side, target-side or control. Revision 3's outcome 1 could not be reached, because each of its "yes" conditions was fixed by the sky before the Odyssey was measured: G_BM about 0.14, 1189 BC passing B&M's criteria, and pct_N4 a reach percentile [r2 R2-1]. Revision 4 rested outcome 1 on the clues nobody fitted (H3, H4), scored by an exact rank test whose floor p_H,min is computed with the target masked, before any target-side number (7, 12). **Revision 5** matches that test to the readings the target passes: it runs on P_BM and on P_MWRA, and the rule reads the larger p, which stays exact if either pool is exchangeable with the target (7.2). The design-stage floor stays 0.026, and a target passing H4 alone still reaches 0.045. B&M's own match is judged by label 2, which has a "no match" form, and Q_tol says when B&M's readings could not have dated anything. **Every outcome is reachable**, by one realisable synthetic set each: S1 (outcome 1), S2 (2; S2nm its "no match" form), S3a and S3b (the two parts of 3), S4 (4), and S0 (inconclusive). Every set marked realisable uses the design-stage null side (C7), and I14(c) reruns all 18 with the measured null side. Revision 5's `verdict_trace.py` reproduces every label and qualifier. The NC condition stays replaced by pct_N4, and G keeps one sense. **Departure:** the review's fix 2 put pct_N4 and an LR in outcome 1. Both are reach-based, so their "yes" was unattainable; pct_N4 stays in label 2 | 1.3, 2.9, 2.10, 3.5, 4.2, 5.4, 7, 9, 12 |
| 2 | blocker | **Resolved.** `controls_real.json` is used exactly as licensed (SHA-256 `135fba67…83f8`, verified by the recheck of revision 3; the re-run did not touch it). The searcher never reads a truth file. The re-draft of five exposed rows and the sibling-convention audit stay, the audit transplanting only sourced conventions between rows whose words state the same feature [r2 R2-10]. **Revision 5** closes two leaks of the same kind as this issue. Revision 4's refusal pattern `*_truth*` missed its own `truth_index.json`, and two truth-side files lacked "truth" in their names; the pattern is now `*truth*` and the files are renamed. And this design, several dossier notes and every recheck carry accepted dates; the agents who translate and search the clue files now work from a copy without Appendix T, on a whitelist, with logged access (10.1, I13(h)) | 6, 6.3, 6.3.4, 10.1, 12.1, App. T |
| 3 | blocker | **Resolved.** Outcome 3 is split into 3a (PC-R) and 3b (the *Almagest* control of B&M's clue types), scored at B&M's tolerances (regime BM, which feeds Q_BM) and at the empirical observer slack (regime SL, which decides 3b). Leave-one-set-out tolerances are the ceiling of the out-of-set maximum, so the rule is always defined [r2 R2-9]. Q_BM conditions every "no" that rests on B&M's tolerances, and Q_H calibrates the held-out test on the same records. **Revision 5** translates the second licence check: the gate's lunar phases come from words only (A.10 and B.5 set to none); the rows whose primary bound is the drafter's use their literal options; the held-out rows are named row by row; and the structural fact held_ALM ≤ 8 is recorded (2.6, 6.4) | 1.3, 2.6, 6.4, 9 |
| 4 | major | **Resolved,** and confirmed by both rechecks. The freeze is a local git commit of the design, the prereg files and all code; `PREREG.sha256` holds the commit hash, the tree hashes and a code tree hash. A second freeze commits the null-side record. Amendments are dated and state which outputs had been read. Publishing the hash outside the machine is optional and needs Jon's permission. Revision 5 adds the build agents' access logs and the public copy to what the first freeze commits (12.1 item 14) | 12 |
| 5 | major | **Resolved.** 1.1 says the 6 years is the C ∧ E rate. The comparison with B&M's own arithmetic at ±1 d (0.88 per century) is regression expectation R13. **Departure (revision 5):** the comparison "with E, against B&M's printed 0.048" is still made, at n = 3, 4 and 5 with exact Poisson intervals, but it is no longer counted. About 1.9 survivors are expected over the whole background (2.4), so a count of 0–3 is consistent with either figure and Poisson noise would decide the prediction. It is R19 | 1.1, 2.4, 8 |
| 6 | major | **Resolved,** and confirmed. MacDonald was read; the conditioning reason is frozen and applied uniformly to C, V, M and E, and to the clues B&M cited as support (H2 is not counted). The slot widths that implement the conditioning are a frozen family [r2 R2-2] | 1.1, 4.2, 5.1, 5.3, 7 |
| 7 | major | **Resolved,** and confirmed. The gardens are nested and sourced: 𝒢_BM* 36 readings, 𝒢_DOC* 35,964, 𝒢_FULL* 767,232. The greedy smallest fork set is reported. 18 of 𝒢_BM*'s 36 readings duplicate the other 18 (2.9) | 5.3, 2.9 |
| 8 | major | **Resolved,** and confirmed: F1b, PC-S jitter of 0–3 d, and the decay curves. Revision 5 gives the negatives' narrator-stated counts the same jitter in the reported DOC and FULL comparisons; the rule's comparison has F1b off on both sides (6.5) | 5.3, 6.2, 6.5 |
| 9 | major | **Resolved,** and confirmed: C_rel and E_rel outside T0b; the calibration h_A 2.04°, h_P 0.92° is a fit, not a visibility | 4.5, 2.9 |
| 10 | major | **Resolved,** and confirmed: hit strengths come from the ΔT mixture, the background runs from −1999, and the target is excluded from its own base rate | 4.1, 4.4, 5.2 |
| 11 | major | **Resolved.** The held-out statistic is a rule input. H1, H5 and H2 are not counted (fix 2), and R_anc's survivors are reported (fix 3). **Fix 1, completed in revision 5.** Revision 4's pool, P_BM, admitted candidates through any Mercury event of 𝒢_BM*, while the target passes only the MWRA readings. P_MWRA is literally "the candidates that pass the same N, C, V and M". The rule reads the larger of the two pools' exact p-values (7.2), and R20 reports whether P_BM is homogeneous (rough: Fisher p 0.78) | 4.2, 7, 9 |
| 12 | major | **Resolved,** and confirmed. The MWRA is a vertex fit at ±1.5 d; flat maxima are flagged; I6 gives them their own tolerance and I7 a tie band [r2 R2-4] | 3.2, 6.1 |
| 13 | major | **Resolved,** and confirmed. Every derived quantity has a second path (10.4), with criteria a correct implementation can meet [r2 R2-4, R2-7]. Revision 5 adds three: the regime file against an independent transcription of 6.4 (`alm_rows.py`), the two-pool p against `verdict_trace.py`, and the public copy against the truth files (I13(h)). I4 now covers every century, so that it names none a truth lies in | 6.1, 10.4 |
| 14 | major | **Resolved,** and confirmed. PC-S has an instrument mode (I10) and a science mode, feeds no rule, and both checks are reported beside INSTR [r2 R2-4] | 6.1, 6.2 |
| 15 | major | **Resolved,** and confirmed. The Iliad is a same-tradition comparison, beside 12 clean negatives; readings whose eclipse is not on Day 0 are mapped to their eclipse [r2 R2-12]. **Revision 5** translates the second licence check: ARG-RETURN-04:d, a Day-0 solar-eclipse reading; AEN-TROY's reading R-iii; Ida as a landmark; the linked ARG-COLCHIS and ARG-CIUS rows. It adds the storm rule, under which weather is never eclipse-compatible, for fiction or for the Odyssey, so QS-SACK-06:a becomes a sensitivity, and it generalises the survivor-to-eclipse mapping to ±k-day options | 6.5, 10.3 |
| 16 | major | **Resolved,** and confirmed. No likelihood ratio enters the rule; the ceiling 1/P(A) is a standing finding; every G has an interval, the wider of the gamma interval and a block bootstrap [r2 R2-6]. **Departure** (kept from revision 3): the review wanted the LR to decide outcomes 1 and 2. On a fixed poem every such ratio is set by the observation model [r1 N1] | 5.3, 5.7, 9 |
| 17 | major | **Resolved.** Everything computable from known numbers is in section 2 with its numbers: the recheck's G_BM, slot table, r_Ody and near misses, R_anc's 9 survivors, BF_BM 2.6 and the rates (2.9). Revision 3's P4, P6, P12, P13, P14, P19, P22 and P30–P35 are settled, regression expectations or dropped (2.7). **Revision 5** applies the same test to revision 4's list: P4 had no power on known numbers and is withdrawn to R19 (2.4), and the homogeneity of the held-out pool, roughly known, is R20 rather than a prediction. Section 8 counts only quantities that need new runs | 2.4, 2.7, 2.9, 2.10, 8 |
| 18 | major | **Resolved,** and confirmed. R_anc's season comes from ancient definitions, under four bounds reported with equal prominence, with and without the eclipse clue; the order in which the union was adopted is recorded [r2 R2-11] | 5.3, 2.9 |
| 19 | minor | **Resolved,** and confirmed: one Espenak–Meeus model, four in the mixture | 0, 2.3 |
| 20 | minor | **Resolved,** and confirmed: A1–A5 are regression tests; I3 is a reported calibration | 3.4, 6.1 |
| 21 | minor | **Resolved.** smag is NASA's magnitude exactly, as `program.js` prints it; `smag_partial` is used only where the reference uses that formula (I2b); X3, h_09 and h_06 read smag [r2 R2-7] | 0, 6.1, 4.4 |
| 22 | minor | **Resolved,** and confirmed: epoch −1176.68; a half-open window; R6 | 0, 3.2 |
| 23 | minor | **Resolved,** and confirmed. The T0 grid stays; T0b's reading is a member of 𝒢_BM*; outcome 1 reads T0_pass, and T0 itself is reported | 3.5, 5.3 |
| 24 | minor | **Resolved,** and confirmed. Revision 5 corrects two more slips: revision 4's held-out script printed 0.208 for "H3 only" on P_BM, where its own text rightly had 0.221 (2.9); and revision 4's provenance tags pointed at a licence-check report that has since been replaced (section 0, [lca1]/[lca2]) | 0, 2.9 |
| 25 | minor | **Resolved,** and confirmed: HIP numbers verified; Sirius uses the barycentric proper motion | 2.1 |

### 14.2 The recheck of revision 2 ([r1], issues 26–42)

The recheck of revision 3 found 16 of these resolved, and N1 unresolved in
substance [r2 §2]. Revision 4's resolutions stand; a row says where revision
5 changed something.

| # | r1 | severity | resolution in revision 4 (revision 5 notes in the row) | sections |
|---|---|---|---|---|
| 26 | N1 | blocker | **Now resolved in substance.** The LR left the rule in revision 3, and the ceiling 1/P(A) is a standing finding (fixes 1, 2a, 4). The substance was that the bench could not say "yes". It now can: outcome 1 rests on the exact held-out test, whose floor (0.026 at the design stage) is computed before the target is read. Fix 3 is generalised correctly this time. Q_attain tests p_H,min, the floor of the evidence outcome 1 actually reads, and not revision 3's U0(n_A), which was the floor of a quantity the sky had already fixed. C7 bars synthetic sets from inventing a null side | 1.3, 2.10, 7, 9.4, 9.5, 12.3 |
| 27 | N2 | major | Resolved. Leave-one-set-out tolerances are now ceilings of the out-of-set maximum [r2 R2-9]. rec_PCS stays out of the gate | 6.4 |
| 28 | N3 | major | Resolved. B&M's option rule is named, and Q_BM is a regression expectation (R9) | 6.4, 8 |
| 29 | N4 | major | Resolved. The mixture scores every ΔT-dependent control row, and the circular controls are tested by Q_ΔT | 6.3.3 |
| 30 | N5 | major | Resolved. Re-draft and audit; the audit is narrowed to sourced conventions between rows stating the same feature [r2 R2-10] | 6.3.4 |
| 31 | N6 | major | Resolved, and extended. C, V and M are conditioned on; E is left out. RE counts for nothing, because outcome 1 reads T0_pass, which uses no E. The slot widths form a frozen family [r2 R2-2]. H2, a clue B&M cited, is not counted | 1.1, 3.5, 4.2, 5.3, 7 |
| 32 | N7 | major | Resolved. Revision 4 also moves the recheck's newly settled items (14.3, #47) | 2.7, 8 |
| 33 | N8 | major | Resolved. R_obs is exact; every G has an interval, now allowing for dependence [r2 R2-6]; one reach definition | 5.3, 5.7 |
| 34 | N9 | minor | Resolved. Ancient season bounds; R_anc with and without the eclipse; the four bounds are reported alike [r2 R2-11] | 5.3 |
| 35 | N10 | minor | Resolved. Ē_N4 is compared with G_BM (P17); pct_N4 stays a percentile | 5.4, 8 |
| 36 | N11 | minor | Resolved. The X-class mapping is recorded, and covers round 2's ARG-RETURN-04:d. QS-SACK-06:a is scored at its own day and site, with its survivor mapped to its eclipse [r2 R2-12]; under revision 5's storm rule it is a sensitivity run, not part of the rule's garden (6.5) | 6.5, 10.3 |
| 37 | N12 | minor | Resolved: `ephemeris=`, `refraction=`, a constant ΔT, one Day 0 per clock, spans per site | 4.1, 4.2, 10.2 |
| 38 | N13 | minor | Resolved: ±1.5 d continuous is the primary MWRA tolerance | 3.2, 5.3, 6.4 |
| 39 | N14 | minor | Resolved: H3 is one predicate | 7 |
| 40 | N15 | minor | Resolved. I3 is out of INSTR. I2b names both sides and compares smag_partial with the reference's partial formula [r2 R2-7] | 6.1 |
| 41 | N16 | minor | Resolved: a brief-only re-drafter, with the exposure limit stated | 6.3.4 |
| 42 | N17 | minor | Resolved | 6.4 |

### 14.3 The recheck of revision 3 ([r2], issues 43–54)

No recheck has seen revision 4's answers to these. Revision 5 reviewed them
and keeps them, with the changes noted in the rows and in 14.4.

| # | r2 | severity | resolution in revision 4 (revision 5 notes in the row) | sections |
|---|---|---|---|---|
| 43 | R2-1 | blocker | **Fix 1, in a two-stage form.** The null-side quantities (G_BM per slot variant, G_DOC, G_BM,u, n_A, n_T, and the held-out floor p_H,min) are computed by frozen code after the first freeze, with the target masked, and committed at a second freeze before any target-side number. The recheck's estimates are in 2.9 now. The thresholds 0.05 and 0.20 were frozen in revision 3 before the recheck's estimate and are unchanged; the order is recorded (9.3). **Fix 2.** Q_attain is redefined on the floor of the evidence outcome 1 reads, p_H,min. Constraint C7 fixes every synthetic set's null side to the measured or design-stage values, so revision 3's unrealisable S1 is gone. Branch tests are marked as such. **Fix 3.** Q_tol states in every verdict when B&M's readings could not have dated anything at 5% (expected: G_BM,lo ≥ 0.087 under every variant), beside 1/P(A). **Fix 4.** Outcome 1 rests on the held-out predicates H3 and H4, promoted to a rule input as an exact rank test against P_BM, and in revision 5 against P_MWRA too, the rule reading the larger p (7.2). Their attainability is estimated now (p_H,min 0.026 = max(0.026, 0.023), target excluded before any computation) and recomputed at the null-side stage. No threshold on G was relaxed. **Departure:** the review asked for G_BM to be computed "before the freeze". The bench's freeze rule [rev #4] also requires that no null result exist before the freeze. The two-stage freeze satisfies both: thresholds and code are frozen first, and the null side is frozen before the target side | 1.3, 2.9, 2.10, 3.5, 7, 9, 12 |
| 44 | R2-2 | major | **Fix 1.** The documented slot is defined with its sources: v0, Venus a visible morning star and Mercury at a named turning point within the *Almagest* slack and visible. MacDonald's reading is restated from the primary: he dates the greatest elongation and does not say "near". **Fix 2.** Six variants are frozen in `slots.json`, and the day counts are paired. **Fix 3.** Every G-based decision is taken under all six, against the claim. Q_slot reports a decision that differs ("slot-dependent"). Label 1 does not depend on the slots, because its null pool is P_BM. **Departure:** a "near greatest elongation" Venus slot (v6) is reported but kept out of the family, because the only width that admits MacDonald's own case is set by the target's value | 4.2, 5.3, 9 |
| 45 | R2-3 | major | **Fix 1.** r_Ody = 0 gives label 2 in its "no match" form, and pct_N4 is not computed. **Fix 2.** pct_N4 is mid-p, and its lower bound counts ties for the Odyssey, so ties cannot fire label 2. **Fix 3.** 2.9 and 2.10 state that the branch turns on 26 Mar 1111 BC, and R15 reports both branches | 1.3, 2.9, 2.10, 5.4, 8, 9 |
| 46 | R2-4 | major | **Fix 1.** I10b has one estimand: truths drawn from T_C and accepted by A(t, δ), all 892 core truths per noise cell. **Fix 2.** INSTR holds only checks that guard rule inputs; I3, I10, I10b and I12 are reported. **Fix 3.** I7 has tie bands (0.01 d, 0.05 min), listed. Beyond the fix, every INSTR criterion was rechecked: I2's totality tolerance allows the reference's 5-s grid; I5(b) allows both convergence tolerances; I6(a) treats flat maxima apart; I9(b)'s Monte Carlo coverage allows three standard errors; I4 has a type tie band | 6.1, 6.2 |
| 47 | R2-5 | major | P12, P19, P32, P33 and P35 are moved: P12 to R15 with its near misses, P19 into R11, P32 to R16, P33 dropped, P35 replaced by 2.10. P4 and P6 are regression expectations R13 and R14, with the note that they sit on their thresholds. A new counted P5 asks the open question, clustering. P22 is dropped, and its value is reported with n = 4. P13, P14 and P34 are in 2.7 and R17 | 2.7, 2.9, 8 |
| 48 | R2-6 | minor | G's interval is the wider of the Fay–Feuer gamma interval and a moving-block bootstrap over the core (136-year blocks; 243-year reported). I9(b) checks coverage on synthetic cores built from real 243-year blocks, so real clustering is kept | 5.3, 6.1 |
| 49 | R2-7 | minor | smag is defined as `program.js` prints it (section 0). I2(a) compares smag with the catalogue's `mag`. `smag_partial` serves I2b. X3, h_09 and h_06 read smag, so an annular eclipse passes by its diameter ratio | 0, 6.1 |
| 50 | R2-8 | minor | **Fix 1.** Epics are drawn until at least 200 enter, and C3 now reads n_stratum ≥ 200 on the entering subset. **Fix 2.** Every clue type has an 18-option fork set × 2 day counts = 36 readings | 5.4, 9.4 |
| 51 | R2-9 | minor | SL tolerance = the out-of-set maximum rounded up to the next whole day: Mercury 6 d in ten counted sets and 5 d in one, Venus 21 d, opposition 1 d (per set: [AppT 2]). The grid's history: the note itself calls 5 or 7 and 21 "the *Almagest* slack" [alm §5 item 1], which suggests that the list was written with the measured slack in view. The bench no longer takes SL values from it. R10 is unchanged | 6.4, 13 |
| 52 | R2-10 | minor | Only conventions with an outside source stated in the file are transplanted, and only into rows whose licence words state the same feature. The drafter's own choices, such as T2-SEASON's 330° start, are never transplanted. The pairs and the excluded transplants are frozen, without the truth, in `sibling_pairs.json` | 6.3.4 |
| 53 | R2-11 | minor | R_anc's four season bounds are reported with equal prominence. 5.3 records that revision 3 adopted the union after the Sun's longitude at 30 Sep 1131 BC (176.69°) was known | 5.3 |
| 54 | R2-12 | minor | A survivor of a reading whose eclipse option sits on another day or site (QS-SACK-06:a) is mapped to its eclipse's conjunction. G_j's targets are the daylight conjunctions at any of the set's observer places, so hit_j and G_j refer to the same event. Revision 5 extends the mapping to the options that place a conjunction within ±k days (AEN-TROY-02:ii-b, ARG-RETURN-04:b), and QS-SACK-06:a is now a sensitivity run under the storm rule | 6.5 |

### 14.4 Found by revision 5 (issues 55–66)

No recheck saw revision 4. Revision 5 reviewed it against the principles of
the redesign (a computable rule with every outcome reachable; a gate of
B&M's own clue types; the controls exactly as licensed, never read by the
searcher; known numbers kept out of the predictions; a code freeze; buildable
interfaces) and against the two round-2 licence checks. "Source" names
where the problem was found.

| # | severity | issue | source | resolution | sections |
|---|---|---|---|---|---|
| 55 | major | The held-out test's null pool was not matched to the reading the target passes. P_BM admits candidates through an MWRA, a greatest elongation or a station; the target passes only MWRA readings; H3 is about Mercury on Day 0, whose phase the Day −34 event sets | revision 4's 7.2 against [rev #11 fix 1] | A second pool, P_MWRA, matched on B&M's applied M. The rule reads p_H = max(p_BM, p_MWRA), which is exact if either pool is exchangeable with the target. A target outside a pool gets p = 1 there. Design stage, target masked: P_MWRA n 43, x_max 0, floor 0.023; p_H,min stays 0.026; the lattice is 0.026 (both), 0.045 (H4 only), 0.227 (H3 only). P_BM's classes do not differ on the rough rows (R20) [me: heldout_strata.py] | 2.9, 2.10, 4.2, 7.2, 7.3, 8 (R12, R18, R20), 9.1–9.5, 10.2, 13 row 48 |
| 56 | major | Truth-side files the searcher's refusal did not cover. Revision 4's pattern `*_truth*` does not match its own `truth_index.json`, and `i2b_reference.json` and `deltat_circular.json` hold truth-side values under neutral names | revision 4's 6, 10.2, 10.1 | Every truth-side file has "truth" in its name (`i2b_truth.json`, `deltat_circular_truth.json`); the pattern is `*truth*`; `tools/build_regimes.py` joins the short list of readers (I13(c)) | 6, 6.1, 6.3.3, 10.1, 10.2, 12.1 |
| 57 | major | The agents who build the searcher and translate the controls' prose could read the controls' accepted dates, and facts measured at them, in this design (2.6, 6.3.3, 6.3.4, 6.4, 8, 13), in three dossier notes and in every recheck. Revision 4 barred only the truth files | revision 4's 10.1 | Truth-side facts move to Appendix T. Three reading tiers: the public tier works from `build/DESIGN.public.md` and a whitelist, with logged access (10.1, I13(h)). I4 now covers every century, so it names none a truth lies in. Background knowledge cannot be removed, and the report says so | 2.6, 4.1, 6, 6.1, 6.3.3, 6.3.4, 6.4, 8, 10.1, 11.1, 12.1, 13 rows 33, 36, 50, App. T |
| 58 | minor | Provenance tags that no longer resolve. Revision 4's "[lca]" meant round 1's report, and round 2 has replaced that file. The re-run of the review loop writes its recheck to the file names revision 4 cites as [r1] and [r2] | the re-run's preparation stage | [lca1] and [lca2]; byte copies of both rechecks, with SHA-256, in `results/design-revision-v5/` | 0, 14 |
| 59 | major | The second *Almagest* licence check changed the file and raised four design points: a new hash; A.10 and B.5 phase classes computed from Ptolemy's coordinates; four primaries whose day bound is the drafter's; new vocabulary (B.2's ratio `relation`, C.3's `magnitude_and_side`); hourless records | [lca2 items 1, 3–5, §D] | Hash recorded with its history. The gate's projection reads words only (A.10 and B.5 none) and the literal `same_apparition` options; both changes only loosen rows, so R10 stands. The vocabulary is added to 10.3, and hourless rows are evaluated at the dawn or evening instant | 2.6, 6.4, 10.3, 12.4 |
| 60 | minor | The held-out rows of the *Almagest* calibration were ambiguous for moon-phase rows (revision 4: "planet–Moon positions … at its primary option", whose primary is the phase class). Three counted sets have no held-out row, so held_ALM ≤ 8, which nothing recorded | revision 4's 6.4 | The held-out rows are named row by row and checked against `alm_rows.py`; held_ALM ≤ 8 is in 2.6, 2.10, C5 and P24 | 2.6, 2.10, 6.4, 8, 9.4 |
| 61 | major | The second licence check of the negatives changed the file and its eclipse-compatible list: a new hash; ARG-RETURN-04:d, a Day-0 solar eclipse at the first site; AEN-TROY's reading R-iii; Ida as a landmark; ARG-COLCHIS-01's night set by -02's option. Its report is not on disk | [lcn2 findings 3–5, 8; problems 1–2] | All translated (6.5): `x_class` X1–X4 for 04:d; a negated `moon_up` for 02:iii; the first observer place for Day-0 options; joint options for linked rows. The relayed report is kept verbatim | 2.6, 6.5, 10.3, 12.1, 12.4, 13 row 51 |
| 62 | major | Storm darkness treated unevenly: QS-SACK-06:a gave Athena's cloud storm a solar-eclipse option, while every other storm darkness was excluded as weather | [lcn2 finding 13(1)] | The storm rule: weather is never eclipse-compatible, for fiction or for the Odyssey (whose darkness is a seer's vision). QS-SACK-06:a is a sensitivity run. The rule works against outcome 4 | 6.5, 13 row 49 |
| 63 | minor | The negatives' narrator-stated counts carry no typical-number jitter, unlike the Odyssey's DOC and FULL gardens | [lcn2 finding 13(2)] | Parity holds for the rule, whose comparison has F1b off on both sides. In the reported DOC and FULL comparisons the negatives' counts get the same ±2 and ±3 d jitter | 6.5 |
| 64 | minor | VF-COLCHIS's "literal" pin used vis7, but after round 1 "none" is the least-inference reading of "serus … vesper" | [lcn2 finding 13(6)] | Re-pinned by the second reader under the existing rule | 6.5, 12.1 |
| 65 | minor | The survivor-to-eclipse mapping covered Day-0 options and eclipse options on another day, but not the options that put a conjunction within ±k days of Night 0 | revision 4's 6.5 | Generalised: a survivor maps to the conjunction its option names; there is at most one | 6.5 |
| 66 | minor | Revision 4's P4 (λ with E at least 0.07 per century) had no power: about 1.9 survivors are expected over the whole background | revision 4's 8.2, against issues 5 and 17 | Withdrawn to the reported comparison R19, with exact Poisson intervals at n = 3, 4, 5; the number P4 is kept so that nothing is renumbered | 2.4, 8 |

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
- the recheck of revision 2 [r1], written as `critique-design-r1.md` and kept
  as `results/design-revision-v5/critique-design-r1.recheck-of-rev2.md`;
  scripts in `results/critique-design-r1/`.
- the recheck of revision 3 [r2], written as `critique-design-r2.md` and kept
  as `results/design-revision-v5/critique-design-r2.recheck-of-rev3.md`;
  scripts in `results/critique-design-r2/` (`check_gbm.py`,
  `check_slot_scaling.py`, `check_ranc_p19.py`, `check_prereg_leaks.py`).
- `data-acquisition.md`, the ephemeris extension, NASA elements, stars and
  calendar; `results/data-acquisition/`.
- `controls-real-drafting.md` and `license-check-controls-real.md`, the real
  eclipse controls; `results/controls-real-drafting/`,
  `results/license-check-controls-real/`.
- `controls-almagest.md`, the *Almagest* control, and its two licence
  checks: round 2 in `license-check-almagest.md`, round 1 in
  `results/license-check-almagest/r2/license-check-almagest.r1.md`;
  `results/controls-almagest/`, `results/license-check-almagest/` (with
  `r2/`).
- `negatives-drafting.md`, the negative controls, and their two licence
  checks: round 1 in `license-check-negatives.md`, round 2 as relayed text in
  `results/design-revision-v5/license-check-negatives-r2.relayed.md`;
  `results/negatives/`, `results/license-check-negatives/` (with `r2/`).
- `research-unread-primaries.md`, on MacDonald, Schoch and Neugebauer,
  Papamarinopoulos, Henriksson and PLSV; `results/unread-primaries/`.
- `DESIGN-v1.md` to `DESIGN-v4.md`, revisions 1–4 of this design.

Revision 3's scratch scripts are in `results/design-revision-r2/`:

- `cp_bounds.py`: pool sizes, interval floors and garden sizes;
- `ranc_season.py`: Arcturus' heliacal rising at −1177 and −1130;
- `synth_sets.py`: the intervals of revision 3's synthetic sets;
- `alm_options.txt`: the options of the *Almagest* rows.

Revision 4's are in `results/design-revision-r3/`:

- `heldout_attain.py`: the design-stage held-out null (2.9), with the target
  removed before any computation; output `.out.txt` and `.json`;
- `synth_sets.py`: the numbers of the synthetic sets of 9.5;
- `verdict_trace.py`: the rule of 9.2 and the constraints of 9.4, run on
  every synthetic set;
- `check_design.py`: mechanical checks of this file (tables, section
  references, prediction ids);
- `splice.py` and `parts/`: how this file was assembled from revision 3.

Revision 5's are in `results/design-revision-v5/`:

- `heldout_strata.py`: the design-stage held-out null split by Mercury
  event, with P_MWRA and the homogeneity table (2.9), the target removed
  before any computation; `.out.txt` and `.json`;
- `alm_rows.py`: the B&M-type projection and the held-out rows of every
  *Almagest* set under 6.4's rules, read from the clue file alone;
- `verdict_trace.py`: the rule of 9.2 with two held-out pools, and the
  constraints of 9.4, run on the 18 synthetic sets of 9.5;
- `check_design.py`: revision 4's mechanical checks of this file, extended
  to the new tags and to Appendix T;
- `parts/`: the sections rewritten in revision 5, spliced into revision 4;
- `preserved_sha256.txt`: the hashes of the documents this file cites;
  byte copies of the two rechecks and of the round-2 *Almagest* report; and
  the relayed round-2 report on the negatives.

Each script has its `.out.txt` beside it.

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

<!-- APPENDIX-T: everything below this line is truth-side. tools/public_design.py cuts the file here; build agents of the public tier never see it (10.1). -->

## Appendix T. Truth-side facts (withheld from build agents)

Each item below was measured at a control's accepted date, or depends on
one. Section 2 says what these facts imply in aggregate; the facts
themselves are kept here so that the agents who translate and search the
control files (the public tier of 10.1) never read them.
`tools/public_design.py` removes everything from the marker line above to
the end of the file, and I13(h) checks the copy.

### T1. The *Almagest* records at the true dates

Measured against DE441 with the true dates [alm §0, §4, Tables 2–6]:

- **Mercury**, 14 records put at or about greatest elongation, offsets from
  the true greatest elongation (record minus event, days) [alm Table 2]:
  - sorted by size: IX.9.3 0.1, IX.9.4 0.2 (printed), IX.7.7 0.8, IX.7.4
    1.1, IX.7.12 1.1, IX.8.4 1.6, IX.7.16 1.8, IX.7.14 2.7, IX.7.15 2.9,
    IX.7.11 3.3 (emended), IX.8.3 3.4, IX.7.9 3.6, IX.7.6 4.2, IX.7.5 5.5;
  - so 3/14 lie within 1 d, 7/14 within 2 d, 12/14 within 4 d and all 14
    within 5.5 d;
  - the elongation stays within 0.5° of its maximum for 5–10 days.
- **Venus**, 8 records: X.3.2b 0.6 and X.3.2a 1.9 (Ptolemy's pair); X.1.3
  16.1, X.1.6 16.7, X.2.3 17.8, X.1.5 18.3, X.2.4 20.3, X.1.4 20.6. The last
  six lie on a 34–35-day plateau within 1° of the maximum.
- **At B&M's ±1 d**, the true dates satisfy every greatest-elongation clue
  of only 2 of the 9 sets that carry one (ALM-A as printed, ALM-E). ALM-C
  needs 3.4 d, ALM-G 5.5, ALM-H 3.6 (emended) and ALM-K 2.9; ALM-D, F and L
  need 16–21 d.
- **B&M's Mercury proxy is a different event.** For the 7 morning
  greatest-elongation records, the nearest rising-azimuth maximum lies −2.5
  to +31.8 d away, and only 2 lie within ±3 d. Every Venus morning record
  rises 125–220 min before the Sun, so B&M's ≥ 90-min test does not
  discriminate.
- **The other kinds are tight.** Oppositions lie within 1.8 d of the
  true-Sun opposition (0.42 d of the mean-Sun one). Planet–star relations
  lie within 1.7 d, and Moon–planet positions within about 2 h of lunar
  motion; every implied lunar phase is right. IV.6.14's mid-eclipse is
  0.02 h from Ptolemy's time, at umag 0.84 against his 5/6, the north limb
  eclipsed. The III.1.10 equinox is 0.87 d late.
- **The cruxes against the sky.** On the printed date of IX.7.11, DE441
  puts Mercury 3.7° west of the Sun (invisible), and 22.7° east on the
  emended date. For IX.9.4 the printed day lies 0.2 d from the true greatest
  elongation and the emended day 2.8 d [alm §1.4].

### T2. What T1 decides under the frozen regimes of 6.4

Row by row from alm Tables 2 and 5 and the options in
`results/design-revision-r2/alm_options.txt` [me, revision 4; revision 5
checked that its projection changes alter none of it]:

- **Regime SL** sets each greatest-elongation tolerance leave-one-set-out,
  as the largest offset among the records outside the set, rounded up to the
  next whole day [r2 R2-9]:
  - Mercury, 6 d for every counted set except ALM-G: 5.5 d (IX.7.5) rounds
    up to 6;
  - Mercury in ALM-G, 5 d: its own IX.7.5 is the 5.5-d record, and the next
    largest is IX.7.6 at 4.2 d;
  - Venus, 21 d for every set: X.1.4, in no set, is the 20.6-d record.

  The true date is retained in **9 of the 11 counted sets**. Two fail:
  - **ALM-G**, because IX.7.5 lies 5.5 d from the maximum, against ALM-G's
    own tolerance of 5 d;
  - **ALM-H**, at its primary, printed crux: on that date Mercury set 12 min
    before the Sun, so `visible_only` fails.

  Revision 5's projection sets A.10 and B.5 to "none" and uses the
  unbounded `same_apparition` options for A.1, B.1, I.1 and J.4. Both
  changes only loosen rows that the truth passes, so no retained truth is
  lost, and neither failure depends on them.
- **Regime BM** (B&M's option rule, at 1.5 d and 90 min): the true date can
  pass in at most 5 counted sets (ALM-B, E, I, J and L):
  - the MWRA proxy fails every morning Mercury row that offers it, in ALM-A,
    G, H and K (nearest maxima +15.7, +6.2, −2.5, +29.5 and +31.8 d);
  - ALM-D and ALM-F each fail a Venus greatest-elongation row (16.1 and
    20.3 d).

  So rec_ALM_BM ≤ 5 < 6, and Q_BM holds whatever the narrowing.

### T3. The real eclipse records at the accepted dates

From the drafter's rough post-freeze check (its own lunar model, not the
bench's; I4 has not run), as the drafting stage reported it [pcr §5; the
truth file; the drafting stage's summary relayed to the design stage]:

- **Primary readings the accepted dates fail:**
  - R-PTOL-BAB: two magnitudes, E2 about 0.11 against the record's 3 digits
    (0.25), and E3 about 0.49 against "more than half";
  - R-PTOL-ALEX: H3's mid-time, 0.64 h from Ptolemy's +4 h, so R-PTOL-CHAIN
    fails too;
  - R-PYDNA: the season and the Moon's altitude. The accepted eclipse, 21 Jun
    168 BC (−167), fell about 5 days *before* the solstice (26 Jun, the
    drafter's computation), so Livy's "after the solstice" is wrong; and the
    Moon rose already eclipsed.
- **All primaries pass** for R-THUC, R-XEN, R-ARBELA and R-DIOD, and for the
  four H-LIVY notices; Livy 38.36.4 passes only through the ±1 h allowed for
  "ferme" (its maximum falls in seasonal day hour 2.41).
- **T2-SEASON.** The accepted date (21 Mar 424 BC, −423) has the Sun at
  355.3°, so only the primary "early" [330°, 60°] admits it; the half-year
  [0°, 180°] fails [r1 N5].
- **T-INT-12.** At the truth the interval is 6.63 years against the stated
  7, near the edge of its ±0.5-year tolerance [r1 N5].
- The E2 and E3 magnitude failures are model-dependent (E3 borderline at
  0.49 against 0.5) and are rechecked by the bench's own lunar module after
  I4.

### T4. The controls in the data behind SMH's ΔT fits

- SMH's Table S10 v2020 of untimed total and annular eclipses lists −309
  "Greek", 13,300–17,160 s, and −187 "Europe", 12,590–12,900 s
  [`data/ref/Table-S10.2020.txt`]. By year and region these are R-DIOD's
  eclipse and H-LIVY's L4 [r1 N4].
- SMH2016 §2b(iv) used Thucydides' 431 BC and Agesilaus' 394 BC eclipses to
  limit ΔT [r1, from a WebFetch summary of the PMC text, *secondary*]. These
  are R-THUC's T1 and R-XEN's X3.
- The S10 interval for −309 is 3,860 s wide, so R-DIOD's pass is probably
  robust. Q_ΔT tests that rather than assuming it (6.3.3).

### T5. Date slips in the truth sources

[pcr problems; the drafting stage's summary]

- Gautschy's "424 BC May 21" for Thuc. 4.52 is apparently a slip for 21 Mar
  424 BC (−423), which the drafter confirmed by computation.
- NASA's "−0412 Aug 28" for Thuc. 7.50 is the TD date of greatest eclipse;
  the local date is the evening of 27 Aug 413 BC (−412).

### T6. The per-set expectations behind R8, R10 and P20

- **R8:** the three counted sets whose accepted dates fail a primary row are
  R-PTOL-BAB, R-PTOL-ALEX and R-PYDNA (T3).
- **R10:** the two counted *Almagest* sets whose truth is not in B under
  regime SL are ALM-G and ALM-H (T2).
- **P20:** seen in the primary run: R-PTOL-BAB, R-PTOL-ALEX, R-ARBELA and
  R-DIOD; not seen: R-THUC, R-XEN and R-PYDNA.

### T7. The data coverage of the control windows

A 136-year window with the anchor at a uniformly random position spans at
most 136 years either side of the anchor [me, from the anchor dates]:

- PC-R windows fall within −856..+272 (the Babylonian triple of −720 to the
  Hadrianic eclipses of +136);
- *Almagest* windows fall within −407..+277 (anchors from −271 to +141).

### T8. Accepted dates that appear, unlabelled, in public-tier notes

- `docs/data-acquisition.md` §2.2 lists the eclipses total at Ithaca for
  some ΔT within ±1σ in −599..+300: −401 Jan 18, −309 Aug 15, −128 Nov 20,
  +174 Feb 19 [acq §2.2]. −309 Aug 15 is R-DIOD's accepted eclipse. The
  table names no control, and the note stays on the public whitelist
  (10.1).
