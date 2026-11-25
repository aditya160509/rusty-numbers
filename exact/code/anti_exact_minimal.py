"""Explicit minimal MSD-first DFAO for positive linear anti-recurrences.
Index input n>=0, output A[n+1]-(k*tau+1)*(n+1). Leading zeros allowed.
The accompanying research note supplies the proof; this program is a cross-check.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from itertools import accumulate
from typing import Iterable

State = tuple[int, int]

@dataclass(frozen=True)
class Anti:
    coeff: tuple[int, ...]
    k: int = field(init=False)
    q: int = field(init=False)
    L: int = field(init=False)
    T: int = field(init=False)
    C: int = field(init=False)
    H: int = field(init=False)
    prefix: tuple[int, ...] = field(init=False)
    def __post_init__(self) -> None:
        if len(self.coeff)<2 or any(type(a) is not int or a<=0 for a in self.coeff):
            raise ValueError('at least two strictly positive integer coefficients required')
        k=len(self.coeff); q=sum(self.coeff); L=k*q
        T=L+1-sum(i*a for i,a in enumerate(self.coeff,1))
        C=((k*k-k)*T+k*k*(q-1)-1)//(k*k-1)
        H=C//k-T
        for name,value in [('k',k),('q',q),('L',L),('T',T),('C',C),('H',H),('prefix',tuple(accumulate(self.coeff,initial=0)))]:
            object.__setattr__(self,name,value)
    @property
    def initial(self) -> State:
        return (0,-self.T)
    def f(self, a:int, b:int, r:int) -> int:
        k,q,L=self.k,self.q,self.L
        j=max(0,min(k,a-k*r))
        t=max(0,min(k,L+b-k*r))
        return -self.T-r-self.prefix[j]+q-self.prefix[t]
    def step(self,state:State,r:int) -> State:
        if not 0<=r<self.q: raise ValueError('digit outside base')
        a,b=state
        return (0 if r==0 else max(0,self.f(a,b,r-1)),self.f(a,b,r))
    def read_state(self, digits:Iterable[int]) -> State:
        state=self.initial
        for r in digits:state=self.step(state,r)
        return state
    def digits(self, digits:Iterable[int]) -> int:
        return self.read_state(digits)[1]
    def state_at(self,n:int) -> State:
        if n<0:raise ValueError('nonnegative index required')
        digits=[]
        while n:
            n,r=divmod(n,self.q);digits.append(r)
        return self.read_state(reversed(digits))
    def evaluate(self,n:int) -> int:
        return self.state_at(n)[1]
    def B(self,m:int) -> int:
        if m<1:raise ValueError('positive complement index required')
        p,z0=divmod(m-1,self.L);z=z0+1
        a,b=self.state_at(p)
        return m+p-int(z<=a)+int(z>self.L+b)
    def A(self,n:int) -> int:
        if n<1:raise ValueError('positive index required')
        return (self.L+1)*n+self.evaluate(n-1)
    def state_count(self) -> int:
        return (self.C+self.H+1+max(0,self.H)+sum(max(0,(self.C-t)//self.k-self.T-(self.prefix[self.k-t]-1)) for t in range(1,self.k)))
    def states(self) -> set[State]:
        ans={(0,b) for b in range(-self.C,self.H+1)}
        ans.update((j,j-1) for j in range(1,self.H+1))
        for t in range(1,self.k):
            delta=self.prefix[self.k-t]-1
            ans.update((j-delta,j) for j in range(delta+1,(self.C-t)//self.k-self.T+1))
        return ans
    def reachable(self) -> set[State]:
        seen={self.initial}; todo=[self.initial]
        for s in todo:
            for r in range(self.q):
                v=self.step(s,r)
                if v not in seen:seen.add(v);todo.append(v)
        return seen
    def automaton(self) -> tuple[list[int],list[list[int]]]:
        states=[self.initial];ids={self.initial:0};out=[];tr=[]
        for s in states:
            out.append(s[1]);row=[]
            for r in range(self.q):
                v=self.step(s,r)
                if v not in ids:ids[v]=len(states);states.append(v)
                row.append(ids[v])
            tr.append(row)
        return out,tr
    def first_occurrence(self, error:int) -> int | None:
        """Smallest positive index n with e_n=error, or None if unattained."""
        seen={self.initial}; todo=[(self.initial,0)]
        for state,p in todo:
            if state[1]==error:return p+1
            for r in range(self.q):
                nxt=self.step(state,r)
                if nxt not in seen:
                    seen.add(nxt);todo.append((nxt,p*self.q+r))
        return None
    def walnut(self) -> str:
        out,tr=self.automaton();offset=self.C
        return f'msd_{self.q}\n\n'+''.join(f'{i} {v+offset}\n'+''.join(f'{r} -> {t}\n' for r,t in enumerate(tr[i]))+'\n' for i,v in enumerate(out))

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('coeff',type=int,nargs='+');p.add_argument('--index',type=int);p.add_argument('--walnut',action='store_true');p.add_argument('--check',action='store_true')
    args=p.parse_args();m=Anti(tuple(args.coeff))
    if args.walnut:print(m.walnut(),end='')
    elif args.index is not None:print(m.A(args.index))
    else:
        print(f'coeff={m.coeff} base={m.q} range=[{-m.C},{m.H}] states={m.state_count()}')
        if args.check:assert m.reachable()==m.states();print('explicit state set equals reachable state set')
