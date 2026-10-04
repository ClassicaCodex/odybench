### 2.9 Known from the recheck of revision 3, and from this revision's design-stage estimate

The recheck rebuilt the rule's pools and garden independently, with rough
methods [r2: check_gbm.py, check_slot_scaling.py, check_ranc_p19.py;
approximations in r2 §5]:

- rises on a 3-minute grid;
- Mercury's rise-azimuth maxima from the declination series, with a 3-point
  vertex;
- stations from the interpolated zero of the daily longitude change;
- conjunctions on DE441 with SMH2020 ΔT, at one site, Ithaki.

The bench recomputes every number below with its own code, and no
confirmation is counted.

**Pools and the C_rel calibration.**

- **C_rel calibration.** h_A = 2.04° and h_P = 0.92° reproduce A(−1177) =
  17 Feb and P(−1177) = 4 Apr. They give 11 Feb–31 Mar at −1700 and 22 Feb–6
  Apr at −700. h_P is a fit to B&M's printed bound, not a visibility: a star
  of magnitude 2.9 is not seen at 0.9° [r2 §1 #9].
- **Candidates.** 27,212 conjunctions in −1999..+200, of which 2,286 are
  spring candidates (C_rel on either count).
- **The core −1748..−51.**
  - n_TC = 892;
  - n_A = 131 under revision 3's slots, with the day counts paired;
  - so P(A | T_C) = 0.147.

  The design's estimates were 903, 139 and 0.154.
- **The identity of 4.2 holds.** No survivor of any of the 36 readings lies
  outside revision 3's slots.

**G over T_A** (W = 136 years, the Fay–Feuer interval of 5.3):

| readings | G | 95% interval | targets reached |
|---|---|---|---|
| T0b's reading alone (sequential, MWRA_vtx ±1.5 d, visibility off) | 0.020 | 0.004–0.061 | 4 / 131 |
| sequential MWRA, all tolerances (6) | 0.032 | 0.012–0.076 | 10 / 131 |
| sequential, all events (18) | 0.121 | 0.073–0.192 | 25 / 131 |
| **𝒢_BM*** (36) | **0.140** | **0.087–0.215** | 26 / 131 |

- **Stationarity.** The two halves of the core give 0.130 and 0.152; a
  shorter run, −1760..−640, gives 0.158 (0.082–0.277).
- **Shape.** Half of the reached targets have reach exactly 1.0.
- **What dominates.** The union is dominated by the GWE and station readings,
  which the recheck's method locates well.
- **The other pools.** G over T_C is 0.0206, and G_BM,u = (n_A/n_T) G_BM ≈
  **0.00172** with n_T ≈ 10,690.
- **What this means.** G_BM does not depend on any measurement of the
  Odyssey. Even T0b's single reading has an upper bound of 0.061, so no
  threshold of 0.05 on G over T_A can be met [r2 R2-1].

**The slot definitions set G_BM** [r2 R2-2; r2: check_slot_scaling.py]. The
same 26 targets are reached under every definition, so G scales as 1/n_A.
The variants are frozen as the family of 4.2:

| variant (4.2) | n_A | G_BM | 95% |
|---|---|---|---|
| v0 documented: Venus visible (AV 7°); Mercury event ≤ 6 d **and** visible | 82 | 0.224 | 0.139–0.344 |
| v1 revision 3: Venus AV 7°; Mercury event ≤ 6 d **or** visible | 131 | 0.140 | 0.087–0.215 |
| v2: Venus AV 7°; Mercury event ≤ 6 d | 87 | 0.211 | 0.131–0.324 |
| v3: Venus AV 7°; Mercury event ≤ 4 d | 66 | 0.278 | 0.172–0.427 |
| v4: Venus lead ≥ 60 min; Mercury as v1 | 101 | 0.182 | 0.112–0.279 |
| v5: Venus lead ≥ 60 min; Mercury event ≤ 4 d | 56 | 0.327 | **0.203**–0.504 |

The smallest lower bound is 0.087, under v1. Only v5 alone would fire
label 2's G leg (lower bound ≥ 0.20). Every variant gives the same G_BM,u,
0.00171–0.00172 [me: `results/design-revision-r3/synth_sets.py`, `.out.txt`].

**The target under 𝒢_BM*** [r2 R2-3].

- **Which readings it passes.** 16 Apr 1178 BC passes only the six
  sequential MWRA readings. It fails the GWE and station readings at
  ≤ 3.5 d: the station is on 5 Mar and GWE on 19 Mar, against Day −34 =
  13 Mar [vis §2.3]. It also fails every parallel reading.
- **Its reach.** The only survivors of the T0b reading in −1260..−1040 are
  18 Mar 1189 BC and 16 Apr 1178 BC. So r_Ody = 11/136 = **0.0815**, and
  19.8% of T_A targets reach at least that much.
- **The near misses** both survive the 2.5-d and 3.5-d readings. That is why
  the union reach equals the 1.5-d reach:
  - 26 Mar 1111 BC, lead 97 min, ΔMWRA 2.27 d;
  - 2 Apr 1098 BC, lead 108 min, ΔMWRA 2.49 d.
- **How firm it is.** The 1111 BC case lies within the recheck's accuracy
  of about 1 d at a flat maximum. At the bench's exact vertex r_Ody could be
  0, which is label 2's "no match" form. Both branches are reported (5.4).

**Rates and the Bayes factor** [r2: check_gbm.py]:

- **Survivors per century.** T0b's reading gives λ = 0.55 per century over
  −1999..+200 (0.71 over −1760..−640). That means about 12 survivors, and a
  Poisson P(≥ 1 in 136 years) of 0.53. The 36 readings give 0.27–1.77 per
  century each.
- **P_spring** (sequential, all candidates, n = 2,204):
  - P(V) = 0.198;
  - P(M, MWRA_vtx ±1.5 d) = 0.036;
  - p_fix|C = P(V ∧ M) = 0.0054;
  - the V–M dependence ratio is 0.76.
- **The Bayes factor.** BF_BM(ρ = 1) ≈ 2.6, with BF_max ≈ 20.7.
- **P(unique)** over the T0b-reading passers in T_A is 0.647, on n = 4.
- **The visibility fork never separates.** Among spring Day −34s within
  3.5 d of a morning event, every one is visible at AV 10°. So 18 of the 36
  readings duplicate the other 18 [r2 §1 #7].

**R_anc with the eclipse clue** [r2: check_ranc_p19.py]. In NASA's Ithaca
site catalogue at canon ΔT there are 9 conjunctions in −1249..−1114 between
12 Sep and 31 Mar with smag ≥ 0.6 and the Sun ≥ 10°:

- 20 Dec 1247 BC;
- 14 Mar 1232 BC;
- 5 Mar 1223 BC;
- 30 Oct 1207 BC;
- 9 Oct 1197 BC;
- 21 Jan 1192 BC;
- 23 Feb 1138 BC;
- 30 Sep 1131 BC;
- 14 Feb 1129 BC.

So R_anc dates nothing in B&M's window, even with its eclipse.

**Prereg files** [r2 §4]:

- every licence string occurs verbatim in its cited row: 125/125 in
  `controls_real.json` and 54/54 in `controls_almagest.json`;
- the only date-like strings outside licence words are the Roman calendar
  names that Livy gives;
- the three clue-file hashes match 12.4.

**The held-out null, estimated for this revision** [me:
`results/design-revision-r3/heldout_attain.py`, `.out.txt`, `.json`].

- **How the target was kept out.** The script removes 16 Apr 1178 BC from
  r2's candidate rows before it computes anything, and asserts that no
  predicate is evaluated on it.
- **The predicates.** H3 and H4 are revision 1's: Mercury within ±3 d of a
  conjunction with the Sun around Day 0/+1 and not visible; Venus–Mars
  ≤ 5° within ±3 d of Day −7 (section 7).
- **Approximations.** Visibility is approximated by an elongation below 10°,
  sampling is daily, and the rows are r2's rough candidates.
- **What has not been done.** No note, review or design revision has
  evaluated H3 or H4 at the target. A search of `docs/` and `results/` finds
  no such computation.

| null pool (whole background, target excluded) | n | q3 (H3) | q4 (H4) | pass both | p_H,min = (1 + both)/(1 + n) | p if the target passed H4 only | p if H3 only |
|---|---|---|---|---|---|---|---|
| **P_BM**: candidates passing some reading of 𝒢_BM* (the rule's pool, 7) | 76 | 0.197 | 0.026 | 1 | **0.026** | 0.039 | 0.221 |
| T_A under v1, daylight | 169 | 0.237 | 0.041 | 1 | 0.012 | 0.047 | 0.241 |
| T_A under v0, daylight | 108 | 0.222 | 0.037 | 0 | 0.009 | 0.046 | 0.229 |

**The order of these choices is recorded.**

- The three pools were defined before the script ran.
- The rule's pool, P_BM, was chosen because it compares the target only with
  candidates that pass the same readings [rev #11 fix 1]. It is the least
  favourable of the three to a "yes".
- H3 and H4 have been frozen since revision 1 (2026-10-03). The score and
  the pool are new in this revision.

