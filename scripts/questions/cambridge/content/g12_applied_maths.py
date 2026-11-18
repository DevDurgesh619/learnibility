"""Cambridge International A Level Mathematics 9709 Paper 6 Probability & Statistics 2 (grade 12,
statistics route).

Chapters follow the P6 coursebook: the Poisson distribution, linear combinations of random
variables, continuous random variables, sampling, estimation and hypothesis tests.

Conventions: probabilities and other non-exact answers to 3 significant figures; z-values to
3 decimal places as read from tables; critical values 1.645, 1.96, 2.326, 2.576. Mark schemes use
M (method), A (accuracy) and B (independent) marks; item marks are read from the mark points in the
key and written as a trailing [n]. Every computed answer is produced in code and, where a second
independent route exists, checked inside the template (exact Fractions against numerical
quadrature, recurrences against direct sums); a template whose check fails returns None.
"""
import math
import re
from fractions import Fraction as Fr

from ._lib import topic, mcq, compose, sf, person, two_people, city, sup, CTX, LETTERS, _part_marks
from .g11_maths import (num, n3, n4, p4, dn, pn, Phi, invPhi, z3, comb, MC, P, PF, T, key_marks, MINUS,
                        prob3, nf, _wrap)

PROFILE = {'mark_scale': {'long': (1.5, 1.5), 'case': (1.25, 1.25)}, 'wordy': False}
CHAPTERS = {}
CHECK_FAILS = []


# ================================================================ helpers

def Q(stem, answer, key, **kw):
    """Single item; marks from the M/A/B tokens, written as a trailing [n]."""
    m = key_marks(key)
    if m and not re.search(r'\[\d+\]\s*$', key):
        key = f'{key} [{m}]'
    d = {'stem': stem, 'answer': answer, 'key': key}
    if m and 'marks' not in kw:
        d['marks'] = max(1, min(20, m))
        d['minutes'] = round(max(1.0, d['marks'] * 1.25) * 2) / 2
    d.update(kw)
    return d


def cmp_(r, intro, parts, k=(2, 3, 4), type_='multi_step', deps=None):
    """compose() with dependencies: deps maps a part index to the indices it relies on, which are
    always included with it, so a chosen subset never refers to a missing earlier part."""
    deps = deps or {}
    built = {}
    for i, p in enumerate(parts):
        x = p(r)
        if x:
            built[i] = (x, _part_marks(x[2]))
    for i in list(built):
        if any(j not in built for j in deps.get(i, ())):
            del built[i]
    if not built:
        return None

    def close(sel):
        out, todo = set(), list(sel)
        while todo:
            i = todo.pop()
            if i not in out:
                out.add(i)
                todo.extend(deps.get(i, ()))
        return sorted(out)

    idx = sorted(built)
    want = CTX.get('want_marks')
    sizes = [n for n in k if n <= len(idx)] or [len(idx)]
    if want:
        sizes = sorted(set(sizes) | ({1, 2, 3, 4} if want <= 3 else {2, 3, 4, 5}))
    best = None
    for _ in range(60):
        n = min(r.choice(sizes), len(idx))
        pick = close(r.sample(idx, n))
        tot = sum(built[i][1] for i in pick)
        score = abs(tot - want) if want else 0
        if want and len(pick) == 1 and want > 2:
            score += 2
        if best is None or score < best[0]:
            best = (score, pick, tot)
        if score == 0:
            break
    _, pick, tot = best
    got = [built[i][0] for i in pick]
    if len(got) == 1:
        t, a, kk = got[0]
        q = {'stem': intro.strip() + ' ' + t, 'answer': a, 'key': kk}
    else:
        q = {'stem': intro.strip() + ' ' + ' '.join(f'({LETTERS[j]}) {t}' for j, (t, _, _) in enumerate(got)),
             'answer': ' '.join(f'({LETTERS[j]}) {a}' for j, (_, a, _) in enumerate(got)),
             'key': ' '.join(f'({LETTERS[j]}) {kk}' for j, (_, _, kk) in enumerate(got))}
    q['marks'] = max(1, min(20, tot))
    q['minutes'] = round(max(1.0, q['marks'] * 1.25) * 2) / 2
    if type_:
        q['type'] = type_
    return q


