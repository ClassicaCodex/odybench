import sys; import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")
from tx import *
for spec in sys.argv[1:]:
    b, r = spec.split(":"); a, _, e = r.partition("-"); a=int(a); e=int(e) if e else a
    print(f"===== SCHOLIA {b}.{a}-{e}")
    for l,k,t in sch(int(b), a, e): print(f"[{l}] {k}: {t}")
