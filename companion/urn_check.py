"""Independent exact checker. Imports no generator or external model module.

The tensor grids certify polynomial identities using the degree bounds
proved in the companion manuscript (Lemmas 5--6 and Section 10), with
certificate roles detailed in CERTIFICATE_MAP.md. Integer signs then prove
the inequalities.
"""
from fractions import Fraction
from math import comb, prod
from itertools import product
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
ANCHORS=((4,4,4),(4,4,5),(4,5,5),(4,5,6),(4,6,6),(6,6,8))


def require(condition,message):
    if not condition:
        raise ArithmeticError(message)


def ff(z,n):
    return prod(z-i for i in range(n))


def cb(n,k):
    return comb(n,k) if 0<=k<=n else 0


def empty_sum(rows,k):
    M=sum(rows)
    require(0<=k<=M,'Invalid urn sample')
    return Fraction(sum(cb(M-r,k) for r in rows),cb(M,k))


def mono_raw(h,k,p,r):
    n,M,D=2*h+p+r,3*h+p+r,r+2
    ds=(0,p,r)
    A=sum(ff(n+2-k,d)*prod(n+2-i for i in range(d,D)) for d in ds)
    B=sum(ff(n+2-k,d+2)*prod(n+2-i for i in range(d+2,D)) for d in ds)
    return ff(M+3-k,3)*A-ff(M+3,3)*B


def anchor_raw(a,k,v):
    m,s,j=3*a+4,2*a+4,sum(v)
    ds=[j-v[r]+2*(r<2) for r in range(3)];D=max(ds)
    A=sum(ff(s-k,d)*prod(s-i for i in range(d,D)) for d in ds)
    return ff(m,j)*A-prod(s-i for i in range(2,D))*(s*(s-1)+2*ff(s-k,2))*ff(m-k,j)


def horner(row,y):
    value=0
    for c in reversed(row):value=value*y+c
    return value


def encoded_R(case,a,x):
    n=case['degree_x'];y=a-case['shift']
    return Fraction(case['sign'],case['scale'])*sum(
        horner(row,y)*comb(n,i)*x**i*(1-x)**(n-i)
        for i,row in enumerate(case['coefficients']))


def inspect_case(case,dx,da,shift,sign):
    require(case['degree_x']==dx and case['degree_parameter']==da,'Declared degrees')
    require(case['shift']==shift and case['sign']==sign,'Declared domain/sign')
    require(type(case['scale']) is int and case['scale']>0,'Positive scale')
    rows=case['coefficients']
    require(len(rows)==dx+1 and all(len(row)==da+1 for row in rows),'Array dimensions')
    require(all(type(c) is int and c>=0 for row in rows for c in row),'Nonnegative integers')
    require(all(row[0]>0 for row in rows),'Strict Bernstein constants')
    return sum(len(row) for row in rows)


