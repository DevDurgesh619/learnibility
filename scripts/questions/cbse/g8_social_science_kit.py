"""Fact-table family kit for the CBSE social science banks (classes 8, 9 and 10).

Used by g8_social_science.py, g9_social_science.py and g10_social_science.py. Each subtopic is
described by a small fact table; this module turns the tables into qbank families.

Subtopic table keys (all optional except that every subtopic needs enough to reach C1-C4):
    T     [(term, definition)]                        definition: lower-case noun phrase, no full stop,
                                                      must not contain the term itself
    FB    [(sentence with ___, answer, [3 wrong])]   wrong answers same category and clearly wrong
    EX    [(C, D, question, [points])]                2 points -> 2-mark item, 3+ points -> 3-mark item
    AR    [(assertion, reason, code, why)]            hand-written Assertion-Reason (code a-d)
    SC    [(stem, correct, [3 wrong], why)]           application / scenario MCQ (C3)
    CAT   [(singular, plural, [members], [non-members])]
    CHRON [(event, year)]                             pooled per chapter for ordering items
    CASE  [(intro, source, [(question, answer, marks)])]   marks add to 4
    LONG  [(D, question, [5 points])]
    MAP   [(label description, place, location note, map)]   map is 'India' or 'world'
    MAPK  'map2' or 'map3' or 'both' (which mock map slot this subtopic's MAP rows serve)
    GEN   [(C, D, type, generator[, F kwargs])]      computed items (numbers worked out in code)
"""
from __future__ import annotations

import itertools

from qbank import F, ar, mcq

ROMAN = ['I', 'II', 'III', 'IV', 'V']


def cap(s: str) -> str:
    return s[:1].upper() + s[1:] if s else s


def fill(sentence: str, word: str) -> str:
    out = sentence.replace('___', word, 1)
    return cap(out) if sentence.startswith('___') else out


def blank(sentence: str) -> str:
    return sentence.replace('___', '______', 1)


def yr(y: int) -> str:
    if y < 0:
        return f'{-y} BCE'
    if y < 1000:
        return f'{y} CE'
    return str(y)


def pts(points: list, n: int | None = None) -> str:
    return ' '.join(f'({i + 1}) {cap(p)}.' for i, p in enumerate(points[:n] if n else points))


# ------------------------------------------------------------------ family factories

def _term_mcq(terms, pool):
    def g(r):
        t, d = r.choice(terms)
        others = [x for x, _ in pool if x != t]
        wrong = r.sample(others, 3)
        form = r.randrange(2)
        stem = f'Which term is used for {d}?' if form == 0 else f'Identify the correct term for the following description: {cap(d)}.'
        return mcq(stem, cap(t), [cap(w) for w in wrong], f'{cap(t)}: {d}.', r)
    return g


def _term_rev(terms, pool):
    def g(r):
        t, d = r.choice(terms)
        others = [y for x, y in pool if x != t]
        wrong = r.sample(others, 3)
        return mcq(f"Which of the following correctly describes '{t}'?", cap(d), [cap(w) for w in wrong],
                   f"'{cap(t)}' means {d}; the other options describe other terms of this chapter.", r)
    return g


def _term_def(terms, pool):
    def g(r):
        t, d = r.choice(terms)
        form = r.randrange(2)
        stem = f"What is meant by '{t}'?" if form == 0 else f"Define the term '{t}'."
        others = [y for x, y in pool if x != t]
        return {'stem': stem, 'answer': cap(d) + '.',
                'key': f'1 mark for the idea: {d}.',
                'distractors': [cap(w) + '.' for w in r.sample(others, min(3, len(others)))]}
    return g


def _fb_mcq(fbs):
    def g(r):
        s, a, wrong = r.choice(fbs)
        return mcq(f'Choose the correct option to complete the statement: {blank(s)}', a, wrong,
                   f'{fill(s, a)}', r)
    return g


def _fb_short(fbs):
    def g(r):
        s, a, wrong = r.choice(fbs)
        return {'stem': f'Fill in the blank: {blank(s)}', 'answer': a,
                'key': f'{fill(s, a)} (1 mark)', 'distractors': list(wrong)}
    return g


def _tf(fbs):
    def g(r):
        s, a, wrong = r.choice(fbs)
        if r.random() < 0.45:
            return {'stem': f'State whether the statement is True or False: {fill(s, a)}',
                    'answer': 'True', 'key': f'True. {fill(s, a)}'}
        w = r.choice(wrong)
        return {'stem': f'State whether the statement is True or False. If false, correct it: {fill(s, w)}',
                'answer': f'False. {fill(s, a)}',
                'key': f"False (½ mark); correction: '{a}' in place of '{w}' (½ mark). {fill(s, a)}"}
    return g


