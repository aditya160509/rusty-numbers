"""Implements the proof for a positive linear form a (k>=2):
 (1) integer bounds -L <= e_n <= U from the contraction inequality,
 (2) the local rule e_{tau*m+r} = F_r(e_{m+t}: -T0<t<T1), valid for m>=T0,
 (3) a DFAO built from F_r (plus a finite exact prefix), minimized.
Usage: proof.py N a1 a2 ... [--cmp RUSTYfile offset]"""
import sys,math,numpy as np,subprocess,os
from fractions import Fraction as Fr
args=sys.argv[1:]; cmp=None
if '--cmp' in args: i=args.index('--cmp'); cmp=(args[i+1],int(args[i+2])); args=args[:i]
N=int(args[0]); a=[int(x) for x in args[1:]]; k=len(a); tau=sum(a); K=k*tau+1
assert k>=2 and min(a)>=1
sia=sum((i+1)*a[i] for i in range(k)); c0=Fr(K*(sia-k*tau),k*tau)
# ---- (1) smallest integer pair (L,U) closed under the induction step
def step_ok(L,U):
    hi=c0+Fr(L-1,k); lo=c0-Fr(U+K,k)
    return math.floor(hi)<=U and math.ceil(lo)>=-L and U>=-L
best=None
for L in range(0,4*K+5):
    for U in range(-L,4*K+5):
        if step_ok(L,U): best=(L,U); break
    if best: break
L,U=best
# a-priori condition used in proof: B_{kn} <= (k+1)n-1 < kappa*n - ... need x-U-1 < kappa*n for x<=B_{kn}, all n>=1
apriori = all((k+1)*n-1-U-1 < K*n for n in range(1,10))  # linear in n, slope K-(k+1)>0, so n=1 is the binding case
# ---- E range for B_M - M*K/(K-1): [-(U+K)/(k tau), (L-1)/(k tau)]
Elo=Fr(-(U+K),k*tau); Ehi=Fr(L-1,k*tau)
ys=[Fr(K*(k*(r-1)+i),k*tau) for r in range(tau) for i in range(1,k+1)]
Ylo=math.floor(min(ys)+Elo); Yhi=math.ceil(max(ys)+Ehi)
T0=next(t for t in range(1,999) if -K*t+U<Ylo)
T1=next(t for t in range(1,999) if K*t-L>=Yhi)
print(f'a={a} k={k} tau={tau} kappa={K} c0={float(c0):.3f}  BOUND e in [{-L},{U}] apriori={apriori}  y in [{Ylo},{Yhi}] T0={T0} T1={T1}')
def F(r,win):  # win: dict t->e_{m+t}, t in (-T0,T1)
    P=sorted(K*t+e for t,e in win.items()); Ps=set(P); ys=[]
    for i in range(1,k+1):
        v=k*(r-1)+i-T0; sol=[y for y in range(Ylo,Yhi+1) if y not in Ps and y-sum(p<y for p in P)==v]
        if len(sol)!=1: raise ValueError(f'no unique y r={r} i={i} sols={sol}')
        ys.append(sol[0])
    return sum(a[i]*ys[i] for i in range(k))-K*r
# ---- data
fn='data_'+'_'.join(map(str,a))+'.bin'
if not os.path.exists(fn) or os.path.getsize(fn)<2*N: subprocess.run(['./gena',str(N),fn]+[str(x) for x in a],check=True)
e=np.fromfile(fn,dtype=np.int16)[:N].astype(np.int64); E=lambda n:int(e[n-1])   # e_n, n>=1
print(f'  data n<={N}: observed range [{e.min()},{e.max()}]  within bound: {e.min()>=-L and e.max()<=U}')
# ---- (2) check local rule against data, all n=tau*m+r with m>=T0 and window inside data
bad=0;cnt=0;mmax=(N-T1)//1
for m in range(T0, min((N-tau)//tau, N-T1)):
    win={t:E(m+t) for t in range(-T0+1,T1)}
    for r in range(tau):
        n=tau*m+r
        if n>N: break
        cnt+=1
        if F(r,win)!=E(n): bad+=1
    if m>T0+200000//tau: break
print(f'  local rule F_r checked on {cnt} terms: mismatches {bad}')
# ---- (3) DFAO for f(p)=e_{p+1} from F only
amar=math.ceil(tau*(T0+1)/(tau-1))+1; bmar=math.ceil(tau*(T1+1)/(tau-1))+1
P0=next(p for p in range(1,10**6) if (tau*(p+1)+1-tau-amar)//tau - T0 >= 1 and p+1-amar>=1)
def child(win,c,Nc):  # win: tuple e_{Nc+i}, i in [-amar,bmar]
    d={Nc+i-amar:win[i] for i in range(len(win))}
    Np=tau*(Nc-1)+c+1; out=[]
    for i in range(-amar,bmar+1):
        I=Np+i; mm,rr=divmod(I,tau); out.append(F(rr,{t:d[mm+t] for t in range(-T0+1,T1)}))
    return tuple(out)
states={};order=[];outv=[];tr=[]
def sid(key,o):
    if key not in states: states[key]=len(order);order.append(key);outv.append(o);tr.append(None)
    return states[key]
sid(('p',0),E(1));i=0
while i<len(order):
    key=order[i];row=[]
    for c in range(tau):
        if key[0]=='p':
            p=key[1]*tau+c
            nk=('p',p) if p<P0 else ('w',tuple(E(p+1+j) for j in range(-amar,bmar+1)))
            row.append(sid(nk,E(p+1)))
        else:
            cw=child(key[1],c,1000*tau)   # position-free: only relative offsets matter
            row.append(sid(('w',cw),cw[amar]))
    tr[i]=row;i+=1
part=list(outv)
while True:
    sig=[(part[s],tuple(part[t] for t in tr[s])) for s in range(len(order))]
    mp={};new=[mp.setdefault(g,len(mp)) for g in sig]
    if len(set(new))==len(set(part)):break
    part=new
ids={part[0]:0}
for s in range(len(order)): ids.setdefault(part[s],len(ids))
rep={}
for s in range(len(order)): rep.setdefault(ids[part[s]],s)
nm=len(ids);T2=[[ids[part[t]] for t in tr[rep[j]]] for j in range(nm)];O2=[outv[rep[j]] for j in range(nm)]
print(f'  DFAO from F: raw states {len(order)} (P0={P0}, window {amar}+{bmar}+1), minimal {nm}')
# validate DFAO against data
Tm=np.array(T2);Om=np.array(O2);ok=True
p=np.arange(0,N);digs=[];x=p.copy()
while x.any(): digs.append(x%tau);x//=tau
s=np.zeros(N,dtype=np.int64)
for dg in reversed(digs): s=Tm[s,dg]
print(f'  DFAO vs data (p<{N}): mismatches {int((Om[s]!=e[:N]).sum())}')
if cmp:
    L2=open(cmp[0]).read().split('\n');q2=int(L2[0].split('_')[1]);o2={};t2={};cur=None
    for l in L2[1:]:
        w=l.split()
        if len(w)==2 and '->' not in l: cur=int(w[0]);o2[cur]=int(w[1])-cmp[1];t2[cur]={}
        elif '->' in l: t2[cur][int(w[0])]=int(w[2])
    seen={(0,0)};st=[(0,0)];eq=q2==tau
    while st and eq:
        u,v=st.pop()
        if O2[u]!=o2[v]: eq=False;break
        for c in range(tau):
            nx=(T2[u][c],t2[v][c])
            if nx not in seen: seen.add(nx);st.append(nx)
    print(f'  equivalent to {os.path.basename(cmp[0])} ({len(o2)} states): {eq}')
