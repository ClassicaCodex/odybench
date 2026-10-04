# Round-3 copy of results/critique-design-r2/v6/narrowing_3b.py (unchanged machinery), extended
# with the frozen meaning and the inferred phase classes set to none.
# Null-side estimate, for the recheck of DESIGN revision 6 (round 2), of how many
# candidate days of a 136-year window pass each counted Almagest set's B&M-type
# projection (DESIGN 6.4, rows as listed in results/design-revision-v6/alm_rows.out.txt)
# under regime SL, i.e. whether a set CAN be "seen" (|S0| <= 0.05 N_cand) in any window.
#
# Reads no truth file and no control date. Windows are placed far from every
# Almagest record (-271..+141) and every PC-R record (-720..+136).
# Tolerances: Mercury greatest elongation 6 d (5 d for ALM-G), Venus 21 d (DESIGN 6.4,
# Appendix T2); "most lenient value" for every other list (DESIGN 6.4 regime table):
# visible_only >= 30 min, visible_before_sunrise >= 5 deg, equinox_tol 2 d, quarter tol 2 d.
#
# ROUGH by design: one geocentric sample per day at 0h UT (Moon interpolated to the
# row's instant), greatest elongations and conjunctions located to the day from the
# elongation series, rise/set leads from the analytic hour angle at Alexandria
# (31.20 N, 29.92 E) with h0 -0.8333 (Sun) / -0.5667 (planets), "dawn" = Sun at -8 deg.
# Rows that need a GE day or a conjunction day are good to about +-1 d.
import sys, json, math, time
import numpy as np
sys.path.insert(0, r"C:\Projects\odybench")
from odybench import ephem

LAT, LON = 31.20, 29.92
PHI = math.radians(LAT)
BODIES = ("sun", "moon", "mercury", "venus", "mars", "jupiter")

def positions(jd_ut):
    """geocentric apparent ecliptic longitude of date, RA and Dec of date (deg)."""
    t = ephem.time_ut(jd_ut, dt="smh2020")
    eps = ephem.mean_obliquity(t.tt) + t._nutation_angles_radians[1]
    out = {}
    for b in BODIES:
        a = ephem.apparent(b, t)
        v = a.xyz.au
        x, y, z = np.einsum("ij...,j...->i...", t.M, v)
        r = np.sqrt(x * x + y * y + z * z)
        ra = np.degrees(np.arctan2(y, x)) % 360.0
        dec = np.degrees(np.arcsin(z / r))
        yl = y * np.cos(eps) + z * np.sin(eps)
        lon = np.degrees(np.arctan2(yl, x)) % 360.0
        out[b] = dict(lon=lon, ra=ra, dec=dec)
    return out

def wrap180(a):
    return (a + 180.0) % 360.0 - 180.0

def hour_angle(dec_deg, h0_deg):
    d = np.radians(dec_deg)
    c = (math.sin(math.radians(h0_deg)) - math.sin(PHI) * np.sin(d)) / (math.cos(PHI) * np.cos(d))
    return np.degrees(np.arccos(np.clip(c, -1.0, 1.0)))   # degrees, >= 0

