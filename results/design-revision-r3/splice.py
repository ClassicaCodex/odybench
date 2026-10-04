"""Design revision 4 scratch: splice the rewritten sections (parts/*.md) into
DESIGN.md (revision 3 text), replacing each span from a start line to the line
before an end line.  Each marker must occur exactly once.
Run: py results/design-revision-r3/splice.py
"""
from pathlib import Path

ROOT = Path("C:/Projects/odybench")
P = ROOT / "results/design-revision-r3/parts"
src = (ROOT / "DESIGN.md").read_text(encoding="utf-8")
lines = src.split("\n")


def find(text):
    idx = [i for i, l in enumerate(lines) if l == text]
    assert len(idx) == 1, (text, idx)
    return idx[0]


def part(*names):
    return "".join((P / n).read_text(encoding="utf-8") for n in names)


# (start marker or None for file start, end marker, replacement)
REPL = [
    (None, "## 0. Conventions and tags", part("00_header.md")),
    ("### 1.3 Outcomes", "## 2. What is already known, and so is not a prediction", part("13_outcomes.md")),
    ("### 2.7 Predictions of earlier revisions that are now settled",
     "### 2.8 Known from the recheck of revision 2, and from this revision", part("27_settled.md")),
    ("### 2.8 Known from the recheck of revision 2, and from this revision",
     "**The observation model's ceiling** [r1 N1; r1: check_lr_cap.py]:",
     "### 2.8 Known from the recheck of revision 2\n\n"),
    ("**What the known numbers already imply for the verdict.** Nothing in this", "## 3. T0: reproduction",
     part("29_known.md", "210_imply.md") + "---\n\n"),
    ("### 3.5 The T0 verdict", "## 4. Shared machinery", part("35_t0.md")),
    ("### 4.2 Candidate pools and target pools (Ithaki unless a rule names another site)",
     "### 4.3 Sky tables and events", part("42_pools.md")),
    ("### 5.4 N4: random epics, the main negative", "### 5.5 N5: window sensitivity", part("54_n4.md")),
    ("### 6.1 Instrument checks", "### 6.2 PC-S: synthetic Odyssey-shaped clue sets", part("61_instr.md")),
    ("## 7. Clues B&M did not use", "## 8. Pre-registered predictions", part("7_heldout.md")),
    ("## 8. Pre-registered predictions", "## 9. The decision rule", part("8_predictions.md")),
    ("## 9. The decision rule", "## 10. Software", part("9_rule.md")),
    ("### 11.2 Run order and expected times", "## 12. Freezing and amendments", part("112_run.md")),
    ("## 12. Freezing and amendments", "## 13. What the dossier could not settle, and how each is handled",
     part("12_freeze.md")),
    ("## 14. Resolution of the reviews", "## Sources", part("14_resolution.md")),
]
spans = []
for start, end, rep in REPL:
    a = 0 if start is None else find(start)
    b = find(end)
    assert a < b, (start, end)
    spans.append((a, b, rep))
spans.sort()
for (a1, b1, _), (a2, b2, _) in zip(spans, spans[1:]):
    assert b1 <= a2, "overlap"
out, cur = [], 0
for a, b, rep in spans:
    out.append("\n".join(lines[cur:a]) + ("\n" if a > cur else ""))
    out.append(rep)
    cur = b
out.append("\n".join(lines[cur:]))
new = "".join(out)
(ROOT / "DESIGN.md").write_text(new, encoding="utf-8")
print("lines:", len(lines), "->", new.count("\n") + 1)
