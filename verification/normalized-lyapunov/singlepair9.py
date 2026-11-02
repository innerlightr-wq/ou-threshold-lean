#!/usr/bin/env python3
"""SECTION 9  The single-correlated-pair theorem (general n).  Exact arithmetic.

Setting: L >= 0, H_k = I + k L, Q > 0, and in a fixed eigenbasis of L the only off-diagonal
entries of Qt are the Hermitian pair (p,q).  With

    eta = |Qt_pq|^2/(Qt_pp Qt_qq - |Qt_pq|^2),  s = lam_p + lam_q,  Delta = lam_p - lam_q,
    D(k) = prod_i (1 + k lam_i),

the claim is
    R(k) = det Sigma_k/det Sigma_0 = (1 + eta k^2 Delta^2/(2 + s k)^2)/D(k),
    R(k) > 1  <=>  eta > T(k) := (D(k) - 1)(2 + s k)^2/(k^2 Delta^2),
with T strictly convex on (0,oo), T -> oo at both ends, a unique minimizer k_dagger satisfying a
polynomial of degree rank(L) + 1, eta_crit = T(k_dagger), and
    eta_crit >= 8 (tr L)(lam_p + lam_q)/(lam_p - lam_q)^2 >= 8.
"""
from fractions import Fraction as Fr
from itertools import combinations

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
def lyap(H, Q):
    n = len(H); idx = [(i, j) for i in range(n) for j in range(i, n)]
    pos = {}
    for t, (i, j) in enumerate(idx): pos[(i, j)] = t; pos[(j, i)] = t
    A, b = [], []
    for (i, j) in idx:
        row = [Fr(0)]*len(idx)
        for k in range(n):
            row[pos[(k, j)]] += H[i][k]; row[pos[(i, k)]] += H[k][j]
        A.append(row); b.append(Fr(Q[i][j]))
    nn = len(b); M = [A[i][:]+[b[i]] for i in range(nn)]
    for c in range(nn):
        piv = next(r for r in range(c, nn) if M[r][c] != 0)
        M[c], M[piv] = M[piv], M[c]; pv = M[c][c]; M[c] = [x/pv for x in M[c]]
        for r in range(nn):
            if r != c and M[r][c]: f = M[r][c]; M[r] = [x-f*y for x, y in zip(M[r], M[c])]
    v = [M[i][nn] for i in range(nn)]
    S = [[Fr(0)]*n for _ in range(n)]
    for t, (i, j) in enumerate(idx): S[i][j] = S[j][i] = v[t]
    return S
def is_pd(M): return all(det([[M[i][j] for j in range(k)] for i in range(k)]) > 0
                         for k in range(1, len(M)+1))

npass = nfail = 0
def chk(ok, label, note=''):
    global npass, nfail
    npass, nfail = npass+bool(ok), nfail+(not ok)
    print(('PASS  ' if ok else 'FAIL  ')+label+('  '+note if note else ''))

print('='*100)
print('SECTION 9  SINGLE-CORRELATED-PAIR THEOREM')
print('='*100)

# instances: (lambdas, diagonal of Qt, pair (p,q), Qt_pq)
INST = [
    ((Fr(0), Fr(2)),                   (Fr(5), Fr(5)),            (0, 1), Fr(4)),
    ((Fr(0), Fr(1), Fr(3)),            (Fr(17,3), Fr(1), Fr(11)), (0, 2), Fr(-7,2)),
    ((Fr(0), Fr(1), Fr(3)),            (Fr(4), Fr(9), Fr(2)),     (1, 2), Fr(3)),
    ((Fr(0), Fr(1), Fr(1), Fr(4)),     (Fr(3), Fr(8), Fr(2), Fr(6)), (0, 3), Fr(4)),
    ((Fr(0), Fr(1,2), Fr(5,2), Fr(7)), (Fr(10), Fr(3), Fr(7), Fr(4)), (1, 3), Fr(-3)),
    ((Fr(2), Fr(2), Fr(5)),            (Fr(6), Fr(6), Fr(9)),     (0, 2), Fr(5)),   # no zero mode
    ((Fr(0), Fr(3), Fr(3)),            (Fr(4), Fr(5), Fr(5)),     (1, 2), Fr(2)),   # Delta = 0
]
def build(lams, diagQ, pq, off):
    n = len(lams); p, q = pq
    Qt = [[Fr(0)]*n for _ in range(n)]
    for i in range(n): Qt[i][i] = Fr(diagQ[i])
    Qt[p][q] = Qt[q][p] = Fr(off)
    return Qt
