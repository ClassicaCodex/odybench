import sys; import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")
from tx import *
for spec in sys.argv[1:]:
    b, r = spec.split(":"); a, _, e = r.partition("-"); a=int(a); e=int(e) if e else a
    print(f"--- {b}.{a}-{e}")
    for k,t in od(int(b),a,e): print(k, t)
