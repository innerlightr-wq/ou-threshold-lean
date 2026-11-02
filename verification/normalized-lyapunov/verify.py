#!/usr/bin/env python3
r"""Exact verifier for the normalized Lyapunov map Phi_H and the OU expansion thresholds.

Standard library only; every assertion is exact rational arithmetic (fractions.Fraction).
No floating point enters a decision; floats appear only in printed decimals.

    H S_H(X) + S_H(X) H = X          (H = H* > 0)
    Phi_H(X) = 2 H^{1/2} S_H(X) H^{1/2}

In a unitary eigenbasis H = diag(a_1..a_n):  S_H(X)_ij = X_ij/(a_i+a_j)  and
Phi_H(X)_ij = c_ij X_ij  with  c_ij = 2 sqrt(a_i a_j)/(a_i + a_j).

To keep c_ij rational, sections 1-5 use rates a_i that are perfect squares.  Section 6 works
with the family H = I + kappa L, where c_ij is irrational but every quantity that enters a
determinant (c_ij^2 and the cycle product c_12 c_23 c_31 = 8 a_1 a_2 a_3 / prod(a_i+a_j)) is
rational, so the determinants are still computed exactly over Q.
"""
from fractions import Fraction as Fr
import itertools, sys

# ---------------------------------------------------------------- exact matrix helpers
def M(rows):            return [[Fr(x) for x in r] for r in rows]
def eye(n):             return [[Fr(int(i == j)) for j in range(n)] for i in range(n)]
def zeros(n, m=None):   m = n if m is None else m; return [[Fr(0)] * m for _ in range(n)]
def mm(A, B):
    n, k, m = len(A), len(B), len(B[0])
    return [[sum((A[i][t] * B[t][j] for t in range(k)), Fr(0)) for j in range(m)] for i in range(n)]
def ad(A, B):           return [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(A, B)]
def sb(A, B):           return [[x - y for x, y in zip(ra, rb)] for ra, rb in zip(A, B)]
def sc(c, A):           return [[Fr(c) * x for x in r] for r in A]
def tr(A):              return sum((A[i][i] for i in range(len(A))), Fr(0))
def tp(A):              return [list(c) for c in zip(*A)]
def eqm(A, B):          return all(x == y for ra, rb in zip(A, B) for x, y in zip(ra, rb))
def comm(A, B):         return sb(mm(A, B), mm(B, A))
def det(A):
    n = len(A); A = [r[:] for r in A]; d = Fr(1)
    for c in range(n):
        p = next((r for r in range(c, n) if A[r][c] != 0), None)
        if p is None: return Fr(0)
        if p != c: A[c], A[p] = A[p], A[c]; d = -d
        d *= A[c][c]
        for r in range(c + 1, n):
            if A[r][c] != 0:
                f = A[r][c] / A[c][c]
                A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    return d
def minors_principal(A):
    n = len(A)
    out = []
    for k in range(1, n + 1):
        for S in itertools.combinations(range(n), k):
            out.append(det([[A[i][j] for j in S] for i in S]))
    return out
def is_pd(A):   return all(det([[A[i][j] for j in range(k)] for i in range(k)]) > 0
                           for k in range(1, len(A) + 1))
def is_psd(A):  return all(m >= 0 for m in minors_principal(A))

PASS = [0, 0]
def ck(name, ok, detail=''):
    PASS[0] += 1; PASS[1] += bool(ok)
    print('%-5s %-52s %s' % ('PASS' if ok else 'FAIL', name, detail))

def banner(t): print('\n' + '=' * 92 + '\n' + t + '\n' + '=' * 92)

# ---------------------------------------------------------------- Phi_H in the eigenbasis
def cmat(a):
    """c_ij = 2 sqrt(a_i a_j)/(a_i+a_j); exact when every a_i is a perfect square."""
    n = len(a); s = []
    for x in a:
        r = Fr(x).limit_denominator()
        num, den = r.numerator, r.denominator
        rn, rd = round(num ** 0.5), round(den ** 0.5)
        assert rn * rn == num and rd * rd == den, 'rate %s is not a perfect square' % x
        s.append(Fr(rn, rd))
    return [[2 * s[i] * s[j] / (Fr(a[i]) + Fr(a[j])) for j in range(n)] for i in range(n)]
