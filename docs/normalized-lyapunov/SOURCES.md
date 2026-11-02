# Prior-art audit

Classification follows the five categories requested: *already in this repository*; *classical
result applied here*; *new explanatory derivation for this project*; *potentially new
model-specific result, novelty not fully established*; *conjecture or refuted candidate*.

"No match found" is **not** evidence of novelty. Search was limited to a handful of targeted
queries on the specific mathematical objects involved; it was not a systematic survey, and no
paper below was read in full except where noted.

## Classical results applied here

| result | source | hypotheses | how used |
|---|---|---|---|
| Solution of `HS + SH = X` is the Schur multiplier by the Löwner/Cauchy kernel `1/(a_i+a_j)` in the eigenbasis | Bhatia, *Matrix Analysis* (GTM 169), Ch. VII; *Positive Definite Matrices*, Ch. 5 | `H = H* > 0` | Lemma 1 |
| `A ∘ B ⪰ 0` for `A, B ⪰ 0` (Schur product theorem) | Schur 1911 | PSD | complete positivity of `Φ_H` (Lemma 2) |
| Mean matrices `[m(a_i,a_j)/M(a_i,a_j)]` are PSD and infinitely divisible | Bhatia–Kosaki, *Mean matrices and infinite divisibility*, LAA 424 (2007); Bhatia–Jain, *Mean matrices and conditional negativity*, ELA | positive rates | `C` is a correlation matrix; checked in C7.1 |
| Multiplicative domain of a Schur-product channel `X ↦ C ∘ X` is `{X : X_{ij} = 0 whenever \|c_{ij}\| < 1}` | Choi 1974 (multiplicative domain of a UCP map); standard in the quantum-channel literature | `C` a correlation matrix | **Lemma 3** is this theorem specialized via `\|c_{ij}\| = 1 ⟺ a_i = a_j`; checked in C7.3 |
| Kadison–Schwarz inequality | Kadison 1952 | UCP map | sign of the square defect (4) |
| `det(A ∘ B) ≥ det B · ∏ A_ii` (Oppenheim) and `det(A∘B) ≥ det A det B` (Schur); equality conditions known | Oppenheim 1930; Schur; equality via RKHS in *Oppenheim–Schur's inequality and RKHS*, Oper. Matrices 18 (2024) | `A, B ⪰ 0` | **left half of Theorem A** and `det Φ_H(Q) ≥ det Q`; C7.4 |
| Hadamard's determinant inequality | Hadamard 1893 | PSD | **right half of Theorem A** (the ceiling) |
| Newton's inequalities (log-concavity of the coefficients of a real-rooted polynomial) | classical | all roots real (here all negative) | monotonicity of `q_m = [κ^m](DB)/[κ^m]B`, step (ii) of Theorem J |
| Descartes' rule of signs | classical; Mathlib `Polynomial.roots_countP_pos_le_signVariations` | real polynomial, roots with multiplicity | **Step 4 of Theorem H**; the nonpositive-tail sign-variation bound is proved on top of it in `ComponentCount.lean` |
| Oppenheim–Schur inequality (the sharper companion stated immediately after Oppenheim) | Yamada, *Oppenheim–Schur's inequality and RKHS*, Oper. Matrices 18 (2024), Thm 1.1(iii) | `A, B ≻ 0` | **Theorem A'**: `det(C∘Q̃)/det Q̃ ≥ 1 + det C (ρ-1)`, giving the explicit sufficient condition (6''') |
| Cauchy determinant formula | classical | distinct nodes | `det C = ∏_{i<j}((a_i-a_j)/(a_i+a_j))²` (6''), C8.3 |

**This is the main outcome of the audit.** Two statements that looked like new results during the
investigation are not:

* `det Φ_H(Q) ≥ det Q` **is Oppenheim's inequality** for a unit-diagonal `C`. Only the equality
  characterization (`⟺ [H,Q] = 0`) is specific to this kernel.
* the exact-preservation classification **is the multiplicative-domain theorem** for Schur
  channels. Only the computation `|c_{ij}| = 1 ⟺ a_i = a_j` is specific.

They are retained because the specializations are what the OU application needs, but they are
recorded as classical, not new.

## New explanatory derivations for this project

* **The normalization (7)** — `bracket = r²κ(anisotropy - couplingCost)`, with the exact floor
  `couplingCost - 32 = 8(κ-1)²/κ`. This gives meanings to the repository's `34` and `3 + 2√2`,
  shows `κ = 1` is optimal for every `r`, and yields a second proof of the main theorem with no
  discriminant and no SOS certificate. Formalized in Lean.
* **Theorem A** as a statement about this model: the sandwich
  `1/det H_κ ≤ det Σ_κ/det Σ_0 ≤ ρ(Q,L)/det H_κ`, and the consequence that expansion is confined
  to the bounded window `det H_κ < ρ(Q,L)`. Assembled from Oppenheim + Hadamard; the assembly and
  the identification of `ρ` as the orientation-sensitive Hadamard ratio of the rotated noise are
  this project's.
* **Theorem B** — `ratio'(0) = -tr L` and `ratio = Θ(κ^{-rank L})` with an exact constant.
  Elementary given Lemma 1, but it is the reason small coupling can never help.
* **The measured gap between (6''') and the true three-mode thresholds** (`7.52×` centre,
  `1.22×` end), with `det C = Θ(κ⁶)` identified as the cause. This is what tells us a sharper
  bound must retain the off-diagonal structure of `Q̃` rather than only `ρ` and `det C`.

