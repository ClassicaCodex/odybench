# odybench — the lean run (amendment 1 to DESIGN.md revision 8)

Written 2026-10-09, before any bench code beyond `ephem.py`, `calendar.py`,
`ccx.py` and A0's partial contract files exists, and before any null-side or
target-side quantity has been computed by bench code. It is committed and
pushed to the public repository before any analysis runs, which gives it an
outside timestamp (DESIGN 12.5).

## Why a lean run

The full design needs about 13 more build agents and 15–27 hours of
computation. The facts on record already settle what most of that machinery
was built to find for this target:

- **Outcome 1 cannot be reached for this target.** The disclosure table settles
  H4 as a fail, from facts published before this bench existed (DESIGN 7.1,
  D1–D2). With H4 failing, no pass pattern of the held-out test reaches 0.05
  (Q_record, 7.2). So the components that only guard a "yes" (gate 3a, label
  4) cannot change the verdict on the Odyssey.
- **The quantities that can still change the verdict** are the rest: T0, the
  look-elsewhere statistic G_BM, the held-out test itself (Q_contra can still
  fire), the eclipse at Ithaca, and the *Almagest* calibration of B&M's
  tolerances.

The lean run computes exactly those, with the design's definitions, and
defers the rest. Nothing deferred is dropped: the full design can still be
run later, and this amendment records what had been computed when it was
written.

## What runs

Every definition is the one DESIGN.md revision 8 gives in the section named.
Nothing is redefined here.

| step | DESIGN | what |
|---|---|---|
| T0 | 3.2–3.5 | B&M's search recomputed with DE441 at B&M's clock ΔT; the T0 grid; T0_pass and R / RE / NR |
| N1 | 5.1 | rates of B&M's applied criteria over the background, λ per century, P(≥ 1) per window width, p_fix, the V–M dependence ratio |
| N3 (part) | 4.2, 5.3 | the pools P_all, P_day, P_spring, T, T_C and T_A(v) for v0–v5 (`data/prereg/slots.json`); the 36 readings of 𝒢_BM*; G_BM(v) with its interval, G_BM,u, and r_Ody, the reach of the target |
| N5 (part) | 5.5 | survivors per century and P(≥ 1) as a function of window width, from the N1 arrays |
| N6 | 5.6 | P(total) and P(magnitude ≥ 0.9) at Ithaki for 16 Apr −1177 and 30 Sep −1130 under the four ΔT models and their mixture; totality windows |
| held-out | 7.1–7.3 | H3 and H4 on the four pools P_BM, P_MWRA, P_BM,E, P_MWRA,E; p_H,min, Q_attain, Q_record, Q_exch at the null side; p_H and Q_contra at the target; H1, H2, H5 reported |
| gate 3b | 6.4 | the *Almagest* control at B&M's tolerances (rec_ALM_BM, Q_BM) and at the leave-one-set-out ceiling tolerances (seen_ALM_SL, gate 3b), if the projection can be built from `controls_almagest.json` and A0's `tools/build_regimes.py` within the run. If it cannot, the run reports the observer-slack table of `docs/controls-almagest.md` recomputed by bench code, and says that gate 3b was not run |

## What is deferred

N4 (random epics, so label 2's pct_N4 leg), PC-S (6.2), PC-R and gate 3a
(6.3), the negatives and label 4 (6.5), the 𝒢_DOC*, 𝒢_FULL* and E-on gardens,
R_anc, the evidential findings of 5.7, the access tiers and public export of
10.1, the PC-R re-draft and the sibling audit (6.3.4).

## The rule, restricted

The rule of DESIGN 9.2 with the deferred inputs marked **not tested**:

- **3a and 4** are not evaluated. The verdict prints "not tested" for each.
- **3b** fires if seen_ALM_SL < 6 (when gate 3b runs).
- **Label 2** holds as "no match" if r_Ody = 0. It holds as "ordinary" if
  G_BM,lo(v) ≥ 0.20 for every slot variant v. The pct_N4 leg is not tested.
- **Label 1** holds if T0_pass and p_H ≤ 0.05 and not 3b. It is printed
  "provisional: 3a and 4 not tested".
- **Qualifiers:** Q_attain, Q_record, Q_contra, Q_exch, Q_tol, Q_slot and Q_BM,
  as defined in 7.2, 9.2 and 6.4.
- **Otherwise** the verdict is inconclusive, with every number beside its
  threshold.

The thresholds are those of `data/prereg/verdict_rule.json`, unchanged.

## Instrument checks kept

- I1: `tools/validate_ephem.py` and `tests/test_ephem.py`; I8:
  `tests/test_calendar.py`.
- **A second implementation of the whole null side.** The recheck's own
  `results/critique-design-r2/check_gbm.py` was written independently of
  the bench, and it computes the same pools, readings and G_BM. The bench's
  survivor sets for the T0b reading must equal its survivor sets, and every
  difference in G_BM(v) larger than 0.01 is explained before the verdict is
  read.
- I6(a): the bench's Mercury rise-azimuth maxima against
  `results/bm2008-reconcile/check_mwra.py` on the Table S2 years other than
  −1177.
- I9(a): reach against brute-force sliding windows on synthetic sets.

## Stages

1. **Code and tests.** No survivor set, reach, G, held-out pass rate or
   control search is computed on the real sky. The only real-sky runs are the
   instrument checks above and the replay of the published Table S2.
2. **Freeze 1.** Commit `LEAN.md`, DESIGN.md and the code; tag `prereg-1`;
   push.
3. **Null side, target masked.** `attain.py` builds every pool without
   16 Apr −1177 and computes N1, G_BM(v), G_BM,u, the held-out pools, p_H,min,
   Q_attain, Q_record, Q_exch and, if built, gate 3b.
4. **Freeze 2.** Commit `results/attain/`; tag `prereg-2`; push.
5. **Target side.** T0, r_Ody, N6, p_H, Q_contra and the verdict. Commit and
   push.

## Already known, and so not a finding of the run

These are design-stage estimates computed by reviewers' scratch scripts
(DESIGN 2.9–2.10). The run recomputes each with bench code and reports any
difference:

- T0 is expected to be RE: 18 Mar 1189 BC passes N, C, V and M as well.
- G_BM is about 0.14 under v1, with lower bounds from 0.087 to 0.20 across
  the slot family. So Q_tol is expected, and so is Q_slot.
- p_H,min is about 0.040; Q_record holds.
- P(total at Ithaki, 16 Apr −1177) is about 0.30 under the mixture.
- rec_ALM_BM ≤ 5 (Q_BM expected); seen_ALM_SL about 9 of 11.

So the expected verdict is inconclusive or label 2, with Q_tol, Q_slot,
Q_record and Q_BM. That expectation is not a prediction and is never counted
as a success.
