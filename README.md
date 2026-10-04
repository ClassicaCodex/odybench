# odybench

A test bench for the claim of Baikouzis & Magnasco (PNAS 105, 2008,
8823–8828) that four sky references in the *Odyssey* (the new moon, the
Pleiades and Boötes, Venus as the morning star, and Hermes read as Mercury)
date the slaughter of the suitors to 16 April 1178 BC, the day of a total
solar eclipse that Schoch (1926) had linked to Theoclymenus' vision, "the sun
has perished out of heaven" (*Od.* 20.356–357).

It is the fourth bench in a series, after vbench (Voynich), labench
(Linear A) and indusbench (Indus script). Each one keeps the same rule: every
test runs first on cases whose answer is known, so that a "no" about the
*Odyssey* means something.

## Status

**Design stage. No analysis has been run.**

- [`DESIGN.md`](DESIGN.md) is the plan, now at revision 8. It went through four
  adversarial reviews (`docs/critique-design*.md`), and the last of them
  found no blocking issue. Section 2 lists the numbers that were already
  known before the bench existed, so that nothing later pretends to predict
  them.
- `docs/research-*.md` is the research dossier: the paper read twice
  independently and reconciled, its critiques, the poem's day count, every
  sky clue in the Greek, the ephemeris stack, visibility thresholds, the
  controls, and the date window.
- `data/prereg/` holds the clue sets for the controls. They were drafted
  from the ancient texts alone and checked for licence word by word. The
  accepted dates are kept apart, in `*_truth.json`, which the searcher never
  reads.
- Built and validated: `odybench/ephem.py` (JPL DE441/DE431, ΔT models,
  eclipses) and `odybench/calendar.py` (exact proleptic Julian). The rest of
  the code is being built to section 10 of the design.

Results will be computed only after the two-stage freeze of DESIGN section 12
has committed the design, the thresholds and the code. The null side is run
first, with the target date masked.

## Not in this repository

Ephemerides, NASA eclipse elements, texts exported from the ClassicaCodex
library, and copies of publications are hashed in `data/SHA256SUMS` but not
published. `tools/fetch_*.py` rebuild the public data.
