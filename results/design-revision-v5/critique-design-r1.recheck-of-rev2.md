# Adversarial review of DESIGN.md, revision 2 (round 1)

Written 2026-10-04, before any bench code beyond `ephem.py`, `ccx.py` and
`calendar.py` exists. I did not write DESIGN.md or the first review.

**What I read.**
- In full: `DESIGN.md` (revision 2, 2,322 lines) and `docs/critique-design.md`.
- The control files, dumped row by row with my own scripts:
  - `data/prereg/controls_real.json` (9 sets, 78 rows);
  - `data/prereg/controls_almagest.json` (12 sets, 72 rows);
  - the eclipse-compatible rows of `negatives.json`, and AEN-TROY in full.
- The two truth files. I read them only to look for leakage, as the task allows.
- In part:
  - `docs/controls-real-drafting.md` §1 and its T2 notes;
  - `docs/controls-almagest.md` §0–1;
  - the dossier passages cited below.
- `data/ref/Table-S10.2020.txt`.
- SMH2016, through a WebFetch summary of the PMC full text only, so it is marked *secondary*.

**Tags.**
- [DESIGN §n, l. m]: revision 2, section n, line m.
- [rev #n]: the first review.
- All other dossier tags are as in DESIGN §0.
- [r1: script]: computed by me with that script in `results/critique-design-r1/`, with its `.out.txt` beside it.
- [me]: my own arithmetic or inference, shown where it is used.

**Conventions.**
- Years are historical BC with the astronomical year after them.
- Dates are proleptic Julian.
- Time scales are as in DESIGN §0.
- Quotations are under 15 words.

---

## 0. Summary

**Old issues.**
- 20 of the 25 are resolved.
- 5 are not: #1, #16, #17 and #18 for reasons new to this revision, and #3 only in part (see the table).
- The rebuild is serious work:
  - The decision rule is a pure function with synthetic tests.
  - The controls are rebuilt from the texts and licence-checked.
  - The gardens are tiered and sourced.
  - The freeze covers the code.

**New problems: 17 (1 blocker, 7 major, 9 minor).**

1. **Outcome 1 is unreachable, and outcome 2's LR clause is close to predetermined (blocker, N1).**
   - In PC-S science mode, every accepted truth gets the Odyssey's own clue set. So R_obs and G are two weightings of one reach function.
   - It follows that LR ≤ 1/P(A), where P(A) is the share of spring targets whose sky has every slot the generator demands.
   - I measure P(A) = 0.154, which caps LR at about 6.5 (95%: 5.1–9.0) [r1: check_lr_cap.py].
   - Outcome 1 needs LR_real,lo ≥ 30. That can never happen. Outcome 2 fires when LR_fav,hi < 10, which is nearly certain.
   - The verdict is therefore set by the generator's slot definitions, not by the Odyssey.
2. **Gate 3b cannot fire (N2).**
   - Its *Almagest* leg scores at tolerances set to the truth's own maxima.
   - Its PC-S leg, rec_PCS, comes to about 0.68 because two design definitions overlap.
3. **rec_ALM_BM, and so Q_BM, is undefined (N3).** The design never says which option of each row regime BM uses, and the answer decides Q_BM.
4. **The SMH ΔT spline was fitted to a counted control (N4).** R-DIOD's eclipse is −309 in Table S10 v2020. The ΔT used to score solar-eclipse controls is not specified.
5. **One answer-dependent primary is not flagged for re-drafting (N5).** T2-SEASON passes the truth (Sun at 355.3°) only because its season starts at 330°. The same set's other two season rows start at 0°.
6. **The conditioning on C is selective (N6).** DESIGN §1.1 says E and V were also formed with the eclipse in view, yet G and T0 = RE still count them.
7. **Several new predictions are already settled (N7).**
   - P23 fails as written: R_anc's own season bound excludes 30 Sep 1131 BC, when the Sun was at 176.7° [r1: check_ranc_season.py].
   - P26 restates the §2.3 table.
   - P30, P32, P41 and P42 follow from the cap above.

**Checked and not a problem.** Instrument check I11(a) can pass. In 3,104 conjunctions of 1350–1100 BC, the Moon is never above −0.8333° at the end of evening nautical twilight of the conjunction day at Troy [r1: check_i11a.py]. A failure there would have blocked every verdict.

---

## 1. The 25 issues of the first review

| # | sev. | resolved? | how, or what is still wrong |
|---|---|---|---|
| 1 | blocker | **no** | **Fixed:** the rule is a pure function of named quantities; every condition names its garden; the unreachable NC condition is replaced by pct_N4; G has one sense; I14's synthetic sets reach every branch (I checked S0–S7 by hand). **Still wrong:** outcome 1 still cannot be reached, for a new reason. Its condition LR_real,lo(BM) ≥ 30 lies above the structural cap of about 6.5 (N1). S1's input "LR 45" can never occur, so I14 proves the code's branches reachable, not the outcomes. |
| 2 | blocker | yes | **Fixed:** the critique's seven unlicensed features are gone. Every row carries licence words and the licence check was blind; Roman dates have a free offset; Livy's prodigies are a hard case. **Residual leaks of a subtler kind, raised as new issues:** an unflagged answer-dependent primary (T2-SEASON, N5); a ΔT model fitted to R-DIOD (N4); tolerances set at the truth's maxima in the *Almagest* control (N2). |
| 3 | blocker | partly | **Fixed:** the split into 3a and 3b; the *Almagest* control; Q_BM as a qualifier on every "no" and as a block on outcome 1. **Still wrong:** 3b cannot fire, because both of its legs are settled by construction (N2). Q_BM's input is undefined (N3). The case the critique feared, a method certified as able to see that cannot, survives at the slack tolerances. |
| 4 | major | yes | Local git freeze, code tree hash, dated amendments that state which outputs had been read, and an EXPLORATORY stamp for unfrozen runs [DESIGN §12]. Publishing the hash outside the machine waits on Jon's permission, as it should. |
| 5 | major | yes | §1.1 now says the 6 years is the C ∧ E rate. P8 and P9 are the critique's two comparisons, and the arithmetic (0.88 and 0.14 per century) checks out [me]. |
| 6 | major | yes | MacDonald was read, both p_fix figures are reported, and the reason is frozen in §5.1. But the same reason applies to E and V, and the design does not apply it there (N6). |
| 7 | major | yes | 𝒢_BM, 𝒢_DOC and 𝒢_FULL hold 144, 143,856 and 3,068,928 readings. The eclipse-compatible subsets hold 47,952 and 1,534,464. I reproduce every product and bit count [me]. The greedy minimal fork set is reported. |
| 8 | major | yes | F1b, a PC-S jitter of 0–3 d, and the decay curves. |
| 9 | major | yes | C_rel and E_rel; the E_rel mapping (n = 3, 4, 5 gives ≤ 4, 5, 6 Apr at −1177) checks out. |
| 10 | major | yes | h_tot, h_09 and h_06 under the four-model mixture; the background runs from −1999; the target is excluded from its own base rate; a site-rotated rate is added. The prereg files still cite the withdrawn classes (N11). |
| 11 | major | yes | Base rates are conditional on the reading; H1 and H5 are not counted; R_anc's survivors are run as well. A new defect in the counted statistic is N14. |
| 12 | major | yes | The MWRA is a vertex fit; rises converge below 0.1 s; flatness is flagged; sensitivities and I6 are added. The continuous tolerance is narrower than B&M's integer one (N13). |
| 13 | major | yes | §10.4 gives every derived quantity a second path. Every reference script it names exists (`check_mwra.py` in both folders, `bm2008-b-checks/ephem.py`, `research_visibility_calc.py`, `eclipse_local.py`, `check_bessel.py`) [checked]. |
| 14 | major | yes | The instrument mode (recall 1.000 on an independent path) is meaningful. But the science mode's rec_PCS is now a gate input, and it is definitional, which is the flaw this issue named (N2). |
| 15 | major | yes | The Iliad is a comparison; 12 clean negatives are built under the Odyssey's rules; NC4 and NC5 become I11. I11(a) holds empirically [r1: check_i11a.py]. |
| 16 | major | **no** | **Fixed:** both sides now count the same event; the LR is a curve over noise; the Venus slack is dropped. **Still wrong:** the ratio is bounded above by 1/P(A) whatever the data (N1). The claim that the denominator is a mean over "thousands of targets" is false. T_C holds about 480 targets, and few of them have reach > 0 (N8). |
| 17 | major | **no** | **Fixed:** the old determined predictions moved to §2.7. **Still wrong:** the new list has the same defect. P23 fails as written; P26 is §2.3's table with thresholds placed around it; P30, P32, P41 and P42 are settled by the cap of N1 (N7). |
| 18 | major | **no** | R_anc is pre-registered, but its primary season bound [180°, 270°) excludes 30 Sep 1131 BC (Sun 176.7°), the autumn eclipse it was added to test. It also takes the eclipse as a clue, so its "eclipse coincidence" is 1 by construction (N7, N9). |
| 19 | minor | yes | One Espenak–Meeus model, four in the mixture. |
| 20 | minor | yes | A1–A5 are labelled regression tests and I3 a calibration. But INSTR requires I3 to "pass" and I3 has no pass criterion (N15). |
| 21 | minor | yes | Pinned definitions (smag, obsc, central flag, umag, pmag). |
| 22 | minor | yes | The epoch is −1176.68; the window is half-open, built with `span_bounds`; P7 predicts the count. |
| 23 | minor | yes | The T0 grid; T0b's reading, in its C_rel/E_rel form, is a member of 𝒢_BM. |
| 24 | minor | yes | All six slips are corrected. A new slip of the same kind is N17. |
| 25 | minor | yes | HIP numbers verified; the Sirius proper motion is adopted with its 1′ model spread [DESIGN §2.1]. |

---

## 2. New issues

### Blocker

#### N1. The likelihood ratio is capped at 1/P(A) ≈ 6.5 by construction, so outcome 1 is unreachable (blocker)

**Where:** §5.7 [l. 1093–1138], §6.2 science mode [l. 1202–1228], §9.2 [l. 1707–1730], §1.3 outcomes 1–2, P41 and P42.

**Evidence: an identity that follows from the design's own text.**

1. **Every accepted poem is the Odyssey's clue set.** In science mode, each clue's *observation* day is "its stated offset plus δ". The stated offsets are the Odyssey's.
   - The poem "has the Odyssey's slots only where the sky supports them", and a truth that fails a slot "is dropped" [§6.2 steps 1–2].
   - The searcher then applies "every reading of 𝒢_BM … at the poem's stated offsets" [step 3].
   - So every accepted poem has the Odyssey's slots at the Odyssey's offsets, and every reading's survivor set S_r over the background is the Odyssey's own.
   - Hence reach(t*; 𝒢) is the Odyssey's reach function evaluated at t*.
2. **R_obs and G are two weightings of that function.** Let A(t, δ) be the event that t's sky supports every slot.
   - R_obs = E[reach(t) · 1_A] / P(A) over spring daylight targets.
   - G = E[reach(t)] over the same targets, T_C [§5.3, §5.7].
   - Therefore **LR = R_obs / G = P_w(A) / P(A) ≤ 1 / P(A)**, where P_w is the reach-weighted probability. Equality holds when every target with reach > 0 satisfies A.
   - Equality is near: all 5 spring daylight new moons that pass B&M's V and M satisfy A [r1: check_lr_cap.py].
3. **P(A) is large.** I measured it on the generator's slots, choosing every interpretation that makes P(A) smaller:
   - Venus a visible morning star (AV 7°) on Day −5;
   - Mercury within 6 d of a *morning* rise-azimuth maximum, greatest western elongation or station, or visible (AV 10°), on Day −34;
   - season and conjunction true by construction.

   Over the 266 spring daylight new moons of −1499..−1000 at Ithaki, P(A) = **0.154** (95%: 0.111–0.198), so **LR ≤ 6.5 (5.1–9.0)** [r1: check_lr_cap.py].
   - The components agree with the dossier: Venus a visible morning star on 43% of spring Day −5s [vis, table at l. 179]; mine is 0.398.
   - With the dossier's stricter Mercury figure (17% within ±5 d of an event on spring Day −34 [vis l. 64]), P(A) ≈ 0.43 × 0.17 = 0.073 and the cap is about 14 [me].
   - Either way the cap is far below 30.
4. **Consequences.**
   - Outcome 1 needs LR_real,lo(BM) ≥ 30, and also LR_real,lo(DOC) ≥ 30 whenever Q_BM holds. That cannot occur for any data. The cap applies to 𝒢_DOC too, since R_obs and G again share the Odyssey's survivor sets.
   - Outcome 2 fires on LR_fav,hi(BM) < 10, which the cap makes nearly certain. Only bootstrap noise in a small sample (N8) could lift the upper bound past 10.
   - The bench can therefore never say "yes". Its preamble rule, that a "no" about the Odyssey must come from a test that could have said "yes", fails at the bottom line.
   - S1's "LR 45" is not a realisable input, so I14 does not establish reachability.
   - The drop fraction that §6.2 already reports is 1 − P(A), the very number that caps the LR.
5. **The LR has no positive control.** No record with a known date is run through R_obs / G, so nothing shows what LR a truly observed sky earns under this machinery.

**Fix.**
1. State the identity in §5.7, and move P(A) and the cap into §2 as known numbers. They are properties of the observation model, not measurements of the Odyssey.
2. Decide what outcome 1 rests on. Either:
   - **(a)** drop the LR from outcome 1 (keep G, pct_N4 and T0) and report the cap as a finding: under a realistic observer, the Odyssey's sky words can raise the odds of Schoch's target by at most about 6.5×; or
   - **(b)** change the observation model so that a real observation can carry more information than slot presence. For example, the generator states the observed tightness and the H1 likelihood is evaluated on matching readings, in the manner of N4's T_obs. Then pre-compute its maximum, and freeze thresholds that the maximum can exceed.
3. Add an assertion to I14: the frozen generator's 1/P(A) must exceed every LR threshold the rule uses, or the freeze is refused.
4. Run the LR machinery on the *Almagest* sets, which are truly observed. That tells the reader what LR real records earn, and so what a threshold of 10 or 30 means.

### Major

#### N2. Gate 3b cannot fire: both of its legs are settled by construction (major)

**Where:** §6.4 regime SL [l. 1401–1415], §6.2 rec_PCS [l. 1222–1228], §9.2, P32 and P35.

**Evidence.**
- **The SL tolerances are the truth's own maxima.**
  - Mercury k = 6 (the truths are all within 5.5 d); oppositions k = 2 (truths within 1.81 d); Venus k = 21 (truths within 20.6 d) [§2.6; alm §4].
  - The design concedes that SL's tolerances "were measured on these same records" [l. 1410].
  - For oppositions it picks 2, not the most lenient listed value of 3. That is the smallest value that still covers the truth.
  - **Mercury's 6 is not in the file's list.** Every greatest-elongation option enumerates k_days [1, 2, 3, 5, 7, 10, 16, 21] [r1: dump_controls_almagest.txt]. §6.4 says a regime "picks one" of the listed values. So regime SL cannot be built from the file as frozen without an unrecorded edit.
- **The narrowing test is already settled by rates.** With the truth inside B guaranteed for the greatest-elongation rows, only |B| ≤ 0.05 N_cand is left. Rough independence arithmetic [me; synodic periods 584 d for Venus and 116 d for Mercury]:
  - ALM-E: Venus within ±21 d (43/584 = 7.4%) × equinox within ±2 d at +33 (5/365 = 1.4%) ≈ 0.1%.
  - ALM-F: the Venus maximum must fall 16–21 d after Day 0, about 1%.
  - ALM-D, ALM-G and ALM-L: about 0.8% each.
  - ALM-A carries many rows.

  Six counted sets therefore pass far below the 5% bound, and seen_ALM_SL ≥ 6 (P35) holds with near certainty.
- **rec_PCS is definitional.** W_BM's Venus option (visible at AV 7°) is the generator's Venus slot. W_BM's Mercury option (any of the three events within 6 d) is the generator's Mercury slot minus its "or visible" branch.
  - Among accepted truths, 28/41 have an event within 6 d [r1: check_lr_cap.py], so rec_PCS ≈ **0.68** at zero noise, against the 0.5 threshold.
  - Both generator and searcher are bench code on one ephemeris, so the number says nothing about sight. This repeats the flaw of review issue #14 inside a gate.
- **The same records do four jobs.** The *Almagest* truths calibrate 𝒢_DOC's F5 6-d option, ν_real's s_M = 3, the PC-S generator's 6-d slot and the SL regime, and then they validate the method. That is training and testing on one set.

**Fix.**
1. Set SL tolerances by leave-one-set-out: the maximum over the *other* sets' records. Or set them from an outside source (e.g. de Jong's Babylonian slack [vis §2]) and freeze them before scoring.
2. Score gate 3b on held-out sets only.
3. Remove rec_PCS from the gate, or compute it with the instrument-mode independent path and a generator whose slot rules differ from W_BM's.
4. Record the regime values in the file by a dated edit.

