"""Print every passage in Almagest books given on argv (default 9,10,11) that
contains a year word, with ~context. Read-only on data/text."""
import sys, re, unicodedata
sys.stdout.reconfigure(encoding='utf-8')
books = sys.argv[1].split(',') if len(sys.argv) > 1 else ['9', '10', '11']
pre = 'urn:cts:greekLit:tlg0363.tlg001.1st1K-grc1.'
def strip(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').lower()
pat = re.compile(r'ετει|ετους|ετη ')
for line in open('data/text/ptolemy-syntaxis-grc.tsv', encoding='utf-8'):
    ref, _, txt = line.rstrip('\n').partition('\t')
    r = ref.replace(pre, '')
    if r.split('.')[0] not in books or '.toc' in r:
        continue
    s = strip(txt)
    hits = [m.start() for m in pat.finditer(s)]
    if hits:
        print(f'== {r} ({len(hits)} hits)')
        last = -1
        for h in hits:
            if h < last:
                continue
            a, b = max(0, h - 60), min(len(txt), h + 330)
            print('   ...' + txt[a:b].replace('\n', ' ') + '...')
            last = b
