/* Independent greedy complement generator; compare to an exported DFAO.
 * Input from stdin: k q states N, coefficients, outputs, then transition rows.
 * Uses bitset of A values and a uint32 array of prefix states.
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include <limits.h>
#define FAIL(msg) do {fprintf(stderr,"%s\n",msg); return 2;} while (0)
static unsigned get(const uint8_t *b,uint64_t i){return (b[i/8]>>(i%8))&1u;}
static void set(uint8_t *b,uint64_t i){b[i/8]|=(uint8_t)(1u<<(i%8));}
int main(void){
    unsigned k,q,S; uint64_t N;
    if(scanf("%u %u %u %"SCNu64,&k,&q,&S,&N)!=4||k<2||q<2||!S||!N) FAIL("bad header");
    uint64_t K=(uint64_t)k*q+1, sum=0;
    uint32_t *a=calloc(k,sizeof(*a)),*tr=calloc((size_t)S*q,sizeof(*tr));
    int64_t *out=calloc(S,sizeof(*out));
    if(!a||!tr||!out) FAIL("allocation failed");
    for(unsigned i=0;i<k;i++){if(scanf("%"SCNu32,&a[i])!=1) FAIL("bad coefficient");sum+=a[i];}
    if(sum!=q) FAIL("wrong trace");
    int64_t maxout=0;
    for(unsigned i=0;i<S;i++){if(scanf("%"SCNd64,&out[i])!=1) FAIL("bad output");if(out[i]>maxout)maxout=out[i];}
    for(size_t i=0;i<(size_t)S*q;i++)if(scanf("%"SCNu32,&tr[i])!=1||tr[i]>=S)FAIL("bad transition");
    if(N>(UINT64_MAX-(uint64_t)maxout-100)/K) FAIL("index overflow");
    uint64_t M=K*N+(uint64_t)maxout+100;
    if(N>SIZE_MAX/sizeof(uint32_t)||M/8+1>SIZE_MAX)FAIL("allocation overflow");
    uint8_t *bits=calloc((size_t)(M/8+1),1);
    uint32_t *states=calloc((size_t)N,sizeof(*states));
    if(!bits||!states)FAIL("large allocation failed");
    uint64_t b=0,prevA=0; int64_t mn=INT64_MAX,mx=INT64_MIN;
    for(uint64_t n=0;n<N;n++){
        uint64_t A=0;
        for(unsigned i=0;i<k;i++){
            do {if(++b>M)FAIL("B out of range");} while(get(bits,b));
            if(a[i]&&b>(UINT64_MAX-A)/a[i])FAIL("sum overflow");
            A+=(uint64_t)a[i]*b;
        }
        if(A<=b||A<=prevA||A>M||get(bits,A))FAIL("invalid greedy A");
        set(bits,A);prevA=A;
        int64_t e=(int64_t)A-(int64_t)(K*(n+1));
        if(n)states[n]=tr[(size_t)states[n/q]*q+n%q];
        if(e!=out[states[n]]){fprintf(stderr,"mismatch n=%"PRIu64" got=%"PRId64" expected=%"PRId64"\n",n+1,e,out[states[n]]);return 1;}
        if(e<mn)mn=e;
        if(e>mx)mx=e;
    }
    printf("PASS k=%u q=%u states=%u N=%"PRIu64" observed=[%"PRId64",%"PRId64"] allocated_bytes=%"PRIu64"\n",k,q,S,N,mn,mx,M/8+1+4*N);
    free(bits);free(states);free(a);free(tr);free(out);return 0;
}
