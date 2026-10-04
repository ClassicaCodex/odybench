# Licence check of `data/prereg/controls_real.json`

Checked 2026-10-04. This was an independent check: I did not write these clue sets.

**What I did not read.** I did not open `data/prereg/controls_real_truth.json` or `docs/research-controls.md`. I also did not open the drafter's own record (`docs/controls-real-drafting.md`), so that its reasoning would not shape mine. Every judgement below comes from the cited rows of `data/text/*.tsv`, read next to the clue file.

## Method

1. **Every quoted word.** For each clue row and each set-level `observer_place` entry, I checked that every `licence_words` string occurs exactly in the cited row of the cited text file.
   - Tool: `results/license-check-controls-real/dump.py` [computed by me with dump.py].
   - Before the edits, all 139 strings were present, character for character. No ref was missing, and none pointed at the wrong row.
   - After the edits, `apply_license_check.py` re-checked all 141 strings: all present.
2. **Every clue row (78).** I read each row against its cited text. For each feature in the statement, I asked four questions:
   - Is it licensed by the quoted words, in that passage, at the stated narrative level?
   - Does it carry a time of day, season, magnitude, totality, site, year interval or day interval that the words do not state?
   - Are the fork options complete, including "none" where the feature is only implied, and is each one justified?
   - Is a simile or lying tale used as a date carrier?
3. **Fixes.** I fixed the file in place with `results/license-check-controls-real/apply_license_check.py`. Every clue row now carries `license_check` ("ok", or "edited: <what and why>"). A top-level `license_check_record` names this report.
4. **Arithmetic.** I re-did the Egyptian-calendar arithmetic by hand:
   - Night indices: E 29, 383, 560; H 6130, 6662, 7164.
   - Differences: 354, 177, 532 and 502 nights. 311,784 nights from E2 to H2.
   - Ptolemy's stated intervals: 354 d 2½ h; 176 d 20½ h; 1 Egyptian year + 166 d 23¾ h; 1 Egyptian year + 137 d 5 h; 854 Egyptian years 73 d 23⅚ h.
   - All of these agree once the stated times before and after midnight are applied [computed by me, by hand].
5. **Leak scan.** I scanned for leaked answers: no year in BC, astronomical year, Julian Day, NASA/canon magnitude or computed hour appears anywhere in the clue file. The only "NASA" is the magnitude convention, and the only "ctl §" is a citation of the critique.

**Freezing.** The file was frozen before this check (sha256 `eb1f0401…9256`, recorded in `results/controls-real-drafting/clue_file_sha256.txt`). The frozen copy is kept byte for byte at `results/license-check-controls-real/controls_real.before-license-check.json`. The checked file's sha256 is `135fba67…83f8`; its CRLF line endings are kept.

**Re-running the build script would undo these edits.** `results/controls-real-drafting/build_controls_real.py` does not contain them, so it must not be re-run over this file. I did not edit it, because it is not mine.

## Summary

- **Rows:** 78 checked. 64 are "ok" and 14 edited.
- **Answer leaks:** none of the leaks listed in critique issue 2 survives. The specific ones were:
  - no "morning" for Thuc. 4.52;
  - no "total" for 7.50;
  - no hour or site for Xen. 2.3.4;
  - no year count linking Xen. 4.3.10;
  - no Julian "summer" for Livy 44.37;
  - no hour or season for Diod. 20.5;
  - no assumed site "Rome" for Livy 22.1.9.
- **Similes and lying tales:** none is used as a date carrier. None occurs in these passages.
  - Gallus's forecast in Livy 44.37.5 is a character's speech in indirect form. It is used only because the narrator confirms it ("edita hora", 44.37.8).
  - Aristander's prophecy in Arrian 3.15.7 is used only through the narrator's statement that it came true in the eclipse month.
- **The one substantive change: unstated sites.** Seven site forks had an observing place as their primary option, although the set itself records that observer as "unstated":
  - T1-SITE, T2-SITE, X1-SITE and X2-SITE (in the pass/fail controls);
  - L1-SITE, L3-SITE and L4-SITE (in the hard case).

  I moved their primary to "none". The other site options are kept as alternatives. **This weakens R-THUC and R-XEN in the primary run**; see "Consequences" below.
- **The other seven edits** make a statement match its words, lengthen a quotation to cover what the statement uses, add a missing justification, or add one missing fork option.

## Every edit

