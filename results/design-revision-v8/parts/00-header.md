Revision 8, written 2026-10-04. Revisions 1–7 are kept unchanged as
`docs/DESIGN-v1.md` to `docs/DESIGN-v7.md`.

**Why an eighth revision.** The final adversarial review of the loop
rechecked revision 7 [r3v7]. It found no blocker. All 25 issues of the first
review and all ten of the recheck of revision 6 stay resolved in their own
terms. One old issue was still not resolved in substance: #71, whether
outcome 4 can fire at all. It raised 11 new issues: three major (R3-1 to
R3-3) and eight minor (R3-4 to R3-11), which section 14 numbers 92–102.
Revision 8 answers all of them, and #71 through R3-2. Section 14 lists every
issue of every review with its resolution; 14.7 is new.

**What revision 8 changes.**

- **Gate 3b's projection reads words only** (6.4) [r3v7 R3-1].
  - A.2, A.5 and B.2 join A.10, B.5 and B.9 at "none". Their phase classes
    are the drafter's inferences from planet–Moon positions and, for A.5,
    from Mars' opposition. The gate holds those relations out, and the clue
    file's own "none" option says that the phase is not stated in words.
    Only B.7, "about a quadrant", keeps its phase class.
  - Setting rows to "none" only loosens them, so no truth is lost. But
    narrowing gets harder. On the recheck's estimate ALM-A now passes about
    4.9% of a window's days, where revision 7's projection passed 0.6%. So
    gate 3b's expected pass rests on two knife-edges, ALM-A and ALM-B (about
    4.4%), and P21 is open again [R3-4].
  - Revision 7's projection, with the inferred phases, is reported as a
    sensitivity.
- **Q_attain4 reads the windows where label 4 is scored** (6.5) [r3v7 R3-2].
  - Its eclipse condition is now hit_j(m̂). Some eclipse-compatible reading
    must make an eclipse of the Odyssey's strength the unique survivor in one
    of the Odyssey's two windows. It is computed on the null side, with m̂
    standing in for M_Ody.
  - Revision 7's E_j counted such eclipses anywhere in the core, where label
    4 can never score them. It is now reported as context.
  - The G condition allows at most 4 targets reached at reach 1: a garden at
    least about four times more selective than 𝒢_BM*. Revision 7's "about 11
    reach-units" was the bound itself. P25 no longer predicts that outcome 4
    is attainable.
  - m̂ = 0.304 lies below the exact M_Ody, so Q_attain4 can err only towards
    silence. It is never printed beside a label 4.
- **I2(c) can be met by a correct implementation** (2.3, 6.1, 10.2)
  [r3v7 R3-3]. The 2.3 table now integrates the continuous totality
  windows. There the SMH2016 parabola gives 0.503 and the mixture 0.308,
  where the 5-s-grid windows gave 0.498 and 0.304. The sub-step synthetic
  cases are measured, not passed, and the other synthetic cases are bisected
  to 0.01 s.
- **Smaller changes.**
  - P21 is open again, on two knife-edges [R3-4].
  - `same_apparition` tests visibility on the row's own day, not on Day 0.
    `visible_before_sunrise` has one instant rule in 6.4 and 10.3: the
    stated hour, else the Sun at −8° [R3-5].
  - I16 resolves a site-search miss to the witnessed value, and a miss by
    the reference never fails INSTR [R3-6].
  - The null windows of `narrowable` and I16(a) lie inside −1000..+300, each
    with its linked events inside the data [R3-7].
  - Q_attain3a and Q_attain3b are printed only beside a gate that fires
    [R3-8].
  - The sealed list leaves out D4, which this design must print, and says
    why that does not matter [R3-9].
  - Q_score is split into Q_score3a and Q_score3b [R3-10].
  - Slips are corrected [R3-11].

**What stands.** What revisions 4–7 established is kept:

- the two-stage freeze;
- the exact held-out rank test, on four pools, as the only route to "yes";
- no gate vetoes label 1, and the disclosure table with Q_record says that,
  for this target, the held-out test could not have said "yes";
- label 2 with its "no match" form;
- the frozen slot family;
- gate 3a's four legs (as licensed and words only, strict and best fit);
- the *Almagest* gate of B&M's own clue types, with leave-one-set-out
  tolerances, the frozen meaning of `same_apparition` and the rounding
  family of the ceilings;
- narrowability as a null-side quantity, with each gate's per-set
  breakdown;
- the independent evaluator of the control searches (I16);
- the exact mixture integral, `deltat_mix.p_exact`;
- G_j on the null side, and outcome 4 against the Odyssey's lower bound;
- Q_exch beside label 1;
- Appendix T and the reading tiers;
- the storm rule;
- the conditioning of every reading formed with the target in view.

The summaries of revisions 4–7 are in `docs/DESIGN-v4.md` to
`docs/DESIGN-v7.md`.

**Status.**
- **Built and validated:** `odybench/ephem.py`, `odybench/ccx.py`,
  `odybench/calendar.py` and the data in section 2.1.
- **Drafted and licence-checked, not frozen:**
  `data/prereg/controls_real.json` (one check), `controls_almagest.json`
  (two checks) and `negatives.json` (two checks). Their hashes are unchanged
  since revision 5 (12.4).
- **Not yet built:** any other bench code.
- **Not yet run:** any null model, control search or held-out check.
- **Computed for revisions 4–8:** design-stage estimates of null-side
  quantities, with the target removed before any computation (2.9).
  - Revision 6 derived the held-out tolerance ceilings by arithmetic on the
    drafter's existing slack table. That is a truth-side step, recorded in
    Appendix T (T2b).
  - Revision 7 added two things. One is a design-stage estimate of the two
    inputs of Q_exch (2.9), on the same rough rows with the target removed
    first. The other is the same arithmetic at the three rounding steps of
    6.4 (T2b).
  - Revision 8 evaluated no sky. It integrated the four ΔT models over the
    continuous totality windows that the recheck had bisected (2.3). It took
    the narrowing of the words-only projection from the recheck's recorded
    runs (2.6). And it redid the arithmetic of outcome 4's bound (2.10, 6.5).
  - Nobody has computed a held-out predicate at the target.
