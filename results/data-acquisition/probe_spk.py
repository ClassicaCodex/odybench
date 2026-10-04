"""Probe the NAIF DE441/DE431 split kernels: segments and bytes needed for a span (scratch)."""
import sys
from jplephem.daf import DAF
from jplephem.excerpter import RemoteFile
from jplephem.spk import SPK
sys.path.insert(0, ".")
from odybench.ephem import jd_from_julian
NAIF = "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/"
jd0 = jd_from_julian(-2060, 1, 1); jd1 = jd_from_julian(241, 1, 1)
print("span JD", jd0, jd1)
for src in sys.argv[1:]:
    spk = SPK(DAF(RemoteFile(NAIF + src)))
    tot = 0
    for summ, seg in zip(spk.daf.summaries(), spk.segments):
        name, values = summ
        start, end = values[-2], values[-1]
        init, intlen, rsize, n = spk.daf.read_array(end - 3, end)
        s0 = (jd0 - 2451545.0) * 86400; s1 = (jd1 - 2451545.0) * 86400
        i = int(max(0, min(n, (s0 - init) // intlen))); j = int(max(0, min(n, (s1 - init) // intlen + 1)))
        nbytes = (j - i) * rsize * 8
        tot += nbytes if seg.target in (1,2,3,4,5,6,10,199,299,301,399) else 0
        print(f"{src} target {seg.target:4d} center {seg.center:3d} JD {seg.start_jd:.1f}..{seg.end_jd:.1f} intlen {intlen/86400:.1f} d rsize {int(rsize)} n {int(n)} -> {nbytes/1e6:8.2f} MB")
    print(src, "total (11 targets)", tot / 1e6, "MB")
