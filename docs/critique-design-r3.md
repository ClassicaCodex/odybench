# Adversarial review of DESIGN.md, revision 7 (recheck, round 3)

Written 2026-10-04 by a reviewer who did not write DESIGN.md or any earlier
review. Scope: `DESIGN.md` revision 7 (all 6,312 lines, Appendix T included;
SHA-256 `4151842d…4cf2`), judged against:
- the 25 issues of `docs/critique-design.md`;
- the recheck of revision 6, `docs/critique-design-r2.md` ([r2v6]). That means its
  ten new issues N1–N10, which DESIGN numbers 82–91, and its finding that #71
  was not resolved.

I also searched for new problems.

**What I read.**
- In full:
  - `DESIGN.md`;
  - `docs/critique-design.md`;
  - `docs/critique-design-r2.md`;
  - every row of `controls_real.json`, through my own dump and by hand;
  - in `controls_almagest.json`, every row of the gate's projection and
    every moon-phase row by hand; the other rows by machine only.
- In part:
  - `docs/license-check-almagest.md`, its "next stage" items 3–7;
  - revision 7's scratch outputs: `verdict_trace.py` and its output,
    `check_design.out.txt`, `pcr_rows.out.txt`, and `heldout_exch.py` with its
    output;
  - [r2v6]'s `narrowing_3b.py` and its output;
  - the first review's `check_p19.py` and `check_bessel.py`;
  - the six PC-R text rows that revision 7 adds to the public export.
- Not read: `docs/critique-design-r1.md`. I know it only through DESIGN 14.5
  and [r2v6] §3.

**What I deliberately did not do.**
- I opened neither truth file. The clue files are byte-identical to the
  versions that [r2v6 C2] checked against the truth (C1 below). So for
  primaries tuned to answers I rely on that check. I looked for unlicensed
  features from the files and the texts alone.
- I evaluated no held-out predicate at the target. My one target-side
  computation is its eclipse's totality window, a public design-stage number
  (2.3), as the first review computed it.
- Where a truth-side fact matters I cite Appendix T. I name no accepted date.

