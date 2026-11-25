import itertools, random, sys
def greedy(a, N):
    k=len(a); used=set(); A=[]; m=1
    for n in range(N):
        B=[]
        while len(B)<k:
            if m not in used: B.append(m)
            m+=1
        # B taken in order; mex pointer: need unused smallest; A values may be skipped later
        x=sum(c*b for c,b in zip(a,B)); A.append(x); used.add(x)
    return A
def greedy2(a,N):  # correct mex with set
    k=len(a); used=set(); A=[]; cur=1
    for n in range(N):
        B=[]
        while len(B)<k:
            while cur in used: cur+=1
            B.append(cur); used.add(cur); cur+=1
        x=sum(c*b for c,b in zip(a,B)); A.append(x); used.add(x)
    return A
def formula(a):
    k=len(a); q=sum(a); L=k*q; K=L+1; A1=sum((i+1)*c for i,c in enumerate(a)); T=K-A1
    C=((k*k-k)*T+k*k*(q-1)-1)//(k*k-1); H=C//k-T
    P=[0]; 
    for c in a: P.append(P[-1]+c)
    S=C+H+1+max(H,0)+sum(max((C-t)//k-T-(P[k-t]-1),0) for t in range(1,k))
    return C,H,S,q,K,T,P,L
def minstates(a, e):  # e: list e[p]=e_{p+1} for p>=0; build kernel-free check via Myhill: use my own DFA from brute data
    pass
def dfa(a):
    C,H,S,q,K,T,P,L=formula(a); k=len(a)
    def F(r,x,y):
        v=-T-r
        for i in range(1,k+1):
            z=k*r+i; v+=a[i-1]*(-(z<=x)+(z>L+y))
        return v
    def d(st,r):
        x,y=st
        return (0,F(0,x,y)) if r==0 else (max(0,F(r-1,x,y)),F(r,x,y))
    start=(0,-T); seen={start}; st=[start]; tr={}
    while st:
        s=st.pop()
        for r in range(q):
            t=d(s,r); tr[s,r]=t
            if t not in seen: seen.add(t); st.append(t)
    # Moore minimization
    part={s:s[1] for s in seen}
    while True:
        sig={s:(part[s],)+tuple(part[tr[s,r]] for r in range(q)) for s in seen}
        ids={}; new={s:ids.setdefault(sig[s],len(ids)) for s in seen}
        if len(ids)==len(set(part.values())): break
        part=new
    return start,tr,q,len(set(part.values()))
def run(a,N):
    C,H,S,q,K,T,P,L=formula(a)
    A=greedy2(a,N); e=[A[n]-K*(n+1) for n in range(N)]
    start,tr,q,ms=dfa(a)
    bad=0
    for p in range(N):
        s=start
        ds=[] ; x=p
        while x: ds.append(x%q); x//=q
        for r in reversed(ds): s=tr[s,r]
        if s[1]!=e[p]: bad+=1
    return (min(e)==-C, max(e)==H, set(e)==set(range(-C,H+1)), ms==S, bad)
random.seed(1); fails=0; cnt=0
forms=[(1,d) for d in range(1,31)]+[tuple(v) for k in (2,3) for v in itertools.product(range(1,5),repeat=k)]+[tuple(random.randint(1,6) for _ in range(random.randint(2,5))) for _ in range(60)]
for a in forms:
    r=run(a,int(sys.argv[1]))
    cnt+=1
    if not all(r[:4]) or r[4]: fails+=1; print("FAIL",a,r)
print("forms",cnt,"fails",fails)
