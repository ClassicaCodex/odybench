import re
T = "C:/Projects/odybench/data/text/"
d = {}
for ln in open(T + "ptolemy-syntaxis-grc.tsv", encoding="utf-8"):
    if "\t" in ln:
        k, v = ln.rstrip("\n").split("\t", 1)
        d[re.sub(r"^urn:cts:[^:]+:[^.]+\.[^.]+\.[^.]+\.", "", k)] = v
for k in ("4.6.3", "4.6.4", "4.6.5"):
    for kk, v in d.items():
        if kk == k or kk.startswith(k + "."):
            print(kk, v[:700]); break
