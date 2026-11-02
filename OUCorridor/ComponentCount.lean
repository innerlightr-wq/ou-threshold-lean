import OUCorridor.SinglePair

/-!
# Sign variations with a nonpositive tail, and the component-count bound

`docs/normalized-lyapunov/DERIVATION.md` §8 proves, for `L ⪰ 0`, `Q ≻ 0`, `H_κ = I + κL` and `Q̃`
with `k` nonzero off-diagonal pairs `E`, that with

    B(κ) = ∏_{{i,j} ∈ E} (a_i + a_j)²,    D(κ) = ∏_i a_i,    a_i = 1 + κλ_i,

the quantity `B · det(C ∘ Q̃)` is a *polynomial* of degree at most `2k`, and consequently

    det Σ_κ/det Σ_0 - 1 = κ A(κ) / (det Q · D(κ) · B(κ))

for a polynomial `A` with `A(0) = -4^k (det Q)(tr L) < 0` and **every coefficient in degree `≥ 2k`
nonpositive** — those degrees receive nothing from `B · det(C ∘ Q̃)`, only `-B·D·det Q`, whose
coefficients are nonnegative.

**This file formalizes the combinatorial consequence of that coefficient pattern**: a real
polynomial whose coefficients are nonpositive from degree `m` upwards has at most `m` sign
variations, hence (by Mathlib's Descartes rule of signs) at most `m` positive roots counted with
multiplicity. Applied with `m = 2k` this is the root count behind the bound
"at most `k` expansion components", each component needing two boundary roots.

Scope: the matrix-level construction of `A` (polynomiality, the degree bound, `A(0)`, the tail
sign pattern) is analytic and is verified by exact rational arithmetic in
`verification/normalized-lyapunov/components11.py`, against independent solves of `HΣ + ΣH = Q̃`.
The final step from "at most `2k` positive roots" to "at most `k` connected components" is also
analytic here (it needs that each bounded component contributes two boundary roots).
-/

namespace OUCorridor

open Polynomial

/-- A polynomial has at most `natDegree` sign variations. -/
theorem signVariations_le_natDegree (P : ℝ[X]) : P.signVariations ≤ P.natDegree := by
  suffices h : ∀ n : ℕ, ∀ P : ℝ[X], P.natDegree = n → P.signVariations ≤ n by
    exact h P.natDegree P rfl
  intro n
  induction n using Nat.strong_induction_on with
  | _ n ih =>
    intro P hP
    by_cases h0 : P = 0
    · simp [h0]
    rcases P.eraseLead_natDegree_lt_or_eraseLead_eq_zero with hlt | hz
    · have hkey := signVariations_eq_eraseLead_add_ite h0
      have hb := ih P.eraseLead.natDegree (by omega) P.eraseLead rfl
      have : P.signVariations ≤ P.eraseLead.signVariations + 1 :=
        signVariations_le_eraseLead_succ P
      omega
    · -- `P` is a monomial: the leading coefficient is nonzero, so the `ite` cannot fire
      have hkey := signVariations_eq_eraseLead_add_ite h0
      have hlc : SignType.sign P.leadingCoeff ≠ 0 := by
        simp [sign_eq_zero_iff, leadingCoeff_eq_zero, h0]
      rw [hz] at hkey
      simp only [signVariations_zero, leadingCoeff_zero, sign_zero, neg_zero] at hkey
      rw [if_neg hlc] at hkey
      omega

/-- **Sign variations with a nonpositive tail.**  If every coefficient of `A` in degree `≥ m` is
nonpositive, then `A` has at most `m` sign variations.

The coefficient list reads (from the top) a block of nonpositive entries, then the at most `m`
free entries in degrees `< m`; a sign sequence of that shape can alternate at most `m` times. -/
theorem signVariations_le_of_tail_nonpos {m : ℕ} {A : ℝ[X]}
    (htail : ∀ j, m ≤ j → A.coeff j ≤ 0) : A.signVariations ≤ m := by
  suffices h : ∀ n : ℕ, ∀ A : ℝ[X], A.natDegree = n → (∀ j, m ≤ j → A.coeff j ≤ 0) →
      A.signVariations ≤ m by
    exact h A.natDegree A rfl htail
  intro n
  induction n using Nat.strong_induction_on with
  | _ n ih =>
    intro A hA ht
    by_cases h0 : A = 0
    · simp only [h0, signVariations_zero]
      exact Nat.zero_le m
    by_cases hdeg : A.natDegree < m
    · exact le_trans (signVariations_le_natDegree A) (by omega)
    -- the leading coefficient sits in the nonpositive tail, hence is strictly negative
    have hlcneg : A.leadingCoeff < 0 := by
      have h1 : A.coeff A.natDegree ≤ 0 := ht A.natDegree (by omega)
      -- `leadingCoeff` is by definition `coeff _ natDegree`, so these are defeq
      have h2 : A.coeff A.natDegree ≠ 0 := leadingCoeff_ne_zero.mpr h0
      exact lt_of_le_of_ne h1 h2
    have hkey := signVariations_eq_eraseLead_add_ite h0
    rcases A.eraseLead_natDegree_lt_or_eraseLead_eq_zero with hlt | hz
    · set B := A.eraseLead with hB
      -- `B` inherits the tail hypothesis
      have htB : ∀ j, m ≤ j → B.coeff j ≤ 0 := by
        intro j hj
        by_cases hjd : j = A.natDegree
        · simp [hB, eraseLead_coeff, hjd]
        · rw [hB, eraseLead_coeff_of_ne j hjd]; exact ht j hj
      have hbd := ih B.natDegree (by omega) B rfl htB
      by_cases hcase : SignType.sign A.leadingCoeff = -SignType.sign B.leadingCoeff
      · -- the sign flipped, so `B`'s leading coefficient is positive and `B` has low degree
        rw [if_pos hcase] at hkey
        have hBpos : 0 < B.leadingCoeff := by
          have : SignType.sign A.leadingCoeff = -1 := by
            simpa using sign_eq_neg_one_iff.mpr hlcneg
          rw [this] at hcase
          have : SignType.sign B.leadingCoeff = 1 := by
            rcases h : SignType.sign B.leadingCoeff with _ | _ | _ <;> simp_all
          simpa using sign_eq_one_iff.mp this
        have hBdeg : B.natDegree < m := by
          by_contra hcon
          have h := htB B.natDegree (by omega)
          exact absurd hBpos (not_lt.mpr h)
        have := le_trans (signVariations_le_natDegree B) (by omega : B.natDegree ≤ m - 1)
        omega
      · rw [if_neg hcase] at hkey; omega
    · rw [hz] at hkey
      have hlc : SignType.sign A.leadingCoeff ≠ 0 := by
        simp [sign_eq_zero_iff, leadingCoeff_eq_zero, h0]
      simp only [signVariations_zero, leadingCoeff_zero, sign_zero, neg_zero] at hkey
      rw [if_neg hlc] at hkey
      omega

/-- **The root count behind the component bound.**  A real polynomial whose coefficients are
nonpositive from degree `m` on has at most `m` positive roots, counted with multiplicity.

With `m = 2k` and `A` the numerator polynomial of `det Σ_κ/det Σ_0 - 1`, this is the input to
"`k` correlated noise pairs ⟹ at most `k` expansion components": each bounded component of
`{κ > 0 : det Σ_κ > det Σ_0}` contributes two boundary roots of `A`. -/
theorem roots_pos_le_of_tail_nonpos {m : ℕ} {A : ℝ[X]}
    (htail : ∀ j, m ≤ j → A.coeff j ≤ 0) :
    A.roots.countP (0 < ·) ≤ m :=
  le_trans A.roots_countP_pos_le_signVariations (signVariations_le_of_tail_nonpos htail)

/-! ### Sharpness of the component bound at `k = 3`

Three *disjoint* correlated pairs attain the bound.  With `Q_b = [[1, b], [b, 1+b²]]` (positive
definite, `det Q_b = 1`), take

    Q̃ = diag(Q₃, Q₆₀, Q₃₅₀₀),    L = diag(0, 1000, 0, 1, 0, 1/10000).

`Q̃` has exactly three nonzero off-diagonal pairs, pairwise disjoint, so no determinant cycle terms
arise.  Both `Q̃` and `L` are block diagonal, so `det Σ_κ` and `det Σ_0` factor over blocks and

    det Σ_κ/det Σ_0 = ∏_j blockRatio a_j b_j κ,
    blockRatio a b κ = (1 + b²(aκ/(2+aκ))²)/(1 + aκ)

for a block with rates `0, a`.  Note this is a **product** over pairs, not a sum — the reason a
search restricted to star patterns (where all pairs share a mode) cannot find this witness.

The seven evaluations below alternate, forcing at least three expansion components; Theorem H
permits at most three, so there are exactly three.

As in the rest of this development, that `sharpRatio` *is* `det Σ_κ/det Σ_0` for this `(L, Q̃)` is
analytic; it is verified by exact rational arithmetic in
`verification/normalized-lyapunov/sharp12.py`, where each `Σ` is checked against `HΣ + ΣH = Q̃`,
together with a connected weighted-graph realization (six vertices, inter-pair edges `10⁻⁸`,
intra-pair edge `(a_j - 4·10⁻⁸)/2`) on which all seven signs survive. -/

/-- Determinant ratio contributed by one correlated block with damping rates `0, a` and
off-diagonal strength `b`. -/
noncomputable def blockRatio (a b κ : ℝ) : ℝ := (1 + b^2 * (a*κ/(2 + a*κ))^2) / (1 + a*κ)

/-- Determinant ratio of the three-pair witness. -/
noncomputable def sharpRatio (κ : ℝ) : ℝ :=
  blockRatio 1000 3 κ * blockRatio 1 60 κ * blockRatio (1/10000) 3500 κ

theorem sharpRatio_lt_one_at_1e5 : sharpRatio (1/100000) < 1 := by
  unfold sharpRatio blockRatio; norm_num

theorem sharpRatio_gt_one_at_500 : 1 < sharpRatio (1/500) := by
  unfold sharpRatio blockRatio; norm_num

theorem sharpRatio_lt_one_at_20 : sharpRatio (1/20) < 1 := by
  unfold sharpRatio blockRatio; norm_num

theorem sharpRatio_gt_one_at_1 : 1 < sharpRatio 1 := by
  unfold sharpRatio blockRatio; norm_num

theorem sharpRatio_lt_one_at_10 : sharpRatio 10 < 1 := by
  unfold sharpRatio blockRatio; norm_num

theorem sharpRatio_gt_one_at_100 : 1 < sharpRatio 100 := by
  unfold sharpRatio blockRatio; norm_num

theorem sharpRatio_lt_one_at_1000 : sharpRatio 1000 < 1 := by
  unfold sharpRatio blockRatio; norm_num

private lemma between_of_convex {K : Set ℝ} (hK : Convex ℝ K) {x y w p q : ℝ}
    (hx : x ∈ K) (hy : y ∈ K) (hp : 0 ≤ p) (hq : 0 ≤ q) (hpq : p + q = 1)
    (hw : p * x + q * y = w) : w ∈ K := by
  have h := hK hx hy hp hq hpq
  simp only [smul_eq_mul] at h
  rwa [hw] at h

/-- **Sharpness at `k = 3`.**  The expansion set of the three-pair witness is not the union of two
convex sets, hence has at least three connected components.  With Theorem H's bound of `k = 3`,
it has exactly three. -/
theorem sharp3_not_union_of_two_convex :
    ¬ ∃ I J : Set ℝ, Convex ℝ I ∧ Convex ℝ J ∧
      {κ : ℝ | 0 < κ ∧ 1 < sharpRatio κ} = I ∪ J := by
  rintro ⟨I, J, hI, hJ, hEq⟩
  have hmem : ∀ {κ : ℝ}, 0 < κ → 1 < sharpRatio κ → κ ∈ I ∪ J := by
    intro κ h1 h2; rw [← hEq]; exact ⟨h1, h2⟩
  have hout : ∀ {κ : ℝ}, sharpRatio κ < 1 → κ ∉ I ∪ J := by
    intro κ h hm
    rw [← hEq] at hm
    exact absurd hm.2 (not_lt.mpr h.le)
  have p1 : (1/500 : ℝ) ∈ I ∪ J := hmem (by norm_num) sharpRatio_gt_one_at_500
  have p2 : (1 : ℝ) ∈ I ∪ J := hmem (by norm_num) sharpRatio_gt_one_at_1
  have p3 : (100 : ℝ) ∈ I ∪ J := hmem (by norm_num) sharpRatio_gt_one_at_100
  have out20 : (1/20 : ℝ) ∉ I ∪ J := hout sharpRatio_lt_one_at_20
  have out10 : (10 : ℝ) ∉ I ∪ J := hout sharpRatio_lt_one_at_10
  -- the three convex-combination certificates
  have c12 : ∀ {K : Set ℝ}, Convex ℝ K → (1/500 : ℝ) ∈ K → (1 : ℝ) ∈ K → (1/20 : ℝ) ∈ K :=
    fun hK hx hy => between_of_convex hK hx hy (p := 475/499) (q := 24/499)
      (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  have c13 : ∀ {K : Set ℝ}, Convex ℝ K → (1/500 : ℝ) ∈ K → (100 : ℝ) ∈ K → (1/20 : ℝ) ∈ K :=
    fun hK hx hy => between_of_convex hK hx hy (p := 49975/49999) (q := 24/49999)
      (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  have c23 : ∀ {K : Set ℝ}, Convex ℝ K → (1 : ℝ) ∈ K → (100 : ℝ) ∈ K → (10 : ℝ) ∈ K :=
    fun hK hx hy => between_of_convex hK hx hy (p := 10/11) (q := 1/11)
      (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  rcases p1 with h1 | h1 <;> rcases p2 with h2 | h2 <;> rcases p3 with h3 | h3
  · exact out20 (Or.inl (c12 hI h1 h2))
  · exact out20 (Or.inl (c12 hI h1 h2))
  · exact out20 (Or.inl (c13 hI h1 h3))
  · exact out10 (Or.inr (c23 hJ h2 h3))
  · exact out10 (Or.inl (c23 hI h2 h3))
  · exact out20 (Or.inr (c13 hJ h1 h3))
  · exact out20 (Or.inr (c12 hJ h1 h2))
  · exact out20 (Or.inr (c12 hJ h1 h2))

/-! ### A necessary cost bound for attaining the full ceiling

Attaining `c = k` components forces `A` to realize all `2k` permitted sign variations, so its last
potentially positive coefficient must be strictly positive: `[κ^{2k-1}]A > 0`.  Since
`κA = N - B·D·det Q` with `deg N ≤ 2k`, that reads
`[κ^{2k}]N > det Q · [κ^{2k}](DB)`, and `N = B·det(C ∘ Q̃)` with `deg B = 2k` gives
`[κ^{2k}]N = [κ^{2k}]B · ρ_∞` where `ρ_∞ = det(C_∞ ∘ Q̃)/det Q̃`.  Hence the **necessary** condition

    ρ_∞  >  T(E, L) := [κ^{2k}](D·B) / [κ^{2k}]B,

and since Hadamard gives `ρ_∞ ≤ ρ = ∏ Q̃_ii/det Q̃`, also `ρ > T(E, L)`.

It is an exclusion test only: below the floor `k` components are impossible, above it they are not
guaranteed.  It is also not optimal — for a single isolated pair it yields `η > 4` where
Theorem F gives the exact `η > 8`.  Its interest is that the `k = 3` witness sits close to it.

For `k` disjoint blocks with rate pairs `(0, a_j)` the limiting channel removes every within-block
correlation, so `ρ_∞ = ρ = ∏_j (1 + η_j)`, and for three blocks the coefficient ratio evaluates to
`costFloor3` below.  Derivation and the exact coefficient computation:
`verification/normalized-lyapunov/cost13.py`. -/

/-- `T(E, L)` for three disjoint blocks with rate pairs `(0, a_j)`. -/
noncomputable def costFloor3 (a₁ a₂ a₃ : ℝ) : ℝ :=
  125 + 40 * (a₁/a₂ + a₁/a₃ + a₂/a₁ + a₂/a₃ + a₃/a₁ + a₃/a₂)
      + 4 * a₁ * a₂ * a₃ * (1/a₁^3 + 1/a₂^3 + 1/a₃^3)

/-- The `k = 3` witness clears the necessary floor, by about 10% in `ρ`. -/
theorem witness_rho_gt_costFloor3 :
    costFloor3 1000 1 (1/10000) < (1 + 3^2) * (1 + 60^2) * (1 + 3500^2 : ℝ) := by
  unfold costFloor3; norm_num

/-- Holding `b₁ = 3` and `b₂ = 60`, the choice `η₃ = 11000000` falls **below** the floor, so three
expansion components are impossible there — even though `η₃` is within 10% of the witness's
`η₃ = 3500² = 12250000`.  The large third correlation is therefore substantially forced within
this construction. -/
theorem eta3_11e6_lt_costFloor3 :
    (1 + 3^2) * (1 + 60^2) * (1 + 11000000 : ℝ) < costFloor3 1000 1 (1/10000) := by
  unfold costFloor3; norm_num

/-- The logical shape of the exclusion, in the form that covers every `c`.  Taking `m = 2c - 1`:
if every coefficient from degree `2c - 1` on is nonpositive then `A` has at most `2c - 1` positive
roots and hence at most `c - 1` components.  So **having at least `c` components requires
`[κ^j]A > 0` for some `j ∈ {2c-1, …, 2k-1}`** — the band narrows to the single coefficient
`[κ^{2k-1}]A` exactly when `c = k`, which is Theorem I. -/
theorem roots_pos_le_of_top_free_nonpos {k : ℕ} {A : ℝ[X]}
    (htail : ∀ j, 2*k - 1 ≤ j → A.coeff j ≤ 0) :
    A.roots.countP (0 < ·) ≤ 2*k - 1 :=
  roots_pos_le_of_tail_nonpos htail

/-! ### A sufficient criterion: monotone envelopes over parameter boxes

Everything above is an exclusion.  For a positive existence criterion, note that `blockRatio` is
monotone in each parameter separately: writing `gFactor z = (z/(2+z))²`, which increases on
`[0,∞)`, the numerator `1 + b² gFactor (aκ)` increases in both `a` and `b ≥ 0` while the
denominator `1 + aκ` increases in `a`.  So over a box `a ∈ [a⁻, a⁺]`, `b ∈ [b⁻, b⁺]`,

    (1 + (b⁻)² gFactor (a⁻κ))/(1 + a⁺κ)  ≤  blockRatio a b κ  ≤  (1 + (b⁺)² gFactor (a⁺κ))/(1 + a⁻κ).

Multiplying these over disjoint blocks bounds the determinant ratio outward.  If the upper product
is `< 1` at separating couplings and the lower product is `> 1` at interleaved ones, then **every**
parameter choice in the box has those separated windows — a sufficient condition for a whole
family rather than for sampled parameters.  Carried out in
`verification/normalized-lyapunov/boxes14.py`, this certifies boxes around

    (a_j) = (1000, 1, 10⁻⁴, 10⁻⁸, 10⁻¹²),   (b_j) = (3, 60, 3500, 45000, 2000000)

with `a_j` free in `±0.1%` and `b_j` in `±0.25%`, giving **exactly four** windows for the first
four blocks and **exactly five** for all five — so Theorem H is sharp at `k = 4` and `k = 5` too,
robustly in the parameters.

The criterion must control *separation*, not only strength: multiplying every `b_j` by `10` makes
every free coefficient of `A` positive, collapsing the sign pattern to `−,+,…,+,−,…,−` and leaving
a single component.  Raising the noise fills the contraction gaps.  A lower bound on noise strength
alone therefore cannot force several windows. -/

/-- The saturating factor in `blockRatio`. -/
noncomputable def gFactor (z : ℝ) : ℝ := (z/(2 + z))^2

theorem blockRatio_eq_gFactor (a b κ : ℝ) :
    blockRatio a b κ = (1 + b^2 * gFactor (a*κ))/(1 + a*κ) := rfl

/-- Cross-multiplication for a division inequality, proved without naming a division lemma. -/
private lemma div_le_div_cross {x y p q : ℝ} (hp : 0 < p) (hq : 0 < q) (h : x*q ≤ y*p) :
    x/p ≤ y/q := by
  have hd : y/q - x/p = (y*p - x*q)/(p*q) := by field_simp
  have hnn : (0:ℝ) ≤ (y*p - x*q)/(p*q) := div_nonneg (by linarith) (by positivity)
  linarith

/-- `gFactor` is monotone on `[0, ∞)`. -/
theorem gFactor_le_gFactor {z w : ℝ} (hz : 0 ≤ z) (hzw : z ≤ w) : gFactor z ≤ gFactor w := by
  have h2z : (0:ℝ) < 2 + z := by linarith
  have h2w : (0:ℝ) < 2 + w := by linarith
  have hfrac : z/(2 + z) ≤ w/(2 + w) :=
    div_le_div_cross h2z h2w (by nlinarith)
  have hnn : (0:ℝ) ≤ z/(2 + z) := by positivity
  exact pow_le_pow_left₀ hnn hfrac 2

/-- **Monotone envelope over a parameter box.**  Each block's ratio is sandwiched by the two
corner expressions, so a product of these bounds certifies an entire family of rates and noise
strengths at once. -/
theorem blockRatio_mem_box {alo ahi blo bhi a b κ : ℝ}
    (hκ : 0 < κ) (halo : 0 < alo) (ha1 : alo ≤ a) (ha2 : a ≤ ahi)
    (hblo : 0 ≤ blo) (hb1 : blo ≤ b) (hb2 : b ≤ bhi) :
    (1 + blo^2 * gFactor (alo*κ))/(1 + ahi*κ) ≤ blockRatio a b κ ∧
      blockRatio a b κ ≤ (1 + bhi^2 * gFactor (ahi*κ))/(1 + alo*κ) := by
  have ha : 0 < a := lt_of_lt_of_le halo ha1
  have hahi : 0 < ahi := lt_of_lt_of_le ha ha2
  have hb : 0 ≤ b := le_trans hblo hb1
  have d1 : (0:ℝ) < 1 + alo*κ := by positivity
  have d2 : (0:ℝ) < 1 + a*κ := by positivity
  have d3 : (0:ℝ) < 1 + ahi*κ := by positivity
  have hglo : gFactor (alo*κ) ≤ gFactor (a*κ) :=
    gFactor_le_gFactor (by positivity) (by nlinarith)
  have hghi : gFactor (a*κ) ≤ gFactor (ahi*κ) :=
    gFactor_le_gFactor (by positivity) (by nlinarith)
  have hgnn : (0:ℝ) ≤ gFactor (a*κ) := by unfold gFactor; positivity
  have hbsq1 : blo^2 ≤ b^2 := pow_le_pow_left₀ hblo hb1 2
  have hbsq2 : b^2 ≤ bhi^2 := pow_le_pow_left₀ hb hb2 2
  have hglonn : (0:ℝ) ≤ gFactor (alo*κ) := by unfold gFactor; positivity
  have hghinn : (0:ℝ) ≤ gFactor (ahi*κ) := by unfold gFactor; positivity
  rw [blockRatio_eq_gFactor]
  refine ⟨div_le_div_cross d3 d2 ?_, div_le_div_cross d2 d1 ?_⟩
  · -- (1 + blo² g(alo κ))(1 + aκ) ≤ (1 + b² g(aκ))(1 + ahi κ)
    have hnum : 1 + blo^2 * gFactor (alo*κ) ≤ 1 + b^2 * gFactor (a*κ) := by
      nlinarith [mul_le_mul hbsq1 hglo hglonn (sq_nonneg b)]
    have hden : 1 + a*κ ≤ 1 + ahi*κ := by nlinarith
    have h1 : (0:ℝ) ≤ 1 + blo^2 * gFactor (alo*κ) := by positivity
    exact mul_le_mul hnum hden (by positivity) (by nlinarith [hnum, h1])
  · -- (1 + b² g(aκ))(1 + alo κ) ≤ (1 + bhi² g(ahi κ))(1 + aκ)
    have hnum : 1 + b^2 * gFactor (a*κ) ≤ 1 + bhi^2 * gFactor (ahi*κ) := by
      nlinarith [mul_le_mul hbsq2 hghi hgnn (sq_nonneg bhi)]
    have hden : 1 + alo*κ ≤ 1 + a*κ := by nlinarith
    have h1 : (0:ℝ) ≤ 1 + b^2 * gFactor (a*κ) := by positivity
    exact mul_le_mul hnum hden (by positivity) (by nlinarith [hnum, h1])

/-! ### The saturation envelope behind the single-window cost

For disjoint blocks the normalized determinant gain is `G(κ) = ∏_j (1 + w_j u_j(κ))` with
`u_j = (s_jκ/(2 + s_jκ))² ∈ [0,1]`, and `ρ_∞ = ∏_j (1 + w_j)`.  Bounding every `u_j` by their
maximum `u_*` and applying the lemma below gives

    G(κ)  ≤  1 + (ρ_∞ - 1) u_*,

which combined with `D(κ) - 1 ≥ κ tr L` and `min_{x>0} (2+x)²/x = 8` (`sq_two_add_ge`) yields the
single-window cost `ρ_∞ > 1 + 8 (tr L)/s_*`, `s_* = max_{E}(λ_p + λ_q)`.  For one isolated pair
that is exactly `η > 8`, recovering Theorem F's sharp threshold where Theorem I alone gave `η > 4`.

Together with the coefficientwise domination `N ⪯ (det Q) ρ_∞ B` and the monotonicity of
`q_m = [κ^m](DB)/[κ^m]B`, this gives a necessary cost for *every* component count on matching
patterns:

    ρ_∞  >  max { 1 + 8 (tr L)/s_* ,  q_{2c} }.

The domination and the monotonicity of `q_m` are verified exactly in
`verification/normalized-lyapunov/interp15.py`; they are not formalized here. -/

/-- A product of `1 + w` with nonnegative weights is at least `1`. -/
theorem one_le_prod_one_add : ∀ (ws : List ℝ), (∀ w ∈ ws, 0 ≤ w) →
    1 ≤ (ws.map (fun w => 1 + w)).prod := by
  intro ws
  induction ws with
  | nil => intro _; simp
  | cons w t ih =>
      intro hw
      have hw0 : 0 ≤ w := hw w (List.mem_cons_self ..)
      have ht : 1 ≤ (t.map (fun w => 1 + w)).prod := ih fun x hx => hw x (List.mem_cons_of_mem _ hx)
      simp only [List.map_cons, List.prod_cons]
      nlinarith

/-- **Saturation envelope.**  For nonnegative weights and `0 ≤ u ≤ 1`,

    ∏_j (1 + w_j u)  ≤  1 + (∏_j (1 + w_j) - 1) u.

Each factor's gain is at most linear in the shared saturation level `u`, so the whole product is
controlled by the fully saturated value `ρ_∞ = ∏ (1 + w_j)`. -/
theorem prod_one_add_mul_le : ∀ (ws : List ℝ), (∀ w ∈ ws, 0 ≤ w) → ∀ {u : ℝ}, 0 ≤ u → u ≤ 1 →
    (ws.map (fun w => 1 + w*u)).prod ≤ 1 + ((ws.map (fun w => 1 + w)).prod - 1) * u := by
  intro ws
  induction ws with
  | nil => intro _ u _ _; simp
  | cons w t ih =>
      intro hw u hu0 hu1
      have hw0 : 0 ≤ w := hw w (List.mem_cons_self ..)
      have hmem : ∀ x ∈ t, 0 ≤ x := fun x hx => hw x (List.mem_cons_of_mem _ hx)
      have hIH := ih hmem hu0 hu1
      have hQ : 1 ≤ (t.map (fun w => 1 + w)).prod := one_le_prod_one_add t hmem
      have hfac : (0:ℝ) ≤ 1 + w*u := by positivity
      have hPnn : (0:ℝ) ≤ (t.map (fun w => 1 + w*u)).prod := by
        refine List.prod_nonneg ?_
        intro x hx
        rcases List.mem_map.mp hx with ⟨y, hy, rfl⟩
        have : 0 ≤ y := hmem y hy
        positivity
      simp only [List.map_cons, List.prod_cons]
      -- (1 + w u) * P ≤ (1 + w u) * (1 + (Q - 1) u) ≤ 1 + ((1+w) Q - 1) u
      have step1 : (1 + w*u) * (t.map (fun w => 1 + w*u)).prod
          ≤ (1 + w*u) * (1 + ((t.map (fun w => 1 + w)).prod - 1) * u) :=
        mul_le_mul_of_nonneg_left hIH hfac
      have step2 : (1 + w*u) * (1 + ((t.map (fun w => 1 + w)).prod - 1) * u)
          ≤ 1 + ((1 + w) * (t.map (fun w => 1 + w)).prod - 1) * u := by
        nlinarith [mul_nonneg (mul_nonneg hw0 hu0) (mul_nonneg (sub_nonneg.mpr hQ) (sub_nonneg.mpr hu1))]
      linarith

end OUCorridor
