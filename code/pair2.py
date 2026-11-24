"""Check: pair (d(n),d(n+1)) determines d(qn+2..qn+q+2) for all n<N. Prints letters, pairs, conflicts, value range."""
import numpy as np,sys
D=int(sys.argv[1]); q=D+1; f=np.memmap(sys.argv[2],dtype=np.int8,mode='r')
N=(len(f)-3*q)//q; x=np.asarray(f[:N*q+3*q]).astype(np.int64)
m={}; bad=0
for n in range(N):
    k=(int(x[n]),int(x[n+1])); blk=tuple(x[q*n+2:q*n+q+3].tolist())
    if m.setdefault(k,blk)!=blk: bad+=1
print(f'd={D} kappa={2*q+1} range=[{int(x.min())},{int(x.max())}] values={len(set(x.tolist()))} pairs={len(m)} conflicts={bad} checked_n={N}')
