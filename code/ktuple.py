"""Minimal k such that (d(n..n+k-1)) determines d(qn+c .. qn+c+q+k-2) for some shift c in 0..k+1. Prints k, c, alphabet size."""
import numpy as np,sys
D=int(sys.argv[1]); q=D+1; f=np.memmap(sys.argv[2],dtype=np.int8,mode='r')
for k in range(1,7):
    N=(len(f)-(k+3)*q)//q; x=np.asarray(f[:N*q+(k+3)*q]).astype(np.int64)
    for c in range(0,k+2):
        m={}; bad=0
        for n in range(N):
            key=tuple(x[n:n+k].tolist()); blk=tuple(x[q*n+c:q*n+c+q+k-1].tolist())
            if m.setdefault(key,blk)!=blk: bad+=1; break
        if bad==0: print(f'd={D} k={k} shift={c} letters={len(m)} checked_n={N}'); sys.exit()
print(f'd={D} no k<=6')
