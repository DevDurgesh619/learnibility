"""Fact-table family kit for the CBSE science banks (g11/g12 chemistry, g12 biology).

A subtopic is described by a spec dict; st_families(spec) turns it into qbank Families:

  topic     short noun phrase used in stems ("pollination")
  terms     [(term, description)]            C1 D1 mcq "Which term describes ...?", C1 D2 "What is meant by ...?"
  groups    [(phrase, [members])]            C2 D1 "Which is <phrase>?", C2 D3 "Which is NOT <phrase>?", C2 D2 classify
  tf        ([true statements], [(false statement, correction)])
                                             C2 D2 correct statement, C3 D3 incorrect statement,
                                             C3 D2 find-and-correct, C2 D3 Assertion-Reason (codes c/d)
  orders    [(prompt, [items in order], reason, sep)]
                                             C3 D3 mcq order, C4 D4 arrange-and-justify
  features  {'intro', 'q', 'what', 'items': [(label, [features])]}
                                             C3 D3 mcq identify, C3 D2 short identify, C3 D3 compare,
                                             C4 D3 case, C4 D4 long (kind long5)
  ar        [(assertion, reason, code, why)] C3 D3 Assertion-Reason
  qa        [(C, D, type, question, answer, key)] or with a 7th element: tuple of extra kinds
  fams      extra Family objects (computed numericals)

Mocks use the custom kind 'long5' for the 5-mark section so only real long answers are chosen.
"""
from __future__ import annotations

import math
import random
import re

from qbank import F, ar, mcq, num

LONG = 'long5'


def cap(s: str) -> str:
    return s[:1].upper() + s[1:] if s and s[0].isascii() else s


def qmark(q: str) -> str:
    """Close a prompt: imperatives ('Identify the ...') take a full stop, questions a question mark."""
    return q + ('.' if q.split()[0] in ('Identify', 'Name', 'State', 'Give') else '?')


def strip_article(p: str) -> str:
    for a in ('a ', 'an ', 'the '):
        if p.startswith(a):
            return p[len(a):]
    return p


def sf(x: float, n: int = 3) -> str:
    """Round to n significant figures and print without exponent where sensible."""
    if x == 0:
        return '0'
    x = float(f'{x:.{n - 1}e}')
    e = math.floor(math.log10(abs(x)))
    if e >= 6 or e <= -4:
        m = x / 10 ** e
        ms = f'{m:.{n - 1}f}'
        if float(ms) >= 10:
            e += 1
            ms = f'{m / 10:.{n - 1}f}'
        return f'{ms} × 10{sup_(e)}'.replace('-', '−')
    d = max(n - 1 - e, 0)
    return f'{x:.{d}f}'.replace('-', '−')


def sup_(n: int) -> str:
    return str(n).translate(str.maketrans('0123456789-', '⁰¹²³⁴⁵⁶⁷⁸⁹⁻'))


def sci(x: float, n: int = 3) -> str:
    """Always scientific notation."""
    if x == 0:
        return '0'
    e = math.floor(math.log10(abs(x)))
    m = x / 10 ** e
    ms = f'{m:.{n - 1}f}'
    if float(ms) >= 10:
        e += 1
        ms = f'{m / 10:.{n - 1}f}'
    return f'{ms} × 10{sup_(e)}'.replace('-', '−')


def near(x: float, n: int = 3, factors=(2, 0.5, 10, 0.1, 1.5, 0.75)) -> list[str]:
    """Plausible wrong numerical answers formatted like the answer."""
    out, seen = [], {sf(x, n)}
    for f in factors:
        s = sf(x * f, n)
        if s not in seen:
            out.append(s)
            seen.add(s)
    return out


def _nums(r, lo, hi, step):
    k = int(round((hi - lo) / step))
    return lo + step * r.randint(0, k)


# ---------------------------------------------------------------- generic generators

