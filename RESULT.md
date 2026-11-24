# Rusty numbers are linear + automatic (proved with Walnut)

**Open problem.** Fokkink & Joshi, *Anti-recurrence sequences* (arXiv 2506.13337, §4–5) ask whether the "rusty numbers", the anti-recurrences for the linear form a = (1,d), satisfy the Clergyman's conjecture: is A_n − κn automatic, where κ = kτ+1? They call this "a challenge to prove, or disprove". For d = 4 the progression A_{5n+1} = 9 + 55n breaks at n = 348. The form (1,d) is not A₁-bounded for d ≥ 3, so their Theorem 12 does not apply.

## Theorem (proved)

For d = 1, …, 8 and d = 11, with A_n = B_{2n−1} + d·B_{2n} and B the complement of A taken blockwise by mex:

| d | κ = 2d+3 | A_n − κn is | msd DFAO states | Automaton | Log |
|---|---|---|---|---|---|
| 1 | 5 | 2-automatic | 2 | `automata/RUSTYB.txt` | `logs/walnut_rusty1.log` |
| 2 | 7 | 3-automatic | 3 | `automata/RUSTYC.txt` | `logs/walnut_rusty2.log` |
| 3 | 9 | 4-automatic | 6 | `automata/RUSTYDTHREE.txt` | `logs/walnut_rusty3.log` |
| 4 | 11 | 5-automatic | 9 | `automata/RUSTYD.txt` | `logs/walnut_rusty4.log` |
| 5 | 13 | 6-automatic | 11 | `automata/RUSTYF.txt` | `logs/walnut_rusty5.log` |
| 6 | 15 | 7-automatic | 16 | `automata/RUSTYG.txt` | `logs/walnut_rusty6.log` |
| 7 | 17 | 8-automatic | 19 | `automata/RUSTYH.txt` | `logs/walnut_rusty7.log` |
| 8 | 19 | 9-automatic | 21 | `automata/RUSTYI.txt` | `logs/walnut_rusty8.log` |
| 11 | 25 | 12-automatic | 31 | `automata/RUSTYL.txt` | `logs/walnut_rusty11_4g.log` |

d = 1 (anti-Fibonacci) and d = 2 (anti-Pell) were already known and serve as controls. **New: d = 3, 4, 5, 6, 7, 8, 11.** Peak memory ≤ 0.71 GB except d = 11 (2.7 GB).

So the conjecture holds for these rusty numbers. For d = 4, one state of the automaton is first reached at prefix 348, which explains the "break" at n = 348.

## Proof method (same as Fokkink–Joshi, Theorem 5)

The automaton gives a candidate A (as κn + output − offset), B²_n = ⌊(A_n+2)/(d+1)⌋ and B¹_n = A_n − d·B²_n. Walnut checks that the candidate satisfies the defining construction:

1. `total`: A, B¹, B² are defined for every n ≥ 1
2. `init`: B¹_1 = 1, B²_1 = 2, A_1 = 1+2d
3. `order`: B¹_n < B²_n < B¹_{n+1} (so the B's are distinct and increasing)
4. `b1_new`, `b2_new`: B¹_n and B²_n are not earlier A's
5. `mex_b1`: every t < B¹_n is an earlier A, B¹ or B² (so B¹_n is the mex)
6. `mex_b2`: every t strictly between B¹_n and B²_n is an earlier A (so B²_n is the next unused number)
7. `sum`: A_n = B¹_n + d·B²_n

Together these say that the candidate follows the mex recursion, which determines the sequence uniquely (their Lemma 3). By induction on n, the candidate equals the true anti-recurrence. **Walnut printed TRUE for all 8 statements in each case**; see `logs/walnut_rusty4.log`, `logs/walnut_rusty5.log`, `logs/walnut_rusty6.log` (raw output in `*.log.raw` for 5 and 6). The scripts are `rusty4.txt`, `rusty5.txt`, `rusty6.txt`.

## How the automata were found (heuristic; the proof does not depend on it)

- `anti.c` generates d(n) = A_{n+1} − κ(n+1); its output matches an independent Python implementation (`anti.py`) on 2M terms.
- `infer_msd.py` builds the msd automaton by Myhill–Nerode merging, then validates it against all 400M generated terms (streamed in 1M-term chunks). This was TRUE for d = 4, 5, 6.
- lsd/kernel counts (`infer.py`, `kern.py`, `depth.py`) grew slowly. The msd representation is the compact one.

## Reproduce

Walnut 6 (github.com/firetto/Walnut), compiled with `javac` against fastutil 8.5.12 and dk.brics automaton 1.12-4. Copy `automata/RUSTY?.txt` into `Word Automata Library/` and `rusty?.txt` into `Command Files/`, then run `load rusty4.txt;`. Run Java with `-Xmx4g` for d = 11.

## Not done

- d = 9, 10 and d ≥ 12: no automaton extracted from 10⁸ terms (states appear very late). A conjectured k-block substitution structure for d ≤ 30 is in `RESULT.md`.
- The general (1,d) family for all d, and the full Clergyman's conjecture: open.
- No independent check by the paper's authors yet.
