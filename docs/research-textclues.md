# Odyssey text clues: an inventory for odybench

Every astronomical, calendrical, lunar, seasonal, weather and time-of-day clue in the Odyssey, classified against the Baikouzis & Magnasco (B&M) reading.

Written 2026-10-03 for `C:\Projects\odybench`. The scripts that produced every count and computed number in this document are in `docs/textclues-scripts/` (see §9).

---

## 0. Conventions

**Dates.** Every date is given as a historical year with the astronomical year in brackets. All dates use the proleptic Julian calendar. B&M's candidate Day 0, the slaughter of the suitors, is **16 April 1178 BC (−1177)**.

**Times.** The times I computed are **local mean time (LMT)** at Ithaca (38.4° N, 20.7° E):

- LMT = UT + 1 h 22.8 min.
- UT = TT − ΔT, with ΔT = 27,603 s. This is the value B&M took from Starry Night [B&M §Method]. B&M's SI notes that the Five Millennium Canon gives 28,590 s [B&M SI Fig. S1].
- The ΔT uncertainty is 2–4° of longitude [B&M SI Fig. S1], which shifts local times by about ±8–16 min.

B&M's own times are "local to the Greek islands" [B&M §Method]. They do not say whether this is mean or apparent time.

**Provenance tags.**

| Tag | Meaning |
|---|---|
| [Od. x.y] | Greek text in `data/text/odyssey-grc.tsv` (Perseus). Line numbers are Perseus's. |
| [Il. x.y], [Hes. WD/Th], [h.Ap / h.Herm / h.Dem] | Local TSVs: Iliad, Hesiod and the Homeric Hymns, exported read-only from the ClassicaCodex library. |
| [schol. Od. x.y (sigla) key] | Dindorf's Odyssey scholia, `data/text/scholia-odyssey-grc.tsv`. The key format is vol.book.section.entry. Manuscript sigla are as printed. |
| [B&M §…] | The paper: PNAS 105:8823–8828, PMC2440358. I read the full text. |
| [B&M SI …] | The Supporting Information. I read it from the local copy `data/bm2008-a/baikouzis-magnasco-2008-SI.pdf`, which a sibling agent fetched from the Wayback Machine. |
| [computed: script] | Computed by me with the named script in `docs/textclues-scripts/`. |
| [inference] | My reasoning, not a source's claim. |
| [secondary, not read] | Known only from a report or abstract. |

**Narrative levels.**

| Code | Level |
|---|---|
| **P** | Primary narrator |
| **C** | A character's speech in the story's present |
| **E** | A character's true embedded narrative of past events: the Apologue (books 9–12), Eumaeus' autobiography (book 15) |
| **L** | Odysseus' lying tales (13.256ff, 14.192–359, 14.462–506, 19.165–202, 24.244ff) |
| **O** | An oath, prophecy or vision about the future |
| **S** | A simile, which sits inside the level of its frame |

