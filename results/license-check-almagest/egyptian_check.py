"""Independent recomputation of every interval row of controls_almagest.json
from the Egyptian dates as they stand in data/text/ptolemy-syntaxis-grc.tsv.
Computed by me (license-check-almagest task); no truth file was read.

Egyptian civil year: 12 x 30 days + 5 epagomenal days = 365 days.
Civil-day convention (the clue file's): a record dated 'D into D+1' falls on
civil day D if made in the evening, D+1 if made before dawn / in the morning.
Era links used, all stated in the Almagest itself:
  Antoninus 2 = Nabonassar 886                      (9.10.3)
  Antoninus 3 = year 463 from Alexander's death     (3.1.9)
  Nabonassar -> Alexander's death = 424 years       (3.7.4; also 10.9.2: 52 = 476)
  Philadelphus 13 = Nabonassar 476                  (10.4.6)
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
M = {m: i for i, m in enumerate(
    'Thoth Phaophi Athyr Choiak Tybi Mechir Phamenoth Pharmouthi Pachon Payni Epiphi Mesore'.split())}

def day(nab_year, month, d):
    """absolute civil-day number in the Nabonassar era (day 0 = Thoth 1, year 1)"""
    return (nab_year - 1) * 365 + M[month] * 30 + (d - 1)

ANT = lambda y: 884 + y          # Antoninus 2 = Nab 886
ALEX = lambda y: 424 + y         # year n from Alexander's death = Nab 424 + n
HAD = lambda y: 1000 + y         # Hadrian: only within-reign differences are used

# record: (era year as Nabonassar-like key, month, civil day, source words summary)
R = {
    'IX.10.3': (ANT(2), 'Epiphi', 2, 'Epiphi 2 into 3, evening (4 1/2 h before midnight)'),
    'X.8.2':   (ANT(2), 'Epiphi', 15, 'Epiphi 15 into 16, 3 h before midnight'),
    'IX.9.4':  (ANT(2), 'Mesore', 24, 'Mesore [..] into 24, dawn (as printed)'),
    'XI.2.2':  (ANT(2), 'Mesore', 27, 'Mesore 26 into 27, before sunrise'),
    'X.4.3':   (ANT(2), 'Tybi', 30, 'Tybi 29 into 30, 4 3/4 h after midnight'),
    'XI.6.2':  (ANT(2), 'Mechir', 6, 'Mechir 6 into 7, 4 h before midnight'),
    'V.3.2':   (ANT(2), 'Phamenoth', 25, 'Phamenoth 25, after sunrise'),
    'VII.2.4': (ANT(2), 'Pharmouthi', 9, 'Pharmouthi 9, sunset'),
    'IX.8.3':  (HAD(19), 'Athyr', 15, 'Athyr 14 into 15, morning star'),
    'IV.6.14': (HAD(19), 'Choiak', 2, 'Choiak 2 into 3, mid-eclipse 1 h before midnight'),
    'IX.7.4':  (HAD(16), 'Phamenoth', 16, 'Phamenoth 16 into 17, evening'),
    'X.1.3':   (HAD(16), 'Pharmouthi', 21, 'Pharmouthi 21 into 22, evening star'),
    'X.3.2b':  (ALEX(463), 'Pharmouthi', 4, 'Antoninus 3 Pharmouthi 4 into 5, evening'),
    'III.1.10': (ALEX(463), 'Pachon', 7, 'year 463 from Alexander, Pachon 7, 1 h after noon'),
    'X.2.4':   (HAD(21), 'Tybi', 2, 'Tybi 2 into 3, evening'),
    'X.1.6':   (HAD(21), 'Mechir', 9, 'Mechir 9 into 10, evening'),
    'X.3.2a':  (HAD(18), 'Pharmouthi', 3, 'Pharmouthi 2 into 3, morning star'),
    'IX.7.5':  (HAD(18), 'Epiphi', 19, 'Epiphi 18 into 19, dawn'),
    'IX.7.9':  (486, 'Choiak', 18, 'Nab 486 Choiak 17 into 18, dawn'),
    'IX.7.11': (486, 'Phamenoth', 30, 'Nab 486 Phamenoth 30 into 1, evening (as printed)'),
    'IX.7.14': (486, 'Payni', 30, 'Nab 486 Payni 30, evening'),
    'X.9.2':   (476, 'Athyr', 21, 'Nab 476 Athyr 20 into 21, dawn'),
    'X.4.6a':  (476, 'Mesore', 18, 'Philadelphus 13 (= Nab 476) Mesore 17 into 18, 12th hour'),
    'X.4.6b':  (476, 'Mesore', 22, 'Mesore 21 into 22 (and: four days later, in words)'),
    'IX.7.16': (504, 'Thoth', 28, 'Nab 504 Thoth 27 into 28, dawn'),
    'XI.3.2':  (ALEX(83), 'Epiphi', 18, 'year 83 from Alexander, Epiphi 17 into 18, dawn'),
    'IX.7.15': (512, 'Thoth', 10, 'Nab 512 Thoth 9 into 10, dawn'),
    'X.1.5':   (HAD(12), 'Athyr', 22, 'Athyr 21 into 22, morning star'),
    'X.2.3':   (HAD(13), 'Epiphi', 3, 'Epiphi 2 into 3, morning star'),
    'IX.9.3':  (HAD(14), 'Mesore', 18, 'Mesore 18, evening'),
}
# (clue_id, anchor, record, day_offset in the file)
rows = [
    ('ALM-A.3', 'IX.10.3', 'X.8.2', 13), ('ALM-A.6', 'IX.10.3', 'IX.9.4', 52),
    ('ALM-A.8', 'IX.10.3', 'XI.2.2', 55), ('ALM-B.4', 'X.4.3', 'XI.6.2', 6),
    ('ALM-B.6', 'X.4.3', 'V.3.2', 55), ('ALM-B.8', 'X.4.3', 'VII.2.4', 69),
    ('ALM-C.2', 'IX.8.3', 'IV.6.14', 17), ('ALM-D.2', 'IX.7.4', 'X.1.3', 35),
    ('ALM-E.2', 'X.3.2b', 'III.1.10', 33), ('ALM-F.2', 'X.2.4', 'X.1.6', 37),
    ('ALM-G.2', 'X.3.2a', 'IX.7.5', 106), ('ALM-H.3', 'IX.7.9', 'IX.7.11', 102),
    ('ALM-H.7', 'IX.7.9', 'IX.7.14', 192), ('ALM-J.3', 'X.9.2', 'X.4.6a', 267),
    ('ALM-J.6', 'X.9.2', 'X.4.6b', 271), ('ALM-K.3', 'IX.7.16', 'XI.3.2', 1385),
    ('ALM-K.6', 'IX.7.16', 'IX.7.15', 2902), ('ALM-L.3', 'X.1.5', 'X.2.3', 586),
    ('ALM-L.5', 'X.1.5', 'IX.9.3', 996),
]
bad = 0
for cid, a, b, off in rows:
    got = day(*R[b][:3]) - day(*R[a][:3])
    flag = 'OK' if got == off else 'MISMATCH'
    bad += got != off
    print(f'{cid:8} {a:8} -> {b:9} file {off:5d}  recomputed {got:5d}  {flag}')
print('mismatches:', bad)
print('ALM-I.4: stated in words, "μετὰ δ ἡμέρας" (9.10.6) -> +4; file 4')
