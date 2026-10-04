# Licence check of `data/prereg/negatives.json`

**Date:** 2026-10-04

**Checker:** an independent agent. I did not draft these sets.

**What I did not open:** any truth file, `docs/research-controls.md`, or the drafter's notes (`docs/negatives-drafting.md`). I judged every row from the cited text alone.

**Result:** 70 clue rows in 13 sets. 21 rows are **edited** and 49 are **ok**. I also made three set-level edits and added one top-level block. Every row now has a `license_check` field.

## 1. Method

1. **Backup.** I copied the file before touching it, to `results/license-check-negatives/negatives.before.json`. All edits are applied from that copy by `results/license-check-negatives/apply_edits.py`, which can be re-run.
2. **String check.** `results/license-check-negatives/dump.py` splits each `licence_words` string on ` … ` and tests every fragment against the cited rows of the cited `data/text` file. It also writes each clue to `results/license-check-negatives/dump_<SET>.txt`, with the cited rows marked and 8 rows of context before and 5 after. I read every row in those dumps, together with its context, to judge three things:
   - the narrative level;
   - whether the passage is a simile or a lying tale;
   - whether each feature of the `statement` and of each fork option is licensed by the words.
3. **Where a day count rests on silence.** I searched the Greek and Latin for time words to confirm that no dawn or nightfall is narrated in the gap ("[me: search]" in the file). The cases:
   - *Arg.* 2.1285–3.744;
   - *Il.* 19.2–23.58 and 24.32–24.351;
   - Quintus 12.340–13.40 and book 14;
   - Valerius Flaccus 1.311–2.40.
4. **External justifications.** I checked every outside source cited in a fork justification against the local files:
   - Pliny, *NH* 16.39.2, 18.31.3, 28.7.3, 10.32.1 and 18.26.1;
   - Virgil, *Georgics* 1.221;
   - Aratus 783–787;
   - Hesiod, *WD* 564–567, 609–610 and 615–616;
   - the scholia-iliad keys 6.16.341.1, 6.17.183.1, 2.17.136.1, 4.18.84.1, 6.18.109.1, 2.18.196.1, 2.18.198.1 ("ἡ ἱστορία παρὰ τοῖς κυκλικοῖς"), 2.23.90.1 and 4.24.22.1;
   - *Od.* 5.51–54.

   All say what the rows claim.

**Licence strings, before and after the edits:**

| | Fragments | Exact matches | Missing refs | Refs out of text order |
|---|---|---|---|---|
| Before the edits | 201 | 201 | 0 | 0 |
| After the edits | 209 | 209 | 0 | 0 |

Many `ref` lists include the whole sentence, not only the quoted rows: 38 rows cite at least one row that carries no quoted fragment. Some details in the statements rest on those cited but unquoted rows, for example "driven back" in ARG-CIUS-05 (1.1016–1017). I treated a cited row as licence and did not edit for this.

## 2. Edits, by kind of failure

### 2.1 A simile or a lying tale inside the licence

- **AEN-CARTHAGE-01.** The licence and the statement included the simile "avi similis, quae circum litora … volat aequora iuxta" (4.254–255), which "Haud aliter" closes at 4.256.
  - I removed the simile and quoted the non-simile frame instead: Atlas at 4.246–247, the plunge at 4.252–254, and the arrival at Carthage at 4.259–261. I corrected the refs to match.
  - The god is named "Cyllenius" (4.252) and "Mercurium" (4.222).
  - No fork option used the simile, so the operational content is unchanged.
  - This matches the Odyssey's own treatment: its gull comparison (*Od.* 5.51–54) carries no date.
- **IL-PATROCLUS-09.** The licence quoted 24.413–414. Hermes speaks those lines in disguise as a Myrmidon squire, which is a lying persona.
  - I removed them from the licence and the refs and kept them in the notes as agreeing with the narrator.
  - The narrator's 24.31 alone now carries the twelfth-dawn interval.

### 2.2 A time of day that the words do not state

- **AEN-TROY-02.** Options i-a and i-b bounded the moonlight at local midnight. The words name no hour.
  - The bound is an inference from the order of events: nightfall (2.250), the fleet under way (2.254), the horse opened (2.259), then "prima quies" (2.268).
  - I spelled out that inference in both justifications and added option **i-c**: Moon up at some instant of the dark hours, any phase.
- **QS-SACK-02.** The statement said "in the evening", and option a bounded the portents before local midnight. Quintus gives no hour.
  - I reworded both to say that the timing is inferred from the order: portents (12.500–520), then the meal (13.1), then the sleep and the torch (13.21–23).
