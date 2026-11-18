"""Shared helpers for the CBSE class 11 commerce banks (cbse-g11-accountancy, cbse-g11-business).

Two parts:
1. `facts(spec)` turns a subtopic's fact table (terms, point lists, distinctions, scenarios,
   Assertion-Reason items, true/false statements, cases) into a list of qbank Families.
2. Small formatting helpers for accounting (journal entries, firm names, amounts).

Fact generators walk their table in a shuffled cycle (`Cyc`), so a family gives every entry once
before it repeats; repeated entries are then rejected by the builder's duplicate check, which marks
the family exhausted.

Mock kinds used by both subjects: 'mcq', 'ar', 'm3' (3-mark), 'm4' (4-mark), 'm6' (6-mark).
"""
from __future__ import annotations

import random

from qbank import F, ar, mcq, inr, GIRLS, BOYS, CITIES

SURNAMES = ['Sharma', 'Gupta', 'Mehta', 'Agarwal', 'Iyer', 'Reddy', 'Khan', 'Singh', 'Bose', 'Nair', 'Patel', 'Jain',
            'Kapoor', 'Verma', 'Das', 'Menon', 'Rao', 'Chopra', 'Malhotra', 'Bansal', 'Joshi', 'Kulkarni', 'Banerjee',
            'Pillai', 'Saxena', 'Mishra', 'Ahuja', 'Sethi', 'Thakur', 'Goyal']
FIRM_SUFFIX = ['Traders', 'Enterprises', 'Stores', 'and Sons', 'Industries', 'Agencies', 'Brothers', 'Retail']
PRODUCTS = ['garments', 'stationery', 'electronic goods', 'furniture', 'spices', 'footwear', 'sports goods',
            'handicrafts', 'mobile accessories', 'organic food products', 'textbooks', 'kitchen appliances',
            'leather bags', 'tea', 'toys', 'bicycles', 'medicines', 'handloom sarees']


class Cyc:
    """Walk a list in shuffled order; reshuffle once every entry has been given."""

    def __init__(self, items):
        self.items = list(items)
        self.order: list[int] = []

    def next(self, r: random.Random):
        if not self.order:
            self.order = list(range(len(self.items)))
            r.shuffle(self.order)
        return self.items[self.order.pop()]

    def __len__(self):
        return len(self.items)


def person(r):
    return r.choice(GIRLS + BOYS)


def firm(r):
    return f'{r.choice(SURNAMES)} {r.choice(FIRM_SUFFIX)}'


def ctx(r) -> dict:
    """Placeholder values for scenario text: {p} {p2} {p3} person names ({his} {He} {he} {him} agree with {p}), {s} surname, {c} {c2} cities,
    {f} {f2} firm names, {g} a product line."""
    p = r.sample(GIRLS + BOYS, 3)
    c = r.sample(CITIES, 2)
    s = r.sample(SURNAMES, 2)
    fem = p[0] in GIRLS
    return {'his': 'her' if fem else 'his', 'His': 'Her' if fem else 'His', 'he': 'she' if fem else 'he', 'He': 'She' if fem else 'He',
            'him': 'her' if fem else 'him',
            'p': p[0], 'p2': p[1], 'p3': p[2], 's': s[0], 'c': c[0], 'c2': c[1],
            'f': f'{s[0]} {r.choice(FIRM_SUFFIX)}', 'f2': f'{s[1]} {r.choice(FIRM_SUFFIX)}',
            'g': r.choice(PRODUCTS)}


def fill(text: str, d: dict) -> str:
    return text.format(**d) if '{' in text else text


def FF(C, D, type_, gen, marks=None, kinds=(), gap=None):
    """Family with minutes scaled from marks (about 1.5 to 2 minutes a mark)."""
    kw = {}
    if marks is not None:
        kw['marks'] = marks
        kw['minutes'] = {1: 1, 2: 3, 3: 5, 4: 6, 5: 8, 6: 9}.get(marks, marks * 1.5)
    if gap:
        kw['gap'] = gap
    return F(C, D, type_, gen, kinds=tuple(kinds), **kw)


def _sq(text, q):
    return text if text.endswith('?') else f'{text} {q}'


def _ord(i):
    return '(' + ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi', 'xii', 'xiii', 'xiv', 'xv', 'xvi'][i] + ')'


# ---------------------------------------------------------------- fact families

