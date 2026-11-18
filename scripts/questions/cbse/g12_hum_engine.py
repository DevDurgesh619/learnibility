"""Fact-table engine for the CBSE class 12 humanities banks (history, political science, geography).

Each subtopic is described in a small line-based format (one fact per line):

    T: term | meaning (noun phrase)                     key term
    Q: question | answer | wrong 1 | wrong 2 | wrong 3  recall fact with same-category distractors
    Y: year | event (noun phrase)                       dated event (only firm CE dates)
    P: place | clue                                     place for map work
    M:category: left | right                            matching pair (pairs of one category are matched together)
    S+: true statement
    S-: false statement | corrected statement
    C: assertion | reason that explains it
    X: C3 D3 3 | stem | model answer                    hand-written short/explain item (C, D, marks)
    L: D4 | stem | answer points                        hand-written long answer (C4)

`families(chapter_specs, cfg)` turns them into qbank Family objects: recall MCQs (decks, so a fact
is never asked twice in the same form), term items, matching and Match-List items, statement MCQs,
Assertion-Reason items, chronology, map items, reason/examine items, source-based (case) items and
the hand-written short and long items. Combinatorial families (statements, A-R, matching, sources)
give the many parallel variants the practice forms and mocks need.

`strict_fits` replaces qbank._fits for these subjects so that a long-answer section only takes
long-answer families, a source-based section only takes source items and the map section only map items.
"""
from __future__ import annotations

import itertools
import random
import re

import qbank
from qbank import F, AR_OPTIONS, DNUM

ROMAN = ['I', 'II', 'III', 'IV']


# ---------------------------------------------------------------- parsing

class Sub:
    def __init__(self, sid: str, topic: str, text: str):
        self.sid, self.topic = sid, topic
        self.T, self.Q, self.Y, self.P, self.M = [], [], [], [], []
        self.Sp, self.Sm, self.C, self.X, self.L = [], [], [], [], []
        for raw in text.strip().splitlines():
            line = raw.strip()
            if not line or line.startswith('#'):
                continue
            tag, _, rest = line.partition(':')
            if tag == 'M':
                cat, _, rest = rest.partition(':')
                parts = [p.strip() for p in rest.split(' | ')]
                assert len(parts) == 2, line
                self.M.append((cat.strip(), parts[0], parts[1]))
                continue
            parts = [p.strip() for p in rest.split(' | ')]
            if tag == 'T':
                assert len(parts) == 2, line
                self.T.append(tuple(parts))
            elif tag == 'Q':
                assert len(parts) == 5, line
                assert len({p.lower() for p in parts[1:]}) == 4, line
                self.Q.append(tuple(parts))
            elif tag == 'Y':
                assert len(parts) == 2 and parts[0].isdigit(), line
                self.Y.append((int(parts[0]), parts[1]))
            elif tag == 'P':
                assert len(parts) == 2, line
                self.P.append(tuple(parts))
            elif tag == 'S+':
                assert len(parts) == 1, line
                self.Sp.append(parts[0])
            elif tag == 'S-':
                assert len(parts) == 2, line
                self.Sm.append(tuple(parts))
            elif tag == 'C':
                assert len(parts) == 2, line
                self.C.append(tuple(parts))
            elif tag == 'X':
                assert len(parts) == 3, line
                tags = parts[0].split()
                self.X.append((tags[0], tags[1], float(tags[2]) if len(tags) > 2 else None, parts[1], parts[2]))
            elif tag == 'L':
                assert len(parts) == 3, line
                self.L.append((parts[0], parts[1], parts[2]))
            else:
                raise ValueError(f'{sid}: bad line {line}')


def ST(sid: str, topic: str, text: str) -> Sub:
    return Sub(sid, topic, text)


# ---------------------------------------------------------------- helpers

def deck(items, recycle: bool = False):
    """Generator factory that hands out each item once (raises IndexError when used up).

    recycle=True reshuffles when empty: for fixed-text items (hand-written X/L lines) whose exact repeats the
    builder's stem check rejects, so an item drawn but not kept (balancing, mock retries) can be drawn again."""
    state = {'left': None}

    def take(r: random.Random):
        if state['left'] is None or (recycle and not state['left']):
            state['left'] = list(items)
            r.shuffle(state['left'])
        if not state['left']:
            raise IndexError('deck empty')
        return state['left'].pop()
    return take