def _terms(spec):
    terms = spec['terms']
    out = []

    def g_term(r):
        t, d = r.choice(terms)
        wrong = [x[0] for x in r.sample([x for x in terms if x[0] != t], 3)]
        return mcq(f'Which term describes {d}?', t, wrong, f'{cap(t)}: {d}.', r)

    def g_define(r):
        t, d = r.choice(terms)
        lead = r.choice(['What is meant by', 'Define the term', 'Explain the term'])
        others = [cap(x[1]) for x in terms if x[0] != t]
        return {'stem': f'{lead} “{t}”.' if lead != 'What is meant by' else f'What is meant by “{t}”?',
                'answer': cap(d) + '.', 'key': f'1 mark: {d}.',
                'distractors': r.sample(others, min(3, len(others)))}

    if len(terms) >= 4:
        out.append(F('C1', 'D1', 'mcq', g_term))
    out.append(F('C1', 'D2', 'short', g_define))
    return out


def _groups(spec):
    groups = spec['groups']
    out = []

    def g_is(r):
        p, mem = r.choice(groups)
        good = r.choice(mem)
        pool = [m for q, ms in groups if q != p for m in ms if m not in mem]
        wrong = r.sample(pool, 3)
        return mcq(f'Which of the following is {p}?', good, wrong, f'{cap(good)} is {p}; the others are not.', r)

    def g_not(r):
        p, mem = r.choice([g for g in groups if len(g[1]) >= 3])
        three = r.sample(mem, 3)
        pool = [(q, m) for q, ms in groups if q != p for m in ms if m not in mem]
        q, odd = r.choice(pool)
        return mcq(f'Which of the following is NOT {p}?', odd, three, f'{cap(odd)} is {q}, not {p}.', r)

    def g_classify(r):
        (p1, m1), (p2, m2) = r.sample(groups, 2)
        k1 = r.randint(1, min(3, len(m1)))
        k2 = min(4 - k1, len(m2))
        k2 = max(k2, 1)
        a = [(x, p1) for x in r.sample(m1, k1)] + [(x, p2) for x in r.sample(m2, k2)]
        r.shuffle(a)
        l1, l2 = strip_article(p1), strip_article(p2)
        lab = {p1: l1, p2: l2}
        return {'stem': f'Classify each of the following as {l1} or {l2}: {", ".join(x for x, _ in a)}.',
                'answer': '; '.join(f'{x} – {lab[p]}' for x, p in a) + '.',
                'key': f'½ mark each: ' + '; '.join(f'{x} – {lab[p]}' for x, p in a) + '.'}

    out.append(F('C2', 'D1', 'mcq', g_is))
    if any(len(g[1]) >= 3 for g in groups) and len(groups) >= 2:
        out.append(F('C2', 'D3', 'mcq', g_not))
    if len(groups) >= 2 and spec.get('classify', True):
        out.append(F('C2', 'D2', 'short', g_classify, marks=2, minutes=2))
    return out


def _tf(spec):
    trues, falses = spec['tf']
    topic = spec.get('topic', 'this topic')
    out = []

    def g_correct(r):
        t = r.choice(trues)
        f = [x[0] for x in r.sample(falses, 3)]
        corr = ' '.join(c for s_, c in falses if s_ in f)
        return mcq(f'Which of the following statements about {topic} is correct?', t, f,
                   f'{t} The other statements are false. {corr}', r)

    def g_incorrect(r):
        ts = r.sample(trues, 3)
        f, corr = r.choice(falses)
        return mcq(f'Which of the following statements about {topic} is incorrect?', f, ts,
                   f'The incorrect statement is “{f}” Correct form: {corr}', r)

    def g_fix(r):
        f, corr = r.choice(falses)
        return {'stem': f'The following statement is incorrect. Rewrite it correctly and give a reason: “{f}”',
                'answer': corr, 'key': f'1 mark for the corrected statement, 1 mark for the reason: {corr}'}

    def g_ar_tf(r):
        if r.random() < 0.5:
            a = r.choice(trues)
            rf, corr = r.choice(falses)
            return ar(a.rstrip('.') + '.', rf.rstrip('.') + '.', 'c', f'A is true. R is false: {corr}')
        af, corr = r.choice(falses)
        rr = r.choice(trues)
        return ar(af.rstrip('.') + '.', rr.rstrip('.') + '.', 'd', f'A is false: {corr} R is a true statement.')

    if len(falses) >= 3:
        out.append(F('C2', 'D2', 'mcq', g_correct))
    if len(trues) >= 3:
        out.append(F('C3', 'D3', 'mcq', g_incorrect))
    out.append(F('C3', 'D2', 'explain', g_fix, marks=2))
    out.append(F('C2', 'D3', 'mcq', g_ar_tf, kinds=('ar',)))
    return out