#### N3. rec_ALM_BM is undefined: regime BM never says which option of a row it uses (major)

**Where:** §6.4 "The B&M-type projection" and "regime BM" [l. 1391–1424]; Q_BM; P36.

**Evidence.**
- Regime BM picks *values* (k = 1, lead 90 min, middle values) but not *options*. Many planet rows offer `ge_true_k`, `ge_mean_k`, `visible_only`, `bm_mwra_k` and `bm_venus_lead` [r1: dump table].
- "B&M's method as written" [l. 1421] would point to B&M's own proxies (`bm_mwra_k`, `bm_venus_lead`). The projection's list admits all of them.
- **The choice decides Q_BM.**
  - Under the greatest-elongation options at k = 1, the true dates pass in only ALM-A (as printed) and ALM-E among the counted sets that carry such a row [§2.6]. The three sets without one are B, I and J. So rec_ALM_BM ≤ 5 < 6, and **Q_BM holds before any run**.
  - Under the *primary* options, ALM-H and ALM-K have only `visible_only` Mercury rows: Ptolemy's greatest-elongation label for the old records is a fork [alm l. 277]. Those sets can pass strict recall, so Q_BM is open.
- So P36 is either known or a real prediction, depending on a choice the design does not make.

**Fix.** Name the option rule for regime BM: for example, "B&M's proxy where the row offers it, else the greatest-elongation option at k = 1, else the primary". Freeze it. If the result is known, move Q_BM into §2.

