"""Small helpers shared by the CBSE class 9 and class 10 maths family modules."""
from __future__ import annotations

import math
import re
from fractions import Fraction as Fr

from qbank import ar, mcq, num, frac, name, two_names, inr, num_distractors  # noqa: F401

PI = Fr(22, 7)


def Q(stem, answer, key, dist=None, **kw) -> dict:
    v = {'stem': stem, 'answer': str(answer), 'key': key}
    if dist:
        v['distractors'] = [str(x) for x in dist]
    v.update(kw)
    return v


def mcqbank(items):
    """items: (stem, correct, [three wrong], key)."""
    def g(r):
        s, c, w, k = r.choice(items)
        return mcq(s, c, w, k, r)
    return g


def arbank(items):
    """items: (assertion, reason, code, why)."""
    def g(r):
        return ar(*r.choice(items))
    return g


def xbank(items):
    """items: (stem, answer, key) for explain-type fact items."""
    def g(r):
        s, a, k = r.choice(items)
        return Q(s, a, k)
    return g


def P(x, y) -> str:
    return f'({fn(x)}, {fn(y)})'


def fn(x) -> str:
    """Number or Fraction to text with true minus sign."""
    if isinstance(x, Fr):
        if x.denominator == 1:
            return num(x.numerator)
        return frac(x.numerator, x.denominator)
    return num(x)


def rad(n: int) -> str:
    """Simplest surd form of √n."""
    if n == 0:
        return '0'
    a, b = 1, n
    k = 2
    while k * k <= b:
        while b % (k * k) == 0:
            b //= k * k
            a *= k
        k += 1
    if b == 1:
        return str(a)
    return ('' if a == 1 else str(a)) + '√' + str(b)


def is_sq(n: int) -> bool:
    return n >= 0 and math.isqrt(n) ** 2 == n


def term(c, var='', first=False, power=1) -> str:
    """One signed term of a polynomial, e.g. term(-3,'x',power=2) -> ' − 3x²'."""
    if c == 0:
        return ''
    sgn = '−' if c < 0 else '+'
    a = abs(c)
    v = ''
    if var:
        v = var + ('' if power == 1 else {2: '²', 3: '³', 4: '⁴'}.get(power, f'^{power}'))
    co = fn(a) if (a != 1 or not var) else ''
    body = co + v
    if first:
        return ('−' if c < 0 else '') + body
    return f' {sgn} {body}'


def poly(coeffs, var='x') -> str:
    """coeffs from highest power: poly([2,-3,1]) -> '2x² − 3x + 1'."""
    n = len(coeffs) - 1
    out = ''
    for i, c in enumerate(coeffs):
        p = n - i
        t = term(c, var if p > 0 else '', first=(out == ''), power=max(p, 1))
        out += t
    return out or '0'


def lin(a, b, var='x') -> str:
    return poly([a, b], var)


def eq2(a, b, c, x='x', y='y') -> str:
    """a x + b y = c."""
    lhs = term(a, x, first=True) + term(b, y)
    return f'{lhs} = {fn(c)}'


def signed(n) -> str:
    return f'+ {fn(n)}' if n >= 0 else f'− {fn(-n)}'


def bracket(n) -> str:
    return f'({fn(n)})' if n < 0 else fn(n)


TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (6, 8, 10), (9, 12, 15), (20, 21, 29), (9, 40, 41), (12, 16, 20), (12, 35, 37)]


def triple(r):
    a, b, c = r.choice(TRIPLES)
    if r.random() < 0.5:
        a, b = b, a
    return a, b, c


def ordinal(n: int) -> str:
    if 10 <= n % 100 <= 20:
        s = 'th'
    else:
        s = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f'{n}{s}'


def pistr(x: Fr) -> str:
    """Value computed with π = 22/7, as a decimal when it terminates, else a fraction."""
    x = Fr(x)
    if x.denominator == 1:
        return num(x.numerator)
    d = x.denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    if d == 1:
        return num(float(x), 4)
    return f'{frac(x.numerator, x.denominator)} (≈ {num(round(float(x), 2))})'


def nz(r, lo=1, hi=9):
    """Random non-zero integer in ±[lo, hi]."""
    return r.choice([-1, 1]) * r.randint(lo, hi)


_MINUS = re.compile(r'(?<=[\s(=,\[:;/×])-(?=\d)|^-(?=\d)')
_MK = re.compile(r'(\d+) marks?\b(?! each)')


def _fix_marks(key: str, marks) -> str:
    nums = [int(n) for n in _MK.findall(key)]
    if not nums or sum(nums) == marks or (len(nums) == 1 and nums[0] == marks):
        return key
    k = re.sub(r'^(\d+) marks?\.$', '', key.strip())
    if not k:
        return ''
    k = re.sub(r'\s*\((\d+) marks?\)', '', k)
    k = re.sub(r'\((\d+) marks?[:;,]\s*', '(', k)
    k = re.sub(r'(\d+) marks?[:;,]\s*', '', k)
    return k.strip()


def polish(files: dict) -> None:
    """Final text clean-up on built items: true minus signs and mark totals that match the item's marks."""
    for items in files.values():
        for q in items:
            for f in ('stem', 'answer', 'markingKey'):
                q[f] = _MINUS.sub('−', q[f])
            if q.get('options'):
                q['options'] = [_MINUS.sub('−', o) for o in q['options']]
                if q['type'] == 'mcq':
                    q['answer'] = _MINUS.sub('−', q['answer'])
            k = _fix_marks(q['markingKey'], q['marks'])
            if re.fullmatch(r'\d+ marks?\.', k.strip()):
                k = ''
            if not k:
                a = q['answer'].rstrip('.')
                k = f'Key points: {a}. Award {num(q["marks"])} mark{"s" if q["marks"] != 1 else ""} for a complete, correctly reasoned answer.'
            q['markingKey'] = k


SUB = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')


def sub(n) -> str:
    return str(n).translate(SUB)
