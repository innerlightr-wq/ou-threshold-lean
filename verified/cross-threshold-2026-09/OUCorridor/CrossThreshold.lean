import OUCorridor.MainTheorem
import OUCorridor.ResidualThreshold

/-!
# Reciprocal threshold structure and the cross-threshold covariance identity

With the reciprocal invariant `s(x) = x + 1/x`:

* **Residual threshold.** `r_D* = 2 + √3` satisfies `s(r_D*) = 4`
  (`residualThreshold_reciprocalInvariant`).
* **Volume threshold.** `r_A* = 3 + 2√2` (`threshold`) satisfies `s(r_A*) = 6`
  (`threshold_reciprocalInvariant`). This is derived from the existing `threshold_quartic`
  through the rational factorization `r⁴ - 34r² + 1 = (r² - 6r + 1)(r² + 6r + 1)`
  (`quartic_rational_factor`).
* **Merger.** At `r = r_A*` the volume bracket is `-8r²(κ - 1)²` (`bracket_threshold`): the two
  crossings of `A(κ) = A(0)` merge at `κ = 1` (`volume_threshold_eq_iff`).
* **Merger invariant.** For the Lyapunov solution `Σ = cov 1 r` of `OUCorridor/Covariance.lean`,
  `(tr Σ)² / det Σ = C(s(r))` with `C(s) = (64/3) s² / (s² + 12)` (`trace_sq_div_det_merger`).
  Here `tr` is the matrix trace and `det` the determinant, so `det Σ` is the generalized variance
  `A = volume`, not `√det Σ`.
* **Cross-threshold identity.** If `μ₁ > μ₂` are the eigenvalues of `Σ` at the volume-critical
  merger `(κ, r) = (1, r_A*)`, then `μ₁ / μ₂ = (r_D*)²` (`cross_threshold_eigenvalue_ratio`),
  i.e. `7 + 4√3`.

The proof of the last statement does not evaluate radicals on both sides. It passes through
`s(r_A*) = 6`, `C(6) = 16`, `q + 1/q = 16 - 2 = 14` for `q = μ₁/μ₂`,
`s(r_D*) = 4`, `s((r_D*)²) = 4² - 2 = 14`, and injectivity of `s` on `[1, ∞)`.
The numerical bridge between the two thresholds is `(64/3) · 6² / (6² + 12) = 16 = 4²`.

The identity is specific to the equal-relaxation normalization (`a₁ = a₂ = 1`).
-/

namespace OUCorridor

noncomputable section

open Real Matrix

/-!  Reciprocal invariant. -/

/-- The reciprocal invariant `s(x) = x + 1/x` (meaningful for `x ≠ 0`; invariant under
    `x ↦ 1/x`, the relabelling `X ↔ Y` of the two components when `x` is a noise ratio). -/
def reciprocalInvariant (x : ℝ) : ℝ :=
  x + 1 / x

theorem reciprocalInvariant_of_quadratic {x c : ℝ} (hx : x ≠ 0) (h : x ^ 2 - c * x + 1 = 0) :
    reciprocalInvariant x = c := by
  unfold reciprocalInvariant
  field_simp
  linear_combination h

/-- `s(x²) = s(x)² - 2`. -/
theorem reciprocalInvariant_sq {x : ℝ} (hx : x ≠ 0) :
    reciprocalInvariant (x^2) = reciprocalInvariant x ^ 2 - 2 := by
  unfold reciprocalInvariant
  field_simp
  ring

/-- `s` is injective on `[1, ∞)`: this excludes the reciprocal root `1/x` of `s(·) = s(x)`. -/
theorem reciprocalInvariant_injOn {x y : ℝ} (hx : 1 ≤ x) (hy : 1 ≤ y)
    (h : reciprocalInvariant x = reciprocalInvariant y) : x = y := by
  have hx0 : x ≠ 0 := by positivity
  have hy0 : y ≠ 0 := by positivity
  unfold reciprocalInvariant at h
  field_simp at h
  have hfac : (x - y) * (x*y - 1) = 0 := by linear_combination h
  rcases mul_eq_zero.mp hfac with h1 | h1
  · linarith
  · nlinarith

/-!  The two thresholds as values of the reciprocal invariant. -/

/-- The rational factorization of the volume-threshold quartic. -/
theorem quartic_rational_factor (r : ℝ) :
    r^4 - 34*r^2 + 1 = (r^2 - 6*r + 1) * (r^2 + 6*r + 1) := by
  ring

