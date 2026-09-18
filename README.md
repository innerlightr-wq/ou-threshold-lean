# OU Threshold — Lean 4 Formal Verification Companion

A machine-checked formalization, in Lean 4 with mathlib, of the central algebraic threshold theorem from:

> Elias De Jesús (2026). *Heterogeneity-Driven Expansion and Synchronization Collapse in Coupled Ornstein–Uhlenbeck Systems.*

The paper studies two diffusively coupled Ornstein–Uhlenbeck processes and shows that, in the equal-relaxation normalization, the stationary **generalized variance** $A(\kappa,r) = \det \Sigma$ can exceed its uncoupled value $A(0,r)$ at some positive coupling strength if and only if the noise-heterogeneity ratio $r$ exceeds the exact threshold

$$
r^{*} = 3 + 2\sqrt{2}.
$$

This repository formalizes and machine-checks that threshold statement as a result in exact real algebra.

Equivalently, and more symmetrically, the criterion is

```
r + 1/r > 6      i.e.      max(r, 1/r) > 3 + 2*sqrt(2)
```

since `r^4 - 34r^2 + 1 = (r^2 - 6r + 1)(r^2 + 6r + 1)` and the second factor is positive for
`r >= 1`. This form is manifestly invariant under `r -> 1/r`, the relabelling symmetry of the two
components, and needs no `r >= 1` hypothesis.

> **Scope:** This is a formal verification companion, not a formalization of the paper's complete stochastic-process content. See [Scope of the Formalization](#scope-of-the-formalization).

