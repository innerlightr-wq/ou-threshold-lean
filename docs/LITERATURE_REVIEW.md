# Literature review

What each source proves, what it does **not** prove, and how this repository uses it. Organized by
mathematical topic. Bibliography: [`../references.bib`](../references.bib) (25 entries, all with
DOIs, all verified against registry metadata — see §12). Claim-by-claim provenance:
[`NOVELTY_AND_PROVENANCE.md`](NOVELTY_AND_PROVENANCE.md).

This file extends the September 2026 audit recorded in `NOVELTY_AND_PROVENANCE.md` to the
residual-threshold, cross-threshold and active-plane results added afterwards.

---

## 1. Linear Ornstein–Uhlenbeck foundations

**`UhlenbeckOrnstein1930`** — the original OU process. Establishes the object; nothing in this
repository depends on the 1930 paper beyond naming.

**`Gardiner2004`** (*Handbook of Stochastic Methods*) — the standard reference for linear
stochastic differential equations, stationary distributions of linear systems with additive noise,
and the potential/detailed-balance conditions. **Proves** that a Hurwitz linear SDE with additive
Gaussian noise has a unique zero-mean stationary Gaussian law whose covariance solves the
continuous Lyapunov equation. **Does not prove** anything about the objective this project
optimizes. *Use:* the stochastic step the repository explicitly does **not** formalize.

**`Vatiwutipong2019`** — closed-form distribution of the multivariate OU process. *Use:*
corroborates the stationary-covariance formula used as the starting point.

## 2. Lyapunov / Sylvester covariance

**`Antoulas2005`** — textbook treatment of Lyapunov equations and Gramians for linear systems:
existence, uniqueness under a Hurwitz drift, and the Gramian machinery. *Use:* the standard
justification for "the algebraic Lyapunov equation has exactly one solution", which the repository
re-proves in Lean for its own small matrices (`lyapunov_unique`, `activeCov_unique`) rather than
importing.

**`Simoncini2016`** (*SIAM Review* 58(3):377–441) — survey of computational methods for linear
matrix equations. **Proves/surveys** projection and low-rank ADI methods exploiting *low-rank
right-hand sides* to obtain *low-rank approximate solutions*, with error and numerical-rank
analysis. **Does not** compute or bound `det X` for a Lyapunov solution `X`. *Use:* cited to mark
the boundary — the phrase "low-rank Lyapunov" in the literature means low-rank *solution
approximation*, a different subject from the exact rank-one *forcing* perturbation studied here.

**`HornJohnson2012`** — *Matrix Analysis*. **Proves** (Thm 1.3.12 and its neighbourhood) that
commuting symmetric matrices are simultaneously diagonalizable. *Use:* the elementary content
behind "`[Q,L] = 0` iff `Q` is diagonal in the Laplacian eigenbasis", used in the three-node
analysis; not formalized in Lean.

**`Barucca2014`** (*Phys. Rev. E* 90, 062129) — coupled heterogeneous OU processes with a symmetric
coupling matrix and node-dependent temperatures. **Its eq. (5)** writes the stationary covariance
in the eigenbasis of the coupling as a double sum with denominators `λ_a + λ_b` — i.e. exactly the
modal formula `Σ̃_ij = Q̃_ij/(D_i + D_j)` this project uses. Also studies eigenvector localization
and a heterogeneity-driven transition. **Does not** study `det Σ`, nor any threshold in coupling
strength for a covariance functional. *Use:* **the citation for the modal covariance formula.**
Nothing about that formula is claimed here.

*(Title note: Crossref carries the typo "heterogenous"; the published APS title reads
"heterogeneous" and that is what `references.bib` uses. Equation number (5) was confirmed in the
arXiv version, arXiv:1407.2031; the published PDF was not opened.)*

**`GodrecheLuck2019`** (*J. Phys. A* 52, 035002) — nonequilibrium stationary states of OU
processes. Eq. (2.15) is the Lyapunov/Sylvester equation `BS + SBᵀ = 2D`; **eq. (2.16)** states the
reversibility condition (`BD` symmetric, i.e. `[B,D] = 0` for symmetric `B`), described there as
long known; **eq. (2.52)** gives the general modal solution in biorthogonal form. **Section 5** is
titled *Electrical arrays* and **§5.1** *RL network*: a resistively coupled array in which each
resistor carries its own temperature. There they state in words that a homogeneous temperature
profile makes the matrices proportional and the process reversible, while an inhomogeneous profile
makes `B` and `D` non-commuting and the process irreversible. *Use:* **the citation for both the modal formula and the
commutator/reversibility statement.** The three-node audit's `[Q,L]` lemma is an elementary
corollary of this for diagonal `Q` on a connected graph and is recorded as such.

