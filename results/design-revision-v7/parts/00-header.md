# odybench — design (revision 7)

A test bench for the claim that the sky clues in the Odyssey date the
slaughter of the suitors to 16 April 1178 BC. It is the fourth in the series
after vbench (Voynich), [labench](../labench/README.md) (Linear A) and
[indusbench](../indusbench/DESIGN.md) (Indus script), and it keeps their rule:
every test is run first on cases whose answer is known, so that a "no" about
the Odyssey means something.

Revision 7, written 2026-10-04. Revisions 1–6 are kept unchanged as
`docs/DESIGN-v1.md` to `docs/DESIGN-v6.md`.

**Why a seventh revision.** The re-run of the review loop rechecked revision 6
[r2v6]. It found all 25 issues of the first review resolved in their own
terms, and 14 of the 15 issues of the recheck of revision 5. One was not
resolved in substance: #71, whether outcome 4 can fire at all. It raised 10
new issues: one blocker (N1), two major (N2, N3) and seven minor (N4–N10).
Revision 7 answers all of them. Section 14 lists every issue of every review
with its resolution; 14.6 is new.

**What revision 7 changes.**

- **Gate 3b now measures the method, and says when it cannot** (6.4, 9)
  [r2v6 N1].
  - **The meaning of `same_apparition` is frozen** (10.3). Revision 6 never
    fixed it, and on the recheck's estimate that one option decided whether
    ALM-B narrows its window to 5%, and so decided the gate.
    - The body must be visible on the record's day, as every row that carries
      the option records a sighting.
    - The greatest elongation must lie on the record's stated side of it,
      between the two conjunctions that bracket the record.
    - The other reading, side of the Sun only, is scored on every leg and
      reported. Q_score now also prints when that reading would change the
      gate's decision.
  - **Whether a set can be narrowed at all is computed on the null side.**
    Three counted sets, ALM-I, J and K, carry too little B&M-type information
    to narrow any window to 5%.
    - `narrowable` is now a null-side quantity for every counted set and leg
      of both gates, frozen at the second freeze.
    - New qualifiers, Q_attain3a and Q_attain3b, say when too few sets can be
      narrowed for a gate to pass. The label is then printed as "untested by
      these controls", not as "cannot see".
  - **Each gate prints a per-set breakdown**: can the set be narrowed, is its
    truth kept, is it seen? This replaces revision 6's static sentence about
    a perfect implementation.
  - **The gates' composition and thresholds are unchanged.** Changing them
    now would lower 3b's threshold with two sets' truth-side failures in view.
    The count of sets seen among those that can be narrowed is printed beside
    each gate.
  - **Restated:** 2.6, 2.10, P21, P27 and the expected-verdict sets S0x and
    S0y. On known numbers at most 8 counted sets can be narrowed, so gate 3b
    needs at least 6 of those 8 seen.
- **Every leave-one-set-out ceiling is taken across its rounding step** (6.4)
  [r2v6 N6]. Revisions 4 and 6 chose their rounding steps with the slack
  table in view, and a step can decide a held-out row at its truth.
  - Q_H and gate 3b now take their decisions against the claim across three
    steps: 0.01°, 0.05° and 0.1°, or 0.1 d, 0.5 d and 1 d.
- **Instrument checks that could not be met are re-specified** [r2v6 N2–N4].
  - `deltat_mix` gains an exact interval integrator. The control rows' P_mix
    and I2(c) use it, and the 41-point grid leaves the rule inputs.
  - I16's reference is vectorised and decides a site-free row by early exit
    on the eclipse's own geometry. It reads `data/jsex/`, and its cost is
    budgeted (11.2).
    - Linked events get a deterministic tie-break.
    - Site searches are compared through witness sites.
  - I15(b)'s Horizons tables are fetched at the null-side stage, by frozen
    code, into `results/attain/`, which the second freeze commits.
- **Outcome 4 is taken against the claim on both sides** (6.5).
  - It compares the negative's upper bound with the Odyssey's lower bound,
    G_BM,u,lo [r2v6 N8].
  - Q_attain4 now also needs a negative whose eclipse-compatible readings can
    make an eclipse of the Odyssey's strength unique [r2v6 #71].
- **Label 1 gains a qualifier, Q_exch** (7.2) [r2v6 N9]. It prints when the
  exchangeability that the exact test rests on is in doubt: P10's held-out
  part fails, or H3 or H4 drifts inside the epoch band. The design-stage
  estimate, with the target masked, finds neither.
- **Smaller changes.**
  - The re-draft brief is built from six PC-R text rows added to the public
    export [N5].
  - Every value the disclosure table marks "constrains" is sealed from every
    agent's direct reads until the second freeze, and the table's post-freeze
    facts are marked as corroboration, not record [N7].
  - The words-only projection states which option PB-E2-TIME keeps. It names
    A-MONTH as its one exception, and reports it at "none" [N10a, b].
  - The justification of the ±700-year band is corrected [N10c], and CP_hi is
    removed [N10d].

**What stands.** What revisions 4–6 established is kept:

- the two-stage freeze;
- the exact held-out rank test, on four pools, as the only route to "yes";
- no gate vetoes label 1, and the disclosure table with Q_record says that,
  for this target, the held-out test could not have said "yes";
- label 2 with its "no match" form;
- the frozen slot family;
- gate 3a's four legs (as licensed and words only, strict and best fit);
- the *Almagest* gate of B&M's own clue types, with leave-one-set-out
  tolerances;
- the independent evaluator of the control searches (I16);
- G_j on the null side;
- Appendix T and the reading tiers;
- the storm rule;
- the conditioning of every reading formed with the target in view.

The summaries of revisions 4–6 are in `docs/DESIGN-v4.md` to
`docs/DESIGN-v6.md`.

