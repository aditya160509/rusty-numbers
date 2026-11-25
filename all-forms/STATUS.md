# STATUS: anti-recurrence / rusty numbers (25 Nov 2026)

## Claimed as proved (full written proof in `note/anti_recurrence_all_forms.pdf`)
For **every positive linear form a = (a_1..a_k), k >= 2, all a_i >= 1** (exactly the setting of Fokkink-Joshi):
1. **Weak conjecture.** A_n - kappa*n is bounded; explicitly |A_n - kappa*n| <= ceil(k*kappa/(k-1)) <= 2*kappa. (Theorem 3)
2. **Clergyman's conjecture.** A_n - kappa*n is tau-automatic. (Theorem 7)
3. **Rusty numbers:** for **every d >= 1**, A_n - (2d+3)n is (d+1)-automatic. This answers both open questions in FJ §5.

Proof outline:
- B_M = M + N(B_M), with N(x) = #{j : A_j < x} (B is the complement of A).
- A_n > B_{kn}, so the B's of block n only "see" A_1..A_{n-1}.
- Contraction: the bounds on e_n are those on e_j (j < n) divided by k. Strong induction, no separate base case.
- Locality: in the counting identity for B at index k(tau*m + r - 1) + i, the kappa*m terms cancel because kappa - 1 = k*tau. This gives e_{tau*m+r} = F_r(e_m, e_{m+1}) in all computed cases; the proof allows any finite window.
- Window lemma: such a recursion on a finite alphabet gives a msd DFAO.

## Status of the claim
- The proof is written out step by step and was re-checked by hand. It is **not refereed**, and no one outside this project has read it.
- No Walnut is needed for the general theorem. The Walnut runs for d <= 15 are independent corroboration.

## Numerical checks (not part of the proof; they test that constants and rule are derived and implemented correctly)
| check | scope | result |
|---|---|---|
| proved bound [-L,U] contains the data | d = 1..15, 20, 30, 50; (2,3), (3,1), (5,1), (1,1,1), (3,1,2), (2,5,1), (1,1,1,1), (1,2,3,4) | all contained; bound tight or within 1-2 of the observed extremes |
| local rule F_r reproduces e_n | same forms, about 2x10^5 terms each | 0 mismatches |
| DFAO built from F_r alone (plus a finite prefix) reproduces e_n | same forms, 3x10^5 to 2x10^6 terms | 0 mismatches |
| that DFAO is language-equivalent to the Walnut automaton | d = 1..15 (RUSTYB..RUSTYP) | equivalent in all 15 cases |

Logs: `logs/log_rusty_1_4.txt` (d=1, d=4), `logs/log_rusty_2_15.txt`, `logs/log_general.txt`.

## What failed or changed along the way
- The earlier empirical claim that the window size k(d) grows with d was an artifact of how the blocks were aligned. With the alignment n = tau*m + r, the window is always (e_m, e_{m+1}).
- The attachment allowed a_i >= 0; the proof needs a_i >= 1 (it uses A_n > B_{kn}). FJ also assume a_i > 0.
- k = 1 is excluded (no contraction). FJ also exclude it.

## Gaps and risks
- **Not refereed.** The highest-risk steps are the lower bound for N(x) in Prop. 2 (the condition U >= -1 - k(tau-1) and the claim that only j < n is counted) and the index bookkeeping in Lemma 6. Have an expert check these first.
- A public GitHub issue (the-omega-institute/trureturing #17371, about 40 days old) preregisters an attempt on exactly this conjecture. I could not open it (GitHub rate-limited the page; the repo is not accessible from this session). Check it for priority before posting.
- The literature search (FJ Integers 2026, Bosma et al. JIS 2025, the OEIS conjecture entries) found no prior proof of boundedness or automaticity for general forms. The Utrecht anti-k-nacci thesis could not be located.

## Files
- `note/anti_recurrence_all_forms.tex|pdf`: the note
- `scripts/proof.py`: computes the constants, checks the bound and the local rule, builds and minimises the DFAO from F_r, checks equivalence with a Walnut automaton
- `scripts/gena.c`: generator for any form (int16 output)
- `logs/`: outputs
