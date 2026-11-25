# Anti-recurrence sequences are linear plus automatic

**Aditya Balaji**, 25 November 2026. A preprint; it has not been refereed.

This repository answers the questions of Fokkink and Joshi ("Anti-recurrence sequences", *Integers* 26 (2026) A24, [arXiv:2506.13337](https://arxiv.org/abs/2506.13337)).

| | Result | Where |
|---|---|---|
| **Main paper** | For every positive linear form a = (a_1, ..., a_k) with k >= 2, A_n - kappa*n is bounded and tau-automatic (the Clergyman's conjecture). In particular, for every d the rusty numbers satisfy: A_n - (2d+3)n is (d+1)-automatic. | [`all-forms/anti_recurrence_all_forms.pdf`](all-forms/anti_recurrence_all_forms.pdf) (5 pages) |
| **Walnut certificates** | Machine proofs for the rusty numbers d = 1, ..., 15 (8 first-order statements each, the method of Fokkink-Joshi Thm. 5) | [`paper/manuscript.pdf`](paper/manuscript.pdf), `automata/`, `walnut/`, `logs/` |
| **Cross-check** | For d <= 15, the automata built from the general proof are equivalent to the Walnut-certified ones | `all-forms/logs/` |

**Prior work.** The same main theorem, by a closely related argument, appears in an unrefereed AI-generated manuscript by L. Cundric dated 11 Oct 2026 ([link](https://github.com/LarsenCundric/ai-research-experiments)). We found it only after finishing. Our proof is independent, and the two together give a second confirmation. See [`all-forms/LITERATURE.md`](all-forms/LITERATURE.md).

## Short version of the proof
1. B_M = M + #{j : A_j < B_M}, because B is the complement of A.
2. If |A_j - kappa*j| is bounded for j < n, the counting identity bounds A_n - kappa*n with the error divided by k. So the error contracts, and |A_n - kappa*n| <= 2*kappa.
3. The same identity shows that A_{tau*m+r} - kappa*(tau*m+r) is a fixed function of a bounded window around m. The kappa*m terms cancel because kappa - 1 = k*tau.
4. A finite-window recursion of this kind gives a tau-automaton.

## Reproduce
- General proof checks: `cd all-forms/scripts && cc -O2 -o gena gena.c && python3 proof.py 300000 1 4 --cmp ../../automata/RUSTYD.txt 6` (needs numpy).
- Walnut certificates: copy `automata/RUSTY*.txt` into Walnut's `Word Automata Library/` and `walnut/rusty*.txt` into `Command Files/`, then run `load rusty4.txt;`. d = 15 uses the equivalent split statements `rusty15b.txt` and `rusty15c.txt` (Walnut's alphabet limit). See `RESULT-d15.md`.

## Disclosure
The work was developed with AI assistance (Anthropic's Claude and the research assistant Astra). The author checked the results and is responsible for the content.
