
<!-- APPENDIX-T: everything below this line is truth-side. tools/public_design.py cuts the file here; build agents of the public tier never see it (10.1). -->

## Appendix T. Truth-side facts (withheld from build agents)

Each item below was measured at a control's accepted date, or depends on
one. Section 2 says what these facts imply in aggregate; the facts
themselves are kept here so that the agents who translate and search the
control files (the public tier of 10.1) never read them.
`tools/public_design.py` removes everything from the marker line above to
the end of the file, and I13(h) checks the copy.

### T1. The *Almagest* records at the true dates

Measured against DE441 with the true dates [alm §0, §4, Tables 2–6]:

- **Mercury**, 14 records put at or about greatest elongation, offsets from
  the true greatest elongation (record minus event, days) [alm Table 2]:
  - sorted by size: IX.9.3 0.1, IX.9.4 0.2 (printed), IX.7.7 0.8, IX.7.4
    1.1, IX.7.12 1.1, IX.8.4 1.6, IX.7.16 1.8, IX.7.14 2.7, IX.7.15 2.9,
    IX.7.11 3.3 (emended), IX.8.3 3.4, IX.7.9 3.6, IX.7.6 4.2, IX.7.5 5.5;
  - so 3/14 lie within 1 d, 7/14 within 2 d, 12/14 within 4 d and all 14
    within 5.5 d;
  - the elongation stays within 0.5° of its maximum for 5–10 days.
