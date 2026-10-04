# Real-record controls: the blind drafting

**Files.**
- The clue file is `data/prereg/controls_real.json`: 9 sets, 78 clue rows.
- It is built by `results/controls-real-drafting/build_controls_real.py`.
- The script looks up every quoted Greek or Latin string in the named row of the named `data/text/*.tsv` file and stops if a string is missing. Every `licence_words` entry is therefore an exact substring of the local text.
- The truth is in `data/prereg/controls_real_truth.json`. The searcher must never read that file. Only the harness may read it, to place the window.

**Freeze.** The clue file was hashed before any accepted date was looked up. The hashes are in `results/controls-real-drafting/clue_file_sha256.txt`:
- clue file SHA-256 `eb1f0401c3984c1b007f74c9bae68d9156a35662258f6d332e70c1abdbbe9256`;
- builder `69ebbadf4efb600e00c7bf6d913537f898b8d7c1c5e95b1b683a826ba3d353b3`;
- time 2026-10-04 05:19 UTC.

The clue file has not been changed since.

This note explains each set and each fork. It contains no accepted dates.

---

## 1. What the drafter had seen: the drafting was not fully blind

The task said to read issues 2 and 15 of `docs/critique-design.md` and to avoid the answers. The following reached me before drafting, and the bench owner should weigh it.

1. **Critique issue 2 (required reading) prints answers.** Its table and notes give:
   - computed local clock times of maximum for Thuc. 4.52, Xen. *Hell.* 2.3.4 and Diod. 20.5.5;
   - the umbral magnitude for Thuc. 7.50;
   - Julian dates for Livy 44.37 and Diod. 20.5.5;
   - the years of the Livy 22.1.9 and 30.38.8 identifications, with their magnitudes;
   - a Julian date and computed hour for Livy 38.36.4.
2. **DESIGN §4.1, row I2b.** Read while looking up the window convention in §3.1–§4.2; §4.3 was not opened. It lists computed local magnitudes for Thuc. 2.28 and Diod. 20.5.
3. **Background knowledge.** As a language model I know the conventionally cited years of most of these eclipses. Examples are Thucydides' first-summer eclipse, Gaugamela, Pydna, and Ptolemy's Babylonian and Hadrianic triples. A drafter with ordinary classical training would know them too.

**Mitigations, fixed before the sets were written:**
- No feature was added that the words do not state.
- Every inferred feature is a fork with a "none" option.
- The primary option follows one rule (§2), applied the same way to every set.
- Darkness thresholds come from the design's existing eclipse classes (DESIGN §3.1: X3 ≥ 0.95, X4 ≥ 0.60), or from geometry (0.5 for a crescent). None was chosen to fit a known value.

Where the rule produced a reading that I believe conflicts with an answer I had seen, I left the reading as the rule produced it. I record the conflict only in the truth file.

**Not opened:** `docs/research-controls.md`, `results/controls/`, `data/ref*/`, any NASA file, DESIGN §4.3, and every part of `critique-design.md` except issues 2 and 15. The Arrian Hekatombaion sentence (3.6.8) and other context rows were read in the local texts only.

## 2. Rules applied to every set

- **A clue is a stated feature.** An implied feature becomes a fork. Its licensing words are quoted, its inference is spelled out, and "none" is one of its options.
- **Primary option.**
  - The primary option is the reading closest to the words, with no inference from narrative order or outside knowledge.
  - Where two sources for one event disagree, the primary is the weakest reading both allow, and each source alone is an alternative. Arbela's magnitude and month and Pydna's season are the cases.
  - Where one source states a feature and the other is silent, the stated feature is primary. Pydna's totality is the case.
- **Intervals.** An interval enters only when the text states it:
  - Ptolemy's Egyptian dates and day counts;
  - Thucydides' numbered war-years;
  - Xenophon's "τῷ δʼ ἐπιόντι ἔτει" headings.

  No modern date enters.
- **Calendars.**
  - A Roman date carries a free integer offset from the proleptic Julian date of the same name. The primary option leaves it unbounded, so the date constrains nothing. A ±90-day bound and a naive offset of zero are alternatives for sensitivity.
  - The Egyptian calendar's epoch in Julian terms is not in the Almagest text, so it is a free integer (`J_free`). The wandering 365-day year makes the dates fix intervals only.
  - Attic month names need the modern reconstruction of the Athenian year (month 1 begins at the first new moon after the summer solstice). It enters with a free offset of −1, 0 or +1 lunation and a "none" option. The reconstruction is a *secondary* source, not in these texts.
