import sympy as sp
k,r,t,s,q,a1,a2,s1,s2 = sp.symbols('kappa r t s q a1 a2 sigma1 sigma2', positive=True)

ok=lambda n,c: print(("PASS " if c else "**FAIL** ")+n)

# --- paper eq (20) / eq:Aequal
A = (k**2*r**4+2*k**2*r**2+k**2+8*k*r**2+4*r**2)/(16*(k+1)**2*(2*k+1))
# --- NEW eq:Amodal
Amod = (1+r**2)**2/(16*(1+2*k)) - (1-r**2)**2/(16*(1+k)**2)
ok("eq:Amodal == eq:Aequal", sp.simplify(A-Amod)==0)

# modal entries from Sigma_ij = Qt_ij/(D_i+D_j), D1=1, D2=1+2k
Qt = sp.Matrix([[(1+r**2)/2,(1-r**2)/2],[(1-r**2)/2,(1+r**2)/2]])
D=[1,1+2*k]
St = sp.Matrix(2,2, lambda i,j: Qt[i,j]/(D[i]+D[j]))
ok("modal Sigma entries", sp.simplify(St[0,0]-(1+r**2)/4)==0 and sp.simplify(St[1,1]-(1+r**2)/(4*(1+2*k)))==0 and sp.simplify(St[0,1]-(1-r**2)/(4*(1+k)))==0)
ok("det modal == A", sp.simplify(St.det()-A)==0)
# and that it really solves the modal Lyapunov eq  M~S + S M~^T = -Q~
Mt = sp.diag(-1,-(1+2*k))
ok("modal Lyapunov residual = 0", sp.simplify(Mt*St+St*Mt.T+Qt)==sp.zeros(2,2))

# Qtilde is the rotation of diag(1,r^2)
R = sp.Matrix([[1,1],[1,-1]])/sp.sqrt(2)
ok("Qtilde = R diag(1,r^2) R^T", sp.simplify(R*sp.diag(1,r**2)*R.T - Qt)==sp.zeros(2,2))

# --- difference formula eq:diff  and B_A
BA = -8*r**2*k**2+(r**4-18*r**2+1)*k-8*r**2
ok("eq:diff numerator bracket == B_A", sp.expand(k*(r**4-18*r**2+1)-8*r**2*(k**2+1)-BA)==0)
ok("A - A(0) = k*B_A/den", sp.simplify(A - r**2/4 - k*BA/(16*(k+1)**2*(2*k+1)))==0)
ok("disc_A factorization", sp.factor(sp.expand((r**4-18*r**2+1)**2-4*64*r**4)) == sp.factor((r**2-1)**2*(r**4-34*r**2+1)))

# --- tangency eq:tangency at r = 3+2sqrt2
rA = 3+2*sp.sqrt(2); rD = 2+sp.sqrt(3)
ok("B_A(kappa;rA) = -8 rA^2 (k-1)^2", sp.simplify(sp.expand(BA.subs(r,rA)) - sp.expand(-8*rA**2*(k-1)**2))==0)

# --- Table invariants
ok("s(rA)=6", sp.simplify(rA+1/rA-6)==0)
ok("s(rD)=4", sp.simplify(rD+1/rD-4)==0)
ok("w(rA^2)=34", sp.simplify(rA**2+1/rA**2-34)==0)
ok("w(rD^2)=14", sp.simplify(rD**2+1/rD**2-14)==0)
ok("w(r^2)=s(r)^2-2", sp.simplify((r**2+1/r**2)-((r+1/r)**2-2))==0)
ok("rA num", abs(float(rA)-5.82843)<1e-5); ok("rD num", abs(float(rD)-3.73205)<1e-5)
ok("disc factor r^4-34r^2+1 == t^2-34t+1", sp.simplify((r**4-34*r**2+1).subs(r**2,t) - (t**2-34*t+1))==0 or sp.expand((t**2-34*t+1).subs(t,r**2)-(r**4-34*r**2+1))==0)

