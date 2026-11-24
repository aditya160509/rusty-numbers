"""Write Walnut word automaton RUSTY{d}.txt and proof script rusty{d}.txt for a=(1,d)."""
import json,sys
D=int(sys.argv[1]); q=D+1; K=2*q+1; A=json.load(open(f'dfao_1_{D}.json'))
off=-min(A['out']); s=f'msd_{q}\n\n'
for i,(row,o) in enumerate(zip(A['trans'],A['out'])):
    s+=f'{i} {o+off}\n'+''.join(f'{j} -> {t}\n' for j,t in enumerate(row))+'\n'
W='RUSTY'+chr(65+D)+('THREE' if D==3 else '')  # Walnut rejects word names ending in a digit
open(f'{W}.txt','w').write(s)
b=f'?msd_{q}'; a,b1,b2=f'a1{D}',f'b1{D}',f'b2{D}'
open(f'rusty{D}.txt','w').write(f'''def {a} "{b} n>0 & s+{off}={K}*n+{W}[n-1]":
def {b2} "{b} Es ${a}(n,s) & {q}*t<=s+2 & s+2<{q}*t+{q}":
def {b1} "{b} Es,t ${a}(n,s) & ${b2}(n,t) & u+{D}*t=s":
eval r{D}_total "{b} An n>0 => (Es,t,u ${a}(n,s) & ${b1}(n,t) & ${b2}(n,u))":
eval r{D}_init "{b} ${b1}(1,1) & ${b2}(1,2) & ${a}(1,{1+2*D})":
eval r{D}_order "{b} An,s,t,u (${b1}(n,s) & ${b2}(n,t) & ${b1}(n+1,u)) => (s<t & t<u)":
eval r{D}_b1_new "{b} An,s,m (${b1}(n,s) & m<n & m>0) => (~${a}(m,s))":
eval r{D}_b2_new "{b} An,s,m (${b2}(n,s) & m<n & m>0) => (~${a}(m,s))":
eval r{D}_mex_b1 "{b} An,s,t (${b1}(n,s) & t>0 & t<s) => (Em m>0 & m<n & (${b1}(m,t)|${b2}(m,t)|${a}(m,t)))":
eval r{D}_mex_b2 "{b} An,u,s,t (${b1}(n,u) & ${b2}(n,s) & u<t & t<s) => (Em m>0 & m<n & ${a}(m,t))":
eval r{D}_sum "{b} An,s,t (${b1}(n,s) & ${b2}(n,t)) => ${a}(n,s+{D}*t)":
''')
