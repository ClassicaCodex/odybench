## 7. Clues B&M did not use

These come from the 76-row inventory [txt §4], and none is used to fit
anything. Since revision 4 this section carries the only evidence that can
give a "yes" (1.3). So it says:

- which clues are blind, and which facts on record settle or constrain
  them;
- how they are scored, and against which pools;
- how the chance of a "yes" is computed before the target is looked at, in
  general and for this target.

### 7.1 The clues, and which are blind

A clue counts only if it meets two tests:

- its reading was formed without the target in view;
- **its value at the target was not settled by facts on record before its
  predicate was frozen** [r1v5 N2 fix 1].
  - "On record" means published, or present in the repository's notes,
    results or data caches.
  - "Settled" covers inference as well as computation.
  - Revision 5's second test asked only whether anyone had *evaluated* the
    predicate at the target. It kept H4 counted because an inference "is
    not a computation", which is a difference of form, not of substance.

That is the uniform rule of 1.1 and 5.3, applied to the clues B&M cited as
support as well as to those they searched with.

| # | clue (lines; day) | predicate (frozen) | status |
|---|---|---|---|
| H1 | "this night is very long" (11.373; Day −7 seq); "these nights are endless" (15.392; Day −3) | night (Sun's centre below −0.833°) ≥ 12.0 h on that night | **not counted** [rev #11]. The threshold was set after the nights of 1178 BC (11.5 h and 11.3 h, a fail) had been computed [txt §5.6], and it measures the season that C already fixes. Reported |
| H2 | σκοτομήνιος, the dark night (14.457; night of Day −5 seq / −4 par) | Moon above the horizon for < 25% of the dark hours | **not counted** (since revision 4). It fails both tests (below). Reported with its conditional base rate |
| H3 | Hermes leads the suitors' souls past the gates of the Sun (24.1–14; night of Day 0/+1) | **one predicate** [r1 N14]: Mercury is not visible (AV 10°) on the mornings and evenings of Day 0 and Day +1, **and** a geocentric conjunction of Mercury with the Sun in ecliptic longitude (inferior or superior) falls within ±3 d of noon (UT+2) on Day 0 or on Day +1 | **counted.** Facts on record constrain its value at the target without settling it (D3–D5 below) |
| H4 | Ares and Aphrodite caught together (Demodocus, 8.266–366; Day −7 seq / −6 par [chron §2.1, §3.1]) | the geocentric Venus–Mars separation at 03:30 UT is ≤ 5° on some day within ±3 d of Day −7 (sequential) or Day −6 (parallel). The count used is the one on which the candidate passes a reading that defines its pool (7.2), and either count will do if it passes on both | **counted, and settled at this target**: facts on record imply that it fails (D1, D2). So the held-out test could not say "yes" for this target (Q_record, 7.2) |
| H5 | Mars invisible in March–April 1178 BC except during the eclipse | Mars not visible (AV 11.5°) on any morning or evening from Day −34 to Day 0 | **not counted**: B&M found it after the date [bm §2]. Reported |
| H6 | the twentieth year (9 lines); a year with Circe and seven with Calypso | the year lies 8–11 years after one of the ancient sack dates (Duris 1334/3 to Ephorus 1135, as in [win §3]; Clement's list [unread §4]) | external check, reported per survivor; strict Eratosthenes alone excludes 1178 BC [win §6] |
| H7 | Theoclymenus at the δεῖπνον; supper "in the light" (20.390–394, 21.428–429) | eclipse maximum in daylight on Day 0 | consistency only, for eclipse-compatible readings; "noon" is not in the text [txt §5.10] |
| H9 | frost feared (5.467, 17.25); hearths and fires (6.305, 7.153, 18.307–311, 19.63–64) | — | weather, not sky. Reported qualitatively, with the five scholia that read autumn or winter [txt §5.6] |
| H10 | nightingale (19.519), swallows (21.411, 22.240), gadfly (22.301 = 18.367) | — | similes, so excluded [txt §5.4]. 18.366–370 is also a wish, read as winter, May or autumn by different advocates, and is used for nothing [unread §2.3] |
| H11 | much-flowering wood (14.353) | — | inside a lying tale, so excluded |
| H12 | Laertes digging round a plant (24.226–231; Day +1) | — | qualitative |
| H13 | Helios' complaint (12.374–390), Poseidon and Zeus (13.125–158) | — | no operational predicate is defensible; listed, not run |

**The disclosure table** (`data/prereg/heldout_disclosure.json`, frozen at the
first freeze) [r1v5 N2 fix 1]. It pairs every target-day fact on record before
H3 and H4 were frozen (revision 1, 2026-10-03 20:25 local) with the predicates
it bears on. Its rows, as drafted for this revision:

| # | fact on record | where, and since when | bears on | status in the table |
|---|---|---|---|---|
| D1 | Mars was not visible in March–April 1178 BC except during the eclipse | B&M 2008, §Historical Plausibility (published 2008); research-bm2008.md l. 64 | H4, H5 | **settles H4, with D2: fails.** An invisible Mars stood within about 20° of the Sun |
| D2 | Venus a morning star far west of the Sun around Day −5: lead 1:42:56 on Ti−5; greatest morning elongation in mid-March | B&M 2008, §Intersecting; MacDonald 1967 p. 327 ("17 March", the year a slip) [unread §2.5]; rev V10 (103.6 min); unread §2.5 (44.3° west on 11 Apr) | H4 | with D1, **settles H4: fails.** Venus 44° west and Mars within about 20° of the Sun cannot lie within 5° of each other on Days −10 to −4 |
| D3 | at the eclipse, all five naked-eye planets within 90° of ecliptic, with each one's magnitude | B&M 2008, Fig. 1; research-bm2008.md l. 596; research-bm2008-b.md l. 410 | H3 (Mercury's brightness on Day 0 bears on its phase), H4, H5 | **constrains H3** |
| D4 | Mercury's spring events of −1177: a morning station on 5 Mar, the greatest western elongation on 19 Mar, and the rise-azimuth maximum about 12.3 Mar | vis §2.3 (2026-10-03); rev #12; 2.9 | H3 (Mercury's superior conjunction follows its greatest western elongation by roughly five weeks) | **constrains H3** |
| D5 | Horizons tables of Mercury and Venus at Ithaki, at dusk on 14 Mar −1177 (Day −33) and at dawn on 10 Apr −1177 (Day −6): quantities 1, 2, 4, 20, 23 (elongation) and 30 | `data/ephem/horizons/venus_mercury_m1177_{03_14_dusk,04_10_dawn}_{199,299}.txt`, fetched 2026-10-03 19:40 local, 45 minutes before revision 1 froze H3 and H4 | H3 (Mercury's elongation six days before Day 0) | **constrains H3.** Its values are not read before the second freeze |
| D6 | the Sun and the Moon at the eclipse | `data/ephem/horizons/sun_moon_m1177_04_16_eclipse_{10,301}.txt` | none | — |

- **How the table is built** (12.1). `tools/disclosure_scan.py` lists every
  file in `docs/`, `results/` and `data/` that holds a quantity of the
  target's sky between Day −40 and Day +1.
  - It matches the files' date strings and JD ranges, and for Horizons
    files the QUANTITIES line of the request.
  - It prints file names, dates and quantity codes, never values.
  - A0 drafts the table from that list and from the published sources, and
    A9 checks it.
  - Neither reads a value that the table marks "constrains": those values
    stay unread until the second freeze.
- **What the table settles.** One field per predicate, `determined`: a value
  (`fail` or `pass`) where facts on record settle it, and `null`
  otherwise. Revision 6 drafts H4 = fail and H3 = null. Q_record and
  Q_contra read only that field (7.2).
- **Why H3 is not marked settled.** D3–D5 limit where Mercury stood near
  Day 0, but whether they fix H3's value cannot be decided without
  evaluating H3 at the target, which the bench forbids before the second
  freeze. 7.3 reports instead how often H3 passes among pool members that
  share D4's Mercury timing, computed with the target masked.

**Why H2 is no longer counted.** It fails both tests:

- **B&M cite 14.457** in support of their new moon. Their text calls it
  "Night −2" [bm-a, clue N; B&M §Method, SI Table S1].
- **Its value at 1178 BC was known.** The dossier computed the Moon's
  circumstances for the night after Day −5 of 1178 BC (moonrise about
  03:48 LMT) [txt §5.2]. That was before revision 1 froze the 25% threshold.
- **It is weak anyway.** Given a Day 0 at conjunction it passes about half
  the time [vis §4.5].

**Why H4 stays in the statistic, and why no predicate is added** [r1v5 N2 fix
2]. The recheck offered two courses, and the third fix asked whether a blind
route to "yes" can still be built.

- **Dropping H4 (course a)** would leave H3 alone. On the design-stage pools
  H3 alone has a floor of 0.208 over the whole background and 0.241 within
  ±700 years [me: `results/design-revision-v6/heldout_epochs.py`]. That is a
  test that cannot say "yes" for any target. It would say less than course
  (b) says: it would hide why the bench cannot say "yes" here.
- **Keeping H4, with a target-side qualifier (course b),** is adopted.
  - H3 and H4 have been frozen since revision 1. The null side keeps both,
    so the rule can still say "yes" for data unlike the Odyssey's (9.5, S1).
  - For this target the disclosure table settles H4, and Q_record prints in
    every verdict that the held-out test could not have said "yes".
  - The table's value for H4 is an inference. If the bench measures H4 as
    passing, Q_contra prints that the record has been contradicted.
  - A predicate believed to fail when it was frozen cannot have been chosen
    to pass. So a pass contradicting the record would not be a product of
    selection, and label 1 would then stand, with Q_contra beside it.
- **No new predicate (fix 3).** A blind route would need a god-movement whose
  day the text fixes and whose sky nobody has on record.
  - The god-movements of the last 40 days are these: Hermes' flight (fitted,
    M), Poseidon's return (fitted, E), the song of Ares and Aphrodite with
    Hermes and Apollo looking on (Day −7, H4), Zeus's thunder from a clear sky
    on Day 0 (20.102–104), and Hermes leading the souls (Day 0/+1, H3).
  - Their planetary sky is on record: B&M's Fig. 1 gives all five planets
    on Day 0 (D3), and D5 gives Mercury and Venus on Day −6.
  - A predicate written now would be written by someone who has read these
    facts.

  So the bench records that it cannot give this target a blind "yes". It
  does not manufacture one.

