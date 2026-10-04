**Status.**
- **Built and validated:** `odybench/ephem.py`, `odybench/ccx.py`,
  `odybench/calendar.py` and the data in section 2.1.
- **Drafted and licence-checked, not frozen:**
  `data/prereg/controls_real.json` (one check), `controls_almagest.json`
  (two checks) and `negatives.json` (two checks). Their hashes are unchanged
  since revision 5 (12.4).
- **Not yet built:** any other bench code.
- **Not yet run:** any null model, control search or held-out check.
- **Computed for revisions 4–7:** design-stage estimates of null-side
  quantities, with the target removed before any computation (2.9).
  - Revision 6 derived the held-out tolerance ceilings by arithmetic on the
    drafter's existing slack table. That is a truth-side step, recorded in
    Appendix T (T2b).
  - Revision 7 added two things. One is a design-stage estimate of the two
    inputs of Q_exch (2.9), on the same rough rows with the target removed
    first. The other is the same arithmetic at the three rounding steps of
    6.4 (T2b).
  - Nobody has computed a held-out predicate at the target.
- **Freezing:** everything in sections 3–9 is frozen in a local git commit
  before any of them runs (section 12).

