"""Helpers for the CBSE class 12 maths (041) and applied maths (241) family modules.

Re-exports the class 9/10 helpers (Q, mcqbank, arbank, xbank, fn, poly ...) and adds matrices,
vectors, multiples of π, LPP corner points and exact probability helpers.
"""
from __future__ import annotations

import itertools
import math
from fractions import Fraction as Fr

from qbank import ar, mcq, num, frac, name, two_names, inr, num_distractors, CITIES, GIRLS, BOYS  # noqa: F401
from g9_maths_h import Q, mcqbank, arbank, xbank, fn, poly, term, rad, P, nz, signed, bracket, is_sq  # noqa: F401


def pick(r, xs):
    return r.choice(xs)


def fz(x) -> str:
    """Fraction/int to text (true minus)."""
    return fn(Fr(x))


def fpar(x) -> str:
    """Fraction in brackets when negative or fractional, for products such as 3 × (−2)."""
    x = Fr(x)
    s = fn(x)
    return f'({s})' if (x < 0 or x.denominator != 1) else s


def dist3(ans: str, cands) -> list:
    out = []
    for c in cands:
        c = str(c)
        if c != ans and c not in out:
            out.append(c)
    return out


# ---------------- multiples of π

def pif(x) -> str:
    """Fraction of π to text: Fr(1,6) -> π/6, Fr(-2,3) -> −2π/3, 0 -> 0."""
    x = Fr(x)
    if x == 0:
        return '0'
    s = '−' if x < 0 else ''
    x = abs(x)
    n, d = x.numerator, x.denominator
    top = 'π' if n == 1 else f'{n}π'
    return s + (top if d == 1 else f'{top}/{d}')


# ---------------- matrices (lists of rows, entries int or Fraction)

def mstr(M) -> str:
    return '[' + '; '.join(', '.join(fz(x) for x in row) for row in M) + ']'


