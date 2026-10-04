"""Round-2 review: read-only scan of the two control clue files.
(1) every licence string occurs verbatim in its cited row of the local text;
(2) no operational/statement/notes/justification string carries a year-like
    number or a calendar month name that the cited words do not contain
    (a crude leak screen: hits are listed for reading by eye).
Run: py results/critique-design-r2/check_prereg_leaks.py
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(".")
_cache = {}


def text_rows(tf):
    tf = str(tf)
    if not tf.startswith("data/"):
        tf = "data/text/" + tf
    if tf not in _cache:
        d = {}
        for line in (ROOT / tf).read_text(encoding="utf-8").splitlines():
            if "\t" in line:
                k, v = line.split("\t", 1)
                d[k] = v
        _cache[tf] = d
    return _cache[tf]


def find_row(rows, ref):
    if ref in rows:
        return rows[ref]
    hits = [v for k, v in rows.items() if k.endswith("." + ref) or k.endswith(":" + ref) or k.split(".", 1)[-1] == ref]
    return " ".join(hits) if hits else None


YEARLIKE = re.compile(r"(?<![\d.])(?:[1-9]\d{2,3})\s*(?:BC|B\.C\.|AD|BCE)|(?<![\w.])-\d{3,4}(?![\d.])")
MONTHS = re.compile(r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\b")


def walk_strings(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk_strings(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk_strings(v, f"{path}[{i}]")
    elif isinstance(o, str):
        yield path, o


for fn in ("data/prereg/controls_real.json", "data/prereg/controls_almagest.json"):
    d = json.loads(Path(fn).read_text(encoding="utf-8"))
    n_ok = n_bad = 0
    bad = []
    items = []
    for s in d["sets"]:
        for clue in s.get("clues", []) + s.get("rows", []):
            items.append(clue)
    items += d.get("clues", [])
    for c in items:
        lw, refs, tfs = c.get("licence_words"), c.get("ref"), c.get("text_file")
        if lw is None or refs is None:
            continue
        if isinstance(lw, str):
            lw = [lw]
        if isinstance(refs, str):
            refs = [refs] * len(lw)
        if isinstance(tfs, str) or tfs is None:
            tfs = [tfs] * len(lw)
        for w, r, tf in zip(lw, refs, tfs):
            if w.startswith("[") or tf is None:
                continue
            row = find_row(text_rows(tf), r)
            parts = [p.strip() for p in re.split(r"…|\.\.\.", w) if p.strip()]
            ok = row is not None and all(p in row for p in parts)
            if ok:
                n_ok += 1
            else:
                n_bad += 1
                bad.append((c.get("clue_id"), r, w[:60]))
    print(f"{fn}: licence strings found verbatim {n_ok}, not found {n_bad}")
    for b in bad[:20]:
        print("   not found:", b)
    hits = []
    for p, sv in walk_strings(d):
        if any(x in p for x in ("licence_words", "license_check_record", "drafting_record", ".ref", "text_file")):
            continue
        for m in YEARLIKE.finditer(sv):
            hits.append((p, m.group(0), sv[max(0, m.start() - 60): m.end() + 40]))
        for m in MONTHS.finditer(sv):
            hits.append((p, m.group(0), sv[max(0, m.start() - 60): m.end() + 40]))
    print(f"  year-like or month-name strings outside licence words: {len(hits)}")
    for h in hits:
        print("   ", h[0][-60:], "|", h[1], "|", h[2].replace("\n", " "))
