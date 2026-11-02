#!/usr/bin/env python3
"""SECTION 8  Reviewer corrections and the Oppenheim-Schur refinement.  Exact arithmetic."""
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
def ratio_of(H, Q): return det(lyap(H, Q))*Fr(2)**len(H)/det(Q)
def diag(q): return [[Fr(q[i]) if i == j else Fr(0) for j in range(len(q))] for i in range(len(q))]

npass = nfail = 0
def chk(ok, label, note=''):
    global npass, nfail
    npass, nfail = npass+bool(ok), nfail+(not ok)
    print(('PASS  ' if ok else 'FAIL  ')+label+('  '+note if note else ''))

print('='*98); print('SECTION 8  REVIEWER CORRECTIONS'); print('='*98)

# ---- 8.1  kappa = 1 does NOT maximize the volume.  d/dk ratio at k=1 = ((r-1/r)^2 - 32)/144.
def ratio2(k, r):
    L2 = [[1, -1], [-1, 1]]
    H = [[Fr(int(i == j))+Fr(k)*Fr(L2[i][j]) for j in range(2)] for i in range(2)]
    return ratio_of(H, diag((1, Fr(r)**2)))
# exact derivative from the closed form ratio = (1 + (k/(1+k))^2 (r-1/r)^2/4)/(1+2k)
def ratio2_cf(k, r):
    k = Fr(k); r = Fr(r)
    return (1 + (k/(1+k))**2 * (r-1/r)**2/4)/(1+2*k)
bad = []
for r in (Fr(2), Fr(6), Fr(9), Fr(20)):
    for k in (Fr(1,3), Fr(1), Fr(5,2), Fr(7)):
        if ratio2(k, r) != ratio2_cf(k, r): bad.append((k, r))
chk(not bad, 'C8.1a two-mode closed form ratio = (1 + (k/(1+k))^2 (r-1/r)^2/4)/(1+2k)', '16 exact pairs')
# derivative at k=1 by exact difference quotient of the closed form, matched to the predicted value
bad = []
for r in (Fr(2), Fr(6), Fr(9), Fr(20), Fr(50)):
    pred = ((r-1/r)**2 - 32)/144
    h = Fr(1, 10**7)
    dq = (ratio2_cf(1+h, r) - ratio2_cf(1-h, r))/(2*h)
    if abs(dq - pred) > Fr(1, 10**6)*max(Fr(1), abs(pred)): bad.append((r, float(dq), float(pred)))
chk(not bad, "C8.1b REVIEWER CORRECTION: d/dk[ratio] at k=1 = ((r-1/r)^2 - 32)/144",
    'POSITIVE above threshold, so the volume is still RISING at k=1: k=1 minimizes the required anisotropy, it does NOT maximize volume')
# and the volume at k=1 is strictly below the volume at the true argmax, above threshold
bad = []
for r in (Fr(7), Fr(9), Fr(20)):
    v1 = ratio2_cf(1, r)
    best = max(ratio2_cf(Fr(i, 20), r) for i in range(1, 4000))
    if not best > v1: bad.append(r)
chk(not bad, 'C8.1c above threshold the volume-maximizing coupling is STRICTLY larger than k=1',
    'r=9: ratio(1) = %.6f vs max %.6f' % (float(ratio2_cf(1, Fr(9))),
                                          float(max(ratio2_cf(Fr(i,20), Fr(9)) for i in range(1,4000)))))

# ---- 8.2  decay exponent = rank L  (not always 2)
print()
GRAPHS = [('two-node path (rank 1)', [[1,-1],[-1,1]], (1, Fr(400))),
          ('three-node path (rank 2)', [[1,-1,0],[-1,2,-1],[0,-1,1]], (1, 1, Fr(400))),
          ('three nodes, one edge (rank 1)', [[1,-1,0],[-1,1,0],[0,0,0]], (1, Fr(400), Fr(9))),
          ('four-node path (rank 3)', [[1,-1,0,0],[-1,2,-1,0],[0,-1,2,-1],[0,0,-1,1]], (1,1,1,Fr(400)))]
