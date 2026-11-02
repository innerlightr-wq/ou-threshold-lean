#!/usr/bin/env python3
"""SECTION 15  A necessary cost bound for EVERY c, on matching (disjoint-pair) patterns.

    T_c^match(E,L) = max{ 1 + 8 tr L/s_* ,  [k^{2c}](DB)/[k^{2c}]B },   s_* = max_{E}(lam_p+lam_q),

necessary for at least c expansion components.  Two ingredients remove the min over the band:
  (i)  COEFFICIENTWISE DOMINATION  N <= det Q * rho_inf * B  (every coefficient), for matching
       patterns, from the per-block identity  n_j = 4 + 4 s_j k + s_j^2 r_j k^2  <=  r_j (2+s_j k)^2;
  (ii) q_m = [k^m](DB)/[k^m]B is NONDECREASING in m, so the band's minimum sits at m = 2c.
The first term comes from G(k) <= 1 + (rho_inf - 1) u_*, D - 1 >= k tr L and min_x (2+x)^2/x = 8.
"""
from fractions import Fraction as Fr
from itertools import combinations

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
def pev(p, t): return sum((c*Fr(t)**i for i, c in enumerate(p)), Fr(0))
def coeff(p, m): return p[m] if m < len(p) else Fr(0)
def dec(x, places=12):
    neg = x < 0
    if neg: x = -x
    w = x.numerator // x.denominator; f = x - w; d = ''
    for _ in range(places):
        f *= 10; dd = f.numerator // f.denominator; d += str(dd); f -= dd
    return ('-' if neg else '') + str(w) + '.' + d

npass = nfail = 0
def chk(ok, label, note=''):
    global npass, nfail
    npass, nfail = npass+bool(ok), nfail+(not ok)
    print(('PASS  ' if ok else 'FAIL  ')+label+('  '+note if note else ''))

def model(pairs, extra=()):
    """pairs = [(lam_p, lam_q, Qpp, Qqq, Qpq)]; extra = uncorrelated eigenvalues (diag noise 1)."""
    lam, blocks = [], []
    for (lp, lq, qp, qq, qpq) in pairs:
        lam += [Fr(lp), Fr(lq)]
        blocks.append((Fr(lp), Fr(lq), Fr(qp), Fr(qq), Fr(qpq)))
    lam += [Fr(x) for x in extra]
    return lam, blocks

def pieces(pairs, extra=()):
    lam, blocks = model(pairs, extra)
    av = [pn([Fr(1), l]) for l in lam]
    B = [Fr(1)]
    for j in range(len(blocks)):
        i0, i1 = 2*j, 2*j+1
        B = pmul(B, pmul(padd(av[i0], av[i1]), padd(av[i0], av[i1])))
    D = [Fr(1)]
    for l in lam: D = pmul(D, [Fr(1), l])
    detQ = Fr(1)
    for (lp, lq, qp, qq, qpq) in blocks: detQ *= (qp*qq - qpq**2)
    # N = B det(C o Qt) = detQ * prod n_j     (uncorrelated modes contribute Qt_ii, here 1)
    N = [detQ]
    nlist, rlist = [], []
    for j, (lp, lq, qp, qq, qpq) in enumerate(blocks):
        i0, i1 = 2*j, 2*j+1
        s = lp + lq
        dj = qp*qq - qpq**2
        eta = qpq**2/dj
        r_inf = (1 + eta) - (4*lp*lq*eta/s**2 if s != 0 else Fr(0))
        n_j = pn([Fr(4), 4*s, s**2*r_inf])
        # verify n_j against the direct expression (a_p+a_q)^2 (QppQqq)/dj - 4 a_p a_q eta
        direct = padd(pmul([qp*qq/dj], pmul(padd(av[i0], av[i1]), padd(av[i0], av[i1]))),
                      [-x for x in pmul([4*eta], pmul(av[i0], av[i1]))])
        assert pn(direct) == n_j, (pn(direct), n_j)
        N = pmul(N, n_j)
        nlist.append(n_j); rlist.append(r_inf)
    rho_inf = Fr(1)
    for r in rlist: rho_inf *= r
    trL = sum(lam)
    s_star = max(blocks[j][0] + blocks[j][1] for j in range(len(blocks)))
    return lam, B, D, detQ, N, nlist, rlist, rho_inf, trL, s_star

print('='*106)
print('SECTION 15  NECESSARY COST FOR EVERY c  (matching patterns)')
print('='*106)

