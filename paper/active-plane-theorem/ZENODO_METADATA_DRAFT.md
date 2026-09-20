# Zenodo deposit metadata — draft

**Status: draft only. Nothing has been uploaded. No DOI has been reserved or assigned.**

Fill the publication date at upload time. Everything else below is ready to paste.

---

## Title

```
Palindromic Covariance Determinants and Reciprocal Thresholds in Two-Mode Linear Ornstein–Uhlenbeck Systems
```

## Resource type

`Publication` → `Preprint`

(Not "Journal article": this has not been submitted to or accepted by a journal.
Not "Working paper" unless Zenodo's form prefers it for an unsubmitted preprint.)

## Authors

| field | value |
|---|---|
| Name | De Jesús, Elias |
| ORCID | 0009-0007-0190-9143 |
| Affiliation | Independent Researcher |

Sole author. No contributors to list.

## Publication date

`YYYY-MM-DD` — **set to the actual upload date.** Do not backdate.

## Version

`1` (or `v1`). This is the first deposit of this work.

It is **not** a new version of the earlier two-node deposit
(10.5281/zenodo.22059089). That is a different paper, cited here as the
motivating special case and recovered in Section 12.1 as a corollary. Do not
attach this to that concept DOI.

## Description / abstract

> Let a stable linear Ornstein–Uhlenbeck system have a symmetric drift whose
> restriction to a two-dimensional invariant subspace has relaxation rates
> D₁, D₂ > 0, and let Σ be its stationary covariance. The Lyapunov solution
> gives 4D₁D₂ det Σ = det Q + ν²Q₁₂², with ν = (D₁−D₂)/(D₁+D₂), for an
> arbitrary symmetric forcing Q on that subspace — the 2×2 Hadamard-product
> expansion behind Oppenheim's inequality, used here and not claimed. Along the
> affine family Q(τ) = q_b I + (τ−1)H with H symmetric of any rank, the
> determinant is quadratic in τ, and the main result is that for q_b > 0 it is
> palindromic if and only if the deformation is trace-normalized, tr H = q_b.
> This criterion is an involution: the complementary forcing H* = q_b I − H
> satisfies τ Q_H(1/τ) = Q_{H*}(τ) unconditionally, so trace normalization is
> exactly closure of the family under the reciprocal transform, and the
> rank-one duality e ↦ e⊥ is its restriction to rank one. Palindromicity then
> forces the coordinate w = τ + 1/τ: the normalized determinant is exactly
> affine in w, which yields an exact generalized-variance threshold.
> Graph-Laplacian corollaries give the optimal thresholds 34, 35+15√5 and 247/2
> for K₂, P₃ and K₃, recovering an earlier two-node result with τ = r². Algebra
> is kept separate from modelling: H positive semidefinite with tr H = q_b
> keeps Q(τ) ≻ 0 for all τ > 0. Three distinct active rates make the
> determinant genuinely cubic, so the closure is tied to having two. The
> identity, the trace criterion, the involution and the reciprocal reduction
> are machine-checked in Lean 4 with mathlib.

(This is the manuscript abstract verbatim, with LaTeX rendered to Unicode. If
Zenodo's description field accepts HTML, the same text with `<p>` wrapping is
fine; do not paraphrase it into a different claim.)

## Keywords

```
Ornstein-Uhlenbeck process
Lyapunov equation
stationary covariance
palindromic polynomial
reciprocal polynomial
generalized variance
heterogeneous noise
stochastic networks
formal verification
Lean
```

Ten keywords, all of them terms the paper actually uses. Do not add
"universality", "complexity", "emergence" or any cross-domain term — the paper
explicitly disclaims all of them.

## License

**Creative Commons Attribution 4.0 International (CC BY 4.0)** for this deposit
(the manuscript PDF and its source).

Note in the deposit description or the notes field:

> The code bundled in the source package (`manuscript_checks.py`,
> `make_figures.py`, `build.sh`) and the Lean development in the associated
> repository remain under that repository's Apache License 2.0.

## Related identifiers

| relation | identifier | type | note |
|---|---|---|---|
| `is supplemented by` | `https://github.com/innerlightr-wq/ou-threshold-lean` | URL | repository holding the Lean formalization and the verification snapshot |
| `cites` | `10.5281/zenodo.22059089` | DOI | the author's earlier two-node OU note; the motivating special case, recovered in Section 12.1 |
| `cites` | `10.5281/zenodo.19632381` | DOI | the author's Dual Diagonal note; conceptual background only, not a source for this theorem |

Do **not** use `is new version of` or `is part of` for either Zenodo DOI.

## Notes

> Machine-checked in Lean 4.33.1 with mathlib pinned at
> 0df444a360eaa60ab8c11dca51a86af692955474. The frozen verification snapshot is
> `verified/palindromic-generalization-2026-09/` in the associated repository:
> 28 audited theorems, each depending only on propext, Classical.choice and
> Quot.sound, with no sorry, no admit and no custom axiom; the recorded build
> completes in 8716 jobs. The manuscript's Table 2 states, result by result,
> what is machine-checked, what is verified symbolically, what is proved
> analytically only, and what is interpretation.
>
> All displayed identities are additionally re-derived in exact arithmetic by
> the bundled `manuscript_checks.py` (126/126 checks).
>
> Not peer reviewed. AI-assisted tools were used for symbolic checking,
> literature organization and citation verification, code support, construction
> and checking of the Lean development, and editorial assistance; the
> machine-checked claims were checked by Lean's kernel under the pinned
> environment, which does not depend on the assistant's correctness. The author
> reviewed the manuscript and takes responsibility for it.
>
> The literature search reported in Section 14 was documented but not
> exhaustive: web, arXiv, Crossref, OpenAlex and INSPIRE, with no access to
> Google Scholar, Scopus, Web of Science, MathSciNet or zbMATH, and no
> non-English literature. "Not located in the literature reviewed" is a
> statement about that search, not a priority claim.

## Files to upload

| file | source |
|---|---|
| `DeJesus_Palindromic_Covariance_Thresholds_2026.pdf` | `paper/active-plane-theorem/main.pdf` |
| `palindromic-covariance-thresholds-source-v1.zip` | `paper/active-plane-theorem/release/` |

The ZIP is the self-contained source package: `main.tex`, `references.bib`, the
three figures, `manuscript_checks.py`, `make_figures.py`, `build.sh`,
`README.md`, `BUILD_INSTRUCTIONS.md`, `LICENSE-NOTE.md`, `SHA256SUMS.txt` and
`main.pdf`. It builds with `latexmk -pdf main.tex` inside its own directory,
with no path reaching outside it — the failure mode of the earlier deposit,
which shipped only a PDF and whose source was later unrecoverable.

## Do not

- Do not assign or reserve a DOI before the deposit is actually being published.
- Do not attach this to the earlier note's concept DOI as a new version.
- Do not list a journal, volume or pages; there are none.
- Do not add co-authors, funders or grant numbers; there are none.
