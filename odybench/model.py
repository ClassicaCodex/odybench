"""
odybench.model -- the shared types of the bench: the contract of DESIGN 10.2.

Written first by the lead (A0) and frozen as the contract that every other
module is built against (DESIGN 10.1).  It holds constants, record dtypes and
dataclasses only; no module logic lives here.

Conventions (DESIGN section 0 and 10.2):
  * years are astronomical (1178 BC = -1177), dates proleptic Julian, and all
    calendar work goes through odybench.calendar;
  * times are JD floats with a named scale (jd_ut, jd_tt); a civil day is a
    JDN (the integer JD of its noon);
  * arrays are numpy; files are NPZ (numeric) or JSON (UTF-8, ensure_ascii=False).

The fields follow 10.2 exactly.  Where 10.2 leaves a field untyped the
annotation is typing.Any, and the meaning is given in the class docstring.
Two light normalisations make JSON round trips exact: Site.span and
Site.columns, Predicate.day (a range) and GStat.widths become tuples.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

# ------------------------------------------------------------- constants

BODIES = ("sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn")

GRAMMAR_STARS = ("alcyone", "arcturus", "sirius", "aldebaran", "betelgeuse",
                 "rigel", "dubhe")           # extras from data/stars.json allowed

DT_MODELS = ("smh2020", "smh2020_parabola", "smh2016_parabola", "em_canon")

# a candidate pool (4.2): one Day-0 date per clock (UT+2, B&M's; LMT at the site)
POOL_DTYPE = [("jd_ut", "f8"), ("jd_tt", "f8"),
              ("day0_jdn_ut2", "i8"), ("day0_jdn_lmt", "i8"),  # one Day-0 date per clock
              ("kind", "U12"), ("cat_idx", "i8"), ("daylight", "?")]


# ----------------------------------------------------------- dataclasses

@dataclass
class Site:
    """A row of data/prereg/sites.json (DESIGN 0, 4.1).

    key: the site key ('ithaki', 'bm', ...); lat, lon: degrees, east positive;
    elev_m: metres; source: where the coordinates come from; span: Julian
    years (y0, y1), inclusive; columns: the sky-table arrays (10.2, sky.py)
    the site needs."""
    key: str
    lat: float
    lon: float
    elev_m: float
    source: str
    span: tuple[int, int]                    # span: Julian years, inclusive
    columns: tuple[str, ...]

    def __post_init__(self):
        self.span = tuple(self.span)
        self.columns = tuple(self.columns)


@dataclass
class Predicate:
    """A canonical predicate (DESIGN 10.3).

    type: one of 10.3's types ('anchor', 'moon_phase', 'turning_point', ...);
    params: its parameters; day: the day offset from Day 0, a range of
    offsets (lo, hi), or None; quant: the quantifier over a range ('any' or
    'all'); site: the site rule (a point, a box, a disc, or none) or None for
    the clue set's own site; dt_rule: how a Delta-T-dependent row passes
    ('mixture_p50': P_mix >= 0.5 by deltat_mix.p_exact; 'site_free': once at
    the canon Delta-T, for a row whose site rule is 'none', 6.3.1)."""
    type: str
    params: dict
    day: int | tuple[int, int] | None
    quant: str = "any"
    site: dict | None = None
    dt_rule: str = "mixture_p50"            # how a dT-dependent row passes

    def __post_init__(self):
        if isinstance(self.day, list):
            self.day = tuple(self.day)


@dataclass
class Option:
    """One fork option of a clue row.  predicate None means the clue is
    dropped; grid holds the option's listed parameter values (the
    drafter's grids, from which a regime picks one value per list)."""
    name: str
    primary: bool
    predicate: Predicate | None              # None = the clue is dropped
    grid: dict[str, list]


@dataclass
class ClueRow:
    """A clue row: clue_id; event_id (the event or events the row speaks of,
    as the clue file gives them); day_offset (civil days after Day 0, or
    None where the row is placed by events); options."""
    clue_id: str
    event_id: Any
    day_offset: Any
    options: list[Option]


@dataclass
class ClueSet:
    """A clue set: set_id; role (counted control, reported, negative, ...);
    anchor_kind (the kind of the anchor event: solar eclipse, lunar eclipse,
    civil day, conjunction); events; links (the interval rows that link the
    events); rows; site_rule; window_widths (years); counted (enters a gate)."""
    set_id: str
    role: str
    anchor_kind: str
    events: Any
    links: Any
    rows: list[ClueRow]
    site_rule: Any
    window_widths: Any
    counted: bool


@dataclass
class Reading:
    """One reading of a garden: clue_id -> (option name, grid values)."""
    choice: dict[str, tuple[str, dict]]     # clue_id -> (option, grid values)


@dataclass
class SearchResult:
    """The result of search.search (10.2).  pool: the candidates; fails:
    f(c), the number of rows candidate c fails (int16 per candidate);
    strict: the indices of S0 = {c: f(c) = 0}; best: the indices of
    B = {c: f(c) = min f}; n_cand: the number of candidates; clusters: the
    number of clusters in B (candidates within 3 days are one, 6.3.2)."""
    pool: Any
    fails: np.ndarray                        # int16
    strict: np.ndarray                       # int64
    best: np.ndarray                         # int64
    n_cand: int
    clusters: int


@dataclass
class GStat:
    """G with its interval (5.3).  value, lo, hi: the rule's G and the wider
    of the gamma and block-bootstrap intervals; n: the pool size; k: the
    targets with reach > 0; garden, pool, slot, widths: what it is G of;
    lo_gamma, hi_gamma, lo_boot, hi_boot: the two intervals; masked: the
    target was masked (12.3)."""
    value: float
    lo: float
    hi: float
    n: int
    k: int
    garden: str
    pool: str
    slot: str | None
    widths: tuple[int, ...]
    lo_gamma: float
    hi_gamma: float
    lo_boot: float
    hi_boot: float
    masked: bool                             # lo, hi = the wider pair (5.3)

    def __post_init__(self):
        self.widths = tuple(self.widths)


__all__ = ["BODIES", "GRAMMAR_STARS", "DT_MODELS", "POOL_DTYPE", "Site", "Predicate", "Option",
           "ClueRow", "ClueSet", "Reading", "SearchResult", "GStat"]
