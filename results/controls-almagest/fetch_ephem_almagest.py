r"""DE441 excerpts for the Almagest records (AD 120-145 and 296-224 BC), written
ONLY to results/controls-almagest/ephem/ (scratch).  Same method as
tools/fetch_ephem.py: HTTP Range reads of NAIF de441_part-1.bsp via jplephem.

    cd C:\Projects\odybench && py results/controls-almagest/fetch_ephem_almagest.py
"""
import sys
from pathlib import Path
from jplephem.daf import DAF
from jplephem.excerpter import RemoteFile, write_excerpt
from jplephem.spk import SPK

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from odybench.ephem import jd_from_julian  # noqa: E402

NAIF = "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de441_part-1.bsp"
OUT = Path(__file__).resolve().parent / "ephem"
TARGETS = (1, 2, 3, 4, 5, 6, 10, 199, 299, 301, 399)
JOBS = [("de441_p0120_p0145.bsp", jd_from_julian(120, 1, 1), jd_from_julian(145, 1, 1)),
        ("de441_m0296_m0224.bsp", jd_from_julian(-296, 1, 1), jd_from_julian(-224, 1, 1))]
if __name__ == "__main__":
    spk = SPK(DAF(RemoteFile(NAIF)))
    summ = [s for s, seg in zip(spk.daf.summaries(), spk.segments) if seg.target in TARGETS]
    OUT.mkdir(parents=True, exist_ok=True)
    for name, jd0, jd1 in JOBS:
        p = OUT / name
        with open(p, "w+b") as o:
            write_excerpt(spk, o, jd0, jd1, summ)
        print(name, jd0, jd1, p.stat().st_size, "bytes")
