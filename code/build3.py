"""Automaton from k-block substitution: d(n..n+k-1) -> d(qn+c .. qn+c+q+k-2).
State for P>=T: window d(P-L..P+R); child windows computed via the block map (closure checked)."""
import numpy as np,sys
D,k,c,T=map(int,sys.argv[1:5]);q=D+1
x=np.fromfile(f'd{D}.bin',dtype=np.int8);N=len(x)
# learn block map
bm={};NN=(N-(k+3)*q)//q
for a0 in range(0,NN,1<<21):
    ns=np.arange(a0,min(a0+(1<<21),NN))
    keys=np.stack([x[ns+i] for i in range(k)],1).astype(np.int16)
    blk=np.stack([x[q*ns+c+j] for j in range(q+k-1)],1).astype(np.int16)
    for row in np.unique(np.concatenate([keys,blk],1),axis=0):
        kk=tuple(int(v) for v in row[:k]);b=tuple(int(v) for v in row[k:])
        if bm.setdefault(kk,b)!=b: sys.exit('block map conflict')
print('block-map letters',len(bm))
def val(win,P,i):  # d(i) given window dict over indices of parent level
    n=(i-c)//q; j=i-c-q*n; kk=tuple(win[n+t] for t in range(k))
    if kk not in bm: raise KeyError(kk)
    return bm[kk][j]
L=1;R=k  # parent indices needed: n in [P-1, P+1+k-1]
def child(w,r):
    P=10**6  # any large P; positions relative
    win={P-L+i:w[i] for i in range(len(w))}
    m=q*P+r
    return tuple(val(win,P,i) for i in range(m-L,m+R+1))
states={};order=[];outv=[];tr=[]
def sid(key,o):
    if key not in states: states[key]=len(order);order.append(key);outv.append(o);tr.append(None)
    return states[key]
sid(('p',0),int(x[0]));i=0
while i<len(order):
    key=order[i];row=[]
    for r in range(q):
        if key[0]=='p':
            n=key[1]*q+r
            nk=('p',n) if n<T else ('w',tuple(int(v) for v in x[n-L:n+R+1]))
            o=int(x[n])
        else:
            try: cw=child(key[1],r)
            except KeyError as e: sys.exit(f'closure failure: unknown key {e}')
            nk=('w',cw);o=cw[L]
        row.append(sid(nk,o))
    tr[i]=row;i+=1
part=list(outv)
while True:
    sig=[(part[s],tuple(part[t] for t in tr[s])) for s in range(len(order))]
    m={};new=[m.setdefault(g,len(m)) for g in sig]
    if len(set(new))==len(set(part)):break
    part=new
ids={part[0]:0}
for s in range(len(order)): ids.setdefault(part[s],len(ids))
rep={}
for s in range(len(order)): rep.setdefault(ids[part[s]],s)
nm=len(ids);T2=[[ids[part[t]] for t in tr[rep[j]]] for j in range(nm)];O2=[outv[rep[j]] for j in range(nm)]
Tm=np.array(T2);Om=np.array(O2);bad=0
for a0 in range(0,N,1<<21):
    n=np.arange(a0,min(a0+(1<<21),N));digs=[]
    while n.any(): digs.append(n%q);n=n//q
    s=np.zeros(len(digs[0]),dtype=np.int64)
    for dg in reversed(digs): s=Tm[s,dg]
    bad+=int((Om[s]!=x[a0:a0+len(s)].astype(np.int64)).sum())
off=-min(O2)
print(f'd={D} raw={len(order)} min={nm} leading0={T2[0][0]==0} mismatches={bad}/{N} offset={off}')
s=f'msd_{q}\n\n'
for j in range(nm): s+=f'{j} {O2[j]+off}\n'+''.join(f'{r} -> {t}\n' for r,t in enumerate(T2[j]))+'\n'
open(f'RUSTY{D}.dfa','w').write(s)
