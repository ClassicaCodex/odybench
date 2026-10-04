# Controls for the Odyssey-eclipse bench

Research note for `odybench`, written 2026-10-03.

**What this is.** A catalogue of *positive controls*, *hard cases* and *negative controls* for testing the method of Baikouzis & Magnasco (2008, PNAS 105:8823; "B&M"). Positive controls are ancient references to sky events whose dates are known independently. Negative controls are fictional or undatable texts with similar sky references. The note ends with a concrete design for a *fair* positive control for a multi-clue dating method (section 7).

**Provenance tags.** Every number and claim carries one:
- `[text: file ref]`: a line or section in a file I exported to `data/text/` from Jon's ClassicaCodex library (section 9). The ref is the CTS passage key with its URN prefix removed.
- `[NASA]`: the NASA *Five Millennium Catalog* of solar and lunar eclipses (Espenak & Meeus). These are the `SEcat5`/`LEcat5` century pages at eclipse.gsfc.nasa.gov, downloaded 2026-10-03 and kept as text in `results/controls/nasa/`.
- `[computed: script]`: computed by me with the scripts in `results/controls/`, using JPL Horizons (ephemeris DE441). The raw output is in `results/controls/*.out.txt`.
- `[secondary: ...]`: a secondary report, named. **I did not read** Stephenson 1997, Newton 1970, Fotheringham 1920, Jacoby 1941, Skutsch 1985 or any Loeb commentary. Where a claim rests on one of these, I say so.
- `[me]`: my own inference.

**Conventions.**
- Dates are in the proleptic Julian calendar. Each date is given as historical BC and as an astronomical year: 431 BC = −430, and 1 BC = 0.
- NASA's catalogue dates are the **TD date of greatest eclipse**. That can fall on the next calendar day from the local date. For example, the Syracuse lunar eclipse is NASA −412 Aug 28 01:15 TD, but local evening 27 Aug 413 BC.
- Local times are **local mean solar time (LMT) = UT + longitude/15**, in hours. They are not apparent solar time; the difference is at most ±16 min.
- ΔT = TT − UT. The values are NASA's catalogue values or Horizons' own default; each table says which.

---

## 0. Summary of findings

1. **Strong positive controls exist, and several are in the library.** Five sets are secure, independently dated, multi-clue and multi-event:
   - Thucydides' three eclipses (431, 424 and 413 BC);
   - Xenophon's *Hellenica* eclipses (406, 404 and 394 BC);
   - the Gaugamela complex: a lunar eclipse on 20 Sep 331 BC, the battle "on the eleventh night after", the Babylonian Astronomical Diary, and Pliny's two-site timing;
   - Pydna: a lunar eclipse on 21 Jun 168 BC, the battle the next day, and a Roman calendar date about 2.5 months off;
   - the *Almagest*'s dated eclipse triples, plus Venus and Mercury greatest-elongation records.

   All are in the library except the cuneiform material. All the dates check against NASA's catalogue `[NASA]`, and I computed local circumstances at the observing sites `[computed]`.
2. **The *Almagest* is the closest analogue of B&M's clue types.** It has lunar eclipses plus Venus and Mercury greatest elongations, all dated to the day.
   - Even this expert record is off from the true maximum elongation. Venus (Theon, *Alm.* X.1) is dated to evening of AD 132 Mar 8, **16 days after** the true greatest elongation (21 Feb, 46.04°). Mercury (*Alm.* IX.8) is dated to AD 134 Oct 2/3, **3 days after** the true maximum (29 Sep, 18.51°) `[computed: run_extra.py]`.
   - Venus stays within 0.5° of its maximum for about 21 days; Mercury for about 6 `[computed]`.
   - This is an empirical noise model for "turning-point" clues such as B&M's Mercury.
3. **Language does not measure magnitude.** Each phrase below is paired with the maximum magnitude I computed at the place of observation `[computed]`:

   | Text and phrase | Magnitude at the site |
   |---|---|
   | Plutarch, *Pel.* 31: darkness in daytime held the city | 0.67 |
   | Herodotus 9.10: the sun "was dimmed" | 0.60 |
   | Thucydides 2.28: a crescent sun, some stars seen | 0.88 |
   | Ennius: "and night", at sunset | ≈0.73 |
   | Archilochus: night out of midday | ≈1.00 |
   | Diodorus 20.5.5: stars seen everywhere | ≈1.00 |

   A darkness phrase such as Od. 20.356–357 therefore cannot by itself require totality.
4. **Single-clue identifications usually rest on chronology from outside the text.**
   - **Archilochus:** I find *two* eclipses total at Thasos, 14 Mar 711 BC (−710) and 6 Apr 648 BC (−647) `[computed]`. The choice of 648 rests on the Gyges synchronism, not on astronomy `[secondary: general literature, not read]`.
   - **Ennius/Cicero:** both 21 Jun 400 BC and 20 Mar 405 BC are sunset eclipses of magnitude about 0.73 at Rome `[computed]`. The choice depends on the model of the Roman calendar `[secondary: C. Bennett, Tyndale "Roman calendar" pages]`.
5. **Ancient authors attach real eclipses to the wrong event or year.** This is the direct analogue of the sceptic's reading of the Odyssey.
   - Herodotus 7.37 puts an eclipse at Xerxes' spring departure from Sardis, where none was visible. The candidates are 2 Oct 480 BC (−479), 17 Feb 478 BC (−477), or a lunar eclipse on 14 Mar 479 BC (−478) `[NASA; computed]`.
   - Plutarch, *Per.* 35, puts the eclipse of 431 BC at Pericles' expedition of 430 BC `[me, from the two texts]`.
   - Lucan 1.540–544 puts a midday darkness at the outbreak of civil war (Jan 49 BC). The nearest real eclipse is 7 Mar 51 BC (−50), magnitude 0.88 at Rome at 13:23 LMT, near midday as Lucan has it. Cassius Dio 41.14.3 lists a total eclipse among the same portents, and Gautschy's list assigns it to 51 BC Mar 7 `[secondary: Gautschy list; computed]`.
6. **Astronomically constructed dates date the method, not the event.**
   - Tarutius (Plutarch, *Rom.* 12.3–6) put Romulus' conception at a total solar eclipse in Ol. 2.1, Choiak 23. That converts to **24 Jun 772 BC (−771)** `[computed]`.
   - A real solar eclipse did occur that day (NASA 02917: partial, gamma 1.0495). At Rome it had magnitude 0.000–0.005, so it was not seen there `[NASA; computed]`.
   - Cicero, *Rep.* 1.25, says outright that earlier eclipses, back to the one "in Romulus' reign", were *computed backwards* from Ennius' eclipse.
7. **The ancient reception of Od. 20.356 is split.**
   - Plutarch, *De facie* 19 (931D–E), reads it as an eclipse. So does Heraclitus' *Homeric Allegories* (§73.2 in the export), citing Hipparchus. Both couple it with Od. 14.162 / 19.307 ("as the old month wanes and the new begins").
   - The Odyssey scholia say flatly that no eclipse occurred: it was Theoclymenus' prophetic vision `[text]`.
   - So B&M's coupling of eclipse and new moon is at least as old as Plutarch. It may inherit a Hellenistic reading rather than derive from the text.