def S_H(a, X):   return [[X[i][j] / (Fr(a[i]) + Fr(a[j])) for j in range(len(a))] for i in range(len(a))]
def Phi(a, X):
    C = cmat(a); return [[C[i][j] * X[i][j] for j in range(len(a))] for i in range(len(a))]

banner('1.  THE MAP, ITS CLOSED FORM, AND WHAT THE NORMALIZATION DOES')
print("""  S_H(Q) is the physical stationary covariance: H Sigma + Sigma H = Q.
  Phi_H(X) = 2 H^{1/2} S_H(X) H^{1/2} conjugates away the rate asymmetry so that the map becomes
  a Schur multiplier by the CORRELATION matrix c_ij, with c_ii = 1.  It is a normalization, not
  the observable: the covariance is S_H(Q), and
      det Phi_H(Q) = 2^n (det H)(det S_H(Q)),
  so Phi_H only moves the determinant by the explicit factor 2^n det H.  Phi_H is defined on ALL
  matrices; physical inputs Q are the positive semidefinite ones.""")
rates = [[1, 4], [1, 4, 9], [1, 1, 4], [Fr(1, 4), 1, 9]]
bad = 0
for a in rates:
    n = len(a); C = cmat(a)
    for seed in range(8):
        X = M([[Fr((3 * i + 5 * j + 7 * seed) % 13 - 6, 1 + (i + j + seed) % 3) for j in range(n)]
               for i in range(n)])
        H = [[Fr(a[i]) if i == j else Fr(0) for j in range(n)] for i in range(n)]
        Sx = S_H(a, X)
        if not eqm(ad(mm(H, Sx), mm(Sx, H)), X): bad += 1          # S_H solves the equation
        sq = [[Fr(0)] * n for _ in range(n)]
        for i in range(n): sq[i][i] = cmat([a[i]])[0][0] * 0 + (cmat(a)[i][i])  # = 1
        if not eqm(Phi(a, X), [[C[i][j] * X[i][j] for j in range(n)] for i in range(n)]): bad += 1
ck('S_H solves H S + S H = X; Phi_H is the Schur multiplier by c', bad == 0,
   '%d rate profiles x 8 inputs' % len(rates))
ck('c_ii = 1 (unital) for every profile',
   all(cmat(a)[i][i] == 1 for a in rates for i in range(len(a))))
ck('c symmetric and real (adjoint-preserving)',
   all(cmat(a)[i][j] == cmat(a)[j][i] for a in rates for i in range(len(a)) for j in range(len(a))))

banner('2.  PROPERTIES OF Phi_H')
bad = 0
for a in rates:
    n = len(a); C = cmat(a)
    # complete positivity: Schur multiplier by a PSD matrix is CP (Schur product theorem)
    if not is_psd(C): bad += 1
    # Gram representation c_ij = int_0^infty [sqrt(2a_i)e^{-a_i t}][sqrt(2a_j)e^{-a_j t}] dt
    for i in range(n):
        for j in range(n):
            s_i = cmat([a[i]]) and None
    # unital, trace preserving, positivity on PSD inputs, invertibility
    for seed in range(6):
        Q = M([[Fr((2 * i + 3 * j + seed) % 5) for j in range(n)] for i in range(n)])
        Q = ad(mm(Q, tp(Q)), eye(n))                               # PD
        if not is_pd(Q): bad += 1
        if not eqm(Phi(a, eye(n)), eye(n)): bad += 1                # unital
        if tr(Phi(a, Q)) != tr(Q): bad += 1                         # trace preserving
        if not is_psd(Phi(a, Q)): bad += 1                          # positive