def _ar_auto(fbs):
    def g(r):
        (s1, a1, w1), (s2, a2, w2) = r.sample(fbs, 2)
        if r.random() < 0.5:
            bad = r.choice(w2)
            return ar(fill(s1, a1), fill(s2, bad), 'c',
                      f'A is true. R is false: {fill(s2, a2)}')
        bad = r.choice(w1)
        return ar(fill(s1, bad), fill(s2, a2), 'd',
                  f'A is false: {fill(s1, a1)} R is true.')
    return g


def _ar_hand(rows):
    def g(r):
        a, rr, code, why = r.choice(rows)
        return ar(a, rr, code, why)
    return g


def _sc(rows):
    def g(r):
        stem, c, wrong, why = r.choice(rows)
        return mcq(stem, c, wrong, why, r)
    return g


def _odd(cats):
    def g(r):
        sing, plur, mem, non = r.choice(cats)
        if r.random() < 0.5:
            three = [cap(x) for x in r.sample(mem, 3)]
            odd = cap(r.choice(non))
            return mcq(f'Which of the following is NOT {sing}?', odd, three,
                       f'{odd} is not {sing}; {", ".join(three)} are {plur}.', r)
        one = cap(r.choice(mem))
        wrong = [cap(x) for x in r.sample(non, 3)]
        return mcq(f'Which of the following is {sing}?', one, wrong,
                   f'{one} is {sing}; {", ".join(wrong)} are not.', r)
    return g


def _name_two(cats):
    def g(r):
        sing, plur, mem, non = r.choice(cats)
        n = r.choice([2, 2, 3]) if len(mem) >= 3 else 2
        word = {2: 'two', 3: 'three'}[n]
        if n == 3:
            return {'stem': f'Name any three {plur}.', 'answer': f'Any three of: {", ".join(mem)}.',
                    'key': f'Any three correct: {", ".join(mem)} (2 marks for three, 1 mark for two).', 'marks': 2, 'minutes': 2}
        return {'stem': f'Name any {word} {plur}.', 'answer': f'Any {word} of: {", ".join(mem)}.',
                'key': f'1 mark each for any {word} correct: {", ".join(mem)}.', 'marks': 2, 'minutes': 2}
    return g


def _chron(events):
    def g(r):
        evs = r.sample(events, 4)
        if len({y for _, y in evs}) < 4:
            raise ValueError('equal years')
        order = sorted(range(4), key=lambda i: evs[i][1])
        right = ', '.join(ROMAN[i] for i in order)
        wrong = set()
        while len(wrong) < 3:
            p = list(order)
            r.shuffle(p)
            s = ', '.join(ROMAN[i] for i in p)
            if s != right:
                wrong.add(s)
        lines = '\n'.join(f'{ROMAN[i]}. {cap(e)}' for i, (e, _) in enumerate(evs))
        key = '; '.join(f'{cap(evs[i][0])} ({yr(evs[i][1])})' for i in order)
        return mcq(f'Arrange the following in chronological order (earliest first):\n{lines}', right, sorted(wrong), key + '.', r)
    return g


def _chron_first(events):
    def g(r):
        evs = r.sample(events, 4)
        if len({y for _, y in evs}) < 4:
            raise ValueError('equal years')
        late = r.random() < 0.4
        tgt = (max if late else min)(evs, key=lambda e: e[1])
        word = 'latest (most recent)' if late else 'earliest'
        return mcq(f'Which of the following happened {word}?', cap(tgt[0]), [cap(e) for e, _ in evs if e != tgt[0]],
                   '; '.join(f'{cap(e)} ({yr(y)})' for e, y in sorted(evs, key=lambda e: e[1])) + '.', r)
    return g


def _year(events, all_years):
    def g(r):
        e, y = r.choice(events)
        cands = sorted({yy for yy in all_years if yy != y}, key=lambda yy: abs(yy - y))[:6]
        if len(cands) < 3:
            cands += [y + d for d in (-3, 2, 5, -7) if y + d not in cands]
        wrong = r.sample(cands[:6], 3)
        return mcq(f'In which year did the following take place: {e}?', yr(y), [yr(w) for w in wrong],
                   f'{cap(e)}: {yr(y)}.', r)
    return g


