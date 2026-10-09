"""
odybench.lean.readings -- the 36 readings of G_BM* and the T0b reading
(DESIGN 5.3, 4.2, 7.2; LEAN.md "N3 (part)").

G_BM* holds, with F2 = (a) (Day 0 the UT+2 conjunction date), F3 = (a') C_rel,
F4 = Venus rising >= 90 min before the Sun, F6 off and F7 = 136 years:

  F1 day count   sequential (C -29/-12, V -5, M -34) or parallel (-28/-11, -4, -33)
  F5 Mercury     event in {rise-azimuth maximum (vertex, morning), greatest
                 western elongation, morning station}
                 x tolerance {1.5, 2.5, 3.5} d (continuous: B&M's 1, 2, 3
                 integer days) x visibility (AV 10 deg: the Sun at or below
                 -10 deg at Mercury's rising) required or not

2 x 18 = 36 readings.  A Mercury event passes if its instant lies within the
tolerance of Mercury's rising instant on the count's Mercury day (5.3: "a
vertex or event instant is compared with the stated day's instant").  The
T0b reading (in its C_rel form, visibility off, F6 off) is the member
(seq, mwra, 1.5, off) [rev #23].

A reading's pass array over a pool requires C on that count, the Venus lead
on that count's Venus day and the Mercury event on that count's Mercury day.
The pool's columns come from odybench.lean.candidates (or its synthetic()).
Every function calls pool.guard() first, so a masked pool that holds
16 Apr -1177 raises TargetMasked.
"""
from __future__ import annotations

import sys
from typing import NamedTuple

import numpy as np

from odybench.lean import TargetMasked
from odybench.lean.candidates import COUNTS

EVENTS = ("mwra", "gwe", "station")
TOLS = (1.5, 2.5, 3.5)
EVENT_COL = {"mwra": "d_mwra", "gwe": "d_gwe", "station": "d_sta",
             "mwra_any": "d_mwra_any"}     # reported only: the maximum whatever Mercury's side (T0b's literal MWRA)
VENUS_LEAD_MIN = 90.0               # F4, BM tier [B&M References; bm 5 V]
MERC_VIS_SUN_ALT = -10.0            # AV 10 deg [vis 2.2]


class Reading(NamedTuple):
    count: str          # 'seq' | 'par'
    event: str          # 'mwra' | 'gwe' | 'station'
    tol: float          # days, continuous
    vis: bool           # Mercury visible (AV 10) required

    @property
    def key(self):
        return f"{self.count}/{self.event}/{self.tol:g}/{'vis' if self.vis else 'novis'}"


READINGS = tuple(Reading(c, e, t, v) for c in ("seq", "par") for e in EVENTS
                 for t in TOLS for v in (False, True))
T0B = Reading("seq", "mwra", 1.5, False)
T0B_INDEX = READINGS.index(T0B)
MWRA_INDICES = tuple(i for i, r in enumerate(READINGS) if r.event == "mwra")
assert len(READINGS) == 36 and len(MWRA_INDICES) == 12


def garden(tier="BM"):
    """The rule garden G_BM* (F6 off).  Only tier BM is built in the lean run."""
    if tier != "BM":
        raise NotImplementedError("the lean run builds only G_BM* (LEAN.md 'What is deferred')")
    return READINGS


def pinned(name):
    """'T0b' -> the T0b reading."""
    if name in ("T0b", "BM"):
        return T0B
    raise KeyError(name)


# ------------------------------------------------------------ predicates

def C(pool, count, kind="rel"):
    pool.guard("C")
    return pool.cols[f"c_{kind}_{count}"]


def V(pool, count, lead_min=VENUS_LEAD_MIN):
    """Venus rises at least lead_min minutes before the Sun on the count's Venus day."""
    pool.guard("V")
    return pool.cols[f"lead_m{-COUNTS[count]['v']}"] >= lead_min


def M(pool, count, event="mwra", tol=1.5, vis=False):
    """A morning Mercury event within tol days of Mercury's rising instant on
    the count's Mercury day (and Mercury visible at AV 10 if vis)."""
    pool.guard("M")
    o = -COUNTS[count]["m"]
    p = pool.cols[f"{EVENT_COL[event]}_m{o}"] <= tol
    if vis:
        p = p & (pool.cols[f"msun_m{o}"] <= MERC_VIS_SUN_ALT)
    return p


def mercury_visible(pool, count):
    pool.guard("mercury_visible")
    return pool.cols[f"msun_m{-COUNTS[count]['m']}"] <= MERC_VIS_SUN_ALT


