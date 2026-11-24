// anti-recurrence generator: writes int8 d(n)=A_{n+1}-kappa(n+1) to file
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(int c,char**v){int k=c-3; long N=atol(v[1]); int a[8],tau=0; for(int i=0;i<k;i++){a[i]=atoi(v[3+i]);tau+=a[i];}
 long kap=(long)k*tau+1; long M=kap*(N+10)+100; unsigned char*inA=calloc(M/8+1,1);
 FILE*f=fopen(v[2],"wb"); long b=1; signed char*out=malloc(N);
 for(long n=0;n<N;n++){long s=0;for(int j=0;j<k;j++){while(inA[b>>3]>>(b&7)&1)b++; s+=a[j]*b; b++;}
  inA[s>>3]|=1<<(s&7); long dd=s-kap*(n+1); if(dd<-127||dd>127){printf("overflow at %ld: %ld\n",n,dd);return 1;} out[n]=dd;}
 fwrite(out,1,N,f); fclose(f); signed char mn=127,mx=-128; for(long n=0;n<N;n++){if(out[n]<mn)mn=out[n];if(out[n]>mx)mx=out[n];}
 printf("N=%ld kappa=%ld range [%d,%d]\n",N,kap,mn,mx);}