**Tags.**
- [D §n] and [D l. n]: revision 7, section n or line n.
- [AppT n]: Appendix T, item n.
- [rev #n]: `critique-design.md`.
- [r2v6 Nn], [r2v6 #n] and [r2v6 Cn]: `critique-design-r2.md`.
- [lca2 item n]: `docs/license-check-almagest.md`, its "next stage" list.
- [me: script]: computed by me with that script in
  `results/critique-design-r3/`, with its output beside it.
- [me]: my own arithmetic, shown where it is used.

A later revision could number this file's issues R3-1 to R3-11 as 92–102.

---

## 0. Summary

**Old issues.**
- **The first review's 25:** all remain resolved in their own terms. Revision
  7 undid none of them. Its residuals on #3, #13, #15 and #17 are new issues
  below.
- **[r2v6]'s ten (#82–91):** all are resolved in their own terms. Their
  residuals are new issues below:
  - #82 (N1) leaves R3-1, R3-4, R3-5 and R3-8;
  - #83 (N2) leaves R3-3;
  - #84 (N3) leaves R3-6 and R3-7;
  - #88 (N7) leaves R3-9.
- **#71 is still not resolved in substance** (R3-2). Revision 7 adds the
  eclipse condition that [r2v6] proposed, E_j. But E_j counts eclipses
  anywhere in the 1,698-year core, while label 4 can only fire inside the
  Odyssey's two fixed windows. So Q_attain4 still reads a necessary
  condition.

**New issues: 11 in all, no blocker, 3 major and 8 minor.** None makes the
verdict uncomputable once fixed before the freeze. None is expected to flip a
label on the known numbers.

**The majors:**
- **R3-1. Gate 3b's projection keeps three lunar phases that the clue file
  says are not in the words.**
  - A.2, A.5 and B.2 are inferred from planet–Moon proximity, and A.5 also
    from an opposition. The gate itself holds out both of those as not in
    B&M's grammar.
  - 6.4's own rule is words alone. Under it, ALM-A passes **4.88–4.90%** of a
    window's days instead of 0.6% [me: `narrowing_inferred_phase.py`].
  - So gate 3b's expected pass would rest on two knife-edges, ALM-A and
    ALM-B, not one. As designed, ALM-A's margin comes from rows that favour
    "the method can see".
- **R3-2. Q_attain4 measures the eclipse condition over the core, but label
  4 is scored only in two fixed windows.**
  - An eclipse made unique in some other century satisfies E_j and can never
    fire label 4.
  - Both parts of outcome 4 are null-side once m̂ stands in for M_Ody, so the
    exact attainability can be computed at the second freeze.
  - The design's allowance of "about 11 reach-units" is the bound itself. The
    count it allows is about 4 targets.
- **R3-3. I2(c) still cannot be met reliably by a correct implementation.**
  - The 2.3 table integrates the first review's 5-s-grid totality window.
  - Over the continuous window, the SMH2016 parabola gives **0.5030** against
    the printed 0.498. That gap of 0.0050 is exactly I2(c)'s tolerance, where
    the design budgets "about 0.003" [me: `i2c_table_gap.py`].
  - Two further conflicts: the synthetic cases' 10⁻⁴ tolerance contradicts
    the design's own sub-step loss of up to 0.007, and its own bisection
    bound of 0.0004.

**What holds up:**
- **The rule.** It is still a pure function of named quantities, and
  revision 7's trace transcribes it line for line (C4).
- **The meaning of `same_apparition`.**
  - The frozen meaning is the one [r2v6] estimated, with lead or lag at
    least 30 min. It gives 30 min in both regimes, as stated (C6).
  - It has a sound textual basis. The file calls `visible_only` these rows'
    minimal reading, and every such row records a sighting.
- **The other projected rows.** Every other projected *Almagest* row is
  licensed by its words (C8).
- **The six text rows.** The rows added to the public export state no
  absolute date (C3).
- **Q_exch.** Its inputs reproduce (C5).
- **The clue files.** They match their hashes. My scan finds every licence
  string verbatim and no date in any operational field (C1, C2).

---

## 1. Checks that passed

| # | claim or property | how I checked | result |
|---|---|---|---|
| C1 | Clue-file hashes [D 12.4] | `sha256sum` | `135fba67…83f8`, `18b3ff01…b458`, `be4f511e…9c82`: **match**, so these are the files [r2v6 C2] checked against the truth |
| C2 | Licence words verbatim; no date in operational fields [D 2.9, I13(a)] | Every licence fragment against its cited row, comparing raw characters. Every operational value, and every *Almagest* statement and note, scanned for signed or BC/AD years, JD-like numbers, Olympiads and the Nabonassar era [me: `scan_clues.py`] | **PC-R:** 125/125 verbatim. ***Almagest*:** 100/100 text fragments verbatim; the other 18 are the interval rows' bracketed placeholders for the withheld Egyptian dates, by design. **No date-like value** anywhere. The drafter's widths that [r2v6 C2] listed (PB-E1-TIME's upper 2 h, D-SITE's 150 km, X1-TIME's 3 h) are as recorded |
| C3 | The six PC-R rows added to the public export state no absolute date [D 6.3.4, 10.1] | Printed Thuc. 2.28.1, 2.47.1, 4.51.1 and 4.52.1, Diod. 20.5.5 and Livy 38.36.4 from `data/text/` | **True.** They give war-year counts (the first, and the seventh, year of the war ended), "the next day" and Livy's hour. No consul, archon or era appears |
| C4 | Revision 7's trace transcribes 9.2 [D 9.5] | Read `verdict_trace.py` against 9.2, and its output | **Line for line**, including `fire3b_other`, Q_attain3a, Q_attain3b, Q_exch, G_BM,u,lo and E_j; the 28 sets reproduce 9.5. One slip in R3-11 |
| C5 | Q_exch's inputs [D 2.9] | `scipy.stats.fisher_exact` [me] | Band halves 0.289, 0.235, 0.173 and 0.464. P10, any eclipse: 0.244 and 0.706. Ionian-visible: 0.179 and 0.786. **Reproduced.** `heldout_exch.py` removes the target before any computation and prints no target value |
| C6 | The frozen meaning is the one the recheck estimated, at "30 min in both regimes" [D 6.4, 10.3] | `narrowing_3b.py`'s visibility proxy; the `visible_only` lists of A.1, B.1, I.1 and J.4 | The estimate used a lead or lag of at least 30 min. Every list is [30, 60]: the most lenient value (SL) and the lower middle (BM) both give 30. **Consistent** |
| C7 | ALM-B narrows to about 4.4% under the frozen meaning [D 2.6] | [r2v6]'s machinery rerun on its three null windows [me: `narrowing_inferred_phase.py`] | **4.40–4.45%.** B.7 (last quarter, +55 d, ±2 d) implies B.2's waning crescent, so B.2 adds nothing to ALM-B's narrowing |
| C8 | The other projected *Almagest* rows are licensed by their words [D 6.4] | Every projected planet, equinox and visibility row read against its licence | **Yes.** The drafter keeps Ptolemy's own inferences, the "γέγονεν ἄρα" (therefore) of H.1, H.4, H.8, K.1 and K.7, at `visible_only`. The exceptions are R3-1's three phase rows |
| C9 | G_BM,u,lo [D 2.9] | 0.087 × 131/10,690 | 0.001066: **reproduced** |
| C10 | The words-only projection [D 6.3] | `pcr_rows.out.txt` against the options in the clue file | **10 rows.** PB-E2-TIME goes to `in-progress` by clause 3; A-MONTH is named; R-PTOL-CHAIN's own rows are unchanged |
| C11 | 1131 BC's column of the 2.3 table under I2(c) | Continuous totality window by bisection, then per-model P(total) [me: `i2c_table_gap.py`] | **Within 0.0029** of every printed value. Contrast R3-3 for 1178 BC |

---

## 2. The 25 issues of the first review

| # | sev | resolved? | comment |
|---|---|---|---|
| 1 | blocker | **yes** | The rule is a pure function, every condition names its garden, pool and stage, and the trace reproduces it (C4). Outcomes 1, 2 (both forms), 3a, 3b and inconclusive are realisable on the design-stage null side; 4 is honestly pending. Residuals: Q_attain4 reads the wrong scope (R3-2), and Q_attain3a or Q_attain3b can contradict a gate that passed (R3-8) |
| 2 | blocker | **yes** | The PC-R file is used exactly as licensed (C1, C2), and gate 3a is taken over four legs. The residual concerns how the *Almagest* file is used, not answers copied into PC-R: R3-1 |
| 3 | blocker | **yes, in its own terms** | 3a and 3b are split, and the *Almagest* gate tests B&M's own kinds, with the star season recorded as untested. **Residual R3-1:** the gate's projection reads three phase classes that come from held-out relations, not from words |
| 4 | major | **yes** | Two-stage git freeze, `PREREG.sha256`, dated amendments; publishing needs Jon's permission |
| 5 | major | **yes** | 1.1 attributes the 6 years to C ∧ E; R13 and R19 |
| 6 | major | **yes** | MacDonald read; conditioning frozen and applied to C, V, M and E |
| 7 | major | **yes** | Three nested, sourced gardens; 𝒢_BM* primary |
| 8 | major | **yes** | F1b, PC-S jitter 0–3 d, and parity for the negatives |
| 9 | major | **yes** | C_rel and E_rel outside T0b |
| 10 | major | **yes** | Mixture hit strengths; background from −1999; target excluded from its base rate. Note: the printed M_Ody of 0.304 is the 5-s-grid value; the exact integral is about 0.308 (R3-3) |
| 11 | major | **yes** | Disclosure table, Q_record, matched pools, and now Q_exch |
| 12 | major | **yes** | Vertex at ±1.5 d, flat maxima flagged, I6(a) on 0.01-s rises |
| 13 | major | **yes** | Every rule input has a second path, and I16 now has a deterministic tie-break, witness sites and a vectorised reference. Residuals R3-3, R3-5, R3-6 and R3-7 concern whether the checks can be met, not missing paths |
| 14 | major | **yes** | Instrument and science modes; PC-S feeds no rule |
| 15 | major | **yes** | Twelve clean negatives and the storm rule. Whether outcome 4 can fire is R3-2 |
| 16 | major | **yes** | No LR in the rule; G intervals the wider of two |
| 17 | major | **yes**, one residual | P10's held-out part moved to R29 because its rough values were known. **Residual R3-4:** by the same rule P21 is now nearly fixed by known numbers |
| 18 | major | **yes** | R_anc under four ancient season bounds |
| 19 | minor | **yes** | One Espenak–Meeus model, four in the mixture |
| 20 | minor | **yes** | A1–A5 are labelled regression tests. One accuracy statement in I2 is wrong (R3-3, R3-11) |
| 21 | minor | **yes** | smag pinned to `program.js` |
| 22 | minor | **yes** | Epoch −1176.68; half-open window |
| 23 | minor | **yes** | T0 grid; T0b's reading is in 𝒢_BM* |
| 24 | minor | **yes** | Slips corrected |
| 25 | minor | **yes** | HIP numbers verified; barycentric Sirius |

---

## 3. The recheck of revision 6: #71 and N1–N10 (DESIGN's #82–91)

| # | r2v6 | sev | resolved? | comment |
|---|---|---|---|---|
| 71 | (r1v5 N5) | major | **no** | E_j is added as [r2v6] proposed. But hit_j can fire only in the reproduction and primary windows at their fixed positions (6.5), and E_j counts any window over the core. So Q_attain4 still reads a necessary condition, and can stay silent when outcome 4 is impossible (R3-2) |
| 82 | N1 | blocker | **yes, in its own terms** | **Fixes.** `same_apparition` is frozen, on textual grounds that hold (C6). Narrowability is a null-side quantity, with Q_attain3a and Q_attain3b. Each gate gets a per-set breakdown, and the label now reads "not shown to see". 2.6, 2.10, P21, P27, S0x and S0y are restated. **Residual 1:** the frozen meaning is the one that lets gate 3b pass, and it was fixed with both the narrowing and the truths known. 9.3 takes every other post-hoc choice against the claim; this one is only disclosed, through Q_score. I accept that, because the side-only meaning is the textually weaker reading. **Residual 2:** the projection still holds three inferred rows (R3-1). **Further residuals:** P21 is nearly determined (R3-4); Q_attain can contradict a passing gate (R3-8); "visible on Day 0" is mis-worded (R3-5) |
| 83 | N2 | major | **yes** | `p_exact` is an exact integrator, and the 41-point grid leaves every rule input. But I2(c)'s comparison with the 2.3 table now sits on its tolerance, for another reason (R3-3) |
| 84 | N3 | major | **yes** | Earliest-instant tie-break on both sides; `bessel_vec.py` with early exit; `data/jsex/`; a budget. Residuals: whose site-search miss fails INSTR (R3-6), and null windows that run past the data (R3-7) |
| 85 | N4 | minor | **yes** | `attain.py` fetches the tables into `results/attain/horizons/` at the null-side stage, and the second freeze commits them |
| 86 | N5 | minor | **yes** | The export holds the six cited rows, and none states an absolute date (C3) |
| 87 | N6 | minor | **yes** | Three rounding steps; Q_H and gate 3b take their decisions against the claim across them. For 3b a finer step only narrows a tolerance and loses no truth [AppT 2], so the coarse leg decides. T2b records B.5's failure at the fine step |
| 88 | N7 | minor | **yes for D3 and D5** | **Done:** a sealed list, a masked export, an access check over both tiers, and `run_i1.py` printing only the summary. D2's post-freeze items are marked as corroboration. **Residual:** D4, also marked "constrains", is printed in the public design itself (R3-9) |
| 89 | N8 | minor | **yes** | Outcome 4 and Q_attain4 now read G_BM,u,lo = 0.00107 (C9), and S4b shows the change. What that bound allows is misstated (R3-2) |
| 90 | N9 | minor | **yes** | Q_exch is a null-side qualifier printed beside label 1, and its inputs reproduce (C5). Six uncorrected tests at 0.05 fire by chance up to about a quarter of the time, as 7.2 says. A Holm-adjusted family would make "in doubt" mean more. That is a choice, not an error |
| 91 | N10 | minor | **yes** | (a) Clause 3 sends PB-E2-TIME to `in-progress` (C10). (b) A-MONTH is named and reported at "none". (c) The band's history is corrected. (d) CP_hi is removed |

---

## 4. New issues

### Major

#### R3-1. Gate 3b's projection keeps three lunar phases that the clue file says are not in the words (major)

**Where.**
- D 6.4, the B&M-type projection: its rule is "each from its words alone, as
  the Odyssey's clues are", and it says "A.2, A.5, B.2 and B.7 need no
  coordinates and stay".
- 2.6, the narrowability bullet; 2.10; P21; R28.
- [AppT 2], "Narrowable and retained"; [AppT 6], P21.
- I13(f), through `alm_rows.py`.

**Evidence.**
- **The rule.** 6.4 builds gate 3b from rows of B&M's kinds, each from its
  words alone. It sets A.10, B.5 and B.9 to "none" because their phase comes
  from numbers, while the Odyssey's phase clue is a phrase (14.161–162).
- **What the clue file says about three of the rows that stay.** A.2, A.5
  and B.2 are moon-phase rows whose primary is a phase class:
  - **A.2, young crescent.** The Moon stands beside Mercury, an evening
    star, and Mercury is never far from the Sun. The drafter calls it "my
    inference".
  - **A.5, near full.** The Moon stands beside Mars, which was at opposition
    about three days before. Also "my inference".
  - **B.2, waning crescent.** Venus stands between β Sco and the Moon, and is
    past its greatest morning elongation. "Drafter's inference".
  - **The file's own verdict.** Each row's "none" option says that the
    Moon's phase is not stated in words. The file's first rule says that
    phases inferred from proximity are forks with a "none" option.
  - **The licence check's verdict.** It calls them "the other inferred
    phases", and offers word-derived phases only as the design's choice
    [lca2 item 4].
- **Where the inference comes from.**
  - Each rests on a planet–Moon position. 6.4 sets those to "none" in the
    gate, "because they are not in B&M's grammar", and holds them out for
    Q_H.
  - A.5 also rests on Mars' nearness to opposition. That is A.4 ("Mars was
    at opposition … about three days before this day"), another held-out
    row.
  - So the gate reads a coarsened copy of held-out information.
- **The design's reason answers a different question.** "Need no
  coordinates" is not "stated in words". B.7's class rests on words ("about a
  quadrant", τεταρτημορίου). The classes of A.2, A.5 and B.2 rest on no word
  at all.
- **What the three rows do.** Share of a 136-year window's days passing
  ALM-A's projection, under the frozen meaning, on [r2v6]'s three null
  windows (−1500, −1100, −700) [me: `narrowing_inferred_phase.py`]:

  | ALM-A's projection | share of days passing |
  |---|---|
  | as 6.4 projects it (A.2 and A.5 at phase class) | 0.54–0.60% |
  | A.2 at "none" only | 0.75–0.85% |
  | A.5 at "none" only | 0.56–0.63% |
  | **both at "none" (words only)** | **4.88–4.89%** (2,422–2,430 days, against a bound of 2,484) |
  | both at "none", with A.9 at civil dawn (10.3's instant) | 4.90% |

  - The two rows carry the same lunar information: a young crescent on Day 0
    makes the Moon near full 13 days later. So either row alone keeps ALM-A
    far below the line, and only the pair decides it.
  - ALM-B is unchanged by B.2 (4.40–4.45%; C7).
- **Consequences.**
  - **Two knife-edges, not one.** Under 6.4's own rule, gate 3b would rest on
    ALM-A, about 0.1 percentage point inside the 5% line, as well as ALM-B,
    about 0.6 inside. Both come from a rough estimate that locates greatest
    elongations to the day. As designed, ALM-A's margin comes from the three
    inferred rows.
  - **The rows only help the claim the gate tests.** Setting them to "none"
    only loosens rows. So no truth is lost (R10 stands), and narrowing only
    gets harder.
  - **The expected pass leans on them:** P21, S0x and 2.10.
  - **For Q_H they work the other way.** The held-out positional rows of A.2,
    A.5 and B.2 are scored inside a pool already filtered by their coarsened
    copies, which lowers their weights. That understates the held-out test,
    so Q_H is more likely to hold. It is conservative, but it is the same
    break in the separation of projection rows from held-out rows.

**Why major, not blocker.** On the rough estimate ALM-A still narrows (4.9%
is below 5%), so the expected label does not flip. But gate 3b's margin, and
P21, rest on rows that 6.4's own principle excludes. They also push towards
"the method can see", the claim the gate exists to test.

**Fix.**
1. Set A.2, A.5 and B.2 to "none" in the B&M-type projection, as 6.4 already
   does for A.10, B.5 and B.9. Report the inferred-phase projection as a
   sensitivity. Only rows are loosened, so R10's nine truths stand.
2. Update `alm_rows.py` and I13(f)'s reference list, and recompute the
   design-stage narrowing.
3. Restate:
   - 2.6 and 2.10;
   - R28, where N_narrow may now be 8, 7 or 6;
   - P21, now genuinely open, with two knife-edges;
   - [AppT 2] and [AppT 6];
   - S0x and S0y.
4. If the design keeps the rows instead, it should:
   - say why a phase inferred from a held-out relation counts as a word;
   - record that the choice favours the claim;
   - take gate 3b across both projections, as gate 3a does, so that the
     choice cannot be what makes it pass.

#### R3-2. Q_attain4 measures the eclipse condition over the core, but label 4 can fire only in two fixed windows (major)

**Where.**
- D 6.5: "Windows", "hit_j", and "Whether outcome 4 could fire at all".
- The Q_attain4 row of 1.3.
- The E_j and hit_j rows of 9.1; 9.2.
- 9.4, C4 and C6; 2.10; 12.3; P25; 14.6 #71.

**Evidence.**
- **hit_j** asks for a unique survivor "in one of the two windows". These are
  the Odyssey's reproduction window (136 years) and its primary window (251
  years), at fixed positions (6.5, "Windows").
- **E_j** counts eclipses with h_tot ≥ m̂ anywhere in the 1,698-year core
  that some eclipse-compatible reading makes unique in some 136- or 251-year
  window around them.
- **So E_j ≥ 1 does not show that hit_j can hold.** An eclipse made unique in
  some other century satisfies E_j and can never fire label 4. Q_attain4 can
  then stay silent while label 4 is impossible, and P25 can pass on it.
- **The converse holds, so the qualifier is sound when it does print.**
  hit_j at M_Ody implies E_j ≥ 1: the fixed windows lie inside the core, and
  M_Ody ≥ m̂ (R3-3). So it errs only towards silence.
- **The exact answer is computable now.** Nothing in label 4 is unknown at
  the null-side stage except M_Ody's exact value.
  - The G condition (G_j against G_BM,u,lo) is null-side.
  - hit_j reads only the negatives' gardens, the sky of two fixed windows,
    and M_Ody. With m̂ in M_Ody's place it is null-side too.
  - So the exact attainability can be frozen at the second freeze.
- **The allowance is misstated.** 2.10 and 6.5 say a negative may have
  "about 11 reach-units". But 11.4 = 0.00107 × 10,690 is the bound itself.
  - When every reached target has reach 1, G_j,hi ≤ 0.00107 needs k ≤ 4. The
    gamma bound is 0.00096 at k = 4 and 0.00109 at k = 5 [me:
    `scipy.stats.gamma.ppf(0.975, k + 1)/n`]. The block bootstrap can only
    widen that.
  - B&M's own 36 readings reach about 18 units (0.00172 × 10,690).
  - So a negative's garden must be at least four times more selective than
    𝒢_BM*. The three sizes on record are 294 readings for AEN-TROY, 90 for
    ARG-RETURN and 32 for QS-SACK, before F5 expansion (2.6). That is the bar
    P25 predicts some negative will clear.

**Fix.**
1. At the null-side stage, define hit_j(m̂): some eclipse-compatible
   reading has, in one of the two fixed windows, a unique survivor with
   h_tot ≥ m̂. Q_attain4 holds if no clean negative has both the G condition
   and hit_j(m̂). Report E_j over the core beside it, as context: could a
   window elsewhere have fired?
2. Restate:
   - C4 and C6;
   - S4, S4b and S14b;
   - P25 and 12.3;
   - 14.6 #71.
3. Replace "about 11 reach-units" with "at most about 4 targets reached; the
   bound is about 11.4 units". Say in 2.10 that this asks for a garden at
   least four times more selective than 𝒢_BM*. P25 should then argue why
   that is plausible, or be restated as open.
4. State in 4.4 that m̂ lies below the exact M_Ody (R3-3), and that this
   keeps Q_attain4 sound.

#### R3-3. I2(c) still cannot be met reliably by a correct implementation (major)

**Where.**
- D 6.1, the I2 row: its pass column and its accuracy column.
- 10.2 `deltat_mix`, "What the scan can miss".
- 10.4, the `deltat_mix.py` row.
- 4.4 (m̂) and 2.3.

**Evidence.**
- **Where the 2.3 values come from.** The table's per-model values come from
  the first review's `check_p19.py`. It integrates each model's Gaussian over
  W78 = (28,805, 29,580) s, its 5-s-grid totality window.
- **The continuous window is wider.** Bisecting the same solver
  (`check_bessel.py`, reading `data/jsex/SEm1199.js`) to 0.01 s gives
  **28,801.02–29,584.91 s** [me: `i2c_table_gap.py`]. 10.2 says a totality
  row hands `p_exact` "the window of `eclipses.totality_window` directly":
  that is, the continuous window.
- **Per model** (canon frame, +34 s for the SMH models, as `check_p19.py`
  converts them):

  | model | 2.3 table | continuous window | gap |
  |---|---|---|---|
  | SMH2020 | 0.294 | 0.2971 | +0.0031 |
  | Addendum 2020 parabola | 0.173 | 0.1751 | +0.0021 |
  | SMH2016 parabola | 0.498 | 0.5030 | **+0.0050** |
  | Espenak–Meeus, canon form | 0.252 | 0.2552 | +0.0032 |
  | mixture | 0.304 | 0.3076 | +0.0036 |

  - I2(c) asks for agreement within 0.005 per model.
  - The SMH2016 parabola sits on that line: 0.0048 against the unrounded
    0.4982, and 0.0050 against the printed 0.498.
  - A fraction of a second's difference in `eclipses.py`'s window, or in the
    frame conversion, puts it over.
  - The accuracy column says the grid costs "about 0.003".
  - The 1131 BC column stays inside, at +0.0029 at most (C11).
- **Two internal conflicts in the synthetic part:**
  - **Sub-step intervals.** 10.2 says I2(c)'s synthetic cases include
    intervals narrower than the 10-s scan, "to measure that loss" of up to
    about 0.007 of one model's mass. Yet 6.1 asks every synthetic case to
    agree within 10⁻⁴.
  - **The bisection bound.** 6.1 says that bisection to 0.1 s moves P by up
    to 0.0004, four times the 10⁻⁴ tolerance. The true bound is smaller:
    about 7.4 × 10⁻⁵ per boundary at σ = 541 s [me: 0.1 s × 1/(541 √(2π))].
    But two boundaries can still exceed 10⁻⁴.
- **Consequence.** I2 is in INSTR, so a correct implementation can block the
  verdict. This is the class of problem [r2v6 N2] found. It is a pre-freeze
  check, so it costs a design edit, not an amendment.

**Fix.**
1. Compare `p_exact` with the 2.3 values recomputed over the continuous
   window (the table above). Or keep the printed table, with a tolerance of
   0.006 and the reason. Correct the accuracy column.
2. Mark the sub-step synthetic cases "measured, not passed". Set the other
   cases' tolerance from the bisection bound, or bisect to 0.01 s.
3. Say in 2.3 and 4.4 that the printed 0.304, and so m̂, are grid-window
   values, and that the exact mixture is about 0.308.

### Minor

#### R3-4. P21 is nearly determined by known numbers (minor)

- **The numbers.** Under 6.4's projection, five of the six sets that can be
  narrowed and keep their truth narrow at 0.07–1.03% of days [r2v6:
  `narrowing_3b.out.txt`; 2.6]. Every one
  keeps its truth at every rounding step [AppT 2]. ALM-B narrows at
  4.40–4.45% (C7). So P21 is settled unless the bench's own ALM-B share moves
  by 0.6 percentage point.
- **The design's own rule.** Revision 7 itself moved P10's held-out part to
  R29, because its rough values were known (2.7). By the same rule P21 is a
  regression expectation, or it should say that only ALM-B's exact share is
  open.
- **If R3-1's fix is adopted**, P21 becomes genuinely open again, with two
  knife-edges, and this issue lapses.

#### R3-5. Two definitions in 6.4 and 10.3 can be read differently by the bench and by I16's reference (minor)

- **"Visible on Day 0".** 6.4 and 10.3 define `same_apparition`'s visibility
  this way.
  - For J.4, whose row lies 267 days after ALM-J's Day 0, that tests Venus on
    the wrong day. The summary at the top says "the record's day".
  - Read literally, it changes J.4's flag on most candidates. On [AppT 2]'s
    own numbers (record minus greatest elongation +45.6 d) it would also fail
    ALM-J's truth, which would make R10's count 8.
- **The dawn instant for `visible_before_sunrise`.**
  - 6.4 says the Sun at −8°, or the stated hour where there is one, and A.9
    states one (five equinoctial hours after midnight).
  - 10.3's `alt_at` row says "civil dawn".
  - The effect on narrowing is small (ALM-A, words only, 4.88% to 4.90%). But
    the flags differ for days near the threshold, and no tie band covers a
    difference of convention.
- **Why it matters.** I16's reference is written from 6.4 and 10.3 (A7). So
  either reading can fail I16(a) at the null-side stage, after the first
  freeze.
- **Fix.**
  - Say "on the row's own day".
  - Give one instant rule for `visible_before_sunrise` in both sections: the
    stated hour if one is given, else the Sun at −8°.

#### R3-6. I16's witness rule does not say whose site-search miss fails INSTR (minor)

- **The rule** (6.1, I16). A mismatch is resolved by evaluating the failing
  side at the other's witness. If it passes there, the miss is listed, and
  INSTR fails "only if a miss changes a seen or strict flag or a set's
  narrowability".
- **The problem.** A miss by the reference, whose search is the coarser
  (a 2° grid with early exit), would fail INSTR though the bench is right.
- **Fix.**
  - Resolve every miss to the witnessed value, on both sides.
  - INSTR fails if the bench's own flag was wrong (a bench-side miss) and
    the flag changes, or if the failing side fails at the witness too.

#### R3-7. The 21 null windows can run past the data (minor)

- **The placement.** I16(a) and `narrowable` place windows at random over
  −1999..+300. But some sets reach well beyond their window:
  - R-THUC links an event 18 war-years after its anchor (T-INT-13);
  - ALM-K's rows run 2,902 days after Day 0.
- **The data.** NASA's elements, and the ephemerides as extended in 11.1,
  end at +300.
- **The effect.** Anchors near the end of a late window lose their linked
  events, and fail rows for lack of data, which makes narrowing look easier.
  The early windows also carry ΔT σ of 2,000–3,700 s (2.3), unlike the gates'
  own windows.
- **Fix.**
  - Place each set's windows so that the window plus the set's longest link
    or offset lies inside the data.
  - Optionally, restrict them to a frozen range, such as −1000..+300, that
    needs no truth.

#### R3-8. Q_attain3a and Q_attain3b can contradict the gate they qualify (minor)

- **Two different windows.** `narrowable` is a majority over 21 null
  windows, while "seen" uses the gate's own window.
- **Sets near the line.** ALM-B is near the 5% line, and so are ALM-H
  (4.37–4.59%) and, under R3-1, ALM-A. Such a set can be narrowed in the
  gate's window and still not be narrowable by majority.
- **The contradiction.** Q_attain then prints "could not have passed" beside
  a gate that passed. 9.4's "known fact" that seen_ALM_SL ≤ 8, because at
  most 8 sets can be narrowed, has the same gap.
- **Fix.** Print Q_attain3a or Q_attain3b only when its gate fires. Or count
  a set as narrowable if it is narrowed in a majority of the null windows or
  in the gate's own window.

#### R3-9. The sealed list omits D4, which the disclosure table marks "constrains" (minor)

- **The definition and the list.** 7.1 defines the sealed list as every line
  and file the scan lists under a "constrains" fact. It then names only D3's
  lines and D5's files.
- **D4 is in the public design.** D4 (Mercury's station on 5 Mar, greatest
  western elongation on 19 Mar, MWRA about 12.3 Mar −1177) is marked
  "constrains H3". Its values are printed in the public copy of DESIGN itself
  (2.2, 2.9, 7.1), and in `research-visibility.md` §2.3, which is
  whitelisted.
- **Why it is minor.** It changes no label: H3 matters only through Q_contra,
  as 7.1 says. But the definition and the list disagree.
- **Fix.** Either say that D4 is public by design, and why that does not
  matter, or narrow the definition.

#### R3-10. Q_score conflates two disclosures that are both expected (minor)

- **Two reasons, one flag.** On the known numbers Q_score holds twice over
  (S0x):
  - gate 3a's best-fit leg sits at 4;
  - gate 3b's decision changes with the meaning of `same_apparition`.
- One flag cannot say which gate's decision rests on a choice made after the
  answers were read.
- **Fix.** Use Q_score3a and Q_score3b, or name the gate in the printed
  qualifier.

#### R3-11. Slips (minor)

- `verdict_trace.py` says it checks "C1–C14" and labels a check "C14 E_j".
  9.4 has C1–C12.
- 11.2, step 2, still computes hit strengths "under the mixture grid". 4.4 and
  6.3.3 now integrate exactly.
- R28 should say N_narrow is 8, "or 7 or 6", since ALM-H (4.37–4.59%) is as
  near the line as ALM-B.
- The accuracy column of I2 in 6.1 gives 0.0004 for a bisection to 0.1 s. It
  is about 7.4 × 10⁻⁵ per boundary at σ = 541 s (R3-3).
- 2.10 and 6.5 say "about 11 reach-units" (R3-2).

---

## 5. What I could not check

- **The bench's exact narrowing of ALM-A (words only) and of ALM-B.** Both
  lie within the rough estimate's accuracy of the 5% line, and that is the
  finding of R3-1.
- **Whether any negative's garden can reach G_j,hi ≤ 0.00107.** Nobody has
  estimated G_j. R3-2 only shows how demanding the bound is.
- **The truth-side margins of [AppT 2] and [AppT 2b].** I did not open the
  truth files. R3-5's remark about J.4 uses only Appendix T's own numbers.
- **SMH2016's Table S4.** It is a pre-freeze task.
- **H3 and H4 at the target.** Not computed, on purpose.
- **`docs/critique-design-r1.md`.** Not read.

## 6. Files produced for this review

All are in `C:\Projects\odybench\results\critique-design-r3\`.

| script | what it does | output |
|---|---|---|
| `scan_clues.py` | Licence-word and date-leak scan of both clue files, and a readable dump of every row and option (C1, C2) | `scan_clues.out.txt`, `scan_clues.dump.txt` |
| `narrowing_inferred_phase.py` | [r2v6]'s `narrowing_3b.py` machinery, unchanged, extended with the frozen meaning and with A.2, A.5 and B.2 set to "none", alone and together, and A.9 at civil dawn (R3-1, R3-5, C7) | `narrowing_inferred_phase.out.txt`, `.json` |
| `i2c_table_gap.py` | The continuous totality windows of 1178 and 1131 BC at Ithaki, by bisection of `check_bessel.py` on `data/jsex/`, and per-model P(total) against the 2.3 table (R3-3, C11) | `i2c_table_gap.out.txt` |