def _match(terms, pool):
    def g(r):
        own = r.sample(terms, min(len(terms), 2))
        rest = [p for p in pool if p not in own]
        four = own + r.sample(rest, 4 - len(own))
        r.shuffle(four)
        perm = list(range(4))
        r.shuffle(perm)            # perm[i] = position in column B of the description of term i
        letters = 'pqrs'
        colb = [None] * 4
        for i, j in enumerate(perm):
            colb[j] = four[i][1]
        right = ', '.join(f'{i + 1}-{letters[perm[i]]}' for i in range(4))
        wrong = set()
        while len(wrong) < 3:
            p = list(range(4))
            r.shuffle(p)
            s = ', '.join(f'{i + 1}-{letters[p[i]]}' for i in range(4))
            if s != right:
                wrong.add(s)
        a = '\n'.join(f'{i + 1}. {cap(t)}' for i, (t, _) in enumerate(four))
        b = '\n'.join(f'({letters[j]}) {cap(colb[j])}' for j in range(4))
        return mcq(f'Match Column A with Column B and choose the correct option.\nColumn A:\n{a}\nColumn B:\n{b}', right, sorted(wrong),
                   '; '.join(f'{cap(t)} – {d}' for t, d in four) + '.', r)
    return g


def _ex(rows):
    def g(r):
        C, D, q, p = r.choice(rows)
        n = len(p)
        if n == 2:
            return {'stem': q, 'answer': pts(p), 'key': f'1 mark each: {pts(p)}', 'marks': 2, 'minutes': 3}
        return {'stem': q, 'answer': pts(p),
                'key': f'1 mark each for any three points: {pts(p)}', 'marks': 3, 'minutes': 5}
    return g


def _case_hand(rows):
    def g(r):
        intro, src, qs = r.choice(rows)
        parts = '\n'.join(f'({"i" * (k + 1) if k < 3 else "iv"}) {q} ({m} mark{"s" if m > 1 else ""})' for k, (q, a, m) in enumerate(qs))
        ans = ' '.join(f'({"i" * (k + 1) if k < 3 else "iv"}) {a}' for k, (q, a, m) in enumerate(qs))
        return {'stem': f'{intro}\n"{src}"\n{parts}', 'answer': ans,
                'key': ' '.join(f'({"i" * (k + 1) if k < 3 else "iv"}) {m} mark{"s" if m > 1 else ""}: {a}' for k, (q, a, m) in enumerate(qs)),
                'marks': 4, 'minutes': 6}
    return g


def _case_cloze(fbs, exs, topic, grade):
    def g(r):
        (s1, a1, _), (s2, a2, _) = r.sample(fbs, 2)
        if a1.lower() == a2.lower():
            raise ValueError('same answer in both blanks')
        two = [x for x in exs if len(x[3]) == 2]
        C, D, q, p = r.choice(two or exs)
        note = f'{blank(s1).replace("______", "(A) ______")} {blank(s2).replace("______", "(B) ______")}'
        tail = q
        return {'stem': (f'Read the revision note prepared by a Class {grade} student on "{topic}" and answer the questions that follow.\n'
                         f'"{note}"\n(i) Fill in blank (A). (1 mark)\n(ii) Fill in blank (B). (1 mark)\n(iii) {tail} (2 marks)'),
                'answer': f'(i) {a1} (ii) {a2} (iii) {pts(p, 2) if len(p) == 2 else pts(p)}',
                'key': f'(i) {a1} – 1 mark. (ii) {a2} – 1 mark. (iii) any two points, 1 mark each: {pts(p)}',
                'marks': 4, 'minutes': 6}
    return g


def _long_hand(rows):
    def g(r):
        D, q, p = r.choice(rows)
        return {'stem': q, 'answer': pts(p), 'key': f'1 mark each for any five points: {pts(p)}', 'marks': 5, 'minutes': 8}
    return g


def _long_combo(c4s, others):
    def g(r):
        C, D, q1, p1 = r.choice(c4s)
        rest = [o for o in others if o[2] != q1]
        C2, D2, q2, p2 = r.choice([o for o in rest if len(o[3]) == 2] or rest)
        q2s = q2
        return {'stem': f'(a) {q1} (3 marks)\n(b) {q2s} (2 marks)',
                'answer': f'(a) {pts(p1)} (b) {pts(p2)}',
                'key': f'(a) any three points, 1 mark each: {pts(p1)} (b) any two points, 1 mark each: {pts(p2)}',
                'marks': 5, 'minutes': 8}
    return g


def _map(rows, n, kind_label):
    def g(r):
        grp = r.choice(sorted({m for *_, m in rows}))
        sub = [x for x in rows if x[3] == grp]
        if len(sub) < n:
            raise ValueError('too few map rows')
        pick = r.sample(sub, n)
        letters = 'abc'
        body = ' '.join(f'({letters[i]}) {cap(d)}' for i, (d, *_rest) in enumerate(pick))
        ans = ' '.join(f'({letters[i]}) {p} – {loc}' for i, (d, p, loc, _) in enumerate(pick))
        return {'stem': f'On an outline political map of {"India" if grp == "India" else "the world"}, locate and label the following: {body}',
                'answer': ans, 'key': f'1 mark for each correct location: {ans}', 'marks': n, 'minutes': n + 1}
    return g


# ------------------------------------------------------------------ assembly

