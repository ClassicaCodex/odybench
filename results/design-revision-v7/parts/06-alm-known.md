- **Which sets can be narrowed at all** (null side; no truth read)
  [r2v6 N1; r2v6: narrowing_3b.py]. The recheck estimated the share of a
  136-year window's days that pass each counted set's projection in regime
  SL. It used three null windows, starting at −1500, −1100 and −700, which
  hold no control date:
  - ALM-A, D, E, F, G, H and L pass 0.07–4.6% of days, so they can be
    narrowed to 5%;
  - ALM-I, J and K pass 14–19% of days, so **no method can narrow them**;
  - ALM-B passes 5.2% of days if `same_apparition` means only "on that side
    of the Sun", and 4.4% if the planet must also be visible on the day.
    Revision 7 freezes the second meaning (6.4, 10.3), so ALM-B can be
    narrowed, by about 0.6 percentage points on this estimate.

  So **at most 8 of the 11 counted sets can be narrowed**, and gate 3b
  (6 of 11) needs at least 6 of those 8. The estimate is rough: one sample a
  day, events located to the day, and rise leads from the analytic hour
  angle at Alexandria. The bench computes narrowability itself at the
  null-side stage (6.4).
- **At the true dates** (truth-side; the tables are in [AppT 1–2]):
  - the observer slack of a "greatest elongation" record is a few days for
    Mercury and up to three weeks for Venus, and B&M's Mercury proxy (the
    MWRA) is a different event from greatest elongation;
  - in regime SL (6.4) the true date is retained in **9 of the 11 counted
    sets**, under the frozen meaning of `same_apparition` and at every
    rounding step [AppT 2]. How many of those 9 can also be narrowed is in
    [AppT 6]; gate 3b's pass needs at least 6 of them (P21);
  - in regime BM the true date can pass in at most 5 counted sets, so
    **rec_ALM_BM ≤ 5 < 6, and Q_BM holds** whatever the narrowing. It is
    recomputed as a regression check, not predicted [r1 N3].
