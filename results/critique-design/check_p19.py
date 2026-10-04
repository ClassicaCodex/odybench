import sys, math
sys.path.insert(0, "C:/Projects/odybench")
from odybench import ephem as E
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_bessel as B
Phi = lambda z: 0.5*(1+math.erf(z/math.sqrt(2)))
# epochs (Julian epoch of the eclipse dates)
y78 = E.julian_epoch(E.jd_from_julian(-1177,4,16,12)); y31 = E.julian_epoch(E.jd_from_julian(-1130,9,30,12))
print("epochs", round(y78,3), round(y31,3))
W78 = (28805, 29580); W31 = (27050, 28035)   # canon-frame totality windows at Ithaki (my Besselian solver)
def conv(y):  # SMH (ndot -25.82) -> canon (ndot -25.858), seconds
    return -0.91072*(-25.858+25.82)*((y-1955)/100)**2
rows = []
for model in ("smh2020","smh2020_parabola","smh2016_parabola","em2006","em2006_canon"):
    m78, m31 = E.delta_t(y78, model), E.delta_t(y31, model)
    s78, s31 = E.delta_t_sigma(y78, model), E.delta_t_sigma(y31, model)
    c78 = conv(y78) if model.startswith("smh") else (0.0 if model=="em2006_canon" else E.ndot_correction(y78, -25.858, -26.0) if hasattr(E,'ndot_correction') else 0)
    c31 = conv(y31) if model.startswith("smh") else (0.0 if model=="em2006_canon" else E.ndot_correction(y31, -25.858, -26.0))
    mu78, mu31 = m78 + c78, m31 + c31
    p78 = Phi((W78[1]-mu78)/s78) - Phi((W78[0]-mu78)/s78)
    p31 = Phi((W31[1]-mu31)/s31) - Phi((W31[0]-mu31)/s31)
    lo = max(W78[0]-mu78, W31[0]-mu31); hi = min(W78[1]-mu78, W31[1]-mu31)
    pj = (Phi(hi/s78) - Phi(lo/s78)) if hi > lo else 0.0
    print(f"{model:18s} dT78 {m78:8.0f}+{c78:5.0f} s78 {s78:5.0f} | dT31 {m31:8.0f}+{c31:5.0f} s31 {s31:5.0f} | P78 {p78:.3f} P31 {p31:.3f} | joint(common offset) {pj:.3f} overlap [{lo:.0f},{hi:.0f}]")
# canon itself with Huber sigma
for name, mu78, mu31 in (("canon(Huber)", 28590.0, 27690.9),):
    s78, s31 = E.sigma_huber(y78), E.sigma_huber(y31)
    p78 = Phi((W78[1]-mu78)/s78) - Phi((W78[0]-mu78)/s78); p31 = Phi((W31[1]-mu31)/s31) - Phi((W31[0]-mu31)/s31)
    lo = max(W78[0]-mu78, W31[0]-mu31); hi = min(W78[1]-mu78, W31[1]-mu31)
    print(name, round(s78), round(s31), "P78 %.3f P31 %.3f joint %.3f" % (p78, p31, Phi(hi/s78)-Phi(lo/s78)))
# magnitude definitions for the 1131 total at Ithaki
EL = B.load_jsex("C:/Projects/odybench/data/refs/nasa/JSEX-SEm1199.js")
Ee = B.elems(EL[(-1130,9,30)]); r = B.maxecl(Ee, 38.367, 20.717, Ee['dT'])
print("1131 at Ithaki: (L1-m)/(L1+L2) = %.4f ; diameter ratio (L1-L2)/(L1+L2) = %.4f" % (r['mag'], (r['L1']-r['L2'])/(r['L1']+r['L2'])))
