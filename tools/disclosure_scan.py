"""
tools/disclosure_scan.py -- the disclosure scan of DESIGN 7.1 (A0; 12.1 item 9).

Lists every file in docs/, results/ and data/ that holds a quantity of the
target's sky between Day -40 and Day +1, by FILE NAME, LINE NUMBER, DATE and
QUANTITY CODE.  It never prints, stores or returns a value: a date is printed
as its civil date only (no clock time, because a time can itself be a
quantity, such as the instant of an event), a Julian Date only as the civil
date it falls on, and a quantity only as a code word (the keyword families of
CODES below).

The target is 16 Apr -1177 (1178 BC), Day 0.  The scanned span is the civil
dates 7 Mar -1177 (Day -40) to 18 Apr -1177 (Dawn +2, the end of Night +1),
both inclusive.

What it matches (DESIGN 7.1: "the files' date strings and JD ranges, and for
Horizons files the QUANTITIES line of the request"):

  * strict dates, which carry the year with the day: -1177-04-16, -11770416
    (NASA's packed ids), m1177_04_10 (file-name style), -1177 Apr 16,
    16 Apr -1177, 16 Apr 1178 BC, April 16, 1178 BC, 1178 BC Apr 16,
    b1178-Apr-16 and B.C. 1178-Apr-16 (Horizons);
  * loose dates: a line with a year token of -1177 / 1178 BC and a named
    March or April day but no strict date (flagged "loose": the day may
    belong to another year named on the same line);
  * Julian Dates whose civil day lies in the span (UT; the span is widened
    by half a day on each side for zone offsets);
  * Horizons responses ($$SOE ... $$EOE): one hit per file, with the
    QUANTITIES of the request and the target body, if any data line falls
    in the span;
  * JSON documents (walked: strings, keys and JD-like numbers; the "line" is
    the key path, with digits in keys masked), NPZ archives (arrays holding a
    JD in the span, or a year axis holding -1177; the "line" is the array
    name), PDF text (the "line" is the page) and file names themselves.

Excluded by rule: the ephemeris kernels (*.bsp; raw ephemerides, not an
evaluated quantity), images (listed as unscanned), and the scan's own
outputs (the two prereg files drafted from it and results/build-A0/).

Usage (from C:\\Projects\\odybench):
    py tools/disclosure_scan.py                    # print the list
    py tools/disclosure_scan.py --json PATH        # also write it as JSON
    py tools/disclosure_scan.py --sealed-json PATH --facts data/prereg/heldout_disclosure.json
    py tools/disclosure_scan.py --selftest         # synthetic fixtures only

The classification of hits into the facts of the disclosure table
(`classify`) is a drafting aid for A0 and the second reader A9: it suggests a
fact id per hit from frozen rules, and `sealed_list` turns the table's
"constrains" facts into the sealed list of access.json (DESIGN 7.1, 10.1).
"""
from __future__ import annotations

import argparse
import fnmatch
import io
import json
import re
import sys
import tempfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from odybench import calendar as C  # noqa: E402

# ---------------------------------------------------------------- the span

TARGET_YEAR = -1177
TARGET = (TARGET_YEAR, 4, 16)                       # Day 0
TARGET_JDN = C.jdn_from_julian(*TARGET)
FIRST_JDN = TARGET_JDN - 40                         # Day -40 = 7 Mar -1177
LAST_JDN = TARGET_JDN + 2                           # 18 Apr -1177: Dawn +2 ends Night +1
JD_LO = FIRST_JDN - 1.0                             # half a day of zone slack each side
JD_HI = LAST_JDN + 1.0

SCAN_DIRS = ("docs", "results", "data")
SELF_EXCLUDED = ("data/prereg/heldout_disclosure.json", "data/prereg/access.json",
                 "results/build-A0/")
KERNEL_SUFFIXES = (".bsp",)
IMAGE_SUFFIXES = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tif", ".tiff")
TEXT_SUFFIXES = (".txt", ".md", ".py", ".tsv", ".csv", ".js", ".jsonl", ".html", ".htm", ".log",
                 ".out", ".err", ".diff", ".xml", ".cfg", ".ini", ".yaml", ".yml", ".tex", "")

MONTHS = {"jan": 1, "january": 1, "feb": 2, "february": 2, "mar": 3, "march": 3, "apr": 4,
          "april": 4, "may": 5, "jun": 6, "june": 6, "jul": 7, "july": 7, "aug": 8, "august": 8,
          "sep": 9, "sept": 9, "september": 9, "oct": 10, "october": 10, "nov": 11,
          "november": 11, "dec": 12, "december": 12}
MON = r"(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|Sept?(?:ember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
MINUS = "[-\u2212\u2013]"                           # hyphen-minus, minus sign, en dash
BC = r"B\.?\s?C\.?(?:E\.?)?"

