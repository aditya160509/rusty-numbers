# Exact discrepancy ranges and minimal automata for linear anti-recurrences

**Research working note — 25 November 2026**  
**Scope:** the attached `rusty-all-d.zip`, the Fokkink–Joshi conjecture, and structural extensions.  
**Status:** complete candidate mathematical proofs, executable implementations, and independently generated computational checks. Not peer reviewed or formally verified. Literature priority is not established.

## 0. Executive result: what to do next

The attached manuscript proves automaticity for rusty parameters `1 <= d <= 15` by individual Walnut certificates (the archive reports those certificates; the actual logs are absent). The route in `PROMPT_ALL_D.md` can be completed without further Walnut runs. More importantly, a two-coordinate inverse-rank identity yields explicit **exact discrepancy ranges and minimal state counts for every strictly positive integer linear form**, not only for the rusty family.

The principal contribution worth developing is the exact structural theorem below. Earlier public projects already claim the full positive-coefficient automaticity conjecture; one also gives a two-term recurrence. Those claims must be cited and checked before publication. The exact state-count formula, the exact range formula, the direct minimal state classification, and the admissible-zero extension are stronger targets than repeating automaticity. I did not find these exact general formulas in the sources I inspected. That is a bounded literature observation, not a priority certificate.

For `a = (1,d)`, let `q=d+1` and let `e_n=A_n-(2d+3)n`. Define

\[
C=\left\lfloor\frac{4d+3}{3}\right\rfloor,
\qquad H=\left\lfloor\frac C2\right\rfloor-2.
\]

Then the proposed exact theorem is

\[
\{e_n:n\ge1\}=[-C,H]\cap\mathbb Z,
\]

and the minimal base-`q` MSD-first DFAO for input `n-1` and output `e_n` has

\[
S(d)=\begin{cases}
2&d=1,\\
3&d=2,\\
10m-4&d=3m,\ m\ge1,\\
10m-1&d=3m+1,\ m\ge1,\\
10m+1&d=3m+2,\ m\ge1.
\end{cases}
\]

Thus the period-three pattern in the archive follows from a proof, rather than being an extrapolation. The proof is a special case of the arbitrary-vector theorem in Sections 2–6.

### Evidence obtained in this session

- Reconstructed DFAOs directly from mathematical inverse-rank rules, with no learned substitution.
- Full product-automaton equivalence to all 15 archive automata (all finite input words, not just a numerical prefix). The initial output fixes the stored output offset.
- Independent general window automata agree with the closed-form minimal construction for every rusty parameter `1..40`, and a subset of general forms.
- The explicit state set equals the reachable set; independent Moore refinement confirms minimality for the tested forms. Tests include every rusty `d=1..40`, plus `d=50,60,100,150,200,300,500`.
- Checked 1,636 exhaustive positive vectors across four grids and 100 additional seeded random vectors. Each was checked against an independent greedy generator on 1,000 terms and against reachability and minimization. Some forms overlap with the rusty checks, so do not add those counts as distinct vectors.
- Tested 423 admissible zero-containing coefficient vectors on 3,000 terms each, plus eight named zero-containing vectors on 100,000 terms.
- Independent compiled C generator: nine forms, 10,000,000 terms each, no discrepancy. Largest bitset-plus-state-array allocation was 93,750,014 bytes (about 94 MB); not a measured process RSS.
- Direct random access to both complementary sequences verified for 10 forms at 20,000 A terms and their generating B blocks.

These are cross-checks of the proofs, not substitutes for them.

## 1. Definitions, conventions and foundational identities

Let `k>=2`, let `a=(a_1,...,a_k)` have strictly positive integer entries (Section 9 separately considers zeros), and define

\[
q=\sum_{i=1}^k a_i,\quad L=kq,\quad K=L+1,
\quad A_1=\sum_{i=1}^k i a_i,
\quad T=K-A_1=1+\sum_{i=1}^k(k-i)a_i.
\]

The original paper uses trace `tau=q`, slope `kappa=K`. We use `L` for the slope minus one and `T` for the magnitude of the initial discrepancy. In particular, `q>=k`, `k<=T<=(k-1)q<=L-k`.

The greedy construction chooses the next `k` smallest unused positive integers as a block of B, then sets

\[
A_n=\sum_{i=1}^k a_i B_{k(n-1)+i}.
\]

The B sequence increases, the positive weighted sum is strictly larger than its last generating B term, and successive A terms differ by at least `L`. Consequently all entries are distinct, the A and B sequences are increasing, and every positive integer is eventually used (the mex tends to infinity). These arguments also give uniqueness by induction. These standard facts are in the original paper, but are included here to specify what is required.

Set

\[
e_n=A_n-Kn\quad(n\ge1),\qquad e_0=0,\quad A_0=0,\quad D_j=A_j-j=Lj+e_j.
\]

The artificial zero is used only for inverse ranks at the boundary; it is not a positive-sequence term and may be outside the exact discrepancy range.

From the gap bound,

\[
e_{n+1}\ge e_n-1\quad(n\ge1).
\tag{1}
\]

This seemingly minor inequality is crucial to the sharpness and state-count proofs. It is **not** asserted for `n=0`.

### Lemma 1 (inverse rank)

For each `m>=1`, let `t(m)` be the number of positive A terms strictly below `B_m`. Then

\[
B_m=m+t(m),\qquad
D_{t(m)}<m\le D_{t(m)+1}.
\tag{2}
\]

Equivalently,

\[
t(m)=\#\{j\ge1:Lj+e_j<m\}.
\tag{3}
\]

**Proof.** Exactly `m-1` B terms and `t(m)` A terms are smaller than `B_m`; hence `B_m=m+t(m)`. Exactly `A_j-j` B terms are smaller than `A_j`, so `A_j<B_m` if and only if `A_j-j<m`. This proves (3); because `D_j` is strictly increasing and `D_0=0`, it also proves (2). For an index in the block generating `A_n`, no A term with index at least `n` is counted, because `B_m<=B_{kn}<A_n`. □

### Lemma 2 (balance identity)

Write the shifted index as

\[
n-1=qp+r,\qquad p\ge0,\quad 0\le r<q.
\]

Put `z_i=kr+i` (so `1<=z_i<=L`). The generating B indices are `m_i=Lp+z_i`. Then

\[
e_{qp+r+1}=-T-r+\sum_{i=1}^k a_i(t(m_i)-p).
\tag{4}
\]

**Proof.** Substitute `B_{m_i}=m_i+t(m_i)` in the recurrence and subtract `K(qp+r+1)`. Use `sum a_i=q`, `sum i*a_i=A_1`, and `L=kq`. □

