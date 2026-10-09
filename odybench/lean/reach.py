"""
odybench.lean.reach -- reach, G with its interval, and P(>= 1 survivor) per
window width (DESIGN 5.3, 5.1 item 5, 5.5; I9(a) in tests/test_lean_reach.py).

reach.  For a reading r with survivors S_r (sorted instants), a target
t in S_r is the unique survivor of a W-wide window [a, a + W) placed at a
uniformly random start a with t inside exactly when the window misses the
neighbouring survivors s- and s+:

    a in I_r(t) = (max(t - W, s-), min(t, s+ - W)]        (empty if t not in S_r)

reach_W(t; G) = |union over r in G of I_r(t)| / W.  Instants are JD_TT of the
conjunctions (10.2: readings.survivors yields JD_TT), W = 365.25 x years.

G(G; P; W) = the mean of reach over the targets of P (16 Apr -1177 excluded
upstream, by the masked pool).  Its interval is the wider of

  * the 95% gamma interval of Fay & Feuer (1997) for a weighted sum of
    counts: y = G, v = sum (reach/n)^2, w = 1/n (the largest possible
    weight),
        G_hi = ((v + w^2) / (2 (y + w))) chi2_0.975(2 (y + w)^2 / (v + w^2))
        G_lo = (v / (2 y)) chi2_0.025(2 y^2 / v),   0 when y = 0
    (DESIGN gives it from memory.  It is the standard statement of Fay &
    Feuer's gamma interval (Stat. Med. 16:791, 1997), as implemented e.g.
    in R's dsrTest/epitools: lower G^-1(alpha/2; shape y^2/v, scale v/y),
    upper G^-1(1 - alpha/2; (y + w_M)^2/(v + w_M^2), (v + w_M^2)/(y + w_M)),
    with G^-1(p; shape, scale) = (scale/2) chi2_p(2 shape) -- identical to
    DESIGN's text with w_M = w = 1/n.  The paper itself was not re-read
    here.  With no target reached G_hi = 3.69/n, and with every nonzero
    reach 1 it is the exact Poisson interval: both are tested);
  * a moving-block bootstrap over the core: blocks of `block_years`
    consecutive Day-0 years (136; 243 reported), drawn with replacement, the
    last truncated so that a resample spans the core's length, 10,000
    resamples, percentile interval.
The rule's [G_lo, G_hi] takes the smaller lower and the larger upper bound.
"""
from __future__ import annotations

import math
import sys

import numpy as np
from scipy.stats import chi2

YEAR_D = 365.25


# ----------------------------------------------------------------- reach

def interval(t, s_prev, s_next, W_days):
    """(lo, hi) of I_r(t) = (max(t - W, s-), min(t, s+ - W)]; empty if lo >= hi.
    s_prev = -inf / s_next = +inf when t has no neighbour on that side."""
    return max(t - W_days, s_prev), min(t, s_next - W_days)


def _union_length(lo, hi):
    o = np.argsort(lo, kind="stable")
    lo, hi = lo[o], hi[o]
    tot, cl, ch = 0.0, lo[0], hi[0]
    for a, b in zip(lo[1:], hi[1:]):
        if a > ch:
            tot += ch - cl
            cl, ch = a, b
        elif b > ch:
            ch = b
    return tot + (ch - cl)


def intervals(targets, survivor_sets, W_days, eps=1e-6):
    """All nonempty I_r(t): arrays (target index, lo, hi).  survivor_sets is an
    iterable of sorted survivor arrays (or (index, array) pairs, as
    readings.survivors yields).  A target belongs to S_r if a survivor lies
    within eps days of it."""
    t = np.asarray(targets, dtype=float)
    ti, los, his = [], [], []
    for S in survivor_sets:
        if isinstance(S, tuple):
            S = S[1]
        S = np.asarray(S, dtype=float)
        if S.size == 0 or t.size == 0:
            continue
        k = np.searchsorted(S, t - eps)
        kk = np.clip(k, 0, S.size - 1)
        member = (k < S.size) & (np.abs(S[kk] - t) <= eps)
        if not member.any():
            continue
        idx = np.nonzero(member)[0]
        kk = kk[idx]
        sp = np.where(kk > 0, S[np.clip(kk - 1, 0, None)], -np.inf)
        sn = np.where(kk + 1 < S.size, S[np.clip(kk + 1, None, S.size - 1)], np.inf)
        tt = t[idx]
        lo = np.maximum(tt - W_days, sp)
        hi = np.minimum(tt, sn - W_days)
        ok = hi > lo
        ti.append(idx[ok])
        los.append(lo[ok])
        his.append(hi[ok])
    if not ti:
        return np.zeros(0, dtype=np.int64), np.zeros(0), np.zeros(0)
    return np.concatenate(ti), np.concatenate(los), np.concatenate(his)


