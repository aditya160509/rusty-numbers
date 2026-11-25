from itertools import product
from rusty_exact import check
n=0
for k,lim in [(2,6),(3,4),(4,3),(5,2)]:
    count=0
    for a in product(range(lim+1),repeat=k):
        if 0 not in a or sum((i+1)*v for i,v in enumerate(a))<=k:continue
        check(a,3000);n+=1;count+=1
    print('k',k,'max coefficient',lim,'admissible nonnegative zero-containing forms tested',count,flush=True)
print('total',n,flush=True)
for a in [(0,2),(3,0),(0,0,2),(0,3,0),(4,0,0),(0,0,0,2),(0,1,0,1),(0,0,0,0,2)]:print(a,check(a,100000),flush=True)
