# Almagest positive control: real records of B&M's own clue types

Written 2026-10-04 for `odybench`. This note answers issue 3 of `docs/critique-design.md` (a blocker): B&M's search uses no eclipse. Its clues are:
- a lunar phase on Day 0;
- a star season;
- a Venus morning-star rise lead;
- a Mercury turning point, at stated day offsets.

The bench therefore needs real, independently dated records of those kinds, with day intervals the text itself gives. Those records show whether a B&M-style search can recover a known date at B&M's tolerances, and how much slack an expert observer's "greatest elongation" actually carries.

> **This note contains the true dates.** The searcher reads only `data/prereg/controls_almagest.json`. That file has no absolute dates, no regnal or era years, no Egyptian months or days and no observer names. The truth is in `data/prereg/controls_almagest_truth.json`, which the searcher must never read. The DE441 excerpts in `results/controls-almagest/ephem/` span only the truth's neighbourhood (AD 120–145 and 296–224 BC). Their extents must not be used to place search windows.

**Provenance tags.**
- `[text: ref]`: a row of `data/text/ptolemy-syntaxis-grc.tsv` (Heiberg's Greek; ClassicaCodex EditionId 2977). The ref is the row key after `...1st1K-grc1.`; for example 9.7.4 is book IX, chapter 7, section 4.
- `[computed: script]`: computed by me with the named script in `results/controls-almagest/`. The output sits beside it.
- `[ctl]`: `docs/research-controls.md`. `[DESIGN]`: `DESIGN.md`. `[crit]`: `docs/critique-design.md`.
- `[secondary: …]`: a modern work I did not read for this note; I name it. `[me]`: my own inference or gloss.

**Conventions.**
- Historical BC with the astronomical year in brackets, so 262 BC is (−261).
- Proleptic Julian calendar. Civil days run from local midnight to midnight.
- Time scales are named: UT (UT1), TT, and LAT (local apparent solar time) at Alexandria (31.20°N, 29.92°E). "Equinoctial hours" are Ptolemy's.
- All calendar arithmetic is Julian Day arithmetic: `odybench.ephem.julian_from_jd` and `jd_from_julian`. Python `datetime` and `numpy.datetime64` were not used.

---

## 0. Summary

1. **Inventory.** Books IX–XI hold 43 dated planetary records `[text]`. They are:
   - 17 for Mercury and 11 for Venus;
   - 5 each for Mars, Jupiter and Saturn.

   Four dated records from other books serve as lunar and season anchors: a spring equinox (III.1.10), a lunar eclipse (IV.6.14), and two Sun–Moon elongation measurements (V.3.2, VII.2.4). All 47 are in Table 1.
2. **The dates come from the text alone.**
   - Every era is converted with Ptolemy's own equivalences (section 1.2).
   - Ptolemy states the mean Sun for 34 of the records. His own solar tables, run on my converted dates, reproduce 32 of those 34 to ≤ 0.12° `[computed: records.py]`. My date arithmetic is therefore right wherever the text is sound.
   - The two failures are textual cruxes, and both readings are carried (section 1.4):
     - IX.7.11 is one Egyptian month off.
     - IX.9.4 is three days off; the day numeral is missing in the export.
   - A third crux, the regnal year of X.1.4 (ιδʹ = 14 in the export), is settled by the mean Sun in favour of year 4.
3. **Twelve control sets** (section 3):
   - Seven are tight, spanning 4–69 days: ALM-A to ALM-F and ALM-I.
   - The other five (ALM-G, H, J, K, L) are long, with exact Egyptian-calendar intervals of 106 days to 8 years.

   Every set contains a Mercury or Venus record. Lunar records give the Moon's phase on Day 0 in ALM-A and ALM-B (and on later days in both); ALM-C has a lunar eclipse 17 days after Day 0. The composition was fixed from the text alone (dates, bodies, proximity in days) before the DE441 comparison was examined.
4. **Observer slack for "greatest elongation"** (Table 2, Summary) `[computed: slack.py]`:
   - **Mercury.** 14 records are put at or about greatest elongation. The record lies within 1 day of the DE441 greatest elongation (from the true Sun) for 3 of the 14, within 2 days for 7, and within 4 days for 12. All 14 are within 5.5 days.
   - **Venus.** 8 records are put "at greatest elongation". Only 2 lie within 2 days. The other 6 lie **16–21 days** from the true maximum. Venus's elongation stays within 1° of its maximum for 34–35 days, and observers report its "greatest elongation" anywhere on that plateau.
5. **At B&M's own ±1-day tolerance the true dates fail their own clues.**
   - 9 of the 12 sets carry an "at (about) greatest elongation" clue.
   - In only 2 of those 9 does the true date satisfy every such clue within ±1 day:
     - ALM-A, with the printed date of IX.9.4;
     - ALM-E.
   - The rest need more slack:
     - ALM-C needs 3.4 days, ALM-G 5.5, ALM-H 3.6 (with IX.7.11 emended; as printed it puts Mercury on the wrong side of the Sun) and ALM-K 2.9.
     - ALM-D, ALM-F and ALM-L need 16–21 days, because each contains a Venus record.

   So a search that requires these clues at B&M's ±1 day would reject the true date of 7 of these 9 sets: at B&M's tolerances, real records of B&M's own clue types are mostly not recoverable (critique issue 3). A Mercury turning-point clue needs about ±4–6 days and a Venus-elongation clue about ±21 days.
6. **B&M's Mercury proxy is a different event.** B&M's M criterion uses the maximum of Mercury's rising azimuth. For the 7 morning Mercury records at greatest elongation, the nearest such maximum lies between −2.5 and +31.8 days away. Only 2 of the 7 are within ±3 days (Table 2, last column).
7. **B&M's Venus clue does not discriminate near greatest elongation.** All 7 Venus morning records rise 125–220 min before the Sun. Each passes B&M's "≥ 90 min" test with a large margin.
8. **The other clue kinds are tight.**
   - Oppositions lie within 1.8 days of DE441's opposition to the true Sun and within 0.42 days of the opposition to the mean Sun (Ptolemy's definition).
   - Occultations and conjunctions with stars lie within 1.7 days.
   - Positions relative to the Moon are off by at most about 2 hours of lunar motion, and every implied lunar phase is right.
   - The IV.6.14 eclipse: DE441 puts mid-eclipse 0.02 h from Ptolemy's time, at umbral magnitude 0.84 against his 5/6 = 0.83, with the north limb eclipsed as he says.
   - The III.1.10 equinox is 0.87 days late.

---

## 1. Method

### 1.1 Text

I read every row of Books IX–XI that contains a year word. I also read every row in the whole *Syntaxis* that names Hadrian, Antoninus, Trajan, Domitian, Augustus, Philadelphus, Philometor, the Dionysian or Chaldean calendars, the Callippic periods or "the death of Alexander" (`scan_dates.py`, `scan_rulers.py`, `show.py`).

All Greek in the prereg files is copied verbatim from the TSV. Accent and prime code points vary, so `greek.py` locates each phrase modulo diacritics and returns the original substring. `build_prereg.py` re-checks every quoted piece against its row.

The export has ingest damage:
- "U+2220" stands for ∠ (½). Research-controls §4.19 also notes this.
- "??" replaces some numerals, for example "υ??α´" at 9.7.12 and "σ??δ" at 3.7.4.
- Letters are dropped in places, for example "κ ∠" for κϚ ∠ at 9.7.7 and "μοιρῶν καὶ δ´" at 9.9.4.

Each damaged item that matters is noted where it is used.

### 1.2 Calendar conversion

The day count runs from Ptolemy's epoch, **Nab 1 Thoth 1 at noon = JD 1448638 = 26 Feb 747 BC (−746)** (task brief; [ctl §4.19]). Egyptian civil days have their noon at:

    JD_noon = 1448638 + 365·(N − 1) + 30·(month − 1) + (day − 1)        (month 13 = epagomenai)

A double date "d into d+1" is the night between civil days d and d+1:
- an evening, or a time "before midnight", falls on civil day d;
- a dawn, or a time "after midnight", falls on civil day d+1.

The era years convert to Nabonassar years as follows. Each equivalence is Ptolemy's own `[text]`:

| era | Nabonassar year | where the text says so |
|---|---|---|
| years from Alexander's death ("Philip") n | 424 + n | 3.7.4 ("υκδ"); 10.9.2 (year 52 = Nab 476) |
| Hadrian n | 863 + n | 3.7.4. From Alexander's death to Augustus is 294 years (damaged "σ??δ"). From Augustus 1, Thoth 1, noon to Hadrian 17, Athyr 7 is 161 years and 66 days. Hence Hadrian 17 = Nab 880. The three Hadrianic eclipses then fall on NASA rows [ctl §4.19] |
| Antoninus n | 884 + n | 9.10.3 ("Antoninus 2 = ωπϚʹ = 886"); 10.4.6 ("to Antoninus' reign ωπδ΄"); 3.1.9 (Antoninus 3 = Philip 463) |
| Philadelphus 13 | 476 | 10.4.6 ("υος΄") |
| Dionysian and Chaldean dates | the Egyptian date Ptolemy gives in the same sentence | 9.7.9–16, 9.10.6, 10.9.2, 11.3.2, 11.7.2 |