/-- `r_A*` is a root of `r² - 6r + 1`, derived from `threshold_quartic`: the second rational
    factor `r² + 6r + 1` is positive at `r_A* > 0`. -/
theorem threshold_quadratic : threshold^2 - 6*threshold + 1 = 0 := by
  have hq := threshold_quartic
  rw [quartic_rational_factor] at hq
  have hpos : 0 < threshold^2 + 6*threshold + 1 := by
    have := threshold_pos
    positivity
  rcases mul_eq_zero.mp hq with h | h
  · exact h
  · linarith

/-- `s(r_A*) = 6`. -/
theorem threshold_reciprocalInvariant : reciprocalInvariant threshold = 6 :=
  reciprocalInvariant_of_quadratic threshold_pos.ne' threshold_quadratic

/-- `s(r_D*) = 4`. -/
theorem residualThreshold_reciprocalInvariant : reciprocalInvariant residualThreshold = 4 :=
  reciprocalInvariant_of_quadratic residualThreshold_ne_zero residualThreshold_quadratic

/-- `s((r_D*)²) = 4² - 2 = 14`. -/
theorem residualThreshold_sq_reciprocalInvariant :
    reciprocalInvariant (residualThreshold^2) = 14 := by
  rw [reciprocalInvariant_sq residualThreshold_ne_zero, residualThreshold_reciprocalInvariant]
  norm_num

/-!  The volume-critical merger at `κ = 1`. -/

/-- At `r = r_A*` the bracket is a negative multiple of a perfect square with double root
    `κ = 1`. -/
theorem bracket_threshold (κ : ℝ) :
    bracket κ threshold = -8 * threshold^2 * (κ - 1)^2 := by
  unfold bracket
  linear_combination κ * threshold_quartic

/-- At `r = r_A*`, a positive coupling reaches the uncoupled volume exactly at `κ = 1`
    (the tangency of paper §8); everywhere else the volume stays below it. -/
theorem volume_threshold_eq_iff {κ : ℝ} (hκ : 0 < κ) :
    volume κ threshold = volume0 threshold ↔ κ = 1 := by
  have hden := denominator_pos hκ.le (κ := κ)
  have hdiff := volume_sub_volume0 κ threshold hκ.le
  rw [bracket_threshold] at hdiff
  have htp := threshold_pos
  constructor
  · intro h
    rw [h, sub_self, eq_comm, div_eq_zero_iff] at hdiff
    rcases hdiff with h1 | h1
    · have : (κ - 1)^2 = 0 := by
        rcases mul_eq_zero.mp h1 with h2 | h2
        · linarith
        · rcases mul_eq_zero.mp h2 with h3 | h3
          · nlinarith
          · exact h3
      nlinarith [pow_eq_zero_iff (n := 2) (a := κ - 1) two_ne_zero |>.mp this]
    · linarith
  · rintro rfl
    have : volume 1 threshold - volume0 threshold = 0 := by rw [hdiff]; ring
    linarith

theorem volume_threshold_le {κ : ℝ} (hκ : 0 ≤ κ) : volume κ threshold ≤ volume0 threshold := by
  have hden := denominator_pos hκ
  have hdiff := volume_sub_volume0 κ threshold hκ
  rw [bracket_threshold] at hdiff
  have : κ * (-8 * threshold^2 * (κ - 1)^2) / (16*(κ+1)^2*(2*κ+1)) ≤ 0 :=
    div_nonpos_of_nonpos_of_nonneg (by nlinarith [sq_nonneg (threshold * (κ - 1))]) hden.le
  linarith

/-!  The merger invariant `(tr Σ)² / det Σ`. -/

/-- Closed form of `(tr Σ)² / det Σ` at `κ = 1` as a function of `s = r + 1/r`. -/
def mergerInvariant (s : ℝ) : ℝ :=
  64/3 * s^2 / (s^2 + 12)

/-- The numerical bridge: `(64/3) · 6² / (6² + 12) = 16 = 4²`. -/
theorem mergerInvariant_six : mergerInvariant 6 = 16 := by
  norm_num [mergerInvariant]

theorem cov_one_trace (r : ℝ) : (cov 1 r).trace = (1 + r^2) / 3 := by
  rw [cov_trace, covXX, covYY]
  ring

