# Two-sided Fisher exact p for the stationarity (R21) and homogeneity (R20) tables of
# DESIGN revision 6, 2.9 (counts as printed there). Recheck of revision 6 (round 2).
from scipy.stats import fisher_exact
cases = {'P_BM halves H3 12/41 vs 3/35': [[12, 29], [3, 32]], 'P_MWRA halves H3 8/25 vs 0/18': [[8, 17], [0, 18]],
         'P_BM near/far H3 10/49 vs 5/27': [[10, 39], [5, 22]], 'P_MWRA near/far 6/28 vs 2/15': [[6, 22], [2, 13]],
         'P_BM classes H3 8/43 vs 7/33': [[8, 35], [7, 26]]}
for k, t in cases.items():
    print(k, 'two-sided Fisher p = %.4f' % fisher_exact(t)[1])
