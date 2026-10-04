# Baikouzis & Magnasco (2008): reproduction-grade extraction (independent extraction b)

Target: Baikouzis C., Magnasco M.O. (2008), "Is an eclipse described in the Odyssey?", *PNAS* 105(26): 8823-8828, doi:10.1073/pnas.0803317105 (published online 24 June 2008, issue 1 July 2008; received 2 July 2007; communicated by M. J. Feigenbaum). Abbreviated **B&M** below.

Conventions. Dates are in the **proleptic Julian calendar**. Years are given as historical BC with the astronomical year in brackets (1178 BC = -1177). B&M's clock times are "local to the Greek islands" (B&M, Method). My check in §6.3 shows that their rise times match **UT+2 h** (zone time on the 30°E meridian), not local mean time. Times marked TT are Terrestrial Time.

Provenance tags:
- **[BM §x]**: main paper (the section heading names the section).
- **[BM T1/T2/F1/F2]**: main-paper tables and figures.
- **[SI p.n]**: Supporting Information page n of 7.
- **[S2]**: SI Table S2.
- **[S1]**: SI Table S1.
- **[me]**: my own inference or computation. The tools for each computation are listed in §14.

---

## 0. What I read, and from where

| Item | Read? | Source actually used |
|---|---|---|
| Main paper, full text | **Yes** | (a) PMC full-text HTML, **PMC2440358**, https://pmc.ncbi.nlm.nih.gov/articles/PMC2440358/ (PMID 18577587). It gives clean text and Table 1, and Table 2 as an image, which I downloaded from the PMC CDN and read. (b) The PDF of the published article as deposited at SEDICI (UNLP repository): https://sedici.unlp.edu.ar/bitstream/handle/10915/82991/Documento_completo.1073_pnas.0803317105.pdf . It is the 6-page PNAS layout, an OCR'd scan, and it carries Table 2's column headers, which the PMC image lacks. |
| Supporting Information (7 pp.) | **Yes** | Wayback Machine snapshot (2021-02-23) of `https://www.pnas.org/content/suppl/2008/06/24/0803317105.DCSupplemental/0803317105SI.pdf`. The file is 1,135,988 bytes, made with XPP, CreationDate 2008-06-24. Its size matches the "1.1 MB" Supplemental PDF that PMC lists. I parsed Table S2 together with its cell colours from the PDF drawing operators (§7). |
| Local copies | | `data/sources/bm2008-b/` holds the main-paper PDF, the SI PDF, the Table 2 image, and `table_s2.tsv` (my transcription of S2, with colour codes). |

Notes on access:
- **PMC2440355 is NOT this paper.** It is a PLoS ONE HIV article. The correct PMCID is **PMC2440358**.
- pnas.org returned HTTP 403 to scripted requests.
- PMC's own PDF and SI links sit behind a proof-of-work bot challenge. I did not bypass it.
- I could **not** read Schoch (1926) or P.V. Neugebauer (1929) themselves. The ADS scan of Schoch's note is JBIG2-encoded and I had no decoder, and the ADS scan viewer did not render. Everything about Schoch and Neugebauer below is **as reported by B&M**.
- I did read Plutarch *De facie* 19 and Heraclitus *Homeric Problems* in the local Greek texts (§12).

---

## 1. One-paragraph summary of the method [BM abstract, Method, References and Constraints]

1. Day 0 is the slaughter of the suitors, which B&M take to be a **New Moon**. They enumerate the **New Moons T_i** in **1250-1115 BC** (-1249 to -1114) and state that there are 1684 of them.
2. They map the Odyssey's day count backward from Day 0 (Table 1, "sequential" reckoning). They then require:
   - the Pleiades and Boötes to be visible as navigation stars throughout Odysseus' 17 days of sailing (T_i-28 to T_i-12, departure on T_i-29);
   - Venus to rise at least 90 min before the Sun on T_i-5;
   - Mercury to be within a few days of its "maximum western rise azimuth" (MWRA) on T_i-34, the day Hermes reaches Ogygia.
3. A fifth, "Equinox", criterion (Poseidon sinks the raft on T_i-11, on or just after the equinox, about 1 April) is **listed but not applied** in the search.
4. Their one fully satisfying date is **16 April 1178 BC (-1177)**, the date of the total solar eclipse that Schoch (1926) and P.V. Neugebauer (1929) had attached to Od. 20.356-357.
5. **The eclipse itself is not a search criterion.**

---

## 2. What B&M claim and what they disclaim

**Claims** [BM abstract; Intersecting the Constraints; Historical Plausibility; Conclusions]:
- In 1250-1115 BC one date alone closely matches their references: 16 April 1178 BCE. It satisfies all criteria as they stated them, under both the sequential and the parallel chronology, and exactly under the sequential one.
- The passages cohere: two different sets of verses (the eclipse verses and the other astronomical references) pinpoint the same date independently, with a very low chance probability.
- They call minute the odds that fictional references would coincide by accident with the century's only eclipse.
- Exact matches happen about once per 2,000 years (§9).
- **Absences** are offered in support:
  - Ares is absent from the foreground story, and Mars was invisible in March/April 1178 BC except during the eclipse.
  - The eclipse fell at noon, the time of the scene (attributed to Schoch), and in early spring.
- They conjecture that one poet built the timeline, and call him "Homer" for lack of a better name. They describe the references as structural, like a perspective grid drawn behind a painting.

**Disclaimers** [BM introduction; Historical Plausibility; Conclusions]:
- If their reading of the passages as astronomical is wrong, the dates and probabilities are wrong, and the whole calculation is a non sequitur. They say their case is far from proved.
- Even if the analysis is right, it does not show that the narrated events happened. A historical Odysseus and an allegorical one structured on an astronomical timeline are equally compatible.
- **They do not assume an eclipse.** The disputed lines 20.356-357 are not used as a criterion.
- Hermes = Mercury is the one implausible assumption. The earliest surviving Hermes-Mercury link is Plato's *Timaeus*, so the identification would push that adoption back by about two centuries.
- They rate the Equinox (Poseidon) reading as much more conjectural than Hermes. It is not applied, only listed.
- The conclusions imply sophisticated astronomy and transmission of data across about five centuries, which B&M call problematic. They decline to guess how the knowledge was acquired.
- They explicitly do not espouse the Babylonian exeligmos route (§12.4). They offer it only as a possible means.
- Dates of first and last visibility are psychophysical, not astronomical, and should carry at least ±1 day of uncertainty [BM Method].

