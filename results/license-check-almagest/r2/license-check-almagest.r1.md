# Licence check: `data/prereg/controls_almagest.json`

**Checked:** 2026-10-04, by an independent agent that did not draft these sets.

**Inputs read:**
- the clue file;
- `data/text/ptolemy-syntaxis-grc.tsv`: every cited row, plus the context rows 3.1.9, 3.7.4, 4.6.13, 9.7.1–9.7.17, 9.8.1–2, 9.9.1–2, 9.10.1–2, 10.1.1–2, 10.2.1–2, 10.4.2 and 10.7.2;
- `docs/critique-design.md` issues 2, 3 and 15.

**Not read:**
- `controls_almagest_truth.json` or any other truth file;
- `docs/research-controls.md`;
- the drafting record `docs/controls-almagest.md` and `results/controls-almagest/` (both may carry the answers).

**Result:**
- 72 rows checked. 29 are `ok`; 43 were edited.
- Of the 43 edits, 9 touch only the notes. 34 change the licence words, the statement wording, the fork options or the primary option.
- No row was removed. No operational option used a time of day, season, magnitude, totality, site, or year or day interval that the text does not state, with one exception: four fork sets bounded "not yet at" or "already past" greatest elongation by a day count the words do not give, and none of their options was the literal, unbounded reading. That option has been added.
- Six statements carried an unstated time-of-day gloss ("before dawn", "a morning object") that no operational option used. They have been reworded.
- No simile or lying tale occurs. Every row is Ptolemy narrating an observation, his own or a record he reports.

Every row now carries `license_check: "ok" | "edited: <what and why>"`. A top-level `license_check` block records:
- the SHA-256 of the file before editing (`e16c559d…37e9`);
- the pre-edit copy;
- the edit script.

## Method

1. **Ref and words.** For each row I opened the `ref` row in the TSV. I tested every `…`-separated fragment of `licence_words` as an exact substring. The check ignores only the tonos/oxia encoding difference: the export mixes U+03AF and U+1F77 in the same word, e.g. μεσονυκτίου at 9.10.3 and at 10.8.2. Every fragment I added is cut from the row by `frag()` in the script, so it is the row's own characters.
2. **Each feature of the statement.** For each feature I asked three questions:
   - Is it in the quoted words?
   - Is it in that passage?
   - Is it at that narrative level?

   I treated time-of-day, side-of-Sun ("evening"/"morning") and direction words as features that need quoted licence.
3. **Intervals.** I recomputed all 19 date-derived interval rows from the Egyptian dates as they stand in the cited rows [computed by me: `results/license-check-almagest/egyptian_check.py`, output `egyptian_check.txt`].
   - Days are 30-day months plus 5 epagomenal days.
   - The civil-day rule is the file's own: "D into D+1" goes to D in the evening and to D+1 at dawn.
   - The era links come from the text only:
     - Antoninus 2 = Nabonassar 886 [9.10.3];
     - Antoninus 3 = year 463 from Alexander's death [3.1.9];
     - Nabonassar to Alexander's death = 424 years [3.7.4; also the pair 52/476 at 10.9.2];
     - Philadelphus 13 = Nabonassar 476 [10.4.6].
   - **All 19 reproduce exactly.**

   I then cross-checked each interval against the mean-Sun longitudes that Ptolemy states in the same rows, at his mean motion of 0;59,8,17,13,12,31°/day [computed by me: `meansun_check.py` / `meansun_check.txt`]. Every interval agrees to within 0.3 day except the two the drafter had already forked as textual cruxes:
   - **ALM-A.6.** The day as printed is 52. The mean Sun gives 48.5, which matches the emended value of 49.
   - **ALM-H.3.** The date as printed gives 102. The mean Sun gives 72.4, which matches the emended value of 72. The conflict is exactly one Egyptian month.

   **Both forks are therefore justified by the text's own numbers.** ALM-I.4 (+4) and the last step of ALM-J.6 (+4) are stated in words ("μετὰ δ ἡμέρας"), and the calendar day numbers in those rows agree.
4. **Forks.** For each fork set I checked three things:
   - Does each option have a justification?
   - Is there exactly one primary option?
   - Does every inferred feature have an explicit `none`?

   Every inferred lunar phase (A.2, A.5, A.10, B.2, B.5) has `none`. So does every star relation. Features the words state outright do not need `none`:
   - greatest elongation "τὸ πλεῖστον ἀπέστη";
   - ἑῷος;
   - the eclipse in C.3;
   - the equinox in E.3;
   - the measured elongations in B.7 and B.9.
5. **Leaks.** I scanned the whole file for era names, regnal years, Egyptian, Dionysian and Chaldean month names, observer names, BC/AD and Julian dates. **None are present**, before or after the edits. My own added notes were also kept free of era names.

## Edits by kind

### A. A feature in the statement had no licensing words quoted (17 rows)

