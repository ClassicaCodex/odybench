# Adversarial review of DESIGN.md, revision 6 (recheck, round 2)

Written 2026-10-04 by a reviewer who did not write DESIGN.md or any earlier
review. Scope: `DESIGN.md` revision 6 (all 5,649 lines, Appendix T included),
judged against the 25 issues of `docs/critique-design.md` and the 15 new issues
of the recheck of revision 5 (`docs/critique-design-r1.md`, [r1v5]), and
searched for new problems.

**This file's name.** The re-run of the review loop writes its round-2 recheck
to `docs/critique-design-r2.md`. The earlier file of that name, the recheck of
revision 3 that DESIGN cites as [r2], is preserved byte for byte at
`results/design-revision-v5/critique-design-r2.recheck-of-rev3.md`. I checked
before overwriting: both had SHA-256 `8db84b10…c493` (`cmp` identical).
DESIGN's [r2 …] tags keep pointing at that copy. A later revision should cite
this file as [r2v6], and could number its N1–N10 as 82–91 in section 14.

**What I read.**
- In full:
  - `DESIGN.md`;
  - `docs/critique-design.md`;
  - `docs/critique-design-r1.md`;
  - both control clue files, `data/prereg/controls_real.json` (78 rows) and
    `controls_almagest.json` (72 rows), dumped row by row [me:
    `dump_clues.py`, `compact_almagest.py`].
- In part:
  - revision 6's scratch outputs: `verdict_trace.py` and its output,
    `alm_rows.out.txt`, `pcr_rows.out.txt`, `heldout_epochs.out.txt`,
    `heldout_ceilings.py` and its output, and `band_counts.out.txt`;
  - the review's `check_bessel.py`;
  - `odybench/ephem.py` (its API);
  - the workflow script, to see how this file is used.
- The truth file `controls_real_truth.json`. I read it only to look for
  primaries tuned to the answers, as the task allows. The *Almagest* truth
  file I used only through round 1's leak scanner, which builds its date
  list from it.
- The file list and request lines of `data/ephem/horizons/`. I read no
  values.

**What I deliberately did not do.**
- I evaluated no held-out predicate (H3, H4) at the target.
- I read no value in the target-day Horizons files (`*m1177*`).
- My estimate of how far the *Almagest* sets can narrow a window uses three
  null windows (starting −1500, −1100 and −700) that hold no control date,
  and it reads no truth.

