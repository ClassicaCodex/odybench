# The unread primaries: MacDonald 1967, Schoch and Neugebauer, Papamarinopoulos 2012, Henriksson 2012, PLSV

Research note for odybench. Written 2026-10-04.

**Scope.** DESIGN §8 item 19 lists the primary sources the dossier had not read. Critique issue 6 turns on one of them, MacDonald 1967: was the spring season clue C formed without the 1178 BC eclipse in view? This note reports what I could obtain, what each source says, and its bearing on the bench. I could not obtain some items, and §8 says why.

**Conventions.** Years are given historical and astronomical: 1178 BC = −1177. Dates are proleptic Julian unless marked. Time scales are named: UT, LMT (local mean time), and LT where a paper uses a zone time.

**Provenance tags.**
- **[read: file, p. n]**: I read the primary text myself at that page.
- **[secondary: X]**: I know the item only through X.
- **[computed: script]**: I computed it myself; the scripts are in `results/unread-primaries/`.
- **[inference]**: my own reasoning, not a source's statement.

---

## 0. Findings in brief

1. **MacDonald argued for March, not May.** He put the voyage from Ogygia in March [read: macdonald, p. 325].
   - His case rests on Od. 5.270–277, the Pleiades, "late setting" Boötes and the Bear. He computed it for 1000 BC with P. V. Neugebauer's star tables and Schoch's arcus visionis values.
   - He adds a timetable built on Poseidon's return from the Ethiopians (Od. 1.22–26, 5.282), read as the equinox. Under it the action starts about 22 Feb, the shipwreck falls about 21 Mar, and the slaughter about the end of the first week of April [p. 326].
   - **B&M report him correctly.** Their quoted sentence is his, from p. 325.
   - **Gainsford's "second half of May" misreads p. 327.** MacDonald cites the reaping match (Od. 18.366) only to answer Schoch, who had said the line showed winter, not April. MacDonald replies that Hesiod puts the sickle-sharpening at the Pleiades' return in the second half of May. That is a rebuttal, not his setting for the poem. Gainsford's locator "MacDonald 1967: 217" is also wrong: the passage is on p. 327.
2. **MacDonald discusses the 1178 BC eclipse and cites Schoch and Neugebauer** [p. 326–327, references p. 327].
   - He gives "1178 B.C.", "April 16" and "11.45 a.m. local time".
   - He calls the one-week gap between his timetable and the eclipse possibly "sheer accident".
   - His references list Schoch's *Die Sterne* 6:88, Schoch's *Die sechs griechischen Dichter-Finsternisse*, and Neugebauer's *Astronomische Chronologie* (1929).
3. **Clue C cannot be shown to have been formed without the eclipse in view. The record points the other way.** [inference, from the items below]
   - (a) Schoch 1926 placed the action in April *because of* the eclipse. His search, −1240 to −1140, had no season constraint [read: schoch-1926-observatory.pdf, p. 20–21].
   - (b) MacDonald lists the earlier season readings: Finsler and Wilamowitz (October–November), Scott (30 Aug–19 Sep) and Gilbert Murray (winter). He also reports Schoch's later "winter and not April". None of them is spring [read: macdonald, p. 324, 326, 327].
   - (c) The spring reading of 5.272 enters the literature in 1967, in a paper that already holds the eclipse. MacDonald even checked Venus in the eclipse year (item 4).
   - **So the design's choice to condition p_fix on C has documentary support.** The unconditional figure should be reported as the "C independent" counterfactual, not as the expected value (§9).
4. **MacDonald is also the first source of B&M's Venus and equinox clues, and both are tied to the eclipse year.**
   - He links Od. 13.93 (Venus) with "greatest morning elongation in 1176 B.C. on March 17", from Neugebauer's tables [p. 327].
   - DE441 puts Venus' greatest western elongation on **16 Mar −1177 = 1178 BC** [computed: venus_elongation_check.py]. No greatest elongation of either kind falls in 1176 BC (−1175).
   - So "1176" is very probably a slip for 1178 [inference]: he was checking Venus in the eclipse year.
   - B&M cite MacDonald for the equinox conjecture but not for Venus [bm2008.txt, around lines 156 and 243].
5. **Papamarinopoulos et al. 2012 read the same star lines as autumn** [read: pap2012.txt].
   - They reach the annular eclipse of 30 Oct 1207 BC (−1206) through a stated search: 64 eclipses, then 14, then 5, then 1. The first cut is an autumn season taken from weather, plant and animal lines; the rest test for Venus in the east and practical visibility, and drop 1143 BC on archaeological grounds.
   - The first author had proposed 16 Apr 1178 BC himself in 2008.
   - Their 16:00 "LT" is UT+2, a zone time. It equals 15:23 LMT at Ithaki, which agrees with the dossier's computed 15:26 LMT [inference; research-critiques.md, eclipse table, line 418].
6. **Henriksson 2012 is about the Iliad only** [read: henriksson2012-extract.txt]. He dates Il. 17.366–377 to the eclipse he labels "June 11, 1312 BC (Gregorian)".
   - The canon has it as −1311 Jun 24 Julian, which is proleptic Gregorian 12 Jun. His Gregorian labels run one day early, in both of his eclipses [computed: jd_checks.py].
   - He does not discuss the Odyssey.
7. **PLSV has no physical extinction model** [read: plsv-doc-accuracy.txt, plsv-doc-compphen.txt].
   - Visibility is a magnitude-dependent arcus visionis plus a "critical altitude", which stands in for extinction and the horizon.
   - Defaults:
     - heliacal AV = 10.5 + 1.4 m;
     - acronychal and cosmical AV = 8.9 + 1.1 m;
     - fixed planetary AVs are Schoch's (1928);
     - critical altitude 0°.
   - ΔT in PLSV is Chapront-Touzé & Chapront (1991).
   - This answers DESIGN §8 item 4, "PLSV's extinction parameters unknown": there are none to know. B&M's "standard magnitude-corrected parameters" are these AV formulas, with their 1° and 2° critical altitudes [inference].
