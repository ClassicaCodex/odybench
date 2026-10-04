"""Design revision 8 scratch [r3v7 R3-3]: the P(total) table of DESIGN 2.3,
recomputed over the CONTINUOUS totality windows, and the accuracy budget of
I2(c)'s comparison with it.

Revision 7's table (results/critique-design/check_p19.py) integrated each
ΔT model's Gaussian over the first review's 5-s-grid windows, 28,805-29,580 s
(16 Apr 1178 BC) and 27,050-28,035 s (30 Sep 1131 BC). DESIGN 10.2 hands
p_exact the window of eclipses.totality_window, i.e. the continuous window.

This script evaluates NO sky. It reads the two continuous windows that the
recheck bisected to 0.01 s with the review's own solver
(results/critique-design-r3/i2c_table_gap.out.txt), and integrates the four
ΔT models over them, exactly as check_p19.py does: model values and sigmas
from odybench.ephem at the epochs check_p19.py uses (noon UT of the eclipse
day), SMH models converted to the canon frame by the ndot term. The 1178 BC
window and its P(total) values are the published reproduction values that
DESIGN 2.3 already lists; nothing else of the target's sky is touched.
The P(smag >= 0.9) column is not recomputed: it is not a totality window and
not an I2(c) reference.
Run: py results/design-revision-v8/i2c_table.py
"""
import math
import re
import sys

sys.path.insert(0, "C:/Projects/odybench")
from odybench import ephem as E  # noqa: E402

GAP_OUT = "C:/Projects/odybench/results/critique-design-r3/i2c_table_gap.out.txt"
MODELS = ("smh2020", "smh2020_parabola", "smh2016_parabola", "em2006_canon")
LABEL = {"smh2020": "SMH2020", "smh2020_parabola": "Addendum 2020 parabola",
         "smh2016_parabola": "SMH2016 parabola", "em2006_canon": "Espenak-Meeus, canon form"}
GRID78 = (28805.0, 29580.0)      # the first review's 5-s-grid windows (check_p19.py)
GRID31 = (27050.0, 28035.0)
PRINTED = {  # revision 7's 2.3 table: P78, P31, joint
    "smh2020": (0.294, 0.494, 0.047), "smh2020_parabola": (0.173, 0.641, 0.052),
    "smh2016_parabola": (0.498, 0.443, 0.108), "em2006_canon": (0.252, 0.412, 0.049),
    "mixture": (0.304, 0.498, 0.064)}


def Phi(z):
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def p_window(mu, sigma, a, b):
    """Gaussian mass of N(mu, sigma) over [a, b]."""
    return Phi((b - mu) / sigma) - Phi((a - mu) / sigma)


def joint_common_offset(mu78, s78, w78, mu31, w31):
    """check_p19.py's joint: one common offset d from each model value, d ~ N(0, s78),
    with both eclipses total: d in [w78 - mu78] and in [w31 - mu31]."""
    lo = max(w78[0] - mu78, w31[0] - mu31)
    hi = min(w78[1] - mu78, w31[1] - mu31)
    return (Phi(hi / s78) - Phi(lo / s78)) if hi > lo else 0.0


def ndot_conv(y):
    """SMH (ndot -25.82) -> canon (ndot -25.858), seconds; as check_p19.py."""
    return -0.91072 * (-25.858 + 25.82) * ((y - 1955) / 100) ** 2


def models_at(y):
    """[(model, mu_canon_frame, sigma)] at Julian epoch y."""
    out = []
    for m in MODELS:
        mu = E.delta_t(y, m) + (ndot_conv(y) if m.startswith("smh") else 0.0)
        out.append((m, mu, E.delta_t_sigma(y, m)))
    return out


def max_density(sigma):
    """largest change of a Gaussian mass per second of boundary shift: 1/(sigma sqrt(2 pi))."""
    return 1.0 / (sigma * math.sqrt(2.0 * math.pi))


def read_windows(path=GAP_OUT):
    t = open(path, encoding="utf-8").read()
    m1 = re.search(r"continuous totality window \(canon frame\): ([\d.]+) - ([\d.]+) s", t)
    m2 = re.search(r"1131 BC continuous totality window: ([\d.]+) - ([\d.]+) s", t)
    return (float(m1.group(1)), float(m1.group(2))), (float(m2.group(1)), float(m2.group(2)))


def table(w78, w31, y78, y31):
    rows = {}
    a78, a31 = models_at(y78), models_at(y31)
    for (m, mu78, s78), (_, mu31, s31) in zip(a78, a31):
        rows[m] = (p_window(mu78, s78, *w78), p_window(mu31, s31, *w31),
                   joint_common_offset(mu78, s78, w78, mu31, w31), mu78, s78, mu31, s31)
    rows["mixture"] = tuple(sum(rows[m][k] for m in MODELS) / 4 for k in range(3)) + (None,) * 4
    return rows


