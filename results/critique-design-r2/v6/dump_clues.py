# Readable dumps of the two control clue files, for the licence and leak review of
# the recheck of DESIGN revision 6 (round 2). Reads only the clue files (never a truth file).
# Output: dump_real_v6.txt, dump_almagest_v6.txt (UTF-8).
import json, pathlib, sys
ROOT = pathlib.Path(r"C:\Projects\odybench")
OUT = pathlib.Path(__file__).parent

def opt_str(o):
    keys = [k for k in o.keys() if k not in ("name", "primary")]
    rest = {k: o[k] for k in keys}
    return f"    {'*' if o.get('primary') else ' '} {o.get('name')}: {json.dumps(rest, ensure_ascii=False)}"

def dump(fname, outname):
    d = json.load(open(ROOT / "data" / "prereg" / fname, encoding="utf-8"))
    lines = []
    for k, v in d.items():
        if k != "sets":
            lines.append(f"## {k}: {json.dumps(v, ensure_ascii=False)}")
    top_clues = d.get("clues") if isinstance(d.get("clues"), list) else None
    for s in d["sets"]:
        lines.append("")
        lines.append("=" * 100)
        hdr = {k: v for k, v in s.items() if k not in ("clues",)}
        sid = s.get("set_id") or s.get("set")
        lines.append(f"SET {sid}: {json.dumps(hdr, ensure_ascii=False)}")
        rows = s["clues"] if "clues" in s else [c for c in top_clues if c.get("set") == sid]
        for c in rows:
            lines.append("-" * 80)
            meta = {k: v for k, v in c.items() if k not in ("fork_options",)}
            lines.append(f"ROW {c.get('clue_id')}: {json.dumps(meta, ensure_ascii=False)}")
            for o in c.get("fork_options", []) or []:
                lines.append(opt_str(o))
    if top_clues is not None:
        for k in ("clues",):
            pass
    (OUT / outname).write_text("\n".join(lines), encoding="utf-8")
    n_rows = len(top_clues) if top_clues is not None else sum(len(s["clues"]) for s in d["sets"])
    print(fname, "sets", len(d["sets"]), "rows", n_rows)

dump("controls_real.json", "dump_real_v6.txt")
dump("controls_almagest.json", "dump_almagest_v6.txt")
