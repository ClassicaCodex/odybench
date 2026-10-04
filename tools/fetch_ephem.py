"""
Re-create the JPL ephemeris excerpts in data/ephem/.  Only the needed byte
ranges of NAIF's split kernels are downloaded (HTTP Range requests), in
chunks of at most 8 MB with retries; no single excerpt is over 300 MB.

    cd C:\\Projects\\odybench && py tools/fetch_ephem.py            # fetch what is missing
    py tools/fetch_ephem.py --list                                  # show the jobs
    py tools/fetch_ephem.py --only de441_m2060_p0241 --force        # redo one job

Existing outputs are never overwritten unless --force is given.  After each
excerpt the script prints its size, SHA-256, JD coverage and targets; the
same facts are tabulated in docs/data-acquisition.md.

Jobs (JD bounds are 0h TDB; calendar labels are PROLEPTIC JULIAN,
astronomical years, except where a bound is marked Gregorian):

* 2026-10-03 (research-ephemeris task):
  - de441_m1320_m1030.bsp: JD 1238939.5-1344860.5 (= proleptic GREGORIAN
    -1320-01-01 .. -1030-01-01, the convention of `jplephem excerpt`), 11
    targets; and the DE431 counterpart with 8 targets.
  - +-60 d eclipse excerpts around -762 Jun 15, -584 May 28, -135 Apr 15,
    -708 Jul 17 (DE441; DE431 except -584).
* 2026-10-04 (data-acquisition task, DESIGN 7.3 and critique issue 10):
  - de441_m2060_p0241.bsp: DE441, -2060-01-01 .. +241-01-01 Julian
    (JD 968642.5-1809083.5), the same 11 targets (237.8 MB of records).
  - de431/de431_m2060_p0001.bsp: DE431 part-1, Sun/EMB/Earth/Moon
    (10, 3, 399, 301) from -2060-01-01 Julian to the end of part-1 at
    JD 1721425.5 (= 1 Jan 3 Julian = AD 1 Jan 1 Gregorian).
  - de431/de431_p0001_p0241.bsp: DE431 part-2, same targets, JD 1721425.5 ..
    1809083.5.  DE431 is split at JD 1721425.5 on the server, so no single
    DE431 excerpt can straddle that instant.
  - de431/de431_m1339_eclipse.bsp, de431_m0647_eclipse.bsp: +-60 d around
    -1339 Jan 8 (1340 BC, Gainsford's list) and -647 Apr 6 (648 BC,
    Archilochus), targets 3, 10, 301, 399 [DESIGN 7.3].

Equivalent command line for the original main excerpt (note the "--":
jplephem's argparse otherwise reads a negative date as an option; dates are
PROLEPTIC GREGORIAN yyyy/mm/dd, astronomical years):

    py -m jplephem excerpt --targets 1,2,3,4,5,6,10,199,299,301,399 -- \
        -1320/1/1 -1030/1/1 \
        https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de441_part-1.bsp \
        data/ephem/de441_m1320_m1030.bsp

(https://ssd.jpl.nasa.gov/ftp/eph/planets/bsp/de441_part-1.bsp returns 404:
the split files live only on the NAIF server; ssd.jpl.nasa.gov has the
unsplit de441.bsp.)
"""
import argparse
import hashlib
import sys
import time
import urllib.request
from pathlib import Path

from jplephem.daf import DAF
from jplephem.excerpter import RemoteFile, write_excerpt
from jplephem.spk import SPK

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from odybench.ephem import jd_from_julian  # noqa: E402

NAIF = "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/"
ALL11 = (1, 2, 3, 4, 5, 6, 10, 199, 299, 301, 399)
SEM = (3, 10, 301, 399)          # Sun, EMB, Earth, Moon: enough for eclipses and new moons
JD_M2060 = jd_from_julian(-2060, 1, 1)      # 968642.5
JD_P0241 = jd_from_julian(241, 1, 1)        # 1809083.5
JD_DE431_SPLIT = 1721425.5                  # end of de431_part-1 / start of part-2 (NAIF log)

JOBS = [
    # (source file, output, jd0, jd1, targets)
    ("de441_part-1.bsp", "data/ephem/de441_m1320_m1030.bsp", 1238939.5, 1344860.5, ALL11),
    ("de431_part-1.bsp", "data/ephem/de431/de431_m1320_m1030.bsp", 1238939.5, 1344860.5,
     (1, 2, 3, 10, 199, 299, 301, 399)),
]
for name, (y, m, d) in {"m0762": (-762, 6, 15), "m0584": (-584, 5, 28),
                        "m0135": (-135, 4, 15), "m0708": (-708, 7, 17)}.items():
    jd = jd_from_julian(y, m, d)
    JOBS.append(("de441_part-1.bsp", f"data/ephem/de441_{name}_eclipse.bsp", jd - 60, jd + 60, SEM))
    if name != "m0584":
        JOBS.append(("de431_part-1.bsp", f"data/ephem/de431/de431_{name}_eclipse.bsp", jd - 60, jd + 60, SEM))
