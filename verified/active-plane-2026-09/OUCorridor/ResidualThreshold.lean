import OUCorridor.Covariance

/-!
# The residual-variance threshold `r_D* = 2 + √3`

Paper §9, Proposition 5, in the equal-relaxation normalization. The conditional residual variance

  `D(κ) = Var(X | Y) = Σxx - Σxy² / Σyy`   (paper eq. (14), Schur complement of `Σyy`)

is defined here from the entries of the Lyapunov solution `cov κ r` of `OUCorridor/Covariance.lean`,
not taken as an independent closed form. The development mirrors the volume threshold:

* `residualVariance_sub_uncoupled`:
  `D(κ) - D(0) = κ B_D(κ, r) / (4(κ+1)(κ²r² + κ² + 4κr² + 2r²))` (paper eq. (27)),
  with `B_D` the quadratic of paper eq. (28);
* `residualDiscr_factor`: its discriminant is `(r²-1)²(r²-4r+1)(r²+4r+1)` (paper eq. (29));
* `exists_residual_improvement_iff_threshold`: for `r ≥ 1`,
  `(∃ κ > 0, D(κ) > D(0)) ↔ r > 2 + √3`.

As for the volume threshold, the stochastic step (the stationary covariance of the SDE solves the
Lyapunov equation) is not formalized.
-/

namespace OUCorridor

noncomputable section

open Real

/-- Conditional residual variance `D(κ) = Var(X | Y)` (paper eq. (14)). -/
def residualVariance (κ r : ℝ) : ℝ :=
  covXX κ r - covXY κ r ^ 2 / covYY κ r

/-- The residual-variance threshold `r_D* = 2 + √3`. -/
def residualThreshold : ℝ :=
  2 + Real.sqrt 3

/-- Sign-controlling quadratic `B_D(κ, r)` (paper eq. (28)). -/
def residualBracket (κ r : ℝ) : ℝ :=
  -2*(r^2 + 1)*κ^2 + (r^4 - 8*r^2 - 1)*κ - 4*r^2

/-- Discriminant of `B_D(·, r)`. -/
def residualDiscr (r : ℝ) : ℝ :=
  (r^4 - 8*r^2 - 1)^2 - 32*r^2*(r^2 + 1)

/-!  Relation to the covariance matrix. -/

/-- `D = det Σ / Σyy`, the second form in paper eq. (14). -/
theorem residualVariance_eq_det_div {κ r : ℝ} (hκ : 0 ≤ κ) (hr : 0 < r) :
    residualVariance κ r = (cov κ r).det / covYY κ r := by
  have h := (covYY_pos hκ hr).ne'
  rw [cov_det, residualVariance]
  field_simp

theorem residualVariance_zero {r : ℝ} (hr : 0 < r) : residualVariance 0 r = 1 / 2 := by
  have : r^2 ≠ 0 := by positivity
  unfold residualVariance covXX covYY covXY
  field_simp
  ring

theorem residualDenominator_pos {κ r : ℝ} (hκ : 0 ≤ κ) (hr : 0 < r) :
    0 < 4*(κ + 1)*(κ^2*r^2 + κ^2 + 4*κ*r^2 + 2*r^2) := by
  have : 0 < 2*r^2 := by positivity
  have : 0 ≤ κ^2*r^2 + κ^2 + 4*κ*r^2 := by positivity
  have : 0 < κ^2*r^2 + κ^2 + 4*κ*r^2 + 2*r^2 := by linarith
  positivity

/-- Paper eq. (27). -/
theorem residualVariance_sub_uncoupled {κ r : ℝ} (hκ : 0 ≤ κ) (hr : 0 < r) :
    residualVariance κ r - residualVariance 0 r =
      κ * residualBracket κ r / (4*(κ + 1)*(κ^2*r^2 + κ^2 + 4*κ*r^2 + 2*r^2)) := by
  have hY := (covYY_pos hκ hr).ne'
  have h1 : (2*κ + 1 : ℝ) ≠ 0 := by positivity
  have h2 : (2*κ^2 + 3*κ + 1 : ℝ) ≠ 0 := by positivity
  have h3 := (residualDenominator_pos hκ hr).ne'
  have h4 : κ^2*r^2 + κ^2 + 4*κ*r^2 + 2*r^2 ≠ 0 := by
    intro h; apply h3; rw [h, mul_zero]
  rw [residualVariance_zero hr]
  unfold residualVariance covXX covYY covXY residualBracket at *
  field_simp
  ring

