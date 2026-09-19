import OUCorridor.Threshold

namespace OUCorridor

noncomputable section

open Real

/-!  =====================  STAGE 5  ===================== -/

/-- Sum-of-squares certificate linking the bracket's discriminant to the
    bracket itself at an arbitrary κ. Pure polynomial identity, holds for
    all κ, r with no side conditions. -/
theorem discr_sos (κ r : ℝ) :
    discr r = (-16*r^2*κ + (r^4 - 18*r^2 + 1))^2 + 32*r^2 * bracket κ r := by
  unfold discr bracket
  ring

/-- The mathematically substantive direction: existence of some κ > 0 with
    bracket κ r > 0 forces the discriminant-quartic r^4 - 34r^2 + 1 to be
    strictly positive. -/
theorem quartic_pos_of_exists_bracket_pos {r : ℝ} (hr : 1 ≤ r)
    {κ : ℝ} (hb : bracket κ r > 0) :
    r^4 - 34*r^2 + 1 > 0 := by
  have hrpos : 0 < r := by linarith
  have hr2pos : 0 < r^2 := pow_pos hrpos 2
  have hsq : (0:ℝ) ≤ (-16*r^2*κ + (r^4 - 18*r^2 + 1))^2 := sq_nonneg _
  have hterm : 0 < 32*r^2 * bracket κ r := by positivity
  have hidentity : discr r
      = (-16*r^2*κ + (r^4 - 18*r^2 + 1))^2 + 32*r^2 * bracket κ r :=
    discr_sos κ r
  have hdiscr_pos : 0 < discr r := by linarith
  have hfact : discr r = (r^2 - 1)^2 * (r^4 - 34*r^2 + 1) := discr_factor r
  rw [hfact] at hdiscr_pos
  by_contra hcon
  push_neg at hcon
  have hsq2 : (0:ℝ) ≤ (r^2 - 1)^2 := sq_nonneg _
  have hle : (r^2 - 1)^2 * (r^4 - 34*r^2 + 1) ≤ (r^2 - 1)^2 * 0 :=
    mul_le_mul_of_nonneg_left hcon hsq2
  rw [mul_zero] at hle
  linarith

/-- STAGE 5 MAIN RESULT. -/
theorem exists_bracket_pos_iff_threshold {r : ℝ} (hr : 1 ≤ r) :
    (∃ κ : ℝ, 0 < κ ∧ bracket κ r > 0) ↔ r > threshold := by
  constructor
  · rintro ⟨κ, _hκ, hb⟩
    have hquartic : r^4 - 34*r^2 + 1 > 0 := quartic_pos_of_exists_bracket_pos hr hb
    exact (quartic_gt_iff_gt_threshold hr).mp hquartic
  · intro hgt
    have hquartic : r^4 - 34*r^2 + 1 > 0 := (quartic_gt_iff_gt_threshold hr).mpr hgt
    refine ⟨1, one_pos, ?_⟩
    rw [bracket_one]
    exact hquartic

/-!  =====================  STAGE 6  ===================== -/

/-- CENTRAL THEOREM. For r ≥ 1, some positive coupling strictly improves
    the stationary covariance volume over its uncoupled value if and only
    if the noise-heterogeneity ratio exceeds the exact threshold 3+2√2. -/
theorem exists_volume_improvement_iff_threshold {r : ℝ} (hr : 1 ≤ r) :
    (∃ κ : ℝ, 0 < κ ∧ volume κ r > volume0 r) ↔ r > threshold := by
  constructor
  · rintro ⟨κ, hκ, hv⟩
    have hb : bracket κ r > 0 := (volume_gt_iff_bracket_gt hκ).mp hv
    exact (exists_bracket_pos_iff_threshold hr).mp ⟨κ, hκ, hb⟩
  · intro hgt
    obtain ⟨κ, hκ, hb⟩ := (exists_bracket_pos_iff_threshold hr).mpr hgt
    exact ⟨κ, hκ, (volume_gt_iff_bracket_gt hκ).mpr hb⟩

end
end OUCorridor
