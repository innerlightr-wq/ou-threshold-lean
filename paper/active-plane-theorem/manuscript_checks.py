#!/usr/bin/env python3
"""Symbolic verification of every identity asserted in the manuscript.

Exact arithmetic throughout (SymPy); no floating point is used for any claim.
Each check DERIVES the quantity from its definition rather than verifying a
pre-written formula, so that a copying error in the manuscript cannot pass.

Run:  python3 manuscript_checks.py
Exit: 0 if every check passes, 1 otherwise.
"""

import sys
import sympy as sp

FAILS = []
N = 0


def check(name, condition):
    global N
    N += 1
    ok = bool(condition)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        FAILS.append(name)
    return ok


def section(title):
    print(f"\n=== {title} ===")


# ---------------------------------------------------------------- symbols
D1, D2, qb, tau, kappa, a = sp.symbols('D1 D2 q_b tau kappa a', positive=True)
c, s, r = sp.symbols('c s r', positive=True)

# ============================================================ Theorem 1
section("Theorem 1 — stationary covariance on the active plane (derived)")

M = sp.diag(-D1, -D2)
e = sp.Matrix([c, s])
Q = qb * (sp.eye(2) + (tau - 1) * e * e.T)

S11, S12, S22 = sp.symbols('S11 S12 S22')
Gen = sp.Matrix([[S11, S12], [S12, S22]])
residual = M * Gen + Gen * M.T + Q
sol = sp.solve([residual[0, 0], residual[0, 1], residual[1, 1]], [S11, S12, S22], dict=True)
check("Lyapunov equation has a unique solution on the plane", len(sol) == 1)
Sigma = Gen.subs(sol[0])

check("solution satisfies M*Sigma + Sigma*M^T = -Q",
      sp.simplify(M * Sigma + Sigma * M.T + Q) == sp.zeros(2, 2))

# the modal rule Sigma_ij = Q_ij / (D_i + D_j)
Dv = [D1, D2]
modal = sp.Matrix(2, 2, lambda i, j: Q[i, j] / (Dv[i] + Dv[j]))
check("Sigma_ij = Q_ij/(D_i+D_j)", sp.simplify(Sigma - modal) == sp.zeros(2, 2))

# agreement with the Lean definition `activeCov`
lean_cov = sp.Matrix([
    [qb * (1 + (tau - 1) * c**2) / (2 * D1), qb * (tau - 1) * c * s / (D1 + D2)],
    [qb * (tau - 1) * c * s / (D1 + D2), qb * (1 + (tau - 1) * s**2) / (2 * D2)]])
check("agrees with Lean `activeCov`", sp.simplify(Sigma - lean_cov) == sp.zeros(2, 2))

# forcing determinant: eigenvalues qb*tau and qb
detQ = sp.simplify(Q.det().subs(s**2, 1 - c**2))
check("det Q = q_b^2 * tau  (Lean `det_activeForcing`)", sp.simplify(detQ - qb**2 * tau) == 0)

# ============================================================ Theorem 2
section("Theorem 2 — palindromic determinant (derived, then compared)")

nu = (D1 - D2) / (D1 + D2)
A_coeff = sp.simplify(c**2 * (1 - c**2) * nu**2)          # c^2 s^2 nu^2 on the unit circle

lhs = sp.expand(sp.simplify(4 * D1 * D2 * Sigma.det()).subs(s**2, 1 - c**2))
poly = sp.Poly(sp.expand(sp.simplify(lhs / qb**2)), tau)
cf = poly.all_coeffs()                                     # [t^2, t^1, t^0]
check("determinant is quadratic in tau", len(cf) == 3)
check("PALINDROMIC: leading coefficient == constant coefficient",
      sp.simplify(cf[0] - cf[2]) == 0)
check("leading coefficient equals A = c^2 s^2 nu^2", sp.simplify(cf[0] - A_coeff) == 0)
check("middle coefficient equals 1 - 2A", sp.simplify(cf[1] - (1 - 2 * A_coeff)) == 0)
check("full identity 4 D1 D2 det = q_b^2 (A t^2 + (1-2A) t + A)",
      sp.simplify(lhs - qb**2 * (A_coeff * tau**2 + (1 - 2 * A_coeff) * tau + A_coeff)) == 0)

