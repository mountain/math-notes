#!/usr/bin/env bash
# Build the finite-trigonometry note and its figures.
set -euo pipefail
cd "$(dirname "$0")"

for f in figures/fig-*.tex; do
  ( cd figures && pdflatex -interaction=nonstopmode "$(basename "$f")" >/dev/null )
done

pdflatex -interaction=nonstopmode finite-trig.tex >/dev/null
pdflatex -interaction=nonstopmode finite-trig.tex >/dev/null
pdflatex -interaction=nonstopmode finite-trig.tex >/dev/null

# PNG previews of the figures
for p in figures/fig-*.pdf; do
  pdftoppm -png -r 200 -singlefile "$p" "${p%.pdf}"
done

echo "built finite-trig.pdf and figures/fig-*.pdf,*.png"
