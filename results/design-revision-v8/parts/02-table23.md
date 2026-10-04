**P(total at Ithaki) per ΔT model**, each model's σ taken as Gaussian, in the
canon frame on NASA's elements (SMH values converted by +34 s). Since revision
8 the totality columns integrate the continuous windows above, as
`eclipses.totality_window` hands them to `p_exact` (10.2) [r3v7 R3-3; me:
`results/design-revision-v8/i2c_table.py`]. Revision 7's values, in
parentheses, integrated the first review's 5-s-grid windows [rev #17;
`results/critique-design/check_p19.out.txt`], and the script reproduces them
exactly. P(smag ≥ 0.9) is the first review's, on a 20-s grid
[`check_mag09.out.txt`]; it is not a totality window and not an I2(c)
reference:

| model (value ± σ at −1176.68) | P(total) 1178 BC | P(total) 1131 BC | joint, common offset | P(smag ≥ 0.9) 1178 BC |
|---|---|---|---|---|
| SMH2020 28,543 ± 720 | 0.297 (0.294) | 0.496 (0.494) | 0.051 (0.047) | 0.932 |
| Addendum 2020 parabola 28,282 ± 541 | 0.175 (0.173) | 0.643 (0.641) | 0.056 (0.052) | 0.934 |
| SMH2016 parabola 28,963 ± 541 | 0.503 (0.498) | 0.446 (0.443) | 0.113 (0.108) | 0.997 |
| Espenak–Meeus, canon form 28,589 ± 1,008 | 0.255 (0.252) | 0.414 (0.412) | 0.052 (0.049) | 0.849 |
| **equal-weight mixture of the four** | **0.308** (0.304) | **0.500** (0.498) | **0.068** (0.064) | **0.928** |

[me: means of the rows above.] Unrounded, the mixture's P(total) for 1178 BC
is 0.3076 over the continuous window and 0.3044 over the grid window. **The
0.304 printed by revisions 1–7, and so m̂ (4.4), are grid-window values**
[r3v7 R3-3]. In the DE431 pairing the three SMH values are 0.299, 0.178 and
0.505 [eph §5.4]; with Espenak–Meeus on NASA's elements (0.255) the mixture
is 0.309 [me]. The 1178 and 1131 BC totality windows
