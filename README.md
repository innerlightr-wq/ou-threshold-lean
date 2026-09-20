# OU Threshold — Lean 4 Formal Verification Companion

A machine-checked formalization, in Lean 4 with mathlib, of the central algebraic threshold theorem from:

> Elias De Jesús (2026). *Heterogeneity-Driven Expansion and Synchronization Collapse in Coupled Ornstein–Uhlenbeck Systems.*

The paper studies two diffusively coupled Ornstein–Uhlenbeck processes and shows that, in the equal-relaxation normalization, the stationary covariance-volume functional $begin:math:text$A\(\\kappa\,r\)$end:math:text$ can exceed its uncoupled value $begin:math:text$A\(0\,r\)$end:math:text$ at some positive coupling strength if and only if the noise-heterogeneity ratio $begin:math:text$r$end:math:text$ exceeds the exact threshold

$begin:math:display$
r\^\\\* \= 3 \+ 2\\sqrt\{2\}\.
$end:math:display$

This repository formalizes and machine-checks that threshold statement as a result in exact real algebra.

It also machine-checks, at the same level of exact real algebra, the paper's second threshold `r_D* = 2 + √3` for the conditional residual variance, the reciprocal structure shared by the two thresholds, and a cross-threshold identity for the eigenvalues of the stationary covariance matrix. See [Stationary Covariance and the Residual-Variance Threshold](#stationary-covariance-and-the-residual-variance-threshold), [Reciprocal Threshold Structure](#reciprocal-threshold-structure), and [Cross-Threshold Covariance Identity](#cross-threshold-covariance-identity).

> **Scope:** This is a formal verification companion, not a formalization of the paper's complete stochastic-process content. See [Scope of the Formalization](#scope-of-the-formalization).

---

## Central Result

For $begin:math:text$r \\ge 1$end:math:text$,

$begin:math:display$
\\boxed\{
\\left\(\\exists\\\,\\kappa\>0\,\\\;
A\(\\kappa\,r\)\>A\(0\,r\)\\right\)
\\iff
r\>3\+2\\sqrt\{2\}
\}
$end:math:display$

This is proved in Lean as:

```lean
exists_volume_improvement_iff_threshold
```

The formal development contains no `sorry`, `admit`, or explicit custom `axiom` placeholders.

---

## Paper

**Elias De Jesús. (2026).**  
*Heterogeneity-Driven Expansion and Synchronization Collapse in Coupled Ornstein–Uhlenbeck Systems.*  
Zenodo.

- **Current version DOI:** https://doi.org/10.5281/zenodo.22059089
- **All-versions DOI:** https://doi.org/10.5281/zenodo.22059088

The all-versions DOI resolves to the latest deposited version. The version-specific DOI identifies the current deposited version associated with this formalization.

---

## Main Formal Result

In the equal-relaxation normalization

$begin:math:display$
a\_1\=a\_2\=1\,\\qquad \\sigma\_1\=1\,\\qquad \\sigma\_2\=r\,
$end:math:display$

define

$begin:math:display$
A\(\\kappa\,r\)
\=
\\frac\{
\\kappa\^2r\^4
\+2\\kappa\^2r\^2
\+\\kappa\^2
\+8\\kappa r\^2
\+4r\^2
\}\{
16\(\\kappa\+1\)\^2\(2\\kappa\+1\)
\}\,
$end:math:display$

with

$begin:math:display$
A\(0\,r\)\=\\frac\{r\^2\}\{4\}\.
$end:math:display$

Then, for every $begin:math:text$r\\ge1$end:math:text$, some positive coupling strictly increases the covariance-volume functional over its uncoupled value if and only if

$begin:math:display$
r\>3\+2\\sqrt2\.
$end:math:display$

The corresponding Lean theorem in `OUCorridor/MainTheorem.lean` is:

```lean
theorem exists_volume_improvement_iff_threshold {r : ℝ} (hr : 1 ≤ r) :
    (∃ κ : ℝ, 0 < κ ∧ volume κ r > volume0 r) ↔ r > threshold
```

where `volume`, `volume0`, and

```lean
threshold := 3 + 2 * Real.sqrt 2
```

are defined in `OUCorridor/Threshold.lean`.

---

## What Is Formally Verified

The central result is supported by the following machine-checked theorem chain:

1. **`volume_zero`**  
   Verifies
   $begin:math:display$
   A\(0\,r\)\=\\frac\{r\^2\}\{4\}\.
   $end:math:display$

2. **`volume_sub_volume0`**  
   Establishes the exact identity expressing
   $begin:math:display$
   A\(\\kappa\,r\)\-A\(0\,r\)
   $end:math:display$
   as $begin:math:text$\\kappa B\(\\kappa\,r\)$end:math:text$ divided by the relevant denominator.

3. **`denominator_pos`**  
   Proves
   $begin:math:display$
   16\(\\kappa\+1\)\^2\(2\\kappa\+1\)\>0
   $end:math:display$
   for $begin:math:text$\\kappa\\ge0$end:math:text$.

4. **`volume_gt_iff_bracket_gt`**  
   For $begin:math:text$\\kappa\>0$end:math:text$,
   $begin:math:display$
   A\(\\kappa\,r\)\>A\(0\,r\)
   \\iff
   B\(\\kappa\,r\)\>0\.
   $end:math:display$

5. **`discr_factor`**  
   Proves the exact discriminant factorization
   $begin:math:display$
   \\operatorname\{discr\}\(r\)
   \=
   \(r\^2\-1\)\^2\(r\^4\-34r\^2\+1\)\.
   $end:math:display$

6. **Exact threshold identities**  
   `threshold_sq`, `threshold_quartic`, `conjugate_sq`, and `threshold_conjugate_mul` establish exact radical identities associated with
   $begin:math:display$
   r\^\\\*\=3\+2\\sqrt2\.
   $end:math:display$

7. **`quartic_gt_iff_gt_threshold`**  
   For $begin:math:text$r\\ge1$end:math:text$,
   $begin:math:display$
   r\^4\-34r\^2\+1\>0
   \\iff
   r\>3\+2\\sqrt2\.
   $end:math:display$

8. **`discr_sos`**  
   Establishes a sum-of-squares certificate connecting the discriminant to $begin:math:text$B\(\\kappa\,r\)$end:math:text$.

9. **`exists_bracket_pos_iff_threshold`**  
   Proves
   $begin:math:display$
   \\left\(\\exists\\\,\\kappa\>0\,\\ B\(\\kappa\,r\)\>0\\right\)
   \\iff
   r\>3\+2\\sqrt2\.
   $end:math:display$
   The reverse direction has the explicit witness $begin:math:text$\\kappa\=1$end:math:text$.

10. **`exists_volume_improvement_iff_threshold`**  
    Combines the preceding results to establish the central covariance-volume threshold theorem.

---

## Stationary Covariance and the Residual-Variance Threshold

### The covariance matrix (`OUCorridor/Covariance.lean`)

In the equal-relaxation normalization, the drift matrix, noise covariance, and the explicit covariance matrix of paper eqs. (7) and (36)–(38) are defined as

```text
M = [[-(1+κ), κ], [κ, -(1+κ)]]        Q = diag(1, r²)

Σxx = (κ²r² + κ² + 4κ + 2)   / (4(2κ² + 3κ + 1))
Σyy = (κ²r² + κ² + 4κr² + 2r²) / (4(2κ² + 3κ + 1))
Σxy = κ(r² + 1) / (4(2κ + 1))
```

For every `κ ≥ 0` Lean proves:

| theorem | statement |
|---|---|
| `cov_lyapunov` | `M Σ + Σ Mᵀ = -Q` (paper eq. (8)) |
| `lyapunov_unique` | every `2 × 2` matrix `S` with `M S + S Mᵀ = -Q` equals `Σ` |
| `det_cov` | `det Σ = A(κ, r)`, i.e. `(cov κ r).det = volume κ r` |