## 2. The general exact discrepancy bound

This section gives a stand-alone proof of the claimed closed-form box. It uses neither a fitted substitution nor any computed sequence terms other than the known first block.

### Theorem 1 (closed form)

For every strictly positive integral coefficient vector of dimension `k>=2`, define

\[
\boxed{C=\left\lfloor\frac{(k^2-k)T+k^2(q-1)-1}{k^2-1}\right\rfloor,\qquad H=\left\lfloor\frac Ck\right\rfloor-T.}
\tag{5}
\]

Then `-C <= e_n <= H` for all `n>=1`. Both endpoints are attained (Section 4); in fact every integer in the interval occurs (Section 5).

### 2.1. Preliminary arithmetic

Set `M=T+q-1`, `N=k^2 M-kT`, `D=k^2-1`. The value `C=floor((N-1)/D)` is the least integer solution of

\[
C=M+\left\lfloor\frac{C-kT}{k^2}\right\rfloor.
\tag{6}
\]

Indeed, (6) is equivalent to

\[
N-k^2<DC\le N.
\]

The smallest integer in this interval is `floor((N-k^2)/D)+1=floor((N-1)/D)`. The floor nesting identity `floor((floor(C/k)-T)/k)=floor((C-kT)/k^2)` gives

\[
C=T+q-1+\lfloor H/k\rfloor,\qquad H=-T+\lfloor C/k\rfloor.
\tag{7}
\]

We need several elementary bounds on `C`. Since `k<=T<=(k-1)q` and `q>=k`,

\[
N-1-DT=k^2(q-1)-(k-1)T-1
\ge(2k-1)q-k^2-1\ge k^2-k-1>0.
\]

Hence `C>=T>=k`. Also

\[
DL-(N-1)\ge k(k-2)q+k^2+1
\ge k^2(k-1)+1>D(k-1).
\]

Thus `C<=L-k`. Consequently,

\[
 k\le T\le C\le L-k,\quad
 -T+1\le H\le q-1-T\le q-k-1,\quad H\ge-L+k.
\tag{8}
\]

### 2.2. Exact scalar floor bounds

For `0<=r<q`, define

\[
\Phi(r,y)=-T-r+\sum_{i=1}^k a_i\left\lfloor\frac{kr+i-1-y}{L}\right\rfloor.
\tag{9}
\]

We claim

\[
\max_{0\le r<q}\Phi(r,-C)=-T+\lfloor C/k\rfloor=H,
\tag{10}
\]

and

\[
\min_{0\le r<q}\Phi(r,H)=-T-q+1-\lfloor H/k\rfloor=-C.
\tag{11}
\]

Here is the complete floor analysis, including negative `H`.

Let `P_j=sum_{i=1}^j a_i`, with `P_0=0`. For `-L<=y<L`, the summand floor equals `-1` if `z_i<=y`, `+1` if `z_i>L+y`, and `0` otherwise. The two nonzero cases cannot overlap. For `y=-C`, only the plus case occurs. Write `C=ks+t`, `0<=t<k`. All blocks before the threshold `L-C` give baseline `-T-r`; if `t>0` there is one partial plus block at `r=q-s-1`, with suffix weight `q-P_{k-t}`; then all blocks `r=q-s,...,q-1` are full plus blocks, giving `-T-r+q`. A partial plus value is at most the first full-plus value, since `P_{k-t}>=1`. The first full block exists because `k<=C<=L-k`. Its value is `-T+s`, which exceeds all baseline values. This proves (10).

For (11), first suppose `H>=0` and write `H=ks+t`, `0<=t<k`. Full minus blocks, if present, are `r=0,...,s-1`, giving `-T-r-q`, with minimum `-T-q+1-s`. The partial minus block at `r=s` subtracts `P_t<=q-1`, so is no smaller. The later baseline values are no smaller than `-T-q+1`. If `s=0`, the minimum is that last baseline value instead, as the partial minus block subtracts at most `q-1`. This proves (11) for nonnegative `H`.

If `H<0`, put `r_0=floor((L+H)/k)=q+floor(H/k)`. By (8), `1<=r_0<=q-1`. Before `r_0` no plus shift occurs, so the last baseline value is `-T-r_0+1`. The partial or full plus block at `r_0` adds at least one, and any later full plus block has value at least `-T+1`. Therefore the minimum is again `-T-r_0+1=-T-q+1-floor(H/k)`. □

### 2.3. Strong induction: no circularity

Suppose all earlier positive-index discrepancies lie in `[-C,H]`. Let `n=qp+r+1` and use (3) for `m_i=Lp+kr+i`. The rank only counts indices below `n`. The lower error bound yields

\[
t(m_i)\le p+\left\lfloor\frac{kr+i-1+C}{L}\right\rfloor.
\]

The upper error bound yields

\[
t(m_i)\ge p+\left\lfloor\frac{kr+i-1-H}{L}\right\rfloor.
\]

For the latter inequality, all positive indices through the displayed right side must be earlier than `n`. By `H>=-L+k`, the floor is at most one. If `p>=1`, then `p+1<=qp<n`. If `p=0,r>=1`, then `1<n`. If `p=r=0`, then `kr+i-1-H<=k-1+L-k=L-1`, so no positive index qualifies. Negative lower bounds are automatically valid. This explicitly handles the induction base.

Now (4) gives `Phi(r,H)<=e_n<=Phi(r,-C)`. By (10) and (11), the desired box is invariant. Strong induction proves Theorem 1's bound. □

**Relation to the archive's contraction:** the symmetric bound in `PROMPT_ALL_D.md` is also correct after the floor and boundary details are supplied; Section 9 gives a proof even allowing admissible zeros. The closed-form box above is substantially sharper.

## 3. The two-coordinate identity and the minimal machine construction

### Theorem 2 (local rule)

For `0<=r<q` and integers `a,b`, put

\[
F_r(a,b)=-T-r+\sum_{i=1}^k a_i\big(-[kr+i\le a]+[kr+i>L+b]\big).
\tag{12}
\]

Here `[condition]` is the indicator, and the `a_i` in the summation are the fixed coefficients (the arguments `a,b` are discrepancies). Then for every `p>=0`,

\[
\boxed{e_{qp+r+1}=F_r(e_p,e_{p+1}).}
\tag{13}
\]

**Proof.** For `p>=1`, all positive indices `j<=p-1` satisfy `D_j<m_i`, since `e_j<=H<L`. All `j>=p+2` fail the inequality, since `e_j>=-C` and `C<=L-k`. Thus in (3) the only uncertain membership is at `p,p+1`:

