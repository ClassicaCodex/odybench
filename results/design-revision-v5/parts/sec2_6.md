### 2.6 Controls: what is already known about them

Facts measured at a control's true date are truth-side. Revision 5 keeps
them in Appendix T, which the agents who translate and search the control
files do not see (10.1). This section keeps the facts that need no truth,
and what the truth-side facts imply in aggregate.

**The *Almagest* records of B&M's own clue types** (`controls_almagest.json`)
[alm §0, §3; lca1; lca2]:

- **Two licence checks**, neither of which read a truth file. Round 1 edited
  43 rows. Round 2 re-checked all 72 and edited 24, removing no row and
  changing no primary option, option name or day offset [lca2 Result]. Every
  word licence is now an exact substring of its cited row, in text order
  [lca2 method 1]. File history: `e16c559d…37e9` (the builder's output),
  `758ee789…4c83` (round 1), `18b3ff01…b458` (round 2) (12.4).
- **Ptolemy's arithmetic, checked without the truth.**
  - His own solar tables reproduce his stated mean Sun for 32 of 34 records
    to ≤ 0.12° [alm §1.3].
  - The two failures are textual cruxes, carried as forks whose primary is
    "as printed": IX.7.11, one Egyptian month (ALM-H.3), and IX.9.4, three
    days (ALM-A.6) [alm §1.4].
  - Round 2 recomputed all 20 interval rows from the Greek alone, and again
    from Ptolemy's Sun. Every interval agrees within 0.3 d except the two
    cruxes, and Ptolemy's Sun confirms both emended intervals, +49 for A.6
    and +72 for H.3 [lca2 method 3].
- **Structure** [me: a dump of the file, `results/design-revision-v5/`
  notes]. 12 sets and 72 rows: 26 planet, 20 interval, 17 star, 7
  moon-phase, 1 lunar-eclipse and 1 season row.
  - ALM-E, ALM-F and ALM-G have no row outside the B&M-type projection whose
    primary is not "none" (F.4, their only star row, has primary "none").
    They therefore have no held-out row (6.4), and **held_ALM ≤ 8** by
    construction.
- **Two lunar phases rest on Ptolemy's numbers, not on his words** [lca2
  item 4; lca1 item 4]. A.10 and B.5 choose their phase class from
  longitudes stated in the row. The other phase rows (A.2, A.5, B.2, B.7,
  B.9) need no coordinates.
- **Four primaries carry a day bound the words do not give** [lca2 §D]. A.1
  and I.1 (`ge_after_within_j`) and B.1 and J.4 (`ge_before_within_j`) bound
  the greatest elongation to j = 7–60 days away. Each row also has the
  literal, unbounded option `ge_*_same_apparition` [lca1 item 2].
- **At the true dates** (truth-side; the tables are in [AppT 1–2]):
  - the observer slack of a "greatest elongation" record is a few days for
    Mercury and up to three weeks for Venus, and B&M's Mercury proxy (the
    MWRA) is a different event from greatest elongation;
  - in regime SL (6.4) the true date is retained in **9 of the 11 counted
    sets**. Whether those 9 also narrow their windows to 5% has not been
    computed; that is what gate 3b still tests (P21);
  - in regime BM the true date can pass in at most 5 counted sets, so
    **rec_ALM_BM ≤ 5 < 6, and Q_BM holds** whatever the narrowing. It is
    recomputed as a regression check, not predicted [r1 N3].

**The real eclipse records** (`controls_real.json`) [pcr §1, §5; lcr]:

- **Freeze and licence check.** The clue file was frozen before any accepted
  date was looked up (SHA-256 `eb1f0401…9256`, 2026-10-04 05:19 UTC). An
  agent blind to the truth then licence-checked it. That agent moved seven
  unstated-site primaries to "none" and made seven other edits
  (SHA-256 `135fba67…83f8`) [lcr]. The re-run of the workflow did not touch
  this file.
- **The drafting was not fully blind.**
  - The drafter had seen critique issue 2 and revision 1's I2b row, and flags
    three primaries as possibly steered: T1-DARK, D-ECL and the ±1 h in
    L4-DARK [pcr §1].
  - The recheck found a fourth that the drafter did not flag, T2-SEASON
    [r1 N5]. Its primary "early" spans solar longitude [330°, 60°], and its
    start and width are the drafter's. The same set's T1- and T3-SEASON use
    Thucydides' half-year, [0°, 180°] (5.20.3).
  - The recheck also named T-INT-12's ±0.5-year tolerance.
  - Why these two matter is truth-side [AppT 3].
- **A rough post-freeze check** by the drafter, with its own lunar model
  (not the bench's; I4 has not run), found that the accepted dates fail some
  primary reading in three of the seven counted sets and pass every primary
  in the other four [pcr §5; AppT 3]. Which rows fail stays on the truth
  side.
- **Four control eclipses appear in the data behind SMH's ΔT fits** [r1 N4]:
  R-DIOD's eclipse, H-LIVY's L4, R-THUC's T1 and R-XEN's X3. The table
  entries, their years and their bounds are truth-side [AppT 4]. Whether the
  *Almagest* lunar timings entered the fits is not settled: SMH2016's Table
  S4 and §4b have not been read (pre-freeze task, 12.1).
- **Moving the site primaries to "none"** weakens R-THUC and R-XEN in the
  primary run [lcr, Consequences].

**The negatives** (`negatives.json`) [neg; lcn; lcn2]:

- 13 sets: 12 clean negatives, and the Iliad as a same-tradition comparison.
- 70 clue rows and 34 excluded rows; 183 fork options after round 2 [lcn2
  finding 1].
- **Two licence checks**, neither of which read a truth file or
  `docs/research-controls.md`.
  - Round 1 edited 21 rows [lcn §3].
  - Round 2 edited 8 more rows and 5 sets, and kept every round-1 edit
    [lcn2 findings 1, 9]. Its report could not be written to `docs/`, so its
    text is kept as [lcn2], and its verdicts are in the file's
    `license_check` fields.
  - All 178 clue fragments and all 32 place and landmark fragments match
    their cited rows, and no date leaks [lcn2 finding 1].
  - File history: `405f78da…bebe` (the builder's output), `f4ae3b26…bb00`
    (round 1), `be4f511e…9c82` (round 2) (12.4).
- **What round 2 changed that the design must translate** (6.5): a new
  Day-0 solar-eclipse option, ARG-RETURN-04:d; a fourth reading of *Aen.*
  2.255 with its pin, AEN-TROY R-iii; Ida moved from the observer places to a
  new `landmarks` list; ARG-COLCHIS-01's night now set by ARG-COLCHIS-02's
  option [lcn2 findings 3–5, 8].
- I11(a), the contradictory AEN-TROY reading R-ii-literal, gives **zero
  survivors** at Troy among 1,683 conjunctions of 1250–1115 BC and 3,104 of
  1350–1100 BC. That holds by astronomy, not by logic [r1:
  check_i11a.py]. Round 2's R-iii keeps 2.340 and is not contradictory, so
  it is an ordinary pinned reading.