- **Hours.**
  - Greek and Roman "hour n of the day (night)" is a seasonal hour: one twelfth of sunrise–sunset (sunset–sunrise).
  - A Roman *vigilia* is a quarter of the night.
  - Ptolemy's hours are equinoctial hours from local apparent midnight (LAT). He states both apparent ("ἁπλῶς") and mean ("ἀκριβῶς") intervals.
- **Magnitudes.**
  - Solar `smag` is the fraction of the Sun's diameter covered at the site.
  - Lunar `umag` is the umbral magnitude.
  - One digit is 1/12 of the lunar diameter.
- **Sites.** The text gives place names. Coordinates are my modern approximate placements, marked as such, and are search inputs, not clues. Where the text places no observer, the set says "unstated" and a `site` clue carries the forks.
- **Window.** `window_years` = 136 for every set. This is the B&M reproduction width (DESIGN §3.1) and the PC-S width (§4.2). The harness places it with the anchor event at a uniformly random position; the clue file carries no position. Events marked `linked: false` get their own window.
- **Similes and lying tales.** None of these passages contains one, so the exclusion did not bite.

---

## 3. The sets

### R-PTOL-BAB: Almagest IV.6, three Babylonian lunar eclipses (E1–E3)

**Source.** Ptolemy quotes a Babylonian record ("φησίν") for each eclipse, then reduces it with his own theory. The record and the reduction are kept apart: the record is primary, and Ptolemy's reductions are alternatives.

| clue | what the text gives | forks |
|---|---|---|
| PB-CAL | Mardokempados yr 1 Thoth 29/30; yr 2 Thoth 18/19; yr 2 Phamenoth 15/16 (4.6.3–5) | none. The nights are 29, 383, 560 on the Egyptian count, with one free `J_free` |
| PB-INT-12, -23 | Ptolemy's own day counts, 354 d 2½ h and 176 d 20½ h (4.6.6) | **calendar-exact** (354 and 177 nights, primary); **ptolemy-hours** (±1 h); **none**. Redundant with PB-CAL; use one or the other |
| PB-E1-MAG | "ἐξέλειπεν ὅλη": total | none |
| PB-E1-TIME | record: began after the rising, "an hour having well passed"; Ptolemy: mid-eclipse 2½ h before Babylon midnight | **record** (first contact 1–2 h after moonrise, primary; the upper bound is my reading of ἱκανῶς); **reduction** (−2.5 h LAT ± 1 h); **none** |
| PB-E1-SUN | Ptolemy computes the Sun at Pisces 24½° | **±5°** (primary); **±15°**; **none** |
| PB-E2-MAG | "ἀπὸ νότου δακτύλους γ": 3 digits, so umag ≈ 0.25 | **±0.10** (primary); **±0.20**; **any partial** |
| PB-E2-DIR | from the south, so the Moon is north of the shadow axis (β > 0) | **β > 0** (primary); **none** |
| PB-E2-TIME | record: 3 digits "at midnight itself"; Ptolemy: mid-eclipse at Babylon midnight | **mid within ±1 h of LAT midnight** (primary); **in progress at midnight**; **none** |
| PB-E2-SUN | Pisces 13¾° | as E1 |
| PB-E3-MAG | "πλεῖον τοῦ ἡμίσους", not "ὅλη" | **0.5 < umag < 1** (primary); **umag > 0.5**; **umag > 0.4** |
| PB-E3-DIR | from the north, so β < 0 | as E2 |
| PB-E3-TIME | record: "began after the rising"; Ptolemy: mid 3½ h before midnight, *assuming* a 3-hour eclipse | **record** (first contact after moonrise, primary); **record-soon** (within 1 h); **reduction**; **none** |
| PB-E3-SUN | Virgo 3¼° | as E1 |

**Why the solar longitudes are forks.**
- Ptolemy computed them from his tables ("κατὰ τοὺς ἐκτεθειμένους ἡμῖν ἐπιλογισμούς"); nobody observed them.
- His year is a few minutes too long (general knowledge), so a computed longitude carried back about nine centuries may be off by days. Hence ±5° for the Babylonian eclipses and ±3° for his own.
- They are still the only season information in the set, because the Egyptian dates cannot carry season once `J_free` is free.

**Observer.** Babylon, licensed by "ἐκ τῶν ἐν Βαβυλῶνι τετηρημένων". The search uses 32.54°N 44.42°E.

