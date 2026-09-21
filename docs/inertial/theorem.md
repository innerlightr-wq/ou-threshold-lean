# Inertial OU Global Reciprocity Theorem

Companion documentation for the two-mode inertial Ornstein–Uhlenbeck
reciprocity result. See [`derivation.md`](derivation.md) for the proof
outline, [`computer_assisted_proof.md`](computer_assisted_proof.md)
for the exact computer-algebra disclosure, and
[`literature_provenance.md`](literature_provenance.md) for the
literature/attribution audit. Full manuscript:
[`paper/inertial/main.tex`](../../paper/inertial/main.tex). Verification
scripts: [`verification/inertial/`](../../verification/inertial/).

## Model

State `(x1,p1,x2,p2)` (unit-mass reduction, `delta_i = gamma_i/m_i`).
Drift matrix
```
A = [[0, 1, 0, 0], [-(omega1^2+k), -delta1, k, 0],
     [0, 0, 0, 1], [k, 0, -(omega2^2+k), -delta2]]
```
Per-bath diffusion `Q1=diag(0,2delta1,0,0)`, `Q2=diag(0,0,0,2delta2)`.
`C1,C2` solve `A*Ci+Ci*A^T=-Qi`. Admissible domain:
`omega1,omega2,k,delta1,delta2 > 0`.

## Main theorem

For `s=T1/T2`, `P(s):=det(s*C1+C2) = c4 s^4+c3 s^3+c2 s^2+c1 s+c0`:

```
P(s) is palindromic   <=>   delta1 = delta2   <=>   gamma1/m1 = gamma2/m2
```

## Oriented comparator theorem

```
sign log(det C2 / det C1)  =  -sign(delta1 - delta2)
```

## Universal balance-slope proposition

At `delta1=delta2=delta`:
```
d/ddelta1 [log(det C2 / det C1)]  =  -4/delta
```
independent of `omega1, omega2, k`.

## Generalized-eigenvalue corollary

For `k>0`, `N := C1^{-1}C2` has four strictly positive real eigenvalues.
`P(s)` is palindromic iff those eigenvalues split into two reciprocal
pairs. Hence: equal specific damping iff palindromic pencil iff reciprocal
eigenvalue pairing of `C1^{-1}C2`.
