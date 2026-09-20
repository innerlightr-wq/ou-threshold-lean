# Changelog — *Heterogeneity-Driven Expansion and Synchronization Collapse in Coupled Ornstein–Uhlenbeck Systems*

## Version 2 — September 2026 (prepared, **not deposited**)

Version 1: Zenodo, deposited 22 August 2026, version DOI
[10.5281/zenodo.22059089](https://doi.org/10.5281/zenodo.22059089), concept DOI
10.5281/zenodo.22059088, CC BY 4.0, single file `main.pdf`, 19 pages.

### 0. Source situation (read this first)

**The LaTeX source of version 1 was not preserved and could not be located.** It is absent from
every branch of this repository, from the rest of the filesystem, and from the Zenodo record,
which contains only `main.pdf`. `main.tex` in this directory is therefore a **reconstruction**
of version 1 from the deposited PDF, followed by the revisions listed below. This is stated in
the manuscript itself (Section 0), in `README.md`, and in `REVISION_SUMMARY.md`.

Consequences a reader should keep in mind:

- Prose wording, line breaks, hyphenation and pagination differ from version 1 (19 pages → 22).
- **Equation and section numbers differ.** A concordance is given in §4 below.
- Every *displayed equation* of version 1 was transcribed and re-verified symbolically before
  being carried over; the mathematical content is preserved exactly.
- The four figures were extracted from the version 1 PDF as vector graphics and are byte-level
  reproductions of the deposited figures. They were **not** regenerated, because the script that
  produced them was not deposited either.

### 1. New results

| | |
|---|---|
| **§11, Theorem 2 (new)** | Cross-threshold identity. At `r = r_A* = 3+2√2` and `κ = 1` — the unique coupling at which the volume enhancement region degenerates — the stationary covariance satisfies `(tr Σ)²/det Σ = 16`, hence its eigenvalue ratio is exactly `q = 7+4√3 = (2+√3)² = (r_D*)²`. |
| **§11.1 (new)** | Both thresholds are reciprocal units: `r_A*` and `r_D*` are the roots >1 of `x²−6x+1=0` and `x²−4x+1=0`, so `s(r_A*) = 6` and `s(r_D*) = 4` for `s(x) = x+1/x`. The threshold conditions can therefore be written without `max(σ₁/σ₂, σ₂/σ₁)`: enhancement occurs iff `s(r) > 6`, residual enhancement iff `s(r) > 4`. |
| **§11.1 (new)** | The discriminant factor `r⁴−34r²+1` of Eq. (21) is identified as `t²−34t+1` in the variance variable `t = r²`; `34` and `14` are the reciprocal invariants `w(t) = t+1/t` of the two thresholds. |
| **§11.2, Eq. (45) (new)** | Additive form: the log-anisotropy of the volume-critical covariance ellipse is `η = ½ log q = log r_D* = arcosh 2`. |
| **§11.2, Remark 4 (new)** | The identity does not survive to `n ≥ 3` as stated: `(tr, det)` no longer fixes spectral shape. Counterexample `(1,8,12)` vs `(2,3,16)` — same trace 21, same determinant 96, ratios 12 and 8. |
| **§7.1, Eq. (23) (new)** | Modal ("normal-mode") closed form `A(κ) = (1+r²)²/[16(1+2κ)] − (1−r²)²/[16(1+κ)²]`, algebraically identical to Eq. (18), which exhibits the mechanism behind the enhancement window. |
| **§15 (new)** | Machine-checked verification in Lean 4 + mathlib, with an explicit list of what is **not** formalized. |
| **§20 (new)** | One-paragraph pointer to a general two-mode ("active-plane") reduction that contains this paper's volume threshold as the instance `τ = r²`, `w = 34`. |

### 2. Corrections

1. **Normal-mode forcing (§7.1, Remark 1).** Version 1, in discussing the strong-coupling
   limit, described the symmetric and antisymmetric modes as though they were independently
   driven. They are not: rotating `Q = diag(σ₁², σ₂²)` into the drift eigenbasis gives
   off-diagonal entry `(σ₁²−σ₂²)/2`, which vanishes **only** for `σ₁ = σ₂`. Heterogeneous
   noise drives the two normal modes with *correlated* noise, and that correlation is exactly
   what produces the enhancement window. No stated result changes — Eq. (23) and Eq. (18) are
   the same function — but the explanation in version 1 was wrong where it was given.
2. **Aubin citation.** Version 1 cited *Viability Theory* as Birkhäuser, 1991, with no DOI. The
   only registered DOI, 10.1007/978-0-8176-4910-4, resolves to the 2009 Modern Birkhäuser
   Classics reprint. The bibliography now cites the 1991 edition as before and records this
   edition mismatch in a `note` field rather than silently attaching a 2009 DOI to a 1991 book.
3. **Ferreira–Metz–Barucca year.** Verified as 2025, Phys. Rev. E **111**, 014151
   (unchanged from version 1; re-verified by DOI content negotiation).

### 3. Sharpened wording

1. **"Synchronization" (§14, Remark 5; Limitation 8).** New remark defining the term as used
   here: degeneration of the *stationary covariance ellipse* toward the diagonal in the
   singular limit `κ → ∞`. Explicitly *not* trajectory synchronization, *not* a stability
   transition, and *not* an application of the master-stability framework, which does not apply
   to a linear system with a globally attracting stationary distribution at every `κ ≥ 0`. The
   title is retained for continuity with version 1, with the remark as its definition.
2. **Amplitude vs. variance ratio (§5.3, new).** Explicit convention: `r = σ₂/σ₁` is the
   amplitude ratio and carries both threshold numbers; `t = r²` is the variance (temperature)
   ratio and is what enters the Lyapunov equation. Their reciprocal invariants are related by
   `w(r²) = s(r)² − 2`. Table 1 collects both for both thresholds. This distinction is what
   makes the numbers 6, 4, 34 and 14 of §11 unambiguous.
3. **Residual crossings (§9, Remark 2).** New: unlike the volume crossings, the two residual
   crossings do **not** satisfy a reciprocal identity — their product is `2r²/(r²+1)`, which
   equals 1 only at `r = 1`. The reciprocal structure shared by the thresholds lives in the
   heterogeneity variable, not the coupling variable. Version 1 did not say this, and the
   juxtaposition of the two thresholds could have been read as implying otherwise.
4. **Generality of Proposition 3 (§6; Limitation 2).** Now stated explicitly that `A′(0) < 0` is the
   only result in the paper holding for arbitrary positive relaxation rates.
5. **Relation to existing work (§2).** Added Godrèche–Luck and the Brownian-gyrator references
   as the nearest two-temperature linear models; noted that the modal solution used in §7.1 is
   standard in that literature; noted that `det Σ` is Wilks's generalized variance.
6. **Novelty wording (§2).** "We did not identify in the literature examined…" retained and
   extended to the new cross-threshold identity, with a pointer to the repository's provenance
   record. No priority claim is made anywhere, and the words "novel", "first", "unprecedented"
   and "universal" are not used of any result in this paper.

### 4. Strengthened limitations (§18)

Items 1–7 are unchanged from version 1. New items:

- **8.** "Synchronization" restricted to the sense of Remark 5.
- **9.** "Expansion" means an increase of `det Σ` relative to its uncoupled value at the same
  parameters, with fixed full support; and it is transient, since `A(κ) → 0`.
- **10.** Theorem 2 is an identity within one two-parameter family, not derived from a
  structural principle, and the `n ≥ 3` counterexample shows its invariant does not survive.
- **11.** The formalization verifies *algebra, not modelling*: no part of the stochastic-process
  argument is machine-checked.

### 5. Section and equation concordance (v1 → v2)

Verified against the compiled `main.aux` of this version, not estimated.

**Sections.**

| v1 | v2 | |
|---|---|---|
| §1–§4 | §1–§4 | unchanged in content |
| §5, §5.1, §5.2 | §5, §5.1, §5.2 | unchanged; **§5.3 new** (amplitude vs. variance ratio) |
| §6 | §6 | + note that Prop. 3 is the only general-rate result |
| §7 | §7 | **§7.1 new** (normal modes and correlated forcing) |
| §8 | §8 | + Eq. (27), the tangency `B_A(κ;r_A*) = −8(r_A*)²(κ−1)²`, double root `κ = 1` |
| §9 | §9 | + Remark 2 (residual crossings are not reciprocal) |
| §10 | §10 | unchanged |
| — | **§11** | **new**: §11.1 reciprocal units, §11.2 cross-threshold identity |
| §11 | §12 | unchanged (numerical example) |
| §12 | §13 | unchanged (figures) |
| §13 | §14 | renamed "Strong-Coupling Limit of the Covariance Geometry"; + Remark 5 |
| — | **§15** | **new** (machine-checked verification) |
| §14 | §16 | unchanged (bosonic Josephson junction) |
| §15 | §17 | unchanged (provisional regime) |
| §16 | §18 | limitations 8–11 added |
| §17 | §19 | unchanged (nonlinear bistable extension) |
| — | **§20** | **new** (companion note: general two-mode reduction) |
| §18 | §21 | + the reciprocal/cross-threshold sentence |
| §19 | §22 | + one sentence on Theorem 2; "synchronization ultimately removes …" reworded |
| Acknowledgments | Acknowledgments | AI-assistance statement expanded |
| Appendix A | Appendix A | + list of newly checked identities |
| — | **Appendix B** | **new** (provenance of the figures) |

Propositions 1–7 and Corollary 1 keep their version 1 numbers. Theorem 1 is unchanged;
**Theorem 2 is new**. Remarks are numbered 1–5 in version 2 and were unnumbered in version 1.

**Equations.** Version 1 numbered (1)–(45); version 2 numbers (1)–(52).

| v1 | v2 | |
|---|---|---|
| (1)–(13) | (1)–(13) | identical numbering and content |
| (14) `D(κ)` | (14) | |
| (15) `C(κ)`, (16) `ρ` | (15) | merged into one display |
| (17) `A(κ) = det Σ` | — | now inline, unnumbered |
| (18) `A(0)`, (19) `A′(0)` | (17) | merged into one display |
| — | **(16)** | **new**: `s(r)`, `w(t)`, `w(r²) = s(r)²−2` |
| (20) `A(κ)`, equal relaxation | (18) | |
| (21) difference formula | (19) | |
| (22) `B_A` | (20) | |
| (23) `Δ_A` | (21) | |
| — | **(22)–(23)** | **new**: `Q̃` and the modal form of `A(κ)` |
| (24) `sup A > A(0)` | (24) | |
| (25) threshold | (25) | |
| (26) `κ₁κ₂ = 1` | (26) | |
| — | **(27)** | **new**: tangency at `r = r_A*` |
| (27) `D(κ) − D(0)` | (28) | |
| (28) `B_D` | (29) | |
| (29) `Δ_D` | (30) | |
| (30) `∃κ: D(κ) > D(0)` | (31) | |
| (31) `r > 2+√3` | — | now inline in Prop. 5, unnumbered |
| (32) `2+√3 < 3+2√2` | (32) | |
| (33) `ρ²(κ)` | (33) | |
| (34) `dρ²/dκ` | (34) | |
| (35) `P(κ,r)` | (35) | |
| — | **(36)–(45)** | **new**: all of §11 |
| (36)–(38) `Σ` components | (46)–(48) | |
| (39)–(42) asymptotics | (49) | merged into one display |
| (43) provisional regime `𝒞` | (50) | |
| (44)–(45) bistable extension | (51)–(52) | |

### 6. Bibliography

Version 1 cited 12 works, none with machine-verified metadata recorded. All 12 have now been
verified by DOI content negotiation against Crossref/DataCite and are carried into the
repository bibliography `references.bib` (33 entries total; this manuscript cites 24 of them).
Added in version 2: Godrèche–Luck 2019, Filliger–Reimann 2007, Dotsenko et al. 2013,
Uhlenbeck–Ornstein 1930, Gardiner 2004, Vatiwutipong–Phewchean 2019, Wilks 1932, Mauchly 1940,
Muirhead 1982, Wolkowicz–Styan 1980, Horn–Johnson 2012, Lauritzen 1996.

### 7. Reproducibility

`verify_revision.py` re-derives and checks **50** statements of this manuscript symbolically
with SymPy, including every displayed equation carried over from version 1, all 32 entries of
Table 2, and every new identity of §11. It exits with all checks passing. It is **not** the
version 1 figure-generating script, which was not deposited and has not been recovered.

### 8. Not changed

- Title, author, ORCID, license (CC BY 4.0).
- All results of version 1: `A′(0) < 0`, both thresholds, `κ₁κ₂ = 1`, monotonicity of `C`, the
  strong-coupling asymptotics, the numerical table, the four figures. Nothing is retracted.
- The DOI. **No new DOI has been reserved or assigned, and nothing has been uploaded to
  Zenodo.** Publishing a new version, which mints a new version DOI under the existing concept
  DOI, remains a manual step for the author.
