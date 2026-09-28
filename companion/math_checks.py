"""Direct finite checks, independent of the polynomial certificate encodings."""
from collections import Counter
from fractions import Fraction as F
from math import comb, gcd
from band_check import require

def cb(n,k):
    return comb(n,k) if 0 <= k <= n else 0

def covariance(N,q,k):
    carrier=[h for h in range(1,N) if gcd(h,10)==1]
    m=len(carrier); Z=cb(m,k)
    rows=Counter(h%3 for h in carrier)
    cols=Counter(h%q for h in carrier)
    cells=Counter((h%3,h%q) for h in carrier)
    return F(sum(Z*cb(m-rho-j+cells[r,c],k)-cb(m-rho,k)*cb(m-j,k)
                 for r,rho in rows.items() for c,j in cols.items()), Z*Z)

def matching(N,q,k):
    m=2*N//5; a=(m-4)//3; s=2*a+4; b=s-2
    pairs=[(h,h+2*q) for h in range(1,N-2*q) if gcd(h*(N-2*q-h),10)==1]
    M=len(pairs); gamma=sum(x%3==2 for e in pairs for x in e)
    T=m*(m-1); B=b*(b-1); S=s*(s-1)
    L=T*gamma-2*M*B; V=M*(T-S)-T*gamma
    return F(k*(k-1)*cb(s,k)*(L*(s-k)*(s-k-1)+B*V),cb(m,k)*S*T*B)

def sign_prediction(N,q,k):
    m=2*N//5; a=(m-4)//3; s=2*a+4
    if q==1 or 2*q>=N or k<2 or k>s:return 0
    g=N//2-q; X=(s-k)*(s-k-1)
    if g in (1,3): p=a*(5*a+7)-2*X
    elif g==7:p=(2*a+1)*(7*a*a-7*a-24)-(11*a-2)*X
    elif g==19 and N>=1000:p=(2*a+1)*(a*a-49*a-72)-(17*a-14)*X
    else:return -1
    return (p>0)-(p<0)

def check_all():
    count=match=0
    for N,qs,ks in (
        (100,[q for q in range(1,102) if gcd(q,30)==1],range(41)),
        (1000,[7,31,127,251,269,419,461,479,481,491,493,497,499,503],
         (0,1,2,3,10,132,269,270,271,272,273,400)),
    ):
        for q in qs:
            for k in ks:
                c=covariance(N,q,k)
                require((c>0)-(c<0)==sign_prediction(N,q,k),"Theorem finite sign check")
                if N<=4*q and 2*q<N and 2<=k<=2*((2*N//5-4)//3)+4:
                    require(c==matching(N,q,k),"Matching identity")
                    match+=1
                count+=1
    # The period table is reconstructed from the actual pair definition.
    base=((2,1,0),(6,1,0),(14,5,2),(18,5,4),(26,7,4),(38,11,6),(42,13,8),(54,17,12))
    for t0,M0,g0 in base:
        for j in range(4):
            t=t0+60*j
            # N=1000 has the fixed required residue 10 mod 30.
            q=(1000-t)//2
            pairs=[(h,h+2*q) for h in range(1,t) if gcd(h*(t-h),10)==1]
            require(len(pairs)==M0+18*j,"Matching period")
            require(sum(x%3==2 for e in pairs for x in e)==g0+12*j,"Row-2 period")
    require(covariance(100,47,8)==F(1771,20974005),"Positive example")
    require(covariance(100,41,15)==-F(51037,134914728),"Negative same-marginal example")
    require(covariance(100,43,15)==F(161,10939032),"Positive same-marginal example")
    # A columnwise counterexample, not a complete partition counterexample.
    from urn_check import empty_sum
    a=64; k=16; rho=(a+2,a+2,a); v=(4,4,6); m=sum(rho)
    contribution=F(cb(m-sum(v),k),cb(m,k))*(empty_sum([rho[i]-v[i] for i in range(3)],k)-empty_sum(rho,k))
    require(contribution==F(330853998011097173518286137,7117411572795499416494730628648788),
            "Oriented column obstruction")
    require(empty_sum((2,6,6),2)-empty_sum((1,5,5),2)==-F(23,1001),
            "Unrestricted urn increment fails")
    return dict(status="PASS",finite_sign_checks=count,matching_identity_checks=match,
                matching_period_rows=32,adverse_controls=5)

