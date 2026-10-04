# Adversarial review of DESIGN.md, revision 5 (recheck, round 1)

Written 2026-10-04 by a reviewer who did not write DESIGN.md. Scope: `DESIGN.md`
revision 5 (all 4,704 lines, Appendix T included), judged against the 25 issues
of `docs/critique-design.md` (read in full), and searched for new problems.

**This file's name.** The re-run of the review loop writes its round-1 recheck
to `docs/critique-design-r1.md`. The earlier file of that name, the recheck of
revision 2 that DESIGN cites as [r1], is preserved byte for byte at
`results/design-revision-v5/critique-design-r1.recheck-of-rev2.md`. I checked
before overwriting: both had SHA-256 `82308707…6e771b`. DESIGN's [r1 …] tags
keep pointing at that copy. A later revision should cite this file as [r1v5].

**What I read.**
- In full: `DESIGN.md`; `docs/critique-design.md`; the three clue files
  `data/prereg/controls_real.json`, `controls_almagest.json` and `negatives.json`
  (dumped row by row).
- In part:
  - `research-unread-primaries.md` §2;
  - `research-bm2008.md` §2 and its list of eclipse circumstances;
  - `controls-real-drafting.md` §1 and §5;
  - `DESIGN-v1.md`, the held-out table;
  - `DESIGN-v2.md` §6.3.2.
- Scripts the revision relied on: `results/design-revision-v5/heldout_strata.py`,
  `verdict_trace.py`, `alm_rows.py` (its inputs) and `scan_truthside.py`; also
  `results/bm2008-b-checks/ephem.py`.
- The truth files `controls_real_truth.json` and `controls_almagest_truth.json`.
  I read them only to build the leak scan and to read the drafter's post-hoc
  notes, as the task allows.
- On the web: the JPL Horizons API documentation, batch-file documentation and
  manual, for rise/transit/set output.

**What I deliberately did not do.** I evaluated neither held-out predicate (H3,
H4) at the target. I did not read the values in any cached target-day Horizons
file. The bench's held-out test is no less blind than it was before this
review.

