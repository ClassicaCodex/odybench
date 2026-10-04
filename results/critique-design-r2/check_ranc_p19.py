"""Round-2 review: is DESIGN rev 3's prediction P19 (R_anc with the eclipse
clue has >= 2 survivors in the reproduction window) already settled by the
NASA site catalogue on disk?
R_anc with the eclipse clue (DESIGN 5.3): Day 0 a conjunction (LMT), Day 0
from Arcturus' heliacal rising (AV 10; 12 Sep at -1177 and -1130 per
results/design-revision-r2/ranc_season.out.txt) to the spring equinox (about
1 Apr at -1177 [bm 9]), and h_06(u, ithaki) >= 0.5, i.e. mixture
P(smag >= 0.6 with the Sun >= 10 deg at maximum) >= 0.5.
Proxy used here: NASA's JavaScript local circumstances at canon Delta-T
(data/jsex/sites/ithaca.jsonl): 'mag' >= 0.6 and Sun altitude 'alt' >= 10,
dated 12 Sep .. 31 Mar (Julian). The season ends drift < 1 day over the
136-year window. The mixture's centre lies within about 50 s of canon
[DESIGN 2.3], so only rows near the thresholds could change.
Run: py results/critique-design-r2/check_ranc_p19.py
"""
import json

MON = {m: i + 1 for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split())}
n = 0
for line in open("data/jsex/sites/ithaca.jsonl", encoding="utf-8"):
    r = json.loads(line)
    s = r["date"]
    neg = s.startswith("-")
    y, mo, d = s.lstrip("-").split("-")
    y = -int(y) if neg else int(y)
    mo, d = MON[mo], int(d)
    if not (-1249 <= y <= -1114):
        continue
    season = (mo == 9 and d >= 12) or mo in (10, 11, 12, 1, 2, 3)
    if season and r["mag"] >= 0.6 and r["alt"] >= 10.0:
        n += 1
        print(f"{s:14s} mag {r['mag']:.4f}  Sun alt {r['alt']:6.2f}  type {r['type']}  (1 partial, 3 total)")
print(f"R_anc-with-eclipse survivors in -1249..-1114 at canon Delta-T: {n}")
