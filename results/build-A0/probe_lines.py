"""Scratch (A0): structure probe for scan hits. Prints, for each requested
line, only: line number, the count of numeric tokens, the scanner's code
words, and the words of a fixed safe vocabulary present on the line (body
names and document-structure words; no visibility or direction words).
Never prints the line itself or any value."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
import disclosure_scan as D  # noqa: E402

SAFE = ["mercury", "venus", "mars", "jupiter", "saturn", "sun", "moon", "eclipse", "fig", "figure",
        "table", "abstract", "horizons", "magnitude", "mag", "elongation", "lead", "pleiades",
        "bootes", "conjunction", "station", "azimuth", "ti", "day", "night", "dawn", "dusk",
        "validate", "spot", "check", "sec", "summary", "plausibility", "historical", "intersecting"]


def probe(path, lo, hi):
    lines = Path(path).read_text(encoding="utf-8", errors="replace").splitlines()
    for i in range(lo, min(hi, len(lines)) + 1):
        ln = lines[i - 1]
        low = ln.lower()
        words = [w for w in SAFE if re.search(rf"\b{w}\b", low)]
        nnum = len(re.findall(r"\d+(?:\.\d+)?", ln))
        print(f"{path}:{i} len={len(ln)} nums={nnum} codes={','.join(D.codes_of(ln))} words={','.join(words)}")


if __name__ == "__main__":
    for spec in sys.argv[1:]:
        p, rng = spec.rsplit(":", 1)
        a, b = (int(x) for x in rng.split("-"))
        probe(p, a, b)
