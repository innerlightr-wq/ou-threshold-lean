# Two-Mode Active-Subspace Reduction and Reciprocal Determinant Thresholds

**First draft, September 2026. Not deposited, not submitted, no DOI.**

A new paper — *not* a revision of the deposited two-node note
([10.5281/zenodo.22059089](https://doi.org/10.5281/zenodo.22059089)), which is cited here as the
motivating special case and is recovered in Section 12 as a corollary.

## The result

For a stable linear OU system whose drift restricted to a two-dimensional invariant subspace has
rates `D1, D2 > 0`, and whose forcing on that subspace is a rank-one deformation of an isotropic
baseline, `Q = q_b (I + (tau-1) e e^T)` along a unit excitation direction `e = c u + s v`:

```
4 D1 D2 det Sigma = q_b^2 ( A tau^2 + (1 - 2A) tau + A ),    A = c^2 s^2 nu^2,
                                                             nu = (D1-D2)/(D1+D2)
```

The quadratic is **palindromic** — leading coefficient equals constant coefficient — because the
forcing family is self-dual, `Q_e(tau) = tau * Q_{e_perp}(1/tau)`, which is
`e e^T + e_perp e_perp^T = I` in disguise. Only then does the reciprocal coordinate
`w = tau + 1/tau` appear: dividing by `tau` makes the normalized determinant exactly affine in
`w`, giving an exact generalized-variance threshold. Graph corollaries follow: `K2` recovers the
two-node threshold with `tau = r^2`, and `P3`, `K3` give `35 + 15*sqrt(5)` and `247/2`.

**`tau` is a variance ratio, not an amplitude ratio.** This is the single easiest way to misreport
a constant by a square; see Remark 2 in the paper.

## Contents

| file | |
|---|---|
| `main.tex` | the manuscript |
| `main.pdf` | compiled, 18 pages, letter |
| `references.bib` | self-contained bibliography, 23 entries, all cited |
| `figures/fig1–3.pdf` | active-plane schematic; affine determinant; threshold curves |
| `manuscript_checks.py` | 61 exact symbolic checks (SymPy) |
| `make_figures.py` | regenerates the figures from the exact formulas |
| `build.sh`, `build.log` | build script and recorded transcript |
| `SHA256SUMS.txt` | digests of every file above |

This directory is **self-contained**: `main.tex` reads `references.bib` from beside it, not from
the repository root. That is deliberate — the previous Zenodo deposit shipped only a PDF, and
reconstructing it later cost real work. Do not repeat that.

## Building and checking

```bash
./build.sh                       # latexmk -pdf, or pdflatex/bibtex/pdflatex x2
python3 manuscript_checks.py     # 61/61 exact checks, exit 0
python3 make_figures.py          # regenerate figures (needs matplotlib)
```

Recorded build: **0 undefined citations, 0 undefined references, 0 overfull boxes, 0 BibTeX
warnings, 23 bibliography entries, 18 pages.**

## What is proved where

- **Machine-checked in Lean 4 + mathlib** (see the paper's Table 2): the covariance block, the
  forcing determinant, self-duality, the palindromic identity, the reciprocal reduction, the
  degeneracy conditions, the coefficient bounds, the threshold equivalence, and all three graph
  corollaries. Environment: Lean 4.33.1, mathlib `0df444a360ea…`, snapshot at
  `verified/active-plane-2026-09/`, no `sorry`, only the three standard mathlib axioms.
- **Analytic only, not formalized**: the `n`-dimensional determinant factorization
  (Proposition 10). The paper says so explicitly rather than implying Lean covers arbitrary `n`.
- **Interpretation, not a theorem**: "effective active dimension" (Section 10.1).

## Bibliography note

`references.bib` here is derived from the repository's curated master bibliography, pruned to the
23 entries this manuscript actually cites, with internal provenance `note` fields stripped (the
`plain` style would print them; the master retains them). One entry, `BoffiDeGregorio2024`, was
added for this manuscript and verified by DOI content negotiation; it is not in the master file.

The master bibliography is **hand-maintained**. Better BibTeX is not authorized to regenerate it —
see `docs/ZOTERO_SETUP.md` §6b for the dry-run evidence behind that decision.

## Deliberately excluded

No universal-corridor or 63/37 claims; no Minkowski, Lorentz, Schwarzschild or relativity analogy;
no philosophical projection language. The general graph lower bound
`w* >= 2 + 64|E|/lambda >= 34` is **not** in the body: the inequality chain reconstructs, but
stating it correctly needs four qualifiers, and it is not load-bearing. It is recorded, with those
qualifiers, as open item 1 in the appendix.