---

## 3. The narrative day-count (Table 1) and how the offsets were derived

**Table 1** [BM T1, transcribed from PMC HTML]. Day 0 is the death of the suitors.
- **Sequential reckoning** counts parallel narrative strands one after another.
- **Parallel reckoning** puts Athena in Sparta instantly, so Odysseus' arrival in Ithaca and Athena's trip to Telemachus fall on the same day.

| Day (sequential) | Day (parallel) | Action (B&M) | Lines (B&M) |
|---|---|---|---|
| -40 | -33 | Council of the Gods; Poseidon in Ethiopia; Athena goes to Telemachus | (none given) |
| -39 | -32 | Ithaca assembly; Telemachus leaves for Pylos | (none given) |
| **-34** | **-33** | Council of the Gods; Zeus sends **Hermes to Ogygia**; Calypso tells Odysseus he can go | v.1-v.261 |
| -33 to -30 | -32 to -29 | Odysseus builds his raft | v.262 |
| **-29** | **-28** | Calypso sends him off **at sunset**; Pleiades, Boötes, the Bear on his left | v.263-v.278 |
| -28 to -12 | -27 to -11 | Sailing (17 days) | v.279 |
| **-11** | **-10** | Poseidon, returning from the Ethiopians, sinks the raft | v.280-v.387 |
| -10 | -9 | Swimming | v.388-v.389 |
| -9 | -8 | Arrives in Phaeacia | v.390-v.493 |
| -8 | -7 | Nausicaa; to Alcinous | vi.1-vii.347 |
| -7 | -6 | Palace, games, narration | viii.1-xiii.16 |
| -6 | -5 | Gifts; boards ship at sunset | xiii.17-xiii.92 |
| **-5** | **-4** | Arrives in Ithaca **with the Star of Dawn**; Athena; dines with Eumaeus | xiii.93-xiv.533 |
| -4 | -4 | Athena fetches Telemachus; he sleeps at Pherae | xv.1-xv.190 |
| -3 | -3 | Telemachus travels; Odysseus dines with Eumaeus | xv.191-xv.302; xv.303-xv.493 |
| -2 | -2 | Telemachus reaches Ithaca at dawn, meets Odysseus | xvi.1-xvi.478 |
| -1 | -1 | Odysseus in his halls; Argos; Penelope; Eurycleia | xvii.1-xx.54/90 |
| **0** | **0** | Festival day of Apollo; eclipse; death of the suitors; meets Penelope | xx.91-xxiii.344 |
| 1 | 1 | Laertes; battle; Athena stops it | xxiii.345- |

**How the offsets come out of the text.** B&M give only the table footnote. The line-level reasoning below is mine [me], checked against the local Greek text (`data/text/odyssey-grc.tsv`):
- **Raft (5.262-263).** The raft is finished on the fourth day and he leaves on the fifth. With Hermes' day = -34, the raft days are -33..-30 and departure is -29.
- **Sailing (5.278-279).** He sails 17 days, and the Phaeacian mountains appear on the 18th, which is when Poseidon sees him (5.282). Sailing is -28..-12; sinking is -11.
- **Drifting (5.388-390).** He drifts two nights and two days and lands on the third day: -9.
- B&M's footnote: Odysseus is at sea for exactly 20 days and 20 nights (he leaves near sunset and lands before sunset) [BM T1 footnote].
- **Phaeacia to Ithaca.** Phaeacian days -8, -7 and -6 (boarding at sunset, 13.17-92), then arrival before dawn with the morning star (13.93-95): -5.
- **Ithaca.** The Ithaca days are counted forward to the slaughter on Day 0.
- **Parallel vs sequential.** The two reckonings differ by exactly **one day** for every Odysseus-strand event from Hermes' visit to the Ithaca landing: -34 vs -33, -29 vs -28, -11 vs -10, -5 vs -4. The Telemachy's start differs by 7 days.
- **The search uses the sequential offsets: -34, -29, -11, -5.** The Method section states its requirements at T_i-29, T_i-5 and T_i-34 [BM Method].

---

## 4. The clues, one by one

### C0: New Moon on Day 0. Defines the search unit, not a filter.
- **Lines and B&M's reading** [BM Method]:
  - Odysseus (as beggar) tells Eumaeus (xiv.161-162) and Penelope (xix.306-307) that Odysseus will come as one month wanes and the next begins: τοῦ μὲν φθίνοντος μηνός, τοῦ δ' ἱσταμένοιο.
  - B&M say Night -2 is dark and moonless, citing xiv.457: νὺξ ... σκοτομήνιος.
  - Day 0 is said several times to be Apollo's festival day. B&M give no line numbers. My identification: 20.156 ἑορτή, 20.276-278 hecatomb in Apollo's grove, 21.258-259 the god's holy feast.
  - SI Table S1 also lists xiv.161, xiv.457 and xix.306 under "New Moon" [S1].
- **Criterion**: T_i is the New Moon date on Day 0 [BM Intersecting the Constraints]. The paper never says what that date means operationally: conjunction instant, time zone, or day boundary. See §7.3, where S2's T_i cannot be reproduced as the conjunction's civil date in any single time zone [me].
- **Offset**: 0.
- **Internal inconsistency [me]**: B&M's own Table 1 puts xiv.457 on Day **-5** (sequential) or -4 (parallel). The night of xiv.457 is the night of Odysseus' first evening at Eumaeus' hut, not "Night -2".

