"""Shared helpers for Cambridge content modules."""
import math
import random

from core import Topic, topic, mcq, fmt  # noqa: F401

PEOPLE = ['Amara', 'Lucas', 'Sofia', 'Kenji', 'Zara', 'Mateo', 'Aisha', 'Noah', 'Leila', 'Ethan', 'Priya', 'Omar',
          'Chloe', 'Daniel', 'Mei', 'Tariq', 'Hana', 'Jonas', 'Ines', 'Kwame', 'Yusuf', 'Elena', 'Ravi', 'Freya',
          'Diego', 'Nadia', 'Samuel', 'Ana', 'Felix', 'Sipho', 'Lina', 'Arjun', 'Grace', 'Mohammed', 'Isla', 'Tomás']
CITIES = ['Nairobi', 'Lima', 'Singapore', 'Dubai', 'Cape Town', 'Lisbon', 'Kuala Lumpur', 'Bogotá', 'Cairo', 'Hanoi',
          'Lagos', 'Doha', 'Jakarta', 'Manila', 'Karachi', 'Muscat', 'Santiago', 'Accra', 'Colombo', 'Auckland',
          'Toronto', 'Madrid', 'Istanbul', 'Bangkok', 'Mumbai', 'Kathmandu', 'Dhaka', 'Riyadh', 'Mexico City', 'Seoul']
CURRENCIES = [('$', 'dollars'), ('€', 'euros'), ('£', 'pounds')]


def person(r):
    return r.choice(PEOPLE)


def two_people(r):
    a, b = r.sample(PEOPLE, 2)
    return a, b


def city(r):
    return r.choice(CITIES)


def sf(x, n=3):
    """Round to n significant figures and format."""
    if x == 0:
        return '0'
    d = n - int(math.floor(math.log10(abs(x)))) - 1
    v = round(x, d)
    if d <= 0:
        v = int(v)
        return f'{v:,}' if abs(v) >= 10000 else str(v)
    s = f'{v:.{d}f}'
    return s


def sci(x, n=3):
    """Scientific notation with Unicode superscripts, e.g. 3.00 × 10⁸."""
    if x == 0:
        return '0'
    e = int(math.floor(math.log10(abs(x))))
    m = x / 10 ** e
    m = round(m, n - 1)
    if abs(m) >= 10:
        m /= 10; e += 1
    return f'{m:.{n - 1}f} × 10{sup(e)}'


SUP = str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹')


def sup(n):
    return str(n).translate(SUP)


def near(r, correct, k=3, rel=(0.5, 2, 1.5, 0.8, 1.25, 10, 0.1), fmtf=None):
    """Plausible numeric distractors around a correct value."""
    f = fmtf or (lambda x: sf(x))
    c = f(correct)
    out = []
    for m in r.sample(rel, len(rel)):
        v = f(correct * m)
        if v != c and v not in out:
            out.append(v)
    return out


def num_mcq(r, correct, distractor_values, fmtf=None, unit=''):
    f = fmtf or (lambda x: sf(x))
    c = f(correct) + unit
    ds = []
    for v in distractor_values:
        s = f(v) + unit
        if s != c and s not in ds:
            ds.append(s)
    return mcq(r, c, ds)


def pick(r, seq, k=1):
    return r.sample(list(seq), k) if k > 1 else r.choice(list(seq))


LETTERS = 'abcdefgh'
CTX = {'want_marks': None}
_MK = __import__('re').compile(r'\[(\d+)\]')


def _part_marks(key):
    m = _MK.findall(key)
    return int(m[-1]) if m else 1