# strict patterns: (regex, (index of year, month, day), year kind)
_STRICT = [
    (re.compile(rf"(?<![\w.]){MINUS}(0?1177)[-/_ ](\d{{1,2}})[-/_ ](\d{{1,2}})(?![\d.])"), (1, 2, 3), "astro"),
    (re.compile(rf"(?<![\w.]){MINUS}(1177)(\d\d)(\d\d)(?!\d)"), (1, 2, 3), "astro"),
    (re.compile(r"(?<![A-Za-z0-9])m(1177)[_-](\d\d)[_-](\d\d)(?!\d)"), (1, 2, 3), "astro"),
    (re.compile(rf"(?<![\w.]){MINUS}(1177)[-/ ,]+{MON}\.?[-/ ]*(\d{{1,2}})(?!\d)", re.I), (1, 2, 3), "astro"),
    (re.compile(rf"(?<!\d)(\d{{1,2}})\s*{MON}\.?,?\s+{MINUS}(1177)(?!\d)", re.I), (3, 2, 1), "astro"),
    (re.compile(rf"(?<!\d)(\d{{1,2}})\s+{MON}\.?,?\s+(1178)\s*{BC}", re.I), (3, 2, 1), "bc"),
    (re.compile(rf"{MON}\.?\s+(\d{{1,2}})(?:st|nd|rd|th)?,?\s+(1178)\s*{BC}", re.I), (3, 1, 2), "bc"),
    (re.compile(rf"(?<!\d)(1178)\s*{BC},?\s+{MON}\.?\s+(\d{{1,2}})(?!\d)", re.I), (1, 2, 3), "bc"),
    (re.compile(rf"(?<!\d)(1178)\s*{BC},?\s+(\d{{1,2}})\s+{MON}", re.I), (1, 3, 2), "bc"),
    (re.compile(rf"\bb(1178)-{MON}-(\d{{1,2}})", re.I), (1, 2, 3), "bc"),
    (re.compile(rf"B\.C\.\s*(1178)-{MON}-(\d{{1,2}})", re.I), (1, 2, 3), "bc"),
]
_YEAR_TOKEN = re.compile(rf"(?<![\w.]){MINUS}0?1177(?![\d])|(?<!\d)1178\s*{BC}|\bb1178\b|"
                         r"(?<![A-Za-z0-9])m1177(?!\d)|B\.C\.\s*1178", re.I)
_LOOSE_MD = [re.compile(r"(?<!\d)(\d{1,2})\s+(Mar(?:ch)?|Apr(?:il)?)\b", re.I),
             re.compile(r"\b(Mar(?:ch)?|Apr(?:il)?)\.?\s+(\d{1,2})(?![\d.])", re.I)]
_JD = re.compile(r"(?<![\d.])(12912[2-6]\d)(\.\d+)?(?![\d])")

# quantity codes: keyword families, matched on the lower-cased line; only the
# code word is ever reported
CODES = [
    ("sun", r"\bsun\b|\bsolar\b|\bsun's\b"),
    ("moon", r"\bmoon|\blunar\b|\bselene\b"),
    ("mercury", r"mercury|\bhermes\b"),
    ("venus", r"\bvenus\b|\baphrodite\b|morning star|evening star|herald"),
    ("mars", r"\bmars\b|\bares\b"),
    ("jupiter", r"jupiter"),
    ("saturn", r"saturn"),
    ("star", r"sirius|arcturus|pleiad|alcyone|aldebaran|hyad|orion|betelgeuse|rigel|dubhe|spica|regulus|\bstars?\b"),
    ("riseset", r"\brise|\brising|\bsets?\b|\bsetting|sunrise|sunset|moonrise|moonset"),
    ("lead", r"\blead|\bled\b|\blag\b|before the sun|after the sun"),
    ("az", r"azimuth|\baz\b|\bazi\b"),
    ("mwra", r"mwra|rise-azimuth|rising azimuth|rise azimuth"),
    ("alt", r"altitude|\balt\b|elevation|\belev\b|above the horizon|below the horizon"),
    ("elong", r"elong"),
    ("ge", r"greatest|\bgwe\b|\bgee\b|max(?:imum)?\.? elongation"),
    ("station", r"station"),
    ("conj", r"conjunction|\bconj\b|new moon|\bti\b"),
    ("mag", r"magnitude|\bmag\b|\bsmag\b|\bumag\b|\bpmag\b|brightness"),
    ("pos", r"longitude|latitude|\blon\b|\blat\b|r\.a\.|\bra\b|declination|\bdec\b|ecliptic"),
    ("phase", r"phase|illuminat|crescent|quarter|full moon"),
    ("ecl", r"eclipse|totality|\btotal\b|annular|obscur|umbra"),
    ("vis", r"visib|visible|invisible|arcus|heliacal|\bav\b"),
    ("twl", r"twilight|\bdawn\b|\bdusk\b|nautical"),
    ("dt", r"delta-?t\b|\u0394t|\bdt\b|tdb-ut"),
    ("equinox", r"equinox"),
    ("sep", r"separation|\bsep\b|distance"),
]
_CODES = [(name, re.compile(rx, re.I)) for name, rx in CODES]
PLANETS = ("mercury", "venus", "mars", "jupiter", "saturn")