#### N4. The ΔT that scores the solar-eclipse controls is unspecified, and SMH2020 was fitted to a counted control (major)

**Where:** §0 (time scales), §6.3, `eclipses.local(…, dt_s)` [§10.2], and I2b.

**Evidence.**
- **Unspecified for solar eclipses.** §0 fixes SMH2020 ΔT for lunar quantities. It names no ΔT for a solar-eclipse control's smag, its LAT of maximum, or its contacts.
  - The drafter's own truth check used SMH2020 [truth file, conventions].
- **The SMH tables contain the control records.**
  - Table S10 v2020 (untimed total and annular eclipses) lists −309 "Greek", bounds 13,300–17,160 s [`data/ref/Table-S10.2020.txt`]. By year and region that is the eclipse of R-DIOD (15 Aug 310 BC), my identification.
  - It also lists −187 "Europe", 12,590–12,900 s: Livy's L4, 17 Jul 188 BC.
  - SMH2016 §2b(iv) used Thucydides' 431 BC and Agesilaus' 394 BC eclipses to "set fairly useful limits to ΔT" (WebFetch summary of the PMC text, *secondary*). These are R-THUC's T1 and R-XEN's X3.
- **The consequence.** Scoring R-DIOD's D-ECL (smag ≥ 0.95 within 150 km of Syracuse) with SMH2020 partly re-reads the constraint that built SMH2020.
  - R-DIOD is one of the four sets P33 expects seen, and gate 3a sits exactly at 4.
  - The S10 interval is wide (3,860 s), so the pass is probably robust. But the design neither says so nor checks it.