def passes_one(pool, r: Reading, c_kind="rel"):
    """bool[n]: the pool's candidates passing reading r."""
    return C(pool, r.count, c_kind) & V(pool, r.count) & M(pool, r.count, r.event, r.tol, r.vis)


def passes(pool, readings=READINGS, c_kind="rel"):
    """bool[R, n]: the pass array of each reading over the pool."""
    pool.guard("readings.passes")
    return np.vstack([passes_one(pool, r, c_kind) for r in readings]) if readings else \
        np.zeros((0, len(pool)), dtype=bool)


def survivors(pool, readings=READINGS, c_kind="rel", pass_array=None):
    """[(reading index, f8[k] survivor JD_TT, sorted)] over the pool."""
    pa = passes(pool, readings, c_kind) if pass_array is None else pass_array
    jt = pool.jd_tt
    return [(i, np.sort(jt[pa[i]])) for i in range(pa.shape[0])]


def bm_reading(pool, c_kind="rel", e_n=None, e_kind="rel", count="seq", tol=1.5, event="mwra",
               vis=False, e_func=None):
    """B&M's applied criteria (N1, DESIGN 5.1 item 1): N (every pool member is a
    conjunction), C (C_rel or fixed), V (lead >= 90 min), M (MWRA vertex within
    tol), and E if e_n is given (E_rel or fixed, n = 3, 4, 5)."""
    p = C(pool, count, c_kind) & V(pool, count) & M(pool, count, event, tol, vis)
    if e_n is not None:
        from odybench.lean.candidates import e_flags
        p = p & (e_func or e_flags)(pool, e_n, e_kind, count)
    return p


def membership(pool, pass_array=None):
    """Members of the held-out pools' parents (DESIGN 4.2, 7.2):

    P_BM   candidates passing at least one of the 36 readings;
    P_MWRA candidates passing at least one of the 12 MWRA readings.

    Returns dict(pass_array bool[36, n], P_BM bool[n], P_MWRA bool[n],
    bm_seq/bm_par: passes some reading on that count; mwra_seq/mwra_par: some
    MWRA reading on that count; bits: uint64[n], bit i set if reading i passes)."""
    pa = passes(pool) if pass_array is None else pass_array
    seq = np.array([r.count == "seq" for r in READINGS])
    mw = np.array([r.event == "mwra" for r in READINGS])
    bits = np.zeros(pa.shape[1], dtype=np.uint64)
    for i in range(pa.shape[0]):
        bits |= pa[i].astype(np.uint64) << np.uint64(i)
    return dict(pass_array=pa, P_BM=pa.any(axis=0), P_MWRA=pa[mw].any(axis=0),
                bm_seq=pa[seq].any(axis=0), bm_par=pa[~seq].any(axis=0),
                mwra_seq=pa[mw & seq].any(axis=0), mwra_par=pa[mw & ~seq].any(axis=0), bits=bits)


def _selftest():
    from odybench.lean import candidates as Cn
    p = Cn.synthetic(seed=5)
    pa = passes(p)
    assert pa.shape == (36, len(p))
    # nesting: a wider tolerance passes a superset; visibility a subset
    for i, r in enumerate(READINGS):
        if r.tol < 3.5:
            j = READINGS.index(r._replace(tol=TOLS[TOLS.index(r.tol) + 1]))
            assert np.all(pa[j][pa[i]]), r
        if r.vis:
            j = READINGS.index(r._replace(vis=False))
            assert np.all(pa[j][pa[i]]), r
    # the identity of DESIGN 4.2: no reading passes a candidate outside T_A(v) for v1..v5
    reached = pa.any(axis=0)
    for v in ("v1", "v2", "v3", "v4", "v5"):
        sl = Cn.slot_A(p, v)
        # synthetic Venus columns respect lead >= 90 -> Sun <= -7, so the identity must hold
        assert not np.any(reached & ~sl), v
    m = membership(p, pa)
    assert np.all(m["P_BM"][m["P_MWRA"]])
    print(f"[readings selftest] P_BM {int(m['P_BM'].sum())}, P_MWRA {int(m['P_MWRA'].sum())}, "
          f"T0b survivors {int(pa[T0B_INDEX].sum())} of {len(p)}")
    pu = Cn.synthetic(seed=5, mask_target=False)
    if np.any(pu.day0 == 1291264):
        pu.masked = True
        try:
            passes(pu)
        except TargetMasked:
            pass
        else:
            raise AssertionError("TargetMasked not raised")
    print("[readings selftest] PASS")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        _selftest()
    else:
        for i, r in enumerate(READINGS):
            print(i, r.key, "(T0b)" if r == T0B else "")
