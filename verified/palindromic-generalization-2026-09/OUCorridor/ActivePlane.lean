import OUCorridor.CrossThreshold

/-!
# Two-mode active-plane reduction under rank-one heterogeneous forcing

This file is independent of the graph: it is a statement about a `2 × 2` block.

Setting. A symmetric stable drift restricted to a two-dimensional invariant plane is
`diag(-D₁, -D₂)` in the basis of its two eigenmodes (the sign convention of
`OUCorridor/Covariance.lean`: `M Σ + Σ Mᵀ = -Q`). The forcing on that plane is an
isotropic baseline `q_b` deformed at rank one along a unit excitation direction
`e = (c, s)`, `c² + s² = 1`:

  `Q(τ) = q_b (I + (τ - 1) e eᵀ)`,  eigenvalues `q_b τ` (along `e`) and `q_b` (along `e^⊥`).

Here `e` is the **excitation direction**, not Euler's number, and `τ > 0` is the ratio of
the deformed forcing eigenvalue to the baseline one.

Main results.

* `activeCov_lyapunov`, `activeCov_unique` — the explicit `Σ` is the unique solution of the
  algebraic Lyapunov equation on the plane.
* `activeForcing_self_dual` — `Q_e(τ) = τ • Q_{e^⊥}(1/τ)`, which is the exact source of the
  reciprocal structure (it is `e eᵀ + e^⊥ e^⊥ᵀ = I` in disguise).
* `det_activeCov_palindromic` — `4 D₁ D₂ det Σ = q_b² (A τ² + (1 - 2A) τ + A)`: a
  **palindromic** quadratic in `τ`, with `A = c²s²ν²`, `ν = (D₁-D₂)/(D₁+D₂)`.
* `normalizedActiveDet_eq` — dividing by `τ` turns that into `1 + A (w - 2)` with
  `w = τ + 1/τ`. The reciprocal coordinate is introduced *only* after the palindromic
  identity is available.
* `volumeRatio_gt_one_iff` — the elementary threshold equivalence.
* `volume_div_volume0_eq` — the repository's own two-node `volume/volume0` is an instance,
  with `τ = r²` (a *variance* ratio, not the amplitude ratio `r`).

Scope. Everything here is exact real algebra on matrices, as in the rest of the repository.
No stochastic-process content is formalized.
-/

namespace OUCorridor

noncomputable section

open Matrix