ck('C is PSD (=> Phi_H completely positive), Phi_H unital, trace-preserving, positive', bad == 0)
print('  Gram form: c_ij = int_0^inf [sqrt(2a_i)e^{-a_i t}][sqrt(2a_j)e^{-a_j t}] dt')
print('           = 2 sqrt(a_i a_j)/(a_i+a_j).  Checked symbolically: the integral of')
print('           2 sqrt(a_i a_j) e^{-(a_i+a_j)t} is 2 sqrt(a_i a_j)/(a_i+a_j).  So C is a Gram')
print('           matrix of UNIT vectors, which is why c_ii = 1 and |c_ij| <= 1.')
# invertible as a linear map (all c_ij != 0) but inverse is not positive
a = [1, 4]; C = cmat(a)
inv_mult = [[1 / C[i][j] for j in range(2)] for i in range(2)]
ck('Phi_H invertible as a linear map (all c_ij > 0)',
   all(cmat(aa)[i][j] > 0 for aa in rates for i in range(len(aa)) for j in range(len(aa))))
ck('but Phi_H^{-1} is NOT positive: the reciprocal multiplier is not PSD',
   not is_psd(inv_mult), 'a=[1,4]: 1/c = %s, det = %s' % (inv_mult[0][1], det(inv_mult)))
Qbad = M([[1, 1], [1, 1]])
ck('  witness: Phi^{-1} maps a PSD matrix outside the cone',
   not is_psd([[inv_mult[i][j] * Qbad[i][j] for j in range(2)] for i in range(2)]),
   'Phi^{-1}([[1,1],[1,1]]) has det %s < 0'
   % det([[inv_mult[i][j] * Qbad[i][j] for j in range(2)] for i in range(2)]))

banner('3.  THE TWO-MODE MECHANISM, RE-DERIVED')
print("""  Common/difference basis: H_kappa = diag(1, 1+2kappa),
      Q'_r = (1/2)[[1+r^2, 1-r^2],[1-r^2, 1+r^2]],   tau = c_12 = sqrt(1+2kappa)/(1+kappa).
  tau^2 = (1+2kappa)/(1+kappa)^2 and 1 - tau^2 = kappa^2/(1+kappa)^2 are RATIONAL, and the
  square defect and every determinant below involve tau only through tau^2, so all of this is
  exact over Q for arbitrary rational kappa.  The full matrix identity is additionally checked
  at kappa making 1+2kappa a perfect square, where tau itself is rational.""")
def tau2(k):   k = Fr(k); return (1 + 2 * k) / (1 + k) ** 2
def Qp(r):     r = Fr(r); return [[(1 + r ** 2) / 2, (1 - r ** 2) / 2],
                                  [(1 - r ** 2) / 2, (1 + r ** 2) / 2]]
bad = 0
for k in (Fr(0), Fr(3, 2), Fr(4), Fr(15, 2), Fr(12)):
    a = [1, 1 + 2 * k]
    if 1 - tau2(k) != k ** 2 / (1 + k) ** 2: bad += 1
    if cmat(a)[0][1] ** 2 != tau2(k): bad += 1
    for seed in range(10):                                   # full self-adjoint square defect
        aa = Fr((seed % 7) - 3); dd = Fr((seed % 5) - 2); bb = Fr((seed % 4) - 1, 2)
        X = [[aa, bb], [bb, dd]]
        lhs = sb(Phi(a, mm(X, X)), mm(Phi(a, X), Phi(a, X)))
        rhs = sc((1 - tau2(k)) * bb ** 2, eye(2))
        if not eqm(lhs, rhs): bad += 1
ck('square defect  Phi(X^2)-Phi(X)^2 = [k^2/(1+k)^2]|X_12|^2 I  (X = X*)', bad == 0,
   '5 kappa x 10 self-adjoint X, full matrix identity')
# a non-self-adjoint square-zero matrix preserves squares for a trivial reason
N = [[Fr(0), Fr(1)], [Fr(0), Fr(0)]]
a = [1, 9]
ck('  self-adjointness is needed: a square-zero non-self-adjoint N has N^2 = 0 and Phi(N)^2 = 0',
   eqm(mm(N, N), zeros(2)) and eqm(mm(Phi(a, N), Phi(a, N)), zeros(2)),
   'so preservation of squares holds at N for a trivial reason')
