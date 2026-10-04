# odybench — design

A test bench for the claim that the sky clues in the Odyssey date the
slaughter of the suitors to 16 April 1178 BC. It is the fourth in the series
after vbench (Voynich), [labench](../labench/README.md) (Linear A) and
[indusbench](../indusbench/DESIGN.md) (Indus script), and it keeps their rule:
every test is run first on cases whose answer is known, so that a "no" about
the Odyssey means something.

Written 2026-10-03 from eight research notes in `docs/` (listed in Sources).
The ephemeris layer (`odybench/ephem.py`) is built and validated. The notes
already computed a good deal: chance rates for each clue, eclipse scans at
Ithaca, and a partial recomputation of B&M's table; section 2.5 lists the
results that bear on the predictions. None of the bench's own tests has been
run. Every test states its pass and fail before it runs, and section 6 is
frozen by hash before any null model, control or held-out check is computed
(section 7.4).

## 0. Conventions and tags

- **Years.** Historical BC with the astronomical year after it: 1178 BC (−1177).
- **Calendar.** Proleptic Julian throughout. 16 Apr 1178 BC is 5 Apr in the
  proleptic Gregorian calendar [crit §2.1].
- **Time scales.** TT (= TD of the eclipse canons); UT = UT1; ΔT = TT − UT.
  UT+2 is zone time on 30°E, the clock Baikouzis & Magnasco actually used
  [bm §3.2]. LMT at 20.72°E = UT + 1 h 22.9 min. LAT is local apparent solar
  time. Every clock time below names its scale.
- **Sites.** Ithaki (Vathy) 38.367°N 20.717°E is the primary site [crit §2.3].
  B&M's clock fits 38.4°N 20.7°E [bm §3.2]. Kefalonia (Argostoli), Paliki
  (Lixouri), Lefkada (Nidri) and Corfu are sensitivity sites.
- **ΔT always travels with its lunar ephemeris** (its ṅ). A ΔT value from one
  pairing is never applied to another [eph §5.3; bm §3.3; ctl §2.3].

**Provenance tags.** A tag names the dossier note and section that carries
the number and its primary source:

| tag | note |
|---|---|
| [bm §n] | `docs/research-bm2008.md`, the reconciled spec of the paper |
| [chron §n] | `docs/research-chronology.md` |
| [txt §n] | `docs/research-textclues.md` |
| [eph §n] | `docs/research-ephemeris.md` |
| [vis §n] | `docs/research-visibility.md` |
| [ctl §n] | `docs/research-controls.md` |
| [win §n] | `docs/research-window.md` |
| [crit §n] | `docs/research-critiques.md` |
| [B&M §X] | the paper itself: Baikouzis & Magnasco, PNAS 105 (2008) 8823–8828, by section heading (Method, References and Constraints, Intersecting the Constraints, Historical Plausibility, Conclusions), Table 1–2, Fig. 1–2; [SI p.n], [S2] for the Supporting Information |
| [Od. x.y] | Greek text, `data/text/odyssey-grc.tsv` |
| [me] | computed or reasoned for this document; the tool is named |

"B&M" is Baikouzis & Magnasco 2008 throughout. Statements a note made from a
secondary report keep that status here and are marked *secondary*.

---

## 1. The claim under test

### 1.1 What the paper says

B&M's abstract, which I paraphrase closely (the full text is local at
`data/bm2008-a/bm2008-pmc-fulltext.txt`):

- They take three overt astronomical references in the epic, to Boötes and
  the Pleiades, to Venus and to the New Moon, and add a conjectural one,
  Hermes' trip to Ogygia read as the motion of the planet Mercury.
- They search every date in 1250–1115 BC (−1249 to −1114) for days matching
  these phenomena in the order and manner the text gives.
- In that span, in their words, "a single date closely matches our
  references": 16 April 1178 BC (−1177), JD 1291263.5 at 0 h [bm §9].
- They do not assume an eclipse; Theoclymenus' vision (Od. 20.356–357) is not
  a search criterion. They speculate afterwards that the references and the
  disputed eclipse passage refer to the total solar eclipse of that day, which
  Schoch (1926) and P. V. Neugebauer (1929) had computed as total over the
  Ionian Islands [B&M abstract; bm §2, §11].

The body adds four claims the bench also tests [B&M §Intersecting, §Historical
Plausibility, §Conclusions; bm §2]:

1. The date satisfies all criteria as stated in the 135-year span, under both
   their sequential and parallel day counts, exactly under the sequential one.
2. The references can be matched exactly about one day in 2,000 years. The
   arithmetic is one candidate New Moon in 6 years × 3 (Venus) × 116 days
   (Mercury) ≈ 2,088 years [bm §10].
3. Two independent sets of verses (the eclipse lines and the other sky
   references) point to the same day; chance agreement of fictional references
   with the only eclipse of the century would be minute.
4. Supporting coincidences found afterwards: the eclipse near noon, early
   spring, Mars invisible except during the eclipse.

The search criteria, as reconciled from the primary text and the
transcriptions of Table S2 [bm §5]:

| clue | lines | criterion | day (sequential / parallel) |
|---|---|---|---|
| N, New Moon | Od. 14.161–162 = 19.306–307; 14.457; Apollo's feast 20.156, 20.276–278, 21.258–259 | Ti is the date of a New Moon (search unit) | 0 / 0 |
| C, Pleiades and late-setting Boötes | Od. 5.270–277 | Ti−29 ≥ 17 Feb and Ti−12 ≤ 4 Apr, so Ti in 18 Mar–16 Apr of a common year | −29 / −28 (all sailing nights to −12 / −11) |
| V, morning star | Od. 13.93–95 | Venus rises ≥ 90 min before the Sun | −5 / −4 |
| M, Hermes = Mercury | Od. 5.43–58, 5.97–103 | Ti−34 within a few days (S2: ≤ 1 to pass) of Mercury's maximum western rise azimuth (MWRA) | −34 / −33 |
| E, Poseidon = equinox | Od. 5.282 | 1 Apr ≤ Ti−11 ≤ 5 Apr; listed, **not applied** | −11 / −10 |
| X, the eclipse | Od. 20.345–357 | not used | 0 |

### 1.2 What the bench can and cannot establish

It can establish:

- whether B&M's computation reproduces with a modern ephemeris, and if not,
  which step fails (section 2);
- how often B&M's criteria, and criteria like them, are met by chance, per
  century and per window (N1, N5);
- how often a date picked out by such criteria would be an eclipse new moon
  if the clues had nothing to do with the eclipse (N2);
- how much the freedom to choose readings, thresholds, tolerances and windows
  inflates a match (N3), and how often a random poem of the same grammar
  "dates" itself as well (N4);
- whether the 1178 BC eclipse was total at Ithaca, as a probability over the
  ΔT models now published (N6);
- whether the method recovers dates that are known, and whether it "dates"
  fiction (section 4);
- whether sky clues B&M did not use agree with their date more often than
  chance (section 5).

It cannot establish:

- that the poet meant any line astronomically. Every reading is a fork
  (section 3.4); the bench prices forks, it does not choose between them.
- that Odysseus, the war or the return happened. B&M say the same [bm §2].
- the season of the poem, the meaning of λυκάβας, whether Hermes is Mercury,
  or whether Apollo's feast fell on the new moon. These are philological
  questions; the notes record that the text and the ancient commentators do
  not settle them [txt §5; vis §3–4; crit §3].
- a posterior probability. The prior that a day-dated sky observation survived
  400–600 years of oral transmission before writing is not something the bench
  can compute; the notes found no comparative case of it [win §10–11]. The
  bench reports likelihood ratios and look-elsewhere-corrected p-values, and
  stops there.

**A bit budget, to fix ideas** [me: arithmetic from vis §1.3, §2.3, §3.4 and
bm §8.2]. Singling out one New Moon among the 1,683 in B&M's window takes
log2(1683) = 10.7 bits. B&M's applied clues carry about C 3.6 bits (8.3% of
New Moons pass), V 2.7 bits (15.8% of spring Day −5s) and M 4.5 bits (6/136
rows pass with DE441): 10.8 bits in all, so about one chance survivor is
expected (1683 × 0.083 × 0.158 × 0.044 = 0.97). The garden of defensible
readings defined in section 3.4 has 428,544 members, which could cost up to
18.7 bits of look-elsewhere if the readings were independent. They are not
independent; measuring how much of that cost is real is the job of N3.

### 1.3 Outcomes

Four outcomes are possible, and each is worth having. The second and the
fourth can hold together.

1. **The text dates the return.** The match survives the garden (N3), random
   epics of the same grammar do not match as well (N4), the controls recover
   known dates (section 4) and the negative controls do not date themselves.
   The bench then says so and says what it would take to believe it.
2. **The match is ordinary.** A comparable date fixed in advance, with no
   relation to the text, is made the unique match by some defensible reading
   often (G ≥ 0.05 in N3). The coincidence then carries no evidential weight,
   whatever its fixed-reading p-value.
3. **The method cannot see.** It loses the true date of real dated passages,
   or of clue sets generated from real skies (PC-R, PC-S). Every "no" about
   the Odyssey is then reported as "could not have seen it".
4. **The method dates fiction.** The Iliad, the Aeneid or the Argonautica
   date themselves as cleanly as the Odyssey (NC). That retires the method,
   not only the claim.

"What, if anything, the text can date" is reported in every case, at the level
the tests support: a relative chronology [chron §5], a month-turn on Day 0
under one reading [txt §5.1], a season that the text does not determine
[txt §5.6], and a year only if outcome 1 holds.