INST = [
    [(0, 1000, 1, 1+9, 3), (0, 1, 1, 1+3600, 60), (0, Fr(1,10**4), 1, 1+3500**2, 3500)],
    [(0, 2, 5, 5, 4)],
    [(0, 1, 4, 9, 3), (0, 7, 2, 11, 4)],
    [(1, 4, 6, 7, 2), (2, 9, 5, 8, 3)],                       # both rates nonzero
    [(0, 3, 3, 10, 5), (1, 6, 4, 4, 1), (2, 2, 9, 9, 4)],      # incl. equal rates in a pair
    [(0, 5, 2, 7, 3)],
]
EXTRA = [(), (), (Fr(3),), (Fr(1,2), Fr(8)), (), (Fr(4), Fr(4), Fr(1,5))]

# ---- 15.1  per-block identity and coefficientwise domination
print()
bad_dom = []; bad_r = []; cnt = 0
for pairs, extra in zip(INST, EXTRA):
    lam, B, D, detQ, N, nlist, rlist, rho_inf, trL, s_star = pieces(pairs, extra)
    for n_j, r in zip(nlist, rlist):
        if r < 1: bad_r.append(r)
        ub = pmul([r], pmul(pn([Fr(2), n_j[1]/Fr(4) if False else Fr(0)]), [Fr(1)]))  # unused
    # N <= detQ * rho_inf * B coefficientwise
    RHS = pmul([detQ*rho_inf], B)
    for m in range(max(len(N), len(RHS))):
        cnt += 1
        if coeff(N, m) > coeff(RHS, m) + Fr(0): bad_dom.append((m, coeff(N, m), coeff(RHS, m)))
chk(not bad_r, 'C15.1a every block has limiting gain r_inf >= 1 (Oppenheim per block)',
    '%d blocks' % sum(len(p) for p in INST))
chk(not bad_dom, 'C15.1 COEFFICIENTWISE DOMINATION  N <= det Q * rho_inf * B',
    '%d coefficient comparisons across 6 matching instances (nonzero rates on both sides of a '
    'pair, equal rates within a pair, and extra uncorrelated damped modes all included); the '
    'per-block identity n_j = 4 + 4 s k + s^2 r_inf k^2 was asserted inside `pieces`' % cnt)

# ---- 15.2  q_m is nondecreasing
print()
bad_q = []; tot = 0
for pairs, extra in zip(INST, EXTRA):
    lam, B, D, detQ, N, nlist, rlist, rho_inf, trL, s_star = pieces(pairs, extra)
    DB = pmul(D, B); k = len(pairs)
    qs = [coeff(DB, m)/coeff(B, m) for m in range(2*k+1)]
    for m in range(1, len(qs)):
        tot += 1
        if qs[m] < qs[m-1]: bad_q.append((m, float(qs[m-1]), float(qs[m])))
chk(not bad_q, 'C15.2 q_m = [k^m](DB)/[k^m]B is NONDECREASING in m for 0 <= m <= 2k',
    '%d comparisons; so the band minimum sits at m = 2c and the disjunction collapses' % tot)
# extra stress: random-ish rate choices
bad_q2 = []
for rates in ((Fr(1), Fr(2), Fr(3)), (Fr(1,100), Fr(5), Fr(900)), (Fr(7), Fr(7), Fr(7)),
              (Fr(1), Fr(10**6), Fr(10**-6)), (Fr(3), Fr(1,3), Fr(11))):
    pairs = [(0, r, 1, 2, 1) for r in rates]
    lam, B, D, detQ, N, nlist, rlist, rho_inf, trL, s_star = pieces(pairs)
    DB = pmul(D, B)
    qs = [coeff(DB, m)/coeff(B, m) for m in range(7)]
    if any(qs[m] < qs[m-1] for m in range(1, 7)): bad_q2.append(rates)
chk(not bad_q2, 'C15.2b monotonicity holds at five further rate triples', 'incl. equal and extreme rates')

# ---- 15.3  the interpolating bound, and the endpoint
print()
def Tc_match(pairs, extra, c):
    lam, B, D, detQ, N, nlist, rlist, rho_inf, trL, s_star = pieces(pairs, extra)
    DB = pmul(D, B)
    return max(1 + 8*trL/s_star, coeff(DB, 2*c)/coeff(B, 2*c))
# single isolated pair (0,a): terms are 9 and 5, so the bound is rho_inf > 9, i.e. eta > 8
one = [(0, Fr(2), 5, 5, 4)]
lam, B, D, detQ, N, nlist, rlist, rho_inf, trL, s_star = pieces(one)
DB = pmul(D, B)
chk(1 + 8*trL/s_star == 9 and coeff(DB, 2)/coeff(B, 2) == 5 and Tc_match(one, (), 1) == 9,
    'C15.3 ENDPOINT: for one isolated pair the two terms are 9 and 5, so the bound is rho_inf > 9',
    'i.e. eta > 8 -- the EXACT single-pair threshold of Theorem F is retained, where Theorem I '
    'alone gave only eta > 4')
