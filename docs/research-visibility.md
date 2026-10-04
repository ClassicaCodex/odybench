# Research: what the Odyssey's sky clues could mean observationally

Scope: bound the "forking paths" in Baikouzis & Magnasco (PNAS 105:8823-8828, 2008; "B&M"). For each sky clue this note gives:

- defensible numerical criteria, from strict to lenient, with sources;
- how often each criterion holds by chance, as a fraction of days or of new moons.

The four clues are: Venus (13.93-94), Mercury/Hermes (book 5), the Pleiades and "late-setting" Bootes (5.270-277), and the new moon (14.161-164, 19.306-307, with 14.457 and 20.155-156).

Companion code: `docs/research_visibility_calc.py`. Output: `results/research-visibility.json`. Cache: `results/research-visibility-mornings.npz`, about 12 MB, which can be regenerated.

## 0. Conventions, tags and method

**Dates.**
- All dates are in the proleptic Julian calendar.
- Years are written as historical year and astronomical year, e.g. 16 Apr 1178 BC (astr. -1177).
- In this era the vernal equinox fell on 1-2 April Julian [calc]. B&M give 1 April, 15:24 [B&M, Results]. So a Julian "April" here is seasonally about late March to April.

**Time scales.**
- Event times are local mean time (LMT) at Ithaca, which is UT + 1 h 22.8 m.
- The ephemeris runs in TT. Delta-T is Skyfield's built-in value: 28,786 s at -1177.
- B&M used 27,602.7 s [B&M, Methods]. Their SI gives 28,907 s for the EmapWin track, and 28,590 s from the Five Millennium Canon [B&M SI, Fig. S1].
- Visibility rates depend on Delta-T only through local clock time. A 20-minute shift is negligible here.

**Site and span.**
- Site: Ithaca, 38.37 N, 20.70 E, sea level.
- Base rates are computed over 1250-1115 BC (astr. -1249..-1114). That is 49,674 mornings and 1,683 conjunctions. B&M count 1,684 new moons [B&M, Methods].

**Ephemeris.** JPL DE441 excerpt `data/ephem/de441_m1320_m1030.bsp`, read with Skyfield 1.55.

**Fixed stars.**
- Own code: Hipparcos J2000 positions with linear proper motion, IAU-2006 precession (from Skyfield), and Meeus' low-precision Sun (ch. 25).
- This lets the same code run at -700 (Hesiod), where the DE441 excerpt has no coverage.
- Checks at -1177: the Meeus Sun is within 0.8' of DE441, and star places are within 1.0' of Skyfield/DE441 [calc].

**Planet visibility model.** The classical arcus-visionis (AV) test of Ptolemy, *Almagest* XIII.7. A planet counts as seen at its morning rising if the Sun's geometric altitude is at or below -AV at the moment of the planet's apparent rising. Altitude-at-twilight tests are given as alternatives. This is a rough model, not a physical extinction and sky-brightness model.

**Crescent model.**
- Yallop's q-test (NAO Technical Note 69, 1997), evaluated at his "best time".
- Also the frequently quoted rule "age >= 24 h and lag >= 48 min".

**Provenance tags used below.**
- [src: ...] means a primary or secondary source I read.
- [Od./Il. x.y] means the Greek text in `data/text/`.
- [Σ Od. x.y] means a Dindorf scholion in `data/text/scholia-odyssey-grc.tsv`.
- [calc] means computed by me with `docs/research_visibility_calc.py`.
- [inf] means my inference.
- [unread] means I rely on a secondary report and did not read the primary.

**Sources I could not read.**
- Gainsford, TAPA 142 (2012) 1-22, a published response to B&M: paywalled (SSRN and MUSE returned 403).
- Schaefer's visibility papers.
- Fatoohi, Stephenson & Al-Dargazelli, JHA 30 (1999), on Babylonian crescent first visibility.
- de Jong, JHA 43 (2012) on Venus. Its numbers are taken from de Jong (2019), fn. 9.
- West's commentary on *Works and Days*, and Kidd's on Aratus.

The B&M Supporting Information was read from a Wayback copy of the PNAS file. The PNAS and PMC copies are blocked by a bot check.

## Summary

| Clue | Strictest defensible reading | Leniently read | Chance rate, strict → lenient [calc] |
|---|---|---|---|
| 1. "Brightest star heralding Dawn" (13.93-94) | Venus rises ≥ 2 h before the Sun | some bright star (Venus, Jupiter, Sirius, Mars) rises before dawn | 20.5 % of days → 70 % of days. B&M's test (Venus rises ≥ 90 min early) holds 29.6 % of all days but only **15.8 %** of B&M's spring new moons (Day −5). |
| 2. Hermes = Mercury (book 5) | Day −34 within ±1 d of a given "turning point" and Mercury visible | within ±5 d of any of station, greatest western elongation (GWE) or rise-azimuth extremum | 0.7-2.1 % → 14 % of days. On B&M's spring Day −34: 1.4 % → 17 %. **Which "turning point" is chosen decides whether 1178 BC passes at all.** |
| 3. Pleiades + "late-setting" Bootes (5.272) | Both ≥ 10° up at the end of nautical dusk | both visible at some time in a dark night, or "late-setting" read as a permanent property | 6.8 % of the year → 87-100 %. B&M's own window ≈ 1 new moon a year (8.3 % of new moons). An autumn window of the same kind also exists. |
| 4. New moon (14.162, 19.307) | Day 0 = date of conjunction (ἕνη καὶ νέα) | the waning or waxing part (decade) of the month | 3.4 % of days → ≈ 68 % of days. The first crescent comes 1-2 evenings after a daytime conjunction (Yallop B: 75 % / 25 %). |

**Key findings**

1. **Venus.** Two readings of "morning star" ("φαάντατος … ἀγγέλλων φάος Ἠοῦς") give very different filters:
   - read loosely, as "Venus is a morning star" (Ptolemy's AV 5°: 44.8 %; de Jong's AV ≈ 7°: 42.4 %), it is a weak filter;
   - read as B&M's "rises ≥ 90 min before the Sun", it is strong and seasonal: 29.6 % of all days, but only 17 % in Julian April and 15.8 % on B&M's Day −5 of spring new moons [calc].
   - B&M's "≈ 1/3" [B&M, Results] is the all-season rate, not the rate in the season the stars clue selects.
   - The Greek says the star rose (ὑπερέσχε, cf. Il. 11.735 of the Sun rising); the word "high" is not in the text.