theorem cov_one_det (r : ℝ) : (cov 1 r).det = (r^4 + 14*r^2 + 1) / 192 := by
  rw [det_cov zero_le_one, volume]
  ring

theorem cov_one_det_pos (r : ℝ) : 0 < (cov 1 r).det := by
  rw [cov_one_det]
  positivity

/-- `(tr Σ)² / det Σ = C(r + 1/r)` at the merger coupling `κ = 1`, for every `r > 0`. -/
theorem trace_sq_div_det_merger {r : ℝ} (hr : 0 < r) :
    (cov 1 r).trace^2 / (cov 1 r).det = mergerInvariant (reciprocalInvariant r) := by
  have h1 : r^4 + 14*r^2 + 1 ≠ 0 := by positivity
  have h2 : (r + 1/r)^2 + 12 ≠ 0 := by positivity
  rw [cov_one_trace, cov_one_det, mergerInvariant, reciprocalInvariant]
  field_simp
  ring

/-!  Eigenvalues of a `2 × 2` matrix. -/

/-- The characteristic polynomial of a `2 × 2` matrix. -/
theorem det_sub_smul_one (A : Matrix (Fin 2) (Fin 2) ℝ) (μ : ℝ) :
    (A - μ • 1).det = μ^2 - A.trace * μ + A.det := by
  rw [Matrix.det_fin_two, Matrix.det_fin_two, Matrix.trace_fin_two]
  simp
  ring

/-- Two distinct eigenvalues have sum `tr A` and product `det A`. -/
theorem eigenvalues_sum_prod {A : Matrix (Fin 2) (Fin 2) ℝ} {μ₁ μ₂ : ℝ}
    (h₁ : (A - μ₁ • 1).det = 0) (h₂ : (A - μ₂ • 1).det = 0) (hne : μ₁ ≠ μ₂) :
    μ₁ + μ₂ = A.trace ∧ μ₁ * μ₂ = A.det := by
  rw [det_sub_smul_one] at h₁ h₂
  have hsum : μ₁ + μ₂ = A.trace := by
    have : (μ₁ - μ₂) * (μ₁ + μ₂ - A.trace) = 0 := by linear_combination h₁ - h₂
    rcases mul_eq_zero.mp this with h | h
    · exact absurd (sub_eq_zero.mp h) hne
    · linarith
  refine ⟨hsum, ?_⟩
  linear_combination -h₁ + μ₁ * hsum

/-- For positive `μ₁, μ₂`: `(μ₁ + μ₂)² / (μ₁ μ₂) = s(μ₁/μ₂) + 2`. -/
theorem sum_sq_div_prod {μ₁ μ₂ : ℝ} (h₁ : μ₁ ≠ 0) (h₂ : μ₂ ≠ 0) :
    (μ₁ + μ₂)^2 / (μ₁ * μ₂) = reciprocalInvariant (μ₁ / μ₂) + 2 := by
  unfold reciprocalInvariant
  field_simp
  ring

/-!  The cross-threshold identity. -/

/-- The uniqueness step: the root `q > 1` of `q + 1/q = 14` is `(r_D*)²`. -/
theorem cross_threshold_ratio_unique {q : ℝ} (hq : 1 < q) (hrecip : q + 1 / q = 14) :
    q = residualThreshold^2 := by
  have hD : 1 ≤ residualThreshold^2 := by nlinarith [residualThreshold_gt_one]
  exact reciprocalInvariant_injOn hq.le hD
    (hrecip.trans residualThreshold_sq_reciprocalInvariant.symm)

/-- Algebraic form: if `q > 1` satisfies `s(q) + 2 = C(s(r_A*))`, then `q = (r_D*)²`. -/
theorem cross_threshold_spectral_ratio {q : ℝ} (hq : 1 < q)
    (hcrit : reciprocalInvariant q + 2 = mergerInvariant (reciprocalInvariant threshold)) :
    q = residualThreshold^2 := by
  -- `s_A = 6` and `C(6) = 16`
  rw [threshold_reciprocalInvariant, mergerInvariant_six] at hcrit
  -- `q + 1/q = 14`; then uniqueness on `q > 1` against `s((r_D*)²) = 4² - 2 = 14`
  exact cross_threshold_ratio_unique hq (by unfold reciprocalInvariant at hcrit; linarith)