The feature was in the row, but the licence string did not quote it.
- **Time of day:** A.1, A.2, A.5, A.7, A.10, B.1, B.5, B.7, D.1, I.1.
- **Time and direction:** B.9. The licence quoted no time and no "east". The row says "μέλλοντος μὲν δύνειν … τοῦ ἡλίου" and "εἰς τὰ ἑπόμενα διάστασιν".
- **Evening, for time and for side of the Sun:** E.1, F.1, F.3, L.6. E.1's licence did not contain "evening" at all; its row has "ἐσπέρας" and "τὴν ἑσπερίαν … ἀπόστασιν".
- **Fragments out of text order, and the time word missing:** G.3.
- **Only one of two longitudes quoted:** J.7 quoted only the second of the two longitudes whose difference it uses.

Where the time phrase contains a day numeral (A.1, A.2, B.9), I left the numeral out with `…`, consistent with withholding the dates. **None of these changes the operational options.**

### B. The licence string was not a substring of the cited row (7 rows)

**H.1, H.4, H.8, K.1, K.7.** The string carried a bracketed row prefix such as "[9.7.8] …". In H.1 and H.4 the words came from another row (9.7.8, 9.7.10). Yet the cited rows themselves contain Ptolemy's statement that the elongation was greatest: "γέγονεν ἄρα ἡ μεγίστη τῆς μέσης ἀπόστασις ἑῴα / ἑσπερία", or for K.1 "γέγονεν ἄρα καὶ αὕτη ἡ διάστασις". They also contain the time word ὄρθρου or ἑσπέρας. I replaced the licence with those same-row words. The chapter-level selection rule now sits in the notes and the GE-option justifications:
- 9.7.2, "μεγίστων ἀποστάσεων τηρήσεις";
- 9.7.8;
- 9.7.10 and 9.7.13;
- 9.7.17, "τῶν δὲ μεγίστων ἀποστάσεων".

The old records' own words remain "ἑῷος/ἑσπέρας" only, so `visible_only` stays primary, as drafted.

**I.4 and J.6.** The string was the interval phrase plus an appended bracketed placeholder. I.4's placeholder also called both dates Egyptian. In fact the second record has only a date in another calendar, and the interval is stated in words. The licence is now the phrase alone, and the notes are corrected.

### C. A time of day in the statement was not in the words (6 rows; wording only)

- **B.2.** "Before dawn": the row gives "4 3/4 equinoctial hours after midnight". Whether that falls before dawn depends on the season, which the file deliberately does not use. Reworded to the stated hour.
- **C.1, G.1, L.1, L.4.** "(before dawn)": these rows have no hour word, only ἑῷος. They now read "morning star (ἑῷος) … no hour is stated".

  In contrast, A.7, G.3, H.1, I.1, K.1 and K.7 keep "before dawn". Their rows carry ὄρθρου.
- **A.9.** "(a morning object)" could be read as heliacal morning-star status. The words say Jupiter was sighted before sunrise, about 5 equinoctial hours after midnight. Reworded, and the licence was extended to the time and sighting words.

**No operational option depended on these words.**

### D. Incomplete fork sets: an unstated day bound (4 rows)

| Row | The words | What the drafted options did |
|---|---|---|
| A.1 | "μηδέπω … ἐληλυθότα" (not yet come to) | bounded "not yet" to j = 7/15/30 days, or dropped it (visible_only) |
| I.1 | "οὐδέπω … ἐληλύθει" (not yet come to) | bounded "not yet" to j = 7/15/30 days, or dropped it (visible_only) |
| B.1 | "μετὰ τὴν μεγίστην ἑῴαν ἀπόστασιν" (after) | bounded "past" to j ≤ 60 days, or dropped it |
| J.4 | "παρεληλύθει" (had passed) | bounded "past" to j ≤ 60 days, or dropped it |

The words give no number of days, so a 7–60-day bound is a day interval the text does not state (critique issue 2). I added the literal unbounded reading as a non-primary option:
- `ge_after_same_apparition` for A.1 and I.1;
- `ge_before_same_apparition` for B.1 and J.4.

Both take `operational: {"bound": "same_apparition"}`. The j-day options stay as narrower readings.

### E. Other edits (4 rows: three substantive, E.3 notes only)

- **F.4 (star relation, Aquarius quadrilateral).**
  - The row's own note said `none` is the default because the star is not securely identified, but `positional` was marked primary. I made `none` primary to match.
  - `positional` named no star, so it could not run. I added the drafter's candidates (λ, φ, ψ1–3 Aqr) with `candidate_rule`: each candidate is a separate branch, never a silent best fit. The old wording "nearest of" was a best-fit rule.
  - I dropped "touch" from the gloss of καταλάμπειν ("outshine").
