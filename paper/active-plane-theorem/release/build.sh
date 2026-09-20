#!/bin/sh
# Build the manuscript. Self-contained: needs only this directory.
set -e
cd "$(dirname "$0")"
if command -v latexmk >/dev/null 2>&1; then
  latexmk -pdf -halt-on-error main.tex
else
  pdflatex -interaction=nonstopmode -halt-on-error main.tex
  bibtex main
  pdflatex -interaction=nonstopmode -halt-on-error main.tex
  pdflatex -interaction=nonstopmode -halt-on-error main.tex
fi
