import re, sys, unicodedata
B = r"C:\Projects\odybench\data\text"
def load(name):
    d = {}; order=[]
    for ln in open(B+"\\"+name, encoding="utf-8"):
        k, _, t = ln.rstrip("\n").partition("\t")
        d[k] = t; order.append(k)
    return d, order
OD, ODO = load("odyssey-grc.tsv")
IL, ILO = load("iliad-grc.tsv")
SC, SCO = load("scholia-odyssey-grc.tsv")
def strip(s):
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower().replace("ʼ","'").replace("’","'")
def od(book, a, b=None):
    b = b or a
    return [(f"{book}.{i}", OD.get(f"{book}.{i}")) for i in range(a, b+1)]
# scholia index: book -> list of (line, key, text)
SCI = {}
for k in SCO:
    p = k.split(".")
    if len(p) < 4 or not p[1].isdigit(): continue
    bk = int(p[1]); t = SC[k]
    m = re.match(r"\s*\(?(\d+)\)?\.", t)
    if m: cur = int(m.group(1)); SCI.setdefault(bk, []).append([cur, k, t]); SCI[bk][-1].append(True)
    else:
        prev = SCI.get(bk, [[0]])[-1][0] if SCI.get(bk) else 0
        SCI.setdefault(bk, []).append([prev, k, t, False])
def sch(book, a, b=None):
    b = b or a
    return [(l,k,t) for l,k,t,_ in SCI.get(book, []) if a <= l <= b]
def grep(d, order, pat):
    r = re.compile(pat)
    return [(k, d[k]) for k in order if r.search(strip(d[k]))]
