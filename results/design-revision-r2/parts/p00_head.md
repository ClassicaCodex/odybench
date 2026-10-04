# odybench — design (revision 3)

A test bench for the claim that the sky clues in the Odyssey date the
slaughter of the suitors to 16 April 1178 BC. It is the fourth in the series
after vbench (Voynich), [labench](../labench/README.md) (Linear A) and
[indusbench](../indusbench/DESIGN.md) (Indus script), and it keeps their rule:
every test is run first on cases whose answer is known, so that a "no" about
the Odyssey means something.

Revision 3, written 2026-10-04. Revision 1 (2026-10-03) is kept unchanged as
`docs/DESIGN-v1.md` and revision 2 (earlier on 2026-10-04) as
`docs/DESIGN-v2.md`. Two adversarial reviews shaped it:

- `docs/critique-design.md` reviewed revision 1: 25 issues, 3 of them
  blockers.
- `docs/critique-design-r1.md` rechecked revision 2. It found 20 of those 25
  resolved and raised 17 new issues, N1–N17, one of them a blocker: the
  likelihood ratio that outcome 1 needed could never exceed about 6.5, so the
  bench could never say "yes".

Revision 3 answers both. Its main changes are these:

- **No likelihood ratio enters the decision rule.** The ceiling the recheck
  found is a true property of the text's words, and it is now reported as a
  finding (section 5.7).
- **Every clue reading formed with the target in view is treated alike.** G
  is taken over targets that satisfy the season, Venus and Mercury readings,
  the equinox clue is left out of every garden the rule reads, and T0 must
  reproduce without it (section 5.3).
- **The background runs to AD 200,** so that the conditioned target pool is
  large enough for outcome 1's interval to be attainable (section 4.1).
- **The *Almagest* gate is calibrated leave-one-set-out,** and B&M's own
  option rule is named, so gate 3b can fire and Q_BM is defined (section 6.4).
- **Solar-eclipse controls are scored under the ΔT mixture,** and the controls
  that helped fit a ΔT model are reported apart (section 6.3).
- **Every synthetic input set is checked against the rule's structural
  constraints,** so that the reachability test proves outcomes, not branches
  (section 9).

Section 14 lists all 42 issues with their resolutions.

**Status.** Built and validated: `odybench/ephem.py`, `odybench/ccx.py`,
`odybench/calendar.py` and the data in section 2.1. Drafted and
licence-checked, not frozen: `data/prereg/controls_real.json`,
`controls_almagest.json` and `negatives.json`. No other bench code exists. No
null model, control search or held-out check has been run. Everything in
sections 3–9 is frozen in a local git commit before any of them runs
(section 12). Section 2 lists what is already known, including what the
known numbers already imply for the verdict. Section 8 lists, with
thresholds, only what needs new runs.

---

