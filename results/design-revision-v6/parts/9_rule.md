## 9. The decision rule

### 9.1 Named quantities

One script computes each quantity the rule reads, and writes it to one JSON
key stamped with the frozen code tree hash (section 12). The **stage** column
says when the quantity may first be computed (12.3):

- **null:** at the null-side stage, with the target masked;
- **target:** after the second freeze; it reads 16 Apr 1178 BC;
- **controls:** after the second freeze; it reads a control's truth and not
  the target.

| quantity | definition | stage | section | written by |
|---|---|---|---|---|
| INSTR | the instrument checks that guard rule inputs all pass: I1, I2, I2b, I4–I9, I11, I13–I16 | each check at its own stage | 6.1 | `results/instrument/summary.json` |
| T0_pass | 16 Apr 1178 BC passes N, C, V and M (E off) in the primary cell | target | 3.5 | `reproduce.py` |
| T0 (reported) | R, RE or NR in the primary cell | target | 3.5 | `reproduce.py` |
| p_H,min; for each pool P ∈ {P_BM, P_MWRA, P_BM,E, P_MWRA,E}: n_P, x_max,P and the counts of members passing H3 only, H4 only and both | the floor of the held-out test: the largest over the four pools of (1 + x_max,P)/(1 + n_P) | null | 7.2 | `attain.py` |
| Q_record | no pass pattern consistent with the `determined` values of the frozen disclosure table reaches p_H ≤ 0.05 on the measured lattice | null, with the frozen table | 7.1, 7.2 | `attain.py` |
| p_H; p_P for each pool; the target's membership of each pool | the held-out exact rank p-value of 1178 BC: the largest of the four p_P, a pool's p being 1 if the target fails every reading that defines it | target | 7.2 | `heldout.py` |
| Q_contra | a measured flag of the target differs from a `determined` value of the disclosure table | target | 7.1 | `heldout.py` |
| G_BM(v), G_BM,lo(v), G_BM,hi(v); n_A(v), k_A(v), for v ∈ {v0, …, v5} | G(𝒢_BM*; T_A(v); W = 136) with the interval of 5.3 | null | 4.2, 5.3 | `attain.py` |
| G_BM,u; n_T | G(𝒢_BM*; T; W = 136); equal to (n_A(v)/n_T) G_BM(v) for v1–v5 | null | 5.3 | `attain.py` |
| G_j, G_j,lo, G_j,hi; n_j | for each of the 12 clean negatives: G of the set's full garden over its targets, with the interval of 5.3 [r1v5 N5] | null | 6.5 | `attain.py` |
| r_Ody | reach_136(16 Apr −1177; 𝒢_BM*) | target | 5.3 | `garden.py` |
| pct_N4, pct_N4,lo, pct_N4,hi; x_gt, x_eq, n_stratum | the mid-p percentile of r_Ody among entering stratum epics, with bounds from the strict and weak counts; undefined when r_Ody = 0 | target | 5.4 | `randomepic.py` |
| seen_PCR[v][leg] | for each variant v ∈ {main, redraft, sibling, noncirc} and leg ∈ {AL_bf, AL_st, WO_bf, WO_st}: the number of the 7 counted PC-R sets seen. *redraft* uses the five re-drafted primaries; *sibling* sets every audited row to its failing sourced convention; *noncirc* triples the circular sets' ΔT σ | controls | 6.3.2–6.3.4 | `controls.py` |
| strict_PCR (reported) | the number of the 7 counted sets with strict recall under the as-licensed primaries, without narrowing | controls | 6.3.2 | `controls.py` |
| seen_ALM_SL[leg], for leg ∈ {bf, st}; rec_ALM_BM | of the 11 counted *Almagest* sets: seen in regime SL (ceiling tolerances, leave-one-set-out) by best fit and strictly; strict recall with narrowing in regime BM | controls | 6.4 | `almagest.py` |
| held_ALM | of the 11 counted *Almagest* sets, the number whose true date has p ≤ 0.05 on the set's held-out rows | controls | 6.4 | `almagest.py` |
| hit_j | for each of the 12 clean negatives: some eclipse-compatible reading has a unique survivor whose eclipse has h_tot ≥ M_Ody. It reads M_Ody, the target's own eclipse strength, so it is target-side, not a control quantity [r1v5 N15g] | target | 6.5 | `negatives.py` |