---

## 2. T0: reproduction

### 2.1 T0a: replay of Table S2 (done; regression test)

Two independent transcriptions of Table S2 agree cell for cell, colours
included: 152 rows × 13 fields, 0 differences [bm §1, §12 row 1]. Applying the
decoded colour rules (Venus orange iff lead ≥ 1:30:00; Mercury orange iff
abs Δ ≤ 1, yellow 2, pale yellow 3; Equinox XXX iff Ti−11 ≥ 1 Apr) to the 136
rows of 1250–1115 BC gives [bm §8.1; `results/bm2008-reconcile/s2_counts.out.txt`]:

| criterion | survivors |
|---|---|
| V | 21 |
| M (abs Δ ≤ 1) | 4: 1236, 1224, 1178, 1157 BC |
| E | 22 (XXX), 20 (1–5 Apr), 17 (1–4 Apr) |
| V and M | **1178 only** |
| V, M and E | 1178 only |

T0a is complete. It becomes the regression test `tests/test_t0.py`, so that
every later change to the rules is checked against the published table.

### 2.2 T0b: the search recomputed with DE441

The algorithm, in order. Every parameter is pinned in the table after it.

1. **Candidates.** Find every geocentric conjunction in apparent ecliptic
   longitude (`ephem.new_moons`) whose UT+2 civil date falls from 1 Jan
   1250 BC to 31 Dec 1115 BC (−1249 to −1114). Expected count 1,683; B&M say
   1,684 [bm §7; `check_ti.out.txt`].
2. **Ti** is the UT+2 civil date of the conjunction. Rise and set times use
   B&M's clock ΔT of 27,602.7 s, which is what reproduces S2's clock
   [bm §3.2].
3. **C.** Keep a candidate if Ti−29 ≥ 17 Feb and Ti−12 ≤ 4 Apr of the same
   Julian year, with true Julian day arithmetic (29 Feb counted). Where two
   New Moons in a year pass, **evaluate both**. S2 lists only one of the two in
   each of the five years where two pass, choosing by no consistent rule, and
   lists out-of-window Ti in three other years [bm §7].
4. **V.** On Ti−5, compute sunrise and Venus rise. Pass if Venus is a morning
   object and rises ≥ 90.0 min before the Sun.
5. **M.** For each morning in a span covering Ti−34 ± 60 d, compute Mercury's
   rising azimuth (from north through east) at the instant of rising. The MWRA
   is the date of the local maximum of that daily series nearest Ti−34;
   equidistant maxima resolve to the earlier. Δ = (Ti−34) − MWRA in true
   Julian days. Pass if abs Δ ≤ 1. Record also whether Mercury is visible on
   Ti−34 (Sun altitude at Mercury's rising ≤ −10°, Ptolemy's arcus visionis
   [vis §2.2]); B&M required visibility in the text but never tabulated it
   [bm §5 M].
6. **E** (reported, not applied). Pass if 1 Apr ≤ Ti−11 ≤ 5 Apr; also
   report the ≤ 4 Apr and ≤ 6 Apr variants and the computed equinox date
   (apparent solar longitude 0°).
7. **Parallel reckoning** (reported, not applied): repeat steps 3–6 at offsets
   −28/−12…−11, −4, −33, −10 [B&M Table 1].
8. **Output** an S2-shaped table for every candidate (`results/t0/candidates.tsv`),
   the survivor sets of every criterion and combination, and the 1178 BC row.
9. **Comparison with S2.** Ti agreement by zone, Venus pass-set equality,
   MWRA agreement (exact and ±1 day), Δ agreement, leap-day effects.

| parameter | value | source |
|---|---|---|
| planets, Sun, Moon | JPL DE441 excerpt `data/ephem/de441_m1320_m1030.bsp` | [eph §1] |
| precession, sidereal time | Vondrak 2011 long-term model, module default | [eph §3] |
| site | 38.4°N 20.7°E, sea level | B&M Fig. 2 gives only Ithaca's latitude; the S2 fit favours 38.4°N [bm §3.2] |
| clock | UT+2 | S2 sunrise − DE441 UT sunrise = +120.0 min, sd 1.6, n = 75 [bm §3.2] |
| ΔT (clock only) | 27,602.7 s, constant | [B&M §Method; bm §3.1] |
| rise definition | airless geometric altitude of the centre at h0 = −0.8333° (Sun) and −0.5667° (planets) | settings that reproduce S2 [bm §3.2, `check_venus.py`] |
| New Moon | apparent ecliptic-longitude conjunction, UT+2 civil date | best single rule, 136/152 [bm §5 N, §13 item 1] |
| window | −1249-01-01 to −1114-12-31, UT+2 dates | [B&M §Method; bm §6] |
| C bounds | Ti−29 ≥ 17 Feb, Ti−12 ≤ 4 Apr | [B&M §References and Constraints; bm §5 C, §12 row 4] |
| V threshold | lead ≥ 90.0 min on Ti−5 | [B&M §References; SI p.1; bm §5 V] |
| M event | local maximum of rising azimuth (N through E), nearest Ti−34 | matches S2 124/152 exactly, 138/152 within ±1 d [bm §5 M] |
| M tolerance | abs Δ ≤ 1 d to pass; 2 and 3 reported | S2 colours [bm §5 M] |
| day arithmetic | true Julian; S2's 365-day arithmetic reported beside it | [bm §5 M: 21 leap-year rows differ] |
| E | 1 Apr ≤ Ti−11 ≤ 5 Apr (also ≤ 4, ≤ 6) | [B&M §References; bm §5 E] |
| offsets | sequential 0, −5, −11, −12, −29, −34 | [B&M Table 1; bm §4] |

### 2.3 T0c: the eclipse statements

For 16 Apr 1178 BC (−1177) the bench computes local circumstances at the five
sites under each pairing below, and the constant-ΔT window for totality
(`ephem.totality_window`):

| pairing | why | values already in the notes |
|---|---|---|
| NASA 5MCSE elements, canon ΔT 28,590 s | the canon B&M quote | Ithaki 0.984, max 10:22 UT = 11:45 LMT = 11:44 LAT, Sun 57°; total for ΔT 28,801–29,585 s [crit §2.3; eph §5.4] |
| DE431 + SMH2020 ΔT 28,543 ± 720 s | SMH's ΔT is tied to the DE430 lunar model | Ithaki 0.984 at LAT 11:44; total for 28,761–29,545 s [eph §5.4] |
| DE441 + SMH2020 ΔT | the bench's planetary ephemeris | Ithaki 0.972 at LAT 11:49; total for 28,922–29,706 s; DE441 is +187.7 s late against DE431 at −1177 [eph §5.3–5.4] |
| DE441 + B&M's 27,602.7 s | what B&M printed | 0.900 at 12:48 UT+2, not total [bm §3.3]. This mixes ephemerides and is reported only to show it |

The canon identity B&M quote (Saros 39 member 31; greatest eclipse 32.7°N
12.7°E; catalogue 01966; γ 0.5187; magnitude 1.0599) is checked against the
canon page [crit §2.1; bm §3.3].

### 2.4 Acceptance criterion

Instrument checks come first. If any fails, the claim-level verdict is not
read until the cause is found.

| check | pass | already measured |
|---|---|---|
| A1 Ti | DE441 UT+2 conjunction dates match S2's Ti in ≥ 134 of 152 rows | 136 [bm §5 N] |
| A2 Venus | DE441 pass set on S2's own Ti equals S2's orange set; S2 lead times reproduced with sd ≤ 3 min | 25/25 equal; offsets sd 1.5 min [bm §3.2, §5 V] |
| A3 MWRA | ≥ 124/152 exact and ≥ 138/152 within ±1 d | 124 and 138 [bm §5 M] |
| A4 1178 BC values | Venus lead 103.6 ± 1 min (B&M 1:42:56); conjunctions 18 Mar 03:31 and 16 Apr 12:25 UT+2; equinox within 10 min of B&M's 15:24; Sun at −12° on 18 Mar within 5 min of B&M's 19:38 | 103.6 min; 03:31, 12:25; 15:31; 19:34 [bm §3.2, §9] |
| A5 canon identity | catalogue entry and greatest-eclipse point as in 2.3 | matched [bm §3.3] |

The verdict on the claim, decided by the T0b survivors of N, C, V and M in
1250–1115 BC (E off):

- **Reproduced as stated:** 16 Apr 1178 BC passes all four and is the only
  candidate that does.
- **Reproduced only with the equinox:** 1178 BC passes all four, other
  candidates do too, and 1178 BC is unique only when E is added.
- **Not reproduced:** 1178 BC fails N, C, V or M; the report names the
  criterion and the margin.

On the eclipse, B&M's statement that Ithaca lay on the edge of totality is
**consistent** if Ithaki is total for some ΔT within one stated sigma of the
SMH2020 value in the DE431 pairing, and **not reproducible as stated**, because
B&M's 27,602.7 s belongs to Starry Night's ṅ, which is not documented
[crit §2.3; ctl §2.3].

### 2.5 What is already known, and so is not a prediction

These came out of the research notes before this design was written. They
are listed so that nothing below pretends to predict them.

- With Mercury recomputed by DE441 on S2's own Ti, M passes in 1236, 1224,
  1190, 1189, 1178 and 1144 BC; 1157 BC drops out (DE441 MWRA 22 Feb, Δ −3);
  V and M is **{1178, 1189}** [bm §8.2; `check_mwra_curves.out.txt`].