bad = []
for nm, L, q in GRAPHS:
    n = len(L)
    rk = n - sum(1 for _ in range(1) for __ in [0])  # placeholder, computed below
    # rank over Q by elimination
    M = [[Fr(x) for x in row] for row in L]; rk = 0
    for c in range(n):
        piv = next((r for r in range(rk, n) if M[r][c] != 0), None)
        if piv is None: continue
        M[rk], M[piv] = M[piv], M[rk]; pv = M[rk][c]; M[rk] = [x/pv for x in M[rk]]
        for r in range(n):
            if r != rk and M[r][c]: f = M[r][c]; M[r] = [x-f*y for x, y in zip(M[r], M[rk])]
        rk += 1
    vals = []
    for k in (Fr(10**3), Fr(10**4), Fr(10**5)):
        H = [[Fr(int(i == j))+k*Fr(L[i][j]) for j in range(n)] for i in range(n)]
        vals.append(k**rk * ratio_of(H, diag(q)))
    conv = abs(vals[2]-vals[1]) < abs(vals[1]-vals[0]) and vals[2] > 0
    print('  %-32s rank L = %d   k^rank * ratio -> %.6f  %s'
          % (nm, rk, float(vals[2]), 'converges' if conv else 'DIVERGES'))
    if not conv: bad.append(nm)
chk(not bad, 'C8.2 REVIEWER CORRECTION: det Sigma_k/det Sigma_0 = Theta(k^{-rank L}), not always k^{-2}',
    'rank 1 -> k^-1 (two-mode), rank n-1 for a connected n-node graph')

# ---- 8.3  det C by the Cauchy determinant formula
print()
def cmat_rational_det(a):
    """det C = prod_{i<j} ((a_i-a_j)/(a_i+a_j))^2  -- Cauchy determinant."""
    n = len(a); p = Fr(1)
    for i in range(n):
        for j in range(i+1, n):
            p *= ((Fr(a[i])-Fr(a[j]))/(Fr(a[i])+Fr(a[j])))**2
    return p
import math
def cmat(a):
    def rt(x):
        num, den = Fr(x).numerator, Fr(x).denominator
        s, t = math.isqrt(num), math.isqrt(den)
        assert s*s == num and t*t == den
        return Fr(s, t)
    s = [rt(x) for x in a]
    return [[2*s[i]*s[j]/(Fr(a[i])+Fr(a[j])) for j in range(len(a))] for i in range(len(a))]
bad = []
for a in ((Fr(1), Fr(4)), (Fr(1), Fr(4), Fr(9)), (Fr(1,4), Fr(9), Fr(25)), (Fr(1), Fr(4), Fr(9), Fr(16)),
          (Fr(4), Fr(4), Fr(9))):
    if det(cmat(a)) != cmat_rational_det(a): bad.append(a)
chk(not bad, 'C8.3 det C = prod_{i<j} ((a_i-a_j)/(a_i+a_j))^2  (Cauchy determinant formula)',
    '5 rate tuples incl. a repeated rate, where det C = 0')

# ---- 8.4  the Oppenheim-Schur refinement
print()
def phi(C, X): return [[C[i][j]*X[i][j] for j in range(len(X))] for i in range(len(X))]
bad = []; tight = 0; cases = 0; slack = []
QS2 = ([[Fr(1), Fr(0)], [Fr(0), Fr(9)]], [[Fr(4), Fr(1)], [Fr(1), Fr(3)]])
QS3 = ([[Fr(2),Fr(1),Fr(0)],[Fr(1),Fr(5),Fr(2)],[Fr(0),Fr(2),Fr(3)]],
       [[Fr(9),Fr(-2),Fr(1)],[Fr(-2),Fr(4),Fr(-1)],[Fr(1),Fr(-1),Fr(6)]],
       [[Fr(1),Fr(0),Fr(0)],[Fr(0),Fr(7),Fr(0)],[Fr(0),Fr(0),Fr(2)]])