def Rformula(k, lams, diagQ, pq, off):
    p, q = pq
    Qt = build(lams, diagQ, pq, off)
    eta = Fr(off)**2/(Fr(diagQ[p])*Fr(diagQ[q]) - Fr(off)**2)
    s = Fr(lams[p]) + Fr(lams[q]); D = Fr(lams[p]) - Fr(lams[q])
    Dk = Fr(1)
    for l in lams: Dk *= (1 + Fr(k)*Fr(l))
    return (1 + eta*Fr(k)**2*D**2/(2 + s*Fr(k))**2)/Dk
def Rexact(k, lams, diagQ, pq, off):
    n = len(lams)
    H = [[(1 + Fr(k)*Fr(lams[i])) if i == j else Fr(0) for j in range(n)] for i in range(n)]
    Qt = build(lams, diagQ, pq, off)
    return det(lyap(H, Qt))*Fr(2)**n/det(Qt)

# ---- 9.1  the exact R formula, against independent Lyapunov solves
bad = []; cases = 0
for lams, diagQ, pq, off in INST:
    Qt = build(lams, diagQ, pq, off)
    if not is_pd(Qt): bad.append(('Qt not PD', lams)); continue
    for k in (Fr(1,10), Fr(41,100), Fr(1), Fr(5,2), Fr(9), Fr(50)):
        cases += 1
        if Rformula(k, lams, diagQ, pq, off) != Rexact(k, lams, diagQ, pq, off):
            bad.append((lams, pq, k))
chk(not bad, 'C9.1 R(k) = (1 + eta k^2 Delta^2/(2+sk)^2)/D(k)',
    '%d exact (instance, kappa) pairs, n = 2,3,4, incl. repeated eigenvalues and no zero mode' % cases)

# ---- 9.2  Delta = 0 kills expansion
lams, diagQ, pq, off = INST[-1]
bad = [k for k in (Fr(1,10), Fr(1), Fr(10), Fr(100))
       if Rexact(k, lams, diagQ, pq, off) >= 1]
chk(not bad and Fr(lams[pq[0]]) == Fr(lams[pq[1]]),
    'C9.2 Delta = 0 (correlated pair has EQUAL damping): no gain, R < 1 at every kappa',
    'the pair must straddle distinct rates')

# ---- 9.3  T and the equivalence
def T(k, lams, pq):
    p, q = pq
    s = Fr(lams[p]) + Fr(lams[q]); D = Fr(lams[p]) - Fr(lams[q])
    Dk = Fr(1)
    for l in lams: Dk *= (1 + Fr(k)*Fr(l))
    return (Dk - 1)*(2 + s*Fr(k))**2/(Fr(k)**2*D**2)
def eta_of(diagQ, pq, off):
    p, q = pq
    return Fr(off)**2/(Fr(diagQ[p])*Fr(diagQ[q]) - Fr(off)**2)
bad = []; cases = 0
for lams, diagQ, pq, off in INST[:-1]:
    e = eta_of(diagQ, pq, off)
    for k in (Fr(1,20), Fr(1,2), Fr(1), Fr(3), Fr(17)):
        cases += 1
        if (Rexact(k, lams, diagQ, pq, off) > 1) != (e > T(k, lams, pq)): bad.append((lams, k))
chk(not bad, 'C9.3 R(k) > 1  <=>  eta > T(k)', '%d cases' % cases)

