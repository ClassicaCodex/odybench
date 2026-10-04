# Dump the three prereg clue files in readable form (critique-design-r1, round 1 on revision 5).
# Reads only data/prereg/controls_real.json, controls_almagest.json, negatives.json (no truth file).
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = 'C:/Projects/odybench/data/prereg/'
which = sys.argv[1]
d = json.load(open(ROOT + which, encoding='utf-8'))

def show(obj, ind=0, maxlen=100000):
    print(json.dumps(obj, ensure_ascii=False, indent=1)[:maxlen])

if which == 'controls_almagest.json':
    for s in d['sets']:
        print('=' * 100)
        show({k: v for k, v in s.items() if k != 'clues'})
    print('#' * 100)
    for c in d['clues']:
        print('-' * 100)
        show(c)
elif which == 'controls_real.json':
    for k, v in d.items():
        if k != 'sets':
            print('==', k); show(v)
    for s in d['sets']:
        print('=' * 100)
        show({k: v for k, v in s.items() if k != 'clues'})
        for c in s.get('clues', []):
            print('-' * 100)
            show(c)
else:
    show(d)