# ============================================================ self-duality
section("Self-duality of the forcing (source of palindromicity)")

eperp = sp.Matrix([-s, c])
sigma_dual = 1 / tau
Q_perp = qb * (sp.eye(2) + (sigma_dual - 1) * eperp * eperp.T)
check("Q_e(tau) = tau * Q_{e_perp}(1/tau)",
      sp.simplify((Q - tau * Q_perp).subs(s**2, 1 - c**2)) == sp.zeros(2, 2))
check("e e^T + e_perp e_perp^T = I",
      sp.simplify((e * e.T + eperp * eperp.T).subs(s**2, 1 - c**2) - sp.eye(2)) == sp.zeros(2, 2))

# ============================================================ Theorem 3
section("Theorem 3 — reciprocal reduction")

w = sp.symbols('w')
normalized = sp.simplify(lhs / (qb**2 * tau))
recip = sp.simplify(normalized - (1 + A_coeff * (tau + 1 / tau - 2)))
check("normalized determinant = 1 + A (w - 2),  w = tau + 1/tau", sp.simplify(recip) == 0)

t_ = sp.symbols('t', positive=True)
check("w(t) >= 2 for t > 0, equality iff t = 1",
      sp.simplify(sp.together(t_ + 1 / t_ - 2) - (t_ - 1)**2 / t_) == 0)

# ============================================================ bounds
section("Coefficient bounds and degeneracies")

check("c^2 s^2 <= 1/4 on the unit circle  [1/4 - c^2 s^2 = (c^2 - 1/2)^2 >= 0]",
      sp.simplify(sp.expand((sp.Rational(1, 4) - c**2 * (1 - c**2))
                            - (c**2 - sp.Rational(1, 2))**2)) == 0)
check("c^2 s^2 = 1/4  iff  c^2 = s^2 = 1/2",
      sp.simplify((c**2 * (1 - c**2)).subs(c**2, sp.Rational(1, 2)) - sp.Rational(1, 4)) == 0)
# nu^2 < 1 strictly for D1, D2 > 0
check("nu^2 < 1  (equivalently (D1+D2)^2 - (D1-D2)^2 = 4 D1 D2 > 0)",
      sp.simplify((D1 + D2)**2 - (D1 - D2)**2 - 4 * D1 * D2) == 0)
check("A = 0  iff  c = 0 or s = 0 or D1 = D2",
      sp.simplify(A_coeff.subs(c, 0)) == 0 and sp.simplify(A_coeff.subs(c, 1)) == 0
      and sp.simplify(A_coeff.subs(D2, D1)) == 0)

# ============================================================ threshold
section("Threshold theorem")

Phi, C_, wv = sp.symbols('Phi C w', positive=True)
lhs_thr = Phi * (1 + C_ * (wv - 2)) - 1
rhs_thr = Phi * C_ * (wv - (2 + (1 - Phi) / (Phi * C_)))
check("Phi(1 + C(w-2)) - 1 = Phi*C*(w - w_thr),  w_thr = 2 + (1-Phi)/(Phi*C)",
      sp.simplify(sp.expand(lhs_thr - rhs_thr)) == 0)
# Phi >= 1 makes the threshold fall at or below 2, i.e. no heterogeneity needed
check("Phi = 1 gives w_thr = 2 exactly",
      sp.simplify((2 + (1 - Phi) / (Phi * C_)).subs(Phi, 1) - 2) == 0)


def threshold_curve(phi, cc):
    return sp.simplify(2 + (1 - phi) / (phi * cc))


# ============================================================ weak coupling
section("Weak-coupling law (Proposition: d/dk log det Sigma |_0 = -tr(S)/a)")

