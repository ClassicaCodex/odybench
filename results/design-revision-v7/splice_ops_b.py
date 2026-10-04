"""Splice operations for DESIGN.md revision 7, part B (section 7 to Appendix T).
Same conventions as splice_ops_a.py."""
P = "results/design-revision-v7/parts/"

OPS_B = [
    # ---------------------------------------------------------------- 7.1
    ("sub", r"""| D2 | Venus a morning star far west of the Sun around Day −5: lead 1:42:56 on Ti−5; greatest morning elongation in mid-March | B&M 2008, §Intersecting; MacDonald 1967 p. 327 ("17 March", under a year that is a slip for 1178) [unread §2.5]; rev V10 (103.6 min); unread §2.5 (44.3° west on 11 Apr) | H4 | with D1, **settles H4: fails.** Venus 44° west and Mars within about 20° of the Sun cannot lie within 5° of each other on Days −10 to −4 |""",
     r"""| D2 | Venus a morning star far west of the Sun around Day −5: lead 1:42:56 on Ti−5; greatest morning elongation in mid-March | **On record:** B&M 2008, §Intersecting (the lead); MacDonald 1967 p. 327 ("17 March", under a year that is a slip for 1178) [unread §2.5]. **Corroboration written after the freeze, not record** [r2v6 N7]: rev V10 (103.6 min, written 3 Oct at 21:02) and unread §2.5 (44.3° west on 11 Apr, written 4 Oct) | H4 | with D1, **settles H4: fails.** A Venus that rises 1 h 43 min before the Sun stands far west of it, and an invisible Mars stood within about 20° of the Sun, so they cannot lie within 5° of each other on Days −10 to −4 |"""),
    ("sub", r"""  - It prints file names, dates and quantity codes, never values.""",
     r"""  - It prints file names, line numbers, dates and quantity codes, never
    values."""),
    ("sub", r"""  - A0 drafts the table from that list and from the published sources, and
    A9 checks it.
  - Neither reads a value that the table marks "constrains": those values
    stay unread until the second freeze.
""", "@@PART:23-sealed.md@@"),
    # ---------------------------------------------------------------- 7.2
    ("sub", r"""  - **Why ±700 years.** It is the band of P8's stationarity test and of the
    recheck's proposed sensitivity. A band of ±350 years would leave about
    14 members in P_MWRA,E, whose floor would then be 0.067 [me:
    `results/design-revision-v6/band_counts.py`].
  - **When it was chosen.** With the design-stage null side in view and no
    target-side value; adding pools can only make "yes" harder.""",
     r"""  - **Why ±700 years.** It is the band the recheck of revision 5 proposed
    [r1v5 N11]. Revision 6 also called it the band of P8's stationarity
    test, which was wrong: P8 compares the first and last 700 years of the
    background [r2v6 N10c]. A band of ±350 years would leave about 14
    members in P_MWRA,E, whose floor would then be 0.067 [me:
    `results/design-revision-v6/band_counts.py`], and outcome 1 would be
    unattainable for every target.
  - **When it was chosen.** With the design-stage null side in view, the
    ±350-year floor among it, and no target-side value. Adding pools can
    only make "yes" harder. The width kept a "yes" possible for some
    target; Q_record rules it out for this one (7.1)."""),
    ("sub", r"""    should not change their rates. P10 tests that on P_spring. R20 tests
    the homogeneity of P_BM across Mercury events, and R21 across epochs.""",
     r"""    should not change their rates. P10 tests that for V and M, and Q_exch
    for H3 and H4 (below). R20 tests the homogeneity of P_BM across Mercury
    events, and R21 across epochs."""),
    ("sub", r"""- **Attainability, a null-side quantity** [r2 R2-1 fix 4].
""", "@@PART:24-exch.md@@" + r"""- **Attainability, a null-side quantity** [r2 R2-1 fix 4].
"""),
    # ---------------------------------------------------------------- 7.3
    ("sub", r"""  - the same within ±700 years of the target against the rest;
""",
     r"""  - the same within ±700 years of the target against the rest;
  - the same inside the band, its early half against its late half, and
    P10's held-out part, which Q_exch reads (R29);
"""),
    # ---------------------------------------------------------------- 8
    ("sub", r"""- **P21, P24, P25 and P27 are restated**: P21 for both legs of gate 3b, P24
  for the ceiling on held_ALM, P25 for outcome 4's attainability, and P27
  for the new expected verdict.""",
     r"""- **P21, P24, P25 and P27 are restated**: P21 for both legs of gate 3b, P24
  for the ceiling on held_ALM, P25 for outcome 4's attainability, and P27
  for the new expected verdict.

Revision 7 changes these [r2v6 N1, N6, N8, N9, #71]:

- **P21, P24, P25 and P27 are restated again**: P21 for the sets that can
  be narrowed, on all six legs; P24 across the rounding steps; P25 with the
  Odyssey's lower bound and the eclipse condition; P27 for the frozen
  meaning of `same_apparition`.
- **P10** keeps V and M, on an eclipse class with power. Its held-out part
  is roughly known, and it moves to R29.
- **R10** states the frozen meaning and the rounding steps.
- **R28** (the gates' attainability) and **R29** (Q_exch) are new."""),
    ("sub", r"""| R10 | In regime SL, with the ceiling tolerances and the word-only projection of 6.4, the truth is in the best-fit set B of exactly 9 counted *Almagest* sets; the two exceptions are named in [AppT 6]. Revision 5's and 6's projection changes (A.10, B.5 and B.9 to none; the literal `same_apparition` options) only loosen rows, so they cannot lose a retained truth (`almagest.py`) | R10 | 2.6, 6.4 |""",
     r"""| R10 | In regime SL, with the ceiling tolerances at every rounding step, the word-only projection of 6.4 and the frozen meaning of `same_apparition`, the truth is in the best-fit set B of exactly 9 counted *Almagest* sets; the two exceptions are named in [AppT 6]. Revision 5's and 6's projection changes (A.10, B.5 and B.9 to none) only loosen rows. The frozen meaning adds a visibility clause to the literal options, so that argument does not cover it; [AppT 2] records that every truth passes the clause (`almagest.py`) | R10 | 2.6, 6.4 |"""),
    ("sub", r"""| R27 | Q_record holds at the null-side stage: with H4 = fail in the disclosure table, no consistent pass pattern reaches p_H ≤ 0.05 on the measured lattice (`attain.py`) [r1v5 N2] | — | 2.10, 7.2 |
""",
     r"""| R27 | Q_record holds at the null-side stage: with H4 = fail in the disclosure table, no consistent pass pattern reaches p_H ≤ 0.05 on the measured lattice (`attain.py`) [r1v5 N2] | — | 2.10, 7.2 |
| R28 | **Q_attain3a and Q_attain3b do not hold.** At the null-side stage R-THUC and R-XEN are the only counted PC-R sets that cannot be narrowed on any leg (N_narrow 5, against a threshold of 4), and ALM-I, J and K the only counted *Almagest* sets (N_narrow 8, or 7 if ALM-B misses the line, against 6) (`attain.py`) [r2v6 N1] | — | 2.6, 6.3.2, 6.4 |
| R29 | **Q_exch does not hold.** P10's held-out part (any solar eclipse against none, over the spring candidates) and the drift of H3 and H4 inside the epoch band, in P_BM,E and P_MWRA,E, all have Fisher p > 0.05; rough values p ≥ 0.17 (`attain.py`) [r2v6 N9] | v6 P10, held-out part | 2.9, 7.2 |
"""),
    ("sub", r"""- **P10.** V and M, and the held-out predicates H3 and H4, pass at the same
  rates on eclipse and on non-eclipse spring new moons (permutation p > 0.05
  for each). The exactness of p_H rests on this for H3 and H4 (7.2).
  (v3 P11, extended)""",
     r"""- **P10.** V and M pass at the same rates on eclipse new moons (a solar
  eclipse anywhere at the conjunction, in NASA's catalogue) and on the
  other spring new moons: two-sided Fisher p > 0.05 for each. The held-out
  part, H3 and H4, is now regression expectation R29, because its rough
  values are known (2.9); Q_exch reads it (7.2). (v3 P11; the eclipse class
  and the held-out part restated in revision 7 [r2v6 N9])"""),
    ("sub", r"""- **P21.** seen_ALM_SL ≥ 6 on both legs: at least 6 of the 9 sets that
  retain their truth (R10) also narrow their window to 5%, by best fit and
  strictly. (v3 P25)""",
     r"""- **P21.** Gate 3b does not fire: seen_ALM_SL ≥ 6 on all six legs, best
  fit and strict at every rounding step, under the frozen meaning of
  `same_apparition`. At most 8 counted sets can be narrowed (R28), so P21
  needs at least 6 of those 8 seen, each keeping its truth; [AppT 6] gives
  the truth-side count. The set nearest the line, ALM-B, passes about 4.4%
  of days on the rough estimate (2.6). (v3 P25; restated in revisions 6 and
  7 [r2v6 N1])"""),
    ("sub", r"""- **P24.** Q_H does not hold: at least 6 of the 11 counted *Almagest* sets
  give their true date p ≤ 0.05 on their own held-out rows, with the
  ceiling tolerances of 6.4. At most 8 sets can qualify by construction,
  and fewer if a truth fails its projection. [AppT 6] gives the truth-side
  number, so this needs 6 of the sets that can qualify [r1v5 N8, #17d].
  (revision 4)""",
     r"""- **P24.** Q_H does not hold: at every rounding step of the held-out
  ceilings (6.4), at least 6 of the 11 counted *Almagest* sets give their
  true date p ≤ 0.05 on their own held-out rows. At most 8 sets can qualify
  by construction, and fewer if a truth fails its projection. [AppT 6]
  gives the truth-side number, and what the fine step does to one held-out
  row [r1v5 N8, #17d; r2v6 N6]. (revision 4; restated in revisions 6 and 7)"""),
    ("sub", r"""- **P25.** Outcome 4 is attainable and does not fire. At the null-side stage
  at least one clean negative has 0 < G_j and G_j,hi ≤ G_BM,u, so Q_attain4
  does not hold. After the second freeze no clean negative fires outcome 4.
  P25 fails if Q_attain4 holds, because a "no 4" would then mean nothing
  [r1v5 N5]. (v3 P28, restated)""",
     r"""- **P25.** Outcome 4 is attainable and does not fire. At the null-side stage
  at least one clean negative has 0 < G_j, G_j,hi ≤ G_BM,u,lo and E_j ≥ 1, so
  Q_attain4 does not hold. After the second freeze no clean negative fires
  outcome 4. P25 fails if Q_attain4 holds, because a "no 4" would then mean
  nothing [r1v5 N5; r2v6 N8, #71]. (v3 P28, restated in revisions 6 and 7)"""),
    ("sub", r"""- **P27.** The verdict's labels are exactly {3a}. Its qualifiers include
  Q_BM, Q_tol, Q_slot and Q_record. They exclude Q_attain, Q_contra, Q_ΔT,
  Q_exposure, Q_H and Q_attain4. Q_score is not predicted, because its leg
  sits on the threshold.
  - P27 is the conjunction of P18, the first branch of R15, P21, P24, P25,
    and the expectations R8, R9, R12, R17 and R24–R27.
  - It fails if any of them fails, including when r_Ody = 0 gives label 2
    its "no match" form.
  - (Restated in revision 6 [r1v5 N1]. Revision 5 expected {inconclusive}
    with Q_BM, Q_tol and Q_slot.)""",
     r"""- **P27.** The verdict's labels are exactly {3a}. Its qualifiers include
  Q_BM, Q_tol, Q_slot and Q_record. They exclude Q_attain, Q_attain3a,
  Q_attain3b, Q_attain4, Q_exch, Q_contra, Q_ΔT, Q_exposure and Q_H.
  Q_score is not predicted: it holds if gate 3a's best-fit leg reaches its
  threshold, or if gate 3b passes under the frozen meaning of
  `same_apparition` and fails under the other, and both are knife-edges.
  - P27 is the conjunction of P18, the first branch of R15, P21, P24, P25,
    and the expectations R8, R9, R12, R17 and R24–R29.
  - It fails if any of them fails: when r_Ody = 0 gives label 2 its "no
    match" form, and when gate 3b fires, as in S0y's {3a, 3b}.
  - (Restated in revisions 6 and 7 [r1v5 N1; r2v6 N1]. Revision 5 expected
    {inconclusive} with Q_BM, Q_tol and Q_slot.)"""),
    # ---------------------------------------------------------------- 9.1
    ("sub", r"""| Q_record | no pass pattern consistent with the `determined` values of the frozen disclosure table reaches p_H ≤ 0.05 on the measured lattice | null, with the frozen table | 7.1, 7.2 | `attain.py` |
""",
     r"""| Q_record | no pass pattern consistent with the `determined` values of the frozen disclosure table reaches p_H ≤ 0.05 on the measured lattice | null, with the frozen table | 7.1, 7.2 | `attain.py` |
| Q_exch | P10's held-out part fails, or H3 or H4 drifts inside the epoch band: two-sided Fisher p ≤ 0.05 in any of the six tests of 7.2 [r2v6 N9] | null | 7.2 | `attain.py` |
"""),
    ("sub", r"""| G_BM,u; n_T | G(𝒢_BM*; T; W = 136); equal to (n_A(v)/n_T) G_BM(v) for v1–v5 | null | 5.3 | `attain.py` |""",
     r"""| G_BM,u, G_BM,u,lo, G_BM,u,hi; n_T | G(𝒢_BM*; T; W = 136), with the interval of 5.3; G_BM,u equals (n_A(v)/n_T) G_BM(v) for v1–v5 | null | 5.3 | `attain.py` |"""),
    ("sub", r"""| G_j, G_j,lo, G_j,hi; n_j | for each of the 12 clean negatives: G of the set's full garden over its targets, with the interval of 5.3 [r1v5 N5] | null | 6.5 | `attain.py` |""",
     r"""| G_j, G_j,lo, G_j,hi; n_j; E_j | for each of the 12 clean negatives: G of the set's full garden over its targets, with the interval of 5.3 [r1v5 N5]; and E_j, the number of core conjunctions with h_tot ≥ m̂ = 0.304 at the eclipse-compatible option's site and day that some eclipse-compatible reading makes unique in a 136- or 251-year window, with E_j at 0.2 and 0.4 reported [r2v6 #71] | null | 6.5 | `attain.py` |
| narrowable[g][leg][set]; N_narrow[g][leg] | for every counted set of gate 3a (four legs) and of gate 3b (six legs, the frozen meaning; the other meaning reported): \|S₀\| (strict) or \|B\| (best fit) is at most 5% of the candidates in at least 11 of the 21 null windows of I16(a); N_narrow is the count over the counted sets [r2v6 N1] | null | 6.3.2, 6.4 | `attain.py` |"""),
    ("sub", r"""| seen_ALM_SL[leg], for leg ∈ {bf, st}; rec_ALM_BM | of the 11 counted *Almagest* sets: seen in regime SL (ceiling tolerances, leave-one-set-out) by best fit and strictly; strict recall with narrowing in regime BM | controls | 6.4 | `almagest.py` |""",
     r"""| seen_ALM_SL[leg] and seen_ALM_SL_side[leg], for leg ∈ {bf, st} × {fine, mid, coarse}; rec_ALM_BM | of the 11 counted *Almagest* sets: seen in regime SL (ceiling tolerances, leave-one-set-out, at each rounding step) by best fit and strictly, under the frozen meaning of `same_apparition` and, read only by Q_score, under the side-only meaning; strict recall with narrowing in regime BM | controls | 6.4 | `almagest.py` |"""),
    ("sub", r"""| held_ALM | of the 11 counted *Almagest* sets, the number whose true date has p ≤ 0.05 on the set's held-out rows | controls | 6.4 | `almagest.py` |""",
     r"""| held_ALM[step], for step ∈ {fine, mid, coarse} | of the 11 counted *Almagest* sets, the number whose true date has p ≤ 0.05 on the set's held-out rows, with the held-out ceilings at that rounding step | controls | 6.4 | `almagest.py` |"""),
    # ---------------------------------------------------------------- 9.2
    ("region", "```\nif not INSTR:", "### 9.3 How to read it", P + "28-rule.md", "\n\n"),
    # ---------------------------------------------------------------- 9.3
    ("sub", r"""  veto is gone, and label 4, which concerns the eclipse match, never bore
  on the held-out test.""",
     r"""  veto is gone, and label 4, which concerns the eclipse match, never bore
  on the held-out test. The exchangeability that the exact test needs is
  qualified instead, by Q_exch (7.2) [r2v6 N9]."""),
    ("sub", r"""  - outcome 4 uses the negative's upper bound, and Q_attain4 says when no
    negative could have met it;""",
     r"""  - outcome 4 sets the negative's upper bound against the Odyssey's lower
    bound, and Q_attain4 says when no negative could have met both its
    conditions [r2v6 N8, #71];"""),
    ("sub", r"""  - **the gates take the decision against "the method can see"** across
    every scoring chosen after the answers were read: 3a fires if any of its
    four legs fails, 3b if either of its two does (6.3.2, 6.4) [r1v5 N1].""",
     r"""  - **the gates take the decision against "the method can see"** across
    every scoring and rounding step chosen after the answers were read: 3a
    fires if any of its four legs fails, 3b if any of its six does, and Q_H
    holds if any rounding step fails (6.3.2, 6.4) [r1v5 N1; r2v6 N6]."""),
    ("region", "- **The gates' thresholds** (4 of 7 and 6 of 11) and the 5% narrowing were",
     "- **Label combinations.**", P + "29-gate-thresholds.md", "\n"),
    ("sub", r"""  2. label 1;""",
     r"""  2. label 1, with Q_exch beside it if Q_exch holds;"""),
    ("sub", r"""  the return by an exact test; separately, the eclipse component, or the
  B&M-type component, cannot see, or the eclipse-matching method dates
  fiction.""",
     r"""  the return by an exact test; separately, the eclipse component, or the
  B&M-type component, is not shown to see (or is untested by these
  controls), or the eclipse-matching method dates fiction."""),
    ("sub", r"""and the verdict says so beside 3a; nothing is relaxed to avoid it (6.3.2) |""",
     r"""and the verdict says so beside 3a, mechanically since revision 7 (narrowable, Q_attain3a and the per-set breakdown); nothing is relaxed to avoid it (6.3.2) |"""),
    ("sub", r"""  6. then Q_attain, Q_record and Q_attain4, which say which outcomes could
     not have been reached.""",
     r"""  6. then Q_attain, Q_record, Q_attain4, Q_attain3a and Q_attain3b, which
     say which outcomes and gates could not have been reached."""),
    # ---------------------------------------------------------------- 9.4, 9.5
    ("region", "I14(b) checks every set against C1–C11.",
     "A realisable set may contradict these, because the rule must also be shown to",
     P + "30-constraints.md", "\n\n"),
    ("region", "`data/prereg/verdict_synthetic/*.json` holds these inputs.", "---\n\n## 10. Software",
     P + "31-synthetic.md", "\n\n"),
]