### R-PTOL-ALEX: Almagest IV.6, Ptolemy's three Alexandrian eclipses (H1–H3)

The same structure as the Babylonian set:
- dates: Hadrian yr 17 Payni 20/21, yr 19 Choiak 2/3, yr 20 Pharmouthi 19/20. These are nights 6130, 6662 and 7164, and the differences match Ptolemy's 4.6.16 intervals;
- magnitudes: total; 5/6 of the diameter from the north; ½ from the north;
- mid-times: −¾ h, −1 h and +4 h from Alexandria midnight;
- solar longitudes: Taurus 13¼°, Chelae 25⅙°, Pisces 14 1/12°.

Ptolemy says "ἐπελογισάμεθα" ("we computed") for the times, so the narrative level records a reduction of his own observation.

Forks:
- **time:** ±0.5 h (primary), ±1 h, none;
- **solar longitude:** ±3° (primary), ±15°, none;
- **magnitude:** ±0.10 (primary), ±0.20, any partial.

Observer: Alexandria, licensed by "ἐν Ἀλεξανδρείᾳ τετηρημένων".

### R-PTOL-CHAIN: the two triples joined by IV.7.1

**PC-LINK.** In IV.7.1 Ptolemy states the interval from E2 to H2: 854 Egyptian years and 73 days, 311,783 days in all, plus 23⅓ hours. Operationally, the night of H2 is 311,784 civil nights after the night of E2. Forks: **calendar-exact** (primary) or **none**.

**Why it is a separate set.** The link sits in the chapter after the one the task names. It is still a day count the text itself gives, so the rule admits it. A separate set lets the bench report the two triples with and without it.

**Window.** The window bounds E1 only.

### R-THUC: Thucydides 2.28 (T1), 4.52 (T2), 7.50.4 (T3)

**T1, 2.28: a solar eclipse.**
- **The words.**
  - It was in "the same summer";
  - "at the new moon by the Moon";
  - "after midday";
  - the Sun "filled out again";
  - "became crescent-shaped";
  - "some stars having appeared".
- **Forks.**
  - **T1-ECL:** the end was seen (Sun up at last contact, primary) or none.
  - **T1-TIME:** maximum after local apparent noon (primary); or first contact after noon; or none.
  - **T1-SHAPE:** the crescent was the greatest phase, 0.5 ≤ smag < 1 (primary); or a crescent passed on the way to totality (smag ≥ 0.5); or none.
  - **T1-DARK:** "some" stars only, so X4 (≥ 0.60) is primary; X3 (≥ 0.95) and none are alternatives.
  - **T1-SEASON:** Thucydides counts by summer and winter halves (5.20.3), so the primary is solar longitude 0–180° (between the equinoxes). The "campaign" option, 330–225°, lets the summer start with early spring (2.2.1 "ἅμα ἦρι ἀρχομένῳ"). None is the third option.
  - **T1-PHASE** is recorded but adds nothing, because every solar eclipse is at new moon.
  - **Site:** unstated. **T1-SITE** forks are Athens (inferred from the Athenian narrator at 1.1.1), the Aegean box (primary), and none.
- **Not used:** the narrative order after the invasion of 2.19.

**T2, 4.52: a solar eclipse.**
- **The words:** "some eclipsing of the Sun", around the new moon, right at the start of the following summer.
- **Forks.**
  - **T2-ECL:** partial (primary) or any.
  - **T2-SEASON:** **early** is primary, solar longitude 330–60°. The two-month width is mine and rests on εὐθύς. The half-year, campaign and none readings are alternatives.
  - **Site:** unstated, with the same forks as T1.
- **Not used:** the earthquake later in the same month.

**T3, 7.50.4: a lunar eclipse.**
- **The words:** at full moon, seen by the Athenians at Syracuse as they were about to sail. No magnitude and no hour are stated.
- **Forks.**
  - **T3-ECL:** umbral eclipse with the Moon up (primary); or a deep penumbral eclipse (pmag ≥ 0.7, my rough threshold).
  - **T3-SEASON:** the text does not state the season at 7.50. The eclipse lies inside the summer that runs from 7.19.1 to 8.1.4, with no winter named between, so it uses the summer forks.
  - **Site:** the Athenian camp at Syracuse ("ἐς τὰς Συρακούσας", "ἐκ τοῦ στρατοπέδου").
