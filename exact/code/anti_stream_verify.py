from pathlib import Path
from subprocess import run
from anti_exact_minimal import Anti
from rusty_exact import build
root=Path(__file__).parent
N=10_000_000
for a in [(1,4),(1,9),(1,20),(2,3),(1,1,1),(3,1,2),(0,2),(3,0),(0,0,0,2)]:
    o,t=Anti(a).automaton() if all(a) else build(a)[:2]
    lines=[f'{len(a)} {sum(a)} {len(o)} {N}', ' '.join(map(str,a)), ' '.join(map(str,o))]+[' '.join(map(str,r)) for r in t]
    result=run([str(root/'anti_stream_check')],input='\n'.join(lines)+'\n',text=True,capture_output=True,check=True)
    print(a,result.stdout.strip(),flush=True)
