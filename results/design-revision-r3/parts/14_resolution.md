## 14. Resolution of the reviews

Three tables follow:

- 14.1 gives the 25 issues of `docs/critique-design.md`, the review of
  revision 1;
- 14.2 gives the 17 issues N1–N17 of `docs/critique-design-r1.md`, the
  recheck of revision 2, numbered 26–42 as the latest recheck numbers them;
- 14.3 gives the 12 issues R2-1 to R2-12 of `docs/critique-design-r2.md`,
  the recheck of revision 3, numbered 43–54 here.

Each row gives the resolution and the sections it changed. Where a
resolution departs from the reviewer's proposed fix, the row says why,
marked **Departure**.

### 14.1 The review of revision 1 (`critique-design.md`)

The latest recheck found 22 of these resolved, and found #1, #17 and #21
unresolved [r2 §1]. Revision 4 resolves those three through the issues of
14.3, as the rows say. It keeps every resolution the rechecks confirmed.

| # | severity | resolution in revision 4 | sections |
|---|---|---|---|
| 1 | blocker | **Now resolved.** The rule is a pure function of named quantities (9.1–9.2). Every condition names its garden, its pool and its stage: null-side, target-side or control. Revision 3's outcome 1 could not be reached, because each of its "yes" conditions was fixed by the sky before the Odyssey was measured: G_BM about 0.14, 1189 BC passing B&M's criteria, and pct_N4 a reach percentile [r2 R2-1]. Revision 4 rests outcome 1 on the clues nobody fitted (H3, H4), scored by an exact rank test whose floor p_H,min (design stage 0.026) is computed with the target masked, before any target-side number (7, 12). B&M's own match is judged by label 2, which now has a "no match" form, and Q_tol says when B&M's readings could not have dated anything. Synthetic sets reach every outcome, the inconclusive verdict, every qualifier and the instrument block. Every set marked realisable uses the design-stage null side (C7), and I14(c) reruns them with the measured null side. The NC condition stays replaced by pct_N4, and G keeps one sense. **Departure:** the review's fix 2 put pct_N4 and an LR in outcome 1. Both are reach-based, so their "yes" was unattainable; pct_N4 stays in label 2 | 1.3, 2.9, 2.10, 3.5, 5.4, 7, 9, 12 |
| 2 | blocker | Resolved, and confirmed by both rechecks. `controls_real.json` is used exactly as licensed (SHA-256 `135fba67…83f8`, verified by the recheck). The searcher never reads a truth file (I13). The re-draft of five exposed rows and the sibling-convention audit stay. The audit now transplants only sourced conventions, between rows whose words state the same feature [r2 R2-10] | 6.3, 6.3.4 |
| 3 | blocker | Resolved, and confirmed. Outcome 3 is split into 3a (PC-R) and 3b (the *Almagest* control of B&M's clue types, scored at B&M's tolerances in regime BM and at the empirical observer slack in regime SL). Leave-one-set-out tolerances are now the ceiling of the out-of-set maximum, so the rule is always defined [r2 R2-9]. Q_BM conditions every "no" that rests on B&M's tolerances. Q_H adds a calibration of the held-out test on the same records | 1.3, 2.6, 6.4, 9 |
| 4 | major | Resolved, and confirmed. The freeze is a local git commit of the design, the prereg files and all code. `PREREG.sha256` holds the commit hash, the tree hashes and a code tree hash. Revision 4 adds a second freeze for the null-side record. Amendments are dated and state which outputs had been read. Publishing the hash outside the machine is optional and needs Jon's permission | 12 |
| 5 | major | Resolved, and confirmed. P4 compares λ with E against B&M's printed 0.048. The comparison with 0.88 per century is now regression expectation R13, because the known rate sits near its bound [r2 R2-5] | 1.1, 2.4, 2.7, 8 |
| 6 | major | Resolved, and confirmed. MacDonald was read; the conditioning reason is frozen and applied uniformly. Revision 4 extends it to the clues B&M cited as support: H2 is not counted (7.1). The slot widths that implement the conditioning are a frozen family [r2 R2-2] | 1.1, 4.2, 5.1, 5.3, 7 |
| 7 | major | Resolved, and confirmed. The gardens are nested and sourced. 𝒢_BM* has 36 readings, 𝒢_DOC* 35,964 and 𝒢_FULL* 767,232 (the recheck reproduced them). The greedy smallest fork set is reported. The recheck notes that 18 of 𝒢_BM*'s 36 readings duplicate the other 18; that is recorded (2.9) | 5.3, 2.9 |
| 8 | major | Resolved, and confirmed: F1b, PC-S jitter of 0–3 d, and the decay curves | 5.3, 6.2 |
| 9 | major | Resolved, and confirmed: C_rel and E_rel outside T0b. The recheck's calibration (h_A 2.04°, h_P 0.92°) is recorded, with its note that h_P is a fit, not a visibility | 4.5, 2.9 |
| 10 | major | Resolved, and confirmed: hit strengths come from the mixture, the background runs from −1999, and the target is excluded from its own base rate | 4.1, 4.4, 5.2 |
| 11 | major | Resolved, and confirmed. The held-out statistic is now a rule input, so revision 4 tightens it. The null pool is P_BM, the candidates that pass the same readings as the target (fix 1). H1, H5 and now H2 are not counted (fix 2). R_anc's survivors are reported (fix 3) | 7 |
| 12 | major | Resolved, and confirmed. The MWRA is a vertex fit at ±1.5 d; flat maxima are flagged. I6 now gives flat maxima their own tolerance, and I7 a tie band [r2 R2-4] | 3.2, 6.1 |
| 13 | major | Resolved, and confirmed. Every derived quantity has a second path (10.4). Revision 4 adds I15 for the held-out predicates. I2, I6, I7 and I9 now have pass criteria that a correct implementation can meet [r2 R2-4, R2-7] | 6.1, 10.4 |
| 14 | major | Resolved, and confirmed. PC-S has an instrument mode (I10) and a science mode, and feeds no rule. I10b now has one estimand, and both are reported beside INSTR [r2 R2-4] | 6.1, 6.2 |
| 15 | major | Resolved, and confirmed. The Iliad is a same-tradition comparison, with 12 clean negatives. Readings whose eclipse is not on Day 0 are mapped to their eclipse [r2 R2-12] | 6.5 |
| 16 | major | Resolved, and confirmed. No likelihood ratio enters the rule. The ceiling 1/P(A) is a standing finding. Every G has an interval, now the wider of the gamma interval and a block bootstrap [r2 R2-6]. **Departure** (kept from revision 3): the review wanted the LR to decide outcomes 1 and 2. On a fixed poem every such ratio is set by the observation model [r1 N1] | 5.3, 5.7, 9 |
| 17 | major | **Now resolved.** Everything computable from known numbers is in section 2 with its numbers, including the recheck's G_BM, slot table, r_Ody and near misses, R_anc's 9 survivors, BF_BM 2.6 and the rates (2.9). Revision 3's P4, P6, P12, P13, P14, P19, P22, P30–P35 are settled, regression expectations or dropped (2.7). Section 8 keeps for counting only quantities that need new runs [r2 R2-5] | 2.7, 2.9, 2.10, 8 |
| 18 | major | Resolved, and confirmed. R_anc's season comes from ancient definitions, and it is run with and without the eclipse clue. Revision 4 reports its four season bounds with equal prominence, and records that the union was adopted after the Sun's longitude at 30 Sep 1131 BC was known [r2 R2-11] | 5.3, 2.9 |
| 19 | minor | Resolved, and confirmed: one Espenak–Meeus model, four in the mixture | 0, 2.3 |
| 20 | minor | Resolved, and confirmed: A1–A5 are regression tests; I3 is a reported calibration | 3.4, 6.1 |
| 21 | minor | **Now resolved.** smag is NASA's magnitude exactly: the covered fraction while partial, the diameter ratio while central, as `program.js` prints it. The partial formula alone is `smag_partial`, used only where the reference uses it (I2b). I2(a) compares smag with the catalogue directly, and X3, h_09 and h_06 read smag at annular eclipses [r2 R2-7] | 0, 6.1, 4.4 |
| 22 | minor | Resolved, and confirmed: epoch −1176.68; a half-open window; R6 | 0, 3.2 |
| 23 | minor | Resolved, and confirmed. The T0 grid stays. T0b's reading is a member of 𝒢_BM*. Outcome 1 reads T0_pass, and T0 itself is reported | 3.5, 5.3 |
| 24 | minor | Resolved, and confirmed. New slips corrected: "near morning elongation" was not MacDonald's wording (4.2); I10b's pool size (6.2) | 4.2, 6.2 |
| 25 | minor | Resolved, and confirmed: HIP numbers verified; Sirius uses the barycentric proper motion | 2.1 |

