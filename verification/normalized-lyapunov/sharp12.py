#!/usr/bin/env python3
"""SECTION 12  Theorem H is SHARP at k = 3: three disjoint correlated pairs, three windows.

Reviewer's construction.  Q_b = [[1, b], [b, 1+b^2]] has det 1 and is positive definite.  Take
    Qt = diag(Q_3, Q_60, Q_3500),   L = diag(0, 1000, 0, 1, 0, 1/10000).
Exactly three nonzero off-diagonal pairs, all DISJOINT, so no determinant cycle terms.  Because Qt
and L are block diagonal, det Sigma and det Sigma_0 both factor over blocks, and
    R(kappa) = prod_j F_{a_j, b_j}(kappa),   F_{a,b} = [1 + b^2 (a k/(2+a k))^2]/(1 + a k).
The PRODUCT structure is what the additive star search of section 11 could not reach.
"""
from fractions import Fraction as Fr
from itertools import permutations, combinations

def det(M):
    n = len(M); M = [row[:] for row in M]; s = Fr(1)
    for c in range(n):
        piv = next((r for r in range(c, n) if M[r][c] != 0), None)
        if piv is None: return Fr(0)
        if piv != c: M[c], M[piv] = M[piv], M[c]; s = -s
        s *= M[c][c]; pv = M[c][c]; M[c] = [x/pv for x in M[c]]
        for r in range(c+1, n):
            if M[r][c]: f = M[r][c]; M[r] = [x-f*y for x, y in zip(M[r], M[c])]
    return s
def is_pd(M):
    return all(det([[M[i][j] for j in range(k)] for i in range(k)]) > 0 for k in range(1, len(M)+1))

# ---- polynomials
def pn(p):
    while len(p) > 1 and p[-1] == 0: p = p[:-1]
    return p
def padd(p, q):
    n = max(len(p), len(q))
    return pn([(p[i] if i < len(p) else Fr(0)) + (q[i] if i < len(q) else Fr(0)) for i in range(n)])
def pmul(p, q):
    out = [Fr(0)]*(len(p)+len(q)-1)
    for i, x in enumerate(p):
        if x:
            for j, y in enumerate(q): out[i+j] += x*y
    return pn(out)
def pev(p, t): return sum((c*Fr(t)**i for i, c in enumerate(p)), Fr(0))
def pdivmod(nu, de):
    nu = nu[:]; q = [Fr(0)]*max(1, len(nu)-len(de)+1)
    while len(nu) >= len(de) and pn(nu) != [Fr(0)]:
        d = len(nu)-len(de)
        if d < 0: break
        c = nu[-1]/de[-1]; q[d] = c
        for i, y in enumerate(de): nu[d+i] -= c*y
        nu = pn(nu)
        if nu == [Fr(0)]: break
    return pn(q), pn(nu)

npass = nfail = 0
def chk(ok, label, note=''):
    global npass, nfail
    npass, nfail = npass+bool(ok), nfail+(not ok)
    print(('PASS  ' if ok else 'FAIL  ')+label+('  '+note if note else ''))

print('='*102)
print('SECTION 12  SHARPNESS OF THEOREM H AT k = 3')
print('='*102)

BS = [(Fr(1000), Fr(3)), (Fr(1), Fr(60)), (Fr(1,10000), Fr(3500))]
LAM = [Fr(0), Fr(1000), Fr(0), Fr(1), Fr(0), Fr(1,10000)]
def Qt_of():
    Q = [[Fr(0)]*6 for _ in range(6)]
    for j, (a, b) in enumerate(BS):
        Q[2*j][2*j] = Fr(1); Q[2*j][2*j+1] = Q[2*j+1][2*j] = b
        Q[2*j+1][2*j+1] = 1 + b**2
    return Q
QT = Qt_of()

# ---- 12.1  the block is positive definite with determinant 1
bad = []
for a, b in BS:
    Qb = [[Fr(1), b], [b, 1+b**2]]
    if det(Qb) != 1 or not is_pd(Qb): bad.append(b)
chk(not bad and is_pd(QT) and det(QT) == 1,
    'C12.1 Q_b = [[1,b],[b,1+b^2]] is positive definite with det 1; Qt is PD with det 1',
    'b = 3, 60, 3500')
pairs = [(i, j) for i in range(6) for j in range(i+1, 6) if QT[i][j] != 0]
chk(pairs == [(0, 1), (2, 3), (4, 5)],
    'C12.2 exactly k = 3 nonzero off-diagonal pairs, pairwise DISJOINT (no cycle terms)',
    'pairs %s' % pairs)

# ---- 12.3  Sigma from the eigenbasis formula; verify it solves the Lyapunov equation; and the
#            product form of R
def Sigma(k, lam, Q):
    n = len(lam)
    return [[Fr(Q[i][j])/(2 + Fr(k)*(Fr(lam[i])+Fr(lam[j]))) for j in range(n)] for i in range(n)]