- **The lunar side, for contrast.** Per the same summary, the *Almagest* Babylonian triple was "retained … as a separate set" and Ptolemy's own Alexandrian timings are not among the timed data. Neither looks circular.

**Fix.**
1. Specify the solar-eclipse ΔT for controls. Use the four-model mixture as for h_tot, scored as P(row passes).
2. Mark R-DIOD (and L4) as circular under SMH2020.
3. Report gate 3a with R-DIOD scored under a ΔT that does not use it (Espenak–Meeus, or the mixture with its σ widened), and without R-DIOD.
4. Check SMH2016's Table S4 and §4b before the freeze, to confirm the *Almagest* triple is not in the fit.

#### N5. An answer-dependent primary is not flagged, and Q_exposure in effect tests one counted row (major)

**Where:** `controls_real.json` R-THUC; §6.3.3; §2.6.

**Evidence.**
- **T2-SEASON's primary is the only one that admits the truth.**
  - Its primary "early" spans [330°, 60°] of solar longitude, a span whose start and width are both the drafter's choice [file, T2-SEASON justification].
  - The same set's T1-SEASON and T3-SEASON use the half-year [0°, 180°], citing Thuc. 5.20.3.
  - The accepted date, 21 Mar 424 BC, has the Sun at 355.3°. "The 'half-year' alternative fails" [controls_real_truth.json, R-THUC].
  - The drafter states that it knew "the conventionally cited years of most of these eclipses" from background knowledge [pcr §1 item 3]. The 424 BC date is among the best known.
  - The row is not among the three flagged as possibly steered.