# --- covariance at kappa=1 (equal relaxation, s1=1,s2=r): use general Prop 2
D_ = a1**2*a2+a1**2*k+a1*a2**2+4*a1*a2*k+2*a1*k**2+a2**2*k+2*a2*k**2
Sxx=(a1*a2*s1**2+a1*k*s1**2+a2**2*s1**2+3*a2*k*s1**2+k**2*s1**2+k**2*s2**2)/(2*D_)
Syy=(a1**2*s2**2+a1*a2*s2**2+3*a1*k*s2**2+a2*k*s2**2+k**2*s1**2+k**2*s2**2)/(2*D_)
Sxy=(k*(a1*s2**2+a2*s1**2+k*s1**2+k*s2**2))/(2*D_)
sub={a1:1,a2:1,s1:1,s2:r}
Sig=sp.Matrix([[Sxx,Sxy],[Sxy,Syy]]).subs(sub)
M=sp.Matrix([[-(1+k),k],[k,-(1+k)]]); Q=sp.diag(1,r**2)
ok("general Sigma solves Lyapunov (equal-relax)", sp.simplify(M*Sig+Sig*M.T+Q)==sp.zeros(2,2))
ok("det Sigma == A", sp.simplify(sp.together(Sig.det()-A))==0)
# eqs (36)-(38)
ok("eq:sxx2", sp.simplify(Sig[0,0]-(k**2*r**2+k**2+4*k+2)/(4*(2*k**2+3*k+1)))==0)
ok("eq:syy2", sp.simplify(Sig[1,1]-(k**2*r**2+k**2+4*k*r**2+2*r**2)/(4*(2*k**2+3*k+1)))==0)
ok("eq:sxy2", sp.simplify(Sig[0,1]-k*(r**2+1)/(4*(2*k+1)))==0)

S1=Sig.subs(k,1)
ok("tr Sigma(1)=(1+r^2)/3", sp.simplify(sp.trace(S1)-(1+r**2)/3)==0)
ok("det Sigma(1)=(r^4+14r^2+1)/192", sp.simplify(S1.det()-(r**4+14*r**2+1)/192)==0)
J2 = sp.trace(S1)**2/S1.det()
sv=sp.symbols('sv',positive=True)
ok("eq:mergerinv J2 = (64/3)s^2/(s^2+12)", sp.simplify(J2 - (sp.Rational(64,3)*(r+1/r)**2/((r+1/r)**2+12)))==0)
ok("J2 at rA = 16", sp.simplify(J2.subs(r,rA)-16)==0)
ev=sorted(S1.subs(r,rA).eigenvals().keys(), key=lambda z: float(z))
qq=sp.simplify(ev[1]/ev[0])
ok("eigenvalue ratio = 7+4sqrt3", sp.simplify(qq-(7+4*sp.sqrt(3)))==0)
ok("7+4sqrt3 = rD^2", sp.simplify(rD**2-(7+4*sp.sqrt(3)))==0)
ok("q+1/q=14", sp.simplify(qq+1/qq-14)==0)
ok("rapidity: log(rD)=arcosh 2", abs(float(sp.log(rD))-float(sp.acosh(2)))<1e-12)
ok("J2 = s(q)+2", sp.simplify(J2.subs(r,rA)-(qq+1/qq+2))==0)
ok("(tr)^2-4det = 12 det at merger", sp.simplify((sp.trace(S1)**2-4*S1.det()).subs(r,rA)-12*S1.det().subs(r,rA))==0)

# --- residual variance
Dres = sp.simplify(Sig.det()/Sig[1,1])
ok("D(0)=1/2", sp.simplify(Dres.subs(k,0)-sp.Rational(1,2))==0)
BD = -2*(r**2+1)*k**2+(r**4-8*r**2-1)*k-4*r**2
ok("eq:Ddiff", sp.simplify(Dres-sp.Rational(1,2)-k*BD/(4*(k+1)*(k**2*r**2+k**2+4*k*r**2+2*r**2)))==0)
ok("disc_D factorization", sp.expand((r**4-8*r**2-1)**2-4*2*(r**2+1)*4*r**2 - (r**2-1)**2*(r**2-4*r+1)*(r**2+4*r+1))==0)
ok("residual crossing product = 2r^2/(r^2+1)", sp.simplify(sp.Rational(-4,1)*r**2/(-2*(r**2+1)) - 2*r**2/(r**2+1))==0)

# --- rho^2 and monotonicity
rho2 = sp.simplify(Sig[0,1]**2/(Sig[0,0]*Sig[1,1]))
ok("eq:rho2", sp.simplify(rho2 - k**2*(k+1)**2*(r**2+1)**2/((k**2*r**2+k**2+4*k+2)*(k**2*r**2+k**2+4*k*r**2+2*r**2)))==0)
P = k**4*(r**2+1)**2+16*k**3*r**2+24*k**2*r**2+16*k*r**2+4*r**2
ok("eq:drho", sp.simplify(sp.diff(rho2,k) - 2*k*(k+1)*(r**2+1)**2*P/((k**2*r**2+k**2+4*k+2)**2*(k**2*r**2+k**2+4*k*r**2+2*r**2)**2))==0)

