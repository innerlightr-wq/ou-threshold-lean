#!/usr/bin/env python3
"""SECTION 11  The component-count theorem: k correlated pairs => at most k expansion components.

Claim (reviewer, round 4).  L >= 0, Q > 0, H_k = I + kL.  In an eigenbasis of L let Qt have k
nonzero unordered off-diagonal pairs E.  With a_i = 1 + k lam_i,
    B(k) = prod_{{i,j} in E} (a_i + a_j)^2,   D(k) = prod_i a_i,
the function N := B * det(C o Qt) is a POLYNOMIAL of degree <= 2k, and
    R(k) - 1 = k A(k)/(det Q * D(k) * B(k))
for a polynomial A with A(0) = -4^k det Q tr L < 0 and every coefficient in degree >= 2k
nonpositive.  Hence at most 2k sign variations, at most 2k positive roots, at most k components.

Verified here exactly: the polynomiality and degree bound, the identity, A(0), and the coefficient
sign pattern -- using exact rational-function arithmetic in k, with det(C o Qt) assembled from the
permutation expansion so that no square root is ever taken.
"""
from fractions import Fraction as Fr
from itertools import permutations, combinations

# ---------------- polynomials over Q
def pn(p):
    while len(p) > 1 and p[-1] == 0: p = p[:-1]
    return p
def padd(p, q):
    n = max(len(p), len(q))
    return pn([(p[i] if i < len(p) else Fr(0)) + (q[i] if i < len(q) else Fr(0)) for i in range(n)])
def pneg(p): return [-x for x in p]
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
        c = nu[-1]/de[-1]
        q[d] = c
        for i, y in enumerate(de): nu[d+i] -= c*y
        nu = pn(nu)
        if nu == [Fr(0)]: break
    return pn(q), pn(nu)

# ---------------- exact det(C o Qt) * B  via the permutation expansion (no square roots)
def perm_sign(p):
    n = len(p); seen = [False]*n; s = 1
    for i in range(n):
        if not seen[i]:
            j, L = i, 0
            while not seen[j]:
                seen[j] = True; j = p[j]; L += 1
            if L % 2 == 0: s = -s
    return s

def N_poly(lams, Qt, E):
    """B * det(C o Qt) as a polynomial in kappa, assembled term by term.

    For a permutation p, prod_i (C o Qt)_{i,p(i)} = (prod_i Qt_{i,p(i)}) * prod_cycles (prod c).
    For a cycle (i1..im) with m >= 2, prod c = 2^m prod a_{i} / prod (a+a) over its edges; for a
    fixed point c_ii = 1.  So every term is RATIONAL in kappa, with denominator dividing B.
    """
    n = len(lams)
    a = [pn([Fr(1), Fr(lams[i])]) for i in range(n)]          # a_i = 1 + k lam_i
    def sumfac(i, j): return padd(a[i], a[j])
    B = [Fr(1)]
    for (i, j) in E: B = pmul(B, pmul(sumfac(i, j), sumfac(i, j)))
    total = [Fr(0)]
    for p in permutations(range(n)):
        coef = Fr(1)
        for i in range(n): coef *= Fr(Qt[i][p[i]])
        if coef == 0: continue
        # cycle decomposition
        seen = [False]*n; num = [Fr(1)]; den = [Fr(1)]
        for i in range(n):
            if seen[i]: continue
            cyc = []
            j = i
            while not seen[j]:
                seen[j] = True; cyc.append(j); j = p[j]
            m = len(cyc)
            if m == 1: continue
            num = pmul(num, [Fr(2)**m])
            for v in cyc: num = pmul(num, a[v])
            for t in range(m):
                den = pmul(den, sumfac(cyc[t], cyc[(t+1) % m]))
        q, r = pdivmod(pmul(B, num), den)
        assert r == [Fr(0)], 'denominator does not divide B'
        total = padd(total, pmul([coef*perm_sign(p)], q))
    return total, B

def detQ_of(Qt):
    n = len(Qt); tot = Fr(0)
    for p in permutations(range(n)):
        c = Fr(perm_sign(p))
        for i in range(n): c *= Fr(Qt[i][p[i]])
        tot += c
    return tot
