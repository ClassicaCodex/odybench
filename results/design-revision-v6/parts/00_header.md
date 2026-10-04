# odybench — design (revision 6)

A test bench for the claim that the sky clues in the Odyssey date the
slaughter of the suitors to 16 April 1178 BC. It is the fourth in the series
after vbench (Voynich), [labench](../labench/README.md) (Linear A) and
[indusbench](../indusbench/DESIGN.md) (Indus script), and it keeps their rule:
every test is run first on cases whose answer is known, so that a "no" about
the Odyssey means something.

Revision 6, written 2026-10-04. Revisions 1–5 are kept unchanged as
`docs/DESIGN-v1.md` to `docs/DESIGN-v5.md`.

**Why a sixth revision.** The re-run of the redesign workflow ("Try again")
rechecked revision 5 [r1v5]. The recheck found 22 of the first review's 25
issues resolved, and #11, #13 and #17 not fully resolved. It raised 15 new
issues: one blocker (N1), six major (N2–N7) and eight minor (N8–N15).
Revision 6 answers all of them. Section 14 lists every issue of every review
with its resolution; 14.5 is new.

**What revision 6 changes.**

- **Gate 3a is scored against the claim, across every scoring chosen after
  the answers were read** (6.3.2) [r1v5 N1, N7].
  - Revision 5 scored the gate by best fit with 5% narrowing. That rule, the
    narrowing and the threshold of 4 were all chosen after the drafter's
    truth-side check. On the known numbers best fit passes at exactly its
    threshold, while all-must-pass, the rule the bench applies to the
    Odyssey and to fiction, fails.
  - Gate 3a now has four legs: the as-licensed primaries and a words-only
    projection, each scored all-must-pass and by best fit. The words-only
    projection drops Ptolemy's table-computed solar longitudes and widens his
    computed mid-eclipse times, as gate 3b already drops his coordinates.
    **3a fires if any leg is below 4**, and Q_score says when the legs
    disagree. Gate 3b gets the same two scorings.
  - **3a is now expected** on the known numbers (2.10).
- **Label 1 is no longer vetoed by 3a, 3b or 4** (1.3, 9.2) [r1v5 N1 fix 5].
  It rests on an exact test, whose validity needs no power calibration.
  Revision 5 already gave that reason for Q_BM and Q_H. The gates now
  qualify only the "no"s.
- **The held-out test is judged blind by substance, not by form** (7.1)
  [r1v5 N2; rev #11].
  - A frozen disclosure table pairs every target-day fact on record before
    H3 and H4 were frozen with the predicate it bears on.
  - H4's value at the target follows from B&M's published remark that Mars
    was invisible, together with V. Every pass pattern that reaches
    p ≤ 0.05 needs H4. So **the held-out test could not have said "yes" for
    this target**, and the new qualifier Q_record says so in every verdict.
  - Outcome 1 stays attainable on the null side, for data unlike the
    Odyssey's (9.5).
  - No new predicate is added. Every god-movement of the last 40 days falls
    on a day whose planets are already published or cached (7.1).
- **The held-out pools are also matched in epoch** (7.2) [r1v5 N11].
  - On the rough rows H3's pass rate differs between the two halves of the
    background (Fisher p 0.041 in P_BM, 0.013 in P_MWRA).
  - The rule now also reads each pool's members within ±700 years of the
    target, and takes the largest p of the four pools.
  - The design-stage floor rises from 0.026 to 0.040, and a target passing
    H4 alone no longer reaches 0.05.
- **Instrument checks are re-specified against their references' measured
  accuracy** (6.1, 10.4) [r1v5 N4, N6; rev #13].
  - I5(a) compares rise and set times with Horizons observer tables, not its
    rise/transit/set output.
  - The Standish code is retired as a reference: its elements were typed
    from memory, and it has no Mars. I6(b) and I15 use Horizons and an
    independent implementation on the validated ephemeris.
  - A new INSTR check, I16, is an independent evaluator of the control
    searches that produce the gate counts.
- **Outcome 4's null side is computed before the target** (6.5, 9) [r1v5
  N5]. G_j of every clean negative is a null-side quantity, frozen at the
  second freeze. Q_attain4 says when no negative could have fired outcome 4.
  Until then outcome 4 is "not ruled out", not "attainable".
- **The public tier no longer reads `data/text/`** (10.1) [r1v5 N3]. The
  Ptolemy rows state every *Almagest* date that the clue file withholds.
  Public agents now work in an exported directory. The public copy of this
  design is served before they start, and every tool call, shell included,
  is logged [r1v5 N9].
- **Smaller changes.**
  - held_ALM is at most 8 by construction, and fewer if a truth fails its
    projection [N8].
  - Held-out tolerances are leave-one-set-out ceilings, as in regime SL [N12,
    N15e].
  - B.9's phase class leaves the gate's projection [N15f].
  - The star-season component of gate 3b is recorded as untested [N13].
  - I9(b)'s per-side coverage bound is 0.975 − 3 SE [N14].
  - Site-"none" rows use a shortcut free of ΔT [N10].
  - hit_j is target-side [N15g], and three slips are corrected [N15a–c].
- **Predictions.**
  - P6, P8's second clause, P20, P22 and P23 are settled, or nearly settled,
    by known numbers. They become regression expectations.
  - P24, P25 and P27 are restated (2.7, 8) [r1v5 #17, N1, N5, N8].

**What stands.** What revisions 4 and 5 established is kept:

- the two-stage freeze;
- the exact held-out rank test as the only route to "yes";
- label 2 with its "no match" form;
- the frozen slot family;
- the *Almagest* gate of B&M's own clue types, with leave-one-set-out
  tolerances;
- Appendix T and the reading tiers;
- the storm rule;
- the conditioning of every reading formed with the target in view.

Their summaries are in `docs/DESIGN-v4.md` and `docs/DESIGN-v5.md`.

**Status.**
- **Built and validated:** `odybench/ephem.py`, `odybench/ccx.py`,
  `odybench/calendar.py` and the data in section 2.1.
- **Drafted and licence-checked, not frozen:**
  `data/prereg/controls_real.json` (one check), `controls_almagest.json`
  (two checks) and `negatives.json` (two checks). Their hashes are unchanged
  since revision 5 (12.4).
- **Not yet built:** any other bench code.
- **Not yet run:** any null model, control search or held-out check.
- **Computed for revisions 4–6:** design-stage estimates of null-side
  quantities only. The target was removed before any computation (2.9).
- **Freezing:** everything in sections 3–9 is frozen in a local git commit
  before any of them runs (section 12).

Section 2 lists what is already known, including what the known numbers imply
for the verdict. Section 8 lists, with thresholds, only what needs new runs.

