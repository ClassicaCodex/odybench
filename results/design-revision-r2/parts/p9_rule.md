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
- **S9** shows Q_attain: with revision 2's pool the floor is above 0.05.
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

