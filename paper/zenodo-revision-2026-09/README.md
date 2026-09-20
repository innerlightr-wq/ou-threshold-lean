# Zenodo revision (version 2) — OU technical note

Prepared 19 September 2026. **Not deposited.** Nothing in this directory has been uploaded to
Zenodo, no DOI has been reserved or minted, and this branch has not been merged.

---

## ⚠ This manuscript is a reconstruction, not the original source

**The LaTeX source of version 1 does not exist.** It is not in any branch of this repository,
not anywhere else on the author's filesystem, and not in the Zenodo record — that record
contains a single file, `main.pdf`. The version 1 deposit did not include source.

`main.tex` in this directory was therefore **reconstructed from the deposited version 1 PDF**
and then revised. This is stated in the manuscript itself (Section 0, first page after the
abstract), in `CHANGELOG.md`, and in `REVISION_SUMMARY.md`. It should not be described as the
original source, and version 1 of the record is not superseded as evidence of what was written
in August 2026.

What the reconstruction preserves and what it does not:

| | |
|---|---|
| **Preserved exactly** | Every displayed equation, every proposition and theorem statement, every proof, the numerical table, the four figures, the reference list, the title, author and license. Each equation was transcribed and then re-verified symbolically before being carried over. |
| **Not preserved** | Prose wording at the sentence level, line breaks, hyphenation, pagination (19 → 22 pages), and **section and equation numbering**. A full concordance is in `CHANGELOG.md` §5. |

The four figures were extracted from the version 1 PDF as vector graphics and are unmodified
reproductions of the deposited figures. They were not regenerated: the script that produced
them was not deposited either, and has not been recovered. See Appendix B of the manuscript.

## Contents

| file | |
|---|---|
| `main.tex` | the revised manuscript (reconstruction + revisions) |
| `main.pdf` | compiled, 22 pages, letter |
| `figures/fig1.pdf` … `fig4.pdf` | the version 1 figures, extracted unmodified |
| `verify_revision.py` | symbolic verification of the manuscript's equations (SymPy) |
| `CHANGELOG.md` | what changed from version 1, with the section/equation concordance |
| `REVISION_SUMMARY.md` | the narrative account, including what was *not* done and why |
| `ZENODO_METADATA_DRAFT.md` | prepared metadata for a manual deposit |
| `SHA256SUMS.txt` | hashes of every file above |
| `build.log` | the build transcript that produced `main.pdf` |

The bibliography is the repository's own `references.bib` (two levels up), referenced as
`\bibliography{../../references}`. Packaging for Zenodo requires copying it next to `main.tex`;
see `ZENODO_METADATA_DRAFT.md`.

## Building

```bash
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

The recorded build is clean: 0 undefined citations, 0 undefined references, 0 overfull boxes,
0 underfull boxes, 0 BibTeX warnings, 24 bibliography entries.

## Verifying the mathematics

```bash
python3 -m venv venv && ./venv/bin/pip install sympy && ./venv/bin/python3 verify_revision.py
```

50 checks, all passing: every displayed equation carried over from version 1, all 32 entries of
Table 2, and every new identity of Section 11. This script is *not* the version 1 figure
script; it checks equations, it does not draw figures.

The statements listed in Section 15 of the manuscript are additionally machine-checked in
Lean 4 + mathlib elsewhere in this repository (`OUCorridor/`, frozen snapshots under
`verified/`), which does not depend on this script being correct.

## What is deliberately not here

- No upload to Zenodo, no DOI reservation, no new DOI.
- No merge to `main`, no pull request, no tag.
- No change to `verified/`, to any Lean source, or to any other branch.
- No separate manuscript for the general active-plane theorem. The manuscript mentions it in
  one paragraph (Section 20) and says it is in preparation; writing it was out of scope here.
- No change to licensing (CC BY 4.0 throughout) and no change to the title.