for a, QQ in ((((Fr(1), Fr(4))), QS2), (((Fr(1), Fr(4), Fr(9))), QS3), (((Fr(1,4), Fr(9), Fr(25))), QS3)):
    C = cmat(a); dC = det(C)
    for Qt in QQ:
        n = len(a); dQ = det(Qt)
        rho = Fr(1)
        for i in range(n): rho *= Qt[i][i]
        rho /= dQ
        lhs = det(phi(C, Qt))/dQ
        rhs = 1 + dC*(rho - 1)
        cases += 1
        if lhs < rhs: bad.append((a, Qt, float(lhs), float(rhs)))
        if lhs == rhs: tight += 1
        slack.append(float(lhs/rhs) if rhs != 0 else None)
chk(not bad, 'C8.4a Oppenheim-Schur refinement: det(C o Qt)/det Qt >= 1 + det C (rho - 1)',
    '%d cases, EQUALITY in %d of them (all the n=2 ones)' % (cases, tight))
# equality in 2D, strict in 3D
eq2 = all(det(phi(cmat((Fr(1),Fr(4))), Q))/det(Q)
          == 1 + det(cmat((Fr(1),Fr(4))))*(Q[0][0]*Q[1][1]/det(Q) - 1) for Q in QS2)
chk(eq2, 'C8.4b the refinement is an IDENTITY for n = 2, so it must recover the exact two-mode threshold')

print()
print('='*98)
print('SECTION 8 TOTALS: %d checks, %d passed, %d failed' % (npass+nfail, npass, nfail))
print('='*98)

# ---- 8.5  the reviewer's centre-noise closed form, and its kappa* cubic
print()
print('  REVIEWER CLOSED FORM (centre noise):')
L3 = [[1,-1,0],[-1,2,-1],[0,-1,1]]
def H3(k): return [[Fr(int(i == j))+Fr(k)*Fr(L3[i][j]) for j in range(3)] for i in range(3)]
def centre_cf(k, r):
    k, r = Fr(k), Fr(r)
    return (1 + 2*k**2*(r-1/r)**2/(2+3*k)**2)/((1+k)*(1+3*k))
bad = []
for r in (Fr(2), Fr(5), Fr(9), Fr(20), Fr(50), Fr(100)):
    for k in (Fr(1,10), Fr(41,100), Fr(1), Fr(3), Fr(25)):
        exact = ratio_of(H3(k), diag((1, r**2, 1)))
        if exact != centre_cf(k, r): bad.append((k, r, float(exact), float(centre_cf(k, r))))
chk(not bad, 'C8.5a REVIEWER: centre ratio = (1 + 2k^2(r-1/r)^2/(2+3k)^2)/((1+k)(1+3k))',
    '30 exact (k,r) pairs vs independent Lyapunov solves')
# expansion <=> (r-1/r)^2 > 8/k + 30 + 36k + 27k^2/2
def centre_cost(k):
    k = Fr(k); return 8/k + 30 + 36*k + Fr(27,2)*k**2
bad = []
for r in (Fr(5), Fr(9), Fr(20)):
    for k in (Fr(1,10), Fr(41,100), Fr(1), Fr(3)):
        if (centre_cf(k, r) > 1) != ((r-1/r)**2 > centre_cost(k)): bad.append((k, r))
chk(not bad, 'C8.5b equivalent form: expansion <=> (r-1/r)^2 > 8/k + 30 + 36k + 27k^2/2', '12 pairs')
# kappa* = positive root of 27k^3 + 36k^2 - 8 = 0, bracketed exactly
def cubic(k): k = Fr(k); return 27*k**3 + 36*k**2 - 8
lo, hi = Fr(0), Fr(1)
for _ in range(80):
    mid = (lo+hi)/2
    if cubic(mid) < 0: lo = mid
    else: hi = mid
chk(cubic(lo) < 0 < cubic(hi), 'C8.5c kappa* is the positive root of 27k^3 + 36k^2 - 8 = 0',
    'bracketed: %.10f < kappa* < %.10f' % (float(lo), float(hi)))