So the closed form `volume`, which `OUCorridor/Threshold.lean` still takes as a definition (unchanged), is now proved to be the determinant of the unique solution of the algebraic Lyapunov equation. The step from the stochastic differential equation to that Lyapunov equation (paper Proposition 1) is **not** formalized. See [Scope](#scope-of-the-formalization).

### The residual-variance threshold (`OUCorridor/ResidualThreshold.lean`)

The conditional residual variance of paper eq. (14),

```text
D(κ, r) = Var(X | Y) = Σxx - Σxy² / Σyy ,
```

is defined from the entries of `Σ` above (`residualVariance`). It is not a separately pasted closed form. Lean proves paper Proposition 5:

```lean
theorem exists_residual_improvement_iff_threshold {r : ℝ} (hr : 1 ≤ r) :
    (∃ κ : ℝ, 0 < κ ∧ residualVariance κ r > residualVariance 0 r) ↔ r > residualThreshold
```

where `residualThreshold := 2 + Real.sqrt 3`. The chain mirrors the volume theorem:

1. `residualVariance_zero`: `D(0, r) = 1/2`.
2. `residualVariance_sub_uncoupled`: `D(κ) - D(0) = κ B_D(κ, r) / (4(κ+1)(κ²r² + κ² + 4κr² + 2r²))` (paper eq. (27)), with `B_D(κ, r) = -2(r²+1)κ² + (r⁴-8r²-1)κ - 4r²` (paper eq. (28)).
3. `residualVariance_gt_iff_bracket_pos`: for `κ > 0`, `D(κ) > D(0) ⟺ B_D(κ, r) > 0`.
4. `residualDiscr_factor`: the discriminant of `B_D` is `(r²-1)²(r²-4r+1)(r²+4r+1)` (paper eq. (29)).
5. `residualDiscr_sos`: a completed-square certificate (forward direction).
6. `residualQuadratic_pos_iff`: for `r ≥ 1`, `r² - 4r + 1 > 0 ⟺ r > 2 + √3`.
7. `exists_residualBracket_pos_iff_threshold`: the reverse direction uses the explicit witness `κ₀ = (r⁴ - 8r² - 1) / (4(r² + 1))`, where `B_D(κ₀) = Δ_D / (8(r² + 1)) > 0`.

`residualVariance_eq_det_div` also records the second form `D = det Σ / Σyy` of paper eq. (14).

---

## Reciprocal Threshold Structure

Write `s(r) = r + 1/r` (`reciprocalInvariant`). This quantity is invariant under `r ↦ 1/r`, the relabelling of the two components.

The volume-threshold quartic factors over the rationals (`quartic_rational_factor`):

```text
r⁴ - 34r² + 1 = (r² - 6r + 1)(r² + 6r + 1)
```

`threshold_quadratic` derives `r_A*² - 6r_A* + 1 = 0` from the existing `threshold_quartic`, using the fact that the second factor is positive. It is not a second radical computation. Both thresholds are therefore roots of reciprocal quadratics:

| threshold | quadratic | `s(r*)` | Lean |
|---|---|---|---|
| `r_A* = 3 + 2√2` (volume, `threshold`) | `r² - 6r + 1 = 0` | `6` | `threshold_quadratic`, `threshold_reciprocalInvariant` |
| `r_D* = 2 + √3` (residual, `residualThreshold`) | `r² - 4r + 1 = 0` | `4` | `residualThreshold_quadratic`, `residualThreshold_reciprocalInvariant` |

Also proved: `residualThreshold_sq` (`(r_D*)² = 7 + 4√3`) and `residualThreshold_sq_reciprocalInvariant` (`s((r_D*)²) = 4² - 2 = 14`, via `reciprocalInvariant_sq`: `s(x²) = s(x)² - 2`).

The theorems state these equalities only. Describing `s` as a common "master coordinate" for the two thresholds is an interpretive reading, not a formal claim.

---

## Cross-Threshold Covariance Identity

The reciprocal-threshold analysis exposes one more exact identity. The present extension records and machine-checks a cross-threshold identity that is not stated in the associated deposited manuscript (Zenodo version [10.5281/zenodo.22059089](https://doi.org/10.5281/zenodo.22059089)). The manuscript states both thresholds and their ordering `2 + √3 < 3 + 2√2`, but no relation between them and no eigenvalue statement for `Σ`.

**The volume-critical merger.** At `r = r_A*` the volume bracket is a perfect square, `B(κ, r_A*) = -8 r_A*² (κ - 1)²` (`bracket_threshold`). The two crossings `κ₁ κ₂ = 1` therefore merge at `κ = 1`: for `κ > 0`, `A(κ, r_A*) = A(0, r_A*) ⟺ κ = 1` (`volume_threshold_eq_iff`), and `A(κ, r_A*) ≤ A(0, r_A*)` for all `κ ≥ 0` (`volume_threshold_le`).

**The merger invariant.** At `κ = 1` the Lyapunov solution has `tr Σ = (1 + r²)/3` and `det Σ = (r⁴ + 14r² + 1)/192`. For every `r > 0` (`trace_sq_div_det_merger`):

```text
(tr Σ)² / det Σ = C(s(r)),        C(s) = (64/3) · s² / (s² + 12).
```

Here `tr` is the matrix trace and `det` the determinant. The denominator is `det Σ = A`, not `√det Σ`.

**Eigenvalues.** For the eigenvalues `0 < μ₂ < μ₁` of a `2 × 2` matrix, `(tr)² / det = q + 1/q + 2` with `q = μ₁/μ₂` (`eigenvalues_sum_prod`, `sum_sq_div_prod`).

**Main theorem.** Eigenvalues enter only as roots of `det(Σ - μ·1) = 0`:

```lean
theorem cross_threshold_eigenvalue_ratio {μ₁ μ₂ : ℝ}
    (h₁ : (cov 1 threshold - μ₁ • 1).det = 0)
    (h₂ : (cov 1 threshold - μ₂ • 1).det = 0)
    (hlt : μ₂ < μ₁) :
    μ₁ / μ₂ = residualThreshold ^ 2
```

In words, at the volume-critical merger `(κ, r) = (1, 3 + 2√2)` the spectral ratio of the stationary covariance is

```text
λ_max / λ_min = (2 + √3)² = 7 + 4√3 .
```

The proof does not substitute radical values into both sides. It passes through the structural chain

```text
s(r_A*) = 6                                   threshold_reciprocalInvariant
C(6) = (64/3) · 36/48 = 16 = 4²               mergerInvariant_six
q + 1/q + 2 = 16   ⇒   q + 1/q = 14           trace_sq_div_det_merger, sum_sq_div_prod
s(r_D*) = 4   ⇒   s((r_D*)²) = 4² - 2 = 14    residualThreshold_sq_reciprocalInvariant
q > 1, (r_D*)² > 1, s injective on [1, ∞)  ⇒  q = (r_D*)²     reciprocalInvariant_injOn
```

`threshold` and `residualThreshold` keep their original, independent definitions (`3 + 2√2` and `2 + √3`). The two thresholds meet only through the numerical equality `C(6) = 16 = 4²`. The hypothesis `q > 1` excludes the reciprocal root `1/(r_D*)² = 7 - 4√3`.

Companion results:

- `cross_threshold_spectral_ratio`: the algebraic form, `1 < q → s(q) + 2 = C(s(r_A*)) → q = (r_D*)²`.
- `cross_threshold_ratio_unique`: `1 < q → q + 1/q = 14 → q = (r_D*)²`.
- `cross_threshold_eigenvalue_ratio_radical`: `μ₁ / μ₂ = 7 + 4√3`.
- `cov_merger_eigenvalues_exist`: non-vacuity. `Σ` at the merger has two distinct real eigenvalues.
- `cross_threshold_rapidity`: `½ log(μ₁/μ₂) = log r_D* = arcosh 2`.

**Limits of the identity.**

- It is specific to the equal-relaxation normalized model (`a₁ = a₂ = 1`, `σ₁ = 1`, `σ₂ = r`).
- It is not preserved when equal relaxation is broken. A floating-point check (not part of the Lean development) used `a₁ = 1`, `a₂ = 1.05`, thresholds defined as in the paper (the least `r` with `sup_{κ>0} F(κ) > F(0)`), and the tangency coupling at the volume threshold. It gives `λ_max/λ_min ≈ 13.566`, against `(r_D*)² ≈ 14.222` for that model.
- No universality is claimed, and no multi-sector or tensor generalization is formalized here.

---

## Two-Mode Active-Subspace Reduction

This section records a general algebraic theorem that **contains** the volume threshold above as
a special case. It is a statement about a two-dimensional block of a linear system; no graph
appears in its hypotheses.

### Setting

Heterogeneous forcing is taken to be a **rank-one deformation** of an isotropic baseline,

```text
Q(τ) = q_b ( I + (τ - 1) e eᵀ ) ,    |e| = 1 ,  τ > 0 ,
```

so `Q` has eigenvalue `q_b τ` along `e` and `q_b` on `e^⊥`. Here **`e` is the excitation
direction** (a unit vector selecting where the heterogeneity points — not Euler's number), and
`τ` is the ratio of the deformed forcing eigenvalue to the baseline one.

Suppose `e` lies in a two-dimensional **invariant plane of the drift**, with relaxation rates
`D₁, D₂ > 0`, and write `e = c u + s v` in the plane's eigenbasis, `c² + s² = 1`. The quantity
`c² s²` (`mixing`) measures how much the excitation occupies *both* active modes.

### What is proved (`OUCorridor/ActivePlane.lean`)

| theorem | statement | class |
|---|---|---|
| `activeCov_lyapunov`, `activeCov_unique` | the explicit `Σ` is the unique solution of `M Σ + Σ Mᵀ = -Q` on the plane | **NEW FORMAL RESULT** (standard mathematics) |
| `det_activeForcing` | `det Q = q_b² τ` | STANDARD MATHEMATICS |
| `activeForcing_self_dual` | `Q_e(τ) = τ • Q_{e^⊥}(1/τ)` — the source of the reciprocal structure | **NEW FORMAL RESULT** |
| `det_activeCov_palindromic` | `4 D₁ D₂ det Σ = q_b² (A τ² + (1-2A) τ + A)`, `A = c²s²ν²`, `ν = (D₁-D₂)/(D₁+D₂)` | **NEW FORMAL RESULT** |
| `normalizedActiveDet_eq` | dividing by `τ`: `= 1 + A (w - 2)` with `w = τ + 1/τ` | **NEW FORMAL RESULT** |
| `two_le_reciprocalExcitation`, `reciprocalExcitation_eq_two_iff` | `w ≥ 2`, equality iff `τ = 1` | STANDARD MATHEMATICS (AM–GM) |
| `rateContrast_sq_lt_one`, `mixing_le_quarter`, `mixing_eq_quarter_iff` | `ν² < 1`; `c²s² ≤ 1/4` with equality iff `c² = s² = 1/2` | STANDARD MATHEMATICS |
| `activeCoeff_eq_zero_iff` | the reciprocal contribution vanishes **iff** `c = 0`, `s = 0`, or `D₁ = D₂` | **NEW FORMAL RESULT** |
| `volumeRatio_gt_one_iff` | `Φ(1 + C(w-2)) > 1 ↔ w > 2 + (1-Φ)/(ΦC)` for `Φ, C > 0` | STANDARD MATHEMATICS |

The order matters and is respected in the file: the **palindromic identity is proved first**, and
the reciprocal coordinate `w = τ + 1/τ` is introduced only afterwards, because `w` is nothing but
the classical substitution that a palindromic quadratic admits.

### Why `t + 1/t` appears

Two exact facts: the active forcing block has determinant exactly `q_b² τ`, and its off-diagonal
entry is proportional to `τ - 1`. Hence `det Σ` is a *quadratic in `τ` whose leading and constant
coefficients coincide*, and `(τ-1)²/τ = w - 2`. Equivalently — and this is the conceptual
statement — the forcing family is self-dual under `(τ, e) ↦ (1/τ, e^⊥)`, which is just
`e eᵀ + e^⊥ e^⊥ᵀ = I`.

### Graph corollaries

| theorem | content | class |
|---|---|---|
| `volume_div_volume0_eq` | the repository's own `volume/volume0` **is** the active-plane formula, with `D₁ = 1`, `D₂ = 1 + 2κ`, `c² = s² = 1/2` and `τ = r²` | **GRAPH COROLLARY** |
| `reciprocalExcitation_sq` | `w(r²) = (r + 1/r)² - 2` — the variance/amplitude bridge | **NEW FORMAL RESULT** |
| `reciprocalExcitation_threshold_sq` | at `r_A* = 3 + 2√2`, `w = 34` | **GRAPH COROLLARY** |
| `p3_thresholdCurve_eq`, `p3_threshold_min`, `p3_threshold_attained` | the P3 centre-node curve is `(27κ³+72κ²+64κ+16)/(2κ)`, minimized by `35 + 15√5` at `κ = (√5-1)/3` | **GRAPH COROLLARY** |
| `k3_thresholdCurve_eq`, `k3_threshold_min`, `k3_threshold_attained` | the K3 one-node curve is `(81κ³+162κ²+112κ+24)/(2κ)`, minimized by `247/2` at `κ = 1/3` | **GRAPH COROLLARY** |

Both graph curves are **derived** from `thresholdCurve` applied to the relevant `Φ` and
`C = c²s²ν²`; no constant is fitted. **Parameterization warning:** `τ` is a noise *variance*
ratio, so for the two-node model `τ = r²` and `w = τ + 1/τ = (r + 1/r)² - 2`. The amplitude
coordinate `r + 1/r = 6` and the variance coordinate `w = 34` describe the same threshold; they
must not be conflated.

### What this does not say

The theorem applies when the heterogeneity excites the common mode **plus exactly one** further
drift eigendirection. It does **not** say that arbitrary high-dimensional forcing reduces to one
scalar: if the excitation reaches more independent modes, the active block is no longer `2 × 2`,
the determinant is no longer a palindromic quadratic, and no reciprocal coordinate follows.
The useful way to say this is that the **effective active subspace dimension** may be smaller
than the ambient dimension — an interpretation, not a formal statement. **INTERPRETATION**

---

## Scale-Free Spectral Shape

`OUCorridor/SpectralShape.lean` records why a single scalar sufficed in the cross-threshold
argument, and why that is special to `2 × 2`.

* `J2_eq_reciprocalInvariant` — `J₂ = (tr Σ)²/det Σ = q + 1/q + 2` for `q = μ₁/μ₂`.
* `eigen_ratio_unique_of_J2` — on the branch `q ≥ 1`, `J₂` **determines** the eigenvalue ratio.
  This is the general form of the uniqueness step used by `cross_threshold_eigenvalue_ratio`.
* `exists_same_trace_det_different_ratio` — for three eigenvalues it fails: `(1, 8, 12)` and
  `(2, 3, 16)` have the same trace `21` and the same determinant `96`, hence the same value of
  every scale-free trace/determinant invariant, but extreme ratios `12` and `8`.

Both are **STANDARD MATHEMATICS** and are recorded, not claimed: `J_n` is (up to a constant) the
reciprocal of Mauchly's (1940) sphericity statistic, and the `n ≥ 3` failure is the elementary
fact that a spectrum is determined by all `n` elementary symmetric functions, of which the trace
and determinant are all of them only when `n = 2`.

The contrast between complete one-scalar reconstruction in two dimensions and higher-dimensional
non-identifiability is consistent with the invariant-theoretic reconstruction perspective of
De Jesús (2026), [10.5281/zenodo.19632381](https://doi.org/10.5281/zenodo.19632381). The results
here are derived independently from the covariance algebra; that note is cited for the
reconstruction analogy only, and not as a source for OU covariance dynamics, Lyapunov equations,
graph formulas, or the rank-one forcing theorem.

---

## Scope of the Formalization

This repository does **not** claim to formalize the paper in full.

The following are not currently formalized in the Lean development:

- stochastic differential equation semantics for the underlying Ornstein–Uhlenbeck processes;
- existence or uniqueness of the stationary Gaussian distribution;
- the fact that the stationary covariance of the process satisfies the continuous Lyapunov equation (paper Proposition 1). What *is* formalized is the algebraic part: the explicit matrix of paper eqs. (36)–(38) is the unique solution of `M Σ + Σ Mᵀ = -Q` for `κ ≥ 0`, and its determinant is `A(κ, r)`;
- the complete stochastic OU model;
- the identification of `residualVariance` with the conditional variance `Var(X | Y)` of the stationary process. The residual-variance threshold criterion itself (paper Proposition 5, `∃ κ > 0, D(κ) > D(0) ⟺ r > 2 + √3` for `r ≥ 1`) **is** formalized, with `D` defined from the Lyapunov solution, at the same algebraic level as the volume threshold;
- the unequal-relaxation covariance formulas (paper eqs. (9)–(13)) and the weak-coupling result `A′(0) < 0` (paper Proposition 3);
- the mutual-information/coherence monotonicity result;
- strong-coupling asymptotics;
- numerical experiments, plots, or tables.

The active-plane development of `OUCorridor/ActivePlane.lean` adds algebraic Lyapunov and
determinant statements about an explicit `2 × 2` block; it adds no stochastic-process content,
and in particular it does not formalize invariant subspaces of general `n × n` drifts — the
active plane enters as explicit rates `D₁, D₂`, with the basis reduction documented rather than
formalized.

In particular, `volume` remains a closed-form definition in `OUCorridor/Threshold.lean`, and the original theorem chain is unchanged. The added `det_cov` proves that this closed form equals `det Σ` for the Lyapunov solution `Σ`. The link from the stochastic system to that Lyapunov equation is still not formalized.

What is formally verified is exact real algebra: the threshold theorems for the scalar functions defined in `OUCorridor/Threshold.lean` and `OUCorridor/ResidualThreshold.lean`, the algebraic Lyapunov facts in `OUCorridor/Covariance.lean`, and the reciprocal and cross-threshold identities in `OUCorridor/CrossThreshold.lean`, including

```lean
exists_volume_improvement_iff_threshold
exists_residual_improvement_iff_threshold
cross_threshold_eigenvalue_ratio
```

---

## Repository Structure

```text
ou-threshold-lean/
├── OUCorridor/
│   ├── Basic.lean
│   ├── Threshold.lean
│   ├── MainTheorem.lean
│   ├── Covariance.lean
│   ├── ResidualThreshold.lean
│   ├── CrossThreshold.lean
│   ├── ActivePlane.lean
│   └── SpectralShape.lean
├── OUCorridor.lean
├── verified/
│   ├── Threshold.lean
│   ├── MainTheorem.lean
│   ├── verification-log.txt
│   ├── SHA256SUMS.txt
│   ├── lean-toolchain
│   ├── lake-manifest.json
│   ├── lakefile.toml
│   └── cross-threshold-2026-09/
│       ├── README.md
│       ├── OUCorridor.lean
│       ├── OUCorridor/  (all six library modules)
│       ├── print-axioms.lean
│       ├── verification-log.txt
│       ├── SHA256SUMS.txt
│       ├── lean-toolchain
│       ├── lake-manifest.json
│       └── lakefile.toml
├── lakefile.toml
├── lake-manifest.json
├── lean-toolchain
└── README.md
```

### `OUCorridor/Threshold.lean`

Contains the definitions and supporting real-algebra results, including the volume functional, bracket polynomial, discriminant factorization, radical threshold identities, and quartic sign theorem.

### `OUCorridor/MainTheorem.lean`

Contains the sum-of-squares certificate, bracket-existence theorem, and the central theorem:

```lean
exists_volume_improvement_iff_threshold
```

### `OUCorridor/Covariance.lean`

Defines the equal-relaxation drift matrix, noise covariance, and explicit covariance matrix `cov κ r` (paper eqs. (36)–(38)). Proves that `cov κ r` is the unique solution of the algebraic Lyapunov equation for `κ ≥ 0` (`cov_lyapunov`, `lyapunov_unique`) and that `det (cov κ r) = volume κ r` (`det_cov`).

### `OUCorridor/ResidualThreshold.lean`

Defines the residual variance `D = Σxx - Σxy²/Σyy` and `residualThreshold := 2 + √3`. Proves the residual-variance threshold theorem `exists_residual_improvement_iff_threshold` (paper Proposition 5) and the radical identities for `2 + √3`.

### `OUCorridor/CrossThreshold.lean`

Defines the reciprocal invariant `s(r) = r + 1/r` and the merger invariant `C(s) = (64/3) s²/(s² + 12)`. Proves `s(r_A*) = 6`, `s(r_D*) = 4`, the rational factorization of the volume quartic, the merger of the volume crossings at `κ = 1`, `(tr Σ)²/det Σ = C(s)` at `κ = 1`, and the cross-threshold identity `cross_threshold_eigenvalue_ratio` with its companions.

### `OUCorridor/ActivePlane.lean`

The two-mode active-subspace reduction: the Lyapunov solution on a two-dimensional invariant
plane, the self-duality of the rank-one forcing family, the palindromic determinant identity, the
reciprocal coordinate and the threshold equivalence, together with the K₂, P3 and K3 corollaries.

### `OUCorridor/SpectralShape.lean`

`J₂ = (tr)²/det` determines the eigenvalue ratio of a `2 × 2` SPD matrix; an explicit pair of
positive triples shows this fails for three.

### `OUCorridor.lean`

Top-level project module importing the formalization.

### `verified/`

Frozen verification record containing copies of the checked proof sources, environment information, build log, and cryptographic fingerprints. The top-level files are the original record and are unchanged. `verified/cross-threshold-2026-09/` is a separate, later snapshot for the cross-threshold extension.

---

## Reproducing the Verification

Clone the repository:

```bash
git clone https://github.com/innerlightr-wq/ou-threshold-lean.git
cd ou-threshold-lean
```

Install or select the Lean toolchain specified by `lean-toolchain`, then obtain the pinned dependencies and build:

```bash
lake update
lake build
```

A successful verification should end with a successful Lean build.

The verification recorded with this repository produced:

```text
Build completed successfully (8710 jobs).
```

With the cross-threshold extension (three additional modules), the build recorded in `verified/cross-threshold-2026-09/` produced:

```text
Build completed successfully (8713 jobs).
```

With the active-plane extension (two further modules), the build recorded in
`verified/active-plane-2026-09/` produced:

```text
Build completed successfully (8715 jobs).
```

### Unfinished-proof audit

The repository was additionally checked with:

```bash
grep -R -n "sorry\|admit\|axiom" OUCorridor --include="*.lean"
```

The recorded audit returned no matches.

This grep is a supplementary repository-level check for those explicit tokens. It is **not** a substitute for Lean's kernel checking of the generated proof terms.

For the cross-threshold snapshot, the grep again returned no matches. In addition, `#print axioms` was run on the main theorems of all modules (`verified/cross-threshold-2026-09/print-axioms.lean`). Each depends only on the standard axioms `propext`, `Classical.choice`, and `Quot.sound`.

---

## Verified Environment

The frozen verification was performed with:

```text
Lean 4.33.1
arm64-apple-darwin24.6.0
Lean commit: 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
```

The files

```text
lean-toolchain
lake-manifest.json
```

record the toolchain and dependency state used for reproducibility.

The verification log is preserved at:

```text
verified/verification-log.txt
```

The cross-threshold snapshot was built with the same pinned toolchain and dependencies on a different platform:

```text
Lean 4.33.1
x86_64-unknown-linux-gnu
Lean commit: 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
mathlib: 0df444a360eaa60ab8c11dca51a86af692955474
```

Its log is preserved at `verified/cross-threshold-2026-09/verification-log.txt`.

---

## Frozen Verification Record

The `verified/` directory preserves the proof state associated with the recorded verification.

It contains:

- copies of `Threshold.lean` and `MainTheorem.lean`;
- the Lean/Lake environment metadata;
- the successful build log;
- SHA-256 fingerprints.

The fingerprints are recorded in:

```text
verified/SHA256SUMS.txt
```

These hashes provide an integrity reference for the exact files associated with the verification record.

The original record above is left untouched. The cross-threshold extension has its own snapshot in `verified/cross-threshold-2026-09/`. It contains copies of all six library modules and the root module, the Lean/Lake environment files, the build log (including the unfinished-proof grep and `#print axioms` output), and SHA-256 fingerprints. Its `README.md` records the base commit and the commit of the verified sources.

---

## Citation

For the research paper, please cite:

> De Jesús, Elias. (2026). *Heterogeneity-Driven Expansion and Synchronization Collapse in Coupled Ornstein–Uhlenbeck Systems*. Zenodo. https://doi.org/10.5281/zenodo.22059088

The DOI above is the all-versions Zenodo DOI and will resolve to the latest deposited version.

For work requiring the specific current paper version associated with this repository:

> De Jesús, Elias. (2026). *Heterogeneity-Driven Expansion and Synchronization Collapse in Coupled Ornstein–Uhlenbeck Systems*. Zenodo. https://doi.org/10.5281/zenodo.22059089

---

## AI Assistance and Verification

The research and conceptual development are by **Elias De Jesús**, with AI assistance used in mathematical derivation, code generation, auditing, and the Lean formalization workflow. This includes the derivation, auditing, and formalization of the residual-threshold and cross-threshold extension.

AI-generated or AI-assisted proof code is not treated as verification in itself. The formal claims represented in this repository are checked by the Lean elaborator and kernel against the definitions, theorem statements, imported libraries, and proof terms in the pinned Lean/mathlib environment.

Accordingly, the role of Lean is distinct from the role of AI assistance: AI supported the construction of the formalization, while Lean provides the machine-checking mechanism for the formal proof.