- 18 Mar 1189 BC (−1188) passes N, C (Ti−29 = 18 Feb in a leap year), V
  (lead 100.9 min) and M (Δ 0), and fails E (Ti−11 = 7 Mar) [bm §8.2].
- No visibility threshold separates the two. At Mercury's rising the Sun
  stood at −13.2° on 13 Mar 1178 BC and −17.1° on 13 Feb 1189 BC, so any
  arcus visionis that admits 1178 admits 1189 [`check_extras.out.txt`].
- Under the parallel reckoning 1178 BC misses the Pleiades bound and the
  equinox bound by one day each [bm §9].
- The eclipse at Ithaki is partial at every central ΔT in the notes. In the
  DE431 pairing, totality needs ΔT 218 to 1,002 s above the SMH2020 central
  value of 28,543 s, i.e. +0.3σ to +1.4σ [eph §5.4; me: arithmetic].
- The Almagest's own Mercury and Venus elongation records sit 3 and 16 days
  from the true extremes [ctl §4.19].

So the expected T0 verdict is "reproduced only with the equinox". T0b must
still run in full: the corrected Ti in 16 rows, the second New Moons of five
years, and true leap-day arithmetic have not been evaluated together.

---

## 3. Null models

### 3.1 Shared machinery

- **Sky tables.** For every day of the span, morning and evening: rise and
  set times and azimuths of the Sun, Moon, Mercury, Venus, Mars, Jupiter and
  Saturn; Sun altitude at each planet's rising and setting (for arcus
  visionis); signed elongation; V magnitude; ecliptic longitude (for
  stations); the times of civil and nautical twilight; altitudes at the end of
  evening and start of morning nautical twilight of Alcyone (Pleiades),
  Arcturus, Sirius, Aldebaran (Hyades), Betelgeuse and Rigel (Orion) and
  Dubhe (the Bear). From these, the events: stations, greatest elongations,
  rise- and set-azimuth extrema, first and last visibility at several arcus
  visionis values, heliacal star phases, equinoxes, conjunctions, full moons,
  first crescent by Yallop's q-test [vis §0, §4.2]. ΔT is SMH2020 for the
  bench proper; T0b alone uses 27,602.7 s.
- **Background span.** 1500–600 BC (−1499 to −599), the span of the eclipse
  scans already made [win §7], with 120 days of margin either side for the
  40-day clue offsets and the ±60-day Mercury searches.
- **Candidate pools.** P_all: every conjunction. P_day: conjunctions whose
  instant falls in Ithaki daylight, 50.9% of them [vis §4.2], the only ones
  that can give a visible solar eclipse. P_spring: conjunctions passing C, about
  1.02 a year, 8.3% of all [vis §3.4].
