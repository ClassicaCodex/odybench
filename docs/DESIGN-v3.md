# odybench — design (revision 3)

A test bench for the claim that the sky clues in the Odyssey date the
slaughter of the suitors to 16 April 1178 BC. It is the fourth in the series
after vbench (Voynich), [labench](../labench/README.md) (Linear A) and
[indusbench](../indusbench/DESIGN.md) (Indus script), and it keeps their rule:
every test is run first on cases whose answer is known, so that a "no" about
the Odyssey means something.

Revision 3, written 2026-10-04. Revision 1 (2026-10-03) is kept unchanged as
`docs/DESIGN-v1.md` and revision 2 (earlier on 2026-10-04) as
`docs/DESIGN-v2.md`. Two adversarial reviews shaped it:

- `docs/critique-design.md` reviewed revision 1: 25 issues, 3 of them
  blockers.
- `docs/critique-design-r1.md` rechecked revision 2. It found 20 of those 25
  resolved and raised 17 new issues, N1–N17, one of them a blocker: the
  likelihood ratio that outcome 1 needed could never exceed about 6.5, so the
  bench could never say "yes".

Revision 3 answers both. Its main changes are these:

- **No likelihood ratio enters the decision rule.** The ceiling the recheck
  found is a true property of the text's words, and it is now reported as a
  finding (section 5.7).
- **Every clue reading formed with the target in view is treated alike.** G
  is taken over targets that satisfy the season, Venus and Mercury readings,
  the equinox clue is left out of every garden the rule reads, and T0 must
  reproduce without it (section 5.3).
- **The background runs to AD 200,** so that the conditioned target pool is
  large enough for outcome 1's interval to be attainable (section 4.1).
- **The *Almagest* gate is calibrated leave-one-set-out,** and B&M's own
  option rule is named, so gate 3b can fire and Q_BM is defined (section 6.4).
- **Solar-eclipse controls are scored under the ΔT mixture,** and the controls
  that helped fit a ΔT model are reported apart (section 6.3).
- **Every synthetic input set is checked against the rule's structural
  constraints,** so that the reachability test proves outcomes, not branches
  (section 9).

Section 14 lists all 42 issues with their resolutions.

**Status.** Built and validated: `odybench/ephem.py`, `odybench/ccx.py`,
`odybench/calendar.py` and the data in section 2.1. Drafted and
licence-checked, not frozen: `data/prereg/controls_real.json`,
`controls_almagest.json` and `negatives.json`. No other bench code exists. No
null model, control search or held-out check has been run. Everything in
sections 3–9 is frozen in a local git commit before any of them runs
(section 12). Section 2 lists what is already known, including what the
known numbers already imply for the verdict. Section 8 lists, with
thresholds, only what needs new runs.

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

  Each row also carries the site's span (Julian years) and the sky-table
  columns it needs. Only Ithaki needs every column over the whole span (4.1)
  [r1 N12].

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
  extrapolation [acq §6 item 3]; no eclipse in the bench lies there. **Every
  ΔT-dependent quantity of a control row or a hit strength is scored under
  the mixture**, each model converted to the frame of the elements or
  ephemeris used (4.4, 6.3.3) [r1 N4]. B&M's 27,602.7 s is T0b's clock
  only.
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
| [r1 Nn], [r1 §n] | `docs/critique-design-r1.md`, new issue Nn or section n (the recheck of revision 2) |
| [r1: script] | a script of the recheck in `results/critique-design-r1/`, with its `.out.txt` |
| [v1 §n], [v2 §n] | `docs/DESIGN-v1.md`, `docs/DESIGN-v2.md` |
| [B&M §X] | the paper: Baikouzis & Magnasco, PNAS 105 (2008) 8823–8828, by section heading; [SI], [S2] its Supporting Information |
| [Od. x.y] | Greek text, `data/text/odyssey-grc.tsv` |
| [me], [me: script] | reasoned or computed for this design; arithmetic is shown, and revision 3's scripts are in `results/design-revision-r2/` with their outputs |

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

**What follows for the bench.** N is the one partial exception: the
scholia already read 14.162 as the ἕνη καὶ νέα, the day of conjunction
[txt §5.1]. Even so, N adds nothing to the coincidence, because every target
is a new moon. The record therefore leaves no categorical reading of C, V, M
or E that was formed blind. A target's agreement with a reading formed for
it is not evidence, so the bench applies one rule to all four [r1 N6]:

- C, V and M are conditioned on: G is taken over targets whose sky
  satisfies them (5.3);
- E is left out of every garden the decision rule reads, and B&M's search
  must reproduce without it (3.5).

What remains as evidence is whether B&M's tolerances, beyond the categorical
readings, single out a target more often than chance, and whether clues that
nobody fitted (section 7) agree.

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
  found no comparative case [win §10–11]. The bench reports
  look-elsewhere-corrected p-values, the evidential ceiling of the words and
  a Bayes factor under B&M's own hypothesis (5.7), and stops there.

