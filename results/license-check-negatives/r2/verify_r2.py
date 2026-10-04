# Round-2 consistency checks on data/prereg/negatives.json after apply_edits_r2.py.
import json, os, re, sys, unicodedata
ROOT = r"C:\Projects\odybench"
sys.stdout.reconfigure(encoding="utf-8")
d = json.load(open(os.path.join(ROOT, "data", "prereg", "negatives.json"), encoding="utf-8"))
sets = {s["set"]: s for s in d["sets"]}
rows = {c["clue_id"]: c for c in d["clues"]}
problems = []

# 1. every row has a verdict; verdict format
for c in d["clues"]:
    v = c.get("license_check")
    if not (v == "ok" or (isinstance(v, str) and v.startswith("edited: "))):
        problems.append(f"{c['clue_id']}: bad license_check {v!r}")
    if "license_check_r1" not in c:
        problems.append(f"{c['clue_id']}: no license_check_r1")
for s in d["sets"]:
    if "license_check" not in s:
        problems.append(f"set {s['set']}: no license_check")

# 2. options: unique names, justification present, 'none' present where forks exist
no_none = []
for c in d["clues"]:
    opts = c["fork_options"]
    names = [o["option"] for o in opts]
    if len(set(names)) != len(names):
        problems.append(f"{c['clue_id']}: duplicate option names {names}")
    for o in opts:
        if not o.get("justification", "").strip() or not o.get("operational", "").strip():
            problems.append(f"{c['clue_id']}:{o['option']}: empty operational/justification")
    if opts and "none" not in names:
        no_none.append(c["clue_id"])
print("forked rows without 'none':", no_none)

# 3. references resolve
def resolve(pair, where):
    cid, _, on = pair.partition(":")
    if cid not in rows:
        problems.append(f"{where}: unknown row {cid}")
        return
    if on and on not in [o["option"] for o in rows[cid]["fork_options"]]:
        problems.append(f"{where}: unknown option {pair}")
for name, s in sets.items():
    for pin, m in s.get("pinned_readings", {}).items():
        for cid, on in m.items():
            resolve(f"{cid}:{on}", f"{name} pin {pin}")
            if not cid.startswith(name + "-"):
                problems.append(f"{name} pin {pin}: row of another set {cid}")
    for pair in s.get("eclipse_compatible_options", []):
        resolve(pair, f"{name} eclipse_compatible")
    for slot, v in s.get("odyssey_slots", {}).items():
        for cid in v.get("clue_ids", []):
            resolve(cid, f"{name} slot {slot}")
    # every row of the set belongs to the set
for c in d["clues"]:
    if c["set"] not in sets:
        problems.append(f"{c['clue_id']}: unknown set")

# 4. observer places: words present at refs
cache = {}
def load(tf):
    if tf not in cache:
        rr = {}
        for line in open(os.path.join(ROOT, "data", "text", tf), encoding="utf-8"):
            k, _, t = line.rstrip("\n").partition("\t")
            rr.setdefault(k, t)
        cache[tf] = rr
    return cache[tf]
for name, s in sets.items():
    for key in ("observer_places", "landmarks"):
        for p in s.get(key, []):
            tf = p.get("text_file", s["text_file"])
            rr = load(tf)
            joined = " ".join(rr.get(k, "") for k in p["ref"])
            for frag in [f.strip() for f in re.split(r"\s*…\s*", p["words"]) if f.strip()]:
                if frag not in joined:
                    problems.append(f"{name} {key} {p['place'][:30]}: words not at refs: {frag}")

# 5. quoted text in the round-2 justifications/statements occurs in the cited texts
checks = [
    ("AEN-TROY-02", "virgil-aeneid-lat.tsv", ["et iam", "per lunam", "tacitae per amica silentia lunae"]),
    ("AEN-TROY-03", "virgil-aeneid-lat.tsv", ["consumpta nocte"]),
    ("AEN-CARTHAGE-03", "virgil-aeneid-lat.tsv", ["hiberno"]),
    ("ARG-CIUS-05", "apollonius-argonautica-grc.tsv", ["αὐτονυχί", "ὑπὸ νυκτὶ"]),
    ("ARG-RETURN-04", "apollonius-argonautica-grc.tsv", ["Αὐτίκα δὲ Κρηταῖον", "νύκτʼ ὀλοὴν"]),
    ("ARG-RETURN-04", "iliad-grc.tsv", ["νύκτʼ ὀλοὴν"]),
]
for cid, tf, strs in checks:
    alltext = "\n".join(load(tf).values())
    for st in strs:
        ok = st in alltext
        print(f"  quote check {cid} in {tf}: {st!r} -> {ok}  codepoints={[hex(ord(ch)) for ch in st if ord(ch) > 0x2a0][:6]}")
        if not ok:
            problems.append(f"{cid}: quote not found {st}")

# 6. no truth leak: years / BC / Julian
s = json.dumps(d, ensure_ascii=False)
for pat in [r"\bB\.?C\.?E?\b", r"\bA\.?D\.?\b", r"Julian", r"\bJD\b", r"Gregorian"]:
    if re.search(pat, s):
        problems.append(f"leak pattern {pat}")

print("rows:", len(d["clues"]), "sets:", len(d["sets"]))
print("edited rows (round 2):", [c["clue_id"] for c in d["clues"] if c["license_check"] != "ok"])
print("edited sets (round 2):", [x["set"] for x in d["sets"] if x["license_check"] != "ok"])
print("PROBLEMS:" if problems else "no problems", *problems, sep="\n  ")