def codes_of(text: str) -> list[str]:
    """The code words whose keyword families occur in text (sorted, unique)."""
    return sorted({name for name, rx in _CODES if rx.search(text)})


def in_span(jdn: int) -> bool:
    return FIRST_JDN <= jdn <= LAST_JDN


def iso(jdn: int) -> str:
    """Civil date of a JDN as -YYYY-MM-DD (astronomical year, proleptic Julian)."""
    y, m, d = C.julian_from_jdn(int(jdn))
    return f"{y:+05d}-{m:02d}-{d:02d}"


def _month(tok: str) -> int | None:
    return MONTHS.get(tok.lower().rstrip("."), None) if not tok.isdigit() else int(tok)


def _date_jdn(year_tok: str, month_tok: str, day_tok: str, kind: str) -> int | None:
    y = int(year_tok)
    y = TARGET_YEAR if kind == "bc" else -y
    if y != TARGET_YEAR:
        return None
    m = _month(month_tok)
    d = int(day_tok)
    if not m or not 1 <= m <= 12 or not 1 <= d <= C.days_in_month(y, m):
        return None
    return C.jdn_from_julian(y, m, d)


def dates_in_text(text: str) -> tuple[list[int], str]:
    """JDNs (in the span) of the dates in text, and their kind:
    'strict', 'loose', 'jd' or '' (none).  Strict dates suppress loose ones."""
    found, kinds = set(), set()
    strict_any = False
    for rx, (iy, im, idd), kind in _STRICT:
        for mt in rx.finditer(text):
            jdn = _date_jdn(mt.group(iy), mt.group(im), mt.group(idd), kind)
            if jdn is None:
                continue
            strict_any = True
            if in_span(jdn):
                found.add(jdn)
                kinds.add("strict")
    if not strict_any and _YEAR_TOKEN.search(text):
        for rx in _LOOSE_MD:
            for mt in rx.finditer(text):
                a, b = mt.group(1), mt.group(2)
                mon, day = (b, a) if a.isdigit() else (a, b)
                m = _month(mon)
                d = int(day)
                if m in (3, 4) and 1 <= d <= 31:
                    jdn = C.jdn_from_julian(TARGET_YEAR, m, min(d, C.days_in_month(TARGET_YEAR, m)))
                    if in_span(jdn):
                        found.add(jdn)
                        kinds.add("loose")
    for mt in _JD.finditer(text):
        jd = float(mt.group(1) + (mt.group(2) or ""))
        if JD_LO <= jd < JD_HI:
            jdn = C.jdn_of_instant(jd)
            found.add(int(min(max(jdn, FIRST_JDN), LAST_JDN)))
            kinds.add("jd")
    kind = "strict" if "strict" in kinds else ("jd" if "jd" in kinds else ("loose" if kinds else ""))
    return sorted(found), kind


# ------------------------------------------------------------------ hits

def _hit(line, jdns, kind, codes):
    return {"line": line, "dates": [iso(j) for j in jdns], "match": kind, "codes": codes}


def planet_list(text: str) -> bool:
    """A line naming three or more of the five planets with a magnitude,
    elongation or position code: the shape of a planet table of one instant,
    such as B&M's Fig. 1 (fact D3), which carries no date on its own line."""
    c = set(codes_of(text))
    return len(c & set(PLANETS)) >= 3 and bool(c & {"mag", "elong", "pos"})


def scan_text_lines(lines: list[str]) -> list[dict]:
    """Per-line hits; a date split over two lines is caught on the first.
    In a file that already has a dated hit, an undated planet-table line
    (planet_list) is listed too, with match "planet-list" and no date."""
    hits, undated = [], []
    for i, ln in enumerate(lines):
        jdns, kind = dates_in_text(ln)
        if not jdns and i + 1 < len(lines):
            pair = ln.rstrip("\n") + " " + lines[i + 1]
            pj, pk = dates_in_text(pair)
            nj, _ = dates_in_text(lines[i + 1])
            extra = sorted(set(pj) - set(nj))
            if extra and pk == "strict":
                jdns, kind = extra, "strict"
        if jdns:
            hits.append(_hit(i + 1, jdns, kind, codes_of(ln)))
        elif planet_list(ln):
            undated.append(_hit(i + 1, [], "planet-list", codes_of(ln)))
    if hits:
        hits = sorted(hits + undated, key=lambda h: h["line"])
    return hits


_HZ_BODY = re.compile(r"Target body name:\s*([A-Za-z]+)", re.I)
_HZ_Q = [re.compile(r"QUANTITIES\s*=\s*'?\"?([0-9][0-9,]*)", re.I),
         re.compile(r"QUANTITIES=(?:%27|'|%22)?([0-9](?:[0-9,]|%2C)*)", re.I)]


