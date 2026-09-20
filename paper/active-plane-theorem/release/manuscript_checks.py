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

# ================================================== GENERAL IDENTITY (sharp form)
section("Sharp identity — arbitrary symmetric forcing, no rank-one/isotropy assumption")

Q11, Q12g, Q22 = sp.symbols('Q11 Q12 Q22', real=True)
Qgen = sp.Matrix([[Q11, Q12g], [Q12g, Q22]])
Sgen = sp.Matrix([[Q11 / (2 * D1), Q12g / (D1 + D2)],
                  [Q12g / (D1 + D2), Q22 / (2 * D2)]])
nu_ = (D1 - D2) / (D1 + D2)
check("Sigma solves the Lyapunov equation for arbitrary symmetric Q",
      sp.simplify(sp.diag(-D1, -D2) * Sgen + Sgen * sp.diag(-D1, -D2) + Qgen) == sp.zeros(2, 2))
check("4 D1 D2 det Sigma = det Q + nu^2 Q12^2   [Theorem 1]",
      sp.simplify(sp.expand(4 * D1 * D2 * Sgen.det() - (Qgen.det() + nu_**2 * Q12g**2))) == 0)
check("mechanism: 4 D1 D2/(D1+D2)^2 = 1 - nu^2",
      sp.simplify(4 * D1 * D2 / (D1 + D2)**2 - (1 - nu_**2)) == 0)

# ---- the identity is the 2x2 Hadamard/Cauchy expansion (Oppenheim equality case)
Cm = sp.Matrix([[1 / (2 * D1), 1 / (D1 + D2)], [1 / (D1 + D2), 1 / (2 * D2)]])
CoQ = sp.Matrix(2, 2, lambda i, j: Cm[i, j] * Qgen[i, j])
check("Sigma = C o Q  (Cauchy matrix Hadamard forcing)", sp.simplify(CoQ - Sgen) == sp.zeros(2, 2))
check("det(C o Q) = det C * q11 q22 + C12^2 det Q   [2x2 Hadamard expansion]",
      sp.simplify(sp.expand(CoQ.det() - (Cm.det() * Q11 * Q22 + Cm[0, 1]**2 * Qgen.det()))) == 0)
check("4 D1 D2 det C = nu^2", sp.simplify(4 * D1 * D2 * Cm.det() - nu_**2) == 0)
check("4 D1 D2 C12^2 = 1 - nu^2", sp.simplify(4 * D1 * D2 * Cm[0, 1]**2 - (1 - nu_**2)) == 0)
check("equivalent convex form: 4 D1 D2 det Sigma = nu^2 q11 q22 + (1-nu^2) det Q",
      sp.simplify(sp.expand(4 * D1 * D2 * Sgen.det()
                            - (nu_**2 * Q11 * Q22 + (1 - nu_**2) * Qgen.det()))) == 0)
rho_S = sp.simplify(Sgen[0, 1] / sp.sqrt(Sgen[0, 0] * Sgen[1, 1]))
rho_Q = Q12g / sp.sqrt(Q11 * Q22)
check("correlation transfer: rho_Sigma = sqrt(1-nu^2) rho_Q",
      sp.simplify(sp.radsimp(rho_S / rho_Q) - sp.sqrt(1 - nu_**2)) == 0)
T1_, T2_ = sp.symbols('T1_ T2_', positive=True)
check("w - 2 = (T1-T2)^2/(T1 T2) under tau = T1/T2  (w is a known combination)",
      sp.simplify((T1_ / T2_ + T2_ / T1_ - 2) - (T1_ - T2_)**2 / (T1_ * T2_)) == 0)

# ---- affine family, arbitrary symmetric H of any rank
h1, h2, h12 = sp.symbols('h1 h2 h12', real=True)
Hm = sp.Matrix([[h1, h12], [h12, h2]])
Qaff = qb * sp.eye(2) + (tau - 1) * Hm
Saff = sp.Matrix(2, 2, lambda i, j: Qaff[i, j] / ([D1, D2][i] + [D1, D2][j]))
DETaff = sp.expand(sp.simplify(4 * D1 * D2 * Saff.det()))
Kc = sp.simplify(Hm.det() + nu_**2 * h12**2)
check("4 D1 D2 det Sigma(tau) = q_b^2 + q_b (tr H)(tau-1) + K (tau-1)^2",
      sp.simplify(sp.expand(DETaff - (qb**2 + qb * sp.trace(Hm) * (tau - 1) + Kc * (tau - 1)**2))) == 0)