*(Year note: Crossref lists 2018 — online-first; the article appears in the 2019 volume 52 and is
cited as 2019. Equation and section numbers were confirmed in arXiv:1807.00694; the paywalled
journal version was not opened.)*

## 3. Network OU / noisy consensus

**`BamiehEtAl2012`** (*IEEE TAC* 57(9):2235–2249) — coherence in large-scale networks.
**Proves** dimension-dependent limits on the `H₂` performance of local feedback, with the
performance measure a **trace** — the steady-state variance of deviations from the average,
reducible to a sum over nonzero Laplacian eigenvalues. **Does not** consider `det Σ` or any
determinant functional. *Use:* establishes what the network literature optimizes, and explains
structurally why the off-diagonal modal correlations this project studies have not been examined
there: a trace sees only the diagonal `Q̃_αα`.

**`PikovskyEtAl2001`**, **`TeramaeTanaka2004`** — synchronization and noise-induced phase
synchronization. *Use:* the interpretation check that produced the audit's one substantive
correction ("synchronization collapse" is not supported by this model, in which the
synchronization error decreases monotonically in the coupling).

## 4. Heterogeneous and low-rank forcing

**`FerreiraMetzBarucca2025`** (*Phys. Rev. E* 111, 014151) — random-matrix ensemble for the
covariance of OU processes with heterogeneous temperatures. **Proves** results for the
**reversible** case, imposing `AD = DAᵀ` explicitly, which is precisely the commuting case.
**Does not** cover the irreversible heterogeneous case — which is exactly the regime this
repository is in whenever the noise profile is non-constant. *Use:* a citable statement that the
nearest random-matrix treatment excludes this regime by hypothesis.

**`SummersEtAl2016`** (*IEEE TCNS* 3(1):91–101) — submodularity and controllability. **Proves**
(Theorem 6) that `f(S) = log det W_S`, the log-determinant of the controllability Gramian, is a
**monotone increasing, submodular** set function of the actuator set `S`; adding an actuator is a
rank-one addition `Q → Q + bbᵀ` to the forcing. **Does not** give any closed-form dependence, does
not treat a *multiplicative* deformation `Q → Q + (τ−1)eeᵀ` with `τ < 1`, and has no threshold in
a scalar coupling parameter. *Use:* **the closest located prior art on determinants of
Lyapunov/Gramian solutions under rank-one forcing changes** — qualitative where this repository is
exact. Any claim about the active-plane theorem must be worded against this paper.

Two cautions, both unresolved and recorded rather than glossed. (i) A published *Correction* to
this article exists in the same journal; it could not be retrieved, so **whether it touches
Theorem 6 is unverified** — check before citing it in a manuscript. (ii) A similarly titled
preprint, Cortesi, Summers & Lygeros, *Submodularity of Energy Related Controllability Metrics*
(arXiv:1403.6351), has different numbering and **no Theorem 6**; the two must not be conflated.

## 5. Determinant / generalized variance

**`Wilks1932`** — introduces the generalized variance `det Σ`. *Use:* the name and provenance of
the repository's `volume` functional; `det_cov` proves the repository's closed form **is** that
determinant.

**`CoverThomas2005`** — Gaussian differential entropy `h = ½log((2πe)ⁿ det Σ)`. *Use:*
interpretation only — the volume threshold is equivalently a stationary-entropy threshold.

## 6. Conditional / residual variance

**`Lauritzen1996`** (*Graphical Models*) — for a Gaussian vector,
`Var(X_i | X_{-i}) = 1/(Σ⁻¹)_ii`, the reciprocal of a diagonal entry of the concentration matrix;
the Schur-complement identity is standard there. **Does not** analyse how that quantity behaves as
a coupling strength varies. *Use:* the definitional identity used by
`residualVariance_eq_det_div` and by the three-node audit's `D_i = 1/(Σ⁻¹)_ii`.

## 7. Covariance shape and sphericity

**`Mauchly1940`** (*Ann. Math. Statist.* 11:204–209) — the sphericity likelihood-ratio statistic
`W = det S / ((tr S)/p)^p`, i.e. the ratio of geometric to arithmetic mean of the eigenvalues
raised to `p`. **Proves** the test; the invariant is scale- and rotation-free, and `W ≤ 1` with
equality iff `Σ ∝ I` is AM–GM. *Use:* `J_n = (tr Σ)ⁿ/det Σ` used in this repository is, up to the
constant `nⁿ`, the reciprocal of Mauchly's statistic. **The repository claims nothing about it.**