def cap(s: str) -> str:
    return s[:1].upper() + s[1:] if s else s


def end(s: str) -> str:
    s = s.strip()
    return s if s[-1:] in '.?!' else s + '.'


def lower1(s: str) -> str:
    if len(s) > 1 and s[0].isupper() and s[1].islower() and not s.split()[0] in KEEP_CAPS:
        return s[0].lower() + s[1:]
    return s


KEEP_CAPS = set()


def opts4(r, correct, wrong):
    wrong = [w for w in wrong if w.strip().lower() != correct.strip().lower()]
    seen, ws = {correct.strip().lower()}, []
    for w in wrong:
        k = w.strip().lower()
        if k not in seen:
            ws.append(w)
            seen.add(k)
    if len(ws) < 3:
        raise ValueError('not enough options')
    o = [correct] + ws[:3]
    r.shuffle(o)
    return o


def letter(opts, ans):
    return 'abcd'[opts.index(ans)]


def subset_label(idx: list[int], n: int) -> str:
    if not idx:
        return 'None of them'
    names = [ROMAN[i] for i in idx]
    if len(idx) == n:
        return 'All of them' if n > 2 else 'Both I and II'
    if len(names) == 1:
        return f'{names[0]} only'
    return ' and '.join([', '.join(names[:-1]), names[-1]]) + ' only'


# ---------------------------------------------------------------- family builders

class Chapter:
    def __init__(self, subs: list[Sub], cfg: dict):
        self.subs = subs
        self.cfg = cfg
        self.allT = [t for s in subs for t in s.T]
        self.allQ = [q for s in subs for q in s.Q]
        self.allY = [y for s in subs for y in s.Y]
        self.allP = [p for s in subs for p in s.P]
        self.allM = [m for s in subs for m in s.M]
        self.allC = [c for s in subs for c in s.C]
        self.allSp = [(s.sid, x) for s in subs for x in s.Sp]


def _term_families(ch: Chapter, s: Sub):
    out = []
    if not s.T:
        return out
    pool_meanings = [m for _, m in ch.allT]
    pool_terms = [t for t, _ in ch.allT]
    if len(ch.allT) < 4:
        return out
    d1 = deck(s.T)

    def term_to_def(r):
        t, m = d1(r)
        wrong = r.sample([x for x in pool_meanings if x != m], 3)
        o = opts4(r, cap(m), [cap(w) for w in wrong])
        return {'stem': f"In the study of {s.topic}, the term '{t}' refers to:", 'options': o, 'answer': cap(m),
                'key': f"({letter(o, cap(m))}) '{t}' means {end(m)}"}
    out.append(F('C1', 'D1', 'mcq', term_to_def))
    d2 = deck(s.T)

    def def_to_term(r):
        t, m = d2(r)
        wrong = r.sample([x for x in pool_terms if x != t], 3)
        o = opts4(r, t, wrong)
        return {'stem': f'Which term describes the following? {end(cap(m))}', 'options': o, 'answer': t,
                'key': f'({letter(o, t)}) {t}: {end(m)}'}
    out.append(F('C1', 'D2', 'mcq', def_to_term))
    d3 = deck(s.T)

    def what_is(r):
        t, m = d3(r)
        return {'stem': f"What is meant by '{t}' in the context of {s.topic}?", 'answer': end(cap(m)),
                'key': f"1 mark: {t} correctly explained as {end(m)}"}
    out.append(F('C1', 'D1', 'short', what_is))
    return out


def _q_families(ch: Chapter, s: Sub):
    if not s.Q:
        return []
    d = deck(s.Q)

    def recall(r):
        q, a, *w = d(r)
        o = opts4(r, a, w)
        return {'stem': q, 'options': o, 'answer': a, 'key': f'({letter(o, a)}) {a}.'}
    return [F('C1', 'D2', 'mcq', recall)]


