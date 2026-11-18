"""Shared family templates for the CBSE science banks (cbse-g8/g9/g10-science).

Fact-based subjects need many distinct, accurate items. Each template below turns a fact
table into a Family whose generator walks the table in a shuffled cycle (so every entry is
offered once before any repeats; repeats are then rejected by the Builder's duplicate check
and the family is marked exhausted).

Templates (all return qbank.Family):
    DEF(defs)            "Define X." / "What is meant by X?"    defs = [(term, definition noun phrase)]
    TERM(defs)           MCQ: definition -> term (other terms of the table as distractors)
    MC(items)            MCQ: (stem, correct, w1, w2, w3[, key])
    SA(items, type=...)  written item: (stem, answer[, key[, [d1, d2, d3]]])
    ARF(items)           Assertion-Reason: (A, R, code, why)
    CLS(cats, tpl)       MCQ "which is an example of {cat}" over {cat: [examples]}; neg=True asks "NOT"
    SORT(cats, tpl)      short: sort 4-6 examples into two categories
    CASE(items), LONG(items)   case-based (4 marks) and long answer (5 marks): (stem, answer, key)
    G(C, D, type, fn)    custom generator (numericals)
"""
from __future__ import annotations

import random
import re

from qbank import F, ar, mcq

__all__ = ['DEF', 'TERM', 'MC', 'SA', 'ARF', 'CLS', 'SORT', 'CASE', 'LONG', 'G', 'cap', 'cyc', 'sig', 'finalize', 'strict_mock_fits', 'SciBuilder']


def _qkey(v: dict) -> str:
    return ' '.join(str(v.get('stem', '')).lower().split()) + ' || ' + ' '.join(str(v.get('answer', '')).lower().split())


def finalize(families: dict) -> dict:
    """Wrap every family generator so that it never offers the same question (stem + answer) twice,
    e.g. the same MCQ with a different set of distractors; add the bank twins of reserved LONG
    families. Returns the same dict."""
    for st, fams in families.items():
        for f in list(fams):
            tw = getattr(f, 'twin', None)
            if tw is not None and tw not in fams:
                fams.append(tw)
        for f in fams:
            if getattr(f.gen, '_uniq', False):
                continue
            f.gen = _uniq(f.gen, f.type == 'mcq')
    return families


def _clean_distractors(v: dict) -> None:
    if 'distractors' not in v:
        return
    seen = {' '.join(str(v['answer']).lower().split())}
    out = []
    for d in v['distractors']:
        k = ' '.join(str(d).lower().split())
        if k and k not in seen:
            seen.add(k)
            out.append(d)
    v['distractors'] = out


def _uniq(fn, is_mcq=False):
    seen = set()

    def gen(r):
        for _ in range(25):
            v = fn(r)
            _clean_distractors(v)
            if 'options' not in v and len(v.get('distractors', [])) < 3:
                if is_mcq:
                    continue
                v.pop('distractors', None)
            k = _qkey(v)
            if k not in seen:
                seen.add(k)
                return v
        raise IndexError('no new variant')
    gen._uniq = True
    return gen


def cap(s: str) -> str:
    return s[:1].upper() + s[1:] if s else s


def cyc(entries: list):
    """Return next(r) giving the entries in a shuffled cycle (shuffle made with the Builder's r)."""
    state = {'order': None, 'i': 0}

    def nxt(r: random.Random):
        if not entries:
            raise IndexError('empty table')
        if state['order'] is None:
            state['order'] = list(range(len(entries)))
            r.shuffle(state['order'])
        e = entries[state['order'][state['i'] % len(entries)]]
        state['i'] += 1
        return e
    return nxt


def sig(x: float, n: int = 3) -> str:
    """Round to n significant figures, plain notation, true minus sign."""
    if x == 0:
        return '0'
    from math import floor, log10
    d = n - 1 - int(floor(log10(abs(x))))
    v = round(x, d)
    if d <= 0:
        s = str(int(v))
    else:
        s = f'{v:.{d}f}'
        if '.' in s:
            s = s.rstrip('0').rstrip('.')
    return s.replace('-', '−')


