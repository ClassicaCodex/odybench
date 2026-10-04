import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from formula import corp, norm
import re
sys.stdout.reconfigure(encoding="utf-8")
for stem in sys.argv[1:]:
    s = " ".join(norm(stem))
    hits = [(k,t) for k,t,w in corp if re.search(r"(^| )"+s, " ".join(w))]
    print(f"### {stem} -> {len(hits)}")
    for k,t in hits[:25]: print("   ", k, t)
