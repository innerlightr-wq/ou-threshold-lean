# Scope: what is proved, where, and what is not

## Machine-checked in Lean (`OUCorridor/NormalizedLyapunov.lean`)

Built against the pinned toolchain `leanprover/lean4:v4.33.1` with Mathlib `v4.33.1`
(`lake build`, 8716 jobs, no errors). No `sorry`, no `admit`, no `axiom`, no `native_decide`.
`#print axioms` reports only `[propext, Classical.choice, Quot.sound]` for all 55 of:

| theorem | statement |
|---|---|
| `bracket_normalized` | `bracket κ r = r²κ (anisotropy r - couplingCost κ)` |
| `couplingCost_sub_32` | `couplingCost κ - 32 = 8(κ-1)²/κ` |
| `couplingCost_ge` | `32 ≤ couplingCost κ` for `κ > 0` |
| `couplingCost_eq_32_iff` | the floor is attained iff `κ = 1` |
| `volume_gt_iff_anisotropy` | `volume κ r > volume0 r ⟺ couplingCost κ < anisotropy r` |
| `anisotropy_gt_32_iff_gt_threshold` | `32 < anisotropy r ⟺ r > threshold` (for `r ≥ 1`) |
| `exists_improvement_iff_gt_threshold` | the repository's main theorem, re-derived |
| `unit_coupling_suffices` | if any coupling improves the volume, `κ = 1` does |
| `anisotropy_threshold` | `anisotropy threshold = 32` |
| `volume_one_not_maximal` | `volume 1 9 < volume (3/2) 9` — `κ = 1` is *not* volume-maximizing |
| `volume_three_halves_improves` | `volume (3/2) 9 > volume0 9` |

And in `OUCorridor/SinglePair.lean`, the single-correlated-pair theorem (Theorem F and G of
[DERIVATION.md](DERIVATION.md)):

| theorem | statement |
|---|---|
| `convexOn_pow_Ioi`, `ConvexOn.const_mul'`, `convexOn_monomial` | building blocks |
| `convexOn_polynomial` | a polynomial with nonnegative coefficients is convex on `(0,∞)` |
| `strictConvexOn_one_div_pos`, `strictConvexOn_const_div` | `A/κ` is strictly convex for `A > 0` |
| `strictConvexOn_thresholdFn` | **`T` is strictly convex on `(0,∞)`** under the normal form (★) |
| `convex_expansion_set` | **the set of expanding couplings is an interval** |
| `onset_coupling_unique` | **the minimizer of `T` is unique** |
| `sq_two_add_ge` | `(2+sκ)² ≥ 8sκ` |
| `thresholdFloor` | `8(trL)sκ² ≤ (D κ - 1)(2+sκ)²`, i.e. `T κ ≥ 8(trL)s/Δ²` |
| `thresholdFloor_ge_eight` | that floor is `≥ 8` whenever `Δ² ≤ s² ≤ (trL)s` |
| `twoMode_thresholdFn_eq`, `centre_thresholdFn_eq` | both repository models in normal form |
| `couplingCost_eq_four_mul_thresholdFn` | `couplingCost = 4T`, so §4 is the `n = 2` case |
| `twoMode_convex_expansion`, `centre_convex_expansion` | the interval theorem, instantiated |
| `witnessRatio`, `witnessRatio_gt_one_at_fiftieth`, `witnessRatio_lt_one_at_tenth`, `witnessRatio_gt_one_at_one` | the two-pair witness and its three decisive evaluations |
| `witness_expansion_set_not_convex` | **the single-pair hypothesis is not removable**: the expansion set can be disconnected |

And in `OUCorridor/ComponentCount.lean`, the combinatorial core of Theorem H:

