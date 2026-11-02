import OUCorridor.NormalizedLyapunov

/-!
# The single-correlated-pair threshold: convexity, uniqueness, interval

Let `L ⪰ 0`, `H_κ = I + κL` with eigenvalues `λ_i`, and let `Q ≻ 0` be a noise matrix whose
rotation `Q̃` into an eigenbasis of `L` has exactly one off-diagonal Hermitian pair `(p,q)`.
Writing

    η = |Q̃_pq|²/(Q̃_pp Q̃_qq - |Q̃_pq|²),  s = λ_p + λ_q,  Δ = λ_p - λ_q,  D(κ) = ∏_i (1 + κλ_i),

the determinant identity of `docs/normalized-lyapunov/DERIVATION.md` gives

    det Σ_κ / det Σ_0 = (1 + η κ²Δ²/(2 + sκ)²) / D(κ),

so volume expansion at coupling `κ > 0` is exactly `η > T κ` with

    T κ = (D κ - 1)(2 + sκ)²/(κ²Δ²).

Expanding `D κ - 1 = ∑_{j≥1} e_j κ^j` (elementary symmetric functions of the `λ_i`, all `≥ 0`,
with `e_1 = tr L`) and multiplying out `(2 + sκ)²` shows that `T` has the shape

    T κ = A/κ + ∑_{j ∈ s} c_j κ^j,     A = 4 (tr L)/Δ² > 0,   c_j ≥ 0.                (★)

**This file formalizes the consequences of (★).**  Every statement below is about a function of
the shape (★); the matrix-level derivation of (★) itself is analytic and is verified by exact
rational arithmetic in `verification/normalized-lyapunov/singlepair9.py`, not in Lean.

Consequences proved here: `T` is strictly convex on `(0,∞)`; hence the set of couplings at which
expansion occurs is an **interval**, and a minimizer of `T` is **unique** — so at the critical `η`
the determinant ratio touches `1` at exactly one coupling.  Separately, a purely algebraic
argument gives the floor `T κ ≥ 8 (tr L) s/Δ²`, which is `≥ 8` whenever `Δ² ≤ s² ≤ (tr L) s`.

The two models already in this repository are instances:

| model | `η` | `A` | `(c_j)` | onset |
|---|---|---|---|---|
| two modes | `(r - 1/r)²/4` | `2` | `(4, 2)` | `κ† = 1`, `η_crit = 8` |
| three-node path, centre noise | `2(r - 1/r)²/9` | `16/9` | `(20/3, 8, 3)` | `27κ³ + 36κ² - 8 = 0` |

`twoMode_thresholdFn_eq` and `centre_thresholdFn_eq` below identify them, and
`couplingCost_eq_four_mul_thresholdFn` connects the first to
`OUCorridor.couplingCost` from `NormalizedLyapunov.lean`.
-/

namespace OUCorridor

noncomputable section

open Set

/-- `κ ^ j` is convex on `(0,∞)`, for every `j` (including `0` and `1`). -/
theorem convexOn_pow_Ioi (j : ℕ) : ConvexOn ℝ (Ioi (0 : ℝ)) (fun κ : ℝ => κ ^ j) := by
  match j with
  | 0 =>
      refine ⟨convex_Ioi 0, fun x _ y _ a b _ _ hab => ?_⟩
      simp only [pow_zero, smul_eq_mul]
      linarith
  | 1 =>
      refine ⟨convex_Ioi 0, fun x _ y _ a b _ _ _ => ?_⟩
      simp only [pow_one, smul_eq_mul]
      exact le_refl _
  | (n+2) =>
      exact ((strictConvexOn_pow (by omega : 2 ≤ n + 2)).convexOn).subset
        Ioi_subset_Ici_self (convex_Ioi (0 : ℝ))