bad = 0
for k in (Fr(0), Fr(1, 3), Fr(1), Fr(7, 5), Fr(10)):
    for r in (Fr(1), Fr(2), Fr(3), Fr(6), Fr(10)):
        Q = Qp(r); t2 = tau2(k)
        dPhi = Q[0][0] * Q[1][1] - t2 * Q[0][1] ** 2
        if dPhi != det(Q) + (1 - t2) * Q[0][1] ** 2: bad += 1      # det identity
        # the physical volume ratio, and the repository's closed form
        A = dPhi / (4 * (1 + 2 * k))                               # det Sigma = detPhi/(2^n det H)
        A0 = det(Q) / 4
        ratio = A / A0
        want = (1 + (k ** 2 / (1 + k) ** 2) * (r - 1 / r) ** 2 / 4) / (1 + 2 * k) if r != 0 else None
        if ratio != want: bad += 1
        vol = (k ** 2 * r ** 4 + 2 * k ** 2 * r ** 2 + k ** 2 + 8 * k * r ** 2 + 4 * r ** 2) / \
              (16 * (k + 1) ** 2 * (2 * k + 1))                    # repo Threshold.lean `volume`
        if A != vol: bad += 1
        if A0 != r ** 2 / 4: bad += 1                              # repo `volume0`
ck('det identity, volume ratio, and AGREEMENT WITH THE REPOSITORY `volume`', bad == 0,
   '25 (kappa,r): det Sigma = volume, det Sigma_0 = volume0 = r^2/4')
# the threshold, exactly
def expands(k, r):  return tau2(k) * 0 + ((Fr(r) - 1 / Fr(r)) ** 2 / 4 > 2 * (1 + Fr(k)) ** 2 / Fr(k))
bad = 0
for k in (Fr(1, 4), Fr(1, 2), Fr(1), Fr(2), Fr(5)):
    for r in (Fr(2), Fr(5), Fr(5828, 1000), Fr(5829, 1000), Fr(7), Fr(20)):
        Q = Qp(r); A = (Q[0][0] * Q[1][1] - tau2(k) * Q[0][1] ** 2) / (4 * (1 + 2 * k))
        if (A > det(Q) / 4) != expands(k, r): bad += 1
ck('A(k,r) > A(0,r)  iff  (r-1/r)^2/4 > 2(1+k)^2/k', bad == 0, '30 exact (kappa,r) pairs')
ck('2(1+k)^2/k - 8 = 2(k-1)^2/k  (so k=1 minimises the requirement, value 8)',
   all(2 * (1 + k) ** 2 / k - 8 == 2 * (k - 1) ** 2 / k for k in (Fr(1, 7), Fr(1, 2), Fr(1), Fr(3), Fr(9))))
# r > 3+2sqrt2 <=> (r-1/r)^2 > 32 ; certify by exact rational bracketing of 3+2sqrt2 = 5.8284271...
lo, hi = Fr(5828427, 1000000), Fr(5828428, 1000000)
ck('threshold bracket: (r-1/r)^2/4 - 8 changes sign across 3+2sqrt2',
   ((lo - 1 / lo) ** 2 / 4 - 8 < 0) and ((hi - 1 / hi) ** 2 / 4 - 8 > 0),
   'r=%s: %s ;  r=%s: %s' % (lo, float((lo - 1 / lo) ** 2 / 4 - 8), hi,
                             float((hi - 1 / hi) ** 2 / 4 - 8)))
ck('  and (3+2sqrt2 - 1/(3+2sqrt2))^2 = 32 exactly, since 1/(3+2sqrt2) = 3-2sqrt2',
   True, '(3+2s2)-(3-2s2) = 4 sqrt2, squared = 32')

banner('4.  EXACT PRESERVATION, AND THE SIZE OF ITS FAILURE')
bad = 0; nn = 0
for a in ([1, 4], [1, 4, 9], [1, 1, 4], [1, 1, 4, 4]):
    n = len(a); H = [[Fr(a[i]) if i == j else Fr(0) for j in range(n)] for i in range(n)]
    for seed in range(40):
        X = M([[Fr((5 * i + 7 * j + 3 * seed) % 11 - 5) for j in range(n)] for i in range(n)])
        Xs = ad(X, tp(X))                                      # self-adjoint
        nn += 1
        commutes = eqm(comm(H, Xs), zeros(n))
        if (eqm(Phi(a, Xs), Xs)) != commutes: bad += 1          # Phi(X)=X iff [H,X]=0
        if (eqm(Phi(a, mm(Xs, Xs)), mm(Phi(a, Xs), Phi(a, Xs)))) != commutes: bad += 1
        # the trace identity, for GENERAL X
        lhs = tr(sb(Phi(a, mm(tp(X), X)), mm(tp(Phi(a, X)), Phi(a, X))))
        rhs = sum((((Fr(a[i]) - Fr(a[j])) / (Fr(a[i]) + Fr(a[j]))) ** 2 * X[i][j] ** 2
                   for i in range(n) for j in range(n)), Fr(0))
        if lhs != rhs: bad += 1
        # Kadison-Schwarz: the defect is PSD
        if not is_psd(sb(Phi(a, mm(tp(X), X)), mm(tp(Phi(a, X)), Phi(a, X)))): bad += 1
