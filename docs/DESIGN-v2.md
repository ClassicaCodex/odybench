# odybench — design (revision 2)

A test bench for the claim that the sky clues in the Odyssey date the
slaughter of the suitors to 16 April 1178 BC. It is the fourth in the series
after vbench (Voynich), [labench](../labench/README.md) (Linear A) and
[indusbench](../indusbench/DESIGN.md) (Indus script), and it keeps their rule:
every test is run first on cases whose answer is known, so that a "no" about
the Odyssey means something.

Revision 2, written 2026-10-04. Revision 1 (2026-10-03) is kept unchanged as
`docs/DESIGN-v1.md`. An adversarial review of it (`docs/critique-design.md`)
found 25 issues, 3 of them blockers. A preparation stage then fetched the
data, built the calendar module, drafted and licence-checked three sets of
clue files, and read the primary sources the dossier had missed. This
revision rebuilds the design on that material. Section 14 lists every issue
with its resolution and the sections it changed.

**Status.** Built and validated: `odybench/ephem.py`, `odybench/ccx.py`,
`odybench/calendar.py` and the data in section 2.1. Drafted and
licence-checked, not frozen: `data/prereg/controls_real.json`,
`controls_almagest.json` and `negatives.json`. No other bench code exists. No
null model, control search or held-out check has been run. Everything in
sections 3–9 is frozen in a local git commit before any of them runs
(section 12), and section 8 lists, with thresholds, what the bench expects
before it looks.

---

## 0. Conventions and tags

- **Years.** Historical BC with the astronomical year after it: 1178 BC
  (−1177).
- **Calendar.** Proleptic Julian throughout. 16 Apr 1178 BC is JD 1291263.5
  at 0 h, and 5 Apr in the proleptic Gregorian calendar [acq §4]. **All
  calendar arithmetic goes through `odybench.calendar`** (exact integer JDN
  arithmetic; half-open day and span bounds; UT+2, LMT and LAT civil dates).
  Python `datetime` and numpy `datetime64` are banned from `odybench/`,
  `tools/`, `tests/` and the top-level scripts; `tests/test_calendar.py`
  enforces the ban [acq §4]. Modules inside the package are run as
  `py -m odybench.x`, never `py odybench/x.py`, because the file would then
  shadow the standard library's `calendar` [acq §4].
- **Time scales.** TT (= TD of the eclipse canons); UT = UT1; ΔT = TT − UT.
  UT+2 is zone time on 30°E, the clock Baikouzis & Magnasco used [bm §3.2].
  LMT is local mean time (UT + longitude/15). LAT is local apparent solar
  time. "Hour n of the day (night)" is a seasonal hour, one twelfth of
  sunrise–sunset (sunset–sunrise); Ptolemy's hours are equinoctial hours of
  LAT [pcr §2]. Every clock time below names its scale.
