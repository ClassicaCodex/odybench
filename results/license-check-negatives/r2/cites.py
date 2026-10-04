# Round-2 licence check: find every "[<file>.tsv key K]" / "[<file>.tsv K-L]" / "[<file>.tsv K]" citation
# inside negatives.json (justifications, notes) and print the cited rows so the claim can be read.
import json, os, re, sys
ROOT = r"C:\Projects\odybench"
sys.stdout.reconfigure(encoding="utf-8")
d = json.load(open(os.path.join(ROOT, "data", "prereg", "negatives.json"), encoding="utf-8"))

cache = {}
def load(tf):
    if tf not in cache:
        rows = []
        for line in open(os.path.join(ROOT, "data", "text", tf), encoding="utf-8"):
            k, _, t = line.rstrip("\n").partition("\t")
            rows.append((k, t))
        cache[tf] = rows
    return cache[tf]

def find(tf, key):
    rows = load(tf)
    out = []
    for i, (k, t) in enumerate(rows):
        if k == key or k.endswith("." + key) or k.endswith(":" + key):
            out.append((i, k, t))
    return out

texts = []
def walk(o, path):
    if isinstance(o, dict):
        for k, v in o.items():
            walk(v, path + [k])
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, path + [str(i)])
    elif isinstance(o, str):
        texts.append((path, o))
walk(d, [])

pat = re.compile(r"([a-z0-9\-]+\.tsv)\s+(?:keys?\s+)?([0-9][0-9A-Za-z\.\-, ]*)")
seen = set()
for path, s in texts:
    for m in pat.finditer(s):
        tf = m.group(1)
        spec = m.group(2).strip().rstrip(",;. ")
        if (tf, spec) in seen:
            continue
        seen.add((tf, spec))
        keys = [x.strip() for x in re.split(r",\s*", spec) if x.strip()]
        print("=" * 80)
        print("CITED", tf, spec, " at", "/".join(path[:3]))
        if not os.path.exists(os.path.join(ROOT, "data", "text", tf)):
            print("   FILE MISSING")
            continue
        for key in keys:
            rng = re.match(r"^(\d+(?:\.\d+)*)-(\d+(?:\.\d+)*)$", key)
            if rng and "." not in rng.group(1):
                a, b = int(rng.group(1)), int(rng.group(2))
                for n in range(a, b + 1):
                    hits = find(tf, str(n))
                    for i, k, t in hits[:1]:
                        print("   ", k, "::", t[:300])
                    if not hits:
                        print("   NOT FOUND", n)
            else:
                hits = find(tf, key)
                if not hits:
                    print("   NOT FOUND", key)
                for i, k, t in hits[:2]:
                    print("   ", k, "::", t[:700])
