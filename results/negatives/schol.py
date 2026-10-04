import sys, re
sys.stdout.reconfigure(encoding="utf-8")
book = sys.argv[1]; lines = [int(x) for x in sys.argv[2].split(",")]
for raw in open("data/text/scholia-iliad-grc.tsv", encoding="utf-8"):
    ref, text = raw.rstrip("\n").split("\t", 1)
    k = ref.split("grc1.")[1]
    parts = k.split(".")
    if len(parts) < 2 or parts[1] != book: continue
    m = re.match(r"\s*(\d+)", text)
    if m and int(m.group(1)) in lines:
        print(k, "\t", text[:700]); print()