theorem residualVariance_gt_iff_bracket_pos {κ r : ℝ} (hκ : 0 < κ) (hr : 0 < r) :
    residualVariance κ r > residualVariance 0 r ↔ residualBracket κ r > 0 := by
  have hden := residualDenominator_pos hκ.le hr
  rw [gt_iff_lt, ← sub_pos, residualVariance_sub_uncoupled hκ.le hr,
    div_pos_iff_of_pos_right hden, mul_pos_iff_of_pos_left hκ]

/-!  Discriminant. -/

/-- Paper eq. (29). -/
theorem residualDiscr_factor (r : ℝ) :
    residualDiscr r = (r^2 - 1)^2 * (r^2 - 4*r + 1) * (r^2 + 4*r + 1) := by
  unfold residualDiscr
  ring

/-- Completed-square certificate (holds for all `κ, r`). -/
theorem residualDiscr_sos (κ r : ℝ) :
    residualDiscr r =
      ((r^4 - 8*r^2 - 1) - 4*(r^2 + 1)*κ)^2 + 8*(r^2 + 1) * residualBracket κ r := by
  unfold residualDiscr residualBracket
  ring

/-!  Radical identities for `r_D* = 2 + √3`. -/

theorem sqrt_three_pos : 0 < Real.sqrt 3 :=
  Real.sqrt_pos.mpr (by norm_num)

theorem sqrt_three_sq : (Real.sqrt 3)^2 = 3 :=
  Real.sq_sqrt (by norm_num)

theorem sqrt_three_gt_one : 1 < Real.sqrt 3 := by
  nlinarith [sqrt_three_sq, sqrt_three_pos]

theorem residualThreshold_gt_one : 1 < residualThreshold := by
  unfold residualThreshold
  linarith [sqrt_three_pos]

theorem residualThreshold_pos : 0 < residualThreshold :=
  lt_trans one_pos residualThreshold_gt_one

theorem residualThreshold_ne_zero : residualThreshold ≠ 0 :=
  residualThreshold_pos.ne'

/-- `r_D*` is the root `> 1` of `r² - 4r + 1`; the other root is `2 - √3 = 1 / r_D*`. -/
theorem residualThreshold_quadratic :
    residualThreshold^2 - 4*residualThreshold + 1 = 0 := by
  unfold residualThreshold
  linear_combination sqrt_three_sq

theorem residualThreshold_sq : residualThreshold^2 = 7 + 4 * Real.sqrt 3 := by
  unfold residualThreshold
  linear_combination sqrt_three_sq

/-- Factorization of the residual quadratic over its two real roots `2 ± √3`. -/
theorem residualQuadratic_factor (r : ℝ) :
    r^2 - 4*r + 1 = (r - residualThreshold) * (r - (2 - Real.sqrt 3)) := by
  unfold residualThreshold
  linear_combination sqrt_three_sq

/-- For `r ≥ 1`, `r² - 4r + 1 > 0 ↔ r > 2 + √3`. -/
theorem residualQuadratic_pos_iff {r : ℝ} (hr : 1 ≤ r) :
    r^2 - 4*r + 1 > 0 ↔ r > residualThreshold := by
  have hconj : 0 < r - (2 - Real.sqrt 3) := by linarith [sqrt_three_gt_one]
  rw [residualQuadratic_factor, gt_iff_lt, mul_pos_iff_of_pos_right hconj, sub_pos]

/-!  The residual-variance threshold theorem (paper Proposition 5). -/