/-- Scaling a convex function by a nonnegative constant keeps it convex.  Stated with `*` rather
than `•` to stay clear of the `ConvexOn ℝ ℝ ℝ` scalar-instance diamond. -/
theorem ConvexOn.const_mul' {S : Set ℝ} {f : ℝ → ℝ} (hf : ConvexOn ℝ S f) {c : ℝ} (hc : 0 ≤ c) :
    ConvexOn ℝ S (fun x => c * f x) := by
  refine ⟨hf.1, fun x hx y hy a b ha hb hab => ?_⟩
  have h := hf.2 hx hy ha hb hab
  simp only [smul_eq_mul] at h ⊢
  nlinarith [h, hc]

/-- A monomial with a nonnegative coefficient is convex on `(0,∞)`. -/
theorem convexOn_monomial {c : ℝ} (hc : 0 ≤ c) (j : ℕ) :
    ConvexOn ℝ (Ioi (0 : ℝ)) (fun κ : ℝ => c * κ ^ j) :=
  ConvexOn.const_mul' (convexOn_pow_Ioi j) hc

/-- A polynomial with nonnegative coefficients is convex on `(0,∞)`. -/
theorem convexOn_polynomial (S : Finset ℕ) {c : ℕ → ℝ} (hc : ∀ j ∈ S, 0 ≤ c j) :
    ConvexOn ℝ (Ioi (0 : ℝ)) (fun κ : ℝ => ∑ j ∈ S, c j * κ ^ j) := by
  classical
  induction S using Finset.induction with
  | empty =>
      refine ⟨convex_Ioi 0, fun x _ y _ a b _ _ hab => ?_⟩
      simp only [Finset.sum_empty, smul_eq_mul]
      linarith
  | insert a S ha ih =>
      refine ⟨convex_Ioi 0, fun x hx y hy p q hp hq hpq => ?_⟩
      have h1 := (convexOn_monomial (hc a (Finset.mem_insert_self a S)) a).2 hx hy hp hq hpq
      have h2 := (ih (fun j hj => hc j (Finset.mem_insert_of_mem hj))).2 hx hy hp hq hpq
      simp only [Finset.sum_insert ha, smul_eq_mul] at h1 h2 ⊢
      linarith

/-- `1/κ` is strictly convex on `(0,∞)`. -/
theorem strictConvexOn_one_div_pos :
    StrictConvexOn ℝ (Ioi (0 : ℝ)) (fun κ : ℝ => 1 / κ) := by
  have h := strictConvexOn_zpow (m := (-1 : ℤ)) (by decide) (by decide)
  refine ⟨convex_Ioi 0, fun x hx y hy hxy a b ha hb hab => ?_⟩
  have := h.2 hx hy hxy ha hb hab
  simpa [zpow_neg, zpow_one, one_div] using this

/-- `A/κ` with `A > 0` is strictly convex on `(0,∞)`. -/
theorem strictConvexOn_const_div {A : ℝ} (hA : 0 < A) :
    StrictConvexOn ℝ (Ioi (0 : ℝ)) (fun κ : ℝ => A / κ) := by
  refine ⟨convex_Ioi 0, fun x hx y hy hxy a b ha hb hab => ?_⟩
  have h := strictConvexOn_one_div_pos.2 hx hy hxy ha hb hab
  simp only [smul_eq_mul, one_div] at h ⊢
  rw [div_eq_mul_inv, div_eq_mul_inv, div_eq_mul_inv]
  nlinarith [h, hA]

/-- The threshold function in the normal form (★): a positive multiple of `1/κ` plus a
polynomial with nonnegative coefficients. -/
def thresholdFn (A : ℝ) (S : Finset ℕ) (c : ℕ → ℝ) : ℝ → ℝ :=
  fun κ => A / κ + ∑ j ∈ S, c j * κ ^ j