| Row | Set | What was wrong | Edit |
|---|---|---|---|
| T1-SITE | R-THUC | Primary "box" (Greek mainland and Aegean, "where the war was being fought"). Thuc. 2.28 names no place where the eclipse was seen, and the set-level `observer_place` says "unstated". Policy 2 bars inference from narrative context or outside knowledge in a primary option. | Primary moved to "none". "box" and "point" (Athens) are kept as alternatives, their justifications marked as inferences from context. |
| T2-SITE | R-THUC | Same: 4.52.1 names no observing place. The Troad sentence that follows (4.52.2) is about the Lesbian exiles, not the eclipse. | Primary moved to "none". |
| X1-SITE | R-XEN | Same. Hell. 1.6.1 names Athens only for the temple fire ("ἐν Ἀθήναις ἐνεπρήσθη"), not for the eclipse. | Primary moved to "none". |
| X2-SITE | R-XEN | Same. Hell. 2.3.4 uses the eclipse only to date Lycophron's battle; no observer is placed. | Primary moved to "none"; "box", "thessaly" and "athens" are alternatives. |
| L1-SITE | H-LIVY | Same. "solis orbem minui visum" (22.1.9) carries no place name of its own. The set says "unstated". | Primary moved from "italy-box" to "none". "sardinia" (the grammatical run from "in Sardinia autem"), "italy-box" and "rome" are kept. |
| L3-SITE | H-LIVY | Primary "rome". The row's own statement says the site is "not stated as such", and the set says "unstated" ("Rome by inference only"). Critique issue 2 flagged exactly this assumption. | Primary moved to "none". |
| L4-SITE | H-LIVY | Primary "rome", from the expiation at the crossroads and a companion prodigy on the Aventine. The darkness itself is not placed, and the set says "unstated". | Primary moved to "none". |
| PB-E3-MAG | R-PTOL-BAB | Statement said "more than half the diameter". The record says only "πλεῖον τοῦ ἡμίσους", and does not say half of what. | Statement reworded. Options are unchanged, because umag > 0.5 is already the weaker of the diameter and area readings (taking the umbra's radius as 2.7 lunar radii, umag 0.50 covers 46% of the disk's area and half the area needs umag ≈ 0.53 [computed by me, circle-overlap formula]). |
| T2-ECL | R-THUC | Statement asserted "partial" as if stated; the words give only "ἐκλιπές τι". | Statement reworded to show the upper bound as a reading. Options "partial" (primary) and "any" are unchanged. |
| T2-SEASON | R-THUC | The primary "early" option starts at Sun longitude 330°, but its justification did not say that this placement of "ἅμα ἦρι ἀρχομένῳ" is the drafter's. The same row's "half-year" option starts at 0°. | Justification now says that the 330° start and the two-month width are both the drafter's, and that the text gives no longitude. Bounds unchanged. |
| A-TIME-CURTIUS | R-ARBELA | Statement said "two days after crossing the Tigris". That is a day interval the words do not give: 4.10.1 says only that the king kept a standing camp there for two days ("Biduo ibi stafiva [stativa] rex habuit"; the local row has the OCR slip), and the eclipse sentence follows with "Sed". | Statement reworded: the two days are narrative context and are not used. The operational option never used them and is unchanged. |
| X1-ECL | R-XEN | "ἐξέλιπεν ἑσπέρας" states no magnitude. The primary "use" requires an umbral eclipse, which is an inference, and the only alternative was to drop X1. | Added the alternative "penumbral-deep" (umbral, or penumbral magnitude ≥ 0.7, Moon up), the same as T3-ECL. The primary is unchanged. |
| PA-INT | R-PTOL-ALEX | The statement gives hours, but the first quotation stopped at "ἡμερῶν ρξς". The hours "κγ U+2220΄ δʹ" are what make the H1→H2 count 532 nights rather than 531. | `licence_words` lengthened to the full interval clauses of 4.6.16 (apparent and mean hours), cut from the local row. |
| PC-LINK | R-PTOL-CHAIN | The quotation gave only the 854 years and 73 days, and the day total. The 311,784-night count also depends on the hours (23 1/2 1/3 apparent) and on the two before-midnight times in 4.7.1. | `licence_words` lengthened to four strings from 4.7.1: E2's date and time, H2's date and time, the interval with hours, and the day total with hours. |

**Metadata (not a clue row).** I added the keys `1.1.1.1`, `7.50.1.1` and `7.50.3.1` to R-THUC's `texts[].local_keys`. T1-SITE, T2-SITE and T3's `observer_place` cite them, but the list omitted them.

