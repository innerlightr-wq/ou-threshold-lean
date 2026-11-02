import OUCorridor.MainTheorem

/-!
# The normalized-Lyapunov form of the two-mode threshold

The repository proves the two-mode volume threshold `r > 3 + 2√2` by way of the quartic
discriminant of `bracket`.  That route is correct but opaque: the number `34` appears as a
coefficient and `3 + 2√2` as its root, with no indication of what either measures.

This file re-derives the *same* theorem through the normalized Lyapunov map.  Writing the
stationary covariance as the Schur multiplier `Φ_H(X)_{ij} = c_{ij} X_{ij}`,
`c_{ij} = 2√(a_i a_j)/(a_i + a_j)`, in the eigenbasis of the damping matrix `H`, dividing
`bracket` by the positive quantity `r² κ` separates it into

* `anisotropy r = (r - 1/r)²`, depending only on the noise, and
* `couplingCost κ = 8 (1 + κ)²/κ`, depending only on the coupling,

so that volume improvement is *exactly* the statement that the noise anisotropy exceeds the
cost of the coupling that would exploit it (`volume_gt_iff_anisotropy`).  The coupling cost is
minimized at `κ = 1` with value `32` (`couplingCost_ge`, `couplingCost_sub_32`), which is what
makes `32 < (r - 1/r)²`, i.e. `r > 3 + 2√2`, the exact threshold.

The two structural constants therefore acquire meanings: `32` is the minimal coupling cost, and
`κ = 1` is the coupling at which that cost is minimal, regardless of `r`.

**What `κ = 1` is and is not.**  `κ = 1` minimizes the *anisotropy required* for improvement, so
whenever any coupling improves the volume the unit coupling already does
(`unit_coupling_suffices`).  It does **not** maximize the volume: above the threshold the volume
is still strictly increasing at `κ = 1`, since
`d/dκ [volume κ r / volume0 r]` at `κ = 1` equals `((r - 1/r)² - 32)/144 > 0`.
`volume_one_not_maximal` records an explicit witness.

Nothing here is a new theorem about the model: `exists_improvement_iff_gt_threshold` below is
`MainTheorem.exists_volume_improvement_iff_threshold` with a different proof.  The analytic
derivation of `Φ_H`, its complete positivity, its multiplicative domain and the determinant
inequality `det Φ_H(Q) ≥ det Q` are *not* formalized here; they are classical facts about Schur
multipliers recorded in `docs/normalized-lyapunov/` and checked exactly in
`verification/normalized-lyapunov/`.
-/

namespace OUCorridor

noncomputable section

open Real

/-- Noise anisotropy: the only way the noise ratio `r` enters the threshold. -/
def anisotropy (r : ℝ) : ℝ := (r - 1/r)^2

/-- Cost of the coupling `κ`, as read off the normalized Lyapunov form. -/
def couplingCost (κ : ℝ) : ℝ := 8*(1+κ)^2/κ

/-- The normalization identity.  Dividing `bracket` by `r² κ > 0` splits it into a pure noise
term and a pure coupling term.  This is an algebraic identity, valid whenever `r ≠ 0` and
`κ ≠ 0`. -/
theorem bracket_normalized {κ r : ℝ} (hκ : κ ≠ 0) (hr : r ≠ 0) :
    bracket κ r = r^2 * κ * (anisotropy r - couplingCost κ) := by
  unfold bracket anisotropy couplingCost
  field_simp
  ring

/-- The coupling cost exceeds its floor `32` by an exact square. -/
theorem couplingCost_sub_32 {κ : ℝ} (hκ : κ ≠ 0) :
    couplingCost κ - 32 = 8*(κ-1)^2/κ := by
  unfold couplingCost
  field_simp
  ring

/-- `32` is the minimal coupling cost over all `κ > 0`. -/
theorem couplingCost_ge {κ : ℝ} (hκ : 0 < κ) : 32 ≤ couplingCost κ := by
  have h : couplingCost κ - 32 = 8*(κ-1)^2/κ := couplingCost_sub_32 (ne_of_gt hκ)
  have : (0:ℝ) ≤ 8*(κ-1)^2/κ := by positivity
  linarith

/-- The floor is attained only at `κ = 1`: the optimal coupling does not depend on the noise. -/
theorem couplingCost_eq_32_iff {κ : ℝ} (hκ : 0 < κ) : couplingCost κ = 32 ↔ κ = 1 := by
  have h : couplingCost κ - 32 = 8*(κ-1)^2/κ := couplingCost_sub_32 (ne_of_gt hκ)
  constructor
  · intro he
    have h0 : 8*(κ-1)^2/κ = 0 := by linarith
    have : (κ-1)^2 = 0 := by
      field_simp at h0
      linarith [h0]
    have := pow_eq_zero_iff (n := 2) (by norm_num) |>.mp this
    linarith
  · intro he
    subst he
    unfold couplingCost
    norm_num

/-- `couplingCost 1 = 32`. -/
theorem couplingCost_one : couplingCost 1 = 32 := by
  unfold couplingCost; norm_num

