# The normalized Lyapunov map and the OU volume threshold

Status of this document: an **analytic derivation**, not a Lean development. The subset that is
machine-checked in Lean is listed in [SCOPE.md](SCOPE.md); the exact-arithmetic verifier for
everything else is `verification/normalized-lyapunov/`.

## 1. Setup

The repository studies the symmetric Ornstein–Uhlenbeck process

    dX_t = -H X_t dt + B dW_t,        H = H* > 0,   Q = BB*,

whose stationary covariance `Σ` is the unique solution of the Lyapunov equation

    H Σ + Σ H = Q.                                                     (1)

`OUCorridor/Covariance.lean` instantiates this with the two-mode drift
`-H_κ`, `H_κ = I + κL`, `L = [[1,-1],[-1,1]]`, and `Q = diag(1, r²)`;
`volume κ r = det Σ` and `volume0 r = det Σ|_{κ=0} = r²/4`.

## 2. The normalized map

Write `S_H(X)` for the solution of (1) with right-hand side `X`, and define

    Φ_H(X) = 2 H^{1/2} S_H(X) H^{1/2}.                                 (2)

**Lemma 1 (closed form).** In an orthonormal eigenbasis of `H` with eigenvalues `a_1,…,a_n > 0`,

    S_H(X)_{ij} = X_{ij}/(a_i + a_j),       Φ_H(X)_{ij} = c_{ij} X_{ij},
    c_{ij} = 2√(a_i a_j)/(a_i + a_j) = GM(a_i,a_j)/AM(a_i,a_j).        (3)

*Proof.* Both sides of (1) are entrywise in that basis: `(HΣ + ΣH)_{ij} = (a_i + a_j)Σ_{ij}`.
Since `a_i + a_j > 0` the solution is unique and given by the first formula; conjugating by
`H^{1/2}` multiplies the `(i,j)` entry by `√(a_i a_j)`. ∎

So **`Φ_H` is the Schur (entrywise) multiplier by the geometric-over-arithmetic mean matrix `C`.**
This is the single observation the rest of the analysis rests on, and it is what makes the
structural facts available: `C` has unit diagonal and is positive semidefinite, so

**Lemma 2.** `Φ_H` is unital, trace-preserving, self-adjointness-preserving and completely
positive. It is invertible as a linear map, but `Φ_H^{-1}` is *not* positive: for `H = diag(1,4)`,
`Φ_H^{-1}([[1,1],[1,1]])` has determinant `-9/16`.

The positivity of `C` is classical: it is a mean matrix in the sense of Bhatia–Kosaki, and is in
fact infinitely divisible (`verification/.../priorart7.py`, C7.1).

**Lemma 3 (the distortion is exactly non-commutativity).** For every `X`,

    Φ_H(X) = X  ⟺  [H, X] = 0,

and for self-adjoint `X`, `Φ_H(X²) = Φ_H(X)²  ⟺  [H, X] = 0`. Quantitatively,

    tr[Φ_H(X*X) - Φ_H(X)*Φ_H(X)] = Σ_{i,j} ((a_i - a_j)/(a_i + a_j))² |X_{ij}|²,   (4)

which is sandwiched by the commutator norm:

    ‖[H,X]‖_F²/(2a_max)²  ≤  (4)  ≤  ‖[H,X]‖_F²/(2a_min)².             (5)

`Φ_H` is a spectral isometry on all of `M_n` iff `H` is a scalar multiple of `I`.

The first part is the multiplicative domain of a Schur-product channel, specialized to this
kernel: `|c_{ij}| = 1 ⟺ a_i = a_j`, so the multiplicative domain is exactly the commutant of `H`
(C7.3 checks this on 193 608 instances).

## 3. Determinants: a two-sided sandwich

Let `U` diagonalize `H` (equivalently `L`), and put `Q̃ = U*QU`. From Lemma 1,

    Σ̃ = ½ D^{-1/2} (C ∘ Q̃) D^{-1/2},   D = diag(a_i),

so `det Σ = det(C ∘ Q̃)/(2ⁿ det H)`, and since `det Σ_0 = det(Q/2) = det Q/2ⁿ`,

    det Σ_κ / det Σ_0 = det(C ∘ Q̃) / (det H_κ · det Q).                (6)

Now apply the two classical determinant bounds for a Hadamard product with a correlation matrix.
Oppenheim's inequality gives `det(C ∘ Q̃) ≥ det Q̃ · ∏ C_ii = det Q`; Hadamard's gives
`det(C ∘ Q̃) ≤ ∏ (C ∘ Q̃)_ii = ∏ Q̃_ii`. Hence:

> **Theorem A (sandwich).** For `H > 0` and `Q > 0`,
>
>     1/det H_κ   ≤   det Σ_κ / det Σ_0   ≤   ρ(Q,L) / det H_κ,
>     ρ(Q,L) = ∏_i Q̃_ii / det Q   ( ≥ 1, the Hadamard ratio of the rotated noise).
>
> The left bound is an equality iff `[H,Q] = 0`.

