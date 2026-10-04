"""Recheck of DESIGN revision 7 (round 3): an independent pass over the two
control clue files, without reading any truth file.

1. Every licence-word string is an exact substring of its cited row (raw
   characters, no Unicode normalisation), as I13(a) requires.
2. Every operational field is scanned for absolute-date-like content: four-
   digit or signed years, JD-like numbers, BC/AD/BCE/CE, Olympiads,
   Nabonassar, archon or consul names in operational (not licence) fields.
3. A per-row dump of statement, licence words and every option with its
   operational parameters, so that the primaries can be read against the
   words by hand (written to scan_clues.dump.txt).

Run: py -X utf8 results/critique-design-r3/scan_clues.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(r"C:\Projects\odybench")
TEXT = ROOT / "data" / "text"
OUT = Path(__file__).with_suffix(".dump.txt")

_cache = {}


def load_text(fn):
    if fn not in _cache:
        rows = {}
        for line in open(TEXT / Path(fn).name, encoding="utf-8"):
            ref, _, txt = line.rstrip("\n").partition("\t")
            rows[ref] = txt
        _cache[fn] = rows
    return _cache[fn]


DATE_PAT = re.compile(
    r"(?<![\d.])(?:[-\u2212]\s?\d{3,4}|\d{3,4}\s?(?:BC|BCE|AD|CE|B\.C\.|A\.D\.))(?![\d.])"
    r"|\b(?:BC|BCE|AD|CE)\b|Olymp|Nabonass|Ναβονασσ|\bJD\b|\b1[0-9]{6}(?:\.\d+)?\b|\b2[0-9]{6}(?:\.\d+)?\b",
    re.IGNORECASE)


def walk(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk(v, f"{path}[{i}]")
    else:
        yield path, obj


def check_real(out):
    d = json.load(open(ROOT / "data/prereg/controls_real.json", encoding="utf-8"))
    n_lic = n_ok = 0
    bad = []
    dates = []
    nrows = 0
    for s in d["sets"]:
        sid = s.get("set_id") or s.get("id")
        out.write(f"\n######## {sid}  {s.get('role','')}  window {s.get('window_years')}  anchor {s.get('anchor_event')}\n")
        for op_ in s.get("observer_place", []):
            out.write(f"  PLACE {json.dumps(op_, ensure_ascii=False)[:500]}\n")
        for ev in s.get("events", []):
            out.write(f"  EVENT {json.dumps(ev, ensure_ascii=False)[:300]}\n")
        for ev in [s]:
            for c in ev.get("clues", []):
                nrows += 1
                lic = c.get("licence_words") or []
                refs = c.get("ref") or []
                tfs = c.get("text_file") or []
                if isinstance(lic, str):
                    lic, refs, tfs = [lic], [refs], [tfs]
                for w, r, t in zip(lic, refs, tfs):
                    n_lic += 1
                    row = load_text(t).get(r)
                    if row is not None and w in row:
                        n_ok += 1
                    else:
                        bad.append((c.get("clue_id"), w[:60], r, row is None))
                out.write(f"   - {c.get('clue_id')} [{c.get('feature', c.get('kind',''))}] {str(c.get('statement',''))[:300]}\n")
                out.write(f"       licence: {' | '.join(lic)[:300]}\n")
                for o in c.get("fork_options", []):
                    op = o.get("operational")
                    out.write(f"       {'*' if o.get('primary') else ' '} {o.get('option')}: {json.dumps(op, ensure_ascii=False)[:300]}\n")
                    for p, v in walk(op, "op"):
                        if isinstance(v, (str, int, float)) and DATE_PAT.search(str(v)):
                            dates.append((c.get("clue_id"), o.get("option"), p, str(v)[:80]))
    return nrows, n_lic, n_ok, bad, dates


def check_alm(out):
    d = json.load(open(ROOT / "data/prereg/controls_almagest.json", encoding="utf-8"))
    n_lic = n_ok = 0
    bad = []
    dates = []
    for c in d["clues"]:
        lic = c.get("licence_words") or ""
        r = c.get("ref")
        t = c.get("text_file")
        row = load_text(t).get(r) if (r and t) else None
        # licence words may join fragments with an ellipsis
        frags = [f.strip() for f in lic.split("…") if f.strip()]
        for f in frags:
            n_lic += 1
            if row is not None and f in row:
                n_ok += 1
            else:
                bad.append((c["clue_id"], f[:60], r, row is None))
        out.write(f"\n   - {c['clue_id']} [{c['kind']}] off {c.get('day_offset')} rec {c.get('record')}: {c['statement'][:300]}\n")
        out.write(f"       licence: {lic[:300]}\n")
        for o in c.get("fork_options", []):
            op = o.get("operational")
            out.write(f"       {'*' if o.get('primary') else ' '} {o.get('option')}: {json.dumps(op, ensure_ascii=False)[:300]}\n")
            for p, v in walk(op, "op"):
                if isinstance(v, (str, int, float)) and DATE_PAT.search(str(v)):
                    dates.append((c["clue_id"], o.get("option"), p, str(v)[:80]))
        for k in ("statement", "notes"):
            v = c.get(k) or ""
            m = DATE_PAT.search(v)
            if m:
                dates.append((c["clue_id"], k, "-", v[max(0, m.start() - 30): m.end() + 30]))
    return len(d["clues"]), n_lic, n_ok, bad, dates


def main():
    with open(OUT, "w", encoding="utf-8") as out:
        out.write("controls_real.json\n")
        r = check_real(out)
        out.write("\n\ncontrols_almagest.json\n")
        a = check_alm(out)
    for name, (nrows, n_lic, n_ok, bad, dates) in (("controls_real", r), ("controls_almagest", a)):
        print(f"{name}: rows {nrows}; licence fragments {n_lic}, found verbatim {n_ok}")
        for b in bad:
            print("   NOT FOUND:", b)
        print(f"   date-like hits in operational fields (and ALM statement/notes): {len(dates)}")
        for x in dates:
            print("     ", x)


if __name__ == "__main__":
    main()
