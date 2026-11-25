# Audit of the exact-discrepancy paper (25 Nov 2026)

Each risky point from the research note, checked by hand while rewriting the proofs:

1. **Indexing** (n-1 = qp+r, m_i = Lp + kr + i): re-derived Lemma 3 (balance identity) from scratch. OK.
2. **Artificial e_0 = 0**: used only in the local rule at p = 0 and in the automaton's initial state. It is never counted in the range or in the gap inequality (which is stated for n >= 1). OK.
3. **Floor identity / smallest fixed point**: (N-k^2, N] contains DC iff c is a fixed point, and the least solution is floor((N-1)/D). Re-derived. OK.
4. **Box induction**: every j used in the lower rank bound is < n, including p = r = 0 (via H >= -L+k). OK.
5. **Sharpness**: the gap inequality is applied only to positive indices. The cases h >= 1 and h <= 0 are separated. The reverse inequalities now come directly from monotonicity (we tightened the wording in the paper). OK.
6. **Reachability**: the 00 reset, and witness parents -k(j+T) and -k(j+T)-t, with the digit range checked to be in [1, q-1]. OK.
7. **Minimality**: one digit separates states with equal output, using a_i > 0. OK.
8. **Zero coefficients**: admissibility induction and contraction bound re-derived. The window radius gives offsets in [-2U-2, 2U+1], inside [-R, R]. OK.

Fixed while writing: the H<0 envelope case (later blocks are >= 1-T, not > 0), and the window-offset bookkeeping in the zero section.

## Computer checks (independent code in checks/)
- checks/v.py: automaton vs brute-force greedy, 170 forms x 20,000 terms: 0 mismatches.
- checks/v2.py: exact range + state count vs reachable set and Moore minimisation, 1,134 forms: 0 mismatches.
- checks/z.py: admissibility rule, 436 zero vectors: 0 mismatches.
- Walnut-minimised RUSTY automata d=1..15 have 2,3,6,9,11,16,19,21,26,29,31,36,39,41,46 states, which equals the formula.
- code/: the original research code and logs (including a C check with 10^7 terms on 9 forms).

Not done: no formal (Lean) verification, and no referee yet.
