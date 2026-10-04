"""
Fetch NASA's Five Millennium Canon Besselian elements (JavaScript Solar
Eclipse Explorer century files) for -1999..+300 and NASA's program.js, and
build the per-site eclipse catalogue with tools/jsex_sites.js.

    cd C:\\Projects\\odybench && py tools/fetch_jsex.py            # fetch missing files, build catalogue
    py tools/fetch_jsex.py --no-fetch                              # only rebuild the catalogue

Source: F. Espenak & J. Meeus, Five Millennium Canon of Solar Eclipses:
-1999 to +3000, NASA/TP-2006-214141 (2006); element files and program.js
(C. O'Byrne & F. Espenak) from https://eclipse.gsfc.nasa.gov/JSEX/ .
"Eclipse Predictions by Fred Espenak, NASA's GSFC".

Writes
  data/jsex/<century>.js, data/jsex/program.js     (verbatim downloads)
  data/jsex/sites/<site>.jsonl                      (one row per eclipse, see jsex_sites.js)
Century files are named by their first year: SEm1999 = -1999..-1900,
SEm0099 = -99..0, SE0001 = 1..100, SE0201 = 201..300.

Sites (lat N, lon E; modern reference points): ithaca = Vathy 38.37 20.72
(as in research-window and research-ephemeris); kefalonia 38.18 20.49,
lefkada 38.83 20.70, corfu 39.62 19.92, zakynthos 37.78 20.90 -- the
coordinates that reproduce results/window/jsex/<site>.jsonl row for row
(results/data-acquisition/jsex_sites_check.txt).
"""
import argparse
import hashlib
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "jsex"
BASE = "https://eclipse.gsfc.nasa.gov/JSEX/"
CENTURIES = [f"SEm{y:04d}" for y in range(1999, 0, -100)] + ["SE0001", "SE0101", "SE0201"]
SITES = {
    "ithaca": (38.37, 20.72),
    "kefalonia": (38.18, 20.49),
    "lefkada": (38.83, 20.70),     # NB: research-ephemeris uses 20.71 E; the window catalogue used 20.70
    "corfu": (39.62, 19.92),
    "zakynthos": (37.78, 20.90),
}


def fetch(name):
    p = OUT / name
    if p.exists():
        return p, False
    for attempt in range(5):
        try:
            with urllib.request.urlopen(BASE + name, timeout=120) as r:
                data = r.read()
            p.write_bytes(data)
            return p, True
        except Exception as exc:          # noqa: BLE001
            sys.stderr.write(f"retry {name}: {exc!r}\n")
            time.sleep(5 * 2 ** attempt)
    raise IOError(name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-fetch", action="store_true")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if not a.no_fetch:
        for name in ["program.js"] + [c + ".js" for c in CENTURIES]:
            p, new = fetch(name)
            h = hashlib.sha256(p.read_bytes()).hexdigest()
            print(f"{name:12s} {p.stat().st_size:7d} bytes  sha256 {h}  {'fetched' if new else 'present'}")
    (OUT / "sites").mkdir(exist_ok=True)
    files = [c + ".js" for c in CENTURIES]
    for site, (lat, lon) in SITES.items():
        out = OUT / "sites" / f"{site}.jsonl"
        r = subprocess.run(["node", str(ROOT / "tools" / "jsex_sites.js"), str(OUT), str(lat), str(lon)] + files,
                           capture_output=True, text=True, check=True)
        out.write_text(r.stdout, encoding="utf-8", newline="\n")
        print(f"{out.relative_to(ROOT)}: {len(r.stdout.splitlines())} eclipses")


if __name__ == "__main__":
    main()
