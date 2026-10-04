# DO NOT RE-RUN: DESIGN.md received further edits after this splice (2026-10-04); re-running would undo them.
"""Assemble DESIGN.md revision 3 from revision 2 (docs/DESIGN-v2.md) and the
new section texts in results/design-revision-r2/parts/.  Sections kept from
revision 2 are copied verbatim (small edits follow with the Edit tool).
Run: cd C:/Projects/odybench && py results/design-revision-r2/splice.py
"""
from pathlib import Path

ROOT = Path(".")
v2 = (ROOT / "docs" / "DESIGN-v2.md").read_text(encoding="utf-8").split("\n")
P = ROOT / "results" / "design-revision-r2" / "parts"


def idx(heading):
    hits = [i for i, l in enumerate(v2) if l.strip() == heading]
    assert len(hits) == 1, (heading, hits)
    return hits[0]


def keep(a, b):
    return "\n".join(v2[idx(a):idx(b)]).rstrip("\n") + "\n\n"


def part(name):
    return (P / name).read_text(encoding="utf-8").rstrip("\n") + "\n\n"


out = []
out.append(part("p00_head.md"))
out.append(keep("## 0. Conventions and tags", "### 1.3 Outcomes"))
out.append(part("p13_outcomes.md"))
out.append(keep("## 2. What is already known, and so is not a prediction", "### 2.6 Controls: what is already known about them"))
out.append(part("p26_known_controls.md"))
out.append(keep("## 3. T0: reproduction", "### 4.1 Spans and coverage"))
out.append(part("p41_spans_pools.md"))
out.append(keep("### 4.3 Sky tables and events", "### 5.3 N3: forking paths"))
out.append(part("p53_garden.md"))
out.append(keep("### 5.5 N5: window sensitivity", "### 5.7 The bottom line: a likelihood ratio on one event"))
for name in ("p57_evidence.md", "p6_controls.md", "p7_heldout.md", "p8_predictions.md",
             "p9_rule.md", "p10_software.md", "p11_data.md", "p12_freeze.md",
             "p13_open.md", "p14_resolution.md"):
    out.append(part(name))
text = "".join(out).rstrip("\n") + "\n"
(ROOT / "DESIGN.md").write_text(text, encoding="utf-8")
print("lines", text.count("\n"), "bytes", len(text.encode("utf-8")))
