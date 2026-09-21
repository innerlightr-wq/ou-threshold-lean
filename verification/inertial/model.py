"""
Shared exact model definitions for the two-mode inertial Ornstein-Uhlenbeck
reciprocity theorem (unit-mass reduction).

State ordering: (x1, p1, x2, p2). Drift matrix A, per-bath diffusion
matrices Q1, Q2, and the stationary single-bath covariances C1, C2
(solutions of A*Ci + Ci*A^T = -Qi) are exactly as used throughout the
inertial-OU audit chain that produced this theorem.

Admissible domain: omega1 > 0, omega2 > 0, k > 0, delta1 > 0, delta2 > 0.
k > 0 is required for controllability (C1, C2 positive definite); k = 0 is
the sole boundary degeneracy (see verify_model_assumptions.py).
"""
import sympy as sp


def build_A(w1, w2, k, d1, d2):
    return sp.Matrix([
        [0, 1, 0, 0],
        [-(w1**2 + k), -d1, k, 0],
        [0, 0, 0, 1],
        [k, 0, -(w2**2 + k), -d2],
    ])


def solve_stationary_covariances(w1, w2, k, d1, d2):
    """Solve A*C1+C1*A^T=-Q1 and A*C2+C2*A^T=-Q2 exactly via linsolve."""
    A = build_A(w1, w2, k, d1, d2)
    names = ['s11', 's12', 's13', 's14', 's22', 's23', 's24', 's33', 's34', 's44']
    syms = sp.symbols(names, real=True)
    s11, s12, s13, s14, s22, s23, s24, s33, s34, s44 = syms
    Sigma = sp.Matrix([[s11, s12, s13, s14],
                        [s12, s22, s23, s24],
                        [s13, s23, s33, s34],
                        [s14, s24, s34, s44]])

    def solve_lyap(Q):
        lhs = A * Sigma + Sigma * A.T + Q
        eqs = [sp.expand(lhs[i, j]) for i in range(4) for j in range(i, 4)]
        sol = list(sp.linsolve(eqs, list(syms)))[0]
        return Sigma.subs(dict(zip(syms, sol)))

    C1 = solve_lyap(sp.diag(0, 2 * d1, 0, 0))
    C2 = solve_lyap(sp.diag(0, 0, 0, 2 * d2))
    return C1, C2


def K_six_monomial(w1, w2, k, d1, d2):
    """The exact six-monomial damping polynomial controlling the sign of
    dF/ddelta1, with coefficients a1..a6 (each manifestly positive for
    omega1,omega2,k>0)."""
    a1 = w2**2 + k
    a2 = w1**2 + w2**2 + 2 * k
    a3 = k**2
    a4 = w1**2 + k
    a5 = (w1**2 - w2**2)**2 + 2 * k**2
    a6 = k**2
    return a1 * d1**3 * d2 + a2 * d1**2 * d2**2 + a3 * d1**2 \
        + a4 * d1 * d2**3 + a5 * d1 * d2 + a6 * d2**2


def Delta_normal_mode(w1, w2, k):
    """Delta = k*omega1^2 + k*omega2^2 + omega1^2*omega2^2 = product of the
    squared normal-mode frequencies of the stiffness block."""
    return k * w1**2 + k * w2**2 + w1**2 * w2**2


def Ktotal(w1, w2, k):
    """The scalar prefactor Ktotal = -4*k^8/Delta^2, manifestly negative
    for k>0. Controls sign(dF/ddelta1) together with K_six_monomial."""
    return -4 * k**8 / Delta_normal_mode(w1, w2, k)**2
