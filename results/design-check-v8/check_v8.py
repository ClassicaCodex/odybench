"""Independent recomputation of the numbers that DESIGN revision 8 states in
answer to issues R3-1 .. R3-11 of docs/critique-design-r3.md (scratch for the
design check of revision 8; written by a reviewer who did not write the fix).

This script evaluates NO sky and runs no search. Its inputs are:
- section-2 values only for the target: the continuous and 5-s-grid totality
  windows of 16 Apr 1178 BC and 30 Sep 1131 BC at Ithaki (DESIGN 2.3) and the
  four Delta-T models (odybench.ephem; at -1176.68 they are checked against
  the means and sigmas printed in the 2.3 table);
- the design-stage G numbers of DESIGN 2.9 (G_BM 0.140 [0.087, 0.215] over
  n_A = 131; n_T = 10,690; 26 reached targets, half of them at reach 1);
- the recheck's recorded narrowing runs on three null windows
  (results/critique-design-r3/narrowing_inferred_phase.json);
- the moon-phase rows of data/prereg/controls_almagest.json (no truth file).

Run from C:/Projects/odybench:
    py results/design-check-v8/check_v8.py              the check
    py results/design-check-v8/check_v8.py --selftest   synthetic data only
"""
import json
import math
import sys

from scipy.optimize import brentq
from scipy.stats import gamma as _gamma

ROOT = "C:/Projects/odybench"
NARROW_JSON = ROOT + "/results/critique-design-r3/narrowing_inferred_phase.json"
CLUE_FILE = ROOT + "/data/prereg/controls_almagest.json"
MODELS = ("smh2020", "smh2020_parabola", "smh2016_parabola", "em2006_canon")
SQ2PI = math.sqrt(2.0 * math.pi)

# ---------------------------------------------------------------- Gaussians


def Phi(z):
    """standard normal CDF"""
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def phi(z):
    """standard normal density"""
    return math.exp(-0.5 * z * z) / SQ2PI


def p_window(mu, sigma, a, b):
    """mass of N(mu, sigma) on [a, b] (0 if b <= a)"""
    if b <= a:
        return 0.0
    return Phi((b - mu) / sigma) - Phi((a - mu) / sigma)


def joint_common_offset(mu1, s1, w1, mu2, w2):
    """first review's joint: one offset d ~ N(0, s1) from each model value, both
    windows total, i.e. d in (w1 - mu1) and in (w2 - mu2)"""
    lo = max(w1[0] - mu1, w2[0] - mu2)
    hi = min(w1[1] - mu1, w2[1] - mu2)
    return Phi(hi / s1) - Phi(lo / s1) if hi > lo else 0.0


def ndot_shift(y, ndot_from=-25.82, ndot_to=-25.858):
    """Delta-T change (s) on moving from a lunar ndot frame to another:
    -0.91072 (ndot_to - ndot_from) ((y - 1955)/100)^2 (Morrison-Stephenson form)"""
    u = (y - 1955.0) / 100.0
    return -0.91072 * (ndot_to - ndot_from) * u * u


def models_at(y, delta_t, delta_t_sigma):
    """[(model, mu in the canon frame, sigma)] at Julian epoch y; SMH models
    shifted from ndot -25.82 to the canon's -25.858"""
    out = []
    for m in MODELS:
        mu = float(delta_t(y, m)) + (ndot_shift(y) if m.startswith("smh") else 0.0)
        out.append((m, mu, float(delta_t_sigma(y, m))))
    return out


def table(models78, models31, w78, w31):
    """{model: (P78, P31, joint)} plus the equal-weight mixture"""
    rows = {}
    for (m, mu78, s78), (_m, mu31, s31) in zip(models78, models31):
        rows[m] = (p_window(mu78, s78, *w78), p_window(mu31, s31, *w31),
                   joint_common_offset(mu78, s78, w78, mu31, w31))
    names = [m for m, _a, _b in models78]
    rows["mixture"] = tuple(sum(rows[m][k] for m in names) / len(names) for k in range(3))
    return rows


def bisect_bound(tol_s, sigma):
    """largest change of a Gaussian mass for one boundary misplaced by tol_s"""
    return tol_s / (sigma * SQ2PI)


