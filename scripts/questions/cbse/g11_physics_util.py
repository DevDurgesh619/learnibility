"""Shared helpers for the CBSE class 11/12 physics and class 11 maths generators.

Only small formatting and pool helpers on top of qbank (qbank itself is not changed).
"""
from __future__ import annotations

import math
import random
from decimal import Decimal, ROUND_HALF_UP

from qbank import F, ar, mcq, num, sup, onorm, name, two_names, inr, CITIES  # noqa: F401


def sig(x: float, n: int = 3) -> str:
    """Format x to n significant figures (half-up rounding, as in school work); scientific notation
    (a × 10ⁿ) when very large or small."""
    if x == 0:
        return '0'
    d = Decimal(repr(float(x)))
    d = d.quantize(Decimal(1).scaleb(d.adjusted() - n + 1), rounding=ROUND_HALF_UP)
    e = d.adjusted()
    if -3 <= e < 5:
        dp = max(0, n - 1 - e)
        s = f'{d:.{dp}f}'
    else:
        m = d.scaleb(-e)
        s = f'{m:.{n - 1}f} × 10{sup(e)}'
    return s.replace('-', '−')


def g(x: float, dp: int = 3) -> str:
    """Given data in a stem: short form, no trailing zeros. Small values keep at least 4 significant
    figures (so 0.0025 is not shown as 0.003)."""
    if abs(x) >= 1e5 or (x != 0 and abs(x) < 1e-3):
        e = math.floor(math.log10(abs(x)))
        m = x / 10 ** e
        ms = f'{m:.{dp}f}'.rstrip('0').rstrip('.')
        return f'{ms} × 10{sup(e)}'.replace('-', '−')
    if x != 0 and abs(x) < 1:
        dp = max(dp, 3 - math.floor(math.log10(abs(x))))
    return num(round(x, 10), dp)


def NUM(stem: str, val: float, unit: str, key: str, wrongs=(), n: int = 3, gap: str | None = None, **kw) -> dict:
    """A numerical item: answer to n s.f. with unit, plus formatted wrong answers for MCQ use."""
    u = unit if unit in ('°', '%') else ((' ' + unit) if unit else '')
    ans = sig(val, n) + u
    ds, seen = [], {onorm(ans)}
    for w in list(wrongs) + [val * 2, val / 2, val * 1.5, val * 4, val / 4, val * 3]:
        if w is None or (isinstance(w, float) and (math.isnan(w) or math.isinf(w))):
            continue
        s = (w if isinstance(w, str) else sig(w, n) + u)
        if onorm(s) not in seen:
            ds.append(s)
            seen.add(onorm(s))
    d = {'stem': stem, 'answer': ans, 'key': key.replace('{ans}', ans), 'distractors': ds[:5]}
    if gap:
        d['gap'] = gap
    d.update(kw)
    return d


def NUM2(stem: str, vals, units, key: str, wrongs=(), n: int = 3, gap: str | None = None, sep: str = '; ') -> dict:
    """Numerical item with two (or more) answers, e.g. ('a', 't'); wrongs is a list of value tuples."""
    def fmt(vs):
        return sep.join(sig(v, n) + (u if u in ('°', '%') else (' ' + u if u else '')) for v, u in zip(vs, units))
    ans = fmt(vals)
    ds, seen = [], {onorm(ans)}
    for w in list(wrongs) + [tuple(v * 2 for v in vals), tuple(v / 2 for v in vals), tuple(v * k for v, k in zip(vals, (1, 2, 1, 2))), tuple(v * k for v, k in zip(vals, (2, 1, 2, 1)))]:
        s = fmt(w)
        if onorm(s) not in seen:
            ds.append(s)
            seen.add(onorm(s))
    d = {'stem': stem, 'answer': ans, 'key': key.replace('{ans}', ans), 'distractors': ds[:5]}
    if gap:
        d['gap'] = gap
    return d


def pool_mcq(items):
    """items: (stem, correct, [three wrong], key)."""
    def gen(r):
        s, c, w, k = r.choice(items)
        return mcq(s, c, list(w), k, r)
    return gen