def _year_families(ch: Chapter, s: Sub):
    out = []
    if s.Y:
        d = deck(s.Y)
        years = sorted({y for y, _ in ch.allY})

        def year(r):
            y, e = d(r)
            near = [x for x in years if x != y and abs(x - y) <= 25]
            cands = list(set(near + [y + k for k in (-3, -2, -1, 1, 2, 3, 5, -5, 10, -10)]) - {y})
            # never offer a year that belongs to the same event elsewhere
            cands = [c for c in cands if (c, e) not in ch.allY]
            wrong = r.sample(cands, 3)
            o = opts4(r, str(y), [str(w) for w in wrong])
            o.sort()
            return {'stem': f'In which year did the following take place: {e}?', 'options': o, 'answer': str(y),
                    'key': f'({letter(o, str(y))}) {cap(e)} took place in {y}.'}
        out.append(F('C1', 'D2', 'mcq', year))
    if s.Y and len({y for y, _ in ch.allY}) >= 4:
        def chrono(r):
            own = r.choice(s.Y)
            rest = [x for x in ch.allY if x[0] != own[0]]
            picks = [own]
            for x in r.sample(rest, len(rest)):
                if all(x[0] != p[0] for p in picks):
                    picks.append(x)
                if len(picks) == 4:
                    break
            if len(picks) < 4:
                raise ValueError('not enough events')
            r.shuffle(picks)
            order = sorted(range(4), key=lambda i: picks[i][0])
            lab = lambda perm: ', '.join(ROMAN[i] for i in perm)
            correct = lab(order)
            perms = [p for p in itertools.permutations(range(4)) if list(p) != order]
            wrong = [lab(p) for p in r.sample(perms, 3)]
            o = opts4(r, correct, wrong)
            lines = '\n'.join(f'{ROMAN[i]}. {cap(picks[i][1])}' for i in range(4))
            key = '; '.join(f'{cap(picks[i][1])} ({picks[i][0]})' for i in order)
            return {'stem': f'Arrange the following in chronological order (earliest first):\n{lines}', 'options': o,
                    'answer': correct, 'key': f'({letter(o, correct)}) {key}.'}
        out.append(F('C2', 'D3', 'mcq', chrono))
    return out


def _place_families(ch: Chapter, s: Sub, first_with_places: bool):
    out = []
    if s.P and len(ch.allP) >= 4:
        d = deck(s.P)
        names = [p for p, _ in ch.allP]

        def place(r):
            p, clue = d(r)
            o = opts4(r, p, r.sample([x for x in names if x != p], 3))
            return {'stem': f'Identify the place from the clue: {end(cap(clue))}', 'options': o, 'answer': p,
                    'key': f'({letter(o, p)}) {p}: {end(clue)}'}
        out.append(F('C1', 'D2', 'mcq', place))
    mn = ch.cfg.get('map_n', 5)
    if first_with_places and len(ch.allP) >= mn + 1:
        mapname = ch.cfg.get('map_name', 'an outline map of the Indian subcontinent')

        def map5(r):
            picks = r.sample(ch.allP, mn)
            lines = '\n'.join(f'{chr(65 + i)}. {cap(c)}' for i, (_, c) in enumerate(picks))
            ans = '; '.join(f'{chr(65 + i)} – {p}' for i, (p, _) in enumerate(picks))
            return {'stem': f'On {mapname}, locate and label the following places (described below) related to {ch.cfg["chapter_topic"]}:\n{lines}',
                    'answer': ans, 'key': f'1 mark each for correctly identifying and labelling: {ans}.',
                    'marks': mn, 'minutes': mn + 2}
        out.append(F('C2', 'D3', 'case', map5, kinds=('map',), marks=mn, minutes=mn + 2))
    return out


