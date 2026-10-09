"""
tools/build_regimes.py -- writes data/prereg/almagest_regimes.json by rule
(A0; DESIGN 6.4, 10.1, 12.1 item 7).  Nothing in the output is chosen by hand.

What the file holds, per set of controls_almagest.json:
  * "projection": the B&M-type projection of 6.4 (option per row), and
    "held_out": the held-out rows of Q_H.  Both equal the lists of
    results/design-revision-v8/alm_rows.out.txt (I13(f)).
  * "regimes": for regime SL at each rounding step (fine, mid, coarse), for
    regime BM, and for the held-out rows at each step, the option and the
    parameter values of every row (6.4's table).
  * "tolerances": the leave-one-set-out ceilings at the three steps.
  * "sensitivities": the reported runs 6.4 names (revision 7's projection,
    all six phase rows at their classes, the bounded primaries, the full
    primary run, the drafter's list values, B&M's 1 d, the emended cruxes).
It holds tolerances and never a date.  The ceiling arithmetic (each maximum
and the record it comes from) is truth-side [AppT 2, 2b], so this tool
writes it only to --arith-out, off the public whitelist.

Inputs:
  data/prereg/controls_almagest.json   the clue file (public)
  results/controls-almagest/slack.json the drafter's slack table (truth-side;
                                       read only by this tool, 6 "Who reads them")
  docs/controls-almagest.md            its 'Summary' line: which records the
                                       text puts at or about greatest elongation
                                       ("alm Table 2", records in no set
                                       included) and the crux readings the
                                       slack summary uses (truth-side note)

The rules (6.4), as code:
  projection   interval rows structural (or their primary, for a crux);
               moon-phase rows at their phase class only where the words state
               the phase: none for every row whose own 'none' option says the
               phase is not stated in words, and for B.9, whose class is read
               off the measured 92 deg [r1v5 N15f]; planet rows of B&M's kinds
               (ge_*, visible_only, visible_before_sunrise, bm_*) at their
               primary, a ge_*_within_j primary replaced by its literal
               ge_*_same_apparition option; the season row at its primary;
               everything else none.
  held out     star rows at their primary (none holds nothing out); planet
               rows whose primary is a position or an opposition; moon-phase
               rows at 'positional', else 'elongation_tol'; the eclipse row.
  regime SL    the projection's options; greatest-elongation k = the
               leave-one-set-out ceiling for the row's body; every other list
               at its most lenient value.
  regime BM    B&M's proxy where the row offers it (bm_mwra_k 1.5 d,
               bm_venus_lead 90 min); else ge_true_k at 1.5 d where offered;
               else the row's option under the projection; every other list
               at its middle value (lower middle for an even count).
  held-out     each row's relation class: planet-star (star rows, J.7's
               position), planet-Moon (positional moon rows), Sun-Moon
               (elongation_tol), opposition (opp_*); tolerance = the largest
               measured |computed - stated| among the class's records outside
               the set (records in no set included), rounded up at the step;
               a lunar class with no record outside the set falls back to the
               pooled lunar classes outside the set.
  ceilings     fine/mid/coarse = up to the next 0.01/0.05/0.1 deg or
               0.1/0.5/1 d.

Usage (from C:\\Projects\\odybench):
    py tools/build_regimes.py                 # writes the regime file and the arithmetic
    py tools/build_regimes.py --check         # also the truth-side checks (counts only)
    py tools/build_regimes.py --selftest      # synthetic slack table only
"""
from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import io
import json
import math
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLUES = ROOT / "data" / "prereg" / "controls_almagest.json"
SLACK = ROOT / "results" / "controls-almagest" / "slack.json"
SUMMARY = ROOT / "docs" / "controls-almagest.md"
OUT = ROOT / "data" / "prereg" / "almagest_regimes.json"
ARITH = ROOT / "results" / "build-A0" / "regimes_arithmetic_truth.json"
ALM_ROWS_OUT = ROOT / "results" / "design-revision-v8" / "alm_rows.out.txt"
HELDOUT_CEILINGS_V6 = ROOT / "results" / "design-revision-v6" / "heldout_ceilings.json"
DESIGN = ROOT / "DESIGN.md"

STEPS = {"fine": {"deg": 0.01, "days": 0.1}, "mid": {"deg": 0.05, "days": 0.5},
         "coarse": {"deg": 0.1, "days": 1.0}}
STEP_ORDER = ("fine", "mid", "coarse")
REPORTED_SETS = ("ALM-C",)                       # 6.3.5: IV.6.14 is counted once, in gate 3a
MEASURED_PHASE = ("ALM-B.9",)                    # 6.4: class read off the measured 92 deg [r1v5 N15f]
NOT_IN_WORDS = "not stated in words"
BM_PLANET = ("ge_", "visible_only", "visible_before_sunrise", "bm_")
# 6.4: "A record contributes nothing when the drafter marks its star as not
# securely identified (X.1.6), or when the stated value is not in the words
# (X.4.3's 1/4 deg, which came from Ptolemy's computed lunar longitude)"
INSECURE_STAR_RECORDS = ("X.1.6",)
MOON_VALUE_NOT_IN_WORDS = ("X.4.3",)
PREDICATE_SENSITIVITIES = ("projection_rev7", "all_phase_rows", "bounded_primary", "bm_k_1d")
BM_GE_K = 1.5                                    # B&M's +/-1 integer day as a continuous tolerance [r1 N13]
BM_GE_K_REPORTED = 1.0
BM_MWRA_K = 1.5
BM_VENUS_LEAD = 90.0
SAME_APPARITION_VISIBLE_MIN = 30.0               # the visible_only minimum at either regime's value (6.4)
LENIENT = {"j_days": max, "k_days": max, "tolerance_days": max, "tolerance_deg": max, "time_tol_h": max,
           "min_minutes_between_body_and_sun_horizon_crossings": min, "min_altitude_deg": min,
           "lead_min": min}


# ------------------------------------------------------------ small helpers

def ceil_step(x: float, step: float) -> float:
    """x rounded up to the next multiple of step (a value on a multiple stays)."""
    k = math.ceil(round(x / step, 9))
    nd = max(0, -int(math.floor(math.log10(step))) + 1)
    return round(k * step, nd)


def opt_name(o: dict) -> str:
    return o.get("name") or o.get("option")


def options(row: dict) -> list[dict]:
    return row.get("fork_options") or []


def primary(row: dict) -> str | None:
    return next((opt_name(o) for o in options(row) if o.get("primary")), None)


def option(row: dict, name: str) -> dict | None:
    return next((o for o in options(row) if opt_name(o) == name), None)


