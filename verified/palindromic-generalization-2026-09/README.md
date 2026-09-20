# Verification snapshot — trace-normalized palindromic generalization (September 2026)

A **fourth**, separate verification record. It does not replace `verified/`,
`verified/cross-threshold-2026-09/` or `verified/active-plane-2026-09/`; all three are left
untouched and all three still verify against the live sources.

## What this snapshot records

The generalization of the active-plane theorem, in `OUCorridor/ActivePlaneGeneral.lean`:

- `det_genCov_eq` — the sharp identity `4 D₁ D₂ det Σ = det Q + ν² q₁₂²` for an **arbitrary
  symmetric** forcing `Q` on the plane. No rank-one, no isotropy, no positivity hypothesis.
- `det_affineCov_eq` — for `Q(τ) = q_b I + (τ−1)H` with `H` symmetric of any rank,
  `4 D₁ D₂ det Σ(τ) = q_b² + q_b (tr H)(τ−1) + K(τ−1)²`, `K = det H + ν² h₁₂²`.
- `affine_palindromic_iff_trace` — for `q_b > 0` the determinant polynomial is palindromic in
  `τ` **iff `tr H = q_b`**. Rank one is sufficient, not necessary.
- `det_affineCov_traceNormalized`, `normalizedAffineDet_eq`, `normalizedAffineDet_div_eq` —
  the collapse to `K(τ−1)² + q_b²τ` and the reciprocal reduction in `w = τ + 1/τ`.
- `affineCoeff_nonneg_of_posSemidef`, `det_affineForcing_pos_of_posSemidef` — the admissibility
  boundary: `K ≥ 0` and `Q(τ) ≻ 0` for all `τ > 0` when `H` is positive semidefinite.
- `det_activeCov_palindromic_of_general`, `affineCov_rankOne`, `affineForcing_rankOne` — the
  previously verified rank-one isotropic theorem recovered as a specialization.
- `affineForcing_complement`, `complementForcing_involutive`, `complementForcing_trace`,
  `complementForcing_traceNormalized`, `complementForcing_det`, `affineCoeff_complement` — the
  complementary-forcing involution `H* = q_b I − H`. The reciprocal transform
  `τ · Q_H(1/τ) = Q_{H*}(τ)` holds unconditionally; `tr H* = 2q_b − tr H`, so the
  trace-normalized family is exactly the family closed under it, and on that family both
  `det H − h₁₂²`-type data and the coefficient `K` are invariant.
- `complementForcing_fixed_iff` — closure is not fixedness: the only forcing fixed by the
  involution is the isotropic `H = (q_b/2) I`.
- `complementForcing_rankOne` — on a rank-one `H = q_b e eᵀ` the involution is exactly the
  exchange `e ↔ e^⊥`, so the rank-one duality is a specialization, not a separate mechanism.

`OUCorridor/ActivePlane.lean` is **unchanged**; the older theorem stands exactly as verified.

## Environment

```text
Lean 4.33.1
x86_64-unknown-linux-gnu
Lean commit: 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
mathlib:     0df444a360eaa60ab8c11dca51a86af692955474
```

## Result

```text
Build completed successfully (8716 jobs).
```

The unfinished-proof grep returned no matches, and all **28** audited theorems depend only on
`propext`, `Classical.choice` and `Quot.sound` — no `sorryAx`, no custom axiom.

## Checking

From this directory:

```bash
sha256sum -c SHA256SUMS.txt
```