def reach(targets, survivor_sets, W_days):
    """f8[m]: reach_W of each target, |union of I_r(t)| / W."""
    t = np.atleast_1d(np.asarray(targets, dtype=float))
    out = np.zeros(t.size)
    ti, lo, hi = intervals(t, survivor_sets, W_days)
    if ti.size == 0:
        return out
    o = np.argsort(ti, kind="stable")
    ti, lo, hi = ti[o], lo[o], hi[o]
    br = np.nonzero(np.diff(ti))[0] + 1
    for a, b in zip(np.concatenate(([0], br)), np.concatenate((br, [ti.size]))):
        out[ti[a]] = _union_length(lo[a:b], hi[a:b]) / W_days
    return out


def reach_max(targets, survivor_sets_by_width: dict, years=(136,)):
    """reach(t) = max over W of reach_W(t) (5.3, gardens of several widths)."""
    return np.max(np.vstack([reach(targets, survivor_sets_by_width[w], w * YEAR_D) for w in years]), axis=0)


# ---------------------------------------------------------------- G

def gamma_interval(reach_values, alpha=0.05):
    """(G, G_lo, G_hi): the Fay-Feuer gamma interval of DESIGN 5.3 over a
    pool of n = len(reach_values) targets (zeros included)."""
    r = np.asarray(reach_values, dtype=float)
    n = r.size
    if n == 0:
        return float("nan"), float("nan"), float("nan")
    y = r.sum() / n
    v = float(np.sum((r / n) ** 2))
    w = 1.0 / n
    hi = (v + w * w) / (2.0 * (y + w)) * chi2.ppf(1 - alpha / 2, 2.0 * (y + w) ** 2 / (v + w * w))
    lo = 0.0 if y == 0 else v / (2.0 * y) * chi2.ppf(alpha / 2, 2.0 * y * y / v)
    return float(y), float(lo), float(hi)


def block_bootstrap(reach_values, target_years, span, block_years=136, n_boot=10000, seed=0,
                    alpha=0.05):
    """Percentile interval (lo, hi) of G by a moving-block bootstrap over the
    years `span` = (y0, y1) inclusive, with the resampled G of each draw."""
    r = np.asarray(reach_values, dtype=float)
    yrs = np.asarray(target_years, dtype=np.int64)
    y0, y1 = int(span[0]), int(span[1])
    L = y1 - y0 + 1
    if not np.all((yrs >= y0) & (yrs <= y1)):
        raise ValueError("targets outside the bootstrap span")
    B = min(int(block_years), L)
    s_y = np.bincount(yrs - y0, weights=r, minlength=L)
    n_y = np.bincount(yrs - y0, minlength=L).astype(float)
    cs = np.concatenate(([0.0], np.cumsum(s_y)))
    cn = np.concatenate(([0.0], np.cumsum(n_y)))
    nb = int(math.ceil(L / B))
    lens = np.full(nb, B)
    lens[-1] = L - B * (nb - 1)
    rng = np.random.default_rng(seed)
    starts = rng.integers(0, L - B + 1, size=(n_boot, nb))
    ends = starts + lens[None, :]
    tot_s = (cs[ends] - cs[starts]).sum(axis=1)
    tot_n = (cn[ends] - cn[starts]).sum(axis=1)
    g = np.where(tot_n > 0, tot_s / np.maximum(tot_n, 1), 0.0)
    lo, hi = np.quantile(g, [alpha / 2, 1 - alpha / 2])
    return float(lo), float(hi), g


def G(reach_values, target_years, span, *, garden="G_BM*", pool="T_A", slot=None, widths=(136,),
      n_boot=10000, seeds=(0, 0), block_years=(136, 243), masked=True):
    """G with its interval (5.3).  Returns a dict with the GStat fields
    (value, lo, hi, n, k, garden, pool, slot, widths, lo_gamma, hi_gamma,
    lo_boot, hi_boot, masked) plus lo_boot243, hi_boot243 (reported) and
    G_any = k/n."""
    r = np.asarray(reach_values, dtype=float)
    y, lo_g, hi_g = gamma_interval(r)
    lo_b, hi_b, _ = block_bootstrap(r, target_years, span, block_years[0], n_boot, seeds[0])
    lo_b2, hi_b2, _ = block_bootstrap(r, target_years, span, block_years[1], n_boot, seeds[1])
    n = int(r.size)
    k = int(np.sum(r > 0))
    return dict(value=y, lo=min(lo_g, lo_b), hi=max(hi_g, hi_b), n=n, k=k, garden=garden, pool=pool,
                slot=slot, widths=list(widths), lo_gamma=lo_g, hi_gamma=hi_g, lo_boot=lo_b, hi_boot=hi_b,
                lo_boot243=lo_b2, hi_boot243=hi_b2, masked=bool(masked),
                G_any=(k / n if n else float("nan")))


