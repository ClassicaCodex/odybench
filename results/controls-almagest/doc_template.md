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

<<TABLES_1>>

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
<<SETROWS>>

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

<<TABLES_2>>

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