def _end(s: str) -> str:
    s = s.strip()
    return s if s[-1:] in '.?!' else s + '.'


# A DEF item can also be served as an MCQ (definition options) when its table has at least this many
# entries; smaller tables would repeat the same four options and trip the near-duplicate check.
DEF_MCQ_MIN = 4


def DEF(defs, C='C1', D='D2', **kw):
    nxt = cyc(defs)

    def gen(r):
        term, d = nxt(r)
        stem = f'Define {term}.' if len(term) % 2 else f'What is meant by {term}?'
        others = [cap(_end(x[1])) for x in defs if x[0] != term]
        r2 = random.Random(term)
        v = {'stem': stem, 'answer': cap(d.strip().rstrip('.')), 'key': f'1 mark: {cap(term)} – {_end(d)}'}
        if len(defs) >= DEF_MCQ_MIN:
            v['distractors'] = [o.rstrip('.') for o in r2.sample(others, min(3, len(others)))]
        return v
    return F(C, D, 'short', gen, **kw)


def TERM(defs, C='C1', D='D1', **kw):
    nxt = cyc(defs)

    def gen(r):
        term, d = nxt(r)
        others = [x[0] for x in defs if x[0] != term]
        wrong = random.Random(term).sample(others, 3)
        return mcq(f'Which term is described here? "{cap(_end(d))}"', term, wrong,
                   f'{cap(term)} is {_end(d)}', r)
    return F(C, D, 'mcq', gen, **kw)


def MC(items, C='C1', D='D2', **kw):
    nxt = cyc(items)

    def gen(r):
        e = nxt(r)
        stem, ok, w = e[0], e[1], list(e[2:5])
        key = e[5] if len(e) > 5 else f'{_end(ok)}'
        return mcq(stem, ok, w, key, r)
    return F(C, D, 'mcq', gen, **kw)


def SA(items, C='C2', D='D3', type='explain', **kw):
    nxt = cyc(items)

    def gen(r):
        e = nxt(r)
        stem, ans = e[0], e[1]
        key = e[2] if len(e) > 2 and e[2] else ans
        v = {'stem': stem, 'answer': ans, 'key': key}
        if len(e) > 3 and e[3]:
            v['distractors'] = list(e[3])
        return v
    return F(C, D, type, gen, **kw)


def ARF(items, C='C2', D='D3', **kw):
    nxt = cyc(items)

    def gen(r):
        a, rr, code, why = nxt(r)
        return ar(a, rr, code, why)
    kinds = tuple(set(kw.pop('kinds', ())) | {'ar'})
    return F(C, D, 'mcq', gen, kinds=kinds, **kw)


_NEG = re.compile(r'^(Which of (?:the following|these)(?: \w+)?) (is|are) ')


def CLS(cats: dict, tpl='Which of the following is {}?', C='C3', D='D2', neg=False, neg_tpl=None, verb='is', **kw):
    """cats: {category phrase as it reads in tpl: [examples]}. Distractors come from other categories.
    neg=True asks for the odd one out; neg_tpl overrides the automatic 'is' -> 'is NOT' rewrite."""
    labels = list(cats)
    owner = {x: c for c, xs in cats.items() for x in xs}
    if neg:
        ntpl = neg_tpl or _NEG.sub(lambda m: f'{m.group(1)} {m.group(2)} NOT ', tpl)
        if 'NOT' not in ntpl:
            raise SystemExit(f'CLS neg template has no NOT: {tpl}')

    def gen(r):
        c = r.choice([k for k in labels if len(cats[k]) >= (3 if neg else 1)])
        others = [x for k in labels if k != c for x in cats[k]]
        if neg:
            odd = r.choice(others)
            right = random.Random(c + odd).sample(cats[c], 3)
            stem = ntpl.replace('{}', c)
            key = f'{cap(odd)} {verb} {owner[odd]}, not {c}. Each of the others ({", ".join(right)}) {verb} {c}.'
            return mcq(stem, odd, right, key, r)
        x = r.choice(cats[c])
        wrong = random.Random(c + x).sample(others, 3)
        key = f'{cap(x)} {verb} {c}. The others: ' + '; '.join(f'{w} – {owner[w]}' for w in wrong) + '.'
        return mcq(tpl.replace('{}', c), x, wrong, key, r)
    return F(C, D, 'mcq', gen, **kw)


