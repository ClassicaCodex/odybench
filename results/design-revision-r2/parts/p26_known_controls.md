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
  That is what gate 3b still tests (P35).
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
  agree here, 5.3). For n = 74 that is **0.050**, so a threshold of 0.05
  could not be met.
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

  30 Sep 1131 BC therefore lies 16–20 days into the agricultural autumn of
  Hesiod (*WD* 609–611) and 3 days before the astronomical autumn of
  Geminus (1.9: the seasons divided at the equinoxes and solstices; local
  `geminus-grc.tsv` 1.9.1). It was total at Ithaki at canon ΔT, with the Sun
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