- **Epoch.** The argument of every ΔT model is the Julian epoch of the TT
  instant, `calendar.julian_epoch(JD_TT) = 2000 + (JD_TT − 2451545)/365.25`,
  identical to `ephem.julian_epoch` [acq §4]. 16 Apr −1177 is epoch
  **−1176.68**. Revision 1 labelled its ΔT values "−1177.29", which was wrong
  [rev #22].
- **Days.** A civil day runs from local midnight to midnight (LMT at the
  site) unless a rule names UT+2. Day n is the civil date of the daylight of
  that day; Night n runs from sunset of Day n to sunrise of Day n+1; Dawn n+1
  is the morning twilight that ends Night n [neg conventions]. T0b and fork
  option F2 (a) use UT+2 civil dates, as B&M did.
- **Sites.** One table, `data/prereg/sites.json`, used by every module:

  | key | place | lat, lon (deg, E +) | role | source |
  |---|---|---|---|---|
  | `ithaki` | Ithaki (Vathy) | 38.37, 20.72 | primary Odyssey site | the coordinates that reproduce the NASA site catalogue [acq §2.2]; Vathy 38.367, 20.717 differs by 0.3 km |
  | `bm` | B&M's fitted site | 38.4, 20.7 | T0b only | the S2 clock fit [bm §3.2] |
  | `kefalonia` | Argostoli | 38.18, 20.49 | sensitivity | [acq §2.2] |
  | `lefkada` | Lefkada town | 38.83, 20.70 | sensitivity | [acq §2.2]. research-ephemeris used 20.71 [eph conventions]; **20.70 is adopted** so that the site catalogue reproduces |
  | `corfu` | Corfu town | 39.62, 19.92 | sensitivity | [acq §2.2] |
  | `zakynthos` | Zakynthos town | 37.78, 20.90 | sensitivity | [acq §2.2] |
  | negative-control and control sites | as given in `negatives.json`, `controls_real.json`, `controls_almagest.json` | | | each file's own `observer_place` entries |

  Revision 1's Paliki (Lixouri) is dropped: Lixouri lies about 0.05° from
  Argostoli [me: approximate coordinates 38.20°N 20.44°E, not checked
  against a gazetteer], and Kefalonia is already within 0.001 in magnitude of
  Ithaki for the 1178 BC eclipse [eph §5.4].
- **ΔT models.** Four, each with its stated 1σ [eph §2.2–2.3; rev #19]:
  SMH2020 (S15 spline plus the HMNAO lod integral before −720), the Addendum
  2020 parabola, the SMH2016 parabola, and Espenak–Meeus in its canon form
  (ṅ −25.858). Revision 1 counted Espenak–Meeus twice, in two ṅ frames; it is
  one model [rev #19]. The **equal-weight mixture** is over these four, each
  taken as a Gaussian with its stated σ (an assumption, stated every time it
  is used [eph §8 item 1]). Espenak–Meeus σ is Huber's before −500 and
  Morrison–Stephenson 2004's 0.8u² from −500, as on NASA's page; the envelope
  is discontinuous at −500 [acq §2.2], which matters only for controls near
  that year and is reported where it does. SMH2020's σ before −2000 is an
  extrapolation [acq §6 item 3]; no eclipse in the bench lies there.
- **ΔT travels with its lunar ephemeris.** SMH models pair with DE431 (the
  DE430 lunar model); Espenak–Meeus pairs with the NASA Besselian elements.
  A value is converted between ṅ frames (−25.82 ↔ −25.858: 34 s at −1177)
  before use in the other frame [eph §2.3, §5.3]. Lunar-timed quantities
  (conjunctions, full moons, lunar eclipses, Moon rise and set) are computed
  with DE431 and SMH2020 ΔT; planets and stars with DE441 [me, from eph §5.3].
  DE431 is split at JD 1721425.5 (AD 1 Jan 3, Julian); no DE431 request may
  straddle it, so all lunar code works in yearly chunks [acq §1.1].
- **Magnitudes** (pinned, one definition per use [rev #21]):
  `smag` = fraction of the Sun's diameter covered at the site, at maximum,
  (L1′ − m)/(L1′ + L2′) in Besselian terms (NASA's "magnitude");
  `obsc` = fraction of the Sun's area covered; a separate **central flag**
  (total, annular or none) with its duration in seconds. The Moon/Sun
  diameter ratio (L1′ − L2′)/(L1′ + L2′) is never called a magnitude: for the
  1131 BC eclipse at Ithaki the two are 1.0169 and 1.0486 [rev #21]. Lunar:
  `umag` umbral and `pmag` penumbral magnitude in the convention of NASA's
  lunar canon, fixed by instrument check I4. One digit = 1/12 of the lunar
  diameter [pcr §2].

**Provenance tags.** A tag names the document and section that carries the
number and its primary source.

| tag | document |
|---|---|
| [bm §n] | `docs/research-bm2008.md`, the reconciled spec of the paper |
| [chron §n] | `docs/research-chronology.md` |
| [txt §n] | `docs/research-textclues.md` |
| [eph §n] | `docs/research-ephemeris.md` |
| [vis §n] | `docs/research-visibility.md` |
| [ctl §n] | `docs/research-controls.md` |
| [win §n] | `docs/research-window.md` |
| [crit §n] | `docs/research-critiques.md` (the responses since Schoch) |
| [rev #n], [rev Vn] | `docs/critique-design.md`, issue n or verification row Vn |
| [acq §n] | `docs/data-acquisition.md` |
| [pcr §n] | `docs/controls-real-drafting.md` |
| [lcr] | `docs/license-check-controls-real.md` |
| [alm §n] | `docs/controls-almagest.md` |
| [lca] | `docs/license-check-almagest.md` |
| [neg §n] | `docs/negatives-drafting.md` |
| [lcn] | `docs/license-check-negatives.md` |
| [unread §n] | `docs/research-unread-primaries.md` |
| [v1 §n] | `docs/DESIGN-v1.md` |
| [B&M §X] | the paper: Baikouzis & Magnasco, PNAS 105 (2008) 8823–8828, by section heading; [SI], [S2] its Supporting Information |
| [Od. x.y] | Greek text, `data/text/odyssey-grc.tsv` |
| [me] | reasoned or computed for this revision; arithmetic is shown |

"B&M" is Baikouzis & Magnasco 2008 throughout. A statement a note made from
a secondary report keeps that status here and is marked *secondary*.

---

## 1. The claim under test

### 1.1 What the paper says

B&M's abstract, paraphrased closely (full text local at
`data/bm2008-a/bm2008-pmc-fulltext.txt`):

- They take three overt astronomical references in the epic (Boötes and the
  Pleiades, Venus, the New Moon) and add a conjectural one, Hermes' trip to
  Ogygia read as the motion of the planet Mercury.
- They search every date in 1250–1115 BC (−1249 to −1114) for days matching
  these phenomena in the order and manner the text gives.
- In that span, in their words, "a single date closely matches our
  references": 16 April 1178 BC (−1177) [bm §9].
- They do not assume an eclipse; Theoclymenus' vision (Od. 20.351–357) is not
  a search criterion. They speculate afterwards that the references and the
  vision refer to the total solar eclipse of that day, which Schoch (1926)
  and P. V. Neugebauer (1929) had computed as total over the Ionian Islands
  [B&M abstract; bm §2, §11].

The body adds four claims the bench also tests [B&M §Intersecting,
§Historical Plausibility, §Conclusions; bm §2]:

1. The date satisfies all criteria as stated in the 135-year span, under both
   their sequential and parallel day counts, exactly under the sequential one.
2. The references can be matched exactly about one day in 2,000 years. The
   arithmetic is one candidate New Moon in 6 years × 3 (Venus) × 116 days
   (Mercury) ≈ 2,088 years [bm §10]. **The 6 years is the rate of the season
   clue C and the equinox clue E together** [B&M §Intersecting; vis §3.4],
   and E is the clue B&M listed but did not apply. The figure therefore
   describes five clues, not the four that were searched [rev #5, V2].
3. Two independent sets of verses (the eclipse lines and the other sky
   references) point to the same day; chance agreement of fictional
   references with the only eclipse of the century would be minute.
4. Supporting coincidences found afterwards: the eclipse near noon, early
   spring, Mars invisible except during the eclipse.

The search criteria, as reconciled from the primary text and the
transcriptions of Table S2 [bm §5]:

| clue | lines | criterion | day (sequential / parallel) |
|---|---|---|---|
| N, New Moon | Od. 14.161–162 = 19.306–307; 14.457; Apollo's feast 20.156, 20.276–278, 21.258–259 | Ti is the date of a New Moon (search unit) | 0 / 0 |
| C, Pleiades and late-setting Boötes | Od. 5.270–277 | Ti−29 ≥ 17 Feb and Ti−12 ≤ 4 Apr, so Ti in 18 Mar–16 Apr of a common year | −29 / −28 (all sailing nights to −12 / −11) |
| V, morning star | Od. 13.93–95 | Venus rises ≥ 90 min before the Sun | −5 / −4 |
| M, Hermes = Mercury | Od. 5.43–58, 5.97–103 | Ti−34 within a few days (S2: ≤ 1 to pass) of Mercury's maximum western rise azimuth (MWRA), Mercury visible | −34 / −33 |
| E, Poseidon = equinox | Od. 5.282 | 1 Apr ≤ Ti−11 ≤ 5 Apr in §References; "on or before 4 April" in §Intersecting; listed, **not applied** | −11 / −10 |
| X, the eclipse | Od. 20.345–357 | not used | 0 |

**Where the clues came from.** No clue in N ∧ C ∧ V ∧ M was formulated blind
to 1178 BC [unread §9 item 3]. Schoch found April *from* the eclipse,
searching −1240 to −1140 with no season constraint [unread §3.1]. Every
season reading before 1967 that MacDonald surveys is autumn or winter
(Finsler, Wilamowitz, Scott, Murray, and Schoch's own later "winter") [unread
§2.1, §2.4]. MacDonald 1967, the first spring reading of 5.272, already cites
the eclipse, shifts his timetable a week to meet it, and checks Venus in the
eclipse year; the equinox reading E is also his [unread §2]. Only M is B&M's
own, and B&M too knew the target.

### 1.2 What the bench can and cannot establish

It can establish:

- whether B&M's computation reproduces with a modern ephemeris, and if not,
  which step fails (section 3);
- how often B&M's criteria, and criteria like them, are met by chance, per
  century and per window (N1, N5);
- how often a date picked out by such criteria would be an eclipse new moon
  if the clues had nothing to do with the eclipse (N2);
- how much the freedom to choose readings, thresholds, tolerances and windows
  inflates a match (N3), and how often a random poem of the same grammar
  "dates" itself to an eclipse as well (N4);
- how probable totality at Ithaca was, over the ΔT models now published (N6);
- whether the method recovers dates that are known, from real eclipse records
  and from real records of B&M's own clue types, and whether it "dates"
  fiction (section 6);
- whether sky clues B&M did not use agree with their date more often than
  chance (section 7).

It cannot establish:

- that the poet meant any line astronomically. Every reading is a fork
  (section 5.3); the bench prices forks, it does not choose between them.
- that Odysseus, the war or the return happened. B&M say the same [bm §2].
- the season of the poem, the meaning of λυκάβας, whether Hermes is Mercury,
  or whether Apollo's feast fell on the new moon. These are philological
  questions; the text and the ancient commentators do not settle them
  [txt §5; vis §3–4; crit §3].
- a posterior probability. The prior that a day-dated sky observation
  survived 400–600 years of oral transmission is not computable; the notes
  found no comparative case [win §10–11]. The bench reports likelihood
  ratios and look-elsewhere-corrected p-values and stops there.

**A bit budget, to fix ideas** [v1 §1.2; rev §1 confirms the arithmetic].
Singling out one New Moon among the 1,683 in B&M's window takes
log2(1683) = 10.7 bits. B&M's applied clues carry about C 3.6 bits (8.3% of
New Moons pass), V 2.7 bits (15.8% of spring Day −5s) and M 4.5 bits (6/136
rows pass with DE441): 10.8 bits in all, so about one chance survivor is
expected (1,683 × 0.083 × 0.158 × 0.044 = 0.97). The forks of section 5.3
could cost up to 7.2 bits (B&M's own forks), 17.1 bits (the documented
garden) or 21.6 bits (the full garden) if the readings were independent. They
are not; measuring how much of that cost is real is the job of N3.

### 1.3 Outcomes

The verdict is a set of labels computed mechanically by `verdict.py` from
named quantities (section 9). The labels:

1. **The text dates the return.** The match survives B&M's own forks (N3),
   random poems of the same grammar, read with the same freedom, rarely reach
   Schoch's target (N4), the likelihood ratio is large at realistic noise,
   both components of the method can see (section 6), and no clean negative
   dates itself. The bench then says so and says what it would take to
   believe it.
2. **The match is ordinary.** A comparable date fixed in advance is made the
   unique match by some reading B&M themselves raised often (G_BM ≥ 0.05), or
   a clue set that truly observed the target's sky would not reach it much
   more often than an unrelated clue set does (likelihood ratio below 10 even
   at the noise most favourable to B&M). The coincidence then carries no
   evidential weight, whatever its fixed-reading p-value.
3. **The method cannot see**, split by component [rev #3]:
   - **3a, the eclipse component**: the method does not recover the dates of
     real eclipse records (PC-R, section 6.3).
   - **3b, the B&M-type component** (lunar phase, star season, morning star,
     Mercury turning point): it does not recover the dates of real
     planetary and lunar records of B&M's own kinds even at the slack real
     observers need (the *Almagest* control, section 6.4), or of synthetic
     clue sets generated from real skies (PC-S, section 6.2).

   Every "no" about the Odyssey that depends on the failing component is
   reported as "could not have seen it".
4. **The method dates fiction.** A clean negative (fiction composed long
   after the events it tells) yields, under its own sourced readings, an
   eclipse match at least as strong and at least as significant as the
   Odyssey's. That retires the method, not only the claim.

**Inconclusive** is reported when none of the labels applies, with every
quantity and threshold beside it. Labels 2, 3a, 3b and 4 can hold together;
label 1 excludes all the others. Three **qualifiers** are always reported
when they hold: Q_BM, "B&M's own tolerances cannot recover expert planetary
records" (section 6.4); Q_strict, "an all-clues-must-pass rule rejects the
true date of most real eclipse records" (section 6.3); and Q_exposure, "gate
3a changes when three possibly steered control rows are re-drafted blind"
(section 6.3.3).

"What, if anything, the text can date" is reported in every case, at the
level the tests support: a relative chronology [chron §5], a month-turn on
Day 0 under one reading [txt §5.1], a season the text does not determine
[txt §5.6], and a year only if outcome 1 holds.

---

## 2. What is already known, and so is not a prediction

These numbers exist before the freeze. They are listed so that nothing in
section 8 pretends to predict them. Where a number came from a rough model,
the row says so and the bench recomputes it, but its confirmation is not
counted as a success.

### 2.1 Instruments already built and validated

| item | result | source |
|---|---|---|
| Ephemeris coverage | one DE441 excerpt −2060-01-01..+241-01-01 Julian (JD 968642.5–1809083.5), 11 bodies, 237.9 MB; DE431 Sun/EMB/Earth/Moon over the same span in two pieces split at JD 1721425.5; DE431 ±60-day excerpts for −1339 Jan 8 and −647 Apr 6 | [acq §1.1] |
| `ephem.kernel()` | picks the shortest covering excerpt; 4,500/4,500 old requests unchanged; Chebyshev records bit-identical between narrow and long excerpts (11 pairs); 68/68 module results identical to the last bit | [acq §1.2–1.3] |
| Ephemeris validation | `validate_ephem.py` 55/55 (identical line for line to 2026-10-03 apart from the file list and run time; run with `PYTHONIOENCODING=utf-8`); `test_ephem.py` 10/10 | [acq §1.3; eph §10] |
| Horizons spot checks, −1999 to +200 | astrometric Sun/Venus/Mercury ≤ 0.0022″, Moon ≤ 0.524″, elongation ≤ 0.57″; az/el ≤ 78″ at −1999 falling to 4″ at +200, tracking the IAU 1982 vs Vondrák sidereal-time difference (+79.5″ at −1999); tolerances fixed before the run | [acq §1.3] |
| DE441 − DE431 lunar offset | follows the +0.00335″ T³ law over −1999..+200 at ratios 0.85–1.03; +187.7 s in greatest-eclipse time at −1177 | [acq §1.3; eph §5.3] |
| NASA Canon elements | 23 century files −1999..+300, 5,486 eclipses, byte-identical to earlier copies; every SEcat5 eclipse matches one element row (TD ≤ 0.5 s, ΔT ≤ 0.5 s, γ ≤ 0.00005); element ΔT = `dt_em2006_canon` at a day-resolved year to ≤ 0.15 s | [acq §2.2] |
| Site catalogues | Ithaca, Kefalonia, Lefkada, Corfu, Zakynthos, 5,486 rows each (NASA's JavaScript); identical field for field to the earlier window catalogue over −1499..−600 | [acq §2.2] |
| Stars | 21 stars in `data/stars.json`; every HIP number read from SIMBAD's identifier list and checked against hip2 (position ≤ 0.038″, \|Hp − V\| ≤ 0.37); the five numbers revision 1 gave from memory are confirmed (Sirius 32349, Aldebaran 21421, Betelgeuse 27989, Rigel 24436, Dubhe 54061) | [acq §3] |
| Sirius | the Hipparcos solution for HIP 32349 is an orbital solution referred to the centre of mass, so its proper motion is barycentric and is adopted, with system RV −8.47 km/s (Bond et al. 2017). At −1177: FK5 long-baseline motion differs by 0.99′, Bond-orbit re-referral by 1.02′, a photocentre motion would be 24.2′ off | [acq §3.3] |
| Calendar | `odybench/calendar.py`; `tests/test_calendar.py` 11/11, including every day of −1999..+500 against independent day counting, 306/306 Horizons calendar dates, and the `datetime` ban; a mutation check catches 5 deliberate bugs. The Meeus ch. 7 values in the test were recalled, not read, but each also agrees with exhaustive counting | [acq §4, §6 item 7] |

### 2.2 Reproduction

- **T0a is done.** Two independent transcriptions of Table S2 agree cell for
  cell (152 rows × 13 fields). The decoded colour rules on the 136 rows of
  1250–1115 BC give V 21, M (\|Δ\| ≤ 1) 4 (1236, 1224, 1178, 1157 BC), E 22
  (XXX) / 20 (1–5 Apr) / 17 (1–4 Apr), V ∧ M = {1178} [bm §8.1;
  `results/bm2008-reconcile/s2_counts.out.txt`].
- With Mercury recomputed by DE441 on S2's own Ti, M passes in 1236, 1224,
  1190, 1189, 1178 and 1144 BC; 1157 BC drops out (DE441 MWRA 22 Feb, Δ −3);
  **V ∧ M = {1178, 1189}** [bm §8.2].
- 18 Mar 1189 BC (−1188) passes N, C (Ti−29 = 18 Feb in a leap year), V
  (lead 100.9 min) and M (Δ 0), and fails E (Ti−11 = 7 Mar) [bm §8.2;
  rev V10].
- No visibility threshold separates the two: at Mercury's rising the Sun
  stood at −13.2° on 13 Mar 1178 BC and −17.1° on 13 Feb 1189 BC [bm §8.2].
- **The integer MWRA is ill-conditioned** [rev #12, V15]. Rises bisected to
  0.01 s give, for 1178 BC, 12 Mar 112.30419° and 13 Mar 112.29647° (vertex
  about 12.3 Mar, Δ about +0.7 d) and, for 1189 BC, 12 Feb 120.48066° and
  13 Feb 120.48110° (vertex about 12.5 Feb): the 1189 integer maximum is
  decided by 0.0004°. Minute-rounded rises put the series 0.1° off and make
  it non-monotonic [`results/bm2008-reconcile/check_extras.out.txt`].
- Venus leads on Ti−5: 103.6 min on 11 Apr 1178 BC (B&M 1:42:56) and
  100.9 min on 13 Mar 1189 BC [rev V10].
- Conjunctions 18 Mar 03:31 and 16 Apr 12:25 UT+2 (−1177, ΔT 27,602.7 s);
  equinox 1 Apr 15:31 UT+2 (B&M 15:24); Sun at −12° on 18 Mar at 19:34 UT+2
  (B&M 19:38) [bm §9].
- Under the parallel reckoning 1178 BC misses the Pleiades bound and the
  equinox bound by one day each [bm §9].
- Under B&M's ≤ 4 Apr equinox bound (§Intersecting), 1178 BC fails E,
  because Ti−11 = 5 Apr [rev #23].
- The candidate count over "1 Jan 1250 – 31 Dec 1115 BC" was 1,682 in the
  timing run (which ended at 0 h on 31 Dec), 1,683 in `check_ti` and 1,684
  in B&M [rev #22].
- Reach of 1178 BC under the T0b reading with E off: 1189 BC lies 11 years
  earlier, so reach_136 ≤ 11/136 = 0.081, and it is 0 if another survivor
  falls in −1176..−1052; that span has not been computed [rev #24c].

### 2.3 The eclipse

| eclipse | site | pairing | values | source |
|---|---|---|---|---|
| 16 Apr 1178 BC | — | canon | catalogue 01966, Saros 39 member 31, γ 0.5187, magnitude 1.0599, greatest eclipse 32.7°N 12.7°E at 17:57:28 TD = 10:00:58 UT, ΔT 28,590.0 s | [rev V4] |
| | Ithaki | NASA elements, canon ΔT | smag 0.984 at 10:22 UT = 11:45 LMT = 11:44 LAT, Sun 57.2°; total for constant ΔT 28,801–29,585 s (28,805–29,580 s on a 5-s grid) | [eph §5.4; rev V5] |
| | Ithaki | DE431 + SMH2020 28,543 ± 720 s | 0.984 at LAT 11:44; total for 28,761–29,545 s, i.e. +218 to +1,002 s above the central value (+0.3σ to +1.4σ) | [eph §5.4] |
| | Ithaki | DE441 + SMH2020 | 0.972 at LAT 11:49; total for 28,922–29,706 s | [eph §5.4] |
| | Ithaki | DE441 + B&M's 27,602.7 s | 0.900 at 12:48 UT+2, not total; mixes ephemerides, reported only to show it | [bm §3.3] |
| | Lefkada | DE441 / DE431, SMH2020 central | 0.981 / 0.993; Kefalonia within 0.001 of Ithaki | [eph §5.4] |
| 30 Sep 1131 BC | Ithaki | NASA, canon | total; 09:49 UT = 11:12 LMT; Sun 51.6°; total for 27,050–28,035 s (−641 to +344 s from canon); smag 1.0169, diameter ratio 1.0486 | [rev V6, #21] |
| 24 Jun 1312 BC | Ithaki | NASA, canon | 0.984 at 12:02 LMT (about 12:09 LAT); total for +539 to +1,449 s above canon | [rev V6; win §7.1] |

**P(total at Ithaki) per ΔT model**, each model's σ taken as Gaussian, in the
canon frame on NASA's elements (SMH values converted by +34 s) [rev #17;
`results/critique-design/check_p19.out.txt`, `check_mag09.out.txt`]:

| model (value ± σ at −1176.68) | P(total) 1178 BC | P(total) 1131 BC | joint, common offset | P(smag ≥ 0.9) 1178 BC |
|---|---|---|---|---|
| SMH2020 28,543 ± 720 | 0.294 | 0.494 | 0.047 | 0.932 |
| Addendum 2020 parabola 28,282 ± 541 | 0.173 | 0.641 | 0.052 | 0.934 |
| SMH2016 parabola 28,963 ± 541 | 0.498 | 0.443 | 0.108 | 0.997 |
| Espenak–Meeus, canon form 28,589 ± 1,008 | 0.252 | 0.412 | 0.049 | 0.849 |
| **equal-weight mixture of the four** | **0.304** | **0.498** | **0.064** | **0.928** |

[me: means of the rows above.] In the DE431 pairing the three SMH values are
0.299, 0.178 and 0.505 [eph §5.4]; with Espenak–Meeus on NASA's elements
(0.252) the mixture is 0.309 [me]. The 1178 and 1131 BC totality windows
overlap only near +220 to +340 s above canon ΔT, so at most one of the two
was likely total at Ithaca [win §7.1]. Magnitude ≥ 0.9 holds for constant ΔT
between about 27,600 and 31,000 s; maximum falls between LAT 10:30 and 12:47
over 26,000–32,000 s [eph §5.4].

**Base rates at Ithaca.** In −1499..−600: total at nominal ΔT 6 events;
total for some ΔT within ±1σ 10; the same and 10–14 h LAT 3 (1312, 1178,
1131 BC); smag ≥ 0.95 at nominal ΔT 15 [win §7.2]. Extended with the new
elements: total for some ΔT within ±1σ, 7 in −1999..−1500 (all partial at
nominal ΔT, σ 2,000–3,700 s) and 4 in −599..+300 [acq §2.2]. Under Schoch's
own rule (maximum 10 a.m.–noon) 1312 BC drops out, its maximum being after
noon [rev #10]. The new-moon base rate for "total within ±1σ" is p_e =
8.98 × 10⁻⁴, and for the near-noon subclass 2.70 × 10⁻⁴ [win §8c].

**B&M's own ΔT is uninterpretable.** Starry Night 6 Pro Plus used 29,300 s
at −1206 (Papamarinopoulos et al. 2012), the Espenak–Meeus parabola + 35 s;
B&M's Starry Night 6.0.4 used 27,602.7 s at −1177, the parabola − 1,114 s.
One smooth ΔT(t) cannot give both: the gap is 1,149 s [unread §7].

### 2.4 Rates and arithmetic

- Per-clue chance rates over 1250–1115 BC at Ithaca: C passes 8.3% of new
  moons (1.02 a year); V passes 15.8% of B&M's spring Day −5s (29.6% of all
  days); M (rise-azimuth maximum, visible) 5.0% at ±2 d and 7.9% at ±3 d of
  spring Day −34s; C ∧ E leaves one new moon per 6.2 years [vis §1.3, §2.3,
  §3.4].
- The rough joint expectation is 1.1 chance matches in 136 years; the
  single-target pass rate is about 0.8% given the spring window and about
  0.07% unconditionally [vis §5].
- B&M's own arithmetic redone at their stated ±1-day colour tolerance:
  1.02 × 1/3 × 3/116 ≈ 0.0088 a year = **0.88 per century** with E off, and
  **0.14 per century** with E on, against the 0.048 per century they printed
  [rev #5].
- Replacing B&M's clock ΔT by SMH2020 + 1σ moves UT by 1,660 s and flips the
  UT+2 date of about **1.9%** of conjunctions [rev #17].
- Window scaling: at criteria fixed in advance the expected double hit is
  10⁻⁵–10⁻³ per 135-year window [win §8c].
- Garden arithmetic of revision 1: 8 × 4 × 6 × 6 × 31 × 4 × 3 = 428,544
  readings (18.7 bits) [rev §1]. Revision 2's gardens are in section 5.3.
- The Mercury turning points are spread: the morning station precedes GWE by
  12–15 d; the rise-azimuth maximum falls 26 d after to 9 d before GWE; under
  "GWE or station within ±2–3 d" 1178 BC fails [vis §2.3, key finding 3].
- With Day 0 one day after the conjunction (Solon's noumenia), 1178 BC
  drops out of the joint test [vis §4.3].
- Given Day 0 a conjunction, the median Moon-up share of the night after
  Day −5 is 25%, so H2's "< 25%" passes about half the time; 24–31% of all
  nights are as dark [vis §4.5; rev #24b].

### 2.5 Sources now read

- **MacDonald, *JBAA* 77 (1967) 324–327** (4 pages, not 324–328) [unread
  §2]. He argues for **March** for the voyage, from Od. 5.270–277 ("late"
  read as lateness), with Neugebauer's star tables and Schoch's arcus
  visionis, plus a timetable reading Poseidon's return (5.282) as the
  equinox. He discusses the 1178 BC eclipse (16 April, 11.45 a.m. local
  time) and shifts his timetable a week to meet it. He gives Venus' greatest
  morning elongation "in 1176 B.C. on March 17"; DE441 has it on 16 Mar −1177
  and none in −1175, so "1176" is very probably a slip for 1178 [unread
  §2.5]. **Gainsford's "second half of May" misreads p. 327**, where
  MacDonald answers Schoch's "winter and not April" from the reaping match;
  Gainsford's locator ("217") and his "26 April 1178" are also wrong [unread
  §2.3].
- **Papamarinopoulos et al., *MAA* 12(1) (2012) 117–128** read the same star
  lines as autumn and reach 30 Oct 1207 BC (−1206) through a stated chain
  (64 → 14 → 5 → 1 eclipses). Their 16:00 "LT" is UT+2, i.e. 15:23 LMT at
  Vathy. Their canon ΔT is 29,136 s. The first author had endorsed 16 Apr
  1178 BC in 2008 [unread §4].
- **Henriksson, *MAA* 12(1) (2012) 63–76** is about the Iliad only; his
  eclipse is the canon's −1311 Jun 24 (Julian); his "Gregorian" labels run
  one day early [unread §5].
- **PLSV has no extinction model.** Visibility is an arcus visionis plus a
  "critical altitude" (default 0°); default AV = 10.5 + 1.4m (heliacal) and
  8.9 + 1.1m (acronychal and cosmical); fixed planetary values are Schoch's
  1928 (Mercury morning first 13°); its ΔT is Chapront-Touzé & Chapront 1991.
  B&M used version 3.0; the documentation read is 3.1 [unread §6].
- Neugebauer & Schoch, *AN* 230 (1927) 57: no Odyssey content; Schoch's 1926
  elements were revised within a year; Mercury heliacal AV values (morning
  first 13.8°) [unread §3.2].
- **Not read**: P. V. Neugebauer, *Astronomische Chronologie* (1929);
  Schoch, *Die Sterne* 6:88 and *Dichter-Finsternisse*; P.Oxy. 3710; Austin
  1975; de Jong 2001 App. A; Stanford 1959; the Oxford commentaries; Starry
  Night internals [unread §8].
- **Text facts found by the drafting agents.** *Aen.* 2.255 "silentia lunae"
  admits the conjunction reading (Pliny *NH* 16.190, local key 16.39.2), and
  2.340 "oblati per lunam", in the same night, contradicts it [neg §3.1].
  *Arg.* 1.1202 is a simile; the full Moon of 1.1231–1232 sits on the same
  night as the morning star of 1.1273 [neg §3.2]. An ancient scholiast
  already read Il. 17.366 as an eclipse, but the text confines that darkness
  to mist while the rest fought in bright sun (17.370–373) [neg §3.5]. The
  17-days-then-18th pair of Od. 5.278–279 recurs at 24.63–65; the
  nine-then-tenth pattern occurs 14 times; τρίτον ἦμαρ three times [rev #8;
  txt §3]. "ἀπ' οὐρανοῦ ἀστερόεντος" (20.113) is a stock epithet, used in
  daylight at Od. 9.527, and the scene follows the dawn at 20.91 [rev #24a].
- **The slot matrix of the negatives** [neg §5]: no clean negative fills all
  five Odyssey slots; the Mercury slot exists only in the Iliad (24.339–345)
  and in Virgil's imitation of Od. 5 (*Aen.* 4.238–258); the morning star in
  every poem closes a night of action; the poets' literal Moons are mostly
  lit, and a Day-0 conjunction is everywhere an inference.

### 2.6 Controls: what is already known about them

**The *Almagest* records of B&M's own clue types** [alm §0, §4], measured
against DE441 with the true dates (so these are truth-side facts):

- Mercury, 14 records put at or about greatest elongation: within 1 d of
  the true greatest elongation 3/14, within 2 d 7/14, within 3 d 9/14, within
  4 d 12/14, within 5.5 d 14/14. The elongation stays within 0.5° of its
  maximum for 5–10 days.
- Venus, 8 records: 2 within 2 d (Ptolemy's X.3.2 pair), the other 6 at
  16.1–20.6 d, on a 34–35-day plateau within 1° of the maximum.
- At B&M's ±1 d, the true dates satisfy every greatest-elongation clue of
  only 2 of the 9 sets that carry one (ALM-A as printed, ALM-E). ALM-C needs
  3.4 d, ALM-G 5.5, ALM-H 3.6 (emended), ALM-K 2.9; ALM-D, F and L need
  16–21 d.
- B&M's Mercury proxy is a different event: for 7 morning greatest-elongation
  records the nearest rising-azimuth maximum lies −2.5 to +31.8 d away, only
  2 within ±3 d. Every Venus morning record rises 125–220 min before the Sun,
  so B&M's ≥ 90-min test does not discriminate.
- Oppositions within 1.8 d of the true-Sun opposition (0.42 d of the
  mean-Sun one); planet–star relations within 1.7 d; Moon–planet positions
  within about 2 h of lunar motion; IV.6.14 mid-eclipse 0.02 h from
  Ptolemy's time at umag 0.84 against his 5/6; the III.1.10 equinox 0.87 d
  late.
- Ptolemy's own solar tables reproduce his stated mean Sun for 32 of 34
  records to ≤ 0.12°; the two failures are textual cruxes carried as forks
  (IX.7.11 one Egyptian month, IX.9.4 three days) [alm §1.3–1.4; lca].

**The real eclipse records** (`controls_real.json`) [pcr §1, §5; lcr]:

- The clue file was frozen before any accepted date was looked up
  (SHA-256 `eb1f0401…9256`, 2026-10-04 05:19 UTC), then licence-checked by an
  agent blind to the truth, who moved seven unstated-site primaries to
  "none" and made seven other edits (SHA-256 `135fba67…83f8`) [lcr].
- **The drafting was not fully blind.** The drafter had seen critique issue
  2 and revision 1's I2b row and flags three primaries as possibly steered:
  T1-DARK, D-ECL and the tolerance in L4-DARK [pcr §1]. Section 6.3.3 has
  them re-drafted by an unexposed agent and measures whether gate 3a depends
  on them.
- A post-freeze check with a **rough** lunar model (not the bench's;
  instrument check I4 not run) found that the accepted dates fail some
  primary readings: two magnitudes in R-PTOL-BAB, one mid-time in
  R-PTOL-ALEX (so also R-PTOL-CHAIN), and the season and Moon altitude in
  R-PYDNA. All primaries pass for R-THUC, R-XEN, R-ARBELA and R-DIOD. The
  accepted Pydna eclipse fell about 5 days before the solstice, so Livy's
  "after the solstice" is wrong [pcr §5; truth file]. The values are kept on
  the truth side.
- Moving the site primaries to "none" weakens R-THUC and R-XEN in the
  primary run [lcr, Consequences].

**The negatives** (`negatives.json`): 13 sets (12 clean negatives and the
Iliad as a same-tradition comparison), 70 clue rows, 34 excluded rows; all
209 licence fragments match the cited rows; no date leaks [neg; lcn].

### 2.7 Revision 1's predictions that are now settled

| v1 prediction | status | numbers |
|---|---|---|
| 1–5 (T0) | largely implied by 2.2 | kept in section 8 as regression expectations, not counted |
| 18 (mixture P(total) 0.15–0.40; P(mag ≥ 0.9) ≥ 0.8) | **holds already** | mixture 0.304 (canon frame), 0.309 (pairing rule); P(smag ≥ 0.9) 0.928 (2.3) |
| 19 (1131 higher under every model; joint ≤ 0.05) | **fails as written** | SMH2016 parabola gives 0.498 vs 0.443; joint 0.108 (SMH2016) and 0.052 (Addendum) exceed 0.05 [rev #17]. Restated per model as P26 |
| 20 (< 2% of dates flip) | sits on its threshold | about 1.9% [rev #17] |
| 21 (PC-S recall ≥ 0.99 at zero noise) | tautological as built | replaced by the two PC-S modes [rev #14] |
| 24 (NC4 zero survivors, NC5 never unique) | true by construction | moved to instrument check I11 [rev #15] |

---

## 3. T0: reproduction

### 3.1 T0a: replay of Table S2 (done)

T0a is complete (2.2). It becomes the regression test `tests/test_t0.py`,
which replays S2's printed values and colours, so that every later change to
the rules is checked against the published table.

### 3.2 T0b: B&M's search recomputed with DE441

T0b reproduces B&M's procedure as written, on DE441, with their clock. It uses
DE441 for the Moon as well, because that is the pairing on which the S2
agreement of 2.2 was measured; the bench proper uses the pairing rule of
section 0, and prediction P27 checks that the T0b survivor set does not move
under it. The steps:

1. **Candidates.** Every geocentric conjunction in apparent ecliptic
   longitude whose UT+2 instant falls in the half-open window
   [−1249 Jan 1 00:00 UT+2, −1113 Jan 1 00:00 UT+2), i.e. through 24:00 UT+2
   on 31 Dec −1114, computed as
   `calendar.span_bounds((-1249,1,1), (-1114,12,31), offset_hours=2)`.
   UT = TT − 27,602.7 s. Expected count 1,683 [rev #22; P7].
2. **Ti** is the UT+2 civil date of the conjunction.
3. **C (fixed Julian).** Ti−29 ≥ 17 Feb and Ti−12 ≤ 4 Apr of the same Julian
   year, with true Julian day arithmetic (29 Feb counted). Where two New
   Moons in a year pass, both are evaluated (S2 lists one by no consistent
   rule [bm §7]).
4. **V.** On Ti−5: Venus a morning object rising ≥ 90.0 min before the Sun.
5. **M.** Every morning over Ti−34 ± 60 d: Mercury's azimuth (north through
   east) at its rising instant, with rise times bisected until converged to
   better than 0.1 s [rev #12 fix 2]. Two definitions are computed:
   - **MWRA_vtx (primary):** the vertex of a least-squares parabola through
     the daily azimuths of the 7 mornings centred on the discrete local
     maximum nearest Ti−34; Δ = (Mercury's rising instant on Ti−34) − (vertex
     instant), continuous, in days [rev #12 fix 1].
   - **MWRA_int (B&M literal):** the civil date of that discrete maximum;
     Δ = (Ti−34) − MWRA_int in whole days; equidistant maxima resolve to the
     earlier.

   Pass if \|Δ\| ≤ 1. Every maximum records its curvature (deg/d²) and its
   margin over the larger neighbouring day; it is flagged **flat** if the
   margin is below 0.001° or the curvature below 0.002°/d² [rev #12 fix 3].
   Mercury's visibility on Ti−34 is recorded three ways: Sun at Mercury's
   rising ≤ −10° (Ptolemy's AV [vis §2.2]); PLSV's AV = 10.5 + 1.4m at a 1°
   critical altitude (the defaults B&M's software used [unread §6]); and not
   required (S2 never tabulated it [bm §5 M]).
6. **E** (reported, not applied): 1 Apr ≤ Ti−11 ≤ 4, 5 or 6 Apr, and the
   computed equinox date.
7. **Parallel reckoning** (reported): steps 3–6 at −28/−12…−11, −4, −33,
   −10 [B&M Table 1].
8. **Output** an S2-shaped table for every candidate
   (`results/t0/candidates.tsv`), the survivor sets of every criterion and
   combination, and the 1178 BC row.
9. **Comparison with S2**: Ti agreement by zone, Venus pass-set equality,
   MWRA agreement (exact and ±1 d), Δ agreement, leap-day effects.
10. **M sensitivity** [rev #12 fix 4]: the M pass set under h0 ± 0.1°,
    latitude 38.2°–38.6° in 0.1° steps, refraction on and off, and the clock
    ΔT ± 720 s.

| parameter | value | source |
|---|---|---|
| planets, Sun, Moon | DE441, `data/ephem/de441_m2060_p0241.bsp` (the shortest covering excerpt is used, with bit-identical records) | [acq §1] |
| precession, sidereal time | Vondrák 2011 long-term model, module default | [eph §3] |
| site | `bm`: 38.4°N 20.7°E, sea level | S2 clock fit [bm §3.2] |
| clock | UT+2 | S2 sunrise − DE441 UT sunrise = +120.0 min, sd 1.6, n = 75 [bm §3.2] |
| ΔT (clock only) | 27,602.7 s, constant | [B&M §Method; bm §3.1] |
| rise definition | airless geometric altitude of the centre at h0 = −0.8333° (Sun) and −0.5667° (planets) | settings that reproduce S2 [bm §3.2] |
| New Moon | apparent ecliptic-longitude conjunction, UT+2 civil date | 136/152 [bm §5 N] |
| window | half-open UT+2 bounds above | [B&M §Method; rev #22] |
| C bounds | Ti−29 ≥ 17 Feb, Ti−12 ≤ 4 Apr (fixed Julian; T0b only) | [bm §5 C; rev #9] |
| V threshold | lead ≥ 90.0 min on Ti−5 | [B&M §References; bm §5 V] |
| M event | MWRA_vtx (primary), MWRA_int (literal) | [rev #12] |
| M tolerance | \|Δ\| ≤ 1 d; 2, 3 reported | S2 colours [bm §5 M] |
| M visibility | off, AV 10°, PLSV | [rev #23; unread §6] |
| day arithmetic | true Julian (`odybench.calendar`); S2's 365-day arithmetic reported beside it | [bm §5 M] |
| E | 1 Apr ≤ Ti−11 ≤ 4 / 5 / 6 Apr | [B&M §References, §Intersecting; rev #23] |
| offsets | sequential 0, −5, −11, −12, −29, −34 | [B&M Table 1] |

### 3.3 T0c: the eclipse statements

For 16 Apr 1178 BC (−1177) the bench computes local circumstances at the
five Ionian sites under each pairing and the constant-ΔT window for totality:

| pairing | why |
|---|---|
| NASA 5MCSE elements, canon ΔT 28,590 s | the canon B&M quote |
| DE431 + each SMH model (SMH2020, Addendum parabola, SMH2016 parabola) | SMH's ΔT is tied to the DE430 lunar model |
| NASA elements + Espenak–Meeus canon form | its own pairing |
| DE441 + SMH2020 | the bench's planetary ephemeris, reported beside |
| DE441 + 27,602.7 s | what B&M printed; mixes ephemerides, reported only to show it |

Values already known are in 2.3. The canon identity (catalogue 01966, Saros
39 member 31) is A5. On B&M's statement that Ithaca lay on the edge of
totality: **consistent** if Ithaki is total for some ΔT within 1σ of the
SMH2020 value in the DE431 pairing (known: +0.3σ to +1.4σ, so consistent);
B&M's own 27,602.7 s is **uninterpretable** for eclipse geometry (2.3).

### 3.4 Regression checks

These thresholds were set at values already measured, so they are labelled
what they are: **regression tests** that the code reproduces known numbers.
They do not test whether DE441 agrees with B&M's software [rev #20].

| check | pass | measured |
|---|---|---|
| A1 Ti | DE441 UT+2 conjunction dates match S2's Ti in ≥ 134 of 152 rows | 136 [bm §5 N] |
| A2 Venus | DE441 pass set on S2's own Ti equals S2's orange set; S2 lead times reproduced with sd ≤ 3 min | 25/25; sd 1.5 min [bm §3.2, §5 V] |
| A3 MWRA | ≥ 124/152 exact and ≥ 138/152 within ±1 d (integer definition) | 124 and 138 [bm §5 M] |
| A4 1178 BC values | Venus lead 103.6 ± 1 min; conjunctions 18 Mar 03:31 and 16 Apr 12:25 UT+2; equinox within 10 min of B&M's 15:24; Sun at −12° on 18 Mar within 5 min of B&M's 19:38 | 103.6; 03:31, 12:25; 15:31; 19:34 [bm §3.2, §9] |
| A5 canon identity | catalogue entry and greatest-eclipse point as in 2.3 | matched [rev V4] |

### 3.5 The T0 verdict

T0 is computed on a grid: E bound ∈ {≤ 4, ≤ 5, ≤ 6 Apr} × Mercury visibility
∈ {off, AV 10°, PLSV} × MWRA ∈ {vtx, int} [rev #23]. In every cell:

- **R, reproduced as stated:** 16 Apr 1178 BC passes N, C, V and M and is the
  only candidate that does.
- **RE, reproduced only with the equinox:** not R, and 1178 BC is the only
  candidate passing N, C, V, M and E.
- **NR, not reproduced:** neither; the report names the failing criterion
  and its margin.

The **primary cell**, used by the decision rule as `T0`, is E ≤ 5 Apr (B&M's
§References), visibility off (S2's table), MWRA_vtx. The whole grid is
reported. Expected (P5): RE in the primary cell, NR under E ≤ 4 Apr.

---

## 4. Shared machinery

### 4.1 Spans and coverage

- **Background** B = −1999-01-01 to −600-12-31 (1,400 Julian years), the
  first year of NASA's elements [acq §2.1] to the end of the earlier scans.
  Revision 1's −1499..−599 is extended [rev #10 fix 2].
- **Data margins** −2060..−540, for the 40-day clue offsets and the ±60-day
  Mercury searches.
- **Target core** −1748..−851: targets must lie at least 251 years inside B
  so that every window of every width lies inside it. One core serves all
  widths, so gardens of different widths share their targets. It contains
  1312, 1178 and 1131 BC.
- **Controls**: PC-R windows fall within −856..+272 and ALM windows within
  −407..+277. DE441 and DE431 must be extended to +300 before they run
  (section 11).

### 4.2 Candidate pools (Ithaki unless a rule names another site)

- **P_all**: every geocentric apparent-longitude conjunction, computed with
  DE431 (yearly chunks) and SMH2020 ΔT for UT.
- **P_day**: conjunctions whose instant falls in daylight at the site (Sun's
  centre above −0.8333°): 50.9% of them at Ithaca [vis §4.2]. Only these can
  give a visible solar eclipse.
- **P_spring**: conjunctions passing C_rel (4.5).
- **Targets** T = P_day ∩ core.

### 4.3 Sky tables and events

Every daily quantity the clues need is tabulated once per site over the
span, by `odybench/sky.py`, and the events derived from them by
`odybench/events.py` (interfaces in 10.2): rise and set times and azimuths
of the Sun, Moon, Mercury, Venus, Mars, Jupiter and Saturn; Sun altitude at
each planet's rising and setting; signed elongation; V magnitude; ecliptic
longitude and latitude; civil, nautical and astronomical twilight; the
altitudes of the grammar stars (Alcyone, Arcturus, Sirius, Aldebaran,
Betelgeuse, Rigel, Dubhe, and the Hyades, Orion and Boötes extras of
`data/stars.json`) at the end and start of nautical twilight, and their rise
and set times; the Moon's illuminated fraction and its share of the dark
hours above the horizon; night length. From these: stations, greatest
elongations (from the true and the mean Sun), oppositions, rise- and
set-azimuth extrema (parabola vertex, as in T0b), first and last visibility
at the AV values of the forks, heliacal star phases, equinoxes and
solstices, conjunctions, full moons, and the first-crescent evening by
Yallop's q-test [vis §4.2]. None of these derived events has yet been
validated against anything; instrument checks I5, I6 and I12 do that
[rev #13].

### 4.4 Eclipse hit strength (replaces the classes X1–X4)

Revision 1's binary classes were defined around the target and estimated
from it: in −1499..−600 its class X1 held three events, of which only the
target was a spring new moon [rev #10]. The bench now uses a probability.
For a conjunction u and a site s, h = 0 if u is not a solar eclipse; else:

- **h_tot(u, s)** = P(the eclipse is total at s, with maximum in daylight),
  under the four-model ΔT mixture, integrating each model's Gaussian over the
  totality window computed on NASA's elements in the canon frame;
- **h_09(u, s)** = mixture P(smag ≥ 0.9, Sun up at maximum);
- **h_06(u, s)** = mixture P(smag ≥ 0.6, Sun ≥ 10° at maximum), the darkness
  that the wording of Hdt. 9.10 and Plut. *Pel.* 31 went with [ctl §0 item 3].

**M_Ody** := h_tot(16 Apr −1177, ithaki), the Odyssey's own eclipse strength
(0.304 on the known numbers; recomputed by `eclipses.py`). Wherever the
decision rule asks for an eclipse "at least as strong as the Odyssey's", it
means h_tot ≥ M_Ody.

Reported beside, never in the rule: the time-of-day variants (maximum
10–12 h LAT, which is Schoch's rule [unread §3.1], and 10–14 h LAT), and
revision 1's envelope classes "total for some ΔT within ±0.5σ, ±1σ, ±2σ"
[rev #10 fix 4]. Base rates: p_e(m) is the fraction of P_day conjunctions in
the background with h_tot ≥ m, with **the target itself excluded** from every
base rate it is compared with [rev #10 fix 3], and a site-rotated estimate at
Ithaki's latitude over 36 longitudes, which does not depend on Ithaca's
particular eclipses [rev #10 fix 2].

### 4.5 Season and equinox bounds relative to each year's sky

B&M's fixed Julian cut-offs drift: the Julian year runs about 0.76 d per
century ahead of the equinox, and the star phases drift about 0.64 d per
century the other way [rev #9]. Outside T0b every season and equinox bound is
computed for each year:

- **C_rel (B&M-calibrated).** For each Julian year y, A(y) is the first
  evening on which Arcturus stands at least h_A high at the end of evening
  nautical twilight (Sun −12°), and P(y) the last evening on which Alcyone
  stands at least h_P high then. h_A and h_P are fixed once, so that
  A(−1177) = 17 Feb and P(−1177) = 4 Apr, B&M's applied bounds [bm §5 C]; if a
  range of values gives the date, its midpoint is taken. C_rel passes if
  Ti−29 ≥ A(y) and Ti−12 ≤ P(y). The calibration fits B&M's printed bounds,
  not a sky outcome, and it makes C_rel identical to the fixed bounds at
  −1177 (at 2° the Pleiades' last evening is 3 Apr, which would drop 1178 BC
  by a day [vis §3.3, §4.3]; that reading is fork F3(b)).
- **E_rel.** Ti−11 lies in [eq(y), eq(y) + n] days, eq(y) being the civil
  date of the computed March equinox (apparent solar longitude 0°), with
  n ∈ {3, 4, 5}, matching ≤ 4, 5 and 6 Apr at −1177, where the equinox falls
  on 1 Apr [bm §9].
- N1 reports λ per century under both the relative and the fixed bounds
  (P13).

### 4.6 Windows

In `data/prereg/windows.json`: reproduction 1250–1115 BC (−1249..−1114,
136 years, half-open UT+2 bounds); primary 1350–1100 BC (−1349..−1099,
251 years); Troy VIIa 1240–1150 BC (−1239..−1149, 91 years); strict
Eratosthenes return 1176–1172 BC (−1175..−1171); background as 4.1 [win §9].
A window of width W years is the half-open JD interval [a, a + 365.25 W).
Control window positions come from `data/prereg/seeds.json`.

---

## 5. Null models

### 5.1 N1: how often B&M's criteria pass by chance

1. Evaluate the **B&M reading** on every candidate in the background: B&M's
   criteria with C_rel and E_rel (4.5), MWRA_vtx, SMH2020 ΔT, site
   `ithaki`.
2. **Rate.** λ = survivors per century, with a Poisson 95% interval, for
   N ∧ C ∧ V ∧ M and for N ∧ C ∧ V ∧ M ∧ E (n = 3, 4, 5).
3. **Two comparisons with B&M** [rev #5]:
   - λ(N ∧ C ∧ V ∧ M ∧ E) against B&M's printed 0.048 per century: B&M as
     written (P9);
   - λ(N ∧ C ∧ V ∧ M) against B&M's own arithmetic redone at their stated
     ±1-day tolerance, 0.88 per century (P8).
4. **Stationarity.** λ per century for each of the 14 centuries, under C_rel
   and E_rel and under the fixed Julian bounds (P13).
5. **Windows.** Slide windows of W = 50, 91, 100, 136, 200, 251, 500 and 900
   years along the background one year at a time; report the empirical
   P(≥ 1 survivor) and the mean count beside the Poisson values. Venus' 8-year
   cycle and Mercury's 13- and 46-year near-repeats cluster survivors; the
   empirical figure includes that.
6. **Per-target rates** [rev #6]. **p_fix|C** (primary) = the fraction of
   P_spring passing V and M: the chance that a target fixed in advance passes
   criteria fixed in advance, given the season. **p_fix** (unconditional) =
   P(C ∧ V ∧ M) over P_all, reported as the counterfactual "C independent of
   the target". The reason for making the conditional figure primary is
   frozen here: the spring reading of C first appears in MacDonald 1967, in a
   paper that already holds the eclipse and fits its timetable to it, and
   before Schoch every season reading was autumn or winter [unread §2.4];
   nothing documents an eclipse-blind spring reading.
7. **Independence.** B&M multiply marginal rates [bm §10]. The joint pass
   count of V and M on P_spring is compared with the product of the
   marginals; the null distribution permutes the Venus outcome among
   candidates with the same Ti day of year (± 3 d), 10,000 times.
8. **Without N.** Repeated with Day 0 any day, to show what N contributes.

### 5.2 N2: the eclipse coincidence

The question: if the criteria had nothing to do with eclipses, how often
would a date they pick be an eclipse new moon at least as strong as the
Odyssey's?

1. **Base rates** p_e(m) over P_day and P_spring, for m = M_Ody and as a
   curve over m (4.4). The pool is new moons, never days: an eclipse can
   only fall on one, and using days would inflate the coincidence about
   29.5-fold [v1 §3.3].
2. **Fixed reading, target first:** P(a target with h_tot ≥ M_Ody passes V and
   M | C) = p_fix|C, under the independence of item 4.
3. **Fixed reading, survivors first:** with s survivors in a window holding n
   candidates, P(≥ 1 survivor with h_tot ≥ m) by the hypergeometric tail, and
   its h-weighted analogue Σ over survivors of h_tot.
4. **Independence of clues and eclipse status.** No clue involves the lunar
   node, so V and M outcomes should not depend on eclipse status once the
   pool is spring new moons. N2 tests this: V and M pass rates on
   eclipse (h_tot > 0 at any of the five Ionian sites) and non-eclipse spring
   new moons, by permutation (P15). Every analytic shortcut below (5.4, 5.7)
   rests on this check.
5. **Background double hits:** survivors of the B&M reading with h_tot ≥ m
   at Ithaki, per century, beside the count expected from the site-rotated
   p_e (the sky clues are evaluated at Ithaki only; the rotation changes only
   which conjunctions are eclipses).

### 5.3 N3: forking paths

B&M's criteria were not fixed in advance (1.1). N3 counts the readings a
careful reader could defend, sorts them by who has defended them, and asks
how often *some* reading makes a given target the unique match.

**The forks.** Each option carries its source and its tier in
`data/prereg/garden.json`. "None" means the clue is dropped. Tier BM holds
the options B&M themselves raised; tier DOC adds options with a named
published proponent for this passage, or the standard published
operationalisation of what such a proponent says; tier FULL adds the rest
[rev #7].

| fork | option | tier | source |
|---|---|---|---|
| F1 day count | B&M sequential (34/29/5) and parallel (33/28/4) | BM | [B&M Table 1; chron §5.1] |
| | de Jong 2001 (33/28/5), Stanford 1959 (32/27/4) | DOC | [chron §0 item 4] |
| | the four inclusive-raft rows | FULL | [chron §5.1] |
| F1b typical numbers [rev #8] | off | BM | — |
| | every offset that depends on a typical-number joint (H→D "fourth/fifth", D→Σ "seventeen/eighteenth", Σ→L "two nights … third", "twentieth") uncertain by ±2 d; or by ±3 d | DOC | Gainsford's objection that the counts are formulaic [crit §3.3]; 5.278–279 = 24.63–65 [rev #8]; [txt §3] |
| | D→Σ replaced by another typical number, 9, 12 or 20 days | FULL | [rev #8 fix 1] |
| F2 Day 0 | (a) conjunction date, UT+2 | BM | [B&M] |
| | (c) the day after, Solon's noumenia; (d) the first-crescent day, Yallop B, day counted from sunset | DOC | Plut. *Sol.* 25.3; Geminus 8.11 [vis §4.1] |
| | (b) conjunction date, LMT | FULL | a clock convention, not a reading |
| F3 stars | (a′) C_rel, B&M-calibrated (4.5) | BM | [B&M; MacDonald 1967, unread §2] |
| | (e) autumn: every raft night inside the autumn co-visibility window (both stars ≥ 2° at the end of nautical twilight), recomputed each year; (f) none, "late-setting" as a permanent property | DOC | (e) Papamarinopoulos et al. 2012 [unread §4] and the scholia's season [txt §5.6]; (f) the scholion on 5.272 and Aratus 581–585 [vis §3.1] |
| | (b) both ≥ 2° on every raft night; (c) both ≥ 5°; (d) departure night only, ≥ 2°, either season | FULL | [vis §3.3–3.4] |
| F4 morning star | Venus rises ≥ 90 min before the Sun | BM | [B&M] |
| | Venus a visible morning star (AV 7°); none (a dawn time-marker) | DOC | MacDonald identifies the star as Venus near morning elongation [unread §2.5], AV from de Jong [vis §1.2]; Gainsford's formula argument [crit §3.3; txt §5.7; neg §5 item 3] |
| | ≥ 60 min; ≥ 120 min; any bright dawn herald (Venus, Jupiter, Sirius, Mars ≤ −1 mag) | FULL | [vis §1.3–1.4] |
| F5 Mercury | event MWRA, GWE or morning station × tolerance 1, 2, 3 d × visibility (AV 10°) required or not: 18 options | BM | B&M name all three events and require visibility; S2 never applied it [B&M §References; bm §5 M; rev #23] |
| | event "any of the three"; tolerance 6 d (the slack of Ptolemy's own Mercury records, 14/14 within 5.5 d [alm §4]); morning first visibility (AV 10°) at 1, 2, 3 or 6 d; none | DOC | B&M call the events close in time; the *Almagest* records; B&M's "heliacal rising 13 Mar" [bm §9]; Gainsford and the absence of any ancient Hermes–Mercury link before Plato [txt §5.9] |
| F6 equinox | off; E_rel with n = 3, 4, 5 | BM | [B&M §References, §Intersecting] |
| F7 window width | 136 years | BM | [B&M] |
| | 91 (Troy VIIa) and 251 (primary) years | DOC | [win §4, §9] |

**Garden sizes** [me: products of the option counts].

| garden | F1 | F1b | F2 | F3 | F4 | F5 | F6 | F7 | readings | bits |
|---|---|---|---|---|---|---|---|---|---|---|
| 𝒢_BM | 2 | 1 | 1 | 1 | 1 | 18 | 4 | 1 | **144** | 7.2 |
| 𝒢_DOC | 4 | 3 | 3 | 3 | 3 | 37 | 4 | 3 | **143,856** | 17.1 |
| 𝒢_FULL | 8 | 6 | 4 | 6 | 6 | 37 | 4 | 3 | **3,068,928** | 21.6 |

F5's 37 in DOC and FULL is 4 events × 4 tolerances × 2 visibility settings,
plus first visibility at 4 tolerances, plus none. **T0b's own reading (in its
C_rel/E_rel form, visibility off) is a member of 𝒢_BM** [rev #23]. Only F2
(a) and (b) put the conjunction on Day 0, where Theoclymenus speaks
[chron §4.H], so the **eclipse-compatible** subsets are 𝒢_BM itself (144),
𝒢_DOC^X (47,952) and 𝒢_FULL^X (1,534,464).

Two readings are left out because they cannot change the result: Day 0 as a
20-day window, and N dropped. Their candidates are days, a superset of the
conjunction dates, so they add no reach for any New Moon target [v1 §3.4;
rev §1 confirms].

**The statistic: reach.** For reading r, let S_r be its survivors over the
background, each mapped to its conjunction (under F2 (c) and (d) a candidate
is mapped back). A target t ∈ S_r is the unique survivor of a W-year window
[a, a + W) placed at a uniformly random start a with t inside exactly when
the window misses the neighbouring survivors s₋ and s₊, that is for
a ∈ I_r(t) = (max(t − W, s₋), min(t, s₊ − W)]; if t ∉ S_r, I_r(t) is empty.
Over a garden 𝒢, **reach_W(t; 𝒢) = |∪_{r∈𝒢} I_r(t)| / W**. For gardens with
several widths, reach(t) = max over W of reach_W(t), a lower bound on the
union [v1 §3.4]. Under T0b with E off, reach_136(1178 BC) ≤ 0.081 and is 0
if a survivor falls in −1176..−1052 [rev #24c; P16]; revision 1's statement
that it "is 0 unless E is on" was wrong.

**The G statistics.**

- **G(𝒢) = mean of reach(t; 𝒢) over the season-matched targets
  T_C = T ∩ P_spring**: the probability that a daylight new moon of the
  target's season, fixed in advance and with no relation to the text, is
  made the unique match by some reading of 𝒢 in a window placed at random
  around it. This is the look-elsewhere-corrected p-value of a coincidence
  whose target was fixed first, as Schoch's was. The targets are restricted
  to the season for the reason that makes p_fix|C primary (5.1 item 6): the
  spring reading was formed with the target in view, so the target's
  agreement with it is not part of the coincidence. **G_BM** uses W = 136
  only; **G_DOC** and **G_FULL** use the max over F7's widths. Each has a
  binomial interval over T_C.
- **G_u(𝒢)**, the same mean over all of T: the counterfactual "season
  independent of the target", reported beside, and used where a text without
  a season clue is compared with the Odyssey (outcome 4, 6.5).
- **G_any(𝒢)** = the fraction of targets with reach > 0: the chance that
  *some* window position and some reading would make a random target unique.
  Reported beside G, because B&M's window was itself drawn from the tradition
  that chose the eclipse [win §6].
- **G_X(𝒢)** = the h_tot-weighted mean reach over eclipse new moons in T,
  with 16 Apr −1177 excluded, compared with G_u (spring eclipses alone are
  too few). If eclipse new moons are reached at the rate of other new moons
  (P21), the eclipse adds nothing beyond its rarity.

**Reported:**

1. reach(16 Apr 1178 BC) under the T0b reading, 𝒢_BM, 𝒢_DOC and 𝒢_FULL.
2. G, G_any and G_X for every garden, with intervals.
3. **The smallest fork set that reaches G ≥ 0.05**, by greedy addition to
   𝒢_BM of the option that raises G most, until G ≥ 0.05; the sequence and
   each option's source are printed [rev #7].
4. The look-elsewhere factor G_BM / p_fix,unique, where p_fix,unique is the
   same quantity for the B&M reading alone.
5. **Alternative datings.** Every eclipse new moon with h_tot ≥ 0.1 at any
   Ionian site that some eclipse-compatible reading makes unique, with the
   readings that do it. Listed whatever the result: 30 Sep 1131 BC (total at
   Ithaki at canon ΔT, inside B&M's window [rev V6]), 24 Jun 1312 BC (the
   Iliad date of Henriksson 2012 [unread §5]), 30 Oct 1207 BC
   (Papamarinopoulos et al. 2012 [unread §4]) and 12 Jan 1183 BC (−1182;
   Schoch's rejected annular eclipse [unread §3.1]; research-window's "1182
   BC" for the same catalogue row is a slip [win §7.2]).
6. Survivors per century for every reading, so the strictness of each garden
   is visible.

**R_anc, the ancient reading** [rev #18]. A pinned reading formed without
knowledge of any computed eclipse, from the scholia, Heraclitus and
Plutarch:

- Day 0 = the conjunction date (LMT at Ithaki): the scholia's ἕνη καὶ νέα on
  14.162 and Heraclitus [txt §5.1];
- season: the Sun's apparent longitude on Day 0 in [180°, 270°), "autumn,
  and already towards winter" (scholia on 11.373, 17.24, 17.191, 14.458,
  6.305 [txt §5.6]); sensitivity [150°, 300°);
- Theoclymenus' vision as a solar eclipse on Day 0 (Heraclitus; Plutarch,
  *De facie* 19 [crit §3.1]): h_06(u, ithaki) ≥ 0.5;
- no planets, no stars (the scholia read 5.272 as slow-setting).

R_anc's survivors in each window, whether one is unique, their h_tot, and
whether 30 Sep 1131 BC is among them are reported beside B&M's. R_anc is the
natural control for the circularity argument, and it cuts both ways. It is
not in the decision rule. The held-out predicates (section 7) are also run on
R_anc's survivors.

### 5.4 N4: random epics, the main negative

N3 holds the poem fixed and varies its reading. N4 holds the reading
machinery fixed and varies the poem. Random poems of the Odyssey's grammar
are the main negative of the bench [rev #15 fix 3]: they set the percentile
that outcome 1 requires and the survivors-first ratio of 5.7.

**The grammar** (`data/prereg/epic_grammar.json`, unchanged from revision 1
except that season clues are relative to each year's sky):

- **Day 0 anchor:** conjunction, full moon, the 7th day of the month (Apollo's
  day in Hesiod, *WD* 770–771 [txt §5.3]), or none.
- **Season clue:** a pair from the archaic star list (Pleiades, Hyades, Orion,
  Sirius, Arcturus [txt §5.8]), both ≥ 2° at the end of evening or morning
  nautical twilight on one night or on a 17-night span, or one star's
  heliacal rising or setting within ±k days.
- **Planet clue:** Venus, Mercury, Mars, Jupiter or Saturn; morning object
  with rise lead ≥ 60/90/120 min, evening object with set lag ≥ 60/90/120
  min, or within ±1–3 days of a turning point (rise- or set-azimuth extremum,
  greatest elongation, station, opposition) or of first or last visibility
  (Ptolemy's AV: Venus 5°, Mercury 10°, Jupiter 10°, Mars 11.5°, Saturn 11°
  [vis §1.2]).
- **Offsets:** variant A ("B&M-shaped") puts a season clue on a span starting
  between −29 and −27 and two planet clues at −5 and −34 around a
  conjunction anchor, clue types drawn at random. Variant B draws the anchor,
  two or three sky clues and their offsets (−40 to −1) freely.

10,000 epics per variant (seed in `seeds.json`), site `ithaki`, evaluated
over the background.

**Per epic:**

- p_c, its primary reading's per-candidate pass rate (its specificity);
- the survivor count in a 136-year window at a random position, and
  P(unique);
- **T_best ≥ T_obs**: each date is scored by −log10 of the product of the
  per-clue base rates at the observed tightness (P(Venus lead ≥ observed),
  P(\|Δ\| ≤ observed), …); T_obs is that score for 1178 BC under the B&M
  reading; the statistic is P(T_best ≥ T_obs) over epics.

**The specificity stratum.** Epics whose p_c lies within a factor 2 of the
Odyssey's (B&M reading) form the stratum; if fewer than 200 epics fall in
it, the factor widens to 4 and the report says so.

**Epic gardens.** Each stratum epic gets a garden built with the same fork
types and multiplicities as the Odyssey's tier: the BM-tier epic garden has
the two-offset day-count fork, 3 turning-point events × 3 tolerances × 2
visibility settings for one planet clue, and an optional season tightening
with 4 settings (144 readings when the epic has those slots); the DOC-tier
epic garden adds the DOC fork types and is subsampled to 1,000 readings, as
is the Odyssey's DOC garden for this comparison only.

**The calibrated percentile (target first).** Schoch's target was fixed
before any reading. For each stratum epic, r_e = reach_136(16 Apr −1177;
the epic's garden) is the chance that this poem, read with the same freedom,
makes Schoch's eclipse new moon the unique match of a window placed at
random around it; r_Ody is the same for the Odyssey under 𝒢_BM.

- **pct_N4(tier)** = the fraction of stratum epics with r_e ≥ r_Ody (ties
  count against the Odyssey): the Odyssey's percentile among random poems
  of the same specificity [rev #1 fix 2], with a binomial 95% interval whose
  upper bound is pct_N4,hi. As G conditions on the target's season, so does
  pct_N4: only epics whose season clue (if they have one) holds for Schoch's
  target enter it. It varies the poem and holds the target; G
  varies the target and holds the poem; under the null they estimate the same
  probability, and P25 checks that they agree.

**The eclipse-match strength (survivors first; reported).** For a text with
garden 𝒢 in a window, M = max over eclipse-compatible readings r of
h_tot(u_r, ithaki), where u_r is r's unique survivor in the window (0 if
none). For each stratum epic, M_e is computed in a window at a random
position, and **p_N4(tier)** = the fraction with M_e ≥ M_Ody. If fewer than 20
epics reach it, p_N4 is computed analytically as the mean over stratum epics
of K_e × p_e(M_Ody), K_e being the number of distinct unique survivors across
the epic's eclipse-compatible readings, which relies on N2's independence
check [rev #16 fix 4]; the direct count is reported beside it, with
bootstrap intervals. p_N4 credits the eclipse's rarity, which is evidence
only if the readings had been formed blind to the eclipse; the record says
they were not (1.1). It therefore enters only the secondary ratio LR_sf
(5.7), never the decision rule.

### 5.5 N5: window sensitivity

N1–N3 run in every window of 4.6. Reported: survivors per century, the
survivor list, the eclipse new moons in the window with their h_tot, and
P(≥ 1) as a function of W from 50 to 900 years. "The single date in the
window" is never reported without the rate beside it [win §9]. Two checks:

- **Strict Eratosthenes.** Eratosthenes put the sack in late spring 1183 BC
  (−1182); with at least 8 years of wandering [Od. 7.259–261, 10.467–470] the
  return falls in about 1175–1173 BC and 1178 BC is outside [win §5–6; rev
  V11]. The report gives the survivors, under each reading, compatible with
  each ancient sack date plus 8–11 years.
- **Gainsford's 1350–1250 BC extension**, which the primary window includes,
  and Henriksson's Iliad date (a sack about 1312 BC puts the return about
  1302 BC, outside B&M's window) [unread §5].

### 5.6 N6: ΔT and the eclipse at Ithaca

1. **Models and pairings** as in section 0: the three SMH models with DE431,
   Espenak–Meeus (canon form) with NASA's elements; DE441 reported beside with
   its offset (+188 s at −1177) [eph §5.3].
2. **Sites:** the five Ionian sites.
3. **Outputs:** magnitude and LAT of maximum as a function of constant ΔT
   from 26,000 to 32,000 s; totality windows; P(total) per model; the
   four-model mixture; P(smag ≥ 0.9); the same in the canon frame on NASA's
   elements. Known values are in 2.3; N6 recomputes them with `eclipses.py`,
   and the recomputation is an instrument check, not a prediction.
4. **30 Sep 1131 BC and 24 Jun 1312 BC** in the DE431 pairing, and joint
   probabilities under a common ΔT offset, per model (P26, which restates
   revision 1's failed prediction 19 per model [rev #17 fix 2]).
5. **ΔT and the clue tests.** Count the candidates whose civil conjunction
   date flips between 27,602.7 s and each model at ±1σ (known: about 1.9% for
   SMH2020 + 1σ), and rerun T0b at SMH2020 ± 1σ with DE431 conjunctions
   (P27).
6. **B&M's own value** is reported as uninterpretable (2.3) and is never
   converted into another frame.

### 5.7 The bottom line: a likelihood ratio on one event

The likelihood ratio compares the probability of one event under two
hypotheses [rev #16 fix 1]. Because Schoch fixed the target from the
eclipse lines before anyone read the star clues for it, the event is
target-first. **The event**: a target fixed in advance, of the target's
season, is the unique survivor of some reading of garden 𝒢 in a window
placed at random around it.

- **Numerator, R_obs(𝒢, ν).** The clues are observations: the poet watched
  the sky of the target day t* and its preceding weeks, with noise ν, and the
  analyst reads the poem with 𝒢. PC-S science mode (6.2) computes it as the
  mean reach_136 of t*, over truth dates of the target's season (the spring
  sub-pool) and noise draws. By N2's independence check, t*'s clues do not
  depend on its eclipse status, so the pool is not restricted to eclipses;
  R_obs on eclipse conjunctions alone is reported beside as a check.
- **Denominator, G(𝒢)** (5.3): the same mean reach when the target has no
  relation to the clues, over the same season-matched targets.
- **LR(𝒢, ν) = R_obs(𝒢, ν) / G(𝒢).** Both sides count the same event on the
  same class of target, and the denominator is a mean over thousands of
  targets, so it is not under-sampled [rev #16 fix 4].
- **LR_sf(𝒢, ν) = R_obs(𝒢, ν) / p_N4** (survivors first: a random poem's
  unique survivor happens to be an eclipse at least as strong as the
  Odyssey's) is reported beside it. It is the ratio revision 1 intended; it
  credits the eclipse's rarity, so it would be the right ratio only if the
  readings had been formed blind to the eclipse.

**Noise** [rev #16 fix 2–3]. ν is a grid: offset jitter j ∈ {0, 1, 2, 3}
days applied independently to every clue offset of the poem, and a
displacement s_M ∈ {0, 3, 6} days of Mercury's turning point from the stated
day. There is no Venus slack: the *Almagest*'s 16–21-day Venus slack was
measured on greatest-elongation records, while B&M's Venus clue is a rise-lead
threshold that every *Almagest* Venus morning record passes with a large
margin [alm §0 item 7, §5 item 3]. Two summaries:

- **ν_real** = (j = 1, s_M = 3): the sequential–parallel ambiguity [chron §5]
  and a Mercury displacement that covers 9 of Ptolemy's 14 greatest-elongation
  records (their median is about 2.2 d [alm §4]). **LR_real(𝒢) = LR(𝒢, ν_real)**, with bootstrap 95% interval
  [LR_real,lo, LR_real,hi].
- **LR_fav(𝒢) = max over the grid**, the noise most favourable to B&M, with
  its interval [LR_fav,lo, LR_fav,hi].

LR is reported as a full curve over ν for 𝒢_BM and for 𝒢_DOC; for 𝒢_DOC,
R_obs and G are both computed on the same 1,000-reading subsample. Intervals
come from a bootstrap over truths and targets. The bench reports LR, G,
p_fix and the bit budget. It does not multiply them by a prior.

---

## 6. Controls

All clue sets, readings, windows, sites, seeds and thresholds for the
controls are in `data/prereg/` and frozen with this document (section 12)
before any control is computed. Truth files are read only by
`odybench/harness.py`, to place windows and to score; the searcher never
reads them, and a static test enforces it (I13).

### 6.1 Instrument checks

Each check compares a code path with something that does not share its code
[rev #13]. All must pass before any claim-level output is read; `verdict.py`
refuses to run otherwise. A check marked "post-freeze" runs first after the
freeze, and the outputs it guards are not opened until it passes; a fix it
forces is a dated amendment (section 12).

| # | what is checked | compared against | pass | when |
|---|---|---|---|---|
| I1 | ephemeris | Horizons; `validate_ephem.py`; `test_ephem.py`; `validate_coverage.py` | 55/55, 10/10, all coverage checks [acq §1.3] | done; rerun pre-freeze |
| I2 | solar-eclipse local circumstances, `eclipses.py` (Python port of NASA's JavaScript, from `results/research-critiques/eclipse_local.py`) | (a) NASA's own `program.js` run in Node: `data/jsex/sites/*.jsonl`, 5 sites × 5,486 eclipses; (b) the review's independent Besselian solver `results/critique-design/check_bessel.py` [rev #13 fix 6] | (a) smag within 0.0005, time of maximum within 0.002 h, Sun altitude within 0.05°, central flag identical; (b) totality windows for 1178, 1131, 1312 and 1183 BC within 5 s | pre-freeze |
| I2b | language-to-magnitude: local smag for the dated eclipses of [ctl §3] | the Horizons-based reference values, moved to the truth-side file `data/prereg/i2b_reference.json` and converted to the pinned definition | within 0.02 where both are below 0.95; for larger values the central flag and duration agree [rev #21 fix 2] | pre-freeze, after the re-draft of 6.3.3 |
| I3 | Hesiod's star calendar at 701 BC, 38.37°N | Hesiod's own numbers | **a calibration, not a validation** [rev #20]: the Pleiades' AV is set so that they are hidden 40 days (*WD* 385–386); "Arcturus ≥ 5° at nautical dusk" is read off *WD* 564–567. The phases are validated by I6(c) | pre-freeze |
| I4 | lunar eclipses, `lunar.py` | NASA LEcat5 rows: every lunar eclipse in the PC-R and ALM truth centuries, and 300 drawn at random from −1999..+300 | type identical; umag and pmag within 0.02; greatest eclipse within 3 min after removing the ΔT difference | pre-freeze |
| I5 | rise, set and transit, `sky.py` | (a) JPL Horizons rise/transit/set output for 1,000 random events (Sun, Moon, Venus, Mercury, Jupiter, Sirius, Arcturus; Ithaki, Alexandria, Troy; −1999..+300; same h0, airless); (b) the dense-grid-plus-bisection rise finder of `results/critique-design/check_mwra.py`, on 2,000 events | (a) within 0.5 min after removing the documented sidereal-time convention difference (5 s at −1999 [acq §1.3]); (b) within 0.1 s | pre-freeze |
| I6 | derived events, `events.py` | (a) the event lists of `results/bm2008-reconcile/check_mwra.py` (rise-azimuth maxima and minima, stations, GWE, inferior conjunction) for all 152 S2 years; (b) the low-precision Standish-element code `results/bm2008-b-checks/ephem.py`, 500 random stations and greatest elongations; (c) heliacal star phases and B&M's spring limits from `docs/research_visibility_calc.py` (its own spherical astronomy and Meeus' solar theory) at −1177 and −700 | (a) same UT+2 civil date in ≥ 150 of 152, vertex instants within 0.05 d; (b) within 1 d; (c) within 1 d | pre-freeze |
| I7 | B&M's reading through `clues.py`, `readings.py` and `search.py` | `tests/bm_reference.py`, a minimal second implementation written by a different agent from section 3.2's text alone, using only `ephem.altaz` and its own rise bisection [rev #13 fix 4] | identical pass flags (N, C, V, M, E and every T0 grid cell) for every candidate in 1250–1115 BC and in 300 random background years | post-freeze, before any T0 output is read |
| I8 | calendar | `tests/test_calendar.py` | 11/11 [acq §4] | done |
| I9 | reach | a brute-force implementation that slides windows in 0.01-year steps, on 10,000 random synthetic survivor sets | reach equal to within 0.0002 | pre-freeze |
| I10 | PC-S instrument mode (6.2) | descriptions generated by an independent code path | recall 1.000 | post-freeze, before PC-S science outputs are read |
| I11 | plumbing negatives (revision 1's NC4 and NC5 [rev #15 fix 4]) | (a) AEN-TROY's pinned R-ii-literal reading, conjunction on Day 0 with the Moon up after nightfall, which contradicts itself [neg §3.1]; (b) a synthetic set with Day 0 a conjunction and the Moon above the horizon at local midnight; (c) Hesiod's star calendar (*WD* 383–385, 564–567, 609–611, 615–621) as event clues around an arbitrary Day 0 | (a), (b) zero survivors in every window; (c) no unique survivor in any 136-year window | post-freeze |
| I12 | first-crescent evening | the Yallop implementation in `docs/research_visibility_calc.py`, 500 lunations | same evening in ≥ 495 | pre-freeze |
| I13 | prereg I/O | every licence string present in its cited row (the licence checkers' dump scripts rerun, comparing raw characters without Unicode normalisation, because the Ptolemy export mixes tonos and oxia and prints the half-sign as the literal "U+2220" [lca next-stage item 7; pcr §5]); every fork option of every row translates to a canonical predicate (10.3); exactly one primary per controls row; no module but `harness.py` and `tools/build_truth_index.py` opens a `*_truth*` path or contains the Nabonassar epoch; `operational_map.json` reviewed by a second agent | all pass | pre-freeze |
| I14 | the decision rule | the synthetic input sets of 9.3 | each returns its stated labels | pre-freeze |

Revision 1's NC4 (the Hymn to Hermes) is dropped: it misread *h.Herm.* 141,
where παννύχιος closes Hermes' clause [rev #15].

### 6.2 PC-S: synthetic Odyssey-shaped clue sets

Revision 1's PC-S generated its clue sets with the same code it searched
with, and with a different grammar, so its "recall ≥ 0.99 or it is a bug"
was either built to fail or tautological [rev #14]. It now has two modes.

**Truth pools** (seeded): (i) 2,000 daylight conjunctions drawn from the
targets T; (ii) every conjunction with h_tot ≥ 0.1 at any Ionian site (the
eclipse check of 5.7); (iii) the spring sub-pool, truths passing C_rel.

**Instrument mode.** Generator and searcher share B&M's grammar. For 200
truths from pool (i), the generator computes each truth's statements by an
independent path: the Standish low-precision planetary code of
`results/bm2008-b-checks/` with its own rise bisection for all 200, and
Horizons for a 50-truth subsample.
Statements are emitted with margins that hold under either ephemeris: the
lead threshold is the true lead minus 5 min, rounded down to 5 min; the
Mercury tolerance is \|Δ\| + 1 d, rounded up; a season statement is made only
if the truth lies at least 2 d inside its C_rel bounds. The searcher is the
bench's machinery with those parameters, on a window around the truth.
**Pass: recall = 1.000.** A miss is a shared-code or conversion bug, found
before any science number is read (I10).

**Science mode.** The generator follows the observation hypothesis of 5.7:

1. Draw the truth t* and the noise ν (offset jitter j, Mercury displacement
   s_M); each clue's observation day is its stated offset plus δ, δ uniform
   on [−j, j].
2. The poem has the Odyssey's slots only where the sky supports them on the
   observation days: Venus a visible morning star (AV 7°) around the landing
   day; Mercury within 6 d (after the displacement s_M) of one of its morning
   events, or visible, around Hermes' day; the Pleiades and Boötes up together
   at some time of the raft nights; Day 0 a conjunction. A truth that fails
   a slot is dropped from that run, and the drop fraction is reported.
3. The searcher applies every reading of 𝒢_BM, and the 1,000-reading DOC
   subsample, at the poem's stated offsets, to the candidates around t*.
4. Recorded: recall under each reading; P(unique) under the B&M reading in a
   window at a random position; t*'s reach_136 under each garden (its mean
   over the spring sub-pool is R_obs, 5.7); and the generator's own
   description of t*'s sky (which Mercury event is nearest and its \|Δ\|, the
   Venus lead, the season class of the raft nights), to show which readings
   succeed and why.

There is no "bug" threshold in science mode. One number from it enters gate
3b: **rec_PCS**, the recall over the spring sub-pool at ν_real of the
**widest-tolerance B&M reading W_BM** (F1 sequential or parallel, F1b ±3 d,
F2 (a), F3 (a′), F4 Venus visible at AV 7°, F5 any of the three events at
6 d with visibility not required, F6 off). Also reported: recall and
P(unique) as curves over ν, and the decay of reach and recall as the
typical-number jitter grows from 0 to ±3 d [rev #8 fix 2–3].

### 6.3 PC-R: real eclipse records with independently known dates (gate 3a)

**The clue file** is `data/prereg/controls_real.json` exactly as licensed
(SHA-256 `135fba67…83f8` [lcr]), with the re-drafted rows of 6.3.3 beside
it. Nine sets:

| set | text | role |
|---|---|---|
| R-PTOL-BAB | *Almagest* IV.6, three Babylonian lunar eclipses | counted |
| R-PTOL-ALEX | *Almagest* IV.6, three Alexandrian lunar eclipses | counted |
| R-PTOL-CHAIN | the two triples joined by IV.7.1 (E2 to H2: 311,784 nights) | reported; it contains BAB and ALEX |
| R-THUC | Thucydides 2.28, 4.52, 7.50 | counted |
| R-XEN | *Hellenica* 1.6.1, 2.3.4 (linked); 4.3.10 (unlinked) | counted (the linked group) |
| R-ARBELA | Plutarch, Arrian, Curtius, Pliny on one lunar eclipse | counted |
| R-PYDNA | Livy 44.36–37; Plutarch *Aem.* 16–17 | counted |
| R-DIOD | Diodorus 20.5.5 | counted |
| H-LIVY | four prodigy notices | hard case, reported, not pass/fail [rev #2 fix 4] |

#### 6.3.1 The search

The harness reads the truth (through
`data/prereg/truth_index.json`, built by `tools/build_truth_index.py` from the
two truth files), places a 136-year window with the anchor event at a
uniformly random position (seed per set), and passes only the clue set, the
window bounds and the event catalogues to the searcher.

- **Candidates** are every event of the anchor's kind in the window: solar
  eclipses from NASA's elements, lunar eclipses (umbral and penumbral) from
  `lunar.py`.
- **Linked events** are found through the interval rows (exact night counts,
  war-years ± tolerance, year headings 1–3); for each anchor candidate the
  linked event that fails fewest rows is taken. Unlinked events (R-XEN's X3,
  the H-LIVY notices) are separate searches, reported and not counted.
- **Calendars** follow the file's conventions: Egyptian dates with a free
  epoch (intervals only); Roman dates with a free offset (primary), ±90 d and
  "naive" as reported alternatives that are never readings of the text; Attic
  months through the modern reconstruction with ±1 lunation, the one primary
  that rests on a calendar outside the text [lcr flagged item 1].
- **Sites**: a point; a box (the row passes if some site in the box
  satisfies it); a disc; or none (some site on Earth: for solar eclipses a 1°
  grid refined near the best point, for lunar eclipses the Moon above the
  horizon somewhere).

#### 6.3.2 Scoring and the gate

**Scoring** [pcr §5 problem 1; truth-file note]. For a reading, f(c) is the
number of clue rows candidate c fails (rows without options are structural:
they define the events and dates).

- **Strict survivors** S₀ = {c : f(c) = 0}: B&M's all-must-pass rule.
- **Best-fit set** B = {c : f(c) = min f}: the dates the record points to,
  allowing for errors in the record.
- **Seen** := truth ∈ B, and \|B\| ≤ 0.05 × N_cand, where N_cand is the
  number of candidates in the window: the method keeps the true date while
  narrowing the window at least 20-fold (4.3 bits). Uniqueness is not
  required, because a weak record cannot be unique however good the method
  is; the gate asks whether the method loses the truth, and that is the
  failure "cannot see" names.
- **Resolution** := the number of clusters in B, where candidates within 3
  days of each other count as one cluster (this matters only for day-unit
  candidates in 6.4); **unique** := one cluster.
- **Strict recall** := f(truth) = 0.

The **primary run** puts every row at its primary option. Also reported for
every set: f(truth), \|S₀\|, \|B\|, the truth's rank; the same with each
row moved, one at a time, to each alternative; and, over all fork
combinations (sampled to 10,000 where larger), the fraction of readings that
make the truth the unique strict survivor. Twenty further window positions
per set are a sensitivity (fraction of windows in which the set is seen).

**The gate.** seen_PCR = the number of the 7 counted sets seen in the primary
run; strict_PCR = the number with strict recall.

- **3a fires if seen_PCR < 4** (fewer than half, rounded up).
- **Q_strict holds if strict_PCR < 4.**

The best-fit rule was chosen after the drafter's post-freeze check showed
that the true dates fail some primary readings under a rough lunar model
(2.6). That choice is therefore not blind, and the strict count is always
reported beside it as Q_strict. The rough check suggests strict recall in 4
of the 7 counted sets; `lunar.py` decides it.

#### 6.3.3 The drafter's exposure

The drafter had seen computed answers and flags three primaries as possibly
steered: T1-DARK, D-ECL and the ±1 h tolerance in L4-DARK [pcr §1]. The gate
uses `controls_real.json` exactly as licensed, and the exposure is measured
beside it rather than edited away. Before the freeze, an agent that has not
read `controls_real_truth.json`, anything in `results/controls-real-drafting/`
or `results/controls/`, `docs/controls-real-drafting.md`,
`docs/critique-design.md`, `docs/DESIGN-v1.md`, `docs/research-controls.md`,
`data/ref*`, or sections 2.6 and 6.1 (I2b) of this file re-drafts these three
rows from the cited text rows (Thuc. 2.28, Diod. 20.5.5, Livy 38.36.4) and the
clue file's own conventions and policies, without seeing their current
options. Its rows go to `data/prereg/pcr_redraft.json`. The harness computes
**seen_PCR,redraft**, the gate count with the re-drafted primaries in place of
the drafter's. **Q_exposure holds if seen_PCR and seen_PCR,redraft fall on
different sides of the gate threshold** (4): gate 3a then depends on the
drafter's exposure, and the verdict says so.

#### 6.3.4 Decisions on the points the licence check left open

- **Unstated sites stay "none" in the primary run** [lcr Consequences]. The
  Odyssey's observer is placed by its narrative (Theoclymenus in Odysseus'
  hall), so the asymmetry with Thucydides 2.28 is real, and a rule "a
  historian's undated notice places its observer in the region of the
  narrative" would be the inference the file's policy 2 excludes. The box and
  point options are reported as the first alternatives, so the cost of the
  rule is visible.
- **IV.6.14 is counted once**: it is H2 of R-PTOL-ALEX (gate 3a), so ALM-C,
  which contains it, is excluded from gate 3b [alm §3].
- **R-PTOL-CHAIN** uses IV.7.1, the chapter after IV.6; it is reported and
  not counted, so the gate does not depend on that choice [pcr problems].
- **"naive" Roman options** are sensitivity runs only and are never reported
  as readings [lcr flagged item 2].
- **Pliny's "apud Arbilam"** may name the battle rather than the site; the
  Tigris-camp alternative is reported [lcr flagged item 4].
- **H-LIVY has no year links** between its notices; each is searched alone
  [pcr §3].

### 6.4 The *Almagest* control: real records of B&M's own clue types (gate 3b)

B&M's search uses no eclipse; its clues are a lunar phase, a star season, a
morning star and a Mercury turning point. Revision 1's "method can see" gate
contained none of these [rev #3]. **The clue file** is
`data/prereg/controls_almagest.json` as licence-checked [lca]: 12 sets of
dated Mercury and Venus elongation records, planet–star and planet–Moon
relations, lunar phases, a lunar eclipse and an equinox, with day intervals
from Ptolemy's own Egyptian dates; the date words themselves are withheld.

**Counted sets**: ALM-A, B and D–L (11). ALM-C is reported only (6.3.4).

**Windows** are 136 years, B&M's width, with the anchor record's true date
at a uniformly random position drawn by the harness (seed per set), as in
6.3.1; twenty further positions are a sensitivity. The truth file
`controls_almagest_truth.json` is read only through `truth_index.json`.

**Candidates** are every civil day in the window as Day 0 (LMT at the
default site), with each row at its stated day offset. Each row is evaluated
at the drafter's instant convention: "evening" and "dawn" are the moments the
Sun is 8° below the horizon, stated hours are local apparent time [alm §1.5];
the convention moves continuous offsets by about ±0.1 d, and the integer-day
test at ±1 d can count 1.1 d as 1 [alm §6]. The two textual cruxes (A.6 and
H.3) run at their primary (as printed); the emended intervals are reported.

**The two Ptolemy files treat Egyptian dates differently**: this file
withholds them, while `controls_real.json` carries them with a free epoch
[alm §3; pcr §2]. Both are kept. With the epoch free, an Egyptian date fixes
only intervals, so the two are equivalent for the searcher, provided no bench
code supplies the Nabonassar epoch (JD 1448638); I13 checks statically that
the number appears only in the truth files and the harness. The `ref` of
every *Almagest* row points at a text row that contains the withheld date, so
the searcher reads only the operational fields and never the text at `ref`
[lca item 6].

**Default site.** Horizon-dependent rows are evaluated at Alexandria,
31.20°N 29.92°E, the only observing place the *Almagest*'s records name
(4.6.13, 9.10.3, 11.2.2). For sets whose rows leave the observer unstated
this is an inference, flagged as such [lca item 5]; Babylon is a sensitivity
for ALM-K.

**The B&M-type projection** (used by the gate): rows of kind interval,
moon-phase (phase-class options only), planet rows about greatest
elongation, before or after greatest elongation, visibility, rise lead and
the rising-azimuth proxy, and the equinox row. Star rows, planet–star and
planet–Moon positional options, oppositions and the eclipse row are set to
none: they are not in B&M's grammar. The full primary run is reported beside.

**Two tolerance regimes.** The file enumerates a list of values for most
parameters; a regime picks one.

| parameter | regime BM (B&M's tolerances) | regime SL (empirical observer slack) |
|---|---|---|
| k_days of greatest-elongation options, Mercury | 1 | 6 (14/14 Mercury records within 5.5 d [alm §4]) |
| k_days of greatest-elongation options, Venus | 1 | 21 (8/8 within 20.6 d) |
| k_days of opposition options | 1 | 2 (all within 1.81 d) |
| k_days of the rising-azimuth proxy | 1 | 3 (largest listed) |
| lead_min | 90 | 60 |
| every other list (j_days, tolerance_deg, tolerance_days, time_tol_h, minimum minutes, minimum altitude) | middle value (lower middle for an even count) | most lenient value |

Regime SL's planet tolerances were measured on these same records, so
recall under SL is nearly guaranteed for those rows; what SL tests is
whether B&M-type clues, at the slack real observers need, keep the true
date while still narrowing the window. Scoring is that of 6.3.2 (best-fit;
seen := truth ∈ B and \|B\| ≤ 0.05 N_cand, N_cand being the days in the
window), and resolution and uniqueness are reported.

**The gate.**

- seen_ALM_SL = the number of the 11 counted sets seen in regime SL
  (projection, best-fit).
- rec_ALM_BM = the number with strict recall and \|S₀\| ≤ 0.05 N_cand in
  regime BM (projection, strict): B&M's method as written, at B&M's
  tolerances.
- **3b fires if seen_ALM_SL < 6** (fewer than half of 11, rounded up), **or
  if rec_PCS < 0.5** (6.2).
- **Q_BM holds if rec_ALM_BM < 6**: "B&M's tolerances cannot recover expert
  planetary records" [rev #3 fix 3]. It conditions every "no" about the
  Odyssey, and it blocks outcome 1 unless outcome 1's conditions also hold
  for 𝒢_DOC, whose tolerances include the slack (section 9).

What is already known (2.6) makes Q_BM likely: at ±1 d the true dates fail a
greatest-elongation clue in 7 of the 9 sets that carry one. The harness must
implement two pieces of new vocabulary: the bound `same_apparition`, and
ALM-F.4's `star_candidates` with one garden branch per candidate [lca].

### 6.5 Negative controls (outcome 4)

**The clue file** is `data/prereg/negatives.json` as licence-checked [lcn]:
12 clean negatives (Virgil, Apollonius, Quintus Smyrnaeus, Valerius Flaccus:
fiction or legend composed long after the events it tells, under the
Odyssey's own selection rules, with no similes and no lying tales) and the
Iliad as a same-tradition comparison [rev #15 fix 1–2; neg §1]. Its
`operational` fields are prose, so each option is translated into a
canonical predicate in `data/prereg/operational_map.json` before the freeze,
and a second agent checks each translation against its prose.

**Pre-freeze decisions and second reading** [neg §6; lcn §4]:

- A second reader checks the interval forks and caps that rest on the
  drafter's own counts: ARG-CIUS n16/n17/n18, ARG-COLCHIS a3/a4, IL
  h12/h13/h15, VF-LEMNOS-01, and the caps free30, xfree, w60 and QS-SACK-06's
  10 d.
- **"literal" means least inference.** Pinned literal readings that use an
  inferred or drafter-width option (AEN-CRETE-01 a60, ARG-RETURN-03 x0,
  ARG-COLCHIS-02 a3) are re-pinned to the least-inference option of their row
  by the second reader.
- QS-SACK-03's BM-analogue pin keeps option b in its new meaning (the
  Pleiades over the dark hours); b-late stays in the garden.
- The same reader checks the place identifications against a gazetteer
  (Pleiades) and flags, in `operational_map.json`, the numeric thresholds
  that are the drafter's operationalisations [lcn §4.3; 13 rows 34–35].

**Windows.** Each clean negative is searched in the Odyssey's own two
windows (reproduction, 136 years; primary, 251 years) at its own site. The
negatives tell events of the same legendary age, and these windows give
fiction exactly the chances the Odyssey had. Twenty further random positions
per width are a sensitivity.

**Gardens.** 𝒢_j is the full product of set j's fork options, with each F5
entry expanded into its tolerance and visibility variants [neg §1 item 6].
Its eclipse-compatible readings are those that contain a solar-eclipse or
Day-0-conjunction option listed in the set's `eclipse_compatible_options`;
lunar-eclipse options are not solar eclipses and are excluded, as the file
says.

**The test** [rev #1 fix 3]:

- **hit_j**: some eclipse-compatible reading of 𝒢_j has, in one of the two
  windows, a unique survivor with h_tot ≥ M_Ody at the set's site (its first
  `observer_places` entry);
- **G_j**: the mean reach_136, under 𝒢_j, over all daylight conjunctions at
  the set's site in the core (most negatives have no season clue, so there
  is no season to condition on);
- **outcome 4 fires if some clean negative has hit_j and G_j ≤ G_BM,u**,
  where G_BM,u is the Odyssey's G_u under 𝒢_BM, over the same kind of target
  set: fiction, read with its own sourced forks, yields an eclipse match at
  least as strong as the Odyssey's, at a look-elsewhere-corrected
  significance at least as great as B&M's reading of the Odyssey under B&M's
  own forks. Because 𝒢_j holds more readings than 𝒢_BM, the comparison
  favours B&M.

Also reported per set: the survivors of each pinned reading (literal,
BM-analogue; R-i, R-ii and R-ii-literal for AEN-TROY), survivors per
century, and the slot matrix of [neg §5].

**The Iliad** (IL-PATROCLUS) gets the same computations, reported as the
same-tradition comparison and not used in the rule. Two consistency checks
run beside it:

- **Iliad against Odyssey.** If both carry real dates, the Iliad's (the tenth
  year of the war) must fall about 8–12 years before the Odyssey's (the
  return in the twentieth year [win §5]). For the pinned BM-analogue readings
  the bench reports the offset and its base rate (the chance that an
  unrelated survivor falls in a given 5-year band).
- **Cross-text competition.** How many texts and readings the gardens attach
  to each eclipse with h_tot ≥ 0.1. 30 Oct 1207 BC and 30 Sep 1131 BC have
  also been claimed for Joshua 10 [crit §0 item 7, *secondary*]; Joshua is
  outside the grammar and is not run.

---

## 7. Clues B&M did not use

From the 76-row inventory [txt §4]. None is used to fit anything. Each
testable one is evaluated (i) on 16 Apr 1178 BC, (ii) on every survivor of
every 𝒢_BM reading, and (iii) for its **base rate conditional on the
reading**: the pass rate among the background survivors of the same reading,
and among P_spring candidates that pass N and C [rev #11 fix 1]. If the clues
record a real sky, held-out clues should pass more often among the survivors
than their conditional base rate.

| # | clue (lines; day) | testable? | predicate (frozen now) | how it enters |
|---|---|---|---|---|
| H1 | "this night is very long" (11.373; Day −7 seq); "these nights are endless" (15.392; Day −3) | yes | night (Sun's centre below −0.833°) ≥ 12.0 h on that night | **non-blind, not counted** [rev #11]: the threshold was set after the nights of 1178 BC (11.5 h and 11.3 h, fail) were computed [txt §5.6], and it measures the season C already fixes. Reported, also under R_anc |
| H2 | σκοτομήνιος, the dark night (14.457; night of Day −5 seq / −4 par) | yes | Moon above the horizon for < 25% of the dark hours | counted. Given Day 0 a conjunction it passes about half the time (median 25%), not "almost always" as revision 1 said [rev #24b; vis §4.5] |
| H3 | Hermes leads the suitors' souls past the gates of the Sun (24.1–14; night of Day 0/+1) | yes, under the Hermes = Mercury rule | (a) Mercury not visible (AV 10°) on the mornings and evenings of Day 0 and +1; (b) Mercury within ±3 days of a conjunction with the Sun | counted, with conditional base rates: 34 days after a morning rising-azimuth maximum Mercury is heading for superior conjunction, so its unconditional rate would mislead [rev #11] |
| H4 | Ares and Aphrodite caught together (8.266–366; Day −7 seq) | yes, under the same rule | Venus–Mars separation ≤ 5° within ±3 days of Day −7 | counted, conditional base rate (V fixes Venus' elongation) |
| H5 | Mars invisible in March–April 1178 BC except during the eclipse | yes | Mars not visible (AV 11.5°) on any morning or evening from Day −34 to Day 0 | **non-blind, not counted**: B&M found it after the date [bm §2] |
| H6 | the twentieth year (9 lines); a year with Circe and seven with Calypso | yes, against ancient sack dates | year lies 8–11 years after one of the ancient sack dates (Duris 1334/3 to Ephorus 1135, as in [win §3]; Clement's list [unread §4]) | external check, reported per survivor; strict Eratosthenes alone excludes 1178 BC [win §6] |
| H7 | Theoclymenus at the δεῖπνον; supper "in the light" (20.390–394, 21.428–429) | partly | eclipse maximum in daylight on Day 0 | consistency only, for eclipse-compatible readings; "noon" is not in the text [txt §5.10] |
| H9 | frost feared (5.467, 17.25); hearths and fires (6.305, 7.153, 18.307–311, 19.63–64) | no | — | weather, not sky; reported qualitatively with the five scholia that read autumn or winter [txt §5.6] |
| H10 | nightingale (19.519), swallows (21.411, 22.240), gadfly (22.301 = 18.367) | no | — | similes; excluded [txt §5.4]. 18.366–370 is also a wish and is read as winter, May or autumn by different advocates; it is used for nothing [unread §2.3] |
| H11 | much-flowering wood (14.353) | no | — | inside a lying tale; excluded |
| H12 | Laertes digging round a plant (24.226–231; Day +1) | no | — | qualitative |
| H13 | Helios' complaint (12.374–390), Poseidon and Zeus (13.125–158) | no | no operational predicate is defensible | listed, not run |

Revision 1's H8 ("starry pre-dawn sky", 20.98–121) is **withdrawn**:
"ἀπ' οὐρανοῦ ἀστερόεντος" (20.113) is a stock epithet, used in daylight at Od.
9.527, and the scene follows the dawn at 20.91 [rev #24a].

**The counted statistic**: the number of the four counted predicates (H2,
H3a, H3b, H4) that 1178 BC passes, against the Poisson-binomial distribution
of their conditional base rates; and, over all 𝒢_BM survivors, the pass rate
against the conditional base rate. Power is low with so few survivors, and
the report says so. The same statistics are computed for R_anc's survivors,
the ancient autumn reading [rev #11 fix 3].

---

## 8. Pre-registered predictions

Written 2026-10-04, before any null model, control search or held-out check
of the bench was run. Everything already computed is in section 2 and is not
repeated here as a prediction [rev #17]. Each prediction names the quantity,
the script that computes it and the threshold that decides it. P1–P7 are
**regression expectations**: implied by section 2, they need the full T0b run
to confirm but are not counted as confirmations. P34 confirms a rough known
result and is not counted either.

**Reproduction (T0; `reproduce.py`)**

- **P1.** Regression checks A1–A5 pass.
- **P2.** 16 Apr 1178 BC passes N, C, V and M in every cell of the T0 grid.
- **P3.** With E off, the N ∧ C ∧ V ∧ M survivors in 1250–1115 BC number at
  least 2 and include 18 Mar 1189 BC.
- **P4.** With E ≤ 5 Apr and with E ≤ 6 Apr the survivor set is exactly
  {16 Apr 1178 BC}; with E ≤ 4 Apr it is empty.
- **P5.** T0 is RE in the primary cell and in every cell with E ≤ 5 or
  ≤ 6 Apr, and NR in every cell with E ≤ 4 Apr.
- **P6.** With C_rel and E_rel in place of the fixed Julian bounds, the
  reproduction-window survivor sets of P3 and P4 are unchanged.
- **P7.** The half-open UT+2 window holds 1,683 conjunctions.

**Rates (N1; `rates.py`)**

- **P8.** λ(N ∧ C ∧ V ∧ M) over the background lies in [0.44, 1.76] per
  century: within a factor 2 of B&M's own arithmetic at their ±1-day
  tolerance (0.88).
- **P9.** λ(N ∧ C ∧ V ∧ M ∧ E_rel, n = 4) is at least 0.07 per century, above
  B&M's printed 0.048 (their own arithmetic at ±1 d gives 0.14).
- **P10.** The background holds at least 6 N ∧ C ∧ V ∧ M survivors, and the
  empirical P(≥ 1 survivor in a 136-year window) is at least 0.5.
- **P11.** p_fix|C lies in [0.002, 0.02] (rough estimate 0.008 [vis §5]); the
  unconditional p_fix lies in [0.0002, 0.002] (rough 0.0007).
- **P12.** The V–M dependence ratio on P_spring lies in [0.5, 2], with
  permutation p > 0.05.
- **P13.** Under C_rel and E_rel no century's λ lies outside the 99% Poisson
  band of the background mean; under the fixed Julian bounds, fewer than 90%
  of the candidates that pass the fixed C in −1999..−1800 also pass C_rel
  (the fixed dates misdescribe the sky away from −1177).

**The eclipse coincidence (N2; `coincidence.py`)**

- **P14.** p_e(M_Ody) over P_spring is within a factor 2 of p_e(M_Ody) over
  P_day, with 16 Apr −1177 excluded from both.
- **P15.** V and M pass rates do not differ between eclipse and non-eclipse
  spring new moons (permutation p > 0.05 for each).

**Forking paths (N3; `garden.py`)**

- **P16.** reach_136(16 Apr 1178 BC) under the T0b reading with E off is 0:
  another survivor falls in −1176..−1052.
- **P17.** G_BM ≥ 2 × p_fix,unique.
- **P18.** G_BM ≤ 0.05; G_DOC ≥ 2 × G_BM; G_FULL ≥ 4 × G_BM.
- **P19.** Some reading of 𝒢_DOC^X makes 30 Sep 1131 BC the unique survivor
  of a 136-year window containing it.
- **P20.** Some reading of 𝒢_FULL^X makes 24 Jun 1312 BC the unique survivor
  of a 251-year window containing it.
- **P21.** G_X(𝒢_BM) lies within a factor 2 of G_u(𝒢_BM): eclipse dates are
  not specially reachable.
- **P22.** G_FULL ≥ 0.05, and the greedy smallest fork set that brings G to
  0.05 adds at most four options to 𝒢_BM.
- **P23.** R_anc: in 1250–1115 BC its survivors include 30 Sep 1131 BC and do
  not include 16 Apr 1178 BC; in the 251-year primary window it has at least
  two survivors.

**Random epics (N4; `randomepic.py`)**

- **P24.** For variant A epics, P(unique survivor in a 136-year window) lies in
  [0.2, 0.6], and P(T_best ≥ T_obs) ≥ 0.2.
- **P25.** pct_N4(BM) lies within a factor 3 of G_BM: varying the poem and
  varying the target give the same null probability.

**ΔT (N6; `deltat.py`)**

- **P26.** In the DE431 pairing: P(total at Ithaki) is higher for 30 Sep
  1131 BC than for 16 Apr 1178 BC under SMH2020, the Addendum parabola and
  Espenak–Meeus, and lower under the SMH2016 parabola; the joint probability
  under a common offset is ≤ 0.06 under the first three and ≥ 0.08 under the
  SMH2016 parabola. (Revision 1's prediction 19, restated per model [rev
  #17].)
- **P27.** The T0b survivor sets (E off; E ≤ 5 Apr) do not change when the
  clock ΔT is replaced by SMH2020, SMH2020 + 1σ and SMH2020 − 1σ with DE431
  conjunctions.

**PC-S (`synthetic.py`)**

- **P28.** Instrument mode recall = 1.000 (an instrument requirement: a miss
  is a bug).
- **P29.** Science mode, zero noise: P(unique) under the B&M reading, over the
  spring truths that pass it, is ≤ 0.6.
- **P30.** At ν_real the B&M reading (±1 d) recovers at most 70% of the
  spring truths.
- **P31.** R_obs(𝒢_BM) at j = 3 is at most half its value at j = 0.
- **P32.** rec_PCS ≥ 0.5.

**Controls (`controls.py`, `almagest.py`, `negatives.py`)**

- **P33.** seen_PCR ≥ 4: R-PTOL-BAB, R-PTOL-ALEX, R-ARBELA and R-DIOD seen;
  R-THUC, R-XEN and R-PYDNA not seen in the primary run.
- **P34.** strict_PCR = 4, the accepted dates failing a primary row in
  R-PTOL-BAB, R-PTOL-ALEX and R-PYDNA (confirms the rough check of 2.6; not
  counted).
- **P35.** seen_ALM_SL ≥ 6.
- **P36.** rec_ALM_BM < 6, so Q_BM holds.
- **P37.** No clean negative fires outcome 4; at least one clean negative has
  a unique survivor of some kind in one of the two Odyssey windows.
- **P38.** Some eclipse-compatible reading of IL-PATROCLUS makes an eclipse new
  moon with h_09 ≥ 0.5 at Troy the unique survivor of the 251-year primary
  window.

**Held-out clues (`heldout.py`)**

- **P39.** 16 Apr 1178 BC passes no more of H2, H3a, H3b and H4 than their
  conditional base rates predict (Poisson-binomial p > 0.1).
- **P40.** Over all 𝒢_BM survivors, the held-out pass rate lies within the
  conditional base rate's 95% interval.

**Bottom line (`verdict.py`)**

- **P41.** LR_real,lo(𝒢_BM) < 30.
- **P42.** The verdict contains neither 1, nor 3a, nor 4, and Q_BM holds.

---

## 9. The decision rule

### 9.1 Named quantities

Every quantity the rule reads is written by one script to one JSON key, and
stamped with the frozen code tree hash (section 12).

| quantity | definition | section | written by |
|---|---|---|---|
| INSTR | all instrument checks I1–I14 pass | 6.1 | `results/instrument/summary.json` |
| T0 | T0 verdict in the primary cell: R, RE or NR | 3.5 | `reproduce.py` |
| G_BM | G(𝒢_BM) over T_C, W = 136 | 5.3 | `garden.py` |
| G_BM,u | G_u(𝒢_BM) over T | 5.3 | `garden.py` |
| G_DOC | G(𝒢_DOC) over T_C, max over W | 5.3 | `garden.py` |
| pct_N4,hi | upper 95% bound of the fraction of stratum epics whose BM-tier garden reaches Schoch's target at least as well as the Odyssey's 𝒢_BM | 5.4 | `randomepic.py` |
| LR_real,lo(BM) | lower bootstrap 95% bound of R_obs(𝒢_BM, ν_real) / G_BM | 5.7 | `verdict.py` from `synthetic.py` and `garden.py` |
| LR_fav,hi(BM) | upper bootstrap 95% bound of max over ν of R_obs(𝒢_BM, ν) / G_BM | 5.7 | same |
| LR_real,lo(DOC) | as LR_real,lo for the 1,000-reading DOC subsample | 5.7 | same |
| seen_PCR, strict_PCR | of the 7 counted PC-R sets: seen; strict recall | 6.3.2 | `controls.py` |
| seen_PCR,redraft | seen_PCR with the three re-drafted rows in place of the drafter's | 6.3.3 | `controls.py` |
| seen_ALM_SL, rec_ALM_BM | of the 11 counted *Almagest* sets: seen at slack; strict recall at B&M's tolerances | 6.4 | `almagest.py` |
| rec_PCS | recall of W_BM at ν_real over the spring sub-pool | 6.2 | `synthetic.py` |
| NEG | for each of the 12 clean negatives: hit_j and G_j | 6.5 | `negatives.py` |

The thresholds are in `data/prereg/verdict_rule.json` and frozen.

### 9.2 The rule

`odybench/verdict_rule.py` implements exactly this, as a pure function of the
quantities above:

```
if not INSTR:                          return BLOCKED (no verdict is read)
labels, qualifiers = {}, {}
if seen_PCR < 4:                        labels += 3a
if seen_ALM_SL < 6 or rec_PCS < 0.5:    labels += 3b
if rec_ALM_BM < 6:                      qualifiers += Q_BM
if strict_PCR < 4:                      qualifiers += Q_strict
if (seen_PCR < 4) != (seen_PCR,redraft < 4):
                                        qualifiers += Q_exposure
if any(hit_j and G_j <= G_BM,u for j in clean negatives):
                                        labels += 4
outcome1 = labels is empty
       and T0 in {R, RE}
       and G_BM <= 0.01
       and LR_real,lo(BM) >= 30
       and pct_N4,hi <= 0.05
       and (Q_BM not in qualifiers
            or (G_DOC <= 0.01 and LR_real,lo(DOC) >= 30))
if outcome1:                            labels = {1}
elif G_BM >= 0.05 or LR_fav,hi(BM) < 10:
                                        labels += 2
if labels is empty:                     labels = {inconclusive}
return labels, qualifiers
```

**How to read it.**

- **Every rule names its garden** [rev #1 fix 1]: 𝒢_BM is primary; 𝒢_DOC
  enters only when Q_BM says B&M's tolerances cannot see real records, and
  then outcome 1 must also hold for the documented garden, whose tolerances
  include the observer slack. The verdict recomputed with 𝒢_DOC and with
  𝒢_FULL in place of 𝒢_BM is printed under it as a sensitivity and never
  replaces it.
- **Outcome 1 can be reached** [rev #1]: its negative-control condition is a
  percentile among random poems in the same specificity stratum (pct_N4), not
  revision 1's "every NC G ≥ 10 × the Odyssey's", which weak texts made
  unreachable; and "dates fiction" is defined separately (outcome 4).
- **G has one sense throughout**: a look-elsewhere-corrected p-value, small
  when the coincidence is notable. Outcome 1 needs it small, outcome 2 large,
  outcome 4 asks whether fiction's is as small as the Odyssey's.
- **Intervals work against the claim being made.** Outcome 1 needs the lower
  bound of LR at realistic noise to reach 30 and the upper bound of the
  percentile to stay under 0.05; outcome 2's ratio condition needs the upper
  bound at the noise most favourable to B&M to stay under 10 [rev #16 fix
  2]. The gap between them is the inconclusive region, and it is reported
  as such, with every number.
- Labels 2, 3a, 3b and 4 can hold together and are all reported. The
  headline leads with 3a or 3b when either holds, because they say which
  "no"s mean nothing.

### 9.3 Synthetic input sets that prove every outcome reachable

`data/prereg/verdict_synthetic/*.json` holds these inputs, and
`tests/test_verdict.py` asserts the stated output for each (instrument check
I14). Only the fields that differ from S1 are given for the later sets.

| set | inputs | labels | qualifiers |
|---|---|---|---|
| **S1** | INSTR true; T0 RE; G_BM 0.004; G_BM,u 0.0004; G_DOC 0.006; pct_N4,hi 0.02; LR_real,lo(BM) 45; LR_fav,hi(BM) 200; LR_real,lo(DOC) 35; seen_PCR 6; seen_PCR,redraft 6; strict_PCR 5; seen_ALM_SL 9; rec_ALM_BM 7; rec_PCS 0.8; no negative hit | **{1}** | none |
| **S2** | G_BM 0.12; G_BM,u 0.012; G_DOC 0.3; pct_N4,hi 0.4; LR_real,lo(BM) 2; LR_fav,hi(BM) 4; LR_real,lo(DOC) 1 | **{2}** | none |
| **S3a** | seen_PCR 2; seen_PCR,redraft 2 | **{3a}** | none |
| **S3b** | seen_ALM_SL 3 | **{3b}** | none |
| **S4** | G_BM 0.02; G_BM,u 0.002; G_DOC 0.04; pct_N4,hi 0.1; LR_real,lo(BM) 12; LR_fav,hi(BM) 15; LR_real,lo(DOC) 9; AEN-TROY: hit true, G_j 0.0015 | **{4}** | none |
| **S0** | as S4, but no negative hit | **{inconclusive}** | none |
| S5 | as S1, but rec_ALM_BM 3 and G_DOC 0.03 | {inconclusive} | Q_BM |
| S6 | as S2, but seen_ALM_SL 3, strict_PCR 2, seen_PCR,redraft 3, and AEN-TROY hit with G_j 0.01 | {2, 3b, 4} | Q_strict, Q_exposure |
| S7 | INSTR false | BLOCKED | — |

S1–S4 reach each of the four outcomes (3 in both its parts), S0 the
inconclusive verdict, S5 the qualifier path that blocks outcome 1, S6 the
co-occurrence of labels and qualifiers, and S7 the instrument block.

---

## 10. Software

### 10.1 Build plan

The build is done by agents in parallel. Each owns the files listed, works
to the interfaces of 10.2, and must not read what is listed in the last
column. `odybench/model.py`, the shared types, is written first and frozen as
the contract.

| agent | owns | depends on | must not read |
|---|---|---|---|
| A0 lead | `odybench/model.py`; `data/prereg/sites.json`, `windows.json`, `seeds.json`, `deltat_models.json`, `verdict_rule.json` | this design | — |
| A1 sky | `odybench/sky.py`, `odybench/events.py`, `tools/build_sky.py`, `tools/build_events.py`, `tools/validate_events.py` (I5, I6, I12) | `model.py`, `ephem.py`, `calendar.py` | — |
| A2 eclipses | `odybench/eclipses.py`, `odybench/lunar.py`, `data/prereg/eclipse_hit.json`, `tools/build_eclipses.py`, `tools/validate_eclipses.py` (I2, I4), `tools/fetch_lecat.py`, `tests/test_eclipses.py`, `tests/test_lunar.py` | `model.py`, `ephem.py`, `data/jsex/` | the truth files (I2b runs through the harness) |
| A3 clues | `odybench/prereg_io.py`, `odybench/clues.py`, `odybench/search.py`, the controls sections of `data/prereg/operational_map.json`, a draft of its negatives section, `tests/test_clues.py`, `tests/test_prereg_io.py` | A1 and A2 interfaces | `*_truth*`, `results/controls-*`, `check_truth*` |
| A4 garden | `odybench/readings.py`, `data/prereg/garden.json`, `readings.json`, `odybench/reach.py` (I9), `rates.py`, `coincidence.py`, `garden.py`, `windows.py` | A3 | `*_truth*` |
| A5 epics and PC-S | `odybench/epic.py`, `odybench/pcs.py`, `data/prereg/epic_grammar.json`, `randomepic.py`, `synthetic.py` (I10) | A3, A4 | `*_truth*` |
| A6 harness and verdict | `odybench/harness.py`, `tools/build_truth_index.py`, `controls.py`, `almagest.py`, `negatives.py`, `heldout.py`, `data/prereg/heldout.json`, `odybench/verdict_rule.py`, `verdict.py`, `read.py`, `odybench/stats.py`, `odybench/prereg.py`, `tools/freeze.py`, `tests/test_verdict.py` (I14) | all | — |
| A7 second implementation | `tests/bm_reference.py` (I7) | `ephem.py`, `calendar.py`, section 3.2 of this design | every other bench module |
| A8 unexposed re-drafter | `data/prereg/pcr_redraft.json` | the cited text rows; the clue file's conventions and policies | the list in 6.3.3 |
| A9 second reader of the negatives | review of the negatives section of `operational_map.json`; interval forks and caps; literal pins (6.5) | `negatives.json`, `data/text/` | — |
| A10 reproduction and ΔT | `reproduce.py`, `deltat.py`, `odybench/s2.py`, `tests/test_t0.py` | A1, A2 | — |

### 10.2 Module interfaces

All times are JD floats with a named scale; all calendar work goes through
`odybench.calendar`. Arrays are numpy; files are NPZ (numeric) or JSON
(UTF-8, `ensure_ascii=False`).

**`odybench/model.py`** (the contract)

```
BODIES = ("sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn")
GRAMMAR_STARS = ("alcyone", "arcturus", "sirius", "aldebaran", "betelgeuse",
                 "rigel", "dubhe")           # extras from data/stars.json allowed
@dataclass Site(key, lat, lon, elev_m, source)
POOL_DTYPE = [("jd_ut","f8"), ("jd_tt","f8"), ("day0_jdn","i8"),
              ("kind","U12"), ("cat_idx","i8")]          # one row per candidate
@dataclass Predicate(type: str, params: dict, day: int | tuple[int,int] | None,
                     quant: str = "any", site: dict | None = None)
@dataclass Option(name: str, primary: bool, predicate: Predicate | None,
                  grid: dict[str, list])                  # None = the clue is dropped
@dataclass ClueRow(clue_id, event_id, day_offset, options: list[Option])
@dataclass ClueSet(set_id, role, anchor_kind, events, links, rows, site_rule,
                   window_widths, counted: bool)
@dataclass Reading(choice: dict[str, tuple[str, dict]])  # clue_id -> (option, grid values)
@dataclass SearchResult(pool, fails: np.ndarray[int16], strict: np.ndarray[int64],
                        best: np.ndarray[int64], n_cand: int, clusters: int)
```

**`odybench/sky.py`**

```
build(site: str, y0: int, y1: int, *, dt_model="smh2020", bodies=BODIES,
      stars=GRAMMAR_STARS, workers=14, out_dir="data/cache") -> Path
load(path) -> SkyTable        # NPZ, n = number of LMT civil days y0-01-01 .. y1-12-31
```

SkyTable arrays (nb bodies, ns stars, n days): `jdn` i8[n]; `jd0_ut` f8[n]
(local midnight); `rise_ut`, `set_ut`, `rise_az`, `set_az` f8[nb, n] (NaN if
none that day; azimuth from north through east); `sun_alt_at_rise`,
`sun_alt_at_set`, `mag_at_rise`, `mag_at_set` f8[nb, n]; `elong`, `lon_ecl`,
`lat_ecl` f8[nb, n] at local midnight (signed elongation, east positive;
apparent of date, geocentric); `twl_eve_ut`, `twl_morn_ut` f8[3, n] (Sun at
−6°, −12°, −18°); `star_alt_eve12`, `star_alt_morn12` f4[ns, n];
`star_rise_ut`, `star_set_ut`, `sun_alt_at_star_rise`,
`sun_alt_at_star_set` f8[ns, n]; `moon_frac_midnight`, `moon_up_frac_dark`,
`night_len_h` f8[n]; `meta` (JSON string: site, ΔT model, ephemeris file
hashes, h0 values, refraction flag, code tree hash). Rise is the topocentric
airless altitude of the centre crossing h0 = −0.8333° (Sun, Moon) or
−0.5667° (planets, stars), found by Meeus' iterated hour angle and bisected
to 0.1 s for Mercury and 1 s otherwise. Lunar quantities use DE431 and
SMH2020 ΔT in yearly chunks that never straddle JD 1721425.5; planets and
stars use DE441.

**`odybench/events.py`**

```
conjunctions(jd_tt0, jd_tt1) -> f8[k]                         # DE431, yearly chunks
full_moons(jd_tt0, jd_tt1) -> f8[k]
stations(body, jd_tt0, jd_tt1) -> rec[("jd_tt","f8"), ("kind","U1")]   # R, D
greatest_elongations(body, jd_tt0, jd_tt1, sun="true"|"mean")
    -> rec[("jd_tt","f8"), ("side","U1"), ("elong","f8")]
oppositions(body, jd_tt0, jd_tt1, sun="true"|"mean") -> f8[k]
azimuth_extrema(sky, body, which="rise"|"set")
    -> rec[("jd_ut","f8"), ("kind","U3"), ("az","f8"), ("curv","f8"),
           ("margin","f8"), ("flat","?")]                     # parabola vertex, 7 days
visibility(sky, body, side, av: float | "plsv", crit_alt=0.0) -> bool[n]
star_phases(sky, star, av) -> rec per year: heliacal rising and setting,
    acronychal rising, cosmical setting (JDN)
season_bounds(sky, h_A, h_P) -> rec per year: A(y), P(y) (JDN)   # C_rel
equinoxes(jd_tt0, jd_tt1) -> rec[("jd_tt","f8"), ("kind","U2")]  # VE AE SS WS
first_crescent(sky, conj_jd_tt, criterion="yallop_B") -> i8     # JDN of the evening
```

**`odybench/eclipses.py`**

```
catalogue(y0=-1999, y1=300) -> rec[idx, jd_td, dt_canon, gamma, type, saros, file, row]
local(ecl, lat, lon, dt_s, elev_m=0.0) -> dict(smag, obsc, central, duration_s,
      t_max_ut, sun_alt, lat_h, c1_ut, c2_ut, c3_ut, c4_ut)
totality_window(ecl, lat, lon) -> (dt_lo, dt_hi) | None      # canon frame
hit_strength(ecl, site, models=FOUR, frame="canon")
      -> dict(h_tot, h_09, h_06, by_model: {model: (p_tot, p_09, p_06)})
site_table(site) -> NPZ cached in data/cache/eclipses_<site>.npz
local_de431(ecl, site, dt_s) -> dict                         # ephem.local_circumstances on DE431
```

**`odybench/lunar.py`**

```
catalogue(y0, y1) -> rec[jd_tt, umag, pmag, type, gamma, lat_sign,
      p1, u1, u2, u3, u4, p4]                                 # contacts, JD TT; NaN if none
local(lecl, lat, lon, dt_s) -> dict(moon_alt at each contact, moonrise_ut,
      moonset_ut, seasonal night hour of each contact, mid_LAT_offset_h)
```

**`odybench/prereg_io.py`, `clues.py`, `search.py`**

```
load_controls_real() / load_controls_almagest() / load_negatives()
      -> list[ClueSet]     # translated through operational_map.json; unknown key -> error
load_odyssey() -> (ClueSet, garden)                           # readings.json, garden.json
evaluate(pred: Predicate, pool, ctx) -> bool[len(pool)]
evaluate_rows(clueset, reading, pool, ctx) -> bool[n_rows, len(pool)]
search(clueset, reading, window: (jd0, jd1), ctx, scoring="strict"|"bestfit")
      -> SearchResult
```

`prereg_io` refuses any path matching `*_truth*` (I13). `ctx` holds the sky
tables, event lists and catalogues for the sites a clue set names.

**`odybench/readings.py`, `reach.py`**

```
garden(tier="BM"|"DOC"|"FULL", eclipse_compatible=False) -> Iterator[Reading]
pinned(name) -> Reading        # "T0b", "BM", "R_anc", "W_BM"
survivors(garden, pool, ctx) -> Iterator[(reading_index, f8[k] survivor JD_TT)]
interval(t, s_prev, s_next, W_days) -> (lo, hi)               # empty if lo >= hi
reach(targets: f8[m], survivor_sets, W_days) -> f8[m]          # |union| / W
G(reach_values) -> (mean, lo, hi)
p_at_least_one(survivors, W_days, b0, b1, step_days=365.25) -> (empirical, poisson, mean)
```

Survivor sets are computed as packed bit masks (uint64[ceil(n_pool/64)]) per
option and ANDed per reading in batches; a reading whose largest survivor gap
is below W contributes no reach and is skipped.

**`odybench/epic.py`, `pcs.py`, `harness.py`, `verdict_rule.py`, `prereg.py`**

```
epic.draw(n, variant, seed) -> list[ClueSet]
epic.garden_for(clueset, tier) -> list[Reading]
pcs.instrument(truths, path="standish"|"horizons") -> list[ClueSet]
pcs.science(truths, nu, garden, ctx) -> rec per truth: recall per reading, reach, description
harness.place_window(set_id, width_years, k) -> (jd0, jd1)     # the only reader of truth_index.json
harness.score(set_id, result: SearchResult) -> dict(seen, strict_recall, f_truth, rank, resolution)
verdict_rule.decide(q: dict, thresholds: dict) -> (set[str], set[str])
prereg.check_frozen() -> dict(commit, tree_hash, amendment)     # raises unless frozen
```

### 10.3 Canonical predicates and the translation of the prereg files

The three prereg files were drafted by different agents with three
vocabularies: `controls_real.json` and `controls_almagest.json` have
machine-readable `operational` dicts, while `negatives.json` has prose
[pcr §5 item 2; lca next-stage item 2; neg]. All are translated into one set
of canonical predicates:

| type | parameters | used for |
|---|---|---|
| `anchor` | rule: conj_ut2, conj_lmt, conj_plus1, first_crescent, full_moon, day7, any_day, solar_eclipse, lunar_eclipse | Day 0 (F2; epics; controls) |
| `moon_phase` | class, tolerance (days) | phase rows. Frozen classes by Sun–Moon elongation E (east +): young crescent 0° < E ≤ 45°; waxing crescent 0° < E < 90°; first quarter \|E − 90°\| ≤ 12.2° × tol; near full 150°–210°; full \|E − 180°\| ≤ 12.2° × k; last quarter \|E − 270°\| ≤ 12.2° × tol; waning crescent 270° < E < 360° [me] |
| `moon_up` | interval of named instants, illuminated-fraction bounds, quantifier | negatives, PC-R |
| `moon_dark_share` | maximum share of the dark hours with the Moon up | H2 |
| `rise_lead`, `set_lag` | body, minutes | V; ALM visible_only (minutes between horizon crossings) |
| `visible` | body, side, AV (degrees or PLSV), critical altitude | F4, F5, H3a, H5 |
| `alt_at` | body or star, named instant, minimum altitude | ALM visible_before_sunrise (civil dawn), negatives |
| `turning_point` | body, event (greatest elongation from the true or mean Sun; station; rise- or set-azimuth extremum; first or last visibility; opposition to the true or mean Sun), side, k days (continuous), visibility required, displacement | M; ALM; epics |
| `ge_relation` | body, side, before or after, j days or `same_apparition` | ALM A.1, B.1, I.1, J.4 |
| `star_covis` | stars, minimum altitude, twilight, span of nights, quantifier; or a season window (C_rel, autumn) | C; F3; epics |
| `star_phase` | star, phase, AV, k days | epics; negatives |
| `rel_position` | body, reference (star, line through two stars, Moon's centre), offset or distance, tolerance, frame | ALM star and Moon rows; one branch per star candidate for F.4 |
| `sun_lon` | range (wraps through 0°) | seasons in PC-R, R_anc |
| `equinox_offset` | event, offset range in days | E_rel; ALM-E.3 |
| `solar_eclipse` | smag range, central flag, minimum h_tot/h_09/h_06, timing (LAT of maximum, first contact after noon, last contact with the Sun up), site rule | X; PC-R; negatives |
| `lunar_eclipse` | umag and pmag ranges, Moon's latitude sign, timing (mid-eclipse offset from LAT midnight, first contact after moonrise, overlap or containment in seasonal night hours or a night quarter), Moon altitude at contacts, moonrise during the umbral phase at a site rule | PC-R; ALM-C |
| `interval` | from event, to event: exact nights, day range, or years ± tolerance | links |
| `calendar` | Egyptian (free epoch), Roman (named date, offset bound or free), Attic (month, lunation offset), report bounds | PC-R |
| `night_length`, `separation`, `herald`, `crescent`, `rise_azimuth` | as named | H1, H4, F4, F2(d), AEN-TROY's Ida rider |

Translation rules: `controls_real.json` and `controls_almagest.json` keys map
to these types by fixed rules in `prereg_io.py`; their free-text values
(relation strings such as "umbral phase overlaps hour", site names such as
"Tigris camp") are listed in `operational_map.json`; an unknown key or value
is an error, never a default. Each `negatives.json` option gets a full
canonical predicate in `operational_map.json`, drafted by A3 and checked
against its prose by A9 (I13).

### 10.4 Independent second implementations

Issue 13 asked which code paths get an independent check, against what, and
at what tolerance. Every derived quantity the verdict rests on has one:

| code path | independent implementation | cross-check | tolerance | check |
|---|---|---|---|---|
| `sky.py` rise and set | JPL Horizons rise/transit/set; the grid-plus-bisection finder of `results/critique-design/check_mwra.py` | 1,000 events; 2,000 events | 0.5 min; 0.1 s | I5 |
| `events.py` stations, greatest elongations, azimuth extrema | `results/bm2008-reconcile/check_mwra.py`; the Standish code of `results/bm2008-b-checks/` | 152 S2 years; 500 events | same civil date in ≥ 150/152 and 0.05 d; 1 d | I6 |
| `events.py` heliacal phases, B&M's spring limits | `docs/research_visibility_calc.py` | −1177 and −700 | 1 d | I6 |
| `events.py` first crescent | the Yallop code of `research_visibility_calc.py` | 500 lunations | ≥ 495 equal | I12 |
| `eclipses.py` | NASA's `program.js` in Node (`data/jsex/sites/`); `results/critique-design/check_bessel.py` | 5 sites × 5,486; four totality windows | smag 0.0005, 0.002 h; 5 s | I2 |
| `lunar.py` | NASA LEcat5 | PC-R and ALM centuries plus 300 random | 0.02; 3 min | I4 |
| the B&M reading through `clues.py`, `readings.py`, `search.py` | `tests/bm_reference.py` (A7) | every T0 cell; 300 random years | identical flags | I7 |
| `reach.py` | brute-force sliding windows | 10,000 synthetic sets | 0.0002 | I9 |
| the PC-S generator | Standish code; Horizons subsample | 200 truths (50 via Horizons) | recall 1.000 | I10 |
| `calendar.py` | exhaustive day counting; Horizons calendar | −1999..+500 | exact | I8 (done) |
| `prereg_io.py` | the licence checkers' dump scripts; A9's review | every row | exact | I13 |
| `verdict_rule.py` | the hand-computed synthetic sets | 9 sets | exact | I14 |

### 10.5 Scripts (top level, as in labench)

| script | test | writes |
|---|---|---|
| `reproduce.py` | T0a, T0b, T0c | `results/t0/` |
| `rates.py` | N1 | `results/n1/` |
| `coincidence.py` | N2 | `results/n2/` |
| `garden.py` | N3, R_anc | `results/n3/` |
| `randomepic.py` | N4 | `results/n4/` |
| `windows.py` | N5 | `results/n5/` |
| `deltat.py` | N6 | `results/n6/` |
| `synthetic.py` | PC-S (both modes) | `results/pcs/` |
| `controls.py` | I2b, PC-R | `results/pcr/` |
| `almagest.py` | the *Almagest* control | `results/alm/` |
| `negatives.py` | the negatives, the Iliad comparison, I11 | `results/nc/` |
| `heldout.py` | section 7 | `results/heldout/` |
| `verdict.py` | section 9 | `results/VERDICT.md`, then the findings in `README.md` |
| `read.py` | a reader: `py read.py -1177-04-16` prints the sky of Days −40 to +1 beside each clue and held-out predicate, as labench's `read.py` prints a tablet | stdout |

Every script writes a machine-readable `<name>.json`, a human-readable
`<name>.out.txt` and, where useful, `.tsv` tables, and stamps each output with
the commit and code tree hash it ran under. Tools: `tools/fetch_ephem.py`
(extend to +300), `tools/fetch_lecat.py`, `tools/fetch_horizons_rts.py`,
`tools/build_sky.py`, `tools/build_events.py`, `tools/build_eclipses.py`,
`tools/build_truth_index.py`, `tools/validate_events.py`,
`tools/validate_eclipses.py`, `tools/freeze.py`; existing:
`validate_ephem.py`, `validate_coverage.py`, `fetch_jsex.py`,
`jsex_sites.js`, `fetch_stars.py`.

Tests (each runnable as `py tests/test_x.py`): `test_calendar.py` and
`test_ephem.py` (exist); `test_t0.py` (S2 replay, A1–A5); `test_reach.py`
(I9); `test_clues.py` (hand-built predicate cases, the B&M reading on S2's
rows); `bm_reference.py` (I7); `test_eclipses.py` (I2); `test_lunar.py`
(I4); `test_events.py` (I5, I6, I12); `test_prereg_io.py` (I13);
`test_verdict.py` (I14).

---

## 11. Data, run order and run times

### 11.1 Data still to acquire

| what | from | size | why |
|---|---|---|---|
| DE441 excerpt +200..+300, the same 11 bodies | NAIF `de441_part-1.bsp` by HTTP Range (`tools/fetch_ephem.py`) | about 10 MB [me: 30 MB per 290 years, scaled] | *Almagest* and PC-R windows reach +277 (4.1); the current excerpt ends at +241 [acq §1.1] |
| DE431 Sun, EMB, Earth, Moon +200..+300 | NAIF `de431_part-2.bsp` | about 6 MB | lunar-timed quantities for the same windows |
| NASA LEcat5 century pages −1999..+300 | eclipse.gsfc.nasa.gov/LEcat5 (`tools/fetch_lecat.py`) | about 23 × 60 kB; 10 already in `results/controls/nasa/` | I4 |
| Horizons rise/transit/set for 1,000 events; positions for 50 PC-S truths | Horizons API (`tools/fetch_horizons_rts.py`), cached in `data/ephem/horizons/` with the request URL on line 1 | small | I5, I10 |
| the *Almagest* reference stars (δ Cap, β and ζ Tau, Castor, Pollux, ζ Gem, Spica, Regulus, Antares, α Lib, β and δ Sco, β, γ and η Vir, δ Cnc, λ, φ and ψ1–3 Aqr, the Pleiades) | `tools/fetch_stars.py` (SIMBAD identifiers, hip2 rows, as in [acq §3]); the drafter fetched them for its own run into `results/controls-almagest/stars.json`, in memory only [alm §1.5] | small | the full primary run of 6.4 (the gate's projection does not use them) |

Fetch with Python urllib or the PowerShell tool: Git Bash's curl carries a
2020 CA bundle, so an HTTPS failure there is local. No library access beyond
`py -m odybench.ccx`. Every new file's SHA-256 goes into `data/SHA256SUMS`.

### 11.2 Run order and expected times

Measured on this machine (16 logical cores): `ephem.altaz` at about
28,000–29,000 body-positions a second per core; `ephem.new_moons` 23.0 s per
136 years; `validate_ephem.py` 118–188 s [v1 §7.5; acq §1.3]. The other
figures are estimates from these.

| # | step | command | estimate | basis |
|---|---|---|---|---|
| 0 | fetch | `py tools/fetch_ephem.py`, `py tools/fetch_lecat.py`, `py tools/fetch_horizons_rts.py` | 10–20 min | network |
| 1 | build code; unit tests | agents (10.1) | — | |
| 2 | sky tables, events, catalogues (needed by the pre-freeze checks) | `py tools/build_sky.py --all`; `py tools/build_events.py`; `py tools/build_eclipses.py` | 1.5–3 h, once | about 170 evaluations a day per site (7 bodies × 2 events × about 4 iterations, twilights, 9 stars) over 1,520 years: about 94 million per site, about 55 min on one core and 5 min on 14; about 17 sites. Eclipses: 5,486 × about 55 sites (36 rotated) with totality bisections |
| 3 | pre-freeze instrument checks I1–I6, I8, I9, I12–I14 | `py tools/validate_ephem.py`; `py tools/validate_events.py`; `py tools/validate_eclipses.py`; `py tests/test_*.py` | 30–60 min | |
| 4 | pre-freeze tasks: re-draft (6.3.3) then I2b; the negatives' second reading (6.5); `operational_map.json` review; builders retired (12.1) | agents | — | |
| 5 | **freeze** | `py tools/freeze.py` | seconds | section 12 |
| 6 | post-freeze instrument checks I7, I10, I11 | `py tests/bm_reference.py`; `py synthetic.py --instrument`; `py negatives.py --plumbing` | 10 min | |
| 7 | T0 | `py reproduce.py` | 5 min | |
| 8 | N1, N2, N5 | `py rates.py`; `py coincidence.py`; `py windows.py` | 5–10 min | lookups on cached tables |
| 9 | N6 | `py deltat.py` | 20–40 min | about 45 totality windows on DE431 |
| 10 | N3 and R_anc | `py garden.py` | 0.5–2 h | 3.07 million FULL readings × about 17,000 candidates as packed bit ANDs on 14 workers, with the gap test of 10.2 |
| 11 | N4 | `py randomepic.py` | 30–60 min | 20,000 epics; stratum epic gardens |
| 12 | PC-S science mode | `py synthetic.py` | 20–40 min | 2,000 truths × 12 noise cells × 1,144 readings |
| 13 | PC-R and the *Almagest* control | `py controls.py`; `py almagest.py` | 20–40 min | 21 windows per set; site "none" grids |
| 14 | negatives | `py negatives.py` | 20–40 min | 13 sets × gardens × 2 (plus 40) windows |
| 15 | held-out | `py heldout.py` | 5 min | |
| 16 | verdict | `py verdict.py` | seconds | |

About 4–8 hours of computation after the freeze, most of it in steps 10–14;
step 2 is cached and run once.

---

## 12. Freezing and amendments

Revision 1 hashed only `DESIGN.md` and `data/prereg/`, on a machine with no
version control, and let every script run unfrozen. Nothing covered the
code, and nothing could refute a charge that thresholds or code changed after
the results [rev #4]. The freeze is now a local git commit.

### 12.1 Before the freeze (all must hold)

1. Every module of 10.2 exists and its unit tests pass.
2. Pre-freeze instrument checks I1–I6, I8, I9, I12–I14 pass (6.1).
3. The unexposed re-draft of 6.3.3 is in `data/prereg/pcr_redraft.json`, and
   I2b has run after it (I2b computes local magnitudes at the truth dates, so
   it must not run before the re-draft exists).
4. The negatives' second reading of 6.5 is done, and its re-pinned readings
   are in `negatives.json` as a recorded edit (a script that rebuilds from
   the licence-checked copy, like the licence checkers' own).
5. `data/prereg/operational_map.json` is complete and reviewed (I13).
6. **The three builders are retired.** `results/controls-real-drafting/build_controls_real.py`,
   `results/controls-almagest/build_prereg.py` and
   `results/negatives/build_negatives.py` would each silently undo the licence
   checks' edits if re-run [lcr; lca; lcn §4.1]. The frozen JSON files are the
   record; the builders are kept for provenance and marked "do not re-run" in
   their first line by their owners or, failing that, listed here as retired.
   `tools/freeze.py` refuses to freeze if any of the three clue files differs
   from the output of its recorded edit scripts (the licence checkers'
   replays from their saved pre-edit copies, followed, for the negatives, by
   the second reader's script).
7. The new prereg files exist: `sites.json`, `windows.json`, `seeds.json`,
   `deltat_models.json`, `readings.json`, `garden.json`, `epic_grammar.json`,
   `heldout.json`, `eclipse_hit.json`, `verdict_rule.json`,
   `verdict_synthetic/`, `operational_map.json`, `pcr_redraft.json`,
   `truth_index.json`, `i2b_reference.json`.
8. `data/SHA256SUMS` is extended to every file in `data/text/`, `data/refs/`
   and the new ephemeris and catalogue files.

### 12.2 The repository

- `git init` in `C:\Projects\odybench`: a local repository with no remote.
  Commits use the machine's existing git identity; nothing is pushed.
- **Committed:** `DESIGN.md`, `docs/`, `odybench/`, `tools/`, `tests/`, the
  top-level scripts, `data/prereg/` (truth files included: the searcher's
  isolation is enforced by code and test, not by hiding files),
  `data/stars.json`, `data/SHA256SUMS`, and the scripts in `results/` with
  their own text outputs, which record what was known before the freeze.
- **Hashed, not committed** (listed in `data/SHA256SUMS`): the ephemeris
  `.bsp` files, `data/jsex/`, `data/text/*.tsv` (exported from Jon's library,
  some in copyright), `data/refs/` (PDFs and their extracted text),
  `data/cache/`, every large binary in `results/`, and every copy of a
  publication kept in `results/` (for example the extracted texts
  `results/data-acquisition/bond2017.txt` and
  `results/controls-real-drafting/gautschy-eclipsecitations.txt`, and the
  PDFs and HTML in `results/unread-primaries/`). Nothing copyrighted enters
  the repository, so a later decision to publish it cannot publish a text by
  accident.

### 12.3 The freeze

`tools/freeze.py`, run on a clean working tree:

1. checks every hash in `data/SHA256SUMS` and the conditions of 12.1;
2. commits everything listed above as the **freeze commit** and tags it
   `prereg-1`;
3. writes `PREREG.sha256` at the repository root, holding: the freeze commit
   hash; the git tree hashes of `odybench/`, `tools/`, `tests/` and
   `data/prereg/` at that commit (`git rev-parse prereg-1:odybench` and so
   on); the blob hashes of `DESIGN.md` and of each top-level script; and a
   git-independent **code tree hash**: the SHA-256 of the sorted lines
   "`<sha256>  <path>`" over every file in `odybench/`, `tools/`, `tests/`,
   `data/prereg/`, `DESIGN.md` and the top-level scripts;
4. commits `PREREG.sha256` alone in the next commit (a file cannot hold the
   hash of the commit that contains it).

Every analysis script calls `prereg.check_frozen()` at start: HEAD must
descend from `prereg-1`, the working tree must be clean, and the current code
tree hash must equal the frozen one or the latest amendment's. Otherwise the
script stops. `--unfrozen` lets it run but stamps every output EXPLORATORY in
its first line, and `verdict.py` refuses to read such outputs.

### 12.4 Amendments

A change to any frozen file after the freeze, code included, is allowed only
as a dated amendment appended to section 12.6 below: what changed, why, the
diff's hash, and **which outputs had already been read** when it was made, in
the way indusbench recorded its correction to test 1 [indusbench DESIGN §4].
The amendment is committed, and its new code tree hash is appended to
`PREREG.sha256` under the old lines, so the file keeps the whole history.
The controls file's own history is recorded the same way: drafted and frozen
before any accepted date was looked up (`eb1f0401…9256`), then licence-checked
by an agent blind to the truth (`135fba67…83f8`) [lcr].

### 12.5 Publishing the hash

Publishing the hash outside the machine (for example a public commit or gist
under the research identity Jon uses for open work, or an OpenTimestamps
proof of `PREREG.sha256`) would give an outside timestamp. It is
**optional and needs Jon's explicit permission**; the bench does not assume
it. Until he gives it, the freeze is verifiable only on this machine, and
`VERDICT.md` says so in its first lines.

### 12.6 Amendments made after the freeze

None yet.

---

## 13. What the dossier could not settle, and how each is handled

| # | open fact | why it is open | handling |
|---|---|---|---|
| 1 | What "Ti = New Moon" means operationally | no single rule reproduces S2's Ti column [bm §5 N] | T0b pins the UT+2 conjunction date (136/152); F2 carries LMT, +1 day and first crescent |
| 2 | Which New Moon when two qualify; S2's out-of-window Ti | S2 follows no consistent rule [bm §7] | T0b evaluates every qualifying New Moon; T0a replays S2 as printed |
| 3 | Why 14 S2 MWRA dates sit 4–8 days from DE441's maxima | Starry Night's Mercury theory, another horizon, or plot reading [bm §5 M] | DE441 vertex maxima used; the integer replay is a regression check (A3) |
| 4 | Mercury's visibility on Ti−34 | never tabulated; **PLSV has no extinction model** (settled [unread §6]) | visibility off, AV 10° and PLSV's AV formula at a 1° critical altitude, all in the T0 grid; a physical extinction model is an upgrade, not a prerequisite |
| 5 | The Pleiades and Arcturus cut-offs (17 Feb; 3, 4 or 5 Apr) | three dates in paper and SI [bm §5 C] | T0b uses 17 Feb / 4 Apr; C_rel is calibrated to them at −1177; F3 carries 2°, 5°, autumn and none |
| 6 | The ṅ and ΔT formula of Starry Night 6.0.4 | unpublished; two published Starry Night values cannot come from one smooth ΔT(t) [unread §7] | 27,602.7 s is the T0b clock only and is never converted |
| 7 | ΔT at −1177 | SMH's own formulations span 681 s; every value before −720 is extrapolation [eph §8] | four models and their mixture (N6), with each σ as a Gaussian (an assumption, stated) |
| 8 | Lunar ephemeris to pair with SMH | DE441's tidal model is unpublished; DE441 − DE431 = +188 s at −1177 [eph §5.3] | lunar-timed quantities on DE431; planets on DE441 (section 0) |
| 9 | Which island is Homeric Ithaca | modern dispute | Ithaki primary; four sensitivity sites; Paliki dropped (section 0) |
| 10 | Lefkada's coordinates | 20.70 in the site catalogue, 20.71 in research-ephemeris [acq §6 item 5] | 20.70 adopted (section 0) |
| 11 | Departure hour from Ogygia; Athena's night in Sparta | the Greek does not say [chron §4.B, §4.F] | F1's grid; F1b for the typical numbers |
| 12 | What Day 0 is; Apollo's feast on the new moon or the 7th | text silent; ancient sources split [txt §5.1, §5.3] | F2 (a)–(d); the 7th as an epic anchor in N4 |
| 13 | The Greek day boundary | not verified from a primary source [vis §6 item 4] | F2 (d) uses a sunset day, (c) a civil day |
| 14 | The meaning of "late-setting" Boötes | late, slow, or Aratus' autumn evenings [txt §5.8; vis §3.1] | F3 (a′)–(f) |
| 15 | Whether the morning star is Venus | Homer's names are separate [vis §1.4] | F4 includes any bright herald and none |
| 16 | The equinox bound | ≤ 4 Apr (§Intersecting), ≤ 5 Apr (§References), XXX = ≤ 6 Apr (S2) [bm §5 E; rev #23] | the T0 grid and F6 carry all three |
| 17 | The window | text 1250–1115 BC, S2 1251–1100 BC; drawn from the tradition that chose the eclipse [bm §6; win §6] | the reproduction window as stated; N5 runs five; G_any reported beside G |
| 18 | Which three lines schol. 14.162 suspects | commentaries not available [txt §10] | every result is conditional on 14.162 = 19.307 being read as a month-turn at all |
| 19 | Primary sources | **read now**: MacDonald 1967 (pp. 324–327), Papamarinopoulos et al. 2012, Henriksson 2012, PLSV 3.1 documentation, Neugebauer & Schoch 1927 [unread §1]. **Still unread**: P. V. Neugebauer 1929 (paywall; Jon could open the HathiTrust record himself), Schoch's *Die Sterne* 6:88 and *Dichter-Finsternisse*, P.Oxy. 3710 (papyri.info needs Jon's approval for the browser), Austin 1975, de Jong 2001 App. A, Stanford 1959, the Oxford commentaries, Starry Night internals | no computed number depends on them; MacDonald's March reading is now documented with the eclipse in view (1.1), which decides p_fix\|C as primary (5.1) |
| 20 | Herwart von Hohenburg's 1612 date | known only through Fotheringham 1921 [crit §1.2] | historical note only |
| 21 | Arcus visionis models are crude | AV bands stand in for extinction; weather moves first and last dates by ±3 to ±15 d [vis §1.2, §6] | AV values are forks; the slack of real observers is measured on the *Almagest* (6.4) |
| 22 | Correlated ΔT errors of 1178 and 1131 BC | 47 years apart [win §7.1] | joint probabilities under a common offset (P26) |
| 23 | The prior for oral transmission of a dated sky | no comparative case [win §10–11] | not quantified; likelihood ratios only |
| 24 | Ephemeris coverage | settled to +241 [acq §1]; controls need +300 | fetched in step 0 (11.1) |
| 25 | Ancient Troy dates | through B&M, Wikipedia and Clement's list as reported by Papamarinopoulos et al. [win §3, §12; unread §4], not FGrHist | the primary window's envelope and H6 only; *secondary* |
| 26 | Hermes = Mercury, and whether any god-movement is astronomical | no ancient parallel before Plato [txt §5.9] | not adjudicated: F5 none; H3–H4 test the rule's consistency |
| 27 | ΔT σ before −2000; the σ discontinuity at −500 | extrapolation; Huber vs MS2004 on NASA's page [acq §6 items 3–4] | no eclipse in the bench before −1999; the discontinuity is reported where a control sits near −500 |
| 28 | Sirius' orbit model | about 1′ at −1177 between published and re-referred proper motions [acq §3.3] | the published centre-of-mass motion is adopted; the re-referred one is a sensitivity; a photocentre motion is never used |
| 29 | The *Almagest* glosses and cruxes | unit glosses (moon 0.5°, cubit 2°, finger 1/12°) and star identifications are the drafter's; IX.7.11 and IX.9.4 are textual cruxes; Heiberg's apparatus and Toomer not consulted [alm §6; lca] | crux intervals are forks (primary as printed); star rows are outside the gate's projection |
| 30 | Exposure of the PC-R drafter | had seen computed answers [pcr §1] | unexposed re-draft of the three flagged rows (6.3.3) |
| 31 | Single words in the negatives | Eous (*Aen.* 3.588), vesper (VF 7.1), ἔκλιθεν (*Arg.* 3.1196), διχόμηνις (*Arg.* 1.1231); Servius and the Apollonius scholia not in the library [neg §6 item 3] | forked, with none |
| 32 | The Meeus ch. 7 values in `test_calendar.py` | recalled, not read [acq §6 item 7] | each also agrees with exhaustive day counting and Horizons, so a wrong one would fail |
| 33 | The accepted dates of the PC-R controls | taken from secondary sources: summaries of Toomer and Pedersen, Gautschy's citation list, NASA's historical-eclipse page; Toomer's translation was not consulted; Gautschy's "424 BC May 21" for Thuc. 4.52 is apparently a slip for 21 Mar [pcr problems] | every accepted date was also recomputed by the drafter; the harness uses `truth_index.json` built from the truth file, and the report marks the sources *secondary* |
| 34 | Coordinates of the negatives' places | Wikipedia coordinates; Giresun Island for the Island of Ares and Cape Sideros for Salmonis are modern identifications; representative points stand in for regions [neg §6 item 4; lcn §4.5] | used as recorded; a gazetteer check (Pleiades) is a pre-freeze task for the second reader of 6.5, and site sensitivity is not expected to matter for star phases |
| 35 | Numeric thresholds in the negatives that are the drafter's but not marked as such (±1 d, ±7 or ±15 d, 2° and 5° altitudes, fraction ≤ 0.25, 2–3 h) | operationalisations of stated features [lcn §4.3] | kept; listed by the second reader in `operational_map.json` with a "drafter's threshold" flag |

---

## 14. Resolution of the review

Each of the 25 issues of `docs/critique-design.md`, with its resolution and
the sections that changed. Where the resolution departs from the critique's
proposed fix, the row says why.

| # | severity | resolution | sections |
|---|---|---|---|
| 1 | blocker | The decision rule is rewritten as a pure function of named quantities (9.1–9.2), each produced by one script. Every condition names its garden: 𝒢_BM primary, 𝒢_DOC when Q_BM holds, 𝒢_DOC and 𝒢_FULL as printed sensitivities. Revision 1's unreachable NC condition is replaced by the critique's calibrated percentile, computed target-first: pct_N4, the share of random poems in the Odyssey's specificity stratum whose gardens reach Schoch's target at least as well (5.4). "Dates fiction" is the critique's definition with hit strength: a clean negative's unique survivor is an eclipse at least as strong as the Odyssey's and its G is no larger (6.5). G has one sense (a p-value) throughout. Nine synthetic input sets prove every outcome, the inconclusive verdict, the qualifier path and the instrument block reachable (9.3), and are a test (I14). **Departure:** the percentile is taken on the reach of Schoch's target rather than on G, because G of a text with few clues falls to 0 whether or not it is dated, the same flaw the critique found in the NC condition. | 1.3, 5.4, 6.5, 9 |
| 2 | blocker | `controls_real.json` was rebuilt from the texts by a drafter, one row per clue with its licensing words, frozen before any accepted date was looked up, and licence-checked by an agent blind to the truth; no leak of the critique's table survives [pcr; lcr]. Unstated features are forks with "none"; Roman dates carry a free offset; Livy's prodigies are a hard case. PC-R uses the file exactly as licensed; the drafter's partial exposure is measured by an unexposed re-draft of the three flagged rows, and Q_exposure reports whether gate 3a depends on it (6.3.3). The site primaries stay "none", with the reason (6.3.4). | 2.6, 6.3, 9 |
| 3 | blocker | Outcome 3 is split into 3a (eclipse component; PC-R gate) and 3b (B&M-type component; the *Almagest* control, 12 sets of dated Mercury, Venus, lunar-phase and equinox records, plus PC-S). The *Almagest* sets are scored at B&M's tolerances and at the measured observer slack; failure at slack fires 3b, failure at B&M's tolerances sets Q_BM, which conditions every "no" and blocks outcome 1 unless it also holds in the documented garden (6.4, 9.2). The overlap of IV.6.14 is counted once. | 1.3, 2.6, 6.2, 6.4, 9 |
| 4 | major | The freeze is a local git commit of the design, the prereg files and all code, made before any null, control or held-out result; `PREREG.sha256` holds the commit hash, git tree hashes and a git-independent code tree hash; post-freeze changes are dated amendments that state which outputs had been read; unfrozen runs are stamped and ignored by the verdict. Publishing the hash is optional and needs Jon's permission (12.5). | 12 |
| 5 | major | Section 1.1 now says the 6 years is the C ∧ E rate. Prediction 6 is replaced by the two comparisons the critique proposed: λ with E against B&M's printed 0.048 (P9), and λ without E against B&M's own arithmetic redone at ±1 d, 0.88 per century (P8). | 1.1, 2.4, 5.1, 8 |
| 6 | major | MacDonald 1967 has been read: he argues for March, with the 1178 BC eclipse in view, and fits his timetable to it; Gainsford misreads him [unread §2]. Nothing documents an eclipse-blind spring reading, so p_fix\|C stays primary and the reason is frozen in 5.1; the unconditional p_fix is reported as the counterfactual. The same reasoning conditions G on the season (5.3). §8 item 19 is corrected (13 row 19). | 1.1, 2.5, 5.1, 5.3, 13 |
| 7 | major | Three nested gardens with the option-level source of every fork in `garden.json`: 𝒢_BM (144, primary), 𝒢_DOC (143,856, named proponents) and 𝒢_FULL (3,068,928, upper bound); G for all three and the greedy smallest fork set that reaches G ≥ 0.05 are reported. | 5.3, 9 |
| 8 | major | Fork F1b prices the typical numbers: ±2 or ±3 d on every offset that depends on a typical-number joint (DOC), or the 17/18-day count replaced by 9, 12 or 20 (FULL). PC-S runs jitter 0–3 d and reports the decay of reach and recall; LR is a curve over it. | 5.3, 5.7, 6.2 |
| 9 | major | Outside T0b, season and equinox bounds are computed each year: C_rel, calibrated so that it equals B&M's printed bounds at −1177, and E_rel relative to the computed equinox. λ is reported per century under both relative and fixed bounds (P13). The PC-S generator and searcher share the relative definitions. | 4.5, 5.1, 6.2, 8 |
| 10 | major | Binary classes are replaced by probabilistic hit strength under the ΔT mixture (h_tot, h_09, h_06); the background is extended to −1999; the target is excluded from its own base rate; a site-rotated rate is computed; 10–12 h (Schoch's rule) and 10–14 h, and ±0.5σ, ±1σ, ±2σ envelopes are reported. The label "Schoch's" is removed from the 10–14 h class. | 4.1, 4.4, 5.2 |
| 11 | major | Held-out base rates are conditional on the reading (among its own survivors, and among P_spring candidates passing N and C); H1 and H5 are labelled non-blind and left out of the counted statistic; the statistics are also run on R_anc's survivors. | 7 |
| 12 | major | MWRA is the vertex of a parabola over 7 mornings, Δ is continuous, rises are converged below 0.1 s, every maximum records curvature and margin and flat ones are flagged; the M pass set is reported under h0 ± 0.1°, latitude 38.2–38.6°, refraction on and off and ΔT ± 1σ; the cross-check against `check_mwra.py` on all 152 S2 years is I6. B&M's integer definition is kept as the literal replay. | 2.2, 3.2, 6.1 |
| 13 | major | Every derived quantity has an independent second implementation or reference with a stated tolerance (10.4): Horizons and a grid-plus-bisection finder for rises; `check_mwra.py` and the Standish code for events; `research_visibility_calc.py` for star phases and crescents; NASA's JavaScript and the review's Besselian solver for eclipses; NASA LEcat5 for lunar eclipses; `tests/bm_reference.py`, written blind to the bench code, for B&M's reading; brute force for reach. The calendar module and the `datetime` ban exist and pass. | 0, 6.1, 10.4 |
| 14 | major | PC-S has an instrument mode (shared grammar, descriptions from an independent code path, recall 1.000 required) and a science mode (the generator follows the observation hypothesis, every garden reading is scored, no bug threshold). | 6.2 |
| 15 | major | The Iliad is a same-tradition comparison. Twelve clean negatives were drafted under the Odyssey's own rules (both readings of *Aen.* 2.255, with 2.340's conflict; Apollonius without the simile and with the missed full Moon; Quintus; Valerius; *Aen.* 4's Hermes) and licence-checked [neg; lcn]. Random poems are the main negative (pct_N4). NC4 and NC5 become plumbing check I11; NC4's misreading of *h.Herm.* 141 is dropped. | 2.5, 5.4, 6.1, 6.5 |
| 16 | major | Both sides of the ratio count one event on one class of target, and the denominator is G, a mean over thousands of targets, so it is not under-sampled. LR is a curve over a noise grid (jitter 0–3 d, Mercury slack 0–6 d); outcome 2 uses its upper bound at the noise most favourable to B&M, outcome 1 the lower bound at realistic noise. The Venus 16-day slack is dropped. **Departure:** the critique's same-event fix is kept, but the event is target-first (R_obs / G), because Schoch fixed the target before the clues were read for it; the survivors-first ratio with the random-epic double-hit denominator (the critique's version, which credits the eclipse's rarity) is reported as LR_sf and kept out of the rule. | 5.4, 5.7, 9 |
| 17 | major | Everything already computed is in section 2 with its numbers, including the per-model P(total) table, the mixture (0.304), P(smag ≥ 0.9) (0.928), the 1.9% date flips and the *Almagest* and PC-R facts. Revision 1's prediction 19 is restated per model (P26); predictions 18, 20, 21 and 24 are retired with their status (2.7). Section 8 keeps only quantities that need new runs; P1–P7 and P34 are marked as uncounted. | 2, 8 |
| 18 | major | R_anc, the ancient reading (the scholia's autumn, the conjunction, Theoclymenus' vision as an eclipse, no planets), is a pinned reading reported beside B&M's, with its survivors and their hit strength; the held-out statistics run on it (P23). | 5.3, 7, 8 |
| 19 | minor | Espenak–Meeus is one model in its canon frame; the mixture is over four models; the −26 form is not used. | 0, 2.3, 5.6 |
| 20 | minor | A1–A5 are labelled regression tests; I3 is labelled a calibration, and star phases are validated independently (I6c). | 3.4, 6.1 |
| 21 | minor | One magnitude definition per use: smag (fraction of the diameter), obscuration, a separate central flag with duration, umag and pmag; the diameter ratio is never called a magnitude; I2b compares like with like and, near 1, compares flags and durations. | 0, 6.1 |
| 22 | minor | The epoch is −1176.68 (the "−1177.29" label is corrected); the window is half-open and ends at 24:00 UT+2 on 31 Dec −1114, built with `calendar.span_bounds`; the TT–UT conversion and Julian-epoch formula are stated; the count is predicted (P7). | 0, 2.2, 3.2, 8 |
| 23 | minor | T0 is a grid over E ≤ 4, 5, 6 Apr, Mercury visibility off, AV 10° and PLSV, and both MWRA definitions; T0b's own reading is a member of 𝒢_BM. | 3.2, 3.5, 5.3 |
| 24 | minor | (a) H8 is withdrawn; (b) H2's base rate is corrected and H2 is counted; (c) the reach statement is corrected (≤ 0.081, 0 if a survivor lies in −1176..−1052; P16); (d) "Schoch's" is removed from the 10–14 h class; (e) §8 item 19 now records MacDonald as read; (f) 1.1 item 2 says the 6 years includes E. | 1.1, 4.4, 5.3, 7, 13 |
| 25 | minor | HIP numbers were verified against SIMBAD and hip2 (all five confirmed); Sirius uses the Hipparcos centre-of-mass proper motion, recorded with its 1′ orbit-model uncertainty; a photocentre motion is excluded. | 2.1, 13 |

---

## Sources

The dossier, in `docs/`:

- `research-bm2008.md` (with `research-bm2008-a.md`, `-b.md`), the
  reconciled spec of Baikouzis & Magnasco 2008; scripts in
  `results/bm2008-reconcile/`.
- `research-chronology.md`, the day count from the Greek and the 8-row grid.
- `research-textclues.md`, the 76-row clue inventory; scripts in
  `docs/textclues-scripts/`.
- `research-ephemeris.md`, the computation stack (`odybench/ephem.py`,
  `tools/validate_ephem.py`, `results/validate_ephem.txt`).
- `research-visibility.md`, chance rates for each clue reading;
  `docs/research_visibility_calc.py`, `results/research-visibility.json`.
- `research-controls.md`, positive, hard and negative controls;
  `results/controls/`.
- `research-critiques.md`, the responses since Schoch;
  `results/research-critiques/`.
- `research-window.md`, the window, Ithaca's eclipse base rates and window
  scaling; `results/window/jsex/`.
- `critique-design.md`, the adversarial review of revision 1;
  `results/critique-design/`.
- `data-acquisition.md`, the ephemeris extension, NASA elements, stars and
  calendar; `results/data-acquisition/`.
- `controls-real-drafting.md` and `license-check-controls-real.md`, the real
  eclipse controls; `results/controls-real-drafting/`,
  `results/license-check-controls-real/`.
- `controls-almagest.md` and `license-check-almagest.md`, the *Almagest*
  control; `results/controls-almagest/`, `results/license-check-almagest/`.
- `negatives-drafting.md` and `license-check-negatives.md`, the negative
  controls; `results/negatives/`, `results/license-check-negatives/`.
- `research-unread-primaries.md`, MacDonald, Schoch and Neugebauer,
  Papamarinopoulos, Henriksson and PLSV; `results/unread-primaries/`.
- `DESIGN-v1.md`, revision 1 of this design.

Primary items behind them, as the notes read them: Baikouzis & Magnasco,
PNAS 105 (2008) 8823–8828, doi:10.1073/pnas.0803317105, with its Supporting
Information and Table S2 (`data/bm2008-a/`); Schoch, *The Observatory* 49
(1926) 19–21; MacDonald, *JBAA* 77 (1967) 324–327; Papamarinopoulos et al.,
*MAA* 12(1) (2012) 117–128; Henriksson, *MAA* 12(1) (2012) 63–76;
Neugebauer & Schoch, *AN* 230 (1927) 57; Gainsford, *TAPA* 142 (2012) 1–22
(*secondary* where it reports MacDonald); Espenak & Meeus, *Five Millennium
Canon of Solar Eclipses* (NASA TP-2006-214141) and its JavaScript Explorer;
NASA's lunar eclipse catalogue (LEcat5); Stephenson, Morrison & Hohenkerk
2016 and the Addendum 2020; JPL DE441 and DE431 (Park et al. 2021); van
Leeuwen 2007 (Hipparcos new reduction), ESA 1997, Bond et al. 2017 (Sirius);
the PLSV 3.1 documentation (Lange & Swerdlow); the Odyssey, Iliad and their
scholia, Ptolemy's *Syntaxis* (Heiberg), Thucydides, Xenophon, Arrian,
Plutarch, Curtius, Pliny, Livy, Diodorus, Virgil, Apollonius, Quintus
Smyrnaeus, Valerius Flaccus, Hesiod and Aratus, exported read-only from
ClassicaCodex into `data/text/`. The bench designs this follows:
`C:\Projects\labench\README.md` and `C:\Projects\indusbench\DESIGN.md`.

