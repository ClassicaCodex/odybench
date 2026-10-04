# Times one call of the review's independent Besselian solver (results/critique-design/check_bessel.py),
# which DESIGN 6.1 names as I16's reference for solar local circumstances, and scales it to a full
# 1-degree site grid (DESIGN 6.3.1: about 2e4 cells per eclipse) for I16(a)'s 21 null windows.
# Recheck of DESIGN revision 6 (round 2). Output: bessel_timing.out.txt
import sys, time
sys.path.insert(0, r'C:/Projects/odybench/results/critique-design')
import check_bessel as cb
E = cb.elems(cb.load_jsex('C:/Projects/odybench/data/refs/nasa/JSEX-SEm1199.js')[(-1177, 4, 16)])
t = time.perf_counter(); n = 20
for i in range(n):
    r = cb.maxecl(E, 38.0 + i * 0.1, 20.0, E['dT'])
dt = (time.perf_counter() - t) / n
print('one maxecl call: %.1f ms' % (dt * 1e3))
cells = 2e4; ecl_per_window = 330
per_window_s = cells * ecl_per_window * dt
print('one 1-deg grid (2e4 cells) x 330 solar eclipses (one 136-yr window): %.0f core-h' % (per_window_s / 3600))
print('x 21 null-side windows x 3 site-none solar events (T1, T2, X2): %.0f core-h = %.0f h on 14 cores'
      % (per_window_s * 21 * 3 / 3600, per_window_s * 21 * 3 / 3600 / 14))
