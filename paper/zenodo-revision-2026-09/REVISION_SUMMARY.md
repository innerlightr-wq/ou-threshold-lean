# Revision summary

**Task:** prepare a revised version of the OU technical note for a new Zenodo version.
**Branch:** `revise-zenodo-ou-2026-09`. **Status:** prepared, not deposited, not merged.

---

## 1. The stop condition was hit: there is no version 1 source

The brief required that if the original TeX source could not be found, I stop before rewriting
the manuscript wholesale, report the situation, and only then produce a clearly labeled
reconstruction if a faithful one was straightforward. That is what happened.

**Search performed, all negative:**

| where | result |
|---|---|
| every branch of `ou-threshold-lean` (`git log --all`, `git grep` across all refs) | no `.tex` file has ever existed in this repository |
| the whole of `$HOME` | no `.tex` matching this manuscript; other projects do have `manuscript/*.tex`, so the absence here is specific, not a naming problem |
| the Zenodo record 22059089 (REST API) | one file: `main.pdf`, 19 pages. No source, no figure script |

**PDF forensics** (consistent with a normal pdfLaTeX build whose sources were simply not kept):
pdfTeX 1.40.25, "LaTeX with hyperref", Computer Modern with CMR17 on the title, letter paper,
19 pages, and **no embedded raster images** — the figures are vector graphics, so they could be
extracted losslessly.

**Judgement.** A faithful reconstruction was straightforward, because the mathematical content
is fully determined by the PDF (every equation is displayed and machine-readable) and the
figures are vector and extractable. So I reconstructed rather than stopping, and labeled it
prominently in four places: the manuscript's own Section 0, this file, `CHANGELOG.md`, and
`README.md`.

**What a reader loses.** Sentence-level wording, line breaks, pagination, and section/equation
numbering are not the version 1 ones. `CHANGELOG.md` §5 gives the full concordance, verified
against the compiled `main.aux` rather than estimated. Version 1 remains available and is not
superseded as a record of the August text.

## 2. Figures

Extracted from the version 1 PDF by locating each figure's bounding box on its page
(whitespace-band detection on a rendered copy) and cropping the page to it, preserving the
vector content. Each extracted file was checked to contain only its own figure — no body text
or neighbouring figure leaks into any of them — and figures 1–3 were inspected visually against
the version 1 pages. They are unmodified reproductions.

They were **not** regenerated. The generating script was not deposited with version 1 and has
not been recovered, which is recorded in Appendix B of the manuscript.

## 3. What was revised

Full detail in `CHANGELOG.md`. In brief:

**New mathematics (Section 11).** The two thresholds `r_A* = 3+2√2` and `r_D* = 2+√3` are shown
to be reciprocal units — the roots greater than 1 of `x²−6x+1=0` and `x²−4x+1=0` — so that
`s(r_A*) = 6` and `s(r_D*) = 4` for `s(x) = x+1/x`, and the threshold conditions can be written
without a `max(σ₁/σ₂, σ₂/σ₁)`. The new **Theorem 2** then links them: at `r = r_A*` and the
unique coupling `κ = 1` where the enhancement region degenerates, `(tr Σ)²/det Σ = 16` exactly,
so the covariance eigenvalue ratio is `7+4√3 = (r_D*)²`. An additive form is
`½ log q = log r_D* = arcosh 2`. A remark records that this does not extend to `n ≥ 3` as
stated, with the counterexample `(1,8,12)` vs `(2,3,16)`.

**One real correction (Section 7.1).** Version 1, discussing the strong-coupling limit,
described the symmetric and antisymmetric normal modes as independently driven. They are not.
Rotating `Q = diag(σ₁², σ₂²)` into the drift eigenbasis leaves off-diagonal entry
`(σ₁²−σ₂²)/2`, zero only for `σ₁ = σ₂`. Heterogeneous noise drives the normal modes with
*correlated* forcing, and that correlation is precisely the mechanism behind the enhancement
window: the modal determinant is
`A(κ) = (1+r²)²/[16(1+2κ)] − (1−r²)²/[16(1+κ)²]`, in which a `1/(2κ)` shrinking term competes
with a faster-decaying `1/κ²` correlation term. No stated result changes — that expression is
algebraically identical to the version 1 formula — but the explanation given in version 1 was
wrong where it was given, and it is now stated correctly and marked as a correction.

**Terminology (Section 14, Remark 5; Limitation 8).** "Synchronization collapse" is now
defined: degeneration of the *stationary covariance ellipse* toward the diagonal in the
singular limit `κ → ∞`. It is explicitly not trajectory synchronization, not a stability
transition, and not an application of the master-stability framework, which does not apply to a
linear system with a globally attracting stationary distribution at every `κ ≥ 0`. The title is
unchanged, per the brief, with the remark as its definition.