**Tags.**
- [D §n] and [D l. n]: DESIGN.md revision 5, section n or line n.
- [AppT n]: its Appendix T.
- [rev #n]: `critique-design.md`.
- [r1] and [r2]: as DESIGN uses them.
- [bm §n], [unread §n], [alm §n]: as in DESIGN's tag table.
- [me: script]: computed by me with the named script in
  `results/critique-design-r1/v5/`, with its output beside it.
- [me]: my own arithmetic or inference.

**Truth-side content.** DESIGN 10.1 keeps `docs/critique-design*.md` off the
public tier. Even so, this file names no accepted date. Where a truth-side fact
matters it cites Appendix T.

---

## 0. Summary

**Old issues.** Of the 25, 22 are resolved. Three are not fully resolved: #11,
#13 and #17. None of #1–3 is among them.

**New issues:** 15 in all, **1 blocker, 6 major and 8 minor**.

**The blocker (N1).** Gate 3a, "the eclipse component can see", passes on the
design's own expected numbers only because of its best-fit scoring rule.
- That rule was chosen after the drafter had looked up the answers.
- Under the all-must-pass rule the bench applies to the Odyssey and to fiction,
  with the same 5% narrowing, the expected count is 2 of 7, against a threshold
  of 4. Gate 3a would then fire.
- The qualifier that is meant to expose the non-blind choice, Q_strict, counts
  strict recall without narrowing. That count is expected to be 4, so Q_strict
  stays silent.
- The verdict's "no 3a", and with it the meaning of every eclipse-dependent "no",
  therefore rests on a rule picked with the answers in view.

**The majors:**
- **N2. The only route to "yes" was closed before it was built.** On the
  lattice, label 1 needs H4. H4's value at the target follows from B&M's
  published remark that Mars was invisible and from V, and both were on record
  when H4 was frozen. The design's own blindness test drops H2 for less.
- **N3. The public tier can read the Almagest dates.** The whitelist includes
  `data/text/`. Ptolemy's rows there state the Nabonassar year and Egyptian day
  of every *Almagest* record, the very words the clue file withholds.
- **N4. Two INSTR checks cannot be met as written.** I5(a) compares with
  Horizons' rise/transit/set output, which has no custom h0, no airless option at
  the bench's h0, and minute resolution. I15(a)'s reference code has no Mars.
- **N5. Outcome 4 is called reachable on a necessary condition only.** The
  negatives' G_j is null-side in kind but is never estimated.
- **N6. The control-search layer that produces seven rule inputs has no second
  implementation.** Meanwhile gate 3a sits on its threshold.
- **N7. Gate 3a scores Ptolemy's table-computed solar longitudes and
  mid-eclipse times.** Revision 5 removes that kind of quantity from gate 3b on
  principle.

**What holds up:**
- The rule is a pure function of named quantities, and `verdict_trace.py`
  transcribes it faithfully.
- The clue files match their recorded hashes. Every licence string is verbatim
  in its row.
- No accepted date appears in the public copy or the whitelisted notes, beyond
  the one Appendix T discloses and a year in I2b's row.
- The two-pool rank test is exact under its stated assumption, and its
  design-stage estimate masks the target.
- The freeze machinery answers #4.

---

## 1. Checks that passed

| # | claim or property | how I checked | result |
|---|---|---|---|
| C1 | Clue-file hashes in D 12.4 | `sha256sum` | `135fba67…83f8`, `18b3ff01…b458` and `be4f511e…9c82`: **match** |
| C2 | Licence strings are verbatim in their rows, in text order [D 2.6, 2.9] | split on "…", raw-character search [me: check_licences.py] | **controls_real 125/125; controls_almagest 54/54.** The 18 *Almagest* interval rows carry withheld-date placeholders, as intended |
| C3 | No modern or absolute date in the searcher's input | regex over every `operational` field and statement [me: check_licences.py] | **None found.** The only date-like strings are those the texts themselves state: Egyptian dates (free epoch), Roman dates (free offset) and "the Ides of March" |
| C4 | Public tier free of accepted dates [D 10.1, I13(h)] | 51 accepted dates in about 15 printed forms each, plus JDNs, searched in every whitelisted note, script, prereg file, Horizons cache file and the public part of DESIGN [me: scan_public_leaks.py] | **One hit:** `data-acquisition.md` l. 265, the "−309 Aug 15" that [AppT 8] already discloses. Year-only: the public copy's "−430" (N15c). Every −720 mention is SMH's spline epoch |
| C5 | Garden sizes [D 5.3] | arithmetic | 36; 35,964; 767,232. Eclipse-compatible: 11,988; 383,616. With F6: 144; 143,856; 3,068,928. **Confirmed** [me] |
| C6 | `verdict_trace.py` transcribes 9.2 | read | **Line for line.** Lattice 0.026 / 0.045 / 0.227 / 1; S0–S13 as tabulated in 9.5 |
| C7 | The design-stage held-out estimate never touches the target [D 2.9] | read `heldout_strata.py` | **Yes.** The target is removed from the rows before anything runs, and `held()` asserts it |
| C8 | 2.4's rate with the equinox clue on | arithmetic | 0.55 × 0.158 = 0.087 per century, 1.9 survivors. P(N ≤ 1) = 0.43; P(N ≥ 4) = 0.125. For N = 4 the exact lower bound is 0.0496, above 0.048. **Confirmed** [me] |
| C9 | The identity G(𝒢_BM*, T) = (n_A/n_T) G(𝒢_BM*, T_A(v)) for v1–v5 [D 4.2] | reasoning | **Holds.** At 38.4°N the Sun sinks at least about 0.17° a minute near the horizon, so a 90-min lead puts it below −13° at Venus' rising. An event within 3.5 d implies the 4-d and 6-d slots [me] |
| C10 | MacDonald 1967 [D 1.1, 2.5] | `research-unread-primaries.md` §2.1–2.5 | **As stated:** the first spring reading of 5.272 cites Schoch and shifts its timetable a week to meet the eclipse; E is his; Gainsford misreads p. 327 |
| C11 | The Fay–Feuer interval as written in 5.3 | algebra | **Consistent** with the gamma interval (shape y²/v, scale v/y, and the w_M correction). y = 0 gives 3.69/n [me] |
| C12 | Filtered eclipse-compatible lists of the negatives [D 6.5] | read `negatives.json` | **Follows from the file:** ARG-RETURN-04:c and QS-SACK-02:a are lunar options, and QS-SACK-06:a is the storm |

---

## 2. The 25 issues of the first review

| # | sev | resolved? | comment |
|---|---|---|---|
| 1 | blocker | **yes** | **What is fixed.** 9.1–9.2 is a pure function of named quantities. Every condition names its garden, pool and stage, and G has one sense (9.3). `verdict_trace.py` reproduces 9.2, and S0–S13 reach every label on the design-stage null side (C6). **Residuals, now separate issues:** outcome 4's realisability rests on a necessary condition only (N5); for this target the only route to label 1 was closed by published facts (N2) |
| 2 | blocker | **yes, for the clue file** | **What is fixed:** `controls_real.json` was drafted before the truth was looked up, then licence-checked. Its hash matches (C1), its licences are verbatim (C2) and it carries no modern date (C3). The five exposed rows are measured by the re-draft and the audit. **The leak has moved to the scorer:** the gate-3a scoring rule was chosen after the answers were read, and it decides the gate (N1) |
| 3 | blocker | **yes** | **What is fixed.** 3a and 3b are split. The *Almagest* B&M-type control is scored at B&M's tolerances (Q_BM) and at leave-one-set-out observer slack (3b). The projection reads words only, and the held-out rows are named. Hash and licences check (C1, C2). **Residuals:** no star-season record (N13); held_ALM's real ceiling is 7 (N8) |
| 4 | major | **yes** | Local git, two freezes, and PREREG.sha256 with the commit, tree and code-tree hashes. Amendments are dated. Publishing is optional and needs Jon's permission (12.5). The access-log part of the first freeze has an ordering bug (N9) |
| 5 | major | **yes** | 1.1 attributes the 6 years to C ∧ E. The four-clue comparison is R13 at 0.88 per century. The comparison with E on is a reported R19 with exact Poisson intervals. 2.4's arithmetic checks (C8) |
| 6 | major | **yes** | MacDonald was read (pp. 324–327). The reason for conditioning is frozen and documented (C10), and both p_fix figures are reported (5.1 item 6) |
| 7 | major | **yes** | Three nested, sourced gardens with G_BM primary. Sizes confirmed (C5). The greedy smallest fork set is reported (P14) |
| 8 | major | **yes** | F1b is in DOC and FULL. PC-S jitters 0–3 d and reports the decay. The negatives' stated counts get the same jitter in the reported comparisons, and the rule's comparison has F1b off on both sides |
| 9 | major | **yes** | C_rel and E_rel are used outside T0b. The h_A/h_P calibration is labelled a fit, and λ is reported per century (P8). P8's second clause is near-determined (see #17) |
| 10 | major | **yes** | Hit strengths come from the four-model mixture. The background runs from −1999. The target is excluded from its own base rates. The site-rotated p_e and Schoch's 10–12 h rule are reported |
| 11 | major | **no** | **Fixes 1–3 are done:** P_MWRA matches the pool to the Mercury event the target passes; H1, H2 and H5 are uncounted; R_anc is reported. **But the counted statistic still holds a predicate whose value at the target was fixed before it was frozen.** H4 follows from B&M's published Mars remark (H5) together with V, and R12 already lists label 1's failure. This is the same defect as the "already known" H1 and H5 of this issue (N2) |
| 12 | major | **yes** | Vertex fit at ±1.5 d, rises converged to 0.1 s, flat maxima flagged, and the sensitivity grid. I6 and I7 have tie bands |
| 13 | major | **no** | Second paths are named for most code, but three gaps remain. (i) Fix 1's comparison with Horizons' rise/transit/set output "within 0.5 min" cannot be met as specified: RTS offers only the TVH, GEO and RAD horizons, at integer-minute steps, and the manual disclaims better than a minute. (ii) The new I15(a) reference code has no Mars. (iii) The control-search layer that produces seven rule inputs has no second implementation (N4, N6) |
| 14 | major | **yes** | Instrument mode (I10) and science mode exist, and PC-S enters no gate. I10's Standish path lacks stars (N4), but I10 is reported only |
| 15 | major | **yes** | The Iliad is a same-tradition comparison, beside 12 clean negatives under the Odyssey's selection rules. The storm rule is in place, and NC4/NC5 moved to I11. The lists are filtered consistently with the file (C12) |
| 16 | major | **yes** | No LR enters the rule; the ceiling 1/P(A) is a standing finding. Each G interval is the wider of the gamma and block-bootstrap intervals. I9(b)'s per-side coverage level is mis-set (N14) |
| 17 | major | **no** | **Done:** the moved items are in section 2. **Remaining:** (a) **P6 is effectively settled.** The rough p_fix\|C is 0.0054, inside [0.002, 0.02] with at least 2.7× margin on each side, and the unconditional ~0.0007 [vis §5] is inside [0.0002, 0.002]; the design itself says the rough value "lies well inside". (b) **P20 sits exactly on its threshold:** the expected seen_PCR is 4 [AppT 6] against "≥ 4". That is revision 1's P20 at 1.9% against 2% again. (c) **P8's second clause is near-determined** by r2's C_rel calibration. At −1700 C_rel admits Ti in about 12 Mar–12 Apr against the fixed 18 Mar–16 Apr, about 87% overlap, against the predicted "< 90%" [me, from D 2.9]. (d) **P24's real ceiling is 6 of 7, not 6 of 8** (N8) |
| 18 | major | **yes** | R_anc is run with and without the eclipse, under four ancient season bounds of equal prominence, with the history recorded |
| 19 | minor | **yes** | Espenak–Meeus is one model, in a four-model mixture |
| 20 | minor | **yes** | A1–A5 are labelled regression tests. I3 is a reported calibration |
| 21 | minor | **yes** | smag is pinned to `program.js`, and smag_partial serves I2b only. One leftover slip: 2.3's 1131 BC row (N15a) |
| 22 | minor | **yes** | Epoch −1176.68; a half-open window; R6 = 1,683 |
| 23 | minor | **yes** | The T0 grid is kept. T0b's reading is a member of 𝒢_BM*. T0_pass is separated from T0 |
| 24 | minor | **yes** | Each slip is corrected: H8 dropped; H2's rate stated; reach 11/136; X1 no longer called Schoch's; MacDonald documented |
| 25 | minor | **yes** | HIP numbers were verified against SIMBAD and hip2. Sirius uses the barycentric orbital solution, with the alternatives quantified |

---

## 3. New issues

### Blocker

#### N1. Gate 3a passes only under a scoring rule chosen after the answers were read, and the qualifier meant to expose that choice cannot (blocker)

**Where:** D 6.3.2 (scoring, the gate, Q_strict); 1.3 (outcome 3a, Q_strict);
2.6; 2.10; 8 (R8, P20, P27); 9.2; [AppT 3, 6].

**Evidence.**

- **What the rule says** [D l. 2356–2393]:
  - *Seen* means two things together: the truth is in the best-fit set B, the
    candidates that fail the fewest rows; and |B| ≤ 0.05 N_cand.
  - **3a fires if seen_PCR < 4.**
  - **Q_strict holds if strict_PCR < 4.** Strict recall is only f(truth) = 0.
    It carries **no narrowing condition**.
- **When the rule was chosen.**
  - 6.3.2 itself says the best-fit rule was chosen after the drafter's
    post-freeze check showed accepted dates failing primary readings, and calls
    the choice "not blind".
  - The rule, the 5% narrowing and the threshold of 4 entered together in
    revision 2 [DESIGN-v2 l. 1280–1310].
  - The drafter, writing after looking the dates up, recommends exactly this
    scoring: a tolerance for failed clues rather than all-must-pass
    [`controls_real_truth.json`, "would_have_written_differently", item 1].
  - Neither earlier recheck examined the rule. A search of both preserved copies
    finds neither "best-fit" nor "Q_strict".
- **What the known numbers give** [AppT 3, 6; R8; P20]:
  - **In four counted sets the truths pass every primary row; in three they
    fail some.**
  - **Seen under best-fit: four sets, so seen_PCR = 4, exactly the
    threshold.**
  - **Two of those four are seen only because best-fit tolerates the rows their
    truths fail.**
  - **The other two sets whose truths pass every primary are expected unseen.**
    Their truths are in S₀, so B = S₀, and their "none" site primaries leave S₀
    wider than 5%. That does not depend on the truth. For R-THUC, D 6.3.4 says
    the set is expected unseen "in any case".
- **Consequence:**
  - All-must-pass with the same 5% narrowing gives an expected count of
    **2 < 4, so 3a fires**.
  - Best-fit gives 4, so 3a does not fire.
  - **The scoring choice alone decides gate 3a.**
- **Q_strict cannot show this.** The two sets whose truths pass strictly but do
  not narrow still count in strict_PCR. So strict_PCR = 4 (R8), and Q_strict is
  silent. The disclosure that D l. 2392–2393 offers for the non-blind choice is
  computed on a quantity that does not depend on the choice.
- **The rule tested is not the rule used.** Every Odyssey-side and fiction-side
  quantity is all-must-pass within a reading: survivors, reach, G, r_Ody and
  hit_j [D 5.3, 6.5]. Gate 3a certifies a best-fit method that the bench never
  applies to the Odyssey or to the negatives.
- **The margin is zero.** Two sets are expected unseen whatever the truth, and
  one fails on known textual errors, so 3a needs every one of the other four. Any one of them
  flips the headline if it fails the narrowing, or if it loses its place in B to
  a candidate that fails fewer rows. Both are possible once the bench's own lunar
  module replaces the drafter's rough model [AppT 3].

**Why it is a blocker.**
- P27's expected verdict is {inconclusive} with Q_BM, Q_tol and Q_slot. Under
  the strict analogue it becomes {3a}.
- Label 3a decides two things:
  - whether the absence of label 4, and every other eclipse-dependent "no", is
    printed as meaningful or as "could not have seen it";
  - whether label 1 is vetoed.
- A gate whose pass rests on a rule picked after reading the answers cannot
  certify that the method can see. The verdict's "no 3a" would be wrong in
  exactly the way critique issue 2 warned of, through the scorer instead of the
  clue file.

**Fix.**
1. Define **seen_PCR,strict** := the number of counted sets with f(truth) = 0
   and |S₀| ≤ 0.05 N_cand.
2. **Let 3a fire if seen_PCR < 4 or seen_PCR,strict < 4.** That is the bound
   against the claim "the method can see", which 9.3 asks of every bound.
   - Apply the same combined side to Q_exposure and Q_ΔT.
   - At the very least, redefine Q_strict as seen_PCR,strict < 4 and print it in
     the headline beside 3a.
3. Restate 2.10, R8, P20 and P27 with the strict count. On [AppT 3, 6] it is
   expected to be 2, so the expected verdict gains 3a (or Q_strict).
4. Record in 6.3.2 that three choices were all made after the truth-side check:
   the scoring rule, the 5% narrowing and the threshold of 4.
5. Decide whether 3a should veto label 1 at all. The held-out test reads no
   eclipse, and 7.2 and S11 already argue that an exact test needs no power
   calibration to say "yes".
6. See N7. The two sets that best-fit rescues also score Ptolemy's
   table-computed quantities.

### Major

#### N2. The only route to label 1 was settled by facts on record before its predicate was frozen (major)

**Where:** D 1.1 ("the clues nobody fitted"); 1.3 label 1; 2.10; 7.1 (the
blindness tests); 7.2; R12; 13 row 42; [rev #11].

**Evidence.**

- **What label 1 needs.** It needs p_H ≤ 0.05. On the design-stage lattice that
  requires the target to pass H4: p_H is 0.045 with H4 alone and 0.026 with both
  predicates, while H3 alone gives 0.227 [D 7.2; 9.4 C8].
- **What was on record when H4 was frozen.** Revision 1 froze H4 on 2026-10-03:
  Venus–Mars within 5° within ±3 d of Day −7 [D 7.1]. By then:
  - B&M had published two facts [B&M §Historical Plausibility and Fig. 1;
    research-bm2008.md l. 64 and l. 596, written at 19:57 that day]:
    - Mars was not visible in March–April 1178 BC except during the eclipse;
    - at the eclipse all five planets lay within less than 90°, with Mars at
      magnitude 1.3.
  - Revision 1's own held-out table puts that remark directly below H4, as H5
    [DESIGN-v1 l. 733–734].
  - V puts Venus far west of the Sun: on Day −5 it rose 103.6 min before the
    Sun, and stood 44.3° from it on 11 Apr [D 2.2; unread §2.5].
  - A Mars within 5° of a Venus 40° or more from the Sun would be a conspicuous
    morning object. B&M's remark excludes that.
- **So H4's value at the target followed from target-day evaluations made before
  it was frozen** [me]. D 2.10, R12 and 13 row 42 draw the same inference.
- **The design's own blindness test.** 7.1 counts a clue only if "nobody has
  evaluated it at the target before its predicate was frozen".
  - It drops H2 because its value at 1178 BC had been computed before its
    threshold was frozen. Revision 1 dropped H1 for being known to fail
    [rev #11].
  - H4's value is fixed by evaluations of the same kind. 7.1 keeps H4 counted
    because the inference "is not a computation". That is a difference of form,
    not of substance.
- **H3 is touched too.** Two items on record bear on H3's test of a conjunction
  within ±3 d. I did not read either value. 7.1's search for prior evaluations
  covered `docs/` and `results/` only.
  - B&M's Fig. 1 gives Mercury's magnitude at the eclipse, on Day 0
    [research-bm2008.md l. 596].
  - A whitelisted cache file holds Mercury's apparent position and its
    elongation from the Sun at Ithaki on Day −6:
    `data/ephem/horizons/venus_mercury_m1177_04_10_dawn_199.txt`, fetched
    2026-10-03, quantities 1, 2, 4, 20, 23 and 30.
- **Consequence.** 9.3 holds that "a test whose most extreme possible
  observation cannot reach 5% has no power". By that standard, once H4's value
  was known, the held-out test could not say "yes" for this target.
  - Q_attain is computed on the null-side floor, so it will still report outcome
    1 as attainable.
  - The verdict will then present "no label 1" as the result of a blind test of
    the unfitted clues.
  - **The labels are not wrong. The qualifier set and the stated meaning of the
    "no" are.**

**Fix.**
1. **Apply 7.1's second test by its substance.** A predicate whose target value
   follows from target-day facts published or computed before it was frozen is
   not blind. Before the first freeze, write a disclosure table that pairs each
   such fact with the held-out predicate it constrains. The facts include:
   - B&M's Fig. 1 magnitudes and planetary arc;
   - H5;
   - V's lead and Venus' elongation;
   - the cached files in `data/ephem/horizons/`.
2. **Then choose one of two courses:**
   - (a) **Drop H4 from the counted statistic.** On the design-stage pools
     p_H,min becomes about (1 + 15)/77 ≈ 0.21. Q_attain then holds, and the
     verdict says outright that the bench cannot say "yes".
   - (b) **Keep H4 and add a target-side qualifier,** printed whenever label 1
     is absent. It says that every pattern below 0.05 needs H4, and published
     facts exclude H4 at this target, so the held-out "no" is not a blind
     result. R12 then becomes a standing finding.
3. **If a blind "yes" route is wanted,** freeze further god-movement predicates
   now. First show, by a documented search of `docs/`, `results/` and `data/`,
   that no prior target-day evaluation exists. Then estimate their null floor
   with the target masked.

#### N3. The public tier's whitelist hands its agents the *Almagest* controls' dates (major)

**Where:** D 10.1 (the public whitelist includes `data/text/`); 6.4 ("the date
words themselves are withheld"; the searcher "never the text at `ref`");
I13(c); I13(h); 13 row 50.

**Evidence.**
- **The clue file withholds the dates.** `controls_almagest.json` withholds
  every Egyptian date from its interval rows. The reason it gives: "with any
  season clue, a wandering-calendar date fixes the absolute year". Yet each
  clue's `ref` names the very text row that states the date.
- **`data/text/` is on the whitelist, and the text states them.** The Ptolemy
  export gives the Nabonassar year and Egyptian day in those rows. Row 9.10.3
  reads "κατὰ τὸ ωπϚʹ ἔτος ἀπὸ Ναβονασσάρου, κατʼ Αἰγυπτίους Ἐπιφὶ βʹ" [checked
  in `ptolemy-syntaxis-grc.tsv`].
- **One line of arithmetic gives the absolute date.** The epoch is well known
  (JD 1448638), and the truth file's conversion is exactly that line.
- **Who can read it.**
  - Every public-tier agent that opens a clue's `ref` can read the truth of the
    counted *Almagest* sets. A3 translates these rows, and A9 checks text rows.
  - For R-PTOL-ALEX and R-PTOL-BAB, the clue file's own statements name Hadrian's
    and Mardokempados' regnal years, which background knowledge converts.
- **What the tiers protect.** 10.1 introduces them because a translator or a
  builder of the searcher "could be steered" by truth-side facts. For gate 3b's
  control they protect nothing. I13(c)'s static ban on the epoch constant guards
  the code, not the agent.

**Fix.**
1. **Take `data/text/` off the public whitelist.**
   - A3 needs only the clue files' operational fields.
   - A9 needs the negatives' texts, and for the sibling pairs only the licence
     words already in the clue file.
   - If text rows are needed, provide an export with the date words masked.
2. **State in 13 row 50 what protection is real.** The Ptolemy sets' truths can
   be derived from the clue file's own statement text plus common knowledge. The
   only real protections are mechanical:
   - the searcher reads operational fields only (I13(c));
   - the second implementation of N6;
   - a review of any search code that special-cases a set.
3. **If text exports stay on the list,** extend I13(h) to scan them for date
   words, such as Ναβονασσάρου and regnal-year formulas.

#### N4. Two checks inside INSTR cannot be met as specified (major)

**Where:** D 6.1 I5(a) and I15(a); 10.4; 10.1 (A7); 11.1.

**Evidence.**

- **I15(a) cannot compute H4 on its named reference.** It is to run "on the
  Standish low-precision code of `results/bm2008-b-checks/ephem.py`".
  - That code's element table holds Mercury, Venus and the Earth–Moon barycentre
    only. **It has no Mars**, nor Jupiter or Saturn, so H4 cannot be computed on
    it [read: its `EL` table].
  - Its elements were typed from memory [research-bm2008-b.md l. 501].
  - It precesses with the IAU 1976 cubic of Meeus ch. 21, whose error at −1999
    (T = −40 centuries) is not measured anywhere.
  - So the tie bands, 0.1° on the Venus–Mars separation and on the Sun's
    altitude at rising, have no measured accuracy behind them. A correct pair of
    implementations may disagree outside them.
- **I5(a) cannot be met with Horizons' rise/transit/set output.** It compares
  `sky.py`'s rise and set times with "JPL Horizons rise/transit/set output … same
  h0, airless", within 0.5 min.
  - Horizons' RTS mode offers only three horizons: true visual (dip and
    refraction), geometric with refraction, and radar (geometric, no
    refraction). None is the bench's airless h0 of −0.8333° or −0.5667°
    [horizons_batch.txt, RTS_ONLY].
  - It locates events at a step of at most 9 whole minutes, under "integer ≤9
    minute resolution" [Horizons API documentation, STEP_SIZE row].
  - The manual warns that rise and set "may not be accurate to less than a
    minute" [Horizons manual].
  - Horizons' UT also rests on its own pre-1962 ΔT, which before 721 BC does not
    follow its manual [`research-ephemeris.md` l. 108].
- **Both checks are in INSTR,** and `verdict.py` refuses to run unless INSTR
  holds [D 6.1, 9.2]. As written, the verdict is either BLOCKED or the checks get
  quietly redefined after the fact. The RTS comparison was itself the first
  review's fix 1 of #13, adopted without checking.
- **I10 (reported only) has the same gap.** Its instrument-mode generator needs
  star altitudes for its season statement, and the Standish path has no stars.

**Fix.**
1. **I15(a):**
   - Add Mars, and any other body H3–H5 need, from the published Standish table,
     fetched with its source.
   - Replace the values typed from memory.
   - Before the first freeze, measure the reference's error against DE441 over
     −1999..+200 for the Venus–Mars separation and for the Sun's altitude at
     Mercury's and Mars' rising.
   - Set each tie band to at least three times the measured error.
   - Alternatively, run I15 on Horizons for every pool member: about 80 members
     × 10 days, a few hundred requests.
2. **I5(a):** use Horizons observer tables instead of RTS output.
   - Request airless apparent alt/az with `TIME_DIGITS=FRACSEC` at 1-min steps
     around each event, and find the h0 crossing by the check's own
     interpolation.
   - Take UT and ΔT from Horizons' own output for both sides.
   - Set the tolerance from the interpolation error plus the documented
     sidereal-time difference.
   - Alternatively, keep RTS output with GEO and a tolerance of at least 1 min
     plus the h0 conversion.
3. **Repeat 6.1's review that a correct implementation can pass** for every
   INSTR row, against each reference's measured accuracy rather than its nominal
   one.

#### N5. Outcome 4 is called reachable on a necessary condition only (major)

**Where:** D 2.10 ("Outcome 4 is attainable"); 6.5; 9.1 (G_j at the "controls"
stage); 9.4 C4, C6 and C7; 9.5 S4; `verdict_trace.py`.

**Evidence.**
- **2.10's argument shows only a necessary condition.** It rests on
  G_BM,u ≈ 0.0017 > U0(10,690) = 0.00035. That says only that a negative that
  reaches no target could meet G_j,hi ≤ G_BM,u.
- **But hit_j needs a unique survivor.** A unique survivor has reach > 0 (C4), so
  G_j > 0.
  - One target at reach 1 already gives G_hi = 11.14/(2n_j) ≈ 0.0005, by 5.3's
    formula [me].
  - G_BM,u is about 18 reach-units spread over 10,690 targets
    (0.00172 × 10,690) [me].
- **G_j averages over every reading of 𝒢_j,** the full product of the set's fork
  options, before F5 expansion [me: neg_garden_sizes.py]:
  - AEN-TROY 294 readings, ARG-RETURN 90, QS-SACK 32;
  - against 𝒢_BM*'s 36.
- **Nobody has checked whether the G condition can be met.** That would need a
  clean negative that reaches as few targets as the Odyssey's 36 readings do and
  also lands a unique eclipse survivor. Nothing estimates this.
- **G_j is null-side in kind, yet it is left free.** It involves no Odyssey
  target and no truth: like G_BM, it is fixed by the sky and the readings. But:
  - C7 fixes only the Odyssey's null-side fields;
  - 9.1 places G_j after the second freeze;
  - S4's G_j (0.00051, upper bound 0.00112) is a free choice, which
    `verdict_trace.py` checks only against 3.69/n_T.
- **This is the defect R2-1 found in revision 3's S1,** now for outcome 4. If no
  clean negative can meet the G condition, then "no label 4" and P25 are a "no"
  that means nothing.

**Fix.**
- Compute G_j, with both intervals, for the 12 clean negatives at the null-side
  stage.
- Add them to C7 and to `attain.json`, and let I14(c) report whether outcome 4
  stays reachable.
- Until then, mark S4 a branch test and change 2.10 to "not ruled out".

#### N6. The search layer that produces the gate inputs has no second implementation (major)

**Where:** D 10.4 ("Every derived quantity the verdict rests on has one"); 6.1;
6.3.1–6.3.2; 6.4; 9.1 (seen_PCR, strict_PCR, seen_ALM_SL, rec_ALM_BM, held_ALM,
hit_j, G_j).

**Evidence.**
- **What the existing checks cover.** I2 and I4 check eclipse and lunar
  circumstances. I5 and I6 check the sky tables and events. I7 checks B&M's
  reading, I9 reach and G. I13 checks only that each option translates to some
  canonical predicate.
- **What nothing independent checks.** First, how `search.py` evaluates the
  control predicates:
  - linked events through exact night counts and war-years;
  - Egyptian intervals with a free epoch, and Roman free offsets;
  - Attic months and seasonal hours;
  - site boxes, discs and "none";
  - `ge_relation` with `same_apparition`, and `rel_position` with B.2's ratio.

  Second, the best-fit, narrowing and cluster logic of `harness.score`.
- **Why it matters.** These produce seven of the rule's inputs, and the margins
  are thin:
  - gate 3a sits on its threshold (N1);
  - gate 3b needs 6 of the 9 sets that keep their truth, and nobody has computed
    their narrowing (P21);
  - Q_H's margin is one set (N8).

  A single predicate bug decides a label, in either direction. PC-S cannot catch
  it, because it uses B&M's grammar only.

**Fix.** Add **I16**: a minimal independent evaluator of every counted set's
primary run, and of the B&M-type projection.
- A public-tier agent writes it from the clue files and 6.3–6.4 alone.
- It is compared on the f(c) vectors over all 21 window positions, with tie bands
  for ΔT-mixture rows near P_mix = 0.5.
- It runs before any gate count is read, and it is part of INSTR.

#### N7. Gate 3a scores Ptolemy's table-computed quantities, which revision 5 removes from gate 3b on principle (major)

**Where:** D 6.3 (`controls_real.json` "exactly as licensed"); 6.4 (A.10 and B.5
set to none); rows PB-E1/E2/E3-SUN, PA-H1/H2/H3-SUN and PA-H1/H2/H3-TIME; 7.1 H7.

**Evidence.**
- **The principle.** 6.4 sets A.10 and B.5 to "none" because a phase computed
  from stated longitudes "is more precise than any phrase, so it would make the
  control easier than the thing it calibrates".
- **Gate 3a's two Ptolemy sets score exactly that kind of quantity as primaries**
  [`controls_real.json`; me: real_rows.txt]:
  - the Sun's longitude at each eclipse, ±5° for BAB and ±3° for ALEX;
    - the rows themselves mark these as computed from Ptolemy's solar tables;
    - the drafter widened the BAB tolerance using outside knowledge of the
      length of Ptolemy's year;
  - Ptolemy's computed mid-eclipse times, ±0.5 h ("ἐπελογισάμεθα", "we
    computed").
- **The thing gate 3a calibrates carries neither.** The Odyssey's eclipse
  component has no season words and no hour words. "Noon" is not in the text
  [D 7.1 H7].
- **These two sets are the ones seen only through best-fit (N1),** so the gate
  rests on both choices at once. Whether they would still be seen with
  words-only rows has not been computed.

**Fix.**
- Give gate 3a the same words-only projection as 3b:
  - PB-*-SUN at "pm15", which uses only the words "about the end of Pisces";
  - "none" wherever the licence is a number only, which covers PA-*-SUN;
  - Ptolemy's computed mid-times at "pm1" or "none";
  - the record's own words kept ("a full hour having passed").
- Report the run with the computed quantities beside it, with a qualifier if the
  gate count differs.
- Or justify the asymmetry explicitly in 6.3.

### Minor

#### N8. held_ALM's ceiling is 7, not 8 (minor)

**Where:** D 2.6, 2.10, 6.4 ("held_ALM ≤ 8"; "Q_H needs 6 of the 8"), 9.4 C5,
P24; [AppT 2].

**Evidence.**
- 6.4 counts a set as not recovered when its truth lies outside the projection's
  pool.
- [AppT 2] records that ALM-H's truth fails `visible_only` at the printed crux.
  That row is in ALM-H's projection (`alm_rows.out.txt`: ALM-H.4,
  visible_only).
- ALM-H has four held-out rows, so it is one of the eight sets that could
  qualify, and it cannot be recovered.
- So held_ALM ≤ 7 on known truth-side numbers, and P24 needs 6 of 7.
- S0's held_ALM of 8 contradicts that truth-side fact. 9.5's "contradicts a known
  fact?" column cannot show it, rightly, because that column is public.

**Fix.**
- Record held_ALM ≤ 7 in [AppT 2, 6].
- Say in the public text "at most 8, fewer if a truth fails its projection".
- Restate P24.

#### N9. The build plan's order cannot satisfy its own access and freeze checks (minor)

**Evidence.**
- **The public copy comes too late.** The public-tier agents build code at step
  1, and must read only `build/DESIGN.public.md` and the paths in
  `access.json` [D 10.1]. But step 4 produces the public copy [D 11.2], and 12.1
  item 14 writes it "from the frozen DESIGN.md".
  - So at step 1 the agents read either the full design or nothing.
  - Their logs then cannot match `access.json`, and I13, which is in INSTR,
    fails.
- **I2b cannot run where the plan puts it.** It must run before the first
  freeze (12.1 items 2–3), and `controls.py` runs it (10.5). But 12.1 item 13
  makes `freeze.py` refuse if `results/` holds any output of 10.5's scripts.
- **The access check cannot see shell reads.** It sees only the paths an agent
  reports. Reads inside shell commands, such as `grep -r` or `cat`, are
  invisible unless the harness logs them.

**Fix.**
- Write `access.json` and the public copy first (A0 and A6), before any
  public-tier agent starts.
- Regenerate them at every design change, logging the diff. At the freeze, check
  that the frozen copy is the one last served.
- Run I2b from a tool that writes to `results/instrument/`.
- Have the orchestrator log the file reads of every tool, shell included.

#### N10. The site-"none" search as specified needs about 10⁹ evaluations per set (minor)

**Evidence.**
- For a solar row whose site is unstated, 6.3.1 searches "a 1° grid refined near
  the best point".
- 6.3.3 integrates every ΔT-dependent row over a 41-point grid for each of four
  models.
- That is about 700 eclipses × 2×10⁴ visible grid sites × 164 ΔT values, or
  about 2×10⁹ local-circumstance evaluations per set [me]. Step 16 allows 30–60
  min for all the controls.

**Fix.**
- State the shortcut: with the site free, a change of ΔT is a shift in
  longitude, so the mixture is irrelevant for site-"none" rows.
- Evaluate those rows on the eclipse's own extremal geometry (the central line,
  the limits, the sunrise and sunset curves) instead of a grid.

#### N11. The held-out pools span 2,200 years, and nothing checks that the H3 and H4 rates are stationary (minor)

**Evidence.**
- 7.2 pools candidates over −1999..+200.
- C_rel is tied to the stars, so the conditioned Day 0 drifts about 31 days
  against the equinox across the background [D 4.1]. That changes Mercury's
  apparition geometry at Day −34, and with it the chance of a conjunction 34
  days later, which is what H3 tests.
- The exactness argument of 7.2 needs exchangeability. P10 and R20 test eclipse
  status and Mercury event class, not epoch.

**Fix.**
- Add R21: the H3 and H4 rates in the early and late halves of each pool, and
  within ±700 years of −1177, with Fisher's p.
- Report p_H on a ±700-year pool as a sensitivity.

#### N12. Q_H uses the drafter's tolerance lists, which regime SL abandoned for R2-9's reason (minor)

**Evidence.**
- The held-out options take "the most lenient listed value" [D 6.4].
- Those lists are the drafter's, and the same drafter computed the slack at the
  true dates. 13 row 41 already concedes that the order cannot be settled for
  the k_days list.
- Regime SL's fix, ceilings of the measured out-of-set slack, is not applied to
  the held-out positional and elongation options.
- The held-out opposition option (A.4) is ambiguous between the two rules
  (N15e).

**Fix.**
- Set the held-out tolerances by the same leave-one-set-out ceiling rule, from
  the measured positional offsets in degrees [AppT 1].
- Report the list values as a sensitivity.

#### N13. Gate 3b holds no star-season record, although 1.3 says it covers one (minor)

**Evidence.**
- 1.3 and 6.4 name the B&M-type component as lunar phase, star season, morning
  star and Mercury turning point.
- The projection holds intervals, phases, planet rows and one equinox row. All 17
  star rows are planet–star positions, and all of them are held out [D 6.4; me:
  dump of `controls_almagest.json`].
- So C, the clue that carries 3.6 of B&M's bits [D 1.2], has no test on real
  records.

**Fix.**
- Say in 1.3, 6.4 and the verdict that the star-season component is untested.
  This is critique #3 fix 4.
- Or add a dated star-phase record, if the library holds one.

#### N14. I9(b)'s coverage bound uses the two-sided level for each side (minor)

**Evidence.**
- I9(b) passes if the coverage of G_hi and of G_lo is "each at least 0.95 −
  3 × its Monte Carlo standard error (about 0.935)" [D 6.1].
- For an equal-tailed 95% interval, each side should cover 0.975.
- The rule uses the bounds one-sidedly: G_lo ≥ 0.20 for label 2 and G_lo > 0.05
  for Q_tol.
- So the check would accept a lower bound that is too high 6.5% of the time
  instead of 2.5%.

**Fix.** Require 0.975 − 3 SE on each side, about 0.965 at 2,000 cores (SE ≈
0.0035).

#### N15. Slips and inconsistencies (minor)

- **(a)** The 2.3 table gives the 1131 BC eclipse "smag 1.0169, diameter ratio
  1.0486". Section 0 defines smag = 1.0486 for that eclipse and calls 1.0169
  smag_partial.
- **(b)** 10.4's `lunar.py` row still reads "the PC-R and ALM centuries, plus 300
  random". 6.1's I4 now covers every century.
- **(c)** The public copy still names a control's year: I2b's "about 90 s at
  −430" [D l. 2203].
  - I13(h) matches dates "in any form the truth files print it", which is ASCII
    "-430". It would miss this form, written with a Unicode minus.
  - Revision 5's `scan_truthside.py` had no pattern for it.
- **(d)** `i2b_truth.json` (12.1 item 11) has no owner in 10.1's table. A
  truth-tier agent must write it from [ctl §3].
- **(e)** A.4's held-out opposition tolerance is ambiguous. 6.4 gives held-out
  options "the most lenient listed value, as in regime SL", which is 3 d. But
  regime SL's own opposition k is the 1-d ceiling. `build_regimes.py` has to be
  mechanical.
- **(f)** B.9's projected phase class ("first quarter") is read off the measured
  92°, the same measurement its held-out row (`elongation_tol`) scores again.
  - 6.4 says B.9 "needs no coordinates". But B.7's quadrant is in its words
    (τεταρτημορίου), while B.9's is a number.
  - Give B.9's projection the word-level class: a waxing Moon, up at sunset.
- **(g)** 9.1 labels hit_j "controls … the target is not involved". But hit_j's
  threshold is M_Ody, the target's own h_tot.
- **(h)** The searcher reads `almagest_regimes.json`, so the public tier does
  too. Its per-set Mercury tolerance identifies the one set whose own record is
  the outlier, and whose truth will therefore fail [D 6.4: 5 d in one set, 6 d
  elsewhere; AppT 2]. This is inherent in leave-one-set-out; 13 row 50 should
  say so.

---

## 4. What I could not check

- **Bench code.** None exists. Every gate expectation used above (N1, N8) is the
  design's own, rough and truth-side [AppT 2, 3, 6]. The bench's lunar module may
  move the knife-edge sets either way.
- **H3 and H4 at the target.** I did not compute them, on purpose. I also did not
  read the values in `data/ephem/horizons/venus_mercury_m1177_04_10_*`.
- **The Horizons RTS internals,** beyond the cited documentation. I relied on:
  - https://ssd-api.jpl.nasa.gov/doc/horizons.html (the STEP_SIZE row);
  - https://ssd.jpl.nasa.gov/ftp/ssd/horizons_batch.txt (RTS_ONLY);
  - https://ssd.jpl.nasa.gov/horizons/manual.html.
- **The Standish table's Mars accuracy at −1999.** I did not measure it. N4's fix
  asks for that measurement.
- **Whether R-PTOL-BAB and R-PTOL-ALEX stay seen without the computed rows** of
  N7. Not computed.
- **SMH2016 Table S4.** Not read. DESIGN lists it as a pre-freeze task.
- **N10's count** is an order of magnitude only.

## 5. Files produced for this review

All are in `C:\Projects\odybench\results\critique-design-r1\v5\`. The earlier
recheck's scripts, one level up, are untouched.

| script | what it does | output |
|---|---|---|
| `dump_prereg.py` | readable dumps of the real and *Almagest* clue files | `dump_real.txt`, `dump_almagest.txt` |
| `check_licences.py` | the licence-string check (raw characters, fragments in order) and a scan of every operational field and statement for date-like content | `check_licences.out.txt` |
| `scan_public_leaks.py` | the 51 accepted dates (built from the truth files) in every printed form, searched over the public whitelist and the public part of DESIGN; year-only mentions | `scan_public_leaks.out.txt` |
| `neg_garden_sizes.py` | the product of fork-option counts per negative set | `neg_garden_sizes.out.txt` |
| `real_rows.py` | one line per `controls_real.json` row: primary option, alternatives, narrative level | `real_rows.txt` |
