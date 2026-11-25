// general anti-recurrence: e_n = A_n - kappa*n, n=1..N, int16. args: N out a1 a2 ...
#include <stdio.h>
#include <stdlib.h>
#define G(a,i) ((a[(i)>>3]>>((i)&7))&1)
#define S(a,i) (a[(i)>>3]|=1<<((i)&7))
int main(int c,char**v){long N=atol(v[1]);int k=c-3;long a[16],tau=0;for(int i=0;i<k;i++){a[i]=atol(v[3+i]);tau+=a[i];}
 long K=k*tau+1,M=K*(N+10)+1000;unsigned char*ia=calloc(M/8+1,1);FILE*f=fopen(v[2],"wb");long b=0;
 short*buf=malloc(2<<20);int bi=0;
 for(long n=1;n<=N;n++){long s=0;for(int i=0;i<k;i++){b++;while(G(ia,b))b++;s+=a[i]*b;}
  if(s>=M){fprintf(stderr,"overflow\n");return 1;} S(ia,s);long e=s-K*n;
  if(e<-32000||e>32000){fprintf(stderr,"e range\n");return 1;} buf[bi++]=(short)e;if(bi==(1<<20)){fwrite(buf,2,bi,f);bi=0;}}
 fwrite(buf,2,bi,f);fclose(f);return 0;}
