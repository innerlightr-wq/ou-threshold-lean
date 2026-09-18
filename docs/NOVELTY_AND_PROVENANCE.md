# Novelty and provenance audit

*Zotero-assisted literature, provenance, stochastic-process and formalization audit,
September 2026. The governing standard is not whether another paper prints the number
`3 + 2√2`, but **whether an existing general covariance or control theorem specializes to this
threshold**.*

Paper under audit: `DeJesus2026ou` — *Heterogeneity-Driven Expansion and Synchronization Collapse
in Coupled Ornstein–Uhlenbeck Systems*, Zenodo,
[10.5281/zenodo.22059089](https://doi.org/10.5281/zenodo.22059089).

Bibliography: [`../references.bib`](../references.bib) — 12 entries, all with DOIs, every record
obtained from publisher metadata. The repository previously carried no bibliography.

---

## 1. Headline: one interpretive finding that matters more than the novelty question

**The algebra is correct and I verified every step. The `3 + 2√2` threshold is real. But the
phrase "synchronization collapse" is not supported by the model, and the audit recommends
retiring it.**

I solved the stationary Lyapunov equation independently and decomposed the system into normal
modes `S = X₁ + X₂`, `D = X₁ − X₂`:

```
Var(S) = (1 + r²)/2                       independent of κ
Var(D) = (1 + r²)/(2(1 + 2κ))             strictly DECREASING in κ, → 0
Cov(S,D) = Var(X₁) − Var(X₂) = (1 − r²)/(2(1 + κ))
```

`Var(D)` is the standard synchronization-error measure, and

```
Var(D)(κ) − Var(D)(0) = −κ(1 + r²)/(2κ + 1)  <  0   for every κ > 0 and every r.
```

**Diffusive coupling monotonically improves synchronization in this model, at every heterogeneity
level. Synchronization never collapses.** At `r = 10, κ* = 1.418` — the paper's own showcase point
— the numbers are:

| κ | det Σ (= `A`) | trace Σ | Var(X₁−X₂) | corr(X₁,X₂) |
|---|---|---|---|---|
| 0 | 25.000 | 50.500 | 50.500 | 0.000 |
| 0.5 | 46.531 | 37.875 | 25.250 | 0.679 |
| **1.418 = κ\*** | **61.435** | 31.832 | **13.163** | **0.766** |
| 3 | 52.795 | 28.857 | 7.214 | 0.830 |
| 10 | 25.298 | 26.452 | 2.405 | 0.923 |

At the coupling that maximises `A`, the synchronization error is **3.8× smaller** than uncoupled
and the correlation has risen from 0 to 0.77. The determinant grows while the trace *falls*.

**Why:** the exact decomposition is

```
det Σ = [ Var(S)·Var(D) − (Var X₁ − Var X₂)² ] / 4
      = (1/4)[ (1+r²)²/(4(1+2κ)) − (1−r²)²/(4(1+κ)²) ]
```

Both terms decrease in κ. The *subtracted* term is a heterogeneity penalty, and when `r` is large
it decays faster (as `(1+κ)^-2`) than the product term (as `(1+2κ)^-1`). So `det Σ` rises because
**coupling equalizes the two marginal variances, removing a heterogeneity-induced near-degeneracy
of the covariance ellipse** — the ellipse becomes rounder. That is the opposite of desynchronization.

**Recommended reframing.** `A(κ,r) > A(0,r)` is exactly equivalent to an increase in the stationary
**Gaussian differential entropy**, since `h = ½ log((2πe)² det Σ)` (`CoverThomas2005`). The
defensible statement is *heterogeneity-driven entropy/volume expansion*, or *decorrelation-free
volume expansion* — not synchronization collapse. This is an **interpretive** correction: no
theorem, proof, or number changes.

## 2. Verdict on novelty

| question | answer |
|---|---|
| Is the algebra correct? | **Yes** — verified symbolically, end to end |
| Is `A` a standard object? | **Yes** — `A = det Σ` exactly, i.e. **Wilks' generalized variance** (`Wilks1932`) |
| Is the stationary covariance standard? | **Yes** — the continuous Lyapunov equation `MΣ + ΣMᵀ + Q = 0`, textbook for 2×2 (`Gardiner2004`, `Vatiwutipong2019`) |
| Was `3 + 2√2` found in the literature for this problem? | **No** |
| Does a stronger known theorem imply it? | **Not found.** No general 2×2-Lyapunov, network-coherence or H₂ theorem located specializes to it — because the *objective* (maximize `det Σ` over coupling) is not the objective that literature optimizes. See §5 |
| Is it a condition-number criterion? | **Almost, but not as stated** — see §4. `cond(Q) = r²`, so the threshold is `cond(Q) > (3+2√2)² = 17 + 12√2 ≈ 33.97`, **not** `cond(Q) > 3+2√2` |
| Is it elementary once set up? | **Yes** — a discriminant condition on a quadratic in κ |
| Is the Lean formalization novel? | **As a domain application, plausibly yes**; as mathematics it formalizes real-algebra facts, and it explicitly does *not* formalize the stochastic model |

**Overall: `ELEMENTARY CONSEQUENCE` of standard OU/Lyapunov algebra, apparently unstated, with a
`FORMALIZATION OF KNOWN RESULT` contribution and one interpretation requiring correction.**
Manuscript revision: **C — moderate framing revision.** The threshold survives untouched; the
synchronization narrative does not.

## 3. Ancestry of the `3 + 2√2` threshold

Every step re-derived independently in this audit.

```
coupled OU:  dX = M X dt + B dW,  M = [[-(1+κ), κ],[κ, -(1+κ)]],  Q = BBᵀ = diag(1, r²)
      │                                                            [STANDARD MODEL]
      ▼  stationary Lyapunov equation  MΣ + ΣMᵀ + Q = 0
Σ entries: s₁,s₂,c in closed form                                  [STANDARD, textbook 2×2]
      │
      ▼  A := det Σ
A(κ,r) = (κ²r⁴ + 2κ²r² + κ² + 8κr² + 4r²) / (16(κ+1)²(2κ+1))       [VERIFIED = det Σ exactly]
      │                                                             A(0,r) = r²/4
      ▼  A − A₀ = κ·B(κ,r) / (16(κ+1)²(2κ+1)),  denominator > 0
sign reduces to B(κ,r) = −8r²κ² + (r⁴−18r²+1)κ − 8r²               [ELEMENTARY ALGEBRA]
      │
      ▼  ∃κ>0 with B>0  ⟺  discriminant > 0  (B has negative leading coeff, B(0)<0)
discr = (r⁴−18r²+1)² − 256r⁴ = (r²−1)²(r⁴−34r²+1)                  [ELEMENTARY]
      │
      ▼  r⁴ − 34r² + 1 = (r²−6r+1)(r²+6r+1)                        [see §6 — factors further
      │                                                             than the repo states]
      ▼  r² − 6r + 1 > 0 for r ≥ 1
r > 3 + 2√2                                                         [THE THRESHOLD]
```

| step | fact | known? | source | Lean? | novel? |
|---|---|---|---|---|---|
| 1 | coupled OU model, stability for κ ≥ 0 | **yes** | `UhlenbeckOrnstein1930`, `Gardiner2004` | **no** | no |
| 2 | stationary covariance solves the Lyapunov equation | **yes** | `Gardiner2004`, `Vatiwutipong2019`, `Antoulas2005` | **no** | no |
| 3 | closed-form 2×2 solution | **yes**, textbook | `Gardiner2004` | **no** | no |
| 4 | `A = det Σ` = generalized variance | **yes** | `Wilks1932` | **no** (taken as a definition) | no |
| 5 | `A − A₀ = κB/denominator` | elementary | — | **yes** (`volume_sub_volume0`) | derivation |
| 6 | reduction to `B > 0` | elementary | — | **yes** (`volume_gt_iff_bracket_gt`) | derivation |
| 7 | discriminant factorization | elementary | — | **yes** (`discr_factor`) | derivation |
| 8 | quartic ⟺ `r > 3+2√2` | elementary radical algebra | — | **yes** (`quartic_gt_iff_gt_threshold`) | derivation |
| 9 | ∃κ>0 ⟺ threshold | elementary; explicit witness κ=1 | — | **yes** (`exists_bracket_pos_iff_threshold`) | **the assembly** |
| 10 | equivalence to entropy increase | immediate from `h = ½log((2πe)²detΣ)` | `CoverThomas2005` | **no** | interpretation |

**Where content enters: steps 5–9, all elementary, all Lean-verified. Steps 1–4 are standard and
are *not* formalized — the Lean development starts at step 5 by taking `A` as a definition.**

## 4. Is it a condition-number criterion? (a trap worth flagging)

`Q = diag(σ₁², σ₂²) = diag(1, r²)`, so `cond(Q) = max(r², 1/r²) = r²` for `r ≥ 1`.
The threshold `r > 3 + 2√2` therefore reads

```
cond(Q) > (3 + 2√2)² = 17 + 12√2 ≈ 33.9706
```

**Anyone restating the threshold as "`cond(Q) > 3+2√2`" would be wrong by a square.** The
repository's `r` is the **noise-amplitude** ratio (`σ₁ = 1, σ₂ = r`), not the variance ratio. The
README's definition is unambiguous, but the distinction should be stated explicitly because
`r` is called a "noise-heterogeneity ratio", which a reader may naturally read as a variance ratio.

## 5. Why no prior theorem specializes to it

The literature optimizes different objectives over coupling:

* **network coherence / H₂** (`BamiehEtAl2012`) minimizes `tr Σ` (or the variance of deviations
  from average) — a *trace* functional, and here the trace is **monotonically decreasing** in κ,
  so that optimization is trivial and has no threshold;
* **stochastic synchronization** (`PikovskyEtAl2001`, `TeramaeTanaka2004`) studies `Var(D)` or
  phase coherence — also monotone here, again no threshold;
* **two-temperature linear Langevin systems** (`DotsenkoEtAl2013`) and the **Brownian gyrator**
  (`FilligerReimann2007`) have exactly this structure — two coupled linear degrees of freedom with
  unequal noise temperatures — and compute stationary covariances, heat flux and torque. They are
  the **closest physical prior art**. But their questions are about *currents* and *rotation*, not
  about maximizing `det Σ` over coupling strength.

So the threshold is unstated because the *question* — "for which heterogeneity can coupling
increase the covariance determinant?" — is not one that literature asks. That is a real
observation, and it is also why the result is modest: the objective is chosen, not forced.

**Caveat on the gyrator comparison:** the Brownian gyrator requires coupling *in the potential*
between coordinates driven at different temperatures, which this model has (`κ` couples the two
coordinates, `Q` is anisotropic). The models are genuinely close, and the audit did **not**
establish that no gyrator paper contains the determinant-maximizing threshold. Tagged
`uncertain-more-search`; this is the audit's main gap.

## 6. Two mathematical observations the repository could use

**6.1 The quartic factors over ℚ, and the threshold is really a quadratic condition.**

```
r⁴ − 34r² + 1 = (r² − 6r + 1)(r² + 6r + 1)
```

For `r ≥ 1` the second factor is positive, so the criterion is simply

```
r² − 6r + 1 > 0   ⟺   r + 1/r > 6   ⟺   r > 3 + 2√2 .
```

The repository's `quartic_factor` factors instead over ℝ as `(r² − θ²)(r² − θ̄²)` with
`θ = 3+2√2`. Both are correct; the rational factorization is simpler and **makes the reciprocal
symmetry manifest**: `r + 1/r` is invariant under `r → 1/r`, which is exactly the relabelling
symmetry `X₁ ↔ X₂`. The clean symmetric statement is

```
∃κ>0 : A(κ,r) > A(0,r)   ⟺   max(r, 1/r) > 3 + 2√2   ⟺   r + 1/r > 6 ,
```

and this form removes the need for the `r ≥ 1` hypothesis. Recommended as a remark; formalizing it
would be a two-line addition.

**6.2 `κ*` is a cubic root with no closed form.** Differentiating `A`:

```
−(r²+1)² κ³ + (r²−4r+1)(r²+4r+1) κ² + (r²−4r+1)(r²+4r+1) κ − 4r² = 0
```

Note the κ² and κ¹ coefficients coincide — a structure worth remarking on. At `r = 10` the roots
are `−0.6197, 0.04462, 1.41819`; the optimum is the largest, `κ* = 1.418186`, confirming the
paper's `≈ 1.418`. There are **two positive critical points** (a local minimum then the maximum),
because `A′(0) < 0` always: coupling *initially decreases* the determinant even above threshold.
That is a genuinely interesting feature and is not mentioned in the README.

## 7. Numerical reproduction (`r = 10`)

| quantity | claimed | reproduced | match |
|---|---|---|---|
| `κ*` | ≈ 1.418 | **1.418186** | ✓ |
| `A(κ*,10)` | — | **61.434822** | — |
| `A(0,10)` | `r²/4 = 25` | **25.000000** | ✓ |
| `A/A₀` | ≈ 2.4574 | **2.457393** | ✓ |
| threshold | `3+2√2` | **5.828427** | ✓ |
| as variance ratio | — | `17+12√2 = 33.970563` | — |

**Numerical illustration, not theorem** — and `r = 10` sits well above threshold, so it exhibits
the phenomenon but says nothing about sharpness.

## 8. Lean formalization audit

| theorem | class | mathematical ancestor |
|---|---|---|
| `volume`, `volume0`, `bracket`, `threshold`, `discr` | definitions | `A` is `det Σ`, **asserted not derived** |
| `volume_zero` | **A: standard algebra** | `A(0,r) = r²/4` |
| `denominator_pos` | **D: helper** | positivity of `16(κ+1)²(2κ+1)` |
| `volume_sub_volume0` | **A: standard algebra** | the `κB/denominator` identity |
| `volume_gt_iff_bracket_gt` | **A** | sign transfer across a positive denominator |
| `discr_factor`, `bracket_one` | **A** | polynomial identities (`ring`) |
| `sqrt_two_pos/sq`, `threshold_pos/ge_one/sq/quartic`, `conjugate_sq`, `threshold_conjugate_mul`, `sqrt_two_gt_four_thirds`, `conjugate_sq_lt_one` | **D: radical helpers** | `(3+2√2)² = 17+12√2`, etc. |
| `quartic_factor`, `factor_two_pos` | **A** | factorization over ℝ in `r²` |
| `quartic_gt_iff_gt_threshold` | **C: the repo-specific reduction** | `r⁴−34r²+1 > 0 ⟺ r > 3+2√2` for `r ≥ 1` |
| `discr_sos` | **C** | sum-of-squares certificate |
| `quartic_pos_of_exists_bracket_pos` | **C** | forward direction |
| `exists_bracket_pos_iff_threshold` | **C** | iff, with explicit witness `κ = 1` |
| `exists_volume_improvement_iff_threshold` | **C: the central theorem** | the threshold statement |

**Verified at kernel level in this audit** (stronger than the README's grep):

```
'OUCorridor.exists_volume_improvement_iff_threshold' depends on axioms:
    [propext, Classical.choice, Quot.sound]
```

No `sorryAx`, no custom axiom — likewise for `exists_bracket_pos_iff_threshold`,
`quartic_gt_iff_gt_threshold` and `discr_sos`. `lake build` reproduced
**"Build completed successfully (8710 jobs)"**, matching the README's recorded count, on
Lean 4.33.1 with mathlib `0df444a360ea`. Only style-linter warnings (short copyright header,
docstring placement, one deprecated `push_neg`).

**What Lean does and does not prove.** The README's scope statement is **accurate and should be
kept verbatim**: the development formalizes the *scalar real-algebra threshold*, taking `A(κ,r)` as
a definition. It does **not** formalize the SDE, the stationary distribution, the Lyapunov equation,
or the derivation of `A`. So the chain "OU model ⟹ `A = det Σ`" — steps 1–4 above — is
**unformalized**, and it is precisely the step where a reader would want machine checking, since
that is where the stochastic content lives. This audit verified it symbolically instead, and the
verification passed exactly.

**Formalization prior art:** no Lean/mathlib formalization of continuous Lyapunov equations, OU
processes, or this threshold was located. mathlib has the real-algebra and `Real.sqrt` machinery the
project uses, but no stochastic-process layer to build on — which explains, and justifies, the
scoping.

## 9. Claim-strength audit

| phrase | where | verdict |
|---|---|---|
| **"Synchronization Collapse"** | paper title, README | **NEEDS QUALIFICATION / REMOVE** — the model's synchronization error decreases monotonically in κ. See §1. This is the audit's one substantive finding |
| "Expansion" | title, README | **NEEDS QUALIFICATION** — the *determinant/entropy* expands; the *trace* contracts. Say which |
| "exact threshold" | README | **SAFE** — it is exact |
| "if and only if" | central result | **SAFE** — verified, and Lean-checked |
| "formally verified", "machine-checked" | throughout | **SAFE** — and the scope section correctly limits it |
| "covariance-volume functional" | README | **NEEDS CITATION** — this is Wilks' generalized variance; say so |
| "noise-heterogeneity ratio `r`" | README | **NEEDS QUALIFICATION** — `r` is the *amplitude* ratio; the variance ratio threshold is `17+12√2` |
| "no `sorry`, `admit`, or explicit custom `axiom`" | README | **SAFE**, and now confirmed by `#print axioms` rather than grep |
| "new", "novel", "first", "universal", "phase transition", "critical" | — | **absent** from the README |

The README makes no novelty claim at all — it is scoped as a "formal verification companion". Its
claim strength is otherwise well calibrated; the problem is in the *paper title's* interpretation.

## 10. What should change

1. **Retire "synchronization collapse"** from the framing, or restrict it to a precisely defined
   quantity that actually collapses. Nothing in this model does. Recommended replacement:
   *heterogeneity-driven expansion of stationary covariance volume (equivalently Gaussian
   entropy)*.
2. **Name `A` as Wilks' generalized variance** `det Σ`, and cite it.
3. **State that `r` is the amplitude ratio**, and give the equivalent variance-ratio threshold
   `17 + 12√2`.
4. **Cite the standard chain** for steps 1–4: `UhlenbeckOrnstein1930`, `Gardiner2004`,
   `Vatiwutipong2019` for the model and Lyapunov solution; `Wilks1932`; `CoverThomas2005` for the
   entropy equivalence.
5. **Acknowledge the closest physical prior art** — `DotsenkoEtAl2013`, `FilligerReimann2007` —
   and say explicitly that those works study currents rather than covariance volume.
6. Optionally add the remarks of §6: the rational factorization / reciprocal-symmetric form
   `r + 1/r > 6`, and that `A′(0) < 0` so coupling is initially harmful even above threshold.
7. **Fix the README's mangled markdown** — every formula is wrapped in
   `$begin:math:text$ … $end:math:text$` escape artifacts, which makes the document nearly
   unreadable on GitHub. This is a rendering defect, not a content one.

None of this touches a theorem, a proof, or a number.

## 11. Repository hygiene

* `OUCorridor/Basic.lean` contains only `def hello := "world"` — a `lake new` leftover, imported by
  `OUCorridor.lean` and listed in the README's structure.
* `verified/` holds **byte-identical** copies of the two proof files (verified by `diff`), i.e. a
  genuine frozen record rather than a diverging duplicate. Nothing imports it, so there is no
  shadowing risk.
* `verified/SHA256SUMS.txt` uses **repository-root-relative** paths, so `sha256sum -c` must be run
  from the root, not from inside `verified/`. From the root all four hashes verify **OK**. Worth one
  line in the README.
* `lake update` did not modify any tracked file.

## 12. Unresolved

1. Whether any Brownian-gyrator or two-temperature paper contains a determinant-maximizing
   coupling threshold. The models coincide; only the objective differs. **Main gap.**
2. Whether the threshold survives unequal damping (`a₁ ≠ a₂`) or correlated noise. Not examined —
   the theorem is stated only for the equal-relaxation, independent-noise, symmetric-coupling case,
   and should not be called universal beyond it.
3. The second threshold `r_D* = 2 + √3` (residual-variance) is mentioned in the README as
   unformalized and was not audited here.