### C1: Pleiades and late-setting Boötes. The season test.
- **Lines**: v.270-277, Calypso's sailing instructions: 5.272 Πληιάδας τ' ἐσορῶντι καὶ ὀψὲ δύοντα Βοώτην, with the Bear kept on his left (5.273-277). [BM Method; S1.] The Bear lines recur at Il. 18.487-489; B&M cite "Il. xviii.485".
- **B&M's reading** [BM References and Constraints]:
  - Keeping the Bear on the left means sailing east.
  - The Pleiades and Boötes appear together after twilight in two seasons: around March (Pleiades set early, Boötes late) and September (the reverse). "Late-setting" Boötes selects March. They follow MacDonald (1967): the Pleiades keep the sunset direction, Arcturus the sunrise direction.
  - **Boötes is represented by Arcturus.** This is named in the SI discussion of its achronical rising and in the MacDonald quote, and Arcturus is labelled in Fig. 2 [SI p.1; BM F2].
  - The paper does not say which Pleiad stands for the cluster.
- **Numerical criterion** [BM References and Constraints; Method]:
  - The Sun is at **-12°** (nautical twilight).
  - Boötes' earliest visible date (its "apparent achronical rising") is **17 February**.
  - The Pleiades' latest visible night is **3 April**.
  - Hence T_i-29 must lie between **17 February and 4 April**. Because he navigates by these stars every night until he is sunk, the **whole 17-day sailing period must lie inside 17 Feb-4 Apr**.
  - Visibility uses Planetary, Lunar, and Stellar Visibility v3.0 with standard magnitude-corrected parameters and a **minimum altitude of 2° for the Pleiades** [BM Method].
  - B&M say one, or at most two, New Moons per year pass this criterion.
- **Offset**: departure on **T_i-29** (sequential; -28 parallel). The sailing nights run T_i-28..T_i-12.
- **Implied window [me]**: T_i-28 ≥ 17 Feb and T_i-12 ≤ 4 Apr give **T_i ≈ 17/18 Mar to 16 Apr**, about a 30-day window per year.
- **1178 BC (-1177) values** [BM Intersecting; F2]:
  - T_i-29 = 18 March, which was itself a New Moon. My check: conjunction 18 Mar 03:26 UT+2 (Meeus).
  - At nautical twilight, 7:38 p.m. (my check: 19:35 UT+2), the Pleiades were astern (west) and Boötes ahead-left. It would be visible all night.
  - The Pleiades' heliacal setting (last visible night) was the night before 5 April, i.e. 4 April.
  - **1178 BC therefore sits on the boundary**: T_i = 16 Apr is the last T_i allowed, and T_i-12 = 4 Apr is the last visible night [me].
- **Boundary inconsistency [me]**: the "last Pleiades night" is given as **3 April** in the References section, **4 April** in the probability paragraph and the 1178 narrative, and **5 April** in SI p.1 (the Palamedes discussion). Arcturus' apparent achronical rising is **17 February** in the main text and "the end of February" in SI p.1.
- **Under parallel reckoning [me]**: 1178 needs Pleiades visibility through T_i-11 = 5 April, one night past their stated last visibility.
- **Table S2 does not enforce this criterion as stated [me]**. It lists exactly one T_i per year, from 13 Mar (1243 BC) to 17 Apr (1246, 1227 BC). Some of these break the stated window: 1246 and 1227 BC have T_i-12 = 5 Apr; 1243 BC has T_i-29 = 12 Feb. In seven years a second New Moon (my Meeus calculation) would also fall in the 18 Mar-16 Apr window but is not evaluated: 1246, 1243, 1227, 1208, 1189, 1178 (the 18 Mar New Moon) and 1113 BC. See §7.

### C2: Venus "high before dawn". The morning-star test.
- **Lines**: xiii.93-95. When the brightest star, the herald of dawn, rises, the Phaeacian ship reaches the island: εὖτ' ἀστὴρ ὑπερέσχε φαάντατος [BM Method; S1].
- **B&M's reading** [BM References and Constraints]:
  - They infer that Venus rose well before dawn. Before daybreak the sailors land, put the sleeping Odysseus ashore, he wakes, talks at length with Athena, and Athena hides the treasure and goes to Sparta, where it is daybreak.
  - In this season, they note, Venus rises up to 2 h before sunrise.
- **Numerical criterion**: on **T_i-5**, **Venus rises at least 90 min before the Sun** (the "1:30 cutoff", SI p.1). They say this happens about **1/3 of the time**.
  - Table 2 and S2 list Venus rise time, sunrise and the difference on T_i-5, or leave them blank if Venus is an evening star.
  - Altitude, magnitude and heliacal visibility are not used. "High" is operationalised **only** as the rise-time lead over sunrise.
  - Colour thresholds reverse-engineered from S2 cell colours [me]: **orange** if lead ≥ 1:30 (the smallest orange is 1:32:08, 1173 BC); **yellow** if 1:02 ≤ lead < 1:30 (the largest yellow is 1:29:06, 1119 BC); **white** if lead ≤ 0:58:25.
- **Offset**: **T_i-5** (sequential; -4 parallel).
- **1178 BC value**: on 11 April Venus rose **1 h 43 min** before sunrise, at magnitude **-4.2** [BM Intersecting]. T2/S2 give 4:39:45 and 6:22:41, a lead of 1:42:56.
- **My check of the clock [me]** (§6.3): my low-precision ephemeris gives 04:40:33 and 06:24:13 in **UT+2** (lead 1:43:40). In local mean time they would be about 37 min earlier.

### C3: Hermes = Mercury. The conjectural turning-point test.
- **Lines**: v.48-55, Hermes skims the sea like a cormorant and comes out of the violet sea at the distant island. v.97-103 (S1 quotes from v.97), Hermes complains about the length of his trip. B&M also cite "v.55, v.97-103" [BM Method; S1].
- **B&M's reading**:
  - Hermes travels far west, delivers his message and immediately turns back east. This is an allegory of an apparent turning point in Mercury's motion. B&M compare the Antikythera mechanism's inscription for a "sterigmos" (station).
  - Supporting imagery: Mercury is never far from the horizon (Hermes flies low over the waves), and Hermes climbs out of the dark water at Ogygia, which B&M equate with Mercury's first morning visibility.
  - B&M themselves call this reading highly uncertain [BM References and Constraints; Historical Plausibility].