\[
t(m_i)=p-[z_i\le e_p]+[z_i>L+e_{p+1}].
\tag{14}
\]

At `p=0` no negative or zero index is counted. The first indicator is zero because `e_0=0` and `z_i>=1`; all `j>=2` fail. So (14) still holds. Substitute in (4). □

This general two-term mechanism has an earlier public counterpart in Larsen Cundric's AI-generated anti-recurrence draft. The following sharp quotient and closed-form state classification are the additional structural results developed here. Do not present the two-term mechanism itself as unprecedented.

### Constant-time evaluation of a transition

Define `clip_k(v)=min(k,max(0,v))`. With prefix sums `P_j`, equation (12) becomes

\[
\boxed{F_r(a,b)=-T-r-P_{\operatorname{clip}_k(a-kr)}+q-P_{\operatorname{clip}_k(L+b-kr)}.}
\tag{15}
\]

Every transition requires only a constant number of integer operations and two prefix-sum lookups, even for large `k`. There is no need to loop over all coefficients per digit.

### Theorem 3 (canonical two-coordinate DFAO)

Define the feature at shifted input index `p>=0` as

\[
W(p)=(\max(e_p,0),e_{p+1}).
\tag{16}
\]

The initial state is `(0,-T)` and the output of `(a,b)` is `b`. The digit transition is

\[
\boxed{
\delta_r(a,b)=
\begin{cases}
(0,F_0(a,b)),&r=0,\\
(\max(0,F_{r-1}(a,b)),F_r(a,b)),&1\le r<q.
\end{cases}}
\tag{17}
\]

For all `p>=0`, `W(qp+r)=delta_r(W(p))`.

**Proof.** Since `z_i>=1`, replacing the first argument of `F_r` by its nonnegative part changes no indicator. Equation (13) therefore proves the second output coordinate and, when `r>=1`, the first coordinate as well. For `r=0` and `p>=1`, `e_{qp}=F_{q-1}(e_{p-1},e_p)`. Every `F_{q-1}` is at most `-T-(q-1)+q=1-T<0`; hence the first coordinate is zero. If `p=0`, its first coordinate is already `max(e_0,0)=0`. This proves the transition identity including leading zeros. The finite box for discrepancies bounds the feature alphabet. Induction on the input digits, using Horner's rule for the base-`q` index, proves that the output is `e_{p+1}` for every input `p`. □

This is a direct all-parameter construction of the automatic discrepancy. The shift is explicit: the machine reads `n-1`, matching `RUSTY*.txt` and the attached manuscript. Automaticity of `e_n` on positive input `n` follows also by the usual closure of automatic sequences under a fixed index shift. Alternatively, construct the unshifted machine from adjacent features with a special initial state. The exact state count below is specifically for the shifted convention; do not quote it for the unshifted machine.

### Synchronization

For every reachable state, `L+b>=k` by (8). Thus in digit zero the plus contribution vanishes and

\[
\delta_0(a,b)=(0,-T-P_{\operatorname{clip}_k(a)}),\qquad
\delta_0^2(a,b)=(0,-T).
\tag{18}
\]

In particular the initial state has a zero self-loop, and the word `00` synchronizes the machine. This will prove recurrence of every output and simplify the exact reachability proof.

## 4. Sharpness: the box is not merely an upper estimate

Let `c=-min_{n>=1} e_n` and `h=max_{n>=1} e_n`, which exist because Theorem 1 has established a finite integer alphabet. Then `T<=c<=C` and `-T<=h<=H`, since `e_1=-T`. We show that `(c,h)` satisfies the same fixed point equations (7). This also proves the narrowest-box conjecture stated in the earlier public draft (subject to checking its latest version and the exact criterion).

The map `F_r(a,b)` is nonincreasing in both arguments, because the coefficients are positive. The box and the artificial value `e_0=0` imply

\[
F_r(h,h)\le e_{qp+r+1}\le F_r(-c,-c).
\tag{19}
\]

At `p=0`, if `h<0` the first argument `e_0=0` exceeds `h`; this does not invalidate the lower inequality because all nonpositive first arguments give identical indicators. For `h>=0` there is no issue.

**Attainment of the upper envelope.** Choose `p>=0` with `e_{p+1}=-c`. If `p>=1`, (1) gives `e_p<=-c+1<=0`; for `p=0`, `e_p=0`. Thus `F_r(e_p,e_{p+1})=F_r(-c,-c)` for every digit `r`, since the first indicator vanishes for both. Taking the maximizing digit and repeating the calculation in Section 2.2 (valid because `k<=c<=L-k`) yields

\[
h=-T+\lfloor c/k\rfloor.
\tag{20}
\]

**Attainment of the lower envelope.** If `h>=1`, choose `p>=1` with `e_p=h`. By (1), `e_{p+1}>=h-1>=0`. The plus indicators vanish for both `e_{p+1}` and `h`, so `F_r(e_p,e_{p+1})=F_r(h,h)` for all digits. If `h<=0`, instead choose `p>=0` with `e_{p+1}=h`. Then `e_p<=0` (including `p=0`), so the first indicators vanish for both and the same equality holds. Take the minimizing digit and apply Section 2.2, now with `h>=-T>=-L+k` and `h<L`. This gives

\[
c=T+q-1+\lfloor h/k\rfloor.
\tag{21}
\]

Equations (20) and (21) imply `c=M+floor((c-kT)/k^2)`. Section 2.1 proved that `C` is the smallest integer solution. But `c<=C` by the bound, so `c=C` and `h=H`. Both endpoints are attained. □

### Consequence: exact range depends on only three aggregate parameters

The endpoints depend only on `k`, the trace `q`, and `T=K-A_1`, not on all individual coefficients. In particular, the general lower bound `e_n>=-kq+k` holds. This strengthens the loose `-kq` bound in the earlier draft. The complete state count does depend on individual prefix sums.

## 5. Every intermediate discrepancy is attained

This does not follow merely from knowing the endpoints: an arbitrary bounded automatic sequence may skip values. Here it follows from (1) and (18).

Take any state reached by a finite word `w`. For any nonzero and arbitrarily long base-`q` prefix `v`, the concatenation `v00w` reaches the same state, because `00` resets to the initial state. Thus every reachable output occurs at arbitrarily large positive indices. In particular choose an occurrence of `H` and a later occurrence of `-C`. As one moves from the first occurrence to the second, (1) says each downward step is at most one. Every integer between `-C` and `H` is therefore attained.

\[
\boxed{\{e_n:n\ge1\}=\{-C,-C+1,\ldots,H\}.}
\tag{22}
\]