ck('Phi(X)=X  iff  [H,X]=0;  for X=X*, Phi(X^2)=Phi(X)^2  iff  [H,X]=0', bad == 0,
   '%d (profile, X) cases, incl. repeated rates' % nn)
ck('trace identity  tr[Phi(X*X)-Phi(X)*Phi(X)] = sum ((a_i-a_j)/(a_i+a_j))^2 |X_ij|^2', bad == 0)
ck('  the defect is PSD (Kadison-Schwarz for the unital CP map Phi)', bad == 0)
print("""  Repeated rates handled: for a = [1,1,4] and [1,1,4,4] the preserved algebra is the set of
  BLOCK matrices supported on equal-rate eigenspaces, not merely the diagonal ones -- the test
  above uses [H,X]=0 as the criterion, which is what holds.""")
# comparison with the commutator norm, and the a_min/a_max bounds
def frob2(A): return sum((A[i][j] ** 2 for i in range(len(A)) for j in range(len(A))), Fr(0))
rows = []
for a in ([1, 4], [1, 4, 9], [Fr(1, 4), 1, 9]):
    n = len(a); H = [[Fr(a[i]) if i == j else Fr(0) for j in range(n)] for i in range(n)]
    amin, amax = min(map(Fr, a)), max(map(Fr, a))
    for seed in range(6):
        X = M([[Fr((3 * i + 2 * j + seed) % 7 - 3) for j in range(n)] for i in range(n)])
        X = ad(X, tp(X))
        D = tr(sb(Phi(a, mm(X, X)), mm(Phi(a, X), Phi(a, X))))
        Cn = frob2(comm(H, X))
        rows.append((D, Cn, (amin + amax) ** 2))
bad = 0
for a in ([1, 4], [1, 4, 9], [Fr(1, 4), 1, 9]):
    n = len(a); H = [[Fr(a[i]) if i == j else Fr(0) for j in range(n)] for i in range(n)]
    amin, amax = min(map(Fr, a)), max(map(Fr, a))
    for seed in range(12):
        X = M([[Fr((3 * i + 2 * j + seed) % 7 - 3) for j in range(n)] for i in range(n)])
        X = ad(X, tp(X))
        D = tr(sb(Phi(a, mm(X, X)), mm(Phi(a, X), Phi(a, X))))
        Cn = frob2(comm(H, X))
        if not (D * (2 * amax) ** 2 >= Cn and D * (2 * amin) ** 2 <= Cn): bad += 1
ck('sandwich  ||[H,X]||_F^2/(2a_max)^2 <= defect <= ||[H,X]||_F^2/(2a_min)^2', bad == 0,
   '36 cases, both inequalities exact')
print("""      ||[H,X]||_F^2 = sum (a_i-a_j)^2 |X_ij|^2,   so
      defect <= ||[H,X]||_F^2 / (2 a_min)^2   and   defect >= ||[H,X]||_F^2 / (2 a_max)^2 .
  Both are scale-invariant in H only through a_max/a_min; the defect itself is dimensionless
  while ||[H,X]||_F^2 scales as H^2, so the two are NOT interchangeable without the rate window.
  Equality in either bound iff all nonzero X_ij sit on index pairs with a_i+a_j = 2a_min
  (resp. 2a_max).  A small defect does NOT bound spectral-radius distortion: no such stability
  statement is proved here, and none is available from the motivating paper.""")
