# Round-2 licence check (independent): dump every cited row of ptolemy-syntaxis-grc.tsv
# next to the clue rows that cite it, and test every licence fragment as an exact substring.
# Reads: data/prereg/controls_almagest.json, data/text/ptolemy-syntaxis-grc.tsv. Writes: stdout only.
import json, sys, unicodedata, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = r"C:\Projects\odybench"
d = json.load(open(ROOT + r"\data\prereg\controls_almagest.json", encoding="utf-8"))
rows = {}
order = []
with open(ROOT + r"\data\text\ptolemy-syntaxis-grc.tsv", encoding="utf-8") as f:
    for line in f:
        line = line.rstrip("\n")
        if not line:
            continue
        k, _, v = line.partition("\t")
        rows[k] = v
        order.append(k)

PFX = "urn:cts:greekLit:tlg0363.tlg001.1st1K-grc1."
ELL = "\u2026"


def norm(s):
    # only for a diagnostic: map oxia (U+1F7x) to tonos forms via NFC/NFD and casefold
    return unicodedata.normalize("NFC", unicodedata.normalize("NFD", s))


def check(clue):
    ref = clue["ref"]
    out = []
    if ref not in rows:
        out.append("REF MISSING")
        return out
    t = rows[ref]
    lw = clue["licence_words"]
    if lw.startswith("["):
        out.append("licence is a bracketed placeholder (withheld dates)")
        return out
    frags = [x.strip() for x in lw.split(ELL)]
    pos = -1
    for fr in frags:
        if not fr:
            out.append("EMPTY FRAGMENT")
            continue
        i = t.find(fr)
        if i < 0:
            j = norm(t).find(norm(fr))
            out.append(("NOT EXACT; NFC-normalised match at %d" % j) if j >= 0 else "NOT FOUND: " + fr)
        else:
            if i < pos:
                out.append("OUT OF TEXT ORDER: " + fr[:30])
            pos = i
            if t.count(fr) > 1:
                out.append("fragment occurs %d times: %s" % (t.count(fr), fr[:30]))
    if not out:
        out.append("all %d fragments exact, in order" % len(frags))
    return out


mode = sys.argv[1] if len(sys.argv) > 1 else "check"
if mode == "check":
    for c in d["clues"]:
        print(c["clue_id"], c["ref"].replace(PFX, ""), "|", "; ".join(check(c)))
elif mode == "rows":
    seen = []
    for c in d["clues"]:
        if c["ref"] not in seen:
            seen.append(c["ref"])
    for r in seen:
        ids = [c["clue_id"] for c in d["clues"] if c["ref"] == r]
        print("=" * 100)
        print(r.replace(PFX, ""), "cited by", ", ".join(ids))
        print(rows.get(r, "<<MISSING>>"))
elif mode == "ref":
    for r in sys.argv[2:]:
        k = PFX + r
        print("=" * 100)
        print(r)
        print(rows.get(k, "<<MISSING>>"))
elif mode == "grep":
    pat = sys.argv[2]
    for k in order:
        if pat in rows[k]:
            print(k.replace(PFX, ""), "|", rows[k][:300])
