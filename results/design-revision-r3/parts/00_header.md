# odybench — design (revision 4)

A test bench for the claim that the sky clues in the Odyssey date the
slaughter of the suitors to 16 April 1178 BC. It is the fourth in the series
after vbench (Voynich), [labench](../labench/README.md) (Linear A) and
[indusbench](../indusbench/DESIGN.md) (Indus script), and it keeps their rule:
every test is run first on cases whose answer is known, so that a "no" about
the Odyssey means something.

Revision 4, written 2026-10-04. Revisions 1–3 are kept unchanged as
`docs/DESIGN-v1.md`, `docs/DESIGN-v2.md` and `docs/DESIGN-v3.md`. Three
adversarial reviews shaped it:

- `docs/critique-design.md` reviewed revision 1: 25 issues, 3 of them
  blockers.
- `docs/critique-design-r1.md` rechecked revision 2: 17 new issues, N1–N17,
  one of them a blocker.
- `docs/critique-design-r2.md` rechecked revision 3. It found 22 of the first
  25 issues and 16 of N1–N17 resolved, and raised 12 new issues, R2-1 to
  R2-12. One is a blocker: outcome 1 could not be reached for any data.
  Outcome 1 needed G_BM, the chance that B&M's own readings make a
  comparable target the unique match, to lie below 0.05. That chance is set
  by the sky alone, before any measurement of the Odyssey, and the recheck
  estimates it at about 0.14.

Revision 4 answers all three. Its main changes are these:

- **"Yes" now rests on evidence formed blind to the target.** Outcome 1 reads
  the held-out clues of section 7: Hermes leading the suitors' souls, and
  Ares caught with Aphrodite. They are scored by an exact rank test against
  the candidates that B&M's own readings accept. Whether that test could
  give p ≤ 0.05 is a null-side number. It is computed before any target-side
  number, and at the design stage it is about 0.026 (2.9).
- **B&M's own match is judged separately.** Label 2 says when it carries no
  weight. The qualifier Q_tol says in every verdict when B&M's readings could
  not have dated any target at 5% (2.10). That is expected, since G_BM is
  about 0.14.
- **The freeze has two stages.** Code, design and thresholds are committed
  before any null, control or held-out result. The null-side quantities (pool
  sizes, G, the held-out null) are then computed with the target masked, and
  committed before any target-side number (12).
- **The slots that define the conditioned pool form a frozen family** of six
  definitions. A G-based decision fires only if it fires under all six (4.2,
  9).
- **Smaller changes:**
  - label 2 has a "no match" form, and ties never decide it (5.4);
  - INSTR holds only the checks that guard rule inputs, each with a tie band
    (6.1);
  - `smag` is NASA's magnitude exactly (0);
  - leave-one-set-out tolerances are ceilings of the measured slack, not
    values from the drafter's grid (6.4);
  - sibling-convention transplants are restricted (6.3.4);
  - R_anc's four season bounds are reported alike (5.3);
  - a reading whose eclipse is not on Day 0 is mapped to its eclipse (6.5);
  - G's interval allows for clustered targets (5.3).

Section 14 lists all 54 issues of the three reviews with their resolutions.

**Status.**
- **Built and validated:** `odybench/ephem.py`, `odybench/ccx.py`,
  `odybench/calendar.py` and the data in section 2.1.
- **Drafted and licence-checked, not frozen:**
  `data/prereg/controls_real.json`, `controls_almagest.json` and
  `negatives.json`.
- **Not yet built:** any other bench code.
- **Not yet run:** any null model, control search or held-out check.
- **Computed for this revision:** design-stage estimates of null-side
  quantities only. The target was removed before any computation (2.9).
- **Freezing:** everything in sections 3–9 is frozen in a local git commit
  before any of them runs (section 12).

Section 2 lists what is already known, including what the known numbers imply
for the verdict. Section 8 lists, with thresholds, only what needs new runs.

---