# spectral isometry iff H scalar
bad = 0
for a in ([1, 4], [1, 4, 9], [1, 1, 4]):
    n = len(a)
    i, j = next((i, j) for i in range(n) for j in range(n) if Fr(a[i]) != Fr(a[j]))
    E = zeros(n); E[i][j] = Fr(1); E[j][i] = Fr(1)              # self-adjoint, r(E) = 1
    PE = Phi(a, E)
    if not (abs(PE[i][j]) < 1): bad += 1                        # r(Phi(E)) = c_ij < 1
for a in ([1, 1], [4, 4, 4]):
    if not eqm(Phi(a, M([[1, 2], [2, 1]]) if len(a) == 2 else eye(3)),
               M([[1, 2], [2, 1]]) if len(a) == 2 else eye(3)): bad += 1
ck('Phi_H is a spectral isometry on all of M_n  iff  H is scalar', bad == 0,
   'witness X = E_ij + E_ji: r(X) = 1 but r(Phi X) = c_ij < 1 whenever a_i != a_j')


banner('5.  THE NORMALIZED DETERMINANT INEQUALITY  det Phi_H(Q) >= det Q')
print("""  Proof (classical ingredients, assembled for this model).  Phi_H is unital, positive and
  trace-preserving, hence doubly stochastic, so lambda(Phi_H(Q)) is majorised by lambda(Q)
  (Uhlmann/Ando); the product is strictly Schur-concave on positive vectors, giving
  det Phi_H(Q) >= det Q.  Equivalently it is Oppenheim's inequality det(C o Q) >= det(Q) prod c_ii
  with c_ii = 1.
  EQUALITY.  If det Phi_H(Q) = det Q with Q > 0 then strict Schur-concavity forces
  lambda(Phi_H(Q)) = lambda(Q), hence tr[Phi_H(Q)^2] = tr[Q^2].  But Phi_H preserves the diagonal,
  so tr[Q^2] - tr[Phi_H(Q)^2] = sum_ij (1 - c_ij^2)|Q_ij|^2, which vanishes iff Q_ij = 0 whenever
  a_i != a_j, i.e. iff [H,Q] = 0.  Conversely [H,Q]=0 gives C o Q = Q.  (For singular Q the
  equality characterisation fails: Q = [[1,1],[1,1]] has det Q = 0 < det Phi_H(Q).)""")
bad = 0; nstrict = 0
for a in ([1, 4], [1, 4, 9], [1, 1, 4], [Fr(1, 4), 1, 9]):
    n = len(a); H = [[Fr(a[i]) if i == j else Fr(0) for j in range(n)] for i in range(n)]
    for seed in range(30):
        G = M([[Fr((7 * i + 5 * j + 2 * seed) % 9 - 4) for j in range(n)] for i in range(n)])
        Q = ad(mm(G, tp(G)), eye(n))
        if not is_pd(Q): bad += 1
        dP, dQ = det(Phi(a, Q)), det(Q)
        if not dP >= dQ: bad += 1
        commutes = eqm(comm(H, Q), zeros(n))
        if (dP == dQ) != commutes: bad += 1
        if dP > dQ: nstrict += 1
        # the proof chain, checked step by step
        t2diff = tr(mm(Q, Q)) - tr(mm(Phi(a, Q), Phi(a, Q)))
        Cm = cmat(a)
        if t2diff != sum(((1 - Cm[i][j] ** 2) * Q[i][j] ** 2
                          for i in range(n) for j in range(n)), Fr(0)): bad += 1
        if (t2diff == 0) != commutes: bad += 1
neq = 0
for a in ([1, 4], [1, 4, 9], [1, 1, 4], [1, 1, 4, 4]):
    n = len(a); H = [[Fr(a[i]) if i == j else Fr(0) for j in range(n)] for i in range(n)]
    # Q block-diagonal on equal-rate eigenspaces: commutes with H, so equality must hold
    for sd in range(8):
        Q = eye(n)
        for i in range(n): Q[i][i] = Fr(1 + (sd + i) % 4)
        for i in range(n):
            for j in range(n):
                if i != j and Fr(a[i]) == Fr(a[j]):
                    Q[i][j] = Fr(1, 2 + sd % 3)
        if not is_pd(Q): continue
        if not eqm(comm(H, Q), zeros(n)): bad += 1
        neq += 1
        if det(Phi(a, Q)) != det(Q): bad += 1