## Rows found "ok", by set

**R-PTOL-BAB** (14 rows; 13 ok)
- **Babylon** is stated: "ἐκ τῶν ἐν Βαβυλῶνι τετηρημένων" (4.6.3).
- **Dates and intervals:** PB-CAL, PB-INT-12 and PB-INT-23 match Ptolemy's dates and his day counts in 4.6.6.
- **Magnitudes:** E1 "ὅλη" (whole), E2 "δακτύλους γ" (3 digits), E3 "πλεῖον τοῦ ἡμίσους" (more than half). The directions "ἀπὸ νότου" and "ἀπʼ ἄρκτων" are both quoted.
- **Times:**
  - Each row separates the Babylonian record ("φησίν") from Ptolemy's reduction, and gives the reduction as an alternative.
  - PB-E1-TIME: the 2 h upper bound for "μιᾶς ὥρας ἱκανῶς παρελθούσης" is labelled as the drafter's.
  - PB-E2-TIME: the primary takes Ptolemy's "mid-eclipse at midnight". That reading is consistent with PB-E2-MAG, which reads the 3 digits as the maximum. The literal "in progress at midnight" is an alternative, so I left it.
- **Solar longitudes:**
  - They are Ptolemy's own computed values, quoted, with "none" options.
  - The ±5° tolerance is the drafter's, and is labelled as such.
  - The longitude conversions are correct: Pisces 24½° = 354.5°, Pisces 13¾° = 343.75°, Virgo 3¼° = 153.25°.

**R-PTOL-ALEX** (13 rows; 12 ok)
- **Alexandria** is stated (4.6.13).
- **Magnitudes:** "ὅλη"; "τὸ U+2220ʹ καὶ γʹ τῆς διαμέτρου" (½ + ⅓ = ⅚ of the diameter, 10 digits); "τὸ ἥμισυ τῆς διαμέτρου" (half the diameter).
- **Times:** "πρὸ ἡμίσους καὶ τετάρτου μιᾶς ὥρας"; "πρὸ α ὥρας"; "μετὰ δ ὥρας". All are Ptolemy's own reductions ("ἐπελογισάμεθα"), at narrator level.
- **Solar longitudes:** Taurus 13¼° = 43.25°, Chelae 25⅙° = 205.17°, Pisces 14 1/12° = 344.08°.
- **Calendar:** night indices and differences are as stated (see Method).

**R-PTOL-CHAIN** (1 row): PC-LINK was edited (see the table). Its arithmetic is correct: 854 × 365 + 73 = 311,783 days, and 311,784 nights once the hours are counted.

**R-THUC** (14 rows; 11 ok)
- **T1-ECL:** "πάλιν ἀνεπληρώθη" (filled out again) licenses "end seen", and "none" is an alternative.
- **T1-PHASE** adds no constraint.
- **T1-TIME:** "μετὰ μεσημβρίαν" (after midday). The primary is the middle reading (maximum after noon); "first contact after noon" and "none" are alternatives.
- **T1-SHAPE:** "μηνοειδής" (crescent-shaped). The 0.5 crescent threshold is the geometry stated in policy 3, and the alternative "crescent-passed" allows totality.
- **T1-DARK:** "ἀστέρων τινῶν ἐκφανέντων" (some stars appeared) maps to the design's class X4, with X3 and "none" as alternatives.
- **Seasons:**
  - T1-SEASON and T3-SEASON: "θέρους" (summer) is stated. The half-year is licensed by 5.20.3 ("ἐξ ἡμισείας ἑκατέρου τοῦ ἐνιαυτοῦ").
  - The placement on the equinoxes is labelled as the drafter's, and "campaign" and "none" are alternatives.
  - T3's summer runs from 7.19.1 ("ἦρος εὐθὺς ἀρχομένου") to 8.1.4 ("τὸ θέρος ἐτελεύτα"). I checked every row between them: no winter begins in that span. 7.31.3's "τοῦ χειμῶνος" refers back to the previous winter.
- **T3-ECL:** "πασσέληνος"; no magnitude and no hour are entered, and the row notes "Totality is not stated".
- **War-year intervals (T-INT-12, T-INT-13):** licensed by the year-end formulas at 2.47.1 (year 1), 4.51.1 (year 7), 7.18.4 (year 18) and 8.6.5 (year 19). All are present, and the intermediate year-ends are consistent.
  - T1 at 2.28 falls inside year 1.
  - T2 at 4.52 immediately follows the end of year 7.
  - T3 at 7.50 falls in year 19.
