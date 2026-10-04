### 6.5 Negative controls (outcome 4)

**The clue file** is `data/prereg/negatives.json` as licence-checked twice
(SHA-256 `be4f511e…9c82`) [lcn; lcn2]. It holds 12 clean negatives (Virgil,
Apollonius, Quintus Smyrnaeus, Valerius Flaccus) and the Iliad as a
same-tradition comparison [rev #15 fix 1–2; neg §1]. Each clean negative is
fiction or legend composed long after the events it tells, drafted under the
Odyssey's own selection rules, with no similes and no lying tales. Its
`operational` fields are prose, so each option is translated into a
canonical predicate in `data/prereg/operational_map.json` before the freeze,
and a second agent checks each translation against its prose. Consumers of
the file read the top-level `license_check` block as `round_1` and `round_2`
[lcn2 finding 2].

**Pre-freeze decisions and second reading** [neg §6; lcn §4; lcn2 finding
13]:

- **Counts and caps.** A second reader checks the interval forks and caps
  that rest on the drafter's own counts: ARG-CIUS n16/n17/n18, ARG-COLCHIS
  a3/a4/afree, IL h12/h13/h15, VF-LEMNOS-01, and the caps free30, xfree, w60
  and QS-SACK-06's 10 d.
- **Rows whose day another row's fork sets** [lcn2 finding 5]. ARG-COLCHIS-01
  (the Arcturus storm) takes its night from ARG-COLCHIS-02's option: Night −7
  under a3, −8 under a4, any of −7 to −10 under afree (the row passes if it
  passes on one of them). Under ARG-COLCHIS-02's "none" the storm night is
  unplaced and row 01 is dropped from the reading, as the file says.
  ARG-CIUS-05 takes its night from ARG-CIUS-06's count (n16, n17, n18) in the
  same way. `readings.py` builds such pairs as joint options, so no reading
  pairs a row with a day its link row does not give.
- **"literal" means least inference.** Pinned literal readings that use an
  inferred or drafter-width option are re-pinned by the second reader to the
  least-inference option of their row: AEN-CRETE-01 a60, ARG-RETURN-03 x0,
  ARG-COLCHIS-02 a3, and, after round 2, VF-COLCHIS-01 vis7, whose
  least-inference reading of "serus … vesper" is now "none" [lcn §4.4; lcn2
  finding 13(6)].
- **QS-SACK-03.** Its BM-analogue pin keeps option b in its new meaning (the
  Pleiades over the dark hours), and b-late stays in the garden.
- **Places, landmarks and thresholds.** The same reader checks the place
  identifications against a gazetteer (Pleiades). Round 2 moved Mount Ida
  from AEN-TROY's `observer_places` to a set-level `landmarks` list, because
  the narrative puts no observer there [lcn2 finding 8]. A Day-0 option is
  evaluated at the set's first `observer_places` entry (Troy for AEN-TROY);
  the `ida` rider of AEN-TROY-07 is the bearing from Troy to the landmark. In
  `operational_map.json` the reader flags the numeric thresholds that are the
  drafter's operationalisations [lcn §4.3; 13 rows 34–35].
- **The withdrawn eclipse classes** [r1 N11]. Several rows still cite
  revision 1's classes:
  - QS-SACK-06:a, ARG-RETURN-04:d (round 2) and IL-PATROCLUS-02's solar_am
    and solar_any require "a solar eclipse of class X1–X4 (DESIGN 3.1)";
  - `controls_real.json` cites "X3 ≥ 0.95, X4 ≥ 0.60".

  `operational_map.json` records one decision for all of them. "Class
  X1–X4" means X2 ∪ X3 ∪ X4 under revision 1's own definitions [v1 §3.1].
  In the bench's probabilistic terms that is h_06 ≥ 0.5 or h_tot ≥ 0.5 at
  the option's site and day. X3 and X4 alone map as in 6.3.3.
- **Round 2's new options** [lcn2 findings 3–4]. AEN-TROY-02:iii (the Moon
  below the horizon at the end of evening nautical twilight of Night 0, any
  phase) is a negated `moon_up`, and it is not eclipse-compatible. It comes
  with the pinned reading R-iii (02:iii, 04:a, 05:none, 07:vis7).
  ARG-RETURN-04:d (a solar eclipse of class X1–X4 at the set's first site on
  Day 0, maximum at any time the Sun is up) is a `solar_eclipse` with
  `x_class` X1–X4, mapped as above. Round 2 marked it as the checker's
  inference and stated the case against it (the text calls the darkness
  night, says no star or Moon was seen, and makes it last to dawn).

**The storm rule** (revision 5) [lcn2 finding 13(1)]. A darkness that the
text attributes to a storm (storm clouds, rain or wind, in a storm
narrative) is weather. It is never eclipse-compatible in the rule's gardens.