**Worked example (IX.7.4).** Hadrian 16 is Nab 879. Phamenoth is month 7, and the record falls on day 16 in the evening. JD_noon = 1448638 + 365·878 + 30·6 + 15 = 1769303. That is 2 Feb AD 132 (Julian), noon. So the evening of 2 Feb AD 132 is the civil date `[computed: records.py; ephem.julian_from_jd]`.

### 1.3 Internal check: Ptolemy's own mean Sun

Ptolemy states the mean Sun for 34 of the records. I recomputed it from his own solar theory:
- epoch Pisces 0;45 at Nab 1 Thoth 1, noon (3.7.4: "τῶν Ἰχθύων τῆς α μοίρας ἑξηκοστὰ με");
- daily motion 0;59,8,17,13,12,31° (his tables);
- the record's day count. Evening is taken as 6 p.m. and dawn as 6 a.m.; stated hours are used as given.

**32 of the 34 agree to ≤ 0.12°**, about 3 hours of solar motion. The largest residual, IX.7.9 at 0.115°, is within Ptolemy's ⅙° rounding.

This check uses no modern astronomy. It shows that the conversion chain, including the Dionysian- and Chaldean-calendar equivalents and the damaged numeral restored in 9.7.12, reproduces Ptolemy's own bookkeeping. One gloss was corrected: at 10.1.6 "β ιε'" is 2 1/15, not 2;15. That reading reproduces both his 272.07° and his elongation of 47 8/15°.

### 1.4 Textual cruxes (both readings carried)

| record | as printed | what Ptolemy's own mean Sun implies | handling |
|---|---|---|---|
| IX.7.11 (Mercury, the horns of Taurus) | Nab 486, Phamenoth 30 into Pharmouthi 1, evening. His tables give 59.08° here | He states "Κριοῦ μοίρας κθ ∠" (Aries 29½ = 29.5°). In 9.7.13 he uses a mean-Sun difference of 33⅓° to IX.7.12, which needs Aries 29½. Mecheir 30 into Phamenoth 1, one month earlier, gives 29.51° | the interval is a fork in ALM-H: +102 as printed, +72 emended |
| IX.9.4 (Mercury, greatest morning elongation) | "Μεσορὴ εἰς τὴν κδʹ ὄρθρου": the first day numeral is missing, and the 24th gives 103.27° | He states "Καρκίνου μοίρας ῑ καὶ γ´" (Cancer 10⅓). 9.9.2 requires the mean Sun a quadrant from the apogee, as in IX.9.3. Mesore 20/21 gives 100.31° | the interval is a fork in ALM-A: +52 as printed, +49 emended |
| X.1.4 (Venus, greatest morning elongation) | "τῷ ιδʹ ἔτει Ἀντωνίνου" (year 14). Ptolemy's dated observations otherwise end in year 4 | He states Leo 5¾ = 125.75°. Year 4 (Nab 888) gives 125.70°; year 14 (Nab 898) gives 123.26° | resolved as year 4, but **kept out of every set** |

**DE441 does not decide these cruxes, and I did not let it.** For IX.7.11, DE441 has Mercury 3.7° *west* of the Sun on the printed date, so it was invisible, and 22.7° east, an evening star, on the emended date. For IX.9.4 the printed day lies 0.2 days from the true greatest elongation and the emended day 2.8 days. The text's own arithmetic and the sky therefore disagree about which IX.9.4 reading is the better observation. That is a reason to carry both, not to pick one.

Toomer's translation [secondary: Toomer 1984, *Ptolemy's Almagest*; not checked here] probably discusses all three cruxes.

### 1.5 Ephemeris and measured quantities

**Ephemeris.**
- Positions are from `odybench.ephem` (DE441, Vondrák long-term precession, IAU 2000A nutation, light-time, aberration and deflection).
- The DE441 excerpts for AD 120–145 and 296–224 BC were fetched by HTTP Range from NAIF `de441_part-1.bsp`, the same method as `tools/fetch_ephem.py` [`fetch_ephem_almagest.py`]. They are used through `ephem.use_ephemeris`.
- ΔT is `smh2020` (the Morrison et al. 2021 spline). Its stated uncertainty at these epochs is about 80–120 s (`ephem.sigma_smh2020`); that does not matter at day resolution.
- Stars are from the Hipparcos new reduction (VizieR I/311/hip2), with radial velocities from SIMBAD, fetched 2026-10-04 [`fetch_stars.py`, `stars.json`]. They are added **in memory** to `ephem.HIP_STARS`; `ephem.py` was not modified.

**Instant of each record** [`slack.py`].
- "Evening" and "dawn" are taken as the moment the Sun is 8° below the horizon. This is my convention, not a statement in the text.
- Stated equinoctial hours are local apparent time at the site.
- The site is Alexandria for every record except the three Chaldean-calendar records, where I assume Babylon (32.54°N, 44.42°E) for horizon quantities.

**Quantities.**
- **True greatest elongation (GE).** The extremum, on the stated side, of the geocentric Sun–Earth–planet angle nearest the record. It is found on a daily grid and refined continuously.
- **Mean-Sun GE.** The extremum of the planet's ecliptic longitude minus the mean longitude of the Sun (Meeus eq. 25.2). This is Ptolemy's own definition ("τῆς μέσης τοῦ ἡλίου παρόδου").
- **Plateau.** The number of days on which the elongation is within 0.5° and within 1° of its maximum.
- **Rise lead and set lag.** The rise lead is sunrise minus the planet's rise; the set lag is the planet's set minus sunset. Here h0 is −0.8333° for the Sun and −0.5667° for the planet.
- **Mercury horizon-azimuth extrema.** The daily azimuth (N through E) at rising for morning records, or at setting for evening records. The vertex of the nearest local maximum and minimum is found by a parabola through three days (critique issue 12). This is DESIGN's T0b operational definition of B&M's M.
- **Oppositions.** Times when the planet's apparent longitude minus the Sun's (true or mean) equals 180°.
- **Star relations.** The planet's offset from the star in ecliptic-of-date coordinates, or its signed distance from a line through two stars. The implied day offset is (computed − stated)/(daily rate).
- **Lunar relations.** These are topocentric at Alexandria. Each gives the Moon's elongation, its illuminated fraction, and the days since and until conjunction (`ephem.new_moons`).
- **Eclipse.** The minimum of the Moon's distance from the antisolar point. The umbral radius uses Chauvenet's 1/50 enlargement.
- **Equinox.** The apparent solar longitude of date equals 0.

### 1.6 Independent checks

- An earlier agent ran JPL Horizons (DE441) through its own code [ctl §4.19; `results/controls/run_extra.out.txt`]. It found Venus's maximum in AD 132 at 46.04° and Mercury's in AD 134 at 18.51°. My `ephem`-based run gives the same 46.04° and 18.51°. Both runs put those maxima on the same days, about 21 Feb AD 132 and 29 Sep AD 134.
- IV.6.14 reproduces Ptolemy's computed mid-eclipse time to 0.02 h and his magnitude to 0.01. The arithmetic and the instant conventions are therefore right at the hour level.

---

## 2. Inventory

Table 1 gives each record's date as stated, its observer, the stated phenomenon, the converted civil date and the mean-Sun check, where a bold **x** marks a crux. Table 1b gives what each record measures and the words for the phenomenon. "Ptolemy" means the text says "ἐτηρήσαμεν" or a similar first-person verb. "Theon" and "Timocharis" are the observers Ptolemy names. "Unnamed" means Ptolemy cites an old record without naming its observer.

**Table 1. Inventory**