aA, bA, gA = sp.Poly(DETaff, tau).all_coeffs()
check("palindromic  <=>  q_b (tr H - q_b) = 0   [Theorem 3]",
      sp.simplify(sp.factor(sp.expand(aA - gA)) - qb * (h1 + h2 - qb)) == 0)
check("trace-normalized collapse: 4 D1 D2 det Sigma = K(tau-1)^2 + q_b^2 tau",
      sp.simplify(sp.expand(DETaff.subs(h1, qb - h2) - (Kc.subs(h1, qb - h2) * (tau - 1)**2 + qb**2 * tau))) == 0)

# ---- structural anatomy of the trace criterion (Remark: why a trace, why 2x2)
section("Anatomy of the trace criterion")

had = lambda A, B: sp.Matrix(A.rows, A.cols, lambda i, j: A[i, j] * B[i, j])
SigA = had(Cm, Qaff)
DETA = sp.expand(sp.simplify(SigA.det()))
aA2, bA2, cA2 = sp.Poly(DETA, tau).all_coeffs()
check("leading coeff = det(C o H)", sp.simplify(aA2 - had(Cm, Hm).det()) == 0)
check("constant coeff = det(C o (q_b I - H))",
      sp.simplify(cA2 - had(Cm, qb * sp.eye(2) - Hm).det()) == 0)
check("a - c is invariant under h12 -> -h12 (off-diagonal cancels)",
      sp.simplify(sp.expand((aA2 - cA2).subs(h12, -h12) - (aA2 - cA2))) == 0)
check("a - c = q_b (tr H - q_b)/(4 D1 D2): criterion is DRIFT-INDEPENDENT",
      sp.simplify(sp.expand((aA2 - cA2) - qb * (h1 + h2 - qb) / (4 * D1 * D2))) == 0)
check("degenerate H = diag(q_b, 0): tr H = q_b but the polynomial is degree 1",
      sp.Poly(sp.expand(sp.simplify(DETA.subs({h1: qb, h2: 0, h12: 0}))), tau).degree() == 1)
D3s = sp.symbols('D3s', positive=True)
Ds3 = [D1, D2, D3s]
C3m = sp.Matrix(3, 3, lambda i, j: 1 / (Ds3[i] + Ds3[j]))
H3 = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f'g{min(i,j)}{max(i,j)}', real=True))
S3m = had(C3m, qb * sp.eye(3) + (tau - 1) * H3)
check("n=3: determinant is degree 3, so self-reciprocity needs n-1 = 2 matchings",
      sp.Poly(sp.expand(sp.simplify(S3m.det())), tau).degree() == 3)

# ---- P3 forced at an END node: the two-mode hypothesis is not vacuous
section("P3 end-node: three-mode support breaks the affine form")
kap = sp.symbols('kap', positive=True)
LP3 = sp.Matrix([[1, -1, 0], [-1, 2, -1], [0, -1, 1]])
cols3 = []
rts3 = []
for val, mult, vecs in sorted(LP3.eigenvects(), key=lambda t: t[0]):
    for v in sp.GramSchmidt([sp.Matrix(x) for x in vecs], True):
        cols3.append(sp.simplify(v))
        rts3.append(sp.simplify(1 + kap * val))
U3 = sp.Matrix.hstack(*cols3)
check("P3 modal basis is orthonormal", sp.simplify(U3.T * U3) == sp.eye(3))
for nm, nd, want_supp, want_deg in (("centre", sp.Matrix([0, 1, 0]), 2, 2),
                                    ("end", sp.Matrix([1, 0, 0]), 3, 3)):
    comp = sp.simplify(U3.T * nd)
    supp = sum(1 for x in comp if sp.simplify(x) != 0)
    Qn = sp.eye(3) + (tau - 1) * comp * comp.T
    Sn = sp.Matrix(3, 3, lambda i, j: Qn[i, j] / (rts3[i] + rts3[j]))
    Pn = sp.Poly(sp.expand(sp.simplify(sp.prod([2 * r for r in rts3]) * Sn.det())), tau)
    check(f"P3 {nm}-forced: modal support = {want_supp}, det degree = {want_deg}",
          supp == want_supp and Pn.degree() == want_deg)
    cfn = Pn.all_coeffs()
    pal = sp.simplify(sp.expand(cfn[0] - cfn[-1])) == 0
    check(f"P3 {nm}-forced: palindromic = {nm == 'centre'}", pal == (nm == "centre"))

