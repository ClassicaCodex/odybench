# One line per row of controls_real.json: kind, feature, primary option with its operational values,
# the alternatives, and the licence check's verdict (no truth file read).
# Output: real_rows.txt
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
d = json.load(open('C:/Projects/odybench/data/prereg/controls_real.json', encoding='utf-8'))
for s in d['sets']:
    print('=====', s['set_id'], '| role:', s.get('role'), '| window', s.get('window_years'), '| anchor', s.get('anchor_event'))
    for op in s.get('observer_place', []):
        print('   PLACE', op.get('events'), op.get('place'), '|', op.get('search_coordinates'))
    for c in s.get('clues', []):
        prim = [(o['option'], json.dumps(o.get('operational', {}), ensure_ascii=False)[:150])
                for o in c['fork_options'] if o.get('primary')]
        others = [o['option'] for o in c['fork_options'] if not o.get('primary')]
        print('  ', c['clue_id'], '|', c.get('kind'), '|', c.get('feature'), '| PRIM', prim, '| ALT', others,
              '| narrative:', (c.get('narrative_level') or '')[:70], '| LC:', (c.get('license_check') or '')[:60])