/-- **`T` is strictly convex on `(0,∞)`.**  This is the structural fact behind everything else:
the `1/κ` term coming from `e_1 = tr L > 0` is strictly convex, and no other term can cancel it
because all remaining coefficients are nonnegative. -/
theorem strictConvexOn_thresholdFn {A : ℝ} (hA : 0 < A) (S : Finset ℕ) {c : ℕ → ℝ}
    (hc : ∀ j ∈ S, 0 ≤ c j) :
    StrictConvexOn ℝ (Ioi (0 : ℝ)) (thresholdFn A S c) := by
  refine ⟨convex_Ioi 0, fun x hx y hy hxy p q hp hq hpq => ?_⟩
  have h1 := (strictConvexOn_const_div hA).2 hx hy hxy hp hq hpq
  have h2 := (convexOn_polynomial S hc).2 hx hy hp.le hq.le hpq
  simp only [thresholdFn, smul_eq_mul] at h1 h2 ⊢
  linarith

/-- **The expansion set is an interval.**  For a fixed noise parameter `η`, the couplings at
which the volume strictly expands form a convex subset of `(0,∞)`.  Combined with
`T → ∞` at both ends (not formalized), this is the "exactly one bounded interval" statement. -/
theorem convex_expansion_set {A : ℝ} (hA : 0 < A) (S : Finset ℕ) {c : ℕ → ℝ}
    (hc : ∀ j ∈ S, 0 ≤ c j) (η : ℝ) :
    Convex ℝ {κ ∈ Ioi (0 : ℝ) | thresholdFn A S c κ < η} :=
  ((strictConvexOn_thresholdFn hA S hc).convexOn).convex_lt η

/-- **The onset coupling is unique.**  Any two minimizers of `T` on `(0,∞)` coincide; so at the
critical noise level the determinant ratio touches `1` at exactly one coupling. -/
theorem onset_coupling_unique {A : ℝ} (hA : 0 < A) (S : Finset ℕ) {c : ℕ → ℝ}
    (hc : ∀ j ∈ S, 0 ≤ c j) {κ₁ κ₂ : ℝ}
    (h₁ : IsMinOn (thresholdFn A S c) (Ioi (0 : ℝ)) κ₁)
    (h₂ : IsMinOn (thresholdFn A S c) (Ioi (0 : ℝ)) κ₂)
    (hκ₁ : κ₁ ∈ Ioi (0 : ℝ)) (hκ₂ : κ₂ ∈ Ioi (0 : ℝ)) :
    κ₁ = κ₂ :=
  (strictConvexOn_thresholdFn hA S hc).eq_of_isMinOn h₁ h₂ hκ₁ hκ₂

/-! ### The algebraic floor

`T κ ≥ 8 (tr L)(λ_p + λ_q)/Δ²`, proved from `D κ - 1 ≥ κ tr L` and `(2 + sκ)² ≥ 8sκ`.
No convexity is used. -/

/-- `(2 + sκ)² ≥ 8sκ`, with equality exactly at `sκ = 2`.  This is what fixes the onset
coupling of the *bound* at `κ = 2/s`. -/
theorem sq_two_add_ge {s κ : ℝ} : 8 * (s * κ) ≤ (2 + s * κ)^2 := by
  nlinarith [sq_nonneg (2 - s * κ)]

/-- **The threshold floor**, in cleared form.  If `D κ - 1 ≥ κ · trL` (true for
`D κ = ∏(1 + κλ_i)` with `λ_i ≥ 0` and `trL = ∑ λ_i`), then

    8 (trL) s κ²  ≤  (D κ - 1)(2 + sκ)².

Dividing by `κ²Δ² > 0` is exactly `T κ ≥ 8 (trL) s/Δ²`.  The division is omitted so that the
statement needs no positivity hypothesis on `Δ`. -/
theorem thresholdFloor {Dk trL s κ : ℝ} (htr : 0 ≤ trL) (hs : 0 < s)
    (hκ : 0 < κ) (hD : κ * trL ≤ Dk - 1) :
    8 * trL * s * κ^2 ≤ (Dk - 1) * (2 + s * κ)^2 := by
  have hc : (0 : ℝ) ≤ 8 * (s * κ) := by positivity
  have hb : (0 : ℝ) ≤ Dk - 1 := le_trans (by positivity) hD
  have h := mul_le_mul hD sq_two_add_ge hc hb
  nlinarith [h]

