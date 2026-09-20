# Palindromic Covariance Determinants and Reciprocal Thresholds in Two-Mode Linear Ornstein–Uhlenbeck Systems

Elias De Jesús — Independent Researcher — ORCID [0009-0007-0190-9143](https://orcid.org/0009-0007-0190-9143)

Self-contained source package for the manuscript. September 2026.

## What the paper proves

Let a stable linear Ornstein–Uhlenbeck system have a **symmetric** drift whose
restriction to a two-dimensional invariant subspace has relaxation rates
`D1, D2 > 0`, and let `Sigma` be its stationary covariance. For an **arbitrary**
symmetric forcing `Q` on that subspace,

```
4 D1 D2 det Sigma = det Q + nu^2 Q12^2 ,    nu = (D1 - D2)/(D1 + D2)
```

This identity is **not claimed**: it is the 2x2 Hadamard-product determinant
expansion behind Oppenheim's inequality, applied to the Cauchy matrix
`C_ij = 1/(D_i + D_j)`, with the remainder written out (Horn & Johnson,
*Matrix Analysis*, 2nd ed., Thm. 7.8.16, eq. (7.8.17), p. 509).

Along the affine family `Q(tau) = q_b I + (tau - 1) H`, with `H` symmetric of
**any rank**, the determinant is quadratic in `tau`, and the main result is:

```
4 D1 D2 det Sigma(tau)  is palindromic in tau   <=>   tr H = q_b
```

The criterion is an **involution**. The complementary forcing `H* = q_b I - H`
satisfies `tau * Q_H(1/tau) = Q_{H*}(tau)` unconditionally, and
`tr H* = 2 q_b - tr H`, so the trace-normalized forcings are exactly the class
*closed* under the reciprocal transform, and on that class the coefficient
`K = det H + nu^2 H12^2` is preserved. Closure is not fixedness: the only fixed
point is the isotropic `H = (q_b/2) I`. On a rank-one `H = q_b e e^T` the
involution is the exchange `e <-> e_perp`, so the familiar rank-one
"self-duality" is a specialization of the trace criterion, not a second
mechanism.

Palindromicity then *forces* the reciprocal coordinate `w = tau + 1/tau`: the
normalized determinant is exactly affine in `w`, which yields an exact
generalized-variance threshold, minimizable over a coupling strength. Graph
corollaries: `K2` -> `34`, `P3` (centre) -> `35 + 15*sqrt(5)`, `K3` -> `247/2`.

**Scope.** `tau` is a ratio of forcing **variances**, not amplitudes; conflating
them misreports a constant by a square. The identity is algebra and holds for
any symmetric `H` and any real `tau`; the stochastic reading needs `H` positive
semidefinite with `tr H = q_b`, which keeps `K >= 0` and `Q(tau)` positive
definite for every `tau > 0`. With three *distinct* active rates the response is
generically cubic, so the closure is tied to having two.

## Contents

| file | |
|---|---|
| `main.tex` | the manuscript source |
| `main.pdf` | compiled, 25 pages, letter |
| `references.bib` | self-contained bibliography, 33 entries, all cited |
| `figures/fig1–3.pdf` | active-plane schematic; affine determinant; threshold curves |
| `manuscript_checks.py` | 126 exact symbolic checks (SymPy) |
| `make_figures.py` | regenerates the figures from the exact formulas |
| `build.sh` | build script |
| `BUILD_INSTRUCTIONS.md` | how to build and verify, with expected output |
| `LICENSE-NOTE.md` | licensing of the manuscript and of the code |
| `SHA256SUMS.txt` | digests of every file above |

Nothing here references a path outside this directory. `main.tex` reads the
`references.bib` beside it, not a repository-level master file.

## Repository and verification

- Repository: <https://github.com/innerlightr-wq/ou-threshold-lean>
- Branch: `generalize-palindromic-determinant`
- Lean formalization: `OUCorridor/ActivePlaneGeneral.lean`
- Frozen verification snapshot: `verified/palindromic-generalization-2026-09/`

The snapshot holds the exact sources, the environment, the build transcript and
the axiom audit: Lean 4.33.1, mathlib pinned at
`0df444a360eaa60ab8c11dca51a86af692955474`, build completing in 8716 jobs, **28
audited theorems** depending only on `propext`, `Classical.choice` and
`Quot.sound`, with no `sorry`, no `admit` and no custom axiom.

Table 2 of the manuscript maps every result to its Lean name and marks its
status. Machine-checked: the determinant identity, the affine formula, the
trace criterion in both directions, the complementary-forcing involution, the
trace-normalized collapse, the reciprocal reduction, the sign of `K` and
positivity of `Q(tau)` under positive semidefiniteness, the rank-one
specialization, and all three graph corollaries. **Not** machine-checked, and
marked as such: the `n`-dimensional factorization (proved analytically), the
cubic three-mode coefficient and the quantum comparison (verified
symbolically), and the interpretive vocabulary.

## Status

**Not peer reviewed.** AI-assisted tools were used for symbolic checking,
literature organization and citation verification, code support, construction
and checking of the Lean development, and editorial assistance; the
machine-checked claims were checked by Lean's kernel under the pinned
environment, which does not depend on the assistant's correctness. The author
reviewed the manuscript and takes responsibility for it.

The literature search behind Section 14 was documented but **not exhaustive** —
web, arXiv, Crossref, OpenAlex and INSPIRE; it did not reach Google Scholar,
Scopus, Web of Science, MathSciNet or zbMATH, and no non-English literature was
searched. "Not located in the literature reviewed" should be read accordingly,
and no priority claim is made.