def _orders(spec):
    orders = spec['orders']
    out = []

    def pick(r):
        prompt, items, why, sep = r.choice(orders)
        k = min(len(items), r.choice([3, 4, 4]))
        idx = sorted(r.sample(range(len(items)), k))
        sub = [items[i] for i in idx]
        return prompt, sub, why, sep

    def g_mcq(r):
        prompt, sub, why, sep = pick(r)
        j = f' {sep} '
        good = j.join(sub)
        perms = set()
        tries = 0
        while len(perms) < 3 and tries < 200:
            tries += 1
            p = sub[:]
            r.shuffle(p)
            s = j.join(p)
            if s != good:
                perms.add(s)
        if len(perms) < 3:
            raise ValueError('not enough permutations')
        return mcq(f'Which of the following shows the correct {prompt}?', good, sorted(perms), f'{good}. {why}', r)

    def g_arrange(r):
        prompt, sub, why, sep = pick(r)
        sh = sub[:]
        while sh == sub:
            r.shuffle(sh)
        good = f' {sep} '.join(sub)
        return {'stem': f'Arrange the following in the correct {prompt}: {", ".join(sh)}. Give a reason.',
                'answer': good, 'key': f'1 mark for the order {good}; 1 mark for the reason: {why}'}

    out.append(F('C3', 'D3', 'mcq', g_mcq))
    out.append(F('C4', 'D4', 'explain', g_arrange, marks=2))
    return out


def _features(spec):
    ft = spec['features']
    items = ft['items']
    intro, q, what = ft['intro'], ft['q'], ft.get('what', 'type')
    out = []

    def obs(r, k=2):
        lab, fs = r.choice(items)
        return lab, r.sample(fs, min(k, len(fs))), fs

    def g_mcq(r):
        lab, f, _ = obs(r, 2)
        wrong = [x[0] for x in r.sample([x for x in items if x[0] != lab], 3)]
        return mcq(f'{intro} {"; ".join(f)}. {qmark(q)}', lab, wrong, f'{cap(lab)}: {"; ".join(f)}.', r)

    def g_short(r):
        lab, f, _ = obs(r, r.choice([2, 3]))
        wrong = [x[0] for x in r.sample([x for x in items if x[0] != lab], min(3, len(items) - 1))]
        return {'stem': f'{intro} {"; ".join(f)}. {qmark(q)} Give a reason.', 'answer': cap(lab),
                'key': f'1 mark: {lab}; 1 mark: the features {"; ".join(f)} are characteristic of it.',
                'distractors': wrong, 'marks': 2}

    def g_compare(r):
        (l1, f1), (l2, f2) = r.sample(items, 2)
        a, b = r.sample(f1, min(2, len(f1))), r.sample(f2, min(2, len(f2)))
        return {'stem': f'Give two differences between {l1} and {l2}.',
                'answer': f'{cap(l1)}: {"; ".join(a)}. {cap(l2)}: {"; ".join(b)}.',
                'key': f'1 mark for each correct, paired difference, e.g. {l1} – {"; ".join(a)}; {l2} – {"; ".join(b)}.'}

    def g_case(r):
        lab, fs = r.choice([x for x in items if len(x[1]) >= 3])
        shown = r.sample(fs, min(len(fs) - 1, 3))
        rest = [x for x in fs if x not in shown]
        l2, f2 = r.choice([x for x in items if x[0] != lab])
        intro2 = ft.get('case', intro)
        return {'stem': (f'{intro2} {"; ".join(shown)}.\n(i) {qmark(q)} (1 mark)\n'
                         f'(ii) State one more feature you would expect to observe. (1 mark)\n'
                         f'(iii) How would the observations differ if it were {l2}? Give two points. (2 marks)'),
                'answer': f'(i) {cap(lab)} (ii) {rest[0]} (iii) {"; ".join(r.sample(f2, min(2, len(f2))))}',
                'key': f'(i) {lab} – 1 mark. (ii) any one of: {"; ".join(rest)} – 1 mark. '
                       f'(iii) for {l2}: {"; ".join(f2[:3])} – 1 mark each for any two.'}

    def g_long(r):
        (l1, f1), (l2, f2) = r.sample(items, 2)
        lab, fs = r.choice([(l1, f1), (l2, f2)])
        shown = r.choice(fs)
        n1, n2 = min(3, len(f1)), min(3, len(f2))
        return {'stem': (f'(a) Distinguish between {l1} and {l2} on any three points. (3 marks)\n'
                         f'(b) {intro} {shown}. {q} – {l1} or {l2}? Justify your answer. (2 marks)'),
                'answer': f'(a) {cap(l1)}: {"; ".join(f1[:n1])}. {cap(l2)}: {"; ".join(f2[:n2])}. (b) {cap(lab)}.',
                'key': f'(a) 1 mark for each of three paired differences. (b) 1 mark: {lab}; 1 mark: “{shown}” is a feature of {lab}.'}

    if len(items) >= 4:
        out.append(F('C3', 'D3', 'mcq', g_mcq))
    out.append(F('C3', 'D2', 'explain', g_short, marks=2))
    if len(items) >= 2:
        if ft.get('compare', True):
            out.append(F('C3', 'D3', 'explain', g_compare, marks=2))
        if any(len(x[1]) >= 3 for x in items) and ft.get('case', True):
            out.append(F('C4', 'D3', 'case', g_case, kinds=('case',)))
        if ft.get('long', True):
            out.append(F('C4', 'D4', 'long', g_long, kinds=(LONG,)))
    return out