bad = []
for a in (Fr(1), Fr(5), Fr(1,3), Fr(1000)):
    p = [(0, a, 1, 2, 1)]
    l2, B2, D2, dQ2, N2, nl2, rl2, ri2, tr2, ss2 = pieces(p)
    if 1 + 8*tr2/ss2 != 9: bad.append(a)
chk(not bad, 'C15.3b the single-pair term is 9 for every rate, as it must be', 'scale invariance')

# ---- 15.4  the three-block spectrum table
print()
P3 = INST[0]
floors = [Tc_match(P3, (), c) for c in (1, 2, 3)]
print('  rate pairs (0,1000), (0,1), (0,1e-4):')
for c, f in zip((1, 2, 3), floors):
    print('    at least %d component(s):  rho_inf floor = %s' % (c, dec(f, 6)))
chk(dec(floors[0], 7) == '9.0080008' and dec(floors[2], 6) == '400400440125.444004'
    and floors[0] < floors[1] < floors[2],
    'C15.4 the three reported floors reproduce exactly and increase with c',
    'c = 2 floor = %s' % dec(floors[1], 6))
lam, B, D, detQ, N, nl, rl, rho_inf3, trL3, ss3 = pieces(P3)
chk(rho_inf3 == Fr(441122536010) and rho_inf3 > floors[2],
    'C15.4b the k = 3 witness has rho_inf = 441122536010, clearing all three floors', '')
chk(Tc_match(P3, (), 3) == Fr(1001001100313610010001, 2500000000),
    "C15.4c at c = k = 3 the bound reduces to Theorem I's coefficient ratio", '')

# ---- 15.5  the enlarged parameter boxes
print()
def g(z): z = Fr(z); return (z/(2+z))**2
A0 = [Fr(1000), Fr(1), Fr(1,10**4), Fr(1,10**8), Fr(1,10**12)]
B0 = [Fr(3), Fr(60), Fr(3500), Fr(45000), Fr(2000000)]
RA, RB = Fr(1,600), Fr(1,240)
def envelope(k, kap, upper):
    p = Fr(1)
    for j in range(k):
        alo, ahi = (1-RA)*A0[j], (1+RA)*A0[j]
        blo, bhi = (1-RB)*B0[j], (1+RB)*B0[j]
        if upper: p *= (1 + bhi**2*g(ahi*Fr(kap)))/(1 + alo*Fr(kap))
        else:     p *= (1 + blo**2*g(alo*Fr(kap)))/(1 + ahi*Fr(kap))
    return p
KS = [(Fr(1,10**5), '<'), (Fr(1,500), '>'), (Fr(1,20), '<'), (Fr(1), '>'), (Fr(10), '<'),
      (Fr(100), '>'), (Fr(1000), '<'), (Fr(10**4), '>'), (Fr(10**6), '<'), (Fr(10**7), '>'),
      (Fr(10**9), '<')]
print('  enlarged boxes: rates +-1/600 (~0.1667%%), b_j +-1/240 (~0.4167%%)')
bad5 = []; bad4 = []; tight = None
for idx, (kap, sense) in enumerate(KS):
    u5, l5 = envelope(5, kap, True), envelope(5, kap, False)
    ok5 = (u5 < 1) if sense == '<' else (l5 > 1)
    if not ok5: bad5.append(kap)
    if sense == '>' and (tight is None or l5 < tight[0]): tight = (l5, kap)
    if idx < 9:
        u4, l4 = envelope(4, kap, True), envelope(4, kap, False)
        if not ((u4 < 1) if sense == '<' else (l4 > 1)): bad4.append(kap)
chk(not bad5 and not bad4,
    'C15.5 CORRECTION: both families still pass every envelope comparison with radii enlarged 5/3x',
    'tightest expansion lower bound %s at kappa = %s' % (dec(tight[0], 8), tight[1]))
chk(abs(float(tight[0]) - 1.00124634) < 1e-7 and tight[1] == Fr(100),
    'C15.5b the tightest bound is ~1.00124634 at kappa = 100, as reported',
    'my earlier reading -- that being within 1e-3 of the PRINTED thresholds meant the radii were '
    'near-maximal -- was wrong: those thresholds were rounded presentation values, and the real '
    'boundary is R = 1')

print()
print('='*106)
print('SECTION 15 TOTALS: %d checks, %d passed, %d failed' % (npass+nfail, npass, nfail))
print('='*106)
