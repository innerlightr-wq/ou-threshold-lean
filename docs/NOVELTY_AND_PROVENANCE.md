# Novelty and provenance

Claim-by-claim provenance for the current state of this repository, covering the original
two-node threshold and everything added afterwards (residual threshold, cross-threshold identity,
active-plane reduction, spectral-shape results).

Bibliography: [`../references.bib`](../references.bib) · literature notes:
[`LITERATURE_REVIEW.md`](LITERATURE_REVIEW.md) · Zotero structure:
[`ZOTERO_SETUP.md`](ZOTERO_SETUP.md).

> **Relation to the earlier audit.** A September 2026 literature/provenance audit of the *two-node*
> work exists on branch `pr1-cleanup-after-cross-threshold` as a file of the same name. This
> document is the superset: it keeps that audit's conclusions (including its interpretive
> correction about "synchronization collapse") and extends the tables to the later results. When
> the two branches are reconciled, **this version supersedes** for the tables, and
> `references.bib` here is a strict superset of the 12 entries there, with identical keys.

## Classification vocabulary

`STANDARD THEORY` · `KNOWN INGREDIENT` · `KNOWN REPARAMETERIZATION` ·
`NEW DERIVATION FROM KNOWN INGREDIENTS` · `APPARENTLY DISTINCT ASSEMBLY` ·
`CLOSEST PRIOR ART FOUND` · `UNCERTAIN — MORE SEARCH NEEDED`.

Formal status is tracked separately, because a provenance table must not imply Lean proved
something it did not: `LEAN FORMALIZED` · `ANALYTICALLY DERIVED, NOT LEAN` ·
`NUMERICALLY CHECKED` · `STANDARD EXTERNAL THEORY` · `INTERPRETATION ONLY`.

---

## 1. Provenance table

