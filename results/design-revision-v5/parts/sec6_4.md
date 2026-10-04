### 6.4 The *Almagest* control: real records of B&M's own clue types (gate 3b)

B&M's search uses no eclipse. Its clues are a lunar phase, a star season, a
morning star and a Mercury turning point, and revision 1's "method can see"
gate contained none of these [rev #3].

**The clue file** is `data/prereg/controls_almagest.json` as licence-checked
twice (SHA-256 `18b3ff01…b458`) [lca1; lca2]. It holds 12 sets of dated
records: Mercury and Venus elongations, planet–star and planet–Moon
relations, lunar phases, a lunar eclipse and an equinox. The day intervals
come from Ptolemy's own Egyptian dates, and the date words themselves are
withheld.

**Counted sets** are ALM-A, B and D–L (11). ALM-C is reported only (6.3.5).

**Windows** are 136 years, B&M's width. The harness draws a uniformly random
position for the anchor record's true date (seed per set), as in 6.3.1, and
twenty further positions are a sensitivity. The truth file
`controls_almagest_truth.json` is read only through `truth_index.json`.

**Candidates** are every civil day in the window as Day 0 (LMT at the
default site), with each row at its stated day offset.

- **Instants.** Each row is evaluated at the drafter's instant convention:
  "evening" and "dawn" are the moments the Sun is 8° below the horizon, and
  stated hours are local apparent time [alm §1.5]. The convention moves
  continuous offsets by about ±0.1 d.
- **Hourless records.** C.1, D.3, G.1, L.1 and L.4 state no hour. Their
  civil day comes from ἑῷος or ἑσπέριος (the morning or evening part of the
  dated night), and Ptolemy's own Sun figures confirm every such offset. The
  harness evaluates them at the "dawn" or "evening" instant accordingly
  [lca2 item 5].
- **Cruxes.** The two textual cruxes (A.6 and H.3) run at their primary, as
  printed, and the emended intervals are reported.
- **ΔT** is the mixture, as in 6.3.3.

**The two Ptolemy files treat Egyptian dates differently.** This file
withholds them, while `controls_real.json` carries them with a free epoch
[alm §3; pcr §2]. Both are kept. With the epoch free, an Egyptian date fixes
only intervals, so the two are equivalent for the searcher, provided that
no bench code supplies the Nabonassar epoch (JD 1448638). I13 checks
statically that the number appears only in the truth files and the harness.
The `ref` of every *Almagest* row points at a text row that contains the
withheld date, so the searcher reads only the operational fields and never
the text at `ref` [lca1 item 6; lca2 item 7].

**Default site.** Horizon-dependent rows are evaluated at Alexandria,
31.20°N 29.92°E. That is the observing place Ptolemy names for his own
records (4.6.13, 9.10.3, 11.2.2). The *Almagest* also names Babylon, for the
Babylonian eclipses of IV.6.3 [r1 N17], but those are in R-PTOL-BAB, not in
the B&M-type sets. For sets whose rows leave the observer unstated the site
is an inference, flagged as such: X.8.2 and IX.9.4 in ALM-A, IX.8.3 in
ALM-C, and the observer of every row of ALM-D to ALM-L [lca1 item 5; lca2
item 6]. Babylon is a sensitivity for ALM-K. ALM-K's prose hints (a
Mesopotamian archive, a Babylonian cubit) are not clues [lca2 item 6].

**The B&M-type projection.** The gate uses only rows of B&M's kinds, each
from its words alone, as the Odyssey's clues are:

- interval rows;
- moon-phase rows, at their phase-class option, **except A.10 and B.5**,
  which are set to "none". Their phase classes are chosen from longitudes
  Ptolemy states in the row, his mean Sun from his tables, not from words
  [lca2 item 4]. The Odyssey's phase clue is a phrase (14.161–162). A phase
  computed from a measured longitude is more precise than any phrase, so it
  would make the control easier than the thing it calibrates. A.2, A.5, B.2,
  B.7 and B.9 need no coordinates and stay [lca2 item 4]. The projection
  with A.10 and B.5 at their phase class is reported as a sensitivity;