def compose(r, intro, parts, k=(2, 3), keep_order=True, type_=None):
    """Build a multi-part structured question.

    parts: callables f(r) -> (text, answer, key) or None. Part marks are read from a trailing
    "[n]" in each part's key. When CTX['want_marks'] is set, the subset of parts is chosen so
    that the marks add up to it where possible.
    """
    built = []
    for i, p in enumerate(parts):
        x = p(r)
        if x:
            built.append((i, x, _part_marks(x[2])))
    if not built:
        return None
    want = CTX.get('want_marks')
    sizes = [n for n in k if n <= len(built)] or [len(built)]
    if want:
        sizes = sorted(set(sizes) | {1, 2, 3, 4} if want <= 3 else set(sizes) | {2, 3, 4, 5})
    best = None
    for _ in range(60):
        n = min(r.choice(sizes), len(built))
        pick = r.sample(built, n)
        tot = sum(m for _, _, m in pick)
        score = abs(tot - want) if want else 0
        if want and n == 1 and want > 2:
            score += 2
        if best is None or score < best[0]:
            best = (score, pick, tot)
        if score == 0:
            break
    _, pick, tot = best
    if keep_order:
        pick.sort(key=lambda x: x[0])
    got = [x for _, x, _ in pick]
    if len(got) == 1:
        t, a, kk = got[0]
        q = {'stem': intro.strip() + ' ' + t, 'answer': a, 'key': kk}
    else:
        stem = intro.strip() + ' ' + ' '.join(f'({LETTERS[j]}) {t}' for j, (t, _, _) in enumerate(got))
        ans = ' '.join(f'({LETTERS[j]}) {a}' for j, (_, a, _) in enumerate(got))
        key = ' '.join(f'({LETTERS[j]}) {kk}' for j, (_, _, kk) in enumerate(got))
        q = {'stem': stem, 'answer': ans, 'key': key}
    q['marks'] = max(1, min(20, tot))
    q['minutes'] = round(max(1.0, q['marks'] * 1.25) * 2) / 2
    if type_:
        q['type'] = type_
    return q


FACTORS = [(2, 'doubled'), (3, 'tripled'), (4, 'multiplied by 4'), (0.5, 'halved'), (1 / 3, 'reduced to one third'), (0.25, 'reduced to a quarter'), (1.5, 'increased by 50%'), (5, 'multiplied by 5')]


def _fac(x):
    for v, w in [(1, 'stays the same'), (2, 'doubles'), (3, 'triples'), (4, 'becomes 4 times bigger'), (0.5, 'halves'), (0.25, 'becomes a quarter'), (8, 'becomes 8 times bigger'), (9, 'becomes 9 times bigger'),
                 (16, 'becomes 16 times bigger'), (1 / 3, 'becomes one third'), (1 / 9, 'becomes one ninth'), (0.125, 'becomes one eighth'), (1 / 16, 'becomes one sixteenth'), (2.25, 'becomes 2.25 times bigger'),
                 (1.5, 'increases by 50%'), (2 / 3, 'falls to two thirds'), (4 / 9, 'falls to four ninths'), (5, 'becomes 5 times bigger'), (0.2, 'falls to one fifth'), (25, 'becomes 25 times bigger'), (0.04, 'falls to 1/25'), (6, 'becomes 6 times bigger'), (12, 'becomes 12 times bigger'), (0.75, 'falls to three quarters')]:
        if abs(x - v) < 1e-9:
            return w
    return f'is multiplied by {sf(x)}'


def relation(t, C, D, eq, target, variables, contexts, unit_note=''):
    """Proportional-reasoning item. variables: {name: exponent} for target ∝ Π var^exp (others held constant)."""
    def fn(r, D_):
        v = r.choice(list(variables))
        k, word = r.choice(FACTORS)
        f = k ** variables[v]
        ctx = r.choice(contexts)
        others = [x for x in variables if x != v]
        keep = (' while the ' + ' and '.join(others) + (' stays' if len(others) == 1 else ' stay') + ' the same') if others else ''
        lead = r.choice(['State and explain', 'Explain', 'Predict, with a reason,'])
        stem = f'{ctx} The {v} is {word}{keep}. {lead} how the {target} changes.'
        return {'stem': stem, 'answer': f'The {target} {_fac(f)}.', 'key': f'Using {eq}: {target} ∝ {v}' + ('' if variables[v] == 1 else ('^' + sf(variables[v]))) + f'; factor = {sf(k)}' + ('' if variables[v] == 1 else f'^{sf(variables[v])}') + f' = {sf(f)}. 1 mark relationship, 1 mark conclusion.' + unit_note,
                'type': 'explain'}
    fn.__name__ = 'relation'
    t.add(C, D, 'explain')(fn)
    return fn