def positive_or_inf(s):
    """a sigma, or infinity where a model function returns none (0)"""
    return s if s > 0 else float("inf")


def max_boundaries(tol_s, sigma, budget=1e-4):
    """how many such boundaries fit inside the budget"""
    b = bisect_bound(tol_s, sigma)
    return int(math.floor(budget / b + 1e-12))


def widen_change(mu, sigma, w, d=1.0):
    """change of the mass on w when both boundaries move outward by d seconds"""
    return p_window(mu, sigma, w[0] - d, w[1] + d) - p_window(mu, sigma, w[0], w[1])


def shifted_joints(models78, models31, w78, w31, d):
    """joint per model when both windows move by d s against the model values"""
    out = {}
    for (m, mu78, s78), (_m, mu31, _s31) in zip(models78, models31):
        out[m] = joint_common_offset(mu78, s78, (w78[0] + d, w78[1] + d), mu31,
                                     (w31[0] + d, w31[1] + d))
    return out

# ---------------------------------------------------------------- G bounds


def ff_upper(reaches, n, level=0.975):
    """Fay-Feuer upper bound of G = sum(reach)/n (DESIGN 5.3), written with the
    gamma quantile: a = (y + w)^2/(v + w^2), scale = (v + w^2)/(y + w)"""
    y = sum(reaches) / n
    v = sum((r / n) ** 2 for r in reaches)
    w = 1.0 / n
    a = (y + w) ** 2 / (v + w * w)
    return float(_gamma.ppf(level, a, scale=(v + w * w) / (y + w)))


def poisson_upper(k, n, level=0.975):
    """exact Poisson upper bound of k counts over n"""
    return float(_gamma.ppf(level, k + 1)) / n


def max_reached(reach, bound, n, kmax=200000):
    """largest k with ff_upper([reach] * k, n) <= bound (ff_upper rises with k)"""
    if ff_upper([], n) > bound:
        return -1
    lo, hi = 0, 1
    while hi <= kmax and ff_upper([reach] * hi, n) <= bound:
        lo, hi = hi, hi * 2
    hi = min(hi, kmax + 1)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if ff_upper([reach] * mid, n) <= bound:
            lo = mid
        else:
            hi = mid
    return lo


def max_units_shaped(shape, bound, n, kmax=5000):
    """largest total reach of a garden whose reached targets repeat the reach
    pattern `shape`, with ff_upper <= bound"""
    best = 0.0
    for k in range(kmax + 1):
        rs = [shape[i % len(shape)] for i in range(k)]
        if ff_upper(rs, n) <= bound:
            best = sum(rs)
        else:
            break
    return best


def thin_limit_units(bound, n, level=0.975):
    """supremum of the total reach U as each reach -> 0: G_hi -> gamma quantile
    with shape (U + 1)^2 and scale 1/(n (U + 1)); solve G_hi = bound"""
    f = lambda u: float(_gamma.ppf(level, (u + 1.0) ** 2, scale=1.0 / (n * (u + 1.0)))) - bound
    if f(0.0) > 0:
        return 0.0
    return brentq(f, 0.0, bound * n * 10 + 10)

# ---------------------------------------------------------------- narrowing


def frac_range(runs, key):
    """(min, max) share of days passing, and (min, max) days, over the windows"""
    fr, dd = [], []
    for w in runs.values():
        s = w["sets"][key]
        fr.append(s["n_pass"] / s["n_cand"])
        dd.append(s["n_pass"])
    return (min(fr), max(fr)), (min(dd), max(dd))


def line_days(runs):
    """the 5% line in days, per window"""
    return sorted({int(math.floor(0.05 * w["n_cand"])) for w in runs.values()})


V8_KEYS = {  # revision 8's projection under the frozen meaning, as the recheck recorded it
    "ALM-A": "ALM-A [frozen, inferred phases none]",
    "ALM-B": "ALM-B [frozen, inferred phases none]",
    "ALM-D": "ALM-D", "ALM-E": "ALM-E", "ALM-F": "ALM-F", "ALM-G": "ALM-G",
    "ALM-H": "ALM-H", "ALM-K": "ALM-K", "ALM-L": "ALM-L",
    "ALM-I": "ALM-I (same_app & visible)", "ALM-J": "ALM-J (same_app & visible)",
}

