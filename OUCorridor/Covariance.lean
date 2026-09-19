import OUCorridor.Threshold

/-!
# The equal-relaxation stationary covariance as a Lyapunov solution

Equal-relaxation normalization of the paper: `a₁ = a₂ = 1`, `σ₁ = 1`, `σ₂ = r`, coupling `κ ≥ 0`.

* `drift κ` is the drift matrix `M` (paper eq. (7)) and `noiseCov r` is `Q = diag(1, r²)`.
* `cov κ r` is the explicit matrix `Σ` with the entries of paper eqs. (36)–(38).
* `cov_lyapunov` proves `M Σ + Σ Mᵀ = -Q` (paper eq. (8)), and `lyapunov_unique` proves that `Σ` is
  the only matrix solving it, for every `κ ≥ 0`.
* `det_cov` proves `det Σ = volume κ r`, so the closed form `volume` taken as a definition in
  `OUCorridor/Threshold.lean` is the determinant of this Lyapunov solution.

**Scope.** Everything here is exact real algebra on `2 × 2` matrices. The step "the stationary
covariance of the OU process solves the continuous Lyapunov equation" (paper Proposition 1:
SDE semantics, existence and uniqueness of the stationary Gaussian law) is *not* formalized.
-/

namespace OUCorridor

noncomputable section

open Matrix

