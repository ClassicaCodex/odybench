- **Why ±700 years.** It is the band the recheck of revision 5 proposed for
  its sensitivity pool [r1v5 N11]. Revision 6 also called it "the band of
  P8's stationarity test". That was wrong: P8 compares the first and last
  700 years of the background, not a band around the target [r2v6 N10c].
  - **The width was chosen with the narrower band's floor in view.** ±350
    years would leave 24 and 14 members, and P_MWRA,E's floor would then be
    0.067 [me: `results/design-revision-v6/band_counts.py`]. That would make
    outcome 1 unattainable for every target.
  - So the choice kept the test able to say "yes" for some target. It did
    not favour a "yes" for this one, which Q_record already rules out (7.1).
- **With H4 dropped**, the recheck's course (a), H3 alone would have floors
  of 0.208 over the whole background and 0.241 within ±700 years
  [me: `heldout_epochs.out.txt`]. Such a test could not say "yes" for any
  target (7.1).

**Is exchangeability in doubt? The inputs of Q_exch** (revision 7)
[r2v6 N9; me: `results/design-revision-v7/heldout_exch.py`, `.out.txt`,
`.json`]. The script removes the target before it computes anything. It
imports revision 5's rough predicates unchanged, as revision 6's script did.

| test | rows | H3 | H4 |
|---|---|---|---|
| drift inside the band, P_BM,E: −1877..−1178 against −1177..−477 | 25 / 24 | 7/25 against 3/24, Fisher p 0.29 | 0/25 against 2/24, p 0.23 |
| drift inside the band, P_MWRA,E | 15 / 13 | 5/15 against 1/13, p 0.17 | 0/15 against 1/13, p 0.46 |
| P10's held-out part: a solar eclipse anywhere at the conjunction (NASA's catalogue) against none, over every spring candidate | 442 / 1,843 | 67/442 against 240/1,843, p 0.24 | 22/442 against 84/1,843, p 0.71 |
| the same, with eclipses visible at an Ionian site for some ΔT within ±2σ (reported) | 80 / 2,205 | 15/80 against 292/2,205, p 0.18 | 4/80 against 102/2,205, p 0.79 |

- No test reaches 0.05, so **Q_exch is not expected** (R29).
- **Which eclipse class P10 uses.** Revision 6's class was "h_tot > 0 at
  any of the five Ionian sites". Only 3 of the 2,285 spring candidates are
  eclipses that could be total at an Ionian site for some ΔT within ±2σ,
  far too few to test. Neither predicate involves the lunar node, so what
  could break exchangeability is node proximity, the property every solar
  eclipse shares. P10 therefore compares every solar eclipse in NASA's
  catalogue with the other spring new moons, and reports the Ionian-visible
  class beside it (5.2). The new class has more power, so the change can
  only make P10 more likely to fail and Q_exch more likely to hold.
- **The band is symmetric about the target.** A linear drift inside it
  cancels in the pool's mean rate. That is one reason Q_exch qualifies
  label 1 and does not block it (7.2).