def pool_ar(items):
    """items: (assertion, reason, code, why)."""
    def gen(r):
        a, rs, c, w = r.choice(items)
        return ar(a, rs, c, w)
    return gen


def pool_txt(items):
    """items: (stem, answer, key) or (stem, answer, key, distractors)."""
    def gen(r):
        it = r.choice(items)
        d = {'stem': it[0], 'answer': it[1], 'key': it[2]}
        if len(it) > 3:
            d['distractors'] = list(it[3])
        return d
    return gen


def term_mcq(table, fwd: str, rev: str | None = None, key_fmt: str = '{a} — {b}.'):
    """table: (term, description). fwd asks for the description of a term ('{a}' placeholder);
    rev asks for the term matching a description ('{b}'). Wrong options come from the same table."""
    def gen(r):
        i = r.randrange(len(table))
        a, b = table[i]
        others = [t for j, t in enumerate(table) if j != i]
        if rev and r.random() < 0.5:
            wrong = [t[0] for t in others if onorm(t[0]) != onorm(a)]
            wrong = r.sample(list(dict.fromkeys(wrong)), 3)
            return mcq(rev.format(a=a, b=b), a, wrong, key_fmt.format(a=a, b=b), r)
        wrong = [t[1] for t in others if onorm(t[1]) != onorm(b)]
        wrong = r.sample(list(dict.fromkeys(wrong)), 3)
        return mcq(fwd.format(a=a, b=b), b, wrong, key_fmt.format(a=a, b=b), r)
    return gen


def tf_mcq(topic: str, trues, falses, why: str = ''):
    """'Which statement about {topic} is correct/incorrect?' built from true and false statement pools."""
    def gen(r):
        if r.random() < 0.6 or len(trues) < 3:
            c = r.choice(trues)
            w = r.sample(falses, 3)
            return mcq(f'Which of the following statements about {topic} is correct?', c, w,
                       f'Correct: "{c}" The other three are false.{(" " + why) if why else ""}', r)
        c = r.choice(falses)
        w = r.sample(trues, 3)
        return mcq(f'Which of the following statements about {topic} is NOT correct?', c, w,
                   f'"{c}" is false; the other three are true.{(" " + why) if why else ""}', r)
    return gen


def choose(r, *xs):
    return r.choice(xs)


def pick(r: random.Random, lo: float, hi: float, step: float) -> float:
    n = int(round((hi - lo) / step))
    return round(lo + step * r.randint(0, n), 10)


def deg(x: float) -> str:
    return f'{num(x, 1)}°'


def ordn(n: int) -> str:
    if 10 <= n % 100 <= 20:
        return f'{n}th'
    return f'{n}{ {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th") }'


import re as _re
from functools import wraps as _wraps

_AN = _re.compile(r'\b([Aa]) (?=(aluminium|iron|ice|insect|oil|elevator|electron|ideal|object|aircraft|aeroplane|AC\b|LCR|LED|n-type|n–p|npn|alpha|engine|isothermal|adiabatic|isobaric|isochoric|open|organ|electric|ellipse|equilateral|odd|even|integer|arithmetic|infinite|empty|element|event|unbiased|ordinary|observer|overtone|outer|inner|r\.m\.s|rms|S\b|F\b|M\b|N\b|X\b))')


def fix_text(s: str) -> str:
    return _AN.sub(lambda m: m.group(1) + 'n ', s)


def polish(families: dict) -> dict:
    """Wrap every family generator so that articles such as 'a aluminium' become 'an aluminium'."""
    for fams in families.values():
        for f in fams:
            if getattr(f.gen, '_polished', False):
                continue
            g0 = f.gen

            @_wraps(g0)
            def gen(r, _g=g0):
                v = _g(r)
                for k in ('stem', 'answer', 'key'):
                    v[k] = fix_text(v[k])
                if v.get('options'):
                    new = [fix_text(o) for o in v['options']]
                    if v['answer'] not in new:
                        v['answer'] = fix_text(v['answer'])
                    v['options'] = new
                if v.get('distractors'):
                    v['distractors'] = [fix_text(str(o)) for o in v['distractors']]
                return v
            gen._polished = True
            f.gen = gen
    return families