**Classification** (the task's four classes):

- **A**: used by B&M, either as a search constraint or as explicit support (paper or SI).
- **B**: unused, but compatible with a mid-April Day 0 at new moon.
- **C**: unused and in tension with it.
- **D**: uninformative or formulaic.

For class A clues, the "Compat." column also gives my own assessment.

**B&M's day numbers** [B&M Table 1] are given as *sequential / parallel*. Under B&M's solution the sequential days map to proleptic Julian dates in 1178 BC (−1177) as follows:

| B&M day | Date (1178 BC) | Event |
|---|---|---|
| −34 | 13 Mar | Hermes at Ogygia |
| −29 | 18 Mar | Departure from Ogygia |
| −11 | 5 Apr | Raft sunk |
| −9 | 7 Apr | Lands on Scheria |
| −7 | 9 Apr | Games; the Apologue told |
| −5 | 11 Apr | Arrival on Ithaca |
| −3 | 13 Apr | Eumaeus' tale |
| −1 | 15 Apr | Odysseus goes to the palace |
| 0 | 16 Apr | The slaughter |
| +1 | 17 Apr | Laertes |

---

## 1. Key findings

1. **Most of the astronomy B&M used is inherited formula.**
   - Od. 5.273–275 are **verbatim Il. 18.487–489**, the star catalogue on the Shield of Achilles [computed: formula.py].
   - The Shield line just before them (Il. 18.486, Pleiades/Hyades/Orion) is **the same verse as Hes. WD 615**, with case and dialect changed.
   - The one non-repeated star line, 5.272, adds Boötes with the epithet ὀψὲ δύοντα. This phrase occurs nowhere else of a star in the corpus searched (Iliad, Odyssey, Hesiod, five Homeric Hymns). In Il. 21.232 it describes evening.
   - Ancient commentators glossed the epithet as a *permanent* property: Boötes sets slowly, going down upright with four zodiacal signs [schol. Od. 5.272 (E; E.H.P.Q.V), citing Aratus 581–582]. Aratus 579–585 ties the "late setting" to the nights when Boötes begins to set at sunset, which in that period is an autumn configuration [inference].
   - B&M's seasonal reading ("visible all night in March") is therefore one interpretation of one epithet, not a clear statement in the text.
2. **The morning star at 13.93–95 is a traditional time-marker.** Its structure ("when the dawn-announcing star goes up, then X") is the same as **Il. 23.226–228** (Heosphoros at the end of Patroclus' pyre-night). Its line-end "ὅς τε μάλιστα" plus an enjambed verb repeats Il. 5.5–6 (Sirius) [computed: formula.py]. The only ancient scholion on the line glosses the verb. It does not identify the star [schol. Od. 13.93 (Q) 2.13.2.64].
3. **Nothing in Hermes' journey (5.43–56) points to the planet Mercury.**
   - Lines 5.43–49 are **7 lines verbatim from Il. 24.339–345**. Lines 5.44–46 recur for Athena at Od. 1.96–98, and 5.47–48 for Hermes at Od. 24.3–4.
   - The rest is a divine-journey type-scene (a stop at Pieria as in Il. 14.225–226; a god compared to a seabird).
   - The passage has no light, star, west, rising, setting or turning vocabulary. "Went away" at 5.148 has no direction.
   - The ancients flagged the block as recycled: lines "improperly transferred" [schol. Od. 5.43 (H.P.Q.)], and they athetized 5.54 [schol. 5.54 (H.P.Q.)].
   - Hermes appears again at 24.1–14, leading the suitors' souls past "the gates of the Sun". B&M's Hermes=Mercury rule is not applied there.
4. **The lykabas couplet is a reused oath-slot, and its meaning was disputed in antiquity.**
   - 14.161–162 = 19.306–307 verbatim. The surrounding oath ("Let Zeus be witness … the hearth of Odysseus to which I come") recurs at 17.155–156 and 20.230–231 with different time-slots.
   - An ancient critic said a line in book 14 had been transferred from book 19 [schol. 14.159 (Q)]. Another suspected three lines as inconsistent and implausible [schol. 14.162 (H)].
   - Every ancient lexicographer glosses λυκάβας as "year" (scholia; Herodian; Suda; Artemidorus; all post-Homeric poets in the library) [computed: library search]. Dio Chrysostom read "this month" (Or. 7.84–85).
   - Murray's Loeb, which B&M quote in the SI, renders the **same Greek** as "day" at 14.161 and "month" at 19.306 [B&M SI Table S1; data/text/odyssey-murray.tsv].
   - The second line ("as the month wanes and the next begins") was read as the ἕνη καὶ νέα, the conjunction day, by Plutarch (*Solon* 25.3) and by the scholia ("the 30th and noumenia, i.e. the ἕνη καὶ νέα"). Plutarch (*De facie* 19) and Heraclitus (*Homeric Problems* 75) then tied it to an eclipse. So the "new-moon" reading is ancient, but it is exegesis.
5. **The text never calls Apollo's festival a new-moon festival.**
   - The text says "a feast for all" (20.156), "the god's holy feast" (21.258–259), the grove of Apollo (20.278) and a sacrifice to Apollo (21.267).
   - The new-moon link is a scholion citing Philochorus (Apollo "Neomenios") [schol. Od. 20.155 (V)]. Hesiod makes the **7th** day Apollo's (WD 770–771). Sparta sacrificed to Apollo at every new moon **and** on the 7th (Hdt. 6.57.2).
   - A Greek νουμηνία (first crescent) is normally the day **after** the conjunction. A solar eclipse falls **on** the conjunction, the ἕνη καὶ νέα (Plut. *Solon* 25.3). This mismatch is my inference [inference].
6. **σκοτομήνιος (14.457) occurs only here in the corpus searched**, and B&M misdate it.
   - The scholia gloss it as "moonless", or as the night "in which the moon is darkened at conjunction" [schol. 14.457 (V; P)].
   - B&M call it "Night −2" [B&M §Method]. Their own Table 1 puts xiii.93–xiv.533 on Day −5 (sequential) / −4 (parallel).
   - Under B&M's solution that night (11/12 April 1178 BC) had a waning crescent about 24% lit, rising about 03:48 LMT. The night was moonless for about 8 hours [computed: moon.py].
   - The clue is compatible, but it is not independent of the new-moon assumption, and it is weak: any night within about ±4–5 days of conjunction would qualify [inference].
7. **The season is split.**
   - The weather of the primary narrative points to a cool, wet season: rain and a strong wet westerly (14.457–458), morning frost feared (17.25; 5.467), fires "for light and warmth", cloaks.
   - Characters twice call the nights very long (11.373; 15.392). Under B&M's dates those nights were about 11.3–11.5 h, *shorter* than the days [computed: nightlength.py].
   - **The ancient scholia read the season as autumn heading into winter**: [schol. 11.373 (H.T.)], [schol. 17.24 (H)], [schol. 17.191 (V)], [schol. 14.458 (B.Q.)], and for Phaeacia [schol. 6.305 (B, H)].
   - Spring appears **only in similes and hypotheticals**: the nightingale "at spring newly begun" (19.519, a hemistich shared with Hes. WD 569); swallows (21.411, 22.240); the gadfly "in spring when days lengthen" (22.301 = 18.367, a stock line); snowmelt (19.205–207).
   - B&M's supports for spring are a lying-tale detail (the "much-flowering wood", 14.353) and two statements the Greek does not make:
     - "the year was drawing to a close" (1.16 says only that the destined year came round);
     - "xi.370 The nights are still at their longest" [B&M SI Table S1]. The Greek of 11.373 says "**this** night is very long". Murray, the translation B&M quote elsewhere, renders it that way.
8. **B&M's paraphrases add things the Greek does not have.** In each of the following cases a modelling assumption entered as if it were text:
   - departure from Ogygia "at sunset" (5.263–269 gives no hour);
   - Hermes going "back east" (5.148 has no direction);
   - a "noontime meal" (20.390 says δεῖπνον, with no hour; the poem has a noon formula at 4.400 = Il. 8.68, which is not used here);
   - Apollo as "a solar deity" (in Homer, Helios is a separate god: Od. 8.302, 12.374–388);
   - "Night −2";
   - "15 March" for Hermes' day [B&M SI Table S1 note] against 13 March in the main text;
   - the departure as the "previous full moon" [B&M SI *Metonic Cycles*] against "That night is New Moon" in the main text.
9. **What the text can date** (my inference; see §7). The text gives:
   - a relative timeline, ±1 day depending on sequential or parallel reckoning, partly built from formulaic numerals;
   - one month-turn statement inside a prophetic oath;
   - an ambiguous season.

   It contains no planetary statement except a generic morning star. On its own the text cannot pick a year.

---

## 2. What B&M used: the inputs as stated

### 2.1 Search constraints

| B&M input | Lines B&M cite | Constraint as stated | Day | B&M result for 1178 BC (−1177) |
|---|---|---|---|---|
| New Moon on Day 0 | 14.161, 19.306, 14.457. Day 0 is also the Apollo festival day [B&M §Method; SI Table S1] | Search only the 1,684 new moons in 1250–1115 BC | 0 | 16 Apr |
| Pleiades and "late-setting" Boötes | 5.270–277 | At nautical twilight on T−29, and on every night of the 17-day sail, both visible: T−29 between 17 Feb and 4 Apr | −29 | 18 Mar; Pleiades astern, Boötes ahead-left at nautical twilight 7:38 pm (Fig. 2) |
| Venus as morning star | 13.93–96 | Venus rises ≥ 90 min before the Sun (true "≈1/3 of the time") | −5 | Rose 1 h 43 min before dawn, magnitude −4.2, on 11 Apr |
| Hermes = Mercury (B&M call it "conjectural") | 5.48ff, 5.55, 5.97–103; SI also quotes 5.225 | Mercury within a few days of its westernmost rising azimuth | −34 | Westernmost azimuth 12–13 Mar; heliacal rising 13 Mar |
| Poseidon's return = equinox (listed, not applied) | 5.282 (and 1.22ff) | 1 Apr ≤ T−11 ≤ 5 Apr | −11 | Equinox 1 Apr 3:24 pm; raft sunk 5 Apr |

B&M state that only one date in the 135 years satisfies all the criteria, and that the joint match happens "only one day every 2,000 years" [B&M §Intersecting].

My equinox computation gives 1 April 1178 BC (−1177) at about 14:27 LMT [computed: nightlength.py], within about an hour of B&M's value. My conjunction is 16 April at about 11:45 LMT [computed: moon.py]. B&M's Fig. 1 gives the eclipse at 12:02 pm local time. These agreements validate my low-precision ephemeris for this purpose.

### 2.2 Supporting remarks (not constraints)

These come from [B&M §References, §Historical Plausibility, SI]:

- The "much-blossoming" wood at 14.353.
- "Numerous references to the nights being long, fires, and coats".
- "At the opening of the poem, it is said that the year was drawing to a close".
- Hesiod (WD 560–563) as evidence that the year ended at the vernal equinox. This reading of WD 561–562 is contested, and the lines are about rationing [inference].
- Murray's Metonic reading of the 20 years and of Day 0.
- In the SI only, as allegories: 360 boars (14.20); Penelope's web as the Moon; the bow as the crescent; the spreading of sails as another first-crescent allegory.
- Ares is absent from the story, and Mars is invisible except at the eclipse.

### 2.3 Internal inconsistencies in B&M that matter for the text

The bench should not inherit these. Each was checked against the Greek and against B&M's own Table 1.

| B&M statement | Problem |
|---|---|
| "Night −2 is dark and moonless (xiv.457)" [B&M §Method] | Their Table 1 puts xiii.93–xiv.533 on Day −5 (sequential) / −4 (parallel). 14.457 is the night of the arrival day. |
| SI Table S1: "v.225 … this was March 15, the day of Hermes visit" | The main text says T−34 = 13 March |
| SI: the departure was the "previous full moon" | The main text says "That night is New Moon" on 18 March. My computation agrees: about 1% lit [computed: moon.py]. |
| "Stringing his bow" on T is a "first crescent" allegory [B&M §Intersecting] | On the eclipse day there is no crescent. Conjunction is at about 11:45 LMT on 16 April [computed: moon.py]. A first crescent needs about 1–2 days after conjunction [inference]. |
| SI "xi.370: The nights are still at their longest" | The Greek (11.373) says "this night is very long, immense". Murray renders it that way. The ancient scholion inferred autumn from it [schol. 11.373 (H.T.)]. At B&M's date (9 Apr) the night was about 11.5 h, shorter than the day [computed: nightlength.py]. |
| "The year was drawing to a close" (opening of the poem) | 1.16 says only that the year destined for his return came round, "as years revolved". This is a formula shared with Hes. Th. 184 and h.Dem. 265 [computed: formula.py]. |
| Departure "at sunset" (Day −29) | 5.263–272 gives no hour. Night-sailing follows simply because he steers through the nights [inference]. |
| Hermes "travels back east" | 5.148: "went away", with no direction |
| Suitors "sitting down for their noontime meal" | 20.390: δεῖπνον, with no hour. The slaughter is in daylight before the δόρπον (21.428–429). |
| Apollo, "a solar deity" | In Homer, Helios is a separate god (Od. 8.302; 12.374–388). The equation of Apollo with the Sun is post-Homeric. |
| 14.161 "this self-same day" and 19.306 "this very month" (Murray, quoted in the SI) | The Greek is identical: τοῦδ' αὐτοῦ λυκάβαντος |

---

## 3. The internal timeline (text anchors)

The day boundaries are marked by dawn and sunset formulas. "ἦμος δ' ἠριγένεια φάνη ῥοδοδάκτυλος Ἠώς" occurs 20 times in the Odyssey and 2 in the Iliad; "δύσετό τ' ἠέλιος σκιόωντό τε πᾶσαι ἀγυιαί" occurs 9 times [computed: occurrences.py].

| B&M day (seq/par) | Julian date, 1178 BC (−1177), seq. | Text anchors | Clues on that day |
|---|---|---|---|
| −34/−33 | 13 Mar | 5.1 (dawn), 5.28–148 (Hermes), 5.225 (sunset) | Hermes (5.43–56) |
| −33…−30 | 14–17 Mar | 5.228 (dawn), 5.262 "the fourth day" | — |
| −29/−28 | 18 Mar | 5.263 "on the fifth" (no hour stated) | Stars (5.270–277) |
| −28…−12 | 19 Mar–4 Apr | 5.278 "seventeen days" | — |
| −11/−10 | 5 Apr | 5.279 "on the eighteenth", 5.282 | Poseidon (5.282) |
| −10, −9 | 6–7 Apr | 5.388–390 "two nights, two days … the third day" | Frost fear (5.467) |
| −8/−7 | 8 Apr | 6.48 (dawn) | Arete at the hearth (6.305) |
| −7/−6 | 9 Apr | 8.1 (dawn) | "Very long night" (11.373) |
| −6/−5 | 10 Apr | 13.18 (dawn), 13.33–35 (sunset departure) | — |
| −5/−4 | 11 Apr | 13.93–95 (morning star), 14.457 (night) | Morning star; oath (14.161); σκοτομήνιος |
| −4/−4 | 12 Apr | 15.56 (dawn at Sparta) | — |
| −3/−3 | 13 Apr | 15.189 (dawn), 15.296 (sunset); 15.392 at the hut | "Endless nights" |
| −2/−2 | 14 Apr | 15.495 (dawn), 16.452 (evening) | — |
| −1/−1 | 15 Apr | 17.1 (dawn), 17.25, 17.191, 19.306, 19.519 | Frost; oath; nightingale |
| 0/0 | 16 Apr | 20.91 (dawn) … 21.428–429 ("supper in daylight") | Festival; vision; similes |
| +1 | 17 Apr | 23.347 (dawn) | Laertes digging (24.227) |

Notes on the timeline:

- The 20-day voyage is stated twice: Zeus, "on the twentieth day" (5.34), and Odysseus, "yesterday, on the twentieth day" (6.170). The day count is internally consistent.
- The numerals are typological:
  - "ἑπτὰ δὲ καὶ δέκα … ὀκτωκαιδεκάτῃ" (17, then the 18th) recurs for Achilles' funeral (Od. 24.63–65).
  - The n/(n+1) pattern "ἐννῆμαρ … δεκάτῃ" (9, then the 10th) occurs 14 times in Iliad, Odyssey and h.Dem [computed: occurrences.py].
  - "τρίτον ἦμαρ ἐυπλόκαμος τέλεσ' Ἠώς" is a three-time formula (5.390 = 9.76 = 10.144).
- Day counts are relative evidence built from stock numbers. That is a forking-path issue for any absolute fit [inference].
- There is an unnarrated day at Eumaeus' hut between the night of 14.457 and the evening of 15.301, under either reckoning [inference from the text sequence above].

---

## 4. Master inventory

Columns:

- **Cat.**: astr = astronomical, lun = lunar, cal = calendrical, seas = seasonal, met = meteorological, tod = time of day, dc = day count.
- **B&M**: whether B&M used the clue.
- **Compat.**: compatibility with Day 0 = conjunction on 16 April 1178 BC (−1177).
- **Parallels**: verbatim or near-verbatim repeats found by `formula.py` / `occurrences.py` in the Iliad, the Odyssey, Hesiod (WD, Th, Sc) and the Homeric Hymns (Dem, Ap, Herm, 31, 32). "= " means verbatim. "≈ " means a shared run of ≥ 4 words, or the same verse with a different case or dialect form.
- **Scholia**: Dindorf.
- **Lvl**: the narrative level codes from §0.

| # | Lines | Greek (short) | Gist | Cat. | B&M | Compat. | Parallels | Scholia | Lvl | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 1.16–17 | ἔτος ἦλθε περιπλομένων ἐνιαυτῶν | The destined year came round | cal | A (support: "year drawing to a close") | **D** — no season in the Greek | line-end = Hes. Th. 184, h.Dem. 265; cf. Od. 11.248, Hes. WD 386 | (H) "revolving, being completed" 1.1.4.24 | P | B&M's paraphrase is unsupported |
| 2 | 1.22–25; 5.282–283 | Αἰθίοπας … δυσομένου Ὑπερίονος οἱ δ' ἀνιόντος; ἐξ Αἰθιόπων ἀνιών | Poseidon among the Ethiopians of sunset and sunrise; on his return he sees the raft | astr? | A (listed, not applied: equinox, after MacDonald 1967) | Conjectural. Fits B&M's dates by construction (equinox 1 Apr, sinking 5 Apr). | — | 1.22 (E): Poseidon = water, Nile flood "at a set time"; 1.23 (M): Aristarchus places him among the *eastern* Ethiopians; 5.282 (P.Q.) likewise | P | The ancient allegory is hydrological, not equinoctial |
| 3 | 5.1–2 | Ἠὼς δ' ἐκ λεχέων παρ' ἀγαυοῦ Τιθωνοῖο | Dawn of Hermes' day | tod | A (day count) | D | = Il. 11.1–2; 5.2 ≈ Il. 19.2 | — | P | — |
| 4 | 5.43–49 | οὐδ' ἀπίθησε διάκτορος ἀργεϊφόντης … ἐδήσατο καλὰ πέδιλα … εἵλετο δὲ ῥάβδον | Hermes ties on his sandals, takes his wand, flies | (planet?) | A (conjectural Mercury) | No text clue. B&M compute Mercury's heliacal rising for 13 Mar. | **= Il. 24.339–345 (7 lines)**; 5.44–46 = Od. 1.96–98 (Athena); 5.47–48 = Od. 24.3–4 | 5.43 (H.P.Q.): the lines were "improperly transferred" to Od. 1.96 and Il. 24.339; 5.45 (B), 5.47 (E.V; H.P.Q.T): the wand = λόγος (allegory) | P | Divine-departure type-scene |
| 5 | 5.50–56 | Πιερίην δ' ἐπιβὰς … λάρῳ ὄρνιθι ἐοικώς … ἐκ πόντου βὰς ἰοειδέος | Via Pieria; skims the waves like a gull; steps out of the violet sea onto the far island | (planet?) | A (low flight = Mercury near the horizon; "climbs out of dark waters" = first morning visibility) | No astronomical vocabulary at all | Pieria stop ≈ Il. 14.225–226 (Hera); god compared to a bird: Od. 5.337, 22.240, Il. 24.80 | 5.51 (V; P): like the bird "in impulse, not form"; **5.54 (H.P.Q.): line added improperly (athetesis)**; 5.55 (P.Q.): the island is far off in remote places | P | — |
| 6 | 5.97–104; 5.148 | τίς δ' ἂν ἑκὼν τοσσόνδε διαδράμοι ἁλμυρὸν ὕδωρ; ἀπέβη | Hermes complains of the long sea trip; then "went away" | (planet?) | A ("protestation", "travels back east") | 5.148 gives no direction | ὣς ἄρα φωνήσας ἀπέβη is stock | 5.100 (B.E.P.Q.T): Calypso's island lies outside "our" sea | C, P | "Back east" is B&M's inference |
| 7 | 5.121–124 | ὅτ' Ὠρίων' ἕλετο ῥοδοδάκτυλος Ἠώς | Dawn carried off Orion; Artemis killed him at Ortygia | astr-myth | — | D | — | 5.121 (P.Q.T; E; V): Orion myths (Euphorion); 5.124 (H.P.Q.): some athetize | C (Calypso) | — |
| 8 | 5.225, 5.228 | ἠέλιος δ' ἄρ' ἔδυ καὶ ἐπὶ κνέφας ἦλθεν | Sunset on Hermes' day; dawn next | tod | A (SI: "March 15") | D | stock sunset/dawn lines | — | P | The SI date conflicts with the main text (13 Mar) |
| 9 | 5.262–263 | τέτρατον ἦμαρ … τῷ δ' ἄρα πέμπτῳ | Raft finished on the 4th day; sent off on the 5th | dc | A | Consistent | τέτρατον ἦμαρ ἔην also at 3.180 | — | P | **No hour of departure given** |
| 10 | 5.268–269 | οὖρον … ἀπήμονά τε λιαρόν τε; πέτασ' ἱστία | A gentle, warm divine wind; he spreads sail | met | A (SI: "first crescent" allegory, said to be at the "previous full moon") | D | 5.268 = 7.266 | — | P | The SI's "full moon" contradicts the paper |
| 11 | 5.270–272 | Πληιάδας τ' ἐσορῶντι καὶ ὀψὲ δύοντα Βοώτην | Steering all night, watching the Pleiades and late-setting Boötes | astr | **A** (Pleiades and Boötes visible at nautical twilight on T−29 and throughout the 17 days) | **Depends on interpretation** (see §5.8). B&M's reading works for March. The ancient "slow-setting" reading is not seasonal; the Aratean link points to autumn evenings. | Line unique; ὀψὲ δύ- elsewhere only Il. 21.232 (of evening); first word echoes Il. 18.486 ≈ Hes. WD 615 | 5.272 (E): Homer knew the stars, cites Il. 18.486; Boötes "slow-setting" because it goes down upright with 4 signs; (E.H.P.Q.V): "setting long after those that rose with it", quoting Aratus 581–582; (B.V): "then oxen are unyoked"; (P.Q.): visible at evening when oxen are freed | P | Habitual description of the whole 17-day voyage, not of one night |
| 12 | 5.273–275 | Ἄρκτον θ', ἣν καὶ ἄμαξαν … οἴη δ' ἄμμορός ἐστι λοετρῶν Ὠκεανοῖο | The Bear circles, watches Orion, and alone never bathes in Ocean | astr | A (implicit: the Bear never sets) | Not date-diagnostic: circumpolar for centuries | **= Il. 18.487–489 (Shield of Achilles), verbatim 3 lines** | 5.273 (P): "in the Iliad too he says the same of the Bear"; 5.275 (P.Q.): Ocean's baths explained | P | Aristotle, *Poetics* 25 (1461a20–21): "alone" is a metaphor for "best known". The line is not an observation. |
| 13 | 5.276–277 | ἐπ' ἀριστερὰ χειρὸς ἔχοντα | Keep the Bear on the left hand | nav | A (sailing east) | D for date | ἐπ' ἀριστερὰ χειρός: h.Herm. 153, 418, 499 | 5.277 (H): carried eastward from the Atlantic | C (reported) | Directional only |
| 14 | 5.278–281; 7.267–268 | ἑπτὰ δὲ καὶ δέκα … ὀκτωκαιδεκάτῃ | 17 days of sailing; on the 18th the mountains of Phaeacia appear | dc | A | Consistent | **Same numeral pair at Od. 24.63–65** (Achilles' funeral); the n/(n+1) pattern is common (ἐννῆμαρ … δεκάτῃ ×14) | 5.280 (P.Q.): ὅθι = "when" (Aristarchus) | P; C | Typological numeral |
| 15 | 5.34; 6.170 | ἤματί κ' εἰκοστῷ; χθιζὸς ἐεικοστῷ … ἤματι | Reach Scheria on the 20th day; "yesterday, the 20th day" | dc | A (implicit in "exactly 20 days at sea") | Consistent | — | — | O (Zeus); C | Fixes the voyage length internally |
| 16 | 5.291–296; 5.385 | ὀρώρει δ' οὐρανόθεν νύξ; Εὖρος, Νότος, Ζέφυρος, Βορέης | Poseidon's storm, all four winds; Athena raises Boreas | met (divine) | A (the sinking day; Hesiod's gales at the Pleiades' setting) | D | 5.294 = 9.69 = 12.315 | — | P | Divine machinery |
| 17 | 5.328 | ὡς δ' ὅτ' ὀπωρινὸς Βορέης φορέῃσιν ἀκάνθας | As the late-summer north wind drives thistle-down | seas (simile) | — | D. If anything autumnal. | ≈ Il. 21.346 (ὡς δ' ὅτ' ὀπωρινὸς Βορέης) | — | S in P | Similes carry no date |
| 18 | 5.388–390 | δύω νύκτας δύο τ' ἤματα; τρίτον ἦμαρ … τέλεσ' Ἠώς | Two nights and two days adrift; calm on the third day | dc | A | Consistent | 5.388 ≈ 9.74; 5.390 = 9.76 = 10.144 | — | P | Formulaic |
| 19 | 5.466–473 | στίβη τε κακὴ καὶ θῆλυς ἐέρση … αὔρη … ψυχρὴ … ἠῶθι πρό | He fears hoarfrost, dew and the cold dawn breeze off the river | met | — | **C (weak)**: frost at sea level on 7 Apr is unusual; it is a fear, not an event | στίβη only here and at 17.25 | 5.466 (B.P.Q.): cannot sleep "because of the cold"; 5.467 (B.T; E; P.Q.; V): στίβη = morning cold, hoarfrost | C (deliberation) | Day −9 |
| 20 | 5.482–485 | φύλλων … χύσις … ὥρῃ χειμερίῃ | A leaf-heap big enough to shelter 2–3 men "in winter-time" | seas (generic) | — | D | — | — | P | Counterfactual measure, not a season |
| 21 | 6.305; 7.153 | ἐπ' ἐσχάρῃ ἐν πυρὸς αὐγῇ | Arete sits at the hearth in the firelight; Odysseus sits by the fire | seas (implied) | — | **C (weak; ancient reading)** | — | **6.305 (B): "this shows the season, that it was winter"; (H) "as if it were winter"; 7.153 (T): critics asked why Arete warms herself as in winter** | P; C | The hearth also served for light and cult |
| 22 | 7.112–121 | χείματος οὐδὲ θέρευς … Ζεφυρίη πνείουσα | Alcinous' orchard fruits all year round | seas (marvel) | — | D | — | — | P | Fairyland |
| 23 | 9.142–145 | οὐδὲ σελήνη οὐρανόθεν προὔφαινε, κατείχετο δὲ νεφέεσσιν | The Moon hidden by clouds on landing at Goat Island | lun | — | D (Apologue, years earlier) | — | 9.144 (H): ἀήρ = mist | E | The poet makes darkness from clouds, not from lunar phase |
| 24 | 10.82–86 | ἐγγὺς γὰρ νυκτός τε καὶ ἤματός εἰσι κέλευθοι | Laestrygonians: the paths of night and day are close | astr-geo | — | D | cf. h.Herm. 482 | 10.86 (H.Q.; H.V.): **Crates: short northern summer nights** near the head of Draco (citing Aratus); others read it as pastures | E | Ancient astronomical exegesis exists |
| 25 | 10.467–470; 2.107; 19.152–153; 24.142–143; 11.294–295; 14.293–294 | ἐνιαυτὸς ἔην, περὶ δ' ἔτραπον ὧραι / μηνῶν φθινόντων | "When the year was done and the seasons turned, as the months waned …" | cal | — | D | 10.469–470 ≈ **Hes. Th. 58–59**; 11.294–295 = 14.293–294 = **h.Ap. 349–350**; 2.107 = 19.152 = 24.142 | 10.469 (B.Q.): the seasons passed, spring, summer and so on | E; C; L | **"μηνῶν φθινόντων" is stock time-passing diction**; relevant to how φθίνοντος μηνός at 14.162 is read |
| 26 | 11.14–19 | οὐδέ ποτ' αὐτοὺς ἠέλιος … καταδέρκεται | The Cimmerians never see the Sun | astr-geo | — | D | 11.17–18 ≈ 12.380–381 | — | E | — |
| 27 | 11.373 | νὺξ δ' ἥδε μάλα μακρή, ἀθέσφατος | "This night is very long, immense" (Alcinous) | seas | A (SI renders it "The nights are still at their longest") | **C (weak)**: at B&M Day −7 (9 Apr 1178 BC) the night was ≈11.5 h, shorter than the day [computed] | — | **(H.T.): "from this too the season appears to be autumn"** | C | B&M's English overstates the Greek |
| 28 | 12.3–4 | Ἠοῦς … οἰκία καὶ χοροί … ἀντολαὶ Ἠελίοιο | Aiaia, home of Dawn and the Sun's risings | astr-geo | — | D | — | — | E | — |
| 29 | 12.62–65 | πέλειαι … ἀμβροσίην … ἀλλ' ἄλλην ἐνίησι πατήρ | Doves bring ambrosia; one is lost each time and Zeus adds another | astr (allegory) | — | D | — | 12.62 (H.Q.; H.Q.V.): read "physically" as the Pleiades, one of the seven made invisible | E (Circe) | The lost-Pleiad motif |
| 30 | 12.127–131 | ἑπτὰ βοῶν ἀγέλαι … πεντήκοντα δ' ἕκαστα | Helios' 7×50 cattle and sheep, never more and never fewer | cal (allegory) | — | D | — | **12.129 (Q. Vind.56): Aristotle — the 350 days of the lunar year**; 12.128 (B): the days | E | Ancient calendrical allegory |
| 31 | 12.312; 14.483 | τρίχα νυκτὸς ἔην, μετὰ δ' ἄστρα βεβήκει | A third of the night left; the stars had moved on | tod | — | D | **12.312 = 14.483 (7 words)**; cf. Il. 10.251–253 | 12.312 (B.Q.; V): "the third part of the night" | E; **L** | 14.483 is inside a lying tale |
| 32 | 12.380–383 | δύσομαι εἰς Ἀίδαο καὶ ἐν νεκύεσσι φαείνω | Helios threatens to go down to Hades and shine among the dead | solar motif | — | D | 12.380–381 ≈ 11.17–18 | 12.383 (H): grammar | E (reported speech of gods) | **Shows "the Sun leaving the sky" as a mythic motif in the same poem** |
| 33 | 13.33–35, 13.78–80 | κατέδυ φάος ἠελίοιο | Leaves Scheria at sunset; sails all night | tod | A (T−6) | Consistent | stock | — | P | — |
| 34 | **13.93–95** | εὖτ' ἀστὴρ ὑπερέσχε φαάντατος, ὅς τε μάλιστα / ἔρχεται ἀγγέλλων φάος Ἠοῦς | When the brightest star rose, the one that comes announcing Dawn's light, the ship drew near the island | astr | **A** (Venus rises ≥ 90 min before the Sun on T−5) | B&M: 1 h 43 min on 11 Apr (not checked here) | **Same device as Il. 23.226–228** (ἦμος δ' ἑωσφόρος εἶσι φόως ἐρέων … τῆμος …); "ὅς τε μάλιστα" at line end + enjambed verb = **Il. 5.5–6** (Sirius); superlatives for Venus and Sirius: Il. 22.318, 22.30; Eosphoros, child of Erigeneia: Hes. Th. 381; φαάντατος only here in the corpus searched | 13.93 (Q): "until it rose above". **No identification of the star**; schol. 2.1 cites Il. 23.226–227 for dawn following Heosphoros | P | A traditional "last hour of night" marker |
| 35 | 13.244–245 | αἰεὶ δ' ὄμβρος ἔχει τεθαλυῖά τ' ἐέρση | Ithaca always has rain and rich dew | climate | — | D | — | (V): dew makes plants thrive | C (Athena) | Habitual |
| 36 | 14.13–20 | τριηκόσιοί τε καὶ ἑξήκοντα | 360 boars | cal (allegory) | A (SI only: solar allegory, "one dies every day") | D | — | — | P | Allegory, not a constraint |
| 37 | **14.158–164 = 19.303–307** | τοῦδ' αὐτοῦ λυκάβαντος ἐλεύσεται ἐνθάδ' Ὀδυσσεύς, / τοῦ μὲν φθίνοντος μηνός, τοῦ δ' ἱσταμένοιο | "Within this very λυκάβας Odysseus will come, as one month wanes and the next begins" | lun / cal | **A** (Day 0 = new moon) | **Compatible** if read as the conjunction day. Alternative readings in §5.1. | **14.161–162 = 19.306–307**; the oath frame 14.158–160 ≈ 17.155–156 ≈ 19.303–305 ≈ 20.230–231; vocabulary = Hes. WD 798 (φθίνοντός θ' ἱσταμένου τε), WD 780 | **14.159 (Q): the line was transferred from book 19 (he is not yet at Odysseus' hearth)**; 14.161 (Q): λυκάβας = "year", from wolves crossing a river nose to tail; (H.Q.V.) "going darkly"; **14.162 (Q.V. Vind.133): "to the 30th and the noumenia, i.e. the ἕνη καὶ νέα"**; **14.162 (H): three lines suspected as inconsistent and implausible**; 19.306 (B): "year", four etymologies | **O** (oath of the disguised Odysseus) | Murray translates λυκάβας as "day" in 14 and "month" in 19. Plut. *Solon* 25.3: Solon named the conjunction day after this Homeric line. |
| 38 | 14.353 | δρίος ἦν πολυανθέος ὕλης | A thicket of much-flowering wood | seas | A (support) | B (weak): spring flowering | πολυανθής only here in the corpus searched | (Q): δρίος = wooded, shady place | **L** | Inside the lie it is a present-day detail: he escaped off Ithaca "in the evening" (14.344) |
| 39 | 14.384 | ἢ ἐς θέρος ἢ ἐς ὀπώρην | An Aetolian once claimed Odysseus would come "by summer or by autumn" | seas | — | D | — | (V; H): ὀπώρη = late summer or autumn | E (Eumaeus' recollection) | A past false prophecy |
| 40 | **14.457–458** | νὺξ δ' ἄρ' ἐπῆλθε κακὴ σκοτομήνιος, ὗε δ' ἄρα Ζεὺς / πάννυχος, αὐτὰρ ἄη Ζέφυρος μέγας αἰὲν ἔφυδρος | A bad, moonless night; rain all night; a strong, ever-wet west wind | **lun** + met | **A** (lunar part; B&M call it "Night −2") | **B**: night of 11/12 Apr 1178 BC: crescent ≈24% lit, rises ≈03:48 LMT, so ≈8 h moonless [computed]. Rain plus westerly is plausible in spring. | "νὺξ δ' ἄρ' ἐπῆλθε κακὴ" + epithet = 14.475 (the lying tale); ὗε δ' ἄρα Ζεύς = Il. 12.25; **σκοτομήνιος a hapax** | **14.457 (V): "moonless, dark; or the night in which the moon is darkened at conjunction with the sun"; (P): "when there is no moon"; 14.458 (B.Q.): Zephyr is rainy "not always, but in winter"** | P | B&M's "Night −2" is wrong by their own Table 1 |
| 41 | 14.475–477, 483 | νὺξ δ' ἄρ' ἐπῆλθε κακὴ Βορέαο πεσόντος, πηγυλίς … χιών … κρύσταλλος | At Troy: a bitter north wind, frost, snow like rime, ice on the shields | met | — | **D** (lying tale set about 20 years earlier at Troy) | 14.475 shares a formula with 14.457; 14.483 = 12.312 | 14.476 (B.Q.; V; B.H.Q.): πηγυλίς = frosty; snow → rime → ice | **L** | Told on the rainy night to get a cloak (14.459–461) |
| 42 | 14.518–533 | χλαῖναν … ἕννυσθαι ὅτε τις χειμὼν ἔκπαγλος ὄροιτο; ἀλεξάνεμον; Βορέω ὑπ' ἰωγῇ | Bed by the fire, fleeces, a spare thick cloak "for a terrible storm"; Eumaeus sleeps outside in a windproof cloak, under a rock sheltered from Boreas | met | (B&M: "fires, coats" generically) | B: a cool, wet night fits April | — | 14.521 (B.H.Q.): a spare cloak "if it storms"; 14.529: ἀλεξάνεμον = protection from cold and wind; 14.533: shelter from Boreas | P | Here χειμών = storm |
| 43 | 15.392–394 | αἵδε δὲ νύκτες ἀθέσφατοι | "These nights are endless: there is time to sleep and time to hear tales" (Eumaeus) | seas | A (generic "long nights") | **C (weak)**: Day −3 night ≈11.3 h, shorter than the day [computed] | cf. 11.373 | — | C | Rhetorical |
| 44 | 15.403–404 | Ὀρτυγίης καθύπερθεν, ὅθι τροπαὶ ἠελίοιο | Syrie, "above Ortygia, where the turnings of the Sun are" | astr-geo | — | D | τροπαί/τροπὰς ἠελίοιο = solstice in Hes. WD 564, 663 | **15.404 (Q.V.): a cave of the Sun where the solstices are marked; (B.H.Q.): "towards the Sun's turnings, i.e. west, above Delos" (Aristarchus, Herodian)** | E (Eumaeus' life story) | Diog. Laert. 1.119: a heliotropion was preserved on Syros (Pherecydes) |
| 45 | 15.495; 16.2 | Ἠὼς ἦλθεν ἐΰθρονος; ἄριστον ἅμ' ἠοῖ, κηαμένω πῦρ | Dawn; breakfast at dawn after lighting a fire | tod, met | A (day count) | B (weak) | Ἠὼς ἦλθεν ἐΰθρονος = 6.48 | — | P | — |
| 46 | 17.23–25 | ἐπεί κε πυρὸς θερέω ἀλέη τε γένηται … μή με δαμάσσῃ στίβη ὑπηοίη | Let me warm myself at the fire and wait for the sun's heat; the morning frost could overcome me in these rags | met | — | **C (weak)**: hoarfrost on Ithaca near sea level in mid-April is unusual | στίβη only here and at 5.467 | 17.23 (Q.V.P.): ἀλέη = the sun's warmth; **17.24 (H): "from this too the season appears autumnal, already toward winter"**; 17.25 (V): morning frost | C (partly a pretext) | Morning of Day −1 (15 Apr) |
| 47 | 17.190–191 | ποτὶ ἕσπερα ῥίγιον ἔσται | The day is far gone; it will soon be colder towards evening | met, tod | — | B | — | 17.190 (B.Q.): midday is past; **17.191 (V): "towards evening it is more wintry"** | C | — |
| 48 | 17.297–299 | κόπρῳ … τέμενος μέγα κοπρήσοντες | A dung heap waiting to manure the estate | agr | — | D | — | — | P | The manuring season is not fixed |
| 49 | 18.358–359 | αἱμασιάς τε λέγων καὶ δένδρεα μακρὰ φυτεύων | Eurymachus' offer of work: building walls, planting trees | agr | — | D | ≈ 24.224 | — | C (hypothetical) | — |
| 50 | 18.366–375; 22.299–301 | ὥρῃ ἐν εἰαρινῇ, ὅτε τ' ἤματα μακρὰ πέλονται | A mowing contest "in spring when days grow long" (hypothetical); the gadfly stings cattle "in spring" (simile) | seas | — | D | **18.367 = 22.301**; ὥρῃ ἐν εἰαρινῇ … = Il. 2.471, 16.643 | **18.367 (Q): ancient critics asked why spring days are called long — some said "spring" stands for "summer"; the answer is that πέλονται means "become" long; (B) the same** | C (hypothetical); S | Stock phrase |
| 51 | 18.307–311; 19.63–64; 19.506–507 | φόως ἔμεν ἠδὲ θέρεσθαι; ἀσσοτέρω πυρὸς … θερσόμενος | Braziers and wood "for light and warmth"; Odysseus draws his stool nearer the fire to get warm | met | A (generic "fires") | B (weak): cool April evenings | — | 19.64 (H): "for light and warmth" | P | Night of Day −1 |
| 52 | 19.172–179 | Μίνως ἐννέωρος βασίλευε | Minos ruled "nine-yearly" as Zeus' confidant | cal | — | D | ἐννέωρος also at Od. 10.19, 10.390, 11.311, Il. 18.351 | 19.179 (B; V): every nine years Minos met Zeus to learn the laws (several versions) | L (the Crete description) | Often taken as the octaeteris; no date |
| 53 | 19.186–202 | (Boreas detains him 12 days at Amnisos) | — | met | — | D | — | — | L | — |
| 54 | 19.204–209 | ὡς δὲ χιὼν κατατήκετ' … ἥν τ' Εὖρος κατέτηξεν | Penelope's tears like mountain snow melted by the east wind | seas (simile: thaw) | — | D. Thematically "spring" (Levaniouk). | — | — | S in P | — |
| 55 | **19.515–523** | χλωρηῒς ἀηδών … καλὸν ἀείδῃσιν ἔαρος νέον ἱσταμένοιο | Like the nightingale singing at "spring newly begun" | seas (simile) | — | **B (weak) / D**: in Hesiod the hemistich marks the swallow's arrival about 60 days after the winter solstice (late Feb–early Mar); mid-April is still spring | **hemistich = Hes. WD 569** | **19.518 (V): χλωρηΐς — seen among green things, "for it appears in spring"** | S in C (Penelope) | Says nothing about the current date |
| 56 | 19.571–581 | ἥδε δὴ ἠὼς εἶσι δυσώνυμος | Tomorrow's dawn will be ill-named: the contest | tod | — | D | — | — | C | — |
| 57 | 20.88–91 | αὐτίκα δὲ χρυσόθρονος ἤλυθεν Ἠώς | Dawn of Day 0 | tod | A | D | = 10.541, 12.142, 15.56 | — | P | — |
| 58 | 20.98–121 | ἐβρόντησεν … ὑψόθεν ἐκ νεφέων; ἀπ' οὐρανοῦ ἀστερόεντος, οὐδέ ποθι νέφος ἐστί | Zeus thunders; the mill-woman: "you thundered from the starry sky, yet there is no cloud anywhere" | met, sky | — | **B**: clear pre-dawn sky. The Moon is not visible: 16 Apr ≈0.3% lit, rising ≈05:36 LMT with the Sun [computed] | οὐρανὸν ἀστερόεντα is stock (8×) | **20.104 (V; B.Q.): how can she say there is no cloud? Answer: "from where clouds usually are", or the golden clouds of Olympus**; 20.113 (V): she speaks by common belief | P; C | The only sky-state report for Day 0 |
| 59 | **20.155–156** | ἀλλὰ μάλ' ἦρι νέονται, ἐπεὶ καὶ πᾶσιν ἑορτή | The suitors will come very early, for it is a feast for everyone | cal (festival) | **A** | The text names no moon phase (§5.3) | ἑορτή occurs only here and at 21.258 in the corpus searched | **20.155 (V): the new moon belongs to all the gods; this day is Apollo's ("first light"), and he was called Neomenios; "the story is in Philochorus"; (V): the poet sets the day as a feast and noumenia sacred to Apollo so Odysseus can attack while men are busy at the festival** | C (Eurycleia) | P.Oxy. 53.3710 [secondary, not read]: Aristonicus said "it was the new moon then" |
| 60 | 20.276–278 | κήρυκες δ' ἀνὰ ἄστυ θεῶν ἱερὴν ἑκατόμβην / ἦγον … ἄλσος ὕπο σκιερὸν ἑκατηβόλου Ἀπόλλωνος | Heralds lead a holy hecatomb through the town; the Achaeans gather in Apollo's shady grove | cal (festival) | **A** | — | 20.276 ≈ Il. 3.245 (κήρυκες δ' ἀνὰ ἄστυ θεῶν φέρον ὅρκια) | **20.276 (B): public heralds of the Ithacans; the poet wants to show the feast is Apollo's** | P | — |
| 61 | **20.345–357** | ἠέλιος δὲ / οὐρανοῦ ἐξαπόλωλε, κακὴ δ' ἐπιδέδρομεν ἀχλύς | Theoclymenus' vision: heads wrapped in night, blood, ghosts going to Erebus, "the Sun has perished from heaven", an evil mist has spread over all | (eclipse claim) | Target (B&M exclude it from the evidence) | n/a | Diction of death: ἀχλύς at death in Il. 5.696, 16.344, 20.421 and **Od. 22.88**; νὺξ ἐκάλυψε ×7 in the Iliad; ὑπὸ ζόφον at Od. 11.57, 11.155; **verse-end template "δ' ἐπιδέδρομεν + noun" = Od. 6.45 (λευκὴ δ' ἐπιδέδρομεν αἴγλη, over Olympus)**; ἐξαπόλωλε at Il. 18.290; darkness over battle at Il. 17.366–368, 16.567; Helios' threat at Od. 12.383 | **20.356 (B): "there was no eclipse of the sun; Theoclymenus, inspired, foresees the sun failing for them; the suitors see nothing and want him thrown out"; (V): not that an eclipse happened, but the sun had failed for the suitors** | **O** (vision) | Heraclitus, *Homeric Problems* 75 and Plut. *De facie* 19 read it as an eclipse at the month-turn, citing 14.162. 6.45 shows ἐπιδέδρομεν means "has spread over", not B&M's "attacking suddenly". |
| 62 | 20.390–394 | δεῖπνον … δόρπου δ' οὐκ ἄν πως ἀχαρίστερον | The pleasant meal now, the grim supper to come | tod | A ("noontime meal") | B (noon is not stated) | — | 20.390 (B): grammar | P | The poem has a noon formula (4.400 = Il. 8.68). It is absent here. |
| 63 | 21.176–185 | πῦρ κῆον … στέατος … θάλποντες | A fire is lit and tallow warmed to soften the bow | tech | — | D | — | — | C; P | Technique, not weather |
| 64 | **21.257–268** | ἑορτὴ τοῖο θεοῖο ἁγνή; Ἀπόλλωνι κλυτοτόξῳ | "It is the god's holy feast", so the contest is postponed; sacrifice to Apollo the archer tomorrow | cal (festival) | **A** | As row 59 | — | **21.258 (V): "the god of the bow"** | C (Antinous) | Apollo is identified only by context |
| 65 | 21.406–411 | ἡ δ' ὑπὸ καλὸν ἄεισε, χελιδόνι εἰκέλη αὐδήν | The bowstring sang like a swallow | seas (simile) | (SI: the bow = crescent) | D / B: swallows are spring birds (Hes. WD 568–569) | — | — | S in P | Borthwick 1988 [secondary, abstract only]: the swallow as a symbol of return |
| 66 | 21.428–430 | νῦν δ' ὥρη καὶ δόρπον … τετυκέσθαι / ἐν φάει | Now it is time to make the suitors' supper "in the light" | tod | — | B: the killing is in daylight | — | — | C (sardonic) | — |
| 67 | 22.7 | πόρῃ δέ μοι εὖχος Ἀπόλλων | Prays that Apollo grant him glory | festival | — | D | — | — | C | — |
| 68 | 22.239–240 | χελιδόνι εἰκέλη ἄντην | Athena perches on the smoky roof-beam like a swallow | seas (simile) | — | D | — | 22.240 (H.Q.): not a real transformation (compare Hermes "like a bird", 5.51) | S in P | Levaniouk: the spring theme |
| 69 | 23.241–246 | νύκτα μὲν ἐν περάτῃ δολιχὴν σχέθεν | Athena holds the long night back and stops Dawn's horses, Lampos and Phaethon | tod (divine) | — | D | — | **23.243 (V): long "not in general, but on that occasion"** | P | A god-made long night |
| 70 | 24.1–14 | Ἑρμείας … παρ' Ἠελίοιο πύλας | Hermes leads the suitors' souls past Ocean, Leucas and the gates of the Sun | (planet?) | — | D. A problem for any Hermes=Mercury rule. | 24.3–4 = 5.47–48 | 24.11 (V; H) | P | B&M do not treat this second Hermes journey (night of Day 0/+1) |
| 71 | 24.226–231, 242 | λιστρεύοντα φυτόν; κνημῖδας … χειρῖδας … αἰγείην κυνέην | Laertes digging round a plant in leather leggings, gloves and a goatskin cap | agr | — | B (weak): digging round vines is a spring task before the snail climbs (Hes. WD 570–572), but it is also year-round work | — | 24.227 (Q.V.): scraping and digging round, for watering | P | Day +1 (17 Apr) |
| 72 | 24.336–344 | ὁππότε δὴ Διὸς ὧραι ἐπιβρίσειαν ὕπερθεν | The vines ripen at various times as the seasons of Zeus weigh down | seas (habitual) | — | D | — | — | C | — |
| 73 | 2.175; 16.206; 17.327; 19.484; 21.208; 23.102; 23.170; 24.322 | ἤλυθον εἰκοστῷ ἔτεϊ ἐς πατρίδα γαῖαν | Came home in the 20th year | cal | A (Murray's Metonic idea, mentioned but not a criterion) | D | 4 verbatim lines plus variants (10 occurrences of "twentieth") | — | various | The "20th year" need not be 19 full years |
| 74 | Dawn and dusk formulas (all books) | ἦμος δ' ἠριγένεια φάνη ῥοδοδάκτυλος Ἠώς; δύσετό τ' ἠέλιος …; Ἠὼς δ' ἐκ λεχέων … | Day boundaries | tod | A (they build the day count) | D | 20× Od / 2× Il; 9×; Od. 5.1 = Il. 11.1 | 2.1 (no sigla printed): the dawn epithets distinguished, citing Il. 23.226–227 for Dawn after Heosphoros | P | Relative counting only |
| 75 | 4.400; 9.56–58 | ἦμος δ' ἠέλιος μέσον οὐρανὸν ἀμφιβεβήκῃ; μετενίσσετο βουλυτόνδε | Noon; ox-unyoking time (afternoon) | tod | — | D | 4.400 ≈ Il. 8.68, 16.777; 9.58 ≈ Il. 16.779 | — | E; C | The tradition had a noon formula, unused at 20.345ff |
| 76 | 3.1–8 | Ἠέλιος δ' ἀνόρουσε … ἱερὰ ῥέζον … ἐνοσίχθονι | Sunrise; the Pylians sacrificing bulls to Poseidon on the shore | tod, festival | — | D | 3.1–3 stock sunrise | — | P | Another festival (Day 3), with no calendar statement |

Counts [computed: by hand from the table above]. There are 76 rows.

- **A (used or cited by B&M, including the day-count anchors):** 35 rows — 1–6, 8–16, 18, 27, 33, 34, 36–38, 40, 42, 43, 45, 51, 57, 59, 60, 62, 64, 65 (SI only), 73 and 74. Row 61 is the hypothesis under test.
- **B (unused, compatible):** 6 rows — 47, 55 (weak), 58, 65 (the swallow, weak), 66 and 71 (weak). Six rows that B&M used (38, 40, 42, 45, 51, 62) also get "B" as my own compatibility verdict.
- **C (in tension):** 3 unused rows — 19, 21 and 46 — plus 2 rows B&M cited only generically or in mistranslation, 27 and 43. To these add the scholia's autumn-winter reading of the season (§5.6).
- **D (uninformative or formulaic):** the remaining 30 or so rows.

---

## 5. Notes on the required items

### 5.1 The lykabas lines (14.161–162 = 19.306–307) and what λυκάβας means

**Text.** The disguised Odysseus swears a formal oath. Its frame (14.158–160 ≈ 19.303–305) is the oath-scene also used by Theoclymenus (17.155–156) and Odysseus (20.230–231). Its content slot differs each time:

- 17.157: "Odysseus is already in his fatherland";
- 20.232: "while you are here Odysseus will come home";
- 14.161–162 and 19.306–307: the λυκάβας couplet.

[Od. as cited; computed: formula.py]. The couplet is a variant fill of a repeated type-scene. It is not a free-standing calendrical notice [inference].

**Ancient critics on the book-14 instance.**

- One scholion says line 159 was "transferred from" the speech to Penelope, because Odysseus "has not yet come to Odysseus' house": the "hearth to which I come" fits book 19, not Eumaeus' hut [schol. 14.159 (Q) 2.14.2.90].
- Another reports that "the three [lines] are suspected" as inconsistent with what precedes them and as implausible: "how could he know …?" [schol. 14.162 (H) 2.14.2.95]. I infer the three are most likely 161–163.
- LSJ notes "perh. day, if Od.14.161–2 are spurious" [LSJ s.v. λυκάβας, via Perseus].

**Meaning of λυκάβας.**

- **Ancient grammar uniformly glosses it as "year".**
  - Scholia [14.161 (Q; H.Q.V.); 19.306 (B)]. Etymologies: wolves crossing a river nose to tail, as day follows day; λύγη "darkness" + αὔω "shine"; "going darkly/secretly".
  - Herodian, who says it "signifies the year".
  - Suda Λ 793: ἐνιαυτός.
  - Artemidorus 2.12.
  - Aelian *NA* 10.26 and Aristophanes of Byzantium's *Epitome*, which tie it to wolves and to the Sun or Apollo.
  - Julian, *Hymn to King Helios*.
  - Bekker's *Anecdota* (via LSJ): an Arcadian word for "year".
  - Every post-Homeric poetic use found in the library is "year": Apollonius Rhodius 1.198, 1.610; Bion fr. 15; Oppian; Quintus; Nonnus (λυκάβαντα δυωδεκάμηνον); Tryphiodorus; the Greek Anthology [computed: library search, 77 matching nodes].
  - These later poets probably *derive* the sense from Homer, so they are not independent [inference].
- **"Month"**: Dio Chrysostom, *Oration* 7.84–85, paraphrases Penelope's promise as "if he would come within that month" (ἐκείνου τοῦ μηνός) [dio-chrysostom-grc.tsv 7.85]. LSJ cites this too.
- **"Day"**: Murray's Loeb at 14.161 ("this self-same day"), but "this very month" at 19.306 for identical Greek [data/text/odyssey-murray.tsv]. B&M's SI quotes both renderings [B&M SI Table S1]. Autenrieth derives the word from λυκ- "light" + βαίνω [Perseus, Autenrieth].
- **"The dark of the moon"**: Norman Austin, *Archery at the Dark of the Moon* (1975) [secondary, not read]. A search summary attributes to Austin the view that λυκάβας is the interlunar period, when the feast of Apollo falls; I could not verify it in the book.

**The second line, τοῦ μὲν φθίνοντος μηνός, τοῦ δ' ἱσταμένοιο.** The vocabulary is Hesiod's calendrical vocabulary: "the waning and the waxing [month]" (WD 798), "of the waxing month" (WD 780). In Odyssean formula, "μηνῶν φθινόντων" (10.470, 19.153, 24.143 ≈ Hes. Th. 59) means "as months passed". There are three readings:

- **(a)** The single **conjunction day, ἕνη καὶ νέα**. This is how Plutarch read it: Solon named the day on which the Moon overtakes the Sun the "old-and-new" day, "being the first, it seems, to understand Homer correctly", and called the following day noumenia (*Solon* 25.3). The scholion agrees: "the 30th and noumenia, i.e. the ἕνη καὶ νέα" [schol. 14.162 (Q.V. Vind.133)]. So do Heraclitus (*Homeric Problems* 75: the eclipse falls at τριακάς καὶ νουμηνία, "as one can learn from Homer himself") and Plutarch *De facie* 19 (931D–E), both of which join the couplet to Theoclymenus' vision.
- **(b)** The **noumenia** (first crescent), the day *after* the conjunction (Plutarch's own distinction).
- **(c)** A **window** of time-within genitives: "late in this month or early in the next". In Attic usage μηνὸς φθίνοντος and ἱσταμένου name the last and first decades of the month, so this is a window of up to about 20 days [inference].

**Consequences for the bench.** B&M took reading (a) and set it equal to Day 0. Reading (b) moves Day 0 by +1 to +2 days relative to the conjunction, which is incompatible with an eclipse on Day 0. Reading (c) is satisfied by about two-thirds of all days. The day on which the prophecy is to come true is not stated to be the slaughter day: "will come" could be the arrival, the revelation or the vengeance [inference].

The oath is spoken on B&M Day −5 (book 14) and Day −1 (book 19). Under (a), both utterances predict the same day 5 and 1 days ahead, which is consistent [inference].

**Classification**: A (used). Compatible under (a) only. The line is formulaic as an oath-slot, and its book-14 instance was doubted by ancient critics.

### 5.2 The σκοτομήνιος night (14.457)

**Text.** σκοτομήνιος occurs only here in the corpus searched (Iliad, Odyssey, Hesiod, five Homeric Hymns) [computed: occurrences.py]. The scholia give two glosses [schol. 14.457 (V; P) 2.14.2.238]:

- "moonless, dark";
- "the night in which the Moon has been darkened by its conjunction with the Sun" (μήνη = σελήνη).

The rest of the line is formulaic. "νὺξ δ' ἄρ' ἐπῆλθε κακή" + epithet recurs at 14.475, in the lying tale, where the epithet slot is filled with "Βορέαο πεσόντος". "ὗε δ' ἄρα Ζεύς" also appears at Il. 12.25.

**Day.** By B&M's Table 1 this is the night of Day −5 (sequential) / −4 (parallel), **not** "Night −2" as their text says.

**Computed lunar circumstances**, assuming B&M's Day 0 = 16 April 1178 BC (−1177) [computed: moon.py, truncated Meeus ch. 47 lunar theory, ΔT = 27,603 s, LMT at 20.7° E]:

| Night (1178 BC) | B&M day | Elongation at midnight | Illuminated | Moonrise (LMT) | Sunrise (LMT) |
|---|---|---|---|---|---|
| 11/12 Apr | −5 seq | 301° | ≈24% | ≈03:48 | ≈05:46 |
| 12/13 Apr | −4 seq | 314° | ≈15% | ≈04:18 | ≈05:44 |
| 15/16 Apr | −1 | 353° | ≈0.3% | ≈05:36 | ≈05:40 |

On 11 April sunset was at ≈18:20, so the night had about 8 hours without a Moon. On the night of 15/16 April the Moon was invisible.

**Reading.** The night is "dark-of-the-month" in the sense of the last week of the lunar month. The clue is compatible, but weak: any night within about ±4–5 days of conjunction has the Moon down for most of the night. It is also not independent of the new-moon constraint, since it is a consequence of it. Besides, it rained all night (14.457–458), so the darkness is over-determined [inference].

**Classification**: A (used). Compatible. Weak and not independent.

### 5.3 Apollo's feast (20.155–156, 20.276–278, 21.257–268): a new-moon festival?

**What the text says.**

- A feast "for all" (πᾶσιν ἑορτή, 20.156).
- Heralds lead a sacred hecatomb through the town, and the Achaeans gather in the shady grove of far-shooting Apollo (20.276–278).
- "Now throughout the land is the holy feast of the god" (21.258–259), which the scholion glosses as "the god of the bow" [schol. 21.258 (V)].
- Antinous proposes sacrificing goats to "Apollo the famed archer" tomorrow (21.265–268).
- Odysseus prays to Apollo for his shot (22.7).

**The text never says the feast is a new-moon (νουμηνία) festival.** ἑορτή occurs only at 20.156 and 21.258 in the corpus searched [computed: occurrences.py].

**Where the new-moon link comes from.**

- **The scholion on 20.155 (V)** [2.20.2.42–43]:
  - people consider the new moon (νεομηνία) to belong to all the gods;
  - the day is Apollo's, since the first light belongs to the cause of fire;
  - "they called him Neomenios";
  - "the story is in Philochorus" (4th–3rd century BC);
  - a second note says the poet sets the day as "feast and noumenia sacred to Apollo" so that Odysseus can attack while men are busy at the festival.
- **P.Oxy. 53.3710** (2nd century AD commentary on Odyssey 20, ed. Haslam 1986) [secondary, not read; reported by sententiaeantiquae.com and by Panchenko's paper on Aristarchus and Thales]:
  - "Aristonicus says it was the new moon then", with a connection to Apollo "since he is the Sun";
  - Aristarchus of Samos is quoted: eclipses happen at the new moon.
- **Murray and Campbell** [B&M SI *Metonic Cycles*].

**Counter-evidence and complications.**

- **Hesiod, WD 770–771**: the holy days are ἕνη (the "old" or last day), the 4th, and the 7th. The 7th is holy because Leto bore Apollo then.
- **Herodotus 6.57.2**: at Sparta a full-grown victim for Apollo was given "every new moon and on the seventh of the waxing month".
- So Apollo's monthly days are the new moon **and** the 7th. A festival of Apollo does not by itself fix the new moon [inference].
- **νουμηνία versus conjunction.** In Greek practice the noumenia is the first day of the month, normally after first visibility of the crescent. Plutarch (*Solon* 25.3) explicitly places the conjunction on the ἕνη καὶ νέα, the day *before* the noumenia. A solar eclipse can only fall on the conjunction. If Day 0 is a noumenia festival in the observational sense, an eclipse on Day 0 is excluded (the eclipse would be the day before). If Day 0 is the ἕνη καὶ νέα, it is not the noumenia festival the scholion describes [inference]. The ancient sources themselves blur these: "τριακὰς καὶ νουμηνία" (Heraclitus; the scholion).
- **"Apollo, a solar deity"** [B&M §Method; SI]. In Homer Helios is a distinct god (Od. 8.302; 12.374–388; 12.127–136). The identification of Apollo with Helios is post-Homeric, and the papyrus' remark that Apollo "is the Sun himself" belongs to the later commentary tradition [inference].

**Classification**: A (used). The new-moon identification is ancient exegesis, not text. It is compatible with the conjunction only on one of several readings, and in tension with an observational noumenia.

### 5.4 "Spring newly begun" (19.519)

The phrase occurs in Penelope's nightingale simile: the daughter of Pandareus, the pale nightingale, sings "at spring newly begun" (ἔαρος νέον ἱσταμένοιο). The hemistich is **identical to Hes. WD 569**. There, about 60 days after the winter solstice, Arcturus rises at dusk and then the swallow appears to men "at spring newly begun" (WD 564–569) [computed: formula.py]. In Hesiod's terms, "newly begun" spring is about late February to early March. Mid-April is still spring [inference].

The scholion explains χλωρηΐς as the bird "seen among green things, for it appears in spring" [schol. 19.518 (V) 2.19.2.164].

The phrase is **a simile inside a character's speech**. It describes when nightingales sing, not when the scene takes place. Levaniouk reads the spring theme as thematic: the return of light and spring in book 19, with the swallow and Apollo's festival [Levaniouk, "Book 19", *Oxford Critical Guide to Homer's Odyssey*, pp. 242–243, chapter PDF; read].

**Classification**: B (weak) / D. Compatible with a spring setting, but it is formulaic and seasonless as evidence.

### 5.5 "Turnings of the Sun" (15.403–404)

Eumaeus' native island Syrie lies "above Ortygia, where the turnings of the Sun are" (ὅθι τροπαὶ ἠελίοιο). In Hesiod τροπαὶ ἠελίοιο means the **solstice** (WD 564, 663).

Two ancient readings [schol. 15.404 (Q.V.; B.H.Q.)]:

- a "cave of the Sun" on the island by which the solstices are marked;
- the phrase gives the direction "toward the Sun's turnings, i.e. westward, above Delos". This is the reading of Aristarchus and Herodian.

Diogenes Laertius 1.119 reports that Pherecydes' ἡλιοτρόπιον (solstice-marker) was preserved on Syros [diogenes-laertius-grc.tsv 1.11.119.3].

The narrative level is E (Eumaeus' life story, from long ago). The clue is geographic or ethnographic and says nothing about the date of Odysseus' return.

**Classification**: D. B&M did not use it.

### 5.6 Weather and cold nights; the season of the arrival

**Primary narrative (P, and C in the story's present), in story order:**

| Day (1178 BC) | Lines | Weather or season signal |
|---|---|---|
| −9 (7 Apr) | 5.466–469 | Fear of frost, dew and the cold dawn breeze off the river |
| −8 (8 Apr) | 6.305, 7.153 | Arete at the hearth |
| −7 (9 Apr) | 11.373 | "This night is very long" |
| −5 (11 Apr) | 14.457–458 | Moonless night; rain all night; strong, ever-wet west wind |
| −5 (11 Apr) | 14.518–533 | Fire, fleeces, a spare thick cloak; Eumaeus sleeps outside in a windproof cloak under a rock sheltered from Boreas |
| −3 (13 Apr) | 15.392 | "These nights are endless" |
| −2 (14 Apr) | 16.2 | A fire lit at dawn |
| −1 (15 Apr) | 17.23–25 | "Let me warm myself first; the morning frost may overcome me in these rags" |
| −1 (15 Apr) | 17.191 | Colder toward evening |
| −1 (15 Apr) | 18.307–311, 19.63–64, 19.506–507 | Braziers; fire "for light and warmth" |
| 0 (16 Apr) | 20.1–4, 20.95 | Fleeces and a cloak in the porch |
| 0 (16 Apr) | 20.113–114 | A clear starry pre-dawn sky with no cloud |
| 0 (16 Apr) | 20.249 | The suitors lay their cloaks on chairs |

**Lying tale (L), 14.475–477:** a bitter north wind, frost, snow like rime, ice on the shields. It is set at Troy about 20 years earlier and told to get a cloak. It says **nothing** about the present season. B&M did not use it either.

**Night length** [computed: nightlength.py; Sun's centre at −0.833°, Ithaca, 1178 BC (−1177), proleptic Julian]:

| Date (1178 BC) | Night length |
|---|---|
| 11 Apr | 11.4 h |
| 16 Apr | 11.2 h |
| 18 Mar | 12.4 h |
| 15 Oct | 12.4 h |
| 15 Nov | 13.6 h |
| 15 Dec | 14.5 h |

So "very long" or "endless" nights (11.373, 15.392) fit late autumn or winter better than mid-April. They are, however, conversational hyperbole: "there is time to sleep and time to hear stories" [inference].

**The ancient commentators' verdict.** Five scholia read the season as autumn heading into winter, or as winter:

- 11.373 (H.T.): "from this too the season appears to be autumn".
- 17.24 (H): "from this too the season appears autumnal, and already towards winter". The words "καὶ ἐντεῦθεν" (from this too) imply that the commentators had other indicators.
- 17.191 (V): "towards evening it is more wintry".
- 14.458 (B.Q.): the west wind is rainy "not always, but in winter".
- 6.305 (B): "this shows the season, that it was winter"; (H) "as if it were winter".

Of these, 11.373 and 6.305 concern Phaeacia and 17.24, 17.191 and 14.458 concern Ithaca.

**Spring signals** are all similes or hypotheticals:

- the nightingale (19.519);
- the swallow (21.411, 22.240);
- the gadfly "in spring when days lengthen" (22.301; the same line as the hypothetical at 18.367, and akin to Il. 2.471 and 16.643);
- snowmelt (19.205–207).

B&M's one "factual" spring item is the "much-flowering" thicket (14.353), and it sits **inside a lie**. Laertes digging round a plant on Day +1 (24.227) is weakly spring-like (Hes. WD 570–572).

**Assessment** [inference]:

- The descriptive weather (rain, westerly, chilly mornings and evenings, fires, cloaks) is compatible with early-to-mid April in the Ionian islands. It is equally compatible with late autumn or winter.
- The ancient reading of the same lines was autumn-winter.
- The "long night" remarks lean mildly against a post-equinox date.
- The season of the arrival is **not determined by the text**.
- B&M's season comes from their reading of 5.272 (§5.8), not from the Ithaca narrative.

**Classification**: 14.457–458 weather B; 17.25, 5.467, 11.373, 15.392 C (weak); 14.475ff D (lying tale); the similes D or weak B.

### 5.7 The morning star (13.93–95)

**Text.** "When the brightest star rose (ὑπερέσχε), the one which most of all comes announcing the light of early-born Dawn, then the sea-going ship drew near the island." The construction is εὖτ' … τῆμος, "when … then".

**Formularity** [computed: formula.py; Il. lines printed above]:

- **Il. 23.226–228**: "When the light-bringer (ἑωσφόρος) goes forth announcing light upon the earth, after whom saffron-robed Dawn spreads over the sea, then (τῆμος) the pyre died down." This has the **same device**: a dawn-announcing star marks the end of a night-long activity (pyre, voyage). The verbs differ: ἐρέων in the Iliad, ἀγγέλλων in the Odyssey.
- **Il. 5.5–6** (the late-summer star, Sirius): "ἀστέρ' ὀπωρινῷ ἐναλίγκιον, ὅς τε μάλιστα / λαμπρὸν παμφαίνῃσι". The line-end "ὅς τε μάλιστα" with the verb enjambed into the next line is identical in form to 13.93–94.
- **Il. 22.317–318**: Hesperos, "the most beautiful star in heaven", in a simile. **Il. 22.26–31**: Sirius, "the brightest" (λαμπρότατος), in a simile. Superlatives are the norm for Venus and Sirius in the tradition.
- **Il. 11.62–63**: the baleful star (Sirius) appearing and disappearing in clouds. **Il. 4.75–78**: a star or meteor sent by Zeus as a portent.
- **Hes. Th. 381**: Eosphoros, child of Erigeneia (Dawn).
- φαάντατος occurs only here in the corpus searched.

**What the ancients said.**

- The only scholion on 13.93 glosses the verb: "until it rose above" [schol. 13.93 (Q)]. It does not identify the star.
- The scholion on 2.1 uses Il. 23.226–227 to explain the dawn epithets: Dawn "saffron-robed" follows Heosphoros.

**Reading** [inference]. The line is a **traditional time-marker** meaning "at the last hour of night, just before dawn". It is not a formula word for word, but the device is inherited. The Iliad uses the same device for the morning after Patroclus' pyre. A literal "Venus was a morning star that day" reading would equally constrain the Iliad's chronology there. That gives the bench an internal positive or negative control (§8).

**Classification**: A (used). B&M compute it as compatible (1 h 43 min on 11 April 1178 BC; not checked here). The device is traditional, so it is weak evidence of a dated observation.

### 5.8 The star lines (5.270–277) and the Shield of Achilles

| Odyssey | Iliad / Hesiod | Status [computed: formula.py] |
|---|---|---|
| 5.272 Πληιάδας τ' ἐσορῶντι καὶ ὀψὲ δύοντα Βοώτην | Il. 18.486 Πληϊάδας θ' Ὑάδας τε τό τε σθένος Ὠρίωνος; Hes. WD 615 Πληιάδες θ' Ὑάδες τε τό τε σθένος Ὠαρίωνος | Same opening word. Il. 18.486 and WD 615 are one verse in different case and dialect. |
| 5.273 Ἄρκτον θ', ἣν καὶ ἄμαξαν ἐπίκλησιν καλέουσιν | Il. 18.487 | Verbatim (7 words) |
| 5.274 ἥ τ' αὐτοῦ στρέφεται καί τ' Ὠρίωνα δοκεύει | Il. 18.488 | Verbatim (8 words) |
| 5.275 οἴη δ' ἄμμορός ἐστι λοετρῶν Ὠκεανοῖο | Il. 18.489 | Verbatim (6 words) |

B&M acknowledge in a bracket that some of "these exact same lines appear in the Iliad (Il. xviii.485)" [B&M §Method]. They draw no consequence from it. The ancient scholiasts flagged the identity too [schol. 5.272 (E) cites Il. 18.486; schol. 5.273 (P): "in the Iliad too he says the same about the Bear"].

**Consequence** [inference]:

- Three of the four star lines are a **star catalogue inherited from the tradition**. In the Iliad it decorates a static artefact, the Shield, and in Hesiod (WD 615) it is part of a seasonal calendar.
- A list taken from the tradition is evidence *against* the passage recording what one observer saw on one night.
- Aristotle already treated "alone has no share" as poetic licence: "alone" stands for "best known" (*Poetics* 25, 1461a20–21). The line is not astronomically exact.

**The unique element is "ὀψὲ δύοντα Βοώτην".** It has three possible readings:

- **(i) B&M (after MacDonald 1967)**: Boötes visible late into the night, that is, it sets late. True in late winter and early spring evenings, when Arcturus rises at dusk (Hes. WD 564–567: 60 days after the winter solstice). Hence B&M's window: T−29 between 17 February and 4 April.
- **(ii) Ancient astronomical gloss**: Boötes is *slow*-setting, a permanent property. "Setting long after those that rose with it", because it goes down upright together with four zodiacal signs, Scorpio to Aquarius [schol. 5.272 (E; E.H.P.Q.V), quoting Aratus 581–582]. On this reading the epithet carries no season.
- **(iii) Aratus 579–585**: when Boötes begins to set at sunset, its setting occupies more than half the night, at ox-unyoking time, and "those nights are named after his late setting" (ἐπ' ὀψὲ δύοντι). Two scholia link the epithet to the unyoking of oxen [schol. 5.272 (B.V; P.Q.)]. If "late-setting nights" are those on which Boötes sets in the evening, the season is autumn, not March. This last step is my inference; the bench should compute the exact dates.

Other points [inference]:

- The Pleiades, without any qualifier, are visible on some part of most nights for about ten months of the year.
- The passage describes Odysseus' **habitual** watch over 17 nights ("sleep did not fall on his eyelids as he watched …"). It does not report what he saw on the first evening.
- "Keep the Bear on your left" (5.276–277) is a heading, not a date.

**Classification**: A (used). 5.273–275 are formulaic and inherited (D-like for dating). 5.272 depends on interpretation; under readings (ii) and (iii) it is uninformative or in tension.

### 5.9 Hermes' journey (5.43–56): does anything indicate the planet Mercury?

**No.** The evidence [Od., Il. as printed; computed: formula.py; scholia]:

1. **5.43–49 are seven lines verbatim from Il. 24.339–345**, where Hermes goes to Priam.
   - 5.44–46 also = Od. 1.96–98 (Athena puts on the same sandals).
   - 5.47–48 = Od. 24.3–4 (Hermes Psychopompos' wand).
   - An ancient critic noted the transfer of these lines, though he took the book-5 instance as their origin [schol. 5.43 (H.P.Q.)].
2. **The non-repeated lines (5.50–54)** describe:
   - a route via Pieria, near Olympus: the same stopover as Hera's journey in Il. 14.225–226;
   - a plunge to the sea and skimming the waves like a gull (λάρος). Gods are compared to birds at Od. 5.337 (Leucothea), 22.240 (Athena), and Il. 24.80 (Iris "like a lead weight"). The scholion: the likeness is "in impulse, not in form" [schol. 5.51 (V; P)].
   - Line 5.54 was **athetized** in antiquity: "someone added the line improperly" [schol. 5.54 (H.P.Q.)].
3. **There is no word for light, star, brightness, west, rising, setting, station or turning.** Ogygia is "far off" (5.55). Its direction is not given. That it lies west of Scheria is inferred from Calypso's instruction to keep the Bear on the left (5.276–277). The scholia place it outside the Mediterranean [schol. 5.100] and "in remote, unspecified places" [schol. 5.55].
4. **The departure (5.148) is "ὣς ἄρα φωνήσας ἀπέβη κρατὺς ἀργεϊφόντης"**: "having spoken, he went away". It has no "back east" and no "turned around".
5. **Ancient allegorists read Hermes as λόγος (speech or reason)**, not as a planet [schol. 5.45 (B), 5.47 (E.V; H.P.Q.T); Heraclitus *All.* ch. 72 local numbering].
6. **Hermes appears again in the dated window**: on the night after the slaughter he leads the suitors' souls "past the gates of the Sun" (24.1–14). B&M's rule (a god's journey stands for a planet's motion) is applied to the book-5 journey and not to this one [inference].
7. **Naming.** The earliest Greek naming of the planet for Hermes is Plato, *Timaeus* 38d and *Epinomis* 987b. B&M concede this.
8. **The Homeric Hymn to Hermes** (75–78: cattle driven with reversed tracks) is B&M's "debatable" allusion to retrograde motion. It is a cattle-theft trick in the text [h.Herm. 75–78].

**Classification**: A (used, conjecturally). No text indication of the planet. Formulaic and recycled.

### 5.10 Dawn formulas and other time-of-day markers

| Formula | Occurrences [computed: occurrences.py] |
|---|---|
| ἦμος δ' ἠριγένεια φάνη ῥοδοδάκτυλος Ἠώς | 20 in the Odyssey, 2 in the Iliad |
| αὐτίκα δὲ χρυσόθρονος ἤλυθεν Ἠώς | 4, all Odyssey (10.541, 12.142, 15.56, 20.91) |
| Ἠὼς δ' ἐκ λεχέων παρ' ἀγαυοῦ Τιθωνοῖο | Od. 5.1 = Il. 11.1 |
| δύσετό τ' ἠέλιος σκιόωντό τε πᾶσαι ἀγυιαί | 9 |
| ἦμος δ' ἠέλιος κατέδυ καὶ ἐπὶ κνέφας ἦλθε | 7 (including Il. 1.475) |
| ἀλλ' ὅτε δὴ τρίτον ἦμαρ ἐυπλόκαμος τέλεσ' Ἠώς | 3 |
| Noon: ἦμος δ' ἠέλιος μέσον οὐρανὸν ἀμφιβεβήκει | Od. 4.400 ≈ Il. 8.68, 16.777 |
| Afternoon: μετενίσσετο βουλυτόνδε | Od. 9.58 ≈ Il. 16.779 |
| Star-clock: τρίχα νυκτὸς ἔην, μετὰ δ' ἄστρα βεβήκει | Od. 12.312 = 14.483; cf. Il. 10.251–253 |

These are useful only for **relative** day counting. They carry no astronomical date.

Two observations [inference]:

- The tradition had a noon formula. It is **not** used at Theoclymenus' vision. The "noon" timing of the eclipse scene is Schoch's and B&M's inference from δεῖπνον (20.390) and the plot.
- Athena's divine lengthening of the reunion night (23.241–246) and Hera's early sunset in Il. 18.239–241 show that day and night lengths in epic are narrative instruments.

**Classification**: D (but A where used for B&M's day count).

### 5.11 Theoclymenus' vision (20.345–357): diction and ancient reception

The vision's language is the stock diction of death and the underworld [computed: occurrences.py; formula.py]:

- night covering heads and faces (compare κατ' ὀφθαλμῶν ἐρεβεννὴ νὺξ ἐκάλυψε, 7 times in the Iliad);
- ἀχλύς, used of a dying man's eyes in Il. 5.696, 16.344, 20.421 and Od. 22.88, the death of Eurymachus on this very day;
- ghosts going "to Erebus beneath the gloom" (compare Od. 11.57, 11.155; Il. 23.51; h.Dem.);
- **the verse-end "κακὴ δ' ἐπιδέδρομεν ἀχλύς" mirrors Od. 6.45 "λευκὴ δ' ἐπιδέδρομεν αἴγλη"** (a white radiance has spread over Olympus). The verb means "has spread over". It does not mean B&M's "attacking suddenly".

The poem itself has the motif of the Sun leaving the sky (12.383, Helios' threat). The Iliad has darkness over battle: "you would not say the Sun or Moon was safe" (Il. 17.366–368), Zeus spreading "deadly night" (Il. 16.567), Ares covering the battle in night (Il. 5.506–507).

**Ancient reception.**

- The Dindorf scholia **deny** that an eclipse took place. "There was no eclipse of the sun. Theoclymenus, prophesying in a kind of inspiration, sees that the sun will fail for them. The suitors see nothing of the kind and want him thrown out as raving" [schol. 20.356 (B) 2.20.2.91]. "Not as if an eclipse had happened, but that for the suitors the sun had failed" [ibid. (V)].
- The eclipse reading belongs to the allegorists and to Plutarch:
  - Heraclitus, *Homeric Problems* 75 (local edition chapter 73): blood-red colour in eclipses; Hipparchus' timing of eclipses to the "30th and noumenia"; 14.162 quoted as giving the time.
  - Plutarch, *De facie* 19 (931D–E): Homer's faces held by night, the Sun perished "near the moon", and that this happens "τοῦ μὲν φθίνοντος μηνὸς τοῦ δ' ἱσταμένοιο".
- **The combination of 20.356–357 with 14.162 is therefore at least first-century AD exegesis.** The papyrus commentary P.Oxy. 3710 continues it [secondary, not read].

---

## 6. Formularity: method and summary

**Method** [computed: `docs/textclues-scripts/formula.py`, `occurrences.py`]:

- Greek was normalised: diacritics stripped, ς→σ, elision marks and punctuation removed.
- A 3-word n-gram index was built over the Iliad (15,687 lines), the Odyssey (12,107), Hesiod's WD, Th and Sc, and the Homeric Hymns 2, 3, 4, 31 and 32. All are exported read-only from the ClassicaCodex library, except the Iliad and Odyssey, which were already in `data/text`.
- For each clue line I report the longest shared contiguous word run with every other line, skipping neighbours within ±3 lines in the same book.
- Aratus was searched separately as later reception. Throughout this document, "hapax" and "only here" mean within this searched corpus, not all of Greek.

**Limitations.** Exact-match normalisation misses dialect, case and inflection variants: Il. 18.486 against WD 615, and Pieria at 5.50 against Il. 14.226, were found by reading. The hymns' coverage is partial.

**Verbatim or near-verbatim repeats among the dating clues:**

| Clue | Repeat | Reading |
|---|---|---|
| Od. 5.273–275 | = Il. 18.487–489 | Inherited star catalogue |
| Od. 5.272 (opening) | Il. 18.486 ≈ Hes. WD 615 | Catalogue verse |
| Od. 5.43–49 | = Il. 24.339–345 (7 lines); 5.44–46 = Od. 1.96–98; 5.47–48 = Od. 24.3–4 | Type-scene |
| Od. 14.161–162 | = 19.306–307; oath frame ≈ 17.155–156, 20.230–231 | Repeated oath-slot |
| Od. 14.457 | "νὺξ δ' ἄρ' ἐπῆλθε κακή" + epithet = 14.475 (lying tale) | Formulaic frame; σκοτομήνιος hapax |
| Od. 13.93–95 | Same device as Il. 23.226–228; "ὅς τε μάλιστα" + enjambment = Il. 5.5–6 | Traditional time-marker; no verbatim repeat |
| Od. 19.519 | Hemistich = Hes. WD 569 | Traditional "start of spring" phrase |
| Od. 18.367 | = 22.301; ≈ Il. 2.471, 16.643 | Stock seasonal phrase |
| Od. 10.469–470 | ≈ Hes. Th. 58–59; also 19.152–153, 24.142–143 | Stock time-passing |
| Od. 11.294–295 | = 14.293–294 = h.Ap. 349–350 | Stock |
| Od. 12.312 | = 14.483 | Stock star-clock |
| Od. 5.278–279 | 17/18 numerals = Od. 24.63–65 | Typological numerals |
| Od. 1.16 | Line-end = Hes. Th. 184, h.Dem. 265 | Stock |
| Od. 20.357 | Verse-end template = Od. 6.45 | Stock template |

The repeated lines do not show that the passages are false. They show that the wording was available to poets regardless of any sky. **A formula inherited from the tradition cannot by itself be a record of a sky seen on one date** [inference, as framed in the task].

---

## 7. What, if anything, the text can date (my inference)

1. **Relative chronology: yes, roughly.**
   - Day 0 is about 34–35 days after Hermes' visit and about 29 days after the departure from Ogygia.
   - The arrival on Ithaca is 4–5 days before Day 0.
   - The ±1-day ambiguity comes from sequential versus parallel reckoning [B&M Table 1]. The 17/18 and 20-day figures are typological, so the numbers may be poetic rather than measured.
2. **Lunar phase: a single, prophetic, possibly interpolated statement.** It says Odysseus's coming falls at a month-turn (14.162 = 19.307). It is supported only weakly and non-independently by σκοτομήνιος, and only by ancient exegesis for the festival. Even granting it, the readings conjunction day, noumenia and 20-day window give different targets. Only the conjunction reading allows an eclipse.
3. **Season: not determined.** The narrative weather is compatible with late autumn through early spring. The ancient commentators read autumn-winter. The spring hints are similes. B&M's season rests on the unique epithet in 5.272, which has a non-seasonal ancient reading.
4. **Planets: nothing explicit.** The Odyssey names no planet. The morning star is a traditional time-marker. Mercury is not in the text.
5. **Year: the text alone cannot select one.** Any absolute date needs the eclipse hypothesis, or B&M's composite of the Venus, Mercury and Boötes interpretations.

---

## 8. Forking paths, and suggestions for the bench's nulls and controls

**Interpretive forks found in the text** (each is a real choice a reader of the Greek has to make):

| # | Fork | Options |
|---|---|---|
| 1 | Meaning of 14.162 | Conjunction day / noumenia (+1–2 d) / ±10-day window |
| 2 | Prophecy target | Arrival / revelation / slaughter |
| 3 | Day 0 festival | New moon / the 7th (Hesiod, Herodotus) / unspecified |
| 4 | ὀψὲ δύοντα | Visible late (B&M) / slow-setting (scholia) / evening-setting season (Aratus) |
| 5 | Star constraint | First night only / all 17 nights (B&M require both) |
| 6 | Morning star | Venus ≥ 90 min before the Sun / any morning visibility / generic time-marker |
| 7 | Hermes | Westernmost rising azimuth / greatest elongation / station / not Mercury |
| 8 | Reckoning | Sequential / parallel |
| 9 | Season | Spring / autumn / unconstrained |
| 10 | Year window | 1250–1115 BC |

Forks 1–9 alone give 3×3×3×3×2×3×4×2×3 = 23,328 paths. Each could be scored, to see how many paths give *some* date with a joint-probability as small as B&M's [inference].

**Internal controls the text offers:**

- **Il. 23.226–228** (Heosphoros at the end of the pyre night) and the Iliad's own day counts (the funeral games, Il. 24.31 "the twelfth dawn", and others). Apply B&M's literal-reading rules to the Iliad and see whether it "dates" as cleanly. This tests the instrument.
- **Hesiod's WD star calendar** (Arcturus 60 days after the solstice, WD 564–567; the Pleiades' setting, WD 615–621) is a text whose star statements are explicitly seasonal and generic. A good positive control for the season-only part of the method.

**Not text controls, but standard:** the dated literary eclipses (Archilochus fr. 122; Hdt. 1.74; Thuc. 2.28; Plut. *Pelopidas* 31) can serve for the eclipse-detection step. Other agents are covering these.

---

## 9. Reproducibility

The scripts are in `C:\Projects\odybench\docs\textclues-scripts\`. Each reads only `data/text/*.tsv`.

| Script | What it does |
|---|---|
| `tx.py` | Loads the Odyssey, Iliad and scholia; indexes the scholia by book and line from their lemma numbers. |
| `scholia.py BOOK:A-B` | Prints the scholia for a line range. |
| `passage.py BOOK:A-B` | Prints the Odyssey Greek for a range. |
| `formula.py BOOK:A-B` | 3-gram index; longest shared runs (≥ 3 words) in the archaic corpus, plus Aratus. |
| `occurrences.py STEM…` | Occurrences of an accent-stripped stem or phrase across the corpus. |
| `moon.py` | Truncated Meeus Sun and Moon (ch. 25 and 47 main terms; about 0.3° accuracy), ΔT = 27,603 s, Ithaca 38.4° N 20.7° E. Prints the conjunction and the Moon's rise and phase for the nights cited. A sanity check only, not the bench's ephemeris. |
| `nightlength.py` | Vernal equinox 1178 BC (−1177) and night lengths. |

The library search for λυκάβας was a read-only `LIKE` query through `odybench.ccx.library()` (77 nodes). The following were exported read-only via `py -m odybench.ccx export`:

- `hesiod-theogony-grc.tsv`, `hesiod-shield-grc.tsv`
- `aratus-phaenomena-grc.tsv`
- `hhymn03-apollo-grc.tsv`, `hhymn04-hermes-grc.tsv`
- `herodotus-grc.tsv`, `heraclitus-allegoriae-grc.tsv`, `plutarch-defacie-grc.tsv`
- `geminus-grc.tsv`, `plato-timaeus-grc.tsv`, `dio-chrysostom-grc.tsv`, `suda-grc.tsv`

Hesiod WD was already present as `hesiod-worksdays-grc.tsv`.

---

## 10. Not read, and open questions

**Primary or secondary sources I could not read:**

| Source | Status |
|---|---|
| Austin, *Archery at the Dark of the Moon* (1975) | Known only from a search summary |
| Gainsford, "Odyssey 20.356–57 and the Eclipse of 1178 B.C.E.", *TAPA* 142.1 (2012) 1–22 | Abstract only. Project MUSE and ResearchGate were behind bot challenges, which I did not bypass. The abstract as indexed says "26 April 1178 B.C.E."; B&M say 16 April. 26 April is not the proleptic Gregorian equivalent, which is about 5 April, so it looks like a typo in the abstract [inference]. |
| MacDonald, "The season of the Odyssey", *J. Brit. Astron. Assoc.* 77 (1967) 324–328 | Known only through B&M |
| Schoch (1926) | Not read by me. A sibling agent saved a copy at `data/bm2008-a/schoch-1926-observatory-49-19.pdf`. |
| P.Oxy. 53.3710 (ed. Haslam 1986) | Secondary reports only |
| Russo / Fernández-Galiano / Heubeck, *Commentary on Homer's Odyssey* vol. III; Hoekstra vol. II; Hainsworth vol. I | Not available. These are the standard treatments of 14.161–162, 19.306–307, 20.156, 21.258 and 5.272–277. |
| Eustathius' Odyssey commentary | Not in the library; probably comments on 13.93, 14.457 and the season |
| Philochorus' fragment on Apollo Neomenios | Known only through the scholion |
| Borthwick, "Odysseus and the Return of the Swallow", *G&R* 35 (1988) 14–22 | Abstract or extract only |
| Guglielmino, Cipolla & Rizzo Giudice, "Astronomy in the Odyssey: The Status Quaestionis" (2017) | Not read (403) |

**Open questions:**

1. On which Julian dates in 1250–1115 BC does Arcturus set at the end of evening twilight at Ithaca? This would test reading (iii) of ὀψὲ δύοντα quantitatively.
2. Which three lines does schol. 14.162 (H) suspect? What did Aristarchus do with 14.158–164? Hoekstra's commentary would answer this.
3. Does the Dindorf text omit scholia on 21.258–268 and 22.300–301, or are there none? Erbse/Pontani's newer editions cover books 1–8 only.
4. Is Murray's "day" at 14.161 a deliberate rendering of the LSJ suggestion ("perh. day")? Any null model of B&M's "New Moon" input should note that the input came partly from a translation.

---

## Sources

**Primary Greek, all local.** Each was exported read-only from Jon's ClassicaCodex library unless noted. Text editions are Perseus or First1K as recorded in the TSV keys.

- `data/text/odyssey-grc.tsv`, `iliad-grc.tsv`, `odyssey-murray.tsv`, `scholia-odyssey-grc.tsv` (Dindorf)
- `hesiod-worksdays-grc.tsv`, `hesiod-theogony-grc.tsv`, `hesiod-shield-grc.tsv`
- `hhymn02-demeter-grc.tsv`, `hhymn03-apollo-grc.tsv`, `hhymn04-hermes-grc.tsv`, `hhymn31-helios-grc.tsv`, `hhymn32-selene-grc.tsv`
- `aratus-phaenomena-grc.tsv`, `herodotus-grc.tsv` (6.57.2), `heraclitus-allegoriae-grc.tsv` (local ch. 72–73 = *Homeric Problems* 70–75 region), `plutarch-defacie-grc.tsv` (ch. 19), `plutarch-solon-grc.tsv` (25.3), `dio-chrysostom-grc.tsv` (7.84–85), `diogenes-laertius-grc.tsv` (1.119), `plato-timaeus-grc.tsv`
- Aristotle, *Poetics* 25 (library editions 1230/1232)
- Library-wide λυκάβας search: Apollonius Rhodius, Oppian, Nonnus, Quintus, Greek Anthology, Herodian, Artemidorus, Aelian, Aristophanes of Byzantium, Suda, Julian, Apollonius Dyscolus

**Baikouzis & Magnasco.**

- C. Baikouzis & M. O. Magnasco, "Is an eclipse described in the Odyssey?", *PNAS* 105 (2008) 8823–8828. https://pmc.ncbi.nlm.nih.gov/articles/PMC2440358/ (full text read).
- The SI, read from the local copy `data/bm2008-a/baikouzis-magnasco-2008-SI.pdf`.

**Dictionaries.**

- LSJ s.v. λυκάβας, via Perseus: http://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.04.0057:entry=luka/bas
- Autenrieth s.v., via Perseus.

**Secondary sources.**

- O. Levaniouk, "Book 19", *Oxford Critical Guide to Homer's Odyssey*, pp. 242–243. Chapter PDF: https://classics.washington.edu/sites/classics/files/documents/research/workid-ukukac0016833-book-part-20.pdf (read, relevant pages).
- P. Gainsford, *TAPA* 142.1 (2012) 1–22, doi:10.1353/apa.2012.0006. Abstract via https://colab.ws/articles/10.1353/apa.2012.0006
- E. K. Borthwick, *G&R* 35 (1988) 14–22. Extract via https://www.cambridge.org/core/journals/greece-and-rome/article/abs/odysseus-and-the-return-of-the-swallow/96001E56E7B51398AC36405E7CB8C560
- P.Oxy. 3710 reports: https://sententiaeantiquae.com/2024/04/08/an-eclipse-in-the-odyssey-2/ ; https://www.academia.edu/13103929/Aristarchus_of_Samos_on_Thales_Theory_of_Eclipses (search summary only)
- Kiwi Hellenist (Gainsford's blog), September 2018: http://kiwihellenist.blogspot.com/2018/09/
- Guglielmino et al. (2017): https://link.springer.com/chapter/10.1007/978-3-319-54487-8_10 (not read)