This argument also supplies arbitrarily long canonical (non-leading-zero) representations for every reachable state. That matters if a referee worries about differing automaton conventions.

## 6. Exact state classification and minimality for ALL positive forms

This is the strongest structural result in this note. It is not limited to the rusty family. It gives the entire reachable state set explicitly; no automaton minimization is needed to compute the answer.

Define for each `t=1,...,k-1`

\[
\Delta_t=P_{k-t}-1,\qquad H_t=\left\lfloor\frac{C-t}{k}\right\rfloor-T.
\tag{23}
\]

Let `x_+=max(x,0)`. The exact reachable states of (17) are the following disjoint families:

\[
\begin{aligned}
Q_0&=\{(0,b):-C\le b\le H\},\\
Q_1&=\{(j,j-1):1\le j\le H\},\\
Q_2&=\bigcup_{t=1}^{k-1}\{(j-\Delta_t,j):\Delta_t+1\le j\le H_t\}.
\end{aligned}
\tag{24}
\]

Empty intervals contribute no states. All variables in (24) are integers.

### 6.1. Why no other positive-first states can exist

A state with positive first coordinate cannot be initial and cannot come from a zero digit. It must come from consecutive values `F_{r-1}(a,b),F_r(a,b)` with `r>=1` and the first value strictly positive.

If `b>=0`, there is no plus contribution and every `F_r` is negative, since `T>=k>=2`. Thus the parent must have `b<0`. For such a reachable parent, (1) implies `e_p<=e_{p+1}+1<=0` whenever `p>=1`, and at `p=0` the first coordinate is zero as well. Its clipped first coordinate is therefore zero. All outputs now come from the baseline, an optional partial plus block, and the trailing full plus blocks. This is the block structure of Section 2.2.

Write `-b=ks+t` with `0<=t<k`. Before the plus region, outputs are `-T-r<0`. Within full plus blocks they are `-T-r+q`, decreasing by exactly one with each digit. If the preceding positive value is from a full plus block, the pair has form `(j,j-1)` with `1<=j<=H`, so is in `Q_1`.

If the preceding positive value is from the unique partial plus block (`t>=1`), its index is `q-s-1`, and the current block is the first full plus block at `q-s`. The latter output equals `j=s-T`. The former equals

\[
-T-(q-s-1)+(q-P_{k-t})=j-(P_{k-t}-1)=j-\Delta_t.
\]

Positivity requires `j>=Delta_t+1`, and `-b=k(j+T)+t<=C` requires `j<=H_t`. Thus the pair belongs to `Q_2`. There are no other cases.

### 6.2. All the listed states are actually reachable

We already proved that every `b` in `[-C,H]` occurs as an output.

- For `b<0`, (1) implies the clipped first coordinate must be zero (including the initial state), so `(0,b)` is reachable.
- For `j>=0` with `j<=H`, take a reachable parent with second coordinate `-k(j+T)`. This is a negative integer in `[-C,H]`, because `j+T<=floor(C/k)` and `H>=0` in the case considered. Its first coordinate is zero. The plus threshold is divisible by `k`, so there is no partial block. The first full plus block is at `r=q-(j+T)`, with output `j`; its preceding block is a negative baseline. Here `1<=r<=q-1` since `T>=k` and `C<=L-k`. Reading digit `r` gives `(0,j)`. This supplies the rest of `Q_0`.
- The same parent with `1<=j<=H`, followed by digit `r+1`, yields `(j,j-1)`. This digit is valid since `j+T>=3`. Thus every `Q_1` state is reached.
- For each allowed `t,j` in `Q_2`, use the reachable parent with second coordinate `-k(j+T)-t`. Its first coordinate is zero, and it has the partial and full plus blocks just analyzed. Reading digit `r=q-(j+T)` yields `(j-Delta_t,j)`. This digit is valid because `k(j+T)+t<=C<=L-k` and `j+T>=3`.

All states in (24) have been reached. The three families are disjoint: `Q_0` has zero first coordinate, `Q_1` has second coordinate one below the first, and `Q_2` has second coordinate at least the first. Within `Q_2`, different `t` give distinct `Delta_t` because every coefficient is positive; for a fixed `t` the second coordinates distinguish different `j`.

### 6.3. Pairwise distinguishability needs at most one digit

Two states with different second coordinates already have different outputs, so the empty suffix distinguishes them. Consider distinct states with the same second coordinate `b` and first coordinates `a<a'`. Since both first coordinates are nonnegative, choose an integer `z` with `a<z<=a'`. It lies in `[1,L]`, since the first coordinates never exceed `max(H,0)<L`. Write `z=kr+i`, `0<=r<q`, `1<=i<=k`.

In `F_r(a',b)` the minus indicator corresponding to this `i` is active, while in `F_r(a,b)` it is inactive. Other minus indicators can only change in the same direction, the plus contribution is identical, and `a_i>0`. Consequently `F_r(a',b)<F_r(a,b)`. The single digit `r` distinguishes the states.

Every state is reachable and every pair is distinguishable. The standard DFAO minimality criterion therefore proves that (24) is the **minimal** state set. No inference from finite samples, partition refinement, or computational search is necessary for this lower bound. Because Section 5 gives nonzero canonical prefixes reaching every state, the same lower bound is valid even when only canonical positive-input words are required.

### Theorem 4 (closed-form exact state complexity)

The minimal MSD-first base-`q` DFAO for the shifted discrepancy `p -> A_{p+1}-K(p+1)` has exactly

\[
\boxed{S(\mathbf a)=C+H+1+H_+ +\sum_{t=1}^{k-1}(H_t-\Delta_t)_+.}
\tag{25}
\]

Equivalently, if `rho=C mod k`, then

\[
\boxed{S(\mathbf a)=C+H+1+H_++\sum_{t=1}^{k-1}\big(H+1-P_{k-t}-[t>\rho]\big)_+.}
\tag{26}
\]

**Proof.** Count the disjoint families (24): `|Q_0|=C+H+1`, `|Q_1|=H_+`, and `|Q_{2,t}|=(H_t-Delta_t)_+`. Minimality was proved above. The equivalent expression follows from `H_t=H-[t>rho]`. □

This is a linear-time arithmetic formula in the dimension `k`. It yields an `O(kq)` upper bound on the state count because `C<=kq-k`, `H<=q-k-1` and each summand is at most `H_+`. A full transition table has `q*S` entries, but need not be materialized. If `H<=0`, the automaton has exactly `C+H+1` states, one for each discrepancy value. This includes the original A1-bounded class, since `A_1<=(k-1)q+2` implies `T>=q-1` and hence `H<=0`.

