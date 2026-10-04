"""Design revision 4 scratch: mechanical checks of DESIGN.md.

* every markdown table row has as many cells as its header;
* code fences are balanced;
* every section reference "(n.m)" or "section n" points at an existing heading;
* every prediction or expectation id cited outside section 8 exists in it;
* every [r2 R2-n] tag names an existing issue (1..12).
Run: py results/design-revision-r3/check_design.py
"""
import re
from pathlib import Path

s = Path("C:/Projects/odybench/DESIGN.md").read_text(encoding="utf-8")
lines = s.split("\n")
problems = []

# tables
hdr = None
in_code = False
for i, l in enumerate(lines, 1):
    if l.startswith("```"):
        in_code = not in_code
        continue
    if in_code:
        continue
    t = l.strip()
    if t.startswith("|") and t.endswith("|"):
        cells = len(re.findall(r"(?<!\\)\|", t)) - 1
        if hdr is None:
            hdr = cells
        elif re.fullmatch(r"\|[\s:|-]+\|", t):
            pass
        elif cells != hdr:
            problems.append(f"l. {i}: table row has {cells} cells, header {hdr}")
    else:
        hdr = None
if in_code:
    problems.append("unbalanced code fence")

# headings
heads = set()
for l in lines:
    m = re.match(r"^#{2,4} (\d+(?:\.\d+){0,2})[. ]", l)
    if m:
        heads.add(m.group(1).rstrip("."))
for i, l in enumerate(lines, 1):
    for m in re.finditer(r"\((\d{1,2}\.\d{1,2}(?:\.\d)?)(?:[,;)]| item| and)", l):
        ref = m.group(1)
        if ref not in heads and not re.search(r"\d\.\d+[°%]", m.group(0)):
            # numbers such as (5.1-9.0) are intervals, not sections
            if not re.search(r"\(\d\.\d+–", l[m.start():m.start() + 12]):
                problems.append(f"l. {i}: section ({ref}) not found")

# predictions
sec8 = s[s.index("## 8. Pre-registered predictions"):s.index("## 9. The decision rule")]
defined = set(re.findall(r"\*\*(P\d+)\.\*\*", sec8)) | set(re.findall(r"^\| (R\d+) \|", sec8, re.M))
outside = s.replace(sec8, "")
outside = outside[:outside.index("### 2.7")] + outside[outside.index("### 2.8"):outside.index("## 14.")]
for m in re.finditer(r"\b([PR]\d{1,2})\b", outside):
    tok = m.group(1)
    if tok not in defined and tok not in ("R2",):
        ctx = outside[max(0, m.start() - 30):m.end() + 10].replace("\n", " ")
        problems.append(f"undefined prediction/expectation {tok}: ...{ctx}...")

for m in re.finditer(r"R2-(\d+)", s):
    if not 1 <= int(m.group(1)) <= 12:
        problems.append(f"bad R2 issue {m.group(0)}")

print(f"{len(lines)} lines; {len(heads)} numbered headings")
print("\n".join(problems) if problems else "no problems found")
