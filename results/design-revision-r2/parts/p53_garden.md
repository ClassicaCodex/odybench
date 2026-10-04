### 5.3 N3: forking paths

B&M's criteria were not fixed in advance (1.1). N3 counts the readings a
careful reader could defend, sorts them by who has defended them, and asks
how often *some* reading makes a given target the unique match.

**The forks.** Each option carries its source and its tier in
`data/prereg/garden.json`. "None" means the clue is dropped. Tier BM holds
the options B&M themselves raised. Tier DOC adds options with a named
published proponent for this passage, or the standard published
operationalisation of what such a proponent says. Tier FULL adds the rest
[rev #7]. Day tolerances are continuous: a vertex or event instant is
compared with the stated day's instant. B&M's integer tolerance of n days is
equivalent to n + 0.5 continuous days, because a vertex lies within half a
day of its discrete maximum [r1 N13].

| fork | option | tier | source |
|---|---|---|---|
| F1 day count | B&M sequential (34/29/5) and parallel (33/28/4) | BM | [B&M Table 1; chron §5.1] |
| | de Jong 2001 (33/28/5), Stanford 1959 (32/27/4) | DOC | [chron §0 item 4] |
| | the four inclusive-raft rows | FULL | [chron §5.1] |
| F1b typical numbers [rev #8] | off | BM | — |
| | every offset that depends on a typical-number joint (H→D "fourth/fifth", D→Σ "seventeen/eighteenth", Σ→L "two nights … third", "twentieth") uncertain by ±2 d; or by ±3 d | DOC | Gainsford's objection that the counts are formulaic [crit §3.3]; 5.278–279 = 24.63–65 [rev #8]; [txt §3] |
| | D→Σ replaced by another typical number, 9, 12 or 20 days | FULL | [rev #8 fix 1] |
| F2 Day 0 | (a) conjunction date, UT+2 | BM | [B&M] |
| | (c) the day after, Solon's noumenia; (d) the first-crescent day, Yallop B, day counted from sunset | DOC | Plut. *Sol.* 25.3; Geminus 8.11 [vis §4.1] |
| | (b) conjunction date, LMT | FULL | a clock convention, not a reading |
| F3 stars | (a′) C_rel, B&M-calibrated (4.5) | BM | [B&M; MacDonald 1967, unread §2] |
| | (e) autumn: every raft night inside the autumn co-visibility window (both stars ≥ 2° at the end of nautical twilight), recomputed each year; (f) none, "late-setting" as a permanent property | DOC | (e) Papamarinopoulos et al. 2012 [unread §4] and the scholia's season [txt §5.6]; (f) the scholion on 5.272 and Aratus 581–585 [vis §3.1] |
| | (b) both ≥ 2° on every raft night; (c) both ≥ 5°; (d) departure night only, ≥ 2°, either season | FULL | [vis §3.3–3.4] |
| F4 morning star | Venus rises ≥ 90 min before the Sun | BM | [B&M] |
| | Venus a visible morning star (AV 7°); none (a dawn time-marker) | DOC | MacDonald identifies the star as Venus near morning elongation [unread §2.5], AV from de Jong [vis §1.2]; Gainsford's formula argument [crit §3.3; txt §5.7; neg §5 item 3] |
| | ≥ 60 min; ≥ 120 min; any bright dawn herald (Venus, Jupiter, Sirius, Mars ≤ −1 mag) | FULL | [vis §1.3–1.4] |
| F5 Mercury | event MWRA (vertex), GWE or morning station × tolerance 1.5, 2.5, 3.5 d (B&M's 1, 2, 3 integer days) × visibility (AV 10°) required or not: 18 options | BM | B&M name all three events and require visibility; S2 never applied it [B&M §References; bm §5 M; rev #23; r1 N13] |
| | event "any of the three"; tolerance 6 d (the slack of Ptolemy's Mercury records, 14/14 within 5.5 d [alm §4]); morning first visibility (AV 10°) at 1.5, 2.5, 3.5 or 6 d; none | DOC | B&M call the events close in time; the *Almagest* records; B&M's "heliacal rising 13 Mar" [bm §9]; Gainsford, and the absence of any ancient Hermes–Mercury link before Plato [txt §5.9] |
| F6 equinox | off | BM (rule gardens) | B&M listed E and did not apply it [B&M §References, §Intersecting] |
| | E_rel with n = 3, 4, 5 | BM (reported gardens only) | MacDonald's reading, formed with the target in view (below) |
| F7 window width | 136 years | BM | [B&M] |
| | 91 (Troy VIIa) and 251 (primary) years | DOC | [win §4, §9] |

**The conditioning rule** [r1 N6; rev #6]. The record shows that every
categorical reading of the clues B&M used was formed by a reader who knew
the target [unread §2.4, §9 item 3]:

| clue | categorical reading | first formed by | the alternative | how the rule gardens treat it |
|---|---|---|---|---|
| N | Day 0 is the conjunction | the scholia on 14.162 (ancient; blind) | — | no conditioning needed: every target is a new moon |
| C | the raft nights are in **spring** | MacDonald 1967, with the eclipse in view; before him every reading was autumn or winter | autumn; none | **conditioned** in 𝒢_BM (target pool T_C ⊂ T_A); priced in 𝒢_DOC by options (e) and (f), but also conditioned there (below) |
| V | the herald star is **Venus**, a morning star | MacDonald, who checked Venus in the eclipse year | none (a dawn formula) | **conditioned** (Venus slot of T_A) |
| M | Hermes' flight is **Mercury** | B&M, who knew the target | none | **conditioned** (Mercury slot of T_A) |
| E | Poseidon's return marks the **equinox** | MacDonald, who fitted his timetable to the eclipse | none | **left out** of every rule garden (F6 = off), and T0 must reproduce without it (3.5) |

A target's agreement with a reading formed for it is not evidence.
Conditioning removes that agreement and keeps the evidence that remains:
whether B&M's *tolerances* (a 90-minute lead rather than any visible morning
star; a Mercury event within 1.5–3.5 d rather than within 6 d) single a
target out, as priced by B&M's own tolerance forks.

E is treated differently from C, V and M for two reasons:

- The text gives Poseidon's day and nothing else about the Sun, so E has no
  tolerance part that could survive conditioning.
- Conditioning on it (E_rel at n = 5) would leave about 28 targets
  (139 × about 0.2). No interval over so few targets could fall below 0.05
  (2.8).

Leaving E out treats the Odyssey and the null alike: the target loses the
uniqueness E gave it, and so does every random target. G with E-on readings
is reported in two forms: union-priced over T_A, and conditioned over
T_A ∩ E_rel(5). Revision 2's G over T_C (season only) is reported too, so G
appears under both conditionings [r1 N6 fix 2].

The rule applies the same pool, T_A, to 𝒢_DOC, although 𝒢_DOC also holds
options that price C, V and M by union ("none", autumn). A union prices only
the choice to include a reading. It does not price the invention of a
reading that fits, which is what the record documents. The DOC options
still widen the tolerance forks (F1, F1b, F2, F4 visible, F5 at 6 d, F7)
for targets in T_A.

**Garden sizes** [me: `cp_bounds.py`; revision 2's sizes are reproduced by
r1 §3].

| garden | F1 | F1b | F2 | F3 | F4 | F5 | F6 | F7 | readings | bits | eclipse-compatible |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 𝒢_BM* (rule) | 2 | 1 | 1 | 1 | 1 | 18 | 1 | 1 | **36** | 5.2 | 36 |
| 𝒢_DOC* (rule) | 4 | 3 | 3 | 3 | 3 | 37 | 1 | 3 | **35,964** | 15.1 | 11,988 |
| 𝒢_FULL* (reported) | 8 | 6 | 4 | 6 | 6 | 37 | 1 | 3 | **767,232** | 19.5 | 383,616 |
| 𝒢_BM, 𝒢_DOC, 𝒢_FULL with F6 (reported) | | | | | | | 4 | | 144; 143,856; 3,068,928 | 7.2; 17.1; 21.6 | 144; 47,952; 1,534,464 |

F5's 37 in DOC and FULL is 4 events × 4 tolerances × 2 visibility settings,
plus first visibility at 4 tolerances, plus none. **T0b's own reading (in
its C_rel form, visibility off, F6 off) is a member of 𝒢_BM*** [rev #23].
Only F2 (a) and (b) put the conjunction on Day 0, where Theoclymenus speaks
[chron §4.H].

Two readings are left out because they cannot change the result: Day 0 as a
20-day window, and N dropped. Their candidates are days, a superset of the
conjunction dates, so they add no reach for any New Moon target [v1 §3.4;
rev §1 confirms].

**The statistic: reach.** For a reading r, let S_r be its survivors over the
background, each mapped to its conjunction (under F2 (c) and (d) a candidate
is mapped back). A target t ∈ S_r is the unique survivor of a W-year window
[a, a + W) placed at a uniformly random start a with t inside, exactly when
the window misses the neighbouring survivors s₋ and s₊. That is,
a ∈ I_r(t) = (max(t − W, s₋), min(t, s₊ − W)]; if t ∉ S_r, I_r(t) is empty.
Over a garden 𝒢, **reach_W(t; 𝒢) = |∪_{r∈𝒢} I_r(t)| / W**. For gardens with
several widths, reach(t) = max over W of reach_W(t), a lower bound on the
union [v1 §3.4]. Under T0b with E off, reach_136(1178 BC) ≤ 0.081, and it is
0 if a survivor falls in −1176..−1052 [rev #24c; P16].

**G and its interval.** For a garden 𝒢, a pool P and widths W:

- **G(𝒢; P; W)** = the mean of reach(t; 𝒢) over the targets t ∈ P, with
  16 Apr −1177 excluded. G is the look-elsewhere-corrected p-value of a
  coincidence whose target was fixed first, as Schoch's was: the chance that
  a target of the pool, fixed in advance and unrelated to the text, is made
  the unique match by some reading of 𝒢 in a window placed at random around
  it.
- **The interval** [G_lo, G_hi] is the 95% gamma interval of Fay & Feuer
  (1997) for a weighted sum of counts [r1 N8 fix 2]. Each target counts
  1, weighted by reach/n, and the largest possible weight is 1/n. Let
  y = G, v = Σ (reach/n)² and w = 1/n. Then
  G_hi = ((v + w²)/(2(y + w))) · χ²_{0.975}(2(y + w)²/(v + w²)) and
  G_lo = (v/(2y)) · χ²_{0.025}(2y²/v), with G_lo = 0 when y = 0.
  - With no target reached, G_hi = 3.69/n.
  - When every nonzero reach is 1, the interval is the exact Poisson one.
  - Unlike a binomial bound on the share of targets reached, it does not
    treat a reach of 0.2 as 1.

  The formula is given from memory. The implementer checks it against the
  paper, and I9 checks its coverage by simulation.
- **Rule quantities.** Each comes with its pool size n and the number k of
  targets with reach > 0.

  | quantity | garden | pool | W | used for |
  |---|---|---|---|---|
  | **G_BM** | 𝒢_BM* | T_A | 136 | outcomes 1 and 2 |
  | **G_DOC** | 𝒢_DOC* | T_A | max over 91, 136, 251 | outcome 1 when Q_BM holds |
  | **G_BM,u** | 𝒢_BM* | T | 136 | outcome 4: the Odyssey's coincidence as B&M would present it, every reading treated as blind, compared with fiction's blind readings |

  G_BM,u = (n_A/n_T) G_BM exactly (4.2).
- **Reported beside, never in the rule:**
  - G over T_C (revision 2's season-only conditioning);
  - the E-on gardens over T_A and over T_A ∩ E_rel(5);
  - G_FULL*;
  - G_BM on each half of the core (stationarity);
  - **G_any**, the fraction of the pool with reach > 0. B&M's window was
    itself drawn from the tradition that chose the eclipse [win §6];
  - **G_X**, the h_tot-weighted mean reach over the eclipse new moons of the
    pool, with 16 Apr −1177 excluded, compared with G_u. If eclipse new moons
    are reached at the rate of other new moons (P21), the eclipse adds
    nothing beyond its rarity.

**Reported:**

1. reach(16 Apr 1178 BC) under the T0b reading, 𝒢_BM*, 𝒢_DOC*, 𝒢_FULL* and
   the E-on gardens.
2. Every G of the list above, with k, n and the interval.
3. **The smallest fork set that reaches G ≥ 0.20 over T_A**, built by greedy
   addition to 𝒢_BM* of the option that raises G most. The sequence and each
   option's source are printed [rev #7].
4. The look-elsewhere factor G_BM / p_fix,unique, where p_fix,unique is the
   same quantity for the T0b reading alone.
5. **Alternative datings.** Every eclipse new moon with h_tot ≥ 0.1 at any
   Ionian site that some eclipse-compatible reading makes unique, with the
   readings that do it. Four are listed whatever the result:
   - 30 Sep 1131 BC, total at Ithaki at canon ΔT and inside B&M's window
     [rev V6];
   - 24 Jun 1312 BC, the Iliad date of Henriksson 2012 [unread §5];
   - 30 Oct 1207 BC, from Papamarinopoulos et al. 2012 [unread §4];
   - 12 Jan 1183 BC (−1182), Schoch's rejected annular eclipse [unread §3.1].
     Research-window's "1182 BC" for the same catalogue row is a slip
     [win §7.2].
6. Survivors per century for every reading, so the strictness of each
   garden is visible.

**R_anc, the ancient reading** [rev #18; r1 N9]. This pinned reading was
formed without knowledge of any computed eclipse, from the scholia,
Heraclitus and Plutarch:

- **Day 0** is the conjunction date (LMT at Ithaki): the scholia's ἕνη καὶ
  νέα on 14.162, and Heraclitus [txt §5.1].
- **Season.** The scholia read the season as "autumnal, and already towards
  winter" (17.24) and as winter (6.305, 14.458) [txt §5.6]. Greek sources
  divide the year two ways:
  - the agricultural year opens autumn with Arcturus' morning rising (*WD*
    609–611) and winter with the Pleiades' morning setting (*WD* 615–617);
  - Geminus divides the year at the equinoxes and solstices (1.9).

  The two divisions disagree. The primary reading therefore follows the rule
  the controls file applies when sources disagree: the weakest reading both
  allow [pcr §2]. Day 0 must fall **from Arcturus' heliacal rising (AV 10°,
  computed each year) to the spring equinox**, that is, in autumn or winter
  on either division. The alternatives are:
  - Geminus' autumn alone, [180°, 270°) of solar longitude (revision 2's
    bound, now sourced);
  - Hesiod's autumn alone, from Arcturus' heliacal rising to the Pleiades'
    morning setting;
  - Geminus' autumn and winter, [180°, 360°).
- **Eclipse.** Theoclymenus' vision is read as a solar eclipse on Day 0
  (Heraclitus; Plutarch, *De facie* 19 [crit §3.1]): h_06(u, ithaki) ≥ 0.5.
- **No planets and no stars**, because the scholia read 5.272 as
  slow-setting.

R_anc is run **with and without the eclipse clue** [r1 N9 fix 2]:

- **Without it**, the only clues are the conjunction and the season, so
  about six new moons a year survive. That version never has a unique
  survivor, so the ancient reading dates nothing without the eclipse. It is
  the only version whose "coincidence" could be compared with B&M's, and the
  comparison is empty by arithmetic.
- **With it**, R_anc is the ancient reading's own dating. Its survivors in
  each window, their h_tot, and whether one is unique are reported beside
  B&M's.

What is already known (2.8): 30 Sep 1131 BC passes the primary season (16–20
days after Arcturus' heliacal rising) and fails Geminus' autumn (3 days
early). 16 Apr 1178 BC fails every season option. R_anc is not in the
decision rule. The held-out predicates (section 7) are also run on its
survivors.

### 5.4 N4: random epics, the main negative

N3 holds the poem fixed and varies its reading. N4 holds the reading
machinery fixed and varies the poem. Random poems of the Odyssey's grammar
are the main negative of the bench [rev #15 fix 3]. They set the percentile
that outcomes 1 and 2 use.

**The grammar** (`data/prereg/epic_grammar.json`, as in revision 1, except
that season clues are relative to each year's sky):

- **Day 0 anchor:** conjunction, full moon, the 7th day of the month
  (Apollo's day in Hesiod, *WD* 770–771 [txt §5.3]), or none.
- **Season clue:** a pair from the archaic star list (Pleiades, Hyades,
  Orion, Sirius, Arcturus [txt §5.8]). Either both stars are ≥ 2° at the end
  of evening or morning nautical twilight on one night or on a 17-night
  span, or one star's heliacal rising or setting falls within ±k days.
- **Planet clue:** Venus, Mercury, Mars, Jupiter or Saturn, in one of three
  forms:
  - a morning object with rise lead ≥ 60/90/120 min;
  - an evening object with set lag ≥ 60/90/120 min;
  - within ±1.5–3.5 days of a turning point (rise- or set-azimuth extremum,
    greatest elongation, station, opposition) or of first or last visibility
    (Ptolemy's AV: Venus 5°, Mercury 10°, Jupiter 10°, Mars 11.5°, Saturn
    11° [vis §1.2]).
- **Offsets.** Variant A ("B&M-shaped") puts a season clue on a span
  starting between −29 and −27, and two planet clues at −5 and −34, around a
  conjunction anchor; the clue types are drawn at random. Variant B draws
  the anchor, two or three sky clues and their offsets (−40 to −1) freely.

10,000 epics per variant (seed in `seeds.json`), site `ithaki`, evaluated
over the background.

**Per epic:**

- p_c, its primary reading's per-candidate pass rate (its specificity);
- the survivor count in a 136-year window at a random position, and
  P(unique);
- **T_best ≥ T_obs.** Each date is scored by −log10 of the product of the
  per-clue base rates at the observed tightness (P(Venus lead ≥ observed),
  P(\|Δ\| ≤ observed), …). T_obs is that score for 1178 BC under the B&M
  reading. The statistic is P(T_best ≥ T_obs) over epics.

**The specificity stratum.** Epics whose p_c lies within a factor 2 of the
Odyssey's (B&M reading) form the stratum. If fewer than 200 epics fall in
it, the factor widens to 4 and the report says so.

**Epic gardens.** Each stratum epic gets a garden built with the same fork
types and multiplicities as the Odyssey's rule garden:

- the BM-tier epic garden has the two-offset day-count fork, and 3
  turning-point events × 3 tolerances × 2 visibility settings for one planet
  clue: 36 readings when the epic has those slots, as 𝒢_BM* has;
- the DOC-tier epic garden adds the DOC fork types.

**The calibrated percentile (target first).** Schoch's target was fixed
before any reading. For each stratum epic, r_e = reach_136(16 Apr −1177;
the epic's garden): the chance that this poem, read with the same freedom,
makes Schoch's eclipse new moon the unique match of a window placed at
random around it. r_Ody is the same for the Odyssey under 𝒢_BM*.

- **Conditioning, as in 5.3.** Only epics whose categorical slots hold at
  Schoch's target enter: the season clue holds, and each planet clue's body
  is present in the stated role (a visible morning or evening object, or
  within 6 d of the named kind of event).
- **pct_N4** = the fraction of entering epics with r_e ≥ r_Ody, ties
  counting against the Odyssey. Its interval [pct_N4,lo, pct_N4,hi] is the
  exact Clopper–Pearson 95% interval over the n_stratum entering epics.
  pct_N4 is a tail fraction, the Odyssey's percentile among random poems of
  the same specificity [rev #1 fix 2]. It is not a probability of the same
  kind as G [r1 N10].
- **Ē_N4** = the mean of r_e over the entering epics. This is the analogue
  of G with the poem varied rather than the target. P25 compares it with
  G_BM, and it never enters the rule [r1 N10 fix].

**The eclipse-match strength (survivors first; reported).** For a text with
garden 𝒢 in a window, M = the maximum, over eclipse-compatible readings r,
of h_tot(u_r, ithaki), where u_r is r's unique survivor in the window (0 if
there is none). For each stratum epic, M_e is computed in a window at a
random position, and **p_N4** = the fraction with M_e ≥ M_Ody. If fewer than
20 epics reach it, p_N4 is computed analytically instead: the mean, over
stratum epics, of K_e × p_e(M_Ody), where K_e is the number of distinct
unique survivors across the epic's eclipse-compatible readings. That relies
on N2's independence check [rev #16 fix 4]. The direct count is reported
beside it, with bootstrap intervals.

p_N4 credits the eclipse's rarity. That rarity would be evidence only if the
readings had been formed blind to the eclipse, and the record says they were
not (1.1). p_N4 is reported and enters no rule. Revision 2's ratio LR_sf is
withdrawn with the other likelihood ratios (5.7).