### 14.2 The recheck of revision 2 (`critique-design-r1.md`, issues 26–42)

The latest recheck found 16 of these resolved, and N1 unresolved in
substance [r2 §2].

| # | r1 | severity | resolution in revision 4 | sections |
|---|---|---|---|---|
| 26 | N1 | blocker | **Now resolved in substance.** The LR left the rule in revision 3, and the ceiling 1/P(A) is a standing finding (fixes 1, 2a, 4). The substance was that the bench could not say "yes". It now can: outcome 1 rests on the exact held-out test, whose floor (0.026 at the design stage) is computed before the target is read. Fix 3 is generalised correctly this time. Q_attain tests p_H,min, the floor of the evidence outcome 1 actually reads, and not revision 3's U0(n_A), which was the floor of a quantity the sky had already fixed. C7 bars synthetic sets from inventing a null side | 1.3, 2.10, 7, 9.4, 9.5, 12.3 |
| 27 | N2 | major | Resolved. Leave-one-set-out tolerances are now ceilings of the out-of-set maximum [r2 R2-9]. rec_PCS stays out of the gate | 6.4 |
| 28 | N3 | major | Resolved. B&M's option rule is named, and Q_BM is a regression expectation (R9) | 6.4, 8 |
| 29 | N4 | major | Resolved. The mixture scores every ΔT-dependent control row, and the circular controls are tested by Q_ΔT | 6.3.3 |
| 30 | N5 | major | Resolved. Re-draft and audit; the audit is narrowed to sourced conventions between rows stating the same feature [r2 R2-10] | 6.3.4 |
| 31 | N6 | major | Resolved, and extended. C, V and M are conditioned on; E is left out. RE counts for nothing, because outcome 1 reads T0_pass, which uses no E. The slot widths form a frozen family [r2 R2-2]. H2, a clue B&M cited, is not counted | 1.1, 3.5, 4.2, 5.3, 7 |
| 32 | N7 | major | Resolved. Revision 4 also moves the recheck's newly settled items (14.3, #47) | 2.7, 8 |
| 33 | N8 | major | Resolved. R_obs is exact; every G has an interval, now allowing for dependence [r2 R2-6]; one reach definition | 5.3, 5.7 |
| 34 | N9 | minor | Resolved. Ancient season bounds; R_anc with and without the eclipse; the four bounds are reported alike [r2 R2-11] | 5.3 |
| 35 | N10 | minor | Resolved. Ē_N4 is compared with G_BM (P17); pct_N4 stays a percentile | 5.4, 8 |
| 36 | N11 | minor | Resolved. The X-class mapping is recorded, and QS-SACK-06:a is scored at its own day and site, with its survivor mapped to its eclipse [r2 R2-12] | 6.5, 10.3 |
| 37 | N12 | minor | Resolved: `ephemeris=`, `refraction=`, a constant ΔT, one Day 0 per clock, spans per site | 4.1, 4.2, 10.2 |
| 38 | N13 | minor | Resolved: ±1.5 d continuous is the primary MWRA tolerance | 3.2, 5.3, 6.4 |
| 39 | N14 | minor | Resolved: H3 is one predicate | 7 |
| 40 | N15 | minor | Resolved. I3 is out of INSTR. I2b names both sides and compares smag_partial with the reference's partial formula [r2 R2-7] | 6.1 |
| 41 | N16 | minor | Resolved: a brief-only re-drafter, with the exposure limit stated | 6.3.4 |
| 42 | N17 | minor | Resolved | 6.4 |

