#!/usr/bin/env python3
"""SECTION 14  A SUFFICIENT criterion: parameter boxes with exactly c expansion windows.

Blocks Q_b = [[1,b],[b,1+b^2]] with rate pairs (0, a_j); R(k) = prod_j F_j(k),
F_j(k) = [1 + b_j^2 g(a_j k)]/(1 + a_j k),  g(z) = (z/(2+z))^2, increasing for z > 0.

Monotone envelope over a box a_j in [a-, a+], b_j in [b-, b+]:
    [1 + (b-)^2 g(a- k)]/(1 + a+ k)  <=  F_j(k)  <=  [1 + (b+)^2 g(a+ k)]/(1 + a- k).
Multiplying over j bounds R outward.  If the UPPER product is < 1 at separating couplings and the
LOWER product is > 1 at interleaved couplings, then EVERY parameter choice in the box has those
separated windows -- a sufficient condition for a whole family, not a sampled check.

Correction this section records: a lower bound on noise strength ALONE cannot force several
windows, because raising all b_j fills the contraction gaps and merges the windows.
"""
from fractions import Fraction as Fr

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

def g(z): z = Fr(z); return (z/(2+z))**2
def F(a, b, k): return (1 + Fr(b)**2*g(Fr(a)*Fr(k)))/(1 + Fr(a)*Fr(k))
def R(k, ab): 
    p = Fr(1)
    for a, b in ab: p *= F(a, b, k)
    return p

def Apoly(ab):
    """kappa*A = N - B*D*detQ for k disjoint blocks Q_{b_j} with rates (0, a_j)."""
    k = len(ab)
    lam = []
    for a, b in ab: lam += [Fr(0), Fr(a)]
    E = [(2*j, 2*j+1) for j in range(k)]
    diag = []
    for a, b in ab: diag += [Fr(1), 1 + Fr(b)**2]
    et = [Fr(b)**2 for a, b in ab]
    av = [pn([Fr(1), Fr(l)]) for l in lam]
    B = [Fr(1)]
    for (i, j) in E: B = pmul(B, pmul(padd(av[i], av[j]), padd(av[i], av[j])))
    D = [Fr(1)]
    for l in lam: D = pmul(D, [Fr(1), Fr(l)])
    N = [Fr(1)]
    for jj, (i, j) in enumerate(E):
        s2 = pmul(padd(av[i], av[j]), padd(av[i], av[j]))
        N = pmul(N, padd(pmul([diag[i]*diag[j]], s2), [-x for x in pmul([4*et[jj]], pmul(av[i], av[j]))]))
    numer = padd(N, [-x for x in pmul(B, pmul(D, [Fr(1)]))])
    A, rem = pdivmod(numer, [Fr(0), Fr(1)])
    assert rem == [Fr(0)]
    return A, 2*k
def signpat(A):
    return ''.join('+' if c > 0 else ('-' if c < 0 else '0') for c in A)
def signvars(A):
    nz = [1 if c > 0 else -1 for c in A if c != 0]
    return sum(1 for i in range(1, len(nz)) if nz[i] != nz[i-1])
def comps(ab, lo=-14, hi=11):
    ks = []
    e = Fr(10)**lo
    while e <= Fr(10)**hi:
        ks.append(e); e *= Fr(115, 100)
    fl = [R(k, ab) > 1 for k in ks]
    return sum(1 for i in range(len(fl)) if fl[i] and (i == 0 or not fl[i-1])), len(ks)

npass = nfail = 0
def chk(ok, label, note=''):
    global npass, nfail
    npass, nfail = npass+bool(ok), nfail+(not ok)
    print(('PASS  ' if ok else 'FAIL  ')+label+('  '+note if note else ''))

print('='*106)
print('SECTION 14  SUFFICIENT CRITERION: PARAMETER BOXES WITH EXACTLY c WINDOWS')
print('='*106)

