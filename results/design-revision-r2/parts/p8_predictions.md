## 8. Pre-registered predictions

Written 2026-10-04, before any null model, control search or held-out check
of the bench was run. Each prediction names its quantity, the script that
computes it and the threshold that decides it.

Revision 3 renumbers the list. The column "v2" gives revision 2's number,
and the predictions that the recheck showed to be settled have moved to
section 2 (table 2.7) [r1 N7]. Items implied by numbers already known are
listed first as **regression expectations**. They need the full run to be
confirmed, and a confirmation is not counted.

### 8.1 Regression expectations (implied by section 2; not counted)

| # | expectation | v2 | basis |
|---|---|---|---|
| R1 | Regression checks A1–A5 pass (`reproduce.py`) | P1 | 2.2, 3.4 |
| R2 | 16 Apr 1178 BC passes N, C, V and M in every cell of the T0 grid | P2 | 2.2 |
| R3 | With E off, the N ∧ C ∧ V ∧ M survivors in 1250–1115 BC number at least 2 and include 18 Mar 1189 BC | P3 | 2.2 |
| R4 | With E ≤ 5 Apr and with E ≤ 6 Apr the survivor set is exactly {16 Apr 1178 BC}; with E ≤ 4 Apr it is empty | P4 | 2.2 |
| R5 | T0 is RE in the primary cell and in every cell with E ≤ 5 or ≤ 6 Apr, and NR in every cell with E ≤ 4 Apr | P5 | 2.2 |
| R6 | The half-open UT+2 window holds 1,683 conjunctions | P7 | 2.2 [rev #22] |
| R7 | In the DE431 pairing the per-model P(total) values move from the canon-frame table of 2.3 by the equivalent of about 40 s. The orderings (1131 above 1178 except under the SMH2016 parabola) and the joint bounds (≤ 0.06 for three models, ≥ 0.08 for SMH2016) are unchanged (`deltat.py`) | P26 | 2.3 [r1 N7] |
| R8 | strict_PCR = 4: the accepted dates fail a primary row in R-PTOL-BAB, R-PTOL-ALEX and R-PYDNA (`controls.py`) | P34 | 2.6 |
| R9 | rec_ALM_BM ≤ 5, so Q_BM holds (`almagest.py`) | P36 | 2.6 |
| R10 | In regime SL the truth is in the best-fit set B of exactly 9 counted *Almagest* sets; it is not in B for ALM-G and ALM-H (`almagest.py`) | — | 2.6 |
| R11 | R_anc with the eclipse clue counts 30 Sep 1131 BC among its survivors in 1250–1115 BC, and not 16 Apr 1178 BC. Without the eclipse clue it has no unique survivor in any window (`garden.py`) | P23 (restated) | 2.8, 5.3 |
| R12 | T0 ≠ R, so outcome 1 does not hold (`verdict.py`) | — | R3, 2.8 |

### 8.2 Predictions (counted)

**Reproduction (T0; `reproduce.py`)**

- **P1.** With C_rel and E_rel in place of the fixed Julian bounds, the
  reproduction-window survivor sets of R3 and R4 are unchanged. (v2 P6)
- **P2.** The T0b survivor sets (E off; E ≤ 5 Apr) do not change when the
  clock ΔT is replaced by SMH2020, SMH2020 + 1σ and SMH2020 − 1σ with DE431
  conjunctions. (v2 P27)
- **P3.** The T0b survivor set with E off is the same under MWRA_vtx at
  ±1.5 d (primary), MWRA_vtx at ±1 d and MWRA_int at ±1 day [r1 N13]. (new)

**Rates (N1; `rates.py`)**

- **P4.** λ(N ∧ C ∧ V ∧ M) over the background lies in [0.44, 1.76] per
  century: within a factor 2 of B&M's own arithmetic at their ±1-day
  tolerance (0.88). (v2 P8)
- **P5.** λ(N ∧ C ∧ V ∧ M ∧ E_rel, n = 4) is at least 0.07 per century,
  above B&M's printed 0.048 (their own arithmetic at ±1 d gives 0.14). (v2 P9)
- **P6.** The background holds at least 10 N ∧ C ∧ V ∧ M survivors, and the
  empirical P(≥ 1 survivor in a 136-year window) is at least 0.5. (v2 P10,
  scaled to the longer background)
- **P7.** p_fix|C lies in [0.002, 0.02] (rough estimate 0.008 [vis §5]); the
  unconditional p_fix lies in [0.0002, 0.002] (rough 0.0007). (v2 P11)
- **P8.** The V–M dependence ratio on P_spring lies in [0.5, 2], with
  permutation p > 0.05. (v2 P12)
- **P9.** Under C_rel, λ(N ∧ C ∧ V ∧ M) in the first and in the last 700
  years of the background agree within a factor 2. Under the fixed Julian
  bounds, fewer than 90% of the candidates that pass the fixed C in
  −1999..−1800 also pass C_rel. (v2 P13, restated for the 2,200-year
  background)

**The eclipse coincidence (N2; `coincidence.py`)**

- **P10.** p_e(M_Ody) over P_spring is within a factor 2 of p_e(M_Ody) over
  P_day, with 16 Apr −1177 excluded from both. (v2 P14)
- **P11.** V and M pass rates do not differ between eclipse and non-eclipse
  spring new moons (permutation p > 0.05 for each). (v2 P15)

**Forking paths (N3; `garden.py`)**

- **P12.** reach_136(16 Apr 1178 BC) under the T0b reading with E off is 0,
  because another survivor falls in −1176..−1052. (v2 P16)
- **P13.** G_BM ≥ 2 × p_fix,unique. (v2 P17)
- **P14.** G_BM (𝒢_BM*, T_A) lies in [0.05, 0.40], and G_DOC ≥ 2 × G_BM.
  (v2 P18, restated for the conditioned pool)
- **P15.** Some reading of 𝒢_DOC*^X makes 30 Sep 1131 BC the unique survivor
  of a 136-year window containing it. (v2 P19)
- **P16.** Some reading of 𝒢_FULL*^X makes 24 Jun 1312 BC the unique
  survivor of a 251-year window containing it. (v2 P20)
- **P17.** G_X(𝒢_BM*) lies within a factor 2 of G_u(𝒢_BM*): eclipse dates
  are not specially reachable. (v2 P21)
- **P18.** The greedy smallest fork set that brings G over T_A to 0.20 adds
  at most four options to 𝒢_BM*. (v2 P22, restated)
- **P19.** R_anc with the eclipse clue has at least two survivors in the
  reproduction window, so it is not unique there either. (v2 P23, restated
  [r1 N7, N9])

**Random epics (N4; `randomepic.py`)**

- **P20.** For variant A epics, P(unique survivor in a 136-year window) lies
  in [0.2, 0.6], and P(T_best ≥ T_obs) ≥ 0.2. (v2 P24)
- **P21.** Ē_N4, the mean reach of Schoch's target over entering stratum
  epics, lies within a factor 3 of G_BM. Varying the poem and varying the
  target give the same null mean [r1 N10]. (v2 P25, restated)

**PC-S (`synthetic.py`)**

- **P22.** Science mode, zero noise: P(unique) under the B&M reading, over
  the truths of T_A that pass it, is ≤ 0.6. (v2 P29)
- **P23.** The B&M reading's recall at j = 3 is at most half its recall at
  j = 0. (v2 P31, restated on recall)

**Controls (`controls.py`, `almagest.py`, `negatives.py`)**

- **P24.** seen_PCR ≥ 4: R-PTOL-BAB, R-PTOL-ALEX, R-ARBELA and R-DIOD are
  seen; R-THUC, R-XEN and R-PYDNA are not seen in the primary run. (v2 P33)
- **P25.** seen_ALM_SL ≥ 6: at least 6 of the 9 sets that retain their truth
  (R10) also narrow their window to 5%. (v2 P35; only narrowing is open)
- **P26.** Q_ΔT does not hold: the circular controls keep their gate status
  when their ΔT is widened. (new [r1 N4])
- **P27.** Q_exposure does not hold. (new [r1 N5])
- **P28.** No clean negative fires outcome 4, and at least one clean negative
  has a unique survivor of some kind in one of the two Odyssey windows.
  (v2 P37)
- **P29.** Some eclipse-compatible reading of IL-PATROCLUS makes an eclipse
  new moon with h_09 ≥ 0.5 at Troy the unique survivor of the 251-year
  primary window. (v2 P38)

**Held-out clues (`heldout.py`)**

- **P30.** 16 Apr 1178 BC passes no more of H2, H3 and H4 than their
  conditional base rates predict (Poisson-binomial p > 0.1). (v2 P39, H3
  counted once)
- **P31.** Over all 𝒢_BM* survivors, the held-out pass rate lies within the
  95% interval of the conditional base rate. (v2 P40)

**Evidential weight (`verdict.py`, standing findings)**

- **P32.** BF_BM(ρ = 1) < 5. (new; the single-reading figure of about 8 in
  2.8 is a rough ceiling, and the garden average is new)
- **P33.** The median *Almagest* Bayes factor over the 11 counted sets is at
  least 10 × BF_BM(ρ = 1). (new [r1 N1 fix 4])

**Bottom line (`verdict.py`)**

- **P34.** G_BM falls in the inconclusive band: G_BM,lo < 0.20 and
  G_BM,hi > 0.05.
- **P35.** The verdict is {inconclusive} or {2}, with Q_BM, and contains no
  3a, 3b or 4.

---