- **Numerical criterion as stated** [BM References and Constraints]:
  - On T_i-34 Mercury must be on the western side of its path, visible, and near a turning point.
  - B&M list three candidate turning-point variables, which they say occur close together in time: heliocentric elongation, the rise-time azimuth (when the rising point becomes westernmost), and the onset of retrograde motion.
  - **The test applied is that T_i-34 lies within a few days of Mercury's maximum western rise azimuth (MWRA).** B&M chose it because they expected it to cover the other turning points as well.
  - The tolerance is never stated numerically in the text. From the S2 colours [me]: **orange if |Δ| ≤ 1 day**, **yellow if |Δ| = 2**, **light yellow if |Δ| = 3**, **white if |Δ| ≥ 4**. Δ = (T_i-34) - MWRA in days; the sign convention was checked on several rows [me].
  - The Mercury visibility threshold is a **1° minimum altitude** in PLSV [BM Method]. **S2 has no visibility column.** As far as the tables show, visibility was checked only for the reported candidate [me].
- **What "MWRA" means numerically.** The paper does not define the azimuth reference. My reverse-engineering [me]:
  - MWRA is the **local maximum of Mercury's rising azimuth measured from north through east**: the **southernmost rising point**, roughly Mercury's local declination minimum during a morning apparition.
  - My calculation reproduces S2's MWRA date **exactly for 14 of 20 rows tested and within ±1 day for 17 of 20**. The misses are 1190 BC (+4 d), 1157 BC (+3 d) and 1189 BC (+8 d).
  - Maximum western elongation does **not** match. It falls 2-10 days later than S2's MWRA in most years.
  - The rising-azimuth curve is very flat at its peak (about 0.05° over 3 days in 1178 BC), so the MWRA date is intrinsically uncertain by about ±1-2 days.
- **Offset**: **T_i-34** (sequential; -33 parallel).
- **1178 BC value**:
  - T_i-34 = **13 March**. Mercury rose at its westernmost azimuth on **12 and 13 March**, and **13 March was its heliacal rising** (first visibility); it was not visible on 12 March [BM Intersecting]. S2: MWRA 13-Mar, Δ = 0.
  - My ephemeris [me]: inferior conjunction about 19 Feb; **direct station about 4-5 Mar**; rising-azimuth maximum 112.29° on 12-13 Mar; **greatest western elongation 18-19 Mar (-27.0°)**. Mercury already rose about 50-63 min before the Sun from 1 March onwards, so a 13 March first visibility depends on PLSV's magnitude/extinction model (Mercury is faint near inferior conjunction).
  - So the "three close events" are spread over about 14 days in 1178.
  - The morning-side station is the **end** of retrograde motion, not its "onset" [me].
- **Discrepancy**: SI Table S1's note to v.225 places Hermes' visit on **15 March** ("almost new moon"). The main text gives **13 March**, and the parallel reckoning would give 14 March [S1 vs BM Intersecting].

### C4: Poseidon's return from the Ethiopians = the equinox. Listed, not applied.
- **Lines**: v.282-ff (Poseidon "returning from the Ethiopians" sees the raft) [BM; S1]. In Table 1 he is "in Ethiopia" on Day -40.
- **B&M's reading**: following MacDonald (1967), the Earthshaker's return from the southern hemisphere could mean the equinox. B&M do **not** apply it; they only list it [BM References and Constraints].
- **Criterion**: **1 April ≤ T_i-11 ≤ 5 April** [BM]. The probability paragraph instead puts the sinking after the equinox (1 April) and no later than the Pleiades' heliacal setting (4 April). In S2, the "Before" column's XXX flags and orange cells mark **T_i-11 from 1 to 6 April** (1246 and 1227 BC are flagged with 6-Apr) [me].
  - Table 2's image shows 30-Mar cells (1210 and 1145 BC) in light yellow; S2 leaves them uncoloured [me].
- **Offset**: **T_i-11** (sequential; -10 parallel).
- **1178 BC value**: equinox **1 April, 3:24 p.m.**; sinking on **5 April** [BM Intersecting]. My check: 1 Apr 15:12 UT+2 (Standish/IAU76).

### C5: Theoclymenus' vision, the eclipse. Not used as a criterion.
- **Lines**: Od. 20.345-357. Athena stirs the suitors' unquenchable laughter; Theoclymenus sees night over their heads, blood on the walls, and ghosts going down to Erebus; 20.356-357 ἠέλιος δὲ / οὐρανοῦ ἐξαπόλωλε, κακὴ δ' ἐπιδέδρομεν ἀχλύς. B&M cite it as xx.356 [BM introduction; S1].
- B&M gloss ἐπιδέδρομεν as connoting a sudden or surprise attack, and κακή as "unlucky" in omen contexts. They set the scene at the noon meal.
- **Status**: explicitly excluded from the search [BM abstract, Method]. It is used post hoc in the discussion: noon timing, early spring, Mars visible only during the eclipse.

### Other textual indications B&M cite (supporting only, not filters)
- "Much-blossoming" woods (xiv.353).
- Long nights, fires and cloaks throughout the poem.
- At the opening, the year is drawing to a close [BM]. They give no line; Od. 1.16 is the likely referent [me]. Hesiod puts the year's end at the vernal equinox (Works and Days 560-563) [BM; SI p.1].
- S1 adds, under Constellations, a note at xi.370 that the nights are still at their longest. The line is actually 11.373 in this numbering [me].

---

## 5. Search window and its justification [BM Method]

Classical dates for the fall of Troy, as listed by B&M, in years BC:

| Source | Fall of Troy, BC |
|---|---|
| Ephorus | 1135 (-1134) |
| "Solsibus" (sic; Sosibius) | 1172 (-1171) |
| Eratosthenes | 1184 (-1183) |
| Plato | 1193 (-1192) |
| Parian chronicle | 1208 (-1207) |
| Dicaearchus | 1212 (-1211) |
| Herodotus | ≈1250 (-1249) |
| Douris | 1333 (-1332) |
| Troy VIIa destruction layer (archaeology) | ≈1190 (-1189) |

- B&M drop Douris, the outlier, and add 10 years for the wanderings. This gives a range of **1240-1125 BC** for the return.
- They extend it by 10 years each way because the dates are modern interpretations: **search window 1250-1115 BC** (-1249 to -1114). They call this the "135-year span".
- The abstract's "sack of Troy around 1192-1184 BCE" is the range Schoch and Neugebauer worked against.
- **Table S2 actually covers 1251-1100 BC** (-1250 to -1099, 152 rows), wider than the stated window [S2]. This matters: a fourth near-candidate, 1111 BC, lies inside S2 but outside the window (§10).

