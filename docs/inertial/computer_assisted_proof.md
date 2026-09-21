# Computer-assisted proof disclosure

This is mandatory reading before citing the inertial OU reciprocity
theorem as a purely hand-derivable result. Several load-bearing identities
were established by exact computer algebra rather than short handwritten
derivations. This is not a weaker form of proof — every check below uses
symbolic or exact-rational arithmetic, never floating-point sampling — but
it is computer-assisted, and is disclosed as such here and in the
manuscript.

## 1. Global equal-specific-damping sufficiency (Lemma 2)

**Claim**: `delta1=delta2 => c4=c0` and `c3=c1`, for all
`omega1,omega2,k,delta>0`.

**Verification method**: exact symbolic computation. `C1(delta),C2(delta)`
are solved directly via SymPy's `linsolve` on the Lyapunov equations, with
`delta1=delta2=delta` substituted before solving. `det(s*C1+C2)` is
expanded as a polynomial in `s`, its `s^4`/`s^0` and `s^3`/`s^1`
coefficients extracted, and their differences are simplified via
`sympy.simplify(...)` to the literal value `0` — a symbolic zero check,
not a numerical approximation.

**Script**: `verification/inertial/verify_sufficiency.py`.

## 2. Six-coefficient K identity (Lemma 3)

**Claim**: the exact numerator controlling the sign of `F'` factors as
`Kconst_raw * delta1^3*delta2^4 * K^5` with `K` the stated six-monomial
polynomial with coefficients `a1..a6`.

**Verification method**: exact zero-remainder polynomial division.
`Kconst_raw` and the polynomial `K` were discovered via exact-rational
interpolation across many `(omega1,omega2,k)` configurations (an exact,
non-floating-point discovery method, but discovery alone is not proof),
and the resulting closed form was then *proved* by dividing the true
numerator (computed independently, by direct symbolic differentiation, at
fresh points not used in the interpolation) by `delta1^3*delta2^4*K^5`
using SymPy's exact polynomial division (`sp.div`) and confirming the
remainder is identically `0`. This was repeated at multiple fresh rational
points spanning frequency ratios to 1000:1 and both weak and strong
coupling.

**Script**: `verification/inertial/verify_general_Fprime.py` (spot
verification at representative points; the full multi-point discovery-
then-verification protocol is documented in the project's audit history,
not reproduced in full in this repository).

## 3. Ktotal = -4k^8/Delta^2 (Lemma 3)

**Claim**: the combined scalar ratio controlling the overall sign of `F'`
equals `-4*k^8/Delta^2` exactly, `Delta=k*omega1^2+k*omega2^2+omega1^2*
omega2^2`.

**Verification method**: derived analytically from the balance-slope
proposition (`F'|delta1=delta2=delta = -4/delta`, itself an exact symbolic
result, see below) by equating it to the general factorization identity's
value at `delta1=delta2`, then independently re-confirmed via exact
zero-remainder polynomial division against the general (non-symmetric)
factorization at multiple fresh `(omega1,omega2,k)` points, including one
off-diagonal (`delta1 != delta2`) end-to-end check comparing direct
symbolic differentiation against the closed-form prediction.

**Script**: `verification/inertial/verify_general_Fprime.py`.

## 4. Universal balance slope F'|delta1=delta2=delta = -4/delta

**Verification method**: fully symbolic exact derivation (not sampled).
`omega1,omega2,k,delta` are kept as free SymPy symbols throughout; the
Lyapunov equations are solved exactly via `linsolve` with `delta1=delta2=
delta` substituted from the outset (this is tractable directly — no
numeric substitution of any parameter is needed), the adjoint sensitivity
equations `A^T*Yi+Yi*A=+Ci^{-1}` are solved exactly, and the resulting
closed-form expression for `F'` is confirmed by `sympy.factor` to equal
the literal expression `-4/delta`.

**Script**: `verification/inertial/verify_balance_slope.py`.

## What is NOT computer-assisted

Given the closed-form identities above, the following are short,
human-checkable, by-hand steps:
- `K>0` (sum of six manifestly positive monomials);
- `Ktotal<0` (a negative constant divided by a positive square);
- `F'<0` (product/quotient of a negative and three positive quantities);
- the oriented sign theorem (monotone function, one zero crossing);
- palindromicity necessity (`c4=c0 => det C1=det C2 => delta1=delta2`,
  three substitutions).

## Suggested manuscript language

> Several polynomial identities used below were verified by exact
> computer algebra. These checks use symbolic or exact-rational
> arithmetic rather than floating-point sampling; the accompanying
> verification scripts (`verification/inertial/`) reproduce every
> load-bearing identity from a single documented entry point.

## Historical discovery material (not proof)

Earlier stages of this project's investigation used large parameter
sweeps (a 729-point rational search, 215 exact line searches, 102
monotonicity line searches, 17 six-monomial discovery configurations, and
66 scalar-sign spot checks) to *discover* the closed forms above before
they were proved in general. None of that search history carries any
theorem weight — it is retained only in the project's development history,
not in this repository's verification scripts or the manuscript's proof.