**Theorem A' (Oppenheim–Schur refinement).**  The source for the equality analysis states, just
after ordinary Oppenheim, the stronger Oppenheim–Schur inequality.  Applied to a unit-diagonal `C`
and `Q̃ ≻ 0` it rearranges to

    det(C ∘ Q̃)/det Q̃  ≥  1 + det C · (ρ - 1).                          (6')

For this kernel `det C` is a Cauchy determinant:

    det C = ∏_{i<j} ((a_i - a_j)/(a_i + a_j))².                          (6'')

(`C = 2 D^{1/2} K D^{1/2}` with `K_{ij} = 1/(a_i+a_j)`; the Cauchy determinant formula and
`∏_{i,j}(a_i+a_j) = 2ⁿ ∏ a_i ∏_{i<j}(a_i+a_j)²` give (6'').)

Combining (6) and (6') yields an **explicit sufficient condition for expansion, valid for all `n`**:

    1 + det C · (ρ(Q,L) - 1)  >  det H_κ.                                (6''')

For `n = 2` the inequality (6') is an *identity*, so (6''') is exactly the two-mode threshold.
For `n ≥ 3` it is strictly weaker — see §5. Its limitations are structural: `det C = 0` whenever
two damping rates coincide, and no bound in the rate spread *alone* can do better, since a `Q`
commuting with `H` gives `det(C∘Q̃)/det Q̃ = 1` for any spread.

Two consequences.

* **`det Φ_H(Q) ≥ det Q`, with equality iff `[H,Q] = 0`** — the normalized map never contracts
  volume. This is Oppenheim's inequality applied to a unit-diagonal `C`; only the equality
  characterization is specific to this kernel.
* **No-expansion ceiling.** Volume expansion (`det Σ_κ > det Σ_0`) requires
  `det H_κ < ρ(Q,L)`. Since `det H_κ → ∞`, **expansion is always confined to a bounded
  κ-window**, computable in closed form. `ρ` depends on the *orientation* of `Q` relative to `L`,
  not on `spec(Q)` (C7.5).

## 4. The two-mode threshold, explained

Dividing the repository's `bracket κ r = -8r²κ² + (r⁴-18r²+1)κ - 8r²` by `r²κ > 0` separates it:

    bracket κ r = r² κ ( anisotropy(r) - couplingCost(κ) ),
    anisotropy(r) = (r - 1/r)²,        couplingCost(κ) = 8(1+κ)²/κ.      (7)

Therefore **volume improves exactly when the noise anisotropy exceeds the cost of the coupling**.
The cost has an exact floor,

    couplingCost(κ) - 32 = 8(κ-1)²/κ  ≥  0,                              (8)

minimized **at `κ = 1`, for every `r`**. So improvement is possible for some `κ > 0` iff
`(r - 1/r)² > 32`, i.e. `r - 1/r > 4√2`, i.e.

    r > 3 + 2√2.

This recovers `MainTheorem.exists_volume_improvement_iff_threshold` with the two structural
constants now carrying meaning: **`34` in the quartic `r⁴ - 34r² + 1` is `32 + 2`**, coming from
the minimal coupling cost `32` via `(r-1/r)² = r² - 2 + 1/r²`; and **`3 + 2√2` is the noise ratio
at which the anisotropy first pays that minimum.** Formalized in
`OUCorridor/NormalizedLyapunov.lean`.

> **What `κ = 1` is and is not.**  `κ = 1` minimizes the *coupling cost*, hence the anisotropy
> *required* for improvement; so whenever some coupling improves the volume, `κ = 1` does.  It does
> **not** maximize the volume. From the closed form
> `det Σ_κ/det Σ_0 = (1 + (κ/(1+κ))² (r-1/r)²/4)/(1+2κ)`,
>
>     d/dκ [ det Σ_κ/det Σ_0 ]  at κ = 1  =  ((r - 1/r)² - 32)/144,
>
> which is **positive above the threshold**: the volume is still rising at `κ = 1`. At `r = 9`,
> `volume 1 9 = 481/12 < 657/16 = volume (3/2) 9`, and the maximizing coupling is near `κ = 1.38`.
> This is recorded in Lean as `volume_one_not_maximal` and in check C8.1.

## 5. Three modes: the threshold is geometry-dependent

Take the path Laplacian `L = [[1,-1,0],[-1,2,-1],[0,-1,1]]` (eigenvalues `0, 1, 3`, so
`a = 1, 1+κ, 1+3κ`) and `H_κ = I + κL`. Let `ratio(κ) = det Σ_κ/det Σ_0`.

**Theorem B (shape).** For every `Q > 0` and every `L ⪰ 0`:

* `ratio(0) = 1`;
* `ratio'(0) = -tr L`  (here `-4`), so **coupling always *decreases* volume to first order**;
* `ratio(κ) = Θ(κ^{-rank L})` as `κ → ∞` — **the exponent is the rank of the coupling, not the
  number of modes**. For a connected `n`-node graph this is `Θ(κ^{-(n-1)})`: `κ^{-1}` for the
  two-mode model, `κ^{-2}` for the three-node path, `κ^{-3}` for the four-node path (C8.2).
  Mechanism: `det H_κ = ∏(1 + κℓ_i) ~ κ^{rank L} ∏_{ℓ_i>0} ℓ_i` while `det(C ∘ Q̃)` tends to a
  positive limit (kernel modes keep `c_{ij} = 1` among themselves and decouple from the rest,
  `c_{0j} → 0`). For the three-node path the constant is
  `Q̃_{00}(Q̃_{11}Q̃_{22}/3 - Q̃_{12}²/4)/det Q`;
* expansion, if it occurs, occurs in the bounded window `det H_κ < ρ(Q,L)` of Theorem A.

*Proof of the second item.* By (6), `ratio(κ)·det H_κ = det(C∘Q̃)/det Q`, and
`1 - c_{ij}² = (a_i-a_j)²/(a_i+a_j)²= O(κ²)`, so `det(C∘Q̃) = det Q̃ + O(κ²)`. Hence
`ratio(κ)·det H_κ = 1 + O(κ²)` while `det(I + κL) = 1 + κ tr L + O(κ²)`. ∎
(Verified symbolically over `ℚ[κ]`: the numerator of `ratio·det H_κ - 1` has a double root at 0.)

**Theorem C (expansion does occur, and the two-mode threshold does not transfer).** With
`Q_r = diag(1,1,r²)` (noise on an end node) and `Q_r = diag(1,r²,1)` (centre node), expansion
occurs for large `r`, with *different* critical ratios:

| model | critical `r` | certified bracket |
|---|---|---|
| two modes (repository) | `3 + 2√2 = 5.828427…` | exact |
| three modes, centre node | `≈ 8.2781` | `[8.278000767, 8.278100768]` |
| three modes, end node | `≈ 10.7202` | `[10.720241993, 10.720242994]` |

Both endpoints are *proved*, not scanned: the expansion side by an exact rational witness
`(κ, r)` with `ratio > 1`, and the no-expansion side by a positivity certificate for
`g = D - N ≥ 0` on `[0,∞)` (subdivided Bernstein coefficients on the compact window of
Theorem A, which covers the rest). The certified bracket is wider than the numerical crossing
because `g` acquires a near-double root at the critical `r`; that is a limitation of the
certificate, not a statement about the intervening `r`.

**Centre-node noise has a closed form.** For `Q = diag(1, r², 1)` the two outer modes carry equal
noise, so `Q̃_{01} = Q̃_{12} = 0` and only one off-diagonal survives:

    det Σ_κ/det Σ_0 = ( 1 + 2κ²(r - 1/r)²/(2+3κ)² ) / ((1+κ)(1+3κ)),

so expansion is equivalent to

    (r - 1/r)²  >  8/κ + 30 + 36κ + 27κ²/2.

The right side has `κ² ·` derivative `27κ³ + 36κ² - 8` and second derivative `16/κ³ + 27 > 0`, so
its unique minimizer is the positive root of

    27κ³ + 36κ² - 8 = 0,     κ_* = 0.4120226592…,     r_* = 8.2780690232…,

which lies inside the certified bracket above. Note `κ_* ≠ 1`: the optimal coupling is **not**
`κ = 1` once there are more than two modes, so even the "minimal cost" reading of `κ = 1` is
two-mode-specific. (Verified against 30 independent exact Lyapunov solves, C8.5.)

**How much does the general sufficient condition (6''') capture?** Not much, and the answer is
quantitative. Taking the first `r` at which (6''') becomes satisfiable for some `κ > 0`:

| orientation | true threshold | (6''') first satisfiable | overshoot |
|---|---|---|---|
| centre node | `≈ 8.2781` | `≈ 62.2554` | `7.52×` |
| end node | `≈ 10.7202` | `≈ 13.1202` | `1.22×` |

The reason is visible in (6''): here `det C = 36κ⁶/[(2+κ)(2+3κ)(2+4κ)]²`, which tends to
`(9/16)κ⁶` as `κ → 0` (the denominator tends to `64`, but the numerator keeps its factor `36`) —
so the refinement contributes almost nothing in the window `κ ≈ 0.4` to `0.9` where expansion
actually happens. **A sharper bound must retain the off-diagonal structure of `Q̃`, not
just `ρ` and a global factor `det C`.** (C8.6.)

`diag(1,1,r²)` and `diag(1,r²,1)` have the **same spectrum**, so:

> **The volume threshold is not a function of `spec(Q)` and `spec(L)`.** It depends on the
> orientation of the noise relative to the network. At `r = 9` the centre-node model expands and
> the end-node model does not (C6.7).

This is why Theorem B's third bullet matters: `ρ(Q,L)` is exactly the orientation-sensitive
quantity, and it is what rules out any single universal constant playing the role of `3 + 2√2`
in the many-mode setting.

## 6. The single-correlated-pair theorem

The centre-node case closed in closed form because equal noise on the two outer nodes forces
`Q̃_{01} = Q̃_{12} = 0`. That is a general class, and it has a general theorem.

**Setting.** `L ⪰ 0`, `H_κ = I + κL` with eigenvalues `λ_i`, `Q ≻ 0`, and in a fixed eigenbasis
of `L` the only off-diagonal entries of `Q̃` are the Hermitian pair `(p,q)`. Put

    η = |Q̃_pq|²/(Q̃_pp Q̃_qq - |Q̃_pq|²),   s = λ_p + λ_q,   Δ = λ_p - λ_q,
    D(κ) = ∏_i (1 + κλ_i) = det H_κ.

**Theorem D (exact ratio).**

    det Σ_κ/det Σ_0  =  ( 1 + η κ²Δ²/(2 + sκ)² ) / D(κ).                (9)

*Proof.* `C ∘ Q̃` is diagonal except for the `(p,q)` block, so
`det(C ∘ Q̃) = ∏_{i≠p,q} Q̃_ii · (Q̃_pp Q̃_qq - c_{pq}²|Q̃_pq|²)`, while
`det Q̃ = ∏_{i≠p,q} Q̃_ii · (Q̃_pp Q̃_qq - |Q̃_pq|²)`. Dividing and using (6),

    det Σ_κ/det Σ_0 = [Q̃_pp Q̃_qq - c_{pq}²|Q̃_pq|²] / [D(κ)(Q̃_pp Q̃_qq - |Q̃_pq|²)]
                     = (1 + (1 - c_{pq}²) η)/D(κ),

and `1 - c_{pq}² = (a_p - a_q)²/(a_p + a_q)² = κ²Δ²/(2 + sκ)²`. ∎

This separates the mechanism: **one correlated pair supplies the gain; every damped mode
contributes to the cost.** If `Δ = 0` there is no gain and expansion is impossible at any `κ`.

**Corollary.** For `Δ ≠ 0` and `κ > 0`, expansion at `κ` is exactly `η > T(κ)` with

    T(κ) = (D(κ) - 1)(2 + sκ)²/(κ²Δ²).                                  (10)

**Theorem E (normal form).** Writing `D(κ) - 1 = ∑_{j≥1} e_j κ^j` with `e_j ≥ 0` the elementary
symmetric functions of the `λ_i` and `e_1 = tr L`, expanding `(2 + sκ)²` gives

    T(κ) = A/κ + ∑_{j≥0} c_j κ^j,     A = 4(tr L)/Δ² > 0,   c_j ≥ 0.     (★)

*Proof.* `T = (1/Δ²)∑_{j≥1} e_j (4κ^{j-2} + 4sκ^{j-1} + s²κ^j)`. The only negative power arises
from `j = 1` at `κ^{-1}`, with coefficient `4e_1/Δ²`; every other term has a nonnegative power and
a nonnegative coefficient. ∎

**Theorem F (convexity, uniqueness, interval).** Under (★), on `(0,∞)`:

* `T` is **strictly convex**, with `T''(κ) ≥ 8(tr L)/(Δ²κ³) > 0`;
* `T → ∞` at both ends, so `T` has a **unique minimizer** `κ_†` and `η_crit = T(κ_†)`;
* for each `η`, `{κ > 0 : T(κ) < η}` is an **interval** — expansion occurs on exactly one
  bounded interval of couplings, and at `η = η_crit` the ratio touches `1` at exactly one `κ`;
* `κ_†` is the unique positive root of `κ²T'(κ)`, a polynomial of degree `rank L + 1` with nonzero
  constant term. So the thresholds are **implicitly** characterized for every `n`; explicit
  radical formulas need not exist.

Formalized in `OUCorridor/SinglePair.lean` (strict convexity, the interval, uniqueness of the
minimizer, and the floor below).

**Theorem G (floor).** Since `D(κ) - 1 ≥ κ tr L` and `(2 + sκ)² ≥ 8sκ` (equality at `sκ = 2`),

    η_crit  ≥  8(tr L)(λ_p + λ_q)/(λ_p - λ_q)²  ≥  8,                   (11)

the second step from `(λ_p-λ_q)² ≤ (λ_p+λ_q)² ≤ (tr L)(λ_p+λ_q)`. **Adding independent damped
modes without adding noise correlation cannot lower the threshold.**

### Both repository models are instances

| model | `η` | `A` | `(c_j)` | onset | `η_crit` |
|---|---|---|---|---|---|
| two modes, `λ = 0,2` | `(r-1/r)²/4` | `2` | `4, 2` | `κ_† = 1` | `8` |
| three-node path, centre noise, `λ = 0,1,3`, pair `(0,2)` | `2(r-1/r)²/9` | `16/9` | `20/3, 8, 3` | `27κ³+36κ²-8 = 0` | `14.7869…` |

The two-mode row gives `(r-1/r)²/4 > 8`, i.e. `r > 3+2√2`, and `couplingCost = 4T`: the
normalization of §4 is the `n = 2` case of (★). The centre row reproduces §5's cubic, since
`κ²T'Δ² = 2(27κ³ + 36κ² - 8)`.

Further instances computed exactly (`singlepair9.py`): `λ = (0,1,3)` pair `(1,2)` gives
`κ_† = 1/3`, `η_crit = 125/3`; `λ = (0,1,1,4)` pair `(0,3)` gives `κ_† = 0.2534…`,
`η_crit = 19.1237…`; `λ = (2,2,5)` (no kernel mode) pair `(0,2)` gives `κ_† = 0.1434…`,
`η_crit = 89.8567…`. The floor (11) holds in each.

### Scope

Theorem D requires `Q̃` to have exactly one off-diagonal pair. The **end-node** three-mode model
has all three off-diagonals nonzero and is *not* covered; its threshold remains only bracketed,
though its expansion set is a single interval at every tested noise level (C9.9).

The single-pair hypothesis is **not removable** — see §7.

## 7. The interval property fails for two correlated pairs

A conjecture considered here — that `{κ > 0 : det Σ_κ > det Σ_0}` is always a single interval — is
**false**, already for three modes on a connected network, and with the determinant cycle term
identically zero.

**Witness.** In the damping eigenbasis,

    L = diag(0, 100, 1),    Q̃ = [[2035, 3, 45], [3, 1, 0], [45, 0, 1]].

`Q̃ ≻ 0` (leading principal minors `2035, 2026, 1`). The eigenvalues `0, 100, 1` are realized by a
**connected weighted triangle** with edge weights `299/6, 1/3, 1/3`: its Laplacian has trace `101`,
sum of `2×2` principal minors `100`, and determinant `0` (C10.8). By Theorem D's computation,
specialized to the two pairs `(0,1)` and `(0,2)` with `Q̃₁₂ = 0`,

    det Σ_κ/det Σ_0 = [ 1 + 9(100κ/(2+100κ))² + 2025(κ/(2+κ))² ] / [(1+100κ)(1+κ)].   (12)

| `κ` | exact ratio | |
|---|---|---|
| `1/50` | `3517825/3121506 = 1.126964…` | expansion |
| `1/10` | `1055/1078 = 0.978664…` | **contraction** |
| `1` | `33907/29189 = 1.161636…` | expansion again |

Three strict rational inequalities, each reproduced from an independent solve of `HΣ + ΣH = Q̃`
(C10.3–C10.5). So the expansion set is disconnected — it has exactly two components on the
scanned range (C10.6). Formalized as `witness_expansion_set_not_convex`.

**Mechanism: two correlated pairs at different damping scales, not cycles.** `Q̃₁₂ = 0` makes
`Q̃₀₁Q̃₁₂Q̃₀₂ = 0`, so no cycle term is involved. The pair `(0,1)` straddles rates `1` and `1+100κ`
and delivers its gain at small `κ`; that gain saturates (`c₀₁ → 0`) before the pair `(0,2)`,
straddling `1` and `1+κ`, delivers its own at `κ ≈ 1`. In between, neither gain covers `det H_κ`.

Note the witness is genuinely joint: zeroing *either* correlation removes expansion altogether
(C10.7), because doing so raises `det Q̃` from `1` to `2026` or `10` and drops the surviving pair's
`η` below its `η_crit`. The near-singularity of `Q̃` is what makes both normalized correlations
strong at once.

**Consequence.** The correct general statement is:

> A single correlated mode pair guarantees one expansion interval (Theorem F). Several correlated
> pairs can produce **separated** expansion intervals, already for three modes on a connected
> network.

### Two bookkeeping corrections this forces

* **"One expansion interval" is not "unimodality".** These were conflated in an earlier draft of
  this document's open question. **When expansion occurs** the ratio is not unimodal, because
  `ratio′(0) = −tr L < 0`: it starts by decreasing. At `r = 9` the two-mode ratio falls to `0.9823`
  at `κ = 0.01`, rises to its maximum `2.0322` near `κ = 1.37`, then falls again (C10.10). An
  earlier draft reported that peak as `1.8037` near `κ = 0.69`, misreading the grid argmax `69/50`
  as `0.69`; `R(3/2) = 73/36 = 2.0278` is already larger. Saying the ratio is *never* unimodal is
  also too broad: with `[H,Q] = 0` the ratio is exactly `1/det H_κ`, which is monotone decreasing
  (C11.10). The interval claim concerns the superlevel set `{R > 1}` and is strictly weaker.
* **The `7.5×` overshoot of (6''') is not caused by the cycle term.** An earlier draft guessed it
  was. It cannot be: the centre-node model *is* single-pair (`Q̃₀₁ = Q̃₁₂ = 0`), so its cycle term
  already vanishes. The actual cause is that the exact mechanism is `1 − c_{02}² = Θ(κ²)`, from the
  one pair that carries noise, whereas `det C` multiplies the rate-difference factors of **all
  three** pairs — including the two carrying no noise correlation — giving `Θ(κ⁶)` (C10.9).
  Discarding pair-specific information is by itself enough to make the bound weak.

## 8. How many expansion components? At most one per correlated pair

The counterexample of §7 raises the quantitative question, and it has a general answer.

**Theorem H.** Let `L ⪰ 0`, `Q ≻ 0`, `H_κ = I + κL`, and suppose that in a fixed eigenbasis of `L`
the matrix `Q̃` has exactly `k` nonzero unordered off-diagonal pairs `E`. Then

    {κ > 0 : det Σ_κ > det Σ_0}  has at most  k  connected components.

*Proof.* Put `a_i = 1 + κλ_i`, `D(κ) = ∏_i a_i = det H_κ` and `B(κ) = ∏_{{i,j} ∈ E}(a_i + a_j)²`.

*Step 1: `N := B · det(C ∘ Q̃)` is a polynomial of degree at most `2k`.* Expand the determinant
over permutations. A permutation contributes `(∏_i Q̃_{i,π(i)}) · ∏_{\text{cycles}} ∏ c`, and over a
cycle of length `m ≥ 2` the square roots cancel:
`∏ c = 2^m (∏_{i ∈ cyc} a_i)/∏_{\text{edges}}(a_i + a_j)`, which is rational of degree `0`. A
surviving term needs `Q̃_{i,π(i)} ≠ 0`, so every cycle edge lies in `E`. A transposition
contributes `c_{ij}²`, denominator `(a_i+a_j)²`; a longer cycle contributes each of its edges once.
So every denominator divides `B`, `N` is a polynomial, and since `det(C ∘ Q̃)` has degree `0` as a
rational function while `deg B = 2k`, `deg N ≤ 2k`.

*Step 2: the numerator.* `det Σ_κ/det Σ_0 = det(C ∘ Q̃)/(D · det Q)` by (6), so

    det Σ_κ/det Σ_0 - 1 = (N - B·D·det Q)/(B·D·det Q).

At `κ = 0` all `a_i = 1`, so `B(0) = 4^k` and `N(0) = 4^k det Q`: the numerator vanishes at `0`,
hence equals `κ A(κ)` for a polynomial `A`. Comparing with `ratio′(0) = −tr L` (Theorem B) gives

    A(0) = -4^k (det Q)(tr L) < 0   whenever L ≠ 0.

*Step 3: the tail signs.* For `j > 2k` the coefficient of `κ^j` in `N` vanishes, so the `κ^j`
coefficient of `κA` comes only from `−B·D·det Q`. Both `B` and `D` are products of `1 + κλ_i` with
`λ_i ≥ 0`, so they have nonnegative coefficients. Hence **every coefficient of `A` in degree
`≥ 2k` is nonpositive.**

*Step 4: counting.* `A`'s coefficient sequence is: a negative constant; at most `2k − 1`
coefficients of unrestricted sign; then a nonpositive tail. Such a sequence has at most `2k` sign
variations, so by Descartes' rule `A` has at most `2k` positive roots with multiplicity.

*Step 5: components.* `ratio < 1` just above `0` (Step 2) and for all large `κ` (Theorem B's
`Θ(κ^{−rank L})` decay). So every component of `{κ > 0 : ratio > 1}` is a bounded open interval
whose two endpoints are positive roots of `A`; distinct components contribute distinct roots,
counting multiplicity at a shared tangency. Hence `#components ≤ 2k/2 = k`. For `L = 0` or `k = 0`
there is no expansion at all. ∎

**Status.** Steps 1–3 are verified exactly in `components11.py` across 7 instances with
`n = 2…5` and `k = 0…5`, with and without cycle terms, each against independent solves of
`HΣ + ΣH = Q̃` (C11.1–C11.4). Step 4's combinatorial core — *nonpositive coefficients from degree
`m` on ⟹ at most `m` sign variations ⟹ at most `m` positive roots* — is **formalized** in
`OUCorridor/ComponentCount.lean` (`signVariations_le_of_tail_nonpos`,
`roots_pos_le_of_tail_nonpos`), on top of Mathlib's `roots_countP_pos_le_signVariations`. Steps 1–3
and 5 remain analytic.

**Sharpness: attained at `k = 1, 2, 3`.** `k = 1` is the two-mode model and `k = 2` is §7's
witness (exactly two components, C10.6). For `k = 3` the bound is attained by **three disjoint
correlated pairs**. With `Q_b = [[1, b], [b, 1+b²]]` (positive definite, `det Q_b = 1`), take

    Q̃ = diag(Q₃, Q₆₀, Q₃₅₀₀),    L = diag(0, 1000, 0, 1, 0, 1/10000).

There are exactly three nonzero off-diagonal pairs, pairwise disjoint, so no cycle terms. Both
`Q̃` and `L` are block diagonal, so both determinants factor and

    ratio(κ) = ∏_j F_{a_j,b_j}(κ),    F_{a,b}(κ) = [1 + b²(aκ/(2+aκ))²]/(1 + aκ).   (13)

| `κ` | `ratio(κ)` | |
|---|---|---|
| `10⁻⁵` | `0.9903097561…` | contraction |
| `1/500` | `1.0850553501…` | expansion |
| `1/20` | `0.5468684142…` | contraction |
| `1` | `2.0567176187…` | expansion |
| `10` | `0.9216229469…` | contraction |
| `100` | `1.0321406040…` | expansion |
| `1000` | `0.9048415486…` | contraction |

All seven comparisons are exact over `ℚ`, each with `Σ` checked against `HΣ + ΣH = Q̃` (C12.3–4).
The alternation forces at least three components and Theorem H permits at most three, so there
are **exactly three**. An independent polynomial route agrees: `A` has degree `8` with coefficient
signs `−,+,−,+,−,+,−,−,−` in ascending degree — exactly `2k = 6` sign variations, so **Descartes
is tight here** and the six crossings forced by the witnesses use the entire budget (C12.6–7).

Note (13) is a **product** over pairs. That is why the star-pattern search of the previous round
could not have found this witness: in a star all pairs share a mode, and the linear reduction
below applies instead.

*Connected realization.* Six vertices in three pairs; every edge between different pairs has weight
`ε = 10⁻⁸`, and the edge inside pair `j` has weight `(a_j − 4ε)/2 > 0`. All weights are positive so
the graph is connected. Applying the Laplacian to the explicit eigenvectors — the all-ones vector,
the three within-pair antisymmetric vectors, and two symmetric vectors orthogonal to `1` — gives
eigenvalues `0, a₁, a₂, a₃, 6ε, 6ε` exactly (C12.9). Using the same `Q̃` in that ordered
eigenbasis, all seven signs survive, with `ratio(10) = 0.920788…`, `ratio(100) = 1.030888…`,
`ratio(1000) = 0.903596…` (C12.10). So sharpness holds on a connected network with a
one-dimensional kernel. Formalized as `sharp3_not_union_of_two_convex`.

**What sharpness does *not* mean.** It does not say the realized component count is a function of
the correlation pattern. Theorem H is a structural *ceiling* that suitable rates and noise
strengths attain; the rates and strengths still decide whether a given system has zero, one, two or
three windows. Keeping the same `k = 3` pattern and the same `L` but rescaling `b_j ↦ b_j/2` (with
the diagonal adjusted to keep `det Q̃ = 1`, i.e. `η_j ↦ η_j/4`) drops the count from three to zero
(C12.11). Halving the off-diagonal entries with the *diagonal held fixed* is even more drastic:
`η ↦ η/(4 + 3η) < 1/3` for every `η` (C13.6). §9 explains both.

**`k = 4` and `k = 5` are attained too** — see §10, where a sufficient criterion certifies whole
parameter boxes with exactly four and exactly five windows. (A crude greedy tuning attempted here
reached only three; the working parameters are `(a_j) = (1000, 1, 10⁻⁴, 10⁻⁸, 10⁻¹²)` with
`(b_j) = (3, 60, 3500, 45000, 2000000)`.) Attainment for arbitrary `k` remains open.

**Star patterns remain a separate question.** For `Q̃ = [[M, x_1, …, x_k], [x_1, 1, 0, …], …]` with
`det Q̃ = M − Σ x_i²`,

    ratio(κ) = [1 + Σ_i w_i g_i(κ)]/D(κ),   w_i = x_i²/det Q̃,   g_i(κ) = (μ_i κ/(2 + μ_i κ))²,

and both `ratio > 1` and `ratio < 1` at a given `κ` are *linear* in `w`. Prescribing three
separated windows is a linear feasibility problem; a bounded search over five scale choices found
no feasible `w`, which settles nothing either way (C11.12). This no longer bears on Theorem H's
sharpness, only on whether a star can achieve the ceiling.

### Two more corrections this forces

* **Per-pair contributions are not additive.** An earlier draft of the open question in
  `REPORT.md` reasoned that "each pair contributes an additive term `η_pq(1 − c_pq²)`". That holds
  for a star (one shared mode) but not in general: two *disjoint* correlated blocks give
  `(1 + η₁δ₁²)(1 + η₂δ₂²)`, with a product term (C11.6). The common-denominator proof above needs
  no additivity and covers cycle terms as well.
* **Star structure does not force one interval.** The same draft proposed star patterns as a
  candidate restriction. §7's counterexample *is* a star — both its correlations share mode `0`
  (C11.7) — so that candidate is refuted by the witness itself. It remains a useful class for
  studying the component count, as the linear reduction above shows.
* **The saturation scale is `2/s`, not `1/Δ`.** Since
  `1 − c_pq² = (Δ²/s²)·(κ/(κ + 2/s))²` (C11.8), a pair's gain saturates on the scale set by the
  rate *sum* `s = λ_p + λ_q`, while `Δ/s` fixes the limiting amplitude. The earlier draft said
  `≈ 1/Δ`.

## 9. A necessary cost bound for attaining the full ceiling

Theorems F–H bound *how complicated* expansion can be. This section bounds *how strong the
correlations must be* to reach the ceiling `c = k` — the first quantitative "when" statement beyond
the single pair of Theorem G.

**The aggregate cost.** Individual pair parameters do not capture all determinant interactions, but
a quantity already in use here does:

    ρ(Q) = ∏_i Q̃_ii / det Q̃.

For disjoint correlated blocks `ρ = ∏_{j=1}^{k}(1 + η_j)`, and for the blocks
`Q_b = [[1,b],[b,1+b²]]` of §8, `η_j = b_j²`.

**Theorem I (necessary cost).** In Theorem H's notation, assume `deg B = 2k`. Attaining `k`
components forces `A` to realize all `2k` permitted sign variations, hence its last potentially
positive coefficient must be positive:

    [κ^{2k-1}] A > 0,   i.e.   [κ^{2k}] N > det Q · [κ^{2k}](D·B).

Writing `ρ_∞ = det(C_∞ ∘ Q̃)/det Q̃` for the limiting normalized gain, `N = B·det(C ∘ Q̃)` with
`deg B = 2k` gives `[κ^{2k}]N = [κ^{2k}]B · ρ_∞`, so

    ρ_∞  >  T(E, L) := [κ^{2k}](D·B) / [κ^{2k}]B,                      (14)

and since Hadamard gives `ρ_∞ ≤ ρ`, also **`ρ > T(E, L)`**. This holds with cycle terms.

**Scope.** (14) is an *exclusion* test: below the floor `k` components are impossible; above it
they are not guaranteed. It is also **not optimal** — for one isolated pair with rates `(0,2)` it
gives `T = 5`, i.e. `η > 4`, whereas Theorem F's exact threshold is `η > 8` (C13.5).

**Closed form for three `(0, a_j)` blocks.** Here `B = ∏_j (2 + a_jκ)²` and `D = ∏_j (1 + a_jκ)`,
so `D·B = ∏_j (4 + 8a_jκ + 5a_j²κ² + a_j³κ³)` and `[κ^6]B = ∏_j a_j²`. Collecting the exponent
multisets `{2,2,2}`, `{3,2,1}`, `{3,3,0}` and dividing by `∏ a_j²`:

    ∏_{i=1}^{3}(1 + η_i)  >  125 + 40 Σ_{i≠j} a_i/a_j + 4 a₁a₂a₃ Σ_i a_i^{-3}.   (15)

The limiting channel kills every within-block correlation (one rate is `0`, the other grows, so
`c → 0`), hence `ρ_∞ = ρ` exactly here and (15) is (14) with no Hadamard slack (C13.1–2).

**The `k = 3` witness sits close to its floor.** At `(a₁,a₂,a₃) = (1000, 1, 10⁻⁴)`,

    T = 1001001100313610010001/2500000000 = 400400440125.444004000400…

while the witness has `ρ = (1+3²)(1+60²)(1+3500²) = 441122536010`, clearing it by about `10%`.
Holding `b₁ = 3` and `b₂ = 60` fixed therefore forces

    η₃ > 11119144.7963…,     b₃ > 3334.538168…,

and the witness's `b₃ = 3500` is only **4.96%** above that floor (C13.3). The exclusion bites:
at `η₃ = 11000000` the coefficient `[κ^5]A` is `−4.2904·10⁷ < 0`, leaving only `4` sign variations
(pattern `−,+,−,+,−,−,−,−,−` instead of `−,+,−,+,−,+,−,−,−`), so at most two components —
confirmed by scanning (C13.4). Machine-checked as `witness_rho_gt_costFloor3` and
`eta3_11e6_lt_costFloor3`, with the logical shape as `roots_pos_le_of_top_free_nonpos`.

**What this does and does not establish.** The large third correlation is substantially forced
*within this fixed construction*. It is not a steep universal cost across all spectra and
correlation patterns, and (14) says nothing about `1 ≤ c < k`, nor anything sufficient.

## 10. A sufficient criterion: monotone envelopes over parameter boxes

Every statement so far is an exclusion, apart from Theorem F's `η > T(κ)` for a single pair. This
section supplies a positive criterion, and it certifies whole families rather than single points.

**The correction that shapes it.** A lower bound on noise strength alone *cannot* force several
windows. Raising all `b_j` fills the intervening contraction gaps and merges the windows: for the
nominal families below, multiplying every `b_j` by `10` makes **every free coefficient of `A`
positive**, collapsing the sign pattern from `−,+,−,+,−,+,−,−,−` to `−,+,+,+,+,+,−,−,−` (two sign
variations) and leaving a single component (C14.5). A sufficient criterion must therefore control
*separation* as well as expansion.

**The envelope.** Write `g(z) = (z/(2+z))²`, which is strictly increasing on `(0,∞)`. For a block
with rates `(0, a)` and strength `b`, `F(κ) = [1 + b²g(aκ)]/(1 + aκ)`, so over a box
`a ∈ [a⁻, a⁺]`, `b ∈ [b⁻, b⁺]` with `0 < a⁻`, `0 ≤ b⁻`:

    [1 + (b⁻)² g(a⁻κ)]/(1 + a⁺κ)  ≤  F(κ)  ≤  [1 + (b⁺)² g(a⁺κ)]/(1 + a⁻κ).      (16)

The numerator increases in `a` and in `b ≥ 0`, the denominator in `a`, so the two corner
expressions bracket `F`. Formalized as `gFactor_le_gFactor` and `blockRatio_mem_box`.

**The criterion.** Multiply (16) over disjoint blocks. If the **upper** product is `< 1` at a set of
separating couplings and the **lower** product is `> 1` at interleaved couplings, then *every*
parameter choice in the box exhibits those separated windows. Combined with Theorem H's ceiling this
pins the count exactly.

**Certified families.** Take

    (a_j) = (1000, 1, 10⁻⁴, 10⁻⁸, 10⁻¹²),    (b_j) = (3, 60, 3500, 45000, 2000000),

the first four blocks for `k = 4` and all five for `k = 5`, and let **every parameter vary
independently** with `a_j` within `±0.1%` and `b_j` within `±0.25%` of nominal. Exact rational
evaluation of the envelope product gives, valid throughout the five-block box:

| `κ` | bound | | `κ` | bound |
|---|---|---|---|---|
| `10⁻⁵` | `R < 0.991` | | `10³` | `R < 0.969` |
| `1/500` | `R > 1.079` | | `10⁴` | `R > 1.449` |
| `1/20` | `R < 0.553` | | `10⁶` | `R < 0.429` |
| `1` | `R > 2.031` | | `10⁷` | `R > 1.793` |
| `10` | `R < 0.938` | | `10⁹` | `R < 0.581` |
| `10²` | `R > 1.013` | | | |

The first nine also hold for the four-block box (C14.3). The five expansion couplings separated by
six contraction couplings force at least five components for every box member; Theorem H permits at
most five; so **exactly five**, and likewise **exactly four** for the four-block box. Hence:

> **Theorem H is sharp at `k = 4` and `k = 5`, robustly** — under simultaneous perturbation of all
> rates and all noise strengths, not just at isolated parameter values.

Both nominal families also saturate Descartes: `signVariations(A) = 8 = 2k` for `k = 4` and
`10 = 2k` for `k = 5` (C14.2). Attainment for arbitrary `k` remains open.

### The band constraint

For `c < k` no individual coefficient is forced, but it is too strong to say nothing is. Having at
least `c` components requires

    [κ^j] A > 0   for some  j ∈ {2c-1, …, 2k-1},                        (17)

since otherwise the nonpositive tail would begin at degree `2c − 1`, giving at most `2c − 1`
positive roots and hence at most `c − 1` components. This interpolates the *logical structure* of
Theorem I: at `c = k` the band narrows to the single coefficient `[κ^{2k-1}]A`. The general
`roots_pos_le_of_tail_nonpos` covers both, with `m = 2c − 1`. §11 collapses the disjunction for
matching patterns.

## 11. A necessary cost for every component count (matching patterns)

For a **matching** pattern — `k` pairwise disjoint correlated pairs, each with positive rate sum —
the disjunction (17) collapses to a single computable floor. Let
`s_* = max_{{p,q} ∈ E}(λ_p + λ_q)`.

**Theorem J.** At least `c` expansion components requires

    ρ_∞  >  T_c^match(E, L) := max{ 1 + 8(tr L)/s_* ,  [κ^{2c}](D·B)/[κ^{2c}]B }.   (18)

The bound is on `ρ_∞ = det(C_∞ ∘ Q̃)/det Q̃`, **not** on `ρ = ∏_i Q̃_ii/det Q̃`. Hadamard gives
`ρ_∞ ≤ ρ`, so (18) also yields the weaker necessary condition `ρ > T_c^match`, and the two
coincide only when the limiting channel kills every correlation — as it does for the zero/positive
rate pairs `(0, a_j)` of §8, where `c_{pq} → 0`, but **not** for an arbitrary pattern, nor for
matching pairs with both rates positive, where `c_{pq} → 2√(λ_pλ_q)/(λ_p+λ_q) > 0`.

The first term is the single-window cost; the second increases with `c` and becomes Theorem I's
coefficient ratio at `c = k`.

*Proof, in two ingredients.*

**(i) Coefficientwise domination `N ⪯ (det Q) ρ_∞ B`.** For one pair with `s = λ_p + λ_q`,
`η = |Q̃_pq|²/det_j` and limiting gain `r_∞ = (1+η) − 4λ_pλ_q η/s²`, the block's normalized
numerator is *exactly*

    n_j(κ) = (a_p+a_q)²(1+η) − 4a_pa_q η = 4 + 4sκ + s² r_∞ κ²,

so, comparing coefficients against `r_∞(2 + sκ)² = r_∞(4 + 4sκ + s²κ²)` and using `r_∞ ≥ 1`
(Oppenheim per block),

    n_j ⪯ r_∞ (a_p + a_q)².

All coefficients are nonnegative, so the inequalities multiply: `N = (det Q)∏_j n_j` gives
`N ⪯ (det Q)(∏_j r_{∞,j}) B = (det Q) ρ_∞ B`. (Verified across six matching instances including
nonzero rates on both sides of a pair, equal rates within a pair, and extra uncorrelated damped
modes — C15.1.)

**(ii) `q_m = [κ^m](D·B)/[κ^m]B` is nondecreasing on `0 ≤ m ≤ 2k`.** All roots of `B` are negative,
so its coefficient sequence is log-concave by Newton's inequalities, making `β_{m-1}/β_m`
nondecreasing; expanding `D·B` transfers this to `q_m` (checked at eleven rate configurations,
C15.2).

Now (17) supplies some `m ∈ {2c, …, 2k}` with `[κ^m]N > (det Q)[κ^m](D·B)`. By (i),
`(det Q)ρ_∞[κ^m]B ≥ [κ^m]N`, so `ρ_∞ > q_m`, and by (ii) `q_m ≥ q_{2c}`. **The band's minimum sits
at its bottom.**

For the first term, write `G(κ) = ∏_j(1 + w_j u_j)`, `u_j = (s_jκ/(2+s_jκ))² ∈ [0,1]`,
`ρ_∞ = ∏_j(1+w_j)`. Since each `u_j ≤ u_*`, the saturation envelope
`∏_j(1 + w_j u) ≤ 1 + (ρ_∞ − 1)u` for `0 ≤ u ≤ 1` (formalized as `prod_one_add_mul_le`) gives
`G(κ) ≤ 1 + (ρ_∞ − 1)u_*`. Expansion needs `G(κ) > D(κ) ≥ 1 + κ tr L`, so
`ρ_∞ − 1 > κ(tr L)/u_* = (tr L)(2 + s_*κ)²/(s_*² κ)`, and `min_{x>0}(2+x)²/x = 8` gives the term. ∎

**Endpoint.** At `c = k = 1` with rates `(0,a)` the two terms are `9` and `5`, so (18) reads
`ρ_∞ = 1 + η > 9`, i.e. **`η > 8` — Theorem F's exact threshold**. This is why the `max` is needed:
Theorem I's coefficient ratio alone gives only `η > 4`, and an interpolating bound must retain the
stronger single-pair result rather than agree with both formulas at the endpoint (C15.3).

**The three-block spectrum.** For rate pairs `(0,1000)`, `(0,1)`, `(0,10⁻⁴)`:

| at least | necessary `ρ_∞` floor |
|---|---|
| `1` component | `9.0080008` |
| `2` components | `8022.603677…` |
| `3` components | `400400440125.444004…` |

The `k = 3` witness has `ρ_∞ = 441122536010` and clears all three (C15.4). These are necessary
bounds — not sufficient conditions, and not claimed optimal.

**Scope.** Theorem J is proved only for matching patterns. For a general correlation pattern the
coefficientwise domination of step (i) is **not** established here, and that — not the `min` over
the band — is the missing step: one must first justify controlling the lower coefficients of `N`
by `ρ_∞`.

### Two further corrections

* **The certified boxes are not nearly maximal.** An earlier reading here took the envelope values
  landing within `10⁻³` of the stated thresholds as evidence that the radii were near-maximal. The
  thresholds were rounded presentation values; the real boundary is `R = 1`. Enlarging both radii by
  `5/3` — rates `±1/600 ≈ ±0.1667%`, strengths `±1/240 ≈ ±0.4167%` — still passes every exact
  envelope comparison, the tightest expansion bound being `1.001246350696674…` at `κ = 100`
  (C15.5).
* **"`c < k` is generic" was unsupported.** A prevalence claim needs a specified parameter domain
  and measure. What is established is that `c = k` holds on nonempty *open* parameter regions
  (§10); narrow certified boxes say nothing about the relative size of the `c < k` region.
