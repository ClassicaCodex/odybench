## 7. Clues B&M did not use

These come from the 76-row inventory [txt §4], and none is used to fit
anything. In revision 4 this section carries the only evidence that can give
a "yes" (1.3). So it says:

- which clues are blind;
- how they are scored, and against which pool;
- how the chance of a "yes" is computed before the target is looked at.

### 7.1 The clues, and which are blind

A clue counts only if it meets two tests:

- its reading was formed without the target in view;
- nobody has evaluated it at the target before its predicate was frozen.

That is the uniform rule of 1.1 and 5.3, applied to the clues B&M cited as
support as well as to those they searched with.

| # | clue (lines; day) | predicate (frozen) | status |
|---|---|---|---|
| H1 | "this night is very long" (11.373; Day −7 seq); "these nights are endless" (15.392; Day −3) | night (Sun's centre below −0.833°) ≥ 12.0 h on that night | **not counted** [rev #11]. The threshold was set after the nights of 1178 BC (11.5 h and 11.3 h, a fail) had been computed [txt §5.6], and it measures the season that C already fixes. Reported |
| H2 | σκοτομήνιος, the dark night (14.457; night of Day −5 seq / −4 par) | Moon above the horizon for < 25% of the dark hours | **not counted** (new in revision 4). It fails both tests (below). Reported with its conditional base rate |
| H3 | Hermes leads the suitors' souls past the gates of the Sun (24.1–14; night of Day 0/+1) | **one predicate** [r1 N14]: Mercury is not visible (AV 10°) on the mornings and evenings of Day 0 and Day +1, **and** a geocentric conjunction of Mercury with the Sun in ecliptic longitude (inferior or superior) falls within ±3 d of noon (UT+2) on Day 0 or on Day +1 | **counted** |
| H4 | Ares and Aphrodite caught together (Demodocus, 8.266–366; Day −7 seq / −6 par [chron §5.1]) | the geocentric Venus–Mars separation at 03:30 UT is ≤ 5° on some day within ±3 d of Day −7 (sequential) or Day −6 (parallel). The count used is the one on which the candidate passes a reading of 𝒢_BM*, and either count will do if it passes on both | **counted** |
| H5 | Mars invisible in March–April 1178 BC except during the eclipse | Mars not visible (AV 11.5°) on any morning or evening from Day −34 to Day 0 | **not counted**: B&M found it after the date [bm §2]. Reported |
| H6 | the twentieth year (9 lines); a year with Circe and seven with Calypso | the year lies 8–11 years after one of the ancient sack dates (Duris 1334/3 to Ephorus 1135, as in [win §3]; Clement's list [unread §4]) | external check, reported per survivor; strict Eratosthenes alone excludes 1178 BC [win §6] |
| H7 | Theoclymenus at the δεῖπνον; supper "in the light" (20.390–394, 21.428–429) | eclipse maximum in daylight on Day 0 | consistency only, for eclipse-compatible readings; "noon" is not in the text [txt §5.10] |
| H9 | frost feared (5.467, 17.25); hearths and fires (6.305, 7.153, 18.307–311, 19.63–64) | — | weather, not sky. Reported qualitatively, with the five scholia that read autumn or winter [txt §5.6] |
| H10 | nightingale (19.519), swallows (21.411, 22.240), gadfly (22.301 = 18.367) | — | similes, so excluded [txt §5.4]. 18.366–370 is also a wish, read as winter, May or autumn by different advocates, and is used for nothing [unread §2.3] |
| H11 | much-flowering wood (14.353) | — | inside a lying tale, so excluded |
| H12 | Laertes digging round a plant (24.226–231; Day +1) | — | qualitative |
| H13 | Helios' complaint (12.374–390), Poseidon and Zeus (13.125–158) | — | no operational predicate is defensible; listed, not run |

**Why H2 is no longer counted.** It fails both tests:

- **B&M cite 14.457** in support of their new moon. Their text calls it
  "Night −2" [bm-a, clue N; B&M §Method, SI Table S1].
- **Its value at 1178 BC was known.** The dossier computed the Moon's
  circumstances for the night after Day −5 of 1178 BC (moonrise about
  03:48 LMT) [txt §5.2]. That was before revision 1 froze the 25% threshold.
- **It is weak anyway.** Given a Day 0 at conjunction it passes about half
  the time [vis §4.5].

**Why H3 and H4 are blind.**

- **Nobody fitted them.** B&M do not treat the second Hermes journey or the
  song of Ares [txt §4 row 70; B&M]. Gainsford lists such god-movements as
  what a consistent Hermes = Mercury rule must also accommodate [crit §3.3].
- **They were frozen early.** Revision 1 wrote both predicates on
  2026-10-03 as tests of that consistency [v1 §5].
- **Nobody has evaluated them at the target.** A search of `docs/` and
  `results/` finds no computation of Mercury on Day 0 or of the Venus–Mars
  separation for 1178 BC. This revision's estimate masked the target (2.9).
- **The inference to the contrary is not a computation.** One inference from
  documented numbers says H4 should fail (2.10). That inference is not a
  computation, and the predicate was not tuned to it.

**What H3 and H4 test.** They test B&M's own encoding hypothesis, that the
poet turned god-movements into planets. If the hypothesis is right, the
other god-movements of the same story should match the same sky. That is
the evidence a "yes" can rest on.

### 7.2 The counted statistic: an exact rank test (a rule input)

- **The null pool, P_BM** (4.2). These are the candidates of P_all over the
  whole background, −1999..+200, that pass at least one reading of 𝒢_BM*.
  No core is needed, because no window is placed.
  - **It is matched to the readings the target passes** [rev #11 fix 1]. H3
    depends on Mercury's phase, which M fixes. H4 depends on Venus'
    elongation, which V fixes.
  - **It does not depend on the slot definitions of 4.2.** So outcome 1 is
    free of R2-2's slot question.
  - **Day and night conjunctions both enter.** Neither predicate depends on
    whether the conjunction falls in daylight, and taking both doubles the
    pool.
- **The score.** s(t) = Σ_{i ∈ {3, 4}} pass_i(t) · (−log10 q_i).
  - q_i is the pass rate of H_i over P_BM ∪ {t_S}.
  - It is computed at the target-side stage, symmetrically in every member,
    so the test is exact.
  - A rarer predicate weighs more. The order of scores is then: passes both;
    passes the rarer predicate only; passes the commoner only; passes
    neither.
- **The p-value.** p_H = (1 + #{u ∈ P_BM : s(u) ≥ s(t_S)}) / (1 + n_H).
  - **Why it is exact.** Under H0, that the text is unrelated to the sky of
    1178 BC, t_S is exchangeable with the members of P_BM, so P(p_H ≤ α) ≤ α
    exactly, and no interval is needed. Ties count against the target.
  - **Exchangeability.** The target was chosen for its eclipse. Neither
    predicate involves the lunar node, so eclipse status should not change
    their rates. P11 tests that on P_spring.
- **Attainability, a null-side quantity** [r2 R2-1 fix 4].
  p_H,min = (1 + x_max)/(1 + n_H), where x_max is the number of P_BM members
  that pass both predicates. A target passing both earns exactly p_H,min.
  - **When.** p_H,min is computed at the null-side stage, with the target
    masked (12.3), before any target-side number.
  - **Design-stage values** [2.9; me: heldout_attain.py]: n_H = 76 and
    x_max = 1, so p_H,min = 0.026.
  - **The lattice:** passes both, 0.026; H4 only, 0.039; H3 only, about
    0.22; neither, 1.
  - **Q_attain** holds if the measured p_H,min exceeds 0.05.
- **In the rule.** Label 1 needs p_H ≤ 0.05 (9.2).

### 7.3 Reported beside the rule

- each predicate at the target, with its margin;
- H1, H2 and H5 at the target, with their base rates over P_BM. These are
  never counted;
- **sensitivity pools.** The test is rerun on T_A(v) for every variant of
  4.2, over the whole background, in daylight. These pools are matched only
  on the categorical slots, so they are not the rule's pool. At the design
  stage their p_H,min values are 0.009–0.012 (2.9);
- the pass rates of H1–H5 among R_anc's survivors, the ancient autumn reading
  [rev #11 fix 3]. R_anc has no planets, so no rank test is run on it;
- **the *Almagest* calibration of the test.** The same rank test is applied
  to the true dates of real records, with their non-B&M rows held out (6.4;
  Q_H).

Power is low: two predicates, and a pool of about 76. The lattice shows that
a target can reach p ≤ 0.05 only by passing H4. The report says so.

---

