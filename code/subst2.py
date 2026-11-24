"""For a=(1,d): build map v=d(n) -> block (d(q n+1+j))_{j<q}, d(n)=A_{n+1}-K(n+1). Report letters/conflicts; dump json."""
import numpy as np,sys,json
D=int(sys.argv[1]); q=D+1; f=np.memmap(f'd_1_{D}.bin',dtype=np.int8,mode='r')
N=(len(f)-2*q)//q; x=np.asarray(f[:N*q+2*q]).astype(np.int64)
m={}; bad=0; first={}
for n in range(0,N):
    blk=tuple(int(v) for v in x[q*n+1:q*n+1+q]); k=int(x[n])
    if k not in m: m[k]=blk; first[k]=n
    elif m[k]!=blk: bad+=1
print(f'd={D} q={q} N={N} letters={sorted(m)} conflicts={bad}')
json.dump({'d':D,'start':[int(v) for v in x[:1]],'map':{str(k):v for k,v in m.items()},'first':first},open(f'subst_{D}.json','w'))
