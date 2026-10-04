# Licence check, round 2: `data/prereg/controls_almagest.json`

**Checked:** 2026-10-04. This is the second independent check. It was done by an agent that drafted none of these sets and did not do round 1. The workflow was re-run ("Try again"), and the file already carried round 1's edits (43 rows). This round re-checks every row as round 1 left it.

Round 1's report, which this file replaces, is kept at `results/license-check-almagest/r2/license-check-almagest.r1.md`.

**Inputs read:**
- the clue file;
- `data/text/ptolemy-syntaxis-grc.tsv`:
  - every cited row (29 rows);
  - the context rows 3.1.9, 3.7.4, 4.6.12–13, 5.3.1, 7.2.3, 9.7.1–3, 9.7.6–8, 9.7.10, 9.7.12–13, 9.7.17, 9.8.1–2, 9.9.1–2, 9.10.1–2, 9.10.4–5, 10.1.1–2, 10.1.4, 10.2.1–2, 10.3.1, 10.4.1–2, 10.4.4–5, 10.7.1–2, 10.8.1, 10.9.1, 11.2.1, 11.3.1 and 11.6.1;
- `docs/critique-design.md` issues 2, 3 and 15;
- DESIGN.md, the *Almagest*-control section (its default site, instant convention and regimes);
- round 1's report.

**Not read:**
- `controls_almagest_truth.json` or any truth file;
- `docs/research-controls.md`, `docs/controls-almagest.md` and `results/controls-almagest/`;
- round 1's scripts and check outputs (`egyptian_check.*`, `meansun_check.*`, `apply_edits.*`, `row_table.md`). The interval check below is therefore independent.

**Disclosure:** to place this task in the workflow I grepped `.workflows/odybench-redesign.js`. The output included the drafting task's prompt line, which states the Nabonassar era epoch. That line gives no set's date, and I did not use it.

## Result

