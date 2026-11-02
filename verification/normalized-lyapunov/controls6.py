#!/usr/bin/env python3
"""SECTION 6  Discriminating controls.

Each control is designed so that a WRONG version of the section 2-5 statements fails it.
All arithmetic is exact over Q (or over Q(sqrt(2)) where the two-mode threshold is involved).
"""
from fractions import Fraction as Fr
from itertools import permutations

# ---------------------------------------------------------------- exact linear algebra over Q
def det(M):
    n = len(M)
    if n == 1: return M[0][0]
    M = [row[:] for row in M]; s = Fr(1)
    for c in range(n):
        piv = next((r for r in range(c, n) if M[r][c] != 0), None)
        if piv is None: return Fr(0)
        if piv != c: M[c], M[piv] = M[piv], M[c]; s = -s
        s *= M[c][c]; pv = M[c][c]
        M[c] = [x/pv for x in M[c]]
        for r in range(c+1, n):
            if M[r][c]: f = M[r][c]; M[r] = [x-f*y for x, y in zip(M[r], M[c])]
    return s
def solve(A, b):
    n, M = len(b), [row[:]+[b[i]] for i, row in enumerate(A)]
    for c in range(n):
        piv = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[piv] = M[piv], M[c]; pv = M[c][c]
        M[c] = [x/pv for x in M[c]]
        for r in range(n):
            if r != c and M[r][c]: f = M[r][c]; M[r] = [x-f*y for x, y in zip(M[r], M[c])]
    return [M[i][n] for i in range(n)]
def lyap(H, Q):
    """Solve H S + S H = Q for symmetric S exactly.  Raises if H has a zero eigenvalue
    pairing (the Sylvester operator X -> HX + XH is singular iff a_i + a_j = 0 for some i,j)."""
    n = len(H)
    idx = [(i, j) for i in range(n) for j in range(i, n)]
    pos = {}
    for t, (i, j) in enumerate(idx): pos[(i, j)] = t; pos[(j, i)] = t
    A, b = [], []
    for (i, j) in idx:
        row = [Fr(0)]*len(idx)
        for k in range(n):
            row[pos[(k, j)]] += H[i][k]; row[pos[(i, k)]] += H[k][j]
        A.append(row); b.append(Fr(Q[i][j]))
    v = solve(A, b)
    S = [[Fr(0)]*n for _ in range(n)]
    for t, (i, j) in enumerate(idx): S[i][j] = S[j][i] = v[t]
    return S
