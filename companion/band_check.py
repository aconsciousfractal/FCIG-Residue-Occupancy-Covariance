"""Standalone verifier for the whole delivered block, Python standard library.

For each band, reconstruct the geometry directly from odd residues. Check the
raw identity on a rational interpolation grid whose size follows from J,D.
No import of the generator, polynomial algebra, or other numerical modules.
Also prove the remaining depth-two instances by direct exact finite sums.
"""
import hashlib
import json
from collections import Counter, defaultdict
from fractions import Fraction as F
from math import comb, gcd, prod
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESIDUES = tuple(u for u in range(30) if gcd(u, 30) == 1)


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def evaluate(coefficients, value):
    result = 0
    for c in reversed(coefficients):
        result = result*value+c
    return result


def geometry(ell, residue):
    out = defaultdict(lambda: [0, 0, 0])
    for r in range(1, 30, 2):
        t0, b0 = (10-2*(ell-1)*residue) % 30, 2*residue % 30
        for length in (ell-1, ell):
            v = [0, 0, 0]
            # Deliberately enumerate every lift, without the 15-cycle shortcut.
            for j in range(length):
                h = r+2*j*residue
                if gcd(h, 10) == 1:
                    v[h % 3] += 1
            if length == ell:
                cs = [1, -2*(ell-1), -t0+30*int(r < t0)]
            else:
                cs = [-1, 2*ell, t0-b0+30*(int(r < b0)-int(r < t0))]
            for i, c in enumerate(cs):
                out[tuple(v)][i] += c
    return {v: tuple(cs) for v, cs in out.items()}


def kernel_values(a, x, vectors, J, D):
    m, s = 3*a+4, 2*a+4
    k = 2+(s-2)*x
    fs, fm = [F(1)], [F(1)]
    for i in range(D):
        fs.append(fs[-1]*(s-k-i))
    for i in range(J):
        fm.append(fm[-1]*(m-k-i))
    row = [prod(m-i for i in range(J))*fs[delta]*prod(s-i for i in range(delta, D))
           for delta in range(D+1)]
    column = [prod(s-i for i in range(2, D))*(s*(s-1)+2*fs[2])
              * fm[j]*prod(m-i for i in range(j, J)) for j in range(J+1)]
    return {v: sum(row[sum(v)-v[r]+(2 if r < 2 else 0)] for r in range(3))-column[sum(v)]
            for v in vectors}