/-- The floor is at least `8` whenever `Δ² ≤ s²` and `s ≤ trL` — i.e. for any `L ⪰ 0`, since
`(λ_p - λ_q)² ≤ (λ_p + λ_q)²` and `λ_p + λ_q ≤ tr L`.  **Adding damped modes without adding
noise correlation can never lower the threshold below `8`.** -/
theorem thresholdFloor_ge_eight {trL s Δ : ℝ} (hs : 0 < s) (hΔ : Δ ≠ 0)
    (hts : s ≤ trL) (hΔs : Δ^2 ≤ s^2) :
    8 ≤ 8 * trL * s / Δ^2 := by
  have hΔ2 : 0 < Δ^2 := by positivity
  rw [le_div_iff₀ hΔ2]
  nlinarith [mul_le_mul_of_nonneg_right hts hs.le]

/-! ### The two repository models as instances -/

/-- Two modes: `L` has eigenvalues `0, 2`, so `A = 2` and the polynomial part is `4 + 2κ`. -/
theorem twoMode_thresholdFn_eq {κ : ℝ} (hκ : κ ≠ 0) :
    thresholdFn 2 {0, 1} (fun j => if j = 0 then 4 else 2) κ = 2 * (1 + κ)^2 / κ := by
  simp only [thresholdFn, Finset.sum_insert, Finset.mem_singleton, Finset.sum_singleton]
  norm_num
  field_simp
  ring

/-- The two-mode threshold function is exactly a quarter of `couplingCost`, so the single-pair
theorem contains `exists_improvement_iff_gt_threshold` as its `n = 2` case. -/
theorem couplingCost_eq_four_mul_thresholdFn {κ : ℝ} (hκ : κ ≠ 0) :
    couplingCost κ = 4 * thresholdFn 2 {0, 1} (fun j => if j = 0 then 4 else 2) κ := by
  rw [twoMode_thresholdFn_eq hκ]
  unfold couplingCost
  field_simp
  ring

/-- Three-node path with centre-node noise: `L` has eigenvalues `0, 1, 3`, the correlated pair is
`(0, 2)`, so `A = 16/9` and the polynomial part is `20/3 + 8κ + 3κ²`. -/
theorem centre_thresholdFn_eq {κ : ℝ} (hκ : κ ≠ 0) :
    thresholdFn (16/9) {0, 1, 2} (fun j => if j = 0 then 20/3 else if j = 1 then 8 else 3) κ
      = (4 + 3*κ) * (2 + 3*κ)^2 / (9*κ) := by
  simp only [thresholdFn, Finset.sum_insert, Finset.mem_insert, Finset.mem_singleton,
    Finset.sum_singleton]
  norm_num
  field_simp
  ring

/-- Both instances satisfy the hypotheses of the general theorems. -/
theorem twoMode_coeffs_nonneg :
    ∀ j ∈ ({0, 1} : Finset ℕ), (0 : ℝ) ≤ (fun j => if j = 0 then (4 : ℝ) else 2) j := by
  intro j _
  dsimp only
  split_ifs <;> norm_num

theorem centre_coeffs_nonneg :
    ∀ j ∈ ({0, 1, 2} : Finset ℕ),
      (0 : ℝ) ≤ (fun j => if j = 0 then (20/3 : ℝ) else if j = 1 then 8 else 3) j := by
  intro j _
  dsimp only
  split_ifs <;> norm_num

/-- The two-mode expansion set is an interval, as an instance of the general theorem. -/
theorem twoMode_convex_expansion (η : ℝ) :
    Convex ℝ {κ ∈ Ioi (0 : ℝ) |
      thresholdFn 2 {0, 1} (fun j => if j = 0 then 4 else 2) κ < η} :=
  convex_expansion_set (by norm_num) _ twoMode_coeffs_nonneg η