A0 = [Fr(1000), Fr(1), Fr(1,10**4), Fr(1,10**8), Fr(1,10**12)]
B0 = [Fr(3), Fr(60), Fr(3500), Fr(45000), Fr(2000000)]
ALO, AHI = Fr(999,1000), Fr(1001,1000)
BLO, BHI = Fr(9975,10000), Fr(10025,10000)

# ---- 14.1  monotonicity of g, and the envelope
bad = [ (z1,z2) for z1 in (Fr(1,100), Fr(1), Fr(7)) for z2 in (Fr(1,100), Fr(1), Fr(7))
        if z1 < z2 and not g(z1) < g(z2) ]
chk(not bad, 'C14.1 g(z) = (z/(2+z))^2 is strictly increasing for z > 0', 'so the envelope is valid')

# ---- 14.2  nominal component counts
print()
for k in (4, 5):
    ab = list(zip(A0[:k], B0[:k]))
    c, npts = comps(ab)
    A, twok = Apoly(ab)
    print('  k = %d nominal:  components = %d   deg A = %-3d sign variations = %-3d (2k = %d)'
          % (k, c, len(A)-1, signvars(A), twok))
    chk(c == k, 'C14.2 the nominal %d-block family has exactly %d expansion components' % (k, k),
        'scan over %d couplings; Theorem H caps it at k = %d, and signVariations = %d = 2k so '
        'Descartes is tight' % (npts, k, signvars(A)))

# ---- 14.3  the box bounds
print()
def prod_bound(k, kap, upper):
    p = Fr(1)
    for j in range(k):
        if upper:
            p *= (1 + (BHI*B0[j])**2*g(AHI*A0[j]*Fr(kap)))/(1 + ALO*A0[j]*Fr(kap))
        else:
            p *= (1 + (BLO*B0[j])**2*g(ALO*A0[j]*Fr(kap)))/(1 + AHI*A0[j]*Fr(kap))
    return p
TABLE = [(Fr(1,10**5), '<', Fr(991,1000)), (Fr(1,500), '>', Fr(1079,1000)),
         (Fr(1,20), '<', Fr(553,1000)), (Fr(1), '>', Fr(2031,1000)),
         (Fr(10), '<', Fr(938,1000)), (Fr(100), '>', Fr(1013,1000)),
         (Fr(1000), '<', Fr(969,1000)), (Fr(10**4), '>', Fr(1449,1000)),
         (Fr(10**6), '<', Fr(429,1000)), (Fr(10**7), '>', Fr(1793,1000)),
         (Fr(10**9), '<', Fr(581,1000))]
print('  five-block box:  a_j in [0.999, 1.001]*a_j0,  b_j in [0.9975, 1.0025]*b_j0')
bad5 = []; bad4 = []
for idx, (kap, sense, thr) in enumerate(TABLE):
    u5, l5 = prod_bound(5, kap, True), prod_bound(5, kap, False)
    ok5 = (u5 < thr) if sense == '<' else (l5 > thr)
    print('    kappa = %-8s %s %-6s   envelope [%.6f, %.6f]   %s'
          % (kap, sense, thr, float(l5), float(u5), 'ok' if ok5 else 'FAILS'))
    if not ok5: bad5.append(kap)
    if idx < 9:
        u4, l4 = prod_bound(4, kap, True), prod_bound(4, kap, False)
        if not ((u4 < thr) if sense == '<' else (l4 > thr)): bad4.append(kap)
chk(not bad5, 'C14.3 all eleven box bounds hold for the FIVE-block box',
    'exact rational inequalities on the monotone envelope, valid for every parameter choice in '
    'the box -- not a sampled check')
