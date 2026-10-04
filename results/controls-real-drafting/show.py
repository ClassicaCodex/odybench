"""Print rows of a data/text tsv whose citation (the part after the last ':'
and the edition id, or the whole ref) matches a regex.

usage: py show.py <file-stem> <regex-on-citation> [maxchars]
"""
import re
import sys
from pathlib import Path

stem, pat = sys.argv[1], sys.argv[2]
maxc = int(sys.argv[3]) if len(sys.argv) > 3 else 100000
path = Path(__file__).resolve().parents[2] / "data" / "text" / (stem + ".tsv")
rx = re.compile(pat)
for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
    ref, _, text = line.partition("\t")
    cit = ref
    m = re.match(r"urn:cts:[^:]+:[^.]+\.[^.]+\.[^.]+\.(.*)$", ref)
    if m:
        cit = m.group(1)
    if rx.search(cit):
        sys.stdout.buffer.write(f"{i}\t{cit}\t{text[:maxc]}\n".encode("utf-8"))
