"""Identify the site coordinates behind results/window/jsex/<site>.jsonl by
reproducing them with tools/jsex_sites.js on the same element files (scratch)."""
import json, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
W = ROOT / "results" / "window" / "jsex"
cands = {"ithaca": [(38.37, 20.72)], "kefalonia": [(38.18, 20.49), (38.2, 20.44), (38.177, 20.489)],
         "lefkada": [(38.83, 20.71), (38.707, 20.712), (38.83, 20.70)],
         "corfu": [(39.62, 19.92), (39.6, 19.9)], "zakynthos": [(37.78, 20.90), (37.79, 20.9)]}
files = [f"SEm{y:04d}.js" for y in range(1499, 600, -100)]
KEYS = ["file", "idx", "jdTD", "dT", "sigmaDT", "date", "type", "mag", "alt", "vis", "utH", "last",
        "maxMag1s", "anyTotal1s", "maxMag2s", "anyTotal2s", "anyCentral2s"]
for site, cs in cands.items():
    ref = [json.loads(l) for l in open(W / f"{site}.jsonl", encoding="utf-8")]
    for lat, lon in cs:
        r = subprocess.run(["node", str(ROOT / "tools" / "jsex_sites.js"), str(W), str(lat), str(lon)] + files,
                           capture_output=True, text=True, check=True)
        new = [json.loads(l) for l in r.stdout.splitlines()]
        same = len(new) == len(ref) and all(all(a[k] == b[k] for k in KEYS) for a, b in zip(new, ref))
        nd = sum(1 for a, b in zip(new, ref) if any(a[k] != b[k] for k in KEYS))
        print(f"{site:10s} {lat:7.3f} {lon:7.3f}: rows {len(new)} vs {len(ref)}; rows differing {nd}; identical={same}")
        if same:
            break