## Potentially new model-specific results, novelty not fully established

* **Theorem C**: the certified three-mode brackets (`≈ 8.2781` centre, `≈ 10.7202` end) and the
  orientation dependence at fixed `spec(Q)`.
  Closest located prior art: Barucca, *Localization in covariance matrices of coupled
  heterogeneous Ornstein–Uhlenbeck processes*, Phys. Rev. E **90** (2014) 062129 — same family of
  models (heterogeneous temperatures, symmetric coupling) but it studies the **eigenvalue spectrum
  and an eigenvector localization transition for random couplings**, not the determinant of the
  stationary covariance for a fixed Laplacian. Also located and not matching: Barucca et al. on a
  random-matrix ensemble for heterogeneous-temperature OU covariances (arXiv:2409.01262);
  entropy-production work on multivariate OU (arXiv:2207.05197), which uses the zero-lag
  covariance fixed point but for a different functional. Neither was read in full.
  **No source stating a determinant/volume threshold in the noise anisotropy for a fixed symmetric
  OU network was found; this does not establish novelty.**

## Already in this repository

`volume`, `volume0`, `bracket`, `threshold`, `discr`, `cov`, `cov_lyapunov`, `lyapunov_unique`,
`det_cov`, `volume_gt_iff_bracket_gt`, `quartic_gt_iff_gt_threshold`,
`exists_volume_improvement_iff_threshold`. The new Lean file imports and reuses these; it
duplicates no definition and modifies no existing proof.

## Raised in review (2026-11-02), eighth round

The reviewer supplied **Theorem J**, a necessary cost for every component count on matching
patterns: `ρ_∞ > max{1 + 8(tr L)/s_*, q_{2c}}`, together with both ingredients that collapse the
band disjunction — the coefficientwise domination `N ⪯ (det Q)ρ_∞B` via the per-block identity
`n_j = 4 + 4sκ + s²r_∞κ²`, and the monotonicity of `q_m` from Newton's inequalities on `B` — plus
the saturation envelope `G ≤ 1 + (ρ_∞−1)u_*` behind the single-window term, the three-block floor
table, and the **endpoint qualification** that an interpolating bound must retain the sharp
single-pair `η > 8` rather than agree with Theorem I's weaker `η > 4`. Also two corrections: that
the certified boxes are not near-maximal (the printed thresholds were rounded; enlarging both radii
by `5/3` still passes), and that calling `c < k` generic needs a specified domain and measure.

