### 6.3 PC-R: real eclipse records with independently known dates (gate 3a)

**The clue file** is `data/prereg/controls_real.json` exactly as licensed
(SHA-256 `135fba67…83f8` [lcr]). The file is never edited. The searcher reads
only its operational fields. Re-drafted rows are used only to measure
exposure (6.3.4). Nine sets:

| set | text | role |
|---|---|---|
| R-PTOL-BAB | *Almagest* IV.6, three Babylonian lunar eclipses | counted |
| R-PTOL-ALEX | *Almagest* IV.6, three Alexandrian lunar eclipses | counted |
| R-PTOL-CHAIN | the two triples joined by IV.7.1 (E2 to H2: 311,784 nights) | reported; it contains BAB and ALEX |
| R-THUC | Thucydides 2.28, 4.52, 7.50 | counted |
| R-XEN | *Hellenica* 1.6.1, 2.3.4 (linked); 4.3.10 (unlinked) | counted (the linked group) |
| R-ARBELA | Plutarch, Arrian, Curtius, Pliny on one lunar eclipse | counted |
| R-PYDNA | Livy 44.36–37; Plutarch *Aem.* 16–17 | counted |
| R-DIOD | Diodorus 20.5.5 | counted |
| H-LIVY | four prodigy notices | hard case, reported, not pass/fail [rev #2 fix 4] |

**Two projections of the file** [r1v5 N7]. Each set is searched under two
choices of option per row. Both are frozen in `data/prereg/pcr_projection.json`.
`tools/build_pcr_projection.py` (A0, 10.1) writes that file by rule from the
clue file alone, and no truth is read.

- **AL, as licensed:** every row at its primary option.
- **WO, words only:** every row at its primary, except the rows that record
  the author's own computation rather than what was seen:
  - **"none"** for a row whose narrative level marks it as computed from the
    author's tables. These are Ptolemy's six solar longitudes, PB-E1, E2 and
    E3-SUN and PA-H1, H2 and H3-SUN ("κατὰ τοὺς ἐκτεθειμένους ἡμῖν
    ἐπιλογισμούς", 4.6.3) [pcr §3].
  - **The widest licensed option short of "none"** for a row that records
    the author's reduction of his own observation. These are Ptolemy's three
    Alexandrian mid-eclipse times, PA-H1, H2 and H3-TIME ("ἐπελογισάμεθα"),
    which go to `pm1`, ±1 h.
  - The Babylonian records' own times (PB-E1, E2 and E3-TIME, primary
    "record") keep their primaries, as do all other rows.

**Why a words-only projection.** The Odyssey's eclipse component has no
season words and no hour words: "noon" is not in the text (7.1, H7). A
longitude computed from tables, or a time reduced by theory, is more precise
than any phrase. It would make the control easier than the thing it
calibrates. That is the reason gate 3b drops Ptolemy's coordinates (6.4),
and the recheck found the asymmetry [r1v5 N7].

**Why both projections enter the gate.** The words-only rule was written
after the drafter's truth-side check (2.6). Loosening a row can retain a
truth that failed it, or widen a narrowing that passed. So its direction is
not known, and the gate takes its decision against the claim over both
projections (6.3.2).

The rule covers all nine sets. Only R-PTOL-BAB and R-PTOL-ALEX contain such
rows, nine in all, and R-PTOL-CHAIN inherits them.
`results/design-revision-v6/pcr_rows.py` transcribes the rule and lists every
affected row [me: its `.out.txt`], and I13(f) checks the file against that
list.

#### 6.3.1 The search

The harness reads the truth through `data/prereg/truth_index.json`, which
`tools/build_truth_index.py` builds from the two truth files. It places a
136-year window with the anchor event at a uniformly random position (seed
per set). It passes the searcher only the clue set, the projection, the
window bounds and the event catalogues.

- **Candidates** are every event of the anchor's kind in the window: solar
  eclipses from NASA's elements, and lunar eclipses (umbral and penumbral)
  from `lunar.py`.
- **Linked events** are found through the interval rows: exact night counts,
  war-years ± tolerance, year headings 1–3. For each anchor candidate, the
  linked event that fails fewest rows is taken. Unlinked events (R-XEN's X3,
  the H-LIVY notices) are separate searches, reported and not counted.
- **Calendars** follow the file's conventions:
  - Egyptian dates have a free epoch (intervals only);
  - Roman dates have a free offset (primary), with ±90 d and "naive" as
    reported alternatives that are never readings of the text;
  - Attic months go through the modern reconstruction with ±1 lunation. This
    is the one primary that rests on a calendar outside the text [lcr
    flagged item 1].
- **Sites**: a point; a box (the row passes if some site in the box
  satisfies it); a disc; or none. "None" means some site on Earth.
  - **Each row is judged on its own**, as in revision 5. Rows of one event
    with an unstated site need not pass at one common site. That is lenient,
    and it is recorded (13 row 59). It is not changed now, because the
    change could move gate 3a in either direction, and the gate's sets are
    known.
  - **The site-"none" shortcut** [r1v5 N10]. With the site free, a change of
    ΔT only shifts the eclipse's track in longitude. So whether *some* site
    on Earth satisfies a row does not depend on ΔT, and a site-"none" row is
    evaluated once, at the canon ΔT, with P_mix equal to 0 or 1. Revision 5's
    text, a 1° grid under the 41-point mixture of four models, would have
    needed about 2 × 10⁹ local-circumstance evaluations per set [r1v5 N10].
  - **Where a site-"none" solar row is evaluated.** On the eclipse's own
    geometry:
    - the central line, sampled every minute while the eclipse is central;
    - a 1° grid over the penumbral zone, refined to 0.1° near any cell that
      passes, or comes within 0.02 in smag of passing.

    A total path 100–250 km wide can fall between 1° grid points, which is
    why the central line is sampled explicitly. That is about 700 eclipses
    × 2 × 10⁴ cells per window: minutes per set on 14 workers.
  - **A site-"none" lunar row** is evaluated over the hemisphere that sees
    the Moon at the relevant contact.
- **ΔT**: the four-model mixture for every other ΔT-dependent row (6.3.3).

#### 6.3.2 Scoring and the gate

**Scoring** [pcr §5 problem 1; truth-file note]. For a reading, f(c) is the
number of clue rows that candidate c fails. Rows without options are
structural: they define the events and dates.

- **Strict survivors** S₀ = {c : f(c) = 0}: B&M's all-must-pass rule.
- **Best-fit set** B = {c : f(c) = min f}: the dates the record points to,
  allowing for errors in the record.
- **Seen (strict)** := the truth is in S₀, and \|S₀\| ≤ 0.05 × N_cand.
- **Seen (best fit)** := the truth is in B, and \|B\| ≤ 0.05 × N_cand.
  - N_cand is the number of candidates in the window.
  - Either way the method keeps the true date while narrowing the window
    at least 20-fold (4.3 bits).
  - Uniqueness is not required, because a weak record cannot be unique
    however good the method is.
  - When S₀ is not empty, B = S₀ and the two agree. They differ only when no
    candidate passes every row. So a set seen strictly is always seen by
    best fit (constraint C10).
- **Resolution** := the number of clusters in B, where candidates within 3
  days of each other count as one cluster (this matters only for day-unit
  candidates in 6.4). **Unique** := one cluster.
- **Strict recall** := f(truth) = 0.

**The legs of gate 3a** [r1v5 N1, N7]. seen_PCR[leg] is the number of the 7
counted sets seen, under four legs:

| leg | projection | scoring | note |
|---|---|---|---|
| AL_bf | as licensed | best fit | revision 5's gate |
| AL_st | as licensed | strict | B&M's rule, and the rule the bench applies to the Odyssey and to fiction (5.3, 6.5) |
| WO_bf | words only | best fit | |
| WO_st | words only | strict | |

- **3a fires if the smallest of the four counts is below 4** (fewer than
  half of 7, rounded up).
- **Q_score holds if 3a fires and some leg reaches 4.** The gate's decision
  then rests on the scoring rule. Q_score replaces revision 5's Q_strict,
  which counted strict recall without narrowing. That count stays at 4
  whichever rule is used, so Q_strict could never show the choice
  [r1v5 N1].

**Why the gate is taken against the claim across all four legs.** Revision 2
made three choices behind revision 5's gate after the drafter's truth-side
check (2.6): best-fit scoring, the 5% narrowing and the threshold of 4.

- **The known numbers** [r1v5 N1; AppT 6]. Best fit on the as-licensed
  primaries gives exactly 4, and two of those four are seen only because
  best fit tolerates rows their truths fail. All-must-pass, with the same
  narrowing, gives fewer than 4.
- **The words-only rule** was written after the same check, and it changes
  which rows a truth fails (6.3).
- **The consequence.** A pass now needs every leg, so no choice made with
  the answers in view can make the gate pass. 9.3 asks that every bound be
  taken against the claim being made, and here the claim is "the method
  can see".
- **The thresholds stay.** The 5% narrowing and the threshold of 4 are kept
  as frozen in revision 2. Under the family they cannot be what makes the
  gate pass.

**What the strict legs measure.** All-must-pass loses a true date whenever
the record itself errs: a season misremembered, a magnitude misjudged, a
time reduced with a flawed theory. That is a property of the method as well
as of the records, because the Odyssey's readings are scored all-must-pass
too. A strict leg below 4 therefore says that B&M's rule does not recover
real eclipse records. Its "no"s about eclipses are then reported as "could
not have seen it".

**Reported for every set**, under each leg:

- f(truth), \|S₀\|, \|B\| and the truth's rank;
- the same with each row moved, one at a time, to each alternative;
- the fraction of readings that make the truth the unique strict survivor,
  over all fork combinations (sampled to 10,000 where there are more);
- as a sensitivity, the fraction of twenty further window positions per set
  in which the set is seen.