def facts(spec: dict) -> list:
    """Families from a fact table. Keys (all optional):

    cat     noun for the terms, e.g. 'accounting term'
    terms   [(term, definition)]                 definition must not name the term
    lists   [(key, title, [(point, explanation)], contrast_key|None)]
            title reads after 'the', e.g. 'merits of sole proprietorship'
    pairs   [(X, Y, [(basis, x_text, y_text)])]
    scen    [(question, pool, [(scenario, answer, why)], feat_key|None)]
            answers must be in pool; scenarios may use {p} {c} {f} ... placeholders.
            feat_key: optional dict key in spec['feat'] mapping answer -> [features] for C4 cases
    feat    {name: {answer: [feature, ...]}}
    ars     [(assertion, reason, code, why)]
    tf      (topic, [true statements], [false statements])
    cases   [(C, D, marks, text, [(question, answer)])]   4- or 6-mark case/HOTS items
    levels  overrides, e.g. {'scen_mcq': ('C3','D2')}
    """
    out = []
    lv = {'term_id': ('C1', 'D1'), 'term_desc': ('C1', 'D2'), 'term_def': ('C1', 'D2'),
          'list_which': ('C1', 'D1'), 'list_odd': ('C2', 'D2'), 'list_state': ('C1', 'D2'),
          'list_two': ('C2', 'D3'), 'list_long': ('C2', 'D4'), 'pair_mcq': ('C2', 'D2'), 'pair_one': ('C2', 'D2'),
          'pair3': ('C2', 'D3'), 'pair6': ('C2', 'D4'), 'scen_mcq': ('C3', 'D2'), 'scen_just': ('C3', 'D3'),
          'scen_two': ('C3', 'D4'), 'scen_feat': ('C4', 'D3'), 'ar': ('C2', 'D3'), 'tf_true': ('C2', 'D2'),
          'tf_false': ('C2', 'D3')}
    lv.update(spec.get('levels', {}))
    cat = spec.get('cat', 'term')

    terms = spec.get('terms') or []
    if len(terms) >= 4:
        ti = Cyc(terms)
        td = Cyc(terms)
        tdef = Cyc(terms)

        def term_id(r, ti=ti):
            t, d = ti.next(r)
            others = [x[0] for x in terms if x[0] != t]
            return mcq(f'Which {cat} is described here? "{d}"', t, r.sample(others, 3), f'{t}: {d}', r)

        def term_desc(r, td=td):
            t, d = td.next(r)
            others = [x[1] for x in terms if x[0] != t]
            return mcq(f'Which of the following best describes "{t}"?', d, r.sample(others, 3), f'{t}: {d}', r)

        def term_def(r, tdef=tdef):
            t, d = tdef.next(r)
            return {'stem': f'What is meant by "{t}"?', 'answer': d, 'key': f'1 mark: {d}'}

        out += [FF(*lv['term_id'], 'mcq', term_id), FF(*lv['term_desc'], 'mcq', term_desc),
                FF(*lv['term_def'], 'short', term_def, marks=1)]

    lists = {k: (title, pts, con) for (k, title, pts, con) in (spec.get('lists') or [])}
    for k, (title, pts, con) in lists.items():
        if con and con in lists and len(lists[con][1]) >= 3 and len(pts) >= 3:
            cpts = lists[con][1]
            ctitle = lists[con][0]

            def which(r, title=title, pts=pts, cpts=cpts, ctitle=ctitle):
                p = r.choice(pts)
                return mcq(f'Which of the following is one of the {title}?', p[0], [x[0] for x in r.sample(cpts, 3)],
                           f'"{p[0]}" is one of the {title}; the others are {ctitle}.', r)

            def odd(r, title=title, pts=pts, cpts=cpts, ctitle=ctitle):
                c = r.choice(cpts)
                return mcq(f'Which of the following is NOT one of the {title}?', c[0], [x[0] for x in r.sample(pts, 3)],
                           f'"{c[0]}" is one of the {ctitle}, not one of the {title}.', r)

            out += [FF(*lv['list_which'], 'mcq', which), FF(*lv['list_odd'], 'mcq', odd)]
        if len(pts) >= 3:
            def state(r, title=title, pts=pts):
                lst = '; '.join(p[0] for p in pts)
                return {'stem': f'State any three {title}.', 'answer': lst,
                        'key': f'Any three of: {lst} (1 mark each).'}

            def two(r, title=title, pts=pts):
                a, b = r.sample(pts, 2)
                return {'stem': f'Explain the following {title}: (i) {a[0]} (ii) {b[0]}.',
                        'answer': f'(i) {a[0]}: {a[1]} (ii) {b[0]}: {b[1]}',
                        'key': f'2 marks each: (i) {a[1]} (ii) {b[1]}'}

            out += [FF(*lv['list_state'], 'explain', state, marks=3, kinds=('m3',)),
                    FF(*lv['list_two'], 'explain', two, marks=4, kinds=('m4',))]
        if len(pts) >= 4:
            def long_(r, title=title, pts=pts):
                k = 6 if len(pts) >= 6 else 4
                word = {4: 'four', 6: 'six'}[k]
                each = '1 mark' if k == 6 else '1½ marks'
                body = ' '.join(f'{_ord(i)} {p[0]}: {p[1]}' for i, p in enumerate(pts))
                return {'stem': f'Explain any {word} {title}.', 'answer': body,
                        'key': f'Any {word} points, {each} each (heading and explanation): {body}'}

            out.append(FF(*lv['list_long'], 'long', long_, marks=6, kinds=('m6',)))

    for (X, Y, bases) in spec.get('pairs') or []:
        if len(bases) >= 3:
            def pair_mcq(r, X=X, Y=Y, bases=bases):
                b = r.sample(bases, 3)
                cap = lambda t: t[0].upper() + t[1:]
                good = f'{cap(b[0][0])}: {b[0][1]}'
                wrong = [f'{cap(x[0])}: {x[2]}' for x in b]
                return mcq(f'Which of the following is true of {X} but not of {Y}?', good, wrong,
                           f'{X}: {good}. The other options describe {Y}.', r)

            def pair_one(r, X=X, Y=Y, bases=bases):
                b = r.choice(bases)
                return {'stem': f'State one difference between {X} and {Y} on the basis of {b[0]}.',
                        'answer': f'{X}: {b[1]}; {Y}: {b[2]}', 'key': f'1 mark: {X}: {b[1]}; {Y}: {b[2]}'}

            def pair_k(r, X=X, Y=Y, bases=bases, k=3):
                bs = r.sample(bases, k)
                names = ', '.join(x[0] for x in bs[:-1]) + ' and ' + bs[-1][0]
                body = ' '.join(f'{_ord(i)} {x[0][0].upper() + x[0][1:]}: {X}: {x[1]}; {Y}: {x[2]}.' for i, x in enumerate(bs))
                return {'stem': f'Distinguish between {X} and {Y} on the basis of {names}.', 'answer': body,
                        'key': f'1 mark for each basis: {body}'}

            def pair4(r, f=pair_k):
                return f(r, k=4)

            out += [FF(*lv['pair_mcq'], 'mcq', pair_mcq), FF(*lv['pair_one'], 'short', pair_one, marks=1),
                    FF(*lv['pair3'], 'explain', pair_k, marks=3, kinds=('m3',))]
            if len(bases) >= 4:
                out.append(FF(*lv['pair3'], 'explain', pair4, marks=4, kinds=('m4',)))
            if len(bases) >= 6:
                def pair6(r, X=X, Y=Y, bases=bases):
                    bs = r.sample(bases, 6)
                    body = ' '.join(f'{_ord(i)} {x[0][0].upper() + x[0][1:]}: {X}: {x[1]}; {Y}: {x[2]}.' for i, x in enumerate(bs))
                    return {'stem': f'Distinguish between {X} and {Y} on any six bases.', 'answer': body,
                            'key': f'1 mark for each basis (any six relevant bases): {body}'}
                out.append(FF(*lv['pair6'], 'long', pair6, marks=6, kinds=('m6',)))

    feat = spec.get('feat') or {}
    for (q, pool, items, fk) in spec.get('scen') or []:
        if not items:
            continue
        c1 = Cyc(items)
        c2 = Cyc(items)

        def scen_mcq(r, q=q, pool=pool, c=c1):
            text, ans, why = c.next(r)
            d = ctx(r)
            others = [p for p in pool if p != ans]
            return mcq(_sq(fill(text, d), q), ans, r.sample(others, 3), f'{ans}. {fill(why, d)}', r)

        def scen_just(r, q=q, pool=pool, c=c2):
            text, ans, why = c.next(r)
            d = ctx(r)
            others = [p for p in pool if p != ans]
            return {'stem': _sq(fill(text, d), q) + ' Justify your answer.', 'answer': f'{ans}. {fill(why, d)}',
                    'key': f'1 mark for identifying {ans}; 2 marks for the justification: {fill(why, d)}',
                    'distractors': r.sample(others, 3)}

        out += [FF(*lv['scen_mcq'], 'mcq', scen_mcq),
                FF(*lv['scen_just'], 'explain', scen_just, marks=3, kinds=('m3',))]
        answers = {i[1] for i in items}
        if len(answers) >= 2:
            def scen_two(r, q=q, items=items):
                a = r.choice(items)
                b = r.choice([i for i in items if i[1] != a[1]])
                d = ctx(r)
                lead = q if not (a[0].endswith('?') or b[0].endswith('?')) else 'Answer each part.'
                return {'stem': f'{lead} In each case give a reason. {_ord(0)} {fill(a[0], d)} {_ord(1)} {fill(b[0], d)}',
                        'answer': f'(i) {a[1]}: {fill(a[2], d)} (ii) {b[1]}: {fill(b[2], d)}',
                        'key': f'2 marks each (1 identification + 1 reason): (i) {a[1]} (ii) {b[1]}'}
            out.append(FF(*lv['scen_two'], 'explain', scen_two, marks=4, kinds=('m4',), gap='G7'))
        if fk and fk in feat:
            fmap = feat[fk]
            fitems = [i for i in items if i[1] in fmap and len(fmap[i[1]]) >= 2]
            if fitems:
                c3 = Cyc(fitems)

                def scen_feat(r, q=q, c=c3, fmap=fmap):
                    text, ans, why = c.next(r)
                    d = ctx(r)
                    fs = fmap[ans]
                    return {'stem': f'{fill(text, d)} (i) {q if not text.endswith("?") else "Answer the question above."} (ii) State two other features of it that would matter in this situation.',
                            'answer': f'(i) {ans}: {fill(why, d)} (ii) Any two of: ' + '; '.join(fs),
                            'key': f'(i) identification with reason, 2 marks; (ii) any two relevant features, 1 mark each: ' + '; '.join(fs)}
                out.append(FF(*lv['scen_feat'], 'case', scen_feat, marks=4, kinds=('m4', 'case'), gap='G7'))

    ars = spec.get('ars') or []
    if ars:
        ca = Cyc(ars)

        def ar_gen(r, ca=ca):
            a, b, code, why = ca.next(r)
            return ar(a, b, code, why)
        out.append(FF(*lv['ar'], 'mcq', ar_gen, kinds=('ar',)))

    tf = spec.get('tf')
    if tf:
        topic, trues, falses = tf
        if len(trues) >= 1 and len(falses) >= 3:
            def tf_true(r):
                t = r.choice(trues)
                return mcq(f'Which of the following statements about {topic} is correct?', t, r.sample(falses, 3),
                           f'Correct: {t}', r)
            out.append(FF(*lv['tf_true'], 'mcq', tf_true))
        if len(trues) >= 3 and len(falses) >= 1:
            def tf_false(r):
                f = r.choice(falses)
                return mcq(f'Which of the following statements about {topic} is NOT correct?', f, r.sample(trues, 3),
                           f'Incorrect statement: {f}', r)
            out.append(FF(*lv['tf_false'], 'mcq', tf_false))

    groups = {}
    for cs in spec.get('cases') or []:
        groups.setdefault((cs[0], cs[1], cs[2]), []).append(cs)
    for (C, D, marks), cs in groups.items():
        cc = Cyc(cs)

        def case(r, cc=cc):
            _, _, mk, text, parts = cc.next(r)
            d = ctx(r)
            qs = ' '.join(f'{_ord(i)} {fill(q, d)}' for i, (q, a) in enumerate(parts))
            ans = ' '.join(f'{_ord(i)} {fill(a, d)}' for i, (q, a) in enumerate(parts))
            return {'stem': f'{fill(text, d)}\n{qs}', 'answer': ans, 'key': f'{mk} marks: {ans}'}
        kind = 'm6' if marks == 6 else 'm4'
        out.append(FF(C, D, 'case', case, marks=marks, kinds=(kind, 'case'), gap='G7'))
    return out


# ---------------------------------------------------------------- accounting formatting

def amt(r, lo, hi, step=500):
    return r.randrange(lo // step, hi // step + 1) * step


def entry(dr, cr) -> str:
    """dr, cr: lists of (account, amount). Returns 'A A/c Dr ₹x; B A/c Dr ₹y; To C A/c ₹z'."""
    parts = [f'{a} Dr {inr(x)}' for a, x in dr] + [f'To {a} {inr(x)}' for a, x in cr]
    return '; '.join(parts)


def acc(a: str) -> str:
    """Account name with A/c suffix."""
    return a if a.endswith('A/c') else f'{a} A/c'


def pa(n: str) -> str:
    """Personal account name in NCERT style."""
    return f"{n}'s A/c"
