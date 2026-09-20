# Zenodo metadata — DRAFT for version 2

> **Nothing has been uploaded.** No new DOI has been reserved, requested, or minted. This file
> is a prepared draft for the author to use manually. Publishing a new version on Zenodo mints
> a new *version* DOI under the existing *concept* DOI; that action is irreversible and is
> deliberately left undone here.

## Existing record (verified against the Zenodo REST API)

| field | value |
|---|---|
| version 1 DOI | `10.5281/zenodo.22059089` |
| concept (all-versions) DOI | `10.5281/zenodo.22059088` |
| deposited | 2026-08-22 |
| license | CC BY 4.0 |
| files | `main.pdf` only (19 pages) |

**Upload as a new version of the existing record** (Zenodo: *New version* on record 22059089),
never as a new standalone record — otherwise the concept DOI no longer groups the two versions.

## Proposed metadata for version 2

```yaml
upload_type:   publication
publication_type: preprint          # unchanged from v1
title:         "Heterogeneity-Driven Expansion and Synchronization Collapse in Coupled
                Ornstein–Uhlenbeck Systems"
version:       "2"
publication_date: 2026-09-19        # adjust to the actual deposit date
language:      eng
license:       cc-by-4.0            # unchanged
creators:
  - name:        "De Jesús, Elias"
    affiliation: "Independent Researcher"
    orcid:       "0009-0007-0190-9143"
```

### Description (HTML for the Zenodo description field)

```html
<p>Two diffusively coupled Ornstein&ndash;Uhlenbeck processes with unequal noise amplitudes are
analyzed exactly through the continuous Lyapunov equation. Three scalar functionals of the
stationary covariance matrix are studied: the residual variance D = Var(X|Y), the Gaussian
mutual information C = I(X;Y), and the covariance volume A = det &Sigma;.</p>

<p>For arbitrary positive relaxation rates and noise amplitudes, A&prime;(0) &lt; 0:
infinitesimal diffusive coupling always initially contracts the stationary covariance volume.
In the equal-relaxation case, sup A(&kappa;) &gt; A(0) if and only if the noise-amplitude ratio
exceeds 3 + 2&radic;2, and the enhancement region is then a bounded interval whose endpoints
satisfy &kappa;<sub>1</sub>&kappa;<sub>2</sub> = 1. A second exact threshold, 2 + &radic;3,
governs enhancement of the conditional residual variance. Gaussian coherence increases strictly
with coupling, while strong coupling drives &rho; &rarr; 1, D &rarr; 0, A &rarr; 0.</p>

<p><strong>New in version 2.</strong> (i) Both thresholds are shown to be reciprocal units
&mdash; roots of x&sup2; &minus; 6x + 1 = 0 and x&sup2; &minus; 4x + 1 = 0 &mdash; and a
cross-threshold identity is proved: at the unique coupling &kappa; = 1 where the volume
enhancement region degenerates, the eigenvalue ratio of the stationary covariance is exactly
(2 + &radic;3)&sup2; = 7 + 4&radic;3. (ii) The central algebraic statements are machine-checked
in Lean 4 with mathlib. (iii) The normal-mode discussion is corrected: heterogeneous noise
drives the symmetric and antisymmetric modes with <em>correlated</em> forcing, which is the
mechanism behind the enhancement window. (iv) Terminology around "synchronization" is
sharpened, the amplitude and variance ratios are distinguished explicitly, and the limitations
are strengthened.</p>

<p><strong>Source note.</strong> The LaTeX source of version 1 was not preserved. The version 2
manuscript is a reconstruction of version 1 from the deposited PDF, followed by the revisions
above; every displayed equation of version 1 was transcribed and re-verified symbolically
before being carried over, and the four figures are the version 1 vector graphics, unmodified.
Section and equation numbers therefore differ from version 1; a concordance is included.</p>

<p>The results are specific to this linear-Gaussian model. No general principle for nonlinear,
biological, cognitive, or social systems is claimed.</p>
```

### Keywords

```
Ornstein-Uhlenbeck process; Lyapunov equation; stationary covariance; generalized variance;
noise heterogeneity; exact threshold; conditional variance; Gaussian mutual information;
synchronization manifold; reciprocal polynomial; formal verification; Lean 4
```

### Related identifiers

| relation | identifier | type | note |
|---|---|---|---|
| `isNewVersionOf` | `10.5281/zenodo.22059089` | DOI | version 1 (set automatically by "New version") |
| `isSupplementedBy` | `https://github.com/innerlightr-wq/ou-threshold-lean` | URL | Lean 4 formalization companion |
| `cites` | `10.5281/zenodo.22051650` | DOI | the author's bosonic Josephson junction note (§16) |

If the formalization repository is itself archived to Zenodo later, replace the GitHub URL with
that DOI and use `isSupplementedBy` in both directions.

### Files to upload

| file | note |
|---|---|
| `main.pdf` | the compiled manuscript (22 pages, letter) |
| `main.tex` | source — **new in v2**; v1 deposited no source |
| `references.bib` | copy of the repository bibliography at this commit |
| `figures/fig1.pdf` … `figures/fig4.pdf` | the four figures, as extracted from v1 |
| `verify_revision.py` | symbolic verification of the manuscript's equations |
| `CHANGELOG.md` | what changed from v1, with the concordance |

Depositing the source this time is the point: the reason this revision needed a reconstruction
is that version 1 deposited only the PDF.

`references.bib` lives at the repository root and must be **copied** next to `main.tex` before
packaging, because `main.tex` refers to it as `../../references` for the in-repository build.
Change that one line to `\bibliography{references}` in the uploaded copy, or upload a build
directory in which the copy sits beside the manuscript.

## Checklist before publishing (manual)

- [ ] Confirm the author intends a new *version*, not a new record.
- [ ] Confirm the reconstruction notice (Section 0) is acceptable as the public description of
      how this version was produced.
- [ ] Rebuild the PDF from the packaged directory and confirm it matches `SHA256SUMS.txt`.
- [ ] Confirm the license remains CC BY 4.0 and no funder/grant metadata is needed.
- [ ] Only then: *New version* → upload → publish. A new version DOI is minted at that point.
