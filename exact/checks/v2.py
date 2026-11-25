import sys,itertools,random
sys.argv=['x','0']
exec(open('v.py').read().split('random.seed(1)')[0])
random.seed(2); bad=0; n=0
forms=[(1,d) for d in range(1,60)]+[tuple(v) for k in (2,3,4) for v in itertools.product(range(1,6),repeat=k)]+[tuple(random.randint(1,9) for _ in range(random.randint(2,6))) for _ in range(300)]
for a in forms:
    C,H,S,*_=formula(a); start,tr,q,ms=dfa(a)
    outs={s[1] for (s,r) in tr}|{start[1]}
    n+=1
    if outs!=set(range(-C,H+1)) or ms!=S: bad+=1; print(a,C,H,S,min(outs),max(outs),ms)
print(n,"forms, bad",bad)
