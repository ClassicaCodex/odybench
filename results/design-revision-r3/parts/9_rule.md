## 9. The decision rule

### 9.1 Named quantities

One script computes each quantity the rule reads, and writes it to one JSON
key stamped with the frozen code tree hash (section 12). The **stage** column
says when the quantity may first be computed (12.3):

- **null:** at the null-side stage, with the target masked;
- **target:** after the second freeze;
- **controls:** after the second freeze; the target is not involved.

| quantity | definition | stage | section | written by |
|---|---|---|---|---|
| INSTR | the instrument checks that guard rule inputs all pass: I1, I2, I2b, I4–I9, I11, I13–I15 | each check at its own stage | 6.1 | `results/instrument/summary.json` |
| T0_pass | 16 Apr 1178 BC passes N, C, V and M (E off) in the primary cell | target | 3.5 | `reproduce.py` |
| T0 (reported) | R, RE or NR in the primary cell | target | 3.5 | `reproduce.py` |
| p_H,min; n_H, x_max | the floor of the held-out test: (1 + x_max)/(1 + n_H) on P_BM | null | 7.2 | `attain.py` |
| p_H | the held-out exact rank p-value of 1178 BC on P_BM | target | 7.2 | `heldout.py` |
| G_BM(v), G_BM,lo(v), G_BM,hi(v); n_A(v), k_A(v), for v ∈ {v0, …, v5} | G(𝒢_BM*; T_A(v); W = 136) with the interval of 5.3 | null | 4.2, 5.3 | `attain.py` |
| G_BM,u; n_T | G(𝒢_BM*; T; W = 136); equal to (n_A(v)/n_T) G_BM(v) for v1–v5 | null | 5.3 | `attain.py` |
| r_Ody | reach_136(16 Apr −1177; 𝒢_BM*) | target | 5.3 | `garden.py` |
| pct_N4, pct_N4,lo, pct_N4,hi; x_gt, x_eq, n_stratum | the mid-p percentile of r_Ody among entering stratum epics, with bounds from the strict and weak counts; undefined when r_Ody = 0 | target | 5.4 | `randomepic.py` |
| seen_PCR, strict_PCR | of the 7 counted PC-R sets: seen; strict recall (ΔT mixture) | controls | 6.3.2–6.3.3 | `controls.py` |
| seen_PCR,redraft; seen_PCR,sibling | seen_PCR with the five re-drafted primaries; with every audited row at its failing sourced sibling convention | controls | 6.3.4 | `controls.py` |
| seen_PCR,noncirc | seen_PCR with the circular sets' ΔT σ tripled | controls | 6.3.3 | `controls.py` |
| seen_ALM_SL, rec_ALM_BM | of the 11 counted *Almagest* sets: seen in regime SL (ceiling tolerances, leave-one-set-out); strict recall with narrowing in regime BM | controls | 6.4 | `almagest.py` |
| held_ALM | of the 11 counted *Almagest* sets, the number whose true date has p ≤ 0.05 on the set's held-out rows | controls | 6.4 | `almagest.py` |
| hit_j, G_j, G_j,hi; n_j | for each of the 12 clean negatives | controls | 6.5 | `negatives.py` |

No likelihood ratio, Bayes factor, PC-S recall or G_DOC is a rule input.
They are reported (1.3, 5.3, 5.7, 6.2). The thresholds are in
`data/prereg/verdict_rule.json` and are frozen at the first freeze, before
any of these quantities is computed.

### 9.2 The rule

`odybench/verdict_rule.py` implements exactly this, as a pure function of the
quantities above:

```
if not INSTR:                                         return BLOCKED (no verdict is read)
labels, qualifiers = {}, {}

# gates and control qualifiers
if seen_PCR < 4:                                      labels += 3a
if seen_ALM_SL < 6:                                   labels += 3b
if rec_ALM_BM < 6:                                    qualifiers += Q_BM
if held_ALM < 6:                                      qualifiers += Q_H
if strict_PCR < 4:                                    qualifiers += Q_strict
side = (seen_PCR < 4)
if (seen_PCR_redraft < 4) != side or (seen_PCR_sibling < 4) != side:
                                                      qualifiers += Q_exposure
if (seen_PCR_noncirc < 4) != side:                    qualifiers += Q_dT

# null-side qualifiers (known at the second freeze)
if p_H_min > 0.05:                                    qualifiers += Q_attain
g2  = {v: G_BM_lo[v] >= 0.20 for v in SLOTS}           # SLOTS = v0..v5
tol = {v: G_BM_lo[v] >  0.05 for v in SLOTS}
if all(tol.values()):                                 qualifiers += Q_tol
if len(set(g2.values())) > 1 or len(set(tol.values())) > 1:
                                                      qualifiers += Q_slot

# 4: the method dates fiction
if any(hit_j and G_j_hi <= G_BM_u for j in clean_negatives):
                                                      labels += 4

# 2: B&M's match carries no weight
if r_Ody == 0:                                        labels += "2 (no match)"
elif all(g2.values()) or pct_N4_lo >= 0.50:           labels += "2 (ordinary)"

# 1: the text dates the return, by the clues nobody fitted
if T0_pass and p_H <= 0.05 and not ({3a, 3b, 4} & labels):
                                                      labels += 1

if labels is empty:                                   labels = {inconclusive}
return labels, qualifiers
```

U0(n) = 3.69/n is the gamma upper bound of a G with no target reached.
CP_hi(x, n) is the Clopper–Pearson 97.5% bound.

### 9.3 How to read it

- **Every rule names its garden, its pool and its stage** [rev #1 fix 1]:
  - 𝒢_BM* over T_A(v) prices B&M's tolerances (label 2's G leg, Q_tol).
  - 𝒢_BM* over T enters only the comparison with fiction, whose readings
    are blind (label 4).
  - P_BM, the candidates that 𝒢_BM* accepts, is the null pool of the
    held-out test (label 1).
  - The verdict recomputed with 𝒢_DOC* and 𝒢_FULL* in place of 𝒢_BM*, with
    the E-on gardens, and with revision 2's pool T_C, is printed beneath it
    as a sensitivity. It never replaces the verdict.
- **Why "yes" rests on the held-out test** [r2 R2-1]. Each of revision 3's
  three "yes" conditions was fixed by the sky before the Odyssey was
  measured:
  - G_BM is about 0.14 by the sky alone;
  - T0 = R needs 18 Mar 1189 BC to fail, and it passes;
  - pct_N4 ≤ 0.05 is a reach percentile of the same kind as G.

  A test whose most extreme possible observation cannot reach 5% has no
  power, and its "no" means nothing. The held-out test's floor p_H,min is
  computed before the target is looked at. Q_attain prints it with every
  verdict.
- **Why T0_pass and not T0 = R.** The uniqueness of 1178 BC in B&M's window
  is a property of the other candidates. Its weight is what G measures, and
  G shows it carries little (Q_tol).
- **G has one sense throughout**: a look-elsewhere-corrected p-value, small
  when the coincidence is notable.
  - Label 2 needs it large.
  - Q_tol says it cannot be small.
  - Outcome 4 asks whether fiction's is as small as the Odyssey's.
- **Bounds work against the claim being made** [r1 N8 fix 2]:
  - label 2's G leg and Q_tol use G_BM,lo under every slot variant, so the
    variant most favourable to B&M decides;
  - label 2's pct leg uses the lower bound from the strict count, so ties
    favour the Odyssey [r2 R2-3];
  - outcome 4 uses the negative's upper bound;
  - label 1's p_H is exact, and ties count against the target.
- **Why 0.05 and 0.20 over T_A.** These thresholds were frozen in revision 3
  (2026-10-04), before the recheck estimated G_BM (later the same day), and
  revision 4 keeps them unchanged [r2 R2-1 fix 1].
  - Revision 2's thresholds, 0.01 and 0.05, were set for G over T_C. For
    𝒢_BM*, G over T_C is (n_A/n_TC) × G over T_A, about 0.147 × G over T_A
    [r2], because targets outside A are never reached (4.2).
  - Revision 2's 0.01 therefore corresponds to about 0.07 over T_A, and its
    0.05 to about 0.34.
- **Label combinations.** Labels 2, 3a, 3b and 4 can hold together, and 1
  can hold with 2. The headline leads with 3a or 3b when either holds,
  because they say which "no"s mean nothing. It then gives 1, 2 and 4, in
  that order.
- **When 1 and 2 hold together**, the headline reads: the clues nobody
  fitted date the return, and B&M's own match is not what shows it.

### 9.4 Structural constraints: what an input set must satisfy to be realisable