# and it is the argmin of the cost, giving r*
cmin = centre_cost(hi)
# r - 1/r = sqrt(cmin)  =>  r = (s + sqrt(s^2+4))/2 with s = sqrt(cmin)
import math
s = math.sqrt(float(cmin)); rstar = (s + math.sqrt(s*s+4))/2
print('    cost(kappa*) = %.10f   =>  r* = %.10f' % (float(cmin), rstar))
# kappa* is the argmin BY THE DERIVATIVE IDENTITY, not by a grid:
#   cost'(k) = -8/k^2 + 36 + 27k,  so  k^2 cost'(k) = 27k^3 + 36k^2 - 8,
# and cost''(k) = 16/k^3 + 27 > 0 for k > 0, so the cubic's unique positive root is the minimum.
def dcost(k): k = Fr(k); return -8/k**2 + 36 + 27*k
bad = [k for k in (Fr(1,10), Fr(41,100), Fr(1), Fr(3), Fr(7,2))
       if Fr(k)**2 * dcost(k) != cubic(k)]
inside = Fr(8278000767, 10**9) < Fr(int(rstar*10**7), 10**7) < Fr(8278100768, 10**9)
chk(not bad and inside and dcost(lo) < 0 < dcost(hi),
    'C8.5d kappa* is the argmin (k^2 cost\'(k) = the cubic, cost\'\' > 0) and r* = %.7f lies '
    'INSIDE the certified bracket' % rstar,
    'certified bracket was [8.278000767, 8.278100768]; the cubic has exactly one positive root')

# ---- 8.6  THE NEXT STEP: how much of the three-mode threshold does the general
#          Oppenheim-Schur sufficient condition  1 + det C (rho-1) > det H_k  capture?
print()
print('  SUFFICIENT CONDITION  1 + det C (rho - 1) > det H_kappa   vs the certified thresholds:')
def detC3(k):
    k = Fr(k)
    return 36*k**6/((2+k)*(2+3*k)*(2+4*k))**2
def rho_end(r): r = Fr(r); return (2+r**2)*(1+r**2)*(5+r**2)/(36*r**2)
def rho_centre(r): r = Fr(r); return (2+r**2)*(1+2*r**2)/(9*r**2)
def suff_holds(r, rho_fn):
    rho = rho_fn(r)
    return any(1 + detC3(Fr(i, 200))*(rho-1) > (1+Fr(i,200))*(1+3*Fr(i,200))
               for i in range(1, 4000))
rows = []
for nm, rho_fn, true_lo, true_hi in (('centre', rho_centre, 8.278000767, 8.278100768),
                                     ('end   ', rho_end, 10.720241993, 10.720242994)):
    lo, hi = Fr(1), Fr(400)
    for _ in range(40):
        mid = (lo+hi)/2
        if suff_holds(mid, rho_fn): hi = mid
        else: lo = mid
    rows.append((nm, float(hi), true_hi))
    print('    %s  sufficient condition first satisfiable at r = %.6f   true threshold ~ %.6f'
          '   factor %.3f' % (nm, float(hi), true_hi, float(hi)/true_hi))
chk(all(rs > tt for _, rs, tt in rows),
    'C8.6 the general sufficient condition is STRICTLY WEAKER than the true three-mode threshold',
    'overshoot factors %.3f (centre) and %.3f (end): det C decays like k^6 so the refinement is '
    'uninformative exactly where expansion happens (small/moderate kappa)'
    % (rows[0][1]/rows[0][2], rows[1][1]/rows[1][2]))
# the stated limitation: repeated rates kill it
chk(cmat_rational_det((Fr(4), Fr(4), Fr(9))) == 0,
    'C8.6b with repeated damping rates det C = 0 and the refinement degenerates to plain Oppenheim',
    'recorded limitation')
# and no bound in the rate spread alone can work: commuting Q gives ratio exactly 1/det H
bad = []
for k in (Fr(1,3), Fr(2)):
    H = [[Fr(int(i == j))+Fr(k)*Fr(L3[i][j]) for j in range(3)] for i in range(3)]
    Q = [[sum(H[i][m]*H[m][j] for m in range(3)) for j in range(3)] for i in range(3)]  # Q = H^2, commutes
    if ratio_of(H, Q) != 1/det(H): bad.append(k)
chk(not bad, 'C8.6c REVIEWER: no bound in the rate spread ALONE can improve on this',
    'Q commuting with H (here Q = H^2) gives det(C o Qt)/det Qt = 1 exactly, for any rate spread')

print()
print('='*98)
print('SECTION 8 TOTALS: %d checks, %d passed, %d failed' % (npass+nfail, npass, nfail))
print('='*98)
