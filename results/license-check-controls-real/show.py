import sys,json
txt=open(sys.argv[1],encoding='utf-8').read()
lines=[l for l in txt.split('\n') if not l.startswith('   CHECK exact')]
rows=[l for l in lines if l.startswith('   ROW ')]
txt='\n'.join(l for l in lines if not l.startswith('   ROW '))
blocks=txt.split('='*100)
print(blocks[0])
for b in blocks[1:]:
    b=b.strip()
    try:
        c=json.loads(b)
    except Exception as e:
        print('RAW',b[:3000]); continue
    print('-----',c['clue_id'],'|',c['kind'],'|',c.get('feature'),'| event',c.get('event'))
    print('STATEMENT:',c['statement'])
    print('LW:',c['licence_words'],'REF:',[r.split('.',3)[-1] if r.startswith('urn') else r for r in c['ref']], 'TF:', sorted(set(c['text_file'])) if isinstance(c['text_file'],list) else c['text_file'])
    for fo in c['fork_options']:
        print('  FORK',fo['option'],'P' if fo.get('primary') else '-','|',fo['reading'],'|',fo['justification'],'|',json.dumps(fo['operational'],ensure_ascii=False), '|', json.dumps({k:v for k,v in fo.items() if k not in ('option','reading','justification','operational','primary')},ensure_ascii=False))
    print('LEVEL:',c['narrative_level']); print('NOTES:',c['notes'])
    extra={k:v for k,v in c.items() if k not in ('set','clue_id','kind','feature','event','statement','licence_words','ref','text_file','fork_options','narrative_level','notes')}
    if extra: print('EXTRA:',json.dumps(extra,ensure_ascii=False))
if len(sys.argv)>2:
    seen=set()
    for r in rows:
        if r not in seen:
            seen.add(r); print(r)
