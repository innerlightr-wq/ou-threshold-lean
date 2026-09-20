import OUCorridor.CrossThreshold

/-!
# Scale-free spectral shape: closure at `n = 2`, non-identifiability for `n ≥ 3`

`J₂ Σ = (tr Σ)²/det Σ` determines the eigenvalue ratio of a `2 × 2` SPD matrix, which is the
algebraic reason the cross-threshold argument of `OUCorridor/CrossThreshold.lean` closes with a
single scalar.  For `n ≥ 3` no single scale-free invariant can do this.

Both statements are **standard mathematics**: `J_n` is, up to a constant, the reciprocal of
Mauchly's (1940) sphericity statistic, and the `n ≥ 3` failure is the elementary fact that a
spectrum needs all `n` elementary symmetric functions (Newton), of which trace and determinant
are all only when `n = 2`.  They are recorded here because the repository uses the `n = 2` case.
-/

namespace OUCorridor

noncomputable section

/-- The scale-free trace/determinant invariant of a `2 × 2` spectrum. -/
def J2 (μ₁ μ₂ : ℝ) : ℝ := (μ₁ + μ₂)^2 / (μ₁ * μ₂)

/-- `J₂ = q + 1/q + 2` for `q = μ₁/μ₂`. -/
theorem J2_eq_reciprocalInvariant {μ₁ μ₂ : ℝ} (h₁ : 0 < μ₁) (h₂ : 0 < μ₂) :
    J2 μ₁ μ₂ = reciprocalInvariant (μ₁ / μ₂) + 2 := by
  rw [J2, reciprocalInvariant]
  field_simp
  ring

/-- **Spectral closure at `n = 2`.**  On the branch `q ≥ 1` the invariant determines the ratio. -/
theorem eigen_ratio_unique_of_J2 {μ₁ μ₂ ν₁ ν₂ : ℝ} (hμ₁ : 0 < μ₁) (hμ₂ : 0 < μ₂)
    (hν₁ : 0 < ν₁) (hν₂ : 0 < ν₂) (hμ : 1 ≤ μ₁ / μ₂) (hν : 1 ≤ ν₁ / ν₂)
    (h : J2 μ₁ μ₂ = J2 ν₁ ν₂) : μ₁ / μ₂ = ν₁ / ν₂ := by
  rw [J2_eq_reciprocalInvariant hμ₁ hμ₂, J2_eq_reciprocalInvariant hν₁ hν₂] at h
  exact reciprocalInvariant_injOn hμ hν (by linarith)

/-- **Non-identifiability for `n = 3`.**  Two positive triples with the same trace and the same
    determinant — hence the same value of every scale-free trace/determinant invariant — but
    different extreme eigenvalue ratios. -/
theorem exists_same_trace_det_different_ratio :
    ∃ μ₁ μ₂ μ₃ ν₁ ν₂ ν₃ : ℝ,
      0 < μ₁ ∧ 0 < μ₂ ∧ 0 < μ₃ ∧ 0 < ν₁ ∧ 0 < ν₂ ∧ 0 < ν₃ ∧
      μ₁ + μ₂ + μ₃ = ν₁ + ν₂ + ν₃ ∧
      μ₁ * μ₂ * μ₃ = ν₁ * ν₂ * ν₃ ∧
      μ₃ / μ₁ ≠ ν₃ / ν₁ := by
  refine ⟨1, 8, 12, 2, 3, 16, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;> norm_num

end
end OUCorridor
