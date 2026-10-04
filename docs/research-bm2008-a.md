# Baikouzis & Magnasco (2008): reproduction-grade extraction (agent a)

Target: Baikouzis C., Magnasco M. O. (2008), *Is an eclipse described in the Odyssey?*, PNAS 105(26):8823-8828, doi:10.1073/pnas.0803317105 (received 2 July 2007, communicated 7 April 2008, issue of 1 July 2008). Abbreviated **B&M** below.

Status: **primary paper read in full (PDF + PMC HTML), Supporting Information read in full (7-page PDF), Schoch 1926 read in full from the ADS scan.** P. V. Neugebauer 1929 was **not** read (see section 10).

Conventions in this document. "BC" years are historical; astronomical year = 1 - BC (1178 BC = -1177). All calendar dates are proleptic Julian unless stated otherwise. Each claim is tagged: **[B&M p./section]** = the paper; **[SI ...]** = the Supporting Information; **[Schoch 1926]** = The Observatory 49:19-21; **[me: tool]** = computed or inferred by me. Text inside [me] tags is my inference, not the authors' claim.

---

## 1. Sources and how they were obtained

| Item | Where it came from | Status |
|---|---|---|
| Main article, HTML full text | https://pmc.ncbi.nlm.nih.gov/articles/PMC2440358/ (PMC ID resolved from the DOI through the NCBI ID converter). **PMC2440355 is NOT this paper**: it is a PLoS One HIV article. | read; saved as `data/bm2008-a/bm2008-pmc-fulltext.txt` |
| Main article, PDF (PNAS print layout, pp. 8823-8828) | Wayback Machine capture 2017-10-31 of `http://www.pnas.org/content/105/26/8823.full.pdf` (`web.archive.org/web/20171031123340id_/...`). Direct pnas.org and Europe PMC returned 403. The PMC PDF link is behind a proof-of-work bot check, which I did not try to get around. | read; `data/bm2008-a/baikouzis-magnasco-2008-pnas.pdf` (474,695 bytes) |
| Supporting Information PDF (7 pp.: SI Discussion, Figs. S1-S2, Tables S1-S2) | Wayback capture 2021-02-23 of `https://www.pnas.org/content/suppl/2008/06/24/0803317105.DCSupplemental/0803317105SI.pdf`. The 2008 Wayback capture of `/cgi/data/0803317105/DCSupplemental/Supplemental_PDF` is **truncated** (129 KB, broken xref), so don't use it. | read; `data/bm2008-a/baikouzis-magnasco-2008-SI.pdf` (1,135,988 bytes; PDF metadata ModDate 2008-06-24) |
| Table 2 (abridged search table) | PMC figure image `zpq999083528st02.jpg`. The column headers come from the PDF text layer. | read; `data/bm2008-a/bm2008-table2-pmc.jpg` |
| Table S2 (full search table) | Rebuilt by me from the SI PDF text layer (pypdf text positions), with cell **fill colours read from the PDF content stream**. `pdftotext -layout` scrambles this table (it attaches values to the wrong years), so **do not use a plain text dump of it**. | `data/bm2008-a/table_s2.tsv`, 152 rows, 1251-1100 BC |
| Schoch C. (1926), The eclipse of Odysseus, *The Observatory* 49:19-21 (bibcode 1926Obs....49...19S) | ADS PDF (JBIG2 scan), rendered with the Windows.Data.Pdf API | read; `data/bm2008-a/schoch-1926-observatory-49-19.pdf` |

Odyssey line numbers below were checked against `data/text/odyssey-grc.tsv` (Perseus Greek) [me: grep].

---

## 2. The claim and what is disclaimed