| | |
|---|---|
| Rows checked | 72, each against its cited row |
| Edited this round | 24 |
| `ok` | 48 |
| File before | `758ee789…4c83` (round 1's output) |
| File after | `18b3ff01915c91d7f424bb514e3cc3ec70e3b311dd257936df64b91faa39b458` |

**What did not change:**
- No row was removed.
- No primary option changed, and no option was removed or renamed.
- No `day_offset` changed.

**Where a test changed.** Only two rows had an operational test changed:
- **B.2:** an untestable offset was replaced by the stated ratio.
- **C.3:** one option was added (`magnitude_and_side`), and one option's magnitude ranges were made explicit.

**What every edited row's verdict records.** Each edited row's `license_check` names what was wrong and why. Round 1's per-row verdicts are kept as `license_check_r1`, and round 1's file-level block as `license_check_r1`.

**What was clean:**
- **Intervals:** all 20 interval rows reproduce from the text alone (method step 3).
- **Similes and lying tales:** none occurs. Every row is Ptolemy narrating, either his own observation or a record he reports.
- **Leaks:** no era year, Egyptian or other calendar month or day, observer name, BC date or Julian date is in the file, before or after this round. E.2's notes name one era, the years "from Alexander's death", without a year number.

**Round 1's edits.** All 43 were re-examined and none is reverted. Two of them had left gaps, which this round closes:
- A.10's licence still lacked "before sunrise".
- B.2's phase justification still said "before dawn".

## Method

1. **Exact words.** For every row I tested each `…`-separated fragment of `licence_words` as an exact substring of the cited row, and in text order [computed by me: `results/license-check-almagest/r2/dump_rows.py check`].
   - Before this round, every fragment of the 54 word licences was an exact substring, but C.3's two fragments were out of text order.
   - After this round, all 54 word licences are exact and in text order.
   - The 18 bracketed licences withhold date words by design. The intervals they stand for were recomputed instead (step 3).
   - Every fragment added this round is cut from the row's own characters.
     - The export mixes tonos and oxia forms of the same letter.
     - It writes the half sign sometimes as "∠" and sometimes as the literal text "U+2220". The conventions now say so.
2. **Each feature of the statement and of the primary option.** I was strict on:
   - time of day;
   - side of the Sun (morning or evening);
   - season, magnitude, totality and site;
   - day intervals;
   - any number a primary option rests on.

   Each of these must be in the quoted words, in that row, at narrator level. I was lenient on the body's name where it is the grammatical subject of the same sentence. Where the name appears only in a chapter heading, round 1's notes already say so.
3. **Intervals, recomputed independently** [computed by me: `results/license-check-almagest/r2/interval_check.py`, output `interval_check.txt`; the output contains date words].
   - **Day count.** Each date phrase is asserted as a substring of its row, and its Greek numerals are parsed from the row. Egyptian years are 12 × 30 + 5 days. The civil day follows the file's convention: in the night "D into D+1", an evening sighting is day D and a pre-dawn sighting is day D+1.
   - **Era links come from the text only** (year numbers left out of this report):
     - the two regnal-year/era equations stated at 9.10.3 and 3.1.9;
     - the 424 Egyptian years from Nabonassar to Alexander's death stated at 3.7.4, which the year pair at 10.9.2 repeats;
     - the same era year stated for both J records, at 10.9.2 and 10.4.6.
   - **All 20 intervals reproduce:** 18 from the dates as printed, plus I.4 and J.6, whose 4 days are stated in words.
   - **Cross-check against Ptolemy's own Sun positions.** I converted each stated position into elapsed days with his mean motion of 0;59,8,17,13,12,31° a day (3.1.14).
     - Where a row gives only the true Sun or an equinox, I converted with his solar model: apogee 5;30 into Gemini (3.7.3, 3.8.1) and eccentricity 2;30 for radius 60 (3.4.7).
     - Every interval then agrees within 0.3 d except the two that are already forked as textual cruxes:

| Row | From the dates | From Ptolemy's Sun | Remark |
|---|---|---|---|
| A.3 | 13.06 d | 13.07 d | |
| A.6 | 51.40 d (+52 as printed) | 48.46 d → civil day +49 | crux; fork `mean_sun_emended` = 49 confirmed |
| A.8 | 54.40 d | 54.40 d | |
| B.4 / B.6 / B.8 | 6.64 / 55.08 / 69.53 d | 6.63 / 55.09 / 69.51 d | B.8 via the true Sun |
| C.2 | 17.75 d | 17.72 d | via the true Sun; confirms the pre-dawn placement of the hourless IX.8.3 (an evening placement gives 18.17 d, +18) |
| D.2 | 35.00 d | 35.00 d | |
| E.2 | 32.75 d | 32.80 d | equinox via the solar model |
| F.2 | 37.00 d | 37.29 d | |
| G.2 | 106.00 d | 106.02 d | |
| H.3 | 102.58 d (+102 as printed) | 72.37 d | crux; one Egyptian month; fork = 72 confirmed |
| H.7 | 192.58 d | 192.43 d | |
| J.3 / J.6 | 267.00 / 271.00 d | 266.99 / 270.98 d | |
| K.3 / K.6 | 1385.00 / 2902.00 d | 1385.00 / 2902.02 d | |
| L.3 / L.5 | 586.00 / 996.58 d | 585.95 / 996.53 d | |

4. **Forks.** For every fork set I checked three things:
   - exactly one option is primary;
   - each option has a justification that matches its `operational`;
   - every inferred feature has an explicit `none`, or an unbounded literal reading where the inference is a bound.
5. **Narrative level and leaks.** I read each row for simile and lying-tale framing, and scanned the whole file for date and name words, before and after the edits.

## Every edit made this round

### A. Operational tests that did not match the words (2 rows)

**B.2 (Venus beside the Moon).** Four problems were fixed:
- **The positional option.** It tested "the stated body-Moon offset", but the words state no Venus–Moon distance. They say only that Venus preceded the Moon's centre by 1½ times the amount it trailed β Sco: "προηγεῖτο ἡμιόλιον, οὗ ὑπελείπετο".
  - The only number on offer was the notes' "about 1/4 deg". That figure is derived from Ptolemy's computed lunar longitude.
  - The option now tests the stated ratio: (Moon's apparent centre − Venus) = 1.5 × (Venus − β Sco), with Venus between the two (`operational.relation`). The tolerances are unchanged.
- **The statement.** It said "in one line" with no quoted words. The licence now includes "μεταξὺ καὶ ἐπʼ εὐθείας ἦν … κέντρῳ τῆς σελήνης". The statement now gives the ratio instead of "just west".
- **The phase justification.** It said "before dawn", which the words do not say; the row gives 4¾ hours after midnight. It now uses a time-free argument: a Moon beside Venus as a morning star past greatest elongation is a waning crescent.
- **The unquoted basis.** The primary phase class rests on Venus being past its greatest morning elongation, and that was not quoted. "τὸν τῆς Ἀφροδίτης ἀστέρα μετὰ τὴν μεγίστην ἑῴαν ἀπόστασιν" was added.

**C.3 (lunar eclipse).** Three problems were fixed:
- **Fragment order.** The licence's fragments were out of text order. It is now the contiguous phrase, in text order, from "τὸν δὲ μέσον χρόνον" to "τῆς διαμέτρου".
- **`magnitude` (primary).** Its justification claimed "from the north", but its test is the magnitude only. The justification was corrected. The literal reading was added as a new non-primary option, `magnitude_and_side`: 5/6 of the diameter eclipsed from the north ("ἐξέλειπεν ἀπʼ ἄρκτων"), with `eclipsed_limb: north`, so the Moon's centre lies south of the shadow's centre at mid-eclipse.
- **`magnitude_and_time`.** It carried only a time tolerance. Its magnitude ranges are now explicit.

### B. Statement or primary features with no quoted words (8 further rows)

Each added fragment comes from the same row.

| Row | Feature | Added words |
|---|---|---|
| A.2 | "while Mercury is an evening star", the basis of the primary phase class | "μηδέπω ἐπὶ τὴν μεγίστην ἑσπερίαν ἀπόστασιν ἐληλυθότα" |
| A.5 | "about three days after Mars' opposition", a day interval and the basis of the primary phase class | "μετὰ γ ἔγγιστα ἡμέρας τῆς γ΄ ἀκρωνύκτου" |
| A.10 | "before sunrise" | "πρὸ τῆς τοῦ ἡλίου ἀνατολῆς, τουτέστιν" |
| A.10 | the longitudes behind the primary phase class (old crescent, about 30° west of the Sun) | Jupiter's sighted longitude and the mean Sun's, quoted |
| B.5 | the longitudes behind the primary phase class (waxing crescent, about 40° east of the Sun) | the Moon's apparent longitude and the mean Sun's, quoted; "same sentence" corrected to "this row" |
| D.4 | "(Ptolemy: about 1 1/2 deg)" | "τὸ δὲ μῆκος αὐτῆς α U+2220΄ ἐστιν ἔγγιστα μοίρας" |
| J.2 | "(morning)" | licence now starts at "ἑῷος ὁ τοῦ Ἄρεως" |
| J.5 | Ptolemy's identification of the star | "ὁ καθʼ ἡμιᾶς μετὰ τὸν ἐπʼ ἄκρας τῆς νοτίου πτέρυγος τῆς Παρθένου" and "Παρθένου μοίρας η δ΄"; the catalogue-epoch words between them are left out as date words |
| K.5 | "morning" | licence now starts at "ἑῷος" |

D.4's positional justification also spoke of stated latitude offsets. The words give only "μικρῷ νοτιώτερος", a little to the south, with no amount. The justification now says that only the side is tested.

### C. Statement wording beyond the words (3 further rows)

- **D.3.** The statement said "(evening)" as the time of the sighting. The row has no hour or time word, only "ἑσπέριος" (as an evening star). The statement is now worded like the ἑῷος rows C.1, G.1, L.1 and L.4: "no hour is stated". A note records that ἑσπέριος places the record in the evening part of its dated night, which fixes D.2's +35.
- **E.3.** The statement said "1 equinoctial hour". The words are "μετὰ μίαν ὥραν ἔγγιστα τῆς μεσημβρίας", with no "ἰσημερινή". This changes nothing operationally: on an equinox day the two kinds of hour coincide.
- **H.6.** The statement read the future infinitive "ἀφέξειν" as a separation measured on the day. The words give the observer's expectation for the passage: "it seemed it would stand off" more than 3 moons south of the common star.
  - The statement, the notes and the positional justification now say so.
  - The same-day latitude test is kept, labelled as the drafter's approximation. `none` remains available.

### D. A primary option with a day bound the words do not give (4 rows)

| Row | The words | Primary option |
|---|---|---|
| A.1 | "μηδέπω … ἐληλυθότα" | `ge_after_within_j` |
| I.1 | "οὐδέπω … ἐληλύθει" | `ge_after_within_j` |
| B.1 | "μετὰ τὴν μεγίστην ἑῴαν ἀπόστασιν" | `ge_before_within_j` |
| J.4 | "παρεληλύθει … τὴν μεγίστην ἑῴαν ἀπόστασιν" | `ge_before_within_j` |

None of these words gives a number of days. Each primary option bounds the greatest elongation to j = 7–60 days, but its justification did not say that the bound is the drafter's. Round 1 added the unbounded literal reading as a non-primary option, but the primary option's own justification still read as if the words gave the bound. The bound is an inferred day interval (critique issue 2). Each justification now says that j is the drafter's bound, an inference, and names the unbounded option. Values and primaries are unchanged.

### E. Notes only (7 rows)

- **A.4.** "To the mean Sun" rests on a definition in another row. It is now quoted from 10.7.2: "τριῶν ἀκρωνύκτων τῶν πρὸς τὴν μέσην τοῦ ἡλίου πάροδον διαμέτρων".
- **B.9.** The licence's "9β" is the numeral ϙβ (92), with the koppa printed as the digit 9. Ptolemy's own reduction in the row confirms it: his Moon is 92 1/8° east of his Sun.
- **C.2, D.2, G.2, L.3 and L.5.** An endpoint of each interval has no hour word. Each note now records two things:
  - its civil day comes from ἑῷος or ἑσπέριος (the morning or evening part of the dated night);
  - Ptolemy's Sun figures confirm the offset (table above). Each offset would be one day larger or smaller with the other placement.

### F. File-level fields

- **`rules_applied`.** The rule "longitudes … are not used" was not true of every row. It now lists the exceptions:
  - A.10 and B.5 choose their phase class from longitudes stated in the row, and each is forked with `none`;
  - J.7 uses the difference of two Venus longitudes Ptolemy gives, forked with `none`;
  - B.7 and B.9 use the measured Sun–Moon distance, which is the observation itself;
  - where a licence quotes the Sun's longitude (A.10, B.5, B.7, B.9), that is a season statement which no option uses except through the Sun–Moon difference.
- **`conventions.licence_words`.** A note was added on the two spellings of the half sign.
- **`license_check`.** This is now round 2's block. Round 1's block is `license_check_r1`, with its report pointer moved to the copy.
- **The `sets` array is unchanged.** I re-checked every `observer_place` word string at its ref, and all are exact. Every set gives a window width only (136 years), with no position.

## Rows confirmed `ok` without edit (48)

- **Intervals (15):** A.3, A.6, A.8, B.4, B.6, B.8, E.2, F.2, H.3, H.7, I.4, J.3, J.6, K.3, K.6.
  - All were recomputed (method step 3).
  - The A.6 and H.3 cruxes are confirmed by Ptolemy's mean Sun.
  - E.2 crosses eras by the link the text states at 3.1.9, and K.3 by the links at 3.7.4 and 10.9.2.
- **Planet rows (20):** A.7, A.9, C.1, D.1, E.1, F.1, F.3, G.1, G.3, H.1, H.4, H.8, J.1, J.7, K.1, K.4, K.7, L.1, L.4, L.6.
  - Each side-of-Sun and time word is quoted.
  - In H.1, H.4, H.8, K.1 and K.7, the greatest-elongation status is Ptolemy's statement in the row, and his selection rule is at 9.7.2, 9.7.8 and 9.7.17. `visible_only` stays primary, since the old records themselves say only ἑῷος or ἑσπέρας.
  - J.7 uses Ptolemy's two longitudes for the four-day motion. It is licensed at narrator level, has `none`, and is now named in `rules_applied`.
- **Moon-phase row (1):** B.7. The measured Sun–Moon distance and the time words are quoted, and "last quarter" is licensed by "τεταρτημορίου … ἔγγιστα τὴν μέσην ἀποχὴν". B.9 is the same kind of record, but it was edited above for a note only.
- **Star rows (12):** B.3, F.4, H.2, H.5, H.9, I.2, I.3, I.5, K.2, K.8, L.2, L.7. Each has `none`. F.4's candidate branches (round 1) stand.

## What the next stage must know

1. **Hash.** DESIGN §12.4 records `758ee789…4c83` as "the checked file". The file is now `18b3ff01…b458`. Its history is:
   1. the builder's output, `e16c559d…37e9`;
   2. round 1's output, `758ee789…4c83`;
   3. round 2's output, `18b3ff01…b458`.

   The pre-edit copy is `results/license-check-almagest/r2/controls_almagest.pre_r2.json`. The script `r2/apply_edits_r2.py` replays this round's edits from it, and its log is `r2/apply_edits_r2.log`.
2. **The builder.** Re-running `results/controls-almagest/build_prereg.py` would silently undo both rounds of edits.
3. **New vocabulary for the harness:**
   - B.2's `positional` carries `relation`, a ratio test against β Sco.
   - C.3's new `magnitude_and_side` carries `eclipsed_limb: north`.
   - C.3's `magnitude_and_time` now carries `umbral_mag_range` explicitly.

   These come on top of round 1's `bound: same_apparition` and F.4's `star_candidates`. ALM-C is report-only and its eclipse row is set to none in the B&M projection, so the gate is unaffected. B.2's positional is not its row's primary.
4. **Two primary phase classes rest on Ptolemy's numbers, not on words.** In A.10 and B.5 they come from his stated longitudes, and the mean Sun's longitude is from his tables. DESIGN's B&M-type projection uses the phase-class options of moon-phase rows, so the gate's lunar-phase input for these two rows is coordinate-derived.
   - Each row has `none`.
   - If the design wants word-derived phases only, put these two rows at `none` in the projection.
   - The other inferred phases (A.2, A.5, B.2) need no coordinates.
5. **Hourless records.** The civil day of a record with no hour word (C.1, D.3, G.1, L.1, L.4) comes from ἑῷος or ἑσπέριος, and Ptolemy's Sun figures confirm every such offset. The harness should evaluate these rows at DESIGN's "dawn" or "evening" instant accordingly.
6. **Sites.** The following records state no site:
   - in ALM-A, X.8.2 and IX.9.4;
   - in ALM-C, IX.8.3.

   Their sets' Alexandria coordinates, and DESIGN's default site, are therefore an inference, as the sets' own `observer_place` strings say. I added no site fork, because its `none` branch, the harness default, is the same place. ALM-K's `observer_place` mentions a possible Mesopotamian archive, and K.8 mentions "Babylonian usage" for the cubit. Both are prose hints, not clues. DESIGN already runs Babylon as ALM-K's sensitivity.
7. **The `ref`s point at the withheld dates.** Every `ref` points at a row that contains the withheld date words, so the searcher must read only the operational fields. `r2/interval_check.txt` contains date words too.
8. **Drafter's glosses.** The following remain the drafter's, not the text's:
   - the star identifications: β Sco, δ Sco, δ Cap, β/ζ Tau, δ Cnc, α Lib, β Vir, η Vir, and F.4's candidates;
   - the units: 1 moon = 0.5°, 1 cubit ≈ 2°, "above" = north (following Ptolemy's own reduction in 9.7.15–16).
