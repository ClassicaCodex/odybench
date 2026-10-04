- **Q_exch, a qualifier on label 1** [r2v6 N9]. Label 1 rests on p_H being
  exact, which needs some pool to be exchangeable with the target, an
  eclipse new moon. No gate vetoes label 1, so the checks of that
  exchangeability must say something themselves. Q_exch holds if either of
  these holds, at two-sided Fisher p ≤ 0.05:
  - **P10's held-out part fails**: H3 or H4 passes at different rates on
    eclipse new moons (a solar eclipse anywhere at the conjunction) and on
    the other spring new moons (5.2);
  - **H3 or H4 drifts inside the epoch band**: its rate differs between the
    band's early half (−1877..−1178) and its late half (−1177..−477), in
    P_BM,E or in P_MWRA,E.

  Both are null-side: `attain.py` computes them with the target masked, and
  they are known at the second freeze. Q_exch is printed beside label 1 and
  in every verdict, and it does not block label 1, for two reasons. Six
  tests at 0.05 fire together by chance with probability up to about 0.26
  even when every pool is exchangeable, so a block would veto a valid exact
  test far too often. And the band is centred on the target, so a linear
  drift inside it cancels in the pool's mean rate. At the design stage no
  test reaches 0.05 (2.9), so Q_exch is not expected (R29).