- **Eclipse classes** at Ithaki, from the NASA 5MCSE Besselian elements with
  canon ΔT and Huber's σ (1,008 s at −1177) [crit §2.1; win §7]. Counts are
  for 1500–600 BC and come from `results/window/jsex/windows-out.txt` [win §7.2]:

  | class | definition | events in 1500–600 BC |
  |---|---|---|
  | **X1** (primary, Schoch's) | total for some ΔT within ±1σ, maximum 10–14 h LAT, Sun up | 3: 1312, 1178, 1131 BC |
  | X2 | total for some ΔT within ±1σ, any hour, Sun up | 10 |
  | X3 | magnitude ≥ 0.95 at canon ΔT | 15 |
  | X4 | magnitude ≥ 0.6 at canon ΔT, Sun ≥ 10° (the darkness wording of Hdt. 9.10 and Plut. *Pel.* 31 went with 0.60 and 0.67 [ctl §0 item 3]) | to compute |

- **Windows.** Reproduction 1250–1115 BC (136 years); primary 1350–1100 BC
  (251 years); Troy VIIa 1240–1150 BC (91 years); strict Eratosthenes
  1176–1172 BC; background 1500–600 BC [win §9].

### 3.2 N1: random dates in the window

The question: how often do B&M's applied criteria pass by chance?

1. Evaluate the B&M reading (T0b conventions, SMH2020 ΔT) on every candidate
   in the background span.
2. **Rate.** λ = survivors per century, with a Poisson 95% interval.
3. **Windows.** Slide windows of W = 50, 100, 136, 200, 250, 500 and 900
   years along the background one year at a time. Report the empirical
   P(≥ 1 survivor) and the mean count, beside the Poisson values. Venus' 8-year
   cycle and Mercury's 13- and 46-year near-repeats cluster survivors; the
   empirical figure includes that, the Poisson one does not.
4. **Per-target rate.** p_fix = the fraction of P_spring that passes V and M
   (N and C hold by construction). This is the probability that a target fixed
   in advance (such as Schoch's eclipse) passes criteria fixed in advance.
5. **Independence.** B&M multiply marginal rates [bm §10]. Compare the joint
   pass count on P_spring with the expectation from the marginals; the null
   distribution comes from permuting the Venus outcome among candidates with
   the same Ti (Julian day of year ± 3 d), 10,000 times.
6. **Without N.** Repeat with Day 0 any day (no New Moon requirement), to
   show what N itself contributes.

Statistics: λ, P(≥ 1 | W), p_fix, the dependence ratio (joint / product of
marginals) and its permutation p.

### 3.3 N2: the eclipse coincidence

The question: if the criteria had nothing to do with eclipses, how often would
a date they pick be an eclipse new moon?

1. For each class X and window: p_e = |X ∩ P_spring| / |P_spring|, and the
   same over P_day. The pool must be New Moons, never days: an eclipse can only
   fall on one, so using days would inflate the coincidence about 29.5-fold
   [me].
2. **Fixed reading, target first:** P(a class-X new moon in the spring
   window passes V and M) = p_fix from N1. This is the strongest form of
   B&M's argument: had the criteria been fixed before anyone looked at
   1178 BC, a pass would be notable at roughly the p_fix level.
3. **Fixed reading, survivors first:** with s survivors in a window holding n
   candidates of which m are class X, P(≥ 1 survivor in X) = 1 − C(n−m, s) /
   C(n, s) (hypergeometric).
4. **Background double hits:** count survivors that are also class X across
   1500–600 BC, per century. The notes' order-of-magnitude estimate is
   10⁻⁵–10⁻³ per 135-year window for criteria fixed in advance [win §8c].

Clue outcomes are taken to be independent of the eclipse status once the
pool is restricted to New Moons in the same season: no clue involves the lunar
node. N2 checks this by comparing V and M pass rates on eclipse and non-eclipse
new moons of P_spring.

### 3.4 N3: forking paths

B&M's criteria were not fixed in advance. The target was Schoch's; the
references, thresholds, tolerances, season, day count and window were chosen
with it in view [win §8; crit §4]. N3 counts the readings a careful reader of
the Greek could defend, and asks how often *some* reading makes a given target
the unique match.

**The forks.** Each option is sourced. "None" means the clue is dropped.

| fork | options | n | sources |
|---|---|---|---|
| F1 day count | the 8 rows of the reading grid: raft count 5 or 4 days, departure-to-landing 20 or 19, Ithaca-to-slaughter 5 or 4. Offsets range: Mercury 31–34, first raft night 27–29, last raft night 11–12, storm 10–11, Venus 4–5 | 8 | [chron §5.1] |
| F2 Day 0 | (a) conjunction date, UT+2; (b) conjunction date, LMT; (c) the day after, Solon's noumenia; (d) the first-crescent day, Yallop B, Greek day from sunset | 4 | [vis §4.1–4.3; Plut. *Sol.* 25.3 via vis §4.1; bm §13 item 1] |
| F3 stars | (a) B&M's fixed Julian cutoffs; (b) recomputed each year, Arcturus and Alcyone both ≥ 2° at the end of nautical twilight on every raft night; (c) the same at ≥ 5°; (d) departure night only, ≥ 2°, either season; (e) autumn: every raft night inside the autumn co-visibility window, recomputed each year; (f) none, "late-setting" as a permanent property | 6 | [vis §3.3–3.4; txt §5.8; crit §3.1] |
| F4 morning star | Venus lead ≥ 60, ≥ 90 (B&M) or ≥ 120 min; Venus a visible morning star (arcus visionis 7°); any bright dawn herald (Venus, Jupiter, Sirius, Mars ≤ −1 mag); none (a time-marker) | 6 | [vis §1.2–1.4; txt §5.7] |
| F5 Mercury | event: MWRA, greatest western elongation, morning station, any of these three, or morning first visibility (arcus visionis 10°); tolerance 1, 2 or 3 days; visibility on the day required or not; or none | 31 | [vis §2.3; B&M §References names the three events; bm §5 M] |
| F6 equinox | off; Σ-day in 1 Apr–4 Apr, 1 Apr–5 Apr or 1 Apr–6 Apr (Σ-day from F1) | 4 | [B&M §References; bm §5 E] |
| F7 window width | 91, 136 or 251 years | 3 | [win §9] |

The full garden has 8 × 4 × 6 × 6 × 31 × 4 × 3 = **428,544** readings
[me: arithmetic]. Only F2 (a) and (b) allow an eclipse on Day 0, where
Theoclymenus speaks [chron §4.H], so the **eclipse-compatible garden** has
214,272. The text-level enumeration in the notes, built from different forks,
gave 23,328 paths [txt §8]; the two counts measure different things and
neither is a count of independent tests.

Two smaller gardens are run beside it:

- **G_BM**, the forks B&M themselves raised: sequential or parallel day count;
  MWRA, elongation or station at 1–3 days, visible; equinox off or at
  ≤ 4/5/6 Apr; window 136 years. 2 × 9 × 4 = **72** readings [me].
- **G_1**, every reading within one fork of B&M's: 1 + 7 + 3 + 5 + 5 + 30 +
  3 + 2 = **56** readings [me].

Two readings are left out because they cannot change the result: Day 0 as a
20-day window ("the waning or waxing part of the month", [vis §4.4]) and N
dropped. Their candidates are days, a superset of the conjunction dates, and a
conjunction date that is the unique survivor among days is also the unique
survivor among conjunction dates, so they add no reach for any New Moon target
[me].

**The statistic: reach.** For reading r, let S_r be its survivors over the
background. Under readings F2 (c) and (d) a candidate is mapped back to its
conjunction, so every target is a conjunction. A target t in S_r is the unique
survivor of a W-year window [a, a+W] placed at a uniformly random start
a ∈ [t−W, t] exactly when the window misses the neighbouring survivors s₋ and
s₊, that is, for a in I_r(t) = (max(t−W, s₋), min(t, s₊−W)); if t is not in
S_r, I_r(t) is empty. Over the garden, **reach_W(t) = |∪_r I_r(t)| / W**,
the probability that some reading makes t the unique match. F7 enters as
three separate widths and reach(t) = max over W of reach_W(t), a lower bound
on the union. Targets closer than 251 years to either end of the background
are left out, so that every window lies inside it.

Reported:

1. reach(16 Apr 1178 BC) under the B&M reading, G_1, G_BM and the full garden.
   Under the T0b reading with E off, 1189 BC lies 11 years away, so reach is 0
   for a 136-year window unless E is on [me, from 2.5].
2. **G = mean reach over P_day** in the background: the probability that a
   new moon fixed in advance, with no relation to the text, is made the unique
   match by some reading. **This is the look-elsewhere-corrected p-value of
   B&M's coincidence.** It is reported for each garden, with a binomial
   interval over the pool.
3. G over each eclipse class X. If eclipse new moons are reached at the same
   rate as other new moons, the eclipse adds nothing beyond its own rarity.
4. The look-elsewhere factor G / p_fix,unique, where p_fix,unique is the same
   quantity for B&M's reading alone.
5. **Alternative datings.** Every class-X1 to X3 eclipse in each window that
   some eclipse-compatible reading makes the unique survivor, with the
   readings that do it. 30 Sep 1131 BC (total at Ithaki at canon ΔT, inside
   B&M's own window [crit §2.4]), 24 Jun 1312 BC, 30 Oct 1207 BC
   (Papamarinopoulos et al. 2012, *secondary* [crit §5]) and 12 Jan 1183 BC
   (Schoch's rejected annular eclipse [crit §1.1]) are listed whatever the
   result.
6. Survivors per century for every reading, so the strictness of the garden is
   visible.

### 3.5 N4: random epics

N3 holds the poem fixed and varies its reading. N4 holds the reading machinery
fixed and varies the poem: random clue sets drawn from the grammar the
Odyssey's clues come from.

**The grammar** (`data/prereg/epic_grammar.json`):

- **Day 0 anchor:** conjunction, full moon, the 7th day of the month
  (Apollo's day in Hesiod, *Works and Days* 770–771 [txt §5.3]), or none.
- **Season clue:** a pair from the archaic star list (Pleiades, Hyades,
  Orion, Sirius, Arcturus; the Shield and Hesiod list [txt §5.8]), both
  ≥ 2° at the end of evening or morning nautical twilight on one night or on
  a 17-night span, or one star's heliacal rising or setting within ±k days.
- **Planet clue:** Venus, Mercury, Mars, Jupiter or Saturn; morning object
  with rise lead ≥ 60/90/120 min, evening object with set lag ≥ 60/90/120 min,
  or within ±1–3 days of a turning point (rise- or set-azimuth extremum,
  greatest elongation, station, opposition) or of first or last visibility
  (Ptolemy's arcus visionis: Venus 5°, Mercury 10°, Jupiter 10°, Mars 11.5°,
  Saturn 11° [vis §1.2]).
- **Offsets:** variant A ("B&M-shaped") puts a season clue on a span starting
  between −29 and −27 and two planet clues at −5 and −34 around a
  conjunction anchor, with the clue types drawn at random. Variant B draws the
  anchor, two or three sky clues and their offsets (−40 to −1) freely.

10,000 epics per variant, seed 20261003.

For each epic, evaluated on the background span:

- p_c, its per-candidate pass rate (its specificity);
- the survivor count in a 136-year window at a random position, and
  P(unique);
- **"matches at least as well":** score each date by −log10 of the product of
  the per-clue base rates at the observed tightness (e.g. P(Venus lead ≥
  observed lead), P(abs Δ ≤ observed)). For the Odyssey, T_obs is that score
  for 1178 BC under the B&M reading. The statistic is P(T_best ≥ T_obs): how
  often the best date in the window matches a random epic at least as tightly
  as 1178 BC matches the Odyssey. Epics are also reported in specificity
  strata within a factor 2 of B&M's p_c;
- the **double hit**: P(unique survivor ∧ survivor in class X), fixed reading.

**Garden-augmented epics.** For 1,000 epics, apply an epic garden built from
the same fork types (threshold menus, ±1-day offsets, season variants,
tolerances 1–3, window widths) and compute G for each epic. Each epic's
garden, and the Odyssey's for this comparison only, is subsampled to 1,000
readings so the two are comparable. This gives the poetic-hypothesis
denominator of the bottom-line ratio (3.8).

### 3.6 N5: window sensitivity

Run N1, N2 and N3 in each window of 3.1. Report survivors per century, the
survivor list, the class-X eclipses in the window, and P(≥ 1) as a function of
W from 50 to 900 years. Never report "the single date in the window" without
the rate beside it [win §9].

Two specific checks:

- **Strict Eratosthenes.** Eratosthenes put the sack in late spring 1183 BC
  (−1182); with at least 8 years of wandering [Od. 7.259–261, 10.467–470] the
  return falls in about 1175–1173 BC, and 1178 BC is outside [win §5–6]. The
  bench reports which survivors, under which readings, are compatible with
  each ancient sack date plus 8–11 years.
- **Gainsford's 1350–1250 BC extension**, which the primary window includes,
  with the four eclipses near Ithaca he lists [crit §2.4; win §4].

### 3.7 N6: ΔT sensitivity of the eclipse at Ithaca

1. **Models** at −1177.29 [eph §2.3]: SMH2020 (S15 + HMNAO lod integral)
   28,543 ± 720 s; Addendum 2020 parabola 28,282 ± 541 s; SMH2016 parabola
   28,963 ± 541 s; Espenak–Meeus 28,716 s and its canon-ṅ form 28,589 s,
   Huber σ 1,008 s.
2. **Pairings:** SMH models with DE431; Espenak–Meeus with the NASA
   elements; DE441 reported beside both with its +188 s offset [eph §5.3].
3. **Sites:** Ithaki, Kefalonia, Paliki, Lefkada, Corfu.
4. **Outputs:** magnitude and LAT of maximum as a function of constant ΔT
   from 26,000 to 32,000 s; totality windows; P(total) per model, taking each
   stated error as a Gaussian 1σ (an assumption, stated each time [eph §8
   item 1]); the equal-weight mixture over the five models; P(magnitude
   ≥ 0.9).
5. **Same for 30 Sep 1131 BC and 24 Jun 1312 BC**, and the joint probabilities
   under a common ΔT offset. The 1178 and 1131 windows overlap only near
   +220 to +340 s above canon ΔT, so at most one of the two was likely total
   at Ithaca [win §7.1].
6. **ΔT and the clue tests.** Count the candidates whose UT+2 conjunction date
   flips between ΔT 27,602.7 s and each model at ±1σ, and rerun T0b at
   SMH2020 ± 1σ.
7. **B&M's own value.** 27,602.7 s with ELP-2000/82's native ṅ maps to about
   29,356 s in the canon frame or about 29,320 s in a DE frame, inside the
   totality window [crit §2.3; ctl §0 item 9]. The ṅ Starry Night used is
   unknown, so this is reported as uninterpretable, not as support.

### 3.8 The bottom-line statistic

Following the controls note [ctl §7.5]:

LR = P(unique match ∧ match is a class-X1 eclipse new moon | the clues are
observations) / P(the same | the clues are poetic).

- **Numerator:** PC-S(a) (4.2), true clue sets generated from X-class eclipse
  dates, at noise levels (ii) and (iii) combined.
- **Denominator:** N4, the double-hit rate of random epics.
- Computed twice: with the reading fixed (LR_fixed) and with the garden on
  both sides (LR_garden). Only LR_garden answers B&M's case, because their
  reading was chosen knowing the target.

The bench reports LR, G, p_fix and the bit budget. It does not multiply them by
a prior.

---

## 4. Controls

All clue sets, readings, windows, sites and random seeds for the controls are
written to `data/prereg/` and frozen with this document before any control is
computed.

### 4.1 Instrument controls (must pass before anything else is read)

| # | control | pass | status |
|---|---|---|---|
| I1 | ephemeris validation, `tools/validate_ephem.py` and `tests/test_ephem.py` | 55/55 and 10/10 | passed 2026-10-03 [eph] |
| I2 | eclipse pipeline: the Python port of NASA's JavaScript Explorer against the original | magnitudes and obscurations equal to 3 decimals | passed for −1199..−1100 at Ithaki [crit §2.2] |
| I2b | local magnitudes for the dated eclipses of [ctl §3], recomputed in `odybench.eclipses` | within 0.02 of the Horizons-based values: Thuc. 2.28 0.877; Hdt. 9.10 0.60; Archilochus 648 BC 1.000; Pelopidas 0.67; Diod. 20.5 0.995; Ennius 400 BC 0.717; *De facie* AD 71 0.979 | to run |
| I3 | Hesiod's star calendar at 701 BC (−700), 38.37°N | Pleiades hidden 36–43 days for arcus visionis 14–16° (Hesiod's 40 [*WD* 385–386]); Arcturus ≥ 5° at the end of nautical twilight from 26 Feb, 60 days after the 28 Dec 702 BC solstice [*WD* 564–567], within ±2 days | computed with Meeus-based code [vis §3.3]; to rerun with `ephem` |
| I4 | lunar eclipses (new module) against NASA LEcat5 rows for the PC-R dates | umbral magnitude within 0.02; greatest eclipse within 3 min after the ephemeris offset | to run |

### 4.2 PC-S: synthetic Odyssey-shaped clue sets

The question: when the clues really are observations, does B&M's method
recover the date, and how often uniquely?

1. **Truth dates t\*** from two pools in 1400–600 BC: (a) every new moon with
   a solar eclipse of magnitude ≥ 0.95 at some Greek-world site (NASA 5MCSE);
   (b) 1,000 ordinary new moons drawn at random [ctl §7.2].
2. **Describe the real sky** at t\* with B&M's slots and grammar, taking at
   each slot the strictest statement that is true: Venus on Day −5 (lead
   ≥ 120/90/60 min, morning visible, evening, invisible); Mercury on Day −34
   (the nearest of MWRA, elongation, station and first visibility, with its
   abs Δ bin 1/2/3, or "not near a turning point"); the season on Days −29 to
   −12 (spring, autumn or none); Day 0 New Moon.
3. **Search** with B&M's method, unchanged, in a 136-year window with t\* at a
   random position.
4. **Noise:** (i) none; (ii) every offset jittered ±1 day, the sequential–
   parallel ambiguity [chron §5]; (iii) the true turning-point date displaced
   by 3 days for Mercury and 16 for Venus, the slack of the Almagest's own
   records [ctl §4.19]; (iv) one clue replaced by a statement true of a
   different random date.
5. **Report** recall (t\* among the survivors), P(unique), the n_other
   distribution, and for pool (a) P(unique ∧ t\* is the eclipse), the LR
   numerator.

Pass for the instrument: recall ≥ 0.99 at zero noise. Anything less is a bug.
Everything else is a measurement, and its expected values are in section 6.

### 4.3 PC-R: real passages with independently known dates

Each is given to the method blind: the clue types and intervals the ancient
text states, its site, and a 136-year window with the truth at a pre-drawn
random position. Recall and n_other are scored. Texts are in `data/text/`,
exported read-only from the library [ctl §9].

| set | text | clue set given to the method | truth | pass looks like |
|---|---|---|---|---|
| R1 | Ptolemy, *Almagest* IV.6 (4.6.3–5) | three lunar eclipses at Babylon, 354 and 177 days apart [me: from the dates]; total, then 3 digits from the south, then more than half from the north; first mid-eclipse about 2½ h before midnight, second at midnight | 19/20 Mar 721 BC (−720), 8/9 Mar and 1/2 Sep 720 BC [ctl §4.19] | truth recovered and unique |
| R2 | *Almagest* IV.6 (4.6.13–15), IX.8, X.1 | three lunar eclipses AD 133–136 at Alexandria with their intervals; Venus greatest evening elongation and Mercury greatest morning elongation at their recorded day offsets | AD 133 May 6, 134 Oct 20, 136 Mar 6; Venus 8 Mar 132; Mercury 2/3 Oct 134 [ctl §4.19] | run twice. Eclipses only: recovered and unique. With the planets at B&M's ±1-day tolerance: recall fails (known: the records are 3 and 16 days off) |
| R3 | Thucydides 2.28, 4.52, 7.50 | solar at new moon, summer of war-year 1, after midday, crescent, Athens; solar near new moon, start of summer, year 8, morning, Athens; total lunar at full moon, late summer, year 19, Syracuse | 3 Aug 431 BC, 21 Mar 424 BC, 27 Aug 413 BC [ctl §4.1–4.3] | recovered and unique |
| R4 | Xenophon, *Hellenica* 1.6.1, 2.3.4, 4.3.10 | lunar in the evening (year n, Athens); solar in the morning (n+2, Pherae); solar crescent in summer (n+12, Coronea) | 406, 404, 394 BC [ctl §4.4] | recovered |
| R5 | Plutarch *Alex.* 31.4; Arrian 3.7.6, 3.15.7; Curtius 4.10.2; Pliny *NH* 2.180 | total lunar eclipse, autumn, second hour of night at Arbela, at moonrise in Sicily; battle 11 nights later | 20 Sep 331 BC [ctl §4.15] | recovered; n_other measured (single-eclipse sets are not expected to be unique) |
| R6 | Livy 44.37; Plutarch *Aem.* 17 | lunar from the 2nd to the 4th hour of night at Pydna, summer; battle next day; Roman date with unknown calendar offset | 21 Jun 168 BC [ctl §4.10] | recovered |
| R7 | Diodorus 20.5.5 | total solar eclipse at sea between Sicily and Africa, morning, late summer, the day after the escape | 15 Aug 310 BC [ctl §4.9] | recovered; n_other measured |
| R8 | Livy 22.1.9, 30.38.8, 37.4.4, 38.36.4 | four solar "diminished sun / darkness" prodigies with consular years 14, 13 and 2 years apart, sites Rome and Cumae | 217, 203, 190, 188 BC [ctl §4.11–4.12] | recovered |

Pass for the set: recall in at least 6 of 8 (R2 counted on its eclipses-only
run). Below 4 of 8, the method cannot recover real dated clue sets and every
Odyssey result is reported as "could not have seen it".

The language-to-magnitude control (I2b's seven eclipses) is used for one
thing only: to justify X4 and to show that a darkness phrase such as Od.
20.356–357 does not by itself require totality (Plut. *Pel.* 31 describes
darkness over the city at magnitude 0.67) [ctl §0 item 3].

Single-eclipse cases with two astronomical candidates (Archilochus: 711 and
648 BC both total at Thasos; Ennius: 405 and 400 BC both about 0.73 at Rome)
are run as a demonstration that the choice comes from outside chronology, not
astronomy [ctl §0 item 4].

### 4.4 Negative controls

Fictional or legendary narratives with the same kinds of sky clue, composed
long after the events they describe, plus a calendar poem and a text whose
clues contradict each other. Each gets its literal reading and its own garden
built from the same fork types, the reproduction and primary windows, and the
same eclipse classes at a site it names.

| set | text and lines | clue set | site | expected (stated now) |
|---|---|---|---|---|
| NC1 | Iliad: 16.567 (Zeus' deadly night), 17.366–368 (sun and moon not safe), 18.239–241 (early sunset) on the day of Patroclus' death, Day D; 23.226–228 Heosphoros at the dawn after the pyre night; Shield stars 18.486–489 as a season fork | Day D a new moon with darkness (the eclipse slot); Venus morning star at D + Δ, Δ fixed from the Greek day count before the run (Papamarinopoulos et al. 2014 used three days [crit §5]); season fork from the Shield stars | Troy, Hisarlık (39.96°N 26.24°E [me: from memory, to be checked]) | survivors at about the Odyssey's rate; some reading makes an eclipse new moon unique. Papamarinopoulos et al. 2014 claim 6 Jun 1218 BC [crit §5, read]; Henriksson 2012 claims 24 Jun 1312 BC [crit §5, *secondary*] |
| NC2 | *Aeneid* 2.255 (the fleet sails under a friendly silent moon), 2.801 (Lucifer rising over Ida at dawn) | Moon up and at least half lit on the night of Day 0; Venus morning star on Day +1 | Troy | many survivors; no uniqueness without extra forks |
| NC3 | *Argonautica* 1.1202 (Orion's wintry setting), 1.1273 (morning star as Heracles is left behind); 4.1695–1697 (moonless dark night) as a separate set | season from Orion's setting; Venus morning star at Day +1; moonless night | Cius (Gemlik) | as NC2 |
| NC4 | Homeric Hymn to Hermes 17–19, 97–100, 141 | born at dawn on the 4th of the month; Moon climbing near dawn; moonlight all night | Pylos | **zero survivors** in every window: a 4-day Moon sets in the evening [ctl §6.5] |
| NC5 | Hesiod *WD* 383–385, 564–567, 609–611, 615–621 | the star calendar used as event clues around an arbitrary Day 0 | Ithaki | about one survivor per year: never unique |

Two consistency checks run beside the negatives:

- **Iliad against Odyssey.** If both texts carry real dates, the Iliad's date
  (the tenth year of the war) must fall about 8–12 years before the Odyssey's
  (return in the twentieth year [win §5]). For the pinned B&M-analogue
  readings, report the offset and its base rate (the chance that an
  unrelated survivor falls in a given 5-year band).
- **Cross-text competition.** Count how many distinct texts and readings the
  garden attaches to each X1–X3 eclipse. The notes list 30 Oct 1207 BC as
  claimed for both the Odyssey and Joshua 10, and 30 Sep 1131 BC for Joshua
  [crit §0 item 7, *secondary*]. Joshua is outside the grammar and is not run.

**Pass and fail for the method.** The method is specific if (i) NC4 returns
no survivors, (ii) NC5 returns no unique survivor, and (iii) the garden reach
G of NC1–NC3 is no higher than that of random epics of the same structure
(N4). If the Odyssey's G and its eclipse coincidence fall inside the range of
NC1–NC3, the Odyssey result is reported as what the method does to any epic.

### 4.5 What the controls decide

- PC-R recall below 4 of 8, or PC-S recall below 0.5 at noise level (ii)
  with the garden's widest tolerances → outcome 3 (the method cannot see),
  whatever N3 says.
- PC-S P(unique) below 0.3 at noise levels (ii) and (iii) → uniqueness is not
  what true observations of this grammar produce. B&M's "single date" is then
  reported as a property of the window, and only G and the LR carry weight.
- An NC1–NC3 text dating itself to an eclipse with G ≥ 0.05 → outcome 4.

---

## 5. Clues B&M did not use

From the 76-row inventory [txt §4]. None of these is used to fit anything. Each
testable one is evaluated (i) on 16 Apr 1178 BC, (ii) on every survivor of
every garden reading, and (iii) on random candidates for its base rate. If the
clues record a real sky, held-out sky clues should pass more often among the
survivors than their base rate; if they do not, at the base rate.

| # | clue (lines; day) | class [txt §4] | testable? | predicate (frozen now) | how it enters |
|---|---|---|---|---|---|
| H1 | "this night is very long" (11.373; Day −7 seq); "these nights are endless" (15.392; Day −3) | C, weak | yes | night (Sun centre below −0.833°) ≥ 12.0 h on that night | held-out. Known for 1178 BC: 11.5 h and 11.3 h, fail [txt §5.6]. The scholia read autumn from 11.373 [txt §5.6] |
| H2 | σκοτομήνιος, the dark night (14.457; night of Day −5 seq / −4 par) | B | yes | Moon above the horizon for < 25% of the dark hours | consistency only: given Day 0 a conjunction it holds almost always, so it carries no information [vis §4.5; txt §5.2]. Base rate 24–31% of nights |
| H3 | Hermes leads the suitors' souls past the gates of the Sun (24.1–14; night of Day 0/+1) | D, but B&M's own rule applies | yes, under the Hermes = Mercury rule | (a) Mercury not visible (arcus visionis 10°) on the mornings and evenings of Day 0 and +1; (b) Mercury within ±3 days of a conjunction with the Sun | a test of the rule's consistency: B&M apply it to book 5 and not to book 24 [txt §5.9] |
| H4 | Ares and Aphrodite caught together (Demodocus' song, 8.266–366; Day −7 seq) | listed by Gainsford among the god-movements a consistent method must accommodate [crit §3.3] | yes, under the same rule | Venus–Mars separation ≤ 5° within ±3 days of Day −7 | consistency of the rule; base rate computed |
| H5 | Mars invisible in March–April 1178 BC except during the eclipse | B&M's own post-hoc support [bm §2] | yes | Mars not visible (arcus visionis 11.5°) on any morning or evening from Day −34 to Day 0 | reported with its base rate; not counted, because it was found after the date |
| H6 | the twentieth year (9 lines); a year with Circe and seven with Calypso | chronological [win §5] | yes, against ancient sack dates | year lies 8–11 years after one of the ancient sack dates (Duris 1334/3 to Ephorus 1135) | external check; reported per survivor. Strict Eratosthenes alone excludes 1178 BC [win §6] |
| H7 | Theoclymenus at the δεῖπνον; supper "in the light" (20.390–394, 21.428–429) | B | partly | eclipse maximum in daylight on Day 0 | consistency only; "noon" is not in the text [txt §5.10] |
| H8 | starry pre-dawn sky without cloud (20.98–121; Day 0) | B | implied by N | Moon not visible before dawn on Day 0 | consistency only |
| H9 | frost feared (5.467, Day −9; 17.25, Day −1); hearth and fires (6.305, 7.153, 18.307–311, 19.63–64) | C, weak | no | — | weather, not sky. Reported qualitatively, with the five scholia that read autumn or winter [txt §5.6] |
| H10 | nightingale at the start of spring (19.519), swallows (21.411, 22.240), gadfly in spring (22.301 = 18.367) | D or weak B; similes | no | — | excluded: similes carry no date [txt §5.4] |
| H11 | much-flowering wood (14.353) | inside a lying tale | no | — | excluded |
| H12 | Laertes digging round a plant (24.226–231; Day +1) | B, weak | no | — | qualitative |
| H13 | Helios' complaint (12.374–390), Poseidon and Zeus (13.125–158) | Gainsford's list [crit §3.3] | no | no operational predicate is defensible | listed, not run |

The held-out statistic: the number of testable astronomical predicates (H1,
H3a, H3b, H4) that 1178 BC passes, against the Poisson-binomial distribution
from their base rates; and, over all garden survivors, the pass rate against
the base rate. Power is low with so few survivors, and the report says so.

---

## 6. Pre-registered predictions

Written 2026-10-03, before any null model, control or held-out check of the
bench was run. The notes' exploratory computations existed; the results among
them that touch a prediction are in 2.5, and the rough rates the predictions
cite are tagged. Each prediction names the threshold that decides it.
"Known" marks an outcome the notes already contain; those are listed for
completeness and are not counted as confirmations.

**Reproduction**

1. T0b instrument checks A1–A5 all pass. *(Known for A1–A4 on S2's own Ti.)*
2. 16 Apr 1178 BC passes N, C, V and M under the pinned conventions.
   Decided by the four pass flags.
3. The N ∧ C ∧ V ∧ M survivors in 1250–1115 BC number at least 2 and include
   18 Mar 1189 BC. Confirmed if the count is ≥ 2 and 1189 BC is among them.
   *(Expected from 2.5; the full recomputation is new.)*
4. Adding E (≤ 5 Apr) leaves 1178 BC alone. Confirmed if the survivor set is
   exactly {1178 BC}.
5. Hence the T0 verdict is "reproduced only with the equinox".

**Rates and coincidence**

6. The background rate of N ∧ C ∧ V ∧ M survivors over 1500–600 BC is at least
   0.24 per century, five times B&M's one in 2,088 years (0.048 per century),
   with a Poisson 95% interval excluding 0.048. The notes' rough estimate is
   about 0.8 per century [vis §5].
7. Over 1500–600 BC there are at least 4 such survivors, and the empirical
   P(≥ 1 survivor in a 136-year window) is at least 0.4.
8. p_fix, the probability that a spring New Moon (one that passes N and C)
   fixed in advance passes V and M, lies between 0.002 and 0.02 (rough
   estimate 0.008 [vis §5]). If it
   does, a pre-registered version of B&M's test would have been notable at
   that level: the bench is not stacked against the claim.
9. The dependence ratio (joint pass rate over the product of marginals) for V
   and M on spring New Moons lies between 0.5 and 2: no strong dependence.

**Forking paths**

10. G_BM, the reach over B&M's own 72 readings, is at least 3 × p_fix,unique.
11. G for the full eclipse-compatible garden is at least 0.10: some defensible
    reading makes a random daylight New Moon the unique match in at least one
    case in ten. If G ≥ 0.05, the eclipse coincidence is not significant at
    the 5% level after look-elsewhere; if G ≤ 0.01, it is, and the report
    says so first.
12. Some eclipse-compatible reading makes 30 Sep 1131 BC (−1130) the unique
    survivor of a 136-year window that contains it. Confirmed by ≥ 1 reading.
13. Some eclipse-compatible reading makes 24 Jun 1312 BC (−1311) the unique
    survivor of a 251-year window that contains it. Confirmed by ≥ 1 reading.
14. G over the X1–X3 eclipse new moons is within a factor 2 of G over P_day:
    eclipse dates are not specially reachable.

**Random epics**

15. For B&M-shaped random epics (variant A), P(unique survivor in a 136-year
    window) lies between 0.2 and 0.6.
16. P(T_best ≥ T_obs) ≥ 0.2: in at least one random epic in five, some date
    in the window matches at least as tightly as 1178 BC matches the Odyssey.
17. The fixed-reading double hit (unique survivor that is an X1 eclipse) is
    ≤ 0.005 per epic.

**ΔT**

18. The equal-weight mixture over the five ΔT models gives P(total at
    Ithaki, 16 Apr 1178 BC) between 0.15 and 0.40, and P(magnitude ≥ 0.9)
    ≥ 0.8. *(Per-model values known: 0.11–0.51 [eph §5.4]; the mixture is
    new.)*
19. P(total at Ithaki) is higher for 30 Sep 1131 BC than for 16 Apr 1178 BC
    under every model, and the joint probability that both were total is
    ≤ 0.05.
20. Fewer than 2% of candidates in 1250–1115 BC change their UT+2
    conjunction date between B&M's ΔT and SMH2020 ± 1σ, and the T0b survivor
    set does not change.

**Controls**

21. PC-S at zero noise: recall ≥ 0.99 (instrument) and P(unique) ≤ 0.6 for
    B&M's grammar in 136-year windows, because about one chance competitor is
    expected per window [§1.2].
22. PC-S with ±1-day offsets and the Almagest slack (Mercury 3 days): recall
    at B&M's ±1-day tolerance ≤ 0.7.
23. PC-R: recall in ≥ 6 of 8 sets; unique in R1, R3 and R8 at least.
24. NC4 (Hymn to Hermes) returns zero survivors in every window; NC5 (Hesiod)
    returns no unique survivor.
25. At least one of NC1–NC3 has an eclipse-compatible reading whose unique
    survivor is an eclipse of magnitude ≥ 0.75 at its site, and the G of
    NC1–NC3 is within a factor 2 of the Odyssey's.

**Held-out clues**

26. 16 Apr 1178 BC passes no more of the four testable held-out predicates
    (H1, H3a, H3b, H4) than their base rates predict (Poisson-binomial
    p > 0.1). *(H1 is known to fail.)*
27. Over all garden survivors, the held-out pass rate is within the base
    rate's 95% interval.

**Bottom line**

28. LR_garden < 10.
29. The verdict under the rule below is outcomes 2 and 4 together: the
    Odyssey's G ≥ 0.05 and LR_garden < 10 (the match is ordinary), PC-R
    recall ≥ 6/8 (so not outcome 3), and at least one of NC1–NC3 dates
    itself to an eclipse as in prediction 25 (the method dates fiction).

**Decision rule for the verdict**, applied mechanically by `verdict.py` in
this order:

| outcome | condition |
|---|---|
| 3, the method cannot see | PC-R recall < 4/8, or PC-S recall < 0.5 at noise level (ii) with the garden's widest tolerances |
| 1, the text dates the return | not 3, **and** T0 reproduced (either form) **and** G ≤ 0.01 **and** LR_garden ≥ 30 **and** every NC1–NC3 G ≥ 10 × the Odyssey's |
| 2, the match is ordinary | not 3, not 1, **and** (G ≥ 0.05 **or** LR_garden < 10) |
| 4, the method dates fiction | not 1, **and** some NC1–NC3 text has G ≥ 0.05 and an eclipse-compatible reading whose unique survivor is an eclipse of magnitude ≥ 0.75 at its site |

Outcomes 2 and 4 can hold together and are then both reported. A result that
meets none of the conditions (for example 0.01 < G < 0.05 with LR_garden
between 10 and 30) is reported as inconclusive, with the numbers and the
thresholds beside them.

---

## 7. Software, run order and run times

### 7.1 Modules (`odybench/`)

| module | status | contents |
|---|---|---|
| `ephem.py` | built, validated | DE441/DE431 positions, ΔT models with sigmas, precession, new moons, solar-eclipse geometry and totality windows [eph §9] |
| `ccx.py` | built | read-only access to the ClassicaCodex library. It is the only way the bench touches the library; nothing writes to it |
| `sky.py` | new | daily sky tables (3.1) over a span, cached as `data/cache/sky_<y0>_<y1>_<dt>.npz`. Rise and set by Meeus' iterated hour-angle method on positions from `ephem` (about 3 evaluations per event), not by fine grids. Works in yearly chunks, because `ephem.kernel()` needs one excerpt to cover each request |
| `events.py` | new | stations, greatest elongations, rise- and set-azimuth extrema, first and last visibility, heliacal star phases, equinoxes, full moons, Yallop q |
| `eclipses.py` | new | solar-eclipse catalogue at sites from NASA 5MCSE elements (from `results/research-critiques/eclipse_local.py`), ΔT envelopes, classes X1–X4; DE431/DE441 local circumstances via `ephem` |
| `lunar.py` | new | lunar eclipses for PC-R, validated against NASA LEcat5 rows (I4) |
| `s2.py` | new | Table S2 loader and colour rules (from `results/bm2008-reconcile/s2_counts.py`) |
| `clues.py` | new | the clue grammar: a clue is (body, phenomenon, offset or span, threshold); a reading is a set of clues plus Day-0 and window choices; `evaluate(reading, pool)` returns a boolean array |
| `readings.py` | new | the B&M reading, the forks F1–F7, the full, eclipse-compatible, G_BM and G_1 gardens |
| `reach.py` | new | the offset intervals of 3.4, their union over readings, sliding-window P(≥ 1) |
| `epic.py` | new | the random-epic generator (3.5) |
| `stats.py` | new | Poisson and binomial intervals, hypergeometric tail, Poisson-binomial, permutation tests, bits |
| `prereg.py` | new | hash check of the frozen files (7.4) |

### 7.2 Scripts (top level, as in labench)

| script | test | writes |
|---|---|---|
| `reproduce.py` | T0a, T0b, T0c | `results/t0/` |
| `rates.py` | N1 | `results/n1/` |
| `coincidence.py` | N2 | `results/n2/` |
| `garden.py` | N3 | `results/n3/` |
| `randomepic.py` | N4 | `results/n4/` |
| `windows.py` | N5 | `results/n5/` |
| `deltat.py` | N6 | `results/n6/` |
| `synthetic.py` | PC-S | `results/pcs/` |
| `controls.py` | I2b–I4, PC-R | `results/pcr/` |
| `negatives.py` | NC1–NC5 and the two consistency checks | `results/nc/` |
| `heldout.py` | section 5 | `results/heldout/` |
| `verdict.py` | section 6, decision rule | `results/VERDICT.md`, then the findings in `README.md` |
| `read.py` | a reader: `py read.py -1177-04-16` prints the sky of Days −40 to +1 beside each clue and each held-out predicate, as labench's `read.py HT88` prints a tablet | stdout |

Every script writes a machine-readable `<name>.json`, a human-readable
`<name>.out.txt` and, where useful, `.tsv` tables, and stamps each output with
the prereg hash it ran under.

Tools: `tools/fetch_ephem.py` (extend), `tools/validate_ephem.py` (exists),
`tools/build_sky.py`, `tools/fetch_stars.py`, `tools/freeze.py`.

Tests: `tests/test_ephem.py` (exists); `tests/test_t0.py` (S2 replay, the 1178
row values of A4); `tests/test_reach.py` (hand-built interval cases);
`tests/test_clues.py` (the B&M reading on the S2 rows); `tests/test_eclipses.py`
(the port against the JavaScript output).

### 7.3 Data to acquire

| what | from | size | why |
|---|---|---|---|
| DE441 excerpt −1560 to +230, targets as now | NAIF `de441_part-1.bsp` by HTTP Range (`tools/fetch_ephem.py`) | about 185 MB [me: 30.0 MB per 290 years, scaled] | the current excerpt covers only −1320 to −1030 [eph §1]: it misses the first 29 years of the primary window, all of the background and every control |
| DE431 eclipse excerpts (±60 d) for −1339 and −647 | NAIF `de431_part-1.bsp` | about 30 kB each | SMH pairing for 1340 BC (Gainsford's list) and Archilochus; the other eclipses in N6 are inside the existing DE431 excerpt |
| Hipparcos and radial velocities for Sirius (HIP 32349), Aldebaran (21421), Betelgeuse (27989), Rigel (24436), Dubhe (54061) | VizieR I/311/hip2, SIMBAD TAP, as in [eph §4] | small | grammar stars; HIP numbers to be confirmed at fetch [me: from memory] |
| NASA LEcat5 century pages for the PC-R lunar eclipses | eclipse.gsfc.nasa.gov | small | I4; some are already in `results/controls/nasa/` |
| NASA JSEX elements −1999 to −1500 | eclipse.gsfc.nasa.gov/JSEX/ | about 85 kB per century | only if the background is extended past 1500 BC |

Fetch from PowerShell or Python's urllib (Git Bash's curl has a 2020 CA
bundle). No library access beyond `odybench.ccx`.

### 7.4 Freezing

`tools/freeze.py` writes `results/PREREG.sha256`: the SHA-256 of this file and
of every file in `data/prereg/` (`readings.json`, `garden.json`,
`eclipse_classes.json`, `windows.json`, `epic_grammar.json`, `controls_real.json`,
`negatives.json`, `heldout.json`, `seeds.json`). Every analysis script checks
the hashes at start and stops on a mismatch. `--unfrozen` lets it run but
stamps every output EXPLORATORY in its first line. Changes after freezing are
allowed only as a dated amendment appended to this file, naming what changed
and why, in the way indusbench recorded its correction to test 1
[indusbench DESIGN §4]. The amendment is then frozen again and the new hash
line is appended to `PREREG.sha256` under the old one, so the file keeps the
whole history. Odybench is not a git repository, so this file is the record;
committing it somewhere public would add an outside timestamp.

### 7.5 Run order and expected times

Measured on this machine [me: `results/design-timing/timing.py` and
`timing.out.txt`, 2026-10-03]:
`ephem.new_moons` over 136 years takes 23.0 s (1,682 conjunctions);
`ephem.altaz` runs at about 28,000–29,000 body-positions a second (1.7 s for
49,673 times; 17.3 s for 480,000). `validate_ephem.py` took 188 s [eph §10].
The other figures are estimates from these.

| # | step | command | estimate | basis |
|---|---|---|---|---|
| 0 | fetch ephemeris extension and stars | `py tools/fetch_ephem.py`, `py tools/fetch_stars.py` | 5–20 min | network-bound, about 185 MB |
| 1 | validate | `py tools/validate_ephem.py`; `py tests/test_ephem.py` | 3–4 min | measured 188 s |
| 2 | freeze | `py tools/freeze.py` | seconds | |
| 3 | sky tables, 1560 BC–AD 230 | `py tools/build_sky.py` | 30–90 min, once | about 60 evaluations per day (rise and set of 7 bodies at 3 each, 7 stars at 2 twilights, the twilights themselves) over 654,000 days is 39 million, about 25 min at 28,000 a second; new moons add about 5 min at 23 s per 136 years |
| 4 | T0 | `py reproduce.py` | 5 min | 136 years of tables |
| 5 | N1, N2 | `py rates.py`; `py coincidence.py` | under 1 min each | lookups on cached tables |
| 6 | N6 | `py deltat.py` | 20–40 min | about 45 totality windows, each a bisection over local circumstances (not yet timed) |
| 7 | N3 | `py garden.py` | 10–30 min | 428,544 readings × about 11,000 candidates as packed boolean ANDs, then interval unions |
| 8 | N4 | `py randomepic.py` | 20–60 min | 20,000 epics as lookups; 1,000 epic gardens of 1,000 readings |
| 9 | N5 | `py windows.py` | 5 min | reuses N1–N3 arrays |
| 10 | PC-S | `py synthetic.py` | 10 min | about 2,000 truth dates × 4 noise levels |
| 11 | PC-R, I2b–I4 | `py controls.py` | 10–20 min | needs step 3's later span |
| 12 | NC | `py negatives.py` | 10–20 min | Troy-site tables for the Iliad and Aeneid |
| 13 | held-out | `py heldout.py` | 2 min | |
| 14 | verdict | `py verdict.py` | seconds | |

About 2.5 to 5 hours in all, most of it in step 3, which is cached and run
once.

---

## 8. What the dossier could not settle, and how each is handled

| # | open fact | why it is open | handling |
|---|---|---|---|
| 1 | What "Ti = New Moon" means operationally | No single rule reproduces S2's Ti column; shifted and unshifted rows interleave at the same clock hours [bm §5 N] | T0b pins the UT+2 conjunction date (136/152); fork F2 carries LMT, +1 day and first crescent |
| 2 | Which New Moon when two qualify; S2's out-of-window Ti in 1246, 1227 and 1243 BC; 1243 BC's Ti is not a New Moon | S2 follows no consistent rule [bm §7] | T0b evaluates every qualifying New Moon; T0a replays S2 as printed and flags the rows |
| 3 | Why 14 S2 MWRA dates sit 4–8 days from DE441's rising-azimuth maxima, all in February–March | Starry Night's Mercury theory, a different horizon, or values read off plots [bm §5 M] | DE441 maxima used; the S2-MWRA replay is reported beside it; agreement ≥ 124/152 is an acceptance check |
| 4 | Mercury's visibility on Ti−34 | Never tabulated; PLSV's extinction parameters unknown [bm §5 M] | arcus visionis 10° (Ptolemy) in T0b; visibility on and off in F5; a physical extinction and sky-brightness model (Schaefer type) is an upgrade, not a prerequisite [vis §6 item 1] |
| 5 | The Pleiades and Arcturus cutoffs (17 Feb; 3, 4 or 5 Apr; 40 or 44 days hidden) | Three dates in the paper and SI; PLSV model unknown; 1178 BC sits on the late bound [bm §5 C] | T0b uses the stated 17 Feb / 4 Apr; F3 recomputes them each year at 2° and 5°, with the arcus visionis calibrated on Hesiod's 40 days (I3) |
| 6 | The ṅ and ΔT formula of Starry Night 6.0.4 | Not published by B&M, and the software itself was not available to check [crit §2.3; ctl §11 item 1] | 27,602.7 s is used only as the clock ΔT in T0b; never for eclipse geometry; its converted value is reported as uninterpretable (N6 item 7) |
| 7 | ΔT at −1177 | SMH's own formulations span 681 s, about one stated sigma; before −720 every value is extrapolation [eph §2.3, §8] | five models, each with its sigma, and their equal-weight mixture (N6) |
| 8 | Whether the HMNAO ε is a Gaussian 1σ | The authors call the extrapolation conjectural [eph §8 item 1] | stated as an assumption every time it is used; the ±2σ range reported beside |
| 9 | Lunar ephemeris to pair with SMH ΔT | DE441's tidal acceleration is not published; DE441 − DE431 = +188 s at −1177 [eph §5.3] | DE431 for SMH-paired eclipse work; NASA elements for the canon; DE441 for planets and for the clue tests; differences reported |
| 10 | Which island is Homeric Ithaca | Modern dispute; windows differ by up to about 120 s [eph §5.4; crit §2.3] | Ithaki primary; four sensitivity sites |
| 11 | Departure hour from Ogygia (20 or 19 days to Scheria) and Athena's night in Sparta (Venus at −5 or −4) | The Greek does not say [chron §4.B, §4.F] | the 8-row grid F1 |
| 12 | What Day 0 is: conjunction, noumenia or a 20-day window; Apollo's feast on the new moon or the 7th | Text silent; ancient sources split [txt §5.1, §5.3; vis §4] | F2 (a)–(d); the 7th as an epic anchor in N4; the window reading is dominated and left out (3.4) |
| 13 | Greek day boundary (sunset or dawn) | Not verified from a primary source [vis §6 item 4] | F2 (d) uses a sunset day; (c) a civil day; both are in the garden |
| 14 | The meaning of "late-setting" Boötes | B&M's late, the scholia's slow, Aratus' autumn evenings [txt §5.8; vis §3.1] | F3 (a)–(f), including autumn and none |
| 15 | Whether the morning star is Venus | Homer's names are separate; the identity is 6th–5th century BC [vis §1.4] | F4 includes any bright herald and none |
| 16 | The equinox bound (≤ 4, ≤ 5 or ≤ 6 Apr) | Three versions in paper and table [bm §5 E] | F6 carries all three; T0 reports each |
| 17 | The window (text 1250–1115 BC; S2 1251–1100 BC) | Endpoints not stated; window drawn from the tradition that chose the eclipse [bm §6; win §6] | reproduction uses the text's window; S2's extra rows (1111 BC) reported; N5 runs five windows |
| 18 | Which three lines schol. 14.162 suspects; whether 14.161–164 is interpolated | Commentaries not available [txt §10] | N dropped is dominated (3.4); every result is stated conditional on 14.162 = 19.307 being read as a month-turn statement at all |
| 19 | Primary sources not read: P. V. Neugebauer 1929; MacDonald 1967; Starry Night and PLSV internals; de Jong's Appendix A; Stanford 1959; the Oxford commentaries; P.Oxy. 3710; Austin 1975; Papamarinopoulos et al. 2012; Henriksson 2012 | Paywalls, empty responses, books not to hand [bm §1; chron §8; crit §8; txt §10] | No computed number depends on them. Where their content enters (MacDonald's March reading, Austin's autumn, Papamarinopoulos' 1207 BC) it enters as a fork option or a listed date, tagged *secondary* |
| 20 | Herwart von Hohenburg's 1612 date | Known only through Fotheringham 1921 [crit §1.2] | historical note only |
| 21 | Arcus visionis models are crude | AV bands stand in for extinction and sky brightness; weather shifts first and last dates by ±3 to ±15 days [vis §1.2, §6] | AV values are forks; the spread they cause is reported; PC-S noise level (iii) covers the slack |
| 22 | The 1178 and 1131 BC ΔT errors are correlated | 47 years apart [win §7.1] | joint probabilities under a common ΔT offset (N6 item 5) |
| 23 | The prior for oral transmission of a dated sky | No comparative case found; the gap is 435–580 years, about 400 of them without writing [win §10–11] | not quantified; the bench reports likelihood ratios only |
| 24 | Ephemeris coverage | The DE441 excerpt covers −1320 to −1030 only [eph §1] | step 0 of 7.5 fetches −1560 to +230 before anything else runs |
| 25 | Ancient Troy dates other than Eratosthenes and Duris | Ephorus, Sosibius, Timaeus, Dicaearchus and Eretes come from Wikipedia and B&M, not FGrHist [win §3, §12] | used only as the envelope of the primary window and in H6; tagged *secondary* |
| 26 | Hermes = Mercury, and whether any god-movement is astronomical | No ancient parallel; first attested in Plato [B&M §Historical Plausibility; txt §5.9; crit §3.3] | not adjudicated: F5 "none" is a fork, and H3–H4 test the rule's consistency |

---

## Sources

The dossier, all in `docs/`, written 2026-10-03:

- `research-bm2008.md`, the reconciled spec of Baikouzis & Magnasco 2008,
  merging `research-bm2008-a.md` and `-b.md`; scripts in
  `results/bm2008-reconcile/`.
- `research-chronology.md`, the day count from the Greek; the 8-row grid.
- `research-textclues.md`, the 76-row clue inventory; scripts in
  `docs/textclues-scripts/`.
- `research-ephemeris.md`, the computation stack (`odybench/ephem.py`,
  `tools/validate_ephem.py`, `results/validate_ephem.txt`).
- `research-visibility.md`, chance rates for each clue reading;
  `docs/research_visibility_calc.py`, `results/research-visibility.json`.
- `research-controls.md`, positive, hard and negative controls;
  `results/controls/`.
- `research-critiques.md`, the responses since Schoch; the Ithaki eclipse
  table; `results/research-critiques/`.
- `research-window.md`, the search window, eclipse base rates at Ithaca and
  window scaling; `results/window/jsex/`.

Primary items behind them, as the notes read them: Baikouzis & Magnasco, PNAS
105 (2008) 8823–8828, doi:10.1073/pnas.0803317105, with its Supporting
Information and Table S2 (`data/bm2008-a/`); Schoch, *The Observatory* 49
(1926) 19–21; Gainsford, *TAPA* 142 (2012) 1–22; Espenak & Meeus, *Five
Millennium Canon of Solar Eclipses* (NASA TP-2006-214141) and its JavaScript
Explorer; Stephenson, Morrison & Hohenkerk 2016 and the Addendum 2020; JPL
DE441 and DE431 (Park et al. 2021); the Odyssey, Iliad, scholia and the
library texts listed in [ctl §9], exported read-only from ClassicaCodex. The
bench designs this follows: `C:\Projects\labench\README.md` and
`C:\Projects\indusbench\DESIGN.md`.