def main():
    w78, w31 = read_windows()
    y78 = E.julian_epoch(E.jd_from_julian(-1177, 4, 16, 12))
    y31 = E.julian_epoch(E.jd_from_julian(-1130, 9, 30, 12))
    print(f"epochs {y78:.3f} {y31:.3f} (check_p19.py's, noon UT)")
    print(f"continuous windows [r3v7: i2c_table_gap.py]: 1178 BC {w78[0]:.2f}-{w78[1]:.2f} s; "
          f"1131 BC {w31[0]:.2f}-{w31[1]:.2f} s")
    grid = table(GRID78, GRID31, y78, y31)
    cont = table(w78, w31, y78, y31)
    print("\nReproduction of revision 7's printed table on the 5-s-grid windows (must agree to rounding):")
    worst = 0.0
    for m in MODELS + ("mixture",):
        g = grid[m][:3]
        d = max(abs(round(g[k], 3) - PRINTED[m][k]) for k in range(3))
        worst = max(worst, d)
        print(f"  {m:18s} {g[0]:.4f} {g[1]:.4f} {g[2]:.4f}  printed {PRINTED[m]}  max |rounded - printed| {d:.4f}")
    assert worst <= 0.0011, "the grid-window values do not reproduce the printed table"

    print("\nThe 2.3 table over the continuous windows (revision 8):")
    print("  model (value +- sigma at -1176.68, canon frame)      P(total) 1178   P(total) 1131   joint   | change from revision 7")
    for m in MODELS + ("mixture",):
        c = cont[m]
        lab = LABEL.get(m, "equal-weight mixture of the four")
        if m != "mixture":
            lab += f" {c[3] - ndot_conv(y78) if m.startswith('smh') else c[3]:,.0f} +- {c[4]:,.0f}"
        dd = tuple(round(c[k], 3) - PRINTED[m][k] for k in range(3))
        print(f"  {lab:52s}  {c[0]:.4f} ({c[0]:.3f})  {c[1]:.4f} ({c[1]:.3f})  {c[2]:.4f} ({c[2]:.3f}) "
              f"| {dd[0]:+.3f} {dd[1]:+.3f} {dd[2]:+.3f}")
    em = cont["em2006_canon"][0]
    pairing = (0.299 + 0.178 + 0.505 + em) / 4
    print(f"\nDE431 pairing (SMH values 0.299, 0.178, 0.505 [eph 5.4], E-M on NASA's elements {em:.4f}): "
          f"mixture {pairing:.4f}")
    print(f"m-hat = 0.304 (revision 7's grid-window mixture) lies {cont['mixture'][0] - 0.304:+.4f} below the "
          f"continuous mixture {cont['mixture'][0]:.4f}")

    print("\nI2(c) budget for P(total) against the recomputed table:")
    print("  table rounding to 0.001: at most 0.0005")
    for tol in (0.1, 0.01):
        print(f"  p_exact bisection to {tol} s: at most {tol * max_density(540.6):.2e} per boundary at sigma 541 s "
              f"(the smallest sigma; {tol * max_density(1007.7):.2e} at 1,008 s)")
    print(f"  a 1-s shift of one boundary: at most {max_density(540.6):.2e} at sigma 541 s")
    for m, mu, s in models_at(y78):
        dens = [math.exp(-0.5 * ((x - mu) / s) ** 2) * max_density(s) for x in w78]
        print(f"    {m:18s} density at the 1178 BC boundaries {dens[0]:.2e} and {dens[1]:.2e} per s; "
              f"a 1-s widening at both moves P by {sum(dens):.4f}")
    mix_dens = sum(math.exp(-0.5 * ((x - mu) / s) ** 2) * max_density(s)
                   for m, mu, s in models_at(y78) for x in w78) / 4
    print(f"  mixture: a 1-s widening at both 1178 BC boundaries moves P by {mix_dens:.4f}")
    worst_model = max(sum(math.exp(-0.5 * ((x - mu) / s) ** 2) * max_density(s) for x in w78)
                      for m, mu, s in models_at(y78))
    print(f"  so with the windows within 1 s of the reference, a correct implementation lies within "
          f"{0.0005 + 2 * 0.1 * max_density(540.6) + worst_model:.4f} of the table (tolerance 0.005)")
    print(f"  revision 7's grid-window table against the continuous values: largest gap "
          f"{max(abs(cont[m][0] - PRINTED[m][0]) for m in MODELS + ('mixture',)):.4f} (1178 BC), "
          f"{max(abs(cont[m][1] - PRINTED[m][1]) for m in MODELS + ('mixture',)):.4f} (1131 BC)")

    print("\nR7's joint bounds (<= 0.06 for three models, >= 0.08 for SMH2016) if both windows shift by d s "
          "against every model value (a frame change):")
    for d in (-40, -10, 0, 10, 40):
        js = []
        for (m, mu78, s78), (_, mu31, _s31) in zip(models_at(y78), models_at(y31)):
            js.append(joint_common_offset(mu78, s78, (w78[0] + d, w78[1] + d), mu31, (w31[0] + d, w31[1] + d)))
        print(f"  d {d:+4d} s: " + "  ".join(f"{m} {j:.4f}" for m, j in zip(MODELS, js)))


if __name__ == "__main__":
    main()