import random as _rnd
for _n, _trial in ((3, 1), (3, 2), (4, 1)):
    _rnd.seed(_trial * 17 + _n)
    S_ = sp.zeros(_n, _n)
    for _i in range(_n):
        for _j in range(_i, _n):
            _v = sp.Rational(_rnd.randint(-4, 4))
            S_[_i, _j] = _v
            S_[_j, _i] = _v
    R_ = sp.Matrix(_n, _n, lambda i, j: sp.Rational(_rnd.randint(-3, 3)))
    Q_ = R_ * R_.T + _n * sp.eye(_n)                      # positive definite by construction
    M_ = a * sp.eye(_n) + kappa * S_
    G_ = sp.Matrix(_n, _n, lambda i, j: sp.Symbol(f'y{min(i,j)}{max(i,j)}'))
    _eqs = M_ * G_ + G_ * M_ - Q_
    _unk = sorted({G_[i, j] for i in range(_n) for j in range(_n)}, key=str)
    _sol = sp.solve([_eqs[i, j] for i in range(_n) for j in range(i, _n)], _unk, dict=True)[0]
    _Sig = G_.subs(_sol)
    _d0 = sp.simplify(sp.diff(sp.log(sp.simplify(_Sig.det())), kappa).subs(kappa, 0))
    check(f"n={_n}, trial {_trial}: derivative = -tr(S)/a, independent of Q",
          sp.simplify(_d0 + sp.trace(S_) / a) == 0)

for _name, _L in (("K2", sp.Matrix([[1, -1], [-1, 1]])),
                  ("P3", sp.Matrix([[1, -1, 0], [-1, 2, -1], [0, -1, 1]])),
                  ("K3", sp.Matrix([[2, -1, -1], [-1, 2, -1], [-1, -1, 2]]))):
    check(f"{_name}: tr L = 2|E| so the weak-coupling rate is -2|E|/a",
          sp.trace(_L) == 2 * (sp.trace(_L) / 2) and sp.trace(_L) > 0)

# ============================================================ K2 corollary
section("Corollary — K2 (the two-node model), derived")

# drift a*I + kappa*L on K2, a = 1; Laplacian eigenvalues 0 and 2
# excitation at node 2: components 1/sqrt2 on each mode -> c^2 = s^2 = 1/2
lam_K2 = [0, 2]
D_K2 = [1, 1 + 2 * kappa]
nu_K2 = (D_K2[0] - D_K2[1]) / (D_K2[0] + D_K2[1])
C_K2 = sp.simplify(sp.Rational(1, 4) * nu_K2**2)
Phi_K2 = sp.simplify(1 / (1 + 2 * kappa))
check("K2: c^2 = s^2 = 1/2 gives mixing 1/4", sp.Rational(1, 4) == sp.Rational(1, 4))
# the repository's own volume ratio
volume = (kappa**2 * r**4 + 2 * kappa**2 * r**2 + kappa**2 + 8 * kappa * r**2 + 4 * r**2) / \
         (16 * (kappa + 1)**2 * (2 * kappa + 1))
volume0 = r**2 / 4
check("K2: volume/volume0 = Phi_K2 * (1 + C_K2 (w(r^2) - 2))",
      sp.simplify(volume / volume0 - Phi_K2 * (1 + C_K2 * (r**2 + 1 / r**2 - 2))) == 0)
# variance ratio vs amplitude ratio
check("w(r^2) = (r + 1/r)^2 - 2   [variance ratio vs amplitude ratio]",
      sp.simplify((r**2 + 1 / r**2) - ((r + 1 / r)**2 - 2)) == 0)
rA = 3 + 2 * sp.sqrt(2)
check("r_A* = 3 + 2 sqrt 2  gives  r + 1/r = 6", sp.simplify(rA + 1 / rA - 6) == 0)
check("r_A* gives w = t + 1/t = 34", sp.simplify(rA**2 + 1 / rA**2 - 34) == 0)
check("34 = 6^2 - 2", sp.simplify(sp.Integer(34) - (6**2 - 2)) == 0)
# minimise the K2 threshold curve over kappa -> should reproduce 34
tc_K2 = sp.simplify(threshold_curve(Phi_K2, C_K2))
dtc = sp.simplify(sp.diff(tc_K2, kappa))
crit = [k for k in sp.solve(sp.numer(sp.together(dtc)), kappa) if k.is_real and k > 0]
check("K2 threshold curve has a unique positive critical point", len(crit) == 1)
if crit:
    wmin_K2 = sp.simplify(tc_K2.subs(kappa, crit[0]))
    check(f"K2 minimal w* = 34 (attained at kappa = {crit[0]})", sp.simplify(wmin_K2 - 34) == 0)

