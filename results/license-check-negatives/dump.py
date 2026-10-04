"""Licence check helper for data/prereg/negatives.json (independent check).

For every clue row, observer_places entry and excluded row, test whether each
' … '-separated licence_words fragment is a substring of the cited rows of
the cited text file, and dump the clue plus the cited rows WITH CONTEXT
(rows before/after, cited rows marked '>>') to a per-set file for reading.

Read-only on project data; writes only under results/license-check-negatives/.
Opens no truth file and not docs/research-controls.md.
"""
import json, os, re, sys, unicodedata

ROOT = r"C:\Projects\odybench"
OUT = os.path.join(ROOT, "results", "license-check-negatives")
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "data", "prereg", "negatives.json")
BEFORE, AFTER = 8, 5
_cache = {}


def load(tf):
    if tf not in _cache:
        rows, order = {}, []
        with open(os.path.join(ROOT, "data", "text", tf), encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                if "\t" not in line:
                    continue
                k, v = line.split("\t", 1)
                rows[k] = v
                order.append(k)
        _cache[tf] = (rows, order, {k: i for i, k in enumerate(order)})
    return _cache[tf]


def norm(s):
    s = unicodedata.normalize("NFC", s)
    for a in ("\u02bc", "\u2019", "\u1fbd", "\u0374", "\u2032", "\u1fbf"):
        s = s.replace(a, "'")
    s = re.sub(r"\s+", " ", s)
    return s.strip()


SEP = " \u2026 "


def check(words, refs, tf):
    """Each fragment must occur in the joined cited rows; also report order."""
    rows, order, idx = load(tf)
    missing = [r for r in refs if r not in rows]
    joined = " ".join(rows.get(r, "") for r in refs)
    out = []
    pos = 0
    for frag in words.split(SEP):
        frag = frag.strip()
        if not frag:
            continue
        if frag in joined:
            st = "exact"
            p = joined.find(frag, pos)
        elif norm(frag) in norm(joined):
            st = "normalised"
            p = norm(joined).find(norm(frag))
        else:
            st = "NOT-FOUND"
            p = -1
        # find which single row(s) hold it
        holders = [r for r in refs if norm(frag) in norm(rows.get(r, ""))]
        out.append((frag, st, holders))
    return missing, out


def context(refs, tf):
    rows, order, idx = load(tf)
    ii = sorted(idx[r] for r in refs if r in idx)
    if not ii:
        return ["   (no cited row found)"]
    keep = set()
    for i in ii:
        keep.update(range(max(0, i - BEFORE), min(len(order), i + AFTER + 1)))
    cited = set(refs)
    out, prev = [], None
    for i in sorted(keep):
        if prev is not None and i != prev + 1:
            out.append("   ...")
        k = order[i]
        out.append("%s %-10s %s" % (">>" if k in cited else "  ", k.split(".perseus-grc2.")[-1], rows[k]))
        prev = i
    return out


def main():
    d = json.load(open(SRC, encoding="utf-8"))
    summary = []
    clues_by_set = {}
    for c in d["clues"]:
        clues_by_set.setdefault(c["set"], []).append(c)
    for s in d["sets"]:
        L = ["#### SET " + s["set"]]
        L.append(json.dumps({k: v for k, v in s.items() if k != "observer_places"}, ensure_ascii=False, indent=1))
        for op in s.get("observer_places", []):
            L.append("-- observer_place " + json.dumps(op, ensure_ascii=False))
            miss, res = check(op["words"], op["ref"], op["text_file"])
            for frag, st, h in res:
                summary.append((s["set"], "observer:" + op["place"][:40], st, frag, ",".join(h), ",".join(miss)))
                L.append("   CHECK %s | %s | in %s" % (st, frag, h))
            L.extend(context(op["ref"], op["text_file"]))
        for c in clues_by_set.get(s["set"], []):
            L.append("")
            L.append("=" * 110)
            L.append(json.dumps(c, ensure_ascii=False, indent=1))
            miss, res = check(c["licence_words"], c["ref"], c["text_file"])
            if miss:
                L.append("   !! REF-MISSING " + ",".join(miss))
            for frag, st, h in res:
                summary.append((s["set"], c["clue_id"], st, frag, ",".join(h), ",".join(miss)))
                L.append("   CHECK %s | %s | in %s" % (st, frag, h))
            # fork option licence words, if any
            for fo in c.get("fork_options", []):
                for key in ("licence_words", "words"):
                    if isinstance(fo, dict) and fo.get(key):
                        fr = fo.get("ref", c["ref"])
                        ftf = fo.get("text_file", c["text_file"])
                        if isinstance(fr, str):
                            fr = [fr]
                        m2, r2 = check(fo[key], fr, ftf)
                        for frag, st, h in r2:
                            summary.append((s["set"], c["clue_id"] + ":" + str(fo.get("option", fo.get("id"))), st, frag, ",".join(h), ",".join(m2)))
                            L.append("   FORK-CHECK %s | %s | in %s %s" % (st, frag, h, m2))
            L.append("   --- context (%s) ---" % c["text_file"])
            L.extend(context(c["ref"], c["text_file"]))
        with open(os.path.join(OUT, "dump_%s.txt" % s["set"]), "w", encoding="utf-8") as f:
            f.write("\n".join(L) + "\n")
    L = ["#### EXCLUDED ROWS"]
    for e in d.get("excluded_rows", []):
        L.append("")
        L.append(json.dumps(e, ensure_ascii=False))
        L.extend(context(e["ref"], e["text_file"]))
    with open(os.path.join(OUT, "dump_EXCLUDED.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    with open(os.path.join(OUT, "check_summary.txt"), "w", encoding="utf-8") as f:
        for row in summary:
            f.write(" | ".join(row) + "\n")
    bad = [r for r in summary if r[2] != "exact" or r[5]]
    print("fragments:", len(summary), "non-exact or missing ref:", len(bad))
    for r in bad:
        print(r)


if __name__ == "__main__":
    main()