- **T-INT-12 shows the same tension.** Its ±0.5-year tolerance is justified by both events lying "in summer halves". The truth gives 6.63 years, "near the edge", and T2 lies outside the half-year summer.
- **Q_exposure has little to measure.**
  - L4-DARK, one of the three re-drafted rows, sits in H-LIVY, which is reported and not counted. Its re-draft cannot change seen_PCR,redraft.
  - R-THUC is predicted unseen whatever T1-DARK says, because its site primaries are "none" (P33).
  - So Q_exposure can flip only through D-ECL.

**Fix.**
1. Add T2-SEASON (and T-INT-12's tolerance) to the unexposed re-draft.
2. Have the re-drafter, or an exposure audit, list every row whose primary passes the truth while a sibling convention fails it.
3. Report gate 3a with each such row at its sibling convention.
4. State in §6.3.3 that the re-draft controls exposure to files only. A language-model drafter's knowledge of famous dates is not removed.

#### N6. The season is conditioned on, but the equinox and Venus readings, also formed with the eclipse in view, are not (major)

**Where:** §1.1 "Where the clues came from" [l. 185–193]; §5.1 item 6; §5.3 (G over T_C); §9.2 (T0 ∈ {R, RE}).

**Evidence.**
- **The design's own sourcing.** MacDonald 1967, the first spring reading, "already cites the eclipse, shifts his timetable a week to meet it, and checks Venus in the eclipse year; the equinox reading E is also his". Also: "No clue in N ∧ C ∧ V ∧ M was formulated blind" [l. 185–193].
- **The frozen reason for conditioning on C** is that the reading "was formed with the target in view, so the target's agreement with it is not part of the coincidence" [l. 917–921].
- **Applied unevenly.** By that reason, E and V belong out of the coincidence too. Instead:
  - 𝒢_BM counts E_rel (F6) and the Venus lead as discriminating clues;
  - outcome 1 accepts T0 = RE, a reproduction that holds only with MacDonald's eclipse-fitted equinox bound.
- **Direction of the bias.** The selective conditioning makes G_BM smaller (more favourable to B&M) by about the pass rates of E and V. It can therefore suppress label 2.

**Fix.**
1. Apply the principle uniformly: condition G on every clue the record shows was formed or tuned with the target in view (C, E, and the Venus identification). Or freeze an argument for why C differs.
2. Report G under both conditionings.
3. Do not let T0 = RE count towards outcome 1 if E is target-informed.

#### N7. Several new predictions are already settled, and one fails as written (major)

**Where:** §8: P23, P26, P30, P32, P36, P41 and P42.

**Evidence.**
- **P23 fails under R_anc's primary season.**
  - R_anc requires the Sun's apparent longitude on Day 0 in [180°, 270°) [l. 962–964].
  - At the conjunction of 30 Sep 1131 BC (10:30 UT) the Sun stood at **176.69°**, and the autumnal equinox of −1130 fell on 3 Oct at 17:17 UT [r1: check_ranc_season.py].
  - So the survivors cannot include 1131 BC, which P23 predicts. Only the sensitivity range [150°, 300°) admits it.
  - The same bound also excludes 12 Jan 1183 BC (282.2°). It admits 30 Oct 1207 BC (206.7°).
- **P26 restates the §2.3 table** with its thresholds placed around the known canon-frame values:
  - "≤ 0.06" for 0.047, 0.052 and 0.049;
  - "≥ 0.08" for 0.108;
  - the per-model orderings, already in the table.

  Only the change to the DE431 frame (about 40 s [rev #17]) is new.
- **P30 is near-certain.** Among accepted truths, B&M's V ∧ M passes in 5/41 = 0.12 [r1: check_lr_cap.py], against P30's "at most 70%".
- **P32 holds by the definitional overlap** of N2 (about 0.68 ≥ 0.5).
- **P41 and P42 follow from N1.** LR_real,lo < 30 is certain, and "the verdict contains no 1" is certain.
- **P36 is known or open,** depending on N3.

**Fix.**
1. Move P26, P30, P32, P41 and P42 into §2 as known, or as regression expectations.
2. Restate P23 with a season bound justified from the ancient sources (see N9), or record that it fails under the current bound.
3. Resolve N3 before deciding P36's status.

#### N8. R_obs and G rest on few targets, and the rule uses point estimates of G (major)

**Where:** §5.3 (T_C), §5.7 [l. 1111–1113], §6.2 truth pools, and §9.2.

**Evidence.**
- **T_C is small.** It holds about **480** targets, not "thousands": 266 spring daylight new moons in 500 years at Ithaki gives 0.53 a year, × 898 core years = 478 [r1: check_lr_cap.py; me].
  - G is the mean of a quantity that is 0 for nearly all of them. At G ≈ 0.01 that means a handful of targets with reach > 0.
- **R_obs's pool is smaller still.**
  - Pool (iii) is the spring part of 2,000 daylight truths: about 170, given 8.5% spring [me].
  - About 26 of those survive the slots (0.154) in each noise cell.
  - Of those, about 12% pass B&M's V ∧ M [r1].
  - The bootstrap bounds of the LR come from a few non-zero values.
- **Point estimates of G go into the rule.** The rule compares G_BM with 0.01 and 0.05 as point estimates, although §9.2 says "intervals work against the claim being made".
- **LR(DOC) mixes reach definitions.**
  - Its numerator is reach_136 [§5.7], while G_DOC in the rule is the max over W [§5.3].
  - G for the LR is taken on the 1,000-reading subsample, while the rule's G_DOC uses the full garden.

**Fix.**
1. Compute R_obs exactly, as Σ_t reach(t) P(A_t) / Σ_t P(A_t) over all of T_C, enumerating δ, instead of by sampling.
2. Give G an exact binomial or bootstrap interval, and use its upper bound in outcome 1 and its lower bound in outcome 2.
3. Use one reach definition (W and garden) on both sides of every ratio.

### Minor

#### N9. R_anc's season bound is the design's, not the scholia's, and its eclipse is a clue (minor)

**Where:** §5.3, R_anc.

**Evidence.**
- [180°, 270°) is the modern astronomical autumn. It is not what "autumn turning to winter" meant to a Greek reader, and the design gives no ancient source for the 180° start. That start is what excludes 1131 BC (N7).
- R_anc also requires h_06 ≥ 0.5 on Day 0. Its survivors are therefore eclipses by construction, so "their h_tot" measures nothing about a coincidence.

**Fix.**
1. Source the season bound from an ancient definition, such as the morning rising of Arcturus as the start of autumn.
2. Report R_anc both with and without the eclipse clue. Only the version without it gives a coincidence to compare with B&M's.

#### N10. pct_N4 and G are different quantities, so P25 compares unlike numbers (minor)

**Where:** §5.4 [l. 1033–1040], P25.

**Evidence.**
- G is a *mean* reach over targets.
- pct_N4 is a *tail fraction*, P(r_e ≥ r_Ody), over epics.
- "Under the null they estimate the same probability" is not true. The analogue of G with the poem varied is E_e[r_e], the mean reach over epics.

**Fix.** Compare G_BM with E_e[r_e] in P25. Keep pct_N4 in the rule as the percentile it is.

#### N11. The withdrawn eclipse classes are still cited in all three prereg files (minor)

**Where:** `controls_real.json`, `negatives.json`, and the `solar_eclipse` predicate [§10.3].

**Evidence.**
- `controls_real.json` policy 3, and the options of T1-DARK, D-ECL, L3 and L4-DARK, justify thresholds by "DESIGN 3.1: X3 ≥ 0.95, X4 ≥ 0.60". Revision 2's §3.1 is now the T0a replay. These rows carry numbers, so they still work.
- `negatives.json` QS-SACK-06:a and IL-PATROCLUS-02 (solar_am, solar_any) require "a solar eclipse of class X1–X4 (DESIGN 3.1)" with no numbers. The translation into `operational_map.json` would have to invent them.
- **QS-SACK-06:a can never hit.** It is listed as eclipse-compatible, but it puts the eclipse near Cape Caphereus on Day +2..+12. hit_j asks for the h_tot of the *Day-0* survivor at Troy.

**Fix.**
1. Define the old classes in terms of h_tot or smag in `operational_map.json`, as a recorded decision.
2. Drop QS-SACK-06:a from `eclipse_compatible_options`, or define its hit at its own day and site.

#### N12. Interfaces that cannot be built as specified, and an under-estimated build (minor)

**Where:** §10.2 and §11.2 step 2.

**Evidence.**
- **T0b cannot be run through the interfaces.**
  - `events.conjunctions` is fixed to DE431, but T0b uses DE441 for the Moon [§3.2], and A4 checks the conjunctions to the minute.
  - `sky.build` has no refraction switch, yet T0b's M sensitivity turns refraction on and off.
  - The constant-ΔT clock only works if `dt_model` accepts a constant.
- **The pool row has one Day-0 date.** `POOL_DTYPE` carries one `day0_jdn`, but F2 (a) and (b) use different clocks.
- **The sky tables are large.** A full-span table (555,180 days) needs about 0.86 GB per site, by the array list of §10.2 [me]. Over about 17 sites that is about 15 GB, and §10 does not say which sites need the full span.
- **The evaluation count is low.** The "170 evaluations a day" omits rise and set for the 21 stars of `data/stars.json`. That adds about 170 more, so step 2 is closer to 3–5 h than 1.5–3 h [me].

**Fix.**
1. Add `ephemeris=` to `events.conjunctions`, and `refraction=` and a constant-ΔT option to `sky.build`.
2. Carry one Day-0 date per clock in the pool.
3. Give each site its span in `sites.json`.

#### N13. The primary MWRA tolerance is narrower than B&M's (minor)

**Where:** §3.2 step 5 and the T0 primary cell.

**Evidence.**
- An integer |Δ| ≤ 1 day corresponds to a continuous |Δ| of up to about 1.5 d, because the vertex lies within half a day of the discrete maximum.
- The primary MWRA_vtx test is |Δ| ≤ 1, which cuts the M window to about 2/3 of B&M's.
- 1178 BC (Δ ≈ +0.7) and 1189 BC (about +0.5) pass either way, but the M rates, p_fix and G_BM change.

**Fix.** Report the vertex test at ±1.5 d as the B&M-equivalent, beside ±1.

#### N14. H3a and H3b are nearly one event in the counted held-out statistic (minor)

**Where:** §7, "The counted statistic".

**Evidence.**
- Mercury within ±3 d of conjunction with the Sun (H3b) almost always means Mercury not visible at AV 10° (H3a).
- The Poisson-binomial treats the two as independent trials, which double-counts H3.

**Fix.** Count H3 once (H3a ∧ H3b), or use the joint conditional base rate.

#### N15. INSTR cannot be evaluated as written (minor)

**Where:** §6.1 and §9.1.

**Evidence.**
- INSTR requires I1–I14 to "pass", but I3 is "a calibration, not a validation" and has no pass criterion.
- I2b compares magnitudes with Horizons-based reference values without naming the ΔT or frame for each side. Near magnitude 1 the comparison depends on that choice.

**Fix.**
1. Exclude I3 from INSTR, or give it a criterion.
2. Name I2b's ΔT and ephemeris on both sides.

#### N16. The re-drafter's isolation leaks in three ways (minor)

**Where:** §6.3.3.

**Evidence.**
- The "conventions and policies" the re-drafter needs sit in `controls_real.json` beside the options it must not see.
- §8 (P33, P34) and §13 and §14 are not on the exclusion list. P34 tells it which counted sets' current primaries pass the truth (R-THUC and R-DIOD among them).
- Its background knowledge of famous dates is not controlled (N5).

**Fix.**
1. Give the re-drafter an extract of the conventions and the text rows only.
2. Exclude §8 and §13–14.
3. Say plainly that the test controls file exposure only.

#### N17. Factual slip: Alexandria is not the only observing place the *Almagest* names (minor)

**Where:** §6.4, default site [l. 1385–1389].

**Evidence.** The design says Alexandria is "the only observing place the *Almagest*'s records name". IV.6.3 names Babylon (licence words "ἐκ τῶν ἐν Βαβυλῶνι τετηρημένων", used in R-PTOL-BAB) [r1: dump_controls_real.txt].

**Fix.** Correct the sentence; the default-site decision itself is unaffected.

---

## 3. Checks that passed

| claim | how checked | result |
|---|---|---|
| Garden sizes 144 / 143,856 / 3,068,928; eclipse-compatible subsets 47,952 / 1,534,464; 7.2, 17.1 and 21.6 bits; F5 = 37 | products of the §5.3 option counts [me] | confirmed |
| Bit budget 10.75 bits; 1,683 × 0.083 × 0.158 × 0.044 = 0.97 | [me] | confirmed |
| B&M's own arithmetic: 0.88 and 0.14 per century | [me] | confirmed |
| Synthetic sets S0–S7 give their stated labels | traced through §9.2 by hand [me] | all eight confirmed |
| Target core −1748..−851; control windows −856..+272 and −407..+277 | from B and the anchor dates [me] | confirmed |
| I11(a), "zero survivors", is attainable | 3,104 conjunctions, 1350–1100 BC, Troy; Moon centre never above −0.8333° at the end of evening nautical twilight of Day 0 [r1: check_i11a.py] | holds (by astronomy, not by logic: a conjunction early on Day 0 is not excluded in principle) |
| Every reference script for I2 and I5–I7 exists | file listing [checked] | confirmed |
| §2.6's PC-R facts (strict failures in BAB, ALEX and PYDNA; all primaries pass in THUC, XEN, ARBELA and DIOD; the three self-flagged rows) | `controls_real_truth.json` | match, apart from T2-SEASON (N5) |
| IV.6.14 counted once (ALM-C reported only) | ALM-C = IX.8.3 + IV.6.14 | confirmed |
| E_rel n = 3, 4, 5 gives ≤ 4, 5, 6 Apr at −1177 | equinox 1 Apr 15:31 UT+2 [bm §9] | confirmed |
| Sun's longitude at the conjunction: 16 Apr 1178 BC 14.28°; 30 Oct 1207 BC 206.70° | [r1: check_ranc_season.py] | for reference |

## 4. What I could not check

- **SMH2016's data tables.** I have only a WebFetch summary of the text. It says the *Almagest* Babylonian timings were kept as a separate set, and that Thucydides' 431 BC and Agesilaus' 394 BC eclipses set limits on ΔT. Table S4 and the fitting section should be read before the freeze (N4).
- **When the *Almagest* k_days list was written.** The note says only the set *composition* was fixed before the DE441 comparison [alm l. 45]. I cannot tell whether the list [1, 2, 3, 5, 7, 10, 16, 21], whose top value 21 matches the measured Venus maximum of 20.6 d, came before or after it.
- **The approximations in check_lr_cap.py.**
  - Rise-azimuth maxima are taken from a daily declination series, good to about 1 d at a 6-d tolerance.
  - Rises come from a 3-minute grid.
  - The approximate B&M M passes 4.5% of spring Day −34s, against the dossier's 4.4% (6/136).
  - The cap's conclusion (≤ 14 even on the dossier's stricter Mercury rate) does not depend on these details.
- **I11(a) elsewhere.** I checked Troy over 1350–1100 BC only, not the 20 extra window positions or the background.
- **ν_real's displacement s_M.** I did not model it in P(A). It changes R_obs, not the cap.

## 5. Files produced

All are in `C:\Projects\odybench\results\critique-design-r1\`:

| file | what it does |
|---|---|
| `check_lr_cap.py`, `.out.txt`, `.rows.tsv` | P(A) for the PC-S generator's slots over the spring new moons of −1499..−1000 at Ithaki, the cap 1/P(A), and B&M's V and M rates among accepted truths |
| `check_ranc_season.py`, `.out.txt` | the Sun's apparent longitude at four conjunctions, and the autumnal equinox of −1130 |
| `check_i11a.py`, `.out.txt` | the survivors of AEN-TROY's R-ii-literal reading at Troy (I11(a)) in the reproduction and primary windows |
| `dump_controls.py`, `dump_controls_real.txt`; `dump_almagest.py`, `dump_controls_almagest.txt` | row-by-row dumps of the two control files (read-only) |