---

## 6. Ephemeris, software, Delta-T, clock

### 6.1 Software [BM Method]
- **Starry Night Pro, v6.0.4** (Imaginova, 2006): general planetarium software and all plots.
  - VSOP87 for the planets; Chapront's **ELP-2000/82** for the Moon.
  - ΔT follows Meeus's implementation of Stephenson & Morrison (1984), with further adjustments.
  - **ΔT for the eclipse = 27,602.7 s**.
- **EmapWin** for eclipse-track maps, custom-corrected by B&M for Espenak's latest ΔT revisions.
- **Planetary, Lunar, and Stellar Visibility (PLSV) v3.0** (Lange & Swerdlow, Alcyone 2006) for extinction and visibility. Standard magnitude-corrected parameters; minimum altitude **1° for Mercury, 2° for the Pleiades**.
- Calendar: **Julian**. Times: "local to the Greek islands". Seasonal statements refer to the 12th century BC.
- Location: Fig. 2 says only "Ithaka's latitude". No coordinates are given [BM F2].

### 6.2 Delta-T [BM Method; SI p.2, Fig. S1]

| Source of ΔT | Value |
|---|---|
| Starry Night Pro, used for the planetarium work | **27,602.7 s** |
| EmapWin track in Fig. S1 | **28,907 s** |
| Five Millennium Canon (Espenak & Meeus 2006), latest revision | **28,590 s** |