2. **Is the star necessarily Venus?** No.
   - Venus is a visible morning star on 42 % of days.
   - On another 23 % of days Jupiter (median −2.1 mag) is a morning object while Venus is not.
   - Sirius heralds dawn from about 27 Jul to 1 Sep (10 % of the year).
   - Some such "brightest dawn star" exists on about 70 % of days [calc].
   - Homer's names are separate: ἑωσφόρος (Il. 23.226) and ἕσπερος (Il. 22.318). The morning and evening star were first identified as one body in the 6th-5th c. BC (Pythagoras or Parmenides) [src: Diogenes Laertius 8.14, 9.23; Pliny NH 2.36-37].
3. **Mercury.** In the paper, B&M's operational test is that Day −34 falls within a few days of Mercury's **westernmost rising azimuth** [B&M, Methods]. "High at dawn" comes from the press summary, not the paper.
   - I reproduce their 12-13 Mar 1178 BC as the local maximum of Mercury's rise azimuth (azimuth from north, i.e. its most southerly rising point) [calc].
   - The conventional turning points fall elsewhere: morning station 5 Mar, GWE 19 Mar.
   - Under a "GWE or station within ±2-3 d" rule, 1178 BC **fails**, and 2 Apr 1250 BC passes instead. 25 Mar 1138 BC also passes with the parallel day count at ±3 d [calc].
   - Mercury was not high on Day −34 (13 Mar): it stood 6.0° up at civil dawn, magnitude +0.7.
   - Across all 135 years, Mercury is never ≥ 8° up at civil dawn in Julian March [calc].
   - Morning apparitions of Mercury are worst in spring. Babylonian texts mark them "omitted" when Mercury lies between 10° Aries and 20° Taurus [src: de Jong 2021 citing ACT 288]. Ptolemy says morning phases fail near the beginning of Taurus [src: *Alm.* XIII.8].
4. **Pleiades and Bootes.**
   - In 1178 BC at Ithaca, Arcturus' declination was +37.7°. It was above the horizon 17.2 h a day, and γ and β Boo never set.
   - The main stars of Bootes rise within about 0.4 h but set over about 3.7 h [calc].
   - So "late/slow-setting Bootes" is a literal permanent property, which is how the scholia and Aratus read it [Σ Od. 5.272; Aratus 581-585].
   - Read as an evening date-marker, there are **two** windows:
     - 16 Feb-3 Apr: B&M's spring window, reproduced to within a day of their 17 Feb and 3 Apr;
     - 20 Sep-29 Oct: the autumn window. This is the season Aratus attaches to Bootes' "late setting" (setting at ox-unyoking time).
   - Hesiod works as a positive control:
     - Pleiades hidden 40 days [WD 385-386] ⇔ AV ≈ 15° (computed 36-43 d at AV 14-16° in 701 BC);
     - Arcturus "at dusk" 60 days after the solstice [WD 564-567] ⇔ "Arcturus ≥ 5° up at nautical dusk" (26 Feb 701 BC = 60 d);
     - Pleiades rising and setting fall at harvest and ploughing [WD 383-384].
   - B&M's SI cites WD 618-621 (the Pleiades plunge into the sea) as the **April evening** setting. In Hesiod's sequence it is the **November morning** setting that ends the sailing season [inf, from WD 614-624].
5. **New moon versus Apollo's feast.**
   - A solar eclipse requires Day 0 = the date of conjunction, with the conjunction in daylight. That holds for 50.9 % of conjunctions at Ithaca [calc].
   - If the feast is the noumenia:
     - Geminus 8.11 defines the noumenia as the day of first appearance. The first crescent then comes 1 evening (75 %) or 2 evenings (25 %) after a daylight conjunction (Yallop B) [calc]. So, with Greek sunset-to-sunset days, the noumenia's daylight is 2-3 days after the eclipse. It is never the eclipse day.
     - Under Solon's administrative rule the noumenia is the day after the "old-and-new" day of conjunction [src: Plutarch, Solon 25.3]. The eclipse then falls the day *before* the feast.
   - Only the scholiasts' merged term "the thirtieth-and-noumenia" [Σ Od. 14.162; Heraclitus QH] lets the feast day and the eclipse day coincide.
   - Moving Day 0 by +1 day already removes 1178 BC from B&M's star window: its 17th sailing night is the Pleiades' last visible evening [calc; B&M, Results].
6. **σκοτομήνιος night (14.457).**
   - B&M's Table 1 places it after Day −5 (sequential) or Day −4 (parallel); their text says "Night −2".
   - With Day 0 = conjunction, the Moon is up a median 25 % (night after Day −5) or 16 % (Day −4) of the dark hours, illuminated 22 % / 13 %.
   - About 24-31 % of all nights are as dark or darker [calc]. It also rained all night (14.457-458).
7. **Chance hits.** These rough per-clue rates imply about 1.1 chance matches to B&M's joint test in 135 years (spring new moons ≈ 1.02 a year × Venus 0.158 × Mercury 0.050). B&M report one match (1178 BC) and two runners-up [B&M SI]. My rough rerun finds 1178 BC and a borderline 18 Mar 1189 BC [calc] [inf]. So the evidential weight rests on the hit coinciding with the eclipse new moon, and on the criteria having been fixed before looking. The null models must test exactly that.

---

## 1. Venus: "the brightest star, which comes announcing the light of early Dawn" (Od. 13.93-94)

### 1.1 What the text says