/-- **Cross-threshold identity.** Let `μ₁ > μ₂` be eigenvalues of the equal-relaxation stationary
    covariance `Σ` (the Lyapunov solution `cov`) at the volume-critical merger `κ = 1`,
    `r = r_A* = 3 + 2√2`. Then `μ₁ / μ₂ = (r_D*)²`, with `r_D* = 2 + √3` the residual threshold. -/
theorem cross_threshold_eigenvalue_ratio {μ₁ μ₂ : ℝ}
    (h₁ : (cov 1 threshold - μ₁ • 1).det = 0)
    (h₂ : (cov 1 threshold - μ₂ • 1).det = 0)
    (hlt : μ₂ < μ₁) :
    μ₁ / μ₂ = residualThreshold^2 := by
  obtain ⟨hsum, hprod⟩ := eigenvalues_sum_prod h₁ h₂ hlt.ne'
  have hdet := cov_one_det_pos threshold
  have htr : 0 < (cov 1 threshold).trace := by
    rw [cov_one_trace]
    positivity
  have hμ₂ : 0 < μ₂ := by nlinarith
  have hμ₁ : 0 < μ₁ := by linarith
  -- `(tr Σ)² / det Σ = s(q) + 2` for `q = μ₁ / μ₂ > 1`
  have hq1 : 1 < μ₁ / μ₂ := (one_lt_div hμ₂).mpr hlt
  have hratio := sum_sq_div_prod hμ₁.ne' hμ₂.ne'
  rw [hsum, hprod, trace_sq_div_det_merger threshold_pos] at hratio
  exact cross_threshold_spectral_ratio hq1 hratio.symm

theorem cross_threshold_eigenvalue_ratio_radical {μ₁ μ₂ : ℝ}
    (h₁ : (cov 1 threshold - μ₁ • 1).det = 0)
    (h₂ : (cov 1 threshold - μ₂ • 1).det = 0)
    (hlt : μ₂ < μ₁) :
    μ₁ / μ₂ = 7 + 4 * Real.sqrt 3 := by
  rw [cross_threshold_eigenvalue_ratio h₁ h₂ hlt, residualThreshold_sq]

/-- Non-vacuity: `Σ` at the merger has two distinct real eigenvalues. -/
theorem cov_merger_eigenvalues_exist :
    ∃ μ₁ μ₂ : ℝ, (cov 1 threshold - μ₁ • 1).det = 0 ∧ (cov 1 threshold - μ₂ • 1).det = 0 ∧
      μ₂ < μ₁ := by
  set T := (cov 1 threshold).trace
  set D := (cov 1 threshold).det
  have hD : 0 < D := cov_one_det_pos threshold
  have hTD : T^2 = 16 * D := by
    have h := trace_sq_div_det_merger threshold_pos
    rw [threshold_reciprocalInvariant, mergerInvariant_six, div_eq_iff hD.ne'] at h
    exact h
  have hdisc : 0 < T^2 - 4*D := by linarith
  have hs := Real.sq_sqrt hdisc.le
  have hspos := Real.sqrt_pos.mpr hdisc
  refine ⟨(T + Real.sqrt (T^2 - 4*D)) / 2, (T - Real.sqrt (T^2 - 4*D)) / 2, ?_, ?_, ?_⟩
  · rw [det_sub_smul_one]
    linear_combination (1/4 : ℝ) * hs
  · rw [det_sub_smul_one]
    linear_combination (1/4 : ℝ) * hs
  · linarith

/-- Rapidity form: `½ log(μ₁/μ₂) = log r_D* = arcosh 2`. -/
theorem cross_threshold_rapidity {μ₁ μ₂ : ℝ}
    (h₁ : (cov 1 threshold - μ₁ • 1).det = 0)
    (h₂ : (cov 1 threshold - μ₂ • 1).det = 0)
    (hlt : μ₂ < μ₁) :
    Real.log (μ₁ / μ₂) / 2 = Real.log residualThreshold ∧
      Real.log residualThreshold = Real.arcosh 2 := by
  refine ⟨?_, ?_⟩
  · rw [cross_threshold_eigenvalue_ratio h₁ h₂ hlt, Real.log_pow]
    push_cast
    ring
  · have hcosh : Real.cosh (Real.log residualThreshold) = 2 := by
      rw [Real.cosh_log residualThreshold_pos, ← one_div]
      have := residualThreshold_reciprocalInvariant
      unfold reciprocalInvariant at this
      linarith
    rw [← hcosh, Real.arcosh_cosh (Real.log_nonneg residualThreshold_gt_one.le)]

end
end OUCorridor
