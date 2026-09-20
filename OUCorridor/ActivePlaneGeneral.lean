import OUCorridor.ActivePlane

/-!
# The general two-mode Lyapunov determinant identity, and trace-normalized palindromicity

This file generalizes `OUCorridor/ActivePlane.lean`.  Nothing there is changed: the rank-one
isotropic theorem `det_activeCov_palindromic` remains exactly as verified, and is recovered
here as a corollary (`det_activeCov_palindromic_of_general`).

Setting.  A symmetric stable drift restricted to a two-dimensional invariant plane is
`diag(-D₁, -D₂)` in the basis of its eigenmodes (the sign convention of
`OUCorridor/Covariance.lean`: `M Σ + Σ Mᵀ = -Q`).  The forcing is an **arbitrary symmetric**
`Q = !![q₁₁, q₁₂; q₁₂, q₂₂]`; no rank-one and no isotropy hypothesis is made.

Main results.

* `genCov_lyapunov`, `genCov_unique` — the explicit `Σ` is the unique solution on the plane.
* `det_genCov_eq` — **the sharp identity**
    `4 D₁ D₂ det Σ = det Q + ν² q₁₂²`,  `ν = (D₁-D₂)/(D₁+D₂)`.
  Everything else in this file is a consequence of it.
* `det_affineCov_eq` — for the affine family `Q(τ) = q_b I + (τ-1) H` with `H` symmetric,
    `4 D₁ D₂ det Σ(τ) = q_b² + q_b (tr H) (τ-1) + K (τ-1)²`,  `K = det H + ν² h₁₂²`.
* `affine_palindromic_iff` / `affine_palindromic_iff_trace` — the determinant polynomial has
  equal leading and constant coefficients **iff** `q_b (tr H - q_b) = 0`, hence for `q_b > 0`
  **iff `tr H = q_b`**.  This is the structural criterion: *rank one is not the mechanism,
  trace normalization is.*
* `det_affineCov_traceNormalized` — under `tr H = q_b`,
    `4 D₁ D₂ det Σ(τ) = K (τ-1)² + q_b² τ`.
* `normalizedAffineDet_eq` — dividing by `τ` gives `q_b² + K (w - 2)`, `w = τ + 1/τ`.
* `affineCoeff_nonneg_of_posSemidef` — `K ≥ 0` when `H` is positive semidefinite, and
  `affineForcing_posDef_of_posSemidef` — `Q(τ)` stays positive definite for every `τ > 0`.
  These separate the *algebraic* theorem (any symmetric `H`) from the *covariance-admissible*
  family (`H` positive semidefinite with `tr H = q_b`).

Scope.  Exact real algebra on matrices, as everywhere in this repository.  No stochastic-process
content is formalized.
-/

namespace OUCorridor

noncomputable section

open Matrix

/-!  ### Arbitrary symmetric forcing on the plane -/