8. **The formula problem.** Od. 5.273–275 (the Bear "which alone has no share in Ocean's baths") is word for word the same as Il. 18.487–489, the Shield of Achilles `[text: odyssey-grc 5.273–275; iliad-grc 18.487–489]`. Aeneid 1.744 = 3.516 shows the same repetition. Star lists in epic are formulaic, so a "Pleiades and Bootes" clue may be stock sea-lore rather than a night's observation.
9. **The ephemeris-dependent ΔT trap, and the Ithaca anchor.**
   - With DE441 via Horizons, the eclipse of 16 Apr 1178 BC (−1177) is **total at Ithaca only for ΔT ≈ 28,900–29,700 s**. NASA's ΔT (28,590 s) gives magnitude 0.975 at Ithaca, and Horizons' default (28,418 s) gives 0.961 `[computed: run_extra.py]`.
   - B&M's ΔT of 27,602.7 s was paired with ELP-2000/82, whose lunar ṅ is about −23.9″/cy². Converting it to a DE-type ṅ (about −25.8″/cy²) gives about 29,320 s, inside the totality band `[me, using NASA's ṅ correction (§2.3)]`.
   - **Never mix a ΔT value with a different ephemeris**: the error here is about 1,700 s.

---

## 1. How the catalogue entries are built

**Fields** for each entry:
- citation, and the line in the exported file;
- the event, its accepted date, and the place of observation;
- the local circumstances `[computed]`;
- the strength of the identification, and who established it;
- clue structure: single event, or multiple clues with day intervals;
- whether the text is in the library, with its EditionId.

**Strength grades.** These are my working scale, for weighting controls `[me]`:
- **A**: the event is unique for type, place and season. The year is fixed by chronology independent of the eclipse (archon or war-year counts, a dated campaign, a regnal date, a cuneiform diary). No serious alternative.
- **B**: accepted, but an astronomically viable alternative exists. Or the year comes partly from the eclipse itself (Thales, Archilochus, Ennius, De facie).
- **C**: contested. The identification depends on emending the text, displacing the event, or a ΔT assumption (Hdt 7.37, Pindar *Paean* 9, the Ugarit and Hittite cases).
- **D**: not an eclipse. The passage is a darkness motif, portent, prophecy or legend.

**Clue structure** codes:
- **S**: single event.
- **S+Y**: single event in a year-count frame.
- **M-d**: several clues linked by explicit *day* intervals, as B&M use for the Odyssey.
- **M-y**: several events linked by year intervals.

## 2. Method for the computed numbers

### 2.1 Global data
Eclipse identity, type, gamma, central path, TD of greatest eclipse and ΔT come from NASA's Five Millennium catalogue `[NASA]`. `results/controls/ecl.py` looks up rows by astronomical year and date.

### 2.2 Local circumstances
`results/controls/local.py` and `hz.py` work as follows:
- They request topocentric apparent RA/Dec and angular diameters of the Sun and Moon from the **JPL Horizons API**: ephemeris DE441, airless, observer at the given longitude and latitude, steps of 1–3 min.
- Magnitude is the fraction of the solar diameter covered: (r☉ + r☾ − separation)/(2r☉).
- Two values are reported: the maximum over the window, and the maximum while the Sun is up (airless elevation > −0.83°).
- For lunar eclipses the scripts report the Moon's altitude at NASA's time of greatest eclipse.
- Horizons reports its own ΔT (quantity 30, TDB − UT). For example, −430: 15,958 s, against NASA's 15,923 s.

**Other ΔT values are emulated by a longitude shift.** If ΔT is δ seconds larger, the same physical geometry is seen from longitude λ − δ·(360°/86164.1 s) `[me; this is the standard equivalence]`. This is how the "NASA ΔT" columns and the Ithaca ΔT scan were produced.

**Caveats** `[me]`:
- Magnitudes are only as good as ΔT. NASA estimates the standard error of ΔT at 622 s at −1000 and 1,900 s at −1500 (2.6° and 7.9° of longitude), and 431 s at −500 `[secondary: NASA, SEhelp/uncertainty2004.html]`.
- For classical-era controls the ΔT uncertainty is far smaller than for the Bronze Age.
- Sites are city centres. The Halys battle site and Polybius' camp in Mysia are approximate.

### 2.3 ΔT and the lunar secular acceleration ṅ
NASA states the following `[secondary: NASA SEhelp/deltatpoly2004.html]`:
- Its ΔT polynomials assume ṅ = −26″/cy².
- The Canon's ELP-2000/82 uses −25.858.
- The correction for that case is c = −0.000012932·(y − 1955)² s.

I generalise this to c = −0.000091072·(ṅ + 26)·(y − 1955)² `[me: linear scaling of NASA's formula]`. At y = −1177, moving from ṅ = −23.89 (original ELP-2000/82) to −25.82 (DE430/440 family) changes the ΔT that reproduces the same event by about 1,720 s `[me]`.

**Rule for the bench:** carry ΔT and ṅ together, as a pair, wherever ΔT appears.

---

## 3. Positive controls: summary table

All dates are proleptic Julian. "Local" is computed at the stated site with NASA's catalogue ΔT `[computed]`; the Horizons-ΔT figures differ by ≤0.01 unless noted. Columns:
- **Str**: strength grade (section 1).
- **Clues**: clue-structure code (section 1).
- **Lib**: ClassicaCodex EditionId (Greek or Latin original first); "—" means not in the library.

| # | Citation | Event | Date (BC / astr.) | Site | Local circumstances [computed] | Str | Clues | Lib |
|---|---|---|---|---|---|---|---|---|
| P1 | Thuc. 2.28 | solar, "after midday", crescent, some stars | 3 Aug 431 BC / −430 Aug 03 | Athens | mag 0.877 at 17:34 LMT, Sun 17° | A | S+Y | 14 (13 Crawley) |
| P2 | Thuc. 4.52.1 | solar near new moon, start of summer | 21 Mar 424 BC / −423 Mar 21 | Athens | mag 0.703 at 08:43 LMT | A | S+Y | 14 |
| P3 | Thuc. 7.50.4 (+Diod. 13.12.6, Plut. *Nic.* 23) | lunar, full moon, then the "thrice nine days" wait | 27 Aug 413 BC (local evening) / NASA −412 Aug 28 01:15 TD | Syracuse | greatest 21:56 LMT, Moon 32° up; total (umbral mag 1.08) | A | M-d | 14, 952, 133 |
| P4 | Xen. *Hell.* 1.6.1 | lunar, "in the evening" | 15 Apr 406 BC / −405 Apr 15 | Athens | greatest 20:49 LMT, Moon 26°; total | A (eclipse); the year heading may be a gloss | S+Y | 832 (831) |
| P4b | Xen. *Hell.* 2.3.4 | solar, Lycophron's battle | 3 Sep 404 BC / −403 Sep 03 | Pherae | mag 0.77 at 08:34 LMT | B | S+Y | 832 |
| P4c | Xen. *Hell.* 4.3.10 | solar, "the sun appeared crescent-shaped" | 14 Aug 394 BC / −393 Aug 14 | Coronea | mag 0.91 at 09:34 LMT | A/B | S | 832 |
| P5 | Hdt. 1.74.2 (+Pliny *NH* 2.53) | solar, day turned to night in battle; Thales | 28 May 585 BC / −584 May 28 | Halys (approx. 39.5N 34E); Miletus | mag 0.974 at 18:14 LMT (Halys), 0.972 (Miletus) | B | S | 687 (686); Pliny 2056 |
| P6 | Hdt. 9.10.3 | solar, "dimmed" | 2 Oct 480 BC / −479 Oct 02 | Isthmus | mag 0.60 at 13:35 LMT (annular) | A/B | S | 687 |
| P7 | Archilochus fr. 122 W | solar, "night from midday" | 6 Apr 648 BC / −647 Apr 06 | Thasos; Paros | Thasos 1.000 (NASA ΔT) / 1.004 TOTAL (Horizons ΔT) at 09:50 LMT; Paros 0.992 | B | S | — (Aristotle *Rhet.* 3.17.16 quotes only the first words: 1236) |
| P8 | Plut. *Pel.* 31.2–3; Diod. 15.80.2–3 | solar at Pelopidas' departure | 13 Jul 364 BC / −363 Jul 13 | Thebes | mag 0.67 at 09:16 LMT | A | S+Y | 99 (98); 952 |
| P9 | Diod. 20.5.5 (Justin 22.6.1) | solar, total, stars everywhere, the day after Agathocles escaped | 15 Aug 310 BC / −309 Aug 15 | at sea off Syracuse | Syracuse 0.995 at 07:39 LMT | A | M-d (escape, then eclipse "next day") | 954 |
| P10 | Livy 44.37.5–8; Plut. *Aem.* 17.7–11; Pliny *NH* 2.53 | lunar, predicted by Sulpicius Gallus; battle of Pydna next day | 21 Jun 168 BC / −167 Jun 21 | Pydna | greatest 20:09 LMT, Moon 5.9° up; total (umbral 1.25) | A | M-d + Roman date | 1855 (1854); 95; 2056 |
| P11 | Livy 37.4.4 | solar, Roman date *a.d. V Id. Quinct.* | 14 Mar 190 BC / −189 Mar 14 | Rome | mag 0.919 at 07:20 LMT | A | S + Roman date | 1855 |
| P12 | Livy 38.36.4 | darkness "between the third and fourth hour" | 17 Jul 188 BC / −187 Jul 17 | Rome | mag 0.993 at 06:16 LMT (see note) | B | S | 1855 |
| P13 | Cic. *Rep.* 1.25 (Ennius *Ann.*) | solar at sunset, "Nonis Iunis" | 21 Jun 400 BC / −399 Jun 21 (alternative: 20 Mar 405 BC / −404 Mar 20) | Rome | 400 BC: 0.717 while the Sun is up (sets eclipsed); 405 BC: 0.748 at sunset | B/C | S + Roman date | 1756 |
| P14 | Plut. *De facie* 19 (931D–E) | solar, near-total, many stars, "beginning just after noon" | 20 Mar AD 71 | Chaeronea | mag 0.979 at 10:58 LMT | B | S | 371 (369 Cherniss) |
| P15 | Plut. *Alex.* 31.4; Arrian 3.7.6, 3.15.7; Curtius 4.10.2; Pliny *NH* 2.180 (=2.70.3 in export); Babylonian Astronomical Diary | lunar; battle 11 nights later | 20 Sep 331 BC / −330 Sep 20 | Arbela/Gaugamela | greatest 21:18 LMT, Moon 36° up; total | A | M-d, plus a 2-site timing | 151, 1186, 1844, 2056 |
| P16 | Polyb. 5.78.1 | lunar, Attalus' Gauls refuse to march | 1 Sep 218 BC / −217 Sep 01 | Mysia (approx.) | greatest at 18:17 LMT with Moon −4° (rose already eclipsed; totality 93 min [NASA]) | A/B | S | 1447 (1446) |
| P17 | Plut. *Dion* 24.1 | lunar at Zacynthus departure | 9 Aug 357 BC / −356 Aug 09 | Zacynthus | partial (umbral 0.19); greatest 19:19 LMT, Moon 1.7° | A/B | S | 177 (176) |
| P17b | Plut. *Dion* 19.4 | solar predicted by Helicon | 12 May 361 BC / −360 May 12 | Syracuse | mag 0.96 at 17:39 LMT | B | S | 177 |
| P18 | Assyrian Eponym Chronicle (eponym Bur-Saggile, month Simanu) | solar | 15 Jun 763 BC / −762 Jun 15 | Assur; Nineveh | Assur 0.953, Nineveh 0.982 at about 10:45 LMT | A | S+Y | — |
| P19 | Ptolemy, *Almagest* IV.6, IV.11, IX.8, X.1 | Babylonian and Alexandrian lunar eclipse triples; Venus and Mercury elongations | see section 4.19 | Babylon; Alexandria | all match NASA rows | A+ | M-d (exact day and hour intervals) | 2977 |

**P12 note.** My computed maximum, 06:16 LMT, comes about 1–2 h before Livy's "third to fourth hour" `[computed; me]`. This is unresolved: either a time-of-day error in the report, or the identification is wrong.

---

## 4. Positive controls: details

### 4.1 Thucydides 2.28 (P1)
- **Text.** "The same summer, at new moon by lunar reckoning (the only time it seems possible)". The sun failed after midday and filled again, becoming crescent, with some stars showing `[text: thucydides-grc 2.28.1.1; thucydides-crawley-eng 2.28.1.1]`.
- **NASA.** −430 Aug 03, annular, gamma 0.8388, greatest eclipse at 68N 6E `[NASA 03764]`.
- **Local.** At Athens: magnitude 0.877 at 17:34 LMT, Sun 17° up, on both ΔTs `[computed: run_solar.out.txt]`. "After midday" ✓ and "crescent" ✓. Stars at 0.88 would mean only the brightest objects `[me]`.
- **Identification.** Stephenson & Fatoohi, "The eclipses recorded by Thucydides", *Historia* 50 (2001) 245–253: dates 431, 424 and 413 BC and finds the accounts reliable `[secondary: search-engine abstract; not read]`.
- **Control value.** The year is fixed by Thucydides' war-year count (summer of year 1). The new-moon remark is an ancient statement of the same constraint B&M use at Day 0.

### 4.2 Thucydides 4.52 (P2)
- **Text.** At the very start of the next summer an eclipse of the sun "about new moon", and an earthquake early in the same month `[text: thucydides-grc 4.52.1.1]`.
- **NASA.** −423 Mar 21, annular, gamma 0.9433 `[NASA 03780]`. The only other solar eclipse in −423 is Sep 14, in the southern hemisphere `[NASA 03781]`.
- **Local.** 0.703 at 08:43 LMT at Athens `[computed]`.
- **Discrepancy.** Gautschy's list gives "424 BC May 21" `[secondary: Gautschy, eclipsecitations.pdf]`. No eclipse occurred in May −423 `[NASA]`, so I treat it as a typo.

### 4.3 Thucydides 7.50 (P3): a multi-clue control with a day interval
- **Text.** As the Athenians were about to sail, the moon, which was full, was eclipsed. Nicias would not discuss leaving until they had waited "thrice nine days", as the seers interpreted it `[text: thucydides-grc 7.50.4.1]`.
- **Conflicting interval.** Diodorus gives "the customary three days" `[text: diodorus-bk11-17-grc 13.12.6.1]`. The interval clue disagrees between sources for an event fixed in every other respect.
- **NASA.** −412 Aug 28 01:15:33 TD, total, umbral magnitude 1.0804 `[NASA 03842]`.
- **Local.** At Syracuse greatest eclipse was 27 Aug at 21:56 LMT, Moon 32° up `[computed: run_lunar.out.txt]`. This is the textbook case of a TD date versus a local date.
- **Plutarch, *Nic.* 23.1–2,** adds that solar eclipses toward the end of the month were by then understood `[text: plutarch-nicias-grc 23.1.1]`.

### 4.4 Xenophon, *Hellenica* (P4, P4b, P4c)
- **1.6.1.** In the year the moon was eclipsed "in the evening" and the old temple of Athena burned `[text: xenophon-hellenica-grc 1.6.1.1]`.
  - NASA: −405 Apr 15 23:33 TD, total `[NASA 03859]`. Greatest at 20:49 LMT at Athens, Moon 25.6° up, so "evening" ✓ `[computed]`.
  - The heading's "Pityas ephor, Callias archon" and "24th year" are described in an edition's notes as glosses. The correct count would be the 25th year `[secondary: search-engine summary of an edition note; not verified]`.
  - By standard Attic reckoning, April 406 falls in the archon year 407/6, not Callias' year 406/5 `[me]`. This fits the gloss diagnosis.
  - Lesson: in a secure positive control the astronomy can be right while the chronological apparatus is wrong.
- **2.3.4 and 4.3.10** are listed by Gautschy (404 BC Sep 3; 394 BC Aug 14) `[secondary: Gautschy]`.
  - −403 Sep 03: annular, 0.77 at Pherae, 08:34 LMT.
  - −393 Aug 14: annular, 0.91 at Coronea, 09:34 LMT. Xenophon's phrase "appeared crescent-shaped" fits `[NASA 03827, 03850; computed: run_solar2.out.txt]`.
- **Control value.** Three eclipses in one author, with relative years known from the narrative: an M-y control (section 7.3).

### 4.5 Herodotus 1.74, Thales (P5)
- **Text.** In the sixth year of war, during battle, day suddenly became night. Thales had foretold it "within the year" `[text: herodotus-grc 1.74.2.1]`.
- **Pliny.** Ol. 48.4 (585/4 BC) `[text: pliny-nh-lat 2.12.1 (= NH 2.53)]`.
- **NASA.** −584 May 28 19:28 TD, total, gamma 0.3201 `[NASA 03379]`.
- **Local.** About 0.97 at the approximate Halys site, 18:14 LMT, Sun 8.6° up; 0.972 at Miletus at 17:50 `[computed]`. The real battlefield is unknown, and totality depends on the site.
- **Alternatives.** 30 Sep 610 BC (−609): 0.70 at the Halys site. 18 May 603 BC (−602): 0.57 `[NASA 03314, 03332; computed]`.
- **Identification.** Stephenson & Fatoohi, *JHA* 28 (1997) 279–282, accept 28 May 585 BC `[secondary: search-engine summary; not read]`. The arXiv/*Culture & Cosmos* paper "On the Eclipse of Thales, Cycles and Probabilities" (arXiv:1307.2095) deals with the probabilities `[secondary: title only]`.
- **Grade B.** The year rests partly on the eclipse itself.

### 4.6 Herodotus 9.10 (P6)
- **Text.** While Cleombrotus was sacrificing at the Isthmus, the sun "was dimmed in the sky" `[text: herodotus-grc 9.10.3.1]`.
- **NASA.** −479 Oct 02, annular `[NASA 03645]`.
- **Local.** 0.60 at the Isthmus, 13:35 LMT `[computed]`. A modest partial phase matches the modest verb ✓.
- **Gautschy** has "480 BC October 2" `[secondary]`.

### 4.7 Archilochus fr. 122 West (P7)
- **Not in the library.** There is no Archilochus edition; the fragment is preserved by Stobaeus, who is not in the library either.
- **Aristotle** quotes only its first words, "of things nothing is unexpected nor sworn impossible". He attributes them to a father speaking about his daughter in an iambus `[text: aristotle-rhetoric-grc 3.17.16.1]`.
- **Gautschy** prints fr. 122.1–4 under "648 BC April 6" `[secondary]`.
- **Identification.** 648 BC goes back to Oppolzer (1887) `[secondary: search-engine summary]`. Jacoby (*CQ* 35, 1941) defended it `[secondary: not read]`.
- **NASA.** −647 Apr 06, total, greatest at 45N 36E `[NASA 03218]`.
- **Local.** Thasos 1.000 (NASA ΔT) or 1.004 total (Horizons ΔT) at 09:50 LMT; Paros 0.99 `[computed]`.
- **Alternative.** 14 Mar 711 BC (−710) was also total at Thasos: 1.015 at 10:33 LMT; Paros 0.96 `[NASA 03060; computed: run_extra.out.txt]`.
- **Lesson.** Astronomy offers two candidates and the poet's biography picks one. **Grade B.**
- **Control value.** A poetic positive control: mythic idiom ("Zeus made night") for a real total eclipse.

### 4.8 Plutarch, *Pelopidas* 31, and Diodorus 15.80 (P8)
- **Plutarch.** As Pelopidas set out, the sun was eclipsed and darkness held the city by day `[text: plutarch-pelopidas-grc 31.2.1]`.
- **Diodorus.** Gives the same event, and the seers read it as the city's "sun" failing `[text: diodorus-bk11-17-grc 15.80.2.1–3.1]`.
- **NASA.** −363 Jul 13, total `[NASA 03919]`.
- **Local.** At Thebes only **0.67** at 09:16 LMT `[computed]`.
- **Exaggeration.** "Darkness held the city" is literary exaggeration of a two-thirds partial eclipse `[me]`. This is the key calibration point against reading darkness words as totality.

### 4.9 Diodorus 20.5.5, Agathocles (P9)
- **Text.** "On the next day" (after the escape from Syracuse harbour) the eclipse was so great that it seemed full night, with stars seen everywhere `[text: diodorus-bk18-20-grc 20.5.5.1]`. Gautschy cites this as 20.5.6 `[secondary]`, a section-numbering difference between editions.
- **NASA.** −309 Aug 15, total, gamma 0.3394 `[NASA 04039]`.
- **Local.** At Syracuse 0.995 (NASA ΔT) or 0.998 (Horizons ΔT) at 07:39 LMT `[computed]`. The fleet was at sea, and the path of totality lay close by.
- **Grade A.** It has a day-interval clue ("next day").

### 4.10 Livy 44.37, Pydna (P10)
- **Text.** Sulpicius Gallus announced that the moon would be eclipsed from the second to the fourth hour of the night `[text: livy-lat 4.44.37.5.1]`. It happened on the night before "pridie nonas Septembres" `[text: livy-lat 4.44.37.8.1]`.
- **Other sources.** Plutarch, *Aem.* 17.7–10 `[text: plutarch-aemilius-grc 17.7.1]`; Pliny 2.53 `[text: pliny-nh-lat 2.12.1]`.
- **NASA.** −167 Jun 21 22:04 TD, total `[NASA 04406]`.
- **Local.** Greatest at Pydna 20:09 LMT, Moon 5.9° up `[computed]`, consistent with eclipse soon after moonrise.
- **Calendar.** The Roman date (4 Sept Roman) is about 75 days ahead of Julian `[me]`.
- **Control value.** A day-interval clue (battle the next day) plus a calendar-offset clue.
- **Library note.** The library's Latin Livy (EditionId 1855) numbers by volume. "4.44.37.5.1" means volume 4, book 44, chapter 37, section 5.

### 4.11–4.12 Livy 37.4.4 and 38.36.4 (P11, P12)
- **37.4.4.** At the *ludi Apollinares*, on a.d. V Id. Quinctiles, light was obscured "when the moon passed under the sun's disc" `[text: livy-lat 3.37.4.4.1]`.
  - NASA: −189 Mar 14, total `[NASA 04310]`. Rome 0.919 at 07:20 LMT `[computed]`.
  - The Roman 11 July corresponds to Julian 14 March, about 4 months ahead `[me]`.
- **38.36.4.** Darkness in daylight between the third and fourth hour `[text: livy-lat 3.38.36.4.1]`.
  - NASA: −187 Jul 17 `[NASA 04315]`. Rome 0.993 at 06:16 LMT `[computed]`. The time of day disagrees (see the P12 note in section 3).
- **Prodigy lists.** Livy also lists "the sun's disc seemed to diminish" among prodigies `[text: livy-lat 2.22.1.9.1; 2.30.38.8.1]`. Gautschy matches these to 11 Feb 217 BC (−216) and 6 May 203 BC (−202) `[secondary]`. I compute 0.65 at Rome and 0.48 at Cumae `[computed: run_solar2.out.txt]`.
- **A natural corpus.** These four Livy items, plus Julius Obsequens, Cassius Dio and Tacitus items in Gautschy, form a *prodigy-list* corpus. Real eclipses there sit among non-astronomical portents.

### 4.13 Cicero, *De re publica* 1.25, Ennius (P13)
- **Text.** Ennius wrote that about the 350th year from the founding, on the Nones of June, "the moon and night blocked the sun". From this day, recorded "in Ennius and the *Annales Maximi*", earlier eclipses were *computed back* to the one on the Nones of Quinctilis in Romulus' reign `[text: cicero-derepublica-lat 1.25.1]`.
- **Standard identification.** 21 Jun 400 BC (−399) `[secondary: Gautschy; search summary]`.
  - NASA: −399 Jun 21 21:52 TD, total, greatest at 64N 97W `[NASA 03836]`.
  - At Rome the Sun set eclipsed: 0.72 while above the horizon `[computed]`.
- **Alternative: 20 Mar 405 BC (−404),** C. Bennett's Roman-calendar model. It needs the Roman calendar about 76 days ahead of Julian `[secondary: instonebrewer.com/TyndaleSites/.../res_ennius.htm]`.
  - NASA: −404 Mar 20, annular `[NASA 03824]`. At Rome 0.748 at sunset, 17:55 LMT `[computed]`.
- **Lesson.** Astronomy cannot separate the two; the calendar model decides.
- **Grade.** B for 400 BC; C if the alternative is taken seriously.

### 4.14 Plutarch, *De facie* 19 (931D–E) (P14)
- **Text.** "This recent conjunction" began just after noon and showed many stars `[text: plutarch-defacie-grc 19.1; plutarch-defacie-cherniss-eng 19.1]`. The same sentence cites Mimnermus, Cydias, Archilochus, Stesichorus and Pindar on eclipses. It then cites Homer: faces covered with night and "the sun has perished out of heaven", "as the waning month gives way to the waxing" `[text: plutarch-defacie-grc 19.1]`.
- **NASA.** AD 71 Mar 20, hybrid, gamma 0.6541, path 31 km `[NASA 04949]`.
- **Local.** 0.979 at Chaeronea at 10:58 LMT (0.986 on Horizons ΔT) `[computed]`.
- **Identification.** Ginzel proposed AD 71. Sandbach objected that the maximum came near 11 a.m. local time, against Plutarch's "after noon" `[secondary: Stephenson & Fatoohi, "The total solar eclipse described by Plutarch", *Histos*; search summary]`.
  - My computed 10:58 LMT agrees with Sandbach's timing `[computed]`.
  - Stephenson & Fatoohi still conclude that the eclipse is AD 71 March 20 and that the setting is Greece `[secondary: Histos PDF; digits lost in my text extraction, so the date comes from the search summary and Gautschy]`.
- **Second role.** This is the earliest surviving *eclipse reading of Od. 20.356–357*, already coupled with Od. 14.162 / 19.307 (section 6).

### 4.15 Gaugamela (P15): the best literary multi-clue positive control
- **Plutarch.** The moon was eclipsed in Boedromion, about the start of the Mysteries. "On the eleventh night after the eclipse" the armies were in sight of each other `[text: plutarch-alexander-grc 31.4.1]`.
- **Arrian.** Most of the moon was eclipsed after the Tigris crossing `[text: arrian-anabasis-grc 3.7.5.1–3.7.6.1]`. He dates the battle to the archonship of Aristophanes, **month Pyanepsion** `[text: arrian-anabasis-grc 3.15.7.1]`. The month names conflict across sources.
- **Curtius.** The moon failed in the first watch `[text: curtius-lat 4.10.2.1]`.
- **Pliny.** At Arbela the eclipse was "at the second hour of night" and in Sicily "at moonrise" `[text: pliny-nh-lat 2.70.3 (= NH 2.180)]`. This is a two-site, longitude-type clue.
- **NASA.** −330 Sep 20 22:24 TD, total `[NASA 04036]`.
- **Local.** Greatest at 21:18 LMT at Arbela, Moon 36° up `[computed]`.
- **Babylonian Astronomical Diary** (BM 36761 + BM 36390) records the eclipse and the panic in Darius' camp `[secondary: livius.org; academia.edu Gaugamela papers; not read]`.
- **Control value.** A real M-d clue set: eclipse, +11 nights, battle, season, hour, two sites. Some clues are noisy (month name).

### 4.16 Polybius 5.78 (P16)
- **Text.** "When an eclipse of the moon occurred", the Gauls refused to march further `[text: polybius-grc 5.78.1.1]`.
- **NASA.** −217 Sep 01, total, 93.4 min of totality `[NASA 04291]`.
- **Local.** At my approximate Mysian site greatest eclipse came 4° before moonrise, so the Moon rose eclipsed `[computed]`.
- **Date.** Fixed by the campaign context `[me; Walbank's commentary not read]`.

### 4.17 Plutarch, *Dion* (P17, P17b)
- **24.1.** The moon was eclipsed after the libations at the departure `[text: plutarch-dion-grc 24.1.1]`.
  - NASA: −356 Aug 09, partial, umbral 0.1938 `[NASA 03975]`.
  - At Zacynthus greatest at 19:19 LMT, Moon 1.7° up, so seen near moonrise `[computed]`.
- **19.4.** Helicon of Cyzicus predicted a solar eclipse `[secondary: Gautschy, 361 BC May 12]`.
  - NASA: −360 May 12, annular `[NASA 03926]`. Syracuse 0.96 at 17:39 LMT `[computed]`.

### 4.18 Assyrian Eponym Chronicle (P18)
- **Not in the library** (cuneiform).
- **The record.** A solar eclipse in the month Simanu, in the eponymy of Bur-Saggile. The standard identification is 15 June 763 BC; it anchors Assyrian absolute chronology `[secondary: general literature, e.g. Millard 1994; not read]`.
- **NASA.** −762 Jun 15, total, gamma 0.2715 `[NASA 02937]`.
- **Local.** 0.953 at Assur, 0.982 at Nineveh, about 10:45 LMT `[computed]`.
- **Amos 8:9** ("the sun shall go down at noon") is often linked to this eclipse `[text: lxx-amos-grc 8.9.1]`. It is a prophecy, not a record (section 5).

### 4.19 Ptolemy's *Almagest* (P19): exact multi-event controls with B&M's own clue types
**Library.** EditionId 2977 (Heiberg Greek). The refs below are the export keys of `ptolemy-syntaxis-grc.tsv`.

**Calendar conversion.** I converted the Egyptian dates with the Nabonassar era: Thoth 1 of year 1 = JD 1448638 = −746 Feb 26, noon. Mardokempad year 1 = Nabonassar year 27; Hadrian year 1 = Nabonassar year 864. Every result matches a NASA catalogue row `[computed: run_extra.out.txt; NASA]`.

| Almagest | Text date | Julian (local) | NASA row | Local [computed] |
|---|---|---|---|---|
| IV.6 (4.6.3) | Mardokempad 1, Thoth 29/30, total | night of 19/20 Mar 721 BC (−720) | −720 Mar 20 00:20 TD, T+ (03072) | Babylon 21:36 LMT, Moon 43°; Ptolemy: total, mid-eclipse about 2½ h before midnight |
| IV.6 (4.6.4) | Mardokempad 2, Thoth 18/19, 3 digits from the south | 8/9 Mar 720 BC (−719) | −719 Mar 09 02:32 TD, P (03074) | Babylon 23:48 LMT, Moon 65°; Ptolemy: mid-eclipse at midnight |
| IV.6 (4.6.5) | Mardokempad 2, Phamenoth 15/16, more than half from the north | 1/2 Sep 720 BC (−719) | −719 Sep 01 22:43 TD, P (03075) | Babylon 19:59 LMT |
| IV.11 (4.11.3) | Phanostratus, Poseideon; Nab 366 Thoth 26/27; the Moon "set while still eclipsed" | 22/23 Dec 383 BC (−382) | −382 Dec 23 09:15 TD, P (03915) | Babylon: greatest 08:00 LMT, after moonset, so the Moon set eclipsed ✓ |
| IV.11 (4.11.4) | Phanostratus, Skirophorion; Phamenoth 24/25 | 18/19 Jun 382 BC (−381) | −381 Jun 18 22:23 TD (03916) | Babylon 21:08 LMT |
| IV.11 (4.11.5) | archon Euandros, Poseideon I; Nab 367 Thoth 16/17; total; *beginning* about 2½ seasonal hours (≈3 equinoctial hours) before midnight | 12/13 Dec 382 BC (−381) | −381 Dec 13 00:16 TD, T− (03917) | Babylon 23:01 LMT (12 Dec) |
| IV.6 (4.6.13) | Hadrian 17, Payni 20/21, total | 6 May AD 133 | AD 133 May 06 (05153) | Alexandria 22:46 LMT |
| IV.6 (4.6.14) | Hadrian 19, Choiak 2/3 | 20 Oct AD 134 | AD 134 Oct 20 (05156) | Alexandria 22:43 LMT |
| IV.6 (4.6.15) | Hadrian 20, Pharmouthi 19/20; half the diameter from the north; Ptolemy: mid-eclipse 4 h after midnight | 5/6 Mar AD 136 | AD 136 Mar 06 04:06 TD (05160) | Alexandria 03:32 LMT |
| X.1 (10.1.3) | Theon: Venus greatest evening elongation, Hadrian 16 Pharmouthi 21/22 | evening of 8 Mar AD 132 | — | elongation on that date 45.00°; true maximum 46.04° on 21 Feb, **16 days earlier** |
| IX.8 (9.8.3) | Mercury greatest morning elongation, Hadrian 19 Athyr 14/15 | 2/3 Oct AD 134 | — | 18.15° on that date; true maximum 18.51° on 29 Sep, **3 days earlier** |

**Why this matters** `[me]`:
- The triples come with exact day and hour intervals and with the *same observable types* B&M rely on: lunar syzygy timing, and an inferior planet at an elongation extreme.
- So the *Almagest* is the natural place to measure how often a B&M-style search recovers a known date when the clues are real expert observations. It also tells us how much timing slack a "turning point" clue needs.

**Library data-quality note.** The Syntaxis text has literal strings "U+2220" where Heiberg prints the half-sign (∠), for example at 4.6.3. 4.6.9 has "??ς". These are ingest artefacts in ClassicaCodex, not in my export `[text]`.

---

## 5. Hard cases and contested identifications

These are not usable as positive controls. They are valuable because each shows how an identification can go wrong.

| # | Citation | Claimed or possible event | What goes wrong | Lib |
|---|---|---|---|---|
| H1 | Hdt. 7.37.2–3 | Total eclipse at Xerxes' spring departure from Sardis, 480 BC; "day turned to night" `[text: herodotus-grc 7.37.2.1]` | No solar eclipse was visible at Sardis in spring 480 `[NASA; computed]`: −479 Apr 09 was total far south (21S 130W); −480 Apr 19 was below Sardis' horizon (magnitude <0 at sunrise). Candidates are displacements: −479 Oct 02 (0.55 at Sardis), 17 Feb 478 BC (−477, annular, **0.948 at Sardis**, 12:11 LMT), or the total lunar eclipse of 14 Mar 479 BC (−478, Moon 26° up at 04:09 LMT). Gautschy picks 478 Feb 17 `[secondary]`. Grade C. | 687 |
| H2 | Pindar, *Paean* 9 | "Beam of the sun ... star stolen in daytime" | 30 Apr 463 BC (−462): 0.976 at Thebes, 14:36 LMT. 1 Sep 488 BC (−487): 0.96 at 05:46 LMT, Sun 4° `[computed]`. Gautschy lists both with "?" `[secondary]`. **Not in library** (only the Olympians, Pythians, Nemeans and Isthmians, EditionIds 859–866). Grade C. | — |
| H3 | Xen. *Anab.* 3.4.8 | A *cloud* hid the sun at Larisa (Nimrud) until the people left `[text: xenophon-anabasis-grc 3.4.8.1]` | The text says cloud. Gautschy's list assigns it to the 19 May 557 BC eclipse (−556) `[secondary]`, which I compute at 0.885 at Nimrud, 17:22 LMT `[computed]`. The eclipse reading overrides what the text says. Grade C/D. | 842 |
| H4 | Plut. *Per.* 35.1–2 | Eclipse as Pericles' fleet sailed (430 BC) | The only matching eclipse is 3 Aug 431 BC (Thuc. 2.28), a year earlier. Plutarch attaches it to the wrong expedition `[me]`. | 81 |
| H5 | Josephus, *AJ* 17.167 | Lunar eclipse on the night Herod burned Matthias, shortly before his death and a Passover `[text: josephus-antiquities-grc 17.167.1]` | Candidates `[NASA]`: 23 Mar 5 BC (−4, total); 15 Sep 5 BC (−4, total); 13 Mar 4 BC (−3, partial 0.36; Jerusalem 03:02 LMT, Moon 40°) `[computed]`; 10 Jan 1 BC (0, total). The interval to Passover decides, and that interval is disputed. A good *M-d with ambiguity* case. Grade C. | 1315 |
| H6 | Ugarit, KTU 1.78 (cuneiform) | "The day ... was put to shame; the Sun went in" | 3 May 1375 BC (Sawyer & Stephenson 1970) versus 5 Mar 1223 BC (de Jong & van Soldt, *Nature* 338, 1989, 238–240). Others proposed: 1192, 1012 BC `[secondary: search summary]`. With NASA ΔT I get Ugarit 0.970 at 06:08 LMT (−1374) and 0.923 at 13:59 LMT (−1222). **Neither is total** without a ΔT change of several hundred seconds `[computed]`. The *same ΔT regime* as the Odyssey eclipse. Grade C. | — |
| H7 | Mursili II's "omen of the sun" (Hittite) | Often identified with 24 Jun 1312 BC | Hattusa 0.991 at 13:33 LMT (−1311) `[computed]`. The identification is contested `[secondary: general; not read]`. Grade C. | — |
| H8 | Ennius alternative | see P13 | The calendar model decides | 1756 |

---

## 6. Negative controls: fiction, legend, calendar poetry, darkness motifs

For each text: the sky clues a B&M-style method could be pointed at, with line refs from the exported files, and why the text cannot date a real event.

### 6.1 Virgil, *Aeneid*: a fictional narrative of the same legendary age
EditionIds 1827 (Latin) and 1826 (Williams English); file `virgil-aeneid-lat.tsv`. Composed 29–19 BC.

**The night Troy fell gives an Odyssey-shaped clue set:**
- the Greeks sail from Tenedos under the friendly silence of the moon (2.255);
- fighters seen "by the moon" (2.340);
- setting stars at midnight (2.9);
- **Lucifer rising over Ida at dawn** (2.801).

That is moon phase + morning star + a day count. A B&M search would return a "date for the fall of Troy" `[me]`.

**Other clues:**
- Palinurus checks Arcturus, the rainy Hyades, the twin Triones and Orion before sailing (3.515–517). This is the direct analogue of Od. 5.272–275, and **3.516 repeats 1.744 word for word** (a formula).
- Three sunless days and three starless nights at sea (3.203–204): a darkness motif with a day count.
- Three moons have filled since Achaemenides was abandoned (3.645): an interval clue.
- Storm-bringing Orion (1.535, 4.52, 7.719).
- Vesper (1.374, 8.280); the Lucifer simile (8.589); Iopas sings "the wandering moon and the sun's labours", meaning eclipses (1.742).

### 6.2 Apollonius, *Argonautica*: Hellenistic epic of a legendary voyage
EditionId 1; file `apollonius-argonautica-grc.tsv`. Composed 3rd century BC.

**Clues:**
- **morning star** rising over the peaks as Heracles is left behind (1.1273);
- the wintry setting of Orion (1.1202);
- Pleiades (3.226);
- sailors watching Helice and Orion (3.744–745);
- Helice at night (3.1195);
- Sirius (2.517; 3.957);
- evening star (4.1290; 4.1629);
- the moonless, starless "pall" night, κατουλάς (4.1695–1697), before Apollo's light at Anaphe: a darkness motif;
- seeing as one sees the new moon through mist (4.1479);
- Medea halting stars and moon (3.533).

The Argonauts' voyage has its own day counts, so multi-clue sets can be built `[me]`.

### 6.3 Hesiod, *Works and Days*: calendar, not event
EditionId 728; file `hesiod-worksdays-grc.tsv`.

**Clues:**
- Pleiades rising and setting as the signs for harvest and ploughing (383–384), hidden for 40 days (385);
- the solstice (479);
- Arcturus rising at dusk 60 days after the winter solstice (564–567);
- Orion and Sirius at mid-sky and Arcturus seen at dawn, the vintage (609–611);
- Pleiades, Hyades and Orion setting (615);
- the Pleiades "fleeing" Orion into the sea, the end of sailing (619–620);
- 50 days after the solstice for sailing (663);
- the "Days", including the 30th and the fourth of the waxing and waning month (765–828; 798).

These are seasonal rules that repeat every year. B&M themselves cite Hesiod for the season of the Pleiades `[secondary: B&M per PMC2440358]`. Applied as event clues, they match every year, so the "uniqueness" any method reports here comes from its other clues `[me]`.

### 6.4 Aratus, *Phaenomena*, with Hipparchus' commentary: real but inherited astronomy
EditionIds 1559 and 3325; files `aratus-phaenomena-grc.tsv` and `hipparchus-in-aratum-grc.tsv`.

**Clues:**
- the Pleiades (254–267);
- crescent-moon weather signs on the third and fourth day (733–736; 778–781);
- the "tetrads" of the waning and waxing month (1148–1150).

The phrase at 1149 echoes Od. 14.162. Hipparchus criticised Aratus and Eudoxus for describing a sky that does not match his own.

**Why it is a negative control** `[me]`: the constellation data can be precession-dated to an epoch much earlier than the poem's composition (c. 275 BC), so its "astronomical date" is *not* the date of the text. Schaefer (2004, *JHA* 35) is often cited for such a dating `[secondary: not read; treat as a pointer only]`.

### 6.5 Homeric Hymns: mythic, and internally inconsistent
**To Hermes** (EditionId 501; `hhymn04-hermes-grc.tsv`):
- born at dawn on "the fourth day of the month" (17–19), stealing the cattle that evening (18);
- near dawn, Selene "had just climbed her watch-post" (97–100);
- moonlight all night long (141).

A 4-day-old moon sets in the evening; it does not rise near dawn, and it does not shine all night. **The three lunar clues contradict each other** `[me]`.

**To Demeter** (EditionId 497): nine days of wandering with torches (47–50), the tenth dawn (51), Helios as the all-seeing witness (62–63).

**To Selene** and **To Helios** (EditionIds 557, 555): generic.

### 6.6 Iliad: same tradition, same formulas
File `data/text/iliad-grc.tsv`.

**Clues:**
- the Shield's constellations: Pleiades, Hyades, Orion, the Bear (18.485–489). **18.487–489 = Od. 5.273–275**;
- Sirius, "Orion's dog", rising in late summer as an evil sign (22.26–31; also 5.5–6);
- the baneful star appearing among clouds (11.62–63);
- Zeus stretches deadly night over the battle (16.567);
- mist so thick that "you would not say the sun or moon was safe" (17.366–368), the closest Homeric parallel to Od. 20.356–357;
- Hera sends the sun down early (18.239–241);
- Agamemnon prays that the sun not set (2.412–413);
- the sun's light falls into Ocean (8.485–486).

**The Iliad is the most direct null** `[me]`: same diction and same composers, applied to a war whose day count is also explicit. Whatever "unique date" the Odyssey clues yield, the method should be shown *not* to yield one equally readily from the Iliad.

### 6.7 Darkness motifs that are not eclipses (grade D)
- **Od. 20.351–357 itself, per the scholia.** On "the sun has perished out of heaven": no eclipse happened; Theoclymenus sees it in a prophetic frenzy, and the suitors, seeing nothing, call him mad `[text: scholia-odyssey-grc 2.20.2.91]`.
  - The scholia on 14.162 explain "the waning month" as "into the 30th and the new-moon day" `[text: scholia-odyssey-grc 2.14.2.94]`.
  - Against this, Heraclitus' *Allegories* reads 20.356 as an eclipse, citing Hipparchus on "trikas and noumenia" and quoting 14.162 `[text: heraclitus-allegoriae-grc 73.2; EditionId 3322]`. Plutarch does the same `[text: plutarch-defacie-grc 19.1]`.
- **Od. 23.243–246:** Athena holds back Dawn, a mythic lengthening of night.
- **Gospels.**
  - Mark 15.33 and Matt. 27.45: darkness from the sixth to the ninth hour `[text: nt-mark-grc 15.33.1; nt-matthew-grc 27.45.1]`.
  - Luke 23.44–45 adds "the sun failing" `[text: nt-luke-grc 23.45.1]`.
  - This is set at Passover, which falls at full moon, so a solar eclipse is impossible `[me]`.
  - Phlegon's "eclipse" (via Africanus and Eusebius in Synkellos) is matched by Gautschy to 24 Nov AD 29 `[secondary]`. Not in the library.
- **Amos 8:9:** prophecy `[text: lxx-amos-grc 8.9.1]`.
- **Virgil, *Georgics* 1.463–468:** at Caesar's death the sun "covered its bright head in dark rust" `[text: virgil-georgics-lat 1.466–468]`.
  - No solar eclipse was visible at Rome in 44 BC. −43 Apr 18 was below the horizon; −43 Oct 12 was at night `[NASA 04663–4; computed]`.
  - Ovid, *Met.* 15.785–790, gives the same portent with a pallid sun, a rust-stained Lucifer and a bloody Moon `[text: ovid-metamorphoses-lat 15.785–790]`.
- **Lucan 1.540–544:** Titan hid his chariot in darkness at midday as the civil war began, compared with Thyestes' Mycenae `[text: lucan-lat 1.540–544]`.
  - Cassius Dio 41.14.3 lists "the whole sun failed" among the same portents `[text: cassius-dio-grc 41.14.3.1]`.
  - Gautschy assigns Dio's item to 7 Mar 51 BC (−50) `[secondary]`: annular, 0.883 at Rome at 13:23 LMT `[NASA 04645; computed]`.
  - Lucan's "sun at mid-heaven" fits that time of day `[me]`.
  - **A real eclipse, displaced about two years into a narrative.**
- **Mythic sun-reversals:** Seneca, *Thyestes* 776–793 (the sun flees backward, night at the wrong time) `[text: seneca-thyestes-lat 776, 785–787, 793]`; Euripides, *Electra* 727–728 (Zeus changed the stars' paths and the sun's light) `[text: euripides-electra-grc 2.727–2.728]`.
- **Romulus' disappearance.**
  - Plutarch, *Rom.* 27.6–7: the sun's light failed and a storm broke `[text: plutarch-romulus-grc 27.6.1]`.
  - Dionysius of Halicarnassus 2.56.6 has the same `[text: dionysius-hal-antiquitates-grc 2.56.6.1]`.
  - Cicero calls it an eclipse and says it was *computed back* `[text: cicero-derepublica-lat 1.25.1]`.

### 6.8 Tarutius' horoscope: astronomy used to fabricate a date (grade D, but astronomically "real")
- **Text.** Plutarch, *Rom.* 12.3–6: Varro asked Tarutius to find Romulus' birth from the events of his life. Tarutius put the conception in Ol. 2.1, Choiak 23, third hour, "when the sun was totally eclipsed" `[text: plutarch-romulus-grc 12.5.1; plutarch-romulus-perrin-eng 12.5.1]`.
- **Conversion.** The Egyptian year beginning in 772 BC converts Choiak 23 to **24 Jun 772 BC (−771)** `[computed: run_extra.out.txt]`.
- **What happened that day.** A real solar eclipse: NASA 02917, partial, gamma 1.0495, greatest at 65N 108W `[NASA]`. At Rome its magnitude was about 0.000–0.005 `[computed]`.
- **Reading** `[me]`: the date is consistent with a *calculated* syzygy near a node. It was neither total nor seen in Rome. Retro-calculation gave a date that is astronomically real and historically meaningless.
- This is exactly what B&M's critics need ruled out for the Odyssey. I have not checked whether the literature already notes the match.

---

## 7. Proposal: a fair positive control for a multi-clue method

### 7.1 What "fair" must mean
B&M's argument has three steps `[secondary: B&M per PMC2440358; offsets per docs/research-bm2008-a.md §4–5]`:
1. Fix a clue set read from the text:
   - new moon at day 0;
   - Venus rising ≥90 min before the Sun at day −5;
   - Pleiades and Bootes both visible at nautical twilight at day −29;
   - Mercury near a turning point at day −34.

   The offsets are sequential; the parallel numbering gives 0, −4, −28, −33.
2. Search the 1,684 new moons of 1250–1115 BC.
3. Note that the single near-match coincides with an eclipse.

Their rarity statement ("one day every 2,000 years") is a property of *the clue grammar*. It is not evidence that the clues are observations.

**A fair positive control must therefore answer two questions:**
- **(Q1) Recall.** When clues really are observations of a known date, does the method recover that date uniquely?
- **(Q2) Specificity against a poet.** When clues are *not* observations, but are generated by a process that knows the sky's general habits (season, morning star, Pleiades lore, moon phase) and not a particular date, how often does the method still return one match? How often does that match land on an eclipse?

Only the ratio of (Q1) to (Q2) gives evidence (section 7.5). The controls must match the Odyssey's structure:
- 4 clues, of the same types and at the same offsets;
- the same window length (135 years, about 1,684 new moons);
- the same latitude band (36–41°N);
- the same tolerances, chosen *before* looking at the target.

### 7.2 Design PC-S: synthetic Odyssey-shaped clue sets, true versus random
Code: `odybench/controls/synthetic.py`, to be written.

1. **Truth dates.** Draw t* from two pools:
   - **(a) Eclipse new moons:** solar eclipses of magnitude ≥0.95 at any Greek-world site, 1400–600 BC, from the NASA catalogue plus local magnitude.
   - **(b) Ordinary new moons** in the same span.
2. **Describe the actual sky.** For each t*, compute what the sky *actually* showed at days −34, −29, −5 and 0, using the *same* ephemeris and ΔT pair as the main search. Encode it in a fixed, coarse vocabulary, the *Odyssey grammar*:
   - Venus: morning star (risen ≥90 min before the Sun) / evening star / invisible.
   - Mercury: near a station or extreme of rising azimuth within ±k days / not. Use k = 3 and k = 16 as the two empirical slacks from the *Almagest* records (section 4.19).
   - Which of {Pleiades, Bootes, Orion, Bear} are visible at nautical dusk or dawn.
   - Moon phase bin at day 0.
3. **Search.** Run B&M's search, unchanged, over a 135-year window that contains t* at a uniformly random position. Record:
   - recall: t* is among the matches;
   - n_other: other matching new moons;
   - eclipse-coincidence: a match falls on a new moon with an eclipse of magnitude ≥0.9 at Ithaca, and separately at any Ionian site.
4. **Noise.** Repeat with noise injected at the levels a poet or an oral tradition would plausibly add:
   - day offsets jittered ±1–3 days (the Thucydides/Diodorus 27-versus-3-day split shows how intervals mutate between sources, section 4.3);
   - one clue dropped or swapped (for example, Venus "high" read as "evening star");
   - the Mercury slack set at 3 or 16 days.
5. **Report** recall and the n_other distribution as functions of noise.

**What it shows.** If ordinary new moons, pool (b), also produce clue sets that match "only once in 2,000 years", then that uniqueness is generic and carries no evidential weight `[me]`.

### 7.3 Design PC-R: real multi-event passages with independently known dates
Blind these: remove absolute dates and give the method only the clue types and intervals the ancient text gives. Recovery is scored within a window of the same length as B&M's, with truth at a random offset.

| Set | Clues given to the method | Truth | Source |
|---|---|---|---|
| R1, *Almagest* Babylonian triple | 3 lunar eclipses; intervals in Egyptian days and hours; magnitudes "total" / "3 digits S" / ">½ N"; site Babylon | −720 Mar 19/20, −719 Mar 8/9, −719 Sep 1/2 | 4.6.3–5 |
| R2, *Almagest* Hadrianic set | 3 lunar eclipses AD 133–136 (intervals); Venus greatest evening elongation and Mercury greatest morning elongation at their recorded day offsets; site Alexandria | see 4.19 | 4.6.13–14, 9.8.3, 10.1.3 |
| R3, Thucydides | solar at new moon in summer of war-year 1, after midday, crescent; solar near new moon at the start of summer of year 8 (morning); lunar at full moon in late summer of year 19, then a 27-day wait | 431, 424, 413 BC | 2.28, 4.52, 7.50 |
| R4, Xenophon | lunar "evening" (year n); solar morning (n+2, Thessaly); solar crescent (n+12, Boeotia, summer) | 406, 404, 394 BC | *Hell.* 1.6.1, 2.3.4, 4.3.10 |
| R5, Gaugamela | lunar, total, 2nd hour of night at Arbela and at moonrise in Sicily; battle 11 nights later; autumn | 20 Sep 331 BC | Plut., Arr., Curt., Pliny |
| R6, Pydna | lunar from the 2nd to the 4th hour of night; battle next day; Roman "pridie Non. Sept."; summer | 21 Jun 168 BC | Livy 44.37 |
| R7, Agathocles | escape at night; next day a total solar eclipse at sea, Sicily–Africa, late summer | 15 Aug 310 BC | Diod. 20.5.5 |
| R8, Livy prodigy series | four "sun diminished / darkness" items with consular years and Roman dates | 217, 203, 190, 188 BC | 22.1.9, 30.38.8, 37.4.4, 38.36.4 |

**Scoring.** Recall; n_other; and, for R6 and R8, whether a *calendar offset* is recovered jointly with the date. The Roman dates run about 2.5 and 4 months ahead of Julian. This tests the Odyssey-relevant question of whether a festival "calendar" date (the Apollo festival at the new moon, Od. 20.156, 20.276–278, 21.258) constrains anything once its calendar is unknown `[me]`.

**Poetic single-clue controls.** Archilochus, Ennius, Hdt 9.10, *De facie* and Pelopidas test the separate step "does this darkness phrase denote an eclipse, and how large". Use them to fit a *language-to-magnitude* likelihood (section 0, item 3) instead of assuming that 20.356 requires totality.

### 7.4 Design NC: run the identical pipeline on the negative texts
Build clue sets from sections 6.1–6.6 with the same grammar and the same rules for choosing passages:
- **Aeneid 2:** moon at night + Lucifer at dawn.
- **Aeneid 3.515–517:** star check before sailing.
- **Argonautica:** morning star 1.1273 + Orion setting 1.1202 + the dark night 4.1695.
- **Iliad:** Shield constellations + Sirius 22.26–31 + darkness 17.366–368.
- **Hymn to Hermes.**

Count the "unique matches in a 135-year window" these produce. That count is the method's empirical false-positive rate on texts known to be non-observational. For any fictional text that returns a unique match, also check the eclipse-coincidence rate.

### 7.5 The statistic to report
For the Odyssey, compare:
- **LR = P(one match ∧ the match is an eclipse new moon | clues are observations) / P(the same | clues are poetic).**

The numerator comes from PC-S(a) and PC-R. The denominator comes from PC-S(b) with poet-generated clue sets, and from NC.

**Account for the forking paths** in the denominator by enumerating all of them:
- sequential versus parallel offsets;
- the 10-year window extension;
- the three Mercury variables;
- the two seasons for the Pleiades and Bootes (spring and autumn);
- which "Venus" passage is used.

The minimum p over that garden is not the p-value: calibrate it against the same enumeration on NC texts `[me]`.

**Pre-register** thresholds, ephemeris and ΔT pair, window, site and grammar in the repo before running any of PC-S, PC-R or NC.

### 7.6 A note on the eclipse-coincidence denominator
B&M's 1178 BC match gains its force only from landing on Schoch's eclipse. The bench should compute the number of new moons in 1250–1115 BC with eclipse magnitude ≥ m at Ithaca, for m = 0.6, 0.8, 0.9 and 1.0, *under the full ΔT uncertainty*.

The language calibration in item 3 of section 0 (Pelopidas 0.67, Hdt 9.10 0.60) argues for m well below 1. ΔT at −1177 is uncertain by 600–1,900 s, which moves the totality band at Ithaca across it (section 0, item 9). Both points enlarge the denominator `[me]`.

---

## 8. Clue-structure inventory: which controls look like the Odyssey

| Feature of the Odyssey case | Best real analogue | Best negative analogue |
|---|---|---|
| Darkness phrase at a narrative climax | Archilochus (real, total); Pelopidas (real, 0.67, "darkness") | Il. 17.366–368; Lucan 1.540 (real but displaced); Gospels |
| New moon / month boundary at day 0 | Thuc. 2.28 ("the only time possible"); Heraclitus *All.* 73.2 | Hesiod WD 798; Aratus 1149 (calendar formula) |
| Morning star a few days before | *Almagest* X.1 (Venus; 16-day slack) | *Aen.* 2.801; *Arg.* 1.1273 |
| Mercury "turning point" about a month before | *Almagest* IX.8 (3-day slack) | none (Hermes as a god of journeys is pervasive) |
| Star lore while sailing | — (no secure dated case) | *Aen.* 3.515–517 (= 1.744); Il. 18.486–489 (= Od. 5.273–275) |
| Day-interval chain | Gaugamela (+11 nights); Thuc. 7.50 (+27 days, or 3 in Diodorus); Agathocles (+1 day); Pydna (+1 day) | Argonautica; *Hymn to Demeter* (9 days, then the 10th) |
| Event date set by external chronology | Archilochus (Gyges); Ennius (calendar model) | Tarutius (computed); Romulus' eclipse (computed per Cicero) |

---

## 9. Library exports made for this note (read-only via `py -m odybench.ccx`)

All are in `C:\Projects\odybench\data\text\`. "Rows" is the export row count.

| File | EditionId | Author / work | Rows |
|---|---|---|---|
| thucydides-grc.tsv | 14 | Thucydides, *History* (Greek) | 3622 |
| thucydides-crawley-eng.tsv | 13 | Thucydides (Crawley) | 3593 |
| herodotus-grc.tsv / herodotus-godley-eng.tsv | 687 / 686 | Herodotus | 4344 / 4338 |
| xenophon-hellenica-grc.tsv / -brownson-eng.tsv | 832 / 831 | Xenophon, *Hellenica* | 1153 / 1146 |
| xenophon-anabasis-grc.tsv / -brownson-eng.tsv | 842 / 841 | Xenophon, *Anabasis* | 1476 / 1469 |
| plutarch-pelopidas-grc.tsv / -perrin-eng.tsv | 99 / 98 | Plutarch, *Pelopidas* | 171 / 171 |
| plutarch-nicias-grc.tsv / -perrin-eng.tsv | 133 / 132 | Plutarch, *Nicias* | 178 / 179 |
| plutarch-aemilius-grc.tsv / -perrin-eng.tsv | 95 / 94 | Plutarch, *Aemilius Paullus* | 320 / 320 |
| plutarch-dion-grc.tsv / -perrin-eng.tsv | 177 / 176 | Plutarch, *Dion* | 389 / 389 |
| plutarch-alexander-grc.tsv / -perrin-eng.tsv | 151 / 150 | Plutarch, *Alexander* | 381 / 378 |
| plutarch-pericles-grc.tsv / -perrin-eng.tsv | 81 / 80 | Plutarch, *Pericles* | 182 / 182 |
| plutarch-romulus-grc.tsv / -perrin-eng.tsv | 61 / 60 | Plutarch, *Romulus* | 170 / 162 |
| plutarch-defacie-grc.tsv / plutarch-defacie-cherniss-eng.tsv | 371 / 369 | Plutarch, *De facie* | 31 / 86 |
| diodorus-bk11-17-grc.tsv | 952 | Diodorus, books 11–17 | 4294 |
| diodorus-bk18-20-grc.tsv | 954 | Diodorus, books 18–20 | 1846 |
| livy-lat.tsv / livy-roberts-eng.tsv | 1855 / 1854 | Livy (Latin, keyed by volume; Roberts English) | 20572 / 20337 |
| cicero-derepublica-lat.tsv | 1756 | Cicero, *De re publica* | 276 |
| ptolemy-syntaxis-grc.tsv | 2977 | Ptolemy, *Syntaxis* (*Almagest*), Heiberg | 3560 |
| aristotle-rhetoric-grc.tsv / -freese-eng.tsv | 1236 / 1235 | Aristotle, *Rhetoric* | 918 / 913 |
| arrian-anabasis-grc.tsv | 1186 | Arrian, *Anabasis* | 1406 |
| curtius-lat.tsv | 1844 | Curtius Rufus | 2621 |
| polybius-grc.tsv / polybius-shuckburgh-eng.tsv | 1447 / 1446 | Polybius | 12533 / 3454 |
| pliny-nh-lat.tsv / pliny-nh-eng.tsv | 2056 / 2055 | Pliny, *Natural History* (Latin keyed by chapter: 2.12.1 = *NH* 2.53; 2.70.3 = *NH* 2.180) | 6276 / 8088 |
| diogenes-laertius-grc.tsv | 16 | Diogenes Laertius | 1962 |
| josephus-antiquities-grc.tsv / -whiston-eng.tsv | 1315 / 1314 | Josephus, *AJ* | 7743 / 1729 |
| nt-luke-grc.tsv, nt-matthew-grc.tsv, nt-mark-grc.tsv, nt-luke-eng.tsv | 782, 778, 780, 781 | Gospels | — |
| lxx-amos-grc.tsv / amos-eng.tsv | 3015 / 1345 | Amos | 147 / 146 |
| apollonius-argonautica-grc.tsv | 1 | Apollonius, *Argonautica* | 5834 |
| virgil-aeneid-lat.tsv / -williams-eng.tsv | 1827 / 1826 | *Aeneid* | 9897 / 13336 |
| virgil-georgics-lat.tsv | 1825 | *Georgics* | 2188 |
| ovid-metamorphoses-lat.tsv, ovid-fasti-lat.tsv | 2042, 2043 | Ovid | 11927, 4971 |
| lucan-lat.tsv | 2029 | Lucan | 8303 |
| hesiod-worksdays-grc.tsv, hesiod-theogony-grc.tsv, hesiod-shield-grc.tsv | 728, 726, 730 | Hesiod | 831, 1042, 479 |
| aratus-phaenomena-grc.tsv | 1559 | Aratus | 1155 |
| hipparchus-in-aratum-grc.tsv | 3325 | Hipparchus, *Commentary on Aratus and Eudoxus* | 638 |
| hhymn02-demeter-grc.tsv, hhymn03-apollo-grc.tsv, hhymn04-hermes-grc.tsv, hhymn31-helios-grc.tsv, hhymn32-selene-grc.tsv | 497, 499, 501, 555, 557 | Homeric Hymns | — |
| dionysius-hal-antiquitates-grc.tsv | 1192 | Dionysius of Halicarnassus | 4256 |
| cassius-dio-grc.tsv | 1311 | Cassius Dio | 4679 |
| seneca-thyestes-lat.tsv | 2070 | Seneca, *Thyestes* | 1304 |
| euripides-electra-grc.tsv | 42 | Euripides, *Electra* (keys are speaker/line; "2.727" = l. 727) | 1741 |
| quintus-smyrnaeus-grc.tsv | 1600 | Quintus Smyrnaeus | 8804 |
| valerius-flaccus-argonautica-lat.tsv | 2081 | Valerius Flaccus | 5596 |
| heraclitus-allegoriae-grc.tsv | 3322 | Heraclitus, *Allegoriae* (*Homeric Problems*) | 172 |

**Not in the library** (checked with `find`):
- Archilochus; Stobaeus; Ennius; Pindar's *Paeans*; Phlegon; Censorinus; Macrobius; Sappho;
- all cuneiform: the Assyrian Eponym Chronicle, Ugarit KTU 1.78, the Astronomical Diaries.

**Present but not exported:** Pindar's victory odes (859–866); Geminus (3313); Cleomedes (3282); Autolycus (3262–3); Exodus (2983 LXX).

Other sessions have exported further files into the same folder (for example, aristonicus, suda, plato-timaeus, plutarch-de-facie-grc). Those are not mine.

## 10. Reproducibility
`C:\Projects\odybench\results\controls\` contains:
- `hz.py`: Horizons client with an on-disk cache in `hzcache/`;
- `local.py`: local circumstances;
- `ecl.py`: NASA catalogue lookup over `nasa/*.txt`;
- `run_solar.py`, `run_solar2.py`, `run_lunar.py`, `run_extra.py`, with their `*.out.txt` outputs.

Run them with `py <script>` from that folder. Cached runs need no network, except for the elongation queries in `run_extra.py` §3.

## 11. Open questions
1. What ṅ, and which ELP-2000/82 variant, did B&M's software (Starry Night Pro) use? This decides whether their ΔT of 27,602.7 s is equivalent to about 29,300 s in a DE frame and therefore total at Ithaca (section 2.3). The reproduction task should settle it.
2. Livy 38.36.4: is the time of day (third to fourth hour) compatible with 17 Jul 188 BC? My maximum is at 06:16 LMT.
3. *De facie*: the time-of-day objection (maximum about 11:00 LMT against "after noon") stands in my computation. Does it matter for using it as a control? It is grade B, not A.
4. Tarutius: is the coincidence of Choiak 23, Ol. 2.1 with the real partial eclipse of −771 Jun 24 already in the literature? Was the date computed with an eclipse cycle?
5. The Ugarit and Hittite cases: what ΔT does totality need at Ugarit and Hattusa, compared with the band that makes −1177 total at Ithaca? A joint ΔT constraint across the Bronze Age claims would be a strong cross-check.
6. Which edition note calls the archon and ephor heading in *Hell.* 1.6.1 a gloss? It needs verifying from a primary edition.
7. The ClassicaCodex *Syntaxis* text has literal "U+2220" and "??" artefacts. Is this a library ingest bug worth fixing on Jon's side?