| # | Repository claim | Location | Prior work | Imported assumption | Convention | Formal status | Classification | Key |
|---|---|---|---|---|---|---|---|---|
| 1 | stationary covariance solves the algebraic Lyapunov equation | `Covariance.lean` `cov_lyapunov` | modal solution in an eigenbasis | that the *process's* stationary covariance obeys it (not formalized) | `M Σ + Σ Mᵀ = -Q`, `M` Hurwitz | LEAN FORMALIZED (algebra only) | STANDARD THEORY | `Barucca2014`, `GodrecheLuck2019`, `Gardiner2004` |
| 2 | that solution is unique | `Covariance.lean` `lyapunov_unique`; `ActivePlane.lean` `activeCov_unique` | Lyapunov uniqueness under Hurwitz drift | — | as above | LEAN FORMALIZED | STANDARD THEORY | `Antoulas2005` |
| 3 | `det Σ` is the generalized variance `A(κ,r)` | `Covariance.lean` `det_cov` | Wilks' generalized variance | — | — | LEAN FORMALIZED | STANDARD THEORY (naming) | `Wilks1932` |
| 4 | volume threshold: `∃κ>0, A(κ) > A(0) ⟺ r > 3+2√2` | `MainTheorem.lean` `exists_volume_improvement_iff_threshold` | the deposited paper, Theorem 1 | equal relaxation, independent additive noise | `σ₁=1, σ₂=r` amplitudes | LEAN FORMALIZED | formalization of an EXISTING RESULT of the author's own paper | `DeJesus2026ou` |
| 5 | residual-variance threshold: `∃κ>0, D(κ) > D(0) ⟺ r > 2+√3` | `ResidualThreshold.lean` `exists_residual_improvement_iff_threshold` | the deposited paper, Proposition 5 | as above; `D = Var(X∣Y)` identified with the Schur complement (not formalized) | `D = Σxx − Σxy²/Σyy` | LEAN FORMALIZED | formalization of an EXISTING RESULT | `DeJesus2026ou`, `Lauritzen1996` |
| 6 | reciprocal coordinate `s(r) = r + 1/r`; `s(r_A*)=6`, `s(r_D*)=4` | `CrossThreshold.lean` | classical reciprocal/self-reciprocal algebra; same structure in the author's reconstruction note | — | amplitude ratio | LEAN FORMALIZED | KNOWN REPARAMETERIZATION | `DeJesus2026dual` (analogy only) |
| 7 | cross-threshold identity: at `(κ,r) = (1, r_A*)`, `μ₁/μ₂ = (r_D*)² = 7+4√3` | `CrossThreshold.lean` `cross_threshold_eigenvalue_ratio` | none located | equal relaxation; the specific model | eigenvalues as roots of `det(Σ−μI)=0` | LEAN FORMALIZED | APPARENTLY DISTINCT ASSEMBLY (model-specific; not preserved under unequal relaxation) | — |
| 8 | active-plane covariance and its uniqueness | `ActivePlane.lean` `activeCov_lyapunov`, `activeCov_unique` | modal Lyapunov solution, specialized to a 2-D block | 2-D drift-invariant plane | `Σ_ij = Q_ij/(D_i+D_j)` | LEAN FORMALIZED | STANDARD THEORY (special case) | `Barucca2014`, `GodrecheLuck2019` |
| 9 | forcing self-duality `Q_e(τ) = τ·Q_{e^⊥}(1/τ)` | `ActivePlane.lean` `activeForcing_self_dual` | elementary (`eeᵀ + e^⊥e^⊥ᵀ = I`) | unit excitation direction | `Q = q_b(I+(τ−1)eeᵀ)` | LEAN FORMALIZED | NEW DERIVATION FROM KNOWN INGREDIENTS | — |
| 10 | palindromic determinant: `4D₁D₂ det Σ = q_b²(Aτ² + (1−2A)τ + A)` | `ActivePlane.lean` `det_activeCov_palindromic` | ingredients standard; closest statement is qualitative | isotropic baseline **on the plane**; rank-one deformation | `A = c²s²ν²`, `ν=(D₁−D₂)/(D₁+D₂)` | LEAN FORMALIZED | **APPARENTLY DISTINCT ASSEMBLY** | `SummersEtAl2016` (closest prior art) |
| 11 | `det Σ/τ = 1 + A(w−2)`, `w = τ+1/τ` | `ActivePlane.lean` `normalizedActiveDet_eq` | self-reciprocal polynomial reduction `P(t) = tᵐQ(t+1/t)` (Thm 3) | `τ > 0` | `w` introduced only after palindromicity | LEAN FORMALIZED | KNOWN REPARAMETERIZATION of a distinct identity | `Vieira2019` |
| 12 | `A = 0 ⟺ c=0 ∨ s=0 ∨ D₁=D₂` | `ActivePlane.lean` `activeCoeff_eq_zero_iff` | — | `D₁,D₂ > 0` | — | LEAN FORMALIZED | NEW DERIVATION FROM KNOWN INGREDIENTS | — |
| 13 | threshold equivalence `Φ(1+C(w−2)) > 1 ⟺ w > 2 + (1−Φ)/(ΦC)` | `ActivePlane.lean` `volumeRatio_gt_one_iff` | elementary algebra | `Φ, C > 0` | — | LEAN FORMALIZED | STANDARD THEORY | — |
| 14 | K₂ corollary: the repository's own `volume/volume0` **is** the active-plane formula, with `τ = r²` | `ActivePlane.lean` `volume_div_volume0_eq`, `reciprocalExcitation_sq` | the deposited paper's model | — | `τ` is a **variance** ratio; `w = (r+1/r)²−2` | LEAN FORMALIZED | NEW DERIVATION FROM KNOWN INGREDIENTS | `DeJesus2026ou` |
| 15 | P3 corollary: curve `(27κ³+72κ²+64κ+16)/(2κ)`, minimum `35+15√5` at `κ=(√5−1)/3` | `ActivePlane.lean` `p3_thresholdCurve_eq`, `p3_threshold_min`, `p3_threshold_attained` | none located | centre-node excitation on the path graph | derived from `thresholdCurve`, not fitted | LEAN FORMALIZED | APPARENTLY DISTINCT ASSEMBLY | — |
| 16 | K3 corollary: curve `(81κ³+162κ²+112κ+24)/(2κ)`, minimum `247/2` at `κ=1/3` | `ActivePlane.lean` `k3_thresholdCurve_eq`, `k3_threshold_min`, `k3_threshold_attained` | none located | one-node excitation on the complete graph | as above | LEAN FORMALIZED | APPARENTLY DISTINCT ASSEMBLY | — |
| 17 | `J₂ = (tr)²/det = q + 1/q + 2` determines `q` on `q ≥ 1` | `SpectralShape.lean` `J2_eq_reciprocalInvariant`, `eigen_ratio_unique_of_J2` | reciprocal of Mauchly's sphericity statistic; 2-D completeness in the author's reconstruction note | SPD, `n = 2` | scale-free | LEAN FORMALIZED | STANDARD THEORY | `Mauchly1940`, `Muirhead1982`, `DeJesus2026dual` |
| 18 | `n ≥ 3`: same trace and determinant, different extreme ratio — `(1,8,12)` vs `(2,3,16)` | `SpectralShape.lean` `exists_same_trace_det_different_ratio` | eigenvalue-bounds literature; §5 of the reconstruction note | positivity | — | LEAN FORMALIZED | STANDARD THEORY (explicit witness of an elementary fact) | `WolkowiczStyan1980`, `DeJesus2026dual` |
| 19 | modal forcing channels for P3; `‖[Q,L]‖²_F = α²+β²` | three-node audit (outside repo) | `[Q,L]=0` ⟺ reversibility; simultaneous diagonalizability | connected graph, diagonal `Q` | `α = d₁−d₃`, `β = d₁−2d₂+d₃` | ANALYTICALLY DERIVED, NOT LEAN | STANDARD THEORY / elementary corollary | `GodrecheLuck2019`, `HornJohnson2012` |
| 20 | `d/dκ log det Σ\|₀ = −tr(L)/a = −2\|E\|/a`, independent of `Q` | three-node / general-graph audits | generalizes the paper's `A′(0) < 0` | any symmetric `S`, any PD `Q` | — | ANALYTICALLY DERIVED, NOT LEAN | NEW DERIVATION FROM KNOWN INGREDIENTS (three lines; `Q`-independence is the only interesting part) | `DeJesus2026ou` |
| 21 | `w* ≥ 2 + 64\|E\|/λ ≥ 34`, equality iff K₂ | general-graph audit | — | rank-one excitation satisfying the active-plane hypothesis | — | ANALYTICALLY DERIVED, NOT LEAN | APPARENTLY DISTINCT ASSEMBLY | — |
| 22 | `det Σ = O(κ^{−(n−1)})` at strong coupling | three-node / general-graph audits | standard asymptotics | connected graph | — | ANALYTICALLY DERIVED, NOT LEAN | STANDARD THEORY | — |
| 23 | "synchronization collapse" is not supported by this model: `Var(X₁−X₂)` decreases monotonically in `κ` | earlier audit; README prose | — | the model itself | — | INTERPRETATION ONLY (the algebra is verified) | INTERPRETIVE CORRECTION to the deposited paper's framing | `PikovskyEtAl2001`, `TeramaeTanaka2004` |