def _match_families(ch: Chapter, s: Sub):
    out = []
    cats = {}
    for cat, a, b in ch.allM:
        cats.setdefault(cat, []).append((a, b))
    own = [(c, a, b) for c, a, b in s.M if len(cats[c]) >= 4]
    if not own:
        return out
    truth = {(a, b) for _, a, b in ch.allM}
    names = ch.cfg.get('match_names', {})

    def pick(r, n):
        cat, a, b = r.choice(own)
        pool = [p for p in cats[cat] if p != (a, b) and p[0] != a and p[1] != b]
        if len(pool) < n - 1:
            raise ValueError('small category')
        sel = [(a, b)]
        for p in r.sample(pool, len(pool)):
            if all(p[0] != q[0] and p[1] != q[1] for q in sel):
                sel.append(p)
            if len(sel) == n:
                break
        if len(sel) < n:
            raise ValueError('small category')
        return cat, sel

    def correct_pair(r):
        cat, sel = pick(r, 4)
        good = sel[0]
        others = sel[1:]
        rights = [b for _, b in others]
        shifted = rights[1:] + rights[:1]
        wrong = [f'{a} – {b}' for (a, _), b in zip(others, shifted)]
        if any((a, b) in truth for (a, _), b in zip(others, shifted)):
            raise ValueError('accidental true pair')
        c = f'{good[0]} – {good[1]}'
        o = opts4(r, c, wrong)
        return {'stem': f'Which of the following pairs is correctly matched?', 'options': o, 'answer': c,
                'key': f'({letter(o, c)}) {c}. ' + '; '.join(f'{a} – {b}' for a, b in others) + ' are the correct pairs for the others.'}
    out.append(F('C2', 'D2', 'mcq', correct_pair))

    def wrong_pair(r):
        cat, sel = pick(r, 5)
        bad_a, bad_b = sel[0][0], sel[4][1]
        if (bad_a, bad_b) in truth:
            raise ValueError('accidental true pair')
        c = f'{bad_a} – {bad_b}'
        good = [f'{a} – {b}' for a, b in sel[1:4]]
        o = opts4(r, c, good)
        return {'stem': 'Which of the following pairs is NOT correctly matched?', 'options': o, 'answer': c,
                'key': f'({letter(o, c)}) {c} is wrong: {sel[0][0]} goes with {sel[0][1]}.'}
    out.append(F('C2', 'D3', 'mcq', wrong_pair))

    def match_list(r):
        cat, sel = pick(r, 4)
        hn = names.get(cat)
        rights = [b for _, b in sel]
        perm = list(range(4))
        r.shuffle(perm)            # perm[k] = index into sel of the k-th right item
        list2 = [rights[p] for p in perm]
        code = lambda m: ', '.join(f'{chr(65 + i)}-{m[i] + 1}' for i in range(4))
        true_map = [perm.index(i) for i in range(4)]
        others = [list(p) for p in itertools.permutations(range(4)) if list(p) != true_map]
        wrong = [code(p) for p in r.sample(others, 3)]
        c = code(true_map)
        o = opts4(r, c, wrong)
        l1 = '\n'.join(f'{chr(65 + i)}. {a}' for i, (a, _) in enumerate(sel))
        l2 = '\n'.join(f'{i + 1}. {b}' for i, b in enumerate(list2))
        head = f'Match List I ({hn[0]}) with List II ({hn[1]})' if hn else 'Match List I with List II'
        return {'stem': f'{head} and choose the correct option.\nList I:\n{l1}\nList II:\n{l2}',
                'options': o, 'answer': c, 'key': f'({letter(o, c)}) ' + '; '.join(f'{a} – {b}' for a, b in sel) + '.'}
    out.append(F('C3', 'D4', 'mcq', match_list, gap='G5'))
    return out


