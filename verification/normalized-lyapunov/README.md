# Exact verifier: normalized Lyapunov map

Companion to [`docs/normalized-lyapunov/`](../../docs/normalized-lyapunov/). Run:

```bash
./run_all.sh
```

Expected output ends with `ALL SECTIONS: 144 / 144 checks passed`. Runtime is a few minutes;
peak memory is a few tens of MiB.

**Python standard library only** — no numpy, sympy, mpmath or scipy (none is installed on the
machine this was written on). All arithmetic is exact `fractions.Fraction`; floats appear only
inside printed diagnostics, never in a pass/fail decision. Damping rates are chosen to be
perfect squares so that `c_ij = 2*sqrt(a_i*a_j)/(a_i + a_j)` is itself rational.

| file | checks | content |
|---|---|---|
| `verify.py` | 24 | closed forms for `S_H`, `Phi_H`; unitality, trace preservation, complete positivity, non-positive inverse; the two-mode square defect and determinant identity; **agreement with the repository's `volume` and `volume0` at 25 exact `(k,r)` pairs**; the exact-preservation classification; the trace identity and commutator sandwich; `det Phi_H(Q) >= det Q`; the Hadamard ceiling |
| `threemode2.py` | 9 | three-mode path Laplacian: eigenbasis determinant vs. an **independent** original-basis Lyapunov solve; `ratio(0) = 1`; the exact slope `-tr L`; certified expansion witnesses; `Theta(k^-2)` decay with its derived constant |
| `threshold3.py` | 4 | two-sided certification of the three-mode brackets — exact rational witness on the expansion side, subdivided-Bernstein positivity certificate on the other |
| `controls6.py` | 11 | discriminating controls: `k = 0`; `r = 1`; `r` below/above `3+2*sqrt(2)`; `[H,Q] = 0`; self-adjoint off-diagonal witness; repeated damping rates; identical `spec(Q)` with different orientation; singular `H` as an excluded-domain control |
| `interp15.py` | 11 | the per-component necessary cost on matching patterns: the per-block numerator identity and coefficientwise domination `N <= (det Q) rho_inf B` across six matching instances, monotonicity of `q_m` at eleven rate configurations, the `eta > 8` endpoint, the three-block floor table, and the enlarged `5/3x` parameter boxes |
| `boxes14.py` | 10 | the sufficient box criterion: monotonicity of `g`, the nominal `k = 4, 5` families with Descartes saturated, all eleven box bounds by exact rational envelope arithmetic, corner spot-checks, the merge correction under `b_j -> 10 b_j`, and the band constraint for `c < k` |
| `cost13.py` | 10 | the necessary cost bound for attaining `c = k`: the closed form against the coefficient ratio at four rate triples, `rho_inf = rho` for disjoint `(0,a)` blocks, the exact floor `T = 400400440125.444004...`, the forced `b_3 > 3334.538168...`, the exclusion at `eta_3 = 11000000` (sign count 6 -> 4), the non-optimality at `k = 1`, and the two halving conventions |
| `sharp12.py` | 11 | sharpness of the component bound at `k = 3`: the three-disjoint-block construction, the product form with every `Sigma` checked against `H S + S H = Qt`, the seven exact alternating evaluations, the tight `2k = 6` sign pattern via an independent polynomial route, the connected weighted-graph realization with eigenvalues verified by applying the Laplacian to explicit eigenvectors, and a control showing sharpness is attainment rather than determination |
| `components11.py` | 12 | the component-count theorem: `B*det(C o Qt)` is a polynomial of degree `<= 2k`, the numerator identity against independent Lyapunov solves, `A(0) = -4^k (det Q)(tr L)`, the nonpositive tail, sign-variation and component counts across `n = 2..5`, `k = 0..5`; plus the round-4 corrections (non-additivity, star patterns, saturation scale `2/s`, the `r = 9` peak, commuting-noise monotonicity) and the `k = 3` linear reduction |
| `multipair10.py` | 11 | the two-pair counterexample refuting the general interval conjecture: positive definiteness, the vanishing cycle term, the ratio against independent Lyapunov solves, the three exact evaluations, disconnectedness, the component count, the effect of zeroing either correlation, the connected weighted-triangle realization, the corrected `7.5x` diagnosis, and the interval-vs-unimodality distinction |
| `singlepair9.py` | 11 | the single-correlated-pair theorem: the exact ratio against independent Lyapunov solves at `n = 2,3,4`, the `Delta = 0` case, the normal form with exact coefficient reconstruction, uniqueness of the onset coupling with `deg = rank L + 1`, the floor `eta_crit >= 8`, both repository models as instances, and an interval test outside the covered class |
| `review8.py` | 14 | reviewer corrections and the Oppenheim-Schur refinement: the exact derivative at `k = 1` (so `k = 1` is **not** volume-maximizing), `Theta(k^-rank L)` decay at ranks 1/2/3, `det C` by the Cauchy formula, the refinement `det(C o Qt)/det Qt >= 1 + det C (rho - 1)` with its measured overshoot against the certified thresholds, and the centre-node closed form with its cubic for `k_*` |
| `priorart7.py` | 6 | controls backing the prior-art classification (infinite divisibility of `C`; multiplicative domain = commutant of `H`, 193 608 instances; Oppenheim and Schur determinant bounds with the equality condition) and the two-sided sandwich |

`threemode.py` is exploratory scratch (the grid survey that located the three-mode crossings
before they were certified). It is deliberately **not** in `run_all.sh`: its `max over a grid`
output is a lower bound on the supremum and proves nothing by itself.

## Conventions

* `ratio = det Sigma_k / det Sigma_0` and `det Sigma_0 = det Q / 2^n` — the normalizing power is
  the **dimension**, not a constant. `ratio_of` in `controls6.py` reads `n` off the matrix.
* "PROVED" in the output means a certificate was produced (exact witness, or a positivity
  certificate), never that a finite grid found nothing.
