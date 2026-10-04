# odybench research note: the search window

What date window did Baikouzis and Magnasco search, what evidence lies behind it, what are the alternatives, and what window should a fair bench use?

*Written 2026-10-03 for odybench. Status: research input for the reproduction and null-model stages. Nothing here is a verdict on the eclipse claim.*

## Conventions

- **Years.** Every date is given as historical BC with the astronomical year in brackets: 1178 BC = astronomical −1177. An Attic or Olympiad year such as "1184/3 BC" runs from midsummer 1184 BC to midsummer 1183 BC, so it is astronomical −1183/−1182.
- **Calendar.** Proleptic Julian unless stated otherwise. 16 April 1178 BC (Julian) is 5 April in the proleptic Gregorian calendar (computed by me with py).
- **Time scales.** UT is Universal Time, TT is Terrestrial (dynamical) Time with TT = UT + ΔT, and LAT is local apparent solar time from the Sun's hour angle at the site.
- **Provenance tags.**
  - `[B&M p.N]` is Baikouzis & Magnasco 2008, PNAS 105:8823–8828, read in full from the open-access PDF (sedici.unlp.edu.ar mirror).
  - `[Gainsford p.N]` is Gainsford 2012, TAPA 142:1–22, read in full from the open-access PDF (Zenodo 343907).
  - `[Od. x.y]` and `[Il. x.y]` are lines checked in `data/text/odyssey-grc.tsv` and `data/text/iliad-grc.tsv`.
  - `[CCX ed. N]` is a passage read in Jon's ClassicaCodex library (read-only access through `odybench.ccx`).
  - `[computed]` is my own calculation; scripts and outputs are in `results/window/jsex/`.
  - `[secondary]` means I could not read the primary source and am relying on a report of it.

---

## 1. Summary

1. **The window B&M searched.** B&M searched 1250–1115 BC (astronomical −1249 to −1114, 1,684 new moons) [B&M p.8824–8825].
   - **How they built it.** They took eight classical dates for the fall of Troy and the destruction of Troy VIIa (about 1190 BC). They dropped Duris (1333 BC) as the outlier, moved every date 10 years later to get the return, and widened the result by 10 years on each side.
   - **Where 1178 BC sits.** The window's midpoint is 1182.5 BC. It is an envelope around the ancient dates, not a window centred on Eratosthenes.
2. **Circularity.** Schoch chose the 1178 BC eclipse because it fitted the classical Troy chronology [B&M abstract]. B&M then built their window from the same chronology. That is a legitimate prior, but it is the prior that selected the eclipse in the first place, so a hit inside the window is not independent support for the chronology.
3. **1178 BC does not fit Eratosthenes plus the Odyssey's own chronology.**
   - Eratosthenes puts the sack in late spring of 1184/3 BC, that is 1183 BC (−1182) [CCX: Clement *Strom.* 1.21.138; Dionysius of Halicarnassus *Ant. Rom.* 1.63.1 and 1.74.2].
   - The Odyssey requires at least 8 years of wandering: one year with Circe and seven with Calypso [Od. 10.467–470, 7.259–261]. Its "twentieth year" formula implies about 10 years.
   - On Eratosthenes' date the return therefore falls about 1175–1173 BC (−1174 to −1172).
   - 1178 BC is only about 5 years after his sack. Fitting 1178 BC requires a sack in about 1188 BC, which no ancient chronographer gives. It falls between Eratosthenes (1184/3) and Timaeus (1193).
4. **Uniqueness inside the window is fragile, and B&M's own Table 2 shows it** [B&M Table 2, re-read by me].
   - With the four criteria they actually applied, at their thresholds, exactly one date qualifies in 136 years.
   - Loosen the Venus threshold from 90 to 85 minutes and the Mercury tolerance to ±4 days, and three dates qualify (1237, 1178 and 1157 BC).
   - Loosen the Mercury tolerance to ±8 days at 90 minutes, and seven dates qualify.
   - Their rarity figure of "one day in about 2,000 years" assumes Mercury matches on the exact day (1/116) and includes the equinox criterion, which they said they would not rely on.
   - At the rate observed in their own table (one per 135 years), the expected number of qualifying dates is 1.85 in a 250-year window and 3.7 in a 500-year window.
