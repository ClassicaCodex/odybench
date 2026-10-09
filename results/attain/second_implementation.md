# The second implementation of the null side: the two differences, explained

LEAN.md requires that the bench's survivor sets for the T0b reading equal those
of the independent rebuild `results/critique-design-r2/check_gbm.py`, and that
every difference be explained before the verdict is read. Written 2026-10-09,
after `attain.py` (target masked) and before freeze 2.

Both implementations find 11 survivors of the T0b reading over the background.
Ten are shared. One date is in each set only:

| Day 0 | C | Venus lead (bench / check) | Mercury Δ from the MWRA vertex (bench / check) | tolerance | in |
|---|---|---|---|---|---|
| 27 Mar 1624 BC (−1623) | both pass | 124.07 / 124.07 min | **1.478 / 1.504 d** | 1.5 d | bench only |
| 31 Mar 585 BC (−584) | both pass | 114.25 / 114.25 min | **1.502 / 1.492 d** | 1.5 d | check only |

Both differences are the same thing. The candidate sits on the edge of the
continuous ±1.5-day Mercury tolerance, and the two codes place the vertex of
Mercury's rise-azimuth maximum 0.01–0.03 d apart. `check_gbm.py` finds rise
times on a 3-minute grid. The bench bisects them to 0.055 s (DESIGN 3.2, 4.3).
A parabola vertex fitted to azimuths that are each off by up to 1.5 minutes of
rise time moves by about that much. The bench's value is the more precise one.
Venus leads agree to 0.0004 min, and C agrees.

Neither date is near the target. G_BM(v1) differs by 0.0013 between the
implementations (bench 0.1463, check 0.1450), against LEAN.md's explanation
threshold of 0.01.

Conclusion: the difference is a tie-band effect of the reference's coarser
rise grid, not an error in either implementation. The bench's values stand.
