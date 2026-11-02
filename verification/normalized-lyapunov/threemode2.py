#!/usr/bin/env python3
"""Exact certification for the three-mode path-Laplacian model.

Independent route: solve H Sigma + Sigma H = Q directly as a 6-dimensional linear system in the
ORIGINAL basis over Q (Gaussian elimination on Fractions), with no eigen-decomposition at all.
This is the control on the eigenbasis determinant formula used in threemode.py.
"""
from fractions import Fraction as Fr
from itertools import permutations

L = [[1, -1, 0], [-1, 2, -1], [0, -1, 1]]
def Hk(k): return [[Fr(int(i == j)) + Fr(k) * Fr(L[i][j]) for j in range(3)] for i in range(3)]
def det3(M):
    return sum((1 if p in ((0,1,2),(1,2,0),(2,0,1)) else -1) * M[0][p[0]] * M[1][p[1]] * M[2][p[2]]
               for p in permutations(range(3)))
def solve(A, b):
    n, M = len(b), [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        piv = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[piv] = M[piv], M[c]
        pv = M[c][c]
        M[c] = [x / pv for x in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [M[i][n] for i in range(n)]
def lyap(H, Q):
    """Solve H S + S H = Q for symmetric S, exactly, in the original basis."""
    idx = [(0,0),(0,1),(0,2),(1,1),(1,2),(2,2)]
    pos = {}
    for t,(i,j) in enumerate(idx): pos[(i,j)] = t; pos[(j,i)] = t
    A, b = [], []
    for (i, j) in idx:
        row = [Fr(0)] * 6
        for k in range(3):
            row[pos[(k, j)]] += H[i][k]
            row[pos[(i, k)]] += H[k][j]
        A.append(row); b.append(Fr(Q[i][j]))
    v = solve(A, b)
    S = [[Fr(0)] * 3 for _ in range(3)]
    for t, (i, j) in enumerate(idx): S[i][j] = S[j][i] = v[t]
    return S

# -------- eigenbasis closed form (same algebra as threemode.py), as an exact rational of kappa
def detSigma_eigen(k, q):
    q1, q2, q3 = map(Fr, q); k = Fr(k)
    a = [Fr(1), 1 + k, 1 + 3 * k]
    Qt00 = (q1 + q2 + q3) / 3; Qt11 = (q1 + q3) / 2; Qt22 = (q1 + 4 * q2 + q3) / 6
    s01 = (q1 - q3) ** 2 / 6; s02 = (q1 - 2 * q2 + q3) ** 2 / 18; s12 = (q1 - q3) ** 2 / 12
    cyc = (q1 - q3) ** 2 * (q1 - 2 * q2 + q3) / 36
    return (Qt00 / (2 * a[0]) * Qt11 / (2 * a[1]) * Qt22 / (2 * a[2])
            + 2 * cyc / ((a[0] + a[1]) * (a[1] + a[2]) * (a[0] + a[2]))
            - Qt00 / (2 * a[0]) * s12 / (a[1] + a[2]) ** 2
            - Qt11 / (2 * a[1]) * s02 / (a[0] + a[2]) ** 2
            - Qt22 / (2 * a[2]) * s01 / (a[0] + a[1]) ** 2)

npass = nfail = 0
def chk(ok, label, note=''):
    global npass, nfail
    npass, nfail = npass + bool(ok), nfail + (not ok)
    print(('PASS  ' if ok else 'FAIL  ') + label + ('  ' + note if note else ''))

print('=' * 92)
print('SECTION 5  THREE-MODE EXTENSION (path Laplacian), exact')
print('=' * 92)

# C25: eigenbasis formula vs independent original-basis Lyapunov solve
bad = []
for k in (Fr(0), Fr(1,7), Fr(1), Fr(3), Fr(17,4), Fr(100)):
    for q in ((1,1,Fr(400)), (1,Fr(400),1), (Fr(9),Fr(4),Fr(1)), (Fr(1),Fr(1),Fr(1))):
        d1 = det3(lyap(Hk(k), [[q[0],0,0],[0,q[1],0],[0,0,q[2]]]))
        d2 = detSigma_eigen(k, q)
        if d1 != d2: bad.append((k, q, d1, d2))
chk(not bad, 'det Sigma: eigenbasis closed form == independent exact Lyapunov solve',
    '24 (kappa,Q) pairs, original basis, no eigen-decomposition' if not bad else str(bad[:1]))

def ratio(k, q): return detSigma_eigen(k, q) * 8 / (Fr(q[0]) * Fr(q[1]) * Fr(q[2]))

# C26: exact initial slope = -tr L, proved by clearing denominators over Q[kappa]
def pnorm(p):
    while len(p) > 1 and p[-1] == 0: p = p[:-1]
    return p
def padd(p, q):
    n = max(len(p), len(q))
    return pnorm([(p[i] if i < len(p) else Fr(0)) + (q[i] if i < len(q) else Fr(0)) for i in range(n)])
def pmul(p, q):
    out = [Fr(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        if x:
            for j, y in enumerate(q): out[i + j] += x * y
    return pnorm(out)
class RF:
    __slots__ = ('n', 'd')
    def __init__(s, n, d=(Fr(1),)): s.n, s.d = pnorm(list(n)), pnorm(list(d))
    def __add__(s, o): return RF(padd(pmul(s.n, o.d), pmul(o.n, s.d)), pmul(s.d, o.d))
    def __sub__(s, o): return RF(padd(pmul(s.n, o.d), [-x for x in pmul(o.n, s.d)]), pmul(s.d, o.d))
    def __mul__(s, o): return RF(pmul(s.n, o.n), pmul(s.d, o.d))
def K(c): return RF((Fr(c),))
KAP = RF((Fr(0), Fr(1)))

def ratio_rf(q):
    """ratio(kappa) = 8 det Sigma(kappa)/det Q as an exact element of Q(kappa)."""
    q1, q2, q3 = map(Fr, q)
    detQ = q1 * q2 * q3
    Qt00 = (q1 + q2 + q3) / 3; Qt11 = (q1 + q3) / 2; Qt22 = (q1 + 4 * q2 + q3) / 6
    s01 = (q1 - q3) ** 2 / 6; s02 = (q1 - 2 * q2 + q3) ** 2 / 18; s12 = (q1 - q3) ** 2 / 12
    cyc = (q1 - q3) ** 2 * (q1 - 2 * q2 + q3) / 36
    a = [K(1), K(1) + KAP, K(1) + KAP * K(3)]
    A01, A12, A02 = a[0] + a[1], a[1] + a[2], a[0] + a[2]
    T = [a[i] + a[i] for i in range(3)]
    detS = (RF((Qt00,), T[0].n) * RF((Qt11,), T[1].n) * RF((Qt22,), T[2].n)
            + K(2) * RF((cyc,), pmul(pmul(A01.n, A12.n), A02.n))
            - RF((Qt00,), T[0].n) * RF((s12,), pmul(A12.n, A12.n))
            - RF((Qt11,), T[1].n) * RF((s02,), pmul(A02.n, A02.n))
            - RF((Qt22,), T[2].n) * RF((s01,), pmul(A01.n, A01.n)))
    return detS * K(Fr(8) / detQ)

bad = []
for q in ((1,1,Fr(400)), (1,Fr(400),1), (Fr(9),Fr(4),Fr(1)), (Fr(1),Fr(1),Fr(1)), (Fr(2),Fr(3),Fr(5))):
    # g(kappa) := ratio(kappa)*det(I + kappa L) - 1,  det(I+kappa L) = (1+k)(1+3k)
    g = ratio_rf(q) * RF((Fr(1), Fr(4), Fr(3))) - K(1)
    num, den = g.n, g.d
    # g vanishes to second order at 0  <=>  num[0] == num[1] == 0  and  den[0] != 0
    # num may be IDENTICALLY zero: for Q = c*I one has Sigma = c H^{-1}/2 exactly, so
    # ratio = 1/det H and g vanishes as a rational function.  That is the strongest form of
    # the claim, not a failure of it.
    ok = den[0] != 0 and num[0] == 0 and (len(num) < 2 or num[1] == 0)
    if not ok: bad.append((q, num[:3], den[:1]))
chk(not bad, 'EXACT in Q[kappa]: ratio(kappa)*det(I+kappa L) - 1 has a DOUBLE root at kappa = 0',
    'so ratio(kappa) = 1 - (tr L) kappa + O(kappa^2), tr L = 4, for every tested Q > 0')

# the slope itself, read off exactly
q = (1, 1, Fr(400))
rr = ratio_rf(q)
slope = (rr.n[1] * rr.d[0] - rr.n[0] * rr.d[1]) / rr.d[0] ** 2
chk(slope == Fr(-4), 'exact slope d/dkappa [det Sigma_kappa/det Sigma_0] at kappa = 0 equals -tr L = -4',
    'computed symbolically as %s' % slope)

chk(all(ratio(Fr(0), q) == 1 for q in ((1,1,Fr(400)), (1,Fr(400),1), (Fr(2),Fr(3),Fr(5)))),
    'ratio(0) = 1 exactly  (kappa = 0 control: H = I, Sigma = Q/2)')

# C27: exact expansion witnesses, certified at rational (kappa, r)
wit = []
for q, nm in (((1,1,'r'), 'end'), ((1,'r',1), 'centre')):
    for rv in (Fr(10), Fr(14), Fr(20), Fr(50)):
        for k in [Fr(i, 10) for i in range(1, 60)]:
            qq = tuple(rv ** 2 if x == 'r' else Fr(x) for x in q)
            v = ratio(k, qq)
            if v > 1: wit.append((nm, rv, k, v)); break
print()
print('  certified expansion witnesses (exact rationals, ratio > 1):')
for nm, rv, k, v in wit:
    print('    %-7s r = %-4s kappa = %-6s  det Sigma_k/det Sigma_0 = %s  = %.6f'
          % (nm, rv, k, v, float(v)))
chk(len(wit) >= 4 and all(v > 1 for *_, v in wit),
    'three-mode determinant EXPANSION occurs (contrary to the two-mode-only intuition)',
    '%d exact witnesses' % len(wit))

# C28: exact critical r per orientation (bisection on exact rationals, sign of max over a kappa grid)
def expands(rv, q):
    qq = tuple(rv ** 2 if x == 'r' else Fr(x) for x in q)
    return any(ratio(Fr(i, 20), qq) > 1 for i in range(1, 400))
print()
for q, nm in (((1,1,'r'), 'Q = diag(1,1,r^2)  (end node) '), ((1,'r',1), 'Q = diag(1,r^2,1)  (centre node)')):
    lo, hi = Fr(1), Fr(60)
    for _ in range(26):
        mid = (lo + hi) / 2
        if expands(mid, q): hi = mid
        else: lo = mid
    print('  %s  critical r bracketed: no expansion at r = %.8f, expansion at r = %.8f'
          % (nm, float(lo), float(hi)))
    chk(not expands(lo, q) and expands(hi, q),
        'exact sign-change bracket for the three-mode threshold (%s)' % nm.split()[2],
        'width %.2e' % float(hi - lo))

# C29: the ceiling theorem's kappa-window is respected by every witness
print()
bad = []
for nm, rv, k, v in wit:
    q = (1, 1, rv ** 2) if nm == 'end' else (1, rv ** 2, 1)
    q1, q2, q3 = map(Fr, q)
    rho = ((q1+q2+q3)/3) * ((q1+q3)/2) * ((q1+4*q2+q3)/6) / (q1*q2*q3)
    detH = (1 + k) * (1 + 3 * k)
    if not (detH < rho): bad.append((nm, rv, k, float(detH), float(rho)))
chk(not bad, 'every expansion witness satisfies the proved necessary condition det H_kappa < rho(Q,L)',
    'no-expansion ceiling theorem holds in the three-mode case')

# C30: large-coupling decay is exactly order kappa^-2 with the predicted constant
print()
print('  large-coupling behaviour (Q = diag(1,1,400)):')
q = (1, 1, Fr(400))
for k in (Fr(10**3), Fr(10**4), Fr(10**5)):
    print('    kappa = %-8s ratio = %.6e   kappa^2 * ratio = %.8f' % (k, float(ratio(k,q)), float(k*k*ratio(k,q))))
# exact limit:  only the kernel mode (l=0) stays O(1); the two nonzero modes each contribute
# one power of kappa, and the kernel mode decorrelates (c_0j -> 0), leaving
#   kappa^2 * ratio  ->  Qt00 * ( Qt11*Qt22/3 - Qt12^2/4 ) / det Q.
q1, q2, q3 = map(Fr, q)
Qt00 = (q1+q2+q3)/3; Qt11 = (q1+q3)/2; Qt22 = (q1+4*q2+q3)/6; s12 = (q1-q3)**2/12
Lexact = Qt00 * (Qt11*Qt22/3 - s12/4) / (q1*q2*q3)
seq = [Fr(k)*Fr(k)*ratio(Fr(k), q) for k in (10**4, 10**5, 10**6)]
err = [abs(v - Lexact) for v in seq]
print('    exact predicted limit = %s = %.7f' % (Lexact, float(Lexact)))
print('    |kappa^2*ratio - limit| at kappa = 1e4, 1e5, 1e6 : %.3e %.3e %.3e'
      % tuple(float(e) for e in err))
# the approach is O(1/kappa): each decade must cut the error by a factor near 10
rats = [float(err[i] / err[i + 1]) for i in range(2)]
chk(Lexact > 0 and all(8 < x < 12 for x in rats),
    'ratio = Theta(kappa^-2) with the DERIVED constant Qt00*(Qt11*Qt22/3 - Qt12^2/4)/det Q',
    'limit %.7f, error falls by %.2f and %.2f per decade (O(1/kappa) as predicted)'
    % (float(Lexact), rats[0], rats[1]))

print()
print('=' * 92)
print('SECTION 5 TOTALS: %d checks, %d passed, %d failed' % (npass + nfail, npass, nfail))
print('=' * 92)
