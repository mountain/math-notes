#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 verify.py
for pass in 1 2 3; do
  if ! pdflatex -halt-on-error -interaction=nonstopmode conic-dynamics.tex >build-output.txt; then
    tail -40 build-output.txt >&2
    exit 1
  fi
done
test -s conic-dynamics.pdf
if rg -n 'Undefined control sequence|LaTeX Error|undefined references|Citation .* undefined|Reference .* undefined|multiply defined|Overfull \\hbox' conic-dynamics.log; then
  echo "Build requires attention; see conic-dynamics.log" >&2
  exit 1
fi
rm build-output.txt
echo "Built conic-dynamics.pdf; no undefined references, duplicate labels, or overfull boxes."