**What H3 and H4 test.** They test B&M's own encoding hypothesis, that the
poet turned god-movements into planets. If the hypothesis is right, the
other god-movements of the same story should match the same sky.

### 7.2 The counted statistic: an exact rank test on four pools (a rule input)

- **Four null pools** (4.2), all drawn from P_all, without the target.
  - **P_BM**: the candidates of the whole background, −1999..+200, that pass
    at least one reading of 𝒢_BM* (revision 4's pool).
  - **P_MWRA**: the candidates that pass at least one of the twelve MWRA
    readings of 𝒢_BM*. That is C on a day count, a Venus lead of at least
    90 min on that count's Venus day, and a morning rise-azimuth maximum
    within 3.5 d of that count's Mercury day. P_MWRA ⊂ P_BM (revision 5).
  - **P_BM,E and P_MWRA,E** (revision 6): the members of each whose Day 0
    (UT+2 civil date) falls in the Julian years −1877..−477, within ±700
    years of the target's year.
- **Why P_MWRA** [rev #11 fix 1]. The test must compare the target with
  candidates that pass the same N, C, V and M.
  - H3 depends on Mercury's phase, which M fixes. H4 depends on Venus'
    elongation, which V fixes.
  - The target passes only B&M's applied Mercury event, the MWRA (2.9, "the
    target under 𝒢_BM*"). A candidate admitted through a greatest
    elongation or a station has Mercury in another phase at Day −34, and so
    possibly on Day 0.
- **Why the epoch pools** [r1v5 N11]. On the rough rows H3 is not
  stationary over the background (2.9, R21):
  - H3 passes 12 of 41 P_BM members in −1999..−900 against 3 of 35 in
    −899..+200 (Fisher p 0.041), and 8 of 25 against 0 of 18 in P_MWRA
    (p 0.013);
  - within ±700 years of the target, against the rest, the rates do not
    differ (10/49 against 5/27, p 1.0; 6/28 against 2/15, p 0.69).

  A rate that drifts with epoch breaks the exchangeability of the
  whole-background pools. The likely cause is precession, which moves the
  conditioned Day 0 about 31 days against the equinox across the background
  (4.1) and so changes Mercury's apparition 34 days earlier [me].
  - **Why ±700 years.** It is the band of P8's stationarity test and of the
    recheck's proposed sensitivity. A band of ±350 years would leave about
    14 members in P_MWRA,E, whose floor would then be 0.067 [me:
    `results/design-revision-v6/band_counts.py`].
  - **When it was chosen.** With the design-stage null side in view and no
    target-side value; adding pools can only make "yes" harder.
- **None of the pools depends on the slot definitions of 4.2,** so outcome 1
  is free of R2-2's slot question. **Day and night conjunctions both enter,**
  because neither predicate depends on daylight.
- **The score.** In each pool P, s(t) = Σ_{i ∈ {3, 4}} pass_i(t) · (−log10 q_i).
  - q_i is the pass rate of H_i over P ∪ {t_S}.
  - It is computed at the target-side stage, symmetrically in every member,
    so the test is exact.
  - A rarer predicate weighs more. The order of scores is then: passes both;
    passes the rarer predicate only; passes the commoner only; passes
    neither.
- **The p-value of a pool.** p_P = (1 + #{u ∈ P : s(u) ≥ s(t_S)}) / (1 + n_P).
  Ties count against the target.
  - **Membership.** The target must itself pass a reading that defines the
    pool, under the bench's conventions (4.2), or it is not exchangeable
    with the pool's members. If it fails every such reading, p_P is set
    to 1. Its Day 0 lies in the epoch band by construction.
- **p_H := the largest of the four p_P.**
  - **Why it is exact.** Under H0, that the text is unrelated to the sky of
    1178 BC, suppose any one pool is exchangeable with the target. Then that
    pool's p satisfies P(p_P ≤ α) ≤ α for every α, and p_H ≥ p_P. So
    P(p_H ≤ α) ≤ α, with no approximation and no interval, **if any pool is
    exchangeable**. A referee who doubts one pool's matching, on Mercury's
    event or on epoch, cannot fault the test on that ground.
  - **The cost.** Label 1 needs all four pools to agree.
  - **Exchangeability and the eclipse.** The target was chosen for its
    eclipse. Neither predicate involves the lunar node, so eclipse status
    should not change their rates. P10 tests that on P_spring. R20 tests
    the homogeneity of P_BM across Mercury events, and R21 across epochs.
- **Attainability, a null-side quantity** [r2 R2-1 fix 4].
  p_H,min = the largest over the four pools of (1 + x_max,P)/(1 + n_P), where
  x_max,P is the number of members of P that pass both predicates. A target
  passing both earns exactly p_H,min.
  - **When.** p_H,min is computed at the null-side stage, with the target
    masked (12.3), before any target-side number.
  - **Design-stage values** [2.9; me: heldout_attain.py, heldout_strata.py,
    `results/design-revision-v6/heldout_epochs.py`]:

    | pool | n | x_max | floor |
    |---|---|---|---|
    | P_BM | 76 | 1 | 0.026 |
    | P_MWRA | 43 | 0 | 0.023 |
    | P_BM,E | 49 | 1 | 0.040 |
    | P_MWRA,E | 28 | 0 | 0.034 |

    So **p_H,min = 0.040**.
  - **The lattice** (p_BM / p_MWRA / p_BM,E / p_MWRA,E → p_H) [me:
    `results/design-revision-v6/verdict_trace.py`]:
    - passes both: 0.026 / 0.023 / 0.040 / 0.034 → **0.040**;
    - H4 only: 0.039 / 0.045 / 0.060 / 0.069 → **0.069**;
    - H3 only: 0.221 / 0.227 / 0.240 / 0.276 → **0.276**;
    - neither: 1.

    Revision 5's two-pool lattice gave 0.026, 0.045 and 0.227. A target
    passing H4 alone no longer reaches 0.05.
  - **Q_attain** holds if the measured p_H,min exceeds 0.05.
- **Q_record, the floor for this target** [r1v5 N2 fix 2(b)].
  - `attain.py` computes it at the null-side stage, from the measured
    lattice and the frozen disclosure table (7.1).
  - Q_record holds if no pass pattern consistent with the table's
    `determined` values has p_H ≤ 0.05.
  - With H4 = fail, the consistent patterns are "H3 only" (0.276 at the
    design stage) and "neither" (1). So **Q_record holds**.
  - It needs no target-side computation, so it is known at the second
    freeze, and it is printed in every verdict.
- **Q_contra** is computed by `heldout.py` after the second freeze. It holds
  if a measured flag of the target differs from a `determined` value of the
  table.
- **In the rule.** Label 1 needs p_H ≤ 0.05 (9.2).

### 7.3 Reported beside the rule

- each predicate at the target, with its margin, and the target's
  membership of each pool;
- p_P for each of the four pools, with each pool's n and lattice;
- the disclosure table, with Q_record and Q_contra;
- H1, H2 and H5 at the target, with their base rates over the pools. These
  are never counted;
- **the homogeneity of P_BM** (R20): the H3 and H4 pass rates of its MWRA
  class and of its GWE-or-station class, with Fisher's exact p;
- **the stationarity table** (R21) [r1v5 N11]:
  - the H3 and H4 rates of P_BM and P_MWRA in the early (−1999..−900) and
    late (−899..+200) halves, with Fisher's p;
  - the same within ±700 years of the target against the rest;
- **H3 given D4** [r1v5 N2]: H3's pass rate among the members of P_MWRA whose
  morning greatest elongation falls 26–30 days before their Day 0, as the
  target's does (D4). It is computed at the null-side stage with the target
  masked. It estimates how far the record had already settled H3, without
  evaluating H3 at the target;
- **the floors with H4 dropped**: 0.208 over the whole background and 0.241
  within ±700 years at the design stage (2.9). This is the recheck's course
  (a), which shows that H3 alone could not say "yes" for any target;
- **sensitivity pools.** The test is rerun on T_A(v) for every variant of
  4.2, over the whole background, in daylight. These pools are matched only
  on the categorical slots, so they are not the rule's pools. At the design
  stage their p_H,min values are 0.009–0.012 (2.9);
- the pass rates of H1–H5 among R_anc's survivors, the ancient autumn reading
  [rev #11 fix 3]. R_anc has no planets, so no rank test is run on it;
- **the *Almagest* calibration of the test.** The same rank test is applied
  to the true dates of real records, with their non-B&M rows held out (6.4;
  Q_H).

Power is low: two predicates, and pools of 28 to 76. The lattice shows that
a target can reach p ≤ 0.05 only by passing both predicates, and Q_record
shows that this target cannot. The report says so.