def scan_horizons(lines: list[str]) -> list[dict]:
    """One hit for a Horizons response whose data rows reach the span."""
    try:
        i0 = next(i for i, ln in enumerate(lines) if ln.startswith("$$SOE"))
        i1 = next(i for i, ln in enumerate(lines) if ln.startswith("$$EOE"))
    except StopIteration:
        return scan_text_lines(lines)
    rows, jdns = [], set()
    for i in range(i0 + 1, i1):
        j, _ = dates_in_text(lines[i])
        if j:
            rows.append(i + 1)
            jdns.update(j)
    head = "".join(lines[:i0])
    body = _HZ_BODY.search(head)
    q = None
    for rx in _HZ_Q:
        mt = rx.search(head)
        if mt:
            q = mt.group(1).replace("%2C", ",").replace("%2c", ",")
            break
    if not rows:
        return []
    codes = ["horizons"] + ([f"Q={q}"] if q else ["Q=?"]) + ([body.group(1).lower()] if body else [])
    return [{"line": f"{rows[0]}-{rows[-1]}", "dates": [iso(j) for j in sorted(jdns)],
             "match": "horizons", "codes": codes}]


def _mask_key(k: str) -> str:
    jdns, kind = dates_in_text(k)
    if jdns and kind == "strict":
        return iso(jdns[0])
    return re.sub(r"\d+", "#", k)


def scan_json_obj(obj) -> list[dict]:
    """Walk a JSON document: strings, keys and JD-like numbers."""
    hits = []

    def walk(o, path, sibling_keys):
        if isinstance(o, dict):
            keys = " ".join(str(k) for k in o.keys())
            for k, v in o.items():
                kj, kk = dates_in_text(str(k))
                p = f"{path}.{_mask_key(str(k))}"
                if kj:
                    hits.append(_hit(p, kj, kk, codes_of(keys + " " + str(k))))
                walk(v, p, keys)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, f"{path}[{i}]", sibling_keys)
        elif isinstance(o, str):
            j, k = dates_in_text(o)
            if j:
                hits.append(_hit(path, j, k, codes_of(sibling_keys + " " + path + " " + o)))
        elif isinstance(o, (int, float)) and not isinstance(o, bool):
            if JD_LO <= float(o) < JD_HI:
                jdn = int(min(max(C.jdn_of_instant(float(o)), FIRST_JDN), LAST_JDN))
                hits.append(_hit(path, [jdn], "jd", codes_of(sibling_keys + " " + path)))

    walk(obj, "$", "")
    return hits


