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

## Result (the lean run, 2026-10-09)

**The Odyssey's sky clues do not date Odysseus' return.** The full verdict,
with every number beside its threshold, is in
[`results/VERDICT.md`](results/VERDICT.md). The run followed
[`LEAN.md`](LEAN.md), an amendment to the design pushed before any analysis.
The code was frozen and pushed as `prereg-1`, and the null side was computed
with 16 April 1178 BC hidden and pushed as `prereg-2`, before the target was
looked at.

1. **The match reproduces but is not unique.** With JPL's DE441, 16 April
   1178 BC passes the four criteria B&M applied (new moon, the Pleiades and
   Boötes season, Venus rising at least 90 minutes before the Sun, Mercury
   near its rise-azimuth maximum), and so does **18 March 1189 BC**.
   - 1178 BC is unique only when B&M's fifth, unapplied clue, the equinox, is
     added with its bound at 5 or 6 April.
   - At 4 April, the bound B&M's own probability paragraph states, 1178 BC
     fails that clue.
   - Under a physical model of Mercury's visibility (B&M's text requires
     Mercury to be visible), 1178 BC fails by 0.11° and 1189 BC passes.
2. **The odds were overstated.**
   - B&M's applied criteria pass by chance about **0.50 times per century**
     [95%: 0.25–0.89]. Their "one day in 2,000 years" (0.048 per century)
     needs the unapplied equinox clue.
   - About **62%** of 136-year windows, the size of theirs, hold at least one
     chance match.
3. **The coincidence with the eclipse is not significant.** B&M's own 36
   readings of their clues would make a comparable spring new moon, fixed in
   advance, the "unique" match with probability **G_BM = 0.15** [0.09–0.22]
   (slot v1; 0.15–0.35 across the six slot definitions). Under every slot,
   the lower bound exceeds 0.05: B&M's tolerances could not have made any
   match notable (Q_tol).
4. **The clues B&M did not fit fail.** Ares caught with Aphrodite (Day −7)
   needs Venus and Mars within 5°; on B&M's date they were never closer than
   **21.7°**. Hermes leading the souls (Day 0) needs Mercury passing the Sun
   within three days; it was not. The exact rank test on four null pools
   gives **p = 1**.
5. **The eclipse was probably not total at Ithaca.** P(total) is **0.31**
   under the mixture of four ΔT models, though P(magnitude ≥ 0.9) is 0.93.
   The eclipse of 30 September 1131 BC, inside B&M's own window, was total at
   Ithaca with probability 0.50.
6. **B&M's tolerances miss real observers.** Ptolemy's dated planetary
   records in the *Almagest* are recovered by a B&M-style search in only
   **3 of 11** sets at B&M's tolerances (Q_BM). With observer slack
   calibrated on the other sets, 6 of 11 are recovered, exactly the gate's
   threshold, and 5 under the other meaning of one frozen definition.

**Labels:** the restricted rule returns **inconclusive** with qualifiers
Q_record, Q_tol, Q_slot and Q_BM. Label 2 ("the match carries no weight")
needs G_BM's lower bound at 0.20 or more under all six slot variants, and
it is reached only under v5. The held-out test could not have said "yes" for
this target, given facts published before the bench existed (Q_record), and
it did not. Gate 3a, label 4 (fiction) and the random-epic leg were deferred
by the lean run and are not tested.

## The repository

- [`DESIGN.md`](DESIGN.md) is the full plan (revision 8, after four
  adversarial reviews in `docs/critique-design*.md`).
  [`LEAN.md`](LEAN.md) is the part that was run.
- `docs/research-*.md` is the research dossier.
- `data/prereg/` holds the control clue sets, drafted from the ancient texts
  alone, with their accepted dates kept apart in `*_truth.json`.
- `odybench/` is the code: `ephem.py` and `calendar.py`, validated, and the
  lean run in `odybench/lean/`. The top-level scripts are `attain.py`,
  `reproduce.py`, `heldout.py`, `deltat.py`, `almagest.py` and `verdict.py`.
  `tools/run_instruments.py` runs every check.
- `results/` holds the outputs: `attain/` (null side, frozen at `prereg-2`),
  `t0/`, `heldout/`, `n6/`, `alm/`, `instrument/`, and `VERDICT.md`.

## Not in this repository

Ephemerides, NASA eclipse elements, texts exported from the ClassicaCodex
library, and copies of publications are hashed in `data/SHA256SUMS` but not
published. `tools/fetch_*.py` rebuild the public data.