| theorem | statement |
|---|---|
| `signVariations_le_natDegree` | a polynomial has at most `natDegree` sign variations |
| `signVariations_le_of_tail_nonpos` | **coefficients nonpositive from degree `m` on ⟹ at most `m` sign variations** |
| `roots_pos_le_of_tail_nonpos` | … hence at most `m` positive roots with multiplicity (via Mathlib's `Polynomial.roots_countP_pos_le_signVariations`) |
| `blockRatio`, `sharpRatio` | the three-disjoint-pair witness `Q̃ = diag(Q₃, Q₆₀, Q₃₅₀₀)`, `L = diag(0,1000,0,1,0,1/10000)` |
| `sharpRatio_lt_one_at_1e5` … `sharpRatio_lt_one_at_1000` | its seven alternating evaluations |
| `sharp3_not_union_of_two_convex` | **Theorem H is sharp at `k = 3`**: the expansion set is not a union of two convex sets, so it has at least three components — and at most three by Theorem H |
| `costFloor3` | `T(E,L)` for three disjoint `(0,a_j)` blocks |
| `witness_rho_gt_costFloor3` | the `k = 3` witness clears the necessary cost floor |
| `eta3_11e6_lt_costFloor3` | `η₃ = 11000000` falls below it, so three components are impossible there |
| `roots_pos_le_of_top_free_nonpos` | the exclusion's logical shape: a nonpositive top free coefficient caps the roots at `2k − 1` |
| `gFactor`, `blockRatio_eq_gFactor` | the saturating factor `g(z) = (z/(2+z))²` |
| `gFactor_le_gFactor` | `g` is monotone on `[0,∞)` |
| `blockRatio_mem_box` | **the monotone envelope**: over a box of rates and strengths, each block's ratio is bracketed by the two corner expressions |
| `one_le_prod_one_add` | `∏(1 + w_j) ≥ 1` for nonnegative weights |
| `prod_one_add_mul_le` | **the saturation envelope** `∏(1 + w_j u) ≤ 1 + (∏(1 + w_j) − 1)u` for `0 ≤ u ≤ 1`, the engine of Theorem J's single-window term |

**What is *not* in Lean here.** The matrix-level derivation of the normal form (★) — Theorems D
and E, i.e. the determinant identity for a single off-diagonal pair and the elementary-symmetric
expansion — is analytic and is checked by exact rational arithmetic, not formalized. The Lean file
takes (★) as its hypothesis and proves its consequences. `T → ∞` at both ends is also not
formalized, so Lean gives *uniqueness of a minimizer* and *convexity of the expansion set*, but
not *existence* of the minimizer.

`exists_improvement_iff_gt_threshold` is **the same statement** as
`MainTheorem.exists_volume_improvement_iff_threshold`. It is not a new theorem; it is a second,
discriminant-free proof. Nothing in the existing files was changed.

## Checked by exact rational arithmetic, not formalized

`verification/normalized-lyapunov/run_all.sh` — **144 checks, 144 passing**, standard library only
(no numpy/sympy/mpmath on this machine), exact `Fraction` arithmetic throughout; floats appear
only in printed diagnostics.

| file | checks | content |
|---|---|---|
| `verify.py` | 24 | Lemmas 1–3, two-mode agreement with `volume`/`volume0` at 25 exact `(κ,r)`, the determinant theorem, the Hadamard ceiling |
| `threemode2.py` | 9 | three-mode Theorem B; eigenbasis formula vs. an independent original-basis Lyapunov solve |
| `threshold3.py` | 4 | two-sided certification of the three-mode brackets (Theorem C) |
| `controls6.py` | 11 | discriminating controls (§ below) |
| `priorart7.py` | 6 | the prior-art classification controls and the Theorem A sandwich |
| `interp15.py` | 11 | Theorem J: the per-block identity and coefficientwise domination `N ⪯ (det Q)ρ_∞B` across six matching instances, monotonicity of `q_m` at eleven rate configurations, the endpoint `η > 8`, the three-block floor table, and the enlarged `5/3×` boxes |
| `boxes14.py` | 10 | the sufficient criterion: monotonicity of `g`, the nominal `k = 4, 5` families with Descartes saturated, all eleven box bounds by exact rational envelope arithmetic, corner spot-checks, the merge correction under `b_j ↦ 10b_j`, and the band constraint (17) |
| `cost13.py` | 10 | Theorem I: the closed form (15) against the coefficient ratio, `ρ_∞ = ρ` for disjoint `(0,a)` blocks, the exact floor `T = 400400440125.444004…`, the forced `b₃ > 3334.538168…`, the exclusion at `η₃ = 11000000`, the non-optimality at `k = 1` (`η > 4` vs the exact `8`), and the two halving conventions |
| `sharp12.py` | 11 | sharpness of Theorem H at `k = 3`: the disjoint-block construction, the product form (13) with every `Σ` checked against `HΣ + ΣH = Q̃`, the seven exact alternating evaluations, the tight `2k = 6` sign pattern, the connected weighted-graph realization with its eigenvectors verified exactly, and what sharpness does not mean |
| `components11.py` | 12 | Theorem H: `B·det(C∘Q̃)` polynomial of degree `≤ 2k`, the numerator identity, `A(0) = −4^k(det Q)(tr L)`, the nonpositive tail, the sign-variation and component counts (7 instances, `n = 2…5`, `k = 0…5`, with and without cycle terms); plus the round-4 corrections and the `k = 3` linear reduction |
| `multipair10.py` | 11 | the two-pair counterexample: `Q̃ ≻ 0`, the vanishing cycle term, the ratio against independent Lyapunov solves, the three exact evaluations, disconnectedness, the component count, the effect of zeroing either correlation, the connected weighted-triangle realization, the corrected `7.5×` diagnosis, and the interval/unimodality distinction |
| `singlepair9.py` | 11 | the single-correlated-pair theorem: the exact ratio (9) against independent Lyapunov solves at `n = 2,3,4`, `Δ = 0`, the equivalence with `η > T`, the normal form (★) with exact coefficient reconstruction, uniqueness of the minimizer with `deg = rank L + 1`, the floor (11), both repository models as instances, the corrected `det C` asymptotic, and the interval test outside the covered class |
| `review8.py` | 14 | the reviewer corrections: the `κ = 1` derivative, `Θ(κ^{-rank L})`, the Cauchy formula for `det C`, the Oppenheim–Schur refinement and its measured overshoot, the centre-node closed form and its cubic |

Discriminating controls in `controls6.py`: `κ = 0`; `r = 1`; `r` below/at/above `3+2√2`;
`[H,Q] = 0`; a self-adjoint off-diagonal witness; repeated damping rates; **identical `spec(Q)`
with different orientation**; and `H` with a zero eigenvalue as an excluded-domain control
(the Sylvester operator is singular, so the whole construction needs `H > 0`).

## Not proved

* **Theorem H's Steps 1–3 and 5 are not formalized.** Lean has the combinatorial step (sign
  variations and the root count); the construction of the polynomial `A` from the matrix data, and
  the final "two boundary roots per component" step, remain analytic.
