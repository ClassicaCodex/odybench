# Baikouzis & Magnasco (2008): reconciled reproduction spec

Target: Baikouzis C., Magnasco M. O. (2008), *Is an eclipse described in the Odyssey?*, PNAS 105(26):8823-8828, doi:10.1073/pnas.0803317105. Received 2 July 2007, communicated by M. J. Feigenbaum 7 April 2008, issue of 1 July 2008. PMC ID **PMC2440358** (the PMC2440355 named in the original task is a different paper; both extractions found this independently). Abbreviated **B&M** below.

This document merges two independent extractions:
- **[A]** `docs/research-bm2008-a.md`
- **[B]** `docs/research-bm2008-b.md`

For every field where they disagreed, and every field where either relied on a secondary report, I went back to the primary paper, the Supporting Information (SI) and, where possible, Schoch (1926). Where a disputed number could be recomputed, I recomputed it with JPL DE441 through `odybench.ephem` (skyfield + ERFA).

## Conventions

- **Years.** Every year is given as historical BC with the astronomical year in parentheses: 1178 BC = -1177.
- **Calendar.** All dates are **proleptic Julian**.
- **Leap years.** BC years with BC ≡ 1 (mod 4) are Julian leap years (astronomical year divisible by 4), e.g. 1189, 1177, 1157 BC.
- **Time scales:**
  - **TT**: Terrestrial Time (= TD/TDT of the eclipse canons).
  - **UT**: UT1.
  - **UT+2**: zone time on the 30°E meridian. This is the clock B&M actually used (section 3.2).
  - **LMT**: local mean time at 20.7°E, equal to UT + 1 h 22.8 min.
  - **LAT**: local apparent solar time.
- **Day offsets.** "Ti - n" means n civil days before the candidate Day 0.

## Provenance tags

- **[B&M §Method]**: the main paper, by section heading. The headings are Introduction (unheaded opening), Method, References and Constraints, Intersecting the Constraints, Historical Plausibility, Conclusions; plus Table 1, Table 2, Fig. 1, Fig. 2.
- **[SI p.n]**: SI page n of 7.
- **[S1]**, **[S2]**: SI Tables S1 and S2.
- **[Schoch 1926 p.n]**: *The Observatory* 49, page n.
- **[A]**, **[B]**: the two extractions.
- **[me: script]**: computed by me. The scripts and their outputs are in `results/bm2008-reconcile/`.

Throughout, what the source says is kept separate from my inference, which is always tagged [me].

---

## 1. Sources actually read

| Item | Copy used | Status |
|---|---|---|
| Main paper, full text | PMC HTML text, `data/bm2008-a/bm2008-pmc-fulltext.txt` | **Read in full by me.** The section quotes and criteria below are checked against it. |
| Main paper, PDF | `data/bm2008-a/baikouzis-magnasco-2008-pnas.pdf` (Wayback 2017 capture of pnas.org, text layer) [A]; `data/sources/bm2008-b/...pdf` = `data/refs/baikouzis-magnasco-2008.pdf` (SEDICI OCR scan, 910,730 bytes) [B] | Used by A and B. I relied on the PMC text plus the Table 2 image. |
| SI (7 pp.) | `data/bm2008-a/baikouzis-magnasco-2008-SI.pdf`. **Byte-identical** to B's copy (`cmp`). Wayback 2021 capture of `pnas.org/content/suppl/2008/06/24/0803317105.DCSupplemental/0803317105SI.pdf`. | **Read by me**: pp. 1-4 text via `pdftotext`. |
| Table S2 (152 rows) | A's and B's transcriptions (`data/bm2008-a/table_s2.tsv`, `data/sources/bm2008-b/table_s2.tsv`). Each was parsed independently from the PDF text positions and fill colours. | **Identical cell for cell**, including all colours: 152 rows × 13 fields, 0 differences [me: comparison script]. All S2 counts below rest on two agreeing parses. |
| Table 2 (main paper) | PMC image `data/bm2008-a/bm2008-table2-pmc.jpg` | **Read by me.** Compared row by row with S2 (§8). |
| Schoch C. (1926), *The eclipse of Odysseus*, *The Observatory* 49:19-21 | `data/bm2008-a/schoch-1926-observatory-49-19.pdf` (ADS JBIG2 scan) | **Rendered and read by me** (Windows.Data.Pdf → PNG). A had read it; B had not. |
| Fotheringham J. K. (1921), *Historical Eclipses*, pp. 16-18 | `data/refs/fotheringham-1921.txt` (local OCR) | Read by me for the Odysseus section only. |
| Plutarch, *De facie* 19.1; Heraclitus, *Allegoriae* 73 | `data/text/plutarch-defacie-grc.tsv`, `data/text/heraclitus-allegoriae-grc.tsv` | Read by me (B had checked them too). |
| Five Millennium Canon page for -1177 Apr 16 | `data/refs/nasa/SEdata_-11770416.html` | Read by me. |
| **Not read** | P. V. Neugebauer, *Astronomische Chronologie* (de Gruyter 1929): no free scan found. T. L. MacDonald (1967), *J. Br. Astron. Assoc.* 77:324-328: the ADS full-text request returned an empty HTTP 202. Schoch, *Die Sterne* 6:88, and *Die sechs griechischen Dichter-Finsternisse* (1926). Murray (1924). | For these, **only B&M's report** is available. |

---

## 2. What B&M claim, and what they disclaim

### Claims
**Sources:** [B&M abstract; §Intersecting the Constraints; §Historical Plausibility; §Conclusions].

