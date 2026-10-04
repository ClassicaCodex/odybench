"""Design revision 3 scratch: the numbers of the synthetic input sets of
DESIGN 9.5, computed from assumed reach vectors with the intervals the design
specifies, so that every set satisfies the structural constraints of 9.4.

G interval: Fay & Feuer (1997) gamma interval for a weighted sum of counts,
each reached target a count of 1 weighted by reach/n, maximum weight 1/n.
pct interval: exact Clopper-Pearson.
Run: py results/design-revision-r2/synth_sets.py
"""
from scipy.stats import beta, chi2

N_A, N_T, N_STRAT = 139, 10690, 200


def gamma_ci(reaches, n):
    y = sum(reaches) / n
    v = sum((r / n) ** 2 for r in reaches)
    w = 1.0 / n
    hi = (v + w * w) / (2 * (y + w)) * chi2.ppf(0.975, 2 * (y + w) ** 2 / (v + w * w))
    lo = 0.0 if y == 0 else v / (2 * y) * chi2.ppf(0.025, 2 * y * y / v)
    return y, lo, hi


def cp(k, n):
    lo = 0.0 if k == 0 else beta.ppf(0.025, k, n - k + 1)
    hi = 1.0 if k == n else beta.ppf(0.975, k + 1, n - k)
    return k / n, lo, hi


def show(label, g):
    print(f"{label:28s} G {g[0]:.5f}  lo {g[1]:.5f}  hi {g[2]:.5f}")


print("U0(n) = 3.69/n:", {n: round(3.689 / n, 4) for n in (70, 74, 139, 10690)})
show("S1 G_BM (3 x 0.30 / 139)", gamma_ci([0.3] * 3, N_A))
show("S1 G_DOC (5 x 0.33 / 139)", gamma_ci([0.33] * 5, N_A))
show("S2 G_BM (60 x 0.70 / 139)", gamma_ci([0.7] * 60, N_A))
show("S2 G_DOC (80 x 0.73 / 139)", gamma_ci([0.73] * 80, N_A))
show("S4 G_BM (20 x 0.70 / 139)", gamma_ci([0.7] * 20, N_A))
show("S4 G_DOC (30 x 0.70 / 139)", gamma_ci([0.7] * 30, N_A))
show("S5 G_DOC (10 x 0.70 / 139)", gamma_ci([0.7] * 10, N_A))
show("S9 G_BM (0 reached / 70)", gamma_ci([], 70))
show("neg G_j (8 x 0.8 / 10690)", gamma_ci([0.8] * 8, N_T))
show("S4 neg G_j (6 x 0.9 / 10690)", gamma_ci([0.9] * 6, N_T))
show("S6 neg G_j (25 x 0.8 / 10690)", gamma_ci([0.8] * 25, N_T))
for k in (2, 40, 124):
    p = cp(k, N_STRAT)
    print(f"pct k={k:3d}/200: {p[0]:.4f}  lo {p[1]:.4f}  hi {p[2]:.4f}")
r = N_A / N_T
for g in (0.00648, 0.3022, 0.1007):
    print(f"G_BM,u = (n_A/n_T) * {g} = {r * g:.6f}")