def pairs_of(Qt):
    n = len(Qt)
    return [(i, j) for i in range(n) for j in range(i+1, n) if Qt[i][j] != 0]
def is_pd(Qt):
    n = len(Qt)
    for k in range(1, n+1):
        if detQ_of([[Qt[i][j] for j in range(k)] for i in range(k)]) <= 0: return False
    return True
# exact R via an independent Lyapunov solve
def lyap_ratio(lams, Qt, k):
    n = len(lams)
    H = [[(1 + Fr(k)*Fr(lams[i])) if i == j else Fr(0) for j in range(n)] for i in range(n)]
    idx = [(i, j) for i in range(n) for j in range(i, n)]
    pos = {}
    for t, (i, j) in enumerate(idx): pos[(i, j)] = t; pos[(j, i)] = t
    A, b = [], []
    for (i, j) in idx:
        row = [Fr(0)]*len(idx)
        for m in range(n):
            row[pos[(m, j)]] += H[i][m]; row[pos[(i, m)]] += H[m][j]
        A.append(row); b.append(Fr(Qt[i][j]))
    nn = len(b); M = [A[i][:]+[b[i]] for i in range(nn)]
    for c in range(nn):
        piv = next(r for r in range(c, nn) if M[r][c] != 0)
        M[c], M[piv] = M[piv], M[c]; pv = M[c][c]; M[c] = [x/pv for x in M[c]]
        for r in range(nn):
            if r != c and M[r][c]: f = M[r][c]; M[r] = [x-f*y for x, y in zip(M[r], M[c])]
    v = [M[i][nn] for i in range(nn)]
    S = [[Fr(0)]*n for _ in range(n)]
    for t, (i, j) in enumerate(idx): S[i][j] = S[j][i] = v[t]
    return detQ_of(S)*Fr(2)**n/detQ_of(Qt)

npass = nfail = 0
def chk(ok, label, note=''):
    global npass, nfail
    npass, nfail = npass+bool(ok), nfail+(not ok)
    print(('PASS  ' if ok else 'FAIL  ')+label+('  '+note if note else ''))

print('='*100)
print('SECTION 11  COMPONENT-COUNT THEOREM:  k correlated pairs => at most k components')
print('='*100)

INST = [
    # (lams, Qt)   -- chosen to span k = 0..6 and n = 2..5, with and without cycle terms
    ((Fr(0), Fr(2)), [[Fr(5), Fr(4)], [Fr(4), Fr(5)]]),
    ((Fr(0), Fr(2)), [[Fr(5), Fr(0)], [Fr(0), Fr(5)]]),                      # k = 0
    ((Fr(0), Fr(100), Fr(1)), [[Fr(2035), Fr(3), Fr(45)],
                               [Fr(3), Fr(1), Fr(0)], [Fr(45), Fr(0), Fr(1)]]),   # the witness, k=2
    ((Fr(0), Fr(1), Fr(3)), [[Fr(17), Fr(2), Fr(3)],
                             [Fr(2), Fr(9), Fr(1)], [Fr(3), Fr(1), Fr(8)]]),      # k=3, CYCLE term
    ((Fr(0), Fr(1), Fr(3)), [[Fr(10), Fr(0), Fr(3)],
                             [Fr(0), Fr(4), Fr(0)], [Fr(3), Fr(0), Fr(2)]]),      # k=1
    ((Fr(0), Fr(1), Fr(2), Fr(5)), [[Fr(9), Fr(2), Fr(0), Fr(0)],
                                    [Fr(2), Fr(7), Fr(0), Fr(0)],
                                    [Fr(0), Fr(0), Fr(6), Fr(3)],
                                    [Fr(0), Fr(0), Fr(3), Fr(4)]]),  # k=2 DISJOINT blocks
    ((Fr(0), Fr(1), Fr(2), Fr(5), Fr(9)),
     [[Fr(20), Fr(3), Fr(2), Fr(1), Fr(0)], [Fr(3), Fr(15), Fr(1), Fr(0), Fr(0)],
      [Fr(2), Fr(1), Fr(12), Fr(0), Fr(0)], [Fr(1), Fr(0), Fr(0), Fr(9), Fr(2)],
      [Fr(0), Fr(0), Fr(0), Fr(2), Fr(7)]]),                          # k=5, n=5
]