- **Not used:** Nicias' "τρὶς ἐννέα ἡμέρας".

**Intervals between the eclipses.**
- **T-INT-12:** year 1 ends at 2.47.1, after 2.28. Year 7 ends at 4.51.1, just before 4.52. So T2 is 7 war-years after T1.
- **T-INT-13:** year 18 ends at 7.18.4 and year 19 at 8.6.5, so T3 is 18 war-years after T1.
- **Forks for both:** ±0.5 year (primary, since both events lie in summer halves); ±1 year; none.
- Every intermediate year-end statement is in the text.

### R-XEN: Hellenica 1.6.1 (X1), 2.3.4 (X2), 4.3.10 (X3)

**X1, 1.6.1: a lunar eclipse.**
- **The words:** "the Moon was eclipsed in the evening", in the year the old temple of Athena burned.
- **The heading problem.** This sentence is one of the Hellenica's chronological headings, which modern editors suspect are interpolated. Critique issue 2 says so, citing a note I did not open. The local text prints no brackets, and I could not tell from it whether the eclipse clause belongs to the gloss. So **X1-ECL** forks into **use** (primary) and **exclude**.
- **X1-TIME:** "ἑσπέρας". The primary option needs some umbral phase between sunset and sunset + 3 h; the 3-hour width is mine. The alternatives are before midnight, or none.
- **X1-SITE:** the clause names Athens, but only for the fire. The options are the Aegean box (primary), Athens, or none.

**X2, 2.3.4: a solar eclipse.**
- **The words:** "about the time of an eclipse of the Sun". The eclipse dates Lycophron of Pherae's battle against the Larisaeans. No magnitude, no hour and no site are given.
- **X2-ECL:** any magnitude (primary); or ≥ 0.5, "noticed".
- **X2-SITE:** the Aegean box (primary); Thessaly, inferred from the Thessalian event; Athens, inferred from the surrounding narrative; or none.
- **X2-SEASON:** none (primary). The "before autumn" alternative comes from narrative order (2.3.9 "τελευτῶντος τοῦ θέρους").

**The interval, X-INT-12.**
- Three headings follow each other: 1.6.1 opens year A; 2.1.10 opens A+1, which ends at 2.2.24; 2.3.1 opens A+2.
- X2 falls "at this time" in A+2, so the gap is between 1 and 3 years (primary), or none.
- These "next year" headings belong to the same suspect apparatus.
- The war-year counts inside the headings (24 and 25) agree with consecutive years but are not used.

**X3, 4.3.10: a solar eclipse.**
- **The words:** "the Sun seemed to appear crescent-shaped", while Agesilaus was at the entry into Boeotia (4.3.9 "μέχρι πρὸς τὰ Βοιωτῶν ὅρια"). I place the observer on the Boeotian frontier near Chaeronea and Coronea, 38.5°N 22.85°E.
- **X3-ECL:** 0.5 ≤ smag < 1 (primary); or any.
- **X3-SEASON:** none (primary). The alternative, after the start of spring, rests on narrative order from 4.1.41 "σχεδὸν δὲ καὶ ἔαρ ἤδη ὑπέφαινεν".
- **No link.** No year count joins X3 to X1 or X2, so X3 is unlinked and gets its own window.

### R-ARBELA: one lunar eclipse in four sources

**Sources.** Plutarch *Alex.* 31.4; Arrian 3.7.6 (local key 3.7.5.1) and 3.15.7; Curtius 4.10.1–2; Pliny *NH* 2.180 (local key 2.70.3).

**Clues and forks.**
- **A-MAG.**
  - Arrian says "τῆς σελήνης τὸ πολύ", the greater part of the Moon. Curtius describes a blood colour fouling all its light, which reads as total.
  - The primary is umag > 0.5, which both allow.
  - The alternatives are total (Curtius), 0.5–1 (Arrian alone, "most, not all"), and none.
- **A-TIME-PLINY.**
  - At Arbela, the "second hour of the night".
  - The primary needs the umbral phase to overlap the 2nd seasonal hour at Arbela.
  - The alternatives are onset in that hour, or none.
- **A-TIME-CURTIUS.**
  - "prima fere vigilia", two days after crossing the Tigris.
  - The primary needs the umbral phase in the first quarter-night, ±1 h for *fere*; the alternative is none.