/-- **Explanatory form of the threshold.**  For positive coupling and positive noise ratio,
the volume improves exactly when the noise anisotropy strictly exceeds the coupling cost. -/
theorem volume_gt_iff_anisotropy {κ r : ℝ} (hκ : 0 < κ) (hr : 0 < r) :
    volume κ r > volume0 r ↔ couplingCost κ < anisotropy r := by
  rw [volume_gt_iff_bracket_gt hκ, bracket_normalized (ne_of_gt hκ) (ne_of_gt hr)]
  have hr2 : (0:ℝ) < r^2 := pow_pos hr 2
  have hpos : (0:ℝ) < r^2 * κ := mul_pos hr2 hκ
  constructor
  · intro h
    have := (mul_pos_iff.mp h)
    rcases this with ⟨_, h2⟩ | ⟨h1, _⟩
    · linarith
    · linarith
  · intro h
    have hd : (0:ℝ) < anisotropy r - couplingCost κ := by linarith
    exact mul_pos hpos hd

/-- The anisotropy exceeds `32` exactly above the repository's threshold (for `r ≥ 1`).
This identifies `32` as the minimal coupling cost and `3 + 2√2` as the noise ratio at which the
anisotropy first pays for it. -/
theorem anisotropy_gt_32_iff_gt_threshold {r : ℝ} (hr : 1 ≤ r) :
    32 < anisotropy r ↔ r > threshold := by
  have hr0 : (0:ℝ) < r := by linarith
  have hr2 : (0:ℝ) < r^2 := pow_pos hr0 2
  have hid : anisotropy r - 32 = (r^4 - 34*r^2 + 1)/r^2 := by
    unfold anisotropy
    field_simp
    ring
  rw [← quartic_gt_iff_gt_threshold hr]
  constructor
  · intro h
    have : (0:ℝ) < (r^4 - 34*r^2 + 1)/r^2 := by rw [← hid]; linarith
    exact (div_pos_iff.mp this).elim (fun p => p.1) (fun p => absurd p.2 (by linarith))
  · intro h
    have : (0:ℝ) < (r^4 - 34*r^2 + 1)/r^2 := div_pos h hr2
    rw [← hid] at this
    linarith

/-- **The repository's main theorem, re-derived through the normalized form.**  No discriminant
and no sum-of-squares certificate is used: improvement is possible iff the noise anisotropy
beats the minimal coupling cost `32`. -/
theorem exists_improvement_iff_gt_threshold {r : ℝ} (hr : 1 ≤ r) :
    (∃ κ, 0 < κ ∧ volume κ r > volume0 r) ↔ r > threshold := by
  have hr0 : (0:ℝ) < r := by linarith
  rw [← anisotropy_gt_32_iff_gt_threshold hr]
  constructor
  · rintro ⟨κ, hκ, hv⟩
    have h1 : couplingCost κ < anisotropy r := (volume_gt_iff_anisotropy hκ hr0).mp hv
    have h2 : (32:ℝ) ≤ couplingCost κ := couplingCost_ge hκ
    linarith
  · intro h
    refine ⟨1, by norm_num, ?_⟩
    rw [volume_gt_iff_anisotropy (by norm_num) hr0, couplingCost_one]
    exact h

/-- **The unit coupling always suffices.**  Whenever *some* coupling improves the volume, `κ = 1`
does, because `κ = 1` minimizes the coupling cost for every `r`.

This is a statement about *when improvement is possible*, not about the size of the improvement:
see `volume_one_not_maximal`. -/
theorem unit_coupling_suffices {r : ℝ} (hr : 1 ≤ r) (h : ∃ κ, 0 < κ ∧ volume κ r > volume0 r) :
    volume 1 r > volume0 r := by
  have hr0 : (0:ℝ) < r := by linarith
  have ht : r > threshold := (exists_improvement_iff_gt_threshold hr).mp h
  rw [volume_gt_iff_anisotropy (by norm_num) hr0, couplingCost_one]
  exact (anisotropy_gt_32_iff_gt_threshold hr).mpr ht

/-- At the threshold itself the unit coupling gives exact equality: the minimal coupling cost is
paid exactly.  (`bracket 1 threshold = 0` is the repository's `threshold_quartic`.) -/
theorem anisotropy_threshold : anisotropy threshold = 32 := by
  have h4 : threshold^4 - 34 * threshold^2 + 1 = 0 := threshold_quartic
  have hp : (0:ℝ) < threshold := threshold_pos
  have hne : threshold ≠ 0 := ne_of_gt hp
  unfold anisotropy
  field_simp
  nlinarith [h4]

/-- `κ = 1` is **not** volume-maximizing.  At `r = 9` (above the threshold `3 + 2√2`) the
coupling `κ = 3/2` gives a strictly larger stationary volume than `κ = 1`:
`volume 1 9 = 481/12 < 657/16 = volume (3/2) 9`.

So `unit_coupling_suffices` must not be read as "`κ = 1` is optimal".  The correct reading is
that the *coupling cost* `couplingCost` is minimized at `κ = 1`. -/
theorem volume_one_not_maximal : volume 1 9 < volume (3/2) 9 := by
  unfold volume
  norm_num

/-- For the same reason, improvement at `κ = 1` does not exhaust the improving couplings. -/
theorem volume_three_halves_improves : volume (3/2) 9 > volume0 9 := by
  unfold volume volume0
  norm_num

end
end OUCorridor