# --- added 2026-10-04 (data-acquisition task)
JOBS += [
    ("de441_part-1.bsp", "data/ephem/de441_m2060_p0241.bsp", JD_M2060, JD_P0241, ALL11),
    ("de431_part-1.bsp", "data/ephem/de431/de431_m2060_p0001.bsp", JD_M2060, JD_DE431_SPLIT, SEM),
    ("de431_part-2.bsp", "data/ephem/de431/de431_p0001_p0241.bsp", JD_DE431_SPLIT, JD_P0241, SEM),
]
for name, (y, m, d) in {"m1339": (-1339, 1, 8), "m0647": (-647, 4, 6)}.items():
    jd = jd_from_julian(y, m, d)
    JOBS.append(("de431_part-1.bsp", f"data/ephem/de431/de431_{name}_eclipse.bsp", jd - 60, jd + 60, SEM))


class ChunkedRemoteFile(RemoteFile):
    """jplephem's RemoteFile, but each read is split into <= CHUNK-byte Range
    requests with a timeout and retries, and the bytes received are counted."""
    CHUNK = 8 * 1024 * 1024

    def __init__(self, url):
        super().__init__(url)
        self.received = 0

    def _get(self, start, size):
        rng = f"bytes={start}-{start + size - 1}"
        for attempt in range(6):
            try:
                req = urllib.request.Request(self.url, headers={"Range": rng})
                with urllib.request.urlopen(req, timeout=300) as r:
                    if r.status != 206:
                        raise IOError(f"HTTP {r.status} for Range {rng}")
                    data = r.read()
                if len(data) != size:
                    raise IOError(f"asked for {size} bytes ({rng}), got {len(data)}")
                return data
            except Exception as exc:          # noqa: BLE001
                wait = 5 * 2 ** attempt
                sys.stderr.write(f"  retry {attempt + 1} for {rng}: {exc!r}; waiting {wait} s\n")
                time.sleep(wait)
        raise IOError(f"giving up on {rng}")

    def read(self, size):
        out = []
        start = self.offset
        done = 0
        while done < size:
            n = min(self.CHUNK, size - done)
            out.append(self._get(start + done, n))
            done += n
            self.received += n
            if size > self.CHUNK:
                sys.stderr.write(f"  {self.filename}: {done / 1e6:7.1f} / {size / 1e6:.1f} MB\n")
        self.offset += size
        return b"".join(out)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def describe(path):
    """Size, SHA-256, common JD coverage and targets of an SPK file."""
    with open(path, "rb") as f:
        spk = SPK(DAF(f))
        segs = spk.segments
        jd0 = max(s.start_jd for s in segs)
        jd1 = min(s.end_jd for s in segs)
        targets = sorted({s.target for s in segs})
    return dict(bytes=Path(path).stat().st_size, sha256=sha256(path), jd0=jd0, jd1=jd1, targets=targets)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true", help="list the jobs and exit")
    ap.add_argument("--only", nargs="*", default=None, help="output basenames (without .bsp) to run")
    ap.add_argument("--force", action="store_true", help="overwrite existing outputs")
    a = ap.parse_args()
    cache = {}
    for src, out, jd0, jd1, targets in JOBS:
        p = ROOT / out
        stem = p.stem
        if a.list:
            print(f"{out:45s} {src:18s} JD {jd0:.1f}..{jd1:.1f} targets {list(targets)}"
                  f"  {'exists' if p.exists() else 'missing'}")
            continue
        if a.only is not None and stem not in a.only:
            continue
        if p.exists() and not a.force:
            print(f"{out}: exists, skipped (use --force to refetch)")
            continue
        if src not in cache:
            f = ChunkedRemoteFile(NAIF + src)
            cache[src] = (f, SPK(DAF(f)))
        f, spk = cache[src]
        before = f.received
        summ = [s for s, seg in zip(spk.daf.summaries(), spk.segments) if seg.target in targets]
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_suffix(".bsp.part")
        t0 = time.time()
        with open(tmp, "w+b") as o:
            write_excerpt(spk, o, jd0, jd1, summ)
        tmp.replace(p)
        d = describe(p)
        print(f"{out}: {d['bytes']} bytes, {(f.received - before) / 1e6:.1f} MB downloaded in "
              f"{time.time() - t0:.0f} s; JD {d['jd0']:.1f}..{d['jd1']:.1f}; targets {d['targets']}; "
              f"sha256 {d['sha256']}")


if __name__ == "__main__":
    main()