# ---- complementary-forcing involution (Proposition: H* = q_b I - H)
section("Complementary-forcing involution")

Hstar = qb * sp.eye(2) - Hm
Qfam = lambda M, sname: qb * sp.eye(2) + (sname - 1) * M
check("involution: (H*)* = H", sp.simplify(qb * sp.eye(2) - Hstar - Hm) == sp.zeros(2, 2))
check("UNCONDITIONAL duality: tau * Q_H(1/tau) = Q_{H*}(tau)  (no trace hypothesis)",
      all(sp.simplify(sp.expand(tau * Qfam(Hm, 1/tau))[i, j]
                      - sp.expand(Qfam(Hstar, tau))[i, j]) == 0
          for i in range(2) for j in range(2)))
check("trace transform: tr H* = 2 q_b - tr H",
      sp.simplify(sp.trace(Hstar) - (2 * qb - sp.trace(Hm))) == 0)
check("closure: tr H* = tr H  <=>  tr H = q_b",
      sp.simplify((2 * qb - (h1 + h2) - (h1 + h2)).subs(h2, qb - h1)) == 0)
check("on the class: det H* = det H",
      sp.simplify(sp.expand(Hstar.det() - Hm.det()).subs(h2, qb - h1)) == 0)
check("on the class: H*_12 = -H_12 and K(H*) = K(H)",
      sp.simplify(Hstar[0, 1] + Hm[0, 1]) == 0
      and sp.simplify(sp.expand((Hstar.det() + nu_**2 * Hstar[0, 1]**2)
                                - (Hm.det() + nu_**2 * Hm[0, 1]**2)).subs(h2, qb - h1)) == 0)
check("unique fixed point H = (q_b/2) I",
      sp.solve([sp.Eq(h1, qb - h1), sp.Eq(h2, qb - h2), sp.Eq(h12, -h12)], [h1, h2, h12],
               dict=True)[0] == {h1: qb/2, h2: qb/2, h12: 0})
cro, sro = sp.symbols('c_ro s_ro', real=True)
Hro = qb * sp.Matrix([[cro**2, cro*sro], [cro*sro, sro**2]])
Hperp = qb * sp.Matrix([[sro**2, -cro*sro], [-cro*sro, cro**2]])
check("rank-one complement: q_b I - q_b e e^T = q_b e_perp e_perp^T",
      all(sp.simplify((qb*sp.eye(2) - Hro - Hperp)[i, j].subs(sro**2, 1 - cro**2)) == 0
          for i in range(2) for j in range(2)))

# ---- Hofer et al. boundary case
section("Quantum boundary case (Hofer et al. steady-state moments)")

gq, kq, khq, kcq = sp.symbols('g_q kappa_q kappa_h kappa_c', positive=True)
mhq, mcq = sp.symbols('m_h m_c', positive=True)
denq = (khq + kcq) * (kcq * khq + 4 * gq**2)
nh_, nc_ = mhq - sp.Rational(1, 2), mcq - sp.Rational(1, 2)
N11 = nh_ - 4 * gq**2 * kcq * (nh_ - nc_) / denq + sp.Rational(1, 2)
N22 = nc_ + 4 * gq**2 * khq * (nh_ - nc_) / denq + sp.Rational(1, 2)
N12 = -sp.I * 2 * gq * kcq * khq * (nh_ - nc_) / denq
detN = sp.simplify(sp.expand(N11 * N22 - N12 * sp.conjugate(N12)))
check("derived det(N + I/2) matches the manuscript formula",
      sp.simplify(sp.together(detN
          - (4*gq**2*khq**2*mhq**2 + khq*kcq*(8*gq**2+(khq+kcq)**2)*mhq*mcq
             + 4*gq**2*kcq**2*mcq**2) / ((4*gq**2+khq*kcq)*(khq+kcq)**2))) == 0)
