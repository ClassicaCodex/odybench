## 8. Pre-registered predictions

Written 2026-10-04, before any null model, control search or held-out check
of the bench was run. Each prediction names its quantity, the script that
computes it and the threshold that decides it.

Revision 4 renumbered the list [r2 R2-5]:

- The column "v3" gives revision 3's number.
- Revision 3's predictions that the recheck found settled or nearly settled
  moved to section 2 (table 2.7). The ones that remain checkable are
  regression expectations.
- The regression expectations are listed first. They need the full run to
  be confirmed, but they are implied by numbers already known, and a
  confirmation is not counted.

Revisions 5 and 6 keep the numbering. A withdrawn prediction keeps its
number, so that nothing is renumbered. Revision 6 changes these entries
[r1v5 #17, N1, N5, N8, N11]:

- **P6** (the p_fix bounds) is settled by the rough values, with margin on
  both sides. It becomes R22.
- **P8's second clause** (the overlap of the fixed and relative season
  bounds) is nearly fixed by the C_rel calibration. It becomes R23; P8
  keeps its first clause.
- **P20** (seen_PCR ≥ 4) sat exactly on its threshold, under a scoring rule
  chosen after the answers were read. Its replacement is the expectation
  that gate 3a fires, R24.
- **P22 and P23** (no Q_ΔT, no Q_exposure) follow from known numbers under
  the combined gate. They become R25 and R26.