**Tags.**
- [D §n] and [D l. n]: revision 6, section n or line n.
- [AppT n]: Appendix T, item n.
- [rev #n]: `critique-design.md`.
- [r1v5 Nn] and [r1v5 #n]: `critique-design-r1.md`.
- Other dossier tags are as in DESIGN's tag table.
- [me: script]: computed by me with that script in
  `results/critique-design-r2/v6/`, with its `.out.txt` beside it.
- [me]: my own arithmetic or inference, shown where it is used.

**Truth-side content.** DESIGN 10.1 keeps `docs/critique-design*.md` off the
public tier. Even so, this file names no accepted date. Where a truth-side fact
matters it cites Appendix T.

---

## 0. Summary

**Old issues.**
- The first review's 25: all are now resolved in their own terms.
- The 15 issues of [r1v5]: 14 are resolved. **N5 is not resolved in
  substance.** Outcome 4 is still called attainable on a necessary condition
  only. G_j is now computed on the null side, but nothing checks that a
  negative could also produce the eclipse hit that outcome 4 needs.
- None of issues #1–3 is unresolved. The new blocker below concerns gate 3b,
  which #3's fix created.

**New issues: 10 in all, 1 blocker, 2 major and 7 minor.**

**The blocker (N1). Gate 3b cannot measure the method. Its outcome is fixed by
how much B&M-type information each *Almagest* set carries, and at the margin by
an option whose meaning the design never fixes.**
- **Three sets can never be narrowed.** ALM-I, ALM-J and ALM-K are projected
  onto rows so weak that 15–19% of all days pass them in any 136-year window
  [me: `narrowing_3b.py`]. "Seen" needs 5% at most. So no method, however good,
  can ever see these three.
- **Two more fail at the truth.** ALM-G and ALM-H fail on truth-side facts
  [AppT 2].
- **So the gate can pass only if all six remaining sets are seen.** Six is
  exactly its threshold.
- **The sixth set sits on the 5% line.** ALM-B's projection passes 5.2% of
  days if `same_apparition` means only "on that side of the Sun", and 4.4% if
  it also requires the planet to be visible. DESIGN does not say which.
- **Consequences.**
  - Two faithful implementations can return opposite labels.
  - Under the literal reading, 3b fires. The verdict would then say that
    B&M-type matching "cannot see" real records. Yet among the sets that can
    both be narrowed and keep their truth, it misses only ALM-B.
  - The design's own expectations (2.6, 2.10, P21, P27, S0x) misread the gate:
    they treat nine sets as able to count.
  - Gate 3a has the same structure: two of its seven sets can never be
    narrowed. The design admits this in prose, but nothing in the rule
    computes it.

**The majors:**
- **N2. INSTR check I2(c) cannot pass through the interface the design
  specifies.** On the 41-point ΔT grid of `deltat_mix`, P(total) for 1178 BC
  comes out 0.285. The 2.3 table and the exact integral give 0.304, and the
  tolerance is 0.005.
- **N3. INSTR check I16 cannot be run as specified.**
  - Its per-row comparison is undefined when linked events tie.
  - The solver it names is scalar Python, at about 28 ms a call. A site grid
    as written costs over 3,000 core-hours.

**What holds up:**
- **The rule.** It is a pure function of named quantities, and
  `verdict_trace.py` reproduces every label and qualifier of 9.5.
- **The clue files.** They match their hashes. I found no primary feature
  tuned to an answer beyond the five rows already under the exposure audit.
- **The public tier.** Its leak scan finds only the disclosed hit.
- **The held-out test.** The epoch pools and the Fisher p-values reproduce,
  and Q_record follows mechanically from the frozen table.
- **Gate 3a.** It can no longer pass by a choice made after the answers were
  read.

---

## 1. Checks that passed

| # | claim or property | how I checked | result |
|---|---|---|---|
| C1 | Clue-file hashes [D 12.4] | `sha256sum` | `135fba67…83f8`, `18b3ff01…b458`, `be4f511e…9c82`: **match** |
| C2 | No unlicensed feature in the control clue files | Every row of both files, primary and alternatives, against its licence words [me: `dump_clues.py`, `compact_almagest.py`]. `controls_real_truth.json` was read only to see which primaries an answer could have steered | **Nothing new.** The steerable primaries are the five already re-drafted and audited (T1-DARK, T2-SEASON, T-INT-12, D-ECL, L4-DARK), plus drafter widths the rows themselves mark: PB-E1-TIME's upper 2 h, D-SITE's 150 km, X1-TIME's 3 h. No operational field carries an absolute date. The *Almagest* file withholds every Egyptian date; its `ref`s point to dated text rows that the public tier no longer reads. Two small inconsistencies are in N10 |
| C3 | Public tier free of accepted dates [D 10.1, I13(h)] | Round 1's scanner with revision 6's whitelist and the public part of DESIGN: 51 accepted dates in all their printed forms, plus year-only mentions [me: `scan_public_leaks_v6.py`] | **One hit**, the disclosed "−309 Aug 15" in `data-acquisition.md` [AppT 8]. **"−430" is gone** from the public text, so [r1v5 N15c] is fixed |
| C4 | Whitelisted revision-6 scripts hold no truth-side fact | grep of `alm_rows.py`, `pcr_rows.py` and `verdict_trace.py` for set-level outcomes | **Clean.** The only truth-like line is the disclosure value H4 = fail, which is target-side and intended |
| C5 | `data/ephem/` (whitelisted) holds no control date | file names and request lines only | Eclipse excerpts at −135, −584, −708 and −762, and the Horizons spot checks: **no current control**. The target-day files of D5 and D6 are there (see N7) |
| C6 | `verdict_trace.py` transcribes 9.2 | read the script and its output | **Line for line.** The lattice is 0.040 / 0.069 / 0.276 / 1, and Q_record holds on the design-stage null side. S0–S15 match the 9.5 table |
| C7 | R20 and R21's Fisher p-values [D 2.9] | `scipy.stats.fisher_exact` [me: `fisher_check.out.txt`] | 0.0408, 0.0132, 1.000, 0.6916 and 0.7801: **reproduced** |
| C8 | The words-only projection changes exactly the rows 6.3 names | read `pcr_rows.out.txt` against the clue file | **9 rows.** The six solar longitudes go to none; PA-H1/H2/H3-TIME go from pm0.5 to pm1 |
| C9 | Appendix T2b's ceilings | read `heldout_ceilings.py` and its output | Reproduced: 1.793° (IX.7.14), 1.323° (X.1.4), 0.699° (XI.6.2), 0.667° (IX.10.3) |
| C10 | I16's ΔT tie band: the 41-point and 201-point grids "differ by discretisation only, inside the 0.02 band" [D 6.1] | four models at −1176.68 in the canon frame; threshold rows over 26,500–31,000 s; interval rows 200–3,000 s wide [me: `grid_discretisation.py`] | **Holds where it matters.** The largest gap, 0.022, comes at P ≈ 0.3. No flag mismatch falls outside \|P − 0.5\| < 0.02 |
| C11 | The four-model mixture of 2.3 | the same script | The 1178 BC window gives **0.3044** against the table's 0.304 |
| C12 | The site-"none" shortcut is free of ΔT [D 6.3.1] | reasoning | **Correct** for features of local geometry (magnitude, local apparent time, Sun altitude, seasonal hours). A change of ΔT is a rotation of the Earth under the shadow, so "some site passes" does not change |
| C13 | H4's "settled" inference (disclosure rows D1–D2) | reasoning from the numbers DESIGN cites (2.2, 2.5, 7.1); no target-day value read | **Sound.** A Mars within 5° of a Venus 44° west of the Sun would rise more than an hour before it, with the Sun well below Mars' arcus visionis. That would make Mars a conspicuous morning object, which B&M's remark excludes [me] |

---

## 2. The 25 issues of the first review

| # | sev | resolved? | comment |
|---|---|---|---|
| 1 | blocker | **yes** | The rule is a pure function of named quantities. Every condition names its garden, pool and stage (9.1–9.2), and C6 confirms the transcription. Outcomes 1, 2 (both forms), 3a, 3b and inconclusive are reachable on the design-stage null side (S1, S2, S2nm, S3a, S3b, S0). Outcome 4 is honestly marked pending (S4), but its reachability is still judged on a necessary condition (see #71). **Residual, now N1:** label 3b's value is not fixed by the frozen design |
| 2 | blocker | **yes** | The clue file is used exactly as licensed (C1, C2). The scorer's leak [r1v5 N1] is closed: gate 3a takes the minimum over four legs, so no scoring chosen after the answers were read can make it pass. The five exposed rows are re-drafted and audited, and under the minimum they can no longer move the gate. Leftovers are minor (N10a, b) |
| 3 | blocker | **yes, in its own terms** | 3a and 3b are split. Gate 3b holds an *Almagest* control of B&M's own types, scored at B&M's tolerances (Q_BM) and at leave-one-set-out slack. The star season is recorded as untested (fix 4). **But the gate as composed cannot measure the method (N1).** That is a new problem in how 3b is scored, not a return of #3's |
| 4 | major | **yes** | Two-stage git freeze, `PREREG.sha256`, dated amendments; publishing is optional and needs Jon's permission (12.5). The access record now comes first (10.1). One data fetch is mis-scheduled (N4) |
| 5 | major | **yes** | 1.1 attributes the 6 years to C ∧ E. R13 holds the four-clue comparison; R19 reports E-on with exact Poisson intervals |
| 6 | major | **yes** | MacDonald read; conditioning frozen and applied uniformly; both p_fix figures reported |
| 7 | major | **yes** | Three nested, sourced gardens; G_BM primary; greedy fork set (P14) |
| 8 | major | **yes** | F1b; PC-S jitter 0–3 d with decay curves; typical-number parity for the negatives |
| 9 | major | **yes** | C_rel and E_rel outside T0b; the calibration is labelled a fit; P8's near-determined clause is R23 |
| 10 | major | **yes** | Mixture hit strengths; background from −1999; target excluded from its base rates; site-rotated p_e |
| 11 | major | **yes** | Fix 2's "label it non-blind" is now applied by substance. A frozen disclosure table records what was on record before H3 and H4 were frozen. Q_record (null side) prints that the test could not have said "yes" for this target, and Q_contra prints if a measurement contradicts the record. The pools are matched in Mercury event and in epoch. Residuals are minor (N7) |
| 12 | major | **yes** | Vertex at ±1.5 d; rises converged to 0.1 s; flat maxima flagged. I6(a) now uses the review's 0.01-s rises |
| 13 | major | **yes** | The three gaps [r1v5 N4, N6] are closed: observer tables for I5(a); the Standish code retired; I16 added. **New feasibility gaps in the new checks** are N2 (I2(c)), N3 (I16) and N4 (I15(b)) |
| 14 | major | **yes** | Instrument mode and science mode; PC-S feeds no rule. I10's path is Horizons plus the Meeus-based star code |
| 15 | major | **yes** | 12 clean negatives and the Iliad as comparison; storm rule; eclipse-compatible lists filtered consistently |
| 16 | major | **yes** | No LR in the rule; G intervals are the wider of gamma and block bootstrap; I9(b) per side 0.975 − 3 SE |
| 17 | major | **yes** | P6, P8's second clause, P20, P22 and P23 moved to R22–R26; P24, P25 and P27 restated. No remaining counted prediction is fixed by a dossier number. But P21 and P27 now rest on a misread ceiling (N1), and P25 on a necessary condition (#71) |
| 18 | major | **yes** | R_anc under four season bounds of equal prominence, with and without the eclipse |
| 19 | minor | **yes** | One Espenak–Meeus model; four in the mixture |
| 20 | minor | **yes** | A1–A5 are labelled regression tests. The new I5(a) and I15(b) tolerances are derived from measured model differences [acq §1.3] |
| 21 | minor | **yes** | smag pinned to `program.js`; the 1131 BC slip corrected |
| 22 | minor | **yes** | Epoch −1176.68; half-open window; R6 = 1,683 |
| 23 | minor | **yes** | T0 grid kept; T0b's reading in 𝒢_BM*; T0_pass separated from T0 |
| 24 | minor | **yes** | Each slip corrected |
| 25 | minor | **yes** | HIP numbers verified; barycentric Sirius |

---

## 3. The 15 issues of the recheck of revision 5 (DESIGN's #67–81)

| # | r1v5 | sev | resolved? | comment |
|---|---|---|---|---|
| 67 | N1 | blocker | **yes** | Gate 3a fires if any of four legs is below 4 (as licensed and words only, each strict and best fit), so no post-hoc choice can make it pass. Q_score replaces Q_strict, and label 1 is no longer vetoed. **Residual (N1):** the gate now cannot pass for any method on known numbers. 6.3.2 admits this in prose ("a perfect implementation … would still fire"), but no rule quantity computes it |
| 68 | N2 | major | **yes** | Course (b): disclosure table (`heldout_disclosure.json`, frozen at the first freeze), Q_record from the table and the measured lattice, and Q_contra. The table's H4 = fail is a sound inference (C13). Residuals are minor (N7) |
| 69 | N3 | major | **yes** | `data/text/` is off the whitelist. The export holds no *Syntaxis* row and no PC-R historian. I13(i) bars set ids in search code, and 10.1 states honestly what protection is real. One build step now cannot be done from the export (N5) |
| 70 | N4 | major | **yes** | I5(a) uses observer tables (QUANTITIES 4 and 30, airless, fractional seconds) with a tolerance derived from the measured ΔGMST. The Standish code is retired, and I15 compares with an `ephem`-based reference and Horizons. Every INSTR row states its reference's accuracy. **But the same review missed I2(c) (N2), and I15(b)'s data cannot be fetched when 11.2 fetches it (N4)** |
| 71 | N5 | major | **no** | G_j is now computed on the null side, with Q_attain4 and S4 marked pending. **But Q_attain4, P25 and S4's coming realisability still read only the necessary G condition** (0 < G_j and G_j,hi ≤ G_BM,u). hit_j also needs an eclipse-compatible reading whose unique survivor is an eclipse with h_tot ≥ M_Ody. G_j counts reach over the whole garden, mostly non-eclipse readings, so a negative can satisfy the G condition with an eclipse-compatible sub-garden that reaches no eclipse at all. **Fix:** at the null-side stage, also count, for each negative, the core eclipse new moons with h_tot ≥ m̂ that some eclipse-compatible reading makes unique in a 136- or 251-year window. Here m̂ is a frozen proxy for M_Ody, for example the 2.3 value 0.30 or a band 0.2–0.4, since M_Ody itself is target-side. Q_attain4 should hold unless one negative meets both conditions, and constraint C4 should gain the matching clause |
| 72 | N6 | major | **yes** | I16 is an independent evaluator of every counted run, in INSTR, at both stages. Its own feasibility is N3 |
| 73 | N7 | major | **yes** | The words-only projection is defined by rule, frozen, and transcribed (C8), and it enters gate 3a as two legs. The departure (all six longitudes to none) is argued from the rows' own narrative level. Slip in N10a |
| 74 | N8 | minor | **yes** | "At most 8 by construction, fewer if a truth fails its projection" in public text; AppT T2 gives 7; P24 restated |
| 75 | N9 | minor | **yes** | `access.json` and the public copy come first and are logged; tool calls and shell command lines are logged and scanned; I2b runs from `tools/run_i2b.py` into `results/instrument/` |
| 76 | N10 | minor | **yes** | The ΔT-free shortcut is correct (C12). The bench's own search is feasible if vectorised. The reference side is not budgeted (N3) |
| 77 | N11 | minor | **yes** | Epoch-matched pools in the rule and R21 reported. The Fisher p-values reproduce (C7). The band's justification has a mis-citation (N10c) |
| 78 | N12 | minor | **yes** | Leave-one-set-out ceilings by relation class. But the rounding step decides one set (N6) |
| 79 | N13 | minor | **yes** | The star season is recorded as untested in 1.3, 6.4 and every verdict |
| 80 | N14 | minor | **yes** | Per-side coverage 0.975 − 3 SE ≈ 0.965 |
| 81 | N15 | minor | **yes** | (a)–(h) done. The public text no longer prints "−430" (C3), and I13(h) normalises minus signs and matches year forms |

---

## 4. New issues

### Blocker

#### N1. Gate 3b cannot measure the method: three of its eleven sets can never be seen, so the gate passes only if the other six all are, and the sixth turns on an undefined option (blocker)

**Where:** D 6.4 (the projection, regime SL, "the gate", "new vocabulary");
2.6 l. 840–842; 2.10 l. 1331–1332; 9.3 l. 3949–3951; 10.3 `ge_relation`
(l. 4558); P21 (l. 3740); P27 (l. 3762); 9.5 S0x; [AppT 2, 6]. For gate 3a:
6.3.2 l. 2709–2720.

**Evidence.**

- **The rule** [D 6.4, 6.3.2].
  - A set is "seen" when its truth is in the best-fit (or strict) set and that
    set holds at most 5% of the window's candidates. For the *Almagest* sets
    the candidates are days, so 5% of 49,674 is 2,484 days.
  - 3b fires if either leg counts fewer than 6 of the 11 counted sets.
  - Narrowing, |S₀| ≤ 0.05 N_cand, does not depend on the truth. It is a
    property of a set's projection and of the window, so it can be computed
    on the null side.
- **What each projection can do.** I estimated, for every counted set, the
  share of days in a 136-year window that pass all of its projection rows
  under regime SL. The rows are those of `alm_rows.out.txt`. The tolerances
  are those of 6.4 and T2: Mercury 6 d (ALM-G 5 d), Venus 21 d, and the most
  lenient listed value otherwise. The three null windows hold no control date
  [me: `narrowing_3b.py`, `.out.txt`, `.json`].

  | set | projection rows | share of days passing (three windows) | can it narrow to 5%? |
  |---|---|---|---|
  | ALM-A | A.1, A.2, A.5, A.7, A.9 | 0.55–0.60% | yes |
  | **ALM-B** | B.1 (`ge_before_same_apparition`), B.2, B.7 | **5.19–5.25%**; **4.40–4.45%** if the planet must also be visible | **on the line** |
  | ALM-D | D.1, D.3 | 0.76–0.94% | yes |
  | ALM-E | E.1, E.3 | 0.07–0.12% | yes |
  | ALM-F | F.1, F.3 | 1.03% | yes |
  | ALM-G | G.1, G.3 | 0.67–0.78% | yes (truth fails [AppT 2]) |
  | ALM-H | H.1, H.4, H.8 | 4.37–4.59% | yes (truth fails [AppT 2]) |
  | **ALM-I** | I.1 (`ge_after_same_apparition`) only | **19.1%** (14.8–15.0% with visibility) | **never** |
  | **ALM-J** | J.1 (Mars before sunrise), J.4 (`ge_before_same_apparition`) | **15.7–16.5%** (13.6–13.9%) | **never** |
  | **ALM-K** | K.1, K.4, K.7 (visibility only) | **14.9–15.0%** | **never** |
  | ALM-L | L.1, L.4, L.6 | 0.76–0.92% | yes |

  The estimate is rough. It uses one geocentric sample a day, events located
  to the day, analytic rise leads at Alexandria, and dawn at the Sun −8°. The
  three "never" rows exceed the line three- to fourfold, far beyond any of
  those errors. ALM-B's row is the one that the approximations, and the
  reading of one option, can move across the line.
- **The ceiling.**
  - ALM-I, J and K are never seen, whatever the method and whatever the
    window.
  - ALM-G and ALM-H fail their truths in regime SL [AppT 2].
  - **So seen_ALM_SL ≤ 6.** 3b fires unless ALM-A, B, D, E, F and L are all
    seen.
  - Five of them narrow comfortably and keep their truths [AppT 2]. **So the
    gate's verdict is ALM-B's narrowing.**
- **That narrowing turns on an option nobody has defined.**
  - B.1's projected option is `ge_before_same_apparition`, operational
    `{"bound": "same_apparition"}`.
  - DESIGN lists `same_apparition` as vocabulary "the harness must implement"
    (l. 3125). 10.3 gives only the type's parameters (l. 4558).
  - The row's statement calls Venus "a morning star", which is a phrase, not
    an operational condition.
  - Is an apparition bounded by conjunctions, or by first and last
    visibility? Must the planet be visible on the day?
  - **Read as "on that side of the Sun", ALM-B passes 5.2% of days, is not
    seen, and 3b fires (seen = 5). Read with visibility, it passes 4.4%, is
    seen, and 3b passes (seen = 6).** The window position moves the share by
    less than 0.1 percentage point; the reading moves it by 0.8.
- **The design misreads its own gate.**
  - 2.6 says the truth is retained in 9 sets and that narrowing "has not been
    computed; that is what gate 3b still tests". 2.10 says "Only narrowing is
    open (P21)".
  - P21 predicts that at least 6 of those 9 narrow. Three of them cannot, so
    P21 needs all six of the rest.
  - P27 and S0x expect no 3b. Under the literal reading, 3b is the expected
    outcome.
  - 9.3 says the 5% narrowing and the thresholds, though set after the
    truth-side check, "cannot be what makes a gate pass" under the family of
    legs. That holds for 3a. It does not hold for 3b: its two legs agree
    (6.4), so the family protects nothing there, and the 5% line is exactly
    what decides ALM-B.
- **Gate 3a has the same structure, disclosed in prose only.**
  - R-THUC and R-XEN have "none" site primaries and "no method can narrow
    them" [D 6.3.2], so 3a's ceiling is 5 of 7.
  - On the strict legs, the record errors of R-PTOL-BAB and R-PYDNA [AppT 6]
    cap the count at 2 or 3.
  - 6.3.2 says the verdict will note that "a perfect implementation … would
    still fire the gate". But no quantity in 9.1 and no line in 9.2 computes
    that, so the note is either a static sentence or absent.

**Why it is a blocker.**
- **Label 3b is a headline label, and the frozen design does not determine
  it.** Two faithful implementations of revision 6, differing only in what
  "same apparition" means, return opposite labels on the same sky.
- **Under the literal reading, the verdict would be wrong about the method.**
  It would print that the B&M-type component "does not recover the dates of
  real planetary and lunar records of B&M's own kinds". In fact it recovers
  five of the six sets that can both be narrowed and keep their truth, and
  misses only the one on the line. Of the other five sets, three fail for lack
  of information that no method could supply, and two on known record
  specifics [AppT 2].
- **The bench's founding rule needs the gates to measure sight.** These gates
  measure the composition of the control sets, and the design does not know
  that, for 3b.

**Fix.** Nothing below relaxes a gate or favours "the method can see".
1. **Freeze the meaning of `same_apparition`** in 10.3 and
   `operational_map.json`:
   - what bounds an apparition (consecutive conjunctions, or first and last
     visibility at a stated arcus visionis);
   - whether the body must be visible that day;
   - at which instant it is judged.

   Report the other reading as a sensitivity.
2. **Make each gate's attainability a null-side quantity.** I16(a) already
   evaluates every counted set in 21 random null windows. From those, record
   for each set and leg whether |S₀| (or |B|) ≤ 0.05 N_cand in a majority of
   windows. Freeze `narrowable[gate][leg]` at the second freeze, in
   `attain.json`.
3. **Add Q_attain3a and Q_attain3b.** Each holds when fewer counted sets can
   be narrowed than the gate's threshold. When one holds, the verdict prints
   that component as "untested by these controls" rather than "cannot see",
   and the dependent "no"s stay "could not have seen it". This mechanises
   6.3.2's sentence about a perfect implementation, and it gives 3b the same
   disclosure.
4. **Restate** 2.6, 2.10, P21 (6 of the 6 sets that can both narrow and keep
   their truth), P27 and S0x (under the literal reading, {3a, 3b}), and 9.3's
   sentence about the thresholds and the 5% narrowing.
5. **Optionally,** recompose gate 3b now from the sets whose projection can
   narrow, by a rule that uses only that null-side property. Record that the
   two truth-side failures (ALM-G and ALM-H) were known when the rule was
   written, and keep the present gate beside it.

### Major

#### N2. INSTR check I2(c) cannot pass through the mixture interface the design specifies (major)

**Where:** D 6.1 I2 (c); 10.4, the `deltat_mix.py` row; 10.2 `deltat_mix`
(l. 4376–4381); 6.3.3; 4.4.

**Evidence.**
- **The check.** I2(c) compares `deltat_mix.py` with the 2.3 table and a
  10⁶-draw Monte Carlo, and asks P(total) "per model and for the mixture
  within 0.005".
- **The interface.** 10.2 gives `deltat_mix` two functions only:
  - `grid(..., n=41)`, 41 points over ±4σ per model with Gaussian weights;
  - `p_pass(fn, …)`, which sums those weights over the points where `fn`
    passes.
- **The numbers.** For the 1178 BC totality window at Ithaki (28,805–29,580
  s, canon frame) and the four models of 2.3 [me: `grid_discretisation.py`]:
  - the exact mixture is **0.3044**, reproducing 2.3's 0.304;
  - the 41-point grid gives **0.2849**, off by **0.0195**, four times the
    tolerance;
  - over interval rows 200–3,000 s wide the grid's error reaches 0.043.
- **Where the exact value comes from.** h_tot "integrates each model's
  Gaussian over the totality window" (4.4), which is exact. But I2(c) names
  `deltat_mix.py`, whose only estimator is the grid.
- **So a correct implementation of the specified interface fails INSTR**, and
  `verdict.py` would then refuse to run [D 9.2].

**Fix.**
- Either add an exact interval integrator to `deltat_mix` (Φ differences
  between the ΔT values where a row's outcome changes, found by bisection, as
  h_tot does) and test that in I2(c);
- or test the grid against its own discretisation bound. That bound is about
  0.02 for threshold rows and 0.04 for interval rows at these σ.

State which definition the control rows' frozen P_mix uses. On the evidence of
C10, I16's 0.02 band can stay.

#### N3. INSTR check I16 cannot be run as specified (major)

**Where:** D 6.1 I16; 6.3.1 (linked events; site "none"); 10.2
`tests/control_reference.py`; 10.4; 11.2 steps 6 and 16.

**Evidence.**
- **(a) The per-row comparison is undefined under ties.**
  - I16 requires "per-row pass flags and f(c) identical for every candidate".
  - For linked sets the search takes, for each anchor, "the linked event that
    fails fewest rows" (6.3.1).
  - When two linked events tie on f but fail different rows, the candidate's
    per-row flags depend on a tie-break that the design does not specify.
  - This is plausible in R-THUC: a ±0.5-year war-year window holds two or
    three solar eclipses, and one may fail the season row while another fails
    a magnitude row. A correct pair of implementations can then disagree
    outside every listed tie band, and INSTR fails.
- **(b) The named reference solver cannot cover the specified search in the
  stated time.**
  - I16 uses `results/critique-design/check_bessel.py` with "its own site
    grid" for unstated sites.
  - That solver is scalar Python: each local maximum scans ±4 h at 0.002-h
    steps.
  - One call takes **about 28 ms** [me: `bessel_timing.py`].
  - A 1° grid of about 2×10⁴ cells, over about 330 solar eclipses per
    136-year window, then costs about 50 core-hours per window.
  - Over I16(a)'s 21 windows and the three site-"none" solar events (T1, T2,
    X2), that is **over 3,000 core-hours**, against 2–4 h for all of step 6.
- **What would still work.** An early-exit or analytic search would not need
  this, because most site-free rows pass at the greatest-eclipse point. But
  the design does not say so.
- **How the two site searches are compared is unspecified.** The tie bands are
  stated on row values, not on site discretisation.
- **A path problem.** The solver reads its elements from `data/refs/nasa/`,
  which is off the public whitelist. A7 must point it at `data/jsex/`.

**Fix.**
- Specify a deterministic tie-break for linked events, for example the
  earliest. Or compare only f(c) and the seen and strict flags, plus the
  per-row flags of unlinked rows.
- Require the reference to decide site-free rows from the eclipse's extremal
  geometry, with early exit, or a vectorised solver. Budget it in 11.2.
- Point the reference at `data/jsex/`.

### Minor

#### N4. I15(b)'s Horizons data cannot exist when 11.2 fetches it (minor)

- **The schedule.** 11.1 and 11.2 fetch Horizons geocentric tables for "every
  P_BM member" at step 0, before the first freeze.
- **The conflict.**
  - P_BM is the survivor set of 𝒢_BM* over the background. 12.1 item 15
    forbids computing it before the freeze.
  - It exists only at step 6, inside `attain.py`.
  - Fetching there means network calls under frozen code, writing into a data
    directory that 12.2 neither commits nor lists among the hashed files.
- **Fix.** Either fetch for a superset that needs no reading (for example
  every C_rel spring candidate, about 2,300, in TLIST batches), or let
  `attain.py` fetch into `results/attain/` (committed at the second freeze)
  and say so in 11.2 and 12.3.

#### N5. A3 cannot build the re-draft brief from the public export (minor)

- **What the brief needs.** 6.3.4 says `tools/make_redraft_brief.py`, written
  by A3 (public tier), writes the brief with the five rows' "cited text rows,
  in full". It also says A3 drafts the sibling pairs "from the clue file and
  the cited rows".
- **What the export holds.** It has no PC-R historian (10.1).
- **Why A3 cannot do it.** `check_access.py` flags any "script the agent wrote
  or ran that names such a path" (l. 4246). So A3 can neither read those rows
  nor write a tool that does without failing I13(h).
- **Fix.** Either a truth-tier agent runs the brief tool, or the export
  includes the handful of cited rows. They are Thuc. 2.28, 2.47.1, 4.51.1,
  4.52, Diod. 20.5.5 and Livy 38.36.4; none states an absolute date. The
  sibling pairs can use the licence words alone, as 10.1 already says for A9.

#### N6. The held-out ceiling's rounding step alone keeps ALM-B's truth inside a held-out row (minor)

- **The rule.** 6.4 rounds held-out ceilings "up to the next 0.1°". Revision 6
  wrote that step with the truth-side slack table already computed
  (`heldout_ceilings.py`, [AppT T2b]).
- **The case it decides.**
  - ALM-B's planet–Moon ceiling comes from IX.10.3, 0.667°, which rounds up to
    0.7°.
  - ALM-B's own record XI.6.2 (row B.5) lies 0.699° off [C9].
  - Unrounded, or rounded to 0.01°, B.5 fails at the truth.
- **Why it matters.** Q_H needs 6 of the 7 sets that can qualify (P24), so one
  set is the whole margin.
- **Fix.**
  - Record that the step was chosen after the slack table existed.
  - Take Q_H against the claim across the rounding steps 0.01°, 0.05° and 0.1°,
    as 6.3.2 takes gate 3a across its legs, or fix the step by a rule written
    without the table.
  - Report B.5's margin.

#### N7. The disclosure table promises values stay unread that the whitelist serves, and lists facts computed after the freeze (minor)

- **The promise.** 7.1 and 12.1 item 9 say nobody reads a value the table
  marks "constrains" before the second freeze.
- **The whitelist.**
  - D3 (B&M's Fig. 1 magnitudes, `research-bm2008.md` l. 596) is on the public
    whitelist.
  - So is D5 (the Day −6 Horizons file, in `data/ephem/`).
  - `check_access.py` flags only paths outside the whitelist, so the promise
    cannot be checked.
- **Post-freeze facts in D2.** D2 cites rev V10's 103.6 min (written 21:02 on 3
  Oct) and unread §2.5's 44.3° (4 Oct), both after the 20:25 freeze. B&M's
  published 1:42:56 lead suffices for the inference.
- **Fix.**
  - Either take `data/ephem/horizons/*m1177*` and the two notes' Fig. 1 lines
    off the public tier (export masked copies), or drop the promise and say
    the values were readable.
  - Mark D2's post-freeze items as corroboration, not record.

#### N8. Outcome 4 compares the negative's upper bound with the Odyssey's point value (minor)

- **What 9.3 says.** "Bounds work against the claim being made."
- **What the rule does.** Label 4 fires when G_j,hi ≤ G_BM,u, where G_BM,u is
  the point value.
- **Why that matters.** The claim is that fiction is dated at least as
  significantly as the Odyssey. Against it, the Odyssey's side should be its
  lower bound.
- **The size of the gap.** Under v1 the scaled interval is about
  0.00107–0.00264 around 0.00172 [D 2.9, scaled by n_A/n_T], so the
  comparison is up to 1.6 times looser than 9.3 implies.
- **Fix.** Compare with G_BM,u,lo, or say why the point value is used. The
  same applies to Q_attain4.

#### N9. With no gate veto, label 1's exchangeability checks condition nothing (minor)

- **The assumption.** Label 1 now rests only on p_H being exact. That holds if
  some pool is exchangeable with the target, an eclipse new moon.
- **The checks.** P10 (eclipse status), R20 (Mercury event) and R21 (epoch)
  test this. But they are a counted prediction and two reported expectations,
  so a failure leaves label 1 standing unqualified.
- **Fix.** Add a qualifier, printed beside label 1, when P10 fails for H3 or H4
  or when R21 shows drift inside the epoch band.

#### N10. Slips (minor)

- **(a)** 6.3 says the Babylonian records' times keep their primaries,
  "primary 'record'", for PB-E1, E2 and E3-TIME. PB-E2-TIME's primary is
  `mid-at-midnight`, justified as "Ptolemy's reading of the record". The
  record's own literal option is `in-progress`. The truth passes either, so
  the gate does not move, but the words-only rule should say which it keeps.
- **(b)** A-MONTH's primary (R-ARBELA) maps Boedromion and Pyanepsion through
  a modern reconstruction of the Attic calendar. That is the one
  outside-knowledge primary in a counted set (policy 2; [lcr flagged item
  1]). The words-only projection, whose principle is "what the words carry",
  keeps it. Without it R-ARBELA would sit near the 5% line. By a hand
  estimate: about 120 umbral eclipses deeper than 0.5 fall in 136 years, the
  timing rows keep roughly one in eight, and that is about 15 against a bound
  of about 16 [me, rough]. Gate 3a's decision would not move, because it
  fires on the as-licensed strict leg either way. Name the exception, and
  report the words-only legs with A-MONTH at "none" as a sensitivity.
- **(c)** "±700 years … is the band of P8's stationarity test" (2.9, 7.2). P8
  compares the first and last 700 years of the background, not a band around
  the target. Also record that the width was chosen with the ±350-year floor
  (0.067, which would make outcome 1 unattainable) in view.
- **(d)** 9.2 defines CP_hi, which the rule never uses.

---

## 5. What I could not check

- **ALM-B's exact narrowing** under the bench's own instants, apparition
  definition and window. My estimate puts it within a percentage point of the
  line either way, and that is the finding. The bench's own number decides
  the label.
- **R-THUC's and R-XEN's narrowing.** I took the design's statement that their
  "none" sites keep S₀ above 5%. A hand estimate agrees. For R-THUC, about
  330 solar anchors, the half-year season, a solar eclipse 7 ± 0.5 years on
  and a lunar one 18 ± 0.5 years on leave about 35 survivors, against a bound
  of about 16 [me, rough].
- **Whether the bench's lunar module moves R-PTOL-BAB's magnitudes** [AppT 3].
  That cannot change 3a's firing. Even with R-PTOL-BAB passing, the
  as-licensed strict leg is capped at 3 by R-PTOL-ALEX's computed mid-time
  and R-PYDNA's word rows [AppT 3, 6].
- **Horizons' TLIST limits** for I5(a)'s 21,000 epochs. I relied on the
  design's description.
- **SMH2016 Table S4.** Not read; it is a pre-freeze task.
- **H3 and H4 at the target.** Not computed, on purpose.

## 6. Files produced for this review

All are in `C:\Projects\odybench\results\critique-design-r2\v6\`. The earlier
recheck's scripts, one level up, are untouched.

| script | what it does | output |
|---|---|---|
| `dump_clues.py` | readable dumps of both control clue files | `dump_real_v6.txt`, `dump_almagest_v6.txt` |
| `compact_almagest.py` | one block per *Almagest* row: statement, licence, every option's parameters | `compact_almagest.txt` |
| `narrowing_3b.py` | null-side share of days passing each counted set's B&M-type projection under regime SL, in three null windows, with and without visibility in `same_apparition` (N1) | `narrowing_3b.out.txt`, `.json` |
| `grid_discretisation.py` | the 41-point ΔT grid against the exact mixture and a 201-point grid (N2, C10, C11) | `grid_discretisation.out.txt` |
| `bessel_timing.py` | the cost of `check_bessel.py`'s local maximum on a site grid (N3) | `bessel_timing.out.txt` |
| `scan_public_leaks_v6.py` | round 1's leak scanner with revision 6's whitelist (C3) | `scan_public_leaks_v6.out.txt` |
| `fisher_check.py` | Fisher exact p for R20 and R21 (C7) | `fisher_check.out.txt` |