- **The Greek.** The passage reads εὖτ' ἀστὴρ ὑπερέσχε φαάντατος, ὅς τε μάλιστα / ἔρχεται ἀγγέλλων φάος Ἠοῦς ἠριγενείης, / τῆμος δὴ νήσῳ προσεπίλνατο ποντοπόρος νηῦς [Od. 13.93-95]. In paraphrase: when the brightest star rose above the horizon, the one that above all comes to announce early Dawn's light, then the ship drew near the island.
- **The verb.** ὑπερέσχε means "rose above" the horizon. The same verb is used of the Sun rising [Il. 11.735 ὑπερέσχεθε γαίης]. The scholion glosses it as ὑπερανέτειλεν, "rose up" [Σ Od. 13.93, Q]. Murray translates "when that brightest of stars rose" [`odyssey-murray.tsv` 13.93.1].
- **No "high".** Nothing in the text says "high". B&M infer that Venus rose well before dawn from the length of the following action, and require Venus to rise ≥ 90 min before the Sun on Day −5 [B&M, Methods]. The AP press summary calls Venus visible and high [src: Akroterion 53 (2008) 129-130, reprinting Schmid/AP, paraphrased].
- **Habitual wording.** "ὅς τε μάλιστα ἔρχεται" is a habitual description of the dawn star. The Iliad uses the same idea as a time-of-night marker: "when the dawn-bringer goes to announce light over the earth" [Il. 23.226 ἑωσφόρος] for the end of Patroclus' pyre night. The Odyssey's line therefore most naturally times the ship's arrival within the night [inf]. Read that way, it needs only that a bright morning star exist.

### 1.2 Visibility criteria in the literature

- **Ptolemy.** Arcus visionis 5° for Venus [src: *Almagest* XIII.7-8, Greek in `ptolemy-syntaxis-grc.tsv` 13.7.8 and 13.8.3: Venus 5°]. In the same passage: Saturn 11°, Jupiter 10°, Mars about 11½°, Mercury 10°.
- **Babylonian data.**
  - de Jong (2012) found Venus AV 6.1-8.6° depending on synodic phase. A nominal Babylonian extinction of 0.27 mag/airmass gives AV ≈ 7° [src: de Jong, AHES (2019), doi:10.1007/s00407-019-00224-0, fn. 9; the 2012 paper itself unread].
  - Elongation at first morning visibility is about −8°, and at last morning visibility about −10° [src: de Jong 2019, fn. 7].
  - Weather shifts the morning-first date by up to ±3 d and the morning-last date by up to ±15 d [src: de Jong 2019, citing de Jong 2012, p. 397].
- **Invisibility at inferior conjunction.** Ptolemy gives the gap from evening last to morning first as about 2 days near the beginning of Pisces and 16 days near the beginning of Virgo [src: *Alm.* XIII.8, `ptolemy-syntaxis-grc.tsv` 13.8.2].
- **One example cycle** [src: de Jong 2019, Fig. 1, 148-146 BC]:
  - 243 d from evening first to evening station;
  - 17 d to evening last;
  - 4 d invisible;
  - 20 d from morning first to morning station;
  - 240 d to morning last;
  - 64 d invisible.
  - That is about 260 days as a morning star out of a 589-day cycle.

### 1.3 Criteria and chance rates

Rates are fractions of all mornings, 1250-1115 BC, Ithaca [calc, `venus` section].

| Criterion (strict → lenient) | Source of the threshold | % of days |
|---|---|---|
| Venus ≥ 20° up when the Sun is at −12° (high at nautical dawn) | "high", my thresholds | 9.6 |
| Rises ≥ 180 min before the Sun | — | 9.3 |
| Rises ≥ 120 min before the Sun | B&M: in this season Venus rises at most about 2 h before the Sun | 20.5 |
| ≥ 20° up at civil dawn (Sun −6°) | — | 15.6 |
| ≥ 10° up at civil dawn | — | 30.9 |
| **Rises ≥ 90 min before the Sun** | **B&M's test [Methods]** | **29.6** |
| Rises ≥ 60 min before the Sun | — | 36.2 |
| Seen at morning rising, AV 10° | conservative | 38.5 |
| Seen at morning rising, AV 8.6° | de Jong 2012, maximum | 40.4 |
| Seen at morning rising, AV 7° | de Jong 2019, nominal | 42.4 |
| Seen at morning rising, AV 5° | Ptolemy | 44.8 |
| Venus west of the Sun (geometric morning side) | — | 50.0 |

**Fraction of the 584-day synodic cycle spent as a morning star** [calc, 85 complete apparitions]:

| | Mean | Range |
|---|---|---|
| AV 5° | 261 d (45 %) | 243-275 d |
| AV 7° | 248 d (42 %) | 225-264 d |
| Geometric, west of the Sun | 292 d (50 %) | — |

**Season matters for B&M's 90-minute test.** The ecliptic lies shallow at dawn in spring.

| Julian month | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Rises ≥ 90 min early (%) | 32 | 30 | 21 | **17** | 17 | 25 | 36 | 34 | 37 | 35 | 35 | 36 |
| Visible, AV 7° (%) | 45 | 40 | 41 | 39 | 38 | 44 | 41 | 44 | 47 | 42 | 48 | 42 |

**Rates on B&M's Day −5 (or −4), per new moon** [calc, `bm_rates`]:

| | Venus rises ≥ 90 min early | Venus visible, AV 7° |
|---|---|---|
| Spring new moons in B&M's window, Day −5 | 15.8 % | 43 % |
| Spring new moons in B&M's window, Day −4 | 16.6 % | 43 % |
| All new moons | 29.4 % | 43 % |

- An independent check, from a sibling transcription of B&M Table S2: the Venus test passes in 21 of 136 years (15 %) [src: `docs/research-bm2008-a.md`].
- **The 1178 BC case** [calc]: on 11 Apr 1178 BC (Day −5) Venus rose 103.7 min before the Sun, at magnitude −4.16. B&M give 1 h 43 min and −4.2 [B&M, Results].

### 1.4 Is "the morning star" necessarily Venus?

**Literary evidence.**
- Homer has a separate morning name and evening name: ἑωσφόρος [Il. 23.226] and ἕσπερος, "the fairest star set in heaven" [Il. 22.318].
- The morning and evening star were first identified as one body by Pythagoras, according to Parmenides [src: DL 8.14]. Favorinus credits Parmenides, others Pythagoras [src: DL 9.23]. Pliny puts the discovery about the 62nd Olympiad, roughly 530 BC [src: Pliny NH 2.36-37, `pliny-nh-eng.tsv` 2.6.4].
- So "the star that heralds dawn" is a role, which Venus fills most conspicuously [inf].
- The superlative is not unique to Venus. Sirius is λαμπρότατος [Il. 22.30], and the "autumn star" (Sirius) shines brightest with the same ὅς τε μάλιστα formula [Il. 5.5-6].