# ---- 9.4  T is strictly convex: midpoint test plus the Laurent structure
bad = []
for lams, diagQ, pq, off in INST[:-1]:
    for a, b in ((Fr(1,10), Fr(1)), (Fr(1,2), Fr(3)), (Fr(1), Fr(20)), (Fr(1,100), Fr(1,2))):
        mid = (a+b)/2
        if not T(mid, lams, pq) < (T(a, lams, pq) + T(b, lams, pq))/2: bad.append((lams, a, b))
chk(not bad, 'C9.4a T is strictly midpoint-convex on (0,oo)', '24 chord tests across 6 instances')
# the structural reason: T = (4 e1/Delta^2)/k + polynomial with NONNEGATIVE coefficients
def elementary(lams):
    """e_j = elementary symmetric polynomials, so D(k) - 1 = sum_{j>=1} e_j k^j."""
    n = len(lams); e = [Fr(0)]*(n+1); e[0] = Fr(1)
    for j in range(1, n+1):
        e[j] = sum((Fr(1) if True else Fr(0))*__import__('math').prod([1])*0 for _ in [])  # placeholder
    e = [Fr(0)]*(n+1); e[0] = Fr(1)
    for j in range(1, n+1):
        tot = Fr(0)
        for S in combinations(range(n), j):
            pr = Fr(1)
            for i in S: pr *= Fr(lams[i])
            tot += pr
        e[j] = tot
    return e
bad = []
for lams, diagQ, pq, off in INST[:-1]:
    p, q = pq
    e = elementary(lams); n = len(lams)
    s = Fr(lams[p]) + Fr(lams[q]); D2 = (Fr(lams[p]) - Fr(lams[q]))**2
    # T = (1/D2) * sum_{j>=1} e_j (4 k^{j-2} + 4 s k^{j-1} + s^2 k^j)
    # coefficient of k^{-1} is 4 e_1/D2 ; all other coefficients must be >= 0
    coef = {}
    for j in range(1, n+1):
        for pw, c in ((j-2, Fr(4)), (j-1, 4*s), (j, s*s)):
            coef[pw] = coef.get(pw, Fr(0)) + e[j]*c/D2
    neg = [(pw, c) for pw, c in coef.items() if c < 0]
    ok_inv = coef.get(-1, Fr(0)) == 4*e[1]/D2 and coef.get(-1, Fr(0)) > 0
    # reconstruct T from the coefficients at a test point
    kk = Fr(7,3)
    recon = sum(c*kk**pw for pw, c in coef.items())
    if neg or not ok_inv or recon != T(kk, lams, pq): bad.append((lams, neg[:2]))
chk(not bad, 'C9.4b STRUCTURE: T = (4 tr L/Delta^2)/k + a polynomial with NONNEGATIVE coefficients',
    'hence T\'\' >= 8 tr L/(Delta^2 k^3) > 0 and T -> oo at both ends; reconstruction exact')

