"""Design revision 5 scratch: scan DESIGN.md above the Appendix T marker for
control accepted dates and per-set truth-side facts. Prints each hit with its
line, for a human to judge. Run: py results/design-revision-v5/scan_truthside.py"""
import re
s = open('DESIGN.md', encoding='utf-8').read()
main = s[:s.index('<!-- APPENDIX-T')]
lines = main.split('\n')
pats = [r'355\.3', r'6\.63', r'424 ?BC', r'431 ?BC', r'413 ?BC', r'394 ?BC', r'[−-]309\b', r'[−-]187\b',
        r'168 ?BC', r'310 ?BC', r'331 ?BC', r'188 ?BC', r'21 Jun', r'Gautschy', r'IX\.7\.5\b', r'5\.5 d', r'20\.6',
        r'AD 1[2-4]\d', r'2[4-7]\d BC', r'[−-]2[2-7]\d\b', r'\+1[2-4]\d\b', r'[−-]72[01]\b', r'721 BC',
        r'[−-]856', r'\+27[27]', r'[−-]407', r'0\.64 h', r'E2 about', r'ALM-G fails', r'ALM-H fails',
        r'15 Aug', r'Aug 15', r'26 Jun', r'0412', r'3 Aug', r'21 Mar 424', r'Pydna[^|]{0,60}solstice']
for i, l in enumerate(lines, 1):
    for p in pats:
        if re.search(p, l):
            print(f'l.{i} [{p}] {l.strip()[:170]}')