def middle(values: list):
    """The middle listed value (lower middle for an even count), on the sorted list."""
    v = sorted(values)
    return v[(len(v) - 1) // 2]


def most_lenient(key: str, values: list):
    if key == "umbral_mag_range":                # the widest range
        return [min(r[0] for r in values), max(r[1] for r in values)]
    fn = LENIENT.get(key)
    if fn is None:
        raise KeyError(f"no leniency direction for list parameter {key!r}")
    return fn(values)


def lists_at(op: dict | None, how: str) -> dict:
    """An option's operational dict with every list taken at the regime's value:
    how = 'lenient' (regime SL) or 'middle' (regime BM)."""
    out = {}
    for k, v in (op or {}).items():
        if isinstance(v, list) and v and not isinstance(v[0], str):
            if k == "umbral_mag_range" and how == "middle":
                out[k] = middle([tuple(r) for r in v])
                out[k] = list(out[k])
            else:
                out[k] = most_lenient(k, v) if how == "lenient" else middle(v)
        else:
            out[k] = v
    return out


def body_of(row: dict) -> str | None:
    """The planet a planet row speaks of: the first word of its statement."""
    m = re.match(r"\s*(Mercury|Venus|Mars|Jupiter|Saturn)\b", row.get("statement") or "")
    return m.group(1).lower() if m else None


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ------------------------------------------- row predicates: body, side, instant
#
# The clue file's operational dicts carry the option and its numbers, but not
# the body a planet row speaks of, the side of the Sun it is seen on, or the
# instant 6.4 evaluates it at.  Those are in the row's statement.  This tool
# reads them off the statement by the fixed rules below and writes them into
# the regime file, so that the search reads operational fields and this file
# only (10.3: an unknown value is an error, never a default).
#   body     the first planet named in the statement; moon-phase rows: moon;
#            the season row: sun
#   side     morning: 'morning star', 'morning object', 'before dawn',
#            'before sunrise'; evening: 'evening star', '(evening)'
#   instant  (6.4) a stated equinoctial hour before or after midnight or noon:
#            local apparent time; a stated seasonal hour of the night: the
#            middle of that hour; otherwise the side's twilight instant, the
#            Sun 8 deg below the horizon ('dawn' or 'evening'), which is also
#            6.4's rule for the hourless records.

_PLANET_WORD = re.compile(r"\b(Mercury|Venus|Mars|Jupiter|Saturn)\b")
_NUMWORD = {"one": 1.0, "two": 2.0, "three": 3.0, "four": 4.0, "five": 5.0, "six": 6.0}
_HOUR = re.compile(r"(\d+(?:\.\d+)?(?: \d+/\d+)?|one|two|three|four|five|six) (?:equinoctial )?hours? "
                   r"(before|after) (midnight|noon)", re.I)
_ORDINAL = {w: i + 1 for i, w in enumerate("first second third fourth fifth sixth seventh eighth ninth tenth "
                                           "eleventh twelfth".split())}
_NIGHT_HOUR = re.compile(r"\b(" + "|".join(_ORDINAL) + r")\b(?: \([^)]*\))? hour of the night", re.I)
_MORNING = re.compile(r"morning (?:star|object)|before (?:dawn|sunrise)", re.I)
_EVENING = re.compile(r"evening star|\(evening\)", re.I)


def _number(s: str) -> float:
    s = s.strip().lower()
    if s in _NUMWORD:
        return _NUMWORD[s]
    parts = s.split()
    x = float(parts[0])
    if len(parts) == 2:
        a, b = parts[1].split("/")
        x += float(a) / float(b)
    return x


def row_predicate(row: dict) -> dict:
    """{'body', 'side', 'instant', 'words'} of a planet, moon-phase or season row,
    read off its statement by the rules above.  Raises on a row they do not cover."""
    s = row.get("statement") or ""
    cid, kind = row["clue_id"], row["kind"]
    words = []
    if kind == "planet":
        m = _PLANET_WORD.search(s)
        if not m:
            raise ValueError(f"{cid}: no planet named in the statement")
        body = m.group(1).lower()
        words.append(m.group(0))
    elif kind == "moon-phase":
        body = "moon"
    elif kind == "season":
        body = "sun"
    else:
        raise ValueError(f"{cid}: no predicate rule for row kind {kind!r}")
    mm, me = _MORNING.search(s), _EVENING.search(s)
    side = None
    if mm and not me:
        side, w = "morning", mm.group(0)
    elif me and not mm:
        side, w = "evening", me.group(0)
    elif mm and me:
        # both words occur (a moon row beside an evening star seen before sunrise): the planet's own side
        # decides only planet rows, and there the first-named side is the record's
        if kind == "planet":
            raise ValueError(f"{cid}: both morning and evening words in a planet row")
        side, w = None, None
    else:
        w = None
    if w:
        words.append(w)
    hm, nm = _HOUR.search(s), _NIGHT_HOUR.search(s)
    if hm:
        n, rel, ref = _number(hm.group(1)), hm.group(2).lower(), hm.group(3).lower()
        base = 24.0 if ref == "midnight" else 12.0
        lat = (base - n if rel == "before" else base + n) % 24.0
        instant = {"kind": "lat", "hours": round(lat, 6)}
        words.append(hm.group(0))
    elif nm:
        instant = {"kind": "night_hour", "hour": _ORDINAL[nm.group(1).lower()], "point": "middle"}
        words.append(nm.group(0))
    elif side == "morning":
        instant = {"kind": "sun_alt", "deg": -8.0, "part": "morning"}
    elif side == "evening":
        instant = {"kind": "sun_alt", "deg": -8.0, "part": "evening"}
    else:
        raise ValueError(f"{cid}: no hour and no side in the statement, so no instant (6.4)")
    if kind == "planet" and side is None:
        raise ValueError(f"{cid}: a planet row with no morning or evening word")
    return {"body": body, "side": side, "instant": instant, "words": words}


# ------------------------------------------------------- projection (6.4)

def unstated_phase_rows(clues: list[dict]) -> set[str]:
    """Moon-phase rows whose own 'none' option says the phase is not stated in words."""
    out = set()
    for c in clues:
        if c["kind"] != "moon-phase":
            continue
        for o in options(c):
            if opt_name(o) == "none" and NOT_IN_WORDS in (o.get("justification") or ""):
                out.add(c["clue_id"])
    return out


def project(clues: list[dict]) -> dict[str, dict]:
    """{set: {"projection": [(clue_id, option)], "held_out": [(clue_id, option)],
    "outside": [clue_id]}} in clue-file order, by 6.4's rules."""
    none_phase = unstated_phase_rows(clues) | set(MEASURED_PHASE)
    by_set: dict[str, list] = {}
    for c in clues:
        by_set.setdefault(c["set"], []).append(c)
    out = {}
    for sid in sorted(by_set):
        proj, held, outside = [], [], []
        for c in by_set[sid]:
            names = [opt_name(o) for o in options(c)]
            prim = primary(c)
            cid, kind = c["clue_id"], c["kind"]
            in_proj = in_held = False
            if kind == "interval":
                proj.append((cid, prim or "structural"))
                in_proj = True
            elif kind == "moon-phase":
                proj.append((cid, "none" if cid in none_phase else "phase_class"))
                in_proj = True
                if "positional" in names:
                    held.append((cid, "positional"))
                    in_held = True
                elif "elongation_tol" in names:
                    held.append((cid, "elongation_tol"))
                    in_held = True
            elif kind == "planet":
                if prim and prim.startswith(BM_PLANET):
                    if prim.endswith("_within_j"):
                        lit = prim.replace("_within_j", "_same_apparition")
                        if lit not in names:
                            raise ValueError(f"{cid}: no literal option {lit}")
                        proj.append((cid, lit))
                    else:
                        proj.append((cid, prim))
                    in_proj = True
                else:
                    held.append((cid, prim))
                    in_held = True
            elif kind == "season":
                proj.append((cid, prim))
                in_proj = True
            elif kind == "star":
                if prim and prim != "none":
                    held.append((cid, prim))
                    in_held = True
            elif kind == "eclipse-lunar":
                held.append((cid, prim))
                in_held = True
            else:
                raise ValueError(f"{cid}: unknown row kind {kind!r}")
            if not in_proj and not in_held:
                outside.append(cid)
        out[sid] = {"projection": proj, "held_out": held, "outside": outside}
    return out


def kept_phase_rows(clues):
    phase = sorted(c["clue_id"] for c in clues if c["kind"] == "moon-phase")
    return [p for p in phase if p not in unstated_phase_rows(clues) | set(MEASURED_PHASE)]


# --------------------------------------------- the slack table and its summary

def parse_summary(text: str) -> dict:
    """From the note's Summary: per body, the records the text puts at or about
    greatest elongation, and the crux readings the summary uses.
    Returns {"records": {body: [ids]}, "cruxes": {id: "emended"|"printed"}}."""
    i = text.index("**Summary: |record")
    block = text[i:i + 4000]
    rec, cruxes = {}, {}
    for m in re.finditer(r"^- (\w+) \(n = (\d+); ([^)]*)\):.*?\n(?:  - .*\n)*?  - sorted: ([^\n]+)", block, re.M):
        body, n, readings, sorted_ = m.group(1), int(m.group(2)), m.group(3), m.group(4)
        ids = [t.strip().split()[0] for t in sorted_.split(",") if t.strip()]
        if len(ids) != n:
            raise ValueError(f"summary for {body}: n = {n} but {len(ids)} records")
        rec[body] = ids
        for part in readings.split(","):
            pm = re.match(r"\s*([IVX]+\.[\w.]+) (?:at its (emended) date|as (printed))", part)
            if pm:
                cruxes[pm.group(1)] = pm.group(2) or pm.group(3)
    if not rec:
        raise ValueError("no Summary block found")
    return {"records": rec, "cruxes": cruxes}


def slack_rows(slack: list[dict], cruxes: dict) -> dict[str, dict]:
    """{record id: slack row}, one row per record: a crux at the summary's reading."""
    out = {}
    for r in slack:
        want = cruxes.get(r["id"])
        if want and not r["reading"].startswith(want):
            continue
        if r["id"] in out:
            raise ValueError(f"two slack rows for {r['id']}")
        out[r["id"]] = r
    return out


_INEQ_BEYOND = re.compile(r"more than|at least|>|\u2265", re.I)
_INEQ_WITHIN = re.compile(r"or less|at most|less than|<|\u2264", re.I)
_LAT_WORD = re.compile(r"\b(north|south)\b", re.I)
_LON_WORD = re.compile(r"\b(east|west|rear|ahead|preced)", re.I)


def inequalities(reading: str) -> dict[str, str]:
    """{component: 'beyond' | 'within'} for the inequality clauses of a stated
    relation: a clause that bounds a north/south distance bears on dlat, an
    east/west one on dlon (read off the words at run time)."""
    out = {}
    for clause in re.split(r";", reading or ""):
        kind = "beyond" if _INEQ_BEYOND.search(clause) else ("within" if _INEQ_WITHIN.search(clause) else None)
        if not kind:
            continue
        if _LAT_WORD.search(clause):
            out["dlat"] = kind
        elif _LON_WORD.search(clause):
            out["dlon"] = kind
    return out


def _component(c: float, s: float, ineq: str | None) -> float:
    """|computed - stated|, or 0 for an inequality that holds."""
    if ineq == "beyond" and c * s > 0 and abs(c) >= abs(s):
        return 0.0
    if ineq == "within" and c * s >= 0 and abs(c) <= abs(s):
        return 0.0
    return abs(c - s)


def star_offset(rid: str, s: dict) -> float | None:
    """The planet-star measured offset of one stated relation (6.4's class table)."""
    if rid in INSECURE_STAR_RECORDS or s.get("kind") in ("note_only", "nearest"):
        return None
    if s["kind"] == "conj":                      # a stated occultation: the separation at the record instant
        return float(s["sep"])
    ineq = inequalities(s.get("reading", ""))
    vals = []
    for comp in ("dlon", "dlat"):
        st = s.get(f"{comp}_s")
        if st is None:
            continue
        vals.append(_component(float(s[f"{comp}_c"]), float(st), ineq.get(comp)))
    if "dist_s" in s:
        vals.append(abs(float(s["dist_c"]) - float(s["dist_s"])))
    if "beyond_pollux_s" in s:
        vals.append(abs(float(s["beyond_pollux_c"]) - float(s["beyond_pollux_s"])))
        vals.append(abs(float(s.get("perp_c", 0.0))))
    return max(vals) if vals else None


def measured(rows: dict[str, dict], ge_records: dict[str, list]) -> dict[str, dict[str, float]]:
    """{class: {record: measured offset}} for the four held-out classes and the
    two greatest-elongation classes (ge:mercury, ge:venus; |record - true GE|, days)."""
    m = {"planet-star": {}, "planet-Moon": {}, "Sun-Moon": {}, "opposition": {}}
    for rid, r in rows.items():
        offs = [o for o in (star_offset(rid, s) for s in (r.get("stars") or [])) if o is not None]
        if offs:
            m["planet-star"][rid] = max(offs)
        mo = r.get("moon")
        if mo and "dlon_s" in mo and rid not in MOON_VALUE_NOT_IN_WORDS:
            m["planet-Moon"][rid] = abs(float(mo["dlon_c"]) - float(mo["dlon_s"]))
        ms = r.get("moonsun")
        if ms:
            m["Sun-Moon"][rid] = abs(float(ms["computed"]) - float(ms["stated"]))
        if r.get("off_opp_mean_d") is not None:
            m["opposition"][rid] = abs(float(r["off_opp_mean_d"]))
    for body, ids in ge_records.items():
        cls = f"ge:{body}"
        m[cls] = {}
        for rid in ids:
            r = rows.get(rid)
            if r is None or r.get("off_ge_true_d") is None:
                raise ValueError(f"no greatest-elongation offset for {rid}")
            m[cls][rid] = abs(float(r["off_ge_true_d"]))
    return m


def ceiling(m: dict[str, dict], cls: str, inset: set[str], unit: str):
    """The leave-one-set-out ceiling of a class at the three steps, with its
    arithmetic: the maximum outside the set (records in no set included);
    a lunar class with none falls back to the pooled lunar classes."""
    out = {rid: v for rid, v in m[cls].items() if rid not in inset}
    pooled = False
    if not out and cls in ("planet-Moon", "Sun-Moon"):
        out = {rid: v for k in ("planet-Moon", "Sun-Moon") for rid, v in m[k].items() if rid not in inset}
        pooled = True
    if not out:
        raise ValueError(f"class {cls} has no record outside the set")
    rid = max(out, key=out.get)
    vals = {s: ceil_step(out[rid], STEPS[s][unit]) for s in STEP_ORDER}
    return vals, {"max": out[rid], "record": rid, "pooled_lunar_fallback": pooled,
                  "n_outside": len(out), "unit": unit, "rounded": vals}


# ------------------------------------------------------------ the regimes

def held_class(row: dict, opt: str) -> str | None:
    if row["kind"] == "star":
        return "planet-star"
    if row["kind"] == "planet":
        if opt.startswith("opp_"):
            return "opposition"
        if opt == "positional":
            return "planet-star"
    if row["kind"] == "moon-phase":
        return "planet-Moon" if opt == "positional" else ("Sun-Moon" if opt == "elongation_tol" else None)
    return None                                   # the eclipse row of the reported ALM-C


def _ge_k(row, tol):
    b = body_of(row)
    if b not in tol:
        raise ValueError(f"{row['clue_id']}: no greatest-elongation ceiling for body {b}")
    return tol[b]


def sl_entry(row: dict, opt: str, ge_tol: dict, opp_tol: float | None, step: str) -> dict:
    """Regime SL: the option, with its lists at the most lenient value and the
    greatest-elongation (and, in the full run, opposition) k at the ceiling."""
    if opt in ("structural", "none"):
        return {"option": opt, "params": {}}
    op = option(row, opt)
    params = lists_at(op.get("operational") if op else None, "lenient")
    if opt in ("ge_true_k", "ge_mean_k"):
        params["k_days"] = _ge_k(row, ge_tol)[step]
    if opt.startswith("opp_") and opp_tol is not None:
        params["k_days"] = opp_tol[step]
    if opt.endswith("_same_apparition"):
        params = {"bound": "same_apparition", "visible_min_minutes": SAME_APPARITION_VISIBLE_MIN,
                  "visible_option": "visible_only"}
    return {"option": opt, "params": params}


def bm_option(row: dict, proj_opt: str) -> str:
    """Regime BM's option: B&M's proxy where offered; else ge_true_k for a
    greatest-elongation row; else the projection's option."""
    if proj_opt in ("structural", "none") or row["kind"] != "planet":
        return proj_opt
    names = [opt_name(o) for o in options(row)]
    for proxy in ("bm_mwra_k", "bm_venus_lead"):
        if proxy in names:
            return proxy
    if "ge_true_k" in names:
        return "ge_true_k"
    return proj_opt


def bm_entry(row: dict, opt: str, ge_k: float = BM_GE_K) -> dict:
    if opt in ("structural", "none"):
        return {"option": opt, "params": {}}
    op = option(row, opt)
    params = lists_at(op.get("operational") if op else None, "middle")
    if opt in ("ge_true_k", "ge_mean_k"):
        params["k_days"] = ge_k
    elif opt == "bm_mwra_k":
        params["k_days"] = BM_MWRA_K
    elif opt == "bm_venus_lead":
        params["lead_min"] = BM_VENUS_LEAD
    elif opt.endswith("_same_apparition"):
        params = {"bound": "same_apparition", "visible_min_minutes": SAME_APPARITION_VISIBLE_MIN,
                  "visible_option": "visible_only"}
    return {"option": opt, "params": params}


def held_entry(row: dict, opt: str, tol: dict | None, step: str) -> dict:
    cls = held_class(row, opt)
    op = option(row, opt)
    params = dict((op or {}).get("operational") or {})
    if cls == "opposition":
        params["k_days"] = tol[step]
    elif cls is not None:
        params["tolerance_deg"] = tol[step]
    else:
        params = lists_at(params, "lenient")
    return {"option": opt, "class": cls, "params": params}


def build(clues_doc: dict, slack: list[dict], summary: dict) -> tuple[dict, dict]:
    clues = clues_doc["clues"]
    rows_by_id = {c["clue_id"]: c for c in clues}
    sets = {s["set"]: s for s in clues_doc["sets"]}
    proj = project(clues)
    srows = slack_rows(slack, summary["cruxes"])
    m = measured(srows, summary["records"])
    counted = [s for s in sorted(sets) if s not in REPORTED_SETS]
    out_sets, arith = {}, {"classes": {k: dict(sorted(v.items(), key=lambda t: -t[1])) for k, v in m.items()},
                           "sets": {}}
    for sid in sorted(sets):
        inset = set(sets[sid]["records"])
        p = proj[sid]
        set_rows = [c for c in clues if c["set"] == sid]
        bodies = sorted({body_of(c) for c in set_rows if c["kind"] == "planet"} - {None})
        ge_tol, ar = {}, {}
        for b in bodies:
            if f"ge:{b}" in m:
                ge_tol[b], ar[f"ge:{b}"] = ceiling(m, f"ge:{b}", inset, "days")
        opp_tol, ar["opposition"] = ceiling(m, "opposition", inset, "days")
        held_tol = {}
        for cid, opt in p["held_out"]:
            cls = held_class(rows_by_id[cid], opt)
            if cls and cls not in held_tol:
                unit = "days" if cls == "opposition" else "deg"
                held_tol[cls], ar[cls] = ceiling(m, cls, inset, unit)
        projected = dict(p["projection"])
        sl, bm, ho = {}, {}, {}
        for step in STEP_ORDER:
            sl[step] = {}
            for c in set_rows:
                cid = c["clue_id"]
                if cid in projected:
                    sl[step][cid] = sl_entry(c, projected[cid], ge_tol, None, step)
                else:
                    sl[step][cid] = {"option": "none", "params": {},
                                     "why": "held out (6.4)" if cid in dict(p["held_out"]) else
                                            "not in B&M's grammar; primary none (6.4)"}
            ho[step] = {cid: held_entry(rows_by_id[cid], opt, held_tol.get(held_class(rows_by_id[cid], opt)), step)
                        for cid, opt in p["held_out"]}
        for c in set_rows:
            cid = c["clue_id"]
            if cid in projected:
                bm[cid] = bm_entry(c, bm_option(c, projected[cid]))
            else:
                bm[cid] = {"option": "none", "params": {}, "why": sl["coarse"][cid]["why"]}
        tolerances = {"greatest_elongation_days": {b: ge_tol[b] for b in bodies if b in ge_tol},
                      "opposition_full_run_days": opp_tol,
                      "held_out": {cls: {**v, "pooled_lunar_fallback": ar[cls]["pooled_lunar_fallback"]}
                                   for cls, v in held_tol.items()}}
        sens = sensitivities(sid, set_rows, projected, dict(p["held_out"]), ge_tol, opp_tol, held_tol)
        # the rows the gate's runs and its no-star sensitivities evaluate get a predicate (body, side, instant)
        pred_ids = {cid for cid, opt in p["projection"]
                    if opt not in ("structural", "none") and rows_by_id[cid]["kind"] != "interval"}
        for key in PREDICATE_SENSITIVITIES:
            pred_ids |= set(sens.get(key, {}).get("rows", {}))
        row_preds = {c["clue_id"]: row_predicate(c) for c in set_rows if c["clue_id"] in pred_ids}
        out_sets[sid] = {"counted": sid not in REPORTED_SETS,
                         "projection": dict(p["projection"]),
                         "held_out": dict(p["held_out"]),
                         "outside": p["outside"],
                         "tolerances": tolerances,
                         "regimes": {"SL": sl, "BM": bm, "held_out": ho},
                         "row_predicates": row_preds,
                         "sensitivities": sens}
        arith["sets"][sid] = ar
    doc = {
        "schema": "odybench almagest_regimes v1 (DESIGN 6.4, 10.2, 12.1 item 7)",
        "written_by": "tools/build_regimes.py (A0), by rule; nothing in it is chosen by hand",
        "clue_file": "data/prereg/controls_almagest.json",
        "clue_file_sha256": sha256(CLUES) if CLUES.exists() else None,
        "inputs": {"slack_table": "results/controls-almagest/slack.json (truth-side; read only by this tool)",
                   "summary": "docs/controls-almagest.md, its Summary of alm Table 2 (the records at or about "
                              "greatest elongation, records in no set included, and the crux readings)"},
        "counted_sets": counted,
        "reported_sets": list(REPORTED_SETS),
        "steps": STEPS,
        "step_order": list(STEP_ORDER),
        "kept_phase_rows": kept_phase_rows(clues),
        "same_apparition": {
            "options": ["ge_after_same_apparition", "ge_before_same_apparition"],
            "frozen": "visible on the row's own day (the day its offset gives): the body on the row's side of "
                      "the Sun, and its rise lead (morning) or set lag (evening) at least the row's visible_only "
                      "minimum at the regime's value, 30 min in both regimes; the apparition is the interval "
                      "between the two geocentric conjunctions of the body with the Sun, in apparent ecliptic "
                      "longitude, that bracket the record's instant; the greatest elongation on the row's side, "
                      "from the true Sun (the event of ge_true_k), lies in it, after the record's instant "
                      "(ge_after) or before it (ge_before) (6.4, 10.3)",
            "side": "the same without the visibility clause (same_apparition_side); scored on every leg of gate 3b "
                    "and reported, read only by Q_score3b (6.4)"},
        "instants": "each row at the drafter's instant convention: 'evening' and 'dawn' are the moments the Sun is "
                    "8 deg below the horizon, stated hours are local apparent time; visible_before_sunrise at the "
                    "hour the row states, else at dawn (Sun at -8 deg); hourless records at the dawn or evening "
                    "instant of their civil day (6.4) [r3v7 R3-5; lca2 item 5]",
        "row_predicate_rules": "per set, 'row_predicates' gives the body, side and instant of every row the gate's "
                               "runs evaluate (and of the rows of the reported runs that need no star), read off the "
                               "row's statement by fixed rules: body = the first planet named (moon-phase rows: moon; "
                               "the season row: sun); side = morning for 'morning star', 'morning object', 'before "
                               "dawn', 'before sunrise', evening for 'evening star', '(evening)'; instant = a stated "
                               "equinoctial hour before or after midnight or noon, as local apparent time; a stated "
                               "seasonal hour of the night, at the middle of that hour; else the side's twilight "
                               "instant, the Sun at -8 deg (6.4). 'words' lists the matched fragments. Added by L3 "
                               "(lean run, 2026-10-09) so that the search reads operational fields and this file only",
        "regime_rules": {
            "SL": "the row's projection option; greatest-elongation k = the leave-one-set-out ceiling of the "
                  "row's body; every other list at its most lenient value (6.4)",
            "BM": f"B&M's proxy where the row offers it (bm_mwra_k {BM_MWRA_K} d, bm_venus_lead {BM_VENUS_LEAD:g} "
                  f"min); else ge_true_k at {BM_GE_K} d where offered (a greatest-elongation row); else the "
                  "projection's option; every other list at its middle value, lower middle for an even count; "
                  "no rounding step (6.4) [r1 N3 fix]",
            "held_out": "each held-out row at its relation class's leave-one-set-out ceiling at the step (6.4)",
            "most_lenient": "the largest value of a bound or tolerance list (j_days, k_days, tolerance_days, "
                            "tolerance_deg, time_tol_h), the smallest of a minimum (minutes, altitude, lead), the "
                            "widest range",
            "ceiling_steps": "fine, mid, coarse = up to the next 0.01, 0.05, 0.1 deg or 0.1, 0.5, 1 d (6.4)"},
        "ceiling_arithmetic": "truth-side [AppT 2, 2b]: each maximum and the record it comes from are written "
                              "only to results/build-A0/regimes_arithmetic_truth.json, off the public whitelist; "
                              "their meaning per set is truth-side (13 row 60)",
        "sets": out_sets,
    }
    return doc, arith


def sensitivities(sid, set_rows, projected, held, ge_tol, opp_tol, held_tol) -> dict:
    """The reported runs of 6.4, as row overrides on regime SL (per step) and BM."""
    rows = {c["clue_id"]: c for c in set_rows}
    out = {}

    def both(cid, opt):
        c = rows[cid]
        return {"SL": {s: sl_entry(c, opt, ge_tol, opp_tol, s) for s in STEP_ORDER},
                "BM": bm_entry(c, opt)}

    rev7 = {cid: both(cid, "phase_class") for cid in ("ALM-A.2", "ALM-A.5", "ALM-B.2") if cid in rows}
    if rev7:
        out["projection_rev7"] = {"rows": rev7, "source": "6.4: revision 7's projection, with A.2, A.5 and B.2 "
                                                          "at their inferred classes"}
    allph = {cid: both(cid, "phase_class") for cid, c in rows.items()
             if c["kind"] == "moon-phase" and projected.get(cid) == "none"}
    if allph:
        out["all_phase_rows"] = {"rows": allph, "source": "6.4: all six phase rows at their classes"}
    bounded = {}
    for cid, c in rows.items():
        prim = primary(c)
        if prim and prim.endswith("_within_j") and projected.get(cid, "").endswith("_same_apparition"):
            bounded[cid] = both(cid, prim)
    if bounded:
        out["bounded_primary"] = {"rows": bounded, "source": "6.4: the bounded primary (j = 7-60 d, the "
                                                             "drafter's inference) is reported as a sensitivity"}
    full = {}
    for cid, c in rows.items():
        prim = primary(c) or "structural"
        if c["kind"] == "interval" and not options(c):
            continue
        sl = {}
        for s in STEP_ORDER:
            cls = held_class(c, prim) if prim not in ("none", "structural") else None
            if cls in held_tol:
                e = held_entry(c, prim, held_tol[cls], s)
            else:
                e = sl_entry(c, prim, ge_tol, opp_tol, s)
            sl[s] = e
        bm = bm_entry(c, prim)
        if prim.startswith("opp_"):
            op = option(c, prim)
            bm["params"]["k_days"] = middle(op["operational"]["k_days"])
        if all(sl[s] == {"option": projected.get(cid), "params": sl[s]["params"]} for s in STEP_ORDER) and \
                projected.get(cid) == prim:
            continue
        full[cid] = {"SL": sl, "BM": bm}
    if full:
        out["full_primary"] = {"rows": full, "source": "6.4: the full primary run (every row at its primary; "
                                                       "the opposition k at the full-run ceiling in SL and the "
                                                       "middle value in BM)"}
    lists = {}
    for cid, opt in held.items():
        op = option(rows[cid], opt)
        lists[cid] = {"option": opt, "params": lists_at((op or {}).get("operational"), "lenient")}
    if lists:
        out["held_out_list_values"] = {"rows": lists, "source": "6.4: the drafter's list values, most lenient, "
                                                                "reported as a sensitivity of Q_H"}
    k1 = {cid: bm_entry(rows[cid], "ge_true_k", BM_GE_K_REPORTED) for cid in projected
          if bm_option(rows[cid], projected[cid]) == "ge_true_k"}
    if k1:
        out["bm_k_1d"] = {"rows": k1, "source": "6.4: B&M's +/-1 d reported beside 1.5 d"}
    emend = {cid: {"option": "mean_sun_emended", "params": dict(option(rows[cid], "mean_sun_emended")["operational"])}
             for cid in projected if option(rows[cid], "mean_sun_emended")}
    if emend:
        out["cruxes_emended"] = {"rows": emend, "source": "6.4: the two cruxes run at their primary, as printed; "
                                                          "the emended intervals are reported"}
    if sid == "ALM-K":
        out["site_babylon"] = {"site": "babylon", "source": "6.4: Babylon is a sensitivity for ALM-K"}
    return out


# ---------------------------------------------------- reference comparisons

def parse_alm_rows(path: Path) -> dict[str, tuple[list, list]]:
    """{set: (projection list, held-out list)} from alm_rows' printed output."""
    out, sid = {}, None
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s.startswith("ALM-") and (" counted" in s or " reported" in s):
            sid = s.split()[0]
            out[sid] = ([], [])
        elif s.startswith("projection:") and sid:
            out[sid][0].extend(x.strip() for x in s.split(":", 1)[1].split(","))
        elif s.startswith("held out") and sid:
            body = s.split(":", 1)[1].strip()
            if body != "(none)":
                out[sid][1].extend(x.strip() for x in body.split(","))
    return out


def as_lists(doc: dict) -> dict[str, tuple[list, list]]:
    return {sid: ([f"{k}:{v}" for k, v in s["projection"].items()], [f"{k}:{v}" for k, v in s["held_out"].items()])
            for sid, s in doc["sets"].items()}


def compare_alm_rows(doc: dict, path: Path = ALM_ROWS_OUT) -> list[str]:
    ref, got = parse_alm_rows(path), as_lists(doc)
    diffs = []
    for sid in sorted(set(ref) | set(got)):
        if ref.get(sid) != got.get(sid):
            diffs.append(sid)
    return diffs


def check_named_options(doc: dict, clues_doc: dict) -> list[str]:
    """I13(f): every option a regime names exists in the clue file."""
    names = {c["clue_id"]: {opt_name(o) for o in options(c)} | ({"structural"} if not options(c) else set())
             for c in clues_doc["clues"]}
    bad = []

    def chk(cid, e):
        o = e["option"]
        if o not in names[cid] and o != "none":
            bad.append(f"{cid}:{o}")

    for sid, s in doc["sets"].items():
        for cid, o in list(s["projection"].items()) + list(s["held_out"].items()):
            if o not in names[cid] and o != "none":
                bad.append(f"{cid}:{o}")
        for step in STEP_ORDER:
            for cid, e in s["regimes"]["SL"][step].items():
                chk(cid, e)
            for cid, e in s["regimes"]["held_out"][step].items():
                chk(cid, e)
        for cid, e in s["regimes"]["BM"].items():
            chk(cid, e)
    return bad


def _parse_t2(design: str) -> dict:
    """The regime-SL ceilings and the held-out tolerances that Appendix T (T2,
    T2b) states, read at run time from the full design (truth tier)."""
    t = re.sub(r"\s+", " ", design[design.index("## Appendix T."):])
    out = {}
    m = re.search(r"Mercury ([\d.]+), ([\d.]+) and ([\d.]+) d \((ALM-[A-L]): ([\d.]+), ([\d.]+) and ([\d.]+) d\); "
                  r"Venus ([\d.]+), ([\d.]+) and ([\d.]+) d; opposition ([\d.]+), ([\d.]+) and ([\d.]+) d", t)
    if m:
        g = [float(x) if re.fullmatch(r"[\d.]+", x) else x for x in m.groups()]
        out["mercury"] = g[0:3]
        out["mercury_exception"] = (g[3], g[4:7])
        out["venus"] = g[7:10]
        out["opposition"] = g[10:13]
    for m in re.finditer(r"(planet\u2013Moon|Sun\u2013Moon|planet\u2013star),? ?(ALM-[A-L])? \((?:from [\w.]+'s|pooled,) "
                         r"[\d.]+\u00b0\): ([\d.]+)\u00b0(?:, ([\d.]+)\u00b0, ([\d.]+)\u00b0| at every step)"
                         r"(?:; (ALM-[A-L]) \(from [\w.]+'s [\d.]+\u00b0\): ([\d.]+)\u00b0, ([\d.]+)\u00b0, ([\d.]+)\u00b0)?", t):
        cls = m.group(1).replace("\u2013", "-")
        vals = [float(m.group(3))] * 3 if m.group(4) is None else [float(m.group(3)), float(m.group(4)),
                                                                     float(m.group(5))]
        out.setdefault("held", {}).setdefault(cls, {})[m.group(2) or "*"] = vals
        if m.group(6):
            out["held"][cls][m.group(6)] = [float(m.group(7)), float(m.group(8)), float(m.group(9))]
    m = re.search(r"opposition \(from [\w.]+'s [\d.]+ d\): ([\d.]+), ([\d.]+) and ([\d.]+) d", t)
    if m:
        out.setdefault("held", {})["opposition"] = {"*": [float(x) for x in m.groups()]}
    return out


def consequences(doc: dict, clues_doc: dict, slack: list[dict]) -> dict:
    """R9 and R10 (2.6) from the slack table at the true dates, row by row,
    without new computation: in regime SL (frozen meaning) the number of
    counted sets whose truth passes every projected row, at each step, and in
    regime BM the number that can pass.  Returns counts only."""
    rows_by_id = {c["clue_id"]: c for c in clues_doc["clues"]}
    printed = {}
    for r in slack:
        if r["reading"].startswith("printed"):
            printed.setdefault(r["id"], r)
    unchecked = set()

    def passes(cid, e):
        row = rows_by_id[cid]
        o, p = e["option"], e["params"]
        if o in ("structural", "none", "as_printed"):
            return True
        r = printed.get(row["record"])
        if r is None:
            unchecked.add(cid)
            return True
        if o == "ge_true_k":
            return abs(r["off_ge_true_d"]) <= p["k_days"]
        if o == "visible_only":
            return r.get("rs_min") is not None and r["rs_min"] >= p["min_minutes_between_body_and_sun_horizon_crossings"]
        if o.endswith("_same_apparition"):
            after = o.startswith("ge_after")
            side = r["off_ge_true_d"] < 0 if after else r["off_ge_true_d"] > 0
            return bool(r.get("side_ok")) and side and r.get("rs_min") is not None and r["rs_min"] >= p["visible_min_minutes"]
        if o == "visible_before_sunrise":
            return r.get("body_alt") is not None and r["body_alt"] >= p["min_altitude_deg"]
        if o == "bm_mwra_k":
            return r.get("az_max_off_d") is not None and abs(r["az_max_off_d"]) <= p["k_days"]
        if o == "bm_venus_lead":
            return r.get("rs_kind") == "rise lead" and r["rs_min"] >= p["lead_min"]
        if o == "equinox_tol":
            return abs(r["equinox"]["off_d"]) <= p["tolerance_days"]
        if o == "phase_class":
            cls = p["class"]
            e_deg = (r["moon"]["elong_signed"]) % 360.0
            centre = {"last_quarter": 270.0, "first_quarter": 90.0}.get(cls)
            if centre is None:
                unchecked.add(cid)
                return True
            return abs(e_deg - centre) <= 12.2 * p["tolerance_days"]
        unchecked.add(cid)
        return True

    out = {"SL": {}, "BM": None}
    counted = [s for s, v in doc["sets"].items() if v["counted"]]
    for step in STEP_ORDER:
        out["SL"][step] = sum(all(passes(cid, e) for cid, e in doc["sets"][s]["regimes"]["SL"][step].items())
                              for s in counted)
    out["BM"] = sum(all(passes(cid, e) for cid, e in doc["sets"][s]["regimes"]["BM"].items()) for s in counted)
    out["unchecked_rows"] = len(unchecked)
    return out


def check(doc: dict, arith: dict, clues_doc: dict, slack: list[dict]) -> list[str]:
    """The truth-side checks of 12.1 item 7.  Returns failure labels only; no
    value and no set name is printed."""
    fails = []
    if compare_alm_rows(doc):
        fails.append("projection/held-out lists differ from alm_rows.out.txt")
    if check_named_options(doc, clues_doc):
        fails.append("a named option is missing from the clue file")
    # coarse-step held-out ceilings against revision 6's heldout_ceilings.json
    if HELDOUT_CEILINGS_V6.exists():
        ref = json.loads(HELDOUT_CEILINGS_V6.read_text(encoding="utf-8"))
        key = {"star": "planet-star", "moon": "planet-Moon", "sunmoon": "Sun-Moon", "opp": "opposition"}
        for sid, row in ref.items():
            for k, v in row.items():
                cls = key[k]
                got = arith["sets"][sid].get(cls)
                if got is None:
                    continue
                if abs(got["rounded"]["coarse"] - v["tolerance"]) > 1e-9 or got["record"] != v["record"]:
                    fails.append("a coarse held-out ceiling differs from heldout_ceilings.json")
    else:
        fails.append("heldout_ceilings.json missing")
    # all three steps against Appendix T (T2, T2b), read at run time
    t2 = _parse_t2(DESIGN.read_text(encoding="utf-8"))
    if not {"mercury", "venus", "opposition", "held"} <= set(t2):
        fails.append("could not parse Appendix T's ceilings")
    else:
        exc_set, exc_vals = t2["mercury_exception"]
        for sid, s in doc["sets"].items():
            ge = s["tolerances"]["greatest_elongation_days"]
            if "mercury" in ge:
                want = exc_vals if sid == exc_set else t2["mercury"]
                if [ge["mercury"][st] for st in STEP_ORDER] != want:
                    fails.append("a Mercury ceiling differs from T2")
            if "venus" in ge and [ge["venus"][st] for st in STEP_ORDER] != t2["venus"]:
                fails.append("a Venus ceiling differs from T2")
            if [s["tolerances"]["opposition_full_run_days"][st] for st in STEP_ORDER] != t2["opposition"]:
                fails.append("an opposition ceiling differs from T2")
            for cls, vals in s["tolerances"]["held_out"].items():
                spec = t2["held"].get(cls, {})
                want = spec.get(sid, spec.get("*"))
                if want is None:
                    fails.append(f"no T2b value for a {cls} ceiling")
                elif [vals[st] for st in STEP_ORDER] != want:
                    fails.append(f"a {cls} ceiling differs from T2b")
    # the known consequences of 2.6: R10 (9 of 11 at every step), R9 (at most 5)
    cq = consequences(doc, clues_doc, slack)
    if any(v != 9 for v in cq["SL"].values()):
        fails.append("regime SL does not retain exactly 9 counted truths at every step (R10)")
    if cq["BM"] > 5:
        fails.append("regime BM retains more than 5 counted truths (R9)")
    if cq["unchecked_rows"]:
        fails.append("some projected rows could not be checked from the slack table")
    return sorted(set(fails))


# ------------------------------------------------------------------ selftest

def _synthetic():
    """A two-set synthetic clue file, slack table and summary."""
    clues_doc = {"sets": [{"set": "ALM-X", "records": ["R.1", "R.2"]}, {"set": "ALM-Y", "records": ["R.3"]}],
                 "clues": [
                     {"set": "ALM-X", "clue_id": "ALM-X.1", "kind": "planet", "record": "R.1", "day_offset": 0,
                      "statement": "Mercury is a morning star at its greatest elongation.",
                      "fork_options": [{"name": "ge_true_k", "primary": True, "operational": {"k_days": [1, 2, 3]}},
                                       {"name": "bm_mwra_k", "primary": False, "operational": {"k_days": [1, 2, 3]}},
                                       {"name": "visible_only", "primary": False,
                                        "operational": {"min_minutes_between_body_and_sun_horizon_crossings": [30, 60]}}]},
                     {"set": "ALM-X", "clue_id": "ALM-X.2", "kind": "moon-phase", "record": "R.1", "day_offset": 0,
                      "statement": "The Moon near Mercury at 4 1/2 equinoctial hours before midnight.",
                      "fork_options": [{"name": "phase_class", "primary": True, "operational": {"class": "young_crescent"}},
                                       {"name": "positional", "primary": False, "operational": {"tolerance_deg": [0.5, 1.0]}},
                                       {"name": "none", "primary": False, "operational": None,
                                        "justification": "the Moon's phase is not stated in words"}]},
                     {"set": "ALM-X", "clue_id": "ALM-X.3", "kind": "interval", "record": "R.2", "day_offset": 5,
                      "fork_options": []},
                     {"set": "ALM-X", "clue_id": "ALM-X.4", "kind": "star", "record": "R.2", "day_offset": 5,
                      "fork_options": [{"name": "positional", "primary": True, "operational": {"tolerance_deg": [0.25, 2.0]}},
                                       {"name": "none", "primary": False, "operational": None}]},
                     {"set": "ALM-Y", "clue_id": "ALM-Y.1", "kind": "planet", "record": "R.3", "day_offset": 0,
                      "statement": "Venus is a morning star past its greatest elongation.",
                      "fork_options": [{"name": "ge_before_within_j", "primary": True, "operational": {"j_days": [7, 15, 30]}},
                                       {"name": "ge_before_same_apparition", "primary": False,
                                        "operational": {"bound": "same_apparition"}},
                                       {"name": "visible_only", "primary": False,
                                        "operational": {"min_minutes_between_body_and_sun_horizon_crossings": [30, 60]}},
                                       {"name": "bm_venus_lead", "primary": False, "operational": {"lead_min": [60, 90, 120]}}]},
                     {"set": "ALM-Y", "clue_id": "ALM-Y.2", "kind": "season", "record": "R.3", "day_offset": 0,
                      "statement": "The spring equinox occurred on this day, about one hour after noon.",
                      "fork_options": [{"name": "equinox_tol", "primary": True,
                                        "operational": {"tolerance_days": [0.5, 1, 2]}}]},
                 ]}
    slack = [
        {"id": "R.1", "reading": "printed", "body": "mercury", "off_ge_true_d": -0.4, "rs_min": 70.0,
         "rs_kind": "rise lead", "side_ok": True, "az_max_off_d": 3.0,
         "moon": {"dlon_c": 1.0, "dlon_s": 1.25, "elong_signed": 30.0}},
        {"id": "R.2", "reading": "printed", "body": "mercury", "off_ge_true_d": 2.13, "rs_min": 80.0,
         "rs_kind": "set lag", "side_ok": True,
         "stars": [{"kind": "offset", "reading": "more than 1 deg south of the star", "dlon_c": 0.3, "dlon_s": 0.0,
                    "dlat_c": -1.6, "dlat_s": -1.0}]},
        {"id": "R.2", "reading": "emended: x", "body": "mercury", "off_ge_true_d": 9.0},
        {"id": "R.3", "reading": "printed", "body": "venus", "off_ge_true_d": 12.0, "rs_min": 200.0,
         "rs_kind": "rise lead", "side_ok": True, "equinox": {"off_d": 0.5},
         "stars": [{"kind": "offset", "reading": "2 deg east of the star", "dlon_c": 2.444, "dlon_s": 2.0,
                    "dlat_c": 0.0, "dlat_s": 0.0}]},
        {"id": "R.9", "reading": "printed", "body": "mercury", "off_ge_true_d": 5.476},
        {"id": "R.8", "reading": "printed", "body": "venus", "off_ge_true_d": 20.592},
        {"id": "R.7", "reading": "printed", "body": "mars", "off_opp_mean_d": 0.424},
        {"id": "R.6", "reading": "printed", "body": "saturn", "moon": {"dlon_c": 0.0, "dlon_s": 0.667}},
    ]
    summary = {"records": {"mercury": ["R.1", "R.2", "R.9"], "venus": ["R.3", "R.8"]}, "cruxes": {"R.2": "printed"}}
    return clues_doc, slack, summary


def selftest(verbose=True) -> bool:
    ok = True

    def chk(cond, msg):
        nonlocal ok
        if not cond:
            ok = False
            print("SELFTEST FAIL:", msg)

    chk(ceil_step(5.476, 0.1) == 5.5 and ceil_step(5.476, 0.5) == 5.5 and ceil_step(5.476, 1.0) == 6.0, "ceil 5.476")
    chk(ceil_step(4.174, 0.1) == 4.2 and ceil_step(4.174, 0.5) == 4.5 and ceil_step(4.174, 1.0) == 5.0, "ceil 4.174")
    chk(ceil_step(20.592, 0.1) == 20.6 and ceil_step(20.592, 0.5) == 21.0, "ceil 20.592")
    chk(ceil_step(0.699, 0.01) == 0.7 and ceil_step(0.667, 0.01) == 0.67 and ceil_step(0.667, 0.05) == 0.7, "ceil deg")
    chk(ceil_step(1.323, 0.05) == 1.35 and ceil_step(1.0, 1.0) == 1.0 and ceil_step(0.424, 0.1) == 0.5, "ceil edges")
    chk(middle([30, 60]) == 30 and middle([0.5, 1, 2]) == 1 and middle([1, 2, 3]) == 2 and middle([5]) == 5, "middle")
    chk(most_lenient("j_days", [7, 15, 30]) == 30 and most_lenient("min_altitude_deg", [5]) == 5
        and most_lenient("min_minutes_between_body_and_sun_horizon_crossings", [30, 60]) == 30
        and most_lenient("umbral_mag_range", [[0.7, 0.95], [0.6, 1.0]]) == [0.6, 1.0], "most lenient")
    chk(inequalities("more than 3 moons (>1.5 deg) south of the common star") == {"dlat": "beyond"}, "ineq beyond")
    chk(inequalities("east of the star by 1 1/2 deg or less; passing it 0.5 deg to the north")
        == {"dlon": "within"}, "ineq within")
    chk(_component(-1.6, -1.0, "beyond") == 0.0 and abs(_component(-0.6, -1.0, "beyond") - 0.4) < 1e-12, "beyond")
    chk(_component(0.8, 1.5, "within") == 0.0 and abs(_component(1.9, 1.5, "within") - 0.4) < 1e-12, "within")
    clues_doc, slack, summary = _synthetic()
    p = project(clues_doc["clues"])
    chk(p["ALM-X"]["projection"] == [("ALM-X.1", "ge_true_k"), ("ALM-X.2", "none"), ("ALM-X.3", "structural")],
        "synthetic projection X")
    chk(p["ALM-X"]["held_out"] == [("ALM-X.2", "positional"), ("ALM-X.4", "positional")], "synthetic held-out X")
    chk(p["ALM-Y"]["projection"] == [("ALM-Y.1", "ge_before_same_apparition"), ("ALM-Y.2", "equinox_tol")],
        "synthetic projection Y")
    doc, arith = build(clues_doc, slack, summary)
    x, y = doc["sets"]["ALM-X"], doc["sets"]["ALM-Y"]
    chk(x["tolerances"]["greatest_elongation_days"]["mercury"] == {"fine": 5.5, "mid": 5.5, "coarse": 6.0},
        "Mercury ceiling outside X (R.9 5.476)")
    chk(arith["sets"]["ALM-X"]["ge:mercury"]["record"] == "R.9", "arithmetic record")
    chk(x["regimes"]["SL"]["coarse"]["ALM-X.1"]["params"]["k_days"] == 6.0, "SL k coarse")
    chk(x["regimes"]["BM"]["ALM-X.1"] == {"option": "bm_mwra_k", "params": {"k_days": 1.5}}, "BM proxy mwra")
    chk(y["regimes"]["BM"]["ALM-Y.1"] == {"option": "bm_venus_lead", "params": {"lead_min": 90.0}}, "BM proxy lead")
    chk(y["regimes"]["SL"]["fine"]["ALM-Y.1"]["params"]["visible_min_minutes"] == 30.0, "same_apparition visibility")
    chk(y["regimes"]["SL"]["fine"]["ALM-Y.2"]["params"]["tolerance_days"] == 2
        and y["regimes"]["BM"]["ALM-Y.2"]["params"]["tolerance_days"] == 1, "lenient and middle lists")
    # planet-star outside X: R.3 (0.444); outside Y: R.2 (inequality holds -> 0.3 from dlon)
    chk(x["tolerances"]["held_out"]["planet-star"]["fine"] == 0.45, "planet-star ceiling X")
    chk(x["regimes"]["held_out"]["mid"]["ALM-X.4"]["params"]["tolerance_deg"] == 0.45, "held-out row tolerance")
    # planet-Moon outside X: R.6 (0.667) -> 0.67, 0.7, 0.7
    chk(x["tolerances"]["held_out"]["planet-Moon"] == {"fine": 0.67, "mid": 0.7, "coarse": 0.7,
                                                       "pooled_lunar_fallback": False}, "planet-Moon ceiling")
    # B&M's 1 d is reported beside 1.5 d for the greatest-elongation k (6.4's table); X.1 offers the MWRA
    # proxy, so regime BM runs it as bm_mwra_k and it has no 1 d run.  Without the proxy it has one.
    chk("bm_k_1d" not in x["sensitivities"], "no 1 d run for a row whose BM option is the MWRA proxy")
    cd2 = copy.deepcopy(clues_doc)
    cd2["clues"][0]["fork_options"] = [o for o in cd2["clues"][0]["fork_options"] if opt_name(o) != "bm_mwra_k"]
    doc2, _ = build(cd2, slack, summary)
    x2 = doc2["sets"]["ALM-X"]
    chk(x2["regimes"]["BM"]["ALM-X.1"] == {"option": "ge_true_k", "params": {"k_days": 1.5}}, "BM ge_true_k 1.5 d")
    chk(x2["sensitivities"].get("bm_k_1d", {}).get("rows") == {"ALM-X.1": {"option": "ge_true_k",
                                                                            "params": {"k_days": 1.0}}},
        "BM 1 d sensitivity")
    chk("bounded_primary" in y["sensitivities"]
        and y["sensitivities"]["bounded_primary"]["rows"]["ALM-Y.1"]["SL"]["fine"]["params"]["j_days"] == 30,
        "bounded primary sensitivity")
    chk(not check_named_options(doc, clues_doc), "named options")
    # row predicates: body, side and instant by the fixed rules
    rp = x["row_predicates"]
    chk(rp["ALM-X.1"]["body"] == "mercury" and rp["ALM-X.1"]["side"] == "morning"
        and rp["ALM-X.1"]["instant"] == {"kind": "sun_alt", "deg": -8.0, "part": "morning"}, "predicate X.1")
    chk(rp["ALM-X.2"]["instant"] == {"kind": "lat", "hours": 19.5}, "predicate X.2 (4 1/2 h before midnight)")
    chk(y["row_predicates"]["ALM-Y.2"] == {"body": "sun", "side": None, "instant": {"kind": "lat", "hours": 13.0},
                                           "words": ["one hour after noon"]}, "predicate Y.2 (one hour after noon)")
    probe = lambda s, k="planet": row_predicate({"clue_id": "P", "kind": k, "statement": s})
    chk(probe("Venus is seen as a morning star at the twelfth (last) hour of the night.")["instant"]
        == {"kind": "night_hour", "hour": 12, "point": "middle"}, "night hour")
    chk(probe("Venus is a morning star on this day (4.75 equinoctial hours after midnight).")["instant"]["hours"]
        == 4.75, "4.75 h after midnight")
    chk(probe("The apparent Moon is west of the Sun (5.25 equinoctial hours before noon (after sunrise)).",
              "moon-phase")["instant"]["hours"] == 6.75, "5.25 h before noon")
    chk(probe("Mercury is an evening star on this day (evening).")["instant"]["part"] == "evening", "evening")
    for bad in ("Mars was at opposition about three days before this day.", "The Moon stands close to Saturn."):
        try:
            probe(bad, "planet" if bad.startswith("Mars") else "moon-phase")
            chk(False, f"no error for {bad!r}")
        except ValueError:
            pass
    if verbose:
        print("build_regimes selftest:", "PASS" if ok else "FAIL")
    return ok


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Write data/prereg/almagest_regimes.json by rule (DESIGN 6.4).")
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--arith-out", default=str(ARITH), help="truth-side arithmetic (off the public whitelist)")
    ap.add_argument("--check", action="store_true", help="truth-side checks; prints counts and labels only")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    if a.selftest:
        return 0 if selftest() else 1
    clues_doc = json.loads(CLUES.read_text(encoding="utf-8"))
    slack = json.loads(SLACK.read_text(encoding="utf-8"))
    summary = parse_summary(SUMMARY.read_text(encoding="utf-8"))
    doc, arith = build(clues_doc, slack, summary)
    Path(a.out).write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    Path(a.arith_out).parent.mkdir(parents=True, exist_ok=True)
    arith["note"] = ("TRUTH-SIDE (AppT 2, 2b): measured at the true dates; never give this file to a public-tier "
                     "agent. Written by tools/build_regimes.py.")
    Path(a.arith_out).write_text(json.dumps(arith, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    out_p = Path(a.out).resolve()
    shown = out_p.relative_to(ROOT) if out_p.is_relative_to(ROOT) else out_p
    print(f"wrote {shown} ({len(doc['sets'])} sets) and the truth-side arithmetic")
    if a.check:
        fails = check(doc, arith, clues_doc, slack)
        cq = consequences(doc, clues_doc, slack)
        print(f"R10: counted truths retained in regime SL: " +
              ", ".join(f"{s} {cq['SL'][s]}" for s in STEP_ORDER) + "; R9: in regime BM at most "
              f"{cq['BM']}")
        print("check:", "PASS" if not fails else "FAIL: " + "; ".join(fails))
        return 1 if fails else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