* **Sharpness of Theorem H is attained at `k = 1, 2, 3, 4, 5`** — the last two robustly, over
  parameter boxes (§10). Attainment for arbitrary `k` is open.
* **The box criterion's bounds are not formalized.** Lean has the envelope lemma
  (`blockRatio_mem_box`) and the monotonicity it rests on; the eleven numerical box bounds and the
  resulting component counts are exact rational arithmetic only.
* **Theorem J covers only matching patterns, and the hypothesis enters twice.** (a) The
  coefficientwise domination `N ⪯ (det Q)ρ_∞B` is obtained by multiplying per-block inequalities,
  so it needs disjointness; it is not established for a general pattern. (b) The single-window term
  `1 + 8(tr L)/s_*` relies on the product representation `G = ∏_j(1 + w_j u_j)` with nonnegative
  weights and `u_j ∈ [0,1]`, which a general network is not known to admit — the formalized
  saturation inequality holds for any such product but does not establish the representation.
  For general patterns only the disjunctive band constraint (17) is available.
* **`ρ_∞` and `ρ` are distinct.** Theorem J bounds `ρ_∞ = det(C_∞ ∘ Q̃)/det Q̃`; Hadamard gives
  `ρ_∞ ≤ ρ = ∏Q̃_ii/det Q̃`, so the `ρ` form is weaker. They coincide for the `(0, a_j)` rate pairs
  used in §8–§10 (where `c_{pq} → 0`) but not for an arbitrary pattern, nor for matching pairs with
  both rates positive.
