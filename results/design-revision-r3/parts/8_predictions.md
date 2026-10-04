## 8. Pre-registered predictions

Written 2026-10-04, before any null model, control search or held-out check
of the bench was run. Each prediction names its quantity, the script that
computes it and the threshold that decides it.

Revision 4 renumbers the list again [r2 R2-5]:

- The column "v3" gives revision 3's number.
- Revision 3's predictions that the recheck found settled or nearly settled
  have moved to section 2 (table 2.7). The ones that remain checkable are
  now regression expectations.
- The regression expectations are listed first. They need the full run to
  be confirmed, but they are implied by numbers already known, and a
  confirmation is not counted.

### 8.1 Regression expectations (implied by section 2; not counted)

| # | expectation | v3 | basis |
|---|---|---|---|
| R1 | Regression checks A1–A5 pass (`reproduce.py`) | R1 | 2.2, 3.4 |
| R2 | 16 Apr 1178 BC passes N, C, V and M in every cell of the T0 grid, so T0_pass is true | R2 | 2.2 |
| R3 | With E off, the N ∧ C ∧ V ∧ M survivors in 1250–1115 BC number at least 2 and include 18 Mar 1189 BC | R3 | 2.2 |
| R4 | With E ≤ 5 Apr and with E ≤ 6 Apr the survivor set is exactly {16 Apr 1178 BC}; with E ≤ 4 Apr it is empty | R4 | 2.2 |
| R5 | T0 is RE in the primary cell and in every cell with E ≤ 5 or ≤ 6 Apr, and NR in every cell with E ≤ 4 Apr | R5 | 2.2 |
| R6 | The half-open UT+2 window holds 1,683 conjunctions | R6 | 2.2 [rev #22] |
| R7 | In the DE431 pairing the per-model P(total) values move from the canon-frame table of 2.3 by the equivalent of about 40 s. The orderings (1131 above 1178 except under the SMH2016 parabola) and the joint bounds (≤ 0.06 for three models, ≥ 0.08 for SMH2016) are unchanged (`deltat.py`) | R7 | 2.3 [r1 N7] |
| R8 | strict_PCR = 4: the accepted dates fail a primary row in R-PTOL-BAB, R-PTOL-ALEX and R-PYDNA (`controls.py`) | R8 | 2.6 |
| R9 | rec_ALM_BM ≤ 5, so Q_BM holds (`almagest.py`) | R9 | 2.6 |
| R10 | In regime SL, with the ceiling tolerances of 6.4, the truth is in the best-fit set B of exactly 9 counted *Almagest* sets; it is not in B for ALM-G and ALM-H (`almagest.py`) | R10 | 2.6, 6.4 |
| R11 | R_anc with the eclipse clue counts 30 Sep 1131 BC among its survivors in 1250–1115 BC under the Hesiod-or-Geminus bound, and not 16 Apr 1178 BC. It has about 9 survivors there, so it is not unique. Without the eclipse clue it has no unique survivor in any window (`garden.py`) | R11, P19 | 2.8, 2.9 |
| R12 | Label 1 does not fire, because H4 fails at 1178 BC and p_H is then at least about 0.22 (`heldout.py`) | — (replaces R12 of v3) | 2.10, an inference, not a computation |
| R13 | λ(N ∧ C ∧ V ∧ M) over the background lies in [0.44, 1.76] per century, near the lower bound | P4 | 2.9 |
| R14 | The background holds about 12 survivors of the T0b reading, and the Poisson P(≥ 1 in 136 years) is about 0.53 | P6 | 2.9 |
| R15 | r_Ody = 11/136 = 0.0815, unless the bench's vertex puts 26 Mar 1111 BC within ±1.5 d, in which case r_Ody = 0 and label 2 takes its "no match" form. Both branches are reported, with that candidate's ΔMWRA and flatness flag (`garden.py`) | P12 | 2.9 |
| R16 | BF_BM(ρ = 1) < 5 (about 2.6) | P32 | 2.9 |
| R17 | Under v1, G_BM lies in [0.05, 0.40] and is at least 2 × p_fix,unique. Over the slot family, label 2's G leg does not fire, and Q_tol and Q_slot hold (`garden.py`) | P13, P14, P34 | 2.9, 2.10 |
| R18 | p_H,min ≤ 0.05 on P_BM, so Q_attain does not hold (`attain.py`) | — | 2.9 |

### 8.2 Predictions (counted)

**Reproduction (T0; `reproduce.py`)**

- **P1.** With C_rel and E_rel in place of the fixed Julian bounds, the
  reproduction-window survivor sets of R3 and R4 are unchanged. (v3 P1)
- **P2.** The T0b survivor sets (E off; E ≤ 5 Apr) do not change when the
  clock ΔT is replaced by SMH2020, SMH2020 + 1σ and SMH2020 − 1σ with DE431
  conjunctions. (v3 P2)
- **P3.** The T0b survivor set with E off is the same under MWRA_vtx at
  ±1.5 d (primary), MWRA_vtx at ±1 d and MWRA_int at ±1 day [r1 N13]. (v3 P3)

**Rates (N1; `rates.py`)**

- **P4.** λ(N ∧ C ∧ V ∧ M ∧ E_rel, n = 4) is at least 0.07 per century,
  above B&M's printed 0.048 (their own arithmetic at ±1 d gives 0.14).
  (v3 P5)
- **P5.** Survivors cluster: for the T0b reading, the empirical P(≥ 1
  survivor in a 136-year window), with windows slid one year at a time over
  the background, is below the Poisson value at the same mean count. The
  causes are Venus' 8-year cycle and Mercury's 13- and 46-year
  near-repeats. (new; replaces v3 P6, whose thresholds the known rate
  already sat on [r2 R2-5])
- **P6.** p_fix|C lies in [0.002, 0.02], and the unconditional p_fix in
  [0.0002, 0.002]. The recheck's rough p_fix|C, 0.0054, lies well inside;
  the exact value is new. (v3 P7)
- **P7.** The V–M dependence ratio on P_spring lies in [0.5, 2], with
  permutation p > 0.05 (rough value 0.76). (v3 P8)
- **P8.** Under C_rel, λ(N ∧ C ∧ V ∧ M) in the first and in the last 700
  years of the background agree within a factor 2. Under the fixed Julian
  bounds, fewer than 90% of the candidates that pass the fixed C in
  −1999..−1800 also pass C_rel. (v3 P9)

**The eclipse coincidence (N2; `coincidence.py`)**

- **P9.** p_e(M_Ody) over P_spring is within a factor 2 of p_e(M_Ody) over
  P_day, with 16 Apr −1177 excluded from both. (v3 P10)
- **P10.** V and M, and the held-out predicates H3 and H4, pass at the same
  rates on eclipse and on non-eclipse spring new moons (permutation p > 0.05
  for each). The exactness of p_H rests on this for H3 and H4 (7.2).
  (v3 P11, extended)

**Forking paths (N3; `garden.py`)**

- **P11.** Some reading of 𝒢_DOC*^X makes 30 Sep 1131 BC the unique survivor
  of a 136-year window containing it. (v3 P15)
- **P12.** Some reading of 𝒢_FULL*^X makes 24 Jun 1312 BC the unique
  survivor of a 251-year window containing it. (v3 P16)
- **P13.** G_X(𝒢_BM*) lies within a factor 2 of G_BM,u: eclipse dates are
  not specially reachable. (v3 P17)
- **P14.** The greedy smallest fork set that brings G over T_A(v1) to 0.20
  adds at most four options to 𝒢_BM*. (v3 P18)
- **P15.** G_DOC ≥ 2 × G_BM under v1. (v3 P14, second clause; its first
  clause is settled, 2.7)

**Random epics (N4; `randomepic.py`)**

- **P16.** For variant A epics, P(unique survivor in a 136-year window) lies
  in [0.2, 0.6], and P(T_best ≥ T_obs) ≥ 0.2. (v3 P20)
- **P17.** Ē_N4, the mean reach of Schoch's target over entering stratum
  epics, lies within a factor 3 of G_BM under v1. Varying the poem and
  varying the target give the same null mean [r1 N10]. (v3 P21)
- **P18.** If r_Ody > 0, pct_N4 lies in [0.05, 0.50]: the Odyssey's reach of
  Schoch's target is neither exceptional nor ordinary among random poems of
  its specificity. Among T_A targets, 19.8% reach at least r_Ody [r2], but
  epics are not targets, and the value is new. (new)

**PC-S (`synthetic.py`)**

- **P19.** The B&M reading's recall at j = 3 is at most half its recall at
  j = 0. (v3 P23)

**Controls (`controls.py`, `almagest.py`, `negatives.py`)**

- **P20.** seen_PCR ≥ 4: R-PTOL-BAB, R-PTOL-ALEX, R-ARBELA and R-DIOD are
  seen; R-THUC, R-XEN and R-PYDNA are not seen in the primary run. (v3 P24)
- **P21.** seen_ALM_SL ≥ 6: at least 6 of the 9 sets that retain their truth
  (R10) also narrow their window to 5%. (v3 P25)
- **P22.** Q_ΔT does not hold. (v3 P26)
- **P23.** Q_exposure does not hold. (v3 P27)
- **P24.** Q_H does not hold: at least 6 of the 11 counted *Almagest* sets
  give their true date p ≤ 0.05 on their own held-out rows (6.4). (new)
- **P25.** No clean negative fires outcome 4, and at least one clean
  negative has a unique survivor of some kind in one of the two Odyssey
  windows. (v3 P28)
- **P26.** Some eclipse-compatible reading of IL-PATROCLUS makes an eclipse
  new moon with h_09 ≥ 0.5 at Troy the unique survivor of the 251-year
  primary window. (v3 P29)

**Bottom line (`verdict.py`)**

- **P27.** The verdict is exactly {inconclusive}. Its qualifiers are exactly
  Q_BM, Q_tol and Q_slot. This is the conjunction of P18, the first branch
  of R15, P20–P25 and the expectations R8, R9, R12 and R17. It fails if any
  of them fails, including when r_Ody = 0 gives label 2 its "no match" form.
  (replaces v3 P34 and P35, which were settled or covered both branches
  [r2 R2-5])

---