A synthetic input set proves an outcome reachable only if real data could
produce it. Revision 3's set S1 used G_BM = 0.0065 with three targets
reached. T0b's single reading already reaches four, and the whole garden
about 26, so S1 could not occur, and nothing in revision 3's constraints
caught it [r2 R2-1].

**Two kinds of input are therefore kept apart:**

- **Null-side fields** are fixed by the sky and the readings. A set that
  claims reachability must use the measured values. Until the null-side
  stage those are the design-stage estimates of 2.9.
- **Target-side and control fields** are free, subject to their lattices and
  intervals.

I14(b) checks every set against C1–C9. I14(c) reruns the sets at the
null-side stage with the measured values.

| # | constraint | why |
|---|---|---|
| C1 | 0 ≤ G_lo ≤ G ≤ G_hi ≤ 1 for every G, and G_hi ≥ U0(n) = 3.69/n with n its pool size | the interval of 5.3 |
| C2 | G_BM,u = (n_A(v)/n_T) · G_BM(v) for v1–v5, the same number for each | no target outside T_A(v) is reached by 𝒢_BM* (4.2) |
| C3 | if r_Ody = 0, pct_N4 is undefined; otherwise pct_N4,lo ≤ pct_N4 ≤ pct_N4,hi, each computed from integer counts x_gt, x_eq and n_stratum ≥ 200 as in 5.4 | 5.4 |
| C4 | if hit_j, then G_j > 0 and G_j,hi ≥ U0(n_j) | a unique survivor in the core has reach > 0 |
| C5 | the counts are integers: 0 ≤ seen_PCR, strict_PCR and the other PC-R counts ≤ 7; 0 ≤ seen_ALM_SL, rec_ALM_BM, held_ALM ≤ 11 | definitions |
| C6 (attainability) | outcome 1 is attainable only if p_H,min ≤ 0.05. Outcome 4 is attainable only if G_BM,u ≥ U0(n_j) | 7.2, C4 |
| C7 (the null side is fixed) [r2 R2-1 fix 2] | the null-side fields (n_T, n_A(v), G_BM(v) with bounds, G_BM,u, n_H, x_max, p_H,min) equal the design-stage estimates of 2.9, or after the null-side stage the measured values. A set that departs from them is marked **branch test**. It shows that a code branch works, and proves no outcome reachable | R2-1 |
| C8 | p_H = (1 + x)/(1 + n_H) for an integer x with x_max ≤ x ≤ n_H, so p_H ≥ p_H,min. With the design-stage counts, the attainable values are 0.026 (both), 0.039 (H4 only), 0.221 (H3 only) and 1 (neither) | 7.2 |
| C9 | T0 ∈ {R, RE} implies T0_pass | 3.5 |

**Known facts, not constraints.** Some target-side and control facts are
already known or inferred:

- T0_pass is true and T0 is RE;
- H4 is inferred to fail, so p_H ≥ 0.22 (2.10);
- rec_ALM_BM ≤ 5;
- seen_ALM_SL ≤ 9;
- strict_PCR = 4 (rough).

A realisable set may contradict these, because the rule must also be shown to
work for data that differ from the Odyssey's. Each set that does is marked
in 9.5. What a realisable set may not contradict is the null side.

### 9.5 Synthetic input sets that prove every outcome reachable

`data/prereg/verdict_synthetic/*.json` holds these inputs.
`tests/test_verdict.py` asserts the stated output for each (I14a) and checks
it against 9.4 (I14b) [me: `results/design-revision-r3/synth_sets.py`,
`.out.txt`].

**The base set, S0.** Every other set starts from it and lists only what
differs.

- **The rule:** INSTR true; T0_pass true, T0 RE.
- **The null side, at the design-stage estimates of 2.9:**
  - G_BM by variant: v0 0.224 [0.139, 0.344]; v1 0.140 [0.087, 0.215]; v2
    0.211 [0.131, 0.324]; v3 0.278 [0.172, 0.427]; v4 0.182 [0.112, 0.279];
    v5 0.327 [0.203, 0.504];
  - n_T 10,690; G_BM,u 0.00172;
  - n_H 76, x_max 1, p_H,min 0.026.
- **The target side:**
  - p_H 0.221 (H3 only);
  - r_Ody 0.0815;
  - pct_N4: x_gt 30, x_eq 10 of n_stratum 200, giving 0.175 [0.104, 0.262].