8. **The two published Starry Night ΔT values do not come from one smooth ΔT(t)** [computed: deltat_checks.py].
   - Papamarinopoulos 2012 report Starry Night 6 Pro Plus using 29,300 s for 30 Oct −1206. That is the Espenak–Meeus parabola +35 s, without the canon's ṅ correction.
   - The same curve would give about 28,750 s at 16 Apr −1177. B&M's Starry Night 6.0.4 gave 27,602.7 s, which is 1,149 s lower.
   - This does not settle §8 item 6, but it narrows it.

---

## 1. Sources: obtained and not obtained

| Item (DESIGN §8 item 19 unless marked) | Status | File |
|---|---|---|
| MacDonald, *JBAA* 77 (1967) 324–327 | **Read**, ADS scan, 4 pages | `data/refs/macdonald-1967-jbaa-77-324.pdf` |
| P. V. Neugebauer, *Astronomische Chronologie* (1929) | **Not read**. De Gruyter paywall plus bot check; the HathiTrust record stalls on a Cloudflare check (§8). Table of contents only, via Crossref | `results/unread-primaries/neug_toc.txt` |
| Neugebauer & Schoch, *AN* 230 (1927) 57–60, "Zur astronomischen Chronologie" (found on ADS; not on the list) | **Read**. Tables and elements; no Odyssey | `data/refs/neugebauer-schoch-1927-an-230-57.pdf` |
| Neugebauer, Schoch obituary, *AN* 237 (1929) 221–222 (found on ADS) | **Read**, first page only; continuation not retrieved | `data/refs/neugebauer-1929-an-237-221-schoch-obituary.pdf` |
| Schoch, *Die Sterne* 6:88; *Die sechs griechischen Dichter-Finsternisse* (1926); Dörpfeld, *Die Sterne* 6:186–187 | **Not found**. Not in ADS; no online copy found | — |
| Papamarinopoulos et al., *MAA* 12(1) (2012) 117–128 | **Read**. Published PDF as posted by friendsofhomer.gr; same pagination and MAA copyright line | `data/refs/papamarinopoulos-2012-maa-12-117.pdf`, `data/refs/pap2012.txt` |
| Henriksson, *MAA* 12(1) (2012) 63–76 | **Read** in the journal's pdf.js viewer; scripted download blocked by a Cloudflare challenge | `data/refs/henriksson2012-extract.txt` (extract) |
| PLSV internals (Lange & Swerdlow) | **Read**, program documentation for v3.1 via the Wayback Machine | `data/refs/plsv-doc-compphen.txt`, `data/refs/plsv-doc-accuracy.txt` |
| Starry Night internals | **Not available** (commercial). Indirect constraint in §7 | — |
| de Jong 2001 App. A; Stanford 1959; Oxford commentaries | **Skipped**: paywalled or in-copyright books | — |
| Austin 1975, *Archery at the Dark of the Moon* | **Skipped**: Internet Archive lending copy only (`access-restricted-item: true`) | — |
| P.Oxy. LIII 3710 | **Not read** (§8) | — |

---

## 2. MacDonald 1967, "The Season of the Odyssey"

**Locator.** T. L. MacDonald, "The Season of the Odyssey", *J. Brit. Astron. Assoc.* 77 (1967), no. 5, pp. 324–327.
- ADS bibcode 1967JBAA...77..324M. The scan is 4 pages; the references end on p. 327, so the "324–328" in B&M ref. 34 and in DESIGN is one page long [read].
- Fetched from `http://articles.adsabs.harvard.edu/pdf/1967JBAA...77..324M`. The `https` URL gave a 504; `adsabs.harvard.edu/full/...` returns an empty HTTP 202, which is what blocked the earlier agent [bm §1].
- sha256 51d2d7f6…9d93.

### 2.1 What it says, page by page

All paraphrase; quotes are under 15 words [read: macdonald].

- **p. 324.**
  - He paraphrases Od. 5.270–277: Calypso told Odysseus to keep the Bear on his left as he sailed east, and he watched the Pleiades, late-setting Boötes, the Bear and Orion. He poses the question of what season that implies.
  - He reports the earlier answers. Finsler and Wilamowitz put the voyage between the end of the first week of October and the third week of November. Scott put it between 30 August and 19 September.
  - He computes for 1000 BC, taking the sack of Troy as 1184 BC (Eratosthenes) or 1160 BC. He tabulates star positions from Neugebauer's tables for AD 1900 and 1000 BC: Alcyone, Rigel, Betelgeuse, Arcturus, Polaris, Dubhe, Merak. Arcturus is at declination +36.64° in 1000 BC, against +19.70° in 1900.
  - On ὀψὲ δύοντα he rejects "slowly setting": ὀψέ always connotes lateness.
- **p. 325.**
  - From Neugebauer's tables and Schoch's Babylonian arcus visionis (4° to 17°), he computes the annual phenomena.
  - **Early September:** the Pleiades are visible all night, with achronycal rising about 20 Sep. Arcturus is visible only an hour or two after sunset, with heliacal rising about 12 Sep. So "late or slow setting would be the merest poetical epithet".
  - **October–November** is worse for Arcturus. The Pleiades' cosmical setting is 1 Nov.
  - **His proposal:** the Pleiades mark the direction of sunset as twilight fades, and Arcturus, setting late, the opposite direction of sunrise. This is the sentence B&M quote.
  - **Spring:** from March to June Boötes is visible all night. In March the Pleiades are visible about four hours after sunset. Their heliacal setting is about 3 Apr and their heliacal rising 19 May.
  - Conclusion, in his words: "It is therefore suggested that Odysseus was making his perilous journey in March."
