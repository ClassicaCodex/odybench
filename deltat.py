"""
deltat.py -- N6 of the lean run (LEAN.md; DESIGN 5.6, 2.3, 4.4): Delta-T and
the eclipse at Ithaca.

For 16 Apr 1178 BC (-1177) and 30 Sep 1131 BC (-1130), at Ithaki and the four
sensitivity sites of data/prereg/sites.json:

* totality windows and smag >= 0.9 windows in constant Delta-T, found by a
  10-s scan (20 s on the JPL ephemerides) over [min(mu - 6 sigma),
  max(mu + 6 sigma)] of the models in that frame and bisected to 0.01 s
  (data/prereg/deltat_models.json, p_exact; the continuous window of 2.3);
* P(total) and P(smag >= 0.9) per Delta-T model, each model a Gaussian with
  its stated sigma (an ASSUMPTION, DESIGN 0), and the equal-weight mixture;
  - in the canon frame on NASA's Besselian elements (the 2.3 table, the
    I2(c) reference): SMH values converted to the canon n-dot by
    ephem.ndot_correction (+34 s at -1177), Espenak-Meeus as it is;
  - in each model's own frame (5.6 item 1): the three SMH models with DE431
    (ephem.local_circumstances), Espenak-Meeus with NASA's elements;
  - DE441 with SMH2020 reported beside, with its offset;
* the joint probability that both eclipses were total, under a common
  offset d ~ N(0, sigma_1178) from each model's value (as 2.3);
* smag and the LAT of maximum as functions of constant Delta-T,
  26,000-32,000 s, at Ithaki.

smag is NASA's magnitude exactly as program.js computes it (DESIGN 0): the
module's jsex_local() is a line-by-line port of getall() of
data/jsex/program.js, with Delta-T (elements[5]) as the argument; total means
program.js's type 3 with the Sun above the horizon at maximum.  The port is
checked against program.js itself under Node (tests/test_lean_deltat.py) and
against NASA's site catalogues (data/jsex/sites/).

Every number here is an eclipse circumstance that DESIGN 2.3 already
publishes, or a function of one; no planet is evaluated.

Usage:
  py deltat.py --out results/build-L2/n6       # anywhere (scratch)
  py deltat.py                                 # results/n6/: only after the second
                                               # freeze (results/attain/FROZEN)
  py deltat.py --selftest                      # port vs the NASA site catalogues
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from odybench import calendar as cal  # noqa: E402
from odybench import ephem as E  # noqa: E402

JSEX_DIR = ROOT / "data" / "jsex"
SITES_JSON = ROOT / "data" / "prereg" / "sites.json"
MODELS_JSON = ROOT / "data" / "prereg" / "deltat_models.json"
FROZEN = ROOT / "results" / "attain" / "FROZEN"
DEFAULT_OUT = ROOT / "results" / "n6"

MODELS = ("smh2020", "smh2020_parabola", "smh2016_parabola", "em_canon")
EPHEM_MODEL = {"smh2020": "smh2020", "smh2020_parabola": "smh2020_parabola",
               "smh2016_parabola": "smh2016_parabola", "em_canon": "em2006_canon"}
LABEL = {"smh2020": "SMH2020", "smh2020_parabola": "Addendum 2020 parabola",
         "smh2016_parabola": "SMH2016 parabola", "em_canon": "Espenak-Meeus, canon form"}
NDOT_CANON, NDOT_SMH = -25.858, -25.82
ECLIPSES = {"1178BC": (-1177, 4, 16), "1131BC": (-1130, 9, 30)}
SITE_KEYS = ("ithaki", "kefalonia", "lefkada", "corfu", "zakynthos")
VATHY = (38.367, 20.717)          # the review's Ithaki, which produced 2.3's windows
SPAN_SIGMA = 6.0
MAG09 = 0.9

# DESIGN 2.3, revision 8 (continuous window), for the comparison printed by main()
REF_23 = {
    "window_1178_canon": (28801.02, 29584.91),
    "window_1131_canon": (27049.07, 28038.49),
    "window_1178_de431_smh": (28761.0, 29545.0),
    "window_1178_de441_smh": (28922.0, 29706.0),
    "P78": {"smh2020": 0.297, "smh2020_parabola": 0.175, "smh2016_parabola": 0.503, "em_canon": 0.255,
            "mixture": 0.308},
    "P31": {"smh2020": 0.496, "smh2020_parabola": 0.643, "smh2016_parabola": 0.446, "em_canon": 0.414,
            "mixture": 0.500},
    "joint": {"smh2020": 0.051, "smh2020_parabola": 0.056, "smh2016_parabola": 0.113, "em_canon": 0.052,
              "mixture": 0.068},
    "P09_78": {"smh2020": 0.932, "smh2020_parabola": 0.934, "smh2016_parabola": 0.997, "em_canon": 0.849,
               "mixture": 0.928},
    "P78_de431": {"smh2020": 0.299, "smh2020_parabola": 0.178, "smh2016_parabola": 0.505, "mixture": 0.309},
    "smag_1178_vathy_canon": 0.984,
    "smag_1131_vathy_canon": 1.0486,
}
I2C_TOL = 0.005


# ------------------------------------------------------------ NASA elements

def load_jsex(path):
    """{(year, month, day): [28 floats]} from a JSEX century file (the Canon's
    Besselian elements, one block of 28 numbers after each '//y m d' line)."""
    txt = Path(path).read_text(encoding="utf-8")
    body = txt[txt.index("new Array(") + len("new Array("):]
    heads = list(re.finditer(r"//\s*(-?\d+)\s+(\d+)\s+(\d+)\s*\n", body))
    out = {}
    for i, h in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(body)
        nums = [float(v) for v in re.findall(r"-?\d+\.\d+(?:[eE][-+]?\d+)?", body[h.end():end])]
        if len(nums) != 28:
            raise ValueError(f"{path}: {h.group(0).strip()} has {len(nums)} numbers")
        out[(int(h.group(1)), int(h.group(2)), int(h.group(3)))] = nums
    return out


def jsex_file_for(year):
    """The JSEX century file holding astronomical year `year` (SEm1199 holds
    -1199..-1100, SE0001 holds +1..+100)."""
    if year >= 1:
        lo = (year - 1) // 100 * 100 + 1
        return JSEX_DIR / f"SE{lo:04d}.js"
    n = (-year) // 100 * 100 + 99                      # SEm<n> holds -n .. -n + 99
    return JSEX_DIR / f"SEm{n:04d}.js"


def elements_for(date):
    y, m, d = date
    return load_jsex(jsex_file_for(y))[(y, m, d)]


# ---------------------------------------------- program.js getall(), ported

def _sqrt(x):
    return math.sqrt(x) if x >= 0 else float("nan")


def _asin(x):
    return math.asin(x) if -1.0 <= x <= 1.0 else float("nan")


def _acos(x):
    return math.acos(x) if -1.0 <= x <= 1.0 else float("nan")


class _JSEX:
    """State of one getall() call: obsvconst, the elements, c1, c2, mid, c3,
    c4 (each 41 entries, indices as program.js documents them)."""

    def __init__(self, el, lat_deg, lon_east_deg, elev_m=0.0):
        self.el = list(el)
        o = [0.0] * 7
        o[0] = lat_deg * math.pi / 180.0
        o[1] = -lon_east_deg * math.pi / 180.0              # west longitude positive
        o[2] = elev_m
        o[3] = 0.0                                          # UT
        tmp = math.atan(0.99664719 * math.tan(o[0]))
        o[4] = 0.99664719 * math.sin(tmp) + (o[2] / 6378140.0) * math.sin(o[0])
        o[5] = math.cos(tmp) + (o[2] / 6378140.0 * math.cos(o[0]))
        o[6] = 0
        self.o = o
        self.c1, self.c2, self.mid, self.c3, self.c4 = ([0.0] * 41 for _ in range(5))

    def timedependent(self, c):
        el = self.el
        t = c[1]
        c[2] = ((el[9] * t + el[8]) * t + el[7]) * t + el[6]
        c[10] = (3.0 * el[9] * t + 2.0 * el[8]) * t + el[7]
        c[3] = ((el[13] * t + el[12]) * t + el[11]) * t + el[10]
        c[11] = (3.0 * el[13] * t + 2.0 * el[12]) * t + el[11]
        ans = ((el[16] * t + el[15]) * t + el[14]) * math.pi / 180.0
        c[4] = ans
        c[5] = math.sin(ans)
        c[6] = math.cos(ans)
        c[12] = (2.0 * el[16] * t + el[15]) * math.pi / 180.0
        ans = (el[19] * t + el[18]) * t + el[17]
        if ans >= 360.0:
            ans = ans - 360.0
        c[7] = ans * math.pi / 180.0
        c[13] = (2.0 * el[19] * t + el[18]) * math.pi / 180.0
        typ = c[0]
        if typ in (-2, 0, 2):
            c[8] = (el[22] * t + el[21]) * t + el[20]
            c[14] = 2.0 * el[22] * t + el[21]
        if typ in (-1, 0, 1):
            c[9] = (el[25] * t + el[24]) * t + el[23]
            c[15] = 2.0 * el[25] * t + el[24]

    def timelocdependent(self, c):
        el, o = self.el, self.o
        self.timedependent(c)
        c[16] = c[7] - o[1] - (el[5] / 13713.44)
        c[17] = math.sin(c[16])
        c[18] = math.cos(c[16])
        c[19] = o[5] * c[17]
        c[20] = o[4] * c[6] - o[5] * c[18] * c[5]
        c[21] = o[4] * c[5] + o[5] * c[18] * c[6]
        c[22] = c[13] * o[5] * c[18]
        c[23] = c[13] * c[19] * c[5] - c[21] * c[12]
        c[24] = c[2] - c[19]
        c[25] = c[3] - c[20]
        c[26] = c[10] - c[22]
        c[27] = c[11] - c[23]
        typ = c[0]
        if typ in (-2, 0, 2):
            c[28] = c[8] - c[21] * el[26]
        if typ in (-1, 0, 1):
            c[29] = c[9] - c[21] * el[27]
        c[30] = c[26] * c[26] + c[27] * c[27]

    def _iterate(self, c, k):
        self.timelocdependent(c)
        sign = -1.0 if c[0] < 0 else 1.0
        if k == 29 and self.mid[29] < 0.0:
            sign = -sign
        tmp, it = 1.0, 0
        while ((tmp > 0.000001) or (tmp < -0.000001)) and it < 50:
            n = _sqrt(c[30])
            tmp = c[26] * c[25] - c[24] * c[27]
            tmp = tmp / n / c[k]
            tmp = sign * _sqrt(1.0 - tmp * tmp) * c[k] / n
            tmp = (c[24] * c[26] + c[25] * c[27]) / c[30] - tmp
            c[1] = c[1] - tmp
            self.timelocdependent(c)
            it += 1

    def getc1c4(self):
        mid = self.mid
        n = _sqrt(mid[30])
        tmp = mid[26] * mid[25] - mid[24] * mid[27]
        tmp = tmp / n / mid[28]
        tmp = _sqrt(1.0 - tmp * tmp) * mid[28] / n
        self.c1[0], self.c4[0] = -2, 2
        self.c1[1] = mid[1] - tmp
        self.c4[1] = mid[1] + tmp
        self._iterate(self.c1, 28)
        self._iterate(self.c4, 28)

    def getc2c3(self):
        mid = self.mid
        n = _sqrt(mid[30])
        tmp = mid[26] * mid[25] - mid[24] * mid[27]
        tmp = tmp / n / mid[29]
        tmp = _sqrt(1.0 - tmp * tmp) * mid[29] / n
        self.c2[0], self.c3[0] = -1, 1
        if mid[29] < 0.0:
            self.c2[1] = mid[1] + tmp
            self.c3[1] = mid[1] - tmp
        else:
            self.c2[1] = mid[1] - tmp
            self.c3[1] = mid[1] + tmp
        self._iterate(self.c2, 29)
        self._iterate(self.c3, 29)

    def observational(self, c):
        mid, o = self.mid, self.o
        if c[0] == 0:
            ct = 1.0
        else:
            ct = -1.0 if (mid[39] == 3 and c[0] in (-1, 1)) else 1.0
        c[31] = math.atan2(ct * c[24], ct * c[25])
        sinlat, coslat = math.sin(o[0]), math.cos(o[0])
        c[32] = _asin(c[5] * sinlat + c[6] * coslat * c[18])
        c[33] = _asin(coslat * c[17] / math.cos(c[32]))
        if c[20] < 0.0:
            c[33] = math.pi - c[33]
        c[34] = c[31] - c[33]
        c[35] = math.atan2(-1.0 * c[17] * c[6], c[5] * coslat - c[18] * sinlat * c[6])
        c[40] = 0 if c[32] > -0.00524 else 1

    def midobservational(self):
        mid = self.mid
        self.observational(mid)
        mid[36] = _sqrt(mid[24] * mid[24] + mid[25] * mid[25])
        mid[37] = (mid[28] - mid[36]) / (mid[28] + mid[29])
        mid[38] = (mid[28] - mid[29]) / (mid[28] + mid[29])

    def getmid(self):
        mid = self.mid
        mid[0] = 0
        mid[1] = 0.0
        it, tmp = 0, 1.0
        self.timelocdependent(mid)
        while ((tmp > 0.000001) or (tmp < -0.000001)) and it < 50:
            tmp = (mid[24] * mid[26] + mid[25] * mid[27]) / mid[30]
            mid[1] = mid[1] - tmp
            it += 1
            self.timelocdependent(mid)

    def getsunriset(self, c, riset):
        o = self.o
        diff, it = 1.0, 0
        while (diff > 0.00001) or (diff < -0.00001):
            it += 1
            if it == 4:
                return
            h0 = _acos((math.sin(-0.00524) - math.sin(o[0]) * c[5]) / math.cos(o[0]) / c[6])
            diff = (riset * h0 - c[16]) / c[13]
            while diff >= 12.0:
                diff -= 24.0
            while diff <= -12.0:
                diff += 24.0
            c[1] += diff
            self.timelocdependent(c)

    @staticmethod
    def copy(src, dst):
        for i in range(1, 41):
            dst[i] = src[i]

    def getall(self):
        mid, c1, c2, c3, c4 = self.mid, self.c1, self.c2, self.c3, self.c4
        self.getmid()
        self.midobservational()
        if mid[37] > 0.0:
            self.getc1c4()
            if (mid[36] < mid[29]) or (mid[36] < -mid[29]):
                self.getc2c3()
                mid[39] = 3 if mid[29] < 0.0 else 2
                for c in (c1, c2, c3, c4):
                    self.observational(c)
                c2[36] = 999.9
                c3[36] = 999.9
                pattern = ((10000 if c1[40] == 0 else 0) + (1000 if c2[40] == 0 else 0)
                           + (100 if mid[40] == 0 else 0) + (10 if c3[40] == 0 else 0)
                           + (1 if c4[40] == 0 else 0))
                if pattern == 11110:
                    self.getsunriset(c4, 1.0); self.observational(c4); c4[40] = 3
                elif pattern == 11100:
                    self.getsunriset(c3, 1.0); self.observational(c3); c3[40] = 3; self.copy(c3, c4)
                elif pattern == 11000:
                    c3[40] = 4
                    self.getsunriset(mid, 1.0); self.midobservational(); mid[40] = 3; self.copy(mid, c4)
                elif pattern == 10000:
                    mid[39] = 1
                    self.getsunriset(mid, 1.0); self.midobservational(); mid[40] = 3; self.copy(mid, c4)
                elif pattern == 1111:
                    self.getsunriset(c1, -1.0); self.observational(c1); c1[40] = 2
                elif pattern == 111:
                    self.getsunriset(c2, -1.0); self.observational(c2); c2[40] = 2; self.copy(c2, c1)
                elif pattern == 11:
                    c2[40] = 4
                    self.getsunriset(mid, -1.0); self.midobservational(); mid[40] = 2; self.copy(mid, c1)
                elif pattern == 1:
                    mid[39] = 1
                    self.getsunriset(mid, -1.0); self.midobservational(); mid[40] = 2; self.copy(mid, c1)
                elif pattern == 0:
                    mid[39] = 0
            else:
                mid[39] = 1
                self.observational(c1)
                self.observational(c4)
                pattern = ((100 if c1[40] == 0 else 0) + (10 if mid[40] == 0 else 0)
                           + (1 if c4[40] == 0 else 0))
                if pattern == 110:
                    self.getsunriset(c4, 1.0); self.observational(c4); c4[40] = 3
                elif pattern == 100:
                    self.getsunriset(mid, 1.0); self.midobservational(); mid[40] = 3; self.copy(mid, c4)
                elif pattern == 11:
                    self.getsunriset(c1, -1.0); self.observational(c1); c1[40] = 2
                elif pattern == 1:
                    self.getsunriset(mid, -1.0); self.midobservational(); mid[40] = 2; self.copy(mid, c1)
                elif pattern == 0:
                    mid[39] = 0
        else:
            mid[39] = 0
        smag_partial = mid[37]
        if mid[39] in (2, 3):
            mid[37] = mid[38]
        return smag_partial


def jsex_local(el, lat, lon_east, dt_s=None, elev_m=0.0):
    """Local circumstances at maximum by program.js's getall(), with
    Delta-T (elements[5], the hour-angle term) set to dt_s (default: the
    Canon's).  Returns smag (mid[37] as printed), smag_partial (before the
    total/annular override), ratio (mid[38]), type (0 none, 1 partial, 2
    annular, 3 total), alt_deg (Sun at maximum), vis (mid[40]), lat_hours
    (12 + hour angle), tt_hours (TD on the elements' date), ut_hours."""
    el = list(el)
    if dt_s is not None:
        el[5] = float(dt_s)
    j = _JSEX(el, lat, lon_east, elev_m)
    sp = j.getall()
    mid = j.mid
    last = 12.0 + (mid[16] * 180.0 / math.pi) / 15.0
    tt_h = mid[1] + el[1]
    return dict(smag=mid[37], smag_partial=sp, ratio=mid[38], type=int(mid[39]),
                alt_deg=mid[32] * 180.0 / math.pi, vis=int(mid[40]),
                lat_hours=((last % 24.0) + 24.0) % 24.0, tt_hours=tt_h,
                ut_hours=((tt_h - el[5] / 3600.0) % 24.0 + 24.0) % 24.0, dt_s=el[5])


# --------------------------------------------------------------- predicates

def nasa_pred(el, lat, lon):
    def f(dt):
        r = jsex_local(el, lat, lon, dt)
        return dict(total=(r["type"] == 3 and r["alt_deg"] > 0.0),
                    mag09=(r["type"] > 0 and r["smag"] >= MAG09 and r["alt_deg"] > 0.0))
    return f


def de_local(lat, lon, jd_tt, dt_s, ephem_dir):
    with E.use_ephemeris(ephem_dir):
        lc = E.local_circumstances(lat, lon, jd_tt, float(dt_s), window_h=2.0)
    central = lc["total"] or lc["annular"]
    smag = lc["ratio"] if central else lc["magnitude"]
    return dict(smag=smag, total=bool(lc["total"]), annular=bool(lc["annular"]),
                alt_deg=lc["sun_alt_deg"], lat_hours=float(lc["lat_hours"]),
                magnitude=lc["magnitude"], ratio=lc["ratio"])


def de_pred(lat, lon, jd_tt, ephem_dir):
    def f(dt):
        r = de_local(lat, lon, jd_tt, dt, ephem_dir)
        return dict(total=(r["total"] and r["alt_deg"] > 0.0),
                    mag09=(r["smag"] >= MAG09 and r["alt_deg"] > 0.0))
    return f


def windows(pred, lo, hi, step, tol=0.01, keys=("total", "mag09")):
    """Intervals of constant Delta-T in [lo, hi] where pred(dt)[key] holds:
    a scan at `step` s, each change bisected to `tol` s.  Returns {key:
    [(a, b, clipped_lo, clipped_hi)]}."""
    grid = np.arange(lo, hi + step / 2.0, step)
    vals = [pred(float(g)) for g in grid]
    out = {}
    for key in keys:
        v = [bool(x[key]) for x in vals]
        edges = []
        for i in range(len(grid) - 1):
            if v[i] != v[i + 1]:
                a, b = float(grid[i]), float(grid[i + 1])
                va = v[i]
                while b - a > tol:
                    m = 0.5 * (a + b)
                    if bool(pred(m)[key]) == va:
                        a = m
                    else:
                        b = m
                edges.append(0.5 * (a + b))
        ws, cur = [], (float(grid[0]) if v[0] else None)
        cur_clip = v[0]
        for e in edges:
            if cur is None:
                cur, cur_clip = e, False
            else:
                ws.append((cur, e, cur_clip, False))
                cur = None
        if cur is not None:
            ws.append((cur, float(grid[-1]), cur_clip, True))
        out[key] = ws
    return out


# ------------------------------------------------------------ probabilities

def phi(z):
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def p_intervals(mu, sigma, ivs):
    return sum(phi((b - mu) / sigma) - phi((a - mu) / sigma) for a, b, *_ in ivs)


def _intersect(A, B):
    out = []
    for a0, a1, *_ in A:
        for b0, b1, *_ in B:
            lo, hi = max(a0, b0), min(a1, b1)
            if hi > lo:
                out.append((lo, hi))
    return out


def joint_common_offset(mu1, s1, w1, mu2, w2):
    """P(both total) with one common offset d ~ N(0, s1) from each model's
    value: d in (W1 - mu1) and in (W2 - mu2) (DESIGN 2.3's joint)."""
    A = [(a - mu1, b - mu1) for a, b, *_ in w1]
    B = [(a - mu2, b - mu2) for a, b, *_ in w2]
    return sum(phi(hi / s1) - phi(lo / s1) for lo, hi in _intersect(A, B))


def sigma_of(model, y):
    """The stated 1-sigma (deltat_models.json): SMH models as ephem states
    them; Espenak-Meeus Huber before -500 and Morrison-Stephenson 2004's
    0.8 u^2 from -500 on (the NASA page's envelope)."""
    if model == "em_canon":
        return float(E.sigma_huber(y)) if y < -500 else float(E.sigma_ms2004(y))
    return float(E.delta_t_sigma(y, EPHEM_MODEL[model]))


def model_values(y, frame):
    """{model: (mu, sigma)} at Julian epoch y.  frame 'canon': every model in
    the canon n-dot frame (SMH + ndot_correction); 'own': each in its own
    (SMH in the DE431 frame, Espenak-Meeus in the canon frame)."""
    out = {}
    for m in MODELS:
        mu = float(E.delta_t(y, EPHEM_MODEL[m]))
        if frame == "canon" and m != "em_canon":
            mu += float(E.ndot_correction(y, NDOT_CANON, NDOT_SMH))
        out[m] = (mu, sigma_of(m, y))
    return out


def scan_range(vals, models=MODELS):
    lo = min(vals[m][0] - SPAN_SIGMA * vals[m][1] for m in models)
    hi = max(vals[m][0] + SPAN_SIGMA * vals[m][1] for m in models)
    return math.floor(lo / 10.0) * 10.0, math.ceil(hi / 10.0) * 10.0


# --------------------------------------------------------------------- run

def site_table():
    s = json.loads(SITES_JSON.read_text(encoding="utf-8"))["sites"]
    out = {k: (float(s[k]["lat"]), float(s[k]["lon"])) for k in SITE_KEYS}
    out["vathy"] = VATHY
    return out


def compute(sites=None, de_sites=("ithaki", "kefalonia", "lefkada", "corfu", "zakynthos", "vathy"),
            de441_sites=("ithaki", "vathy"), nasa_step=10.0, de_step=20.0, log=print):
    sites = sites or site_table()
    res = dict(eclipses={}, sites={k: list(v) for k, v in sites.items()},
               assumption="each Delta-T model a Gaussian with its stated sigma (DESIGN 0)")
    for ek, date in ECLIPSES.items():
        el = elements_for(date)
        jd_tt = el[0]
        y = float(cal.julian_epoch(jd_tt))
        canon = model_values(y, "canon")
        own = model_values(y, "own")
        rec = dict(date=f"{date[0]}-{date[1]:02d}-{date[2]:02d}", jd_tt_greatest=jd_tt, epoch=y,
                   canon_dt_s=el[5], models_canon_frame=canon, models_own_frame=own, sites={})
        lo_c, hi_c = scan_range(canon)
        lo_o, hi_o = scan_range(own, MODELS[:3])
        for sk, (lat, lon) in sites.items():
            t0 = time.time()
            r = dict(lat=lat, lon=lon)
            wn = windows(nasa_pred(el, lat, lon), lo_c, hi_c, nasa_step)
            r["nasa"] = dict(scan=[lo_c, hi_c, nasa_step], windows=wn,
                             at_model={m: jsex_local(el, lat, lon, canon[m][0]) for m in MODELS},
                             at_canon=jsex_local(el, lat, lon, None))
            r["P_canon"] = {}
            for key in ("total", "mag09"):
                pm = {m: p_intervals(canon[m][0], canon[m][1], wn[key]) for m in MODELS}
                pm["mixture"] = sum(pm[m] for m in MODELS) / len(MODELS)
                r["P_canon"][key] = pm
            if sk in de_sites:
                wd = windows(de_pred(lat, lon, jd_tt, E.EPHEM_DIR / "de431"), lo_o, hi_o, de_step)
                r["de431"] = dict(scan=[lo_o, hi_o, de_step], windows=wd,
                                  at_model={m: de_local(lat, lon, jd_tt, own[m][0], E.EPHEM_DIR / "de431")
                                            for m in MODELS[:3]})
                r["P_own"] = {}
                for key in ("total", "mag09"):
                    pm = {m: p_intervals(own[m][0], own[m][1], wd[key]) for m in MODELS[:3]}
                    pm["em_canon"] = r["P_canon"][key]["em_canon"]
                    pm["mixture"] = sum(pm[m] for m in MODELS) / len(MODELS)
                    r["P_own"][key] = pm
            if sk in de441_sites:
                mu, s = own["smh2020"]
                wd = windows(de_pred(lat, lon, jd_tt, E.EPHEM_DIR), mu - SPAN_SIGMA * s, mu + SPAN_SIGMA * s,
                             de_step)
                r["de441_smh2020"] = dict(windows=wd, P={k: p_intervals(mu, s, wd[k]) for k in wd},
                                          at_value=de_local(lat, lon, jd_tt, mu, E.EPHEM_DIR))
            rec["sites"][sk] = r
            log(f"  {ek} {sk}: {time.time() - t0:.1f} s")
        res["eclipses"][ek] = rec
    # joints, per site, under a common offset
    a, b = res["eclipses"]["1178BC"], res["eclipses"]["1131BC"]
    res["joint"] = {}
    for sk in sites:
        ra, rb = a["sites"][sk], b["sites"][sk]
        j = {}
        jc = {}
        for m in MODELS:
            mu1, s1 = a["models_canon_frame"][m]
            mu2, _ = b["models_canon_frame"][m]
            jc[m] = joint_common_offset(mu1, s1, ra["nasa"]["windows"]["total"], mu2, rb["nasa"]["windows"]["total"])
        jc["mixture"] = sum(jc[m] for m in MODELS) / len(MODELS)
        j["canon"] = jc
        if "de431" in ra and "de431" in rb:
            jo = {}
            for m in MODELS[:3]:
                mu1, s1 = a["models_own_frame"][m]
                mu2, _ = b["models_own_frame"][m]
                jo[m] = joint_common_offset(mu1, s1, ra["de431"]["windows"]["total"], mu2,
                                            rb["de431"]["windows"]["total"])
            jo["em_canon"] = jc["em_canon"]
            jo["mixture"] = sum(jo[m] for m in MODELS) / len(MODELS)
            j["own"] = jo
        res["joint"][sk] = j
    # magnitude and LAT of maximum against constant Delta-T, Ithaki
    lat, lon = sites["ithaki"]
    el = elements_for(ECLIPSES["1178BC"])
    curve = []
    for dt in np.arange(26000.0, 32000.0 + 1, 250.0):
        rn = jsex_local(el, lat, lon, dt)
        rd = de_local(lat, lon, el[0], dt, E.EPHEM_DIR / "de431")
        curve.append(dict(dt_s=float(dt), nasa_smag=rn["smag"], nasa_type=rn["type"], nasa_lat_h=rn["lat_hours"],
                          de431_smag=rd["smag"], de431_total=rd["total"], de431_lat_h=rd["lat_hours"]))
    res["curve_1178BC_ithaki"] = curve
    return res


def _fmt_w(ws):
    if not ws:
        return "none"
    return "; ".join(f"{a:,.2f}-{b:,.2f}" + (" (scan edge)" if (cl or ch) else "") for a, b, cl, ch in ws)


def report(res):
    L = []
    p = L.append
    p("N6 (DESIGN 5.6, LEAN.md): Delta-T and the eclipse at Ithaca")
    p("Assumption: each Delta-T model a Gaussian with its stated sigma (DESIGN 0).")
    p("smag: NASA's magnitude as program.js prints it (port of getall()); total = type 3, Sun up at maximum.")
    p("")
    for ek, rec in res["eclipses"].items():
        p(f"== {ek} ({rec['date']}), greatest eclipse JD(TT) {rec['jd_tt_greatest']:.6f}, epoch {rec['epoch']:.3f}, "
          f"canon Delta-T {rec['canon_dt_s']:.1f} s")
        p("   models (canon frame | own frame), mu +- sigma:")
        for m in MODELS:
            c, o = rec["models_canon_frame"][m], rec["models_own_frame"][m]
            p(f"     {LABEL[m]:28s} {c[0]:9.1f} +- {c[1]:6.1f} | {o[0]:9.1f} +- {o[1]:6.1f}")
        for sk, r in rec["sites"].items():
            p(f"   -- {sk} ({r['lat']}, {r['lon']})")
            ac = r["nasa"]["at_canon"]
            p(f"      NASA elements at canon Delta-T: smag {ac['smag']:.4f} (partial formula {ac['smag_partial']:.4f}), "
              f"type {ac['type']}, max {ac['ut_hours']:.3f} h UT, LAT {ac['lat_hours']:.3f} h, Sun {ac['alt_deg']:.1f} deg")
            p(f"      canon frame, NASA elements: total for {_fmt_w(r['nasa']['windows']['total'])} s; "
              f"smag >= 0.9 for {_fmt_w(r['nasa']['windows']['mag09'])} s")
            for key, name in (("total", "P(total)"), ("mag09", "P(smag >= 0.9)")):
                pm = r["P_canon"][key]
                p(f"      {name:15s} canon: " + "  ".join(f"{m} {pm[m]:.4f}" for m in MODELS + ("mixture",)))
            if "de431" in r:
                p(f"      DE431 (SMH frame): total for {_fmt_w(r['de431']['windows']['total'])} s; "
                  f"smag >= 0.9 for {_fmt_w(r['de431']['windows']['mag09'])} s")
                for m in MODELS[:3]:
                    a = r["de431"]["at_model"][m]
                    p(f"        at {LABEL[m]} ({rec['models_own_frame'][m][0]:.0f} s): smag {a['smag']:.4f}, "
                      f"LAT {a['lat_hours']:.3f} h, Sun {a['alt_deg']:.1f} deg, total {a['total']}")
                for key, name in (("total", "P(total)"), ("mag09", "P(smag >= 0.9)")):
                    pm = r["P_own"][key]
                    p(f"      {name:15s} own:   " + "  ".join(f"{m} {pm[m]:.4f}" for m in MODELS + ("mixture",)))
            if "de441_smh2020" in r:
                d = r["de441_smh2020"]
                p(f"      DE441 + SMH2020 (beside): total for {_fmt_w(d['windows']['total'])} s; "
                  f"P(total) {d['P']['total']:.4f}; smag at the SMH2020 value {d['at_value']['smag']:.4f}, "
                  f"LAT {d['at_value']['lat_hours']:.3f} h")
        p("")
    p("== joint P(both total), common offset d ~ N(0, sigma_1178) from each model's value")
    for sk, j in res["joint"].items():
        for fr, jm in j.items():
            p(f"   {sk:10s} {fr:5s}: " + "  ".join(f"{m} {jm[m]:.4f}" for m in MODELS + ("mixture",)))
    p("")
    p("== smag and LAT of maximum against constant Delta-T, 1178 BC, Ithaki (sites.json)")
    for row in res["curve_1178BC_ithaki"]:
        p(f"   {row['dt_s']:8.0f} s  NASA smag {row['nasa_smag']:.4f} type {row['nasa_type']} LAT {row['nasa_lat_h']:.3f} h"
          f" | DE431 smag {row['de431_smag']:.4f} total {row['de431_total']} LAT {row['de431_lat_h']:.3f} h")
    p("")
    p("== against DESIGN 2.3 (revision 8; continuous windows; the I2(c) tolerance is 0.005 on P(total))")
    cmp_ = compare_23(res)
    for line in cmp_["lines"]:
        p("   " + line)
    p(f"   largest |difference| in P(total), canon frame: {cmp_['max_dp']:.4f} "
      f"({'within' if cmp_['max_dp'] <= I2C_TOL else 'OUTSIDE'} {I2C_TOL})")
    return "\n".join(L) + "\n", cmp_


def compare_23(res):
    lines, dps = [], []
    a = res["eclipses"]["1178BC"]["sites"]
    b = res["eclipses"]["1131BC"]["sites"]
    for sk in ("vathy", "ithaki"):
        if sk not in a:
            continue
        w78 = a[sk]["nasa"]["windows"]["total"]
        w31 = b[sk]["nasa"]["windows"]["total"]
        lines.append(f"{sk}: 1178 BC canon window {_fmt_w(w78)} (2.3: {REF_23['window_1178_canon'][0]:,.2f}-"
                     f"{REF_23['window_1178_canon'][1]:,.2f}); 1131 BC {_fmt_w(w31)} (2.3: "
                     f"{REF_23['window_1131_canon'][0]:,.2f}-{REF_23['window_1131_canon'][1]:,.2f})")
        for key, ref, src in (("P78", REF_23["P78"], a), ("P31", REF_23["P31"], b)):
            pm = src[sk]["P_canon"]["total"]
            d = {m: pm[m] - ref[m] for m in ref}
            if sk == "vathy":
                dps += [abs(x) for x in d.values()]
            lines.append(f"{sk} {key}: " + "  ".join(f"{m} {pm[m]:.4f} (2.3 {ref[m]:.3f}, {d[m]:+.4f})" for m in ref))
        jm = res["joint"][sk]["canon"]
        lines.append(f"{sk} joint: " + "  ".join(f"{m} {jm[m]:.4f} (2.3 {REF_23['joint'][m]:.3f})"
                                                 for m in REF_23["joint"]))
        pm = a[sk]["P_canon"]["mag09"]
        lines.append(f"{sk} P(smag>=0.9) 1178: " + "  ".join(
            f"{m} {pm[m]:.4f} (2.3 {REF_23['P09_78'][m]:.3f}, a 20-s grid value)" for m in REF_23["P09_78"]))
        if "P_own" in a[sk]:
            po = a[sk]["P_own"]["total"]
            lines.append(f"{sk} P78 own frame (DE431 SMH + E-M on NASA): " + "  ".join(
                f"{m} {po[m]:.4f} (2.3 {REF_23['P78_de431'][m]:.3f})" for m in REF_23["P78_de431"]))
            lines.append(f"{sk} DE431 window: {_fmt_w(a[sk]['de431']['windows']['total'])} "
                         f"(2.3, ithaki: {REF_23['window_1178_de431_smh'][0]:,.0f}-{REF_23['window_1178_de431_smh'][1]:,.0f})")
        if "de441_smh2020" in a[sk]:
            lines.append(f"{sk} DE441 window: {_fmt_w(a[sk]['de441_smh2020']['windows']['total'])} "
                         f"(2.3: {REF_23['window_1178_de441_smh'][0]:,.0f}-{REF_23['window_1178_de441_smh'][1]:,.0f})")
        ac = a[sk]["nasa"]["at_canon"]
        lines.append(f"{sk} smag 1178 at canon Delta-T {ac['smag']:.4f} (2.3 0.984); 1131 "
                     f"{b[sk]['nasa']['at_canon']['smag']:.4f} (2.3 1.0486, total)")
    return dict(lines=lines, max_dp=max(dps) if dps else float("nan"))


def _json_default(o):
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError(type(o))


def summary(res):
    """The compact numbers the verdict reads (reported beside the rule)."""
    out = {}
    for ek in ECLIPSES:
        for sk, r in res["eclipses"][ek]["sites"].items():
            out.setdefault(sk, {})[ek] = dict(
                P_total_canon=r["P_canon"]["total"], P_mag09_canon=r["P_canon"]["mag09"],
                P_total_own=r.get("P_own", {}).get("total"), P_mag09_own=r.get("P_own", {}).get("mag09"),
                window_total_canon=[w[:2] for w in r["nasa"]["windows"]["total"]],
                window_total_de431=[w[:2] for w in r.get("de431", {}).get("windows", {}).get("total", [])])
    for sk, j in res["joint"].items():
        out.setdefault(sk, {})["joint"] = j
    return out


def selftest():
    """The port against NASA's site catalogues (data/jsex/sites/*.jsonl,
    written by tools/jsex_sites.js from program.js) for every eclipse of
    three century files at the five sites, at the Canon's Delta-T."""
    st = site_table()
    names = {"ithaki": "ithaca", "kefalonia": "kefalonia", "lefkada": "lefkada", "corfu": "corfu",
             "zakynthos": "zakynthos"}
    worst = dict(mag=0.0, alt=0.0, last=0.0, type=0)
    n = 0
    for sk, fn in names.items():
        lat, lon = st[sk]
        rows = [json.loads(x) for x in (JSEX_DIR / "sites" / f"{fn}.jsonl").read_text(encoding="utf-8").splitlines()
                if x.strip()]
        for f in ("SEm0699.js", "SEm1199.js", "SE0101.js"):
            els = load_jsex(JSEX_DIR / f)
            keys = list(els)
            for row in (r for r in rows if r["file"] == f):
                el = els[keys[row["idx"]]]
                r = jsex_local(el, lat, lon, None)
                n += 1
                if r["type"] != row["type"]:
                    worst["type"] += 1
                worst["mag"] = max(worst["mag"], abs(round(r["smag"], 4) - row["mag"]))
                worst["alt"] = max(worst["alt"], abs(round(r["alt_deg"], 2) - row["alt"]))
                worst["last"] = max(worst["last"], min(abs(r["lat_hours"] - row["last"]),
                                                       24 - abs(r["lat_hours"] - row["last"])))
    print(f"selftest: {n} catalogue rows; type mismatches {worst['type']}; max |smag diff| {worst['mag']:.5f}; "
          f"max |alt diff| {worst['alt']:.3f} deg; max |LAT diff| {worst['last'] * 60:.3f} min")
    ok = worst["type"] == 0 and worst["mag"] <= 1.5e-4 and worst["alt"] <= 0.011 and worst["last"] <= 0.002
    print("selftest", "PASS" if ok else "FAIL")
    return ok


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", help="output directory (default results/n6, after the second freeze only)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return 0 if selftest() else 1
    out = Path(a.out) if a.out else DEFAULT_OUT
    if not out.is_absolute():
        out = ROOT / out
    if out.resolve() == DEFAULT_OUT.resolve() and not FROZEN.exists():
        print(f"refusing to write {DEFAULT_OUT}: the second freeze has not happened ({FROZEN} is absent); "
              f"use --out results/build-<agent>/... for a scratch run")
        return 2
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    res = compute()
    txt, cmp_ = report(res)
    res["comparison_with_design_2_3"] = cmp_
    res["summary"] = summary(res)
    res["elements"] = {k: str(jsex_file_for(v[0]).relative_to(ROOT)) for k, v in ECLIPSES.items()}
    res["elements_sha256"] = {k: hashlib.sha256(jsex_file_for(v[0]).read_bytes()).hexdigest()
                              for k, v in ECLIPSES.items()}
    res["run_s"] = round(time.time() - t0, 1)
    (out / "n6.json").write_text(json.dumps(res, indent=1, default=_json_default, ensure_ascii=False),
                                 encoding="utf-8")
    (out / "n6.out.txt").write_text(txt, encoding="utf-8")
    print(txt)
    print(f"wrote {out / 'n6.json'} and n6.out.txt in {res['run_s']} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
