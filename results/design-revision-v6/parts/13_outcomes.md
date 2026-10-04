### 1.3 Outcomes

The verdict is a set of labels computed mechanically by `verdict.py` from
named quantities (section 9). Every condition names its garden and its target
pool. It also says what kind of input it reads (9.1):

- **null-side:** fixed by the sky and the readings, with the target masked;
- **target-side:** it reads 16 Apr 1178 BC;
- **control:** it reads a control's truth, and not the target.

Every interval is taken against the claim being made.

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

1. **The text dates the return.** Both must hold:
   - **T0_pass.** B&M's applied criteria (N, C, V and M, without the equinox
     clue) pass for 16 Apr 1178 BC with a modern ephemeris (3.5).
     - This is the part of B&M's reproduction that depends on the target's
       own sky.
     - Whether 1178 BC is also the only candidate in their window (T0 = R)
       depends on the other candidates' skies. It is reported, and it
       counts for nothing. Its weight is what G prices, under label 2.
   - **p_H ≤ 0.05.** The clues nobody fitted agree with that date.
     - The held-out predicates H3 and H4 rank 1178 BC by an exact rank test
       in each of four null pools (section 7).
     - The pools are the candidates that B&M's own readings accept (P_BM),
       those that pass the Mercury event B&M applied (P_MWRA), and the
       members of each within ±700 years of the target (P_BM,E and
       P_MWRA,E).
     - p_H is the largest of the four p-values.

   **No gate vetoes label 1** [r1v5 N1 fix 5]. The test is exact: under H0 it
   says "yes" with probability at most 5%, whatever the method's power.
   - The gates 3a and 3b, and the qualifiers Q_BM and Q_H, measure power.
     They decide what a "no" means, not whether a "yes" is valid.
   - Revision 5 already gave that reason for Q_BM and Q_H, and yet still
     vetoed label 1 by 3a and 3b.
   - Label 4 concerns the eclipse match, which the held-out test does not
     use.

   Every other label that holds is printed beside label 1 (9.3).

   **The held-out test's floor** is p_H,min: the p-value that the most
   favourable possible target would earn, the largest of the four pools'
   floors.
   - It is computed with the target masked, before any target-side number
     (9.4, 12).
   - At the design stage it is about 0.040 (2.9), so outcome 1 is attainable
     **for some target**.
   - **For this target it is not.** Facts on record before H3 and H4 were
     frozen settle H4, and every pass pattern below 0.05 needs H4 (7.1).
     Q_record says so in every verdict.
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
   - **3a, the eclipse component.** The method does not recover the dates of
     real eclipse records (PC-R, section 6.3).
     - It is scored on four legs: the as-licensed primaries and a
       words-only projection, each scored all-must-pass and by best fit.
     - 3a holds if **any** leg counts fewer than 4 of the 7 counted sets
       seen (6.3.2) [r1v5 N1, N7].
   - **3b, the B&M-type component** (lunar phase, morning star and Mercury
     turning point). The method does not recover the dates of real
     planetary and lunar records of B&M's own kinds, at observer slack
     calibrated on the *other* records (the *Almagest* control, section
     6.4).
     - It is scored all-must-pass and by best fit, and holds if either
       counts fewer than 6 of the 11 counted sets.
     - B&M's fourth kind, the star season, has no dated real record, so that
       component is **untested** [r1v5 N13; rev #3 fix 4].

   Every "no" about the Odyssey that depends on the failing component is
   reported as "could not have seen it".
4. **The method dates fiction.** The eclipse-matching method, applied to a
   clean negative (fiction composed long after the events it tells), yields
   under the negative's own sourced readings an eclipse match at least as
   strong as the Odyssey's (hit_j). Its significance must also be at least
   as great, even at the negative's least favourable bound
   (G_j,hi ≤ G_BM,u). That retires the eclipse-matching method, not only the
   claim. Whether any clean negative *could* meet that bound is a null-side
   question, settled before the target is looked at (Q_attain4, 6.5).

**Inconclusive** is reported when none of the labels applies, with every
quantity and threshold beside it. Labels 1, 2, 3a, 3b and 4 can hold
together in any combination; the two forms of label 2 exclude each other.

**Qualifiers** are reported whenever they hold:

| qualifier | meaning | inputs | section |
|---|---|---|---|
| Q_attain | outcome 1 could not have been reached by any target, because p_H,min > 0.05 (the largest of the four pools' floors). Every "no" about the dating is then a "could not have said yes" | null-side | 7, 9.4 |
| Q_record | the held-out test could not have said "yes" for **this** target, given facts on record before H3 and H4 were frozen: every pass pattern with p_H ≤ 0.05 needs a predicate that the frozen disclosure table records as failing at the target [r1v5 N2] | null-side and the frozen table | 7.1, 7.2 |
| Q_contra | a measured held-out flag of the target contradicts a value the disclosure table records as determined. The record, the inference from it, or the bench is wrong | target-side | 7.1 |
| Q_tol | B&M's own readings could not have dated any target at 5%: G_BM,lo > 0.05 under every slot definition. Printed beside the words' ceiling 1/P(A) [r2 R2-1 fix 3] | null-side | 5.3, 5.7 |
| Q_slot | a G-based decision (label 2's G leg, or Q_tol) differs between slot definitions: "slot-dependent" [r2 R2-2 fix 3] | null-side | 4.2 |
| Q_attain4 | outcome 4 could not have fired: no clean negative has 0 < G_j and G_j,hi ≤ G_BM,u. "No label 4" then means nothing [r1v5 N5] | null-side | 6.5, 9.4 |
| Q_BM | B&M's own tolerances and proxies cannot recover expert planetary records | controls | 6.4 |
| Q_H | the held-out rank test does not recover real records: fewer than 6 of the 11 counted *Almagest* sets give their true date p ≤ 0.05 on their own held-out rows. At most 8 sets can, because three have no held-out row, and fewer if a truth fails its projection (6.4) [r1v5 N8] | controls | 6.4 |
| Q_score | the legs of gate 3a, or of gate 3b, fall on both sides of the gate's threshold: the gate's decision rests on the scoring rule. It replaces revision 5's Q_strict [r1v5 N1] | controls | 6.3.2, 6.4 |
| Q_exposure | gate 3a's combined decision changes when the possibly steered control rows are re-drafted blind, or set to a sourced sibling convention | controls | 6.3.4 |
| Q_ΔT | gate 3a's combined decision changes when the controls whose eclipses helped fit the ΔT models are scored without that fit | controls | 6.3.3 |

**Standing findings** are printed with every verdict and never change a
label. They are:

- the evidential ceiling of the words: 1/P(A), and the Bayes factor BF_BM
  under B&M's own encoding hypothesis (5.7);
- the T0 grid, with R, RE or NR in each cell (3.5);
- the ancient reading R_anc under its four season bounds (5.3);
- the held-out clues in detail (7):
  - each predicate at the target;
  - the disclosure table and what it settles;
  - the sensitivity pools;
  - the stationarity table (R21);
  - the uncounted H1, H2 and H5;
- the *Almagest* calibrations of the Bayes factor and of the held-out test
  (5.7, 6.4);
- the legs of both gates, and the star-season component that gate 3b does
  not test (6.3.2, 6.4).

"What, if anything, the text can date" is reported in every case, at the
level the tests support:

- a relative chronology [chron §5];
- a month-turn on Day 0 under one reading [txt §5.1];
- a season the text does not determine [txt §5.6];
- a year only if outcome 1 holds.

