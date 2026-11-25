# Exact discrepancy and state complexity of anti-recurrence sequences

**Aditya Balaji**, independent researcher, 25 November 2026. Preprint, not refereed.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24528659.svg)](https://doi.org/10.5281/zenodo.24528659)

This repository answers and extends the questions of Fokkink and Joshi ("Anti-recurrence sequences", *Integers* 26 (2026) A24, [arXiv:2506.13337](https://arxiv.org/abs/2506.13337)).

| | Result | Where |
|---|---|---|
| **Main paper (v2)** | For every positive form: the **exact range** of A_n - kappa*n (closed formula, sharp, with every value attained), proving Cundric's "narrowest box" conjecture; and the **exact minimal automaton** with its state count. For the rusty numbers: 10m-4, 10m-1, 10m+1 states for d = 3m, 3m+1, 3m+2. Also: exactly which forms with zero coefficients work, and that they are automatic too. | [`exact/paper/exact_anti_recurrence.pdf`](exact/paper/exact_anti_recurrence.pdf) (7 pages) |
| **Audit and checks** | Hand audit of every risky step; independent checks on 1,134 forms; zero mismatches | [`exact/AUDIT.md`](exact/AUDIT.md), `exact/checks/`, `exact/code/` |
| **Walnut certificates** | Machine proofs for the rusty numbers d = 1..15. Walnut's minimised automata have exactly the predicted state counts. | [`paper/manuscript.pdf`](paper/manuscript.pdf), `automata/`, `walnut/`, `logs/` |
| **Earlier note (v1)** | An independent proof of automaticity for all positive forms | [`all-forms/anti_recurrence_all_forms.pdf`](all-forms/anti_recurrence_all_forms.pdf) |

**Prior work.** Automaticity for all positive forms was claimed first by L. Cundric (unrefereed AI-generated manuscript, Oct 2026, [link](https://github.com/LarsenCundric/ai-research-experiments)), who also gives the two-term recursion. It was later claimed in Lean by [TrueTuring](https://www.trureturing.org/research/fokkink-joshi-whole-antirecurrence-automaticity/). The exact range, the full-range statement and the minimal state counts are new here, as far as we know. See [`all-forms/LITERATURE.md`](all-forms/LITERATURE.md).

## Short version of the v1 proof
1. B_M = M + #{j : A_j < B_M}, because B is the complement of A.
2. If |A_j - kappa*j| is bounded for j < n, the counting identity bounds A_n - kappa*n with the error divided by k. So the error contracts, and |A_n - kappa*n| <= 2*kappa.
3. The same identity shows that A_{tau*m+r} - kappa*(tau*m+r) is a fixed function of a bounded window around m. The kappa*m terms cancel because kappa - 1 = k*tau.
4. A finite-window recursion of this kind gives a tau-automaton.

## Reproduce
- v2 checks: `cd exact/checks && python3 v2.py` (exact range + state counts, about 1 minute) and `python3 v.py 20000` (against brute force).
- General proof checks: `cd all-forms/scripts && cc -O2 -o gena gena.c && python3 proof.py 300000 1 4 --cmp ../../automata/RUSTYD.txt 6` (needs numpy).
- Walnut certificates: copy `automata/RUSTY*.txt` into Walnut's `Word Automata Library/` and `walnut/rusty*.txt` into `Command Files/`, then run `load rusty4.txt;`. d = 15 uses the equivalent split statements `rusty15b.txt` and `rusty15c.txt` (Walnut's alphabet limit). See `RESULT-d15.md`.

## Disclosure
The work was developed with AI assistance (Anthropic's Claude and OpenAI's Codex). The author checked the results and is responsible for the content.
