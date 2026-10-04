### 9.5 Synthetic input sets that prove every outcome reachable

`data/prereg/verdict_synthetic/*.json` holds these inputs.
`tests/test_verdict.py` asserts the stated output for each (I14a) and checks
it against 9.4 (I14b). `results/design-revision-v5/verdict_trace.py` is an
executable transcription of 9.2 and of C1–C9 for revision 5. It computes
each pool's p from the target's pass pattern and the pool's counts, with the
weights of 7.2 taken over pool and target, and it reproduces every label,
qualifier and realisability mark of the table below [me: the script and its
`.out.txt`]. Revision 4's sets are kept under their names, and S12 and S13
are new.

**The four outcomes, one set each** (with S0, inconclusive): **S1** reaches
outcome 1, **S2** outcome 2 (and S2nm its "no match" form), **S3a** and
**S3b** the two parts of outcome 3, and **S4** outcome 4. All five are
realisable: their null side is the design-stage estimate of 2.9.

**The base set, S0.** Every other set starts from it and lists only what
differs.

- **The rule:** INSTR true; T0_pass true, T0 RE.
- **The null side, at the design-stage estimates of 2.9:**
  - G_BM by variant: v0 0.224 [0.139, 0.344]; v1 0.140 [0.087, 0.215]; v2
    0.211 [0.131, 0.324]; v3 0.278 [0.172, 0.427]; v4 0.182 [0.112, 0.279];
    v5 0.327 [0.203, 0.504];
  - n_T 10,690; G_BM,u 0.00172;
  - P_BM: n 76; 14 members pass H3 only, 1 H4 only, 1 both. P_MWRA: n 43;
    8 pass H3 only, 1 H4 only, none both. p_H,min = max(0.0260, 0.0227) =
    0.026.
- **The target side:**
  - the target is a member of both pools and passes H3 only: p_BM 0.221,
    p_MWRA 0.227, so p_H = 0.227;
  - r_Ody 0.0815;
  - pct_N4: x_gt 30, x_eq 10 of n_stratum 200, giving 0.175 [0.104, 0.262].
- **The controls:**
  - seen_PCR 5, strict_PCR 4, redraft 5, sibling 5, noncirc 5;
  - seen_ALM_SL 7, rec_ALM_BM 3, held_ALM 8;
  - every negative: hit false, G_j 0.0006, hi 0.0012, n_j 10,690.

| set | differs from S0 | labels | qualifiers | null side (C7) | contradicts a known fact? |
|---|---|---|---|---|---|
| **S0** | — | **{inconclusive}** | Q_BM, Q_tol, Q_slot | realisable | none |
| **S1** | the target passes H3 and H4: p_BM 0.026, p_MWRA 0.023, so p_H 0.026 | **{1}** | Q_BM, Q_tol, Q_slot | realisable | H4 inferred to fail |
| S1b | H4 only: p_BM 0.039, p_MWRA 0.045, so p_H 0.045 | {1} | Q_BM, Q_tol, Q_slot | realisable | H4 inferred to fail |
| **S2** | pct_N4: x_gt 118, x_eq 12, giving 0.620 [0.518, 0.716] | **{2 (ordinary)}** | Q_BM, Q_tol, Q_slot | realisable | none |
| **S2nm** | r_Ody 0; pct_N4 undefined | **{2 (no match)}** | Q_BM, Q_tol, Q_slot | realisable | none (the branch R15 allows) |
| **S3a** | seen_PCR 2, redraft 2, sibling 2, noncirc 2 | **{3a}** | Q_BM, Q_tol, Q_slot | realisable | none |
| **S3b** | seen_ALM_SL 3 | **{3b}** | Q_BM, Q_tol, Q_slot | realisable | none |
| **S4** | AEN-TROY: hit true, G_j 0.00051, hi 0.00112 | **{4}** | Q_BM, Q_tol, Q_slot | realisable | none |
| S5 | as S1, but 4 members of P_BM pass both, so p_H,min = p_H = 0.0649 | {inconclusive} | Q_BM, Q_tol, Q_slot, **Q_attain** | **branch test** | — |
| S6 | as S1, with S2's pct_N4 | {1, 2 (ordinary)} | Q_BM, Q_tol, Q_slot | realisable | H4 inferred to fail |
| S6b | as S2, but seen_ALM_SL 3, held_ALM 4, strict_PCR 2, redraft 3, noncirc 3; AEN-TROY as S4 | {2 (ordinary), 3b, 4} | Q_BM, Q_H, Q_strict, Q_exposure, Q_ΔT, Q_tol, Q_slot | realisable | none |
| S7 | INSTR false | BLOCKED | — | realisable | — |
| S8 | as S1, but T0_pass false (T0 NR) | {inconclusive} | Q_BM, Q_tol, Q_slot | realisable | T0_pass expected true |
| S9 | as S1, but seen_PCR 3, redraft 3, sibling 3, noncirc 3 | {3a} | Q_BM, Q_tol, Q_slot | realisable | H4 inferred to fail |
| S10 | every variant at v5's values: G_BM 0.327 [0.203, 0.504], n_A 56 | {2 (ordinary)} | Q_BM, Q_tol (no Q_slot) | **branch test** | — |
| S11 | as S1, but rec_ALM_BM 7 and held_ALM 4 | {1} | Q_H, Q_tol, Q_slot | realisable | rec_ALM_BM ≥ 6 |
| S12 | as S1, but the target is not a member of P_MWRA, so p_MWRA = 1 and p_H = 1 | {inconclusive} | Q_BM, Q_tol, Q_slot | realisable | the target passes MWRA readings (2.9) |
| S13 | as S1b, but 2 members of P_MWRA pass H4 only: p_BM 0.039, p_MWRA 0.068, so p_H 0.068 | {inconclusive} | Q_BM, Q_tol, Q_slot | **branch test** | — |

**What each set shows:**

- **The four outcomes and the inconclusive verdict.** S1 reaches 1, S2 and
  S2nm reach 2 in both forms, S3a and S3b reach 3 in both parts, S4 reaches
  4, and S0 is inconclusive.
- **All of these are realisable.** Their null side is the design-stage
  estimate. The only known fact S1 contradicts is the inferred failure of
  H4, which is target-side.
- **Two ways to a "yes".** S1 passes both held-out predicates; S1b passes H4
  alone, and on the design-stage counts both pools still put it below 0.05.
- **What blocks label 1:** a gate (S9); T0_pass false (S8); a target outside
  one of the pools (S12); or one pool's p above 0.05 while the other's is
  below it (S13, a branch test, because on the design-stage counts the two
  pools agree in every cell).
- **What does not block it:** Q_BM and Q_H. S11 shows label 1 with Q_H and
  without Q_BM. Q_H conditions the held-out "no"s; a "yes" from the exact
  test is valid without it (7.2).
- **Co-occurrence.** S6 shows labels 1 and 2 together. S6b shows labels and
  every control qualifier together.
- **Branch tests.** S5 shows the Q_attain branch, S10 the label-2 G leg and
  S13 the max over the pools. Each needs null-side values that contradict
  2.9, so none proves an outcome reachable.
- **S7** shows the instrument block.

**At the null-side stage** (12.3), I14(c) replaces the null-side fields by
the measured values and reruns S0–S13. Each set keeps the target's pass
pattern (both, H4 only, H3 only, neither), and each pool's p is recomputed
with the measured counts. If S1 then no longer returns {1}, outcome 1 is
unattainable, and Q_attain says so in every verdict. If S1b no longer
returns {1}, a target passing H4 alone could not be dated, and the record
says so. Both are recorded at the second freeze, before any target-side
number exists.