## 7. Specialization to rusty numbers

Take `k=2`, `a_1=1`, `a_2=d`, `q=d+1`. Then `T=2` and the prefix sum `P_1=1`. Thus

\[
C=\left\lfloor\frac{4q-1}{3}\right\rfloor,
\qquad H=\lfloor C/2\rfloor-2,
\]

and

\[
S(d)=C+H+1+H_++(\lfloor(C-1)/2\rfloor-2)_+.
\tag{27}
\]

For `d=1`, `C=2,H=-1`, giving `S=2`. For `d=2`, `C=3,H=-1`, giving `S=3`. For `d>=3`, `H>=0`, and `floor((C-1)/2)-2>=0`. Splitting by `d mod 3` gives:

| Parameter | C | H | Minimal state count |
|---|---:|---:|---:|
| `d=3m`, `m>=1` | `4m+1` | `2m-2` | `10m-4` |
| `d=3m+1`, `m>=1` | `4m+2` | `2m-1` | `10m-1` |
| `d=3m+2`, `m>=1` | `4m+3` | `2m-1` | `10m+1` |

Consequently `S(d+3)=S(d)+10` for every `d>=3`. The exact discrepancy range and all state families are known. In particular, the state-count pattern is no longer a conjecture if the foregoing proof withstands review.

For this specialization the local rule is especially simple:

\[
u(z)=-[z\le a]+[z>2q+b],\quad
F_r(a,b)=-2-r+u(2r+1)+d\,u(2r+2).
\tag{28}
\]

The minimal state set is

\[
\{(0,b):-C\le b\le H\}
\cup\{(j,j-1):1\le j\le H\}
\cup\{(j,j):1\le j\le\lfloor(C-5)/2\rfloor\}.
\tag{29}
\]

This is also a uniform substitution construction: replace each state by its ordered list of successors for digits `0..q-1`, take the fixed point beginning at `(0,-2)`, and apply the coding `(a,b)->b`. No fitted block map is required.

### Selected computational confirmations

| d | Exact minimum | Exact maximum | Minimal states |
|---:|---:|---:|---:|
| 3 | -5 | 0 | 6 |
| 4 | -6 | 1 | 9 |
| 5 | -7 | 1 | 11 |
| 9 | -13 | 4 | 26 |
| 15 | -21 | 8 | 46 |
| 16 | -22 | 9 | 49 |
| 17 | -23 | 9 | 51 |
| 18 | -25 | 10 | 56 |
| 30 | -41 | 18 | 96 |
| 40 | -54 | 25 | 129 |
| 100 | -134 | 65 | 329 |
| 300 | -401 | 198 | 996 |
| 500 | -667 | 331 | 1661 |

These are outputs of exact reachable finite automata checked computationally, not estimates of endpoints from finite sequences. See `anti_formula_results.txt` for the complete tested subset.

### The original d=4 break

For `(1,4)` one has `q=5`, `C=6`, `H=1`. At digit `r=0`, the plus shift is absent and the only possible minus shift comes from the first coefficient when `e_p=1`. Thus `e_{5p+1}=-2-[e_p=1]`. The progression `A_{5p+1}=9+55p` fails precisely when `e_p=1`. The original paper reports the first such failure at `p=348`. Our breadth-first search of the exact machine gives the first occurrence of discrepancy `1` at shifted input `347`, i.e. positive index `348`, confirming this directly. The supplied automaton and our equivalent construction give the same explanation. The general rule now makes it possible to find first occurrences by shortest-word search instead of generating long prefixes.

## 8. Random access, automaticity and practical improvements

The rank formula (14) also holds for arbitrary `m>=1`, not only indices of a particular block: write `m=Lp+z`, `1<=z<=L`. After reading `p` in base `q`, the state is `(a,b)=(max(e_p,0),e_{p+1})`. Then

\[
\boxed{B_m=m+p-[z\le a]+[z>L+b].}
\tag{30}
\]

The A sequence is `A_n=Kn+output(n-1)`. Thus both sequences can be evaluated at a large index without calculating any earlier terms.

Complexities (integer arithmetic operations, not a bit-complexity assertion):

- Prefix-sum preprocessing and exact endpoint/state-count calculation: `O(k)` arithmetic operations.
- One digit transition: `O(1)` arithmetic operations, using (15).
- Evaluate `A_n` or `B_m`: `O(log_q n)` or `O(log_q m)` digit transitions after preprocessing. An MSD stream needs `O(1)` additional current-state storage; the provided Python implementation buffers the input digits while converting an integer to base `q`.
- Explicit reachable transition table: `O(q*S)` time and storage, plus coefficient preprocessing. This is output-size proportional. The explicit state family can be generated in `O(S+k)` time.
- No 400M-term training data, guessed substitutions, SAT, Z3, or high-memory Walnut search is needed for the main theorem.

### Explicit shift back to input `n` (no closure theorem required)

Let `W(p)` denote the state of any finite shifted DFAO on input `p`, so its output is `e_{p+1}`. Add a special initial state with output zero, whose zero transition is itself. For positive input prefix `n`, maintain the pair `(W(n-1),W(n))`, with output given by the first component. When a digit `r` is appended, the pair for `qn+r` is

- `(delta_{r-1}(W(n)), delta_r(W(n)))` if `r>=1`;
- `(delta_{q-1}(W(n-1)), delta_0(W(n)))` if `r=0`.

From the special initial state, a nonzero digit `r` enters `(W(r-1),W(r))`, which is determined by the initial shifted machine state and the one-digit transitions. This gives a finite automaton for `e_n` with `e_0=0`, with at most `1+S^2` states if the shifted machine has `S` states. The construction applies equally to the zero-coefficient window automaton in Section 9. It establishes the exact automaticity statement of the original conjecture without relying on an external shift-closure theorem. The exact minimal state count proved in Section 6 remains specifically the shifted count.

## 9. Extension to nonnegative coefficients (a separate theorem)

The archive's prompt says `a_i>=0`, while the original Fokkink–Joshi conjecture requires all `a_i>0`. Zero coefficients cannot be silently included in the positive theorem because the greedy construction may collide in the first block and the state-count classification uses strict positivity.

### Theorem 5 (admissibility and automaticity)

Let `k>=2` and `a_i` be nonnegative integers. Set `q=sum a_i` and `A_1^*=sum i*a_i`. The standard greedy construction of strictly increasing complementary positive A and B sequences is valid **if and only if**

\[
\boxed{A_1^*>k.}
\tag{31}
\]