## 2. Imported theory → repository use

| Source input | Repository use |
|---|---|
| Lyapunov/Sylvester covariance theory (`Antoulas2005`, `Barucca2014`, `GodrecheLuck2019`) | the algebraic covariance statements verified in Lean; the stochastic step is *not* formalized |
| reversibility / commutator condition (`GodrecheLuck2019`) | modal-independence analysis in the three-node audit |
| generalized variance (`Wilks1932`), Gaussian entropy (`CoverThomas2005`) | naming and interpretation of `det Σ`; entropy reading of the threshold |
| network coherence / H₂ (`BamiehEtAl2012`) | context: the network literature optimizes a **trace**, which cannot see modal cross-correlations |
| submodularity of `log det` Gramian (`SummersEtAl2016`) | the closest prior art against which the active-plane determinant result is worded |
| sphericity statistics (`Mauchly1940`, `Muirhead1982`), eigenvalue bounds (`WolkowiczStyan1980`) | provenance of `J₂`/`J_n` and of the `n ≥ 3` non-identifiability |
| Gaussian graphical models (`Lauritzen1996`) | the identity `D_i = 1/(Σ⁻¹)_ii` |
| self-reciprocal polynomial reduction (`Vieira2019` Thm 3) | the `t + 1/t` representation, used only after palindromicity is proved |
| symmetric-invariant reconstruction (`DeJesus2026dual`) | background analogy for 2-D completeness and the `n ≥ 3` obstruction — **not** a source for any OU, Lyapunov or graph statement |
| Hadamard-with-Cauchy structure (`TownsendWilber2018`) | cited to mark that this structure is known, and used there for singular-value bounds rather than determinants |