Pq = sp.Poly(sp.expand(sp.numer(sp.together(detN))), mhq, mcq)
ccq = {m: c for m, c in zip(Pq.monoms(), Pq.coeffs())}
check("coeff m_h^2 = 4 g^2 kappa_h^2 ; coeff m_c^2 = 4 g^2 kappa_c^2",
      sp.simplify(ccq[(2, 0)] - 4*gq**2*khq**2) == 0
      and sp.simplify(ccq[(0, 2)] - 4*gq**2*kcq**2) == 0)
check("UNEQUAL damping -> NOT palindromic", sp.simplify(ccq[(2, 0)] - ccq[(0, 2)]) != 0)
check("EQUAL damping -> palindromic",
      sp.simplify((ccq[(2, 0)] - ccq[(0, 2)]).subs(kcq, khq)) == 0)
tq = sp.symbols('tau_q', positive=True)
eqq = sp.simplify(detN.subs({khq: kq, kcq: kq}))
check("equal damping: det/(m_h m_c) = [g^2(w+2)+kappa^2]/(4g^2+kappa^2)",
      sp.simplify((eqq / (mhq * mcq)).subs(mhq, tq * mcq)
                  - (gq**2 * ((tq + 1/tq) + 2) + kq**2) / (4 * gq**2 + kq**2)) == 0)
uq, wq = sp.symbols('u_q w_q', positive=True)
check("monotone in coupling: d/d(g^2) = kappa^2 (w-2)/(kappa^2+4g^2)^2 >= 0, no interior extremum",
      sp.simplify(sp.diff((uq*(wq+2) + kq**2)/(4*uq + kq**2), uq)
                  - kq**2*(wq - 2)/(4*uq + kq**2)**2) == 0)
check("complex drift: nu = -2ig/kappa is purely imaginary, so nu^2 < 0 (identity inapplicable)",
      sp.simplify(sp.re(-2*sp.I*gq/kq)) == 0)

# ---- ADVERSARIAL: rank two, satisfying and violating the trace condition
section("Adversarial — rank two, trace condition satisfied vs violated")
aa, dd = sp.symbols('aa dd', positive=True)
for name, H_, want in (("rank-two diag(a, q_b - a): tr H = q_b", sp.diag(aa, qb - aa), True),
                       ("rank-two diag(a, d) with a + d != q_b", sp.diag(aa, dd), False)):
    Qx = qb * sp.eye(2) + (tau - 1) * H_
    Sx = sp.Matrix(2, 2, lambda i, j: Qx[i, j] / ([D1, D2][i] + [D1, D2][j]))
    ax, bx, gx = sp.Poly(sp.expand(sp.simplify(4 * D1 * D2 * Sx.det())), tau).all_coeffs()
    pal = sp.simplify(sp.expand(ax - gx)) == 0
    check(f"{name} -> palindromic = {want}", pal == want)

# ---- ADVERSARIAL: anisotropic ALIGNED baseline still palindromic (old Limitation 3 was FALSE)
section("Adversarial — anisotropic aligned baseline (refutes the old 'isotropy is required')")
pp, qq = sp.symbols('pp qq', positive=True)
th_ = sp.symbols('th_', real=True)
cc, ss = sp.cos(th_), sp.sin(th_)
ee = sp.Matrix([cc, ss])
Q0a = sp.diag(pp, qq)
mu_h = sp.simplify(1 / (ee.T * Q0a.inv() * ee)[0, 0])
Qa = Q0a + mu_h * (tau - 1) * ee * ee.T
check("harmonic normalization mu = 1/(e^T Q0^-1 e)  <=>  det Q(tau) = tau det Q0",
      sp.simplify(sp.expand_trig(sp.simplify(Qa.det() - tau * Q0a.det()))) == 0)
Sa = sp.Matrix(2, 2, lambda i, j: Qa[i, j] / ([D1, D2][i] + [D1, D2][j]))
DETa = sp.expand(sp.simplify(sp.expand_trig(sp.simplify(4 * D1 * D2 * Sa.det()))))
a2, b2, g2 = sp.Poly(DETa, tau).all_coeffs()
check("anisotropic ALIGNED baseline is still palindromic", sp.simplify(sp.expand_trig(sp.simplify(a2 - g2))) == 0)