/-- Drift of the active plane, in the basis of its two eigenmodes (rates `D₁`, `D₂`). -/
def activeDrift (D₁ D₂ : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![-D₁, 0; 0, -D₂]

/-- Rank-one deformed forcing `q_b (I + (τ-1) e eᵀ)` with excitation direction `e = (c, s)`. -/
def activeForcing (qb τ c s : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![qb * (1 + (τ - 1) * c ^ 2), qb * (τ - 1) * c * s;
     qb * (τ - 1) * c * s, qb * (1 + (τ - 1) * s ^ 2)]

/-- The stationary covariance on the active plane: `Σ_ij = Q_ij / (D_i + D_j)`. -/
def activeCov (D₁ D₂ qb τ c s : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![qb * (1 + (τ - 1) * c ^ 2) / (2*D₁), qb * (τ - 1) * c * s / (D₁ + D₂);
     qb * (τ - 1) * c * s / (D₁ + D₂), qb * (1 + (τ - 1) * s ^ 2) / (2*D₂)]

/-- Rate contrast of the active pair, `ν = (D₁ - D₂)/(D₁ + D₂)`. -/
def rateContrast (D₁ D₂ : ℝ) : ℝ := (D₁ - D₂) / (D₁ + D₂)

/-- Modal mixing of the excitation direction, `c² s²`. -/
def mixing (c s : ℝ) : ℝ := c ^ 2 * s ^ 2

/-- The coefficient of the reciprocal coordinate: `A = c² s² ν²`. -/
def activeCoeff (D₁ D₂ c s : ℝ) : ℝ := mixing c s * (rateContrast D₁ D₂)^2

/-- The reciprocal coordinate `w = τ + 1/τ`. -/
def reciprocalExcitation (τ : ℝ) : ℝ := τ + 1 / τ

/-!  ### The Lyapunov solution on the plane -/

theorem activeCov_lyapunov {D₁ D₂ : ℝ} (h₁ : 0 < D₁) (h₂ : 0 < D₂) (qb τ c s : ℝ) :
    activeDrift D₁ D₂ * activeCov D₁ D₂ qb τ c s
      + activeCov D₁ D₂ qb τ c s * (activeDrift D₁ D₂)ᵀ
      = -activeForcing qb τ c s := by
  have hd1 : (D₁ : ℝ) ≠ 0 := ne_of_gt h₁
  have hd2 : (D₂ : ℝ) ≠ 0 := ne_of_gt h₂
  have hs : (D₁ + D₂ : ℝ) ≠ 0 := by positivity
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [activeDrift, activeForcing, activeCov, Matrix.vecMul,
      dotProduct, Fin.sum_univ_two] <;>
    field_simp <;> ring

/-- Uniqueness: the Lyapunov equation on the plane has exactly one solution. -/
theorem activeCov_unique {D₁ D₂ : ℝ} (h₁ : 0 < D₁) (h₂ : 0 < D₂) (qb τ c s : ℝ)
    {S : Matrix (Fin 2) (Fin 2) ℝ}
    (hS : activeDrift D₁ D₂ * S + S * (activeDrift D₁ D₂)ᵀ = -activeForcing qb τ c s) :
    S = activeCov D₁ D₂ qb τ c s := by
  have hd1 : (D₁ : ℝ) ≠ 0 := ne_of_gt h₁
  have hd2 : (D₂ : ℝ) ≠ 0 := ne_of_gt h₂
  have hs : (D₁ + D₂ : ℝ) ≠ 0 := by positivity
  have h00 := congrFun (congrFun hS 0) 0
  have h01 := congrFun (congrFun hS 0) 1
  have h10 := congrFun (congrFun hS 1) 0
  have h11 := congrFun (congrFun hS 1) 1
  simp [activeDrift, activeForcing, Matrix.mul_apply, Matrix.vecMul, dotProduct,
    Fin.sum_univ_two] at h00 h01 h10 h11
  ext i j
  fin_cases i <;> fin_cases j <;> simp [activeCov] <;> field_simp <;> linarith

/-!  ### The self-duality behind the reciprocal structure -/

/-- With `e = (c, s)` a unit vector and `e^⊥ = (-s, c)`,
    `Q_e(τ) = τ • Q_{e^⊥}(1/τ)`.  This is `e eᵀ + e^⊥ e^⊥ᵀ = I` written out, and it is the
    exact reason the determinant below is palindromic. -/
theorem activeForcing_self_dual {c s τ σ qb : ℝ} (hcs : c ^ 2 + s ^ 2 = 1) (hστ : σ * τ = 1) :
    activeForcing qb τ c s = τ • activeForcing qb σ (-s) c := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [activeForcing]
  · linear_combination (qb * (τ - 1)) * hcs + (-(qb * s ^ 2)) * hστ
  · linear_combination (qb * c * s) * hστ
  · linear_combination (qb * c * s) * hστ
  · linear_combination (qb * (τ - 1)) * hcs + (-(qb * c ^ 2)) * hστ

/-- The same duality in the form used informally: with `τ ≠ 0` one may take `σ = 1/τ`. -/
theorem activeForcing_self_dual_inv {c s τ qb : ℝ} (hcs : c ^ 2 + s ^ 2 = 1) (hτ : τ ≠ 0) :
    activeForcing qb τ c s = τ • activeForcing qb (1/τ) (-s) c :=
  activeForcing_self_dual hcs (by field_simp)

/-!  ### The palindromic determinant identity -/

/-- The forcing block has determinant `q_b² τ` (eigenvalues `q_b τ` and `q_b`). -/
theorem det_activeForcing {c s : ℝ} (hcs : c ^ 2 + s ^ 2 = 1) (qb τ : ℝ) :
    (activeForcing qb τ c s).det = qb^2 * τ := by
  rw [activeForcing, Matrix.det_fin_two_of]
  linear_combination (qb^2 * (τ - 1)) * hcs

/-- **Palindromic determinant.** `4 D₁ D₂ det Σ = q_b² (A τ² + (1 - 2A) τ + A)` with
    `A = c² s² ν²`: the leading and constant coefficients in `τ` coincide. -/
theorem det_activeCov_palindromic {D₁ D₂ c s : ℝ} (h₁ : 0 < D₁) (h₂ : 0 < D₂)
    (hcs : c ^ 2 + s ^ 2 = 1) (qb τ : ℝ) :
    4 * D₁ * D₂ * (activeCov D₁ D₂ qb τ c s).det
      = qb^2 * (activeCoeff D₁ D₂ c s * τ^2
          + (1 - 2 * activeCoeff D₁ D₂ c s) * τ + activeCoeff D₁ D₂ c s) := by
  have hd1 : (D₁ : ℝ) ≠ 0 := ne_of_gt h₁
  have hd2 : (D₂ : ℝ) ≠ 0 := ne_of_gt h₂
  have hsum : (D₁ + D₂ : ℝ) ≠ 0 := by positivity
  -- the forcing block has determinant qb^2 τ (already proved), written out:
  have hQ : (qb * (1 + (τ - 1) * c ^ 2)) * (qb * (1 + (τ - 1) * s ^ 2))
      - (qb * (τ - 1) * c * s) * (qb * (τ - 1) * c * s) = qb^2 * τ := by
    have h := det_activeForcing hcs qb τ
    rw [activeForcing, Matrix.det_fin_two_of] at h
    linarith [h]
  -- clearing denominators, with no use of the constraint:
  have hsplit : 4 * D₁ * D₂ * (D₁ + D₂)^2 * (activeCov D₁ D₂ qb τ c s).det
      = (qb * (1 + (τ - 1) * c ^ 2)) * (qb * (1 + (τ - 1) * s ^ 2)) * (D₁ + D₂)^2
        - 4 * D₁ * D₂ * ((qb * (τ - 1) * c * s) * (qb * (τ - 1) * c * s)) := by
    rw [activeCov, Matrix.det_fin_two_of]
    field_simp
    ring
  -- now a pure polynomial step, using hQ exactly once
  have hkey : 4 * D₁ * D₂ * (D₁ + D₂)^2 * (activeCov D₁ D₂ qb τ c s).det
      = qb^2 * ((D₁ + D₂)^2 * τ + c ^ 2*s ^ 2*(D₁ - D₂)^2 * (τ - 1)^2) := by
    rw [hsplit]; linear_combination ((D₁ + D₂)^2) * hQ
  rw [activeCoeff, mixing, rateContrast]
  field_simp
  linear_combination hkey

/-!  ### The reciprocal coordinate, introduced only now -/

theorem two_le_reciprocalExcitation {τ : ℝ} (hτ : 0 < τ) : 2 ≤ reciprocalExcitation τ := by
  have h : reciprocalExcitation τ - 2 = (τ - 1)^2 / τ := by
    rw [reciprocalExcitation]; field_simp; ring
  have h2 : 0 ≤ (τ - 1)^2 / τ := div_nonneg (sq_nonneg _) hτ.le
  linarith

theorem reciprocalExcitation_eq_two_iff {τ : ℝ} (hτ : 0 < τ) :
    reciprocalExcitation τ = 2 ↔ τ = 1 := by
  have h : reciprocalExcitation τ - 2 = (τ - 1)^2 / τ := by
    rw [reciprocalExcitation]; field_simp; ring
  constructor
  · intro he
    have hz : (τ - 1)^2 / τ = 0 := by rw [← h, he]; ring
    have : (τ - 1)^2 = 0 := by
      rcases div_eq_zero_iff.mp hz with h' | h'
      · exact h'
      · exact absurd h' (ne_of_gt hτ)
    have := pow_eq_zero_iff (n := 2) (a := τ - 1) two_ne_zero |>.mp this
    linarith
  · rintro rfl; rw [reciprocalExcitation]; norm_num

/-- **Normalized active determinant.** Dividing the palindromic quadratic by `τ` gives an
    exactly affine function of the reciprocal coordinate. -/
theorem normalizedActiveDet_eq {D₁ D₂ c s qb τ : ℝ} (h₁ : 0 < D₁) (h₂ : 0 < D₂)
    (hcs : c ^ 2 + s ^ 2 = 1) (hqb : qb ≠ 0) (hτ : 0 < τ) :
    4 * D₁ * D₂ * (activeCov D₁ D₂ qb τ c s).det / (qb^2 * τ)
      = 1 + activeCoeff D₁ D₂ c s * (reciprocalExcitation τ - 2) := by
  have hpal := det_activeCov_palindromic h₁ h₂ hcs qb τ
  rw [hpal, reciprocalExcitation]
  field_simp
  ring

/-!  ### Size and vanishing of the coefficient -/

theorem rateContrast_sq_lt_one {D₁ D₂ : ℝ} (h₁ : 0 < D₁) (h₂ : 0 < D₂) :
    (rateContrast D₁ D₂)^2 < 1 := by
  have hsum : (0 : ℝ) < D₁ + D₂ := by linarith
  rw [rateContrast, div_pow, div_lt_one (by positivity)]
  nlinarith

theorem mixing_le_quarter {c s : ℝ} (hcs : c ^ 2 + s ^ 2 = 1) : mixing c s ≤ 1/4 := by
  rw [mixing]
  nlinarith [sq_nonneg (c ^ 2 - s ^ 2)]

theorem mixing_eq_quarter_iff {c s : ℝ} (hcs : c ^ 2 + s ^ 2 = 1) :
    mixing c s = 1/4 ↔ c ^ 2 = 1/2 ∧ s ^ 2 = 1/2 := by
  rw [mixing]
  constructor
  · intro h
    have hsq : (c ^ 2 - s ^ 2)^2 = 0 := by nlinarith
    have : c ^ 2 - s ^ 2 = 0 := by
      nlinarith [pow_eq_zero_iff (n := 2) (a := c ^ 2 - s ^ 2) two_ne_zero |>.mp hsq]
    constructor <;> linarith
  · rintro ⟨hc, hs⟩; rw [hc, hs]; norm_num

theorem activeCoeff_nonneg (D₁ D₂ c s : ℝ) : 0 ≤ activeCoeff D₁ D₂ c s := by
  rw [activeCoeff, mixing]; positivity

/-- The reciprocal contribution vanishes exactly in the degenerate cases: the excitation
    lies in a single active mode, or the two active rates coincide. -/
theorem activeCoeff_eq_zero_iff {D₁ D₂ c s : ℝ} (h₁ : 0 < D₁) (h₂ : 0 < D₂) :
    activeCoeff D₁ D₂ c s = 0 ↔ c = 0 ∨ s = 0 ∨ D₁ = D₂ := by
  have hsum : (0 : ℝ) < D₁ + D₂ := by linarith
  rw [activeCoeff, mixing, rateContrast, div_pow, mul_eq_zero, mul_eq_zero, div_eq_zero_iff]
  constructor
  · rintro (h | h)
    · rcases h with h | h
      · exact Or.inl (by nlinarith [pow_eq_zero_iff (n := 2) (a := c) two_ne_zero |>.mp h])
      · exact Or.inr (Or.inl (by nlinarith [pow_eq_zero_iff (n := 2) (a := s) two_ne_zero |>.mp h]))
    · rcases h with h | h
      · refine Or.inr (Or.inr ?_)
        have : D₁ - D₂ = 0 := by
          nlinarith [pow_eq_zero_iff (n := 2) (a := D₁ - D₂) two_ne_zero |>.mp h]
        linarith
      · exact absurd h (by positivity)
  · rintro (rfl | rfl | rfl)
    · exact Or.inl (Or.inl (by ring))
    · exact Or.inl (Or.inr (by ring))
    · exact Or.inr (Or.inl (by ring))

/-!  ### The threshold equivalence -/

/-- Elementary threshold equivalence, denominator-free form (pure rearrangement). -/
theorem volumeRatio_gt_one_iff_mul (Φ C w : ℝ) :
    Φ * (1 + C * (w - 2)) > 1 ↔ Φ * C * (w - 2) > 1 - Φ := by
  constructor <;> intro h <;> nlinarith [h]

/-- Threshold equivalence in solved form: with a positive prefactor and a positive
    coefficient, the ratio exceeds one exactly above an explicit reciprocal-coordinate value. -/
theorem volumeRatio_gt_one_iff {Φ C w : ℝ} (hΦ : 0 < Φ) (hC : 0 < C) :
    Φ * (1 + C * (w - 2)) > 1 ↔ w > 2 + (1 - Φ) / (Φ * C) := by
  have hpos : (0 : ℝ) < Φ * C := by positivity
  have key : w - (2 + (1 - Φ) / (Φ * C)) = (Φ * (1 + C * (w - 2)) - 1) / (Φ * C) := by
    field_simp; ring
  constructor
  · intro h
    have h1 : 0 < (Φ * (1 + C * (w - 2)) - 1) / (Φ * C) := div_pos (by linarith) hpos
    rw [← key] at h1
    linarith
  · intro h
    have h1 : 0 < w - (2 + (1 - Φ) / (Φ * C)) := by linarith
    rw [key] at h1
    have h2 := (div_pos_iff_of_pos_right hpos).mp h1
    linarith

/-!  ### Two-node corollary: the repository's own volume ratio is an instance

The two-node model of `OUCorridor/Threshold.lean` has `Q = diag(1, r²)`, i.e. a rank-one
deformation of the identity along the second node's basis vector.  In the drift eigenbasis
`u₀ = (1,1)/√2`, `u₁ = (1,-1)/√2` that direction has `c² = s² = 1/2`, so `mixing = 1/4`;
the active rates are `D₁ = a = 1` (common mode) and `D₂ = a + 2κ` (relative mode), and the
deformation parameter is the **variance** ratio `τ = r²`, not the amplitude ratio `r`.
-/

/-- **K₂ corollary.**  `volume/volume0` is exactly the active-plane formula. -/
theorem volume_div_volume0_eq {κ r : ℝ} (hκ : 0 ≤ κ) (hr : r ≠ 0) :
    volume κ r / volume0 r
      = (1 / (1 + 2*κ))
        * (1 + (1/4) * (rateContrast 1 (1 + 2*κ))^2 * (reciprocalExcitation (r^2) - 2)) := by
  have h1 : (κ + 1 : ℝ) ≠ 0 := by positivity
  have h2 : (2*κ + 1 : ℝ) ≠ 0 := by positivity
  have h3 : (r^2 : ℝ) ≠ 0 := pow_ne_zero 2 hr
  rw [volume, volume0, rateContrast, reciprocalExcitation]
  field_simp
  ring

/-- The parameterization bridge: the rank-one parameter is the **variance** ratio, so its
    reciprocal coordinate is the square of the amplitude one, minus two.  This is why
    `r + 1/r = 6` (amplitude) and `w = 34` (variance) describe the same threshold. -/
theorem reciprocalExcitation_sq {r : ℝ} (hr : r ≠ 0) :
    reciprocalExcitation (r^2) = (reciprocalInvariant r)^2 - 2 := by
  rw [reciprocalExcitation, reciprocalInvariant]
  field_simp
  ring

/-- At the existing volume threshold `r_A* = 3 + 2√2`, the reciprocal coordinate is `34`. -/
theorem reciprocalExcitation_threshold_sq : reciprocalExcitation (threshold^2) = 34 := by
  rw [reciprocalExcitation_sq threshold_pos.ne', threshold_reciprocalInvariant]
  norm_num

/-!  ### Graph corollaries: the exact P3 and K3 constants

For a graph drift `aI + κL` the active rates are `D₁ = a` (common mode) and `D₂ = a + κλ`
(one relative eigenmode), so `ν = -κλ/(2a + κλ)`, and the passive modes enter only through
`Φ = ∏_{j≥1} a/(a + κλ_j)`.  The threshold value of the reciprocal coordinate is then
`thresholdCurve Φ C` with `C = c²s²ν²`, minimized over `κ`.

Below, both curves are *derived* from `thresholdCurve` for the relevant data and then minimized
exactly; no constant is fitted.
-/

/-- The threshold value of the reciprocal coordinate, from `volumeRatio_gt_one_iff`. -/
def thresholdCurve (Φ C : ℝ) : ℝ := 2 + (1 - Φ) / (Φ * C)

/-- P3 with heterogeneity at the centre node: `λ = 3`, `c² = 1/3`, `s² = 2/3`
    (so `C = c²s²ν² = 2κ²/(2+3κ)²`), passive mode `λ = 1`, `Φ = 1/((1+κ)(1+3κ))`. -/
theorem p3_thresholdCurve_eq {κ : ℝ} (hκ : 0 < κ) :
    thresholdCurve (1 / ((1 + κ) * (1 + 3*κ))) (2*κ ^ 2 / (2 + 3*κ) ^ 2)
      = (27*κ ^ 3 + 72*κ ^ 2 + 64*κ + 16) / (2*κ) := by
  have h1 : (1 + κ : ℝ) ≠ 0 := by positivity
  have h2 : (1 + 3*κ : ℝ) ≠ 0 := by positivity
  have h3 : (2 + 3*κ : ℝ) ≠ 0 := by positivity
  have h4 : (κ : ℝ) ≠ 0 := ne_of_gt hκ
  rw [thresholdCurve]
  field_simp
  ring

/-- K3 with heterogeneity at any node: `λ = 3`, `c² = 1/3`, same `C`, passive mode `λ = 3`,
    `Φ = 1/(1+3κ)²`. -/
theorem k3_thresholdCurve_eq {κ : ℝ} (hκ : 0 < κ) :
    thresholdCurve (1 / (1 + 3*κ) ^ 2) (2*κ ^ 2 / (2 + 3*κ) ^ 2)
      = (81*κ ^ 3 + 162*κ ^ 2 + 112*κ + 24) / (2*κ) := by
  have h2 : (1 + 3*κ : ℝ) ≠ 0 := by positivity
  have h3 : (2 + 3*κ : ℝ) ≠ 0 := by positivity
  have h4 : (κ : ℝ) ≠ 0 := ne_of_gt hκ
  rw [thresholdCurve]
  field_simp
  ring

/-- **P3 constant.**  The P3 threshold curve is bounded below by `35 + 15√5`. -/
theorem p3_threshold_min {κ : ℝ} (hκ : 0 < κ) :
    35 + 15 * Real.sqrt 5 ≤ (27*κ ^ 3 + 72*κ ^ 2 + 64*κ + 16) / (2*κ) := by
  have h5 : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
  have h5pos : 0 < Real.sqrt 5 := Real.sqrt_pos.mpr (by norm_num)
  have hfac : 27*κ ^ 3 + 72*κ ^ 2 + 64*κ + 16 - (35 + 15 * Real.sqrt 5) * (2*κ)
      = 9 * (κ - (Real.sqrt 5 - 1)/3) ^ 2 * (3*κ + 6 + 2 * Real.sqrt 5) := by
    linear_combination (9*κ - 2*Real.sqrt 5 - 2) * h5
  rw [le_div_iff₀ (by positivity : (0:ℝ) < 2*κ)]
  nlinarith [sq_nonneg (κ - (Real.sqrt 5 - 1)/3), hfac, h5pos, hκ]

/-- The P3 bound is attained at `κ* = (√5 - 1)/3`. -/
theorem p3_threshold_attained :
    (27*((Real.sqrt 5 - 1)/3) ^ 3 + 72*((Real.sqrt 5 - 1)/3) ^ 2
        + 64*((Real.sqrt 5 - 1)/3) + 16) / (2*((Real.sqrt 5 - 1)/3))
      = 35 + 15 * Real.sqrt 5 := by
  have h5 : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
  have h5pos : 0 < Real.sqrt 5 := Real.sqrt_pos.mpr (by norm_num)
  have hne : ((Real.sqrt 5 - 1)/3 : ℝ) ≠ 0 := by
    have : (1:ℝ) < Real.sqrt 5 := by nlinarith
    positivity
  rw [div_eq_iff (by positivity : (2*((Real.sqrt 5 - 1)/3) : ℝ) ≠ 0)]
  linear_combination (Real.sqrt 5 - 5) * h5

/-- **K3 constant.**  The K3 threshold curve is bounded below by `247/2`, attained at `κ = 1/3`.
    Here the factorization is rational: `81κ³ + 162κ² - 135κ + 24 = 3(3κ-1)²(3κ+8)`. -/
theorem k3_threshold_min {κ : ℝ} (hκ : 0 < κ) :
    (247 : ℝ)/2 ≤ (81*κ ^ 3 + 162*κ ^ 2 + 112*κ + 24) / (2*κ) := by
  rw [le_div_iff₀ (by positivity : (0:ℝ) < 2*κ)]
  nlinarith [sq_nonneg (3*κ - 1), hκ]

theorem k3_threshold_attained :
    (81*(1/3 : ℝ) ^ 3 + 162*(1/3 : ℝ) ^ 2 + 112*(1/3 : ℝ) + 24) / (2*(1/3 : ℝ)) = 247/2 := by
  norm_num

end
end OUCorridor