## 3. Current Zenodo version versus current repository state

Both statements below were checked against the deposited PDF itself, not from memory.

**`DOI 10.5281/zenodo.22059089`** (version DOI; concept DOI `10.5281/zenodo.22059088`), *Technical
note*, deposited **2026-08-22**, CC BY 4.0, one file `main.pdf`. Its contents: the coupled OU
model and exact stationary covariance (§§3–4); covariance geometry `D`, `C`, `A` (§5); universal
weak-coupling contraction `A′(0) < 0` (§6); the equal-relaxation reduction and the exact
covariance-volume threshold `3 + 2√2` with `κ₁κ₂ = 1` (§§7–8); the residual-variance threshold
`2 + √3` (§9); strict monotonicity of Gaussian coherence (§10); a numerical example and figures
(§§11–12); strong-coupling asymptotics (§13); limitations (§16).

**Not present in the deposit** (verified by text search: `Lean` 0 hits, `cross-threshold` 0,
`rank-one` 0, `Laplacian` 0, `active` 0, `three-node` 0):

| result | where it now lives | status |
|---|---|---|
| Lean formalization of the volume threshold | `MainTheorem.lean` | post-deposit |
| algebraic Lyapunov solution + uniqueness + `det Σ = volume` | `Covariance.lean` | post-deposit |
| Lean formalization of the residual-variance criterion | `ResidualThreshold.lean` | post-deposit |
| reciprocal-threshold identities `s(r_A*)=6`, `s(r_D*)=4` | `CrossThreshold.lean` | post-deposit |
| cross-threshold spectral identity `q = (2+√3)²` | `CrossThreshold.lean` | post-deposit |
| active-plane palindromic determinant theorem and threshold equivalence | `ActivePlane.lean` | post-deposit |
| K₂/P3/K3 corollaries, including `35+15√5` and `247/2` | `ActivePlane.lean` | post-deposit |
| `J₂` closure and the `n ≥ 3` witness | `SpectralShape.lean` | post-deposit |
| three-node modal-channel analysis, `‖[Q,L]‖² = α²+β²`, weak/strong-coupling laws | external audits, not in the repository | post-deposit, not formalized |

The deposited record is **not wrong**; it is simply the **current deposited version**, while the
repository is the **current research and formalization state**. No Zenodo record was modified in
this pass.

## 4. Publication recommendation

**Recommendation: C — both, but sequenced, and with the second kept small.**

1. **A modest revision of the OU note** (`DeJesus2026ou`). Two things in it should change
   regardless of anything new: the interpretive correction of row 23 (the synchronization framing),
   and a pointer to the machine-checked companion. Both are already supported by work in hand.
2. **A separate short theorem note** for the active-plane result — but only if the wording of
   §11 of `LITERATURE_REVIEW.md` survives further search. Its case rests on *one* unclaimed item:
   the exact closed-form determinant response and the minimized threshold. Four of its five
   ingredients are standard and must be cited as such, so a standalone paper would spend most of
   its length on background. If it is written, its natural framing is the **linear-system** form
   (a two-dimensional drift-invariant plane), with the graph cases as corollaries — not as a
   graph paper.

Against option A alone: the active-plane theorem is more general than the deposited paper and
would distort it. Against option B alone: the two-node threshold is the reason anyone would read
the general statement, and it is already deposited. Conceptual unity therefore favours keeping the
OU note as the domain paper and the theorem note as the general one, cross-referenced.

**Not recommended:** any claim of priority, any use of "novel"/"first", or any suggestion that
the reciprocal coordinate, the `t + 1/t` substitution, the modal covariance formula, Mauchly's
statistic, or low-rank Lyapunov theory originate here. They do not.