def _ar(spec):
    lst = spec['ar']

    def g(r):
        a, b, code, why = r.choice(lst)
        return ar(a, b, code, why)
    return [F('C3', 'D3', 'mcq', g, kinds=('ar',))]


def _qa(spec):
    groups = {}
    for it in spec['qa']:
        C, D, typ = it[0], it[1], it[2]
        kinds = it[6] if len(it) > 6 else ()
        if typ == 'long':
            kinds = tuple(set(kinds) | {LONG})
        groups.setdefault((C, D, typ, kinds), []).append(it)
    out = []
    for (C, D, typ, kinds), its in groups.items():
        def g(r, its=its):
            it = r.choice(its)
            v = {'stem': it[3], 'answer': it[4], 'key': it[5]}
            if len(it) > 7:
                v['distractors'] = list(it[7])
            return v
        out.append(F(C, D, typ, g, kinds=kinds))
    return out


_MINUS = re.compile(r'(^|[\s(=/:;,\[])-(?=\d)')


def fix_minus(x):
    if isinstance(x, str):
        return _MINUS.sub(lambda m: m.group(1) + '−', x)
    if isinstance(x, list):
        return [fix_minus(y) for y in x]
    return x


def _wrap(f):
    g0 = f.gen

    def g(r):
        v = g0(r)
        return {k: (fix_minus(val) if k in ('stem', 'answer', 'key', 'options', 'distractors') else val) for k, val in v.items()}
    g.__name__ = getattr(g0, '__name__', 'g')
    f.gen = g
    return f


def st_families(spec: dict) -> list:
    fams = []
    if 'terms' in spec:
        fams += _terms(spec)
    for gk in ('groups', 'groups2', 'groups3'):
        if gk in spec:
            fams += _groups(dict(spec, groups=spec[gk]))
    if 'tf' in spec:
        fams += _tf(spec)
    if 'orders' in spec:
        fams += _orders(spec)
    for fk in ('features', 'features2'):
        if fk in spec:
            fams += _features(dict(spec, features=spec[fk]))
    if 'ar' in spec:
        fams += _ar(spec)
    if 'qa' in spec:
        fams += _qa(spec)
    fams += spec.get('fams', [])
    return [_wrap(f) for f in fams]


def build_all(prefix: str, specs: dict) -> dict:
    """specs: {'ch01-st1': spec, ...} -> {subtopicId: [Family]}"""
    return {f'{prefix}-{k}': st_families(v) for k, v in specs.items()}


# CBSE board pattern for Class XII science theory (70 marks, 33 questions; SQP 2024-25 onward):
# A 16 × 1 (12 MCQ + 4 Assertion-Reason), B 5 × 2, C 7 × 3, D 2 case-based × 4, E 3 × 5.
SCIENCE_PATTERN = [(12, 1, 'mcq'), (4, 1, 'ar'), (5, 2, 'short'), (7, 3, 'short3'), (2, 4, 'case'), (3, 5, LONG)]
