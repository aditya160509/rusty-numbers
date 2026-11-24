"""Infer msd-base-q DFAO for d(n). State for prefix value p: the function (e,j)->d(p*q^e+j), j<q^e.
Two prefixes are merged if these agree on all indices < N up to depth E. Validates on all N terms after."""
import numpy as np,sys,json
d=np.memmap(sys.argv[1],dtype=np.int8,mode='r'); q=int(sys.argv[2]); E=int(sys.argv[3]); N=len(d)
def sig(p):
    parts=[]
    for e in range(E+1):
        lo=p*q**e; hi=min(lo+q**e,N)
        if lo>=N: break
        parts.append(d[lo:hi])
    return np.concatenate(parts)
reps=[0]; sigs=[sig(0)]; trans=[]; i=0
while i<len(reps):
    row=[]
    for j in range(q):
        c=reps[i]*q+j; s=sig(c); hit=None
        for k,t in enumerate(sigs):
            L=min(len(s),len(t))
            if L>=q**(E-1) and np.array_equal(s[:L],t[:L]): hit=k;break
        if hit is None:
            if len(s)<q**(E-1): sys.exit(f'undetermined: prefix {c} sig len {len(s)}; states {len(reps)}')
            reps.append(c); sigs.append(s); hit=len(reps)-1
        row.append(hit)
    trans.append(row); i+=1
out=[int(d[p]) for p in reps]
print('states',len(reps),'largest rep',max(reps))
# validate on all N terms, streamed in 1M-term chunks to keep memory low
T=np.array(trans,dtype=np.int32); O=np.array(out,dtype=np.int8); ok=True; C=1<<20
for a in range(0,N,C):
    x=np.arange(a,min(a+C,N),dtype=np.int64); digs=[]
    while x.any(): digs.append((x%q).astype(np.int32)); x//=q
    s=np.zeros(len(digs[0]) if digs else 1,dtype=np.int32)
    for dg in reversed(digs): s=T[s,dg]
    if not (O[s]==np.asarray(d[a:a+len(s)])).all(): ok=False; break
print('validated on all',N,'terms:',ok)
json.dump({'q':q,'trans':trans,'out':out,'reps':reps},open(sys.argv[4],'w'))
