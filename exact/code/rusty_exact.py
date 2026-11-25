from collections import deque
from math import ceil

def direct(a,N):
 k=len(a); q=sum(a); K=k*q+1; used=set(); b=0; x=[]
 for n in range(1,N+1):
  block=[]
  for i in range(k):
   b+=1
   while b in used:b+=1
   block.append(b)
  A=sum(v*w for v,w in zip(a,block)); used.add(A); x.append(A-K*n)
 return x

def build(a):
 k=len(a);q=sum(a); L=k*q;K=L+1
 # C = ceil((k H+K)/(k-1)), H=K*sum(a_i*(k-i))/L
 J=sum(v*(k-i-1) for i,v in enumerate(a)); C=(k*K*J+K*L+(k-1)*L-1)//((k-1)*L)
 # u satisfies (z-C)/L-1 <= u < (z+C)/L, z=kr+i in [1,L]
 U=(C+L-1)//L
 R=1
 while (R+q-1)//q+U+1>R:R+=1
 P=R+U+2
 x=direct(a,q*P+R+1)
 def rule(w,r,shift):
  us=[]
  for i in range(1,k+1):
   z=k*r+i
   for u in range(-U,U+1):
    # rank t=p+shift+u; e_t=x[t-1]
    if L*u+w[R+shift+u-1]<z<=L*(u+1)+w[R+shift+u]:
     us.append(u);break
   else:raise AssertionError((a,r,shift,w))
  return sum(v*(i+1-k+u) for i,(v,u) in enumerate(zip(a,us)))-r-1
 # check formula: A = sum a_i*(L*p+kr+i+p+u) = q*K*p+q*kr+sum a_i(i+u); subtract K*(qp+r+1) -> sum a_i(i+u)-r-K
 # above formula sum a_i(i-k+u)-r-1 yes
 def key(n):return (0,n) if n<P else (1,tuple(x[n-R:n+R+1]))
 keys=[key(0)]; ids={keys[0]:0}; out=[]; tr=[]
 for typ,v in keys:
  out.append(x[v] if typ==0 else v[R]); row=[]
  for r in range(q):
   if typ==0: t=key(q*v+r)
   else:
    w=tuple(rule(v,(r+h)%q,(r+h)//q) for h in range(-R,R+1));t=(1,w)
   if t not in ids:ids[t]=len(keys);keys.append(t)
   row.append(ids[t])
  tr.append(row)
 part=out
 while True:
  m={};new=[m.setdefault((out[s],tuple(part[t] for t in tr[s])),len(m)) for s in range(len(keys))]
  if new==part:break
  part=new
 reps={}
 for s,p in enumerate(part):reps.setdefault(p,s)
 return [out[reps[p]] for p in range(len(reps))], [[part[t] for t in tr[reps[p]]] for p in range(len(reps))],len(keys)

def check(a,N=10000):
 o,t,raw=build(a);q=sum(a);states=[0]*N
 for n in range(1,N):states[n]=t[states[n//q]][n%q]
 assert [o[s] for s in states]==direct(a,N),a
 return len(o),raw
if __name__=='__main__':
 for d in range(1,101):
  m,raw=check((1,d));print(d,m,raw,flush=True)
