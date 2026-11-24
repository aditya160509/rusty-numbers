"""Does the pair (d(n),d(n+1)) determine block d(qn+c .. qn+c+q) (length q+1)? Try shifts c."""
import numpy as np,sys
D=int(sys.argv[1]); q=D+1; f=np.memmap(f'd_1_{D}.bin',dtype=np.int8,mode='r')
N=(len(f)-3*q)//q; x=np.asarray(f[:N*q+3*q]).astype(np.int64)
best=None
for c in (0,1,2):
    m={}; bad=0
    for n in range(N):
        k=(int(x[n]),int(x[n+1])); blk=tuple(int(v) for v in x[q*n+c:q*n+c+q+1])
        if m.setdefault(k,blk)!=blk: bad+=1
    print(f'd={D} shift {c}: pair-letters {len(m)} conflicts {bad}')