OPS_C = [
    # ---------------------------------------------------------------- 10.1
    ("sub", r"""  - `data/prereg/*.json` except `*truth*`, and `data/jsex/`, `data/ephem/`
    and `data/stars.json`;""",
     r"""  - `data/prereg/*.json` except `*truth*`, and `data/jsex/`, `data/ephem/`
    (less the sealed files of 7.1) and `data/stars.json`;"""),
    ("sub", r"""    - for every other file it holds only the rows that `negatives.json`
      cites (five rows of Pliny);
    - it holds **no row of Ptolemy's *Syntaxis*, and none of the historians
      of PC-R**. The Ptolemy rows state the Nabonassar year and Egyptian day
      of every *Almagest* record, which the clue file withholds; one line of
      arithmetic turns them into the truth. A3 needs only the clue files'
      operational fields, and A9 needs the negatives' texts and, for the
      sibling pairs, the licence words already in `controls_real.json`;""",
     r"""    - for every other file it holds only the rows that `negatives.json`
      cites (five rows of Pliny), and the six rows that the five re-drafted
      PC-R rows cite (6.3.4): Thucydides 2.28.1, 2.47.1, 4.51.1 and 4.52.1,
      Diodorus 20.5.5 and Livy 38.36.4. None states an absolute date, and
      I13(h) scans them [r2v6 N5];
    - it holds **no row of Ptolemy's *Syntaxis*, and no other row of the
      historians of PC-R**. The Ptolemy rows state the Nabonassar year and
      Egyptian day of every *Almagest* record, which the clue file
      withholds; one line of arithmetic turns them into the truth. A3 needs
      the clue files' operational fields and the six rows above, and A9
      needs the negatives' texts and, for the sibling pairs, the licence
      words already in `controls_real.json`;"""),
    ("sub", r"""  - these notes: `docs/research-bm2008*.md`, `research-chronology.md`,""",
     r"""  - these notes, with the sealed lines of 7.1 masked in the export:
    `docs/research-bm2008*.md`, `research-chronology.md`,"""),
    ("sub", r"""  `data/ref*/`, and the rest of `results/`.""",
     r"""  `data/ref*/`, and the rest of `results/`. The sealed files of 7.1 are off
  it too, for another reason: they hold the target's sky."""),
    ("sub", r"""1. **Before any public-tier agent starts**, A0 writes `access.json`. A6 then""",
     r"""1. **Before any public-tier agent starts**, A0 writes `access.json`, with
   the sealed list of 7.1. A6 then"""),
    ("sub", r"""  - a script the agent wrote or ran that names such a path.
""",
     r"""  - a script the agent wrote or ran that names such a path;
  - for every agent of either tier, a direct read of a sealed path before
    `prereg-2` (7.1) [r2v6 N7].
"""),
    ("sub", r"""`odybench/model.py`; `data/prereg/access.json` (first, step 1 above); `sites.json`""",
     r"""`odybench/model.py`; `data/prereg/access.json` (first, step 1 above, with the sealed list of 7.1); `sites.json`"""),
    ("sub", r"""(6.4: options, parameters, held-out rows and their ceiling tolerances, all by rule)""",
     r"""(6.4: options, parameters, held-out rows and their ceiling tolerances at the three rounding steps, all by rule)"""),
    ("sub", r"""`tools/make_redraft_brief.py`, `tests/test_clues.py`""",
     r"""`tools/make_redraft_brief.py` (from the export's six PC-R rows, 6.3.4), `tests/test_clues.py`"""),
    ("sub", r"""| A6 harness and verdict | truth | `tools/public_design.py`, `tools/export_public.py`, `tools/check_access.py` (all first, step 1 above);""",
     r"""| A6 harness and verdict | truth | `tools/public_design.py`, `tools/export_public.py` (with the six PC-R rows and the masked notes), `tools/check_access.py` (with the sealed paths, over both tiers) (all first, step 1 above); `tools/run_i1.py` (6.1);"""),
    ("sub", r"""`tests/control_reference.py` (I16) |""",
     r"""`tests/control_reference.py` and `tests/bessel_vec.py` (I16) |"""),
    # ---------------------------------------------------------------- 10.2
    ("region", "**`odybench/deltat_mix.py`** (the four-model mixture, 0 and 6.3.3)",
     "**`odybench/eclipses.py`**", P + "33a-deltat-mix.md", "\n\n"),
    ("sub", r"""local(ecl, lat, lon, dt_s, elev_m=0.0) -> dict(smag, obsc, central, duration_s,""",
     r"""local(ecl, lat, lon, dt_s: float | f8[m], elev_m=0.0) -> dict(smag, obsc, central, duration_s,"""),
    ("sub", r"""local(lecl, lat, lon, dt_s) -> dict(moon_alt at each contact, moonrise_ut,""",
     r"""local(lecl, lat, lon, dt_s: float | f8[m]) -> dict(moon_alt at each contact, moonrise_ut,"""),
    ("sub", r"""load_controls_almagest(regime="SL"|"BM"|"held_out") / load_negatives()""",
     r"""load_controls_almagest(regime="SL"|"BM"|"held_out", step="fine"|"mid"|"coarse",
      apparition="frozen"|"side") / load_negatives()"""),
    ("sub", r"""      # scorings; site-"none" rows use the shortcut of 6.3.1""",
     r"""      # scorings; site-"none" rows use the shortcut of 6.3.1; linked events take
      # the fewest failed rows, ties going to the earliest (6.3.1)"""),
    ("region", "reference_fails(clueset_json: dict, projection: dict, window: (jd0, jd1),",
     "**`odybench/pools.py`, `readings.py`, `reach.py`, `evidence.py`**", P + "33b-control-ref.md", "\n\n"),
    ("sub", r"""      -> dict(seen_bf, seen_st, strict_recall, f_truth, rank, resolution)   # both scorings (6.3.2)
""",
     r"""      -> dict(seen_bf, seen_st, strict_recall, f_truth, rank, resolution)   # both scorings (6.3.2)
harness.narrowing(result: SearchResult) -> dict(frac_strict, frac_bf)
      # reads no truth; attain.py uses it on the 21 null windows for narrowable (6.3.2, 6.4)
"""),
    ("sub", r"""heldout.stationarity(flags_null: dict, years: dict) -> dict(table, fisher_p)               # R21
""",
     r"""heldout.stationarity(flags_null: dict, years: dict) -> dict(table, fisher_p)               # R21
heldout.exch(flags_spring: bool[n, 2], eclipse_any: bool[n], flags_band: dict[str, bool[m, 2]],
      years: dict) -> dict(tests, fisher_p, Q_exch)   # 7.2: P10's held-out part, the drift inside the band
"""),
    ("sub", r"""attain.run() -> writes results/attain/attain.json            # n_T, n_TC, n_A[v], G_BM[v] (GStat),
      # G_BM_u, G_DOC[v] (reported); per held-out pool (four) n, x_max, the H3-only, H4-only
      # and both counts, q3, q4; p_H_min; the lattice; Q_record; the homogeneity (R20),
      # stationarity (R21) and "H3 given D4" tables; G_j (GStat) and n_j for the 12 clean
      # negatives; Q_attain4; the checks I7(a), I9(b, c), I11, I15(a, b), I16(a), I14(c)""",
     r"""attain.run() -> writes results/attain/attain.json            # n_T, n_TC, n_A[v], G_BM[v] (GStat),
      # G_BM_u (GStat, with lo and hi), G_DOC[v] (reported); per held-out pool (four) n, x_max,
      # the H3-only, H4-only and both counts, q3, q4; p_H_min; the lattice; Q_record; the
      # homogeneity (R20), stationarity (R21) and "H3 given D4" tables; Q_exch with its six
      # tests (7.2); G_j (GStat), n_j and E_j (at 0.304, with 0.2 and 0.4) for the 12 clean
      # negatives; Q_attain4; narrowable and N_narrow for every counted set and leg of both
      # gates, both meanings for 3b; Q_attain3a, Q_attain3b; the Horizons tables of I15(b),
      # fetched into results/attain/horizons/; the checks I7(a), I9(b, c), I11, I15(a, b),
      # I16(a), I14(c)"""),
    ("sub", r"""`attain.json` is the only file the second freeze commits besides its text
output.""",
     r"""`attain.json` is the only file the second freeze commits besides its text
output and the Horizons tables of I15(b) in `results/attain/horizons/`."""),
    # ---------------------------------------------------------------- 10.3
    ("sub", r"""| `ge_relation` | body, side, before or after, j days or `same_apparition` (the literal option the projection uses, 6.4) | ALM A.1, B.1, I.1, J.4 |""",
     r"""| `ge_relation` | body, side, before or after, j days or `same_apparition` (the literal option the projection uses; its meaning is frozen below and in 6.4), and `same_apparition_side`, the side-only meaning for the reported runs | ALM A.1, B.1, I.1, J.4 |"""),
    ("sub", r"""- **ΔT-dependent predicates** pass when P_mix ≥ 0.5 (`dt_rule="mixture_p50"`),""",
     r"""- **ΔT-dependent predicates** pass when P_mix ≥ 0.5 (`dt_rule="mixture_p50"`,
  with P_mix the exact integral `deltat_mix.p_exact`, 10.2),"""),
    ("sub", r"""- **Linked rows** (6.5). A row whose day another row's option sets is built""",
     r"""- **`same_apparition`** (frozen in revision 7) [r2v6 N1]. The body is on the
  row's side of the Sun and visible on Day 0: its lead or lag is at least
  the row's `visible_only` minimum at the regime's value, 30 min. The
  apparition is the interval between the conjunctions with the Sun, in
  apparent ecliptic longitude, that bracket the record's instant. The
  greatest elongation on the row's side, from the true Sun, lies in it,
  after the instant (A.1, I.1) or before it (B.1, J.4).
  `same_apparition_side` is the same without the visibility clause, for the
  reported runs of 6.4.
- **Linked rows** (6.5). A row whose day another row's option sets is built"""),
    ("sub", r"""  "none" and his three computed Alexandrian mid-times to ±1 h (6.3). Each""",
     r"""  "none", his three computed Alexandrian mid-times to ±1 h, and PB-E2-TIME to
  the record's own `in-progress` (6.3). Each"""),
    # ---------------------------------------------------------------- 10.4
    ("sub", r"""| `deltat_mix.py` | `ephem.delta_t` and `ephem.delta_t_sigma` evaluated directly, and a 10⁶-draw Monte Carlo of the mixture | P(total) for 1178 and 1131 BC on NASA's elements against the 2.3 table | 0.005 | I2(c) |""",
     r"""| `deltat_mix.py` (`p_exact`) | closed-form Gaussian masses of synthetic step and interval functions; `ephem.delta_t` and `ephem.delta_t_sigma` evaluated directly; a 10⁶-draw Monte Carlo of the mixture | the synthetic cases; P(total) for 1178 and 1131 BC on NASA's elements against the 2.3 table | 10⁻⁴; 0.005, and 3 SE + 0.001 against the Monte Carlo | I2(c) |"""),
    ("sub", r"""| the control searches: `search.py` and `harness.score` | `tests/control_reference.py` (A7, public tier), with the review's Besselian solver for solar circumstances, its own lunar-shadow geometry and its own ΔT mixture | every counted set and leg, and the regime-SL, regime-BM and held-out runs; 21 random background windows per set (null-side stage) and the gates' own windows (controls stage) | identical per-row flags and f(c) outside the tie bands of 6.1; identical seen and strict flags | I16 |""",
     r"""| the control searches: `search.py` and `harness.score`, and the narrowing that `narrowable` reads | `tests/control_reference.py` (A7, public tier), with `tests/bessel_vec.py` for solar circumstances (early exit on the eclipse's own geometry for site-free rows), its own lunar-shadow geometry and its own ΔT mixture | every counted set and leg, both meanings of `same_apparition` and every rounding step, and the regime-BM and held-out runs; 21 random background windows per set (null-side stage) and the gates' own windows (controls stage) | identical f(c), seen and strict flags; identical per-row flags for anchor and unlinked rows, and for linked rows where both sides chose the same event; site-free rows compared by witness; all outside the tie bands of 6.1 | I16 |
| `tests/bessel_vec.py` (I16's solar reference) | the review's scalar solver `check_bessel.maxecl`, which I2(b) checks against `eclipses.py` | 1,000 random site–eclipse pairs | magnitude 10⁻⁵; time of maximum 1 s | I16, first |"""),
    # ---------------------------------------------------------------- 10.5
    ("sub", r"""| `coincidence.py` | N2 | `results/n2/` |""",
     r"""| `coincidence.py` | N2 (P10's V and M part; its held-out part runs in `attain.py`) | `results/n2/` |"""),
    ("sub", r"""| `controls.py` | I16(b) first, then PC-R on both projections and both scorings, every variant, and the exposure audit (I2b runs earlier, from `tools/run_i2b.py`) | `results/pcr/` |""",
     r"""| `controls.py` | I16(b) first, then PC-R on both projections and both scorings, every variant, the words-only legs with A-MONTH at none (reported), the per-set breakdown, and the exposure audit (I2b runs earlier, from `tools/run_i2b.py`) | `results/pcr/` |"""),
    ("sub", r"""| `almagest.py` | I16(b) first, then the *Almagest* control on both scorings, regime BM, the held-out calibration and the Bayes factors | `results/alm/` |""",
     r"""| `almagest.py` | I16(b) first, then the *Almagest* control on both scorings at three rounding steps under both meanings of `same_apparition`, with the per-set breakdown and the 4% and 6% lines; regime BM; the held-out calibration at three steps; and the Bayes factors | `results/alm/` |"""),
    ("sub", r"""| `attain.py` | the null-side stage: pools with the target masked; G_BM per slot variant, G_BM,u, G_DOC (reported); the four held-out pools with their counts, p_H,min, the lattice and Q_record; the homogeneity (R20), stationarity (R21) and "H3 given D4" tables; G_j for the 12 clean negatives and Q_attain4; the checks I7(a), I9(b, c), I11, I15(a, b), I16(a) and I14(c) | `results/attain/` (committed at the second freeze) |""",
     r"""| `attain.py` | the null-side stage: pools with the target masked; G_BM per slot variant, G_BM,u with its bounds, G_DOC (reported); the four held-out pools with their counts, p_H,min, the lattice and Q_record; the homogeneity (R20), stationarity (R21) and "H3 given D4" tables; Q_exch; G_j and E_j for the 12 clean negatives, and Q_attain4; narrowable and N_narrow for both gates, and Q_attain3a and Q_attain3b; the Horizons fetch of I15(b); the checks I7(a), I9(b, c), I11, I15(a, b), I16(a) and I14(c) | `results/attain/`, with `horizons/` (committed at the second freeze) |"""),
    ("sub", r"""  and `tools/run_i2b.py` (6.1, 12.1).""",
     r"""  and `tools/run_i2b.py` (6.1, 12.1); and revision 7's `tools/run_i1.py`
  (6.1, 7.1)."""),
    ("sub", r"""| `control_reference.py` | I16 |""",
     r"""| `control_reference.py`, `bessel_vec.py` | I16 |"""),
    # ---------------------------------------------------------------- 11
    ("sub", r"""| **Horizons geocentric tables** (QUANTITIES 31 and 23, TT): 200 random events for I6(b), every P_BM member for I15(b), and 200 PC-S truths for I10 | the same tool | a few hundred requests | I6(b), I15(b), I10 [r1v5 N4] |""",
     r"""| **Horizons geocentric tables** (QUANTITIES 31 and 23, TT): 200 random events for I6(b), and 200 PC-S truths for I10 | the same tool, at step 0 | a few hundred requests | I6(b), I10 [r1v5 N4] |
| **Horizons geocentric tables for every P_BM member** (I15(b)) | the same tool, called by `attain.py` at the null-side stage, because P_BM exists only then; cached in `results/attain/horizons/` with the request URL on line 1 (12.3) | about 80 members × 4 bodies; tens of requests | I15(b) [r2v6 N4] |"""),
    ("sub", r"""the disclosure scan and `heldout_disclosure.json` (7.1);""",
     r"""the disclosure scan, `heldout_disclosure.json` and the sealed list (7.1);"""),
    ("region", "| 6 | null side | I7(a), I9(b, c), I11, I15(a, b) and I16(a)",
     "| 7 | | **second freeze**", P + "37-step6.md", "\n"),
    ("sub", r"""| 16 | target and controls | PC-R and the *Almagest* control, with its held-out calibration; **I16(b) first**, on the gates' own windows, before any gate count is read | `py controls.py`; `py almagest.py` | 1–2 h | 21 windows per set; two projections and two scorings for PC-R, two scorings for 3b; the site-"none" shortcut (6.3.1); the mixture grid; I16(b) repeats the evaluation once |""",
     r"""| 16 | target and controls | PC-R and the *Almagest* control, with its held-out calibration; **I16(b) first**, on the gates' own windows, before any gate count is read | `py controls.py`; `py almagest.py` | 1.5–3 h | 21 windows per set; two projections and two scorings for PC-R; for 3b, two scorings at three rounding steps under two meanings; the site-"none" shortcut (6.3.1); the exact mixture integral; I16(b) repeats the evaluation once, its reference under 30 min [r2v6 N3] |"""),
    ("sub", r"""After the first freeze, about 8–14 hours of computation remain.""",
     r"""After the first freeze, about 9–17 hours of computation remain."""),
    # ---------------------------------------------------------------- 12
    ("sub", r"""2. The pre-freeze instrument checks pass: I1, I2, I4 (after its convention""",
     r"""2. The pre-freeze instrument checks pass: I1 (rerun through
   `tools/run_i1.py`, whose full output is sealed, 7.1), I2, I4 (after its convention"""),
    ("sub", r"""   values of both regimes for every projected row, and the ceiling
   tolerances of every held-out row (6.4).""",
     r"""   values of both regimes for every projected row, and the ceiling
   tolerances of every held-out row, at each of the three rounding steps
   (6.4)."""),
    ("sub", r"""   - A9 has checked it;
   - nobody has read a value that the table marks "constrains".""",
     r"""   - A9 has checked it;
   - `access.json` holds the sealed list of 7.1: every line and file the
     scan lists under a "constrains" fact, and every output that prints
     those values;
   - `tools/check_access.py` has found no direct read of a sealed path by
     any agent [r2v6 N7]."""),
    ("sub", r"""    - I13(h) has passed on both the copy and the text export;""",
     r"""    - I13(h) has passed on both the copy and the text export, the six PC-R
      rows of 6.3.4 and the masked notes of 7.1 included;"""),
    ("sub", r"""  - after the null-side stage, `results/attain/`.""",
     r"""  - after the null-side stage, `results/attain/`, with the Horizons tables of
    I15(b) in `results/attain/horizons/` [r2v6 N4]."""),
    ("sub", r"""- **The checks.** It runs I7(a), I9(b, c), I11, I15(a, b) and I16(a) first,
  and stops if any fails.
- **The quantities.** It computes the null-side quantities of 9.1, G_j and
  Q_record included, and writes `results/attain/attain.json` and
  `attain.out.txt`.""",
     r"""- **Network.** `attain.py` makes one kind of network request: the Horizons
  geocentric tables of I15(b), for the members of P_BM it has just built,
  through the frozen `tools/fetch_horizons_obs.py`. Each response is cached
  in `results/attain/horizons/` with its request URL on line 1, and the
  second freeze commits them [r2v6 N4].
- **The checks.** It runs I7(a), I9(b, c), I11, I15(a, b) and I16(a) first,
  and stops if any fails.
- **The quantities.** It computes the null-side quantities of 9.1: G_j and
  E_j, Q_record, Q_exch, and narrowable for both gates included. It writes
  `results/attain/attain.json` and `attain.out.txt`."""),
    ("sub", r"""  - whether S4 is realisable, which is Q_attain4 [r1v5 N5];""",
     r"""  - whether S4 is realisable, which is Q_attain4 [r1v5 N5; r2v6 #71];
  - Q_attain3a, Q_attain3b and Q_exch;"""),
    ("sub", r"""  - is outcome 4 attainable (Q_attain4)?""",
     r"""  - is outcome 4 attainable (Q_attain4)?
  - could either gate have passed (Q_attain3a, Q_attain3b)?
  - is the held-out test's exchangeability in doubt (Q_exch)?"""),
    # ---------------------------------------------------------------- 13
    ("sub", r"""| 62 | Whether the held-out rates are stationary over the background | the rough rows show H3's rate drifting between the halves [r1v5 N11] | epoch-matched pools in the rule (7.2); R21 |
""",
     r"""| 62 | Whether the held-out rates are stationary over the background | the rough rows show H3's rate drifting between the halves [r1v5 N11] | epoch-matched pools in the rule (7.2); R21 |
""" + "@@PART:39-open-rows.md@@"),
    # ---------------------------------------------------------------- 14
    ("sub", r"""Five tables follow:""", r"""Six tables follow:"""),
    ("sub", r"""- **14.5 gives the 15 issues N1–N15 of the recheck of revision 5 [r1v5],
  numbered 67–81.**""",
     r"""- 14.5 gives the 15 issues N1–N15 of the recheck of revision 5 [r1v5],
  numbered 67–81;
- **14.6 gives the 10 issues N1–N10 of the recheck of revision 6 [r2v6],
  numbered 82–91, and its finding on #71.**"""),
    ("sub", r"""marked **Departure**. Rows 26–66 keep revision 5's text, and where revision
6 changes one of those resolutions, 14.5 says so.""",
     r"""marked **Departure**. Rows 26–66 keep revision 5's text, and rows 67–81
revision 6's. Where a later revision changes one of those resolutions, 14.5
or 14.6 says so."""),
    ("sub", r"""The recheck of revision 5 found 22 of these resolved, and #11, #13 and #17
not fully resolved [r1v5 §2]. Revision 6 resolves those three through the
issues of 14.5, and the rows below say what else it changed.""",
     r"""The recheck of revision 5 found 22 of these resolved, and #11, #13 and #17
not fully resolved [r1v5 §2]. Revision 6 resolved those three through the
issues of 14.5. The recheck of revision 6 found all 25 resolved in their own
terms [r2v6 §2]; its residuals are its new issues, which 14.6 answers. The
rows below say where revision 7 changed a resolution."""),
    ("sub", r"""Every set marked realisable uses the design-stage null side (C7), and I14(c) reruns all 21 with the measured null side.""",
     r"""Every set marked realisable uses the design-stage null side (C7), and I14(c) reruns all of them with the measured null side."""),
    ("sub", r"""pct_N4 stays in label 2 | 1.3, 2.9, 2.10, 3.5, 4.2, 5.4, 6.5, 7, 9, 12 |""",
     r"""pct_N4 stays in label 2. **Revision 7** [r2v6 N1, N8, #71]: Q_attain3a and Q_attain3b say when a gate could not have passed; outcome 4 compares with the Odyssey's lower bound and needs a negative that can reach an eclipse of its strength; the trace holds 28 sets | 1.3, 2.9, 2.10, 3.5, 4.2, 5.4, 6.5, 7, 9, 12 |"""),
    ("sub", r"""which is this issue's fix 4 [N13] | 1.3, 2.6, 6.3, 6.4, 9 |""",
     r"""which is this issue's fix 4 [N13]. **Revision 7** [r2v6 N1, N6]: the meaning of `same_apparition` is frozen; which sets can be narrowed is a null-side quantity, with Q_attain3b and a per-set breakdown; gate 3b and Q_H are taken across three rounding steps | 1.3, 2.6, 6.3, 6.4, 9, 10.3 |"""),
    ("sub", r"""Every INSTR row now states its reference's measured accuracy (6.1) | 6.1, 6.2, 10.1, 10.4, 11 |""",
     r"""Every INSTR row now states its reference's measured accuracy (6.1). **Revision 7** [r2v6 N2–N4]: I2(c) tests an exact mixture integrator; I16's reference is vectorised, with a deterministic tie-break, witness sites and a budget; I15(b)'s data are fetched at the null-side stage | 6.1, 6.2, 6.3.3, 10.1, 10.2, 10.4, 11, 12.3 |"""),
    ("sub", r"""Section 8 counts only quantities that need new runs | 2.7, 2.10, 8 |""",
     r"""Section 8 counts only quantities that need new runs. **Revision 7** [r2v6 N1, N9, #71]: P21, P24, P25 and P27 are restated on the gate's real ceiling, the rounding family and the lower bound, and P10's held-out part, now roughly known, moves to R29 | 2.7, 2.10, 8 |"""),
    ("sub", r"""P25 now predicts attainability as well as the absence of label 4 | 1.3, 2.6, 2.10, 6.5, 8, 9, 10.1, 11.2 |""",
     r"""P25 now predicts attainability as well as the absence of label 4. **Not resolved in substance** [r2v6 #71]: revision 7 adds the eclipse condition (14.6) | 1.3, 2.6, 2.10, 6.5, 8, 9, 10.1, 11.2 |"""),
    ("sub", r"""---

## Sources""", "@@PART:40-review-r2v6.md@@" + r"""---

## Sources"""),
    # ---------------------------------------------------------------- Sources
    ("sub", r"""  `scan_public_leaks.py`, `neg_garden_sizes.py`, `real_rows.py`,
  `dump_prereg.py`).""",
     r"""  `scan_public_leaks.py`, `neg_garden_sizes.py`, `real_rows.py`,
  `dump_prereg.py`).
- the recheck of revision 6 [r2v6], written by the re-run of the review loop
  as `critique-design-r2.md` and kept as
  `results/design-revision-v7/critique-design-r2.recheck-of-rev6.md`;
  scripts in `results/critique-design-r2/v6/` (`narrowing_3b.py`,
  `grid_discretisation.py`, `bessel_timing.py`, `scan_public_leaks_v6.py`,
  `fisher_check.py`, `dump_clues.py`, `compact_almagest.py`)."""),
    ("sub", r"""- `DESIGN-v1.md` to `DESIGN-v5.md`, revisions 1–5 of this design.""",
     r"""- `DESIGN-v1.md` to `DESIGN-v6.md`, revisions 1–6 of this design."""),
    ("sub", r"""Each script has its `.out.txt` beside it.""",
     "@@PART:41-sources-v7.md@@" + r"""Each script has its `.out.txt` beside it."""),
    ("sub", r"""| 55 | Whether any clean negative could fire outcome 4 | it needs a garden that makes some targets unique but few enough that G_j,hi ≤ G_BM,u; nobody has estimated G_j [r1v5 N5] | G_j at the null-side stage; Q_attain4 reports the answer before any target-side number (6.5) |""",
     r"""| 55 | Whether any clean negative could fire outcome 4 | it needs a garden that makes some targets unique but few enough that G_j,hi ≤ G_BM,u,lo, and an eclipse-compatible reading that can make an eclipse of the Odyssey's strength unique; nobody has estimated G_j or E_j [r1v5 N5; r2v6 N8, #71] | G_j and E_j at the null-side stage; Q_attain4 reports the answer before any target-side number (6.5) |"""),
    ("sub", r"""**`tests/control_reference.py`** (I16, A7) exposes one function, so that the""",
     r"""**`tests/control_reference.py`** (I16, A7) exposes two functions, so that the"""),
    # ---------------------------------------------------------------- current-revision phrases
    ("sub", r"""  Revisions 4–6 keep them unchanged, and the order is recorded here [r2""",
     r"""  Revisions 4–7 keep them unchanged, and the order is recorded here [r2"""),
    ("sub", r"""Revisions 5 and 6 keep the numbering. A withdrawn prediction keeps its""",
     r"""Revisions 5–7 keep the numbering. A withdrawn prediction keeps its"""),
    ("sub", r"""  revision 1, with their resolution as of revision 6;""",
     r"""  revision 1, with their resolution as of revision 7;"""),
    ("sub", r"""| # | severity | resolution, as of revision 6 | sections |""",
     r"""| # | severity | resolution, as of revision 7 | sections |"""),
    # ---------------------------------------------------------------- revision 7's transcriptions
    ("sub", r"""`results/design-revision-v6/verdict_trace.py`, an independent transcription of 9.2 |""",
     r"""`results/design-revision-v7/verdict_trace.py`, an independent transcription of 9.2 |"""),
    ("sub", r"""    port), and `design-revision-v6/alm_rows.py`, `pcr_rows.py` and
    `verdict_trace.py`. None of them holds a control's date [me: grep].""",
     r"""    port), `design-revision-v6/alm_rows.py`, and `design-revision-v7/pcr_rows.py`
    and `verdict_trace.py`. None of them holds a control's date [me: grep;
    `results/design-revision-v7/scan_public.py`]."""),
    ("sub", r"""`results/design-revision-v6/verdict_trace.py`'s `p_pool`, an independent transcription of 7.2""",
     r"""`results/design-revision-v7/verdict_trace.py`'s `p_pool`, an independent transcription of 7.2"""),
    ("sub", r"""| `pcr_projection.json` | `results/design-revision-v6/pcr_rows.py`, a transcription of 6.3's rule written before the file |""",
     r"""| `pcr_projection.json` | `results/design-revision-v7/pcr_rows.py`, a transcription of 6.3's rule written before the file |"""),
    ("sub", r"""| `verdict_rule.py` | the synthetic sets as traced by `results/design-revision-v6/verdict_trace.py`; the structural constraints; the rerun with the measured null side | 21 sets; 11 constraints | exact | I14 |""",
     r"""| `verdict_rule.py` | the synthetic sets as traced by `results/design-revision-v7/verdict_trace.py`; the structural constraints; the rerun with the measured null side | 28 sets; 12 constraints | exact | I14 |"""),
    ("sub", r"""   it must equal `results/design-revision-v6/pcr_rows.out.txt` (I13(f))""",
     r"""   it must equal `results/design-revision-v7/pcr_rows.out.txt` (I13(f))"""),
    ("sub", r"""      # violated constraints C1-C11 of 9.4; [] if realisable, "pending" if it""",
     r"""      # violated constraints C1-C12 of 9.4; [] if realisable, "pending" if it"""),
    # ---------------------------------------------------------------- Appendix T
    ("sub", r"""### T2b. The held-out tolerances under the ceiling rule of 6.4""",
     "@@PART:42a-appT2.md@@" + r"""### T2b. The held-out tolerances under the ceiling rule of 6.4"""),
    ("sub", r"""### T3. The real eclipse records at the accepted dates""",
     "@@PART:42b-appT2b.md@@" + r"""### T3. The real eclipse records at the accepted dates"""),
    ("sub", r"""### T4. The controls in the data behind SMH's ΔT fits""",
     "@@PART:42c-appT3T6.md@@" + r"""### T4. The controls in the data behind SMH's ΔT fits"""),
    ("sub", r"""### T7. The data coverage of the control windows""",
     "@@PART:42d-appT6.md@@" + r"""### T7. The data coverage of the control windows"""),
]