- **R21** (stationarity of the held-out rates) and **R27** (Q_record) are new.
- **P21, P24, P25 and P27 are restated**: P21 for both legs of gate 3b, P24
  for the ceiling on held_ALM, P25 for outcome 4's attainability, and P27
  for the new expected verdict.

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
| R8 | Strict recall (f(truth) = 0, no narrowing) holds in 4 of the 7 counted PC-R sets under the as-licensed primaries: the accepted dates fail a primary row in three counted sets, named in [AppT 6] (`controls.py`) | R8 | 2.6 |
| R9 | rec_ALM_BM ≤ 5, so Q_BM holds (`almagest.py`) | R9 | 2.6 |
| R10 | In regime SL, with the ceiling tolerances and the word-only projection of 6.4, the truth is in the best-fit set B of exactly 9 counted *Almagest* sets; the two exceptions are named in [AppT 6]. Revision 5's and 6's projection changes (A.10, B.5 and B.9 to none; the literal `same_apparition` options) only loosen rows, so they cannot lose a retained truth (`almagest.py`) | R10 | 2.6, 6.4 |
| R11 | R_anc with the eclipse clue counts 30 Sep 1131 BC among its survivors in 1250–1115 BC under the Hesiod-or-Geminus bound, and not 16 Apr 1178 BC. It has about 9 survivors there, so it is not unique. Without the eclipse clue it has no unique survivor in any window (`garden.py`) | R11, P19 | 2.8, 2.9 |
| R12 | Label 1 does not fire. H4 fails at 1178 BC, as the disclosure table infers from facts on record (7.1, D1–D2), and p_H is then at least about 0.28 on the design-stage lattice. Q_contra does not hold (`heldout.py`) | — | 2.10, 7.1 |
| R13 | λ(N ∧ C ∧ V ∧ M) over the background lies in [0.44, 1.76] per century, near the lower bound | P4 | 2.9 |
| R14 | The background holds about 12 survivors of the T0b reading, and the Poisson P(≥ 1 in 136 years) is about 0.53 | P6 | 2.9 |
| R15 | r_Ody = 11/136 = 0.0815, unless the bench's vertex puts 26 Mar 1111 BC within ±1.5 d, in which case r_Ody = 0 and label 2 takes its "no match" form. Both branches are reported, with that candidate's ΔMWRA and flatness flag (`garden.py`) | P12 | 2.9 |
| R16 | BF_BM(ρ = 1) < 5 (about 2.6) | P32 | 2.9 |
| R17 | Under v1, G_BM lies in [0.05, 0.40] and is at least 2 × p_fix,unique. Over the slot family, label 2's G leg does not fire, and Q_tol and Q_slot hold (`garden.py`) | P13, P14, P34 | 2.9, 2.10 |
| R18 | p_H,min ≤ 0.05 on each of the four held-out pools (design stage: P_BM 0.026, P_MWRA 0.023, P_BM,E 0.040, P_MWRA,E 0.034), so Q_attain does not hold (`attain.py`) | — | 2.9, 7.2 |
| R19 | λ(N ∧ C ∧ V ∧ M ∧ E_rel) at n = 3, 4 and 5 over the background, each with its exact Poisson 95% interval, beside B&M's printed 0.048 per century and their own arithmetic's 0.14. At n = 4 about 1.9 survivors are expected (0.087 per century), so the interval contains 0.048 unless the count reaches 4, which has probability about 0.13. Withdrawn from the counted list as revision 4's P4, because a count this small cannot decide a threshold near 0.048 (`rates.py`) | P5 (v4 P4) | 2.4 [rev #5] |
| R20 | H3 and H4 pass at the same rate in P_BM's MWRA class and in its GWE-or-station class: Fisher's exact p > 0.05 for each (rough: H3 8/43 against 7/33, p 0.78; H4 1/43 against 1/33) (`heldout.py`) | — | 2.9 |
| R21 | **H3 is not stationary over the background, and is stationary within the epoch band.** H3's pass rate differs between the early (−1999..−900) and the late (−899..+200) half of P_BM and of P_MWRA (rough: 12/41 against 3/35, Fisher p 0.041; 8/25 against 0/18, p 0.013), and does not differ between the members within ±700 years of the target and the rest (rough: p 1.0 and 0.69). H4 is too rare to compare (rough: 2/41 against 0/35) (`heldout.py`) [r1v5 N11] | — | 2.9, 7.2 |
| R22 | p_fix\|C lies in [0.002, 0.02], and the unconditional p_fix in [0.0002, 0.002]. Rough values: 0.0054 [r2: check_gbm.py] and about 0.0007 [vis §5], each at least 2.7 times inside its bounds (`rates.py`) [r1v5 #17a] | v5 P6 | 2.9 |
| R23 | Under the fixed Julian bounds, fewer than 90% of the candidates that pass the fixed C in −1999..−1800 also pass C_rel. The C_rel calibration already gives about 87% overlap at −1700 (Ti in about 12 Mar–12 Apr against the fixed 18 Mar–16 Apr), and less earlier (`rates.py`) [r1v5 #17c] | v5 P8, second clause | 2.9 |
| R24 | **Gate 3a fires.** Both all-must-pass legs (AL_st, WO_st) count at most 3 counted sets seen, below 4. The best-fit leg on the as-licensed primaries (AL_bf) is expected at 4, so Q_score is likely, but it is not counted, because 4 is the threshold [AppT 6] (`controls.py`) [r1v5 N1; #17b] | v5 P20 | 2.6, 6.3.2 |
| R25 | Q_ΔT does not hold: scoring the circular sets with every model's σ tripled does not flip gate 3a's combined decision, because its all-must-pass legs stay below 4 [AppT 6] (`controls.py`) | v5 P22 | 2.10, 6.3.3 |
| R26 | Q_exposure does not hold: neither the unexposed re-draft nor the sibling-convention audit flips gate 3a's combined decision, for the same reason [AppT 6] (`controls.py`) | v5 P23 | 2.10, 6.3.4 |
| R27 | Q_record holds at the null-side stage: with H4 = fail in the disclosure table, no consistent pass pattern reaches p_H ≤ 0.05 on the measured lattice (`attain.py`) [r1v5 N2] | — | 2.10, 7.2 |

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

- **P4.** *Withdrawn in revision 5* to the reported comparison R19. The
  number is kept. (v3 P5)
- **P5.** Survivors cluster: for the T0b reading, the empirical P(≥ 1
  survivor in a 136-year window), with windows slid one year at a time over
  the background, is below the Poisson value at the same mean count. The
  causes are Venus' 8-year cycle and Mercury's 13- and 46-year
  near-repeats. (new in revision 4; replaces v3 P6, whose thresholds the
  known rate already sat on [r2 R2-5])
- **P6.** *Withdrawn in revision 6* to the regression expectation R22: the
  rough values lie well inside both bounds [r1v5 #17a]. The number is kept.
  (v3 P7)
- **P7.** The V–M dependence ratio on P_spring lies in [0.5, 2], with
  permutation p > 0.05 (rough value 0.76). (v3 P8)
- **P8.** Under C_rel, λ(N ∧ C ∧ V ∧ M) in the first and in the last 700
  years of the background agree within a factor 2. Its second clause, on
  the fixed bounds, is R23 [r1v5 #17c]. (v3 P9)

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
  epics are not targets, and the value is new. (new in revision 4)

**PC-S (`synthetic.py`)**

- **P19.** The B&M reading's recall at j = 3 is at most half its recall at
  j = 0. (v3 P23)

**Controls (`controls.py`, `almagest.py`, `negatives.py`, `attain.py`)**

- **P20.** *Withdrawn in revision 6* to the regression expectation R24. Its
  count, 4, sat exactly on its threshold, under a scoring rule chosen after
  the answers were read [r1v5 N1, #17b]. The number is kept. (v3 P24)
- **P21.** seen_ALM_SL ≥ 6 on both legs: at least 6 of the 9 sets that
  retain their truth (R10) also narrow their window to 5%, by best fit and
  strictly. (v3 P25)
- **P22.** *Withdrawn in revision 6* to R25. (v3 P26)
- **P23.** *Withdrawn in revision 6* to R26. (v3 P27)
- **P24.** Q_H does not hold: at least 6 of the 11 counted *Almagest* sets
  give their true date p ≤ 0.05 on their own held-out rows, with the
  ceiling tolerances of 6.4. At most 8 sets can qualify by construction,
  and fewer if a truth fails its projection. [AppT 6] gives the truth-side
  number, so this needs 6 of the sets that can qualify [r1v5 N8, #17d].
  (revision 4)
- **P25.** Outcome 4 is attainable and does not fire. At the null-side stage
  at least one clean negative has 0 < G_j and G_j,hi ≤ G_BM,u, so Q_attain4
  does not hold. After the second freeze no clean negative fires outcome 4.
  P25 fails if Q_attain4 holds, because a "no 4" would then mean nothing
  [r1v5 N5]. (v3 P28, restated)
- **P26.** Some eclipse-compatible reading of IL-PATROCLUS makes an eclipse
  new moon with h_09 ≥ 0.5 at Troy the unique survivor of the 251-year
  primary window. (v3 P29)

**Bottom line (`verdict.py`)**

- **P27.** The verdict's labels are exactly {3a}. Its qualifiers include
  Q_BM, Q_tol, Q_slot and Q_record. They exclude Q_attain, Q_contra, Q_ΔT,
  Q_exposure, Q_H and Q_attain4. Q_score is not predicted, because its leg
  sits on the threshold.
  - P27 is the conjunction of P18, the first branch of R15, P21, P24, P25,
    and the expectations R8, R9, R12, R17 and R24–R27.
  - It fails if any of them fails, including when r_Ody = 0 gives label 2
    its "no match" form.
  - (Restated in revision 6 [r1v5 N1]. Revision 5 expected {inconclusive}
    with Q_BM, Q_tol and Q_slot.)

