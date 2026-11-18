"""Shared helpers for the CBSE class 11 Economics (030) question bank."""
from __future__ import annotations

import math
import random

from qbank import F, ar, mcq, onorm, num, inr, name, two_names, GIRLS, BOYS, CITIES

_USED: dict = {}
_ORDER: dict = {}


class Cycler:
    """Cycle through table rows so that forms and the bank do not repeat a row until all are used."""

    def __init__(self, ns):
        self.used = _USED.setdefault(ns, set())
        self.order = _ORDER.setdefault(ns, [])

    def pick(self, r, seq):
        seq = list(seq)
        keys = [repr(x) for x in seq]
        free = [i for i, k in enumerate(keys) if k not in self.used]
        if not free:
            recent = set(k for k in self.order[-max(1, len(seq) // 2):] if k in keys)
            for k in keys:
                if k not in recent:
                    self.used.discard(k)
            free = [i for i, k in enumerate(keys) if k not in self.used]
        i = r.choice(free)
        self.used.add(keys[i])
        self.order.append(keys[i])
        return seq[i]


_CYC: dict = {}


def cp(key, r, seq):
    return _CYC.setdefault(key, Cycler(key)).pick(r, seq)


def M(C, D, rows, **kw):
    """MCQ family over rows (stem, correct, [wrong...], key)."""
    key = f'M{id(rows)}'

    def gen(r):
        stem, ans, wrong, k = cp(key, r, rows)
        w = list(wrong)
        w = r.sample(w, 3) if len(w) > 3 else w
        return mcq(stem, ans, w, k, r)
    return F(C, D, 'mcq', gen, **kw)


def W(C, D, typ, rows, **kw):
    """Written family over rows (stem, answer, key[, distractors])."""
    key = f'W{id(rows)}'

    def gen(r):
        row = cp(key, r, rows)
        d = {'stem': row[0], 'answer': row[1], 'key': row[2]}
        if len(row) > 3:
            d['distractors'] = list(row[3])
        return d
    return F(C, D, typ, gen, **kw)


def AR(C, D, rows, **kw):
    """Assertion-Reason family over rows (A, R, code, why)."""
    key = f'A{id(rows)}'

    def gen(r):
        a, rr, code, why = cp(key, r, rows)
        return ar(a, rr, code, why)
    kw.setdefault('kinds', ('ar',))
    return F(C, D, 'mcq', gen, **kw)


def G(C, D, typ, fn, **kw):
    return F(C, D, typ, fn, **kw)


def classify(items, stem_tpl, key_tpl='{x} is an example of {c}.'):
    """items: list of (example, category). MCQ: which category does the example belong to (options = categories)."""
    cats = sorted({c for _, c in items})
    key = f'C{id(items)}'

    def gen(r):
        x, c = cp(key, r, items)
        wrong = [k for k in cats if k != c]
        if len(wrong) > 3:
            wrong = r.sample(wrong, 3)
        if len(wrong) < 3:
            raise ValueError('need 4 categories')
        return mcq(stem_tpl.format(x=x), c, wrong, key_tpl.format(x=x, c=c), r)
    return gen


def pick_example(items, target, stem):
    """MCQ: which of these is an example of `target` (one correct, three from other categories)."""
    key = f'P{id(items)}{target}'

    def gen(r):
        good = [x for x, c in items if c == target]
        bad = [(x, c) for x, c in items if c != target]
        g = cp(key, r, good)
        b = r.sample(bad, 3)
        return mcq(stem, g, [x for x, _ in b], f'{g}: {target}. The others: ' + '; '.join(f'{x}: {c}' for x, c in b) + '.', r)
    return gen


def odd_one(items, stem='Which of the following is the odd one out?'):
    key = f'O{id(items)}'

    def gen(r):
        cats = sorted({c for _, c in items})
        c = cp(key, r, cats)
        same = [x for x, k in items if k == c]
        if len(same) < 3:
            raise ValueError('few')
        three = r.sample(same, 3)
        oc = r.choice([k for k in cats if k != c])
        odd = r.choice([x for x, k in items if k == oc])
        return mcq(stem, odd, three, f'{", ".join(three)} are {c}; {odd} is {oc}.', r)
    return gen


def rnd_mean_data(r, n, lo, hi, step=1):
    """n integers in [lo, hi] whose mean is an integer."""
    for _ in range(200):
        xs = [r.randrange(lo, hi + 1, step) for _ in range(n)]
        if sum(xs) % n == 0 and len(set(xs)) > 2:
            return xs
    raise ValueError('no data')


def f2(x, dp=2):
    return num(round(x, dp), dp)


def frac_str(x, dp=2):
    return f'{x:.{dp}f}'


def series(xs, sep=', '):
    return sep.join(str(x) for x in xs)


def table(head, rows):
    """Plain-text table: head = list of column names, rows = list of lists."""
    out = [' | '.join(str(h) for h in head)]
    for rw in rows:
        out.append(' | '.join(str(x) for x in rw))
    return '\n'.join(out)
