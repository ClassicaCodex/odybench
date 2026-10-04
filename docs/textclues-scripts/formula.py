import sys, re, unicodedata, collections
sys.stdout.reconfigure(encoding="utf-8")
B = r"C:\Projects\odybench\data\text\\"
def norm(s):
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    s = s.replace("ς","σ")
    s = re.sub(r"[ʼ'’`᾽]", " ", s)
    s = re.sub(r"[^\w\s]", " ", s)
    s = re.sub(r"\d+", " ", s)
    return s.split()
def load(fn, tag, keyfix=lambda k:k):
    out=[]
    for ln in open(B+fn, encoding="utf-8"):
        k,_,t = ln.rstrip("\n").partition("\t")
        if not t: continue
        out.append((tag+" "+keyfix(k), t, norm(t)))
    return out
lastref = lambda k: k.split("grc2.")[-1] if "grc2." in k else k
corp = []
OD = load("odyssey-grc.tsv","Od"); IL = load("iliad-grc.tsv","Il")
corp += OD + IL
corp += load("hesiod-worksdays-grc.tsv","Hes.WD",lastref)
corp += load("hesiod-theogony-grc.tsv","Hes.Th",lastref)
corp += load("hesiod-shield-grc.tsv","[Hes.]Sc",lastref)
for fn,tag in [("hhymn02-demeter-grc.tsv","h.Dem"),("hhymn03-apollo-grc.tsv","h.Ap"),("hhymn04-hermes-grc.tsv","h.Herm"),("hhymn31-helios-grc.tsv","h.31"),("hhymn32-selene-grc.tsv","h.32")]:
    corp += load(fn,tag,lastref)
LATE = load("aratus-phaenomena-grc.tsv","Arat",lastref)
idx = {c[0]:i for i,c in enumerate(corp)}
# n-gram index
N=3
gram = collections.defaultdict(set)
for i,(k,t,w) in enumerate(corp):
    for j in range(len(w)-N+1):
        gram[tuple(w[j:j+N])].add(i)
def parallels(key, minn=3, show=12, skipnear=3):
    i = idx[key]; k,t,w = corp[i]
    res = collections.defaultdict(int)
    for j in range(len(w)-N+1):
        for o in gram[tuple(w[j:j+N])]:
            if o==i: continue
            ok,ot,ow = corp[o]
            # skip neighbours in same passage
            if ok.split()[0]==k.split()[0]:
                try:
                    if ok.split(".")[0]==k.split(".")[0] and abs(int(ok.split(".")[-1])-int(k.split(".")[-1]))<=skipnear: continue
                except: pass
            res[o]+=1
    out=[]
    for o,c in sorted(res.items(), key=lambda x:-x[1]):
        ok,ot,ow = corp[o]
        # longest common contiguous run
        best=0
        for a in range(len(w)):
            for b in range(len(ow)):
                L=0
                while a+L<len(w) and b+L<len(ow) and w[a+L]==ow[b+L]: L+=1
                best=max(best,L)
        if best>=minn: out.append((best,ok,ot))
    out.sort(key=lambda x:-x[0])
    return k,t,out[:show], len(out)
def late(key, minn=3):
    i = idx[key]; w = corp[i][2]; out=[]
    for ok,ot,ow in LATE:
        best=0
        for a in range(len(w)):
            for b in range(len(ow)):
                L=0
                while a+L<len(w) and b+L<len(ow) and w[a+L]==ow[b+L]: L+=1
                best=max(best,L)
        if best>=minn: out.append((best,ok,ot))
    return sorted(out,key=lambda x:-x[0])[:5]
if __name__=="__main__":
    for spec in sys.argv[1:]:
        b, r = spec.split(":"); a,_,e = r.partition("-"); a=int(a); e=int(e) if e else a
        for l in range(a,e+1):
            key=f"Od {b}.{l}"
            if key not in idx: continue
            k,t,out,n = parallels(key)
            print(f"## {k}: {t}   [{n} parallels with >=3-word run]")
            for L,ok,ot in out: print(f"    {L}w  {ok}: {ot}")
            for L,ok,ot in late(key,4): print(f"    LATE {L}w {ok}: {ot}")