# ---------------------------------------------------------------- clue file


def phase_rows(clues):
    """moon-phase rows: id -> (primary option, primary justification, text of the
    'none' option or None, set of option names)"""
    out = {}
    for c in clues:
        if c.get("kind") != "moon-phase":
            continue
        prim = [o for o in c["fork_options"] if o.get("primary")]
        none = [o for o in c["fork_options"] if o["option"] == "none"]
        out[c["clue_id"]] = (prim[0]["option"] if prim else None,
                             prim[0].get("justification", "") if prim else "",
                             none[0].get("justification") if none else None,
                             {o["option"] for o in c["fork_options"]})
    return out


def words_only_none(rows):
    """rows a words-only projection must set to 'none': those whose own 'none'
    option says the phase is not stated in words"""
    return sorted(k for k, (_p, _j, nj, _o) in rows.items()
                  if nj and "not stated in words" in nj)

# ---------------------------------------------------------------- public copy


MARKER = "<!-- APPENDIX-T:"


def phrase_lines(text, phrases):
    """[(line number, 'public' or 'AppT', phrase)] for every line holding one of the
    phrases; 'public' means above the Appendix-T marker line"""
    out, public = [], True
    for i, line in enumerate(text.splitlines(), 1):
        if line.startswith(MARKER):
            public = False
        for p in phrases:
            if p in line:
                out.append((i, "public" if public else "AppT", p))
    return out

# ---------------------------------------------------------------- main


