# Palindromic Covariance Determinants and Reciprocal Thresholds

**First draft, September 2026. Not deposited, not submitted, no DOI.**

A new paper — *not* a revision of the deposited two-node note
([10.5281/zenodo.22059089](https://doi.org/10.5281/zenodo.22059089)), which is cited here as the
motivating special case and is recovered in Section 12 as a corollary.

## The result

For a **symmetric** drift whose restriction to a two-dimensional invariant subspace has rates
`D1, D2 > 0`, and an **arbitrary symmetric** forcing `Q` on that subspace:

```
4 D1 D2 det Sigma = det Q + nu^2 Q12^2 ,    nu = (D1-D2)/(D1+D2)
```

with `Q12` the off-diagonal in the drift eigenbasis. No rank-one, isotropy or positivity
assumption. **This identity is not claimed as new**: writing `Sigma = C o Q` for the Cauchy
matrix `C_ij = 1/(D_i+D_j)`, it is the 2x2 Hadamard-product determinant expansion behind
Oppenheim's inequality (Horn & Johnson, *Matrix Analysis* 2nd ed., Thm 7.8.16 eq. (7.8.17)
p. 509; originally Oppenheim 1930), with the remainder written out. The same pipeline (Cauchy-Hadamard,
then Oppenheim, then a determinant bound) appears in arXiv:1101.0754 §4.1.5 for a discrete-time
covariance, stopping at the inequality. Equivalently
`4 D1 D2 det Sigma = nu^2 q11 q22 + (1-nu^2) det Q`, and dividing through,
`rho_Sigma = sqrt(1-nu^2) rho_Q` — stationary correlation is forcing correlation damped by the
geometric/arithmetic mean ratio of the rates. For the affine family `Q(tau) = q_b I + (tau-1) H`, `H` symmetric of any rank:

```
4 D1 D2 det Sigma(tau) = q_b^2 + q_b (tr H)(tau-1) + K (tau-1)^2 ,   K = det H + nu^2 H12^2
```

and — the structural point — the quadratic is **palindromic iff `tr H = q_b`**. Rank-one
excitation `H = q_b e e^T` satisfies this automatically for every direction `e`, which is why
it works; it is **not** the mechanism. Palindromicity then forces `w = tau + 1/tau`, giving an
exact generalized-variance threshold. Graph corollaries: `K2` → 34, `P3` → `35+15*sqrt(5)`,
`K3` → `247/2`.

**What is actually claimed** is the trace criterion, the palindromic symmetry it controls, and
the exact threshold — not the identity, and not the coordinate `w` (which is an invertible
function of the standard two-temperature combination `(T1-T2)^2/(T1 T2)`).

**`tau` is a variance ratio, not an amplitude ratio** — conflating them misreports a constant by
a square (Remark 2).

**Admissibility.** The identity is algebra and holds for any symmetric `H` and any real `tau`.
For the stochastic reading take `H` positive semidefinite with `tr H = q_b`: then `K >= 0` and
`Q(tau)` stays positive definite for every `tau > 0`.

**Failure boundary.** With three *distinct* rates and genuine three-mode support the response is
generically cubic, leading coefficient proportional to `prod_{i<j} (D_i - D_j)^2`. `K3` is not a
counterexample: its relevant eigenspace is degenerate, so its *distinct-rate* dimension is two.

## Contents

| file | |
|---|---|
| `main.tex` | the manuscript |
| `main.pdf` | compiled, 23 pages, letter |
| `references.bib` | self-contained bibliography, 32 entries, all cited |
| `figures/fig1–3.pdf` | active-plane schematic; affine determinant; threshold curves |
| `manuscript_checks.py` | 111 exact symbolic checks (SymPy), including adversarial assumption tests |
| `make_figures.py` | regenerates the figures from the exact formulas |
| `build.sh`, `build.log` | build script and recorded transcript |
| `SHA256SUMS.txt` | digests of every file above |

This directory is **self-contained**: `main.tex` reads `references.bib` from beside it, not from
the repository root. That is deliberate — the previous Zenodo deposit shipped only a PDF, and
reconstructing it later cost real work. Do not repeat that.

## Building and checking

```bash
./build.sh                       # latexmk -pdf, or pdflatex/bibtex/pdflatex x2
python3 manuscript_checks.py     # 111/111 exact checks, exit 0
python3 make_figures.py          # regenerate figures (needs matplotlib)
```

Recorded build: **0 undefined citations, 0 undefined references, 0 overfull boxes, 0 BibTeX
warnings, 32 bibliography entries, 23 pages.**

## What is proved where

- **Machine-checked in Lean 4 + mathlib** (paper Table 2): the general determinant identity, the
  affine formula, the trace criterion (both directions), the trace-normalized collapse, the
  reciprocal reduction, the sign of `K` and positivity of `Q(tau)` under positive
  semidefiniteness, the rank-one specialization recovering the earlier theorem, and all three
  graph corollaries. Environment: Lean 4.33.1, mathlib `0df444a360ea…`, build 8716 jobs,
  20 theorems audited, only `propext`/`Classical.choice`/`Quot.sound`, no `sorry`.
  Snapshot: `verified/palindromic-generalization-2026-09/`. The earlier snapshot
  `verified/active-plane-2026-09/` is unchanged and still verifies.
- **Symbolically verified only**: the anisotropic self-duality counterexample, the cubic
  three-mode coefficient, the weak-coupling law.
- **Analytic only, not formalized**: the `n`-dimensional determinant factorization
  (Proposition 10), which needs all five hypotheses listed in its accompanying remark.
- **Interpretation**: "distinct-rate dimension".

## Bibliography note

`references.bib` here is derived from the repository's curated master bibliography, pruned to the
23 entries this manuscript actually cites, with internal provenance `note` fields stripped (the
`plain` style would print them; the master retains them). One entry, `BoffiDeGregorio2024`, was
added for this manuscript and verified by DOI content negotiation; it is not in the master file.

The master bibliography is **hand-maintained**. Better BibTeX is not authorized to regenerate it —
see `docs/ZOTERO_SETUP.md` §6b for the dry-run evidence behind that decision.

## Deliberately excluded

No universal-corridor or 63/37 claims; no Minkowski, Lorentz, Schwarzschild or relativity analogy;
no philosophical projection language. The general graph lower bound `w* >= 2 + 64|E|/lambda >= 34` has been **removed entirely**: the
inequality chain reconstructs, but stating it correctly needs four qualifiers (lambda is the
*active* eigenvalue, not algebraic connectivity; `|E|` is an unweighted edge count; admissibility
of the excitation is load-bearing; the derivation assumes the active plane contains the common
mode), and the equality-iff-`K2` direction was never written out. It is not load-bearing for
anything claimed, so the paper is stronger without it.