- **The controls:**
  - seen_PCR 5, strict_PCR 4, redraft 5, sibling 5, noncirc 5;
  - seen_ALM_SL 7, rec_ALM_BM 3, held_ALM 8;
  - every negative: hit false, G_j 0.0006, hi 0.0012, n_j 10,690.

| set | differs from S0 | labels | qualifiers | null side (C7) | contradicts a known fact? |
|---|---|---|---|---|---|
| **S0** | — | **{inconclusive}** | Q_BM, Q_tol, Q_slot | realisable | none |
| **S1** | p_H 0.026 (passes H3 and H4) | **{1}** | Q_BM, Q_tol, Q_slot | realisable | H4 inferred to fail |
| S1b | p_H 0.039 (H4 only) | {1} | Q_BM, Q_tol, Q_slot | realisable | H4 inferred to fail |
| **S2** | pct_N4: x_gt 118, x_eq 12, giving 0.620 [0.518, 0.716] | **{2 (ordinary)}** | Q_BM, Q_tol, Q_slot | realisable | none |
| **S2nm** | r_Ody 0; pct_N4 undefined | **{2 (no match)}** | Q_BM, Q_tol, Q_slot | realisable | none (the branch R15 allows) |
| **S3a** | seen_PCR 2, redraft 2, sibling 2, noncirc 2 | **{3a}** | Q_BM, Q_tol, Q_slot | realisable | none |
| **S3b** | seen_ALM_SL 3 | **{3b}** | Q_BM, Q_tol, Q_slot | realisable | none |
| **S4** | AEN-TROY: hit true, G_j 0.00051, hi 0.00112 | **{4}** | Q_BM, Q_tol, Q_slot | realisable | none |
| S5 | as S1, but x_max 4, so p_H,min = p_H = 0.0649 | {inconclusive} | Q_BM, Q_tol, Q_slot, **Q_attain** | **branch test** | — |
| S6 | as S1, with S2's pct_N4 | {1, 2 (ordinary)} | Q_BM, Q_tol, Q_slot | realisable | H4 inferred to fail |
| S6b | as S2, but seen_ALM_SL 3, held_ALM 4, strict_PCR 2, redraft 3, noncirc 3; AEN-TROY as S4 | {2 (ordinary), 3b, 4} | Q_BM, Q_H, Q_strict, Q_exposure, Q_ΔT, Q_tol, Q_slot | realisable | none |
| S7 | INSTR false | BLOCKED | — | realisable | — |
| S8 | as S1, but T0_pass false (T0 NR) | {inconclusive} | Q_BM, Q_tol, Q_slot | realisable | T0_pass expected true |
| S9 | as S1, but seen_PCR 3, redraft 3, sibling 3, noncirc 3 | {3a} | Q_BM, Q_tol, Q_slot | realisable | H4 inferred to fail |
| S10 | every variant at v5's values: G_BM 0.327 [0.203, 0.504], n_A 56 | {2 (ordinary)} | Q_BM, Q_tol (no Q_slot) | **branch test** | — |
| S11 | as S1, but rec_ALM_BM 7 and held_ALM 4 | {1} | Q_H, Q_tol, Q_slot | realisable | rec_ALM_BM ≥ 6 |

**What each set shows:**

- **The four outcomes and the inconclusive verdict.** S1 reaches 1, S2 and
  S2nm reach 2 in both forms, S3a and S3b reach 3 in both parts, S4 reaches
  4, and S0 is inconclusive.
- **All of these are realisable.** Their null side is the design-stage
  estimate. The only known fact S1 contradicts is the inferred failure of
  H4, which is target-side.
- **What blocks label 1:** a gate (S9), or T0_pass false (S8).
- **What does not block it:** Q_BM and Q_H. S11 shows label 1 with Q_H and
  without Q_BM. Q_H conditions the held-out "no"s; a "yes" from the exact
  test is valid without it (7.2).
- **Co-occurrence.** S6 shows labels 1 and 2 together. S6b shows labels and
  every control qualifier together.
- **Branch tests.** S5 shows the Q_attain branch and S10 the label-2 G leg.
  Both need null-side values that contradict 2.9, so they are not proofs of
  reachability.
- **S7** shows the instrument block.

**At the null-side stage** (12.3), I14(c) replaces the null-side fields by
the measured values and reruns S0–S11. If S1 then no longer returns {1},
outcome 1 is unattainable, and Q_attain says so in every verdict. That is
recorded at the second freeze, before any target-side number exists.

---