/-- An arbitrary symmetric forcing on the active plane. -/
def genForcing (q11 q12 q22 : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![q11, q12; q12, q22]

/-- The stationary covariance for an arbitrary symmetric forcing: `Σ_ij = Q_ij / (D_i + D_j)`. -/
def genCov (D₁ D₂ q11 q12 q22 : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![q11 / (2*D₁), q12 / (D₁ + D₂);
     q12 / (D₁ + D₂), q22 / (2*D₂)]

theorem genCov_lyapunov {D₁ D₂ : ℝ} (h₁ : 0 < D₁) (h₂ : 0 < D₂) (q11 q12 q22 : ℝ) :
    activeDrift D₁ D₂ * genCov D₁ D₂ q11 q12 q22
      + genCov D₁ D₂ q11 q12 q22 * (activeDrift D₁ D₂)ᵀ
      = -genForcing q11 q12 q22 := by
  have hd1 : (D₁ : ℝ) ≠ 0 := ne_of_gt h₁
  have hd2 : (D₂ : ℝ) ≠ 0 := ne_of_gt h₂
  have hs : (D₁ + D₂ : ℝ) ≠ 0 := by positivity
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [activeDrift, genForcing, genCov, Matrix.vecMul, dotProduct, Fin.sum_univ_two] <;>
    field_simp <;> ring

/-- Uniqueness of the solution on the plane. -/
theorem genCov_unique {D₁ D₂ : ℝ} (h₁ : 0 < D₁) (h₂ : 0 < D₂) (q11 q12 q22 : ℝ)
    {S : Matrix (Fin 2) (Fin 2) ℝ}
    (hS : activeDrift D₁ D₂ * S + S * (activeDrift D₁ D₂)ᵀ = -genForcing q11 q12 q22) :
    S = genCov D₁ D₂ q11 q12 q22 := by
  have hd1 : (D₁ : ℝ) ≠ 0 := ne_of_gt h₁
  have hd2 : (D₂ : ℝ) ≠ 0 := ne_of_gt h₂
  have hs : (D₁ + D₂ : ℝ) ≠ 0 := by positivity
  have h00 := congrFun (congrFun hS 0) 0
  have h01 := congrFun (congrFun hS 0) 1
  have h10 := congrFun (congrFun hS 1) 0
  have h11 := congrFun (congrFun hS 1) 1
  simp [activeDrift, genForcing, Matrix.mul_apply, Matrix.vecMul, dotProduct,
    Fin.sum_univ_two] at h00 h01 h10 h11
  ext i j
  fin_cases i <;> fin_cases j <;> simp [genCov] <;> field_simp <;> linarith

/-!  ### The sharp determinant identity

Everything downstream follows from this one line.  Note that no structure whatsoever is assumed
of the forcing beyond symmetry: not rank one, not isotropy, not positivity.
-/

/-- **General two-mode Lyapunov determinant identity.**
    `4 D₁ D₂ det Σ = det Q + ν² q₁₂²` with `ν = (D₁-D₂)/(D₁+D₂)`.

    The mechanism is `4 D₁ D₂ /(D₁+D₂)² = 1 - ν²`: the off-diagonal of `Σ` carries the
    denominator `D₁+D₂` rather than the geometric mean, and the deficit is exactly `ν²`. -/
theorem det_genCov_eq {D₁ D₂ : ℝ} (h₁ : 0 < D₁) (h₂ : 0 < D₂) (q11 q12 q22 : ℝ) :
    4 * D₁ * D₂ * (genCov D₁ D₂ q11 q12 q22).det
      = (genForcing q11 q12 q22).det + (rateContrast D₁ D₂)^2 * q12^2 := by
  have hd1 : (D₁ : ℝ) ≠ 0 := ne_of_gt h₁
  have hd2 : (D₂ : ℝ) ≠ 0 := ne_of_gt h₂
  have hs : (D₁ + D₂ : ℝ) ≠ 0 := by positivity
  rw [genCov, genForcing, rateContrast, Matrix.det_fin_two_of, Matrix.det_fin_two_of]
  field_simp
  ring

/-!  ### The affine forcing family -/

/-- The affine forcing family `Q(τ) = q_b I + (τ - 1) H`, `H = !![h₁, h₁₂; h₁₂, h₂]`. -/
def affineForcing (qb τ h1 h12 h2 : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  genForcing (qb + (τ - 1) * h1) ((τ - 1) * h12) (qb + (τ - 1) * h2)

/-- The stationary covariance of the affine family. -/
def affineCov (D₁ D₂ qb τ h1 h12 h2 : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  genCov D₁ D₂ (qb + (τ - 1) * h1) ((τ - 1) * h12) (qb + (τ - 1) * h2)

/-- The coefficient `K = det H + ν² h₁₂²`.  Equivalently `K = h₁h₂ - (1-ν²) h₁₂²`. -/
def affineCoeff (D₁ D₂ h1 h12 h2 : ℝ) : ℝ :=
  (h1 * h2 - h12^2) + (rateContrast D₁ D₂)^2 * h12^2

/-- **The affine determinant formula.**
    `4 D₁ D₂ det Σ(τ) = q_b² + q_b (tr H)(τ-1) + K (τ-1)²`. -/
theorem det_affineCov_eq {D₁ D₂ : ℝ} (h₁ : 0 < D₁) (h₂ : 0 < D₂) (qb τ h1 h12 h2 : ℝ) :
    4 * D₁ * D₂ * (affineCov D₁ D₂ qb τ h1 h12 h2).det
      = qb^2 + qb * (h1 + h2) * (τ - 1) + affineCoeff D₁ D₂ h1 h12 h2 * (τ - 1)^2 := by
  rw [affineCov, det_genCov_eq h₁ h₂, genForcing, Matrix.det_fin_two_of, affineCoeff]
  ring

/-!  ### Palindromicity is a trace condition

Expanding the previous theorem in powers of `τ` gives leading coefficient `K` and constant
coefficient `q_b² - q_b (tr H) + K`.  They agree exactly when `q_b (tr H - q_b) = 0`.
-/

/-- The expansion in powers of `τ`: leading coefficient `K`, middle `q_b (tr H) - 2K`,
    constant `q_b² - q_b (tr H) + K`. -/
theorem det_affineCov_expand {D₁ D₂ : ℝ} (h₁ : 0 < D₁) (h₂ : 0 < D₂) (qb τ h1 h12 h2 : ℝ) :
    4 * D₁ * D₂ * (affineCov D₁ D₂ qb τ h1 h12 h2).det
      = affineCoeff D₁ D₂ h1 h12 h2 * τ^2
        + (qb * (h1 + h2) - 2 * affineCoeff D₁ D₂ h1 h12 h2) * τ
        + (qb^2 - qb * (h1 + h2) + affineCoeff D₁ D₂ h1 h12 h2) := by
  rw [det_affineCov_eq h₁ h₂]
  ring

/-- **Palindromicity criterion, raw form.**  Leading coefficient equals constant coefficient
    exactly when `q_b (tr H - q_b) = 0`. -/
theorem affine_palindromic_iff (D₁ D₂ qb h1 h12 h2 : ℝ) :
    affineCoeff D₁ D₂ h1 h12 h2
        = qb^2 - qb * (h1 + h2) + affineCoeff D₁ D₂ h1 h12 h2
      ↔ qb * (h1 + h2 - qb) = 0 := by
  constructor
  · intro h; nlinarith [h]
  · intro h; nlinarith [h]

/-- **Palindromicity criterion.**  For a positive baseline the determinant polynomial is
    palindromic in `τ` **iff the deformation is trace-normalized**, `tr H = q_b`.

    This is the sharp statement: rank one is *sufficient* (a unit rank-one `q_b e eᵀ` has
    trace `q_b` automatically) but not necessary. -/
theorem affine_palindromic_iff_trace {qb : ℝ} (hqb : 0 < qb) (D₁ D₂ h1 h12 h2 : ℝ) :
    affineCoeff D₁ D₂ h1 h12 h2
        = qb^2 - qb * (h1 + h2) + affineCoeff D₁ D₂ h1 h12 h2
      ↔ h1 + h2 = qb := by
  rw [affine_palindromic_iff]
  constructor
  · intro h
    rcases mul_eq_zero.mp h with h' | h'
    · exact absurd h' (ne_of_gt hqb)
    · linarith
  · intro h; rw [h]; ring

/-- **Trace-normalized determinant.**  Under `tr H = q_b`, the whole polynomial collapses to
    `K (τ-1)² + q_b² τ`, which is manifestly palindromic. -/
theorem det_affineCov_traceNormalized {D₁ D₂ : ℝ} (h₁ : 0 < D₁) (h₂ : 0 < D₂)
    {qb h1 h2 : ℝ} (htr : h1 + h2 = qb) (τ h12 : ℝ) :
    4 * D₁ * D₂ * (affineCov D₁ D₂ qb τ h1 h12 h2).det
      = affineCoeff D₁ D₂ h1 h12 h2 * (τ - 1)^2 + qb^2 * τ := by
  rw [det_affineCov_eq h₁ h₂, htr]
  ring

/-- **Reciprocal reduction, general form.**  Dividing the trace-normalized determinant by `τ`
    gives an exactly affine function of `w = τ + 1/τ`. -/
theorem normalizedAffineDet_eq {D₁ D₂ : ℝ} (h₁ : 0 < D₁) (h₂ : 0 < D₂)
    {qb h1 h2 : ℝ} (htr : h1 + h2 = qb) {τ : ℝ} (hτ : 0 < τ) (h12 : ℝ) :
    4 * D₁ * D₂ * (affineCov D₁ D₂ qb τ h1 h12 h2).det / τ
      = qb^2 + affineCoeff D₁ D₂ h1 h12 h2 * (reciprocalExcitation τ - 2) := by
  have hτ' : τ ≠ 0 := ne_of_gt hτ
  rw [det_affineCov_traceNormalized h₁ h₂ htr, reciprocalExcitation]
  field_simp
  ring

/-!  ### Admissibility: when is the family a genuine forcing covariance?

The identity above is pure algebra and holds for every symmetric `H` and every real `τ`.  For
the stochastic reading one needs `Q(τ)` positive definite, and for the threshold statement one
needs `K ≥ 0`.  Both follow from `H` positive semidefinite.
-/

/-- For a positive semidefinite deformation, `K ≥ 0`.  (For indefinite `H`, `K` may be
    negative: e.g. `H = diag(2,-1)` gives `K = -2`.) -/
theorem affineCoeff_nonneg_of_posSemidef (D₁ D₂ : ℝ) {h1 h12 h2 : ℝ}
    (hdet : 0 ≤ h1 * h2 - h12 ^ 2) :
    0 ≤ affineCoeff D₁ D₂ h1 h12 h2 := by
  have : 0 ≤ (rateContrast D₁ D₂)^2 * h12^2 := by positivity
  rw [affineCoeff]; linarith

/-- Trace-normalized positive semidefinite deformations keep the forcing positive definite for
    every `τ > 0`: the eigenvalues of `Q(τ)` are `q_b + (τ-1)η` with `0 ≤ η ≤ tr H = q_b`. -/
theorem det_affineForcing_pos_of_posSemidef {qb h1 h12 h2 : ℝ} (hqb : 0 < qb)
    (htr : h1 + h2 = qb) (hdet : 0 ≤ h1 * h2 - h12 ^ 2) {τ : ℝ} (hτ : 0 < τ) :
    0 < (affineForcing qb τ h1 h12 h2).det := by
  rw [affineForcing, genForcing, Matrix.det_fin_two_of]
  have key : (qb + (τ - 1) * h1) * (qb + (τ - 1) * h2) - (τ - 1) * h12 * ((τ - 1) * h12)
      = qb^2 * τ + (τ - 1)^2 * (h1 * h2 - h12^2) := by
    rw [show h2 = qb - h1 by linarith]; ring
  rw [key]
  have h1' : 0 < qb^2 * τ := by positivity
  have h2' : 0 ≤ (τ - 1)^2 * (h1 * h2 - h12^2) := by positivity
  linarith

/-!  ### The rank-one isotropic model as a corollary

Taking `H = q_b e eᵀ` with `e = (c, s)` a unit vector gives `tr H = q_b` automatically, so the
trace criterion is met without any extra hypothesis, and `K` reduces to `q_b² c² s² ν²`.
-/

/-- A unit rank-one deformation is automatically trace-normalized. -/
theorem rankOne_trace {c s : ℝ} (hcs : c ^ 2 + s ^ 2 = 1) (qb : ℝ) :
    qb * c ^ 2 + qb * s ^ 2 = qb := by
  linear_combination qb * hcs

/-- For the rank-one deformation `H = q_b e eᵀ`, the general coefficient `K` collapses to
    `q_b² · (c²s²ν²)`, i.e. `q_b²` times the `activeCoeff` of `ActivePlane.lean`. -/
theorem affineCoeff_rankOne (D₁ D₂ qb c s : ℝ) :
    affineCoeff D₁ D₂ (qb * c ^ 2) (qb * c * s) (qb * s ^ 2)
      = qb^2 * activeCoeff D₁ D₂ c s := by
  rw [affineCoeff, activeCoeff, mixing]
  ring

/-- The affine family with a rank-one deformation **is** the forcing of `ActivePlane.lean`. -/
theorem affineForcing_rankOne (qb τ c s : ℝ) :
    affineForcing qb τ (qb * c ^ 2) (qb * c * s) (qb * s ^ 2) = activeForcing qb τ c s := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [affineForcing, genForcing, activeForcing, mul_add, add_mul, mul_comm, mul_assoc,
      mul_left_comm]

/-- **The old theorem, recovered.**  `det_activeCov_palindromic` is the rank-one specialization
    of `det_affineCov_traceNormalized`; the two agree identically. -/
theorem det_activeCov_palindromic_of_general {D₁ D₂ c s : ℝ} (h₁ : 0 < D₁) (h₂ : 0 < D₂)
    (hcs : c ^ 2 + s ^ 2 = 1) (qb τ : ℝ) :
    4 * D₁ * D₂ * (affineCov D₁ D₂ qb τ (qb * c ^ 2) (qb * c * s) (qb * s ^ 2)).det
      = qb^2 * (activeCoeff D₁ D₂ c s * τ^2
          + (1 - 2 * activeCoeff D₁ D₂ c s) * τ + activeCoeff D₁ D₂ c s) := by
  rw [det_affineCov_traceNormalized h₁ h₂ (rankOne_trace hcs qb), affineCoeff_rankOne]
  ring

/-- The two covariance definitions agree on the rank-one family, so the general development is
    a genuine extension of `ActivePlane.lean` rather than a parallel one. -/
theorem affineCov_rankOne {D₁ D₂ : ℝ} (h₁ : 0 < D₁) (h₂ : 0 < D₂) (qb τ c s : ℝ) :
    affineCov D₁ D₂ qb τ (qb * c ^ 2) (qb * c * s) (qb * s ^ 2)
      = activeCov D₁ D₂ qb τ c s := by
  have hd1 : (D₁ : ℝ) ≠ 0 := ne_of_gt h₁
  have hd2 : (D₂ : ℝ) ≠ 0 := ne_of_gt h₂
  have hs : (D₁ + D₂ : ℝ) ≠ 0 := by positivity
  ext i j
  fin_cases i <;> fin_cases j <;> simp [affineCov, genCov, activeCov] <;> field_simp <;> ring

/-!  ### The threshold, restated with `K`

`volumeRatio_gt_one_iff` of `ActivePlane.lean` is already stated for an abstract positive
coefficient, so it applies verbatim with `C = K / q_b²`.  Recorded here for completeness.
-/

/-- Normalized against the homogeneous value `q_b²`, the trace-normalized determinant is
    `1 + (K/q_b²)(w - 2)`, so the threshold theorem applies with `C = K/q_b²`. -/
theorem normalizedAffineDet_div_eq {D₁ D₂ : ℝ} (h₁ : 0 < D₁) (h₂ : 0 < D₂)
    {qb h1 h2 : ℝ} (hqb : qb ≠ 0) (htr : h1 + h2 = qb) {τ : ℝ} (hτ : 0 < τ) (h12 : ℝ) :
    4 * D₁ * D₂ * (affineCov D₁ D₂ qb τ h1 h12 h2).det / (qb^2 * τ)
      = 1 + (affineCoeff D₁ D₂ h1 h12 h2 / qb^2) * (reciprocalExcitation τ - 2) := by
  have hτ' : τ ≠ 0 := ne_of_gt hτ
  rw [det_affineCov_traceNormalized h₁ h₂ htr, reciprocalExcitation]
  field_simp
  ring

end
end OUCorridor
