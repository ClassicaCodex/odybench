"""Scratch (A0): for given lines, report the SHAPES of the numbers on the line
(verse reference, degrees, clock time, minutes, percent, year, plain) and
context flags, never the numbers or the text."""
import re
import sys
from pathlib import Path

SHAPES = [("verse", r"\b\d{1,2}\.\d{1,3}(?:[-–]\d{1,3})?\b(?!\s*(?:°|deg|min|h\b|d\b|%))"),
          ("deg", r"\d+(?:\.\d+)?\s*(?:°|deg)"),
          ("clock", r"\b\d{1,2}:\d\d"),
          ("minutes", r"\d+(?:\.\d+)?\s*min"),
          ("hours", r"\d+(?:\.\d+)?\s*h\b"),
          ("days", r"\d+(?:\.\d+)?\s*(?:d\b|days?)"),
          ("percent", r"\d+(?:\.\d+)?\s*%"),
          ("mag", r"[-−]\d+\.\d+\b|\bmag\w*\s*[-−]?\d"),
          ("year", r"\b1[0-3]\d\d\s*BC|[-−]1[0-3]\d\d\b")]
CTX = [("1178/-1177", r"1178|[-−]1177"), ("target", r"target|b&m's date|16 apr"),
       ("computed", r"comput|de44|de43|horizons|skyfield|ephem"), ("threshold", r"threshold|≥|≤|>=|<=|at least|below")]
for spec in sys.argv[1:]:
    p, n = spec.rsplit(":", 1)
    ln = Path(p).read_text(encoding="utf-8", errors="replace").splitlines()[int(n) - 1]
    sh = {k: len(re.findall(rx, ln, re.I)) for k, rx in SHAPES}
    cx = [k for k, rx in CTX if re.search(rx, ln, re.I)]
    print(f"{spec}: " + " ".join(f"{k}={v}" for k, v in sh.items() if v) + f" | ctx={','.join(cx)}")