- **QS-SACK-03.** Option b timed the Pleiades "at nightfall", which nothing licenses.
  - The passage is set "Ἰλίου ὀλλυμένης" (13.551), during the sack, which begins only after the city is asleep (13.21–29).
  - Option b now spans the dark hours, with the drafter's 5° altitude.
  - New option **b-late** carries the after-midnight reading, with the inference stated.
  - The BM-analogue pinned reading still names `b`, which now means the dark-hours version.
- **IL-PATROCLUS-02.** The statement said "before noon", and solar_am required the eclipse maximum before local apparent noon.
  - 16.567 only precedes 16.777, and "ὄφρα μὲν Ἠέλιος μέσον οὐρανὸν ἀμφιβεβήκει" describes a span of time around noon, so the order does not fix the hour.
  - I reworded the statement and stated the inference in solar_am's justification.
  - I added option **solar_any** (eclipse maximum at any daylight hour) and listed it in the set's `eclipse_compatible_options`.

### 2.3 Day or year intervals presented as stated

- **AEN-CARTHAGE-07.** The statement put Dido's banquet "in the summer before Night 0" and her count "since Troy".
  - The words give only "septima … aestas": the seventh summer of his wandering, where "aestas" can also stand for a year.
  - I reworded the statement.
  - Option a's justification now spells out the chain of inference to a 6–8-year gap: the wandering began in the first summer after the fall (3.8); the departure falls in Dido's "hiberno … sidere" winter (4.309), if that is read literally; the 6–8 range is the drafter's.
  - The row notes and the set notes no longer call the interval between the two Night 0s "stated".
- **ARG-CIUS-06.** The statement gave "next day the sacrifice" as if the text said it.
  - No dawn is named between the halcyon night and the sacrifice. There is only a daylight view (1.1112–1113), which I now quote. I spelled out the inference.
  - Option n16's justification did not distinguish it from n17. I restated it: the twelve storm nights are counted from the night after the third day of mourning.
- **ARG-COLCHIS-02.** Option a3 presented one day's coasting as a count, but "ἐπιπρὸ γὰρ αἰὲν ἔτεμνον" gives none.
  - I relabelled a3 as the shortest reading.
  - I added **afree** (0–3 extra days, a bound I set as drafter) and **none** (the storm night unlinked), matching how the file treats its other uncounted intervals.
- **ARG-COLCHIS-03.** The statement's Night −3 (Medea sleepless) was not quoted, and its Day −3 rests on silence.
  - I quoted 3.744 and 3.751.
  - The statement now says that no time marker falls between 2.1285 and 3.744.
- **ARG-RETURN-03.** Option x0 assumes no stay at Carpathos, which the text does not say, and the fork had no "none".
  - I said so in the justification and added **none** (Day E unlinked).
- **VF-LEMNOS-01.** Option a, "the departure day is Day 0", ignored the storm of 1.608–656, whose darkness the text calls "nox" (1.617; "nox ista", 1.670) before daylight returns (1.655).
  - I quoted the storm and spelled out the one-day reading as an inference in both justifications.
  - I changed the set's `day0` so that Day 0 is no longer called "the first day of the voyage" outright.
- **IL-PATROCLUS-07.** "Hector dies on Day +1" had no quoted support.
  - The note now gives the basis: the dawn at 19.1, and no narrated sunset or dawn until 23.58.
  - Within that gap, only speeches and the excluded similes at 22.26–31 and 22.317–318 mention night or stars.

### 2.4 A season or site carried over without saying so

- **AEN-CARTHAGE-03.** Options a and b apply Dido's "hiberno … sidere" to Night 0. Her words date her speech and the fleet-building, on an earlier day that is not counted. Both justifications now state that transfer as an inference.
- **ARG-COLCHIS-04.** The words place the sailors who watch Helice and Orion only "ἐνὶ πόντῳ". The options were computed at the set's site, Colchis, without saying so. They are now marked as using the set's site as the drafter's stand-in.

### 2.5 Fork menus that were incomplete, duplicated or unjustified

- **AEN-ETNA-04.** The justification for "none" was just "dropped". Option c, "no phase constraint on Day +1", had the same operational content as "none", so the garden counted one path twice. I merged c into "none", which now carries c's reason.
- **ARG-COLCHIS-01.** The text names no phase of Arcturus, but the menu offered only three of its four seasonal phases.
  - I added option **d**, the evening (acronychal) rising, citing Hesiod *WD* 564–567, "ἐπιτέλλεται ἀκροκνέφαιος".
  - I marked the ±15-day widths as the drafter's.
