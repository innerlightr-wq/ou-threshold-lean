# OU Threshold — Lean 4 Formal Verification Companion

A machine-checked formalization, in Lean 4 with mathlib, of the central algebraic threshold theorem from:

> Elias De Jesús (2026). *Heterogeneity-Driven Expansion and Synchronization Collapse in Coupled Ornstein–Uhlenbeck Systems.*

The paper studies two diffusively coupled Ornstein–Uhlenbeck processes and shows that, in the equal-relaxation normalization, the stationary covariance-volume functional $begin:math:text$A\(\\kappa\,r\)$end:math:text$ can exceed its uncoupled value $begin:math:text$A\(0\,r\)$end:math:text$ at some positive coupling strength if and only if the noise-heterogeneity ratio $begin:math:text$r$end:math:text$ exceeds the exact threshold

$begin:math:display$
r\^\\\* \= 3 \+ 2\\sqrt\{2\}\.
$end:math:display$

This repository formalizes and machine-checks that threshold statement as a result in exact real algebra.

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

## Scope of the Formalization

This repository does **not** claim to formalize the paper in full.

The following are not currently formalized in the Lean development:

- stochastic differential equation semantics for the underlying Ornstein–Uhlenbeck processes;
- existence or uniqueness of the stationary Gaussian distribution;
- derivation of the stationary covariance matrix from the continuous Lyapunov equation;
- the complete stochastic OU model;
- the residual-variance threshold
  $begin:math:display$
  r\_D\^\\\*\=2\+\\sqrt3\;
  $end:math:display$
- the mutual-information/coherence monotonicity result;
- strong-coupling asymptotics;
- numerical experiments, plots, or tables.

In particular, the Lean development takes the closed-form scalar function $begin:math:text$A\(\\kappa\,r\)$end:math:text$ as a definition rather than deriving it from the underlying $begin:math:text$2\\times2$end:math:text$ stochastic system.

What is formally verified is the exact algebraic threshold theorem for the scalar functions defined in `OUCorridor/Threshold.lean` and its consequence:

```lean
exists_volume_improvement_iff_threshold
```

---

## Repository Structure

```text
ou-threshold-lean/
├── OUCorridor/
│   ├── Basic.lean
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
