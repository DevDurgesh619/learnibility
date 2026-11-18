"""Helpers for the CBSE class 12 Applied Mathematics (241) family modules.

Re-exports the class 12 maths helpers and adds family re-use from the 041 modules (copied Family objects,
optionally filtered), time/fraction formatting and small statistics tables.
"""
from __future__ import annotations

import dataclasses
import math
from fractions import Fraction as Fr

from qbank import F, ar, mcq, num, name, two_names, inr, num_distractors, CITIES, GIRLS, BOYS  # noqa: F401
from g12_maths_h import (Q, mcqbank, arbank, xbank, fn, fz, fpar, poly, term, dist3, pick, pif, surd, binom,  # noqa: F401
                         mstr, mmul, det, inv, adj, unimod, lin_eq, rand_mat, lpp_vertices, cons_str)

M = 'cbse-g12-maths-ch'
import re as _re
TRIG = _re.compile(r'(?<![a-z])(sin|cos|tan|cot|sec|cosec)(?![a-z])|⁻¹')


def _maths_families():
    import g12_maths_a
    import g12_maths_b
    import g12_maths_c
    out = {}
    for m in (g12_maths_a, g12_maths_b, g12_maths_c):
        out.update(m.FAMILIES)
    return out


_MF = None


def no_trig(gen, bad=TRIG):
    """Wrap a 041 generator so that variants using trigonometric or inverse-trigonometric functions
    (outside the 241 syllabus) are rejected; the builder retries on ValueError."""
    def g(r):
        v = gen(r)
        text = v['stem'] + ' ' + v['answer'] + ' ' + ' '.join(v.get('options') or []) + ' ' + ' '.join(v.get('distractors') or [])
        if bad.search(text):
            raise ValueError('outside 241 scope')
        return v
    g.__name__ = gen.__name__ + '_nt'
    return g


def reuse(key: str, skip=(), filt=None) -> list:
    """Fresh copies of the 041 families of subtopic M + key, minus generators named in skip."""
    global _MF
    if _MF is None:
        _MF = _maths_families()
    out = []
    for f in _MF[M + key]:
        if f.gen.__name__ in skip:
            continue
        g = filt(f.gen) if filt else f.gen
        if filt and not _yields(g):
            continue
        out.append(dataclasses.replace(f, gen=g, used=0, exhausted=False, st='', kinds=tuple(f.kinds)))
    return out


def _yields(g, tries=120, need=0.35, distinct=10) -> bool:
    """True if a filtered generator still gives valid items often enough and with enough variety."""
    import random
    r = random.Random(12345)
    ok, seen = 0, set()
    for _ in range(tries):
        try:
            v = g(r)
        except (ValueError, ZeroDivisionError, IndexError):
            continue
        ok += 1
        seen.add(v['stem'])
    return ok >= need * tries and len(seen) >= min(distinct, ok)


# ---------------- formatting

def hm(h) -> str:
    """Hours as a Fraction to 'h hours m minutes' text: 24/5 -> 4 h 48 min."""
    h = Fr(h)
    mins = h * 60
    if mins.denominator != 1:
        return f'{fz(h)} hours'
    mins = int(mins)
    a, b = divmod(mins, 60)
    if b == 0:
        return f'{a} hour' + ('s' if a != 1 else '')
    if a == 0:
        return f'{b} minutes'
    return f'{a} h {b} min'


def mixed(x) -> str:
    """Fraction as a mixed number: 14/3 -> 4 2/3."""
    x = Fr(x)
    if x.denominator == 1 or abs(x) < 1:
        return fz(x)
    s = '−' if x < 0 else ''
    x = abs(x)
    w = x.numerator // x.denominator
    return f'{s}{w} {fz(x - w)}'


def ratio(a, b) -> str:
    a, b = Fr(a), Fr(b)
    l = math.lcm(a.denominator, b.denominator)
    a, b = int(a * l), int(b * l)
    g = math.gcd(a, b) or 1
    return f'{a // g} : {b // g}'


def ratio3(a, b, c) -> str:
    a, b, c = Fr(a), Fr(b), Fr(c)
    l = math.lcm(a.denominator, b.denominator, c.denominator)
    a, b, c = int(a * l), int(b * l), int(c * l)
    g = math.gcd(math.gcd(a, b), c) or 1
    return f'{a // g} : {b // g} : {c // g}'


def pct(x, dp=2) -> str:
    return num(float(x), dp) + '%'


def rs(x, dp=2) -> str:
    """Rupees with Indian grouping, two decimals only when needed."""
    x = float(x)
    if abs(x - round(x)) < 0.005:
        return inr(round(x))
    return inr(round(x, 2))


def interval(lo, hi, lo_closed=True, hi_closed=False) -> str:
    """Interval text with ∞: interval(None, 3) -> (−∞, 3)."""
    left = '(−∞' if lo is None else ('[' if lo_closed else '(') + fz(lo)
    right = '∞)' if hi is None else fz(hi) + (']' if hi_closed else ')')
    return f'{left}, {right}'


# ---------------- standard normal table (area from 0 to z), two decimals of z

def phi(z: float) -> float:
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def area0(z: float) -> float:
    """Area under the standard normal curve between 0 and z (table value, 4 dp)."""
    return round(phi(abs(z)) - 0.5, 4)


# Critical t values (two-tailed) for the usual levels; df 1..30.
T_05 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228,
        11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145, 15: 2.131, 16: 2.120, 17: 2.110, 18: 2.101, 19: 2.093, 20: 2.086,
        21: 2.080, 22: 2.074, 23: 2.069, 24: 2.064, 25: 2.060, 26: 2.056, 27: 2.052, 28: 2.048, 29: 2.045, 30: 2.042}
T_01 = {1: 63.657, 2: 9.925, 3: 5.841, 4: 4.604, 5: 4.032, 6: 3.707, 7: 3.499, 8: 3.355, 9: 3.250, 10: 3.169,
        11: 3.106, 12: 3.055, 13: 3.012, 14: 2.977, 15: 2.947, 16: 2.921, 17: 2.898, 18: 2.878, 19: 2.861, 20: 2.845,
        21: 2.831, 22: 2.819, 23: 2.807, 24: 2.797, 25: 2.787, 26: 2.779, 27: 2.771, 28: 2.763, 29: 2.756, 30: 2.750}
