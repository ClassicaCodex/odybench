"""
Tests of odybench/lean/reach.py (DESIGN 5.3; instrument check I9(a) of
LEAN.md).  Synthetic data only.

    cd C:\\Projects\\odybench && py tests/test_lean_reach.py

I9(a): reach against brute-force sliding windows on 10,000 synthetic survivor
sets, tolerance 0.0002.  Two brute forces, neither of which uses the interval
formula of 5.3:
  * the exact sweep: every distinct window position class between
    consecutive breakpoints (a survivor entering or leaving the window) is
    tested at its midpoint by counting each reading's survivors in [a, a + W)
    directly; all 10,000 sets;
  * a plain grid of window starts (200,000 positions over [t - W, t)) on 200
    of the sets, whose discretisation error is below 1e-4.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from odybench.lean import reach as R  # noqa: E402

TOL = 0.0002


def _seed(purpose, key):
    s = json.loads((ROOT / "data" / "prereg" / "seeds.json").read_text(encoding="utf-8"))
    return s["purposes"][purpose]["seeds"][key]


def synthetic_set(rng):
    """(t, survivor sets, W): R readings with survivors drawn around t at
    random rates, t in some sets and not in others."""
    W = float(rng.choice([1.0, 136 * 365.25, 50.0, 7.3]))
    nr = int(rng.integers(1, 7))
    t = float(rng.uniform(-5, 5) * W)
    sets = []
    for _ in range(nr):
        rate = rng.uniform(0.2, 4.0) / W
        span = 6 * W
        k = rng.poisson(rate * span)
        S = t + rng.uniform(-3 * W, 3 * W, size=k)
        if rng.random() < 0.75:
            S = np.append(S, t)
        if rng.random() < 0.1 and S.size:                  # a neighbour exactly W away
            S = np.append(S, t + W * rng.choice([-1, 1]))
        sets.append(np.sort(S))
    return t, sets, W


def brute_sweep(t, sets, W):
    pts = [t - W, t]
    for S in sets:
        near = S[(S > t - 2 * W - 1e-9) & (S < t + 2 * W + 1e-9)]
        pts.extend(near - W)
        pts.extend(near)
    pts = np.unique(np.clip(np.array(pts), t - W, t))
    if pts.size < 2:
        return 0.0
    mids = 0.5 * (pts[:-1] + pts[1:])
    lens = np.diff(pts)
    hit = np.zeros(mids.size, dtype=bool)
    for S in sets:
        if not np.any(S == t):
            continue
        cnt = np.searchsorted(S, mids + W, side="left") - np.searchsorted(S, mids, side="left")
        inside_t = (mids <= t) & (t < mids + W)
        hit |= (cnt == 1) & inside_t
    return float(lens[hit].sum() / W)


def brute_grid(t, sets, W, n=200000):
    a = t - W + (np.arange(n) + 0.5) * (W / n)
    hit = np.zeros(n, dtype=bool)
    for S in sets:
        if not np.any(S == t):
            continue
        cnt = np.searchsorted(S, a + W, side="left") - np.searchsorted(S, a, side="left")
        hit |= cnt == 1
    return float(hit.mean())


def test_I9a_reach_vs_bruteforce_10000():
    rng = np.random.default_rng(_seed("I9_synthetic", "reach_10000"))
    worst = 0.0
    n_pos = 0
    for k in range(10000):
        t, sets, W = synthetic_set(rng)
        r = float(R.reach([t], sets, W)[0])
        b = brute_sweep(t, sets, W)
        worst = max(worst, abs(r - b))
        n_pos += r > 0
        assert abs(r - b) <= TOL, (k, r, b, W)
    assert n_pos > 3000, n_pos                      # the sets exercise nonzero reach
    print(f"    I9(a) exact sweep: 10,000 sets, max |reach - brute| = {worst:.2e}, nonzero {n_pos}")


def test_I9a_reach_vs_grid_slide():
    rng = np.random.default_rng(_seed("I9_synthetic", "reach_10000") + 1)
    worst = 0.0
    for k in range(200):
        t, sets, W = synthetic_set(rng)
        r = float(R.reach([t], sets, W)[0])
        b = brute_grid(t, sets, W)
        worst = max(worst, abs(r - b))
        assert abs(r - b) <= TOL, (k, r, b)
    print(f"    I9(a) grid slide: 200 sets, max |reach - grid| = {worst:.2e}")


def test_reach_many_targets_matches_single():
    rng = np.random.default_rng(3)
    W = 136 * 365.25
    sets = [np.sort(rng.uniform(0, 2200 * 365.25, rng.integers(20, 200))) for _ in range(36)]
    targets = np.unique(np.concatenate([s[rng.random(s.size) < 0.3] for s in sets] + [rng.uniform(0, 8e5, 50)]))
    many = R.reach(targets, sets, W)
    one = np.array([R.reach([x], sets, W)[0] for x in targets])
    assert np.allclose(many, one, atol=1e-14)
    # readings.survivors() yields (index, array) pairs: accepted too
    pairs = [(i, s) for i, s in enumerate(sets)]
    assert np.allclose(R.reach(targets, pairs, W), many)


def test_interval_formula_cases():
    W = 10.0
    assert R.interval(5.0, -np.inf, np.inf, W) == (-5.0, 5.0)
    lo, hi = R.interval(5.0, 2.0, 12.0, W)          # (max(-5, 2), min(5, 2)] = empty
    assert hi <= lo
    assert abs(R.reach([11 * 365.25], [np.array([0.0, 11 * 365.25])], 136 * 365.25)[0] - 11 / 136) < 1e-12


def test_gamma_interval_special_cases():
    for n in (10, 100, 892):
        y, lo, hi = R.gamma_interval(np.zeros(n))
        assert y == 0 and lo == 0 and abs(hi - 3.689 / n) < 2e-3 / n and abs(hi - R.U0(n)) < 1e-15
        for k in (1, 3, min(20, n)):
            v = np.zeros(n)
            v[:k] = 1.0
            y, lo, hi = R.gamma_interval(v)
            _, plo, phi = R.poisson_rate(k, n)
            assert abs(lo - plo) < 1e-12 and abs(hi - phi) < 1e-12, (n, k)


def test_gamma_interval_coverage_simulation():
    """Coverage of the gamma interval for independent reaches (I9 checks the
    formula by simulation; the dependent case is I9(b), not run here)."""
    rng = np.random.default_rng(11)
    n, p = 400, 0.06
    true = p * 0.5
    cover = 0
    for _ in range(2000):
        hit = rng.random(n) < p
        r = np.where(hit, rng.random(n), 0.0)
        _, lo, hi = R.gamma_interval(r)
        cover += lo <= true <= hi
    assert cover / 2000 >= 0.93, cover / 2000


def test_block_bootstrap():
    rng = np.random.default_rng(5)
    yrs = rng.integers(-1748, -50, 1000)
    r = np.where(rng.random(1000) < 0.1, rng.random(1000), 0.0)
    lo, hi, g = R.block_bootstrap(r, yrs, (-1748, -51), 136, 4000, 9)
    assert lo < r.mean() < hi and g.size == 4000
    # every draw spans exactly the core's length: a constant reach gives a constant G
    lo2, hi2, g2 = R.block_bootstrap(np.full(1000, 0.25), yrs, (-1748, -51), 136, 500, 9)
    assert np.allclose(g2, 0.25)
    G = R.G(r, yrs, (-1748, -51), n_boot=1000, seeds=(1, 2))
    assert G["lo"] == min(G["lo_gamma"], G["lo_boot"]) and G["hi"] == max(G["hi_gamma"], G["hi_boot"])


def test_p_at_least_one_bruteforce():
    rng = np.random.default_rng(8)
    S = np.sort(rng.uniform(0, 2200 * 365.25, 40))
    for Wy in (50, 136, 900):
        W = Wy * 365.25
        e, p, m = R.p_at_least_one(S, W, 0.0, 2200 * 365.25)
        starts = np.arange(0, 2200 * 365.25 - W + 1e-6, 365.25)
        c = np.array([np.sum((S >= a) & (S < a + W)) for a in starts])
        assert abs(e - np.mean(c >= 1)) < 1e-12 and abs(m - c.mean()) < 1e-12
        assert abs(p - (1 - math.exp(-40 / (2200 * 365.25) * W))) < 1e-12


if __name__ == "__main__":
    import time
    fails = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            t0 = time.time()
            try:
                fn()
                print(f"PASS {name} ({time.time() - t0:.1f} s)")
            except Exception as exc:          # noqa: BLE001
                fails += 1
                print(f"FAIL {name}: {exc!r}")
    print("all passed" if not fails else f"{fails} failed")
    sys.exit(1 if fails else 0)