def build(prefix: str, data: dict, names: dict | None = None, grade: int = 8) -> dict:
    """data: {'01-st1': table, ...}. Returns {subtopicId: [Family]}."""
    names = names or {}
    chapters: dict[str, list[str]] = {}
    for k in data:
        chapters.setdefault(k.split('-')[0], []).append(k)
    fams = {}
    for ch, keys in chapters.items():
        pool_t = [t for k in keys for t in data[k].get('T', [])]
        pool_ev = [e for k in keys for e in data[k].get('CHRON', [])]
        years = [y for _, y in pool_ev]
        for k in keys:
            d = data[k]
            out = []
            T, FB, EX = d.get('T', []), d.get('FB', []), d.get('EX', [])
            if T and len(pool_t) >= 4:
                out += [F('C1', 'D1', 'mcq', _term_mcq(T, pool_t), gap='G4'),
                        F('C1', 'D2', 'short', _term_def(T, pool_t)),
                        F('C2', 'D2', 'mcq', _term_rev(T, pool_t))]
                if len(pool_t) >= 5:
                    out.append(F('C3', 'D3', 'mcq', _match(T, pool_t)))
            if FB:
                out += [F('C1', 'D2', 'mcq', _fb_mcq(FB)), F('C1', 'D1', 'short', _fb_short(FB), gap='G4'),
                        F('C2', 'D2', 'short', _tf(FB))]
            if len(FB) >= 2:
                out.append(F('C2', 'D3', 'mcq', _ar_auto(FB), kinds=('ar',)))
            if d.get('AR'):
                out.append(F('C3', 'D3', 'mcq', _ar_hand(d['AR']), kinds=('ar',)))
            if d.get('SC'):
                out.append(F('C3', 'D2', 'mcq', _sc(d['SC'])))
            if d.get('CAT'):
                out.append(F('C3', 'D1', 'mcq', _odd(d['CAT'])))
                if any(len(c[2]) >= 3 for c in d['CAT']):
                    out.append(F('C2', 'D2', 'short', _name_two([c for c in d['CAT'] if len(c[2]) >= 3]), kinds=('sa2',)))
            if d.get('CHRON') and len(pool_ev) >= 4:
                evs = d['CHRON']
                use = pool_ev if len(evs) < 6 else evs
                out += [F('C3', 'D3', 'mcq', _chron(use)), F('C3', 'D2', 'mcq', _chron_first(use)),
                        F('C1', 'D1', 'mcq', _year(evs, years), gap='G4')]
            groups: dict[tuple, list] = {}
            for row in EX:
                C, D, q, p = row
                groups.setdefault((C, D, 2 if len(p) == 2 else 3), []).append(row)
            for (C, D, n), rows in groups.items():
                out.append(F(C, D, 'explain', _ex(rows), kinds=('sa2',) if n == 2 else ('sa3',),
                             gap='G5' if C == 'C4' else None))
            if d.get('CASE'):
                out.append(F('C3', 'D4', 'case', _case_hand(d['CASE']), gap='G7'))
            if len(FB) >= 2 and EX:
                out.append(F('C3', 'D3', 'case', _case_cloze(FB, EX, names.get(k, 'this topic').split(':')[0], grade), gap='G7'))
            if d.get('LONG'):
                for D in sorted({x[0] for x in d['LONG']}):
                    out.append(F('C4', D, 'long', _long_hand([x for x in d['LONG'] if x[0] == D]), kinds=('la5',), gap='G5'))
            c4 = [x for x in EX if x[0] == 'C4' and len(x[3]) >= 3]
            if c4 and len(EX) >= 2:
                out.append(F('C4', 'D4', 'long', _long_combo(c4, EX), kinds=('la5',), gap='G5'))
            if d.get('MAP'):
                mk = d.get('MAPK', 'both')
                if mk in ('map2', 'both'):
                    out.append(F('C1', 'D2', 'short', _map(d['MAP'], 2, 'map2'), kinds=('map2',), marks=2, minutes=3))
                if mk in ('map3', 'both'):
                    out.append(F('C1', 'D2', 'short', _map(d['MAP'], 3, 'map3'), kinds=('map3',), marks=3, minutes=4))
            for row in d.get('GEN', []):
                C, D, typ, fn = row[:4]
                kw = row[4] if len(row) > 4 else {}
                out.append(F(C, D, typ, fn, **kw))
            fams[f'{prefix}{k}'] = out
    return fams


def check(fams: dict) -> list[str]:
    """Report subtopics missing a concept group (the validator needs C1-C4 in every subtopic bank)."""
    bad = []
    for st, fs in fams.items():
        have = {f.C for f in fs}
        miss = {'C1', 'C2', 'C3', 'C4'} - have
        if miss:
            bad.append(f'{st}: missing {sorted(miss)}')
    return bad


def map_rows(*rows):
    return list(rows)