- Extrapolating ΔT before the earliest verified eclipses has errors that grow quadratically with time. For this eclipse B&M estimate **about 2-3°** of longitude, roughly the width of the track [BM intro].
- Fig. S1 caption:
  - Different ΔT models shift the track by about 1° of longitude.
  - The ΔT error for this period corresponds to about **3°** (Stephenson & Houlden 1986), **4°** (Huber's model, calibration 500 BC) or **2°** (Huber, calibration 750 BC).
  - In all cases the track runs **NE-SW**.
  - The EmapWin track is shifted **north** of the Starry Night path. On the Starry Night path, **Ithaka and Paliki lie on the northern edge of totality**.
- The planetary criteria are insensitive to ΔT at the day level. ΔT does matter for the New-Moon civil date when the conjunction falls near midnight (§7.3) [me].

### 6.3 Clock convention: my check [me]
I recomputed three Table 2 rows with a low-precision ephemeris (§14), at Ithaca 38.4°N 20.7°E with ΔT = 27,602.7 s:

| Row | Venus rise (mine / paper) | Sunrise (mine / paper) | Lead (mine / paper) |
|---|---|---|---|
| 1178 BC | 04:40:33 / 4:39:45 | 06:24:13 / 6:22:41 | 1:43:40 / 1:42:56 |
| 1250 BC | 04:44:56 / 4:45:55 | 06:48:08 / 6:49:20 | 2:03:12 / 2:03:25 |
| 1170 BC | 04:51:57 / 4:51:24 | 07:09:37 / 7:08:31 | 2:17:39 / 2:17:07 |

All times are **UT+2**. Local mean time would read about 37 min earlier. The equinox (my 1 Apr 15:12 vs B&M 3:24 p.m.) and the -12° twilight on 18 Mar (my 19:35 vs B&M 7:38 p.m.) agree to within about 13 min and 3 min in UT+2. **So B&M's "local" clock is UT+2.** The Fig. 1 eclipse time, "12:02 p.m. local time", is presumably UT+2 too. My Meeus conjunction is 16 Apr 12:20 UT+2.

---

## 7. Candidate unit, count, and the actual table

### 7.1 What the text says
- Because Day 0 is a New Moon, B&M enumerate every New Moon in 1250-1115 BC, **1684** of them, and call each date T_i [BM Method]. My Meeus count for 1 Jan 1250 BC-31 Dec 1115 BC is 1683, consistent.
- The constellation criterion leaves one, or at most two, T_i per year; the rest are discarded.
- Then the Venus (T_i-5), Mercury (T_i-34) and listed-only Equinox (T_i-11) tests are applied.
- B&M describe Table S2 as listing every year of 1250-1115 BCE with each criterion's pass or fail. Table 2 is an abridgement to the years where the Mercury criterion is nearly met [BM Intersecting].

### 7.2 What Table S2 actually contains [S2; transcription in `data/sources/bm2008-b/table_s2.tsv`]
- **152 rows, one per year, 1251-1100 BC.** Columns:

| Column | Content |
|---|---|
| Year BC | |
| T_i | |
| Venus | rise time on T_i-5, sunrise, and difference (blank if Venus is an evening star) |
| Hermes | MWRA date and Δ |
| Equinox | "Sinks T_i-11" date and a "Before" column of XXX flags |
| Moon/Const | colour of the first (year) column |

- Cell colours, extracted from the PDF fill operators [me]:

| Colour | RGB | Meaning |
|---|---|---|
| orange | (1, 0.604, 0) | "fully satisfied" |
| yellow | (0.988, 0.953, 0.02) | narrowly missed |
| light yellow | (1, 1, 0.604) | narrowly missed, slightly worse |
| white | none | "not close" |

- Per the caption, the **year column is coloured by the minimum of the Venus and Mercury colours**, not counting the Equinox [BM Intersecting; Table 2 caption].
- **There is no explicit constellation or visibility column.** The constellation criterion appears only through the choice of one T_i per year, and that choice does not strictly follow the stated window (see C1) [me].
- **Leap-year arithmetic [me]**: S2's Δ values for BC leap years (BC year ≡ 1 mod 4, e.g. 1189, 1177 and 1157 BC = -1188, -1176, -1156) match date subtraction that **ignores 29 February**. Examples: 1157 BC is -1 in S2 but 0 with leap-correct arithmetic, and the main Table 2 prints 0. 1177 BC is 3 vs 4; 1189 BC is 7 vs 8.

### 7.3 Can T_i be reproduced? [me, Meeus ch. 49, ΔT 27,602.7 s]
- 138/152 S2 dates equal the local-mean-time civil date of the conjunction. This count includes 1175 BC, whose conjunction falls at 00:00 LMT on 13 Apr.
- **13 rows are one day earlier** than that date; in all of them the conjunction falls between about 01:05 and 05:40 LMT. They are 1248, 1246, 1245, 1205, 1187, 1177, 1154, 1147, 1135, 1134, 1125, 1105 and 1101 BC.
- Other rows with conjunctions as late as about 01:35 LMT are *not* shifted. So no single time zone or day-boundary rule reproduces the column.
- **1243 BC's T_i = 13 Mar is about 2.8 days from any conjunction** (Meeus: 15 Mar 20:06 LMT). It looks like a typo, but the row's Venus, MWRA and T_i-11 entries were all computed from 13 Mar.
- For 1178 BC the S2 date agrees: conjunction 16 Apr 12:20 UT+2.

---

## 8. Survivors per clue

**As stated by B&M:**

| Criterion | B&M's statement |
|---|---|
| Constellations | 1 or 2 T_i per year |
| Venus | about 1/3 of the time |
| Mercury | sterigmos once per 116 days |
| Equinox + Pleiades (1-4/5 Apr) | one T_i every 6 years |
| All criteria as stated | one T_i, 16 Apr 1178 BC |
| Narrowly missed | two dates, discussed in SI; neither satisfies the Equinox |

[BM Intersecting; probability paragraph]

**Counted by me from Table S2 for 1250-1115 BC (136 rows)**, with all S2 rows (1251-1100 BC, 152) in brackets:

| Criterion | Rows | Years |
|---|---|---|
| Rows (one T_i per year) | 136 [152] | |
| Venus a morning star on T_i-5 (non-blank) | 67 [75] | |
| Venus lead ≥ 90 min (orange) | 21 [25] | 21/136 = 15% of all rows; 21/67 = 31% of morning rows. B&M's "about 1/3" is the conditional rate. |
| Venus lead 60-90 min (yellow) | 21 [23] | |
| Mercury \|Δ\| ≤ 1 (orange) | 4 [4] | 1236, 1224, 1178, 1157 BC |
| Mercury \|Δ\| = 2 (yellow) | 2 [3] | 1144, 1143 [+1111] |
| Mercury \|Δ\| = 3 (light yellow) | 6 | 1223, 1203, 1191, 1190, 1177, 1145 |
| Equinox flag (T_i-11 in 1-6 Apr) | 22 [26] | about one per 6.2 years |
| Venus orange AND Mercury orange | 1 | **1178** |
| Venus ≥ 60 min AND Mercury \|Δ\| ≤ 3 | 3 [4] | 1191, 1178, 1157 [+1111] |
| Mercury \|Δ\| ≤ 3 AND Equinox | 2 | 1224 (Venus fails, lead 0:32:38), 1178 |
| Venus orange AND Equinox | 4 | 1194, 1186, 1178, 1159 |
| All (Venus, Mercury, Equinox) | 1 | **1178** |

**Simple expectation under independence [me]**:
- 136 rows × 0.154 (Venus orange) × 0.029 (Mercury orange) ≈ **0.6 expected** joint Venus-and-Mercury passes. Observed: 1.
- With yellows allowed: 136 × 0.31 × 0.088 ≈ 3.7 expected; observed 3.
- So the Venus-and-Mercury coincidence alone is roughly what chance gives across the window. The rarity in B&M's argument comes from (a) adding the Equinox/Pleiades boundary, which was not applied in the search, and (b) the coincidence with the independently known eclipse date.
- This is a first-order reading of their own table, not a null model.

---

## 9. Probability / significance claim [BM, paragraph after Fig. 2; Conclusions]

**Statement (paraphrased).** Satisfying all five references this strictly is extremely rare:
- requiring the raft's sinking after the equinox (1 April) and on or before the Pleiades' heliacal setting (4 April) leaves one T_i every 6 years;
- one third of those have a high Venus;
- Mercury's sterigmos happens once every 116 days.

So an exact match happens only one day in about **2,000 years**. The Conclusions add that fictional references would be very unlikely to coincide by accident with the century's only eclipse.

**Arithmetic reconstruction [me]**: 6 yr × 3 × 116 ≈ 2,088 yr, i.e. "2,000 years".

**Assumptions implicit in it [me]**:
- (i) **Mercury is treated as an exact-day match** (1/116). The search itself accepts "within a few days"; orange is ±1 day, so the factor would be about 3/116. That makes about 700 yr; with ±3 days, about 300 yr.
- (ii) It **includes the Equinox criterion**, which the search deliberately did not apply.
- (iii) The factors are treated as independent. Equinox and Pleiades are both seasonal, which B&M acknowledge.
- (iv) There is no correction for the choice among clue readings: which turning-point variable, which reckoning, which tolerances, the 1:30 cutoff, the window extension.
- (v) There is no look-elsewhere count over other possible clue sets or other windows.
- (vi) The Venus factor of 1/3 is conditional on Venus being a morning star. The unconditional S2 rate is about 15%, which would make their estimate *more* extreme, not less.
- (vii) The window of about 136 years was centred on Troy-fall dates that also motivated Schoch's eclipse, so the only-eclipse-of-the-century framing and the search window are not independent of the eclipse.
- B&M report no formal p-value, null model or Monte Carlo.

---

## 10. Dates that pass [BM; SI p.1 "Runner-Up Dates"; S2]

| Date (Julian) | Astronomical | Status | Details |
|---|---|---|---|
| **16 April 1178 BC** | -1177-04-16 | All criteria, including the listed Equinox | Venus lead 1:42:56; MWRA 13 Mar, Δ 0; T_i-11 = 5 Apr; equinox 1 Apr. B&M say it holds under both reckonings and exactly under sequential. |
| 24 March 1157 BC | -1156-03-24 | Runner-up (yellow) | Mercury fully satisfied (MWRA 19 Feb; Δ -1 in S2, 0 in T2). Venus lead 1:25:12, just under the 1:30 cutoff. Fails Equinox: T_i-11 = 13 Mar. Sailing would start in late February and the killing would fall more than a week before the equinox [SI p.1]. My MWRA for 1157 is 22 Feb, which would give Δ = -3 [me]. |
| 9 April 1191 BC | -1190-04-09 | Weaker runner-up (light yellow) | Venus lead 1:06:29; Mercury missed by 3 days (MWRA 9 Mar). Sinking 29 Mar, near but before the equinox [SI p.1]. |
| 26 March 1111 BC | -1110-03-26 | Yellow in S2, **outside the stated window**, not discussed | Venus 1:37:29 (orange); MWRA 22 Feb, Δ -2 (yellow); T_i-11 = 15 Mar [S2; me]. |
| 14 April 1224 BC | -1223-04-14 | Not a candidate | Mercury Δ 0 and Equinox 3 Apr both orange, but Venus lead only 0:32:38 [S2]. |

Under the **parallel** reckoning I estimate for 1178 BC [me]:
- Mercury T_i-33 = 14 Mar, Δ = +1;
- Venus on 12 Apr, lead 1 h 43 m (my ephemeris: 102.7 min vs 103.7 min on 11 Apr);
- sinking T_i-10 = **6 Apr**, which is outside the main text's "≤ 5 April" and one night past the stated Pleiades last visibility.

So "both chronologies" holds only with a one-day tolerance on the Equinox/Pleiades bound.

---

## 11. Reported circumstances for 16 April 1178 BC (-1177) [BM F1, Intersecting; SI Fig. S1]

| Day | Date (1178 BC) | Event |
|---|---|---|
| T_i-34 | 13 Mar | Mercury at westernmost rise azimuth (12-13 Mar) and heliacal rising (13 Mar) |
| T_i-29 | 18 Mar | New Moon; departure; at nautical twilight (7:38 p.m.) Pleiades astern, Boötes ahead-left, Ursa Major due north (Fig. 2) |
| | 1 Apr | Vernal equinox, 3:24 p.m. |
| | 4 Apr (night) | Last visibility of the Pleiades (heliacal setting); invisible for about 40 days |
| T_i-11 | 5 Apr | Raft sunk |
| T_i-5 | 11 Apr | Phaeacians reach Ithaca; Venus rose 1 h 43 min before sunrise, mag -4.2 |
| T_i | 16 Apr | Total solar eclipse over the Ionian Islands, 12:02 p.m. local, Fig. 1 (= UT+2 per §6.3) |

**The eclipse** [BM F1; abstract; Historical Plausibility]:
- **The 31st eclipse of Saros 39.**
- **All five naked-eye planets visible together** within less than 90° of ecliptic. Fig. 1 magnitudes: Venus -4, Jupiter -1.9, Mercury -1.2, Saturn 0.16, Mars 1.3.
- The hidden Sun was "crowned" by the Pleiades.
- **Greatest eclipse at 32.7°N 12.7°E**, about 50 km WSW of Tripoli, 33° due west of Babylon.
- Mars was not visible in March/April 1178 BC except during the eclipse.
- The eclipse fell at noon, as Schoch had pointed out.
- Totality is extremely rare at any one place: about once in 370 years.
- Track NE-SW (Fig. S1). On Starry Night's path Ithaka and Paliki lie on the northern edge of totality; EmapWin shifts the track north.

---

## 12. History B&M cite: eclipse identifications

1. **Ancient allegorists** [BM intro]:
   - **Plutarch** suggested Od. 20.356-357 describes a total solar eclipse: *De facie* §19, ps.-Plutarch *De vita et poesi Homeri* §108; *Pelopidas* cited as Plutarch's own eclipse descriptions.
   - **Heraclitus the Allegorist** (*Quaestiones Homericae* §75) developed the same reading.
   - Both note the references to the day being New Moon.
   - Local verification [me]:
     - Plutarch *De facie* 19 (`data/text/plutarch-defacie-grc.tsv`, section 19.1) cites Homer's faces covered in night and the Sun perished from heaven, and ties it to the "waning month / rising month" line. In the same section he describes a recent noon eclipse with stars visible.
     - Heraclitus (`data/text/heraclitus-allegoriae-grc.tsv`) has the eclipse allegory, with a lacuna, at **ch. 73.1-73.2 of the 1st1K edition** (B&M's §75 follows a different numbering). It mentions Hipparchus, the "old-and-new" day (ἕνη καὶ νέα), Theoclymenus, and the waning/rising-month line.
2. **Objections** B&M summarise:
   - no explicit eclipse elsewhere in the poem;
   - the scene is indoors and nobody else reacts;
   - the darkness fits Hades imagery;
   - some (Page 1955) consider the lines suspect;
   - most translations carry no eclipse footnote at xx.356.
3. **Specific historical eclipse**:
   - Fotheringham (1921), Halley Lecture, cited in general for specific-eclipse identifications.
   - **Schoch (1926)**: *The Observatory* 49:19-21, "The eclipse of Odysseus"; *Die Sterne* 6:88; *Die sechs griechischen Dichter-Finsternisse* (Berlin-Steglitz, self-published).
   - **P.V. Neugebauer (1929)**: *Astronomische Chronologie*.
   - Per B&M's abstract, Schoch and Neugebauer computed that the eclipse of **16 April 1178 BCE was total over the Ionian Islands**, and that it was the only suitable eclipse in over a century to match the classical Troy dates of about 1192-1184 BCE. They also noted the noon timing.
   - **I did not read Schoch or P.V. Neugebauer; their eclipse parameters (secular acceleration or ΔT used, path, local time) are therefore unknown to me beyond B&M's report.**
   - Do not confuse this Neugebauer with **Otto Neugebauer** (*HAMA* 1975), whom B&M cite separately on Thales.
4. **Cycles discussion** [BM Historical Plausibility; SI Fig. S2]:
   - **One exeligmos later** (three Saros cycles), on **18 May 1124 BC** (-1123), the track of totality passed almost over **Babylon**; greatest eclipse 32.9°N 45.3°E, about 90 km ENE of Babylon.
   - **Thales**: the eclipse of **28 May 585 BC** (-584). One Saros earlier, on **18 May 603 BC** (-602), the central line passed about 220 km SE of Ur. Half a Saros earlier, on **23 May 594 BC** (-593), there was a total lunar eclipse visible from Greece and Mesopotamia.
   - B&M argue that Otto Neugebauer's objection (no manageable local cycle) has two loopholes: two sites, and intercalated lunar eclipses. They explicitly do not claim this is how the poet learned of the 1178 eclipse.
5. **Metonic and lunar allegory** [BM; SI p.1]:
   - Murray (1924) and Campbell (1964): Day 0 as the end of a Metonic cycle; the 19 years of absence; the shroud and the bow as lunar allegories.
   - B&M add that Odysseus' spreading of his sails on Day -29 is a first-crescent allegory. The SI instead ties the sail-spreading to the previous **full** moon, which contradicts the main text's **New** Moon on 18 March [me].
   - SI speculation:
     - an "almost-arrival" (the bag of winds) on **14 April 1186 BC** (-1185), via a 99-lunation sub-cycle;
     - an allegorical fall of Troy half a Metonic cycle earlier, on **15 October 1188 BC** (-1187), with a total lunar eclipse partially visible from Troy at dawn.
6. **Season**:
   - MacDonald (1967, *J. Br. Astron. Assoc.* 77:324-328) argued for March sailing and suggested the Poseidon-equinox link.
   - Hesiod *Works and Days* is used for the agricultural star calendar: Arcturus 60 days after the solstice; the Pleiades hidden 40 days; gales when the Pleiades set [SI p.1].
   - de Santillana & von Dechend (1969, *Hamlet's Mill*) is cited for the idea of two significant divine voyages.

---

## 13. Reproduction hazards and internal inconsistencies (collected)

1. **Pleiades last visibility**: given as 3 April, 4 April and 5 April (BM References / probability paragraph and 1178 narrative / SI p.1). 1178 BC lies on this boundary.
2. **Arcturus achronical rising**: 17 Feb (main text) vs "end of February" (SI p.1).
3. **Equinox window**: "1 Apr ≤ T_i-11 ≤ 5 Apr" (text) vs "≤ 4 Apr" (probability paragraph) vs S2 flags reaching 6 Apr. Table 2 colours 30-Mar light yellow; S2 does not.
4. **Mercury tolerance** is never stated in the text. Colour levels decoded from S2: ±1 / 2 / 3 days.
5. **MWRA** is undefined in the paper. It decodes as the maximum rising azimuth from north, i.e. the southernmost rising point [me]. It is flat-topped, so ±1-2 days is intrinsic.
6. **Mercury visibility** is required by the text but not tabulated.
7. **Venus "high"** means rise-time lead ≥ 1:30 only. Altitude and magnitude are not tested.
8. **Hermes' day**: 13 Mar (text) vs 15 Mar (S1 note to v.225).
9. **Night -2 = xiv.457** contradicts Table 1, where xiv.457 falls on Day -5 (sequential).
10. **"Previous full moon"** (SI) vs New Moon on 18 Mar (main text).
11. **One T_i per year in S2.** Seven years with a second qualifying New Moon are not evaluated; one of them is 18 Mar 1178 BC. 1243 BC's T_i is not a New Moon.
12. **S2 Δ arithmetic ignores BC leap days**: 1157 BC is -1 in S2 vs 0 in Table 2.
13. **S2 spans 1251-1100 BC, not 1250-1115 BC.** It shows an undiscussed yellow candidate in 1111 BC.
14. **Day convention for T_i** is unreproducible as a conjunction date in any single time zone. 13 rows are one day early relative to LMT; 1243 BC is off by about 2.8 d.
15. **Parallel reckoning** breaks the ≤ 5 Apr sinking bound for 1178 by one day.
16. **The probability estimate** uses an exact-day Mercury match and the unapplied Equinox criterion (§9).

---

## 14. My independent checks: tools and status

All are in `results/bm2008-b-checks/`: `run_checks.py`, output in `run_checks.out.txt`.

| Tool | Basis | Accuracy / settings |
|---|---|---|
| `ephem.py` | Standish (JPL) Keplerian elements, Table 2a (3000 BC-3000 AD), J2000 ecliptic; IAU 1976 precession (Meeus ch. 21); GMST (Meeus 12.4) | No nutation or aberration. ΔT fixed at B&M's 27,602.7 s. Site 38.4°N, 20.7°E. Rise defined at h0 = -0.5667° (planets) and -0.8333° (Sun). Arcminute-level accuracy, enough for day-level extrema. |
| `newmoon.py` | Meeus ch. 49 New-Moon algorithm | Times in TT, converted with the same ΔT |

These checks are low-precision and only test consistency with B&M's tables. **They are not a reproduction with VSOP87/ELP, a modern ΔT model, or PLSV visibility.**

---

## Sources
- Baikouzis C., Magnasco M.O. (2008) PNAS 105(26):8823-8828, doi:10.1073/pnas.0803317105.
  - Full-text HTML: https://pmc.ncbi.nlm.nih.gov/articles/PMC2440358/
  - Article PDF (SEDICI deposit): https://sedici.unlp.edu.ar/bitstream/handle/10915/82991/Documento_completo.1073_pnas.0803317105.pdf
  - Table 2 image: https://cdn.ncbi.nlm.nih.gov/pmc/blobs/d042/2449324/99ba8f68282c/zpq999083528st02.jpg
- Supporting Information PDF: http://web.archive.org/web/20210223135650/https://www.pnas.org/content/suppl/2008/06/24/0803317105.DCSupplemental/0803317105SI.pdf
- Odyssey Greek text (Perseus): `data/text/odyssey-grc.tsv`. Iliad 18.485-489: `data/text/iliad-grc.tsv`.
- Plutarch *De facie* 19: `data/text/plutarch-defacie-grc.tsv`. Heraclitus *Allegoriae* 73: `data/text/heraclitus-allegoriae-grc.tsv`.
- Meeus J., *Astronomical Algorithms*, 2nd ed., ch. 7, 12, 21, 49; Standish E.M., "Keplerian Elements for Approximate Positions of the Major Planets" (JPL), Table 2a. Both were used from memory in code. The Venus-time match in §6.3 validates them to about 1-2 min.
- Not read (reported via B&M only): Schoch 1926 (Observatory 49:19-21; Die Sterne 6:88; Dichter-Finsternisse); P.V. Neugebauer 1929; MacDonald 1967; Murray 1924; Fotheringham 1921; Espenak & Meeus 2006.
