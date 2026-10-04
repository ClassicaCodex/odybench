"""Design revision 8 scratch [r3v7 R3-2 fix 3]: what outcome 4's G condition,
G_j,hi <= G_BM,u,lo, allows a clean negative's garden to reach.

Pure arithmetic on design-stage numbers already in DESIGN 2.9 (no sky, no
search): n_T = 10,690 core targets; G_BM,u = (131/10,690) x 0.140 and
G_BM,u,lo = (131/10,690) x 0.087 (v1). The upper bound is the Fay-Feuer gamma
interval of DESIGN 5.3, each target counting 1 weighted by reach/n:
  y = G, v = sum (reach/n)^2, w = 1/n,
  G_hi = ((v + w^2) / (2 (y + w))) chi2_0.975(2 (y + w)^2 / (v + w^2)).
The rule's interval is the wider of this and a block bootstrap, which can only
widen it, so every count below is an upper limit.
Run: py results/design-revision-v8/outcome4_bound.py
"""
import math

from scipy.stats import chi2, gamma

N_T = 10690
G_BM_U = 131 / N_T * 0.140
G_BM_U_LO = 131 / N_T * 0.087


def g_hi(reaches, n=N_T):
    """Fay-Feuer upper 97.5% bound of G = sum(reaches)/n (DESIGN 5.3)."""
    y = sum(reaches) / n
    v = sum((r / n) ** 2 for r in reaches)
    w = 1.0 / n
    return ((v + w * w) / (2 * (y + w))) * chi2.ppf(0.975, 2 * (y + w) ** 2 / (v + w * w))


def max_targets(reach, bound=G_BM_U_LO, n=N_T, k_max=10000):
    """the largest number k of reached targets, each with the given reach, with g_hi <= bound."""
    best = 0
    for k in range(0, k_max + 1):
        if g_hi([reach] * k, n) <= bound:
            best = k
        else:
            break
    return best


def max_units_shaped(shape, bound=G_BM_U_LO, n=N_T, k_max=2000):
    """the largest total reach of a garden whose reached targets have the given reach
    distribution (a list repeated cyclically), with g_hi <= bound."""
    best = 0.0
    for k in range(0, k_max + 1):
        rs = [shape[i % len(shape)] for i in range(k)]
        if g_hi(rs, n) <= bound:
            best = sum(rs)
        else:
            break
    return best


def main():
    print(f"n_T {N_T}; G_BM,u {G_BM_U:.6f} ({G_BM_U * N_T:.1f} reach-units); "
          f"G_BM,u,lo {G_BM_U_LO:.6f} ({G_BM_U_LO * N_T:.2f} units)")
    print(f"no target reached: G_hi = {g_hi([]):.6f} = {g_hi([]) * N_T:.3f}/n (U0, DESIGN 9.2: 3.69/n)")
    print("k targets each of reach 1 (the exact Poisson bound gamma.ppf(0.975, k + 1)/n):")
    for k in range(0, 7):
        ff = g_hi([1.0] * k)
        print(f"  k {k}: G_hi {ff:.6f}  (gamma {gamma.ppf(0.975, k + 1) / N_T:.6f})  "
              f"{'<=' if ff <= G_BM_U_LO else '> '} G_BM,u,lo")
    print("largest number of reached targets, and reach-units, with G_hi <= G_BM,u,lo, by reach per target:")
    for r in (1.0, 0.75, 0.5, 0.25, 0.1, 0.05, 0.01):
        k = max_targets(r)
        print(f"  reach {r:4.2f}: at most {k:4d} targets = {k * r:5.2f} units")
    shape = [1.0, 0.41]  # 2.9: half of G_BM*'s 26 reached targets at reach 1; mean reach 18.4/26 = 0.71
    u = max_units_shaped(shape)
    print(f"a garden shaped like G_BM*'s (half its reached targets at reach 1, the rest 0.41): "
          f"at most {u:.2f} units")
    print(f"G_BM* reaches {G_BM_U * N_T:.1f} units, so the negative's garden must reach at most "
          f"{4 / (G_BM_U * N_T):.2f} of that at reach 1 ({G_BM_U * N_T / 4:.1f} times more selective), "
          f"and at most {u / (G_BM_U * N_T):.2f} if shaped like G_BM* ({G_BM_U * N_T / u:.1f} times)")
    k_bm = max_targets(1.0, bound=G_BM_U)
    print(f"(against revision 6's point value G_BM,u the count at reach 1 would have been {k_bm})")


if __name__ == "__main__":
    main()