def SORT(cats: dict, tpl='Classify the following as {A} or {B}: {L}.', C='C3', D='D3', type='explain', n=(2, 3), **kw):
    """Sort a random sample of examples from two categories."""
    labels = [k for k in cats if len(cats[k]) >= n[0]]

    def gen(r):
        a, b = r.sample(labels, 2)
        ka = r.randint(n[0], min(n[1], len(cats[a])))
        kb = r.randint(n[0], min(n[1], len(cats[b])))
        xa, xb = r.sample(cats[a], ka), r.sample(cats[b], kb)
        xa = [x.rstrip('.') for x in xa]
        xb = [x.rstrip('.') for x in xb]
        lst = xa + xb
        r.shuffle(lst)
        long_items = any(len(x.split()) > 4 or ',' in x for x in lst)
        sep = '; ' if long_items else ', '
        L = '; '.join(f'({i + 1}) {x}' for i, x in enumerate(lst)) if long_items else ', '.join(lst)
        stem = tpl.format(A=a, B=b, L=L).replace('..', '.')
        ans = f'{cap(a)}: {sep.join(sorted(xa))}. {cap(b)}: {sep.join(sorted(xb))}.'
        return {'stem': stem, 'answer': ans, 'key': f'½ mark per correctly placed item (rounded): {ans}'}
    return F(C, D, type, gen, **kw)


def CASE(items, C='C4', D='D3', **kw):
    nxt = cyc(items)

    def gen(r):
        e = nxt(r)
        return {'stem': e[0], 'answer': e[1], 'key': e[2] if len(e) > 2 else e[1]}
    kw.setdefault('gap', 'G7')
    return F(C, D, 'case', gen, **kw)


def _long(items, C, D, **kw):
    nxt = cyc(items)

    def gen(r):
        e = nxt(r)
        return {'stem': e[0], 'answer': e[1], 'key': e[2] if len(e) > 2 else e[1]}
    return F(C, D, 'long', gen, **kw)


def LONG(items, C='C4', D='D3', **kw):
    """Long-answer (5-mark) family. The first half of the entries (rounded up) is reserved for the
    mocks (5-mark section), the rest may also be used in the bank and practice forms.
    Returns a Family when everything is reserved, else a Family whose .twin is the bank family."""
    k = (len(items) + 1) // 2
    res = _long(items[:k], C, D, **kw)
    res.mock_only = True
    if len(items) > k:
        res.twin = _long(items[k:], C, D, **kw)
    return res


def G(C, D, type_, fn, **kw):
    return F(C, D, type_, fn, **kw)


def strict_mock_fits():
    """Make mock slots take only items whose own marking key matches the slot's marks:
    short (2 marks) <- explain/numerical; short3 (3) <- multi_step; long (5) <- long; case (4) <- case or kinds case.
    Patches qbank._fits for this process only (qbank.py itself is unchanged)."""
    import qbank
    orig = qbank._fits

    def fits(f, kind):
        if kind == 'short':
            return f.type in ('explain', 'numerical') and f.C in ('C2', 'C3', 'C4')
        if kind == 'short3':
            return f.type == 'multi_step'
        if kind == 'long':
            return f.type == 'long' or 'long' in f.kinds
        if kind == 'case':
            return f.type == 'case' or 'case' in f.kinds
        return orig(f, kind)
    qbank._fits = fits


def _bank(fams):
    return [f for f in fams if not getattr(f, 'mock_only', False)]


def _make_builder():
    import qbank

    class SciBuilder(qbank.Builder):
        """qbank.Builder that keeps mock-only families (reserved LONG items) out of the bank and practice forms."""

        def _pick(self, fams, *a, **k):
            return super()._pick(_bank(fams), *a, **k)

        def _closest(self, fams, *a, **k):
            return super()._closest(_bank(fams), *a, **k)
    return SciBuilder


def SciBuilder(*a, **k):
    return _make_builder()(*a, **k)