Classification: **new explanatory derivation for this project**; its ingredients are classical
(Newton's inequalities; Oppenheim per block).

Attribution: the theorem, both ingredients, the endpoint qualification and both corrections are the
reviewer's. This repository verified the per-block identity and the domination across six matching
instances (including nonzero rates on both sides of a pair, equal rates within a pair, and extra
uncorrelated modes), confirmed `q_m` monotonicity at eleven rate configurations, reproduced all
three floors and the endpoint exactly, re-verified the enlarged boxes with the tightest bound
`1.001246350696674…`, and formalized the saturation envelope.

## Raised in review (2026-11-02), seventh round

The reviewer supplied **the sufficient criterion and the `k = 4, 5` sharpness families**: the
monotone envelope (16), the nominal parameters
`(a_j) = (1000, 1, 10⁻⁴, 10⁻⁸, 10⁻¹²)`, `(b_j) = (3, 60, 3500, 45000, 2000000)`, the box radii
(`±0.1%` in rates, `±0.25%` in strengths), the eleven certifying couplings and their bounds, and
the band constraint (17) for `c < k`. Together with the **correction that a lower bound on noise
strength alone cannot force several windows** — raising all `b_j` merges the windows, as
`b_j ↦ 10b_j` demonstrates — so a sufficient criterion must control separation.

Classification: **new explanatory derivation for this project** (the envelope and criterion are
elementary given the product form; the certified families are a construction). Whether such
parameter-box criteria for OU covariance volume appear in the literature was not determined.

Attribution: the criterion, the families, the band constraint and the merge correction are the
reviewer's. This repository verified the monotonicity and all eleven box bounds exactly, confirmed
the nominal counts and that both families saturate Descartes, checked five corners of each box
independently, verified the merge claim at the coefficient level, and formalized the envelope
(`gFactor_le_gFactor`, `blockRatio_mem_box`).

## Raised in review (2026-11-02), sixth round

The reviewer supplied **Theorem I, a necessary cost bound for attaining `c = k` components**:
`ρ_∞ > T(E,L) = [κ^{2k}](DB)/[κ^{2k}]B`, with `ρ > T` following by Hadamard; the closed form (15)
for three `(0,a_j)` blocks; the exact floor `T = 400400440125.444004…` at the witness's rates, the
forced `b₃ > 3334.538168…` (the witness's `3500` being ~5% above it), and the exclusion check at
`η₃ = 11000000`. Together with two corrections: that the bound is not optimal (`η > 4` for one
pair against the exact `8`), and that the §8 halving control needed its convention stated, since
halving off-diagonals with the diagonal fixed sends `η ↦ η/(4+3η) < 1/3`.

Classification: **new explanatory derivation for this project**, from Theorem H's coefficient
structure plus Hadamard. The aggregate `ρ` was already in use here (Theorem A).

Attribution: the bound, the closed form, the numerical consequences and both corrections are the
reviewer's. This repository verified (15) against the coefficient ratio at four rate triples,
confirmed `ρ_∞ = ρ` for disjoint `(0,a)` blocks numerically, reproduced the floor and the forced
`b₃` exactly, confirmed the `η₃ = 11000000` exclusion drops the sign count from 6 to 4, and
formalized the two numerical statements and the exclusion's logical shape.

## Raised in review (2026-11-02), fifth round

The reviewer supplied an **exact `k = 3` witness establishing sharpness of Theorem H**: three
*disjoint* correlated blocks `Q_b = [[1,b],[b,1+b²]]` with `b = 3, 60, 3500` against
`L = diag(0,1000,0,1,0,1/10000)`, the product form (13), seven alternating rational evaluations,
the coefficient sign pattern `−,+,−,+,−,+,−,−,−` saturating the `2k = 6` Descartes budget, and a
connected weighted-graph realization (inter-pair weight `ε = 10⁻⁸`, intra-pair `(a_j − 4ε)/2`) with
eigenvalues `0, a₁, a₂, a₃, 6ε, 6ε`. The reviewer also corrected the interpretation of sharpness:
it is attainment of a structural ceiling, not a claim that the component count is determined by the
correlation pattern.

Classification: **new model-specific result** (the witness), delimiting Theorem H exactly.
Attribution: the construction, the connected realization and the interpretive correction are the
reviewer's. This repository verified all seven values against `HΣ + ΣH = Q̃`, confirmed the tight
sign pattern by an independent polynomial route, verified the graph's eigenvalues by applying its
Laplacian to the explicit eigenvectors, formalized the sharpness statement
(`sharp3_not_union_of_two_convex`), and recorded that `k ≥ 4` attainment remains untested.

## Raised in review (2026-11-02), fourth round

The reviewer supplied a **proof of the component-count theorem** (Theorem H of
[DERIVATION.md](DERIVATION.md)): `k` correlated noise pairs ⟹ at most `k` expansion components,
via the common-denominator construction `N = B·det(C∘Q̃)` of degree `≤ 2k`, the numerator identity,
`A(0) = −4^k(det Q)(tr L)`, the nonpositive tail from degree `2k`, Descartes' rule, and two
boundary roots per component. The argument covers cycle terms, which an additive reading would
not. The reviewer also pointed to Mathlib's `Polynomial.roots_countP_pos_le_signVariations` for
formalization, and supplied four further corrections (non-additivity of per-pair contributions;
star patterns not forcing one interval; saturation scale `2/s`; the misreported `r = 9` peak and
the over-broad "never unimodal").

Classification: **new explanatory derivation for this project**, assembled from the determinant
identity (6) established here plus classical ingredients (permutation expansion, Descartes' rule
of signs). Whether the statement appears in the OU literature was not determined.

Attribution: the theorem, its proof, the Mathlib pointer and all four corrections are the
reviewer's. This repository verified Steps 1–3 exactly across 7 instances against independent
Lyapunov solves, formalized Step 4's combinatorial core
(`OUCorridor/ComponentCount.lean`), and recorded the `k ≥ 3` sharpness question with its linear
reduction for star patterns.

## Raised in review (2026-11-02), third round

The reviewer supplied an **exact counterexample refuting the general interval conjecture** (§7 of
[DERIVATION.md](DERIVATION.md)): `L = diag(0,100,1)`, `Q̃ = [[2035,3,45],[3,1,0],[45,0,1]]`, with
the three evaluations at `κ = 1/50, 1/10, 1`, the connected weighted-triangle realization
(`299/6, 1/3, 1/3`), the observation that the determinant cycle term vanishes so the mechanism is
two correlated pairs at different damping scales, the corrected diagnosis of the `7.5×` overshoot,
and the warning that "one expansion interval" must stay distinct from "unimodality".

Classification: **refuted candidate** (for the conjecture) plus **new model-specific result** (the
witness itself, which delimits Theorem F exactly). Attribution: the witness and all three
corrections are the reviewer's; this repository verified it against independent Lyapunov solves,
determined the component count, established that zeroing either correlation removes expansion
entirely, and formalized the refutation (`witness_expansion_set_not_convex`).

## Raised in review (2026-11-02), second round

A further review supplied the **single-correlated-pair theorem** (Theorems D–G of
[DERIVATION.md](DERIVATION.md)): the exact ratio (9), the normal form (★), strict convexity of `T`
with `T'' ≥ 8(tr L)/(Δ²κ³)`, the resulting uniqueness of the onset coupling and interval structure
of the expansion set, the degree-`(rank L + 1)` equation for `κ_†`, and the floor
`η_crit ≥ 8(tr L)s/Δ² ≥ 8`. It also corrected `det C ~ (9/16)κ⁶` (the factor `36` had been
dropped).

Classification: **new explanatory derivation for this project**, built from the determinant
identity (6) already established here plus elementary convexity. The individual ingredients are
classical (elementary symmetric functions; strict convexity of `κ ↦ 1/κ`; convexity of monomials
with nonnegative coefficients; `ConvexOn.convex_lt` for sublevel sets; uniqueness of minimizers of
strictly convex functions). Whether the *combination*, as a statement about symmetric OU networks,
appears in the literature was not determined — the same unresolved question as for Theorem C.

Attribution: the theorem and the `det C` correction are the reviewer's. This repository supplied
the determinant identity it is built on, the exact verification (`singlepair9.py`, 11 checks), the
Lean formalization of Theorems F and G (`OUCorridor/SinglePair.lean`), the additional instances
(`λ = (0,1,3)` pair `(1,2)`; `(0,1,1,4)`; `(2,2,5)`), and the observation that the interval
structure appears to persist outside the covered class.

## Raised in review (2026-11-02), verified here

An external reviewer supplied four corrections/additions, all confirmed by exact computation in
`review8.py` and adopted above:

1. the `κ = 1` optimality wording (derivative `((r-1/r)² - 32)/144` at `κ = 1`) — **correction**;
2. the decay exponent is `rank L` — **correction**;
3. the Oppenheim–Schur refinement already present in the cited source, with `det C` by Cauchy —
   **addition**, now Theorem A′, together with the observation that no rate-spread-only bound can
   improve on it (commuting `Q` gives ratio exactly `1`);
4. the centre-node closed form and the cubic `27κ³ + 36κ² - 8 = 0` giving
   `r_* = 8.2780690232…` inside the certified bracket — **addition**.

Attribution: items 1–4 are the reviewer's; the verification, the measured overshoot of (6''') and
the `Θ(κ⁶)` diagnosis of its cause are this repository's.

## Refuted candidate

* **"The expansion set `{κ > 0 : det Σ_κ > det Σ_0}` is always a single interval."** Posed here as
  the next question after the single-pair theorem, with supporting numerical evidence from the
  end-node model. **Refuted** by the exact two-pair witness above: expansion at `κ = 1/50`,
  contraction at `κ = 1/10`, expansion again at `κ = 1`. The supporting evidence was sound about
  the model it tested and simply did not reach the general claim.
* **"The certified boxes are nearly maximal, since the envelope lands within `10⁻³` of the
  bounds."** Claimed here; **wrong** — those were rounded presentation thresholds, and the radii
  can be enlarged by `5/3` and still pass.
* **"`c < k` is the generic case."** Asserted here without a domain or measure; **withdrawn**.
* **"A lower bound on the pair parameters `η_pq` would give a sufficient condition for `c`
  components."** Proposed here as the shape of the missing criterion; **refuted** — raising all
  strengths merges the windows into one. The criterion must bound strengths *and* preserve
  contraction gaps, which the envelope does by certifying both directions at interleaved couplings.
* **"Sharpness would mean the component count depends only on the correlation pattern."** Stated
  here when posing the sharpness question; **wrong** — sharpness is attainment of a ceiling. The
  same `k = 3` pattern with correlations scaled by `1/2` has zero components.
* **"Each correlated pair contributes an additive term, so star patterns should force one
  interval."** Conjectured here as the route to the component bound; **both halves refuted** —
  disjoint blocks multiply, and the counterexample is a star. The component bound is true anyway,
  by the common-denominator proof.
* **"The `7.5×` overshoot lives in the determinant cycle term."** Conjectured here; **refuted** —
  the centre-node model is single-pair and has no cycle term, and neither does the counterexample.
* **"The two-mode onset coupling `κ = 1` is universal."** Refuted: by Theorem F the onset coupling
  is the positive root of a degree-`(rank L + 1)` polynomial, equal to `1` only for the two-mode
  model. For the three-node path with centre noise it is `0.4120226592…`.
* **"The two-mode threshold `3 + 2√2` extends to many modes with the same constant."** Refuted by
  Theorem C: the three-mode critical ratios are `≈ 8.2781` and `≈ 10.7202`, both certified away
  from `5.8284`. The prompt's instruction not to extrapolate the two-mode off-diagonal
  determinant formula to `n ≥ 3` was correct.

## The motivating paper

Colbrook–Stepaniants, *spectral isometries* (arXiv:2610.40470v1) was used **as motivation only**,
not as a theorem. Its Theorem 1.1 (a unital surjective spectral isometry of a C*-algebra is a
Jordan isomorphism) suggested asking *when `Φ_H` preserves algebraic structure*, which led to
Lemma 3. But Lemma 3 is proved directly from (3), and its content coincides with the
multiplicative-domain theorem above; no hypothesis of the spectral-isometry paper is invoked
anywhere in this derivation, and its Prop. 4.2 / Lemma 3.2 are not used. A separate audit of that
paper against the RH work is in the `weil-window-control` repository
(`extensions/spectral-isometry-transfer-2026-11-02/`), with a no-transfer verdict.

## Attribution

The two-mode threshold `r > 3 + 2√2`, the `volume`/`bracket`/`discr` formulation, the covariance
construction and the main theorem are the repository's own prior results (`OUCorridor/Threshold.lean`,
`MainTheorem.lean`, `Covariance.lean`). This work reorganizes and extends them; it does not
rederive them independently of those definitions.
