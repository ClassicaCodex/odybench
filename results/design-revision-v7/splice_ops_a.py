"""Splice operations for DESIGN.md revision 7, part A (header to section 6).
Each op is one of:
  ("region", start_anchor, end_anchor, part_file, sep)  - replace [start, end) by the part
  ("sub", old, new)                                       - replace exactly one occurrence
Anchors and old strings are copied from docs/DESIGN-v6.md (revision 6).
"""
P = "results/design-revision-v7/parts/"

OPS_A = [
    # ---------------------------------------------------------------- header
    ("region", "# odybench — design (revision 6)", "**Status.**", P + "00-header.md", "\n\n"),
    ("region", "**Status.**", "Section 2 lists what is already known, including what the known numbers imply",
     P + "01-status.md", "\n\n"),
    # ---------------------------------------------------------------- section 0
    ("sub", r"""  the mixture**, each model converted to the frame of the elements or
  ephemeris used (4.4, 6.3.3) [r1 N4]. B&M's 27,602.7 s is T0b's clock
  only.""",
     r"""  the mixture**, integrated exactly over each model's Gaussian, each model
  converted to the frame of the elements or ephemeris used (4.4, 6.3.3)
  [r1 N4; r2v6 N2]. B&M's 27,602.7 s is T0b's clock only."""),
    ("sub", r"""section 14 numbers its own R2-1 to R2-12 as 43–54 |""",
     r"""section 14 numbers its own R2-1 to R2-12 as 43–54. The re-run's round-2 recheck now holds that file name; it is cited as [r2v6] |"""),
    ("sub", r"""| [r1v5: script] | a script of that recheck in `results/critique-design-r1/v5/`, with its output |
""",
     r"""| [r1v5: script] | a script of that recheck in `results/critique-design-r1/v5/`, with its output |
| [r2v6 Nn], [r2v6 #n], [r2v6 Cn], [r2v6 §n] | the recheck of revision 6 (new issue Nn, old issue #n, passed check Cn, or section n), written 2026-10-04 by the re-run of the review loop as `docs/critique-design-r2.md`, SHA-256 `6a36dbe3…39fd`. A byte copy is kept at `results/design-revision-v7/critique-design-r2.recheck-of-rev6.md`, because a later round may reuse the name. Section 14.6 numbers its N1–N10 as 82–91 |
| [r2v6: script] | a script of that recheck in `results/critique-design-r2/v6/`, with its output |
"""),
    ("sub", r"""| [v1 §n] … [v5 §n] | `docs/DESIGN-v1.md` … `docs/DESIGN-v5.md` (revision 4: SHA-256 `bd828f14…f5db`; revision 5: `dc082ae1…c85d`) |""",
     r"""| [v1 §n] … [v6 §n] | `docs/DESIGN-v1.md` … `docs/DESIGN-v6.md` (revision 4: SHA-256 `bd828f14…f5db`; revision 5: `dc082ae1…c85d`; revision 6: `c386efda…49b1`) |"""),
    ("sub", r"""revision 5's in `results/design-revision-v5/` and revision 6's in `results/design-revision-v6/`, each with its outputs; the path is given wherever it matters |""",
     r"""revision 5's in `results/design-revision-v5/`, revision 6's in `results/design-revision-v6/` and revision 7's in `results/design-revision-v7/`, each with its outputs; the path is given wherever it matters |"""),
    ("sub", r"""`results/design-revision-v5/preserved_sha256.txt` and, for revision 6's
additions, `results/design-revision-v6/preserved_sha256.txt`.""",
     r"""`results/design-revision-v5/preserved_sha256.txt` and, for the additions of
revisions 6 and 7, `results/design-revision-v6/preserved_sha256.txt` and
`results/design-revision-v7/preserved_sha256.txt`."""),
    # ---------------------------------------------------------------- 1.3
    ("region", "3. **The method cannot see**, split by component [rev #3]:",
     "**Inconclusive** is reported when none of the labels applies", P + "03-outcome3-4.md", "\n\n"),
    ("region", "| qualifier | meaning | inputs | section |",
     "**Standing findings** are printed with every verdict and never change a", P + "04-qualifiers.md", "\n\n"),
    ("sub", r"""- the legs of both gates, and the star-season component that gate 3b does
  not test (6.3.2, 6.4).""",
     r"""- the legs of both gates, and the star-season component that gate 3b does
  not test (6.3.2, 6.4);
- each gate's per-set breakdown (whether each counted set can be narrowed,
  keeps its truth and is seen), with the count seen among the sets that can
  be narrowed, and gate 3b under the other meaning of `same_apparition`
  (6.3.2, 6.4) [r2v6 N1]."""),
    # ---------------------------------------------------------------- 2.6
    ("region", "- **At the true dates** (truth-side; the tables are in [AppT 1–2]):",
     "**The real eclipse records** (`controls_real.json`) [pcr §1, §5; lcr]:", P + "06-alm-known.md", "\n\n"),
    ("sub", r"""- **On the known numbers gate 3a fires.** Both all-must-pass legs are
  expected below 4, while the best-fit leg on the as-licensed primaries is
  expected at exactly 4 (2.10; the per-set basis is in [AppT 6]).
""",
     r"""- **On the known numbers gate 3a fires.** Both all-must-pass legs are
  expected below 4, while the best-fit leg on the as-licensed primaries is
  expected at exactly 4 (2.10; the per-set basis is in [AppT 6]).
""" + "@@PART:07-pcr-known.md@@"),
    ("sub", r"""- **G_j has no estimate yet.** Nobody has computed how often a negative's
  garden makes a random target unique. So whether outcome 4 can fire is
  open until the null-side stage (6.5) [r1v5 N5].""",
     r"""- **G_j has no estimate yet.** Nobody has computed how often a negative's
  garden makes a random target unique, nor whether its eclipse-compatible
  readings can reach an eclipse of the Odyssey's strength (E_j). So
  whether outcome 4 can fire is open until the null-side stage (6.5)
  [r1v5 N5; r2v6 #71]."""),
    # ---------------------------------------------------------------- 2.7
    ("sub", r"""| v5 P27 ({inconclusive}, with Q_BM, Q_tol and Q_slot) | **no longer the expectation** | gate 3a is expected to fire and Q_record to hold (2.10) [r1v5 N1, N2]. Restated |
""",
     r"""| v5 P27 ({inconclusive}, with Q_BM, Q_tol and Q_slot) | **no longer the expectation** | gate 3a is expected to fire and Q_record to hold (2.10) [r1v5 N1, N2]. Restated |
""" + "@@PART:08-settled-rows.md@@"),
    # ---------------------------------------------------------------- 2.9
    ("region", "- **Why ±700 years.** It is the band of P8's stationarity test and of the\n  recheck's proposed sensitivity. ±350 years",
     "**The order of these choices is recorded.**", P + "09-band-exch.md", "\n\n"),
    ("sub", r"""- **The other pools.** G over T_C is 0.0206, and G_BM,u = (n_A/n_T) G_BM ≈
  **0.00172** with n_T ≈ 10,690.""",
     r"""- **The other pools.** G over T_C is 0.0206, and G_BM,u = (n_A/n_T) G_BM ≈
  **0.00172** with n_T ≈ 10,690. The same scaling of the interval gives
  **G_BM,u,lo ≈ 0.00107** and G_BM,u,hi ≈ 0.00263, the bound that outcome
  4 now uses (6.5) [r2v6 N8; me: `results/design-revision-v7/verdict_trace.py`]."""),
    # ---------------------------------------------------------------- 2.10
    ("sub", r"""    - Venus stood 44.3° west of the Sun on Day −5 [unread §2.5], and V needs
      it well west.""",
     r"""    - Venus rose 1 h 43 min before the Sun on Day −5, by B&M's published
      lead, so it stood far west of the Sun, as V needs. A later
      computation, 44.3° west [unread §2.5], corroborates it, but it was not
      on record when H4 was frozen [r2v6 N7]."""),
    ("sub", r"""  - The best-fit leg on the as-licensed primaries is expected at 4, exactly
    its threshold. So Q_score is expected too, but it is not determined.
""",
     r"""  - The best-fit leg on the as-licensed primaries is expected at 4, exactly
    its threshold. So Q_score is expected too, but it is not determined.
  - Two counted sets, R-THUC and R-XEN, cannot be narrowed by any method, so
    at most 5 can be seen on any leg (2.6).
"""),
    ("region", "- **Gate 3b** retains the truth in 9 of 11 sets (2.6). Only narrowing is",
     "  This expectation is not a prediction, and it is never counted as a", P + "11-known-verdict.md", "\n\n"),
    # ---------------------------------------------------------------- 4.4
    ("sub", r"""hit_j included, is target-side and is computed after the second freeze (9.1)
[r1v5 N15g].""",
     r"""hit_j included, is target-side and is computed after the second freeze (9.1)
[r1v5 N15g].

**m̂ = 0.304**, the design-stage value of M_Ody (2.3), is frozen now as its
null-side stand-in. Q_attain4 reads it through E_j, because M_Ody itself
reads the target (6.5) [r2v6 #71]. E_j is also reported at 0.2 and 0.4."""),
    # ---------------------------------------------------------------- 5.2, 5.3
    ("sub", r"""   pool is spring new moons. N2 tests this: V and M pass rates on
   eclipse (h_tot > 0 at any of the five Ionian sites) and non-eclipse spring
   new moons, by permutation (P10). Every analytic shortcut below (5.4, 5.7)
   rests on this check.""",
     r"""   pool is spring new moons. N2 tests this: V and M pass rates on eclipse
   new moons (a solar eclipse anywhere at the conjunction, in NASA's
   catalogue: node proximity) and on the other spring new moons, by Fisher's
   exact test (P10). The class "visible at an Ionian site" is reported
   beside it. Revision 6's class, h_tot > 0 at an Ionian site, holds about 3
   spring candidates and so tests nothing (2.9). The same comparison for H3
   and H4 runs at the null-side stage, in `attain.py`, because Q_exch reads
   it (7.2) [r2v6 N9]. Every analytic shortcut below (5.4, 5.7) rests on
   this check."""),
    ("sub", r"""  | **G_BM,u** | 𝒢_BM* | T | 136 | outcome 4: the Odyssey's coincidence as B&M would present it, every reading treated as blind, compared with fiction's blind readings |""",
     r"""  | **G_BM,u**, with G_BM,u,lo and G_BM,u,hi | 𝒢_BM* | T | 136 | outcome 4: the Odyssey's coincidence as B&M would present it, every reading treated as blind, compared at its lower bound with fiction's blind readings [r2v6 N8] |"""),
    ("sub", r"""  G_BM,u = (n_A(v)/n_T) G_BM(v) exactly, for v1–v5 (4.2). Each G_BM(v) is""",
     r"""  G_BM,u = (n_A(v)/n_T) G_BM(v) exactly, for v1–v5 (4.2). Its interval is
  computed directly over T, as the interval above; the gamma part scales by
  n_A(v)/n_T exactly, so on the design-stage numbers G_BM,u,lo ≈ 0.00107
  and G_BM,u,hi ≈ 0.00263 (2.9). Each G_BM(v) is"""),
    # ---------------------------------------------------------------- 6.1
    ("sub", r"""  I6(b), I10 and I15 now use Horizons and an independent implementation
  on the validated ephemeris.
""",
     r"""  I6(b), I10 and I15 now use Horizons and an independent implementation
  on the validated ephemeris.

The recheck of revision 6 found three more that could not be met as written
[r2v6 N2–N4]: I2(c), whose grid could not reach its tolerance; I16, whose
tie-breaks were undefined and whose scalar reference would have cost over
3,000 core-hours; and I15(b), whose data were to be fetched before they
could exist. Their rows below are re-specified.
"""),
    ("region", "| I1 | ephemeris |", "| I2b | language-to-magnitude", P + "15-instr-rows-a.md", "\n"),
    ("region", "| I15 | the held-out predicates H3 and H4, `heldout.py`",
     "Revision 1's NC4 (the Hymn to Hermes) is dropped", P + "15-instr-rows-b.md", "\n\n"),
    # ---------------------------------------------------------------- 6.3
    ("sub", r"""  - The Babylonian records' own times (PB-E1, E2 and E3-TIME, primary
    "record") keep their primaries, as do all other rows.
""", "@@PART:16-wo-rule.md@@"),
    ("sub", r"""The rule covers all nine sets. Only R-PTOL-BAB and R-PTOL-ALEX contain such
rows, nine in all, and R-PTOL-CHAIN inherits them.
`results/design-revision-v6/pcr_rows.py` transcribes the rule and lists every
affected row [me: its `.out.txt`], and I13(f) checks the file against that
list.""",
     r"""The rule covers all nine sets. Only R-PTOL-BAB and R-PTOL-ALEX contain such
rows, ten in all, and R-PTOL-CHAIN inherits them.
`results/design-revision-v7/pcr_rows.py`, revision 6's script with the third
clause, transcribes the rule and lists every affected row [me: its
`.out.txt`], and I13(f) checks the file against that list."""),
    ("sub", r"""  war-years ± tolerance, year headings 1–3. For each anchor candidate, the
  linked event that fails fewest rows is taken.""",
     r"""  war-years ± tolerance, year headings 1–3. For each anchor candidate, the
  linked event that fails fewest rows is taken; among linked events that
  tie, the earliest by TT instant, in the bench and in I16's reference alike
  [r2v6 N3a]."""),
    ("sub", r"""- **ΔT**: the four-model mixture for every other ΔT-dependent row (6.3.3).""",
     r"""- **ΔT**: the four-model mixture, integrated exactly, for every other
  ΔT-dependent row (6.3.3)."""),
    ("sub", r"""**Why the gate is taken against the claim across all four legs.** Revision 2""",
     "@@PART:18-narrowable-3a.md@@" + r"""**Why the gate is taken against the claim across all four legs.** Revision 2"""),
    ("sub", r"""- **The thresholds stay.** The 5% narrowing and the threshold of 4 are kept
  as frozen in revision 2. Under the family they cannot be what makes the
  gate pass.""",
     r"""- **The thresholds stay.** The 5% narrowing and the threshold of 4 are kept
  as frozen in revision 2. Under the family they cannot be what makes this
  gate pass. That holds for gate 3a, whose legs disagree on the known
  numbers. It does not hold for gate 3b, whose legs are expected to agree;
  6.4 says how that is disclosed [r2v6 N1]."""),
    ("region", "**What the expected firing does not say.** On the known numbers 3a fires",
     "**Reported for every set**, under each leg:", P + "18-firing-says.md", "\n\n"),
    ("sub", r"""- **Pass rule.** A row passes for a candidate if
  P_mix(row passes) ≥ 0.5. The probability is integrated over a 41-point
  ΔT grid spanning ±4σ of each model, weighting each model's Gaussian
  equally.""",
     r"""- **Pass rule.** A row passes for a candidate if P_mix(row passes) ≥ 0.5.
  P_mix is the exact integral of `deltat_mix.p_exact` (10.2): the ΔT
  values at which the row's outcome changes are found by a 10-s scan and
  bisection to 0.1 s, and each model's Gaussian mass over the passing
  intervals is summed, the four models weighted equally [r2v6 N2].
  Revision 6 integrated over a 41-point grid, which errs by up to 0.02 for
  a threshold row and 0.04 for an interval row [r2v6: grid_discretisation.py];
  the grid now enters no rule input."""),
    ("sub", r"""     field. I13(e) checks this.
""",
     r"""     field. I13(e) checks this. A3 reads the cited rows in the public text
     export, which since revision 7 holds exactly these six: Thucydides
     2.28.1, 2.47.1, 4.51.1 and 4.52.1, Diodorus 20.5.5 and Livy 38.36.4.
     None states an absolute date, and I13(h) scans them [r2v6 N5].
"""),
    ("sub", r"""   - **Who decides.** A3 drafts the pair list from the clue file and the
     cited rows. A9, the second reader, checks it. Neither reads the truth.
     I13(f) checks that it parses.""",
     r"""   - **Who decides.** A3 drafts the pair list from the clue file, whose
     licence words quote the cited rows. A9, the second reader, checks it
     from the same. Neither reads the truth, and neither needs the other
     PC-R rows, which stay off the export [r2v6 N5]. I13(f) checks that it
     parses."""),
    # ---------------------------------------------------------------- 6.4
    ("sub", r"""  (`ge_after_same_apparition`, `ge_before_same_apparition`): their primary's""",
     r"""  (`ge_after_same_apparition`, `ge_before_same_apparition`, with the meaning
  frozen below): their primary's"""),
    ("sub", r"""**Two regimes, frozen in `data/prereg/almagest_regimes.json`** [r1 N2 fix 4;""",
     "@@PART:21a-sameapp-rounding.md@@" + r"""**Two regimes, frozen in `data/prereg/almagest_regimes.json`** [r1 N2 fix 4;"""),
    ("sub", r"""(records in no set included), rounded up to the next whole day [r1 N2 fix 1; r2 R2-9]. For Mercury this comes to 6 d in ten counted sets and 5 d in one; for Venus to 21 d in every set [AppT 2] |""",
     r"""(records in no set included), rounded up at each step of the rounding family above: the next 0.1, 0.5 or whole day, the last being revision 4's rule [r1 N2 fix 1; r2 R2-9; r2v6 N6]. At the coarse step this comes to 6 d for Mercury in ten counted sets and 5 d in one, and to 21 d for Venus in every set; the finer steps are in [AppT 2] |"""),
    ("sub", r"""| opposition k (full run only) | leave-one-set-out ceiling over the oppositions in no set: 0.42 d (mean Sun) rounded up = 1 d | middle value |""",
     r"""| opposition k (full run only) | leave-one-set-out ceiling over the oppositions in no set: 0.42 d (mean Sun), rounded up to 0.5, 0.5 and 1 d at the three steps | middle value |"""),
    ("region", "**The gate** [r1v5 N1].", "**The held-out calibration (Q_H)**", P + "21b-gate3b.md", "\n\n"),
    ("sub", r"""    in no set included). Degrees are rounded up to the next 0.1°, and days
    to the next whole day.""",
     r"""    in no set included), rounded up at each step of the rounding family
    above. Revision 6 rounded degrees up to the next 0.1° and days to the
    next whole day, which is now the coarse step. It chose 0.1° with the
    slack table in view [r2v6 N6]; what the steps do at the truths is in
    [AppT 2b]."""),
    ("sub", r"""  - So A.4's opposition tolerance is regime SL's 1 d, not the 3 d that
    revision 5's wording implied [r1v5 N15e].""",
     r"""  - So A.4's opposition tolerance is regime SL's (1 d at the coarse step),
    not the 3 d that revision 5's wording implied [r1v5 N15e]."""),
    ("sub", r"""- **The count.** held_ALM is the number of the 11 counted sets whose truth
  has p ≤ 0.05. **Q_H holds if held_ALM < 6.** It conditions the held-out
  "no" ("the held-out test could not have seen it"). It does not block a
  "yes", for the reason given in 1.3.""",
     r"""- **The count.** held_ALM[step] is the number of the 11 counted sets whose
  truth has p ≤ 0.05 at that rounding step. **Q_H holds if
  held_ALM[step] < 6 at some step**: the decision is taken against the
  claim that the held-out test can see, as gate 3a's is [r2v6 N6]. Q_H
  conditions the held-out "no" ("the held-out test could not have seen
  it"). It does not block a "yes", for the reason given in 1.3."""),
    ("region", "**What is already known** (2.6; the per-set facts are in [AppT 1–2, 6]):",
     "**New vocabulary the harness must implement**", P + "21c-alm-known.md", "\n\n"),
    ("sub", r"""- the bound `same_apparition` (A.1, B.1, I.1, J.4);""",
     r"""- the bound `same_apparition` (A.1, B.1, I.1, J.4), with the meaning frozen
  above and in 10.3, and its side-only meaning for the reported runs;"""),
    # ---------------------------------------------------------------- 6.5
    ("region", "- **Outcome 4 fires if some clean negative has hit_j and G_j,hi ≤ G_BM,u.**",
     "Also reported per set:", P + "22-outcome4.md", "\n\n"),
]