def check(out=print):
    sys.path.insert(0, ROOT)
    from odybench import ephem as E
    from odybench import calendar as C

    y78 = C.julian_epoch(C.jd_from_julian(-1177, 4, 16, 12.0))
    y31 = C.julian_epoch(C.jd_from_julian(-1130, 9, 30, 12.0))
    out(f"epochs (noon UT, as the first review's check_p19.py): {y78:.3f} {y31:.3f}")
    m78 = models_at(y78, E.delta_t, E.delta_t_sigma)
    m31 = models_at(y31, E.delta_t, E.delta_t_sigma)
    printed = {"smh2020": (28543, 720), "smh2020_parabola": (28282, 541),
               "smh2016_parabola": (28963, 541), "em2006_canon": (28589, 1008)}
    for (m, mu, s) in m78:
        raw = mu - (ndot_shift(y78) if m.startswith("smh") else 0.0)
        ok = abs(raw - printed[m][0]) < 0.5 and abs(s - printed[m][1]) < 0.5
        out(f"  2.3's printed model value {m}: {printed[m][0]} +- {printed[m][1]} reproduced: {ok}")
    out(f"  ndot shift at -1176.68: {ndot_shift(y78):.2f} s (2.3: +34 s)")

    # DESIGN 2.3 windows (section-2 published values)
    W78C, W31C = (28801.02, 29584.91), (27049.07, 28038.49)
    W78G, W31G = (28805.0, 29580.0), (27050.0, 28035.0)
    grid = table(m78, m31, W78G, W31G)
    cont = table(m78, m31, W78C, W31C)
    v7 = {"smh2020": (0.294, 0.494, 0.047), "smh2020_parabola": (0.173, 0.641, 0.052),
          "smh2016_parabola": (0.498, 0.443, 0.108), "em2006_canon": (0.252, 0.412, 0.049),
          "mixture": (0.304, 0.498, 0.064)}
    v8 = {"smh2020": (0.297, 0.496, 0.051), "smh2020_parabola": (0.175, 0.643, 0.056),
          "smh2016_parabola": (0.503, 0.446, 0.113), "em2006_canon": (0.255, 0.414, 0.052),
          "mixture": (0.308, 0.500, 0.068)}
    out("\nR3-3: the 2.3 table (rounded to 0.001) against revision 7 (grid) and revision 8 (continuous)")
    bad7 = bad8 = 0
    for m in MODELS + ("mixture",):
        g = tuple(round(x, 3) for x in grid[m])
        c = tuple(round(x, 3) for x in cont[m])
        bad7 += sum(abs(a - b) > 1e-9 for a, b in zip(g, v7[m]))
        bad8 += sum(abs(a - b) > 1e-9 for a, b in zip(c, v8[m]))
        out(f"  {m:18s} grid {g} (v7 {v7[m]})   continuous {c} (v8 {v8[m]})")
    out(f"  cells differing from the printed table: revision 7 {bad7}, revision 8 {bad8}")
    out(f"  mixture P78 unrounded: grid {grid['mixture'][0]:.4f}, continuous {cont['mixture'][0]:.4f};"
        f" continuous - 0.304 = {cont['mixture'][0] - 0.304:.4f}")
    gap = max(abs(cont[m][0] - v7[m][0]) for m in MODELS + ("mixture",))
    out(f"  largest gap of revision 7's printed 1178 BC values to the continuous ones: {gap:.4f}")
    joints = [cont[m][2] for m in MODELS]
    out(f"  joints over the continuous windows: {min(joints):.3f}-{max(joints):.3f}; all > 0.05: "
        f"{all(j > 0.05 for j in joints)}")
    em = cont["em2006_canon"][0]
    out(f"  DE431-pairing mixture (0.299, 0.178, 0.505 with E-M {em:.3f}): {(0.299 + 0.178 + 0.505 + em) / 4:.3f}")

    out("\nR3-3: the I2(c) budget")
    for tol in (0.1, 0.01):
        out(f"  bisection to {tol} s at sigma 540.6: {bisect_bound(tol, 540.6):.2e} per boundary; "
            f"10^-4 holds for {max_boundaries(tol, 540.6)} boundaries")
    s_min78 = min(s for _m, _mu, s in m78)
    s_min31 = min(s for _m, _mu, s in m31)
    out(f"  smallest model sigma at -1176.68: {s_min78:.1f} s; at -1129.22: {s_min31:.1f} s "
        f"(10^-4 at 0.01 s holds for {max_boundaries(0.01, s_min31)} boundaries there)")
    for yy in (-500.0, 0.0, 300.0):
        # ephem's em2006_canon sigma is Huber's, 0 from -500 on; section 0 uses
        # Morrison-Stephenson 2004's 0.8 u^2 there, which is larger than SMH2020's
        s_min = min(positive_or_inf(float(E.delta_t_sigma(yy, m))) for m in MODELS)
        out(f"  smallest model sigma at {yy:+.0f}: {s_min:.0f} s -> 0.01 s bisection "
            f"{bisect_bound(0.01, s_min):.1e} per boundary; 10^-4 holds for "
            f"{max_boundaries(0.01, s_min)} boundaries")
    out(f"  a missed sub-step interval (10 s) at sigma 540.6: up to {10 * 1 / (540.6 * SQ2PI):.4f}")
    generic = 2 * 1.0 / (min(s_min78, s_min31) * SQ2PI)
    out(f"  window-independent bound for a 1-s error at both boundaries: {generic:.4f}; with rounding "
        f"0.0005 and 0.1-s bisection at both: {0.0005 + generic + 2 * bisect_bound(0.1, 540.6):.4f} "
        f"(tolerance 0.005)")
    spec = max(max(widen_change(mu, s, W78C), widen_change(mu, s, W78C, -1.0) * -1) for _m, mu, s in m78)
    out(f"  the design's 'at most 0.0011' for a 1-s change at both 1178 BC boundaries holds: {spec <= 0.00115}")

    out("\nR7 (joint bounds <= 0.06 for three models, >= 0.08 for SMH2016) under +-40 s")
    worst = {m: max(shifted_joints(m78, m31, W78C, W31C, d)[m] for d in range(-40, 41, 5)) for m in MODELS}
    least = min(shifted_joints(m78, m31, W78C, W31C, d)["smh2016_parabola"] for d in range(-40, 41, 5))
    # only booleans and the one value 14.7 states (the Addendum's 'at most 0.060') are printed
    out(f"  Addendum parabola's largest joint over the shifts rounds to {worst['smh2020_parabola']:.3f} "
        f"(14.7: at most 0.060)")
    out(f"  three models <= 0.06 at every shift: "
        f"{all(worst[m] <= 0.06 for m in MODELS if m != 'smh2016_parabola')}; SMH2016 >= 0.08 at every "
        f"shift: {least >= 0.08}")

    out("\nR3-2: what G_j,hi <= G_BM,u,lo allows (DESIGN 2.9 numbers)")
    n_t, n_a = 10690, 131
    g_u, g_u_lo = 0.140 * n_a / n_t, 0.087 * n_a / n_t
    out(f"  G_BM,u {g_u:.6f} = {g_u * n_t:.2f} units; G_BM,u,lo {g_u_lo:.6f} = {g_u_lo * n_t:.2f} units")
    out(f"  U0 = ff_upper([]) = {ff_upper([], n_t):.6f} = {ff_upper([], n_t) * n_t:.3f}/n")
    for k in (4, 5):
        out(f"  k = {k} at reach 1: Fay-Feuer {ff_upper([1.0] * k, n_t):.6f}, Poisson {poisson_upper(k, n_t):.6f}")
    out(f"  reach 1: at most {max_reached(1.0, g_u_lo, n_t)} targets")
    for r in (0.5, 0.1, 0.01, 0.001):
        k = max_reached(r, g_u_lo, n_t)
        out(f"  reach {r}: at most {k} targets = {k * r:.2f} units")
    out(f"  thin-spread supremum: {thin_limit_units(g_u_lo, n_t):.2f} units")
    shaped = max_units_shaped([1.0, 0.41], g_u_lo, n_t)
    out(f"  shaped like G_BM* (half at reach 1, the rest 0.41; mean {(13 + 13 * 0.41) / 26:.2f}, "
        f"18.3/26 = {0.140 * 131 / 26:.2f}): at most {shaped:.2f} units; "
        f"G_BM* reaches {g_u * n_t:.1f}, ratio {g_u * n_t / shaped:.1f} (reach-1 ratio {g_u * n_t / 4:.1f})")

    out("\nR3-1 / R3-4 / R3-7: the recheck's recorded narrowing, revision 8's projection")
    runs = json.load(open(NARROW_JSON, encoding="utf-8"))
    out(f"  windows start {[w['start_year'] for w in runs.values()]}, 5% line {line_days(runs)} days")
    for s, key in V8_KEYS.items():
        (f0, f1), (d0, d1) = frac_range(runs, key)
        out(f"  {s}: {100 * f0:.2f}-{100 * f1:.2f}%  days {d0}-{d1}  margin to 5%: "
            f"{100 * (0.05 - f1):+.2f} to {100 * (0.05 - f0):+.2f} points")
    for key in ("ALM-A (A.2 only none) [frozen, inferred phases none]",
                "ALM-A (A.5 only none) [frozen, inferred phases none]",
                "ALM-A (civil dawn for A.9) [frozen, inferred phases none]",
                "ALM-A (same_app & visible)", "ALM-B (same_app & visible)", "ALM-B"):
        (f0, f1), _d = frac_range(runs, key)
        out(f"  {key}: {100 * f0:.2f}-{100 * f1:.2f}%")
    b_with = [w["sets"]["ALM-B (same_app & visible)"]["n_pass"] for w in runs.values()]
    b_without = [w["sets"]["ALM-B [frozen, inferred phases none]"]["n_pass"] for w in runs.values()]
    out(f"  ALM-B day counts with and without B.2 identical: {b_with == b_without}")
    for w in runs.values():
        out(f"  window {w['start_year']}..{w['start_year'] + 136}: before -1000 entirely: "
            f"{w['start_year'] + 136 <= -1000}; partly: {w['start_year'] < -1000}")

    out("\nR3-1: the moon-phase rows of the clue file")
    clues = json.load(open(CLUE_FILE, encoding="utf-8"))["clues"]
    rows = phase_rows(clues)
    for k in sorted(rows):
        p, j, nj, opts = rows[k]
        out(f"  {k}: primary {p}; 'inference' in its justification: {'inference' in j}; "
            f"none option: {nj!r}")
    out(f"  rows whose own 'none' says not stated in words: {words_only_none(rows)}")

    out("\nNew-blocker scan: where 'ALM-B ... knife-edge' and 'nearly determined by known numbers' sit")
    phrases = ("ALM-B the knife-edge", "ALM-B is the knife-edge", "nearly determined by known numbers",
               "P21 nearly determined")
    for name in ("docs/DESIGN-v7.md", "DESIGN.md"):
        text = open(ROOT + "/" + name, encoding="utf-8").read()
        out(f"  {name}: {phrase_lines(text, phrases)}")


