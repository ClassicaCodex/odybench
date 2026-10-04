"""Design revision 8 scratch: replace one region of DESIGN.md by a part file.

  py results/design-revision-v8/replace_region.py START END PART [--keep-end]

The region runs from the unique occurrence of START up to the first
occurrence of END after it. Without --keep-end the END text is replaced too;
with it, END is kept. START must occur exactly once, and END at least once
after it, or nothing is written. Each run appends a line to splice.log.
"""
import sys
from pathlib import Path

DESIGN = Path("C:/Projects/odybench/DESIGN.md")
LOG = Path("C:/Projects/odybench/results/design-revision-v8/splice.log")
PARTS = Path("C:/Projects/odybench/results/design-revision-v8/parts")


def replace_region(text, start, end, new, keep_end=False):
    """return text with [start .. end] (or [start .. end) with keep_end) replaced by new."""
    n = text.count(start)
    if n != 1:
        raise ValueError(f"start anchor occurs {n} times")
    a = text.index(start)
    b = text.find(end, a + len(start))
    if b < 0:
        raise ValueError("end anchor not found after the start anchor")
    if not keep_end:
        b += len(end)
    return text[:a] + new + text[b:]


def main():
    args = [x for x in sys.argv[1:] if x != "--keep-end"]
    keep = "--keep-end" in sys.argv
    start, end, part = args
    new = (PARTS / part).read_text(encoding="utf-8")
    text = DESIGN.read_text(encoding="utf-8")
    out = replace_region(text, start, end, new, keep)
    DESIGN.write_text(out, encoding="utf-8", newline="\n")
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"{part}: {len(text)} -> {len(out)} chars; start {start[:50]!r}; end {end[:40]!r}; "
                f"keep_end {keep}\n")
    print(f"ok: {part}, {len(text)} -> {len(out)} chars")


if __name__ == "__main__":
    main()
