# Report: the OU covariance response as a normalized Lyapunov map

**Verdict: the view is useful, and it now yields a general threshold theorem, not only an
explanation.**

Recognizing the normalized covariance response as the Schur multiplier by the
geometric-over-arithmetic mean matrix turns the repository's two-mode threshold from a
discriminant computation into a statement with meaning, and gives a second machine-checked proof
of the main theorem. Pushed further, it produces the **single-correlated-pair theorem**
(Theorems D–G): for any `L ⪰ 0` and any noise whose rotation has one off-diagonal pair, the exact
determinant ratio is `(1 + ηκ²Δ²/(2+sκ)²)/det H_κ`, the threshold function is strictly convex, the
onset coupling is unique and solves a degree-`(rank L + 1)` polynomial, the expanding couplings
form one bounded interval, and `η_crit ≥ 8(tr L)s/Δ² ≥ 8`. **The two-mode threshold and the
three-node cubic are the two smallest instances of one result.**

The theorem's hypothesis is **sharp**: with two correlated pairs at different damping scales the
expansion set can be *disconnected*, by an exact three-mode witness on a connected network whose
determinant cycle term vanishes identically (§7 of [DERIVATION.md](DERIVATION.md)). And the
disconnection is **quantitatively bounded and the bound is attained**: `k` correlated noise pairs
allow at most `k` expansion components (Theorem H, §8), proved by a common-denominator construction
plus Descartes' rule of signs, and three disjoint correlated pairs realize exactly three windows —
on a connected network, with the Descartes budget saturated. So the qualitative picture is now
complete: the correlation pattern caps the complexity of the expansion set, and nothing weaker
does. A first quantitative *when* statement follows too (Theorem I, §9): attaining the full ceiling
`c = k` requires the aggregate correlation `ρ = ∏Q̃_ii/det Q̃` to exceed an explicit coefficient
ratio `T(E,L)`, and the `k = 3` witness sits only `5%` above its own floor in `b₃`. And a
**sufficient** criterion closes the loop (§10): monotone envelopes certify entire parameter boxes
with exactly four and exactly five windows, so the ceiling is attained at `k = 1…5`, robustly under
simultaneous perturbation of all rates and strengths. Finally, on matching patterns the necessary
cost extends to *every* component count (Theorem J, §11), with the sharp single-pair `η > 8`
recovered at the endpoint.

Along the way the investigation **refuted** ten natural guesses — that `3 + 2√2` extends to many
modes; that the onset coupling `κ = 1` is universal; that the expansion set is always one interval;
that the `7.5×` overshoot of Theorem A′ comes from the determinant cycle term; that per-pair
contributions are additive; that star correlation patterns force one interval; and that sharpness
would make the component count a function of the correlation pattern; and that a lower bound on
noise strength alone would give a sufficient condition for several windows; that the certified
parameter boxes were near-maximal; and that `c < k` is generic — and reclassified two results that looked new as classical (Oppenheim's inequality; the multiplicative
domain of a Schur channel).

## 1. Plain language

A symmetric OU system has a stationary covariance `Σ` determined by `HΣ + ΣH = Q`, where `H` is
the damping and `Q` the noise. Rescaling by the damping, the map `Q ↦ Φ_H(Q)` that produces the
covariance is, in the damping's own eigenbasis, nothing but *entrywise multiplication by a fixed
matrix of correlation coefficients* — one coefficient per pair of damping rates, equal to the
geometric mean of the pair over its arithmetic mean. That coefficient is `1` when the two rates
agree and shrinks as they separate.

Everything follows from reading that off. The covariance is a damped copy of the noise, damped
pair-by-pair according to how unequal the damping rates are. Coupling the system spreads the
damping rates apart, which shrinks the off-diagonal coefficients: this is both the *cost* of
coupling and, because shrinking an off-diagonal entry of a positive matrix can raise its
determinant, the *mechanism* by which coupling can expand the covariance volume. The threshold is
exactly the point where the noise is lopsided enough that the gain beats the cost.

