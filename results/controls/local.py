import math, sys
from hz import horizons, jd_julian, jd_to_julian
OMEGA = 360/86164.0905
def sep_deg(ra1, d1, ra2, d2):
    r = math.radians
    c = math.sin(r(d1))*math.sin(r(d2)) + math.cos(r(d1))*math.cos(r(d2))*math.cos(r(ra1-ra2))
    return math.degrees(math.acos(max(-1, min(1, c))))
def solar_local(lon, lat, y, m, d_td, dT_nasa, half_window_h=4.0, step='2 m', dT_alt=None):
    """d_td: fractional day of NASA greatest eclipse in TD. Returns dict for Horizons dT and alt dT."""
    jd_ut_guess = jd_julian(y, m, d_td) - dT_nasa/86400
    res = {}
    for label, dTa in (('horizons', None), ('alt', dT_alt)):
        if label == 'alt' and dTa is None: continue
        # first get horizons dT
        probe = horizons(10, lon, lat, jd_ut_guess, jd_ut_guess+0.01, step='10 m')
        dTh = probe[0][6]
        if dTa is None: lon_eff, shift = lon, 0.0
        else:
            delta = dTa - dTh
            lon_eff, shift = lon - OMEGA*delta, delta
        jd0 = jd_ut_guess - half_window_h/24 + shift/86400; jd1 = jd_ut_guess + half_window_h/24 + shift/86400
        S = horizons(10, round(lon_eff, 4), lat, jd0, jd1, step=step)
        M = horizons(301, round(lon_eff, 4), lat, jd0, jd1, step=step)
        best = None; bestup = None
        for s, mm in zip(S, M):
            rs = s[5]/7200; rm = mm[5]/7200
            sp = sep_deg(s[1], s[2], mm[1], mm[2])
            mag = (rs + rm - sp)/(2*rs)
            if best is None or mag > best[0]:
                best = (mag, s[0], s[4], sp, rs, rm)
            if s[4] > -0.83 and (bestup is None or mag > bestup[0]):
                bestup = (mag, s[0], s[4], sp, rs, rm)
        mag, jd_h, el, sp, rs, rm = best
        magup = bestup[0] if bestup else None
        total = (rm > rs) and (sp < rm - rs)
        jd_ut = jd_h - shift/86400   # UT under the assumed dT
        lmt = (jd_ut + 0.5 + lon/360) % 1 * 24
        res[label] = dict(dT=dTh if dTa is None else dTa, mag=mag, magup=magup, total=total, edge=(abs(jd_h-jd0)<0.01 or abs(jd_h-jd1)<0.01), ut=jd_to_julian(jd_ut), lmt_h=lmt, sun_el=el)
    return res
def lunar_moon_alt(lon, lat, y, m, d_td, dT_nasa):
    jd_ut = jd_julian(y, m, d_td) - dT_nasa/86400
    M = horizons(301, lon, lat, jd_ut, jd_ut+0.001, step='1 m')
    S = horizons(10, lon, lat, jd_ut, jd_ut+0.001, step='1 m')
    lmt = (jd_ut + 0.5 + lon/360) % 1 * 24
    return dict(moon_el=M[0][4], sun_el=S[0][4], lmt_h=lmt, ut=jd_to_julian(jd_ut), dTh=M[0][6])
def fmt_h(h):
    hh = int(h); mm = int(round((h-hh)*60))
    if mm == 60: hh, mm = hh+1, 0
    return f'{hh:02d}:{mm:02d}'
