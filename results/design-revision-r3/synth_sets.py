"""Design revision 4 scratch: the numbers of the synthetic input sets of
DESIGN 9.5, and the checks of 9.4 they must satisfy.

Null-side fields are the design-stage estimates of DESIGN 2.9 (constraint C7):
  * slot-variant pools and G_BM per variant: r2's check_slot_scaling.out.txt
    (Fay-Feuer gamma interval; the block-bootstrap widening of 5.3 can only
    widen them);
  * G_BM,u = sum(reach) / n_T, the same for every variant (identity of 4.2);
  * held-out pool P_BM: n_H = 76, 1 member passes H3 and H4, 2 pass H4,
    15 pass H3 (results/design-revision-r3/heldout_attain.out.txt).
Target-side fields (T0_pass, p_H, r_Ody, pct_N4, the control counts, hit_j)
are free, subject to the lattice and interval constraints C1-C9.
Run: py results/design-revision-r3/synth_sets.py
"""
from scipy.stats import beta, chi2

N_T = 10690
VARIANTS = {   # name: (n_A, G, lo, hi)  [r2: check_slot_scaling.py]
    "v0 documented (Venus AV 7; Mercury event <= 6 d and visible)": (82, 0.224, 0.139, 0.344),
    "v1 revision 3 (Venus AV 7; Mercury event <= 6 d or visible)": (131, 0.140, 0.087, 0.215),
    "v2 (Venus AV 7; Mercury event <= 6 d)": (87, 0.211, 0.131, 0.324),
    "v3 (Venus AV 7; Mercury event <= 4 d)": (66, 0.278, 0.172, 0.427),
    "v4 (Venus lead >= 60 min; Mercury as v1)": (101, 0.182, 0.112, 0.279),
    "v5 (Venus lead >= 60 min; Mercury event <= 4 d)": (56, 0.327, 0.203, 0.504),
}
N_H, X_BOTH, X_H4, X_H3 = 76, 1, 2, 15


def gamma_ci(reaches, n):
    y = sum(reaches) / n
    v = sum((r / n) ** 2 for r in reaches)
    w = 1.0 / n
    hi = (v + w * w) / (2 * (y + w)) * chi2.ppf(0.975, 2 * (y + w) ** 2 / (v + w * w))
    lo = 0.0 if y == 0 else v / (2 * y) * chi2.ppf(0.025, 2 * y * y / v)
    return y, lo, hi


def cp_lo(k, n):
    return 0.0 if k == 0 else beta.ppf(0.025, k, n - k + 1)


def cp_hi(k, n):
    return 1.0 if k == n else beta.ppf(0.975, k + 1, n - k)


def pct(x_gt, x_eq, n):
    """mid-p point; lower bound from the strict count, upper from the weak count (5.4)."""
    return (x_gt + 0.5 * x_eq) / n, cp_lo(x_gt, n), cp_hi(x_gt + x_eq, n)


print("Slot family (design-stage estimates, r2):")
gu = set()
for k, (n, g, lo, hi) in VARIANTS.items():
    gu.add(round(n * g / N_T, 5))
    print(f"  {k:66s} n_A {n:4d}  G_BM {g:.3f} [{lo:.3f}, {hi:.3f}]  "
          f"label-2 G-leg {'fires' if lo >= 0.20 else 'no'}  Q_tol {'yes' if lo > 0.05 else 'no'}  "
          f"(n_A/n_T) G = {n * g / N_T:.5f}")
mins = min(v[2] for v in VARIANTS.values())
print(f"  min over variants of G_BM,lo = {mins:.3f}: label-2 G-leg fires only if >= 0.20 -> "
      f"{'fires' if mins >= 0.2 else 'does not fire'}; Q_tol (> 0.05) -> {'holds' if mins > 0.05 else 'no'}")
fires = [k[:2] for k, v in VARIANTS.items() if v[2] >= 0.20]
print(f"  variants where the G-leg alone would fire: {fires} -> Q_slot holds")
print(f"  G_BM,u across variants (identity): {sorted(gu)}  (r2 printed 0.00172)")

print("\nHeld-out lattice on P_BM (score order: both > H4 only > H3 only > none, since q4 < q3):")
pmin = (1 + X_BOTH) / (1 + N_H)
print(f"  p_H,min (passes both) = (1+{X_BOTH})/(1+{N_H}) = {pmin:.4f}")
print(f"  passes H4 only: (1+{X_H4})/(1+{N_H}) = {(1 + X_H4) / (1 + N_H):.4f}")
x_ge_h3 = X_H3 + X_H4 - X_BOTH
print(f"  passes H3 only: (1+{x_ge_h3})/(1+{N_H}) = {(1 + x_ge_h3) / (1 + N_H):.4f}")
print(f"  passes neither: 1.0000")
print(f"  S5 (Q_attain branch test): x_both 4 -> p_H,min = {(1 + 4) / (1 + N_H):.4f}")

print("\npct_N4 (mid-p; lo from strict count, hi from weak count), n = 200:")
for xg, xe in ((30, 10), (118, 12), (2, 0)):
    p, lo, hi = pct(xg, xe, 200)
    print(f"  x_gt {xg:3d}, x_eq {xe:2d}: pct {p:.4f}  lo {lo:.4f}  hi {hi:.4f}  "
          f"label-2 pct-leg {'fires' if lo >= 0.5 else 'no'}")

print("\nNegatives (G_j over n_j = 10,690):")
for lab, reaches in (("no-hit sets: 8 x 0.8", [0.8] * 8), ("S4 AEN-TROY: 6 x 0.9", [0.9] * 6),
                     ("S6b AEN-TROY: 25 x 0.8", [0.8] * 25)):
    g = gamma_ci(reaches, N_T)
    print(f"  {lab:24s} G_j {g[0]:.5f}  lo {g[1]:.5f}  hi {g[2]:.5f}   G_j,hi <= G_BM,u 0.00172: {g[2] <= 0.00172}")
print(f"\nU0(n) = 3.689/n: n_T {3.689 / N_T:.5f}; n_H floor 1/(1+n_H) = {1 / (1 + N_H):.4f}")