- **A-SICILY.**
  - Pliny adds that the same eclipse was seen in Sicily as the Moon rose.
  - The primary is moonrise somewhere in Sicily during the umbral phase. The alternatives are moonrise at Syracuse, or none: Pliny's sentence illustrates longitude and may be a computed example.
- **A-MONTH.**
  - Plutarch puts the eclipse in Boedromion, near the start of the Mysteries. Arrian puts the battle in Pyanepsion, "in the same month" as the eclipse.
  - The primary is the union of Attic months 3 and 4, offset ±1 lunation. Each month alone, or none, are the alternatives.

**Not used.**
- Arrian's archon year, which needs a modern archon list.
- Plutarch's "eleventh night", which dates the battle, not the sky.
- Arrian's Hekatombaion at Thapsacus (3.6.8), which only orders events.

**Observers.**
- Arbela, from Pliny ("apud Arbilam"), at 36.19°N 44.01°E.
- The camp just over the Tigris, from Arrian and Curtius. The crossing point is not known; I placed it at 36.5°N 43.0°E ± 0.5°.
- Sicily, from Pliny.

### R-PYDNA: Livy 44.36–37 and Plutarch *Aem.* 16–17

| clue | what the text gives | forks |
|---|---|---|
| P-MAG | Plutarch: light gone, colours changing, the Moon "ἠφανίσθη"; Livy is silent | **total** (primary); **≥ 0.8**; **any umbral** |
| P-TIME | Gallus forecast "ab hora secunda usque ad quartam horam noctis" (44.37.5), and it came "edita hora" (44.37.8). This is a character's forecast that the narrator confirms. Plutarch: after nightfall and dinner | **overlap** with seasonal night hours 2–4 (primary); **within** (the whole umbral phase inside hours 2–4); **none** |
| P-ALT | Plutarch: "πλήρης οὖσα καὶ μετέωρος" | **altitude ≥ 10° at first umbral contact** (primary; the 10° is mine); **above the horizon**; **none** |
| P-END | both sources say the emergence was seen | **Moon up at last umbral contact** (primary); **none** |
| P-SEASON | Livy 44.36.1, "Tempus anni post circumactum solstitium erat", said of that very day; Plutarch 16.9, "θέρους γὰρ ἦν ὥρα φθίνοντος" | **solar longitude 90–180°** (union, primary); **Livy alone, 90–120°**; **Plutarch alone, 120–180°**; **none** |
| P-DATE | "nocte, quam pridie nonas Septembres insecuta est dies": the evening of Roman 3 September | **free offset** (primary); **±90 d**; **naive** (sensitivity) |

**A correction to the critique.** Critique issue 2 says the earlier draft's "summer" for this set came from the Julian answer. The text does carry a season: 44.36.1, one chapter before the eclipse sentence, plus Plutarch 16.9.

**Observer.** The camps before Pydna: "πρὸ τῆς Πύδνης" (16.5), and Livy's survivors who fled "Pydnam ex acie" (44.42.7). The search uses 40.37°N 22.60°E.

### R-DIOD: Diodorus 20.5.5

**The words.** On the day after Agathocles' fleet slipped out of Syracuse at nightfall, the Sun was eclipsed so far that it seemed fully night, with stars seen everywhere.

**Forks.**
- **D-ECL:** **X3, ≥ 0.95** is primary, because ancient accounts do not separate total from near-total darkness. **Total** and **X4** are alternatives.
- **D-SITE:** **day-out** is primary: within 150 km of Syracuse, one day's rowing. The distance is mine, and the course is not given. **Syracuse** and the **route box** from Sicily to Africa are alternatives (20.6.1 gives six days and nights to Libya).

**Deliberately absent.** The text gives no hour and no season, so the set has none.

**Not used.** Diodorus' count from the fall of Troy (20.2.3), because no second dated sky event is in the set.

### H-LIVY: the prodigy notices, a hard case reported but not pass/fail

