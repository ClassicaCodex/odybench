"""Independent consistency check of the day_offsets in controls_almagest.json
against the MEAN-Sun longitudes Ptolemy states in the same rows.
Computed by me (license-check-almagest task). Inputs typed from the data/text
rows quoted in docs/license-check-almagest.md; no truth file read.
Ptolemy's mean solar motion: 0;59,8,17,13,12,31 deg/day (Almagest III.1).
Times of day: hours after local midnight of the civil day (approx; 'dawn' = 5h,
'evening' = 19h when no hour is stated).
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
v = 59/60 + 8/3600 + 17/60**3 + 13/60**4 + 12/60**5 + 31/60**6
SIGN = dict(Ari=0, Tau=30, Gem=60, Cnc=90, Leo=120, Vir=150, Lib=180, Sco=210,
            Sgr=240, Cap=270, Aqr=300, Psc=330)
def L(sign, d, m=0):
    return SIGN[sign] + d + m/60

# (set, from-record, to-record, file day_offset, lam0, hour0, lam1, hour1)
cases = [
    ('A', 'IX.10.3', 'X.8.2', 13, L('Tau', 22, 34), 19.5, L('Gem', 5, 27), 21.0),
    ('A', 'IX.10.3', 'IX.9.4 as printed', 52, L('Tau', 22, 34), 19.5, L('Cnc', 10, 20), 5.0),
    ('A', 'IX.10.3', 'IX.9.4 emended', 49, L('Tau', 22, 34), 19.5, L('Cnc', 10, 20), 5.0),
    ('A', 'IX.10.3', 'XI.2.2', 55, L('Tau', 22, 34), 19.5, L('Cnc', 16, 11), 5.0),
    ('B', 'X.4.3', 'XI.6.2', 6, L('Sgr', 22, 9), 4.75, L('Sgr', 28, 41), 20.0),
    ('B', 'X.4.3', 'V.3.2', 55, L('Sgr', 22, 9), 4.75, L('Aqr', 16, 27), 6.75),
    ('D', 'IX.7.4', 'X.1.3', 35, L('Aqr', 9, 45), 19.0, L('Psc', 14, 15), 19.0),
    ('F', 'X.2.4', 'X.1.6', 37, L('Sco', 25, 30), 19.0, L('Cap', 2, 15), 19.0),
    ('G', 'X.3.2a', 'IX.7.5', 106, L('Aqr', 25, 30), 5.0, L('Gem', 10, 0), 5.0),
    ('H', 'IX.7.9', 'IX.7.11 as printed', 102, L('Aqr', 18, 10), 5.0, L('Ari', 29, 30), 19.0),
    ('H', 'IX.7.9', 'IX.7.11 emended', 72, L('Aqr', 18, 10), 5.0, L('Ari', 29, 30), 19.0),
    ('H', 'IX.7.9', 'IX.7.14', 192, L('Aqr', 18, 10), 5.0, L('Leo', 27, 50), 19.0),
    ('J', 'X.9.2', 'X.4.6a', 267, L('Cap', 23, 54), 5.0, L('Lib', 17, 3), 5.0),
    ('J', 'X.9.2', 'X.4.6b', 271, L('Cap', 23, 54), 5.0, L('Lib', 20, 59), 5.0),
    ('K', 'IX.7.16', 'XI.3.2', 1385, L('Sco', 24, 50), 5.0, L('Vir', 9, 56), 5.0),
    ('K', 'IX.7.16', 'IX.7.15', 2902, L('Sco', 24, 50), 5.0, L('Sco', 5, 10), 5.0),
    ('L', 'X.1.5', 'X.2.3', 586, L('Lib', 17, 52), 5.0, L('Tau', 25, 24), 5.0),
    ('L', 'X.1.5', 'IX.9.3', 996, L('Lib', 17, 52), 5.0, L('Cnc', 10, 5), 19.0),
]
print(f"{'set':3} {'from':8} {'to':20} {'file':>6} {'elapsed_d(file)':>15} {'meanSun_d':>10} {'resid_d':>8}")
for s, a, b, off, l0, h0, l1, h1 in cases:
    elapsed = off + (h1 - h0) / 24          # days implied by the file's offset
    base = elapsed * v                      # mean-Sun motion expected
    dl = (l1 - l0 - base + 180) % 360 - 180 # residual in degrees
    implied = elapsed + dl / v
    print(f"{s:3} {a:8} {b:20} {off:6d} {elapsed:15.2f} {implied:10.2f} {implied-elapsed:8.2f}")