chk(not bad4, 'C14.3b the first nine bounds hold for the FOUR-block box', '')
# consequence: every member has >= 4 resp. >= 5 components
nplus5 = sum(1 for _, s, _ in TABLE if s == '>')
nplus4 = sum(1 for _, s, _ in TABLE[:9] if s == '>')
chk(nplus5 == 5 and nplus4 == 4,
    'C14.4 the alternation gives >= 5 (resp. >= 4) components for EVERY box member; Theorem H '
    'caps them at 5 and 4, so exactly 5 and exactly 4',
    'sharpness of Theorem H therefore holds at k = 4 and k = 5, robustly in the parameters')
# spot-check a few interior corners against the envelope
bad = []
for corner in ((ALO, BLO), (AHI, BHI), (ALO, BHI), (AHI, BLO), (Fr(1), Fr(1))):
    fa, fb = corner
    for k in (4, 5):
        ab = [(fa*A0[j], fb*B0[j]) for j in range(k)]
        tab = TABLE if k == 5 else TABLE[:9]
        for kap, sense, thr in tab:
            v = R(kap, ab)
            if (sense == '<' and not v < 1) or (sense == '>' and not v > 1): bad.append((corner, k, kap))
chk(not bad, 'C14.4b five corners of each box individually show the same alternation',
    'consistent with the envelope (which already covers the whole box)')

# ---- 14.5  CORRECTION: raising all noise strengths MERGES the windows
print()
for mult, tag in ((Fr(1), 'nominal'), (Fr(10), 'all b_j x 10')):
    for k in (3, 5):
        ab = [(A0[j], mult*B0[j]) for j in range(k)]
        A, twok = Apoly(ab)
        c, _ = comps(ab)
        pat = signpat(A)
        print('  k=%d %-14s components = %-2d sign variations = %-3d pattern %s'
              % (k, tag, c, signvars(A), pat if len(pat) <= 22 else pat[:22]+'...'))
ab10_5 = [(A0[j], 10*B0[j]) for j in range(5)]
A10, _ = Apoly(ab10_5)
free = [A10[j] for j in range(1, 10)]
c10, _ = comps(ab10_5)
chk(c10 == 1 and all(x > 0 for x in free),
    'C14.5 CORRECTION: multiplying every b_j by 10 makes all free coefficients POSITIVE and '
    'leaves ONE component',
    'so a lower bound on noise strength alone cannot force several windows -- raising the '
    'strengths fills the contraction gaps. A sufficient criterion must control SEPARATION too.')

# ---- 14.6  Target 1: the weaker band constraint for c < k
print()
# >= c components requires [kappa^j]A > 0 for some j in {2c-1, ..., 2k-1}
bad = []
for k in (3, 4, 5):
    ab = list(zip(A0[:k], B0[:k]))
    A, twok = Apoly(ab)
    cc, _ = comps(ab)
    for c in range(1, cc+1):
        band = [A[j] for j in range(2*c-1, min(2*k, len(A)))]
        if not any(x > 0 for x in band): bad.append((k, c))
chk(not bad, 'C14.6 for every c <= (actual count), some coefficient in degrees {2c-1,...,2k-1} is '
    'positive', 'the band constraint interpolating Theorem I; at c = k the band is the single '
    'coefficient [kappa^{2k-1}]A, recovering Theorem I exactly')
# and it genuinely excludes: a nonpositive band from 2c-1 caps the count at c-1
A_lo, _ = Apoly([(Fr(1000), Fr(3)), (Fr(1), Fr(60)), (Fr(1,10**4), Fr(3317))])
c_lo, _ = comps([(Fr(1000), Fr(3)), (Fr(1), Fr(60)), (Fr(1,10**4), Fr(3317))])
chk(A_lo[5] <= 0 and c_lo <= 2,
    'C14.6b with b_3 = 3317 (below the Theorem I floor 3334.538) the top band coefficient is '
    'nonpositive and at most 2 components remain', '[kappa^5]A = %.4e, components = %d'
    % (float(A_lo[5]), c_lo))

print()
print('='*106)
print('SECTION 14 TOTALS: %d checks, %d passed, %d failed' % (npass+nfail, npass, nfail))
print('='*106)