| event | the words | site | forks |
|---|---|---|---|
| L1, 22.1.9 | "solis orbem minui visum", in a list "ex pluribus simul locis" | not named for the item | **magnitude:** any (primary), ≥ 0.5. **Site:** Italy–Sicily–Sardinia box (primary); Sardinia (the grammatical reading: "in Sardinia autem" governs the items up to "Praeneste"); Rome (where the report was made); none. **Date:** none (primary). The alternative puts the eclipse within 12 months before the report, made on the Ides of March as "iam ver adpetebat" |
| L1b, 22.1.9 | at Arpi, "pugnantemque cum luna solem" | Arpi | **not an eclipse** (primary); or an eclipse seen at Arpi |
| L2, 30.38.8 | "Cumis solis orbis minui visus" | Cumae (stated) | **magnitude:** any (primary), ≥ 0.5. **Date:** none (primary). The alternative puts it before that year's Ludi Apollinares, by narrative order |
| L3, 37.4.4 | Roman date a.d. V Id. Quint.; at the Ludi Apollinares; clear sky; daylight darkened because "luna sub orbem solis subisset" | Rome, inferred from the games and "ab urbe est profectus" | **magnitude:** X4 (primary), any, X3. **Date:** free Roman offset (primary), ±90 d, naive. **Site:** Rome (primary), Italy box, none |
| L4, 38.36.4 | "luce inter horam tertiam ferme et quartam tenebrae obortae": the text does not say eclipse | Rome, inferred from "in omnibus compitis" and "in Aventino" | **cause:** an eclipse ≥ 0.60 with its maximum in seasonal day hours 3–4 ± 1 h (primary); an eclipse at any hour; or not an eclipse (undatable). **Date:** none (primary). The alternative puts the darkness within 120 days before the Roman Ides of March |

**No textual year interval joins these notices.**
- Livy does state war-years elsewhere: 23.30.17, 24.9.7, 27.22.1, 28.10.8, 28.38.12 and 30.44.2 ("finitum est septimo decimo anno").
- They reach the prodigy passages only by counting consular years, which Livy does not state as a number at these passages.
- I did not enter such links. My own counting would also have been exposed to the years in critique issue 2.

Each notice is therefore searched alone. The point of the hard case is to show how often such a notice is unique.

---

## 4. Left out on purpose

| item | why |
|---|---|
| Archon, ephor, consul and Olympiad names (Thuc. 2.2.1, Xen. *Hell.* 1.6.1 and 2.3.1, Arr. 3.15.7, Diod. 20.3.1) | need modern lists to become dates |
| Thuc. 4.52 earthquake; Nicias' 27 days; Plutarch's eleventh night; Curtius' two days in camp | not sky events, or they date the battle rather than the sky |
| Narrative-order seasons (Thuc. 2.28 after 2.19; Xen. 2.3.4 and 4.3.10; Livy 30.38) | alternatives only, never primary |
| Ptolemy's night lengths (12 h, 11 h) | follow from his computed solar longitudes; noted, not separate clues |
| Pliny *NH* 2.180's second eclipse (the solar eclipse of the consuls Vipstanus and Fonteius, Campania hours 7–8 and Armenia hours 10–11) | not in the task. It is a good further control: two sites with hours, and a Roman date under the Julian calendar |

## 5. Things the bench owner should know

1. **Text artefacts in the local files.**
   - The Ptolemy file prints Heiberg's half-sign as the literal string `U+2220` (648 times). The licence words quote it as it stands, and the notes explain it.
   - Curtius 4.10.1 has the OCR slip "stafiva".
   - Arrian's eclipse sentence sits in local row 3.7.5.1, not 3.7.6.
   - Pliny *NH* 2.180 is local key 2.70.3.
2. **A new field, `operational`.** It holds machine-readable parameters, but the vocabulary (`smag`, `umag`, `seasonal_night_hours`, `site_box`, `offset_days`, `delta_nights` …) is not yet read by any code. The searcher module will need to implement it or translate it.
3. **Six readings are mine, not the text's.**
   - the upper bound of ἱκανῶς (2 h);
   - εὐθύς as two months;
   - ἑσπέρα as 3 h;
   - μετέωρος as ≥ 10°;
   - one day's rowing as 150 km;
   - a deep penumbral eclipse as pmag ≥ 0.7.

   Each has a looser alternative or a "none" beside it.
4. **Post-freeze check.** After the hash was taken, I looked up the accepted dates and checked them against the primary options with `results/controls-real-drafting/check_truth.py`; its output is `check_truth.out`. Both files sit on the truth side: like the truth file, keep them away from the searcher. The truth file records:
   - which primary options the accepted dates fail, and why;
   - what I would have written differently had I known the answers;
   - which three choices may have been steered by what I had seen beforehand.

   The bench owner should read that section before freezing.
5. **Outcome expectations.** The Ptolemy sets carry exact day intervals and three magnitudes and times each, so they should be close to unique in any window. The single-eclipse sets (R-DIOD, X3, and every H-LIVY event) are expected to be weak. That is the intended spread.
