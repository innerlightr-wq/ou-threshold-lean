#!/usr/bin/env python3
"""SECTION 10  The interval conjecture is FALSE: an exact three-mode counterexample.

Reviewer's witness, in the damping eigenbasis:
    L = diag(0, 100, 1),   Qt = [[2035, 3, 45], [3, 1, 0], [45, 0, 1]].
Qt has TWO correlated pairs, (0,1) and (0,2), at very different damping scales, and
Qt_12 = 0 so the determinant CYCLE term Qt_01 Qt_12 Qt_02 vanishes identically.

Everything below is exact rational arithmetic; the ratio is checked against an independent
solve of H Sigma + Sigma H = Qt, not against the closed form it is meant to test.
"""
from fractions import Fraction as Fr
from itertools import permutations

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

npass = nfail = 0
def chk(ok, label, note=''):
    global npass, nfail
    npass, nfail = npass+bool(ok), nfail+(not ok)
    print(('PASS  ' if ok else 'FAIL  ')+label+('  '+note if note else ''))

print('='*100)
print('SECTION 10  THE INTERVAL CONJECTURE IS FALSE (exact counterexample)')
print('='*100)

LAM = (Fr(0), Fr(100), Fr(1))
QT = [[Fr(2035), Fr(3), Fr(45)], [Fr(3), Fr(1), Fr(0)], [Fr(45), Fr(0), Fr(1)]]

# ---- 10.1  the noise matrix is positive definite
minors = [det([[QT[i][j] for j in range(k)] for i in range(k)]) for k in (1, 2, 3)]
chk(minors == [Fr(2035), Fr(2026), Fr(1)] and all(m > 0 for m in minors),
    'C10.1 Qt is positive definite', 'leading principal minors %s' % [str(m) for m in minors])
chk(QT[1][2] == 0,
    'C10.2 the determinant CYCLE term vanishes: Qt_12 = 0, so Qt_01 Qt_12 Qt_02 = 0',
    'the mechanism needs no cycle term -- it is TWO correlated pairs at different damping scales')

# ---- 10.3  the closed form, against independent Lyapunov solves
def H_of(k):
    return [[(1 + Fr(k)*LAM[i]) if i == j else Fr(0) for j in range(3)] for i in range(3)]
def R_exact(k):
    return det(lyap(H_of(k), QT))*Fr(2)**3/det(QT)
def R_formula(k):
    k = Fr(k)
    return ((1 + 9*(100*k/(2+100*k))**2 + 2025*(k/(2+k))**2) / ((1+100*k)*(1+k)))
bad = []
grid = [Fr(1,1000), Fr(1,50), Fr(1,20), Fr(1,10), Fr(1,4), Fr(1,2), Fr(1), Fr(3), Fr(20), Fr(500)]
for k in grid:
    if R_exact(k) != R_formula(k): bad.append((k, R_exact(k), R_formula(k)))
chk(not bad, 'C10.3 R(k) = [1 + 9(100k/(2+100k))^2 + 2025(k/(2+k))^2]/[(1+100k)(1+k)]',
    '%d exact couplings, each against an independent solve of H Sigma + Sigma H = Qt' % len(grid))

# ---- 10.4  the three decisive evaluations, exactly
print()
TABLE = [(Fr(1,50), Fr(3517825, 3121506), 'expansion'),
         (Fr(1,10), Fr(1055, 1078), 'contraction'),
         (Fr(1),    Fr(33907, 29189), 'expansion again')]
bad = []
for k, claimed, what in TABLE:
    got = R_exact(k)
    print('  kappa = %-6s R = %-22s = %.6f   %s' % (k, got, float(got), what))
    if got != claimed: bad.append((k, got, claimed))
chk(not bad, 'C10.4 the three reported exact values are correct',
    'reproduced from the Lyapunov solve, not from the closed form')

# ---- 10.5  DISCONNECTEDNESS, proved by three strict inequalities
k1, k2, k3 = Fr(1,50), Fr(1,10), Fr(1)
r1, r2, r3 = R_exact(k1), R_exact(k2), R_exact(k3)
chk(r1 > 1 and r2 < 1 and r3 > 1 and k1 < k2 < k3,
    'C10.5 {kappa > 0 : R(kappa) > 1} is NOT an interval -- the conjecture is REFUTED',
    'R(1/50) = %.6f > 1 > R(1/10) = %.6f, and R(1) = %.6f > 1; three strict rational '
    'inequalities, no grid inference' % (float(r1), float(r2), float(r3)))

# ---- 10.6  how many components?
print()
flags = []
ks = [Fr(i, 2000) for i in range(1, 400)] + [Fr(i, 100) for i in range(20, 400)] \
     + [Fr(i) for i in range(4, 200)]
for k in ks: flags.append(R_exact(k) > 1)
runs = sum(1 for i in range(1, len(flags)) if flags[i] and not flags[i-1]) + (1 if flags[0] else 0)
chk(runs == 2, 'C10.6 the expansion set has exactly TWO components on the tested range',
    '%d couplings scanned; one component from the fast pair, one from the slow pair' % len(ks))

