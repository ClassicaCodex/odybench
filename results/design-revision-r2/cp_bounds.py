"""Design revision 3 scratch: pool-size arithmetic and Clopper-Pearson bounds
that decide whether each outcome of the decision rule is attainable.

Inputs (all from earlier work, cited in DESIGN rev 3 section 2):
- spring daylight new moons at Ithaki: 266 in -1499..-1000 (500 yr)
  [critique-design-r1, check_lr_cap.out.txt];
- P(A) = 0.154 (95% 0.111-0.198) [same];
- daylight share of conjunctions 50.9% [research-visibility 4.2];
- 12.3683 synodic months per Julian year.
Core of revision 3: -1748..-51 inclusive (1,698 years).
Run: py results/design-revision-r2/cp_bounds.py
"""
from scipy.stats import beta

CORE_Y = 1698
spring_day_per_y = 266 / 500
n_TC = spring_day_per_y * CORE_Y
n_T = 12.3683 * 0.509 * CORE_Y
for pa in (0.111, 0.154, 0.198):
    print(f"P(A) {pa}: n_A = {n_TC * pa:.0f}")
print(f"n_T (daylight conjunctions in core) = {n_T:.0f};  n_TC = {n_TC:.0f}")


def cp_hi(k, n):
    return 1.0 if k >= n else float(beta.ppf(0.975, k + 1, n - k))


def cp_lo(k, n):
    return 0.0 if k == 0 else float(beta.ppf(0.025, k, n - k + 1))


for n in (100, 139, 179, 200, 480, 903, 10690):
    print(f"n={n:6d}: " + "  ".join(f"k={k}: {cp_hi(k, n):.4f}" for k in range(0, 6)))
# largest k with CP upper <= 0.05
for n in (100, 139, 179, 200, 903):
    k = 0
    while cp_hi(k + 1, n) <= 0.05:
        k += 1
    print(f"n={n}: CP_hi <= 0.05 for k <= {k if cp_hi(0, n) <= 0.05 else 'none'}")
# Revision 2's pool, for comparison: core -1748..-851 (898 yr)
n_TC2 = spring_day_per_y * 898
print(f"rev 2 core: n_TC = {n_TC2:.0f}, n_A = {n_TC2 * 0.154:.0f}, CP_hi(0, n_A) = {cp_hi(0, round(n_TC2 * 0.154)):.4f}")
# garden sizes with F6 off (DESIGN rev 3 5.3)
import math
bm = 2 * 1 * 1 * 1 * 1 * 18 * 1 * 1
doc = 4 * 3 * 3 * 3 * 3 * 37 * 1 * 3
full = 8 * 6 * 4 * 6 * 6 * 37 * 1 * 3
print("gardens (F6 off):", bm, doc, full, [round(math.log2(x), 1) for x in (bm, doc, full)])
print("eclipse-compatible:", bm, doc // 3, full // 2)
