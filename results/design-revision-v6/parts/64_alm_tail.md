**The B&M-type projection.** The gate uses only rows of B&M's kinds, each
from its words alone, as the Odyssey's clues are:

- interval rows;
- moon-phase rows, at their phase-class option, **except A.10, B.5 and
  B.9**, which are set to "none".
  - A.10 and B.5 choose their phase class from longitudes Ptolemy states in
    the row, his mean Sun from his tables [lca2 item 4].
  - B.9's class, first quarter, is read off the measured Sun–Moon distance
    of 92° (VII.2.4). B.7's class rests on the words "about a quadrant"
    (τεταρτημορίου), so B.7 stays [r1v5 N15f].
  - The Odyssey's phase clue is a phrase (14.161–162). A phase computed from
    a measured or tabulated longitude is more precise than any phrase, so it
    would make the control easier than the thing it calibrates.
  - A.2, A.5, B.2 and B.7 need no coordinates and stay [lca2 item 4].
  - The projection with A.10, B.5 and B.9 at their phase class is reported
    as a sensitivity.
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
`results/design-revision-v6/alm_rows.py` transcribes these rules (revision
5's script with B.9 added to its "none" list) and lists every set's
projection and held-out rows [me: its `.out.txt`]. A0's builder must
reproduce those lists (I13(f)).

**The star-season component is untested** [r1v5 N13; rev #3 fix 4].
- The projection holds intervals, phases, planet rows and one equinox row.
- All 17 star rows are planet–star positions, and all of them are held out.
- The *Almagest* has no dated heliacal star phase [alm §3].
- So C, the clue that carries 3.6 of B&M's bits (1.2), has no test on real
  records. Gate 3b tests the lunar-phase, morning-star and Mercury
  components only, and the verdict says so as a standing finding.
- Adding a star-phase record would need a new dated source, a new drafting
  and a new licence check. None is in reach before the freeze, so none is
  planned.

**Two regimes, frozen in `data/prereg/almagest_regimes.json`** [r1 N2 fix 4;
N3 fix].
- The licence-checked clue file stays byte for byte as it is; its SHA-256
  is recorded in 12.4.
- The regime file names, for every row of the projection and every held-out
  row, the option and the parameter values each regime uses. I13(f) checks
  that every named option exists.
- `tools/build_regimes.py` (A0, 10.1) writes the file mechanically, from
  these rules and the slack table [AppT 1]. Nothing in it is chosen by hand.

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
| option | the row's primary, with the projection's exceptions (A.10, B.5 and B.9 none; A.1, I.1, B.1 and J.4 at `ge_*_same_apparition`) | B&M's own proxy where the row offers it (`bm_mwra_k`, `bm_venus_lead`); else, for a greatest-elongation row, `ge_true_k`; else the row's primary, with the same exceptions [r1 N3 fix] |
| Mercury and Venus greatest-elongation k | **leave-one-set-out ceiling**: the largest \|record − true greatest elongation\| (true Sun) among the records of that body *outside* the set, from alm Table 2 (records in no set included), rounded up to the next whole day [r1 N2 fix 1; r2 R2-9]. For Mercury this comes to 6 d in ten counted sets and 5 d in one; for Venus to 21 d in every set [AppT 2] | 1.5 d, B&M's ±1 integer day as a continuous tolerance [r1 N13]; 1 d reported |
| `bm_mwra_k` | — (not primary anywhere) | 1.5 d |
| `bm_venus_lead`, minimum lead | — | 90 min |
| opposition k (full run only) | leave-one-set-out ceiling over the oppositions in no set: 0.42 d (mean Sun) rounded up = 1 d | middle value |
| every other list in a projected row (j_days, tolerance_days, time_tol_h, minimum minutes, minimum altitude) | most lenient value | middle value (lower middle for an even count) |

Under leave-one-set-out, no set is scored with a tolerance taken from its
own records. **Gate 3b is therefore scored on held-out sets only** [r1 N2
fix 2]. The same records also calibrate the 6-d DOC option of F5 and the
Mercury slot of T_A (5.3), but those serve the Odyssey's garden. Neither
validates the method, so the training-and-testing overlap the recheck
found is broken [r1 N2]. Scoring follows 6.3.2, with N_cand the days in the
window. Resolution and uniqueness are reported.

The per-set tolerances in `almagest_regimes.json` are visible to the
searcher. Under leave-one-set-out, a set whose tolerance differs from the
others is the set that holds the outlier record, and its truth may fail. That
is inherent in the rule, and 13 row 60 records it [r1v5 N15h].

**The gate** [r1v5 N1].

- seen_ALM_SL[leg] is the number of the 11 counted sets seen in regime SL,
  under two legs: best fit (`bf`) and strict (`st`), both with the 5%
  narrowing of 6.3.2.
- **3b fires if either leg is below 6** (fewer than half of 11, rounded up).
  Q_score holds if one leg reaches 6 and the other does not.
- In a window of some 50,000 candidate days S₀ is rarely empty, and then
  B = S₀, so the two legs are expected to agree. Taking both costs nothing,
  and it applies one scoring family to both gates.
- rec_ALM_BM is the number of sets with strict recall and \|S₀\| ≤ 0.05
  N_cand in regime BM (projection, strict).
- **Q_BM holds if rec_ALM_BM < 6**: "B&M's tolerances cannot recover expert
  planetary records" [rev #3 fix 3].
  - It conditions every "no" that rests on B&M's tolerances: label 2's G
    leg, Q_tol and pct_N4.
  - It never blocked outcome 1 after revision 3. Revision 6 removes the last
    gate vetoes too (1.3).
- PC-S no longer enters the gate [r1 N2 fix 3].

**The held-out calibration (Q_H)** [r2 R2-1 fix 4]. Outcome 1 rests on a
rank test of unfitted clues at a date. The founding rule asks for that test
to be shown on records whose date is known.

- **The held-out rows**, named row by row [me: `results/design-revision-v6/alm_rows.out.txt`]:
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
- **Tolerances: leave-one-set-out ceilings, as in regime SL** [r1v5 N12,
  N15e].
  - Revision 5 took the most lenient value of the drafter's lists, the rule
    regime SL abandoned for R2-9's reason.
  - Each held-out row now takes the largest measured \|computed − stated\|
    among the records of its **relation class** *outside* the set (records
    in no set included). Degrees are rounded up to the next 0.1°, and days
    to the next whole day.
  - The classes and their measured offsets come from the slack table [alm
    Tables 3–5; AppT 2]:

    | class | rows | measured offset |
    |---|---|---|
    | planet–star | the star rows; J.7 | each stated component (a longitude or latitude offset, a distance from a line, a distance along it), \|computed − stated\|; a stated occultation, the separation at the record instant; an inequality that holds, 0 |
    | planet–Moon | A.2, A.5, A.10, B.2, B.5 | \|computed − stated\| in longitude |
    | Sun–Moon | B.7, B.9 | \|computed − stated\| elongation |
    | opposition | A.4 | \|record − mean-Sun opposition\|, in days |

  - **Exclusions and fallbacks.**
    - A record contributes nothing when the drafter marks its star as not
      securely identified (X.1.6), or when the stated value is not in the
      words (X.4.3's ¼°, which came from Ptolemy's computed lunar longitude
      [lca2 item 3]).
    - Cruxes enter at the reading the slack summary uses, as regime SL's do.
    - A class with no record outside the set falls back to the pooled lunar
      classes outside the set.
  - So A.4's opposition tolerance is regime SL's 1 d, not the 3 d that
    revision 5's wording implied [r1v5 N15e].
  - The list values are reported as a sensitivity.
- **The count.** held_ALM is the number of the 11 counted sets whose truth
  has p ≤ 0.05. **Q_H holds if held_ALM < 6.** It conditions the held-out
  "no" ("the held-out test could not have seen it"). It does not block a
  "yes", for the reason given in 1.3.
- **Sets that cannot qualify** [r1v5 N8].
  - A set counts as not recovered if it has no held-out row, or if its truth
    is not in the projection's pool. That works against the test.
  - Three counted sets have no held-out row, so **held_ALM ≤ 8 by
    construction, and fewer if a truth fails its own projection**. The
    truth-side ceiling is in [AppT 6].
  - Q_H's threshold of 6 is kept as frozen. That is demanding, and it is
    meant to be: the qualifier then speaks only when the machinery fails on
    records whose held-out rows are star positions, much sharper clues than
    the Odyssey's.

**What is already known** (2.6; the per-set facts are in [AppT 1–2, 6]):

- in regime SL the true date is retained in 9 of the 11 counted sets, and
  only narrowing remains open (P21);
- rec_ALM_BM is at most 5, so **Q_BM holds**, and the bench recomputes it as
  a regression check;
- held_ALM is at most 8 by construction, and at most the truth-side ceiling
  of [AppT 6]. It has not been computed; P24 predicts at least 6.

**New vocabulary the harness must implement** [lca1 item 2; lca2 item 3]:

- the bound `same_apparition` (A.1, B.1, I.1, J.4);
- F.4's `star_candidates`, with one garden branch per candidate;
- B.2's positional `relation`: (Moon's apparent centre − Venus) = 1.5 ×
  (Venus − β Sco), with Venus between the two. This is a held-out row;
- C.3's option `magnitude_and_side` with `eclipsed_limb: north`, and
  `umbral_mag_range` in `magnitude_and_time`. ALM-C is reported only, so
  these never reach the gate.