**A bit budget, to fix ideas** [v1 §1.2; rev §1 confirms the arithmetic].
Singling out one New Moon among the 1,683 in B&M's window takes
log2(1683) = 10.7 bits. B&M's applied clues carry about C 3.6 bits (8.3% of
New Moons pass), V 2.7 bits (15.8% of spring Day −5s) and M 4.5 bits (6/136
rows pass with DE441): 10.8 bits in all, so about one chance survivor is
expected (1,683 × 0.083 × 0.158 × 0.044 = 0.97). The forks of section 5.3
could cost up to 5.2 bits (B&M's own forks, without the equinox), 15.1
bits (the documented garden) or 19.5 bits (the full garden) if the readings
were independent. They are not, and measuring how much of that cost is real
is the job of N3.

The record also shows that every categorical reading behind C, V and M was
formed with the target in view (1.1). Conditioning on those readings
(5.3) removes C's 3.6 bits and the 2.7 bits of the slot event A
(P(A) = 0.154 [r1 N1]). By the recheck's count, about 3.0 bits remain:
B&M's V ∧ M passes about 5 of the 41 targets that satisfy A [r1]. The
per-clue figures do not add up exactly, because V, M and A overlap. Those
remaining bits are what the tolerances add, and they are what G over T_A
prices.

### 1.3 Outcomes

The verdict is a set of labels computed mechanically by `verdict.py` from
named quantities (section 9). Every condition names its garden and its
target pool (section 5.3), and every interval is taken against the claim
being made. The labels:

1. **The text dates the return.** Five things must all hold:
   - B&M's search reproduces as stated, without the equinox clue
     (T0 = R, section 3.5).
   - After the conditioning of section 5.3, a target fixed in advance is
     rarely made the unique match by any of B&M's own readings
     (G_BM,hi ≤ 0.05).
   - Random poems of the same grammar, read with the same freedom, rarely
     reach Schoch's target as well as the Odyssey does (pct_N4,hi ≤ 0.05).
   - Both components of the method can see (section 6).
   - No clean negative dates itself.

   When B&M's tolerances cannot recover expert records (Q_BM), the second
   condition must also hold for the documented garden. The bench then says
   so, and it prints beside the label the evidential weight the words can
   carry (section 5.7).
2. **The match is ordinary.** Either condition is enough:
   - B&M's own readings often make a comparable target the unique match
     (G_BM,lo ≥ 0.20);
   - at least half the random poems of the same specificity reach Schoch's
     target as well as the Odyssey does (pct_N4,lo ≥ 0.50).

   The coincidence then carries no evidential weight, whatever its
   fixed-reading p-value.
3. **The method cannot see**, split by component [rev #3]:
   - **3a, the eclipse component**: the method does not recover the dates of
     real eclipse records (PC-R, section 6.3).
   - **3b, the B&M-type component** (lunar phase, star season, morning star,
     Mercury turning point): the method does not recover the dates of real
     planetary and lunar records of B&M's own kinds, at observer slack
     calibrated on the *other* records (the *Almagest* control, section
     6.4).

   Every "no" about the Odyssey that depends on the failing component is
   reported as "could not have seen it".
4. **The method dates fiction.** A clean negative (fiction composed long
   after the events it tells) yields, under its own sourced readings, an
   eclipse match at least as strong as the Odyssey's (hit_j). Its
   significance must also be at least as great, even at the negative's
   least favourable bound (G_j,hi ≤ G_BM,u). That retires the method, not
   only the claim.

**Inconclusive** is reported when none of the labels applies, with every
quantity and threshold beside it. Labels 2, 3a, 3b and 4 can hold together;
label 1 excludes all the others.

**Qualifiers** are reported whenever they hold:

| qualifier | meaning | section |
|---|---|---|
| Q_BM | B&M's own tolerances and proxies cannot recover expert planetary records | 6.4 |
| Q_strict | an all-clues-must-pass rule rejects the true date of most real eclipse records | 6.3 |
| Q_exposure | gate 3a changes when the possibly steered control rows are re-drafted blind, or when they are set to their sibling convention | 6.3.4 |
| Q_ΔT | gate 3a changes when the controls whose eclipses helped fit the ΔT models are scored without that fit | 6.3.3 |
| Q_attain | with the measured pool sizes, outcome 1 could not have been reached at all; every "no" is then a "could not have said yes" | 9.4 |

**Standing findings** are printed with every verdict and never change a
label. They are: the evidential ceiling of the words (1/P(A), and the Bayes
factor BF_BM under B&M's own encoding hypothesis, section 5.7); the T0 grid
(3.5); the ancient reading R_anc (5.3); and the held-out clues (7).

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
  readings (18.7 bits) [rev §1]. Revision 3's gardens are in section 5.3.
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

- Mercury, 14 records put at or about greatest elongation, offsets from the
  true greatest elongation (record minus event, days) [alm Table 2]:
  - sorted by size: IX.9.3 0.1, IX.9.4 0.2 (printed), IX.7.7 0.8, IX.7.4 1.1,
    IX.7.12 1.1, IX.8.4 1.6, IX.7.16 1.8, IX.7.14 2.7, IX.7.15 2.9, IX.7.11
    3.3 (emended), IX.8.3 3.4, IX.7.9 3.6, IX.7.6 4.2, IX.7.5 5.5;
  - so 3/14 lie within 1 d, 7/14 within 2 d, 12/14 within 4 d and all 14
    within 5.5 d;
  - the elongation stays within 0.5° of its maximum for 5–10 days.
- Venus, 8 records: X.3.2b 0.6 and X.3.2a 1.9 (Ptolemy's pair); X.1.3 16.1,
  X.1.6 16.7, X.2.3 17.8, X.1.5 18.3, X.2.4 20.3, X.1.4 20.6. The last six
  lie on a 34–35-day plateau within 1° of the maximum.
- At B&M's ±1 d, the true dates satisfy every greatest-elongation clue of
  only 2 of the 9 sets that carry one (ALM-A as printed, ALM-E). ALM-C needs
  3.4 d, ALM-G 5.5, ALM-H 3.6 (emended) and ALM-K 2.9; ALM-D, F and L need
  16–21 d.
- B&M's Mercury proxy is a different event. For the 7 morning
  greatest-elongation records, the nearest rising-azimuth maximum lies −2.5
  to +31.8 d away, and only 2 lie within ±3 d. Every Venus morning record
  rises 125–220 min before the Sun, so B&M's ≥ 90-min test does not
  discriminate.
- Oppositions lie within 1.8 d of the true-Sun opposition (0.42 d of the
  mean-Sun one). Planet–star relations lie within 1.7 d, and Moon–planet
  positions within about 2 h of lunar motion. IV.6.14's mid-eclipse is 0.02 h
  from Ptolemy's time, at umag 0.84 against his 5/6. The III.1.10 equinox is
  0.87 d late.
- Ptolemy's own solar tables reproduce his stated mean Sun for 32 of 34
  records to ≤ 0.12°. The two failures are textual cruxes, carried as forks
  (IX.7.11 one Egyptian month, IX.9.4 three days) [alm §1.3–1.4; lca]. The
  primary option of each crux is "as printed".

**What these facts already decide under the frozen regimes of 6.4** [me,
row by row from alm Tables 2 and 5 and the options in
`results/design-revision-r2/alm_options.txt`]:

- **Regime SL** sets each greatest-elongation tolerance leave-one-set-out:
  the smallest listed value at or above the largest offset among the records
  *outside* the set. That gives Mercury 7 d for every set except ALM-G (5 d,
  since its own IX.7.5 is the 5.5-d record and the next largest is IX.7.6 at
  4.2 d), and Venus 21 d for every set (X.1.4, in no set, is the 20.6-d
  record). The true date is then retained in **9 of the 11 counted sets**.
  Two fail:
  - **ALM-G** fails because IX.7.5 lies 5.5 d from the maximum, against
    ALM-G's own tolerance of 5 d.
  - **ALM-H** fails at its primary, printed crux: on the printed date of
    IX.7.11, Mercury stood 3.7° *west* of the Sun, and that evening it set
    12 min *before* the Sun, so `visible_only` fails.

  Whether each of the 9 also narrows its window to 5% has not been computed.
  That is what gate 3b still tests (P25).
- **Regime BM** applies B&M's option rule (6.4): the proxy where a row offers
  it, else the greatest-elongation option, at 1.5 d and 90 min. Under it the
  true date can pass in at most 5 counted sets (ALM-B, E, I, J and L):
  - the MWRA proxy fails every morning Mercury row that offers it, in ALM-A,
    G, H and K (nearest maxima +15.7, +6.2, −2.5, +29.5 and +31.8 d);
  - ALM-D and ALM-F each fail a Venus greatest-elongation row (16.1 and
    20.3 d).

  So **rec_ALM_BM ≤ 5 < 6, and Q_BM holds** whatever the narrowing. It is
  recomputed as a regression check, not predicted [r1 N3].

**The real eclipse records** (`controls_real.json`) [pcr §1, §5; lcr]:

- **Freeze and licence check.** The clue file was frozen before any accepted
  date was looked up (SHA-256 `eb1f0401…9256`, 2026-10-04 05:19 UTC). An
  agent blind to the truth then licence-checked it. That agent moved seven
  unstated-site primaries to "none" and made seven other edits
  (SHA-256 `135fba67…83f8`) [lcr].
- **The drafting was not fully blind.** The drafter had seen critique issue
  2 and revision 1's I2b row, and flags three primaries as possibly steered:
  T1-DARK, D-ECL and the ±1 h in L4-DARK [pcr §1]. The recheck found a
  fourth that the drafter did not flag [r1 N5]:
  - **T2-SEASON's primary "early"** spans solar longitude [330°, 60°]. Its
    start and width are the drafter's.
  - The same set's T1- and T3-SEASON use the half-year [0°, 180°] (Thuc.
    5.20.3).
  - The accepted date has the Sun at 355.3°, so only the primary admits it.
  - T-INT-12's ±0.5-year tolerance is near its edge at the truth (6.63
    years against 7).
- **A rough post-freeze check** (the drafter's lunar model, not the
  bench's; I4 not run) found that the accepted dates fail some primary
  readings:
  - two magnitudes in R-PTOL-BAB;
  - one mid-time in R-PTOL-ALEX, so R-PTOL-CHAIN fails too;
  - the season and the Moon's altitude in R-PYDNA. The accepted Pydna
    eclipse fell about 5 days *before* the solstice, so Livy's "after the
    solstice" is wrong.

  All primaries pass for R-THUC, R-XEN, R-ARBELA and R-DIOD [pcr §5; truth
  file]. These values stay on the truth side.
- **Some controls helped fit the ΔT models** [r1 N4]:
  - SMH's Table S10 v2020 of untimed total and annular eclipses lists −309
    "Greek", 13,300–17,160 s, and −187 "Europe", 12,590–12,900 s
    [`data/ref/Table-S10.2020.txt`]. By year and region these are R-DIOD's
    eclipse and Livy's L4 (H-LIVY).
  - SMH2016 §2b(iv) used Thucydides' 431 BC and Agesilaus' 394 BC eclipses
    to limit ΔT [r1, from a WebFetch summary of the PMC text, *secondary*].
    These are R-THUC's T1 and R-XEN's X3.
  - Whether the *Almagest* lunar timings entered the fits is not settled.
    SMH2016's Table S4 and §4b have not been read (pre-freeze task, 12.1).
- **Moving the site primaries to "none"** weakens R-THUC and R-XEN in the
  primary run [lcr, Consequences].

**The negatives** (`negatives.json`) [neg; lcn]:

- 13 sets: 12 clean negatives, and the Iliad as a same-tradition comparison.
- 70 clue rows and 34 excluded rows.
- All 209 licence fragments match the cited rows, and no date leaks.
- I11(a), the contradictory AEN-TROY reading R-ii-literal, gives **zero
  survivors** at Troy among 1,683 conjunctions of 1250–1115 BC and 3,104 of
  1350–1100 BC. That holds by astronomy, not by logic [r1:
  check_i11a.py].

### 2.7 Predictions of earlier revisions that are now settled

| revision, prediction | status | numbers |
|---|---|---|
| v1 1–5 (T0) | largely implied by 2.2 | kept in section 8 as regression expectations, not counted |
| v1 18 (mixture P(total) 0.15–0.40; P(mag ≥ 0.9) ≥ 0.8) | **holds already** | mixture 0.304 (canon frame), 0.309 (pairing rule); P(smag ≥ 0.9) 0.928 (2.3) |
| v1 19 (1131 higher under every model; joint ≤ 0.05) | **fails as written** | the SMH2016 parabola gives 0.498 against 0.443; the joint 0.108 (SMH2016) and 0.052 (Addendum) exceed 0.05 [rev #17] |
| v1 20 (< 2% of dates flip) | sits on its threshold | about 1.9% [rev #17] |
| v1 21 (PC-S recall ≥ 0.99 at zero noise) | tautological as built | replaced by the two PC-S modes [rev #14] |
| v1 24 (NC4 zero survivors, NC5 never unique) | true by construction | moved to instrument check I11 [rev #15] |
| v2 P23 (R_anc's survivors include 1131 BC) | **fails as written** | v2's season bound [180°, 270°) excludes 30 Sep 1131 BC, when the Sun stood at 176.69° [r1 N7]. Restated with an ancient season definition (5.3), under which the known part moves to 2.8 |
| v2 P26 (per-model P(total) orderings and joint bounds, DE431 frame) | **known** in the canon frame | the 2.3 table [r1 N7]. Only the move to the DE431 frame (about 40 s) is new, and 5.6 recomputes it as a regression expectation |
| v2 P30 (at ν_real the B&M reading recovers ≤ 70% of spring truths) | **near-certain** | B&M's V ∧ M passes 5 of 41 accepted truths at zero noise [r1: check_lr_cap.py] |
| v2 P32 (rec_PCS ≥ 0.5) | **definitional** | about 0.68 (28/41) by the overlap of generator and searcher [r1 N2]. rec_PCS is removed from the gate |
| v2 P34 (strict_PCR = 4) | confirms a rough known check | a regression expectation (8) |
| v2 P36 (rec_ALM_BM < 6) | **known** under the frozen option rule | 2.6 |
| v2 P41, P42 (LR_real,lo < 30; no outcome 1) | **follow from the ceiling** | LR ≤ 1/P(A) ≈ 6.5 [r1 N1]. Withdrawn with the LR (5.7) |

### 2.8 Known from the recheck of revision 2, and from this revision

**The observation model's ceiling** [r1 N1; r1: check_lr_cap.py]:

- **The slot event A.** Over the 266 spring daylight new moons of
  −1499..−1000 at Ithaki (fixed C bounds, SMH2020 ΔT), A is defined on
  Day −5 and Day −34 (sequential count) as follows:
  - Venus is a visible morning star at AV 7°, which holds for **0.398** of
    the targets;
  - Mercury lies within 6 d of a morning rise-azimuth maximum, greatest
    western elongation or station, or is visible at AV 10°, which holds for
    **0.342** (event alone 0.241, visible alone 0.327).
- **The ceiling.** Both hold for **P(A) = 0.154** of the targets (binomial
  95%: 0.111–0.198). Hence LR ≤ 1/P(A) ≈ **6.5** (5.1–9.0). Over all 519
  spring conjunctions, P(A) = 0.148.
- **The components agree with the dossier.** Venus is a visible morning star
  on 43% of spring Day −5s [vis, table at l. 179]. With the dossier's
  stricter Mercury figure (17% within ±5 d of an event), P(A) ≈ 0.073 and
  the ceiling is about 14.
- **Among the 41 targets in A:**
  - B&M's V ∧ M (lead ≥ 90 min; \|Δ\| ≤ 1 d to the rise-azimuth maximum,
    approximated from declination) passes **5 of 41 = 0.12**;
  - 28 of 41 have a Mercury event within 6 d;
  - every one of the 5 targets that pass B&M's V and M satisfies A.
- **Consequence for the Bayes factor.** The Bayes factor that B&M's reading
  alone can give a target of T_A is at most about 41/5 ≈ 8 (5.7). That rests
  on r1's approximate M rule, so it is a rough figure.

**Pool sizes and attainable bounds** [me: `results/design-revision-r2/cp_bounds.py`,
`.out.txt`]:

- **Revision 2's pools.** Its core (−1748..−851, 898 years) holds about
  **478** spring daylight targets (r1 estimated about 480), and so about 74
  in T_A.
- **The floor.** With no target reached, the 95% upper bound on a G is
  3.69/n (the Fay–Feuer gamma interval and the Clopper–Pearson interval
  agree here, 5.3). For n = 74 that is **0.0499**, so a threshold of 0.05
  could be met only if not a single target were reached.
- **Revision 3's pools.** Its core (−1748..−51, 1,698 years, section 4.1)
  holds about **10,690** daylight conjunctions (T), **903** spring ones
  (T_C) and **139** in T_A (100–179 over P(A)'s interval). The floor for
  T_A is then **0.0265**.

**Other numbers already computed:**

- **The Sun's apparent longitude at four conjunctions** [r1:
  check_ranc_season.py]:
  - 16 Apr 1178 BC (10:09 UT): 14.28°;
  - 30 Sep 1131 BC (10:30 UT): **176.69°**;
  - 30 Oct 1207 BC (13:27 UT): 206.70°;
  - 12 Jan 1183 BC (07:46 UT): 282.20°.

  The autumnal equinox of −1130 fell on 3 Oct, 17:17 UT.
- **Arcturus' heliacal rising at Ithaki** (first morning on which Arcturus
  rises with the Sun at or below −AV; DE441, SMH2020) [me:
  `results/design-revision-r2/ranc_season.py`, `.out.txt`]:
  - in −1177: 9, 12 and 14 Sep at AV 8°, 10° and 12° (the dossier gives
    8–13 Sep [vis §3.3]);
  - in −1130: **10, 12 and 14 Sep**.

  30 Sep 1131 BC therefore lies 16–20 days after the vintage marker of
  Hesiod's farming calendar (*WD* 609–611) and 3 days before the astronomical autumn of
  Geminus. *Isagoge* 1.9 divides the year into four seasons at the
  equinoxes and solstices (the autumn clause sits in a lacuna), and 2.17
  says the seasons begin in the cardinal signs (local `geminus-grc.tsv`
  1.9.1, 2.17.1). It was total at Ithaki at canon ΔT, with the Sun
  at 51.6° (2.3).
- **I11(a)** holds at Troy (2.6).

**What the known numbers already imply for the verdict.** Nothing in this
list is a prediction, and the bench recomputes every item with its own code:

- **T0 = RE is expected.** 18 Mar 1189 BC passes N, C, V and M without the
  equinox (2.2), and revision 3 requires T0 = R for outcome 1 (5.3).
  **Outcome 1 is therefore not expected to hold.** That is a fact about the
  data, not about the rule: synthetic set S1 shows that the rule reaches it
  (9.5).
- **Q_BM holds** (2.6).
- **Gate 3b** retains the truth in 9 of 11 sets. Only narrowing is open.
- **The words' evidential ceiling** is about 6.5 for blind categorical
  readings, and 1 once those readings are conditioned on, because the record
  shows that they were formed with the target in view (5.7).

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
section 0, and prediction P2 checks that the T0b survivor set does not move
under it. The steps:

1. **Candidates.** Every geocentric conjunction in apparent ecliptic
   longitude whose UT+2 instant falls in the half-open window
   [−1249 Jan 1 00:00 UT+2, −1113 Jan 1 00:00 UT+2), i.e. through 24:00 UT+2
   on 31 Dec −1114, computed as
   `calendar.span_bounds((-1249,1,1), (-1114,12,31), offset_hours=2)`.
   UT = TT − 27,602.7 s. Expected count 1,683 [rev #22; R6].
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

   Pass if \|Δ\| ≤ 1.5 d for MWRA_vtx, B&M's integer tolerance of 1 day
   as a continuous one: a vertex lies within half a day of its discrete
   maximum [r1 N13]; ±1 d is reported beside it. Pass if \|Δ\| ≤ 1 for
   MWRA_int. Every maximum records its curvature (deg/d²) and its
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
| M tolerance | MWRA_vtx \|Δ\| ≤ 1.5 d (±1, ±2.5, ±3.5 reported); MWRA_int \|Δ\| ≤ 1 (2, 3 reported) | S2 colours [bm §5 M]; continuous equivalent [r1 N13] |
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
§References), visibility off (S2's table), MWRA_vtx at ±1.5 d. The whole grid is
reported. Expected (R5): RE in the primary cell, NR under E ≤ 4 Apr.

**Only R counts toward outcome 1** [r1 N6 fix 3]. RE is a reproduction that
holds only with the equinox clue, whose reading MacDonald fitted to the
eclipse (5.3). 18 Mar 1189 BC passes N, C, V and M (2.2), so T0 = RE is
expected, and outcome 1 with it is not expected (2.8).

---

## 4. Shared machinery

### 4.1 Spans and coverage

- **Background** B = −1999-01-01 to +200-12-31 (2,200 Julian years).
  - It starts with the first year of NASA's elements [acq §2.1]. Every
    ephemeris, element and star file needed is already on disk (DE441 and
    DE431 to +241, NASA elements to +300 [acq §1.1, §2.1]).
  - Revision 2's background ended at −600. Its conditioned target pool would
    then hold about 74 targets. With so few, the interval could fall below
    0.05 only if not one target were reached (2.8) [r1 N8]. Extending the
    background to +200 nearly doubles the pool.
  - **The cost is stationarity.** Precession moves the star season about 31
    days against the equinox over 2,200 years. P9 tests the rates, and 5.3
    reports G on each half of the core.
- **Data margins** −2060..+241, covering the 40-day clue offsets and the
  ±60-day Mercury searches.
- **Target core** −1748..−51. Targets must lie at least 251 years inside B
  so that every window of every width lies inside it. One core serves all
  widths, so gardens of different widths share their targets. The core
  contains 1312, 1178 and 1131 BC.
- **Controls.** PC-R windows fall within −856..+272 and ALM windows within
  −407..+277. DE441 and DE431 are extended to +300 before the controls run
  (11.1).
- **Per-site spans** are in `data/prereg/sites.json` [r1 N12]. Only Ithaki
  needs every column over the whole span. Each negative-control site needs
  the background, but only the columns its sets use. Each control site needs
  only the union of its 21 window positions.

### 4.2 Candidate pools and target pools (Ithaki unless a rule names another site)

**Candidate pools.**

- **P_all** holds every geocentric apparent-longitude conjunction, computed
  with DE431 in yearly chunks and SMH2020 ΔT for UT. Each candidate carries
  **one Day-0 date per clock**: `day0_jdn_ut2` (B&M's clock; F2 (a)) and
  `day0_jdn_lmt` (F2 (b), the negatives, R_anc) [r1 N12].
- **P_day** holds the conjunctions whose instant falls in daylight at the
  site (Sun's centre above −0.8333°). At Ithaca that is 50.9% of them [vis
  §4.2], and only these can give a visible solar eclipse.
- **P_spring** holds the conjunctions passing C_rel (4.5) on the sequential
  or the parallel count, with Day 0 the UT+2 date. The slots below use the
  same Day 0, so that the identity at the end of this section is exact.

**Target pools.** Section 5.3 says which pool each G uses, and why.

| pool | definition | size in the core (estimate, 2.8) |
|---|---|---|
| T | P_day ∩ core | about 10,690 |
| T_C | T ∩ P_spring | about 903 |
| T_A | the targets in T_C whose sky satisfies the Venus slot and the Mercury slot below, on either day count | about 139 (100–179) |

- **The Venus slot.** On Day −5 or Day −4, Venus rises before the Sun, with
  the Sun at or below −7° at Venus' rising (AV 7° [vis §1.2]).
- **The Mercury slot.** On Day −34 or Day −33, Mercury lies within 6.0 d
  (continuous) of a morning rise-azimuth maximum (vertex, 4.3), a greatest
  western elongation, or a station while west of the Sun. Alternatively, it
  is a visible morning object, with the Sun at or below −10° at Mercury's
  rising.

The slots are revision 2's PC-S generator slots, which the recheck measured
[r1 N1], with the parallel count added. The 6-day width is the slack of
Ptolemy's Mercury records (2.6). It defines what "Hermes is Mercury" means
categorically. It is not used to validate anything: gate 3b is calibrated
leave-one-set-out (6.4).

**One identity follows.** Every reading of the rule's B&M garden requires C,
a Venus lead of at least 90 min (which implies the Venus slot: at Ithaca's
latitude the Sun sinks at least about 0.15° a minute near the horizon, so a
90-min lead puts it below −13° when Venus rises [me]) and a morning Mercury
event within 3.5 d (which implies the Mercury slot). So no target
outside T_A is ever reached by it, and

  G(𝒢_BM*, T) = (n_A / n_T) · G(𝒢_BM*, T_A)

exactly. I9 checks this identity in the code, and I14 uses it as a
realisability constraint (9.4).

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
  (P9).

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
   criteria with C_rel and E_rel (4.5), MWRA_vtx at ±1.5 d, SMH2020 ΔT,
   site `ithaki`.
2. **Rate.** λ = survivors per century, with a Poisson 95% interval, for
   N ∧ C ∧ V ∧ M and for N ∧ C ∧ V ∧ M ∧ E (n = 3, 4, 5).
3. **Two comparisons with B&M** [rev #5]:
   - λ(N ∧ C ∧ V ∧ M ∧ E) against B&M's printed 0.048 per century: B&M as
     written (P5);
   - λ(N ∧ C ∧ V ∧ M) against B&M's own arithmetic redone at their stated
     ±1-day tolerance, 0.88 per century (P4).
4. **Stationarity.** λ per century for each of the 22 centuries of the
   background, under C_rel and E_rel and under the fixed Julian bounds
   (P9).
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
   nothing documents an eclipse-blind spring reading. The same reason applies
   to V, M and E, and 5.3 applies it to all four [r1 N6].
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
   new moons, by permutation (P11). Every analytic shortcut below (5.4, 5.7)
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
the options B&M themselves raised. Tier DOC adds options with a named
published proponent for this passage, or the standard published
operationalisation of what such a proponent says. Tier FULL adds the rest
[rev #7]. Day tolerances are continuous: a vertex or event instant is
compared with the stated day's instant. B&M's integer tolerance of n days is
equivalent to n + 0.5 continuous days, because a vertex lies within half a
day of its discrete maximum [r1 N13].

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
| F5 Mercury | event MWRA (vertex), GWE or morning station × tolerance 1.5, 2.5, 3.5 d (B&M's 1, 2, 3 integer days) × visibility (AV 10°) required or not: 18 options | BM | B&M name all three events and require visibility; S2 never applied it [B&M §References; bm §5 M; rev #23; r1 N13] |
| | event "any of the three"; tolerance 6 d (the slack of Ptolemy's Mercury records, 14/14 within 5.5 d [alm §4]); morning first visibility (AV 10°) at 1.5, 2.5, 3.5 or 6 d; none | DOC | B&M call the events close in time; the *Almagest* records; B&M's "heliacal rising 13 Mar" [bm §9]; Gainsford, and the absence of any ancient Hermes–Mercury link before Plato [txt §5.9] |
| F6 equinox | off | BM (rule gardens) | B&M listed E and did not apply it [B&M §References, §Intersecting] |
| | E_rel with n = 3, 4, 5 | BM (reported gardens only) | MacDonald's reading, formed with the target in view (below) |
| F7 window width | 136 years | BM | [B&M] |
| | 91 (Troy VIIa) and 251 (primary) years | DOC | [win §4, §9] |

**The conditioning rule** [r1 N6; rev #6]. The record shows that every
categorical reading of the clues B&M used was formed by a reader who knew
the target [unread §2.4, §9 item 3]:

| clue | categorical reading | first formed by | the alternative | how the rule gardens treat it |
|---|---|---|---|---|
| N | Day 0 is the conjunction | the scholia on 14.162 (ancient; blind) | — | no conditioning needed: every target is a new moon |
| C | the raft nights are in **spring** | MacDonald 1967, with the eclipse in view; before him every reading was autumn or winter | autumn; none | **conditioned** (T_A ⊂ T_C); 𝒢_DOC also holds options (e) and (f), and is conditioned too (below) |
| V | the herald star is **Venus**, a morning star | MacDonald, who checked Venus in the eclipse year | none (a dawn formula) | **conditioned** (Venus slot of T_A) |
| M | Hermes' flight is **Mercury** | B&M, who knew the target | none | **conditioned** (Mercury slot of T_A) |
| E | Poseidon's return marks the **equinox** | MacDonald, who fitted his timetable to the eclipse | none | **left out** of every rule garden (F6 = off), and T0 must reproduce without it (3.5) |

A target's agreement with a reading formed for it is not evidence.
Conditioning removes that agreement and keeps the evidence that remains:
whether B&M's *tolerances* (a 90-minute lead rather than any visible morning
star; a Mercury event within 1.5–3.5 d rather than within 6 d) single a
target out, as priced by B&M's own tolerance forks.

E is treated differently from C, V and M for two reasons:

- The text gives Poseidon's day and nothing else about the Sun, so E has no
  tolerance part that could survive conditioning.
- Conditioning on it (E_rel at n = 5) would leave about 28 targets
  (139 × about 0.2). No interval over so few targets could fall below 0.05
  (2.8).

Leaving E out treats the Odyssey and the null alike: the target loses the
uniqueness E gave it, and so does every random target. G with E-on readings
is reported in two forms: union-priced over T_A, and conditioned over
T_A ∩ E_rel(5). Revision 2's G over T_C (season only) is reported too, so G
appears under both conditionings [r1 N6 fix 2].

The rule applies the same pool, T_A, to 𝒢_DOC, although 𝒢_DOC also holds
options that price C, V and M by union ("none", autumn). A union prices only
the choice to include a reading. It does not price the invention of a
reading that fits, which is what the record documents. The DOC options
still widen the tolerance forks (F1, F1b, F2, F4 visible, F5 at 6 d, F7)
for targets in T_A.

**Garden sizes** [me: `cp_bounds.py`; revision 2's sizes are reproduced by
r1 §3].

| garden | F1 | F1b | F2 | F3 | F4 | F5 | F6 | F7 | readings | bits | eclipse-compatible |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 𝒢_BM* (rule) | 2 | 1 | 1 | 1 | 1 | 18 | 1 | 1 | **36** | 5.2 | 36 |
| 𝒢_DOC* (rule) | 4 | 3 | 3 | 3 | 3 | 37 | 1 | 3 | **35,964** | 15.1 | 11,988 |
| 𝒢_FULL* (reported) | 8 | 6 | 4 | 6 | 6 | 37 | 1 | 3 | **767,232** | 19.5 | 383,616 |
| 𝒢_BM, 𝒢_DOC, 𝒢_FULL with F6 (reported) | | | | | | | 4 | | 144; 143,856; 3,068,928 | 7.2; 17.1; 21.6 | 144; 47,952; 1,534,464 |

F5's 37 in DOC and FULL is 4 events × 4 tolerances × 2 visibility settings,
plus first visibility at 4 tolerances, plus none. **T0b's own reading (in
its C_rel form, visibility off, F6 off) is a member of 𝒢_BM*** [rev #23].
Only F2 (a) and (b) put the conjunction on Day 0, where Theoclymenus speaks
[chron §4.H].

Two readings are left out because they cannot change the result: Day 0 as a
20-day window, and N dropped. Their candidates are days, a superset of the
conjunction dates, so they add no reach for any New Moon target [v1 §3.4;
rev §1 confirms].

**The statistic: reach.** For a reading r, let S_r be its survivors over the
background, each mapped to its conjunction (under F2 (c) and (d) a candidate
is mapped back). A target t ∈ S_r is the unique survivor of a W-year window
[a, a + W) placed at a uniformly random start a with t inside, exactly when
the window misses the neighbouring survivors s₋ and s₊. That is,
a ∈ I_r(t) = (max(t − W, s₋), min(t, s₊ − W)]; if t ∉ S_r, I_r(t) is empty.
Over a garden 𝒢, **reach_W(t; 𝒢) = |∪_{r∈𝒢} I_r(t)| / W**. For gardens with
several widths, reach(t) = max over W of reach_W(t), a lower bound on the
union [v1 §3.4]. Under T0b with E off, reach_136(1178 BC) ≤ 0.081, and it is
0 if a survivor falls in −1176..−1052 [rev #24c; P12].

**G and its interval.** For a garden 𝒢, a pool P and widths W:

- **G(𝒢; P; W)** = the mean of reach(t; 𝒢) over the targets t ∈ P, with
  16 Apr −1177 excluded. G is the look-elsewhere-corrected p-value of a
  coincidence whose target was fixed first, as Schoch's was: the chance that
  a target of the pool, fixed in advance and unrelated to the text, is made
  the unique match by some reading of 𝒢 in a window placed at random around
  it.
- **The interval** [G_lo, G_hi] is the 95% gamma interval of Fay & Feuer
  (1997) for a weighted sum of counts [r1 N8 fix 2]. Each target counts
  1, weighted by reach/n, and the largest possible weight is 1/n. Let
  y = G, v = Σ (reach/n)² and w = 1/n. Then
  G_hi = ((v + w²)/(2(y + w))) · χ²_{0.975}(2(y + w)²/(v + w²)) and
  G_lo = (v/(2y)) · χ²_{0.025}(2y²/v), with G_lo = 0 when y = 0.
  - With no target reached, G_hi = 3.69/n.
  - When every nonzero reach is 1, the interval is the exact Poisson one.
  - Unlike a binomial bound on the share of targets reached, it does not
    treat a reach of 0.2 as 1.

  The formula is given from memory. The implementer checks it against the
  paper, and I9 checks its coverage by simulation.
- **Rule quantities.** Each comes with its pool size n and the number k of
  targets with reach > 0.

  | quantity | garden | pool | W | used for |
  |---|---|---|---|---|
  | **G_BM** | 𝒢_BM* | T_A | 136 | outcomes 1 and 2 |
  | **G_DOC** | 𝒢_DOC* | T_A | max over 91, 136, 251 | outcome 1 when Q_BM holds |
  | **G_BM,u** | 𝒢_BM* | T | 136 | outcome 4: the Odyssey's coincidence as B&M would present it, every reading treated as blind, compared with fiction's blind readings |

  G_BM,u = (n_A/n_T) G_BM exactly (4.2).
- **Reported beside, never in the rule:**
  - G over T_C (revision 2's season-only conditioning);
  - the E-on gardens over T_A and over T_A ∩ E_rel(5);
  - G_FULL*;
  - G_BM on each half of the core (stationarity);
  - **G_any**, the fraction of the pool with reach > 0. B&M's window was
    itself drawn from the tradition that chose the eclipse [win §6];
  - **G_X**, the h_tot-weighted mean reach over the eclipse new moons of T,
    with 16 Apr −1177 excluded, compared with G_BM,u (spring eclipses
    alone are too few). If eclipse new moons are reached at the rate of
    other new moons (P17), the eclipse adds nothing beyond its rarity.

**Reported:**

1. reach(16 Apr 1178 BC) under the T0b reading, 𝒢_BM*, 𝒢_DOC*, 𝒢_FULL* and
   the E-on gardens.
2. Every G of the list above, with k, n and the interval.
3. **The smallest fork set that reaches G ≥ 0.20 over T_A**, built by greedy
   addition to 𝒢_BM* of the option that raises G most. The sequence and each
   option's source are printed [rev #7].
4. The look-elsewhere factor G_BM / p_fix,unique, where p_fix,unique is the
   same quantity for the T0b reading alone.
5. **Alternative datings.** Every eclipse new moon with h_tot ≥ 0.1 at any
   Ionian site that some eclipse-compatible reading makes unique, with the
   readings that do it. Four are listed whatever the result:
   - 30 Sep 1131 BC, total at Ithaki at canon ΔT and inside B&M's window
     [rev V6];
   - 24 Jun 1312 BC, the Iliad date of Henriksson 2012 [unread §5];
   - 30 Oct 1207 BC, from Papamarinopoulos et al. 2012 [unread §4];
   - 12 Jan 1183 BC (−1182), Schoch's rejected annular eclipse [unread §3.1].
     Research-window's "1182 BC" for the same catalogue row is a slip
     [win §7.2].
6. Survivors per century for every reading, so the strictness of each
   garden is visible.

**R_anc, the ancient reading** [rev #18; r1 N9]. This pinned reading was
formed without knowledge of any computed eclipse, from the scholia,
Heraclitus and Plutarch:

- **Day 0** is the conjunction date (LMT at Ithaki): the scholia's ἕνη καὶ
  νέα on 14.162, and Heraclitus [txt §5.1].
- **Season.** The scholia read the season as "autumnal, and already towards
  winter" (17.24) and as winter (6.305, 14.458) [txt §5.6]. Greek sources
  divide the year two ways:
  - Hesiod's farming calendar marks the vintage by Arcturus' morning rising
    (*WD* 609–611) and the ploughing, as winter comes on, by the Pleiades'
    morning setting (*WD* 615–617). Its autumn runs from the first to the
    second, and its winter from the second;
  - Geminus divides the year at the equinoxes and solstices (*Isagoge*
    1.9, 2.17).

  The two divisions disagree. The primary reading therefore follows the rule
  the controls file applies when sources disagree: the weakest reading both
  allow [pcr §2]. Day 0 must fall **from Arcturus' heliacal rising (AV 10°,
  computed each year) to the spring equinox**, that is, in autumn or winter
  on either division. The alternatives are:
  - Geminus' autumn alone, [180°, 270°) of solar longitude (revision 2's
    bound, now sourced);
  - Hesiod's autumn alone, from Arcturus' heliacal rising to the Pleiades'
    morning setting;
  - Geminus' autumn and winter, [180°, 360°).
- **Eclipse.** Theoclymenus' vision is read as a solar eclipse on Day 0
  (Heraclitus; Plutarch, *De facie* 19 [crit §3.1]): h_06(u, ithaki) ≥ 0.5.
- **No planets and no stars**, because the scholia read 5.272 as
  slow-setting.

R_anc is run **with and without the eclipse clue** [r1 N9 fix 2]:

- **Without it**, the only clues are the conjunction and the season, so
  about six new moons a year survive. That version never has a unique
  survivor, so the ancient reading dates nothing without the eclipse. It is
  the only version whose "coincidence" could be compared with B&M's, and the
  comparison is empty by arithmetic.
- **With it**, R_anc is the ancient reading's own dating. Its survivors in
  each window, their h_tot, and whether one is unique are reported beside
  B&M's.

What is already known (2.8): 30 Sep 1131 BC passes the primary season (16–20
days after Arcturus' heliacal rising) and fails Geminus' autumn (3 days
early). 16 Apr 1178 BC fails every season option. R_anc is not in the
decision rule. The held-out predicates (section 7) are also run on its
survivors.

### 5.4 N4: random epics, the main negative

N3 holds the poem fixed and varies its reading. N4 holds the reading
machinery fixed and varies the poem. Random poems of the Odyssey's grammar
are the main negative of the bench [rev #15 fix 3]. They set the percentile
that outcomes 1 and 2 use.

**The grammar** (`data/prereg/epic_grammar.json`, as in revision 1, except
that season clues are relative to each year's sky):

- **Day 0 anchor:** conjunction, full moon, the 7th day of the month
  (Apollo's day in Hesiod, *WD* 770–771 [txt §5.3]), or none.
- **Season clue:** a pair from the archaic star list (Pleiades, Hyades,
  Orion, Sirius, Arcturus [txt §5.8]). Either both stars are ≥ 2° at the end
  of evening or morning nautical twilight on one night or on a 17-night
  span, or one star's heliacal rising or setting falls within ±k days.
- **Planet clue:** Venus, Mercury, Mars, Jupiter or Saturn, in one of three
  forms:
  - a morning object with rise lead ≥ 60/90/120 min;
  - an evening object with set lag ≥ 60/90/120 min;
  - within ±1.5–3.5 days of a turning point (rise- or set-azimuth extremum,
    greatest elongation, station, opposition) or of first or last visibility
    (Ptolemy's AV: Venus 5°, Mercury 10°, Jupiter 10°, Mars 11.5°, Saturn
    11° [vis §1.2]).
- **Offsets.** Variant A ("B&M-shaped") puts a season clue on a span
  starting between −29 and −27, and two planet clues at −5 and −34, around a
  conjunction anchor; the clue types are drawn at random. Variant B draws
  the anchor, two or three sky clues and their offsets (−40 to −1) freely.

10,000 epics per variant (seed in `seeds.json`), site `ithaki`, evaluated
over the background.

**Per epic:**

- p_c, its primary reading's per-candidate pass rate (its specificity);
- the survivor count in a 136-year window at a random position, and
  P(unique);
- **T_best ≥ T_obs.** Each date is scored by −log10 of the product of the
  per-clue base rates at the observed tightness (P(Venus lead ≥ observed),
  P(\|Δ\| ≤ observed), …). T_obs is that score for 1178 BC under the B&M
  reading. The statistic is P(T_best ≥ T_obs) over epics.

**The specificity stratum.** Epics whose p_c lies within a factor 2 of the
Odyssey's (B&M reading) form the stratum. If fewer than 200 epics fall in
it, the factor widens to 4 and the report says so.

**Epic gardens.** Each stratum epic gets a garden built with the same fork
types and multiplicities as the Odyssey's rule garden:

- the BM-tier epic garden has the two-offset day-count fork, and 3
  turning-point events × 3 tolerances × 2 visibility settings for one planet
  clue: 36 readings when the epic has those slots, as 𝒢_BM* has;
- the DOC-tier epic garden adds the DOC fork types.

**The calibrated percentile (target first).** Schoch's target was fixed
before any reading. For each stratum epic, r_e = reach_136(16 Apr −1177;
the epic's garden): the chance that this poem, read with the same freedom,
makes Schoch's eclipse new moon the unique match of a window placed at
random around it. r_Ody is the same for the Odyssey under 𝒢_BM*.

- **Conditioning, as in 5.3.** Only epics whose categorical slots hold at
  Schoch's target enter: the season clue holds, and each planet clue's body
  is present in the stated role (a visible morning or evening object, or
  within 6 d of the named kind of event).
- **pct_N4** = the fraction of entering epics with r_e ≥ r_Ody, ties
  counting against the Odyssey. Its interval [pct_N4,lo, pct_N4,hi] is the
  exact Clopper–Pearson 95% interval over the n_stratum entering epics.
  pct_N4 is a tail fraction, the Odyssey's percentile among random poems of
  the same specificity [rev #1 fix 2]. It is not a probability of the same
  kind as G [r1 N10].
- **Ē_N4** = the mean of r_e over the entering epics. This is the analogue
  of G with the poem varied rather than the target. P21 compares it with
  G_BM, and it never enters the rule [r1 N10 fix].

**The eclipse-match strength (survivors first; reported).** For a text with
garden 𝒢 in a window, M = the maximum, over eclipse-compatible readings r,
of h_tot(u_r, ithaki), where u_r is r's unique survivor in the window (0 if
there is none). For each stratum epic, M_e is computed in a window at a
random position, and **p_N4** = the fraction with M_e ≥ M_Ody. If fewer than
20 epics reach it, p_N4 is computed analytically instead: the mean, over
stratum epics, of K_e × p_e(M_Ody), where K_e is the number of distinct
unique survivors across the epic's eclipse-compatible readings. That relies
on N2's independence check [rev #16 fix 4]. The direct count is reported
beside it, with bootstrap intervals.

p_N4 credits the eclipse's rarity. That rarity would be evidence only if the
readings had been formed blind to the eclipse, and the record says they were
not (1.1). p_N4 is reported and enters no rule. Revision 2's ratio LR_sf is
withdrawn with the other likelihood ratios (5.7).

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
   probabilities under a common ΔT offset, per model. Revision 1's failed
   prediction 19 is restated per model [rev #17 fix 2]. Its canon-frame
   values are known (2.3), so the DE431-frame recomputation is regression
   expectation R7, not a prediction [r1 N7].
5. **ΔT and the clue tests.** Count the candidates whose civil conjunction
   date flips between 27,602.7 s and each model at ±1σ (known: about 1.9% for
   SMH2020 + 1σ), and rerun T0b at SMH2020 ± 1σ with DE431 conjunctions
   (P2).
6. **B&M's own value** is reported as uninterpretable (2.3) and is never
   converted into another frame.

### 5.7 Evidential weight: an identity, a ceiling and a Bayes factor

Revision 2's bottom line was a likelihood ratio, LR = R_obs/G. In it,
R_obs was the mean reach of a truth whose sky an observer had described.
The recheck showed that it can never pass about 6.5, whatever the data
[r1 N1]. The argument has four steps.

1. With the poem held fixed, every truth accepted in PC-S science mode
   carries the Odyssey's clue set at the Odyssey's offsets.
2. So the survivor sets are the Odyssey's, and R_obs and G are two
   weightings of one reach function: R_obs = E[reach · 1_A] / P(A) and
   G = E[reach], both over T_C.
3. Hence

   **LR_slot = P_w(A) / P(A) ≤ 1 / P(A)**, where P_w is the reach-weighted
   probability.
4. P(A) is 0.154, so the ceiling is about 6.5 (5.1–9.0) (2.8).

**The identity is a finding, not a bug.** An observer who records that a
bright star heralded the dawn and that Hermes flew can raise the odds of a
target by at most the inverse of how often a sky has those features. The
precision that B&M's criteria carry (90 minutes, ±1 day) belongs to the
reader, not to the text. Two consequences follow:

- under the conditioning of 5.3, where the categorical readings were formed
  with the target in view, LR_slot over T_A is identically 1;
- any rule threshold on such a ratio is decided by the observation model,
  not by the Odyssey.

**So no likelihood ratio enters the decision rule** [r1 N1 fix 2(a)].
Outcome 1 rests on G over T_A, on pct_N4 and on T0. Outcome 2 rests on G
and pct_N4. Revision 2's R_obs/G, its curve over noise and LR_sf are
withdrawn as rule inputs. What is reported, as standing findings beside the
verdict:

1. **The ceiling.** P(A), with its interval, and 1/P(A), recomputed on the
   bench's sky tables over T_C. **LR_slot(ν)** is also given as a curve over
   the noise grid of 6.2. Its numerator is computed exactly, not by
   sampling [r1 N8 fix 1]:

   R_obs(ν) = Σ_t Σ_δ reach(t) · 1[A(t, δ)] · w(δ) / Σ_t Σ_δ 1[A(t, δ)] · w(δ),

   - t runs over T_C;
   - δ runs over every vector of slot-day offsets in [−j, j], with weight
     w(δ) uniform, and with the Mercury displacement s_M applied to the slot
     tolerance;
   - reach is taken from the same garden and the same W as the denominator
     [r1 N8 fix 3].

   No new survivor sets are needed, because the poem is fixed.
2. **The Bayes factor of the residual fit under B&M's own hypothesis.**
   H1_BM says that the poet encoded the phenomena of some reading r of
   𝒢_BM*, each reading equally likely (π_r = 1/36). H0 says the clues are
   unrelated to the target. Under H1_BM, with probability ρ_r the target's
   sky passes reading r. Otherwise it is a sky drawn from T_A that fails r.
   For the target t_S = 16 Apr −1177,

   BF_BM(ρ) = Σ_r π_r [ ρ_r · 1{t_S passes r} / p_r + (1 − ρ_r) · 1{t_S fails r} / (1 − p_r) ],

   where p_r = (number of targets of T_A \ {t_S} passing r + 1)/(n_A + 1).
   This is the pass rate of reading r as a filter (survival, not uniqueness),
   with the add-one rule so that no p_r is 0. BF_BM is exact for the
   whole pass/fail vector of t_S under that model.
   - It is reported at ρ_r = 1, the model most favourable to B&M, and at
     ρ_r = the PC-S science-mode recall of r at ν_real (6.2).
   - Its ceiling is BF_max = Σ_r π_r/p_r, reached when t_S passes every
     reading.
   - From the recheck's numbers, B&M's reading alone passes about 5 of 41
     targets of T_A, so it can contribute at most about 8 (2.8). That figure
     is rough.
3. **The *Almagest* calibration** [r1 N1 fix 4]. The same estimator is
   applied to each counted *Almagest* set:
   - it gives the BF of the set's true date under the set's own garden (its
     fork options, at regime-SL tolerances);
   - p_r is the share of the civil days in the set's 21 window positions
     that pass reading r.

   This shows what truly observed records, whose statements carry their own
   precision, earn under the machinery that scores the Odyssey.
4. **The blind version of the words.** The words' ceiling if the categorical
   readings had been formed blind is 1/P(A), about 6.5. The bench prints it
   beside BF_BM as "what the words could carry if C, V and M had been
   proposed without the target".

The bench reports these figures, together with G, p_fix and the bit budget.
It does not multiply any of them by a prior.

---

## 6. Controls

All clue sets, readings, windows, sites, seeds, regimes and thresholds for
the controls are in `data/prereg/` and are frozen with this document
(section 12) before any control is computed. Truth files are read only by
`odybench/harness.py`, to place windows, to score and to run the exposure
audit (6.3.4). The searcher never reads them, and a static test enforces
this (I13).

### 6.1 Instrument checks

Each check compares a code path with something that does not share its code
[rev #13]. **INSTR** holds when I1, I2, I2b and I4–I14 all pass. I3 is a
calibration with no pass criterion, so it is reported and is not part of
INSTR [r1 N15]. `verdict.py` refuses to run unless INSTR holds.

A check marked "post-freeze" runs first after the freeze. The outputs it
guards are not opened until it passes, and a fix it forces is a dated
amendment (section 12).

| # | what is checked | compared against | pass | when |
|---|---|---|---|---|
| I1 | ephemeris | Horizons; `validate_ephem.py`; `test_ephem.py`; `validate_coverage.py` | 55/55, 10/10, all coverage checks [acq §1.3] | done; rerun pre-freeze |
| I2 | solar-eclipse local circumstances, `eclipses.py` (Python port of NASA's JavaScript, from `results/research-critiques/eclipse_local.py`) | (a) NASA's own `program.js` run in Node: `data/jsex/sites/*.jsonl`, 5 sites × 5,486 eclipses; (b) the review's independent Besselian solver `results/critique-design/check_bessel.py` [rev #13 fix 6] | (a) smag within 0.0005, time of maximum within 0.002 h, Sun altitude within 0.05°, central flag identical; (b) totality windows for 1178, 1131, 1312 and 1183 BC within 5 s; (c) `deltat_mix.py`: P(total) for 1178 and 1131 BC per model and for the mixture on NASA's elements, against the 2.3 table and a 10⁶-draw Monte Carlo, within 0.005 | pre-freeze |
| I2b | language-to-magnitude: local smag for the dated eclipses of [ctl §3] | the values printed in [ctl §3], moved to the truth-side file `data/prereg/i2b_reference.json` | **both sides named** [r1 N15]. The bench side is `eclipses.local` on NASA's elements at the element row's canon ΔT (ṅ −25.858). The reference side is Horizons DE441 geometry at NASA's catalogue ΔT, applied by the longitude-shift equivalence [ctl §2.2], which mixes frames by the DE441 − canon offset (about 90 s at −430 [acq §1.3; me: 0.00335″ T³]). Pass: smag within 0.02, or within the change produced by ±100 s of ΔT if that is larger; above 0.95, the central flag agrees | pre-freeze, after the re-draft of 6.3.4 |
| I3 | Hesiod's star calendar at 701 BC, 38.37°N | Hesiod's own numbers | **a calibration, not a validation, and not in INSTR** [rev #20; r1 N15]. The Pleiades' AV is set so that they are hidden 40 days (*WD* 385–386); "Arcturus ≥ 5° at nautical dusk" is read off *WD* 564–567. The phases are validated by I6(c) | pre-freeze |
| I4 | lunar eclipses, `lunar.py` | NASA LEcat5 rows: every lunar eclipse in the PC-R and ALM truth centuries, and 300 drawn at random from −1999..+300 | type identical; umag and pmag within 0.02; greatest eclipse within 3 min after removing the ΔT difference | pre-freeze |
| I5 | rise, set and transit, `sky.py` | (a) JPL Horizons rise/transit/set output for 1,000 random events (Sun, Moon, Venus, Mercury, Jupiter, Sirius, Arcturus; Ithaki, Alexandria, Troy; −1999..+300; same h0, airless); (b) the dense-grid-plus-bisection rise finder of `results/critique-design/check_mwra.py`, on 2,000 events | (a) within 0.5 min after removing the documented sidereal-time convention difference (5 s at −1999 [acq §1.3]); (b) within 0.1 s | pre-freeze |
| I6 | derived events, `events.py` | (a) the event lists of `results/bm2008-reconcile/check_mwra.py` (rise-azimuth maxima and minima, stations, GWE, inferior conjunction) for all 152 S2 years; (b) the low-precision Standish-element code `results/bm2008-b-checks/ephem.py`, 500 random stations and greatest elongations; (c) heliacal star phases and B&M's spring limits from `docs/research_visibility_calc.py` (its own spherical astronomy and Meeus' solar theory) at −1177 and −700; Arcturus' heliacal rising at −1177 and −1130 against `results/design-revision-r2/ranc_season.py` | (a) same UT+2 civil date in ≥ 150 of 152, vertex instants within 0.05 d; (b) within 1 d; (c) within 1 d | pre-freeze |
| I7 | B&M's reading through `clues.py`, `readings.py` and `search.py` | `tests/bm_reference.py`, a minimal second implementation written by a different agent from section 3.2's text alone, using only `ephem.altaz` and its own rise bisection [rev #13 fix 4] | identical pass flags (N, C, V, M, E and every T0 grid cell) for every candidate in 1250–1115 BC and in 300 random background years | post-freeze, before any T0 output is read |
| I8 | calendar | `tests/test_calendar.py` | 11/11 [acq §4] | done |
| I9 | reach, G and the pools | (a) a brute-force implementation that slides windows in 0.01-year steps, on 10,000 random synthetic survivor sets; (b) the coverage of the G interval of 5.3, on 10,000 synthetic reach vectors drawn at n = 100, 139 and 903 with true G from 0.001 to 0.3; (c) the identity G(𝒢_BM*, T) = (n_A/n_T) G(𝒢_BM*, T_A) on the real tables | (a) reach equal within 0.0002; (b) coverage of G_hi ≥ 0.95 and of G_lo ≥ 0.95 at every cell; (c) exact to float rounding | pre-freeze (c: post-freeze, first) |
| I10 | PC-S instrument mode (6.2) | descriptions generated by an independent code path | recall 1.000 | post-freeze, before PC-S science outputs are read |
| I10b | the exact R_obs of 5.7 | R_obs simulated end-to-end in PC-S science mode (generator and searcher, 2,000 truths per noise cell) | agreement within the simulation's 95% interval in every noise cell | post-freeze |
| I11 | plumbing negatives (revision 1's NC4 and NC5 [rev #15 fix 4]) | (a) AEN-TROY's pinned R-ii-literal reading, conjunction on Day 0 with the Moon up after nightfall, which contradicts itself [neg §3.1]; (b) a synthetic set with Day 0 a conjunction and the Moon above the horizon at local midnight; (c) Hesiod's star calendar (*WD* 383–385, 564–567, 609–611, 615–621) as event clues around an arbitrary Day 0 | (a), (b) zero survivors in every window (a is known to hold at Troy in two windows, 2.6); (c) no unique survivor in any 136-year window | post-freeze |
| I12 | first-crescent evening | the Yallop implementation in `docs/research_visibility_calc.py`, 500 lunations | same evening in ≥ 495 | pre-freeze |
| I13 | prereg I/O | (a) every licence string present in its cited row: the licence checkers' dump scripts are rerun, comparing raw characters without Unicode normalisation, because the Ptolemy export mixes tonos and oxia and prints the half-sign as the literal "U+2220" [lca next-stage item 7; pcr §5]; (b) every fork option of every row translates to a canonical predicate (10.3), with exactly one primary per controls row; (c) no module but `harness.py` and `tools/build_truth_index.py` opens a `*_truth*` path or contains the Nabonassar epoch; (d) `operational_map.json` is reviewed by a second agent; (e) the re-draft brief of 6.3.4 contains no statement, option name or justification string of `controls_real.json`, and exactly the five briefed rows; (f) `almagest_regimes.json` and `deltat_circular.json` parse, and every value they name exists in the clue files | all pass | pre-freeze |
| I14 | the decision rule | (a) the synthetic input sets of 9.5; (b) the structural constraints of 9.4 | (a) each returns its stated labels and qualifiers; (b) every synthetic set satisfies every structural constraint, so that what is proved reachable is an outcome and not a code branch [r1 N1 fix 3] | pre-freeze |

Revision 1's NC4 (the Hymn to Hermes) is dropped: it misread *h.Herm.* 141,
where παννύχιος closes Hermes' clause [rev #15].

### 6.2 PC-S: synthetic Odyssey-shaped clue sets

Revision 1's PC-S generated its clue sets with the same code it searched
with, and with a different grammar, so its "recall ≥ 0.99 or it is a bug"
was either built to fail or tautological [rev #14]. Revision 2 split it into
two modes. It also let one science-mode number, rec_PCS, into gate 3b. The
recheck showed that number to be definitional (about 0.68, because generator
and searcher share slot rules) [r1 N2], so **PC-S no longer enters any gate
or rule.**

**Truth pools** (seeded):

- (i) 2,000 daylight conjunctions drawn from T;
- (ii) every conjunction with h_tot ≥ 0.1 at any Ionian site;
- (iii) the targets of T_A.

**Instrument mode (I10).**

- **Generator.** Generator and searcher share B&M's grammar. For 200 truths
  from pool (i), the generator computes each truth's statements by an
  independent path: the Standish low-precision planetary code of
  `results/bm2008-b-checks/`, with its own rise bisection, for all 200, and
  Horizons for a 50-truth subsample.
- **Margins.** Statements are emitted with margins that hold under either
  ephemeris:
  - the lead threshold is the true lead minus 5 min, rounded down to 5 min;
  - the Mercury tolerance is \|Δ\| + 1 d, rounded up;
  - a season statement is made only if the truth lies at least 2 d inside
    its C_rel bounds.
- **Search.** The searcher is the bench's machinery with those parameters,
  on a window around the truth.
- **Pass: recall = 1.000.** A miss is a shared-code or conversion bug, found
  before any science number is read.

**Science mode: the noise study.** For each truth of pool (iii) and each
cell of the noise grid ν:

- **The noise grid.** Offset jitter j ∈ {0, 1, 2, 3} days applies
  independently to every clue offset. A displacement s_M ∈ {0, 3, 6} days
  moves Mercury's turning point from the stated day. There is no Venus
  slack: the *Almagest*'s 16–21-day Venus slack was measured on
  greatest-elongation records, while B&M's Venus clue is a rise-lead
  threshold that every *Almagest* Venus morning record passes with a large
  margin [alm §0 item 7, §5 item 3]. ν_real = (j = 1, s_M = 3).
- **The generator emits B&M-event statements** of the truth's own sky:
  - the Venus lead, rounded down to 5 min;
  - the nearest morning Mercury event, with its kind and offset;
  - the season class of the raft nights.

  All are stated at the stated offsets plus the noise.
- **The searcher applies every reading of 𝒢_BM*** and the DOC tolerance forks.

Recorded:

- recall and P(unique) of each reading, as curves over ν;
- **ρ_r(ν)**, the recall of reading r among the truths whose zero-noise sky
  passes r. It enters only BF_BM (5.7);
- the decay of reach and recall as the typical-number jitter grows from 0 to
  ±3 d [rev #8 fix 2–3];
- the generator's description of each truth's sky, to show which readings
  succeed and why.

There is no "bug" threshold in science mode. I10b checks the end-to-end
simulation of R_obs against its exact reweighting (5.7).

### 6.3 PC-R: real eclipse records with independently known dates (gate 3a)

**The clue file** is `data/prereg/controls_real.json` exactly as licensed
(SHA-256 `135fba67…83f8` [lcr]). The searcher reads only its operational
fields. Re-drafted rows are used only to measure exposure (6.3.4). Nine
sets:

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

The harness reads the truth through `data/prereg/truth_index.json`, which
`tools/build_truth_index.py` builds from the two truth files. It places a
136-year window with the anchor event at a uniformly random position (seed
per set). It passes the searcher only the clue set, the window bounds and
the event catalogues.

- **Candidates** are every event of the anchor's kind in the window: solar
  eclipses from NASA's elements, and lunar eclipses (umbral and penumbral)
  from `lunar.py`.
- **Linked events** are found through the interval rows: exact night counts,
  war-years ± tolerance, year headings 1–3. For each anchor candidate, the
  linked event that fails fewest rows is taken. Unlinked events (R-XEN's X3,
  the H-LIVY notices) are separate searches, reported and not counted.
- **Calendars** follow the file's conventions:
  - Egyptian dates have a free epoch (intervals only);
  - Roman dates have a free offset (primary), with ±90 d and "naive" as
    reported alternatives that are never readings of the text;
  - Attic months go through the modern reconstruction with ±1 lunation. This
    is the one primary that rests on a calendar outside the text [lcr
    flagged item 1].
- **Sites**: a point; a box (the row passes if some site in the box
  satisfies it); a disc; or none. "None" means some site on Earth: for solar
  eclipses a 1° grid refined near the best point, and for lunar eclipses the
  Moon above the horizon somewhere.
- **ΔT**: the four-model mixture (6.3.3).

#### 6.3.2 Scoring and the gate

**Scoring** [pcr §5 problem 1; truth-file note]. For a reading, f(c) is the
number of clue rows that candidate c fails. Rows without options are
structural: they define the events and dates.

- **Strict survivors** S₀ = {c : f(c) = 0}: B&M's all-must-pass rule.
- **Best-fit set** B = {c : f(c) = min f}: the dates the record points to,
  allowing for errors in the record.
- **Seen** := the truth is in B, and \|B\| ≤ 0.05 × N_cand, where N_cand is
  the number of candidates in the window. The method keeps the true date
  while narrowing the window at least 20-fold (4.3 bits). Uniqueness is not
  required, because a weak record cannot be unique however good the method
  is. The gate asks whether the method loses the truth, and that is the
  failure "cannot see" names.
- **Resolution** := the number of clusters in B, where candidates within 3
  days of each other count as one cluster (this matters only for day-unit
  candidates in 6.4). **Unique** := one cluster.
- **Strict recall** := f(truth) = 0.

The **primary run** puts every row at its primary option. Also reported for
every set:

- f(truth), \|S₀\|, \|B\| and the truth's rank;
- the same with each row moved, one at a time, to each alternative;
- the fraction of readings that make the truth the unique strict survivor,
  over all fork combinations (sampled to 10,000 where there are more);
- as a sensitivity, the fraction of twenty further window positions per set
  in which the set is seen.

**The gate.** seen_PCR is the number of the 7 counted sets seen in the
primary run, and strict_PCR the number with strict recall.

- **3a fires if seen_PCR < 4** (fewer than half, rounded up).
- **Q_strict holds if strict_PCR < 4.**

The best-fit rule was chosen after the drafter's post-freeze check had
shown that the true dates fail some primary readings under a rough lunar
model (2.6). That choice is therefore not blind, and the strict count is
always reported beside it as Q_strict.

#### 6.3.3 ΔT for the controls, and the controls that helped fit it

**Every ΔT-dependent row is scored under the four-model mixture** of section
0 [r1 N4 fix 1]. This applies to solar smag, the LAT of maximum, the
contacts and the Sun's altitude, and to lunar contacts, seasonal hours and
the Moon's altitude.

- **Frames.** Solar rows use NASA's elements in the canon frame, each
  model's value converted to it. Lunar rows use DE431, each model converted
  to the DE431 frame.
- **Pass rule.** A row passes for a candidate if
  P_mix(row passes) ≥ 0.5. The probability is integrated over a 41-point
  ΔT grid spanning ±4σ of each model, weighting each model's Gaussian
  equally.
- **Mapping of the X classes.** The controls file's "X3 ≥ 0.95" and
  "X4 ≥ 0.60" become P_mix(smag ≥ 0.95) ≥ 0.5 and P_mix(smag ≥ 0.60 with
  the Sun ≥ 10° at maximum) ≥ 0.5 at the row's site rule (10.3).
- **Sensitivities.** Reported at thresholds of 0.05 and 0.95.

**Circular controls** [r1 N4 fix 2–4]. Some control eclipses entered the
data that fitted the ΔT models (2.6):

- R-DIOD (−309, Table S10 v2020);
- H-LIVY's L4 (−187, same table);
- R-THUC's T1 (431 BC) and R-XEN's X3 (394 BC), per SMH2016 §2b(iv)
  (*secondary*).

**A pre-freeze task** reads SMH2016's Table S4 and §4b and the 2020
Addendum's tables. It lists every control eclipse used in any fit, and
whether the *Almagest* timings are among them, in
`data/prereg/deltat_circular.json` with page locators (12.1).

**seen_PCR,noncirc** is the gate count with each circular set's ΔT-dependent
rows rescored under the mixture with every model's σ multiplied by 3. A
model fitted to a record cannot then constrain that record much.

- **Q_ΔT holds** if seen_PCR,noncirc falls on the other side of 4 from
  seen_PCR.
- Gate 3a is also reported with the circular sets removed, the threshold
  then being half the remaining counted sets, rounded up. That count is
  reported only.

The S10 interval for −309 is 3,860 s wide, so R-DIOD's pass is probably
robust. Q_ΔT tests that rather than assuming it.

#### 6.3.4 The drafter's exposure

The drafter had seen computed answers and flags three primaries as possibly
steered: T1-DARK, D-ECL and the ±1 h tolerance in L4-DARK [pcr §1]. The
recheck adds T2-SEASON, whose primary alone admits the truth, and
T-INT-12's ±0.5-year tolerance [r1 N5]. The gate uses `controls_real.json`
exactly as licensed. The exposure is measured beside the gate, two ways,
rather than edited away.

1. **An unexposed re-draft of the five rows** [r1 N5 fix 1; N16].
   - **The brief.** `tools/make_redraft_brief.py` (written by A3, who does
     not read truth files) writes `data/prereg/pcr_redraft_brief.json`. It
     holds:
     - the file-level conventions and policies of `controls_real.json`;
     - for each of T1-DARK, T2-SEASON, T-INT-12, D-ECL and L4-DARK, its set,
       its feature kind and its cited text rows, in full.

     It holds no statement, option, justification, note or licence-check
     field. I13(e) checks this.
   - **The re-drafter.** An agent that has read nothing else in the
     repository (no `DESIGN.md`, `docs/`, `results/`, `data/ref*`, and no
     other `data/prereg/` file) drafts the five rows from the brief alone,
     into `data/prereg/pcr_redraft.json`.
   - **seen_PCR,redraft** is the gate count with the re-drafted primaries in
     place of the drafter's.
2. **A sibling-convention audit** [r1 N5 fix 2–3]. It runs post-freeze, in
   `controls.py`, because it reads the truth.
   - Rows of the counted sets are grouped by feature kind (season, site,
     darkness or magnitude, time, interval tolerance) and by operational
     type.
   - For every row whose primary passes the truth, each sibling's primary
     parameters are transplanted into the row wherever the operational keys
     match. An example is T1-SEASON's [0°, 180°] into T2-SEASON.
   - Every row that some sibling convention makes fail is listed in
     `results/pcr/exposure_audit.json`.
   - **seen_PCR,sibling** is the gate count with each listed row at its
     failing sibling convention, all at once.

**Q_exposure holds** if seen_PCR,redraft or seen_PCR,sibling falls on the
other side of 4 from seen_PCR.

**What this controls, and what it does not.** It controls exposure to
files. It does not remove a language-model drafter's background knowledge
of famous dates (the eclipse of 424 BC is among the best known), and no
re-draft by such an agent can [r1 N5 fix 4]. As the recheck noted, a re-draft
of L4-DARK cannot move the gate, because H-LIVY is not counted. R-THUC is
expected unseen in any case, because its site primaries are "none". So
Q_exposure turns in practice on D-ECL and on what the audit finds.

#### 6.3.5 Decisions on the points the licence check left open

- **Unstated sites stay "none" in the primary run** [lcr Consequences]. The
  Odyssey's observer is placed by its narrative (Theoclymenus in Odysseus'
  hall), so the asymmetry with Thucydides 2.28 is real. A rule that "a
  historian's undated notice places its observer in the region of the
  narrative" would be the inference the file's policy 2 excludes. The box
  and point options are reported as the first alternatives, so the cost of
  the rule is visible.
- **IV.6.14 is counted once.** It is H2 of R-PTOL-ALEX (gate 3a), so ALM-C,
  which contains it, is excluded from gate 3b [alm §3].
- **R-PTOL-CHAIN** uses IV.7.1, the chapter after IV.6. It is reported and
  not counted, so the gate does not depend on that choice [pcr problems].
- **"naive" Roman options** are sensitivity runs only, and are never
  reported as readings [lcr flagged item 2].
- **Pliny's "apud Arbilam"** may name the battle rather than the site, so
  the Tigris-camp alternative is reported [lcr flagged item 4].
- **H-LIVY has no year links** between its notices, so each is searched
  alone [pcr §3].

### 6.4 The *Almagest* control: real records of B&M's own clue types (gate 3b)

B&M's search uses no eclipse. Its clues are a lunar phase, a star season, a
morning star and a Mercury turning point, and revision 1's "method can see"
gate contained none of these [rev #3].

**The clue file** is `data/prereg/controls_almagest.json` as licence-checked
[lca]. It holds 12 sets of dated records: Mercury and Venus elongations,
planet–star and planet–Moon relations, lunar phases, a lunar eclipse and an
equinox. The day intervals come from Ptolemy's own Egyptian dates, and the
date words themselves are withheld.

**Counted sets** are ALM-A, B and D–L (11). ALM-C is reported only (6.3.5).

**Windows** are 136 years, B&M's width. The harness draws a uniformly random
position for the anchor record's true date (seed per set), as in 6.3.1, and
twenty further positions are a sensitivity. The truth file
`controls_almagest_truth.json` is read only through `truth_index.json`.

**Candidates** are every civil day in the window as Day 0 (LMT at the
default site), with each row at its stated day offset. Each row is evaluated
at the drafter's instant convention: "evening" and "dawn" are the moments
the Sun is 8° below the horizon, and stated hours are local apparent time
[alm §1.5]. The convention moves continuous offsets by about ±0.1 d. The
two textual cruxes (A.6 and H.3) run at their primary, as printed, and the
emended intervals are reported. ΔT is the mixture, as in 6.3.3.

**The two Ptolemy files treat Egyptian dates differently.** This file
withholds them, while `controls_real.json` carries them with a free epoch
[alm §3; pcr §2]. Both are kept. With the epoch free, an Egyptian date fixes
only intervals, so the two are equivalent for the searcher, provided that
no bench code supplies the Nabonassar epoch (JD 1448638). I13 checks
statically that the number appears only in the truth files and the harness.
The `ref` of every *Almagest* row points at a text row that contains the
withheld date, so the searcher reads only the operational fields and never
the text at `ref` [lca item 6].

**Default site.** Horizon-dependent rows are evaluated at Alexandria,
31.20°N 29.92°E. That is the observing place Ptolemy names for his own
records (4.6.13, 9.10.3, 11.2.2). The *Almagest* also names Babylon, for the
Babylonian eclipses of IV.6.3 [r1 N17], but those are in R-PTOL-BAB, not in
the B&M-type sets. For sets whose rows leave the observer unstated the site
is an inference, flagged as such [lca item 5]. Babylon is a sensitivity for
ALM-K.

**The B&M-type projection.** The gate uses only rows of B&M's kinds:

- interval rows;
- moon-phase rows, phase-class options only;
- planet rows about greatest elongation, before or after greatest
  elongation, visibility, rise lead and the rising-azimuth proxy;
- the equinox row.

Star rows, planet–star and planet–Moon positional options, oppositions and
the eclipse row are set to none, because they are not in B&M's grammar. The
full primary run is reported beside.

**Two regimes, frozen in `data/prereg/almagest_regimes.json`** [r1 N2 fix 4;
N3 fix]. The licence-checked clue file stays byte for byte as it is (its
SHA-256 is recorded in 12.4). The regime file names, for every row of the
projection, the option and the parameter values each regime uses. I13(f)
checks that every named option exists. Leave-one-set-out values are always
taken from the row's own list. Regime BM's 1.5 d is not in the lists: the
lists are the drafter's tolerance grids, not licences, and the regime file
records the value as a decision [r1 N2 fix 4].

| | regime SL (observer slack, leave-one-set-out) | regime BM (B&M's method as written) |
|---|---|---|
| option | the row's primary | B&M's own proxy where the row offers it (`bm_mwra_k`, `bm_venus_lead`); else, for a greatest-elongation row, `ge_true_k`; else the row's primary [r1 N3 fix] |
| Mercury and Venus greatest-elongation k | **leave-one-set-out**: the smallest value of the row's own list at or above the largest \|record − true greatest elongation\| (true Sun) among the records of that body *outside* the set, from alm Table 2 (records in no set included) [r1 N2 fix 1] | 1.5 d, B&M's ±1 integer day as a continuous tolerance [r1 N13]; 1 d reported |
| `bm_mwra_k` | — (not primary anywhere) | 1.5 d |
| `bm_venus_lead`, minimum lead | — | 90 min |
| opposition k (full run only) | leave-one-set-out over the oppositions in no set: listed value ≥ 0.42 d (mean Sun) = 1 d | middle value |
| every other list (j_days, tolerance_deg, tolerance_days, time_tol_h, minimum minutes, minimum altitude) | most lenient value | middle value (lower middle for an even count) |

Under leave-one-set-out, no set is scored with a tolerance taken from its
own records. **Gate 3b is therefore scored on held-out sets only** [r1 N2
fix 2]. The same records also calibrate the 6-d DOC option of F5 and the
Mercury slot of T_A (5.3), but those serve the Odyssey's garden. Neither
validates the method, so the training-and-testing overlap the recheck
found is broken [r1 N2]. Scoring follows 6.3.2: best-fit; seen := the truth
is in B and \|B\| ≤ 0.05 N_cand, N_cand being the days in the window.
Resolution and uniqueness are reported.

**The gate.**

- seen_ALM_SL is the number of the 11 counted sets seen in regime SL
  (projection, best-fit).
- rec_ALM_BM is the number with strict recall and \|S₀\| ≤ 0.05 N_cand in
  regime BM (projection, strict).
- **3b fires if seen_ALM_SL < 6** (fewer than half of 11, rounded up).
  PC-S no longer enters the gate [r1 N2 fix 3].
- **Q_BM holds if rec_ALM_BM < 6**: "B&M's tolerances cannot recover expert
  planetary records" [rev #3 fix 3]. It conditions every "no" about the
  Odyssey. It blocks outcome 1 unless G_DOC,hi ≤ 0.05 too (section 9).

**What is already known.** Under these frozen rules the truth-side slack
already decides much (2.6):

- truth is retained in 9 of 11 sets in regime SL, with ALM-G and ALM-H
  failing, and only narrowing remains open (P25);
- rec_ALM_BM is at most 5, so **Q_BM holds**, and the bench recomputes it as
  a regression check.

The harness must implement two pieces of new vocabulary: the bound
`same_apparition`, and ALM-F.4's `star_candidates`, with one garden branch
per candidate [lca].

### 6.5 Negative controls (outcome 4)

**The clue file** is `data/prereg/negatives.json` as licence-checked [lcn].
It holds 12 clean negatives (Virgil, Apollonius, Quintus Smyrnaeus, Valerius
Flaccus) and the Iliad as a same-tradition comparison [rev #15 fix 1–2; neg
§1]. Each clean negative is fiction or legend composed long after the events
it tells, drafted under the Odyssey's own selection rules, with no similes
and no lying tales. Its `operational` fields are prose, so each option is
translated into a canonical predicate in `data/prereg/operational_map.json`
before the freeze, and a second agent checks each translation against its
prose.

**Pre-freeze decisions and second reading** [neg §6; lcn §4]:

- **Counts and caps.** A second reader checks the interval forks and caps
  that rest on the drafter's own counts: ARG-CIUS n16/n17/n18, ARG-COLCHIS
  a3/a4, IL h12/h13/h15, VF-LEMNOS-01, and the caps free30, xfree, w60 and
  QS-SACK-06's 10 d.
- **"literal" means least inference.** Pinned literal readings that use an
  inferred or drafter-width option (AEN-CRETE-01 a60, ARG-RETURN-03 x0,
  ARG-COLCHIS-02 a3) are re-pinned by the second reader to the
  least-inference option of their row.
- **QS-SACK-03.** Its BM-analogue pin keeps option b in its new meaning (the
  Pleiades over the dark hours), and b-late stays in the garden.
- **Places and thresholds.** The same reader checks the place
  identifications against a gazetteer (Pleiades). In `operational_map.json`
  the reader flags the numeric thresholds that are the drafter's
  operationalisations [lcn §4.3; 13 rows 34–35].
- **The withdrawn eclipse classes** [r1 N11]. Several rows still cite
  revision 1's classes:
  - QS-SACK-06:a and IL-PATROCLUS-02's solar_am and solar_any require "a
    solar eclipse of class X1–X4 (DESIGN 3.1)";
  - `controls_real.json` cites "X3 ≥ 0.95, X4 ≥ 0.60".

  `operational_map.json` records one decision for all of them. "Class
  X1–X4" means X2 ∪ X3 ∪ X4 under revision 1's own definitions [v1 §3.1].
  In the bench's probabilistic terms that is h_06 ≥ 0.5 or h_tot ≥ 0.5 at
  the option's site and day. X3 and X4 alone map as in 6.3.3.

**Windows.** Each clean negative is searched in the Odyssey's own two
windows (reproduction, 136 years; primary, 251 years) at its own site. The
negatives tell events of the same legendary age, and these windows give
fiction exactly the chances the Odyssey had. Twenty further random positions
per width are a sensitivity.

**Gardens.** 𝒢_j is the full product of set j's fork options, with each F5
entry expanded into its tolerance and visibility variants [neg §1 item 6].
Its eclipse-compatible readings are those that contain a solar-eclipse or
Day-0-conjunction option listed in the set's `eclipse_compatible_options`.
Lunar-eclipse options are not solar eclipses and are excluded, as the file
says. The negatives' readings were drafted without any target, so their G
needs no conditioning (5.3).

**The test** [rev #1 fix 3]:

- **hit_j** holds when some eclipse-compatible reading of 𝒢_j has, in one of
  the two windows, a unique Day-0 survivor whose eclipse has h_tot ≥ M_Ody.
  Each option is evaluated at **its own day and its own site** [r1 N11 fix
  2]:
  - for a Day-0 option, at the set's first `observer_places` entry;
  - for QS-SACK-06:a, near Cape Caphereus on Day +2..+12 after the unique
    Day-0 survivor.
- **G_j** is the mean reach_136, under 𝒢_j, over all daylight conjunctions
  at the set's site in the core. Its interval is the gamma interval of 5.3.
- **Outcome 4 fires if some clean negative has hit_j and G_j,hi ≤ G_BM,u.**
  G_BM,u is the Odyssey's G under 𝒢_BM* over T, the same kind of
  unconditioned target set. It is the Odyssey's coincidence as B&M would
  present it, with every reading treated as blind, so the comparison
  favours B&M twice: 𝒢_j holds more readings than 𝒢_BM*, and the negative is
  taken at its upper bound.

Also reported per set:

- the survivors of each pinned reading (literal and BM-analogue; R-i, R-ii
  and R-ii-literal for AEN-TROY);
- survivors per century;
- the slot matrix of [neg §5].

**The Iliad** (IL-PATROCLUS) gets the same computations. It is reported as
the same-tradition comparison and is not used in the rule. Two consistency
checks run beside it:

- **Iliad against Odyssey.** If both carry real dates, the Iliad's (the
  tenth year of the war) must fall about 8–12 years before the Odyssey's
  (the return in the twentieth year [win §5]). For the pinned BM-analogue
  readings the bench reports the offset and its base rate: the chance that
  an unrelated survivor falls in a given 5-year band.
- **Cross-text competition.** The bench counts how many texts and readings
  the gardens attach to each eclipse with h_tot ≥ 0.1. 30 Oct 1207 BC and 30
  Sep 1131 BC have also been claimed for Joshua 10 [crit §0 item 7,
  *secondary*]. Joshua is outside the grammar and is not run.

---

## 7. Clues B&M did not use

These come from the 76-row inventory [txt §4], and none is used to fit
anything. Each testable one is evaluated three ways:

- (i) on 16 Apr 1178 BC;
- (ii) on every survivor of every 𝒢_BM* reading;
- (iii) for its **base rate conditional on the reading** [rev #11 fix 1]:
  the pass rate among the background survivors of the same reading, and
  among the candidates of P_spring that pass N and C.

If the clues record a real sky, held-out clues should pass more often among
the survivors than their conditional base rate says.

| # | clue (lines; day) | testable? | predicate (frozen now) | how it enters |
|---|---|---|---|---|
| H1 | "this night is very long" (11.373; Day −7 seq); "these nights are endless" (15.392; Day −3) | yes | night (Sun's centre below −0.833°) ≥ 12.0 h on that night | **non-blind, not counted** [rev #11]. The threshold was set after the nights of 1178 BC (11.5 h and 11.3 h, a fail) had been computed [txt §5.6], and it measures the season C already fixes. Reported, also under R_anc |
| H2 | σκοτομήνιος, the dark night (14.457; night of Day −5 seq / −4 par) | yes | Moon above the horizon for < 25% of the dark hours | counted. Given Day 0 a conjunction it passes about half the time (median 25%), not "almost always" as revision 1 said [rev #24b; vis §4.5] |
| H3 | Hermes leads the suitors' souls past the gates of the Sun (24.1–14; night of Day 0/+1) | yes, under the Hermes = Mercury rule | **one predicate** [r1 N14]: Mercury not visible (AV 10°) on the mornings and evenings of Day 0 and +1, **and** within ±3 days of a conjunction with the Sun | counted once, with the joint conditional base rate. Revision 2 counted its two halves as two trials, but they are nearly one event. 34 days after a morning rising-azimuth maximum Mercury is heading for superior conjunction, so its unconditional rate would mislead [rev #11] |
| H4 | Ares and Aphrodite caught together (8.266–366; Day −7 seq) | yes, under the same rule | Venus–Mars separation ≤ 5° within ±3 days of Day −7 | counted, with a conditional base rate (V fixes Venus' elongation) |
| H5 | Mars invisible in March–April 1178 BC except during the eclipse | yes | Mars not visible (AV 11.5°) on any morning or evening from Day −34 to Day 0 | **non-blind, not counted**: B&M found it after the date [bm §2] |
| H6 | the twentieth year (9 lines); a year with Circe and seven with Calypso | yes, against ancient sack dates | the year lies 8–11 years after one of the ancient sack dates (Duris 1334/3 to Ephorus 1135, as in [win §3]; Clement's list [unread §4]) | external check, reported per survivor; strict Eratosthenes alone excludes 1178 BC [win §6] |
| H7 | Theoclymenus at the δεῖπνον; supper "in the light" (20.390–394, 21.428–429) | partly | eclipse maximum in daylight on Day 0 | consistency only, for eclipse-compatible readings; "noon" is not in the text [txt §5.10] |
| H9 | frost feared (5.467, 17.25); hearths and fires (6.305, 7.153, 18.307–311, 19.63–64) | no | — | weather, not sky. Reported qualitatively, with the five scholia that read autumn or winter [txt §5.6] |
| H10 | nightingale (19.519), swallows (21.411, 22.240), gadfly (22.301 = 18.367) | no | — | similes, so excluded [txt §5.4]. 18.366–370 is also a wish, read as winter, May or autumn by different advocates, and is used for nothing [unread §2.3] |
| H11 | much-flowering wood (14.353) | no | — | inside a lying tale, so excluded |
| H12 | Laertes digging round a plant (24.226–231; Day +1) | no | — | qualitative |
| H13 | Helios' complaint (12.374–390), Poseidon and Zeus (13.125–158) | no | no operational predicate is defensible | listed, not run |

Revision 1's H8 ("starry pre-dawn sky", 20.98–121) is **withdrawn**:
"ἀπ' οὐρανοῦ ἀστερόεντος" (20.113) is a stock epithet, used in daylight at
Od. 9.527, and the scene follows the dawn at 20.91 [rev #24a].

**The counted statistic.** Two figures are computed:

- the number of the three counted predicates (H2, H3, H4) that 1178 BC
  passes, against the Poisson-binomial distribution of their conditional
  base rates;
- over all 𝒢_BM* survivors, the pass rate against the conditional base rate.

Power is low with so few survivors, and the report says so. The same
statistics are computed for R_anc's survivors, the ancient autumn reading
[rev #11 fix 3]. The held-out clues are the bench's only evidence formed
blind to the target, and they enter no rule. Their result is a standing
finding (1.3).

---

## 8. Pre-registered predictions

Written 2026-10-04, before any null model, control search or held-out check
of the bench was run. Each prediction names its quantity, the script that
computes it and the threshold that decides it.

Revision 3 renumbers the list. The column "v2" gives revision 2's number,
and the predictions that the recheck showed to be settled have moved to
section 2 (table 2.7) [r1 N7]. Items implied by numbers already known are
listed first as **regression expectations**. They need the full run to be
confirmed, and a confirmation is not counted.

### 8.1 Regression expectations (implied by section 2; not counted)

| # | expectation | v2 | basis |
|---|---|---|---|
| R1 | Regression checks A1–A5 pass (`reproduce.py`) | P1 | 2.2, 3.4 |
| R2 | 16 Apr 1178 BC passes N, C, V and M in every cell of the T0 grid | P2 | 2.2 |
| R3 | With E off, the N ∧ C ∧ V ∧ M survivors in 1250–1115 BC number at least 2 and include 18 Mar 1189 BC | P3 | 2.2 |
| R4 | With E ≤ 5 Apr and with E ≤ 6 Apr the survivor set is exactly {16 Apr 1178 BC}; with E ≤ 4 Apr it is empty | P4 | 2.2 |
| R5 | T0 is RE in the primary cell and in every cell with E ≤ 5 or ≤ 6 Apr, and NR in every cell with E ≤ 4 Apr | P5 | 2.2 |
| R6 | The half-open UT+2 window holds 1,683 conjunctions | P7 | 2.2 [rev #22] |
| R7 | In the DE431 pairing the per-model P(total) values move from the canon-frame table of 2.3 by the equivalent of about 40 s. The orderings (1131 above 1178 except under the SMH2016 parabola) and the joint bounds (≤ 0.06 for three models, ≥ 0.08 for SMH2016) are unchanged (`deltat.py`) | P26 | 2.3 [r1 N7] |
| R8 | strict_PCR = 4: the accepted dates fail a primary row in R-PTOL-BAB, R-PTOL-ALEX and R-PYDNA (`controls.py`) | P34 | 2.6 |
| R9 | rec_ALM_BM ≤ 5, so Q_BM holds (`almagest.py`) | P36 | 2.6 |
| R10 | In regime SL the truth is in the best-fit set B of exactly 9 counted *Almagest* sets; it is not in B for ALM-G and ALM-H (`almagest.py`) | — | 2.6 |
| R11 | R_anc with the eclipse clue counts 30 Sep 1131 BC among its survivors in 1250–1115 BC, and not 16 Apr 1178 BC. Without the eclipse clue it has no unique survivor in any window (`garden.py`) | P23 (restated) | 2.8, 5.3 |
| R12 | T0 ≠ R, so outcome 1 does not hold (`verdict.py`) | — | R3, 2.8 |

### 8.2 Predictions (counted)

**Reproduction (T0; `reproduce.py`)**

- **P1.** With C_rel and E_rel in place of the fixed Julian bounds, the
  reproduction-window survivor sets of R3 and R4 are unchanged. (v2 P6)
- **P2.** The T0b survivor sets (E off; E ≤ 5 Apr) do not change when the
  clock ΔT is replaced by SMH2020, SMH2020 + 1σ and SMH2020 − 1σ with DE431
  conjunctions. (v2 P27)
- **P3.** The T0b survivor set with E off is the same under MWRA_vtx at
  ±1.5 d (primary), MWRA_vtx at ±1 d and MWRA_int at ±1 day [r1 N13]. (new)

**Rates (N1; `rates.py`)**

- **P4.** λ(N ∧ C ∧ V ∧ M) over the background lies in [0.44, 1.76] per
  century: within a factor 2 of B&M's own arithmetic at their ±1-day
  tolerance (0.88). (v2 P8)
- **P5.** λ(N ∧ C ∧ V ∧ M ∧ E_rel, n = 4) is at least 0.07 per century,
  above B&M's printed 0.048 (their own arithmetic at ±1 d gives 0.14). (v2 P9)
- **P6.** The background holds at least 10 N ∧ C ∧ V ∧ M survivors, and the
  empirical P(≥ 1 survivor in a 136-year window) is at least 0.5. (v2 P10,
  scaled to the longer background)
- **P7.** p_fix|C lies in [0.002, 0.02] (rough estimate 0.008 [vis §5]); the
  unconditional p_fix lies in [0.0002, 0.002] (rough 0.0007). (v2 P11)
- **P8.** The V–M dependence ratio on P_spring lies in [0.5, 2], with
  permutation p > 0.05. (v2 P12)
- **P9.** Under C_rel, λ(N ∧ C ∧ V ∧ M) in the first and in the last 700
  years of the background agree within a factor 2. Under the fixed Julian
  bounds, fewer than 90% of the candidates that pass the fixed C in
  −1999..−1800 also pass C_rel. (v2 P13, restated for the 2,200-year
  background)

**The eclipse coincidence (N2; `coincidence.py`)**

- **P10.** p_e(M_Ody) over P_spring is within a factor 2 of p_e(M_Ody) over
  P_day, with 16 Apr −1177 excluded from both. (v2 P14)
- **P11.** V and M pass rates do not differ between eclipse and non-eclipse
  spring new moons (permutation p > 0.05 for each). (v2 P15)

**Forking paths (N3; `garden.py`)**

- **P12.** reach_136(16 Apr 1178 BC) under the T0b reading with E off is 0,
  because another survivor falls in −1176..−1052. (v2 P16)
- **P13.** G_BM ≥ 2 × p_fix,unique. (v2 P17)
- **P14.** G_BM (𝒢_BM*, T_A) lies in [0.05, 0.40], and G_DOC ≥ 2 × G_BM.
  (v2 P18, restated for the conditioned pool)
- **P15.** Some reading of 𝒢_DOC*^X makes 30 Sep 1131 BC the unique survivor
  of a 136-year window containing it. (v2 P19)
- **P16.** Some reading of 𝒢_FULL*^X makes 24 Jun 1312 BC the unique
  survivor of a 251-year window containing it. (v2 P20)
- **P17.** G_X(𝒢_BM*) lies within a factor 2 of G_BM,u: eclipse dates
  are not specially reachable. (v2 P21)
- **P18.** The greedy smallest fork set that brings G over T_A to 0.20 adds
  at most four options to 𝒢_BM*. (v2 P22, restated)
- **P19.** R_anc with the eclipse clue has at least two survivors in the
  reproduction window, so it is not unique there either. (v2 P23, restated
  [r1 N7, N9])

**Random epics (N4; `randomepic.py`)**

- **P20.** For variant A epics, P(unique survivor in a 136-year window) lies
  in [0.2, 0.6], and P(T_best ≥ T_obs) ≥ 0.2. (v2 P24)
- **P21.** Ē_N4, the mean reach of Schoch's target over entering stratum
  epics, lies within a factor 3 of G_BM. Varying the poem and varying the
  target give the same null mean [r1 N10]. (v2 P25, restated)

**PC-S (`synthetic.py`)**

- **P22.** Science mode, zero noise: P(unique) under the B&M reading, over
  the truths of T_A that pass it, is ≤ 0.6. (v2 P29)
- **P23.** The B&M reading's recall at j = 3 is at most half its recall at
  j = 0. (v2 P31, restated on recall)

**Controls (`controls.py`, `almagest.py`, `negatives.py`)**

- **P24.** seen_PCR ≥ 4: R-PTOL-BAB, R-PTOL-ALEX, R-ARBELA and R-DIOD are
  seen; R-THUC, R-XEN and R-PYDNA are not seen in the primary run. (v2 P33)
- **P25.** seen_ALM_SL ≥ 6: at least 6 of the 9 sets that retain their truth
  (R10) also narrow their window to 5%. (v2 P35; only narrowing is open)
- **P26.** Q_ΔT does not hold: the circular controls keep their gate status
  when their ΔT is widened. (new [r1 N4])
- **P27.** Q_exposure does not hold. (new [r1 N5])
- **P28.** No clean negative fires outcome 4, and at least one clean negative
  has a unique survivor of some kind in one of the two Odyssey windows.
  (v2 P37)
- **P29.** Some eclipse-compatible reading of IL-PATROCLUS makes an eclipse
  new moon with h_09 ≥ 0.5 at Troy the unique survivor of the 251-year
  primary window. (v2 P38)

**Held-out clues (`heldout.py`)**

- **P30.** 16 Apr 1178 BC passes no more of H2, H3 and H4 than their
  conditional base rates predict (Poisson-binomial p > 0.1). (v2 P39, H3
  counted once)
- **P31.** Over all 𝒢_BM* survivors, the held-out pass rate lies within the
  95% interval of the conditional base rate. (v2 P40)

**Evidential weight (`verdict.py`, standing findings)**

- **P32.** BF_BM(ρ = 1) < 5. (new; the single-reading figure of about 8 in
  2.8 is a rough ceiling, and the garden average is new)
- **P33.** The median *Almagest* Bayes factor over the 11 counted sets is at
  least 10 × BF_BM(ρ = 1). (new [r1 N1 fix 4])

**Bottom line (`verdict.py`)**

- **P34.** G_BM falls in the inconclusive band: G_BM,lo < 0.20 and
  G_BM,hi > 0.05.
- **P35.** The verdict is {inconclusive} or {2}, with Q_BM, and contains no
  3a, 3b or 4.

---

## 9. The decision rule

### 9.1 Named quantities

One script computes each quantity the rule reads and writes it to one JSON
key, stamped with the frozen code tree hash (section 12).

| quantity | definition | section | written by |
|---|---|---|---|
| INSTR | instrument checks I1, I2, I2b and I4–I14 all pass (I3 is a calibration and is excluded) | 6.1 | `results/instrument/summary.json` |
| T0 | T0 verdict in the primary cell (E ≤ 5 Apr, visibility off, MWRA_vtx at ±1.5 d): R, RE or NR | 3.5 | `reproduce.py` |
| G_BM, G_BM,lo, G_BM,hi; n_A, k_A | G(𝒢_BM*; T_A; W = 136), its gamma interval, the pool size and the number of targets reached | 5.3 | `garden.py` |
| G_DOC, G_DOC,hi | G(𝒢_DOC*; T_A; max over W) and its upper bound | 5.3 | `garden.py` |
| G_BM,u; n_T | G(𝒢_BM*; T; W = 136) = (n_A/n_T) G_BM | 5.3, 4.2 | `garden.py` |
| pct_N4, pct_N4,lo, pct_N4,hi; n_stratum | the share of entering stratum epics whose BM-tier garden reaches Schoch's target at least as well as 𝒢_BM* does, with its Clopper–Pearson interval and the number of entering epics | 5.4 | `randomepic.py` |
| seen_PCR, strict_PCR | of the 7 counted PC-R sets: seen; strict recall (ΔT mixture) | 6.3.2–6.3.3 | `controls.py` |
| seen_PCR,redraft; seen_PCR,sibling | seen_PCR with the five re-drafted primaries; with every audited row at its failing sibling convention | 6.3.4 | `controls.py` |
| seen_PCR,noncirc | seen_PCR with the circular sets' ΔT σ tripled | 6.3.3 | `controls.py` |
| seen_ALM_SL, rec_ALM_BM | of the 11 counted *Almagest* sets: seen in regime SL (leave-one-set-out); strict recall with narrowing in regime BM (B&M's option rule) | 6.4 | `almagest.py` |
| hit_j, G_j, G_j,hi; n_j | for each of the 12 clean negatives | 6.5 | `negatives.py` |

No likelihood ratio, Bayes factor, PC-S recall or held-out count is a rule
input. They are standing findings (1.3, 5.7, 6.2, 7). The thresholds are in
`data/prereg/verdict_rule.json` and are frozen.

### 9.2 The rule

`odybench/verdict_rule.py` implements exactly this, as a pure function of
the quantities above:

```
if not INSTR:                                   return BLOCKED (no verdict is read)
labels, qualifiers = {}, {}
if seen_PCR < 4:                                labels += 3a
if seen_ALM_SL < 6:                             labels += 3b
if rec_ALM_BM < 6:                              qualifiers += Q_BM
if strict_PCR < 4:                              qualifiers += Q_strict
side = (seen_PCR < 4)
if (seen_PCR_redraft < 4) != side or (seen_PCR_sibling < 4) != side:
                                                qualifiers += Q_exposure
if (seen_PCR_noncirc < 4) != side:              qualifiers += Q_dT
if U0(n_A) > 0.05 or CP0(n_stratum) > 0.05:     qualifiers += Q_attain
if any(hit_j and G_j_hi <= G_BM_u for j in clean negatives):
                                                labels += 4
outcome1 = labels is empty
       and T0 == R
       and G_BM_hi <= 0.05
       and pct_N4_hi <= 0.05
       and (Q_BM not in qualifiers or G_DOC_hi <= 0.05)
if outcome1:                                    labels = {1}
elif G_BM_lo >= 0.20 or pct_N4_lo >= 0.50:      labels += 2
if labels is empty:                             labels = {inconclusive}
return labels, qualifiers
```

Here U0(n) = 3.69/n is the gamma upper bound of a G with no target reached,
and CP0(n) = 1 − 0.025^(1/n) is the Clopper–Pearson upper bound of a share
with no epic counted.

### 9.3 How to read it

- **Every rule names its garden and its pool** [rev #1 fix 1].
  - 𝒢_BM* over T_A is primary.
  - 𝒢_DOC* over T_A enters only when Q_BM says that B&M's tolerances cannot
    see real records. Outcome 1 must then also hold for the documented
    garden, whose tolerances include the observer slack.
  - 𝒢_BM* over T enters only the comparison with fiction, whose readings
    are blind.
  - The verdict recomputed with 𝒢_DOC* and 𝒢_FULL* in place of 𝒢_BM*, with
    the E-on gardens, and with revision 2's pool T_C, is printed beneath it
    as a sensitivity. It never replaces the verdict.
- **G has one sense throughout**: a look-elsewhere-corrected p-value, small
  when the coincidence is notable.
  - Outcome 1 needs it small.
  - Outcome 2 needs it large.
  - Outcome 4 asks whether fiction's is as small as the Odyssey's.
- **Intervals work against the claim being made** [r1 N8 fix 2]:
  - outcome 1 uses the upper bounds of G and of the percentile;
  - outcome 2 uses their lower bounds;
  - outcome 4 uses the negative's upper bound.

  The gap between 0.05 and 0.20 for G, and between 0.05 and 0.50 for the
  percentile, is the inconclusive region. It is reported as such, with
  every number.
- **Why 0.05 and 0.20 over T_A.** The thresholds of revision 2 (0.01 and
  0.05) were set for G over T_C. For 𝒢_BM*, G over T_C equals
  (n_A/n_TC) G over T_A, about 0.154 × G over T_A, because targets outside
  A are never reached (4.2). Revision 2's 0.01 therefore corresponds to
  about 0.065 over T_A, and revision 3's 0.05 is slightly stricter. Revision
  2's 0.05 corresponds to about 0.32, and revision 3's 0.20 is more
  generous to "ordinary". Both sit above the floor U0(139) = 0.0265.
- **T0 must be R.** RE is a reproduction that holds only with the
  equinox clue, whose reading was fitted to the eclipse [r1 N6 fix 3].
- **Labels 2, 3a, 3b and 4 can hold together** and are all reported. The
  headline leads with 3a or 3b when either holds, because they say which
  "no"s mean nothing.

### 9.4 Structural constraints: what an input set must satisfy to be realisable

A synthetic input set proves an outcome reachable only if real data could
produce it. Revision 2's set S1 asked for a likelihood ratio of 45 where the
structure allowed at most about 6.5, so it proved a code branch reachable
and not an outcome [r1 N1]. Every quantity of 9.1 obeys the following
constraints, and I14(b) checks each synthetic set against all of them. The
estimates of n are those of 2.8. At verdict time `verdict.py` re-checks the
attainability constraints with the measured n and records Q_attain.

| # | constraint | why |
|---|---|---|
| C1 | 0 ≤ G_lo ≤ G ≤ G_hi ≤ 1 for every G, and G_hi ≥ U0(n) = 3.69/n with n its pool size | the gamma interval (5.3) |
| C2 | G_BM,u = (n_A/n_T) · G_BM, with n_A ≈ 139 and n_T ≈ 10,690 | no target outside T_A is reached by 𝒢_BM* (4.2) |
| C3 | pct_N4,lo ≤ pct_N4 ≤ pct_N4,hi, and pct_N4,hi ≥ CP0(n_stratum) with n_stratum ≥ 200, so pct_N4,hi ≥ 0.018 | Clopper–Pearson (5.4) |
| C4 | if hit_j, then G_j > 0 and G_j,hi ≥ U0(n_j) | a unique survivor in the core has reach > 0 |
| C5 | the counts are integers: 0 ≤ seen_PCR, strict_PCR and the other PC-R counts ≤ 7; 0 ≤ seen_ALM_SL, rec_ALM_BM ≤ 11 | definitions |
| C6 (attainability) | outcome 1 is attainable only if U0(n_A) ≤ 0.05 and CP0(n_stratum) ≤ 0.05, that is n_A ≥ 74 and n_stratum ≥ 73. Outcome 4 is attainable only if G_BM,u ≥ U0(n_j), that is G_BM ≥ about 0.027 when n_j ≈ n_T | C1–C4 |

Some facts are already known about the Odyssey's inputs (2.8): T0 is
expected to be RE, rec_ALM_BM is at most 5, and seen_ALM_SL is at most 9.
**These are known facts, not structural constraints.** A synthetic set may
contradict them, because the rule must also be shown to work for data that
differ from the Odyssey's. Each set that does is marked in 9.5.

### 9.5 Synthetic input sets that prove every outcome reachable

`data/prereg/verdict_synthetic/*.json` holds these inputs, and
`tests/test_verdict.py` asserts the stated output for each (I14a) and checks
it against 9.4 (I14b). Every set uses n_A = 139, n_T = 10,690,
n_stratum = 200 and n_j = 10,690 unless it says otherwise. Only the fields
that differ from S1 are given for the later sets.

| set | inputs | labels | qualifiers | contradicts a known fact? |
|---|---|---|---|---|
| **S1** | INSTR true; T0 R; G_BM 0.0065, lo 0.0013, hi 0.034 (k_A 3); G_BM,u 0.000084; G_DOC 0.012, hi 0.040; pct_N4 0.010, lo 0.0012, hi 0.036 (2 of 200); seen_PCR 6, strict_PCR 5, redraft 6, sibling 6, noncirc 6; seen_ALM_SL 8; rec_ALM_BM 3; every negative: hit false, G_j 0.0006, hi 0.0012 | **{1}** | Q_BM | T0 = R (expected RE) |
| **S2** | T0 RE; G_BM 0.30, lo 0.23, hi 0.39; G_BM,u 0.0039; G_DOC 0.42, hi 0.53; pct_N4 0.62, lo 0.55, hi 0.69 | **{2}** | Q_BM | none |
| **S3a** | seen_PCR 2, redraft 2, sibling 2, noncirc 2 | **{3a}** | Q_BM | T0 = R |
| **S3b** | seen_ALM_SL 3 | **{3b}** | Q_BM | T0 = R |
| **S4** | T0 RE; G_BM 0.10, lo 0.062, hi 0.16; G_BM,u 0.0013; G_DOC 0.15, hi 0.22; pct_N4 0.20, lo 0.15, hi 0.26; AEN-TROY: hit true, G_j 0.0005, hi 0.0011 | **{4}** | Q_BM | none |
| **S0** | as S4, but no negative hit | **{inconclusive}** | Q_BM | none |
| S5 | as S1, but G_DOC 0.050, hi 0.097 | {inconclusive} | Q_BM | T0 = R |
| S6 | as S2, but seen_ALM_SL 3, strict_PCR 2, redraft 3, noncirc 3; AEN-TROY: hit true, G_j 0.0019, hi 0.0028 | {2, 3b, 4} | Q_BM, Q_strict, Q_exposure, Q_ΔT | none |
| S7 | INSTR false | BLOCKED | — | — |
| S8 | as S1, but T0 RE | {inconclusive} | Q_BM | none |
| S9 | as S1, but n_A 70, k_A 0, G_BM 0, lo 0, hi 0.053, G_BM,u 0 | {inconclusive} | Q_BM, Q_attain | T0 = R |
| S10 | as S1, but rec_ALM_BM 7 and G_DOC hi 0.09 | **{1}** | none | T0 = R; rec_ALM_BM ≥ 6 |

What each set shows:

- **S1–S4** reach each of the four outcomes, with 3 in both of its parts.
  S0 reaches the inconclusive verdict.
- **S5** shows the Q_BM path blocking outcome 1. **S10** shows that the path
  matters only when Q_BM holds.
- **S6** shows labels and qualifiers occurring together.
- **S8** shows that RE does not count toward outcome 1 [r1 N6].
- **S9** shows Q_attain: with a pool of 70 targets, about revision 2's
  size, the floor is above 0.05.
- **S7** shows the instrument block.

The arithmetic of the sets:

- Every interval is computed with the methods of 5.3 and 5.4 from an assumed
  reach vector [me: `results/design-revision-r2/synth_sets.py`, `.out.txt`].
  For example, S1's G_BM is three targets reached at reach 0.3 out of 139.
- Every G_BM,u is (n_A/n_T) G_BM (C2).
- S4's and S6's negatives satisfy C4 and sit below G_BM,u, which C6 allows
  because their G_BM ≥ 0.027.

**Outcome 1 is reachable for data that pass T0, and it is not expected for
the Odyssey,** whose T0 is expected to be RE (2.8). That expectation is a
fact about the Odyssey's data, which the bench recomputes. It is not a
property of the rule.

---

## 10. Software

### 10.1 Build plan

The build is done by agents in parallel. Each agent owns the files listed
for it, works to the interfaces of 10.2, and must not read what is listed in
the last column. The lead writes `odybench/model.py`, the shared types,
first, and it is frozen as the contract. Code inside the package runs as
`py -m odybench.x`, never as `py odybench/x.py`, because the file would
then shadow the standard library's `calendar` [acq §4].

| agent | owns | depends on | must not read |
|---|---|---|---|
| A0 lead | `odybench/model.py`; `data/prereg/sites.json` (with a span and a column set per site), `windows.json`, `seeds.json`, `deltat_models.json`, `verdict_rule.json`, `almagest_regimes.json` | this design | — |
| A1 sky | `odybench/sky.py`, `odybench/events.py`, `tools/build_sky.py`, `tools/build_events.py`, `tools/validate_events.py` (I5, I6, I12), `tools/fetch_horizons_rts.py` | `model.py`, `ephem.py`, `calendar.py` | — |
| A2 eclipses | `odybench/eclipses.py`, `odybench/lunar.py`, `odybench/deltat_mix.py`, `data/prereg/eclipse_hit.json`, `tools/build_eclipses.py`, `tools/validate_eclipses.py` (I2, I4), `tools/fetch_lecat.py`, `tests/test_eclipses.py`, `tests/test_lunar.py` | `model.py`, `ephem.py`, `data/jsex/` | the truth files (I2b runs through the harness) |
| A3 clues | `odybench/prereg_io.py`, `odybench/clues.py`, `odybench/search.py`, the controls sections of `data/prereg/operational_map.json`, a draft of its negatives section, `tools/make_redraft_brief.py`, `tests/test_clues.py`, `tests/test_prereg_io.py` | A1 and A2 interfaces | `*_truth*`, `results/controls-*`, `check_truth*` |
| A4 garden | `odybench/readings.py`, `odybench/pools.py`, `odybench/reach.py` (I9), `odybench/evidence.py`, `data/prereg/garden.json`, `readings.json`, `rates.py`, `coincidence.py`, `garden.py`, `windows.py` | A3 | `*_truth*` |
| A5 epics and PC-S | `odybench/epic.py`, `odybench/pcs.py`, `data/prereg/epic_grammar.json`, `randomepic.py`, `synthetic.py` (I10, I10b) | A3, A4 | `*_truth*` |
| A6 harness and verdict | `odybench/harness.py`, `tools/build_truth_index.py`, `controls.py`, `almagest.py`, `negatives.py`, `heldout.py`, `data/prereg/heldout.json`, `odybench/verdict_rule.py`, `verdict.py`, `read.py`, `odybench/stats.py`, `odybench/prereg.py`, `tools/freeze.py`, `tests/test_verdict.py` (I14), `data/prereg/verdict_synthetic/` | all | — |
| A7 second implementation | `tests/bm_reference.py` (I7) | `ephem.py`, `calendar.py`, section 3.2 of this design | every other bench module |
| A8 unexposed re-drafter | `data/prereg/pcr_redraft.json` | `data/prereg/pcr_redraft_brief.json` only | everything else in the repository (6.3.4) |
| A9 second reader of the negatives | the review of the negatives section of `operational_map.json`; the interval forks and caps; the literal pins and the X-class decision (6.5); the replay script of its edits | `negatives.json`, `data/text/` | — |
| A10 reproduction and ΔT | `reproduce.py`, `deltat.py`, `odybench/s2.py`, `tests/test_t0.py` | A1, A2 | — |
| A11 ΔT-fit reader | `data/prereg/deltat_circular.json` (6.3.3), with page locators into SMH2016 and the 2020 Addendum | the two papers and their supplementary tables | the truth files |

### 10.2 Module interfaces

All times are JD floats with a named scale, and all calendar work goes
through `odybench.calendar`. Arrays are numpy. Files are NPZ (numeric) or
JSON (UTF-8, `ensure_ascii=False`).

**`odybench/model.py`** (the contract)

```
BODIES = ("sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn")
GRAMMAR_STARS = ("alcyone", "arcturus", "sirius", "aldebaran", "betelgeuse",
                 "rigel", "dubhe")           # extras from data/stars.json allowed
DT_MODELS = ("smh2020", "smh2020_parabola", "smh2016_parabola", "em_canon")
@dataclass Site(key, lat, lon, elev_m, source, span: tuple[int, int],
                columns: tuple[str, ...])                    # span: Julian years, inclusive
POOL_DTYPE = [("jd_ut","f8"), ("jd_tt","f8"),
              ("day0_jdn_ut2","i8"), ("day0_jdn_lmt","i8"),  # one Day-0 date per clock
              ("kind","U12"), ("cat_idx","i8"), ("daylight","?")]
@dataclass Predicate(type: str, params: dict, day: int | tuple[int,int] | None,
                     quant: str = "any", site: dict | None = None,
                     dt_rule: str = "mixture_p50")            # how a ΔT-dependent row passes
@dataclass Option(name: str, primary: bool, predicate: Predicate | None,
                  grid: dict[str, list])                      # None = the clue is dropped
@dataclass ClueRow(clue_id, event_id, day_offset, options: list[Option])
@dataclass ClueSet(set_id, role, anchor_kind, events, links, rows, site_rule,
                   window_widths, counted: bool)
@dataclass Reading(choice: dict[str, tuple[str, dict]])     # clue_id -> (option, grid values)
@dataclass SearchResult(pool, fails: np.ndarray[int16], strict: np.ndarray[int64],
                        best: np.ndarray[int64], n_cand: int, clusters: int)
@dataclass GStat(value: float, lo: float, hi: float, n: int, k: int,
                 garden: str, pool: str, widths: tuple[int, ...])
```

**`odybench/sky.py`** [r1 N12]

```
build(site: str, y0: int, y1: int, *, dt_model: str | float = "smh2020",
      refraction: bool = False, bodies=BODIES, stars=GRAMMAR_STARS,
      columns: tuple[str, ...] | None = None, workers=14,
      out_dir="data/cache") -> Path
load(path) -> SkyTable        # NPZ, n = number of LMT civil days y0-01-01 .. y1-12-31
```

- **The ΔT argument.** A float `dt_model` is a constant ΔT in seconds. That
  is T0b's clock (27,602.7 s).
- **Refraction.** `refraction=True` adds standard refraction for T0b's M
  sensitivity. The default is airless, as in the S2 reproduction.
- **SkyTable arrays** (nb bodies, ns stars, n days):

  | arrays | type | content |
  |---|---|---|
  | `jdn` | i8[n] | civil day |
  | `jd0_ut` | f8[n] | local midnight |
  | `rise_ut`, `set_ut` | f8[nb, n] | NaN if there is none that day |
  | `rise_az`, `set_az` | f8[nb, n] | azimuth from north through east; f8 because Mercury's rise-azimuth maxima are resolved to 0.0001° |
  | `sun_alt_at_rise`, `sun_alt_at_set`, `mag_at_rise`, `mag_at_set` | f4[nb, n] | |
  | `elong`, `lat_ecl` | f4[nb, n] | at local midnight; signed elongation, east positive |
  | `lon_ecl` | f8[nb, n] | at local midnight; apparent of date, geocentric |
  | `twl_eve_ut`, `twl_morn_ut` | f8[3, n] | Sun at −6°, −12° and −18° |
  | `star_alt_eve12`, `star_alt_morn12` | f4[ns, n] | |
  | `star_rise_ut`, `star_set_ut` | f8[ns, n] | |
  | `sun_alt_at_star_rise`, `sun_alt_at_star_set` | f4[ns, n] | |
  | `moon_frac_midnight`, `moon_up_frac_dark`, `night_len_h` | f4[n] | |
  | `meta` | JSON string | site, ΔT model, ephemeris file hashes, h0 values, refraction flag, code tree hash |

- **Rise** is the topocentric altitude of the centre crossing h0 = −0.8333°
  (Sun, Moon) or −0.5667° (planets, stars). It is found by Meeus' iterated
  hour angle and bisected to 0.1 s for Mercury and to 1 s otherwise.
- **Ephemerides.** Lunar quantities use DE431 and SMH2020 ΔT, in yearly
  chunks that never straddle JD 1721425.5. Planets and stars use DE441.
- **Size.** Every column over the full margins (−2060..+241, 840,000 days)
  takes about 0.9 GB. Only Ithaki is built so. Every other site has the span
  and column set of `sites.json` [r1 N12 fix 3].

**`odybench/events.py`**

```
conjunctions(jd_tt0, jd_tt1, ephemeris="de431") -> f8[k]      # yearly chunks; "de441" for T0b
full_moons(jd_tt0, jd_tt1, ephemeris="de431") -> f8[k]
stations(body, jd_tt0, jd_tt1) -> rec[("jd_tt","f8"), ("kind","U1")]   # R, D
greatest_elongations(body, jd_tt0, jd_tt1, sun="true"|"mean")
    -> rec[("jd_tt","f8"), ("side","U1"), ("elong","f8")]
oppositions(body, jd_tt0, jd_tt1, sun="true"|"mean") -> f8[k]
azimuth_extrema(sky, body, which="rise"|"set")
    -> rec[("jd_ut","f8"), ("kind","U3"), ("az","f8"), ("curv","f8"),
           ("margin","f8"), ("flat","?")]                      # parabola vertex, 7 days
visibility(sky, body, side, av: float | "plsv", crit_alt=0.0) -> bool[n]
star_phases(sky, star, av) -> rec per year: heliacal rising and setting,
    acronychal rising, cosmical setting (JDN)
season_bounds(sky, h_A, h_P) -> rec per year: A(y), P(y) (JDN)   # C_rel
equinoxes(jd_tt0, jd_tt1) -> rec[("jd_tt","f8"), ("kind","U2")]  # VE AE SS WS
first_crescent(sky, conj_jd_tt, criterion="yallop_B") -> i8     # JDN of the evening
```

**`odybench/deltat_mix.py`** (the four-model mixture, 0 and 6.3.3)

```
grid(jd_tt, frame="canon"|"de431", n=41) -> (dt_s: f8[4, n], w: f8[4, n])  # ±4σ per model, Gaussian weights, models equal
p_pass(fn: Callable[[float], bool], jd_tt, frame, sigma_scale=1.0) -> float
```

**`odybench/eclipses.py`**

```
catalogue(y0=-1999, y1=300) -> rec[idx, jd_td, dt_canon, gamma, type, saros, file, row]
local(ecl, lat, lon, dt_s, elev_m=0.0) -> dict(smag, obsc, central, duration_s,
      t_max_ut, sun_alt, lat_h, c1_ut, c2_ut, c3_ut, c4_ut)
totality_window(ecl, lat, lon) -> (dt_lo, dt_hi) | None      # canon frame
hit_strength(ecl, site, models=DT_MODELS, frame="canon", sigma_scale=1.0)
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
load_controls_real() / load_controls_almagest(regime="SL"|"BM") / load_negatives()
      -> list[ClueSet]     # through operational_map.json and almagest_regimes.json; unknown key -> error
load_odyssey() -> (ClueSet, garden)                           # readings.json, garden.json
evaluate(pred: Predicate, pool, ctx) -> bool[len(pool)]       # dt_rule applied inside
evaluate_p(pred: Predicate, pool, ctx) -> f8[len(pool)]       # P_mix(pass), for reports
evaluate_rows(clueset, reading, pool, ctx) -> bool[n_rows, len(pool)]
search(clueset, reading, window: (jd0, jd1), ctx, scoring="strict"|"bestfit")
      -> SearchResult
make_redraft_brief(rows=("T1-DARK","T2-SEASON","T-INT-12","D-ECL","L4-DARK"))
      -> writes data/prereg/pcr_redraft_brief.json             # tools/make_redraft_brief.py
```

`prereg_io` refuses any path that matches `*_truth*` (I13). `ctx` holds the
sky tables, event lists and catalogues for the sites a clue set names.

**`odybench/pools.py`, `readings.py`, `reach.py`, `evidence.py`**

```
pools.targets(kind="T"|"T_C"|"T_A"|"T_A_E5", site="ithaki") -> rec[POOL_DTYPE]
pools.slot_A(pool, ctx) -> bool[len(pool)]                    # 4.2's Venus and Mercury slots
readings.garden(tier="BM"|"DOC"|"FULL", equinox=False, eclipse_compatible=False)
      -> Iterator[Reading]                                     # equinox=False: the rule gardens (F6 off)
readings.pinned(name) -> Reading        # "T0b", "BM", "R_anc", "R_anc_noecl"
readings.survivors(garden, pool, ctx) -> Iterator[(reading_index, f8[k] survivor JD_TT)]
reach.interval(t, s_prev, s_next, W_days) -> (lo, hi)         # empty if lo >= hi
reach.reach(targets: f8[m], survivor_sets, W_days) -> f8[m]   # |union| / W
reach.G(reach_values: f8[n], garden, pool, widths) -> GStat   # gamma interval of 5.3
reach.p_at_least_one(survivors, W_days, b0, b1, step_days=365.25) -> (empirical, poisson, mean)
evidence.bf(t_S, garden, pool, ctx, rho: float | dict) -> dict(bf, bf_max, p_r: f8[R], passes: bool[R])
evidence.lr_slot(garden, pool_TC, nu) -> dict(R_obs, G, P_A, P_wA, lr)   # exact reweighting, 5.7
```

Survivor sets are packed bit masks (uint64[ceil(n_pool/64)]) per option,
ANDed per reading in batches. A reading whose largest survivor gap is below
W contributes no reach and is skipped.

**`odybench/epic.py`, `pcs.py`, `harness.py`, `verdict_rule.py`, `prereg.py`**

```
epic.draw(n, variant, seed) -> list[ClueSet]
epic.garden_for(clueset, tier) -> list[Reading]
epic.enters(clueset, t_S, ctx) -> bool                        # categorical slots hold at Schoch's target (5.4)
pcs.instrument(truths, path="standish"|"horizons") -> list[ClueSet]
pcs.science(truths, nu, garden, ctx) -> rec per truth: recall per reading, reach, description
harness.place_window(set_id, width_years, k) -> (jd0, jd1)     # the only reader of truth_index.json
harness.score(set_id, result: SearchResult) -> dict(seen, strict_recall, f_truth, rank, resolution)
harness.exposure_audit(file="controls_real") -> list[dict(row, sibling, params, fails)]
verdict_rule.decide(q: dict, thresholds: dict) -> (set[str], set[str])
verdict_rule.check_structure(q: dict, n: dict) -> list[str]    # violated constraints of 9.4; [] if realisable
prereg.check_frozen() -> dict(commit, tree_hash, amendment)     # raises unless frozen
```

### 10.3 Canonical predicates and the translation of the prereg files

Three agents drafted the three prereg files, in three vocabularies.
`controls_real.json` and `controls_almagest.json` have machine-readable
`operational` dicts, while `negatives.json` has prose [pcr §5 item 2; lca
next-stage item 2; neg]. All three are translated into one set of canonical
predicates.

| type | parameters | used for |
|---|---|---|
| `anchor` | rule: conj_ut2, conj_lmt, conj_plus1, first_crescent, full_moon, day7, any_day, solar_eclipse, lunar_eclipse | Day 0 (F2; epics; controls) |
| `moon_phase` | class, tolerance (days) | phase rows. Classes are frozen by the Sun–Moon elongation E (east +): young crescent 0° < E ≤ 45°; waxing crescent 0° < E < 90°; first quarter \|E − 90°\| ≤ 12.2° × tol; near full 150°–210°; full \|E − 180°\| ≤ 12.2° × k; last quarter \|E − 270°\| ≤ 12.2° × tol; waning crescent 270° < E < 360° [me] |
| `moon_up` | interval of named instants, illuminated-fraction bounds, quantifier | negatives, PC-R |
| `moon_dark_share` | maximum share of the dark hours with the Moon up | H2 |
| `rise_lead`, `set_lag` | body, minutes | V; ALM visible_only (minutes between horizon crossings); `bm_venus_lead` |
| `visible` | body, side, AV (degrees or PLSV), critical altitude | F4, F5, H3, H5, the slots of T_A |
| `alt_at` | body or star, named instant, minimum altitude | ALM visible_before_sunrise (civil dawn), negatives |
| `turning_point` | body; event (greatest elongation from the true or mean Sun; station; rise- or set-azimuth extremum; first or last visibility; opposition to the true or mean Sun); side; k days (continuous); visibility required; displacement | M; ALM (`ge_true_k`, `ge_mean_k`, `bm_mwra_k`, `opp_*`); epics |
| `ge_relation` | body, side, before or after, j days or `same_apparition` | ALM A.1, B.1, I.1, J.4 |
| `star_covis` | stars, minimum altitude, twilight, span of nights, quantifier; or a season window (C_rel, autumn) | C; F3; epics |
| `star_phase` | star, phase, AV, k days | epics; negatives; R_anc's season bound |
| `rel_position` | body, reference (star, line through two stars, Moon's centre), offset or distance, tolerance, frame | ALM star and Moon rows; one branch per star candidate for F.4 |
| `sun_lon` | range (wrapping through 0°) | seasons in PC-R, R_anc |
| `equinox_offset` | event, offset range in days | E_rel; ALM-E.3 |
| `solar_eclipse` | smag range, central flag, minimum h_tot/h_09/h_06, timing (LAT of maximum, first contact after noon, last contact with the Sun up), site rule; `x_class` ∈ {X3, X4, X1–X4} mapped as in 6.3.3 and 6.5 | X; PC-R; negatives |
| `lunar_eclipse` | umag and pmag ranges, the Moon's latitude sign, timing (mid-eclipse offset from LAT midnight, first contact after moonrise, overlap or containment in seasonal night hours or a night quarter), the Moon's altitude at contacts, moonrise during the umbral phase at a site rule | PC-R; ALM-C |
| `interval` | from event, to event: exact nights, day range, or years ± tolerance | links |
| `calendar` | Egyptian (free epoch), Roman (named date, offset bound or free), Attic (month, lunation offset), report bounds | PC-R |
| `night_length`, `separation`, `herald`, `crescent`, `rise_azimuth` | as named | H1, H4, F4, F2(d), AEN-TROY's Ida rider |

**Translation rules.**

- **The two controls files.** Their keys map to these types by fixed rules
  in `prereg_io.py`. Their free-text values (relation strings such as
  "umbral phase overlaps hour", site names such as "Tigris camp") are listed
  in `operational_map.json`. An unknown key or value is an error, never a
  default.
- **The negatives.** Each `negatives.json` option gets a full canonical
  predicate in `operational_map.json`, drafted by A3 and checked against its
  prose by A9 (I13).
- **ΔT-dependent predicates** pass when P_mix ≥ 0.5 (`dt_rule="mixture_p50"`),
  with 0.05 and 0.95 as reported sensitivities (6.3.3).

### 10.4 Independent second implementations

Issue 13 asked which code paths get an independent check, against what, and
at what tolerance. Every derived quantity the verdict rests on has one:

| code path | independent implementation | cross-check | tolerance | check |
|---|---|---|---|---|
| `sky.py` rise and set | JPL Horizons rise/transit/set; the grid-plus-bisection finder of `results/critique-design/check_mwra.py` | 1,000 events; 2,000 events | 0.5 min; 0.1 s | I5 |
| `events.py` stations, greatest elongations, azimuth extrema | `results/bm2008-reconcile/check_mwra.py`; the Standish code of `results/bm2008-b-checks/` | 152 S2 years; 500 events | same civil date in ≥ 150/152 and 0.05 d; 1 d | I6 |
| `events.py` heliacal phases, B&M's spring limits, Arcturus' rising | `docs/research_visibility_calc.py`; `results/design-revision-r2/ranc_season.py` | −1177, −700, −1130 | 1 d | I6 |
| `events.py` first crescent | the Yallop code of `research_visibility_calc.py` | 500 lunations | ≥ 495 equal | I12 |
| `eclipses.py` | NASA's `program.js` in Node (`data/jsex/sites/`); `results/critique-design/check_bessel.py` | 5 sites × 5,486; four totality windows | smag 0.0005, 0.002 h; 5 s | I2 |
| `lunar.py` | NASA LEcat5 | the PC-R and ALM centuries, plus 300 random | 0.02; 3 min | I4 |
| `deltat_mix.py` | `ephem.delta_t` and `ephem.delta_t_sigma` evaluated directly, and a 10⁶-draw Monte Carlo of the mixture | P(total) for 1178 and 1131 BC on NASA's elements against the 2.3 table | 0.005 | I2 (added row) |
| the B&M reading through `clues.py`, `readings.py`, `search.py` | `tests/bm_reference.py` (A7) | every T0 cell; 300 random years | identical flags | I7 |
| `reach.py` reach | brute-force sliding windows | 10,000 synthetic sets | 0.0002 | I9(a) |
| `reach.G` interval | simulation of coverage | 10,000 reach vectors per cell | coverage ≥ 0.95 | I9(b) |
| `pools.py` and `readings.py` together | the identity G(𝒢_BM*, T) = (n_A/n_T) G(𝒢_BM*, T_A) | the real tables | exact | I9(c) |
| the PC-S generator | Standish code; Horizons subsample | 200 truths (50 via Horizons) | recall 1.000 | I10 |
| `evidence.lr_slot` | end-to-end simulation in `pcs.science` | 2,000 truths per noise cell | within the simulation interval | I10b |
| `calendar.py` | exhaustive day counting; the Horizons calendar | −1999..+500 | exact | I8 (done) |
| `prereg_io.py` | the licence checkers' dump scripts; A9's review; the brief's leak scan | every row | exact | I13 |
| `verdict_rule.py` | the hand-computed synthetic sets; the structural constraints | 12 sets; 6 constraints | exact | I14 |

### 10.5 Scripts (top level, as in labench)

| script | test | writes |
|---|---|---|
| `reproduce.py` | T0a, T0b, T0c | `results/t0/` |
| `rates.py` | N1 | `results/n1/` |
| `coincidence.py` | N2 | `results/n2/` |
| `garden.py` | N3, R_anc, the evidential findings of 5.7 | `results/n3/` |
| `randomepic.py` | N4 | `results/n4/` |
| `windows.py` | N5 | `results/n5/` |
| `deltat.py` | N6 | `results/n6/` |
| `synthetic.py` | PC-S (both modes) | `results/pcs/` |
| `controls.py` | I2b, PC-R, the exposure audit | `results/pcr/` |
| `almagest.py` | the *Almagest* control and its Bayes factors | `results/alm/` |
| `negatives.py` | the negatives, the Iliad comparison, I11 | `results/nc/` |
| `heldout.py` | section 7 | `results/heldout/` |
| `verdict.py` | section 9 | `results/VERDICT.md`, then the findings in `README.md` |
| `read.py` | a reader: `py read.py -1177-04-16` prints the sky of Days −40 to +1 beside each clue and held-out predicate, as labench's `read.py` prints a tablet | stdout |

Every script writes three kinds of output, each stamped with the commit and
code tree hash it ran under:

- a machine-readable `<name>.json`;
- a human-readable `<name>.out.txt`;
- `.tsv` tables, where useful.

**Tools.**

- New: `tools/fetch_ephem.py` (extended to +300), `tools/fetch_lecat.py`,
  `tools/fetch_horizons_rts.py`, `tools/build_sky.py`,
  `tools/build_events.py`, `tools/build_eclipses.py`,
  `tools/build_truth_index.py`, `tools/make_redraft_brief.py`,
  `tools/validate_events.py`, `tools/validate_eclipses.py`,
  `tools/freeze.py`.
- Existing: `validate_ephem.py`, `validate_coverage.py`, `fetch_jsex.py`,
  `jsex_sites.js`, `fetch_stars.py`.

**Tests**, each runnable as `py tests/test_x.py`:

| test | covers |
|---|---|
| `test_calendar.py`, `test_ephem.py` | exist |
| `test_t0.py` | S2 replay, A1–A5 |
| `test_reach.py` | I9 |
| `test_clues.py` | hand-built predicate cases, and the B&M reading on S2's rows |
| `bm_reference.py` | I7 |
| `test_eclipses.py` | I2 |
| `test_lunar.py` | I4 |
| `test_events.py` | I5, I6, I12 |
| `test_prereg_io.py` | I13 |
| `test_verdict.py` | I14 |

---

## 11. Data, run order and run times

### 11.1 Data still to acquire

| what | from | size | why |
|---|---|---|---|
| DE441 excerpt +241..+300, the same 11 bodies | NAIF `de441_part-1.bsp` by HTTP Range (`tools/fetch_ephem.py`) | about 6 MB [me: 238 MB per 2,301 years, scaled] | *Almagest* and PC-R windows reach +277 (4.1); the current excerpt ends at +241 [acq §1.1] |
| DE431 Sun, EMB, Earth, Moon +241..+300 | NAIF `de431_part-2.bsp` | about 4 MB [me: 17.7 MB per 240 years, scaled] | lunar-timed quantities for the same windows |
| NASA LEcat5 century pages −1999..+300 | eclipse.gsfc.nasa.gov/LEcat5 (`tools/fetch_lecat.py`) | about 23 × 60 kB; 10 are already in `results/controls/nasa/` | I4 |
| Horizons rise/transit/set for 1,000 events; positions for 50 PC-S truths | Horizons API (`tools/fetch_horizons_rts.py`), cached in `data/ephem/horizons/` with the request URL on line 1 | small | I5, I10 |
| the *Almagest* reference stars (δ Cap, β and ζ Tau, Castor, Pollux, ζ Gem, Spica, Regulus, Antares, α Lib, β and δ Sco, β, γ and η Vir, δ Cnc, λ, φ and ψ1–3 Aqr, the Pleiades) | `tools/fetch_stars.py` (SIMBAD identifiers and hip2 rows, as in [acq §3]). The drafter fetched them for its own run into `results/controls-almagest/stars.json`, in memory only [alm §1.5] | small | the full primary run of 6.4 (the gate's projection does not use them) |
| SMH2016's full text with Table S4, and the 2020 Addendum's tables | the Royal Society and PMC pages (open access) | small | `deltat_circular.json` (6.3.3), read by A11 |

Fetch with Python urllib or the PowerShell tool. Git Bash's curl carries a
2020 CA bundle, so an HTTPS failure there is local. There is no library
access beyond `py -m odybench.ccx`. Every new file's SHA-256 goes into
`data/SHA256SUMS`. The background of 4.1 needs no new data.

### 11.2 Run order and expected times

Measured on this machine (16 logical cores) [v1 §7.5; acq §1.3]:

- `ephem.altaz` runs at about 28,000–29,000 body-positions a second per
  core;
- `ephem.new_moons` takes 23.0 s per 136 years;
- `validate_ephem.py` takes 118–188 s.

The other figures are estimates from these.

| # | step | command | estimate | basis |
|---|---|---|---|---|
| 0 | fetch | `py tools/fetch_ephem.py`, `py tools/fetch_lecat.py`, `py tools/fetch_horizons_rts.py` | 10–20 min | network |
| 1 | build code; unit tests | agents (10.1) | — | |
| 2 | sky tables, events, catalogues (needed by the pre-freeze checks) | `py tools/build_sky.py --all`; `py tools/build_events.py`; `py tools/build_eclipses.py` | **3–5 h, once** [r1 N12] | about 310 evaluations a day for a full-column site (7 bodies × 2 events × about 4 iterations; 6 twilights; **21 stars × 2 events × about 4**; star altitudes; Moon). Ithaki over 840,000 days is about 260 million evaluations: 2.5 h on one core, about 12 min on 14. About 10 negative-control sites at a third of the columns, over the background, take about 40 min on 14 cores; the control sites take their windows only. Eclipses: 5,486 × about 55 sites (36 rotated) with totality bisections, under the mixture grid. Disk: about 0.9 GB for Ithaki and 4–5 GB in all in `data/cache/` |
| 3 | pre-freeze instrument checks I1–I6, I8, I9(a, b), I12–I14 | `py tools/validate_ephem.py`; `py tools/validate_events.py`; `py tools/validate_eclipses.py`; `py tests/test_*.py` | 30–60 min | |
| 4 | pre-freeze tasks: the re-draft brief, then the re-draft (6.3.4), then I2b; the negatives' second reading (6.5); the review of `operational_map.json`; `deltat_circular.json` (6.3.3); `almagest_regimes.json` (6.4); the builders retired (12.1) | agents | — | |
| 5 | **freeze** | `py tools/freeze.py` | seconds | section 12 |
| 6 | post-freeze instrument checks I7, I9(c), I10, I10b, I11 | `py tests/bm_reference.py`; `py garden.py --identity`; `py synthetic.py --instrument`; `py negatives.py --plumbing` | 20 min | |
| 7 | T0 | `py reproduce.py` | 5 min | |
| 8 | N1, N2, N5 | `py rates.py`; `py coincidence.py`; `py windows.py` | 10–20 min | lookups on cached tables, over a background 1.6 times longer |
| 9 | N6 | `py deltat.py` | 20–40 min | about 45 totality windows on DE431 |
| 10 | N3, R_anc and the evidential findings | `py garden.py` | 1–3 h | 𝒢_FULL* (767,232 readings) and the reported E-on gardens (up to 3.07 million) × about 27,000 candidates, as packed bit ANDs on 14 workers with the gap test of 10.2 |
| 11 | N4 | `py randomepic.py` | 30–60 min | 20,000 epics; stratum epic gardens |
| 12 | PC-S science mode | `py synthetic.py` | 20–40 min | 2,000 truths × 12 noise cells × the BM and DOC tolerance forks |
| 13 | PC-R and the *Almagest* control | `py controls.py`; `py almagest.py` | 30–60 min | 21 windows per set; site "none" grids; the mixture grid |
| 14 | negatives | `py negatives.py` | 20–40 min | 13 sets × gardens × 2 windows (plus 40 sensitivity windows) |
| 15 | held-out | `py heldout.py` | 5 min | |
| 16 | verdict | `py verdict.py` | seconds | |

After the freeze, about 5–9 hours of computation remain, most of it in steps
10–14. Step 2 is cached and runs once.

---

## 12. Freezing and amendments

Revision 1 hashed only `DESIGN.md` and `data/prereg/`, on a machine with no
version control, and it let every script run unfrozen. Nothing covered the
code, and nothing could refute a charge that thresholds or code had changed
after the results came in [rev #4]. The freeze is now a local git commit.
The recheck found this resolved [r1 §1, #4]. Revision 3 changes only the
list of files.

### 12.1 Before the freeze (all must hold)

1. Every module of 10.2 exists and its unit tests pass.
2. The pre-freeze instrument checks I1–I6, I8, I9(a, b), I12, I13 and I14
   pass (6.1).
3. **The re-draft** (6.3.4) is done, in order:
   - `tools/make_redraft_brief.py` has written
     `data/prereg/pcr_redraft_brief.json`, and I13(e) has passed on it;
   - the unexposed re-drafter has written `data/prereg/pcr_redraft.json`;
   - I2b has run after that, because I2b computes local magnitudes at the
     truth dates and must not run before the re-draft exists.
4. **The negatives' second reading** (6.5) is done. Its re-pinned readings
   and the X-class decision are in `negatives.json` and
   `operational_map.json` as recorded edits: a script that rebuilds from the
   licence-checked copy, like the licence checkers' own.
5. `data/prereg/operational_map.json` is complete and reviewed (I13).
6. **`data/prereg/deltat_circular.json`** lists every control eclipse used in
   SMH2016's and the 2020 Addendum's fits, with page locators (6.3.3).
7. **`data/prereg/almagest_regimes.json`** names the option and parameter
   values of both regimes for every projected row, with the
   leave-one-set-out arithmetic shown (6.4). It reproduces the known
   consequences of 2.6 (R9, R10).
8. **The three builders are retired.** Each would silently undo the licence
   checks' edits if re-run [lcr; lca; lcn §4.1]:
   - `results/controls-real-drafting/build_controls_real.py`;
   - `results/controls-almagest/build_prereg.py`;
   - `results/negatives/build_negatives.py`.

   The frozen JSON files are the record. The builders are kept for
   provenance and marked "do not re-run" in their first line by their owners
   or, failing that, listed here as retired. `tools/freeze.py` refuses to
   freeze if any of the three clue files differs from the output of its
   recorded edit scripts: the licence checkers' replays from their saved
   pre-edit copies, followed, for the negatives, by the second reader's
   script.
9. The new prereg files exist: `sites.json`, `windows.json`, `seeds.json`,
   `deltat_models.json`, `readings.json`, `garden.json`, `epic_grammar.json`,
   `heldout.json`, `eclipse_hit.json`, `verdict_rule.json`,
   `verdict_synthetic/`, `operational_map.json`, `pcr_redraft_brief.json`,
   `pcr_redraft.json`, `almagest_regimes.json`, `deltat_circular.json`,
   `truth_index.json`, `i2b_reference.json`.
10. `data/SHA256SUMS` is extended to every file in `data/text/` and
    `data/refs/`, and to the new ephemeris and catalogue files.
11. `tools/freeze.py` evaluates constraint C6 of 9.4 with the measured pool
    sizes. n_A and n_T are counts of targets from the sky tables and the
    slot definitions alone. No reach, survivor set or G is computed before
    the freeze. It refuses to freeze if outcome 1 is unattainable [r1 N1 fix
    3]. With the estimates of 2.8 it is attainable (U0(139) = 0.0265).

### 12.2 The repository

- **Where.** `git init` in `C:\Projects\odybench` makes a local repository
  with no remote. Commits use the machine's existing git identity, and
  nothing is pushed.
- **Committed:**
  - `DESIGN.md`, `docs/`, `odybench/`, `tools/`, `tests/` and the top-level
    scripts;
  - `data/prereg/`, truth files included. The searcher's isolation is
    enforced by code and test, not by hiding files;
  - `data/stars.json` and `data/SHA256SUMS`;
  - the scripts in `results/` with their own text outputs, which record
    what was known before the freeze.
- **Hashed, not committed** (listed in `data/SHA256SUMS`):
  - the ephemeris `.bsp` files and `data/jsex/`;
  - `data/text/*.tsv`, exported from Jon's library, some of them in
    copyright;
  - `data/refs/` (PDFs and their extracted text) and `data/cache/`;
  - every large binary in `results/`;
  - every copy of a publication kept in `results/`. Examples are the
    extracted texts `results/data-acquisition/bond2017.txt` and
    `results/controls-real-drafting/gautschy-eclipsecitations.txt`, and the
    PDFs and HTML in `results/unread-primaries/`.

  Nothing copyrighted enters the repository, so a later decision to publish
  it cannot publish a text by accident.

### 12.3 The freeze

`tools/freeze.py`, run on a clean working tree:

1. checks every hash in `data/SHA256SUMS` and the conditions of 12.1;
2. commits everything listed above as the **freeze commit**, and tags it
   `prereg-1`;
3. writes `PREREG.sha256` at the repository root. It holds:
   - the freeze commit hash;
   - the git tree hashes of `odybench/`, `tools/`, `tests/` and
     `data/prereg/` at that commit (`git rev-parse prereg-1:odybench` and so
     on);
   - the blob hashes of `DESIGN.md` and of each top-level script;
   - a git-independent **code tree hash**: the SHA-256 of the sorted lines
     "`<sha256>  <path>`" over every file in `odybench/`, `tools/`, `tests/`,
     `data/prereg/`, `DESIGN.md` and the top-level scripts;
4. commits `PREREG.sha256` alone in the next commit, because a file cannot
   hold the hash of the commit that contains it.

Every analysis script calls `prereg.check_frozen()` at start. HEAD must
descend from `prereg-1`, the working tree must be clean, and the current
code tree hash must equal the frozen one or the latest amendment's.
Otherwise the script stops. `--unfrozen` lets it run, but it stamps every
output EXPLORATORY in its first line, and `verdict.py` refuses to read such
outputs.

### 12.4 Amendments

A change to any frozen file after the freeze, code included, is allowed only
as a dated amendment appended to 12.6 below. The amendment states:

- what changed;
- why;
- the hash of the diff;
- **which outputs had already been read** when it was made, in the way
  indusbench recorded its correction to test 1 [indusbench DESIGN §4].

The amendment is committed, and its new code tree hash is appended to
`PREREG.sha256` under the old lines, so the file keeps the whole history.

The clue files' own histories are recorded the same way:

- `controls_real.json` was drafted and frozen before any accepted date was
  looked up (`eb1f0401…9256`), then licence-checked by an agent blind to the
  truth (`135fba67…83f8`) [lcr];
- `controls_almagest.json` was licence-checked from the pre-edit file
  `e16c559d…37e9` [lca], and the checked file is `758ee789…4c83` (hashed
  for this revision, 2026-10-04 [me]);
- `negatives.json` was licence-checked from the copy in
  `results/license-check-negatives/negatives.before.json` [lcn], and the
  checked file is `f4ae3b26…bb00` [me].

These are the hashes as of this revision. If the pre-freeze tasks of 12.1
(the negatives' second reading) change a file, `freeze.py` records the new
hash with the script that made the change.

### 12.5 Publishing the hash

Publishing the hash outside the machine would give an outside timestamp. Two
ways to do it are a public commit or gist under the research identity Jon
uses for open work, and an OpenTimestamps proof of `PREREG.sha256`.
Publishing is **optional and needs Jon's explicit permission**, and the
bench does not assume it. Until he gives it, the freeze is verifiable only
on this machine, and `VERDICT.md` says so in its first lines.

### 12.6 Amendments made after the freeze

None yet.

---

## 13. What the dossier could not settle, and how each is handled

| # | open fact | why it is open | handling |
|---|---|---|---|
| 1 | What "Ti = New Moon" means operationally | no single rule reproduces S2's Ti column [bm §5 N] | T0b pins the UT+2 conjunction date (136/152); F2 carries LMT, +1 day and first crescent |
| 2 | Which New Moon when two qualify; S2's out-of-window Ti | S2 follows no consistent rule [bm §7] | T0b evaluates every qualifying New Moon; T0a replays S2 as printed |
| 3 | Why 14 S2 MWRA dates sit 4–8 days from DE441's maxima | Starry Night's Mercury theory, another horizon, or plot reading [bm §5 M] | DE441 vertex maxima are used; the integer replay is a regression check (A3) |
| 4 | Mercury's visibility on Ti−34 | never tabulated; **PLSV has no extinction model** (settled [unread §6]) | visibility off, AV 10°, and PLSV's AV formula at a 1° critical altitude, all in the T0 grid; a physical extinction model is an upgrade, not a prerequisite |
| 5 | The Pleiades and Arcturus cut-offs (17 Feb; 3, 4 or 5 Apr) | three dates in the paper and SI [bm §5 C] | T0b uses 17 Feb and 4 Apr; C_rel is calibrated to them at −1177; F3 carries 2°, 5°, autumn and none |
| 6 | The ṅ and ΔT formula of Starry Night 6.0.4 | unpublished; two published Starry Night values cannot come from one smooth ΔT(t) [unread §7] | 27,602.7 s is the T0b clock only and is never converted |
| 7 | ΔT at −1177 | SMH's own formulations span 681 s; every value before −720 is extrapolation [eph §8] | four models and their mixture, each σ taken as Gaussian (an assumption, stated) |
| 8 | The lunar ephemeris to pair with SMH | DE441's tidal model is unpublished; DE441 − DE431 = +188 s at −1177 [eph §5.3] | lunar-timed quantities on DE431, planets on DE441 (section 0) |
| 9 | Which island is Homeric Ithaca | modern dispute | Ithaki primary; four sensitivity sites; Paliki dropped (section 0) |
| 10 | Lefkada's coordinates | 20.70 in the site catalogue, 20.71 in research-ephemeris [acq §6 item 5] | 20.70 adopted (section 0) |
| 11 | The departure hour from Ogygia; Athena's night in Sparta | the Greek does not say [chron §4.B, §4.F] | F1's grid; F1b for the typical numbers |
| 12 | What Day 0 is; Apollo's feast on the new moon or the 7th | the text is silent; ancient sources split [txt §5.1, §5.3] | F2 (a)–(d); the 7th as an epic anchor in N4 |
| 13 | The Greek day boundary | not verified from a primary source [vis §6 item 4] | F2 (d) uses a sunset day, (c) a civil day |
| 14 | The meaning of "late-setting" Boötes | late, slow, or Aratus' autumn evenings [txt §5.8; vis §3.1] | F3 (a′)–(f) |
| 15 | Whether the morning star is Venus | Homer's names are separate [vis §1.4] | F4 includes any bright herald and none |
| 16 | The equinox bound | ≤ 4 Apr (§Intersecting), ≤ 5 Apr (§References), XXX = ≤ 6 Apr (S2) [bm §5 E; rev #23] | the T0 grid carries all three. **E is left out of every rule garden**, because its reading was formed with the target in view (5.3) |
| 17 | The window | text 1250–1115 BC, S2 1251–1100 BC; drawn from the tradition that chose the eclipse [bm §6; win §6] | the reproduction window as stated; N5 runs five; G_any is reported beside G |
| 18 | Which three lines schol. 14.162 suspects | commentaries not available [txt §10] | every result is conditional on 14.162 = 19.307 being read as a month-turn at all |
| 19 | Primary sources | **Read**: MacDonald 1967 (pp. 324–327), Papamarinopoulos et al. 2012, Henriksson 2012, the PLSV 3.1 documentation, Neugebauer & Schoch 1927 [unread §1]. **Still unread**: P. V. Neugebauer 1929 (paywalled; Jon could open the HathiTrust record himself); Schoch's *Die Sterne* 6:88 and *Dichter-Finsternisse*; P.Oxy. 3710 (papyri.info needs Jon's approval for the browser); Austin 1975; de Jong 2001 App. A; Stanford 1959; the Oxford commentaries; Starry Night internals | no computed number depends on them. MacDonald's March reading is documented as formed with the eclipse in view (1.1), which fixes the conditioning of 5.3 |
| 20 | Herwart von Hohenburg's 1612 date | known only through Fotheringham 1921 [crit §1.2] | historical note only |
| 21 | Arcus visionis models are crude | AV bands stand in for extinction; weather moves first and last dates by ±3 to ±15 d [vis §1.2, §6] | AV values are forks; the slack of real observers is measured on the *Almagest* (6.4) |
| 22 | Correlated ΔT errors of 1178 and 1131 BC | 47 years apart [win §7.1] | joint probabilities under a common offset (R7) |
| 23 | The prior for oral transmission of a dated sky | no comparative case [win §10–11] | not quantified; no likelihood ratio or Bayes factor is multiplied by a prior |
| 24 | Ephemeris coverage | settled to +241 [acq §1]; the controls need +300 | fetched in step 0 (11.1) |
| 25 | Ancient Troy dates | known through B&M, Wikipedia and Clement's list as reported by Papamarinopoulos et al. [win §3, §12; unread §4], not from FGrHist | used only for the primary window's envelope and H6; *secondary* |
| 26 | Hermes = Mercury, and whether any god-movement is astronomical | no ancient parallel before Plato [txt §5.9] | not adjudicated: F5 none; H3–H4 test the rule's consistency; the categorical reading is conditioned on (5.3) |
| 27 | ΔT σ before −2000; the σ discontinuity at −500 | extrapolation; Huber against MS2004 on NASA's page [acq §6 items 3–4] | no eclipse in the bench lies before −1999; the discontinuity is reported where a control sits near −500 |
| 28 | Sirius' orbit model | about 1′ at −1177 between the published and the re-referred proper motions [acq §3.3] | the published centre-of-mass motion is adopted; the re-referred one is a sensitivity; a photocentre motion is never used |
| 29 | The *Almagest* glosses and cruxes | the unit glosses (moon 0.5°, cubit 2°, finger 1/12°) and the star identifications are the drafter's; IX.7.11 and IX.9.4 are textual cruxes; Heiberg's apparatus and Toomer were not consulted [alm §6; lca] | crux intervals are forks (primary as printed); star rows are outside the gate's projection |
| 30 | Exposure of the PC-R drafter | the drafter had seen computed answers [pcr §1]; one unflagged row was found by the recheck [r1 N5] | an unexposed re-draft of five rows from a brief, and a sibling-convention audit (6.3.4); background knowledge of famous dates cannot be removed |
| 31 | Single words in the negatives | Eous (*Aen.* 3.588), vesper (VF 7.1), ἔκλιθεν (*Arg.* 3.1196), διχόμηνις (*Arg.* 1.1231); Servius and the Apollonius scholia are not in the library [neg §6 item 3] | forked, with none |
| 32 | The Meeus ch. 7 values in `test_calendar.py` | recalled, not read [acq §6 item 7] | each also agrees with exhaustive day counting and with Horizons, so a wrong one would fail |
| 33 | The accepted dates of the PC-R controls | taken from secondary sources: summaries of Toomer and Pedersen, Gautschy's citation list, NASA's historical-eclipse page. Toomer's translation was not consulted. Gautschy's "424 BC May 21" for Thuc. 4.52 is apparently a slip for 21 Mar [pcr problems] | the drafter also recomputed every accepted date; the harness uses `truth_index.json` built from the truth file; the report marks the sources *secondary* |
| 34 | Coordinates of the negatives' places | Wikipedia coordinates; Giresun Island for the Island of Ares and Cape Sideros for Salmonis are modern identifications; representative points stand in for regions [neg §6 item 4; lcn §4.5] | used as recorded; a gazetteer check (Pleiades) is a pre-freeze task for the second reader of 6.5; site sensitivity is not expected to matter for star phases |
| 35 | Numeric thresholds in the negatives that are the drafter's but not marked as such (±1 d, ±7 or ±15 d, 2° and 5° altitudes, fraction ≤ 0.25, 2–3 h) | operationalisations of stated features [lcn §4.3] | kept; listed by the second reader in `operational_map.json` with a "drafter's threshold" flag |
| 36 | Whether SMH's fits used the control eclipses | Table S10 v2020 lists −309 and −187; SMH2016 §2b(iv) names 431 and 394 BC (*secondary*); Table S4 and §4b unread [r1 N4, §4] | the mixture scores every control; Q_ΔT tests the circular sets with σ tripled; `deltat_circular.json` is a pre-freeze task (6.3.3) |
| 37 | The formula of the G interval | the Fay & Feuer (1997) gamma interval is given from memory | the implementer checks it against the paper; I9(b) checks its coverage by simulation |
| 38 | Stationarity over the 2,200-year background | precession moves the star season about 31 days against the equinox | P9 tests the rates; G is reported on each half of the core |
| 39 | The approximations behind P(A) = 0.154 | the recheck used a 3-minute rise grid and a declination-based rise-azimuth maximum, good to about 1 d at a 6-d tolerance [r1 §4] | the bench recomputes P(A) on its own tables (5.7); n_A is measured before the freeze (12.1 item 11) |
| 40 | The slot that defines "Hermes is Mercury" | its 6-d width comes from the *Almagest* slack | the slot defines a pool, not a test; gate 3b is calibrated leave-one-set-out, so no record both calibrates and validates the gate (6.4) |
| 41 | When the *Almagest* k_days list [1, 2, 3, 5, 7, 10, 16, 21] was written | its top value matches the measured Venus maximum; the note fixes only the set composition before the DE441 comparison [r1 §4; alm §3] | leave-one-set-out takes from the list only the smallest value at or above an out-of-set maximum, so the list's history affects the rounding and not the calibration |

---

## 14. Resolution of the reviews

Two tables follow. The first gives the 25 issues of `docs/critique-design.md`
(the review of revision 1), the second the 17 new issues of
`docs/critique-design-r1.md` (the recheck of revision 2). Each row gives the
resolution and the sections it changed. Where a resolution departs from the
reviewer's proposed fix, the row says why, marked **Departure**.

### 14.1 The review of revision 1 (`critique-design.md`)

The recheck found 20 of these resolved by revision 2. It found #1, #16, #17
and #18 unresolved for reasons new to revision 2, and #3 resolved only in
part [r1 §1]. Revision 3 resolves those five through the new issues of 14.2,
as the rows say.

| # | severity | resolution in revision 3 | sections |
|---|---|---|---|
| 1 | blocker | **Now resolved.** The rule is a pure function of named quantities (9.1–9.2), and every condition names its garden and its target pool. Revision 2's unreachable NC condition stays replaced by the calibrated percentile pct_N4. Revision 2's outcome 1 was still unreachable, because its likelihood ratio was capped near 6.5 [r1 N1]. Revision 3 removes every likelihood ratio from the rule. Outcome 1 rests on T0 = R, on G over T_A with its gamma upper bound, on pct_N4, on the gates and on the negatives. The background is extended so that the pool is large enough for the upper bound to fall below 0.05 (4.1, 2.8). Twelve synthetic sets reach every outcome, the inconclusive verdict, each qualifier and the instrument block. Each set is checked against the structural constraints of 9.4 (I14b), so what is proved reachable is an outcome and not a code branch. `freeze.py` and Q_attain test attainability with the measured pool sizes. **Departure** (kept from revision 2): the percentile is taken on the reach of Schoch's target rather than on G, because G of a text with few clues falls to 0 whether or not it is dated | 1.3, 4.1, 5.3, 5.4, 5.7, 9, 12.1 |
| 2 | blocker | Resolved in revision 2 and confirmed by the recheck. `controls_real.json` was rebuilt from the texts, frozen before any accepted date was looked up, and licence-checked blind. Revision 3 closes the subtler leaks the recheck found. An unflagged answer-dependent primary (T2-SEASON) and a near-edge tolerance (T-INT-12) are re-drafted from a brief and audited against their sibling conventions (6.3.4). The ΔT models that were fitted to control eclipses are tested by Q_ΔT (6.3.3). The *Almagest* tolerances are no longer set at the truth's own maxima (6.4) | 2.6, 6.3, 6.4 |
| 3 | blocker | **Now resolved.** Outcome 3 stays split into 3a (PC-R) and 3b (the *Almagest* control) [rev #3]. The recheck found that 3b could not fire and that Q_BM was undefined [r1 N2, N3]. Revision 3 sets the observer slack leave-one-set-out, so that every set is scored as held out. It names B&M's option rule, and it removes the definitional PC-S recall from the gate. What the truth-side slack already decides is stated in 2.6: truth is retained in 9 of 11 sets, and Q_BM holds. Only narrowing remains open (P25) | 1.3, 2.6, 6.2, 6.4, 9 |
| 4 | major | Resolved and confirmed. The freeze is a local git commit of the design, the prereg files and all code. `PREREG.sha256` holds the commit hash, the git tree hashes and a git-independent code tree hash. Amendments are dated and state which outputs had been read. Unfrozen runs are stamped and refused by the verdict. Publishing the hash outside the machine is optional and needs Jon's explicit permission (12.5). Revision 3 updates only the file lists | 12 |
| 5 | major | Resolved and confirmed. Section 1.1 says that the 6 years is the C ∧ E rate. The two comparisons are P4 (0.88 per century, E off) and P5 (0.048 printed, E on) | 1.1, 2.4, 5.1, 8 |
| 6 | major | Resolved and confirmed: MacDonald was read, and both p_fix figures are reported with the frozen reason. Revision 3 applies the same reason uniformly, to V, M and E as well as C [r1 N6] | 1.1, 2.5, 5.1, 5.3 |
| 7 | major | Resolved and confirmed. The gardens are nested, with sources per option. The rule gardens leave out E: 𝒢_BM* 36, 𝒢_DOC* 35,964 and 𝒢_FULL* 767,232 readings, with revision 2's sizes reported for the E-on gardens. The greedy smallest fork set is reported, now up to G ≥ 0.20 over T_A | 5.3 |
| 8 | major | Resolved and confirmed: fork F1b, PC-S jitter of 0–3 d, and the decay of reach and recall | 5.3, 6.2 |
| 9 | major | Resolved and confirmed: C_rel and E_rel outside T0b, and λ per century under both kinds of bound. P9 is restated for the longer background | 4.5, 5.1, 8 |
| 10 | major | Resolved and confirmed. Hit strength comes from the mixture; the target is excluded from its own base rate; a site-rotated rate is computed; Schoch's 10–12 h rule is reported. The background now reaches +200 | 4.1, 4.4, 5.2 |
| 11 | major | Resolved. Base rates are conditional on the reading, and H1 and H5 are not counted. Revision 3 counts H3 once [r1 N14] | 7 |
| 12 | major | Resolved. MWRA is a vertex fit, rises converge below 0.1 s, flat maxima are flagged, and sensitivities and I6 are added. Revision 3 makes ±1.5 d, B&M's integer tolerance as a continuous one, the primary test [r1 N13] | 2.2, 3.2, 3.5, 6.1 |
| 13 | major | Resolved and confirmed: every derived quantity has a second path (10.4). Revision 3 adds the coverage check of the G interval and the pool identity (I9b, c), the exact-against-simulated check of R_obs (I10b), and a Monte Carlo check of the ΔT mixture | 6.1, 10.4 |
| 14 | major | Resolved. PC-S has an instrument mode (I10, recall 1.000) and a science mode. Revision 3 removes the definitional science-mode recall from gate 3b [r1 N2]; science mode is now a noise study that feeds no rule | 6.2 |
| 15 | major | Resolved and confirmed. The Iliad is a same-tradition comparison. Twelve clean negatives were drafted and licence-checked. Random poems are the main negative. NC4 and NC5 became I11, and I11(a) is known to hold at Troy (2.6) | 2.6, 6.1, 6.5 |
| 16 | major | **Now resolved.** The recheck showed that any ratio R_obs/G on the fixed poem is bounded by 1/P(A), and that T_C holds about 480 targets, not thousands [r1 N1, N8]. Revision 3 states the identity and reports the ceiling as a finding (5.7, 2.8). It takes every likelihood ratio out of the rule, gives every G a gamma interval, enlarges the pool by extending the background, computes R_obs exactly with one reach definition on both sides, and calibrates the reported Bayes factor on the *Almagest*. **Departure:** the review asked for the LR to be defined on one event (done in revision 2) and to decide outcomes 1 and 2. Revision 3 keeps it out of the rule, because on a fixed poem every such ratio is set by the observation model, not by the Odyssey [r1 N1] | 2.8, 4.1, 5.3, 5.7, 9 |
| 17 | major | **Now resolved.** Everything computable from known numbers is in section 2 with its numbers. That includes revision 2's settled predictions P23, P26, P30, P32, P34, P36, P41 and P42 (2.7), the recheck's numbers, and what they imply for the verdict (2.8). Section 8 separates regression expectations (R1–R12, not counted) from predictions that need new runs (P1–P35) | 2, 8 |
| 18 | major | **Now resolved.** R_anc's season comes from ancient definitions: the union of Hesiod's agricultural autumn and winter (from Arcturus' heliacal rising) and Geminus' astronomical seasons (to the spring equinox). Arcturus' rising was computed for −1130 (2.8). R_anc runs with and without the eclipse clue, and only the version without it gives a comparable coincidence, which is empty by arithmetic. The known part of revision 2's P23 moved to 2.8 and R11; P19 is the new prediction [r1 N7, N9] | 2.8, 5.3, 7, 8 |
| 19 | minor | Resolved and confirmed: one Espenak–Meeus model, four models in the mixture | 0, 2.3 |
| 20 | minor | Resolved. A1–A5 are regression tests. I3 is a calibration, now also left out of INSTR [r1 N15] | 3.4, 6.1, 9.1 |
| 21 | minor | Resolved and confirmed: the magnitude definitions are pinned, and I2b compares like with like, with both sides now named [r1 N15] | 0, 6.1 |
| 22 | minor | Resolved and confirmed: epoch −1176.68; the window is half-open, built with `span_bounds`; the count is expected (R6) | 0, 2.2, 3.2, 8 |
| 23 | minor | Resolved. The T0 grid covers E, visibility and the MWRA definition. T0b's reading (F6 off) is a member of 𝒢_BM* | 3.2, 3.5, 5.3 |
| 24 | minor | Resolved and confirmed: all six slips corrected. The recheck's new slip of the same kind is corrected too [r1 N17] | 1.1, 4.4, 5.3, 6.4, 7, 13 |
| 25 | minor | Resolved and confirmed: the HIP numbers were verified, and Sirius uses the barycentric proper motion | 2.1, 13 |

### 14.2 The recheck of revision 2 (`critique-design-r1.md`)

| # | severity | resolution in revision 3 | sections |
|---|---|---|---|
| N1 | blocker | **The identity is stated** in 5.7: on a fixed poem, LR_slot = P_w(A)/P(A) ≤ 1/P(A). P(A) = 0.154 and the ceiling of about 6.5 are in 2.8 as known numbers (fix 1). **Option (a) is taken** (fix 2): no likelihood ratio enters the rule, and the ceiling is printed with every verdict as a finding. Under revision 3's uniform conditioning, LR_slot over T_A is identically 1. The evidence that remains (B&M's tolerances beyond the categorical readings) is measured by G over T_A, and it is reported as a Bayes factor BF_BM under B&M's own encoding hypothesis, with its ceiling. Fix 3, an I14 assertion against LR thresholds, has nothing to assert, because the rule holds none. It is generalised: I14(b) checks every synthetic set against the structural constraints of 9.4, `freeze.py` refuses to freeze if outcome 1 is unattainable with the measured pool sizes, and Q_attain reports it at verdict time. The estimator is run on the *Almagest* sets (fix 4) | 1.3, 2.7, 2.8, 5.7, 6.1, 9, 12.1 |
| N2 | major | **SL tolerances are set leave-one-set-out** (fix 1), so every set is scored as held out (fix 2). **rec_PCS is removed** from the gate (fix 3). The regime values are recorded (fix 4). **Departure:** they go in a new frozen file, `almagest_regimes.json`, instead of an edit to the licence-checked clue file. The clue file then stays byte-identical to its recorded hash, and I13(f) ties the two together. What the truth-side slack already decides is stated in 2.6, and only narrowing remains open | 2.6, 6.2, 6.4, 9, 12.1 |
| N3 | major | **The option rule for regime BM is named:** B&M's proxy where the row offers it; else `ge_true_k` at 1.5 d; else the primary. Under it Q_BM is known to hold (rec_ALM_BM ≤ 5), so it is in 2.6 and is a regression expectation (R9) | 2.6, 6.4, 8 |
| N4 | major | Every ΔT-dependent control row is scored under the four-model mixture, P_mix ≥ 0.5 (fix 1). The circular controls (R-DIOD and L4 from Table S10 v2020; T1 and X3 from SMH2016, *secondary*) are listed (fix 2). Q_ΔT reports whether gate 3a changes when they are rescored, and the gate is also reported without them (fix 3). SMH2016's Table S4 and §4b, and the 2020 Addendum, are read before the freeze into `deltat_circular.json` (fix 4). **Departure:** the review suggested Espenak–Meeus for the rescoring. Revision 3 triples every model's σ instead, because Espenak–Meeus also rests on fits to ancient eclipses | 2.6, 6.3.3, 9, 12.1 |
| N5 | major | T2-SEASON and T-INT-12's tolerance join the re-draft (fix 1). A sibling-convention audit lists every row whose primary passes the truth while a sibling convention fails it, and gate 3a is recomputed with those rows (fixes 2–3). Q_exposure uses both. Section 6.3.4 says plainly that the re-draft controls exposure to files only (fix 4) | 2.6, 6.3.4, 9 |
| N6 | major | **The principle is applied uniformly** (fix 1). The categorical readings C, V and M are conditioned (pool T_A). G is reported under T_C and T_A, and with the E-on gardens (fix 2). T0 = RE does not count toward outcome 1 (fix 3). **Departure:** E is not conditioned on but left out of every rule garden. Conditioning on E would leave about 28 targets, too few for any interval to fall below 0.05, and E has no tolerance part that could survive conditioning. Leaving it out removes E's contribution from the Odyssey and the null alike | 1.1, 1.3, 2.8, 3.5, 4.2, 5.3, 5.4, 9 |
| N7 | major | Revision 2's P26, P30, P32, P34, P36, P41 and P42 are moved to section 2, either as settled (2.7) or as regression expectations (R7–R9) (fix 1). Its P23 is restated with an ancient season bound: the known part is in 2.8 and R11, and P19 is new (fix 2). Its P36 is settled by N3 (fix 3) | 2.7, 2.8, 8 |
| N8 | major | R_obs is computed exactly by reweighting over T_C and every δ (fix 1). Every G has a gamma interval, with the upper bound used in outcome 1 and the lower in outcome 2 (fix 2). One reach definition and one garden are used on both sides of every reported ratio (fix 3). Beyond the fixes, the background is extended to +200, so that n_A is about 139 and not 74 | 4.1, 4.2, 5.3, 5.7, 9 |
| N9 | minor | The season bound is sourced from ancient definitions (Hesiod's Arcturus and Pleiades phases, Geminus' equinoxes and solstices; their union is primary) (fix 1). R_anc is reported with and without the eclipse clue (fix 2) | 2.8, 5.3, 8 |
| N10 | minor | Revision 2's P25 (now P21) compares G_BM with Ē_N4, the mean reach over epics. pct_N4 stays in the rule as the percentile it is | 5.4, 8 |
| N11 | minor | `operational_map.json` records the X-class decision: "X1–X4" maps to h_06 ≥ 0.5 or h_tot ≥ 0.5, and X3 and X4 to their smag thresholds under the mixture (fix 1). QS-SACK-06:a is scored at its own day and site (fix 2, its second option) | 6.3.3, 6.5, 10.3 |
| N12 | minor | `events.conjunctions(…, ephemeris=)`, and `sky.build(…, dt_model=float, refraction=)` (fix 1). One Day-0 date per clock in `POOL_DTYPE` (fix 2). A span and a column set for each site in `sites.json` (fix 3). Step 2 is re-estimated at 3–5 h with the star events, and disk at 4–5 GB | 4.1, 4.2, 10.2, 11.2 |
| N13 | minor | The continuous vertex test at ±1.5 d is B&M's integer ±1 and is the primary (T0's primary cell, F5's BM tolerances 1.5/2.5/3.5, regime BM). ±1 is reported, and P3 predicts that the survivor set does not depend on the choice | 3.2, 3.5, 5.3, 6.4, 8 |
| N14 | minor | H3 is one predicate (H3a ∧ H3b) with a joint conditional base rate | 7, 8 |
| N15 | minor | I3 is left out of INSTR (fix 1). I2b names its ΔT and ephemeris on both sides, with a tolerance that allows for the frame difference (fix 2) | 6.1, 9.1 |
| N16 | minor | The re-drafter reads only a generated brief, which holds the conventions, the policies and the cited rows, with no options (fix 1). It reads nothing else in the repository, so §8 and §13–14 are excluded with the rest (fix 2). The test is stated to control file exposure only (fix 3) | 6.1, 6.3.4, 10.1 |
| N17 | minor | Corrected: Ptolemy names Alexandria for his own records and Babylon for the Babylonian eclipses (IV.6.3), which belong to R-PTOL-BAB | 6.4 |

---

## Sources

The dossier, in `docs/`:

- `research-bm2008.md` (with `research-bm2008-a.md` and `-b.md`), the
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
- `critique-design-r1.md`, the recheck of revision 2;
  `results/critique-design-r1/`.
- `data-acquisition.md`, the ephemeris extension, NASA elements, stars and
  calendar; `results/data-acquisition/`.
- `controls-real-drafting.md` and `license-check-controls-real.md`, the real
  eclipse controls; `results/controls-real-drafting/`,
  `results/license-check-controls-real/`.
- `controls-almagest.md` and `license-check-almagest.md`, the *Almagest*
  control; `results/controls-almagest/`, `results/license-check-almagest/`.
- `negatives-drafting.md` and `license-check-negatives.md`, the negative
  controls; `results/negatives/`, `results/license-check-negatives/`.
- `research-unread-primaries.md`, on MacDonald, Schoch and Neugebauer,
  Papamarinopoulos, Henriksson and PLSV; `results/unread-primaries/`.
- `DESIGN-v1.md` and `DESIGN-v2.md`, revisions 1 and 2 of this design.

This revision's scratch scripts are in `results/design-revision-r2/`:

- `cp_bounds.py`: pool sizes, interval floors and garden sizes;
- `ranc_season.py`: Arcturus' heliacal rising at −1177 and −1130;
- `synth_sets.py`: the intervals of the synthetic sets;
- `alm_options.txt`: the options of the *Almagest* rows.

Each has its `.out.txt` beside it.

Primary items behind them, as the notes read them:

- **The paper.** Baikouzis & Magnasco, PNAS 105 (2008) 8823–8828,
  doi:10.1073/pnas.0803317105, with its Supporting Information and Table S2
  (`data/bm2008-a/`).
- **Earlier datings and their critics.**
  - Schoch, *The Observatory* 49 (1926) 19–21.
  - MacDonald, *JBAA* 77 (1967) 324–327.
  - Papamarinopoulos et al., *MAA* 12(1) (2012) 117–128.
  - Henriksson, *MAA* 12(1) (2012) 63–76.
  - Neugebauer & Schoch, *AN* 230 (1927) 57.
  - Gainsford, *TAPA* 142 (2012) 1–22 (*secondary* where it reports
    MacDonald).
- **Eclipse canons and ΔT.**
  - Espenak & Meeus, *Five Millennium Canon of Solar Eclipses* (NASA
    TP-2006-214141) and its JavaScript Explorer.
  - NASA's lunar eclipse catalogue (LEcat5).
  - Stephenson, Morrison & Hohenkerk 2016 and the Addendum 2020, with Table
    S10 v2020 (`data/ref/`).
- **Ephemerides and stars.**
  - JPL DE441 and DE431 (Park et al. 2021).
  - van Leeuwen 2007 (the Hipparcos new reduction), ESA 1997, and Bond et
    al. 2017 (Sirius).
- **Other.**
  - The PLSV 3.1 documentation (Lange & Swerdlow).
  - Fay & Feuer, *Statistics in Medicine* 16 (1997) 791–801, for the gamma
    interval (cited from memory, 13 row 37).
- **The ancient texts.** The Odyssey, the Iliad and their scholia; Ptolemy's
  *Syntaxis* (Heiberg); Geminus; Thucydides; Xenophon; Arrian; Plutarch;
  Curtius; Pliny; Livy; Diodorus; Virgil; Apollonius; Quintus Smyrnaeus;
  Valerius Flaccus; Hesiod; and Aratus. All were exported read-only from
  ClassicaCodex into `data/text/`.

The bench designs this one follows are `C:\Projects\labench\README.md` and
`C:\Projects\indusbench\DESIGN.md`.