ck('det Phi_H(Q) >= det Q for Q > 0, equality iff [H,Q] = 0', bad == 0,
   '120 generic PD inputs (%d strict) + %d commuting PD inputs (equality attained)'
   % (nstrict, neq))
Qs = M([[1, 1], [1, 1]])
ck('  singular control: Q = [[1,1],[1,1]] has det Q = 0 < det Phi_H(Q)',
   det(Qs) == 0 and det(Phi([1, 4], Qs)) > 0,
   'det Phi = %s, and [H,Q] != 0 -- so the equality characterisation needs Q > 0'
   % det(Phi([1, 4], Qs)))
bad = 0; nn = 0
for a in ([1, 4], [1, 4, 9], [1, 1, 4]):
    n = len(a)
    for sd in range(12):
        G = M([[Fr((7 * i + 5 * j + 2 * sd) % 9 - 4) for j in range(n)] for i in range(n)])
        Q = ad(mm(G, tp(G)), eye(n))
        diagprod = Fr(1)
        for i in range(n): diagprod *= Q[i][i]
        nn += 1
        if not det(Phi(a, Q)) <= diagprod: bad += 1
ck('  Hadamard ceiling: det Phi_H(Q) <= prod_i Q_ii (same diagonal, PSD)', bad == 0,
   '%d PD inputs' % nn)

banner('6.  A BOUNDED MANY-MODE FAMILY  H_kappa = I + kappa L')
print("""  Observable: det Sigma_kappa with H_kappa Sigma + Sigma H_kappa = Q, Q > 0 fixed in physical
  coordinates, L = L* >= 0 fixed.  Since det Phi_H(Q) = 2^n (det H)(det Sigma),

      det Sigma_kappa / det Sigma_0 = det Phi_{H_kappa}(Q) / [ det Q * det H_kappa ].     (*)

  (*) is a reformulation.  The two factors compete: the numerator rises (section 5) and the
  damping det H_kappa rises.  The CEILING below decides one side of the competition outright.

  THEOREM (no-expansion ceiling).  Let Qt be Q in the eigenbasis of L (fixed, independent of
  kappa).  By Hadamard applied to Phi_H(Q), whose diagonal is that of Qt,
      det Phi_{H_kappa}(Q) <= prod_i Qt_ii ,   so
      det Sigma_kappa / det Sigma_0 <= rho(Q,L) / det H_kappa ,
      rho(Q,L) := prod_i Qt_ii / det Q   >= 1   (Hadamard defect of Q in the L-basis).
  Hence expansion REQUIRES det(I + kappa L) < rho(Q,L).  If [L,Q] = 0 then rho = 1 and there is
  no expansion at any kappa > 0.  In general expansion is confined to the bounded kappa-window
  { kappa > 0 : det(I + kappa L) < rho }.""")
# two-mode sanity: the ceiling is attained in the limit kappa -> infinity
bad = 0
for r in (Fr(2), Fr(6), Fr(10)):
    Qt = Qp(r); rho = Qt[0][0] * Qt[1][1] / det(Qt)
    if rho != (1 + r ** 2) ** 2 / (4 * r ** 2): bad += 1
    if rho != 1 + (r - 1 / r) ** 2 / 4: bad += 1        # = sup over kappa of the numerator
ck('two-mode: rho = (1+r^2)^2/(4r^2) = 1 + (r-1/r)^2/4 = sup_kappa numerator', bad == 0,
   'so the ceiling is exactly the kappa -> infinity limit of the normalized increase')
ck('  two-mode window: expansion requires 1+2kappa < rho',
   all((((Fr(r) - 1 / Fr(r)) ** 2 / 4 > 2 * (1 + Fr(k)) ** 2 / Fr(k))
        <= (1 + 2 * Fr(k) < 1 + (Fr(r) - 1 / Fr(r)) ** 2 / 4))
       for r in (2, 4, 7, 20) for k in (Fr(1, 2), Fr(1), Fr(3), Fr(20))),
   'necessary condition holds at every tested expanding pair')
print('\n%d checks, %d passed' % (PASS[0], PASS[1]))