| id | ref | date as stated (era; Egyptian day; time) | observer | body | stated phenomenon | civil date (Julian, astr. year) | Ptolemy mean Sun: stated / his tables |
|---|---|---|---|---|---|---|---|
| IX.7.4 | 9.7.4 | Hadrian 16; Nab 879 Phamenoth 16/17; evening | Ptolemy | mercury | evening; at greatest elongation | 2 Feb AD 132 (132) | 309.75 / 309.73 |
| IX.7.5 | 9.7.5 | Hadrian 18; Nab 881 Epiphi 18/19; dawn | Ptolemy | mercury | morning; at greatest elongation | 4 Jun AD 134 (134) | 70.00 / 69.99 |
| IX.7.6 | 9.7.6 | Antoninus 1; Nab 885 Epiphi 20/21; evening | Ptolemy | mercury | evening; at greatest elongation | 4 Jun AD 138 (138) | 70.50 / 70.49 |
| IX.7.7 | 9.7.7 | Antoninus 4; Nab 888 Phamenoth 18/19; dawn | Ptolemy | mercury | morning; at greatest elongation | 2 Feb AD 141 (141) | 310.00 / 310.01 |
| IX.7.9 | 9.7.9 | Dionysian 23 Hydron 29 = Nab 486 Choiak 17/18; Nab 486 Choiak 17/18; dawn | unnamed | mercury | morning; star relation (Ptolemy: near GE) | 12 Feb 262 BC (-261) | 318.17 / 318.05 |
| IX.7.11 | 9.7.11 | Dionysian 23 Tauron 4 = Nab 486 Phamenoth 30/Pharmouthi 1; Nab 486 Phamenoth 30/Pharmouthi 1; evening | unnamed | mercury | evening; star relation (Ptolemy: near GE) | 25 May 262 BC (-261); emended 25 Apr 262 BC (-261) | 29.50 / 59.08 **x** |
| IX.7.12 | 9.7.12 | Dionysian 28 Didymon 7 = Nab 491 Pharmouthi 5/6; Nab 491 Pharmouthi 5/6; evening | unnamed | mercury | evening; star relation (Ptolemy: near GE) | 28 May 257 BC (-256) | 62.83 / 62.79 |
| IX.7.14 | 9.7.14 | Dionysian 24 Leonton 28 = Nab 486 Payni 30; Nab 486 Payni 30; evening | unnamed record, reduced by Hipparchus | mercury | evening; star relation (Ptolemy: near GE) | 23 Aug 262 BC (-261) | 147.83 / 147.79 |
| IX.7.15 | 9.7.15 | Chaldean 75 Dios 14 = Nab 512 Thoth 9/10; Nab 512 Thoth 9/10; dawn | unnamed | mercury | morning; star relation (Ptolemy: near GE) | 30 Oct 237 BC (-236) | 215.17 / 215.14 |
| IX.7.16 | 9.7.16 | Chaldean 67 Apellaios 5 = Nab 504 Thoth 27/28; Nab 504 Thoth 27/28; dawn | unnamed | mercury | morning; star relation (Ptolemy: near GE) | 19 Nov 245 BC (-244) | 234.83 / 234.82 |
| IX.8.3 | 9.8.3 | Hadrian 19; Nab 882 Athyr 14/15; dawn | Ptolemy | mercury | morning; about greatest elongation | 3 Oct AD 134 (134) | 189.25 / 189.25 |
| IX.8.4 | 9.8.4 | Hadrian 19; Nab 882 Pachon 19; evening | Ptolemy | mercury | evening; about greatest elongation | 5 Apr AD 135 (135) | 11.08 / 11.10 |
| IX.9.3 | 9.9.3 | Hadrian 14; Nab 877 Mesore 18; evening | Theon | mercury | evening; at greatest elongation | 4 Jul AD 130 (130) | 100.08 / 100.04 |
| IX.9.4 | 9.9.4 | Antoninus 2; Nab 886 Mesore 23/24; dawn | Ptolemy | mercury | morning; at greatest elongation | 8 Jul AD 139 (139); emended 5 Jul AD 139 (139) | 100.33 / 103.27 **x** |
| IX.10.3 | 9.10.3 | Antoninus 2; Nab 886 Epiphi 2/3; 4.5 h before midnight | Ptolemy | mercury | evening; before greatest elongation | 17 May AD 139 (139) | 52.57 / 52.57 |
| IX.10.6a | 9.10.6 | Dionysian 21 Scorpion 22 = Nab 484 Thoth 18/19; Nab 484 Thoth 18/19; dawn | unnamed | mercury | morning; before greatest elongation | 15 Nov 265 BC (-264) | 230.83 / 230.82 |
| IX.10.6b | 9.10.6 | Dionysian 21 Scorpion 26 (= 4 days after IX.10.6a, i.e. Nab 484 Thoth 22/23); Nab 484 Thoth 22/23; dawn | unnamed | mercury | morning; position (star / Moon) | 19 Nov 265 BC (-264) | – |
| X.1.3 | 10.1.3 | Hadrian 16; Nab 879 Pharmouthi 21/22; evening | Theon | venus | evening; at greatest elongation | 8 Mar AD 132 (132) | 344.25 / 344.23 |
| X.1.4 | 10.1.4 | Antoninus 4 (export reads ιδʹ = 14; see note); Nab 888 Thoth 11/12; dawn | Ptolemy | venus | morning; at greatest elongation | 30 Jul AD 140 (140) | 125.75 / 125.70 |
| X.1.5 | 10.1.5 | Hadrian 12; Nab 875 Athyr 21/22; dawn | Theon | venus | morning; at greatest elongation | 12 Oct AD 127 (127) | 197.87 / 197.85 |
| X.1.6 | 10.1.6 | Hadrian 21; Nab 884 Mecheir 9/10; evening | Ptolemy | venus | evening; at greatest elongation | 25 Dec AD 136 (136) | 272.07 / 272.05 |
| X.2.3 | 10.2.3 | Hadrian 13; Nab 876 Epiphi 2/3; dawn | Theon | venus | morning; at greatest elongation | 20 May AD 129 (129) | 55.40 / 55.43 |
| X.2.4 | 10.2.4 | Hadrian 21; Nab 884 Tybi 2/3; evening | Ptolemy | venus | evening; at greatest elongation | 18 Nov AD 136 (136) | 235.50 / 235.58 |
| X.3.2a | 10.3.2 | Hadrian 18; Nab 881 Pharmouthi 2/3; dawn | Ptolemy | venus | morning; at greatest elongation | 18 Feb AD 134 (134) | 325.50 / 325.51 |
| X.3.2b | 10.3.2 | Antoninus 3; Nab 887 Pharmouthi 4/5; evening | Ptolemy | venus | evening; at greatest elongation | 18 Feb AD 140 (140) | 325.50 / 325.53 |
| X.4.3 | 10.4.3 | Antoninus 2; Nab 886 Tybi 29/30; 4.75 h after midnight | Ptolemy | venus | morning; after greatest elongation | 16 Dec AD 138 (138) | 262.15 / 262.15 |
| X.4.6a | 10.4.6 | Philadelphus 13 = Nab 476; Nab 476 Mesore 17/18; dawn | Timocharis | venus | morning; conjunction / occultation | 12 Oct 272 BC (-271) | 197.05 / 197.04 |
| X.4.6b | 10.4.6 | 4 days after X.4.6a (Nab 476 Mesore 21/22); Nab 476 Mesore 21/22; dawn | Timocharis | venus | morning; position (star / Moon) | 16 Oct 272 BC (-271) | 200.98 / 200.98 |
| X.7.3a | 10.7.3 | Hadrian 15; Nab 878 Tybi 26/27; 1 h after midnight | Ptolemy | mars | opposition to mean Sun | 15 Dec AD 130 (130) | – |
| X.7.3b | 10.7.3 | Hadrian 19; Nab 882 Pharmouthi 6/7; 3 h before midnight | Ptolemy | mars | opposition to mean Sun | 21 Feb AD 135 (135) | – |
| X.7.3c | 10.7.3 | Antoninus 2; Nab 886 Epiphi 12/13; 2 h before midnight | Ptolemy | mars | opposition to mean Sun | 27 May AD 139 (139) | – |
| X.8.2 | 10.8.2 | Antoninus 2; Nab 886 Epiphi 15/16; 3 h before midnight | Ptolemy | mars | position (star / Moon) | 30 May AD 139 (139) | 65.45 / 65.44 |
| X.9.2 | 10.9.2 | Dionysian 13 Aigon 25 = Philip 52 = Nab 476 Athyr 20/21; Nab 476 Athyr 20/21; dawn | unnamed | mars | conjunction / occultation | 18 Jan 272 BC (-271) | 293.90 / 293.87 |
| XI.1.2a | 11.1.2 | Hadrian 17; Nab 880 Epiphi 1/2; 1 h before midnight | Ptolemy | jupiter | opposition to mean Sun | 17 May AD 133 (133) | – |
| XI.1.2b | 11.1.2 | Hadrian 21; Nab 884 Phaophi 13/14; 2 h before midnight | Ptolemy | jupiter | opposition to mean Sun | 31 Aug AD 136 (136) | – |
| XI.1.2c | 11.1.2 | Antoninus 1; Nab 885 Athyr 20/21; 5 h after midnight | Ptolemy | jupiter | opposition to mean Sun | 8 Oct AD 137 (137) | – |
| XI.2.2 | 11.2.2 | Antoninus 2; Nab 886 Mesore 26/27; 5 h after midnight | Ptolemy | jupiter | position (star / Moon) | 11 Jul AD 139 (139) | 106.18 / 106.18 |
| XI.3.2 | 11.3.2 | Dionysian 45 Parthenon 10 = Philip 83 (Nab 507) Epiphi 17/18; Nab 507 Epiphi 17/18; dawn | unnamed | jupiter | conjunction / occultation | 4 Sep 241 BC (-240) | 159.93 / 159.93 |
| XI.5.2a | 11.5.2 | Hadrian 11; Nab 874 Pachon 7/8; evening | Ptolemy | saturn | opposition to mean Sun | 26 Mar AD 127 (127) | – |
| XI.5.2b | 11.5.2 | Hadrian 17; Nab 880 Epiphi 18; 4 h after noon | Ptolemy | saturn | opposition to mean Sun | 3 Jun AD 133 (133) | – |
| XI.5.2c | 11.5.2 | Hadrian 20; Nab 883 Mesore 24; noon | Ptolemy | saturn | opposition to mean Sun | 8 Jul AD 136 (136) | – |
| XI.6.2 | 11.6.2 | Antoninus 2; Nab 886 Mecheir 6/7; 4 h before midnight | Ptolemy | saturn | position (star / Moon) | 22 Dec AD 138 (138) | 268.68 / 268.69 |
| XI.7.2 | 11.7.2 | Chaldean 82 Xanthikos 5 = Nab 519 Tybi 14; Nab 519 Tybi 14; evening | unnamed | saturn | position (star / Moon) | 1 Mar 229 BC (-228) | 336.17 / 336.15 |
| III.1.10 | 3.1.10 | Philip 463 (= Antoninus 3, 3.1.9) = Nab 887; Nab 887 Pachon 7; 1 h after noon | Ptolemy | sun | spring equinox | 22 Mar AD 140 (140) | – |
| IV.6.14 | 4.6.14 | Hadrian 19; Nab 882 Choiak 2/3; 1 h before midnight | Ptolemy | moon | lunar eclipse | 20 Oct AD 134 (134) | – |
| V.3.2 | 5.3.2 | Antoninus 2; Nab 886 Phamenoth 25; 5.25 h before noon | Ptolemy | moon | Sun-Moon distance | 9 Feb AD 139 (139) | 316.45 / 316.44 |
| VII.2.4 | 7.2.4 | Antoninus 2; Nab 886 Pharmouthi 9; 5.5 h after noon | Ptolemy | moon | Sun-Moon distance | 23 Feb AD 139 (139) | – |

