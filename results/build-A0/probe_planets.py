"""Scratch (A0): list lines naming two or more planets, with codes and safe
words only (see probe_lines.py); never the line text or a value."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import disclosure_scan as D  # noqa: E402
from probe_lines import SAFE  # noqa: E402

for path in sys.argv[1:]:
    lines = Path(path).read_text(encoding="utf-8", errors="replace").splitlines()
    for i, ln in enumerate(lines, 1):
        c = set(D.codes_of(ln))
        if len(c & set(D.PLANETS)) >= 2:
            words = [w for w in SAFE if re.search(rf"\b{w}\b", ln.lower())]
            print(f"{path}:{i} nums={len(re.findall(r'[0-9]+', ln))} codes={','.join(sorted(c))} words={','.join(words)}")