def check_lyap(k, lam, Q, S):
    n = len(lam)
    H = [[(1 + Fr(k)*Fr(lam[i])) if i == j else Fr(0) for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            v = sum(H[i][m]*S[m][j] for m in range(n)) + sum(S[i][m]*H[m][j] for m in range(n))
            if v != Fr(Q[i][j]): return False
    return True
def R_direct(k, lam=LAM, Q=QT):
    S = Sigma(k, lam, Q)
    assert check_lyap(k, lam, Q, S), 'Sigma does not solve the Lyapunov equation'
    return det(S)*Fr(2)**len(lam)/det(Q)
def F(a, b, k):
    a, b, k = Fr(a), Fr(b), Fr(k)
    return (1 + b**2*(a*k/(2+a*k))**2)/(1+a*k)
def R_product(k):
    p = Fr(1)
    for a, b in BS: p *= F(a, b, k)
    return p
GRID = [Fr(1,10**5), Fr(1,500), Fr(1,20), Fr(1), Fr(10), Fr(100), Fr(1000)]
bad = [k for k in GRID + [Fr(1,7), Fr(3), Fr(10**4)] if R_direct(k) != R_product(k)]
chk(not bad, 'C12.3 R(kappa) = prod_j F_{a_j,b_j}(kappa), each Sigma verified against H S + S H = Qt',
    '10 exact couplings; block-diagonal Qt and L make both determinants factor')

# ---- 12.4  the seven exact witnesses
print()
EXPECT = ['<', '>', '<', '>', '<', '>', '<']
bad = []
signs = []
for k, want in zip(GRID, EXPECT):
    v = R_direct(k)
    got = '>' if v > 1 else ('<' if v < 1 else '=')
    signs.append(got)
    print('  kappa = %-9s R = %.10f   %s 1   %s'
          % (k, float(v), got, 'expansion' if got == '>' else 'contraction'))
    if got != want: bad.append((k, got, want))
chk(not bad, 'C12.4 the seven reported values alternate contraction/expansion exactly as claimed',
    'all comparisons with 1 exact over Q; decimals shown for readability only')
runs = sum(1 for i in range(len(signs)) if signs[i] == '>' and (i == 0 or signs[i-1] != '>'))
chk(runs == 3, 'C12.5 the alternation forces AT LEAST three expansion components',
    'and Theorem H permits at most k = 3, so there are EXACTLY three')

# ---- 12.6  the numerator polynomial: degree, sign pattern, and attainment of the 2k bound
print()
a_pol = [pn([Fr(1), Fr(l)]) for l in LAM]
B = [Fr(1)]
for (i, j) in pairs: B = pmul(B, pmul(padd(a_pol[i], a_pol[j]), padd(a_pol[i], a_pol[j])))
D = [Fr(1)]
for l in LAM: D = pmul(D, [Fr(1), Fr(l)])
# N = B * det(C o Qt): here Qt is block diagonal with only transpositions, so
# det(C o Qt) = prod_j [Qt_2j,2j Qt_2j+1,2j+1 - c_j^2 Qt_2j,2j+1^2] and c_j^2 = 4 a_2j a_2j+1/(..)^2
N = [Fr(1)]
for j, (i0, i1) in enumerate(pairs):
    s2 = pmul(padd(a_pol[i0], a_pol[i1]), padd(a_pol[i0], a_pol[i1]))
    diagprod = pmul([QT[i0][i0]*QT[i1][i1]], s2)
    cross = pmul([4*QT[i0][i1]**2], pmul(a_pol[i0], a_pol[i1]))
    N = pmul(N, padd(diagprod, [-x for x in cross]))
numer = padd(N, [-x for x in pmul(B, pmul(D, [det(QT)]))])
A, rem = pdivmod(numer, [Fr(0), Fr(1)])
k_pairs = len(pairs)
sg = [1 if c > 0 else (-1 if c < 0 else 0) for c in A]
nz = [s for s in sg if s != 0]
sv = sum(1 for i in range(1, len(nz)) if nz[i] != nz[i-1])
print('  deg A = %d,  coefficient signs (ascending): %s'
      % (len(A)-1, ''.join('+' if s > 0 else ('-' if s < 0 else '0') for s in sg)))
print('  sign variations = %d,  Theorem H bound 2k = %d' % (sv, 2*k_pairs))
chk(rem == [Fr(0)] and len(A)-1 == 8
    and ''.join('+' if s > 0 else ('-' if s < 0 else '0') for s in sg) == '-+-+-+---'
    and sv == 2*k_pairs,
    'C12.6 the sign pattern is -,+,-,+,-,+,-,-,- with exactly 2k = 6 sign variations',
    'so Descartes is TIGHT here: the six crossings forced by the witnesses use the whole budget')
bad = [k for k in GRID if (pev(A, k) > 0) != (R_direct(k) > 1)]
chk(not bad, 'C12.7 sign(A) agrees with sign(R - 1) at all seven witnesses',
    'independent polynomial route reproduces the alternation')

# ---- 12.8  a CONNECTED realization keeps all seven signs
print()
EPS = Fr(1, 10**8)
AJ = [Fr(1000), Fr(1), Fr(1,10000)]
W = [(a - 4*EPS)/2 for a in AJ]
chk(all(w > 0 for w in W), 'C12.8 intra-pair weights (a_j - 4 eps)/2 are positive', 'eps = 1e-8')
# build the 6-vertex weighted Laplacian: every inter-pair edge eps, intra-pair edge W[j]
wt = [[Fr(0)]*6 for _ in range(6)]
for i in range(6):
    for j in range(6):
        if i == j: continue
        wt[i][j] = W[i//2] if i//2 == j//2 else EPS
Lg = [[Fr(0)]*6 for _ in range(6)]
for i in range(6):
    Lg[i][i] = sum(wt[i][j] for j in range(6) if j != i)
    for j in range(6):
        if j != i: Lg[i][j] = -wt[i][j]
# verify the predicted eigenvectors exactly
def mv(M, v): return [sum(M[i][j]*v[j] for j in range(len(v))) for i in range(len(M))]
bad = []
ones = [Fr(1)]*6
if any(x != 0 for x in mv(Lg, ones)): bad.append('kernel')
for j in range(3):
    v = [Fr(0)]*6; v[2*j] = Fr(1); v[2*j+1] = Fr(-1)
    out = mv(Lg, v)
    if any(out[m] != AJ[j]*v[m] for m in range(6)): bad.append(('antisym', j))
for c in ([Fr(1), Fr(1), Fr(-1), Fr(-1), Fr(0), Fr(0)], [Fr(1), Fr(1), Fr(0), Fr(0), Fr(-1), Fr(-1)]):
    out = mv(Lg, c)
    if any(out[m] != 6*EPS*c[m] for m in range(6)): bad.append('sym')
chk(not bad, 'C12.9 the connected graph has Laplacian eigenvalues 0, a_1, a_2, a_3, 6 eps, 6 eps',
    'verified by applying L to the explicit eigenvectors exactly; all edge weights > 0 so the '
    'graph is connected, and the kernel is one-dimensional')
LAM2 = [Fr(0), Fr(1000), 6*EPS, Fr(1), 6*EPS, Fr(1,10000)]
bad = []
print('  connected realization, same Qt in the ordered eigenbasis:')
for k, want in zip(GRID, EXPECT):
    v = R_direct(k, LAM2, QT)
    got = '>' if v > 1 else ('<' if v < 1 else '=')
    if k in (Fr(10), Fr(100), Fr(1000)):
        print('    kappa = %-6s R = %.6f  %s 1' % (k, float(v), got))
    if got != want: bad.append((k, got, want))
chk(not bad, 'C12.10 all seven alternating signs SURVIVE on the connected network',
    'so sharpness at k = 3 holds with a connected graph and a one-dimensional kernel')

# ---- 12.11  what sharpness does and does not mean
print()
# same pattern, same L, but weaker correlations -> fewer windows
bad = []
counts = []
for scale in (Fr(1), Fr(1,2), Fr(1,10)):
    Q2 = [[Fr(0)]*6 for _ in range(6)]
    for j, (a, b) in enumerate(BS):
        bb = b*scale
        Q2[2*j][2*j] = Fr(1); Q2[2*j][2*j+1] = Q2[2*j+1][2*j] = bb
        Q2[2*j+1][2*j+1] = 1 + bb**2
    ks = [Fr(i, 10**6) for i in range(1, 300)] + [Fr(i, 10**4) for i in range(3, 300)] \
         + [Fr(i, 100) for i in range(3, 300)] + [Fr(i) for i in range(3, 400)] \
         + [Fr(i*10) for i in range(40, 400)]
    fl = [R_direct(x, LAM, Q2) > 1 for x in ks]
    c = sum(1 for i in range(len(fl)) if fl[i] and (i == 0 or not fl[i-1]))
    counts.append((scale, c))
print('  same correlation PATTERN (k = 3) and same L, correlations scaled by t:')
for scale, c in counts: print('    t = %-6s expansion components found: %d' % (scale, c))
chk(counts[0][1] == 3 and counts[-1][1] < 3,
    'C12.11 CORRECTION: sharpness does NOT mean the component count is determined by the pattern',
    'Theorem H is a structural CEILING that suitable rates and noise strengths attain; the same '
    'k = 3 pattern gives fewer windows when the correlations are weakened')

print()
print('='*102)
print('SECTION 12 TOTALS: %d checks, %d passed, %d failed' % (npass+nfail, npass, nfail))
print('='*102)