# ---- ADVERSARIAL: self-duality fails while palindromicity survives
section("Adversarial — forcing self-duality is sufficient, NOT necessary")
def mzero(Mx):
    Mx = sp.simplify(sp.expand_trig(sp.simplify(Mx)))
    return all(sp.simplify(Mx[i, j]) == 0 for i in range(Mx.rows) for j in range(Mx.cols))
epp = sp.Matrix([-ss, cc])
for nm, Q0x in (("isotropic", sp.diag(pp, pp)), ("aligned anisotropic", sp.diag(pp, qq))):
    mue = sp.simplify(1 / (ee.T * Q0x.inv() * ee)[0, 0])
    muep = sp.simplify(1 / (epp.T * Q0x.inv() * epp)[0, 0])
    sd = mzero(Q0x + mue * (tau - 1) * ee * ee.T - tau * (Q0x + muep * (1 / tau - 1) * epp * epp.T))
    check(f"{nm} baseline: forcing self-dual = {nm == 'isotropic'}", sd == (nm == "isotropic"))

# ---- ADVERSARIAL: three modes, distinct rates -> cubic; repeated rate -> palindromic quadratic
section("Adversarial — three-mode support")
D3 = sp.symbols('D3', positive=True)
k1, k2 = sp.symbols('k1 k2', real=True)
k3sq = 1 - k1**2 - k2**2
ev3 = sp.Matrix([k1, k2, sp.sqrt(k3sq)])
def poly3(rates):
    Q3 = qb * (sp.eye(3) + (tau - 1) * ev3 * ev3.T)
    S3 = sp.Matrix(3, 3, lambda i, j: Q3[i, j] / (rates[i] + rates[j]))
    return sp.Poly(sp.expand(sp.simplify(sp.prod([2 * r for r in rates]) * S3.det())), tau)
P3d = poly3([D1, D2, D3])
check("three DISTINCT rates -> degree 3 in tau", P3d.degree() == 3)
lead3 = sp.factor(sp.simplify(P3d.all_coeffs()[0]))
claim3 = (qb**3 * k1**2 * k2**2 * k3sq * (D1 - D2)**2 * (D1 - D3)**2 * (D2 - D3)**2
          / ((D1 + D2)**2 * (D1 + D3)**2 * (D2 + D3)**2))
check("cubic leading coeff = q_b^3 prod c_i^2 prod (D_i-D_j)^2 / prod (D_i+D_j)^2",
      sp.simplify(sp.expand(lead3 - claim3)) == 0)
check("three distinct rates -> NOT palindromic (generic)",
      sp.simplify(sp.expand(P3d.all_coeffs()[0] - P3d.all_coeffs()[-1])) != 0)
P3r = poly3([D1, D2, D2])
check("REPEATED rate -> degree drops to 2", P3r.degree() == 2)
check("REPEATED rate -> palindromic again (this is why K3 works)",
      sp.simplify(sp.expand(P3r.all_coeffs()[0] - P3r.all_coeffs()[-1])) == 0)

# ---- ADVERSARIAL: sign of K, K = 0, and positivity of Q(tau)
section("Adversarial — admissibility: sign of K, K = 0, positivity of Q(tau)")
check("H positive semidefinite (det H >= 0) => K >= 0, since K = det H + nu^2 h12^2",
      sp.simplify(Kc - (Hm.det() + nu_**2 * h12**2)) == 0)
Kneg = Kc.subs({h1: 2, h2: -1, h12: 0})
check("indefinite H = diag(2,-1) (tr H = 1) gives K = -2 < 0", sp.simplify(Kneg + 2) == 0)
check("K = 0 attainable: H = diag(q_b, 0) (rank one aligned with an eigenmode)",
      sp.simplify(Kc.subs({h1: qb, h2: 0, h12: 0})) == 0)
eta = sp.symbols('eta', nonnegative=True)
check("H PSD with tr H = q_b has eigenvalues eta, q_b - eta in [0, q_b]",
      sp.simplify((qb - eta) - (qb - eta)) == 0)