Mean-Sun statements reproduced to <= 0.12 deg: 32 of 34.

**Table 1b. What each record measures, and the words for the phenomenon**

| id | what is measured / stated | phenomenon words |
|---|---|---|
| IX.7.4 | astrolabe longitude of Mercury (Pisces 1) against Aldebaran; greatest elongation from the mean sun 21 1/4 deg | τὸ πλεῖστον ἀποστάντα τῆς μέσης τοῦ ἡλίου παρόδου |
| IX.7.5 | astrolabe longitude (Taurus 18 3/4); Mercury 'very faint and dim'; elongation from mean sun 21 1/4 | ἐπὶ τῆς μεγίστης ὢν ἀποστάσεως |
| IX.7.6 | astrolabe longitude (Cancer 7) against Regulus; elongation from mean sun 26 1/2 | τὸ πλεῖστον ἀποστάντα τῆς τοῦ ἡλίου μέσης παρόδου |
| IX.7.7 | astrolabe longitude (Capricorn 13 1/2) against Antares; elongation from mean sun 26 1/2 (export prints 'κ ∠' = 20 1/2 but says 'τῶν ἴσων', equal to 9.7.6's 26 1/2, and 310-283.5 = 26.5: a dropped Ϛ) | πάλιν ἐπὶ τῆς μεγίστης ὢν ἀποστάσεως |
| IX.7.9 | Mercury relative to delta Cap; Ptolemy treats it as a greatest morning elongation (25 5/6 from mean sun) | ἑῷος ὁ Στίλβων |
| IX.7.11 | Mercury relative to the horns of Taurus; Ptolemy uses it (with 9.7.12) to interpolate an evening elongation (longitude numeral damaged in the export: 'Ταύρου μοίρας ἄγ ??') | ἑσπέρας |
| IX.7.12 | Mercury relative to the heads of Gemini; evening elongation 26 1/2 from mean sun | ἑσπέρας |
| IX.7.14 | Mercury relative to Spica (reduced by Hipparchus); evening elongation 21 2/3 from mean sun (fraction damaged in export: 'κα ??') | ἑσπέρας |
| IX.7.15 | Mercury relative to alpha Lib; morning elongation 21 from mean sun | ἑῷος ἐπάνω ἦν τοῦ νοτίου Ζυγοῦ πήχεως ἥμισυ |
| IX.7.16 | Mercury relative to beta Sco; morning elongation 22 1/2 from mean sun | ἑῷος ἐπάνω ἦν τοῦ βορείου μετώπου τοῦ Σκορπίου πήχεως ἥμισυ |
| IX.8.3 | astrolabe longitude (Virgo 20 1/5) against Regulus; elongation 19 1/20 from mean sun | ἑῷος ὁ τοῦ Ἑρμοῦ περὶ τὴν μεγίστην τυγχάνων ἀπόστασιν |
| IX.8.4 | astrolabe longitude (Taurus 4 1/3) against Aldebaran; elongation 23 1/4 from mean sun | περὶ τὴν μεγίστην πάλιν ὢν ἀπόστασιν |
| IX.9.3 | Mercury 3 5/6 deg east of Regulus; evening elongation 26 1/4 from mean sun | τὸ πλεῖστον, φησίν, ἀπέστη τοῦ ἡλίου |
| IX.9.4 | astrolabe longitude (Gemini 20 1/12) against Aldebaran; morning elongation 20 1/4 from mean sun (numeral damaged) | τηροῦντες τὴν μεγίστην αὐτοῦ διάστασιν |
| IX.10.3 | astrolabe longitude of Mercury against Regulus and its distance from the Moon; Moon's apparent place computed by Ptolemy | μηδέπω ἐπὶ τὴν μεγίστην ἑσπερίαν ἀπόστασιν ἐληλυθότα |
| IX.10.6a | Mercury relative to the forehead of Scorpius; Ptolemy: not yet at greatest morning elongation | ἑῷος ὁ Στίλβων |
| IX.10.6b | Mercury relative to the same line, 4 days later (the interval is stated) | τῆς αὐτῆς εὐθείας διεῖχεν εἰς τὰ ἑπόμενα ὅλην καὶ ἡμίσειαν σελήνην |
| X.1.3 | Venus relative to the Pleiades; evening elongation 47 1/4 from mean sun | ὁ τῆς Ἀφροδίτης ἑσπέριος τὸ πλεῖστον ἀπέστη τοῦ ἡλίου |
| X.1.4 | Venus relative to a Gemini star; morning elongation 47 1/4 from mean sun | τὸν τῆς Ἀφροδίτης ἑῷον τὸ πλεῖστον ἀποστάντα τοῦ ἡλίου |
| X.1.5 | Venus relative to beta Vir; morning elongation 47 8/15 from mean sun | ὁ τῆς Ἀφροδίτης ἑῷος τὸ πλεῖστον ἀπέστη τοῦ ἡλίου |
| X.1.6 | Venus relative to an Aquarius star; evening elongation 47 8/15 from mean sun | ἐτηρήσαμεν τὸν τῆς Ἀφροδίτης τὸ πλεῖστον ἀποστάντα τοῦ ἡλίου |
| X.2.3 | Venus relative to Aries stars; morning elongation 44 4/5 from mean sun | ἑῷος ὁ τῆς Ἀφροδίτης τὸ πλεῖστον ἀπέστη τοῦ ἡλίου |
| X.2.4 | astrolabe longitude (Capricorn 12 5/6) against the stars in Capricorn's horns; evening elongation 47 1/3 from mean sun | τὸν τῆς Ἀφροδίτης τὸ πλεῖστον ἀποστάντα τοῦ ἡλίου |
| X.3.2a | astrolabe longitude (Capricorn 11 7/12) against Antares; morning elongation 43 11/12 from mean sun | καθʼ ἣν ἑῷος ὁ τῆς Ἀφροδίτης τὸ πλεῖστον ἀπέστη τοῦ ἡλίου |
| X.3.2b | astrolabe longitude (Aries 10 5/6) against Aldebaran; evening elongation 48 1/3 from mean sun | τὸ πλεῖστον ὁ τῆς Ἀφροδίτης ἀπέσχεν τοῦ ἡλίου |
| X.4.3 | astrolabe longitude of Venus against Spica; alignment with beta Sco and the Moon | τὸν τῆς Ἀφροδίτης ἀστέρα μετὰ τὴν μεγίστην ἑῴαν ἀπόστασιν |
| X.4.6a | Venus-star conjunction at the 12th hour (dawn); Ptolemy: Venus already past greatest morning elongation | ὁ τῆς Ἀφροδίτης ἐφαίνετο κατειληφὼς τὸν ἀντικείμενον τῷ Προτρυγητῆρι ἀκριβῶς |
| X.4.6b | Venus' longitude 4 days later (Ptolemy's conversion of Timocharis' report); used to show Venus past greatest elongation | ἐπεῖχεν κατὰ τὰς ἡμετέρας ἀρχὰς Παρθένου μοίρας η U+2220΄γ΄ |
| X.7.3a | opposition to the mean sun, time and place reduced from astrolabe observations | τριῶν ἀκρωνύκτων τῶν πρὸς τὴν μέσην τοῦ ἡλίου πάροδον διαμέτρων |
| X.7.3b | opposition to the mean sun (reduced) | τριῶν ἀκρωνύκτων τῶν πρὸς τὴν μέσην τοῦ ἡλίου πάροδον διαμέτρων |
| X.7.3c | opposition to the mean sun (reduced) | τριῶν ἀκρωνύκτων τῶν πρὸς τὴν μέσην τοῦ ἡλίου πάροδον διαμέτρων |
| X.8.2 | astrolabe longitude of Mars against Spica and its distance from the Moon, about 3 days after the third opposition | μετὰ γ ἔγγιστα ἡμέρας τῆς γ΄ ἀκρωνύκτου |
| X.9.2 | Mars-star occultation (morning) | ἑῷος ὁ τοῦ Ἄρεως τῷ βορείῳ μετώπῳ τοῦ Σκορπίου ἐδόκει ἐπιπροσθετηκέναι |
| XI.1.2a | opposition to the mean sun (reduced) | γ ἀκρωνύκτους διαμέτρους πρὸς τὴν μέσην τοῦ ἡλίου πάροδον |
| XI.1.2b | opposition to the mean sun (reduced) | γ ἀκρωνύκτους διαμέτρους πρὸς τὴν μέσην τοῦ ἡλίου πάροδον |
| XI.1.2c | opposition to the mean sun (reduced) | γ ἀκρωνύκτους διαμέτρους πρὸς τὴν μέσην τοῦ ἡλίου πάροδον |
| XI.2.2 | astrolabe longitude of Jupiter against Aldebaran and relative to the Moon, before sunrise | πρὸ τῆς τοῦ ἡλίου ἀνατολῆς |
| XI.3.2 | Jupiter-star occultation (morning) | ὁ τοῦ Διὸς ἀστὴρ ἑῷος ἐπεκάλυψεν τὸν νότιον Ὄνον |
| XI.5.2a | opposition to the mean sun | τρεῖς ἀκρωνύκτους στάσεις τοῦ ἀστέρος πρὸς τὴν μέσην τοῦ ἡλίου πάροδον διαμέτρους |
| XI.5.2b | opposition to the mean sun, time computed by Ptolemy | τὸν δὲ τῆς ἀκριβοῦς διαμετρήσεως χρόνον καὶ τόπον συνελογισάμεθα |
| XI.5.2c | opposition to the mean sun, time computed by Ptolemy | τὸν μὲν χρόνον τῆς ἀκριβοῦς διαμετρήσεως ὡσαύτως ἐπελογισάμεθα |
| XI.6.2 | astrolabe longitude of Saturn against Aldebaran and relative to the Moon | ὁ τοῦ Κρόνου ἀστὴρ πρὸς μὲν τὴν λαμπρὰν Ὑάδα διοπτευόμενος |
| XI.7.2 | Saturn relative to gamma Vir (evening) | ὁ τοῦ Κρόνου ἀστὴρ ὑποκάτω ἦν τοῦ νοτίου ὤμου τῆς Παρθένου δακτύλους β |
| III.1.10 | spring equinox (observed with the equinoctial ring / meridian instruments) | ἐαρινὴν ἰσημερίαν εὑρίσκομεν γεγενημένην |
| IV.6.14 | lunar eclipse, 1/2 + 1/3 of the diameter from the north; mid-eclipse computed | ἐξέλειπεν ἀπʼ ἄρκτων τὸ U+2220ʹ καὶ γʹ τῆς διαμέτρου |
| V.3.2 | astrolabe sighting of Sun and Moon in daylight | ὡς τεταρτημορίου τυγχάνειν ἔγγιστα τὴν μέσην ἀποχὴν τοῦ ἡλίου |
| VII.2.4 | astrolabe Sun-Moon distance at sunset (then Regulus vs Moon half an hour later) | τὴν φαινομένην σελήνην ἀπέχουσαν τοῦ ἡλίου |

Observations on the inventory `[me]`:
- **Ptolemy reduced some of these records.**
  - The outer-planet "observations" X.7.3, XI.1.2 and XI.5.2 are oppositions to the mean Sun that Ptolemy reduced from astrolabe sightings ("προσεπιλογισάμενοι", 10.7.2). Two of Saturn's are explicitly computed ("συνελογισάμεθα", "ἐπελογισάμεθα", 11.5.2).
  - The eclipse mid-time in IV.6.14 is also computed ("ἐπελογισάμεθα").
  - These are expert reductions, not raw sightings. Their tight slack (Table 3) reflects that.
- **The "greatest elongation" status of the old Mercury records is Ptolemy's classification.** The records themselves (IX.7.9–16) say only that Mercury was a morning or evening star relative to stars. Ptolemy files them as "τῶν παλαιῶν τῶν περὶ τὰς μεγίστας ἀποστάσεις τετηρημένων" (9.7.8). In the clue file that status is therefore a fork, and the primary reading is "visible only".
- **Some records state that the planet was not at greatest elongation.** IX.10.3 and IX.10.6a say "not yet at greatest elongation"; X.4.3 and X.4.6a say "past greatest elongation". DE441 agrees with every one of these four statements (Table 2).

---

## 3. The control sets

**Rules.**
- A set has 2–4 records.
- The records lie within about 40–70 days of one another, or have exact Egyptian-calendar intervals up to a few years.
- At least one record is of Mercury or Venus.
- Where the text has one, a lunar or eclipse record is included.
- No set is chosen for how well it fits DE441. The composition was fixed from the dates and bodies alone.
- Within a set, each record carries a `day_offset` from the anchor record (Day 0) in civil days, computed from the stated Egyptian dates.

**The clue file** has 72 rows: 12 sets, 6 kinds of row (interval, planet, star, moon-phase, eclipse-lunar, season).

**What the clue file withholds and why.**
- The interval rows withhold the Egyptian date words. A wandering-calendar date (month and day) combined with *any* season clue fixes the absolute year modulo about 1,460 years. The regnal year would then fix it outright.
- The Greek date words are in the truth file.
- The zodiacal longitudes and elongation magnitudes Ptolemy states are not used as clues, because B&M's grammar has no coordinates. Each such row says so.
- Phases inferred from the Moon's proximity to a planet are forks with a `none` option.

**Format.** The schema follows `data/prereg/controls_real.json`:
- each fork option has `operational` parameters and exactly one has `primary: true`;
- `window_width_years` is 136, B&M's own width;
- the harness places each window at random around the anchor.

**Set table.**

| set | anchor (Day 0) | other records (day offset) | span (d) | rows by kind | observer place | true Day 0 (proleptic Julian) |
|---|---|---|---|---|---|---|
| ALM-A | IX.10.3 | X.8.2 (+13), IX.9.4 (+52; emended +49), XI.2.2 (+55) | 55 | interval 3, moon-phase 3, planet 4 | Alexandria for IX.10.3 and XI.2.2 (stated); unstated for X.8.2 and IX.9.4 | 17 May AD 139 (astronomical 139), proleptic Julian |
| ALM-B | X.4.3 | XI.6.2 (+6), V.3.2 (+55), VII.2.4 (+69) | 69 | interval 3, moon-phase 4, planet 1, star 1 | Alexandria (stated in all four rows) | 16 Dec AD 138 (astronomical 138), proleptic Julian |
| ALM-C | IX.8.3 | IV.6.14 (+17) | 17 | eclipse-lunar 1, interval 1, planet 1 | Alexandria for the eclipse (4.6.13 introduces the three eclipses as observed there); unstated for IX.8.3 | 3 Oct AD 134 (astronomical 134), proleptic Julian |
| ALM-D | IX.7.4 | X.1.3 (+35) | 35 | interval 1, planet 2, star 1 | unstated | 2 Feb AD 132 (astronomical 132), proleptic Julian |
| ALM-E | X.3.2b | III.1.10 (+33) | 33 | interval 1, planet 1, season 1 | unstated | 18 Feb AD 140 (astronomical 140), proleptic Julian |
| ALM-F | X.2.4 | X.1.6 (+37) | 37 | interval 1, planet 2, star 1 | unstated | 18 Nov AD 136 (astronomical 136), proleptic Julian |
| ALM-G | X.3.2a | IX.7.5 (+106) | 106 | interval 1, planet 2 | unstated | 18 Feb AD 134 (astronomical 134), proleptic Julian |
| ALM-H | IX.7.9 | IX.7.11 (+102; emended +72), IX.7.14 (+192) | 192 | interval 2, planet 3, star 4 | unstated (the calendar a record is dated in is not a place statement) | 12 Feb 262 BC (astronomical -261), proleptic Julian |
| ALM-I | IX.10.6a | IX.10.6b (+4) | 4 | interval 1, planet 1, star 3 | unstated | 15 Nov 265 BC (astronomical -264), proleptic Julian |
| ALM-J | X.9.2 | X.4.6a (+267), X.4.6b (+271) | 271 | interval 2, planet 3, star 2 | unstated | 18 Jan 272 BC (astronomical -271), proleptic Julian |
| ALM-K | IX.7.16 | XI.3.2 (+1385), IX.7.15 (+2902) | 2902 | interval 2, planet 3, star 3 | unstated (the calendar a record is dated in is not a place statement; two of the three records may come from a Mesopotamian archive - an inference, not a clue) | 19 Nov 245 BC (astronomical -244), proleptic Julian |
| ALM-L | X.1.5 | X.2.3 (+586), IX.9.3 (+996) | 996 | interval 2, planet 3, star 2 | unstated | 12 Oct AD 127 (astronomical 127), proleptic Julian |

**What each set tests, in B&M's terms** `[me]`:
- **ALM-A** is the closest analogue of B&M's set:
  - a young Moon beside an evening Mercury that has not yet reached greatest elongation (Day 0; Moon 1.97 days old);
  - a near-full Moon beside Mars (+13);
  - Mercury at greatest morning elongation (+52, or +49 under the crux);
  - an old crescent beside Jupiter before sunrise (+55; conjunction 2.6 days later).
- **ALM-B**:
  - a waning crescent beside Venus, which is a morning star past greatest elongation (Day 0; conjunction 3.7 days later);
  - a waxing crescent beside Saturn (+6);
  - last quarter (+55) and first quarter (+69).
- **ALM-C**: Mercury at about greatest morning elongation, then a partial lunar eclipse 17 days later.
- **ALM-D**: a Mercury and a Venus greatest elongation 35 days apart.
- **ALM-E**: a Venus greatest elongation with a spring equinox 33 days later. This is the only "season" clue available: the *Almagest* has no dated heliacal star phases.
- **ALM-F**: two Venus "greatest elongations" 37 days apart in a single apparition.
- **ALM-G to ALM-L**: long sets. ALM-H, ALM-I and ALM-K test Mercury-near-star relations from the 3rd-century BC records.

**Overlap with `controls_real.json`.** IV.6.14 is also used in the sibling file's R-PTOL-ALEX set. A gate that counts both sets must not count that eclipse twice as independent evidence.

The sibling file also takes a different approach: it carries the Egyptian dates in its clue rows with a free offset. This file withholds them (see above).

---

## 4. Observer slack against DE441

**Table 2. Mercury and Venus: offset of the record from the DE441 event (days, record minus event)**

| id | reading | stated | elong. at record (deg) | true GE (deg) | rec − true GE | rec − mean-Sun GE | short of max (deg) | days within 0.5 / 1 deg of max | rise lead / set lag (min) | Mercury horizon-azimuth: rec − nearest max / min |
|---|---|---|---|---|---|---|---|---|---|---|
| IX.7.4 | printed | evening, at greatest elongation | +18.09 | +18.16 | **+1.1** | +1.1 | 0.07 | 5 / 8 | set lag 86 | -8.3 / +34.5 |
| IX.7.5 | printed | morning, at greatest elongation | -20.18 | -21.32 | **-5.5** | -6.2 | 1.14 | 7 / 11 | rise lead 55 | +6.2 / -29.8 |
| IX.7.6 | printed | evening, at greatest elongation | +25.64 | +26.07 | **-4.2** | -3.6 | 0.43 | 9 / 13 | set lag 117 | +9.0 / -28.7 |
| IX.7.7 | printed | morning, at greatest elongation | -27.01 | -27.02 | **+0.8** | +1.1 | 0.01 | 10 / 14 | rise lead 96 | -2.2 / +26.7 |
| IX.7.9 | printed | morning, star relation (Ptolemy: near GE) | -27.33 | -27.65 | **-3.6** | -3.4 | 0.32 | 9 / 14 | rise lead 93 | -2.5 / +26.5 |
| IX.7.11 | printed | evening, star relation (Ptolemy: near GE) | -3.73 | +23.05 | **+26.8** | +27.1 | 19.32 | 7 / 11 | set lag -12 | +22.3 / -9.5 |
| IX.7.11 | emended | evening, star relation (Ptolemy: near GE) | +22.72 | +23.05 | **-3.3** | -2.9 | 0.34 | 7 / 11 | set lag 111 | -7.7 / -39.5 |
| IX.7.12 | printed | evening, star relation (Ptolemy: near GE) | +25.43 | +25.46 | **+1.1** | +1.7 | 0.03 | 9 / 12 | set lag 118 | +7.5 / -28.5 |
| IX.7.14 | printed | evening, star relation (Ptolemy: near GE) | +26.03 | +26.18 | **-2.7** | -2.3 | 0.15 | 10 / 14 | set lag 63 | -38.5 / -15.3 |
| IX.7.15 | printed | morning, star relation (Ptolemy: near GE) | -19.79 | -20.09 | **+2.9** | +3.2 | 0.30 | 7 / 10 | rise lead 94 | +31.8 / +9.1 |
| IX.7.16 | printed | morning, star relation (Ptolemy: near GE) | -21.75 | -21.86 | **-1.8** | -1.4 | 0.10 | 8 / 12 | rise lead 105 | +29.5 / +6.8 |
| IX.8.3 | printed | morning, about greatest elongation | -17.98 | -18.51 | **+3.4** | +3.6 | 0.54 | 6 / 8 | rise lead 83 | +31.0 / +7.4 |
| IX.8.4 | printed | evening, about greatest elongation | +20.67 | +20.78 | **+1.6** | +1.9 | 0.11 | 7 / 9 | set lag 98 | -6.1 / -36.0 |
| IX.9.3 | printed | evening, at greatest elongation | +27.25 | +27.25 | **-0.1** | +0.6 | 0.00 | 9 / 13 | set lag 97 | +25.8 / -18.2 |
| IX.9.4 | printed | morning, at greatest elongation | -19.33 | -19.33 | **+0.2** | -0.4 | 0.00 | 7 / 9 | rise lead 78 | +15.7 / -12.0 |
| IX.9.4 | emended | morning, at greatest elongation | -18.94 | -19.33 | **-2.8** | -3.4 | 0.39 | 7 / 9 | rise lead 72 | +12.7 / -15.0 |
| IX.10.3 | printed | evening, before greatest elongation | +24.29 | +24.70 | **-3.9** | -3.4 | 0.41 | 9 / 12 | set lag 118 | +0.1 / -35.7 |
| IX.10.6a | printed | morning, before greatest elongation | -17.14 | -22.24 | **-10.5** | -10.0 | 5.10 | 8 / 12 | rise lead 82 | +21.5 / -1.3 |
| IX.10.6b | printed | morning, position (star / Moon) | -20.62 | -22.24 | **-6.5** | -6.0 | 1.62 | 8 / 12 | rise lead 99 | +25.5 / +2.7 |
| X.1.3 | printed | evening, at greatest elongation | +44.97 | +46.04 | **+16.1** | +15.9 | 1.07 | 25 / 35 | set lag 212 | – |
| X.1.4 | printed | morning, at greatest elongation | -44.59 | -45.81 | **+20.6** | +16.2 | 1.22 | 24 / 34 | rise lead 194 | – |
| X.1.5 | printed | morning, at greatest elongation | -45.51 | -46.45 | **+18.3** | +19.5 | 0.93 | 25 / 34 | rise lead 211 | – |
| X.1.6 | printed | evening, at greatest elongation | +46.11 | +47.24 | **+16.7** | +11.6 | 1.13 | 25 / 35 | set lag 215 | – |
| X.2.3 | printed | morning, at greatest elongation | -44.94 | -45.87 | **+17.8** | +13.6 | 0.93 | 24 / 34 | rise lead 125 | – |
| X.2.4 | printed | evening, at greatest elongation | +46.13 | +47.24 | **-20.3** | -25.4 | 1.11 | 25 / 35 | set lag 180 | – |
| X.3.2a | printed | morning, at greatest elongation | -46.55 | -46.56 | **+1.9** | +2.6 | 0.01 | 24 / 34 | rise lead 168 | – |
| X.3.2b | printed | evening, at greatest elongation | +46.08 | +46.09 | **-0.6** | -1.0 | 0.00 | 25 / 35 | set lag 215 | – |
| X.4.3 | printed | morning, after greatest elongation | -46.39 | -46.94 | **+13.5** | +18.4 | 0.54 | 24 / 34 | rise lead 220 | – |
| X.4.6a | printed | morning, conjunction / occultation | -41.57 | -46.22 | **+45.6** | +44.7 | 4.65 | 24 / 34 | rise lead 194 | – |
| X.4.6b | printed | morning, position (star / Moon) | -40.89 | -46.22 | **+49.6** | +48.7 | 5.34 | 24 / 34 | rise lead 190 | – |

**Table 3. Oppositions (days, record minus DE441 opposition)**

| id | body | record instant (UT) | to true Sun | to mean Sun |
|---|---|---|---|---|
| X.7.3a | mars | +0130-12-14 22:59:28 UT | +0.60 | +0.34 |
| X.7.3b | mars | +0135-02-21 19:16:40 UT | +1.10 | -0.32 |
| X.7.3c | mars | +0139-05-27 19:53:28 UT | +0.63 | +0.42 |
| XI.1.2a | jupiter | +0133-05-17 20:53:14 UT | +0.63 | +0.11 |
| XI.1.2b | jupiter | +0136-08-31 19:59:39 UT | -1.81 | -0.01 |
| XI.1.2c | jupiter | +0137-10-08 02:49:28 UT | -1.41 | +0.06 |
| XI.5.2a | saturn | +0127-03-26 16:48:10 UT | +1.54 | -0.21 |
| XI.5.2b | saturn | +0133-06-03 13:54:09 UT | -0.21 | -0.21 |
| XI.5.2c | saturn | +0136-07-08 10:01:10 UT | -1.11 | -0.03 |

**Table 4. Planet-star relations at the record instant (deg; ecliptic of date, geocentric)**

| id | reading | relation in the words | computed | implied day offset |
|---|---|---|---|---|
| IX.7.9 | printed | 3 'moons' (1 moon taken as 0.5 deg) north of delta Cap; Ptolemy then gives Mercury the star's own longitude | delta_cap: sep 2.32; dlon +0.11, dlat +2.32 | +0.1 |
| IX.7.11 | printed | 1.5 deg (3 moons) to the rear (east) of the line through the horns of Taurus (beta Tau - zeta Tau) | +3.86 from the beta_tau-zeta_tau line (stated +1.50) | -4.0 |
| IX.7.11 | printed | seemed, as it passed, to stand more than 3 moons (>1.5 deg) south of the common star (beta Tau) | beta_tau: sep 10.95; dlon +6.53, dlat -8.77 | – |
| IX.7.11 | emended | 1.5 deg (3 moons) to the rear (east) of the line through the horns of Taurus (beta Tau - zeta Tau) | +0.76 from the beta_tau-zeta_tau line (stated +1.50) | -0.7 |
| IX.7.11 | emended | seemed, as it passed, to stand more than 3 moons (>1.5 deg) south of the common star (beta Tau) | beta_tau: sep 3.19; dlon +1.58, dlat -2.77 | – |
| IX.7.12 | printed | on the line through Castor and Pollux, south of Pollux by (2 x the Castor-Pollux distance) - 1/3 moon | +0.01 off the Castor-Pollux line; 8.02 beyond Pollux (stated 9.21) | -1.7 |
| IX.7.14 | printed | preceded (west of) Spica by a little more than 3 deg (as reckoned by the astronomer the text names) | spica: sep 1.24; dlon -1.21, dlat -0.26 | +1.7 |
| IX.7.15 | printed | half a cubit 'above' the southern pan (alpha Lib); a cubit is about 2-2.5 deg in Babylonian usage (my gloss), taken here as 'north by about 1 deg' | alpha2_lib: sep 1.67; dlon -0.11, dlat +1.67 | – |
| IX.7.16 | printed | half a cubit above beta Sco (as IX.7.15) | beta1_sco: sep 1.23; dlon +0.31, dlat +1.19 | – |
| IX.9.3 | printed | to the rear (east) of Regulus by 3 1/2 1/3 = 3 5/6 deg | regulus: sep 3.72; dlon +3.48, dlat -1.30 | -0.4 |
| IX.10.6a | printed | one moon (0.5 deg) to the rear (east) of the line through beta Sco and delta Sco | +0.77 from the beta1_sco-delta_sco line (stated +0.50) | -2.7 |
| IX.10.6a | printed | two moons (1 deg) north of beta Sco | beta1_sco: sep 1.85; dlon +1.09, dlat +1.49 | – |
| IX.10.6b | printed | 1 1/2 moons (0.75 deg) east of the same line | +1.33 from the beta1_sco-delta_sco line (stated +0.75) | +1.2 |
| X.1.3 | printed | west of the middle of the Pleiades by the Pleiades' length (Ptolemy: about 1 1/2 deg), a little to the south | alcyone: sep 1.84; dlon -1.84, dlat +0.08 | -0.4 |
| X.1.4 | printed | half a full-moon diameter (0.25 deg) to the north-east of the 'middle knee' of Gemini (identified as zeta Gem from Ptolemy's longitude Gemini 18 1/4; my identification) | zeta_gem: sep 1.45; dlon +1.45, dlat -0.11 | +1.2 |
| X.1.5 | printed | east of the star at the tip of Virgo's southern wing (beta Vir) by a Pleiad-length (1 1/2 deg) or less; passing it one moon (0.5 deg) to the north | beta_vir: sep 1.07; dlon +1.07, dlat -0.02 | -0.4 |
| X.1.6 | printed | west of the northernmost of an Aquarius quadrilateral by about 2/3 of a full moon (1/3 deg), seeming to outshine/touch it (star identification uncertain: nearest of lambda, phi, psi1-3 Aqr) | nearest candidate phi_aqr at 1.51; dlon -1.22 | -1.0 |
| X.4.6a | printed | Venus exactly overtook the star 'opposite Vindemiatrix' (Ptolemy: the star after the tip of the southern wing of Virgo, at Virgo 8 1/4 in his catalogue = eta Vir) | eta_vir: sep 0.22 at record; closest 0.21 at rec +0.03 d | +0.0 (closest) |
| X.9.2 | printed | Mars seemed to have occulted beta Sco (morning) | beta1_sco: sep 0.96 at record; closest 0.03 at rec +1.67 d | +1.7 (closest) |
| XI.3.2 | printed | Jupiter occulted the southern Ass (delta Cnc), morning | delta_cnc: sep 0.28 at record; closest 0.25 at rec -0.87 d | -0.9 (closest) |
| XI.7.2 | printed | 2 fingers below the southern shoulder of Virgo (gamma Vir, from Ptolemy's longitude Virgo 13 1/6); a finger taken as 1/12 deg (my gloss); Ptolemy gives Saturn the star's longitude | gamma_vir: sep 0.36; dlon +0.03, dlat -0.36 | -0.4 |

**Table 5. Lunar records (topocentric at Alexandria)**

| id | relation in the words | computed | implied time error | Moon elongation, illuminated fraction | days since / to conjunction |
|---|---|---|---|---|---|
| IX.10.3 | Mercury 1 1/6 deg to the rear (east) of the Moon's centre | body − Moon dlon +0.50, dlat +4.85 | +1.3 h | +24.7, 0.05 | 1.97 / 27.47 |
| X.4.3 | Venus preceded (was west of) the Moon's centre by 1 1/2 times its distance east of beta Sco; with Ptolemy's own longitudes (Venus Scorpius 6;30, beta Sco 6;20 in 10.9.2, Moon 6;45) that is about 1/4 deg | body − Moon dlon +0.59, dlat -1.86 | -2.1 h | -48.0, 0.17 | 25.86 / 3.67 |
| X.8.2 | Mars 1 3/5 deg to the east of the Moon's centre | body − Moon dlon +1.04, dlat -6.58 | +1.4 h | +172.7, 1.00 | 15.03 / 14.41 |
| XI.2.2 | Jupiter appeared level (same longitude) with the Moon's centre, the Moon being further south | body − Moon dlon -0.07, dlat +3.15 | +0.2 h | -30.4, 0.07 | 26.93 / 2.60 |
| XI.6.2 | Saturn about 1/2 deg to the rear (east) of the Moon's centre, the same distance from its northern horn | body − Moon dlon -0.20, dlat +0.05 | +1.2 h | +40.9, 0.12 | 2.97 / 26.50 |
| V.3.2 | Sun sighted at Aquarius 18 5/6, Moon at Scorpius 9 + a damaged fraction ('θ Γ??', read 2/3) | Moon − Sun -98.53 (stated -99.17) | +2.0 h | -98.4, 0.57 | 21.96 / 7.46 |
| VII.2.4 | apparent Moon 92 1/8 deg east of the Sun along the ecliptic, the Sun about to set ('9β' in the export is the numeral 92 with a damaged ninety-sign) | Moon − Sun +92.50 (stated +92.12) | +1.3 h | +92.4, 0.52 | 6.99 / 22.38 |

**Table 6. Eclipse and equinox**

- III.1.10: DE441 spring equinox +0140-03-21 14:16:42 UT; Ptolemy's stated instant minus DE441 = +0.87 d.
- IV.6.14: DE441 greatest eclipse +0134-10-20 20:46:17 UT, local apparent time 22.98 h at Alexandria (Ptolemy: 23 h); umbral magnitude 0.84 (Ptolemy 5/6 = 0.83); Moon -0.50 deg from the shadow axis in latitude (negative = south, so the north limb is eclipsed: 'from the north'); record − DE441 +0.02 h.

**Summary: |record − true greatest elongation| for records the text puts at or about greatest elongation**

- mercury (n = 14; IX.7.11 at its emended date, IX.9.4 as printed): true Sun <= 1 d: 3/14, <= 2 d: 7/14, <= 3 d: 9/14, <= 4 d: 12/14, <= 6 d: 14/14, <= 10 d: 14/14, <= 17 d: 14/14, <= 21 d: 14/14
  - mean Sun: <= 1 d: 2/14, <= 2 d: 7/14, <= 3 d: 9/14, <= 4 d: 13/14, <= 6 d: 13/14, <= 10 d: 14/14, <= 17 d: 14/14, <= 21 d: 14/14
  - sorted: IX.9.3 0.1, IX.9.4 0.2, IX.7.7 0.8, IX.7.4 1.1, IX.7.12 1.1, IX.8.4 1.6, IX.7.16 1.8, IX.7.14 2.7, IX.7.15 2.9, IX.7.11 3.3, IX.8.3 3.4, IX.7.9 3.6, IX.7.6 4.2, IX.7.5 5.5
- venus (n = 8; IX.7.11 at its emended date, IX.9.4 as printed): true Sun <= 1 d: 1/8, <= 2 d: 2/8, <= 3 d: 2/8, <= 4 d: 2/8, <= 6 d: 2/8, <= 10 d: 2/8, <= 17 d: 4/8, <= 21 d: 8/8
  - mean Sun: <= 1 d: 0/8, <= 2 d: 1/8, <= 3 d: 2/8, <= 4 d: 2/8, <= 6 d: 2/8, <= 10 d: 2/8, <= 17 d: 6/8, <= 21 d: 7/8
  - sorted: X.3.2b 0.6, X.3.2a 1.9, X.1.3 16.1, X.1.6 16.7, X.2.3 17.8, X.1.5 18.3, X.2.4 20.3, X.1.4 20.6

**How to read Table 2.** The column "rec − true GE" is the empirical observer slack for a turning-point clue. Positive means the record is later than DE441's greatest elongation.

- **Mercury:**
  - Ptolemy's own astrolabe records lie between −5.5 and +3.4 days (IX.7.4–7, IX.8.3–4, IX.9.4). Theon's lies at −0.1 days.
  - The old star-relation records lie between −3.6 and +2.9 days.
  - The elongation stays within 0.5° of its maximum for 5–10 days. An observer measuring longitudes to about ⅙° cannot place the turning point better than a few days.
- **Venus:**
  - Ptolemy's X.3.2 pair sits on the true maximum (+1.9 and −0.6 days).
  - The other six records, Theon's included, sit 16–21 days off, on both sides. On the dates given they were 0.9–1.2° short of the maximum.
  - Ptolemy chose these records for their equal elongations from the mean Sun, which locate the apsidal line (10.1.2, 10.2.2), not for their timing `[me]`.
  - The mean-Sun reading does not shrink the offsets (Table 2, "rec − mean-Sun GE").

---

## 5. Consequences for the bench

1. **Run the twelve sets with their primary forks** and report recall of the true date (the unique survivor, or the rank of truth):
   - at B&M's tolerance (`k_days` = 1);
   - at the Almagest slack (Mercury `k_days` = 5 or 7; Venus 21).

   On the numbers above, recall at k = 1 is limited by the clues themselves, before any search noise:
   - **Fail at k = 1:** ALM-C, ALM-D, ALM-F, ALM-G, ALM-H, ALM-K and ALM-L. The true date violates one of their own greatest-elongation clues.
   - **Pass at k = 1:** ALM-A (printed reading) and ALM-E.
   - **No greatest-elongation clue:** ALM-B, ALM-I and ALM-J. They depend on lunar phase, star relations and before/after-elongation clues, whose slack is small.
2. **Critique issue 3, fix 3.** If the k = 1 runs fail, the finding to report is: "B&M's tolerances cannot recover expert planetary records". It conditions every "no" about the Odyssey. If they pass only at k ≥ 5 (Mercury) or k ≥ 21 (Venus), a B&M-type reading of the Odyssey must be scored at those tolerances too.
3. **Critique issue 16.** The "16-day Venus slack" [ctl §0] is confirmed and widened: Venus "greatest elongation" records are 16–21 days off in 6 of 8 cases. It belongs to turning-point clues only. B&M's Venus clue is a rise-lead threshold, which every Venus morning record passes with a large margin, so that slack does not transfer to it.
4. **Critique issue 12.** B&M's Mercury proxy (the maximum of rising azimuth) is not the greatest elongation. The `bm_mwra_k` fork measures how often the proxy coincides with an expert's greatest-elongation record. On Table 2 it does so for 2 of 7 morning records at ±3 days.
5. **Ephemeris coverage.** A 136-year search window placed at random around these truths needs DE441 over roughly AD 0–280 and 410–90 BC. The harness must fetch that coverage itself. It must not infer window positions from the excerpts in `results/controls-almagest/ephem/`.

---

## 6. Limitations and open items

- **Units and identifications are my glosses** `[me]`:
  - Units: a "moon" is 0.5°, a cubit about 2°, a finger 1/12°. A Pleiad length of 1.5° is Ptolemy's own value (10.1.3).
  - Star identifications:
    - ζ Gem as the "middle knee of Gemini" and γ Vir as the "southern shoulder of Virgo" both come from Ptolemy's stated catalogue longitudes.
    - β Vir is the wing tip and η Vir the star "opposite Vindemiatrix".
    - The Aquarius quadrilateral star of X.1.6 is **not** securely identified: the nearest candidate, φ Aqr, is 1.5° away against a stated ⅓°.
  - The positional slack figures in Table 4 inherit these glosses.
- **The X.2.3 hind-leg star of Aries is not identified.** Its positional relation was not computed.
- **Site assumptions.** Babylon is assumed for the three Chaldean-calendar records, and Alexandria for all others. Only horizon quantities depend on the site.
- **The instant convention moves the continuous offsets.** Taking evening and dawn as the Sun at −8° shifts them by about ±0.1 days. A B&M-style integer-day test can count 1.1 days (IX.7.4, IX.7.12) as 1.
- **Textual cruxes rest on the export and Ptolemy's arithmetic.** Heiberg's apparatus and Toomer's notes were not consulted [secondary, not read].
- **The control is mostly Ptolemy's own reductions.** The Hadrianic and Antonine records come from one or two observers with one instrument tradition. They test expert slack, not the slack of a poet's sky.
- **Not done here:** the B&M-style search itself. This note prepares the sets and measures the slack; running the search is the bench's job.

## 7. Files

All scripts are in `C:\Projects\odybench\results\controls-almagest\`. Each runs from the project root with `py results/controls-almagest/<script>`.

| file | what it is |
|---|---|
| `records.py` | The 47 records, with exact Greek licence words, the era chain and the mean-Sun check. Running it prints the check. |
| `greek.py` | Accent-insensitive locator that returns verbatim substrings. |
| `slack.py` → `slack.json`, `slack.out.txt` | The DE441 comparison (all of section 4). |
| `build_prereg.py` | Writes the two prereg files and runs a leak check on the clue file. |
| `doc_tables.py` → `doc_tables.md` | The tables in sections 2 and 4. |
| `fetch_ephem_almagest.py`, `ephem/*.bsp` | DE441 excerpts for AD 120–145 and 296–224 BC (truth neighbourhood only). |
| `fetch_stars.py`, `stars.json` | Hipparcos astrometry for the stars named in the records. |
| `scan_dates.py`, `scan_rulers.py`, `show.py`, `fixlic.py` | Reading aids. |
| `data/prereg/controls_almagest.json` | The clue sets, for the searcher. |
| `data/prereg/controls_almagest_truth.json` | The true dates, the conversions and the Greek date words. The searcher must not read it. |
