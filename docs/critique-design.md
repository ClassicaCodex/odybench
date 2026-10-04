# Adversarial review of DESIGN.md

Written 2026-10-03, before any bench code exists. Scope: `DESIGN.md` (read in
full) and the dossier in `docs/`. The job was to find what is wrong or missing,
not to praise what works, so section 1 records the checks that passed in a single
table and section 2 lists the problems.

**What I read.**
- In full: `DESIGN.md`; `research-bm2008.md`; `research-chronology.md`;
  `research-critiques.md`; `research-window.md`; `research-visibility.md`;
  `research-controls.md`; the B&M full text (`data/bm2008-a/bm2008-pmc-fulltext.txt`).
- In part:
  - `research-ephemeris.md`: §1–9, and the PASS lines of §10.
  - `research-textclues.md`: §0–3 and §5–10. I did not read the §4 inventory row by row.
  - `research-bm2008-a.md` §11–12 and `research-bm2008-b.md` §13–14. Both are otherwise merged into `research-bm2008.md`.
- Not read: `docs/research_visibility_calc.py` and `docs/textclues-scripts/`.

**Conventions.** Years are historical BC with the astronomical year after them:
16 Apr 1178 BC (−1177). Calendar dates are proleptic Julian. Time scales:
- TT is Terrestrial Time (the canons' TD).
- UT is UT1, and ΔT = TT − UT.
- UT+2 is zone time on 30°E, B&M's clock.
- LMT is local mean time at 20.717°E (UT + 1 h 22.9 min).
- LAT is local apparent solar time.

**Tags.** The dossier tags are the same as DESIGN's: [bm §n], [chron §n], [txt §n], [eph §n], [vis §n],
[ctl §n], [win §n] and [crit §n]. The other tags are:
- [DESIGN §n]: the design itself.
- [B&M §X]: the paper, which I read in the PMC text.
- [Od. x.y], [Il. x.y] and the like: lines I read in `data/text/`. The printouts are in
  `results/critique-design/check_lines*.out.txt`.
- [me: script]: computed by me with the named script in
  `results/critique-design/`, whose output sits beside it.
- [me]: my own arithmetic or inference.

Quotations from copyrighted modern works are kept under 15 words. Everything
else is paraphrased.

---

## 0. Summary

There are 25 issues: **3 blockers, 15 major and 7 minor**.

The astronomy the design relies on checks out. I re-derived the following independently:
- the ΔT values;
- the canon entry for the eclipse;
- the eclipse circumstances at Ithaki;
- the 1131 BC and 1312 BC eclipses;
- the Venus leads;
- every Greek and Latin line number I tried.

The problems are in the logic that turns measurements into a verdict, in the controls, and in a few places where the
instrument is fragile:

1. **The decision rule cannot run as written** (issue 1).
   - It never names which garden's G it uses.
   - Its condition on the negative controls makes outcome 1 unreachable.
   - It uses G in opposite senses for outcomes 1 and 4.
2. **The positive controls leak their answers** (issue 2). Times of day, seasons, totality and year intervals that are not in
   Thucydides, Xenophon, Diodorus or Livy were copied into the clue sets from the
   computed truth.
3. **The "method can see" gate is decided by eclipse records** (issue 3). No control of
   the kind B&M actually used (stars, Venus, a Mercury turning point, the new moon)
   is allowed to trigger outcome 3. The one that exists, the *Almagest* planets, is expected to fail and is
   excluded from the gate.
4. **Several pre-registered predictions are already settled by numbers in the dossier** (issue 17). By
   my arithmetic, prediction 19 fails as written.
5. **The Mercury criterion as specified is numerically ill-conditioned** (issue 12). For
   1189 BC (−1188), the integer date of the azimuth maximum is decided by 0.0004°.

---

## 1. Verification of the claims the design leans on most

| # | Claim in DESIGN | Checked against | Result |
|---|---|---|---|
| V1 | B&M's criteria and offsets [DESIGN §1.1]: **C** Ti−29 ≥ 17 Feb and the 17 sailing days within 17 Feb–4 Apr; **V** Venus rises ≥ 90 min before the Sun on Ti−5; **M** Ti−34 near Mercury's westernmost rising azimuth; **E** 1 Apr ≤ Ti−11 ≤ 5 Apr, listed and not applied; sequential and parallel offsets | B&M §References and Constraints, §Intersecting, Table 1 (PMC text) | **Confirmed**, with three qualifications. (a) The text requires Mercury to be "visible" on Ti−34; T0b records this but does not apply it (issue 23). (b) B&M's probability paragraph bounds the sinking at "on or before … 4 April", and under that bound 1178 BC fails E (issue 23). (c) B&M call 14.457 "Night −2", which contradicts their Table 1; DESIGN H2 correctly uses −5/−4. |
| V2 | "Matched exactly about one day in 2,000 years: one New Moon in 6 years × 3 × 116 days" [DESIGN §1.1 item 2] | B&M §Intersecting | **The arithmetic is right (2,088 years) but the attribution is wrong.** The "one Ti every 6 years" is the rate for C and E together, the equinox clue B&M did not apply. B&M frame it as satisfying "all five references this strictly". DESIGN omits this, and prediction 6 builds on the omission (issue 5). |
| V3 | ΔT at −1177 Apr 16 [DESIGN §3.7 item 1]: E-M 28,716 s; canon 28,590 s; SMH2016 parabola 28,963 s; Addendum 2020 parabola 28,282 s; Huber σ 1,008 s | Formulas in eph §2.1, recomputed by hand at decimal year −1176.7 | **Confirmed.** −20 + 32u² = 28,716.8; minus the ṅ correction of 126.8 gives 28,590.0; −320 + 32.5τ² = 28,963; −10 + 31.4τ² = 28,282; Huber gives 1,007.8 s [me]. **The epoch label "−1177.29" is wrong.** The values belong to −1176.68 (issue 22). |
| V4 | Canon identity [DESIGN §2.3]: catalogue 01966, Saros 39 member 31, γ 0.5187, magnitude 1.0599, greatest eclipse at 32.7°N 12.7°E | `data/ref/nasa_besselian_-11770416.txt`, `nasa_5mcse_catalog_lines.txt`, `data/refs/nasa/SEsaros039.html` | **Confirmed.** Greatest eclipse 17:57:28 TD = 10:00:58 UT; ΔT 28,590.0 s; lunation −39291; type T; path 227.8 km; central duration 4 m 33 s. Saros 39 runs from relative number −37 (member 1), so relative −07 is member 31. |
| V5 | Ithaki at canon ΔT: magnitude 0.984, maximum 10:22 UT = 11:45 LMT, Sun 57°; total for ΔT 28,801–29,585 s on the NASA elements [DESIGN §2.3, crit §2.3] | My own local-circumstance solver from the NASA polynomial elements. It follows the textbook formulation and shares no code with the NASA JavaScript port or with `ephem` [me: check_bessel.py] | **Confirmed.** Magnitude 0.9839 at 10:22 UT (11:45 LMT), Sun 57.2°; totality window 28,805–29,580 s on a 5-s grid. With B&M's 27,602.7 s the magnitude is 0.909 at 12:08 LMT (crit §2.3 gives 0.909 at 12:07). |
| V6 | 30 Sep 1131 BC (−1130) total at Ithaki at canon ΔT; 24 Jun 1312 BC (−1311) magnitude 0.984, total for +540 to +1,440 s [DESIGN §3.4 item 5, §3.7 item 5; win §7.1] | Same solver, JSEX elements | **Confirmed.** 1131 BC: total, 09:49 UT = 11:12 LMT, Sun 51.6°, window 27,050–28,035 s, i.e. −641 to +344 s from canon. 1312 BC: 0.984 at 12:02 LMT, total for +539 to +1,449 s. The "1.049" quoted for 1131 BC is the Moon-to-Sun diameter ratio (I get 1.0486); the fraction-of-diameter formula gives 1.017 (issue 21). |
| V7 | Day 0 is JD 1291263.5 at 0 h; 16 Apr Julian = 5 Apr proleptic Gregorian; Ti window 18 Mar–16 Apr; Ti−34, −29, −12, −11 and −5 fall on 13 Mar, 18 Mar, 4 Apr, 5 Apr and 11 Apr [DESIGN §0–1] | Meeus eq. 7.1 by hand; calendar arithmetic (−1177 is a common year) | **Confirmed.** |
| V8 | Greek and Latin citations | Local TSVs; about 60 lines read [me: check_lines*.py]. Odyssey: 20.351–357; 5.270–279; 13.93–95; 14.161–162 = 19.306–307; 14.457; 20.155–156; 20.276–278; 21.258–259; 5.282; 5.43–55; 5.97–103; 5.148; 11.373; 15.392; 24.1–14; 7.259–261; 10.467–470; 6.170; 5.34; 1.22–24; 24.63–65; 20.390–394; 21.428–429. Iliad: 16.567; 17.366–368; 18.239–241; 18.485–489; 23.226–228; 24.339–345. Others: *Aen.* 2.255 and 2.801; *Arg.* 1.1202, 1.1273, 4.1695–1697; *h.Herm.* 17–19, 97–100, 141; *WD* 383–387, 564–567, 609–621, 770–771, 798 | **Every line number I checked is right.** Three readings are wrong: H8 treats a stock epithet as an observation; NC3 takes a season clue from a simile; NC4 misreads line 141 (issues 15 and 24). |
| V9 | The positive-control passages and the clue sets built from them [DESIGN §4.3] | Thuc. 2.28, 4.52, 7.50; Xen. *Hell.* 1.6.1, 2.3.4, 4.3.10; Diod. 20.5.5; Livy 44.37, 22.1.9, 30.38.8, 37.4.4, 38.36.4; Plut. *Alex.* 31.4; Arr. 3.7.6, 3.15.7; Curt. 4.10.2; Pliny 2.180; Ptol. 4.6.3–5 [me: check_lines3.py, check_lines4.py] | The events and dates match ctl. **But R3, R4, R6, R7 and R8 contain features the texts do not state** (issue 2). R1 (*Almagest* IV.6) is confirmed: total; three digits from the south at midnight; more than half from the north. Its mid-eclipse times are Ptolemy's own reductions. |
| V10 | Venus lead 103.6 min on 11 Apr 1178 BC and 100.9 min on 13 Mar 1189 BC (−1188); the UT+2 clock [DESIGN §2.4, §2.5] | My own 0.01-s rise bisection on `ephem` positions, ΔT 27,602.7 s, 38.4°N 20.7°E, h0 −0.8333°/−0.5667° [me: check_venus.py] | **Confirmed**: 103.6 and 100.9 min. My sunrise is 06:24:13 UT+2 against S2's 06:22:41. |
| V11 | Strict Eratosthenes excludes 1178 BC [DESIGN §3.6] | Od. 7.259–261 and 10.467–470 read; win §3 | **Confirmed.** The sack falls in late spring 1183 BC (−1182). Adding at least 8 years gives a return in 1175 BC (−1174) or later. |
| V12 | X1 is "Schoch's" class [DESIGN §3.1] | Schoch 1926, p. 20, as read in bm §11 | **Not as labelled.** Schoch required greatest phase between 10 a.m. and noon; X1 uses 10–14 h LAT (issue 10). |
| V13 | MacDonald 1967 supports a March season [DESIGN §8 item 19] | B&M §References; Gainsford 2012 p. 8 (`data/refs/gainsford2012.txt`, around line 71) | **Contested.** Gainsford reports that MacDonald argued for the second half of May, from the reaping match at Od. 18.366–370. The primary is unread (issue 6). |
| V14 | Predictions 18 and 19 still need new runs [DESIGN §6] | My computation from the dossier's ΔT models and my totality windows [me: check_p19.py, check_mag09.py] | **Already determined** (issue 17). |
| V15 | The 1178 and 1189 Mercury azimuth maxima are robust [DESIGN §2.5] | My 0.01-s rise bisection [me: check_mwra.py] | Both pass at ±1 d. **The integer maximum for 1189 BC is decided by 0.0004°** (issue 12). |

Some points also hold up and need no change:
- **The dominance argument [DESIGN §3.4].** The 20-day-window reading and the "N dropped" reading cannot add reach for a
  conjunction target, so leaving them out is correct.
- **The garden counts.** 8 × 4 × 6 × 6 × 31 × 4 × 3 = 428,544, which is 18.7 bits; G_1 has 56 readings and G_BM 72.
- **The bit budget.** 1,683 × 0.083 × 0.158 × 0.044 = 0.97.

---

## 2. Issues

Each issue gives its severity, where it sits in DESIGN, the evidence and a
concrete fix.

### Blockers

#### 1. The decision rule is undefined in one place and self-contradictory in two (blocker)

**Where:** DESIGN §6, the decision-rule table; §4.4, "Pass and fail for the method"; §1.3.

**Evidence.**
- **G is never tied to a garden.** The rule uses "G" without saying which one. §3.4 defines G for
  B&M's own reading, G_1, G_BM, the full garden and the eclipse-compatible garden, and
  reports it "for each garden". Prediction 11 uses the eclipse-compatible garden; the
  rule does not say. `verdict.py` cannot be written from this text.
- **Outcome 1 is unreachable.** It requires "every NC1–NC3 G ≥ 10 × the Odyssey's".
  - G is a reach: the chance that some reading makes a target fixed in advance the unique survivor of a window [DESIGN §3.4].
  - A text whose clues are few or weak never has a unique survivor. Every interval I_r(t) is then empty and G → 0 [me, from the §3.4 definition].
  - The design itself expects NC2 and NC3 to give "many survivors; no uniqueness" [DESIGN §4.4]. Their clues are weak: Venus is a visible morning star on 42% of days [vis §1.3].
  - So G_NC2 and G_NC3 ≈ 0, the outcome-1 condition fails, and it fails whatever the Odyssey shows.
- **G is used in opposite senses.**
  - In §3.4, G is the look-elsewhere-corrected p-value, so a high G means a coincidence is *ordinary*.
  - Outcome 4 ("the method dates fiction") is triggered by an NC text with G ≥ 0.05. That only says eclipse matches on fiction are cheap. It does not say fiction is dated "as cleanly as the Odyssey" [DESIGN §1.3].
  - §4.4(iii) calls the method specific when NC G is *low* (no higher than random epics). The outcome-1 rule needs NC G to be *high*.
  - When the Odyssey's G is close to the random epics' G, which is the expected case, the two rules contradict each other.

**Fix.**
1. Name the garden in every rule. I recommend G_BM as the primary garden and the eclipse-compatible full garden as a sensitivity (issue 7).
2. Replace the NC condition with a calibrated percentile. Compute the Odyssey's G as a percentile of the G distribution of N4 random epics in the same specificity stratum. Outcome 1 then needs the Odyssey below the 5th percentile *and* LR_garden ≥ 30.
3. Define "dates fiction" as follows: a clean negative text (issue 15) has an eclipse-compatible reading whose unique survivor is an X-class eclipse, with G no greater than the Odyssey's.
4. Before freezing, test `verdict.py` on four synthetic input sets built to produce each outcome. That shows the rule can reach all four.

#### 2. The positive-control clue sets contain information taken from the known answers (blocker)

**Where:** DESIGN §4.3, the R1–R8 table, and prediction 23. The features below are not in the texts [me: check_lines3.py].

| Set | Feature given to the method | What the text says | Where the feature came from |
|---|---|---|---|
| R3, Thuc. 4.52.1 | "morning" | the eclipse happened "περὶ νουμηνίαν" at the start of summer; **no time of day** | the computed 08:43 LMT [ctl §3 P2] |
| R3, Thuc. 7.50.4 | "total" | "πασσέληνος" (full moon) only | NASA's umbral magnitude 1.08 [ctl §3 P3] |
| R4, Xen. *Hell.* 2.3.4 | "solar in the morning … Pherae" | "κατὰ δὲ τοῦτον τὸν καιρὸν περὶ ἡλίου ἔκλειψιν": no time of day, no observing site. Pherae is Lycophron's city | the computed 08:34 LMT [ctl §3 P4b] |
| R4 | years n, n+2, n+12; "summer" for 4.3.10 | no year count joins these items; the year headings are suspected glosses [ctl §4.4]; 4.3.10.1 has no season | the modern dates 406, 404 and 394 BC (−405, −403, −393) |
| R6, Livy 44.37 | "summer" | the Roman date "pridie nonas Septembres" (44.37.8). The clue set itself says the calendar offset is unknown | the Julian truth, 21 Jun 168 BC (−167) |
| R7, Diod. 20.5.5 | "morning, late summer" | the next day the eclipse made it seem full night, with stars everywhere; no hour, no season | the computed 07:39 LMT and 15 Aug 310 BC (−309) [ctl §3 P9] |
| R8, Livy 22.1.9 | site "Rome" | "solis orbem minui visum" stands in a list that starts with Sicily and Sardinia; no site | assumed |

R8's "truth" is also partly the product of eclipse matching:
- 217 BC (−216) and 203 BC (−202) are Gautschy's identifications, at magnitude 0.65 at Rome and 0.48 at Cumae [ctl §4.11–4.12, secondary].
- 17 Jul 188 BC (−187) peaks at 06:16 LMT, while Livy says "inter horam tertiam ferme et quartam" [ctl §3 P12 note].
- Recovering R8 therefore tests agreement with Gautschy, not dating ability. Prediction 23 nonetheless expects R8 to be unique.

**Why it matters.** Time of day, season and magnitude are the most discriminating parts of an eclipse clue. Copying them in from the computed truth raises recall and uniqueness. It also makes the PC-R ≥ 6/8 gate that guards outcome 3 easier to pass.

**Fix.**
1. Rebuild `controls_real.json` from the texts alone, one row per clue. Each row carries the Greek or Latin word that licenses the clue and its line key.
2. Clues the text lacks are either dropped or entered as forks.
3. The sets are drafted by an agent with no access to ctl §3 or the NASA tables, then frozen.
4. Demote R8 to a "hard case".
5. Treat Roman dates as carrying an unknown calendar offset, a free parameter.

#### 3. The "method can see" gate is decided by controls that do not use B&M's clue types (blocker)

**Where:** DESIGN §4.3, §4.5, the outcome-3 row of §6, and the preamble rule that "a 'no' about the Odyssey means something".

**Evidence.**
- **B&M's search uses no eclipse.** Its clues are N (conjunction), C (a star season), V (a Venus rise lead) and M (a Mercury rising-azimuth extremum). The eclipse is not a criterion [B&M abstract; DESIGN §1.1].
- **The PC-R sets are eclipse records.** R1 and R3–R8 are solar or lunar eclipses [DESIGN §4.3].
- **The one planetary analogue is excluded.** R2 alone contains planetary clues: Venus greatest evening elongation and Mercury greatest morning elongation. The design expects that part to fail at ±1 day, since the records are 3 and 16 days from the true extremes [ctl §0 item 2]. It then counts R2 "on its eclipses-only run".
- **PC-S cannot show sight.** It generates its clue sets with the same ephemeris, grammar and code it searches with [DESIGN §4.2; ctl §7.2]. Zero-noise recall therefore tests self-consistency, not sight (issue 14).
- **So outcome 3 cannot fire for the clue types that matter.**
  - Outcome 3 fires only on PC-R < 4/8 or PC-S < 0.5 at noise level (ii) [DESIGN §6].
  - A method that cannot recover real planetary and stellar records at B&M's tolerances is therefore certified as able to see. R2 is predicted to show exactly that.
  - The expected verdict, "the match is ordinary", would then be a "no" from an instrument never shown to see this kind of signal, which is the case the bench's own rule forbids.

**Fix.**
1. Split outcome 3 into two outcomes:
   - 3a: the eclipse-detection component cannot see;
   - 3b: the B&M-type component (stars, Venus, Mercury, lunar phase) cannot see.
2. Build a real-record control of B&M's types from dated *Almagest* records (IX–XI; local `ptolemy-syntaxis-grc.tsv`; Nabonassar and Dionysian dates). Planetary turning points and morning-star appearances with known dates, plus the true lunar phase on those dates, give sets searchable at B&M's tolerances and at the *Almagest* slack.
3. Count R2's planets in the gate. If they fail at ±1 d, report "B&M's tolerances cannot recover expert planetary records" as a finding that conditions every "no" about the Odyssey.
4. If no real control of this type can be built, say so in the verdict: the ability to recover B&M-type clues from real records is then untested.

### Major

#### 4. The pre-registration cannot be verified and does not cover the code (major)

**Where:** DESIGN §7.4, and the §6 preamble.

**Evidence.**
- The design says outright that odybench is not a git repository, so `DESIGN.md` "is the record".
- The freeze hashes `DESIGN.md` and `data/prereg/*` only. The code that computes every statistic (`sky.py`, `events.py`, `clues.py`, `reach.py` and the rest) is not covered.
- The predictions were written after exploratory computations by the same agents [DESIGN §2.5].
- `--unfrozen` lets every script run anyway.

A hostile referee will say the thresholds or the code were changed after the results came in, and nothing in the bench could refute that.

**Fix.**
1. Run `git init` and commit the design, the prereg files and all code before step 4.
2. Put the commit hash and a tree hash of `odybench/`, `tools/` and the top-level scripts into `PREREG.sha256`.
3. Publish the hash outside the machine, as a public commit, a gist or an OpenTimestamps proof.
4. Record every code change after the freeze as a dated amendment.

#### 5. Prediction 6 compares the four-clue rate with B&M's five-clue figure (major)

**Where:** DESIGN §1.1 item 2, and prediction 6.

**Evidence.**
- B&M's 1-in-2,088-years figure multiplies a seasonal rate of "one Ti every 6 years", and that rate already includes the equinox bound [B&M §Intersecting; bm §10 item 1; crit §4 item 5]. Prediction 6 tests λ(N∧C∧V∧M) ≥ 5 × 0.048 per century, with E off.
- **B&M's own arithmetic already predicts more.** With E off and their own ±1-day colour tolerance, 1.02 per year × 1/3 × 3/116 ≈ 0.0088 per year, or **0.88 per century** [me]. That is about 1.2 expected chance matches in 136 years.
- With E on and ±1 day, their figure becomes 0.14 per century, three times what they printed [me].
- The dossier's own estimate is about 0.8 per century [vis §5].

Prediction 6 is therefore near-certain, and it argues against a figure B&M did not give for the applied clues.

**Fix.** Make two comparisons instead:
1. λ(N∧C∧V∧M∧E), with E at ≤ 4, ≤ 5 and ≤ 6 Apr, against 0.048 per century: B&M as written.
2. λ(N∧C∧V∧M) against B&M's own arithmetic redone at their stated tolerance (about 0.9 per century). Predict this second ratio to lie within a factor of 2.

Correct §1.1 item 2 to say that the 6 years is the C∧E rate.

#### 6. p_fix conditions on the season clue, and the case for doing so rests on an unread source (major)

**Where:** DESIGN §3.2 item 4, §3.3 item 2, prediction 8, and §8 item 19.

**Evidence.**
- p_fix is defined as the fraction of spring new moons passing V and M, "N and C hold by construction", and called the probability for "a target fixed in advance (such as Schoch's eclipse)".
- Schoch fixed the target in 1926. If the season reading were also independent, the target's chance of passing C belongs in the coincidence. C passes 8.3% of new moons [vis §3.4], so P(C∧V∧M | target) ≈ 0.083 × 0.008 ≈ 0.0007 [vis §5 gives about 0.07%]. **Conditioning on C understates the coincidence about 12-fold.**
- Conditioning is right only if C was chosen with the target in view, which the design asserts [DESIGN §3.4 preamble] but cannot document:
  - MacDonald 1967, the source of the season reading, is unread [bm §1; DESIGN §8 item 19].
  - B&M say he supported March sailing [B&M §References].
  - Gainsford says he argued for the second half of May [gainsford2012.txt, around line 71].
  - That 1178 BC sits exactly on the C bound (Ti−12 = 4 Apr) [bm §5 C] is suggestive, not proof.
- Prediction 8's "the bench is not stacked against the claim" rests on p_fix.

**Fix.**
1. Report both p_fix given C and p_fix unconditional, with the reason for the choice frozen in the prereg.
2. Obtain MacDonald, *JBAA* 77 (1967) 324–328, before freezing. It decides whether the March season was formed without the 1178 eclipse in view.
3. Correct §8 item 19 to read "contested".

#### 7. The garden's composition can set G (major)

**Where:** DESIGN §3.4, and predictions 10–11.

**Evidence.**
- The full garden has 428,544 readings. It includes options nobody has proposed for this passage: Jupiter, Sirius or Mars as the herald; 31 Mercury variants; Day 0 at the first crescent.
- G cannot fall when forks are added.
- Prediction 11 expects G ≥ 0.10 without any computation behind it.
- G_BM, which has 72 readings, is computed but not designated as decisive.

A referee defending B&M will call the full garden a straw garden, and the decision rule gives them nothing to answer with.

**Fix.** Use three nested gardens and name G_BM as primary:
1. **G_BM:** the forks B&M themselves raised.
2. **A "documented" garden:** only forks with a named published proponent. Examples are Austin's autumn, the scholia's slow-setting Boötes, de Jong's 19-day count, Stanford's count and Solon's noumenia.
3. **The full garden:** an upper bound.

Report G for all three, together with the smallest set of forks that reaches G ≥ 0.05. Store the source of every fork in `garden.json`.

#### 8. The formulaic day counts are not priced (major)

**Where:** DESIGN §3.4 fork F1, and §4.2 noise level (ii).

**Evidence.** Several of the day counts are typical numbers:
- The 17-days-then-18th pair of 5.278–279 recurs for Achilles' funeral, "ἑπτὰ δὲ καὶ δέκα … ὀκτωκαιδεκάτῃ" [Od. 24.63–65, checked].
- The nine-then-tenth pattern occurs 14 times [txt §3].
- "τρίτον ἦμαρ ἐυπλόκαμος τέλεσ' Ἠώς" occurs three times (5.390 = 9.76 = 10.144) [txt §3].
- The "twentieth day" appears at 5.34 and 6.170.

Fork F1 allows only ±1 day at two joints [chron §5.1], and PC-S jitters offsets by only ±1 day. This is Gainsford's central philological objection [crit §3.3], and the bench does not test it.

**Fix.**
1. Add a fork F1b in which each typical-number interval is uncertain by ±2 or ±3 days, or is replaced by the other typical numbers (9/10, 12, 17/18, 20).
2. Run PC-S at ±2–3 days.
3. Report how reach and recall decay as the jitter grows.

#### 9. Fixed Julian cut-off dates are carried across 900 years and into the controls (major)

**Where:** DESIGN §2.2, §3.2 item 1, §3.4 fork F6, and §4.2–4.3.

**Evidence.**
- C (17 Feb, 4 Apr) and E (1–5 Apr, with F6's 1–4 and 1–6 Apr) are fixed Julian dates. N1 applies "the B&M reading (T0b conventions)" across 1500–600 BC (−1499 to −599).
- **The equinox drifts against the Julian calendar.** The Julian year is about 0.0076 days longer than the tropical year, so the equinox moves about 0.76 days earlier per century [me].
  - It falls on 1 Apr in 1178 BC [bm §3.2], about 27–28 Mar in 600 BC (−599) and about 3–4 Apr in 1500 BC (−1499) [me].
  - In 600 BC the bound "1 Apr ≤ Ti−11" therefore means 5–9 days after the equinox.
- **The star phases drift the other way.** They move about 0.64 days later per century (sidereal against Julian year) [me], and precession adds its own changes. In 701 BC (−700) Arcturus first stands ≥ 5° high at nautical dusk on 26 Feb [vis §3.3], against the 17 Feb cut-off.
- **The controls are affected too.** PC-S truth dates span 1400–600 BC and the PC-R truths reach AD 136.
  - Suppose the generator defines "spring" from the real sky while the searcher uses the fixed dates. Zero-noise recall then falls below 0.99 near the window edges.
  - §4.2 would call that shortfall "a bug" (issue 14).

**Fix.**
1. In every null and control, express C and E relative to events computed for each year: Ti−11 within 0–4 days after the computed equinox, and the star bounds from F3(b).
2. Keep the fixed Julian dates in T0b only.
3. Report λ per century, to show the rates are stationary.

#### 10. The eclipse classes were defined around the target and are estimated from it (major)

**Where:** DESIGN §3.1 (X1–X4), §3.3 item 1, §3.4 items 3 and 5, and predictions 13–14.

**Evidence.**
- **X1 is not Schoch's class.** It is labelled "Schoch's" but uses a maximum at 10–14 h LAT. Schoch required greatest phase between 10 a.m. and noon [bm §11].
  - Under Schoch's own rule, 24 Jun 1312 BC (−1311) drops out of X1. Its maximum falls at 12:02 LMT [me: check_bessel.py] and about 12:09 LAT [win §7.1].
  - The "±1σ" rule admits 1178 BC at +0.3σ [DESIGN §2.5].
- **The spring base rate is estimated from the target alone.** In 1500–600 BC, X1 is {1312, 1178, 1131 BC}, and only 1178 BC is a spring new moon. So p_e(X1 ∩ P_spring) is estimated from the target itself.
- **G over X1 rests on two events.**
  - Reach leaves out targets within 251 years of the background's ends, so the usable span is 1249–851 BC (−1248 to −850) [me].
  - That leaves two X1 targets, 1178 and 1131 BC. G over X1 therefore rests on n = 2, one of which is the claim itself.
  - Prediction 13 tests 1312 BC, which the same edge rule excludes.

**Fix.**
1. Replace the binary classes with a probabilistic hit strength: P(total at the site | ΔT model) and P(magnitude ≥ m).
2. Extend the background to the limit of the NASA elements (−1999) and of DE441. Alternatively, estimate p_e by rotating longitude at a fixed latitude, which gives a rate that does not depend on Ithaca.
3. Exclude the target from its own base rate.
4. Report results for 10–12 h and 10–14 h, and for ±0.5σ, ±1σ and ±2σ.

#### 11. The held-out test is neither held out nor independent (major)

**Where:** DESIGN §5, and predictions 26–27.

**Evidence.**
- **Two outcomes are already known.**
  - H1, a night of at least 12.0 h, is known to fail for 1178 BC: the nights were 11.5 h and 11.3 h [DESIGN §5; txt §5.6]. The 12.0-h threshold was frozen after those lengths were computed.
  - H5 is B&M's own post-hoc observation.
- **The predicates are tied to the clues that were fitted.**
  - H1 measures the season, which C already fixes. A night of 12 h or more needs a date before late March or after late September [txt §5.6 night-length table].
  - H3 (Mercury invisible or near conjunction on Day 0) depends on M: 34 days after a morning rising-azimuth maximum, Mercury is heading for superior conjunction [vis §2.3 spacing; me].
  - H4 depends on the Venus elongation that V fixes.
- With base rates "on random candidates" [DESIGN §5 (iii)], H1 fails and H3 passes for structural reasons alone.

**Fix.**
1. Compute each base rate conditional on the reading, among candidates that pass the same N, C, V and M, or compare 1178 BC only with the other survivors of that reading.
2. Leave H1 and H5 out of the counted statistic, or label it non-blind.
3. Add the ancient autumn reading (issue 18).

#### 12. The Mercury criterion as specified is numerically ill-conditioned (major)

**Where:** DESIGN §2.2 step 5, the M row of the §2.2 parameter table, `sky.py` [DESIGN §7.1], and §2.5.

**Evidence.**
- T0b takes "the date of the local maximum of that daily series nearest Ti−34". Near its maximum, Mercury's rising azimuth changes by less than 0.01° a day.
- My recomputation uses a rise bisection to 0.01 s on `ephem` positions [me: check_mwra.py]. The values bracketing each maximum are below; the vertex is a parabola through the three days around it.

  | Year | Day before | Day after | Discrete maximum | Vertex | Δ from Ti−34 |
  |---|---|---|---|---|---|
  | 1178 BC (−1177) | 12 Mar 112.30419° | 13 Mar 112.29647° | 12 Mar | about 12.3 Mar | about +0.7 d |
  | 1189 BC (−1188) | 12 Feb 120.48066° | 13 Feb 120.48110° | 13 Feb | about 12.5 Feb | |

  For 1189 BC the integer maximum is decided by **0.0004°**, about one second of rise time.
- **Coarse rise times scramble the series.** `check_extras.py` uses rise times rounded to the minute. It gives 112.20°, 112.16°, 112.20° and 112.18° for 11–14 Mar 1178 BC [results/bm2008-reconcile/check_extras.out.txt, lines 8–11]. That series is not monotonic and is about 0.1° off, enough to move the discrete maximum by days.
- Extraction b already noted that the maximum is "flat-topped, so ±1-2 days is intrinsic" [bm-b §13 item 5].
- `sky.py` plans "about 3 evaluations per event" [DESIGN §7.1].
- M carries about 4.5 of the 10.8 bits in the budget [DESIGN §1.2], and it alone produced the 1157 and 1189 BC flips [DESIGN §2.5].

**Fix.**
1. Define the MWRA as the vertex of a parabola fitted to the daily azimuths over ±3 days, and Δ as a continuous difference.
2. Require rise times converged to better than 0.1 s for this quantity.
3. Record the curvature of each maximum and flag flat ones.
4. Report the M pass set under h0 ± 0.1°, latitude 38.2–38.6°, refraction on and off, and ΔT ± 1σ.
5. Cross-check against `check_mwra.py`'s independent rise finder on all 152 S2 years.

#### 13. One sky-table implementation feeds every test, so a common-mode bug would not show (major)

**Where:** DESIGN §3.1 and §7.1–7.2.

**Evidence.**
- **One table serves everything.** The target, the nulls, the gardens, PC-S and the negative controls all read the same `sky_*.npz` from `sky.py` and `events.py`.
- **The derived events are unvalidated.** The `ephem` positions are validated against Horizons [eph §7]. No rise, set, twilight, station, elongation or star phase has been validated against anything.
- **PC-S would hide such a bug.** It would reproduce the bug in its generator and its searcher alike.
- **Plausible bugs of this kind:**
  - proleptic-Gregorian dates from `numpy.datetime64` or `datetime` (an 11-day shift at −1177 [DESIGN §0]);
  - day offsets off by one (−34 against −33 is exactly the parallel reading);
  - leap-day arithmetic;
  - the azimuth convention (the azimuth minimum is 29 days from the maximum [bm §5 M]).

**Fix.**
1. Check 1,000 random rise and set events against Horizons' rise/transit/set output, and against the dense-grid rise code in `results/bm2008-reconcile/`, to within 0.5 min.
2. Check the stations and elongations from `events.py` against the lists in `check_mwra.py` for all 152 years.
3. Check the heliacal star phases against vis §3.3 (independent Meeus-based code) at −1177 and −700.
4. Write a minimal second implementation of B&M's reading, independent of `clues.py`, that must return the identical T0b pass set.
5. Property-test the calendar module over −1999 to +500 (round trips, day of year, the leap rule), and ban `datetime` and `datetime64` from the bench.
6. Keep this review's independent Besselian solver as a cross-check of `eclipses.py`.

#### 14. PC-S is self-referential, and its generator and searcher use different grammars (major)

**Where:** DESIGN §4.2 steps 2–3, its pass criterion, and prediction 21.

**Evidence.**
- **The generator** describes Mercury by "the nearest of MWRA, elongation, station and first visibility" and the season as "spring, autumn or none".
- **The searcher** is "B&M's method, unchanged", which uses the MWRA and a fixed spring window.
- **The pass criterion** then says that recall below 0.99 at zero noise "is a bug".
- **Both ways out fail.**
  - A clue such as "station within 2 days" or "autumn" cannot be recovered by B&M's method, so recall below 0.99 is built into the design.
  - Restricting the generator to B&M's grammar instead makes recall 1 by construction, and the test then shows nothing.

**Fix.** Split PC-S into two modes:
1. **An instrument mode.** Generator and searcher share one grammar and the requirement is recall = 1.000. Generate the descriptions by an independent code path, either the low-precision code in `results/bm2008-b-checks/` or Horizons for a subsample, so that shared bugs show up as failures.
2. **A science mode.** The generator speaks its own vocabulary, every garden reading is scored, and there is no "bug" threshold.

#### 15. The negative controls are mis-built and cannot support outcome 4 (major)

**Where:** DESIGN §4.4 (NC1–NC5), and predictions 24–25.

**Evidence.**
- **NC1 (the Iliad) is not a negative under the hypothesis being tested.**
  - It comes from the same tradition and the same composers, and the design itself tests whether its date agrees with the Odyssey's.
  - Yet NC1 is the only negative with an eclipse slot, so in practice outcome 4 rests on the Iliad.
- **NC2 reads Aeneid 2.255 one way only.**
  - The line, "a Tenedo tacitae per amica silentia lunae" [checked], is taken to mean the Moon was up and at least half lit.
  - In Latin, *silens luna* is the Moon at conjunction. Pliny says some call the day of conjunction the day of "silentis lunae" [*NH* 16.190; local key 16.39.2].
  - On that reading NC2 becomes a new moon followed by Lucifer at dawn (2.801): an Odyssey-shaped set that is compatible with an eclipse. The expectation "no uniqueness" then no longer follows.
- **NC3 takes its season from a simile.** *Arg.* 1.1202 ("χειμερίη ὀλοοῖο δύσις πέλει Ὠρίωνος") sits inside a simile, "ὡς δ' ὅταν" at 1.1201 [checked]. The design excludes similes as date carriers for the Odyssey (H10).
- **NC4 misreads its text.** In *h.Herm.* 141, "παννύχιος· καλὸν δὲ φόως κατέλαμπε Σελήνης", παννύχιος closes Hermes' clause: the text does not say the moonlight lasted all night [checked].
- **NC4 and NC5 cannot fail.** NC4's zero survivors and NC5's lack of a unique survivor follow from the construction (contradictory clues; annual phases). They test plumbing, not specificity.

**Fix.**
1. Reclassify the Iliad as a same-tradition comparison.
2. Build clean negatives with clues as rich as the Odyssey's from local late fiction, and apply the Odyssey's own selection rules to them (no similes, no lying tales):
   - the *Aeneid*, under both readings of 2.255;
   - the *Argonautica*'s non-simile clues (1.1273, and 4.1695–1697);
   - Quintus Smyrnaeus;
   - Valerius Flaccus.
3. Make N4's synthetic poets the main negative.
4. Move NC4 and NC5 to the instrument checks.

#### 16. The likelihood ratio mixes events, assumes a noise level and may be under-sampled (major)

**Where:** DESIGN §3.8, §3.5, §4.2 noise level (iii), and the LR thresholds 10 and 30 in §6.

**Evidence.**
- **The two sides count different events.** The numerator is said to come from "X-class eclipse dates", but PC-S pool (a) is any eclipse of magnitude ≥ 0.95 anywhere in the Greek world.
- **The noise level is a design choice.**
  - Levels (ii) and (iii) are chosen by the bench.
  - Level (iii) applies the *Almagest*'s 16-day Venus slack, which was measured for greatest elongation [ctl §0 item 2], to B&M's Venus rise-lead clue. That clue has no turning point.
- **The denominator may be under-sampled.**
  - LR_garden's denominator comes from 1,000 epic gardens subsampled to 1,000 readings each [§3.5].
  - With about 3 X1 eclipses in 900 years [DESIGN §3.1], a small G leaves only single-digit double-hit counts.
  - The resulting LR then cannot be placed on either side of 10 or 30.

**Fix.**
1. Define both sides on the same event: a unique survivor whose eclipse at the named site has P(total) ≥ p or magnitude ≥ m.
2. Report the LR as a curve over noise (0, ±1, ±2 and ±3 d jitter; 0–16 d slack), and decide the verdict at the noise level most favourable to B&M.
3. Drop the Venus 16-day slack, or translate it into a rise-lead tolerance.
4. Require at least 20 denominator events, or compute P(unique) × p_e analytically under the N2 independence check. Give bootstrap intervals in either case.

#### 17. Several "pre-registered" predictions are already determined, and one fails as written (major)

**Where:** DESIGN §6, predictions 1–5, 18–21 and 24.

**Evidence.**
- **Prediction 18 is already known.** The per-model probabilities are in eph §5.4. Their equal-weight mean is (0.299 + 0.178 + 0.505 + 0.277 + 0.261)/5 = **0.30** [me]. In the canon frame I get 0.294 [me: check_p19.py]. P(magnitude ≥ 0.9) is 0.85–1.00 by model, mean about 0.91 [me: check_mag09.py].
- **Prediction 19 fails as written.** I worked in the canon frame, with NASA elements and my totality windows (1178 BC: 28,805–29,580 s; 1131 BC: 27,050–28,035 s) [me: check_p19.py]. The SMH models were converted with ṅ −25.82 → −25.858, about +34 s.

  | Model | P(total, 1178 BC) | P(total, 1131 BC) | Joint, common offset |
  |---|---|---|---|
  | SMH2016 parabola | 0.498 | 0.443 | 0.108 |
  | Addendum 2020 parabola | 0.173 | 0.641 | 0.052 |
  | other models | | | 0.047–0.049 |

  - "Higher for 1131 under every model" fails under the SMH2016 parabola.
  - "Joint ≤ 0.05" fails for two of the five models.
  - Caveat: the DE431 pairing would shift both windows by about 40 s.
- **Prediction 20 sits on its own expected value.** Going from B&M's ΔT to SMH2020 + 1σ moves UT by 1,660 s, or 27.7 min. That flips about 1.9% of conjunction dates [me], right at the 2% threshold.
- **The rest are known or tautological.** Predictions 1–5 are largely known [DESIGN §2.5]. Prediction 21 is tautological (issue 14) and prediction 24 is true by construction (issue 15).

**Fix.**
1. Move every computable item into §2.5 as known, with its numbers.
2. Restate prediction 19 per model.
3. Keep §6 for quantities that genuinely need new runs.

#### 18. The one reading formed without knowledge of any computed eclipse is missing (major)

**Where:** DESIGN §3.4 item 5, and §5 H9.

**Evidence.**
- The scholia read the season as autumn turning to winter. Five of them do so, on 11.373, 17.24, 17.191, 14.458 and 6.305 [txt §5.6].
- The scholia read 14.162 as the ἕνη καὶ νέα, the day of conjunction [txt §5.1].
- Heraclitus and Plutarch read 20.356–357 as a solar eclipse on that day [crit §3.1].
- **This reading is older than Schoch (1926) and cannot be contaminated by him.**
- Inside B&M's window, the canon gives a total eclipse at Ithaki on 30 Sep 1131 BC (−1130), at 11:12 LMT [crit §2.4; me: check_bessel.py].
- The design uses the scholia's season only qualitatively (H9), and lists 1131 BC only as an "alternative dating".

**Fix.** Pre-register R_anc, the ancient reading: autumn per the scholia, Day 0 at the conjunction, Theoclymenus' vision as the eclipse, and no planets. Report its survivors and its eclipse coincidence beside B&M's. It is the natural control for the circularity argument, and it cuts both ways.

### Minor

#### 19. The ΔT model list counts Espenak–Meeus twice and pairs one copy wrongly (minor)

**Where:** DESIGN §3.7 items 1–2, and prediction 18.

**Evidence.**
- N6 lists "Espenak–Meeus 28,716 s and its canon-ṅ form 28,589 s" as two of five models, and pairs E-M with the NASA elements.
- They are one model in two ṅ frames, −26 and −25.858 [eph §2.1, §2.3]. Only 28,589 s is consistent with the NASA elements, by DESIGN §0's own pairing rule.
- The equal-weight "five-model" mixture therefore gives E-M 2/5 of the weight.

**Fix.** Treat E-M as one model and mix over four. Use the −26 form only with an ephemeris whose ṅ is −26.

#### 20. Acceptance tolerances and calibrations were set after the measurements (minor)

**Where:** DESIGN §2.4 (A1, A3, A4), and §4.1 (I3).

**Evidence.**
- A1 requires ≥ 134 against a measured 136.
- A3 requires ≥ 124 and ≥ 138, exactly the measured values.
- A4's tolerances each sit just beyond a measured gap:
  - Venus 103.6 ± 1 min, centred on DE441, against B&M's 102.9;
  - the equinox within 10 min (measured 7);
  - twilight within 5 min (measured 4).
- I3 takes the Pleiades' arcus visionis and the "Arcturus ≥ 5°" rule from Hesiod's own numbers [vis §3.3, §6 item 6], then uses Hesiod to check them.

**Fix.** Either label these regression tests, or derive the tolerances beforehand from documented model differences: VSOP87 against DE441, the h0 conventions and the ΔT clock.

#### 21. Three definitions of eclipse magnitude are in use (minor)

**Where:** DESIGN §3.1 (X3 ≥ 0.95, X4 ≥ 0.6), and §4.1 I2b (agreement within 0.02).

**Evidence.** For the 1131 BC total eclipse at Ithaki the definitions give different numbers:
- The diameter ratio, (L1′−L2′)/(L1′+L2′), gives 1.0486, which is the "1.049" quoted.
- The fraction of the diameter covered, (L1′−m)/(L1′+L2′), gives 1.0169 [me: check_p19.py].
- ctl uses (r☉ + r☾ − sep)/(2r☉) [ctl §2.2].

Near magnitude 1 the definitions differ by more than I2b's 0.02 tolerance. The cases most exposed are Archilochus at 1.000 and Diodorus at 0.995.

**Fix.**
1. Pin one definition for each use: the covered fraction for partial phases, and a separate total or annular flag with duration.
2. Compare like with like in I2b.

#### 22. Calendar and epoch conventions are under-specified (minor)

**Where:** DESIGN §3.7 item 1, §2.2 step 1, and §7.5.

**Evidence.**
- **The epoch label is wrong.** The ΔT values are labelled "at −1177.29" (the same label appears as a column heading in eph §2.3). They were computed at decimal year −1176.68 [eph §2.3 header], and I reproduce E-M's 28,716.8 at −1176.71 [me]. Evaluating literally at −1177.29 moves the parabolas by about +11 s [me].
- **The new-moon count has three values.** Over "1 Jan 1250 – 31 Dec 1115 BC" it is 1,682 in the timing run, which ended at 0 h on 31 Dec [results/design-timing/timing.out.txt]. It is 1,683 in `check_ti` and 1,684 in B&M.

**Fix.**
1. Specify an inclusive end at 24:00 UT+2 on 31 Dec −1114, the TT-to-UT conversion, and the Julian-epoch formula.
2. Correct the label.

#### 23. The T0 verdict hides two choices (minor)

**Where:** DESIGN §2.4, and §3.4 (G_BM).

**Evidence.**
- **The equinox bound.** B&M's §References gives ≤ 5 Apr, but their probability paragraph says on or before 4 April [B&M §Intersecting]. Under ≤ 4 Apr, 1178 BC fails E, because Ti−11 = 5 Apr [bm §5 E].
- **Mercury's visibility.** B&M's text requires Mercury to be visible; T0b does not apply this.
- **G_BM excludes T0b's own reading.** G_BM fixes "visible", so the T0b reading is not a member of G_BM.

**Fix.** Report the T0 verdict under E ≤ 4, ≤ 5 and ≤ 6 Apr, with visibility on and off, and put the T0b reading inside G_BM.

#### 24. Factual and textual slips in DESIGN (minor)

**Where:** DESIGN §1.1 item 2, §3.1, §3.4 item 1, §5 H2 and H8, and §8 item 19.

**Evidence.**
- **(a) H8.** It reads a "starry pre-dawn sky" into 20.98–121. But "ἀπ' οὐρανοῦ ἀστερόεντος" (20.113) is a stock epithet: the phrase in its case forms occurs 11 times in the Iliad and Odyssey [me: grep], including in daylight at Od. 9.527. The scene also comes after the dawn at 20.91 [checked].
- **(b) H2.** "Given Day 0 a conjunction it holds almost always" is wrong. For the night after Day −5, the median Moon-up share is 25% [vis §4.5], so the < 25% threshold passes about half the time.
- **(c) §3.4 item 1.** It says 1189 BC "lies 11 years away, so reach is 0 for a 136-year window unless E is on".
  - The design's own interval, I = (max(t−W, s₋), min(t, s₊−W)), gives a reach of 11/136 ≈ 0.08.
  - Reach would be 0 only if another survivor fell between 1177 BC (−1176) and 1053 BC (−1052). No note has computed that span [me].
- **(d)** X1 is called "Schoch's" (issue 10).
- **(e)** §8 item 19 calls March "MacDonald's March reading" as if settled (issue 6).
- **(f)** §1.1 item 2 omits that the 6 years includes E (issue 5).

**Fix.** Correct each one.

#### 25. Star inputs need checking at fetch (minor)

**Where:** DESIGN §7.3.

**Evidence.**
- The new grammar stars come with HIP numbers "from memory": Sirius 32349, Aldebaran 21421, Betelgeuse 27989, Rigel 24436 and Dubhe 54061. They match my recollection too, but neither of us has checked a catalogue.
- Sirius is a 50-year binary. Its short-baseline Hipparcos proper motion includes an orbital component of order 0.3″ a year [me: order of magnitude, from a ≈ 7.5″ and P ≈ 50 yr]. Over 3,100 years that can amount to 0.2–0.3°, enough to move its heliacal date by a fraction of a day.

**Fix.**
1. Verify the HIP numbers when fetching.
2. Use a long-baseline or barycentric proper motion for Sirius, and record which one was used.

---

## 3. What I could not check

- **MacDonald 1967** (*JBAA* 77:324–328). It is unread, and the secondary reports conflict (B&M against Gainsford). It bears on issue 6.
- **Starry Night's ṅ and ΔT recipe, and PLSV's parameters.** I have nothing to add to DESIGN §8 items 4 and 6.
- **Servius on *Aen.* 2.255.** It is not local. The interlunium sense of *silens luna* rests here on Pliny *NH* 16.190 alone.
- **The source of Ptolemy's mid-eclipse times in R1.** They are his own reductions from the reported start times [4.6.3]. I did not trace the Babylonian originals.
- **Whether any survivor lies between 1177 BC (−1176) and 1053 BC (−1052).** This decides the reach of 1178 BC under the T0b reading (issue 24c). The DE441 excerpt covers it, but it was not computed.
- **Bench code.** I ran none, because none exists. My eclipse checks use my own solver on NASA's elements. My rise times use my own bisection on `odybench.ephem` positions, and positions are the only part of `ephem` that has been validated against Horizons.

## 4. Files produced for this review

All are in `C:\Projects\odybench\results\critique-design\`, each with its `.out.txt`:

| Script | What it does |
|---|---|
| `check_bessel.py` | An independent local-circumstance solver for NASA polynomial elements. It covers 1178, 1131, 1312 and 1183 BC at Ithaki, with totality windows. |
| `check_p19.py` | P(total) for 1178 and 1131 BC under each ΔT model, and the joint probability; magnitude definitions. |
| `check_mag09.py` | The ΔT range with magnitude ≥ 0.9 at Ithaki, and its probability under each model. |
| `check_mwra.py` | Mercury's rising azimuth near the maximum, with rises bisected to 0.01 s, for 1178 BC and 1189 BC. |
| `check_venus.py` | Venus leads on 11 Apr 1178 BC and 13 Mar 1189 BC. |
| `check_lines.py`, `check_lines2.py`, `check_lines3.py`, `check_lines4.py` | Printouts of every cited line from `data/text/`. |
