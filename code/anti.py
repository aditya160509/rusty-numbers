"""Anti-recurrence sequences A_n = sum a_j B_{(n-1)k+j}; B = complement of A, taken blockwise by mex."""
import sys
def anti(a,N):
    k=len(a); A=[]; inA=set(); b=1
    while len(A)<N:
        blk=[]
        while len(blk)<k:
            if b not in inA: blk.append(b)
            b+=1
        v=sum(x*y for x,y in zip(a,blk)); A.append(v); inA.add(v)
    return A
if __name__=='__main__':
    a=tuple(map(int,sys.argv[1].split(','))); N=int(sys.argv[2])
    A=anti(a,N); k=len(a); tau=sum(a); kap=k*tau+1
    d=[A[n]-kap*(n+1) for n in range(N)]
    print('first',A[:12]); print('kappa',kap,'diff range',min(d),max(d))
    import pickle; pickle.dump(A,open(f'anti_{"_".join(map(str,a))}.pkl','wb'))
