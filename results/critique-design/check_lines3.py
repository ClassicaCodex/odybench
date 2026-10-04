import sys, re
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
def grepk(name, pat, maxn=12, width=900):
    d = load(name); n=0
    print("=====", name, pat)
    for k,v in d.items():
        if re.match(pat, k):
            print(k, "\t", v[:width]); n+=1
            if n>=maxn: break
grepk("thucydides-grc", r"^2\.28\.")
grepk("thucydides-grc", r"^4\.52\.1")
grepk("thucydides-grc", r"^7\.50\.4")
grepk("xenophon-hellenica-grc", r"^1\.6\.1\.")
grepk("xenophon-hellenica-grc", r"^2\.3\.4\.")
grepk("xenophon-hellenica-grc", r"^4\.3\.10\.")
grepk("diodorus-bk18-20-grc", r"^20\.5\.[56]\.")
grepk("livy-lat", r"^4\.44\.37\.[5-9]\.")
grepk("livy-lat", r"^2\.22\.1\.(8|9|10)\.")
grepk("livy-lat", r"^2\.30\.38\.8\.")
grepk("livy-lat", r"^3\.37\.4\.4\.")
grepk("livy-lat", r"^3\.38\.36\.4\.")
grepk("plutarch-alexander-grc", r"^31\.4\.")
grepk("arrian-anabasis-grc", r"^3\.7\.6\.")
grepk("arrian-anabasis-grc", r"^3\.15\.7\.")
grepk("curtius-lat", r"^4\.10\.[1-2]\.")
grepk("pliny-nh-lat", r"^2\.70\.3")