def _statement_families(ch: Chapter, s: Sub):
    out = []
    if len(s.Sp) + len(s.Sm) < 3 or not s.Sp:
        return out
    items = [(x, True, None) for x in s.Sp] + [(f, False, c) for f, c in s.Sm]
    two_opts = ['I only', 'II only', 'Both I and II', 'Neither I nor II']

    def two(r):
        pk = r.sample(items, 2)
        tv = [p[1] for p in pk]
        c = {(True, False): 'I only', (False, True): 'II only', (True, True): 'Both I and II', (False, False): 'Neither I nor II'}[tuple(tv)]
        o = two_opts[:]
        lines = '\n'.join(f'{ROMAN[i]}. {end(p[0])}' for i, p in enumerate(pk))
        why = ' '.join(f'{ROMAN[i]} is correct.' if p[1] else f'{ROMAN[i]} is incorrect: {end(p[2])}' for i, p in enumerate(pk))
        return {'stem': f'Consider the following statements about {s.topic}:\n{lines}\nWhich of the statements given above is/are correct?',
                'options': o, 'answer': c, 'key': f'({letter(o, c)}) {why}'}
    out.append(F('C2', 'D2', 'mcq', two))

    if len(items) >= 4:
        def three(r):
            pk = r.sample(items, 3)
            idx = [i for i, p in enumerate(pk) if p[1]]
            if not idx:
                raise ValueError('need one true')
            c = subset_label(idx, 3)
            pool = [subset_label(list(x), 3) for k in (1, 2, 3) for x in itertools.combinations(range(3), k)]
            o = opts4(r, c, r.sample([p for p in pool if p != c], 3))
            lines = '\n'.join(f'{ROMAN[i]}. {end(p[0])}' for i, p in enumerate(pk))
            why = ' '.join(f'{ROMAN[i]} is correct.' if p[1] else f'{ROMAN[i]} is incorrect: {end(p[2])}' for i, p in enumerate(pk))
            return {'stem': f'Read the following statements about {s.topic}:\n{lines}\nWhich of these statements are correct?',
                    'options': o, 'answer': c, 'key': f'({letter(o, c)}) {why}'}
        out.append(F('C3', 'D3', 'mcq', three, gap='G3'))

    if len(s.Sp) >= 3 and s.Sm:
        def not_correct(r):
            f, corr = r.choice(s.Sm)
            ts = r.sample(s.Sp, 3)
            o = opts4(r, end(f), [end(t) for t in ts])
            return {'stem': f'Which one of the following statements about {s.topic} is NOT correct?', 'options': o,
                    'answer': end(f), 'key': f'({letter(o, end(f))}) It is incorrect. {end(corr)}'}
        out.append(F('C2', 'D2', 'mcq', not_correct, gap='G3'))

    if len(s.Sm) >= 3:
        def correct_one(r):
            t = r.choice(s.Sp)
            fs = r.sample(s.Sm, 3)
            o = opts4(r, end(t), [end(f) for f, _ in fs])
            return {'stem': f'Which one of the following statements about {s.topic} is correct?', 'options': o,
                    'answer': end(t), 'key': f'({letter(o, end(t))}) The others are wrong: ' + ' '.join(end(c) for _, c in fs)}
        out.append(F('C2', 'D3', 'mcq', correct_one, gap='G3'))

    if s.Sm:
        d = deck(s.Sm)

        def fix(r):
            f, corr = d(r)
            return {'stem': f'The following statement about {s.topic} is incorrect. Rewrite it correctly and justify your correction: "{end(f)}"',
                    'answer': end(corr), 'key': f'1 mark for the corrected statement ({end(corr)}); 1 mark for a supporting fact from the NCERT chapter.',
                    'marks': 2, 'minutes': 3}
        out.append(F('C3', 'D2', 'explain', fix, gap='G3', marks=2, minutes=3))
    return out


_PRON = ('he ', 'she ', 'it ', 'its ', 'they ', 'them ', 'their ', 'this ', 'these ', 'those ', 'his ', 'her ')


def _standalone(x: str) -> bool:
    """A statement that reads on its own (no leading pronoun), so it can stand as an unrelated Reason."""
    low = x.strip().lower() + ' '
    return not low.startswith(_PRON) and ' them ' not in low[:40]


def _causal_families(ch: Chapter, s: Sub):
    out = []
    if not s.C:
        return out
    others_sp = [x for sid, x in ch.allSp if sid != s.sid] or [x for _, x in ch.allSp]
    others_sp = [x for x in others_sp if _standalone(x)] or others_sp
    falses = s.Sm or [f for x in ch.subs for f in x.Sm]

    def ar_item(r):
        code = r.choices('abcd', weights=[4, 2, 2, 2])[0]
        if code == 'a':
            A, R = r.choice(s.C)
            why = f'Both are true and R explains A: {end(R)}'
        elif code == 'b':
            A, _ = r.choice(s.C)
            R = r.choice(others_sp)
            why = 'Both statements are true, but R deals with a different point and does not explain A.'
        elif code == 'c':
            A, _ = r.choice(s.C)
            f, corr = r.choice(falses)
            R = f
            why = f'A is true. R is false: {end(corr)}'
        else:
            f, corr = r.choice(falses)
            A = f
            pool = [x for x in [c[1] for c in s.C] + s.Sp if _standalone(x)]
            R = r.choice(pool or [c[1] for c in s.C] + s.Sp)
            why = f'A is false: {end(corr)} R is true.'
        return qbank.ar(end(cap(A)), end(cap(R)), code, why)
    out.append(F('C3', 'D3', 'mcq', ar_item, kinds=('ar',), gap='G3'))

    allR = [c[1] for c in ch.allC]
    if len(allR) >= 4:
        d = deck(s.C)

        def best(r):
            A, R = d(r)
            own_r = [c[1] for c in s.C if c[1] != R]
            rest = [x for x in allR if x != R and x not in own_r]
            wrong = (r.sample(own_r, min(2, len(own_r))) + r.sample(rest, 3))[:3]
            o = opts4(r, end(cap(R)), [end(cap(w)) for w in wrong])
            return {'stem': f'Statement: {end(A)}\nWhich one of the following best explains this statement?', 'options': o,
                    'answer': end(cap(R)), 'key': f'({letter(o, end(cap(R)))}) {end(cap(R))}'}
        out.append(F('C3', 'D2', 'mcq', best))

    shared = deck(s.C)

    def reason(r):
        A, R = shared(r)
        return {'stem': f'Give a reason for the following: {end(A)}', 'answer': end(cap(R)),
                'key': f'2 marks: {end(cap(R))} (1 mark for the reason, 1 for linking it to the statement).',
                'marks': 2, 'minutes': 3}
    out.append(F('C2', 'D3', 'explain', reason, marks=2, minutes=3))

    def examine(r):
        A, R = shared(r)
        return {'stem': f'"{end(A)}" Examine this statement with reference to {s.topic}.',
                'answer': f'The statement is valid. {end(cap(R))}',
                'key': f'3 marks: 1 for accepting or qualifying the statement, 1 for the reason ({end(R)}), 1 for supporting evidence from the chapter.',
                'marks': 3, 'minutes': 5}
    out.append(F('C4', 'D3', 'explain', examine, marks=3, minutes=5))
    return out


