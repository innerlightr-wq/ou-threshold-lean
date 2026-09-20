# Build and verification instructions

This directory is self-contained. Nothing in it references a file outside it.

## Build the PDF

```bash
./build.sh
```

or equivalently, from inside this directory:

```bash
latexmk -pdf main.tex
```

If `latexmk` is unavailable, `build.sh` falls back to:

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

**Requirements.** A TeX distribution providing `article`, `geometry`, `amsmath`,
`amssymb`, `amsthm`, `graphicx`, `booktabs`, `fontenc`, `inputenc`, `microtype`
and `hyperref` (all present in a standard TeX Live install), plus `bibtex`.
`main.tex` uses `\bibliographystyle{plain}` and `\bibliography{references}`,
which resolves to the `references.bib` beside it.

**Expected result.** 25 pages, letter paper. A clean build reports
0 undefined citations, 0 undefined references, 0 overfull boxes and
0 BibTeX warnings, with 33 bibliography entries, all of them cited.

## Re-run the symbolic verification

```bash
python3 manuscript_checks.py
```

**Requirements.** Python 3 and SymPy (`pip install sympy`). No other package.

**Expected result.** `126/126 checks passed` and exit status 0.

The script is not a spot check. It derives each quantity from its definition
rather than confirming a pre-written formula — it solves the Lyapunov equation
from scratch, extracts the determinant's coefficients in `tau` and compares
leading against constant, builds `Phi` and `A` for `P3` and `K3` from the graph
Laplacians, and confirms each exact minimum by algebraic factorization. Exact
rational and radical arithmetic throughout; no floating-point step enters any
claim. A transcription error in the manuscript would therefore fail a check
rather than pass one.

## Regenerate the figures (optional)

```bash
python3 make_figures.py
```

**Requirements.** Python 3, NumPy and Matplotlib. Writes `figures/fig1.pdf`,
`figures/fig2.pdf`, `figures/fig3.pdf`. Every plotted curve is evaluated from
the exact closed forms proved in the paper, and the marked minima are the exact
algebraic constants, not numerical optimizations. The figures are included in
this package already built, so this step is only needed to reproduce them.

## Machine-checked proofs (not included here)

The Lean 4 formalization is not bundled with this source package, to keep it to
what a reader of the manuscript needs. It lives in the repository named in the
README, under `OUCorridor/`, with a frozen snapshot — sources, environment,
build transcript and axiom audit — at
`verified/palindromic-generalization-2026-09/`. Section 17 of the manuscript
and its Table 2 record which statements are machine-checked and which are not.
