#!/usr/bin/env python3
"""Rigorous two-sided certification of the three-mode threshold.

Expansion means  ratio(kappa) > 1  for some kappa > 0, where ratio = N(kappa)/D(kappa) in lowest
terms is an explicit element of Q(kappa) (threemode2.py).  Write

    g(kappa) := D(kappa) - N(kappa),        so   no expansion on (0,oo)  <=>  g >= 0 there.

The denominator D is a product of (a_i + a_j) factors, hence strictly positive for kappa >= 0.

CERTIFICATE USED FOR THE NEGATIVE SIDE.  g has rational coefficients.  If every coefficient of g
is >= 0 then g >= 0 on [0,oo) and no expansion occurs -- a proof, not a grid scan.  When some
coefficients are negative we fall back to a Bernstein certificate on the compact window supplied
by the no-expansion ceiling theorem: expansion forces det H_kappa < rho(Q,L), i.e.
(1+kappa)(1+3kappa) < rho, so kappa < kmax(r).  Map [0,kmax] -> [0,1] by kappa = kmax*t and expand
g in the Bernstein basis of degree m; all-nonnegative Bernstein coefficients certify g >= 0 there,
and the ceiling theorem covers kappa >= kmax.

POSITIVE SIDE.  A single exact rational (kappa, r) with ratio > 1 is already a proof.
"""
from fractions import Fraction as Fr

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
def pev(p, t): return sum((c * Fr(t) ** i for i, c in enumerate(p)), Fr(0))
class RF:
    __slots__ = ('n', 'd')
    def __init__(s, n, d=(Fr(1),)): s.n, s.d = pnorm(list(n)), pnorm(list(d))
    def __add__(s, o): return RF(padd(pmul(s.n, o.d), pmul(o.n, s.d)), pmul(s.d, o.d))
    def __sub__(s, o): return RF(padd(pmul(s.n, o.d), [-x for x in pmul(o.n, s.d)]), pmul(s.d, o.d))
    def __mul__(s, o): return RF(pmul(s.n, o.n), pmul(s.d, o.d))
def K(c): return RF((Fr(c),))
KAP = RF((Fr(0), Fr(1)))

def ratio_rf(q):
    q1, q2, q3 = map(Fr, q)
    detQ = q1 * q2 * q3
    Qt00 = (q1+q2+q3)/3; Qt11 = (q1+q3)/2; Qt22 = (q1+4*q2+q3)/6
    s01 = (q1-q3)**2/6; s02 = (q1-2*q2+q3)**2/18; s12 = (q1-q3)**2/12
    cyc = (q1-q3)**2*(q1-2*q2+q3)/36
    a = [K(1), K(1)+KAP, K(1)+KAP*K(3)]
    A01, A12, A02 = a[0]+a[1], a[1]+a[2], a[0]+a[2]
    T = [a[i]+a[i] for i in range(3)]
    detS = (RF((Qt00,), T[0].n)*RF((Qt11,), T[1].n)*RF((Qt22,), T[2].n)
            + K(2)*RF((cyc,), pmul(pmul(A01.n, A12.n), A02.n))
            - RF((Qt00,), T[0].n)*RF((s12,), pmul(A12.n, A12.n))
            - RF((Qt11,), T[1].n)*RF((s02,), pmul(A02.n, A02.n))
            - RF((Qt22,), T[2].n)*RF((s01,), pmul(A01.n, A01.n)))
    return detS*K(Fr(8)/detQ)

def gpoly(q):
    """g = D - N  with ratio = N/D;  D > 0 for kappa >= 0 by construction."""
    rr = ratio_rf(q)
    return padd(rr.d, [-x for x in rr.n]), rr.d

def bernstein_nonneg(p, kmax, m):
    """Bernstein coefficients of p(kmax*t) in degree m on t in [0,1], exactly."""
    from math import comb
    c = [pev(p, 0)]*0
    # coefficients of p(kmax*t)
    q = [p[i]*Fr(kmax)**i for i in range(len(p))]
    n = len(q)-1
    if m < n: m = n
    # elevate: b_k = sum_i q_i * C(k,i)/C(m,i)   (standard monomial -> Bernstein, degree m)
    b = []
    for k in range(m+1):
        s = Fr(0)
        for i in range(n+1):
            if i <= k: s += q[i]*Fr(comb(k, i), comb(m, i))
        b.append(s)
    return b

def kmax_of(q):
    q1, q2, q3 = map(Fr, q)
    rho = ((q1+q2+q3)/3)*((q1+q3)/2)*((q1+4*q2+q3)/6)/(q1*q2*q3)
    lo, hi = Fr(0), Fr(1)
    while (1+hi)*(1+3*hi) < rho: hi *= 2
    for _ in range(60):
        mid = (lo+hi)/2
        if (1+mid)*(1+3*mid) < rho: lo = mid
        else: hi = mid
    return hi, rho          # (1+hi)(1+3hi) >= rho, so expansion impossible for kappa >= hi