def selftest(out=print):
    """synthetic data only: every function on hand-built cases"""
    assert abs(Phi(0.0) - 0.5) < 1e-12 and abs(phi(0.0) - 1 / SQ2PI) < 1e-12
    assert abs(p_window(0.0, 1.0, -1.96, 1.96) - 0.95) < 1e-3
    assert p_window(0.0, 1.0, 1.0, 1.0) == 0.0
    assert abs(joint_common_offset(0.0, 1.0, (-1.0, 1.0), 10.0, (10.0, 12.0)) - (Phi(1.0) - 0.5)) < 1e-12
    assert joint_common_offset(0.0, 1.0, (-1.0, 0.0), 0.0, (0.5, 1.0)) == 0.0
    assert abs(ndot_shift(1955.0)) < 1e-12 and ndot_shift(-1176.68) > 33.9
    fake_dt = lambda y, m: {"smh2020": 100.0, "smh2020_parabola": 200.0,
                            "smh2016_parabola": 300.0, "em2006_canon": 400.0}[m]
    fake_s = lambda y, m: 50.0
    ms = models_at(1955.0, fake_dt, fake_s)
    assert [round(mu) for _m, mu, _s in ms] == [100, 200, 300, 400]
    t = table(ms, ms, (-10000.0, 10000.0), (-10000.0, 10000.0))
    assert abs(t["mixture"][0] - 1.0) < 1e-9 and abs(t["mixture"][2] - 1.0) < 1e-9
    t2 = table(ms, ms, (0.0, 1000.0), (0.0, 1000.0))
    assert abs(t2["smh2020"][0] - (Phi(18.0) - Phi(-2.0))) < 1e-12
    assert abs(bisect_bound(0.1, 540.6) - 7.38e-5) < 1e-7 and max_boundaries(0.01, 540.6) == 13
    assert positive_or_inf(0.0) == float("inf") and positive_or_inf(5.0) == 5.0
    assert abs(widen_change(0.0, 1.0, (-1.0, 1.0), 0.0)) < 1e-15
    sj = shifted_joints(ms, ms, (0.0, 1000.0), (0.0, 1000.0), 0.0)
    assert abs(sj["smh2020"] - (Phi(18.0) - Phi(-2.0))) < 1e-9
    assert abs(ff_upper([], 1000) * 1000 - 3.689) < 1e-3
    assert abs(ff_upper([1.0] * 3, 1000) - poisson_upper(3, 1000)) < 1e-12
    assert max_reached(1.0, poisson_upper(4, 1000) + 1e-12, 1000) == 4
    assert max_units_shaped([1.0], poisson_upper(2, 1000) + 1e-12, 1000) == 2.0
    u = thin_limit_units(10.0 / 1000, 1000)
    assert 6.0 < u < 7.5
    runs = {"w1": {"start_year": 0, "n_cand": 100, "sets": {"X": {"n_pass": 4, "n_cand": 100}}},
            "w2": {"start_year": 200, "n_cand": 100, "sets": {"X": {"n_pass": 6, "n_cand": 100}}}}
    assert frac_range(runs, "X") == ((0.04, 0.06), (4, 6)) and line_days(runs) == [5]
    clues = [{"clue_id": "S.1", "kind": "moon-phase", "fork_options": [
        {"option": "phase_class", "primary": True, "justification": "my inference"},
        {"option": "none", "primary": False, "justification": "the Moon's phase is not stated in words"}]},
        {"clue_id": "S.2", "kind": "moon-phase", "fork_options": [
            {"option": "phase_class", "primary": True, "justification": "the words"}]},
        {"clue_id": "S.3", "kind": "planet", "fork_options": []}]
    r = phase_rows(clues)
    assert set(r) == {"S.1", "S.2"} and words_only_none(r) == ["S.1"]
    doc = "a knife\nX the knife-edge\n" + MARKER + " cut -->\nX the knife-edge\n"
    assert phrase_lines(doc, ("X the knife-edge",)) == [(2, "public", "X the knife-edge"),
                                                       (4, "AppT", "X the knife-edge")]
    out("selftest: all synthetic cases pass")
    return True


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    else:
        check()