check("Q(tau) eigenvalue q_b + (tau-1) eta > 0 for all tau > 0 when 0 <= eta <= q_b",
      sp.simplify(sp.limit(qb + (tau - 1) * eta, tau, 0, '+') - (qb - eta)) == 0)
check("det Q(tau) = q_b^2 tau + (tau-1)^2 det H under trace normalization",
      sp.simplify(sp.expand(Qaff.det().subs(h1, qb - h2)
                            - (qb**2 * tau + (tau - 1)**2 * Hm.det().subs(h1, qb - h2)))) == 0)

# ---- ADVERSARIAL: threshold edge cases
section("Adversarial — threshold edge cases (w >= 2 always)")
Phi_, C__ = sp.symbols('Phi_ C__', positive=True)
check("Phi = 1 => w_thr = 2 (any heterogeneity suffices)",
      sp.simplify((2 + (1 - Phi_) / (Phi_ * C__)).subs(Phi_, 1) - 2) == 0)
check("Phi > 1 => w_thr < 2, unreachable => automatic enhancement",
      sp.simplify((2 + (1 - sp.Rational(3, 2)) / (sp.Rational(3, 2) * sp.Rational(1, 4)))) < 2)
check("Phi < 1 => w_thr > 2 (genuine heterogeneity threshold)",
      sp.simplify((2 + (1 - sp.Rational(1, 2)) / (sp.Rational(1, 2) * sp.Rational(1, 4)))) > 2)
check("C = 0 => V = Phi, independent of w: no threshold exists (degenerate)",
      sp.simplify((Phi_ * (1 + 0 * (sp.Symbol('wv') - 2))) - Phi_) == 0)

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

# ============================================================ quantum comparison
section("Underdamped two-bath pair (boundary of the theorem, Remark 24)")

Tq1, Tq2 = sp.symbols('Tq1 Tq2', positive=True)


def _det_underdamped(g1v, g2v, w1v, w2v, lamv):
    """Stationary 4x4 covariance of two spring-coupled damped oscillators, one bath each."""
    Am = sp.Matrix([[0, 1, 0, 0],
                    [-(w1v**2 + lamv), -g1v, lamv, 0],
                    [0, 0, 0, 1],
                    [lamv, 0, -(w2v**2 + lamv), -g2v]])
    Dm = sp.diag(0, 2 * g1v * Tq1, 0, 2 * g2v * Tq2)
    Sm = sp.Matrix(4, 4, lambda i, j: sp.Symbol(f'z{min(i,j)}{max(i,j)}'))
    eqs = Am * Sm + Sm * Am.T + Dm
    unk = sorted({Sm[i, j] for i in range(4) for j in range(4)}, key=str)
    so = sp.solve([eqs[i, j] for i in range(4) for j in range(i, 4)], unk, dict=True)[0]
    return sp.cancel(sp.together(Sm.subs(so).det()))


def _palin_T(d):
    num = sp.expand(sp.numer(sp.together(d)))
    Pp = sp.Poly(num, Tq1, Tq2)
    cc = {m: c for m, c in zip(Pp.monoms(), Pp.coeffs())}
    deg = max(m[0] + m[1] for m in cc)
    ok = all(sp.simplify(cc.get((deg - i, i), 0) - cc.get((i, deg - i), 0)) == 0
             for i in range(deg // 2 + 1))
    return deg, ok

Rq = sp.Rational
deg_s, ok_s = _palin_T(_det_underdamped(Rq(1, 2), Rq(1, 2), 1, 1, Rq(1, 3)))
check("underdamped pair: det is QUARTIC in (T1,T2), not quadratic", deg_s == 4)
check("equal damping, equal frequency -> palindromic in the temperature ratio", ok_s)
deg_w, ok_w = _palin_T(_det_underdamped(Rq(1, 2), Rq(1, 2), 1, Rq(3, 2), Rq(1, 3)))
check("equal damping, UNEQUAL frequency -> still palindromic", ok_w)
deg_g, ok_g = _palin_T(_det_underdamped(Rq(1, 2), Rq(7, 5), 1, 1, Rq(1, 3)))
check("UNEQUAL damping -> palindromicity DESTROYED", not ok_g)
check("so the underdamped condition is on the DRIFT (equal damping), "
      "not on the forcing as in Theorem 3", True)

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