def mmul(A, B):
    return [[sum(Fr(A[i][k]) * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def madd(A, B, a=1, b=1):
    return [[a * Fr(x) + b * Fr(y) for x, y in zip(ra, rb)] for ra, rb in zip(A, B)]


def mscale(A, k):
    return [[k * Fr(x) for x in row] for row in A]


def tr(A):
    return [list(c) for c in zip(*A)]


def eye(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def det(A):
    n = len(A)
    if n == 1:
        return Fr(A[0][0])
    if n == 2:
        return Fr(A[0][0]) * A[1][1] - Fr(A[0][1]) * A[1][0]
    return sum((-1) ** j * Fr(A[0][j]) * det(minor_m(A, 0, j)) for j in range(n))


def minor_m(A, i, j):
    return [row[:j] + row[j + 1:] for k, row in enumerate(A) if k != i]


def cof(A, i, j):
    return (-1) ** (i + j) * det(minor_m(A, i, j))


def adj(A):
    n = len(A)
    if n == 2:
        return [[A[1][1], -A[0][1]], [-A[1][0], A[0][0]]]
    return tr([[cof(A, i, j) for j in range(n)] for i in range(n)])


def inv(A):
    d = det(A)
    return mscale(adj(A), Fr(1) / d)


def rand_mat(r, n, m=None, lo=-5, hi=6, nonsing=False):
    m = m or n
    while True:
        A = [[r.randint(lo, hi - 1) for _ in range(m)] for _ in range(n)]
        if not nonsing or (n == m and det(A) != 0):
            return A


def unimod(r, n=3, dets=(1, -1, 2, -2, 3, -3)):
    """Random small integer n×n matrix with |det| small so inverses stay tidy."""
    while True:
        A = [[r.randint(-3, 4) for _ in range(n)] for _ in range(n)]
        if det(A) in dets and sum(1 for row in A for x in row if x == 0) <= 3:
            return A


def lin_eq(coeffs, rhs, vars_='xyz') -> str:
    s = ''
    for c, v in zip(coeffs, vars_):
        s += term(c, v, first=(s == ''))
    return f'{s or "0"} = {fz(rhs)}'


# ---------------- vectors

def vstr(v, names=('î', 'ĵ', 'k̂')) -> str:
    s = ''
    for c, e in zip(v, names):
        c = Fr(c)
        if c == 0:
            continue
        co = '' if abs(c) == 1 else (f'({fn(abs(c))})' if c.denominator != 1 else fn(abs(c)))
        if s == '':
            s = ('−' if c < 0 else '') + co + e
        else:
            s += (' − ' if c < 0 else ' + ') + co + e
    return s or '0⃗'


def dot(a, b):
    return sum(Fr(x) * y for x, y in zip(a, b))


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def sq(a):
    return sum(Fr(x) * x for x in a)


def surd(n2) -> str:
    """√ of a non-negative Fraction in simplest form, e.g. 8 -> 2√2, 9/4 -> 3/2, 3/4 -> √3/2."""
    n2 = Fr(n2)
    if n2 == 0:
        return '0'
    p, q = n2.numerator, n2.denominator
    # √(p/q) = √(pq)/q
    a, b = _sqf(p * q)
    coef = Fr(a, q)
    if b == 1:
        return fn(coef)
    top = ('' if coef.numerator == 1 else str(coef.numerator)) + f'√{b}'
    return top if coef.denominator == 1 else f'{top}/{coef.denominator}'


def _sqf(n):
    a, b, k = 1, n, 2
    while k * k <= b:
        while b % (k * k) == 0:
            b //= k * k
            a *= k
        k += 1
    return a, b


def gcdl(xs):
    g = 0
    for x in xs:
        g = math.gcd(g, int(x))
    return g or 1


def prim(v):
    """Integer vector divided by the gcd of its entries (sign kept)."""
    g = gcdl(v)
    return [x // g for x in v]


# ---------------- LPP

def lpp_vertices(cons):
    """cons: list of (a, b, c, sense) meaning a x + b y (≤ or ≥) c, sense in {'<=', '>='}. x, y ≥ 0 added.
    Returns the sorted list of feasible corner points (Fractions)."""
    lines = [(a, b, c) for a, b, c, _ in cons] + [(1, 0, 0), (0, 1, 0)]
    pts = set()
    for (a1, b1, c1), (a2, b2, c2) in itertools.combinations(lines, 2):
        d = a1 * b2 - a2 * b1
        if d == 0:
            continue
        x = Fr(c1 * b2 - c2 * b1, d)
        y = Fr(a1 * c2 - a2 * c1, d)
        if x < 0 or y < 0:
            continue
        ok = True
        for a, b, c, s in cons:
            v = a * x + b * y
            if (s == '<=' and v > c) or (s == '>=' and v < c):
                ok = False
                break
        if ok:
            pts.add((x, y))
    return sorted(pts)


def cons_str(a, b, c, s, x='x', y='y'):
    lhs = term(a, x, first=True) + term(b, y) if a else term(b, y, first=True)
    return f'{lhs} {"≤" if s == "<=" else "≥"} {fz(c)}'


# ---------------- probability

def pf(x) -> str:
    x = Fr(x)
    return fn(x)


def binom(n, k):
    return math.comb(n, k)


# ---------------- final text clean-up (run after polish)

import re as _re

_TIDY = [
    (_re.compile(r'(?<![A-Za-z\d])-(?=\d)'), '−'),                     # hyphen-minus before a digit
    (_re.compile(r'\+ −'), '− '),                                        # a + −b  ->  a − b
    (_re.compile(r'− −'), '+ '),                                         # a − −b  ->  a + b
    (_re.compile(r'(?<![\d.,/^])\b1(?=[a-zθ](?![a-zA-Z]))'), ''),        # 1x -> x, −1k -> −k
    (_re.compile(r'(?<=[=+−(] )1 (?=(?:cos|sin|tan|sec|log)\b)'), ''),  # = 1 cos 4x -> = cos 4x
    (_re.compile(r'√\(([a-z])\)'), r'√\1'),                              # √(x) -> √x
    (_re.compile(r'(?<![\d.,/])\b1 sq units'), '1 sq unit'),
    (_re.compile(r'(?<![\w(/^.])(\d+/\d+)(?=[a-zA-Zπ(îĵ])'), r'(\1)'),       # 1/5P -> (1/5)P, 25/4(π − 2) -> (25/4)(π − 2)
    (_re.compile(r'(?<=[−+] )1\((?=[a-z])'), '('),                        # − 1(y + x dy/dx) -> − (y + …)
    (_re.compile(r'(?<![\d.,/₹])\b1 (year|month|day|hour|order|file|apple|banana|orange|pen|pencil|notebook|book|chair|table|unit|item|article|toy)s\b'),
     r'1 \1'),                                                                # 1 years -> 1 year
    (_re.compile(r'\(1/−(\d+)\)'), r'−(1/\1)'),                                # (1/−6) -> −(1/6)
    (_re.compile(r'(?<=\))/1(?![\d.,/])'), ''),                                 # (5I − A)/1 -> (5I − A)
    (_re.compile(r' \+ 0(?=$|[;,)])'), ''),                                      # y² = x² + 0 -> y² = x²
    (_re.compile(r'subtract \(−(\d+(?:/\d+)?)\)'), r'add \1'),                  # subtract (−6) -> add 6
]


def tidy_text(s: str) -> str:
    for p, rep in _TIDY:
        s = p.sub(rep, s)
    return s


def tidy(files: dict) -> None:
    """Sign and unit-coefficient clean-up on every stem, answer, key and option."""
    for items in files.values():
        for q in items:
            for k in ('stem', 'answer', 'markingKey'):
                if isinstance(q.get(k), str):
                    q[k] = tidy_text(q[k])
            if isinstance(q.get('options'), list):
                q['options'] = [tidy_text(o) if isinstance(o, str) else o for o in q['options']]
