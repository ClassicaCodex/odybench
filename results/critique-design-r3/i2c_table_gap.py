"""Recheck of DESIGN revision 7 (round 3): can I2(c)'s second criterion,
"P(total) per model and for the mixture within 0.005 of the 2.3 table", be
met by an exact integrator?

The 2.3 table (results/critique-design/check_p19.py) integrates each model's
Gaussian over the review's 5-s-grid totality window for 16 Apr -1177 at Ithaki,
28,805-29,580 s (canon frame, NASA elements). DESIGN 10.2 says a totality row
hands p_exact "the window of eclipses.totality_window directly", i.e. the
continuous window. Here the continuous window is found by bisecting the same
review solver (check_bessel.py, which reads data/jsex/... through its own
default path; only its maxecl is used) to 0.01 s, and the per-model P(total)
is computed both ways, with the same model values, sigmas and +34 s frame
conversion that check_p19.py uses.

The target's own eclipse is a public, design-stage number (DESIGN 2.3); no
held-out predicate is evaluated. Run: py -X utf8 results/critique-design-r3/i2c_table_gap.py
"""
import math
import sys

sys.path.insert(0, r"C:\Projects\odybench")
sys.path.insert(0, r"C:\Projects\odybench\results\critique-design")
from odybench import ephem as E          # noqa: E402
import check_bessel as B                  # noqa: E402

Phi = lambda z: 0.5 * (1 + math.erf(z / math.sqrt(2)))
LAT, LON = 38.367, 20.717                 # the review's Ithaki (check_bessel.ITH)


def load():
    # check_bessel's own loader and file; the JSEX century file for -1199..-1100
    for path in (r"C:\Projects\odybench\data\jsex\SEm1199.js",
                 r"C:\Projects\odybench\data\refs\nasa\JSEX-SEm1199.js"):
        try:
            return B.load_jsex(path), path
        except Exception:
            continue
    raise SystemExit("no JSEX file for -1199")


def edge(Ee, lo, hi, want_total_at_hi):
    """bisect the dT at which totality starts (or ends) between lo and hi."""
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        tot = B.maxecl(Ee, LAT, LON, mid)["total"]
        if tot == want_total_at_hi:
            hi = mid
        else:
            lo = mid
        if hi - lo < 0.01:
            break
    return 0.5 * (lo + hi)


def main():
    EL, path = load()
    Ee = B.elems(EL[(-1177, 4, 16)])
    a = edge(Ee, 28795.0, 28810.0, True)        # partial below, total above
    b = edge(Ee, 29575.0, 29590.0, False)       # total below, partial above
    print(f"elements: {path}")
    print(f"continuous totality window (canon frame): {a:.2f} - {b:.2f} s; the 2.3 table used 28805 - 29580 s")
    y78 = E.julian_epoch(E.jd_from_julian(-1177, 4, 16, 12))
    conv = lambda y: -0.91072 * (-25.858 + 25.82) * ((y - 1955) / 100) ** 2
    tot_grid = tot_exact = 0.0
    for model in ("smh2020", "smh2020_parabola", "smh2016_parabola", "em2006_canon"):
        mu = E.delta_t(y78, model) + (conv(y78) if model.startswith("smh") else 0.0)
        s = E.delta_t_sigma(y78, model)
        pg = Phi((29580 - mu) / s) - Phi((28805 - mu) / s)
        pe = Phi((b - mu) / s) - Phi((a - mu) / s)
        tot_grid += pg / 4
        tot_exact += pe / 4
        print(f"{model:18s} mu {mu:8.1f} sigma {s:6.1f}  P(grid window) {pg:.4f} (table {round(pg, 3):.3f})  "
              f"P(continuous) {pe:.4f}  difference {pe - pg:+.4f}  vs table {pe - round(pg, 3):+.4f}")
    print(f"mixture: grid {tot_grid:.4f}  continuous {tot_exact:.4f}  difference {tot_exact - tot_grid:+.4f}")

    # the same for 30 Sep 1131 BC (-1130), whose 2.3 column used the 5-s-grid window 27,050-28,035 s
    EL2, path2 = None, None
    for p in (r"C:\Projects\odybench\data\jsex\SEm1199.js",):
        EL2, path2 = B.load_jsex(p), p
    key = (-1130, 9, 30)
    if key not in EL2:
        print("1131 BC eclipse not in", path2)
        return
    E2 = B.elems(EL2[key])
    a2 = edge(E2, 27040.0, 27056.0, True)
    b2 = edge(E2, 28030.0, 28045.0, False)
    print(f"\n1131 BC continuous totality window: {a2:.2f} - {b2:.2f} s; the 2.3 table used 27050 - 28035 s")
    y31 = E.julian_epoch(E.jd_from_julian(-1130, 9, 30, 12))
    mg = me = 0.0
    for model in ("smh2020", "smh2020_parabola", "smh2016_parabola", "em2006_canon"):
        mu = E.delta_t(y31, model) + (conv(y31) if model.startswith("smh") else 0.0)
        s = E.delta_t_sigma(y31, model)
        pg = Phi((28035 - mu) / s) - Phi((27050 - mu) / s)
        pe = Phi((b2 - mu) / s) - Phi((a2 - mu) / s)
        mg += pg / 4
        me += pe / 4
        print(f"{model:18s} P(grid window) {pg:.4f} (table {round(pg, 3):.3f})  P(continuous) {pe:.4f}  vs table {pe - round(pg, 3):+.4f}")
    print(f"mixture: grid {mg:.4f}  continuous {me:.4f}  difference {me - mg:+.4f}")


if __name__ == "__main__":
    main()
