"""show.py FILE REF[:N] ...   print rows (REF:N prints N rows from REF on)
   show.py FILE /substring    print every row containing substring (NFC, case-insensitive)
Read-only on data/text."""
import os, sys, unicodedata

ROOT = r"C:\Projects\odybench\data\text"
sys.stdout.reconfigure(encoding="utf-8")
tf = sys.argv[1]
rows, order = {}, []
with open(os.path.join(ROOT, tf), encoding="utf-8") as f:
    for line in f:
        line = line.rstrip("\n")
        if "\t" in line:
            k, v = line.split("\t", 1)
            rows[k] = v
            order.append(k)
idx = {k: i for i, k in enumerate(order)}
pref = ""
if order and "perseus-grc2." in order[0]:
    pref = order[0].split("perseus-grc2.")[0] + "perseus-grc2."
for a in sys.argv[2:]:
    if a.startswith("s="):
        q = unicodedata.normalize("NFC", a[2:]).lower()
        for k in order:
            if q in unicodedata.normalize("NFC", rows[k]).lower():
                print(k.replace(pref, ""), rows[k][:600])
        continue
    n = 1
    if ":" in a and not a.startswith("urn"):
        a, n = a.rsplit(":", 1)
        n = int(n)
    k = a if a in idx else pref + a
    if k not in idx:
        print("MISSING", a)
        continue
    i = idx[k]
    for j in range(i, min(len(order), i + n)):
        print(order[j].replace(pref, ""), rows[order[j]][:1500])
