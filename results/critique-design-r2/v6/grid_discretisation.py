# How far apart can the bench's 41-point Delta-T mixture grid (DESIGN 6.3.3; deltat_mix.grid,
# +-4 sigma per model, Gaussian weights, models equal) and I16's 201-point reference grid be,
# for a row that passes on one Delta-T interval (a totality window) or a half-line (a threshold)?
# I16 lists a flag mismatch as a tie only if |P_mix - 0.5| < 0.02 (DESIGN 6.1, I16).
# I2(c) asks deltat_mix.py for P(total) within 0.005 of a 1e6-draw Monte Carlo (DESIGN 6.1, I2).
# Models at -1176.68 in the canon frame (DESIGN 2.3 table; SMH values +34 s): exact CDF vs grids.
import numpy as np
from math import erf, sqrt

MODELS = {  # mean, sigma (s), canon frame, from DESIGN 2.3
    "smh2020": (28543 + 34, 720), "add2020": (28282 + 34, 541),
    "smh2016": (28963 + 34, 541), "em_canon": (28589, 1008)}

def Phi(x):
    return 0.5 * (1 + erf(x / sqrt(2)))

def grid(n):
    z = np.linspace(-4, 4, n)
    w = np.exp(-z * z / 2); w /= w.sum()
    return z, w

def p_exact(lo, hi):
    return np.mean([Phi((hi - m) / s) - Phi((lo - m) / s) for m, s in MODELS.values()])

def p_grid(lo, hi, n):
    z, w = grid(n)
    tot = 0.0
    for m, s in MODELS.values():
        x = m + s * z
        tot += w[(x >= lo) & (x <= hi)].sum()
    return tot / len(MODELS)

out = []
# 1. the 1178 BC totality window at Ithaki (NASA elements, canon frame): 28,805-29,580 s
#    (the models above are the -1176.68 values, so only the 1178 BC window is meaningful here)
for (lo, hi, label) in [(28805, 29580, "1178 BC totality window")]:
    pe = p_exact(lo, hi)
    out.append(f"{label}: exact {pe:.4f}  41-pt {p_grid(lo, hi, 41):.4f}  201-pt {p_grid(lo, hi, 201):.4f}"
               f"  |41-exact| {abs(p_grid(lo, hi, 41) - pe):.4f}")
# 2. half-line rows (pass for dT >= c): sweep c, look at cases where the two grids straddle 0.5
worst = (0, None)
straddle_outside_band = []
for c in np.arange(26500, 31000, 1.0):
    p41 = p_grid(c, 1e9, 41); p201 = p_grid(c, 1e9, 201); pe = p_exact(c, 1e9)
    d = abs(p41 - p201)
    if d > worst[0]:
        worst = (d, (c, p41, p201, pe))
    if (p41 >= 0.5) != (p201 >= 0.5) and abs(p41 - 0.5) >= 0.02 and abs(p201 - 0.5) >= 0.02:
        straddle_outside_band.append((c, round(p41, 4), round(p201, 4)))
out.append(f"half-line rows over c in 26,500..31,000 s: max |P41 - P201| = {worst[0]:.4f} at c = {worst[1][0]:.0f} "
           f"(P41 {worst[1][1]:.4f}, P201 {worst[1][2]:.4f}, exact {worst[1][3]:.4f})")
out.append(f"flag mismatches with BOTH sides outside the 0.02 tie band: {len(straddle_outside_band)} values of c "
           f"(first: {straddle_outside_band[:3]})")
# 3. interval rows (pass for lo <= dT <= lo + width) anywhere: max |P41 - exact|, and I16 flag failures
worst2 = 0
fail_either, fail_bench, near_half = [], [], 0
for wdt in (200, 400, 780, 1000, 1500, 2000, 2500, 3000):
    for lo in np.arange(25000, 31500, 5.0):
        p41 = p_grid(lo, lo + wdt, 41); p201 = p_grid(lo, lo + wdt, 201); pe = p_exact(lo, lo + wdt)
        worst2 = max(worst2, abs(p41 - pe))
        if abs(p41 - 0.5) < 0.1:
            near_half += 1
        if (p41 >= 0.5) != (p201 >= 0.5):
            # reading (i): tie band applies if EITHER side is within 0.02 of 0.5
            if abs(p41 - 0.5) >= 0.02 and abs(p201 - 0.5) >= 0.02:
                fail_either.append((wdt, lo, round(p41, 4), round(p201, 4)))
            # reading (ii): tie band read on the bench side only
            if abs(p41 - 0.5) >= 0.02:
                fail_bench.append((wdt, lo, round(p41, 4), round(p201, 4)))
out.append(f"interval rows (width 200-3000 s): max |P41 - exact| = {worst2:.4f}; cases with |P41-0.5|<0.1: {near_half}")
out.append(f"  I16 flag mismatches outside the tie band, band read on either side: {len(fail_either)}; "
           f"band read on the bench side only: {len(fail_bench)}; examples {fail_bench[:4]}")
# 4. one model alone, step at its mean: the largest single-model error of a 41-point grid
z, w = grid(41)
out.append(f"single Gaussian, 41 points over +-4 sigma: largest weight {w.max():.4f}; "
           f"step error at a node up to about half to one weight")
print("\n".join(out))
open(__file__.replace(".py", ".out.txt"), "w").write("\n".join(out) + "\n")