- **L.2.** "Πλειάδος μῆκος ἢ ἔλασσον τῷ ἑαυτοῦ μεγέθει" was glossed "a Pleiad-length or less". The words say less by the planet's own size. Ptolemy's own reduction in the row gives 1;25° against 1;30°. Wording corrected; tolerances unchanged.
- **H.3.** The fork justification blamed the printed "day numeral". The conflict is 30 days, a whole month. Wording corrected; values unchanged and verified (see Method, step 3).
- **E.3 (notes).** The notes glossed "εὑρίσκομεν" as observed. The verb means "we find". Corrected; 3.1.9 calls the matching autumn equinox observed ("ἐτηρήσαμεν").

### F. Notes only (8 rows; with E.3, 9 notes-only rows in all)

- **E.2 and K.3.** The interval crosses eras. I recorded where the text itself states the link: 3.1.9 for E.2, and 3.7.4 and 10.9.2 for K.3. No outside chronology enters.
- **H.5, H.6, H.9, K.2, K.8, L.7.** The planet is not named in the cited row; it is named in the chapter heading:
  - 9.7.1, "τοῦ τοῦ Ἑρμοῦ ἀστέρος";
  - 9.9.1, "τῶν τοῦ τοῦ Ἑρμοῦ ἀνωμαλιῶν".

  A.7, H.4, H.8, K.1, K.7 and L.6 carry the same note alongside their other edits.

### G. Set-level fields (not clue rows)

| Set | Old description | New description |
|---|---|---|
| ALM-A | "young Moon" and "near-full Moon" stated as fact | marked as inferred phases |
| ALM-B | "waning Moon" stated as fact | marked as an inferred phase |
| ALM-C | "some 18 days later" | "civil day +17" (`span_days` is 17) |
| ALM-L | "about 1.7 years" | "about 2.7 years" (`span_days` is 996) |

ALM-L's "one observer's set" also became "one written collection", from "ἐν ταῖς παρὰ …" in all three rows.

I checked every `observer_place` word string at its ref; all are present. Alexandria is stated for:
- 9.10.3 and 11.2.2 (set A);
- all four B rows;
- the three eclipses of 4.6.13 (set C).

Every other set is correctly "unstated". The `window_width_years` field is a width only (136 years) in every set. **There are no positions.**

## Rows confirmed `ok` without edit (29)

**Intervals:** A.3, A.6, A.8, B.4, B.6, B.8, C.2, D.2, F.2, G.2, H.7, J.3, K.6, L.3, L.5. All were recomputed, and all match.

**Other rows:**
- A.4: Mars "μετὰ γ ἔγγιστα ἡμέρας τῆς γ΄ ἀκρωνύκτου". The opposition is to the mean Sun per 10.7.2, verified.
- B.3, D.4, H.2, I.2, I.3, I.5, J.2, J.5, K.5: star relations, each with `none`.
- C.3: the eclipse. "τὸ ∠ʹ καὶ γʹ τῆς διαμέτρου", from the north. The mid-time is Ptolemy's own computation, "ἐπελογισάμεθα", as the notes say. Alexandria is per 4.6.13.
- D.3: Venus "ἑσπέριος τὸ πλεῖστον ἀπέστη". A reported record ("φησιν"), with the narrator reporting.
- J.1 and K.4: "ἑῷος" for Mars and Jupiter.

## What the next stage must know

1. **Re-running the builder would undo these edits.** `results/controls-almagest/build_prereg.py` writes this file, and re-running it would silently undo every edit here. Port them into the builder, or keep the file frozen. The pre-edit copy is in `results/license-check-almagest/controls_almagest.before.json`, and `apply_edits.py` replays the edits from it.
2. **The new fork options need harness support.** `ge_after_same_apparition` and `ge_before_same_apparition` take `{"bound": "same_apparition"}`. F.4's `positional` now carries `star_candidates` and `candidate_rule`. The harness must implement both, since no grammar for them existed before.
3. **The glosses are the drafter's, not the text's. I checked them for consistency with Ptolemy's own descriptions and stated longitudes, not against an external catalogue:**
   - **Star identifications:** β Sco, δ Sco, δ Cap, β/ζ Tau, δ Cnc, α Lib, β Vir, η Vir, and F.4's candidates.
   - **Units:** 1 moon = 0.5°, 1 cubit ≈ 2°, "above" = north.
4. **The lunar-phase inferences break a stated rule.** A.10, B.2 and B.5 derive the phase class from longitudes Ptolemy states in the same sentence, while `rules_applied` says longitudes are not used. The inference is licensed by the passage and each row has `none`, so I left it.
5. **Set ALM-A uses one site for all four records.** It applies Alexandria to all four, but the site is stated for only two (9.10.3, 11.2.2). The same observer ("ἡμεῖς") makes this a reasonable inference, which the set's own `value` string flags.
6. **The `ref`s point at the withheld dates.** Every `ref` points at a row that carries the Egyptian date this file withholds. This is unavoidable when citations are required. The searcher must read only the operational fields, never the text at `ref`.
7. **Day assignment for two second records.** In I.4 and J.6 the second record's time of day is not stated. Its civil day comes from the stated four-day interval, which is consistent with the stated calendar day.