**`Muirhead1982`** §8.3 — textbook treatment of the same statistic. *Use:* secondary reference.

**`WolkowiczStyan1980`** (*Linear Algebra Appl.* 29:471–506) — bounds for eigenvalues using
traces. **Proves** two-sided eigenvalue bounds from `tr Σ` and `tr Σ²`. **Does not** claim that
trace and determinant determine a spectrum — on the contrary, the existence of this bounds
literature is the standard acknowledgement that they do not, for `n ≥ 3`. *Use:* the citable
context for `exists_same_trace_det_different_ratio`; that Lean theorem is an explicit witness of a
standard fact, not a new result.

## 8. Reciprocal and palindromic algebra

A polynomial of even degree `2m` with palindromic (self-reciprocal) coefficients can be written
`P(t) = tᵐ Q(t + 1/t)` with `Q` of degree `m`. That is why `w = t + 1/t` is the natural coordinate
once `det Σ` is known to be palindromic in `τ`, and the repository treats it as standard algebra:
`w` is introduced **only after** palindromicity is proved (`det_activeCov_palindromic` precedes
`normalizedActiveDet_eq`).

**`Vieira2019`** (*Polynomials with Symmetric Zeros*, IntechOpen, DOI 10.5772/intechopen.82728) —
**Theorem 3** states exactly this reduction for self-reciprocal polynomials of even degree, with
zeros on the unit circle corresponding to real zeros of `Q` in `[−2,2]`. Open access, verified on
the publisher page. It is a book chapter rather than a journal article, which is the best
DOI-bearing source located for an otherwise textbook fact.

**Naming caution:** the substitution is sometimes called a "Chebyshev transform", but that name
**could not be verified as established terminology** from any primary source. Describe the
substitution rather than leaning on the name.

**`DeJesus2026dual`** — records the same reciprocal structure in a different setting: for a
rectangle with edge ratio `r`, the invariant `tr(T)·tr(T⁻¹)` equals `r + 1/r` in the note's
normalization (its Prop. 4.1), and Prop. 4.2 shows it determines the ratio up to `r ↔ 1/r`.
For a `2 × 2` matrix `tr(T)tr(T⁻¹) = (tr T)²/det T`, so this is literally the `J₂` of §7 in
another guise. See §10 for the boundary on how this source may be used.

## 9. Graph spectral structure

No external source is cited for graph spectra. The Laplacian spectra used (`P3`: `{0,1,3}`;
`K3`: `{0,3,3}`) are derived symbolically in the three-node audit and, where needed, in Lean; the
common/relative mode language is standard and carries no citation weight. `BamiehEtAl2012`
supplies the network context. This is recorded as a deliberate absence, not an oversight.

## 10. Reconstruction / invariant context — and its boundary

**`DeJesus2026dual`** (Zenodo 10.5281/zenodo.19632381) — an invariant basis for reconstructing
orthogonal-hyperrectangle shape from aggregated scalars. **Proves**, in its own setting: §4, the
two-dimensional case is *complete* — one reciprocal invariant determines the aspect ratio up to
inversion; §5.1, a dimensional obstruction for `n ≥ 3` (shape space has dimension `n − 1`, so no
single scalar can be reconstructive), with an explicit 3D counterexample in §5.2; and the general
`n − 1` scalar principle, which the note itself states is a specialization of the classical theory
of symmetric functions, citing the diffusion-tensor-imaging reconstruction literature (Basser &
Pierpaoli; Ennis & Kindlmann) and explicitly **not** claiming a new reconstruction theorem.

**Boundary, stated explicitly.** This source is used **only** for: two-dimensional reciprocal
completeness, the `n − 1` shape-dimension count, and the failure of single-scalar reconstruction
for `n ≥ 3`. It is **not** a source for: OU dynamics, Lyapunov or Sylvester equations, stochastic
processes, graph covariance, or rank-one forcing — it contains none of these. The repository's
`SpectralShape.lean` results are derived independently from the covariance algebra, and their
standard provenance is §7 (Mauchly, Muirhead, Wolkowicz–Styan), not this note. The relationship is
an **analogy between two instances of the same elementary invariant-theoretic fact**, and is worth
recording precisely because both instances are the author's.

## 11. Closest prior art to the active-plane theorem

The assembly at issue is: *isotropic baseline forcing on a two-dimensional drift-invariant plane,
deformed at rank one, yields a palindromic determinant, hence an exactly affine dependence of the
normalized generalized variance on `w = t + 1/t`, hence an exact threshold after minimizing over
the coupling.* Its ingredients are individually standard, and each is cited above:

| ingredient | status | source |
|---|---|---|
| modal Lyapunov solution | standard, published | `Barucca2014` eq. (5); `GodrecheLuck2019` eq. (2.52) |
| commutator/reversibility | standard | `GodrecheLuck2019` eq. (2.16), §5.1 |
| `det Σ` = generalized variance | standard | `Wilks1932` |
| log-det under rank-one forcing *addition* | standard, **qualitative** | `SummersEtAl2016` Thm 6 |
| `t + 1/t` substitution | textbook | `Vieira2019` Thm 3 |
| `J_n` and its non-injectivity for `n ≥ 3` | standard | `Mauchly1940`, `WolkowiczStyan1980` |
| Hadamard-with-Cauchy structure of `Σ` | published, used elsewhere for singular-value bounds | `TownsendWilber2018` §4.1 eq. (29) — numbering verified on arXiv:1712.05864 only |

**What was searched for and not found:** an exact closed-form dependence of `det Σ` on a rank-one
*forcing* perturbation; an exact threshold in coupling strength at which a covariance determinant
(or Gaussian entropy) reverses direction; and a two-mode Lyapunov covariance with a reciprocal
symmetry in a noise-strength ratio. Two independent search passes located nothing equivalent; the
nearest statement in the literature remains `SummersEtAl2016` Theorem 6, which is monotonicity and
submodularity in the *actuator set*, not a closed form and not a threshold in a scalar parameter.

Accordingly the repository's wording is, and should remain:

> The repository formalizes an exact palindromic determinant identity for a two-mode active OU
> covariance under isotropic baseline forcing and rank-one heterogeneous excitation. The
> ingredients draw on standard Lyapunov covariance theory and standard reciprocal-polynomial
> algebra; the exact threshold assembly is treated as a repository-specific derivation unless
> equivalent prior work is identified.

This is classified **APPARENTLY DISTINCT ASSEMBLY**, with `SummersEtAl2016` as the recorded
closest prior art. It is *not* classified as novel, and no priority is claimed.

## 12. Open literature questions

1. ~~A citable source for the palindromic → `t + 1/t` substitution.~~ **Resolved:** `Vieira2019`
   Thm 3. Two residual items: the name "Chebyshev transform" is unverified as terminology (the
   README currently uses it and should be softened the next time that file is edited — deliberately
   not edited here, to avoid a conflict with the other documentation branch), and a
   journal-quality alternative to an IntechOpen chapter would be preferable if one exists.
2. **Whether any nonequilibrium-statistical-mechanics paper computes `det Σ` versus coupling** for
   a two-temperature linear system. The two-node model coincides with the Brownian gyrator
   (`FilligerReimann2007`) and two-temperature Langevin dynamics (`DotsenkoEtAl2013`); both study
   currents and heat flux rather than covariance volume, and neither was found to compute the
   determinant. Tagged `uncertain-more-search`.
3. **Whether the published *Correction* to `SummersEtAl2016` affects Theorem 6.** Not retrieved;
   check before citing that theorem in a manuscript.
4. **Whether the `n ≥ 3` non-identifiability has a standard named citation** rather than being
   folded into the eigenvalue-bounds literature. None was located; `WolkowiczStyan1980` is used as
   the context.
5. **Graph-theoretic characterization** of which `(graph, node)` pairs satisfy the active-plane
   hypothesis — open mathematically, not a literature question, and recorded in the general-graph
   audit rather than here.

### Metadata corrections made in this pass

Three, all from checking primary sources rather than registry strings:

* `Barucca2014` — Crossref title carries the typo "heterogenous"; corrected to the published APS
  spelling "heterogeneous".
* `GodrecheLuck2019` — Crossref year is 2018 (online-first); the article is in volume 52 (2019)
  and is cited as 2019.
* The earlier audit described Godrèche & Luck §5.1 as "an open chain"; the section is in fact
  *RL network* within *Electrical arrays*. The physics cited from it is unchanged.

Every other entry matched its registry record field-for-field. All 25 entries carry a DOI; all
resolve; BibTeX compiles with zero warnings.

**Provenance of quoted equation numbers.** Where an equation or theorem number appears above
(`Barucca2014` eq. 5; `GodrecheLuck2019` eqs. 2.15/2.16/2.52 and §5.1; `SummersEtAl2016` Thm 6;
`TownsendWilber2018` §4.1 eq. 29), it was read from the arXiv or open-access version; publisher
numbering was confirmed only where the publisher page was openly readable. This is recorded
because Elsevier numbering in particular can differ from arXiv numbering.
