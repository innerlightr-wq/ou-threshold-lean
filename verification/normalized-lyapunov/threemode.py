#!/usr/bin/env python3
r"""Exact three-mode analysis:  L = path Laplacian P3,  H_kappa = I + kappa L,  Q = diag(q1,q2,q3).

Eigen-decomposition of L = [[1,-1,0],[-1,2,-1],[0,-1,1]]:
    l = 0, 1, 3  with unnormalised eigenvectors u0=(1,1,1), u1=(1,0,-1), u2=(1,-2,1),
    |u0|^2 = 3, |u1|^2 = 2, |u2|^2 = 6.
So a_i = 1 + kappa*l_i = 1, 1+kappa, 1+3kappa and det H_kappa = (1+kappa)(1+3kappa).

In that orthonormal basis Qt_ij = u_i^T Q u_j/(|u_i||u_j|).  The only combinations entering a
3x3 determinant are the diagonal entries, the squared off-diagonals, and the cycle product -- and
each of those is RATIONAL even though the individual off-diagonals carry square roots:

    Qt00 = (q1+q2+q3)/3        Qt01^2 = (q1-q3)^2/6
    Qt11 = (q1+q3)/2           Qt02^2 = (q1-2q2+q3)^2/18
    Qt22 = (q1+4q2+q3)/6       Qt12^2 = (q1-q3)^2/12
    Qt01*Qt12*Qt02 = (q1-q3)^2 (q1-2q2+q3)/36

Likewise c_ij^2 = 4 a_i a_j/(a_i+a_j)^2 and the cycle product
c01*c12*c02 = 8 a0 a1 a2/[(a0+a1)(a1+a2)(a0+a2)] are rational.  Everything below is therefore
computed exactly over Q (as rational functions of kappa for fixed rational q's).
"""
from fractions import Fraction as Fr

# ------------------------------------------------- univariate polynomials / rational functions
def pnorm(p):
    while len(p) > 1 and p[-1] == 0: p = p[:-1]
    return p
def padd(p, q):
    n = max(len(p), len(q))
    return pnorm([ (p[i] if i < len(p) else Fr(0)) + (q[i] if i < len(q) else Fr(0))
                   for i in range(n) ])
def pneg(p):   return [-x for x in p]
def pmul(p, q):
    out = [Fr(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        if x:
            for j, y in enumerate(q): out[i + j] += x * y
    return pnorm(out)
def pev(p, t):  return sum((c * Fr(t) ** i for i, c in enumerate(p)), Fr(0))
class RF:
    __slots__ = ('n', 'd')
    def __init__(self, n, d=(Fr(1),)): self.n, self.d = pnorm(list(n)), pnorm(list(d))
    def __add__(s, o): return RF(padd(pmul(s.n, o.d), pmul(o.n, s.d)), pmul(s.d, o.d))
    def __sub__(s, o): return RF(padd(pmul(s.n, o.d), pneg(pmul(o.n, s.d))), pmul(s.d, o.d))
    def __mul__(s, o): return RF(pmul(s.n, o.n), pmul(s.d, o.d))
    def ev(s, t):      return pev(s.n, t) / pev(s.d, t)
def K(c):  return RF((Fr(c),))
KAP = RF((Fr(0), Fr(1)))

def analyse(q, name):
    q1, q2, q3 = map(Fr, q)
    detQ = q1 * q2 * q3
    Qt00 = (q1 + q2 + q3) / 3
    Qt11 = (q1 + q3) / 2
    Qt22 = (q1 + 4 * q2 + q3) / 6
    s01 = (q1 - q3) ** 2 / 6
    s02 = (q1 - 2 * q2 + q3) ** 2 / 18
    s12 = (q1 - q3) ** 2 / 12
    cyc = (q1 - q3) ** 2 * (q1 - 2 * q2 + q3) / 36
    a = [K(1), K(1) + KAP, K(1) + KAP * K(3)]
    # det Sigma, Sigma_ij = Qt_ij/(a_i+a_j)
    def R(x, den): return RF((Fr(1),), (Fr(1),)) * K(x) * RF((Fr(1),), den.n) if False else None
    def over(xnum, dpoly):  return RF((xnum,), dpoly)
    A01, A12, A02 = a[0] + a[1], a[1] + a[2], a[0] + a[2]
    T0, T1, T2 = a[0] + a[0], a[1] + a[1], a[2] + a[2]
    detS = (over(Qt00, T0.n) * over(Qt11, T1.n) * over(Qt22, T2.n)
            + K(2) * RF((cyc,), pmul(pmul(A01.n, A12.n), A02.n))
            - over(Qt00, T0.n) * RF((s12,), pmul(A12.n, A12.n))
            - over(Qt11, T1.n) * RF((s02,), pmul(A02.n, A02.n))
            - over(Qt22, T2.n) * RF((s01,), pmul(A01.n, A01.n)))
    detS0 = detQ / 8
    ratio = detS * K(1 / detS0)
    rho = Qt00 * Qt11 * Qt22 / detQ
    return dict(name=name, q=(q1, q2, q3), detQ=detQ, ratio=ratio, rho=rho,
                detH=lambda k: (1 + Fr(k)) * (1 + 3 * Fr(k)), Qt=(Qt00, Qt11, Qt22))

print('=' * 92)
print('THREE-MODE PATH LAPLACIAN:  exact behaviour of  det Sigma_kappa / det Sigma_0')
print('=' * 92)
for q, name in (((1, 1, 'r2'), 'Q = diag(1,1,r^2)   noise on an END node'),
                ((1, 'r2', 1), 'Q = diag(1,r^2,1)   noise on the CENTRE node')):
    print('\n' + name)
    print('%8s %16s %22s %16s %14s' % ('r', 'rho(Q,L)', 'max ratio over kappa grid',
                                       'argmax kappa', 'expands?'))
    for rv in (Fr(1), Fr(2), Fr(5), Fr(10), Fr(20), Fr(50), Fr(100)):
        qq = tuple((rv ** 2 if x == 'r2' else Fr(x)) for x in q)
        A = analyse(qq, name)
        best, bk = Fr(0), None
        kg = [Fr(i, 20) for i in range(1, 400)] + [Fr(i) for i in range(20, 400, 5)]
        for k in kg:
            v = A['ratio'].ev(k)
            if v > best: best, bk = v, k
        print('%8s %16.6f %22.12f %16s %14s'
              % (rv, float(A['rho']), float(best), bk, 'YES' if best > 1 else 'no'))
    # exact structural facts
    qq = tuple((Fr(7) ** 2 if x == 'r2' else Fr(x)) for x in q)
    A = analyse(qq, name)
    r0 = A['ratio']
    print('  ratio(0) = %s   (must be 1)' % r0.ev(0))
    h = Fr(1, 10 ** 6)
    print('  (ratio(h)-1)/h at h = 1e-6 : %.6f      -tr L = -4  (exact initial slope)'
          % float((r0.ev(h) - 1) / h))
    print('  ratio at kappa = 10^3, 10^4 : %.3e, %.3e   (-> 0 like 1/kappa^2)'
          % (float(r0.ev(1000)), float(r0.ev(10000))))
    print('  proved window: expansion needs det H_kappa = (1+k)(1+3k) < rho = %.6f'
          % float(A['rho']))
    kmax = None
    for i in range(1, 100000):
        k = Fr(i, 1000)
        if (1 + k) * (1 + 3 * k) >= A['rho']: kmax = k; break
    print('  so expansion is impossible for kappa >= %s  (exact rational cutoff)' % kmax)