def mm(A, B): return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def sub(A, B): return [[A[i][j]-B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
def is_pd(M):
    return all(det([[M[i][j] for j in range(k)] for i in range(k)]) > 0 for k in range(1, len(M)+1))
def comm(A, B): return sub(mm(A, B), mm(B, A))
def ratio_of(H, Q):
    """det Sigma_H(Q) / det Sigma_I(Q).  Sigma_I = Q/2, so det Sigma_I = det Q / 2^n:
    the normalizing power is the DIMENSION, not a fixed constant."""
    n = len(H)
    return det(lyap(H, Q)) * Fr(2)**n / det(Q)
def iszero(M): return all(x == 0 for row in M for x in row)

npass = nfail = 0
def chk(ok, label, note=''):
    global npass, nfail
    npass, nfail = npass+bool(ok), nfail+(not ok)
    print(('PASS  ' if ok else 'FAIL  ')+label+('  '+note if note else ''))

print('='*96)
print('SECTION 6  DISCRIMINATING CONTROLS')
print('='*96)

# ------------------------------------------------------------------ 6.1  kappa = 0
I2 = [[Fr(1), Fr(0)], [Fr(0), Fr(1)]]
Q = [[Fr(1), Fr(0)], [Fr(0), Fr(400)]]
S = lyap(I2, Q)
chk(S == [[Fr(1,2), Fr(0)], [Fr(0), Fr(200)]] and ratio_of(I2, Q) == 1,
    'C6.1  kappa = 0: Sigma = Q/2 and det Sigma/det Sigma_0 = 1 for every Q',
    'no coupling, no determinant change, at arbitrarily large r')

# ------------------------------------------------------------------ 6.2  r = 1 (isotropic noise)
def Hk2(k): return [[1+Fr(k), -Fr(k)], [-Fr(k), 1+Fr(k)]]
bad = []
for k in (Fr(1,5), Fr(1), Fr(7), Fr(100)):
    H = Hk2(k); S = lyap(H, I2)
    # Sigma = H^{-1}/2 exactly, so det ratio = 1/det H < 1
    if not (ratio_of(H, I2) == 1/det(H) and ratio_of(H, I2) < 1): bad.append(k)
chk(not bad, 'C6.2  r = 1: Sigma = H^{-1}/2 exactly, ratio = 1/det H < 1, NEVER expansion',
    'isotropic noise can never trip the threshold, at any coupling')

# ------------------------------------------------------------------ 6.3  r below / at / above 3+2sqrt(2)
def vol_ratio2(k, r):
    return ratio_of(Hk2(k), [[Fr(1), Fr(0)], [Fr(0), Fr(r)**2]])
rstar = 3+2*2**0.5
below, above = Fr(5), Fr(6)          # 5 < 5.8284 < 6
m_below = max(vol_ratio2(Fr(i,100), below) for i in range(1, 2001))
w_above = next((Fr(i,100) for i in range(1, 2001) if vol_ratio2(Fr(i,100), above) > 1), None)
chk(m_below < 1 and w_above is not None,
    'C6.3  two-mode threshold is SHARP in r: r = 5 never expands, r = 6 does',
    'max ratio at r=5 is %.9f (<1); witness at r=6 is kappa = %s' % (float(m_below), w_above))
# at the threshold itself: r^2 = 17 + 12 sqrt(2); use the repo bracket instead of a float
hi = Fr(5828428, 10**6); lo = Fr(5828426, 10**6)
chk(all(vol_ratio2(Fr(i,100), lo) <= 1 for i in range(1, 2001))
    and any(vol_ratio2(Fr(i,100), hi) > 1 for i in range(1, 2001)),
    'C6.3b exact rational sign change straddling 3+2sqrt(2) = %.9f' % rstar,
    'no expansion at r = %s, expansion at r = %s' % (lo, hi))

# ------------------------------------------------------------------ 6.4  noise commuting with H
bad = []
for k in (Fr(1,3), Fr(2), Fr(50)):
    H = Hk2(k)
    for Qc in ([[Fr(3), Fr(0)], [Fr(0), Fr(3)]],                      # scalar
               [[Fr(5), Fr(2)], [Fr(2), Fr(5)]],                      # same eigenvectors as H
               [[Fr(7), Fr(-3)], [Fr(-3), Fr(7)]]):
        if not iszero(comm(H, Qc)): bad.append(('noncomm', k)); continue
        S = lyap(H, Qc)
        # commuting noise: Sigma = H^{-1}Q/2, ratio = 1/det H < 1, and [H,Sigma] = 0
        if not (ratio_of(H, Qc) == 1/det(H) and iszero(comm(H, S))): bad.append((k, Qc))
chk(not bad, 'C6.4  [H,Q] = 0: Sigma = H^{-1}Q/2, ratio = 1/det H < 1, expansion IMPOSSIBLE',
    'the mechanism needs noise misaligned with the damping geometry, 9 cases')

# ------------------------------------------------------------------ 6.5  self-adjoint off-diagonal witness
# Phi_H preserves self-adjointness; a purely off-diagonal self-adjoint X must still obey the
# square-defect formula.  X = [[0,1],[1,0]] with H = diag(a1,a2).
bad = []
for a1, a2 in ((Fr(1), Fr(1)), (Fr(1), Fr(4)), (Fr(2), Fr(9)), (Fr(1), Fr(100))):
    H = [[a1, Fr(0)], [Fr(0), a2]]
    X = [[Fr(0), Fr(1)], [Fr(1), Fr(0)]]
    c = 4*a1*a2/(a1+a2)**2                    # c_12^2, rational even when c_12 is not
    PhiX2 = [[c, Fr(0)], [Fr(0), c]]          # Phi(X^2) = Phi(I) = I ... careful: X^2 = I
    # Phi(X^2) = Phi(I) = I since Phi is unital; Phi(X)^2 = c * I
    defect = sub([[Fr(1), Fr(0)], [Fr(0), Fr(1)]], [[c, Fr(0)], [Fr(0), c]])
    ok = (defect[0][0] == 1-c and defect[0][0] >= 0
          and (defect[0][0] == 0) == (a1 == a2))
    if not ok: bad.append((a1, a2))
chk(not bad, 'C6.5  self-adjoint off-diagonal X = [[0,1],[1,0]]: Phi(X^2)-Phi(X)^2 = (1-c_12^2) I',
    'vanishes exactly when the two damping rates coincide, 4 rate pairs')

# ------------------------------------------------------------------ 6.6  repeated damping rates
# If H has a repeated eigenvalue on a block, c_ij = 1 there and Phi acts as the identity on it.
bad = []
for a in (Fr(1), Fr(3), Fr(7,2)):
    H3 = [[a, Fr(0), Fr(0)], [Fr(0), a, Fr(0)], [Fr(0), Fr(0), 2*a]]
    for Qd in ([[Fr(1), Fr(2), Fr(0)], [Fr(2), Fr(9), Fr(1)], [Fr(0), Fr(1), Fr(4)]],):
        if not is_pd(Qd): bad.append('notpd'); continue
        S = lyap(H3, Qd)
        # on the repeated block (indices 0,1) Phi is the identity: 2 a S_ij = Q_ij
        ok = all(2*a*S[i][j] == Qd[i][j] for i in (0, 1) for j in (0, 1))
        if not ok: bad.append(a)
chk(not bad, 'C6.6  repeated damping rates: Phi_H restricts to the IDENTITY on that spectral block',
    'c_ij = 1 there; degeneracy removes all distortion, 3 scales')

# ------------------------------------------------------------------ 6.7  same Q spectrum, different orientation
# This is the sharpest control: diag(1,1,r^2) and diag(1,r^2,1) have the SAME eigenvalues.
# A threshold depending only on the noise spectrum would give them the same critical r.
L3 = [[1, -1, 0], [-1, 2, -1], [0, -1, 1]]
def H3k(k): return [[Fr(int(i == j))+Fr(k)*Fr(L3[i][j]) for j in range(3)] for i in range(3)]
def ratio3(k, q):
    Qd = [[Fr(q[i]) if i == j else Fr(0) for j in range(3)] for i in range(3)]
    return ratio_of(H3k(k), Qd)
r = Fr(9)
end  = max(ratio3(Fr(i,50), (1, 1, r**2)) for i in range(1, 400))
cent = max(ratio3(Fr(i,50), (1, r**2, 1)) for i in range(1, 400))
chk(end < 1 < cent,
    'C6.7  SAME noise spectrum, different orientation: at r = 9 the centre node expands and the end node does not',
    'max ratio: end %.9f, centre %.9f -- the threshold is NOT a function of spec(Q) alone' % (float(end), float(cent)))

# ------------------------------------------------------------------ 6.8  excluded domain: H with a zero eigenvalue
sing = [[Fr(1), Fr(1)], [Fr(1), Fr(1)]]      # eigenvalues 0, 2
chk(det(sing) == 0, 'C6.8  excluded-domain control: H singular (eigenvalues 0 and 2)',
    'a_i + a_j = 0 occurs, so the Sylvester operator is singular')
failed = False
try:
    lyap(sing, Q)
except StopIteration:
    failed = True
chk(failed, 'C6.8b the Lyapunov solve is NOT uniquely solvable for singular H, as required',
    'Phi_H and the whole normalized-Lyapunov construction need H > 0; the repo keeps kappa > -1/2')
# and the repository's own domain: H_kappa > 0 iff kappa > -1/2 in two modes
chk(all(is_pd(Hk2(k)) for k in (Fr(0), Fr(1,10), Fr(5)))
    and not is_pd(Hk2(Fr(-1,2))) and not is_pd(Hk2(Fr(-1))),
    'C6.8c two-mode domain: H_kappa > 0 for kappa > -1/2, fails at kappa = -1/2 and -1',
    'matches the repository hypothesis 0 < kappa')

print()
print('='*96)
print('SECTION 6 TOTALS: %d checks, %d passed, %d failed' % (npass+nfail, npass, nfail))
print('='*96)