**What they claim** [B&M abstract; *Intersecting the Constraints*; *Conclusions*]:
- They take three "overt" astronomical references (Boötes and the Pleiades; Venus; the New Moon) plus one "conjectural" one (Hermes' trip to Ogygia read as the planet Mercury). Searching every new moon in 1250-1115 BC, they find a **single date that satisfies all of them: 16 April 1178 BC** (-1177), which is also the date of the total solar eclipse that Schoch identified.
- They say the clues hang together: two different sets of verses point to the same date independently, with a very low chance probability. They state that the references can be matched exactly only **one day every 2,000 years** (section 8).
- They say the odds that purely fictional references would coincide by accident with **the only eclipse of the century** are minute.
- Post hoc, they suggest these references, together with the disputed eclipse passage, may be the work of one hand ("Homer"), may refer to the historical eclipse, and may form a structural timeline for the poem.

**What they disclaim** [B&M Introduction caveats; *Historical Plausibility*; *Conclusions*]:
- The eclipse is **not used as a clue**. The analysis is done explicitly without assuming an eclipse, because the Theoclymenus lines are suspect. (But Day 0 = New Moon is used, and a new moon is a necessary condition for a solar eclipse [me].)
- If their reading of the passages as astronomical phenomena is wrong, the dates and probabilities are wrong too; the whole calculation would then be a non sequitur.
- Even if the reading is right, it says nothing about whether the narrated events happened. A historical Odysseus and an allegorical timeline are equally compatible.
- The Hermes = Mercury identification is conjectural. The first surviving Hermes-Mercury link is in Plato's *Timaeus*, so their reading would require moving that association about two centuries earlier.
- The Poseidon = equinox reading is much more conjectural and is **not applied** as a selection criterion. It is only listed for confirmation.
- They say the case is still a long way from proof. They do not endorse any particular way the Poet could have known about the eclipse (the Babylon exeligmos idea is offered only as a possibility).
- Dates of first and last visibility are psychophysical, so each should be taken as uncertain by at least a day [B&M *Method*].

---

## 3. Conventions, software, ephemeris and Delta-T

**Stated** [B&M *Method*, bracketed software note; SI Fig. S1 caption]:
- Calendar: all dates Julian (proleptic for these years). Times are given as local time for the Greek islands. Seasonal references are for the 12th century BC.
- Planetarium: **Starry Night Pro 6.0.4** (Imaginova 2006, ref. 31). It uses VSOP87 for the planets and Chapront's ELP-2000/82 for the Moon, and computes Delta-T after Meeus, following Stephenson & Morrison (1984), plus further adjustments. **Delta-T for the eclipse in Starry Night is 27,602.7 s.**
- Eclipse maps: **EmapWin**, custom-corrected for the latest Delta-T revisions from Espenak (ref. 2). The track in Fig. S1 uses **Delta-T = 28,907 s**. The SI notes that the Five Millennium Canon lists **28,590 s** for this eclipse [SI Fig. S1].
- Visibility: **Planetary, Lunar, and Stellar Visibility 3.0** (Lange & Swerdlow, Alcyone 2006, ref. 32). They used its standard magnitude-corrected parameters with a **minimum altitude of 1 deg for Mercury and 2 deg for the Pleiades**.
- Delta-T uncertainty: the error from extrapolating Delta-T is about 2-3 deg of longitude, roughly the width of the totality track [B&M Introduction]. The SI gives about 3 deg (Stephenson & Houlden 1986), 4 deg (Huber's model, calibrated at 500 BC) and 2 deg (Huber, calibrated at 750 BC); in all cases the track runs NE-SW. Different Delta-T models move the track by about 1 deg of longitude. Delta-T is extrapolated from the mean parabola, without short-term fluctuations [SI Fig. S1].
- Delta-T matters only for the eclipse track. The clue tests (rising times, azimuths, visibility) depend on Delta-T only through local times, which Starry Night computed with its own Delta-T [me].

**Inferred time zone** [me: Python, Meeus low-precision Sun, 75 rows of Table S2]:
- The Table S2 "sunrise" column equals my computed UT sunrise **+2.000 h** (sd 1.6 min) for a site at 20.7 deg E. Latitudes from 37 to 39 deg N fit equally well, so the dates near the equinox don't pin down latitude.
- So the tabulated "local" times are **zone time UT+2 (EET)**, not local mean or apparent solar time.
- On this reading, the eclipse time "12:02 p.m. local" [B&M Fig. 1] is about 10:02 UT, or about 11:25 LMT at 20.7 deg E (using Starry Night's Delta-T). Schoch gives 11:41 LMT (section 10).
- Fig. 2 is stated to use Ithaka's latitude [B&M Fig. 2 caption].

---

## 4. Narrative chronology and day offsets (B&M Table 1)

B&M number the slaughter day as **Day 0**. Two numberings are kept [B&M Table 1 and its footnote]:
- **sequential (consecutive)**: events narrated one after another are counted on separate days;
- **parallel**: simultaneous events are not double-counted (e.g. Athena reaches Sparta instantly).

**The search uses the sequential offsets.** 1178 BC is said to satisfy the criteria under both numberings, and "exactly" under the sequential one [B&M *Intersecting*].

| Day (seq) | Day (par) | Event [B&M Table 1] | Lines [B&M] |
|---|---|---|---|
| -40 | -33 | Council of the gods; Poseidon among the Ethiopians; Athena goes to Telemachus | (book 1) |
| -39 | -32 | Ithaca assembly; Telemachus leaves for Pylos | |
| **-34** | -33 | Council of the gods; Zeus sends **Hermes to Ogygia**; Calypso tells Odysseus he may go | v.1-v.261 |
| -33 to -30 | -32 to -29 | Odysseus builds his raft | v.262 |
| **-29** | -28 | Calypso sends him off **at sunset**; he watches the **Pleiades and Boötes**, Bear on his left | v.263-v.278 |
| -28 to -12 | -27 to -11 | sailing (17 days) | v.279 |
| **-11** | -10 | Poseidon, back from the Ethiopians, sees him and **sinks the raft** | v.280-v.387 |
| -10 | -9 | swimming | v.388-389 |
| -9 | -8 | lands in Phaeacia, sleeps in leaves | v.390-493 |
| -8 | -7 | meets Nausicaa; goes to Alcinous | vi.1-vii.347 |
| -7 | -6 | Alcinous' palace; games; tells his story | viii.1-xiii.16 |
| -6 | -5 | gifts; boards ship at sunset | xiii.17-92 |
| **-5** | -4 | **reaches Ithaca with the Star of Dawn**; Athena; dines with Eumaeus | xiii.93-xiv.533 |
| -4 | -4 | Athena fetches Telemachus; he sleeps at Pherae | xv.1-190 |
| -3 | -3 | Telemachus travels; Odysseus dines with Eumaeus | xv.191-493 |
| -2 | -2 | Telemachus reaches Ithaca at dawn; meets Odysseus | xvi.1-478 |
| -1 | -1 | Odysseus enters his hall; Argos; Penelope; Eurycleia | xvii.1-xx.54/90 |
| **0** | 0 | Festival of Apollo; eclipse; death of the suitors; meets Penelope | xx.91-xxiii.344 |
| 1 | 1 | Laertes; battle; Athena stops it | xxiii.345- |

**How the offsets come from the text** [B&M Table 1, its note, and my line checks in `odyssey-grc.tsv`]:
- **-34 to -29:** the raft is finished on the fourth day (Od. 5.262) and Calypso sends him off on the fifth (5.263).
- **-29 to -11:** he sails 17 days (5.278), and the Phaeacian mountains appear on the 18th (5.279), when Poseidon sees him (5.282-283).
- **-11 to -9:** two nights and two days in the water (5.388), then land on the third day (5.390).
- **Total at sea:** B&M note he leaves near sunset and lands before sunset, so he is at sea exactly 20 days and 20 nights.
- **-6 to -5:** he boards at sunset on Day -6 and reaches Ithaca before dawn on Day -5 (13.93-95).
- **Ti and Day 0:** the search date **Ti is identified with Day 0**, the date of the new moon (conjunction) [B&M *Method*].

---

## 5. The clues: lines, interpretation, numerical criterion, offset

Throughout, **Ti** is the date of the candidate new moon (Day 0), and "Ti - n" means n days before it.

### Clue N: New Moon on Day 0 (search unit)
- **Lines.**
  - Od. 14.161-162 (to Eumaeus) and 19.306-307 (to Penelope): Odysseus will come "as one moon wanes and the next begins".
  - 14.457: a dark, moonless night (σκοτομήνιος) [B&M *Method*; SI Table S1].
  - Day 0 is also the festival of Apollo. B&M say this is stated several times, without line numbers; I find it at 20.155-156, 20.276-278 and 21.258-259 [me].
- **Interpretation.** Day 0 is a new moon, so only new moons are searched [B&M *References and Constraints*]. Murray's Metonic-cycle reading is mentioned as background, not used as a criterion [B&M; SI *Metonic Cycles*].
- **Criterion.** Ti = date of a new moon. Table S2's Ti matches my own conjunction dates in UT+2 for 137 of 152 rows (my check: Meeus ch. 49 algorithm, Delta-T 27,602.7 s). The 15 disagreements are listed in section 11.
- **Offset.** 0.
- **Inconsistency.** B&M call 14.457 "Night -2", but their own Table 1 puts xiii.93-xiv.533 on Day -5 (sequential) / -4 (parallel) [me].

### Clue C: Pleiades, late-setting Boötes, the Bear (season of departure)
- **Lines.** Od. 5.270-277, checked: 5.272 has the Pleiades and "late-setting Boötes" (ὀψὲ δύοντα Βοώτην), 5.273-275 the Bear, 5.276-277 the Bear kept on the left. B&M note that Il. 18.485ff repeats some of these lines [B&M *Method*; SI Table S1].
- **Interpretation** [B&M *References and Constraints*]:
  - The Bear is circumpolar; keeping it on the left means he sails east.
  - The Pleiades and Boötes are far apart in the sky. Both are visible together after twilight in two seasons:
    - around **March**: the Pleiades set early and Boötes sets late;
    - around **September**: the reverse.
  - The text calls Boötes late-setting, so B&M choose **March**, following MacDonald (1967, ref. 34).
  - The star that stands for Boötes is **Arcturus**: the SI and the MacDonald quote speak of Arcturus. B&M do not say which object stands for the Pleiades (presumably the cluster as handled by the visibility program) [me].
- **Numerical criterion** [B&M *References and Constraints*]:
  - Reference event: **nautical twilight, Sun at -12 deg**.
  - Earliest date Boötes is visible (its apparent achronical rising): **17 February**.
  - Latest night the Pleiades are visible: **3 April**.
  - Requirement: the departure date and the whole 17-day sailing period must fall within 17 Feb to 4 Apr. Operationally, **Ti - 29 >= 17 Feb and Ti - 12 <= 4 Apr** (equivalently Ti - 11 <= 5 Apr), so Ti lies in **18 Mar to 16 Apr** in a common year [me: arithmetic].
  - The same fixed Julian dates are used for every year.
  - One, or at most two, new moons per year pass; the others are discarded.
- **Offsets.** Ti - 29 (departure) through Ti - 12 (last night of sailing).
- **Supporting remarks** (not criteria) [B&M; SI]:
  - Long nights and fires throughout the poem. The SI cites xi.370; in the Greek text it is 11.373 [me].
  - "Much-blossoming" trees at 14.353.
  - The year is said to be ending at the start of the poem. B&M give no line; possibly 1.16 [me].
  - Hesiod (*Works and Days*) has the year ending at the vernal equinox, and links the Pleiades' setting to gales.

### Clue V: Venus before dawn on arrival at Ithaca
- **Lines.** Od. 13.93-95: the brightest star, the one that heralds the dawn, has risen when the ship reaches the island. B&M cite xiii.93-96 [B&M *Method*; SI Table S1].
- **Interpretation.** The star is Venus as morning star. B&M infer it rose well before dawn because much happens before daybreak: landing, Odysseus asleep, the talk with Athena, the hiding of the treasure [B&M *References and Constraints*].
- **Numerical criterion.** On **Ti - 5**, Venus must rise **at least 90 min before the Sun** (rising times from Starry Night; the location fits about 20.7 deg E at UT+2 [me]). B&M add that in this season Venus rises at most about 2 h before sunrise.
  - This compares rising times only. It is not an arcus-visionis visibility test [me].
  - Blank Table S2 cells mean Venus was an evening star on Ti - 5.
- **Colour thresholds in Table S2** [me: fill colours from the PDF]:
  - orange (pass): Venus lead >= 1:30:00. Smallest orange value 1:32:08; largest non-orange 1:29:06.
  - yellow (near miss): from about 1:00 to 1:30. Smallest yellow value 1:02:26; largest white 0:58:25.
  - white: below about 1:00.
  - The SI confirms the cutoff: it describes 1157 BC as falling just below the 1:30 cutoff [SI *Runner-Up Dates*].
- **Claimed rate.** About **1/3** of the time [B&M]. In Table S2 (1250-1115 BC) it passes in **21 of 136** years (15%). That is **21 of the 67** years in which Venus is a morning star on Ti - 5, i.e. 31%, so B&M's 1/3 matches the rate *given* a morning-star Venus, not the overall rate [me].
- **Offset.** Ti - 5 (sequential; Ti - 4 parallel).

### Clue M: Hermes' journey to Ogygia read as Mercury at a turning point (conjectural)
- **Lines.** Od. 5.43-58 (the flight low over the waves; B&M "v.48 onwards"), 5.55 (arrival at the far-off island) and 5.97-103 (Hermes complains about the long trip). SI Table S1 also quotes **5.225** (sunset on the day of the visit) [B&M *Method*, *Historical Plausibility*; SI Table S1].
- **Interpretation.** Hermes travels far west, delivers his message and returns east at once: an allegory of a planetary turning point (station, *sterigmos*), the term used on the Antikythera mechanism (ref. 38).
- **Numerical criterion as stated.** On **Ti - 34**, Mercury must be on the western side of its path, **visible**, and close to a turning point [B&M *References and Constraints*].
  - B&M discuss three candidate variables: elongation from the Sun; the azimuth of its rising point, at its westernmost; and the start of retrograde motion. They say these are close together in time.
  - The test actually used: Ti - 34 must fall **within a few days of Mercury's westernmost rising azimuth**.
  - Table 2 / S2 column "MWRA" (maximum western rise azimuth) gives the date of the nearest such maximum to Ti - 34.
- **Operational criterion in Table S2** [me: reconstruction]:
  - Δ = (Ti - 34) - MWRA date, in days.
  - Colours: |Δ| <= 1 orange (pass), |Δ| = 2 yellow, |Δ| = 3 pale yellow, |Δ| >= 4 white.
- **Visibility.** The "visible" requirement is not represented in Table S2. Visibility is reported only for 1178 BC [me].
- **1178 BC values** [B&M *Intersecting*]:
  - Ti - 34 = 13 Mar.
  - The westernmost rising azimuth falls on 12 and 13 Mar.
  - 13 Mar is Mercury's **heliacal rising** (first morning visibility; Alcyone PLSV standard parameters, Mercury minimum altitude 1 deg). Mercury was not visible on 12 Mar.
- **Claimed rate.** A station occurs once per 116 days, Mercury's synodic period [B&M].
- **Ambiguity** [me]:
  - The rising azimuth of a rising body is always in the east, so "maximum western rise azimuth" has no unambiguous numerical definition.
  - Possible readings: the azimuth extreme of the rising point, a station in ecliptic longitude, or greatest western elongation. These can fall about 1-2 weeks apart.
  - A heliacal rising on 13 Mar suggests Mercury was just past inferior conjunction, i.e. near its retrograde-to-direct station rather than at greatest western elongation.
  - The bench should test each reading.
- **Offset.** Ti - 34 (sequential; Ti - 33 parallel).

### Clue E: Poseidon back from the Ethiopians read as the equinox (NOT applied)
- **Lines.** Od. 5.282-283 (and Poseidon among the Ethiopians at the start, Table 1 Day -40) [B&M; SI Table S1].
- **Interpretation.** MacDonald's suggestion that the Earth-shaker's return from the south marks the vernal equinox. B&M treat it as too conjectural to apply and list it only for confirmation [B&M *References and Constraints*].
- **Criterion if applied.** **1 Apr <= Ti - 11 <= 5 Apr** [B&M]. The probability paragraph instead bounds the sinking between the equinox (1 April) and, inclusively, the heliacal setting of the Pleiades **(4 April)**. Under that wording **1178 BC itself fails**, since its Ti - 11 is 5 Apr [me].
- **Table S2.** Column "Before" is marked XXX **exactly** when Ti - 11 >= 1 Apr (152 of 152 rows) [me].
- **1178 BC.** Equinox on 1 April at 3:24 p.m.; sinking on 5 April [B&M].
- **Offset.** Ti - 11 (sequential; Ti - 10 parallel).

### Clue X: the eclipse itself (NOT used)
- **Lines.** Od. 20.345-357, especially 20.356-357: the sun has perished from the sky and an evil mist has come over it (ἠέλιος δὲ οὐρανοῦ ἐξαπόλωλε, κακὴ δ' ἐπιδέδρομεν ἀχλύς). B&M cite it as xx.356.
- **Use.** Explicitly excluded as a clue [B&M Introduction].
- **Post hoc.** B&M later offer as additional support [B&M *Intersecting*]:
  - Ares is absent from the main story, and Mars was invisible in March-April 1178 except during the eclipse;
  - the eclipse fell at noon, as Schoch noted, matching the story's midday meal;
  - early spring fits the story.

---

## 6. Search window and enumeration

**Window** [B&M *Method*]:
- Classical dates for the fall of Troy (BC): Ephorus 1135; "Solsibus" [sic] 1172; Eratosthenes 1184; Plato 1193; Parian Marble 1208; Dicaearchus 1212; Herodotus about 1250; Douris 1333. Troy VIIa's destruction is dated to about 1190.
- Leaving out Douris gives **1240-1125 BC** for Odysseus' return, which they widen by 10 years each way to **1250-1115 BC**.
- They call it a 135-year span; inclusive, it is 136 years [me].

**Unit enumerated** [B&M *Method*]:
- **All 1684 new moons in 1250-1115 BC.** My Meeus count for 1 Jan 1250 BC to 31 Dec 1115 BC (UT+2) is 1683 [me].
- The constellation criterion keeps one, or at most two, per year.

**Table S2 as published** [SI Table S2; me: transcription]:
- One Ti per year, **1251 BC to 1100 BC (152 rows)**. That is wider than the stated search window.
- The Ti dates run from 13 Mar to 17 Apr.
- Three rows break the 18 Mar - 16 Apr rule: 1246 BC (17 Apr), 1227 BC (17 Apr), and 1243 BC (13 Mar, also two days off my computed conjunction).
- Columns: Year BC | Ti | Venus rise on Ti-5 | sunrise | difference | MWRA | Δ | Ti-11 ("Sinks") | "Before" (XXX).
- Table 2 in the paper is a 28-row extract (years where the Mercury criterion is close); its values agree with Table S2 except as noted in section 11.

---

## 7. Survivors by clue, alone and combined

B&M state only the final result: **one date**, 16 Apr 1178 BC, in 1250-1115 BC; two near misses are discussed in the SI. All counts below are **[me: Python over the transcribed Table S2, using the authors' printed values and thresholds]**.

**Stated window, 1250-1115 BC (136 rows, one Ti per year):**

| Criterion | Rows passing | Years |
|---|---|---|
| N + C (one Ti per year listed) | 136; 133 strictly inside 18 Mar - 16 Apr | |
| V: Venus lead >= 1:30 | **21** (another 21 yellow at 1:00-1:30; 69 evening-star blanks) | |
| M: \|Δ\| <= 1 | **4** | 1236, 1224, 1178, 1157 |
| M: \|Δ\| <= 2 | 6 | adds 1144, 1143 |
| M: \|Δ\| <= 3 | 12 | |
| E: 1 Apr <= Ti-11 <= 5 Apr | 20 (17 if <= 4 Apr) | |
| **V and M (\|Δ\| <= 1)** | **1** | **1178** |
| V and M (\|Δ\| <= 3) | 1 | 1178 |
| V and E | 4 | 1194, 1186, 1178, 1159 |
| M and E | 2 | 1224, 1178 |
| V and M and E | 1 | 1178 |

**Near misses** [SI *Runner-Up Dates*; colours me]:
- **24 Mar 1157 BC** (-1156):
  - Venus 1:25:12 (just under 1:30). Mercury Δ = 0 in Table 2, -1 in Table S2; the true value is 0 (section 11).
  - Ti - 11 = 13 Mar, so it fails the equinox reading.
  - The SI calls it early (departure in late February; suitors killed more than a week before the equinox) but an otherwise very good match to the first four references.
- **9 Apr 1191 BC** (-1190):
  - Venus 1:06:29; Mercury missed by 3 days; Ti - 11 = 29 Mar.
  - The SI calls it a weaker candidate.
- **Year-cell colours in Table S2** (minimum of the Venus and Mercury colours): 1178 orange; 1157 yellow; **1111 yellow**; 1191 pale yellow.

**Full Table S2, 1251-1100 BC (152 rows):**
- V passes 25 rows; M (|Δ| <= 1) passes 4 (the same four years).
- V and M (|Δ| <= 2): **1178 and 1111 BC.**
- **26 Mar 1111 BC** (-1110): Venus 1:37:29 (passes), Mercury Δ = -2 (near miss), Ti - 11 = 15 Mar. It is outside the stated window; the authors coloured it yellow but do not mention it in the text.

---

## 8. Probability and significance claim

**The claim** [B&M *Intersecting the Constraints*]:
- Requiring the sinking to fall after the equinox (1 Apr) and on or before the Pleiades' heliacal setting (4 Apr) leaves one Ti every **6 years**.
- One-third of those have a high Venus.
- Mercury's station occurs once every **116 days**.
- So the references can be matched exactly only **one day every 2,000 years**.
- Implied arithmetic [me]: 6 x 3 x 116 = 2,088, presented as a frequency of once per 2,000 years.

**Further rhetoric:**
- They say they did not pick which references to pursue: the ones examined are all they found.
- They call the odds of a chance coincidence with the only eclipse of the century very small [B&M *Conclusions*].
- There is no formal test, p-value, trials factor or null model.

**Assumptions in the calculation** [me]:
- **Independence.** The three clues are treated as independent.
- **Mercury rate.** It is an exact-day match (1/116), although the acceptance tolerance actually used is about ±1 day, i.e. about 3/116, and the text says "a few days".
- **Venus rate.** "1/3" is the rate *given* a morning-star Venus. The unconditional rate in Table S2 is 21/136 = 0.15.
- **Equinox clue.** It is included in the probability although it was "not applied" in the selection.
- **No look-elsewhere correction** for:
  - the choice among interpretations (two seasons for the stars, three Mercury variables, sequential or parallel offsets);
  - the tolerances;
  - which passages count as clues.
- **Shared constraint with the eclipse.** The New Moon requirement is common to the eclipse hypothesis, and the window was chosen from Troy dates.

**Rough check from their own table** [me]:
- With independent clues and the empirical rates in 1250-1115 BC (V 21/136, M within ±1 day 4/136), the **expected number of V-and-M years in the 136-year window is 21 x 4 / 136 = 0.62**. That gives P(at least one) of about 0.46 under a Poisson approximation.
- Adding E (20/136) gives an expected 0.09.
- This is only an indicative calculation for the bench's null models, not a result.

---

## 9. Result dates (as claimed)

**Day 0 = Ti = 16 April 1178 BC = 16 Apr -1177**, proleptic Julian (JD 1291263.5 at 0h) [B&M; JD me]. It is the new moon and the day of the total solar eclipse.

| Day | Date (1178 BC, Jul.) | What B&M report |
|---|---|---|
| Ti - 34 | 13 Mar | Mercury at westernmost rising azimuth on 12-13 Mar; heliacal rising 13 Mar |
| Ti - 29 | 18 Mar | departure. At nautical twilight (7:38 p.m., Ithaka latitude) the Pleiades are astern and Boötes ahead-left, visible all night (Fig. 2). B&M state this night is New Moon; my Meeus conjunction is about 03:20 UT+2 on 18 Mar |
| Ti - 12 / -11 | 4 / 5 Apr | Pleiades' last night 4 Apr (heliacal setting); raft sunk 5 Apr; equinox 1 Apr 3:24 p.m. |
| Ti - 5 | 11 Apr | Venus rises 4:39:45, sunrise 6:22:41, lead 1:42:56 (text: 1 h 43 min), magnitude -4.2 |
| Ti | 16 Apr | total eclipse seen from the Ionian Islands at 12:02 p.m. "local" (= UT+2 [me]); my Meeus conjunction is about 12:14 UT+2 |

Times are those printed by B&M, which I identify as UT+2 zone time (section 3).

---

## 10. History cited: Plutarch to Schoch and Neugebauer, with eclipse circumstances

**As cited by B&M** [B&M Introduction and refs 6-16]:
- **Plutarch** (*De facie* §19; ps.-Plutarch *De Vita et Poesi Homeri* §108) and **Heraclitus** the allegorist (*Homeric Questions* §75) read Theoclymenus' speech as a poetic description of a total solar eclipse. Both noted the references to the New Moon.
- Objections that B&M summarise: no explicit eclipse elsewhere; the scene is indoors; nobody else sees it; the darkness fits Hades imagery. Page (1955) treats the lines as suspect.
- The idea that the passage refers to a historical eclipse is credited to Fotheringham (1921, *Historical Eclipses*), and the 16 April 1178 BC identification to **Schoch** (refs 1, 12, 13) and **Neugebauer** (ref. 14).
  - Ref. 14 is **P. V. Neugebauer**, *Astronomische Chronologie* (de Gruyter, 1929).
  - Ref. 42 is a different person: **O. Neugebauer**, HAMA (1975), cited only for the Thales discussion.
- Abstract: in the late 1920s Schoch and Neugebauer computed that the eclipse was total over the Ionian Islands, and was the only suitable eclipse in over a century fitting the classical sack of Troy around 1192-1184 BC, a decade earlier.
- Introduction: B&M found no translation of the Odyssey that mentions an eclipse in a note on xx.356.
- B&M say oral transmission of such information over about five centuries is implausible, and that eclipse computation before the 8th-century BC records carries growing Delta-T error.

**Eclipse circumstances reported by B&M** [B&M Introduction, Fig. 1, *Historical Plausibility*; SI Fig. S1, S2]:
- 16 Apr 1178 BC, close to local noon; **the 31st eclipse of Saros series 39**.
- From the Ionian Islands at **12:02 p.m. local time**, all five naked-eye planets, the Moon and the corona were visible on an arc of the ecliptic of less than 90 deg. The Pleiades stood around the hidden Sun like a crown.
- Planet magnitudes: Venus -4, Jupiter -1.9, Mercury -1.2, Saturn 0.16, Mars 1.3.
- The equinox had been on 1 April.
- **Greatest eclipse at 32.7 N, 12.7 E**, about 50 km WSW of Tripoli, 33 deg due west of Babylon.
- Track NE-SW. With Starry Night's Delta-T, **Ithaka and Paliki lie on the northern edge of totality**; the EmapWin track (Delta-T 28,907 s) is shifted further north.
- Total solar eclipses recur at a given place about once in 370 years (ref. 3).
- One exeligmos later, **18 May 1124 BC**, the eclipse was total over Babylon; greatest eclipse at 32.9 N, 45.3 E, about 90 km ENE of Babylon.
- Thales:
  - 28 May 585 BC;
  - one Saros earlier, **18 May 603 BC**, totality passed about 220 km SE of Ur;
  - half a Saros earlier, 23 May 594 BC, a total lunar eclipse was visible from Greece and Mesopotamia.
- SI extras, offered as allegories:
  - a total lunar eclipse on **15 Oct 1188 BC**, offered as an allegorical date for the fall of Troy, half a Metonic cycle earlier;
  - **14 Apr 1186 BC**, a Metonic subcycle (99/136 lunations), as the near-arrival of the bag-of-winds episode.

**Schoch 1926 (primary, read)** [Schoch 1926, The Observatory 49:19-21]:
- Uses Cotterill's translation of Od. 20.351-352, 355-357.
- Cites Plutarch and the medieval commentator **Eustathius** for the eclipse reading. Eustathius is not cited by B&M.
- Cites **Fotheringham** (*Historical Eclipses*, 1921, pp. 16-18) as supporting the reading but declining to use it to date the Trojan War.
- **Method:**
  - Oppolzer's *Syzygientafeln* (1881), which he corrected throughout.
  - His own secular terms: +12.24″ s² in the Moon's mean longitude (from Fotheringham's Almagest occultations, MN 75:377-394, 1915); +9.60″ s² in the mean elongation, from ancient solar eclipses; hence +2.64″ s² in the Sun's mean longitude; and a correction of -1.10″ to Newcomb's centennial solar motion. Here s is Julian centuries from 1800 Jan 0.
- **Search interval: -1240 to -1140** (astronomical years).
- **Result:** only the total eclipse of **-1177 April 16** (civil day counted from midnight) qualifies.
  - The order of events in Book 20 puts greatest phase between **10 a.m. and noon**; this is the only solar eclipse in that time window.
  - With his solar elements, **the southern limit of totality passes through Ithaca**, where totality is momentary at **11:41 local mean time**, the time he gives for Theoclymenus' warning.
  - He rejects the only other large eclipse at Ithaca in the interval, the annular eclipse of **-1182 Jan 12**: magnitude 11.4 digits, greatest phase 14 min after sunrise, which does not fit the narrative.
- **Hour-by-hour reconstruction of Day 0:** sunrise 5:40 a.m. ... suitors' meal 10:30-12:00 ... warning 11:41 LMT ... slaughter in the evening.
- **New Moon:** cites 14.161-162 and 19.306-307 as proof. He notes that λυκάβας literally means a journey of light and can denote a year, month or day.
- **Chronology:** the traditional date for Odysseus' return (-1172) would be 5 years too late. His restored chronology:
  - Trojan War -1197 to -1187; fall of Troy -1187; wanderings -1187 to -1177;
  - landing on Scheria early April -1177; **landing on Ithaca -1177 April 12, morning**;
  - **slaughter of the suitors -1177 April 16, 6 to 8:30 p.m.**
- Schoch's Ithaca landing (12 April) is Ti - 4, i.e. B&M's *parallel* numbering, not the sequential Ti - 5 [me].

**Not read:**
- Schoch, *Die Sterne* 6:88 (1926), and *Die sechs griechischen Dichter-Finsternisse* (Berlin-Steglitz, 1926).
- P. V. Neugebauer, *Astronomische Chronologie* (1929): de Gruyter, paywalled; no free scan found on archive.org.
- For Neugebauer I rely **only on B&M's statement**.
- MacDonald (1967, J. Br. Astron. Assoc. 77:324-328) also not read; known only through B&M's quotation of it.

---

## 11. Internal inconsistencies and gaps (for reproduction)

1. **Pleiades' last visibility is given three ways:**
   - 3 Apr [B&M *References*: latest night the Pleiades are visible];
   - the night of 4 Apr = heliacal setting [B&M *Intersecting*];
   - 5 Apr [SI *Metonic Cycles*].
2. **Sinking bound.** Ti - 11 <= 5 Apr [B&M *References*], but no later than 4 April in the probability paragraph. 1178 BC passes only with <= 5 Apr.
3. **Hermes' day.** 13 Mar (Ti - 34) [B&M *Intersecting*] versus 15 Mar [SI Table S1, note at v.225].
4. **Moon phase at departure.** "That night is New Moon" on 18 Mar [B&M]; my computation agrees (conjunction about 03:20 UT+2). The SI instead places the departure at the preceding full moon [SI *Metonic Cycles*], which is wrong by half a lunation [me].
5. **14.457.** Called "Night -2", but placed on Day -5 (sequential) by B&M's own Table 1.
6. **Δ arithmetic ignores 29 February.** Printed Δ matches 365-day year arithmetic in **152 of 152** rows; true proleptic-Julian arithmetic matches only 131 [me].
   - The 21 leap-year rows whose interval spans 29 Feb are off by one day.
   - **1157 BC: Table S2 has -1, Table 2 has 0 (true value 0).** This is the only value I found that differs between the two tables.
   - **1177 BC: Table S2 has 3 (pale yellow), the true value is 4 (white).**
   - None of this changes the V-and-M survivor set.
7. **Ti dates.**
   - Agree with my conjunction dates (Meeus ch. 49, Delta-T 27,602.7 s, UT+2) for 137 of 152 rows.
   - 14 disagree by one day, all at conjunctions computed between 00:00 and 06:15 UT+2. That is plausibly within the precision of my truncated-series check, but it could also be a day-boundary convention.
   - **1243 BC (13 Mar) is two days off** (computed 15 Mar about 21h). Its Ti - 11 = 2 Mar is consistent with the printed Ti, so the error carries through that row.
8. **Window mismatch.** The text says 1250-1115 BC, but Table S2 runs 1251-1100 BC. The extra years contain a near miss (1111 BC) that the authors coloured but did not discuss.
9. **Venus "1/3"** is a conditional rate; the unconditional rate is 0.15 (section 5).
10. **1684 new moons** versus my 1683 for 1250-1115 BC inclusive: an endpoint convention.
11. **"Local time" is UT+2 zone time** (sunrise fit), not LMT. Schoch uses LMT; B&M's 12:02 p.m. corresponds to about 11:25 LMT [me].
12. **Three Delta-T values** for the eclipse (27,602.7 s, 28,907 s, 28,590 s). Schoch (1926) predates Delta-T as a parameter and used his own secular accelerations instead.
13. **MWRA** is not numerically defined (section 5, clue M). The text's "visible" requirement is applied only to 1178.
14. **Where Ithaca sits relative to the track:**
    - Schoch: on the southern limit of totality;
    - Starry Night track (B&M SI): on the northern edge;
    - EmapWin track: shifted north.
15. **Two ways to read the stars.** The constellation cutoffs (17 Feb, 3/4 Apr) were computed once, apparently for the 12th century BC and Ithaca's latitude, and applied as fixed Julian dates to every year from 1251 to 1100 BC.
16. **Ti selection.** The rule for choosing one Ti per year when two new moons qualify is not stated.

---

## 12. Reproduction checklist (parameters to implement)

- **Candidates.** All new moons, 1 Jan 1250 BC to 31 Dec 1115 BC (and 1251-1100 BC to match Table S2). Ti = calendar date of the conjunction in UT+2 zone time; proleptic Julian; astronomical years.
- **Season (C).** Ti - 29 >= 17 Feb and Ti - 12 <= 4 Apr. Better: recompute the cutoffs for each year from the stars' visibility at nautical twilight (Sun at -12 deg), with Arcturus for Boötes, the Pleiades at a 2 deg minimum altitude, and Ithaca's latitude (about 38.4 N, 20.7 E).
- **Venus (V).** On Ti - 5: sunrise minus Venus rise >= 90 min (Venus must be a morning star). Near-miss band 60-90 min.
- **Mercury (M).** Date of Mercury's turning point nearest Ti - 34 within ±1 day; near misses at ±2-3. Implement the three definitions separately:
  - (a) extreme of the rising-point azimuth;
  - (b) retrograde-to-direct station in ecliptic longitude;
  - (c) greatest western elongation.
  
  Optionally also require morning visibility (1 deg minimum altitude, standard extinction).
- **Equinox (E).** Report only, not as a filter: 1 Apr <= Ti - 11 <= 5 Apr (and the <= 4 Apr variant).
- **Offsets.** Sequential (34, 29, 12/11, 5); repeat with parallel (33, 28, 11/10, 4).
- **Ephemeris.** B&M used VSOP87 + ELP-2000/82 with Starry Night's Delta-T (27,602.7 s for 1178 BC). A modern DE-series ephemeris with the Morrison-Stephenson Delta-T should be run alongside.
- **Expected outcome to match.** In 1250-1115 BC: V passes 21 rows, M (±1) passes 4 (1236, 1224, 1178, 1157), and V-and-M is only 1178. Near misses: 1157, 1191, and 1111 outside the window.

---

## 13. Files written by this extraction

- `C:\Projects\odybench\docs\research-bm2008-a.md` (this document)
- `C:\Projects\odybench\data\bm2008-a\baikouzis-magnasco-2008-pnas.pdf`: main paper (Wayback 2017 capture of the pnas.org PDF)
- `C:\Projects\odybench\data\bm2008-a\baikouzis-magnasco-2008-SI.pdf`: complete SI (Wayback 2021 capture)
- `C:\Projects\odybench\data\bm2008-a\bm2008-pmc-fulltext.txt`: text extracted from the PMC HTML
- `C:\Projects\odybench\data\bm2008-a\bm2008-table2-pmc.jpg`: Table 2 image
- `C:\Projects\odybench\data\bm2008-a\table_s2.tsv`: Table S2 transcription with authors' cell colours (O/Y/y)
- `C:\Projects\odybench\data\bm2008-a\schoch-1926-observatory-49-19.pdf`: Schoch 1926 (ADS scan)
