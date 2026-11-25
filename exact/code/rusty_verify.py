from pathlib import Path
from collections import deque
from rusty_exact import build, check
ROOT=Path(__file__).parent/'rusty_work'
def supplied(d):
 name={3:'DTHREE',4:'D'}.get(d,chr(65+d))
 lines=(ROOT/'automata'/f'RUSTY{name}.txt').read_text().splitlines();out={};tr={}
 for line in lines[1:]:
  if not line.strip():continue
  if '->' in line:
   r,t=map(int,line.split('->'));tr[s][r]=t
  else:
   s,o=map(int,line.split());out[s]=o;tr[s]={}
 offset=out[0]+2
 return [out[i]-offset for i in range(len(out))],[[tr[i][r] for r in range(d+1)] for i in range(len(out))]
def equiv(o,t,p,u):
 seen={(0,0)};todo=deque(seen)
 while todo:
  a,b=todo.popleft();assert o[a]==p[b],(a,b,o[a],p[b])
  for x,y in zip(t[a],u[b]):
   if (x,y) not in seen:seen.add((x,y));todo.append((x,y))
 return len(seen)
if __name__=='__main__':
 for d in range(1,16):
  o,t,raw=build((1,d));p,u=supplied(d);print('equiv',d,len(o),raw,equiv(o,t,p,u),flush=True)
 for a in [(2,3),(1,1,1),(3,1,2),(10,1),(1,10),(1,1,1,1),(1,2,3,4),(2,2)]:print('general',a,check(a,100000),flush=True)
 for d in range(16,41):
  m,raw=check((1,d));assert m==10*(d//3)+[-4,-1,1][d%3];print('count',d,m,raw,flush=True)