def main():
    windows = [(-1500, "w1"), (-1100, "w2"), (-700, "w3")]
    EXTRA = 3000          # days after the window for the longest offset (ALM-K: 2902)
    report = {}
    for y0, tag in windows:
        t0 = time.time()
        jd0 = ephem.jd_from_julian(y0, 1, 1) + 0.5 - 1.0      # 0h UT, from the day before
        n_win = int(round(ephem.jd_from_julian(y0 + 136, 1, 1) - ephem.jd_from_julian(y0, 1, 1)))
        n_all = n_win + EXTRA + 2
        jd = jd0 + np.arange(n_all, dtype=float)
        P = positions(jd)
        sun, moon = P["sun"], P["moon"]
        # signed elongations (east +) and separations
        el = {b: wrap180(P[b]["lon"] - sun["lon"]) for b in ("mercury", "venus", "mars", "jupiter")}
        # Moon-Sun elongation (0..360, east of the Sun increasing) at 0h UT; daily motion for interpolation
        E0 = (moon["lon"] - sun["lon"]) % 360.0
        dE = np.diff(np.unwrap(np.radians(E0))) * 180 / math.pi
        dE = np.append(dE, dE[-1])
        def E_at(hours_ut):                          # Moon-Sun elongation at hours UT of each day
            return (E0 + dE * hours_ut / 24.0) % 360.0
        # conjunction days (sign change of the signed elongation) and greatest elongations
        events = {}
        for b in ("mercury", "venus"):
            e = el[b]
            conj = np.nonzero(np.sign(e[:-1]) != np.sign(e[1:]))[0]        # index i: between i and i+1
            ae = np.abs(e)
            ge_e, ge_w = [], []
            for i in range(1, len(e) - 1):
                if ae[i] >= ae[i - 1] and ae[i] > ae[i + 1] and ae[i] > 10.0:
                    (ge_e if e[i] > 0 else ge_w).append(i)
            events[b] = dict(conj=np.array(conj), ge={"east": np.array(ge_e), "west": np.array(ge_w)})
        idx = np.arange(n_all)
        def near_ge(b, side, k):
            g = events[b]["ge"][side]
            d = np.abs(idx[:, None] - g[None, :]).min(axis=1)
            return d <= k
        def same_app(b, side, after):
            """on `side` today; GE on that side still ahead (after=True) or already passed
            (after=False) within the current apparition (between consecutive conjunctions)."""
            e = el[b]
            on = (e > 0) if side == "east" else (e < 0)
            conj = events[b]["conj"]
            g = events[b]["ge"][side]
            res = np.zeros(n_all, bool)
            for i in np.nonzero(on)[0]:
                prev_c = conj[conj < i]
                next_c = conj[conj >= i]
                lo = prev_c[-1] + 1 if len(prev_c) else -10**9
                hi = next_c[0] if len(next_c) else 10**9
                if after:
                    res[i] = np.any((g >= i) & (g <= hi))
                else:
                    res[i] = np.any((g >= lo) & (g <= i))
            return res
        # rise lead (morning) / set lag (evening), minutes, at Alexandria
        def lead_min(b, side):
            Hs = hour_angle(sun["dec"], -0.8333)
            Hb = hour_angle(P[b]["dec"], -0.5667)
            if side == "west":     # rising: sidereal time of rising = RA - H
                d = wrap180((sun["ra"] - Hs) - (P[b]["ra"] - Hb))
            else:                  # setting: RA + H
                d = wrap180((P[b]["ra"] + Hb) - (sun["ra"] + Hs))
            return d * 4.0 * 0.99727
        def visible_before_sunrise(b, min_alt=5.0, sun_alt=-8.0):
            Hs = hour_angle(sun["dec"], sun_alt)         # Sun at sun_alt deg (DESIGN 6.4: -8; 10.3 says civil dawn, -6)
            lst = sun["ra"] - Hs
            H = np.radians(lst - P[b]["ra"])
            d = np.radians(P[b]["dec"])
            alt = np.degrees(np.arcsin(np.sin(PHI) * np.sin(d) + np.cos(PHI) * np.cos(d) * np.cos(H)))
            return alt >= min_alt
        # equinox instants (Sun longitude crossing 0), as day index with fraction
        sl = sun["lon"]
        eq_i = np.nonzero((wrap180(sl[:-1]) < 0) & (wrap180(sl[1:]) >= 0))[0]
        eq_t = eq_i + (-wrap180(sl[eq_i])) / (wrap180(sl[eq_i + 1]) - wrap180(sl[eq_i]))
        def equinox_within(row_hours_ut, tol_d):
            tt = idx + row_hours_ut / 24.0
            d = np.abs(tt[:, None] - eq_t[None, :]).min(axis=1)
            return d <= tol_d
        # instants (UT hours at Alexandria, LAT ~ UT + 2 h): evening ~17 h UT, dawn ~2.5 h UT
        EV, DAWN = 17.0, 2.5
        E_ev, E_dawn = E_at(EV), E_at(DAWN)
        rows = {
            # projection rows as in alm_rows.out.txt; (offset, boolean array)
            "ALM-A": [(0, same_app("mercury", "east", True)),
                      (0, (E_ev > 0) & (E_ev <= 45)),                    # young crescent
                      (13, (E_at(19.0) >= 150) & (E_at(19.0) <= 210)),   # near full
                      (52, near_ge("mercury", "west", 6)),
                      (55, visible_before_sunrise("jupiter"))],
            "ALM-B": [(0, same_app("venus", "west", False)),
                      (0, (E_dawn > 270) & (E_dawn < 360)),              # waning crescent
                      (55, np.abs(E_at(4.75) - 270) <= 24.4)],           # last quarter, tol 2 d
            "ALM-D": [(0, near_ge("mercury", "east", 6)), (35, near_ge("venus", "east", 21))],
            "ALM-E": [(0, near_ge("venus", "east", 21)), (33, equinox_within(11.0, 2.0))],
            "ALM-F": [(0, near_ge("venus", "east", 21)), (37, near_ge("venus", "east", 21))],
            "ALM-G": [(0, near_ge("venus", "west", 21)), (106, near_ge("mercury", "west", 5))],
            "ALM-H": [(0, lead_min("mercury", "west") >= 30), (102, lead_min("mercury", "east") >= 30),
                      (192, lead_min("mercury", "east") >= 30)],
            "ALM-I": [(0, same_app("mercury", "west", True))],
            "ALM-J": [(0, visible_before_sunrise("mars")), (267, same_app("venus", "west", False))],
            "ALM-K": [(0, lead_min("mercury", "west") >= 30), (1385, visible_before_sunrise("jupiter")),
                      (2902, lead_min("mercury", "west") >= 30)],
            "ALM-L": [(0, near_ge("venus", "west", 21)), (586, near_ge("venus", "west", 21)),
                      (996, near_ge("mercury", "east", 6))],
        }
        # the same rows with "same apparition" also requiring visibility (>= 30 min), a stricter bracket
        strict = {
            "ALM-A": [(0, same_app("mercury", "east", True) & (lead_min("mercury", "east") >= 30))] + rows["ALM-A"][1:],
            "ALM-B": [(0, same_app("venus", "west", False) & (lead_min("venus", "west") >= 30))] + rows["ALM-B"][1:],
            "ALM-I": [(0, same_app("mercury", "west", True) & (lead_min("mercury", "west") >= 30))],
            "ALM-J": [rows["ALM-J"][0], (267, same_app("venus", "west", False) & (lead_min("venus", "west") >= 30))],
        }
        # Round-3 addition: the frozen meaning (visible) with the three phase classes that the
        # clue file marks as the drafter's inference ("the Moon's phase is not stated in words")
        # set to none: A.2 (young crescent), A.5 (near full), B.2 (waning crescent). B.7's
        # class rests on words (tetartemoriou) and stays.
        words = {
            "ALM-A": [strict["ALM-A"][0], rows["ALM-A"][3], rows["ALM-A"][4]],      # A.1 vis, A.7, A.9
            "ALM-A (A.2 only none)": [strict["ALM-A"][0], rows["ALM-A"][2], rows["ALM-A"][3], rows["ALM-A"][4]],
            "ALM-A (A.5 only none)": [strict["ALM-A"][0], rows["ALM-A"][1], rows["ALM-A"][3], rows["ALM-A"][4]],
            "ALM-B": [strict["ALM-B"][0], rows["ALM-B"][2]],                         # B.1 vis, B.7
            # the same words-only ALM-A with A.9 judged at civil dawn (Sun -6 deg), as 10.3's
            # alt_at row says, instead of 6.4's Sun -8 deg
            "ALM-A (civil dawn for A.9)": [strict["ALM-A"][0], rows["ALM-A"][3],
                                           (55, visible_before_sunrise("jupiter", sun_alt=-6.0))],
            "ALM-A as projected (civil dawn for A.9)": [strict["ALM-A"][0], rows["ALM-A"][1], rows["ALM-A"][2],
                                                        rows["ALM-A"][3],
                                                        (55, visible_before_sunrise("jupiter", sun_alt=-6.0))],
        }
        start = 1                               # index of the window's first day (jd0 was the day before)
        out = {}
        for name, rr in (list(rows.items()) + [(k + " (same_app & visible)", v) for k, v in strict.items()]
                         + [(k + " [frozen, inferred phases none]", v) for k, v in words.items()]):
            ok = np.ones(n_win, bool)
            for off, arr in rr:
                ok &= arr[start + off: start + off + n_win]
            frac = float(ok.mean())
            per_row = [float(arr[start + off: start + off + n_win].mean()) for off, arr in rr]
            out[name] = dict(frac=round(frac, 4), n_pass=int(ok.sum()), n_cand=n_win,
                             narrows=frac <= 0.05, per_row=[round(x, 3) for x in per_row])
        report[tag] = dict(start_year=y0, n_cand=n_win, sets=out, seconds=round(time.time() - t0, 1))
        print(tag, y0, "N_cand", n_win, "5% =", round(0.05 * n_win), "days", f"({time.time()-t0:.0f} s)")
        for name, r in out.items():
            print(f"  {name:32s} pass {r['frac']*100:6.2f}%  ({r['n_pass']:6d} days)  narrows: {r['narrows']}  per-row {r['per_row']}")
    json.dump(report, open(__file__.replace(".py", ".json"), "w"), indent=1)

if __name__ == "__main__":
    main()
