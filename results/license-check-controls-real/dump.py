"""Licence check helper: for every clue row and observer_place entry in
data/prereg/controls_real.json, test whether each licence_words string is a
substring of the cited row in the cited text file, and dump the clue plus the
full text of every cited row to a per-set file for reading.

Read-only on the project data; writes only under results/license-check-controls-real/.
Does NOT open controls_real_truth.json.
"""
import json, os, sys, unicodedata, re

ROOT = r"C:\Projects\odybench"
OUT = os.path.join(ROOT, "results", "license-check-controls-real")
_cache = {}


def load(tf):
    if tf not in _cache:
        rows = {}
        order = []
        with open(os.path.join(ROOT, tf), encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                if "\t" not in line:
                    continue
                k, v = line.split("\t", 1)
                rows[k] = v
                order.append(k)
        _cache[tf] = (rows, order)
    return _cache[tf]


def norm(s):
    s = unicodedata.normalize("NFC", s)
    s = s.replace("\u02bc", "'").replace("\u2019", "'").replace("\u1fbd", "'")
    s = s.replace("\u0374", "'").replace("\u2032", "'")
    s = re.sub(r"\s+", " ", s)
    return s


def check(words, refs, tfs):
    res = []
    for w, r, tf in zip(words, refs, tfs):
        rows, _ = load(tf)
        if r not in rows:
            res.append((w, r, tf, "REF-MISSING"))
            continue
        t = rows[r]
        if w in t:
            res.append((w, r, tf, "exact"))
        elif norm(w) in norm(t):
            res.append((w, r, tf, "normalised"))
        else:
            res.append((w, r, tf, "NOT-FOUND"))
    return res


def main():
    d = json.load(open(os.path.join(ROOT, "data", "prereg", "controls_real.json"), encoding="utf-8"))
    summary = []
    for s in d["sets"]:
        lines = []
        lines.append("#### SET " + s["set_id"])
        for op in s["observer_place"]:
            lines.append("-- observer_place " + json.dumps(op, ensure_ascii=False))
            for w, r, tf, st in check(op["licence_words"], op["ref"], op["text_file"]):
                summary.append((s["set_id"], "observer:" + op["place"], st, w, r))
                lines.append("   CHECK %s | %s | %s" % (st, w, r))
        for c in s["clues"]:
            lines.append("")
            lines.append("=" * 100)
            lines.append(json.dumps(c, ensure_ascii=False, indent=1))
            tfs = c["text_file"]
            refs = c["ref"]
            words = c["licence_words"]
            if isinstance(tfs, str):
                tfs = [tfs] * len(words)
            if isinstance(refs, str):
                refs = [refs] * len(words)
            if not (len(words) == len(refs) == len(tfs)):
                lines.append("   !! PARALLEL LIST LENGTH MISMATCH %d %d %d" % (len(words), len(refs), len(tfs)))
            for w, r, tf, st in check(words, refs, tfs):
                summary.append((s["set_id"], c["clue_id"], st, w, r))
                lines.append("   CHECK %s | %s | %s" % (st, w, r))
            # fork option licence words, if any
            for fo in c.get("fork_options", []) or []:
                if "licence_words" in fo:
                    lines.append("   fork licence words present: " + json.dumps(fo["licence_words"], ensure_ascii=False))
            seen = []
            for r, tf in zip(refs, tfs):
                if (r, tf) in seen:
                    continue
                seen.append((r, tf))
                rows, _ = load(tf)
                lines.append("   ROW [%s] %s :: %s" % (tf, r, rows.get(r, "<<MISSING>>")))
        with open(os.path.join(OUT, "dump_%s.txt" % s["set_id"]), "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
    with open(os.path.join(OUT, "check_summary.txt"), "w", encoding="utf-8") as f:
        for row in summary:
            f.write("\t".join(row) + "\n")
    bad = [r for r in summary if r[2] not in ("exact",)]
    print("checked", len(summary), "strings; non-exact:", len(bad))
    for r in bad:
        print("\t".join(r))


if __name__ == "__main__":
    main()
