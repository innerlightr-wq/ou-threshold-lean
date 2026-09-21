# Proof outline

See [`theorem.md`](theorem.md) for statements and
[`computer_assisted_proof.md`](computer_assisted_proof.md) for the
computer-algebra disclosure. This is a condensed proof sketch; the full
manuscript (`paper/inertial/main.tex`) has complete derivations.

## Lemma 1 — Pencil and positivity

`Sigma(T1,T2)=T1*C1+T2*C2` (linearity of the Lyapunov equation in the
forcing). `c4=det(C1)`, `c0=det(C2)` (the `s^4`/`s^0` coefficients of
`det(sC1+C2)`, by multilinearity of `det`). For `k>0`, `C1,C2 ≻ 0`
(single-bath Kalman/Krylov controllability determinant `=k^2` exactly;
`k=0` is the sole boundary degeneracy, where the drift decouples into two
independent blocks).

## Lemma 2 — Sufficiency

`delta1=delta2 => c4=c0` and `c3=c1` (full palindromicity), for all
`omega1,omega2,k,delta>0`. Shortest known proof: substitute `delta1=delta2
=delta` directly into the Lyapunov equations before solving (this is a
genuine structural simplification, not merely "one fewer unknown" — the
common damping commutes with the stiffness-diagonalizing rotation, see
Lemma 3's derivation), solve for `C1(delta),C2(delta)` symbolically, and
confirm `det(sC1+C2)`'s coefficient symmetry by exact simplification to
zero.

## Lemma 3 — Derivative factorization and positivity

Write `F := log(det C2/det C1)`. The exact identity
```
F' = Ktotal(omega1,omega2,k) * delta1^3*delta2^4 / [K(delta1,delta2)^4 * det(C1)*det(C2)]

K = a1*d1^3d2+a2*d1^2d2^2+a3*d1^2+a4*d1d2^3+a5*d1d2+a6*d2^2
a1=omega2^2+k,  a2=omega1^2+omega2^2+2k,  a3=k^2
a4=omega1^2+k,  a5=(omega1^2-omega2^2)^2+2k^2,  a6=k^2

Ktotal = -4k^8/Delta^2,   Delta = k*omega1^2+k*omega2^2+omega1^2*omega2^2
```
`K>0` (sum of six manifestly positive terms) and `Ktotal<0` (a negative
constant times a positive quantity) each follow in one line. Since
`det(C1),det(C2)>0` (Lemma 1) and `delta1,delta2>0`, `F'<0` everywhere.

### Balance-slope proposition

At `delta1=delta2=delta`, the p-block damping matrix is `delta*I`, which
commutes with the orthogonal transform diagonalizing the stiffness block
`[[omega1^2+k,-k],[-k,omega2^2+k]]`. This decouples the deterministic
drift into two independent damped oscillators (common damping `delta`,
normal-mode frequencies `Omega1,Omega2`), with per-bath noise becoming a
rank-1 source correlated across the two decoupled modes. Each mode's
self-covariance solves via the classical single-oscillator equipartition
identity; the cross-mode correlation solves a 2x2 Sylvester equation in
closed form. Feeding the resulting closed-form `C1(delta),C2(delta)` into
the adjoint-Lyapunov sensitivity identity gives `F'=-4/delta` exactly,
with all `omega1,omega2,k`-dependence cancelling.

## Theorem 1 — Global monotonicity and oriented comparator

`F'<0` everywhere (Lemma 3) plus the base point `F(delta2,delta2)=0`
(immediate corollary of Lemma 2) gives: `F` strictly decreasing in
`delta1`, single zero at `delta1=delta2`, hence
`sign(F)=-sign(delta1-delta2)`. Corollary: `det C1=det C2 <=> delta1=delta2`.

## Theorem 2 — Palindromicity iff equal specific damping

Necessity: `palindromic => c4=c0 => det C1=det C2 => delta1=delta2`
(Theorem 1's corollary — `c3=c1` is never needed for necessity).
Sufficiency: Lemma 2. Hence `P(s)` palindromic iff `delta1=delta2` iff
`gamma1/m1=gamma2/m2`.

## Corollaries

- **Generalized eigenvalues**: `N=C1^{-1}C2` has four positive real
  eigenvalues for `k>0`; palindromicity iff reciprocal pairing.
- **`w=s+1/s` reduction**: on `delta1=delta2`, `P(s)/s^2 = c4*w^2+c3*w+
  (c2-2c4)`, a genuine quadratic.
