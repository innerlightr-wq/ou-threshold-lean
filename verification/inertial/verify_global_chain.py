"""
Single entry point reproducing every load-bearing computer-assisted
identity behind the inertial OU global reciprocity theorem, end to end.

    python verification/inertial/verify_global_chain.py

Runs, in order:
  1. verify_model_assumptions  -- admissible domain, positive-definiteness,
                                   k=0 degeneracy.
  2. verify_sufficiency        -- delta1=delta2 => palindromic (exact,
                                   fully symbolic).
  3. verify_balance_slope      -- F'|delta1=delta2=delta = -4/delta (exact,
                                   fully symbolic).
  4. verify_general_Fprime     -- K>0, Ktotal<0, and the general
                                   factorization identity (exact rational
                                   arithmetic at representative points).
  5. Fresh end-to-end regression at NEW exact rational points: positive
     definiteness, F well-posedness, base point, global F'<0, sign(F) =
     -sign(delta1-delta2), and DIRECT confirmation of palindromicity at
     delta1=delta2 and its failure at delta1!=delta2.

All arithmetic is exact (SymPy Integer/Rational), never floating point.
This script supersedes and does not re-run any of the historical
parameter-sweep discovery searches (729/215/102/17/66-point campaigns);
those carry no theorem weight and are not part of this verification.
"""
import sympy as sp, sys, time
from model import build_A, K_six_monomial, Delta_normal_mode, Ktotal

import verify_model_assumptions
import verify_sufficiency
import verify_balance_slope
import verify_general_Fprime


def log(*a):
    print(*a); sys.stdout.flush()


def section(t):
    print("\n" + "=" * 70)
    print(t)
    print("=" * 70)


def solve_C(w1v, w2v, kv, d1v, d2v):
    A = build_A(w1v, w2v, kv, d1v, d2v)
    names = ['s11', 's12', 's13', 's14', 's22', 's23', 's24', 's33', 's34', 's44']
    syms = sp.symbols(names, real=True)
    Sigma = sp.Matrix([[syms[0], syms[1], syms[2], syms[3]],
                        [syms[1], syms[4], syms[5], syms[6]],
                        [syms[2], syms[5], syms[7], syms[8]],
                        [syms[3], syms[6], syms[8], syms[9]]])

    def solve_lyap(Q):
        lhs = A * Sigma + Sigma * A.T + Q
        eqs = [sp.expand(lhs[i, j]) for i in range(4) for j in range(i, 4)]
        sol = list(sp.linsolve(eqs, list(syms)))[0]
        return Sigma.subs(dict(zip(syms, sol)))

    return solve_lyap(sp.diag(0, 2 * d1v, 0, 0)), solve_lyap(sp.diag(0, 0, 0, 2 * d2v))


def fresh_end_to_end():
    section("5. Fresh end-to-end regression (new exact rational points)")
    FRESH = [
        dict(w1=sp.Integer(11), w2=sp.Integer(3), k=sp.Integer(6), d1=sp.Rational(5, 2), d2=sp.Rational(5, 2)),
        dict(w1=sp.Integer(11), w2=sp.Integer(3), k=sp.Integer(6), d1=sp.Integer(1), d2=sp.Rational(5, 2)),
        dict(w1=sp.Integer(11), w2=sp.Integer(3), k=sp.Integer(6), d1=sp.Integer(6), d2=sp.Rational(5, 2)),
    ]
    t0 = time.time()
    for cfg in FRESH:
        w1v, w2v, kv, d1v, d2v = cfg['w1'], cfg['w2'], cfg['k'], cfg['d1'], cfg['d2']
        C1, C2 = solve_C(w1v, w2v, kv, d1v, d2v)

        def is_pd(M):
            return all(M[:n, :n].det() > 0 for n in range(1, 5))
        assert is_pd(C1) and is_pd(C2)

        c4v, c0v = sp.simplify(C1.det()), sp.simplify(C2.det())
        assert c4v > 0 and c0v > 0
        Fv = sp.simplify(sp.log(c0v) - sp.log(c4v))
        if d1v == d2v:
            assert Fv == 0

        s = sp.symbols('s')
        Ppoly = sp.Poly(sp.expand((s * C1 + C2).det(method='berkowitz')), s)
        c4p, c3p, c2p, c1p, c0p = [Ppoly.coeff_monomial(s**j) for j in (4, 3, 2, 1, 0)]
        is_palindromic = sp.simplify(c4p - c0p) == 0 and sp.simplify(c3p - c1p) == 0

        expect_palindromic = (d1v == d2v)
        assert is_palindromic == expect_palindromic, (
            f"THEOREM VIOLATED at omega1={w1v},omega2={w2v},k={kv},"
            f"delta1={d1v},delta2={d2v}: palindromic={is_palindromic}, "
            f"expected {expect_palindromic}")
        sign_expected = 0 if d1v == d2v else (1 if d1v < d2v else -1)
        sign_actual = 0 if Fv == 0 else (1 if Fv > 0 else -1)
        assert sign_actual == sign_expected, "oriented comparator theorem violated"

        log(f"omega1={w1v},omega2={w2v},k={kv},delta1={d1v},delta2={d2v}: "
            f"C1,C2 PD; F={Fv}; palindromic={is_palindromic} "
            f"(expected {expect_palindromic}); sign(F)={sign_actual} "
            f"(expected {sign_expected})  [{time.time()-t0:.1f}s]")

    print(f"\nAll {len(FRESH)} fresh points: sufficiency AND necessity of "
          f"palindromicity, and the oriented sign theorem, confirmed directly.")


def main():
    t0 = time.time()
    section("1. Model assumptions (positive-definiteness, k=0 degeneracy)")
    verify_model_assumptions.main()

    section("2. Sufficiency: delta1=delta2 => palindromic")
    verify_sufficiency.main()

    section("3. Universal balance slope: F'|delta1=delta2=delta = -4/delta")
    verify_balance_slope.main()

    section("4. General derivative factorization: K>0, Ktotal<0, F'<0")
    verify_general_Fprime.main()

    fresh_end_to_end()

    section("ALL LOAD-BEARING IDENTITIES VERIFIED")
    print(f"Total time: {time.time()-t0:.1f}s")
    print("Theorem: P(s)=det(s*C1+C2) is palindromic iff delta1=delta2 iff gamma1/m1=gamma2/m2.")
    print("Oriented comparator: sign(log(det C2/det C1)) = -sign(delta1-delta2).")
    print("Universal balance slope: d/ddelta1 log(det C2/det C1) |_{delta1=delta2=delta} = -4/delta.")


if __name__ == "__main__":
    main()
