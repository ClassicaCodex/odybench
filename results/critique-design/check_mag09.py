# Delta-T range (canon frame) giving magnitude >= 0.9 at Ithaki for -1177 Apr 16, NASA elements; and P under each model
import sys, os, math
sys.path.insert(0, "C:/Projects/odybench"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from odybench import ephem as E
import check_bessel as B
Phi = lambda z: 0.5*(1+math.erf(z/math.sqrt(2)))
Ee = B.elems(B.load_jsex("C:/Projects/odybench/data/refs/nasa/JSEX-SEm1199.js")[(-1177,4,16)])
ok = [dt for dt in range(25000, 33001, 20) if B.maxecl(Ee, 38.367, 20.717, dt)['mag'] >= 0.9]
lo, hi = min(ok), max(ok); print("mag>=0.9 for canon-frame dT in [%d, %d] s (20-s grid)" % (lo, hi))
y = E.julian_epoch(E.jd_from_julian(-1177,4,16,12))
conv = -0.91072*(-25.858+25.82)*((y-1955)/100)**2
for m in ("smh2020","smh2020_parabola","smh2016_parabola","em2006_canon"):
    mu = E.delta_t(y, m) + (conv if m.startswith("smh") else 0); s = E.delta_t_sigma(y, m)
    print("%-17s P(mag>=0.9) = %.3f" % (m, Phi((hi-mu)/s) - Phi((lo-mu)/s)))
