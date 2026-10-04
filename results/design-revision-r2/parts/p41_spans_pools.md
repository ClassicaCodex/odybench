### 4.1 Spans and coverage

- **Background** B = −1999-01-01 to +200-12-31 (2,200 Julian years).
  - It starts with the first year of NASA's elements [acq §2.1]. Every
    ephemeris, element and star file needed is already on disk (DE441 and
    DE431 to +241, NASA elements to +300 [acq §1.1, §2.1]).
  - Revision 2's background ended at −600. Its conditioned target pool would
    then hold about 74 targets, and with so few no interval could fall below
    0.05 (2.8) [r1 N8]. Extending the background to +200 nearly doubles the
    pool.
  - **The cost is stationarity.** Precession moves the star season about 31
    days against the equinox over 2,200 years. P13 tests the rates, and 5.3
    reports G on each half of the core.
- **Data margins** −2060..+241, covering the 40-day clue offsets and the
  ±60-day Mercury searches.
- **Target core** −1748..−51. Targets must lie at least 251 years inside B
  so that every window of every width lies inside it. One core serves all
  widths, so gardens of different widths share their targets. The core
  contains 1312, 1178 and 1131 BC.
- **Controls.** PC-R windows fall within −856..+272 and ALM windows within
  −407..+277. DE441 and DE431 are extended to +300 before the controls run
  (11.1).
- **Per-site spans** are in `data/prereg/sites.json` [r1 N12]. Only Ithaki
  needs every column over the whole span. Each negative-control site needs
  the background, but only the columns its sets use. Each control site needs
  only the union of its 21 window positions.

### 4.2 Candidate pools and target pools (Ithaki unless a rule names another site)

**Candidate pools.**

- **P_all** holds every geocentric apparent-longitude conjunction, computed
  with DE431 in yearly chunks and SMH2020 ΔT for UT. Each candidate carries
  **one Day-0 date per clock**: `day0_jdn_ut2` (B&M's clock; F2 (a)) and
  `day0_jdn_lmt` (F2 (b), the negatives, R_anc) [r1 N12].
- **P_day** holds the conjunctions whose instant falls in daylight at the
  site (Sun's centre above −0.8333°). At Ithaca that is 50.9% of them [vis
  §4.2], and only these can give a visible solar eclipse.
- **P_spring** holds the conjunctions passing C_rel (4.5).

**Target pools.** Section 5.3 says which pool each G uses, and why.

| pool | definition | size in the core (estimate, 2.8) |
|---|---|---|
| T | P_day ∩ core | about 10,690 |
| T_C | T ∩ P_spring | about 903 |
| T_A | the targets in T_C whose sky satisfies the Venus slot and the Mercury slot below, on either day count | about 139 (100–179) |

- **The Venus slot.** On Day −5 or Day −4, Venus rises before the Sun, with
  the Sun at or below −7° at Venus' rising (AV 7° [vis §1.2]).
- **The Mercury slot.** On Day −34 or Day −33, Mercury lies within 6.0 d
  (continuous) of a morning rise-azimuth maximum (vertex, 4.3), a greatest
  western elongation, or a station while west of the Sun. Alternatively, it
  is a visible morning object, with the Sun at or below −10° at Mercury's
  rising.

The slots are revision 2's PC-S generator slots, which the recheck measured
[r1 N1], with the parallel count added. The 6-day width is the slack of
Ptolemy's Mercury records (2.6). It defines what "Hermes is Mercury" means
categorically. It is not used to validate anything: gate 3b is calibrated
leave-one-set-out (6.4).

**One identity follows.** Every reading of the rule's B&M garden requires C,
a Venus lead of at least 90 min (which implies the Venus slot) and a morning
Mercury event within 3.5 d (which implies the Mercury slot). So no target
outside T_A is ever reached by it, and

  G(𝒢_BM*, T) = (n_A / n_T) · G(𝒢_BM*, T_A)

exactly. I9 checks this identity in the code, and I14 uses it as a
realisability constraint (9.4).