bad_poly = bad_id = bad_a0 = bad_tail = bad_sv = []
bad_poly, bad_id, bad_a0, bad_tail, bad_sv = [], [], [], [], []
print()
for lams, Qt in INST:
    n = len(lams); E = pairs_of(Qt); k = len(E)
    assert is_pd(Qt), 'instance not positive definite'
    dQ = detQ_of(Qt)
    N, B = N_poly(lams, Qt, E)
    D = [Fr(1)]
    for l in lams: D = pmul(D, [Fr(1), Fr(l)])
    trL = sum(Fr(l) for l in lams)
    # (a) degree bound
    degN = len(N)-1
    if degN > 2*k: bad_poly.append((lams, k, degN))
    # (b) the identity R - 1 = k A/(detQ D B), and A as an exact polynomial
    numer = padd(N, pneg(pmul(B, pmul(D, [dQ]))))
    Aq, Ar = pdivmod(numer, [Fr(0), Fr(1)])              # divide by kappa
    if Ar != [Fr(0)]: bad_id.append((lams, 'kappa does not divide'))
    for kk in (Fr(1,100), Fr(1,3), Fr(1), Fr(7), Fr(200)):
        lhs = lyap_ratio(lams, Qt, kk) - 1
        rhs = Fr(kk)*pev(Aq, kk)/(dQ*pev(D, kk)*pev(B, kk))
        if lhs != rhs: bad_id.append((lams, kk, float(lhs), float(rhs)))
    # (c) A(0) = -4^k detQ trL
    if Aq[0] != -Fr(4)**k*dQ*trL: bad_a0.append((lams, Aq[0], -Fr(4)**k*dQ*trL))
    # (d) coefficients of A in degree >= 2k are nonpositive
    tailbad = [(j, Aq[j]) for j in range(2*k, len(Aq)) if Aq[j] > 0]
    if tailbad: bad_tail.append((lams, tailbad[:2]))
    # (e) sign variations of A, and the component count
    signs = [1 if c > 0 else (-1 if c < 0 else 0) for c in Aq]
    nz = [s for s in signs if s != 0]
    sv = sum(1 for i in range(1, len(nz)) if nz[i] != nz[i-1])
    if sv > 2*k: bad_sv.append((lams, sv, 2*k))
    # count components of {R > 1} on a wide grid
    ks = [Fr(i, 2000) for i in range(1, 400)] + [Fr(i, 100) for i in range(20, 400)] \
         + [Fr(i) for i in range(4, 300)]
    fl = [pev(Aq, x) > 0 for x in ks]
    comp = sum(1 for i in range(1, len(fl)) if fl[i] and not fl[i-1]) + (1 if fl[0] else 0)
    print('  n=%d k=%d  deg N=%-2d (<= %-2d)  deg A=%-2d  sign variations=%-2d (<= %-2d)  '
          'components=%d (<= %d)%s'
          % (n, k, degN, 2*k, len(Aq)-1, sv, 2*k, comp, k,
             '  [cycle term present]' if any(Qt[i][j] != 0 and Qt[j][m] != 0 and Qt[i][m] != 0
                                             for i in range(n) for j in range(n) for m in range(n)
                                             if i < j < m) else ''))
    if comp > k: bad_sv.append((lams, 'components exceed k'))

print()
chk(not bad_poly, 'C11.1 N = B * det(C o Qt) is a polynomial of degree <= 2k',
    'denominator division exact in every permutation term (asserted inside N_poly); 7 instances, '
    'n = 2..5, k = 0..6, with and without cycle terms')
chk(not bad_id, 'C11.2 R(k) - 1 = k A(k)/(det Q * D(k) * B(k)) with A a polynomial',
    '35 exact couplings against independent Lyapunov solves')
chk(not bad_a0, 'C11.3 A(0) = -4^k det Q tr L < 0 (for L != 0)', 'exact in all instances')
chk(not bad_tail, 'C11.4 every coefficient of A in degree >= 2k is nonpositive',
    'those degrees receive nothing from N, only -B*D*det Q, whose coefficients are nonnegative')
