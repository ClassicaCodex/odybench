"""List every passage naming a Roman-era or Ptolemaic ruler/era in the Syntaxis (all books)."""
import sys, re, unicodedata
sys.stdout.reconfigure(encoding='utf-8')
pre = 'urn:cts:greekLit:tlg0363.tlg001.1st1K-grc1.'
def strip(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').lower()
pat = re.compile(r'αδριαν|αδρια |αντωνιν|τραιαν|δομετιαν|αυγουστ|φιλαδελφ|φιλομητορ|ευεργετ|κατα διονυσ|χαλδαι|καλιππ|αλεξανδρου τελευτ')
for line in open('data/text/ptolemy-syntaxis-grc.tsv', encoding='utf-8'):
    ref, _, txt = line.rstrip('\n').partition('\t')
    r = ref.replace(pre, '')
    if '.toc' in r: continue
    s = strip(txt)
    for m in pat.finditer(s):
        a = max(0, m.start() - 40); b = min(len(txt), m.start() + 110)
        print(f'{r:10s} {txt[a:b]}')