**Amplitude vs. variance (Section 5.3).** `r = σ₂/σ₁` carries both threshold numbers; `t = r²`
is what enters the Lyapunov equation; `w(r²) = s(r)²−2` relates their reciprocal invariants.
Table 1 gives both for both thresholds. Without this, the numbers 6, 4, 34 and 14 in Section 11
are ambiguous.

**Formal verification (Section 15).** New section reporting the Lean 4 + mathlib development in
this repository, with an explicit list of what is *not* formalized — the stochastic-process
content of Proposition 1, the general-rate covariance and `A′(0) < 0`, the monotonicity of `C`,
the asymptotics, the table and the figures — and the plain statement that the machine-checked
part is the algebra, not the modelling.

**Limitations (Section 18).** Items 1–7 unchanged; four added, covering the restricted sense of
"synchronization", the restricted and transient sense of "expansion", the confinement of
Theorem 2 to one two-parameter family, and the algebra/modelling gap in the formalization.

## 4. Verification performed

**Symbolic (`verify_revision.py`, 50 checks, all passing).** Every displayed equation carried
over from version 1 was re-derived, not merely copied: the general covariance solves the
Lyapunov equation, `det Σ` matches, `A(0)` and `A′(0)` for arbitrary rates, the difference
formula, both discriminant factorizations, both thresholds, `κ₁κ₂ = 1`, the `ρ²` derivative
factorization, all four asymptotic rates, and **all 32 entries of Table 2** to better than
`6×10⁻⁵`. Every new identity of Section 11 was checked the same way, including the merger
invariant, the eigenvalue ratio, `arcosh 2`, and the `n ≥ 3` counterexample.

One check initially reported a failure, `1−ρ² ~ 2/κ`. Investigation showed the *test* was at
fault (a structural equality against SymPy's unevaluated limit object), not the paper: the
limit is exactly 2, confirmed by series expansion and numerically at `κ = 10³, 10⁵, 10⁷`.
Version 1's Eq. (39) is correct.

**Build.** `pdflatex → bibtex → pdflatex ×2`, clean: 0 undefined citations, 0 undefined
references, 0 overfull boxes, 0 underfull boxes, 0 BibTeX warnings, 24 bibliography entries,
22 pages.

**Bibliography.** The 12 works cited by version 1 were verified by DOI content negotiation
against Crossref/DataCite and added to the repository's `references.bib` (now 33 entries).
Two problems surfaced and were handled rather than papered over:

- *Aubin, Viability Theory.* Version 1 cites the 1991 Birkhäuser edition. The only registered
  DOI, `10.1007/978-0-8176-4910-4`, resolves to the **2009** Modern Birkhäuser Classics
  reprint. The entry cites 1991 as before and records the edition mismatch in a `note`, rather
  than attaching a 2009 DOI to a 1991 book silently.
- *The author's own Zenodo note* (`DeJesus2026bjj`). DataCite returns it as an `@article` with
  no journal and an author string ending in a comma, which BibTeX rejects. Reformatted into the
  house `@misc` style used by the other Zenodo entries, with the reformatting noted in the
  entry.

## 5. What was deliberately not done

| | |
|---|---|
| **No Zenodo upload**, no DOI reserved or minted | the brief forbids it; `ZENODO_METADATA_DRAFT.md` prepares the deposit for the author to perform manually |
| **No merge, no PR, no tag** | branch `revise-zenodo-ou-2026-09` is pushed and left for review |
| **No change to `verified/`, to any Lean source, or to any other branch** | the three frozen snapshots still hash-verify |
| **No separate active-plane manuscript** | explicitly out of scope; the manuscript devotes one paragraph (Section 20) to it and says it is in preparation |
| **No title change** | no compelling mathematical reason; the ambiguity in it is addressed by Remark 5 instead |
| **No licensing change** | CC BY 4.0 throughout |
| **No "contextual corridor", no 63/37 split, no Minkowski or relativity analogy** | not introduced anywhere; the `arcosh` in Eq. (45) is used as the inverse hyperbolic cosine it is, with no kinematic reading attached |
| **No "novel", "first", "unprecedented" or "universal"** applied to any result | the literature statement remains "we did not identify in the literature examined…", with no priority claim |
| **The palindromic substitution is not called a "Chebyshev transform"** | it is described as a Chebyshev-*type* identity for `w(r²) = s(r)²−2`, which is what it is, with no source claimed |

## 6. Open items for the author

1. **Decide whether to deposit.** If yes, follow `ZENODO_METADATA_DRAFT.md`, and deposit the
   source this time — the need for a reconstruction is a direct consequence of version 1 having
   deposited only a PDF.
2. **The version 1 figure script is still missing.** If it resurfaces, regenerating the figures
   would let Appendix B be dropped.
3. **The general active-plane manuscript** remains to be written; the Lean development for it
   already exists on `formalize-active-plane-reduction`.
4. **Zotero** was not written to, here or in the preceding task: the local API needs a GUI
   approval dialog. The eight references added to `references.bib` in this task should be filed
   into the existing library by hand, per `docs/ZOTERO_SETUP.md` §5.