- planet rows about greatest elongation, before or after greatest
  elongation, visibility, rise lead and the rising-azimuth proxy. **A.1,
  I.1, B.1 and J.4 use their literal, unbounded option**
  (`ge_after_same_apparition`, `ge_before_same_apparition`): their primary's
  bound of 7–60 days is the drafter's inference [lca2 §D], and an inferred
  day interval never enters a gate (critique issue 2). The bounded primary
  is reported as a sensitivity;
- the equinox row.

Star rows, planet–star and planet–Moon positional options, the measured
Sun–Moon distance (`elongation_tol`), oppositions and the eclipse row are set
to none, because they are not in B&M's grammar. They are the held-out rows
below. The full primary run is reported beside.
`results/design-revision-v5/alm_rows.py` transcribes these rules and lists
every set's projection and held-out rows [me: `alm_rows.out.txt`].

**Two regimes, frozen in `data/prereg/almagest_regimes.json`** [r1 N2 fix 4;
N3 fix]. The licence-checked clue file stays byte for byte as it is (its
SHA-256 is recorded in 12.4). The regime file names, for every row of the
projection, the option and the parameter values each regime uses. I13(f)
checks that every named option exists. `tools/build_regimes.py` (A0, 10.1)
writes it mechanically from these rules and from the slack table
[AppT 1]; nothing in it is chosen by hand.

**No regime takes its tolerances from the drafter's grids** [r2 R2-9]. The
lists are the drafter's grids, not licences, and the regime file records
each value as a decision [r1 N2 fix 4]. Regime BM's 1.5 d is not in the
lists. Regime SL's values are ceilings of measured slack:

- **Revision 3's rule is replaced.** It took the smallest listed value at or
  above the out-of-set maximum. That rule is undefined when no listed value
  covers the maximum.
- **The grid's history cannot be settled.** For Venus only the grid's top
  value covered the out-of-set maximum. The note itself calls Mercury 5 or 7
  d and Venus 21 d "the *Almagest* slack" [alm §5 item 1]. That suggests the
  list was written with the measured slack in view, but the file times
  cannot settle it [r2 R2-9].
- **The ceiling rule** depends on neither the list nor its history, and it is
  always defined.

