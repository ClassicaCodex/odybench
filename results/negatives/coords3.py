import json, urllib.request, urllib.parse, sys
titles = ["Carthage","Llogara Pass","Karaburun Peninsula","Kafireas","Cape Sidero","Sideros","Itanos","Benghazi","Lake Tritonis","Ida (Crete)","Akrokeraunia","Aci Trezza","Gargarus"]
q = {"action":"query","prop":"coordinates","coprimary":"all","titles":"|".join(titles),"format":"json","redirects":"1"}
url = "https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode(q)
req = urllib.request.Request(url, headers={"User-Agent":"odybench-negatives/0.1 (research script)"})
d = json.load(urllib.request.urlopen(req, timeout=60))
out = {}
for p in d["query"]["pages"].values():
    c = p.get("coordinates")
    out[p["title"]] = [(x["lat"], x["lon"]) for x in c] if c else ("missing" if "missing" in p else None)
out["_redirects"] = {r["from"]: r["to"] for r in d["query"].get("redirects", [])}
sys.stdout.reconfigure(encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=1))