- **Venus**, 8 records: X.3.2b 0.6 and X.3.2a 1.9 (Ptolemy's pair); X.1.3
  16.1, X.1.6 16.7, X.2.3 17.8, X.1.5 18.3, X.2.4 20.3, X.1.4 20.6. The last
  six lie on a 34–35-day plateau within 1° of the maximum.
- **At B&M's ±1 d**, the true dates satisfy every greatest-elongation clue
  of only 2 of the 9 sets that carry one (ALM-A as printed, ALM-E). ALM-C
  needs 3.4 d, ALM-G 5.5, ALM-H 3.6 (emended) and ALM-K 2.9; ALM-D, F and L
  need 16–21 d.
- **B&M's Mercury proxy is a different event.** For the 7 morning
  greatest-elongation records, the nearest rising-azimuth maximum lies −2.5
  to +31.8 d away, and only 2 lie within ±3 d. Every Venus morning record
  rises 125–220 min before the Sun, so B&M's ≥ 90-min test does not
  discriminate.
- **The other kinds are tight.** Oppositions lie within 1.8 d of the
  true-Sun opposition (0.42 d of the mean-Sun one). Planet–star relations
  lie within 1.7 d, and Moon–planet positions within about 2 h of lunar
  motion; every implied lunar phase is right. IV.6.14's mid-eclipse is
  0.02 h from Ptolemy's time, at umag 0.84 against his 5/6, the north limb
  eclipsed. The III.1.10 equinox is 0.87 d late.
- **The cruxes against the sky.** On the printed date of IX.7.11, DE441
  puts Mercury 3.7° west of the Sun (invisible), and 22.7° east on the
  emended date. For IX.9.4 the printed day lies 0.2 d from the true greatest
  elongation and the emended day 2.8 d [alm §1.4].

### T2. What T1 decides under the frozen regimes of 6.4

Row by row from alm Tables 2 and 5 and the options in
`results/design-revision-r2/alm_options.txt` [me, revision 4; revision 5
checked that its projection changes alter none of it]:

- **Regime SL** sets each greatest-elongation tolerance leave-one-set-out,
  as the largest offset among the records outside the set, rounded up to the
  next whole day [r2 R2-9]:
  - Mercury, 6 d for every counted set except ALM-G: 5.5 d (IX.7.5) rounds
    up to 6;
  - Mercury in ALM-G, 5 d: its own IX.7.5 is the 5.5-d record, and the next
    largest is IX.7.6 at 4.2 d;
  - Venus, 21 d for every set: X.1.4, in no set, is the 20.6-d record.

  The true date is retained in **9 of the 11 counted sets**. Two fail:
  - **ALM-G**, because IX.7.5 lies 5.5 d from the maximum, against ALM-G's
    own tolerance of 5 d;
  - **ALM-H**, at its primary, printed crux: on that date Mercury set 12 min
    before the Sun, so `visible_only` fails.

  Revision 5's projection sets A.10 and B.5 to "none" and uses the
  unbounded `same_apparition` options for A.1, B.1, I.1 and J.4. Both
  changes only loosen rows that the truth passes, so no retained truth is
  lost, and neither failure depends on them.
- **Regime BM** (B&M's option rule, at 1.5 d and 90 min): the true date can
  pass in at most 5 counted sets (ALM-B, E, I, J and L):
  - the MWRA proxy fails every morning Mercury row that offers it, in ALM-A,
    G, H and K (nearest maxima +15.7, +6.2, −2.5, +29.5 and +31.8 d);
  - ALM-D and ALM-F each fail a Venus greatest-elongation row (16.1 and
    20.3 d).

  So rec_ALM_BM ≤ 5 < 6, and Q_BM holds whatever the narrowing.

### T3. The real eclipse records at the accepted dates

From the drafter's rough post-freeze check (its own lunar model, not the
bench's; I4 has not run), as the drafting stage reported it [pcr §5; the
truth file; the drafting stage's summary relayed to the design stage]:

- **Primary readings the accepted dates fail:**
  - R-PTOL-BAB: two magnitudes, E2 about 0.11 against the record's 3 digits
    (0.25), and E3 about 0.49 against "more than half";
  - R-PTOL-ALEX: H3's mid-time, 0.64 h from Ptolemy's +4 h, so R-PTOL-CHAIN
    fails too;
  - R-PYDNA: the season and the Moon's altitude. The accepted eclipse, 21 Jun
    168 BC (−167), fell about 5 days *before* the solstice (26 Jun, the
    drafter's computation), so Livy's "after the solstice" is wrong; and the
    Moon rose already eclipsed.
- **All primaries pass** for R-THUC, R-XEN, R-ARBELA and R-DIOD, and for the
  four H-LIVY notices; Livy 38.36.4 passes only through the ±1 h allowed for
  "ferme" (its maximum falls in seasonal day hour 2.41).
- **T2-SEASON.** The accepted date (21 Mar 424 BC, −423) has the Sun at
  355.3°, so only the primary "early" [330°, 60°] admits it; the half-year
  [0°, 180°] fails [r1 N5].
- **T-INT-12.** At the truth the interval is 6.63 years against the stated
  7, near the edge of its ±0.5-year tolerance [r1 N5].
- The E2 and E3 magnitude failures are model-dependent (E3 borderline at
  0.49 against 0.5) and are rechecked by the bench's own lunar module after
  I4.

### T4. The controls in the data behind SMH's ΔT fits

- SMH's Table S10 v2020 of untimed total and annular eclipses lists −309
  "Greek", 13,300–17,160 s, and −187 "Europe", 12,590–12,900 s
  [`data/ref/Table-S10.2020.txt`]. By year and region these are R-DIOD's
  eclipse and H-LIVY's L4 [r1 N4].
- SMH2016 §2b(iv) used Thucydides' 431 BC and Agesilaus' 394 BC eclipses to
  limit ΔT [r1, from a WebFetch summary of the PMC text, *secondary*]. These
  are R-THUC's T1 and R-XEN's X3.
- The S10 interval for −309 is 3,860 s wide, so R-DIOD's pass is probably
  robust. Q_ΔT tests that rather than assuming it (6.3.3).

### T5. Date slips in the truth sources

[pcr problems; the drafting stage's summary]

- Gautschy's "424 BC May 21" for Thuc. 4.52 is apparently a slip for 21 Mar
  424 BC (−423), which the drafter confirmed by computation.
- NASA's "−0412 Aug 28" for Thuc. 7.50 is the TD date of greatest eclipse;
  the local date is the evening of 27 Aug 413 BC (−412).

### T6. The per-set expectations behind R8, R10 and P20

- **R8:** the three counted sets whose accepted dates fail a primary row are
  R-PTOL-BAB, R-PTOL-ALEX and R-PYDNA (T3).
- **R10:** the two counted *Almagest* sets whose truth is not in B under
  regime SL are ALM-G and ALM-H (T2).
- **P20:** seen in the primary run: R-PTOL-BAB, R-PTOL-ALEX, R-ARBELA and
  R-DIOD; not seen: R-THUC, R-XEN and R-PYDNA.

### T7. The data coverage of the control windows

A 136-year window with the anchor at a uniformly random position spans at
most 136 years either side of the anchor [me, from the anchor dates]:

- PC-R windows fall within −856..+272 (the Babylonian triple of −720 to the
  Hadrianic eclipses of +136);
- *Almagest* windows fall within −407..+277 (anchors from −271 to +141).
