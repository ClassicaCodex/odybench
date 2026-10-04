**The gate** [r1v5 N1; r2v6 N1, N6].

- **The legs.** seen_ALM_SL[leg] is the number of the 11 counted sets seen
  in regime SL under the frozen meaning of `same_apparition`. There are six
  legs: best fit (`bf`) and strict (`st`), each at the fine, mid and coarse
  rounding steps of the ceilings. Every leg uses the 5% narrowing of 6.3.2.
- **3b fires if any leg is below 6** (fewer than half of 11, rounded up).
- **The other meaning of `same_apparition`.** seen_ALM_SL_side[leg] is the
  same count with the option read as "on that side of the Sun" only. It
  enters no label. **Q_score holds** if gate 3b's decision under it differs
  from the decision under the frozen meaning, or if the six legs fall on
  both sides of 6.
- In a window of some 50,000 candidate days S₀ is rarely empty, and when it
  is not, B = S₀. So the two scorings are expected to agree, and on the
  known numbers the three steps too [AppT 2]. Taking every leg costs little,
  and it applies one family to both gates.
- **Which sets can be narrowed: gate 3b's attainability** [r2v6 N1 fixes
  2–3]. narrowable[3b][leg][set] and N_narrow[3b][leg] are defined as for
  gate 3a (6.3.2): on the 21 null windows of I16(a), at the null-side stage,
  frozen at the second freeze.
  - **Q_attain3b holds if N_narrow[3b][leg] < 6 on some leg.** Label 3b is
    then printed as "untested by these controls".
  - On the recheck's rough estimate (2.6), ALM-I, J and K cannot be narrowed
    on any leg. ALM-B can under the frozen meaning (4.4% of days) and cannot
    under the other (5.2%). The other seven can. So N_narrow is about 8,
    Q_attain3b is not expected (R28), and gate 3b needs at least 6 of those
    8.
  - The per-set breakdown of 6.3.2, and the count seen among the narrowable
    sets, are printed beside gate 3b too.
- **Why the composition is not changed** [r2v6 N1 fix 5]. The recheck offered
  the option of recomposing gate 3b from the sets that can be narrowed. Two
  counted sets lose their truth in regime SL, and that was known when this
  revision was written [AppT 2]. Recomposing now would lower the threshold
  from 6 of 11 to 4 of 8 with those failures in view, which favours "the
  method can see". So the rule keeps the frozen gate. The recomposed count,
  the sets seen among the narrowable ones, is printed beside it.
- **What the 5% line decides here.** For gate 3a the family of legs protects
  the 5% line: the legs disagree on the known numbers, and a pass needs
  every leg. Gate 3b's legs are expected to agree, so the family protects
  nothing there, and the 5% line decides ALM-B.
  - The line was frozen in revision 2, after the drafter's slack table
    existed, and before anyone had estimated ALM-B's narrowing; the recheck
    of revision 6 did that first.
  - Q_score, through the other meaning, and the per-set breakdown disclose
    it. The gate is also reported with the line at 4% and at 6%.
- **Regime BM.** rec_ALM_BM is the number of sets with strict recall and
  \|S₀\| ≤ 0.05 N_cand in regime BM (projection, strict). Its tolerances are
  B&M's, not ceilings, so it has no rounding step.
- **Q_BM holds if rec_ALM_BM < 6**: "B&M's tolerances cannot recover expert
  planetary records" [rev #3 fix 3].
  - It conditions every "no" that rests on B&M's tolerances: label 2's G
    leg, Q_tol and pct_N4.
  - It never blocked outcome 1 after revision 3. Revision 6 removed the last
    gate vetoes too (1.3).
- PC-S no longer enters the gate [r1 N2 fix 3].

