import itertools
def ok(a,N=3000):
    k=len(a); used=set(); cur=1; prevA=0; lo=hi=0; q=sum(a); K=k*q+1
    for n in range(1,N+1):
        B=[]
        while len(B)<k:
            while cur in used: cur+=1
            B.append(cur); used.add(cur); cur+=1
        x=sum(c*b for c,b in zip(a,B))
        if x<=B[-1] or x<=prevA or x in used: return False,None
        used.add(x); prevA=x; e=x-K*n; lo=min(lo,e); hi=max(hi,e)
    return True,(lo,hi)
bad=0;n=0
for k in (2,3,4):
  for a in itertools.product(range(0,5),repeat=k):
    if 0 not in a or sum(a)==0: continue
    A1=sum((i+1)*c for i,c in enumerate(a)); v,r=ok(a); n+=1
    if v!=(A1>k): bad+=1; print(a,A1,v)
print(n,"zero vectors, mismatches",bad)
