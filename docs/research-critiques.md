# Responses to the "Odyssey eclipse" dating: Schoch (1926) to Baikouzis & Magnasco (2008)

Research note for odybench. Written 2026-10-03.

**Scope.** This note collects every published response, critique, replication or follow-up I could find to:

- the identification of Theoclymenus' vision (Od. 20.351-357) with the total solar eclipse of 16 April 1178 BC (astronomical year -1177), made by Schoch (1926) and P. V. Neugebauer (1929);
- the multi-clue dating of the same day by Baikouzis & Magnasco (PNAS 2008, "B&M" below).

It also gives the NASA Five Millennium Canon entry for that eclipse, my own computation of how it looked from the Ionian islands, and a list of every other eclipse of magnitude above 0.8 there between 1300 and 1050 BC.

**Conventions.** Every year is given twice, historical and astronomical: 1178 BC = -1177. All calendar dates are proleptic Julian unless marked otherwise. Time scales:
- **TT**: Terrestrial Time. The canon calls it TD.
- **UT**: Universal Time, equal to TT - ΔT.
- **LMT**: local mean solar time, equal to UT + longitude/15. At Vathy on Ithaki (20.717° E) that is UT + 1 h 22 m 52 s.
- **LAT**: local apparent (sundial) solar time.

**Provenance tags.**
- **[read]** means I read the primary text myself. A location follows it.
- **[secondary: X]** means I know the item only through X.
- **[computed]** means I computed it myself. The tool is named. The scripts are in `C:\Projects\odybench\results\research-critiques\`.
- **[inference]** marks my own reasoning, as opposed to anything a source states.

---

## 0. Findings in brief

1. **The canon itself does not make Ithaca total.** I used the canon's own Besselian elements and its ΔT of 28,590 s.
   - At Vathy (Ithaki) the 16 April 1178 BC eclipse is a deep partial: magnitude 0.984, 98.8% of the disc covered, maximum at 10:22 UT (11:45 LMT) with the Sun 57° high.
   - The southern limit of totality passed about 90 km north of Vathy, measured along Vathy's meridian. The path covered Corfu and Paxoi, but not Lefkada, Ithaki or Kefalonia.
   - Ithaki is total only if ΔT lies between 28,802 and 29,584 s. The probability of that is about 0.25 under the canon's own Huber error model (σ = 1,008 s), and about 0.30 under the HMNAO error (σ = 720 s). **[computed]** (§2.3)
   - Schoch's own 1926 computation already put the southern limit of totality right on Ithaca. **[read]** (§1.1)
2. **"The only eclipse of the century" is not true inside B&M's own search window.** On the same canon elements, the eclipse of 30 September 1131 BC (-1130) is *total* at Ithaki: magnitude 1.049, 3 m 39 s of totality, maximum at 09:49 UT = 11:12 LMT. That date lies inside B&M's 1250-1115 BC window. Schoch's window (-1240 to -1140) stopped just short of it. Under the same ΔT error model its probability of totality at Ithaki (0.41-0.49) is *higher* than 1178 BC's (0.25-0.30). **[computed]** (§2.4)
3. **The only full scholarly rebuttal of B&M is Gainsford (TAPA 142, 2012).** I read it in full.
   - He argues that four of B&M's five astronomical "references" fail:
     - Hermes = Mercury has no ancient parallel and is cherry-picked.
     - "Late-setting Boötes" is mistranslated, and its context is a formulaic repetition of Il. 18.
     - The equinox clue is geographically wrong.
     - The Venus clue depends on the season.
   - He argues that the 135-year window is too narrow.
   - He argues that the poem's day-count is too poetic and too incoherent to bear a rigid chronology.
   - He accepts only the new-moon clue. (§3.3)
4. **I found no formal statistical critique** (null model, look-elsewhere correction, sensitivity analysis) of B&M in the literature, 2008-2026. The statistical objections in print are verbal:
   - Gainsford on cherry-picking and "illusory coherence";
   - J. Evans ("castle of cards") and R. H. van Gent (the coherence is what needs explaining), both quoted in *Science News* in 2008.
   §4 lists the degrees of freedom a bench should test. **[inference]**
5. **The ancient reading is split, and the split is old.**
   - Both Odyssey scholia on 20.356-357 flatly deny an eclipse: "οὐ γὰρ ἡλίου ἔκλειψις ἐγένετο", "for no eclipse of the Sun occurred" (schol. B). **[read, local file]**
   - Heraclitus (*Homeric Problems*) and the speaker Lucius in Plutarch, *De facie* 19, read it as an eclipse. Both pair it with the "waning/waxing month" line, 14.162 = 19.307. That is the same pairing B&M make. **[read, library]**
   - Aristarchus suspected the lines 14.162-164, one of the two new-moon passages (Aristonicus, schol. H). **[read, library]**
6. **Several alternative "Odyssey eclipse" dates have been proposed** (§6):
   - 12 January 1183 BC, an annular eclipse considered and rejected by Schoch;
   - 30 October 1207 BC, annular (Papamarinopoulos et al. 2012), which at Ithaki is a 0.82 partial **[computed]**;
   - 689 BC (Pocock 1965) **[secondary]**;
   - an undated 1612 attempt by Herwart von Hohenburg **[secondary]**.
7. **The same few eclipses get attached to several texts.**
   - 30 October 1207 BC: claimed for the Odyssey (Papamarinopoulos 2012) and for Joshua 10:12 (Humphreys & Waddington 2017; Vainstub et al. 2020).
   - 30 September 1131 BC: claimed for Joshua (Khalisi 2021), and total at Ithaca on the canon (finding 2).
   - A null model that lets different texts compete for the same eclipse is therefore relevant to the bench. **[inference]**

---

## 1. The claim as published

### 1.1 Schoch 1926, "The Eclipse of Odysseus", *The Observatory* 49 (No. 620), 19-21 [read: ADS scan, `data/refs/schoch-1926-observatory.pdf`]

- **Method.**
  - Schoch used Oppolzer's *Syzygientafeln*, corrected with his own secular-acceleration terms: +12.24″s² in the Moon's mean longitude, from the Almagest occultations, and +2.64″s² in the Sun's (p. 20).
  - He scanned -1240 to -1140.
  - He found that "the total solar eclipse of -1177, April 16 … can alone be taken into consideration" (p. 20).
- **The time of day comes from a reconstruction of the narrative.** Schoch built an hour-by-hour timetable of Book 20 and set Theoclymenus' warning at **11:41 local mean time** (p. 20).
- **Where totality fell.** "My elements of the Sun make the southern limit of totality pass through the island of Ithaca" (p. 21). On his own numbers, Ithaca sat on the edge of the path.
- **The rejected alternative.** The only other large eclipse at Ithaca in his century was the annular eclipse of -1182 January 12 (1183 BC). It reached only 11.4 digits and peaked 14 minutes after sunrise, so he rejected it (p. 21).
- **His chronology.** Fall of Troy -1187; landing on Ithaca -1177 April 12; slaughter of the suitors -1177 April 16 (p. 21).
- **His new-moon evidence.** Od. 14.161-162 and 19.306-307 (p. 21).
- **Related items I have not read.** Schoch 1926b, *Die Sterne* 6: 88; Schoch 1926c, *Die sechs griechischen Dichter-Finsternisse* [secondary: Gainsford 2012 n.4; B&M refs 12-13]. P. V. (Paul Victor) Neugebauer, *Astronomische Chronologie* (1929) [secondary: B&M ref 14]. He is not Otto Neugebauer; B&M's ref 42 is Otto.

### 1.2 Fotheringham 1921, *Historical Eclipses* (Halley Lecture), pp. 16-18 [read: Internet Archive OCR, `data/refs/fotheringham-1921.txt`]

- Fotheringham argued, before Schoch, that "the Sun has perished out of heaven" ought to mean a total eclipse.
- His supports:
  - the new-moon lines 14.158-164 = 19.303-307;
  - the moonless night of 14.457;
  - the feast day of 20.156 and 20.276;
  - Plutarch, *De facie* 931F, and Eustathius.
- He reports Monro's objection that no actual darkness is mentioned that day, and that the darkness is the darkness of death.
- He reports that **Herwart von Hohenburg in 1612** "went so far as to date the return of Odysseus and the Trojan war by means of the eclipse". This is the earliest modern dating attempt I found. I could not establish Herwart's date.
- He refused to date the Trojan War by the eclipse. Schoch quotes this caution (Schoch p. 20).

### 1.3 Baikouzis & Magnasco 2008, PNAS 105(26): 8823-8828, doi:10.1073/pnas.0803317105 [read: full text, `data/refs/bm2008.txt`; Supporting Information NOT read, see §8]

**Design.**
- B&M do *not* assume an eclipse.
- They take every new moon in 1250-1115 BC: 1,684 of them (p. 8825).
- Each new moon is a candidate Day 0, and they test four clues against it:
  1. Day -29, Od. 5.272-277: the Pleiades and "late-setting" Boötes are visible together at nautical twilight. This confines the 17 sailing days to 17 February-4 April.
  2. Day -5, Od. 13.93-95: Venus rises at least 90 minutes before the Sun. They say this happens about one-third of the time.
  3. Day 0: new moon, from 14.161-162 = 19.306-307, 14.457, and 20.156 and 20.276.
  4. Day -34, Od. 5.43-148: Mercury is "within a few days" of its westernmost rise-time azimuth. This is the "conjectural" reading of Hermes' trip to Ogygia.
- An optional fifth clue: the equinox falls just before Day -11, from Poseidon's return in Od. 5.282 (pp. 8825-8826).
- They report results under both a "consecutive" and a "parallel" day-numbering (Table 1).

**Software and ΔT.**
- Starry Night Pro 6.0.4, which uses VSOP87 for the planets and ELP-2000/82 for the Moon.
- ΔT "according to Meeus following Stephenson and Morrison (1984) with additional adjustments; ΔT for our eclipse is 27,602.7 sec".
- EmapWin for eclipse tracks.
- Planetary, Lunar and Stellar Visibility 3.0, with minimum altitudes of 1° for Mercury and 2° for the Pleiades (p. 8825).

**Result.**
- A single date satisfies all criteria: 16 April 1178 BC (-1177). Day -34 falls on 13 March; Day -29 on 18 March; the equinox on 1 April; Day -5 on 11 April, when Venus rises 1 h 43 min before dawn (p. 8826).

**Their own caveats** (pp. 8824, 8828):
- If the passages are misread, "our whole calculation would be a nonsequitur".
- Hermes = Mercury predates the first attested association (Plato) by about two centuries.
- The coherence is noted "(post hoc)".
- The ΔT error in the path is "≈2-3°, approximately the width of the track itself" (SI Fig. S1, which I have not read).

**Their rarity claim** (p. 8826): the references "can be matched exactly only one day every 2,000 years". This comes from:
- one eligible new moon every 6 years, a figure that already includes the equinox clue;
- × 1/3 for Venus;
- × 1/116 for Mercury's turning point.

**Figure 1.** "31st eclipse in Saros Series 39 … at 12:02 p.m. local time". Greatest eclipse at 32.7 N, 12.7 E, "50 km WSW of Tripoli" (p. 8828).

**Smaller claims.**
- Total solar eclipses recur about once in 370 years at a given place (p. 8823).
- One exeligmos later, on 18 May 1124 BC, the path passed about 90 km ENE of Babylon (p. 8828).

---

## 2. The NASA Five Millennium Canon entry, and what it implies for Ithaca

### 2.1 Canon entry for -1177 April 16 [read: NASA pages fetched 2026-10-03, saved in `data/refs/nasa/`]

Sources: `SEcat5/SE-1199--1100.html`, `SEsearch/SEdata.php?Ecl=-11770416` (Besselian elements) and `SEsaros/SEsaros039.html`, all on eclipse.gsfc.nasa.gov (Espenak & Meeus 2006, NASA/TP-2006-214141).

| Field | Value |
|---|---|
| Catalogue number | **01966** |
| Calendar date | -1177 Apr 16 = 16 April 1178 BC, Julian. This is 5 April -1177 proleptic Gregorian **[computed]** |
| Greatest eclipse | **17:57:28 TT (TD)** = 10:00:58 UT; JD(TT) 1291264.24800 |
| ΔT used | **28,590.0 s** |
| Lunation number | -39291 |
| Saros | **39**, member 31 of the series (sequence -37 to …; "Rel. -07") **[computed from the Saros 39 table]** |
| Type | **T** (total); QLE flag "p-" |
| Gamma | **0.5187** |
| Magnitude | **1.0599** |
| Greatest eclipse at | **32.7° N, 12.7° E**, in the Mediterranean off Tripolitania; Sun altitude 58.6°, azimuth 145.5° |
| Path width | **227.8 km** |
| Central duration | **4 m 33 s** |
| Ephemerides | VSOP87 / ELP2000-82; lunar ṅ = -25.858″/cy² (`SEcat5/secular.html`) |
| Besselian elements | t0 = 18.000 TT; x0 = -0.2285050, y0 = 0.4663150, d0 = 5.7173300°, μ0 = 90.087601°, l1 = 0.5345530, l2 = -0.0115270, tan f1 = 0.0046077, tan f2 = 0.0045847 |

NASA's "Solar Eclipses of Historical Interest" page lists this eclipse as the "Odyssey Eclipse" without caveat (`data/refs/nasa/SEhistory.html`). Gainsford 2012 (p. 5) criticises it for that.

**How the canon's ΔT is built** [read: `SEcat5/deltatpoly.html`, `secular.html`]:
- Before -500 the canon uses ΔT = -20 + 32u², with u = (y - 1820)/100. At y = -1176.7 that gives 28,717 s.
- It then adds c = -0.000012932 (y - 1955)² = -127 s, to convert from Morrison & Stephenson's ṅ = -26″/cy² to the ephemeris's -25.858.
- The result is 28,590 s **[computed; matches the catalogue]**.

**ΔT uncertainty.**
- The canon quotes Huber's (2000) Brownian model: σ = 365.25 N √[(NQ/3)(1 + N/M)]/1000 s, with N = |y + 500|, Q = 0.058 ms²/yr, M = 2500 (`SEcat5/uncertainty.html`) [read]. At -1177 this gives **σ ≈ 1,008 s ≈ 4.2° of longitude** **[computed]**. The page's own table lists 622 s at -1000 and 1,900 s at -1500.
- The alternative is HMNAO, i.e. Stephenson, Morrison & Hohenkerk 2016 and Morrison et al. 2021. Their long-term extrapolation, the integrated LOD function with ṅ = -25.82, gives 28,544 s at -1176.7. Converted to the canon's ṅ that is **28,578 s**: the two models agree to 12 s. The HMNAO tabulated error for -1600 to -901 is **720 s ≈ 3.0°** [secondary: the ytliu0/DeltaT code, which reproduces astro.ukho.gov.uk/nao/lvm tables; computed].
- Both models are extrapolations. SMH2016's data begin at -720 BC (720 BC). NASA's page says that before 1000 BCE ΔT "must rely on a certain amount of modeling".

### 2.2 How the computation was done, and how it was checked [computed]

- I downloaded the canon's Besselian elements for -1399 to -1000 as NASA's JavaScript Solar Eclipse Explorer files `JSEX/SEm1399.js` … `SEm1099.js` (974 eclipses).
- I ported the Explorer's local-circumstance code (`JSEX/program.js`, O'Byrne & Espenak) to Python: `eclipse_local.py`.
- I ran NASA's original JavaScript headless (`jsex_harness.js`). For every eclipse of -1199 to -1100 seen from Ithaki, my port reproduces the original's magnitude and obscuration to 3 decimals.
- ΔT enters the geometry only through the hour angle, h = μ - λ_W - 1.002738·ΔT·2π/86400. So I propagated ΔT uncertainty by sliding ΔT and recomputing (`ionian_eclipses.py`).
- **Cross-check against a published third party.** For 30 October 1207 BC at the Ionian islands, and for 6 June 1218 BC at Troy, my obscurations are 0.747 and 0.752. Papamarinopoulos et al. (2012; 2014) quote 75% and 75.2% [read: Papamarinopoulos 2014 p. 93-94]. For 17 November 1301 BC at Ithaki I get 0.461; they say 46%.

### 2.3 Local circumstances of the 16 April 1178 BC eclipse in western Greece [computed, canon elements]

At the canon's ΔT of 28,590 s:

| Site (lat N, lon E) | Type | Magnitude | Max (UT) | ΔT window for totality (s) | P(total), canon prior (σ 1,008 s) | P(total), HMNAO prior (28,578 ± 720 s) |
|---|---|---|---|---|---|---|
| Corfu town (39.62, 19.92) | **T** | 1.060 | 10:25 | 28,284-29,080 | 0.31 | n/c |
| Paxoi (39.20, 20.18) | **T** | 1.060 | 10:24 | 28,460-29,250 | 0.29 | n/c |
| Lefkada / Nidri (38.71, 20.71), Dörpfeld's Ithaca | P | 0.991 | 10:22 | 28,714-29,500 | 0.27 | 0.33 |
| **Ithaki / Vathy (38.367, 20.717)** | **P** | **0.984** (obscuration 0.988) | **10:22 UT = 11:45 LMT = 11:44 LAT; 18:18 TT**; Sun altitude 57°, azimuth 173° | **28,802-29,584** | **0.25** | **0.30** |
| Kefalonia / Argostoli (38.18, 20.49) | P | 0.984 | 10:21 | 28,796-29,574 | 0.25 | 0.30 |
| Paliki / Lixouri (38.20, 20.44), Bittlestone's Ithaca | P | 0.986 | 10:22 | 28,778-29,556 | 0.26 | 0.30 |
| Zakynthos (37.78, 20.90) | P | 0.969 | 10:21 | 28,996-29,768 | 0.22 | n/c |
| Pylos (36.91, 21.70) | P | 0.937 | 10:21 | 29,400-30,166 | 0.15 | n/c |
| Athens (37.97, 23.73) | P | 0.921 | 10:26 | 29,624-30,400 | 0.12 | n/c |

(n/c = not computed.)

At Vathy the partial phase runs 09:06-11:41 UT (JS Explorer output). At canon ΔT the central line crosses Ithaki's meridian at 40.54° N. Totality on that meridian spans 39.19-42.20° N, so Vathy lies about 91 km south of the southern limit.

**Which island is Ithaca barely matters here.** The four candidate "Ithacas" differ by at most about 90 s in their totality windows, far less than σ(ΔT). None of the published critiques turns on the identification. B&M thank Bittlestone and Diggle and cite *Odysseus Unbound* only for Poseidon's epithets. **[read B&M p. 8826; inference]**

**B&M's ΔT of 27,602.7 s.** Put into the canon geometry, it moves the path *west*. The central line would then cross 20.7° E at 43.9° N, and Ithaki would see only 0.909 at 10:44 UT (12:07 LMT) **[computed]**.

So B&M's ΔT gives a total eclipse at Ithaca only if Starry Night's lunar ephemeris carried a different ṅ. Here is the arithmetic. ELP-2000/82's native ṅ is -23.8946″/cy² (my assumption; I have not checked it in Starry Night). With it, 27,602.7 s corresponds to about 29,356 s in the canon frame, using ΔT_new = ΔT_old - 0.91072 Δṅ T². That value lies inside the totality window. The stated ΔT therefore cannot be interpreted without knowing Starry Night's ṅ. **[inference; open question]**

B&M's "12:02 p.m. local time" is close to the LMT of maximum I get with their ΔT (12:07). The canon gives 11:45 LMT.

### 2.4 Is 1178 BC "the only eclipse of the century" at Ithaca? [computed]

Among all canon eclipses at Ithaki between 1300 and 1050 BC, only these have a non-negligible chance of totality under the canon's ΔT uncertainty. The 1340 BC eclipse, which falls just outside that range, is added for comparison.

The P columns integrate a normal ΔT prior over the totality window. §7 uses a ±2σ grid instead, which gives values up to 0.02 different. Times of central eclipses are taken from NASA's own JavaScript output (mid-eclipse, i.e. closest approach of the shadow axis).

| Date (UT, Julian) | Canon type at Ithaki | ΔT window for totality (s) | Canon ΔT | P(total), canon σ | P(total), HMNAO |
|---|---|---|---|---|---|
| 8 Jan 1340 BC (-1339); outside the range, for comparison | **T** 1.039, but only 57 s of totality at Vathy; 08:36 UT = 09:59 LMT, Sun 21° | 27,883-31,837 | 31,773 | 0.52 | 0.65 |
| 24 Jun 1312 BC (-1311) | P 0.984, 12:01 LMT | 31,743-32,653 | 31,203 | 0.20 | 0.15 |
| 10 Feb 1286 BC (-1285) | P 0.870 | 32,987-33,693 | 30,693 | 0.03 | <0.001 |
| **16 Apr 1178 BC (-1177)** | P 0.984, 11:45 LMT | 28,802-29,584 | 28,590 | **0.25** | **0.30** |
| **30 Sep 1131 BC (-1130)** | **T 1.049, 3 m 39 s, 09:49 UT = 11:12 LMT, Sun 52°** | 27,053-28,035 | 27,691 | **0.41** | **0.49** |

Notes on this table:
- The expected number of total eclipses at Ithaki over all 624 canon eclipses of 1300-1050 BC is about 0.7. That is one per ~360 years, consistent with B&M's "once in 370 years".
- 30 September 1131 BC lies inside B&M's 1250-1115 BC search window. It is excluded only by their season constraints. Schoch's 1926 window (-1240 to -1140) excluded it outright. Its local time of maximum also falls inside Schoch's "10 a.m. to noon" requirement.
- Gainsford (2012, p. 13 n.32), citing the canon maps, already noted four eclipses "almost directly over Ithaca" in 1350-1250 BC. I find them as follows:
  - 8 Jan 1340: total at Ithaki at canon ΔT;
  - 24 Jun 1312: P 0.984;
  - 14 Apr 1281: annular at Ithaki, 0.935, 05:17 UT = 06:40 LMT;
  - 27 Sep 1261: P 0.882.
- He also gives the ΔT longitude uncertainty for that period as 5.1-6°, which agrees with the Huber σ of 1,213-1,426 s I compute for those dates.

---

## 3. Philological critiques

### 3.1 The ancient readings

**Odyssey scholia** (Dindorf 1855; `data/text/scholia-odyssey-grc.tsv`, keys `2.20.2.86`-`2.20.2.92`) [read]:
- **On 20.356-357 (schol. B):** "οὐ γὰρ ἡλίου ἔκλειψις ἐγένετο", "for no eclipse of the Sun occurred". The scholion goes on: Theoclymenus, prophesying in some inspired state, sees that the Sun will fail *for them*. The suitors see nothing of the kind and want him thrown out as raving.
- **On 20.356-357 (schol. V):** not as though an eclipse had happened, but that for the suitors the Sun had failed. Theoclymenus' exit is "economic", i.e. a device of plot.
- **On 20.355, εἰδώλων (schol. B):** the ghosts are the suitors' souls going to Hades.
- **On 20.362 (schol. B):** take him to the agora "so that he may see the light", since he likens what is in the house to night. This is the line Dörpfeld and Gainsford use: it is daylight outside.
- **On 20.343 (schol. B):** the bloody meat was seen by Theoclymenus, not by the suitors.
- **On 20.155-156 (schol. V, citing Philochorus):** the feast is the νεομηνία, the new moon, sacred to all gods and to Apollo Neomenios. A second V-scholion: the new-moon feast of Apollo keeps the townsmen busy, giving a good moment for the attack. On 20.276 (schol. B), the poet "wants to show the feast is Apollo's".
- **On 14.162, τοῦ μὲν φθίνοντος (Q, V, Vind. 133):** "to the thirtieth and new moon", ἔνη καὶ νέα.
- **On 14.457, σκοτομήνιος (V):** moonless, *or* the night when the Moon is darkened by conjunction with the Sun.
- **On 5.272, ὀψὲ δύοντα Βοώτην:** "setting long after those that rose with it", explained from Aratus: Boötes sets together with four zodiacal signs. An alternative scholion (B.V): "then [i.e. in the evening] the oxen are released". So the ancient gloss is *slow-setting*, a fixed property of the constellation, not a seasonal clue. Aratus, *Phaen.* 581-585, says the same [read: library EditionId 1559]. **[inference]** This supports Gainsford's and Hainsworth's "general, not seasonal" reading.

**Aristarchus via Aristonicus** (*De signis Odysseae*, library EditionId 3257, node 14.162_164) [read]:
- Lines 14.162-164 are "suspected as inconsistent with what precedes, and as suspect and unconvincing" (schol. H). One of the two new-moon passages was thus under Alexandrian obelus.
- No athetesis of 19.306-307 or 20.351-357 is recorded in this edition.

**Heraclitus, *Homeric Problems*** (library EditionId 3322, exported to `data/text/heraclitus-allegoriae-grc.tsv`) [read]:
- In this (1st1K) edition the passage is **ch. 73.1-73.2**, and a lacuna (marked "……") precedes it. B&M (ref 9) and Gainsford (n.3, n.7, n.27) cite it as **ch. 75**, sections 2-8 in the modern numbering.
- Heraclitus reads 20.351-357 as an allegory of a solar eclipse:
  - the Sun's disc is dimmed and stars shine through;
  - Theoclymenus "who hears the divine" is aptly named;
  - in eclipses the light turns blood-red, which explains the "walls spattered with blood".
- He then fixes the day. The eclipse's appointed time, "which Hipparchus determined precisely", is the "thirtieth and new moon" day, called ἕνη τε καὶ νέα in Attic, and Homer gives it with τοῦ μὲν φθίνοντος μηνός, τοῦ δ' ἱσταμένοιο (14.162 = 19.307).
- This is the B&M pairing, made in the 1st century AD.

**Plutarch, *De facie* 19 (931D-F)** (library EditionIds 371 Greek and 369 Cherniss, Loeb; exported) [read]:
- The speaker Lucius argues that a solar eclipse resembles sunset, citing a recent eclipse that began just after noon and showed many stars.
- He lists poets who lament eclipses: Mimnermus, Cydias, Archilochus, Stesichorus, Pindar.
- "To crown all" he cites Homer: faces held in night and gloom, the Sun perished from heaven "with reference to the Moon" (περὶ τὴν σελήνην), and this "naturally occurs" τοῦ μὲν φθίνοντος μηνὸς τοῦ δ' ἱσταμένοιο.
- Gainsford (n.3) calls Plutarch's position equivocal.

**Other ancient readings** [secondary: Gainsford 2012 n.3, n.5]:
- [Plut.] *Vit. Hom.* 2.108 and Eustathius on Od. 14.161, 14.457, 19.307 and 20.357 accept an eclipse; Eustathius takes it allegorically.
- Schol. Arat. *Phaen.* 864 quotes Od. 19.307 in connection with solar eclipses.
- [Plut.] *Vit. Hom.* 2.108 and Eustathius on Il. 16.567 also see an *Iliad* eclipse there.
- Gainsford's tally: Heraclitus, ps.-Plutarch and Eustathius accept; Plutarch equivocates; both Odyssey scholia reject.

**P.Oxy. LIII 3710** (ed. Haslam 1986), a 2nd-century AD commentary on Od. 20 [secondary: sententiaeantiquae.com 2017 post; Lebedev 1990, *Apeiron* 23: 77ff., doi:10.1515/apeiron.1990.23.2.77, abstract only]:
- It comments on 20.356.
- It ties the new moon to Apollo "since he is the Sun".
- It quotes Aristarchus of Samos, who cites Thales (and Heraclitus of Ephesus), for eclipses happening at the new moon.
- Gainsford did not use it in 2012 (per the same blog).

### 3.2 Modern philology before 2008 [mostly secondary: Gainsford 2012 pp. 2-4, n.6, n.11-12]

- **Dörpfeld 1926**, *Die Sterne* 6: 186-187, rebutted Schoch from context:
  - Theoclymenus describes souls going to Erebus, where the Sun notoriously does not shine;
  - 20.362 shows no unusual darkness;
  - the suitors do not believe him;
  - no narrator or character mentions an eclipse.
  I have not read Dörpfeld.
- **Approving or allowing:**
  - Fotheringham 1921 [read];
  - Shewan 1928, *CW* 21: 196-198, approving Schoch;
  - Pocock 1965, *Odyssean Essays* 55-63, a historical eclipse but in 689 BC;
  - Willcock 1966 (CR review);
  - Austin 1975, *Archery at the Dark of the Moon* 239-253: a symbolic eclipse at the festival of Apollo Noumenios;
  - Levine 1983, "Theoklymenos and the Apocalypse", *CJ* 79: 1-7, figurative.
  - Gainsford notes that Shewan and Pocock confuse the year notation (-1177 vs 1178 BC).
- **Commentaries reading it as figurative death-imagery:** Monro 1901: 196; Ameis-Hentze-Cauer 1911: 68; Russo 1992: 124-125; Rutherford 1992: 234.
- **Suspected lines.** Page 1955 thought the Theoclymenus lines suspect, since that seems to be his only function [secondary: B&M p. 8823, ref 10].
- **Merry and van Leeuwen** [secondary: Fotheringham p. 18]: Merry allows an eclipse as the climax of the vision; van Leeuwen ignores the ancient interpretation.

### 3.3 Gainsford 2012: the only full rebuttal of B&M [read: TAPA 142: 1-22, doi:10.1353/apa.2012.0006; Zenodo record 343907; `data/refs/gainsford2012.txt`]

**Framing (pp. 4-5).**
- Dörpfeld's contextual objections do not touch B&M, because B&M make no assumption about 20.356. So "scholarly silence" is the wrong response.
- He notes that the AP, AFP, NASA's historical-eclipse page and Wikipedia had already adopted 1178 BC.

**Item by item (pp. 6-15).**
- **Reference 1, Hermes = Mercury.**
  - No Greek text, not even Aratus, uses a god's movement on earth to stand for a heavenly body's.
  - Taking Hermes but not the others is cherry-picking. If the method were sound, it would also have to accommodate:
    - Zeus/Jupiter, motionless on Olympus;
    - Ares-Aphrodite (Od. 8) as a conjunction;
    - Helios-Zeus (Od. 12.374-390), including Helios' threat to shine among the dead (12.382-383);
    - Poseidon-Zeus (13.125-158);
    - the "night" of Il. 16.567.
  - This directly contradicts B&M's "we have not chosen the references to pursue".
- **Reference 2, Pleiades and "late-setting" Boötes.**
  - ὀψέ means late in an absolute sense, "late in the day / in the evening", not "later than"; compare Il. 21.232.
  - Other advocates put the voyage in autumn: Austin, 19 September-8 November; Pocock, late autumn to winter, from the ripe grapes at 5.68-69. MacDonald 1967, whom B&M follow, actually argued for late May; his reaping-match evidence is contradicted by the ploughing match at 18.371-375.
  - Hainsworth 1988: 277 calls it "general astronomical, not specifically navigational or seasonal, data".
  - Od. 5.271-276 is largely a verbatim repeat of Il. 18.486-489 (Achilles' shield), which presumes it is not geared to its context. **[computed]** Od. 5.273-275 = Il. 18.487-489 word for word. Od. 5.272 shares only Πληιάδας, and "late-setting Boötes" is *not* in the Iliad passage.
- **Reference 3, Poseidon's return as the equinox.** The Aithiopes are at both the sunrise and the sunset edges of the earth (Od. 1.22-24), and Poseidon returns from the east, via the Solymoi (5.283). So the "return from the southern hemisphere" reading is simply wrong.
- **Reference 4, Venus.** It is weak only through the season, and the 90-minute threshold is unexplained.
- **Reference 5, the new moon.** This is "the only wholly tenable reference".
  - Alternatives: Austin's festival of Apollo Noumenios; and new-moon debt collection, the "old and new" ἕνη καὶ νέα of Ar. *Clouds* 1131-1200, which Heraclitus also uses. These undermine the eclipse reading but not B&M's logic.
- **Archaeology and the window.** The window rests on late ancient Troy-dates and on Troy VIIa. Troy VIh and the Tawagalawa letter would allow a Trojan War in the 1290s or earlier, so the scan should be extended to 1350-1250 BC. See n.32 on eclipses over Ithaca then, and §2.4 above.
- **Numbers.** "Seventeen days … on the eighteenth" (5.278-279) recurs for Achilles' funeral (24.63-65) [verified locally]. "Nine … tenth" and "six … seventh" are typical numbers. Hawke 2008 shows Homeric number-frequencies are unlike those of natural language.
- **Chronology.** B&M's hybrid of Zieliński's law and Delebecque's "law of succession" occupies the "hard" extreme. It still leaves:
  - the doubled council of the gods;
  - Athena's past-tense reference (5.18-20) to a Telemachy that, on B&M's own chronology, lies three weeks in the future.
- **Conclusion.** An argument from coherence is epistemologically weak, and here the coherence is "illusory". It is "not a plausible conjecture either".
- **Slip in the source.** Gainsford's summary and first paragraph give "26 April 1178 B.C.E.". The Julian date is 16 April, and the proleptic Gregorian date is 5 April **[computed]**. 26 April matches neither, so it is evidently a slip.

**Gainsford 2018 blog** ("The citation problem", Kiwi Hellenist, Sept 2018) [secondary: WebFetch summary]. It criticises B&M's and Papamarinopoulos et al.'s engagement with Homeric scholarship: B&M cite only three Homeric works, Page, Murray and Bittlestone.

### 3.4 Press-quoted expert reactions, 2008 [read: Castelvecchi, *Science News*, 26 June 2008, via WebFetch]

- **James Evans** (University of Puget Sound): the thesis "would require a major revision of the history of ancient astronomy". Because it rests on Hermes = Mercury, it is a "castle of cards".
- **Robert H. van Gent** (Utrecht): the "biggest problem is how to explain the apparent coherence".

*Scientific American* (Minkel, 23 June 2008) quotes no outside critic [read via WebFetch].

---

## 4. Statistical critiques

**Published.** I found no formal statistical critique of B&M (null distribution, Monte Carlo, look-elsewhere correction or sensitivity analysis). I checked:
- Semantic Scholar's list of papers citing the PNAS paper (2008-2026, 26 entries);
- the papers citing Gainsford (3 entries);
- web searches.

The statistical objections in print are verbal ones:
- Gainsford's cherry-picking of deities and "illusory coherence" (§3.3);
- van Gent on coherence (§3.4);
- Evans on a chain of dependent conjectures (§3.4).

**Where the look-elsewhere enters: the degrees of freedom the bench should vary** [inference, from B&M's text]:

1. **Window.** The window is 1250-1115 BC (135 years), built from classical Troy dates "extended by 10 years" (p. 8825). Those dates are the same tradition that led Schoch to 1178 BC, and the authors knew the target date before they fixed the window. Gainsford wants 1350-1250 added.
2. **Day-numbering.** There are two chronologies, consecutive and parallel, and B&M report success under both. The Delebecque-based table itself involves choices (Gainsford §"General issues 3").
3. **Thresholds.**
   - Venus must rise at least 90 minutes before the Sun (why 90?).
   - Visibility altitudes are 1° for Mercury and 2° for the Pleiades, with standard extinction.
   - Mercury must be "within a few days" of its westernmost rise azimuth. That definition was picked from three candidate "turning points": westernmost azimuth, greatest elongation, station.
4. **Graded matching.** Table 2 colours near-misses (orange or yellow). "Two days in which the criteria are narrowly missed" are discussed only in the SI.
5. **The rarity figure includes a clue they said they did not use.** "One day every 2,000 years" is built from "one T every 6 years", which already applies the equinox criterion they called "far more conjectural" and used "merely … for additional confirmation". It also assumes an exact-day Mercury match. On B&M's own frequencies **[computed]**:
   - with the equinox and a ±2 to ±3-day Mercury tolerance: one match per ~300-420 years, i.e. ~0.3-0.45 expected chance matches in their 135-year window;
   - without the equinox ("one or at most two moons T each year"): one match per ~35-70 years, i.e. ~2-4 expected.
   B&M found one full match plus two near misses.
6. **Post-hoc supporting coincidences.** "Ares does not appear… Mars was not visible… except at the eclipse"; noon timing; early spring (p. 8826). These were added after the match was found.
7. **Clue selection.** "The ones we have examined are all we have found" (p. 8826). Gainsford lists several other candidate "astronomical" god-movements that were not used.
8. **The eclipse term itself.** At canon ΔT the match is a 0.984 partial at Ithaki, with P(total) about 0.25-0.30, and there is a total eclipse at Ithaki inside the window (1131 BC; §2.4). How large a "hit" an eclipse counts as depends on ΔT and on which island is Ithaca.
9. **Cross-text competition.** The same eclipses are claimed for different texts:
   - 30 October 1207 BC: Odyssey (Papamarinopoulos 2012) and Joshua 10 (Humphreys & Waddington 2017; Vainstub et al. 2020);
   - 30 September 1131 BC: Joshua (Khalisi 2021).
   A null in which random or unrelated texts are scored with the same protocol would measure how often such "matches" arise.

---

## 5. Later work applying the same kind of method to other texts (2008 onward)

| Work | Text | Claimed date(s) | What I read |
|---|---|---|---|
| Papamarinopoulos, Preka-Papadema, Antonopoulos, Mitropetrou, Tsironi, Mitropetros 2012, *Mediterranean Archaeology & Archaeometry* (MAA) 12(1): 117-128, "A new astronomical dating of Odysseus' return to Ithaca" | Odyssey: an eclipse plus Venus plus Pleiades/Boötes, *autumn* season | Return 25 Oct 1207 BC; slaughter at the **annular eclipse of 30 Oct 1207 BC** (-1206), 75% obscuration in the Ionian islands, max ~16:00 local | Secondary: q-mag.org summary and the authors' own recap in Papamarinopoulos et al. 2014 [read] |
| Papamarinopoulos, Preka-Papadema, Mitropetros 2013, MAA, "The anatomy of a complex astronomical phenomenon described in the Odyssey" | Odyssey (Theoclymenus' second prophecy; a "meteor shower" of dove's feathers) | Late Oct 1207 BC | Title and abstract snippet only |
| Papamarinopoulos et al. 2014, MAA 14(1): 93-102, "A new astronomical dating of the Trojan War's end" (Zenodo 10.5281/zenodo.14315) | Iliad 16-18 (Sarpedon and Patroclus' deaths; Venus three days later) | **Annular eclipse 6 Jun 1218 BC** (-1217), 75.2% at Troy, max 15:45 LT; "pair" with 1207 BC | Read in full (`data/refs/pap2014.txt`). They use Starry Night 6 Pro and the NASA canon / Jubier, scanning 1400-1130 BC |
| Henriksson 2012, MAA 12(1): 63-76, "The Trojan War dated by two solar eclipses" | Iliad 17.366-377, plus a Hittite eclipse | **Total eclipse 11 Jun 1312 BC (Gregorian) = 24 Jun 1312 BC Julian** (-1311), and an eclipse in 1335 BC (Mursili II) | Secondary: Papamarinopoulos 2014 pp. 93-94; Brianas (n.d.) |
| Papamarinopoulos, Preka-Papadema, Gazeas 2016, "Extreme physical phenomena during the Trojan War" | Iliad | n/k | Title only (Semantic Scholar) |
| Guglielmino, Cipolla, Rizzo Giudice 2017, "Astronomy in the Odyssey: the status quaestionis", in *The Light, the Stones and the Sacred* (Astrophys. Space Sci. Proc. 48): 165-180, doi:10.1007/978-3-319-54487-8_10 | Review | Discusses the 1207 BC proposals | Abstract snippet only |
| Humphreys & Waddington 2017, *Astronomy & Geophysics* 58(5): 5.39-5.42, doi:10.1093/astrogeo/atx178 | Joshua 10:12-13 | **Annular eclipse 30 Oct 1207 BC**, used to date Merneptah and Ramesses II | Secondary (news and search summaries). A&G 59(4) 4.10 (2018) carries a follow-up exchange I have not read |
| Vainstub, Yizhaq, Avner 2020, *Vetus Testamentum*, doi:10.1163/15685330-12341412 | Joshua 10 and Habakkuk 3 | **30 Oct 1207 BC** (annular) | Abstract (Semantic Scholar) |
| Khalisi 2021, arXiv:2102.09402, "Joshua's total solar eclipse at Gibeon" | Joshua 10:12 | **Total eclipse 30 Sep 1131 BC** (-1130); claims to halve the ΔT error | Abstract (arXiv) |
| Glover 2014, *Classical Quarterly* 64(2): 471-492, "The eclipse of Xerxes in Herodotus 7.37" | Herodotus | Cites B&M; a philological treatment of a "non-fitting" eclipse | Title only. A natural negative control |
| Simon 2024, *International Journal of Cartography*, doi:10.1080/23729333.2024.2392970 | Eclipse maps and ΔT; Near-Eastern eclipse traditions | Proposes "Long Chronology" eclipses as ΔT anchors; cites B&M and Gainsford | Abstract only |
| Theodossiou, Manimanis, Mantarakis, Dimitrijević 2011, *J. Astron. Hist. Heritage* 14(1): 22-30 | Homeric astronomy survey | n/k | Not read (ADS PDF timed out) |
| Brianas (n.d., c. 2024-25), "Reanalyzing and reconciling issues of the authenticity and dating of the Trojan War" (Achilles Foundation web PDF) | Adopts Papamarinopoulos' 1218/1207 BC pair | — | Read (`data/refs/coa.txt`); not peer-reviewed |
| Marchant 2026, *Nature* d41586-026-02275-0, "What *The Odyssey* reveals about ancient science" | Feature | n/k | Title only (paywall) |
| Kubarev 2020; Volkov 2016/2024; Vella 2016 ("Homer's Ogygia") | Bible; Iliad; Odyssey | n/k | Titles only (Semantic Scholar citation list) |

**Positive-control candidates** (NASA "Solar Eclipses of Historical Interest", `data/refs/nasa/SEhistory.html` [read]):
- 15 Jun 763 BC (-762), Assyrian eponym;
- 6 Apr 648 BC (-647), Archilochus;
- 28 May 585 BC (-584), Thales;
- 19 May 557 BC (-556), Larisa;
- 2 Oct 480 BC (-479), Xerxes, Herodotus 9.10;
- 3 Aug 431 BC (-430), Thucydides 2.28;
- 21 Mar 424 BC (-423), Thucydides 4.52;
- also listed: 3 May 1375 BC (-1374, Ugarit) and 5 Jun 1302 BC (-1301, Shang).

**Independence of the "known" dates varies.** Some are fixed partly *by* the eclipse: Thales, Archilochus, and the Assyrian eclipse within the eponym list. Thucydides' are fixed independently by his war-year count. **[inference]**

---

## 6. Alternative dates proposed for an "Odyssey eclipse"

Local values at Ithaki use the canon ΔT **[computed]**.

| Proposer | Date (Julian; BC / astronomical) | Type (canon) | At Ithaki, canon ΔT | Source status |
|---|---|---|---|---|
| Herwart von Hohenburg 1612 (*Novae… chronologiae*) | not established | — | — | Secondary: Fotheringham 1921 p. 18 |
| Schoch 1926; P. V. Neugebauer 1929; endorsed by Shewan 1928; B&M 2008 | **16 Apr 1178 BC / -1177** | T, Saros 39 | P 0.984 at 11:45 LMT; P(total) 0.25-0.30 | Read (Schoch, B&M) |
| Schoch 1926 (considered, rejected) | 12 Jan 1183 BC / -1182 | A (canon gamma 0.6863, magnitude 0.9908) | P 0.968 at 07:55 LMT, Sun 4° | Read |
| Pocock 1965 | "689 BC". The only large eclipse that year in the Ionian islands is the annular one of **11 Jan 689 BC / -688** (A 0.927 at Ithaki) **[inference + computed]** | A | A 0.927 | Secondary: Gainsford n.6 |
| Austin 1975 | none (symbolic eclipse at the new-moon festival) | — | — | Secondary: Gainsford |
| Papamarinopoulos et al. 2012 | **30 Oct 1207 BC / -1206** | A | P 0.818, obscuration 0.747, 15:26 LMT, Sun 20° | Secondary + 2014 recap |
| Implied under Henriksson's 1312 BC Troy (raised and rejected by Papamarinopoulos 2014) | 17 Nov 1301 BC / -1300 | — | P 0.570, obscuration 0.461, 08:10 LMT | Read (Pap. 2014); computed |
| *Not proposed by anyone; found here* | **30 Sep 1131 BC / -1130** | T | **T 1.049, 3 m 39 s, 11:12 LMT** | Computed |

---

## 7. All solar eclipses of magnitude > 0.8 at Ithaki, 1300-1050 BC (-1299 to -1049)

These are from the NASA 5MCSE elements at the canon ΔT, with the Sun above the horizon. "±2σ" slides ΔT by up to twice the Huber σ. P values are Gaussian weights over that grid **[computed: `table_ithaki.py`; full list in `ionian_eclipses.csv`]**.
- Dates are the **UT** calendar date of local maximum (Julian). For two eclipses this differs from the canon's TT date: 6 Aug -1220 (canon 7 Aug) and 27 May -1189 (canon 28 May).
- Types: P = partial, A = annular, T = total. LMT is at Vathy.
- Rows marked † exceed 0.8 only somewhere within ±2σ.
- Times for the annular and total rows are NASA JavaScript mid-eclipse times.

| UT date (Julian) | BC | Type | Magnitude | Obscuration | Max UT | Max LMT | Sun altitude | Magnitude range ±2σ | P(mag > 0.8) | P(total) |
|---|---|---|---|---|---|---|---|---|---|---|
| -1285 Feb 10 | 1286 | P | 0.870 | 0.846 | 11:13 | 12:36 | 34 | 0.70-1.05 | 0.82 | 0.02 |
| -1283 Jun 15 | 1284 | P | 0.885 | 0.872 | 09:20 | 10:43 | 69 | 0.84-0.97 | 1.00 | 0 |
| -1280 Apr 14 | 1281 | **A** | 0.935 | 0.875 | 05:17 | 06:40 | 11 | 0.93-0.94 | 1.00 | 0 |
| -1260 Sep 27 | 1261 | P | 0.882 | 0.830 | 13:22 | 14:45 | 37 | 0.79-0.95 | 0.98 | 0 |
| -1246 Dec 20 | 1247 | P | 0.875 | 0.827 | 08:55 | 10:17 | 24 | 0.83-0.95 | 1.00 | 0 |
| -1231 Mar 14 † | 1232 | P | 0.700 | 0.633 | 11:42 | 13:05 | 43 | 0.53-0.87 | 0.10 | 0 |
| -1222 Mar 05 | 1223 | P | 0.864 | 0.838 | 11:04 | 12:27 | 41 | 0.77-0.97 | 0.92 | 0 |
| -1220 Aug 06 | 1221 | P | 0.902 | 0.888 | 17:38 | 19:01 | 1 | 0.50-0.97 | 0.86 | 0 |
| -1207 May 16 | 1208 | P | 0.935 | 0.907 | 09:53 | 11:15 | 66 | 0.84-0.97 | 1.00 | 0 |
| -1206 Oct 30 | 1207 | P (annular elsewhere) | 0.818 | 0.747 | 14:03 | 15:26 | 20 | 0.82-0.83 | 1.00 | 0 |
| -1196 Oct 09 † | 1197 | P | 0.799 | 0.717 | 05:50 | 07:12 | 14 | 0.74-0.83 | 0.47 | 0 |
| -1191 Jan 21 | 1192 | P | 0.807 | 0.749 | 10:45 | 12:08 | 30 | 0.74-0.90 | 0.57 | 0 |
| -1189 May 27 † | 1190 | P (at sunset) | 0.327 | 0.211 | 17:32 | 18:55 | 0 | 0.00-0.81 | 0.00 | 0 |
| -1182 Jan 12 | 1183 | P | 0.968 | 0.950 | 06:32 | 07:55 | 4 | 0.77-0.98 | 0.99 | 0 |
| **-1177 Apr 16** | **1178** | **P** (T in Corfu) | **0.984** | **0.988** | **10:22** | **11:45** | **57** | **0.83-1.06** | **1.00** | **0.26** |
| -1153 Jun 18 | 1154 | P | 0.912 | 0.878 | 04:39 | 06:02 | 16 | 0.83-0.97 | 1.00 | 0 |
| -1152 Dec 01 | 1153 | **A** (at sunset) | 0.919 | 0.844 | 15:23 (sunset) | 16:46 | 0 | 0.49-0.92 | 0.74 | 0 |
| -1137 Feb 23 | 1138 | P | 0.838 | 0.792 | 10:45 | 12:08 | 38 | 0.73-0.96 | 0.74 | 0 |
| **-1130 Sep 30** | **1131** | **T** (3 m 39 s) | 1.049 | 1.000 | 09:49 | 11:12 | 52 | 0.93-1.05 | 1.00 | **0.43** |
| -1128 Feb 14 | 1129 | P | 0.846 | 0.805 | 07:31 | 08:54 | 17 | 0.83-0.87 | 1.00 | 0 |
| -1108 Jul 29 | 1109 | P | 0.835 | 0.778 | 04:25 | 05:48 | 11 | 0.77-0.90 | 0.89 | 0 |
| -1105 May 29 † | 1106 | P | 0.790 | 0.743 | 17:15 | 18:38 | 3 | 0.69-0.86 | 0.37 | 0 |
| -1102 Sep 21 | 1103 | P | 0.951 | 0.936 | 06:28 | 07:51 | 25 | 0.91-0.98 | 1.00 | 0 |
| -1090 Aug 09 | 1091 | P (A at Corfu and Lefkada) | 0.957 | 0.924 | 14:24 | 15:47 | 38 | 0.89-0.96 | 1.00 | 0 |
| -1089 Dec 25 | 1090 | P | 0.833 | 0.757 | 08:08 | 09:31 | 18 | 0.75-0.91 | 0.81 | 0 |
| -1077 May 20 † | 1078 | P | 0.766 | 0.699 | 06:48 | 08:10 | 38 | 0.70-0.84 | 0.15 | 0 |
| -1074 Mar 18 | 1075 | P | 0.892 | 0.869 | 07:00 | 08:23 | 22 | 0.87-0.91 | 1.00 | 0 |
| -1067 Oct 23 | 1068 | P | 0.838 | 0.803 | 11:48 | 13:11 | 40 | 0.74-0.92 | 0.81 | 0 |
| -1059 May 30 | 1060 | P | 0.836 | 0.782 | 16:08 | 17:31 | 16 | 0.79-0.89 | 0.94 | 0 |

- **Count.** Of 624 canon eclipses in 1300-1050 BC, 94 are visible at Ithaki at canon ΔT; 24 exceed 0.8 and 10 exceed 0.9.
- **Other sites.** A five-site comparison (Corfu, Nidri, Vathy, Lixouri, Zakynthos) is in `sites_check.md`. Corfu reaches totality only in 1178 BC and 1131 BC. Some eclipses exceed 0.8 at Corfu or Zakynthos but not at Vathy:
  - -1206 Oct 30: 0.827 at Zakynthos, 0.799 at Corfu;
  - -1196 Oct 09: 0.814 at Zakynthos;
  - -1105 May 29: 0.804 at Zakynthos.

**The Ugarit eclipse at sunrise.** The canon's Ugarit eclipse of 3 May 1375 BC (-1374) happens to reach 0.894 at Ithaki, but only at sunrise **[computed; outside the requested range, shown for interest]**.

---

## 8. Open questions and sources I could not read

- **B&M's Supporting Information** (Table S1, Table S2, Fig. S1 on the ΔT path spread, the SI Discussion of the two near-miss dates). PNAS returned 403. PMC serves a proof-of-work bot challenge, which I did not attempt to get past. Europe PMC says the article is not open access.
- **Starry Night's lunar ṅ and ΔT formula.** These are needed to interpret B&M's 27,602.7 s (§2.3).
- **Primary texts known only at second hand:**
  - Dörpfeld 1926;
  - Schoch 1926b and 1926c;
  - P. V. Neugebauer 1929;
  - Shewan 1928;
  - Pocock 1965 (the exact 689 BC date);
  - Austin 1975;
  - Levine 1983;
  - MacDonald 1967;
  - Russo 1992 and Hainsworth 1988 (Oxford commentary);
  - [Plut.] *Vit. Hom.* 2.108;
  - Eustathius;
  - schol. Arat. 864;
  - P.Oxy. 3710 (Haslam 1986) and Lebedev 1990.
- **Later work known only at second hand or by title:**
  - Papamarinopoulos et al. 2012 (MAA blocks automated access) and 2013;
  - Henriksson 2012;
  - Humphreys & Waddington 2017 and the 2018 A&G exchange;
  - Theodossiou et al. 2011;
  - Guglielmino et al. 2017;
  - Glover 2014;
  - Simon 2024;
  - Marchant 2026.
- **Herwart von Hohenburg's 1612 date** for the Odyssey eclipse.
- **Whether any author has rerun B&M's search** with the Supporting Information and an independent ephemeris. I found none.

## 9. Files produced or used

**References** (`C:\Projects\odybench\data\refs\`):
- `baikouzis-magnasco-2008.pdf` and `bm2008.txt`;
- `gainsford-2012-tapa.pdf` and `gainsford2012.txt`;
- `schoch-1926-observatory.pdf`;
- `fotheringham-1921.txt`;
- `papamarinopoulos-2014-trojanwar.pdf` and `pap2014.txt`;
- `councilofachilles-trojanwar-dating.pdf` and `coa.txt`;
- `nasa\` (catalogue pages, Besselian elements, Saros 39, the Huber ΔT page, the secular-acceleration page, the JSEX element files and program).

**Texts exported read-only from ClassicaCodex** (`C:\Projects\odybench\data\text\`):
- `heraclitus-allegoriae-grc.tsv` (EditionId 3322);
- `plutarch-defacie-grc.tsv` (371);
- `plutarch-defacie-cherniss.tsv` (369);
- `aristonicus-signis-odysseae-grc.tsv` (3257).

**Computation** (`C:\Projects\odybench\results\research-critiques\`):
- `eclipse_local.py`: a port of the NASA JS Eclipse Explorer;
- `jsex_harness.js`: runs the original NASA code headless, for validation;
- `ionian_eclipses.py` and `ionian_eclipses.csv`: 974 eclipses of -1399 to -1000 at Vathy, with ΔT sensitivity;
- `table_ithaki.py` and `table_ithaki.md`;
- `sites_check.py` and `sites_check.md`;
- `jsex_ithaki_-1399_-1000.txt`: NASA's own JS output at Vathy.
