"""Exact controls for the two deductive corollaries; no companion imports."""
from fractions import Fraction
from itertools import combinations
from math import comb
import json


def need(condition, message):
    if not condition:
        raise ArithmeticError(message)


def mul(p, q):
    result = [0] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            result[i + j] += x * y
    return result


def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def one_set_covariance(rows, v, k):
    m = sum(rows)
    j = sum(v)
    denominator = comb(m, k)
    return sum(Fraction(choose(m - rows[i] - j + v[i], k), denominator)
               - Fraction(choose(m - rows[i], k) * choose(m - j, k), denominator**2)
               for i in range(3))


def check():
    identities = []
    for gap, factor, low, divisor, quotient, remainder in [
        (7, 11**3, [-24, -7, 7], [-2, 11], [-6753, -539, 1694], -45450),
        (19, 17**3, [-72, -49, 1], [-14, 17], [-78471, -27557, 578], -1452330),
    ]:
        left = [factor * c for c in mul([1, 2], low)]
        right = mul(divisor, quotient)
        right[0] += remainder
        need(left == right, "Polynomial identity for gap " + str(gap))
        identities.append({"gap": gap, "coefficients": left})
    remainders = []
    for gap, constant, coefficient, offset, depths, cutoff in [
        (7, 45450, 11, 2, range(2, 5), 5),
        (19, 1452330, 17, 14, range(3, 6), 6),
    ]:
        for d in depths:
            a = 4 * (10**(d - 1) - 1) // 3
            divisor = coefficient * a - offset
            rem = constant % divisor
            need(rem != 0, "Divisibility obstruction")
            remainders.append({"gap": gap, "depth": d, "divisor": divisor, "remainder": rem})
        a = 4 * (10**(cutoff - 1) - 1) // 3
        need(coefficient * a - offset > constant, "Monotone cutoff")
    # Coefficient identity for9*(1+10a^2+14a), a=4*(T-1)/3.
    a = [Fraction(-4, 3), Fraction(4, 3)]
    aa = mul(a, a)
    dd = [9 * (10 * aa[i] + (14 * a[i] if i < 2 else 0)
               + (1 if i == 0 else 0)) for i in range(3)]
    need(dd == [1, -152, 160], "Remaining square-equation identity")

    rows = (42, 42, 40)
    row_of = [0]*42 + [1]*42 + [2]*40
    starts = (0, 42, 84)
    first = {start + j for start in starts for j in range(4)}
    second = {start + j for start in starts for j in range(2, 6)}
    need(len(first & second) == 6, "Genuine overlap")
    sum_u = sum_v = sum_uv = count = 0
    for pair in combinations(range(sum(rows)), 2):
        u = len({row_of[x] for x in pair})
        v = 2 * int(any(x in first for x in pair)) + 3 * int(any(x in second for x in pair))
        sum_u += u
        sum_v += v
        sum_uv += u*v
        count += 1
    direct = Fraction(sum_uv * count - sum_u * sum_v, count**2)
    expected = 5 * one_set_covariance(rows, (4, 4, 4), 2)
    need(direct == expected and direct < 0, "Weighted overlapping-set identity")
    for k in (0, 1, 85, 124):
        need(one_set_covariance(rows, (4, 4, 4), k) == 0, "Deterministic zero range")
    return dict(status="PASS",polynomial_identities=identities,divisibility_remainders=remainders,
                monotone_cutoffs_checked=2,square_equation_identity=True,
                overlapping_pair_subsets=count,overlapping_weighted_covariance=str(direct),
                deterministic_zero_controls=4,
                scope="Arithmetic and finite controls; uniform conclusions use the written proofs.")


if __name__ == "__main__":
    print(json.dumps(check(),indent=2,sort_keys=True))

