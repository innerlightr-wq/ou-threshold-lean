#!/usr/bin/env python3
"""SECTION 7 controls.  Each one tests a LITERATURE statement against this project's objects,
so that the prior-art classification rests on a check rather than on recollection.

Phi_H(X) = C o X in the eigenbasis of H, with c_ij = 2 sqrt(a_i a_j)/(a_i + a_j) = GM/AM.
Exact arithmetic throughout: rates are perfect squares so every c_ij is rational.
"""
from fractions import Fraction as Fr
from itertools import permutations, product

def det(M):
    n = len(M)
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
def mm(A, B): return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def sub(A, B): return [[A[i][j]-B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
def iszero(M): return all(x == 0 for row in M for x in row)
def is_psd(M):
    # all principal minors (not just leading) >= 0  <=>  PSD for symmetric M
    n = len(M)
    for k in range(1, n+1):
        for S in permutations(range(n), k):
            S = sorted(S)
            if det([[M[i][j] for j in S] for i in S]) < 0: return False
    return True
def is_pd(M):
    return all(det([[M[i][j] for j in range(k)] for i in range(k)]) > 0 for k in range(1, len(M)+1))

def cmat(rates):
    """c_ij = 2 sqrt(a_i a_j)/(a_i + a_j).  rates must be perfect squares of rationals."""
    import math
    def rt(x):
        num, den = x.numerator, x.denominator
        a, b = math.isqrt(num), math.isqrt(den)
        assert a*a == num and b*b == den, 'rate %s is not a perfect square' % x
        return Fr(a, b)
    s = [rt(Fr(a)) for a in rates]
    return [[2*s[i]*s[j]/(Fr(rates[i])+Fr(rates[j])) for j in range(len(rates))] for i in range(len(rates))]
def Phi(C, X): return [[C[i][j]*X[i][j] for j in range(len(X))] for i in range(len(X))]

npass = nfail = 0
def chk(ok, label, note=''):
    global npass, nfail
    npass, nfail = npass+bool(ok), nfail+(not ok)
    print(('PASS  ' if ok else 'FAIL  ')+label+('  '+note if note else ''))

print('='*98)
print('SECTION 7  CONTROLS ON THE PRIOR-ART CLASSIFICATION')
print('='*98)

RATES = [(Fr(1), Fr(4), Fr(9)), (Fr(1), Fr(1), Fr(4)), (Fr(4), Fr(4), Fr(4)),
         (Fr(1), Fr(4), Fr(4)), (Fr(1,4), Fr(9), Fr(25))]

# 7.1  C is a correlation matrix, and infinitely divisible (Bhatia-Kosaki mean matrices):
#      every entrywise power C^(t) is PSD.  Tested for t = 1,2,3,4 (rational powers stay exact
#      for even t; odd powers of this kernel are rational too since c_ij is rational here).
bad = []
for rates in RATES:
    C = cmat(rates)
    if not (all(C[i][i] == 1 for i in range(3)) and is_psd(C)): bad.append(('psd', rates))
    for t in (2, 3, 4, 8):
        Ct = [[C[i][j]**t for j in range(3)] for i in range(3)]
        if not is_psd(Ct): bad.append(('divis', rates, t))
chk(not bad, 'C7.1  C is a unit-diagonal PSD (correlation) matrix and every Hadamard power C^(t) is PSD',
    'the GM/AM mean matrix; infinite divisibility is Bhatia-Kosaki, 5 rate triples x t=1,2,3,4,8')

# 7.2  Phi_H is unital, trace-preserving on the eigenbasis diagonal, and positive;
#      complete positivity is the Schur product theorem (Schur 1911) applied to C.
bad = []
for rates in RATES:
    C = cmat(rates)
    I3 = [[Fr(int(i == j)) for j in range(3)] for i in range(3)]
    if Phi(C, I3) != I3: bad.append(('unital', rates))
    for Q in ([[Fr(2),Fr(1),Fr(0)],[Fr(1),Fr(5),Fr(2)],[Fr(0),Fr(2),Fr(3)]],
              [[Fr(9),Fr(-2),Fr(1)],[Fr(-2),Fr(4),Fr(-1)],[Fr(1),Fr(-1),Fr(6)]]):
        if not is_pd(Q): bad.append(('input', rates)); continue
        if not is_pd(Phi(C, Q)): bad.append(('pos', rates))
        if sum(Phi(C, Q)[i][i] for i in range(3)) != sum(Q[i][i] for i in range(3)):
            bad.append(('trace', rates))
chk(not bad, 'C7.2  Phi_H unital, trace-preserving, positive (Schur product theorem)',
    '5 rate triples x 2 positive-definite inputs')

# 7.3  MULTIPLICATIVE DOMAIN.  Literature: for a Schur-product channel X -> C o X with C a
#      correlation matrix, the multiplicative domain is { X : X_ij = 0 whenever |c_ij| < 1 }.
#      Here |c_ij| = 1  <=>  a_i = a_j, so the predicted multiplicative domain is exactly the
#      commutant of H.  This is the control that reclassifies the section-4 "classification"
#      result as a specialization of a known theorem rather than a new one.
bad = []
tested = 0
for rates in RATES:
    C = cmat(rates)
    n = 3
    supp = [[(Fr(rates[i]) == Fr(rates[j])) for j in range(n)] for i in range(n)]
    # (a) X supported inside the predicted domain: Phi is multiplicative against every Y
    for vals in product((Fr(0), Fr(1), Fr(3)), repeat=n*n):
        X = [[vals[i*n+j] if supp[i][j] else Fr(0) for j in range(n)] for i in range(n)]
        if iszero(X): continue
        for Y in ([[Fr(1),Fr(2),Fr(3)],[Fr(4),Fr(5),Fr(6)],[Fr(7),Fr(8),Fr(9)]],
                  [[Fr(0),Fr(1),Fr(0)],[Fr(2),Fr(0),Fr(5)],[Fr(1),Fr(1),Fr(1)]]):
            tested += 1
            if not iszero(sub(Phi(C, mm(X, Y)), mm(Phi(C, X), Phi(C, Y)))):
                bad.append(('mult fails inside domain', rates, X)); break
        else: continue
        break
    # (b) X with a single entry OUTSIDE the predicted domain: Phi(X*X) != Phi(X)*Phi(X)
    for i in range(n):
        for j in range(n):
            if supp[i][j]: continue
            X = [[Fr(0)]*n for _ in range(n)]
            X[i][j] = Fr(1)
            XsX = mm([[X[b][a] for b in range(n)] for a in range(n)], X)   # X^T X
            PX = Phi(C, X)
            lhs = Phi(C, XsX)
            rhs = mm([[PX[b][a] for b in range(n)] for a in range(n)], PX)
            tested += 1
            if iszero(sub(lhs, rhs)): bad.append(('mult holds outside domain', rates, (i, j)))
chk(not bad, 'C7.3  multiplicative domain of Phi_H is EXACTLY the commutant of H',
    'matches the known Schur-channel characterization { X_ij = 0 where |c_ij| < 1 }; %d instances' % tested)

# 7.4  OPPENHEIM.  det(C o Q) >= det(Q) * prod C_ii = det Q, with the general Oppenheim-Schur
#      inequality.  So the determinant theorem of section 4 is Oppenheim 1930 applied to a
#      unit-diagonal C -- classical, with only the equality characterization specialized here.
bad = []
strict = eq = 0
QS = ([[Fr(2),Fr(1),Fr(0)],[Fr(1),Fr(5),Fr(2)],[Fr(0),Fr(2),Fr(3)]],
      [[Fr(9),Fr(-2),Fr(1)],[Fr(-2),Fr(4),Fr(-1)],[Fr(1),Fr(-1),Fr(6)]],
      [[Fr(1),Fr(0),Fr(0)],[Fr(0),Fr(7),Fr(0)],[Fr(0),Fr(0),Fr(2)]])
for rates in RATES:
    C = cmat(rates)
    for Q in QS:
        d1, d0 = det(Phi(C, Q)), det(Q)
        if d1 < d0: bad.append((rates, 'violates Oppenheim'))
        # Oppenheim also gives the stronger  det(C o Q) >= det C * prod Q_ii  (Schur) -- check
        if d1 < det(C) * Q[0][0]*Q[1][1]*Q[2][2]: bad.append((rates, 'violates Schur form'))
        commuting = all(C[i][j] == 1 or Q[i][j] == 0 for i in range(3) for j in range(3))
        if d1 == d0: eq += 1
        else: strict += 1
        if commuting != (d1 == d0): bad.append((rates, Q, 'equality condition'))
chk(not bad, 'C7.4  det Phi_H(Q) >= det Q (Oppenheim) AND >= det C * prod Q_ii (Schur), equality iff [H,Q]=0',
    '%d strict, %d equality cases over 15 pairs' % (strict, eq))

# 7.5  NOT classical: the ceiling theorem's quantity rho(Q,L) = prod Qt_ii/det Q is the Hadamard
#      ratio of the ROTATED noise, so it depends on the eigenvectors of L, not only spec(Q).
#      Control: two Q with identical spectra and different rho.
L3 = [[1,-1,0],[-1,2,-1],[0,-1,1]]
def rotate(q):
    # Qt = U^T Q U in the orthonormal eigenbasis of L3
    import math
    u = [[Fr(1),Fr(1),Fr(1)], [Fr(1),Fr(0),Fr(-1)], [Fr(1),Fr(-2),Fr(1)]]
    nrm = [3, 2, 6]
    Q = [[Fr(q[i]) if i == j else Fr(0) for j in range(3)] for i in range(3)]
    out = [[Fr(0)]*3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            s = sum(u[i][a]*Q[a][b]*u[j][b] for a in range(3) for b in range(3))
            out[i][j] = s   # un-normalised; diagonal entries need /nrm[i]
    return [[out[i][j] for j in range(3)] for i in range(3)], nrm
r2 = Fr(81)
rhos = []
for q in ((1, 1, r2), (1, r2, 1)):
    O, nrm = rotate(q)
    diag = [O[i][i]/nrm[i] for i in range(3)]
    rhos.append(diag[0]*diag[1]*diag[2]/(Fr(q[0])*Fr(q[1])*Fr(q[2])))
chk(rhos[0] != rhos[1],
    'C7.5  rho(Q,L) depends on the ORIENTATION of Q relative to L, not on spec(Q)',
    'same spectrum {1,1,81}: rho = %.6f (end) vs %.6f (centre)' % (float(rhos[0]), float(rhos[1])))

# 7.6  THE SANDWICH.  In the eigenbasis of H,  Sigma = (1/2) D^{-1/2} (C o Qt) D^{-1/2}  with
#      D = diag(a), so  det Sigma = det(C o Qt)/(2^n det H)  and
#          ratio := det Sigma_kappa/det Sigma_0 = det(C o Qt)/(det H * det Q).
#      Oppenheim gives det(C o Qt) >= det Qt = det Q and Hadamard gives
#      det(C o Qt) <= prod Qt_ii, hence the two-sided bound
#          1/det H_kappa  <=  ratio  <=  rho(Q,L)/det H_kappa,     rho = prod Qt_ii/det Q.
#      The left bound says coupling never costs more than det H; the right bound confines
#      expansion to the bounded window { det H_kappa < rho }.
def lyap_solve(H, Q):
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
    M = [A[i][:]+[b[i]] for i in range(len(b))]
    nn = len(b)
    for c in range(nn):
        piv = next(r for r in range(c, nn) if M[r][c] != 0)
        M[c], M[piv] = M[piv], M[c]; pv = M[c][c]
        M[c] = [x/pv for x in M[c]]
        for r in range(nn):
            if r != c and M[r][c]: f = M[r][c]; M[r] = [x-f*y for x, y in zip(M[r], M[c])]
    v = [M[i][nn] for i in range(nn)]
    S = [[Fr(0)]*n for _ in range(n)]
    for t, (i, j) in enumerate(idx): S[i][j] = S[j][i] = v[t]
    return S

bad = []; tight_lo = tight_hi = 0; cases = 0
for k in (Fr(1,10), Fr(1,2), Fr(1), Fr(3), Fr(20)):
    H = [[Fr(int(i == j))+Fr(k)*Fr(L3[i][j]) for j in range(3)] for i in range(3)]
    for q in ((1, 1, Fr(400)), (1, Fr(400), 1), (Fr(2), Fr(3), Fr(5)), (Fr(7), Fr(7), Fr(7))):
        Q = [[Fr(q[i]) if i == j else Fr(0) for j in range(3)] for i in range(3)]
        ratio = det(lyap_solve(H, Q))*Fr(2)**3/det(Q)
        detH = det(H)
        O, nrm = rotate(q)
        rho = (O[0][0]/nrm[0])*(O[1][1]/nrm[1])*(O[2][2]/nrm[2])/(Fr(q[0])*Fr(q[1])*Fr(q[2]))
        cases += 1
        if not (1/detH <= ratio <= rho/detH): bad.append((k, q, float(ratio)))
        if ratio == 1/detH: tight_lo += 1
        if ratio == rho/detH: tight_hi += 1
chk(not bad, 'C7.6  SANDWICH 1/det H_kappa <= det Sigma_k/det Sigma_0 <= rho(Q,L)/det H_kappa',
    'Oppenheim left, Hadamard right; %d cases, left tight in %d (isotropic/aligned noise)' % (cases, tight_lo))

print()
print('='*98)
print('SECTION 7 TOTALS: %d checks, %d passed, %d failed' % (npass+nfail, npass, nfail))
print('='*98)