def check_one(path, expected_ell):
    cert = json.loads(path.read_text())
    ell = cert["ell"]
    require(ell == expected_ell and cert["schema"] == "p71-band-certificate-v1", "Certificate identity")
    tables = {u: geometry(ell, u) for u in RESIDUES}
    vectors = tuple(sorted(set().union(*tables.values())))
    J = max(map(sum, vectors))
    D = max(sum(v)-v[r]+(2 if r < 2 else 0) for v in vectors for r in range(3))
    require((cert["J"], cert["D"], cert["bernstein_degree"], cert["coefficient_degree"])
            == (J, D, J, J+D-1), "Derived degree bounds")
    shift, scale = cert["shift"], cert["scale"]
    require(shift == 132 and type(scale) is int and scale > 0, "Certified domain and scale")
    require(D <= 2*shift+4 and J <= 3*shift+4, "Positive common denominator")
    require(cert["vectors"] == [list(v) for v in vectors], "Full type alphabet")
    require(cert["endpoint_denominators"] == [2*ell, 2*(ell-1)], "Band endpoints")
    for entry in cert["affine_types"]:
        u = entry["residue"]
        stored = {tuple(e["vector"]): (e["A"], e["B"], e["C"]) for e in entry["entries"]}
        require(stored == tables[u] and len(entry["entries"]) == len(stored), "Affine multiplicities")
    require({e["residue"] for e in cert["affine_types"]} == set(RESIDUES)
            and len(cert["affine_types"]) == 8, "Every residue table")
    expected = {(u, den, i) for u in RESIDUES for den in (2*ell, 2*(ell-1)) for i in range(J+1)}
    cases = {(c["residue"], c["endpoint_denominator"], c["bernstein_index"]):
             c["negative_scaled_B_at_shift_plus_y"] for c in cert["cases"]}
    require(set(cases) == expected and len(cert["cases"]) == len(expected), "Every Bernstein coefficient")
    for coefficients in cases.values():
        require(len(coefficients) == J+D and all(type(n) is int and n >= 0 for n in coefficients)
                and coefficients[0] > 0, "Coefficientwise strict negativity on a>=132")
    # Raw total degree <= J+D+1, degree in x <= J+2.
    # Thus J+D+2 values of a and J+3 values of x prove the full identity.
    xs = [F(j, J+2) for j in range(J+3)]
    bases = [[comb(J, i)*x**i*(1-x)**(J-i) for i in range(J+1)] for x in xs]
    stream = hashlib.sha256()
    equalities = 0
    for a in range(shift, shift+J+D+2):
        N = F(15*a+20, 2)
        weights = {(u, den): {v: A*N+B*N/den+C for v, (A, B, C) in table.items()}
                   for u, table in tables.items() for den in (2*ell, 2*(ell-1))}
        Bs = {(u, den): [-F(evaluate(cases[u, den, i], a-shift), scale) for i in range(J+1)]
              for u in RESIDUES for den in (2*ell, 2*(ell-1))}
        for x_index, (x, basis) in enumerate(zip(xs, bases)):
            k = 2+(2*a+2)*x
            kernels = kernel_values(a, x, vectors, J, D)
            for u, den in weights:
                left = sum(c*kernels[v] for v, c in weights[u, den].items())
                right = k*(k-1)*sum(B*b for B, b in zip(Bs[u, den], basis))
                require(left == right, f"Exact identity {ell},{u},{den},{a},{x_index}")
                stream.update(f"{ell}|{u}|{den}|{a}|{x_index}|{left.numerator}|{left.denominator}\n".encode())
                equalities += 1
    return dict(ell=ell, vectors=len(vectors), J=J, D=D, bernstein_coefficients=len(cases),
                integer_coefficients=sum(map(len, cases.values())),
                strictly_positive_integer_coefficients=sum(n > 0 for cs in cases.values() for n in cs),
                grid_shape=[J+D+2, J+3], exact_grid_equalities=equalities,
                identity_values_sha256=stream.hexdigest(),
                certificate_sha256=hashlib.sha256(path.read_bytes()).hexdigest())


def small_depth():
    carrier = [h for h in range(1, 100) if gcd(h, 10) == 1]
    m, s = 40, 28
    records, checked = [], 0
    for q in range(4, 25):
        if gcd(q, 30) != 1:
            continue
        cells = Counter((h % 3, h % q) for h in carrier)
        rows = Counter(h % 3 for h in carrier)
        cols = Counter(h % q for h in carrier)
        values = []
        for k in range(m+1):
            Z = comb(m, k)
            def C(n):
                return comb(n, k) if n >= k else 0
            numerator = sum(Z*C(m-nr-nc+cells[r, c])-C(m-nr)*C(m-nc)
                            for r, nr in rows.items() for c, nc in cols.items())
            cov = F(numerator, Z*Z)
            require(cov < 0 if 2 <= k <= s else cov == 0, f"Depth-two sign q={q}, k={k}")
            values.append(dict(k=k, numerator=cov.numerator, denominator=cov.denominator))
            checked += 1
        records.append(dict(N=100, q=q, covariances=values))
    require(records == json.loads((ROOT/"certificates/depth2.json").read_text()), "Every depth-two exact fraction")
    return checked


def check_all():
    receipts = []
    for ell in range(3, 17):
        receipt = check_one(ROOT/f"certificates/band_{ell:02d}.json", ell)
        receipts.append(receipt)

    small = small_depth()
    result = dict(status="PASS", checker="standalone exact rational interpolation",
                  uniform_domain="d>=3, N/32<=q<N/4, gcd(q,30)=1",
                  small_depth_domain="d=2, q=7,11,13,17,19,23; all 41 cardinalities",
                  bands=receipts, small_depth_equalities=small,
                  total_grid_equalities=sum(r["exact_grid_equalities"] for r in receipts),
                  total_bernstein_coefficients=sum(r["bernstein_coefficients"] for r in receipts),
                  total_integer_coefficients=sum(r["integer_coefficients"] for r in receipts),
                  statement="Written proof plus exact finite certificates; no proof-assistant formalization.")
    return result
