# Round-2 licence check: dump every clue row of data/prereg/negatives.json beside
# the cited rows of data/text (with context), and verify each licence_words
# fragment against the cited rows.  Read-only on all project data.
import json, sys, os, unicodedata, re

ROOT = r"C:\Projects\odybench"
OUT = os.path.join(ROOT, "results", "license-check-negatives", "r2")
sys.stdout.reconfigure(encoding="utf-8")

d = json.load(open(os.path.join(ROOT, "data", "prereg", "negatives.json"), encoding="utf-8"))

_cache = {}
def load(tf):
    if tf not in _cache:
        rows = []
        with open(os.path.join(ROOT, "data", "text", tf), encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n").rstrip("\r")
                if "\t" not in line:
                    continue
                k, t = line.split("\t", 1)
                rows.append((k, t))
        idx = {}
        for i, (k, t) in enumerate(rows):
            idx.setdefault(k, i)
        _cache[tf] = (rows, idx)
    return _cache[tf]

def short(k):
    m = re.search(r"grc\d?\.(.*)$", k)
    return m.group(1) if m else k

def frag_check(lw, refs, tf):
    rows, idx = load(tf)
    missing_refs = [r for r in refs if r not in idx]
    joined = " ".join(rows[idx[r]][1] for r in refs if r in idx)
    res = []
    frags = [f.strip() for f in re.split(r"\s*…\s*", lw) if f.strip()]
    for f in frags:
        exact = f in joined
        nfc = unicodedata.normalize("NFC", f) in unicodedata.normalize("NFC", joined)
        where = [short(r) for r in refs if r in idx and f in rows[idx[r]][1]]
        if not where:
            # fragment may span two rows
            where = ["(spans rows)" if exact else "-"]
        res.append((f, exact, nfc, where))
    return missing_refs, res

def context(tf, refs, before=4, after=3, gapmax=8):
    rows, idx = load(tf)
    ii = sorted(idx[r] for r in refs if r in idx)
    if not ii:
        return []
    keep = set()
    for i in ii:
        for j in range(i - before, i + after + 1):
            if 0 <= j < len(rows):
                keep.add(j)
    for a, b in zip(ii, ii[1:]):
        if b - a <= gapmax:
            keep.update(range(a, b + 1))
    out = []
    prev = None
    cited = set(ii)
    for j in sorted(keep):
        if prev is not None and j != prev + 1:
            out.append("      ...")
        mark = ">>" if j in cited else "  "
        out.append(f"   {mark} {short(rows[j][0])}\t{rows[j][1]}")
        prev = j
    return out

sets = {s["set"]: s for s in d["sets"]}
by_set = {}
for c in d["clues"]:
    by_set.setdefault(c["set"], []).append(c)

summary = []
for sname, s in sets.items():
    lines = []
    lines.append("=" * 100)
    lines.append(f"SET {sname}")
    sc = {k: v for k, v in s.items()}
    lines.append(json.dumps(sc, ensure_ascii=False, indent=1))
    for op in s.get("observer_places", []):
        if op.get("ref") and op.get("words"):
            tf = op.get("text_file", s["text_file"])
            refs = op["ref"] if isinstance(op["ref"], list) else [op["ref"]]
            mr, res = frag_check(op["words"], refs, tf)
            lines.append(f" PLACE {op.get('place')}: missing refs {mr}")
            for f, ex, nfc, where in res:
                lines.append(f"   frag exact={ex} nfc={nfc} where={where}: {f}")
            lines.extend(context(tf, refs, 2, 2))
    for c in by_set.get(sname, []):
        lines.append("-" * 100)
        lines.append(f"CLUE {c['clue_id']}  kind={c['kind']}  level={c['narrative_level']}")
        lines.append(json.dumps(c, ensure_ascii=False, indent=1))
        refs = c["ref"] if isinstance(c["ref"], list) else [c["ref"]]
        mr, res = frag_check(c["licence_words"], refs, c["text_file"])
        lines.append(f" missing refs: {mr}")
        bad = False
        for f, ex, nfc, where in res:
            lines.append(f"   frag exact={ex} nfc={nfc} where={where}: {f}")
            if not ex:
                bad = True
        lines.append(" TEXT:")
        lines.extend(context(c["text_file"], refs))
        summary.append(f"{c['clue_id']}: refs_missing={mr} frags_ok={not bad} nfrags={len(res)}")
    with open(os.path.join(OUT, f"d2_{sname}.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

# excluded rows
lines = []
for e in d.get("excluded_rows", []):
    lines.append("-" * 100)
    lines.append(json.dumps(e, ensure_ascii=False))
    refs = e["ref"] if isinstance(e["ref"], list) else [e["ref"]]
    lines.extend(context(e["text_file"], refs, 2, 2))
with open(os.path.join(OUT, "d2_EXCLUDED.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

with open(os.path.join(OUT, "d2_summary.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(summary) + "\n")
print("\n".join(summary))