- **T3's observer place:** "the Athenian camp at Syracuse" is narrative-stated (7.50.3: the Syracusans prepare to attack them "by ships and by foot"; "ἐκ τοῦ στρατοπέδου"). The first licence string, "ἐς τὰς Συρακούσας" (7.50.1), describes Gylippus arriving, but together with 7.50.3 it places the camp.

**R-XEN** (9 rows; 7 ok)
- **X1-TIME:** "ἑσπέρας" (in the evening). The 3 h width is labelled as the drafter's; "before midnight" and "none" are alternatives.
- **X1-ECL:** the "exclude" option for a possible gloss stays as written.
- **X-INT-12:** the year structure checks out.
  - The year opens at 1.6.1 ("τῷ δʼ ἐπιόντι ἔτει").
  - The next year opens at 2.1.10 and ends at 2.2.24 ("ὁ ἐνιαυτὸς ἔληγεν").
  - The year after that opens at 2.3.1.
  - No other year boundary lies in between: 2.1.8's "τούτῳ δὲ τῷ ἐνιαυτῷ" refers to the current year.
  - The 1–3 year bound follows.
  - The unused war-year counts ("τεττάρων καὶ εἴκοσιν", 1.6.1; "πέντε καὶ εἴκοσι", 2.1.7) are present and consistent.
- **X2-ECL:** "περὶ ἡλίου ἔκλειψιν" (about the time of an eclipse of the Sun); no hour and no magnitude are entered.
- **Seasons from narrative order:** X2-SEASON and X3-SEASON both have primary "none".
- **X3** is unlinked from X1 and X2, as it should be: no year count joins them.
  - X3-ECL: "μηνοειδὴς ἔδοξε φανῆναι" (seemed to appear crescent-shaped).
  - X3's observer: the narrative puts it at Agesilaus' army at the entry into Boeotia ("ὄντος δʼ αὐτοῦ ἐπὶ τῇ ἐμβολῇ", 4.3.10; "μέχρι πρὸς τὰ Βοιωτῶν ὅρια", 4.3.9).

**R-ARBELA** (6 rows; 5 ok)
- **A-ECL** quotes all four sources.
- **A-MAG:** the primary, "> 0.5", is the weakest reading compatible with both Arrian ("τὸ πολύ", the greater part) and Curtius ("lumen omne foedavit", fouled all its light), as policy 2 requires when sources disagree.
- **A-TIME-PLINY:** "noctis secunda hora" (the second hour of the night), at Arbela ("apud Arbilam").
- **A-SICILY:** "eademque in Sicilia exoriens" (the same eclipse seen rising in Sicily).
- **A-MONTH:** Boedromion (Plutarch 31.4) or Pyanepsion (Arrian 3.15.7), with the union as primary.
- **Site:** the Tigris camp is stated (Arrian 3.7.5 local, "διαβαίνει τὸν πόρον … ἐνταῦθα ἀναπαύει τὸν στρατόν"; Curtius "ibi").

**R-PYDNA** (7 rows; all ok)
- **Timing:**
  - P-TIME: "ab hora secunda usque ad quartam horam noctis" (from the second to the fourth hour of the night), confirmed by "edita hora" (at the hour announced).
  - Plutarch: "ἐπεὶ δὲ νὺξ γεγόνει" (when night had come).
- **The Moon:**
  - P-ECL and P-ALT: "πλήρης οὖσα καὶ μετέωρος" (full and high in the sky). The 10° altitude is labelled as the drafter's.
  - P-MAG: Plutarch's "ἠφανίσθη" (vanished) supports "total" as primary; "deep" and "umbral" are alternatives.
  - P-END: "donec luna in suam lucem emersit" (until the Moon came out into its own light); "ὡς εἶδε πρῶτον … ἀποκαθαιρομένην" (when he first saw it clearing).
- **P-SEASON** is licensed by Livy 44.36.1, "Tempus anni post circumactum solstitium erat" (the solstice had come round), and Plutarch 16.9, "θέρους … ὥρα φθίνοντος" (waning summer). The union is the primary.
- **P-DATE:** the Roman date carries a free offset as primary, as the rules require.
- **Site:** the camps before Pydna are stated (Plut. 16.5, "πρὸ τῆς Πύδνης"; Livy 44.42.7).