**Other "brightest dawn star" candidates** [calc, `venus.herald`, `herald`]:

| Who heralds dawn | % of days |
|---|---|
| Venus a visible morning star (AV 7°) | 42.4 |
| Jupiter a visible morning object (AV 10°, median mag −2.1), Venus not | 23.2 |
| Jupiter rising 30-240 min before the Sun, Venus not | 8.9 |
| Sirius rising 30-240 min before sunrise and seen (AV 10°): 27 Jul-1 Sep | 10.1 |
| Mars brighter than −1 mag as a visible morning object | 3.5 |
| **Any of Venus, Jupiter, Sirius or Mars** | **70.0** |
| None of them | 30.0 |

- Venus is always the brightest of these when it is visible: its faintest is −3.8 mag, while Jupiter's brightest is −2.9 mag [calc].
- So if the clue means "the brightest object that heralds dawn", it excludes only about 30 % of days. If it means Venus specifically, it excludes about 55-58 %.

---

## 2. Mercury (Hermes' journey to Ogygia, Od. 5.43-58, 5.97-103)

### 2.1 The reading under test

- **What B&M actually test.** Hermes flies from Pieria, falls onto the sea, skims the waves like a gull (λάρῳ ὄρνιθι), and steps ashore from the violet sea at the far island [Od. 5.49-56]. He complains about the length of the trip [Od. 5.99-102]. B&M treat this as an allegory of Mercury reaching a western turning point [B&M, Methods]. Their operational test is that Day −34 falls within a few days of the date when Mercury's rising azimuth is at its westernmost, and that Mercury is visible [B&M, Methods, paraphrased].
- **The press version.** The AP report has Mercury high at dawn near the western end of its path [src: Akroterion 53, AP text, paraphrased]. That is a gloss, not the paper's criterion.
- **Day counts.** The paper uses Ti−5 / Ti−29 / Ti−34 (sequential). The press version gives "six / twenty-nine / thirty-three days before" [src: same].
- **Evidential gap.** B&M acknowledge that the first surviving Hermes-Mercury link is in Plato [B&M, Historical Plausibility]. I did not check the Plato passage.

### 2.2 Visibility criteria in the literature

- **Ptolemy.** Mercury's arcus visionis is 10° [src: *Alm.* XIII.7, Greek 13.7.8: "τῶν δὲ ιβ∠γʹ πρὸς τὰ ι"]. Mercury's morning phases fail when they would fall near the beginning of Taurus, and evening phases near the beginning of Scorpio [src: *Alm.* XIII.8, 13.8.2].
- **Babylonian data**, from de Jong, "A study of Babylonian planetary theory III. The planet Mercury", AHES 75 (2021) 491-522, doi:10.1007/s00407-020-00269-6 (open access, read):
  - Mercury is invisible about half the time.
  - Solar elongation at morning first visibility and at the morning station is −17° ± 4°.
  - About one in seven pairs of first/last appearances is recorded as "omitted" (16 pairs among 220 observations).
  - Morning appearances are omitted in spring (April-June). The ACT rule: morning phases are omitted when Mercury is between 10° Aries and 20° Taurus (citing ACT p. 288).
  - First and last appearances happen at about 5° altitude.
  - With extinction k = 0.27 mag/airmass (Babylon average), 15 of 97 synthetic morning visibilities are omitted. With k ≤ 0.20 none are.
  - de Jong quotes a 669 BC letter (25 March) complaining that one day Mercury may be too early to see and on another lie flat on the horizon [secondary, via de Jong; Parpola letter 53 unread].
- **Schaefer.** Schaefer's physical models (extinction plus sky brightness) are the standard modern tool, but I did not read them [unread]. Here the AV bands stand in for them.

### 2.3 Criteria and chance rates

Rates are fractions of all mornings, 1250-1115 BC [calc, `mercury` and `mercury_events`].

**Position and visibility tests.**

| Criterion (strict → lenient) | % of days |
|---|---|
| ≥ 10° up at civil dawn, morning side ("high at dawn") | 9.1 (Julian Mar: 0.0; Apr-Jul: 0.0) |
| ≥ 5° up at civil dawn | 19.8 (Mar: 12.4; Apr-May: 0) |
| West elongation ≥ 25° | 4.5 |
| West elongation ≥ 18° | 19.1 |
| Seen at morning rising, AV 12° | 18.6 (with mag ≤ +1: 17.1) |
| Seen at morning rising, AV 10° (Ptolemy) | 23.5 (with mag ≤ +1: 20.9) |
| Seen at morning rising, AV 8° | 30.8 |
| Morning side, geometric | 49.9 |

**Turning-point tests**, as % of days for ±k days around the event.

| Event | ±0 d | ±1 d | ±2 d | ±3 d | ±5 d | ±7 d |
|---|---|---|---|---|---|---|
| GWE | 0.86 | 2.6 | 4.3 | 6.1 | 9.5 | 13.0 |
| GWE, Mercury visible (AV 10°) | 0.70 | 2.1 | 3.5 | 4.9 | 7.6 | 10.2 |
| Morning station (retrograde → direct, the "sterigmos"), visible | 0.59 | 1.8 | 2.9 | 4.1 | 6.2 | 8.0 |
| Morning first visibility, AV 10° | — | 2.2 | — | 5.1 | 8.0 | — |
| Rise-azimuth maximum, morning side, visible | — | 0.73 | 1.2 | 1.7 | 2.7 | — |
| **Any of GWE / station / rise-azimuth maximum**, visible | — | 4.5 | 7.5 | 10.2 | 13.9 | — |

- **Counts.** GWE comes 3.15 times a year (mean spacing 115.9 d). The rise-azimuth maximum while Mercury is a visible morning object comes only 0.89 times a year, because it depends on the season [calc].
- **Spacing of the three "turning points".** The morning station precedes GWE by 12-15 d (mean 13.5 d). The rise-azimuth maximum falls anywhere from 26 d after to 9 d before GWE [calc]. B&M describe these events as close in time but not coinciding [B&M, Methods, paraphrased]. In fact they span up to two weeks or more, so choosing among them is a real fork.
- **Omitted morning apparitions** (no morning sighting within ±15 d of a GWE): AV 10°: 69 of 429 (16 %); AV 12°: 115 of 429 (27 %); AV 8°: 0 [calc]. The Babylonian 15/97 (15 %) [de Jong 2021] matches AV 10°.