/-- Existence of a positive coupling with `B_D > 0` forces `r > 2 + √3`. -/
theorem gt_residualThreshold_of_bracket_pos {r : ℝ} (hr : 1 ≤ r) {κ : ℝ}
    (hb : residualBracket κ r > 0) : r > residualThreshold := by
  have hdisc : 0 < residualDiscr r := by
    rw [residualDiscr_sos κ]
    have : 0 < 8*(r^2 + 1) * residualBracket κ r := by positivity
    nlinarith [sq_nonneg ((r^4 - 8*r^2 - 1) - 4*(r^2 + 1)*κ)]
  rw [residualDiscr_factor] at hdisc
  have hplus : 0 < r^2 + 4*r + 1 := by nlinarith
  have hsq : 0 ≤ (r^2 - 1)^2 := sq_nonneg _
  refine (residualQuadratic_pos_iff hr).mp ?_
  by_contra hcon
  have hcon : r^2 - 4*r + 1 ≤ 0 := not_lt.mp hcon
  have : (r^2 - 1)^2 * (r^2 - 4*r + 1) ≤ 0 := mul_nonpos_of_nonneg_of_nonpos hsq hcon
  nlinarith [mul_nonpos_of_nonpos_of_nonneg this hplus.le]

/-- Above the threshold the vertex `κ₀ = (r⁴ - 8r² - 1) / (4(r² + 1))` is a positive coupling
    with `B_D(κ₀) = Δ_D / (8(r² + 1)) > 0`. -/
theorem exists_bracket_pos_of_gt_residualThreshold {r : ℝ} (hr : r > residualThreshold) :
    ∃ κ : ℝ, 0 < κ ∧ residualBracket κ r > 0 := by
  have h3 : (3 : ℝ) < r := by
    unfold residualThreshold at hr
    linarith [sqrt_three_gt_one]
  have hr1 : 1 ≤ r := by linarith
  have hq : r^2 - 4*r + 1 > 0 := (residualQuadratic_pos_iff hr1).mpr hr
  have hw : 0 < r^2 + 1 := by positivity
  have hdisc : 0 < residualDiscr r := by
    rw [residualDiscr_factor]
    have : 0 < (r^2 - 1)^2 := by
      have : 0 < r^2 - 1 := by nlinarith
      positivity
    have : 0 < r^2 + 4*r + 1 := by nlinarith
    positivity
  have hnum : 0 < r^4 - 8*r^2 - 1 := by nlinarith
  refine ⟨(r^4 - 8*r^2 - 1) / (4*(r^2 + 1)), by positivity, ?_⟩
  have hval : residualBracket ((r^4 - 8*r^2 - 1) / (4*(r^2 + 1))) r =
      residualDiscr r / (8*(r^2 + 1)) := by
    unfold residualBracket residualDiscr
    field_simp
    ring
  rw [hval]
  positivity

theorem exists_residualBracket_pos_iff_threshold {r : ℝ} (hr : 1 ≤ r) :
    (∃ κ : ℝ, 0 < κ ∧ residualBracket κ r > 0) ↔ r > residualThreshold := by
  constructor
  · rintro ⟨κ, _, hb⟩
    exact gt_residualThreshold_of_bracket_pos hr hb
  · exact exists_bracket_pos_of_gt_residualThreshold

/-- **Residual-variance threshold** (paper Proposition 5). For `r ≥ 1`, some positive coupling
    strictly increases the conditional residual variance `Var(X | Y)` over its uncoupled value
    `1/2` if and only if `r > 2 + √3`. -/
theorem exists_residual_improvement_iff_threshold {r : ℝ} (hr : 1 ≤ r) :
    (∃ κ : ℝ, 0 < κ ∧ residualVariance κ r > residualVariance 0 r) ↔ r > residualThreshold := by
  have hr0 : 0 < r := by linarith
  rw [← exists_residualBracket_pos_iff_threshold hr]
  refine exists_congr fun κ => and_congr_right fun hκ => ?_
  exact residualVariance_gt_iff_bracket_pos hκ hr0

end
end OUCorridor