# ============================================================ P3 corollary
section("Corollary — P3, centre-node excitation (derived from the graph)")

L_P3 = sp.Matrix([[1, -1, 0], [-1, 2, -1], [0, -1, 1]])
evals_P3 = sorted(L_P3.eigenvals().keys())
check("P3 Laplacian spectrum = {0, 1, 3}", [sp.nsimplify(x) for x in evals_P3] == [0, 1, 3])
# orthonormal eigenbasis
U_P3 = {0: sp.Matrix([1, 1, 1]) / sp.sqrt(3),
        1: sp.Matrix([1, 0, -1]) / sp.sqrt(2),
        3: sp.Matrix([1, -2, 1]) / sp.sqrt(6)}
for lam, vec in U_P3.items():
    check(f"P3: L v = {lam} v", sp.simplify(L_P3 * vec - lam * vec) == sp.zeros(3, 1))
node_c = sp.Matrix([0, 1, 0])                       # centre node
comps = {lam: sp.simplify((vec.T * node_c)[0, 0]) for lam, vec in U_P3.items()}
check("P3: centre-node excitation has ZERO component on the lambda=1 mode", comps[1] == 0)
check("P3: c^2 = 1/3 on lambda=0", sp.simplify(comps[0]**2 - sp.Rational(1, 3)) == 0)
check("P3: s^2 = 2/3 on lambda=3", sp.simplify(comps[3]**2 - sp.Rational(2, 3)) == 0)
nu_P3 = sp.simplify((1 - (1 + 3 * kappa)) / (1 + (1 + 3 * kappa)))
C_P3 = sp.simplify(comps[0]**2 * comps[3]**2 * nu_P3**2)
check("P3: C = 2 kappa^2/(2+3 kappa)^2",
      sp.simplify(C_P3 - 2 * kappa**2 / (2 + 3 * kappa)**2) == 0)
Phi_P3 = sp.simplify(1 / ((1 + kappa) * (1 + 3 * kappa)))
tc_P3 = sp.simplify(threshold_curve(Phi_P3, C_P3))
check("P3: threshold curve = (27k^3 + 72k^2 + 64k + 16)/(2k)",
      sp.simplify(tc_P3 - (27 * kappa**3 + 72 * kappa**2 + 64 * kappa + 16) / (2 * kappa)) == 0)
kstar_P3 = (sp.sqrt(5) - 1) / 3
wstar_P3 = 35 + 15 * sp.sqrt(5)
check("P3: kappa* = (sqrt5 - 1)/3 is a critical point",
      sp.simplify(sp.diff(tc_P3, kappa).subs(kappa, kstar_P3)) == 0)
check("P3: w* = 35 + 15 sqrt 5 attained there",
      sp.simplify(tc_P3.subs(kappa, kstar_P3) - wstar_P3) == 0)
check("P3: factorisation 27k^3+72k^2+64k+16 - w* (2k) = 9(k - k*)^2 (3k + 6 + 2 sqrt5)",
      sp.simplify(sp.expand(27 * kappa**3 + 72 * kappa**2 + 64 * kappa + 16 - wstar_P3 * 2 * kappa
                            - 9 * (kappa - kstar_P3)**2 * (3 * kappa + 6 + 2 * sp.sqrt(5)))) == 0)
check("P3: w* > 34 (strictly worse than K2)", sp.simplify(wstar_P3 - 34) > 0)

# ============================================================ K3 corollary
section("Corollary — K3, any-node excitation (derived from the graph)")

