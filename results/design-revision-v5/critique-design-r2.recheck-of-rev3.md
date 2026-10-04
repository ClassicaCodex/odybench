# Adversarial review of DESIGN.md, revision 3 (round 2)

Written 2026-10-04, before any bench code beyond `ephem.py`, `ccx.py` and
`calendar.py` exists. I did not write DESIGN.md or either earlier review.

**What I read.**
- In full: `DESIGN.md` (revision 3, 3,191 lines), `docs/critique-design.md`
  and `docs/critique-design-r1.md`.
- The three clue files: `controls_real.json` and `controls_almagest.json`,
  scanned row by row with my own script, plus the eclipse-compatible sets of
  `negatives.json`.
- The truth files. I read them only to look for leakage, as the task allows.
- The scratch work behind revision 3 (`results/design-revision-r2/`) and r1's
  scripts and outputs.
- In part:
  - `docs/controls-almagest.md` §4–5;
  - `docs/research-visibility.md` §2.3;
  - NASA's `data/jsex/program.js`;
  - `data/jsex/sites/ithaca.jsonl`.

**Tags.**
- [D3 §n, l. m]: revision 3, section n, line m.
- [rev #n]: the first review.
- [r1 Nn]: the recheck of revision 2.
- All other dossier tags are as in DESIGN §0.
- [r2: script]: computed by me with that script in
  `results/critique-design-r2/`, with its `.out.txt` beside it.
- [me]: my own arithmetic or inference, shown where it is used.

**Conventions.**
- Years are historical BC with the astronomical year after them.
- Dates are proleptic Julian.
- Time scales are as in DESIGN §0.
- Quotations are under 15 words.

**Numbering for the structured result.** The first review's issues keep
their numbers 1–25. The recheck's N1–N17 are numbered 26–42, which is the
order DESIGN §14 uses. My new issues are R2-1 to R2-12.

---

## 0. Summary

**Old issues.**
- 22 of the first review's 25 are resolved. Three are not:
  - #1: outcome 1 is unreachable again, for a new reason (R2-1);
  - #17: the new prediction list again holds settled items (R2-5);
  - #21: the pinned magnitude is mislabelled as NASA's, and the I2 check compares unlike quantities (R2-7).
- #18 is resolved in substance, with a post-hoc caveat (R2-11).
- 16 of the recheck's 17 are resolved. N1 is not: the likelihood ratio has
  left the rule, but the bench still cannot say "yes" (R2-1).

**New problems: 12 (1 blocker, 4 major, 7 minor).**

1. **Outcome 1 is unattainable, and the verdict would not say so (blocker,
   R2-1).**
   - G_BM is a property of the garden 𝒢_BM* and of Ithaca's sky. It does not
     depend on any measurement of the Odyssey.
   - I estimate it at **0.140 (95%: 0.087–0.215)** over the design's own core
     and pool [r2: check_gbm.py]. Even T0b's single reading gives G 0.020,
     with an upper bound of 0.061.
   - Outcome 1 needs G_BM,hi ≤ 0.05, so it cannot occur for any data.
   - Q_attain and `freeze.py` test only the floor 3.69/n_A, which is the bound when no target is reached. They will pass,
     and the verdict will omit "could not have said yes".
   - The design's own numbers already imply this: §1.2's "about 3.0 bits
     remain", and P14's lower bound of 0.05, which is the outcome-1 threshold.
2. **The width of the slots that define T_A sets G_BM (major, R2-2).**
   - G_BM over T_A equals G over T_C divided by P(A | T_C).
   - Defensible alternative slots move G_BM from 0.14 to 0.18–0.33. The tightest one crosses the label-2 bound and
     the Q_attain floor [r2: check_slot_scaling.py].
3. **Label 2 versus "inconclusive" hangs on one candidate and a tie rule
   (major, R2-3).**
   - If r_Ody = 0, as P12 predicts, pct_N4 = 1 by ties and label 2 fires.
   - My estimate is r_Ody = 11/136. The deciding candidate is 26 Mar 1111 BC, with ΔMWRA ≈ 2.3 d against a tolerance of 1.5 d.
4. **INSTR contains checks that will fail without a bug and so block the
   verdict (major, R2-4).**
   - I10b compares two different estimands, on a pool of about 140 truths that the design calls 2,000.
   - I7 demands identical flags at continuous thresholds.
5. **Settled predictions again (major, R2-5).**
   - These are already determined or close to it: P12 (expected to fail), P19 (9 survivors against "≥ 2"), P32, P33 and P35.
   - P4 and P6 sit near their thresholds.

**Checked and not a problem.**
- The pool identity of 4.2 holds: no survivor of any of the 36 readings lies outside T_A.
- P(A | T_C) is 0.147 on the full core.
- Every licence string in both control files is found verbatim (125 and 54).
- No date leaks into the operational fields.
- The three clue-file hashes match §12.4.
- The rule gives the stated labels for all twelve synthetic sets, traced by hand (section 4).

---

## 1. The 25 issues of the first review

| # | sev. | resolved? | how, or what is still wrong |
|---|---|---|---|
| 1 | blocker | **no** | **Fixed:** the rule is a pure function of named quantities; every condition names its garden and its pool; the NC condition is replaced by pct_N4; G has one sense; Q_attain and C1–C6 are new. **Still wrong:** outcome 1 is unreachable for a reason the structural constraints do not encode. Its G condition depends on the sky alone, and that is already about 0.14 (R2-1). S1's G_BM of 0.0065 with k_A = 3 cannot occur when T0b's single reading already reaches 4 targets of T_A. So I14 again proves a code branch reachable, not an outcome. |
| 2 | blocker | yes | `controls_real.json` is unchanged since the recheck (SHA-256 `135fba67…83f8`, verified). All 125 licence strings occur verbatim in their cited rows. Date-like strings outside the licence words are only the Roman calendar names the texts give (*pridie Nonas Septembres*, the Ides of March) [r2: check_prereg_leaks.py]. The re-draft and the sibling audit address the recheck's subtler leaks. The audit as written can flip for reasons that are not exposure (R2-10). |
| 3 | blocker | yes | Split into 3a and 3b. Leave-one-set-out tolerances mean no set is scored with its own records. B&M's option rule is named, so Q_BM is defined, and it is known to hold (rec_ALM_BM ≤ 5). Gate 3b can now fire: ALM-G and ALM-H lose their truths, and narrowing is open. Residuals: the rule is undefined when no listed value covers the out-of-set maximum, and the grid's 21-d value post-dates the slack measurement (R2-9). |
| 4 | major | yes | Git freeze, code tree hash, dated amendments; unchanged and adequate. |
| 5 | major | yes | P4 and P5 are the two comparisons. P4's lower bound, 0.44 per century, sits near my estimate of 0.55 per century (R2-5). |
| 6 | major | yes | MacDonald was read and the conditioning is now uniform. The uniform rule created the slot-width dependence of R2-2. |
| 7 | major | yes | The tiers are sourced. I reproduce the sizes 36, 35,964 and 767,232 [me: 2×18; 4·3·3·3·3·37·3; 8·6·4·6·6·37·3]. In my estimate the visibility fork never separates passers from failers among spring Day −34s within 3.5 d of a morning event: every one is visible at AV 10°. So 18 of the 36 BM readings duplicate the other 18 [r2: check_gbm.py]. That is harmless for G but worth recording. |
| 8 | major | yes | F1b and the PC-S jitter study. |
| 9 | major | yes | C_rel and E_rel. My calibration reproduces A(−1177) = 17 Feb and P(−1177) = 4 Apr at h_A = 2.04° and h_P = 0.92° [r2: check_gbm.py]. h_P is a geometric fit to B&M's printed date, not a visibility: a magnitude-2.9 star is not seen at 0.9°. The design says the fit is to printed bounds (4.5), so this is a note, not an issue. |
| 10 | major | yes | Hit strengths come from the mixture, the background runs from −1999, and the target is excluded from its own base rate. |
| 11 | major | yes | Conditional base rates; H1 and H5 not counted; H3 counted once. |
| 12 | major | yes | Vertex fit, ±1.5 d as primary, flatness flags. The ±1.5 d continuous tolerance makes exact-flag checks fragile (R2-4). |
| 13 | major | yes | Every derived quantity has a second path (10.4). Three of the cross-checks cannot pass as specified: I2(a) (R2-7), and I7 and I10b (R2-4). |
| 14 | major | yes | PC-S feeds no rule. The science mode's pool and its check I10b are inconsistent (R2-4). |
| 15 | major | yes | The Iliad is a comparison and 12 clean negatives exist. Only AEN-TROY, ARG-RETURN and QS-SACK have eclipse-compatible options, so outcome 4 rests on those three sets. |
| 16 | major | yes | No likelihood ratio enters the rule. The sample-size worry now applies to G: its interval treats dependent reaches as independent counts (R2-6). |
| 17 | major | **no** | The old settled items moved to §2.7. The new list again holds items that existing numbers settle or nearly settle: P12, P19, P32, P33 and P35, and P4 and P6 at their thresholds (R2-5). |
| 18 | major | yes | R_anc is pre-registered, with a sourced season and runs with and without the eclipse. The primary bound was chosen after the Sun's longitude at 30 Sep 1131 BC was known (R2-11). With the eclipse clue, R_anc has about 9 survivors in the reproduction window, so it dates nothing (R2-5). |
| 19 | minor | yes | One Espenak–Meeus model, four in the mixture. |
| 20 | minor | yes | A1–A5 are regression tests and I3 is outside INSTR. |
| 21 | minor | **no** | The definitions are pinned, but §0 calls smag, (L1′ − m)/(L1′ + L2′), "NASA's magnitude". NASA's `program.js` replaces it with the Moon/Sun ratio for total and annular eclipses (lines 534–537). So I2(a)'s "smag within 0.0005" of `program.js` cannot pass at central eclipses, as with 1131 BC (1.0169 against 1.0486). The two definitions also differ at annular eclipses near the 0.95 threshold (R2-7). |
| 22 | minor | yes | Epoch −1176.68, half-open window, R6. |
| 23 | minor | yes | The T0 grid, and T0b's reading is a member of 𝒢_BM*. |
| 24 | minor | yes | All earlier slips corrected. New slips are in R2-7 and R2-4. |
| 25 | minor | yes | HIP numbers verified; Sirius uses the barycentric proper motion. |

## 2. The 17 issues of the recheck (numbered 26–42)

| # | r1 | sev. | resolved? | how, or what is still wrong |
|---|---|---|---|---|
| 26 | N1 | blocker | **no** | The LR part is resolved: no likelihood ratio is a rule input, and the ceiling is a standing finding. The substance of N1 is not resolved. The bench still cannot say "yes", now because G_BM is about 0.14 by the sky alone. Fix 3, the reachability assertion, was generalised to the wrong floor: Q_attain tests 3.69/n_A (R2-1). |
| 27 | N2 | major | yes | Leave-one-set-out SL tolerances; rec_PCS removed from the gate; regime values in `almagest_regimes.json`. Caveats in R2-9. |
| 28 | N3 | major | yes | The option rule is named. Q_BM holds, as regression expectation R9. |
| 29 | N4 | major | yes | The mixture scores every ΔT-dependent row. The circular sets are listed. Q_ΔT uses σ × 3, and `deltat_circular.json` is a pre-freeze task. |
| 30 | N5 | major | yes | Re-draft of five rows plus a sibling audit. The audit's transplant rule needs narrowing (R2-10). |
| 31 | N6 | major | yes | Conditioning on C, V and M, with E left out and T0 = R required. The resulting pool's slot widths are unanchored (R2-2). |
| 32 | N7 | major | yes | The seven listed predictions are moved or restated. The class of problem recurs in new items (R2-5). |
| 33 | N8 | major | yes | Exact R_obs, a gamma interval for every G, one reach definition, a longer background. The interval's independence assumption remains (R2-6). |
| 34 | N9 | minor | yes | The season comes from Hesiod and Geminus, and R_anc runs with and without the eclipse. The post-hoc caveat is R2-11. |
| 35 | N10 | minor | yes | Ē_N4 is compared with G_BM; pct_N4 stays a percentile. |
| 36 | N11 | minor | yes | The X-class mapping is recorded, and QS-SACK-06:a is scored at its own day and site. G_j for such a reading is undefined (R2-12). |
| 37 | N12 | minor | yes | `ephemeris=`, `refraction=`, a constant ΔT, one Day 0 per clock, and spans per site. |
| 38 | N13 | minor | yes | ±1.5 d continuous is the primary tolerance. |
| 39 | N14 | minor | yes | H3 is one predicate. |
| 40 | N15 | minor | yes | I3 is out of INSTR, and I2b names both sides. INSTR now contains other checks that can fail without a bug (R2-4). |
| 41 | N16 | minor | yes | Brief-only re-drafter; the exposure limit is stated. |
| 42 | N17 | minor | yes | Corrected. |

---

## 3. New issues

### Blocker

#### R2-1. Outcome 1 cannot be reached for any data, and Q_attain will not say so (blocker)

**Where:** §1.3 outcome 1 [D3 l. 308–322]; §2.8 "What the known numbers
already imply" [l. 765–777]; §5.3, rule quantities [l. 1276–1285]; §9.2
[l. 2329–2336]; §9.4 C6 [l. 2402]; §9.5 S1 [l. 2420]; §12.1 item 11
[l. 2892–2896].

**Evidence.**

1. **G_BM does not measure the Odyssey.** G_BM is the mean reach over T_A
   (16 Apr −1177 excluded) of the 36 readings of 𝒢_BM* [l. 1257–1262]. It is
   fixed by the readings' clue definitions and by Ithaca's sky. No
   Odyssey-specific measurement (T0, r_Ody) enters it. In outcome 1 the
   Odyssey's own data enter only through T0 and pct_N4.
2. **Its value is already about 0.14.** I rebuilt the rule's pool and garden
   independently [r2: check_gbm.py; approximations in section 5]:
   - the background −1999..+200, with 27,212 conjunctions;
   - C_rel calibrated to 17 Feb and 4 Apr at −1177;
   - the 36 readings: day count × {MWRA, GWE, morning station} × {1.5, 2.5, 3.5} d × visibility;
   - the slots of 4.2;
   - the core −1748..−51;
   - reach as |∪ I_r(t)|/W with W = 136 years;
   - the Fay–Feuer interval exactly as 5.3 writes it.

   | readings | G over T_A | 95% interval | targets reached |
   |---|---|---|---|
   | T0b's reading alone (seq, MWRA_vtx ±1.5 d, visibility off) | 0.020 | 0.004–**0.061** | 4 / 131 |
   | sequential MWRA, all tolerances (6) | 0.032 | 0.012–0.076 | 10 / 131 |
   | sequential, all events (18) | 0.121 | 0.073–0.192 | 25 / 131 |
   | **𝒢_BM*** (36) | **0.140** | **0.087–0.215** | 26 / 131 |

   - Pool: n_TC = 892 and n_A = 131 (P(A | T_C) = 0.147), against the design's 903 and 139.
   - The identity of 4.2 holds: 0 survivors of any reading lie outside the slots.
   - Each half of the core gives 0.13–0.15.
   - A shorter run (−1760..−640) gives 0.158 (0.082–0.277).
   - The union is dominated by the GWE and station readings, which my code locates well (a parabola vertex on the elongation; the zero of the longitude rate). It does not hang on the approximate rising-azimuth maxima.
3. **So outcome 1's G condition (G_BM,hi ≤ 0.05) cannot hold.**
   - It fails even at the lower 95% bound of my estimate.
   - Even if B&M's garden were cut to their single T0b reading, the upper bound would be 0.061.
   - Since Q_BM is known to hold, outcome 1 also needs G_DOC,hi ≤ 0.05, and G_DOC ≥ G_BM.
4. **The design's own numbers say the same.**
   - §1.2 [l. 292–299]: after conditioning, "about 3.0 bits remain" (log2(41/5)). A p of 0.05 needs 4.3 bits, before B&M's own forks (up to 5.2 bits) are priced.
   - P14 predicts G_BM ∈ [0.05, 0.40] [l. 2219]. Its lower bound is the outcome-1 threshold, so the design predicts that its own outcome 1 is unattainable.
   - By §1.1 B&M also knew the target when they chose the 90-min and ±1-d tolerances, which are the "evidence that remains". The only blind evidence, the held-out clues of section 7, enters no rule [l. 2140–2142].
5. **The rule hides it.**
   - Q_attain fires only if U0(n_A) = 3.69/n_A > 0.05 [l. 2329, 2343]. That is the floor when *no* target is reached. It holds at n_A ≈ 139 (0.027), so Q_attain will not fire.
   - `freeze.py` will agree that "outcome 1 is attainable" [l. 2895–2896].
   - §2.8 calls the expected failure of outcome 1 "a fact about the data, not about the rule" [l. 770–772]. For the G condition it is a fact about the rule and the sky.
   - S1 [l. 2420] puts G_BM = 0.0065 with k_A = 3. T0b's single reading already reaches 4 targets, and the whole garden about 26, so S1 is not realisable. C1–C6 contain no constraint that would catch this.
   - This is r1 N1 again: the verdict would print "inconclusive" or {2} as a "no" from a test that could not have said "yes". That breaks the bench's founding rule and makes the verdict wrong in its qualifiers.

**Fix.**
1. Compute G_BM, G_DOC and their intervals **before the freeze**, as P(A) and
   n_A already are [l. 2892–2895]. They do not read the target's pass or fail
   (exclude 16 Apr −1177 from the targets). Put them in §2 as known
   numbers, as r1 asked for P(A). Freeze the thresholds before they are
   computed, or keep revision 3's thresholds, and record the order.
2. Redefine Q_attain (and C6, and freeze item 11) as **"outcome 1's G
   conditions are attainable"**, that is, G_BM,hi ≤ 0.05 and, when Q_BM holds,
   G_DOC,hi ≤ 0.05 *with the measured G*. Add constraint C7: a synthetic set's
   G_BM must equal the measured value, or the set is marked "contradicts the
   null". Then S1 must be marked unrealisable.
3. If, as estimated here, the G conditions cannot be met, say so in §1.3 and
   in every verdict, beside the 1/P(A) ceiling. Under the uniform
   conditioning rule, B&M's own readings make about one conditioned spring
   target in five "unique", so no reading of the Odyssey's sky words can date
   the return at 5%.
4. If a reachable "yes" is still wanted, it must rest on evidence formed blind
   to the target. The candidates are the held-out predicates of section 7,
   promoted to a rule input with their attainability computed before the
   freeze. A new or relaxed threshold on G must not be used to get one.

### Major

#### R2-2. The slot widths that define T_A set G_BM, and nothing in the record fixes them (major)

**Where:** §4.2, the Venus and Mercury slots [l. 970–982]; §5.3, the
conditioning rule [l. 1184–1221]; §9.3, "Why 0.05 and 0.20" [l. 2372–2378];
§13 row 40.

**Evidence.**
- **How the slots set G.** By the identity of 4.2, G(𝒢_BM*; T_A) = G(𝒢_BM*; T_C) / P(A | T_C). So the
  rule's comparison is equivalent to comparing the slot-free G over T_C with
  0.05 · P(A) and 0.20 · P(A). The slot definition is a multiplier on both
  thresholds. §9.3 already rescales revision 2's thresholds by 1/0.154 for
  that reason.
- **Where the slots came from.** They are r1's PC-S generator slots, with the Mercury width taken from the
  *Almagest* slack [l. 978–982]. They are not MacDonald's or B&M's
  categorical readings. MacDonald puts Venus "near morning elongation"
  [l. 1175], which is narrower than "any visible morning star". B&M's Hermes
  is a named turning point with Mercury visible [l. 216], which is narrower
  than "within 6 d of any of three events, or merely visible".
- **The sensitivity, measured.** The reached targets are the same in every
  case below, so G scales exactly as n_A [r2: check_slot_scaling.py]:

  | slot variant | n_A | G_BM | 95% |
  |---|---|---|---|
  | design (Venus AV 7°; Mercury event ≤ 6 d **or** visible) | 131 | 0.140 | 0.087–0.215 |
  | Venus lead ≥ 60 min; Mercury as design | 101 | 0.182 | 0.112–0.279 |
  | Mercury event ≤ 6 d only | 87 | 0.211 | 0.131–0.324 |
  | Mercury event ≤ 6 d **and** visible | 82 | 0.224 | 0.139–0.344 |
  | Mercury event ≤ 4 d only | 66 | 0.278 | 0.172–0.427 |
  | Venus lead ≥ 60 min; Mercury event ≤ 4 d | 56 | 0.327 | **0.203**–0.504 |

  The last row fires label 2 (G_BM,lo ≥ 0.20). Its n_A is below 74, so Q_attain also holds. The design's choice is the most generous to B&M of these.
- **"Either day count" is ambiguous.** T_A requires the slots "on either day count" [l. 968]. Mixing Day −5 with
  Day −33 gives a larger pool than requiring the pairs (−5, −34) or
  (−4, −33). I used the pairs.

**Fix.**
1. Define each slot from the documented categorical reading it conditions
   on, with its source:
   - Venus near greatest morning elongation (MacDonald), with the width stated;
   - Mercury at a named turning point and visible (B&M).
2. Freeze those definitions and state the pairing of the day counts.
3. Report G_BM and the verdict under at least the variants above. The headline verdict holds only if it is the same
   across them; otherwise report "slot-dependent".

#### R2-3. Label 2 or "inconclusive" is decided by one candidate through the tie rule of pct_N4 (major)

**Where:** §5.4 pct_N4, "ties counting against the Odyssey"
[l. 1433–1438]; §9.2 outcome 2 [l. 2338]; P12 [l. 2216–2217]; P35.

**Evidence.**
- r_Ody is the reach of Schoch's target under 𝒢_BM*. 16 Apr 1178 BC passes
  only the six sequential MWRA readings. It fails the GWE and station readings at ≤ 3.5 d (station 5 Mar, GWE 19 Mar against Day −34 = 13 Mar [vis §2.3]) and the parallel C [bm §9].
- 18 Mar 1189 BC is a survivor 11 years earlier, so r_Ody ≤ 11/136. **P12
  predicts r_Ody = 0**, through another survivor in −1176..−1052.
- **If P12 holds:** every entering epic has r_e ≥ 0 = r_Ody, so pct_N4 = 1 and
  pct_N4,lo = 0.025^(1/n) ≈ 0.98. Label 2, "the match is ordinary", fires
  through ties alone, when in fact B&M's readings make no match at all.
- **My estimate says P12 fails** [r2: check_gbm.py]:
  - no T0b-reading survivor lies in −1176..−1052, so r_Ody = 11/136 = 0.0815;
  - 19.8% of T_A targets reach at least that under 𝒢_BM*, so pct_N4 is likely about 0.2, and the verdict would be "inconclusive";
  - the near misses are 26 Mar 1111 BC (lead 97 min, ΔMWRA 2.27 d) and 2 Apr 1098 BC (lead 108 min, ΔMWRA 2.49 d). Both survive the 2.5-d and 3.5-d readings. That is why the union reach of 1178 BC equals the 1.5-d reach;
  - my rising-azimuth maxima come from the declination series, which r1 rated "good to about 1 d", so the 1111 BC case could fall either side of 1.5 d.
- **So the headline label turns on one Mercury vertex** and on how ties are
  counted. P35 ("{inconclusive} or {2}") covers both outcomes, which is why it
  is near-certain (R2-5).

**Fix.**
1. If r_Ody = 0, output a distinct finding: "no match: no reading of 𝒢_BM*
   makes Schoch's target unique in any window". Do not compute pct_N4 from
   ties in that case.
2. Otherwise count ties at one half (mid-p).
3. State in §2.8 that the label depends on the M status of 26 Mar 1111 BC
   under the bench's exact vertex, and report both branches.

#### R2-4. INSTR contains checks that fail without a bug, so the verdict can be blocked (major)

**Where:** §6.1, INSTR [l. 1599–1601]; I7 [l. 1616]; I10b [l. 1620]; §6.2,
truth pools and science mode [l. 1639–1664]; §11.2 step 12; §9.2 line 1.

**Evidence.**
- **I10b compares two different estimands.**
  - The exact R_obs runs over **T_C**, weighted by A(t, δ) at the jittered days [l. 1538–1546].
  - The science mode draws its truths from **pool (iii), the targets of T_A** [l. 1643, 1663–1664].
  - At j > 0, targets of T_C \ T_A that satisfy A at a jittered day enter the exact denominator and are never simulated. Their reach is 0, so the two R_obs differ systematically.
  - "Agreement within the simulation's 95% interval in every noise cell" will then fail.
- **The pool is not the size the design states.** Pool (iii) holds about 131–139 truths in the core [r2], but I10b and step 12 speak of "2,000 truths per noise cell".
- **I7 demands identical flags at continuous thresholds.** It requires "identical pass flags" for every candidate in 1250–1115 BC and 300 random years, about 6,000 candidates, between two implementations.
  - The thresholds are continuous: ±1.5 d on a 7-point vertex, and 90.0 min.
  - Two codes that each converge rises to "better than 0.1 s" can differ by up to 0.1 s. A rising body's azimuth changes by about 0.0026°/s at 38°N (15°/h × sin φ), so their azimuths can differ by about 3 × 10⁻⁴° [me].
  - At the flatness limit of 0.002°/d², that moves a 7-point vertex by of order 0.01 d [me].
  - With nearest-event distances spread over about 58 d, about 0.02/58 of candidates lie that close to the ±1.5-d edge. Over about 5,400 candidates that gives of order one disagreement [me]. The check can fail without a bug.
- **The cost of a failure.** `verdict.py` refuses to run unless INSTR holds [l. 1601, 2319]. A post-freeze failure forces an amendment after outputs exist. I10 and I10b guard quantities that enter no rule.

**Fix.**
1. Define one estimand for I10b: simulate truths from T_C and accept them by A(t, δ). Fix the truth counts.
2. Restrict INSTR to checks that guard rule inputs, and report I10 and I10b beside it.
3. Give I7 a tie band. Flags may differ only where the margin to a threshold is below a stated ε (e.g. 0.01 d, 0.05 min), and such candidates are listed.

#### R2-5. Predictions that existing numbers already settle, or nearly settle (major)

**Where:** §8.2 [l. 2175–2284].

| prediction | status | evidence |
|---|---|---|
| P12 (reach of 1178 BC is 0) | **expected to fail** | no T0b-reading survivor in −1176..−1052; r_Ody = 0.0815 [r2: check_gbm.py]. Near misses are in R2-3 |
| P19 (R_anc with the eclipse clue has ≥ 2 survivors in the reproduction window) | **settled** | `data/jsex/sites/ithaca.jsonl` at canon ΔT lists **9** conjunctions in −1249..−1114 between 12 Sep and 31 Mar with smag ≥ 0.6 and the Sun ≥ 10° (20 Dec 1247, 14 Mar 1232, 5 Mar 1223, 30 Oct 1207, 9 Oct 1197, 21 Jan 1192, 23 Feb 1138, 30 Sep 1131, 14 Feb 1129 BC) [r2: check_ranc_p19.py] |
| P32 (BF_BM(ρ = 1) < 5) | **near-certain** | 1178 BC passes 6 of 36 readings (R2-3). With p_r taken from T_A, BF_BM(1) ≈ **2.6** and BF_max ≈ 20.7 [r2: check_gbm.py]. Even if each of the six passed nothing else, the bound is 6 · (n_A + 1)/36 ≈ 22 |
| P33 (median *Almagest* BF ≥ 10 × BF_BM(1)) | **near-certain by construction** | it compares an unconditioned BF over day candidates with a BF conditioned on the categorical readings. The two are not the same kind of number |
| P35 ({inconclusive} or {2}, with Q_BM, no 3a, 3b or 4) | **near-certain** in its first clause | T0 = RE is expected (R12), G_BM ≈ 0.14, and the {2}/inconclusive split is R2-3's tie question |
| P13 (G_BM ≥ 2 p_fix,unique), P14 (G_BM ∈ [0.05, 0.40]) | roughly settled | 0.140 against 0.020; 0.140 |
| P4 (λ ≥ 0.44 per century), P6 (≥ 10 survivors; P(≥ 1 in 136 yr) ≥ 0.5) | **near threshold** | λ of the T0b reading 0.55 per century over −1999..+200 (0.71 over −1760..−640); 12 expected survivors; Poisson P(≥ 1) = 1 − e^{−0.75} = 0.53 |
| P22 (P(unique) ≤ 0.6 among T_A passers of the B&M reading) | **no power** | about 4 truths in the core pass that reading; my value is 0.65 on those 4 |

My values for P7 and P8 sit inside their ranges: p_fix|C 0.0054 and a dependence ratio of 0.76 [r2]. They are not settled.

**Fix.** Move P12 (with its near misses), P19, P32, P33 and P35 to §2 as known
or as regression expectations. Restate P4 and P6 with bounds that the rough
numbers do not already sit on, or say that they do. Drop P22 or compute it
over the whole background, and state its n.

### Minor

#### R2-6. The G interval assumes independent counts, and its coverage check cannot see the dependence (minor)

**Where:** §5.3, "G and its interval" [l. 1263–1275]; I9(b) [l. 1618].

**Evidence.**
- The Fay–Feuer interval treats each reached target as an independent Poisson count with a fixed weight.
- Reaches are not independent:
  - neighbouring targets share survivor gaps;
  - Venus' 8-year cycle and Mercury's 13- and 46-year near-repeats cluster passes (5.1 item 5 says so for survivors);
  - half the reached targets have reach exactly 1.0 [r2].
- I9(b) checks coverage on "synthetic reach vectors". If those are drawn independently, it confirms the formula on the model it assumes.
- Both outcome bounds read this interval, G_hi for outcome 1 and G_lo for outcome 2. Under R2-2's tighter slots, G_lo sits at the 0.20 threshold.

**Fix.** Check coverage with a block bootstrap over the background (e.g.
243-year or 136-year blocks), or with time-shifted real survivor sets, and
use the wider of the two intervals.

#### R2-7. "smag" is not NASA's magnitude for central eclipses, so I2(a) cannot pass (minor)

**Where:** §0, Magnitudes [l. 126–135]; I2(a) [l. 1610]; the X3 mapping [l. 1796–1798].

**Evidence.**
- §0 defines smag = (L1′ − m)/(L1′ + L2′) and calls it "NASA's 'magnitude'".
- `data/jsex/program.js` computes that quantity (line 361) but then sets the magnitude to the Moon/Sun ratio for total and annular eclipses (lines 534–537).
- The site catalogue accordingly gives 1.0486 for 30 Sep 1131 BC at Ithaki, which the design's own table gives as the diameter ratio, against an smag of 1.0169.
- I2(a) requires smag within 0.0005 of `program.js` and so fails at every central eclipse at a site.
- At annular eclipses the two definitions also differ near the X3 threshold of 0.95.

**Fix.**
1. In I2(a), compare smag with `program.js`'s mid[37] before the central override, or compare the ratio with mid[38].
2. Correct §0.
3. State which quantity X3 and h_09 use at annular eclipses.

#### R2-8. N4: the entering subset is not sized, and epic gardens are undefined for some clue types (minor)

**Where:** §5.4 [l. 1411–1441]; C3 [l. 2399].

**Evidence.**
- **The sizing rule applies to the wrong set.** The widening rule ("fewer than 200 … the factor widens to 4") applies to the stratum. n_stratum in the rule counts *entering* epics, those whose categorical slots hold at Schoch's target.
  - For a variant-A epic that needs a season clue and two planet roles to hold on fixed days, entering is of order P(C) · P(A) ≈ 0.1 or less [me, by analogy with P(A) = 0.15].
  - So C3's "n_stratum ≥ 200" is not guaranteed, and the synthetic sets assume it.
- **Some gardens are undefined.** The BM-tier epic garden is defined only for turning-point planet clues ("3 events × 3 tolerances × 2 visibility"). An epic whose planet clues are rise-lead or set-lag clues gets fewer forks, and a smaller r_e. That biases pct_N4 toward the Odyssey.

**Fix.** Draw epics until at least 200 enter the stratum. Give every clue type
an epic-garden fork set of 36 readings, matching 𝒢_BM*'s multiplicity
(e.g. lead thresholds × day count × visibility).

#### R2-9. Leave-one-set-out can be undefined, and the grid value it relies on was set after the slack was measured (minor)

**Where:** §6.4 regime SL [l. 1965]; §13 row 41 [l. 3040].

**Evidence.**
- **The undefined case.** The rule takes "the smallest value of the row's own list at or above" the out-of-set maximum. If no listed value covers it, the rule is undefined.
- **The 21-d value.** For Venus the out-of-set maximum is 20.6 d (X.1.4). Only the grid's top value, 21, covers it.
  - That grid is in `results/controls-almagest/build_prereg.py`, last modified at 00:38. The slack measurement `slack.out.txt` was written at 00:35:45 the same night.
  - The value 21 may therefore post-date the measurement. The file times cannot settle it.
  - §13 row 41 says the list's history affects only rounding. It also decides whether the rule is defined for Venus, and so whether ALM-D, F and L keep their truths.

**Fix.** Define the SL tolerance as the out-of-set maximum rounded up to the
next whole day, independent of the drafter's grid. Record when the grid's 21
was written, if the drafter's notes show it.

#### R2-10. The sibling-convention audit transplants stricter conventions across different wordings (minor)

**Where:** §6.3.4 item 2 [l. 1852–1866].

**Evidence.**
- **The transplant goes both ways.** "Each sibling's primary parameters are transplanted … wherever the operational keys match", for every row whose primary passes.
- **It then tests rows against conventions they do not state.**
  - T2-SEASON's "start of the following summer" span, [330°, 60°], moves into T1-SEASON ("the same summer", Sun about 128° at the accepted date) and T3-SEASON. Both then fail.
  - That tests the rows against a convention their words do not state, not exposure.
- **The result is all-at-once.** seen_PCR,sibling and Q_exposure can flip without any exposure.

**Fix.** Transplant only between rows whose licence words state the same
feature, or only conventions that are equal or weaker. List the excluded
transplants.

#### R2-11. R_anc's primary season was chosen with the answer known (minor)

**Where:** §5.3 R_anc [l. 1328–1346]; §2.8 [l. 741–762]; R11.

**Evidence.**
- r1 computed 176.69° for 30 Sep 1131 BC, three days before Geminus' autumn. Revision 3 then adopted the union of Hesiod's and Geminus' seasons, which admits it.
- The union is sourced and defended by the controls' "weakest reading" policy. But the choice among the four sourced bounds was made with the result in view.
- R_anc is outside the rule and R11 is not counted, so the harm is limited to the standing finding.

**Fix.** Report the four bounds with equal prominence, and record in §5.3 that
the primary was chosen after the 1131 BC value was known.

#### R2-12. G_j is undefined for a reading whose eclipse is not on Day 0 (minor)

**Where:** §6.5, hit_j and G_j [l. 2059–2067].

**Evidence.**
- QS-SACK-06:a puts the eclipse at Cape Caphereus on Day +2..+12. Its Day 0 cannot then be a conjunction.
- G_j is a mean reach "over all daylight conjunctions". For this reading the survivors are Day-0 days, and the reading names no rule mapping them to conjunction targets.
- (F2 (c) and (d) have a mapping rule; the negatives do not.)

**Fix.** Map such a survivor to its eclipse conjunction, or compute G_j over
the reading's own Day-0 candidates, and state which.

---

## 4. Checks that passed

| claim | how checked | result |
|---|---|---|
| The pool identity of 4.2 (no 𝒢_BM* survivor outside T_A) | all 36 readings over −1999..+200 [r2: check_gbm.py] | 0 violations |
| P(A) and pool sizes | same run, core −1748..−51 | P(A \| T_C) = 0.147; n_TC 892, n_A 131 (design 0.154, 903, 139) |
| C_rel reproduces B&M's bounds at −1177 | calibration midpoints [r2] | 17 Feb and 4 Apr (h_A 2.04°, h_P 0.92°); 11 Feb–31 Mar at −1700, 22 Feb–6 Apr at −700 |
| Garden sizes 36 / 35,964 / 767,232 | products of the 5.3 option counts [me] | confirmed |
| The twelve synthetic sets give their stated labels and qualifiers | traced by hand through 9.2 [me] | all twelve confirmed: S1 {1}+Q_BM; S2 {2}; S3a {3a}; S3b {3b}; S4 {4}; S0, S5, S8 inconclusive; S6 {2, 3b, 4} with all four qualifiers; S7 BLOCKED; S9 Q_attain; S10 {1} with none |
| The S-set intervals | `results/design-revision-r2/synth_sets.out.txt` against the table | match |
| C6 numbers | U0(74) = 0.0499, CP0(73) = 0.0493 [me] | confirmed |
| Licence strings | every string, split at ellipses, found verbatim in its cited row [r2: check_prereg_leaks.py] | `controls_real.json` 125/125; `controls_almagest.json` 54/54 |
| Date leaks into operational fields | regex scan for year-like numbers and month names outside licence words [r2] | 5 hits, all Roman calendar names stated by Livy (H-LIVY, R-PYDNA); none in the *Almagest* file |
| Clue-file hashes in §12.4 | `sha256sum` | `135fba67…83f8`, `758ee789…4c83` and `f4ae3b26…bb00` match |
| P7, P8 ranges are not already settled | P_spring (seq) over −1999..+200 [r2] | p_fix\|C 0.0054 in [0.002, 0.02]; V–M dependence ratio 0.76 in [0.5, 2] |
| Outcome 4 is attainable by C6 | G_BM,u = (n_A/n_T) G_BM ≈ 0.0017 > U0(10,690) = 0.00035 [r2; me] | yes |
| R_anc arithmetic (30 Sep 1131 BC 16–20 d after Arcturus' rising; about 3 d before the autumnal equinox) | `ranc_season.out.txt`; r1's 3 Oct 17:17 UT | confirmed |
| 1178 BC fails GWE and station readings | vis §2.3: station 5 Mar, GWE 19 Mar against Day −34 = 13 Mar | confirmed in my run (passes only the six sequential MWRA readings) |

## 5. What I could not check, and the limits of my estimates

- **`check_gbm.py` is rough and independent of the bench.**
  - Rises come from a 3-minute grid.
  - Mercury's rising-azimuth maxima come from the declination series at 03:30 UT, with a 3-point vertex rather than the design's 7-point least-squares fit.
  - Stations come from the interpolated zero of the daily longitude change.
  - Conjunctions are on DE441, not DE431, with SMH2020 ΔT and one site.
  - The single-reading λ (0.55–0.71 per century) agrees with the dossier's 0.8 [vis §5] and B&M's own 0.88.
  - The G_BM estimate has its own sampling uncertainty (26 reached targets). But R2-1's conclusion needs only that G_BM exceed about 0.03, which the lower 95% bound (0.087) and the design's own §1.2 and P14 all clear.
- **P12's deciding case** (26 Mar 1111 BC, ΔMWRA ≈ 2.3 d) needs the bench's exact vertex. My method is good to about 1 d at a flat maximum.
- **Not computed:**
  - the N4 entering fraction (R2-8);
  - the narrowing of the nine *Almagest* sets that keep their truth (P25);
  - the PC-R gate (P24).
- **SMH2016 Table S4.** Whether the *Almagest* lunar timings entered the SMH fits is still unread. It is left to A11, as the design says.

## 6. Files produced

All are in `C:\Projects\odybench\results\critique-design-r2\`:

| file | what it does |
|---|---|
| `check_gbm.py` with `check_gbm.out.txt`, `check_gbm.rows.json` (−1760..−640) and `check_gbm_full.out.txt`, `check_gbm_full.rows.json` (−1999..+200, env `GBM_FULL=1`) | C_rel calibration; the spring candidates; the 36 readings of 𝒢_BM*; the slots of T_A; reach and G with the Fay–Feuer interval; r_Ody; the per-reading rates; p_fix\|C and the V–M ratio; BF_BM(1); the near misses after 1178 BC |
| `check_slot_scaling.py`, `.out.txt` | G_BM and its interval under six slot definitions of T_A |
| `check_ranc_p19.py`, `.out.txt` | R_anc-with-eclipse survivors in the reproduction window from NASA's Ithaca site catalogue |
| `check_prereg_leaks.py`, `.out.txt` | licence strings found verbatim, and a scan for date leaks, in the two control clue files (read-only) |
