import Mathlib

namespace OUCorridor

noncomputable section

open Real

def volume (κ r : ℝ) : ℝ :=
  (κ^2 * r^4 + 2*κ^2*r^2 + κ^2 + 8*κ*r^2 + 4*r^2) /
  (16*(κ+1)^2*(2*κ+1))

def volume0 (r : ℝ) : ℝ :=
  r^2 / 4

def bracket (κ r : ℝ) : ℝ :=
  -8*r^2*κ^2 + (r^4 - 18*r^2 + 1)*κ - 8*r^2

def threshold : ℝ :=
  3 + 2 * Real.sqrt 2

theorem volume_zero (r : ℝ) : volume 0 r = volume0 r := by
  unfold volume volume0
  ring

theorem denominator_pos {κ : ℝ} (hk : 0 ≤ κ) :
    0 < 16*(κ+1)^2*(2*κ+1) := by
  have h1 : (0:ℝ) < κ + 1 := by linarith
  have h2 : (0:ℝ) < 2*κ + 1 := by linarith
  positivity

theorem volume_sub_volume0 (κ r : ℝ) (hk : 0 ≤ κ) :
    volume κ r - volume0 r =
      κ * bracket κ r / (16*(κ+1)^2*(2*κ+1)) := by
  have h1 : (κ + 1 : ℝ) ≠ 0 := by
    have : (0:ℝ) < κ + 1 := by linarith
    exact ne_of_gt this
  have h2 : (2*κ + 1 : ℝ) ≠ 0 := by
    have : (0:ℝ) < 2*κ + 1 := by linarith
    exact ne_of_gt this
  unfold volume volume0 bracket
  field_simp
  ring

theorem volume_gt_iff_bracket_gt {κ r : ℝ} (hk : 0 < κ) :
    volume κ r > volume0 r ↔ bracket κ r > 0 := by
  have hk0 : (0:ℝ) ≤ κ := hk.le
  have hden : (0:ℝ) < 16*(κ+1)^2*(2*κ+1) := denominator_pos hk0
  have hdiff : volume κ r - volume0 r
      = κ * bracket κ r / (16*(κ+1)^2*(2*κ+1)) :=
    volume_sub_volume0 κ r hk0
  constructor
  · intro h
    have hgt0 : (0:ℝ) < κ * bracket κ r / (16*(κ+1)^2*(2*κ+1)) := by
      have hpos : (0:ℝ) < volume κ r - volume0 r := by linarith
      rwa [hdiff] at hpos
    rcases div_pos_iff.mp hgt0 with ⟨hnum, _⟩ | ⟨hnum, hd⟩
    · rcases mul_pos_iff.mp hnum with ⟨_, hb⟩ | ⟨hneg, _⟩
      · exact hb
      · linarith
    · linarith
  · intro hb
    have hnum : (0:ℝ) < κ * bracket κ r := mul_pos hk hb
    have hgt0 : (0:ℝ) < κ * bracket κ r / (16*(κ+1)^2*(2*κ+1)) :=
      div_pos hnum hden
    have hpos : (0:ℝ) < volume κ r - volume0 r := by rwa [hdiff]
    linarith

/-!  =====================  STAGE 2  ===================== -/

def discr (r : ℝ) : ℝ :=
  (r^4 - 18*r^2 + 1)^2 - 256*r^4

theorem discr_factor (r : ℝ) :
    discr r = (r^2 - 1)^2 * (r^4 - 34*r^2 + 1) := by
  unfold discr
  ring

theorem bracket_one (r : ℝ) :
    bracket 1 r = r^4 - 34*r^2 + 1 := by
  unfold bracket
  ring

/-!  =====================  STAGE 3  ===================== -/

theorem sqrt_two_pos : 0 < Real.sqrt 2 :=
  Real.sqrt_pos.mpr (by norm_num)

theorem sqrt_two_sq : (Real.sqrt 2)^2 = 2 :=
  Real.sq_sqrt (by norm_num)

theorem threshold_pos : 0 < threshold := by
  unfold threshold
  have h := sqrt_two_pos
  linarith