/-- The three-node centre-noise expansion set is an interval. -/
theorem centre_convex_expansion (η : ℝ) :
    Convex ℝ {κ ∈ Ioi (0 : ℝ) |
      thresholdFn (16/9) {0, 1, 2}
        (fun j => if j = 0 then 20/3 else if j = 1 then 8 else 3) κ < η} :=
  convex_expansion_set (by norm_num) _ centre_coeffs_nonneg η

/-! ### Sharpness: multiple correlated pairs can split the expansion set

The single-pair hypothesis of `convex_expansion_set` cannot be dropped.  In the damping
eigenbasis take

    L = diag(0, 100, 1),    Q̃ = [[2035, 3, 45], [3, 1, 0], [45, 0, 1]]

(positive definite: leading principal minors `2035, 2026, 1`; realized on a *connected* weighted
triangle with edge weights `299/6, 1/3, 1/3`).  `Q̃` has **two** correlated pairs, `(0,1)` and
`(0,2)`, at damping scales `100` and `1`, and `Q̃₁₂ = 0`, so the determinant cycle term vanishes.
The determinant identity gives the ratio `witnessRatio` below, and the three evaluations
`witnessRatio_lt_one_at_tenth` sandwiched by `..._gt_one_at_fiftieth` and `..._gt_one_at_one`
show the expansion set is **disconnected**.

Scope, as elsewhere in this file: that `witnessRatio` *is* `det Σ_κ/det Σ_0` for this `(L, Q̃)` is
the analytic determinant identity, verified by exact rational arithmetic in
`verification/normalized-lyapunov/multipair10.py` against an independent solve of
`HΣ + ΣH = Q̃`.  Lean checks the three inequalities that make the set disconnected. -/

/-- Determinant ratio of the two-pair witness, `det Σ_κ/det Σ_0`. -/
def witnessRatio (κ : ℝ) : ℝ :=
  (1 + 9 * (100*κ/(2 + 100*κ))^2 + 2025 * (κ/(2 + κ))^2) / ((1 + 100*κ) * (1 + κ))

theorem witnessRatio_gt_one_at_fiftieth : 1 < witnessRatio (1/50) := by
  unfold witnessRatio; norm_num

theorem witnessRatio_lt_one_at_tenth : witnessRatio (1/10) < 1 := by
  unfold witnessRatio; norm_num

theorem witnessRatio_gt_one_at_one : 1 < witnessRatio 1 := by
  unfold witnessRatio; norm_num

/-- **The expansion set need not be an interval.**  For the two-pair witness there are couplings
`κ₁ < κ₂ < κ₃` with expansion at `κ₁` and `κ₃` but contraction at `κ₂`, so
`{κ > 0 | witnessRatio κ > 1}` is not convex.  Compare `convex_expansion_set`, which assumes a
single correlated pair. -/
theorem witness_expansion_set_not_convex :
    ¬ Convex ℝ {κ ∈ Ioi (0 : ℝ) | 1 < witnessRatio κ} := by
  intro hconv
  have h1 : (1/50 : ℝ) ∈ {κ ∈ Ioi (0 : ℝ) | 1 < witnessRatio κ} :=
    ⟨by norm_num, witnessRatio_gt_one_at_fiftieth⟩
  have h3 : (1 : ℝ) ∈ {κ ∈ Ioi (0 : ℝ) | 1 < witnessRatio κ} :=
    ⟨by norm_num, witnessRatio_gt_one_at_one⟩
  -- (90/98)·(1/50) + (8/98)·1 = 1/10 exactly, so 1/10 would have to lie in the set
  have hmem := hconv h1 h3 (a := 90/98) (b := 8/98) (by norm_num) (by norm_num) (by norm_num)
  have e : ((90 : ℝ)/98) • ((1 : ℝ)/50) + ((8 : ℝ)/98) • (1 : ℝ) = 1/10 := by
    simp only [smul_eq_mul]; norm_num
  rw [e] at hmem
  exact absurd hmem.2 (not_lt.mpr witnessRatio_lt_one_at_tenth.le)

end
end OUCorridor