def shift(p, u, w):
    """coefficients of p(u + w*t) in t, exactly."""
    n = len(p)-1
    out = [Fr(0)]*(n+1)
    # Horner in t:  build iteratively
    acc = [Fr(0)]
    for c in reversed(p):
        # acc <- acc*(u + w t) + c
        new = [Fr(0)]*(len(acc)+1)
        for i, x in enumerate(acc):
            new[i] += x*Fr(u)
            new[i+1] += x*Fr(w)
        new[0] += c
        acc = new
    while len(acc) > 1 and acc[-1] == 0: acc = acc[:-1]
    return acc

def no_expansion_certificate(q, maxdepth=14, mdeg=None):
    """Proof that g >= 0 on [0,oo): monomial-sign test, else subdivided Bernstein on the
    compact ceiling window, with the ceiling theorem covering kappa >= kmax."""
    g, D = gpoly(q)
    if all(c >= 0 for c in g):
        return 'all-nonnegative monomial coefficients (valid on all of [0,oo))'
    kmax, rho = kmax_of(q)
    m = mdeg or len(g)+6
    boxes, done, depth = [(Fr(0), kmax)], 0, 0
    while boxes:
        depth += 1
        if depth > 200000: return None
        u, v = boxes.pop()
        b = bernstein_nonneg(shift(g, u, v-u), 1, m)
        if all(x >= 0 for x in b):
            done += 1; continue
        if v-u < kmax/Fr(2)**maxdepth: return None
        mid = (u+v)/2
        boxes.append((u, mid)); boxes.append((mid, v))
    return 'subdivided Bernstein (deg %d, %d boxes) on [0,%.6f]; ceiling theorem covers kappa >= %.6f' % (
        m, done, float(kmax), float(kmax))

def expansion_witness(q):
    rr = ratio_rf(q)
    for num in range(1, 2001):
        k = Fr(num, 100)
        if pev(rr.n, k) > pev(rr.d, k): return k, pev(rr.n, k)/pev(rr.d, k)
    return None

npass = nfail = 0
def chk(ok, label, note=''):
    global npass, nfail
    npass, nfail = npass+bool(ok), nfail+(not ok)
    print(('PASS  ' if ok else 'FAIL  ')+label+('  '+note if note else ''))

print('='*96)
print('SECTION 5b  TWO-SIDED CERTIFICATION OF THE THREE-MODE THRESHOLD')
print('='*96)
for qt, nm in (((1,1,'r'), 'Q = diag(1,1,r^2)  noise on an END node'),
               ((1,'r',1), 'Q = diag(1,r^2,1)  noise on the CENTRE node')):
    print('\n'+nm)
    lo, hi = Fr(1), Fr(60)
    for _ in range(40):
        mid = (lo+hi)/2
        q = tuple(mid**2 if x == 'r' else Fr(x) for x in qt)
        if expansion_witness(q) is not None: hi = mid
        else: lo = mid
    # POSITIVE SIDE: an exact rational witness just above the grid crossing is already a proof.
    rhi = Fr(int(hi*10**9)+1, 10**9)
    qhi = tuple(rhi**2 if x == 'r' else Fr(x) for x in qt)
    w = expansion_witness(qhi)
    # NEGATIVE SIDE: step back until the positivity certificate succeeds.  Near the critical r
    # the polynomial g has a near-double root, so the certified gap is wider than the grid gap;
    # that is a limitation of the certificate, not evidence about the intervening r values.
    cert = rlo = None
    for eps in (Fr(1,10**7), Fr(1,10**6), Fr(1,10**5), Fr(1,10**4), Fr(1,10**3), Fr(1,100)):
        rlo = Fr(int(lo*10**9), 10**9) - eps
        qlo = tuple(rlo**2 if x == 'r' else Fr(x) for x in qt)
        cert = no_expansion_certificate(qlo, maxdepth=22)
        if cert: break
    print('  r- = %s = %.9f   (PROVED no expansion)' % (rlo, float(rlo)))
    print('  r+ = %s = %.9f   (PROVED expansion)' % (rhi, float(rhi)))
    print('  certified two-sided bracket width = %.2e' % float(rhi-rlo))
    chk(cert is not None, 'PROVED no expansion at r = %.9f' % float(rlo), 'certificate: %s' % cert)
    chk(w is not None, 'PROVED expansion at r = %.9f' % float(rhi),
        'exact witness kappa = %s, ratio - 1 = %s' % (w[0], w[1]-1) if w else '')
    kmax, rho = kmax_of(qhi)
    print('  rho(Q,L) = %.6f   ceiling window kappa < %.6f' % (float(rho), float(kmax)))

print('\n  two-mode reference threshold (repository MainTheorem): r* = 3 + 2*sqrt(2) = %.9f' % (3+2*2**0.5))
print('='*96)
print('SECTION 5b TOTALS: %d checks, %d passed, %d failed' % (npass+nfail, npass, nfail))
print('='*96)