**Seasonal visibility, AV 10°**, % of mornings by Julian month [calc]:

| Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 42 | 38 | 25 | 2 | 0 | 4 | 17 | 21 | 26 | 31 | 36 | 41 |

**Rates on B&M's Day −34, for spring new moons in their star window** [calc, `bm_rates`]:

| Criterion | ±1 d | ±2 d | ±3 d | ±5 d |
|---|---|---|---|---|
| GWE, visible | 1.4 % | 2.9 % | 4.3 % | 8.6 % |
| GWE or station, visible | 3.6 % | 6.5 % | 8.6 % | 17.3 % |
| Rise-azimuth maximum, visible | — | 5.0 % | 7.9 % | — |

### 2.4 The 1178 BC case under each reading [calc, `mercury_events.window_1178BC`]

| Event | Date |
|---|---|
| Inferior conjunction | 20 Feb 1178 BC (astr. −1177) |
| Morning station | 5 Mar |
| Local maximum of rise azimuth | 12 Mar (112.29° from north, the same value on 12 and 13 Mar); B&M give "12 and 13 March" |
| **Day −34** | **13 Mar** |
| GWE (27.1°) | 19 Mar |

**Morning visibility runs:**
- AV 8°: 25 Feb-5 Apr.
- AV 10°: 28 Feb-29 Mar.
- AV 12°: 5-21 Mar.
- B&M's PLSV model (1° minimum altitude) puts first visibility on 13 Mar [B&M, Results].

**On 13 Mar 1178 BC (Day −34):**
- elongation 26.1° W;
- rising 63 min before the Sun, with the Sun at −13.1° at Mercury's rising;
- magnitude +0.7;
- **6.0° up at civil dawn**: a typical, not a "high", spring apparition.

**Consequences for B&M's joint test** (star window; Venus rises ≥ 90 min early on Day −5; Mercury visible at AV 10° on Day −34) [calc, `bm_rates.joint_hits_1250_1115BC`]:

| Mercury criterion | Hits, 1250-1115 BC |
|---|---|
| Rise-azimuth maximum ±2 d | 18 Mar 1189 BC (on the edge of the star window) and **16 Apr 1178 BC** |
| GWE or station ±2 d | 2 Apr 1250 BC only (1178 BC fails) |
| GWE or station ±3 d, with Day −4/−33 | adds 25 Mar 1138 BC |
| Rise-azimuth maximum ±3 d, with Venus ≥ 60 min | adds 24 Mar 1157 BC (one of B&M's runners-up [B&M SI]) |

---

## 3. Pleiades and "late-setting" Bootes (Od. 5.270-277)

### 3.1 What the text says, and how the ancients read it

**The passage.** Πληιάδας τ' ἐσορῶντι καὶ ὀψὲ δύοντα Βοώτην [Od. 5.272], said of Odysseus, sleepless at the steering oar, watching these stars and keeping the Bear on his left [5.273-277]. ὀψέ means "late"; compare δείελος ὀψὲ δύων, "late-setting evening" [Il. 21.232]. The text names no time of night and no season.

**Scholia on 5.272** [Σ Od. 5.272, Dindorf; keys `1.5.2.239-249`]:
- Bootes is "slow-setting" (βραδέως δυόμενον) because it lies upright when setting and takes a long time to go down, setting together with four zodiacal signs.
- Another note reads ὀψὲ δύοντα as "setting long after the stars that rose with it", quotes Aratus on the four signs, and names them as Scorpio through Aquarius.
- One note says Bootes is "the same as Arcturus".
- Another says Bootes appears in the evening, when oxen are freed from the yoke.

**Aratus, Phaenomena 581-585** [`aratus-phaenomena-grc.tsv`]. Paraphrased:
- Ocean receives Bootes over four signs together.
- When he sets with the setting Sun, at ox-unyoking time, his setting fills more than half the night.
- Those nights are named after his late setting (ἐπ' ὀψὲ δύοντι).
- [inf] Aratus thus reuses Homer's phrase both for a permanent property (slow setting) and for a *season*: nights when Bootes begins setting at dusk, i.e. autumn.

**Geminus 14.11** [`geminus-grc.tsv`]. Arcturus is ἀμφιφανής: on many nights it is seen setting after sunset and rising before sunrise in the same night.

**B&M's reading** [B&M, Methods; SI]:
- Odysseus sets sail at sunset on Ti−29 and sees both stars at nautical twilight.
- Bootes "sets late", in fact staying visible all night.
- Spring (17 Feb-4 Apr) rather than September.
- All 17 sailing nights must fall inside the window.
- They follow T. L. MacDonald [unread].

### 3.2 The sky in 1178 BC at Ithaca [calc, `stars`]

**Places of date in 1178 BC.**

| Star | RA | Dec |
|---|---|---|
| Arcturus | 177.0° | **+37.7°** (today +19.2°) |
| Alcyone (Pleiades) | 13.2° | +9.8° |
| γ Boo | — | +54.5° |
| β Boo | — | +55.6° |
| δ Boo | — | +48.2° |

- At 38.37° N, stars north of about +51.1° never set. So **γ and β Boo were circumpolar**.
- Arcturus was above the horizon **17.2 h** a day; Alcyone 13.1 h.
- The non-circumpolar stars of the figure (Arcturus, η, ε, δ) rise within 0.43 h of each other, but set over **3.69 h**. Hesiod's era is similar: in 701 BC the spans were 0.32 h rising and 3.28 h setting, with γ and β still circumpolar.
- So "late/slow-setting Bootes" is literally true every night of the year in the Late Bronze Age and in archaic Greece [calc]. Read this way, the clue carries no date [inf].

### 3.3 Annual phases and the Hesiod positive control

**Ancient star calendar for 1178 BC (astr. −1177), 38.37° N** [calc, AV bands]:

| Phenomenon | Arcturus (AV 8-12°) | Pleiades / Alcyone (AV 12-18°) |
|---|---|---|
| Morning first, heliacal rising | 8-13 Sep | 7-22 May |
| Evening last, heliacal setting | 5-12 Nov | 31 Mar-6 Apr |
| Last visible evening rising (acronychal, "rises at dusk") | 12-16 Feb | 31 Aug-14 Sep |
| First visible morning setting (cosmical) | 13-20 Jun | 3-9 Nov |
| Days wholly invisible | none (ἀμφιφανής Sep-Nov) | 30-52 d (AV 15° ≈ 41 d) |

**Positive control: Hesiod, about 700 BC** [calc for 701 BC (astr. −700), same site]:

| Hesiod | Computed | Verdict |
|---|---|---|
| Pleiades hidden 40 nights and days [WD 385-386] | 36 d (AV 14°), 43 d (AV 16°), so **40 d ⇔ AV ≈ 15°** | calibrates the Pleiades AV. B&M SI give about 44 days, depending on latitude. |
| Harvest at the Pleiades' rising, ploughing at their setting [WD 383-384]; plough when Pleiades, Hyades and Orion set [WD 615-617] | morning first 13-18 May; cosmical setting 7-9 Nov | fits the Greek harvest and ploughing seasons |
| Arcturus "first rises brilliant at dusk" 60 days after the winter solstice [WD 564-567] | solstice 28 Dec 702 BC. Rising seen at dusk on 17-21 Feb = 50-54 d. Arcturus ≥ 5° up at nautical dusk from **26 Feb = 60 d** | Hesiod's 60 matches "already clearly up at nightfall" |
| Vintage when Dawn sees Arcturus [WD 609-611] | Arcturus morning first 12-16 Sep | fits |
| WD 618-621: Pleiades flee Orion and "fall into the misty sea"; storms; haul the ship ashore [622-624] | morning setting early November | B&M SI attach this to the April evening setting. Hesiod's context (ploughing, the end of sailing) points to November [inf]. |

**B&M's limits reproduced** (end of nautical twilight, Sun −12°) [calc]:

| Limit | Mine | B&M [Methods] |
|---|---|---|
| Arcturus first up at nautical dusk | 12 Feb (≥ 0°), 16 Feb (≥ 2°) | 17 Feb |
| Pleiades last up at nautical dusk | 6 Apr (≥ 0°), **3 Apr (≥ 2°)** | 3 Apr |

### 3.4 Criteria and chance rates [calc, 1178 BC; 701 BC within ±1-3 d]

**Evening co-visibility, both stars at the end of nautical twilight (Sun −12°).**

| Minimum altitude | Windows | % of year |
|---|---|---|
| ≥ 10° | 1-25 Mar only | 6.8 |
| ≥ 5° | 21 Feb-30 Mar and 27 Sep-20 Oct | 17.0 |
| ≥ 2° | 16 Feb-3 Apr and 20 Sep-29 Oct | 23.8 |

- At the Sun −18° the spring window shifts about 6-7 d earlier (10 Feb-27 Mar at ≥ 2°).

**B&M's strict reading.** Both stars must be visible at nautical dusk (≥ 2°) on the departure night *and on all 17 sailing nights*. This gives Ti ∈ [18 Mar, 16 Apr]: **1.02 new moons a year = 8.3 % of new moons**. Adding the equinox requirement (1 Apr ≤ Ti−11 ≤ 5 Apr) leaves 1 new moon per 6.2 years [calc]. B&M give one such new moon every 6 years [B&M, Results].

**Other readings.**

| Reading | Windows | % of year (or new moons) |
|---|---|---|
| The same strict reading, autumn window instead | Ti−29 ∈ [20 Sep, 12 Oct] | about 0.8 new moons a year [inf from runs] |
| Departure night only, either season | — | 23.8 % (about 24 % of new moons) |
| Both stars at morning nautical twilight, ≥ 2° | 12 May-14 Jun and 16 Sep-30 Oct | 21.6 |
| Both up together at some moment of a dark night, ≥ 5° | all but 31 Mar-17 May | **86.8** |
| Both up together at some moment of a dark night, ≥ 10° | — | 49 |
| Both up together at some moment of a dark night, ≥ 20° | — | 43 |
| "Late-setting" = Arcturus visible at dusk and up all night | 16 Feb-19 Jun | 34 |
| "Late-setting" = Arcturus sets after local midnight, before dawn | 20 Jun-9 Aug | 14 |
| "Late-setting" in Aratus' sense = Arcturus sets within 2 h after nautical dusk, with Bootes' setting lasting > half the night | 18 Sep-5 Nov | 13 |
| "Late/slow-setting" as a permanent property (scholia, Aratus 581-582) | — | 100 |

**Forking paths [inf].**
- The clue fixes a season only if read as an *evening* snapshot. Even then it allows two seasons.
- B&M choose spring because Bootes stays up all night, which is their sense of "late-setting".
- The ancient commentators read ὀψὲ δύοντα as "slow-setting".
- Aratus's own "late-setting nights" are the autumn evenings. Those also offer the Pleiades (rising) and Bootes (setting) together after dusk.
- If Odysseus watched through the night, as "sleep did not fall on his eyelids" implies, the clue holds on 87 % of nights.

---

## 4. The new moon: conjunction, last crescent, or first crescent?

### 4.1 The texts and the ancient readings

**The lines.**
- Odysseus swears "τοῦδ' αὐτοῦ λυκάβαντος ἐλεύσεται ἐνθάδ' Ὀδυσσεύς, / τοῦ μὲν φθίνοντος μηνός, τοῦ δ' ἱσταμένοιο" [Od. 14.161-162, said to Eumaeus on B&M Day −5/−4]. He repeats it to Penelope on the eve of the slaughter [Od. 19.306-307].
- λυκάβας is itself uncertain:
  - the scholia gloss it as ἐνιαυτός, "year" [Σ Od. 19.306, B; Σ Od. 14.161, Q];
  - Butler renders "this self same year";
  - Murray renders "this self-same day" at 14.161 and "this very month" at 19.306 [`odyssey-butler.tsv`, `odyssey-murray.tsv`].
- **Hesiod's usage of the same pair.** He speaks of the 4th day "of the waning and of the waxing" month [WD 797-798, τετράδ' … φθίνοντός θ' ἱσταμένου τε]. φθίνων and ἱστάμενος name the *parts* of the month. So the Homeric phrase can mean "in the waning part of this month or the waxing part of the next", not a single day [inf].

**Ancient readings that make it the day of conjunction.**
- Scholia on 14.162: "the thirtieth and the noumenia". Vind. 133 adds: "that is, the ἕνη καὶ νέα" [Σ Od. 14.162, Q, V, Vind. 133].
- Plutarch: Solon called the day on which the Moon overtakes the Sun "old and new". The part before conjunction belongs to the ending month, the rest to the new one. Solon was "the first … to understand Homer's verse" rightly. The *following* day was called noumenia [src: Plutarch, Solon 25.3].
- Athens used the same term for the last day of the month [Aristophanes, Clouds 1131-1134, 1178-1200].
- Heraclitus: an eclipse can fall only on "the so-called thirtieth and noumenia, which the Attic people call ἕνη καὶ νέα", a rule he says Hipparchus made exact. He quotes 14.162 for the timing [src: Heraclitus, Homeric Problems; ch. 73.2 in the 1st1K edition `heraclitus-allegoriae-grc.tsv`; chapter numbers differ between editions].
- Plutarch, De facie: Homer's line about the Sun perishing from heaven refers to the Moon, and to an eclipse at the turn from the waning to the waxing month (paraphrase) [src: Plutarch, De facie 19, Greek and Cherniss tr. in `data/text/`].
- P. Oxy. 53.3710, a 2nd-c. AD commentary on Od. 20 [secondary: sententiaeantiquae.com, 2017; papyrus unread]:
  - Aristonicus says it was the new moon, connecting this with Apollo as the Sun;
  - Aristarchus of Samos is cited for eclipses happening at the new moon.

**Apollo's feast and the new moon.**
- The day of the slaughter is a feast "for all" [Od. 20.155-156]. The heralds lead a hecatomb to Apollo's grove [Od. 20.276-278]. It is the god's holy feast [Od. 21.258], and the goats are for Apollo the archer [Od. 21.265-267].
- The scholion on 20.155, citing Philochorus [Σ Od. 20.155, V]:
  - the *neomenia* is held sacred to all the gods;
  - it is Apollo's day as the source of first light;
  - he is called Νεομήνιος.
- Another scholion: the poet sets the attack on the noumenia of Apollo [Σ Od. 20.156, V].
- So the new-moon link comes from the scholia, not from the poem.
- Hesiod gives Apollo a different monthly day: the 7th is holy because Leto bore Apollo on it [WD 770-771]. That is an alternative festival day at first-quarter Moon [inf].

**Ancient definitions of the noumenia.**
- Geminus: conjunction falls "around the thirtieth" [src: Geminus 8.1].
- The day on which the Moon "appears new" is the noumenia [src: Geminus 8.11].
- The crescent appears "at the earliest on the noumenia, at the latest on the third" [src: Geminus 9.14].

**The eclipse reading in antiquity.** The scholia deny that an eclipse happened: Theoclymenus foresees that the Sun will fail *for the suitors* [Σ Od. 20.356, B, V].

### 4.2 What the Moon actually did [calc, `moon`; 1,683 conjunctions, 1250-1115 BC, Ithaca]

- **Daylight conjunctions** (needed for a visible solar eclipse at Ithaca): 50.9 %.

**First evening of crescent visibility, counted from the date of conjunction.**

| Criterion | Same evening | +1 | +2 | +3 | Age at first sighting (min / median) |
|---|---|---|---|---|---|
| Yallop A (easily visible) | 0 % | 57 % | 42 % | 1 % | 21.9 h / 41.5 h |
| **Yallop B (naked eye, perfect conditions)** | 1.7 % | 69 % | 29 % | 0.4 % | **15.6 h** / 37.4 h |
| Yallop B, daylight conjunctions only | **0 %** | **75 %** | **25 %** | 0 % | — |
| Yallop C (lenient) | 4 % | 76 % | 20 % | 0.1 % | 15.1 h / 34.4 h |
| Age ≥ 24 h and lag ≥ 48 min | 0 % | 60 % | 35 % | 5 % | 24.0 h / 40.7 h |

- Cross-check: the USNO records the youngest reliable naked-eye sighting at 15.5 h after new moon, and first visibility "about one day" after for good observers [src: aa.usno.navy.mil/faq/crescent].

**Last morning of the old crescent** (Yallop B):
- on the morning before the conjunction date: 68 %;
- two mornings before: 31 %;
- on the conjunction date itself: 0.3 %.

**Dates with no crescent in either twilight** (Yallop B):

| Number of such dates | 1 | 2 | 3 |
|---|---|---|---|
| Share of lunations | 43 % | 52 % | 4 % |

The mean is 1.6 such dates per lunation, or 5.4 % of days.

### 4.3 The eclipse versus Apollo's feast

B&M's chain of reasoning is: Day 0 = new moon = Apollo's feast = eclipse day [B&M, Methods; Table 1]. The quantified tension [calc for distributions; inf for calendar mapping]:

| If the feast (Day 0) is … | Days from the solar eclipse (conjunction date) to the feast's daylight | P(eclipse on the feast day) |
|---|---|---|
| ἕνη καὶ νέα = date of conjunction (scholia's "thirtieth-and-noumenia"; Heraclitus) | 0 | possible: B&M's reading |
| noumenia by Solon's rule, the day after ἕνη καὶ νέα (Plutarch, Solon 25.3) | +1 | 0 |
| noumenia = first crescent (Geminus 8.11), day counted from sunset (Greek usage [inf]) | +2 (75 %) or +3 (25 %), Yallop B | 0 |
| noumenia = first crescent, day counted from dawn | +1 (75 %) or +2 (25 %) | 0 |
| Apollo's 7th (Hesiod WD 770-771) | about +6 to +7 | 0 |

**Effect on the other clues if Day 0 moves 1-3 days after the conjunction** [calc, `bm_rates`]:
- **Venus test:** essentially unchanged; the Day −5 rate moves by less than 1 point.
- **Star window:** 1178 BC is at its very edge. Ti−12 = 4 Apr is the Pleiades' last visible evening [B&M, Results]; I get 3 Apr at ≥ 2° and 6 Apr at ≥ 0°.
- With Day 0 = conjunction + 1 (Solon's noumenia), **1178 BC drops out** of the joint test under the rise-azimuth criterion, leaving 1189 BC. Under the GWE-or-station criterion the hits remain 1250 BC, plus 1138 BC at ±3 d.

### 4.4 Criteria for "as this month wanes and the next begins" (14.162 / 19.307)

| Reading (strict → lenient) | Basis | % of days |
|---|---|---|
| The date of conjunction (ἕνη καὶ νέα) | Plutarch, Solon 25.3; Σ 14.162; Heraclitus | 3.4 |
| A day with no crescent visible at all | observation | 5.4 |
| Conjunction ±1 day | uncertainty in the day boundary or in observing the conjunction | 10.2 |
| From the last old crescent to the first new crescent, inclusive | observation | ≈ 12 |
| Last decade of this month or first decade of the next | Hesiod WD 797-798 usage | ≈ 68 |
| Any time "within this λυκάβας" (year) | Σ 19.306 | 100 |

### 4.5 The "moonless" night (Od. 14.457, νὺξ … σκοτομήνιος)

- **Placement.** The night falls within xiii.93-xiv.533, the day Odysseus reaches Eumaeus. B&M's Table 1 makes that Day −5 (sequential) or Day −4 (parallel). Their text calls it "Night −2" [B&M, Methods vs Table 1]: an internal inconsistency.
- **Moonlight under each reading** [calc]:

| Reading | Night | Moon up, share of dark hours (median, range) | Illuminated |
|---|---|---|---|
| Day 0 = conjunction | after Day −5 | 25 % (2-53 %) | 22 % |
| Day 0 = conjunction | after Day −4 | 16 % (0-41 %) | 13.5 % |
| Day 0 = conjunction | after Day −2 | 0 % | 3 % |
| Day 0 = first-crescent noumenia (Yallop B) | after Day −5 | 4 % | — |
| Day 0 = first-crescent noumenia (Yallop B) | after Day −4 | 0 % | — |

- **Base rates over all nights:**
  - the Moon is up for less than 25 % of dark hours on 31.6 % of nights, and less than 10 % on 20.1 %;
  - nights at least as dark as B&M's median Night −4 or −5 make up 24-31 %.
- It also "rained all night" with a strong west wind [Od. 14.457-458]. So "σκοτομήνιος" may describe a dark night for weather as much as for the Moon [inf].

---

## 5. What these rates imply for the bench [inf]

**B&M's frequency argument.** B&M multiply three things [B&M, Results, paraphrased]:
- one candidate new moon every 6 years (stars plus equinox);
- the Venus test passing 1/3 of the time;
- Mercury's station recurring every 116 days, treated as an exact-day event.

That gives an exact match about once in 2,000 years.

**Problems with that argument.**
- The equinox clue was *not* applied in their search [B&M, Methods].
- The Venus rate in the relevant season is about 1/6, not 1/3.
- The Mercury test actually used allows "a few days". That makes it 5-8 % of spring Day −34s, not 1/116 ≈ 0.9 %.

**Rough chance count with my rates.** About 1.02 spring new moons a year × 0.158 (Venus) × 0.050 (Mercury, rise-azimuth maximum ±2 d) ≈ 0.008 a year. That is about 1.1 expected chance matches in 136 years. B&M found one match plus two runners-up (1157 and 1191 BC) [B&M SI]. My crude rerun finds 1178 BC and a borderline 1189 BC [calc].

**What the bench must test.**
- **The coincidence itself.** Does the match land on the eclipse new moon more often than chance would? For a single pre-chosen new moon, the chance that all criteria pass is roughly 0.158 × 0.05 ≈ 0.8 %, given that it is in the spring window. It is about 0.07 % unconditionally (× 8.3 % for the window).
- **Forking paths.** How much the forks multiply those odds. The forks:
  - the Mercury turning point (3 or more choices, ±k);
  - the Venus threshold (visibility versus ≥ 60/90/120 min);
  - the star reading (spring versus autumn versus none);
  - sequential versus parallel day counts;
  - the definition of Day 0 (conjunction versus noumenia, +0 to +3).
- **Which forks are decisive.** Two are not harmless:
  - the Mercury turning point: with GWE or station, 1178 BC fails;
  - the definition of Day 0: at +1 d, 1178 BC falls out of the star window.

## 6. Open questions and limitations

1. **Visibility models are crude.** Planets use arcus-visionis bands; Mercury's brightness enters only through a magnitude cut. A Schaefer-type extinction and sky-brightness model (or de Jong's criterion) should replace the AV bands before final numbers. Weather variability alone moves first and last dates by ±3 to ±15 d [de Jong 2019].
2. **What B&M's "westernmost rise-time azimuth" means.** My reproduction (local maximum of azimuth from north) matches their 12-13 Mar, but the definition should be confirmed against their Table S2 column "MWRA" across all years. A sibling document reconstructs it: `docs/research-bm2008-a.md`.
3. **Unread sources.** Gainsford (TAPA 2012), Fatoohi et al. (JHA 1999) and de Jong (JHA 2012) are unread here. Gainsford may already list several of the forks above.
4. **The Greek day boundary.** Sunset-to-sunset is standard for classical Athens. I did not verify a primary source for it here, nor whether Homeric day-counting is dawn-based (the poem counts days by dawns). This shifts the noumenia offsets by one day.
5. **The autumn window as a null.** Should the autumn star window (20 Sep-29 Oct evenings, Aratus' "late-setting" season) be run as an alternative reading in the null models? It doubles the number of candidate new moons.
6. **Hesiod's 60 days.** Hesiod's "60 days" fits only the "≥ 5° at nautical dusk" definition; the strict "rising seen at dusk" gives 50-54 d. Is this good enough to use as a positive control for the star-visibility thresholds, or does it show those thresholds are underdetermined?
7. **One site only.** All rates are for Ithaca. Other candidate Ithacas, such as Paliki/Kefalonia, differ by less than 0.5° in latitude, so the change should be negligible, but it was not checked.
