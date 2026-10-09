"""
odybench.lean -- the lean run of LEAN.md (amendment 1 to DESIGN.md revision 8).

Every definition is DESIGN.md revision 8's, in the section each module names.
This package holds only the modules of the lean run:

  sky.py         rise/set, azimuths, elongations, Mercury events, C_rel, equinoxes (L1)
  candidates.py  P_all, P_day, P_spring, T, T_C, T_A(v); the masked target (L1)
  readings.py    the 36 readings of G_BM* and the T0b reading (L1)
  reach.py       reach, G with its interval, P(>= 1) per window width (L1)
  heldout.py, deltat.py, verdict.py   (L2)
  almagest.py                         (L3)

Shared constants live here so that every module masks the same day.
Run modules as `py -m odybench.lean.x`, never `py odybench/lean/x.py`
(odybench/calendar.py would shadow the standard library).
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CACHE_DIR = ROOT / "data" / "cache"
PREREG_DIR = ROOT / "data" / "prereg"

# The target: 16 Apr 1178 BC (-1177), proleptic Julian; JD 1291263.5 at 0 h,
# so its civil day number (JDN, the JD of its noon) is 1291264 (DESIGN 0).
TARGET_YMD = (-1177, 4, 16)
TARGET_JDN = 1291264


class TargetMasked(RuntimeError):
    """Raised when a predicate is asked to evaluate 16 Apr -1177 while the
    pool is masked (DESIGN 4.2, 12.3; I13(g))."""


def check_target_masked(day0_jdn, masked: bool, what: str = "pool") -> None:
    """Raise TargetMasked if `masked` and any Day 0 (UT+2 civil day) is the
    target's.  Every evaluation function of the lean run calls this first."""
    if not masked:
        return
    import numpy as np
    d = np.asarray(day0_jdn)
    if d.size and bool(np.any(d == TARGET_JDN)):
        raise TargetMasked(f"{what} holds 16 Apr -1177 while the target is masked")