* **Theorem J's two ingredients are not formalized.** Lean has the saturation envelope
  (`prod_one_add_mul_le`) behind the single-window term; the coefficientwise domination and the
  monotonicity of `q_m` (Newton's inequalities on `B`) are exact-arithmetic checks only.
* **Theorem I is an exclusion test, not a criterion, and it is not optimal.** It gives `η > 4` for
  a single pair where the exact threshold is `8`. It says nothing about `1 ≤ c < k`, and nothing
  sufficient. Its `k = 3` consequence is specific to that fixed construction and is not a
  universal cost across spectra and patterns.
* **Whether a *star* pattern can attain the ceiling is still open.** The `k = 3` witness uses
  disjoint blocks, so the star feasibility question (C11.12) is untouched by it.
* **The single-pair theorem does not extend to general `Q̃`, and this is now settled
  negatively.** With two correlated pairs at different damping scales the expansion set can be
  **disconnected** — §7 of [DERIVATION.md](DERIVATION.md) gives an exact three-mode witness on a
  connected weighted triangle, with the determinant cycle term identically zero. So Theorem F's
  hypothesis is not removable. What restrictions short of "one pair" preserve one interval is open.
* The end-node three-mode model (all three off-diagonals nonzero) happens to have a single
  expansion interval at every tested noise level (C9.9), but that is **evidence about that model
  only**, not a general fact — the witness above shows the general claim is false.
* **Existence of the minimizer is not formalized** (only uniqueness and the interval property);
  `T → ∞` at both ends is argued analytically.
* **No closed form for the *end-node* three-mode critical `r`.** For centre-node noise the
  threshold *is* in closed form: `r_*` is determined by the positive root of `27κ³ + 36κ² - 8 = 0`
  (`κ_* = 0.4120226592…`, `r_* = 8.2780690232…`). For end-node noise all three off-diagonals
  survive and only certified rational brackets are available; a resultant computation would settle
  it but needs bivariate polynomial arithmetic that is not implemented here.
* **No general many-mode threshold.** Theorem B gives the shape (`ratio'(0) = -tr L`, decay
  `Θ(κ^{-2})`, bounded window) for all `n`, but the critical noise ratio is not characterized
  for `n ≥ 3`. Theorem C shows no single constant can play that role, so a general statement
  must be a condition on `(Q, L)` jointly, presumably through `ρ(Q,L)`.
* **`det H_κ < ρ(Q,L)` is necessary, not sufficient**, for expansion. All witnesses respect it
  (C7.5/C7.6) but it does not decide the boundary.
* **The general sufficient condition `1 + det C (ρ-1) > det H_κ` is far from sharp for `n ≥ 3`**:
  it first becomes satisfiable at `r ≈ 62.26` (centre) and `r ≈ 13.12` (end) against true
  thresholds `8.2781` and `10.7202` — overshoot `7.52×` and `1.22×` (C8.6). It also degenerates
  entirely (`det C = 0`) when two damping rates coincide.
* **Nothing here concerns the inertial (second-order) model.** `paper/` describes a different
  system; no first-order claim has been inserted into it.

## Corrections recorded during this work

`det Σ_0 = det(Q/2) = det Q/2ⁿ`: the normalizing power is the **dimension**. An early version of
`controls6.py` carried the `n = 3` factor `8` into the two-mode controls, which inflated the
reported two-mode maxima by a factor of 2 and produced five spurious failures. Fixed by
`ratio_of`, which reads `n` off the matrix. `verify.py` always used `/4` for `n = 2` and was
unaffected, as was the agreement with `volume0 r = r²/4`.

**`κ = 1` is not volume-maximizing.** An earlier draft of this documentation and of the Lean
theorem name (`one_is_optimal`) asserted that "`κ = 1` is optimal independently of `r`". That is
wrong as stated: `κ = 1` minimizes the *coupling cost*, hence the anisotropy required for any
improvement, but above the threshold the volume is still strictly increasing at `κ = 1`
(derivative `((r-1/r)² - 32)/144 > 0`). The theorem is now `unit_coupling_suffices` and the
counter-reading is pinned down in Lean by `volume_one_not_maximal`. Raised in review.

**Per-pair contributions are not additive, and star patterns do not force one interval.** An
earlier draft of the open question in `REPORT.md` claimed each correlated pair contributes an
additive term, and proposed star patterns as a candidate restriction. Disjoint correlated blocks
multiply rather than add (C11.6), and the counterexample is itself a star (C11.7). Raised in
review.

**The saturation scale of a pair is `2/s`, not `1/Δ`.** From
`1 − c_pq² = (Δ²/s²)(κ/(κ+2/s))²`: the rate *sum* sets the scale, the ratio `Δ/s` the amplitude
(C11.8). Raised in review.

**The reported `r = 9` peak was wrong.** An earlier draft gave `1.8037` near `κ = 0.69`; that came
from misreading the grid argmax `69/50` as `0.69`. The maximum is `2.0322` near `κ = 1.37`, and
`R(3/2) = 73/36 = 2.0278` already exceeds the reported value. Raised in review.

**"The ratio is never unimodal" was too broad.** With `[H,Q] = 0` the ratio is `1/det H_κ`, which
is monotone decreasing. The initial-dip argument applies when expansion occurs (C11.10). Raised in
review.

**The `7.5×` overshoot is not caused by the determinant cycle term.** An earlier draft of
`REPORT.md` conjectured that, and used it to predict where a counterexample would live. It is
wrong twice over: the centre-node model is itself single-pair, so its cycle term already vanishes;
and the counterexample that did arrive also has a vanishing cycle term. The real cause of the
overshoot is that `det C` multiplies the rate-difference factors of *all* pairs, including those
carrying no noise correlation (`Θ(κ⁶)` against the exact `Θ(κ²)`). Raised in review.

**"One expansion interval" is not "unimodality".** An earlier draft stated these as equivalent
when posing the general question. They are not: `ratio′(0) = −tr L < 0`, so the ratio always starts
by decreasing and is never unimodal, while the interval claim concerns only `{R > 1}`. Raised in
review.

**`det C ~ (9/16)κ⁶`, not `κ⁶/64`.** An earlier draft dropped the factor `36` in
`det C = 36κ⁶/[(2+κ)(2+3κ)(2+4κ)]²` when taking `κ → 0`. The denominator tends to `64` but the
numerator keeps its `36`. The sixth-order suppression — and hence the overshoot table — is
unaffected. Raised in review.

**The large-coupling exponent is `rank L`, not `2`.** An earlier draft stated `Θ(κ^{-2})` as if
general; it is correct only for the three-node connected case. The exponent is `rank L`
(`n - 1` for a connected `n`-node graph), verified at ranks 1, 2 and 3 in C8.2. Raised in review.