5. **Under modern ΔT, 1178 BC is not the only suitable eclipse, and it is not certainly total at Ithaca** [computed with NASA's 5MCSE Besselian elements and the JSEX algorithm].
   - At the canon's nominal ΔT (28,590 s), 16 April 1178 BC was a 98.4% partial eclipse at Ithaca at about 11:44 LAT. Totality crossed Corfu, not Ithaca.
   - Ithaca is in totality only if ΔT is 220 to 990 s higher than nominal. With Huber's σ ≈ 1,008 s, that has a probability of about 0.25.
   - B&M's own window also contains the eclipse of **30 September 1131 BC (−1130)**. At nominal ΔT it was total at Ithaca, at about 11:16 LAT, with probability about 0.41 under ΔT uncertainty.
   - Just outside their window is **24 June 1312 BC (−1311)**. It was near noon and total in the Ionian Islands at nominal ΔT. At Ithaca specifically, its probability of totality is about 0.20.
   - So "the only eclipse of the century" holds only if the season is fixed to spring. An autumn reading of the Odyssey has been argued (Austin 1975, as reported in [Gainsford p.8]), and 1131 BC fits that reading.
6. **How chance scales with window width** (section 7).
   - The chance of at least one date meeting the clue set rises as 1 − e^(−λW).
     - At B&M's stated rate it is 4.7% for 100 years, 6.3% for 135, 9.1% for 200 and 21% for 500.
     - At the rate their own table shows for the applied criteria it is 52%, 63%, 77% and 97.5%.
   - The chance of at least one near-noon total eclipse at Ithaca (within ±1σ ΔT) is 31%, 41%, 53% and 92% for those widths (empirical, 1500–600 BC).
   - The "double hit" (a clue-set date that is also such an eclipse) grows only linearly with W. For fixed, pre-registered criteria it is roughly 10⁻⁵ to 10⁻³ for a 135-year window.
   - So the window width matters less than whether the criteria were fixed before the target date was known. That question belongs to the forking-paths null model.
7. **Recommended windows.**
   - **Primary, pre-registered:** 1350–1100 BC (−1349 to −1099). It covers every ancient sack date including Duris, Troy VIh (about 1300 BC) and Troy VIIa, plus the 8–11-year return offset and a margin.
   - **Reproduction:** B&M's 1250–1115 BC.
   - **Archaeological sensitivity:** Troy VIIa only, 1240–1150 BC.
   - **Background:** 1500–600 BC.
   - Report rates per century and the probability of at least one hit as a function of W, never "unique in the window".
8. **Composition and oral transmission.**
   - Composition. The Odyssey's composition is dated from about 743–713 BC (Janko, linguistic) to about 650–600 BC (West and others). Its written fixation may be as late as the late 6th century BC.
   - The gap. That puts 435 to 580 years between 1178 BC and composition, about 400 of them with no writing in Greece.
   - What survives oral transmission. Comparative scholarship finds that the gist of an event can survive oral transmission for a very long time. It does not find that day-level dates or calendar facts survive.
   - Eclipse identification in oral history. The identification is notoriously circular: a suitable eclipse can be found for almost any proposed date (Henige 1976).
   - The ancient scholia. They explicitly deny that an eclipse happened [scholia B and V on Od. 20.356].

---

## 2. What B&M searched, and why

All points in this section are from B&M, read in full.

- **The window.** Classical estimates for the fall of Troy, in years BC, are listed as: 1135 (Ephorus), 1172 ("Solsibus", i.e. Sosibius), 1184 (Eratosthenes), 1193 ("Plato"), 1208 (Parian chronicle), 1212 (Dicaearchus), about 1250 (Herodotus) and 1333 (Douris). The Troy VIIa destruction layer is "≈1190 B.C." [B&M p.8824].
  - B&M drop Douris "separated from the others by the largest margin". From the remaining dates they derive 1240–1125 BC for Odysseus' return, which is the sack date minus 10 years in BC numbering.
  - They then extend the range by 10 years on each side, giving 1250–1115 BC [B&M p.8825].
  - In astronomical years this is −1249 to −1114: 136 calendar years, which they call 135.
  - They enumerate all 1,684 new moons in the range [B&M p.8825].
- **The Schoch and Neugebauer background.** The abstract reports that Schoch and Neugebauer computed in the late 1920s that the eclipse of 16 April 1178 BC was total over the Ionian Islands. It was the only suitable eclipse in more than a century consistent with a sack about a decade earlier, around 1192–1184 BC [B&M p.8823].
  - The references are Schoch 1926 (*The Observatory* 49:19–21; *Die Sterne* 6:88; *Die sechs griechischen Dichter-Finsternisse*) and P. V. Neugebauer 1929 (*Astronomische Chronologie*) [B&M refs 1, 12–14].
  - This Neugebauer is Paul Viktor, not Otto.
  - `[secondary]`: I could not read Schoch or P. V. Neugebauer. ADS returned an empty page for 1926Obs....49...19S.
- **Software, ΔT and conventions** [B&M p.8825].
  - Software: Starry Night Pro, which uses VSOP87 and ELP-2000/82. ΔT "for our eclipse" was 27,602.7 s.
  - Eclipse tracks came from EmapWin, "custom-corrected" to Espenak's ΔT.
  - Dates are Julian. Times are local to the Greek islands.
  - The NASA 5MCSE catalogue uses ΔT = 28,590 s for this eclipse (catalogue page SE-1199--1100, read by me). The two ΔT values cannot be compared directly, because a ΔT value belongs to a particular lunar ephemeris and its tidal acceleration.
- **The criteria.** T is the new moon on the slaughter day, Day 0 [B&M p.8825–8826].
  - (i) On T−29 at nautical twilight, the Pleiades and Boötes are visible together, and the 17 sailing days fall within 17 February–4 April [Od. 5.272–277].
  - (ii) On T−5, Venus rises at least 90 minutes before the Sun [Od. 13.93–95].
  - (iii) On T−34, Mercury is "within a few days" of its westernmost rising azimuth [Od. 5.44–54, conjectural].
  - (iv) T is a new moon [Od. 14.161–162 = 19.306–307; 14.457].
  - (v) An equinox criterion: 1 April ≤ T−11 ≤ 5 April. B&M call it "far more conjectural" and do not apply it in the colour-coding [B&M p.8826].
- **The result.** A single date in the span meets all criteria "as stated": 16 April 1178 BC [B&M p.8826]. Two dates narrowly miss them; B&M discuss these in their SI, which I have not read, and neither meets the equinox criterion.
- **Rarity.** About one new moon in 6 years satisfies the equinox and Pleiades criteria. One third of those have a high Venus. Mercury's turning point comes once every 116 days. Hence about one exact match in 2,000 years [B&M p.8826]. My check of the arithmetic: 6 × 3 × 116 days gives one match per about 2,088 years.
- **The eclipse.** The 5MCSE catalogue lists −1177 Apr 16 as #01966, total, Saros 39, γ = 0.5187, magnitude 1.0599. Greatest eclipse is at 17:57:28 TD at 33°N 13°E, with a 228 km path and 4 m 33 s duration (catalogue page, read by me).
  - That is about 10:01 UT, near Tripoli in Libya. B&M give the greatest-eclipse point as 32.7°N 12.7°E [B&M p.8828].
  - Gainsford dates the eclipse "26 April 1178" [Gainsford p.1]. That matches neither B&M and NASA (16 April Julian) nor the proleptic Gregorian date (5 April), so it is probably a slip.

---

## 3. Ancient dates for the fall of Troy

| Authority | Fall of Troy | Astronomical year of the sack | Basis | How I verified it |
|---|---|---|---|---|
| Duris of Samos | 1334/3 BC | −1333/−1332 | 1,000 years from the capture of Troy to Alexander's crossing into Asia (334 BC) | Clement, *Strom.* 1.21.139.2 [CCX ed. 1486], read |
| Eretes (?) | 1291 BC | −1290 | FGrHist 242 F 1 | [secondary: Wikipedia "Trojan War" §Dates] |
| Herodotus | over 800 years before himself; "≈1250" | about −1249 | Pan lived about 800 years before Herodotus, and that is fewer years than have passed since Troy | Hdt. 2.145.4 [CCX eds. 686/687], read. The figure 1250 is a modern inference (Herodotus was writing about 440–425 BC) |
| Dicaearchus | 1212 BC | −1211 | *Bios Hellados* | [secondary: Wikipedia; B&M] |
| Marmor Parium | 1209/8 BC | Thargelion falls in 1208 BC (−1207) | 945 years before the archonship of Diognetus (264/3 BC), in the 22nd year of Menestheus, 7th day from the end of Thargelion | FGrHist 239 A24 (§25 in ToposText) [secondary: ToposText translation; Wikipedia] |
| Timaeus | 1193 BC | −1192 | FGrHist 566 F 125 | [secondary: Wikipedia]. B&M give 1193 to "Plato", which I could not verify |
| **Eratosthenes** | **1184/3 BC** | **late spring 1183 BC (−1182)** | Intervals of 80 years (sack to Return of the Heraclids), 60 (to the Ionian migration), 159 (to Lycurgus' guardianship) and 108 (to the year before Olympiad 1). That is 407 years back from 777/6 BC, giving 1184/3 BC | Clement, *Strom.* 1.21.138.1 [CCX ed. 1486], read. Cross-check: Cato's "432 years after Troy" falls in Olympiad 7.1 (752/1 BC) by Eratosthenes' canons, which again gives 1184/3 [Dion. Hal. *Ant. Rom.* 1.74.2, CCX ed. 1192] |
| Sosibius | 1172 BC | −1171 | FGrHist 595 F 1 | [secondary: Wikipedia; B&M] |
| Ephorus | 1135 BC | −1134 | FGrHist 70 F 223 | [secondary: Wikipedia; B&M] |

Notes:

- **Day and season.**
  - Dionysius says Troy was taken late in the season, 17 days before the summer solstice, on the 8th day from the end of Thargelion by Athenian reckoning [Dion. Hal. *Ant. Rom.* 1.63.1, CCX ed. 1192, read].
  - The Parian Marble also puts it in Thargelion.
  - Thargelion is the 11th Attic month, so a sack in the Attic year "1184/3" falls in calendar 1183 BC. Most modern writers simply say "1184 BC".
  - Hellanicus gives 12 Thargelion [secondary: Wikipedia, FGrHist 4 F 152].
- **Spread.** The ancient dates span about 200 years, from 1334 to 1135 BC. Wikipedia gives their mean as about 1220 BC [secondary].
  - They mostly derive from genealogies of kings, and all are at least seven centuries after the supposed event, with no written intermediaries [Gainsford p.12].
  - Clement's other intervals, for Phanias, Ephorus, Timaeus and Cleitarchus, are counted from the Return of the Heraclids. Turning them into sack dates depends on the interval assumed (Clement himself gives 80, 120 or 180 years). For Eratosthenes, his 774-year figure does not reproduce Eratosthenes' 1104 BC Return exactly. I treat those conversions as unverified.
- **Ancient dates for Homer relative to Troy** [CCX ed. 1486, *Strom.* 1.21.117, read]. These show how uncertain the gap between the event and the poet was even in antiquity.
  - Crates: Homer about 80 years after the sack.
  - Eratosthenes: after the 100th year from the sack.
  - Theopompus: 500 years after the expedition.
  - Herodotus: Homer and Hesiod not more than 400 years before himself, so about 850 BC [Hdt. 2.53.2, CCX, read].
  - Parian Marble: Homer 643 years before 264/3 BC, that is 907/6 BC [ToposText §30, secondary].

---

## 4. Archaeology of Troy VI and VIIa

| Layer and event | Date | Character | Source |
|---|---|---|---|
| Troy VIh end | about 1300 BC (about 1275 in older literature) | Collapsed masonry and subsidence suggesting an earthquake. Not burned, no victims | [secondary: Wikipedia "Troy", citing Jablonka 2011, Bryce 2006 pp.64–66, Rose 2014 p.30; Wikipedia "Trojan War"] |
| Troy VIIa (= VIi) end | about 1180 BC (Wikipedia); "≈1190" (B&M) | Burned destruction layer with signs of enemy attack. The Korfmann excavations found bronze arrowheads and fire-damaged human remains in early-12th-century layers | [secondary: Wikipedia "Troy", citing Jablonka 2011, Bryce 2006 p.59] |
| Blegen's date for VIIa | about 1240, later raised to about 1270 BC | | [secondary: Rutter, Dartmouth *Aegean Prehistory* Lesson 27] |
| Rutter's judgement | probably within about 1230–1180 BC. Nylander argued for 1200–1190; Podzuweit for lower | | same source |
| Mountjoy 1999 (*Studia Troica* 9:295–346) | end of VIIa at the transition from LH IIIB2 to IIIC Early, about 1210–1190 BC | Dated by Mycenaean pottery | [secondary: search-result summary; not read] |
| Radiocarbon | 40 Middle and Late Bronze Age samples fall into 4 clusters. Cluster 3 (Troy VI Late) has a midpoint around 1400 BC and ends in an earthquake. Cluster 4 (Troy VIIa and VIIb1) has a midpoint around 1190 BC | Clusters are separated by about 100 years, and the method resolves about 100–300 years. Radiocarbon puts VIIa in the 12th century but cannot separate 1210, 1180 and 1150 BC | Demján & Pavúk 2021, *Radiocarbon* 63:429–438, read (CC BY). The underlying data are Kromer, Korfmann & Jablonka 2003 (not read) and Pavúk 2020 (not read) |
| Hittite evidence | A dispute over Wilusa (Troy) appears in the Tawagalawa letter, under Hattusili III (1267–1237) or perhaps Muwattalli II (1295–1272) | A war, if there was one, could date to the 1290s or earlier | [Gainsford p.12–13, citing Bryce 2005, 2006, and Gurney 2002] |

Gainsford's point stands: Troy VIh has not been ruled out as "Homeric Troy". He suggests extending the search to 1350–1250 BC, and lists four eclipses close to Ithaca in that period: 1340 BC (total), 1312 BC (total), 1281 BC (annular) and 1261 BC (annular) [Gainsford p.13 n.32]. My computation (section 6) reproduces all four.

---

## 5. The Odyssey's own chronology

I checked every line below in `data/text/odyssey-grc.tsv` and `iliad-grc.tsv`.

- **The return in the twentieth year.** Nine lines say it.
  - 2.175 (Halitherses' prophecy, with ἐεικοστῷ ἐνιαυτῷ).
  - 16.206, 19.484, 21.208 and 24.322 (all ἤλυθον εἰκοστῷ ἔτεϊ ἐς πατρίδα γαῖαν).
  - 17.327 (Argos).
  - 19.222 (this is now the twentieth year since he left).
  - 23.102 and 23.170 (ἔλθοι ἐεικοστῷ ἔτεϊ).
  - All four lines named in the task (2.175, 16.206, 19.484, 23.102) are confirmed.
- **The length of the war.** Nine years of war, with Troy taken in the tenth: Od. 3.118 (εἰνάετες), 5.107, 14.240–241, 22.228; Il. 2.134, 2.295, 2.328–329.
- **The wanderings.** Circe kept him a full year (10.467–470). Calypso kept him seven years, and he left when the eighth came round (7.259–261). Aeolus held him a month (10.14), and the south wind at Thrinacia blew for a month (12.325). The rest is legs of 6, 9 and 17 days.
  - The narrated wanderings therefore add up to about 8 years and a few months after the sack.
  - The ordinal "twentieth year", after about 9–10 years of war, implies a return about 9–10 years after the sack.
  - **Offset for the bench:** return = sack + 8 to 11 years, allowing for inclusive counting.
- **The number is a formula.**
  - Helen's "twentieth year since I left my homeland" [Il. 24.765–766] is spoken in the tenth year of the war. Apollodorus reconciles it with a tradition of a 20-year war: an aborted first expedition to Mysia and an eight-year interval before Aulis [Apollod. *Epit.* 3.18, CCX ed. 1453, read].
  - The same slot holds "fifth year" in Odysseus' lie to Laertes [Od. 24.309–310].
  - Homeric "typical numbers" (9 then 10, 17 then 18, 6 then 7) are poetic, not records [Gainsford p.13–15, citing Hawke 2008 and de Jong 2001].
  - The internal chronology is coherent at the level of "about ten years after the sack". It is not reliable to the year.

---

## 6. Circularity check

1. **The eclipse was chosen by the chronology.** Schoch looked for an eclipse a decade after a sack in about 1192–1184 BC [B&M p.8823]. The match between the eclipse and the traditional date was built in; it is not evidence.
2. **The window comes from the same chronology.** B&M's window is an envelope around the classical dates, about 1250 to 1135 BC moved later by 10 years, plus Troy VIIa. It is not centred on Eratosthenes: its midpoint is 1182.5 BC. 1178 BC sits near the middle, 72 years from the early edge and 63 from the late edge. This is a reasonable prior, but it is the same prior that produced the candidate.
3. **Eratosthenes plus Homer does not give 1178 BC** (computed by me from the sources above).
   - The sack falls in late spring 1183 BC (−1182). Adding the at-least-8-year internal chronology gives a return no earlier than mid-1175 BC (−1174); for a spring return that means spring 1174 BC (−1173).
   - The "twentieth year" reading gives 1174/1173 BC (−1173/−1172).
   - 1178 BC (−1177) is 4.9 years after Eratosthenes' sack. That is too early by at least 3 years.
   - For 1178 BC to be 8–10 years after the sack, the sack must fall in about 1188–1187 BC (−1187/−1186). No ancient authority gives that date. It lies between Eratosthenes (1184/3) and Timaeus (1193), and inside Schoch's "1192–1184".
   - Gainsford notes that Wikipedia's Odyssey article (2011) said the B&M argument "places" the fall of Troy in 1188 BC [Gainsford p.5]. That is an output of the argument, not an independent input.
4. **The rarity figure was computed after the fact** (my reading of [B&M p.8825–8826]).
   - The method states a Mercury tolerance of "within a few days". The rarity arithmetic uses an exact-day match (1/116), which is the precision achieved for 1178 BC (Δ = 0 in their Table 2).
   - The rarity arithmetic includes the equinox criterion that the method does not apply.
   - Using the stated tolerance (±3 days, so 7/116) with the equinox criterion gives one match per about 300 years, not per 2,000.
5. **Uniqueness depends on the window.** In B&M's Table 2, under the criteria they applied:
   - Mercury Δ = 0 happens three times: 1224, 1178 and 1157 BC.
   - Venus rises at least 90 minutes ahead in 7 of the 28 listed years.
   - Only 1178 BC meets both. 1157 BC misses the Venus threshold by 5 minutes (1 h 25 m 12 s), and 1237 BC by 4.4 minutes with Mercury Δ = −4.
   - At the observed rate of about one per 135 years, a fair window of 250 years or more is expected to hold about 2–4 qualifying dates (section 7).

---

## 7. Eclipses near Ithaca, 1500–600 BC (computed)

**Method.**
- **Inputs.** The Besselian elements are those of the Five Millennium Canon (Espenak & Meeus 2006). Local circumstances come from NASA's JavaScript Solar Eclipse Explorer code (`program.js`, O'Byrne & Espenak, GPL), run in Node with the per-century element files `SEm1499.js` through `SEm0699.js` from eclipse.gsfc.nasa.gov/JSEX/.
- **Site.** Ithaca is taken as 38.37°N 20.72°E.
- **ΔT uncertainty.** I varied the hour-angle ΔT of each eclipse by up to ±2σ. σ comes from Huber's formula on NASA's 5MCSE uncertainty page: 365.25·N·√((N·0.058/3)(1+N/2500))/1000 s, with N = |year − (−500)|.
- **Results.** Scripts: `results/window/jsex/local.js`, `scan.js`, `finescan.js`, `windows.py`. Outputs: `ithaca.jsonl` (2,138 eclipses), plus Kefalonia, Zakynthos, Lefkada and Corfu, and `windows-out.txt`.

**Instrument checks.**
- Munich, 11 August 1999: total at 10:38 UT.
- Side, Turkey, 29 March 2006: total at 10:57 UT.
- Paris, 11 August 1999: partial, magnitude 0.99.
- For 1178 BC, the path at nominal ΔT runs from Tripoli through Malta to Corfu, matching the 5MCSE map image I viewed. The model puts the greatest-eclipse point next to Tripoli, as B&M say.
- The model reproduces Gainsford's four NASA-based eclipses near Ithaca for 1350–1250 BC.

### 7.1 The candidates

| Eclipse (Julian) | At Ithaca, nominal 5MCSE ΔT | Total at Ithaca if ΔT is offset by | σ(ΔT) | P(total at Ithaca) under N(0, σ) | Notes |
|---|---|---|---|---|---|
| 16 Apr 1178 BC (−1177) | partial, magnitude 0.984; maximum 10:22 UT, about 11:44 LAT, about 18:19 TT; Sun altitude 57° | +220 to +990 s | 1,008 s | 0.25 | Total at Corfu at nominal ΔT (P ≈ 0.30). Under B&M's Starry Night ΔT value, read on the 5MCSE ephemeris, the magnitude at Ithaca would be only about 0.91. That comparison mixes ephemerides; see section 2 |
| 30 Sep 1131 BC (−1130) | **total**, magnitude 1.049; 09:49 UT, about 11:16 LAT; Sun altitude 52° | −630 to +340 s | 899 s | 0.41 | **Inside B&M's window.** It is a new moon, near noon and in autumn. Catalogue #02087, total |
| 24 Jun 1312 BC (−1311) | partial, 0.984; about 12:09 LAT; Sun altitude 75° | +540 to +1,440 s | 1,350 s | 0.20 | Total in the Ionian Islands at nominal ΔT (5-island union). Greatest eclipse at 39°N 17°E. Gainsford lists it |
| 8 Jan 1340 BC (−1339) | total, 1.039; about 09:49 LAT; Sun altitude 21° | covers 0 | 1,426 s | high | Morning, winter |
| 6 Apr 648 BC (−647) | total at Ithaca; 0.995 at Paros and Thasos | | 93 s | | The Archilochus eclipse (fr. 122 West), a positive-control candidate |

Correlated ΔT errors (my inference): the 1178 and 1131 BC eclipses are 47 years apart, so their ΔT errors are nearly equal. Their windows for totality at Ithaca overlap only near +220 to +340 s. Whichever ΔT is true, at most about one of the two was total at Ithaca.

### 7.2 Base rates at Ithaca

The rate is the number of events in 1500–600 BC (−1499 to −600).

| Event class | Events in 900 years | Rate |
|---|---|---|
| A. Total at nominal ΔT, Sun up | 6 | 1 per 150 years |
| B. Total for some ΔT within ±1σ | 10 | 1 per 90 years |
| C. Total for some ΔT within ±2σ | 11 | 1 per 82 years |
| D. Class B and 10–14 h LAT ("near noon", Schoch-style) | 3 | 1 per 300 years |
| E. Central (total or annular) within ±2σ | 28 | 1 per 32 years |
| F. Magnitude ≥ 0.95 at nominal ΔT | 15 | 1 per 60 years |
| Ionian region (any of 5 islands), class B | 12 | 1 per 75 years |
| Ionian region, class D | 4 | 1 per 225 years |

B&M quote about one total eclipse per 370 years at a given place [B&M p.8823, citing Guillermier & Koutchmy 1999]. Ithaca in this era had more (6 at nominal ΔT where 2.4 would be expected), so the bench should use the site's computed rates, not the global average.

Class counts inside specific windows:
- **B&M's 1250–1115 BC:** class B has 2 (1178, 1131); class D has 2; class F has 3 (adds 12 January 1182 BC, 0.968, in the morning).
- **Proposed 1350–1100 BC:** class B has 4 (1340, 1312, 1178, 1131); class D has 3 (1312, 1178, 1131).

---

## 8. How the chance of a coincidental hit scales with window width

**8a. At least one date meeting the clue set in a window of W years.** Poisson, P = 1 − e^(−λW). Computed by me with `scaling.py`; the rates come from B&M's text and their Table 2.

| Rate λ (source) | W = 100 | 135 | 200 | 250 | 500 |
|---|---|---|---|---|---|
| (a) 1 per 2,088 years: B&M's stated rarity, with the equinox criterion and exact-day Mercury | 0.047 | 0.063 | 0.091 | 0.113 | 0.213 |
| (a′) 1 per 298 years: B&M's arithmetic with their stated ±3-day Mercury tolerance | 0.285 | 0.364 | 0.489 | 0.567 | 0.813 |
| (b) 1 per 135 years: B&M Table 2, the 4 applied criteria at their thresholds (1 date) | 0.523 | 0.632 | 0.773 | 0.843 | 0.975 |
| (c) 3 per 135 years: Table 2 with Venus ≥ 85 min and Mercury within ±4 days | 0.892 | 0.950 | 0.988 | 0.996 | 1.000 |
| (d) 7 per 135 years: Table 2 with Venus ≥ 90 min and Mercury within ±8 days | 0.994 | 0.999 | 1.000 | 1.000 | 1.000 |

Rates (b) to (d) rest on very few events: one, three and seven dates in one window. The Poisson 95% interval for one event in 135 years is about 0.025 to 5.6 events. The bench should measure these rates directly over 1500–600 BC.

**8b. At least one candidate eclipse at Ithaca in W years.** Empirical, from sliding windows over 1500–600 BC (computed).

| Class | W = 100 | 135 | 200 | 250 | 500 |
|---|---|---|---|---|---|
| A. Total at nominal ΔT | 0.58 | 0.72 | 0.92 | 1.00 | 1.00 |
| B. Total within ±1σ ΔT | 0.75 | 0.85 | 0.93 | 1.00 | 1.00 |
| D. Class B and near noon | 0.31 | 0.41 | 0.53 | 0.57 | 0.92 |
| F. Magnitude ≥ 0.95 | 0.90 | 0.97 | 1.00 | 1.00 | 1.00 |

**8c. Expected "double hits": a clue-set date that is also an Ithaca eclipse.** The count is λ·W·p_e, where p_e is the probability that a given new moon is such an eclipse. p_e is 8.98×10⁻⁴ for class B and 2.70×10⁻⁴ for class D (computed). The table uses class D; class B values are 3.3 times larger.

| Rate | W = 100 | 135 | 200 | 500 |
|---|---|---|---|---|
| (a) | 1.3×10⁻⁵ | 1.7×10⁻⁵ | 2.6×10⁻⁵ | 6.5×10⁻⁵ |
| (b) | 2.0×10⁻⁴ | 2.7×10⁻⁴ | 4.0×10⁻⁴ | 1.0×10⁻³ |
| (d) | 1.4×10⁻³ | 1.9×10⁻³ | 2.8×10⁻³ | 7.0×10⁻³ |

**Reading the tables** (my inference).
- The claim that one date is unique in the window is very sensitive to W and to the thresholds. Under the applied criteria it is roughly what a 135-year window should produce by chance.
- The claim that the unique date is also an eclipse is not very sensitive to W. It rises only linearly, by about 3.7 times from 135 to 500 years, and it stays small (10⁻⁵ to 10⁻²) for criteria fixed in advance.
- B&M's criteria were not fixed in advance. The date was known (Schoch), and the references, thresholds, season and chronology were chosen with it in view [Gainsford p.6–11, 15–18].
- So the decisive null is the forking-paths and look-elsewhere model: how often can a flexible reading of the text make some eclipse in a plausible window the unique match? The window width alone is not decisive.
- Defining the eclipse target also changes base rates by a factor of 5 or more: Ithaca or the region, total or deep partial, near noon or any time, how ΔT is handled. These choices must be pre-registered too.

---

## 9. What window should a fair bench use

1. **Prior for the sack.** Take the union of three things.
   - The ancient chronographers: 1334/3 (Duris) to 1135 (Ephorus). Do not drop the outlier.
   - The archaeology: Troy VIh about 1300 BC; Troy VIIa about 1230–1180 BC; radiocarbon cluster around 1190 BC with resolution of about 100 years or more.
   - The Hittite Wilusa episodes (1290s to 1230s BC).
2. **Return offset.** Add 8 to 11 years after the sack (section 5).
3. **Primary pre-registered window: 1350–1100 BC (astronomical −1349 to −1099; 251 years).** This is the sack range shifted by the offset, with a ±10-year margin as B&M used.
4. **Reproduction window: 1250–1115 BC (−1249 to −1114)**, exactly as B&M.
5. **Sensitivity windows.**
   - Troy VIIa only: 1240–1150 BC (−1239 to −1149).
   - Strict Eratosthenes: return 1176–1172 BC (−1175 to −1171). 1178 BC falls outside it.
   - Agnostic background: 1500–600 BC (−1499 to −599), or as far as the elements go (5MCSE reaches −1999).
6. **What to report.** For every window, report qualifying dates per century and the probability of at least one hit as a function of W, for W from 50 to 900. Do not report "the single date in the window".
7. **Positive controls with the same machinery.**
   - The Archilochus eclipse of 6 April 648 BC (−647), which is near-contemporary and explicit.
   - The Thales eclipse of 28 May 585 BC (−584), reported in Herodotus 1.74 about 150 years later.
   - In 800–500 BC, ΔT σ is 100–450 s rather than 1,000–1,400 s, so a negative result there means something.
   - Run each control in windows of the same widths, so that the window effect itself is calibrated.

---

## 10. When was the Odyssey composed

**Ancient views.**
- Herodotus put Homer not more than 400 years before his own time, so about 850 BC [Hdt. 2.53.2, read].
- The Parian Marble gives 907/6 BC [secondary].
- Ancient chronographers put Homer 80 to 500 years after Troy [Clement *Strom.* 1.21.117, read].

**Modern estimates.**

| Scholar | Date | Basis | Source |
|---|---|---|---|
| Janko 1982 | Iliad about 750–725 BC, Odyssey about 743–713 BC | Linguistic statistics | [secondary: Perseus Encyclopedia "Homer" and Kiwi Hellenist 2021, via search summaries; book not read] |
| Powell | 800–750 BC | | [secondary: Wikipedia "Homer", citing Powell 1996] |
| Altschuler, Calude, Meade & Pagel 2013 (*BioEssays*) | Iliad 762 BC with a historical prior (95% CI 1157–376 BC); 707 BC without it (61 BC–1351 BC) | Phylogenetic dating of vocabulary | [PMC3654165, read via fetch] |
| West | Iliad about 660–650 BC at the earliest; Odyssey up to a generation later | | [secondary: Wikipedia "Homer", citing West 2011 and 2012, and Hall 2002] |
| van Wees | 670–650 BC | | [secondary: Kiwi Hellenist] |
| Burkert 1976 | Iliad after 663 BC | Allusion to Egyptian Thebes | [secondary: Kiwi Hellenist] |
| Nagy | No single date. An evolving tradition that stabilised by the 6th century BC and kept changing until the mid-2nd century BC | | [secondary: Wikipedia "Homer"] |
| Gainsford (blog) | Prefers the 600s BC; puts dissemination in the late 6th century in Athens | | [Kiwi Hellenist 2021, read via fetch summary] |

**Working range.** The Odyssey was composed about 750–600 BC, possibly fixed in writing as late as about 520 BC.
- The gap from 1178 BC is about 435 years (Janko) to 580 years (late 7th century), and about 650 years to Peisistratean fixation (computed).
- Writing: Linear B ends with the palaces around 1200 BC. The Greek alphabet comes into use in the late 9th or early 8th century BC; the oldest inscriptions, the Dipylon oinochoe and Nestor's cup, date from about 740–720 BC. So about 400 years of the gap had no writing at all [secondary: Wikipedia "Greek alphabet", "Dipylon inscription", "Greek Dark Ages" citing Knodell 2021, "Linear B"].

---

## 11. Could a specific sky observation survive 400–600 years of oral transmission?

**The gist survives; the date does not.**
- Nunn & Reid 2016 (*Australian Geographer* 47:11–47) document Aboriginal stories from 21 coastal locations of land lost to the sea. They read these as memories of post-glacial sea-level rise more than about 7,000 years old [secondary: abstract via search summary].
- The dating there comes from geology. The stories carry what happened, not when.

**Eclipses in oral tradition are understood but not dated.**
- Hamacher & Norris 2011 (*J. Astron. Hist. Heritage* 14(2)) survey 50 Aboriginal accounts of eclipses. The accounts show causal understanding and treat eclipses as omens; they are not datable records [abstract, arXiv 1105.2635, read].

**Matching eclipses to oral history is circular.**
- Henige 1976, "'Day was of sudden turned into night': On the use of eclipses for dating oral history", *Comparative Studies in Society and History* 18:476–501, reviews African cases (Bunyoro, Ankole, Buganda, Kuba, Dahomey).
- He finds the eclipse references vague, that they migrate between sources, and that matching them is circular. He remarks that a suitable eclipse could be found for almost any proposed date of the Trojan War [secondary: the Cambridge abstract page, via fetch summary; full text not read].
- The Haudenosaunee League shows the same pattern. Its founding "sign in the sky" has been tied to the eclipses of 1142, 1451 and 1536 AD, each choice following the chronology the scholar assumed (Mann & Fields 1997, *American Indian Culture and Research Journal* 21(2)) [secondary: search summary].
- That is the same structure as Schoch's choice of the 1178 BC eclipse.

**Standard references I did not read in this session.**
- Vansina, *Oral Tradition as History* (1985), and Henige, *The Chronology of Oral Tradition* (1974): chronology is the most fragile element of oral tradition, through telescoping and the "floating gap".
- Lord, *The Singer of Tales* (1960): epic is recomposed in each performance, and specifics such as numbers and names drift.

**What the Homeric tradition did carry from the Bronze Age.**
- Some concrete objects, kept alive in formulae: the boar's-tusk helmet [Il. 10.261–265] and Ajax's tower shield [Il. 7.219]. Both lines checked.
- Homeric star lore, by contrast, is generic and formulaic. Od. 5.272–277 repeats Il. 18.486–489 almost word for word, and Hainsworth (1988) judges it general astronomical lore, not navigational or seasonal data [Gainsford p.8–10].
- Greek poetic eclipses that are genuinely datable are contemporary or nearly so: Archilochus fr. 122 West (648 BC) and Stesichorus fr. 271 Page (557 BC) [Gainsford p.6 n.15].

**Ancient readers.**
- The Odyssey scholia flatly deny that an eclipse happened. Scholion B on 20.356 reads Theoclymenus as foreseeing in prophetic frenzy that the sun would be eclipsed for the suitors; scholion V agrees [local `scholia-odyssey-grc.tsv`, entry 2.20.2.91, read].
- Plutarch quotes the line in an eclipse context in *De facie* 19 (931E) [CCX ed. 369, read].
- Heraclitus (*All.* 75) reads it allegorically [Gainsford p.2 n.3].

**B&M's own assessment.**
- They call preservation through centuries of oral tradition improbable, though not impossible.
- They float a Babylonian route through the exeligmos: the eclipse of 18 May 1124 BC (−1123) passed near Babylon. They decline to argue for it [B&M p.8827–8828].
- Their mechanism needs the day, a near-noon totality and five weeks of Venus and Mercury positions to be carried forward. That is far beyond anything the comparative literature shows surviving without writing.

**Assessment** (my inference).
- No evidence I found shows a day-dated astronomical observation surviving 400 years or more of non-literate transmission.
- The bench should treat the prior as very low. Its first question should be whether the text carries recoverable date information at all, tested with positive controls, before asking which date it carries.

---

## 12. Open questions and what I could not verify

- **Not read:** Schoch 1926 (three items), P. V. Neugebauer 1929, Dörpfeld 1926, Mountjoy 1999, Pavúk 2020, Kromer et al. 2003, Austin 1975, Henige 1976 (full text) and B&M's SI (Table S2 and the near-miss dates).
- **Ancient dates not checked against FGrHist:** Ephorus 1135, Sosibius 1172, Timaeus 1193, Dicaearchus 1212 and Eretes 1291 come from Wikipedia and B&M.
- **B&M's "Plato" for 1193 BC** is unexplained.
- **ΔT and ephemeris consistency.** B&M's 27,602.7 s (Starry Night) and the 5MCSE's 28,590 s belong to different lunar tidal accelerations. The bench should recompute the sky and the eclipse track on one consistent ephemeris and ΔT model, and carry the ΔT uncertainty as a distribution.
- **The two other near-noon Ionian eclipses.** Does B&M's clue set, in either a spring or an autumn reading, select 30 September 1131 BC (−1130) or 24 June 1312 BC (−1311)? This should be run in the reproduction stage.
- **Season.** Spring (B&M, after MacDonald 1967), autumn (Austin 1975) or late May (MacDonald's reaping argument) [Gainsford p.8]. The choice decides which eclipses count as candidates.
- **The Gainsford date slip.** His "26 April 1178" disagrees with both the Julian and the proleptic Gregorian dates.

---

## 13. Sources

- Baikouzis C., Magnasco M. O. 2008. "Is an eclipse described in the Odyssey?" *PNAS* 105(26):8823–8828. doi:10.1073/pnas.0803317105. Read: https://sedici.unlp.edu.ar/bitstream/handle/10915/82991/Documento_completo.1073_pnas.0803317105.pdf ; PMC2440358.
- Gainsford P. 2012. "*Odyssey* 20.356–57 and the eclipse of 1178 B.C.E.: a response to Baikouzis and Magnasco." *TAPA* 142:1–22. Read: https://zenodo.org/records/343907
- Espenak F., Meeus J. 2006. *Five Millennium Canon of Solar Eclipses* (NASA TP-2006-214141). Catalogue: https://eclipse.gsfc.nasa.gov/SEcat5/SE-1199--1100.html ; map: https://eclipse.gsfc.nasa.gov/5MCSEmap/-1199--1100/-1177-04-16.gif ; JSEX code and elements: https://eclipse.gsfc.nasa.gov/JSEX/ ; ΔT uncertainty: https://eclipse.gsfc.nasa.gov/SEcat5/uncertainty.html
- Demján P., Pavúk P. 2021. "Clustering of calibrated radiocarbon dates…" *Radiocarbon* 63(2):429–438. doi:10.1017/RDC.2020.129
- Rutter J. *Aegean Prehistory*, Lesson 27: https://sites.dartmouth.edu/aegean-prehistory/lessons/lesson-27-narrative/
- Wikipedia (raw wikitext fetched 2026-10-03): "Trojan War" §Dates of the Trojan War; "Troy" §Troy VI–VII; "Homer"; "Parian Chronicle"; "Greek alphabet"; "Dipylon inscription"; "Greek Dark Ages"; "Linear B".
- ToposText, Marmor Parium: https://topostext.org/work/119
- Altschuler E. L. et al. 2013. *BioEssays* 35:417–420; PMC3654165.
- Kiwi Hellenist (Gainsford) 2021, "The dates of Homer": https://kiwihellenist.blogspot.com/2021/11/dates-homer.html
- Henige D. 1976. *CSSH* 18(4):476–501 (abstract page): https://www.cambridge.org/core/journals/comparative-studies-in-society-and-history/article/abs/day-was-of-sudden-turned-into-night1-on-the-use-of-eclipses-for-dating-oral-history/464F2A1DBE397F0F2C221318A1004E44
- Hamacher D. W., Norris R. P. 2011. *J. Astron. Hist. Heritage* 14(2); arXiv:1105.2635.
- Nunn P. D., Reid N. J. 2016. *Australian Geographer* 47(1):11–47.
- Mann B. A., Fields J. L. 1997. *American Indian Culture and Research Journal* 21(2).
- Primary texts read in the ClassicaCodex library (read-only): Clement of Alexandria, *Stromata* 1.21.117, 1.21.138–139 (ed. 1486); Dionysius of Halicarnassus, *Ant. Rom.* 1.63.1, 1.74.2 (ed. 1192); Herodotus 2.53, 2.145 (eds. 686, 687); Apollodorus, *Epitome* 3.15–19 (ed. 1453); Plutarch, *De facie* 19 (ed. 369).
- Local texts: `data/text/odyssey-grc.tsv`, `iliad-grc.tsv`, `scholia-odyssey-grc.tsv` (Dindorf).

## 14. Artifacts

These are in `C:\Projects\odybench\results\window\jsex\`:

- NASA `program.js` (GPL) and the element files `SEm1499.js`–`SEm0699.js`, plus `SE1901.js` and `SE2001.js` for the instrument checks.
- My harness: `local.js` (local circumstances and the ΔT envelope), `scan.js` and `finescan.js` (ΔT scans), `windows.py` (base rates and sliding windows), `scaling.py` (window scaling).
- Outputs: `*.jsonl`, `windows-out.txt`, `scaling-out.txt`, and `scan-*.txt` for the three candidate eclipses.
- Run with `node` (`C:\Program Files\nodejs`) and `py`.
