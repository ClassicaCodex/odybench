"""Check that every markdown table row in DESIGN.md has the same number of
cells as its header (unescaped pipes inside cells would break a table).
Scratch script for the design revision task."""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
lines = open("DESIGN.md", encoding="utf-8").read().split("\n")


def cells(line):
    s = line.strip()
    s = re.sub(r"\\\|", "", s)          # escaped pipes are content
    s = re.sub(r"`[^`]*`", "", s)        # code spans may contain pipes
    return s.count("|") - 1


in_code = False
header = None
bad = 0
for i, line in enumerate(lines, 1):
    if line.strip().startswith("```"):
        in_code = not in_code
        continue
    if in_code:
        continue
    if line.strip().startswith("|"):
        n = cells(line)
        if header is None:
            header = n
        elif n != header:
            bad += 1
            print(f"line {i}: {n} cells, header {header}: {line[:90]}")
    else:
        header = None
print("rows with a cell-count mismatch:", bad)
