"""Design revision 3 scratch: where does 30 Sep 1131 BC (-1130) fall in the
ancient Greek seasonal divisions at Ithaki?

- Agricultural/Hesiodic: autumn begins with Arcturus' morning first visibility
  (heliacal rising; Hesiod WD 609-611, vintage "when Dawn sees Arcturus"),
  winter with the Pleiades' morning setting (WD 615-617).
- Astronomical (Geminus 1.9): autumn begins at the autumnal equinox.

Arcturus' heliacal rising here = first morning on which Arcturus rises
(centre at -0.5667 deg, airless, as the bench's rise convention) while the Sun
is at or below -AV, for AV in {8, 10, 12} (research-visibility's AV band for
Arcturus).  1-minute grid; DE441; SMH2020 Delta-T; 38.37 N 20.72 E.
Also -1177 for comparison with research-visibility 3.3 (8-13 Sep).
Run: cd C:/Projects/odybench && py results/design-revision-r2/ranc_season.py
"""
import sys
import numpy as np

sys.path.insert(0, ".")
from odybench import ephem, calendar as cal  # noqa: E402

LAT, LON = 38.37, 20.72
H0 = -0.5667


def heliacal_rising(year, av):
    lmt = cal.lmt_offset_hours(LON)
    for doy_month, doy_day in [(8, d) for d in range(15, 32)] + [(9, d) for d in range(1, 31)] + [(10, d) for d in range(1, 16)]:
        jdn = cal.jdn_from_julian(year, doy_month, doy_day)
        # 00:00 to 08:00 LMT of that civil day, in UT
        jd0 = jdn - 0.5 - lmt / 24.0
        grid = jd0 + np.arange(0, 8 * 60 + 1) / 1440.0
        a_star, _ = ephem.altaz("arcturus", grid, LAT, LON)
        a_sun, _ = ephem.altaz("sun", grid, LAT, LON)
        a_star, a_sun = np.asarray(a_star), np.asarray(a_sun)
        idx = np.nonzero((a_star[:-1] < H0) & (a_star[1:] >= H0))[0]
        if len(idx) == 0:
            continue
        i = idx[0]
        if a_sun[i] <= -av:
            return (year, doy_month, doy_day, float(a_sun[i]))
    return None


def main():
    for year in (-1177, -1130):
        for av in (8, 10, 12):
            print(f"year {year}  AV {av:>2}: Arcturus morning first {heliacal_rising(year, av)}")
    # autumnal equinox -1130 for reference (r1: 3 Oct 17:17 UT)


if __name__ == "__main__":
    main()
