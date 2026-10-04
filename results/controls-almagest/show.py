"""Print given Almagest sections in full: py show.py 9.7.4 9.7.5 ..."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
pre = 'urn:cts:greekLit:tlg0363.tlg001.1st1K-grc1.'
want = sys.argv[1:]
rows = {}
for line in open('data/text/ptolemy-syntaxis-grc.tsv', encoding='utf-8'):
    ref, _, txt = line.rstrip('\n').partition('\t')
    rows[ref.replace(pre, '')] = txt
for w in want:
    if w.endswith('*'):
        ks = [k for k in rows if k.startswith(w[:-1])]
    else:
        ks = [w]
    for k in ks:
        print(f'== {k}\n{rows.get(k, "<missing>")}\n')