## 2. Precise statements

See [DERIVATION.md](DERIVATION.md) for proofs. In brief, with `H > 0`, rates `a_i`,
`c_ij = 2√(a_i a_j)/(a_i + a_j)`:

* **Lemma 1.** `Φ_H(X)_{ij} = c_{ij} X_{ij}` in the eigenbasis of `H`.
* **Lemma 2.** `Φ_H` is unital, trace-preserving and completely positive; `Φ_H^{-1}` is not
  positive.
* **Lemma 3.** `Φ_H(X) = X ⟺ [H,X] = 0`; for self-adjoint `X`, `Φ_H(X²) = Φ_H(X)² ⟺ [H,X] = 0`;
  `Φ_H` is a spectral isometry on `M_n` iff `H` is scalar. The square defect has the exact trace
  `Σ ((a_i-a_j)/(a_i+a_j))² |X_{ij}|²`, sandwiched between
  `‖[H,X]‖_F²/(2a_max)²` and `‖[H,X]‖_F²/(2a_min)²`.
* **Theorem A.** `1/det H_κ ≤ det Σ_κ/det Σ_0 ≤ ρ(Q,L)/det H_κ` with
  `ρ(Q,L) = ∏_i Q̃_ii/det Q`; the left bound is an equality iff `[H,Q] = 0`. Consequently
  **expansion is confined to the bounded window `det H_κ < ρ(Q,L)`.**
* **Theorem A′.** The Oppenheim–Schur refinement gives `det(C∘Q̃)/det Q̃ ≥ 1 + det C (ρ-1)` with
  `det C = ∏_{i<j}((a_i-a_j)/(a_i+a_j))²` (Cauchy), hence the explicit **sufficient** condition
  `1 + det C (ρ-1) > det H_κ`, an identity for `n = 2`.
* **Normalization (two modes).** `bracket κ r = r²κ(anisotropy r - couplingCost κ)` with
  `anisotropy r = (r-1/r)²`, `couplingCost κ = 8(1+κ)²/κ`, and `couplingCost κ - 32 = 8(κ-1)²/κ`.
  Hence improvement is possible iff `(r-1/r)² > 32` iff `r > 3+2√2`. **`κ = 1` minimizes the
  coupling cost, so it suffices whenever any coupling works — but it does not maximize the
  volume**: the derivative at `κ = 1` is `((r-1/r)² - 32)/144 > 0` above threshold.
* **Theorem B (all `n`).** `ratio(0) = 1`, `ratio'(0) = -tr L`, and
  `ratio = Θ(κ^{-rank L})` — `κ^{-1}` for two modes, `κ^{-(n-1)}` for a connected `n`-node graph.
* **Theorem C (three modes).** Expansion occurs, with certified critical brackets
  `[8.278000767, 8.278100768]` (centre-node noise) and `[10.720241993, 10.720242994]` (end node).
  Since the two noise matrices have the same spectrum, **the threshold is not a function of
  `spec(Q)` and `spec(L)`.** The centre case is in closed form: expansion iff
  `(r-1/r)² > 8/κ + 30 + 36κ + 27κ²/2`, minimized at the positive root of `27κ³ + 36κ² - 8 = 0`,
  giving `κ_* = 0.4120226592…` and `r_* = 8.2780690232…`. Note `κ_* ≠ 1`: **the minimal-cost
  coupling being `1` is two-mode-specific.**

* **Theorems D–G (single correlated pair).** See §2 of this report's companion; formalized in
  `OUCorridor/SinglePair.lean` for the convexity, interval, uniqueness and floor statements.