def SUBN(n):
    return str(n).translate(str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉'))


def MCk(r, stem, correct, distractors, key):
    q = MC(r, stem, correct, distractors, key if key.rstrip().endswith(']') else key + ' [1]')
    if q:
        q['marks'] = key_marks(q['key']) or 1
        q['minutes'] = 1.5
    return q


def ok(a, b, tag='', tol=1e-6):
    try:
        good = abs(a - b) <= tol * max(1.0, abs(a), abs(b))
    except TypeError:
        good = False
    if not good:
        CHECK_FAILS.append((tag, a, b))
    return good


def ppmf(l, k):
    if k < 0:
        return 0.0
    return math.exp(-l) * l ** k / math.factorial(k)


def pcdf(l, k):
    """P(X <= k) for Po(l), by direct summation."""
    return sum(ppmf(l, i) for i in range(0, k + 1)) if k >= 0 else 0.0


def pcdf_rec(l, k):
    """Independent check: recurrence p(i+1) = p(i) * l / (i + 1)."""
    if k < 0:
        return 0.0
    p = math.exp(-l)
    s = p
    for i in range(k):
        p = p * l / (i + 1)
        s += p
    return s


def bpmf(n, p, k):
    if k < 0 or k > n:
        return 0.0
    return comb(n, k) * p ** k * (1 - p) ** (n - k)


def bcdf(n, p, k):
    return sum(bpmf(n, p, i) for i in range(0, min(k, n) + 1)) if k >= 0 else 0.0


def L(x):
    """Format a Poisson / distribution parameter."""
    return num(round(x, 6)) if abs(x - round(x, 6)) < 1e-9 else n3(x)


def ex(l, k):
    """e^(−λ) λ^k / k! written out."""
    if k == 0:
        return f'e^({MINUS}{L(l)})'
    if k == 1:
        return f'e^({MINUS}{L(l)}) × {L(l)}'
    return f'e^({MINUS}{L(l)}) × {L(l)}{sup(k)}/{k}!'


def terms(l, ks):
    return ' + '.join(ex(l, k) for k in ks)


def p3(x):
    return prob3(x)


def zc(alpha, tails):
    """Critical z for significance level alpha (one or two tails), table values."""
    tab = {(0.10, 1): 1.282, (0.05, 1): 1.645, (0.025, 1): 1.96, (0.01, 1): 2.326, (0.005, 1): 2.576,
           (0.10, 2): 1.645, (0.05, 2): 1.96, (0.02, 2): 2.326, (0.01, 2): 2.576}
    return tab[(alpha, tails)]


CONF = {90: 1.645, 95: 1.96, 98: 2.326, 99: 2.576, 92: 1.751, 94: 1.881, 96: 2.054, 97: 2.17}


def pct(a):
    return f'{num(a)}%'


def iv(a, b):
    return f'({n3(a)}, {n3(b)})'


def fin():
    for ts in CHAPTERS.values():
        for t in ts:
            for tp in t.templates:
                if not getattr(tp.fn, '_wrapped', False):
                    tp.fn = _wrap(tp.fn)
                    tp.fn._wrapped = True


# ================================================================ Chapter 1: The Poisson distribution

# (events, base interval, [(other interval, multiplier)], plausible λ values per base interval)
PCTX = [
    ('calls received by a helpline', 'a 10-minute period', [('a 30-minute period', 3), ('a 5-minute period', 0.5), ('a one-hour period', 6)], [1.2, 1.5, 1.8, 2.4, 2.5, 3.2]),
    ('emails received by a manager', 'an hour', [('an 8-hour working day', 8), ('a half-hour period', 0.5), ('a 15-minute period', 0.25)], [2, 2.4, 3.6, 4, 4.8]),
    ('flaws in a roll of fabric', 'a 1-metre length', [('a 5-metre length', 5), ('a 20 cm length', 0.2), ('a 2.5-metre length', 2.5)], [0.6, 0.8, 1.2, 1.5, 2]),
    ('cars passing a point on a quiet road', 'a one-minute period', [('a 5-minute period', 5), ('a 30-second period', 0.5), ('a 3-minute period', 3)], [1.4, 1.8, 2.2, 3, 3.5]),
    ('typing errors made by a typist', 'a page', [('a 10-page report', 10), ('half a page', 0.5), ('a 4-page letter', 4)], [0.4, 0.6, 0.8, 1.1, 1.5]),
    ('bacteria in a sample of pond water', '1 ml', [('a 5 ml sample', 5), ('a 0.5 ml sample', 0.5), ('a 2 ml sample', 2)], [1.6, 2.4, 3.2, 4.4, 5.2]),
    ('customers arriving at a bank counter', 'a 5-minute period', [('a 20-minute period', 4), ('an hour', 12), ('a one-minute period', 0.2)], [1.5, 2, 2.5, 3, 4]),
    ('accidents at a road junction', 'a month', [('a year', 12), ('a 3-month period', 3), ('a 6-month period', 6)], [0.5, 0.8, 1.25, 1.5]),
    ('meteors seen by an observer', 'a 10-minute period', [('an hour', 6), ('a 5-minute period', 0.5), ('a 30-minute period', 3)], [1.5, 2.5, 3, 3.5]),
    ('weeds in a lawn', 'a square metre', [('a 4 m² area', 4), ('a 0.25 m² quadrat', 0.25), ('a 10 m² area', 10)], [2.5, 3, 4, 5.5, 6]),
    ('goals scored by a hockey team', 'a match', [('a set of 3 matches', 3), ('the first half of a match', 0.5), ('a set of 5 matches', 5)], [1.4, 1.8, 2.2, 2.6]),
    ('earthquakes of magnitude 5 or more in a region', 'a year', [('a 5-year period', 5), ('a 6-month period', 0.5), ('a 10-year period', 10)], [0.7, 1.2, 1.5, 2.1]),
]


def rpo(r, D=2):
    c = r.choice(PCTX)
    lam = r.choice(c[3])
    return c, lam


def unit_pl(u):
    """'a 10-minute period' -> '10-minute periods'."""
    if u == '1 ml':
        return '1 ml samples'
    w = u.split(' ', 1)[1] if u.split(' ', 1)[0] in ('a', 'an') else u
    return w + ('es' if w.endswith('ch') else 's')


def po_intro(c, lam):
    return f'The number of {c[0]} in {c[1]} has the distribution Po({L(lam)}).'


po1 = T('The Poisson distribution Po(λ): conditions and calculating probabilities', 'poisson distribution', 'po(λ)', 'conditions and calculating probabilities')
po1.fixed('C1', (1, 2), [
    ('If X ~ Po(λ), then P(X = r) =', 'e^(−λ) λʳ/r!', 'Poisson probability formula. [1]', ['λʳ/r!', 'e^(−λ) rλ/r!', 'e^(−r) λʳ/r!']),
    ('Which condition is needed for a Poisson model?', 'Events occur independently and at random', 'Also singly and at a constant average rate. [1]', ['There is a fixed number of trials', 'Each trial has two outcomes', 'Events occur at regular intervals']),
    ('For X ~ Po(λ), P(X = 0) =', 'e^(−λ)', 'λ⁰/0! = 1. [1]', ['0', '1 − e^(−λ)', 'λe^(−λ)']),
    ('For X ~ Po(λ), P(X ≥ 1) =', '1 − e^(−λ)', 'Complement of P(X = 0). [1]', ['e^(−λ)', 'λe^(−λ)', '1 − λe^(−λ)']),
    ('Which of these is most suitably modelled by a Poisson distribution?', 'The number of radioactive decays detected in one second', 'Random, independent events at a constant average rate. [1]', ['The number of heads in 10 throws of a coin', 'The height of a randomly chosen student', 'The number of throws needed to obtain a six']),
    ('The number of misprints in a book follows Po(0.4) per page. The distribution of the number of misprints in 5 pages is', 'Po(2)', 'λ scales with the length of the interval: 5 × 0.4. [1]', ['Po(0.4)', 'Po(0.08)', 'B(5, 0.4)']),
])
po1.fixed('C2', (2, 3), [
    ('State two conditions required for the number of cars passing a point on a road in one minute to be modelled by a Poisson distribution.', 'Cars pass independently of each other and at random, at a constant average rate (and one at a time).', 'B1 independently / at random; B1 constant average rate [2]'),
    ('Explain why the number of passengers getting off a bus at a stop might not be well modelled by a Poisson distribution.', 'Passengers often travel in groups, so they do not get off independently or singly.', 'B1 not independent / not singly; B1 reason in context [2]'),
    ('Explain why the number of customers entering a shop in an hour may not follow a Poisson distribution with the same mean throughout the day.', 'The average rate is not constant: it is higher at busy times such as lunchtime than early morning.', 'B1 rate not constant; B1 context [2]'),
])


@po1.add('C1', (1, 2, 3))
def po1_c1(r, D):
    c, lam = rpo(r)
    kind = r.choice(['pmf', 'zero', 'scale', 'ge1'])
    if kind == 'pmf':
        k = r.randint(1, 4)
        v = ppmf(lam, k)
        return MCk(r, po_intro(c, lam) + f' Find the probability that exactly {k} occur in {c[1]}.', n3(v),
                   [n3(lam ** k / math.factorial(k)) if lam ** k / math.factorial(k) < 1 else n3(v * 2), n3(pcdf(lam, k)), n3(math.exp(-lam) * lam ** k), n3(ppmf(lam, k - 1))],
                   f'{ex(lam, k)} = {n3(v)}.')
    if kind == 'zero':
        v = math.exp(-lam)
        return MCk(r, po_intro(c, lam) + f' Find the probability that none occur in {c[1]}.', n3(v), [n3(1 - v), n3(lam * v), '0', n3(math.exp(-1 / lam))], f'e^({MINUS}{L(lam)}) = {n3(v)}.')
    if kind == 'ge1':
        v = 1 - math.exp(-lam)
        return MCk(r, po_intro(c, lam) + f' Find the probability that at least one occurs in {c[1]}.', n3(v), [n3(1 - v), n3(1 - lam * math.exp(-lam)), n3(lam * math.exp(-lam)), n3(1 - math.exp(-lam) - lam * math.exp(-lam))],
                   f'1 − e^({MINUS}{L(lam)}) = {n3(v)}.')
    alt, m = r.choice(c[2])
    return MCk(r, po_intro(c, lam) + f' State the distribution of the number of {c[0]} in {alt}.', f'Po({L(lam * m)})', [f'Po({L(lam)})', f'Po({L(lam / m)})', f'B({max(2, int(m * 10))}, {L(min(0.9, lam / 10))})', f'Po({L(lam + m)})'],
               f'Mean scales with the interval: {L(lam)} × {num(m)} = {L(lam * m)}.')


@po1.add('C2', (2, 3, 4), 'explain')
def po1_err(r, D):
    c, lam = rpo(r)
    nm = person(r)
    kind = r.choice(['lt', 'scale', 'ge'])
    k = r.randint(2, 4)
    if kind == 'lt':
        wrong = pcdf(lam, k)
        right = pcdf(lam, k - 1)
        return Q(po_intro(c, lam) + f' {nm} calculates P(fewer than {k} occur in {c[1]}) as P(X = 0) + P(X = 1) + … + P(X = {k}) = {n3(wrong)}. Explain the error and find the correct probability.',
                 f'“Fewer than {k}” means X ≤ {k - 1}, so P(X = {k}) must not be included: P(X ≤ {k - 1}) = {n3(right)}.', f'B1 should be X ≤ {k - 1}; M1 {terms(lam, range(k))}; A1 {n3(right)}')
    if kind == 'scale':
        alt, m = r.choice([x for x in c[2] if x[1] > 1] or c[2])
        wrong = 1 - math.exp(-lam)
        right = 1 - math.exp(-lam * m)
        return Q(po_intro(c, lam) + f' {nm} says the probability that at least one occurs in {alt} is 1 − e^({MINUS}{L(lam)}) = {n3(wrong)}. Explain the error and find the correct probability.',
                 f'The mean must be scaled to the new interval: λ = {L(lam * m)}, so the probability is 1 − e^({MINUS}{L(lam * m)}) = {n3(right)}.', f'B1 λ = {L(lam * m)}; M1 1 − e^({MINUS}{L(lam * m)}); A1 {n3(right)}')
    wrong = 1 - pcdf(lam, k)
    right = 1 - pcdf(lam, k - 1)
    return Q(po_intro(c, lam) + f' {nm} calculates P(at least {k} occur in {c[1]}) as 1 − P(X ≤ {k}) = {n3(wrong)}. Explain the error and find the correct probability.',
             f'P(X ≥ {k}) = 1 − P(X ≤ {k - 1}); {nm} has wrongly excluded X = {k}. Correct value {n3(right)}.', f'B1 1 − P(X ≤ {k - 1}); M1 1 − ({terms(lam, range(k))}); A1 {n3(right)}')


SCEN_NOT = [
    ('the number of people in a queue at a supermarket checkout each minute', 'people arrive in groups (families) and the rate varies through the day, so arrivals are not independent and the rate is not constant'),
    ('the number of goals scored in the second half of a football match by a team that scored in the first half', 'goals may not be independent: scoring may change how the teams play'),
    ('the number of students absent from a class on a day during a flu outbreak', 'absences are not independent because flu spreads from person to person'),
    ('the number of trains arriving at a station in 10 minutes', 'trains run to a timetable, so arrivals are not random'),
    ('the number of rainy days in a week', 'there is a maximum of 7, and wet days tend to follow wet days, so they are not independent'),
    ('the number of customers at a restaurant between 12:00 and 15:00', 'the rate is not constant: lunchtime is much busier'),
]


@po1.add('C2', (2, 3, 4), 'explain')
def po1_model(r, D):
    s, why = r.choice(SCEN_NOT)
    nm = person(r)
    if D <= 2:
        return Q(f'{nm} wants to model {s} in {city(r)} by a Poisson distribution. Give a reason why this model may not be suitable.', cap(why) + '.', 'B1 reason linked to a Poisson condition, in context')
    return Q(f'{nm} wants to model {s} in {city(r)} by a Poisson distribution. State the conditions required for a Poisson model and explain whether they are likely to hold.',
             'Events must occur singly, independently, at random and at a constant average rate. Here ' + why + ', so the model is unlikely to be suitable.', 'B1 two conditions stated; B1 explanation in context; B1 conclusion')


def cap(s):
    return s[:1].upper() + s[1:]


@po1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def po1_calc(r, D):
    c, lam = rpo(r)
    stem = po_intro(c, lam)
    if D == 1:
        k = r.randint(1, 4)
        v = ppmf(lam, k)
        return Q(stem + f' Find the probability that exactly {k} occur in {c[1]}.', n3(v), f'M1 {ex(lam, k)}; A1 {n3(v)}')
    if D == 2:
        k = r.randint(1, 3)
        v = pcdf(lam, k)
        if not ok(v, pcdf_rec(lam, k)):
            return None
        return Q(stem + f' Find the probability that at most {k} occur in {c[1]}.', n3(v), f'M1 {terms(lam, range(k + 1))}; A1 {n3(v)}')
    if D == 3:
        k = r.randint(2, 4)
        v = 1 - pcdf(lam, k - 1)
        if r.random() < 0.5:
            return Q(stem + f' Find the probability that at least {k} occur in {c[1]}.', n3(v), f'M1 1 − P(X ≤ {k - 1}); M1 1 − ({terms(lam, range(k))}); A1 {n3(v)}')
        a = r.randint(1, 2)
        b = a + r.randint(2, 3)
        v = pcdf(lam, b - 1) - pcdf(lam, a)
        return Q(stem + f' Find P({a} < X < {b}), where X is the number in {c[1]}.', n3(v), f'M1 P(X = {a + 1}) + … + P(X = {b - 1}); M1 {terms(lam, range(a + 1, b))}; A1 {n3(v)}')
    if D == 4:
        alt, m = r.choice(c[2])
        l2 = lam * m
        k = max(1, min(6, int(l2) - r.randint(0, 1)))
        v = pcdf(l2, k)
        if not ok(v, pcdf_rec(l2, k)):
            return None
        return Q(stem + f' Find the probability that at most {k} occur in {alt}.', p3(v), f'B1 λ = {L(l2)}; M1 {terms(l2, range(k + 1))}; A1 {p3(v)}')
    if r.random() < 0.5:
        tgt = r.choice([0.9, 0.95, 0.99, 0.999])
        t = 1
        while 1 - math.exp(-lam * t) <= tgt:
            t += 1
        x = -math.log(1 - tgt) / lam
        if not ok(t, math.floor(x) + 1, 'po1 t'):
            return None
        return Q(stem + f' Find the smallest number, t, of {unit_pl(c[1])} for which the probability of at least one occurrence in total is greater than {tgt}.', str(t),
                 f'B1 Po({L(lam)}t); M1 1 − e^({MINUS}{L(lam)}t) > {tgt}; M1 t > −ln({num(round(1 - tgt, 6))}) ÷ {L(lam)} = {n3(x)}; A1 t = {t}')
    p0 = round(math.exp(-lam), 4)
    lam2 = -math.log(p0)
    k = r.randint(1, 3)
    v = ppmf(lam2, k)
    return Q(f'The number of {c[0]} in {c[1]} has a Poisson distribution. The probability that none occur in {c[1]} is {p0}. Find the probability that exactly {k} occur in {c[1]}.', n3(v),
             f'M1 e^({MINUS}λ) = {p0}; A1 λ = {n3(lam2)}; M1 {ex(lam2, k).replace(L(lam2), n3(lam2))}; A1 {n3(v)}')


def po1_c4(r, D):
    c, lam = rpo(r)
    alt, m = r.choice(c[2])
    l2 = lam * m
    k = r.randint(1, 3)
    days = r.randint(3, 5)
    p0 = math.exp(-lam)
    pd = 1 - pcdf(lam, 0)
    pk = ppmf(lam, k)
    v2 = 1 - pcdf(l2, 1)
    one = days * p0 * (1 - p0) ** (days - 1)
    intro = po_intro(c, lam)
    parts = [
        P(f'Find the probability that exactly {k} occur in {c[1]}.', n3(pk), f'M1 {ex(lam, k)}; A1 {n3(pk)}'),
        P(f'Find the probability that at least 2 occur in {alt}.', p3(v2), f'B1 λ = {L(l2)}; M1 1 − (e^({MINUS}{L(l2)}) + e^({MINUS}{L(l2)}) × {L(l2)}); A1 {p3(v2)}'),
        P(f'Find the probability that at least one occurs in each of {days} separate {unit_pl(c[1])}.', p3(pd ** days), f'M1 (1 − e^({MINUS}{L(lam)})){sup(days)}; A1 {p3(pd ** days)}'),
        P(f'Find the probability that, in {days} separate {unit_pl(c[1])}, exactly one has no occurrences.', p3(one), f'B1 p = e^({MINUS}{L(lam)}) = {n3(p0)}; M1 {days} × {n3(p0)} × (1 − {n3(p0)}){sup(days - 1)}; A1 {p3(one)}'),
        P('State one assumption needed for the Poisson model to be valid in this context.', 'The events occur independently and at random, at a constant average rate.', 'B1 in context'),
    ]
    return cmp_(r, intro, parts)


po1.add('C4', (2, 3, 4, 5))(po1_c4)


po2 = T('Mean and variance of the Poisson distribution and checking suitability', 'mean and variance of the poisson distribution', 'checking suitability')
po2.fixed('C1', (1, 2), [
    ('If X ~ Po(λ), then Var(X) =', 'λ', 'For a Poisson distribution E(X) = Var(X) = λ. [1]', ['√λ', 'λ²', 'λ(1 − λ)']),
    ('If X ~ Po(9), the standard deviation of X is', '3', '√9 = 3. [1]', ['9', '81', '4.5']),
    ('A set of count data has mean 4.1 and variance 9.6. This suggests that a Poisson model is', 'unlikely to be suitable, because the mean and variance are not approximately equal', 'For Poisson, mean ≈ variance. [1]', ['suitable, because the mean is greater than 1', 'suitable, because the variance is positive', 'unlikely to be suitable, because the mean is less than 5']),
    ('If X ~ Po(λ) and P(X = 2) = P(X = 3), then λ =', '3', 'λ²/2 = λ³/6 gives λ = 3. [1]', ['2', '2.5', '6']),
])
po2.fixed('C2', (2, 3), [
    ('Explain why comparing the mean and variance of a set of count data helps to decide whether a Poisson model is suitable.', 'For a Poisson distribution the mean and variance are equal, so if the sample mean and variance are close the model may be suitable; if they differ greatly it is not.', 'B1 E(X) = Var(X) for Poisson; B1 conclusion rule [2]'),
    ('A variable X takes the values 0, 1, 2, …, 5 only. Explain why X cannot have an exact Poisson distribution.', 'A Poisson variable can take any non-negative integer value with no upper limit, so P(X > 5) > 0 for a Poisson distribution.', 'B1 no upper limit; B1 P(X > 5) > 0 [2]'),
])


@po2.add('C1', (1, 2, 3))
def po2_c1(r, D):
    kind = r.choice(['sd', 'var', 'ratio', 'zero'])
    if kind == 'sd':
        lam = r.choice([1.44, 2.25, 3.24, 4, 6.25, 7.29, 12.25, 16])
        return MCk(r, f'X ~ Po({L(lam)}). Find the standard deviation of X.', L(math.sqrt(lam)), [L(lam), L(lam ** 2), L(lam / 2), L(math.sqrt(lam) / 2)], f'σ = √{L(lam)} = {L(math.sqrt(lam))}.')
    if kind == 'var':
        s = r.choice([1.2, 1.5, 1.8, 2.1, 2.5, 3])
        return MCk(r, f'X has a Poisson distribution with standard deviation {num(s)}. Find E(X).', L(s * s), [num(s), L(math.sqrt(s)), L(2 * s), L(s * s * 2)], f'E(X) = Var(X) = {num(s)}² = {L(s * s)}.')
    if kind == 'ratio':
        k = r.randint(1, 4)
        c = r.choice([Fr(1, 2), Fr(2), Fr(3, 2), Fr(3), Fr(4, 3)])
        lam = c * (k + 1)
        return MCk(r, f'X ~ Po(λ) and P(X = {k + 1}) = {num(c)} × P(X = {k}). Find λ.', num(lam), [num(c), num(c * k), num(c * (k + 2)), num(lam * 2)],
                   f'P(X = {k + 1})/P(X = {k}) = λ/{k + 1} = {num(c)}, so λ = {num(lam)}.')
    p0 = r.choice([0.1, 0.2, 0.25, 0.3, 0.4, 0.5])
    lam = -math.log(p0)
    return MCk(r, f'X ~ Po(λ) and P(X = 0) = {p0}. Find λ, correct to 3 significant figures.', n3(lam), [n3(1 - p0), n3(math.exp(-p0)), n3(-math.log10(p0)), n3(1 / p0)], f'e^({MINUS}λ) = {p0} ⇒ λ = −ln {p0} = {n3(lam)}.')


def freq_table(r, lam, n, over=False):
    """Frequencies for 0..K from Po(lam) expected counts (rounded), optionally overdispersed."""
    K = max(5, int(lam + 3 * math.sqrt(lam)) + 1)
    fs = []
    for x in range(K):
        e = n * ppmf(lam, x)
        fs.append(max(0, int(round(e * (r.uniform(0.85, 1.15))))))
    fs.append(max(0, n - sum(fs)))
    if fs[-1] == 0:
        fs = fs[:-1]
    if over:
        # move mass to the tails
        fs[0] += int(n * 0.12)
        fs[-1] += int(n * 0.1)
        mid = int(lam)
        fs[mid] = max(1, fs[mid] - int(n * 0.22))
    return fs


@po2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def po2_fit(r, D):
    lam = r.choice([1.2, 1.5, 1.8, 2.0, 2.4, 3.0])
    n = r.choice([50, 80, 100, 120, 150, 200])
    over = r.random() < 0.35
    fs = freq_table(r, lam, n, over)
    N = sum(fs)
    xs = list(range(len(fs)))
    sfx = sum(x * f for x, f in zip(xs, fs))
    sfx2 = sum(x * x * f for x, f in zip(xs, fs))
    mean = sfx / N
    var = sfx2 / N - mean ** 2
    ctx = r.choice(['the number of faults found on each of {N} circuit boards', 'the number of insects found on each of {N} leaves', 'the number of phone calls received by a receptionist in each of {N} five-minute periods',
                    'the number of misprints on each of {N} pages of a newspaper', 'the number of birds landing on a feeder in each of {N} one-minute periods'])
    ctx = ctx.format(N=N)
    tab = ', '.join(f'{x}: {f}' for x, f in zip(xs, fs))
    stem = f'{person(r)} records {ctx}. The results (number: frequency) are {tab}.'
    if D == 1:
        return Q(stem + ' Calculate the mean number.', n3(mean), f'M1 Σfx ÷ Σf = {sfx} ÷ {N}; A1 {n3(mean)}')
    close = abs(var - mean) / mean < 0.2
    verdict = (f'Mean {n3(mean)} and variance {n3(var)} are approximately equal, so a Poisson model may be suitable.' if close else
               f'Mean {n3(mean)} and variance {n3(var)} are not close, so a Poisson model is not suitable.')
    if D == 2:
        return Q(stem + ' Calculate the mean and variance of the data.', f'mean {n3(mean)}, variance {n3(var)}', f'M1 Σfx = {sfx}, Σf = {N}; A1 mean {n3(mean)}; M1 Σfx²/Σf − mean² with Σfx² = {sfx2}; A1 {n3(var)}')
    if D == 3:
        return Q(stem + ' Calculate the mean and variance of the data and comment on whether a Poisson distribution might be a suitable model.', f'{verdict}',
                 f'M1 mean {n3(mean)}; M1 variance {n3(var)}; A1 both; B1 comment comparing mean and variance')
    e2 = N * ppmf(mean, 2)
    e0 = N * ppmf(mean, 0)
    return Q(stem + f' Calculate the mean and variance, comment on the suitability of a Poisson model, and, using a Poisson distribution with the same mean, calculate the expected frequencies of 0 and 2.',
             f'{verdict} Expected frequencies: 0: {n3(e0)}, 2: {n3(e2)}.', f'M1 mean {n3(mean)}; A1 variance {n3(var)}; B1 comment; M1 {N} × e^({MINUS}{n3(mean)}); A1 {n3(e0)}; A1 {n3(e2)}')


@po2.add('C3', (1, 2, 3, 4), 'numerical')
def po2_param(r, D):
    kind = r.choice(['ratio', 'sd', 'zero2'])
    if kind == 'ratio':
        a = r.randint(1, 3)
        b = a + 1
        c = r.choice([Fr(1, 2), Fr(3, 4), Fr(5, 4), Fr(3, 2), Fr(2)])
        lam = c * b
        k = r.randint(0, 3)
        v = ppmf(float(lam), k)
        return Q(f'The random variable X has the distribution Po(λ). Given that P(X = {b}) = {num(c)} × P(X = {a}), find λ and hence find P(X = {k}).', f'λ = {num(lam)}; {n3(v)}',
                 f'M1 e^({MINUS}λ)λ{sup(b)}/{b}! = {num(c)} × e^({MINUS}λ)λ{sup(a)}/{a}!; A1 λ = {num(lam)}; A1 {n3(v)}')
    if kind == 'sd':
        s = r.choice([1.2, 1.4, 1.6, 1.8, 2.2])
        lam = s * s
        k = r.randint(1, 3)
        v = 1 - pcdf(lam, k)
        return Q(f'The number of {r.choice(PCTX)[0]} in a given interval has a Poisson distribution with standard deviation {num(s)}. Find the probability that more than {k} occur in the interval.', n3(v),
                 f'B1 λ = {num(s)}² = {L(lam)}; M1 1 − ({terms(lam, range(k + 1))}); A1 {n3(v)}')
    p1 = r.choice([0.2, 0.25, 0.3, 0.35])
    # P(X >= 1) = 1 - p0
    p0 = round(r.uniform(0.05, 0.4), 2)
    lam = -math.log(p0)
    v = 1 - pcdf(lam, 1)
    return Q(f'For a Poisson variable X, P(X ≥ 1) = {num(round(1 - p0, 2))}. Find the value of the mean of X, and hence find P(X ≥ 2).', f'λ = {n3(lam)}; {n3(v)}',
             f'M1 1 − e^({MINUS}λ) = {num(round(1 - p0, 2))}; A1 λ = {n3(lam)}; M1 1 − e^({MINUS}λ)(1 + λ); A1 {n3(v)}')


@po2.add('C2', (2, 3, 4), 'explain')
def po2_err(r, D):
    lam = r.choice([2.5, 3.6, 4.2, 5.1])
    var = round(lam * r.choice([2.2, 2.6, 3.1]), 1)
    nm = person(r)
    kind = r.choice(['mean_only', 'sd'])
    if kind == 'mean_only':
        return Q(f'A sample of count data has mean {num(lam)} and variance {num(var)}. {nm} says that a Poisson model is suitable because the data are counts with mean {num(lam)}. Explain why {nm} is wrong.',
                 f'For a Poisson distribution the variance should be approximately equal to the mean; here the variance {num(var)} is much larger than the mean {num(lam)}, so the data are more spread out than a Poisson model would give.',
                 'B1 mean should equal variance; B1 comparison with these values and conclusion')
    s = math.sqrt(lam)
    return Q(f'X ~ Po({num(lam)}). {nm} says that the standard deviation of X is {num(lam)}. Explain the error and state the correct standard deviation.',
             f'{num(lam)} is the variance; the standard deviation is √{num(lam)} = {n3(s)}.', f'B1 Var(X) = λ; B1 {n3(s)}')


def po2_c4(r, D):
    lam = r.choice([1.6, 2.0, 2.4, 2.8])
    n = r.choice([80, 100, 120])
    fs = freq_table(r, lam, n)
    N = sum(fs)
    xs = list(range(len(fs)))
    sfx = sum(x * f for x, f in zip(xs, fs))
    sfx2 = sum(x * x * f for x, f in zip(xs, fs))
    mean = sfx / N
    var = sfx2 / N - mean ** 2
    m = round(mean, 1)
    tab = ', '.join(f'{x}: {f}' for x, f in zip(xs, fs))
    intro = f'The numbers of flaws found in each of {N} sheets of glass were recorded (number of flaws: frequency): {tab}.'
    w = r.choice([3, 4, 5])
    parts = [
        P('Calculate the mean and variance of the number of flaws per sheet.', f'mean {n3(mean)}, variance {n3(var)}', f'M1 Σfx/Σf; A1 {n3(mean)}; M1 Σfx²/Σf − x̄²; A1 {n3(var)}'),
        P('Comment on whether a Poisson distribution is suitable.', 'Mean and variance are approximately equal, so Poisson may be suitable.' if abs(var - mean) / mean < 0.2 else 'Mean and variance differ, so a Poisson model may not be suitable.', 'B1 comparison and conclusion'),
        P(f'Use the distribution Po({num(m)}) to find the probability that a sheet has more than 2 flaws.', n3(1 - pcdf(m, 2)), f'M1 1 − ({terms(m, range(3))}); A1 {n3(1 - pcdf(m, 2))}'),
        P(f'Use Po({num(m)}) to find the expected number of the {N} sheets with no flaws.', n3(N * math.exp(-m)), f'M1 {N} × e^({MINUS}{num(m)}); A1 {n3(N * math.exp(-m))}'),
        P(f'Sheets are packed in boxes of {w}. Find the probability that a box contains fewer than 3 flaws in total.', n3(pcdf(m * w, 2)), f'B1 Po({L(m * w)}); M1 {terms(m * w, range(3))}; A1 {n3(pcdf(m * w, 2))}'),
    ]
    return cmp_(r, intro, parts)


po2.add('C4', (2, 3, 4, 5))(po2_c4)


po3 = T('Using the Poisson distribution as an approximation to the binomial', 'poisson distribution as an approximation to the binomial', 'approximation to the binomial')
po3.fixed('C1', (1, 2), [
    ('A Poisson distribution is a suitable approximation to B(n, p) when', 'n is large and np is small (n > 50 and np < 5)', 'p small so that λ = np is small. [1]', ['n is small and p is close to 0.5', 'np > 5 and nq > 5', 'p is close to 1']),
    ('X ~ B(400, 0.008). The approximating Poisson distribution is', 'Po(3.2)', 'λ = np = 400 × 0.008. [1]', ['Po(0.008)', 'Po(400)', 'Po(3.17)']),
    ('Which binomial distribution is best approximated by a Poisson distribution?', 'B(500, 0.004)', 'n large, np = 2 small. [1]', ['B(20, 0.4)', 'B(60, 0.5)', 'B(10, 0.02)']),
])
po3.fixed('C2', (2, 3), [
    ('Explain why the Poisson distribution with mean np gives a good approximation to B(n, p) when n is large and p is small.', 'When p is small, 1 − p ≈ 1, so the binomial variance np(1 − p) ≈ np = mean, matching the Poisson property that mean = variance.', 'B1 1 − p ≈ 1; B1 variance ≈ mean [2]'),
    ('Explain why a Poisson approximation would not be suitable for X ~ B(60, 0.45).', 'np = 27 is not small (p is not small), so the variance np(1 − p) = 14.85 is very different from the mean; a normal approximation would be better.', 'B1 np too large / p not small; B1 suggests normal approximation or mean ≠ variance [2]'),
])

BAPPROX = [('A machine produces bolts, of which {p}% are defective. A random sample of {n} bolts is taken.', 'defective bolts'),
           ('In a large population, {p}% of people have a rare blood type. A random sample of {n} people is chosen.', 'people with the rare blood type'),
           ('A seed company states that {p}% of its seeds fail to germinate. A packet of {n} seeds is sown.', 'seeds that fail to germinate'),
           ('On average {p}% of flights from an airport are cancelled. A random sample of {n} flights is chosen.', 'cancelled flights'),
           ('{p}% of the light bulbs made in a factory are faulty. A box of {n} bulbs is chosen at random.', 'faulty bulbs'),
           ('A website finds that {p}% of visitors make a purchase. A random sample of {n} visitors is taken.', 'visitors who make a purchase')]


def rbap(r):
    for _ in range(30):
        n = r.choice([60, 80, 100, 120, 150, 200, 250, 300, 400, 500, 800, 1000])
        p = r.choice([0.2, 0.4, 0.5, 0.6, 0.8, 1, 1.2, 1.5, 2, 2.5, 3])
        lam = n * p / 100
        if 0.5 <= lam < 5 and abs(lam * 100 - round(lam * 100)) < 1e-6:
            return n, p, lam
    return 200, 1, 2.0


@po3.add('C1', (1, 2, 3))
def po3_c1(r, D):
    n, p, lam = rbap(r)
    ctx, what = r.choice(BAPPROX)
    if r.random() < 0.5:
        return MCk(r, ctx.format(p=num(p), n=n) + f' X is the number of {what}. Which distribution is a suitable approximation for X?', f'Po({L(lam)})',
                   [f'Po({num(p)})', f'N({L(lam)}, {L(lam * (1 - p / 100))})', f'Po({L(lam * (1 - p / 100))})', f'Po({n})'], f'n = {n} large, np = {L(lam)} < 5, so Po({L(lam)}).')
    k = r.randint(0, 2)
    v = ppmf(lam, k)
    return MCk(r, ctx.format(p=num(p), n=n) + f' Use a Poisson approximation to find the probability that there are exactly {k} {what}.', n3(v),
               [n3(bpmf(n, p / 100, k)) if n3(bpmf(n, p / 100, k)) != n3(v) else n3(v * 1.1), n3(ppmf(lam, k + 1)), n3(pcdf(lam, k)) if k else n3(1 - v), n3(ppmf(p, k))], f'Po({L(lam)}): {ex(lam, k)} = {n3(v)}.')


@po3.add('C2', (2, 3, 4), 'explain')
def po3_err(r, D):
    n, p, lam = rbap(r)
    ctx, what = r.choice(BAPPROX)
    nm = person(r)
    k = r.randint(1, 3)
    kind = r.choice(['var', 'bad'])
    if kind == 'var':
        wl = lam * (1 - p / 100)
        return Q(ctx.format(p=num(p), n=n) + f' {nm} approximates the number of {what} by Po({L(wl)}), using λ = np(1 − p). Explain the error and find the approximate probability that there are at most {k}.',
                 f'The Poisson parameter is the mean, λ = np = {L(lam)}; P(X ≤ {k}) ≈ {n3(pcdf(lam, k))}.', f'B1 λ = np = {L(lam)}; M1 {terms(lam, range(k + 1))}; A1 {n3(pcdf(lam, k))}')
    n2 = r.choice([40, 50, 60])
    p2 = r.choice([30, 40, 45, 55])
    return Q(f'{nm} wants to use a Poisson approximation for X ~ B({n2}, {num(p2 / 100)}). Explain why this is not appropriate and suggest a more suitable approximation, stating its parameters.',
             f'np = {L(n2 * p2 / 100)} is not small (p is not small), so the mean and variance {L(n2 * p2 / 100 * (1 - p2 / 100))} differ; use N({L(n2 * p2 / 100)}, {L(n2 * p2 / 100 * (1 - p2 / 100))}).',
             f'B1 np > 5 / p not small; B1 normal approximation; B1 N({L(n2 * p2 / 100)}, {L(n2 * p2 / 100 * (1 - p2 / 100))})')


@po3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def po3_calc(r, D):
    n, p, lam = rbap(r)
    ctx, what = r.choice(BAPPROX)
    stem = ctx.format(p=num(p), n=n)
    pp = p / 100
    if D <= 2:
        k = r.randint(1, 3)
        v = pcdf(lam, k)
        return Q(stem + f' Use a suitable approximation to find the probability that there are at most {k} {what}.', n3(v), f'B1 Po({L(lam)}); M1 {terms(lam, range(k + 1))}; A1 {n3(v)}')
    if D == 3:
        k = r.randint(2, 4)
        v = 1 - pcdf(lam, k - 1)
        return Q(stem + f' Use a suitable approximation to find the probability that there are at least {k} {what}. Justify your choice of approximation.', n3(v),
                 f'B1 n = {n} > 50 and np = {L(lam)} < 5; B1 Po({L(lam)}); M1 1 − ({terms(lam, range(k))}); A1 {n3(v)}')
    k = r.randint(1, 3)
    va = pcdf(lam, k)
    vb = bcdf(n, pp, k)
    err = abs(va - vb) / vb * 100
    if D == 4:
        return Q(stem + f' Find P(X ≤ {k}), where X is the number of {what}, using (i) the binomial distribution, (ii) a Poisson approximation. Calculate the percentage error in the approximation.',
                 f'(i) {n3(vb)} (ii) {n3(va)}; percentage error {n3(err)}%', f'M1 binomial terms; A1 {n3(vb)}; M1 Po({L(lam)}); A1 {n3(va)}; B1 {n3(err)}%')
    m = r.choice([3, 4, 5])
    pz = math.exp(-lam)
    v = 1 - (1 - pz) ** m
    return Q(stem + f' {m} such samples are taken. Use a Poisson approximation to find the probability that at least one of the samples contains no {what}.', n3(v),
             f'B1 P(none) ≈ e^({MINUS}{L(lam)}) = {n3(pz)}; M1 1 − (1 − {n3(pz)}){sup(m)}; A1 {n3(v)}')


def po3_c4(r, D):
    n, p, lam = rbap(r)
    ctx, what = r.choice(BAPPROX)
    pp = p / 100
    k = r.randint(1, 3)
    n2 = n * r.choice([2, 3])
    l2 = n2 * pp
    if l2 >= 15:
        return None
    intro = ctx.format(p=num(p), n=n) + f' X is the number of {what}.'
    parts = [
        P('State the exact distribution of X.', f'B({n}, {num(pp)})', 'B1'),
        P('Explain why a Poisson distribution can be used as an approximation, stating its mean.', f'n = {n} is large and np = {L(lam)} < 5; Po({L(lam)})', 'B1 conditions; B1 λ'),
        P(f'Use the approximation to find P(X ≤ {k}).', n3(pcdf(lam, k)), f'M1 {terms(lam, range(k + 1))}; A1 {n3(pcdf(lam, k))}'),
        P(f'A larger sample of {n2} is taken. Use a Poisson approximation to find the probability that it contains more than {int(l2) + 1} {what}.', n3(1 - pcdf(l2, int(l2) + 1)),
          f'B1 Po({L(l2)}); M1 1 − P(Y ≤ {int(l2) + 1}); A1 {n3(1 - pcdf(l2, int(l2) + 1))}'),
    ]
    return cmp_(r, intro, parts)


po3.add('C4', (2, 3, 4, 5))(po3_c4)


po4 = T('Normal approximation to the Poisson distribution with continuity correction', 'normal approximation to the poisson', 'continuity correction')
po4.fixed('C1', (1, 2), [
    ('X ~ Po(30). The approximating normal distribution is', 'N(30, 30)', 'Mean = variance = λ. [1]', ['N(30, √30)', 'N(30, 900)', 'N(0, 30)']),
    ('A normal approximation to Po(λ) is suitable when', 'λ > 15', 'Syllabus condition: λ large (λ > 15). [1]', ['λ < 5', 'λ is an integer', 'λ < 1']),
    ('When X ~ Po(25) is approximated by Y ~ N(25, 25), P(X ≤ 20) is approximated by', 'P(Y < 20.5)', 'Continuity correction: X ≤ 20 includes 20, so use 20.5. [1]', ['P(Y < 19.5)', 'P(Y < 20)', 'P(Y > 20.5)']),
    ('When X ~ Po(40) is approximated by Y ~ N(40, 40), P(X > 45) is approximated by', 'P(Y > 45.5)', 'X > 45 means X ≥ 46, so use 45.5. [1]', ['P(Y > 44.5)', 'P(Y > 45)', 'P(Y < 45.5)']),
])
po4.fixed('C2', (2, 3), [
    ('Explain why a continuity correction is needed when a normal distribution is used to approximate a Poisson distribution.', 'The Poisson distribution is discrete but the normal is continuous; each integer value is represented by the interval of width 1 centred on it, so boundaries are moved by 0.5.', 'B1 discrete to continuous; B1 interval x ± 0.5 [2]'),
    ('Explain why the normal distribution is a good approximation to Po(λ) for large λ.', 'As λ increases the Poisson distribution becomes more symmetrical and bell-shaped, so N(λ, λ) gives a good fit.', 'B1 symmetrical / bell-shaped for large λ; B1 N(λ, λ) [2]'),
])

NCTX = [('calls to a call centre', 'an hour', (20, 60)), ('cars passing a toll booth', 'a 10-minute period', (18, 45)), ('emails received by a company', 'an hour', (25, 80)),
        ('customers entering a supermarket', 'a 15-minute period', (20, 50)), ('particles emitted by a radioactive source', 'a minute', (30, 90)),
        ('hits on a website', 'a minute', (40, 120)), ('goals scored in a football league', 'a weekend', (20, 40)), ('ambulance call-outs in a city', 'a day', (16, 40))]


def cc_text(kind, k):
    return {'le': (f'at most {k}', k + 0.5, 'lt'), 'lt': (f'fewer than {k}', k - 0.5, 'lt'), 'ge': (f'at least {k}', k - 0.5, 'gt'), 'gt': (f'more than {k}', k + 0.5, 'gt')}[kind]


@po4.add('C1', (1, 2, 3))
def po4_c1(r, D):
    c = r.choice(NCTX)
    lam = r.randint(*c[2])
    kind = r.choice(['le', 'lt', 'ge', 'gt'])
    k = lam + r.choice([-6, -4, -3, 3, 4, 6])
    txt, b, side = cc_text(kind, k)
    sym = '<' if side == 'lt' else '>'
    return MCk(r, f'The number of {c[0]} in {c[1]} has the distribution Po({lam}) and is approximated by Y ~ N({lam}, {lam}). The probability that there are {txt} is approximated by', f'P(Y {sym} {num(b)})',
               [f'P(Y {sym} {num(2 * k - b)})', f'P(Y {sym} {k})', f'P(Y {"<" if sym == ">" else ">"} {num(b)})', f'P(Y {sym} {num(b + 1)})'], f'Continuity correction: {txt} → Y {sym} {num(b)}.')


@po4.add('C3', (1, 2, 3, 4, 5), 'numerical')
def po4_calc(r, D):
    c = r.choice(NCTX)
    lam = r.randint(*c[2])
    s = math.sqrt(lam)
    stem = f'The number of {c[0]} in {c[1]} has the distribution Po({lam}).'
    if D <= 2:
        kind = r.choice(['le', 'ge'])
        k = lam + (r.randint(-8, -2) if kind == 'le' else r.randint(2, 8))
        txt, b, side = cc_text(kind, k)
        z = (b - lam) / s
        v = Phi(z) if side == 'lt' else 1 - Phi(z)
        return Q(stem + f' Use a suitable approximation to find the probability that there are {txt} in {c[1]}.', n3(v),
                 f'B1 N({lam}, {lam}); M1 continuity correction {num(b)}; M1 standardise ({num(b)} − {lam})/√{lam} = {z3(z)}; A1 {n3(v)}')
    if D == 3:
        a = lam - r.randint(2, 6)
        bb = lam + r.randint(2, 6)
        z1, z2 = (a - 0.5 - lam) / s, (bb + 0.5 - lam) / s
        v = Phi(z2) - Phi(z1)
        return Q(stem + f' Use a suitable approximation to find the probability that the number in {c[1]} is between {a} and {bb} inclusive.', n3(v),
                 f'B1 N({lam}, {lam}); M1 {num(a - 0.5)} and {num(bb + 0.5)}; M1 standardise both: {z3(z1)}, {z3(z2)}; A1 {n3(v)}')
    if D == 4:
        base = r.choice([lam / 3, lam / 4, lam / 2])
        base = round(base, 1)
        m = r.choice([3, 4, 5, 6])
        l2 = base * m
        if l2 <= 15:
            return None
        k = int(l2) + r.randint(2, 6)
        z = (k - 0.5 - l2) / math.sqrt(l2)
        v = 1 - Phi(z)
        return Q(f'The number of {c[0]} has a Poisson distribution with mean {num(base)} per unit interval. Use a suitable approximation to find the probability that there are at least {k} in {m} unit intervals.', n3(v),
                 f'B1 λ = {L(l2)}; B1 N({L(l2)}, {L(l2)}); M1 ({num(k - 0.5)} − {L(l2)})/√{L(l2)} = {z3(z)}; A1 {n3(v)}')
    # D5: find k with P(X >= k) < alpha
    alpha = r.choice([0.05, 0.1, 0.02])
    zc_ = invPhi(1 - alpha)
    # smallest k with 1 - Phi((k - 0.5 - lam)/s) < alpha  -> k - 0.5 > lam + zc s
    k = math.floor(lam + zc_ * s + 0.5) + 1
    while 1 - Phi((k - 1 - 0.5 - lam) / s) < alpha:
        k -= 1
    while 1 - Phi((k - 0.5 - lam) / s) >= alpha:
        k += 1
    return Q(stem + f' Use a normal approximation to find the smallest integer k such that the probability of at least k {c[0]} in {c[1]} is less than {alpha}.', str(k),
             f'B1 N({lam}, {lam}); M1 (k − 0.5 − {lam})/√{lam} > {z3(zc_)}; M1 solve: k > {n3(lam + 0.5 + zc_ * s)}; A1 k = {k}')


@po4.add('C2', (2, 3, 4), 'explain')
def po4_err(r, D):
    c = r.choice(NCTX)
    lam = r.randint(*c[2])
    s = math.sqrt(lam)
    k = lam + r.randint(2, 7)
    nm = person(r)
    kind = r.choice(['nocc', 'sd'])
    right = 1 - Phi((k + 0.5 - lam) / s)
    if kind == 'nocc':
        return Q(f'The number of {c[0]} in {c[1]} has the distribution Po({lam}). {nm} uses N({lam}, {lam}) to find P(more than {k}) as P(Y > {k}). Explain the error and find the correct approximate probability.',
                 f'A continuity correction is needed: “more than {k}” means X ≥ {k + 1}, so use P(Y > {num(k + 0.5)}) = {n3(right)}.', f'B1 continuity correction {num(k + 0.5)}; M1 ({num(k + 0.5)} − {lam})/√{lam}; A1 {n3(right)}')
    wrong = 1 - Phi((k + 0.5 - lam) / lam)
    return Q(f'The number of {c[0]} in {c[1]} has the distribution Po({lam}). {nm} approximates P(more than {k}) by standardising with ({num(k + 0.5)} − {lam}) ÷ {lam}. Explain the error and find the correct approximate probability.',
             f'The variance is {lam}, so the standard deviation is √{lam} = {n3(s)}; dividing by {lam} is wrong. P = 1 − Φ({z3((k + 0.5 - lam) / s)}) = {n3(right)}.', f'B1 divide by √{lam}; M1 standardise correctly; A1 {n3(right)}')


def po4_c4(r, D):
    c = r.choice(NCTX)
    base = r.choice([2.5, 3, 3.5, 4, 4.5, 5])
    m = r.choice([5, 6, 8, 10])
    l2 = base * m
    if l2 <= 15:
        return None
    k1 = r.randint(1, 3)
    k2 = int(l2) - r.randint(3, 6)
    z = (k2 + 0.5 - l2) / math.sqrt(l2)
    intro = f'The number of {c[0]} in a one-minute period has the distribution Po({num(base)}).'
    parts = [
        P(f'Find the probability that there are at most {k1} in a one-minute period.', n3(pcdf(base, k1)), f'M1 {terms(base, range(k1 + 1))}; A1 {n3(pcdf(base, k1))}'),
        P(f'State the distribution of the number in a {m}-minute period and explain why a normal approximation is appropriate.', f'Po({L(l2)}); λ = {L(l2)} > 15', 'B1 Po; B1 reason'),
        P(f'Use a suitable approximation to find the probability that there are at most {k2} in a {m}-minute period.', n3(Phi(z)), f'B1 N({L(l2)}, {L(l2)}); M1 continuity correction {num(k2 + 0.5)}; M1 z = {z3(z)}; A1 {n3(Phi(z))}'),
    ]
    return cmp_(r, intro, parts, k=(2, 3))


po4.add('C4', (2, 3, 4, 5))(po4_c4)

CHAPTERS[1] = [po1, po2, po3, po4]


# ================================================================ Chapter 2: Linear combinations of random variables

def lin_s(a, b, v='X'):
    """'3X + 2', 'X − 4', '5 − 2X'."""
    a, b = Fr(a), Fr(b)
    if a == 1:
        t = v
    elif a == -1:
        t = MINUS + v
    else:
        t = num(a) + v
    if b == 0:
        return t
    return f'{t} + {num(b)}' if b > 0 else f'{t} − {num(-b)}'


def rdist(r):
    """A discrete distribution with exact Fraction probabilities."""
    for _ in range(40):
        k = r.choice([3, 4])
        xs = sorted(r.sample(range(0, 7), k))
        den = r.choice([10, 20])
        cuts = sorted(r.sample(range(1, den), k - 1))
        ps = [Fr(b - a, den) for a, b in zip([0] + cuts, cuts + [den])]
        if all(p > 0 for p in ps):
            return xs, ps
    return [0, 1, 2], [Fr(1, 4), Fr(1, 2), Fr(1, 4)]


def mv(xs, ps):
    e = sum(x * p for x, p in zip(xs, ps))
    e2 = sum(x * x * p for x, p in zip(xs, ps))
    return e, e2 - e * e


lc1 = T('E(aX + b) and Var(aX + b)', 'e(ax + b)', 'var(ax + b)')
lc1.fixed('C1', (1, 2), [
    ('If Var(X) = 4, then Var(3X + 5) =', '36', 'Var(aX + b) = a²Var(X) = 9 × 4. [1]', ['17', '12', '41']),
    ('If E(X) = 6, then E(2X − 3) =', '9', 'E(aX + b) = aE(X) + b. [1]', ['12', '3', '15']),
    ('Adding a constant to every value of a random variable', 'changes the mean but not the variance', 'Var(X + b) = Var(X). [1]', ['changes the variance but not the mean', 'changes both the mean and the variance', 'changes neither']),
    ('If Var(X) = 5, then Var(4 − X) =', '5', 'Var(b − X) = (−1)²Var(X). [1]', ['−1', '1', '−5']),
])
lc1.fixed('C2', (2, 3), [
    ('Explain why Var(X − 7) = Var(X).', 'Subtracting 7 shifts every value (and the mean) by the same amount, so deviations from the mean, and hence the spread, are unchanged.', 'B1 shift of all values and mean; B1 spread unchanged [2]'),
    ('Explain why the standard deviation of −2X is 2σ, not −2σ, where σ is the standard deviation of X.', 'Var(−2X) = (−2)²Var(X) = 4σ², and the standard deviation is the positive square root, 2σ.', 'B1 (−2)²; B1 standard deviation is non-negative [2]'),
])


@lc1.add('C1', (1, 2, 3))
def lc1_c1(r, D):
    m = r.randint(-5, 20)
    v = r.choice([2, 3, 4, 5, 6, 8, 9, 2.5, 1.5])
    a = r.choice([2, 3, 4, 5, -2, -3, Fr(1, 2)])
    b = r.randint(-10, 10)
    if r.random() < 0.5:
        e = a * m + b
        return MCk(r, f'E(X) = {num(m)} and Var(X) = {num(v)}. Find E({lin_s(a, b)}).', num(e), [num(a * m), num(m + b), num(a * a * m + b), num(a * m - b) if b else num(a * m + 1)], f'E({lin_s(a, b)}) = {num(a)} × {pn(num(m))} {"+" if b >= 0 else "−"} {abs(b)} = {num(e)}.')
    vv = Fr(a) ** 2 * Fr(v)
    return MCk(r, f'E(X) = {num(m)} and Var(X) = {num(v)}. Find Var({lin_s(a, b)}).', num(vv), [num(a * Fr(v)), num(vv + b) if b else num(vv + 1), num(abs(a) * Fr(v) + abs(b)), num(Fr(v))], f'Var({lin_s(a, b)}) = ({num(a)})² × {num(v)} = {num(vv)}.')


@lc1.add('C2', (2, 3, 4), 'explain')
def lc1_err(r, D):
    m = r.randint(3, 30)
    v = r.choice([2, 3, 4, 5, 6, 8, 9])
    a = r.choice([2, 3, 4, 5])
    b = r.randint(2, 15)
    nm = person(r)
    kind = r.choice(['lin', 'addb', 'sd'])
    if kind == 'lin':
        return Q(f'Var(X) = {v}. {nm} writes Var({lin_s(a, -b)}) = {a} × {v} − {b} = {a * v - b}. Explain the errors and find the correct value.',
                 f'The constant does not affect the variance and the multiplier must be squared: Var({lin_s(a, -b)}) = {a}² × {v} = {a * a * v}.', f'B1 constant has no effect; B1 multiplier squared; B1 {a * a * v}')
    if kind == 'addb':
        return Q(f'Var(X) = {v}. {nm} writes Var({lin_s(a, b)}) = {a}² × {v} + {b}² = {a * a * v + b * b}. Explain the error and find the correct value.',
                 f'Adding the constant {b} shifts all values equally and does not change the variance: Var = {a * a * v}.', f'B1 constant does not change variance; B1 {a * a * v}')
    sd = math.sqrt(v)
    return Q(f'X has standard deviation {n3(sd)}. {nm} says the standard deviation of {lin_s(-a, b)} is {MINUS}{a} × {n3(sd)} = {MINUS}{n3(a * sd)}. Explain the error and find the correct standard deviation.',
             f'Standard deviation cannot be negative: Var = ({MINUS}{a})² × {v} = {a * a * v}, so the standard deviation is {n3(a * sd)}.', f'B1 standard deviation is non-negative / square the multiplier; B1 {n3(a * sd)}')


@lc1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def lc1_table(r, D):
    xs, ps = rdist(r)
    e, v = mv(xs, ps)
    a = r.choice([2, 3, 4, 5, 10])
    b = r.choice([-6, -5, -4, -3, 2, 5, 8, 12, 20])
    tab = ', '.join(f'P(X = {x}) = {num(p)}' for x, p in zip(xs, ps))
    ctx = r.choice(['The number of goals X scored by a team in a match has the probability distribution', 'The number of faulty items X in a box has the distribution',
                    'The score X on a biased spinner has the distribution', 'The number of children X in a randomly chosen family in a town has the distribution'])
    stem = f'{ctx} {tab}.'
    if D == 1:
        return Q(stem + ' Find E(X).', num(e), f'M1 Σxp; A1 {num(e)}')
    if D == 2:
        return Q(stem + ' Find E(X) and Var(X).', f'E(X) = {num(e)}, Var(X) = {num(v)}', f'M1 Σxp = {num(e)}; M1 Σx²p − [E(X)]²; A1 Var(X) = {num(v)}')
    E2 = a * e + b
    V2 = a * a * v
    if D == 3:
        return Q(stem + f' Find E({lin_s(a, b)}) and Var({lin_s(a, b)}).', f'{num(E2)}, {num(V2)}', f'M1 E(X) = {num(e)}; A1 E = {num(E2)}; M1 Var(X) = {num(v)}; A1 Var = {num(V2)}')
    price = r.choice([5, 8, 10, 12, 15])
    fixed = r.choice([3, 5, 6, 10])
    E3 = price * e - fixed
    V3 = price * price * v
    return Q(f'{stem} The profit, in dollars, is {price}X − {fixed}. Find the mean and standard deviation of the profit.', f'mean ${num(E3)}, standard deviation ${n3(math.sqrt(V3))}',
             f'M1 E(X) = {num(e)}; A1 {num(E3)}; M1 Var(X) = {num(v)}; M1 {price}² × {num(v)} = {num(V3)}; A1 {n3(math.sqrt(V3))}')


@lc1.add('C3', (1, 2, 3, 4), 'numerical')
def lc1_conv(r, D):
    kind = r.choice(['temp', 'pay', 'score'])
    if kind == 'temp':
        m = r.randint(12, 32)
        s = r.choice([2, 2.5, 3, 4, 5])
        ef = Fr(9, 5) * m + 32
        sf_ = Fr(9, 5) * Fr(s)
        return Q(f'The daily maximum temperature in {city(r)} in July, X °C, has mean {m} and standard deviation {num(s)}. The temperature in °F is F = 1.8X + 32. Find the mean and standard deviation of F.',
                 f'mean {num(ef)} °F, standard deviation {num(sf_)} °F', f'M1 1.8 × {m} + 32; A1 {num(ef)}; M1 1.8 × {num(s)}; A1 {num(sf_)}')
    if kind == 'pay':
        m = r.randint(20, 45)
        s = r.choice([4, 5, 6, 8])
        rate = r.choice([12, 15, 18, 20])
        base = r.choice([50, 80, 100])
        return Q(f'The number of hours, H, worked per week by part-time staff has mean {m} and standard deviation {s}. Weekly pay is ${rate}H + {base}. Find the mean and variance of weekly pay.',
                 f'mean ${rate * m + base}, variance {rate * rate * s * s}', f'M1 {rate} × {m} + {base}; A1 {rate * m + base}; M1 {rate}² × {s}²; A1 {rate * rate * s * s}')
    m = r.randint(40, 70)
    s = r.randint(8, 15)
    tm, ts = r.choice([(50, 10), (100, 15), (60, 12)])
    a = Fr(ts, s)
    b = tm - a * m
    return Q(f'Raw test scores X have mean {m} and standard deviation {s}. They are scaled to Y = aX + b, with a > 0, so that Y has mean {tm} and standard deviation {ts}. Find a and b.',
             f'a = {num(a)}, b = {num(b)}', f'M1 a × {s} = {ts}; A1 a = {num(a)}; M1 {num(a)} × {m} + b = {tm}; A1 b = {num(b)}')


def lc1_c4(r, D):
    xs, ps = rdist(r)
    e, v = mv(xs, ps)
    a = r.choice([2, 3, 5])
    b = r.choice([1, 4, 7, -2])
    tab = ', '.join(f'P(X = {x}) = {num(p)}' for x, p in zip(xs, ps))
    nm = person(r)
    intro = f'In a game, {nm} spins a spinner and the score X has the distribution {tab}. The player wins {lin_s(a, b)} points.'
    parts = [
        P('Find E(X).', num(e), f'M1 Σxp; A1 {num(e)}'),
        P('Find Var(X).', num(v), f'M1 Σx²p = {num(v + e * e)}; A1 {num(v)}'),
        P(f'Find the mean and variance of the number of points won.', f'{num(a * e + b)}, {num(a * a * v)}', f'M1 {a}E(X) {"+" if b > 0 else "−"} {abs(b)}; A1 {num(a * e + b)}; A1 {num(a * a * v)}'),
        P('Find the probability that the points won are greater than the mean number of points won.', num(sum(p for x, p in zip(xs, ps) if a * x + b > a * e + b)),
          f'M1 identifies values with {lin_s(a, b)} > {num(a * e + b)}, i.e. X > {num(e)}; A1 {num(sum(p for x, p in zip(xs, ps) if a * x + b > a * e + b))}'),
    ]
    return cmp_(r, intro, parts)


lc1.add('C4', (2, 3, 4, 5))(lc1_c4)


lc2 = T('E(aX + bY) and Var(aX + bY) for independent random variables', 'e(ax + by)', 'var(ax + by)', 'independent random variables')
lc2.fixed('C1', (1, 2), [
    ('For independent X and Y, Var(X − Y) =', 'Var(X) + Var(Y)', 'Var(X − Y) = Var(X) + (−1)²Var(Y). [1]', ['Var(X) − Var(Y)', 'Var(Y) − Var(X)', '[Var(X) − Var(Y)]²']),
    ('X₁, X₂ and X₃ are independent observations of X, with Var(X) = 4. Var(X₁ + X₂ + X₃) =', '12', '3 × 4; compare Var(3X) = 36. [1]', ['36', '4', '6']),
    ('If X has variance 5, Var(2X) is', '20', '2² × 5; compare Var(X₁ + X₂) = 10. [1]', ['10', '5', '25']),
    ('E(aX + bY) = aE(X) + bE(Y) holds', 'for any random variables X and Y', 'The independence condition is needed only for the variance result. [1]', ['only if X and Y are independent', 'only if X and Y are normal', 'only if a and b are positive']),
])
lc2.fixed('C2', (2, 3), [
    ('Explain the difference between 2X and X₁ + X₂, where X₁ and X₂ are independent observations of X.', '2X doubles a single observation, so Var(2X) = 4Var(X); X₁ + X₂ adds two independent observations, whose variation partly cancels, so Var(X₁ + X₂) = 2Var(X).', 'B1 2X is one value doubled, variance 4Var(X); B1 sum of two, variance 2Var(X) [2]'),
    ('State the condition needed for Var(X + Y) = Var(X) + Var(Y), and explain why it matters.', 'X and Y must be independent; if they are related, large values of X may tend to occur with large (or small) values of Y, increasing (or reducing) the variance of the sum.', 'B1 independent; B1 explanation [2]'),
])


@lc2.add('C1', (1, 2, 3))
def lc2_c1(r, D):
    ex_, vx = r.randint(2, 20), r.randint(1, 9)
    ey, vy = r.randint(2, 20), r.randint(1, 9)
    a, b = r.choice([1, 2, 3, 4]), r.choice([1, 2, 3, -1, -2, -3])
    if r.random() < 0.4:
        e = a * ex_ + b * ey
        return MCk(r, f'X and Y are independent with E(X) = {ex_}, Var(X) = {vx}, E(Y) = {ey}, Var(Y) = {vy}. Find E({lin_s(a, 0)} {"+" if b > 0 else "−"} {lin_s(abs(b), 0, "Y")}).', num(e),
                   [num(a * ex_ - b * ey), num(ex_ + ey), num(a * a * ex_ + b * b * ey), num(e + 1)], f'{a} × {ex_} {"+" if b > 0 else "−"} {abs(b)} × {ey} = {e}.')
    v = a * a * vx + b * b * vy
    return MCk(r, f'X and Y are independent with Var(X) = {vx} and Var(Y) = {vy}. Find Var({lin_s(a, 0)} {"+" if b > 0 else "−"} {lin_s(abs(b), 0, "Y")}).', num(v),
               [num(a * a * vx - b * b * vy), num(a * vx + abs(b) * vy), num(a * vx + b * vy), num((a * a * vx + b * b * vy) * 2)], f'{a}² × {vx} + ({b})² × {vy} = {v}.')


@lc2.add('C2', (2, 3, 4), 'explain')
def lc2_err(r, D):
    vx, vy = r.randint(2, 12), r.randint(2, 12)
    nm = person(r)
    n = r.randint(3, 6)
    kind = r.choice(['minus', 'multi'])
    if kind == 'minus':
        return Q(f'X and Y are independent with Var(X) = {vx} and Var(Y) = {vy}. {nm} writes Var(X − Y) = {vx} − {vy} = {vx - vy}. Explain the error and find the correct value.',
                 f'Variances add for a difference: Var(X − Y) = Var(X) + (−1)²Var(Y) = {vx + vy}.', f'B1 (−1)² = 1 so variances add; B1 {vx + vy}')
    return Q(f'The mass of a randomly chosen apple has variance {vx} g². {nm} says the variance of the total mass of {n} randomly chosen apples is {n}² × {vx} = {n * n * vx} g². Explain the error and find the correct value.',
             f'The total is X₁ + … + X{SUBN(n)} of independent apples, not {n}X: Var = {n} × {vx} = {n * vx} g².', f'B1 sum of independent observations, not {n}X; B1 {n * vx}')


@lc2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def lc2_calc(r, D):
    ctx = r.choice([('the time, in minutes, taken to cook a meal', 'the time, in minutes, taken to serve it'), ('the mass, in grams, of an empty jar', 'the mass, in grams, of jam put in it'),
                    ('the length, in cm, of a red rod', 'the length, in cm, of a blue rod'), ('the score of a student on paper 1', 'the score of a different, randomly chosen student on paper 2'),
                    ('the daily number of litres of milk produced by cow A', 'the daily number of litres produced by cow B')])
    ex_, sx = r.randint(10, 60), r.randint(2, 8)
    ey, sy = r.randint(10, 60), r.randint(2, 8)
    stem = f'X is {ctx[0]} and Y is {ctx[1]}. X and Y are independent, with E(X) = {ex_}, standard deviation {sx}, E(Y) = {ey} and standard deviation {sy}.'
    if D <= 2:
        return Q(stem + ' Find the mean and variance of X + Y.', f'{ex_ + ey}, {sx * sx + sy * sy}', f'B1 mean {ex_ + ey}; M1 {sx}² + {sy}²; A1 {sx * sx + sy * sy}')
    a, b = r.choice([2, 3]), r.choice([2, 3, 4])
    if D == 3:
        return Q(stem + f' Find the mean and standard deviation of {a}X − {b}Y.', f'{a * ex_ - b * ey}, {n3(math.sqrt(a * a * sx * sx + b * b * sy * sy))}',
                 f'B1 mean {a * ex_ - b * ey}; M1 {a}² × {sx * sx} + {b}² × {sy * sy}; A1 {n3(math.sqrt(a * a * sx * sx + b * b * sy * sy))}')
    n = r.randint(3, 6)
    vs = n * sx * sx + sy * sy
    vm = n * n * sx * sx + sy * sy
    return Q(stem + f' Let T = X₁ + X₂ + … + X{n} + Y, where the Xᵢ are independent observations of X. Find E(T) and Var(T), and compare Var(T) with Var({n}X + Y).',
             f'E(T) = {n * ex_ + ey}; Var(T) = {vs}; Var({n}X + Y) = {vm}, which is larger.', f'B1 E(T) = {n * ex_ + ey}; M1 {n} × {sx * sx} + {sy * sy}; A1 {vs}; M1 {n}² × {sx * sx} + {sy * sy}; A1 {vm}')


def lc2_c4(r, D):
    ex_, vx = r.randint(20, 60), r.randint(4, 25)
    ey, vy = r.randint(20, 60), r.randint(4, 25)
    n = r.randint(2, 5)
    intro = f'The random variables X and Y are independent, with E(X) = {ex_}, Var(X) = {vx}, E(Y) = {ey} and Var(Y) = {vy}.'
    parts = [
        P('Find E(2X + 3Y) and Var(2X + 3Y).', f'{2 * ex_ + 3 * ey}, {4 * vx + 9 * vy}', f'B1 {2 * ex_ + 3 * ey}; M1 4 × {vx} + 9 × {vy}; A1 {4 * vx + 9 * vy}'),
        P('Find E(X − Y) and Var(X − Y).', f'{ex_ - ey}, {vx + vy}', f'B1 {ex_ - ey}; B1 {vx + vy}'),
        P(f'Find the variance of the sum of {n} independent observations of X.', str(n * vx), f'M1 {n} × {vx}; A1 {n * vx}'),
        P(f'Find Var({n}X) and explain why it differs from your previous answer.', f'{n * n * vx}; {n}X is one observation multiplied by {n}, so its variance is {n}² × Var(X)', f'B1 {n * n * vx}; B1 explanation'),
    ]
    return cmp_(r, intro, parts, deps={3: [2]})


lc2.add('C4', (2, 3, 4, 5))(lc2_c4)


lc3 = T('Linear combinations of independent normal variables', 'linear combinations of independent normal variables', 'normal variables')
lc3.fixed('C1', (1, 2), [
    ('X ~ N(10, 4) and Y ~ N(15, 9) are independent. The distribution of X + Y is', 'N(25, 13)', 'Means add; variances add. [1]', ['N(25, 5)', 'N(25, 25)', 'N(25, 36)']),
    ('X ~ N(20, 5) and Y ~ N(12, 3) are independent. The distribution of X − Y is', 'N(8, 8)', 'Variances add for a difference. [1]', ['N(8, 2)', 'N(32, 8)', 'N(8, 4)']),
    ('X ~ N(μ, σ²). The distribution of 3X is', 'N(3μ, 9σ²)', 'Var(3X) = 9σ². [1]', ['N(3μ, 3σ²)', 'N(μ, 9σ²)', 'N(3μ, σ²)']),
])

NPAIRS = [('the mass of a randomly chosen bag of flour', 'g', (1000, 1020), (6, 15), 'the mass of an empty box', 'g', (200, 260), (5, 12), False),
          ('the time taken by Amara to complete a crossword', 'minutes', (25, 40), (3, 7), 'the time taken by Lucas', 'minutes', (25, 40), (3, 7), True),
          ('the length of a rod of type A', 'cm', (40, 80), (1, 3), 'the length of a rod of type B', 'cm', (30, 70), (1, 3), True),
          ('the mass of a randomly chosen man', 'kg', (70, 85), (8, 12), 'the mass of a randomly chosen woman', 'kg', (55, 70), (6, 10), True),
          ('the volume of drink in a bottle', 'ml', (495, 510), (3, 6), 'the volume of a jug', 'ml', (500, 520), (4, 8), True),
          ('the time for a bus journey from home to the station', 'minutes', (20, 35), (2, 5), 'the time for the train journey that follows', 'minutes', (40, 70), (3, 8), False)]


def rnp(r):
    c = r.choice(NPAIRS)
    mx, sx = r.randint(*c[2]), r.randint(*c[3])
    my, sy = r.randint(*c[6]), r.randint(*c[7])
    return c, mx, sx, my, sy


@lc3.add('C1', (1, 2, 3))
def lc3_c1(r, D):
    mx, vx, my, vy = r.randint(5, 40), r.randint(2, 20), r.randint(5, 40), r.randint(2, 20)
    a = r.choice([2, 3, 4])
    kind = r.choice(['diff', 'combo'])
    if kind == 'diff':
        return MCk(r, f'X ~ N({mx}, {vx}) and Y ~ N({my}, {vy}) are independent. State the distribution of X − Y.', f'N({mx - my}, {vx + vy})', [f'N({mx - my}, {vx - vy})', f'N({mx + my}, {vx + vy})', f'N({mx - my}, {vx * vx + vy * vy})', f'N({my - mx}, {abs(vx - vy) + 1})'],
                   f'Mean {mx} − {my}; variance {vx} + {vy}.')
    return MCk(r, f'X ~ N({mx}, {vx}) and Y ~ N({my}, {vy}) are independent. State the distribution of {a}X + Y.', f'N({a * mx + my}, {a * a * vx + vy})', [f'N({a * mx + my}, {a * vx + vy})', f'N({a * mx + my}, {a * a * vx + vy * vy})', f'N({mx + my}, {a * a * vx + vy})', f'N({a * mx + my}, {a * (vx + vy)})'],
               f'Mean {a} × {mx} + {my}; variance {a}² × {vx} + {vy}.')


@lc3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def lc3_calc(r, D):
    c, mx, sx, my, sy = rnp(r)
    sx_, sy_ = f'X ~ N({mx}, {sx}²)', f'Y ~ N({my}, {sy}²)'
    stem = f'{cap(c[0])} is X {c[1]} and {c[4]} is Y {c[5]}, where {sx_} and {sy_} independently.'
    if D <= 2:
        k = mx + my + r.choice([-2, -1, 1, 2]) * r.randint(1, 2) * max(1, int(math.sqrt(sx * sx + sy * sy)))
        s = math.sqrt(sx * sx + sy * sy)
        z = (k - mx - my) / s
        v = 1 - Phi(z)
        return Q(stem + f' Find P(X + Y > {k}).', n3(v), f'B1 N({mx + my}, {sx * sx + sy * sy}); M1 ({k} − {mx + my})/√{sx * sx + sy * sy} = {z3(z)}; A1 {n3(v)}')
    if D == 3:
        s = math.sqrt(sx * sx + sy * sy)
        if c[8]:
            d = mx - my
            z = -d / s
            v = 1 - Phi(z)
            return Q(stem + ' Find the probability that X is greater than Y.', n3(v), f'B1 X − Y ~ N({d}, {sx * sx + sy * sy}); M1 P(X − Y > 0): z = {z3(z)}; A1 {n3(v)}')
        a = mx + my - r.randint(1, 3) * int(s)
        b = mx + my + r.randint(1, 3) * int(s)
        v = Phi((b - mx - my) / s) - Phi((a - mx - my) / s)
        return Q(stem + f' Find P({a} < X + Y < {b}).', n3(v), f'B1 X + Y ~ N({mx + my}, {sx * sx + sy * sy}); M1 standardise both: {z3((a - mx - my) / s)}, {z3((b - mx - my) / s)}; A1 {n3(v)}')
    n = r.randint(2, 6)
    if D == 4:
        mt = n * mx + my
        vt = n * sx * sx + sy * sy
        k = mt + r.choice([-1, 1]) * r.randint(1, 2) * int(math.sqrt(vt))
        z = (k - mt) / math.sqrt(vt)
        v = Phi(z)
        return Q(stem + f' Find the probability that the total of {n} independent values of X and one value of Y is less than {k}.', n3(v),
                 f'B1 mean {mt}; B1 variance {n} × {sx * sx} + {sy * sy} = {vt}; M1 z = {z3(z)}; A1 {n3(v)}')
    a = r.choice([2, 3])
    md = a * mx - n * my
    vd = a * a * sx * sx + n * sy * sy
    z = -md / math.sqrt(vd)
    v = 1 - Phi(z)
    return Q(stem + f' Find the probability that {a}X is greater than the sum of {n} independent values of Y.', n3(v),
             f'M1 {a}X − (Y₁ + … + Y{n}); B1 mean {md}; B1 variance {a}² × {sx * sx} + {n} × {sy * sy} = {vd}; M1 z = {z3(z)}; A1 {n3(v)}')


@lc3.add('C2', (2, 3, 4), 'explain')
def lc3_err(r, D):
    c, mx, sx, my, sy = rnp(r)
    nm = person(r)
    n = r.randint(3, 5)
    return Q(f'{cap(c[0])} is X {c[1]}, where X ~ N({mx}, {sx}²). {nm} says the total of {n} independent values of X has distribution N({n * mx}, {n * n * sx * sx}). Explain the error and give the correct distribution.',
             f'The variance of the sum of {n} independent values is {n} × {sx * sx} = {n * sx * sx}, not {n}² × {sx * sx} (which is for {n}X). Correct: N({n * mx}, {n * sx * sx}).', f'B1 independent observations, not {n}X; B1 N({n * mx}, {n * sx * sx})')


def lc3_c4(r, D):
    c, mx, sx, my, sy = rnp(r)
    n = r.randint(3, 6)
    cap_ = n * mx + my + r.randint(1, 2) * int(math.sqrt(n * sx * sx + sy * sy) + 1)
    z1 = (cap_ - n * mx - my) / math.sqrt(n * sx * sx + sy * sy)
    s = math.sqrt(sx * sx + sy * sy)
    d = mx - my
    intro = f'{cap(c[0])} is X {c[1]}, with X ~ N({mx}, {sx}²); {c[4]} is Y {c[5]}, with Y ~ N({my}, {sy}²). All values are independent.'
    parts = [
        P('Find the probability that a randomly chosen value of X is greater than a randomly chosen value of Y.', n3(1 - Phi(-d / s)), f'B1 X − Y ~ N({d}, {sx * sx + sy * sy}); M1 z = {z3(-d / s)}; A1 {n3(1 - Phi(-d / s))}') if c[8] else (lambda r: None),
        P(f'Find the probability that the total of {n} values of X and one value of Y exceeds {cap_}.', n3(1 - Phi(z1)), f'B1 mean {n * mx + my}; B1 variance {n * sx * sx + sy * sy}; M1 z = {z3(z1)}; A1 {n3(1 - Phi(z1))}'),
        P(f'Find the probability that 2X differs from X₁ + X₂ by more than {sx}, where X, X₁ and X₂ are independent values.', n3(2 * (1 - Phi(sx / math.sqrt(6 * sx * sx)))),
          f'M1 2X − (X₁ + X₂) ~ N(0, 4 × {sx * sx} + 2 × {sx * sx} = {6 * sx * sx}); M1 2 × P(Z > {z3(sx / math.sqrt(6 * sx * sx))}); A1 {n3(2 * (1 - Phi(sx / math.sqrt(6 * sx * sx))))}'),
    ]
    return cmp_(r, intro, parts)


lc3.add('C4', (2, 3, 4, 5))(lc3_c4)


lc4 = T('Sums of independent Poisson variables', 'sums of independent poisson variables', 'poisson variables')
lc4.fixed('C1', (1, 2), [
    ('X ~ Po(2) and Y ~ Po(3) are independent. The distribution of X + Y is', 'Po(5)', 'Sum of independent Poisson variables is Poisson with λ = 2 + 3. [1]', ['Po(6)', 'Po(2.5)', 'N(5, 5)']),
    ('X ~ Po(4) and Y ~ Po(1) are independent. Which statement about X − Y is true?', 'It does not have a Poisson distribution', 'X − Y can be negative; its variance 5 ≠ mean 3. [1]', ['X − Y ~ Po(3)', 'X − Y ~ Po(5)', 'X − Y ~ Po(4)']),
    ('The number of red cars passing in a minute is Po(1.5) and of blue cars Po(0.8), independently. The number of red or blue cars in a minute is', 'Po(2.3)', '[1]', ['Po(0.7)', 'Po(1.2)', 'Po(1.15)']),
])
lc4.fixed('C2', (2, 3), [
    ('Explain why X − Y cannot have a Poisson distribution when X and Y are independent Poisson variables.', 'X − Y can take negative values, which is impossible for a Poisson variable; also its variance (λ + μ) is not equal to its mean (λ − μ).', 'B1 negative values; B1 mean ≠ variance [2]'),
])

PSUM = [('incoming calls', 'outgoing calls', 'a hospital switchboard', '10 minutes'), ('cars', 'lorries', 'a road junction', '5 minutes'), ('emails from customers', 'emails from staff', 'an office', 'an hour'),
        ('flaws of type A', 'flaws of type B', 'a 1 m length of cable', None), ('adult visitors', 'child visitors', 'a museum shop', '10 minutes'), ('red admirals', 'peacock butterflies', 'a garden', '15 minutes')]


@lc4.add('C3', (1, 2, 3, 4, 5), 'numerical')
def lc4_calc(r, D):
    a_, b_, where, per = r.choice(PSUM)
    la = r.choice([0.8, 1.2, 1.5, 2, 2.5, 3])
    lb = r.choice([0.4, 0.6, 1, 1.4, 1.8])
    tot = la + lb
    when = f' in {per}' if per else ''
    stem = f'The numbers of {a_} and {b_} at {where}{when} have independent distributions Po({L(la)}) and Po({L(lb)}).'
    if D == 1:
        k = r.randint(1, 4)
        v = ppmf(tot, k)
        return Q(stem + f' Find the probability that the total number is exactly {k}.', n3(v), f'B1 Po({L(tot)}); M1 {ex(tot, k)}; A1 {n3(v)}')
    if D == 2:
        k = r.randint(2, 4)
        v = pcdf(tot, k)
        return Q(stem + f' Find the probability that the total number is at most {k}.', n3(v), f'B1 Po({L(tot)}); M1 {terms(tot, range(k + 1))}; A1 {n3(v)}')
    if D == 3:
        m = r.choice([2, 3, 4])
        t2 = tot * m
        k = max(2, int(t2) - r.randint(0, 2))
        v = 1 - pcdf(t2, k - 1)
        return Q(stem + f' Find the probability that the total number in {m} such periods is at least {k}.', n3(v), f'B1 Po({L(t2)}); M1 1 − P(T ≤ {k - 1}); A1 {n3(v)}')
    n = r.randint(2, 5)
    j = r.randint(0, n)
    p = la / tot
    v = bpmf(n, p, j)
    direct = ppmf(la, j) * ppmf(lb, n - j) / ppmf(tot, n)
    if not ok(v, direct, 'lc4 cond'):
        return None
    if D == 4:
        return Q(stem + f' Given that the total number is {n}, find the probability that exactly {j} are {a_}.', n3(v),
                 f'M1 P(X = {j}) × P(Y = {n - j}) ÷ P(X + Y = {n}); M1 correct Poisson terms with Po({L(tot)}) in denominator; A1 {n3(v)}')
    k = r.randint(1, 2)
    v2 = (1 - pcdf(la, 0)) * pcdf(lb, k)
    return Q(stem + f' Find the probability that there is at least one of the {a_} and at most {k} of the {b_}.', n3(v2), f'M1 (1 − e^({MINUS}{L(la)})) × P(Y ≤ {k}); M1 P(Y ≤ {k}) = {n3(pcdf(lb, k))}; A1 {n3(v2)}')


@lc4.add('C2', (2, 3, 4), 'explain')
def lc4_err(r, D):
    la, lb = r.choice([2, 3, 4, 5]), r.choice([1, 1.5, 2])
    nm = person(r)
    kind = r.choice(['diff', 'mult'])
    if kind == 'diff':
        return Q(f'X ~ Po({la}) and Y ~ Po({num(lb)}) are independent. {nm} says that X − Y ~ Po({L(la - lb)}). Explain why this is wrong.',
                 f'X − Y can be negative, which a Poisson variable cannot; and Var(X − Y) = {L(la + lb)} ≠ E(X − Y) = {L(la - lb)}.', 'B1 negative values possible; B1 variance ≠ mean')
    m = r.randint(2, 4)
    return Q(f'X ~ Po({la}). {nm} says that {m}X ~ Po({m * la}). Explain why this is wrong.',
             f'{m}X takes only multiples of {m}, and Var({m}X) = {m * m * la} ≠ E({m}X) = {m * la}; it is X₁ + … + X{SUBN(m)} (independent) that is Po({m * la}).', f'B1 only multiples of {m} / variance ≠ mean; B1 sum of independent values is Po')


def lc4_c4(r, D):
    a_, b_, where, per = r.choice(PSUM)
    la = r.choice([1.2, 1.5, 2, 2.5])
    lb = r.choice([0.5, 0.8, 1, 1.5])
    tot = la + lb
    n = r.randint(3, 5)
    m = r.choice([6, 8, 10])
    when = f' in {per}' if per else ''
    big = tot * m
    k = int(big) + r.randint(2, 5)
    z = (k - 0.5 - big) / math.sqrt(big)
    intro = f'The numbers of {a_} and {b_} at {where}{when} have independent distributions Po({L(la)}) and Po({L(lb)}).'
    parts = [
        P('Find the probability that the total number is exactly 3.', n3(ppmf(tot, 3)), f'B1 Po({L(tot)}); M1 {ex(tot, 3)}; A1 {n3(ppmf(tot, 3))}'),
        P(f'Given that the total is {n}, find the probability that all {n} are {a_}.', n3((la / tot) ** n), f'M1 P(X = {n})P(Y = 0) ÷ P(T = {n}); A1 {n3((la / tot) ** n)}'),
        P(f'Use a suitable approximation to find the probability that the total in {m} such periods is at least {k}.', n3(1 - Phi(z)), f'B1 Po({L(big)}) ≈ N({L(big)}, {L(big)}); M1 continuity correction {num(k - 0.5)}; M1 z = {z3(z)}; A1 {n3(1 - Phi(z))}'),
    ]
    return cmp_(r, intro, parts, k=(2, 3))


lc4.add('C4', (2, 3, 4, 5))(lc4_c4)

CHAPTERS[2] = [lc1, lc2, lc3, lc4]


# ================================================================ Chapter 3: Continuous random variables

def simpson(f, a, b, n=4000):
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(a + i * h)
    return s * h / 3


class Pdf:
    """f(x) = k × Σ c_p x^p on [lo, hi]; coefs {p: Fraction}."""

    def __init__(self, expr, coefs, lo, hi):
        self.expr, self.c, self.lo, self.hi = expr, {p: Fr(v) for p, v in coefs.items()}, Fr(lo), Fr(hi)
        tot = self._int(self.c, self.lo, self.hi)
        self.k = 1 / tot

    @staticmethod
    def _int(c, a, b):
        s = Fr(0)
        for p, v in c.items():
            if p == -1:
                raise ValueError
            s += v * (Fr(b) ** (p + 1) - Fr(a) ** (p + 1)) / (p + 1)
        return s

    def f(self, x):
        return float(self.k) * sum(float(v) * x ** p for p, v in self.c.items())

    def prob(self, a, b):
        a, b = max(Fr(a), self.lo), min(Fr(b), self.hi)
        if b <= a:
            return Fr(0)
        return self.k * self._int(self.c, a, b)

    def moment(self, m):
        c = {p + m: v for p, v in self.c.items()}
        if -1 in c:
            v = c.pop(-1)
            return float(self.k * self._int(c, self.lo, self.hi)) + float(self.k * v) * (math.log(self.hi) - math.log(self.lo))
        return self.k * self._int(c, self.lo, self.hi)

    def mean(self):
        return self.moment(1)

    def var(self):
        m = self.mean()
        return self.moment(2) - m * m

    def quantile(self, q):
        lo, hi = float(self.lo), float(self.hi)
        for _ in range(100):
            mid = (lo + hi) / 2
            if float(self.prob(self.lo, Fr(mid).limit_denominator(10 ** 9))) < q:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2

    def check(self):
        a, b = float(self.lo), float(self.hi)
        if any(self.f(a + (b - a) * i / 50) < -1e-12 for i in range(51)):
            return False
        good = ok(simpson(self.f, a, b), 1.0, 'pdf int')
        good = good and ok(simpson(lambda x: x * self.f(x), a, b), float(self.mean()), 'pdf mean')
        good = good and ok(simpson(lambda x: x * x * self.f(x), a, b), float(self.moment(2)), 'pdf m2')
        return good


def xp(n):
    return 'x' if n == 1 else f'x{sup(n)}'


def rpdf(r, allow_log=True):
    kind = r.choice(['pow', 'pow', 'lin', 'quad', 'sq', 'shift', 'off'] + (['inv'] if allow_log else []))
    if kind == 'pow':
        n, a = r.choice([1, 2, 3]), r.choice([1, 2, 3, 4])
        return Pdf(f'k{xp(n)}', {n: 1}, 0, a)
    if kind == 'lin':
        a = r.choice([2, 3, 4, 5, 6])
        return Pdf(f'k({a} − x)', {0: a, 1: -1}, 0, a)
    if kind == 'quad':
        a = r.choice([1, 2, 3, 4])
        return Pdf(f'kx({a} − x)', {1: a, 2: -1}, 0, a)
    if kind == 'sq':
        a = r.choice([1, 2, 3])
        return Pdf(f'k({a * a} − x²)', {0: a * a, 2: -1}, 0, a)
    if kind == 'shift':
        c, a = r.choice([1, 2, 3]), r.choice([1, 2, 3, 4])
        return Pdf(f'k(x + {c})', {1: 1, 0: c}, 0, a)
    if kind == 'off':
        n, lo, hi = r.choice([(1, 1, 3), (1, 2, 4), (2, 1, 2), (2, 1, 3), (1, 1, 5), (3, 1, 2)])
        return Pdf(f'k{xp(n)}', {n: 1}, lo, hi)
    a = r.choice([2, 3, 4, 5])
    return Pdf('k/x²', {-2: 1}, 1, a)


def pdf_stem(P_):
    return (f'The continuous random variable X has probability density function given by f(x) = {P_.expr} for {num(P_.lo)} ≤ x ≤ {num(P_.hi)}, and f(x) = 0 otherwise, '
            'where k is a constant.')


def ex_(v):
    """Exact fraction, 3 s.f. decimal if the fraction is unwieldy."""
    if isinstance(v, Fr):
        return num(v) if v.denominator <= 2000 else n3(float(v))
    return n3(v)


def interior(r, P_):
    lo, hi = P_.lo, P_.hi
    w = hi - lo
    cands = sorted({lo + w * Fr(i, 4) for i in (1, 2, 3)} | {lo + w * Fr(i, 3) for i in (1, 2)} | {Fr(x) for x in range(int(lo) + 1, int(hi))})
    cands = [c for c in cands if lo < c < hi]
    return r.choice(cands)


crv1 = T('Probability density functions and calculating probabilities by integration', 'probability density functions', 'calculating probabilities by integration')
crv1.fixed('C1', (1, 2), [
    ('For a continuous random variable X, P(X = 2) =', '0', 'Probability is area; a single point has zero width. [1]', ['f(2)', '1/2', '1 − f(2)']),
    ('Which condition must a probability density function f satisfy?', 'The total area under the graph of f is 1', 'Also f(x) ≥ 0 for all x. [1]', ['f(x) ≤ 1 for all x', 'f has a maximum value of 1', 'f(0) = 0']),
    ('For a continuous random variable, P(a < X < b) is found by', 'integrating f(x) from a to b', 'Area under the pdf between a and b. [1]', ['evaluating f(b) − f(a)', 'evaluating f(b)', 'differentiating f(x)']),
    ('A pdf has f(x) = k for 0 ≤ x ≤ 5 and 0 otherwise. k =', '0.2', 'Area of rectangle 5k = 1. [1]', ['5', '1', '0.5']),
])
crv1.fixed('C2', (2, 3), [
    ('Explain why P(X < 3) = P(X ≤ 3) for a continuous random variable X.', 'X is continuous, so P(X = 3) = 0; including the end point adds no probability.', 'B1 P(X = 3) = 0; B1 continuous [2]'),
    ('Explain why a probability density function can take values greater than 1.', 'Probabilities are given by areas, not by the height of f; a tall, narrow region can still have area at most 1.', 'B1 probability = area; B1 height can exceed 1 if width small [2]'),
])


@crv1.add('C1', (1, 2, 3))
def crv1_c1(r, D):
    P_ = rpdf(r, allow_log=False)
    if not P_.check():
        return None
    return MCk(r, pdf_stem(P_) + ' Find the value of k.', num(P_.k), [num(1 / P_.k), num(P_.k * 2), num(P_.k / 2), num(1 / P_.hi) if num(1 / P_.hi) != num(P_.k) else num(P_.k * 3)],
               f'∫ from {num(P_.lo)} to {num(P_.hi)} of f(x) dx = 1 gives k = {num(P_.k)}.')


@crv1.add('C2', (2, 3, 4), 'explain')
def crv1_valid(r, D):
    kind = r.choice(['neg', 'err_k', 'err_area'])
    nm = person(r)
    if kind == 'neg':
        a = r.choice([2, 3, 4])
        b = a + r.choice([1, 2, 3])
        return Q(f'{nm} says that f(x) = k(x − {a}) for 0 ≤ x ≤ {b}, and f(x) = 0 otherwise, is a probability density function for a suitable positive constant k. Explain why this is impossible.',
                 f'For 0 ≤ x < {a}, x − {a} < 0, so f(x) < 0 for positive k; a pdf can never be negative.', 'B1 f(x) < 0 for 0 ≤ x < ' + str(a) + '; B1 pdf must be non-negative')
    P_ = rpdf(r, allow_log=False)
    if not P_.check():
        return None
    if kind == 'err_k':
        return Q(pdf_stem(P_) + f' {nm} finds k by solving f({num(P_.hi)}) = 1. Explain the error and find the correct value of k.',
                 f'The condition is that the total area is 1: ∫ f(x) dx over [{num(P_.lo)}, {num(P_.hi)}] = 1, giving k = {num(P_.k)}.', f'B1 area under f equals 1; M1 integrates and sets equal to 1; A1 k = {num(P_.k)}')
    b = interior(r, P_)
    pv = P_.prob(P_.lo, b)
    wrong = P_.k * sum(float(v) * float(b) ** p for p, v in P_.c.items())
    return Q(pdf_stem(P_) + f' It is given that k = {num(P_.k)}. {nm} says that P(X < {num(b)}) = f({num(b)}) = {n3(float(wrong))}. Explain the error and find P(X < {num(b)}).',
             f'f({num(b)}) is the height of the density, not a probability; P(X < {num(b)}) = ∫ from {num(P_.lo)} to {num(b)} of f(x) dx = {ex_(pv)}.', f'B1 probability is the area / integral; M1 integrates from {num(P_.lo)} to {num(b)}; A1 {ex_(pv)}')


@crv1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def crv1_calc(r, D):
    P_ = rpdf(r)
    if not P_.check():
        return None
    stem = pdf_stem(P_)
    if D == 1:
        return Q(stem + ' Find the value of k.', num(P_.k), f'M1 integrates f and sets total = 1; A1 k = {num(P_.k)}')
    b = interior(r, P_)
    if D == 2:
        pv = P_.prob(P_.lo, b)
        return Q(stem + f' Show that k = {num(P_.k)} and find P(X < {num(b)}).', ex_(pv), f'M1 ∫ f(x) dx = 1; A1 k = {num(P_.k)} shown; M1 ∫ from {num(P_.lo)} to {num(b)}; A1 {ex_(pv)}')
    if D == 3:
        c = interior(r, P_)
        a_, b_ = sorted([b, c])
        if a_ == b_:
            a_ = P_.lo + (P_.hi - P_.lo) / 4
            b_ = P_.lo + 3 * (P_.hi - P_.lo) / 4
        pv = P_.prob(a_, b_)
        return Q(stem + f' Find the value of k and hence find P({num(a_)} < X < {num(b_)}).', f'k = {num(P_.k)}; {ex_(pv)}', f'M1 total area 1; A1 k = {num(P_.k)}; M1 ∫ from {num(a_)} to {num(b_)}; A1 {ex_(pv)}')
    if D == 4:
        pv = P_.prob(b, P_.hi)
        n = r.choice([3, 4, 5])
        v = 1 - (1 - float(pv)) ** n
        return Q(stem + f' Find k. {n} independent values of X are taken. Find the probability that at least one of them is greater than {num(b)}.',
                 f'k = {num(P_.k)}; {n3(v)}', f'M1 total area 1; A1 k = {num(P_.k)}; M1 P(X > {num(b)}) = {ex_(pv)}; M1 1 − (1 − {ex_(pv)}){sup(n)}; A1 {n3(v)}')
    # D5: find a such that P(X < a) = given exact
    q = r.choice([Fr(1, 4), Fr(1, 2), Fr(3, 4), Fr(1, 10), Fr(9, 10)])
    a = P_.quantile(float(q))
    if not ok(float(P_.prob(P_.lo, Fr(a).limit_denominator(10 ** 8))), float(q), 'crv q', 1e-5):
        return None
    return Q(stem + f' Find k and the value of a such that P(X < a) = {num(q)}.', f'k = {num(P_.k)}; a = {n3(a)}', f'M1 total area 1; A1 k = {num(P_.k)}; M1 ∫ from {num(P_.lo)} to a of f(x) dx = {num(q)}; M1 solves for a; A1 a = {n3(a)}')


def crv1_c4(r, D):
    P_ = rpdf(r, allow_log=False)
    if not P_.check():
        return None
    b = interior(r, P_)
    pv = P_.prob(b, P_.hi)
    n = r.choice([3, 4, 5])
    j = r.randint(1, n - 1)
    pb = bpmf(n, float(pv), j)
    intro = pdf_stem(P_)
    parts = [
        P('Show that k = ' + num(P_.k) + '.', f'k = {num(P_.k)}', 'M1 ∫ f(x) dx = 1; A1 k shown'),
        P(f'Find P(X > {num(b)}).', ex_(pv), f'M1 ∫ from {num(b)} to {num(P_.hi)}; A1 {ex_(pv)}'),
        P(f'{n} independent observations of X are taken. Find the probability that exactly {j} of them are greater than {num(b)}.', n3(pb), f'M1 B({n}, {ex_(pv)}); M1 {n}C{j} p{sup(j)}(1 − p){sup(n - j)}; A1 {n3(pb)}'),
        P(f'Find P(X < {num(b)} | X < {num((b + P_.hi) / 2)}).', ex_(P_.prob(P_.lo, b) / P_.prob(P_.lo, (b + P_.hi) / 2)),
          f'M1 P(X < {num(b)}) ÷ P(X < {num((b + P_.hi) / 2)}); A1 {ex_(P_.prob(P_.lo, b) / P_.prob(P_.lo, (b + P_.hi) / 2))}'),
    ]
    return cmp_(r, intro, parts)


crv1.add('C4', (2, 3, 4, 5))(crv1_c4)


crv2 = T('Mean and variance of a continuous random variable', 'mean and variance of a continuous random variable')
crv2.fixed('C1', (1, 2), [
    ('For a continuous random variable with pdf f on [a, b], E(X) =', '∫ₐᵇ x f(x) dx', 'Definition of the mean. [1]', ['∫ₐᵇ f(x) dx', '∫ₐᵇ x² f(x) dx', 'f((a + b)/2)']),
    ('Var(X) for a continuous random variable is', 'E(X²) − [E(X)]²', '∫x²f(x) dx − μ². [1]', ['E(X²)', '[E(X)]² − E(X²)', '∫(x − μ) f(x) dx']),
    ('X has pdf f(x) = 1/4 for 0 ≤ x ≤ 4. E(X) =', '2', 'Symmetric about x = 2. [1]', ['1/4', '4', '1']),
])
crv2.fixed('C2', (2, 3), [
    ('Explain how the symmetry of a pdf can be used to write down E(X).', 'If the graph of f is symmetrical about x = c, then values equally above and below c are equally likely, so E(X) = c (and the median is also c).', 'B1 symmetrical about c; B1 E(X) = c [2]'),
])


@crv2.add('C1', (1, 2, 3))
def crv2_c1(r, D):
    kind = r.choice(['sym', 'pow'])
    if kind == 'sym':
        a = r.choice([2, 4, 6, 8])
        P_ = Pdf(f'kx({a} − x)', {1: a, 2: -1}, 0, a)
        return MCk(r, pdf_stem(P_) + ' Write down E(X).', num(Fr(a, 2)), [num(P_.k), num(a), num(Fr(a, 3)), num(Fr(2 * a, 3))], f'f is symmetrical about x = {num(Fr(a, 2))}, so E(X) = {num(Fr(a, 2))}.')
    n, a = r.choice([1, 2, 3]), r.choice([1, 2, 3, 4, 5])
    P_ = Pdf(f'k{xp(n)}', {n: 1}, 0, a)
    m = P_.mean()
    return MCk(r, pdf_stem(P_) + f' Given that k = {num(P_.k)}, find E(X).', num(m), [num(Fr(a, 2)), num(m * Fr(n + 1, n + 2)) if m * Fr(n + 1, n + 2) != m else num(m + 1), num(P_.moment(2)), num(Fr(a * n, n + 2) + 1)],
               f'E(X) = ∫ x f(x) dx = {num(m)}.')


@crv2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def crv2_calc(r, D):
    P_ = rpdf(r)
    if not P_.check():
        return None
    m, v = P_.mean(), P_.var()
    stem = pdf_stem(P_) + f' It is given that k = {num(P_.k)}.'
    if D <= 2:
        return Q(stem + ' Find E(X).', ex_(m), f'M1 ∫ x f(x) dx; M1 correct integration; A1 {ex_(m)}')
    if D == 3:
        return Q(stem + ' Find E(X) and Var(X).', f'E(X) = {ex_(m)}, Var(X) = {ex_(v)}', f'M1 ∫ x f(x) dx; A1 {ex_(m)}; M1 ∫ x² f(x) dx − [E(X)]²; A1 {ex_(v)}')
    s = math.sqrt(float(v))
    mu = float(m)
    pv = float(P_.prob(max(P_.lo, Fr(mu - s).limit_denominator(10 ** 6)), min(P_.hi, Fr(mu + s).limit_denominator(10 ** 6))))
    if not ok(pv, simpson(P_.f, max(float(P_.lo), mu - s), min(float(P_.hi), mu + s)), 'crv2 within', 1e-5):
        return None
    if D == 4:
        return Q(stem + ' Find the standard deviation of X, and find the probability that X lies within one standard deviation of its mean.', f'σ = {n3(s)}; {n3(pv)}',
                 f'M1 E(X) = {ex_(m)}; M1 Var(X) = {ex_(v)}; A1 σ = {n3(s)}; M1 ∫ from {n3(mu - s)} to {n3(mu + s)}; A1 {n3(pv)}')
    a, b = r.choice([2, 3, 5]), r.choice([1, 4, 10])
    return Q(stem + f' Y = {a}X + {b}. Find E(Y) and Var(Y).', f'E(Y) = {ex_(a * m + b)}, Var(Y) = {ex_(a * a * v)}', f'M1 E(X) = {ex_(m)}; M1 Var(X) = {ex_(v)}; A1 E(Y); A1 Var(Y) = {a}² Var(X)')


@crv2.add('C2', (2, 3, 4), 'explain')
def crv2_err(r, D):
    P_ = rpdf(r, allow_log=False)
    if not P_.check():
        return None
    m, v = P_.mean(), P_.var()
    nm = person(r)
    wrong = P_.moment(2)
    return Q(pdf_stem(P_) + f' It is given that k = {num(P_.k)}. {nm} states that Var(X) = ∫ x² f(x) dx = {ex_(wrong)}. Explain the error and find Var(X).',
             f'The square of the mean must be subtracted: Var(X) = {ex_(wrong)} − ({ex_(m)})² = {ex_(v)}.', f'B1 subtract [E(X)]²; M1 E(X) = {ex_(m)}; A1 {ex_(v)}')


def crv2_c4(r, D):
    P_ = rpdf(r, allow_log=False)
    if not P_.check():
        return None
    m, v = P_.mean(), P_.var()
    med = P_.quantile(0.5)
    pm = P_.prob(Fr(m), P_.hi)
    intro = pdf_stem(P_)
    parts = [
        P('Find the value of k.', num(P_.k), f'M1 total area 1; A1 {num(P_.k)}'),
        P('Find E(X).', ex_(m), f'M1 ∫ x f(x) dx; A1 {ex_(m)}'),
        P('Find Var(X).', ex_(v), f'M1 ∫ x² f(x) dx − [E(X)]²; A1 {ex_(v)}'),
        P('Find the probability that X is greater than its mean.', ex_(pm), f'M1 ∫ from {ex_(m)} to {num(P_.hi)}; A1 {ex_(pm)}'),
        P('Find the median of X and state, with a reason, whether the distribution is positively or negatively skewed.',
          f'median {n3(med)}; ' + ('mean < median, so negatively skewed' if float(m) < med - 1e-9 else 'mean > median, so positively skewed' if float(m) > med + 1e-9 else 'mean = median, symmetrical'),
          f'M1 ∫ to m = 0.5; A1 {n3(med)}; B1 comparison with mean'),
    ]
    return cmp_(r, intro, parts)


crv2.add('C4', (2, 3, 4, 5))(crv2_c4)


crv3 = T('Median and other percentiles of a continuous random variable', 'median and other percentiles', 'percentiles of a continuous random variable')
crv3.fixed('C1', (1, 2), [
    ('The median m of a continuous random variable with pdf f on [a, b] satisfies', '∫ₐᵐ f(x) dx = 0.5', 'Half the area lies below m. [1]', ['f(m) = 0.5', '∫ₐᵐ x f(x) dx = 0.5', 'f′(m) = 0']),
    ('The upper quartile q of X satisfies', 'P(X < q) = 0.75', '[1]', ['P(X < q) = 0.25', 'f(q) = 0.75', 'P(X > q) = 0.75']),
    ('For a pdf that is symmetrical about x = 3, the median is', '3', 'Symmetry. [1]', ['1.5', '0.5', '6']),
])
crv3.fixed('C2', (2, 3), [
    ('Explain how you can tell from the shape of a pdf whether the median is less than the mean.', 'If the pdf has a long tail to the right (positive skew), the mean is pulled above the median, so the median is less than the mean.', 'B1 positive skew / long right tail; B1 mean pulled towards the tail [2]'),
])


@crv3.add('C1', (1, 2, 3))
def crv3_c1(r, D):
    n, a = r.choice([1, 2, 3]), r.choice([1, 2, 3, 4])
    P_ = Pdf(f'k{xp(n)}', {n: 1}, 0, a)
    q = r.choice([Fr(1, 2), Fr(1, 4), Fr(3, 4)])
    val = float(a) * float(q) ** (1 / (n + 1))
    nm = {Fr(1, 2): 'median', Fr(1, 4): 'lower quartile', Fr(3, 4): 'upper quartile'}[q]
    return MCk(r, pdf_stem(P_) + f' Given that k = {num(P_.k)}, find the {nm} of X, correct to 3 significant figures.', n3(val),
               [n3(float(a) * float(q)), n3(float(a) * float(q) ** (1 / n)) if n > 1 else n3(float(a) * float(q) ** 0.25), n3(float(a) * (1 - float(q)) ** (1 / (n + 1))), n3(float(P_.mean()))],
               f'(m/{a}){sup(n + 1)} = {num(q)} ⇒ m = {a} × {num(q)}^(1/{n + 1}) = {n3(val)}.')


@crv3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def crv3_calc(r, D):
    P_ = rpdf(r)
    if not P_.check():
        return None
    stem = pdf_stem(P_) + f' It is given that k = {num(P_.k)}.'
    med = P_.quantile(0.5)
    if not ok(float(P_.prob(P_.lo, Fr(med).limit_denominator(10 ** 9))), 0.5, 'median', 1e-6):
        return None
    if D <= 2:
        return Q(stem + ' Find the median of X.', n3(med), f'M1 ∫ from {num(P_.lo)} to m of f(x) dx = 0.5; M1 solves equation in m; A1 {n3(med)}')
    if D == 3:
        q1, q3 = P_.quantile(0.25), P_.quantile(0.75)
        return Q(stem + ' Find the interquartile range of X.', n3(q3 - q1), f'M1 ∫ to q₁ = 0.25 gives q₁ = {n3(q1)}; M1 ∫ to q₃ = 0.75 gives q₃ = {n3(q3)}; A1 IQR {n3(q3 - q1)}')
    pc_ = r.choice([10, 20, 80, 90, 95])
    v = P_.quantile(pc_ / 100)
    if D == 4:
        return Q(stem + f' Find the {pc_}th percentile of X.', n3(v), f'M1 ∫ from {num(P_.lo)} to p of f(x) dx = {num(Fr(pc_, 100))}; M1 solve; A1 {n3(v)}')
    m = P_.mean()
    return Q(stem + ' Find the median of X and the mean of X, and hence comment on the skewness of the distribution.',
             f'median {n3(med)}, mean {ex_(m)}; ' + ('mean < median, so negatively skewed.' if float(m) < med - 1e-9 else 'mean > median, so positively skewed.' if float(m) > med + 1e-9 else 'symmetrical.'),
             f'M1 median equation; A1 {n3(med)}; M1 ∫ x f(x) dx; A1 {ex_(m)}; B1 skewness comment')


@crv3.add('C2', (2, 3, 4), 'explain')
def crv3_err(r, D):
    n, a = r.choice([1, 2, 3]), r.choice([2, 3, 4])
    P_ = Pdf(f'k{xp(n)}', {n: 1}, 0, a)
    nm = person(r)
    med = float(a) * 0.5 ** (1 / (n + 1))
    k = P_.k
    wrong = (0.5 / float(k)) ** (1 / n)
    return Q(pdf_stem(P_) + f' It is given that k = {num(k)}. {nm} finds the median by solving f(m) = 0.5, obtaining m = {n3(wrong)}. Explain the error and find the median.',
             f'The median satisfies P(X < m) = 0.5, i.e. the area ∫₀ᵐ f(x) dx = 0.5, not f(m) = 0.5. m = {a} × 0.5^(1/{n + 1}) = {n3(med)}.', f'B1 area condition; M1 ∫₀ᵐ {num(k)}{xp(n)} dx = 0.5; A1 {n3(med)}')


def crv3_c4(r, D):
    P_ = rpdf(r, allow_log=False)
    if not P_.check():
        return None
    med = P_.quantile(0.5)
    q1, q3 = P_.quantile(0.25), P_.quantile(0.75)
    m = P_.mean()
    ctx = r.choice(['the time, in hours, that a patient waits in a clinic', 'the distance, in km, that a delivery van travels between stops', 'the mass, in kg, of sand in a bag',
                    'the lifetime, in years, of a component'])
    intro = f'X represents {ctx}. ' + pdf_stem(P_)
    parts = [
        P('Find k.', num(P_.k), f'M1 total area 1; A1 {num(P_.k)}'),
        P('Find the median of X.', n3(med), f'M1 ∫ to m = 0.5; A1 {n3(med)}'),
        P('Find the interquartile range of X.', n3(q3 - q1), f'M1 quartile equations; A1 q₁ = {n3(q1)}; A1 q₃ = {n3(q3)}, IQR {n3(q3 - q1)}'),
        P('Find E(X).', ex_(m), f'M1 ∫ x f(x) dx; A1 {ex_(m)}'),
        P(f'Find the probability that two independent values of X are both less than the median.', '0.25', 'B1 0.5² = 0.25'),
    ]
    return cmp_(r, intro, parts)


crv3.add('C4', (2, 3, 4, 5))(crv3_c4)

CHAPTERS[3] = [crv1, crv2, crv3]


# ================================================================ Chapter 4: Sampling

# (population, variable, biased method, why biased, better method)
SURVEYS = [
    ('all students at a large school in {c}', 'the mean time spent on homework each night', 'asks the first 40 students arriving at the library',
     'students who use the library are likely to spend more time on homework than others', 'number all students on the school register and use random numbers to choose 40'),
    ('adults living in a town', 'opinions about a new bus service', 'interviews people waiting at a bus stop on a weekday morning',
     'people at a bus stop already use buses, and those at work or who drive are excluded', 'choose people at random from the electoral register'),
    ('all employees of a company', 'satisfaction with working hours', 'emails a questionnaire and uses the first 50 replies',
     'people with strong opinions or more free time are more likely to reply (self-selection / non-response bias)', 'select 50 employees at random from a staff list and follow up non-responses'),
    ('the trees in a forest', 'the mean height', 'measures the 30 trees nearest the car park',
     'trees near the car park may differ (e.g. more light, more disturbance) from those in the rest of the forest', 'use random coordinates on a grid over the forest map to choose trees'),
    ('the households in a small town', 'monthly spending on electricity', 'telephones households listed in an old telephone directory',
     'the directory omits households without landlines or that have moved recently, so the sampling frame is incomplete', 'use an up-to-date list of addresses as the sampling frame and select at random'),
    ('shoppers at a shopping centre', 'the amount spent per visit', 'asks every shopper leaving one expensive department store',
     'shoppers at one expensive store are not representative of all shoppers', 'question shoppers at randomly chosen times and at all exits'),
    ('the fish in a lake', 'the mean length', 'uses a net with large mesh',
     'small fish escape through the mesh, so the sample overestimates the mean length', 'use nets with a range of mesh sizes at randomly chosen locations'),
    ('the voters in a town', 'support for a political party', 'surveys followers of the party’s social media account',
     'followers are likely to support the party, so support is overestimated', 'use a random sample from the electoral register'),
]


# population units and plausible sizes for items that number a sampling frame (shoppers have no list)
SURVEY_N = {'the mean time spent on homework each night': ('students', [850, 1200, 1500]), 'opinions about a new bus service': ('adults', [2400, 3600, 5800]),
            'satisfaction with working hours': ('employees', [400, 600, 850]), 'the mean height': ('trees', [400, 600, 850, 1200]),
            'monthly spending on electricity': ('households', [850, 1200, 2400]), 'the mean length': ('fish', [400, 600, 850]),
            'support for a political party': ('voters', [2400, 3600, 5800])}


def _sv(r, listed=False):
    s = list(r.choice([x for x in SURVEYS if not listed or x[1] in SURVEY_N]))
    s[0] = s[0].format(c=city(r))
    return s


sam1 = T('Populations, samples, random sampling and sources of bias', 'populations, samples', 'random sampling', 'sources of bias')
sam1.fixed('C1', (1, 2), [
    ('A list of all the members of a population from which a sample is chosen is called', 'a sampling frame', '[1]', ['a census', 'a statistic', 'a parameter']),
    ('A census is', 'a survey of every member of the population', '[1]', ['a random sample of 10% of the population', 'a list of sampling units', 'a biased sample']),
    ('In a random sample', 'every possible sample of the given size has an equal chance of being chosen', 'Each member is equally likely and selections are independent. [1]', ['the sample is chosen by the researcher for convenience', 'every tenth member is chosen', 'only volunteers take part']),
    ('A quantity calculated from a sample, such as the sample mean, is called', 'a statistic', 'A population value is a parameter. [1]', ['a parameter', 'a sampling frame', 'a census']),
    ('Which is a reason for using a sample rather than a census?', 'Testing may destroy the items, e.g. testing the lifetime of light bulbs', '[1]', ['A sample always gives exact population values', 'A census is never possible', 'A sample has no sampling error']),
])
sam1.fixed('C2', (2, 3), [
    ('Give two advantages of taking a sample rather than a census.', 'A sample is cheaper and quicker; it is the only option if testing is destructive; with a large population a census may be impractical.', 'B1 B1 two valid advantages [2]'),
    ('Explain what is meant by a biased sample.', 'A sample that is not representative of the population because some members are more likely to be chosen than others, so estimates are systematically too high or too low.', 'B1 not representative; B1 systematic over/under-estimation [2]'),
    ('Explain why a large biased sample is not better than a small random sample.', 'Increasing the size of a biased sample does not remove the bias; its estimates remain systematically wrong, whereas a random sample gives unbiased estimates.', 'B1 bias does not reduce with size; B1 random sample unbiased [2]'),
])


@sam1.add('C2', (1, 2, 3, 4), 'explain')
def sam1_bias(r, D):
    pop, var, meth, why, better = _sv(r)
    nm = person(r)
    stem = f'{nm} wants to estimate {var} for {pop}. {nm} {meth}.'
    if D == 1:
        others = [s[3] for s in SURVEYS if s[3] != why]
        return MCk(r, stem + ' Why is this sample likely to be biased?', cap(why), [cap(x) for x in r.sample(others, 3)], 'The method does not give every member an equal chance of selection.')
    if D == 2:
        return Q(stem + ' Explain why this sample is likely to be biased.', cap(why) + '.', 'B1 reason in context')
    return Q(stem + ' Explain why this sample is likely to be biased and describe a better method of choosing the sample.', f'{cap(why)}. Better: {better}.', 'B1 reason for bias in context; B1 better method; B1 detail of random selection')


@sam1.add('C3', (1, 2, 3, 4, 5), 'case')
def sam1_case(r, D):
    pop, var, meth, why, better = _sv(r, listed=True)
    n = r.choice([30, 40, 50, 60, 80])
    unit, Ns = SURVEY_N[var]
    N = r.choice(Ns)
    nm = person(r)
    intro = f'{nm} wants to estimate {var} for {pop}. There are {N} {unit} in the population. {nm} {meth}.'
    parts = [
        P('Explain why this sample may be biased.', cap(why) + '.', 'B1 in context'),
        P(f'Describe how {nm} could choose a random sample of size {n}.', f'Obtain a list of all {N} members (sampling frame); number them 1 to {N}; use random numbers (calculator or tables) to choose {n} different numbers, ignoring repeats and numbers above {N}; select those members.', 'B1 list and number members; B1 random numbers; B1 ignore repeats / out-of-range'),
        P('State whether a value calculated from the sample, such as a sample mean or proportion, is a parameter or a statistic.', 'A statistic', 'B1'),
        P('Give one reason why a sample rather than a census is used.', 'A census would be time-consuming and expensive for the whole population.', 'B1'),
        P('Explain why a different random sample would probably give a different estimate.', 'Each random sample contains different members, so the estimate varies from sample to sample (sampling variability).', 'B1'),
    ]
    return cmp_(r, intro, parts, type_='case')


def sam1_c4(r, D):
    pop, var, meth, why, better = _sv(r)
    nm = person(r)
    mu = r.randint(20, 60)
    sd = r.randint(4, 12)
    n = r.choice([30, 40, 50])
    intro = f'{nm} wants to estimate {var} for {pop}. {nm} {meth}.'
    z = 2 / (sd / math.sqrt(n))
    parts = [
        P('Explain why this method may give a biased estimate.', cap(why) + '.', 'B1 reason in context'),
        P('Suggest a better method of sampling.', cap(better) + '.', 'B1 random method; B1 detail'),
        P(f'With an improved method, the variable is found to have mean {mu} and standard deviation {sd}. Find the probability that the mean of a random sample of {n} differs from {mu} by more than 2.', n3(2 * (1 - Phi(z))),
          f'B1 X̄ ~ N({mu}, {sd}²/{n}) approximately; M1 z = 2 ÷ ({sd}/√{n}) = {z3(z)}; A1 {n3(2 * (1 - Phi(z)))}'),
        P('Explain why the central limit theorem is relevant to the previous part.', f'The distribution of the variable is unknown, but n = {n} is large, so the sample mean is approximately normally distributed.', 'B1 n large; B1 X̄ approximately normal'),
    ]
    return cmp_(r, intro, parts, deps={3: [2]})


sam1.add('C4', (2, 3, 4, 5))(sam1_c4)


RAND_FRAMES = [('members of a sports club', 'membership number'), ('pupils in a year group', 'register number'), ('houses in a village', 'house number on the council list'),
               ('trees in an orchard', 'tag number'), ('patients registered at a clinic', 'patient number'), ('cars in a company fleet', 'fleet number')]


def pick_random(digits, N, k):
    w = len(str(N))
    out, used = [], []
    for i in range(0, len(digits) - w + 1, w):
        v = int(digits[i:i + w])
        if 1 <= v <= N and v not in out:
            out.append(v)
            if len(out) == k:
                break
        used.append(v)
    return out


sam2 = T('Using random numbers to select a sample', 'using random numbers to select a sample', 'random numbers')
sam2.fixed('C1', (1, 2), [
    ('Members of a population of 650 are numbered 001 to 650. Using random digits in groups of three, the group 734 should be', 'ignored, because it is greater than 650', '[1]', ['used as member 734', 'used as member 084', 'used as member 73']),
    ('When choosing a sample without replacement using random numbers, a number that has already been chosen should be', 'ignored', '[1]', ['used again', 'replaced by the next number up', 'halved']),
    ('Population members are numbered 00 to 89. How many digits should be read at a time from a random number table?', '2', '[1]', ['1', '3', '4']),
])
sam2.fixed('C2', (2, 3), [
    ('Explain why the members of a population should be numbered before using random numbers to choose a sample.', 'Numbering creates a sampling frame in which every member has a unique label, so each can be selected with equal probability by random numbers.', 'B1 unique labels; B1 equal chance of selection [2]'),
])


@sam2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def sam2_pick(r, D):
    what, lab = r.choice(RAND_FRAMES)
    N = r.choice([60, 75, 80, 90, 120, 250, 360, 480, 600, 750, 850])
    w = len(str(N))
    k = 3 if D <= 2 else 4 if D == 3 else 5
    digits = ''.join(str(r.randint(0, 9)) for _ in range(w * 14))
    sel = pick_random(digits, N, k)
    if len(sel) < k:
        return None
    # require at least one rejected group in the used portion for D >= 3
    groups = [int(digits[i:i + w]) for i in range(0, len(digits) - w + 1, w)]
    used_n = 0
    got = []
    for g in groups:
        used_n += 1
        if 1 <= g <= N and g not in got:
            got.append(g)
            if len(got) == k:
                break
    rejected = [g for g in groups[:used_n] if not (1 <= g <= N)] + [g for i, g in enumerate(groups[:used_n]) if 1 <= g <= N and g in groups[:i]]
    if D >= 3 and not rejected:
        return None
    shown = ' '.join(digits[i:i + 5] for i in range(0, len(digits), 5))
    stem = (f'The {N} {what} are numbered 1 to {N} by {lab}. Starting at the beginning of the row of random digits below and reading groups of {w} digits, '
            f'choose a random sample of {k} without replacement. Random digits: {shown}')
    key = f'B1 reads groups of {w}; B1 ignores values above {N} (and 0) and repeats; B1 {", ".join(map(str, sel))}'
    if D == 1:
        return MCk(r, stem, ', '.join(map(str, sel)), [', '.join(map(str, groups[:k])) if groups[:k] != sel else ', '.join(map(str, sel[::-1])), ', '.join(str(int(digits[i:i + w + 1])) for i in range(0, k * (w + 1), w + 1)),
                                                        ', '.join(str(int(digits[i:i + w - 1] or 0)) for i in range(0, k * max(1, w - 1), max(1, w - 1))), ', '.join(map(str, sorted(sel)[::-1]))], key)
    return Q(stem, ', '.join(map(str, sel)) + (f' (rejected: {", ".join(map(str, rejected))})' if rejected else ''), key)


@sam2.add('C2', (2, 3, 4), 'explain')
def sam2_err(r, D):
    what, lab = r.choice(RAND_FRAMES)
    N = r.choice([300, 450, 600, 800])
    nm = person(r)
    kind = r.choice(['mod', 'first'])
    if kind == 'mod':
        return Q(f'The {N} {what} are numbered 001 to {N}. {nm} reads three-digit random numbers and, when a number is greater than {N}, subtracts {N} from it and uses the result. Explain why this method is not fair.',
                 f'Numbers from 001 to {999 - N} can be obtained in two ways (directly and after subtracting {N}), so they are more likely to be chosen than numbers above {999 - N}.', 'B1 some members can arise in two ways; B1 unequal probabilities of selection')
    n = r.choice([20, 30, 40])
    return Q(f'The {N} {what} are listed in alphabetical order. {nm} chooses a sample of {n} by taking the first {n} names on the list. Explain why this is not a random sample and describe how to use random numbers to obtain one.',
             f'Members later in the list have no chance of being chosen (and names starting with certain letters may share characteristics). Number the members 001 to {N}, generate three-digit random numbers, ignoring repeats and values above {N}, until {n} are chosen.',
             'B1 not every member has a chance; B1 numbering; B1 random numbers ignoring repeats / out of range')


sam3 = T('The distribution of the sample mean and the central limit theorem', 'distribution of the sample mean', 'central limit theorem')
sam3.fixed('C1', (1, 2), [
    ('X ~ N(50, 16). The distribution of the mean of a random sample of size 4 is', 'N(50, 4)', 'Var(X̄) = σ²/n = 16/4. [1]', ['N(50, 16)', 'N(12.5, 4)', 'N(50, 1)']),
    ('The central limit theorem states that, for a large random sample from any distribution with mean μ and variance σ²,', 'X̄ is approximately N(μ, σ²/n)', '[1]', ['X is approximately normal', 'X̄ = μ exactly', 'X̄ is approximately N(μ, σ²)']),
    ('The standard deviation of the sample mean (standard error) for samples of size n is', 'σ/√n', '[1]', ['σ/n', 'σ²/n', 'σ√n']),
    ('If the population is normal, the sample mean is normally distributed', 'for any sample size', 'The CLT is only needed when the population is not normal. [1]', ['only if n ≥ 30', 'only if n is even', 'only if σ is known']),
])
sam3.fixed('C2', (2, 3), [
    ('Explain why the central limit theorem is not needed when the population is normally distributed.', 'A linear combination (including the mean) of independent normal variables is itself normal, so X̄ is exactly normal for any n.', 'B1 X̄ exactly normal; B1 for any n [2]'),
    ('Explain why the variance of the sample mean decreases as the sample size increases.', 'Var(X̄) = σ²/n; with more observations, high and low values tend to cancel, so sample means cluster more closely around μ.', 'B1 σ²/n; B1 interpretation [2]'),
])

SCTX = [('the lengths of bolts made by a machine', 'mm', (40, 120), (2, 6), True), ('the masses of apples from an orchard', 'g', (120, 180), (10, 25), False),
        ('the times taken to answer calls at a call centre', 'seconds', (30, 90), (8, 25), False), ('the heights of sunflower plants', 'cm', (150, 220), (12, 30), True),
        ('the daily sales at a café', 'dollars', (300, 800), (40, 120), False), ('the volumes of juice in cartons', 'ml', (990, 1010), (4, 9), True)]


@sam3.add('C1', (1, 2, 3))
def sam3_c1(r, D):
    c = r.choice(SCTX)
    mu, sd = r.randint(*c[2]), r.randint(*c[3])
    n = r.choice([4, 9, 16, 25, 36, 64, 100])
    v = Fr(sd * sd, n)
    return MCk(r, f'{cap(c[0])} have mean {mu} {c[1]} and standard deviation {sd} {c[1]}. State the variance of the mean of a random sample of {n}.', num(v),
               [num(Fr(sd, n)), num(Fr(sd * sd)), num(Fr(sd * sd, int(math.sqrt(n)))), num(Fr(sd, int(math.sqrt(n))))], f'σ²/n = {sd}²/{n} = {num(v)}.')


@sam3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def sam3_calc(r, D):
    c = r.choice(SCTX)
    mu, sd = r.randint(*c[2]), r.randint(*c[3])
    norm = c[4]
    n = r.choice([4, 6, 8, 10, 12]) if norm else r.choice([30, 40, 50, 60, 80, 100])
    se = sd / math.sqrt(n)
    dist = f'normally distributed with mean {mu} {c[1]} and standard deviation {sd} {c[1]}' if norm else f'distributed with mean {mu} {c[1]} and standard deviation {sd} {c[1]}'
    stem = f'{cap(c[0])} are {dist}. A random sample of {n} is taken.'
    k = mu + r.choice([-1, 1]) * round(r.uniform(0.4, 2.0) * se, 1 if se < 5 else 0)
    z = (k - mu) / se
    if D <= 2:
        v = 1 - Phi(z) if k > mu else Phi(z)
        side = 'greater' if k > mu else 'less'
        why = '' if norm else ' (by the central limit theorem, since n is large)'
        return Q(stem + f' Find the probability that the sample mean is {side} than {num(k)} {c[1]}.', n3(v), f'B1 X̄ ~ N({mu}, {sd}²/{n}){why}; M1 z = ({num(k)} − {mu}) ÷ ({sd}/√{n}) = {z3(z)}; A1 {n3(v)}')
    if D == 3:
        d = round(r.uniform(0.5, 1.8) * se, 1 if se < 5 else 0)
        if d <= 0:
            return None
        zz = d / se
        v = 2 * Phi(zz) - 1
        return Q(stem + f' Find the probability that the sample mean is within {num(d)} {c[1]} of {mu} {c[1]}.' + ('' if norm else ' State why your answer is approximate.'),
                 n3(v) + ('' if norm else '; the population is not known to be normal, so X̄ is only approximately normal by the CLT'), f'B1 N({mu}, {sd}²/{n}); M1 z = {num(d)} ÷ ({sd}/√{n}) = {z3(zz)}; M1 2Φ(z) − 1; A1 {n3(v)}' + ('' if norm else '; B1 CLT'))
    if D == 4:
        tgt = r.choice([0.05, 0.02, 0.01])
        d = round(r.uniform(0.15, 0.5) * sd, 1)
        if d <= 0:
            return None
        zc_ = invPhi(1 - tgt / 2)
        nmin = math.ceil((zc_ * sd / d) ** 2 - 1e-9)
        while 2 * (1 - Phi(d / (sd / math.sqrt(nmin)))) >= tgt:
            nmin += 1
        while nmin > 1 and 2 * (1 - Phi(d / (sd / math.sqrt(nmin - 1)))) < tgt:
            nmin -= 1
        return Q(f'{cap(c[0])} are {dist}. Find the smallest sample size n for which the probability that the sample mean differs from {mu} {c[1]} by more than {num(d)} {c[1]} is less than {tgt}.', str(nmin),
                 f'M1 {num(d)} ÷ ({sd}/√n) > {z3(zc_)}; M1 √n > {n3(zc_ * sd / d)}; A1 n = {nmin}')
    T_ = n * mu + r.choice([-1, 1]) * round(r.uniform(0.5, 1.8) * sd * math.sqrt(n))
    zt = (T_ - n * mu) / (sd * math.sqrt(n))
    v = 1 - Phi(zt) if T_ > n * mu else Phi(zt)
    side = 'more' if T_ > n * mu else 'less'
    return Q(stem + f' Find the probability that the total of the {n} values is {side} than {num(T_)} {c[1]}.', n3(v),
             f'M1 total ~ N({n * mu}, {n} × {sd}²) or X̄ < {n3(T_ / n)}; M1 z = {z3(zt)}; A1 {n3(v)}')


@sam3.add('C2', (2, 3, 4), 'explain')
def sam3_err(r, D):
    c = r.choice(SCTX)
    mu, sd = r.randint(*c[2]), r.randint(*c[3])
    n = r.choice([16, 25, 36, 49, 64])
    nm = person(r)
    kind = r.choice(['n', 'clt'])
    if kind == 'n':
        return Q(f'{cap(c[0])} have mean {mu} {c[1]} and standard deviation {sd} {c[1]}. {nm} says the standard deviation of the mean of a sample of {n} is {sd}/{n} = {n3(sd / n)}. Explain the error and find the correct value.',
                 f'The standard deviation of X̄ is σ/√n = {sd}/{int(math.sqrt(n))} = {n3(sd / math.sqrt(n))}.', f'B1 σ/√n; B1 {n3(sd / math.sqrt(n))}')
    n2 = r.choice([5, 6, 8])
    return Q(f'{cap(c[0])} have mean {mu} {c[1]} and standard deviation {sd} {c[1]}; their distribution is unknown. {nm} uses the central limit theorem to say that the mean of a sample of {n2} is approximately normally distributed. Comment on this.',
             f'The central limit theorem requires a large sample (usually n ≥ 30); with n = {n2} and an unknown, possibly skewed population, X̄ may not be approximately normal.', 'B1 n too small; B1 population not known to be normal')


@sam3.add('C3', (2, 3, 4, 5), 'numerical')
def sam3_poisson(r, D):
    lam = r.choice([2.4, 3, 3.5, 4.2, 5, 6.5])
    n = r.choice([40, 50, 60, 80, 100])
    c = r.choice(PCTX)
    se = math.sqrt(lam / n)
    k = round(lam + r.choice([-1, 1]) * r.uniform(0.6, 1.8) * se, 2)
    z = (k - lam) / se
    v = 1 - Phi(z) if k > lam else Phi(z)
    side = 'greater' if k > lam else 'less'
    return Q(f'The number of {c[0]} in {c[1]} has the distribution Po({L(lam)}). The numbers in {n} randomly chosen {unit_pl(c[1])} are recorded. Use a suitable approximation to find the probability that the sample mean is {side} than {num(k)}.',
             n3(v), f'B1 X̄ ~ N({L(lam)}, {L(lam)}/{n}) by CLT; M1 z = ({num(k)} − {L(lam)}) ÷ √({L(lam)}/{n}) = {z3(z)}; A1 {n3(v)}')


def sam3_c4(r, D):
    c = r.choice(SCTX)
    mu, sd = r.randint(*c[2]), r.randint(*c[3])
    n = r.choice([30, 40, 50, 64])
    se = sd / math.sqrt(n)
    k = mu + round(r.uniform(0.8, 1.6) * se, 1)
    z = (k - mu) / se
    m = r.choice([3, 4, 5])
    p1 = 1 - Phi(z)
    intro = f'{cap(c[0])} have mean {mu} {c[1]} and standard deviation {sd} {c[1]}. Random samples of size {n} are taken.'
    parts = [
        P('State the approximate distribution of the sample mean, giving a reason.', f'N({mu}, {num(Fr(sd * sd, n))}), by the central limit theorem since n = {n} is large', 'B1 normal with mean; B1 variance; B1 CLT reason'),
        P(f'Find the probability that the sample mean exceeds {num(k)} {c[1]}.', n3(p1), f'M1 z = {z3(z)}; A1 {n3(p1)}'),
        P(f'{m} independent samples are taken. Find the probability that at least one of the sample means exceeds {num(k)} {c[1]}.', n3(1 - (1 - p1) ** m), f'M1 1 − (1 − {n3(p1)}){sup(m)}; A1 {n3(1 - (1 - p1) ** m)}'),
        P('State the effect on the variance of the sample mean of multiplying the sample size by 4.', 'It is divided by 4 (the standard error is halved).', 'B1'),
    ]
    return cmp_(r, intro, parts)


sam3.add('C4', (2, 3, 4, 5))(sam3_c4)

CHAPTERS[4] = [sam1, sam2, sam3]


# ================================================================ Chapter 5: Estimation

ECTX = [('the masses, x grams, of a random sample of {n} tomatoes', 'g', (80, 140), (6, 15)), ('the times, x minutes, taken by {n} randomly chosen students to run 3 km', 'minutes', (14, 22), (1, 3)),
        ('the lengths, x cm, of {n} randomly chosen fish caught in a lake', 'cm', (25, 45), (3, 7)), ('the daily rainfall, x mm, on {n} randomly chosen days in the wet season in {c}', 'mm', (12, 30), (3, 8)),
        ('the reaction times, x milliseconds, of {n} randomly chosen drivers', 'ms', (200, 320), (20, 50)), ('the weekly spending, x dollars, of {n} randomly chosen students in {c}', 'dollars', (30, 70), (8, 20))]


def esample(r, n):
    c = r.choice(ECTX)
    mu, sd = r.randint(*c[2]), r.randint(*c[3])
    xs = [round(r.gauss(mu, sd), 1) for _ in range(n)]
    return c, mu, sd, xs


def sums(xs):
    sx = round(sum(xs), 1)
    sx2 = round(sum(x * x for x in xs), 2)
    return sx, sx2


def ubv(n, sx, sx2):
    return (sx2 - sx * sx / n) / (n - 1)


est1 = T('Unbiased estimates of population mean and variance', 'unbiased estimates', 'population mean and variance')
est1.fixed('C1', (1, 2), [
    ('An unbiased estimate of the population variance from a sample of size n is', '(1/(n − 1))[Σx² − (Σx)²/n]', 'Divide by n − 1. [1]', ['(1/n)[Σx² − (Σx)²/n]', 'Σx²/n − x̄', '(1/(n − 1))Σx² − x̄²']),
    ('An unbiased estimator of the population mean is', 'the sample mean x̄', '[1]', ['the sample median', 'the sample mode', 'Σx/(n − 1)']),
    ('A sample of 10 values has Σ(x − x̄)² = 45. An unbiased estimate of the population variance is', '5', '45 ÷ 9. [1]', ['4.5', '45', '0.5']),
])
est1.fixed('C2', (2, 3), [
    ('Explain why dividing by n − 1 rather than n gives an unbiased estimate of the population variance.', 'Deviations are measured from the sample mean, which is closer to the data than the population mean, so Σ(x − x̄)² tends to underestimate Σ(x − μ)²; dividing by n − 1 corrects this so the expected value equals σ².', 'B1 deviations from x̄ are too small on average; B1 n − 1 makes E(s²) = σ² [2]'),
    ('Explain what is meant by an unbiased estimate of a population parameter.', 'An estimate from a statistic whose expected value (mean over all possible samples) equals the parameter.', 'B1 expected value; B1 equals parameter [2]'),
])


@est1.add('C1', (1, 2, 3))
def est1_c1(r, D):
    n = r.choice([8, 10, 12, 15, 20, 25])
    c, mu, sd, xs = esample(r, n)
    sx, sx2 = sums(xs)
    s2 = ubv(n, sx, sx2)
    return MCk(r, f'For a random sample of {n} values, Σx = {num(sx)} and Σx² = {num(sx2)}. Find an unbiased estimate of the population variance.', n3(s2),
               [n3(s2 * (n - 1) / n), n3(sx2 / n - sx / n), n3(sx2 / (n - 1)), n3(math.sqrt(s2))], f'({num(sx2)} − {num(sx)}²/{n}) ÷ {n - 1} = {n3(s2)}.')


@est1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def est1_calc(r, D):
    if D <= 2:
        n = r.choice([6, 7, 8])
        c, mu, sd, xs = esample(r, n)
        sx, sx2 = sums(xs)
        m = sx / n
        s2 = ubv(n, sx, sx2)
        if not ok(s2, sum((x - m) ** 2 for x in xs) / (n - 1), 'ubv'):
            return None
        desc = c[0].format(n=n, c=city(r))
        return Q(f'The values of {desc} are: ' + ', '.join(num(x) for x in xs) + '. Find unbiased estimates of the population mean and variance.',
                 f'{n3(m)}, {n3(s2)}', f'B1 x̄ = {n3(m)}; M1 Σx² = {num(sx2)} used with n − 1; A1 {n3(s2)}')
    n = r.choice([20, 30, 40, 50, 60, 80, 100])
    c, mu, sd, xs = esample(r, n)
    desc = c[0].format(n=n, c=city(r))
    if D == 3:
        sx, sx2 = sums(xs)
        m = sx / n
        s2 = ubv(n, sx, sx2)
        return Q(f'For {desc}, Σx = {num(sx)} and Σx² = {num(sx2)}. Find unbiased estimates of the population mean and variance.', f'{n3(m)}, {n3(s2)}',
                 f'B1 x̄ = {n3(m)}; M1 ({num(sx2)} − {num(sx)}²/{n}) ÷ {n - 1}; A1 {n3(s2)}')
    a = int(round(mu))
    sd_ = round(sum(x - a for x in xs), 1)
    sd2 = round(sum((x - a) ** 2 for x in xs), 1)
    m = a + sd_ / n
    s2 = (sd2 - sd_ * sd_ / n) / (n - 1)
    if not ok(s2, ubv(n, sum(xs), sum(x * x for x in xs)), 'coded', 1e-2):
        return None
    if D == 4:
        return Q(f'For {desc}, Σ(x − {a}) = {num(sd_)} and Σ(x − {a})² = {num(sd2)}. Find unbiased estimates of the population mean and variance.', f'{n3(m)}, {n3(s2)}',
                 f'M1 x̄ = {a} + {num(sd_)}/{n}; A1 {n3(m)}; M1 ({num(sd2)} − {num(sd_)}²/{n}) ÷ {n - 1}; A1 {n3(s2)}')
    k = r.choice([0.5, 1, 2])
    pz = 1 - Phi(k * 1.0)
    return Q(f'For {desc}, Σ(x − {a}) = {num(sd_)} and Σ(x − {a})² = {num(sd2)}. Find unbiased estimates of the population mean and variance, and use them with a normal model to estimate the proportion of the population greater than {n3(m + k * math.sqrt(s2))}.',
             f'{n3(m)}, {n3(s2)}; {n3(pz)}', f'M1 x̄; A1 {n3(m)}; M1 s²; A1 {n3(s2)}; M1 z = {z3(k)}; A1 {n3(pz)}')


@est1.add('C2', (2, 3, 4), 'explain')
def est1_err(r, D):
    n = r.choice([10, 12, 15, 20])
    c, mu, sd, xs = esample(r, n)
    sx, sx2 = sums(xs)
    s2 = ubv(n, sx, sx2)
    wrong = sx2 / n - (sx / n) ** 2
    nm = person(r)
    return Q(f'For a random sample of {n} values, Σx = {num(sx)} and Σx² = {num(sx2)}. {nm} calculates Σx²/{n} − (Σx/{n})² = {n3(wrong)} and states that this is an unbiased estimate of the population variance. Explain the error and find the unbiased estimate.',
             f'This is the sample variance, which is biased (too small on average); multiply by {n}/{n - 1}: {n3(s2)}.', f'B1 divide by n − 1 / multiply by n/(n − 1); B1 {n3(s2)}')


def est1_c4(r, D):
    n = r.choice([40, 50, 60, 80])
    c, mu, sd, xs = esample(r, n)
    sx, sx2 = sums(xs)
    m = sx / n
    s2 = ubv(n, sx, sx2)
    se = math.sqrt(s2 / n)
    desc = c[0].format(n=n, c=city(r))
    cl = r.choice([90, 95, 99])
    zc_ = CONF[cl]
    intro = f'For {desc}, Σx = {num(sx)} and Σx² = {num(sx2)}.'
    parts = [
        P('Find unbiased estimates of the population mean and variance.', f'{n3(m)}, {n3(s2)}', f'B1 {n3(m)}; M1 n − 1 divisor; A1 {n3(s2)}'),
        P(f'Find a {cl}% confidence interval for the population mean.', iv(m - zc_ * se, m + zc_ * se), f'M1 {n3(m)} ± {zc_} × √({n3(s2)}/{n}); B1 z = {zc_}; A1 {iv(m - zc_ * se, m + zc_ * se)}'),
        P('Explain why it is not necessary to assume that the population is normally distributed.', f'n = {n} is large, so by the central limit theorem the sample mean is approximately normal.', 'B1 large n; B1 CLT'),
    ]
    return cmp_(r, intro, parts, k=(2, 3))


est1.add('C4', (2, 3, 4, 5))(est1_c4)


est2 = T('Confidence intervals for a population mean using the normal distribution', 'confidence intervals for a population mean', 'normal distribution')
est2.fixed('C1', (1, 2), [
    ('The z-value used for a 95% confidence interval is', '1.96', 'Φ(1.96) = 0.975. [1]', ['1.645', '2.576', '1.282']),
    ('The z-value used for a 99% confidence interval is', '2.576', 'Φ(2.576) = 0.995. [1]', ['2.326', '1.96', '3.09']),
    ('Increasing the sample size, with the same confidence level, makes the confidence interval', 'narrower', 'Width ∝ 1/√n. [1]', ['wider', 'unchanged', 'centred on a different value']),
    ('Increasing the confidence level from 90% to 99%, with the same sample, makes the interval', 'wider', 'Larger z. [1]', ['narrower', 'unchanged', 'shift to the right']),
])
est2.fixed('C2', (2, 3), [
    ('Explain why a confidence interval for a mean can be calculated from a large sample even when the population distribution is unknown.', 'By the central limit theorem the sample mean is approximately normally distributed for large n, and the sample variance gives a good estimate of σ².', 'B1 CLT; B1 s² estimates σ² [2]'),
])


@est2.add('C1', (1, 2, 3))
def est2_c1(r, D):
    cl = r.choice([90, 95, 98, 99])
    m = round(r.uniform(10, 200), 1)
    sd = r.choice([2, 3, 4, 5, 6, 8, 10, 12])
    n = r.choice([16, 25, 36, 49, 64, 100])
    zc_ = CONF[cl]
    h = zc_ * sd / math.sqrt(n)
    return MCk(r, f'A random sample of {n} from a normal population with standard deviation {sd} has mean {num(m)}. Find a {cl}% confidence interval for the population mean.', iv(m - h, m + h),
               [iv(m - zc_ * sd / n, m + zc_ * sd / n), iv(m - zc_ * sd, m + zc_ * sd), iv(m - 1.645 * sd / math.sqrt(n), m + 1.645 * sd / math.sqrt(n)) if cl != 90 else iv(m - 1.96 * sd / math.sqrt(n), m + 1.96 * sd / math.sqrt(n)), iv(m - h / 2, m + h / 2)],
               f'{num(m)} ± {zc_} × {sd}/√{n}.')


@est2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def est2_calc(r, D):
    c = r.choice(ECTX)
    mu, sd = r.randint(*c[2]), r.randint(*c[3])
    cl = r.choice([90, 95, 98, 99])
    zc_ = CONF[cl]
    if D <= 2:
        n = r.choice([10, 12, 15, 20, 25])
        m = round(mu + r.uniform(-1, 1) * sd / math.sqrt(n), 1)
        h = zc_ * sd / math.sqrt(n)
        desc = c[0].format(n=n, c=city(r))
        return Q(f'The population of values in {desc} is normal with standard deviation {sd} {c[1]}. The sample mean is {num(m)} {c[1]}. Find a {cl}% confidence interval for the population mean.',
                 iv(m - h, m + h), f'B1 z = {zc_}; M1 {num(m)} ± {zc_} × {sd}/√{n}; A1 {iv(m - h, m + h)}')
    if D == 3:
        n = r.choice([40, 50, 60, 80, 100])
        xs = [r.gauss(mu, sd) for _ in range(n)]
        sx, sx2 = sums([round(x, 1) for x in xs])
        m = sx / n
        s2 = ubv(n, sx, sx2)
        h = zc_ * math.sqrt(s2 / n)
        desc = c[0].format(n=n, c=city(r))
        return Q(f'For {desc}, Σx = {num(sx)} and Σx² = {num(sx2)}. Calculate a {cl}% confidence interval for the population mean.', iv(m - h, m + h),
                 f'M1 x̄ = {n3(m)}; M1 s² = {n3(s2)}; B1 z = {zc_}; M1 x̄ ± z√(s²/n); A1 {iv(m - h, m + h)}')
    if D == 4:
        w = round(r.uniform(0.2, 0.6) * sd, 1)
        if w <= 0:
            return None
        n = math.ceil((2 * zc_ * sd / w) ** 2 - 1e-9)
        if not ok(2 * zc_ * sd / math.sqrt(n) <= w + 1e-12 and 2 * zc_ * sd / math.sqrt(n - 1) > w, True, 'n width'):
            return None
        return Q(f'{cap(c[0].format(n="n", c=city(r)))}: the population standard deviation is {sd} {c[1]}. Find the smallest sample size for which the width of a {cl}% confidence interval for the population mean is at most {num(w)} {c[1]}.',
                 str(n), f'M1 2 × {zc_} × {sd}/√n ≤ {num(w)}; M1 √n ≥ {n3(2 * zc_ * sd / w)}; A1 n = {n}')
    n = r.choice([25, 36, 49, 64, 100])
    m = round(mu + r.uniform(-1, 1), 1)
    zz = round(r.choice([1.2, 1.4, 1.5, 1.75, 1.8, 2.0, 2.2, 2.4]), 2)
    h = zz * sd / math.sqrt(n)
    lo, hi = round(m - h, 2), round(m + h, 2)
    zg = (hi - lo) / 2 / (sd / math.sqrt(n))
    conf = 2 * Phi(zg) - 1
    return Q(f'A random sample of {n} values is taken from a normal population with standard deviation {sd}. An a% confidence interval for the population mean, calculated from the sample, is ({num(lo)}, {num(hi)}). Find the sample mean and the value of a.',
             f'x̄ = {num(round((lo + hi) / 2, 3))}; a = {n3(conf * 100)}', f'B1 x̄ = ({num(lo)} + {num(hi)})/2; M1 z × {sd}/√{n} = {num(round((hi - lo) / 2, 4))}; A1 z = {z3(zg)}; M1 2Φ(z) − 1; A1 a = {n3(conf * 100)}')


@est2.add('C2', (2, 3, 4), 'explain')
def est2_err(r, D):
    sd = r.choice([4, 5, 6, 8])
    n = r.choice([25, 36, 49, 64])
    m = round(r.uniform(20, 80), 1)
    nm = person(r)
    kind = r.choice(['n', 'z'])
    if kind == 'n':
        h = 1.96 * sd / math.sqrt(n)
        return Q(f'A random sample of {n} from a normal population with standard deviation {sd} has mean {num(m)}. {nm} calculates a 95% confidence interval as {num(m)} ± 1.96 × {sd}/{n}. Explain the error and find the correct interval.',
                 f'The standard error is σ/√n = {sd}/√{n}, not σ/n: {iv(m - h, m + h)}.', f'B1 σ/√n; M1 {num(m)} ± 1.96 × {sd}/{int(math.sqrt(n))}; A1 {iv(m - h, m + h)}')
    h = 2.576 * sd / math.sqrt(n)
    return Q(f'A random sample of {n} from a normal population with standard deviation {sd} has mean {num(m)}. {nm} calculates a 99% confidence interval using z = 2.326. Explain the error and find the correct interval.',
             f'2.326 is for a 98% interval (or a 1% one-tailed value); a 99% two-sided interval uses z = 2.576: {iv(m - h, m + h)}.', f'B1 z = 2.576; M1 {num(m)} ± 2.576 × {sd}/√{n}; A1 {iv(m - h, m + h)}')


def est2_c4(r, D):
    c = r.choice(ECTX)
    mu, sd = r.randint(*c[2]), r.randint(*c[3])
    n = r.choice([50, 60, 80, 100])
    xs = [round(r.gauss(mu, sd), 1) for _ in range(n)]
    sx, sx2 = sums(xs)
    m = sx / n
    s2 = ubv(n, sx, sx2)
    se = math.sqrt(s2 / n)
    cl1, cl2 = 95, r.choice([90, 99])
    h1, h2 = CONF[cl1] * se, CONF[cl2] * se
    claim = round(m + r.choice([-1, 1]) * r.uniform(1.0, 2.8) * se, 1)
    desc = c[0].format(n=n, c=city(r))
    intro = f'For {desc}, Σx = {num(sx)} and Σx² = {num(sx2)}.'
    parts = [
        P('Find unbiased estimates of the population mean and variance.', f'{n3(m)}, {n3(s2)}', f'B1 {n3(m)}; M1 divisor n − 1; A1 {n3(s2)}'),
        P(f'Find a {cl1}% confidence interval for the population mean.', iv(m - h1, m + h1), f'M1 x̄ ± 1.96√(s²/n); A1 {iv(m - h1, m + h1)}'),
        P(f'Find a {cl2}% confidence interval for the population mean.', iv(m - h2, m + h2), f'B1 z = {CONF[cl2]}; A1 {iv(m - h2, m + h2)}'),
        P(f'It is claimed that the population mean is {num(claim)} {c[1]}. Comment on this claim using your {cl1}% interval.',
          (f'{num(claim)} lies inside the interval, so the data do not contradict the claim.' if m - h1 < claim < m + h1 else f'{num(claim)} lies outside the interval, so there is evidence against the claim.'), 'B1 compares with interval; B1 conclusion in context'),
    ]
    return cmp_(r, intro, parts, deps={3: [1]})


est2.add('C4', (2, 3, 4, 5))(est2_c4)


est3 = T('Confidence intervals for a population proportion from a large sample', 'confidence intervals for a population proportion', 'large sample')
est3.fixed('C1', (1, 2), [
    ('An approximate confidence interval for a population proportion p, from a large sample with sample proportion p̂, is', 'p̂ ± z√(p̂(1 − p̂)/n)', '[1]', ['p̂ ± z p̂(1 − p̂)/n', 'p̂ ± z√(p̂/n)', 'p̂ ± z(1 − p̂)/√n']),
    ('In a random sample of 200 people, 46 are left-handed. The sample proportion is', '0.23', '46/200. [1]', ['0.46', '0.77', '0.0023']),
    ('For a fixed sample size, the width of a confidence interval for a proportion is greatest when p̂ is', '0.5', 'p̂(1 − p̂) is maximised at 0.5. [1]', ['0', '1', '0.05']),
])
est3.fixed('C2', (2, 3), [
    ('Explain why a confidence interval for a proportion calculated from a large sample is only approximate.', 'It uses a normal approximation to the binomial distribution of the number of successes, and uses p̂ in place of the unknown p in the standard error.', 'B1 normal approximation; B1 p̂ used for p [2]'),
])

PCTXS = [('people in a random sample of {n} adults in {c} said they cycle to work', 'adults in {c} who cycle to work'), ('of {n} randomly chosen seeds germinated', 'seeds that germinate'),
         ('of {n} randomly selected customers rated a service as excellent', 'customers who rate the service as excellent'), ('of {n} randomly chosen phones of a model developed a battery fault', 'phones with a battery fault'),
         ('students in a random sample of {n} from a university in {c} are vegetarian', 'vegetarian students at the university'), ('of {n} randomly chosen eggs from a farm were double-yolked', 'double-yolked eggs')]


@est3.add('C1', (1, 2, 3))
def est3_c1(r, D):
    n = r.choice([100, 150, 200, 250, 300, 400, 500])
    x = r.randint(int(n * 0.08), int(n * 0.7))
    ph = x / n
    cl = r.choice([90, 95, 99])
    zc_ = CONF[cl]
    h = zc_ * math.sqrt(ph * (1 - ph) / n)
    return MCk(r, f'In a random sample of {n}, {x} have a certain property. Find an approximate {cl}% confidence interval for the population proportion.', iv(ph - h, ph + h),
               [iv(ph - zc_ * ph * (1 - ph) / n, ph + zc_ * ph * (1 - ph) / n), iv(ph - zc_ * math.sqrt(ph / n), ph + zc_ * math.sqrt(ph / n)), iv(ph - h / 2, ph + h / 2), iv(ph - zc_ * math.sqrt(ph * (1 - ph) / (n - 1)) * 1.3, ph + zc_ * math.sqrt(ph * (1 - ph) / (n - 1)) * 1.3)],
               f'p̂ = {n3(ph)}; {n3(ph)} ± {zc_}√({n3(ph)} × {n3(1 - ph)}/{n}).')


@est3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def est3_calc(r, D):
    a, b = r.choice(PCTXS)
    cty = city(r)
    n = r.choice([80, 100, 120, 150, 200, 250, 300, 400, 500])
    x = r.randint(int(n * 0.1), int(n * 0.6))
    ph = x / n
    cl = r.choice([90, 95, 98, 99])
    zc_ = CONF[cl]
    se = math.sqrt(ph * (1 - ph) / n)
    stem = f'{x} {a.format(n=n, c=cty)}.'
    if D <= 3:
        return Q(stem + f' Calculate an approximate {cl}% confidence interval for the proportion of {b.format(c=cty)}.', iv(ph - zc_ * se, ph + zc_ * se),
                 f'B1 p̂ = {n3(ph)}; M1 {n3(ph)} ± {zc_}√({n3(ph)} × {n3(1 - ph)}/{n}); A1 {iv(ph - zc_ * se, ph + zc_ * se)}')
    if D == 4:
        w = r.choice([0.06, 0.08, 0.1])
        nmin = math.ceil(4 * zc_ * zc_ * ph * (1 - ph) / (w * w) - 1e-9)
        return Q(stem + f' Using this sample proportion as an estimate, find the smallest sample size needed for an approximate {cl}% confidence interval of total width at most {w}.', str(nmin),
                 f'M1 2 × {zc_}√({n3(ph)} × {n3(1 - ph)}/n) ≤ {w}; M1 n ≥ {n3(4 * zc_ * zc_ * ph * (1 - ph) / (w * w))}; A1 {nmin}')
    lo, hi = round(ph - zc_ * se, 3), round(ph + zc_ * se, 3)
    ph2 = (lo + hi) / 2
    h = (hi - lo) / 2
    n2 = zc_ * zc_ * ph2 * (1 - ph2) / (h * h)
    return Q(f'A random sample of n {b.format(c=cty).split(" who")[0] if " who" in b else "items"} gives an approximate {cl}% confidence interval ({num(lo)}, {num(hi)}) for the proportion of {b.format(c=cty)}. Find the sample proportion and estimate n.',
             f'p̂ = {num(round(ph2, 4))}; n ≈ {round(n2)}', f'B1 p̂ = ({num(lo)} + {num(hi)})/2; M1 {zc_}√(p̂(1 − p̂)/n) = {num(round(h, 4))}; A1 n ≈ {round(n2)}')


@est3.add('C2', (2, 3, 4), 'explain')
def est3_err(r, D):
    n = r.choice([120, 200, 250, 400])
    x = r.randint(int(n * 0.15), int(n * 0.5))
    ph = x / n
    nm = person(r)
    h = 1.96 * math.sqrt(ph * (1 - ph) / n)
    return Q(f'In a random sample of {n} people, {x} own a pet. {nm} calculates a 95% confidence interval for the proportion as {n3(ph)} ± 1.96 × {n3(ph)} × {n3(1 - ph)} ÷ {n}. Explain the error and find the correct interval.',
             f'The standard error is the square root: √(p̂(1 − p̂)/n) = {n3(math.sqrt(ph * (1 - ph) / n))}. Interval {iv(ph - h, ph + h)}.', f'B1 square root missing; M1 {n3(ph)} ± 1.96√({n3(ph)} × {n3(1 - ph)}/{n}); A1 {iv(ph - h, ph + h)}')


def est3_c4(r, D):
    a, b = r.choice(PCTXS)
    cty = city(r)
    n = r.choice([150, 200, 250, 300])
    x = r.randint(int(n * 0.2), int(n * 0.5))
    ph = x / n
    se = math.sqrt(ph * (1 - ph) / n)
    claim = round(ph + r.choice([-1, 1]) * r.uniform(1.0, 3.0) * se, 2)
    k = r.choice([5, 8, 10])
    intro = f'{x} {a.format(n=n, c=cty)}.'
    parts = [
        P(f'Find an approximate 95% confidence interval for the proportion of {b.format(c=cty)}.', iv(ph - 1.96 * se, ph + 1.96 * se), f'B1 p̂ = {n3(ph)}; M1 ± 1.96√(p̂(1 − p̂)/{n}); A1 {iv(ph - 1.96 * se, ph + 1.96 * se)}'),
        P(f'A report claims that the proportion is {num(claim)}. Comment on this claim.', (f'{num(claim)} lies inside the interval, so the claim is supported.' if ph - 1.96 * se < claim < ph + 1.96 * se else f'{num(claim)} lies outside the interval, so the claim is doubtful.'), 'B1 comparison; B1 conclusion'),
        P(f'{k} independent 95% confidence intervals are calculated from different samples. Find the probability that all {k} contain the true proportion.', n3(0.95 ** k), f'M1 0.95{sup(k)}; A1 {n3(0.95 ** k)}'),
        P('Explain why the sample must be random.', 'So that it is representative and p̂ is an unbiased estimate of p; otherwise the interval may be systematically wrong.', 'B1'),
    ]
    return cmp_(r, intro, parts, deps={1: [0]})


est3.add('C4', (2, 3, 4, 5))(est3_c4)


est4 = T('Interpreting confidence intervals in context', 'interpreting confidence intervals', 'in context')
est4.fixed('C1', (1, 2), [
    ('A 95% confidence interval for μ is (12.1, 14.3). Which statement is correct?', 'If many such intervals were calculated, about 95% of them would contain μ', 'μ is fixed; the interval varies from sample to sample. [1]', ['μ lies between 12.1 and 14.3 with probability 0.95 for this interval', '95% of the data lie between 12.1 and 14.3', 'The sample mean lies in the interval with probability 0.95']),
    ('Twenty independent 90% confidence intervals for μ are calculated. The expected number that contain μ is', '18', '20 × 0.9. [1]', ['2', '19', '20']),
    ('A 95% confidence interval for μ is (48.2, 51.6). Does it support the claim that μ = 50?', 'Yes, because 50 lies within the interval', '[1]', ['No, because 50 is not the centre', 'No, because the interval is too wide', 'Yes, because 50 is greater than 48.2 only']),
])
est4.fixed('C2', (2, 3), [
    ('A student says: “There is a 95% probability that μ lies in the interval (4.2, 5.8).” Explain why this statement is not strictly correct.', 'μ is a fixed constant and either lies in the interval or not; the 95% refers to the method: 95% of intervals constructed this way contain μ.', 'B1 μ fixed; B1 95% of intervals from repeated samples [2]'),
    ('Explain the effect on a confidence interval of using a smaller confidence level.', 'A smaller z-value is used, so the interval is narrower but is less likely to contain the true mean.', 'B1 narrower; B1 less likely to contain μ [2]'),
])


@est4.add('C3', (1, 2, 3, 4, 5), 'numerical')
def est4_calc(r, D):
    cl = r.choice([90, 95, 98, 99])
    p = cl / 100
    k = r.choice([5, 6, 8, 10, 12, 15, 20])
    if D == 1:
        return MCk(r, f'{k} independent {cl}% confidence intervals for a population mean are calculated from different random samples. Find the expected number of intervals that do not contain the true mean.', num(round(k * (1 - p), 4)),
                   [num(round(k * p, 4)), num(round(1 - p, 4)), num(round(k * (1 - p) * 2, 4)), num(k)], f'{k} × {num(round(1 - p, 2))} = {num(round(k * (1 - p), 4))}.')
    if D == 2:
        return Q(f'{k} independent {cl}% confidence intervals for a population mean are calculated. Find the probability that all of them contain the true mean.', n3(p ** k), f'M1 {num(p)}{sup(k)}; A1 {n3(p ** k)}')
    if D == 3:
        j = k - r.randint(1, 2)
        v = 1 - bcdf(k, p, j - 1)
        return Q(f'{k} independent {cl}% confidence intervals for a population proportion are calculated. Find the probability that at least {j} of them contain the true proportion.', n3(v),
                 f'M1 B({k}, {num(p)}); M1 P(X ≥ {j}) = ' + ' + '.join(f'P(X = {i})' for i in range(j, k + 1)) + f'; A1 {n3(v)}')
    c = r.choice(ECTX)
    mu, sd = r.randint(*c[2]), r.randint(*c[3])
    n = r.choice([25, 36, 50, 64])
    m = round(mu + r.uniform(-0.5, 0.5) * sd / math.sqrt(n), 1)
    zc_ = CONF[cl]
    h = zc_ * sd / math.sqrt(n)
    claim = round(m + r.choice([-1, 1]) * r.uniform(0.3, 1.8) * h, 1)
    inside = m - h < claim < m + h
    if D == 4:
        desc = c[0].format(n=n, c=city(r))
        return Q(f'For {desc}, the sample mean is {num(m)} {c[1]}; the population standard deviation is {sd} {c[1]}. Calculate a {cl}% confidence interval for the population mean and use it to comment on a claim that the mean is {num(claim)} {c[1]}.',
                 f'{iv(m - h, m + h)}; ' + ('the claimed value lies inside, so the claim is not contradicted.' if inside else 'the claimed value lies outside, so there is evidence against the claim.'),
                 f'M1 {num(m)} ± {zc_} × {sd}/√{n}; A1 {iv(m - h, m + h)}; B1 conclusion in context')
    lo1 = round(m - h, 2)
    hi1 = round(m + h, 2)
    cl2 = r.choice([c_ for c_ in (90, 95, 98, 99) if c_ != cl])
    h2 = CONF[cl2] * sd / math.sqrt(n)
    return Q(f'A {cl}% confidence interval for a population mean, from a sample of size {n} from a normal population with known standard deviation, is ({num(lo1)}, {num(hi1)}). Find the {cl2}% confidence interval from the same sample.',
             iv(m - h2, m + h2), f'B1 x̄ = {num(round((lo1 + hi1) / 2, 3))}; M1 σ/√n = half-width ÷ {zc_} = {n3((hi1 - lo1) / 2 / zc_)}; M1 x̄ ± {CONF[cl2]} × σ/√n; A1 {iv(m - h2, m + h2)}')


@est4.add('C2', (1, 2, 3, 4), 'explain')
def est4_claim(r, D):
    lo = round(r.uniform(10, 60), 1)
    hi = round(lo + r.uniform(1.5, 6), 1)
    cl = r.choice([90, 95, 99])
    nm = person(r)
    stmts = [(f'There is a {cl}% probability that μ lies between {num(lo)} and {num(hi)}.', False, f'μ is fixed; {cl}% refers to the proportion of such intervals, over repeated samples, that contain μ.'),
             (f'{cl}% of the population values lie between {num(lo)} and {num(hi)}.', False, 'The interval is for the mean, not for individual values; most individual values lie well outside it.'),
             (f'If the sampling were repeated many times, about {cl}% of the intervals obtained would contain μ.', True, 'This is the correct interpretation of a confidence interval.'),
             (f'A {100 - (100 - cl) // 2 if cl < 99 else 99.5}% interval from the same data would be narrower.', False, 'A higher confidence level needs a larger z-value, so the interval would be wider.')]
    s, okk, why = r.choice(stmts)
    return Q(f'A {cl}% confidence interval for a population mean μ is ({num(lo)}, {num(hi)}). {nm} states: “{s}” Is this correct? Explain.', ('Correct. ' if okk else 'Not correct. ') + why, 'B1 judgement; B1 explanation')


def est4_c4(r, D):
    c = r.choice(ECTX)
    mu, sd = r.randint(*c[2]), r.randint(*c[3])
    n = r.choice([36, 49, 64, 100])
    m = round(mu + r.uniform(-0.5, 0.5) * sd / math.sqrt(n), 1)
    h95 = 1.96 * sd / math.sqrt(n)
    claim = round(m + r.choice([-1, 1]) * r.uniform(1.1, 1.5) * h95, 1)
    h99 = 2.576 * sd / math.sqrt(n)
    desc = c[0].format(n=n, c=city(r))
    k = r.choice([10, 12, 20])
    intro = f'For {desc}, the sample mean is {num(m)} {c[1]}. The population is normal with standard deviation {sd} {c[1]}. A manager claims the population mean is {num(claim)} {c[1]}.'
    parts = [
        P('Find a 95% confidence interval for the population mean.', iv(m - h95, m + h95), f'M1 {num(m)} ± 1.96 × {sd}/√{n}; A1 {iv(m - h95, m + h95)}'),
        P('Find a 99% confidence interval for the population mean.', iv(m - h99, m + h99), f'M1 2.576; A1 {iv(m - h99, m + h99)}'),
        P('Comment on the manager’s claim, referring to both intervals.', ('The claim lies outside the 95% interval but ' + ('inside' if m - h99 < claim < m + h99 else 'also outside') + ' the 99% interval') +
          ('; the evidence against it is fairly strong but not conclusive at the 1% level.' if m - h99 < claim < m + h99 else '; there is strong evidence against the claim.'),
          'B1 position relative to each interval; B1 balanced conclusion'),
        P(f'{k} such 95% intervals are calculated from independent samples. Find the probability that exactly {k - 1} contain the true mean.', n3(bpmf(k, 0.95, k - 1)), f'M1 {k} × 0.95{sup(k - 1)} × 0.05; A1 {n3(bpmf(k, 0.95, k - 1))}'),
    ]
    return cmp_(r, intro, parts, deps={2: [0, 1]})


est4.add('C4', (2, 3, 4, 5))(est4_c4)

CHAPTERS[5] = [est1, est2, est3, est4]


# ================================================================ Chapter 6: Hypothesis tests

H0, H1 = 'H₀', 'H₁'
TAILS = '<>≠'


def pctp(p):
    return num(round(float(p) * 100, 6)) + '%'


def apc(alpha):
    return num(round(alpha * 100, 6)) + '%'


def pfm(p):
    if isinstance(p, Fr):
        return num(p) if p.denominator % 3 == 0 else dn(p)
    return num(p)


def hyp(par, v, tail):
    return f'{H0}: {par} = {v}, {H1}: {par} {tail} {v}'


def concl(rej, alpha, subj, d):
    if rej:
        return f'Reject {H0}. There is sufficient evidence at the {apc(alpha)} significance level that {subj} {d}.'
    return f'Do not reject {H0}. There is insufficient evidence at the {apc(alpha)} significance level that {subj} {d}.'


# Binomial test contexts: dirs are the alternatives for <, >, ≠ (None if unnatural)
BCTX = [
    dict(s='In the past, {pp} of the customers at a café in {c} ordered a cold drink. After the menu is changed, the owner wishes to test whether this proportion {d}.',
         dirs=('has decreased', 'has increased', 'has changed'), subj='the proportion of customers who order a cold drink',
         samp='In a random sample of {n} customers after the change, {x} ordered a cold drink.', ps=[0.2, 0.25, 0.3, 0.4], unit='customers'),
    dict(s='{nm} suspects that a coin {d}.', dirs=('is biased against heads', 'is biased towards heads', 'is biased'), subj='the coin',
         samp='The coin is tossed {n} times and shows heads {x} times.', ps=[Fr(1, 2)], unit='tosses'),
    dict(s='{nm} suspects that an ordinary six-sided die {d}.', dirs=('shows a six less often than it should', 'shows a six more often than it should', 'is biased with respect to sixes'),
         subj='the die', samp='The die is thrown {n} times and shows a six {x} times.', ps=[Fr(1, 6)], unit='throws'),
    dict(s='A seed company states that {pp} of its tomato seeds germinate. A gardener in {c} wishes to test whether the germination rate {d}.',
         dirs=('is lower than stated', 'is higher than stated', 'is different from the stated value'), subj='the germination rate',
         samp='The gardener plants {n} randomly chosen seeds and {x} of them germinate.', ps=[0.6, 0.7, 0.75, 0.8, 0.85], unit='seeds'),
    dict(s='A standard treatment for a condition is successful for {pp} of patients. Doctors in {c} test whether a new treatment {d}.',
         dirs=('is less successful', 'is more successful', 'has a different success rate'), subj='the new treatment',
         samp='Of {n} randomly chosen patients given the new treatment, the number treated successfully is {x}.', ps=[0.3, 0.4, 0.55, 0.6, 0.65], unit='patients'),
    dict(s='A factory in {c} has found that {pp} of the components it makes are faulty. After new machinery is installed, the manager tests whether the proportion of faulty components {d}.',
         dirs=('has decreased', 'has increased', 'has changed'), subj='the proportion of faulty components',
         samp='In a random sample of {n} components made by the new machinery, the number of faulty components is {x}.', ps=[0.1, 0.12, 0.15, 0.2, 0.25], unit='components'),
    dict(s='A national survey found that {pp} of adults in {c} read a daily newspaper. A journalist wishes to test whether the proportion for young adults {d}.',
         dirs=('is lower', 'is higher', 'is different'), subj='the proportion for young adults',
         samp='In a random sample of {n} young adults, {x} read a daily newspaper.', ps=[0.25, 0.3, 0.35, 0.4, 0.45], unit='young adults'),
    dict(s='{nm} is an archer who hits the centre of the target with probability {pd}. After a new coaching programme, {nm} wishes to test whether this probability {d}.',
         dirs=('has decreased', 'has increased', 'has changed'), subj="{nm}'s probability of hitting the centre",
         samp='In {n} shots after the programme, {nm} hits the centre {x} times.', ps=[0.2, 0.25, 0.3, 0.35, 0.4], unit='shots'),
    dict(s='A test consists of multiple-choice questions, each with 4 options. A teacher wishes to test whether {nm} {d}.',
         dirs=(None, 'does better than guessing at random', None), subj=f'{{nm}}',
         samp='{nm} answers {n} questions and gets {x} correct.', ps=[Fr(1, 4)], unit='questions'),
    dict(s='In the past, {pp} of the buses on a route in {c} arrived late. After a new timetable is introduced, the bus company tests whether the proportion of late buses {d}.',
         dirs=('has decreased', 'has increased', 'has changed'), subj='the proportion of late buses',
         samp='Of {n} randomly chosen buses after the change, {x} arrived late.', ps=[0.15, 0.2, 0.25, 0.3, 0.35], unit='buses'),
]


def bpv(n, p, x, side):
    return bcdf(n, p, x) if side == '<' else 1 - bcdf(n, p, x - 1)


def bpv_chk(n, p, x, side):
    a = bpv(n, p, x, side)
    b = sum(bpmf(n, p, i) for i in (range(0, x + 1) if side == '<' else range(x, n + 1)))
    return ok(a, b, 'bpv')


def bset(r, tails=TAILS, ns=(10, 12, 15, 16, 18, 20, 24, 25), alphas=(0.1, 0.05, 0.025, 0.01), want=None):
    """Random binomial test with an observed value giving a clear decision."""
    cs = [c for c in BCTX if any(c['dirs'][i] and TAILS[i] in tails for i in range(3))]
    c = r.choice(cs)
    tail = r.choice([TAILS[i] for i in range(3) if c['dirs'][i] and TAILS[i] in tails])
    p = r.choice(c['ps'])
    pf = float(p)
    n = r.choice(ns)
    alpha = r.choice([a for a in alphas if not (tail == '≠' and a == 0.025)])
    side = tail if tail != '≠' else r.choice('<>')
    ae = alpha / 2 if tail == '≠' else alpha
    rej, nrej = [], []
    for x in range(0, n + 1):
        if (side == '<' and x >= n * pf) or (side == '>' and x <= n * pf):
            continue
        v = bpv(n, pf, x, side)
        if v < 0.0005 or v > 0.35 or abs(v - ae) < 0.12 * ae:
            continue
        (rej if v < ae else nrej).append((x, v))
    w = want if want is not None else r.random() < 0.5
    pool = (rej if w else nrej) or rej or nrej
    if not pool:
        return None
    x, v = r.choice(pool)
    if not bpv_chk(n, pf, x, side):
        return None
    nm, cty = person(r), city(r)
    d = c['dirs'][TAILS.index(tail)]
    f = dict(pp=pctp(p), pd=pfm(p), nm=nm, c=cty, d=d)
    return dict(c=c, tail=tail, side=side, p=p, pf=pf, n=n, x=x, pv=v, alpha=alpha, ae=ae, rej=v < ae, nm=nm, d=d,
                setup=c['s'].format(**f), samp=c['samp'].format(n=n, x=x, **f).replace(' 1 times', ' once'), subj=c['subj'].format(**f),
                hyp=hyp('p', pfm(p), tail), f=f)


def pv_s(side, x, dist):
    return (f'P(X ≤ {x})' if side == '<' else f'P(X ≥ {x})') + (f' with X ~ {dist}' if dist else '')


def bdist(b):
    return f'B({b["n"]}, {pfm(b["p"])})'


def btest_key(b, hyp_mark=True):
    k = (f'B1 {b["hyp"]}; ' if hyp_mark else '') + f'M1 {pv_s(b["side"], b["x"], bdist(b))}' + \
        (f' = 1 − P(X ≤ {b["x"] - 1})' if b['side'] == '>' else '') + f'; A1 {p3(b["pv"])}; M1 compare with {num(b["ae"])}' + \
        (' (two-tailed, so half of the significance level)' if b['tail'] == '≠' else '') + '; A1 conclusion in context'
    return k


def btest_ans(b):
    return f'{b["hyp"]}; {pv_s(b["side"], b["x"], "")} = {p3(b["pv"])} ' + ('<' if b['rej'] else '>') + f' {num(b["ae"])}. ' + concl(b['rej'], b['alpha'], b['subj'], b['d'])


# Poisson test contexts
HPCTX = [
    dict(ev='calls received by a helpline', short='calls received', base='a 10-minute period', chg="After the helpline's website is redesigned, the manager wishes to test whether the mean number of calls {d}.",
         subj='the mean number of calls', obs=[('a 30-minute period', 3), ('a one-hour period', 6), ('a 20-minute period', 2)], big=[('a 3-hour period', 18), ('a 2-hour period', 12)], lams=[1.2, 1.5, 1.8, 2.4]),
    dict(ev='accidents at a road junction in {c}', short='accidents', base='a month', chg='After traffic lights are installed, a council officer wishes to test whether the mean number of accidents {d}.',
         subj='the mean number of accidents', obs=[('a 6-month period', 6), ('a year', 12), ('a 4-month period', 4)], big=[('a 2-year period', 24), ('a 3-year period', 36)], lams=[0.5, 0.8, 1.25, 1.5]),
    dict(ev='flaws', short='flaws', base='a 1-metre length of fabric from a mill', chg='After a new loom is installed, the manager wishes to test whether the mean number of flaws {d}.',
         subj='the mean number of flaws', obs=[('a 5-metre length', 5), ('a 4-metre length', 4), ('a 10-metre length', 10)], big=[('a 25-metre length', 25), ('a 40-metre length', 40)], lams=[0.6, 0.8, 1.2, 1.5]),
    dict(ev='emails received by an office manager', short='emails received', base='an hour', chg='After a new spam filter is installed, the manager wishes to test whether the mean number of emails {d}.',
         subj='the mean number of emails', obs=[('a 3-hour period', 3), ('a 4-hour period', 4), ('a 2-hour period', 2)], big=[('a 10-hour period', 10), ('a 12-hour period', 12)], lams=[2, 2.4, 3, 3.6]),
    dict(ev='bacteria', short='bacteria', base='1 ml of river water taken near a factory in {c}', chg='After the factory closes, a scientist wishes to test whether the mean number of bacteria {d}.',
         subj='the mean number of bacteria', obs=[('a 5 ml sample', 5), ('a 4 ml sample', 4), ('a 2 ml sample', 2)], big=[('a 10 ml sample', 10), ('a 12 ml sample', 12)], lams=[1.6, 2.4, 3.2]),
    dict(ev='earthquakes of magnitude 5 or more in a region', short='such earthquakes', base='a year', chg='A geologist wishes to test whether the mean number of such earthquakes {d}.',
         subj='the mean number of earthquakes', obs=[('a 5-year period', 5), ('a 4-year period', 4), ('a 10-year period', 10)], big=[('a 20-year period', 20), ('a 25-year period', 25)], lams=[0.7, 1.2, 1.5]),
    dict(ev='typing errors made by a typist', short='errors', base='a page', chg='After a training course, the typist wishes to test whether the mean number of errors {d}.',
         subj='the mean number of errors', obs=[('a 10-page report', 10), ('a 5-page report', 5), ('an 8-page report', 8)], big=[('a 40-page report', 40), ('a 50-page report', 50)], lams=[0.4, 0.6, 0.8, 1.1]),
    dict(ev='meteors seen by an observer in {c}', short='meteors seen', base='a 10-minute period', chg='An astronomer moves to a new observing site and wishes to test whether the mean number of meteors seen {d}.',
         subj='the mean number of meteors seen', obs=[('a one-hour period', 6), ('a 30-minute period', 3), ('a 20-minute period', 2)], big=[('a 2-hour period', 12), ('a 3-hour period', 18)], lams=[1.5, 2, 2.5]),
    dict(ev='customers arriving at a shop in {c}', short='customers arriving', base='a 5-minute period', chg='After an advertising campaign, the owner wishes to test whether the mean number of customers arriving {d}.',
         subj='the mean number of customers arriving', obs=[('a 15-minute period', 3), ('a 20-minute period', 4), ('a 10-minute period', 2)], big=[('a one-hour period', 12), ('a 2-hour period', 24)], lams=[1.5, 2, 2.5, 3]),
]
PDIRS = ('has decreased', 'has increased', 'has changed')


def ppv(l, x, side):
    return pcdf(l, x) if side == '<' else 1 - pcdf(l, x - 1)


def ppv_chk(l, x, side):
    a = ppv(l, x, side)
    b = pcdf_rec(l, x) if side == '<' else 1 - pcdf_rec(l, x - 1)
    return ok(a, b, 'ppv')


def pset(r, tails=TAILS, alphas=(0.1, 0.05, 0.025, 0.01), big=False, want=None):
    c = r.choice(HPCTX)
    tail = r.choice(tails)
    l0 = r.choice(c['lams'])
    per, mlt = r.choice(c['big'] if big else c['obs'])
    lam = round(l0 * mlt, 6)
    if (not big and lam > 15) or (big and lam < 15):
        return None
    alpha = r.choice([a for a in alphas if not (tail == '≠' and a == 0.025)])
    side = tail if tail != '≠' else r.choice('<>')
    ae = alpha / 2 if tail == '≠' else alpha
    rej, nrej = [], []
    sd = math.sqrt(lam)
    for x in range(0, int(lam + 6 * sd) + 3):
        if (side == '<' and x >= lam) or (side == '>' and x <= lam):
            continue
        if big:
            z = (x + 0.5 - lam) / sd if side == '<' else (x - 0.5 - lam) / sd
            v = Phi(z) if side == '<' else 1 - Phi(z)
        else:
            v = ppv(lam, x, side)
        if v < 0.0005 or v > 0.35 or abs(v - ae) < 0.12 * ae:
            continue
        (rej if v < ae else nrej).append((x, v))
    w = want if want is not None else r.random() < 0.5
    pool = (rej if w else nrej) or rej or nrej
    if not pool:
        return None
    x, v = r.choice(pool)
    if not big and not ppv_chk(lam, x, side):
        return None
    cty = city(r)
    d = PDIRS[TAILS.index(tail)]
    ev = c['ev'].format(c=cty)
    setup = f'The number of {ev} in {c["base"].format(c=cty)} has a Poisson distribution with mean {L(l0)}. ' + c['chg'].format(d=d)
    samp = f'In a randomly chosen {per.split(" ", 1)[1] if per.startswith(("a ", "an ")) else per}, the number of {c["short"]} is {x}.'
    return dict(c=c, tail=tail, side=side, l0=l0, lam=lam, per=per, x=x, pv=v, alpha=alpha, ae=ae, rej=v < ae, d=d, setup=setup, samp=samp,
                subj=c['subj'], hyp=hyp('λ', L(l0), tail), big=big, base=c['base'].format(c=cty))


def ptest_key(b, hyp_mark=True):
    k = (f'B1 {b["hyp"]} (or in terms of the mean for {b["per"]}); ' if hyp_mark else '') + f'B1 mean for {b["per"]} = {L(b["lam"])}; '
    if b['big']:
        cc = b['x'] + 0.5 if b['side'] == '<' else b['x'] - 0.5
        z = (cc - b['lam']) / math.sqrt(b['lam'])
        k += f'M1 N({L(b["lam"])}, {L(b["lam"])}) used; M1 continuity correction {num(cc)}; M1 z = ({num(cc)} − {L(b["lam"])})/√{L(b["lam"])} = {z3(z)}; A1 {p3(b["pv"])}'
    else:
        k += f'M1 {pv_s(b["side"], b["x"], "Po(" + L(b["lam"]) + ")")}' + (f' = 1 − P(X ≤ {b["x"] - 1})' if b['side'] == '>' else '') + f'; A1 {p3(b["pv"])}'
    k += f'; M1 compare with {num(b["ae"])}; A1 conclusion in context'
    return k


def ptest_ans(b):
    return f'{b["hyp"]}; X ~ {"N" if b["big"] else "Po"}' + (f'({L(b["lam"])}, {L(b["lam"])})' if b['big'] else f'({L(b["lam"])})') + \
        f'; {"P(X ≤ " if b["side"] == "<" else "P(X ≥ "}{b["x"]}) {"≈" if b["big"] else "="} {p3(b["pv"])} ' + ('<' if b['rej'] else '>') + f' {num(b["ae"])}. ' + concl(b['rej'], b['alpha'], b['subj'], b['d'])


# Normal-mean test contexts
HNCTX = [
    dict(pop='The masses of bags of rice filled by a machine', u='g', mus=[500, 750, 1000], sds=[4, 5, 6, 8, 10], chg='After the machine is serviced, the manager wishes to test whether the mean mass {d}.',
         dirs=PDIRS, subj='the mean mass', samp='A random sample of {n} bags filled after the service has mean mass {xb} g.', item='bags'),
    dict(pop='The times taken by employees in {c} to complete a task', u='minutes', mus=[24, 30, 36, 45], sds=[3, 4, 5, 6], chg='After a training session, the manager wishes to test whether the mean time {d}.',
         dirs=PDIRS, subj='the mean time', samp='{n} randomly chosen employees who attended the training have a mean time of {xb} minutes.', item='employees'),
    dict(pop='The lifetimes of batteries of a certain brand', u='hours', mus=[240, 300, 400, 500], sds=[20, 25, 30, 40], chg='A consumer group wishes to test whether the mean lifetime {d}.',
         dirs=('is less than this', 'is more than this', 'is different from this'), subj='the mean lifetime', samp='A random sample of {n} batteries has mean lifetime {xb} hours.', item='batteries'),
    dict(pop='The heights of sunflowers of a certain variety grown in {c}', u='cm', mus=[150, 165, 180, 200], sds=[12, 15, 18, 20], chg='A farmer uses a new fertiliser and wishes to test whether the mean height {d}.',
         dirs=PDIRS, subj='the mean height', samp='A random sample of {n} sunflowers grown with the fertiliser has mean height {xb} cm.', item='sunflowers'),
    dict(pop='The volumes of juice in cartons filled by a machine', u='ml', mus=[250, 330, 500, 1000], sds=[3, 4, 5, 8], chg='An inspector wishes to test whether the mean volume {d}.',
         dirs=('is less than this', 'is more than this', 'is different from this'), subj='the mean volume', samp='A random sample of {n} cartons has mean volume {xb} ml.', item='cartons'),
    dict(pop='The journey times on a bus route in {c}', u='minutes', mus=[35, 42, 50, 55], sds=[4, 5, 6], chg='After a new bus lane opens, the bus company wishes to test whether the mean journey time {d}.',
         dirs=PDIRS, subj='the mean journey time', samp='{n} randomly chosen journeys after the bus lane opens have a mean time of {xb} minutes.', item='journeys'),
    dict(pop='The masses of apples from an orchard', u='g', mus=[120, 140, 150, 160], sds=[12, 15, 18, 20], chg='After a change of irrigation method, the owner wishes to test whether the mean mass {d}.',
         dirs=PDIRS, subj='the mean mass of the apples', samp='A random sample of {n} apples picked after the change has mean mass {xb} g.', item='apples'),
    dict(pop='The reaction times of drivers in a simulator test', u='ms', mus=[220, 250, 280], sds=[25, 30, 40], chg='A researcher wishes to test whether the mean reaction time of drivers who have just used a phone {d}.',
         dirs=('is lower', 'is higher', 'is different'), subj='the mean reaction time of such drivers', samp='A random sample of {n} drivers who have just used a phone has mean reaction time {xb} ms.', item='drivers'),
]


def nset(r, tails=TAILS, ns=(20, 25, 30, 36, 40, 50, 60, 64, 80, 100), alphas=(0.1, 0.05, 0.025, 0.01), want=None, normal=None):
    c = r.choice(HNCTX)
    tail = r.choice(tails)
    alpha = r.choice([a for a in alphas if not (tail == '≠' and a == 0.025)])
    zcv = zc(alpha, 2 if tail == '≠' else 1)
    mu, sd, n = r.choice(c['mus']), r.choice(c['sds']), r.choice(ns)
    side = tail if tail != '≠' else r.choice('<>')
    w = want if want is not None else r.random() < 0.5
    se = sd / math.sqrt(n)
    dp = 1 if se >= 0.2 else 2
    for _ in range(30):
        z = r.uniform(zcv + 0.1, zcv + 1.3) if w else r.uniform(0.3, zcv - 0.1)
        xb = round(mu + (-1 if side == '<' else 1) * z * se, dp)
        zz = (xb - mu) / se
        if abs(abs(zz) - zcv) > 0.05 and abs(zz) > 0.2:
            break
    else:
        return None
    rej = abs(zz) > zcv
    cty = city(r)
    d = c['dirs'][TAILS.index(tail)]
    normal = (n < 30) if normal is None else normal
    pop = c['pop'].format(c=cty)
    setup = f'{pop} {"are normally distributed with" if normal else "have"} mean {mu} {c["u"]} and standard deviation {sd} {c["u"]}. ' + c['chg'].format(d=d)
    samp = c['samp'].format(n=n, xb=num(xb)) + ' Assume that the standard deviation is unchanged.'
    return dict(c=c, tail=tail, side=side, mu=mu, sd=sd, n=n, xb=xb, z=zz, zcv=zcv, alpha=alpha, rej=rej, d=d, setup=setup, samp=samp,
                subj=c['subj'], hyp=hyp('μ', num(mu), tail), normal=normal, u=c['u'])


def past(b, cty):
    pop = b['c']['pop'].format(c=cty)
    return f'In the past, {pop[0].lower() + pop[1:]} had mean {b["mu"]} {b["u"]}. ' + b['c']['chg'].format(d=b['d'])


def xbf(x):
    v = round(x, 4)
    return num(v) if abs(v - x) < 1e-9 else n4(x)


def ntest_key(b, hyp_mark=True):
    zsgn = MINUS if b['side'] == '<' else ''
    return (f'B1 {b["hyp"]}; ' if hyp_mark else '') + f'M1 z = ({num(b["xb"])} − {b["mu"]})/({b["sd"]}/√{b["n"]}); A1 {z3(b["z"])}; ' + \
        f'M1 compare with {zsgn}{b["zcv"]}' + (' (two-tailed)' if b['tail'] == '≠' else '') + '; A1 conclusion in context'


def ntest_ans(b):
    zsgn = MINUS if b['side'] == '<' else ''
    cmpw = ('<' if b['side'] == '<' else '>') if b['rej'] else ('>' if b['side'] == '<' else '<')
    return f'{b["hyp"]}; z = {z3(b["z"])} {cmpw} {zsgn}{b["zcv"]}. ' + concl(b['rej'], b['alpha'], b['subj'], b['d'])


# ---------------------------------------------------------------- ht1

ht1 = T('Null and alternative hypotheses, significance level, one- and two-tailed tests', 'null and alternative hypotheses', 'significance level', 'one- and two-tailed tests')
ht1.fixed('C1', (1, 2), [
    ('In a hypothesis test, the null hypothesis is', 'the hypothesis assumed to be true unless there is sufficient evidence against it', 'H₀ is assumed true; the test looks for evidence against it. [1]',
     ['the hypothesis that the sample result is correct', 'the hypothesis the researcher wants to prove', 'always a statement that a parameter has changed']),
    ('The significance level of a test is', 'the probability of rejecting H₀ when H₀ is true', 'Significance level = P(reject H₀ | H₀ true). [1]',
     ['the probability that H₀ is true', 'the probability that H₁ is true', 'the probability of accepting H₀ when it is false']),
    ('A test of H₀: p = 0.4 against H₁: p ≠ 0.4 is', 'a two-tailed test', 'H₁ allows values on both sides of 0.4. [1]', ['a one-tailed test', 'a test about the sample proportion', 'a test with no critical region']),
    ('The critical region of a test is', 'the set of values of the test statistic for which H₀ is rejected', '[1]', ['the set of values for which H₀ is accepted as true', 'the value of the test statistic observed', 'the region where H₁ is proved']),
    ('For a two-tailed test at the 5% significance level using a discrete distribution, the probability in each tail is compared with', '0.025', 'Half of 5% in each tail. [1]', ['0.05', '0.1', '0.01']),
    ('Hypotheses in a test are statements about', 'a population parameter', 'Hypotheses refer to p, λ or μ, not to sample statistics. [1]', ['a sample statistic', 'the observed value', 'the critical value']),
])
ht1.fixed('C2', (2, 3), [
    ('Explain why hypotheses are stated in terms of a population parameter and not the sample result.', 'The sample result is known; the test is about the unknown population value (p, λ or μ) from which the sample came, and whether the sample is consistent with the value in H₀.', 'B1 sample value known; B1 inference about population parameter [2]'),
    ('Explain the difference between a one-tailed and a two-tailed test.', 'A one-tailed test looks for a change in one specified direction (H₁ uses < or >); a two-tailed test looks for a change in either direction (H₁ uses ≠) and splits the significance level between both tails.', 'B1 one direction vs either; B1 significance level split between tails [2]'),
    ('Explain why "do not reject H₀" is preferred to "accept H₀" as a conclusion.', 'Failing to find evidence against H₀ does not show that H₀ is true; the sample is simply consistent with H₀.', 'B1 lack of evidence; B1 not proof that H₀ is true [2]'),
    ('Explain why a researcher should choose the hypotheses and significance level before collecting the data.', 'Choosing them after seeing the data could bias the test, e.g. choosing a tail or level that makes the result significant.', 'B1 avoids bias; B1 example of choosing tail or level to suit the data [2]'),
])


@ht1.add('C1', (1, 2, 3))
def ht1_c1(r, D):
    b = bset(r)
    if not b:
        return None
    p, t = pfm(b['p']), b['tail']
    other = [x for x in TAILS if x != t]
    sp = dn(Fr(b['x'], b['n']))
    ds = [hyp('p', p, other[0]), hyp('p', p, other[1]), f'{H0}: p {t} {p}, {H1}: p = {p}', hyp('p', sp, t)]
    return MCk(r, f'{b["setup"]} {b["samp"]} Which are the correct hypotheses for the test?', b['hyp'], ds,
               f'p is the population proportion; {H1} uses {t} because the suspicion is that {b["subj"]} {b["d"]}.')


@ht1.add('C1', (1, 2, 3))
def ht1_zc(r, D):
    a, tl = r.choice([(0.1, 1), (0.05, 1), (0.025, 1), (0.01, 1), (0.1, 2), (0.05, 2), (0.02, 2), (0.01, 2)])
    zv = zc(a, tl)
    b = nset(r, tails=('≠',) if tl == 2 else '<>', alphas=(a,))
    if not b:
        return None
    alln = ['1.282', '1.645', '1.96', '2.326', '2.576']
    sgn = MINUS if b['side'] == '<' and tl == 1 else ''
    corr = (f'±{num(zv)}' if tl == 2 else f'{sgn}{num(zv)}')
    ds = [(f'±{v}' if tl == 2 else f'{sgn}{v}') for v in alln if v != num(zv)]
    ds.append(f'{MINUS if not sgn else ""}{num(zv)}' if tl == 1 else num(zv))
    return MCk(r, f'{b["setup"]} The test is carried out at the {apc(a)} significance level using the normal distribution. State the critical value(s) of z.', corr, r.sample(ds, len(ds)),
               f'{"Two" if tl == 2 else "One"}-tailed at {apc(a)}: ' + (f'{apc(a / 2)} in each tail' if tl == 2 else f'{apc(a)} in one tail') + f', z = {corr}.')


@ht1.add('C2', (2, 3, 4), 'explain')
def ht1_err(r, D):
    b = bset(r, tails='<>' if D <= 3 else TAILS)
    if not b:
        return None
    nm = person(r)
    kind = r.choice(['sample', 'tail', 'accept', 'pmf'] + (['half'] if b['tail'] == '≠' else []))
    p = pfm(b['p'])
    if kind == 'sample':
        sp = n3(b['x'] / b['n'])
        claim = f'writes the hypotheses as {H0}: p = {sp}, {H1}: p {b["tail"]} {sp}'
        a = f'The hypotheses must use the population value given by the claim, not the sample proportion {sp}: {b["hyp"]}.'
        k = 'B1 hypotheses are about the population parameter; B1 correct hypotheses'
    elif kind == 'tail':
        wt = '>' if b['tail'] == '<' else '<'
        if b['tail'] == '≠':
            wt = '<'
        claim = f'writes {H1}: p {wt} {p}'
        a = f'{H1} must match the suspicion that {b["subj"]} {b["d"]}, so {H1}: p {b["tail"]} {p}' + (' (two-tailed).' if b['tail'] == '≠' else '.')
        k = 'B1 identifies wrong direction; B1 correct alternative hypothesis'
    elif kind == 'accept':
        claim = f'finds that the result is not significant and concludes: "This proves that {H0} is true."'
        a = f'Not rejecting {H0} only means there is insufficient evidence against it; it does not prove that {H0} is true. The conclusion should be "there is insufficient evidence that {b["subj"]} {b["d"]}".'
        k = 'B1 no proof that H₀ is true; B1 correct form of conclusion'
    elif kind == 'pmf':
        v = bpmf(b['n'], b['pf'], b['x'])
        claim = f'calculates P(X = {b["x"]}) = {p3(v)} and compares this with {num(b["ae"])}'
        a = f'The test must use the probability of a result at least as extreme as {b["x"]}: {pv_s(b["side"], b["x"], "")} = {p3(b["pv"])}, which is then compared with {num(b["ae"])}.'
        k = f'B1 tail probability needed, not P(X = {b["x"]}); B1 {pv_s(b["side"], b["x"], "")} = {p3(b["pv"])}'
    else:
        claim = f'compares {pv_s(b["side"], b["x"], "")} = {p3(b["pv"])} with {num(b["alpha"])}'
        a = f'The test is two-tailed, so the tail probability must be compared with half the significance level, {num(b["ae"])}.'
        k = 'B1 two-tailed; B1 compare with half the significance level'
    return Q(f'{b["setup"]} {b["samp"]} A test is carried out at the {apc(b["alpha"])} significance level. {nm} {claim}. Explain the mistake.', a, k)


@ht1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def ht1_decide(r, D):
    if D <= 2:
        b = bset(r, tails='<>')
        if not b:
            return None
        if D == 1:
            return Q(f'{b["setup"]} {b["samp"]} The hypotheses are {b["hyp"]}, and the test is at the {apc(b["alpha"])} significance level. Given that {pv_s(b["side"], b["x"], "")} = {p3(b["pv"])}, state the conclusion of the test.',
                     concl(b['rej'], b['alpha'], b['subj'], b['d']), f'M1 compare {p3(b["pv"])} with {num(b["alpha"])}; A1 conclusion in context')
        return Q(f'{b["setup"]} {b["samp"]} State suitable hypotheses for a test at the {apc(b["alpha"])} significance level and, given that {pv_s(b["side"], b["x"], "")} = {p3(b["pv"])}, state the conclusion.',
                 f'{b["hyp"]}. ' + concl(b['rej'], b['alpha'], b['subj'], b['d']), f'B1 {b["hyp"]}; M1 compare with {num(b["alpha"])}; A1 conclusion in context')
    if D == 3:
        b = bset(r, tails='≠')
        if not b:
            return None
        return Q(f'{b["setup"]} {b["samp"]} Given that {pv_s(b["side"], b["x"], "")} = {p3(b["pv"])}, state suitable hypotheses and carry out the test at the {apc(b["alpha"])} significance level.',
                 f'{b["hyp"]}. Two-tailed: {p3(b["pv"])} ' + ('<' if b['rej'] else '>') + f' {num(b["ae"])}. ' + concl(b['rej'], b['alpha'], b['subj'], b['d']),
                 f'B1 {b["hyp"]}; M1 compare with {num(b["ae"])} (half of {apc(b["alpha"])}); A1 conclusion in context')
    b = bset(r, tails=TAILS if D == 5 else '<>')
    if not b:
        return None
    m = b['pv'] * (2 if b['tail'] == '≠' else 1) * 100
    lead = f'{b["setup"]} {b["samp"]}'
    if D == 4:
        return Q(lead + f' State suitable hypotheses and find the set of significance levels, α%, for which {H0} would be rejected.', f'{b["hyp"]}; {pv_s(b["side"], b["x"], "")} = {p3(b["pv"])}, so reject {H0} if α > {n3(m)}.',
                 f'B1 {b["hyp"]}; M1 {pv_s(b["side"], b["x"], bdist(b))}; A1 {p3(b["pv"])}; A1 α > {n3(m)}')
    return Q(lead + f' Find the set of significance levels, α%, for which a test would conclude that {b["subj"]} {b["d"]}.',
             f'{pv_s(b["side"], b["x"], "")} = {p3(b["pv"])}; ' + (f'two-tailed, so α > 2 × {p3(b["pv"])} × 100 = {n3(m)}.' if b['tail'] == '≠' else f'α > {n3(m)}.'),
             f'B1 {b["hyp"]}; M1 {pv_s(b["side"], b["x"], bdist(b))}; A1 {p3(b["pv"])}' + ('; M1 doubled for two tails' if b['tail'] == '≠' else '') + f'; A1 α > {n3(m)}')


def ht1_c4(r, D):
    b = bset(r, tails='<>≠')
    if not b:
        return None
    intro = f'{b["setup"]} {b["samp"]}'
    tw = 'two-tailed' if b['tail'] == '≠' else 'one-tailed'
    parts = [
        P(f'Explain why a {tw} test is appropriate.', (f'The suspicion is only that {b["subj"]} {b["d"]}, in one direction.' if b['tail'] != '≠' else f'A change in either direction is of interest ({b["subj"]} {b["d"]}).'), 'B1'),
        P(f'Carry out the test at the {apc(b["alpha"])} significance level.', btest_ans(b), btest_key(b)),
        P('Explain what is meant by the significance level in this context.', f'The probability, {num(b["alpha"])}, of concluding that {b["subj"]} {b["d"]} when in fact p = {pfm(b["p"])}.',
          'B1 probability of rejecting H₀ when true; B1 in context'),
        P('State one assumption needed for the binomial model to be valid.', f'The {b["c"]["unit"]} are independent of each other (with the same probability of success for each).', 'B1'),
    ]
    return cmp_(r, intro, parts, k=(2, 3, 4))


ht1.add('C4', (2, 3, 4, 5))(ht1_c4)


# ---------------------------------------------------------------- ht2

ht2 = T('Hypothesis tests using the binomial and Poisson distributions', 'hypothesis tests using the binomial', 'Poisson distributions')
ht2.fixed('C1', (1, 2), [
    ('In a test of H₀: p = 0.3 against H₁: p > 0.3 with X ~ B(20, 0.3), 10 successes are observed. The probability compared with the significance level is', 'P(X ≥ 10)', 'Values at least as extreme as the observed value. [1]', ['P(X = 10)', 'P(X ≤ 10)', 'P(X > 10)']),
    ('In a test of H₀: λ = 4 against H₁: λ < 4 with X ~ Po(4), 1 event is observed. The probability compared with the significance level is', 'P(X ≤ 1)', '[1]', ['P(X = 1)', 'P(X ≥ 1)', 'P(X < 1)']),
    ('The mean number of events in 1 hour is 2.5. Under H₀, the distribution of the number of events in 4 hours is', 'Po(10)', '2.5 × 4. [1]', ['Po(2.5)', 'Po(0.625)', 'B(4, 2.5)']),
    ('For a discrete test statistic the actual significance level of a test is usually', 'less than the stated significance level', 'The critical region is chosen so its probability does not exceed the stated level. [1]', ['exactly equal to the stated level', 'greater than the stated level', 'equal to 0.5']),
])
ht2.fixed('C2', (2, 3), [
    ('Explain why, for a binomial test, the probability of the observed value or a more extreme value is used rather than the probability of the observed value alone.', 'Any single value can have a small probability; the test asks how likely a result at least as extreme as the observed one is when H₀ is true.', 'B1 single values have small probabilities; B1 tail probability measures extremeness [2]'),
    ('Explain why the actual significance level of a test based on the Poisson distribution is often not exactly 5%.', 'The distribution is discrete, so the tail probabilities jump in steps and there is usually no critical region with probability exactly 0.05.', 'B1 discrete; B1 probabilities in steps [2]'),
])


@ht2.add('C1', (1, 2, 3))
def ht2_c1(r, D):
    b = bset(r, tails='<>', ns=(8, 10, 12, 15))
    if not b:
        return None
    n, pf, x, s = b['n'], b['pf'], b['x'], b['side']
    alt = [bpmf(n, pf, x), bpv(n, pf, x + (1 if s == '<' else -1), s) if 0 <= x + (1 if s == '<' else -1) <= n else 1 - b['pv'], 1 - b['pv'], bpv(n, pf, x + (-1 if s == '<' else 1), s)]
    return MCk(r, f'{b["setup"]} {b["samp"]} The hypotheses are {b["hyp"]}. Find the probability that is compared with the significance level.', p3(b['pv']), [p3(v) for v in alt],
               f'{pv_s(s, x, bdist(b))} = {p3(b["pv"])}.')


@ht2.add('C1', (1, 2, 3))
def ht2_po_c1(r, D):
    b = pset(r, tails='<>')
    if not b:
        return None
    m_ = b['lam'] / b['l0']
    alt = [L(b['l0']), L(round(b['lam'] * 2, 6)), L(round(b['l0'] / m_, 6)), L(round(b['lam'] + b['l0'], 6))]
    return MCk(r, f'{b["setup"]} {b["samp"]} State the distribution of the number in {b["per"]} under {H0}.', f'Po({L(b["lam"])})', [f'Po({a})' for a in alt],
               f'Mean scaled to {b["per"]}: {L(b["l0"])} × {num(round(b["lam"] / b["l0"], 6))} = {L(b["lam"])}.')


@ht2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def ht2_calc(r, D):
    if D <= 2:
        b = bset(r, tails='<>', ns=(8, 10, 12, 15) if D == 1 else (15, 16, 18, 20, 24, 25))
        if not b:
            return None
        return Q(f'{b["setup"]} {b["samp"]} Test at the {apc(b["alpha"])} significance level whether {b["subj"]} {b["d"]}.', btest_ans(b), btest_key(b))
    if D == 3:
        b = pset(r, tails='<>')
        if not b:
            return None
        return Q(f'{b["setup"]} {b["samp"]} Carry out the test at the {apc(b["alpha"])} significance level.', ptest_ans(b), ptest_key(b))
    if D == 4:
        b = r.choice([bset(r, tails='≠'), pset(r, tails='≠')])
        if not b:
            return None
        if 'lam' in b:
            return Q(f'{b["setup"]} {b["samp"]} Carry out the test at the {apc(b["alpha"])} significance level.', ptest_ans(b), ptest_key(b))
        return Q(f'{b["setup"]} {b["samp"]} Test at the {apc(b["alpha"])} significance level whether {b["subj"]} {b["d"]}.', btest_ans(b), btest_key(b))
    b = pset(r, tails='<>', big=True)
    if not b:
        return None
    return Q(f'{b["setup"]} {b["samp"]} Use a suitable approximating distribution to carry out the test at the {apc(b["alpha"])} significance level.', ptest_ans(b), ptest_key(b) + '; B1 justification λ > 15')


def bcr(n, p, side, a):
    """Critical region boundary for B(n, p): returns (c, size, next) or None."""
    if side == '<':
        c = -1
        while c + 1 <= n and bcdf(n, p, c + 1) <= a:
            c += 1
        if c < 0:
            return None
        return c, bcdf(n, p, c), bcdf(n, p, c + 1)
    c = n + 1
    while c - 1 >= 0 and 1 - bcdf(n, p, c - 2) <= a:
        c -= 1
    if c > n:
        return None
    return c, 1 - bcdf(n, p, c - 1), 1 - bcdf(n, p, c - 2)


def pcr(l, side, a):
    if side == '<':
        c = -1
        while pcdf(l, c + 1) <= a:
            c += 1
        if c < 0:
            return None
        return c, pcdf(l, c), pcdf(l, c + 1)
    c = 0
    while 1 - pcdf(l, c - 1) > a:
        c += 1
    if not ok(1 - pcdf(l, c - 1), 1 - pcdf_rec(l, c - 1), 'pcr'):
        return None
    return c, 1 - pcdf(l, c - 1), 1 - pcdf(l, c - 2)


def cr_text(side, c):
    return f'X ≤ {c}' if side == '<' else f'X ≥ {c}'


def cr_key(side, c, size, nxt, ae):
    if side == '<':
        return f'M1 P(X ≤ {c}) = {p4(size)} ≤ {num(ae)}; M1 P(X ≤ {c + 1}) = {p4(nxt)} > {num(ae)}; A1 {cr_text(side, c)}'
    return f'M1 P(X ≥ {c}) = {p4(size)} ≤ {num(ae)}; M1 P(X ≥ {c - 1}) = {p4(nxt)} > {num(ae)}; A1 {cr_text(side, c)}'


@ht2.add('C3', (2, 3, 4, 5), 'numerical')
def ht2_cr(r, D):
    if D <= 4:
        use_p = D >= 3 and r.random() < 0.6
        b = pset(r, tails='<>') if use_p else bset(r, tails='<>', ns=(10, 12, 15, 16, 18, 20, 25))
        if not b:
            return None
        cr = pcr(b['lam'], b['side'], b['alpha']) if use_p else bcr(b['n'], b['pf'], b['side'], b['alpha'])
        if not cr:
            return None
        c, size, nxt = cr
        lead = (f'{b["setup"]} The number in a randomly chosen {b["per"].split(" ", 1)[1]} is to be used for the test.' if use_p else
                f'{b["setup"]} A random sample of {b["n"]} {b["c"]["unit"]} is to be used for the test.')
        if b.get('c', {}).get('unit') == 'tosses' or (not use_p and b['c']['unit'] in ('throws', 'shots', 'questions')):
            lead = f'{b["setup"]} The test is to be based on {b["n"]} {b["c"]["unit"]}.'
        q = f' Using a {apc(b["alpha"])} significance level, find the critical region' + (' and state the probability of a Type I error.' if D == 4 else '.')
        a = cr_text(b['side'], c) + (f'; P(Type I error) = {p3(size)}' if D == 4 else '')
        k = f'B1 {b["hyp"]}; ' + cr_key(b['side'], c, size, nxt, b['alpha']) + (f'; B1 {p3(size)}' if D == 4 else '')
        return Q(lead + q, a, k)
    b = bset(r, tails='≠', ns=(15, 16, 18, 20, 24, 25), alphas=(0.1, 0.05))
    if not b:
        return None
    lo = bcr(b['n'], b['pf'], '<', b['ae'])
    hi = bcr(b['n'], b['pf'], '>', b['ae'])
    if not lo or not hi:
        return None
    lead = f'{b["setup"]} The test is to be based on {b["n"]} {b["c"]["unit"]} and carried out at the {apc(b["alpha"])} significance level.'
    return Q(lead + ' Find the critical region and its actual significance level.', f'X ≤ {lo[0]} or X ≥ {hi[0]}; actual significance level = {p3(lo[1] + hi[1])}',
             f'B1 {b["hyp"]}; B1 {num(b["ae"])} in each tail; ' + cr_key('<', lo[0], lo[1], lo[2], b['ae']) + '; ' + cr_key('>', hi[0], hi[1], hi[2], b['ae']) + f'; B1 {p4(lo[1])} + {p4(hi[1])} = {p3(lo[1] + hi[1])}')


@ht2.add('C2', (2, 3, 4), 'explain')
def ht2_err(r, D):
    b = pset(r, tails='<>')
    if not b:
        return None
    nm = person(r)
    kind = r.choice(['scale', 'pmf', 'side'])
    if kind == 'scale':
        wrong = ppv(b['l0'], b['x'], b['side'])
        claim = f'uses X ~ Po({L(b["l0"])}) and finds {pv_s(b["side"], b["x"], "")} = {p3(wrong)}'
        a = f'The mean must be scaled to {b["per"]}: X ~ Po({L(b["lam"])}), giving {pv_s(b["side"], b["x"], "")} = {p3(b["pv"])}. ' + concl(b['rej'], b['alpha'], b['subj'], b['d'])
        k = f'B1 mean should be {L(b["lam"])}; M1 {p3(b["pv"])}; A1 conclusion'
    elif kind == 'pmf':
        wrong = ppmf(b['lam'], b['x'])
        claim = f'calculates P(X = {b["x"]}) = {p3(wrong)} using Po({L(b["lam"])}) and compares it with {num(b["ae"])}'
        a = f'A tail probability is needed: {pv_s(b["side"], b["x"], "")} = {p3(b["pv"])}. ' + concl(b['rej'], b['alpha'], b['subj'], b['d'])
        k = 'B1 tail probability needed; M1 ' + p3(b['pv']) + '; A1 conclusion'
    else:
        x, s = b['x'], b['side']
        wrong = pcdf(b['lam'], x - 1) if s == '<' else 1 - pcdf(b['lam'], x)
        claim = f'calculates ' + (f'P(X < {x})' if s == '<' else f'P(X > {x})') + f' = {p3(wrong)} using Po({L(b["lam"])})'
        a = f'The observed value must be included: {pv_s(s, x, "")} = {p3(b["pv"])}. ' + concl(b['rej'], b['alpha'], b['subj'], b['d'])
        k = f'B1 observed value {x} must be included; M1 {p3(b["pv"])}; A1 conclusion'
    return Q(f'{b["setup"]} {b["samp"]} The test is at the {apc(b["alpha"])} significance level. {nm} {claim}. Identify the error and give the correct conclusion.', a, k)


def ht2_c4(r, D):
    use_p = r.random() < 0.5
    b = pset(r, tails='<>') if use_p else bset(r, tails='<>', ns=(12, 15, 16, 18, 20, 25))
    if not b:
        return None
    cr = pcr(b['lam'], b['side'], b['alpha']) if use_p else bcr(b['n'], b['pf'], b['side'], b['alpha'])
    if not cr:
        return None
    c, size, nxt = cr
    inside = (b['x'] <= c) if b['side'] == '<' else (b['x'] >= c)
    if inside != b['rej']:
        ok(1, 0, 'cr vs pv')
        return None
    if use_p:
        intro = f'{b["setup"]} The test uses the number in a randomly chosen {b["per"].split(" ", 1)[1]} and a {apc(b["alpha"])} significance level.'
    else:
        intro = f'{b["setup"]} The test uses {b["n"]} {b["c"]["unit"]} and a {apc(b["alpha"])} significance level.'
    parts = [
        P('State the null and alternative hypotheses.', b['hyp'], 'B1'),
        P('Find the critical region.', cr_text(b['side'], c), cr_key(b['side'], c, size, nxt, b['alpha'])),
        P(f'The observed value is {b["x"]}. State the conclusion of the test.', concl(b['rej'], b['alpha'], b['subj'], b['d']), f'M1 {b["x"]} {"in" if inside else "not in"} critical region; A1 conclusion in context'),
        P('State the probability of a Type I error.', p3(size), f'B1 P({cr_text(b["side"], c)}) = {p3(size)}'),
    ]
    return cmp_(r, intro, parts, k=(3, 4), deps={2: [1], 3: [1]})


ht2.add('C4', (2, 3, 4, 5))(ht2_c4)


# ---------------------------------------------------------------- ht3

ht3 = T('Hypothesis tests for a population mean using the normal distribution', 'hypothesis tests for a population mean', 'normal distribution')
ht3.fixed('C1', (1, 2), [
    ('In a test for a population mean with known σ, the test statistic is', 'z = (x̄ − μ₀)/(σ/√n)', 'The sample mean has standard deviation σ/√n. [1]', ['z = (x̄ − μ₀)/σ', 'z = (x̄ − μ₀)/(σ²/n)', 'z = (x̄ − μ₀)/(σ/n)']),
    ('A one-tailed test of H₀: μ = 50 against H₁: μ > 50 at the 5% level rejects H₀ if', 'z > 1.645', '[1]', ['z > 1.96', 'z < −1.645', '|z| > 1.645']),
    ('A two-tailed test for a mean at the 1% significance level rejects H₀ if', '|z| > 2.576', '0.5% in each tail. [1]', ['|z| > 2.326', 'z > 2.576', '|z| > 1.96']),
    ('A test for a mean of a non-normal population using a large sample relies on', 'the central limit theorem', 'x̄ is approximately normal for large n. [1]', ['the Poisson approximation', 'the population being symmetric', 'the sample being small']),
])
ht3.fixed('C2', (2, 3), [
    ('Explain why a test for a population mean can be carried out using a large sample even when the population is not normally distributed.', 'By the central limit theorem the sample mean is approximately normally distributed when n is large, whatever the population distribution.', 'B1 CLT; B1 applies to the sample mean for large n [2]'),
    ('Explain why, when σ is unknown and the sample is large, the unbiased estimate s² can be used in place of σ².', 'For a large sample s² is a reliable estimate of σ², so (x̄ − μ)/(s/√n) is approximately N(0, 1).', 'B1 large sample so s² close to σ²; B1 test statistic approximately standard normal [2]'),
])


@ht3.add('C1', (1, 2, 3))
def ht3_c1(r, D):
    b = nset(r, tails='<>≠')
    if not b:
        return None
    mu, sd, n, xb = b['mu'], b['sd'], b['n'], b['xb']
    z = b['z']
    ds = [n3((xb - mu) / sd), n3((xb - mu) / (sd / n)), n3((xb - mu) / (sd * sd / n)), n3((xb - mu) * math.sqrt(n) / (sd * sd))]
    return MCk(r, f'{b["setup"]} {b["samp"]} Find the value of the test statistic z.', n3(z), ds, f'z = ({num(xb)} − {mu})/({sd}/√{n}) = {n3(z)}.')


@ht3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def ht3_calc(r, D):
    if D <= 2:
        b = nset(r, tails='<>', ns=(9, 10, 12, 16, 20, 25) if D == 1 else (16, 20, 25, 30, 36, 40))
        if not b:
            return None
        if D == 1:
            return Q(f'{b["setup"]} {b["samp"]} The hypotheses are {b["hyp"]}. Calculate the value of the test statistic and complete the test at the {apc(b["alpha"])} significance level.', ntest_ans(b), ntest_key(b, False))
        return Q(f'{b["setup"]} {b["samp"]} Test at the {apc(b["alpha"])} significance level whether {b["subj"]} {b["d"]}.', ntest_ans(b), ntest_key(b))
    if D == 3:
        b = nset(r, tails='≠')
        if not b:
            return None
        return Q(f'{b["setup"]} {b["samp"]} Test at the {apc(b["alpha"])} significance level whether {b["subj"]} {b["d"]}.', ntest_ans(b), ntest_key(b))
    if D == 4:
        b = nset(r, tails=TAILS, ns=(40, 50, 60, 80, 100), normal=False)
        if not b:
            return None
        n, mu = b['n'], b['mu']
        # build a sample with the required mean and roughly the stated sd
        rng_sd = b['sd'] * r.uniform(0.85, 1.15)
        sx = round(b['xb'] * n, 1)
        s2 = rng_sd ** 2
        sx2 = round(s2 * (n - 1) + sx * sx / n, 1)
        s2 = ubv(n, sx, sx2)
        xb = sx / n
        z = (xb - mu) / math.sqrt(s2 / n)
        if abs(abs(z) - b['zcv']) < 0.05:
            return None
        rej = abs(z) > b['zcv'] and ((z < 0) == (b['side'] == '<'))
        cty = city(r)
        lead = past(b, cty)
        stem = f'{lead} For a random sample of {n} {b["c"]["item"]}, the values x {b["u"]} satisfy Σx = {num(sx)} and Σx² = {num(sx2)}. Test at the {apc(b["alpha"])} significance level whether {b["subj"]} {b["d"]}.'
        zsgn = MINUS if b['side'] == '<' else ''
        return Q(stem, f'x̄ = {xbf(xb)}, s² = {n4(s2)}; {b["hyp"]}; z = {z3(z)}; compare with {zsgn}{b["zcv"]}. ' + concl(rej, b['alpha'], b['subj'], b['d']),
                 f'B1 x̄ = {xbf(xb)}; M1 s² = ({num(sx2)} − {num(sx)}²/{n})/{n - 1}; A1 {n4(s2)}; B1 {b["hyp"]}; M1 z = ({xbf(xb)} − {mu})/√({n4(s2)}/{n}); A1 {z3(z)}; M1 compare with {zsgn}{b["zcv"]}; A1 conclusion in context')
    b = nset(r, tails='<>', normal=True)
    if not b:
        return None
    se = b['sd'] / math.sqrt(b['n'])
    cv = b['mu'] - b['zcv'] * se if b['side'] == '<' else b['mu'] + b['zcv'] * se
    return Q(f'{b["setup"]} A random sample of {b["n"]} {b["c"]["item"]} is to be taken. The hypotheses are {b["hyp"]}. Find the set of values of the sample mean for which {H0} is rejected at the {apc(b["alpha"])} significance level.',
             ('x̄ < ' if b['side'] == '<' else 'x̄ > ') + n4(cv), f'M1 (x̄ − {b["mu"]})/({b["sd"]}/√{b["n"]}) = {MINUS if b["side"] == "<" else ""}{b["zcv"]}; A1 critical value {n4(cv)}; A1 ' + ('x̄ < ' if b['side'] == '<' else 'x̄ > ') + n4(cv))


@ht3.add('C2', (2, 3, 4), 'explain')
def ht3_err(r, D):
    b = nset(r, tails=TAILS)
    if not b:
        return None
    nm = person(r)
    kind = r.choice(['sigma', 'crit'] if b['tail'] == '≠' else ['sigma', 'var'])
    if kind == 'sigma':
        wz = (b['xb'] - b['mu']) / b['sd']
        if abs(wz - b['z']) < 0.01:
            return None
        claim = f'calculates z = ({num(b["xb"])} − {b["mu"]})/{b["sd"]} = {z3(wz)}'
        a = f'The standard deviation of the sample mean is σ/√n, so z = ({num(b["xb"])} − {b["mu"]})/({b["sd"]}/√{b["n"]}) = {z3(b["z"])}. ' + concl(b['rej'], b['alpha'], b['subj'], b['d'])
        k = f'B1 should divide by σ/√n; M1 z = {z3(b["z"])}; A1 conclusion'
    elif kind == 'var':
        wz = (b['xb'] - b['mu']) / (b['sd'] ** 2 / b['n'])
        if abs(wz - b['z']) < 0.01:
            return None
        claim = f'calculates z = ({num(b["xb"])} − {b["mu"]})/({b["sd"]}²/{b["n"]}) = {z3(wz)}'
        a = f'The variance σ²/n has been used instead of the standard deviation σ/√n; z = {z3(b["z"])}. ' + concl(b['rej'], b['alpha'], b['subj'], b['d'])
        k = f'B1 square root of σ²/n needed; M1 z = {z3(b["z"])}; A1 conclusion'
    else:
        wc = zc(b['alpha'], 1)
        claim = f'compares z = {z3(b["z"])} with the critical value {"" if b["side"] == ">" else MINUS}{wc}'
        a = f'The test is two-tailed, so {apc(b["alpha"] / 2)} is in each tail and the critical values are ±{b["zcv"]}. ' + concl(b['rej'], b['alpha'], b['subj'], b['d'])
        if (abs(b['z']) > wc) == b['rej']:
            return None
        k = f'B1 two-tailed critical value ±{b["zcv"]}; A1 conclusion'
    return Q(f'{b["setup"]} {b["samp"]} The test is at the {apc(b["alpha"])} significance level. {nm} {claim}. Explain the error and state the correct conclusion.', a, k)


def ht3_c4(r, D):
    b = nset(r, tails='<>', ns=(50, 60, 80, 100, 120), normal=False, alphas=(0.05, 0.1))
    if not b:
        return None
    n, mu = b['n'], b['mu']
    sx = round(b['xb'] * n, 1)
    s2t = (b['sd'] * r.uniform(0.85, 1.15)) ** 2
    sx2 = round(s2t * (n - 1) + sx * sx / n, 1)
    s2 = ubv(n, sx, sx2)
    xb = sx / n
    z = (xb - mu) / math.sqrt(s2 / n)
    zcv = b['zcv']
    rej = abs(z) > zcv and ((z < 0) == (b['side'] == '<'))
    if abs(abs(z) - zcv) < 0.05 or abs(abs(z) - 2.326) < 0.05:
        return None
    rej1 = abs(z) > 2.326 and ((z < 0) == (b['side'] == '<'))
    cty = city(r)
    lead = past(b, cty)
    intro = f'{lead} For a random sample of {n} {b["c"]["item"]}, the values x {b["u"]} satisfy Σx = {num(sx)} and Σx² = {num(sx2)}.'
    zsgn = MINUS if b['side'] == '<' else ''
    parts = [
        P('Find unbiased estimates of the population mean and variance.', f'{xbf(xb)}, {n4(s2)}', f'B1 {xbf(xb)}; M1 divisor {n - 1}; A1 {n4(s2)}'),
        P(f'Test at the {apc(b["alpha"])} significance level whether {b["subj"]} {b["d"]}.', f'{b["hyp"]}; z = {z3(z)}; ' + concl(rej, b['alpha'], b['subj'], b['d']),
          f'B1 {b["hyp"]}; M1 z = ({xbf(xb)} − {mu})/√({n4(s2)}/{n}); A1 {z3(z)}; M1 compare with {zsgn}{zcv}; A1 conclusion in context'),
        P('Explain why it is not necessary to know that the population is normally distributed.', f'n = {n} is large, so by the central limit theorem x̄ is approximately normal.', 'B1 large n; B1 CLT'),
        P('State, with a reason, whether the conclusion would be the same at the 1% significance level.', f'Critical value {zsgn}2.326; z = {z3(z)}, so ' + ('reject H₀' if rej1 else 'do not reject H₀') + ('; the same conclusion.' if rej1 == rej else '; a different conclusion.'),
          'M1 compare with 2.326; A1 correct comparison'),
    ]
    return cmp_(r, intro, parts, k=(2, 3, 4), deps={2: [1], 3: [1]})


ht3.add('C4', (2, 3, 4, 5))(ht3_c4)


# ---------------------------------------------------------------- ht4

ht4 = T('Type I and Type II errors and their probabilities', 'type i and type ii errors', 'probabilities')
ht4.fixed('C1', (1, 2), [
    ('A Type I error occurs when', 'H₀ is rejected when it is true', '[1]', ['H₀ is not rejected when it is false', 'H₁ is rejected when it is true', 'the test statistic is calculated incorrectly']),
    ('A Type II error occurs when', 'H₀ is not rejected when it is false', '[1]', ['H₀ is rejected when it is true', 'H₀ is rejected when it is false', 'the significance level is too small']),
    ('For a test using a continuous test statistic, the probability of a Type I error equals', 'the significance level', '[1]', ['1 − the significance level', 'the probability of a Type II error', '0.5']),
    ('Reducing the significance level of a test (with the same sample size) will usually', 'increase the probability of a Type II error', 'A smaller critical region makes failing to reject a false H₀ more likely. [1]',
     ['increase the probability of a Type I error', 'decrease the probability of a Type II error', 'not change either error probability']),
])
ht4.fixed('C2', (2, 3), [
    ('Explain why the probability of a Type II error can only be calculated if a particular value of the parameter is given.', 'A Type II error occurs when H₀ is false; its probability depends on the actual (true) value of the parameter, which H₁ does not specify.', 'B1 H₁ gives a range of values; B1 probability depends on the true value [2]'),
    ('Explain how the probability of a Type II error can be reduced without increasing the probability of a Type I error.', 'Increase the sample size: the sampling distribution becomes narrower, so the test is more likely to detect a real change.', 'B1 larger sample; B1 reason [2]'),
])


def err_ctx(r):
    k = r.random()
    if k < 0.4:
        b = bset(r, tails='<>')
    elif k < 0.7:
        b = pset(r, tails='<>')
    else:
        b = nset(r, tails='<>')
    return b


@ht4.add('C1', (1, 2, 3))
def ht4_c1(r, D):
    b = err_ctx(r)
    if not b:
        return None
    aux = b['d'].split(' ')[0]
    if aux not in ('has', 'is', 'does') or b['subj'] in ('the coin', 'the die') or ('c' in b and b['c'].get('subj') == '{nm}'):
        return None
    which = r.choice(['I', 'II'])
    opt_I = f'Concluding that {b["subj"]} {b["d"]}, when in fact it {aux} not'
    opt_II = f'Concluding that there is no evidence that {b["subj"]} {b["d"]}, when in fact it {aux}'
    opt_3 = f'Concluding that {b["subj"]} {b["d"]}, when in fact it {aux}'
    opt_4 = f'Concluding that there is no evidence that {b["subj"]} {b["d"]}, when in fact it {aux} not'
    corr = opt_I if which == 'I' else opt_II
    ds = [o for o in (opt_I, opt_II, opt_3, opt_4) if o != corr]
    return MCk(r, f'{b["setup"]} Which statement describes a Type {which} error in this context?', corr, ds,
               f'Type I: rejecting a true {H0}; Type II: not rejecting a false {H0}.')


def bsize_t2(r, b, D):
    """Binomial CR with probability of Type II for a stated alternative."""
    cr = bcr(b['n'], b['pf'], b['side'], b['alpha'])
    if not cr:
        return None
    c, size, nxt = cr
    pf = b['pf']
    cand = [round(pf + d_, 2) for d_ in ((-0.1, -0.15, -0.2) if b['side'] == '<' else (0.1, 0.15, 0.2))]
    cand = [q for q in cand if 0.02 <= q <= 0.95]
    if not cand:
        return None
    p1 = r.choice(cand)
    t2 = 1 - bcdf(b['n'], p1, c) if b['side'] == '<' else bcdf(b['n'], p1, c - 1)
    chk = sum(bpmf(b['n'], p1, i) for i in (range(c + 1, b['n'] + 1) if b['side'] == '<' else range(0, c)))
    if not ok(t2, chk, 't2'):
        return None
    return c, size, nxt, p1, t2


@ht4.add('C3', (1, 2, 3, 4, 5), 'numerical')
def ht4_calc(r, D):
    if D == 1:
        b = nset(r, tails=TAILS)
        if not b:
            return None
        return MCk(r, f'{b["setup"]} A random sample of {b["n"]} {b["c"]["item"]} is used to test {b["hyp"]} at the {apc(b["alpha"])} significance level. State the probability of a Type I error.',
                   num(b['alpha']), [num(round(1 - b['alpha'], 4)), num(round(b['alpha'] / 2, 4)), num(round(b['alpha'] * 2, 4)), num(round(b['alpha'] + 0.05, 4))],
                   'For a continuous test statistic, P(Type I error) = significance level.')
    if D == 2:
        if r.random() < 0.5:
            b = bset(r, tails='<>', ns=(10, 12, 15, 20))
            if not b:
                return None
            cr = bcr(b['n'], b['pf'], b['side'], b['alpha'])
            if not cr:
                return None
            c, size, _ = cr
            return Q(f'{b["setup"]} The test is based on {b["n"]} {b["c"]["unit"]}, and {H0} is rejected if {cr_text(b["side"], c)}, where X is the number of successes. Find the probability of a Type I error.',
                     p3(size), f'M1 P({cr_text(b["side"], c)}) with {bdist(b)}; A1 {p3(size)}')
        b = pset(r, tails='<>')
        if not b:
            return None
        cr = pcr(b['lam'], b['side'], b['alpha'])
        if not cr:
            return None
        c, size, _ = cr
        return Q(f'{b["setup"]} The test uses the number, X, in a randomly chosen {b["per"].split(" ", 1)[1]}; {H0} is rejected if {cr_text(b["side"], c)}. Find the probability of a Type I error.',
                 p3(size), f'B1 Po({L(b["lam"])}); M1 P({cr_text(b["side"], c)}); A1 {p3(size)}')
    if D == 3:
        b = pset(r, tails='<>')
        if not b:
            return None
        cr = pcr(b['lam'], b['side'], b['alpha'])
        if not cr:
            return None
        c, size, _ = cr
        mlt = b['lam'] / b['l0']
        l1 = round(b['l0'] * (r.choice([0.4, 0.5, 0.6]) if b['side'] == '<' else r.choice([1.5, 1.8, 2])), 2)
        lam1 = round(l1 * mlt, 6)
        t2 = 1 - pcdf(lam1, c) if b['side'] == '<' else pcdf(lam1, c - 1)
        if not ok(t2, 1 - pcdf_rec(lam1, c) if b['side'] == '<' else pcdf_rec(lam1, c - 1), 't2p'):
            return None
        return Q(f'{b["setup"]} The test uses the number, X, in a randomly chosen {b["per"].split(" ", 1)[1]}; {H0} is rejected if {cr_text(b["side"], c)}. Find the probability of a Type I error, and the probability of a Type II error if in fact the mean for {b["base"]} is {L(l1)}.',
                 f'P(Type I) = {p3(size)}; P(Type II) = {p3(t2)}', f'M1 P({cr_text(b["side"], c)}) with Po({L(b["lam"])}); A1 {p3(size)}; B1 Po({L(lam1)}); M1 P(' + (f'X ≥ {c + 1}' if b['side'] == '<' else f'X ≤ {c - 1}') + f'); A1 {p3(t2)}')
    if D == 4:
        b = bset(r, tails='<>', ns=(15, 16, 18, 20, 24, 25))
        if not b:
            return None
        res = bsize_t2(r, b, D)
        if not res:
            return None
        c, size, nxt, p1, t2 = res
        return Q(f'{b["setup"]} The test is based on {b["n"]} {b["c"]["unit"]} at the {apc(b["alpha"])} significance level. Find the critical region, and find the probability of a Type II error if in fact p = {num(p1)}.',
                 f'{cr_text(b["side"], c)}; P(Type II) = {p3(t2)}', cr_key(b['side'], c, size, nxt, b['alpha']) + f'; M1 P(' + (f'X ≥ {c + 1}' if b['side'] == '<' else f'X ≤ {c - 1}') + f') with B({b["n"]}, {num(p1)}); A1 {p3(t2)}')
    b = nset(r, tails='<>', normal=True)
    if not b:
        return None
    se = b['sd'] / math.sqrt(b['n'])
    cv = b['mu'] - b['zcv'] * se if b['side'] == '<' else b['mu'] + b['zcv'] * se
    shift = r.choice([1.0, 1.5, 2.0, 2.5]) * se
    dpl = 1 if se >= 0.5 else 2
    mu1 = round(b['mu'] - shift if b['side'] == '<' else b['mu'] + shift, dpl)
    t2 = 1 - Phi((cv - mu1) / se) if b['side'] == '<' else Phi((cv - mu1) / se)
    return Q(f'{b["setup"]} A random sample of {b["n"]} {b["c"]["item"]} is used to test {b["hyp"]} at the {apc(b["alpha"])} significance level. Find the probability of a Type II error if in fact μ = {num(mu1)}.',
             n3(t2), f'M1 critical value {b["mu"]} {"−" if b["side"] == "<" else "+"} {b["zcv"]} × {b["sd"]}/√{b["n"]}; A1 {n4(cv)}; M1 P(x̄ {"≥" if b["side"] == "<" else "≤"} {n4(cv)} | μ = {num(mu1)}); M1 z = ({n4(cv)} − {num(mu1)})/({b["sd"]}/√{b["n"]}); A1 {n3(t2)}')


@ht4.add('C2', (2, 3, 4), 'explain')
def ht4_err(r, D):
    b = bset(r, tails='<>', ns=(12, 15, 16, 18, 20, 25))
    if not b:
        return None
    cr = bcr(b['n'], b['pf'], b['side'], b['alpha'])
    if not cr:
        return None
    c, size, _ = cr
    nm = person(r)
    kind = r.choice(['comp', 'def', 'alpha'])
    if kind == 'comp':
        claim = f'says: "P(Type I error) = {p3(size)}, so P(Type II error) = 1 − {p3(size)} = {p3(1 - size)}."'
        a = f'Type I and Type II errors are not complementary: a Type II error is not rejecting {H0} when it is false, and its probability depends on the true value of p, which is not given.'
        k = 'B1 not complementary; B1 depends on the true value of p'
    elif kind == 'def':
        if b['d'].startswith('has '):
            claim = f'says: "A Type I error is concluding that {b["subj"]} {b["d"]} when it really has."'
            a = f'That is a correct decision. A Type I error is rejecting {H0} when it is true: concluding that {b["subj"]} {b["d"]} when in fact p = {pfm(b["p"])}.'
        else:
            claim = f'says: "A Type I error is not rejecting {H0} when {H0} is false."'
            a = f'That is a Type II error. A Type I error is rejecting {H0} when it is true: concluding that {b["subj"]} {b["d"]} when in fact p = {pfm(b["p"])}.'
        k = 'B1 identifies the error; B1 correct description in context'
    else:
        claim = f'says: "The test is at the {apc(b["alpha"])} level, so P(Type I error) = {num(b["alpha"])}."'
        a = f'For a discrete distribution the critical region {cr_text(b["side"], c)} has probability {p3(size)} under {H0}, which is less than {num(b["alpha"])}; P(Type I error) = {p3(size)}.'
        k = f'B1 discrete so not exactly {num(b["alpha"])}; M1 P({cr_text(b["side"], c)}); A1 {p3(size)}'
    return Q(f'{b["setup"]} The test uses {b["n"]} {b["c"]["unit"]} at the {apc(b["alpha"])} significance level, and {H0} is rejected if {cr_text(b["side"], c)}. {nm} {claim} Explain why {nm} is wrong.', a, k)


def ht4_c4(r, D):
    if r.random() < 0.5:
        b = nset(r, tails='<>', normal=True, alphas=(0.05, 0.1, 0.01))
        if not b:
            return None
        se = b['sd'] / math.sqrt(b['n'])
        cv = b['mu'] - b['zcv'] * se if b['side'] == '<' else b['mu'] + b['zcv'] * se
        dpl = 1 if se >= 0.5 else 2
        mu1 = round(b['mu'] - 2 * se if b['side'] == '<' else b['mu'] + 2 * se, dpl)
        t2 = 1 - Phi((cv - mu1) / se) if b['side'] == '<' else Phi((cv - mu1) / se)
        ineq = 'x̄ < ' if b['side'] == '<' else 'x̄ > '
        intro = f'{b["setup"]} A random sample of {b["n"]} {b["c"]["item"]} is to be used to test {b["hyp"]} at the {apc(b["alpha"])} significance level.'
        parts = [
            P(f'Find the set of values of the sample mean for which {H0} is rejected.', ineq + n4(cv), f'M1 {b["mu"]} {"−" if b["side"] == "<" else "+"} {b["zcv"]} × {b["sd"]}/√{b["n"]}; A1 {ineq}{n4(cv)}'),
            P('State the probability of a Type I error.', num(b['alpha']), 'B1'),
            P(f'Find the probability of a Type II error if in fact μ = {num(mu1)}.', n3(t2), f'M1 P({"x̄ ≥ " if b["side"] == "<" else "x̄ ≤ "}{n4(cv)} | μ = {num(mu1)}); M1 standardise; A1 {n3(t2)}'),
            P('State the effect on the probability of a Type II error of using a larger sample, with the same significance level.', 'It decreases, because σ/√n is smaller so the distributions of x̄ under the two values of μ overlap less.', 'B1 decreases; B1 reason'),
        ]
        return cmp_(r, intro, parts, k=(3, 4), deps={2: [0]})
    b = bset(r, tails='<>', ns=(15, 16, 18, 20, 24, 25))
    if not b:
        return None
    res = bsize_t2(r, b, D)
    if not res:
        return None
    c, size, nxt, p1, t2 = res
    intro = f'{b["setup"]} The test is based on {b["n"]} {b["c"]["unit"]} and uses a {apc(b["alpha"])} significance level.'
    parts = [
        P('State suitable hypotheses and find the critical region.', f'{b["hyp"]}; {cr_text(b["side"], c)}', f'B1 {b["hyp"]}; ' + cr_key(b['side'], c, size, nxt, b['alpha'])),
        P('Find the probability of a Type I error.', p3(size), f'B1 {p3(size)}'),
        P(f'Find the probability of a Type II error if in fact p = {num(p1)}.', p3(t2), 'M1 P(' + (f'X ≥ {c + 1}' if b['side'] == '<' else f'X ≤ {c - 1}') + f') with B({b["n"]}, {num(p1)}); A1 {p3(t2)}'),
        P('Explain, in context, what is meant by a Type II error.', f'Concluding that there is no evidence that {b["subj"]} {b["d"]} when in fact it {b["d"].split(" ")[0]}.', 'B1'),
    ]
    return cmp_(r, intro, parts, k=(3, 4), deps={1: [0], 2: [0]})


ht4.add('C4', (2, 3, 4, 5))(ht4_c4)

CHAPTERS[6] = [ht1, ht2, ht3, ht4]

fin()