### 14.3 The recheck of revision 3 (`critique-design-r2.md`, issues 43–54)

| # | r2 | severity | resolution in revision 4 | sections |
|---|---|---|---|---|
| 43 | R2-1 | blocker | **Fix 1, in a two-stage form.** The null-side quantities (G_BM per slot variant, G_DOC, G_BM,u, n_A, n_T, and the held-out floor p_H,min) are computed by frozen code after the first freeze, with the target masked, and committed at a second freeze before any target-side number. The recheck's estimates are in 2.9 now. The thresholds 0.05 and 0.20 were frozen in revision 3 before the recheck's estimate and are unchanged; the order is recorded (9.3). **Fix 2.** Q_attain is redefined on the floor of the evidence outcome 1 reads, p_H,min. Constraint C7 fixes every synthetic set's null side to the measured or design-stage values, so revision 3's unrealisable S1 is gone. Branch tests are marked as such. **Fix 3.** Q_tol states in every verdict when B&M's readings could not have dated anything at 5% (expected: G_BM,lo ≥ 0.087 under every variant), beside 1/P(A). **Fix 4.** Outcome 1 rests on the held-out predicates H3 and H4, promoted to a rule input as an exact rank test against P_BM. Their attainability is estimated now (p_H,min 0.026, target excluded before any computation) and recomputed at the null-side stage. No threshold on G was relaxed. **Departure:** the review asked for G_BM to be computed "before the freeze". The task also requires that no null result exist before the freeze. The two-stage freeze satisfies both: thresholds and code are frozen first, and the null side is frozen before the target side | 1.3, 2.9, 2.10, 3.5, 7, 9, 12 |
| 44 | R2-2 | major | **Fix 1.** The documented slot is defined with its sources: v0, Venus a visible morning star and Mercury at a named turning point within the *Almagest* slack and visible. MacDonald's reading is restated from the primary: he dates the greatest elongation and does not say "near". **Fix 2.** Six variants are frozen in `slots.json`, and the day counts are paired. **Fix 3.** Every G-based decision is taken under all six, against the claim. Q_slot reports a decision that differs ("slot-dependent"). Label 1 does not depend on the slots, because its null pool is P_BM. **Departure:** a "near greatest elongation" Venus slot (v6) is reported but kept out of the family, because the only width that admits MacDonald's own case is set by the target's value | 4.2, 5.3, 9 |
| 45 | R2-3 | major | **Fix 1.** r_Ody = 0 gives label 2 in its "no match" form, and pct_N4 is not computed. **Fix 2.** pct_N4 is mid-p, and its lower bound counts ties for the Odyssey, so ties cannot fire label 2. **Fix 3.** 2.9 and 2.10 state that the branch turns on 26 Mar 1111 BC, and R15 reports both branches | 1.3, 2.9, 2.10, 5.4, 8, 9 |
| 46 | R2-4 | major | **Fix 1.** I10b has one estimand: truths drawn from T_C and accepted by A(t, δ), all 892 core truths per noise cell. **Fix 2.** INSTR holds only checks that guard rule inputs; I3, I10, I10b and I12 are reported. **Fix 3.** I7 has tie bands (0.01 d, 0.05 min), listed. Beyond the fix, every INSTR criterion was rechecked: I2's totality tolerance allows the reference's 5-s grid; I5(b) allows both convergence tolerances; I6(a) treats flat maxima apart; I9(b)'s Monte Carlo coverage allows three standard errors; I4 has a type tie band | 6.1, 6.2 |
| 47 | R2-5 | major | P12, P19, P32, P33 and P35 are moved: P12 to R15 with its near misses, P19 into R11, P32 to R16, P33 dropped, P35 replaced by 2.10. P4 and P6 are regression expectations R13 and R14, with the note that they sit on their thresholds. A new counted P5 asks the open question, clustering. P22 is dropped, and its value is reported with n = 4. P13, P14 and P34 are in 2.7 and R17 | 2.7, 2.9, 8 |
| 48 | R2-6 | minor | G's interval is the wider of the Fay–Feuer gamma interval and a moving-block bootstrap over the core (136-year blocks; 243-year reported). I9(b) checks coverage on synthetic cores built from real 243-year blocks, so real clustering is kept | 5.3, 6.1 |
| 49 | R2-7 | minor | smag is defined as `program.js` prints it (section 0). I2(a) compares smag with the catalogue's `mag`. `smag_partial` serves I2b. X3, h_09 and h_06 read smag, so an annular eclipse passes by its diameter ratio | 0, 6.1 |
| 50 | R2-8 | minor | **Fix 1.** Epics are drawn until at least 200 enter, and C3 now reads n_stratum ≥ 200 on the entering subset. **Fix 2.** Every clue type has an 18-option fork set × 2 day counts = 36 readings | 5.4, 9.4 |
| 51 | R2-9 | minor | SL tolerance = the out-of-set maximum rounded up to the next whole day: Mercury 6 d (5 d for ALM-G), Venus 21 d, opposition 1 d. The grid's history: the note itself calls 5 or 7 and 21 "the *Almagest* slack" [alm §5 item 1], which suggests that the list was written with the measured slack in view. The bench no longer takes SL values from it. R10 is unchanged | 6.4, 13 |
| 52 | R2-10 | minor | Only conventions with an outside source stated in the file are transplanted, and only into rows whose licence words state the same feature. The drafter's own choices, such as T2-SEASON's 330° start, are never transplanted. The pairs and the excluded transplants are frozen, without the truth, in `sibling_pairs.json` | 6.3.4 |
| 53 | R2-11 | minor | R_anc's four season bounds are reported with equal prominence. 5.3 records that revision 3 adopted the union after the Sun's longitude at 30 Sep 1131 BC (176.69°) was known | 5.3 |
| 54 | R2-12 | minor | A survivor of a reading whose eclipse option sits on another day or site (QS-SACK-06:a) is mapped to its eclipse's conjunction. G_j's targets are the daylight conjunctions at any of the set's observer places, so hit_j and G_j refer to the same event | 6.5 |

---

