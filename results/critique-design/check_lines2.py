import sys, re
sys.path.insert(0, r"C:\Users\Jon\AppData\Local\Temp\claude\C--Projects\7f771488-41ba-4f32-8787-76be4fdb1f11\scratchpad")
T = "C:/Projects/odybench/data/text/"
def load(name):
    d = {}
    with open(T + name + ".tsv", encoding="utf-8") as f:
        for ln in f:
            ln = ln.rstrip("\n")
            if "\t" not in ln: continue
            k, v = ln.split("\t", 1)
            k = re.sub(r"^urn:cts:[^:]+:[^.]+\.[^.]+\.[^.]+\.", "", k)
            d[k] = v
    return d
def grepk(name, pat, maxn=12):
    d = load(name); n=0
    print("=====", name, pat)
    for k,v in d.items():
        if re.match(pat, k):
            print(k, "\t", v[:400]); n+=1
            if n>=maxn: break
grepk("virgil-aeneid-lat", r"^2\.(25[3-6]|80[01])$")
grepk("apollonius-argonautica-grc", r"^1\.(120[0-3]|127[2-4])$")
grepk("apollonius-argonautica-grc", r"^4\.(169[4-8])$")
grepk("hhymn04-hermes-grc", r"^(1[7-9]|9[7-9]|100|14[01])$")
grepk("hesiod-worksdays-grc", r"^(38[3-7]|56[4-7]|609|61[0-9]|62[01]|77[01]|79[78])$", 40)