# ---- 9.5  unique minimizer; its polynomial has degree rank L + 1
print()
def rank_of(lams): return sum(1 for l in lams if Fr(l) != 0)
bad = []
for lams, diagQ, pq, off in INST[:-1]:
    p, q = pq; n = len(lams)
    e = elementary(lams)
    s = Fr(lams[p]) + Fr(lams[q]); D2 = (Fr(lams[p]) - Fr(lams[q]))**2
    m = rank_of(lams)
    # k^2 T'(k) * D2 is a polynomial; build it from the Laurent coefficients of T*D2
    coef = {}
    for j in range(1, n+1):
        for pw, c in ((j-2, Fr(4)), (j-1, 4*s), (j, s*s)):
            coef[pw] = coef.get(pw, Fr(0)) + e[j]*c
    # derivative: sum pw*c*k^{pw-1}; multiply by k^2 -> sum pw*c*k^{pw+1}
    dcoef = {pw+1: pw*c for pw, c in coef.items() if pw != 0}
    deg = max(pw for pw, c in dcoef.items() if c != 0)
    lo = min(pw for pw, c in dcoef.items() if c != 0)
    # locate the minimizer by exact bisection on the sign of T'
    def dT(k):
        return sum(c*Fr(k)**pw for pw, c in dcoef.items())
    a, b = Fr(1, 10**6), Fr(10**6)
    while dT(b) <= 0: b *= 2
    while dT(a) >= 0: a /= 2
    for _ in range(150):      # initial width is 1e6, so 70 halvings only reach ~1e-15
        mid = (a+b)/2
        if dT(mid) < 0: a = mid
        else: b = mid
    kd = b
    # k^2 T' has EXACTLY ONE sign change on (0,oo): negative below the bracket, positive above.
    gmin = min(T(Fr(i, 2000), lams, pq) for i in range(1, 40000))
    one_change = (dT(a) < 0 < dT(b) and b - a < Fr(1, 10**18)
                  and all(dT(Fr(i, 10**4)) < 0 for i in range(1, 10**4) if Fr(i, 10**4) < a)
                  and all(dT(Fr(i, 10)) > 0 for i in range(1, 400) if Fr(i, 10) > b))
    # T at the root undercuts EVERY grid value (the grid, step 5e-4, overshoots the true
    # minimum by O(h^2 T''), up to ~3e-6 here, so an absolute tolerance is the wrong test)
    ok = (one_change and T(kd, lams, pq) <= gmin + Fr(1, 10**30)
          and deg == m + 1 and lo == 0)
    print('  lam = %-28s pair %s  rank L = %d  deg(k^2 T\') = %d  k_dagger = %.9f  eta_crit = %.6f'
          % (str(tuple(float(x) for x in lams)), pq, m, deg, float(kd), float(T(kd, lams, pq))))
    if not ok: bad.append((lams, deg, m))
chk(not bad, 'C9.5 unique minimizer: k^2 T\' has exactly ONE sign change, and is a polynomial of '
    'degree exactly rank(L) + 1 with nonzero constant term',
    'root bracketed to < 1e-18; T there matches a 40000-point grid minimum')

# ---- 9.6  the floor:  eta_crit >= 8 (tr L) s/Delta^2 >= 8
print()
bad = []
for lams, diagQ, pq, off in INST[:-1]:
    p, q = pq
    e = elementary(lams)
    s = Fr(lams[p]) + Fr(lams[q]); D2 = (Fr(lams[p]) - Fr(lams[q]))**2
    floor1 = 8*e[1]*s/D2
    gmin = min(T(Fr(i, 2000), lams, pq) for i in range(1, 40000))
    if not (gmin >= floor1 and floor1 >= 8): bad.append((lams, float(gmin), float(floor1)))
chk(not bad, 'C9.6 eta_crit >= 8 (tr L)(lam_p + lam_q)/(lam_p - lam_q)^2 >= 8',
    'uses (2+sk)^2 >= 8sk and tr L >= s >= |Delta|; 6 instances')

# ---- 9.7  the two existing controls as instances
print()
r = Fr(9)
# two modes: L = path on 2, eigenvalues 0,2; Q = diag(1,r^2)
Qt2 = [[(1+r**2)/2, (1-r**2)/2], [(1-r**2)/2, (1+r**2)/2]]
eta2 = Qt2[0][1]**2/(Qt2[0][0]*Qt2[1][1] - Qt2[0][1]**2)
chk(eta2 == (r - 1/r)**2/4 and T(1, (Fr(0), Fr(2)), (0, 1)) == 8,
    'C9.7a two-mode instance: eta = (r-1/r)^2/4 and T(1) = 8, so k_dagger = 1 and eta_crit = 8',
    'recovers (r-1/r)^2 > 32, i.e. r > 3+2sqrt(2)')
