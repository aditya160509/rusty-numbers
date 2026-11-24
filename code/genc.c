#include <stdio.h>
#include <stdlib.h>
#define G(a,i) ((a[(i)>>3]>>((i)&7))&1)
#define S(a,i) (a[(i)>>3]|=1<<((i)&7))
int main(int c,char**v){long N=atol(v[1]);int d=atoi(v[2]);long K=2*d+3,M=K*(N+10)+100;
 unsigned char*ia=calloc(M/8+1,1);FILE*f=fopen(v[3],"wb");long b=0;signed char buf[1<<20];int bi=0;
 for(long n=0;n<N;n++){long b1=b+1;while(G(ia,b1))b1++;long b2=b1+1;while(G(ia,b2))b2++;b=b2;
  long a=b1+(long)d*b2;S(ia,a);buf[bi++]=(signed char)(a-K*(n+1));if(bi==(1<<20)){fwrite(buf,1,bi,f);bi=0;}}
 fwrite(buf,1,bi,f);fclose(f);}