def _case_families(ch: Chapter, s: Sub):
    out = []
    if len(s.Sp) < 3:
        return out
    cm = ch.cfg.get('case_marks', (1, 1, 2))
    qs = s.Q or ch.allQ
    ts = s.T or ch.allT
    cs = s.C or ch.allC

    def subqs(r, n_extra=0):
        parts, ans = [], []
        q, a, *_ = r.choice(qs)
        parts.append(q)
        ans.append(a)
        t, m = r.choice(ts)
        parts.append(f"Explain the term '{t}' as it relates to this theme.")
        ans.append(end(cap(m)))
        A, R = r.choice(cs)
        parts.append(f'Explain the reason behind the following: {end(A)}')
        ans.append(end(cap(R)))
        return parts, ans

    def case(r):
        sts = r.sample(s.Sp, 3)
        parts, ans = subqs(r)
        body = '\n'.join(f'({lab}) {p} ({m})' for lab, p, m in zip(['i', 'ii', 'iii'], parts, cm))
        ak = ' '.join(f'({["i", "ii", "iii"][i]}) {a}' for i, a in enumerate(ans))
        return {'stem': f'Read the following extract on {s.topic} and answer the questions that follow.\n"{" ".join(end(x) for x in sts)}"\n{body}',
                'answer': ak, 'key': f'{"+".join(str(m) for m in cm)} marks: ' + ak, 'marks': sum(cm), 'minutes': 6}
    out.append(F('C4', 'D4', 'case', case, kinds=('case',), gap='G7', marks=sum(cm), minutes=6))

    def case_eval(r):
        sts = r.sample(s.Sp, min(4, len(s.Sp)))
        A, R = r.choice(cs)
        t, m = r.choice(ts)
        fx = [f for f in (s.Sm or [])]
        p1 = f"Explain the term '{t}', which is related to the theme of the extract."
        p2 = f'Using the extract and your own knowledge, explain the following: {end(A)}'
        p3 = 'Assess whether the extract gives a complete picture of the theme. Give one argument.'
        if fx:
            f, corr = r.choice(fx)
            p3 = f'A student concludes: "{end(f)}" Use your knowledge of the chapter to evaluate this conclusion.'
            a3 = f'The conclusion is wrong: {end(corr)}'
        else:
            a3 = 'Credit any reasoned argument about the limits of the source (one-sided, partial, needs other evidence).'
        ans = f'(i) {end(cap(m))} (ii) {end(cap(R))} (iii) {a3}'
        body = f'(i) {p1} ({cm[0]})\n(ii) {p2} ({cm[1]})\n(iii) {p3} ({cm[2]})'
        return {'stem': f'Study the extract below and answer the questions.\n"{" ".join(end(x) for x in sts)}"\n{body}',
                'answer': ans, 'key': f'{"+".join(str(x) for x in cm)} marks: ' + ans, 'marks': sum(cm), 'minutes': 7}
    out.append(F('C4', 'D5', 'case', case_eval, kinds=('case',), gap='G7', marks=sum(cm), minutes=7))
    return out