> **Provenance note (September 2026 audit).** A literature and provenance audit is recorded in
> [`docs/NOVELTY_AND_PROVENANCE.md`](docs/NOVELTY_AND_PROVENANCE.md), with verified references in
> [`references.bib`](references.bib); what a future manuscript revision would need to say is noted
> in [`docs/MANUSCRIPT_REVISION_NOTES.md`](docs/MANUSCRIPT_REVISION_NOTES.md). Three points belong
> up front:
>
> 1. The functional `A` is exactly `det Σ`, the stationary covariance determinant — **Wilks'
>    generalized variance**. The audit re-derived the stationary covariance from the Lyapunov
>    equation and confirmed the definition used here matches it exactly.
> 2. `r` is the **noise-amplitude** ratio (`σ₁ = 1`, `σ₂ = r`). The equivalent **variance**-ratio
>    threshold is `(3+2√2)² = 17 + 12√2 ≈ 33.97`, and the condition number of
>    `Q = diag(1, r²)` is `r²`, so the criterion is `cond(Q) > 17 + 12√2` — not `> 3+2√2`.
> 3. The audit found that **the synchronization error decreases monotonically in the coupling**:
>    `Var(X₁−X₂) = (1+r²)/(2(1+2κ))`. Generalized-variance expansion therefore does **not** indicate
>    loss of synchronization in this model; the two occur together. The defensible reading of
>    `A(κ,r) > A(0,r)` is an increase in stationary Gaussian **entropy**, since
>    `h = ½ log((2πe)² det Σ)`. See [Model Scope and Interpretation](#model-scope-and-interpretation)
>    below, and §1 of the provenance document.

---

## Central Result

For $r \ge 1$,

$$
\boxed{
\left(\exists\,\kappa>0,\;
A(\kappa,r)>A(0,r)\right)
\iff
r>3+2\sqrt{2}
}
$$

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

$$
a_1=a_2=1,\qquad \sigma_1=1,\qquad \sigma_2=r,
$$

define

$$
A(\kappa,r)
=
\frac{
\kappa^2r^4
+2\kappa^2r^2
+\kappa^2
+8\kappa r^2
+4r^2
}{
16(\kappa+1)^2(2\kappa+1)
},
$$

with

$$
A(0,r)=\frac{r^2}{4}.
$$

Then, for every $r\ge1$, some positive coupling strictly increases the generalized variance over its uncoupled value if and only if

$$
r>3+2\sqrt2.
$$

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

## Model Scope and Interpretation

### The model the threshold belongs to

The threshold is exact, but it is a statement about one specific model rather than a general
principle. The assumptions are:

- exactly **two** components;
- **equal** relaxation rates ($a_1 = a_2 = 1$ after normalization);
- **symmetric, diffusive** coupling — the same $\kappa$ in both directions;
- **independent additive** noises with no cross-correlation, so $Q = BB^{\mathsf T} = \mathrm{diag}(1, r^2)$ is diagonal;
- the **stationary Gaussian** law of the linear system, i.e. the $\Sigma$ solving the continuous
  Lyapunov equation $M\Sigma + \Sigma M^{\mathsf T} + Q = 0$.

Nothing here is claimed for three or more components, unequal damping, asymmetric or directed
coupling, correlated noise, multiplicative noise, or transient (non-stationary) behaviour. The
number $3 + 2\sqrt{2}$ should be read as exact **within this normalization**, not as universal.

### What `A` measures

$A(\kappa,r) = \det \Sigma$ is the **generalized variance** in the sense of Wilks (1932): the
determinant of the stationary covariance matrix. Two neighbouring quantities are routinely
conflated with it, and are kept distinct here.

- The area of the concentration ellipse $\{x : x^{\mathsf T}\Sigma^{-1}x \le 1\}$ is
  $\pi\sqrt{\det \Sigma}$ — proportional to $\sqrt{\det \Sigma}$, **not** to $\det \Sigma$.
- The differential entropy of the stationary bivariate Gaussian is

  $$
  h(\Sigma) = \tfrac{1}{2}\log\!\big((2\pi e)^{2}\det \Sigma\big),
  $$

  which is the standard Gaussian entropy formula (Cover & Thomas, *Elements of Information
  Theory*, 2nd ed., Ch. 8), recorded here purely as an interpretation — **not** as a new theorem
  of this repository.

Since $x \mapsto \sqrt{x}$ and $x \mapsto \tfrac12\log((2\pi e)^2 x)$ are both strictly increasing
on $(0,\infty)$, these three quantities order configurations identically, so $r > 3 + 2\sqrt{2}$ is
equally the threshold for ellipse area and for stationary entropy. They are **monotonically
equivalent, not equal**, and must not be interchanged in any statement about magnitudes, rates, or
ratios — an expansion factor of $2.457$ in $\det \Sigma$ is a factor $1.567$ in ellipse area and an
additive $\tfrac12\log 2.457 \approx 0.449$ nat in entropy.

### Heterogeneity: amplitude ratio versus variance ratio

$r$ is the **noise-amplitude** ratio ($\sigma_1 = 1$, $\sigma_2 = r$). The corresponding statement
in terms of noise *variances* — equivalently the condition number of the diffusion matrix, since
$\mathrm{cond}(Q) = r^2$ for $Q = \mathrm{diag}(1, r^2)$ — is

$$
\mathrm{cond}(Q) > (3 + 2\sqrt{2})^{2} = 17 + 12\sqrt{2} \approx 33.9706 .
$$

Writing $\mathrm{cond}(Q) > 3 + 2\sqrt{2}$ would be wrong by a square. (The symbol $\kappa$ is
reserved throughout this repository for the coupling strength, so the condition number is written
$\mathrm{cond}(\cdot)$ and never $\kappa(\cdot)$.)

### The optimal coupling has no simple closed form

Above threshold, the coupling maximizing $A(\cdot,r)$ is a root of the cubic

$$
-(r^2+1)^2\kappa^3 + (r^2-4r+1)(r^2+4r+1)\kappa^2 + (r^2-4r+1)(r^2+4r+1)\kappa - 4r^2 = 0
$$

(the $\kappa^2$ and $\kappa^1$ coefficients coincide). It is therefore algebraic of degree three in
general, with no simple closed form, and is best quoted numerically. Two consequences matter for
interpretation:

- $A$ is **not** monotone increasing in the coupling. Indeed $A'(0) < 0$ for every $r$, because the
  cubic's constant term is $-4r^2 < 0$: weak coupling *decreases* the generalized variance even
  above threshold. There are two positive critical points — a local minimum first, then the
  maximum — so the expansion never occurs at arbitrarily weak coupling: any $\kappa$ witnessing it
  is bounded away from $0$.
- At $r = 10$ the cubic's roots are $-0.6197$, $0.04462$ and $1.41819$; the maximizer is the
  largest, $\kappa^{*} \approx 1.418186$, where $A(\kappa^{*},10) \approx 61.4348$ against
  $A(0,10) = 25$, a ratio $A/A_0 \approx 2.457393$.

The formal result asserts only the *existence* of some $\kappa > 0$ with $A(\kappa,r) > A(0,r)$; it
says nothing about the location or value of the maximizer.

### Terminology: "synchronization collapse"

The paper's title uses the phrase *synchronization collapse*. The audit found that the
synchronization error is monotonically **decreasing** in the coupling, for every $r$ and every
$\kappa > 0$:

$$
\operatorname{Var}(X_1 - X_2) = \frac{1 + r^2}{2(1 + 2\kappa)} .
$$

Coupling therefore always improves synchronization in this model — including in exactly the regime
where $\det \Sigma$ expands, so the two effects coexist rather than trading off. Accordingly this
repository's prose describes the phenomenon as **coupling-induced generalized-variance expansion**
(equivalently, **coupling-induced stationary-entropy expansion**), and uses the paper's original
phrase only when citing the paper's title. The Lean identifiers (`volume`, `volume0`) are left
unchanged, so the formal statements are unaffected by this wording change.

---

## What Is Formally Verified

The central result is supported by the following machine-checked theorem chain:

1. **`volume_zero`**  
   Verifies
   $$
   A(0,r)=\frac{r^2}{4}.
   $$

2. **`volume_sub_volume0`**  
   Establishes the exact identity expressing
   $$
   A(\kappa,r)-A(0,r)
   $$
   as $\kappa B(\kappa,r)$ divided by the relevant denominator.

3. **`denominator_pos`**  
   Proves
   $$
   16(\kappa+1)^2(2\kappa+1)>0
   $$
   for $\kappa\ge0$.

4. **`volume_gt_iff_bracket_gt`**  
   For $\kappa>0$,
   $$
   A(\kappa,r)>A(0,r)
   \iff
   B(\kappa,r)>0.
   $$

5. **`discr_factor`**  
   Proves the exact discriminant factorization
   $$
   \operatorname{discr}(r)
   =
   (r^2-1)^2(r^4-34r^2+1).
   $$

6. **Exact threshold identities**  
   `threshold_sq`, `threshold_quartic`, `conjugate_sq`, and `threshold_conjugate_mul` establish exact radical identities associated with
   $$
   r^{*}=3+2\sqrt2.
   $$

7. **`quartic_gt_iff_gt_threshold`**  
   For $r\ge1$,
   $$
   r^4-34r^2+1>0
   \iff
   r>3+2\sqrt2.
   $$

8. **`discr_sos`**  
   Establishes a sum-of-squares certificate connecting the discriminant to $B(\kappa,r)$.

9. **`exists_bracket_pos_iff_threshold`**  
   Proves
   $$
   \left(\exists\,\kappa>0,\ B(\kappa,r)>0\right)
   \iff
   r>3+2\sqrt2.
   $$
   The reverse direction has the explicit witness $\kappa=1$.

10. **`exists_volume_improvement_iff_threshold`**  
    Combines the preceding results to establish the central generalized-variance threshold theorem.

---

## Scope of the Formalization

This repository does **not** claim to formalize the paper in full.

The following are not currently formalized in the Lean development:

- stochastic differential equation semantics for the underlying Ornstein–Uhlenbeck processes;
- existence or uniqueness of the stationary Gaussian distribution;
- derivation of the stationary covariance matrix from the continuous Lyapunov equation;
- the complete stochastic OU model;
- the residual-variance threshold
  $$
  r_D^{*}=2+\sqrt3;
  $$
- the mutual-information/coherence monotonicity result;
- strong-coupling asymptotics;
- numerical experiments, plots, or tables.

In particular, the Lean development takes the closed-form scalar function $A(\kappa,r)$ as a definition rather than deriving it from the underlying $2\times2$ stochastic system.

**No end-to-end formal verification of the stochastic differential equation is claimed.** What the
Lean kernel checks is a statement of exact real algebra about the two scalar functions `volume` and
`volume0`. That `volume` really is $\det \Sigma$ for the coupled OU system is established on paper —
by solving the Lyapunov equation, independently re-derived in
[`docs/NOVELTY_AND_PROVENANCE.md`](docs/NOVELTY_AND_PROVENANCE.md) — and is *not* part of the
machine-checked chain. A reader who doubts that identification should treat the Lean development as
verifying an algebraic theorem about a polynomial ratio, which is exactly what it does.

What is formally verified is the exact algebraic threshold theorem for the scalar functions defined in `OUCorridor/Threshold.lean` and its consequence:

```lean
exists_volume_improvement_iff_threshold
```

---

## Repository Structure

```text
ou-threshold-lean/
├── OUCorridor/
│   ├── Threshold.lean
│   └── MainTheorem.lean
├── OUCorridor.lean
├── verified/
│   ├── Threshold.lean
│   ├── MainTheorem.lean
│   ├── verification-log.txt
│   ├── SHA256SUMS.txt
│   ├── lean-toolchain
│   ├── lake-manifest.json
│   └── lakefile.toml
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

### `OUCorridor.lean`

Top-level project module importing the formalization.

### `verified/`

Frozen verification record containing copies of the checked proof sources, environment information, build log, and cryptographic fingerprints.

`verified/` is an **integrity record, not part of the build**: no Lean file imports it, `lake` never
compiles it, and it holds no mathematics that `OUCorridor/` does not. Its `Threshold.lean` and
`MainTheorem.lean` are currently byte-identical to the corresponding files under `OUCorridor/`. It
is retained deliberately, so that the hashes in `verified/SHA256SUMS.txt` continue to identify the
exact sources behind the recorded build; it should be refreshed, not deleted, if the proofs
change.

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

### Unfinished-proof audit

The repository was additionally checked with:

```bash
grep -R -n "sorry\|admit\|axiom" OUCorridor --include="*.lean"
```

The recorded audit returned no matches.

This grep is a supplementary repository-level check for those explicit tokens. It is **not** a substitute for Lean's kernel checking of the generated proof terms.

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
The paths inside that file are relative to the repository root, so it must be checked from the root:

```bash
sha256sum -c verified/SHA256SUMS.txt
```

---

## Citation

For the research paper, please cite:

> De Jesús, Elias. (2026). *Heterogeneity-Driven Expansion and Synchronization Collapse in Coupled Ornstein–Uhlenbeck Systems*. Zenodo. https://doi.org/10.5281/zenodo.22059088

The DOI above is the all-versions Zenodo DOI and will resolve to the latest deposited version.

For work requiring the specific current paper version associated with this repository:

> De Jesús, Elias. (2026). *Heterogeneity-Driven Expansion and Synchronization Collapse in Coupled Ornstein–Uhlenbeck Systems*. Zenodo. https://doi.org/10.5281/zenodo.22059089

---

## AI Assistance and Verification

The research and conceptual development are by **Elias De Jesús**, with AI assistance used in mathematical derivation, code generation, auditing, and the Lean formalization workflow.

AI-generated or AI-assisted proof code is not treated as verification in itself. The formal claims represented in this repository are checked by the Lean elaborator and kernel against the definitions, theorem statements, imported libraries, and proof terms in the pinned Lean/mathlib environment.

Accordingly, the role of Lean is distinct from the role of AI assistance: AI supported the construction of the formalization, while Lean provides the machine-checking mechanism for the formal proof.