def check_all():
    mono=json.loads((ROOT/'certificates/urn_monotonicity.json').read_text())
    anchors=json.loads((ROOT/'certificates/column_anchors.json').read_text())
    require(mono['schema']==anchors['schema']=='p71-uniform-padding-v1' and mono['factor']==anchors['factor']=='k(k-1)', 'Certificate schema and factor')
    require(mono['kind']=='urn-increment' and anchors['kind']=='column-anchor','Certificate kind')
    expected=[[0,p,r] for r in range(5) for p in range(r+1)]
    require([c['offsets'] for c in mono['cases']]==expected,'All fifteen urn profiles required')
    require([tuple(c['vector']) for c in anchors['cases']]==list(ANCHORS),'All six anchors required')
    ncoeff=ngrid=nhyper=0
    for case in mono['cases']:
        _,p,r=case['offsets'];require(case['D']==r+2,'Urn denominator')
        ncoeff+=inspect_case(case,r+1,r+3,16,1)
        # Raw degrees: parameter <= r+5, x <= r+3.
        for h in range(16,16+r+6):
            n=2*h+p+r
            for j in range(r+4):
                x=Fraction(j,r+3);k=2+n*x
                require(mono_raw(h,k,p,r)==k*(k-1)*encoded_R(case,h,x),'Urn polynomial identity')
                ngrid+=1
        for h in (16,17,20):
            rows=[h,h+p,h+r];M=sum(rows);n=M-h;D=r+2
            for k in range(2,n+3):
                diff=empty_sum([x+1 for x in rows],k)-empty_sum(rows,k)
                raw=mono_raw(h,k,p,r)
                value=Fraction(cb(n+2,k),cb(M+3,k))*Fraction(raw,ff(n+2,D)*ff(M+3-k,3))
                require(diff==value and diff>0,'Direct urn probability identity')
                nhyper+=1
    for case in anchors['cases']:
        v=tuple(case['vector']);J=sum(v);D=max(J-v[r]+2*(r<2) for r in range(3))
        require(case['J']==J and case['D']==D,'Anchor denominator')
        ncoeff+=inspect_case(case,J,J+D-2,40,-1)
        # Raw degrees: parameter <= J+D, x <= J+2.
        for a in range(40,40+J+D+1):
            for j in range(J+3):
                x=Fraction(j,J+2);k=2+(2*a+2)*x
                require(anchor_raw(a,k,v)==k*(k-1)*encoded_R(case,a,x),'Anchor polynomial identity')
                ngrid+=1
        for a in (40,41,48,64,132):
            rows=[a+2,a+2,a];m=sum(rows);s=2*a+4
            for k in (2,3,a,s-1,s):
                conditional=empty_sum([rows[i]-v[i] for i in range(3)],k)
                col=Fraction(cb(m-J,k),cb(m,k))
                actual=col*(conditional-empty_sum(rows,k))
                value=Fraction(cb(s,k),cb(m,k))*Fraction(anchor_raw(a,k,v),ff(s,D)*ff(m,J))
                require(actual==value and actual<0,'Direct anchor probability identity')
                nhyper+=1
    # All normalized columns and the majorization comparison are finite.
    major=[]
    worst={0:(0,0,0),1:(0,0,1),2:(0,1,1),3:(0,1,2),4:(0,2,2)}
    for e in product(range(3),repeat=3):
        if min(e):continue
        E=sum(e)
        w=e if e==(0,0,2) else worst[E]
        original=sorted((2-e[0],2-e[1],-e[2]))
        upper=sorted((2-w[0],2-w[1],-w[2]))
        require(sum(original)==sum(upper) and original[0]>=upper[0] and original[-1]<=upper[-1],
                'Majorization comparison')
        major.append(dict(offsets=e,worst_offsets=w,minimum_anchor=6 if e==(0,0,2) else 4))
    exceptional=[];vectors_seen=set()
    for ell in range(2,17):
        for u in (1,7,11,13,17,19,23,29):
            for start in range(1,30,2):
                for L in (ell-1,ell):
                    v=[0,0,0]
                    for i in range(L):
                        h=start+2*i*u
                        if h%5:v[h%3]+=1
                    b=min(v);e=tuple(x-b for x in v)
                    require(max(e)<=2,'Column spread')
                    vectors_seen.add(e)
                    if e==(0,0,2):
                        require(ell in (10,11) and tuple(v)==(2,2,4),'Exceptional shape restriction')
                        exceptional.append(dict(ell=ell,residue=u,start=start,length=L,vector=v))
    require(vectors_seen=={tuple(x['offsets']) for x in major},'Normalized alphabet coverage')
    require(exceptional,'Exceptional shape must occur')
    # Complete finite part of the new theorem, read as a separate certificate.
    small=json.loads((ROOT/'certificates/small_cutoffs.json').read_text())
    require([c['N'] for c in small]==[250,280],'Both small cutoffs required')
    nsmall=0
    for item in small:
        N=item['N'];q=7;m=2*N//5;a=(m-4)//3;s=2*a+4
        require(item['q']==q and item['m']==m and item['s']==s,'Small-cutoff parameters')
        C=[[0]*q for _ in range(3)]
        for h in range(1,N):
            if h%2 and h%5:C[h%3][h%q]+=1
        require(C==item['cells'],'Small-cutoff matrix')
        rho=[sum(row) for row in C]
        gamma=[sum(C[r][c] for r in range(3)) for c in range(q)]
        require(len(item['covariances'])==m+1,'All small-cutoff cardinalities required')
        for k,stored in enumerate(item['covariances']):
            Z=cb(m,k)
            raw=sum(Z*cb(m-rho[r]-gamma[c]+C[r][c],k)-cb(m-rho[r],k)*cb(m-gamma[c],k)
                    for r in range(3) for c in range(q))
            value=Fraction(raw,Z*Z)
            require(stored==[value.numerator,value.denominator],'Small-cutoff fraction')
            require(value<0 if 2<=k<=s else value==0,'Small-cutoff sign')
            nsmall+=1
    out=dict(status='PASS',urn_profiles=15,anchors=6,integer_coefficients=ncoeff,
             rational_identity_checks=ngrid,direct_probability_checks=nhyper,
             normalized_types=len(major),exceptional_occurrences=len(exceptional),
             small_cutoff_exact_checks=nsmall)
    return out