# --- A'(0) general, eq:Aprime
Ag = sp.simplify(sp.Matrix([[Sxx,Sxy],[Sxy,Syy]]).det())
ok("A(0) general", sp.simplify(Ag.subs(k,0)-s1**2*s2**2/(4*a1*a2))==0)
ok("A'(0) general", sp.simplify(sp.diff(Ag,k).subs(k,0)+s1**2*s2**2*(a1+a2)/(4*a1**2*a2**2))==0)
# eq:Ageneral matches
Agen=(a1**2*s1**2*s2**2+2*a1*a2*s1**2*s2**2+4*a1*k*s1**2*s2**2+a2**2*s1**2*s2**2+4*a2*k*s1**2*s2**2+k**2*s1**4+2*k**2*s1**2*s2**2+k**2*s2**4)/(4*(a1+a2+2*k)**2*(a1*a2+a1*k+a2*k))
ok("eq:Ageneral", sp.simplify(Ag-Agen)==0)

# --- asymptotics
ok("1-rho^2 ~ 2/k", sp.simplify(sp.limit((1-rho2)*k,k,sp.oo)-2)==0)
ok("D ~ (r^2+1)/(4k)", sp.simplify(sp.limit(Dres*k,k,sp.oo)-(r**2+1)/4)==0)
ok("A ~ (r^2+1)^2/(32k)", sp.simplify(sp.limit(A*k,k,sp.oo)-(r**2+1)**2/32)==0)
ok("Sigma -> (r^2+1)/8", all(sp.simplify(sp.limit(Sig[i,j],k,sp.oo)-(r**2+1)/8)==0 for i in range(2) for j in range(2)))

# --- numerical example r=10
A10=A.subs(r,10); roots=sp.solve(sp.Eq(A10, sp.Rational(25,1)),k); rts=sorted([float(x) for x in roots if x.is_real and x>0])
ok("kappa1,kappa2 for r=10", abs(rts[0]-0.0984954)<1e-6 and abs(rts[1]-10.1527546)<1e-6 and abs(rts[0]*rts[1]-1)<1e-9)
kstar=[x for x in sp.nroots(sp.Poly(sp.expand(sp.numer(sp.simplify(sp.together(sp.diff(A10,k))))),k)) if x.is_real and x>0]; ks=float(max(kstar))
ok("kappa* = 1.41819", abs(ks-1.41819)<1e-5)
ok("A(k*)/A(0) = 2.4574", abs(float(A10.subs(k,ks))/25-2.4574)<1e-4)
# table
import math
rows=[(0,0.0,0.0,0.5,1.0),(0.5,0.6792,0.3093,1.3131,1.8613),(1.0,0.7376,0.3926,2.0330,2.3752),
      (1.41819,0.7658,0.4415,2.3493,2.4574),(2.0,0.7949,0.4996,2.5406,2.3780),
      (5.0,0.8734,0.7196,2.2877,1.6378),(10.0,0.9225,0.9522,1.6346,1.0119),(100,0.9903,1.9728,0.2406,0.1245)]
bad=[]
for kv,rh,Cv,Dv,Av in rows:
    rh_=math.sqrt(float(rho2.subs({r:10,k:kv}))); C_=-0.5*math.log(1-rh_**2); D_v=float(Dres.subs({r:10,k:kv})); A_=float(A10.subs(k,kv))/25
    for nm,got,exp in (("rho",rh_,rh),("C",C_,Cv),("D",D_v,Dv),("A",A_,Av)):
        if abs(got-exp)>6e-5: bad.append((kv,nm,got,exp))
ok("Table 2 (all 32 entries)", not bad)
if bad: print("   ",bad)

# --- n>=3 counterexample
import itertools
sp1=(1,8,12); sp2=(2,3,16)
ok("counterexample (1,8,12) vs (2,3,16)", sum(sp1)==sum(sp2)==21 and sp1[0]*sp1[1]*sp1[2]==sp2[0]*sp2[1]*sp2[2]==96 and max(sp1)/min(sp1)==12 and max(sp2)/min(sp2)==8)
