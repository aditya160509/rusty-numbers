# Literature check (25 Nov 2026)

- It claims the same Main Theorem: for every positive form with k >= 2, A_n - kappa*n is tau-automatic, with -k*tau <= A_n - kappa*n <= tau - k (sharper than our 2*kappa).
- Same method: a discrepancy bound, then a two-term recursion d(tau*q + r + 1) = G_r(d(q), d(q+1)), then an explicit automaton. It also explains the n = 348 break for d = 4, gives a Walnut proof for (1,4), and runs computations on 746 forms.
- It is not refereed, and its author says he has not verified the mathematics.

Other sources checked:
- Fokkink-Joshi, Integers 26 (2026) A24 (journal version, Jan 2026): still lists the conjecture and the rusty numbers as open.
- Kimberling-Moses 2019: growth rates only, no boundedness.
- Bosma et al. 2025: special cases only.
- GitHub the-omega-institute/trureturing issue 17371 (15 Oct 2026): a preregistered attempt, with no proof.
- OpenAI "Ten Advances" (Aug 2026): unrelated.

**Conclusion:** our all-forms proof is independent but NOT first (about 6 weeks later). Present it as an independent proof or verification and cite Cundric/Grok. Our d <= 15 Walnut proofs and the exact match between the proof-built automata and the Walnut automata are useful independent confirmation.
