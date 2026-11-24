# Rusty numbers are linear + automatic (proved with Walnut)

**Open problem.** Fokkink & Joshi, *Anti-recurrence sequences* (arXiv 2506.13337, §4–5) ask whether the "rusty numbers", the anti-recurrences for the linear form a = (1,d), satisfy the Clergyman's conjecture: is A_n − κn automatic, where κ = kτ+1? They call this "a challenge to prove, or disprove". For d = 4 the progression A_{5n+1} = 9 + 55n breaks at n = 348. The form (1,d) is not A₁-bounded for d ≥ 3, so their Theorem 12 does not apply.

## Theorem (proved)

For every d = 1, …, 15, with A_n = B_{2n−1} + d·B_{2n} and B the complement of A taken blockwise by mex:

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
| 9 | 21 | 10-automatic | 26 | `automata/RUSTYJ.txt` | `logs/walnut_rusty9_dl.log` |
| 10 | 23 | 11-automatic | 29 | `automata/RUSTYK.txt` | `logs/walnut_rusty10_dl.log` |
| 11 | 25 | 12-automatic | 31 | `automata/RUSTYL.txt` | `logs/walnut_rusty11_4g.log` |
| 12 | 27 | 13-automatic | 36 | `automata/RUSTYM.txt` | `logs/walnut_rusty12_dl.log` |
| 13 | 29 | 14-automatic | 39 | `automata/RUSTYN.txt` | `logs/walnut_rusty13_dl.log` |
| 14 | 31 | 15-automatic | 41 | `automata/RUSTYO.txt` | `logs/walnut_rusty14_dl.log` |
| 15 | 33 | 16-automatic | 46 | `automata/RUSTYP.txt` | `logs/walnut_rusty15_8g.log` + `15b`, `15c` (see note) |

d = 1 (anti-Fibonacci) and d = 2 (anti-Pell) were already known and serve as controls. **New: d = 3 to 15.** Peak memory up to 8 GB for d = 15.

Note on d = 15: Walnut hit its input-alphabet limit on `order` and `mex_b2` (base 16, 4+ variables). They were checked in equivalent split form: `order` as B¹ₙ<B²ₙ and B²ₙ<B¹ₙ₊₁ (`rusty15b.txt`); `mex_b2` via helpers lo(n,t)=∃u B¹ₙ=u<t, hi(n,t)=∃s t<s=B²ₙ, ea(n,t)=∃m<n Aₘ=t (`rusty15c.txt`). Since B¹, B² are functions (by `total`), these are equivalent to the originals. All TRUE.
Automata for d = 9, 10, 12–15 were built by `build3.py` from the k-block substitution (supplied externally); the Walnut proof does not depend on how they were found.

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

- d ≥ 16: not attempted. Walnut base-17+ will need the split form throughout and more memory.
- The general (1,d) family for all d, and the full Clergyman's conjecture: open.
- No independent check by the paper's authors yet.
