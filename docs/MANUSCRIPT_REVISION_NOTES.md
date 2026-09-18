# Manuscript Revision Notes

**Status: notes only. Nothing has been published, deposited, or re-versioned.**

The deposited paper (Zenodo [10.5281/zenodo.22059089](https://doi.org/10.5281/zenodo.22059089)) is
unchanged. No new manuscript version has been prepared, no Zenodo record has been edited, and the
existing PDF has not been overwritten. This file exists so that the September 2026 audit's
conclusions are not lost before the author decides whether to revise.

Classification carried over from the audit, unchanged:

> **C — moderate framing revision.**
> The mathematics is correct and the threshold is exact. What needs revising is the *interpretation*
> of what expands and what collapses. No theorem, proof, or numerical value is affected.

The supporting evidence is in [`NOVELTY_AND_PROVENANCE.md`](NOVELTY_AND_PROVENANCE.md); this file
only lists what a revision would change.

---

## 1. The one substantive item

**The paper's "synchronization collapse" does not occur in the paper's own model.**

For the equal-relaxation, symmetric-coupling, independent-noise system, the stationary variance of
the difference mode is

```
Var(X₁ − X₂) = (1 + r²) / (2(1 + 2κ))
```

which is strictly decreasing in `κ` for every `r` and every `κ > 0`. Coupling monotonically
*improves* synchronization — including at and above `r = 3 + 2√2`, and including at the maximizing
coupling `κ*`. The expansion of `det Σ` and the improvement of synchronization happen together;
they are not a trade-off.

The determinant nevertheless grows because

```
det Σ = [ Var(S)·Var(D) − (Var X₁ − Var X₂)² ] / 4,     S = X₁+X₂,  D = X₁−X₂
```

and the heterogeneity penalty `(1 − r²)² / (4(1 + κ)²)` decays faster in `κ` than the product term
does. That is the correct mechanism, and it is a statement about generalized variance, not about
phase coherence.

**Revision required:** replace every claim of synchronization loss with the quantity that actually
expands — the stationary generalized variance `det Σ`, equivalently the stationary Gaussian entropy
`h = ½ log((2πe)² det Σ)`. Both readings are defensible and exact; "collapse" is not.

## 2. Title

The title's second clause carries the incorrect claim. Recommended replacements are listed in §14
of the audit document. **The title is not changed here**: it belongs to a published deposit, and
renaming it is the author's decision.

## 3. Four wording items

1. **Name the objective.** `A(κ,r) = det Σ` is Wilks' generalized variance (Wilks 1932). Say so and
   cite it, rather than coining "covariance-volume functional".
2. **Say which heterogeneity ratio.** `r` is the noise-*amplitude* ratio. In noise variances, or
   equivalently as a condition number of `Q = diag(1, r²)`, the threshold is
   `cond(Q) > (3+2√2)² = 17 + 12√2 ≈ 33.97`. Writing `cond(Q) > 3 + 2√2` would be wrong by a
   square.
3. **Distinguish determinant from ellipse area.** The concentration ellipse's area is
   `π√(det Σ)`, proportional to `√det Σ`. The two give the same threshold, since `√·` is strictly
   increasing, but they are not the same quantity and their growth factors differ.
4. **Do not call the threshold universal.** It is exact for two components with equal damping,
   symmetric coupling, and independent additive noises, in the stationary regime. Unequal damping,
   correlated noise, more components, and transients are all unexamined.

## 4. Two optional additions

Both are elementary and neither changes a result.

1. **Reciprocal-symmetric form.** Since `r⁴ − 34r² + 1 = (r² − 6r + 1)(r² + 6r + 1)` and the second
   factor is positive for `r ≥ 1`, the criterion is `r + 1/r > 6`, i.e. `max(r, 1/r) > 3 + 2√2`.
   This is manifestly invariant under relabelling the two components and needs no `r ≥ 1`
   hypothesis.
2. **Non-monotonicity in the coupling.** `A′(0) < 0` for every `r`, so weak coupling *reduces* the
   generalized variance even above threshold; there are two positive critical points, a local
   minimum then the maximum. The maximizer solves a cubic with no simple closed form and should be
   quoted numerically (`κ* ≈ 1.418186` at `r = 10`, where `A/A₀ ≈ 2.457393`).

## 5. What must not change

* Every theorem, proof, and numerical value, including the threshold `3 + 2√2` itself.
* The Lean development, its definitions, and its identifiers.
* The scope statement: the formalization covers the scalar real-algebra threshold, and claims no
  end-to-end verification of the stochastic differential equation.
