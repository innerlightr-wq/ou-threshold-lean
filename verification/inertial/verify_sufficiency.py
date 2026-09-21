"""
Verifies: delta1=delta2 => P(s)=det(sC1+C2) is palindromic (c4=c0 and
c3=c1), for ALL admissible omega1,omega2,k,delta>0 (fully symbolic, no
restriction on any parameter).

Method: exact symbolic computation. C1(delta), C2(delta) are solved
directly (SymPy linsolve) with delta1=delta2=delta substituted from the
start; det(s*C1+C2) is expanded and its s^4/s^0 and s^3/s^1 coefficients
are compared via sp.simplify(...)==0. This is an exact computer-algebra
identity check (symbolic simplification to zero), not a numerical or
floating-point verification.
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
    log(f"C1(delta), C2(delta) solved symbolically. [{time.time() - t0:.1f}s]")

    # c4=det(sC1+C2)'s s^4 coefficient = det(C1); c0 = det(C2). c3,c1 are the
    # classical multilinear (mixed-determinant) expansion coefficients: sum
    # over the four ways to replace one column of C1 by the corresponding
    # column of C2 (resp. C2 by C1). This avoids expanding the full quartic
    # pencil determinant in s, which is far more expensive for these
    # particular rational-function entries.
    c4 = sp.together(C1.det(method='berkowitz'))
    c0 = sp.together(C2.det(method='berkowitz'))

    def mixed(cols_primary, cols_other, swap_col):
        M = cols_primary.copy()
        M[:, swap_col] = cols_other[:, swap_col]
        return M.det(method='berkowitz')

    c3 = sum(mixed(C1, C2, j) for j in range(4))
    c1 = sum(mixed(C2, C1, j) for j in range(4))
    log(f"c4,c0,c3,c1 computed via direct determinant + mixed-determinant "
        f"expansion. [{time.time() - t0:.1f}s]")

    diff_c4c0 = sp.simplify(c4 - c0)
    diff_c3c1 = sp.simplify(c3 - c1)
    log(f"c4 - c0 = {diff_c4c0}   [{time.time() - t0:.1f}s]")
    log(f"c3 - c1 = {diff_c3c1}   [{time.time() - t0:.1f}s]")

    assert diff_c4c0 == 0, "SUFFICIENCY FAILS: c4 != c0 at delta1=delta2"
    assert diff_c3c1 == 0, "SUFFICIENCY FAILS: c3 != c1 at delta1=delta2"

    print(f"\nVERIFIED: delta1=delta2 => P(s) palindromic, for all "
          f"omega1,omega2,k,delta>0 (exact symbolic proof, {time.time()-t0:.1f}s).")


if __name__ == "__main__":
    main()
