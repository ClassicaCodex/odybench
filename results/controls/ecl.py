import re, glob, sys
sys.stdout.reconfigure(encoding='utf-8')
D='C:/Projects/odybench/results/controls/nasa/'
rows={'S':{}, 'L':{}}
for kind,pat in (('S','SEcat5_*.txt'),('L','LEcat5_*.txt')):
    for f in glob.glob(D+pat):
        for line in open(f,encoding='utf-8',errors='replace'):
            m=re.match(r'^(\d{5}) +(-?\d+) (\w{3}) (\d\d) +(\d\d:\d\d:\d\d) +(\d+) +(.*)$', line)
            if m:
                rows[kind][(int(m.group(2)),m.group(3),int(m.group(4)))]=line.rstrip()
def get(kind,y,mon,d):
    return rows[kind].get((y,mon,d),'NOT FOUND')
Q=[l.split() for l in sys.argv[1:]]
for q in sys.argv[1:]:
    k,y,mon,d=q.split(',')
    print(k,y,mon,d,'->',get(k,int(y),mon,int(d)))
