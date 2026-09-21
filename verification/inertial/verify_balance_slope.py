"""
Verifies the universal balance-slope identity: at delta1=delta2=delta,

    F'(delta1) := d/ddelta1 [log(det C2) - log(det C1)]  =  -4/delta

exactly, for ALL omega1,omega2,k,delta>0 (fully symbolic).

Method: exact symbolic computation via the adjoint-Lyapunov route.
Y1, Y2 solve A^T*Yi+Yi*A = +Ci^{-1} (note the sign: positive, not
negative); F' = 2*[e2^T*Y2*v2 - e2^T*Y1*u1], u1=C1*e2-e2, v2=C2*e2. This
is an exact symbolic derivation, not sampled at numeric points.
"""
import sympy as sp, sys, time
from model import build_A


def log(*a):
    print(*a); sys.stdout.flush()


def main():
    t0 = time.time()
    w1, w2, k, delta = sp.symbols('omega1 omega2 k delta', positive=True, real=True)

    A = build_A(w1, w2, k, delta, delta)
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

    C1 = solve_lyap(sp.diag(0, 2 * delta, 0, 0))
    C2 = solve_lyap(sp.diag(0, 0, 0, 2 * delta))
    log(f"C1, C2 solved. [{time.time()-t0:.1f}s]")

    c4 = sp.factor(C1.det(method='berkowitz'))
    c0 = sp.factor(C2.det(method='berkowitz'))
    assert sp.simplify(c4 - c0) == 0, "base-point lemma failed: det C1 != det C2 at delta1=delta2"
    log("Base-point lemma confirmed: det(C1) = det(C2) at delta1=delta2.")

    C1inv, C2inv = C1.inv(), C2.inv()

    Yn = sp.symbols('y11 y12 y13 y14 y22 y23 y24 y33 y34 y44', real=True)
    y11, y12, y13, y14, y22, y23, y24, y33, y34, y44 = Yn
    Y = sp.Matrix([[y11, y12, y13, y14],
                    [y12, y22, y23, y24],
                    [y13, y23, y33, y34],
                    [y14, y24, y34, y44]])

    def solve_Y(Cinv):
        lhs = A.T * Y + Y * A - Cinv  # A^T Yi + Yi A = +Ci^{-1}
        eqs = [sp.together(lhs[i, j]) for i in range(4) for j in range(i, 4)]
        sol = list(sp.linsolve(eqs, list(Yn)))[0]
        return Y.subs(dict(zip(Yn, sol)))

    Y1, Y2 = solve_Y(C1inv), solve_Y(C2inv)
    log(f"Y1, Y2 solved. [{time.time()-t0:.1f}s]")

    e2 = sp.Matrix([0, 1, 0, 0])
    u1 = C1 * e2 - e2
    v2 = C2 * e2
    Fprime = sp.factor(sp.together(2 * ((e2.T * Y2 * v2)[0] - (e2.T * Y1 * u1)[0])))

    log(f"F'(delta1)|_{{delta1=delta2=delta}} = {Fprime}")
    assert Fprime == -4 / delta, f"UNEXPECTED RESULT: {Fprime}"

    print(f"\nVERIFIED: F'|_delta1=delta2=delta = -4/delta exactly, for all "
          f"omega1,omega2,k,delta>0 ({time.time()-t0:.1f}s).")


if __name__ == "__main__":
    main()