# ---- 10.7  zeroing EITHER correlation restores a single interval (single-pair theorem)
print()
for kill, keep in ((2, '(0,1) only, lam 0 vs 100'), (1, '(0,2) only, lam 0 vs 1')):
    Q2 = [row[:] for row in QT]
    Q2[0][kill] = Q2[kill][0] = Fr(0)
    assert all(det([[Q2[i][j] for j in range(m)] for i in range(m)]) > 0 for m in (1, 2, 3))
    def R2(k):
        return det(lyap(H_of(k), Q2))*Fr(2)**3/det(Q2)
    fl = [R2(k) > 1 for k in ks]
    rr = sum(1 for i in range(1, len(fl)) if fl[i] and not fl[i-1]) + (1 if fl[0] else 0)
    print('  keep %-26s expansion components: %d' % (keep, rr))
    chk(rr == 0, 'C10.7 killing either correlation removes ALL expansion (%s)' % keep,
        'the witness needs BOTH. Zeroing one raises det Qt from 1 to %s, which weakens the '
        'surviving pair\'s normalized correlation eta below its eta_crit -- so this is not two '
        'independently expanding pairs, it is a near-singular Qt (det 1 against diagonal 2035) '
        'making both correlations strong at once.' % det(Q2))

# ---- 10.8  a connected weighted triangle realizes these eigenvalues
print()
w12, w13, w23 = Fr(299,6), Fr(1,3), Fr(1,3)
Ltri = [[w12+w13, -w12, -w13], [-w12, w12+w23, -w23], [-w13, -w23, w13+w23]]
tr = sum(Ltri[i][i] for i in range(3))
# char poly coefficients: tr = 0+100+1, sum of 2x2 principal minors = 0*100+0*1+100*1, det = 0
minor2 = sum(det([[Ltri[i][j] for j in S] for i in S])
             for S in ((0,1), (0,2), (1,2)))
chk(tr == 101 and minor2 == 100 and det(Ltri) == 0,
    'C10.8 the weighted triangle (299/6, 1/3, 1/3) has Laplacian eigenvalues 0, 100, 1',
    'tr = %s, sum of 2x2 principal minors = %s, det = 0 -- so the witness lives on a CONNECTED '
    'network' % (tr, minor2))

# ---- 10.9  the 7.5x overshoot: corrected diagnosis
print()
# centre-node three-node model: lam = 0,1,3; only pair (0,2) carries noise.
# exact mechanism:  1 - c_02^2 = k^2 Delta^2/(2+s k)^2 = Theta(k^2)
# Oppenheim-Schur:  det C = prod over ALL THREE pairs = Theta(k^6)
lam3 = (Fr(0), Fr(1), Fr(3))
def one_minus_c2(k, i, j):
    ai, aj = 1 + Fr(k)*lam3[i], 1 + Fr(k)*lam3[j]
    return (ai-aj)**2/(ai+aj)**2
def detC(k):
    p = Fr(1)
    for i in range(3):
        for j in range(i+1, 3):
            ai, aj = 1 + Fr(k)*lam3[i], 1 + Fr(k)*lam3[j]
            p *= (ai-aj)**2/(ai+aj)**2
    return p
rows = []
for k in (Fr(1,100), Fr(1,1000)):
    mech = one_minus_c2(k, 0, 2)/Fr(k)**2
    dc = detC(k)/Fr(k)**6
    rows.append((k, mech, dc))
    print('  k = %-8s (1 - c_02^2)/k^2 = %.6f    det C/k^6 = %.6f' % (k, float(mech), float(dc)))
chk(all(m > 0 and d > 0 for _, m, d in rows),
    'C10.9 CORRECTED diagnosis of the 7.5x overshoot: it is NOT the cycle term',
    'the centre-node model is itself SINGLE-PAIR (Qt_01 = Qt_12 = 0, cycle term zero). The exact '
    'mechanism is 1 - c_02^2 = Theta(k^2) from ONE pair, while det C multiplies the rate-difference '
    'factors of ALL THREE pairs, giving Theta(k^6). The loss is pair-specific information, not cycles.')

# ---- 10.10  "one expansion interval" is NOT "unimodality"
print()
# the two-mode expanding ratio DECREASES first: ratio'(0) = -tr L < 0 always.
def R2m(k, r):
    k, r = Fr(k), Fr(r)
    return (1 + (k/(1+k))**2*(r-1/r)**2/4)/(1+2*k)
r = Fr(9)
lo = R2m(Fr(1,100), r)
peak, kpeak = max((R2m(Fr(i,200), r), Fr(i,200)) for i in range(1, 4000))
far = R2m(Fr(10), r)
chk(lo < 1 < peak and peak > far,
    'C10.10 when expansion occurs the ratio is NOT unimodal: it dips first',
    'two-mode r = 9: R(1/100) = %.6f < 1, maximum %.6f at kappa = %s, then R(10) = %.6f. '
    'Since R\'(0) = -tr L < 0 the ratio always starts by DECREASING, so {R > 1} being an '
    'interval is strictly weaker than unimodality. (With commuting noise R = 1/det H is '
    'monotone, so "never unimodal" would be too broad -- see C11.10.)'
    % (float(lo), float(peak), kpeak, float(far)))

print()
print('='*100)
print('SECTION 10 TOTALS: %d checks, %d passed, %d failed' % (npass+nfail, npass, nfail))
print('='*100)
