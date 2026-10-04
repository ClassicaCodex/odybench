"""Scratch (A0): list lines that name a planet together with a relative-day
marker of the target (Day n, Ti, Night n, Dawn n, the eclipse), with codes
and safe words only; never the line text or a value."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
import disclosure_scan as D  # noqa: E402

REL = re.compile(r"\b(day|night|dawn)\s*[-−+]?\s*\d|\bti\s*[-−]\s*\d|\bti\b|eclipse|1178|−1177|-1177", re.I)
bodies = set(sys.argv[1].split(","))
for path in sys.argv[2:]:
    lines = Path(path).read_text(encoding="utf-8", errors="replace").splitlines()
    for i, ln in enumerate(lines, 1):
        c = set(D.codes_of(ln))
        if c & bodies and REL.search(ln):
            marks = sorted({m.group(0).lower().replace("−", "-") for m in REL.finditer(ln)})
            marks = [re.sub(r"\d+", "n", m) if not m.startswith(("day", "night", "dawn", "ti")) else m for m in marks]
            print(f"{path}:{i} nums={len(re.findall(r'[0-9]+', ln))} codes={','.join(sorted(c))} marks={'|'.join(marks)}")
