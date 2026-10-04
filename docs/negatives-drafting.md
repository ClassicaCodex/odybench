# Negative controls: drafting notes

Written 2026-10-04 for `data/prereg/negatives.json`. It replaces the negative
controls NC1–NC3 of DESIGN §4.4, which critique-design issue 15 found mis-built.
NC4 (Hymn to Hermes) and NC5 (Hesiod) are not redrafted here; the critique moves
them to the instrument checks.

**What the file holds.**
- 13 clue sets, 70 clue rows and 34 excluded rows.
- 12 sets are clean negatives: fiction or legend composed long after the events it
  tells, from Virgil, Apollonius, Quintus Smyrnaeus and Valerius Flaccus.
- 1 set is the Iliad. It is rebuilt as a **same-tradition comparison**, not a
  negative.
- There is no truth file, because these texts have no true date. In its place,
  each set records which of the Odyssey's clue slots it fills (§5).

**Tags.**
- [text: file key]: a row of `data/text/`.
- [txt §n], [DESIGN §n], [crit-design #n]: `docs/research-textclues.md`,
  `DESIGN.md` and `docs/critique-design.md`.
- [me]: my own reading or arithmetic. [me: script] names the script, which is in
  `results/negatives/`.

Dates are historical BC with the astronomical year after them, proleptic Julian.
No date of any kind is in the clue file. A leak check in the builder refuses BC/AD
years, astronomical years and month names.

---

## 1. Rules applied

These are the Odyssey's selection rules [txt §0, §4; DESIGN §5 H10], as restated
for this task.

1. **Who may speak.** A clue is a statement by the narrator or by a character
   speaking in the story.
   - Embedded true narratives count as character speech: Aeneas to Dido in
     *Aeneid* 2–3, and Achaemenides. This is the Odyssey's level E. Each row's
     notes say so.
   - Similes and lying tales are excluded as date carriers. Each excluded line
     is listed in `excluded_rows` with its reason.
   - Disguised deceivers count as lying tales: Sinon, Fama, and Iris disguised as
     Beroe.
2. **Only what the words state.** A time of day, season, phase, site, magnitude
   or interval that the words do not state is not a clue.
   - When I judged a feature implied, it enters as a fork option. The option
     spells out the inference and sits beside an explicit `none`.
   - Thresholds the words do not give are marked as the drafter's, in the
     option's justification. Examples: "≥ 0.5 lit", "±15 days", "5° altitude".
3. **Intervals.** An interval enters only when the text gives it.
   - Where a step has no count, the interval row carries a fork with a bound I
     chose, and says so: `free30`, `xfree`, `w60`, and VF-LEMNOS-01 `b`.
   - A single year interval is stated between two sets: *Aen.* 1.755–756, Dido's
     "seventh summer". It is entered as AEN-CARTHAGE-07.
4. **Sites.** Each site is a place the narrative names, quoted with its words.
   - The coordinates are my identification of that place. They come from the
     Wikipedia API, fetched 2026-10-04 and saved in
     `results/negatives/coords*.out.json`.
   - Where the text names a region but no point, the file says so. This applies
     to Crete for Pergamea, the Libyan coast for ARG-RETURN's Day E, and the open
     sea for VF-LEMNOS.
   - Two identifications are modern and are flagged in the file: the Island of
     Ares as Giresun Island, and Salmonis as Cape Sideros.
5. **Windows.** Each set gives widths only: 136 and 251 years, the reproduction
   and primary windows [DESIGN §3.1]. No set carries a position.
6. **Fork menus.**
   - The morning star uses DESIGN F4: lead ≥ 60, 90 or 120 min, visible at
     arcus visionis 7°, any bright herald, or none.
   - Hermes = Mercury uses DESIGN F5: MWRA, greatest western elongation, morning
     station, any of the three, or first visibility; tolerance 1–3 days; with or
     without visibility; or none.
   - So each set's garden is built from the same fork types as the Odyssey's.
   - The evening star uses the mirror image of F4.
   - The fork-product counts the builder prints count option entries only. Each
     F5 entry stands for its 6 tolerance-and-visibility variants, as in DESIGN.
7. **Pinned readings.** Every set has two pinned readings:
   - `literal`: the least-inference option for each clue;
   - `BM-analogue`: what a B&M-style reader would pick. That means a conjunction
     anchor where any fork allows one, Venus lead ≥ 90 min, MWRA ±1 day, and
     season stars recomputed.

   AEN-TROY instead has `R-i`, `R-ii`, `R-ii-literal` and `BM-analogue`, as §3.1
   explains. IL-PATROCLUS adds an `eclipse-reading`.

**How the lines were found.**
- I searched every local text for sky vocabulary with
  `results/negatives/tx.py`, then read each episode in full.
  - Greek: σελήνη/μήνη, ἀστήρ/ἄστρα, ἑωσφόρος, ἕσπερος, Ὠρίων, Πληιάδες, Ἀρκτοῦρος,
    Ἑλίκη, Σείριος, νύξ/ἠώς, and the day-count words.
  - Latin: luna, sidus, Lucifer, Eous, Vesper, Orion, Pleiad, Arctos, Sirius,
    and so on.
- I exported the Iliad scholia (EditionId 3805) read-only with
  `py -m odybench.ccx export 3805 data/text/scholia-iliad-grc.tsv` (30,391 rows).
  No other library access was made.
- `results/negatives/build_negatives.py` holds the clue data.
  - It finds each licence-words fragment in the cited rows, matching without
    diacritics, and copies the exact original characters into the JSON.
  - It fails on a missing fragment or ref, an invalid pinned option, or a date
    leak.
  - Every fragment in the file was found.

---

## 2. Summary of the sets

"Eclipse-compatible" lists the options that put a conjunction or an eclipse into
a reading. These are the readings by which the critique's definition of "dates
fiction" could fire [crit-design #1, fix 3].

| set | text, lines | Day 0 (anchor) | operational clues | named site | eclipse-compatible |
|---|---|---|---|---|---|
| AEN-TROY | *Aen.* 2.248–2.802 | the festal day; Night 0 = the sack | Moon (2.255, two readings), Moon (2.340), Lucifer over Ida (Dawn +1), festal day | Troy; Tenedos; Ida | 2.255 reading ii; festal day as new moon |
| AEN-CRETE | *Aen.* 3.121–3.152 | the Penates' vision night | full Moon; Sirius season (unlinked) | Crete (Pergamea) | none |
| AEN-ITALY | *Aen.* 3.506–3.524 | Palinurus' night | Arcturus, Hyades, Bears and Orion before midnight | Ceraunian mountains | none |
| AEN-ETNA | *Aen.* 3.568–3.654 | arrival under Etna | Moon at the dead of night; "primo Eoo" (Dawn +1); "tertia lunae cornua" (Day +1) | the Cyclopes' shore by Etna | none |
| AEN-CARTHAGE | *Aen.* 4.238–4.587, 1.755–756 | the departure night | Mercury's descent (Day M1, unlinked by count), winter, Mercury in a dream (Night 0); year link to AEN-TROY | Carthage | none |
| ARG-CIUS | *Arg.* 1.1015–1.1283 | arrival at Cius | full Moon (Night 0), morning star (Dawn +1), halcyon (Night −2), dark night at Cyzicus (Night −17 ± 1) | Cius; Cyzicus | none |
| ARG-COLCHIS | *Arg.* 2.1097–4.183 | the ordeal day | Arcturus' "wet path" (Night −7), Orion nocturne (Night −3), the Bear at midnight (Night −1), moonrise during the flight (Night 0) | the Phasis; Island of Ares | none |
| ARG-RETURN | *Arg.* 4.1620–4.1718 | departure from Crete | evening star (Day −3 − x), the "pall" night without stars or moon (Night 0) | Cretan sea; Anaphe | moonless night as conjunction; lunar eclipse |
| QS-SACK | QS 12.345–14.470 | the day the horse is found | stars hidden under a cloudless sky (Night 0), Electra's withdrawal from the Pleiades, storm darkness (≥ Day +2) | Troy; Tenedos; Caphereus | Day 0 as conjunction; lunar eclipse; solar eclipse at Caphereus |
| VF-LEMNOS | VF 1.310–2.79, 2.357–372 | first day at sea | horned Moon at nightfall, Orion and Perseus setting (Night 0), a Pleiad at dawn (Dawn +1), the Pleiad's storm and a fourth-day Moon (Day L, unstated) | Pallene–Athos–Lemnos | none |
| VF-CYZICUS | VF 3.1–3.258 | departure from Cyzicus | Moon shining in the night battle | Cyzicus | none |
| VF-COLCHIS | VF 7.1–7.23 | Medea's evening | evening star (Day 0), "eous" (Dawn +1) | Colchis | none |
| IL-PATROCLUS | *Il.* 11.1–24.695 | the day Patroclus dies | three darknesses (Day 0), the Shield's stars and full Moon (Night 0), Heosphoros (Dawn +3), Hermes' journey (Day +12 to +15) | Troy plain and camp | conjunction; solar eclipse before noon, after noon, or near sunset |

---

## 3. Notes by text

### 3.1 Virgil, *Aeneid*

**2.255 has two readings, and the file pins both** [crit-design #15].

- **Reading i: the Moon is up.** It has two variants:
  - `i-a`, with the "at least half lit" threshold DESIGN NC2 added;
  - `i-b`, without it.

  The words "tacitae per amica silentia lunae" state no phase [text: virgil-aeneid-lat 2.255].
- **Reading ii: *silens luna* is the Moon at conjunction.** Pliny says the day
  of coitus is called by some *interlunium*, by others the day "silentis lunae"
  [text: pliny-nh-lat 16.39.2 = *NH* 16.190].
  - The same usage recurs twice in the local Pliny: once against "plena"
    [text: pliny-nh-lat 18.31.3], once beside eclipses [text: pliny-nh-lat 28.7.3].
  - Reading ii has two variants: conjunction on Day 0 (`ii-a`), or within ±1.5
    days (`ii-b`, the days of invisibility).
- Servius' note on the line is not in the library and was not read.

**A finding DESIGN did not have: 2.340 conflicts with reading ii.** Four Trojans
join Aeneas "oblati per lunam", met by moonlight, during the same night
[text: virgil-aeneid-lat 2.340].
- A Moon at conjunction is not up at night.
- Reading ii therefore makes the night's own clues contradict each other, unless
  2.340 is read as "by night". The night is "nox atra" at 2.360 and "caeca" at
  2.397.
- Three readings are pinned for this:
  - `R-i`: the Moon is up, so 2.340 holds.
  - `R-ii`: conjunction, with 2.340 dropped.
  - `R-ii-literal`: conjunction, with 2.340 kept. This reading is
    self-contradictory and should return no survivors, as NC4 was built to do.
- The critique expected reading ii to make NC2 "Odyssey-shaped". That holds only
  if one of the night's two lunar lines is read away [me].

**Lucifer rises over Ida at 2.801.** The words "iugis summae surgebat Lucifer
Idae" place the rising over the Ida ridges, as seen from the mound of Ceres
outside Troy (2.742).
- The summit lies at a bearing of 119° from Hisarlık, 58 km away
  [me: great-circle bearing from the Wikipedia coordinates of Troy, 39.9575 N
  26.2389 E, and Mount Ida, 39.70 N 26.833 E].
- At 40° N, Venus rises at that azimuth only at a declination near −22°
  [me: sin δ = cos A cos φ, geometric].
- This rider (`ida`) is my geography, not the text. Its tolerance (±15° or ±30°)
  is mine.

**The festal day (2.248–249)** answers to Apollo's feast on the Odyssey's Day 0.
- The `conj` option copies B&M's step from feast to new moon [txt §5.3].
- No source ties the Trojans' celebration to the Moon, so `none` is the literal
  reading.

**Book 3 has no day count back to the night of Troy.**
- The departure "as summer had scarcely begun" (3.8) and the wintering at Actium
  (3.284–285) have no stated interval to anything else. They are excluded.
- That leaves three self-contained episodes:
  - **AEN-CRETE**: the dog-star plague and the full Moon of the Penates' vision.
  - **AEN-ITALY**: Palinurus' star list.
  - **AEN-ETNA**: the cloud-held Moon, "primo Eoo", and Achaemenides' "third
    moon".
- The storm of three sunless days and starless nights (3.195–204) is excluded.
  The text gives storm cloud as the cause ("involvere diem nimbi").

**Two formulas in book 3 matter for the analogy.**
- 3.516 "Arcturum pluviasque Hyadas geminosque Triones" repeats 1.744 (Iopas'
  song) word for word [text: virgil-aeneid-lat 1.744, 3.516]. So Palinurus' star
  list stands to the *Aeneid* as Od. 5.273–275 stands to Il. 18.487–489
  [txt §5.8]: a catalogue line reused, attached to a steersman.
- 3.589 repeats 4.7 [text: virgil-aeneid-lat 3.589, 4.7]: the dawn after "primo
  Eoo" is a dawn formula.

**AEN-CARTHAGE goes beyond the books the task named.** I added it for two
reasons.
- **The Hermes slot.** *Aen.* 4.238–258 is Virgil's rewriting of Od. 5.43–54:
  talaria, the wand, and a bird skimming low over the sea.
  - It is the only clean negative in which B&M's Hermes = Mercury rule can be
    applied to a Hermes journey modelled on the Odyssey's.
  - Its interval to the departure night is not stated. Only a drafter's bound
    (`free30`) links it.
- **The year link.** Dido's "septima ... aestas" (1.755–756) links it to
  AEN-TROY by a stated year count.
  - The poem repeats "the seventh summer" a year later, in Iris' disguised
    speech (5.626). That line is excluded as a lying tale, and its contradiction
    is the `none` justification.

### 3.2 Apollonius, *Argonautica*

**DESIGN NC3 took its season from a simile.** 1.1201–1204 ("ὡς δ' ὅταν ...
χειμερίη ... δύσις ... Ὠρίωνος") is a simile and is now excluded, as the critique
found.

**NC3 also missed the full Moon at Cius.** Hylas is caught by the nymph because
"the mid-month Moon, shining from the sky, struck him"
[text: apollonius-argonautica-grc 1.1231–1232: "διχόμηνις ἀπ' αἰθέρος αὐγάζουσα βάλλε σεληναίη"].
- This happens in the early night: he is fetching water "for supper"
  (ποτιδόρπιον, 1.1209).
- At the end of the same night the dawn star rises over the peaks
  (1.1273–1274). Its verb ὑπερέσχεθεν echoes Od. 13.93 ὑπερέσχε.
- So ARG-CIUS has a Day-0 phase and a Dawn +1 morning star. But its phase is the
  opposite of the Odyssey's: a full Moon, not a conjunction.

**ARG-CIUS runs back 16–18 nights to the night battle at Cyzicus.** The chain,
from 1.1015–1152, is three days of mourning, twelve days and nights of storm,
the halcyon on the following night, the sacrifice on Dindymon, and departure.
- The three counts n16, n17 and n18 are forks [me: count]. The halcyon night is
  Night −2 in all three.
- **The battle night.** Apollonius says only that the Doliones did not recognise
  the heroes "ὑπὸ νυκτί". A moonless night is therefore a fork, not a clue.
- **The halcyon** brings in a season only through ancient bird lore.
  - Pliny gives halcyon days of 7 days either side of the winter solstice, and
    says the bird is seen only at the Pleiades' setting and the solstices
    [text: pliny-nh-lat 10.32.1; 18.26.1].
  - This is the same kind of step as reading the Odyssey's feast as a new moon
    through a scholion. It is entered as a fork, with `none` as the literal
    reading.

**ARG-COLCHIS gives a 7–8-night chain with four sky statements** (2.1097 to
4.183):
- "ὕδατι σημαίνων διερὴν ὁδὸν Ἀρκτούροιο" (2.1099), Arcturus' wet path. The
  phase is unnamed, so morning setting, heliacal rising and evening setting are
  all forks.
- the nocturne in which sailors look to Helice and Orion (3.744–746), a generic
  scene;
- the leaning Bear at Jason's midnight sacrifice (3.1195–1196);
- the Moon "newly rising from the horizon" as Medea flees (4.54–55).
  - Read literally this is a moonrise inside the night, so a waning Moon.
  - Option `b` (moonrise after midnight) is my inference from the events that
    still fill the night before dawn (4.109–113, 4.183).
- The count from the Ares storm to arrival at the Phasis has a one-day fork, a3
  or a4. The heroes "kept cutting forward" (2.1244) with no count given.

**ARG-RETURN.** The "fold-star" at sunset (4.1629–1630) is an evening star.
- Four nights to an unstated number later comes the κατουλάς: "neither stars
  nor moonbeams" (4.1694–1698).
- The crossing from Carpathos to Crete has no count, hence the fork `x0` /
  `xfree`.
- The night lacks stars as well as Moon. So the moonless reading (`a`, H2's
  predicate) is a reading, not the text's explanation. Of the options, it is the
  closest analogue to the Odyssey's σκοτομήνιος, which also comes with rain all
  night (Od. 14.457).
- **Excluded: the poem's only eclipse is a simile.** 4.1286–1287 describes the
  Sun bringing night at midday with the stars shining. It is excluded as a
  simile, like everything else in that form.

### 3.3 Quintus Smyrnaeus, *Posthomerica* 12–14

The thinnest set. Books 12–14 have no lunar statement, no morning star and no
Hermes [me: search for σελη-, μηνη-, ἑωσφόρ-, ἕσπερ- and ἀστήρ across all 14 books;
the only hits are in books 1, 2, 5, 6, 8 and 10, and 6.257 is the Hesperides. Hermes
(Ἑρμει-, Ἑρμη-, ἀργειφ-) appears only at 3.699 and 10.189].

What remains:
- **The prodigies of Night 0.** Mist covers all the stars over the city
  "although the shining sky was cloudless" (12.514–516), among bleeding altars,
  weeping statues and self-opening gates. Its forks are a lunar eclipse, a bright
  Moon, or a conjunction anchor, all of them inferences; `none` is literal.
- **Electra's withdrawal from the Pleiades during the sack** (13.551–557).
  - This is told as hearsay (φασι) and made permanent (αἰέν).
  - The Iliad scholia tell the same aetiology and assign it to the Cyclic poets
    [text: scholia-iliad-grc key 2.18.198.1]. It is inherited story, not a sky.
- **Athena's storm** (14.461–462), on an unstated day of the voyage home. The
  text names its clouds.

The Athena dream night (12.104–105) is excluded. It is separated from Day 0 by
the three days of building (12.147) and an unstated gap.

### 3.4 Valerius Flaccus, *Argonautica*

**Both lunar statements in VF-LEMNOS render Aratus' weather signs.**
- The clear Moon "nec gravido ... cornu" at nightfall (2.56) is Aratus' thin,
  clean third-day Moon, which means fair weather.
- The Moon "quarto densam ... ortu" at Lemnos (2.367) is his thick fourth-day
  Moon, which means rain [text: aratus-phaenomena-grc 783–787].
- So the literal operational reading is a young crescent, a few days after
  conjunction. The `none` option names the source.

**The star statements of the first night pull in different directions.**
- **Tiphys' "tantus Orion iam cadit, ... iam stridet in aequore Perseus"**
  (2.62–63) is ambiguous:
  - setting at nightfall points to spring;
  - "the season of Orion's setting" points to late autumn.
- **"sub Eoae dubios Atlantidis ignes"** at dawn (2.72) has two readings:
  - a Pleiad's first dawn appearance;
  - the Pleiades' dawn setting, which is Virgil's usage of "Eoae Atlantides"
    [text: virgil-georgics-lat 1.221].
- **The Lemnos storm** "Pliada ... nimboso moverat astro" (2.357) is the stormy
  Pleiad setting.
- The forks carry all these readings. Some combinations are probably impossible.
  - A strict spring reading of 2.62 cannot go with a dawn setting of the
    Pleiades.
  - The bench will find out which [me: not computed].

**VF-CYZICUS is VF's version of the night Apollonius left dark.** Here the Moon
shines out "piceo ... polo" to save Erymus (3.195–196). The same episode is
moonlit in one poet and unlit in the other.

**VF-COLCHIS (7.1–23) has two literal planet statements.** Medea is parted from
Jason by the "serus ... vesper" and sees her threshold whiten "tenui ... eoo".
Read literally, Venus would be the evening star and then the next morning's
morning star. That is possible only near inferior conjunction. The literal
pinned reading may have no survivors [me].

### 3.5 Iliad: NC1 rebuilt as a same-tradition comparison

The Iliad shares the Odyssey's tradition and diction, and DESIGN itself tests
whether its date agrees with the Odyssey's. So it cannot be a negative
[crit-design #15]. It is kept because it fills every Odyssey slot in the same
diction. That measures what B&M's reading does to the Odyssey's own tradition.

**Day counts** [text: iliad-grc]:
- Day 0 runs from 11.1 to 18.241. Books 11–18 are one day.
- Hector dies on Day +1.
- Dawn +2 comes at 23.109.
- The pyre burns through Night +2 (23.217–218).
- Heosphoros rises at Dawn +3 (23.226–228). This matches the three days DESIGN
  NC1 attributes to Papamarinopoulos et al. 2014 [crit §5].
- Day H, Priam's journey, is "the twelfth dawn" from Hector's death. The narrator
  gives it at 24.31, and Hermes in disguise repeats it at 24.413–414.
  - The scholion counts the death day as the first: wood-cutting, then the games
    as the third day, then nine [text: scholia-iliad-grc key 4.24.22.1].
  - That gives the fork h12/h13, plus a minority h15.

**The darkness lines.** These are what DESIGN called the eclipse slot.
- **16.567.** Zeus' "deadly night" falls before the noon line 16.777. The
  scholia gloss it as murk, σκότον, citing Od. 5.294
  [text: scholia-iliad-grc key 6.16.341.1].
- **17.366–368.** "You would not have said the Sun or the Moon was safe." This
  comes after 16.779's afternoon, and an ancient scholiast already says one would
  have taken it for an eclipse [text: scholia-iliad-grc key 6.17.183.1].
  - But the text itself confines the darkness to mist over the best fighters.
    The rest fought "ὑπ' αἰθέρι" in bright sun, with no cloud on land or
    mountain (17.370–373).
  - Another scholion makes the same point: not over the whole battle
    [key 2.17.136.1].
  - Zeus then scatters the mist and the Sun shines out (17.649–650).
- **18.239–241.** Hera's early sunset. The scholia call it wholly mythical and
  compare Od. 23.243 [keys 4.18.84.1, 6.18.109.1].
- Two darkness episodes on one day, one before noon and one after, cannot both
  be one eclipse. The forks carry both, and the garden will show which one any
  surviving reading uses [me].

**The Shield (18.483–489).** On the Shield, Hephaestus puts "σελήνην τε
πλήθουσαν", which the scholia gloss as πανσέληνον [key 2.18.196.1], and the
star catalogue. It is entered as a season fork, as DESIGN asked.
- Read as the sky of Night 0: co-visibility of the named stars.
- Read through Hes. WD 615–616: the setting of the Pleiades, Hyades and Orion
  marks the ploughing season [text: hesiod-worksdays-grc 615–616].
- A full Moon on Night 0 contradicts every conjunction option of the darkness
  rows. The garden carries both.

**The Hermes slot was added.** 24.339–345 is the seven-line passage that Od.
5.43–49 repeats verbatim [txt §5.9].
- Hermes reaches the Hellespont at dusk (24.351) and leaves for Olympus as Dawn
  spreads (24.694–695).
- Under B&M's rule this is a Mercury slot, 12–15 days after the darkness day. In
  the Odyssey it falls 34 days before the anchor.

**Kept out of the clue file.** The published Iliad datings appear only here, never
in `negatives.json`:
- Papamarinopoulos et al. 2014: 6 Jun 1218 BC (−1217) [crit §5, read];
- Henriksson 2012: 24 Jun 1312 BC (−1311) [crit §5, *secondary*].

The ninth-to-tenth-year statements (Il. 2.295, 2.328–329) are noted as the link
DESIGN §4.4's Iliad-against-Odyssey check uses. No position is recorded.

DESIGN's Troy coordinates were "from memory, to be checked". Wikipedia gives
39.9575 N 26.2389 E, which agrees with them to 0.01°.

---

## 4. What changed against DESIGN §4.4

| DESIGN | problem | now |
|---|---|---|
| NC1 counted as a negative | same tradition [crit-design #15] | IL-PATROCLUS, role "same-tradition comparison"; Hermes slot and day counts added |
| NC1 "Day D a new moon" | not in the text | a fork (`conj`) on the darkness row, with `none` |
| NC2 "Moon up and at least half lit" | "half lit" is not in the words; reading ii missing | 2.255 forked i-a / i-b / ii-a / ii-b / none; Pliny cited; 2.340 found and its conflict with reading ii pinned |
| NC2 "Venus morning star on Day +1" | right | kept as F4; Ida azimuth rider added as a fork |
| NC3 season from 1.1202 | simile | excluded |
| NC3 "Venus morning star at Day +1" | right, but the full Moon of the same night (1.1231) was missing | ARG-CIUS with both |
| NC3 "moonless night" 4.1695–1697 | the text hides the stars too | forks a / b / c / none, H2's predicate as `a` |
| (absent) | Quintus, Valerius, more of Virgil | QS-SACK, VF-LEMNOS, VF-CYZICUS, VF-COLCHIS, AEN-CRETE, AEN-ITALY, AEN-ETNA, AEN-CARTHAGE |

---

## 5. Odyssey slots each set fills

The Odyssey's grammar under B&M's reading [DESIGN §1.1; txt §2–4] has five slots:
- **Day-0 phase:** conjunction on Day 0, from the oath 14.161–162.
- **Season stars:** Pleiades and Boötes on Days −29 to −12.
- **Morning star:** Day −5 (13.93–95).
- **Mercury:** Hermes' journey on Day −34.
- **Darkness:** Theoclymenus' vision on Day 0, which B&M did not use as a
  criterion.

Status codes: "text" means the literal reading fills the slot; "fork" means only
a non-literal option does; "–" means empty.

| set | Day-0 phase | season stars | morning star | Mercury | darkness / eclipse |
|---|---|---|---|---|---|
| AEN-TROY | fork (reading ii); literal: a lit Moon | – | text, Dawn +1 | – | – |
| AEN-CRETE | text: full Moon | text, Sirius (unlinked) | – | – | – |
| AEN-ITALY | – | text: Arcturus, Hyades, Bears, Orion (a formula) | – | – | – |
| AEN-ETNA | text: Moon at midnight; waxing on Day +1 | – | fork ("Eoo"), Dawn +1 | – | – (cloud) |
| AEN-CARTHAGE | – | text: winter (rhetorical) | – | text: Mercury's descent (interval unstated); dream on Night 0 | – |
| ARG-CIUS | text: full Moon | fork: halcyon | text, Dawn +1 | – | fork: dark night −17 |
| ARG-COLCHIS | text: moonrise in the night (waning) | text: Arcturus (−7); fork: Orion (−3) | – | – | – |
| ARG-RETURN | text: moonless night | – | evening star instead, Day −3 − x | – | fork: lunar eclipse |
| QS-SACK | fork: conjunction | fork: Pleiad aetiology | – | – | text: prodigy (fork: lunar eclipse); storm (fork: solar) |
| VF-LEMNOS | text: horned Moon (young crescent); fourth-day Moon later | text: Orion/Perseus setting; Pleiad at dawn; Pleiad storm | – | – | – |
| VF-CYZICUS | text: Moon up late in the night | – | – | – | – |
| VF-COLCHIS | – | – | fork ("eoo"), plus an evening star | – | – |
| IL-PATROCLUS | fork: conjunction | fork: the Shield | text, Dawn +3 | fork: Hermes, Day +12 to +15 | text: three darknesses (mist) |

**What the matrix shows** [me]:

1. **No clean negative fills all five slots.**
   - Only the same-tradition Iliad does, and only through forks, which is also
     how the Odyssey fills them [txt §7].
   - Among clean negatives, ARG-CIUS fills four, two of them by fork.
   - AEN-TROY reaches the Odyssey's exact anchor only under reading ii.
2. **The Mercury slot exists in only two places.** The Iliad has it, and so does
   Virgil's imitation of Od. 5. Both are Hermes passages copied from the same
   model. Elsewhere B&M's rule has nothing to attach to. That is a limit on what
   N4's synthetic poets must supply.
3. **The morning star always closes a night of action** (Aen. 2.801, Arg.
   1.1273, Il. 23.226, and as forks Aen. 3.588 and VF 7.22).
   - In four poems (five passages) it comes at the dawn after the night of the
     main event.
   - This supports the reading of Od. 13.93–95 as a narrative time-marker
     [txt §5.7]. It is not evidence about any one dawn's sky.
4. **The poets' Moons are mostly lit.** Where these poems state a phase or a
   presence literally, the Moon is usually up and bright: full at Cius and
   Crete, up at Troy (2.340), at Cyzicus in VF, and under Etna. A dark Moon
   appears literally only in ARG-RETURN, with the stars hidden too. The Day-0
   conjunction the Odyssey's reading needs is everywhere an inference.

---

## 6. Open points

1. **Interval forks rest on my counts and caps.** Each needs a second reader
   before freezing:
   - ARG-CIUS n16/n17/n18;
   - ARG-COLCHIS a3/a4;
   - IL h12/h13/h15;
   - VF-LEMNOS-01 (departure the same day as Night 0, or not);
   - the caps `free30`, `xfree` (10 days), `w60`, and QS-SACK-06's 10 days.
2. **The Iliad's Night 0 assumes the Shield is made on the night of Day 0.** I
   took this from the narrative sequence (18.369–19.3) without checking it line
   by line.
3. **Readings of single words I could not settle from local sources:**
   - Eous (*Aen.* 3.588): the morning star or the dawn?
   - vesper (VF 7.1): the evening star or the evening?
   - ἔκλιθεν (*Arg.* 3.1196): which way does the Bear lean?
   - διχόμηνις (*Arg.* 1.1231): exactly full, or merely bright?

   Ancient commentaries on Virgil (Servius) and Apollonius (the scholia) are not
   in the library.
4. **Site identifications should be checked against a gazetteer such as
   Pleiades.** These are Wikipedia coordinates:
   - Island of Ares = Giresun Island;
   - Salmonis = Cape Sideros;
   - the Cyclopes' shore = Aci Trezza;
   - the ARG-RETURN Day E point = Cyrene.
5. **Not searched in full:**
   - *Aeneid* 5–12. The book 5 Anchises anniversary, a stated one-year interval
     (5.46–50), would link the book 3 Drepanum episode to book 5. It was not
     entered.
   - The day counts of *Argonautica* book 2. Its sky statements were all read.
     The amphilyke at Thynias (2.669–671) is a time-of-day line and was not
     entered.
   - *Valerius* 4–8, scanned for named stars and the Moon only.
6. **What `searchable` means.** Every set is marked searchable, but several are
   season-only or single-clue sets: AEN-ITALY, AEN-CRETE, VF-CYZICUS and
   VF-COLCHIS. They are expected to have many survivors and cannot be unique.
   They are kept so that the "many survivors" expectation is measured, not
   assumed.

---

## 7. Files

- `data/prereg/negatives.json`: the clue file, written by the builder.
  - The top level holds `sets`, `clues` and `excluded_rows`.
  - Each set holds `observer_places` (words, refs, coordinates and their
    source), `window_width_years`, `pinned_readings`, `odyssey_slots` and
    `eclipse_compatible_options`.
- `data/text/scholia-iliad-grc.tsv`: exported read-only, EditionId 3805.
- `results/negatives/`: the scratch work.
  - `build_negatives.py`: the builder.
  - `tx.py`: the text reader.
  - `schol.py`: Iliad scholia lookup.
  - `coords*.py` and their outputs: Wikipedia coordinates.

To rebuild, run `py results/negatives/build_negatives.py` from the project root.
It prints 13 sets, 70 clues and 34 excluded rows.
