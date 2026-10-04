"""Cross-check of Sirius A's orbital velocity at J1991.25 with two orbits (scratch):
Bond et al. 2017 (Tables 4-5) and the Hipparcos DMSA/O solution (I/239 hip_dm_o)."""
import math
def vel(P_yr, T_yr, a_mas, e, w_deg, i_deg, Om_deg, ep, sign):
    i, Om, w = map(math.radians, (i_deg, Om_deg, w_deg))
    A = a_mas * (math.cos(w) * math.cos(Om) - math.sin(w) * math.sin(Om) * math.cos(i))
    B = a_mas * (math.cos(w) * math.sin(Om) + math.sin(w) * math.cos(Om) * math.cos(i))
    F = a_mas * (-math.sin(w) * math.cos(Om) - math.cos(w) * math.sin(Om) * math.cos(i))
    G = a_mas * (-math.sin(w) * math.sin(Om) + math.cos(w) * math.cos(Om) * math.cos(i))
    def pos(t):
        M = 2 * math.pi * (t - T_yr) / P_yr; E = M
        for _ in range(60): E -= (E - e * math.sin(E) - M) / (1 - e * math.cos(E))
        X, Y = math.cos(E) - e, math.sqrt(1 - e * e) * math.sin(E)
        return sign * (B * X + G * Y), sign * (A * X + F * Y)
    h = 1e-3
    (e1, n1), (e2, n2) = pos(ep - h), pos(ep + h)
    return (e2 - e1) / (2 * h), (n2 - n1) / (2 * h), pos(ep)
ep = 1991.25
# Bond 2017: relative orbit of B about A; A's orbit = -(aA/a) x relative, aA = 2476.1 mas
ve, vn, p = vel(50.1284, 1994.5715, 2476.1, 0.59142, 149.161, 136.336, 45.400, ep, -1)
print(f"Bond 2017:  v_A = ({ve:+.1f} E, {vn:+.1f} N) mas/yr, |v| {math.hypot(ve, vn):.1f}; offset of A from barycentre ({p[0]:+.0f}, {p[1]:+.0f}) mas")
# Hipparcos DMSA/O: photocentre orbit, P 18295.4 d, T = JD 2440000 - 27123.7, a0 2490.40 mas, e .5923, w 327.27, i 136.53, Om 44.86
T = 2000.0 + (2440000.0 - 27123.7 - 2451545.0) / 365.25
P = 18295.4 / 365.25
ve2, vn2, p2 = vel(P, T, 2490.40, 0.5923, 327.27, 136.53, 44.86, ep, +1)
print(f"Hipparcos DMSA/O: T = {T:.3f}, P = {P:.3f} yr; v_photocentre = ({ve2:+.1f} E, {vn2:+.1f} N) mas/yr, |v| {math.hypot(ve2, vn2):.1f}; offset ({p2[0]:+.0f}, {p2[1]:+.0f}) mas")
print(f"difference between the two orbits' velocities: {math.hypot(ve - ve2, vn - vn2):.1f} mas/yr")
