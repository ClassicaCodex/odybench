"""Design revision 7: assemble DESIGN.md from the frozen revision-6 copy
(docs/DESIGN-v6.md) by the operations in splice_ops_a.py and splice_ops_b.py.

  ("region", start, end, part, sep): replace from the unique `start` up to the
      first `end` after it by the part file (trailing newlines stripped) + sep;
  ("sub", old, new): replace the unique `old` by `new`; "@@PART:name@@" inside
      `new` expands to the part file's text.
Every anchor and every `old` must occur exactly once in the text at the moment
its operation runs, or the script stops without writing anything.
Run: cd C:/Projects/odybench && py results/design-revision-v7/splice.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, "results/design-revision-v7")
from splice_ops_a import OPS_A  # noqa: E402
from splice_ops_b import OPS_B, OPS_C  # noqa: E402

SRC = Path("docs/DESIGN-v6.md")
DST = Path("DESIGN.md")
PARTS = Path("results/design-revision-v7/parts")


def part(name):
    return (PARTS / Path(name).name).read_text(encoding="utf-8")


def expand(s):
    return re.sub(r"@@PART:([^@]+)@@", lambda m: part(m.group(1)), s)


def main():
    text = SRC.read_text(encoding="utf-8")
    n0 = len(text)
    log = []
    for i, op in enumerate(OPS_A + OPS_B + OPS_C):
        kind = op[0]
        if kind == "sub":
            _, old, new = op
            c = text.count(old)
            if c != 1:
                sys.exit(f"op {i} (sub): old text occurs {c} times: {old[:90]!r}")
            text = text.replace(old, expand(new))
            log.append(f"{i:3d} sub     {old[:70]!r}")
        elif kind == "region":
            _, start, end, pname, sep = op
            c = text.count(start)
            if c != 1:
                sys.exit(f"op {i} (region): start occurs {c} times: {start[:90]!r}")
            s = text.index(start)
            e = text.find(end, s + len(start))
            if e < 0:
                sys.exit(f"op {i} (region): end not found after start: {end[:90]!r}")
            body = part(pname).rstrip("\n") + sep
            log.append(f"{i:3d} region  {start[:50]!r} .. {end[:30]!r}: {e - s} -> {len(body)} chars")
            text = text[:s] + body + text[e:]
        else:
            sys.exit(f"op {i}: unknown kind {kind}")
    if "@@PART:" in text:
        sys.exit("an unexpanded part placeholder survives")
    DST.write_text(text, encoding="utf-8", newline="\n")
    print("\n".join(log))
    print(f"{len(OPS_A) + len(OPS_B) + len(OPS_C)} operations; {n0} -> {len(text)} characters; "
          f"{text.count(chr(10))} lines written to {DST}")


if __name__ == "__main__":
    main()