/-- Drift matrix `M` of the equal-relaxation coupled OU system (paper eq. (7), `a₁ = a₂ = 1`). -/
def drift (κ : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![-(1 + κ), κ; κ, -(1 + κ)]

/-- Noise covariance `Q = B Bᵀ = diag(σ₁², σ₂²)` with `σ₁ = 1`, `σ₂ = r`. -/
def noiseCov (r : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![1, 0; 0, r^2]

/-- `Σxx` (paper eq. (36)). -/
def covXX (κ r : ℝ) : ℝ :=
  (κ^2*r^2 + κ^2 + 4*κ + 2) / (4*(2*κ^2 + 3*κ + 1))

/-- `Σyy` (paper eq. (37)). -/
def covYY (κ r : ℝ) : ℝ :=
  (κ^2*r^2 + κ^2 + 4*κ*r^2 + 2*r^2) / (4*(2*κ^2 + 3*κ + 1))

/-- `Σxy` (paper eq. (38)). -/
def covXY (κ r : ℝ) : ℝ :=
  κ*(r^2 + 1) / (4*(2*κ + 1))

/-- The explicit equal-relaxation stationary covariance matrix `Σ(κ, r)`. -/
def cov (κ r : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![covXX κ r, covXY κ r; covXY κ r, covYY κ r]

theorem drift_transpose (κ : ℝ) : (drift κ)ᵀ = drift κ := by
  ext i j
  fin_cases i <;> fin_cases j <;> rfl

/-- The four scalar equations of `M S + S Mᵀ = -Q` for an arbitrary `2 × 2` matrix `S`. -/
theorem lyapunov_iff (κ r : ℝ) (S : Matrix (Fin 2) (Fin 2) ℝ) :
    drift κ * S + S * (drift κ)ᵀ = -noiseCov r ↔
      (-2*(1 + κ)*S 0 0 + κ*(S 0 1 + S 1 0) = -1 ∧
       -2*(1 + κ)*S 0 1 + κ*(S 0 0 + S 1 1) = 0 ∧
       -2*(1 + κ)*S 1 0 + κ*(S 0 0 + S 1 1) = 0 ∧
       -2*(1 + κ)*S 1 1 + κ*(S 0 1 + S 1 0) = -r^2) := by
  rw [drift_transpose, ← Matrix.ext_iff]
  constructor
  · intro h
    refine ⟨?_, ?_, ?_, ?_⟩
    · have := h 0 0
      simp [drift, noiseCov, Matrix.mul_apply, Matrix.vecMul, dotProduct, Fin.sum_univ_two] at this
      linarith
    · have := h 0 1
      simp [drift, noiseCov, Matrix.mul_apply, Matrix.vecMul, dotProduct, Fin.sum_univ_two] at this
      linarith
    · have := h 1 0
      simp [drift, noiseCov, Matrix.mul_apply, Matrix.vecMul, dotProduct, Fin.sum_univ_two] at this
      linarith
    · have := h 1 1
      simp [drift, noiseCov, Matrix.mul_apply, Matrix.vecMul, dotProduct, Fin.sum_univ_two] at this
      linarith
  · rintro ⟨h00, h01, h10, h11⟩ i j
    fin_cases i <;> fin_cases j <;>
      simp [drift, noiseCov, Matrix.mul_apply, Matrix.vecMul, dotProduct, Fin.sum_univ_two] <;>
      linarith

/-- `Σ(κ, r)` solves the stationary Lyapunov equation `M Σ + Σ Mᵀ = -Q` (paper eq. (8)). -/
theorem cov_lyapunov {κ : ℝ} (hκ : 0 ≤ κ) (r : ℝ) :
    drift κ * cov κ r + cov κ r * (drift κ)ᵀ = -noiseCov r := by
  have h1 : (2*κ + 1 : ℝ) ≠ 0 := by positivity
  have h2 : (2*κ^2 + 3*κ + 1 : ℝ) ≠ 0 := by positivity
  rw [lyapunov_iff]
  simp only [cov, covXX, covYY, covXY, Matrix.of_apply, Matrix.cons_val', Matrix.cons_val_zero,
    Matrix.cons_val_one, Matrix.empty_val', Matrix.cons_val_fin_one]
  refine ⟨?_, ?_, ?_, ?_⟩ <;> field_simp <;> ring

/-- Uniqueness: for `κ ≥ 0` every solution `S` of `M S + S Mᵀ = -Q` equals `Σ(κ, r)`. -/
theorem lyapunov_unique {κ : ℝ} (hκ : 0 ≤ κ) (r : ℝ) {S : Matrix (Fin 2) (Fin 2) ℝ}
    (hS : drift κ * S + S * (drift κ)ᵀ = -noiseCov r) : S = cov κ r := by
  obtain ⟨e00, e01, e10, e11⟩ := (lyapunov_iff κ r S).mp hS
  obtain ⟨f00, f01, f10, f11⟩ := (lyapunov_iff κ r (cov κ r)).mp (cov_lyapunov hκ r)
  -- the difference `T = S - Σ` solves the homogeneous equation; show `T = 0`
  set p := S 0 0 - cov κ r 0 0
  set q := S 0 1 - cov κ r 0 1
  set u := S 1 0 - cov κ r 1 0
  set v := S 1 1 - cov κ r 1 1
  have ha : (0 : ℝ) < 1 + κ := by linarith
  have hqu : q = u := by
    have : 2*(1 + κ)*(q - u) = 0 := by simp only [q, u]; linarith
    rcases mul_eq_zero.mp this with h | h
    · linarith
    · linarith
  have hpv : p = v := by
    have : 2*(1 + κ)*(p - v) = 0 := by simp only [p, v, q, u] at hqu ⊢; linarith
    rcases mul_eq_zero.mp this with h | h
    · linarith
    · linarith
  -- `(1+κ) q = κ p` and `(1+κ) p = κ q`, hence `(1 + 2κ) q = 0`
  have hq1 : (1 + κ)*q = κ*p := by simp only [p, q, v] at hpv ⊢; linarith
  have hp1 : (1 + κ)*p = κ*q := by simp only [p, q, u] at hqu ⊢; linarith
  have hq0 : q = 0 := by
    have : (1 + 2*κ)*q = 0 := by nlinarith
    rcases mul_eq_zero.mp this with h | h
    · linarith
    · exact h
  have hp0 : p = 0 := by
    have : (1 + κ)*p = 0 := by rw [hp1, hq0, mul_zero]
    rcases mul_eq_zero.mp this with h | h
    · linarith
    · exact h
  ext i j
  fin_cases i <;> fin_cases j
  · simp only [p] at hp0; simp; linarith
  · simp only [q] at hq0; simp; linarith
  · simp only [u] at hqu; simp; linarith
  · simp only [v] at hpv; simp; linarith

theorem cov_det (κ r : ℝ) : (cov κ r).det = covXX κ r * covYY κ r - covXY κ r ^ 2 := by
  rw [cov, Matrix.det_fin_two_of]
  ring

theorem cov_trace (κ r : ℝ) : (cov κ r).trace = covXX κ r + covYY κ r := by
  rw [cov, Matrix.trace_fin_two_of]

/-- The closed-form `volume` of `OUCorridor/Threshold.lean` is `det Σ` of the Lyapunov solution. -/
theorem det_cov {κ : ℝ} (hκ : 0 ≤ κ) (r : ℝ) : (cov κ r).det = volume κ r := by
  have h1 : (κ + 1 : ℝ) ≠ 0 := by positivity
  have h2 : (2*κ + 1 : ℝ) ≠ 0 := by positivity
  have h3 : (2*κ^2 + 3*κ + 1 : ℝ) ≠ 0 := by positivity
  rw [cov_det, covXX, covYY, covXY, volume]
  field_simp
  ring

theorem covYY_pos {κ r : ℝ} (hκ : 0 ≤ κ) (hr : 0 < r) : 0 < covYY κ r := by
  unfold covYY
  have : 0 < 2*r^2 := by positivity
  have : 0 ≤ κ^2*r^2 + κ^2 + 4*κ*r^2 := by positivity
  apply div_pos
  · linarith
  · positivity

end
end OUCorridor