No likelihood ratio, Bayes factor, PC-S recall or G_DOC is a rule input.
They are reported (1.3, 5.3, 5.7, 6.2). The thresholds, the projections and
the disclosure table are in `data/prereg/verdict_rule.json`,
`pcr_projection.json`, `almagest_regimes.json` and `heldout_disclosure.json`,
frozen at the first freeze, before any of these quantities is computed.

### 9.2 The rule

`odybench/verdict_rule.py` implements exactly this, as a pure function of the
quantities above:

```
if not INSTR:                                         return BLOCKED (no verdict is read)
labels, qualifiers = {}, {}
LEGS  = (AL_bf, AL_st, WO_bf, WO_st)
POOLS = (P_BM, P_MWRA, P_BM_E, P_MWRA_E)

# gate 3a: four legs, the decision taken against "the method can see" (6.3.2)
def fire3a(v): return min(seen_PCR[v][leg] for leg in LEGS) < 4
side = fire3a(main)
if side:                                              labels += 3a
# gate 3b: two legs (6.4)
fire3b = min(seen_ALM_SL[bf], seen_ALM_SL[st]) < 6
if fire3b:                                            labels += 3b
if (side and max(seen_PCR[main][leg] for leg in LEGS) >= 4) or \
   (fire3b and max(seen_ALM_SL[bf], seen_ALM_SL[st]) >= 6):
                                                      qualifiers += Q_score
if rec_ALM_BM < 6:                                    qualifiers += Q_BM
if held_ALM < 6:                                      qualifiers += Q_H
if fire3a(redraft) != side or fire3a(sibling) != side:
                                                      qualifiers += Q_exposure
if fire3a(noncirc) != side:                           qualifiers += Q_dT

# null-side qualifiers (known at the second freeze)
p_H_min = max((1 + x_max[P]) / (1 + n[P]) for P in POOLS)    # 7.2
if p_H_min > 0.05:                                    qualifiers += Q_attain
if Q_record:                                          qualifiers += Q_record   # from attain.json, 7.2
g2  = {v: G_BM_lo[v] >= 0.20 for v in SLOTS}           # SLOTS = v0..v5
tol = {v: G_BM_lo[v] >  0.05 for v in SLOTS}
if all(tol.values()):                                 qualifiers += Q_tol
if len(set(g2.values())) > 1 or len(set(tol.values())) > 1:
                                                      qualifiers += Q_slot
if not any(0 < G_j[j] and G_j_hi[j] <= G_BM_u for j in clean_negatives):
                                                      qualifiers += Q_attain4

# target-side qualifier
if Q_contra:                                          qualifiers += Q_contra   # from heldout.json, 7.1

# 4: the eclipse-matching method dates fiction
if any(hit_j[j] and G_j_hi[j] <= G_BM_u for j in clean_negatives):
                                                      labels += 4

# 2: B&M's match carries no weight
if r_Ody == 0:                                        labels += "2 (no match)"
elif all(g2.values()) or pct_N4_lo >= 0.50:           labels += "2 (ordinary)"

# 1: the text dates the return, by the clues nobody fitted; no gate vetoes it (1.3)
p_H = max(p[P] for P in POOLS)                        # p[P] = 1 if the target is not a member of P
if T0_pass and p_H <= 0.05:                           labels += 1

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
  - P_BM, the candidates that 𝒢_BM* accepts, and P_MWRA, those that pass
    the Mercury event B&M applied, each over the whole background and within
    ±700 years of the target, are the null pools of the held-out test
    (label 1). The rule reads the largest p.
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
  computed before the target is looked at, and Q_attain prints it with
  every verdict.
- **Why no gate vetoes label 1** [r1v5 N1 fix 5]. The held-out test is exact:
  its chance of a false "yes" is at most 5% whatever its power. The gates
  measure power, and so do Q_BM and Q_H. They tell the reader which "no"s
  mean nothing. They cannot make a valid "yes" invalid. Revision 5 already
  argued this for Q_BM and Q_H (S11) and kept the veto for 3a and 3b. The
  veto is gone, and label 4, which concerns the eclipse match, never bore
  on the held-out test.
- **Why Q_record is printed in every verdict** [r1v5 N2]. Q_attain asks
  whether the test could have said "yes" for some target. Q_record asks
  whether it could have said "yes" for this one, given what was on record
  before its predicates were frozen. Both are known at the second freeze.
  - For this target, the record settles H4, and every pass pattern below
    0.05 needs H4. So the held-out "no" is not a blind result, and the
    verdict says so instead of presenting it as one.
  - If the bench nonetheless measures H4 as passing, Q_contra prints that
    the record has been contradicted. A label 1 then stands beside it,
    because a predicate believed to fail when it was frozen cannot have
    been chosen to pass.
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
  - outcome 4 uses the negative's upper bound, and Q_attain4 says when no
    negative could have met it;
  - label 1's p_H is exact, ties count against the target, and it is the
    largest of four pools' p-values, so it stays valid if any one pool is
    exchangeable with the target (7.2);
  - **the gates take the decision against "the method can see"** across
    every scoring chosen after the answers were read: 3a fires if any of its
    four legs fails, 3b if either of its two does (6.3.2, 6.4) [r1v5 N1].
- **Why 0.05 and 0.20 over T_A.** These thresholds were written in revision
  3 (2026-10-04, file time 03:21 local), before the recheck estimated G_BM
  (its `check_gbm.py` ran from 03:35, and its report is timed 03:53).
  Revisions 4–6 keep them unchanged, and the order is recorded here [r2
  R2-1 fix 1]. They are frozen at the first freeze, before the bench
  computes any G.
  - Revision 2's thresholds, 0.01 and 0.05, were set for G over T_C. For
    𝒢_BM*, G over T_C is (n_A/n_TC) × G over T_A, about 0.147 × G over T_A
    [r2], because targets outside A are never reached (4.2).
  - Revision 2's 0.01 therefore corresponds to about 0.07 over T_A, and its
    0.05 to about 0.34.
- **The gates' thresholds** (4 of 7 and 6 of 11) and the 5% narrowing were
  set in revision 2, after the drafter's truth-side check (2.6). They are
  kept. Under the family of legs they cannot be what makes a gate pass.
- **Label combinations.** Any of labels 1, 2, 3a, 3b and 4 can hold
  together, and the two forms of label 2 exclude each other. The headline
  is ordered:
  1. Q_contra, if it holds, because it says that the record, the inference
     or the bench is wrong;
  2. label 1;
  3. 3a and 3b, which say which "no"s mean nothing;
  4. label 2;
  5. label 4;
  6. then Q_attain, Q_record and Q_attain4, which say which outcomes could
     not have been reached.
- **When 1 and 2 hold together**, the headline reads: the clues nobody
  fitted date the return, and B&M's own match is not what shows it.
- **When 1 holds with 3a, 3b or 4**, it reads: the clues nobody fitted date
  the return by an exact test; separately, the eclipse component, or the
  B&M-type component, cannot see, or the eclipse-matching method dates
  fiction.

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

I14(b) checks every set against C1–C11. I14(c) reruns the sets at the
null-side stage with the measured values.

| # | constraint | why |
|---|---|---|
| C1 | 0 ≤ G_lo ≤ G ≤ G_hi ≤ 1 for every G, G_j included, and G_hi ≥ U0(n) = 3.69/n with n its pool size | the interval of 5.3 |
| C2 | G_BM,u = (n_A(v)/n_T) · G_BM(v) for v1–v5, the same number for each | no target outside T_A(v) is reached by 𝒢_BM* (4.2) |
| C3 | if r_Ody = 0, pct_N4 is undefined; otherwise pct_N4,lo ≤ pct_N4 ≤ pct_N4,hi, each computed from integer counts x_gt, x_eq and n_stratum ≥ 200 as in 5.4 | 5.4 |
| C4 | if hit_j, then G_j > 0 and G_j,hi ≥ U0(n_j) | a unique survivor in the core has reach > 0 |
| C5 | the counts are integers: every seen_PCR leg of every variant, and strict_PCR, lie in 0..7; seen_ALM_SL's legs and rec_ALM_BM in 0..11; held_ALM in 0..8 | definitions; three counted sets have no held-out row (6.4) |
| C6 (attainability) | outcome 1 is attainable only if p_H,min ≤ 0.05; outcome 4 only if some clean negative has 0 < G_j and G_j,hi ≤ G_BM,u, both on the null side | 7.2, C4 [r1v5 N5] |
| C7 (the null side is fixed) [r2 R2-1 fix 2] | the null-side fields equal the design-stage estimates of 2.9, or after the null-side stage the measured values: n_T, n_A(v), G_BM(v) with bounds, G_BM,u; for each of the four held-out pools its n, x_max and the counts of members passing H3 and H4; p_H,min; Q_record. **G_j, its bounds and n_j have no design-stage estimate** [r1v5 N5]. Until the null-side stage, a set whose labels or qualifiers depend on them is marked **pending**: it shows that a code branch works, and proves no outcome reachable. A set that departs from the other null-side fields is a **branch test** | R2-1 |
| C8 | in each pool P, p_P = (1 + x)/(1 + n_P) for an integer x with x_max,P ≤ x ≤ n_P, x fixed by the target's pass pattern (both, H4 only, H3 only, neither) and the pool's counts; p_H = the largest of the four p_P ≥ p_H,min. With the design-stage counts the attainable values of p_H are 0.040 (both), 0.069 (H4 only), 0.276 (H3 only) and 1 (neither) | 7.2 |
| C9 | T0 ∈ {R, RE} implies T0_pass | 3.5 |
| C10 | within one projection, a strict leg is at most its best-fit leg: seen_PCR[v][AL_st] ≤ seen_PCR[v][AL_bf], seen_PCR[v][WO_st] ≤ seen_PCR[v][WO_bf], and seen_ALM_SL[st] ≤ seen_ALM_SL[bf] | a set seen strictly has a non-empty S₀, so B = S₀ (6.3.2) |
| C11 | the disclosure table's `determined` values are frozen, and a set may not change them. A set whose target flags contradict them is realisable, and it must print Q_contra | 7.1 |

**Known facts, not constraints.** Some target-side and control facts are
already known or inferred:

- T0_pass is true and T0 is RE;
- the disclosure table settles H4 to fail, so p_H ≥ 0.276 (2.10);
- the target passes MWRA readings, so it is a member of all four pools
  (2.9);
- rec_ALM_BM ≤ 5;
- seen_ALM_SL ≤ 9 on either leg;
- both all-must-pass legs of gate 3a are at most 3, and strict recall holds
  in 4 counted sets (rough; AppT 6).

A realisable set may contradict these, because the rule must also be shown to
work for data that differ from the Odyssey's. Each set that does is marked
in 9.5. What a realisable set may not contradict is the null side.

### 9.5 Synthetic input sets that prove every outcome reachable

`data/prereg/verdict_synthetic/*.json` holds these inputs.
`tests/test_verdict.py` asserts the stated output for each (I14a) and checks
it against 9.4 (I14b). `results/design-revision-v6/verdict_trace.py` is an
executable transcription of 9.2 and of C1–C11 for revision 6. It computes
each pool's p from the target's pass pattern and the pool's counts, with the
weights of 7.2 taken over pool and target. It reproduces every label,
qualifier and realisability mark of the table below [me: the script and its
`.out.txt`]. Revision 5's sets keep their names; S0x, S14 and S15 are new.

**The outcomes, one set each:**

- **S1** reaches outcome 1;
- **S2** reaches outcome 2, and **S2nm** its "no match" form;
- **S3a** and **S3b** reach the two parts of outcome 3;
- **S4** reaches outcome 4;
- **S0** is inconclusive, and **S0x** is the verdict expected on known
  facts.

S1, S2, S2nm, S3a, S3b, S0 and S0x are realisable: their null side is the
design-stage estimate of 2.9. **S4 is pending** until G_j is measured at
the null-side stage [r1v5 N5]: outcome 4 is not ruled out, and not yet shown
attainable.

**The base set, S0.** Every other set starts from it and lists only what
differs.

- **The rule:** INSTR true; T0_pass true, T0 RE.
- **The null side, at the design-stage estimates of 2.9:**
  - G_BM by variant: v0 0.224 [0.139, 0.344]; v1 0.140 [0.087, 0.215]; v2
    0.211 [0.131, 0.324]; v3 0.278 [0.172, 0.427]; v4 0.182 [0.112, 0.279];
    v5 0.327 [0.203, 0.504];
  - n_T 10,690; G_BM,u 0.00172;
  - the held-out pools, as (n; members passing H3 only, H4 only, both):
    - P_BM (76; 14, 1, 1);
    - P_MWRA (43; 8, 1, 0);
    - P_BM,E (49; 9, 1, 1);
    - P_MWRA,E (28; 6, 1, 0);
  - p_H,min = max(0.026, 0.023, 0.040, 0.034) = 0.040;
  - the disclosure table: H4 = fail, so Q_record holds.
- **The target side:**
  - the target is a member of all four pools and passes H3 only: p 0.221,
    0.227, 0.240 and 0.276, so p_H = 0.276;
  - r_Ody 0.0815;
  - pct_N4: x_gt 30, x_eq 10 of n_stratum 200, giving 0.175 [0.104, 0.262].
- **The controls:**
  - gate 3a: every leg 5, in every variant;
  - gate 3b: both legs 7; rec_ALM_BM 3; held_ALM 7.
- **The negatives** (pending, C7): every hit false; G_j 0.0006 with
  G_j,hi 0.0012 and n_j 10,690. These are placeholders.

| set | differs from S0 | labels | qualifiers | null side (C7) | contradicts a known fact? |
|---|---|---|---|---|---|
| **S0** | — | **{inconclusive}** | Q_BM, Q_tol, Q_slot, Q_record | realisable | gate 3a's all-must-pass legs, expected at most 3 |
| **S0x** | gate 3a legs AL_bf 4, AL_st 2, WO_bf 3, WO_st 3, in every variant | **{3a}** | Q_BM, Q_tol, Q_slot, Q_record, Q_score | realisable | none: the verdict expected on known facts (2.10) |
| **S1** | the target passes H3 and H4: p 0.026, 0.023, 0.040, 0.034, so p_H 0.040 | **{1}** | Q_BM, Q_tol, Q_slot, Q_record, **Q_contra** | realisable | H4, settled to fail (D1–D2); gate 3a's legs |
| S1b | H4 only: p 0.039, 0.045, 0.060, 0.069, so p_H 0.069 | {inconclusive} | Q_BM, Q_tol, Q_slot, Q_record, Q_contra | realisable | H4; gate 3a's legs |
| **S2** | pct_N4: x_gt 118, x_eq 12, giving 0.620 [0.518, 0.716] | **{2 (ordinary)}** | Q_BM, Q_tol, Q_slot, Q_record | realisable | gate 3a's legs |
| **S2nm** | r_Ody 0; pct_N4 undefined | **{2 (no match)}** | Q_BM, Q_tol, Q_slot, Q_record | realisable | gate 3a's legs (r_Ody 0 is the branch R15 allows) |
| **S3a** | gate 3a: every leg 2, in every variant | **{3a}** | Q_BM, Q_tol, Q_slot, Q_record | realisable | none |
| **S3b** | gate 3b: both legs 3 | **{3b}** | Q_BM, Q_tol, Q_slot, Q_record | realisable | gate 3a's legs |
| **S4** | AEN-TROY: hit true, G_j 0.00051, hi 0.00112 | **{4}** | Q_BM, Q_tol, Q_slot, Q_record | **pending** (G_j) | gate 3a's legs |
| S5 | as S1, but 4 members of P_BM pass both, so p_H,min = p_H = 0.0649 | {inconclusive} | Q_BM, Q_tol, Q_slot, Q_record, Q_contra, **Q_attain** | **branch test** | — |
| S6 | as S1, with S2's pct_N4 | {1, 2 (ordinary)} | Q_BM, Q_tol, Q_slot, Q_record, Q_contra | realisable | H4; gate 3a's legs |
| S6b | as S2, but gate 3a legs 4, 2, 3, 2 (re-draft 4, 4, 4, 4; non-circular 5, 4, 4, 4), gate 3b 3 and 3, held_ALM 4; AEN-TROY as S4 | {2 (ordinary), 3a, 3b, 4} | Q_BM, Q_H, Q_ΔT, Q_exposure, Q_record, Q_score, Q_tol, Q_slot | pending (G_j) | — |
| S7 | INSTR false | BLOCKED | — | realisable | — |
| S8 | as S1, but T0_pass false (T0 NR) | {inconclusive} | Q_BM, Q_tol, Q_slot, Q_record, Q_contra | realisable | T0_pass expected true; H4 |
| S9 | as S1, but gate 3a: every leg 3 | **{1, 3a}** | Q_BM, Q_tol, Q_slot, Q_record, Q_contra | realisable | H4 |
| S10 | every variant at v5's values: G_BM 0.327 [0.203, 0.504], n_A 56 | {2 (ordinary)} | Q_BM, Q_tol, Q_record (no Q_slot) | **branch test** | — |
| S11 | as S1, but rec_ALM_BM 7 and held_ALM 4 | {1} | Q_H, Q_tol, Q_slot, Q_record, Q_contra | realisable | rec_ALM_BM ≥ 6; H4 |
| S12 | as S1, but the target is not a member of P_MWRA or P_MWRA,E, so their p is 1 and p_H 1 | {inconclusive} | Q_BM, Q_tol, Q_slot, Q_record, Q_contra | realisable | the target passes MWRA readings (2.9) |
| S13 | as S1, but 2 members of P_MWRA,E pass both: p_MWRA,E 0.103, which is also p_H,min | {inconclusive} | Q_BM, Q_tol, Q_slot, Q_record, Q_contra, **Q_attain** | **branch test** | — |
| S14 | every negative: G_j 0.0030, hi 0.0045 | {inconclusive} | Q_BM, Q_tol, Q_slot, Q_record, **Q_attain4** | pending (G_j) | — |
| S15 | as S1, with gate 3b legs 3 and 3, and AEN-TROY as S4 | **{1, 3b, 4}** | Q_BM, Q_tol, Q_slot, Q_record, Q_contra | pending (G_j) | H4 |

**What each set shows:**

- **The four outcomes and the inconclusive verdict.** S1 reaches 1, S2 and
  S2nm reach 2 in both forms, S3a and S3b reach 3 in both parts, S4 reaches
  4, and S0 is inconclusive.
- **Which are proven reachable now.** S1, S2, S2nm, S3a, S3b and S0 are
  realisable on the design-stage null side. The only known fact S1
  contradicts is target-side: H4, which the record settles to fail. That is
  why Q_record holds in every set, and why S1 also prints Q_contra. S4's
  realisability waits for G_j.
- **The expected verdict.** S0x reproduces it: {3a}, with Q_score because
  one leg sits at its threshold.
- **One way to a "yes".** S1 passes both held-out predicates. S1b passes H4
  alone: on the four-pool lattice that gives 0.069, so it is no longer
  enough, which is the cost of the epoch pools.
- **What blocks label 1:** T0_pass false (S8); a target outside some pools
  (S12); or a pool whose floor exceeds 0.05 (S13, a branch test, because on
  the design-stage counts every pool's floor is below 0.05).
- **What does not block it:** the gates and the control qualifiers. S9 shows
  label 1 with 3a, S15 with 3b and 4 (pending), and S11 with Q_H and without
  Q_BM.
- **Co-occurrence.** S6 shows labels 1 and 2 together. S6b shows labels and
  every control qualifier together.
- **Branch tests.** S5 shows the Q_attain branch, S10 the label-2 G leg and
  S13 a single pool's veto. Each needs null-side values that contradict
  2.9, so none proves an outcome reachable. S14 shows Q_attain4, and is
  pending.
- **S7** shows the instrument block.

**At the null-side stage** (12.3), I14(c) replaces the null-side fields by
the measured values, G_j included, and reruns S0–S15.

- Each set keeps the target's pass pattern (both, H4 only, H3 only,
  neither), and each pool's p is recomputed with the measured counts.
- If S1 then no longer returns {1}, outcome 1 is unattainable, and Q_attain
  says so in every verdict.
- The measured G_j settle S4, S6b, S14 and S15. If no clean negative has
  0 < G_j and G_j,hi ≤ G_BM,u, outcome 4 is unattainable, and Q_attain4
  says so.
- Q_record is recomputed from the measured lattice.
- All of this is recorded at the second freeze, before any target-side
  number exists.