1. **The search.** Take three "overt" references (Boötes and the Pleiades; Venus; the New Moon) plus one "conjectural" one (Hermes' trip to Ogygia = the planet Mercury). Search exhaustively for dates in **1250-1115 BC** (-1249 to -1114). One date matches closely: **16 April 1178 BC (-1177)**.
2. **Satisfies the criteria.** In the 135-year span, that date satisfies "all criteria as stated". It satisfies all five references (including the unapplied Equinox) under both the parallel and the sequential chronology, and "exactly" under the sequential one.
3. **Coherence.** The references "cohere". Two separate sets of verses, the eclipse lines and the other astronomical references, point to the same date with a very low chance probability. An exact match happens about "one day every 2,000 years" (§10).
4. **The eclipse coincidence.** The chance that purely fictional references would match the century's only eclipse by accident is minute.
5. **Supporting absences and timing:**
   - Ares is absent from the foreground story, and Mars was not visible in March-April 1178 BC except during the eclipse.
   - The eclipse falls at noon, as Schoch noted, matching the scene.
   - It falls in early spring.
6. **One hand.** Post hoc, B&M say the references, including the disputed eclipse lines, may be the work of one poet, whom they call "Homer". On this view the references are structural, a timeline behind the poem.

### Disclaimers
**Sources:** [B&M Introduction caveats; §Method; §Historical Plausibility; §Conclusions].

- **Wrong readings.** If the passages are not astronomical, the dates and probabilities fail, and the whole calculation is a non sequitur. The case is "still far from proved".
- **No claim about events.** Even if the readings are right, the analysis says nothing about whether the events happened. A historical Odysseus and an allegorical, astronomically structured one are equally compatible.
- **No eclipse assumed.** Od. 20.356-357 is not a search criterion. [me: Day 0 = New Moon is still imposed, and that is a necessary condition for a solar eclipse.]
- **Hermes = Mercury** is the one implausible assumption. Its first surviving attestation is Plato's *Timaeus*, so it would require moving the Greek adoption of planet-god names about two centuries earlier.
- **Poseidon = equinox** is "far more conjectural" and is **not applied**. It is only listed for confirmation.
- **Transmission.** The conclusions imply sophisticated astronomy and centuries of transmission, which B&M call problematic. They "dare not conjecture" how the knowledge was obtained, and do not espouse the Babylon/exeligmos route.
- **Visibility uncertainty.** First and last visibility dates are psychophysical, so each carries at least ±1 day of uncertainty [B&M §Method].

---

## 3. Software, ephemeris, Delta-T, clock, site

### 3.1 Stated by B&M
**Sources:** [B&M §Method; Fig. 1, Fig. 2 captions; SI p.2 Fig. S1 caption].

- **Planetarium: Starry Night Pro 6.0.4** (Imaginova 2006, ref. 31).
  - VSOP87 for the planets; Chapront ELP-2000/82 for the Moon.
  - ΔT from Meeus, following Stephenson & Morrison (1984), "with additional adjustments".
  - **ΔT for the eclipse = 27,602.7 s.**
- **Eclipse maps: EmapWin**, custom-corrected for Espenak's ΔT revisions.
  - The Fig. S1 track uses **ΔT = 28,907 s**.
  - The Five Millennium Canon lists **28,590 s** for this eclipse.
- **Visibility: Planetary, Lunar, and Stellar Visibility (PLSV) 3.0** (Lange & Swerdlow, Alcyone 2006, ref. 32). Standard magnitude-corrected parameters; minimum altitude **1° for Mercury** and **2° for the Pleiades**.
- **Calendar and times.** Julian calendar. Times are "local to the Greek islands". Seasonal references are for the 12th century BC. The only site information is "Ithaka's latitude" (Fig. 2).
- **ΔT error.** Extrapolation error is about 2-3° of longitude, about the width of the track [B&M Introduction]. The SI gives about 3° (Stephenson & Houlden 1986), 4° (Huber, calibrated at 500 BC) and 2° (Huber, calibrated at 750 BC). Different ΔT models move the track by about 1°, and the track is always NE-SW [SI p.2].
- **Track position.** On the Starry Night path, Ithaka and Paliki lie on the northern edge of totality; the EmapWin track is shifted north [SI p.2].

### 3.2 Clock and site: settled
A and B both concluded that the clock is UT+2 (A from a 75-row sunrise fit; B from three rows). I recomputed **every** Table S2 sunrise and Venus rise on Ti-5 with DE441 [me: `check_venus.py`]:
- **Settings:** site 38.4°N 20.7°E; ΔT 27,602.7 s; airless altitude; h0 = -0.8333° for the Sun and -0.5667° for Venus.
- **Result: S2 sunrise − computed UT sunrise = +120.0 min** (sd 1.6 min, n = 75), and S2 Venus rise − computed = +119.9 min (sd 1.5 min). **B&M's "local" times are UT+2 zone time.**
- **Latitude.** The sunrise column alone barely constrains latitude [A]. But the Venus and Sun offsets agree only near 38.4°N: at 37.0°N they differ by 1.6 min, at 39.5°N by 1.5 min. So the site is consistent with Ithaca's latitude, as Fig. 2 says [me].
- **Spot checks for 1178 BC** [me: `check_extras.py`, DE441, ΔT 27,602.7 s]:
  - Sun at -12° on 18 Mar: **19:34 UT+2**. B&M (Fig. 2): 7:38 p.m. B had 19:35.
  - Vernal equinox (apparent solar longitude 0°): **1 Apr 1178 BC 21:11:31 TT = 15:31 UT+2**. B&M: 3:24 p.m. B had 15:12.

### 3.3 ΔT is not portable between ephemerides (new check)
The Fig. 1 eclipse time, 12:02 p.m. "local", could **not** be reproduced. I computed DE441 local circumstances at Ithaca, 38.37°N 20.72°E [me: `check_extras.py`]:

| ΔT (s) | Maximum, UT+2 | Magnitude | Total? |
|---|---|---|---|
| 27,602.7 | 12:48 | 0.900 | no |
| 28,590 | 12:26 | 0.975 | no |
| 28,907 | 12:18 | 0.999 | no (Paliki, about 38.25°N 20.40°E: total, 105 s) |

- So **DE441 with Starry Night's ΔT does not put Ithaka on the edge of totality**, as B&M's Starry Night run did. A ΔT value only means something together with the lunar theory, i.e. its secular acceleration, that it was fitted with [me].
- **The greatest-eclipse point B&M quote is the Canon's.** B&M give 32.7°N 12.7°E, "50 km WSW of Tripoli". That is exactly the Five Millennium Canon's point (VSOP87/ELP-2000/82, ΔT = 28,590 s, greatest eclipse 10:00:58 UT = 17:57:28 TT) [`data/refs/nasa/SEdata_-11770416.html`]. It is not the Starry Night (27,602.7 s) geometry [me].
- **For the clue tests**, ΔT matters only through clock times and through the calendar date of conjunctions near midnight [me].

---

## 4. Narrative chronology and day offsets

**Table 1** [B&M Table 1, footnote; lines checked by me in `data/text/odyssey-grc.tsv`]. Day 0 = the slaughter of the suitors.
- **Sequential** reckoning counts parallel strands as consecutive days. **The search uses the sequential offsets.**
- **Parallel** reckoning has Athena reach Sparta instantly.

| Day seq | Day par | Event (B&M) | B&M lines | Greek text check [me] |
|---|---|---|---|---|
| -40 | -33 | Council of Gods; Poseidon among the Ethiopians; Athena to Telemachus | (none) | book 1; Poseidon among Ethiopians 1.22-26 |
| -39 | -32 | Ithaca assembly; Telemachus leaves | | |
| **-34** | -33 | Council; Zeus sends **Hermes to Ogygia**; Calypso releases Odysseus | v.1-261 | Hermes' flight 5.43-58; arrival 5.55; complaint 5.97-103; sunset 5.225 |
| -33..-30 | -32..-29 | Raft built | v.262 | 5.262: "the fourth day, and all was done" |
| **-29** | -28 | Sent off **at sunset**; Pleiades, Boötes, Bear on the left | v.263-278 | 5.263 (fifth day); stars 5.270-277 |
| -28..-12 | -27..-11 | Sailing, 17 days | v.279 | 5.278 (17 days); 5.279 (18th day, mountains appear) |
| **-11** | -10 | Poseidon, back from the Ethiopians, sinks the raft | v.280-387 | 5.282 |
| -10 | -9 | Swimming | v.388-389 | 5.388 (two nights, two days) |
| -9 | -8 | Lands in Phaeacia | v.390-493 | 5.390 (third day) |
| -8 | -7 | Nausicaa; to Alcinous | vi.1-vii.347 | |
| -7 | -6 | Palace, games, narration | viii.1-xiii.16 | |
| -6 | -5 | Gifts; boards ship at sunset | xiii.17-92 | |
| **-5** | -4 | **Reaches Ithaca with the Star of Dawn**; Athena; Eumaeus | xiii.93-xiv.533 | 13.93-95; 14.161-162; 14.457 |
| -4 | -4 | Athena fetches Telemachus | xv.1-190 | |
| -3 | -3 | Telemachus travels; Odysseus with Eumaeus | xv.191-493 | |
| -2 | -2 | Telemachus reaches Ithaca at dawn | xvi.1-478 | |
| -1 | -1 | Odysseus in his hall; Penelope; Eurycleia | xvii.1-xx.54/90 | 19.306-307 |
| **0** | 0 | Festival of Apollo; eclipse; death of the suitors | xx.91-xxiii.344 | 20.156; 20.276-278; 20.356-357; 21.258-259 |
| 1 | 1 | Laertes; battle | xxiii.345- | |

- **Time at sea.** Table 1's footnote: Odysseus leaves near sunset and lands before sunset, so he is at sea exactly 20 days and 20 nights.
- **Where the two reckonings differ.** They differ by exactly one day for every Odysseus-strand event from Hermes' visit through the Ithaca landing: -34/-33, -29/-28, -11/-10, -5/-4 [A, B; confirmed from Table 1].

---

## 5. The clues: lines, interpretation, exact criterion, offset

**Ti** is the candidate New Moon date (Day 0). Clues N, C, V and M were applied in the search; E was listed but not applied; X (the eclipse) was not used.

### N: New Moon on Day 0 (defines the search unit)

**Lines** [B&M §Method; S1; me: Greek checked]:
- Od. 14.161-162 (to Eumaeus) and 19.306-307 (to Penelope): one month waning, the next beginning (τοῦ μὲν φθίνοντος μηνός, τοῦ δ' ἱσταμένοιο).
- 14.457: a moonless night (σκοτομήνιος).
- **Festival of Apollo on Day 0.** B&M say it is stated several times but give no lines. My identification: 20.156 (ἑορτή), 20.276-278 (hecatomb in Apollo's grove), 21.258-259. Fotheringham (1921, p.17) cites the same 20.156 and 20.276 as the feast day.

**Interpretation** [B&M §References and Constraints]:
- Day 0 is a New Moon, so only New Moons are searched.
- Murray's Metonic-cycle reading (Day 0 = the end of a 19-year cycle) is background only, not a criterion [B&M §Method; SI p.1].

**Criterion.** **Ti = the date of a New Moon.** B&M give no operational definition: they do not say whether this is the conjunction instant, in which time zone, or with which day boundary.

What Table S2 actually prints, compared with DE441 conjunctions [me: `check_ti.py`, `check_ti_ra.py`; ΔT 27,602.7 s]:

| Definition | UT | LMT 20.7°E | UT+2 | UT+3 |
|---|---|---|---|---|
| Ecliptic-longitude conjunction, civil date | 134/152 | 138/152 | 136/152 | 132/152 |
| Right-ascension conjunction | 128 | 127 | 124 | |
| Minimum Sun-Moon separation | 135 | 135 | 135 | |

- **No single rule reproduces the column.** Ti dates one day early are interleaved with unshifted rows at the same clock hours.
  - The 01:46 UT+2 conjunction of 1177 BC is printed a day early, but the 00:41 UT+2 conjunction of 1175 BC is not.
  - The 06:19 conjunction of 1245 BC is shifted, but 06:07 (1249 BC) and 06:45 (1173 BC) are not.
- **Rows that differ from the UT+2 conjunction date (16):** 1248, 1246, 1245, 1205, 1187, 1177, 1154, 1147, 1135, 1134, 1125, 1115, 1112, 1105 and 1101 BC are one day early; plus 1243 BC.
- **1243 BC is not a New Moon.** S2 prints 13 Mar; the conjunction is 15 Mar 1243 BC 20:49 UT+2. That row's Venus, Mercury and Ti-11 entries were all computed from 13 Mar.

**Offset:** 0.

**Inconsistency.** B&M call 14.457 "Night -2". But their own Table 1 puts xiii.93-xiv.533 on Day -5 (sequential) / -4 (parallel) [A, B; confirmed]. Fotheringham (1921, p.17) likewise puts the moonless night on the evening of the Eumaeus prediction.

### C: Pleiades, late-setting Boötes, the Bear (season of the voyage)

**Lines** [B&M §Method; S1; me: Greek checked]:
- Od. 5.270-277:
  - 5.272: Πληιάδας τ' ἐσορῶντι καὶ ὀψὲ δύοντα Βοώτην;
  - 5.273-275: the Bear;
  - 5.276-277: Calypso told him to keep it on his left.
- **Iliad parallel.** B&M cite "Il. xviii.485". The Bear lines **Il. 18.487-489 repeat Od. 5.273-275 word for word**, and Il. 18.486 names the Pleiades, Hyades and Orion [me: `iliad-grc.tsv`]. A's "18.485ff" and B's "18.487-489" are therefore both right, at different granularity.

**Interpretation** [B&M §References and Constraints]:
- The Bear is circumpolar; keeping it on the left means sailing east.
- The Pleiades and Boötes appear together after twilight around March (Pleiades set early, Boötes late) and around September (the reverse). The epithet "late-setting" for Boötes selects **March**, following MacDonald (1967) (not read; known only through B&M's quotation).
- Boötes is represented by **Arcturus**. The SI (p.1) discusses Arcturus' apparent achronical rising, and MacDonald's quoted sentence speaks of Arcturus. B&M do not say which star or model stands for the Pleiades.

**Criterion, as stated** [B&M §References and Constraints]:
- At nautical twilight (Sun at -12°), Boötes' earliest visibility (its "apparent achronical rising") is **17 February**.
- The **latest night the Pleiades are visible is 3 April**. "Hence Ti-29 should be between 17 February and 4 April."
- Because he steers by these stars every night until sunk, **the whole 17 days of sailing before the sinking must lie within 17 February-4 April**.
- The constellation reference "requires the sinking to be no later than 5 April" [same section, Equinox paragraph].
- One, or at most two, Ti per year pass; the rest are discarded.
- Visibility: PLSV, Pleiades minimum altitude 2° [B&M §Method].

**Operational form (reconciled)**: **Ti - 29 ≥ 17 Feb and Ti - 12 ≤ 4 Apr** (equivalently Ti - 11 ≤ 5 Apr).
- So Ti runs from **18 Mar to 16 Apr in a common year**, and from **17 Mar to 16 Apr in a Julian leap year** when the 29 February is counted.
- The cutoffs are fixed Julian dates applied to every year.

**Offsets:** departure Ti - 29 (sequential; -28 parallel); sailing nights Ti - 28 ... Ti - 12; sinking Ti - 11.

**1178 BC (-1177).**
- Ti - 29 = **18 Mar**, itself a New Moon: conjunction at 03:31 UT+2, DE441 with ΔT 27,602.7 s [me]. A had 03:20 and B 03:26 with Meeus.
- At nautical twilight, 7:38 p.m. (Fig. 2), the Pleiades were astern and Boötes ahead-left, visible all night.
- Ti - 12 = **4 Apr**. B&M call the night before 5 April the heliacal setting, the last visible night, after which the Pleiades hide for 40 days [B&M §Intersecting].
- **So 1178 BC sits exactly on the late boundary.**

**Internal inconsistencies** [confirmed in the primary]:
- **Pleiades' last night:** 3 Apr [§References]; 4 Apr [§Intersecting, probability paragraph]; "April 5" [SI p.1, Palamedes paragraph].
- **Arcturus' apparent achronical rising:** 17 Feb [main text] vs "the end of February" [SI p.1]. B noticed this; A did not.
- **Pleiades' invisible period:** 40 days [main text, after Hesiod] vs 44 days "depending on latitude" [SI p.1]. Neither A nor B noticed this.

**Supporting cues, not criteria:**
- Long nights, fires and cloaks. S1 says "xi.370", which is **Od. 11.373** (νὺξ δ' ἥδε μάλα μακρή) in the Greek numbering.
- "Much-blossoming" wood, 14.353.
- The year is ending at the poem's opening. B&M give no line; possibly 1.16 [me].
- Hesiod puts the year's end at the vernal equinox [SI p.1].

### V: the morning star before the Ithaca landing

**Lines.** Od. 13.93-95 [me: Greek checked]: εὖτ' ἀστὴρ ὑπερέσχε φαάντατος ... ἀγγέλλων φάος Ἠοῦς. B&M cite xiii.93-96.

**Interpretation** [B&M §References and Constraints]:
- The star is Venus as morning star, and it rose well ahead of dawn, because a lot happens before daybreak:
  - the landing;
  - the sleeping Odysseus set ashore;
  - his talk with Athena;
  - the hiding of the treasure;
  - Athena's departure for Sparta.
- In this season Venus rises at most about 2 h before the Sun.

**Criterion.** On **Ti - 5**, **Venus rises at least 90 min before the Sun** ("1:30 cutoff", SI p.1). B&M say this happens about 1/3 of the time.
- "High" is operationalised **only** as this rise-time lead. There is no altitude, magnitude or arcus-visionis test.
- S2 leaves the cell blank when Venus is an evening star.

**S2 colour coding** [me: `s2_counts.py`; agreed by A and B]:
- **orange** ⇔ lead ≥ 1:30:00 (exact for all 152 rows; smallest orange 1:32:08, largest non-orange 1:29:06);
- **yellow** ⇔ lead from about 1:00 to 1:30 (smallest yellow 1:02:26 in 1101 BC, 1:06:29 inside the window; largest white 0:58:25);
- **white** otherwise.

**Offset:** Ti - 5 (sequential; Ti - 4 parallel).

**1178 BC:**
- 11 Apr: Venus rises 4:39:45, the Sun 6:22:41 (UT+2), lead **1:42:56**, magnitude -4.2 [B&M; S2].
- DE441 [me]: lead 103.6 min.

**Robustness check** [me: `check_venus.py`]: the DE441 pass set (lead ≥ 90 min) is **identical to S2's orange set** (25 of 25 rows in 1251-1100 BC). The Venus column reproduces exactly.

### M: Hermes = Mercury at a turning point (conjectural; applied)

**Lines** [B&M §Method, §Historical Plausibility; S1; me: Greek checked]:
- The flight over the waves "v.48 onwards". S1 quotes Murray's translation labelled v.48, which is Greek 5.47-56 in Perseus.
- Arrival at the far island, v.55.
- Hermes' complaint about the long trip, v.97-103.
- S1 also quotes **5.225** (sunset that day), annotated "March 15, the day of Hermes visit, almost new moon".

**Interpretation:**
- Hermes goes far west, delivers his message and turns straight back east. B&M read this as an allegory of a planetary turning point, a station (*sterigmos*, the term on the Antikythera mechanism).
- Hermes skimming low over the sea = Mercury never far from the horizon.
- Hermes climbing out of the dark sea at Ogygia = Mercury's first morning visibility [§Historical Plausibility].

**Criterion as stated** [B&M §References and Constraints]:
- On **Ti - 34**, Mercury must be on the western side of its path, **visible**, and close to a turning point.
- B&M name three candidate variables: elongation from the Sun; rising azimuth ("when it becomes westernmost"); and the onset of retrograde motion. They call these "close together in time".
- The test adopted: on Ti - 34 Mercury is "within a few days of achieving its westernmost rise-time azimuth"; this is meant to cover the other turning points too.
- S2's column "MWRA" (maximum western rise azimuth) is "the date of the closest maximum western rise azimuth to Ti - 34" [§Intersecting].

**What MWRA is numerically: settled** [me: `check_mwra.py`, DE441, 38.4°N 20.7°E, h0 = -0.5667°, all 152 rows]. For each S2 year I compared the printed MWRA with the nearest event of each candidate kind:

| Candidate event | Exact match | Within ±1 d | Median (event - S2 MWRA) |
|---|---|---|---|
| **Local maximum of rising azimuth, measured from N through E** (southernmost rising point) | **124/152** | **138/152** | 0 d |
| Retrograde-to-direct station (ecliptic longitude) | 0 | 0 | -8 d |
| Greatest western elongation | 2 | 7 | +5 d |
| Local minimum of rising azimuth (northernmost rising point) | 0 | 0 | -29 d |
| Direct-to-retrograde station; inferior conjunction | 0 | 0 | far |

- **MWRA = the date of the local maximum of Mercury's rising azimuth, measured from north through east**: the southernmost rising point, roughly a minimum of declination during the morning apparition. This confirms B's reverse-engineering (14/20 rows with a low-precision ephemeris) on all 152 rows with DE441.
- A's suggestion that 13 Mar 1178 BC lay near the retrograde-to-direct station is wrong. DE441 has that station on 5 Mar and greatest western elongation on 19 Mar 1178 BC [me]. The three events B&M call "close together" are spread over about two weeks.

**Tolerance.** "A few days" in the text. The S2 colours decode exactly as [me, agreed by A and B; checked on all 152 rows]:
- **orange: |Δ| ≤ 1**;
- **yellow: |Δ| = 2**;
- **pale yellow: |Δ| = 3**;
- **white: |Δ| ≥ 4**.

Here **Δ = (Ti - 34) - MWRA**, in days.

**Arithmetic.** The printed Δ **ignores 29 February**. It matches 365-day arithmetic in 152 of 152 rows and true Julian arithmetic in 131. The 21 leap-year rows whose interval spans 29 Feb are off by one day: 1249, 1241, 1229, 1221, 1209, 1201, 1197, 1189, 1181, 1177, 1173, 1169, 1161, 1157, 1149, 1141, 1137, 1129, 1117, 1109 and 1101 BC [me: `s2_counts.py`].
- **1157 BC:** S2 prints -1; true arithmetic on the printed MWRA gives 0, which is what Table 2 prints.
- **1177 BC:** S2 prints 3 (pale yellow); the true value is 4 (white).

**Visibility.** The "visible" requirement is not tabulated in S2. It is reported only for 1178 BC.

**Offset:** Ti - 34 (sequential; Ti - 33 parallel).

**1178 BC** [B&M §Intersecting]: Ti - 34 = 13 Mar. Mercury rose at its westernmost azimuth on 12 and 13 Mar. **13 Mar was its heliacal rising**; it was not visible on 12 Mar. S2: MWRA 13 Mar, Δ 0.

DE441 [me: `check_mwra_curves.py`, `check_extras.py`]:
- Rising azimuth 112.304° on 12 Mar and 112.299° on 13 Mar: a flat maximum, with DE441 putting it on 12 Mar, so Δ = +1.
- From 11 to 14 Mar, Mercury rises with the Sun at -13.1° to -13.3°, at V = +0.8 to +0.65 (Mallama & Hilton 2018 phase law). By any arcus-visionis test, 12 and 13 Mar are equally placed. The "first visible on 13 Mar" result is a threshold outcome of PLSV's parameters, not a sharp event.

**Inconsistency.** Hermes' visit is 13 Mar in the main text but **15 Mar** in the S1 note at v.225 [SI p.4]. Parallel reckoning would give 14 Mar.

**Claimed rate.** "Mercury's sterigmos happens once every 116 days" (the synodic period).

### E: Poseidon's return from the Ethiopians = equinox (listed, NOT applied)

**Lines.** Od. 5.282ff: Poseidon, returning from the Ethiopians, sees Odysseus from the Solymi mountains. At the outset he is among the Ethiopians (1.22-26; Table 1 Day -40).

**Interpretation.** MacDonald's conjecture that the Earth-shaker's return from the south marks the vernal equinox. B&M rate it far more conjectural than Hermes and do **not** apply it.

**Criterion if applied.** Ti - 11 on or shortly after the equinox (about 1 April). Combined with the constellation bound: **1 Apr ≤ Ti - 11 ≤ 5 Apr** [§References and Constraints]. Three versions exist:
- **Probability paragraph:** after 1 April and on or before **4 April**. Under that wording 1178 BC (Ti - 11 = 5 Apr) fails.
- **S2 "Before" column:** XXX (and an orange Ti - 11 cell) **exactly when Ti - 11 ≥ 1 Apr**. In this table that means 1-6 Apr, since the largest Ti - 11 printed is 6 Apr [me]. A's "≥ 1 Apr" and B's "1-6 Apr" are the same set.
- **Table 2 image:** 30 Mar is coloured pale yellow (1210 and 1145 BC); S2 does not colour it [me: image].

**Offset:** Ti - 11 (sequential; Ti - 10 parallel).

**1178 BC.** Equinox 1 Apr, 3:24 p.m. (DE441: 15:31 UT+2 [me]); sinking 5 Apr.

### X: Theoclymenus' vision, the eclipse (NOT used)

**Lines.** Od. 20.345-357; the key words are 20.356-357, ἠέλιος δὲ / οὐρανοῦ ἐξαπόλωλε, κακὴ δ' ἐπιδέδρομεν ἀχλύς. B&M cite xx.356.

**B&M's glosses.** ἐπιδέδρομεν connotes a sudden attack; κακή can mean "unlucky" of omens. They set the scene at the noon meal.

**Use.** Explicitly excluded from the search. It enters only post hoc: noon timing, early spring, Mars seen only during the eclipse, "only eclipse of the century".

**Offset:** 0.

---

## 6. Search window

**Text** [B&M §Method]. Classical dates for the fall of Troy (BC; astronomical in parentheses):

| Source | BC (astronomical) |
|---|---|
| Ephorus | 1135 (-1134) |
| "Solsibus" [sic; Sosibius] | 1172 (-1171) |
| Eratosthenes | 1184 (-1183) |
| Plato | 1193 (-1192) |
| Parian chronicle | 1208 (-1207) |
| Dicaearchus | 1212 (-1211) |
| Herodotus | about 1250 (-1249) |
| Douris | 1333 (-1332) |
| Troy VIIa destruction layer | about 1190 (-1189) |

- Dropping Douris gives **1240-1125 BC** for Odysseus' return. Widened by 10 years each side, the search window is **1250-1115 BC (-1249 to -1114)**.
- B&M call it the "135-year span"; inclusive, it is 136 years.

**What S2 actually covers:** 1251-1100 BC (-1250 to -1099), 152 rows. That is 16 more years than the text says [A, B; confirmed].

**Dependence on the eclipse** [me, following B]. The window was built from the same Troy-date tradition that led Schoch to search -1240 to -1140, so it is not independent of the eclipse hypothesis.

---

## 7. Candidate unit and count

**Text** [B&M §Method; §References]:
- "All 1684 New Moons" in 1250-1115 BC, each called Ti.
- The constellation criterion leaves one, or at most two, per year.
- **Recount:** **1683** conjunctions fall on UT+2 civil dates from 1 Jan 1250 BC to 31 Dec 1115 BC [me: DE441 `check_ti.py`]. A and B also got 1683 with Meeus. The difference of one is an endpoint convention.

**Table S2 as published:**
- Exactly **one Ti per year**, running from 13 Mar to 17 Apr.
- **Columns:** Year BC | Ti | Venus rise on Ti-5 | sunrise | difference | MWRA | Δ | Ti-11 ("Sinks") | "Before" (XXX).
- **Colours** mark each criterion. The year cell takes the minimum of the Venus and Mercury colours, excluding the Equinox [§Intersecting].
- There is **no constellation or visibility column**.

**Where S2 departs from the stated constellation rule** [me: DE441 conjunctions, UT+2 dates]:

| Year BC | S2 Ti | In-window New Moon(s) | Status |
|---|---|---|---|
| 1246 | 17 Apr (Ti-12 = 5 Apr) | 19 Mar | S2 Ti outside the window |
| 1227 | 17 Apr | 18 Mar | S2 Ti outside the window |
| 1243 | 13 Mar (not a New Moon) | 14 Apr | S2 Ti outside the window |
| 1208 | 16 Apr | 18 Mar, 16 Apr | two qualify; later one listed |
| 1197 (leap) | 15 Apr | 17 Mar (only if 29 Feb is counted), 15 Apr | two qualify; later one listed |
| 1189 (leap) | 18 Mar | 18 Mar, 16 Apr | two qualify; **earlier** one listed |
| 1178 | 16 Apr | 18 Mar, 16 Apr | two qualify; later one listed |
| 1113 | 16 Apr | 18 Mar, 16 Apr | two qualify; later one listed |

- B's list of seven "unevaluated second New Moons" mixed these two categories and missed 1197.
- No consistent rule (earlier or later New Moon) explains S2's choices.

**Table 2** (main paper, 28 rows) is **exactly the rows of 1250-1115 BC with |printed Δ| ≤ 9** [me: `s2_counts.py` vs the image]. Its values match S2 except in two places:
- 1157 BC Δ: 0 in Table 2, -1 in S2;
- the pale-yellow 30-Mar Equinox cells.

This confirms A's "only differing value" and B's colour note.

---

## 8. Survivors by clue

**B&M state** [§Intersecting; SI p.1]:

| Criterion | B&M's statement |
|---|---|
| Constellations | 1-2 Ti per year |
| Venus | about 1/3 pass |
| Mercury | a sterigmos every 116 days |
| Equinox with the Pleiades bound | one Ti every 6 years |
| All criteria as stated | a single date, 16 Apr 1178 BC |
| Narrow misses | **24 Mar 1157 BC** (-1156) and **9 Apr 1191 BC** (-1190); neither satisfies the Equinox |

### 8.1 Counts from the published S2 values and colours
**Source:** [me: `s2_counts.py`; numbers identical in A and B].

| Criterion | 1250-1115 BC (136 rows) | 1251-1100 BC (152 rows) |
|---|---|---|
| Venus a morning star on Ti-5 | 67 (69 blank) | 75 |
| **V**: lead ≥ 1:30 (orange) | **21** (15% of rows; 31% of morning rows) | 25 |
| V near miss (yellow) | 21 | 23 |
| **M**: \|Δ\| ≤ 1 (orange) | **4**: 1236, 1224, 1178, 1157 | 4 |
| M: \|Δ\| = 2 | 1144, 1143 | + 1111 |
| M: \|Δ\| = 3 | 1223, 1203, 1191, 1190, 1177, 1145 | same |
| E: XXX (Ti-11 ≥ 1 Apr, i.e. 1-6 Apr) | 22 | 26 |
| E: 1-5 Apr | 20 | 24 |
| E: 1-4 Apr | 17 | 20 |
| **V and M (orange)** | **1178 only** | 1178 only |
| V and M within ±2 | 1178 | 1178, **1111** |
| V (orange or yellow) and M within ±3 | 1191, 1178, 1157 | + 1111 |
| V and E | 1194, 1186, 1178, 1159 | same |
| M and E | 1224 (Venus lead 0:32:38), 1178 | same |
| V, M and E | 1178 | 1178 |
| Year-cell colours | 1178 orange, 1157 yellow, 1191 pale yellow | + 1111 yellow |

**Near misses** [SI p.1 "Runner-Up Dates"; S2]:
- **24 Mar 1157 BC (-1156).**
  - Venus 1:25:12, "just shy" of 1:30.
  - Mercury "satisfied fully": MWRA 19 Feb; Δ 0 in Table 2, -1 in S2.
  - Ti-11 = 13 Mar, so it fails the Equinox.
  - B&M call it early (sailing in late February).
- **9 Apr 1191 BC (-1190).** Venus 1:06:29; Mercury missed by 3 days; sinking 29 Mar. B&M call it weaker.
- **26 Mar 1111 BC (-1110).** Venus 1:37:29 (orange), Δ -2, Ti-11 = 15 Mar. It is coloured yellow in S2 and lies outside the stated window, and is **never mentioned** by B&M [A, B; confirmed].

### 8.2 Survivors when Mercury is recomputed with DE441 (new; preliminary)
**Source:** [me: `check_mwra_curves.py`]. MWRA was redefined as the DE441 rising-azimuth maximum nearest Ti-34, with true Julian day arithmetic and S2's own Ti.

- **M passes (|Δ| ≤ 1): 1236, 1224, 1190, 1189, 1178, 1144 BC** (6, all inside the window). The printed values give 4.
- **1157 BC drops out.** The DE441 maximum is 22 Feb (rising azimuth 118.199°, against 118.034° on S2's 19 Feb), so Δ = -3. B had found the same 22 Feb.
- **1189 BC enters.** S2's MWRA is 5 Feb, but the DE441 curve has a single clean peak on **13 Feb 1189 BC = Ti-34**, so Δ = 0. S2's 5 Feb is 0.7° below that peak.
- **V and M (DE441 Venus = S2 Venus) = {1178, 1189}.**

**18 Mar 1189 BC (-1188) under the applied criteria:**
- **N:** it is a New Moon.
- **C:** Ti-29 = 18 Feb (leap year) ≥ 17 Feb; Ti-12 = 6 Mar ≤ 4 Apr.
- **V:** lead 1:40:21 in S2; 100.9 min with DE441.
- **M:** Δ = 0. Mercury rises with the Sun at -17.1°, at V ≈ +0.2, better placed than 13 Mar 1178 BC (-13.2°, V ≈ +0.7).
- **E:** it fails (Ti-11 = 7 Mar).

**So with a modern ephemeris, B&M's *applied* criteria (N, C, V, M) are met by two dates in the window.** The uniqueness of 1178 BC then rests on the unapplied Equinox clue. This is my computation, not B&M's claim. It needs a proper visibility model before it becomes a finding.

### 8.3 Chance expectation from B&M's own rates (indicative)
**Source:** [me; A and B got the same].

- Independent V (21/136) and M (4/136) over 136 rows: **E[V∧M] = 0.62**, so P(at least one) ≈ 0.46 (Poisson).
- Adding E: 0.10 with the XXX flags, 0.09 with 1-5 Apr.

These are rough first-order estimates, not the bench's null models.

---

## 9. Result dates (as claimed), with checks

| Day | Date, 1178 BC (-1177), proleptic Julian | B&M | Check [me, DE441] |
|---|---|---|---|
| Ti-34 | 13 Mar | Mercury at westernmost rising azimuth 12-13 Mar; heliacal rising 13 Mar | Rising-azimuth max 12 Mar (flat); station 5 Mar; greatest western elongation 19 Mar |
| Ti-29 | 18 Mar | Departure; New Moon; nautical twilight 7:38 p.m. | Conjunction 18 Mar 09:11 TT = 03:31 UT+2 (ΔT 27,602.7 s); 03:15 UT+2 with SMH2020 ΔT 28,553 s. Sun at -12° at 19:34 UT+2 |
| — | 1 Apr | Equinox 3:24 p.m. | 21:11:31 TT = 15:31 UT+2 |
| Ti-12 | 4 Apr | Last night of the Pleiades | not checked (PLSV-dependent) |
| Ti-11 | 5 Apr | Raft sunk | — |
| Ti-5 | 11 Apr | Venus rises 4:39:45, Sun 6:22:41, lead 1:42:56, magnitude -4.2 | Lead 103.6 min |
| **Ti** | **16 Apr** (JD 1291263.5 at 0h) | Total eclipse; 12:02 p.m. "local" from the Ionian Islands (Fig. 1) | Conjunction 16 Apr 18:05:10 TT = 12:25 UT+2 (ΔT 27,602.7 s). Eclipse at Ithaca not total with DE441 for 27,602.7 or 28,590 s (§3.3) |

**Under parallel reckoning** (Ti-33, -28, -10, -4) [B; arithmetic confirmed by me]:
- Hermes falls on 14 Mar: Δ +1 against S2's MWRA, +2 against DE441's 12 Mar.
- Sailing nights run to 5 Apr, one past the Pleiades bound.
- The sinking falls on **6 Apr**, one day past the ≤ 5 Apr bound.

So "both chronologies" holds only with a one-day tolerance.

---

## 10. The probability claim and its assumptions

**Claim** [B&M paragraph after Fig. 2]:
1. Require the sinking after the equinox (1 Apr) and on or before the Pleiades' heliacal setting (4 Apr). That leaves **one Ti every 6 years**.
2. **One third** of those have a high Venus.
3. **Mercury's sterigmos happens once every 116 days.**
4. So the references "can be matched exactly only one day every 2,000 years".

Implied arithmetic: 6 × 3 × 116 = 2,088 years [A, B]. The Conclusions add that fictional references matching "the only eclipse of the century" by accident would be minute odds. B&M also say "the ones we have examined are all we have found" [§Intersecting]. There is no null model, p-value, Monte Carlo or trials factor.

**Assumptions and slippages** [me; A and B agree; the extra checks are mine]:
1. **The 6 years matches S2's XXX flags (1-6 Apr), not the stated 1-4 Apr bound.**
   - 22/136 rows are flagged, one per 6.2 years.
   - The stated 1-4 Apr bound passes 17/136, one per 8.0 years.
   - 1-5 Apr passes 20/136, one per 6.8 years.
   - Under the stated 1-4 Apr bound, 1178 itself fails.
2. **The Equinox factor is the one criterion B&M did not apply.**
3. **The Venus "1/3" is conditional on a morning-star Venus** (21/67). Unconditionally it is 21/136 = 0.15.
4. **Mercury is treated as an exact-day match (1/116).** The acceptance used is ±1 day, about 3/116; the text says "a few days". The resulting figure is then about 700 years, or about 300 years at ±3 days [B].
5. **The factors are treated as independent**, though C and E are both seasonal (B&M concede E "is not independent of the constellations reference").
6. **No correction is made for interpretive forks:**
   - which season the stars imply;
   - which Mercury variable;
   - sequential or parallel reckoning;
   - the 1:30 cutoff;
   - the tolerances;
   - the window extension;
   - which passages count as clues;
   - the ephemeris (§8.2).
7. **The New Moon condition is shared with the eclipse hypothesis**, and the window was drawn from the same Troy-date tradition.

---

## 11. History cited, and what the primary sources say

**B&M's account** [B&M Introduction, refs 1, 6-16]:
- **Plutarch** (*De facie* §19; ps.-Plutarch *De vita et poesi Homeri* §108; *Pelopidas* for his own eclipse descriptions) and **Heraclitus the Allegorist** (*Quaestiones Homericae* §75) read 20.356-357 as a total solar eclipse and noted the New Moon cues.
- **Objections B&M summarise:**
  - no explicit eclipse elsewhere in the poem;
  - the scene is indoors and nobody else sees it;
  - the imagery fits Hades;
  - the lines are suspect (Page 1955);
  - B&M found no translation that footnotes an eclipse at xx.356.
- **Historical-eclipse idea:** Fotheringham (1921). The 16 April 1178 BC eclipse is attributed to **Schoch** (refs 1, 12, 13) and **Neugebauer**. Ref. 14 is **P. V. Neugebauer**, *Astronomische Chronologie* (1929). He is not O. Neugebauer, who is ref. 42, *HAMA*, cited only on Thales.
- **Abstract:** in the late 1920s Schoch and Neugebauer computed that the eclipse was total over the Ionian Islands, and the only suitable one in more than a century fitting a sack of Troy around 1192-1184 BC.

**Checked by me in the local texts:**
- **Plutarch** *De facie* 19.1 contains the eclipse discussion, including a recent noon eclipse with stars visible.
- **Heraclitus**, local 1st1K edition, **ch. 73.2**:
  - the eclipse allegory;
  - Hipparchus;
  - the Attic "old-and-new" day (ἕνη καὶ νέα);
  - Theoclymenus;
  - the waning/rising-month line.
  
  B&M's §75 uses a different numbering [B; confirmed].
- **Fotheringham 1921, pp. 16-18** (local OCR):
  - reads 14.161-162 and 19.306-307 as New Moon cues, 14.457 as a moonless evening, and 20.156 and 20.276 as the feast;
  - takes the vision as a total eclipse, citing Plutarch (*De facie* 931F) and Eustathius;
  - reports that **Herwart von Hohenburg (1612)** had already dated the return by the eclipse;
  - declines to date the Trojan War with it himself.

**Schoch (1926), *The Observatory* 49:19-21** (primary; read by me, confirming A's account in full):
- **p.19.** Quotes Od. 20.351-352 and 355-357 in Cotterill's translation, and 361-362 (the suitors mock the seer).
- **p.20, the reading.** Plutarch and the medieval commentator Eustathius took the passage as an eclipse. Fotheringham supported the reading but would not use it for dating.
- **p.20, the lunar and solar terms:**
  - From Fotheringham's Almagest occultations (MN 75:377-394, 1915): +12.24″ s² in the Moon's mean longitude.
  - From ancient solar eclipses: +9.60″ s² in the mean elongation, giving +2.64″ s² in the Sun's mean longitude.
  - A correction of -1.10″ to Newcomb's centennial solar motion.
  - Here s = Julian centuries since 1800 Jan 0.
- **p.20, the search.** With Oppolzer's *Syzygientafeln* (1881), "corrected throughout", he examined **-1240 to -1140**. Only the **total eclipse of -1177 April 16** (civil day reckoned from midnight) qualifies. The order of events in book 20 puts greatest phase **between 10 a.m. and noon**.
- **p.20, his reconstruction of Day 0 morning:**
  - sunrise 5:40;
  - the suitors' meal 10:30-12:00;
  - **Theoclymenus' warning 11:41 local mean time**;
  - slaughter in the evening.
- **p.21, the eclipse at Ithaca:**
  - It is the only solar eclipse between 10 a.m. and noon in the interval.
  - **His solar elements put the southern limit of totality through Ithaca**, with momentary totality at 11:41.
  - The only other large eclipse at Ithaca in the century was the annular eclipse of **-1182 Jan 12** (1183 BC): 11.4 digits, greatest phase 14 min after sunrise. He rejects it.
- **p.21, New Moon and chronology:**
  - New Moon is "proved" by 14.161-162 and 19.306-307.
  - The traditional return in -1172 would be five years off.
  - His chronology: Trojan War -1197 to -1187; fall of Troy -1187; wanderings -1187 to -1177; Scheria early April -1177; **Ithaca landing -1177 April 12, morning**; **slaughter -1177 April 16, 6 to 8:30 p.m.**
  - [me] His 12 April landing is Ti-4, B&M's *parallel* numbering, not the sequential Ti-5 used in the search.
- **[me]** Schoch puts Ithaca on the **southern** limit of totality. B&M's Starry Night path puts it on the **northern** edge.

**Eclipse circumstances B&M report** [Fig. 1; §Historical Plausibility; SI pp.2-3]:
- **Identity and sky:**
  - 31st eclipse of Saros 39.
  - All five naked-eye planets within an arc of less than 90°.
  - Magnitudes: Venus -4, Jupiter -1.9, Mercury -1.2, Saturn 0.16, Mars 1.3.
  - The Pleiades "crown" the hidden Sun.
- **Geometry:**
  - Greatest eclipse at 32.7°N 12.7°E; this is the Canon's point (§3.3).
  - Totality recurs at a given place about once in 370 years.
- **Exeligmos:** one exeligmos later, **18 May 1124 BC** (-1123), totality passed near Babylon (greatest eclipse 32.9°N 45.3°E).
- **Thales:**
  - 28 May 585 BC (-584);
  - one Saros earlier, **18 May 603 BC** (-602), totality passed about 220 km SE of Ur;
  - half a Saros earlier, **23 May 594 BC** (-593), a total lunar eclipse.
- **SI speculations:**
  - **14 Apr 1186 BC** (-1185): the "almost-arrival", via a 99-lunation subcycle;
  - **15 Oct 1188 BC** (-1187): an allegorical fall of Troy, with a total lunar eclipse.

---

## 12. Disagreements and how they were settled

| # | Field | A said | B said | Settled by | Verdict |
|---|---|---|---|---|---|
| 1 | Table S2 transcription | 152 rows, values and colours | 152 rows, values and colours | Cell-by-cell comparison [me] | **Identical** (0 differences in 1,976 cells). All counts in §8.1 stand. |
| 2 | Ti vs conjunction date | Matches the UT+2 date in 137/152; the misses are probably check precision or a day-boundary convention | Matches the LMT date in 138/152; no single zone works | DE441 (sub-minute accuracy) [me: `check_ti.py`, `check_ti_ra.py`] | LMT 138, UT+2 136, UT 134; RA conjunction and minimum separation are worse. Shifted and unshifted rows interleave at the same hours, so **it is not check precision. B is right**: no single rule reproduces the column. |
| 3 | 1243 BC Ti | About 2 days off (conjunction 15 Mar about 21h) | About 2.8 days from any conjunction | DE441 | Conjunction 15 Mar 1243 BC 20:49 UT+2; S2's 13 Mar is not a New Moon. Both are right; the gap is 2.4-2.9 days depending on the reference hour. |
| 4 | Operational constellation window | Ti-29 ≥ 17 Feb and Ti-12 ≤ 4 Apr, giving 18 Mar-16 Apr | "T_i-28 ≥ 17 Feb" in one place, giving 17/18 Mar-16 Apr; elsewhere Ti-29 | Primary text, §References | B&M: "Ti -29 should be between 17 February and 4 April", the whole 17 sailing days inside, sinking no later than 5 April. **A's form is correct.** In a leap year Ti may be 17 Mar if 29 Feb is counted. |
| 5 | Second qualifying New Moon | Rule unstated (no list) | 7 years: 1246, 1243, 1227, 1208, 1189, 1178, 1113 | DE441 per-year listing [me] | Two in-window New Moons in **1208, 1197 (leap), 1189, 1178, 1113**. Separately, S2's Ti lies **outside** the window in 1246, 1227 and 1243 while an in-window New Moon exists. B mixed the two categories and missed 1197. S2 lists the later New Moon in four years and the earlier one in 1189: no consistent rule. |
| 6 | MWRA definition | Ambiguous (azimuth extreme, station or GWE); 13 Mar 1178 "near the retrograde-to-direct station" | Local maximum of rising azimuth from N through E (southernmost rising point); 14/20 rows | DE441, all 152 rows [me: `check_mwra.py`] | **B confirmed**: 124/152 exact, 138/152 within ±1. Stations: 0/152 within ±1 (median -8 d). GWE: 7/152 (median +5 d). A's station remark is wrong: station 5 Mar, GWE 19 Mar 1178 BC. |
| 7 | 1157 BC Mercury | Δ: S2 -1, Table 2 0, "true value 0" | S2 -1 / Table 2 0; own MWRA 22 Feb, so Δ -3 | Table 2 image; DE441 | Both are right at different levels. Printed MWRA with true arithmetic gives 0. **The DE441 maximum is 22 Feb, so Δ = -3** (pale yellow): with a modern ephemeris the "runner-up" loses its Mercury pass. |
| 8 | Equinox flag | XXX exactly when Ti-11 ≥ 1 Apr; E count 20 (1-5 Apr) or 17 (1-4 Apr) | XXX and orange for Ti-11 in 1-6 Apr; count 22 [26] | `s2_counts.py` | Same set: the largest printed Ti-11 is 6 Apr. All counts confirmed: 22 XXX, 20 at 1-5 Apr, 17 at 1-4 Apr in the window. B&M's "one every 6 years" matches the XXX set, not their stated ≤ 4 Apr bound (new). |
| 9 | Venus colour thresholds | Smallest yellow 1:02:26 | Yellow 1:02-1:29 | `s2_counts.py` | Both right for the full table (1:02:26 is 1101 BC). Inside the window the smallest yellow is 1:06:29. |
| 10 | Clock / site | UT+2 from a sunrise fit (sd 1.6 min); latitude unconstrained | UT+2 from 3 rows; 38.4°N 20.7°E | DE441, 75 rows [me: `check_venus.py`] | UT+2 confirmed (+120.0 min, sd 1.6). The Venus-Sun consistency favours about 38.4°N (new). DE441's Venus pass set equals S2's exactly. |
| 11 | 1178 conjunction times | 18 Mar 03:20, 16 Apr 12:14 UT+2 (Meeus) | 03:26, 12:20 UT+2 (Meeus) | DE441 | 03:31 and 12:25 UT+2 with ΔT 27,602.7 s. Same dates in all cases. |
| 12 | Equinox time | not checked | 15:12 UT+2 | DE441 | 15:31 UT+2, against B&M's 15:24. |
| 13 | Parallel reckoning for 1178 | Offsets given, not evaluated | Sinking 6 Apr, breaks ≤ 5 Apr | Arithmetic plus Table 1 | B confirmed. The sailing nights also run past the 4 Apr Pleiades bound. |
| 14 | Arcturus date | 17 Feb only | 17 Feb (text) vs "end of February" (SI) | SI p.1 | B confirmed. Also new: Pleiades invisible for 40 days (text) vs 44 days (SI). |
| 15 | Hermes lines | 5.43-58 | 5.48-55 | Greek text; S1 | B&M cite "v.48 onwards", v.55 and v.97-103. S1's "v.48" quote is Greek 5.47-56. Both are acceptable; the spec uses 5.43-58 for the flight and 5.97-103 for the complaint. |
| 16 | Apollo festival lines | 20.155-156 | 20.156 | Greek text | ἑορτή is at 20.156; 20.155 is context. |
| 17 | Iliad parallel | Il. 18.485ff | Il. 18.487-489 | `iliad-grc.tsv` | Il. 18.487-489 = Od. 5.273-275 verbatim; B&M cite xviii.485. Both are acceptable. |
| 18 | Schoch 1926 (secondary for B) | Read: method, -1240 to -1140, 11:41 LMT, southern limit, -1182 Jan 12 rejected, chronology | Not read (relied on B&M) | Rendered and read by me | **A confirmed on every point checked** (§11). |
| 19 | Neugebauer (secondary for both) | P. V. Neugebauer 1929, not read | same | B&M reference list | Ref. 14 is P. V. Neugebauer, confirmed. Still not read: no free scan found. |
| 20 | Heraclitus locus | B&M §75 (reported) | ch. 73.1-73.2 in the local 1st1K text | Local text | B confirmed: the eclipse allegory is at 73.2 in the local edition. |
| 21 | Fig. 1 "12:02 p.m. local" | About 10:02 UT, about 11:25 LMT (assuming UT+2) | "Presumably UT+2" | DE441 local circumstances | Not reproducible: DE441 gives a maximum at Ithaca of 12:48 UT+2 (ΔT 27,602.7 s, magnitude 0.90) or 12:26 UT+2 (28,590 s, 0.975). The clock reading UT+2 is plausible from §3.2, but the eclipse geometry depends on ephemeris and ΔT together (§3.3). |
| 22 | New Moon count | 1683 vs B&M's 1684 | 1683 | DE441 | 1683; endpoint convention. |
| 23 | Table 2 composition | 28-row extract where "Mercury is close" | 28 years where Mercury is close | `s2_counts.py` vs image | Exactly the rows of 1250-1115 BC with \|printed Δ\| ≤ 9. The only value difference is 1157's Δ; plus the 30-Mar colours. |
| 24 | Main-paper PDF | Wayback pnas.org PDF (text layer) | SEDICI OCR scan | — | Not a content disagreement. Both agree with the PMC text I read. |
| 25 | Mercury heliacal rising 13 Mar 1178 | Reported | Reported; noted it rose 50-63 min before the Sun from 1 Mar | DE441 | Geometry nearly constant 11-14 Mar (Sun -13.1° to -13.3° at Mercury's rising). The 12 vs 13 Mar distinction is a PLSV threshold effect (new). |

---

## 13. What the paper leaves unspecified (choices a reproduction must make)

1. **What "Ti = New Moon" means.** The conjunction definition (ecliptic longitude is the best fit), the time zone and the day boundary are not stated. S2's column cannot be reproduced exactly (§5 N). A reproduction must choose one, for example the civil date of the geocentric longitude conjunction in UT+2 or in LMT. Because the bench clues shift by whole days, it should report sensitivity to that choice. 1243 BC must be corrected.
2. **Which New Moon when two qualify**, and whether out-of-window Ti (1246, 1227, 1243 BC) are allowed. S2 follows no consistent rule. Evaluate both candidates in the five two-New-Moon years.
3. **Leap days.** S2's Δ ignores 29 Feb. The constellation window's lower end moves to 17 Mar in leap years only if 29 Feb is counted.
4. **Observer site and horizon.** Only "Ithaka's latitude" is given. The data fit UT+2 at about 38.4°N 20.7°E, but Ithaca, Paliki and Kefalonia are all live options.
   - The rise definitions (refraction, h0, limb, airless or not) follow unstated Starry Night defaults.
5. **Constellation visibility model:**
   - which Pleiad or what cluster magnitude;
   - Arcturus as stand-in for Boötes;
   - PLSV extinction parameters;
   - which epoch and latitude the fixed cutoffs (17 Feb; 3, 4 or 5 Apr) were computed for;
   - whether to recompute them each year;
   - which of the three Pleiades dates to use;
   - why September is excluded (the "late-setting" reading).
6. **Mercury:**
   - MWRA is now pinned empirically as the rising-azimuth maximum from N through E, but the paper never defines it.
   - The tolerance ("a few days", decoded as ±1 to pass, ±2 and ±3 as near misses) is unstated.
   - The text's "visible" requirement was checked only for 1178.
   - The tie rule when two maxima are about equally distant from Ti-34 is unstated.
   - Results depend on the ephemeris (§8.2: 1157 drops out and 1189 enters with DE441).
7. **Venus.** The 90-min threshold and the roughly 60-min near-miss band are arbitrary. There is no altitude, magnitude or visibility test, and the reading of "high" is not fixed.
8. **Day reckoning:**
   - sequential (used) or parallel (1178 then fails both the Pleiades and Equinox bounds by one day);
   - whether a Homeric "day" starts at dawn, sunset or midnight (B&M use civil midnight dates);
   - the 14.457 "Night -2" inconsistency.
9. **The Equinox clue.** It is not applied, yet it carries the probability argument and, with DE441, the uniqueness. Its bound is given as ≤ 4, ≤ 5 or (in S2) ≤ 6 Apr.
10. **Window.** The text says 1250-1115 BC; S2 covers 1251-1100 BC. Endpoints are not stated, and the window is drawn from the same tradition as the eclipse identification.
11. **Ephemeris and ΔT.**
    - Starry Night's VSOP87/ELP-2000/82 with ΔT 27,602.7 s cannot be rerun. A ΔT value cannot be carried over to DE441 unchanged (§3.3).
    - For the clue tests, ΔT matters mainly through conjunction dates near midnight and through clock times.
    - For the eclipse track, ΔT and the lunar theory must be paired consistently: Canon 28,590 s with ELP-2000/82 corrected for ṅ, or SMH2020 with DE441.
12. **Statistics.** B&M give no null model, no independence test, no look-elsewhere correction over interpretive forks (season, Mercury variable, reckoning, thresholds, clue selection, window), and no treatment of the shared New Moon condition. The bench has to supply all of these.

---

## 14. Files

All in `results/bm2008-reconcile/`, each with its output:
- `check_ti.py` / `.out.txt`: Ti against DE441 conjunctions by time zone; the New Moon count; second qualifying New Moons.
- `check_ti_ra.py` / `.out.txt`: RA-conjunction and minimum-separation definitions.
- `s2_counts.py` / `.out.txt`: all S2 counts, colour rules, leap-day arithmetic, Table 2 membership.
- `check_mwra.py` / `.out.txt` / `.json`: MWRA candidate definitions against S2, all 152 rows.
- `check_mwra_curves.py` / `.out.txt`: rising-azimuth curves; DE441 Δ and survivors.
- `check_venus.py` / `.out.txt`: S2 clock and Venus column against DE441.
- `check_extras.py` / `.out.txt`: 1178 conjunctions, equinox, twilight, eclipse circumstances, Mercury morning geometry.

Ephemeris: `odybench/ephem.py` with `data/ephem/de441_m1320_m1030.bsp`. Pages rendered for reading Schoch are in the session scratchpad only, not in the project.