For every such admissible vector, the discrepancy `e_n=A_n-(kq+1)n` is q-automatic. This section proves existence, boundedness and automaticity, but does not assert the positive-coefficient exact range and minimality formulas for zeros.

**Admissibility proof.** If `A_1^*<=k`, the initial B block is `1,...,k`; a positive `A_1^*` collides with it, while `A_1^*=0` violates positivity. Thus (31) is necessary. Conversely assume `A_1^*>k`, which implies `q>=2`. The first A term exceeds the first block. Inductively, all earlier A terms are strictly increasing and consecutive A gaps are at least `kq>=2k`, because each coordinate of consecutive B blocks increases by at least `k` and all weights are nonnegative. In the current B block, at most one earlier A term can lie strictly between its first and last B entries. Otherwise two consecutive earlier A terms in that interval would have at least `kq-1>=2k-1` intermediate integers not in the earlier A set. All would have to be current B entries, since mex chooses all unused integers in that interval; this is impossible for a block of `k` entries. Therefore the last B entry is at most the first plus `k`. From the second block onward the first B entry is at least `k+1`. The weighted sum is at least `q` times the first entry, hence strictly larger than the last entry. It also exceeds the preceding A term by at least `kq`. This completes the induction; mex gives disjointness, exhaustion, and uniqueness. □

Example inadmissible: `(2,0)` with `k=2` gives initial B block `(1,2)` and `A_1^*=2`. Example admissible: `(3,0)` with `k=2` gives `A_1^*=3` and a valid complementary construction. The case `(0,2)` is also admissible.

### 9.1. Symmetric contraction bound (completion of the archive's Step 1)

For an admissible vector, let `L=kq`, `K=L+1`, `J=sum (k-i)*a_i`, and put `G=KJ/L`. Choose

\[
C_0=\left\lceil\frac{kG+K}{k-1}\right\rceil.
\tag{32}
\]

We claim `|e_n|<=C_0` for all `n>=1`. Suppose it holds for all earlier indices and let `m` belong to the B block generating `A_n`. Write `x=B_m` and `N(x)=#\{j>=1:A_j<x\}`. All counted indices satisfy `j<n`; hence `x=m+N(x)<=kn+n-1<K n`. The induction hypothesis gives

\[
\frac{x-C_0}{K}-1\le N(x)\le\frac{x+C_0}{K}.
\]

For the lower bound, count positive `j<(x-C_0)/K`, all earlier than `n` because `x<K n`. The number of such integers is at least `(x-C_0)/K-1`; if the latter is negative, the inequality is automatic. For the upper bound, any counted `j` satisfies `Kj-C_0<x`. Substitute `N(x)=x-m` and rearrange:

\[
-\frac{C_0+K}{L}\le B_m-\frac{Km}{L}\le\frac{C_0}{L}.
\]

The weighted sum of the linear approximation yields `Kn-G`; the error is at most `q(C_0+K)/L=(C_0+K)/k`. Thus

\[
|e_n|\le G+\frac{C_0+K}{k}\le C_0.
\]

The proof is valid also at `n=1`, because no earlier positive A indices are counted and the lower-bound argument explicitly respects `j<n`. Strong induction proves boundedness. □

### 9.2. Exact inverse-rank window automaton (completion of the archive's Step 2)

Use (2)–(4) with `n-1=qp+r`, `z_i=kr+i`. Write `t(m_i)=p+u_i`; then `u_i` is uniquely determined by

\[
Lu_i+e_{p+u_i}<z_i\le L(u_i+1)+e_{p+u_i+1}.
\tag{33}
\]

The artificial zero `e_0=0` lies in the symmetric bound. By `1<=z_i<=L` and `|e_j|<=C_0`, these inequalities imply

\[
- U\le u_i\le U,\qquad U=\lceil C_0/L\rceil.
\tag{34}
\]

Indeed `u_i<(z_i+C_0)/L<=1+C_0/L` and `u_i>=(z_i-C_0)/L-1`; rounding the two integer bounds gives (34). For sufficiently large `p`, all candidate indices in (33) are positive. In the shifted sequence `x(p)=e_{p+1}`, the local rule for `x(qp+r)` uses only `x(p+u_i-1),x(p+u_i)`. Its value is `-T-r+sum a_i*u_i`, from (4).

Choose an integer radius `R` satisfying

\[
\lceil R/q\rceil+U+1\le R,
\]

which exists since `q>=2` (e.g. `R=2(U+1)` works). Set `P=R+U+2`. Use two types of states:

1. An exact small-index state for `0<=p<P`.
2. A window `(x(p-R),...,x(p+R))` for `p>=P`.

For a window state at index `p`, a child window at `qp+r` has entries `x(qp+r+h)` for `-R<=h<=R`. Divide `r+h=qs+r'` with `0<=r'<q`; then `|s|<=ceil(R/q)`. The local rule for each entry needs only parent offsets `s+u_i-1,s+u_i`, both within `[-R,R]` by the radius inequality. The choice of `P` ensures all candidate indices are positive. Thus every child window is determined by the current window and the digit. For exact states, a finite initial greedy prefix determines the transition, including the first window states: generating `qP+R+1` discrepancy values suffices. A window state never transitions back to a small-index state. There are at most `P+(2C_0+1)^(2R+1)` states. The output is the exact small-index value or the window center. This gives an explicit finite reachable automaton, correct by induction on the MSD input digits. □

This proof works without strict positivity once admissibility is established. It also gives an independent construction for cross-checking the sharper positive-coefficient theorem. See `rusty_exact.py` and `zero_coeff_verify.py`.

### Why not assert (25) for zeros?

The lower-bound argument for minimality distinguishes states by a strictly positive weight at a threshold. With zero coefficients, some adjacent first-coordinate thresholds can be indistinguishable, and distinct partial-block cases may coincide. The endpoint proof also uses strictly positive prefix and suffix weights. The admissibility/automaticity theorem above is safe; developing a sharp quotient for zero coefficients is a legitimate follow-on problem.

## 10. Reproducibility and archive audit

The companion ZIP contains standard-library Python code, the independent C checker, logs, and the 15 original automata. It does not include a compiled binary; build it locally. The Markdown research note is also supplied as a standalone file. Run the following from the extracted directory:

```bash
# Exact state count, full-range parameters, and reachable-state equality
python anti_exact_minimal.py 1 16 --check
python anti_exact_minimal.py 2 3 --check
python anti_exact_minimal.py 1 500 --check

# Compute A_n without computing earlier terms
python anti_exact_minimal.py 1 20 --index 1000000000000000000

# Emit Walnut DFAO (nonnegative stored outputs, offset = C)
python anti_exact_minimal.py 1 16 --walnut > RUSTY16.txt

# Exact state set, independent partition refinement and all archive equivalences
python anti_formula_verify.py

# Independent general-window comparison
python rusty_verify.py

# Admissible nonnegative coefficients
python zero_coeff_verify.py

# 90 million greedy terms compared to the constructed automata
cc -O3 -std=c11 -Wall -Wextra anti_stream_check.c -o anti_stream_check
python anti_stream_verify.py
```

Python API for random access:

```python
from anti_exact_minimal import Anti
m = Anti((1, 20))
print(m.C, m.H, m.state_count())
print(m.A(10**18))
print(m.B(10**18))
```

The 15 automata are under `rusty_work/automata/` in the companion archive so the equivalence script resolves its relative paths. The archive's raw outputs use an additive offset; the check normalizes each one using the known `e_1=-2`, rather than assuming all offsets are the same. A product traversal compares outputs for each reachable pair and all digit successors. It proves equivalence of the two finite machines on every word, conditional only on correctness of the parser and product traversal. Correctness of the constructed machine comes from the mathematical proof.

### Files in the original archive and what changed

| Original file | Assessment |
|---|---|
| `PROMPT_ALL_D.md` | Correct core direction; initial nonnegative scope needed a separate admissibility argument; exact indexing and closed radius were missing. |
| `RESULT.md` | Valuable computational baseline. Reported state counts were all independently reproduced and the DFAOs were compared by product traversal. Referenced Walnut logs are absent. |
| `manuscript.pdf` | Good finite-result starting point; the proposed new note replaces parameter-by-parameter proof with structural theorems. Do not claim the earlier verification was rerun. |
| `build3.py` | Learns block maps from finite generated data. Useful discovery tool, unnecessary for the proof. Empirical closure and finite-prefix agreement alone do not establish correctness. |
| `genc.c` | Fast bitset generator, but stores discrepancies in signed 8-bit format, which can overflow for large parameters. Our C checker uses signed 64-bit outputs and validates indices for the test sizes. |
| `walnut/*.txt` | Reproducible specifications for fixed parameters. We did not run Walnut in this session. |
| `automata/*.txt` | All 15 machines agree with the mathematically constructed shifted DFAO on every word after output normalization. |

The archive's formula `B^{(2)}_n=floor((A_n+2)/(d+1))` is useful for fixed-parameter Walnut verification, but it is not needed by the new proof. Our inverse-rank identity computes the entire B sequence directly and avoids assuming an a priori restriction on pair gaps.

### Computational limits and caveats

- The 10^7-term tests cover nine named forms, not every form or every parameter. Numerical evidence alone cannot certify universal statements.
- The independent window generator and minimal-pair generator share mathematical identities but are separate constructions. The C checker uses a direct greedy definition, not the local formula to generate A.
- Moore minimization is used as a cross-check of the exact minimality proof; it is not part of the proof's lower-bound argument.
- The Python greedy generator stores earlier A values in a set and is intended for modest checks. Use the C bitset checker for large prefixes. The C checker is an offline research utility, not hardened against arbitrary malicious input or astronomical allocations.
- No Lean build, Walnut executable run, or independent human mathematical review was completed here.
- No priority claim follows from search results. The earlier public proofs and their latest revisions require a careful audit before any submission.

## 11. Literature and novelty assessment

The following sources were found or inspected during Exa searches and a supplemental web search. Source claims are distinguished from mathematical work in this note.

