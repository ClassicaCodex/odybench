- **The gates' thresholds** (4 of 7 and 6 of 11) and the 5% narrowing were
  set in revision 2, after the drafter's truth-side check (2.6). They are
  kept. For gate 3a the family of legs means that they cannot be what makes
  the gate pass, because the legs disagree on the known numbers and a pass
  needs every one. **For gate 3b they can** [r2v6 N1]. Its legs are expected
  to agree, so the family protects nothing, and the 5% line decides ALM-B
  under the frozen meaning of `same_apparition` (6.4). Revision 6 said the
  family covered both gates, which was wrong. What discloses it instead:
  - Q_score prints when gate 3b's decision changes under the other meaning
    of `same_apparition`;
  - the per-set breakdown shows which sets can be narrowed, which keep their
    truth, and which are seen;
  - Q_attain3b prints when too few sets can be narrowed for the gate to
    pass;
  - the gate is also reported with the line at 4% and at 6%.
- **How a gate label is printed** [r2v6 N1]. A firing gate is printed as
  "the eclipse (or B&M-type) component is not shown to recover real
  records", with its per-set breakdown. With Q_attain3a (or Q_attain3b) it
  is printed as "untested by these controls: too few counted sets can be
  narrowed". Either way, every "no" that depends on that component is
  "could not have seen it".
