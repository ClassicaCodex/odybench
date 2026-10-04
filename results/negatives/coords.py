import json, urllib.request, urllib.parse, sys
titles = ["Troy","Cius","Cyzicus","Poti","Anafi","Giresun Island","Karpathos","Lemnos","Strophades","Mount Ida (Turkey)","Ceraunian Mountains","Bozcaada","Mount Athos","Myrina, Lemnos","Cape Caphireus","Salmonion","Kapıdağ Peninsula","Gemlik","Mount Etna","Catania","Pagasae","Mount Dindymon (Cyzicus)","Pergamea","Kydonia","Leucas","Actium","Lake Tritonis","Euesperides","Cyrene","Phasis (town)"]
out = {}
for i in range(0, len(titles), 20):
    q = {"action":"query","prop":"coordinates","titles":"|".join(titles[i:i+20]),"format":"json","redirects":"1"}
    url = "https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode(q)
    req = urllib.request.Request(url, headers={"User-Agent":"odybench-negatives/0.1 (research script)"})
    d = json.load(urllib.request.urlopen(req, timeout=60))
    redir = {r["from"]: r["to"] for r in d["query"].get("redirects", [])}
    norm = {r["from"]: r["to"] for r in d["query"].get("normalized", [])}
    for p in d["query"]["pages"].values():
        c = p.get("coordinates")
        out[p["title"]] = (c[0]["lat"], c[0]["lon"]) if c else None
    out["_redirects_%d" % i] = redir
sys.stdout.reconfigure(encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=1))