def _hand_families(ch: Chapter, s: Sub):
    out = []
    long_marks = ch.cfg.get('long_marks', 8)
    by_tag = {}
    for C, D, marks, stem, ans in s.X:
        by_tag.setdefault((C, D, marks), []).append((stem, ans))
    for (C, D, marks), lst in by_tag.items():
        mk = marks or 3
        d = deck(lst, recycle=True)

        def gen(r, d=d, mk=mk):
            stem, ans = d(r)
            return {'stem': stem, 'answer': ans, 'key': f'{int(mk) if mk == int(mk) else mk} marks: ' + ans,
                    'marks': mk if mk != int(mk) else int(mk), 'minutes': max(2, round(mk * 1.6))}
        typ = 'short' if mk <= 1 else 'explain'
        out.append(F(C, D, typ, gen, marks=int(mk) if mk == int(mk) else mk, minutes=max(2, round(mk * 1.6))))
    by_d = {}
    for D, stem, ans in s.L:
        by_d.setdefault(D, []).append((stem, ans))
    for D, lst in by_d.items():
        d = deck(lst, recycle=True)

        def gen(r, d=d):
            stem, ans = d(r)
            return {'stem': stem, 'answer': ans,
                    'key': f'{long_marks} marks: credit each relevant point explained with NCERT evidence – ' + ans,
                    'marks': long_marks, 'minutes': round(long_marks * 1.5)}
        out.append(F('C4', D, 'long', gen, marks=long_marks, minutes=round(long_marks * 1.5), gap='G5'))
    return out


def families(chapters: list[list[Sub]], cfgs: list[dict], extra: dict | None = None) -> dict:
    fams = {}
    for subs, cfg in zip(chapters, cfgs):
        ch = Chapter(subs, cfg)
        first_p = next((s.sid for s in subs if s.P), None)
        for s in subs:
            fl = []
            fl += _term_families(ch, s)
            fl += _q_families(ch, s)
            fl += _year_families(ch, s)
            fl += _place_families(ch, s, s.sid == first_p)
            fl += _match_families(ch, s)
            fl += _statement_families(ch, s)
            fl += _causal_families(ch, s)
            fl += _case_families(ch, s)
            fl += _hand_families(ch, s)
            if extra and s.sid in extra:
                fl += extra[s.sid]
            fams[s.sid] = fl
    return fams


# ---------------------------------------------------------------- stricter mock fitting

def strict_fits(f, kind: str) -> bool:
    if kind == 'map':
        return 'map' in f.kinds
    if 'map' in f.kinds:
        return False
    if kind == 'ar':
        return 'ar' in f.kinds
    if kind == 'mcq':
        return f.type == 'mcq' and 'ar' not in f.kinds
    if kind == 'case':
        return 'case' in f.kinds
    if kind == 'long':
        return f.type == 'long'
    if kind == 'short':          # 2-mark answers
        return f.type in ('explain', 'numerical') and f.C in ('C2', 'C3') and (f.marks or 2) <= 2
    if kind == 'short3':         # 3- or 4-mark answers
        return f.type in ('explain', 'numerical', 'multi_step') and DNUM[f.D] >= 2 and (f.marks or 3) >= 3
    return f.type == kind


def install():
    qbank._fits = strict_fits


# ---------------------------------------------------------------- runner

def run(sid: str, generated_by: str, chapters: list, mock_pattern: list, extra: dict | None = None,
        mpm: float = 2.25, accuracy: list | None = None):
    """Build and write a subject. QB_LIMIT=n builds only the first n chapters (for testing, into QB_QUESTIONS_DIR)."""
    import os
    install()
    subs = [c for c, _ in chapters]
    cfgs = [cfg for _, cfg in chapters]
    fams = families(subs, cfgs, extra)
    b = qbank.Builder(sid, generated_by, fams, mock_pattern, mock_minutes_per_mark=mpm)
    limit = int(os.environ.get('QB_LIMIT', '0'))
    if limit:
        b.cur['chapters'] = b.cur['chapters'][:limit]
        b.t = dict(b.t, chapters=limit, mocks=int(os.environ.get('QB_MOCKS', b.t['mocks'])))
    else:
        have = {s.sid for c in subs for s in c}
        need = {s['id'] for ch in b.cur['chapters'] for s in ch['subtopics']}
        if have != need:
            raise SystemExit(f'subtopics missing: {sorted(need - have)[:5]} extra: {sorted(have - need)[:5]}')
    files = b.build()
    b.write(files, accuracy=accuracy)
    print(f'{sid}: wrote {sum(len(v) for v in files.values())} questions')
    return b, files