- The new options **i-c** (AEN-TROY-02), **solar_any** (IL-PATROCLUS-02), **b-late** (QS-SACK-03) and **afree** and **none** (ARG-COLCHIS-02), and **none** (ARG-RETURN-03), are listed under 2.2 and 2.3.

### 2.6 Statement features the quoted words did not cover

- **AEN-CARTHAGE-05.** "Urges him to flee before dawn": I added 4.565 "Non fugis hinc praeceps" and 4.568 "si te his attigerit terris Aurora morantem".
- **AEN-CARTHAGE-06.** "Leaves at once": I added 4.582 "litora deseruere".
- **VF-COLCHIS-01.** The statement asserted "the late evening star", but "serus vesper" reads just as naturally as "late evening". I made the statement neutral, and "none" now gives that reading.

### 2.7 Widths that were the drafter's but not marked

- **ARG-CIUS-07.** Pliny (10.32.1) gives "circa solstitia" and no width. Option b's ±15 days is now marked as the drafter's.

### 2.8 Set-level and top-level changes

| Where | Change |
|---|---|
| VF-LEMNOS `day0` | Reworded; see VF-LEMNOS-01 |
| IL-PATROCLUS `eclipse_compatible_options` | Added `IL-PATROCLUS-02:solar_any` |
| AEN-CARTHAGE `notes` | The year link to AEN-TROY is now called inferred, not stated |
| Top-level `license_check` block | Records who checked, the report, the backup, the script, and the builder warning in §4.1 |

All pinned readings, `eclipse_compatible_options` entries and `odyssey_slots` clue_ids still resolve to existing options. I checked this with a script.

## 3. Per-row verdicts

The `license_check` text in the JSON gives the full reason for each edited row.