- **Why.** The drafter already excluded *Aen.* 3.195–204 ("involvere diem
  nimbi") on that ground, and kept out Valerius 1.617 and 1.670 and *Arg.*
  2.1102–1105 [neg §3.1; lcn2 finding 13(1)]. QS-SACK-06:a, Athena's storm
  ("σὺν δʼ ἔχεεν νεφέλας … νὺξ δʼ ἐχύθη περὶ γαῖαν", Quintus 14.461–462),
  was the one storm darkness given a solar-eclipse option. Round 2 found the
  treatment uneven and left the choice to the design.
- **The same rule for the Odyssey.** Theoclymenus' darkness (Od. 20.351–357)
  is a seer's vision with no storm, so the rule does not touch it.
  ARG-RETURN-04's "pall" is not attributed to a storm either, so its
  eclipse option stays. The Iliad's mist at 17.366 is not a storm, and the
  Iliad is reported only.
- **Direction.** The rule removes a reading from fiction, so it works
  against outcome 4, the claim it guards.
- **QS-SACK-06:a** leaves the rule's eclipse-compatible readings. QS-SACK with
  it restored is reported as a sensitivity, scored at its own day and site as
  below.

**Typical-number parity** [lcn2 finding 13(2)]. Outcome 4 compares 𝒢_j with
𝒢_BM*, whose F1b is off, so neither side jitters its stated day counts.
Parity holds for the rule. In the reported comparisons with 𝒢_DOC* and
𝒢_FULL*, where the Odyssey's gardens carry F1b, the negatives'
narrator-stated counts get the same ±2-day and ±3-day jitter: ARG-CIUS-06's
three days and twelve days and nights, IL-PATROCLUS-09's twelfth dawn, and
ARG-RETURN-02's two nights.

**Windows.** Each clean negative is searched in the Odyssey's own two
windows (reproduction, 136 years; primary, 251 years) at its own site. The
negatives tell events of the same legendary age, and these windows give
fiction exactly the chances the Odyssey had. Twenty further random positions
per width are a sensitivity.

**Gardens.** 𝒢_j is the full product of set j's fork options, with each F5
entry expanded into its tolerance and visibility variants [neg §1 item 6].
Its **eclipse-compatible readings** are those that contain an option listed
in the set's `eclipse_compatible_options`, less two kinds:

- lunar-eclipse options, which are not solar eclipses, as the file says;
- storm-darkness options, by the storm rule.

For the clean negatives that leaves AEN-TROY-02:ii-a, AEN-TROY-02:ii-b and
AEN-TROY-05:conj; ARG-RETURN-04:b and ARG-RETURN-04:d; and QS-SACK-02:c. The
negatives' readings were drafted without any target, so their G needs no
conditioning (5.3).

**The test** [rev #1 fix 3]:

- **hit_j** holds when some eclipse-compatible reading of 𝒢_j has, in one of
  the two windows, a unique survivor whose eclipse has h_tot ≥ M_Ody. Each
  option is evaluated at **its own day and its own site** [r1 N11 fix 2]:
  - a Day-0 option (AEN-TROY-02:ii-a, AEN-TROY-05:conj, QS-SACK-02:c,
    ARG-RETURN-04:d) at the set's first `observer_places` entry, on Day 0;
  - an option that places a conjunction within ±k days of Night 0
    (AEN-TROY-02:ii-b, ±1.5 d; ARG-RETURN-04:b, ±2 d) at the same place, on
    the date of that conjunction;
  - in the sensitivity run only, QS-SACK-06:a near Cape Caphereus on Day
    +2..+12.
- **Mapping a survivor to its eclipse** [r2 R2-12; revision 5 generalises
  it]. Every survivor of an eclipse-compatible reading is mapped to the
  conjunction that its eclipse-compatible option names, as F2 (c) and (d)
  map a candidate back in 5.3:
  - for a Day-0 option, the survivor itself;
  - for a ±k-day option, the conjunction within those days of Night 0;
  - for an eclipse option on another day, the conjunction of that eclipse.

  Conjunctions are 29.5 days apart, so there is at most one. Reach is then
  computed on the mapped dates, so hit_j and G_j refer to the same eclipse
  event.
- **G_j** is the mean reach_136, under 𝒢_j, over the set's targets: every
  conjunction in the core that falls in daylight at one or more of the
  set's `observer_places`. Its interval is the interval of 5.3, the wider of
  the gamma and the block-bootstrap intervals. G over the eclipse-compatible
  readings alone is reported beside; the full 𝒢_j can only be larger, which
  works against outcome 4.
- **Outcome 4 fires if some clean negative has hit_j and G_j,hi ≤ G_BM,u.**
  G_BM,u is the Odyssey's G under 𝒢_BM* over T, the same kind of
  unconditioned target set. It is the Odyssey's coincidence as B&M would
  present it, with every reading treated as blind, so the comparison
  favours B&M twice: 𝒢_j holds more readings than 𝒢_BM*, and the negative is
  taken at its upper bound.

Also reported per set:

- the survivors of each pinned reading (literal and BM-analogue; R-i, R-ii,
  R-ii-literal and R-iii for AEN-TROY);
- survivors per century;
- the slot matrix of [neg §5].

**The Iliad** (IL-PATROCLUS) gets the same computations. It is reported as
the same-tradition comparison and is not used in the rule. Two consistency
checks run beside it:

- **Iliad against Odyssey.** If both carry real dates, the Iliad's (the
  tenth year of the war) must fall about 8–12 years before the Odyssey's
  (the return in the twentieth year [win §5]). For the pinned BM-analogue
  readings the bench reports the offset and its base rate: the chance that
  an unrelated survivor falls in a given 5-year band.
- **Cross-text competition.** The bench counts how many texts and readings
  the gardens attach to each eclipse with h_tot ≥ 0.1. 30 Oct 1207 BC and 30
  Sep 1131 BC have also been claimed for Joshua 10 [crit §0 item 7,
  *secondary*]. Joshua is outside the grammar and is not run.