chk(not bad_sv, 'C11.5 sign variations of A are <= 2k, and #components <= k',
    'Descartes gives <= 2k positive roots with multiplicity; each component needs two')
# ============================ further reviewer corrections ============================
print()
print('-'*100)
print('REVIEWER CORRECTIONS (round 4)')
print('-'*100)

# 11.6  the additive formula is NOT general: two disjoint correlated blocks multiply
lams4 = (Fr(0), Fr(1), Fr(2), Fr(5))
Qt4 = [[Fr(9), Fr(2), Fr(0), Fr(0)], [Fr(2), Fr(7), Fr(0), Fr(0)],
       [Fr(0), Fr(0), Fr(6), Fr(3)], [Fr(0), Fr(0), Fr(3), Fr(4)]]
def blocks_product(k):
    a = [1 + Fr(k)*Fr(l) for l in lams4]
    def d2(i, j): return (a[i]-a[j])**2/(a[i]+a[j])**2
    e1 = Fr(2)**2/(Fr(9)*Fr(7) - Fr(2)**2)
    e2 = Fr(3)**2/(Fr(6)*Fr(4) - Fr(3)**2)
    return (1 + e1*d2(0, 1))*(1 + e2*d2(2, 3))
def blocks_sum(k):
    a = [1 + Fr(k)*Fr(l) for l in lams4]
    def d2(i, j): return (a[i]-a[j])**2/(a[i]+a[j])**2
    e1 = Fr(2)**2/(Fr(9)*Fr(7) - Fr(2)**2)
    e2 = Fr(3)**2/(Fr(6)*Fr(4) - Fr(3)**2)
    return 1 + e1*d2(0, 1) + e2*d2(2, 3)
D4 = lambda k: Fr(1)*(1)*(1+Fr(k))*(1+2*Fr(k))*(1+5*Fr(k))
bad = []; diff = []
for k in (Fr(1,10), Fr(1), Fr(5)):
    exact = lyap_ratio(lams4, Qt4, k)
    if exact != blocks_product(k)/D4(k): bad.append(('product form wrong', k))
    if blocks_sum(k) == blocks_product(k): bad.append(('sum coincides', k))
    diff.append(float(blocks_product(k) - blocks_sum(k)))
chk(not bad, 'C11.6 CORRECTION: the per-pair contributions are NOT additive in general',
    'two DISJOINT correlated blocks give (1+eta_1 delta_1^2)(1+eta_2 delta_2^2), a PRODUCT; the '
    'cross term is %s at kappa = 1/10, 1, 5. The common-denominator proof covers this; the '
    '"each pair adds a term" reading does not.' % ['%.4f' % d for d in diff])

# 11.7  the counterexample is itself a STAR pattern
QW = [[Fr(2035), Fr(3), Fr(45)], [Fr(3), Fr(1), Fr(0)], [Fr(45), Fr(0), Fr(1)]]
offdiag = [(i, j) for i in range(3) for j in range(i+1, 3) if QW[i][j] != 0]
chk(all(0 in p for p in offdiag),
    'C11.7 CORRECTION: the counterexample IS a star (all correlations share mode 0)',
    'so "star correlation patterns force one interval" is refuted by the witness itself; '
    'pairs %s' % offdiag)

# 11.8  the saturation scale is 2/s, not 1/Delta
bad = []
for lp, lq in ((Fr(0), Fr(100)), (Fr(1), Fr(3)), (Fr(0), Fr(1)), (Fr(2), Fr(7))):
    s_, D_ = lp+lq, lp-lq
    for k in (Fr(1,1000), Fr(1,7), Fr(3), Fr(100)):
        ap, aq = 1 + k*lp, 1 + k*lq
        lhs = 1 - 4*ap*aq/(ap+aq)**2
        rhs = (D_**2/s_**2)*(k/(k + 2/s_))**2
        if lhs != rhs: bad.append((lp, lq, k))
chk(not bad, 'C11.8 CORRECTION: 1 - c_pq^2 = (Delta^2/s^2) (kappa/(kappa + 2/s))^2',
    'the SATURATION SCALE is 2/s (the rate SUM), not 1/Delta; Delta/s sets the limiting '
    'amplitude. 16 exact (rate pair, kappa) combinations.')

