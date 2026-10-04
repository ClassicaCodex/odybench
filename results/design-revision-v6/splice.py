"""Design revision 6 scratch: assemble DESIGN.md (revision 6) from revision 5
(docs/DESIGN-v5.md, an unchanged byte copy) and the rewritten sections in
results/design-revision-v6/parts/.  Each part replaces the block from its start
line (inclusive) to its end line (exclusive); 14.5 is inserted before the
separator that precedes "## Sources".  Smaller edits are made afterwards with
the Edit tool, and recorded in the revision's own section 14.
Run: py results/design-revision-v6/splice.py
"""
import hashlib

SRC = "docs/DESIGN-v5.md"
OUT = "DESIGN.md"
P = "results/design-revision-v6/parts/"

REPLACE = [
    ("# odybench — design (revision 5)", "---", "00_header.md"),
    ("### 1.3 Outcomes", "---", "13_outcomes.md"),
    ("### 2.6 Controls: what is already known about them",
     "### 2.7 Predictions of earlier revisions that are now settled", "26_controls_known.md"),
    ("### 2.10 What the known numbers already imply for the verdict", "---", "210_implied.md"),
    ("### 6.1 Instrument checks", "### 6.2 PC-S: synthetic Odyssey-shaped clue sets", "61_instr.md"),
    ("### 6.3 PC-R: real eclipse records with independently known dates (gate 3a)",
     "#### 6.3.3 ΔT for the controls, and the controls that helped fit it", "63_pcr_head.md"),
    ("**The B&M-type projection.** The gate uses only rows of B&M's kinds, each",
     "### 6.5 Negative controls (outcome 4)", "64_alm_tail.md"),
    ("## 7. Clues B&M did not use", "---", "7_heldout.md"),
    ("## 8. Pre-registered predictions", "---", "8_predictions.md"),
    ("## 9. The decision rule", "---", "9_rule.md"),
    ("### 10.1 Build plan", "### 10.2 Module interfaces", "101_build.md"),
    ("### 10.4 Independent second implementations",
     "### 10.5 Scripts (top level, as in labench)", "104_second.md"),
    ("## 11. Data, run order and run times", "---", "11_data_run.md"),
    ("### 12.1 Before the first freeze (all must hold)", "### 12.2 The repository", "121_before.md"),
    ("## 14. Resolution of the reviews",
     "### 14.2 The recheck of revision 2 ([r1], issues 26–42)", "14_head.md"),
]


def read_part(name):
    text = open(P + name, encoding="utf-8").read()
    if not text.endswith("\n"):
        text += "\n"
    return text.splitlines(keepends=True)


def main():
    lines = open(SRC, encoding="utf-8").read().splitlines(keepends=True)
    for start, end, part in REPLACE:
        idx = [i for i, l in enumerate(lines) if l.rstrip("\n") == start]
        assert len(idx) == 1, (start, len(idx))
        i = idx[0]
        j = next(k for k in range(i + 1, len(lines)) if lines[k].rstrip("\n") == end)
        lines[i:j] = read_part(part)
    # insert 14.5 before the separator preceding "## Sources"
    s = [i for i, l in enumerate(lines) if l.rstrip("\n") == "## Sources"]
    assert len(s) == 1
    k = s[0]
    while lines[k - 1].strip() == "":
        k -= 1
    assert lines[k - 1].rstrip("\n") == "---", lines[k - 1]
    k -= 1                                   # index of the '---' line
    lines[k:k] = read_part("145_r1v5.md")
    out = "".join(lines)
    open(OUT, "w", encoding="utf-8", newline="\n").write(out)
    print("wrote", OUT, len(lines), "lines;", hashlib.sha256(out.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    main()
