### 7.2 The counted statistic: an exact rank test on two pools (a rule input)

- **Two null pools** (4.2). Both are drawn from P_all over the whole
  background, −1999..+200. No core is needed, because no window is placed.
  - **P_BM**: the candidates that pass at least one reading of 𝒢_BM*
    (revision 4's pool).
  - **P_MWRA** (revision 5): the candidates that pass at least one of the
    twelve MWRA readings of 𝒢_BM*, that is, C on a day count, a Venus lead
    of at least 90 min on that count's Venus day, and a morning
    rise-azimuth maximum within 3.5 d of that count's Mercury day. P_MWRA ⊂
    P_BM.
- **Why two** [rev #11 fix 1]. The test must compare the target with
  candidates that pass the same N, C, V and M.
  - H3 depends on Mercury's phase, which M fixes. H4 depends on Venus'
    elongation, which V fixes.
  - The target passes only B&M's applied Mercury event, the MWRA (2.9, "the
    target under 𝒢_BM*"). A candidate admitted through a greatest elongation
    or a station has Mercury in another phase at Day −34, and so possibly on
    Day 0. P_MWRA is matched to the reading the target passes; P_BM is
    larger and so has a finer lattice.
  - On the rough rows the two classes of P_BM do not differ in H3 or H4
    (2.9), but the bench does not lean on that.
- **Neither pool depends on the slot definitions of 4.2,** so outcome 1 is
  free of R2-2's slot question. **Day and night conjunctions both enter,**
  because neither predicate depends on daylight, and taking both doubles
  the pools.
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
    to 1.
- **p_H := max(p_BM, p_MWRA).**
  - **Why it is exact.** Under H0, that the text is unrelated to the sky of
    1178 BC, suppose either pool is exchangeable with the target. Then that
    pool's p satisfies P(p_P ≤ α) ≤ α for every α, and p_H ≥ p_P. So
    P(p_H ≤ α) ≤ α, with no approximation and no interval, **if either pool
    is exchangeable**. A referee who doubts one pool's matching cannot fault
    the test on that ground.
  - **The cost.** Label 1 now needs both pools to agree. On the design-stage
    lattice the two give the same verdict in every cell (below).
  - **Exchangeability and the eclipse.** The target was chosen for its
    eclipse. Neither predicate involves the lunar node, so eclipse status
    should not change their rates. P10 tests that on P_spring, and R20
    tests the homogeneity of P_BM across Mercury events.
- **Attainability, a null-side quantity** [r2 R2-1 fix 4].
  p_H,min = max over the two pools of (1 + x_max,P)/(1 + n_P), where x_max,P
  is the number of members of P that pass both predicates. A target passing
  both earns exactly p_H,min.
  - **When.** p_H,min is computed at the null-side stage, with the target
    masked (12.3), before any target-side number.
  - **Design-stage values** [2.9; me: heldout_attain.py and
    heldout_strata.py]: P_BM n 76, x_max 1, floor 0.026; P_MWRA n 43,
    x_max 0, floor 0.023. So **p_H,min = 0.026**.
  - **The lattice** (p_BM / p_MWRA → p_H): passes both, 0.026 / 0.023 →
    **0.026**; H4 only, 0.039 / 0.045 → **0.045**; H3 only, 0.221 / 0.227
    → **0.227**; neither, 1.
  - **Q_attain** holds if the measured p_H,min exceeds 0.05.
- **In the rule.** Label 1 needs p_H ≤ 0.05 (9.2).

### 7.3 Reported beside the rule

- each predicate at the target, with its margin, and the target's
  membership of each pool;
- p_BM and p_MWRA separately, with each pool's n and lattice;
- H1, H2 and H5 at the target, with their base rates over both pools. These
  are never counted;
- **the homogeneity of P_BM** (R20): the H3 and H4 pass rates of its MWRA
  class and of its GWE-or-station class, with Fisher's exact p;
- **sensitivity pools.** The test is rerun on T_A(v) for every variant of
  4.2, over the whole background, in daylight. These pools are matched only
  on the categorical slots, so they are not the rule's pools. At the design
  stage their p_H,min values are 0.009–0.012 (2.9);
- the pass rates of H1–H5 among R_anc's survivors, the ancient autumn reading
  [rev #11 fix 3]. R_anc has no planets, so no rank test is run on it;
- **the *Almagest* calibration of the test.** The same rank test is applied
  to the true dates of real records, with their non-B&M rows held out (6.4;
  Q_H).

Power is low: two predicates, and pools of about 76 and 43. The lattice
shows that a target can reach p ≤ 0.05 only by passing H4. The report says
so.