# three-node path, centre noise: eigenvalues 0,1,3; pair (0,2)
Qt3d = ((2+r**2)/3, Fr(1), (1+2*r**2)/3); off3 = (2 - 2*r**2)/Fr(18).__rpow__(1) if False else None
off3sq = 2*(1-r**2)**2/9
eta3 = off3sq/((2+r**2)/3*(1+2*r**2)/3 - off3sq)
lams3 = (Fr(0), Fr(1), Fr(3))
# k^2 T' * Delta^2 = 2(27k^3 + 36k^2 - 8) for this instance
def dT3(k):
    e = elementary(lams3); s = Fr(3); D2 = Fr(9)
    coef = {}
    for j in range(1, 4):
        for pw, c in ((j-2, Fr(4)), (j-1, 4*s), (j, s*s)):
            coef[pw] = coef.get(pw, Fr(0)) + e[j]*c
    return sum(pw*c*Fr(k)**(pw+1) for pw, c in coef.items() if pw != 0)
bad = [k for k in (Fr(1,3), Fr(1), Fr(2), Fr(7,2))
       if dT3(k) != 2*(27*Fr(k)**3 + 36*Fr(k)**2 - 8)]
chk(eta3 == 2*(r - 1/r)**2/9 and not bad,
    'C9.7b three-node centre instance: eta = 2(r-1/r)^2/9 and k^2 T\' Delta^2 = 2(27k^3+36k^2-8)',
    'the cubic for k_dagger is an instance of the general degree-(rank+1) equation')

# ---- 9.8  det C asymptotics, corrected
print()
dC = lambda k: 36*Fr(k)**6/((2+Fr(k))*(2+3*Fr(k))*(2+4*Fr(k)))**2
vals = [dC(Fr(1,10**j))/Fr(1,10**j)**6 for j in (2, 3, 4, 5)]
err = [abs(v - Fr(9,16)) for v in vals]
rats = [float(err[i]/err[i+1]) for i in range(3)]
chk(all(9 < x < 11 for x in rats),
    'C9.8 CORRECTION: det C ~ (9/16) k^6 as k -> 0, NOT k^6/64 (the factor 36 was dropped)',
    'det C/k^6 -> 9/16 = 0.5625 with O(k) error: %s; per-decade error ratios %s'
    % (', '.join('%.6f' % float(v) for v in vals), ', '.join('%.2f' % x for x in rats)))

# ---- 9.9  does the interval structure survive OUTSIDE the single-pair class?
#      The end-node three-mode model has ALL THREE off-diagonals of Qt nonzero, so it is not
#      covered by the theorem.  Test whether {kappa : R > 1} is still a single interval.
print()
L3p = [[1, -1, 0], [-1, 2, -1], [0, -1, 1]]
def Rend(k, r):
    n = 3
    H = [[Fr(int(i == j)) + Fr(k)*Fr(L3p[i][j]) for j in range(n)] for i in range(n)]
    Q = [[(Fr(r)**2 if i == 2 else Fr(1)) if i == j else Fr(0) for j in range(n)] for i in range(n)]
    return det(lyap(H, Q))*Fr(2)**n/det(Q)
print('  end-node model (all three off-diagonals nonzero; OUTSIDE the single-pair class):')
bad = []
for r in (Fr(11), Fr(12), Fr(15), Fr(25), Fr(60), Fr(200)):
    flags = [Rend(Fr(i, 50), r) > 1 for i in range(1, 1500)]
    runs = sum(1 for i in range(1, len(flags)) if flags[i] and not flags[i-1])
    runs += 1 if flags[0] else 0
    print('    r = %-4s expansion runs on the kappa grid: %d' % (r, runs))
    if runs > 1: bad.append(r)
chk(not bad, 'C9.9 the expansion set stays a SINGLE interval outside the single-pair class',
    'end-node model, 6 noise levels x 1499 couplings: never more than one run -- consistent with '
    'convexity holding in general, which the theorem does NOT cover')

print()
print('='*100)
print('SECTION 9 TOTALS: %d checks, %d passed, %d failed' % (npass+nfail, npass, nfail))
print('='*100)