**R-DIOD** (2 rows; both ok)
- **D-ECL:** "ὥστε ὁλοσχερῶς φανῆναι νύκτα, θεωρουμένων τῶν ἀστέρων πανταχοῦ" (so that it seemed full night, with stars seen everywhere). The primary is class X3, with "total" and X4 as alternatives. No hour and no season are entered, which is correct.
- **D-SITE:** the narrative puts the observers in Agathocles' fleet at sea on the day after the escape ("τῇ δʼ ὑστεραίᾳ"; "οἱ περὶ τὸν Ἀγαθοκλέα"). The 150 km radius is labelled as the drafter's, and the whole crossing ("route-box") is an alternative.

**H-LIVY** (12 rows; 9 ok) — a hard case.
- **Magnitudes:** L1/L2-ECL "solis orbem minui visum" (the Sun's disk seemed diminished), with any magnitude as primary; L3-ECL "obscurata lux est" (the daylight was darkened).
- **Dates from narrative order:** L1-, L2- and L4-DATE all have primary "none".
- **L3-DATE:** the Roman date carries a free offset.
- **L1b** (Arpi) is excluded as primary.
- **L2's site,** Cumae, is stated ("Cumis").
- **L4-DARK** says plainly that "the text does not say eclipse", and has a "not-eclipse" option. Its hours are stated: "inter horam tertiam ferme et quartam" (between about the third and fourth hour).

## Consequences of the site change

- **R-THUC** keeps its stated observer only for the lunar eclipse T3, at the Syracuse camp. In the primary run, T1 and T2 must satisfy their other clues at some place on Earth. "After midday" (T1-TIME) and "stars seen" (T1-DARK) then constrain very little.
- **R-XEN in the primary run** reduces to an evening lunar eclipse somewhere (X1), a solar eclipse somewhere 1–3 years later (X2), and an unlinked crescent eclipse at the Boeotian frontier (X3).
- **The gate.** Both sets are therefore less likely to give a unique date in the primary run. That bears on the PC-R gate (DESIGN, prediction 23).
- **The box options remain** as the first alternative, so the bench can report how much the regional assumption adds.
- **If the design owner wants a regional box in the primary,** that is a design rule, for example: "a historian's undated notice places an unstated observer in the region of the narrative". It should be written into DESIGN and the file's policies and applied uniformly. It should not be decided row by row in the clue file.

## Flagged, not edited (judgement calls for the design owner)

1. **A-MONTH.** Its primary converts an Attic month name into a sky season with a modern reconstruction: month 1 begins at the first new moon after the summer solstice, with an offset of ±1 lunation. That rule is secondary knowledge, not in these texts. The row and the file's `conventions` say so, and "none" is an alternative.
   - This is the only primary option in the file that depends on a calendar reconstruction outside the text.
   - The Roman dates are entered with a free offset, as the rules require.
   - The Egyptian dates fix intervals only, and Ptolemy states those intervals himself.
2. **"naive" options in P-DATE and L3-DATE.** These read the Roman date as Julian (offset 0). Each is labelled "sensitivity only; not a licensed reading". They are harmless as non-primary options, but a result under them must never be reported as a reading of the text.
3. **L4-DARK.** The primary reads "tenebrae obortae" (darkness came on) as a solar eclipse. The text gives no cause. I kept it because the row's kind is "darkness", it says plainly that the text does not say eclipse, and it carries a "not-eclipse" option. This is the same step the bench tests for the Odyssey's darkness clue.
4. **Pliny's "apud Arbilam Magni Alexandri victoria"** may name the battle rather than the observing site. A-TIME-PLINY uses Arbela as the site. The camp across the Tigris is about 1° of longitude away (about 4 minutes of time; drafter's coordinates). This matters only for the "onset" option.
5. **D-SITE** has no "none" option. I judged its site to be stated by the narrative (the observers are the fleet at sea) and its radius to be an operational choice, so "none" is not required. The weakest reading is "route-box".

## Files

- `data/prereg/controls_real.json`: edited in place (14 rows); `license_check` on all 78 rows; `license_check_record` added.
- `results/license-check-controls-real/controls_real.before-license-check.json`: the frozen file before this check (sha256 `eb1f0401…9256`).
- `results/license-check-controls-real/dump.py`: checks the strings and dumps each set with its cited rows (`dump_<set>.txt`, `check_summary.txt`).
- `results/license-check-controls-real/show.py`: compact viewer used for reading.
- `results/license-check-controls-real/apply_license_check.py`: applies the edits, cuts the lengthened quotations from the local rows, re-checks every string, and confirms exactly one primary per fork list.