- **p. 326.**
  - Hesiod WD 385–387: the Pleiades are hidden forty days. He remarks that the agreement may confirm the calculation more than the poet.
  - WD 663: sailing fifty days after the solstice. WD 678ff: spring sailing, which Hesiod does not praise. "And in fact Odysseus was shipwrecked."
  - Nothing in the Odyssey contradicts March, he says; "The indications are vague." Gilbert Murray thought it winter, from the fires. Others objected to October because Telemachus' journey suggested high summer.
  - Od. 1.16: the year of return has come. Athena would not wait until August or October.
  - Poseidon is among the Ethiopians in Hesiod's Lenaeon, January–February (WD 504–505, 527).
  - At Od. 5.282 Poseidon, returning, sees Odysseus. He asks whether this "would be imaginative to think of" as the equinox. If so, the action starts about 22 Feb and the shipwreck is about 21 Mar. Since the epic needs fewer than 45 days, the slaughter falls about the end of the first week of April.
  - Then: "This is where coincidence takes a hand." Theoclymenus (Rieu's translation of Od. 20.351–357); Dörpfeld's Hades reading; Plutarch's eclipse reading.
- **p. 327.**
  - New Moon: 14.457, 14.161 and 19.306.
  - "Schoch and Neugebauer took up the idea": only one eclipse was total over the Ionian Islands; the line of totality crossed Leucas; 16 April 1178 BC.
  - A one-week shift of his timetable and of Poseidon's return, "needed in any case for New Moon", reaches the eclipse.
  - 11.45 a.m. local time suits the text.
  - Just before Theoclymenus speaks, the suitors' faces change and their food seems spattered with blood (Od. 20.345–349; the line numbers are mine). So, he says, the effect was not limited to the seer.
  - Schoch "bowed to Dörpfeld's authority", adding that 18.366 shows "winter and not April". MacDonald answers with the reaping match and Hesiod's Pleiades return in the second half of May.
  - Venus at 13.93: by Neugebauer's tables, greatest morning elongation on 17 March "1176 B.C." (see §2.5).
  - He closes: "I am very far from thinking that anything is proved."
  - References: Rieu; the Loeb Homer and Hesiod; Plutarch, *De facie* ch. 19; P. V. Neugebauer, *Astronomische Chronologie* (Berlin 1929) and *Tafeln zur Astronomischen Chronologie* (Leipzig, 1912–1925); C. Schoch, *Die Sterne* 6, 88, and *Die sechs griechischen Dichter-Finsternisse* (privately printed); W. Dörpfeld, *Die Sterne* 6, 186–7.

### 2.2 The season he argues for, and from which lines

- **March, for the voyage from Ogygia.** The primary ground is Od. 5.270–277: the stars, "late setting" read as lateness, and the navigational logic of sunset against sunrise [p. 324–325].
- **Supporting grounds.**
  - Hesiod's spring sailing, WD 678ff, and the shipwreck [p. 326].
  - Od. 1.16, the year of return [p. 326].
  - Poseidon among the Ethiopians (Od. 1.22ff) read as Hesiod's Lenaeon [p. 326].
  - Poseidon's return at Od. 5.282 read as the equinox [p. 326].
- **For the slaughter:** about the end of the first week of April by his timetable, or 16 April after the one-week shift [p. 326–327].
- **B&M's report is accurate.** B&M write that he "supported" March sailing in "a lucid short paper", and quote his p. 325 sentence [bm2008.txt, around lines 169–176].
- B&M's equinox conjecture (E) is MacDonald's p. 326, as they say [bm2008.txt, around lines 156 and 243].

### 2.3 The reaping match: B&M and Gainsford, settled from the primary

- **Gainsford says** MacDonald "has argued for a setting in the second half of May", from Od. 18.366–370 and Hesiod WD 383–384 (11 May). He objects that the ploughing match at 18.371–375 would give November by the same logic [gainsford2012.txt, around line 71, n. 20].
- **The primary says otherwise** [p. 327]. MacDonald brings in 18.366 only to rebut Schoch's claim, which he quotes: "according to 18, 366, it was winter and not April". He replies that the reaping match points to the late-May Pleiades return, so not to winter.
  - He does not offer May as his season.
  - He does not reconcile the May hint with his April slaughter.
- **Gainsford's ploughing point stands against the use of 18.366 as a season marker by anyone.** But his description of MacDonald's position is wrong, and so is his page ("217" for p. 327).
- **Gainsford also dates the eclipse "26 April 1178"** in his summary and opening sentence [gainsford2012.txt, lines 5–6], while his n. 1 says dates are Julian. Julian 16 Apr −1177 is Gregorian 5 Apr, so neither calendar gives 26 April [computed: jd_checks.py; ephem.jd_from_julian docstring]. **Treat Gainsford's dates and locators as secondary, to be checked.**
- **What the text says** [read: odyssey-grc.tsv 18.366–377; odyssey-murray.tsv 18.365].
  - 18.366–370 is a wish: "if only" a contest could be held ὥρῃ ἐν εἰαρινῇ, ὅτε τ᾽ ἤματα μακρὰ πέλονται ("in spring, when the days are long"). The contest is mowing grass (ἐν ποίῃ) with a sickle (δρέπανον); it is not explicitly a grain harvest.
  - 18.371–375 wish for a ploughing match.
  - 18.376–377 for a war "today" (σήμερον).
  - Line 18.367 recurs as a simile at 22.301, so it is formulaic.
  - Schoch (per MacDonald) and Papamarinopoulos 2012 read the wish as implying "not now". MacDonald reads it through Hesiod. **None of these readings is forced, and the bench should not use 18.366 as a clue** [inference; DESIGN H10 already excludes similes].

### 2.4 Was the season clue C formed without the eclipse in view?

**Evidence.**
1. **Schoch 1926 derived April from the eclipse.**
   - He searched −1240 to −1140 for a total eclipse between 10 a.m. and noon, with no season constraint [read: schoch-1926-observatory.pdf, p. 20].
   - He then dated the landing on Scheria to the beginning of April −1177, the landing on Ithaca to 12 Apr, and the slaughter to 16 Apr [p. 21].
   - So the first spring placement of the action in the modern literature is a consequence of the eclipse.
2. **Schoch himself later read 18.366 as winter** [secondary: MacDonald p. 327]. The eclipse's discoverer did not hold a star-based spring reading.
3. **Every earlier season reading that MacDonald surveys is autumn or winter** [read: macdonald p. 324, 326]. The scholia read autumn turning to winter [txt §5.6].
4. **MacDonald 1967 is the first spring reading of 5.272 that B&M cite. It was written 41 years after Schoch, by an author who cites Schoch's two 1926 eclipse papers and Neugebauer 1929** [p. 327 references].
   - The paper presents the stars first and the eclipse as "coincidence" [p. 326]. That is the order of the argument; it does not establish the order of discovery [inference].
   - His timetable is then shifted a week to meet 16 April [p. 327].
5. **His Venus check is in the eclipse year** [§2.5; computed]. That shows he was assembling the clue set around 1178 BC.

**Verdict** [inference]. Nothing documents an eclipse-blind spring reading of Od. 5.272.
- Before Schoch the readings were autumn.
- The spring date of the action was first a product of the eclipse (Schoch 1926).
- The only spring star reading B&M cite was published by an author who had the eclipse in his references and fitted his timetable to it.
- MacDonald's star argument has internal reasons of its own (the sunset and sunrise logic, "late" read as lateness). The documents cannot show what he would have concluded without the eclipse. They can show that he did not write without it.
- **So conditioning on C, as DESIGN §3.2 does, is the reading the record supports.** Critique issue 6's twelve-fold "understatement" holds only under a counterfactual (C independent of the target) for which there is no document. Its fix 1, reporting both figures with the reason frozen, remains right.

### 2.5 MacDonald's other numbers, checked

- **Venus.** He writes "greatest morning elongation in 1176 B.C. on March 17" [p. 327].
  - DE441 gives morning (western) greatest elongations on 16 Mar −1177 (46.14°) and 17 Oct −1176. Evening ones fall on 29 May −1176 and 4 Jan −1174. There is none in −1175 = 1176 BC [computed: venus_elongation_check.py → venus_elongation_check.txt; geocentric, UT].
  - **His date matches 1178 BC to within a day.** Either "1176" is a misprint or slip for 1178, or he wrote an astronomical year loosely [inference].
  - On B&M's Ti−5, 11 Apr −1177 at 03:00 UT, Venus is 44.3° west of the Sun [same script].
- **Pleiades.** His heliacal setting "about April 3" is for 1000 BC with Schoch's arcus visionis [p. 325]. B&M's "latest night … 3 April" is for −1177 at nautical twilight and 2° [bm §5 C]. The visibility note reproduces B&M's 3 Apr independently [vis §3, table at line 383]. **The match of numbers is therefore not evidence that B&M copied MacDonald** [inference].
- **The B&M quotation.** MacDonald's sentence says "late or slowly setting Arcturus" [p. 325], although on p. 324 he rejects "slowly" as a sense of ὀψέ. B&M quote the sentence as printed.

---

## 3. Schoch and P. V. Neugebauer

### 3.1 Schoch 1926, *The Observatory* 49:19–21, re-read for the season question [read: data/refs/schoch-1926-observatory.pdf]

- **p. 20.**
  - Schoch revised the Moon's and Sun's secular terms: +12.24″ s² in the Moon's mean longitude and +2.64″ s² in the Sun's. He used Oppolzer's *Syzygientafeln* corrected throughout.
  - He searched −1240 to −1140 and found that "the total solar eclipse of −1177, April 16 … can alone be taken into consideration".
  - He gave a timetable of the day, with the warning at 11.41 local mean time.
- **p. 21.**
  - It is the only eclipse between 10 a.m. and noon. The southern limit of totality runs through Ithaca. The annular eclipse of −1182 Jan 12 is rejected (11.4 digits, 14 minutes after sunrise).
  - New Moon from 14.161–162 and 19.306–307.
  - His restored chronology: landing on Scheria at the beginning of April −1177, landing on Ithaca on −1177 Apr 12, slaughter on −1177 Apr 16, 6 to 8.30 p.m.
- **Bearing.** There is no season clue in Schoch's search. The season follows from the eclipse (§2.4 item 1).

### 3.2 Neugebauer & Schoch, "Zur astronomischen Chronologie", *Astron. Nachr.* 230 (1927) cols. 57–64 [read: data/refs/neugebauer-schoch-1927-an-230-57.pdf; ADS 1927AN....230...57N]

- The note is not about the Odyssey. Neugebauer reviews Schoch's booklet *Die säkulare Akzeleration des Mondes und der Sonne* (Selbstverlag, 1926). He says it gives the foundations only briefly, and asks Schoch to publish all his data.
- Neugebauer reports an empirical solar acceleration of +1.49″ s², almost exactly Fotheringham's 1.50. He then gives corrections to his own tables to bring them to Schoch's elements: Tabelle 1, by Julian year from −4000.
- He also corrects his heliacal arcus visionis values for Mercury: appearance in the west 11°, disappearance in the west 11.7°, appearance in the east 13.8°, disappearance in the east 10° [col. 60].
- Schoch adds heliacal rising and setting dates at Babylon for α Per, δ CMa and Deneb, from his 1924 arcus visionis paper.
- Schoch gives corrections to Schram's cycle tables (Tabelle 2).
- **Bearing** [inference].
  - The elements behind Schoch's January 1926 "southern limit through Ithaca" were revised within a year.
  - Neugebauer's contemporary remark that Schoch had not published his data is a caution on how far the 1926 track can be trusted. The dossier already found that the canon puts the limit about 90 km north of Vathy [research-critiques §0 item 1].
  - The Mercury values are a period alternative to the bench's 10° (Ptolemy) arcus visionis for F5 [DESIGN §8 item 4].

### 3.3 Neugebauer, death notice of Carl Schoch, *Astron. Nachr.* 237 (1929) cols. 221–222 [read: first scan page only; ADS 1929AN....237..221N]

- Schoch was born 5 March 1873 and died 19 November 1929. He worked as an insurance mathematician, went to Oxford in 1922 to work with Fotheringham on Babylonian texts, and joined the Astronomisches Rechen-Institut in 1926.
- His main work, Neugebauer says, was the 1926 elements for Sun and Moon in *Die säkulare Acceleration*, the corrected Schram eclipse tables (*Sirius* 59, 1926), and the revision of Oppolzer's *Syzygientafeln*.
- **Schoch never gave an exhaustive discussion of the material he used.** He meant to in summer 1929 but died first.
- The Odyssey is not mentioned on this page. The notice continues on the next scan page (col. 223), which I did not retrieve: the ADS PDF for this bibcode has one page.

### 3.4 P. V. Neugebauer, *Astronomische Chronologie* (de Gruyter, Berlin 1929): not read

- **Access.** De Gruyter has digitised it: DOI 10.1515/9783111497990 (Text) and 10.1515/9783111498003 (Tafeln). The PDFs are paywalled, and scripted requests get an empty HTTP 202 (a bot check).
- HathiTrust has a catalog record, 001475387, "Multiple Items". Its viewability is unknown because the record page stalled on a Cloudflare security check in the browser, which I did not try to pass.
- A 1929 publication may be open in the US [inference: US copyright term], so **Jon could open it in his own browser.**
- **Where to look.** The Crossref table of contents is in `results/unread-primaries/neug_toc.txt`:
  - ch. XI, "Beispiel für die astronomische Behandlung eines Textes", pp. 28–31;
  - §13, "Allgemeine Orientierung über Finsternisse", pp. 95–109;
  - §14, "Berechnung einer Finsternis nach den hier gegebenen verbesserten Tafeln von Schram", pp. 109–133.
- If Neugebauer worked the Odyssey eclipse as an example, it will be in one of these [inference].
- What it contains on the Odyssey is still known only through B&M's abstract and MacDonald p. 327 [secondary].

### 3.5 Other Schoch and Dörpfeld items

- ADS indexes only four Schoch items for 1920–1932: 1924 MNRAS 84:731, 1924 AN 222:27, 1926 Obs 49:19 and 1928 MiABe 2. *Die Sterne* is not indexed.
- I found no online copy of *Die Sterne* 6:88 or 6:186–187, nor of *Die sechs griechischen Dichter-Finsternisse*.
- Schoch's "winter and not April" from 18.366 is known only through MacDonald p. 327 [secondary].
- **Found in passing, not obtained.**
  - Hlad, O. (1970), "Odyssey and the solar eclipse of −1178", *Říše hvězd* 51:171–172 (ADS 1970Rise...51..171H; no scan).
  - Guglielmino, Cipolla & Rizzo Giudice (2017), "Astronomy in the Odyssey: the status quaestionis", Springer ASSP 48:165, which cites MacDonald or Schoch [ADS citation search].
  - Pogo, "Carl Schoch (1873–1929)", *Isis* 15 (1931) 163–169, an obituary with a probable bibliography (JSTOR) [Crossref].

---

## 4. Papamarinopoulos et al. 2012, "A new astronomical dating of Odysseus' return to Ithaca", *MAA* 12(1) 117–128

**Locator.** St. P. Papamarinopoulos, P. Preka-Papadema, P. Antonopoulos, H. Mitropetrou, A. Tsironi and P. Mitropetros.
- Received 31/10/2011; the accepted date is printed as 02/12/2012.
- Read from the published PDF (12 pages, MAA page heads, "Copyright © 2012 MAA") posted at `https://www.friendsofhomer.gr/wp-content/uploads/2016/11/Odysseus-Omega.pdf`. The MAA's own copy is at `https://www.maajournal.com/index.php/maa/article/view/587/518`, behind a Cloudflare challenge for scripts.
- Text in `data/refs/pap2012.txt`. Page numbers below are journal pages.

**What it says** [read: pap2012.txt].
- **p. 118.**
  - Papamarinopoulos (2008) and B&M (2008), "independently to each other", had proposed 16 Apr 1178 BC (JD 1291264), as had Schoch 1926.
  - All three "ignored" other diagnostic information in the poem.
- **p. 119, Tables 1–2.** Ancient Troy dates via Clement: Douris 1454 or 1514; Cleitarchus and Timaeus 1274 or 1334; Eratosthenes 1184, 1228 or 1288; Ephorus 1189 or 1249; Phanias 1169 or 1229; Herodotus about 1250; Dicaearchus 1212; Parian Chronicle 1208; Sosibius 1171. Archaeologists' dates for Troy VI and VIIa follow.
- **p. 120.**
  - **Window:** 1300–1130 BC. The lower bound is chosen for Achaean power. The upper is extended by 41 years "to include" the palaces' destruction.
  - **Eclipse list:** Jubier's site, from the Five Millennium Canon (VSOP87D and ELP-2000/82), gives 64 eclipses visible from the Ionian islands.
  - **Season cues** are listed for autumn. Cold: 5.467–469, 14.518–522, 14.529–533, 14.457–458, 17.23–25, 17.190–191. Plants: 13.196, 14.353 and 24.221–344. Animals: 14.410–414, 17.170–171, 15.397. Long nights: 15.391–394, ἀθέσφατοι. Habits: spinning.
- **p. 121.**
  - They read 18.366–367 and 22.301 as contrasts: spring has long days, but now the nights are long, so it is autumn.
  - Only 14 of the 64 eclipses fall in September–November.
  - New moon from 14.161–162, 19.306–307 and 14.457.
  - Venus visible in the east five days before (13.93–95).
  - Pleiades, Boötes, the Bear and Orion visible all night (5.270–277). Their joint presence occurs in spring and autumn, "however the spring's case is invalidated".
  - Five eclipses pass the Venus test. Three (1298, 1252, 1234 BC) are "not practically visible". 1143 BC is rejected because the palace system had collapsed.
- **p. 122, Table 3.** The 1207 BC annular eclipse: 30 Oct, JD 1280869, 75% obscuration.
  - Times in LT, "equal to Universal Time (UT)+2 hours": begins 14:30, maximum 16:00 (Sun 20° up), ends 17:25.
  - ΔT 29,136 s ± 1,077 s from the canon, after Morrison & Stephenson 2004.
  - Sunset 17:58 LT.
  - Table 3 also prints 1143 Nov 11, maximum 07:58 LT, 51.5%. The "0.82 %" and "1.92 %" for 1298 and 1252 BC are as printed.
- **p. 123–124.**
  - Starry Night 6 Pro Plus "uses" ΔT 29,300 s, 164 s from the canon.
  - Return on 25 Oct 1207 BC (JD 1280864): Venus rises 05:13 LT, the Sun 06:50 LT, Venus at magnitude −3.94 and 18° up.
  - They read "late-setting Boötes" as Boötes failing to set: β and γ Boo are circumpolar at their latitude, so it sets "slowly but in reality it doesn't completely" (Fig. 3, at Palermo).
- **p. 124–126, against B&M.**
  - Nights after the vernal equinox are short. Night length on 14 Apr 1178 BC is about 11 h, against about 13 h on 30 Oct 1207 BC.
  - Noon is "dinner", while the slaughter is at late afternoon "supper" preparation (21.428–429).
  - B&M's own 4 Apr Pleiades heliacal setting falls before the sinking.
  - B&M omit Orion.
  - Mercury's station is "ordinary".
  - For Poseidon they offer the 50% partial lunar eclipse of 15 Oct 1207 BC, 05:30 LT.
  - Autumn equinox: 4 Oct 1207 BC (JD 1280843).
- **p. 127.** Acknowledgement to William Mullen for suggesting that they study the seasonal details.

**Checks** [computed: jd_checks.py].
- Every JD label in the paper converts to the Julian date it is attached to: 1280869 = 30 Oct −1206, 1280864 = 25 Oct, 1280843 = 4 Oct, 1280854 = 15 Oct, and 1291264 = 16 Apr −1177. Their dates are proleptic Julian, astronomical year −1206.
- Their 16:00 LT (UT+2) is 14:00 UT, which is 15:23 LMT at Vathy (UT + 1 h 22 m 52 s [research-critiques conventions]). That agrees with the dossier's computed 15:26 LMT maximum [research-critiques.md, eclipse table, line 418]. **The "~16:00 local" in the dossier is a zone time, not LMT.**

**Bearing on the bench** [inference].
1. **It is a documented autumn reading of the same clue C.** It shows that C's season is an analyst's choice in both directions. F3's autumn branch, and the critique's request to test the autumn mirror, have a published precedent.
2. **The first author moved from 16 Apr 1178 BC (2008) to autumn (2012)** after a colleague's suggestion to read the seasonal lines. A season clue that flips with the analyst cannot be treated as a datum independent of the target.
3. **Its search is itself a forking path.** It fixes the window to 1300–1130 BC, cuts on season, Venus and "practical visibility", and drops 1143 BC on archaeology. It is a natural rival chain for N3's garden, and 30 Oct 1207 BC is already a listed date [DESIGN §8 item 19].
4. **ΔT data point for Starry Night** (§7).

---

## 5. Henriksson 2012, "The Trojan War dated by two solar eclipses", *MAA* 12(1) 63–76

**Read** in the journal's pdf.js viewer; extract with page locators in `data/refs/henriksson2012-extract.txt`.

- **Claim.** Il. 17.366–377, darkness over the fight for Patroclus' body under a clear sky elsewhere, records a total eclipse at Troy near the southern limit of totality. Of four eclipses of magnitude above 0.990 at Troy in 1000–2000 BC, only 1312 BC fits: 12:35:24 LMT, magnitude 1.002 at Troy, limit 7.4 km south [p. 65, Table 1].
  - A 2011 recalibration moves the limit 400 m south and the time to 12:36:08 [p. 66].
  - The Shield of Achilles' constellations (Il. 18.484–489) are read as the sky seen during totality [p. 67].
  - A second eclipse, 1335 BC in the tenth year of Mursili II and partial 0.89 at Hattusa (Schoch's identification), anchors the Hittite chronology [p. 71].
- **Method.** Schoch's 1931 formulas, with a ΔT parabola coefficient of 36.28 s/cy² against Stephenson & Morrison's 31.0 [p. 66, 68]. He argues against Stephenson's approach [p. 68–69].
- **Calendar.** He says all dates are Gregorian [p. 65].
  - The canon lists the eclipse as −1311 Jun 24, Julian [results/research-critiques/ionian_eclipses.csv], which is proleptic Gregorian **12** Jun.
  - The canon's −1334 Mar 13 is Gregorian **1 Mar**, while he writes "February 28 (March 13 Julian)".
  - So his Gregorian labels run one day early, consistently [computed: jd_checks.py]. **Use the Julian dates: 24 Jun 1312 BC and 13 Mar 1335 BC.** The dossier's "24 Jun 1312 BC Julian" [research-critiques line 380] is right.
- **Bearing** [inference].
  - The paper has nothing on the Odyssey or its season.
  - It matters only for window sensitivity (N5): a Troy of about 1312 BC puts Odysseus' return about 1302 BC, outside B&M's 1250–1115 BC window.
  - It also matters for the date list, where Papamarinopoulos 2014 already gave the implied 17 Nov 1301 BC [research-critiques line 419].

---

## 6. PLSV internals (Lange & Swerdlow)

**Locator.** "Computation of Visibility Phenomena" and "Sources of Computations and Cautions concerning Accuracy", PLSV 3.1 documentation.
- Live site 404 on 2026-10-04. Read from Wayback captures:
  - `http://web.archive.org/web/20200714181118/http://www.alcyone-ephemeris.info:80/plsv/documentation/compphen.html`;
  - `.../web/20200614175725/http://www.alcyone-ephemeris.info:80/plsv/documentation/accuracy.html`.
- Text in `data/refs/plsv-doc-*.txt`.
- **B&M used version 3.0; this documents 3.1.**
- An installer `plsv31.exe` is archived; I did not download or run it.

**What it says** [read].
- **Ephemeris.** Moshier's, close to DE404 and corrected toward DE406. Stars come from the Yale Bright Star Catalogue (J2000 and proper motion). The bundled star list includes stars only to magnitude 2.5 [compphen].
- **ΔT** is from Chapront-Touzé & Chapront (1991) [accuracy].
- **Visibility test.** On each day, the object is "possibly visible" when it is above a **critical altitude** while the Sun is at least the **arcus visionis** below the horizon [compphen]. The critical altitude is "the least altitude at which the planet can be seen due to atmospheric extinction and irregularities in the horizon". The default is 0°, adjustable per object [compphen, accuracy].
  - **There is no extinction or sky-brightness model.** The authors write that changing the critical altitude moves dates more than reasonable changes of the arcus visionis [accuracy, summary].
- **Arcus visionis defaults** [accuracy].
  - Fixed planetary values are Schoch's (1928). For Mercury: EF 10.5°, EL 11°, MF 13°, ML 9.5°.
  - Variable: AV = 10.5 + 1.4 m for heliacal phenomena, and AV = 8.9 + 1.1 m for acronychal rising and cosmical setting.
  - Stars use the same two formulas. For example, magnitude 0.0 gives 10.5° heliacal and 8.9° acronychal; magnitude 3.0 gives 14.7° and 12.2°.
- **Lunar first visibility:** lower-limb altitude plus 1/3 of the Moon–Sun separation ≥ 11.3° [compphen].

**Bearing** [inference].
- DESIGN §8 item 4 says "PLSV's extinction parameters unknown". **There are none.** B&M's "standard magnitude-corrected parameters" [bm §Method] should be read as the variable AV formulas, with their stated critical altitudes of 1° for Mercury and 2° for the Pleiades. T0b can now emulate PLSV directly.
  - For Mercury's morning first visibility, AV = 10.5 + 1.4 m. At the m = +0.65 to +0.8 of 11–14 Mar −1177 [bm §5 M], that is about 11.4–11.6°.
  - The date then depends mainly on when Mercury brightens past that line at 1° altitude.
- B&M say they used PLSV "for atmospheric extinction calculations" [bm2008.txt, around line 204]. PLSV does not compute extinction, so that phrase means the critical-altitude setting.
- For C, B&M state a nautical-twilight (−12°) test, not an AV test [bm2008.txt, around lines 176–181]. Alcyone (V ≈ 2.9) is not in PLSV's bundled star list, so the Pleiades must have been added by hand if PLSV was used for them.
- The visibility note already reproduces B&M's 17 Feb and 3 Apr with geometry alone [vis §3].

---

## 7. Starry Night's ΔT: a cross-check from two papers

[computed: deltat_checks.py → deltat_checks.txt]

| Date | Canon reported | Parabola −20 + 32u² | Parabola + canon ṅ correction | Starry Night reported |
|---|---|---|---|---|
| 16 Apr −1177 | 28,590 s [SEdata] | 28,716.9 s | **28,590.1 s** | 27,602.7 s (6.0.4, B&M) |
| 30 Oct −1206 | 29,136 s [Pap. 2012 p. 122] | 29,265.3 s | **29,136.2 s** | 29,300 s (6 Pro Plus, Pap. 2012 p. 123–124) |

- **The instrument checks out.** The script reproduces both canon values to 0.2 s from the Espenak–Meeus parabola and the canon's ṅ term, −0.000012932 (y − 1955)².
- **Starry Night 6 Pro Plus** sits 35 s above the bare parabola at −1206. It plausibly uses the Morrison & Stephenson 2004 parabola without the ṅ correction [inference].
- **Starry Night 6.0.4** sits 1,114 s below the same parabola at −1177. B&M say only that it computes ΔT "according to Meeus following Stephenson and Morrison" [bm2008.txt, around line 199].
- **One smooth ΔT(t) cannot give both values.** From 29,300 s at −1206 it would give about 28,752 s at −1177, which is 1,149 s more than B&M's.
- Either the versions differ, or a setting was changed, or one value is misreported [inference].
- **This supports DESIGN's handling** of 27,602.7 s as uninterpretable for eclipse geometry (§8 item 6). The bench should not try to "convert" it.

---

## 8. What I could not obtain, and why

- **P. V. Neugebauer 1929** (§3.4).
  - De Gruyter: paywall, and an empty 202 to scripts. WebFetch got 405.
  - HathiTrust: 403 to scripts and WebFetch. In the browser, the search results loaded (record 001475387), but the record page stalled on a Cloudflare "security verification" that I did not attempt.
  - Internet Archive has only Wislicenus's 1895 book of the same title.
- **P.Oxy. LIII 3710** (TM 60566).
  - papyri.info/dclp/60566 serves an Anubis bot-check page to scripts.
  - The browser tool refused the site as "not approved for tool access", so it is unread. If Jon approves papyri.info for the browser, or opens it himself, the DCLP record may carry the edition text.
- **Austin 1975.** Internet Archive item `archeryatdarkofm0000aust_h4d7` is lending-only (`access-restricted-item: true`). Not borrowed.
- **de Jong 2001 Appendix A, Stanford 1959, the Oxford commentaries:** in-copyright books, not openly available. Skipped.
- **Schoch's *Die Sterne* 6:88, *Dichter-Finsternisse*, and Dörpfeld's *Die Sterne* 6:186–187:** not in ADS, and no online copy found.
- **Starry Night internals:** commercial. §7 is the only constraint found.
- **Henriksson 2012's PDF and the MAA copy of Papamarinopoulos 2012:** Cloudflare-challenged for scripts. Henriksson was read in the browser; Papamarinopoulos came from the friendsofhomer.gr copy.

---

## 9. Bearing on the bench: proposed changes for the owners of DESIGN.md and critique-design.md

These are proposals only. I have not edited either file.

1. **Critique V13 / issue 6 / DESIGN §8 item 19.**
   - Replace "contested" with: "MacDonald 1967 read. He argues for March from Od. 5.270–277, with the 1178 BC eclipse in view (p. 326–327). Gainsford's 'second half of May' misreads his rebuttal of Schoch at p. 327."
   - Correct the page range to 324–327.
2. **p_fix (critique issue 6, fix 1).**
   - Keep "p_fix given C" as primary. Freeze the reason in the prereg: the spring reading of C first appears after, and alongside, the eclipse (§2.4).
   - Report the unconditional figure as the "C independent of the target" counterfactual. Do not report it as an understatement.
3. **The same provenance applies to V and E** [inference]. MacDonald paired 13.93 Venus with the eclipse year (§2.5) and invented the equinox reading of 5.282. Only M (Hermes = Mercury) is B&M's own, and B&M too knew the target. No clue in N∧C∧V∧M was formulated blind to 1178 BC. That belongs in N3's description of the garden.
4. **Use 18.366–370 for nothing.** It is a wish ("if only … in spring"), formulaic (= 22.301), and read as winter, May or autumn by different advocates (§2.3).
5. **PLSV emulation in T0b** (§6): AV = 10.5 + 1.4 m (heliacal), 8.9 + 1.1 m (acronychal and cosmical), a critical altitude of 1° for Mercury and 2° for the Pleiades, and no extinction. Neugebauer's 1927 Mercury values (morning first 13.8°) and Schoch's (MF 13°) are period alternatives for F5.
6. **Date list.** 30 Oct 1207 BC (Papamarinopoulos 2012) is confirmed from the primary. Its "16:00 local" is UT+2 zone time, which is 15:23 LMT at Vathy. Henriksson's Iliad eclipse is 24 Jun 1312 BC (Julian), not "11 June".
7. **Provenance hygiene.** Gainsford 2012 has at least three slips relevant here: MacDonald's position, MacDonald's page, and "26 April". Anything taken from him alone stays *secondary*.

---

## 10. Files and scripts

**Saved under `data/refs/`:**
- `macdonald-1967-jbaa-77-324.pdf` (ADS scan, 4 pp.);
- `papamarinopoulos-2012-maa-12-117.pdf` and `pap2012.txt`;
- `henriksson2012-extract.txt`;
- `neugebauer-schoch-1927-an-230-57.pdf`;
- `neugebauer-1929-an-237-221-schoch-obituary.pdf`;
- `plsv-doc-compphen.txt` and `plsv-doc-accuracy.txt`.

**Scripts and outputs in `results/unread-primaries/`:**
- `jd_checks.py` → `jd_checks.txt` (JD labels; Gregorian and Julian conversions);
- `deltat_checks.py` → `deltat_checks.txt` (canon and Starry Night ΔT);
- `venus_elongation_check.py` → `venus_elongation_check.txt` (Venus greatest elongations, DE441);
- `neug_toc.py` → `neug_toc.txt` (Crossref chapter list of Neugebauer 1929);
- `fetch.py` and `cr_search.py` (fetch helpers);
- scratch: raw HTML and PDFs, `genuth1992.pdf` (an ADS hit on Homeric astronomy, about Iliad comet imagery; not relevant).

**ADS searches run** (2026-10-04, ui.adsabs.harvard.edu):
- `author:"Neugebauer, P" year:1925-1931` (12 hits);
- `author:"Schoch, C" year:1920-1932` (4 hits);
- title searches on Odysseus/Odyssey/Homer with eclipse/season terms, 1900–2026;
- `citations()` of 1967JBAA...77..324M and 1926Obs....49...19S (3 hits: B&M 2008, Guglielmino et al. 2017, Simon 2026).