def U0(n):
    """The gamma upper bound of a G with no target reached, 3.69/n (9.2)."""
    return 0.5 * chi2.ppf(0.975, 2.0) / n


# ------------------------------------------------------- windows, rates

def poisson_rate(k, exposure, alpha=0.05):
    """(rate, lo, hi): k events over `exposure` units, exact (Garwood) interval."""
    lo = 0.0 if k == 0 else 0.5 * chi2.ppf(alpha / 2, 2 * k)
    hi = 0.5 * chi2.ppf(1 - alpha / 2, 2 * k + 2)
    return k / exposure, lo / exposure, hi / exposure


def window_counts(survivors, W_days, b0, b1, step_days=YEAR_D):
    """Counts of survivors in every half-open window [a, a + W) with a = b0,
    b0 + step, ... and a + W <= b1."""
    S = np.sort(np.asarray(survivors, dtype=float))
    nwin = int(math.floor((b1 - b0 - W_days) / step_days + 1e-9)) + 1
    if nwin <= 0:
        return np.zeros(0, dtype=np.int64)
    a = b0 + step_days * np.arange(nwin)
    return np.searchsorted(S, a + W_days, side="left") - np.searchsorted(S, a, side="left")


def p_at_least_one(survivors, W_days, b0, b1, step_days=YEAR_D):
    """(empirical P(>= 1), Poisson P(>= 1), mean count) over windows of width
    W slid one step at a time along [b0, b1) (5.1 item 5).  The Poisson value
    is 1 - exp(-lambda W), lambda the survivors per day over [b0, b1)."""
    S = np.asarray(survivors, dtype=float)
    c = window_counts(S, W_days, b0, b1, step_days)
    lam = np.sum((S >= b0) & (S < b1)) / (b1 - b0)
    if c.size == 0:
        return float("nan"), float(1 - math.exp(-lam * W_days)), float("nan")
    return float(np.mean(c >= 1)), float(1 - math.exp(-lam * W_days)), float(c.mean())


def _selftest():
    rng = np.random.default_rng(7)
    W = 136 * YEAR_D
    # a lone survivor: reach 1
    assert abs(reach([0.0], [np.array([0.0])], W)[0] - 1.0) < 1e-12
    # two survivors 11 years apart: the later one's reach is 11/136
    r = reach([11 * YEAR_D], [np.array([0.0, 11 * YEAR_D])], W)[0]
    assert abs(r - 11 / 136) < 1e-12, r
    # union over readings
    r = reach([0.0], [np.array([-10.0, 0.0]), np.array([0.0, 20.0])], 100.0)[0]
    assert abs(r - (10 + 20) / 100.0) < 1e-12, r
    # gamma interval: no target reached -> 3.69/n; all reaches 1 -> exact Poisson
    n = 100
    y, lo, hi = gamma_interval(np.zeros(n))
    assert y == 0 and lo == 0 and abs(hi - U0(n)) < 1e-12 and abs(hi * n - 3.689) < 1e-3
    vals = np.zeros(n); vals[:5] = 1.0
    y, lo, hi = gamma_interval(vals)
    _, plo, phi = poisson_rate(5, n)
    assert abs(lo - plo) < 1e-12 and abs(hi - phi) < 1e-12
    # bootstrap brackets the mean on a stationary synthetic core
    yrs = rng.integers(-1748, -50, 900)
    rv = np.where(rng.random(900) < 0.1, rng.random(900), 0.0)
    g = G(rv, yrs, (-1748, -51), n_boot=2000, seeds=(1, 2))
    assert g["lo"] <= g["value"] <= g["hi"], g
    # P(>= 1): survivors every 100 years, windows of 50 years -> 0.5
    S = np.arange(0, 2200, 100) * YEAR_D
    e, p, m = p_at_least_one(S, 50 * YEAR_D, 0.0, 2200 * YEAR_D)
    assert abs(e - 0.5) < 0.02 and abs(m - 0.5) < 0.02, (e, m)
    print(f"[reach selftest] G {g['value']:.4f} [{g['lo']:.4f}, {g['hi']:.4f}] gamma "
          f"[{g['lo_gamma']:.4f}, {g['hi_gamma']:.4f}] boot [{g['lo_boot']:.4f}, {g['hi_boot']:.4f}]")
    print("[reach selftest] PASS")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        _selftest()
    else:
        print(__doc__)
