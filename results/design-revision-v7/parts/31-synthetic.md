`data/prereg/verdict_synthetic/*.json` holds these inputs.
`tests/test_verdict.py` asserts the stated output for each (I14a) and checks
it against 9.4 (I14b). `results/design-revision-v7/verdict_trace.py` is an
executable transcription of 9.2 and of C1–C12 for revision 7. It computes
each pool's p from the target's pass pattern and the pool's counts, with the
weights of 7.2 taken over pool and target. It reproduces every label,
qualifier and realisability mark of the table below [me: the script and its
`.out.txt`]. Revision 6's sets keep their names. S0y, S4b, S14b and S16–S19
are new, and S0x is restated [r2v6 N1].

**The outcomes, one set each:**

- **S1** reaches outcome 1;
- **S2** reaches outcome 2, and **S2nm** its "no match" form;
- **S3a** and **S3b** reach the two parts of outcome 3;
- **S4** reaches outcome 4;
- **S0** is inconclusive.

**The verdicts expected on known facts:** **S0x** if gate 3b passes (P21)
and **S0y** if it does not.

S1, S2, S2nm, S3a, S3b, S0, S0x and S0y are realisable: their null side is
the design-stage estimate of 2.6 and 2.9. **S4 is pending** until G_j and E_j
are measured at the null-side stage [r1v5 N5; r2v6 #71]: outcome 4 is not
ruled out, and not yet shown attainable.

**The base set, S0.** Every other set starts from it and lists only what
differs.

- **The rule:** INSTR true; T0_pass true, T0 RE.
- **The null side, at the design-stage estimates of 2.6 and 2.9:**
  - G_BM by variant: v0 0.224 [0.139, 0.344]; v1 0.140 [0.087, 0.215]; v2
    0.211 [0.131, 0.324]; v3 0.278 [0.172, 0.427]; v4 0.182 [0.112, 0.279];
    v5 0.327 [0.203, 0.504];
  - n_T 10,690; G_BM,u 0.00172 [0.00107, 0.00263];
  - the held-out pools, as (n; members passing H3 only, H4 only, both):
    - P_BM (76; 14, 1, 1);
    - P_MWRA (43; 8, 1, 0);
    - P_BM,E (49; 9, 1, 1);
    - P_MWRA,E (28; 6, 1, 0);
  - p_H,min = max(0.026, 0.023, 0.040, 0.034) = 0.040;
  - the disclosure table: H4 = fail, so Q_record holds;
  - Q_exch false;
  - N_narrow 5 on every leg of gate 3a, and 8 on every leg of gate 3b.
- **The target side:**
  - the target is a member of all four pools and passes H3 only: p 0.221,
    0.227, 0.240 and 0.276, so p_H = 0.276;
  - r_Ody 0.0815;
  - pct_N4: x_gt 30, x_eq 10 of n_stratum 200, giving 0.175 [0.104, 0.262].
- **The controls:**
  - gate 3a: every leg 5, in every variant;
  - gate 3b: every leg 7, under both meanings of `same_apparition`;
    rec_ALM_BM 3; held_ALM 7 at every step.
- **The negatives** (pending, C7): every hit false; G_j 0.0004 with
  G_j,hi 0.0009, n_j 10,690 and E_j 2. These are placeholders.

| set | differs from S0 | labels | qualifiers | null side (C7) | contradicts a known fact? |
|---|---|---|---|---|---|
| **S0** | — | **{inconclusive}** | Q_BM, Q_tol, Q_slot, Q_record | realisable | gate 3a's all-must-pass legs, expected at most 3 |
| **S0x** | gate 3a legs AL_bf 4, AL_st 2, WO_bf 3, WO_st 3, in every variant; gate 3b 6 on every leg, and 5 under the other meaning | **{3a}** | Q_BM, Q_tol, Q_slot, Q_record, Q_score | realisable | none: the verdict expected on known facts if P21 holds (2.10) |
| **S0y** | as S0x, but gate 3b 5 on every leg under both meanings | **{3a, 3b}** | Q_BM, Q_tol, Q_slot, Q_record, Q_score | realisable | none: the verdict expected if P21 fails (2.10) |
| **S1** | the target passes H3 and H4: p 0.026, 0.023, 0.040, 0.034, so p_H 0.040 | **{1}** | Q_BM, Q_tol, Q_slot, Q_record, **Q_contra** | realisable | H4, settled to fail (D1–D2); gate 3a's legs |
| S1b | H4 only: p 0.039, 0.045, 0.060, 0.069, so p_H 0.069 | {inconclusive} | Q_BM, Q_tol, Q_slot, Q_record, Q_contra | realisable | H4; gate 3a's legs |
| **S2** | pct_N4: x_gt 118, x_eq 12, giving 0.620 [0.518, 0.716] | **{2 (ordinary)}** | Q_BM, Q_tol, Q_slot, Q_record | realisable | gate 3a's legs |
| **S2nm** | r_Ody 0; pct_N4 undefined | **{2 (no match)}** | Q_BM, Q_tol, Q_slot, Q_record | realisable | gate 3a's legs (r_Ody 0 is the branch R15 allows) |
| **S3a** | gate 3a: every leg 2, in every variant | **{3a}** | Q_BM, Q_tol, Q_slot, Q_record | realisable | none |
| **S3b** | gate 3b: every leg 3, under both meanings | **{3b}** | Q_BM, Q_tol, Q_slot, Q_record | realisable | gate 3a's legs |
| **S4** | AEN-TROY: hit true, G_j 0.0004, hi 0.0009, E_j 2 | **{4}** | Q_BM, Q_tol, Q_slot, Q_record | **pending** (G_j, E_j) | gate 3a's legs |
| S4b | AEN-TROY: hit true, G_j 0.0005, hi 0.0012, which lies between the Odyssey's lower bound (0.00107) and its point value (0.00172) | {inconclusive} | Q_BM, Q_tol, Q_slot, Q_record | pending (G_j, E_j) | gate 3a's legs |
| S5 | as S1, but 4 members of P_BM pass both, so p_H,min = p_H = 0.0649 | {inconclusive} | Q_BM, Q_tol, Q_slot, Q_record, Q_contra, **Q_attain** | **branch test** | — |
| S6 | as S1, with S2's pct_N4 | {1, 2 (ordinary)} | Q_BM, Q_tol, Q_slot, Q_record, Q_contra | realisable | H4; gate 3a's legs |
| S6b | as S2, but gate 3a legs 4, 2, 3, 2 (re-draft 4, 4, 4, 4; non-circular 5, 4, 4, 4), gate 3b 3 on every leg under both meanings, held_ALM 4 at every step; AEN-TROY as S4 | {2 (ordinary), 3a, 3b, 4} | Q_BM, Q_H, Q_ΔT, Q_exposure, Q_record, Q_score, Q_tol, Q_slot | pending (G_j, E_j) | — |
| S7 | INSTR false | BLOCKED | — | realisable | — |
| S8 | as S1, but T0_pass false (T0 NR) | {inconclusive} | Q_BM, Q_tol, Q_slot, Q_record, Q_contra | realisable | T0_pass expected true; H4 |
| S9 | as S1, but gate 3a: every leg 3 | **{1, 3a}** | Q_BM, Q_tol, Q_slot, Q_record, Q_contra | realisable | H4 |
| S10 | every variant at v5's values: G_BM 0.327 [0.203, 0.504], n_A 56 | {2 (ordinary)} | Q_BM, Q_tol, Q_record (no Q_slot) | **branch test** | — |
| S11 | as S1, but rec_ALM_BM 7 and held_ALM 4 at every step | {1} | Q_H, Q_tol, Q_slot, Q_record, Q_contra | realisable | rec_ALM_BM ≥ 6; H4 |
| S12 | as S1, but the target is not a member of P_MWRA or P_MWRA,E, so their p is 1 and p_H 1 | {inconclusive} | Q_BM, Q_tol, Q_slot, Q_record, Q_contra | realisable | the target passes MWRA readings (2.9) |
| S13 | as S1, but 2 members of P_MWRA,E pass both: p_MWRA,E 0.103, which is also p_H,min | {inconclusive} | Q_BM, Q_tol, Q_slot, Q_record, Q_contra, **Q_attain** | **branch test** | — |
| S14 | every negative: G_j 0.0030, hi 0.0045, E_j 2 | {inconclusive} | Q_BM, Q_tol, Q_slot, Q_record, **Q_attain4** | pending (G_j, E_j) | — |
| S14b | every negative: G_j 0.0004, hi 0.0009, but E_j 0 | {inconclusive} | Q_BM, Q_tol, Q_slot, Q_record, **Q_attain4** | pending (G_j, E_j) | — |
| S15 | as S1, with gate 3b 3 on every leg under both meanings, and AEN-TROY as S4 | **{1, 3b, 4}** | Q_BM, Q_tol, Q_slot, Q_record, Q_contra | pending (G_j, E_j) | H4 |
| S16 | gate 3a: every leg 2, and only 3 counted PC-R sets can be narrowed on every leg | {3a} | Q_BM, Q_tol, Q_slot, Q_record, **Q_attain3a** | **branch test** | — |
| S17 | gate 3b: every leg 4 under both meanings, and only 5 counted *Almagest* sets can be narrowed on every leg | {3b} | Q_BM, Q_tol, Q_slot, Q_record, **Q_attain3b** | **branch test** | — |
| S18 | as S1, but Q_exch holds | {1} | Q_BM, Q_tol, Q_slot, Q_record, Q_contra, **Q_exch** | **branch test** | H4 |
| S19 | held_ALM 5 at the fine step, 7 at the others | {inconclusive} | Q_BM, Q_tol, Q_slot, Q_record, **Q_H** | realisable | — |

**What each set shows:**

- **The four outcomes and the inconclusive verdict.** S1 reaches 1, S2 and
  S2nm reach 2 in both forms, S3a and S3b reach 3 in both parts, S4 reaches
  4, and S0 is inconclusive.
- **Which are proven reachable now.** S1, S2, S2nm, S3a, S3b and S0 are
  realisable on the design-stage null side. The only known fact S1
  contradicts is target-side: H4, which the record settles to fail. That is
  why Q_record holds in every set, and why S1 also prints Q_contra. S4's
  realisability waits for G_j and E_j.
- **The expected verdicts.** S0x reproduces the verdict expected if gate 3b
  passes: {3a}, with Q_score twice over, because gate 3a's best-fit leg sits
  at its threshold and gate 3b's pass rests on the meaning of
  `same_apparition`. S0y reproduces the verdict expected if it does not:
  {3a, 3b}.
- **One way to a "yes".** S1 passes both held-out predicates. S1b passes H4
  alone: on the four-pool lattice that gives 0.069, so it is not enough.
- **What blocks label 1:** T0_pass false (S8); a target outside some pools
  (S12); or a pool whose floor exceeds 0.05 (S13, a branch test, because on
  the design-stage counts every pool's floor is below 0.05).
- **What does not block it:** the gates and the control qualifiers. S9 shows
  label 1 with 3a, S15 with 3b and 4 (pending), S11 with Q_H and without
  Q_BM, and S18 with Q_exch, which qualifies label 1 but leaves it standing.
- **Outcome 4 against the Odyssey's lower bound** [r2v6 N8]. S4b's negative
  would have fired outcome 4 under revision 6's comparison with the point
  value, and does not now.
- **What Q_attain4 needs** [r2v6 #71]. S14 lacks the G condition, and S14b
  the eclipse condition: in S14b every negative's G condition holds, but no
  eclipse-compatible reading reaches an eclipse of the Odyssey's strength.
- **The gates' attainability** [r2v6 N1]. S16 and S17 show 3a and 3b printed
  as "untested by these controls". They are branch tests: the design-stage
  N_narrow (5 and 8) clears both thresholds.
- **The rounding family** [r2v6 N6]. S19 shows Q_H from the fine step alone.
- **Co-occurrence.** S6 shows labels 1 and 2 together. S6b shows labels and
  every control qualifier together.
- **Branch tests.** S5 shows the Q_attain branch, S10 the label-2 G leg, S13
  a single pool's veto, S16 and S17 the gates' attainability, and S18
  Q_exch. Each needs null-side values that contradict 2.6 or 2.9, so none
  proves an outcome reachable. S14 and S14b show Q_attain4, and are pending.
- **S7** shows the instrument block.

**At the null-side stage** (12.3), I14(c) replaces the null-side fields by
the measured values, G_j and E_j included, and reruns S0–S19.

- Each set keeps the target's pass pattern (both, H4 only, H3 only,
  neither), and each pool's p is recomputed with the measured counts.
- If S1 then no longer returns {1}, outcome 1 is unattainable, and Q_attain
  says so in every verdict.
- The measured G_j and E_j settle S4, S4b, S6b, S14, S14b and S15. If no clean
  negative meets both conditions of Q_attain4, outcome 4 is unattainable,
  and Q_attain4 says so.
- The measured N_narrow settles whether Q_attain3a or Q_attain3b holds, and
  Q_exch is read from the measured tests.
- Q_record is recomputed from the measured lattice.
- All of this is recorded at the second freeze, before any target-side
  number exists.

