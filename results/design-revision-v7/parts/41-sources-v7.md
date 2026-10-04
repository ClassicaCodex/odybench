Revision 7's are in `results/design-revision-v7/`:

- `heldout_exch.py`: the design-stage inputs of Q_exch: the drift of H3 and
  H4 inside the epoch band, and P10's held-out part on every spring
  candidate, under three eclipse classes (2.9). The target is removed
  before any computation; `.out.txt` and `.json`;
- `pcr_rows.py`: revision 6's transcription of the words-only projection,
  with the third clause of 6.3; it changes ten rows;
- `verdict_trace.py`: the rule of 9.2 with gate 3b's six legs and the other
  meaning of `same_apparition`, Q_attain3a, Q_attain3b, Q_exch, the lower
  bound of outcome 4 and the eclipse condition of Q_attain4, and the
  constraints C1–C12, run on the 28 synthetic sets of 9.5;
- `check_design.py` and `scan_public.py`: revision 6's mechanical checks and
  leak scan, extended to issues 82–91 and the new tags;
- `splice.py` and `parts/`: how this file was assembled from revision 6;
- `critique-design-r2.recheck-of-rev6.md` and `preserved_sha256.txt`: the
  byte copy of the recheck, and the hashes of what revision 7 cites.

