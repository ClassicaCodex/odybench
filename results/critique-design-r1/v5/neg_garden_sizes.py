# Size of each negative's reading garden before F5 expansion: the product of its rows' option counts
# (negatives.json as licence-checked twice; no truth file exists for negatives).
import json, math, sys, io
from collections import defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
d = json.load(open('C:/Projects/odybench/data/prereg/negatives.json', encoding='utf-8'))
prod = defaultdict(lambda: 1); rows = defaultdict(int)
for c in d['clues']:
    s = c.get('set') or c.get('set_id')
    prod[s] *= len(c.get('fork_options', [])) or 1
    rows[s] += 1
for s in prod:
    print(f"{s:14s} rows {rows[s]:2d}  product of option counts {prod[s]:>8,d}  ({math.log2(prod[s]):.1f} bits)")
print("G_BM* for comparison: 36 readings (5.2 bits)")