theorem threshold_ge_one : 1 ≤ threshold := by
  unfold threshold
  have h := sqrt_two_pos
  linarith

theorem threshold_sq : threshold^2 = 17 + 12 * Real.sqrt 2 := by
  have h2 : (Real.sqrt 2)^2 = 2 := sqrt_two_sq
  unfold threshold
  nlinarith

theorem threshold_quartic :
    threshold^4 - 34 * threshold^2 + 1 = 0 := by
  have h2 : (Real.sqrt 2)^2 = 2 := sqrt_two_sq
  unfold threshold
  nlinarith [h2]

theorem conjugate_sq :
    (3 - 2 * Real.sqrt 2)^2 = 17 - 12 * Real.sqrt 2 := by
  have h2 : (Real.sqrt 2)^2 = 2 := sqrt_two_sq
  nlinarith

theorem threshold_conjugate_mul :
    threshold * (3 - 2 * Real.sqrt 2) = 1 := by
  have h2 : (Real.sqrt 2)^2 = 2 := sqrt_two_sq
  unfold threshold
  nlinarith

/-!  =====================  STAGE 4 (NOT YET CONFIRMED COMPILING)  ===================== -/

theorem sqrt_two_gt_four_thirds : (4:ℝ)/3 < Real.sqrt 2 := by
  nlinarith [sqrt_two_sq, sqrt_two_pos]

theorem conjugate_sq_lt_one : (3 - 2 * Real.sqrt 2)^2 < 1 := by
  rw [conjugate_sq]
  linarith [sqrt_two_gt_four_thirds]

/-- Exact factorization: r^4-34r^2+1 splits as (r^2 - threshold^2) times
    (r^2 - conjugate^2), where conjugate = 3 - 2√2 is the other root
    of x^2 - 34x + 1 = 0 (in x = r^2). -/
theorem quartic_factor (r : ℝ) :
    r^4 - 34*r^2 + 1 = (r^2 - threshold^2) * (r^2 - (3 - 2*Real.sqrt 2)^2) := by
  rw [threshold_sq, conjugate_sq]
  linear_combination (144:ℝ) * sqrt_two_sq

theorem factor_two_pos {r : ℝ} (hr : 1 ≤ r) :
    0 < r^2 - (3 - 2*Real.sqrt 2)^2 := by
  have h1 : (1:ℝ) ≤ r^2 := by nlinarith [sq_nonneg (r - 1)]
  have h2 : (3 - 2*Real.sqrt 2)^2 < 1 := conjugate_sq_lt_one
  linarith

/-- STAGE 4 MAIN RESULT. For r ≥ 1, the quartic is positive exactly
    above the threshold. -/
theorem quartic_gt_iff_gt_threshold {r : ℝ} (hr : 1 ≤ r) :
    r^4 - 34*r^2 + 1 > 0 ↔ r > threshold := by
  have hfact : r^4 - 34*r^2 + 1
      = (r^2 - threshold^2) * (r^2 - (3 - 2*Real.sqrt 2)^2) := quartic_factor r
  have hpos2 : 0 < r^2 - (3 - 2*Real.sqrt 2)^2 := factor_two_pos hr
  have htp : 0 < threshold := threshold_pos
  have hrp : 0 < r := by linarith
  have hsum_pos : 0 < r + threshold := by linarith
  rw [hfact]
  constructor
  · intro hprod
    have hfactor1 : 0 < r^2 - threshold^2 := by
      by_contra hcon
      push_neg at hcon
      nlinarith [mul_nonneg (neg_nonneg.mpr hcon) hpos2.le, hprod]
    have hd : 0 < r - threshold := by
      by_contra hcon
      push_neg at hcon
      nlinarith [mul_nonneg (neg_nonneg.mpr hcon) hsum_pos.le, hfactor1]
    linarith
  · intro hgt
    have hd : 0 < r - threshold := by linarith
    have hfactor1 : 0 < r^2 - threshold^2 := by
      nlinarith [mul_pos hd hsum_pos]
    exact mul_pos hfactor1 hpos2

end
end OUCorridor
