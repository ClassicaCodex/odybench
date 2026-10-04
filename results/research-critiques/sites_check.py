"""Nominal (canon Delta T) magnitude at five Ionian-island sites for every eclipse
of -1299..-1049 that exceeds 0.8 at any of them. Dates: canon (TT) date."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eclipse_local as E
S = {"Corfu": (39.62, 19.92), "Nidri(Lefkada)": (38.707, 20.712), "Vathy(Ithaki)": (38.367, 20.717),
     "Lixouri(Paliki)": (38.200, 20.437), "Zakynthos": (37.78, 20.90)}
print("| canon date | BC | " + " | ".join(S) + " |")
print("|---|---|" + "---|" * len(S))
for lab, el in E.load((-1299, -1049)):
    m = {k: E.local(el, la, lo, step_h=1 / 360) for k, (la, lo) in S.items()}
    if max(v["mag"] for v in m.values()) > 0.8:
        print(f"| {lab[0]} {lab[1]:02d} {lab[2]:02d} | {1-lab[0]} | " +
              " | ".join(f"{v['mag']:.3f}{v['type'] if v['type'] in 'AT' else ''}" for v in m.values()) + " |")