1. Robbert Fokkink and Gandhar Joshi, *Anti-recurrence sequences*, [arXiv:2506.13337v1](https://arxiv.org/html/2506.13337v1), 16 June 2025. Journal version: *INTEGERS* 26 (2026), A24, [DOI:10.5281/zenodo.18305140](https://doi.org/10.5281/zenodo.18305140), [journal PDF](https://math.colgate.edu/~integers/aa24/aa24.pdf). Original precise conjecture is Conjecture 4 in the preprint and Conjecture 2 in the journal. Their A1-bounded theorem is Theorem 12 in the preprint and Theorem 4 in the journal. They explicitly identify the rusty-number problem. The original paper is included in the user's archive.
2. TrueTuring, [The whole positive coefficient anti-recurrence conjecture](https://www.trureturing.org/research/fokkink-joshi-whole-antirecurrence-automaticity/) and [proof blueprint](https://the-omega-institute.github.io/trureturing-mdbook/Blueprint/D5/S1/Recurrence/AntiRecurrenceAutomaticity.html). Claims a Lean-checked full positive-coefficient theorem via bounded discrepancy and local windows. Its public statement explicitly excludes minimal state counts, a uniform executable generator and runtime bounds from what is established there. I did not build its Lean source. This precludes a responsible unqualified novelty claim for the general automaticity theorem.
3. Larsen Cundric (experiment organizer), AI-generated draft *Linear anti-recurrence sequences are linear plus automatic*, [repository and v4 manuscript](https://github.com/LarsenCundric/ai-research-experiments/tree/main/papers/anti-recurrence). [Proof v2.1, dated 9 October 2026](https://raw.githubusercontent.com/LarsenCundric/ai-research-experiments/main/papers/anti-recurrence/artifact/docs/PROOF.md). The repository explicitly says the draft is not peer reviewed and the organizer has not independently verified the mathematics. Its older proof gives a box criterion, the bound `-kq<=e_n<=q-k`, a general two-term recurrence, a triple-state automaton, and empirical minimal counts for a few examples. It explicitly conjectures that the narrowest valid box equals the actual discrepancy range. Our Sections 2 and 4 derive exact endpoints and prove sharpness; Sections 5 and 6 give the full range and exact minimal shifted state count. I inspected the repository README and substantial older proof text, but did not fully audit the current v4 PDF or all associated code. Check whether these new exact results already appear in its latest revision before claiming novelty. Cite this draft for the two-term mechanism and the previously stated narrowest-box conjecture.
4. Jean-Paul Allouche and Jeffrey Shallit, *Automatic Sequences: Theory, Applications, Generalizations*, Cambridge University Press, 2003. Standard background on automatic sequences, uniform morphisms, kernels and fixed shifts. Consult the book for exact theorem numbers before using them in a manuscript.
5. Hans Zantema and Wieb Bosma, *Complexity of automatic sequences*, *Information and Computation* 288 (2022), 104710, [paper](https://www.sciencedirect.com/science/article/pii/S0890540121000250). Relevant framing of MSD and LSD state complexity. The minimality criterion used here is standard: reachability and pairwise distinguishability. [State complexity of reversals of DFAOs](https://arxiv.org/html/1705.07150v2) is also relevant to a possible LSD extension.

The source search was targeted to exact state counts, sharp discrepancy, existing general automaticity proofs, and two-term recurrences. It was not a systematic review of all citing literature, theses, OEIS comments, repository histories, conference proceedings, or unpublished work. The author of this note should not imply otherwise.

### What could be a publishable contribution?

| Result | Prior-art assessment from inspected sources | Present status |
|---|---|---|
| Full positive-coefficient automaticity | Already publicly claimed by at least two projects | Independent candidate proof here; cite prior work |
| Inverse-rank locality | Prior public proof uses it | Not a novelty claim |
| General two-term recursion | Explicit in earlier AI-generated draft | Not a novelty claim |
| Closed-form exact sharp range for every positive form | Earlier inspected proof conjectures sharpness of the optimal box | Candidate theorem, full argument in Sections 2 and 4 |
| All integers in range occur | Not found in inspected sources | Candidate theorem, Section 5 |
| Explicit minimal clipped-pair DFAO and state complexity for every positive form | Existing claims report selected sizes; no exact general formula found | Candidate theorem, Section 6 |
| Rusty period-three count | No prior proof found in targeted searches | Corollary of general theorem |
| Admissible-zero automaticity | Outside original conjecture and the cited strictly positive theorem statements | Candidate extension, Section 9; further literature needed |
| Random access to both A and B, constant digit-step arithmetic | Direct consequences of explicit rules | Useful computational contribution; novelty not established |

## 12. What I would do before submitting anything

### First priority: independently audit the proofs

The entire main argument is short enough for line-by-line review. Focus on these specific potential failure points:

1. **Indexing:** check every `n-1=qp+r` substitution and every occurrence of artificial `e_0=0`. Ensure it is not accidentally included in a range or gap assumption for positive indices.
2. **Strict rank inequalities:** `D_t<m<=D_{t+1}` rather than a version with both inequalities strict. Recheck the `-1` in the scalar floor identity (9).
3. **Integer fixed point:** the strict lower endpoint in `N-k^2<DC<=N` selects the smaller of two possible solutions; a rounding error changes the sharp range.
4. **Box induction:** verify that every index used for the lower rank estimate is below `n`, including `p=r=0`. This is why the condition `H>=-L+k` matters.
5. **Sharpness:** (1) must not be applied to `e_0,e_1`. Check both cases `h>=1` and `h<=0` separately, and why the appropriate argument of `F_r` can be replaced without changing its output.
6. **State reachability:** verify the reset `00`, the full interval proof, and each witness parent `-k(j+T)-t`. Do not replace reachability with an observed transition graph.
7. **Lower bound:** all coefficients are strictly positive, so an active minus threshold strictly changes a one-digit output; this is the key to minimality and why the zero case is separate.
8. **Zero extension:** the gap argument for at most one earlier A inside a B block is inductive; verify that no B entries from past blocks occur above the current first B entry, and no future A are used in the greedy selection.

If all these survive independent review, a full mathematical manuscript can center on the exact state-complexity theorem. If a flaw is found, isolate the affected statement rather than discarding the entire project. In particular, the exact window construction is an independent fallback for automaticity.

### Second priority: prior-art audit and responsible attribution

Read the current Larsen Cundric v4 manuscript and the TrueTuring Lean theorem in full. Search citing literature, repository commits, mathematical forums, and the relevant authors' pages for exact ranges, pair-state minimization, and state-complexity formulas. A public timestamp alone does not prove correctness or priority. Contact the original authors only after understanding the argument and writing a concise independent note. Disclose AI-assisted derivation and checks in accordance with the target venue's authorship and disclosure policies. Do not present generated proofs as independently human-verified.

Suggested manuscript title: **Exact discrepancy and state complexity of linear anti-recurrence sequences**. A possible organization: (1) background and prior automaticity claims, (2) inverse-rank representation, (3) exact bounds and sharpness, (4) canonical minimal machine, (5) rusty-number formula, (6) optional zero extension and computational consequences. This is more substantive than the original parameter-bounded paper.

### Further research directions, ranked

1. **Formal verification of the new exact theorems.** Formalize Lemmas 1–2, floor identities, bound invariant, sharpness, synchronizing automaton, reachable family classification, and pairwise distinguishability. The prior Lean development may offer usable definitions and lemmas, subject to license and attribution. A formal proof of exact state complexity would substantially improve credibility.
2. **Sharp state complexity for nonnegative forms.** Extend the clipped-pair idea by grouping thresholds corresponding to positive coefficients, including the effect of zero prefix/suffix weights. Start with vectors with one zero and sparse one-coordinate forms. The general window construction supplies exact answers to guide conjectures.
3. **Unshifted and LSD state complexity.** The present formula is for shifted MSD input. Determine exact counts for `e_n` with `e_0=0`, and for the reversed input direction (finite kernel). The universal `00` reset may help but does not by itself settle these variants. Avoid mixing conventions when comparing counts.
4. **Frequency and distribution.** The explicit substitution gives a finite transition matrix. Compute exact limiting output frequencies and, if they exist, average discrepancy, using the digit-uniform Markov chain. The reset implies a unique reachable communicating class, since each state can return to the start and the start reaches every state. The initial self-loop makes it aperiodic. Thus for uniformly sampled base-q words of increasing fixed length, convergence follows; extension to all arbitrary prefix lengths requires a separate argument.
5. **First-occurrence lengths and rare extrema.** BFS on the explicit minimal automaton yields shortest digit words reaching any output. Lexicographically smallest among shortest canonical words gives the first index. This directly addresses the famous `d=4` failure at `p=348` and gives exact rare-event certificates for all parameters.
6. **Parameter families and asymptotic geometry.** Formula (26) is piecewise quasi-polynomial under affine parameter families. Analyze the normalized state-count surface on the coefficient simplex; characterize when `H<=0` and when each partial-block family appears. This offers systematic classifications beyond the rusty case.
7. **Other complementary constructions.** Investigate variable block lengths, signed coefficients, or nonhomogeneous forms only after proving existence and monotonicity. The original inverse rank identity holds for any increasing complementary pair, but contraction, sharp bounds, and locality depend on the recurrence and cannot simply be assumed.

The concrete next step is not to send another prompt asking an AI to guess the all-d theorem. It is to read Sections 2–6, reproduce the scripts, and independently attack the proof at the eight points above. The central deliverable is an exact candidate theorem already written down with both upper and lower bounds, not a suggestion to keep extrapolating.