| Row | Verdict | Note |
|---|---|---|
| AEN-TROY-01 | ok | "ruit oceano nox" (2.250) |
| AEN-TROY-02 | edited | §2.2. The Pliny refs for *silens luna* are verified |
| AEN-TROY-03 | ok | Order only |
| AEN-TROY-04 | ok | "per lunam"; "none" is justified by 2.360/2.397, which are outside the wolf simile (2.355–358) |
| AEN-TROY-05 | ok | The new-moon fork is an analogy, with "none" |
| AEN-TROY-06 | ok | "consumpta nocte" (2.795) |
| AEN-TROY-07 | ok | Lucifer is Venus. The site rests on 2.742–748 plus 2.795. The `ida` rider is marked as drafter's geography; I recomputed its 119° bearing |
| AEN-CRETE-01 | ok | The window width is marked as the drafter's |
| AEN-CRETE-02 | ok | "plena … luna" |
| AEN-ITALY-01/02/03 | ok | "Necdum orbem medium" puts the sky survey before midnight |
| AEN-ETNA-01/02/03 | ok | "nox intempesta"; "primo … Eoo" with "none" (3.589 = 4.7) |
| AEN-ETNA-04 | edited | §2.5. Achaemenides is not a lying tale: the poem confirms his account |
| AEN-CARTHAGE-01 | edited | §2.1 |
| AEN-CARTHAGE-02 | ok | The free30 bound is marked as the drafter's, with "none" |
| AEN-CARTHAGE-03 | edited | §2.4 |
| AEN-CARTHAGE-04 | ok | "medio volvuntur sidera lapsu" |
| AEN-CARTHAGE-05/06 | edited | §2.6 |
| AEN-CARTHAGE-07 | edited | §2.3 |
| ARG-CIUS-01 | ok | A ἦμος/τῆμος time marker, not a simile |
| ARG-CIUS-02 | ok | διχόμηνις; "for supper" gives the early evening |
| ARG-CIUS-03 | ok | 1.1273 begins after the bull simile (1.1265–1272) |
| ARG-CIUS-04/05 | ok | |
| ARG-CIUS-06 | edited | §2.3 |
| ARG-CIUS-07 | edited | §2.7 |
| ARG-COLCHIS-01/02/03/04 | edited | §2.5, §2.3, §2.3, §2.4 |
| ARG-COLCHIS-05 | ok | "μέσσην νύκτα" (Medea's speech) plus the narrator's leaning Bear |
| ARG-COLCHIS-06 | ok | The drafter's late-night option is marked as such |
| ARG-COLCHIS-07 | ok | ἦμος/τῆμος time marker |
| ARG-RETURN-01/02 | ok | ἀστὴρ αὔλιος; the two-night count is stated |
| ARG-RETURN-03 | edited | §2.3 |
| ARG-RETURN-04/05 | ok | The lunar-eclipse option is marked as the drafter's |
| QS-SACK-01 | ok | |
| QS-SACK-02/03 | edited | §2.2 |
| QS-SACK-04/05/06 | ok | Day +2 or later for the storm is licensed by the sailing after the Day +2 events. The upper bound is marked as the drafter's |
| VF-LEMNOS-01 | edited | §2.3 |
| VF-LEMNOS-02…07 | ok | Tiphys' speech is character speech, not a lying tale. Georgics 1.221 and Aratus 783–787 are verified |
| VF-CYZICUS-01/02/03 | ok | "prona sidera" (3.33) justifies the late-night option |
| VF-COLCHIS-01 | edited | §2.6 |
| VF-COLCHIS-02 | ok | "lux orta" is in the main clause; the simile starts at 7.24 |
| IL-PATROCLUS-01 | ok | |
| IL-PATROCLUS-02 | edited | §2.2 |
| IL-PATROCLUS-03/04/05/06 | ok | 17.366 comes after the afternoon marker at 16.779. Scholia keys verified. The Shield is an ekphrasis, with "none" |
| IL-PATROCLUS-07 | edited | §2.3 |
| IL-PATROCLUS-08 | ok | ἦμος δ' ἑωσφόρος comes after the simile at 23.222–225 |
| IL-PATROCLUS-09 | edited | §2.1 |
| IL-PATROCLUS-10 | ok | Day H is the day of the twelfth dawn: there is no dawn between 24.31 and 24.351. "ἐπὶ κνέφας" (24.351) gives the evening |

## 4. Remarks I did not turn into edits

### 4.1 The builder will overwrite these edits

`results/negatives/build_negatives.py` writes `negatives.json`. Re-running it would silently undo these edits. I do not own that script and did not touch it.

**Before the file is frozen, someone must port `apply_edits.py` into the builder, or retire the builder.**

### 4.2 Three forks have no "none", by design

The three forks are ARG-CIUS-06, IL-PATROCLUS-09 and VF-LEMNOS-01.

- **ARG-CIUS-06 and IL-PATROCLUS-09.** The narrator states those counts ("ἤματα … τρία", "δυωδεκάτη … ἠώς"). The options are counting conventions, and the rows that depend on them, ARG-CIUS-05 and IL-PATROCLUS-10, each have their own "none".
- **VF-LEMNOS-01.** The departure day anchors no other row.

### 4.3 Many numeric thresholds are the drafter's but not marked

These are operational versions of features the words do state, so I left them alone:

| Row | Threshold |
|---|---|
| ARG-CIUS-02 a | 3 h after sunset |
| AEN-CRETE-02 a | ±1 day of opposition |
| VF-LEMNOS-02 a | illuminated fraction ≤ 0.25, for "nec gravido … cornu" |
| VF-LEMNOS-03 a | sets before midnight |
| VF-LEMNOS-03 b | ±15 days |
| VF-LEMNOS-04 | ±7 days |
| VF-LEMNOS-05 a | ±15 days |
| IL-PATROCLUS-05 a | last 2 h before sunset |
| IL-PATROCLUS-06 b | ±15 days |

Rows across the sets also use 2° and 5° altitude cuts.

### 4.4 Some "literal" pinned readings contain inferences

Some "literal" pinned readings use options that rest on inference or on the drafter's widths:

- AEN-CRETE-01 `a60`;
- ARG-RETURN-03 `x0`, now labelled as an inference;
- ARG-COLCHIS-02 `a3`.

I did not change any pins. The design owner should decide whether "literal" should mean "least inference".

### 4.5 Smaller points

- **VF-LEMNOS observer point.** The point is (40.0 N, 24.7 E), east of Athos. But 2.75–76, "primus … exegit … Phoebus Athon", suggests the Sun rose over Athos as seen from the ship, which would put the ship west of the mountain. The coordinates are already marked as the drafter's, and the shift does not matter for star phases.
- **VF-LEMNOS-06 option a.** Under VF-LEMNOS-07's 1–60-day window, a fourth-day Moon falls on some day of the stay almost always, so this option constrains almost nothing. That is not a licensing problem.
- **AEN-TROY `observer_places`.** These include Mount Ida, which is a landmark for the `ida` rider, not an observer's place. The entry labels it as such.
- **Window.** Every set carries `window_width_years` = [136, 251]: widths only, with no position.
- **Leak check.** I searched the file for dates and years (BC/AD, "Julian", four-digit negative years). Nothing in it leaks a date.