| | regime SL (observer slack, leave-one-set-out) | regime BM (B&M's method as written) |
|---|---|---|
| option | the row's primary, with the two exceptions of the projection (A.10 and B.5 none; A.1, I.1, B.1 and J.4 at `ge_*_same_apparition`) | B&M's own proxy where the row offers it (`bm_mwra_k`, `bm_venus_lead`); else, for a greatest-elongation row, `ge_true_k`; else the row's primary, with the same two exceptions [r1 N3 fix] |
| Mercury and Venus greatest-elongation k | **leave-one-set-out ceiling**: the largest \|record − true greatest elongation\| (true Sun) among the records of that body *outside* the set, from alm Table 2 (records in no set included), rounded up to the next whole day [r1 N2 fix 1; r2 R2-9]. For Mercury this comes to 6 d in ten counted sets and 5 d in one; for Venus to 21 d in every set [AppT 2] | 1.5 d, B&M's ±1 integer day as a continuous tolerance [r1 N13]; 1 d reported |
| `bm_mwra_k` | — (not primary anywhere) | 1.5 d |
| `bm_venus_lead`, minimum lead | — | 90 min |
| opposition k (full run only) | leave-one-set-out ceiling over the oppositions in no set: 0.42 d (mean Sun) rounded up = 1 d | middle value |
| every other list (j_days, tolerance_deg, tolerance_days, time_tol_h, minimum minutes, minimum altitude) | most lenient value | middle value (lower middle for an even count) |

Under leave-one-set-out, no set is scored with a tolerance taken from its
own records. **Gate 3b is therefore scored on held-out sets only** [r1 N2
fix 2]. The same records also calibrate the 6-d DOC option of F5 and the
Mercury slot of T_A (5.3), but those serve the Odyssey's garden. Neither
validates the method, so the training-and-testing overlap the recheck
found is broken [r1 N2]. Scoring follows 6.3.2: best-fit; seen := the truth
is in B and \|B\| ≤ 0.05 N_cand, N_cand being the days in the window.
Resolution and uniqueness are reported.

**The gate.**

- seen_ALM_SL is the number of the 11 counted sets seen in regime SL
  (projection, best-fit).
- rec_ALM_BM is the number with strict recall and \|S₀\| ≤ 0.05 N_cand in
  regime BM (projection, strict).
- **3b fires if seen_ALM_SL < 6** (fewer than half of 11, rounded up).
  PC-S no longer enters the gate [r1 N2 fix 3].
- **Q_BM holds if rec_ALM_BM < 6**: "B&M's tolerances cannot recover expert
  planetary records" [rev #3 fix 3]. It conditions every "no" that rests on
  B&M's tolerances: label 2's G leg, Q_tol and pct_N4. It no longer blocks
  outcome 1. Revision 3 used it to demand G_DOC there, but outcome 1 now
  rests on the exact held-out test, whose validity does not depend on
  anyone's tolerances being realistic (7.2).

**The held-out calibration (Q_H)** [r2 R2-1 fix 4]. Outcome 1 rests on a
rank test of unfitted clues at a date. The founding rule asks for that test
to be shown on records whose date is known.

- **The held-out rows**, named row by row (revision 4 left the moon-phase
  rows ambiguous; [me: `alm_rows.out.txt`]):
  - star rows, at their primary option (F.4's primary is "none", so F.4
    holds nothing out);
  - planet rows whose primary is a position or an opposition: A.4
    (`opp_mean_k`) and J.7 (`positional`);
  - moon-phase rows, at the option that states the record's own
    measurement: `positional` (the planet–Moon relation) for A.2, A.5, A.10,
    B.2 and B.5, and `elongation_tol` (the measured Sun–Moon distance) for
    B.7 and B.9.

  Per counted set: ALM-A A.2, A.4, A.5, A.10; ALM-B B.2, B.3, B.5, B.7, B.9;
  ALM-D D.4; ALM-H H.2, H.5, H.6, H.9; ALM-I I.2, I.3, I.5; ALM-J J.2, J.5,
  J.7; ALM-K K.2, K.5, K.8; ALM-L L.2, L.7. **ALM-E, ALM-F and ALM-G have
  none.** `almagest_regimes.json` lists them.
- **The null pool.** The candidate days of the set's window that pass every
  projection row in regime SL, with the true date excluded.
- **The score and the p-value.** The score is that of 7.2: each held-out row
  is weighted by −log10 of its pass rate over the pool plus the truth. The
  p-value is p = (1 + #{days with score ≥ the truth's})/(1 + n).
- **Tolerances.** Each held-out option takes the most lenient listed value,
  as in regime SL.
- **The count.** held_ALM is the number of the 11 counted sets whose truth
  has p ≤ 0.05. **Q_H holds if held_ALM < 6.** It conditions the held-out
  "no" ("the held-out test could not have seen it"), and it does not block a
  "yes", for the reason given under Q_BM.
- **Sets with nothing held out.** A set whose truth is not in the
  projection's pool, or which has no held-out row, counts as not recovered.
  That works against the test. Three counted sets have no held-out row, so
  **held_ALM ≤ 8** by construction, and Q_H needs 6 of the 8 that can
  qualify. That is demanding, and it is meant to be: the qualifier then
  speaks only when the machinery fails on records whose held-out rows are
  star positions, much sharper clues than the Odyssey's.

**What is already known** (2.6; the per-set facts are in [AppT 1–2]):

- in regime SL the true date is retained in 9 of the 11 counted sets, and
  only narrowing remains open (P21);
- rec_ALM_BM is at most 5, so **Q_BM holds**, and the bench recomputes it as
  a regression check;
- held_ALM ≤ 8 by construction, and it has not been computed. P24 predicts
  at least 6.

**New vocabulary the harness must implement** [lca1 item 2; lca2 item 3]:

- the bound `same_apparition` (A.1, B.1, I.1, J.4);
- F.4's `star_candidates`, with one garden branch per candidate;
- B.2's positional `relation`: (Moon's apparent centre − Venus) = 1.5 ×
  (Venus − β Sco), with Venus between the two. This is a held-out row;
- C.3's option `magnitude_and_side` with `eclipsed_limb: north`, and
  `umbral_mag_range` in `magnitude_and_time`. ALM-C is reported only, so
  these never reach the gate.

