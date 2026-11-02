#!/usr/bin/env bash
# Exact verifier for docs/normalized-lyapunov/.  Standard library only, no numpy/sympy/mpmath.
# Every check is exact rational arithmetic; floats appear only in printed diagnostics.
set -u
cd "$(dirname "$0")"
total=0; pass=0
for f in verify.py threemode2.py threshold3.py controls6.py priorart7.py review8.py singlepair9.py multipair10.py components11.py sharp12.py cost13.py boxes14.py interp15.py; do
  echo "################ $f"
  out=$(timeout 1800 python3 -u "$f" 2>&1) || { echo "$out"; echo "RUNNER: $f exited nonzero"; exit 1; }
  echo "$out"
  p=$(printf '%s\n' "$out" | grep -c '^PASS  ')
  fl=$(printf '%s\n' "$out" | grep -c '^FAIL  ')
  total=$((total+p+fl)); pass=$((pass+p))
  if [ "$fl" -ne 0 ]; then echo "RUNNER: $f has $fl failing checks"; exit 1; fi
done
echo
echo "========================================================================"
echo "ALL SECTIONS: $pass / $total checks passed"
echo "========================================================================"
