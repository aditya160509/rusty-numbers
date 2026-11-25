from itertools import product
from random import Random
from anti_exact_minimal import Anti
from rusty_exact import build,direct
from rusty_verify import supplied,equiv

def minimize_count(o,t):
    p=o
    while True:
        table={};new=[table.setdefault((o[i],tuple(p[j] for j in row)),len(table)) for i,row in enumerate(t)]
        if new==p:return len(set(p))
        p=new

def verify(a, compare_window=False, prefix=0):
    m=Anti(a);s=m.states();v=m.reachable()
    assert s==v,(a,s-v,v-s)
    assert len(s)==m.state_count()
    assert min(b for _,b in s)==-m.C and max(b for _,b in s)==m.H
    o,t=m.automaton();assert minimize_count(o,t)==len(o),a
    if compare_window:
        p,u,_=build(a);equiv(o,t,p,u)
    if prefix:
        x=direct(a,prefix);state=[0]*prefix
        for n in range(1,prefix):state[n]=t[state[n//m.q]][n%m.q]
        assert [o[s] for s in state]==x,a
    return m
if __name__=='__main__':
    for d in range(1,41):
        m=verify((1,d),compare_window=True,prefix=10000)
        if d<=15:equiv(*m.automaton(),*supplied(d))
        print('rusty',d,-m.C,m.H,m.state_count(),flush=True)
    for d in [50,60,100,150,200,300,500]:
        m=verify((1,d),prefix=10000);print('large rusty',d,-m.C,m.H,m.state_count(),flush=True)
    n=0
    for k,lim in [(2,25),(3,8),(4,4),(5,3)]:
        for a in product(range(1,lim+1),repeat=k):
            verify(a,compare_window=(max(a)<=3),prefix=1000);n+=1
        print('exhaustive',k,lim,'cumulative',n,flush=True)
    rng=Random(1234)
    for _ in range(100):
        k=rng.randrange(2,9);a=tuple(rng.randrange(1,26) for _ in range(k));verify(a,prefix=1000)
    print('random',100,'passed',flush=True)
