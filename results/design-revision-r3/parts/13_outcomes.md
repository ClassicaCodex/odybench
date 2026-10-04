### 1.3 Outcomes

The verdict is a set of labels computed mechanically by `verdict.py` from
named quantities (section 9). Every condition names its garden and its target
pool. It also says whether its input is **null-side** (fixed by the sky and
the readings, with the target masked) or **target-side** (it reads 16 Apr
1178 BC) (9.1). Every interval is taken against the claim being made.

Revision 3's outcome 1 asked for G_BM,hi ≤ 0.05. G_BM is null-side, and the
recheck estimates it at about 0.14 (95%: 0.087–0.215). So no sky of 1178 BC
could have met that condition [r2 R2-1]. The same holds for revision 3's
other two "yes" conditions:

- **T0 = R** needs 18 Mar 1189 BC to fail B&M's criteria, and it passes them
  whatever the Odyssey encodes (2.2).
- **pct_N4,hi ≤ 0.05** is a reach percentile of the same kind as G (5.4).

A "yes" therefore has to rest on evidence that B&M did not fit, and whose
power to say "yes" can be checked before the target is looked at [r2 R2-1
fix 4]. The labels are these.

1. **The text dates the return.** All four must hold:
   - **T0_pass.** B&M's applied criteria (N, C, V and M, without the equinox
     clue) pass for 16 Apr 1178 BC with a modern ephemeris (3.5).
     - This is the part of B&M's reproduction that depends on the target's
       own sky.
     - Whether 1178 BC is also the only candidate in their window (T0 = R)
       depends on the other candidates' skies. It is reported, and it
       counts for nothing. Its weight is what G prices, under label 2.
   - **p_H ≤ 0.05.** The clues nobody fitted agree with that date. The
     held-out predicates H3 and H4 rank 1178 BC among the candidates that
     B&M's own readings accept at p_H ≤ 0.05, by an exact rank test
     (section 7).
   - **No 3a and no 3b.** Both components of the method can see (section 6).
   - **No 4.** No clean negative dates itself.

   The held-out test has a null-side floor, p_H,min: the p-value that the
   most favourable possible target would earn. It is computed with the
   target masked, before any target-side number (9.4, 12). At the design
   stage it is about 0.026 (2.9), so outcome 1 is attainable.
2. **B&M's match carries no weight.** The label takes one of two forms:
   - **No match.** No reading of 𝒢_BM* makes 1178 BC the unique survivor of
     any 136-year window containing it (r_Ody = 0) [r2 R2-3].
   - **Ordinary.** Either condition is enough:
     - B&M's own readings make a comparable target the unique match often
       (G_BM,lo ≥ 0.20 under every slot definition of 4.2);
     - at least half the random poems of the same specificity reach
       Schoch's target as well as the Odyssey does (pct_N4,lo ≥ 0.50, ties
       counted for the Odyssey).

   Label 2 judges B&M's fitted readings, and label 1 judges the clues nobody
   fitted. Both can hold at once. The verdict then says that the unfitted
   clues date the return, and that B&M's own match is not what shows it.
3. **The method cannot see**, split by component [rev #3]:
   - **3a, the eclipse component**: the method does not recover the dates of
     real eclipse records (PC-R, section 6.3).
   - **3b, the B&M-type component** (lunar phase, star season, morning star,
     Mercury turning point): the method does not recover the dates of real
     planetary and lunar records of B&M's own kinds, at observer slack
     calibrated on the *other* records (the *Almagest* control, section
     6.4).

   Every "no" about the Odyssey that depends on the failing component is
   reported as "could not have seen it".
4. **The method dates fiction.** A clean negative (fiction composed long
   after the events it tells) yields, under its own sourced readings, an
   eclipse match at least as strong as the Odyssey's (hit_j). Its
   significance must also be at least as great, even at the negative's
   least favourable bound (G_j,hi ≤ G_BM,u). That retires the method, not
   only the claim.

**Inconclusive** is reported when none of the labels applies, with every
quantity and threshold beside it. Labels 2, 3a, 3b and 4 can hold together.
Label 1 can hold with label 2, and excludes 3a, 3b and 4.

**Qualifiers** are reported whenever they hold:

| qualifier | meaning | inputs | section |
|---|---|---|---|
| Q_attain | outcome 1 could not have been reached by any target, because p_H,min > 0.05. Every "no" about the dating is then a "could not have said yes" | null-side | 7, 9.4 |
| Q_tol | B&M's own readings could not have dated any target at 5%: G_BM,lo > 0.05 under every slot definition. Printed beside the words' ceiling 1/P(A) [r2 R2-1 fix 3] | null-side | 5.3, 5.7 |
| Q_slot | a G-based decision (label 2's G leg, or Q_tol) differs between slot definitions: "slot-dependent" [r2 R2-2 fix 3] | null-side | 4.2 |
| Q_BM | B&M's own tolerances and proxies cannot recover expert planetary records | controls | 6.4 |
| Q_H | the held-out rank test does not recover real records: fewer than 6 of the 11 counted *Almagest* sets give their true date p ≤ 0.05 on their own held-out rows | controls | 6.4 |
| Q_strict | an all-clues-must-pass rule rejects the true date of most real eclipse records | controls | 6.3 |
| Q_exposure | gate 3a changes when the possibly steered control rows are re-drafted blind, or set to a sourced sibling convention | controls | 6.3.4 |
| Q_ΔT | gate 3a changes when the controls whose eclipses helped fit the ΔT models are scored without that fit | controls | 6.3.3 |

**Standing findings** are printed with every verdict and never change a
label. They are:

- the evidential ceiling of the words: 1/P(A), and the Bayes factor BF_BM
  under B&M's own encoding hypothesis (5.7);
- the T0 grid, with R, RE or NR in each cell (3.5);
- the ancient reading R_anc under its four season bounds (5.3);
- the held-out clues in detail: each predicate at the target, the sensitivity
  pools, and the uncounted H1, H2 and H5 (7);
- the *Almagest* calibrations of the Bayes factor and of the held-out test
  (5.7, 6.4).

"What, if anything, the text can date" is reported in every case, at the
level the tests support:

- a relative chronology [chron §5];
- a month-turn on Day 0 under one reading [txt §5.1];
- a season the text does not determine [txt §5.6];
- a year only if outcome 1 holds.

---