* **Theorem H (component count).** If `Q̃` has `k` nonzero off-diagonal pairs then
  `{κ > 0 : det Σ_κ > det Σ_0}` has at most `k` components. `B·det(C∘Q̃)` is a polynomial of degree
  `≤ 2k` (`B = ∏_{E}(a_i+a_j)²`), the numerator of `ratio − 1` is `κA(κ)` with
  `A(0) = −4^k(det Q)(tr L) < 0` and all coefficients nonpositive from degree `2k`, so `A` has at
  most `2k` sign variations and at most `2k` positive roots; each component needs two.
  Formalized: the sign-variation and root-count step, and the `k = 3` sharpness statement
  (`ComponentCount.lean`). Attained at `k = 1, 2, 3` — the `k = 3` witness being
  `Q̃ = diag(Q₃, Q₆₀, Q₃₅₀₀)` against `L = diag(0,1000,0,1,0,1/10000)` with
  `Q_b = [[1,b],[b,1+b²]]`, where the ratio factors as `∏_j [1 + b_j²(a_jκ/(2+a_jκ))²]/(1+a_jκ)`
  and seven exact evaluations alternate. Attainment for `k ≥ 4` is untested.
* **Theorem J (necessary cost for every `c`, matching patterns).** With
  `s_* = max_E(λ_p+λ_q)`, at least `c` components requires
  `ρ_∞ > max{1 + 8(tr L)/s_*, [κ^{2c}](DB)/[κ^{2c}]B}`. The band disjunction collapses because
  `N ⪯ (det Q)ρ_∞B` coefficientwise (from the exact per-block numerator `4 + 4sκ + s²r_∞κ²`) and
  `q_m = [κ^m](DB)/[κ^m]B` is nondecreasing (Newton's inequalities on `B`). At `c = k = 1` the two
  terms are `9` and `5`, giving `η > 8` — Theorem F's exact threshold. For the three-block
  spectrum the floors are `9.0080008`, `8022.603677…`, `400400440125.444004…`. Formalized: the
  saturation envelope (`prod_one_add_mul_le`).
* **The box criterion (sufficient).** With `g(z) = (z/(2+z))²` increasing,
  `[1 + (b⁻)²g(a⁻κ)]/(1 + a⁺κ) ≤ F(κ) ≤ [1 + (b⁺)²g(a⁺κ)]/(1 + a⁻κ)`; products of these bounds
  certify whole boxes. Around `(a_j) = (1000, 1, 10⁻⁴, 10⁻⁸, 10⁻¹²)`,
  `(b_j) = (3, 60, 3500, 45000, 2000000)` with `a_j` free in `±0.1%` and `b_j` in `±0.25%`, eleven
  exact couplings give exactly five windows for all five blocks and exactly four for the first
  four. Formalized: the envelope (`blockRatio_mem_box`); the numerical bounds are exact arithmetic.
* **Theorem I (necessary cost).** Attaining `c = k` forces `[κ^{2k-1}]A > 0`, hence
  `ρ_∞ > T(E,L) := [κ^{2k}](DB)/[κ^{2k}]B`, and `ρ > T(E,L)` by Hadamard. For three disjoint
  `(0,a_j)` blocks this is `∏(1+η_i) > 125 + 40Σ_{i≠j}a_i/a_j + 4a₁a₂a₃Σa_i^{-3}`. At the witness's
  rates `T = 400400440125.444004…` against `ρ = 441122536010`, forcing `b₃ > 3334.538168…`.
  An exclusion test only, and not optimal (`η > 4` for one pair, against the exact `8`).
* **Sharpness of D–G.** `L = diag(0,100,1)`, `Q̃ = [[2035,3,45],[3,1,0],[45,0,1]]` (a connected
  weighted triangle, `299/6, 1/3, 1/3`) expands at `κ = 1/50`, contracts at `κ = 1/10`, and
  expands again at `κ = 1`, all exactly. Formalized as `witness_expansion_set_not_convex`.

**Limitations.** Theorems D–G need `Q̃` to have exactly one off-diagonal pair, and that hypothesis
is not removable; Theorem H's matrix construction and its final counting step are analytic, only
its combinatorial core and the `k = 3` witness are formalized, and attainment for `k ≥ 4` is
untested beyond `k = 5`; Theorems I and J are necessary only and not claimed optimal; Theorem J
covers only matching patterns, the coefficientwise domination being unproved for general patterns; the end-node three-mode model is not covered and its threshold stays bracketed; no general many-mode threshold;
`det H_κ < ρ` is necessary but not sufficient; the certified brackets are wider than the
numerical crossings because the certificate degrades at a near-double root. See [SCOPE.md](SCOPE.md).

## 3. New to the project vs. new to the literature

**New to the project, classical in the literature:** Lemma 1 (Löwner/Cauchy kernel, Bhatia);
positivity and infinite divisibility of `C` (Bhatia–Kosaki mean matrices); complete positivity
(Schur 1911); Lemma 3 (multiplicative domain of a Schur-product channel, Choi); `det Φ_H(Q) ≥
det Q` (**Oppenheim 1930** — this is the correction of the biggest misclassification made during
the investigation); the Hadamard ceiling.

**New to the project, assembled here:** the single-correlated-pair theorem (raised in review,
built on the determinant identity established here, verified and formalized here); the normalization identity and cost floor and their
consequences for the meaning of `34` and `3+2√2`; Theorem A as a model statement, with `ρ`
identified as the orientation-sensitive Hadamard ratio; Theorem B; and the measured gap between
Theorem A′ and the true three-mode thresholds (`7.52×` centre, `1.22×` end) with
`det C = Θ(κ⁶)` identified as its cause.

**Possibly new to the literature, not established:** Theorem C. Closest located prior art
(Barucca, Phys. Rev. E 90 (2014) 062129 and the related random-matrix work) treats the *spectrum*
of heterogeneous coupled-OU covariances with random couplings, not the determinant for a fixed
Laplacian. No determinant/volume threshold result was found; that is not evidence of novelty.
See [SOURCES.md](SOURCES.md).

## 4. The spectral-isometry paper

**Motivation only.** Colbrook–Stepaniants (arXiv:2610.40470v1) prompted the question "when does
`Φ_H` preserve algebraic structure?", which produced Lemma 3. No theorem, hypothesis or estimate
of that paper is used; Lemma 3 is proved from Lemma 1 directly, and its content coincides with the
classical multiplicative-domain theorem.

## 5. Many-mode outcome

**A general theorem now exists for one structured class** (Theorems D–G), with both repository
models as its two smallest instances, and its hypothesis is **sharp**: two correlated pairs at
separated damping scales can split the expansion set into two components (§7 of the derivation,
formalized). Outside that class the picture is:

Tractable, with a **refutation** as the headline: the two-mode constant does not extend, and
neither does the optimal coupling (`κ_* = 0.412…` for the centre-node three-mode model, not `1`).
What does extend is the *shape* (Theorem B: first-order decrease with slope `-tr L`,
`Θ(κ^{-rank L})` decay, bounded expansion window) and the sufficient condition of Theorem A′.

The reviewer-proposed test of Theorem A′ against the certified thresholds has now been run, and
it is **negative in a quantitative and informative way**: A′ first becomes satisfiable at
`r ≈ 62.26` (centre) and `r ≈ 13.12` (end), overshooting by `7.52×` and `1.22×`. The cause is that
`det C = 36κ⁶/[(2+κ)(2+3κ)(2+4κ)]² ≈ κ⁶/64` for small `κ`, so A′ carries almost no information in
the `κ ≈ 0.4`–`0.9` window where expansion actually occurs. A′ also degenerates entirely when two
damping rates coincide. Conversely no bound in the rate spread alone can do better, since `Q`
commuting with `H` gives ratio exactly `1`. **So a sharper bound must retain the off-diagonal
structure of `Q̃`, not merely `ρ` and the scalar `det C`.**

## 6. Files, commands, validation

Added: `OUCorridor/NormalizedLyapunov.lean`, `OUCorridor/SinglePair.lean`,
`OUCorridor/ComponentCount.lean`, `docs/normalized-lyapunov/` (this file,
`DERIVATION.md`, `SCOPE.md`, `SOURCES.md`), `verification/normalized-lyapunov/`
(`run_all.sh`, `verify.py`, `threemode2.py`, `threshold3.py`, `controls6.py`, `priorart7.py`,
`review8.py`, `singlepair9.py`, `multipair10.py`, `components11.py`, `sharp12.py`,
`cost13.py`, `boxes14.py`, `interp15.py`, `threemode.py` (scratch), `README.md`).
Modified: `OUCorridor.lean` (three imports), `README.md` (one new section plus a structure entry).
Unchanged: every existing Lean definition and proof, `verified/`, `paper/`.

Commands: `lake build` → *Build completed successfully (8716 jobs)*, no errors;
`lake env lean` on a temporary `#print axioms` file → `[propext, Classical.choice, Quot.sound]`
for all 55 new theorems (temporary file removed);
`verification/normalized-lyapunov/run_all.sh` → **144 / 144 checks passed**.
No `sorry`, `admit`, `axiom` or `native_decide` anywhere in `OUCorridor/`.

## 7. Next question

Eight previous candidates are closed: sharpening Oppenheim in the rate spread (it exists, it is
Theorem A′, and §5 measures how weak it is), the single-pair characterization (Theorems D–G), and
the general interval conjecture (**refuted**, §7 of the derivation).

The question posed last round — "which restrictions short of one correlated pair force one
interval?" — was answered in a better form than asked: not by finding a restriction, but by
bounding the damage. Theorem H says `k` pairs give at most `k` components, so the qualitative
picture is now complete for every `(L, Q)`. Both of that question's proposed candidate
restrictions were refuted along the way (star patterns, and the additive reading that motivated
them).

Sharpness at `k = 3` is now settled — affirmatively, and by disjoint blocks rather than the star
I had guessed at, whose feasibility question is still open but no longer load-bearing.

The band constraint has now been collapsed into a scalar cost bound (Theorem J), so the question
posed last round is answered — on matching patterns. That hypothesis is where the remaining gap
sits, and the reviewer has identified the precise missing step rather than leaving it open-ended.

**The replacement: extend Theorem J past the matching hypothesis.** It enters in *two* places, and
both need their own argument.

> **(a)** Does `N ⪯ (det Q) ρ_∞ B` hold coefficientwise when `Q̃` has an arbitrary off-diagonal
> pattern — overlapping pairs, cycles and all?
>
> **(b)** Is there a replacement for the product representation
> `G(κ) = ∏_j (1 + w_j u_j(κ))` with nonnegative weights `w_j` and `u_j ∈ [0,1]`, on which the
> single-window term `1 + 8(tr L)/s_*` depends?

(a) is proved here only by multiplying per-block inequalities, which needs disjointness; for a
general pattern `det(C ∘ Q̃)` no longer factors, cycle terms appear with signs, and the `(2k+1)`-term
comparison has to be made directly. (b) is a separate gap: `prod_one_add_mul_le` is an abstract
inequality about any such product, but it does **not** establish that a general network's normalized
gain *has* that form. The `q_m` monotonicity is the one genuinely pattern-independent ingredient,
being a property of `B` alone.

Two reasons (a) is the right first target. It is a *finite, checkable* statement at each `(n, k)`,
so it can be tested before being proved — and a counterexample would be as informative as a proof,
since it would show that `ρ_∞` cannot control the lower coefficients of `N` and that any general
coefficient-ratio bound needs finer data. It would also extend the coefficient-ratio half of
Theorem J on its own, leaving (b) as the only remaining obstacle.

Secondary, unchanged: whether the disjoint-block construction attains the ceiling for *every* `k`
(the §10 families give `k = 4, 5`; no infinite family is proved).