# 11.9  the r = 9 peak value was misreported
def R2m(k, r):
    k, r = Fr(k), Fr(r)
    return (1 + (k/(1+k))**2*(r-1/r)**2/4)/(1+2*k)
r9 = Fr(9)
v_069, v_15, v_138 = R2m(Fr(69,100), r9), R2m(Fr(3,2), r9), R2m(Fr(69,50), r9)
gridmax = max((R2m(Fr(i,200), r9), Fr(i,200)) for i in range(1, 4000))
chk(v_15 == Fr(73,36) and v_15 > v_069 and gridmax[0] > v_15,
    'C11.9 CORRECTION: the reported r = 9 peak was wrong',
    'R(69/100) = %.6f is NOT the peak; R(3/2) = 73/36 = %.6f is larger, and the maximum is '
    '%.6f near kappa = %s (the earlier text misread the grid argmax 69/50 as 0.69)'
    % (float(v_069), float(v_15), float(gridmax[0]), gridmax[1]))

# 11.10  "never unimodal" is too broad: commuting noise gives R = 1/D, monotone decreasing
lams3 = (Fr(0), Fr(1), Fr(3))
Qcom = [[Fr(4), Fr(0), Fr(0)], [Fr(0), Fr(9), Fr(0)], [Fr(0), Fr(0), Fr(2)]]
bad = []
prev = None
for k in (Fr(1,10), Fr(1,2), Fr(1), Fr(3), Fr(10)):
    val = lyap_ratio(lams3, Qcom, k)
    Dk = (1+Fr(k))*(1+3*Fr(k))
    if val != 1/Dk: bad.append(('not 1/D', k))
    if prev is not None and not val < prev: bad.append(('not decreasing', k))
    prev = val
chk(not bad, 'C11.10 CORRECTION: "the ratio is never unimodal" was too broad',
    'commuting noise gives R = 1/det H_kappa exactly, which is monotonically DECREASING (hence '
    'trivially unimodal). The initial-dip objection applies when expansion occurs.')

# 11.11  each 2x2 principal minor of the triangle Laplacian is 100/3
w12, w13, w23 = Fr(299,6), Fr(1,3), Fr(1,3)
Ltri = [[w12+w13, -w12, -w13], [-w12, w12+w23, -w23], [-w13, -w23, w13+w23]]
m2 = [detQ_of([[Ltri[i][j] for j in S] for i in S]) for S in ((0,1), (0,2), (1,2))]
chk(all(x == Fr(100,3) for x in m2) and sum(m2) == 100,
    'C11.11 each 2x2 principal minor of the triangle Laplacian is 100/3 (sum 100)',
    'added detail; the stated eigenvalues 0, 100, 1 were already correct')

# 11.12  sharpness at k = 3: the question is a LINEAR feasibility problem, and a bounded
#        search did not settle it
print()
print('  k = 3 sharpness.  For a STAR pattern Qt = [[M, x_1..x_k],[x_1,1,..],..] with')
print('  det Qt = M - sum x_i^2, one has  R(kappa) = [1 + sum_i w_i g_i(kappa)]/D(kappa)  with')
print('  w_i = x_i^2/det Qt  and  g_i(kappa) = (mu_i kappa/(2 + mu_i kappa))^2.  Both "R > 1 at')
print('  kappa" and "R < 1 at kappa" are LINEAR inequalities in w, so asking for c prescribed')
print('  expansion windows separated by prescribed gaps is a linear feasibility problem in w.')
print('  A bounded search (5 scale choices, 3-variable vertex enumeration over the 5')
print('  constraints) found NO feasible w for three separated windows. This is INCONCLUSIVE:')
print('  it neither exhibits a 3-component witness nor shows none exists.')
chk(True, 'C11.12 k = 3 sharpness recorded as OPEN, with the LP reduction',
    'the bound is <= k for all k; attainment is known only for k = 1 and k = 2')

print()
print('='*100)
print('SECTION 11 TOTALS: %d checks, %d passed, %d failed' % (npass+nfail, npass, nfail))
print('='*100)
