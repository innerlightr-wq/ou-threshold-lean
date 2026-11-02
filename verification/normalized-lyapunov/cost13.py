#!/usr/bin/env python3
"""SECTION 13  A NECESSARY cost bound for attaining the full ceiling c = k.

Theorem H says k correlated pairs give at most k expansion components.  Attaining k requires A to
realize all 2k permitted sign variations, which forces its last potentially positive coefficient
to be positive:  [kappa^{2k-1}] A > 0.  Since kappa*A = N - B*D*det Q with deg N <= 2k,

    [kappa^{2k}] N  >  det Q * [kappa^{2k}](D B),

and N = B det(C o Qt) with deg B = 2k gives [kappa^{2k}]N = [kappa^{2k}]B * rho_inf, where
rho_inf = det(C_inf o Qt)/det Qt.  Hence the necessary condition

    rho_inf  >  T(E,L) := [kappa^{2k}](D B) / [kappa^{2k}] B,

and by Hadamard rho_inf <= rho = prod Qt_ii/det Qt, so rho > T(E,L) is necessary too.
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
def dec(x, places=12):
    """exact decimal string for a Fraction (float printing is lossy at this magnitude)."""
    neg = x < 0
    if neg: x = -x
    whole = x.numerator // x.denominator
    frac = x - whole
    digits = ''
    for _ in range(places):
        frac *= 10
        d = frac.numerator // frac.denominator
        digits += str(d)
        frac -= d
    return ('-' if neg else '') + str(whole) + '.' + digits

npass = nfail = 0
def chk(ok, label, note=''):
    global npass, nfail
    npass, nfail = npass+bool(ok), nfail+(not ok)
    print(('PASS  ' if ok else 'FAIL  ')+label+('  '+note if note else ''))

print('='*104)
print('SECTION 13  NECESSARY COST BOUND FOR c = k COMPONENTS')
print('='*104)

def blocks_data(rates, etas):
    """k disjoint 2x2 blocks [[1,b],[b,1+b^2]] with eta_j = b_j^2, rates (0, a_j)."""
    k = len(rates); n = 2*k
    lam = []
    for a in rates: lam += [Fr(0), Fr(a)]
    Q = [[Fr(0)]*n for _ in range(n)]
    for j, e in enumerate(etas):
        Q[2*j][2*j] = Fr(1); Q[2*j][2*j+1] = Q[2*j+1][2*j] = Fr(1)  # placeholder, b set below
        Q[2*j+1][2*j+1] = 1 + Fr(e)
        # b^2 = eta since det = (1)(1+eta) - b^2 = 1  =>  b^2 = eta
        Q[2*j][2*j+1] = Q[2*j+1][2*j] = None
    return lam, Q
def build(rates, etas):
    """exact Qt; off-diagonals carry b = sqrt(eta), so we store eta and use it only squared."""
    k = len(rates); n = 2*k
    lam = []
    for a in rates: lam += [Fr(0), Fr(a)]
    E = [(2*j, 2*j+1) for j in range(k)]
    diag = []
    for e in etas: diag += [Fr(1), 1 + Fr(e)]
    return lam, E, diag, [Fr(e) for e in etas]

def Apoly(rates, etas):
    """kappa*A = N - B*D*detQ, computed exactly (only eta = b^2 is ever needed)."""
    lam, E, diag, et = build(rates, etas)
    n = len(lam)
    a = [pn([Fr(1), Fr(l)]) for l in lam]
    B = [Fr(1)]
    for (i, j) in E: B = pmul(B, pmul(padd(a[i], a[j]), padd(a[i], a[j])))
    D = [Fr(1)]
    for l in lam: D = pmul(D, [Fr(1), Fr(l)])
    detQ = Fr(1)
    for e in et: detQ *= (Fr(1)*(1+e) - e)          # = 1 per block
    # N = B * prod_j [ Qt_ii Qt_jj - c_j^2 b_j^2 ],  c_j^2 = 4 a_i a_j/(a_i+a_j)^2
    N = [Fr(1)]
    for jj, (i, j) in enumerate(E):
        s2 = pmul(padd(a[i], a[j]), padd(a[i], a[j]))
        dp = pmul([diag[i]*diag[j]], s2)
        cr = pmul([4*et[jj]], pmul(a[i], a[j]))
        N = pmul(N, padd(dp, [-x for x in cr]))
    numer = padd(N, [-x for x in pmul(B, pmul(D, [detQ]))])
    A, rem = pdivmod(numer, [Fr(0), Fr(1)])
    assert rem == [Fr(0)]
    return A, B, D, detQ, len(E)

def Tfloor_coeffs(rates):
    """T(E,L) = [kappa^{2k}](D B)/[kappa^{2k}]B, computed from the polynomials."""
    k = len(rates)
    lam = []
    for a in rates: lam += [Fr(0), Fr(a)]
    a = [pn([Fr(1), Fr(l)]) for l in lam]
    E = [(2*j, 2*j+1) for j in range(k)]
    B = [Fr(1)]
    for (i, j) in E: B = pmul(B, pmul(padd(a[i], a[j]), padd(a[i], a[j])))
    D = [Fr(1)]
    for l in lam: D = pmul(D, [Fr(1), Fr(l)])
    DB = pmul(D, B)
    return DB[2*k]/B[2*k]
def Tfloor_formula3(rates):
    a1, a2, a3 = [Fr(x) for x in rates]
    s = sum(x/y for x in (a1, a2, a3) for y in (a1, a2, a3) if x is not y)
    return 125 + 40*s + 4*a1*a2*a3*(1/a1**3 + 1/a2**3 + 1/a3**3)

RATES3 = (Fr(1000), Fr(1), Fr(1,10000))
# ---- 13.1  the closed formula for three blocks matches the coefficient ratio
T_coeff = Tfloor_coeffs(RATES3)
T_form = Tfloor_formula3(RATES3)
chk(T_coeff == T_form,
    'C13.1 T(E,L) = 125 + 40 sum_{i!=j} a_i/a_j + 4 a_1a_2a_3 sum_i a_i^-3  for three (0,a_j) blocks',
    'coefficient ratio = closed formula = %s' % T_coeff)
print('  T = %s' % T_coeff)
print('    = %s   (exact decimal; float printing loses digits at this magnitude)' % dec(T_coeff))
# other rate choices
bad = [r for r in ((Fr(5), Fr(2), Fr(1)), (Fr(100), Fr(3), Fr(1,7)), (Fr(1), Fr(1), Fr(1)))
       if Tfloor_coeffs(r) != Tfloor_formula3(r)]
chk(not bad, 'C13.1b the formula agrees at three further rate triples (incl. all rates equal)',
    'all-equal rates give T = 125 + 240 + 12 = 377')

# ---- 13.2  rho_inf = rho for disjoint (0,a) blocks, and Hadamard rho_inf <= rho in general
print()
ETAS = (Fr(9), Fr(3600), Fr(12250000))
rho = Fr(1)
for e in ETAS: rho *= (1+e)
chk(rho == Fr(441122536010),
    'C13.2 rho = prod (1 + eta_j) = (1+9)(1+3600)(1+3500^2) = 441122536010',
    'for Q_b the limiting channel kills every within-block correlation (c -> 0 when one rate is '
    '0 and the other grows), so rho_inf = rho exactly')
# check rho_inf = rho numerically: det(C o Qt)/det Qt -> rho
lam, E, diag, et = build(RATES3, ETAS)
def ratio_num(k):
    A, B, D, detQ, kk = Apoly(RATES3, ETAS)
    return pev(A, k)
def detCQ_over_detQ(k):
    a = [1 + Fr(k)*Fr(l) for l in lam]
    p = Fr(1)
    for jj, (i, j) in enumerate(E):
        c2 = 4*a[i]*a[j]/(a[i]+a[j])**2
        p *= (diag[i]*diag[j] - c2*et[jj])
    return p
vals = [detCQ_over_detQ(Fr(10)**m) for m in (6, 9, 12)]
chk(all(v < rho for v in vals) and vals[2] > rho*Fr(999,1000),
    'C13.2b det(C o Qt)/det Qt increases to rho as kappa -> infinity',
    'at kappa = 1e6, 1e9, 1e12: %s (rho = %s)'
    % (['%.6e' % float(v) for v in vals], rho))

# ---- 13.3  the witness clears the floor, and by how little
print()
chk(rho > T_coeff, 'C13.3 the k = 3 witness satisfies the necessary condition rho > T(E,L)',
    'rho = %s  >  T = %s   (ratio %.6f)' % (rho, dec(T_coeff, 6), float(rho/T_coeff)))
eta3_floor = T_coeff/((1+Fr(9))*(1+Fr(3600))) - 1
import math
b3_floor = math.sqrt(float(eta3_floor))
print('  holding b_1 = 3, b_2 = 60: eta_3 > %s, i.e. b_3 > %.6f' % (dec(eta3_floor, 4), b3_floor))
chk(abs(float(eta3_floor) - 11119144.7963) < 1 and abs(b3_floor - 3334.538168) < 1e-4,
    'C13.3b the forced floor is eta_3 > 11119144.796..., b_3 > 3334.538168...',
    'the witness uses b_3 = 3500, only %.2f%% above the floor' % (100*(3500/b3_floor - 1)))

# ---- 13.4  below the floor the sign count drops, so k components become impossible
print()
def signvars(A):
    sg = [1 if c > 0 else (-1 if c < 0 else 0) for c in A]
    nz = [s for s in sg if s != 0]
    return sum(1 for i in range(1, len(nz)) if nz[i] != nz[i-1]), sg
for e3, tag in ((Fr(12250000), 'b_3 = 3500 (above floor)'),
                (Fr(11000000), 'eta_3 = 11000000 (below floor)')):
    A, B, D, detQ, kk = Apoly(RATES3, (Fr(9), Fr(3600), e3))
    sv, sg = signvars(A)
    top = A[2*kk-1]
    print('  %-34s [k^{2k-1}]A = %-26s sign variations = %d  (%s)'
          % (tag, ('%+.6e' % float(top)), sv,
             ''.join('+' if s > 0 else ('-' if s < 0 else '0') for s in sg)))
A_lo, _, _, _, kk = Apoly(RATES3, (Fr(9), Fr(3600), Fr(11000000)))
sv_lo, _ = signvars(A_lo)
chk(A_lo[2*kk-1] < 0 and sv_lo == 4,
    'C13.4 at eta_3 = 11000000 the top free coefficient is NEGATIVE and only 4 sign variations '
    'remain', 'so at most 2 expansion components -- three are impossible below the floor')
# and the exclusion is real: count components there
ks = []
e = Fr(1,10**9)
while e < Fr(10)**9:
    ks.append(e); e *= Fr(12,10)
fl = [pev(A_lo, x) > 0 for x in ks]
comp = sum(1 for i in range(len(fl)) if fl[i] and (i == 0 or not fl[i-1]))
chk(comp <= 2, 'C13.4b scanning confirms at most two components below the floor',
    '%d found over %d couplings' % (comp, len(ks)))

# ---- 13.5  the bound is NOT optimal: one isolated pair gives eta > 4, not eta > 8
print()
T1 = Tfloor_coeffs((Fr(2),))     # single block, rates (0,2) -- the two-mode model
chk(T1 == 5, 'C13.5 for one isolated pair the bound gives rho > 5, i.e. eta > 4',
    'but the exact threshold from Theorem F is eta_crit = 8, so the coefficient bound is '
    'necessary and NOT optimal; its value here is that the k = 3 witness sits close to it')

# ---- 13.6  the halving control: what exactly was varied
print()
def eta_after_halving_offdiag(eta):
    """diagonal entries fixed, off-diagonal halved:  eta -> eta/(4 + 3 eta)."""
    return eta/(4 + 3*eta)
bad = []
for e in (Fr(9), Fr(3600), Fr(12250000)):
    # P = Qt_pp Qt_qq is fixed; b^2 = eta P/(1+eta); halve b
    P = (1 + e)          # for Q_b: Qt_pp Qt_qq = 1*(1+b^2) = 1 + eta
    b2 = e
    e_new = (b2/4)/(P - b2/4)
    if e_new != eta_after_halving_offdiag(e): bad.append(e)
chk(not bad and all(eta_after_halving_offdiag(e) < Fr(1,3) for e in (Fr(9), Fr(3600), Fr(12250000))),
    'C13.6 CLARIFICATION: halving the off-diagonals with the diagonal FIXED sends '
    'eta -> eta/(4+3eta) < 1/3',
    'a drastic drop. The section-12 control instead rescaled b and adjusted the diagonal to keep '
    'det Qt = 1, which sends eta -> t^2 eta (12250000 -> 3062500 at t = 1/2) -- still far below '
    'the floor 11119144.8, so the new bound EXPLAINS that control')

print()
print('='*104)
print('SECTION 13 TOTALS: %d checks, %d passed, %d failed' % (npass+nfail, npass, nfail))
print('='*104)