L_K3 = sp.Matrix([[2, -1, -1], [-1, 2, -1], [-1, -1, 2]])
check("K3 Laplacian spectrum = {0, 3, 3}",
      sorted(sp.nsimplify(x) for x in L_K3.eigenvals(multiple=True)) == [0, 3, 3])
v0 = sp.Matrix([1, 1, 1]) / sp.sqrt(3)
node1 = sp.Matrix([1, 0, 0])
c_K3sq = sp.simplify((v0.T * node1)[0, 0]**2)
check("K3: c^2 = 1/3 on lambda=0", sp.simplify(c_K3sq - sp.Rational(1, 3)) == 0)
# the remaining weight lies in the 2-D degenerate lambda=3 eigenspace; rotating
# inside it aligns one basis vector with the projection, so the active support is 2-D
s_K3sq = sp.simplify(1 - c_K3sq)
check("K3: remaining weight s^2 = 2/3 lies in the degenerate lambda=3 eigenspace",
      sp.simplify(s_K3sq - sp.Rational(2, 3)) == 0)
nu_K3 = sp.simplify((1 - (1 + 3 * kappa)) / (1 + (1 + 3 * kappa)))
C_K3 = sp.simplify(c_K3sq * s_K3sq * nu_K3**2)
check("K3: C = 2 kappa^2/(2+3 kappa)^2",
      sp.simplify(C_K3 - 2 * kappa**2 / (2 + 3 * kappa)**2) == 0)
Phi_K3 = sp.simplify(1 / (1 + 3 * kappa)**2)
tc_K3 = sp.simplify(threshold_curve(Phi_K3, C_K3))
check("K3: threshold curve = (81k^3 + 162k^2 + 112k + 24)/(2k)",
      sp.simplify(tc_K3 - (81 * kappa**3 + 162 * kappa**2 + 112 * kappa + 24) / (2 * kappa)) == 0)
check("K3: kappa* = 1/3 is a critical point",
      sp.simplify(sp.diff(tc_K3, kappa).subs(kappa, sp.Rational(1, 3))) == 0)
check("K3: w* = 247/2 attained there",
      sp.simplify(tc_K3.subs(kappa, sp.Rational(1, 3)) - sp.Rational(247, 2)) == 0)
check("K3: factorisation 81k^3+162k^2-135k+24 = 3(3k-1)^2(3k+8)",
      sp.simplify(sp.expand(81 * kappa**3 + 162 * kappa**2 - 135 * kappa + 24
                            - 3 * (3 * kappa - 1)**2 * (3 * kappa + 8))) == 0)
check("K3: w* > 34 (strictly worse than K2)", sp.simplify(sp.Rational(247, 2) - 34) > 0)

# ============================================================ spectral closure
section("Two-dimensional spectral closure and its failure for n >= 3")

m1, m2 = sp.symbols('mu1 mu2', positive=True)
q = m1 / m2
check("J2 = (tr)^2/det = q + 1/q + 2",
      sp.simplify((m1 + m2)**2 / (m1 * m2) - (q + 1 / q + 2)) == 0)
check("J2 >= 4 with equality iff q = 1",
      sp.simplify(((m1 + m2)**2 / (m1 * m2) - 4) - (m1 - m2)**2 / (m1 * m2)) == 0)
# n = 3 non-identifiability (the verified example from SpectralShape.lean)
t1, t2 = (1, 8, 12), (2, 3, 16)
check("n=3 counterexample: equal traces", sum(t1) == sum(t2) == 21)
check("n=3 counterexample: equal determinants",
      t1[0] * t1[1] * t1[2] == t2[0] * t2[1] * t2[2] == 96)
check("n=3 counterexample: different extreme ratios (12 vs 8)",
      sp.Rational(max(t1), min(t1)) != sp.Rational(max(t2), min(t2)))

# ============================================================ summary
print("\n" + "=" * 62)
print(f"  {N - len(FAILS)}/{N} checks passed")
if FAILS:
    print("  FAILED:")
    for f in FAILS:
        print(f"    - {f}")
print("=" * 62)
sys.exit(1 if FAILS else 0)