def scan_npz(path: Path) -> list[dict]:
    """Arrays holding a JD in the span, or a year axis holding -1177."""
    hits = []
    with np.load(path, allow_pickle=False) as f:
        names = list(f.keys())
        allnames = " ".join(names)
        for name in names:
            a = f[name]
            if a.dtype.kind not in "fiu" or a.size == 0:
                continue
            v = a.astype(float, copy=False).ravel()
            inside = (v >= JD_LO) & (v < JD_HI)
            if inside.any():
                jd = v[inside]
                jdns = sorted({int(min(max(C.jdn_of_instant(float(x)), FIRST_JDN), LAST_JDN)) for x in jd[:: max(1, len(jd) // 200)]}
                              | {int(C.jdn_of_instant(float(jd.min()))), int(C.jdn_of_instant(float(jd.max())))})
                jdns = [x for x in jdns if in_span(x)]
                hits.append(_hit(f"npz:{name} shape={tuple(a.shape)}", jdns, "jd", codes_of(allnames)))
            elif re.search(r"year|yr", name, re.I) and np.any(v == TARGET_YEAR):
                hits.append(_hit(f"npz:{name} shape={tuple(a.shape)}", [FIRST_JDN, LAST_JDN], "year-axis",
                                 codes_of(allnames)))
    return hits


def scan_pdf(path: Path) -> list[dict]:
    """PDF text, page by page; a hit's "line" is p<page>:<line on the page>."""
    from pypdf import PdfReader                      # noqa: PLC0415
    lines, where = [], []
    reader = PdfReader(str(path))
    for p, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception:                            # noqa: BLE001
            continue
        for k, ln in enumerate(text.splitlines(), start=1):
            lines.append(ln)
            where.append(f"p{p}:{k}")
    hits = scan_text_lines(lines)
    for h in hits:
        h["line"] = where[h["line"] - 1]
    return hits


def scan_file(path: Path, rel: str) -> dict:
    """{path, kind, hits, note} for one file."""
    suf = path.suffix.lower()
    rep = {"path": rel, "kind": "text", "hits": [], "note": ""}
    name_j, name_k = dates_in_text(rel)
    if name_j:
        rep["hits"].append(_hit(0, name_j, name_k, codes_of(rel.replace("_", " "))))
    try:
        if suf in KERNEL_SUFFIXES:
            rep.update(kind="excluded", note="ephemeris kernel (raw ephemeris, not an evaluated quantity)")
        elif suf in IMAGE_SUFFIXES:
            rep.update(kind="unscanned", note="image")
        elif suf == ".npz":
            rep["kind"] = "npz"
            rep["hits"] += scan_npz(path)
        elif suf == ".pdf":
            rep["kind"] = "pdf"
            rep["hits"] += scan_pdf(path)
        elif suf == ".json":
            rep["kind"] = "json"
            try:
                obj = json.loads(path.read_text(encoding="utf-8", errors="replace"))
                rep["hits"] += scan_json_obj(obj)
            except json.JSONDecodeError:
                rep["kind"] = "text"
                rep["hits"] += scan_text_lines(path.read_text(encoding="utf-8", errors="replace").splitlines())
        else:
            raw = path.read_bytes()
            if b"\x00" in raw[:4096] and suf not in TEXT_SUFFIXES:
                rep.update(kind="unscanned", note="binary")
            else:
                lines = raw.decode("utf-8", errors="replace").splitlines()
                if any(ln.startswith("$$SOE") for ln in lines):
                    rep["kind"] = "horizons"
                    rep["hits"] += scan_horizons(lines)
                else:
                    rep["hits"] += scan_text_lines(lines)
    except Exception as exc:                         # noqa: BLE001
        rep.update(kind="error", note=f"{type(exc).__name__}")
    return rep


def iter_files(root: Path, dirs=SCAN_DIRS):
    for d in dirs:
        base = root / d
        if not base.exists():
            continue
        for p in sorted(base.rglob("*")):
            if p.is_file():
                rel = p.relative_to(root).as_posix()
                if any(rel == x or (x.endswith("/") and rel.startswith(x)) for x in SELF_EXCLUDED):
                    continue
                yield p, rel


def scan(root: Path = ROOT, dirs=SCAN_DIRS) -> dict:
    """The full scan: {span, files (with hits), unscanned, excluded, errors}."""
    files, unscanned, excluded, errors = [], [], [], []
    for p, rel in iter_files(root, dirs):
        rep = scan_file(p, rel)
        if rep["kind"] == "excluded":
            excluded.append({"path": rel, "note": rep["note"]})
        elif rep["kind"] == "unscanned":
            unscanned.append({"path": rel, "note": rep["note"], "name_dates": [h["dates"] for h in rep["hits"]]})
        elif rep["kind"] == "error":
            errors.append({"path": rel, "note": rep["note"]})
        if rep["hits"] and rep["kind"] not in ("excluded",):
            files.append(rep)
    return {"span": {"first": iso(FIRST_JDN), "last": iso(LAST_JDN), "target": iso(TARGET_JDN),
                     "days": "Day -40 .. Day +2 (Dawn +2 ends Night +1)", "jd_window": "civil day, UT, +/-0.5 d"},
            "scanned_dirs": list(dirs), "self_excluded": list(SELF_EXCLUDED),
            "files": files, "unscanned": unscanned, "excluded": excluded, "errors": errors}


# --------------------------------------------------------- classification

D5_FILES = re.compile(r"^data/ephem/horizons/venus_mercury_m1177_(03_14_dusk|04_10_dawn)_\d+\.txt$")
D6_FILES = re.compile(r"^data/ephem/horizons/sun_moon_m1177_04_16_eclipse_\d+\.txt$")
D5_OUTPUTS = re.compile(r"^results/validate_ephem\.txt$|^results/data-acquisition/validate_ephem\.[^/]*\.txt$|"
                        r"^results/instrument/i1/")


def _day(date: str) -> int:
    y, m, d = (int(x) for x in re.match(r"([+-]\d+)-(\d\d)-(\d\d)", date).groups())
    return C.jdn_from_julian(y, m, d) - TARGET_JDN


def classify(path: str, hit: dict) -> str:
    """A suggested fact id for one hit (drafting aid; DESIGN 7.1's table):
    D5 / D6 by file, D5-output, D3 (three or more planets with a magnitude or
    elongation code), D4 (Mercury's spring events, in March), D2 (Venus' lead
    or elongation, Days -15..-1), D1 (Mars' visibility), H3-other (Mercury,
    Days -6..+2), H4-other (Venus or Mars, Days -10..-4), ECL (the Day-0
    eclipse), H2 (the Moon, Nights -5/-4), else OTHER."""
    codes = set(hit["codes"])
    days = [_day(d) for d in hit["dates"]] if hit["dates"] else []
    planets = codes & set(PLANETS)
    if D5_FILES.match(path):
        return "D5"
    if D6_FILES.match(path):
        return "D6"
    if D5_OUTPUTS.match(path):
        return "D5-output"
    if len(planets) >= 3 and codes & {"mag", "elong", "pos"}:
        return "D3"
    if "mercury" in codes and codes & {"station", "ge", "mwra", "az"} and days and max(days) <= -26:
        return "D4"
    if "mercury" in codes and days and any(-6 <= d <= 2 for d in days):
        return "H3-other"
    if "venus" in codes and codes & {"lead", "elong", "ge", "riseset"} and days and any(-15 <= d <= -1 for d in days):
        return "D2"
    if "mars" in codes and "vis" in codes:
        return "D1"
    if codes & {"venus", "mars"} and days and any(-10 <= d <= -4 for d in days):
        return "H4-other"
    if "ecl" in codes and days and 0 in days:
        return "ECL"
    if "moon" in codes and days and any(d in (-5, -4) for d in days):
        return "H2"
    return "OTHER"


def classify_all(report: dict) -> dict:
    """{fact id: [(path, line), ...]} over every hit of a scan."""
    out: dict[str, list] = {}
    for f in report["files"]:
        for h in f["hits"]:
            out.setdefault(classify(f["path"], h), []).append((f["path"], h["line"]))
    return out


def _covered(path: str, line, files, lines, globs) -> bool:
    if path in files or any(fnmatch.fnmatchcase(path, g) for g in globs):
        return True
    return isinstance(line, int) and line in lines.get(path, ())


def sealed_list(report: dict, facts: list[dict], public_by_design=("D4",), reviewed=(),
                outputs=()) -> dict:
    """The sealed list of access.json (DESIGN 7.1): every line and file that
    the scan lists under a "constrains" fact, except a fact this design must
    itself print (public_by_design), plus every output that prints their
    values.

    facts: the disclosure table's rows.  A row is sealed when its "status" is
    "constrains" and its id is not public by design.  Its "locators" name what
    is sealed: {"path", "lines": [...]} for lines, {"path", "file": true} for a
    whole file, {"glob": ...} for outputs yet to be written.  Its
    "scan_classes" are the classify() ids whose hits it must cover.

    reviewed: hits of those classes that a reader checked and found to be no
    value of the target's sky (a description of a fact, a file name), as
    {"path", "lines": [...], "reason"}.  Every remaining hit of a sealed class
    that no locator covers is returned under "uncovered": the list is
    complete only when "uncovered" is empty."""
    sealed = [f for f in facts if f.get("status") == "constrains" and f["id"] not in public_by_design]
    files, lines, globs = set(outputs), {}, set()
    for f in sealed:
        for loc in f.get("locators", []):
            if loc.get("glob"):
                globs.add(loc["glob"])
            elif loc.get("file"):
                files.add(loc["path"])
            else:
                lines.setdefault(loc["path"], set()).update(int(x) for x in loc["lines"])
    for p in list(lines):
        if p in files:
            lines.pop(p)
    rv_files = {r["path"] for r in reviewed if r.get("file")}
    rv_lines: dict[str, set] = {}
    for r in reviewed:
        if not r.get("file"):
            rv_lines.setdefault(r["path"], set()).update(r["lines"])
    classes = sorted({c for f in sealed for c in f.get("scan_classes", [f["id"]])})
    uncovered = []
    for rep in report["files"]:
        for h in rep["hits"]:
            cls = classify(rep["path"], h)
            if cls not in classes:
                continue
            if _covered(rep["path"], h["line"], files, lines, globs):
                continue
            if rep["path"] in rv_files or h["line"] in rv_lines.get(rep["path"], ()):
                continue
            uncovered.append({"path": rep["path"], "line": h["line"], "class": cls})
    return {"files": sorted(files),
            "lines": [{"path": p, "lines": sorted(v)} for p, v in sorted(lines.items())],
            "globs": sorted(globs),
            "facts": [f["id"] for f in sealed],
            "classes": classes,
            "uncovered": uncovered}


# ------------------------------------------------------------------ output

def format_report(report: dict, classify_hits: bool = False) -> str:
    out = [f"disclosure scan: civil dates {report['span']['first']} .. {report['span']['last']} "
           f"(target {report['span']['target']}; {report['span']['days']})",
           f"scanned: {', '.join(report['scanned_dirs'])}; self-excluded: {', '.join(report['self_excluded'])}"]
    n_hits = 0
    for f in report["files"]:
        out.append(f"{f['path']}  [{f['kind']}]  {len(f['hits'])} hit(s)")
        for h in f["hits"]:
            n_hits += 1
            cls = f"  -> {classify(f['path'], h)}" if classify_hits else ""
            out.append(f"    {h['line']}: {','.join(h['dates'])}  {h['match']}  {' '.join(h['codes'])}{cls}")
    out.append(f"{len(report['files'])} files, {n_hits} hits")
    if report["unscanned"]:
        out.append("unscanned (listed, not read): " + ", ".join(u["path"] for u in report["unscanned"]))
    if report["errors"]:
        out.append("errors: " + ", ".join(f"{e['path']} ({e['note']})" for e in report["errors"]))
    out.append(f"excluded by rule: {len(report['excluded'])} ephemeris kernels")
    return "\n".join(out)


# ---------------------------------------------------------------- selftest

def _fixtures(base: Path) -> dict:
    """Synthetic files with planted values that must never reach the output.
    Every planted value is a string of the form 7.13579 or 1:42:56-like that
    no date or code can produce."""
    planted = ["7.13579", "1:42:51", "3.97531", "86.4213"]
    (base / "docs").mkdir(parents=True)
    (base / "results" / "x").mkdir(parents=True)
    (base / "data" / "ephem" / "horizons").mkdir(parents=True)
    (base / "docs" / "note.md").write_text(
        "intro line without a date\n"
        f"On 16 Apr 1178 BC Venus led the Sun by {planted[1]} at dawn.\n"
        f"-1177-04-14 Mercury elongation {planted[0]} deg\n"
        "The eclipse of 18 Mar 1189 BC is outside the year.\n"
        f"In -1177 the Moon on Apr 12 had altitude {planted[2]}\n"
        "a table: -1177-02-17 Arcturus first evening (outside the span)\n"
        f"JD 1291263.01734 conjunction; JD 1291300.5 is later; {planted[3]}\n"
        "a date split over lines: 16 April\n1178 BC is Day 0\n"
        f"Fig. 1: Mercury mag {planted[0]}, Venus mag {planted[2]}, Mars, Jupiter and Saturn\n",
        encoding="utf-8")
    (base / "docs" / "undated.md").write_text(
        "a planet table with no target date anywhere in the file:\n"
        "Mercury mag 1, Venus mag 2, Mars mag 3\n", encoding="utf-8")
    hz = ["API https://ssd.jpl.nasa.gov/api/horizons.api?format=text&QUANTITIES=%271%2C2%2C4%2C20%27\n",
          " Target body name: Mercury (199)\n", "$$SOE\n",
          f" b1178-Apr-10 04:30     {planted[0]} {planted[2]}\n", " b1178-Apr-11 04:30     1 2\n",
          "$$EOE\n"]
    (base / "data" / "ephem" / "horizons" / "venus_mercury_m1177_04_10_dawn_199.txt").write_text("".join(hz), encoding="utf-8")
    hz2 = ["$$SOE\n", " b1210-Jun-01 04:30  1 2\n", "$$EOE\n"]
    (base / "data" / "ephem" / "horizons" / "other_m1210.txt").write_text("".join(hz2), encoding="utf-8")
    (base / "results" / "x" / "vis.json").write_text(json.dumps(
        {"rows": [{"date": "-1177-04-17", "mercury_alt": float(planted[2])},
                  {"date": "-1177-06-01", "mercury_alt": 1.0}],
         "jd_event": 1291262.75, "-1177-03-20": {"venus": float(planted[3])}}), encoding="utf-8")
    jd = np.array([1291200.5, 1291240.5, 1291262.5, 1291300.5])
    np.savez(base / "results" / "x" / "mornings.npz", jd=jd, mercury_alt=np.array([1.0, 2.0, 3.0, 4.0]))
    np.savez(base / "results" / "x" / "years.npz", year=np.array([-1179, -1178, -1177]), venus=np.zeros(3))
    np.savez(base / "results" / "x" / "far.npz", jd=np.array([1500000.5]))
    (base / "data" / "kernel.bsp").write_bytes(b"\x00\x01binary")
    return {"planted": planted}


def selftest(verbose: bool = True) -> bool:
    ok = True

    def check(cond, msg):
        nonlocal ok
        if not cond:
            ok = False
            print("SELFTEST FAIL:", msg)

    with tempfile.TemporaryDirectory() as td:
        base = Path(td)
        fx = _fixtures(base)
        rep = scan(base)
        text = format_report(rep, classify_hits=True) + json.dumps(rep)
        for v in fx["planted"]:
            check(v not in text, f"planted value {v} reached the output")
        check(not re.search(r"\d\d:\d\d", text), "a clock time reached the output")
        byp = {f["path"]: f for f in rep["files"]}
        note = byp.get("docs/note.md")
        check(note is not None, "note.md not listed")
        if note:
            lines = {h["line"]: h for h in note["hits"]}
            check(2 in lines and lines[2]["dates"] == ["-1177-04-16"] and lines[2]["match"] == "strict", "BC date")
            check("venus" in lines[2]["codes"] and "lead" in lines[2]["codes"], "codes of line 2")
            check(3 in lines and lines[3]["dates"] == ["-1177-04-14"], "ISO date")
            check(4 not in lines, "another year's date must not hit")
            check(5 in lines and lines[5]["match"] == "loose" and lines[5]["dates"] == ["-1177-04-12"], "loose date")
            check(6 not in lines, "a strict date outside the span must not hit")
            check(7 in lines and lines[7]["dates"] == ["-1177-04-15"] and lines[7]["match"] == "jd", "JD in span")
            check(8 in lines and lines[8]["dates"] == ["-1177-04-16"], "date split over two lines")
            check(10 in lines and lines[10]["match"] == "planet-list" and lines[10]["dates"] == []
                  and classify("docs/note.md", lines[10]) == "D3", "undated planet table (D3 shape)")
        check("docs/undated.md" not in byp, "a planet table in a file with no target date is not listed")
        hz = byp.get("data/ephem/horizons/venus_mercury_m1177_04_10_dawn_199.txt")
        check(hz is not None and hz["kind"] == "horizons", "Horizons file")
        if hz:
            h = [x for x in hz["hits"] if x["match"] == "horizons"]
            check(len(h) == 1 and "Q=1,2,4,20" in h[0]["codes"] and "mercury" in h[0]["codes"]
                  and h[0]["dates"] == ["-1177-04-10", "-1177-04-11"], "Horizons hit")
            check(classify(hz["path"], h[0]) == "D5", "D5 classification")
        check("data/ephem/horizons/other_m1210.txt" not in byp, "Horizons file outside the span")
        js = byp.get("results/x/vis.json")
        check(js is not None and len(js["hits"]) == 3, "JSON hits (row date, JD number, date key)")
        if js:
            check(any("mercury" in h["codes"] for h in js["hits"]), "JSON sibling-key codes")
            check(all("#" in h["line"] or "$" in h["line"] for h in js["hits"]), "JSON key paths")
        npz = byp.get("results/x/mornings.npz")
        check(npz is not None and npz["hits"][0]["line"].startswith("npz:jd"), "NPZ JD axis")
        check("results/x/years.npz" in byp, "NPZ year axis")
        check("results/x/far.npz" not in byp, "NPZ outside the span")
        check(any(e["path"] == "data/kernel.bsp" for e in rep["excluded"]), "kernel excluded")
        d5 = "data/ephem/horizons/venus_mercury_m1177_04_10_dawn_199.txt"
        facts = [{"id": "D5", "status": "constrains", "scan_classes": ["D5", "H3-other"],
                  "locators": [{"path": d5, "file": True}, {"glob": "results/instrument/i1/*"}]},
                 {"id": "D3", "status": "constrains", "scan_classes": ["D3"],
                  "locators": [{"path": "docs/note.md", "lines": [10]}]},
                 {"id": "D4", "status": "constrains", "scan_classes": ["D4"]},
                 {"id": "D2", "status": "settles", "scan_classes": ["D2"]}]
        sl = sealed_list(rep, facts, outputs=("results/validate_ephem.txt",))
        check(d5 in sl["files"] and "results/validate_ephem.txt" in sl["files"], "sealed D5 file and output")
        check(sl["lines"] == [{"path": "docs/note.md", "lines": [10]}], "sealed D3 line")
        check(sl["globs"] == ["results/instrument/i1/*"], "sealed glob")
        check(sl["facts"] == ["D5", "D3"] and "D4" not in sl["classes"] and "D2" not in sl["classes"],
              "D4 public by design, D2 not sealed")
        unc = {(u["path"], u["line"]) for u in sl["uncovered"]}
        check(("docs/note.md", 3) in unc, "an H3-other hit no locator covers is reported uncovered")
        sl2 = sealed_list(rep, facts, reviewed=[{"path": "docs/note.md", "lines": [3], "reason": "test"}])
        check(("docs/note.md", 3) not in {(u["path"], u["line"]) for u in sl2["uncovered"]},
              "a reviewed hit is not reported uncovered")
    if verbose:
        print("disclosure_scan selftest:", "PASS" if ok else "FAIL")
    return ok


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[1])
    ap.add_argument("--json", help="write the scan as JSON")
    ap.add_argument("--classify", action="store_true", help="print a suggested fact id per hit")
    ap.add_argument("--facts", help="heldout_disclosure.json, for --sealed-json")
    ap.add_argument("--sealed-json", help="write the sealed list derived from --facts")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--quiet", action="store_true", help="print the summary line only")
    a = ap.parse_args(argv)
    if a.selftest:
        return 0 if selftest() else 1
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    rep = scan(ROOT)
    txt = format_report(rep, classify_hits=a.classify)
    print(txt.splitlines()[-3] if a.quiet else txt)
    if a.json:
        Path(a.json).parent.mkdir(parents=True, exist_ok=True)
        Path(a.json).write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    if a.sealed_json:
        table = json.loads(Path(a.facts).read_text(encoding="utf-8"))
        sl = sealed_list(rep, table["facts"], public_by_design=tuple(table.get("public_by_design", ["D4"])),
                         reviewed=table.get("reviewed_not_sealed", []),
                         outputs=tuple(table.get("sealed_outputs", [])))
        Path(a.sealed_json).write_text(json.dumps(sl, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"sealed: {len(sl['files'])} files, {sum(len(x['lines']) for x in sl['lines'])} lines in "
              f"{len(sl['lines'])} files, {len(sl['globs'])} globs; uncovered hits: {len(sl['uncovered'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
