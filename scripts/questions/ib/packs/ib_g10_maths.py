"""IB MYP 5 Mathematics (Standard & Extended) – ib-g10-maths.

Criteria language: A knowing & understanding, B investigating patterns, C communicating,
D applying mathematics in real-life contexts. Extended-mathematics chapters (logarithms,
transformations, trigonometric functions, vectors, further probability) are included as the
curriculum lists them. Items use international contexts; every numerical answer is computed
(fractions / sympy / decimal rounding), never typed in. Structure follows ib_g9_maths.py.
"""
from __future__ import annotations

import math
import random
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as Fr

import sympy as sp

from _common import F, Registry, T, fmt, frac, mcq, name, num_distractors, pe, sup, two_names, CITIES
from ib_myp_maths_common import PLACES, place, money, m, lin, poly, sgn, fr, g, dp, ordinal, explain, short, surd_parts, surd, x, y

CONFIG = {'minutesPerMark': 1.2, 'mcqMinutes': 1.5}

# MYP eAssessment (on-screen, 2 h): 3 tasks ≈ 100 marks –
# Task 1 knowing & understanding (A + C) ≈ 33, Task 2 investigating patterns (B + C) ≈ 32,
# Task 3 applying mathematics in real-life contexts (C + D) ≈ 35. 25 items.
MOCK = [
    dict(section='Task 1 – Knowing and understanding (criteria A and C)', count=11, c=['C1', 'C3'], d=[2, 3, 3], marks=3),
    dict(section='Task 2 – Investigating patterns (criteria B and C): short investigations', count=3, c=['C2', 'C3'], d=[3, 3, 4], marks=4),
    dict(section='Task 2 – Investigating patterns (criteria B and C): extended investigations', count=4, c=['C2', 'C4'], d=[3, 4, 4], marks=5),
    dict(section='Task 3 – Applying mathematics in real-life contexts (criteria C and D)', count=7, c=['C3', 'C4'], d=[3, 4, 4, 5], marks=5),
]

R = Registry()


def init(subject_id):
    pass


def templates(st):
    return R.build(st)


def rnd(v, places):
    """Round half up to a number of decimal places (exact, via Decimal)."""
    q = Decimal(1).scaleb(-places) if places > 0 else Decimal(1)
    return Decimal(str(v)).quantize(q, rounding=ROUND_HALF_UP)


def r2(v, k=2) -> str:
    """Half-up rounding to k d.p., trailing zeros dropped, typographic minus."""
    s = str(rnd(float(v), k))
    if '.' in s:
        s = s.rstrip('0').rstrip('.')
    if s in ('-0', '−0'):
        s = '0'
    return m(s)


def rsf(v, sf=3) -> str:
    """Half-up rounding to sf significant figures, typographic minus."""
    v = float(v)
    if v == 0:
        return '0'
    d = Decimal(repr(v))
    e = d.adjusted()
    q = Decimal(1).scaleb(e - sf + 1)
    r = d.quantize(q, rounding=ROUND_HALF_UP)
    s = f'{int(r)}' if e - sf + 1 >= 0 else f'{r:f}'
    return m(s)


def fx(v) -> str:
    return m(frac(Fr(v)))


def cash(cur, v):
    return money(cur, float(rnd(float(v), 2)))


def big(v) -> str:
    """Integer with thin-space-free comma grouping."""
    return f'{int(v):,}'


def ptxt(p) -> str:
    return f'({m(p[0])}, {m(p[1])})'


def coef(a) -> str:
    """Coefficient written in front of a bracket or variable: 1 → '', −1 → '−', 3/80 → '(3/80)'."""
    a = Fr(a)
    s = '−' if a < 0 else ''
    a = abs(a)
    if a == 1:
        return s
    if a.denominator == 1:
        return s + str(a.numerator)
    return s + f'({a.numerator}/{a.denominator})'


def _a(word: str) -> str:
    return ('an ' if word[:1].lower() in 'aeiou8' or word[:2] in ('11', '18') else 'a ') + word


def sx(e) -> str:
    """sympy expression → pretty text with typographic minus."""
    return pe(e).replace('-', '−')


def sq(a: int, b: int) -> str:
    """a√b in simplest form."""
    k, r = surd_parts(b)
    a *= k
    if r == 1:
        return m(a)
    return f'{"" if a == 1 else "−" if a == -1 else m(a)}√{r}'


# =============================================================================================
# ch01 Number: Real Numbers, Surds and Exponents
# =============================================================================================
R.facts('ch01-st1', F(
    terms=[('real numbers', 'the set ℝ of all rational and irrational numbers; every point on the number line'),
           ('interval notation', 'a way of writing a set of real numbers between two endpoints, using [ ] for included endpoints and ( ) for excluded ones, e.g. (−2, 5]'),
           ('absolute value', 'the distance of a number from zero on the number line, written |x|; it is never negative'),
           ('irrational number', 'a real number that cannot be written as a/b with integers a and b (b ≠ 0); its decimal neither terminates nor recurs')],
    facts=[('Which set contains −4 but not 0.5?', 'ℤ', ['ℕ', 'ℚ', 'ℝ'], 'ℤ is the integers: −4 is an integer but 0.5 is not.'),
           ('What is the value of |−7| − |3|?', '4', ['−10', '10', '−4'], '|−7| = 7 and |3| = 3, so 7 − 3 = 4.'),
           ('Which interval describes x ≥ 2?', '[2, ∞)', ['(2, ∞)', '(−∞, 2]', '[2, ∞]'], 'The endpoint 2 is included and infinity is never included.'),
           ('Which of these numbers is irrational?', '√12', ['√16', '0.4̅', '22/7'], '12 is not a perfect square, so √12 = 2√3 is irrational.')],
    why=[('Explain why |a − b| gives the distance between a and b on the number line.', 'Subtracting gives the signed gap between the numbers; taking the absolute value removes the sign, so the result is the length of the gap whichever number is larger.'),
         ('Explain why infinity is always written with a round bracket in interval notation.', '∞ is not a real number, so it can never be an endpoint that is included in the set.'),
         ('Explain why the equation |x| = −3 has no solutions.', 'An absolute value is a distance, so it is always ≥ 0; it can never equal a negative number.'),
         ('Explain why every recurring decimal is a rational number.', 'A recurring decimal can be turned into a fraction (e.g. multiply by a power of 10 and subtract), so it can be written as a/b with integers a and b.')],
    misc=[('|x| = 5 means x = 5.', 'x can be 5 or −5, because both are 5 units from zero.'),
          ('The interval (1, 4) contains the numbers 2 and 3 only.', 'It contains every real number strictly between 1 and 4, for example 1.5 and π.'),
          ('|a + b| is always equal to |a| + |b|.', 'Only when a and b have the same sign; e.g. |3 + (−5)| = 2 but |3| + |−5| = 8.')],
    contrast=[('the interval [a, b]', 'the interval (a, b)', '[a, b] includes both endpoints (a ≤ x ≤ b); (a, b) excludes them (a < x < b).'),
              ('rational numbers', 'irrational numbers', 'Rationals can be written as a/b with integers (terminating or recurring decimals); irrationals cannot (non-terminating, non-recurring decimals).')],
))

_INEQ = [('<', '≤'), ('≤', '<'), ('<', '<'), ('≤', '≤')]


def _interval(a, b, lo, hi):
    return f'{"[" if lo == "≤" else "("}{m(a)}, {m(b)}{"]" if hi == "≤" else ")"}'


@R.add('ch01-st1', 'C1', (1, 3), 'mcq')
def interval_mcq(rng, slot):
    a = rng.randint(-9, 3)
    b = a + rng.randint(2, 10)
    lo, hi = rng.choice(_INEQ)
    corr = _interval(a, b, lo, hi)
    wr = [_interval(a, b, l2, h2) for l2, h2 in _INEQ if (l2, h2) != (lo, hi)]
    return mcq(rng, f'Which interval represents {m(a)} {lo} x {hi} {m(b)}?', corr, wr,
               f'{"Square" if lo == "≤" else "Round"} bracket at {m(a)} ({"included" if lo == "≤" else "excluded"}); {"square" if hi == "≤" else "round"} bracket at {m(b)}: {corr}.')


@R.add('ch01-st1', 'C3', (1, 4), 'short')
def abs_equation(rng, slot):
    a = rng.choice([1, 2, 3, 4, 5])
    b = rng.randint(-12, 12)
    c = rng.randint(1, 15)
    s1, s2 = Fr(c - b, a), Fr(-c - b, a)
    lhs = f'|{lin(a, b)}|'
    if slot.d <= 2 or rng.random() < 0.5:
        return short(f'Solve {lhs} = {c}.', f'x = {fx(max(s1, s2))} or x = {fx(min(s1, s2))}',
                     f'{lin(a, b)} = {c} or {lin(a, b)} = −{c} (M1); x = {fx(s1)} (A1); x = {fx(s2)} (A1).', 3)
    h = rng.randint(-8, 8)
    r = rng.randint(1, 9)
    strict = rng.random() < 0.5
    if rng.random() < 0.5:
        ans = _interval(h - r, h + r, '<' if strict else '≤', '<' if strict else '≤')
        return short(f'Solve |x{sgn(-h) if h else ""}| {"<" if strict else "≤"} {r}, giving your answer in interval notation.', ans,
                     f'{m(h - r)} {"<" if strict else "≤"} x {"<" if strict else "≤"} {m(h + r)} (M1 A1); interval {ans} (C1).', 3)
    ans = f'(−∞, {m(h - r)}{")" if strict else "]"} ∪ {"(" if strict else "["}{m(h + r)}, ∞)'
    return short(f'Solve |x{sgn(-h) if h else ""}| {">" if strict else "≥"} {r}, giving your answer in interval notation.', ans,
                 f'x {"<" if strict else "≤"} {m(h - r)} or x {">" if strict else "≥"} {m(h + r)} (M1 A1); union of intervals {ans} (C1).', 3)


def _real_pool(rng):
    pool = [(str(rng.randint(2, 40)), 'ℕ'), (m(-rng.randint(1, 30)), 'ℤ'), ('0', 'ℤ')]
    a, b = rng.randint(1, 13), rng.choice([3, 4, 6, 7, 9])
    if a % b == 0:
        a += 1
    pool.append((f'{"−" if rng.random() < 0.5 else ""}{a}/{b}', 'ℚ'))
    k = rng.randint(2, 9)
    pool.append((f'√{k * k}', 'ℕ'))
    pool.append((f'√{rng.choice([2, 3, 5, 6, 7, 8, 10, 12, 15, 18])}', 'irrational'))
    pool.append(('π' if rng.random() < 0.5 else f'{rng.randint(1, 4)}π', 'irrational'))
    d = rng.randint(1, 9)
    pool.append((f'0.{d}{d}{d}… (recurring)', 'ℚ'))
    pool.append((f'∛{rng.choice([8, 27, 64, 125])}', 'ℕ'))
    rng.shuffle(pool)
    return pool[:rng.randint(5, 7)]


@R.add('ch01-st1', 'C3', (1, 3), 'short')
def classify_reals(rng, slot):
    pool = _real_pool(rng)
    ans = '; '.join(f'{s}: {k}' for s, k in pool)
    return short(f'For each number, state the smallest of the sets ℕ, ℤ, ℚ or "irrational" that contains it: {", ".join(s for s, _ in pool)}.', ans,
                 f'{ans}. A1 for every two correct; simplify roots such as √(perfect square) first (criterion C: correct set symbols).', 3)


@R.add('ch01-st1', 'C2', (2, 4), 'explain')
def abs_explain(rng, slot):
    who = name(rng)
    h, r = rng.randint(-6, 9), rng.randint(2, 8)
    kind = rng.choice(['dist', 'wrongsol', 'triangle'])
    if kind == 'dist':
        return explain(f'Explain, using the idea of distance, why the solution of |x{sgn(-h) if h else ""}| ≤ {r} is the interval [{m(h - r)}, {m(h + r)}].',
                       f'|x{sgn(-h) if h else ""}| is the distance from x to {m(h)}; the points within {r} units of {m(h)} run from {m(h - r)} to {m(h + r)}, endpoints included because of ≤.',
                       'Distance interpretation (R1); endpoints and brackets justified (R1).', 2)
    if kind == 'wrongsol':
        return explain(f'{who} solves |x{sgn(-h) if h else ""}| > {r} and writes {m(h - r)} > x > {m(h + r)}. Explain why this is wrong and give the correct solution.',
                       f'No number is both less than {m(h - r)} and greater than {m(h + r)}; the solution is two separate pieces: x < {m(h - r)} or x > {m(h + r)}.',
                       'Contradiction identified (R1); correct union stated (A1).', 2)
    a, b = rng.randint(2, 9), -rng.randint(2, 9)
    return explain(f'Using a = {a} and b = {m(b)}, show that |a + b| ≤ |a| + |b| and explain when the two sides are equal.',
                   f'|{a} + ({m(b)})| = {abs(a + b)} and |{a}| + |{m(b)}| = {a + abs(b)}, so {abs(a + b)} ≤ {a + abs(b)}; the two sides are equal only when a and b have the same sign (or one is 0).',
                   'Both sides evaluated (A1); condition for equality explained (R1).', 2)


@R.add('ch01-st1', 'C4', (3, 5), 'multi_step')
def tolerance_task(rng, slot):
    city, country, cur, cname = place(rng)
    kind = rng.choice(['bolt', 'fridge', 'flight', 'pool'])
    if kind == 'bolt':
        L = rng.choice([40, 45, 50, 60, 75, 80, 120])
        t = Fr(rng.choice([1, 2, 3, 5]), 10)
        meas = sorted({L + Fr(rng.randint(-6, 6), 10) for _ in range(5)})
        ok = [v for v in meas if abs(v - L) <= t]
        ans = f'(a) |x − {L}| ≤ {g(float(t))} (b) [{g(float(L - t))}, {g(float(L + t))}] (c) accepted: {", ".join(g(float(v)) for v in ok) or "none"} (d) the absolute value measures how far each bolt is from {L} mm in either direction'
        q_ = (f'A factory in {city} makes bolts that should be {L} mm long. A bolt is accepted if its length x mm is within {g(float(t))} mm of {L} mm. (a) Write this condition using absolute value. '
              f'(b) Write the accepted lengths in interval notation. (c) Which of these bolts are accepted: {", ".join(g(float(v)) for v in meas)} mm? (d) Explain why absolute value is a good way to describe a tolerance.')
    elif kind == 'fridge':
        lo, hi = rng.randint(0, 3), rng.randint(5, 8)
        c, r = Fr(lo + hi, 2), Fr(hi - lo, 2)
        ans = f'(a) [{lo}, {hi}] (b) centre {g(float(c))} °C, half-width {g(float(r))} °C: |T − {g(float(c))}| ≤ {g(float(r))} (c) |{m(lo - 2)} − {g(float(c))}| = {g(float(abs(lo - 2 - c)))} > {g(float(r))}, so {m(lo - 2)} °C is outside the safe range'
        q_ = (f'Food regulations in {country} say a fridge must stay between {lo} °C and {hi} °C inclusive. (a) Write the safe temperatures T in interval notation. '
              f'(b) Write the condition as a single absolute-value inequality and explain how you found its numbers. (c) A sensor reads {m(lo - 2)} °C. Use your inequality to decide whether this is safe.')
    elif kind == 'flight':
        T = rng.choice([90, 105, 120, 135, 150, 165, 180])
        e = rng.choice([5, 10, 15])
        arr = [T + rng.randint(-25, 25) for _ in range(4)]
        on = [a for a in arr if abs(a - T) <= e]
        ans = f'(a) |t − {T}| ≤ {e} (b) [{T - e}, {T + e}] (c) on time: {", ".join(map(str, on)) or "none"}; proportion {fx(Fr(len(on), 4))} (d) e.g. a tighter tolerance is fairer to passengers but harder for the airline to meet'
        q_ = (f'An airline in {city} calls a flight "on time" if its journey time t minutes is within {e} minutes of the scheduled {T} minutes. (a) Write this as an absolute-value inequality. (b) Write it in interval notation. '
              f'(c) Four flights took {", ".join(map(str, arr))} minutes. Which were on time, and what fraction is this? (d) Comment on the effect of changing the tolerance.')
    else:
        d = rng.choice([25, 50])
        e = Fr(rng.choice([1, 2, 3]), 100)
        lanes = sorted({d + Fr(rng.randint(-5, 5), 100) for _ in range(4)})
        bad = [v for v in lanes if abs(v - d) > e]
        ans = f'(a) |L − {d}| ≤ {g(float(e))} (b) [{g(float(d - e), 4)}, {g(float(d + e), 4)}] (c) outside: {", ".join(g(float(v), 4) for v in bad) or "none"} (d) records need fair, comparable distances'
        q_ = (f'For international records, a {d} m pool in {city} must have lanes whose length L metres is within {g(float(e))} m of {d} m. (a) Write the condition with absolute value. (b) Write it in interval notation. '
              f'(c) Lanes were measured as {", ".join(g(float(v), 4) for v in lanes)} m. Which lanes are outside the tolerance? (d) Suggest why such a strict tolerance is needed.')
    return short(q_, ans, f'{ans}. Absolute-value statement (A1); interval notation (A1 C1); values tested correctly (M1 A1); reasoning in context (D: R1).', 6, 'multi_step', 'G5')


R.facts('ch01-st2', F(
    terms=[('surd', 'an irrational root such as √3 or ∛5 that cannot be simplified to a rational number'),
           ('rational exponent', 'an exponent of the form p/q, where a^(p/q) = (q-th root of a)^p'),
           ('rationalising the denominator', 'rewriting a fraction so that no surd remains in its denominator, by multiplying top and bottom by a suitable surd or conjugate'),
           ('conjugate', 'the conjugate of a + √b is a − √b; their product a² − b is rational')],
    facts=[('What is 16^(3/4)?', '8', ['12', '64', '4'], '⁴√16 = 2 and 2³ = 8.'),
           ('Simplify √50.', '5√2', ['25√2', '2√5', '10√5'], '√50 = √25 × √2 = 5√2.'),
           ('What is 9^(−1/2)?', '1/3', ['−3', '−1/3', '3'], 'A negative exponent gives the reciprocal: 1/√9 = 1/3.'),
           ('Which expression equals 1/√5 with a rational denominator?', '√5/5', ['5/√5', '√5', '1/5'], 'Multiply top and bottom by √5.')],
    why=[('Explain why a^(1/2) = √a, using the laws of exponents.', '(a^(1/2))² = a^(1/2 × 2) = a¹ = a, so a^(1/2) is the positive number whose square is a, which is √a.'),
         ('Explain why √a + √b is not equal to √(a + b) in general.', 'Roots do not distribute over addition: e.g. √9 + √16 = 7 but √25 = 5; only products split, √(ab) = √a√b.'),
         ('Explain why multiplying by the conjugate removes the surd from a denominator such as 3 + √2.', '(3 + √2)(3 − √2) = 9 − 2 = 7: the cross terms cancel and √2 × √2 is rational, so the denominator becomes rational.'),
         ('Explain why a^0 = 1 for any non-zero a.', 'aⁿ ÷ aⁿ = 1, but by the division law it is also a^(n − n) = a⁰, so a⁰ = 1.')],
    misc=[('8^(−1/3) = −2.', 'A negative exponent gives a reciprocal, not a negative: 8^(−1/3) = 1/∛8 = 1/2.'),
          ('√12 simplified is 6√2.', 'Take out the largest square factor: √12 = √4 × √3 = 2√3.'),
          ('(√3 + 1)² = 3 + 1 = 4.', 'Expand fully: (√3 + 1)² = 3 + 2√3 + 1 = 4 + 2√3.')],
    contrast=[('a^(−n)', '−aⁿ', 'a^(−n) = 1/aⁿ is the reciprocal and is positive for a > 0; −aⁿ is the negative of aⁿ.'),
              ('a^(1/n)', 'a/n', 'a^(1/n) is the n-th root of a; a/n is a divided by n (e.g. 8^(1/3) = 2 but 8/3 ≈ 2.67).')],
))

_RE = {2: '√', 3: '∛', 4: '⁴√', 5: '⁵√'}


@R.add('ch01-st2', 'C1', (1, 3), 'mcq')
def rational_exp_mcq(rng, slot):
    q = rng.choice([2, 3, 4])
    b = rng.choice([2, 3, 4, 5]) if q <= 3 else rng.choice([2, 3])
    p = rng.choice([v for v in (1, 2, 3, -1, -2, -3) if math.gcd(abs(v), q) == 1])
    base = b ** q
    val = Fr(b) ** p
    wr = [fx(Fr(base * p, q)), fx(-val), fx(Fr(b) ** (-p)), fx(Fr(base) ** 1 * p)]
    wr = [w for w in dict.fromkeys(wr) if w != fx(val)]
    return mcq(rng, f'Evaluate {base}^({m(p)}/{q}).', fx(val), wr[:3],
               f'{_RE[q]}{base} = {b}, then raise to the power {m(p)}: {fx(val)}.')


@R.add('ch01-st2', 'C3', (1, 4), 'short')
def eval_rational_exp(rng, slot):
    terms = []
    total = Fr(1)
    for _ in range(2 if slot.d >= 3 else 1):
        q = rng.choice([2, 3, 4])
        b = rng.choice([2, 3, 5]) if q != 4 else rng.choice([2, 3])
        p = rng.choice([v for v in (1, 2, 3, -1, -2) if math.gcd(abs(v), q) == 1])
        terms.append((b ** q, p, q, Fr(b) ** p))
    if len(terms) == 1:
        base, p, q, v = terms[0]
        return short(f'Without a calculator, evaluate {base}^({m(p)}/{q}).', fx(v), f'{_RE[q]}{base} = {round(base ** (1 / q))} (M1); power {m(p)} → {fx(v)} (A1).', 2)
    (b1, p1, q1, v1), (b2, p2, q2, v2) = terms
    op = rng.choice(['×', '÷', '+'])
    res = v1 * v2 if op == '×' else v1 / v2 if op == '÷' else v1 + v2
    return short(f'Without a calculator, evaluate {b1}^({m(p1)}/{q1}) {op} {b2}^({m(p2)}/{q2}).', fx(res),
                 f'{b1}^({m(p1)}/{q1}) = {fx(v1)} (A1); {b2}^({m(p2)}/{q2}) = {fx(v2)} (A1); {fx(res)} (A1).', 3)


@R.add('ch01-st2', 'C3', (2, 5), 'short')
def surd_simplify(rng, slot):
    kind = rng.choice(['collect', 'expand', 'ration', 'conj'])
    if kind == 'collect':
        n = rng.choice([2, 3, 5, 6, 7])
        ks = rng.sample([2, 3, 4, 5, 6], 3)
        sg = [1, rng.choice([1, -1]), rng.choice([1, -1])]
        tot = sum(s * k for s, k in zip(sg, ks))
        txt = f'√{ks[0] ** 2 * n}' + ''.join(f' {"+" if s > 0 else "−"} √{k * k * n}' for s, k in zip(sg[1:], ks[1:]))
        return short(f'Simplify {txt}, giving your answer in the form a√{n}.', sq(tot, n) if tot else '0',
                     'Each surd written as k√' + str(n) + ' (M1 A1); collected: ' + (sq(tot, n) if tot else '0') + ' (A1).', 3)
    if kind == 'expand':
        a, c = rng.randint(1, 7), rng.randint(1, 7)
        b = rng.choice([2, 3, 5, 6, 7, 10, 11])
        rat, irr = a * c - b, c - a
        res = m(rat) + (f' {"+" if irr > 0 else "−"} {sq(abs(irr), b)}' if irr else '')
        return short(f'Expand and simplify ({a} + √{b})({c} − √{b}).', res,
                     f'Four terms {a * c} − {a}√{b} + {c}√{b} − {b} (M1); collect: {res} (A1 A1).', 3)
    if kind == 'ration':
        k, n = rng.randint(1, 12), rng.choice([2, 3, 5, 6, 7, 10])
        c = rng.randint(1, 4)
        gg = math.gcd(k, c * n)
        a1, d1 = k // gg, c * n // gg
        res = f'{"" if a1 == 1 else a1}√{n}' + (f'/{d1}' if d1 != 1 else '')
        dtxt = f'{"" if c == 1 else c}√{n}'
        return short(f'Rationalise the denominator and simplify: {k}/({dtxt}).', res,
                     f'Multiply by √{n}/√{n} (M1); {k}√{n}/{c * n} (A1); simplified {res} (A1).', 3)
    a = rng.randint(2, 6)
    b = rng.choice([2, 3, 5, 6, 7])
    if a * a == b:
        a += 1
    sgn_ = rng.choice([1, -1])
    d = a * a - b
    k = rng.randint(1, 9)
    num = k * d if rng.random() < 0.5 else k
    gg = math.gcd(num, d)
    nn, dd = num // gg, d // gg
    if dd < 0:
        nn, dd = -nn, -dd
    conj = f'{a} {"−" if sgn_ > 0 else "+"} √{b}'
    res = f'{"" if nn == 1 else "−" if nn == -1 else m(nn)}({conj})' + (f'/{dd}' if dd != 1 else '')
    return short(f'Rationalise the denominator: {num}/({a} {"+" if sgn_ > 0 else "−"} √{b}).', res,
                 f'Multiply by the conjugate ({conj}) (M1); denominator {a * a} − {b} = {d} (A1); {res} (A1).', 3)


@R.add('ch01-st2', 'C2', (2, 4), 'explain')
def surd_explain(rng, slot):
    who = name(rng)
    kind = rng.choice(['add', 'neg', 'frac', 'largest'])
    if kind == 'add':
        a, b = rng.sample([4, 9, 16, 25, 36, 49, 64], 2)
        return explain(f'{who} claims √{a} + √{b} = √{a + b}. Use these numbers to explain why the claim is false.',
                       f'√{a} + √{b} = {math.isqrt(a)} + {math.isqrt(b)} = {math.isqrt(a) + math.isqrt(b)}, but √{a + b} ≈ {g(math.sqrt(a + b), 3)}; roots do not split over addition.',
                       'Both sides evaluated (A1); general reason (R1).', 2)
    if kind == 'neg':
        b, q = rng.choice([(2, 3), (3, 3), (2, 5), (4, 3), (5, 2), (6, 2), (2, 4)])
        return explain(f'{who} says {b ** q}^(−1/{q}) = −{b}. Explain the mistake and give the correct value.',
                       f'The negative exponent means reciprocal, not negative: {b ** q}^(−1/{q}) = 1/{_RE[q]}{b ** q} = 1/{b}.',
                       'Meaning of the negative exponent (R1); 1/' + str(b) + ' (A1).', 2)
    if kind == 'frac':
        b, q, p = rng.choice([(2, 3, 2), (3, 3, 2), (2, 4, 3), (4, 3, 2), (5, 2, 3), (3, 2, 3)])
        return explain(f'Explain why {b ** q}^({p}/{q}) can be worked out as ({_RE[q]}{b ** q}){sup(p)} and evaluate it.',
                       f'{b ** q}^({p}/{q}) = ({b ** q}^(1/{q})){sup(p)} by the power law; {_RE[q]}{b ** q} = {b}, so the value is {b}{sup(p)} = {b ** p}.',
                       'Power law justification (R1); value (A1).', 2)
    a, b = rng.randint(2, 7), rng.randint(2, 7)
    n1, n2 = rng.sample([2, 3, 5, 6, 7], 2)
    v1, v2 = a * math.sqrt(n1), b * math.sqrt(n2)
    if abs(v1 - v2) < 1e-9:
        return None
    return explain(f'Without a calculator, explain which is larger: {a}√{n1} or {b}√{n2}.',
                   f'{a}√{n1} = √{a * a * n1} and {b}√{n2} = √{b * b * n2}; since {max(a * a * n1, b * b * n2)} > {min(a * a * n1, b * b * n2)}, {f"{a}√{n1}" if v1 > v2 else f"{b}√{n2}"} is larger.',
                   'Both written as single roots (M1); comparison justified (R1).', 2)


@R.add('ch01-st2', 'C4', (3, 5), 'multi_step')
def surd_task(rng, slot):
    city = rng.choice(CITIES)
    kind = rng.choice(['tile', 'pattern', 'rect', 'paper'])
    if kind == 'tile':
        n = rng.choice([2, 3, 5, 6, 7])
        k = rng.randint(2, 6)
        A = k * k * n
        ans = f'(a) √{A} = {sq(1, A)} cm (b) {sq(4, A)} cm (c) diagonal = {sq(1, A)} × √2 = {sq(1, 2 * A)} cm (d) about {g(math.sqrt(2 * A), 3)} cm; exact form avoids rounding errors in later steps'
        q_ = (f'A designer in {city} makes square tiles of area {A} cm². (a) Find the side length in simplest surd form. (b) Find the perimeter in simplest surd form. '
              f'(c) Find the length of the diagonal in simplest surd form. (d) Give the diagonal to 3 significant figures and explain why the exact form is useful.')
    elif kind == 'pattern':
        ns = rng.sample(range(2, 15), 3)
        ns = [n for n in ns if math.isqrt(n) ** 2 != n] or [2, 3, 5]
        n4 = rng.randint(15, 60)
        rows = '; '.join(f'(√{n} + 1)(√{n} − 1) = {n - 1}' for n in ns)
        ans = f'(a) {rows} (b) the result is always one less than the number under the root (c) (√n + 1)(√n − 1) = n − √n + √n − 1 = n − 1 (d) {n4 - 1}'
        q_ = (f'Investigate the product (√n + 1)(√n − 1). (a) Evaluate it for n = {", ".join(map(str, ns))}. (b) Describe the pattern. (c) Prove your conjecture algebraically. '
              f'(d) Use it to write down (√{n4} + 1)(√{n4} − 1).')
    elif kind == 'rect':
        a, b = rng.choice([2, 3, 5]), rng.choice([6, 7, 10, 11])
        p, q = rng.randint(1, 4), rng.randint(1, 4)
        area_rat, area_irr = p * q * 0, 0
        # sides p√a and q√b
        prod = sq(p * q, a * b)
        diag2 = p * p * a + q * q * b
        ans = f'(a) area = {p if p > 1 else ""}√{a} × {q if q > 1 else ""}√{b} = {prod} m² (b) perimeter = {sq(2 * p, a)} + {sq(2 * q, b)} m (c) diagonal = √({p * p * a} + {q * q * b}) = {sq(1, diag2)} m (d) about {g(math.sqrt(diag2), 3)} m'
        q_ = (f'A rectangular garden plot in {city} measures {p if p > 1 else ""}√{a} m by {q if q > 1 else ""}√{b} m. (a) Find its exact area in simplest form. (b) Find its exact perimeter. '
              f'(c) Use Pythagoras\' theorem to find the exact length of the diagonal. (d) Give the diagonal to 3 significant figures.')
    else:
        k = rng.randint(1, 4)
        w = 210 * k // 1
        ans = f'(a) the ratio stays 1 : √2 because halving the long side gives (√2/2) : 1 = 1 : √2 (b) {g(w * math.sqrt(2), 4)} mm (c) the area halves each time: A{k} → A{k + 1} has half the area (d) side ratio of A{k + 1} to A{k} is 1 : √2, so lengths shrink by 1/√2 = √2/2'
        q_ = (f'A-series paper (used in {city}) has sides in the ratio 1 : √2, and folding a sheet in half gives the next size. (a) Show that the half-sheet has the same ratio 1 : √2. '
              f'(b) A sheet has short side {w} mm; find its long side to 4 s.f. (c) Describe what happens to the area. (d) Find, in surd form, the length scale factor from one size to the next.')
    return short(q_, ans, f'{ans}. Surds simplified exactly (A1 A1); method/proof communicated (B/C: M1 R1); answer in context with sensible accuracy (D: A1).', 6, 'multi_step', 'G5')


R.facts('ch01-st3', F(
    terms=[('exponential equation', 'an equation in which the unknown appears in an exponent, e.g. 3^(x + 1) = 27'),
           ('common base', 'writing both sides of an equation as powers of the same number so the exponents can be equated'),
           ('equating exponents', 'using the fact that if a^m = a^n (a > 0, a ≠ 1) then m = n')],
    facts=[('Solve 2^x = 64.', 'x = 6', ['x = 32', 'x = 8', 'x = 5'], '64 = 2⁶.'),
           ('Write 27 as a power of 3.', '3³', ['3⁹', '3²', '9³'], '3 × 3 × 3 = 27.'),
           ('Solve 5^x = 1/25.', 'x = −2', ['x = 2', 'x = −1/2', 'x = 1/2'], '1/25 = 5^(−2).'),
           ('Write 8^x as a power of 2.', '2^(3x)', ['2^(x + 3)', '2^(8x)', '6^x'], '8 = 2³, so 8^x = (2³)^x = 2^(3x).')],
    why=[('Explain why you can equate the exponents when 3^a = 3^b.', 'The function 3^x is one-to-one (always increasing), so equal outputs come only from equal inputs: a = b.'),
         ('Explain why 2^x = −8 has no real solution.', '2^x is positive for every real x, so it can never equal a negative number.'),
         ('Explain why 4^x = 8 needs both sides rewritten before you can solve it.', '4 and 8 are different bases; writing them as 2² and 2³ gives 2^(2x) = 2³, so 2x = 3 and x = 3/2.')],
    misc=[('If 2^x = 2^5 × 2^3, then x = 15.', 'Multiplying powers adds exponents: 2^5 × 2^3 = 2^8, so x = 8.'),
          ('9^x = 27 has no solution because 27 is not a power of 9.', 'Both are powers of 3: 3^(2x) = 3³, so x = 3/2.')],
))

_BASES = {2: [(2, 1), (4, 2), (8, 3), (16, 4), (32, 5)], 3: [(3, 1), (9, 2), (27, 3), (81, 4)], 5: [(5, 1), (25, 2), (125, 3)]}


def _k(u, e):
    return e if u == 1 else f'{u}({e})'


def _pw(base_txt, a, c):
    e = lin(a, c)
    return f'{base_txt}^{e}' if e in ('x',) else f'{base_txt}^({e})'


@R.add('ch01-st3', 'C1', (1, 3), 'mcq')
def exp_eq_mcq(rng, slot):
    b = rng.choice([2, 3, 5])
    n = rng.randint(-3, 5)
    if n == 0:
        n = 2
    rhs = fx(Fr(b) ** n)
    return mcq(rng, f'Solve {b}^x = {rhs}.', f'x = {m(n)}', [f'x = {m(-n)}', f'x = {fx(Fr(b ** abs(n), b))}', f'x = {m(n + 1)}'],
               f'{rhs} = {b}{sup(n)}, so x = {m(n)}.')


@R.add('ch01-st3', 'C3', (1, 4), 'short')
def exp_eq_solve(rng, slot):
    b = rng.choice([2, 3, 5])
    if slot.d <= 2:
        a, c = rng.choice([1, 2, 3]), rng.randint(-4, 4)
        xs = rng.randint(-2, 4)
        N = a * xs + c
        rhs = fx(Fr(b) ** N)
        return short(f'Solve {_pw(b, a, c)} = {rhs}.', f'x = {m(xs)}', f'{rhs} = {b}{sup(N)} (M1); {lin(a, c)} = {m(N)} (A1); x = {m(xs)} (A1).', 3)
    (B1, u), (B2, v) = rng.sample(_BASES[b], 2)
    a, c = rng.randint(1, 3), rng.randint(-3, 3)
    d, e = rng.randint(1, 3), rng.randint(-3, 3)
    den = u * a - v * d
    if den == 0:
        return None
    xs = Fr(v * e - u * c, den)
    return short(f'Solve {_pw(B1, a, c)} = {_pw(B2, d, e)}.', f'x = {fx(xs)}',
                 f'Common base {b}: {b}^({_k(u, lin(a, c))}) = {b}^({_k(v, lin(d, e))}) (M1); {_k(u, lin(a, c))} = {_k(v, lin(d, e))} (M1); x = {fx(xs)} (A1).', 3)


@R.add('ch01-st3', 'C3', (2, 5), 'short')
def exp_eq_product(rng, slot):
    b = rng.choice([2, 3])
    p, q = rng.randint(1, 4), rng.randint(1, 4)
    k = rng.choice([t for t in range(1, 7) if t != q])
    if rng.random() < 0.5:
        # b^(px) × b^q = b^k   → px + q = k
        xs = Fr(k - q, p)
        rhs = b ** k
        return short(f'Solve {_pw(b, p, 0)} × {b ** q} = {rhs}.', f'x = {fx(xs)}', f'{b ** q} = {b}{sup(q)} and {rhs} = {b}{sup(k)} (M1); {lin(p, q)} = {k} (A1); x = {fx(xs)} (A1).', 3)
    # (1/b)^(x) = b^k type : b^(−x) = b^(px + q)  → −x = px + q
    xs = Fr(-q, p + 1)
    return short(f'Solve (1/{b})^x = {b}^({lin(p, q)}).', f'x = {fx(xs)}', f'(1/{b})^x = {b}^(−x) (M1); −x = {lin(p, q)} (A1); x = {fx(xs)} (A1).', 3)


@R.add('ch01-st3', 'C2', (2, 4), 'explain')
def exp_eq_explain(rng, slot):
    who = name(rng)
    b = rng.choice([2, 3])
    (B1, u), (B2, v) = rng.sample(_BASES[b][1:], 2)
    kind = rng.choice(['base', 'neg', 'add'])
    if kind == 'base':
        xs = Fr(v, u)
        return explain(f'{who} says {B1}^x = {B2} cannot be solved without a calculator. Explain how to solve it exactly.',
                       f'Write both sides as powers of {b}: {b}^({lin(u, 0)}) = {b}{sup(v)}, so {lin(u, 0)} = {v} and x = {fx(xs)}.',
                       'Common base identified (R1); solution (A1).', 2)
    if kind == 'neg':
        return explain(f'Explain why the equation {B1}^x = −{B2} has no real solution, while {B1}^x = 1/{B2} does.',
                       f'{B1}^x > 0 for every real x, so it cannot be negative; 1/{B2} = {b}^(−{v}) is positive, giving x = {fx(Fr(-v, u))}.',
                       'Positivity of exponentials (R1); second equation solved (A1).', 2)
    k = rng.randint(2, 5)
    return explain(f'{who} solves {b}^x + {b}^x = {b}{sup(k)} by writing {b}^(2x) = {b}{sup(k)}. Explain the error and solve the equation correctly.',
                   f'{b}^x + {b}^x = 2 × {b}^x, not {b}^(2x) (adding does not add exponents). {"So 2^(x + 1) = 2^" + str(k) + ", x = " + str(k - 1) if b == 2 else "So 2 × 3^x = 3^" + str(k) + ", 3^x = 3^" + str(k) + "/2, which needs logarithms: x = " + rsf(k - math.log(2, 3), 3)}.',
                   'Error explained (R1); correct solution (A1).', 2)


@R.add('ch01-st3', 'C4', (3, 5), 'multi_step')
def exp_eq_task(rng, slot):
    city = rng.choice(CITIES)
    kind = rng.choice(['bacteria', 'halflife', 'chain', 'tournament'])
    if kind == 'bacteria':
        N0 = rng.choice([50, 100, 200, 250, 400, 500])
        d = rng.choice([15, 20, 30, 40])
        k = rng.randint(4, 9)
        ans = f'(a) N = {N0} × 2^(t/{d}) (b) {big(N0 * 2 ** 3)} bacteria (c) {big(N0 * 2 ** k)} = {N0} × 2{sup(k)} so t/{d} = {k}, t = {k * d} minutes (d) real growth slows when food or space runs out'
        q_ = (f'A lab in {city} grows a culture that starts with {N0} bacteria and doubles every {d} minutes. (a) Write a formula for the number N after t minutes. (b) Find N after {3 * d} minutes. '
              f'(c) Without a calculator, find when N = {big(N0 * 2 ** k)}. (d) Explain one reason the model may fail for large t.')
    elif kind == 'halflife':
        M0 = rng.choice([64, 80, 96, 128, 160, 320])
        h = rng.choice([5, 6, 8, 12, 25])
        k = rng.randint(2, 5)
        Mk = Fr(M0, 2 ** k)
        ans = f'(a) M = {M0} × (1/2)^(t/{h}) (b) {g(float(Fr(M0, 4)))} mg (c) {g(float(Mk))} = {M0} × 2^(−{k}), so t = {k * h} hours (d) it never reaches 0 exactly, because (1/2)^(t/{h}) > 0'
        q_ = (f'A hospital in {city} uses a medical isotope with a half-life of {h} hours. A dose starts at {M0} mg. (a) Write a formula for the mass M after t hours. (b) Find the mass after {2 * h} hours. '
              f'(c) Without a calculator, find when the mass is {g(float(Mk))} mg. (d) Explain whether the mass ever reaches zero.')
    elif kind == 'chain':
        s = rng.choice([2, 3, 4])
        k = rng.randint(4, 8)
        ans = f'(a) {s}, {s ** 2}, {s ** 3} (b) {s}^n (c) {s}^n = {big(s ** k)} = {s}{sup(k)}, so n = {k} rounds (d) total = {s}({s}{sup(k)} − 1)/({s} − 1) = {big(s * (s ** k - 1) // (s - 1))}'
        q_ = (f'A charity in {city} starts a message chain: in round 1 one person sends it to {s} people, and in every later round each new receiver sends it to {s} more. (a) Write the number of new receivers in rounds 1, 2 and 3. '
              f'(b) Write an expression for round n. (c) Without a calculator, find the round in which {big(s ** k)} new people receive it. (d) Find the total number of receivers in the first {k} rounds.')
    else:
        k = rng.randint(4, 8)
        ans = f'(a) 2^n players allow n rounds (b) {2 ** k} = 2{sup(k)}, so {k} rounds (c) {2 ** k - 1} matches (one player is knocked out per match) (d) 2^n − 1'
        q_ = (f'A knockout tennis tournament in {city} halves the number of players each round until one champion is left. (a) Explain why the number of players should be a power of 2. (b) With {2 ** k} players, find the number of rounds by solving an exponential equation. '
              f'(c) Find the total number of matches. (d) Write a formula for the number of matches with 2^n players.')
    return short(q_, ans, f'{ans}. Model or common base set up (M1); exponents equated and solved (A1 A1); pattern generalised (B: R1); interpretation in context (D: R1).', 6, 'multi_step', 'G5')


R.facts('ch01-st4', F(
    terms=[('absolute error', 'the size of the difference between an approximate (or measured) value and the exact value: |V_A − V_E|'),
           ('percentage error', 'the absolute error as a percentage of the exact value: |V_A − V_E| / |V_E| × 100%'),
           ('upper and lower bounds', 'the largest and smallest values that a rounded measurement could have been')],
    facts=[('A length of 48 cm is estimated as 50 cm. What is the percentage error?', '4.17%', ['4%', '2%', '96%'], '|50 − 48| ÷ 48 × 100 ≈ 4.17%.'),
           ('A mass is 7.4 kg to 1 d.p. What is its lower bound?', '7.35 kg', ['7.3 kg', '7.45 kg', '7.39 kg'], 'Half of 0.1 below 7.4.'),
           ('In the percentage-error formula, you divide by:', 'the exact value', ['the approximate value', 'the sum of the two values', '100'], 'Error is measured relative to the true value.')],
    why=[('Explain why percentage error is more useful than absolute error for comparing the accuracy of two estimates.', 'An error of 1 cm is large on a 5 cm object but tiny on a 5 m one; dividing by the exact value puts both on the same relative scale.'),
         ('Explain why the absolute value is used in the percentage-error formula.', 'The error is a size; overestimates and underestimates of the same amount should give the same positive percentage.'),
         ('Explain why the upper bound of a difference a − b uses the upper bound of a and the lower bound of b.', 'To make a difference as large as possible, the first number must be as large as possible and the subtracted number as small as possible.')],
    misc=[('Percentage error = |approximate − exact| ÷ approximate × 100.', 'You divide by the exact value, not the approximate one.'),
          ('A length of 12 cm to the nearest cm has upper bound 12.4 cm.', 'The upper bound is 12.5 cm (the boundary at which it would round up).')],
))


@R.add('ch01-st4', 'C1', (1, 3), 'mcq')
def pct_error_mcq(rng, slot):
    E = rng.choice([40, 48, 60, 75, 80, 120, 125, 150, 200, 250])
    A = E + rng.choice([-1, 1]) * rng.choice([2, 3, 4, 5, 6, 8, 10])
    pe_ = abs(A - E) / E * 100
    wr = [r2(abs(A - E) / A * 100, 2) + '%', r2(abs(A - E), 2) + '%', r2(A / E * 100, 2) + '%']
    return mcq(rng, f'The exact value is {E} and an estimate is {A}. What is the percentage error?', r2(pe_, 2) + '%', wr,
               f'|{A} − {E}| ÷ {E} × 100 = {r2(pe_, 2)}%.')


_EST = [('the number of people at a concert', 'people'), ('the height of a tree', 'm'), ('the mass of a parcel', 'kg'), ('the length of a corridor', 'm'),
        ('the time for a run', 's'), ('the volume of water in a tank', 'L'), ('the cost of a shopping basket', '')]


@R.add('ch01-st4', 'C3', (1, 4), 'short')
def pct_error_calc(rng, slot):
    what, u = rng.choice(_EST)
    city, country, cur, cname = place(rng)
    if u == 'people':
        E = rng.randint(800, 9000)
        A = round(E, -2) if rng.random() < 0.5 else round(E * rng.uniform(0.85, 1.15), -2)
        if A == E:
            A += 100
        Et, At = big(E), big(A)
    elif u == '':
        E = Fr(rng.randint(2000, 9000), 100)
        A = Fr(round(float(E)))
        if A == E:
            A += 1
        Et, At = cash(cur, E), cash(cur, A)
    else:
        E = Fr(rng.randint(120, 950), 10)
        A = Fr(round(float(E) * rng.uniform(0.85, 1.15)))
        if A == E:
            A += 1
        Et, At = f'{g(float(E), 4)} {u}', f'{g(float(A), 4)} {u}'
    pe_ = abs(Fr(A) - Fr(E)) / Fr(E) * 100
    return short(f'In {city}, {what} was estimated as {At}. The exact value was {Et}. Find the percentage error, correct to 2 decimal places.', f'{rnd(float(pe_), 2)}%',
                 f'|{At} − {Et}| = absolute error (M1); ÷ exact {Et} × 100 (M1); {rnd(float(pe_), 2)}% (A1).', 3)


@R.add('ch01-st4', 'C3', (2, 5), 'short')
def bounds_calc(rng, slot):
    acc = rng.choice([1, Fr(1, 10)])
    a = Fr(rng.randint(30, 120)) if acc == 1 else Fr(rng.randint(30, 120), 10)
    b = Fr(rng.randint(10, 60)) if acc == 1 else Fr(rng.randint(10, 60), 10)
    h = Fr(acc) / 2
    unit = rng.choice(['cm', 'm'])
    acc_t = f'the nearest {unit}' if acc == 1 else '1 decimal place'
    kind = rng.choice(['area', 'perim', 'diff'])
    if kind == 'area':
        lo, hi = (a - h) * (b - h), (a + h) * (b + h)
        return short(f'A rectangle measures {g(float(a), 4)} {unit} by {g(float(b), 4)} {unit}, each to {acc_t}. Find the lower and upper bounds of its area.',
                     f'lower {g(float(lo), 6)} {unit}², upper {g(float(hi), 6)} {unit}²', f'Bounds of each side ±{g(float(h))} (M1); LB {g(float(a - h), 5)} × {g(float(b - h), 5)} (A1); UB {g(float(a + h), 5)} × {g(float(b + h), 5)} (A1).', 3)
    if kind == 'perim':
        lo, hi = 2 * (a + b - 2 * h), 2 * (a + b + 2 * h)
        return short(f'A rectangular frame measures {g(float(a), 4)} {unit} by {g(float(b), 4)} {unit}, each to {acc_t}. Find the lower and upper bounds of its perimeter.',
                     f'lower {g(float(lo), 6)} {unit}, upper {g(float(hi), 6)} {unit}', f'Bounds ±{g(float(h))} on each side (M1); LB (A1); UB (A1).', 3)
    if a <= b:
        a, b = b + 5, a
    lo, hi = (a - h) - (b + h), (a + h) - (b - h)
    return short(f'Two lengths are {g(float(a), 4)} {unit} and {g(float(b), 4)} {unit}, each to {acc_t}. Find the lower and upper bounds of their difference.',
                 f'lower {g(float(lo), 6)} {unit}, upper {g(float(hi), 6)} {unit}', f'LB = LB(a) − UB(b) (M1 A1); UB = UB(a) − LB(b) (A1).', 3)


@R.add('ch01-st4', 'C2', (2, 4), 'explain')
def error_explain(rng, slot):
    who, who2 = two_names(rng)
    e1, a1 = rng.randint(10, 40), 0
    a1 = e1 + rng.randint(1, 3)
    e2 = rng.randint(300, 900)
    a2 = e2 + rng.randint(5, 20)
    p1, p2 = (a1 - e1) / e1 * 100, (a2 - e2) / e2 * 100
    if rng.random() < 0.5:
        better = who if p1 < p2 else who2
        return explain(f'{who} estimates a {e1} cm book is {a1} cm long; {who2} estimates a {e2} cm desk is {a2} cm long. {who2} says {who} was more accurate because the error was smaller. Explain, using percentage error, who was more accurate.',
                       f'{who}: {r2(p1, 2)}%; {who2}: {r2(p2, 2)}%; so {better} was relatively more accurate – the size of the error must be compared with the size of the object.',
                       'Both percentage errors (A1); comparison justified (R1).', 2)
    return explain(f'{who} says the percentage error of estimating {e1} as {a1} is |{a1} − {e1}| ÷ {a1} × 100 = {r2((a1 - e1) / a1 * 100, 2)}%. Explain the mistake and correct it.',
                   f'Divide by the exact value {e1}, not the estimate: {r2(p1, 2)}%.', 'Mistake identified (R1); correct value (A1).', 2)


@R.add('ch01-st4', 'C4', (3, 5), 'multi_step')
def error_task(rng, slot):
    city = rng.choice(CITIES)
    kind = rng.choice(['pi', 'crowd', 'scale', 'speed'])
    if kind == 'pi':
        approx = [('22/7', 22 / 7), ('3.14', 3.14), ('355/113', 355 / 113), ('3', 3.0), ('√10', math.sqrt(10))]
        ch = rng.sample(approx, 3)
        errs = [(t, abs(v - math.pi) / math.pi * 100) for t, v in ch]
        best = min(errs, key=lambda e: e[1])[0]
        r = rng.randint(5, 40)
        ans = f'(a) ' + '; '.join(f'{t}: {rsf(e, 3)}%' for t, e in errs) + f' (b) {best} (c) with π: {dp(2 * math.pi * r)} cm; with {best}: {dp(2 * dict(ch)[best] * r)} cm (2 d.p.) (d) more accurate approximations matter for large or precise objects'
        q_ = (f'Students in {city} compare approximations for π: {", ".join(t for t, _ in ch)}. (a) Find the percentage error of each, to 3 s.f. (b) State which is the most accurate. '
              f'(c) Find the circumference of a circle of radius {r} cm using π and using your best approximation. (d) Comment on when the choice of approximation matters.')
    elif kind == 'crowd':
        E = rng.randint(20, 80) * 1000 + rng.randint(0, 999)
        ests = [round(E * rng.uniform(0.8, 1.2), -3) for _ in range(3)]
        n1, n2 = two_names(rng)
        names = [n1, n2, 'the police']
        errs = [abs(a - E) / E * 100 for a in ests]
        best = names[errs.index(min(errs))]
        ans = '(a) ' + '; '.join(f'{nm}: {r2(e, 2)}%' for nm, e in zip(names, errs)) + f' (b) {best} (c) {big(E)} people to the nearest 1000 is {big(round(E, -3))}; bounds {big(round(E, -3) - 500)} ≤ n < {big(round(E, -3) + 500)} (d) e.g. counting in a sample area and scaling up'
        q_ = (f'The ticket scanners at a festival in {city} recorded {big(E)} people. Estimates were: {n1} {big(ests[0])}, {n2} {big(ests[1])}, the police {big(ests[2])}. (a) Find each percentage error to 2 d.p. '
              f'(b) Who was most accurate? (c) Round the true figure to the nearest thousand and give the bounds that rounded value represents. (d) Suggest a method that would give a better estimate.')
    elif kind == 'scale':
        true = Fr(rng.randint(500, 3000), 10)
        meas = true + Fr(rng.choice([-1, 1]) * rng.randint(2, 15), 10)
        pe1 = abs(meas - true) / true * 100
        ans = f'(a) {g(float(abs(meas - true)), 3)} g (b) {rnd(float(pe1), 2)}% (c) {"yes" if pe1 <= 1 else "no"} – the limit is 1% (d) the same absolute error is a larger percentage of a smaller mass'
        q_ = (f'A market inspector in {city} checks a scale with a certified mass of {g(float(true), 5)} g; the scale reads {g(float(meas), 5)} g. (a) Find the absolute error. (b) Find the percentage error to 2 d.p. '
              f'(c) The law allows 1% error. Does the scale pass? (d) Explain why the same scale may fail when weighing small items.')
    else:
        d = rng.choice([100, 200, 400])
        t = Fr(rng.randint(110, 600), 10) if d > 100 else Fr(rng.randint(100, 160), 10)
        lo_v, hi_v = (d - Fr(1, 2)) / (t + Fr(1, 20)), (d + Fr(1, 2)) / (t - Fr(1, 20))
        ans = f'(a) d in [{g(d - 0.5, 5)}, {g(d + 0.5, 5)}), t in [{g(float(t) - 0.05, 5)}, {g(float(t) + 0.05, 5)}) (b) {g(float(d / t), 4)} m/s (c) lower {rsf(float(lo_v), 4)} m/s, upper {rsf(float(hi_v), 4)} m/s (d) max distance ÷ min time gives the largest speed'
        q_ = (f'At an athletics meeting in {city}, a runner covers {d} m (to the nearest metre) in {g(float(t), 4)} s (to the nearest 0.1 s). (a) Write the bounds of the distance and the time. (b) Find the average speed using the recorded values, to 4 s.f. '
              f'(c) Find the lower and upper bounds of the speed to 4 s.f. (d) Explain which bounds you used for the upper bound of speed.')
    return short(q_, ans, f'{ans}. Percentage error or bounds formula used correctly (M1 A1 A1); comparison or check carried out (D: R1); conclusion communicated with suitable accuracy (C1).', 6, 'multi_step', 'G5')



# =============================================================================================
# ch02 Sequences and Financial Mathematics
# =============================================================================================
R.facts('ch02-st1', F(
    terms=[('arithmetic sequence', 'a sequence in which each term is found by adding the same number, the common difference d, to the previous term'),
           ('common difference', 'the constant amount d = u(n+1) − u(n) between consecutive terms of an arithmetic sequence'),
           ('arithmetic series', 'the sum of the terms of an arithmetic sequence, Sₙ = n/2 (2u₁ + (n − 1)d) = n/2 (u₁ + uₙ)')],
    facts=[('What is the common difference of 17, 13, 9, 5, …?', '−4', ['4', '−13', '13/17'], '13 − 17 = −4.'),
           ('Which formula gives the n-th term of an arithmetic sequence?', 'uₙ = u₁ + (n − 1)d', ['uₙ = u₁ + nd', 'uₙ = u₁ × dⁿ⁻¹', 'uₙ = n/2 (u₁ + d)'], 'Start at u₁ and add d a total of n − 1 times.'),
           ('Find the sum 1 + 2 + 3 + … + 100.', '5050', ['5000', '10100', '4950'], 'S = 100/2 × (1 + 100) = 5050.')],
    why=[('Explain why the n-th term formula uses (n − 1)d and not nd.', 'The first term already is u₁; to reach the n-th term you take n − 1 steps of size d.'),
         ('Explain why Sₙ = n/2 (u₁ + uₙ).', 'Writing the series forwards and backwards and adding gives n pairs, each equal to u₁ + uₙ; this is twice the sum.'),
         ('Explain how the graph of an arithmetic sequence shows its common difference.', 'The points (n, uₙ) lie on a straight line whose gradient is d.')],
    misc=[('In 5, 8, 11, …, the 20th term is 5 + 20 × 3 = 65.', 'Use (n − 1)d: u₂₀ = 5 + 19 × 3 = 62.'),
          ('An arithmetic sequence with a negative difference must have negative terms.', 'Terms decrease but can stay positive for a while, e.g. 50, 45, 40, …')],
))


def _seq(a, d, n):
    return [a + i * d for i in range(n)]


@R.add('ch02-st1', 'C1', (1, 3), 'mcq')
def arith_mcq(rng, slot):
    a, d = rng.randint(-10, 20), rng.choice([v for v in range(-7, 9) if v])
    n = rng.randint(8, 30)
    un = a + (n - 1) * d
    return mcq(rng, f'The arithmetic sequence {", ".join(m(t) for t in _seq(a, d, 4))}, … has n-th term uₙ. Find u{n}.'.replace(f'u{n}', 'u' + str(n).translate(str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉'))),
               m(un), [m(a + n * d), m(a * n + d), m(a + (n - 2) * d)], f'u₁ = {m(a)}, d = {m(d)}: {m(a)} + ({n} − 1)({m(d)}) = {m(un)}.')


def _sub(n):
    return str(n).translate(str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉'))


@R.add('ch02-st1', 'C3', (1, 4), 'short')
def arith_terms(rng, slot):
    a, d = rng.randint(-15, 30), rng.choice([v for v in range(-9, 13) if v])
    if slot.d <= 2:
        n = rng.randint(10, 40)
        un, Sn = a + (n - 1) * d, Fr(n, 2) * (2 * a + (n - 1) * d)
        return short(f'For the arithmetic sequence {", ".join(m(t) for t in _seq(a, d, 3))}, …, find u{_sub(n)} and S{_sub(n)}.', f'u{_sub(n)} = {m(un)}; S{_sub(n)} = {fx(Sn)}',
                     f'd = {m(d)} (A1); u{_sub(n)} = {m(a)} + {n - 1}({m(d)}) = {m(un)} (A1); S{_sub(n)} = {n}/2 ({m(2 * a)} + {n - 1}({m(d)})) = {fx(Sn)} (M1 A1).', 4)
    p, q = sorted(rng.sample(range(2, 25), 2))
    up, uq = a + (p - 1) * d, a + (q - 1) * d
    k = rng.randint(30, 60)
    return short(f'In an arithmetic sequence, u{_sub(p)} = {m(up)} and u{_sub(q)} = {m(uq)}. Find the first term, the common difference and u{_sub(k)}.',
                 f'u₁ = {m(a)}, d = {m(d)}, u{_sub(k)} = {m(a + (k - 1) * d)}',
                 f'{q - p}d = {m(uq - up)} (M1) → d = {m(d)} (A1); u₁ = {m(up)} − {p - 1}({m(d)}) = {m(a)} (A1); u{_sub(k)} = {m(a + (k - 1) * d)} (A1).', 4)


@R.add('ch02-st1', 'C3', (2, 5), 'short')
def arith_count(rng, slot):
    a, d = rng.randint(1, 40), rng.randint(2, 9)
    n = rng.randint(12, 45)
    last = a + (n - 1) * d
    if rng.random() < 0.5:
        S = n * (a + last) // 2 if (n * (a + last)) % 2 == 0 else Fr(n * (a + last), 2)
        return short(f'Find the sum of the arithmetic series {a} + {a + d} + {a + 2 * d} + … + {last}.', fx(Fr(S)),
                     f'n = ({last} − {a})/{d} + 1 = {n} (M1 A1); S = {n}/2 ({a} + {last}) = {fx(Fr(S))} (A1).', 3)
    T = rng.randint(400, 3000)
    k = next(i for i in range(1, 500) if Fr(i, 2) * (2 * a + (i - 1) * d) > T)
    return short(f'For the series {a} + {a + d} + {a + 2 * d} + …, find the smallest number of terms whose sum exceeds {big(T)}.', f'{k} terms',
                 f'Sₙ = n/2 ({2 * a} + {d}(n − 1)) > {T} (M1); S{_sub(k - 1)} = {fx(Fr(k - 1, 2) * (2 * a + (k - 2) * d))}, S{_sub(k)} = {fx(Fr(k, 2) * (2 * a + (k - 1) * d))} (A1); n = {k} (A1).', 3)


@R.add('ch02-st1', 'C2', (2, 4), 'explain')
def arith_explain(rng, slot):
    who = name(rng)
    a, d = rng.randint(2, 15), rng.randint(3, 9)
    kind = rng.choice(['member', 'gauss', 'nd'])
    if kind == 'member':
        t = a + d * rng.randint(20, 60) + rng.randint(1, d - 1)
        return explain(f'Explain whether {t} is a term of the sequence {a}, {a + d}, {a + 2 * d}, ….',
                       f'uₙ = {a} + (n − 1){d}; {t} − {a} = {t - a}, which is not a multiple of {d}, so n would not be a whole number: {t} is not a term.',
                       'n-th term equation set up (M1); non-integer n interpreted (R1).', 2)
    if kind == 'gauss':
        n = rng.choice([50, 60, 80, 100, 200])
        return explain(f'Explain how to find 1 + 2 + … + {n} quickly by pairing terms.',
                       f'Pair 1 with {n}, 2 with {n - 1}, …: each pair is {n + 1} and there are {n // 2} pairs, so the sum is {n // 2} × {n + 1} = {n // 2 * (n + 1)}.',
                       'Pairing idea (R1); total (A1).', 2)
    n = rng.randint(10, 30)
    return explain(f'{who} says the {ordinal(n)} term of {a}, {a + d}, {a + 2 * d}, … is {a + n * d}. Explain the mistake and correct it.',
                   f'{who} added {d} {n} times; only {n - 1} steps are needed after the first term: {a} + {n - 1} × {d} = {a + (n - 1) * d}.',
                   'Mistake identified (R1); correct term (A1).', 2)


@R.add('ch02-st1', 'C4', (3, 5), 'multi_step')
def arith_task(rng, slot):
    city, country, cur, cname = place(rng)
    kind = rng.choice(['theatre', 'savings', 'training', 'logs'])
    if kind == 'theatre':
        a, d, n = rng.randint(14, 30), rng.randint(2, 4), rng.randint(18, 32)
        T = Fr(n, 2) * (2 * a + (n - 1) * d)
        k = rng.randint(n // 2, n)
        cap = int(T) - rng.randint(50, 200)
        rows = next(i for i in range(1, n + 1) if Fr(i, 2) * (2 * a + (i - 1) * d) >= cap)
        ans = f'(a) {a + (n - 1) * d} seats (b) {fx(T)} seats (c) row {k} has {a + (k - 1) * d} seats (d) {rows} rows'
        q_ = (f'A theatre in {city} has {a} seats in the front row, and each row has {d} more seats than the row in front. There are {n} rows. (a) Find the number of seats in the back row. (b) Find the total number of seats. '
              f'(c) How many seats are in row {k}? (d) A school group of {cap} must fill rows from the front. How many rows will they need?')
    elif kind == 'savings':
        a, d = rng.choice([20, 25, 30, 40, 50]), rng.choice([5, 10, 15])
        n = 12
        T = Fr(n, 2) * (2 * a + (n - 1) * d)
        goal = int(T) + rng.randint(100, 600)
        k = next(i for i in range(1, 100) if Fr(i, 2) * (2 * a + (i - 1) * d) >= goal)
        ans = f'(a) {money(cur, a + 11 * d, 0)} (b) {money(cur, int(T), 0)} (c) month {k} (d) the amount saved each month grows linearly, so the total grows quadratically'
        q_ = (f'{name(rng)} in {city} saves {money(cur, a, 0)} in January and then {money(cur, d, 0)} more each month than the month before. (a) How much is saved in December? (b) Find the total saved in the year. '
              f'(c) In which month does the total first reach {money(cur, goal, 0)}, if the pattern continues into the next year? (d) Describe how the monthly amount and the running total change.')
    elif kind == 'training':
        a, d = rng.choice([2, 3, 4, 5]), Fr(rng.choice([1, 2, 3, 5]), 2)
        target = rng.choice([21, 25, 30, 42])
        n = next(i for i in range(1, 200) if a + (i - 1) * d >= target)
        tot = Fr(n, 2) * (2 * a + (n - 1) * d)
        ans = f'(a) uₙ = {a} + (n − 1)({g(float(d))}) (b) week {n} (c) {g(float(tot), 5)} km (d) the increase cannot continue forever – fatigue/injury limits the model'
        q_ = (f'A runner in {city} trains for a race: she runs {a} km in week 1 and increases her long run by {g(float(d))} km every week. (a) Write a formula for the distance in week n. '
              f'(b) In which week does her long run first reach at least {target} km? (c) Find the total distance of her long runs up to and including that week. (d) Comment on the limitations of the model.')
    else:
        top = rng.randint(1, 6)
        n = rng.randint(8, 20)
        bottom = top + n - 1
        tot = n * (top + bottom) // 2
        ans = f'(a) {bottom} (b) {tot} logs (c) {next(i for i in range(1, 200) if i * (2 * top + i - 1) // 2 >= tot + 40)} rows for at least {tot + 40} logs (d) S = n/2 (2 × {top} + (n − 1))'
        q_ = (f'Logs at a timber yard in {city} are stacked in rows: the top row has {top} logs and each row below has one more log, with {n} rows. (a) How many logs are in the bottom row? '
              f'(b) Find the total number of logs. (c) How many rows would be needed (same top row) to hold at least {tot + 40} logs? (d) Write a formula for the number of logs in n rows.')
    return short(q_, ans, f'{ans}. Arithmetic model identified (A1); n-th term and sum formulas applied (M1 A1 A1); answer interpreted in context (D: R1 C1).', 6, 'multi_step', 'G5')


R.facts('ch02-st2', F(
    terms=[('geometric sequence', 'a sequence in which each term is found by multiplying the previous term by the same number, the common ratio r'),
           ('common ratio', 'the constant r = u(n+1) ÷ u(n) between consecutive terms of a geometric sequence'),
           ('geometric series', 'the sum of the terms of a geometric sequence, Sₙ = u₁(rⁿ − 1)/(r − 1) for r ≠ 1')],
    facts=[('What is the common ratio of 48, 24, 12, 6, …?', '1/2', ['−24', '2', '−1/2'], '24 ÷ 48 = 1/2.'),
           ('Which formula gives the n-th term of a geometric sequence?', 'uₙ = u₁rⁿ⁻¹', ['uₙ = u₁rⁿ', 'uₙ = u₁ + (n − 1)r', 'uₙ = (u₁r)ⁿ⁻¹'], 'Multiply by r a total of n − 1 times.'),
           ('Find the sum of the first 5 terms of 1, 3, 9, 27, ….', '121', ['81', '243', '120'], '(3⁵ − 1)/(3 − 1) = 242/2 = 121.')],
    why=[('Explain why a geometric sequence with 0 < r < 1 has terms that get smaller but never reach zero.', 'Each term is a fraction of the previous positive term, so it is always positive but shrinks towards 0.'),
         ('Explain how to tell whether a sequence is arithmetic or geometric.', 'Check differences and ratios of consecutive terms: a constant difference means arithmetic, a constant ratio means geometric.'),
         ('Explain why the terms of a geometric sequence with r < 0 alternate in sign.', 'Multiplying by a negative number changes the sign each time.')],
    misc=[('The 10th term of 3, 6, 12, … is 3 × 2¹⁰.', 'u₁₀ = 3 × 2⁹ = 1536; the exponent is n − 1.'),
          ('2, 4, 6, 8, … is geometric because the numbers double.', 'Only the first step doubles; the differences are constant (2), so it is arithmetic.')],
))


@R.add('ch02-st2', 'C1', (1, 3), 'mcq')
def geo_mcq(rng, slot):
    a = rng.choice([1, 2, 3, 4, 5, 6, 81, 64, 128])
    r = rng.choice([2, 3, -2, Fr(1, 2)]) if a < 50 else rng.choice([Fr(1, 2), Fr(1, 4), Fr(-1, 2)]) if a != 81 else Fr(1, 3)
    n = rng.randint(5, 8)
    un = a * Fr(r) ** (n - 1)
    return mcq(rng, f'Find u{_sub(n)} for the geometric sequence {", ".join(fx(a * Fr(r) ** i) for i in range(3))}, ….', fx(un),
               [fx(a * Fr(r) ** n), fx(a * Fr(r) ** (n - 2)), fx(a + (n - 1) * Fr(r))], f'r = {fx(r)}; u{_sub(n)} = {a} × ({fx(r)}){sup(n - 1)} = {fx(un)}.')


@R.add('ch02-st2', 'C3', (1, 4), 'short')
def geo_terms(rng, slot):
    a = rng.randint(2, 9)
    r = rng.choice([2, 3, -2, -3, Fr(1, 2), Fr(3, 2)])
    n = rng.randint(6, 10)
    un = a * Fr(r) ** (n - 1)
    Sn = a * (Fr(r) ** n - 1) / (Fr(r) - 1)
    if slot.d <= 2:
        return short(f'For the geometric sequence {", ".join(fx(a * Fr(r) ** i) for i in range(3))}, …, find the common ratio and u{_sub(n)}.', f'r = {fx(r)}; u{_sub(n)} = {fx(un)}',
                     f'r = {fx(a * Fr(r))} ÷ {a} = {fx(r)} (A1); u{_sub(n)} = {a}({fx(r)}){sup(n - 1)} (M1) = {fx(un)} (A1).', 3)
    if rng.random() < 0.5:
        return short(f'Find the sum of the first {n} terms of the geometric sequence {", ".join(fx(a * Fr(r) ** i) for i in range(3))}, ….', fx(Sn),
                     f'r = {fx(r)} (A1); Sₙ = {a}(({fx(r)}){sup(n)} − 1)/({fx(r)} − 1) (M1); = {fx(Sn)} (A1).', 3)
    p, q = 2, rng.randint(4, 6)
    rr = rng.choice([2, 3, -2])
    up, uq = a * rr ** (p - 1), a * rr ** (q - 1)
    return short(f'In a geometric sequence, u₂ = {m(up)} and u{_sub(q)} = {m(uq)}. Find the possible values of the common ratio and the first term.',
                 (f'r = {m(rr)}, u₁ = {a}' if (q - p) % 2 else f'r = {abs(rr)}, u₁ = {fx(Fr(up, abs(rr)))}; or r = −{abs(rr)}, u₁ = {fx(Fr(up, -abs(rr)))}'),
                 f'r{sup(q - p)} = {m(uq)} ÷ {m(up)} = {m(uq // up)} (M1); r = {"" if (q - p) % 2 else "±"}{abs(rr) if (q - p) % 2 == 0 else rr} (A1); u₁ = u₂ ÷ r (A1).', 3)


@R.add('ch02-st2', 'C3', (2, 5), 'short')
def geo_exceed(rng, slot):
    a = rng.randint(2, 12)
    r = rng.choice([2, 3, Fr(3, 2), Fr(5, 4)])
    T = rng.choice([1000, 5000, 10000, 50000, 100000])
    n = next(i for i in range(1, 200) if a * Fr(r) ** (i - 1) > T)
    if rng.random() < 0.5:
        return short(f'Find the first term of the geometric sequence {", ".join(fx(a * Fr(r) ** i) for i in range(3))}, … that is greater than {big(T)}, and state its position.',
                     f'u{_sub(n)} {"≈ " + rsf(float(a * Fr(r) ** (n - 1)), 5) if Fr(r).denominator > 1 else "= " + big(a * Fr(r) ** (n - 1))}',
                     f'{a}({fx(r)})ⁿ⁻¹ > {T} (M1); u{_sub(n - 1)} ≈ {rsf(float(a * Fr(r) ** (n - 2)), 4)}, u{_sub(n)} ≈ {rsf(float(a * Fr(r) ** (n - 1)), 4)} (A1); n = {n} (A1).', 3)
    k = next(i for i in range(1, 200) if a * (Fr(r) ** i - 1) / (Fr(r) - 1) > T)
    return short(f'How many terms of the geometric series {" + ".join(fx(a * Fr(r) ** i) for i in range(3))} + … are needed for the sum to exceed {big(T)}?', f'{k} terms',
                 f'Sₙ = {a}(({fx(r)})ⁿ − 1)/({fx(r)} − 1) > {T} (M1); S{_sub(k - 1)} ≈ {rsf(float(a * (Fr(r) ** (k - 1) - 1) / (Fr(r) - 1)), 4)}, S{_sub(k)} ≈ {rsf(float(a * (Fr(r) ** k - 1) / (Fr(r) - 1)), 4)} (A1); {k} (A1).', 3)


@R.add('ch02-st2', 'C2', (2, 4), 'explain')
def geo_explain(rng, slot):
    who = name(rng)
    a, d = rng.randint(2, 6), rng.randint(2, 4)
    kind = rng.choice(['which', 'exp', 'infinite'])
    if kind == 'which':
        s1 = [a * d ** i for i in range(4)]
        s2 = [a + d * i for i in range(4)]
        return explain(f'{who} has two sequences: P = {", ".join(map(str, s1))}, … and Q = {", ".join(map(str, s2))}, …. Explain which is geometric and which is arithmetic, and which grows faster in the long run.',
                       f'P has constant ratio {d} (geometric); Q has constant difference {d} (arithmetic). Geometric growth multiplies, so P eventually grows much faster.',
                       'Both identified with reason (R1); long-term comparison (R1).', 2)
    if kind == 'exp':
        n = rng.randint(8, 15)
        return explain(f'{who} writes u{_sub(n)} = {a} × {d}{sup(n)} for the sequence {a}, {a * d}, {a * d * d}, …. Explain the mistake and correct it.',
                       f'u₁ = {a} × {d}⁰, so the exponent is n − 1: u{_sub(n)} = {a} × {d}{sup(n - 1)} = {big(a * d ** (n - 1))}.',
                       'Exponent n − 1 explained (R1); correct value (A1).', 2)
    S = Fr(a, 1) / (1 - Fr(1, d))
    return explain(f'Explain why the sum {a} + {fx(Fr(a, d))} + {fx(Fr(a, d * d))} + … never exceeds {fx(S)}, however many terms are added.',
                   f'r = 1/{d}, so each term is a fraction of the last and the terms shrink towards 0; the sums approach u₁/(1 − r) = {a}/(1 − 1/{d}) = {fx(S)} but never reach it.',
                   'Ratio and shrinking terms (R1); limit value (A1).', 2)


@R.add('ch02-st2', 'C4', (3, 5), 'multi_step')
def geo_task(rng, slot):
    city, country, cur, cname = place(rng)
    kind = rng.choice(['ball', 'salary', 'grains', 'virus'])
    if kind == 'ball':
        h0 = rng.choice([2, 3, 4, 5, 6, 8])
        r = Fr(rng.choice([3, 3, 4, 7]), rng.choice([5, 4, 10, 8]))
        if r >= 1:
            r = Fr(3, 5)
        k = rng.randint(4, 7)
        hk = h0 * r ** k
        dist = h0 + 2 * sum(h0 * r ** i for i in range(1, k))
        n = next(i for i in range(1, 100) if h0 * r ** i < Fr(1, 10))
        ans = f'(a) {rsf(float(h0 * r), 3)} m, {rsf(float(h0 * r ** 2), 3)} m (b) {rsf(float(hk), 3)} m (c) after bounce {n} (d) {rsf(float(dist), 4)} m when it lands for the {ordinal(k)} time'
        q_ = (f'A ball is dropped from {h0} m in a sports lab in {city}. After each bounce it rises to {fx(r)} of its previous height. (a) Find the heights of the first two bounces. (b) Find the height of the {ordinal(k)} bounce. '
              f'(c) After which bounce is the height first less than 10 cm? (d) Find the total vertical distance travelled from the drop until it lands for the {ordinal(k)} time.')
    elif kind == 'salary':
        S0 = rng.choice([30000, 36000, 42000, 48000, 55000])
        p = rng.choice([2, 2.5, 3, 3.5, 4, 5])
        n = 10
        r = 1 + p / 100
        ans = f'(a) {money(cur, S0 * r ** 4)} (b) {money(cur, S0 * (r ** n - 1) / (r - 1))} (c) year {next(i for i in range(1, 100) if S0 * r ** (i - 1) >= 1.5 * S0)} (d) a fixed raise of {money(cur, S0 * p / 100, 0)} gives {money(cur, n / 2 * (2 * S0 + (n - 1) * S0 * p / 100))} in total, less than the percentage plan'
        q_ = (f'An engineer in {city} starts on a salary of {money(cur, S0, 0)} a year with a {g(p)}% rise every year. (a) Find the salary in year 5. (b) Find the total earned over the first {n} years. '
              f'(c) In which year does the salary first reach 1.5 times the starting salary? (d) Compare with a plan that adds a fixed {money(cur, S0 * p / 100, 0)} every year.')
    elif kind == 'grains':
        s = rng.choice([1, 2, 3])
        k = rng.choice([16, 20, 24, 32])
        tot = s * (2 ** k - 1)
        ans = f'(a) {s} × 2ⁿ⁻¹ (b) {big(s * 2 ** (k - 1))} (c) {big(tot)} (d) about {rsf(tot * 0.065 / 1e6, 3)} tonnes; the doubling grows far faster than people expect'
        q_ = (f'In a puzzle told in {city}, {s} grain{"s" if s > 1 else ""} of rice {"are" if s > 1 else "is"} placed on the first square of a board, and each square has double the previous square. (a) Write an expression for the number on square n. '
              f'(b) How many are on square {k}? (c) Find the total on the first {k} squares. (d) A grain has mass about 0.065 g. Estimate the total mass in tonnes and comment.')
    else:
        c0 = rng.choice([10, 20, 30, 50])
        r = Fr(rng.choice([13, 14, 15, 16, 18]), 10)
        n = rng.randint(6, 10)
        ans = f'(a) r = {g(float(r))} (b) {big(round(float(c0 * r ** (n - 1))))} (c) {big(round(float(c0 * (r ** n - 1) / (r - 1))))} (d) control measures reduce r; if r < 1 the weekly cases fall'
        q_ = (f'Health officials in {city} record {c0}, {g(float(c0 * r), 4)}, {g(float(c0 * r * r), 4)} new cases of a virus in weeks 1, 2, 3. (a) Show that the data fit a geometric model and find r. (b) Predict the new cases in week {n}. '
              f'(c) Predict the total cases in the first {n} weeks. (d) Explain how measures such as vaccination would change the model.')
    return short(q_, ans, f'{ans}. Geometric model identified with r (A1); n-th term and sum used (M1 A1 A1); pattern / limitation discussed in context (B/D: R1 C1).', 6, 'multi_step', 'G5')


R.facts('ch02-st3', F(
    terms=[('compound interest', 'interest calculated on the principal and on the interest already added, so the amount grows geometrically: A = P(1 + r/(100k))^(kn)'),
           ('depreciation', 'a decrease in value over time, often by a fixed percentage each year: V = V₀(1 − r/100)ⁿ'),
           ('multiplier', 'the number you multiply by for a percentage change, e.g. 1.04 for a 4% increase or 0.85 for a 15% decrease'),
           ('compounding period', 'how often interest is added: yearly (k = 1), half-yearly (k = 2), quarterly (k = 4) or monthly (k = 12)')],
    facts=[('What is the multiplier for a 6% depreciation?', '0.94', ['1.06', '0.06', '0.6'], '100% − 6% = 94%.'),
           ('€1000 is invested at 5% compound interest per year. Its value after 2 years is:', '€1102.50', ['€1100.00', '€1050.00', '€1105.00'], '1000 × 1.05² = 1102.50.'),
           ('Interest of 6% per year compounded monthly uses which rate per month?', '0.5%', ['6%', '0.6%', '72%'], '6 ÷ 12 = 0.5% per month.')],
    why=[('Explain why compound interest earns more than simple interest at the same rate.', 'Compound interest also earns interest on previous interest, so the amount grows by a larger amount each year.'),
         ('Explain why more frequent compounding gives a slightly larger final amount.', 'Interest is added sooner and then starts earning interest itself; e.g. 1.005¹² ≈ 1.0617 > 1.06.'),
         ('Explain why a value depreciating by a fixed percentage never reaches zero.', 'Each year it is multiplied by a positive number less than 1, so it shrinks but stays positive.')],
    misc=[('A 10% rise followed by a 10% fall returns to the original value.', '1.1 × 0.9 = 0.99, so the value is 1% lower.'),
          ('Depreciation of 20% per year means the item is worthless after 5 years.', 'It keeps 80% each year: 0.8⁵ ≈ 0.33, so about a third of the value is left.')],
))

_COMP = [(1, 'yearly'), (2, 'half-yearly'), (4, 'quarterly'), (12, 'monthly')]


@R.add('ch02-st3', 'C1', (1, 3), 'mcq')
def multiplier_mcq(rng, slot):
    p = rng.choice([2, 3, 4, 5, 6, 8, 12, 15, 18, 25])
    up = rng.random() < 0.5
    corr = g(1 + p / 100, 4) if up else g(1 - p / 100, 4)
    wr = [g(1 - p / 100, 4) if up else g(1 + p / 100, 4), g(p / 100, 4), g(1 + p / 10, 4) if up else g(p / 10, 4)]
    return mcq(rng, f'Which multiplier represents {_a(str(p) + "% " + ("increase" if up else "decrease"))}?', corr, wr,
               f'{100 + p if up else 100 - p}% = {corr}.')


@R.add('ch02-st3', 'C3', (1, 4), 'short')
def compound_calc(rng, slot):
    city, country, cur, cname = place(rng)
    P = rng.choice([1500, 2000, 2500, 4000, 5000, 8000, 12000, 15000, 20000])
    rate = rng.choice([1.5, 2, 2.4, 3, 3.6, 4, 4.5, 5, 6])
    n = rng.randint(3, 12)
    k, kt = rng.choice(_COMP) if slot.d >= 3 else (1, 'yearly')
    A = P * (1 + rate / (100 * k)) ** (k * n)
    return short(f'{name(rng)} invests {money(cur, P, 0)} in a bank in {city} at {g(rate)}% per year, compounded {kt}. Find the value after {n} years and the interest earned.',
                 f'{cash(cur, A)}; interest {cash(cur, A - P)}',
                 f'A = {P}(1 + {g(rate)}/{100 * k})^{k * n} (M1 A1); {cash(cur, A)} (A1); interest {cash(cur, A - P)} (A1).', 4)


@R.add('ch02-st3', 'C3', (2, 5), 'short')
def depreciation_calc(rng, slot):
    city, country, cur, cname = place(rng)
    item = rng.choice(['car', 'laptop', 'delivery van', 'tractor', 'e-bike', 'printing machine'])
    V0 = rng.choice([1200, 1800, 2500, 6000, 18000, 24000, 32000, 45000])
    p = rng.choice([8, 10, 12, 15, 18, 20, 25])
    n = rng.randint(3, 8)
    V = V0 * (1 - p / 100) ** n
    if rng.random() < 0.5:
        return short(f'{_a(item).capitalize()} bought in {city} for {money(cur, V0, 0)} depreciates by {p}% per year. Find its value after {n} years.', cash(cur, V),
                     f'Multiplier {g(1 - p / 100)} (A1); {V0} × {g(1 - p / 100)}{sup(n)} (M1); {cash(cur, V)} (A1).', 3)
    half = next(i for i in range(1, 100) if (1 - p / 100) ** i <= 0.5)
    return short(f'{_a(item).capitalize()} bought in {city} for {money(cur, V0, 0)} depreciates by {p}% per year. After how many whole years is it first worth half its original value or less?', f'{half} years',
                 f'{g(1 - p / 100)}ⁿ ≤ 0.5 (M1); {g(1 - p / 100)}{sup(half - 1)} ≈ {rsf((1 - p / 100) ** (half - 1), 3)}, {g(1 - p / 100)}{sup(half)} ≈ {rsf((1 - p / 100) ** half, 3)} (A1); {half} years (A1).', 3)


@R.add('ch02-st3', 'C3', (2, 5), 'short')
def reverse_compound(rng, slot):
    city, country, cur, cname = place(rng)
    P = rng.choice([2000, 3000, 4000, 5000, 6000, 7500, 10000])
    rate = rng.choice([2, 2.5, 3, 4, 5, 6])
    n = rng.randint(3, 8)
    A = round(P * (1 + rate / 100) ** n, 2)
    if rng.random() < 0.5:
        return short(f'An account in {city} pays {g(rate)}% compound interest per year. After {n} years it holds {cash(cur, A)}. Find the amount originally invested, to the nearest whole unit.', money(cur, round(A / (1 + rate / 100) ** n), 0),
                     f'P × {g(1 + rate / 100, 4)}{sup(n)} = {A} (M1); P = {A} ÷ {g(1 + rate / 100, 4)}{sup(n)} (A1); {money(cur, round(A / (1 + rate / 100) ** n), 0)} (A1).', 3)
    r_ = ((A / P) ** (1 / n) - 1) * 100
    return short(f'{money(cur, P, 0)} grows to {cash(cur, A)} in {n} years with annual compounding. Find the annual interest rate.', f'{rsf(r_, 3)}%',
                 f'(1 + r/100){sup(n)} = {A}/{P} (M1); 1 + r/100 = ({A}/{P})^(1/{n}) (A1); r = {rsf(r_, 3)}% (A1).', 3)


@R.add('ch02-st3', 'C2', (2, 4), 'explain')
def compound_explain(rng, slot):
    who = name(rng)
    city, country, cur, cname = place(rng)
    p = rng.choice([5, 10, 15, 20, 25])
    kind = rng.choice(['updown', 'simple', 'freq'])
    if kind == 'updown':
        return explain(f'A shop in {city} raises a price by {p}% and later reduces the new price by {p}%. {who} says the price is back to the original. Explain why this is wrong.',
                       f'The multipliers are {g(1 + p / 100)} and {g(1 - p / 100)}; their product is {g((1 + p / 100) * (1 - p / 100), 4)}, so the final price is {g(p * p / 100, 4)}% lower than the original.',
                       'Multipliers combined (M1); conclusion (R1).', 2)
    if kind == 'simple':
        P, r, n = rng.choice([1000, 2000, 5000]), rng.choice([3, 4, 5, 6]), rng.choice([5, 10, 15])
        ci, si = P * (1 + r / 100) ** n - P, P * r * n / 100
        return explain(f'Explain why {money(cur, P, 0)} at {r}% for {n} years earns more with compound interest than with simple interest, and find the difference.',
                       f'Simple: {cash(cur, si)}; compound: {cash(cur, ci)}. Compound interest also earns interest on interest, so it is {cash(cur, ci - si)} more.',
                       'Both interests (A1); reason (R1).', 2)
    r = rng.choice([4, 6, 8, 12])
    return explain(f'Explain why {r}% per year compounded monthly gives a little more than {r}% compounded yearly.',
                   f'Monthly: (1 + {r}/1200)¹² ≈ {g((1 + r / 1200) ** 12, 5)}, an effective rate of {rsf(((1 + r / 1200) ** 12 - 1) * 100, 3)}% > {r}%, because interest added earlier earns interest itself.',
                   'Effective rate (A1); reason (R1).', 2)


@R.add('ch02-st3', 'C4', (3, 5), 'multi_step')
def compound_task(rng, slot):
    city, country, cur, cname = place(rng)
    kind = rng.choice(['accounts', 'car', 'population', 'double'])
    if kind == 'accounts':
        P = rng.choice([5000, 8000, 10000, 15000])
        r1, k1 = rng.choice([(4.2, 1), (4.0, 1), (3.9, 1)])
        r2_, k2 = rng.choice([(4.0, 12), (3.9, 4), (4.1, 2)])
        n = rng.randint(5, 10)
        A1, A2 = P * (1 + r1 / 100 / k1) ** (k1 * n), P * (1 + r2_ / 100 / k2) ** (k2 * n)
        best = 'A' if A1 > A2 else 'B'
        ans = f'(a) A: {cash(cur, A1)} (b) B: {cash(cur, A2)} (c) account {best}, by {cash(cur, abs(A1 - A2))} (d) effective annual rates: A {rsf(((1 + r1 / 100 / k1) ** k1 - 1) * 100, 4)}%, B {rsf(((1 + r2_ / 100 / k2) ** k2 - 1) * 100, 4)}%'
        q_ = (f'{name(rng)} has {money(cur, P, 0)} to save in {city} for {n} years. Account A pays {g(r1)}% per year compounded {dict(_COMP)[k1]}; account B pays {g(r2_)}% per year compounded {dict(_COMP)[k2]}. '
              f'(a) Find the value in A after {n} years. (b) Find the value in B. (c) Which is better, and by how much? (d) Find the effective annual rate of each and explain how it helps the comparison.')
    elif kind == 'car':
        V0 = rng.choice([22000, 28000, 35000, 40000])
        p = rng.choice([12, 15, 18, 20])
        n = rng.randint(3, 6)
        V = V0 * (1 - p / 100) ** n
        yrs = next(i for i in range(1, 50) if V0 * (1 - p / 100) ** i < 0.25 * V0)
        ans = f'(a) V = {V0} × {g(1 - p / 100)}ⁿ (b) {cash(cur, V)} (c) {cash(cur, V0 - V)} ({rsf((V0 - V) / V0 * 100, 3)}% of the price) (d) during year {yrs}'
        q_ = (f'A new car costs {money(cur, V0, 0)} in {city} and loses {p}% of its value each year. (a) Write a formula for its value after n years. (b) Find its value after {n} years. '
              f'(c) Find the total loss in value over those years and express it as a percentage of the price. (d) In which year does it first fall below a quarter of its price?')
    elif kind == 'population':
        P0 = rng.randint(120, 900) * 1000
        p = rng.choice([1.2, 1.5, 1.8, 2.1, 2.5, 3.2])
        n = rng.randint(5, 15)
        Pn = P0 * (1 + p / 100) ** n
        yrs = next(i for i in range(1, 300) if (1 + p / 100) ** i >= 2)
        ans = f'(a) {g(1 + p / 100, 4)} (b) {big(round(Pn))} (c) {yrs} years (d) growth rates change (migration, birth rates), so long-term predictions are unreliable'
        q_ = (f'The population of {city} is {big(P0)} and is growing by {g(p)}% per year. (a) State the annual multiplier. (b) Predict the population in {n} years. '
              f'(c) After how many whole years will the population first be at least double? (d) Explain why this model may not be reliable for 50 years.')
    else:
        r = rng.choice([2, 3, 4, 6, 8, 9, 12])
        yrs = next(i for i in range(1, 300) if (1 + r / 100) ** i >= 2)
        ans = f'(a) {yrs} years (b) 72 ÷ {r} = {g(72 / r, 3)} years (c) {"close" if abs(yrs - 72 / r) <= 1 else "not very close"}: rule of 72 estimate {g(72 / r, 3)} vs {yrs} (d) the doubling time does not depend on the amount, because (1 + r/100)ⁿ = 2 does not contain P'
        q_ = (f'A bank in {city} advertises {r}% interest per year, compounded yearly. (a) Find the number of whole years for any deposit to first double. (b) The "rule of 72" says the doubling time is about 72 ÷ rate. Use it. '
              f'(c) Comment on how good the rule is for this rate. (d) Explain why the doubling time is the same for {money(cur, 100, 0)} as for {money(cur, 100000, 0)}.')
    return short(q_, ans, f'{ans}. Correct multiplier and formula (A1 M1); values calculated (A1 A1); comparison or limitation explained in context (D: R1 C1).', 6, 'multi_step', 'G5')


R.facts('ch02-st4', F(
    terms=[('loan', 'money borrowed that must be repaid with interest, usually in regular instalments'),
           ('flat-rate interest', 'interest calculated only on the original amount borrowed for the whole term: I = P × r/100 × n'),
           ('annuity / regular saving', 'equal deposits made at regular intervals into an account that pays compound interest'),
           ('total cost of credit', 'the total amount repaid minus the amount borrowed')],
    facts=[('A loan of $2000 at 8% flat rate for 3 years costs how much interest?', '$480', ['$160', '$519.42', '$2480'], '2000 × 0.08 × 3 = 480.'),
           ('Monthly repayments of $150 for 2 years total:', '$3600', ['$1800', '$300', '$150'], '150 × 24 = 3600.'),
           ('A longer loan term with the same rate usually means:', 'lower monthly payments but more total interest', ['higher payments and less interest', 'the same total interest', 'no interest'], 'Interest is paid for longer.')],
    why=[('Explain why a lower monthly repayment can cost more overall.', 'The lower payment usually comes from a longer term, so interest is charged for more months and the total repaid is larger.'),
         ('Explain why a flat-rate loan is more expensive than its rate suggests.', 'Interest is charged on the full amount for the whole term, even though the debt goes down as you repay it.'),
         ('Explain why starting to save earlier makes a large difference with compound interest.', 'Early deposits have more years to earn interest on interest, so they grow by a larger factor.')],
    misc=[('A loan of $1000 at 10% per year for 2 years always costs $200 in interest.', 'That is only true for flat-rate (simple) interest; with compound interest or reducing balance the total differs.'),
          ('Saving $100 a month for a year at interest gives exactly $1200.', 'Interest is added, so the total is more than $1200 (if the rate is positive).')],
))


@R.add('ch02-st4', 'C1', (1, 3), 'mcq')
def loan_mcq(rng, slot):
    city, country, cur, cname = place(rng)
    P = rng.choice([1200, 2400, 3000, 4800, 6000])
    r = rng.choice([5, 6, 8, 9, 10, 12])
    n = rng.choice([2, 3, 4, 5])
    I = P * r * n // 100
    return mcq(rng, f'A loan of {money(cur, P, 0)} is taken at {r}% flat-rate interest per year for {n} years. What is the monthly repayment?', cash(cur, (P + I) / (12 * n)),
               [cash(cur, P / (12 * n)), cash(cur, (P + I) / n), cash(cur, I / (12 * n))], f'Interest {money(cur, I, 0)}; total {money(cur, P + I, 0)} ÷ {12 * n} months.')


@R.add('ch02-st4', 'C3', (1, 4), 'short')
def flat_loan(rng, slot):
    city, country, cur, cname = place(rng)
    item = rng.choice(['a motorbike', 'a laptop', 'a sofa', 'solar panels', 'a used car', 'a piano'])
    P = rng.choice([1500, 2400, 3600, 5000, 7200, 9000])
    dep = rng.choice([0, 10, 20])
    r = rng.choice([6, 7.5, 8, 9, 11, 12])
    n = rng.choice([2, 3, 4])
    D = P * dep / 100
    L = P - D
    I = L * r / 100 * n
    pay = (L + I) / (12 * n)
    total = D + L + I
    return short(f'{name(rng)} buys {item} in {city} priced {money(cur, P, 0)}. {"They pay a " + str(dep) + "% deposit and borrow the rest" if dep else "They borrow the full price"} at {g(r)}% flat-rate interest per year for {n} years. Find the monthly repayment and the total cost.',
                 f'monthly {cash(cur, pay)}; total {cash(cur, total)}',
                 f'Borrowed {cash(cur, L)} (A1); interest {cash(cur, L)} × {g(r / 100)} × {n} = {cash(cur, I)} (M1 A1); ÷ {12 * n} months = {cash(cur, pay)} (A1); total {cash(cur, total)} (A1).', 5)


@R.add('ch02-st4', 'C3', (2, 5), 'short')
def savings_plan(rng, slot):
    city, country, cur, cname = place(rng)
    D = rng.choice([500, 1000, 1200, 1500, 2000, 2500])
    r = rng.choice([2, 3, 3.5, 4, 5])
    n = rng.randint(4, 12)
    i = r / 100
    FV = D * ((1 + i) ** n - 1) / i
    return short(f'{name(rng)} in {city} deposits {money(cur, D, 0)} at the end of every year into an account paying {g(r)}% compound interest per year. Find the total in the account just after the {ordinal(n)} deposit, and the interest earned.',
                 f'{cash(cur, FV)}; interest {cash(cur, FV - D * n)}',
                 f'Geometric series {D}(1 + {g(1 + i, 4)} + … + {g(1 + i, 4)}{sup(n - 1)}) (M1); = {D}({g(1 + i, 4)}{sup(n)} − 1)/{g(i, 4)} (A1) = {cash(cur, FV)} (A1); interest {cash(cur, FV - D * n)} (A1).', 4)


@R.add('ch02-st4', 'C2', (2, 4), 'explain')
def loan_explain(rng, slot):
    city, country, cur, cname = place(rng)
    who = name(rng)
    P = rng.choice([3000, 4000, 6000])
    r = rng.choice([6, 8, 10])
    n1, n2 = 2, rng.choice([4, 5])
    m1, m2 = (P + P * r * n1 / 100) / (12 * n1), (P + P * r * n2 / 100) / (12 * n2)
    if rng.random() < 0.5:
        return explain(f'{who} in {city} can borrow {money(cur, P, 0)} at {r}% flat rate over {n1} years or {n2} years. {who} prefers {n2} years "because it is cheaper". Explain whether this is right.',
                       f'{n1} years: {cash(cur, m1)}/month, total {cash(cur, m1 * 12 * n1)}; {n2} years: {cash(cur, m2)}/month, total {cash(cur, m2 * 12 * n2)}. The monthly payment is lower but the total cost is higher.',
                       'Both options compared (A1); conclusion about monthly vs total cost (R1).', 2)
    a = rng.randint(18, 25)
    b = a + 10
    return explain(f'Explain why someone who saves {money(cur, 100, 0)} a month from age {a} usually ends up with far more at age 60 than someone who saves {money(cur, 200, 0)} a month from age {b}.',
                   f'The early saver’s money has {10} more years of compound growth; growth multiplies, so the extra years outweigh the larger later deposits (at typical rates).',
                   'Compound growth over time (R1); comparison (R1).', 2)


@R.add('ch02-st4', 'C4', (3, 5), 'multi_step')
def finance_task(rng, slot):
    city, country, cur, cname = place(rng)
    kind = rng.choice(['phone', 'goal', 'lease', 'credit'])
    if kind == 'phone':
        price = rng.choice([900, 1100, 1300, 1500])
        mth = rng.choice([45, 50, 55, 60, 65])
        n = rng.choice([24, 30, 36])
        dep = rng.choice([0, 50, 100])
        tot = dep + mth * n
        extra = tot - price
        flat = extra / price / (n / 12) * 100
        ans = f'(a) {money(cur, tot, 0)} (b) {money(cur, extra, 0)} (c) about {rsf(flat, 3)}% per year (flat rate) (d) saving {money(cur, mth, 0)} a month would buy it after {math.ceil(price / mth)} months, avoiding interest'
        q_ = (f'A phone costs {money(cur, price, 0)} in {city}. A plan offers it for {money(cur, dep, 0)} down and {money(cur, mth, 0)} per month for {n} months. (a) Find the total paid on the plan. (b) Find the extra cost compared with paying cash. '
              f'(c) Find the equivalent flat interest rate per year. (d) Suggest an alternative and how long it would take.')
    elif kind == 'goal':
        goal = rng.choice([5000, 8000, 10000, 12000])
        r = rng.choice([3, 4, 5])
        D = rng.choice([1000, 1500, 2000])
        i = r / 100
        n = next(k for k in range(1, 100) if D * ((1 + i) ** k - 1) / i >= goal)
        ans = f'(a) {cash(cur, D * ((1 + i) ** 3 - 1) / i)} (b) after {n} deposits (years) (c) {cash(cur, D * ((1 + i) ** n - 1) / i)}, of which {cash(cur, D * ((1 + i) ** n - 1) / i - D * n)} is interest (d) without interest it takes {math.ceil(goal / D)} years'
        q_ = (f'{name(rng)} in {city} wants {money(cur, goal, 0)} for university and deposits {money(cur, D, 0)} at the end of each year into an account paying {r}% compound interest. (a) Find the balance after 3 deposits. '
              f'(b) After how many deposits is the goal first reached? (c) Find the balance then and the interest earned. (d) Compare with saving in a jar with no interest.')
    elif kind == 'lease':
        price = rng.choice([18000, 24000, 30000])
        lease = rng.choice([280, 320, 360, 400])
        dep_r = rng.choice([12, 15, 18])
        yrs = 3
        val = price * (1 - dep_r / 100) ** yrs
        buy_cost = price - val
        lease_cost = lease * 12 * yrs
        better = 'buying' if buy_cost < lease_cost else 'leasing'
        ans = f'(a) {cash(cur, val)} (b) {cash(cur, buy_cost)} (c) {money(cur, lease_cost, 0)} (d) {better} is cheaper by {cash(cur, abs(buy_cost - lease_cost))}; other factors: insurance, maintenance, cash available'
        q_ = (f'A company in {city} needs a van for 3 years. Option 1: buy it for {money(cur, price, 0)} and sell it after 3 years; it depreciates by {dep_r}% per year. Option 2: lease it for {money(cur, lease, 0)} per month. '
              f'(a) Find the van’s value after 3 years. (b) Find the cost of buying (price minus resale value). (c) Find the total lease cost. (d) Recommend an option and give one other factor to consider.')
    else:
        B = rng.choice([1200, 1500, 2000, 2500])
        r = rng.choice([1.5, 1.8, 2, 2.2])
        pay = rng.choice([100, 150, 200])
        bal = B
        months = 0
        interest = 0.0
        while bal > 0 and months < 200:
            it = bal * r / 100
            interest += it
            bal = bal + it - pay
            months += 1
        ans = f'(a) {cash(cur, B * r / 100)} (b) {cash(cur, B * (1 + r / 100) - pay)} (c) {months} months; total interest about {cash(cur, interest)} (d) the effective annual rate is {rsf(((1 + r / 100) ** 12 - 1) * 100, 3)}%, much more than 12 × {g(r)}% suggests'
        q_ = (f'A credit card in {city} has a balance of {money(cur, B, 0)} and charges {g(r)}% interest per month on the balance. {name(rng)} pays {money(cur, pay, 0)} at the end of each month after interest is added. '
              f'(a) Find the interest in the first month. (b) Find the balance after the first payment. (c) Use a spreadsheet-style table to find how many months it takes to clear the debt and the total interest. (d) Find the effective annual interest rate and comment.')
    return short(q_, ans, f'{ans}. Correct financial model (M1); calculations accurate to the cent (A1 A1); options compared in context (D: R1); recommendation communicated clearly (C1).', 6, 'multi_step', 'G5')


# =============================================================================================
# ch03 Quadratic Functions and Equations
# =============================================================================================
R.facts('ch03-st1', F(
    terms=[('standard form', 'the form y = ax² + bx + c; c is the y-intercept'),
           ('factorised form', 'the form y = a(x − p)(x − q); p and q are the x-intercepts (roots)'),
           ('vertex form', 'the form y = a(x − h)² + k; the vertex (turning point) is (h, k)'),
           ('axis of symmetry', 'the vertical line x = h through the vertex of a parabola; also x = −b/(2a)')],
    facts=[('What is the vertex of y = 2(x − 3)² + 5?', '(3, 5)', ['(−3, 5)', '(3, −5)', '(2, 5)'], 'Vertex form a(x − h)² + k has vertex (h, k).'),
           ('The parabola y = −(x + 1)(x − 7) has its axis of symmetry at:', 'x = 3', ['x = −3', 'x = 4', 'x = 7'], 'Halfway between the roots −1 and 7.'),
           ('If a < 0 in y = ax² + bx + c, the parabola:', 'opens downwards and has a maximum', ['opens upwards and has a minimum', 'has no vertex', 'is a straight line'], 'A negative leading coefficient flips the parabola.')],
    why=[('Explain why the axis of symmetry of y = a(x − p)(x − q) is x = (p + q)/2.', 'A parabola is symmetric about its axis, and the two roots are mirror images, so the axis lies exactly halfway between them.'),
         ('Explain why vertex form is useful for finding the maximum or minimum value.', '(x − h)² ≥ 0, so a(x − h)² + k is smallest (a > 0) or largest (a < 0) when x = h, giving the value k directly.'),
         ('Explain what the value of c tells you in y = ax² + bx + c.', 'Setting x = 0 gives y = c, so c is the y-intercept.')],
    misc=[('The vertex of y = (x + 4)² − 2 is (4, −2).', 'x + 4 = x − (−4), so h = −4: the vertex is (−4, −2).'),
          ('Every quadratic can be written in factorised form with real numbers.', 'Only if it has real roots; e.g. x² + 1 has no real roots.')],
    contrast=[('vertex form', 'factorised form', 'Vertex form a(x − h)² + k shows the turning point; factorised form a(x − p)(x − q) shows the x-intercepts.')],
))


def _q_from_vertex(a, h, k):
    return sp.expand(a * (x - h) ** 2 + k)


@R.add('ch03-st1', 'C1', (1, 3), 'mcq')
def vertex_mcq(rng, slot):
    a = rng.choice([1, 2, 3, -1, -2])
    h, k = rng.randint(-6, 6), rng.randint(-9, 9)
    form = f'{coef(a)}(x{sgn(-h) if h else ""})²{sgn(k) if k else ""}'
    return mcq(rng, f'State the vertex of y = {form}.', ptxt((h, k)), [ptxt((-h, k)), ptxt((h, -k)), ptxt((-h, -k)) if h and k else ptxt((k, h))],
               f'y = a(x − h)² + k has vertex (h, k) = {ptxt((h, k))}.')


@R.add('ch03-st1', 'C3', (1, 4), 'short')
def complete_square(rng, slot):
    a = rng.choice([1, 1, 2, 3, -1, -2]) if slot.d >= 3 else 1
    h, k = rng.randint(-7, 7), rng.randint(-12, 12)
    if h == 0:
        h = 2
    e = _q_from_vertex(a, h, k)
    form = f'{coef(a)}(x{sgn(-h)})²{sgn(k) if k else ""}'
    return short(f'Write y = {sx(e)} in the form a(x − h)² + k, and state the vertex and the {"minimum" if a > 0 else "maximum"} value of y.', f'y = {form}; vertex {ptxt((h, k))}; {"minimum" if a > 0 else "maximum"} {m(k)}',
                 f'{"Factor out " + str(a) + ", then h" if a != 1 else "H"}alf the x-coefficient: h = {m(h)} (M1); y = {form} (A1); vertex {ptxt((h, k))} and {"min" if a > 0 else "max"} {m(k)} (A1).', 3)


@R.add('ch03-st1', 'C3', (2, 5), 'short')
def factorised_features(rng, slot):
    a = rng.choice([1, 2, -1, -2, 3])
    p, q = sorted(rng.sample(range(-8, 9), 2))
    h = Fr(p + q, 2)
    k = a * (h - p) * (h - q)
    e = sp.expand(a * (x - p) * (x - q))
    if rng.random() < 0.5:
        return short(f'For y = {coef(a)}(x{sgn(-p) if p else ""})(x{sgn(-q) if q else ""}), find the x-intercepts, the y-intercept, the axis of symmetry and the vertex.',
                     f'x-intercepts {m(p)} and {m(q)}; y-intercept {m(a * p * q)}; x = {fx(h)}; vertex ({fx(h)}, {fx(k)})',
                     f'Roots (A1); y-intercept a·p·q = {m(a * p * q)} (A1); axis halfway (M1 A1); vertex y-value by substitution (A1).', 5)
    return short(f'Factorise y = {sx(e)} and hence find where the graph crosses the x-axis and the coordinates of its vertex.',
                 f'y = {coef(a)}(x{sgn(-p) if p else ""})(x{sgn(-q) if q else ""}); crosses at x = {m(p)}, {m(q)}; vertex ({fx(h)}, {fx(k)})',
                 f'Correct factorisation (M1 A1); roots (A1); vertex at x = {fx(h)} (A1).', 4)


@R.add('ch03-st1', 'C3', (2, 5), 'short')
def quad_from_info(rng, slot):
    a = rng.choice([1, 2, 3, -1, -2, Fr(1, 2), Fr(-1, 2)])
    h, k = rng.randint(-5, 5), rng.randint(-8, 8)
    px = h + rng.choice([-3, -2, 2, 3, 4])
    py = a * (px - h) ** 2 + k
    if rng.random() < 0.5:
        return short(f'A parabola has vertex {ptxt((h, k))} and passes through {ptxt((px, fx(py)))}. Find its equation in vertex form.',
                     f'y = {coef(a)}(x{sgn(-h) if h else ""})²{sgn(k) if k else ""}',
                     f'y = a(x{sgn(-h) if h else ""})²{sgn(k) if k else ""} (M1); substitute {ptxt((px, fx(py)))}: {fx(py)} = a({px - h})²{sgn(k) if k else ""} (M1); a = {fx(a)} (A1).', 3)
    p, q = sorted(rng.sample(range(-6, 7), 2))
    yi = rng.choice([v for v in range(-12, 13) if v])
    if p * q == 0:
        return None
    aa = Fr(yi, p * q)
    e = sp.expand(sp.Rational(aa.numerator, aa.denominator) * (x - p) * (x - q))
    return short(f'A parabola crosses the x-axis at x = {m(p)} and x = {m(q)} and the y-axis at y = {m(yi)}. Find its equation in the form y = ax² + bx + c.', f'y = {sx(e)}',
                 f'y = a(x{sgn(-p)})(x{sgn(-q)}) (M1); a × {m(p * q)} = {m(yi)} → a = {fx(aa)} (A1); expanded (A1).', 3)


@R.add('ch03-st1', 'C2', (2, 4), 'explain')
def forms_explain(rng, slot):
    who = name(rng)
    h, k = rng.randint(1, 7), rng.randint(1, 9)
    kind = rng.choice(['sign', 'which', 'noroots'])
    if kind == 'sign':
        return explain(f'{who} says the vertex of y = (x + {h})² − {k} is ({h}, −{k}). Explain the error.',
                       f'Vertex form is (x − h)², and x + {h} = x − (−{h}), so h = −{h}: the vertex is (−{h}, −{k}).', 'Sign of h explained (R1); correct vertex (A1).', 2)
    if kind == 'which':
        return explain(f'A designer needs the highest point of an arch modelled by a quadratic. Explain which form of the quadratic is most useful and why.',
                       'Vertex form a(x − h)² + k, because the maximum point (h, k) can be read off directly.', 'Form chosen (A1); reason (R1).', 2)
    return explain(f'Explain why y = (x − {h})² + {k} does not cross the x-axis.',
                   f'(x − {h})² ≥ 0, so y ≥ {k} > 0 for every x: the minimum value is {k}, above the axis.', 'Square non-negative (R1); minimum above axis (R1).', 2)


@R.add('ch03-st1', 'C4', (3, 5), 'multi_step')
def quad_forms_task(rng, slot):
    city = rng.choice(CITIES)
    kind = rng.choice(['arch', 'family', 'cable', 'fountain'])
    if kind == 'arch':
        w = rng.choice([20, 24, 30, 36, 40])
        H = rng.choice([8, 9, 10, 12, 15])
        a = Fr(-H, (w // 2) ** 2)
        x1 = rng.randint(2, w // 2 - 1)
        h1 = a * (x1 - w // 2) ** 2 + H
        ans = f'(a) y = {coef(a)}x(x − {w}) (b) y = {coef(a)}(x − {w // 2})² + {H} (c) {rsf(float(h1), 3)} m (d) the arch is symmetric, so the height is the same {w - 2 * x1} m further along, at x = {w - x1}'
        q_ = (f'A bridge arch in {city} is a parabola that meets the ground at x = 0 and x = {w} m and has a maximum height of {H} m. (a) Write its equation in factorised form. (b) Write it in vertex form. '
              f'(c) Find the height {x1} m from one end. (d) Explain, using symmetry, where else the arch has the same height.')
    elif kind == 'family':
        k = rng.randint(2, 6)
        ans = f'(a) vertices (1, −{k}), (2, −{k}), (3, −{k}) (b) all vertices lie on the line y = −{k}; h moves the graph horizontally (c) y = x² − 2hx + h² − {k} (d) roots h ± √{k}, so the roots are always 2√{k} = {g(2 * math.sqrt(k), 3)} apart'
        q_ = (f'Investigate the family y = (x − h)² − {k}. (a) Find the vertex for h = 1, 2, 3. (b) Describe the pattern. (c) Expand the equation in terms of h. '
              f'(d) Find the roots in terms of h and show that the distance between them does not depend on h.')
    elif kind == 'cable':
        sp_ = rng.choice([100, 120, 150, 200])
        low, tower = rng.choice([5, 8, 10]), rng.choice([40, 50, 60])
        a = Fr(tower - low, (sp_ // 2) ** 2)
        ans = f'(a) y = {coef(a)}(x − {sp_ // 2})² + {low} (b) {rsf(float(a * (sp_ // 4 - sp_ // 2) ** 2 + low), 3)} m (c) x = {rsf(sp_ / 2 - math.sqrt(float((20 - low) / a)), 4)} m and x = {rsf(sp_ / 2 + math.sqrt(float((20 - low) / a)), 4)} m (d) y = {sx(sp.expand(sp.Rational(a.numerator, a.denominator) * (x - sp_ // 2) ** 2 + low))}'
        q_ = (f'The main cable of a suspension bridge in {city} hangs between towers {sp_} m apart, {tower} m above the road; its lowest point is {low} m above the road, midway. Taking x = 0 at the left tower, '
              f'(a) write the cable’s equation in vertex form. (b) Find its height a quarter of the way across. (c) Find where the cable is 20 m above the road. (d) Write the equation in standard form.')
    else:
        h, k = Fr(rng.choice([2, 3, 4, 5]), 2), rng.choice([3, 4, 5, 6])
        a = -rng.choice([1, 2, 3])
        root = h + Fr(1) * sp.sqrt(sp.Rational(k, -a))
        r_num = float(h) + math.sqrt(k / -a)
        ans = f'(a) y = {m(a)}(x − {fx(h)})² + {k} (b) {k} m at {fx(h)} m from the nozzle (c) {fx(a * h * h + k)} m (d) x = {fx(h)} + √({fx(Fr(k, -a))}) ≈ {rsf(r_num, 3)} m'
        q_ = (f'A water jet in a fountain in {city} follows y = {m(a)}(x − {fx(h)})² + {k}, where x m is the horizontal distance from the nozzle. (a) State the form of this equation. (b) Find the maximum height and where it occurs. '
              f'(c) Find the height of the nozzle (x = 0). (d) Find where the water hits the ground (y = 0).')
    return short(q_, ans, f'{ans}. Appropriate form chosen and features identified (A1 A1); algebra correct (M1 A1); conclusion justified or generalised (B/D: R1 C1).', 6, 'multi_step', 'G5')


R.facts('ch03-st2', F(
    terms=[('quadratic formula', 'the formula x = (−b ± √(b² − 4ac)) / (2a) gives the roots of ax² + bx + c = 0'),
           ('discriminant', 'Δ = b² − 4ac; it decides the number of real roots: Δ > 0 two, Δ = 0 one (repeated), Δ < 0 none'),
           ('quadratic inequality', 'an inequality such as ax² + bx + c > 0, solved by finding the roots and using the shape of the parabola')],
    facts=[('How many real roots has x² − 6x + 9 = 0?', 'one (repeated)', ['two', 'none', 'three'], 'Δ = 36 − 36 = 0.'),
           ('Solve x² − 5x + 6 = 0.', 'x = 2 or x = 3', ['x = −2 or x = −3', 'x = 1 or x = 6', 'x = 5 or x = 6'], '(x − 2)(x − 3) = 0.'),
           ('The solution of (x − 1)(x − 4) < 0 is:', '1 < x < 4', ['x < 1 or x > 4', 'x < 4', 'x > 1'], 'The parabola opens up and is below the axis between its roots.')],
    why=[('Explain why the sign of the discriminant tells you the number of real roots.', 'The formula contains √Δ: a positive Δ gives two different values (±), zero gives one, and a negative Δ has no real square root.'),
         ('Explain why you must not divide both sides of x² = 5x by x.', 'Dividing by x assumes x ≠ 0 and loses the solution x = 0; factorise x(x − 5) = 0 instead.'),
         ('Explain how a sketch helps to solve x² − x − 6 ≥ 0.', 'The parabola opens upwards with roots −2 and 3; it is on or above the axis outside the roots, so x ≤ −2 or x ≥ 3.')],
    misc=[('If (x − 3)(x + 2) = 6, then x − 3 = 6 or x + 2 = 6.', 'The zero-product rule only works when the product is 0; expand and rearrange first.'),
          ('x² > 9 means x > 3.', 'Also x < −3, since (−4)² = 16 > 9.')],
))


@R.add('ch03-st2', 'C1', (1, 3), 'mcq')
def discriminant_mcq(rng, slot):
    a, b, c = rng.choice([1, 2, 3, -1]), rng.randint(-9, 9), rng.randint(-9, 9)
    D = b * b - 4 * a * c
    corr = 'two distinct real roots' if D > 0 else 'one repeated real root' if D == 0 else 'no real roots'
    opts = ['two distinct real roots', 'one repeated real root', 'no real roots', 'infinitely many roots']
    return mcq(rng, f'How many real roots has {sx(a * x ** 2 + b * x + c)} = 0?', corr, [o for o in opts if o != corr],
               f'Δ = ({m(b)})² − 4({m(a)})({m(c)}) = {m(D)}.')


@R.add('ch03-st2', 'C3', (1, 4), 'short')
def quad_formula(rng, slot):
    a, b, c = rng.choice([1, 2, 3, -2]), rng.randint(-9, 9), rng.randint(-9, 9)
    D = b * b - 4 * a * c
    if D <= 0 or math.isqrt(D) ** 2 == D:
        return None
    k, r = surd_parts(D)
    r1, r2_ = (-b + math.sqrt(D)) / (2 * a), (-b - math.sqrt(D)) / (2 * a)
    if slot.d >= 3:
        return short(f'Solve {sx(a * x ** 2 + b * x + c)} = 0, giving exact answers in simplest surd form.', f'x = ({m(-b)} ± {sq(k, r)})/{2 * a}',
                     f'Δ = {D} (A1); x = ({m(-b)} ± √{D})/{2 * a} (M1); √{D} = {sq(k, r)} (A1).', 3)
    return short(f'Solve {sx(a * x ** 2 + b * x + c)} = 0, giving your answers to 2 decimal places.', f'x = {r2(max(r1, r2_))} or x = {r2(min(r1, r2_))}',
                 f'Δ = {D} (A1); formula substituted (M1); {r2(max(r1, r2_))}, {r2(min(r1, r2_))} (A1).', 3)


@R.add('ch03-st2', 'C3', (2, 5), 'short')
def quad_inequality(rng, slot):
    a = rng.choice([1, 1, 2, -1])
    p, q = sorted(rng.sample(range(-8, 9), 2))
    e = sp.expand(a * (x - p) * (x - q))
    op = rng.choice(['<', '≤', '>', '≥'])
    inside = (op in '<≤') == (a > 0)
    strict = op in '<>'
    if inside:
        ans = f'{m(p)} {"<" if strict else "≤"} x {"<" if strict else "≤"} {m(q)}'
    else:
        ans = f'x {"<" if strict else "≤"} {m(p)} or x {">" if strict else "≥"} {m(q)}'
    return short(f'Solve {sx(e)} {op} 0.', ans,
                 f'Roots x = {m(p)}, {m(q)} (M1 A1); parabola opens {"up" if a > 0 else "down"}, so the required region is {"between" if inside else "outside"} the roots: {ans} (A1).', 3)


@R.add('ch03-st2', 'C2', (2, 4), 'explain')
def solve_explain(rng, slot):
    who = name(rng)
    k = rng.randint(2, 9)
    kind = rng.choice(['divide', 'square', 'prod', 'k'])
    if kind == 'divide':
        return explain(f'{who} solves x² = {k}x by dividing by x and gets x = {k}. Explain what is wrong and give the full solution.',
                       f'Dividing by x loses the root x = 0. x² − {k}x = 0 → x(x − {k}) = 0 → x = 0 or x = {k}.', 'Lost root explained (R1); both roots (A1).', 2)
    if kind == 'square':
        return explain(f'{who} says the solution of x² > {k * k} is x > {k}. Explain why this is incomplete.',
                       f'Negative numbers also have squares greater than {k * k}, e.g. (−{k + 1})² = {(k + 1) ** 2}; the solution is x < −{k} or x > {k}.', 'Counter-example (R1); full solution (A1).', 2)
    if kind == 'prod':
        p = rng.randint(1, 5)
        return explain(f'{who} solves (x − {p})(x + 1) = {k} by writing x − {p} = {k} or x + 1 = {k}. Explain the mistake.',
                       'The zero-product property only applies when the product is 0. Expand and rearrange to x² ' + m(f'{1 - p:+d}').replace('+', '+ ').replace('−', '− ') + f'x − {p + k} = 0 first.',
                       'Zero-product condition (R1); correct method (A1).', 2)
    c = k * k
    return explain(f'Explain how to find the values of m for which x² + mx + {c} = 0 has two equal roots.',
                   f'Equal roots need Δ = 0: m² − 4 × {c} = 0, so m² = {4 * c} and m = ±{2 * k}.', 'Δ = 0 condition (R1); values (A1).', 2)


@R.add('ch03-st2', 'C4', (3, 5), 'multi_step')
def solve_task(rng, slot):
    city, country, cur, cname = place(rng)
    kind = rng.choice(['garden', 'profit', 'path', 'kvalue'])
    if kind == 'garden':
        w = rng.randint(4, 12)
        d = rng.randint(2, 6)
        A = w * (w + d)
        ans = f'(a) x(x + {d}) = {A} (b) x² + {d}x − {A} = 0 → (x − {w})(x + {w + d}) = 0 (c) x = {w}: {w} m by {w + d} m (reject x = −{w + d}) (d) perimeter {2 * (2 * w + d)} m'
        q_ = (f'A rectangular vegetable plot in {city} is {d} m longer than it is wide and has an area of {A} m². Let the width be x m. (a) Write an equation for the area. (b) Rearrange and solve it. '
              f'(c) State the dimensions and explain why one solution is rejected. (d) Find the length of fencing needed to go round it.')
    elif kind == 'profit':
        p, q = sorted(rng.sample(range(2, 30), 2))
        a = rng.choice([1, 2, 5, 10])
        e = sp.expand(-a * (x - p) * (x - q))
        h = Fr(p + q, 2)
        ans = f'(a) P = {sx(e)} (b) P = 0 at x = {p} and {q} (c) profit when {p} < x < {q} (d) maximum at x = {fx(h)}: {money(cur, float(-a * (h - p) * (h - q)) * 100, 0)}'
        q_ = (f'A café in {city} models its daily profit P (in hundreds of {cname}) from selling x litres of smoothie as P = −{a if a > 1 else ""}(x − {p})(x − {q}). (a) Expand the model. '
              f'(b) Find the break-even points. (c) Solve P > 0 and interpret it. (d) Find the maximum profit and the number of litres that gives it.')
    elif kind == 'path':
        L, W = rng.choice([(20, 12), (24, 16), (30, 20), (18, 10), (16, 12)])
        A_path = rng.choice([L * W // 2, L * W // 3, L * W // 4])
        # (L + 2x)(W + 2x) − LW = A → 4x² + 2(L+W)x − A = 0
        disc = 4 * (L + W) ** 2 + 16 * A_path
        xw = (-2 * (L + W) + math.sqrt(disc)) / 8
        ans = f'(a) (L + 2x)(W + 2x) − {L * W} = {A_path} (b) 4x² + {2 * (L + W)}x − {A_path} = 0 (c) x ≈ {rsf(xw, 3)} m (d) the negative root is meaningless for a width'
        q_ = (f'A park in {city} has a {L} m by {W} m lawn. A path of constant width x m is built around it with an area of {A_path} m². (a) Write an equation in x. (b) Write it in the form ax² + bx + c = 0. '
              f'(c) Solve it to find the width of the path to 3 s.f. (d) Explain why one solution is rejected.')
    else:
        c = rng.choice([4, 9, 16, 25, 36])
        k = math.isqrt(c)
        ans = f'(a) Δ = m² − {4 * c} (b) m = ±{2 * k} (c) m < −{2 * k} or m > {2 * k} (d) −{2 * k} < m < {2 * k}'
        q_ = (f'Investigate the equation x² + mx + {c} = 0 for different values of m. (a) Write the discriminant in terms of m. (b) Find m when the equation has equal roots. '
              f'(c) Find the values of m for two distinct real roots. (d) Find the values of m for which there are no real roots.')
    return short(q_, ans, f'{ans}. Equation or condition formed (M1 A1); solved correctly (A1 A1); solutions interpreted and checked in context (D/B: R1 C1).', 6, 'multi_step', 'G5')


R.facts('ch03-st3', F(
    terms=[('simultaneous equations (linear–quadratic)', 'a pair of equations, one linear and one quadratic, solved by substitution to find their intersection points'),
           ('tangent line', 'a line that touches a curve at exactly one point; for a line and a parabola the resulting quadratic has Δ = 0'),
           ('substitution', 'replacing a variable in one equation using the expression for it from another equation')],
    facts=[('A line and a parabola can intersect in at most how many points?', '2', ['1', '3', '4'], 'Substitution gives a quadratic, which has at most two roots.'),
           ('Substituting y = x + 1 into y = x² − 1 gives:', 'x² − x − 2 = 0', ['x² + x = 0', 'x² − x = 0', 'x² + x − 2 = 0'], 'x + 1 = x² − 1.'),
           ('If the substituted quadratic has Δ < 0, the line:', 'misses the parabola', ['is a tangent', 'cuts it twice', 'is the axis of symmetry'], 'No real roots means no intersection.')],
    why=[('Explain why solving a linear and a quadratic equation simultaneously gives at most two solutions.', 'Substituting the line into the quadratic gives one quadratic equation in x, which has at most two real roots.'),
         ('Explain how the discriminant shows whether a line is a tangent to a parabola.', 'After substitution, Δ = 0 gives exactly one repeated root, so the line meets the curve at one point only.'),
         ('Explain why you must find both coordinates of each intersection point.', 'A point needs an x- and a y-value; substitute each x back into the linear equation to get y.')],
    misc=[('Once you have found the x-values, you are finished.', 'Each x must be substituted back to find the matching y-value.'),
          ('If the quadratic has one root, the line crosses the parabola once.', 'It touches it (tangent) rather than crossing.')],
))


@R.add('ch03-st3', 'C1', (1, 3), 'mcq')
def intersect_mcq(rng, slot):
    b, c = rng.randint(-6, 6), rng.randint(-6, 6)
    mm, n = rng.randint(-4, 4), rng.randint(-8, 8)
    A, B, C = 1, b - mm, c - n
    D = B * B - 4 * A * C
    corr = '2' if D > 0 else '1' if D == 0 else '0'
    return mcq(rng, f'How many points of intersection do y = {sx(x ** 2 + b * x + c)} and y = {lin(mm, n)} have?', corr, [o for o in ['0', '1', '2', '3'] if o != corr],
               f'{sx(x ** 2 + B * x + C)} = 0 has Δ = {m(D)}.')


@R.add('ch03-st3', 'C3', (1, 4), 'short')
def intersect_solve(rng, slot):
    a = rng.choice([1, 1, 2, -1])
    r1, r2_ = sorted(rng.sample(range(-6, 7), 2))
    mm, n = rng.randint(-5, 5), rng.randint(-8, 8)
    # a(x − r1)(x − r2) = (quad − line) → quad = line + a(x−r1)(x−r2)
    quad = sp.expand(mm * x + n + a * (x - r1) * (x - r2_))
    p1, p2 = (r1, mm * r1 + n), (r2_, mm * r2_ + n)
    return short(f'Find the coordinates of the points where the line y = {lin(mm, n)} meets the curve y = {sx(quad)}.', f'{ptxt(p1)} and {ptxt(p2)}',
                 f'{sx(quad)} = {lin(mm, n)} → {sx(sp.expand(a * (x - r1) * (x - r2_)))} = 0 (M1); x = {m(r1)}, {m(r2_)} (A1); y-values from the line (A1).', 3)


@R.add('ch03-st3', 'C3', (2, 5), 'short')
def tangent_k(rng, slot):
    a = rng.choice([1, 2, 3])
    mm = rng.choice([v for v in range(-8, 9) if v])
    b = rng.randint(-4, 4)
    # a x² + b x + k − (m x) → a x² + (b − m)x + k... we want y = mx + c tangent to y = ax² + bx: ax² + (b − m)x − c = 0, Δ = (b − m)² + 4ac = 0
    cval = Fr(-(b - mm) ** 2, 4 * a)
    xt = Fr(mm - b, 2 * a)
    yt = mm * xt + cval
    return short(f'The line y = {lin(mm, 0)} + c is a tangent to the curve y = {sx(a * x ** 2 + b * x)}. Find c and the point of contact.', f'c = {fx(cval)}; point ({fx(xt)}, {fx(yt)})',
                 f'{sx(a * x ** 2 + (b - mm) * x)} − c = 0 (M1); Δ = {m((b - mm) ** 2)} + {4 * a}c = 0 (M1); c = {fx(cval)} (A1); x = {fx(xt)}, y = {fx(yt)} (A1).', 4)


@R.add('ch03-st3', 'C2', (2, 4), 'explain')
def intersect_explain(rng, slot):
    who = name(rng)
    k = rng.randint(1, 9)
    kind = rng.choice(['miss', 'yvals', 'count'])
    if kind == 'miss':
        return explain(f'Explain, using the discriminant, why the line y = −{k} never meets the parabola y = x² + 1.',
                       f'x² + 1 = −{k} → x² + {k + 1} = 0, Δ = −{4 * (k + 1)} < 0, so there are no real solutions.', 'Equation formed (M1); Δ < 0 interpreted (R1).', 2)
    if kind == 'yvals':
        return explain(f'{who} solves y = x + {k} and y = x² + {k} and writes "x = 0 or x = 1". Explain what is missing and complete the answer.',
                       f'The y-coordinates are needed: (0, {k}) and (1, {k + 1}).', 'Missing y identified (R1); points (A1).', 2)
    return explain(f'Explain how to find the values of c for which the line y = 2x + c meets y = x² in two points.',
                   'x² − 2x − c = 0 must have Δ > 0: 4 + 4c > 0, so c > −1.', 'Δ > 0 condition (R1); c > −1 (A1).', 2)


@R.add('ch03-st3', 'C4', (3, 5), 'multi_step')
def intersect_task(rng, slot):
    city = rng.choice(CITIES)
    kind = rng.choice(['ramp', 'laser', 'family', 'road'])
    if kind == 'ramp':
        a = Fr(-1, rng.choice([5, 10, 20]))
        u = rng.choice([1, 2])
        mm = Fr(1, rng.choice([2, 4, 5]))
        # ball: y = a x² + u x ; ramp: y = m x → a x² + (u − m)x = 0 → x = (m − u)/a
        xh = (mm - u) / a
        ans = f'(a) {coef(a)}x² + {coef(u - mm)}x = 0 (b) x = 0 or x = {fx(xh)} (c) ({fx(xh)}, {fx(mm * xh)}) (d) the vertex of the ball’s path is at x = {fx(Fr(-u, 2) / a)}, so it {"has passed its highest point (falling)" if Fr(-u, 2) / a < xh else "lands exactly at its highest point" if Fr(-u, 2) / a == xh else "is still rising"} when it lands'
        q_ = (f'A skateboarder in {city} launches a ball from the bottom of a straight ramp. The ball follows y = {coef(a)}x² + {coef(u)}x and the ramp is y = {coef(mm)}x (metres). (a) Form an equation for where they meet. '
              f'(b) Solve it. (c) Find where the ball lands on the ramp. (d) Decide whether the ball is rising or falling when it lands, with a reason.')
    elif kind == 'laser':
        k = rng.randint(1, 6)
        mm = rng.randint(1, 5)
        c_t = Fr(-mm * mm, 4)
        ans = f'(a) x² − {mm}x − c + {k} = 0 → wait, simplified: x² − {mm}x + ({k} − c) = 0 (b) Δ = {mm * mm} − 4({k} − c) (c) c = {fx(k + c_t)} (tangent) (d) c > {fx(k + c_t)} two points; c < {fx(k + c_t)} misses'
        ans = f'(a) x² − {mm}x + ({k} − c) = 0 (b) Δ = {mm * mm} − 4({k} − c) (c) c = {fx(k + c_t)} (tangent) (d) c > {fx(k + c_t)}: two points; c < {fx(k + c_t)}: no intersection'
        q_ = (f'In a light show in {city}, a laser beam follows y = {mm}x + c and a curved screen is y = x² + {k}. (a) Show that the beam meets the screen when x² − {mm}x + ({k} − c) = 0. (b) Find the discriminant. '
              f'(c) Find c when the beam just touches the screen. (d) Describe how many points are lit for other values of c.')
    elif kind == 'family':
        c = rng.randint(1, 5)
        ans = f'(a) m = 0: x² + {c} = 0 no solutions; m = ±{2 * math.isqrt(4 * c) // 2 if math.isqrt(4 * c) ** 2 == 4 * c else "2√" + str(c)}: tangent (b) x² − mx + {c} = 0, Δ = m² − {4 * c} (c) |m| > {g(2 * math.sqrt(c), 3)}: two points; |m| = {g(2 * math.sqrt(c), 3)}: tangent; |m| < {g(2 * math.sqrt(c), 3)}: none (d) the tangents are y = ±{sq(2, c)}x'
        q_ = (f'Investigate the lines y = mx through the origin and the parabola y = x² + {c}. (a) Try m = 0 and one other value. (b) Write the quadratic for the intersections and its discriminant. '
              f'(c) Classify the number of intersections for all m. (d) Write the equations of the two tangent lines.')
    else:
        k = rng.randint(2, 6)
        r1, r2_ = sorted(rng.sample(range(1, 12), 2))
        mm = rng.choice([1, 2, -1])
        n = rng.randint(0, 10)
        quad = sp.expand(mm * x + n - (x - r1) * (x - r2_))
        ans = f'(a) {sx(quad)} = {lin(mm, n)} (b) x = {r1}, {r2_} (c) {ptxt((r1, mm * r1 + n))} and {ptxt((r2_, mm * r2_ + n))} (d) distance = √({(r2_ - r1) ** 2} + {(mm * (r2_ - r1)) ** 2}) ≈ {rsf(math.hypot(r2_ - r1, mm * (r2_ - r1)), 3)} km'
        q_ = (f'On a map of {city} (units km) a hill path follows y = {sx(quad)} and a straight road follows y = {lin(mm, n)}. (a) Write an equation for where they cross. (b) Solve it. '
              f'(c) Find the coordinates of the crossings. (d) Find the straight-line distance between the crossings.')
    return short(q_, ans, f'{ans}. Substitution and quadratic formed (M1 A1); solved (A1); discriminant / points interpreted (B/D: R1 R1); communication (C1).', 6, 'multi_step', 'G5')


R.facts('ch03-st4', F(
    terms=[('optimisation', 'finding the maximum or minimum value of a quantity, e.g. using the vertex of a quadratic model'),
           ('projectile model', 'a quadratic model h(t) = −½gt² + ut + h₀ for the height of an object moving under gravity'),
           ('domain of a model', 'the values of the input for which the model makes sense in context, e.g. times between launch and landing')],
    facts=[('The maximum value of h = −5(t − 2)² + 30 is:', '30', ['2', '−5', '35'], 'The vertex is (2, 30).'),
           ('A rectangle has perimeter 40 m. Its greatest possible area is:', '100 m²', ['400 m²', '40 m²', '80 m²'], 'A 10 m × 10 m square.'),
           ('For h(t) = −4.9t² + 14.7t, the ball is at its highest when t is:', '1.5 s', ['3 s', '14.7 s', '0 s'], 't = −b/(2a) = 14.7/9.8.')],
    why=[('Explain why the vertex of a quadratic model gives its maximum or minimum.', 'The parabola is symmetric and turns at the vertex; with a < 0 every other point is lower, so the vertex is the maximum.'),
         ('Explain why a projectile model is only valid between launch and landing.', 'Before launch and after landing the object is not in flight, so the formula (e.g. negative heights) no longer describes it.'),
         ('Explain why, for a fixed perimeter, a square gives the largest rectangular area.', 'A = x(P/2 − x) is a downward parabola with vertex at x = P/4, which makes both sides equal.')],
    misc=[('The ball is highest at the time it lands.', 'It lands when h = 0; it is highest at the vertex, halfway between the roots for h₀ = 0.'),
          ('To maximise revenue, always charge the highest possible price.', 'Higher prices reduce sales; revenue p × q is largest at the vertex of the quadratic.')],
))


@R.add('ch03-st4', 'C1', (1, 3), 'mcq')
def maxval_mcq(rng, slot):
    a = rng.choice([1, 2, 3, 5])
    h, k = rng.randint(1, 8), rng.randint(5, 60)
    return mcq(rng, f'What is the maximum value of y = −{a if a > 1 else ""}(x − {h})² + {k}?', str(k), [str(h), str(k + a), m(-a)],
               f'(x − {h})² ≥ 0, so y ≤ {k}; the maximum is {k} at x = {h}.')


@R.add('ch03-st4', 'C3', (1, 4), 'short')
def projectile_calc(rng, slot):
    city = rng.choice(CITIES)
    obj = rng.choice(['ball', 'stone', 'rocket', 'javelin', 'water balloon'])
    u = rng.choice([9.8, 12, 14.7, 15, 19.6, 20, 24.5, 25])
    h0 = rng.choice([0, 1, 1.5, 2, 5, 10])
    tmax = u / 9.8
    hmax = h0 + u * u / (2 * 9.8)
    tl = (u + math.sqrt(u * u + 4 * 4.9 * h0)) / 9.8
    ht = f'h = −4.9t² + {g(u)}t{" + " + g(h0) if h0 else ""}'
    if slot.d <= 2:
        return short(f'The height of a {obj} in {city} is {ht} metres after t seconds. Find the maximum height and when it occurs.', f'{rsf(hmax, 3)} m at t = {rsf(tmax, 3)} s',
                     f't = −b/(2a) = {g(u)}/9.8 (M1) = {rsf(tmax, 3)} s (A1); h = {rsf(hmax, 3)} m (A1).', 3)
    return short(f'The height of a {obj} in {city} is {ht} metres after t seconds. Find the maximum height and the time at which it hits the ground.', f'max {rsf(hmax, 3)} m; lands at t = {rsf(tl, 3)} s',
                 f'Vertex t = {rsf(tmax, 3)} (M1), h = {rsf(hmax, 3)} m (A1); h = 0 solved with the formula, positive root (M1) t = {rsf(tl, 3)} s (A1).', 4)


@R.add('ch03-st4', 'C3', (2, 5), 'short')
def optimise_area(rng, slot):
    city, country, cur, cname = place(rng)
    kind = rng.choice(['wall', 'free', 'revenue'])
    if kind == 'wall':
        L = rng.choice([40, 48, 60, 80, 100, 120])
        return short(f'A farmer in {country} has {L} m of fencing to make a rectangular pen against a long wall (the wall forms one side). Find the dimensions that maximise the area and the maximum area.',
                     f'{g(L / 4)} m by {g(L / 2)} m; {g(L * L / 8)} m²', f'A = x({L} − 2x) (M1 A1); vertex x = {g(L / 4)} (M1); area {g(L * L / 8)} m² (A1).', 4)
    if kind == 'free':
        P = rng.choice([24, 36, 50, 64, 90])
        return short(f'A rectangular garden in {city} has perimeter {P} m. Write the area in terms of the width x and find the maximum area.', f'A = x({g(P / 2)} − x); max {g(P * P / 16)} m² when x = {g(P / 4)} m',
                     f'Length = {g(P / 2)} − x (A1); A = x({g(P / 2)} − x) (M1); vertex x = {g(P / 4)} (A1); {g(P * P / 16)} m² (A1).', 4)
    a = rng.choice([200, 300, 400, 500, 600])
    b = rng.choice([5, 10, 20, 25])
    p = Fr(a, 2 * b)
    return short(f'A museum in {city} sells q = {a} − {b}p tickets a day at price p {cname}. Find the price that maximises daily revenue and the maximum revenue.',
                 f'p = {cash(cur, p)}; revenue {cash(cur, p * (a - b * p))}', f'R = p({a} − {b}p) (M1); vertex p = {a}/{2 * b} (M1) = {g(float(p), 4)} (A1); R = {cash(cur, p * (a - b * p))} (A1).', 4)


@R.add('ch03-st4', 'C2', (2, 4), 'explain')
def optimise_explain(rng, slot):
    who = name(rng)
    u = rng.choice([10, 15, 20, 25])
    kind = rng.choice(['domain', 'land', 'price'])
    if kind == 'domain':
        tl = u / 5
        return explain(f'A ball’s height is h = {u}t − 5t². Explain why the model only makes sense for 0 ≤ t ≤ {g(tl)}.',
                       f'h = 0 at t = 0 (launch) and t = {g(tl)} (landing); outside this interval the model gives negative heights, but the ball is on the ground.',
                       'Roots found (A1); domain justified (R1).', 2)
    if kind == 'land':
        return explain(f'{who} says that for h = {u}t − 5t² the ball is highest at t = {g(u / 5)}. Explain the mistake and correct it.',
                       f't = {g(u / 5)} is when it lands (h = 0). The highest point is midway between the roots: t = {g(u / 10)}, h = {g(u * u / 20)} m.',
                       'Mistake identified (R1); correct maximum (A1).', 2)
    return explain(f'Explain why a concert organiser in {rng.choice(CITIES)} should not simply raise the ticket price as high as possible to maximise revenue.',
                   'Revenue = price × number sold; raising the price reduces the number sold, so revenue is a downward parabola with a maximum at the vertex, not at the highest price.',
                   'Trade-off identified (R1); vertex as optimum (R1).', 2)


@R.add('ch03-st4', 'C4', (3, 5), 'multi_step')
def optimise_task(rng, slot):
    city, country, cur, cname = place(rng)
    kind = rng.choice(['tickets', 'pens', 'kick', 'box'])
    if kind == 'tickets':
        p0 = rng.choice([20, 25, 30, 40])
        n0 = rng.choice([400, 500, 600, 800])
        dn = rng.choice([10, 20, 25])
        if n0 - dn * p0 <= 2 * dn:
            dn = 5
        # price p0 + x, sales n0 − dn x  → R = (p0 + x)(n0 − dn x)
        xv = Fr(n0 - dn * p0, 2 * dn)
        R0 = (p0 + xv) * (n0 - dn * xv)
        ans = f'(a) R = ({p0} + x)({n0} − {dn}x) (b) x = {fx(xv)} (c) price {cash(cur, p0 + xv)}, {g(float(n0 - dn * xv), 4)} tickets, revenue {cash(cur, R0)} (d) e.g. demand may not fall linearly; capacity limits'
        q_ = (f'A football club in {city} sells {n0} tickets at {money(cur, p0, 0)}. For every {money(cur, 1, 0)} increase in price, {dn} fewer tickets are sold. Let x be the price increase. (a) Write the revenue R in terms of x. '
              f'(b) Find the value of x that maximises R. (c) Find the best price, the number of tickets and the revenue. (d) State one limitation of the model.')
    elif kind == 'pens':
        L = rng.choice([60, 90, 120, 150])
        k = rng.choice([2, 3])
        # k equal pens side by side: fence = 2 lengths? width x, (k+1) widths and 2 lengths: (k+1)x + 2y = L
        xv = Fr(L, 2 * (k + 1))
        yv = (L - (k + 1) * xv) / 2
        ans = f'(a) y = ({L} − {k + 1}x)/2 (b) A = x({L} − {k + 1}x)/2 (c) x = {fx(xv)} m, y = {fx(yv)} m (d) max area {fx(xv * yv)} m²'
        q_ = (f'A farm in {country} uses {L} m of fencing to make a rectangle divided into {k} equal pens by {k - 1} fence{"s" if k > 2 else ""} parallel to the width x m. Let the length be y m. '
              f'(a) Express y in terms of x. (b) Write the total area A in terms of x. (c) Find the dimensions that maximise A. (d) Find the maximum area.')
    elif kind == 'kick':
        u = rng.choice([14.7, 19.6, 24.5])
        h0 = rng.choice([0.5, 1, 1.5])
        bar = rng.choice([2.5, 3, 3.5])
        tm = u / 9.8
        hm = h0 + u * u / 19.6
        disc = u * u - 4 * 4.9 * (bar - h0)
        t1, t2 = (u - math.sqrt(disc)) / 9.8, (u + math.sqrt(disc)) / 9.8
        tl = (u + math.sqrt(u * u + 4 * 4.9 * h0)) / 9.8
        ans = f'(a) {rsf(hm, 3)} m at {rsf(tm, 3)} s (b) between {rsf(t1, 3)} s and {rsf(t2, 3)} s (c) {rsf(t2 - t1, 3)} s above the bar height (d) lands at {rsf(tl, 3)} s; air resistance is ignored'
        q_ = (f'In a rugby match in {city}, the ball’s height is h = −4.9t² + {g(u)}t + {g(h0)} metres. (a) Find the maximum height and when it occurs. (b) Find the times when the ball is above {g(bar)} m. '
              f'(c) For how long is it above that height? (d) When does it land, and what has the model ignored?')
    else:
        s = rng.choice([20, 24, 30, 36])
        # open-top tray: fold up sides of height x from s×s sheet... quadratic for surface? Use gutter: width s, fold x on each side: area of cross-section x(s − 2x)
        xv = Fr(s, 4)
        ans = f'(a) A = x({s} − 2x) (b) 0 < x < {s // 2} (c) x = {fx(xv)} cm (d) {fx(xv * (s - 2 * xv))} cm²'
        q_ = (f'A metal sheet {s} cm wide is bent along two lines to make a rain gutter in {city}, folding up x cm on each side to form a rectangular channel. (a) Write the cross-sectional area A. '
              f'(b) State the domain of x in context. (c) Find the value of x that gives the greatest flow area. (d) Find this area.')
    return short(q_, ans, f'{ans}. Quadratic model formed (M1 A1); vertex / roots found (A1 A1); solution interpreted and limitations discussed (D: R1 C1).', 6, 'multi_step', 'G5')



# =============================================================================================
# ch04 Functions: Domain, Range, Composite and Inverse
# =============================================================================================
R.facts('ch04-st1', F(
    terms=[('domain', 'the set of all input values (x-values) for which a function is defined'),
           ('range', 'the set of all output values (y-values) that a function produces from its domain'),
           ('function', 'a relation in which every input in the domain has exactly one output'),
           ('vertical line test', 'a graph represents a function if no vertical line crosses it more than once')],
    facts=[('What is the domain of f(x) = √(x − 3)?', 'x ≥ 3', ['x > 3', 'x ≥ 0', 'all real x'], 'The expression under the root must be ≥ 0.'),
           ('What is the range of f(x) = x² + 4?', 'f(x) ≥ 4', ['f(x) ≥ 0', 'all real numbers', 'f(x) > 4'], 'x² ≥ 0, so x² + 4 ≥ 4.'),
           ('Which value is excluded from the domain of f(x) = 5/(x + 2)?', 'x = −2', ['x = 2', 'x = 0', 'x = 5'], 'Division by zero is undefined.')],
    why=[('Explain why the domain of f(x) = 1/x excludes 0.', 'Division by zero is undefined, so f(0) has no value.'),
         ('Explain why a circle x² + y² = 25 is not the graph of a function.', 'A vertical line such as x = 3 meets it twice (y = 4 and y = −4), so one input has two outputs.'),
         ('Explain how to find the range of a quadratic function from its vertex.', 'The vertex is the lowest (a > 0) or highest (a < 0) point, so the range is y ≥ k or y ≤ k where k is the y-coordinate of the vertex.')],
    misc=[('The range of f(x) = (x − 2)² is x ≥ 2.', 'The range is about outputs: f(x) ≥ 0. (x ≥ 2 is not a restriction at all.)'),
          ('The domain of √(5 − x) is x ≥ 5.', 'Need 5 − x ≥ 0, so x ≤ 5.')],
    contrast=[('domain', 'range', 'The domain is the set of allowed inputs (x); the range is the set of outputs (y) that actually occur.')],
))


def _dr(rng):
    """Random function with its domain and range text."""
    kind = rng.choice(['sqrt', 'recip', 'quad', 'quadneg', 'lin_restricted', 'sqrtneg'])
    a, b = rng.randint(-6, 6), rng.randint(-5, 9)
    if kind == 'sqrt':
        return f'f(x) = √(x{sgn(-a) if a else ""}){sgn(b) if b else ""}', f'x ≥ {m(a)}', f'f(x) ≥ {m(b)}'
    if kind == 'sqrtneg':
        return f'f(x) = √({a} − x){sgn(b) if b else ""}'.replace('√(0 − x)', '√(−x)'), f'x ≤ {m(a)}', f'f(x) ≥ {m(b)}'
    if kind == 'recip':
        return f'f(x) = 1/(x{sgn(-a) if a else ""}){sgn(b) if b else ""}', f'x ≠ {m(a)}', f'f(x) ≠ {m(b)}'
    if kind == 'quad':
        return f'f(x) = (x{sgn(-a) if a else ""})²{sgn(b) if b else ""}', 'all real x', f'f(x) ≥ {m(b)}'
    if kind == 'quadneg':
        return f'f(x) = {m(b)} − (x{sgn(-a) if a else ""})²', 'all real x', f'f(x) ≤ {m(b)}'
    mm = rng.choice([2, 3, -2, -1, 4])
    lo, hi = sorted(rng.sample(range(-5, 6), 2))
    ys = sorted([mm * lo + b, mm * hi + b])
    return f'f(x) = {lin(mm, b)}, −∞ < x < ∞ restricted to {m(lo)} ≤ x ≤ {m(hi)}'.replace('−∞ < x < ∞ restricted to ', ''), f'{m(lo)} ≤ x ≤ {m(hi)}', f'{m(ys[0])} ≤ f(x) ≤ {m(ys[1])}'


@R.add('ch04-st1', 'C1', (1, 3), 'mcq')
def domain_mcq(rng, slot):
    f, d, r = _dr(rng)
    wr = [r.replace('f(x)', 'x'), d.replace('x', 'f(x)', 1) if d != 'all real x' else 'x ≥ 0', 'all real numbers' if r != 'all real numbers' else 'x > 0']
    wr = [w for w in dict.fromkeys(wr) if w != r]
    if len(wr) < 3:
        wr.append('f(x) > 0')
    return mcq(rng, f'What is the range of {f}?', r, wr[:3], f'Domain {d}; range {r}.')


@R.add('ch04-st1', 'C3', (1, 4), 'short')
def domain_range(rng, slot):
    f, d, r = _dr(rng)
    return short(f'State the domain and range of {f}.', f'domain {d}; range {r}', f'Domain {d} (A1) – {"root argument ≥ 0" if "√" in f else "denominator ≠ 0" if "1/" in f else "given/unrestricted"}; range {r} (A1).', 2)


@R.add('ch04-st1', 'C3', (2, 5), 'short')
def range_restricted(rng, slot):
    a = rng.choice([1, 2, -1])
    h, k = rng.randint(-4, 4), rng.randint(-6, 6)
    lo = h - rng.randint(1, 4)
    hi = h + rng.randint(1, 5)
    vals = [a * (t - h) ** 2 + k for t in (lo, hi)] + [k]
    ylo, yhi = min(vals), max(vals)
    f = f'f(x) = {coef(a)}(x{sgn(-h) if h else ""})²{sgn(k) if k else ""}'
    return short(f'Find the range of {f} for the domain {m(lo)} ≤ x ≤ {m(hi)}.', f'{m(ylo)} ≤ f(x) ≤ {m(yhi)}',
                 f'Vertex ({m(h)}, {m(k)}) lies in the domain (M1); f({m(lo)}) = {m(vals[0])}, f({m(hi)}) = {m(vals[1])} (A1); range {m(ylo)} ≤ f(x) ≤ {m(yhi)} (A1).', 3)


@R.add('ch04-st1', 'C2', (2, 4), 'explain')
def domain_explain(rng, slot):
    who = name(rng)
    a = rng.randint(1, 9)
    kind = rng.choice(['sqrt', 'func', 'context'])
    if kind == 'sqrt':
        return explain(f'{who} says the domain of f(x) = √(x − {a}) is x > {a}. Explain whether this is correct.',
                       f'Not quite: √0 = 0 is defined, so x = {a} is allowed; the domain is x ≥ {a}.', 'Endpoint tested (R1); correct domain (A1).', 2)
    if kind == 'func':
        return explain(f'Explain why y² = x (for x ≥ 0) is not a function of x, but y = √x is.',
                       f'For x = {a * a}, y² = x gives y = {a} or y = −{a} (two outputs); y = √x takes only the non-negative root, so each x has one output.',
                       'Two outputs shown (R1); one output for √x (R1).', 2)
    n = rng.choice([20, 30, 40, 50])
    return explain(f'A taxi fare is C(d) = 3 + 2d for a trip of d km, and the taxi will travel at most {n} km. Explain a sensible domain and the corresponding range.',
                   f'Distances are 0 < d ≤ {n} (no negative trips, maximum {n} km), so the fares are 3 < C ≤ {3 + 2 * n}.', 'Domain from context (R1); range (A1).', 2)


@R.add('ch04-st1', 'C4', (3, 5), 'multi_step')
def domain_task(rng, slot):
    city, country, cur, cname = place(rng)
    kind = rng.choice(['phone', 'tank', 'ticket', 'ball'])
    if kind == 'phone':
        c0, per = rng.choice([10, 15, 20]), rng.choice([2, 3, 4, 5])
        cap = rng.choice([20, 30, 40, 50])
        ans = f'(a) C(g) = {c0} + {per}g (b) 0 ≤ g ≤ {cap} (c) {money(cur, c0, 0)} ≤ C ≤ {money(cur, c0 + per * cap, 0)} (d) a discrete domain if only whole GB are charged: g ∈ {{0, 1, …, {cap}}}'
        q_ = (f'A mobile plan in {city} costs {money(cur, c0, 0)} per month plus {money(cur, per, 0)} per GB, with a cap of {cap} GB. (a) Write the cost C as a function of the data used, g GB. '
              f'(b) State a suitable domain. (c) Find the range. (d) Explain how the domain changes if data is charged only in whole GB.')
    elif kind == 'tank':
        V0 = rng.choice([500, 600, 800, 1000, 1200])
        r = rng.choice([20, 25, 40, 50])
        T = V0 / r
        ans = f'(a) V(t) = {V0} − {r}t (b) 0 ≤ t ≤ {g(T)} (c) 0 ≤ V ≤ {V0} (d) after {g(T)} minutes the tank is empty, so V(t) < 0 has no meaning'
        q_ = (f'A water tank in {city} holds {V0} L and drains at {r} L per minute. (a) Write the volume V as a function of time t minutes. (b) State the domain in context. (c) State the range. '
              f'(d) Explain why values of t beyond the domain make no sense.')
    elif kind == 'ticket':
        cap = rng.choice([200, 250, 300, 400])
        p = rng.choice([12, 15, 18, 25])
        cost = rng.choice([800, 1000, 1500])
        ans = f'(a) P(n) = {p}n − {cost} (b) n ∈ {{0, 1, 2, …, {cap}}} (c) −{money(cur, cost, 0)} ≤ P ≤ {money(cur, p * cap - cost, 0)} (d) break-even at n = {math.ceil(cost / p)} tickets'
        q_ = (f'A school concert in {city} sells tickets at {money(cur, p, 0)} each; the hall holds {cap} people and the costs are {money(cur, cost, 0)}. (a) Write the profit P as a function of the number of tickets sold, n. '
              f'(b) State the domain. (c) State the range. (d) Find the smallest number of tickets needed to make a profit of at least zero.')
    else:
        u = rng.choice([10, 15, 20, 25])
        tl = u / 5
        ans = f'(a) 0 ≤ t ≤ {g(tl)} (b) h(t) = 5t({g(tl)} − t); max at t = {g(tl / 2)}: {g(u * u / 20)} m (c) 0 ≤ h ≤ {g(u * u / 20)} (d) negative h after landing has no meaning'
        q_ = (f'A ball kicked in a stadium in {city} has height h(t) = {u}t − 5t² metres. (a) Find a suitable domain for the model. (b) Find the maximum height. (c) State the range. '
              f'(d) Explain why the model is not used outside the domain.')
    return short(q_, ans, f'{ans}. Function modelled (A1); domain justified from context (R1 A1); range found (A1); communication with correct notation (C1).', 5, 'multi_step', 'G5')


R.facts('ch04-st2', F(
    terms=[('composite function', 'a function formed by applying one function to the output of another: (f ∘ g)(x) = f(g(x))'),
           ('inner function', 'in f(g(x)), g is applied first, so g is the inner function'),
           ('function notation', 'writing f(x) to name the output of function f for input x')],
    facts=[('If f(x) = 2x and g(x) = x + 3, what is f(g(1))?', '8', ['5', '7', '6'], 'g(1) = 4, then f(4) = 8.'),
           ('If f(x) = x² and g(x) = x − 1, then f(g(x)) is:', '(x − 1)²', ['x² − 1', 'x² − x', '(x² − 1)²'], 'Put g(x) into f.'),
           ('In general, f(g(x)) and g(f(x)) are:', 'different', ['always equal', 'always zero', 'inverses'], 'The order of composition matters.')],
    why=[('Explain why f(g(x)) is usually different from g(f(x)).', 'The functions are applied in a different order, e.g. "add 3 then double" gives a different result from "double then add 3".'),
         ('Explain how to find f(g(2)).', 'Work from the inside: find g(2) first, then use that value as the input of f.'),
         ('Explain why the domain of f(g(x)) can be smaller than the domain of g.', 'Some outputs of g may not be allowed inputs for f, so those x-values must be removed.')],
    misc=[('f(g(x)) means f(x) × g(x).', 'It means apply g first and then f, not multiply.'),
          ('To find f(g(3)) you work out f(3) first.', 'The inner function g is applied first.')],
))


def _rand_lin(rng):
    return rng.choice([2, 3, -1, -2, 4, 5]), rng.randint(-7, 7)


@R.add('ch04-st2', 'C1', (1, 3), 'mcq')
def composite_mcq(rng, slot):
    a, b = _rand_lin(rng)
    c, d = _rand_lin(rng)
    v = rng.randint(-4, 5)
    fg = a * (c * v + d) + b
    gf = c * (a * v + b) + d
    wr = [m(gf), m((a * v + b) * (c * v + d)), m(a * v + b + c * v + d)]
    wr = [w for w in dict.fromkeys(wr) if w != m(fg)]
    while len(wr) < 3:
        wr.append(m(fg + len(wr) + 1))
    return mcq(rng, f'f(x) = {lin(a, b)} and g(x) = {lin(c, d)}. Find f(g({m(v)})).', m(fg), wr[:3],
               f'g({m(v)}) = {m(c * v + d)}; f({m(c * v + d)}) = {m(fg)}.')


@R.add('ch04-st2', 'C3', (1, 4), 'short')
def composite_expr(rng, slot):
    a, b = _rand_lin(rng)
    kind = rng.choice(['lin', 'quad', 'quad2'])
    if kind == 'lin':
        c, d = _rand_lin(rng)
        F_, G_ = a * x + b, c * x + d
    elif kind == 'quad':
        F_, G_ = x ** 2 + rng.randint(-5, 5), a * x + b
    else:
        F_, G_ = a * x + b, x ** 2 + rng.randint(-5, 5)
    fg = sp.expand(F_.subs(x, G_))
    gf = sp.expand(G_.subs(x, F_))
    return short(f'Given f(x) = {sx(F_)} and g(x) = {sx(G_)}, find (f ∘ g)(x) and (g ∘ f)(x) in simplified form.', f'(f ∘ g)(x) = {sx(fg)}; (g ∘ f)(x) = {sx(gf)}',
                 f'f(g(x)) = f({sx(G_)}) (M1) = {sx(fg)} (A1); g(f(x)) = {sx(gf)} (A1).', 3)


@R.add('ch04-st2', 'C3', (2, 5), 'short')
def composite_solve(rng, slot):
    a, b = _rand_lin(rng)
    c, d = _rand_lin(rng)
    xs = rng.randint(-6, 6)
    target = a * (c * xs + d) + b
    if rng.random() < 0.5:
        return short(f'f(x) = {lin(a, b)} and g(x) = {lin(c, d)}. Solve f(g(x)) = {m(target)}.', f'x = {m(xs)}',
                     f'f(g(x)) = {sx(sp.expand(a * (c * x + d) + b))} (M1 A1); = {m(target)} → x = {m(xs)} (A1).', 3)
    k = rng.randint(1, 6)
    # f(x) = x² + k, g(x) = c x + d ; f(g(x)) = target2 with g(x) = ±t
    t = rng.randint(1, 6)
    tgt = t * t + k
    x1, x2 = Fr(t - d, c), Fr(-t - d, c)
    return short(f'f(x) = x² + {k} and g(x) = {lin(c, d)}. Solve f(g(x)) = {tgt}.', f'x = {fx(max(x1, x2))} or x = {fx(min(x1, x2))}',
                 f'({lin(c, d)})² + {k} = {tgt} (M1); {lin(c, d)} = ±{t} (A1); x = {fx(x1)}, {fx(x2)} (A1).', 3)


@R.add('ch04-st2', 'C2', (2, 4), 'explain')
def composite_explain(rng, slot):
    who = name(rng)
    a, b = rng.randint(2, 5), rng.randint(1, 9)
    kind = rng.choice(['order', 'mult', 'domain'])
    if kind == 'order':
        v = rng.randint(1, 6)
        return explain(f'f(x) = {a}x and g(x) = x + {b}. {who} says f(g({v})) = g(f({v})). Explain, with calculations, whether this is true.',
                       f'f(g({v})) = f({v + b}) = {a * (v + b)}; g(f({v})) = g({a * v}) = {a * v + b}; they differ by {a * (v + b) - a * v - b}, because the order of operations changes.',
                       'Both evaluated (A1); conclusion with reason (R1).', 2)
    if kind == 'mult':
        return explain(f'{who} writes f(g(x)) = (x + {b})(x²) for f(x) = x² and g(x) = x + {b}. Explain the error.',
                       f'f(g(x)) means substitute g(x) into f: f(x + {b}) = (x + {b})², not a product of f and g.', 'Meaning of composition (R1); correct result (A1).', 2)
    return explain(f'f(x) = √x and g(x) = x − {b}. Explain why the domain of f(g(x)) is x ≥ {b}.',
                   f'f(g(x)) = √(x − {b}); the square root needs x − {b} ≥ 0, so x ≥ {b}.', 'Composite formed (A1); domain reason (R1).', 2)


@R.add('ch04-st2', 'C4', (3, 5), 'multi_step')
def composite_task(rng, slot):
    city, country, cur, cname = place(rng)
    kind = rng.choice(['exchange', 'discount', 'temp', 'ripple'])
    if kind == 'exchange':
        rate = rng.choice([1.08, 1.12, 0.92, 1.35, 0.85, 1.5])
        fee = rng.choice([2, 3, 4, 5])
        amt = rng.choice([200, 300, 500, 800])
        ans = f'(a) f(g(x)) = {g(rate)}(x − {fee}) (b) g(f(x)) = {g(rate)}x − {fee} (c) fee first: {r2(rate * (amt - fee))}; convert first: {r2(rate * amt - fee)} (d) the results differ by {r2(abs(fee * (rate - 1)))}: {"converting first" if rate > 1 else "charging the fee first"} gives the customer more, because in f(g(x)) the fee is also multiplied by the rate'
        q_ = (f'A bureau in {city} converts money with f(x) = {g(rate)}x and charges a fee g(x) = x − {fee}. (a) Write f(g(x)) and explain what it means. (b) Write g(f(x)). '
              f'(c) Find both values for x = {amt}. (d) Explain why the order matters to a customer.')
    elif kind == 'discount':
        p = rng.choice([10, 15, 20, 25])
        c = rng.choice([5, 10, 20])
        price = rng.choice([80, 120, 150, 200, 250])
        d1 = (1 - p / 100) * (price - c)
        d2 = (1 - p / 100) * price - c
        ans = f'(a) D(x) = {g(1 - p / 100)}x, V(x) = x − {c} (b) D(V(x)) = {g(1 - p / 100)}(x − {c}); V(D(x)) = {g(1 - p / 100)}x − {c} (c) {cash(cur, d1)} vs {cash(cur, d2)} (d) V(D(x)) is cheaper for the customer by {cash(cur, d1 - d2)}'
        q_ = (f'A shop in {city} offers {p}% off (D) and a {money(cur, c, 0)} voucher (V). (a) Write D and V as functions of the price x. (b) Write D(V(x)) and V(D(x)). '
              f'(c) Find the price paid each way for a {money(cur, price, 0)} jacket. (d) Which order should a customer ask for, and why?')
    elif kind == 'temp':
        t = rng.randint(-10, 35)
        ans = f'(a) F(C) = 1.8C + 32 (b) K(C) = C + 273.15 (c) F(K⁻¹ … ) – composite: F as a function of kelvin: F = 1.8(K − 273.15) + 32 (d) {g(t + 273.15, 6)} K → {g(1.8 * t + 32, 4)} °F'
        q_ = (f'A weather station in {city} records temperature in kelvin. (a) Write the function F(C) that converts °C to °F. (b) Write K(C) converting °C to kelvin. '
              f'(c) Write a composite function that converts kelvin directly to °F. (d) Use it to convert {g(t + 273.15, 6)} K.')
    else:
        v = rng.choice([2, 3, 4, 5])
        ans = f'(a) r(t) = {v}t (b) A(r) = πr² (c) A(r(t)) = {v * v}πt² (d) {g(v * v * math.pi * 25, 4)} cm² after 5 s; the area grows with the square of time'
        q_ = (f'A stone dropped into a pond in {city} makes a circular ripple whose radius grows at {v} cm per second. (a) Write the radius r as a function of time t. (b) Write the area A as a function of r. '
              f'(c) Find A(r(t)) and simplify it. (d) Find the area after 5 seconds and describe how the area grows.')
    return short(q_, ans, f'{ans}. Functions written (A1); composite formed in the correct order (M1 A1); evaluated (A1); context interpreted (D: R1).', 5, 'multi_step', 'G5')


R.facts('ch04-st3', F(
    terms=[('inverse function', 'the function f⁻¹ that reverses f: if f(a) = b then f⁻¹(b) = a'),
           ('one-to-one function', 'a function in which different inputs always give different outputs; only these have inverses'),
           ('reflection in y = x', 'the graph of f⁻¹ is the reflection of the graph of f in the line y = x')],
    facts=[('If f(x) = 3x − 6, what is f⁻¹(x)?', '(x + 6)/3', ['3x + 6', '(x − 6)/3', '1/(3x − 6)'], 'Swap and rearrange: x = 3y − 6.'),
           ('If f(5) = 12, then f⁻¹(12) is:', '5', ['12', '1/12', '−5'], 'The inverse reverses the mapping.'),
           ('The graph of y = f⁻¹(x) is a reflection of y = f(x) in:', 'the line y = x', ['the x-axis', 'the y-axis', 'the origin'], 'Inputs and outputs swap.')],
    why=[('Explain why f(x) = x² (all real x) has no inverse function.', 'It is not one-to-one: f(2) = f(−2) = 4, so the inverse would have to send 4 to two values.'),
         ('Explain why f⁻¹(x) is not the same as 1/f(x).', 'f⁻¹ undoes f; 1/f(x) is the reciprocal of the output. For f(x) = 2x, f⁻¹(x) = x/2 but 1/f(x) = 1/(2x).'),
         ('Explain why the domain of f⁻¹ is the range of f.', 'The inverse takes the outputs of f as its inputs, so its allowed inputs are exactly the values f produces.')],
    misc=[('f⁻¹(x) = 1/f(x).', 'The −1 means inverse function, not reciprocal.'),
          ('Every function has an inverse.', 'Only one-to-one functions do; others need their domain restricted.')],
))


def _dv(a):
    return str(a) if a > 0 else f'({m(a)})'


@R.add('ch04-st3', 'C1', (1, 3), 'mcq')
def inverse_mcq(rng, slot):
    a, b = rng.choice([2, 3, 4, 5, -2]), rng.randint(-9, 9)
    if b == 0:
        b = 3
    corr = f'(x{sgn(-b)})/{a}' if a > 0 else f'({m(b)} − x)/{-a}'
    wr = [f'{m(a)}x{sgn(-b)}', f'(x{sgn(b)})/{a}' if a > 0 else f'({m(-b)} − x)/{-a}', f'1/({lin(a, b)})']
    return mcq(rng, f'f(x) = {lin(a, b)}. Which is f⁻¹(x)?', corr, wr, f'x = {lin(a, b, "y")} → y = (x{sgn(-b)})/{m(a)}.')


@R.add('ch04-st3', 'C3', (1, 4), 'short')
def inverse_find(rng, slot):
    kind = rng.choice(['lin', 'frac', 'cube', 'rat']) if slot.d >= 3 else 'lin'
    a, b = rng.choice([2, 3, 4, 5, -3]), rng.randint(-9, 9)
    if kind == 'lin':
        v = rng.randint(-10, 20)
        return short(f'f(x) = {lin(a, b)}. Find f⁻¹(x) and f⁻¹({m(v)}).', f'f⁻¹(x) = (x{sgn(-b) if b else ""})/{_dv(a)}; f⁻¹({m(v)}) = {fx(Fr(v - b, a))}',
                     f'Swap x and y: x = {lin(a, b, "y")} (M1); y = (x{sgn(-b) if b else ""})/{_dv(a)} (A1); f⁻¹({m(v)}) = {fx(Fr(v - b, a))} (A1).', 3)
    if kind == 'frac':
        c = rng.choice([2, 3, 4, 5])
        return short(f'f(x) = ({lin(a, b)})/{c}. Find f⁻¹(x).', f'f⁻¹(x) = ({c}x{sgn(-b) if b else ""})/{_dv(a)}',
                     f'x = ({lin(a, b, "y")})/{c} (M1); {c}x = {lin(a, b, "y")} (A1); y = ({c}x{sgn(-b) if b else ""})/{_dv(a)} (A1).', 3)
    if kind == 'cube':
        return short(f'f(x) = x³{sgn(b) if b else ""}. Find f⁻¹(x) and f⁻¹({m(b + 8)}).', f'f⁻¹(x) = ∛(x{sgn(-b) if b else ""}); f⁻¹({m(b + 8)}) = 2',
                     f'x = y³{sgn(b) if b else ""} (M1); y = ∛(x{sgn(-b) if b else ""}) (A1); ∛8 = 2 (A1).', 3)
    c = rng.randint(1, 6)
    return short(f'f(x) = {c}/(x{sgn(-b) if b else ""}), x ≠ {m(b)}. Find f⁻¹(x) and state its domain.', f'f⁻¹(x) = {c}/x{sgn(b) if b else ""}, x ≠ 0',
                 f'x = {c}/(y{sgn(-b) if b else ""}) (M1); y{sgn(-b) if b else ""} = {c}/x (A1); y = {c}/x{sgn(b) if b else ""}, x ≠ 0 (A1).', 3)


@R.add('ch04-st3', 'C3', (2, 5), 'short')
def inverse_verify(rng, slot):
    a, b = rng.choice([2, 3, 4, -2]), rng.randint(-8, 8)
    h, k = rng.randint(1, 5), rng.randint(-5, 5)
    if rng.random() < 0.5:
        e = sp.expand(a * ((x - b) / a) + b)
        return short(f'f(x) = {lin(a, b)}. Find f⁻¹(x) and show that f(f⁻¹(x)) = x.', f'f⁻¹(x) = (x{sgn(-b) if b else ""})/{m(a)}; f(f⁻¹(x)) = {m(a)} × (x{sgn(-b) if b else ""})/{m(a)}{sgn(b) if b else ""} = {sx(e)}',
                     'Inverse (A1); composition set up (M1); simplifies to x (A1).', 3)
    return short(f'f(x) = (x − {h})² {"+" if k >= 0 else "−"} {abs(k)} for x ≥ {h}. Find f⁻¹(x), and state its domain and range.',
                 f'f⁻¹(x) = {h} + √(x{sgn(-k) if k else ""}); domain x ≥ {m(k)}; range f⁻¹(x) ≥ {h}',
                 f'x = (y − {h})²{sgn(k) if k else ""} (M1); positive root since y ≥ {h} (R1); f⁻¹(x) = {h} + √(x{sgn(-k) if k else ""}) (A1); domain/range swap (A1).', 4)


@R.add('ch04-st3', 'C2', (2, 4), 'explain')
def inverse_explain(rng, slot):
    who = name(rng)
    a = rng.randint(2, 6)
    kind = rng.choice(['recip', 'restrict', 'graph'])
    if kind == 'recip':
        return explain(f'{who} says that for f(x) = {a}x, f⁻¹(x) = 1/({a}x). Explain the error.',
                       f'f⁻¹ undoes f: dividing by {a} undoes multiplying by {a}, so f⁻¹(x) = x/{a}. 1/({a}x) is the reciprocal of f(x).', 'Notation explained (R1); correct inverse (A1).', 2)
    if kind == 'restrict':
        return explain(f'Explain why f(x) = (x − {a})² needs a restricted domain before it can have an inverse, and suggest a suitable domain.',
                       f'It is not one-to-one, e.g. f({a - 1}) = f({a + 1}) = 1. Restricting to x ≥ {a} (one side of the vertex) makes it one-to-one.', 'Not one-to-one shown (R1); domain (A1).', 2)
    return explain(f'The point ({a}, {a * a + 1}) lies on y = f(x). Explain which point must lie on y = f⁻¹(x), and why.',
                   f'({a * a + 1}, {a}): the inverse swaps inputs and outputs, which reflects the point in y = x.', 'Point (A1); reason (R1).', 2)


@R.add('ch04-st3', 'C4', (3, 5), 'multi_step')
def inverse_task(rng, slot):
    city, country, cur, cname = place(rng)
    kind = rng.choice(['taxi', 'temp', 'shoe', 'code'])
    if kind == 'taxi':
        c0, per = rng.choice([3, 4, 5]), rng.choice([1.5, 2, 2.5, 3])
        budget = rng.choice([30, 40, 50, 60])
        ans = f'(a) C(d) = {g(c0)} + {g(per)}d (b) C⁻¹(x) = (x − {g(c0)})/{g(per)} (c) {g((budget - c0) / per, 4)} km (d) C⁻¹ gives the distance for a given fare'
        q_ = (f'A taxi in {city} charges {cash(cur, c0)} plus {cash(cur, per)} per km. (a) Write the cost C as a function of distance d. (b) Find the inverse function. '
              f'(c) Use it to find how far you can travel for {money(cur, budget, 0)}. (d) Explain what the inverse function represents in context.')
    elif kind == 'temp':
        t = rng.randint(40, 100)
        ans = f'(a) F⁻¹(x) = (x − 32)/1.8 (b) {g((t - 32) / 1.8, 4)} °C (c) F(F⁻¹(x)) = 1.8(x − 32)/1.8 + 32 = x (d) the two graphs are reflections in y = x; they meet at (−40, −40)'
        q_ = (f'Visitors from {city} convert temperatures with F(C) = 1.8C + 32. (a) Find the inverse function. (b) Use it to convert {t} °F to °C. (c) Show that F(F⁻¹(x)) = x. '
              f'(d) Describe how the graphs of F and F⁻¹ are related and find where they intersect.')
    elif kind == 'shoe':
        a, b = rng.choice([(1.5, 1.5), (1.27, 2), (3, -22)])
        L = rng.randint(22, 29)
        S = a * L + b
        ans = f'(a) S(L) = {g(a)}L {"+" if b >= 0 else "−"} {g(abs(b))} (b) S⁻¹(x) = (x {"−" if b >= 0 else "+"} {g(abs(b))})/{g(a)} (c) size {g(S, 3)}; length {g((S - b) / a, 3)} cm (d) only for lengths where the sizes are realistic, e.g. 20 ≤ L ≤ 32 cm'
        q_ = (f'A shoe company in {city} converts foot length L cm into a size using S(L) = {g(a)}L {"+" if b >= 0 else "−"} {g(abs(b))}. (a) Write down S(L). (b) Find S⁻¹(x). '
              f'(c) Find the size for a {L} cm foot, and use the inverse to check your answer. (d) Suggest a sensible domain.')
    else:
        a, b = rng.choice([3, 5, 7]), rng.randint(2, 9)
        word = [rng.randint(1, 26) for _ in range(4)]
        enc = [a * w + b for w in word]
        ans = f'(a) {", ".join(map(str, enc))} (b) E⁻¹(x) = (x − {b})/{a} (c) {", ".join(map(str, word))} (d) E must be one-to-one so that every code number decodes to exactly one letter'
        q_ = (f'A coding club in {city} encrypts letters (A = 1, …, Z = 26) with E(x) = {a}x + {b}. (a) Encode the numbers {", ".join(map(str, word))}. (b) Find the decoding function E⁻¹. '
              f'(c) Decode {", ".join(map(str, enc))}. (d) Explain why the encoding function must be one-to-one.')
    return short(q_, ans, f'{ans}. Function and inverse found (A1 M1 A1); inverse used correctly (A1); meaning in context or graphical link explained (D/C: R1).', 5, 'multi_step', 'G5')


R.facts('ch04-st4', F(
    terms=[('rational function', 'a function that is a fraction of two polynomials, such as f(x) = (2x + 1)/(x − 3)'),
           ('vertical asymptote', 'a vertical line x = a that the graph approaches but never meets, where the denominator is zero'),
           ('horizontal asymptote', 'a horizontal line y = b that the graph approaches as x becomes very large or very small')],
    facts=[('What is the vertical asymptote of y = 1/(x − 4)?', 'x = 4', ['x = −4', 'y = 4', 'y = 0'], 'The denominator is zero at x = 4.'),
           ('What is the horizontal asymptote of y = 3 + 2/(x + 1)?', 'y = 3', ['y = 2', 'x = −1', 'y = 0'], '2/(x + 1) → 0 as x grows.'),
           ('The horizontal asymptote of y = (6x + 1)/(2x − 5) is:', 'y = 3', ['y = 6', 'x = 5/2', 'y = −1/5'], 'Ratio of leading coefficients: 6/2.')],
    why=[('Explain why y = 1/x never equals 0.', 'A fraction is 0 only if its numerator is 0; the numerator is 1, so 1/x is never 0.'),
         ('Explain why the graph of y = 1/(x − 2) has a vertical asymptote at x = 2.', 'At x = 2 the denominator is 0 and the function is undefined; as x approaches 2 the values grow without bound.'),
         ('Explain how to find the horizontal asymptote of y = (ax + b)/(cx + d).', 'For large |x| the constants matter less, so y ≈ ax/(cx) = a/c.')],
    misc=[('y = 5/(x + 3) has a vertical asymptote at x = 3.', 'The denominator is zero when x = −3.'),
          ('A graph can never cross any asymptote.', 'It never meets a vertical asymptote, but it may cross a horizontal one for small x.')],
))


@R.add('ch04-st4', 'C1', (1, 3), 'mcq')
def asymptote_mcq(rng, slot):
    a, b = rng.randint(-6, 6), rng.randint(-6, 6)
    k = rng.choice([1, 2, 3, 5, -1, -4])
    f = f'y = {k}/(x{sgn(-a) if a else ""}){sgn(b) if b else ""}'
    corr = f'x = {m(a)} and y = {m(b)}'
    wr = [f'x = {m(-a)} and y = {m(b)}', f'x = {m(a)} and y = {m(k)}', f'x = {m(b)} and y = {m(a)}']
    wr = [w for w in dict.fromkeys(wr) if w != corr]
    while len(wr) < 3:
        wr.append(f'x = {m(-a)} and y = {m(-b - 1)}')
    return mcq(rng, f'State the asymptotes of {f}.', corr, wr[:3], f'Denominator 0 at x = {m(a)}; fraction → 0 so y → {m(b)}.')


@R.add('ch04-st4', 'C3', (1, 4), 'short')
def rational_features(rng, slot):
    a, c = rng.choice([1, 2, 3, 4, -2]), rng.choice([1, 2])
    b, d = rng.randint(-9, 9), rng.randint(-6, 6)
    if a * d - b * c == 0:
        return None
    num, den = a * x + b, c * x + d
    va, ha = Fr(-d, c), Fr(a, c)
    xi = Fr(-b, a)
    yi = Fr(b, d) if d else None
    return short(f'For f(x) = ({sx(num)})/({sx(den)}), find the vertical and horizontal asymptotes and the axis intercepts.',
                 f'x = {fx(va)}; y = {fx(ha)}; x-intercept ({fx(xi)}, 0); ' + (f'y-intercept (0, {fx(yi)})' if yi is not None else 'no y-intercept (x = 0 is the asymptote)'),
                 f'VA: denominator 0 (A1); HA: ratio {a}/{c} (A1); x-intercept from numerator 0 (A1); y-intercept f(0) (A1).', 4)


@R.add('ch04-st4', 'C3', (2, 5), 'short')
def rational_transform(rng, slot):
    k = rng.choice([1, 2, 3, 4, 6, -2, -3])
    h, v = rng.randint(-5, 5), rng.randint(-5, 5)
    if rng.random() < 0.5:
        return short(f'Describe the transformations that map y = 1/x onto y = {k}/(x{sgn(-h) if h else ""}){sgn(v) if v else ""}, and state the asymptotes of the new graph.',
                     f'{"vertical stretch factor " + str(abs(k)) + (", reflection in the x-axis" if k < 0 else "") + "; " if abs(k) != 1 or k < 0 else ""}translation by ({m(h)} over {m(v)}); asymptotes x = {m(h)}, y = {m(v)}',
                     'Stretch/reflection (A1); translation vector (A1); asymptotes (A1).', 3)
    # find domain and range
    return short(f'State the domain and range of f(x) = {k}/(x{sgn(-h) if h else ""}){sgn(v) if v else ""}.', f'domain x ≠ {m(h)}; range f(x) ≠ {m(v)}',
                 f'x ≠ {m(h)} (A1); the fraction is never 0, so f(x) ≠ {m(v)} (R1 A1).', 3)


@R.add('ch04-st4', 'C2', (2, 4), 'explain')
def rational_explain(rng, slot):
    who = name(rng)
    a = rng.randint(1, 7)
    kind = rng.choice(['zero', 'sign', 'cross'])
    if kind == 'zero':
        return explain(f'Explain why the range of f(x) = {a}/x + {a} does not include {a}.', f'{a}/x is never 0 (numerator {a} ≠ 0), so f(x) can never equal {a}; y = {a} is the horizontal asymptote.',
                       'Fraction never 0 (R1); link to asymptote (R1).', 2)
    if kind == 'sign':
        return explain(f'{who} says y = 1/(x + {a}) has its vertical asymptote at x = {a}. Explain the mistake.',
                       f'The asymptote is where the denominator is 0: x + {a} = 0 gives x = −{a}.', 'Denominator condition (R1); correct asymptote (A1).', 2)
    return explain(f'Explain how the graph of y = {a}/x behaves as x gets very large and as x gets close to 0 from the right.',
                   f'As x → ∞, {a}/x → 0 (approaches the x-axis); as x → 0⁺, {a}/x becomes very large and positive (approaches the y-axis).', 'Large x behaviour (R1); near 0 behaviour (R1).', 2)


@R.add('ch04-st4', 'C4', (3, 5), 'multi_step')
def rational_task(rng, slot):
    city, country, cur, cname = place(rng)
    kind = rng.choice(['average', 'share', 'drug', 'speed'])
    if kind == 'average':
        F0, v = rng.choice([500, 800, 1200, 2000]), rng.choice([2, 3, 4, 5])
        n = rng.choice([100, 200, 500])
        target = v + rng.choice([1, 2])
        need = math.ceil(F0 / (target - v))
        ans = f'(a) A(n) = ({F0} + {v}n)/n = {v} + {F0}/n (b) {cash(cur, v + F0 / n)} (c) y = {v}: the average cost approaches the variable cost {money(cur, v, 0)} (d) n ≥ {need} items'
        q_ = (f'A print shop in {city} has fixed costs of {money(cur, F0, 0)} and spends {money(cur, v, 0)} per poster. (a) Write the average cost per poster A(n) for n posters. (b) Find A({n}). '
              f'(c) State the horizontal asymptote and interpret it. (d) How many posters must be printed for the average cost to be at most {money(cur, target, 0)}?')
    elif kind == 'share':
        P = rng.choice([600, 900, 1200, 1500])
        ans = f'(a) S(n) = {P}/n (b) n ≠ 0; in context n ∈ {{1, 2, 3, …}} (c) S → 0 but never reaches it (d) {math.ceil(P / 50)} people for at most {money(cur, 50, 0)} each'
        q_ = (f'A group in {city} shares the {money(cur, P, 0)} cost of a holiday house equally between n people. (a) Write the share S(n). (b) State the domain in context. '
              f'(c) Describe what happens to S as n increases, using asymptotes. (d) How many people are needed for each share to be at most {money(cur, 50, 0)}?')
    elif kind == 'drug':
        k = rng.choice([20, 30, 40, 50])
        ans = f'(a) C(0) = 0, C(1) = {g(k / 2, 3)}, C(4) = {g(4 * k / 17, 3)} (b) the denominator t² + 1 grows faster than kt (c) y = 0 (d) the concentration falls towards zero as the drug leaves the body'
        q_ = (f'A clinic in {city} models the concentration of a medicine as C(t) = {k}t/(t² + 1) mg/L after t hours. (a) Find C(0), C(1) and C(4). (b) Explain why C(t) decreases for large t. '
              f'(c) State the horizontal asymptote. (d) Interpret the asymptote in context.')
    else:
        d = rng.choice([120, 180, 240, 300])
        ans = f'(a) t(v) = {d}/v (b) {g(d / 60, 3)} h at 60 km/h; {g(d / 100, 3)} h at 100 km/h (c) as v → 0, t → ∞ (vertical asymptote v = 0); as v grows, t → 0 (d) v > 0, and in practice up to the speed limit'
        q_ = (f'A drive from {city} to a nearby town is {d} km. (a) Write the time t hours as a function of the average speed v km/h. (b) Find the time at 60 km/h and 100 km/h. '
              f'(c) Describe the asymptotes and what they mean. (d) State a sensible domain.')
    return short(q_, ans, f'{ans}. Rational model formed (A1); values found (A1); asymptotes identified and interpreted (A1 R1); communication (C1).', 5, 'multi_step', 'G5')


# =============================================================================================
# ch05 Exponential Functions and Models
# =============================================================================================
R.facts('ch05-st1', F(
    terms=[('exponential function', 'a function of the form f(x) = a × bˣ + c with b > 0, b ≠ 1'),
           ('horizontal asymptote', 'the line y = c that the graph of y = a × bˣ + c approaches but never reaches'),
           ('growth and decay', 'the behaviour of y = bˣ, which increases (growth) when b > 1 and decreases (decay) when 0 < b < 1')],
    facts=[('What is the y-intercept of y = 3 × 2ˣ?', '3', ['2', '6', '1'], '2⁰ = 1.'),
           ('What is the horizontal asymptote of y = 5ˣ − 4?', 'y = −4', ['y = 0', 'y = 5', 'x = −4'], '5ˣ → 0 as x → −∞.'),
           ('Which function represents decay?', 'y = 0.8ˣ', ['y = 1.2ˣ', 'y = 2ˣ', 'y = x²'], 'The base is between 0 and 1.')],
    why=[('Explain why y = 2ˣ is always positive.', 'A positive number raised to any real power is positive, so the graph stays above the x-axis.'),
         ('Explain why every graph y = bˣ passes through (0, 1).', 'b⁰ = 1 for any b > 0.'),
         ('Explain how y = 2ˣ + 3 differs from y = 2ˣ.', 'It is translated 3 units up, so its asymptote is y = 3 and its y-intercept is 4.')],
    misc=[('y = 2ˣ crosses the x-axis at x = 0.', 'It never crosses the x-axis; it crosses the y-axis at (0, 1).'),
          ('y = (1/2)ˣ is the same as y = −2ˣ.', '(1/2)ˣ = 2^(−x), a reflection in the y-axis, and is positive; −2ˣ is negative.')],
))


@R.add('ch05-st1', 'C1', (1, 3), 'mcq')
def exp_graph_mcq(rng, slot):
    a, b, c = rng.choice([1, 2, 3, 4, 5]), rng.choice([2, 3, 4]), rng.randint(-6, 6)
    f = f'y = {coef(a)}{b}ˣ{sgn(c) if c else ""}'.replace('y = ', 'y = ', 1)
    if a != 1:
        f = f'y = {a} × {b}ˣ{sgn(c) if c else ""}'
    corr = f'(0, {m(a + c)}) and y = {m(c)}'
    wr = [f'(0, {m(a)}) and y = {m(c)}', f'(0, {m(a + c)}) and y = 0', f'(0, {m(c)}) and y = {m(a)}']
    wr = [w for w in dict.fromkeys(wr) if w != corr]
    while len(wr) < 3:
        wr.append(f'(0, {m(a + c + 1)}) and y = {m(c - 1)}')
    return mcq(rng, f'State the y-intercept and horizontal asymptote of {f}.', corr, wr[:3], f'At x = 0: {a} + {m(c)} = {m(a + c)}; as x → −∞, y → {m(c)}.')


@R.add('ch05-st1', 'C3', (1, 4), 'short')
def exp_graph_features(rng, slot):
    a = rng.choice([1, 2, 3, -1, -2, 5])
    b = rng.choice([2, 3, Fr(1, 2), Fr(1, 3), 4])
    c = rng.randint(-6, 6)
    bt = fx(b) if Fr(b).denominator == 1 else f'({fx(b)})'
    f = f'y = {"" if a == 1 else "−" if a == -1 else str(a) + " × "}{bt}ˣ{sgn(c) if c else ""}'
    yi = a + c
    vals = [(t, a * Fr(b) ** t + c) for t in (-1, 1, 2)]
    beh = 'increasing' if (a > 0) == (Fr(b) > 1) else 'decreasing'
    rng_txt = f'y > {m(c)}' if a > 0 else f'y < {m(c)}'
    return short(f'For {f}: (a) find the y-intercept, (b) state the horizontal asymptote, (c) state whether the function is increasing or decreasing, (d) state the range.',
                 f'(a) (0, {m(yi)}) (b) y = {m(c)} (c) {beh} (d) {rng_txt}',
                 f'y-intercept (A1); asymptote (A1); {beh} – check values {", ".join(f"f({m(t)}) = {fx(v)}" for t, v in vals)} (A1); range (A1).', 4)


@R.add('ch05-st1', 'C3', (2, 5), 'short')
def exp_find_params(rng, slot):
    b = rng.choice([2, 3, 4, 5])
    a = rng.choice([1, 2, 3, 4, 5, 6])
    c = rng.randint(-5, 5)
    x1 = rng.randint(1, 3)
    y1 = a * b ** x1 + c
    return short(f'The graph of y = a × {b}ˣ + c has horizontal asymptote y = {m(c)} and passes through (0, {m(a + c)}). Find a and c, and hence find y when x = {x1}.',
                 f'a = {a}, c = {m(c)}; y = {m(y1)}', f'c from the asymptote (A1); a + c = {m(a + c)} → a = {a} (A1); y = {a} × {b}{sup(x1)}{sgn(c) if c else ""} = {m(y1)} (A1).', 3)


@R.add('ch05-st1', 'C2', (2, 4), 'explain')
def exp_graph_explain(rng, slot):
    who = name(rng)
    b = rng.choice([2, 3, 4, 5])
    c = rng.randint(1, 8)
    kind = rng.choice(['zero', 'reflect', 'compare'])
    if kind == 'zero':
        return explain(f'{who} says y = {b}ˣ + {c} crosses the x-axis when x is very negative. Explain why this is wrong.',
                       f'{b}ˣ > 0 for all x, so y > {c} > 0; the graph approaches the asymptote y = {c} but never crosses the x-axis.', 'Positivity (R1); asymptote (R1).', 2)
    if kind == 'reflect':
        return explain(f'Explain why the graphs of y = {b}ˣ and y = (1/{b})ˣ are reflections of each other in the y-axis.',
                       f'(1/{b})ˣ = {b}^(−x), so each point (x, y) on y = {b}ˣ corresponds to (−x, y) on the other graph.', 'Index law (R1); reflection (R1).', 2)
    k = rng.randint(5, 9)
    return explain(f'Explain why y = 2ˣ eventually becomes larger than y = x{sup(2)} + {c * 10}, even though it is smaller at x = {k - 4}.',
                   f'2ˣ doubles each time x increases by 1, while a quadratic grows by a steadily increasing but additive amount; exponential growth always overtakes polynomial growth (e.g. at x = 10: {2 ** 10} vs {100 + c * 10}).',
                   'Growth comparison (R1); numerical evidence (A1).', 2)


@R.add('ch05-st1', 'C4', (3, 5), 'multi_step')
def exp_graph_task(rng, slot):
    city = rng.choice(CITIES)
    kind = rng.choice(['coffee', 'family', 'compare', 'spread'])
    if kind == 'coffee':
        room = rng.choice([18, 20, 22, 24])
        T0 = rng.choice([85, 90, 95])
        k = rng.choice([0.9, 0.85, 0.8])
        ans = f'(a) T(0) = {T0} °C (b) T({10}) = {rsf(room + (T0 - room) * k ** 10, 3)} °C (c) y = {room}: the coffee cools towards room temperature (d) about {next(i for i in range(1, 200) if room + (T0 - room) * k ** i < 40)} minutes'
        q_ = (f'A cup of coffee in a café in {city} cools according to T(t) = {room} + {T0 - room} × {g(k)}ᵗ °C after t minutes. (a) Find the initial temperature. (b) Find the temperature after 10 minutes. '
              f'(c) State the horizontal asymptote and interpret it. (d) After how many whole minutes is the coffee first below 40 °C?')
    elif kind == 'family':
        c = rng.randint(1, 6)
        ans = f'(a) y-intercepts 1 + {c} = {1 + c} for all; asymptote y = {c} (b) larger b is steeper for x > 0 and flatter for x < 0 (c) they all meet at (0, {1 + c}) (d) b between 0 and 1 gives decreasing graphs with the same asymptote'
        q_ = (f'Investigate the family y = bˣ + {c} for b = 2, 3 and 5. (a) Find the y-intercept and asymptote of each. (b) Describe how the value of b changes the graph. '
              f'(c) State the point common to all the graphs. (d) Predict what happens when 0 < b < 1.')
    elif kind == 'compare':
        a = rng.choice([100, 200, 500])
        d = rng.choice([50, 80, 100])
        n = next(i for i in range(1, 100) if 2 ** i > a + d * i)
        ans = f'(a) Plan A: {a} + {d}n; Plan B: 2ⁿ (b) after 5 days A gives {a + 5 * d}, B gives 32 (c) day {n} (d) exponential growth eventually overtakes linear growth'
        q_ = (f'A savings app in {city} offers Plan A: {a} points plus {d} points per day, or Plan B: 2ⁿ points on day n. (a) Write a formula for each plan. (b) Compare the points after 5 days. '
              f'(c) On which day does Plan B first give more points? (d) Explain why this always happens eventually.')
    else:
        N0 = rng.choice([2, 3, 5])
        b = rng.choice([1.5, 2, 2.5])
        cap = rng.choice([1000, 5000, 10000])
        d = next(i for i in range(1, 200) if N0 * b ** i >= cap)
        ans = f'(a) {N0}, {g(N0 * b, 4)}, {g(N0 * b * b, 4)} (b) N = {N0} × {g(b)}ᵗ (c) day {d} (d) the model ignores the limited population; growth must slow down'
        q_ = (f'A rumour spreads in a school in {city}: {N0} students know it on day 0, and the number multiplies by {g(b)} each day. (a) Find the numbers on days 0, 1 and 2. (b) Write a model N(t). '
              f'(c) On which day does N first reach {big(cap)}? (d) Explain why the model fails eventually.')
    return short(q_, ans, f'{ans}. Exponential features found (A1 A1); calculations (M1 A1); pattern / limitation explained (B/D: R1).', 5, 'multi_step', 'G5')


R.facts('ch05-st2', F(
    terms=[('exponential growth model', 'N(t) = N₀ × bᵗ with b > 1, or N(t) = N₀(1 + r)ᵗ for growth at rate r per period'),
           ('exponential decay model', 'N(t) = N₀ × bᵗ with 0 < b < 1, e.g. N₀(1 − r)ᵗ or N₀(1/2)^(t/h) for half-life h'),
           ('half-life', 'the time taken for a decaying quantity to halve'),
           ('doubling time', 'the time taken for a growing quantity to double')],
    facts=[('A population of 500 grows by 8% per year. Which model is correct?', 'P = 500 × 1.08ᵗ', ['P = 500 × 0.08ᵗ', 'P = 500 + 8t', 'P = 500 × 8ᵗ'], 'Growth multiplier 1.08.'),
           ('A substance has a half-life of 6 days. What fraction remains after 18 days?', '1/8', ['1/3', '1/6', '1/2'], 'Three half-lives: (1/2)³.'),
           ('In N = 200 × 0.95ᵗ, the quantity decreases by:', '5% per period', ['95% per period', '0.95 per period', '200 per period'], '1 − 0.95 = 0.05.')],
    why=[('Explain why exponential decay never reaches zero in the model.', 'Each period the amount is multiplied by a positive number less than 1, so it stays positive.'),
         ('Explain why a constant percentage growth gives an exponential model rather than a linear one.', 'The increase each period is a percentage of the current amount, which itself grows; so equal time steps multiply rather than add.'),
         ('Explain why the half-life does not depend on the starting amount.', 'N₀(1/2)^(t/h) halves whenever t increases by h, whatever N₀ is.')],
    misc=[('Decay by 20% per year means N = N₀ × 0.2ᵗ.', 'Keeping 80% each year gives N₀ × 0.8ᵗ.'),
          ('After two half-lives nothing is left.', 'A quarter is left; each half-life halves what remains.')],
))


@R.add('ch05-st2', 'C1', (1, 3), 'mcq')
def growth_mcq(rng, slot):
    p = rng.choice([3, 4, 5, 6, 8, 12, 15, 20])
    up = rng.random() < 0.5
    N0 = rng.choice([200, 500, 1000, 2500])
    b = 1 + p / 100 if up else 1 - p / 100
    corr = f'N = {N0} × {g(b)}ᵗ'
    wr = [f'N = {N0} × {g(1 - p / 100 if up else 1 + p / 100)}ᵗ', f'N = {N0} × {g(p / 100)}ᵗ', f'N = {N0} {"+" if up else "−"} {p}t']
    return mcq(rng, f'A quantity starts at {N0} and {"grows" if up else "decreases"} by {p}% per year. Which model gives N after t years?', corr, wr, f'Multiplier {g(b)}.')


@R.add('ch05-st2', 'C3', (1, 4), 'short')
def growth_calc(rng, slot):
    city = rng.choice(CITIES)
    kind = rng.choice(['pop', 'decay', 'half'])
    if kind == 'pop':
        N0 = rng.randint(20, 900) * 100
        p = rng.choice([1.5, 2, 2.5, 3, 4, 6])
        t = rng.randint(4, 20)
        return short(f'The number of cyclists using a bike-share in {city} is {big(N0)} and grows by {g(p)}% per year. Predict the number after {t} years.', big(round(N0 * (1 + p / 100) ** t)),
                     f'N = {N0} × {g(1 + p / 100, 4)}ᵗ (M1); t = {t} (A1); ≈ {big(round(N0 * (1 + p / 100) ** t))} (A1).', 3)
    if kind == 'decay':
        N0 = rng.choice([80, 120, 200, 500])
        p = rng.choice([5, 8, 10, 12, 15])
        t = rng.randint(3, 12)
        return short(f'A lake near {city} has {N0} mg/L of a pollutant, which falls by {p}% each month. Find the level after {t} months.', f'{rsf(N0 * (1 - p / 100) ** t, 3)} mg/L',
                     f'Multiplier {g(1 - p / 100)} (A1); {N0} × {g(1 - p / 100)}{sup(t)} (M1); {rsf(N0 * (1 - p / 100) ** t, 3)} mg/L (A1).', 3)
    h = rng.choice([5, 8, 12, 15, 30])
    M = rng.choice([40, 64, 100, 250])
    t = rng.randint(h // 2, 4 * h)
    return short(f'A radioactive sample in a lab in {city} has a half-life of {h} hours and an initial mass of {M} g. Find the mass after {t} hours.', f'{rsf(M * 0.5 ** (t / h), 3)} g',
                 f'M = {M}(1/2)^(t/{h}) (M1); exponent {fx(Fr(t, h))} (A1); {rsf(M * 0.5 ** (t / h), 3)} g (A1).', 3)


@R.add('ch05-st2', 'C3', (2, 5), 'short')
def growth_find_rate(rng, slot):
    city = rng.choice(CITIES)
    N0 = rng.choice([100, 200, 400, 800, 1500])
    p = rng.choice([3, 4, 5, 6, 8, 10, 12])
    t = rng.randint(3, 10)
    up = rng.random() < 0.6
    b = 1 + p / 100 if up else 1 - p / 100
    Nt = round(N0 * b ** t)
    br = (Nt / N0) ** (1 / t)
    return short(f'The {rng.choice(["population of birds", "number of bees in a colony", "number of app users", "fish stock"])} near {city} changes from {big(N0)} to {big(Nt)} in {t} years. Assuming an exponential model N = N₀bᵗ, find b and the annual percentage {"growth" if up else "decrease"}.',
                 f'b ≈ {rsf(br, 3)}; about {rsf(abs(br - 1) * 100, 2)}% per year',
                 f'{Nt} = {N0}b{sup(t)} (M1); b = ({Nt}/{N0})^(1/{t}) ≈ {rsf(br, 4)} (A1); {rsf(abs(br - 1) * 100, 2)}% (A1).', 3)


@R.add('ch05-st2', 'C2', (2, 4), 'explain')
def growth_explain(rng, slot):
    who = name(rng)
    p = rng.choice([10, 20, 25, 30])
    kind = rng.choice(['wrongmult', 'half', 'linear'])
    if kind == 'wrongmult':
        return explain(f'{who} models a car losing {p}% of its value per year with V = V₀ × {g(p / 100)}ᵗ. Explain the mistake.',
                       f'Losing {p}% means keeping {100 - p}%, so the multiplier is {g(1 - p / 100)}: V = V₀ × {g(1 - p / 100)}ᵗ.', 'Multiplier explained (R1); correct model (A1).', 2)
    if kind == 'half':
        h = rng.choice([3, 4, 5, 8])
        return explain(f'A medicine has a half-life of {h} hours. {who} says it will all be gone after {2 * h} hours. Explain why this is wrong.',
                       f'Each half-life halves what remains: after {h} h, 1/2 is left; after {2 * h} h, 1/4 is left.', 'Repeated halving (R1); fraction left (A1).', 2)
    return explain(f'Explain why a town growing by {p}% a year gains more people each year, while one growing by 500 people a year does not.',
                   f'{p}% of a larger population is a larger number each year (exponential), whereas adding 500 is the same every year (linear).', 'Percentage of a changing amount (R1); comparison (R1).', 2)


@R.add('ch05-st2', 'C4', (3, 5), 'multi_step')
def growth_task(rng, slot):
    city, country, cur, cname = place(rng)
    kind = rng.choice(['carbon', 'phones', 'forest', 'caffeine'])
    if kind == 'carbon':
        pct = rng.choice([25, 40, 60, 70])
        t = 5730 * math.log(pct / 100) / math.log(0.5)
        ans = f'(a) N = N₀(1/2)^(t/5730) (b) {rsf(0.5 ** (1000 / 5730) * 100, 3)}% (c) about {rsf(t, 3)} years (d) the half-life is constant and very long compared with human history'
        q_ = (f'Carbon-14 has a half-life of 5730 years. A bone found near {city} has {pct}% of its original carbon-14. (a) Write a model for the fraction remaining. (b) What percentage remains after 1000 years? '
              f'(c) Estimate the age of the bone (use a graph or trial and improvement). (d) Explain why this method works for archaeological dating.')
    elif kind == 'phones':
        N0 = rng.choice([2, 5, 8, 12])
        p = rng.choice([20, 25, 30, 40])
        tgt = rng.choice([50, 80, 100])
        n = next(i for i in range(1, 100) if N0 * (1 + p / 100) ** i >= tgt)
        ans = f'(a) U = {N0} × {g(1 + p / 100)}ᵗ million (b) {rsf(N0 * (1 + p / 100) ** 5, 3)} million (c) year {n} (d) the number of people who could use the app is limited, so growth must slow; a logistic model would fit better later'
        q_ = (f'A new app launched in {country} has {N0} million users worldwide and grows by {p}% per year. (a) Write a model for the number of users U after t years. (b) Predict the users after 5 years. '
              f'(c) In which year do users first reach {tgt} million? (d) Discuss whether the model is realistic in the long term.')
    elif kind == 'forest':
        A0 = rng.choice([5000, 8000, 12000])
        p = rng.choice([2, 3, 4, 5])
        n = next(i for i in range(1, 300) if (1 - p / 100) ** i <= 0.5)
        ans = f'(a) A = {A0} × {g(1 - p / 100)}ᵗ km² (b) {big(round(A0 * (1 - p / 100) ** 10))} km² (c) {n} years (d) e.g. replanting would change the multiplier; deforestation rates vary'
        q_ = (f'A forest near {city} covers {big(A0)} km² and is shrinking by {p}% per year. (a) Write a model for the area A after t years. (b) Find the area after 10 years. '
              f'(c) After how many whole years will half of the forest be gone? (d) Suggest a reason why the model might change.')
    else:
        dose = rng.choice([80, 95, 120, 150, 200])
        h = rng.choice([4, 5, 6])
        ans = f'(a) C = {dose}(1/2)^(t/{h}) (b) {rsf(dose * 0.5 ** (8 / h), 3)} mg (c) about {next(i for i in range(1, 100) if dose * 0.5 ** (i / h) < 20)} hours (d) the decay is fastest at first in mg per hour, because half of a larger amount is lost each half-life'
        q_ = (f'A student in {city} drinks coffee with {dose} mg of caffeine; caffeine has a half-life of about {h} hours. (a) Write a model for the caffeine C mg after t hours. (b) Find the amount after 8 hours. '
              f'(c) After how many whole hours is it first below 20 mg? (d) Explain when the caffeine leaves the body fastest.')
    return short(q_, ans, f'{ans}. Correct exponential model (A1 M1); calculations (A1 A1); interpretation and limitations (D: R1 C1).', 6, 'multi_step', 'G5')


R.facts('ch05-st3', F(
    terms=[('exponential regression', 'using technology to find the exponential model y = a × bˣ that best fits a set of data'),
           ('ratio test for exponential data', 'if successive y-values (for equal x-steps) have an approximately constant ratio, an exponential model is suitable'),
           ('residual', 'the difference between an observed value and the value predicted by a model')],
    facts=[('Data with y-values 5, 10, 20, 40 for x = 0, 1, 2, 3 fit which model?', 'y = 5 × 2ˣ', ['y = 5x + 5', 'y = 2 × 5ˣ', 'y = 5x²'], 'Constant ratio 2 and starting value 5.'),
           ('Which data set is best modelled by an exponential function?', '3, 6, 12, 24', ['3, 6, 9, 12', '3, 5, 7, 9', '1, 4, 9, 16'], 'Only it has a constant ratio.'),
           ('In y = a × bˣ, the value of a is:', 'the value of y when x = 0', ['the growth rate', 'the asymptote', 'the value of y when x = 1'], 'b⁰ = 1.')],
    why=[('Explain how to decide whether a table of values is better modelled by a linear or an exponential function.', 'Linear data have constant differences for equal x-steps; exponential data have constant ratios.'),
         ('Explain why predictions from a fitted model become less reliable far outside the data.', 'The pattern might not continue (extrapolation), and small errors in b are multiplied many times.'),
         ('Explain how two data points determine a model y = a × bˣ.', 'Substituting both points gives two equations; dividing them eliminates a and gives b, then a follows.')],
    misc=[('If the differences increase, the data must be exponential.', 'Quadratic data also have increasing differences; check whether the ratios are constant.'),
          ('An exponential model fitted to data will pass through every point.', 'A best-fit model is close to the points but not usually through all of them.')],
))


@R.add('ch05-st3', 'C1', (1, 3), 'mcq')
def fit_mcq(rng, slot):
    a, b = rng.choice([2, 3, 4, 5, 10]), rng.choice([2, 3])
    ys = [a * b ** i for i in range(4)]
    corr = f'y = {a} × {b}ˣ'
    return mcq(rng, f'The table shows x = 0, 1, 2, 3 and y = {", ".join(map(str, ys))}. Which model fits exactly?', corr,
               [f'y = {b} × {a}ˣ', f'y = {a}x + {ys[1] - a}' if ys[1] != a else f'y = {a}x', f'y = {a} × {b + 1}ˣ'], f'Constant ratio {b}; y(0) = {a}.')


@R.add('ch05-st3', 'C3', (1, 4), 'short')
def fit_two_points(rng, slot):
    a = rng.choice([2, 3, 4, 5, 6, 8, 10, 20])
    b = rng.choice([2, 3, Fr(1, 2), Fr(3, 2), 4])
    x1, x2 = sorted(rng.sample(range(1, 6), 2))
    y1, y2 = a * Fr(b) ** x1, a * Fr(b) ** x2
    return short(f'An exponential model y = a × bˣ passes through ({x1}, {fx(y1)}) and ({x2}, {fx(y2)}). Find a and b.', f'a = {a}, b = {fx(b)}',
                 f'Divide: b{sup(x2 - x1)} = {fx(y2 / y1)} (M1); b = {fx(b)} (A1); a = {fx(y1)} ÷ {fx(b)}{sup(x1)} = {a} (A1).', 3)


@R.add('ch05-st3', 'C3', (2, 5), 'short')
def fit_table(rng, slot):
    city = rng.choice(CITIES)
    a = rng.choice([50, 80, 120, 200, 500])
    b = rng.choice([1.2, 1.3, 1.5, 0.8, 0.7, 0.9])
    ys = [round(a * b ** i * rng.uniform(0.98, 1.02)) for i in range(5)]
    ratios = [ys[i + 1] / ys[i] for i in range(4)]
    bb = sum(ratios) / 4
    what = rng.choice(['online followers of a band', 'mould spots on bread', 'visitors to a website (hundreds)', 'temperature difference of cooling tea (°C)'])
    xp = 7
    return short(f'The {what} in {city} over 5 days (day 0 to day 4) were {", ".join(map(str, ys))}. (a) Show that the data are approximately exponential. (b) Estimate the ratio b and write a model y = a × bᵗ. (c) Predict day {xp}.',
                 f'(a) ratios {", ".join(rsf(r, 3) for r in ratios)} ≈ constant (b) b ≈ {rsf(bb, 3)}, y ≈ {ys[0]} × {rsf(bb, 3)}ᵗ (c) ≈ {rsf(ys[0] * float(rsf(bb, 3)) ** xp, 3)}',
                 'Ratios calculated (M1 A1); model (A1); prediction with comment on extrapolation (A1).', 4)


@R.add('ch05-st3', 'C2', (2, 4), 'explain')
def fit_explain(rng, slot):
    who = name(rng)
    a, d = rng.randint(2, 8), rng.randint(2, 6)
    kind = rng.choice(['linear', 'extrap', 'diff'])
    if kind == 'linear':
        ys = [a + d * i for i in range(4)]
        return explain(f'{who} says the data {", ".join(map(str, ys))} (for x = 0, 1, 2, 3) are exponential. Explain why a linear model is better.',
                       f'The differences are all {d} (constant), while the ratios {", ".join(rsf(ys[i + 1] / ys[i], 3) for i in range(3))} are not constant.', 'Differences (A1); ratios not constant (R1).', 2)
    if kind == 'extrap':
        return explain(f'A model fitted to {d + 3} weeks of data on the spread of an invasive plant predicts it will cover the whole country within a year. Explain why this prediction may be unreliable.',
                       'It is extrapolation far beyond the data; growth slows when space or resources run out, and small errors in the growth factor are multiplied many times.', 'Extrapolation (R1); real-world limit (R1).', 2)
    ys = [a * d ** i for i in range(4)]
    return explain(f'Explain why the differences of {", ".join(map(str, ys))} are not constant, but the data still follow a simple pattern.',
                   f'Differences {", ".join(str(ys[i + 1] - ys[i]) for i in range(3))} grow, but each term is {d} times the last: a constant ratio, so y = {a} × {d}ˣ.', 'Ratio identified (R1); model (A1).', 2)


@R.add('ch05-st3', 'C4', (3, 5), 'multi_step')
def fit_task(rng, slot):
    city = rng.choice(CITIES)
    kind = rng.choice(['bacteria', 'cooling', 'prices', 'views'])
    a = rng.choice([100, 200, 300, 500])
    b = rng.choice([1.4, 1.6, 1.8, 0.75, 0.85])
    ys = [round(a * b ** i * rng.uniform(0.97, 1.03)) for i in range(6)]
    ratios = [ys[i + 1] / ys[i] for i in range(5)]
    bb = float(rsf(sum(ratios) / 5, 3))
    lab = {'bacteria': ('bacteria count (thousands) in a petri dish', 'hours'), 'cooling': ('temperature above room temperature (°C) of a pie', 'ten-minute intervals'),
           'prices': ('price index of a rare stamp', 'years'), 'views': ('daily views (hundreds) of a video', 'days')}[kind]
    xp = 9
    pred = ys[0] * bb ** xp
    ans = f'(a) ratios {", ".join(rsf(r, 3) for r in ratios)} – roughly constant, so exponential (b) y ≈ {ys[0]} × {g(bb)}ᵗ (c) t = 3: {rsf(ys[0] * bb ** 3, 3)} vs {ys[3]} (residual {rsf(ys[3] - ys[0] * bb ** 3, 2)}) (d) {rsf(pred, 3)}; extrapolation – {"growth must slow" if bb > 1 else "the value levels off / measurement error grows"}'
    q_ = (f'A student in {city} records the {lab[0]} at t = 0 to 5 {lab[1]}: {", ".join(map(str, ys))}. (a) Investigate whether an exponential model is suitable. (b) Find a model y = a × bᵗ using the first value and the mean ratio. '
          f'(c) Compare the model with the data at t = 3. (d) Use the model to predict t = {xp} and comment on its reliability.')
    return short(q_, ans, f'{ans}. Ratios used to justify the model (B: M1 R1); model parameters (A1 A1); residual / prediction and reliability (D: R1 C1).', 6, 'multi_step', 'G5')


# =============================================================================================
# ch06 Logarithms (Extended)
# =============================================================================================
R.facts('ch06-st1', F(
    terms=[('logarithm', 'the number log_b(x), which is the power to which b must be raised to give x: log_b(x) = y ⇔ bʸ = x'),
           ('common logarithm', 'a logarithm with base 10, written log x or lg x'),
           ('natural logarithm', 'a logarithm with base e ≈ 2.718, written ln x')],
    facts=[('What is log₂ 32?', '5', ['16', '6', '1/5'], '2⁵ = 32.'),
           ('Write 10³ = 1000 in logarithmic form.', 'log 1000 = 3', ['log 3 = 1000', 'log₃ 1000 = 10', 'log 10 = 3'], 'log_b(x) = y ⇔ bʸ = x.'),
           ('What is log₅ 1?', '0', ['1', '5', 'undefined'], '5⁰ = 1.'),
           ('What is log₃(1/9)?', '−2', ['2', '1/2', '−1/2'], '3⁻² = 1/9.')],
    why=[('Explain why log_b(b) = 1 for any valid base b.', 'b¹ = b, so the power needed is 1.'),
         ('Explain why log₂(−8) is undefined (for real numbers).', '2ʸ is positive for every real y, so no power of 2 equals −8.'),
         ('Explain why log 500 lies between 2 and 3.', '10² = 100 and 10³ = 1000, and 500 is between them, so the power is between 2 and 3.')],
    misc=[('log₂ 8 = 8/2 = 4.', 'log₂ 8 asks "2 to what power is 8?": 2³ = 8, so the answer is 3.'),
          ('log 0 = 0.', 'log 0 is undefined: no power of 10 equals 0.')],
))

_LOGB = [(2, [1, 2, 3, 4, 5, 6, 7]), (3, [1, 2, 3, 4]), (4, [1, 2, 3]), (5, [1, 2, 3]), (10, [1, 2, 3, 4, 5, 6])]


def _la(v):
    t = fx(v)
    return f'({t})' if '/' in t or t.startswith('−') else t


def _lsub(b):
    return '' if b == 10 else str(b).translate(str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉'))


@R.add('ch06-st1', 'C1', (1, 3), 'mcq')
def log_eval_mcq(rng, slot):
    b, ks = rng.choice(_LOGB)
    k = rng.choice(ks) * rng.choice([1, 1, -1])
    v = Fr(b) ** k
    return mcq(rng, f'Evaluate log{_lsub(b)} {_la(v)}.', m(k), [fx(v / b), m(-k), fx(Fr(1, k))] if abs(k) != 1 else [m(b), m(-k), '0'],
               f'{b}{sup(k)} = {fx(v)}.')


@R.add('ch06-st1', 'C3', (1, 4), 'short')
def log_convert(rng, slot):
    b, ks = rng.choice(_LOGB)
    k = rng.choice(ks) * rng.choice([1, -1])
    v = Fr(b) ** k
    kind = rng.choice(['tolog', 'toexp', 'solve'])
    if kind == 'tolog':
        return short(f'Write {b}{sup(k)} = {fx(v)} in logarithmic form.', f'log{_lsub(b)} {_la(v)} = {m(k)}', f'Base {b}, argument {fx(v)}, value {m(k)} (A1 A1).', 2)
    if kind == 'toexp':
        return short(f'Write log{_lsub(b)} {_la(v)} = {m(k)} in exponential form.', f'{b}{sup(k)} = {fx(v)}', f'b^(value) = argument (A1 A1).', 2)
    which = rng.choice(['arg', 'base'])
    if which == 'arg' or k < 0:
        return short(f'Solve log{_lsub(b)} x = {m(k)}.', f'x = {fx(v)}', f'x = {b}{sup(k)} (M1) = {fx(v)} (A1).', 2)
    return short(f'Solve log_x {fx(v)} = {k}, where x > 0.', f'x = {b}', f'x{sup(k)} = {fx(v)} (M1); x = {b} (A1).', 2)


@R.add('ch06-st1', 'C3', (2, 5), 'short')
def log_between(rng, slot):
    b = rng.choice([2, 3, 10])
    lo = rng.randint(1, 5 if b != 10 else 4)
    v = rng.randint(b ** lo + 1, b ** (lo + 1) - 1)
    val = math.log(v, b)
    return short(f'Without a calculator, state the two consecutive integers between which log{_lsub(b)} {v} lies. Then use a calculator to evaluate it to 3 s.f.', f'{lo} and {lo + 1}; {rsf(val, 3)}',
                 f'{b}{sup(lo)} = {b ** lo} < {v} < {b ** (lo + 1)} = {b}{sup(lo + 1)} (M1 A1); {rsf(val, 3)} (A1).', 3)


@R.add('ch06-st1', 'C2', (2, 4), 'explain')
def log_def_explain(rng, slot):
    who = name(rng)
    b, ks = rng.choice(_LOGB[:4])
    k = rng.choice(ks)
    kind = rng.choice(['divide', 'neg', 'inverse'])
    if kind == 'divide':
        return explain(f'{who} says log{_lsub(b)} {b ** k} = {b ** k}/{b} = {fx(Fr(b ** k, b))}. Explain the mistake and give the correct value.',
                       f'A logarithm is an exponent, not a quotient: {b}{sup(k)} = {b ** k}, so log{_lsub(b)} {b ** k} = {k}.', 'Meaning of log (R1); value (A1).', 2)
    if kind == 'neg':
        return explain(f'Explain why log{_lsub(b)}(1/{b ** k}) is negative.', f'1/{b ** k} = {b}{sup(-k)}: a number between 0 and 1 needs a negative power of {b}, so the log is −{k}.', 'Negative exponent (R1); value (A1).', 2)
    return explain(f'Explain why {b}^(log{_lsub(b)} x) = x for x > 0.', f'log{_lsub(b)} x is the power of {b} that gives x, so raising {b} to that power gives x: the functions are inverses.', 'Definition used (R1); inverse relationship (R1).', 2)


@R.add('ch06-st1', 'C4', (3, 5), 'multi_step')
def log_def_task(rng, slot):
    city = rng.choice(CITIES)
    kind = rng.choice(['table', 'digits', 'inverse', 'memory'])
    if kind == 'table':
        b = rng.choice([2, 3])
        ks = list(range(-2, 5))
        ans = f'(a) ' + ', '.join(f'log{_lsub(b)} {_la(Fr(b) ** k)} = {m(k)}' for k in ks) + f' (b) multiplying x by {b} adds 1 to the log (c) log{_lsub(b)} x < 0 for 0 < x < 1; undefined for x ≤ 0 (d) y = log{_lsub(b)} x is the reflection of y = {b}ˣ in y = x'
        q_ = (f'Investigate y = log{_lsub(b)} x. (a) Complete a table for x = {", ".join(fx(Fr(b) ** k) for k in ks)}. (b) Describe the pattern when x is multiplied by {b}. (c) Describe the sign of log{_lsub(b)} x for different x. '
              f'(d) Describe how the graph is related to y = {b}ˣ.')
    elif kind == 'digits':
        n = rng.choice([2, 3, 7])
        p = rng.choice([20, 30, 50, 64, 100])
        digits = math.floor(p * math.log10(n)) + 1
        ans = f'(a) log 10 = 1, log 100 = 2, log 1000 = 3 (b) a whole number with d digits has d − 1 ≤ log N < d (c) log({n}{sup(p)}) = {p} log {n} ≈ {rsf(p * math.log10(n), 4)} (d) {digits} digits'
        q_ = (f'A computer club in {city} wants to know how many digits {n}{sup(p)} has. (a) Find log 10, log 100 and log 1000. (b) Explain the link between log N and the number of digits of N. '
              f'(c) Find log({n}{sup(p)}) using log Nᵏ = k log N. (d) Hence state the number of digits.')
    elif kind == 'inverse':
        b = rng.choice([2, 3, 5, 10])
        ans = f'(a) f⁻¹(x) = log{_lsub(b)} x (b) domain x > 0, range all real numbers (c) the y-axis (x = 0) is a vertical asymptote of the log graph (d) (1, 0) and ({b}, 1)'
        q_ = (f'f(x) = {b}ˣ. (a) Find f⁻¹(x). (b) State the domain and range of f⁻¹. (c) Explain how the horizontal asymptote of f becomes an asymptote of f⁻¹. (d) Write two points on the graph of f⁻¹.')
    else:
        n = rng.choice([8, 16, 32, 64, 128, 256])
        k = int(math.log2(n))
        ans = f'(a) log₂ {n} = {k} (b) {k} questions (c) {math.ceil(math.log2(1000))} questions for 1000 numbers (d) each yes/no answer halves the possibilities, so the number of questions is log₂ N rounded up'
        q_ = (f'In a guessing game played in {city}, you find a secret number from 1 to N by asking yes/no questions that halve the possibilities. (a) Evaluate log₂ {n}. (b) How many questions are needed for N = {n}? '
              f'(c) How many for N = 1000? (d) Explain why logarithms appear in this problem.')
    return short(q_, ans, f'{ans}. Logarithms evaluated from the definition (A1 A1); pattern / link explained (B: R1 R1); communicated with correct notation (C1).', 5, 'multi_step', 'G5')


R.facts('ch06-st2', F(
    terms=[('product law', 'the rule log_b(MN) = log_b M + log_b N'),
           ('quotient law', 'the rule log_b(M/N) = log_b M − log_b N'),
           ('power law', 'the rule log_b(Mᵏ) = k log_b M'),
           ('change of base', 'the rule log_b x = log x / log b, for evaluating logs with any base on a calculator')],
    facts=[('Simplify log 4 + log 25.', '2', ['log 29', '100', '1'], 'log(4 × 25) = log 100 = 2.'),
           ('Write 3 log₂ x as a single logarithm.', 'log₂(x³)', ['log₂(3x)', '(log₂ x)³', 'log₆ x'], 'Power law.'),
           ('Evaluate log₂ 48 − log₂ 3.', '4', ['log₂ 45', '16', '5'], 'log₂(48/3) = log₂ 16 = 4.')],
    why=[('Explain why log(MN) = log M + log N, using exponent laws.', 'If M = 10ᵃ and N = 10ᵇ then MN = 10^(a + b), so log(MN) = a + b = log M + log N.'),
         ('Explain why log(M + N) is not equal to log M + log N.', 'The product law turns multiplication into addition; there is no law for the log of a sum, e.g. log(10 + 10) = log 20 ≈ 1.30 but log 10 + log 10 = 2.'),
         ('Explain why log_b(1/x) = −log_b x.', 'log_b(1/x) = log_b 1 − log_b x = 0 − log_b x.')],
    misc=[('log 8 / log 2 = log 4.', 'log 8 / log 2 = 3 (change of base: log₂ 8); log 4 ≈ 0.602.'),
          ('(log x)² = 2 log x.', 'The power law applies to log(x²), not to the square of the log.')],
))


@R.add('ch06-st2', 'C1', (1, 3), 'mcq')
def log_law_mcq(rng, slot):
    b = rng.choice([2, 3, 5, 10])
    p, q = rng.randint(2, 9), rng.randint(2, 9)
    kind = rng.choice(['prod', 'quot', 'pow'])
    if kind == 'prod':
        return mcq(rng, f'Write log{_lsub(b)} {p} + log{_lsub(b)} {q} as a single logarithm.', f'log{_lsub(b)} {p * q}', [f'log{_lsub(b)} {p + q}', f'log{_lsub(b)}{_lsub(2 * b)} {p * q}'.replace(f'log{_lsub(b)}{_lsub(2 * b)}', f'log{_lsub(2 * b)}'), f'(log{_lsub(b)} {p})(log{_lsub(b)} {q})'], 'Product law.')
    if kind == 'quot':
        return mcq(rng, f'Write log{_lsub(b)} {p * q} − log{_lsub(b)} {q} as a single logarithm.', f'log{_lsub(b)} {p}', [f'log{_lsub(b)} {p * q - q}', f'log{_lsub(b)} {p * q} / log{_lsub(b)} {q}', f'log{_lsub(b)} {p * q * q}'], 'Quotient law.')
    return mcq(rng, f'Write {q} log{_lsub(b)} {p} as a single logarithm.', f'log{_lsub(b)} {p ** q}', [f'log{_lsub(b)} {p * q}', f'(log{_lsub(b)} {p}){sup(q)}', f'log{_lsub(b)} {q ** p}'], 'Power law.')


@R.add('ch06-st2', 'C3', (1, 4), 'short')
def log_law_eval(rng, slot):
    b = rng.choice([2, 3, 10])
    tgt = rng.randint(1, 4 if b != 10 else 3)
    T = b ** tgt
    divs = [d for d in range(2, T) if T % d == 0 and d != T // d] if T > 3 else []
    if rng.random() < 0.5 and divs:
        d = rng.choice(divs)
        return short(f'Without a calculator, evaluate log{_lsub(b)} {d} + log{_lsub(b)} {T // d}.', str(tgt), f'log{_lsub(b)}({d} × {T // d}) = log{_lsub(b)} {T} (M1) = {tgt} (A1).', 2)
    k = rng.randint(2, 9)
    return short(f'Without a calculator, evaluate log{_lsub(b)} {T * k} − log{_lsub(b)} {k}.', str(tgt), f'log{_lsub(b)}({T * k}/{k}) = log{_lsub(b)} {T} (M1) = {tgt} (A1).', 2)


@R.add('ch06-st2', 'C3', (2, 5), 'short')
def log_law_combine(rng, slot):
    b = rng.choice([2, 3, 5, 10])
    p, q, r = rng.randint(2, 4), rng.randint(1, 3), rng.randint(1, 3)
    if rng.random() < 0.5:
        return short(f'Write {p} log{_lsub(b)} x + {str(q) + " " if q > 1 else ""}log{_lsub(b)} y − {str(r) + " " if r > 1 else ""}log{_lsub(b)} z as a single logarithm.', f'log{_lsub(b)}(x{sup(p)}y{sup(q) if q > 1 else ""}/z{sup(r) if r > 1 else ""})',
                     'Power law on each term (M1); product and quotient laws (M1); single log (A1).', 3)
    c = rng.choice([2, 3, 5, 6, 7, 11])
    v = math.log(c) / math.log(b if b != 10 else 10)
    t = rng.choice([7, 9, 13, 20, 50])
    return short(f'Use the change-of-base rule to evaluate log{_lsub(b) if b != 10 else "₁₀"} {t} and log₇ {c * 7}, each to 3 significant figures.',
                 f'{rsf(math.log(t) / math.log(b), 3)}; {rsf(math.log(c * 7) / math.log(7), 3)}',
                 f'log {t}/log {b} (M1) = {rsf(math.log(t) / math.log(b), 3)} (A1); log {c * 7}/log 7 = {rsf(math.log(c * 7) / math.log(7), 3)} (A1).', 3)


@R.add('ch06-st2', 'C2', (2, 4), 'explain')
def log_law_explain(rng, slot):
    who = name(rng)
    a, b = rng.randint(2, 9), rng.randint(2, 9)
    kind = rng.choice(['sum', 'square', 'divide'])
    if kind == 'sum':
        return explain(f'{who} writes log {a} + log {b} = log {a + b}. Explain the error and give the correct single logarithm.',
                       f'The product law gives log {a} + log {b} = log({a} × {b}) = log {a * b}; logs turn products into sums, not sums into sums.', 'Law stated (R1); log ' + str(a * b) + ' (A1).', 2)
    if kind == 'square':
        return explain(f'{who} says (log {a})² = 2 log {a}. Use a calculator value to show this is false, and explain which expression equals 2 log {a}.',
                       f'(log {a})² ≈ {rsf(math.log10(a) ** 2, 3)} but 2 log {a} ≈ {rsf(2 * math.log10(a), 3)}; 2 log {a} = log({a}²) = log {a * a}.', 'Numerical check (A1); correct law (R1).', 2)
    return explain(f'{who} writes log {a * b} ÷ log {b} = log {a}. Explain why this is wrong.',
                   f'Division of logs is not a log law; log({a * b}/{b}) = log {a * b} − log {b} = log {a}. log {a * b} ÷ log {b} ≈ {rsf(math.log10(a * b) / math.log10(b), 3)} is log{_lsub(b)} {a * b}.', 'Correct law (R1); value check (A1).', 2)


@R.add('ch06-st2', 'C4', (3, 5), 'multi_step')
def log_law_task(rng, slot):
    city = rng.choice(CITIES)
    kind = rng.choice(['prove', 'slide', 'pattern', 'base'])
    if kind == 'prove':
        b = rng.choice([2, 3, 10])
        ans = f'(a) M = {b}ᵖ, N = {b}^q (b) MN = {b}^(p + q) so log{_lsub(b)}(MN) = p + q (c) M/N = {b}^(p − q) (d) e.g. M = {b ** 3}, N = {b}: log{_lsub(b)} {b ** 4} = 4 = 3 + 1'
        q_ = (f'Prove the logarithm laws for base {b}. (a) Let log{_lsub(b)} M = p and log{_lsub(b)} N = q; write M and N as powers of {b}. (b) Prove the product law. (c) Prove the quotient law. '
              f'(d) Check the product law with a numerical example.')
    elif kind == 'slide':
        a, b = rng.randint(2, 9), rng.randint(2, 9)
        ans = f'(a) log {a} ≈ {rsf(math.log10(a), 3)}, log {b} ≈ {rsf(math.log10(b), 3)} (b) sum ≈ {rsf(math.log10(a) + math.log10(b), 3)} = log {a * b} (c) multiplication becomes addition of lengths proportional to logs (d) subtract lengths: log({a * b}) − log({b}) = log {a}'
        q_ = (f'Before calculators, engineers in {city} multiplied with slide rules, which add lengths proportional to logarithms. (a) Find log {a} and log {b}. (b) Add them and show the result is log {a * b}. '
              f'(c) Explain how a slide rule multiplies. (d) Explain how it could divide {a * b} by {b}.')
    elif kind == 'pattern':
        b = rng.choice([2, 3])
        ks = [1, 2, 3, 4]
        ans = f'(a) {", ".join(f"log{_lsub(b)} {b ** k} = {k}" for k in ks)} (b) the logs go up by 1 as the numbers multiply by {b} (c) log{_lsub(b)}({b}ⁿ) = n log{_lsub(b)} {b} = n (power law) (d) log{_lsub(b)} {b ** 10} = 10'
        q_ = (f'Investigate log{_lsub(b)} of powers of {b}. (a) Evaluate log{_lsub(b)} {", ".join(str(b ** k) for k in ks)}. (b) Describe the pattern. (c) Prove it with the power law. (d) Use it to write down log{_lsub(b)} {b ** 10}.')
    else:
        v = rng.choice([20, 50, 80, 200])
        ans = f'(a) log₂ {v} = log {v}/log 2 ≈ {rsf(math.log2(v), 3)} (b) 2^{rsf(math.log2(v), 3)} ≈ {rsf(2 ** float(rsf(math.log2(v), 3)), 3)} ≈ {v} (c) ln {v}/ln 2 gives the same value (d) log_b x = log_c x / log_c b for any base c'
        q_ = (f'A calculator in {city} only has log (base 10) and ln. (a) Use change of base to find log₂ {v}. (b) Check your answer by raising 2 to that power. (c) Show that using ln gives the same value. (d) State the change-of-base rule in general.')
    return short(q_, ans, f'{ans}. Laws stated and applied (A1 M1); proof / verification (B: R1 A1); communication with correct notation (C1).', 5, 'multi_step', 'G5')


R.facts('ch06-st3', F(
    terms=[('solving with logarithms', 'taking logarithms of both sides to bring the unknown down from an exponent: aˣ = b ⇒ x = log b / log a'),
           ('logarithmic equation', 'an equation with the unknown inside a logarithm, solved by converting to exponential form'),
           ('extraneous solution', 'a value found algebraically that does not satisfy the original equation (e.g. makes a log argument ≤ 0)')],
    facts=[('Solve 2ˣ = 10 (to 3 s.f.).', 'x = 3.32', ['x = 5', 'x = 0.301', 'x = 20'], 'x = log 10 / log 2.'),
           ('Solve log₃ x = 4.', 'x = 81', ['x = 12', 'x = 64', 'x = 4/3'], 'x = 3⁴.'),
           ('Taking logs of 5ˣ = 30 gives:', 'x log 5 = log 30', ['log 5x = 30', 'x = log 30 − log 5', '5 log x = log 30'], 'Power law.')],
    why=[('Explain why logarithms are needed to solve 3ˣ = 20 but not 3ˣ = 27.', '27 = 3³ has a common base, but 20 is not a whole-number power of 3, so x must be found with x = log 20/log 3.'),
         ('Explain why you must check solutions of logarithmic equations.', 'log is only defined for positive arguments; a solution that makes an argument zero or negative must be rejected.'),
         ('Explain why taking logarithms of both sides keeps an equation balanced.', 'log is a function, so equal inputs give equal outputs.')],
    misc=[('log(2x) = 2 log x.', 'log(2x) = log 2 + log x; 2 log x = log(x²).'),
          ('If 4ˣ = 9, then x = 9/4.', 'x = log 9 / log 4 ≈ 1.58.')],
))


@R.add('ch06-st3', 'C1', (1, 3), 'mcq')
def solve_log_mcq(rng, slot):
    b = rng.choice([2, 3, 5, 1.5, 4])
    c = rng.choice([7, 10, 15, 20, 40, 100])
    v = math.log(c) / math.log(b)
    return mcq(rng, f'Solve {g(b)}ˣ = {c}, to 3 s.f.', f'x = {rsf(v, 3)}', [f'x = {rsf(c / b, 3)}', f'x = {rsf(math.log10(c / b), 3)}', f'x = {rsf(math.log10(c) * b, 3)}'],
               f'x = log {c}/log {g(b)} = {rsf(v, 3)}.')


@R.add('ch06-st3', 'C3', (1, 4), 'short')
def solve_exp_log(rng, slot):
    b = rng.choice([2, 3, 5, 1.2, 1.05, 0.8])
    a = rng.choice([1, 2, 3, 5, 100])
    c = rng.randint(2, 9)
    k = rng.randint(-3, 3)
    rhs = a * rng.choice([7, 12, 20, 35, 50]) if b > 1 else a * Fr(rng.randint(1, 9), 10)
    rhs = float(rhs)
    v = (math.log(rhs / a) / math.log(b) - k) / c if c else 0
    lhs = f'{a} × ' if a != 1 else ''
    return short(f'Solve {lhs}{g(b)}^({lin(c, k)}) = {g(rhs)}, giving x to 3 s.f.', f'x = {rsf(v, 3)}',
                 f'{g(b)}^({lin(c, k)}) = {g(rhs / a, 4)} (A1); ({lin(c, k)}) log {g(b)} = log {g(rhs / a, 4)} (M1); x = {rsf(v, 3)} (A1).', 3)


@R.add('ch06-st3', 'C3', (2, 5), 'short')
def solve_log_eq(rng, slot):
    b = rng.choice([2, 3, 10])
    kind = rng.choice(['simple', 'sum', 'diff'])
    if kind == 'simple':
        a, c = rng.randint(1, 5), rng.randint(-5, 5)
        k = rng.randint(1, 4 if b != 10 else 2)
        xs = Fr(b ** k - c, a)
        return short(f'Solve log{_lsub(b)}({lin(a, c)}) = {k}.', f'x = {fx(xs)}', f'{lin(a, c)} = {b}{sup(k)} = {b ** k} (M1 A1); x = {fx(xs)} (A1).', 3)
    if kind == 'sum':
        # log(x) + log(x + d) = k → x(x + d) = b^k ; choose root
        r = rng.randint(1, 9)
        d = rng.randint(1, 6)
        T = r * (r + d)
        k = None
        for kk in range(1, 10):
            if b ** kk == T:
                k = kk
        if k is None:
            return short(f'Solve log{_lsub(b)} x + log{_lsub(b)}(x + {d}) = log{_lsub(b)} {T}.', f'x = {r} (x = −{r + d} rejected)',
                         f'x(x + {d}) = {T} (M1); (x − {r})(x + {r + d}) = 0 (A1); x = {r}, reject −{r + d} since log of a negative is undefined (R1).', 3)
        return short(f'Solve log{_lsub(b)} x + log{_lsub(b)}(x + {d}) = {k}.', f'x = {r}', f'x(x + {d}) = {T} (M1); x = {r} (A1); negative root rejected (R1).', 3)
    k = rng.randint(1, 3 if b != 10 else 1)
    a = rng.randint(2, 9)
    # log(ax) − log(x − 1) = k → ax = b^k (x − 1) → x = b^k/(b^k − a)
    B = b ** k
    if B == a:
        return None
    xs = Fr(B, B - a)
    valid = xs > 1
    return short(f'Solve log{_lsub(b)}({a}x) − log{_lsub(b)}(x − 1) = {k}.', f'x = {fx(xs)}' if valid else 'no solution',
                 f'{a}x/(x − 1) = {B} (M1); {a}x = {B}x − {B} → x = {fx(xs)} (A1); {"valid since x > 1" if valid else "rejected: x − 1 ≤ 0, so no solution"} (R1).', 3)


@R.add('ch06-st3', 'C2', (2, 4), 'explain')
def solve_log_explain(rng, slot):
    who = name(rng)
    b, c = rng.choice([2, 3, 4, 5, 6]), rng.choice([10, 20, 30, 45, 50])
    kind = rng.choice(['divide', 'check', 'why'])
    if kind == 'divide':
        return explain(f'{who} solves {b}ˣ = {c} by writing x = {c}/{b}. Explain the error and give the correct solution to 3 s.f.',
                       f'{b}ˣ is not {b} × x. Take logs: x log {b} = log {c}, so x = log {c}/log {b} ≈ {rsf(math.log(c) / math.log(b), 3)}.', 'Error identified (R1); solution (A1).', 2)
    if kind == 'check':
        return explain(f'{who} solves log x + log(x − 3) = 1 and gets x = 5 or x = −2. Explain which solution(s) to keep.',
                       'x = 5: log 5 + log 2 = log 10 = 1 ✓. x = −2 gives log(−2), which is undefined, so it is rejected.', 'Check each (R1); conclusion (A1).', 2)
    return explain(f'Explain why the equation {b}ˣ = −{c} cannot be solved by taking logarithms.',
                   f'{b}ˣ > 0 for all x, so there is no solution; log(−{c}) is undefined, which is why the method fails.', 'Positivity (R1); log of negative (R1).', 2)


@R.add('ch06-st3', 'C4', (3, 5), 'multi_step')
def solve_log_task(rng, slot):
    city, country, cur, cname = place(rng)
    kind = rng.choice(['savings', 'cooling', 'pop', 'drug'])
    if kind == 'savings':
        P = rng.choice([2000, 5000, 8000])
        r = rng.choice([3, 4, 5, 6])
        T = rng.choice([1.5, 2, 3])
        t = math.log(T) / math.log(1 + r / 100)
        ans = f'(a) {money(cur, P, 0)} × {g(1 + r / 100)}ᵗ = {money(cur, P * T, 0)} (b) t = log {g(T)}/log {g(1 + r / 100)} ≈ {rsf(t, 3)} (c) {math.ceil(t)} whole years (d) the time does not depend on P'
        q_ = (f'{name(rng)} invests {money(cur, P, 0)} in {city} at {r}% per year compound interest. (a) Write an equation for when the investment reaches {money(cur, P * T, 0)}. (b) Solve it using logarithms. '
              f'(c) State the number of whole years needed. (d) Explain why the answer is the same for any starting amount.')
    elif kind == 'cooling':
        room, T0, k = rng.choice([20, 22]), rng.choice([90, 95]), rng.choice([0.92, 0.9, 0.88])
        tgt = rng.choice([40, 50, 60])
        t = math.log((tgt - room) / (T0 - room)) / math.log(k)
        ans = f'(a) {T0 - room} × {g(k)}ᵗ = {tgt - room} (b) {g(k)}ᵗ = {g((tgt - room) / (T0 - room), 4)} (c) t ≈ {rsf(t, 3)} minutes (d) never: {g(k)}ᵗ > 0 so T > {room}'
        q_ = (f'Soup in a kitchen in {city} cools as T = {room} + {T0 - room} × {g(k)}ᵗ °C. (a) Write an equation for when T = {tgt}. (b) Rearrange to isolate the exponential. (c) Solve using logarithms. '
              f'(d) Explain whether the soup ever reaches {room} °C.')
    elif kind == 'pop':
        A0, ra = rng.choice([(50000, 3), (80000, 2.5)])
        B0, rb = rng.choice([(120000, 0.5), (100000, 1)])
        t = math.log(B0 / A0) / math.log((1 + ra / 100) / (1 + rb / 100))
        ans = f'(a) A = {big(A0)} × {g(1 + ra / 100)}ᵗ, B = {big(B0)} × {g(1 + rb / 100)}ᵗ (b) ({g(1 + ra / 100)}/{g(1 + rb / 100)})ᵗ = {g(B0 / A0, 4)} (c) t ≈ {rsf(t, 3)} years (d) assumes constant rates'
        q_ = (f'Town A near {city} has {big(A0)} people growing at {g(ra)}% a year; town B has {big(B0)} growing at {g(rb)}% a year. (a) Write models for both. (b) Form an equation for when they are equal. '
              f'(c) Solve it with logarithms. (d) State one assumption.')
    else:
        D, h = rng.choice([(400, 6), (500, 4), (250, 3)])
        lim = rng.choice([50, 80, 100])
        t = h * math.log(lim / D) / math.log(0.5)
        ans = f'(a) {D}(1/2)^(t/{h}) = {lim} (b) t = {h} × log({fx(Fr(lim, D))})/log(1/2) (c) ≈ {rsf(t, 3)} hours (d) each half-life halves the amount, so log base 2 counts half-lives: {rsf(t / h, 3)} half-lives'
        q_ = (f'A patient in {city} receives {D} mg of a medicine with a half-life of {h} hours. (a) Write an equation for when {lim} mg remains. (b) Rearrange it using logarithms. (c) Solve for t. '
              f'(d) Interpret the number of half-lives.')
    return short(q_, ans, f'{ans}. Equation formed (M1 A1); logarithms used correctly (M1 A1); interpreted in context (D: R1 C1).', 6, 'multi_step', 'G5')


R.facts('ch06-st4', F(
    terms=[('logarithmic scale', 'a scale in which each step represents multiplication by a fixed factor (usually 10)'),
           ('pH', 'pH = −log[H⁺], where [H⁺] is the hydrogen-ion concentration in mol/L'),
           ('decibel level', 'L = 10 log(I/I₀) dB, where I₀ = 10⁻¹² W/m² is the threshold of hearing'),
           ('Richter magnitude', 'M = log(A/A₀); each increase of 1 means 10 times the amplitude of the seismic wave')],
    facts=[('A solution has [H⁺] = 10⁻⁴ mol/L. Its pH is:', '4', ['−4', '10⁴', '0.0001'], 'pH = −log 10⁻⁴ = 4.'),
           ('An earthquake of magnitude 6 has an amplitude how many times that of magnitude 4?', '100', ['2', '20', '1.5'], '10^(6 − 4).'),
           ('An increase of 10 dB means the intensity is multiplied by:', '10', ['2', '100', '1.1'], 'L = 10 log(I/I₀).')],
    why=[('Explain why logarithmic scales are used for earthquakes and sound.', 'The quantities range over many powers of ten; a log scale turns this into a manageable range of numbers.'),
         ('Explain why a pH drop of 1 means the solution is 10 times more acidic.', 'pH = −log[H⁺], so lowering pH by 1 multiplies [H⁺] by 10.'),
         ('Explain why doubling the intensity of a sound adds about 3 dB.', '10 log 2 ≈ 3.01, so the level increases by about 3 dB.')],
    misc=[('A magnitude 8 earthquake is twice as strong as a magnitude 4.', 'The amplitude is 10⁴ = 10 000 times as large.'),
          ('pH 3 is less acidic than pH 5 because 3 is smaller.', 'Lower pH means higher [H⁺]: pH 3 is 100 times more acidic.')],
))


@R.add('ch06-st4', 'C1', (1, 3), 'mcq')
def logscale_mcq(rng, slot):
    a, b = sorted(rng.sample(range(2, 9), 2))
    kind = rng.choice(['richter', 'ph'])
    if kind == 'richter':
        return mcq(rng, f'How many times larger is the amplitude of a magnitude {b} earthquake than a magnitude {a} earthquake?', big(10 ** (b - a)),
                   [str(b - a), f'{fx(Fr(b, a))}', big(10 ** (b - a + 1))], f'10^({b} − {a}).')
    return mcq(rng, f'How many times greater is [H⁺] in a solution with pH {a} than in one with pH {b}?', big(10 ** (b - a)),
               [str(b - a), big(10 ** (b - a - 1)) if b - a > 1 else '1/10', f'{fx(Fr(b, a))}'], f'10^({b} − {a}).')


@R.add('ch06-st4', 'C3', (1, 4), 'short')
def ph_calc(rng, slot):
    city = rng.choice(CITIES)
    kind = rng.choice(['toph', 'toH'])
    sub = rng.choice(['lemon juice', 'tap water', 'sea water', 'coffee', 'rain water', 'a cleaning product', 'tomato juice'])
    if kind == 'toph':
        mant = rng.choice([1.5, 2, 3.2, 4, 5, 6.3, 7.9])
        e = rng.randint(2, 12)
        H = mant * 10 ** (-e)
        return short(f'A sample of {sub} tested in {city} has [H⁺] = {g(mant)} × 10{sup(-e)} mol/L. Find its pH to 2 d.p.', str(rnd(-math.log10(H), 2)),
                     f'pH = −log({g(mant)} × 10{sup(-e)}) (M1) = {rnd(-math.log10(H), 2)} (A1).', 2)
    pH = round(rng.uniform(1.5, 12.5), 1)
    H = 10 ** (-pH)
    return short(f'A sample of {sub} in {city} has pH {g(pH)}. Find [H⁺] in mol/L, in standard form to 3 s.f.', f'{rsf(H / 10 ** math.floor(math.log10(H)), 3)} × 10{sup(math.floor(math.log10(H)))} mol/L',
                 f'[H⁺] = 10^(−{g(pH)}) (M1 A1).', 2)


@R.add('ch06-st4', 'C3', (2, 5), 'short')
def db_richter_calc(rng, slot):
    city = rng.choice(CITIES)
    kind = rng.choice(['db', 'dbratio', 'richter'])
    if kind == 'db':
        mant, e = rng.choice([1, 2, 3, 5, 8]), rng.randint(-9, -2)
        I = mant * 10.0 ** e
        L = 10 * math.log10(I / 1e-12)
        src = rng.choice(['a busy street', 'a school canteen', 'a train platform', 'a concert', 'a library'])
        return short(f'The sound intensity at {src} in {city} is {mant} × 10{sup(e)} W/m². Using L = 10 log(I/10⁻¹²), find the sound level in dB to 3 s.f.', f'{rsf(L, 3)} dB',
                     f'I/I₀ = {mant} × 10{sup(e + 12)} (M1); L = 10 log({mant} × 10{sup(e + 12)}) (A1) = {rsf(L, 3)} dB (A1).', 3)
    if kind == 'dbratio':
        d = rng.choice([3, 6, 10, 15, 20, 25, 30])
        return short(f'A concert in {city} is {d} dB louder than the street outside. How many times greater is its sound intensity?', f'{rsf(10 ** (d / 10), 3)} times',
                     f'ΔL = 10 log(I₂/I₁) (M1); I₂/I₁ = 10^({d}/10) (A1) = {rsf(10 ** (d / 10), 3)} (A1).', 3)
    M1, M2 = round(rng.uniform(3, 6), 1), round(rng.uniform(6.1, 9), 1)
    return short(f'Two earthquakes near {city} had magnitudes {g(M1)} and {g(M2)}. How many times larger was the amplitude of the stronger one?', f'{rsf(10 ** (M2 - M1), 3)} times',
                 f'10^({g(M2)} − {g(M1)}) (M1) = 10^{g(round(M2 - M1, 1))} (A1) ≈ {rsf(10 ** (M2 - M1), 3)} (A1).', 3)


@R.add('ch06-st4', 'C2', (2, 4), 'explain')
def logscale_explain(rng, slot):
    who = name(rng)
    a = rng.randint(3, 6)
    d = rng.randint(1, 3)
    kind = rng.choice(['richter', 'ph', 'db'])
    if kind == 'richter':
        return explain(f'{who} says a magnitude {a + d} earthquake is only "a bit stronger" than a magnitude {a}. Explain why this is misleading.',
                       f'The Richter scale is logarithmic: a difference of {d} means 10{sup(d)} = {10 ** d} times the amplitude.', 'Log scale (R1); factor (A1).', 2)
    if kind == 'ph':
        return explain(f'Explain why changing the pH of a pool from {a + d} to {a} is a large change in acidity.',
                       f'pH = −log[H⁺]; a fall of {d} multiplies [H⁺] by 10{sup(d)} = {10 ** d}.', 'Inverse log relationship (R1); factor (A1).', 2)
    return explain(f'Explain why two identical speakers together are about 3 dB louder than one, not twice as many decibels.',
                   'The intensity doubles; ΔL = 10 log 2 ≈ 3 dB, because the decibel scale is logarithmic.', 'Intensity doubles (R1); 10 log 2 (A1).', 2)


@R.add('ch06-st4', 'C4', (3, 5), 'multi_step')
def logscale_task(rng, slot):
    city = rng.choice(CITIES)
    kind = rng.choice(['quake', 'noise', 'acid', 'stars'])
    if kind == 'quake':
        M1, M2 = round(rng.uniform(4, 5.5), 1), round(rng.uniform(6, 8), 1)
        ans = f'(a) {rsf(10 ** (M2 - M1), 3)} times the amplitude (b) energy ratio ≈ 10^(1.5 × {g(round(M2 - M1, 1))}) ≈ {rsf(10 ** (1.5 * (M2 - M1)), 3)} (c) M = {g(M1)} + log 2 ≈ {rsf(M1 + math.log10(2), 3)} (d) a linear scale would need numbers from 1 to about 10⁹'
        q_ = (f'Seismologists in {city} recorded a magnitude {g(M1)} earthquake and later a magnitude {g(M2)} one. (a) Compare their amplitudes. (b) Energy grows as 10^(1.5M); compare their energies. '
              f'(c) Find the magnitude of a quake with twice the amplitude of the first. (d) Explain why a logarithmic scale is used.')
    elif kind == 'noise':
        L1 = rng.choice([70, 75, 80, 85])
        lim = 85
        n = rng.choice([2, 4, 10])
        ans = f'(a) I = 10^({L1}/10) × 10⁻¹² = {rsf(10 ** (L1 / 10 - 12), 3)} W/m² (b) {n} machines: L = {L1} + 10 log {n} ≈ {rsf(L1 + 10 * math.log10(n), 3)} dB (c) {"above" if L1 + 10 * math.log10(n) > lim else "within"} the {lim} dB limit (d) the most machines allowed: {int(10 ** ((lim - L1) / 10))}'
        q_ = (f'A machine in a factory in {city} produces {L1} dB. (a) Find its intensity using L = 10 log(I/10⁻¹²). (b) Find the level when {n} identical machines run together. '
              f'(c) Compare with a safety limit of {lim} dB. (d) Find the largest number of machines that can run together within the limit.')
    elif kind == 'acid':
        p1, p2 = round(rng.uniform(5.4, 6.0), 1), round(rng.uniform(4.0, 5.0), 1)
        ans = f'(a) [H⁺] = {rsf(10 ** (-p1), 3)} and {rsf(10 ** (-p2), 3)} mol/L (b) {rsf(10 ** (p1 - p2), 3)} times more acidic (c) pH {rsf(p2 + math.log10(2), 3)} after halving [H⁺] (d) pH differences hide large changes in concentration'
        q_ = (f'Normal rain near {city} has pH {g(p1)}; acid rain measured there has pH {g(p2)}. (a) Find [H⁺] for each. (b) How many times more acidic is the acid rain? '
              f'(c) If treatment halves [H⁺] of the acid rain, find the new pH. (d) Explain why reporting only pH may hide the size of the change.')
    else:
        m1, m2 = rng.randint(1, 3), rng.randint(5, 7)
        ans = f'(a) brightness ratio 100^({m2 - m1}/5) = {rsf(100 ** ((m2 - m1) / 5), 3)} (b) the star with magnitude {m1} is brighter (lower = brighter) (c) each magnitude step is 100^(1/5) ≈ 2.51 times (d) a log scale compresses the huge range of brightness'
        q_ = (f'Astronomers in {city} use magnitudes: a difference of 5 magnitudes means a brightness ratio of 100. (a) Compare a magnitude {m1} star with a magnitude {m2} star. (b) Which is brighter? '
              f'(c) Find the brightness ratio for a difference of 1 magnitude. (d) Explain why such a scale is useful.')
    return short(q_, ans, f'{ans}. Log formula applied (M1 A1); ratios / values computed (A1 A1); interpretation of the logarithmic scale (D: R1 C1).', 6, 'multi_step', 'G5')



SEA = ['Lisbon', 'Cape Town', 'Singapore', 'Mumbai', 'Melbourne', 'Dubai', 'Oslo', 'Lima', 'Accra', 'Sydney', 'Valparaíso', 'Halifax', 'Auckland', 'Mombasa', 'Busan']


# =============================================================================================
# ch07 Transformations of Functions (Extended)
# =============================================================================================
_BASEF = [('x²', lambda t: t * t), ('|x|', abs), ('√x', None), ('x³', lambda t: t ** 3), ('1/x', None), ('2ˣ', lambda t: Fr(2) ** t)]


def _shift_txt(base, h, k):
    """Text of y = f(x − h) + k for a named base function written in x."""
    inner = f'x{sgn(-h)}' if h else 'x'
    if base == 'x²':
        core = f'({inner})²' if h else 'x²'
    elif base == 'x³':
        core = f'({inner})³' if h else 'x³'
    elif base == '|x|':
        core = f'|{inner}|'
    elif base == '√x':
        core = f'√({inner})' if h else '√x'
    elif base == '1/x':
        core = f'1/({inner})' if h else '1/x'
    else:
        core = f'2^({inner})' if h else '2ˣ'
    return core + (sgn(k) if k else '')


R.facts('ch07-st1', F(
    terms=[('translation of a graph', 'a transformation that moves every point of a graph the same distance in the same direction without changing its shape'),
           ('vertical translation', 'the transformation y = f(x) + k, which moves the graph k units up (down if k < 0)'),
           ('horizontal translation', 'the transformation y = f(x − h), which moves the graph h units to the right (left if h < 0)'),
           ('translation vector', 'a column vector (h over k) describing a move h right and k up')],
    facts=[('The graph of y = f(x − 3) is the graph of y = f(x) moved:', '3 units right', ['3 units left', '3 units up', '3 units down'], 'Replacing x with x − 3 shifts right.'),
           ('The vertex of y = x² is (0, 0). The vertex of y = (x + 2)² − 5 is:', '(−2, −5)', ['(2, −5)', '(−2, 5)', '(2, 5)'], 'Translation by (−2 over −5).'),
           ('y = f(x) + 4 is a translation by the vector:', '(0 over 4)', ['(4 over 0)', '(−4 over 0)', '(0 over −4)'], '4 units up.')],
    why=[('Explain why y = f(x − 2) moves the graph to the right, not to the left.', 'To get the same output as f(a), the new function needs x − 2 = a, i.e. x = a + 2: every point moves 2 units right.'),
         ('Explain why a translation does not change the shape of a graph.', 'Every point moves by the same vector, so distances and angles between points stay the same.'),
         ('Explain how a translation affects the asymptotes of y = 1/x.', 'The asymptotes move with the graph: y = 1/(x − h) + k has asymptotes x = h and y = k.')],
    misc=[('y = (x + 4)² is y = x² moved 4 units right.', 'x + 4 = x − (−4), so the graph moves 4 units left.'),
          ('y = f(x) − 3 moves the graph 3 units left.', 'Subtracting outside the function moves it 3 units down.')],
))


@R.add('ch07-st1', 'C1', (1, 3), 'mcq')
def translate_mcq(rng, slot):
    base = rng.choice(['x²', '|x|', 'x³', '√x'])
    h, k = rng.choice([v for v in range(-6, 7) if v]), rng.choice([v for v in range(-6, 7) if v])
    corr = f'({m(h)} over {m(k)})'
    return mcq(rng, f'Which translation vector maps y = {base} onto y = {_shift_txt(base, h, k)}?', corr,
               [f'({m(-h)} over {m(k)})', f'({m(k)} over {m(h)})', f'({m(h)} over {m(-k)})'], f'f(x − h) + k with h = {m(h)}, k = {m(k)}.')


@R.add('ch07-st1', 'C3', (1, 4), 'short')
def translate_point(rng, slot):
    base = rng.choice(['x²', '|x|', 'x³', '√x', '1/x', '2ˣ'])
    h, k = rng.randint(-6, 6), rng.randint(-6, 6)
    if h == 0 and k == 0:
        return None
    key = {'x²': ('vertex', (0, 0)), '|x|': ('vertex', (0, 0)), 'x³': ('point of inflection', (0, 0)), '√x': ('end point', (0, 0)), '2ˣ': ('y-intercept', (0, 1)), '1/x': ('centre of symmetry (where the asymptotes meet)', (0, 0))}[base]
    p = (key[1][0] + h, key[1][1] + k)
    extra = ''
    if base == '1/x':
        extra = f'; asymptotes x = {m(h)}, y = {m(k)}'
    if base == '2ˣ':
        extra = f'; asymptote y = {m(k)}'
    return short(f'The graph of y = {base} is translated to give y = {_shift_txt(base, h, k)}. Describe the translation and find the image of the {key[0]} {ptxt(key[1])}{" and the asymptotes" if base in ("1/x", "2ˣ") else ""}.',
                 f'translation ({m(h)} over {m(k)}); {ptxt(p)}{extra}', f'Vector (A1); image point {ptxt(p)} (A1){"; asymptotes (A1)" if extra else ""}.', 3 if extra else 2)


@R.add('ch07-st1', 'C3', (2, 5), 'short')
def translate_equation(rng, slot):
    a, b, c = 1, rng.randint(-6, 6), rng.randint(-8, 8)
    h, k = rng.choice([v for v in range(-5, 6) if v]), rng.randint(-6, 6)
    f = x ** 2 + b * x + c
    gx = sp.expand(f.subs(x, x - h) + k)
    return short(f'f(x) = {sx(f)}. The graph is translated by ({m(h)} over {m(k)}). Find the equation of the image in the form y = ax² + bx + c.', f'y = {sx(gx)}',
                 f'y = f(x{sgn(-h)}){sgn(k) if k else ""} (M1); substitute (x{sgn(-h)}) (A1); expanded {sx(gx)} (A1).', 3)


@R.add('ch07-st1', 'C2', (2, 4), 'explain')
def translate_explain(rng, slot):
    who = name(rng)
    h = rng.randint(2, 7)
    kind = rng.choice(['dir', 'order', 'domain'])
    if kind == 'dir':
        return explain(f'{who} says y = (x − {h})² is y = x² moved {h} units left. Explain the mistake using a point on the graph.',
                       f'y = (x − {h})² has its vertex where x − {h} = 0, i.e. at x = {h}: the vertex (0, 0) moves to ({h}, 0), {h} units right.', 'Point checked (A1); direction explained (R1).', 2)
    if kind == 'order':
        return explain(f'Explain why translating y = f(x) up {h} units and then right {h} units gives the same graph as doing it the other way round.',
                       f'Both give y = f(x − {h}) + {h}: a vertical and a horizontal translation act on different coordinates, so they commute.', 'Equation in both orders (A1); reason (R1).', 2)
    return explain(f'Explain how the domain of y = √(x − {h}) compares with the domain of y = √x.',
                   f'y = √x has domain x ≥ 0; the translation {h} units right gives x ≥ {h}.', 'Domain of base (A1); shifted domain (R1).', 2)


@R.add('ch07-st1', 'C4', (3, 5), 'multi_step')
def translate_task(rng, slot):
    city = rng.choice(CITIES)
    kind = rng.choice(['logo', 'ramp', 'family', 'temps'])
    if kind == 'logo':
        h, k = rng.randint(2, 8), rng.randint(1, 6)
        ans = f'(a) vertex (0, 0) → ({h}, {k}) (b) y = (x − {h})² + {k} (c) y = x² − {2 * h}x + {h * h + k} (d) the shape is unchanged; only its position changes'
        q_ = (f'A designer in {city} uses the curve y = x² for a logo and wants to move it so that its lowest point is at ({h}, {k}). (a) Describe the vertex before and after. (b) Write the new equation. '
              f'(c) Expand it. (d) Explain what stays the same under a translation.')
    elif kind == 'ramp':
        h = rng.choice([2, 3, 4, 5])
        k = rng.choice([1, 2, 3])
        ans = f'(a) y = |x − {h}| + {k} (b) lowest point ({h}, {k}) (c) at x = 0: y = {h + k} (d) both sides have gradient ±1; the translation keeps them'
        q_ = (f'A skate-park ramp in {city} has a V-shaped profile modelled by y = |x| translated {h} m right and {k} m up. (a) Write its equation. (b) State the lowest point. '
              f'(c) Find the height at x = 0. (d) Explain why the slopes of the sides are unchanged.')
    elif kind == 'family':
        ks = rng.sample(range(-4, 5), 3)
        ans = f'(a) vertices ' + ', '.join(f'({k}, 0)' for k in ks) + ' (b) each is a horizontal translation of y = x² (c) y = (x − h)² has vertex (h, 0) and axis x = h (d) y = (x − h)² + k: vertex (h, k)'
        q_ = (f'Investigate y = (x − h)² for h = {", ".join(map(str, ks))}. (a) Find the vertex of each. (b) Describe the transformation. (c) Generalise for any h. (d) Extend your rule to y = (x − h)² + k.')
    else:
        d = rng.choice([2, 3, 5])
        T = rng.choice([14, 18, 22, 25])
        ans = f'(a) a vertical translation of {d} units up (b) g(t) = f(t) + {d} (c) {T + d} °C (d) a horizontal translation g(t) = f(t − 2) shifts the times by 2 hours'
        q_ = (f'The temperature in {city} on a spring day follows T = f(t). On the next day every temperature is {d} °C higher. (a) Describe the transformation of the graph. (b) Write the new function g in terms of f. '
              f'(c) If f(14) = {T}, find g(14). (d) Describe the function if instead the whole pattern happened 2 hours later.')
    return short(q_, ans, f'{ans}. Translation identified and described (A1 A1); equation written (A1); generalised / interpreted (B/D: R1); notation (C1).', 5, 'multi_step', 'G5')


R.facts('ch07-st2', F(
    terms=[('reflection in the x-axis', 'the transformation y = −f(x): every y-value changes sign; (x, y) → (x, −y)'),
           ('reflection in the y-axis', 'the transformation y = f(−x): every x-value changes sign; (x, y) → (−x, y)'),
           ('even function', 'a function with f(−x) = f(x), whose graph is symmetric in the y-axis'),
           ('odd function', 'a function with f(−x) = −f(x), whose graph has rotational symmetry of order 2 about the origin')],
    facts=[('The point (3, 5) lies on y = f(x). Which point lies on y = −f(x)?', '(3, −5)', ['(−3, 5)', '(−3, −5)', '(5, 3)'], 'y-values change sign.'),
           ('The point (3, 5) lies on y = f(x). Which point lies on y = f(−x)?', '(−3, 5)', ['(3, −5)', '(−3, −5)', '(5, 3)'], 'x-values change sign.'),
           ('Which function is even?', 'f(x) = x⁴ + 1', ['f(x) = x³', 'f(x) = x + 1', 'f(x) = 2ˣ'], 'f(−x) = f(x).')],
    why=[('Explain why y = x² is unchanged by reflection in the y-axis.', '(−x)² = x², so f(−x) = f(x): the graph is symmetric about the y-axis.'),
         ('Explain why the roots of y = f(x) and y = −f(x) are the same.', 'Where f(x) = 0, −f(x) = 0 too: points on the x-axis do not move under reflection in the x-axis.'),
         ('Explain why y = 2^(−x) is a decreasing function.', 'It is the reflection of the increasing graph y = 2ˣ in the y-axis, so it falls from left to right.')],
    misc=[('y = −f(x) reflects the graph in the y-axis.', 'The minus outside changes y-values: it reflects in the x-axis.'),
          ('y = f(−x) for f(x) = x + 3 is y = −x − 3.', 'f(−x) = −x + 3; −x − 3 is −f(x).')],
))


@R.add('ch07-st2', 'C1', (1, 3), 'mcq')
def reflect_fn_mcq(rng, slot):
    p, q = rng.choice([v for v in range(-7, 8) if v]), rng.choice([v for v in range(-7, 8) if v])
    which = rng.choice(['−f(x)', 'f(−x)', '−f(−x)'])
    img = {'−f(x)': (p, -q), 'f(−x)': (-p, q), '−f(−x)': (-p, -q)}[which]
    others = [o for o in [(p, -q), (-p, q), (-p, -q), (q, p)] if o != img]
    return mcq(rng, f'The point {ptxt((p, q))} lies on y = f(x). Which point must lie on y = {which}?', ptxt(img), [ptxt(o) for o in others[:3]],
               f'y = {which}: {ptxt((p, q))} → {ptxt(img)}.')


@R.add('ch07-st2', 'C3', (1, 4), 'short')
def reflect_fn_eq(rng, slot):
    a, b, c = rng.choice([1, 2, -1, 3]), rng.randint(-6, 6), rng.randint(-8, 8)
    f = a * x ** 2 + b * x + c
    if rng.random() < 0.5:
        f = rng.choice([1, 2, -1]) * x ** 3 + b * x ** 2 + c
    which = rng.choice(['−f(x)', 'f(−x)'])
    gx = sp.expand(-f) if which == '−f(x)' else sp.expand(f.subs(x, -x))
    return short(f'f(x) = {sx(f)}. Find y = {which} in simplified form and describe the transformation.', f'y = {sx(gx)}; reflection in the {"x" if which == "−f(x)" else "y"}-axis',
                 f'{"Every term negated" if which == "−f(x)" else "x replaced by (−x)"} (M1); {sx(gx)} (A1); reflection in the {"x" if which == "−f(x)" else "y"}-axis (A1).', 3)


@R.add('ch07-st2', 'C3', (2, 5), 'short')
def even_odd(rng, slot):
    kinds = [(x ** 4 - rng.randint(1, 5) * x ** 2, 'even'), (x ** 3 - rng.randint(1, 5) * x, 'odd'), (x ** 2 + rng.randint(1, 4) * x, 'neither'),
             (rng.randint(2, 5) * x ** 5 + x, 'odd'), (x ** 2 + rng.randint(1, 9), 'even'), (x ** 3 + rng.randint(1, 6), 'neither')]
    f, t = rng.choice(kinds)
    fm = sp.expand(f.subs(x, -x))
    return short(f'Determine algebraically whether f(x) = {sx(f)} is even, odd or neither, and describe its symmetry.', f'f(−x) = {sx(fm)}; {t}' + ('; symmetric in the y-axis' if t == 'even' else '; rotational symmetry about the origin' if t == 'odd' else ''),
                 f'f(−x) found (M1 A1); compared with f(x) and −f(x) (R1); conclusion (A1).', 4)


@R.add('ch07-st2', 'C2', (2, 4), 'explain')
def reflect_fn_explain(rng, slot):
    who = name(rng)
    k = rng.randint(2, 9)
    kind = rng.choice(['which', 'roots', 'exp'])
    if kind == 'which':
        return explain(f'{who} says y = −(x − {k})² is the reflection of y = (x − {k})² in the y-axis. Explain the error.',
                       f'The minus is outside the function, so the y-values change sign: it is a reflection in the x-axis (vertex ({k}, 0) stays, the parabola opens downward).', 'Correct axis (R1); justification (A1).', 2)
    if kind == 'roots':
        return explain(f'f(x) has roots x = {k} and x = −{k + 1}. Explain what the roots of y = f(−x) are.',
                       f'Reflecting in the y-axis changes x to −x, so the roots become x = −{k} and x = {k + 1}.', 'Effect on x-values (R1); roots (A1).', 2)
    return explain(f'Explain why y = (1/{k})ˣ and y = {k}^(−x) are the same graph.', f'(1/{k})ˣ = {k}^(−x) by the laws of exponents: both are the reflection of y = {k}ˣ in the y-axis.', 'Index law (R1); reflection (R1).', 2)


@R.add('ch07-st2', 'C4', (3, 5), 'multi_step')
def reflect_fn_task(rng, slot):
    city = rng.choice(CITIES)
    kind = rng.choice(['pts', 'butterfly', 'abs', 'oddeven'])
    if kind == 'pts':
        pts = [(rng.randint(-5, 5), rng.randint(-5, 5)) for _ in range(3)]
        ans = f'(a) {", ".join(ptxt((p, -q)) for p, q in pts)} (b) {", ".join(ptxt((-p, q)) for p, q in pts)} (c) {", ".join(ptxt((-p, -q)) for p, q in pts)} (d) y = −f(−x) is a rotation of 180° about the origin'
        q_ = (f'The graph of y = f(x) passes through {", ".join(ptxt(p) for p in pts)}. (a) Find the images on y = −f(x). (b) Find the images on y = f(−x). (c) Find the images on y = −f(−x). '
              f'(d) Describe the single transformation that maps y = f(x) onto y = −f(−x).')
    elif kind == 'butterfly':
        a = rng.choice([1, 2, 3])
        ans = f'(a) f(−x) = {a}(−x)² ... = f(x): the curve is its own mirror image (b) y = −{a}x² (c) both pieces together are symmetric in both axes (d) even functions are symmetric in the y-axis'
        ans = f'(a) f(−x) = {a}x² = f(x), so the curve is symmetric in the y-axis (b) y = −{a}x² (c) together the two curves are symmetric in both axes (d) any even function'
        q_ = (f'A jewellery maker in {city} designs a pendant from y = {coef(a)}x² for −2 ≤ x ≤ 2 and its reflection. (a) Show that y = {coef(a)}x² is unchanged by reflection in the y-axis. '
              f'(b) Write the equation of its reflection in the x-axis. (c) Describe the symmetry of the finished pendant. (d) Which other functions would give the same symmetry?')
    elif kind == 'abs':
        h = rng.randint(1, 6)
        ans = f'(a) y = |x − {h}| has vertex ({h}, 0) (b) y = −|x − {h}|: vertex ({h}, 0), opens down (c) y = |−x − {h}| = |x + {h}|: vertex (−{h}, 0) (d) f(−x) moved the vertex; −f(x) flipped it'
        q_ = (f'Investigate reflections of f(x) = |x − {h}|. (a) Describe its graph. (b) Find and describe y = −f(x). (c) Find and simplify y = f(−x). (d) Compare the effects of the two reflections.')
    else:
        n = rng.choice([2, 3, 4, 5])
        ans = f'(a) f(−x) = (−x)^{n} = {"x" + sup(n) if n % 2 == 0 else "−x" + sup(n)} (b) {"even" if n % 2 == 0 else "odd"} (c) xⁿ is even for even n and odd for odd n (d) e.g. x² + x is neither'
        q_ = (f'Investigate whether f(x) = x{sup(n)} is even or odd. (a) Find f(−x). (b) Classify it. (c) Generalise for xⁿ. (d) Give an example of a polynomial that is neither even nor odd.')
    return short(q_, ans, f'{ans}. Reflections applied correctly (A1 A1); pattern generalised (B: R1); explanation communicated (C1 R1).', 5, 'multi_step', 'G5')


R.facts('ch07-st3', F(
    terms=[('vertical stretch', 'the transformation y = a f(x), which multiplies every y-value by a; scale factor a parallel to the y-axis'),
           ('horizontal stretch', 'the transformation y = f(bx), which multiplies every x-value by 1/b; scale factor 1/b parallel to the x-axis'),
           ('invariant point', 'a point that does not move under a transformation, e.g. points on the x-axis under a vertical stretch')],
    facts=[('The point (4, 6) lies on y = f(x). Which point lies on y = 3f(x)?', '(4, 18)', ['(12, 6)', '(4/3, 6)', '(4, 2)'], 'y-values multiplied by 3.'),
           ('The point (4, 6) lies on y = f(x). Which point lies on y = f(2x)?', '(2, 6)', ['(8, 6)', '(4, 12)', '(4, 3)'], 'x-values multiplied by 1/2.'),
           ('y = f(x/3) is a horizontal stretch with scale factor:', '3', ['1/3', '−3', '9'], 'f(bx) with b = 1/3 has scale factor 1/b = 3.')],
    why=[('Explain why y = f(2x) squashes the graph horizontally rather than stretching it.', 'To get the output f(a), the new function needs 2x = a, i.e. x = a/2: every x-value is halved.'),
         ('Explain why the x-intercepts of y = f(x) are invariant under y = 5f(x).', 'At an x-intercept y = 0, and 5 × 0 = 0, so those points do not move.'),
         ('Explain why a vertical stretch by factor −1 is the same as a reflection.', 'y = −f(x) multiplies each y-value by −1, which reflects the graph in the x-axis.')],
    misc=[('y = f(3x) stretches the graph horizontally by factor 3.', 'The scale factor is 1/3: the graph is compressed towards the y-axis.'),
          ('y = 2f(x) moves the graph up 2 units.', 'It multiplies y-values by 2 (a stretch); f(x) + 2 moves it up.')],
))


@R.add('ch07-st3', 'C1', (1, 3), 'mcq')
def stretch_mcq(rng, slot):
    p, q = rng.choice([2, 3, 4, 6, -2, 8]), rng.choice([3, 4, 5, -6, 10])
    a = rng.choice([2, 3, 4, Fr(1, 2)])
    kind = rng.choice(['v', 'h'])
    if kind == 'v':
        img = (p, Fr(q) * a)
        return mcq(rng, f'The point {ptxt((p, q))} lies on y = f(x). Which point lies on y = {coef(a)}f(x)?', f'({m(p)}, {fx(img[1])})',
                   [f'({fx(Fr(p) * a)}, {m(q)})', f'({fx(Fr(p) / a)}, {m(q)})', f'({m(p)}, {fx(Fr(q) / a)})'], f'y-values × {fx(a)}.')
    return mcq(rng, f'The point {ptxt((p, q))} lies on y = f(x). Which point lies on y = f({coef(a)}x)?', f'({fx(Fr(p) / a)}, {m(q)})',
               [f'({fx(Fr(p) * a)}, {m(q)})', f'({m(p)}, {fx(Fr(q) * a)})', f'({m(p)}, {fx(Fr(q) / a)})'], f'x-values × 1/{fx(a)}.')


@R.add('ch07-st3', 'C3', (1, 4), 'short')
def stretch_describe(rng, slot):
    a = rng.choice([2, 3, 4, 5, Fr(1, 2), Fr(1, 3)])
    kind = rng.choice(['v', 'h'])
    base = rng.choice(['x²', 'x³', '√x', '|x|', '2ˣ'])
    p, q = rng.choice({'x²': [(2, 4), (3, 9), (-1, 1)], 'x³': [(2, 8), (-1, -1), (1, 1)], '√x': [(4, 2), (9, 3), (16, 4)], '|x|': [(-3, 3), (2, 2), (5, 5)], '2ˣ': [(1, 2), (3, 8), (0, 1)]}[base])
    if kind == 'v':
        eq = f'y = {fx(a)}{base}' if base != '2ˣ' else f'y = {fx(a)} × 2ˣ'
        return short(f'Describe the transformation that maps y = {base} onto {eq}, and find the image of the point {ptxt((p, q))}.', f'vertical stretch, scale factor {fx(a)}; ({m(p)}, {fx(Fr(q) * a)})',
                     f'Vertical stretch (A1) scale factor {fx(a)} (A1); image ({m(p)}, {fx(Fr(q) * a)}) (A1).', 3)
    inner = f'{fx(a)}x' if Fr(a).denominator == 1 else f'x/{Fr(a).denominator}'
    eq = {'x²': f'y = ({inner})²', 'x³': f'y = ({inner})³', '√x': f'y = √({inner})', '|x|': f'y = |{inner}|', '2ˣ': f'y = 2^({inner})'}[base]
    return short(f'Describe the transformation that maps y = {base} onto {eq}, and find the image of the point {ptxt((p, q))}.', f'horizontal stretch, scale factor {fx(1 / Fr(a))}; ({fx(Fr(p) / a)}, {m(q)})',
                 f'Horizontal stretch (A1) scale factor 1/{fx(a)} = {fx(1 / Fr(a))} (A1); image ({fx(Fr(p) / a)}, {m(q)}) (A1).', 3)


@R.add('ch07-st3', 'C3', (2, 5), 'short')
def stretch_equation(rng, slot):
    b, c = rng.randint(-6, 6), rng.randint(-6, 6)
    f = x ** 2 + b * x + c
    a = rng.choice([2, 3, Fr(1, 2)])
    if rng.random() < 0.5:
        gx = sp.expand(sp.Rational(Fr(a).numerator, Fr(a).denominator) * f)
        return short(f'f(x) = {sx(f)}. Find the equation of the graph after a vertical stretch with scale factor {fx(a)}, and state its y-intercept.', f'y = {sx(gx)}; y-intercept {fx(Fr(c) * a)}',
                     f'y = {fx(a)}f(x) (M1); {sx(gx)} (A1); y-intercept (A1).', 3)
    k = rng.choice([2, 3])
    gx = sp.expand(f.subs(x, k * x))
    return short(f'f(x) = {sx(f)}. Find the equation of the graph after a horizontal stretch with scale factor 1/{k}.', f'y = {sx(gx)}',
                 f'y = f({k}x) (M1); substitute {k}x (A1); {sx(gx)} (A1).', 3)


@R.add('ch07-st3', 'C2', (2, 4), 'explain')
def stretch_explain(rng, slot):
    who = name(rng)
    k = rng.randint(2, 5)
    kind = rng.choice(['factor', 'invariant', 'vs'])
    if kind == 'factor':
        return explain(f'{who} says y = f({k}x) is a horizontal stretch with scale factor {k}. Explain the error.',
                       f'x-values are divided by {k}: the point (a, f(a)) moves to (a/{k}, f(a)), so the scale factor is 1/{k} (a compression).', 'Effect on a point (A1); correct factor (R1).', 2)
    if kind == 'invariant':
        return explain(f'Explain which points of y = f(x) do not move under the transformation y = {k}f(x).',
                       f'Points with y = 0 (on the x-axis), because {k} × 0 = 0.', 'Invariant points (A1); reason (R1).', 2)
    return explain(f'For f(x) = x², explain why {k * k}f(x) and f({k}x) give the same graph.',
                   f'f({k}x) = ({k}x)² = {k * k}x² = {k * k}f(x): for this function a horizontal stretch by 1/{k} equals a vertical stretch by {k * k}.', 'Algebra (A1); interpretation (R1).', 2)


@R.add('ch07-st3', 'C4', (3, 5), 'multi_step')
def stretch_task(rng, slot):
    city = rng.choice(CITIES)
    kind = rng.choice(['bridge', 'sound', 'parab', 'scale'])
    if kind == 'bridge':
        k = rng.choice([2, 3, 4, Fr(3, 2), Fr(5, 2)])
        H, W = rng.choice([4, 5, 6, 8]), rng.choice([10, 12, 16, 20])
        ans = f'(a) a vertical stretch with scale factor {fx(k)} (b) y = {coef(k)}f(x) (c) roots unchanged at x = 0 and x = {W}; maximum height {g(float(k * H))} m (d) a horizontal stretch y = f(x/2) would make it {2 * W} m wide'
        q_ = (f'An engineer in {city} models an arch {H} m tall and {W} m wide with y = f(x), 0 ≤ x ≤ {W}, and wants a new arch {fx(k)} times as tall but with the same width. (a) Describe the transformation. (b) Write the new function. '
              f'(c) Explain what happens to the roots and the maximum. (d) Describe the transformation needed to make the arch twice as wide instead.')
    elif kind == 'sound':
        a, b = rng.choice([2, 3]), rng.choice([2, 3])
        ans = f'(a) amplitude × {a} (vertical stretch) (b) period ÷ {b} (horizontal stretch factor 1/{b}) (c) y = {a} sin({b}x) (d) louder (amplitude) and higher pitch (frequency)'
        q_ = (f'A music student in {city} models a sound wave by y = sin x. (a) Describe the effect of y = {a} sin x. (b) Describe the effect of y = sin({b}x). (c) Write a function with both effects. '
              f'(d) Interpret the two stretches in terms of sound.')
    elif kind == 'parab':
        ks = [2, 3, 4]
        ans = f'(a) y = 2x², 3x², 4x² (b) each is a vertical stretch of y = x² (c) y = (√k x)² = kx²: also a horizontal stretch by 1/√k (d) k = {rng.choice([5, 6, 7])}: factor 1/√k ≈ …'
        kk = rng.choice([5, 6, 7])
        ans = f'(a) the points (1, k) are (1, 2), (1, 3), (1, 4) (b) each is a vertical stretch of y = x² with factor k (c) kx² = (√k x)², so it is also a horizontal stretch with factor 1/√k (d) for k = {kk}: factor 1/√{kk} ≈ {rsf(1 / math.sqrt(kk), 3)}'
        q_ = (f'Investigate y = kx² for k = {", ".join(map(str, ks))}. (a) Find the point with x = 1 on each. (b) Describe each as a transformation of y = x². (c) Show that y = kx² can also be described as a horizontal stretch. '
              f'(d) Find the horizontal scale factor for k = {kk}.')
    else:
        s = rng.choice([2, 5, 10])
        ans = f'(a) x-values × {s} (b) y = f(x/{s}) (c) a point (3, 7) moves to ({3 * s}, 7) (d) a map scale changes horizontal distances only if the vertical axis is unchanged'
        q_ = (f'A graph of a cycling route in {city} shows height y against distance x km. The distances are recalculated in units {s} times smaller. (a) Explain how the x-values change. '
              f'(b) Write the new function in terms of f. (c) Find the image of (3, 7). (d) Explain why the heights do not change.')
    return short(q_, ans, f'{ans}. Stretch identified with correct factor (A1 A1); function written (A1); interpreted / generalised (B/D: R1); communication (C1).', 5, 'multi_step', 'G5')


R.facts('ch07-st4', F(
    terms=[('combined transformation', 'two or more transformations applied in sequence, e.g. y = a f(x − h) + k'),
           ('order of transformations', 'vertical changes act on y-values: stretch/reflect before translating; horizontal changes act on x inside the function'),
           ('general form', 'the form y = a f(b(x − h)) + k: vertical stretch a, horizontal stretch 1/b, translation (h over k)')],
    facts=[('y = 2f(x) + 3 is: stretch by 2 vertically, then:', 'translate 3 up', ['translate 3 right', 'translate 3 down', 'stretch by 3'], 'Multiply first, then add.'),
           ('The vertex of y = −3(x − 1)² + 4 is:', '(1, 4)', ['(−1, 4)', '(1, −4)', '(−3, 4)'], 'Vertex form.'),
           ('(2, 5) on y = f(x) maps to which point on y = 2f(x − 1) + 3?', '(3, 13)', ['(1, 13)', '(3, 10)', '(3, 16)'], 'x + 1 = 3, y = 2 × 5 + 3.')],
    why=[('Explain why the order of a vertical stretch and a vertical translation matters.', 'Stretching then translating gives a f(x) + k; translating then stretching gives a(f(x) + k) = a f(x) + ak – a different translation.'),
         ('Explain how to find the image of a point under y = a f(x − h) + k.', 'The x-coordinate moves h right; the y-coordinate is multiplied by a and then k is added: (p, q) → (p + h, aq + k).'),
         ('Explain why y = −f(x) + k does not have the same maximum as y = f(x) + k.', 'The reflection turns the minimum of f into a maximum, so the extreme values change.')],
    misc=[('y = 3f(x) + 1 and y = 3(f(x) + 1) are the same.', '3(f(x) + 1) = 3f(x) + 3, a translation of 3, not 1.'),
          ('In y = f(2(x − 3)) the graph moves 6 units right.', 'The translation is 3 units right; the 2 is a horizontal stretch.')],
))


@R.add('ch07-st4', 'C1', (1, 3), 'mcq')
def combined_mcq(rng, slot):
    p, q = rng.randint(-5, 5), rng.randint(-5, 5)
    a, h, k = rng.choice([2, 3, -1, -2]), rng.randint(-4, 4), rng.randint(-5, 5)
    img = (p + h, a * q + k)
    others = [(p - h, a * q + k), (p + h, a * (q + k)), (p + h, q + k)]
    others = [o for o in dict.fromkeys(others) if o != img]
    while len(others) < 3:
        others.append((img[0] + 1, img[1] - 1))
    return mcq(rng, f'The point {ptxt((p, q))} lies on y = f(x). Find its image on y = {coef(a)}f(x{sgn(-h) if h else ""}){sgn(k) if k else ""}.', ptxt(img), [ptxt(o) for o in others[:3]],
               f'x: {m(p)} + {m(h)} = {m(img[0])}; y: {m(a)} × {m(q)} + {m(k)} = {m(img[1])}.')


@R.add('ch07-st4', 'C3', (1, 4), 'short')
def combined_describe(rng, slot):
    a, h, k = rng.choice([2, 3, -1, -2, Fr(1, 2)]), rng.choice([v for v in range(-5, 6) if v]), rng.choice([v for v in range(-6, 7) if v])
    base = rng.choice(['x²', '|x|', '√x', 'x³'])
    eq = coef(a) + _shift_txt(base, h, 0).replace(base, base)
    eq = f'{coef(a)}{_shift_txt(base, h, 0)}{sgn(k)}'
    parts = []
    if a < 0:
        parts.append('reflection in the x-axis')
    if abs(a) != 1:
        parts.append(f'vertical stretch, scale factor {fx(abs(Fr(a)))}')
    parts.append(f'translation ({m(h)} over {m(k)})')
    return short(f'Describe fully, in order, a sequence of transformations that maps y = {base} onto y = {eq}.', '; then '.join(parts),
                 ' '.join('(A1)' for _ in parts) + ' each transformation; correct order: stretch/reflect before the vertical translation (R1).', len(parts) + 1)


@R.add('ch07-st4', 'C3', (2, 5), 'short')
def combined_equation(rng, slot):
    a, h, k = rng.choice([2, 3, -1, -2]), rng.choice([v for v in range(-4, 5) if v]), rng.randint(-6, 6)
    b, c = rng.randint(-4, 4), rng.randint(-5, 5)
    f = x ** 2 + b * x + c
    gx = sp.expand(a * f.subs(x, x - h) + k)
    steps = (f'{"a reflection in the x-axis and " if a < 0 else ""}a vertical stretch with scale factor {abs(a)}' if abs(a) != 1 else 'a reflection in the x-axis')
    return short(f'f(x) = {sx(f)}. The graph undergoes {steps}, followed by a translation ({m(h)} over {m(k)}). Find the equation of the final graph in expanded form.', f'y = {sx(gx)}',
                 f'y = {coef(a)}f(x{sgn(-h)}){sgn(k) if k else ""} (M1 A1); expanded {sx(gx)} (A1).', 3)


@R.add('ch07-st4', 'C2', (2, 4), 'explain')
def combined_explain(rng, slot):
    who = name(rng)
    a, k = rng.randint(2, 4), rng.randint(1, 6)
    kind = rng.choice(['order', 'point', 'inside'])
    if kind == 'order':
        return explain(f'{who} translates y = f(x) up {k} units and then stretches it vertically by factor {a}, expecting y = {a}f(x) + {k}. Explain why the result is different.',
                       f'Translating first gives f(x) + {k}; stretching then multiplies everything by {a}: {a}f(x) + {a * k}. To get {a}f(x) + {k}, stretch first.', 'Both orders (A1); conclusion (R1).', 2)
    if kind == 'point':
        p, q = rng.randint(1, 5), rng.randint(1, 5)
        return explain(f'Explain how the point ({p}, {q}) on y = f(x) moves under y = {a}f(x − {k}) − 1.',
                       f'x moves {k} right to {p + k}; y is multiplied by {a} then 1 is subtracted: {a * q - 1}. Image ({p + k}, {a * q - 1}).', 'Each coordinate explained (R1); image (A1).', 2)
    return explain(f'Explain why y = f({a}(x − {k})) moves the graph {k} units right, not {a * k}.',
                   f'Writing it as f({a}x − {a * k}) hides the translation; in the bracketed form the shift is x − {k}, i.e. {k} right, after a horizontal stretch by 1/{a}.', 'Factorised form (R1); correct translation (A1).', 2)


@R.add('ch07-st4', 'C4', (3, 5), 'multi_step')
def combined_task(rng, slot):
    city = rng.choice(CITIES)
    kind = rng.choice(['fountain', 'logo', 'match', 'family'])
    if kind == 'fountain':
        a, h, k = rng.choice([-1, -2, Fr(-1, 2)]), rng.randint(2, 5), rng.randint(3, 8)
        root = h + math.sqrt(k / -float(a))
        ans = f'(a) reflection in the x-axis{", vertical stretch factor " + fx(abs(Fr(a))) if abs(Fr(a)) != 1 else ""}, translation ({h} over {k}) (b) y = {coef(a)}(x − {h})² + {k} (c) maximum ({h}, {k}) (d) lands at x ≈ {rsf(root, 3)} m'
        q_ = (f'A designer in {city} turns y = x² into the path of a water jet with a maximum height of {k} m at {h} m from the nozzle and the same shape as y = {coef(a)}x². (a) Describe the transformations. '
              f'(b) Write the equation. (c) State the maximum point. (d) Find where the water lands (y = 0) to 3 s.f.')
    elif kind == 'logo':
        pts = [(0, 0), (2, 4), (-1, 1)]
        a, h, k = rng.choice([2, -1, 3]), rng.randint(-3, 3), rng.randint(-4, 4)
        ans = f'(a) {", ".join(ptxt((p + h, a * q + k)) for p, q in pts)} (b) y = {coef(a)}(x{sgn(-h) if h else ""})²{sgn(k) if k else ""} (c) vertex ({m(h)}, {m(k)}) (d) {"opens downward" if a < 0 else "narrower than y = x²" if a > 1 else "same shape"}'
        q_ = (f'The points {", ".join(ptxt(p) for p in pts)} lie on y = x². The graph is transformed to y = {coef(a)}(x{sgn(-h) if h else ""})²{sgn(k) if k else ""}. (a) Find the images of the three points. (b) Write the equation. '
              f'(c) State the vertex. (d) Describe the shape compared with y = x².')
    elif kind == 'match':
        h, k = rng.randint(1, 5), rng.randint(1, 5)
        ans = f'(a) translation ({h} over 0) (b) vertical stretch factor 2 (c) translation (0 over {k}) (d) y = 2|x − {h}| + {k}'
        q_ = (f'Investigate the sequence: start with y = |x|. (a) Describe the transformation to y = |x − {h}|. (b) Then to y = 2|x − {h}|. (c) Then to y = 2|x − {h}| + {k}. (d) Write the final equation and its vertex.')
        ans = ans.replace(f'(d) y = 2|x − {h}| + {k}', f'(d) y = 2|x − {h}| + {k}, vertex ({h}, {k})')
    else:
        a = rng.choice([2, 3])
        ans = f'(a) y = {a}(x − h)² + k (b) vertex (h, k), axis x = h (c) for {a} > 0 the range is y ≥ k (d) any parabola with leading coefficient {a} is a transformation of y = {a}x²'
        q_ = (f'Investigate the family y = {a}x² + bx + c. (a) Show by completing the square that each member can be written as y = {a}(x − h)² + k. (b) State the vertex and axis. (c) State the range. (d) Draw a conclusion about the family.')
    return short(q_, ans, f'{ans}. Transformations identified in a valid order (A1 A1); equation / images correct (A1 A1); generalisation or context (B/D: R1).', 5, 'multi_step', 'G5')


# =============================================================================================
# ch08 Non-right-angled Trigonometry
# =============================================================================================
def _dg(v, k=1):
    return f'{r2(v, k)}°'


def sind(a):
    return math.sin(math.radians(a))


def cosd(a):
    return math.cos(math.radians(a))


R.facts('ch08-st1', F(
    terms=[('unit circle', 'a circle of radius 1 centred at the origin; the point at angle θ from the positive x-axis is (cos θ, sin θ)'),
           ('quadrant', 'one of the four regions of the plane cut by the axes; the signs of sin, cos and tan depend on the quadrant'),
           ('related acute angle', 'the acute angle between the terminal side of θ and the x-axis')],
    facts=[('sin 150° equals:', 'sin 30°', ['−sin 30°', 'cos 30°', '−cos 30°'], 'sin(180° − θ) = sin θ.'),
           ('In which quadrant are both sine and cosine negative?', 'the third', ['the first', 'the second', 'the fourth'], '180° < θ < 270°.'),
           ('cos 120° equals:', '−1/2', ['1/2', '√3/2', '−√3/2'], 'cos(180° − 60°) = −cos 60°.')],
    why=[('Explain why sin θ = sin(180° − θ).', 'On the unit circle the points at θ and 180° − θ are reflections in the y-axis, so they have the same y-coordinate.'),
         ('Explain why cos θ is negative for 90° < θ < 180°.', 'The point on the unit circle is to the left of the y-axis, so its x-coordinate is negative.'),
         ('Explain why sin²θ + cos²θ = 1.', 'The point (cos θ, sin θ) is on the unit circle; by Pythagoras its coordinates satisfy x² + y² = 1.')],
    misc=[('If sin θ = 0.5 then θ = 30° only.', 'For 0° ≤ θ ≤ 180°, θ = 30° or 150°.'),
          ('tan 135° = 1 because 135° is in the second quadrant.', 'tan is negative in the second quadrant: tan 135° = −1.')],
))

_EXACT = {0: ('0', '1', '0'), 30: ('1/2', '√3/2', '√3/3'), 45: ('√2/2', '√2/2', '1'), 60: ('√3/2', '1/2', '√3'), 90: ('1', '0', 'undefined')}


def _exact(fn, ang):
    a = ang % 360
    ref = a % 180
    ref = ref if ref <= 90 else 180 - ref
    i = {'sin': 0, 'cos': 1, 'tan': 2}[fn]
    v = _EXACT[ref][i]
    if v in ('0', 'undefined'):
        return v
    s = {'sin': math.sin, 'cos': math.cos, 'tan': math.tan}[fn](math.radians(a))
    return ('−' if s < 0 else '') + v


@R.add('ch08-st1', 'C1', (1, 3), 'mcq')
def unit_circle_mcq(rng, slot):
    ang = rng.choice([120, 135, 150, 210, 225, 240, 300, 315, 330])
    fn = rng.choice(['sin', 'cos', 'tan'])
    corr = _exact(fn, ang)
    pool = ['1/2', '−1/2', '√3/2', '−√3/2', '√2/2', '−√2/2', '1', '−1', '√3', '−√3', '√3/3', '−√3/3']
    wr = [p for p in pool if p != corr and p.lstrip('−') == corr.lstrip('−')] + [p for p in pool if p.lstrip('−') != corr.lstrip('−')]
    return mcq(rng, f'Find the exact value of {fn} {ang}°.', corr, wr[:1] + rng.sample(wr[1:], 2), f'Related angle {ang % 180 if ang % 180 <= 90 else 180 - ang % 180}°; sign from the quadrant.')


@R.add('ch08-st1', 'C3', (1, 4), 'short')
def unit_circle_point(rng, slot):
    ang = rng.choice([v for v in range(10, 360, 5) if v % 90])
    q = ang // 90 + 1
    if rng.random() < 0.5:
        return short(f'Find, to 3 s.f., the coordinates of the point on the unit circle at {ang}° from the positive x-axis, and state the quadrant.',
                     f'({rsf(cosd(ang), 3)}, {rsf(sind(ang), 3)}); quadrant {q}', f'(cos {ang}°, sin {ang}°) (M1); values (A1); quadrant {q} (A1).', 3)
    s = round(rng.uniform(0.1, 0.95), 2)
    a1 = math.degrees(math.asin(s))
    return short(f'Find all angles θ with 0° ≤ θ ≤ 360° such that sin θ = {g(s)}, to 1 d.p.', f'θ = {_dg(a1)} or θ = {_dg(180 - a1)}',
                 f'sin⁻¹ {g(s)} = {_dg(a1)} (A1); 180° − {_dg(a1)} = {_dg(180 - a1)} (M1 A1).', 3)


@R.add('ch08-st1', 'C3', (2, 5), 'short')
def trig_from_one(rng, slot):
    a, c = rng.choice([(3, 5), (5, 13), (8, 17), (7, 25), (20, 29)])
    b = int(math.isqrt(c * c - a * a))
    obtuse = rng.random() < 0.5
    return short(f'θ is an {"obtuse" if obtuse else "acute"} angle with sin θ = {a}/{c}. Find the exact values of cos θ and tan θ.',
                 f'cos θ = {"−" if obtuse else ""}{b}/{c}; tan θ = {"−" if obtuse else ""}{a}/{b}',
                 f'sin²θ + cos²θ = 1 (M1); cos²θ = {b * b}/{c * c} (A1); sign from the quadrant (R1); tan θ = sin θ/cos θ (A1).', 4)


@R.add('ch08-st1', 'C2', (2, 4), 'explain')
def unit_circle_explain(rng, slot):
    who = name(rng)
    a = rng.choice([20, 25, 35, 40, 50, 55, 65, 70])
    kind = rng.choice(['two', 'cos', 'sign'])
    if kind == 'two':
        return explain(f'{who} says the only angle between 0° and 180° with sine equal to sin {a}° is {a}°. Explain why this is wrong.',
                       f'sin(180° − θ) = sin θ, so sin {180 - a}° = sin {a}° as well; both points on the unit circle have the same height.', 'Second angle (A1); reason (R1).', 2)
    if kind == 'cos':
        return explain(f'Explain why cos {180 - a}° = −cos {a}°.', f'The points at {a}° and {180 - a}° are mirror images in the y-axis, so their x-coordinates are opposite.', 'Unit-circle reflection (R1); conclusion (R1).', 2)
    return explain(f'Explain why tan {180 + a}° = tan {a}°.', f'The point at {180 + a}° is the half-turn image of the point at {a}°: both coordinates change sign, so their ratio sin/cos is unchanged.', 'Signs of both coordinates (R1); ratio (R1).', 2)


@R.add('ch08-st1', 'C4', (3, 5), 'multi_step')
def unit_circle_task(rng, slot):
    city = rng.choice(CITIES)
    kind = rng.choice(['ferris', 'table', 'clock', 'identity'])
    if kind == 'ferris':
        r = rng.choice([20, 25, 30, 40, 60])
        ang = rng.choice([30, 60, 120, 150, 210, 240])
        ans = f'(a) ({rsf(r * cosd(ang), 3)}, {rsf(r * sind(ang), 3)}) m (b) height above the hub {rsf(r * sind(ang), 3)} m (c) {r + 5 + r * sind(ang):.1f} m above the ground (d) another angle with the same height: {(180 - ang) % 360}°'
        q_ = (f'A Ferris wheel in {city} has radius {r} m with its hub {r + 5} m above the ground. A cabin is at {ang}° anticlockwise from the horizontal through the hub. (a) Find its coordinates relative to the hub. '
              f'(b) Find its height relative to the hub. (c) Find its height above the ground. (d) Find another angle at which a cabin is at the same height.')
    elif kind == 'table':
        a = rng.choice([30, 45, 60])
        ans = f'(a) sin: {_exact("sin", a)}, {_exact("sin", 180 - a)}, {_exact("sin", 180 + a)}, {_exact("sin", 360 - a)} (b) cos: {_exact("cos", a)}, {_exact("cos", 180 - a)}, {_exact("cos", 180 + a)}, {_exact("cos", 360 - a)} (c) the values repeat with sign changes by quadrant (d) "All Students Take Calculus": all, sin, tan, cos positive in quadrants 1–4'
        q_ = (f'Investigate {a}°, {180 - a}°, {180 + a}° and {360 - a}°. (a) Find the exact sine of each. (b) Find the exact cosine of each. (c) Describe the pattern. (d) State a rule for which ratios are positive in each quadrant.')
    elif kind == 'clock':
        L = rng.choice([8, 10, 12, 15])
        hr = rng.choice([1, 2, 4, 5, 7, 8, 10, 11])
        ang = (90 - 30 * hr) % 360
        ans = f'(a) {30 * hr}° clockwise from 12 (b) {ang}° anticlockwise from the positive x-axis (c) ({rsf(L * cosd(ang), 3)}, {rsf(L * sind(ang), 3)}) cm (d) every hour the hand turns 30°, so the coordinates repeat every 12 hours'
        q_ = (f'The hour hand of a clock tower in {city} is {L} cm long. At {hr} o\'clock (minute hand at 12): (a) find the angle of the hour hand measured clockwise from 12. (b) Convert it to an angle measured anticlockwise from 3 o\'clock. '
              f'(c) Find the coordinates of the tip relative to the centre. (d) Explain the periodic nature of the motion.')
    else:
        ang = rng.choice([25, 40, 110, 160, 200, 290])
        ans = f'(a) sin {ang}° ≈ {rsf(sind(ang), 3)}, cos {ang}° ≈ {rsf(cosd(ang), 3)} (b) sum of squares ≈ 1 (c) x² + y² = 1 on the unit circle (d) tan {ang}° = sin/cos ≈ {rsf(math.tan(math.radians(ang)), 3)}'
        q_ = (f'Investigate sin²θ + cos²θ for θ = {ang}°. (a) Find sin θ and cos θ. (b) Calculate sin²θ + cos²θ. (c) Prove that the result is always 1. (d) Verify that tan θ = sin θ/cos θ for this angle.')
    return short(q_, ans, f'{ans}. Unit-circle values (A1 A1); quadrant / sign reasoning (R1); pattern or context (B/D: R1); communication (C1).', 5, 'multi_step', 'G5')


R.facts('ch08-st2', F(
    terms=[('sine rule', 'a/sin A = b/sin B = c/sin C, relating each side of a triangle to the sine of the opposite angle'),
           ('ambiguous case', 'when two sides and a non-included acute angle are given, two different triangles may fit, because sin θ = sin(180° − θ)'),
           ('opposite side', 'the side of a triangle that does not touch a given angle')],
    facts=[('The sine rule is most useful when you know:', 'two angles and one side', ['three sides', 'two sides and the included angle', 'only the three angles'], 'Each side is paired with its opposite angle.'),
           ('In triangle ABC, a = 10, A = 30°, B = 45°. Then b is:', '10√2', ['5√2', '20', '10'], 'b = 10 sin 45°/sin 30°.'),
           ('The ambiguous case can occur when you know:', 'two sides and a non-included angle', ['three sides', 'three angles', 'two angles and a side'], 'SSA.')],
    why=[('Explain why the ambiguous case gives two possible triangles.', 'Solving sin B = k gives an acute angle and its supplement 180° − B; both may fit with the given angle if their sum is less than 180°.'),
         ('Explain why the sine rule cannot be used directly with three sides.', 'Every ratio a/sin A needs a known angle; with only sides no ratio is complete, so use the cosine rule.'),
         ('Explain how to check whether the obtuse solution in the ambiguous case is possible.', 'Add it to the given angle; if the sum is less than 180°, a third angle exists and the triangle is possible.')],
    misc=[('The sine rule only works in right-angled triangles.', 'It works in any triangle; SOHCAHTOA is the special right-angled case.'),
          ('sin B = 0.8 has only one solution in a triangle.', 'B ≈ 53.1° or 126.9°; both may be possible.')],
))


@R.add('ch08-st2', 'C1', (1, 3), 'mcq')
def sine_rule_mcq(rng, slot):
    A, B = rng.randint(30, 80), rng.randint(30, 80)
    a = rng.randint(5, 20)
    b = a * sind(B) / sind(A)
    return mcq(rng, f'In triangle ABC, A = {A}°, B = {B}° and a = {a} cm. Find b to 3 s.f.', f'{rsf(b, 3)} cm',
               [f'{rsf(a * sind(A) / sind(B), 3)} cm', f'{rsf(a * B / A, 3)} cm', f'{rsf(a * sind(180 - A - B) / sind(A), 3)} cm'], f'b = a sin B / sin A.')


def _tri_aas(rng):
    A, B = rng.randint(25, 85), rng.randint(25, 85)
    C = 180 - A - B
    if C < 15:
        return None
    a = rng.randint(6, 40)
    return A, B, C, a


@R.add('ch08-st2', 'C3', (1, 4), 'short')
def sine_rule_side(rng, slot):
    t = _tri_aas(rng)
    if not t:
        return None
    A, B, C, a = t
    lbl = rng.choice([('P', 'Q', 'R'), ('A', 'B', 'C'), ('X', 'Y', 'Z'), ('K', 'L', 'M')])
    b, c = a * sind(B) / sind(A), a * sind(C) / sind(A)
    return short(f'In triangle {"".join(lbl)}, angle {lbl[0]} = {A}°, angle {lbl[1]} = {B}° and the side opposite {lbl[0]} is {a} cm. Find the other two sides to 3 s.f.',
                 f'side opposite {lbl[1]}: {rsf(b, 3)} cm; side opposite {lbl[2]}: {rsf(c, 3)} cm',
                 f'Third angle {C}° (A1); sine rule {a}/sin {A}° = x/sin {B}° (M1); {rsf(b, 3)} (A1); {rsf(c, 3)} (A1).', 4)


@R.add('ch08-st2', 'C3', (2, 5), 'short')
def sine_rule_angle(rng, slot):
    A = rng.randint(25, 70)
    a = rng.randint(6, 20)
    b = round(a * rng.uniform(1.05, 1.0 / sind(A) - 0.05), 1)
    s = b * sind(A) / a
    if not (0 < s < 1):
        return None
    B1 = math.degrees(math.asin(s))
    B2 = 180 - B1
    two = A + B2 < 180
    return short(f'In triangle ABC, a = {a} cm, b = {g(b)} cm and A = {A}°. Find the possible values of angle B, to 1 d.p.',
                 f'B = {_dg(B1)}' + (f' or B = {_dg(B2)}' if two else ''),
                 f'sin B = {g(b)} sin {A}°/{a} = {rsf(s, 4)} (M1 A1); B = {_dg(B1)} (A1); {"also " + _dg(B2) + " since " + str(A) + "° + " + _dg(B2) + " < 180° (R1)" if two else "180° − " + _dg(B1) + " is too large with A (R1)"}.', 4)


@R.add('ch08-st2', 'C2', (2, 4), 'explain')
def sine_rule_explain(rng, slot):
    who = name(rng)
    A = rng.randint(30, 60)
    kind = rng.choice(['amb', 'sss', 'check'])
    if kind == 'amb':
        a, b = rng.randint(6, 9), rng.randint(10, 14)
        s = b * sind(A) / a
        if s >= 1:
            return None
        B1 = math.degrees(math.asin(s))
        return explain(f'In triangle ABC, A = {A}°, a = {a} cm and b = {b} cm. {who} finds B = {_dg(B1)} and stops. Explain why there may be another triangle.',
                       f'sin B = {rsf(s, 3)} is also satisfied by B = {_dg(180 - B1)}; since {A}° + {_dg(180 - B1)} {"<" if A + 180 - B1 < 180 else "≥"} 180°, {"a second triangle exists" if A + 180 - B1 < 180 else "the second triangle is not possible here"}.',
                       'Supplementary angle (R1); check of angle sum (A1).', 2)
    if kind == 'sss':
        return explain(f'{who} tries to use the sine rule on a triangle with sides 7 cm, 9 cm and 12 cm. Explain why this does not work and what to use instead.',
                       'No angle is known, so no ratio side/sin(angle) is complete. Use the cosine rule to find an angle first.', 'Reason (R1); cosine rule (R1).', 2)
    return explain(f'Explain how you know that the largest angle of a triangle is opposite the longest side, using the sine rule.',
                   'a/sin A = b/sin B, so a > b exactly when sin A > sin B; for angles of a triangle this means the larger side faces the larger angle.', 'Sine rule ratio (R1); conclusion (R1).', 2)


@R.add('ch08-st2', 'C4', (3, 5), 'multi_step')
def sine_rule_task(rng, slot):
    city = rng.choice(SEA)
    kind = rng.choice(['tower', 'river', 'amb', 'island'])
    if kind == 'tower':
        d = rng.randint(30, 80)
        e1, e2 = rng.randint(20, 35), rng.randint(40, 60)
        # two observers d apart on the same side; angles of elevation e1 (far) and e2 (near)
        apex = e2 - e1
        L = d * sind(e1) / sind(apex)
        h = L * sind(e2)
        ans = f'(a) angle at the top = {e2}° − {e1}° = {apex}° (b) distance from the near point to the top = {rsf(L, 3)} m (c) height = {rsf(h, 3)} m (d) the ground is assumed level and the observers in line with the tower'
        q_ = (f'Two surveyors in {city} stand {d} m apart in line with a tower. From the farther one the angle of elevation of the top is {e1}°, and from the nearer one it is {e2}°. (a) Find the angle at the top of the tower in the triangle formed. '
              f'(b) Use the sine rule to find the distance from the nearer surveyor to the top. (c) Find the height of the tower. (d) State an assumption.')
    elif kind == 'river':
        AB = rng.randint(50, 200)
        A, B = rng.randint(40, 75), rng.randint(40, 75)
        C = 180 - A - B
        AC = AB * sind(B) / sind(C)
        w = AC * sind(A)
        ans = f'(a) {C}° (b) AC = {rsf(AC, 3)} m (c) width ≈ {rsf(w, 3)} m (d) only two angles and one length are needed; no one crosses the river'
        q_ = (f'To measure a river near {city}, points A and B are {AB} m apart on one bank and C is a tree on the opposite bank. Angle CAB = {A}° and angle CBA = {B}°. (a) Find angle ACB. '
              f'(b) Find AC. (c) Find the width of the river (the perpendicular distance from C to AB). (d) Explain the advantage of this method.')
    elif kind == 'amb':
        A = rng.randint(30, 50)
        a = rng.randint(7, 10)
        b = round(a * rng.uniform(1.1, 1 / sind(A) - 0.1), 1)
        s = b * sind(A) / a
        B1 = math.degrees(math.asin(s))
        B2 = 180 - B1
        c1 = a * sind(180 - A - B1) / sind(A)
        c2 = a * sind(180 - A - B2) / sind(A)
        ans = f'(a) sin B = {rsf(s, 4)} (b) B = {_dg(B1)} or {_dg(B2)} (c) c = {rsf(c1, 3)} cm or {rsf(c2, 3)} cm (d) the given angle is not between the two given sides, so the side a can "swing" to two positions'
        q_ = (f'Investigate triangle ABC with A = {A}°, a = {a} cm and b = {g(b)} cm. (a) Find sin B. (b) Find both possible values of B. (c) Find the length c for each triangle. (d) Explain geometrically why two triangles exist.')
    else:
        d = rng.randint(10, 40)
        A, B = rng.randint(35, 70), rng.randint(35, 70)
        C = 180 - A - B
        PA, PB = d * sind(B) / sind(C), d * sind(A) / sind(C)
        ans = f'(a) {C}° (b) {rsf(PA, 3)} km from A, {rsf(PB, 3)} km from B (c) {"A" if PA < PB else "B"} is closer (d) angle measurements must be accurate; a 1° error changes the answers'
        q_ = (f'Two coastguard stations A and B near {city} are {d} km apart. A boat P in distress is seen at angle PAB = {A}° and angle PBA = {B}°. (a) Find angle APB. (b) Find the distance of the boat from each station. '
              f'(c) Which station should send help? (d) Comment on the accuracy needed.')
    return short(q_, ans, f'{ans}. Sine rule set up (M1); angles/sides found (A1 A1); ambiguous case or geometry interpreted (R1); answer in context with units (D: C1).', 5, 'multi_step', 'G5')


R.facts('ch08-st3', F(
    terms=[('cosine rule', 'the formula a² = b² + c² − 2bc cos A, linking three sides of a triangle and one angle'),
           ('included angle', 'the angle between two given sides of a triangle'),
           ('cosine rule for angles', 'the rearranged formula cos A = (b² + c² − a²)/(2bc)')],
    facts=[('The cosine rule is used when you know:', 'three sides, or two sides and the included angle', ['two angles and a side', 'only three angles', 'one side only'], 'SSS or SAS.'),
           ('If a² = b² + c², angle A is:', '90°', ['obtuse', 'acute', '60°'], 'cos A = 0.'),
           ('A triangle has sides 5, 7, 8. The largest angle is opposite the side:', '8', ['5', '7', 'all are equal'], 'Largest angle faces the longest side.')],
    why=[('Explain why the cosine rule becomes Pythagoras\' theorem when A = 90°.', 'cos 90° = 0, so the term 2bc cos A vanishes: a² = b² + c².'),
         ('Explain why a negative value of cos A means angle A is obtuse.', 'Cosine is negative for angles between 90° and 180°.'),
         ('Explain why the cosine rule gives a unique angle (no ambiguous case).', 'cos⁻¹ gives exactly one angle between 0° and 180°, and cosine is different for each such angle.')],
    misc=[('a² = b² + c² − 2bc cos A can be simplified to a² = (b + c)² cos A.', 'The terms cannot be combined like that; keep b² + c² − 2bc cos A.'),
          ('If cos A = −0.3, then A cannot be found because cosines must be positive.', 'A = cos⁻¹(−0.3) ≈ 107.5°, an obtuse angle.')],
))


@R.add('ch08-st3', 'C1', (1, 3), 'mcq')
def cosine_mcq(rng, slot):
    b, c = rng.randint(4, 15), rng.randint(4, 15)
    A = rng.choice([40, 50, 60, 70, 100, 120])
    a = math.sqrt(b * b + c * c - 2 * b * c * cosd(A))
    return mcq(rng, f'In triangle ABC, b = {b} cm, c = {c} cm and A = {A}°. Find a to 3 s.f.', f'{rsf(a, 3)} cm',
               [f'{rsf(math.sqrt(b * b + c * c + 2 * b * c * cosd(A)), 3)} cm', f'{rsf(math.sqrt(b * b + c * c), 3)} cm', f'{rsf(b * b + c * c - 2 * b * c * cosd(A), 3)} cm'],
               f'a² = {b}² + {c}² − 2({b})({c}) cos {A}°.')


@R.add('ch08-st3', 'C3', (1, 4), 'short')
def cosine_side(rng, slot):
    b, c = rng.randint(5, 30), rng.randint(5, 30)
    A = rng.randint(20, 150)
    a = math.sqrt(b * b + c * c - 2 * b * c * cosd(A))
    city = rng.choice(CITIES)
    if rng.random() < 0.5:
        return short(f'Two straight paths in a park in {city} leave a gate at an angle of {A}° to each other. One is {b} m long and the other {c} m. Find the straight-line distance between their ends.',
                     f'{rsf(a, 3)} m', f'd² = {b}² + {c}² − 2({b})({c}) cos {A}° (M1 A1); {rsf(a, 3)} m (A1).', 3)
    return short(f'In triangle PQR, PQ = {b} cm, PR = {c} cm and angle QPR = {A}°. Find QR to 3 s.f.', f'{rsf(a, 3)} cm',
                 f'QR² = {b}² + {c}² − 2({b})({c}) cos {A}° (M1 A1); {rsf(a, 3)} cm (A1).', 3)


@R.add('ch08-st3', 'C3', (2, 5), 'short')
def cosine_angle(rng, slot):
    while True:
        a, b, c = sorted(rng.sample(range(4, 25), 3))
        if a + b > c:
            break
    C = math.degrees(math.acos((a * a + b * b - c * c) / (2 * a * b)))
    if rng.random() < 0.5:
        return short(f'A triangle has sides {a} cm, {b} cm and {c} cm. Find its largest angle to 1 d.p. and state whether the triangle is acute, right-angled or obtuse.',
                     f'{_dg(C)}; {"obtuse" if C > 90.05 else "right-angled" if abs(C - 90) < 0.05 else "acute"}',
                     f'Largest angle opposite {c} (R1); cos C = ({a}² + {b}² − {c}²)/(2 × {a} × {b}) = {rsf((a * a + b * b - c * c) / (2 * a * b), 4)} (M1 A1); {_dg(C)} (A1).', 4)
    A = math.degrees(math.acos((b * b + c * c - a * a) / (2 * b * c)))
    return short(f'A triangular plot of land has sides {a} m, {b} m and {c} m. Find the angle between the {b} m and {c} m sides, to 1 d.p.', _dg(A),
                 f'cos θ = ({b}² + {c}² − {a}²)/(2 × {b} × {c}) (M1 A1); {_dg(A)} (A1).', 3)


@R.add('ch08-st3', 'C2', (2, 4), 'explain')
def cosine_explain(rng, slot):
    who = name(rng)
    b, c = rng.randint(5, 12), rng.randint(5, 12)
    A = rng.choice([100, 110, 120, 130])
    kind = rng.choice(['sign', 'choose', 'pyth'])
    if kind == 'sign':
        return explain(f'{who} calculates a² = {b}² + {c}² − 2({b})({c}) cos {A}° and says the answer must be smaller than {b}² + {c}² = {b * b + c * c}. Explain the mistake.',
                       f'cos {A}° is negative, so −2bc cos A is positive and a² = {rsf(b * b + c * c - 2 * b * c * cosd(A), 4)} is larger than {b * b + c * c}.', 'Sign of cos (R1); value (A1).', 2)
    if kind == 'choose':
        return explain(f'Explain whether to use the sine rule or the cosine rule to find the third side of a triangle with sides {b} cm and {c} cm and an included angle of {A - 60}°.',
                       'Cosine rule: the known angle is between the two known sides, so no side–opposite-angle pair is complete for the sine rule.', 'Choice (A1); reason (R1).', 2)
    return explain(f'Explain why the cosine rule is a generalisation of Pythagoras\' theorem.', 'When A = 90°, cos A = 0 and a² = b² + c²; for other angles the term −2bc cos A corrects for A not being a right angle.', 'Special case (R1); role of correction term (R1).', 2)


@R.add('ch08-st3', 'C4', (3, 5), 'multi_step')
def cosine_task(rng, slot):
    city = rng.choice(SEA)
    kind = rng.choice(['ships', 'field', 'robot', 'roof'])
    if kind == 'ships':
        v1, v2 = rng.sample(range(10, 26), 2)
        t = rng.choice([2, 3, 4])
        ang = rng.randint(40, 130)
        d = math.sqrt((v1 * t) ** 2 + (v2 * t) ** 2 - 2 * v1 * v2 * t * t * cosd(ang))
        ans = f'(a) {v1 * t} km and {v2 * t} km (b) {ang}° (c) {rsf(d, 3)} km (d) the distance grows by {rsf(d / t, 3)} km each hour'
        q_ = (f'Two ferries leave the port of {city} at the same time. One sails at {v1} km/h and the other at {v2} km/h, on courses {ang}° apart. (a) Find how far each has sailed after {t} hours. '
              f'(b) State the angle between their paths. (c) Find the distance between them. (d) Describe how the distance between them changes over time.')
    elif kind == 'field':
        a, b, c = rng.choice([(40, 55, 70), (60, 80, 110), (35, 50, 62), (90, 75, 120)])
        C = math.degrees(math.acos((a * a + b * b - c * c) / (2 * a * b)))
        area = 0.5 * a * b * sind(C)
        ans = f'(a) the angle opposite the {c} m side (b) {_dg(C)} (c) area = ½ × {a} × {b} × sin {_dg(C)} ≈ {rsf(area, 4)} m² (d) about {rsf(area / 10000, 3)} hectares'
        q_ = (f'A farmer near {city} has a triangular field with sides {a} m, {b} m and {c} m. (a) Identify the largest angle. (b) Find it using the cosine rule. (c) Find the area of the field. (d) Convert the area to hectares.')
    elif kind == 'robot':
        d1, d2 = rng.randint(3, 10), rng.randint(3, 10)
        turn = rng.choice([30, 45, 60, 80, 100])
        inner = 180 - turn
        d = math.sqrt(d1 * d1 + d2 * d2 - 2 * d1 * d2 * cosd(inner))
        ans = f'(a) {inner}° (b) {rsf(d, 3)} m (c) {rsf(d1 + d2 - d, 3)} m shorter (d) the straight path is shortest because a triangle side is less than the sum of the other two'
        q_ = (f'A robot in a lab in {city} drives {d1} m, turns {turn}° and drives {d2} m. (a) Find the interior angle at the turn. (b) Find the straight-line distance back to the start. '
              f'(c) How much shorter is the straight path? (d) Explain why the straight path is always shorter.')
    else:
        w = rng.randint(6, 12)
        s1, s2 = round(w * rng.uniform(0.55, 0.7), 1), round(w * rng.uniform(0.55, 0.7), 1)
        apex = math.degrees(math.acos((s1 * s1 + s2 * s2 - w * w) / (2 * s1 * s2)))
        ans = f'(a) {_dg(apex)} (b) {"obtuse" if apex > 90 else "acute"} (c) height ≈ {rsf(s1 * sind(math.degrees(math.acos((s1 * s1 + w * w - s2 * s2) / (2 * s1 * w)))), 3)} m (d) the rafters must fit the span: {g(s1)} + {g(s2)} > {w}'
        q_ = (f'The roof truss of a house in {city} is a triangle with base {w} m and rafters {g(s1)} m and {g(s2)} m. (a) Find the angle at the top. (b) Is it acute or obtuse? '
              f'(c) Find the height of the top above the base. (d) Explain a condition the rafter lengths must satisfy.')
    return short(q_, ans, f'{ans}. Cosine rule set up (M1 A1); results accurate (A1); interpreted in context (D: R1); clear communication with units (C1).', 5, 'multi_step', 'G5')


R.facts('ch08-st4', F(
    terms=[('area formula ½ab sin C', 'the area of any triangle is half the product of two sides and the sine of the included angle'),
           ('included angle', 'the angle between the two sides used in ½ab sin C'),
           ('segment of a circle', 'the region between a chord and an arc; its area is sector area minus triangle area')],
    facts=[('A triangle has sides 8 cm and 10 cm with included angle 30°. Its area is:', '20 cm²', ['40 cm²', '80 cm²', '34.6 cm²'], '½ × 8 × 10 × ½.'),
           ('½ab sin C gives the largest area for fixed a and b when C is:', '90°', ['180°', '45°', '60°'], 'sin C is largest (1) at 90°.'),
           ('Two triangles with sides 6, 9 and included angles 40° and 140° have:', 'equal areas', ['different areas', 'no area', 'areas in ratio 40 : 140'], 'sin 40° = sin 140°.')],
    why=[('Explain why ½ab sin C works for any triangle.', 'b sin C is the perpendicular height from the vertex to side a, so the area is ½ × base × height.'),
         ('Explain why two different triangles can have the same two sides and the same area.', 'sin C = sin(180° − C), so an acute and an obtuse included angle give the same area.'),
         ('Explain why ½ab sin C gives ½ab for a right angle.', 'sin 90° = 1, so it reduces to ½ × base × height.')],
    misc=[('Area = ½ab sin C can use any angle of the triangle.', 'The angle must be between sides a and b (the included angle).'),
          ('If the area and two sides are known, the included angle is unique.', 'sin C = k has two solutions C and 180° − C.')],
))


@R.add('ch08-st4', 'C1', (1, 3), 'mcq')
def area_mcq(rng, slot):
    a, b = rng.randint(4, 20), rng.randint(4, 20)
    C = rng.choice([30, 40, 50, 65, 110, 130, 150])
    A = 0.5 * a * b * sind(C)
    return mcq(rng, f'Find the area of a triangle with sides {a} cm and {b} cm and included angle {C}° (3 s.f.).', f'{rsf(A, 3)} cm²',
               [f'{rsf(a * b * sind(C), 3)} cm²', f'{rsf(0.5 * a * b * cosd(C) if cosd(C) > 0 else 0.5 * a * b, 3)} cm²', f'{rsf(0.5 * a * b, 3)} cm²' if C != 90 else '0 cm²'], '½ab sin C.')


@R.add('ch08-st4', 'C3', (1, 4), 'short')
def area_calc(rng, slot):
    city, country, cur, cname = place(rng)
    a, b = rng.randint(5, 60), rng.randint(5, 60)
    C = rng.randint(20, 160)
    A = 0.5 * a * b * sind(C)
    if rng.random() < 0.5:
        pr = rng.choice([12, 18, 25, 40])
        return short(f'A triangular garden bed in {city} has sides {a} m and {b} m with an angle of {C}° between them. Find its area and the cost of turf at {money(cur, pr, 0)} per m².',
                     f'{rsf(A, 3)} m²; {cash(cur, A * pr)}', f'½ × {a} × {b} × sin {C}° (M1) = {rsf(A, 3)} m² (A1); cost {cash(cur, A * pr)} (A1).', 3)
    return short(f'Find the area of triangle XYZ with XY = {a} cm, XZ = {b} cm and angle YXZ = {C}°.', f'{rsf(A, 3)} cm²', f'½ × {a} × {b} × sin {C}° (M1 A1) = {rsf(A, 3)} cm² (A1).', 3)


@R.add('ch08-st4', 'C3', (2, 5), 'short')
def area_reverse(rng, slot):
    a, b = rng.randint(6, 20), rng.randint(6, 20)
    C = rng.randint(25, 80)
    A = round(0.5 * a * b * sind(C), 1)
    s = 2 * A / (a * b)
    if s >= 1:
        return None
    C1 = math.degrees(math.asin(s))
    if rng.random() < 0.5:
        return short(f'A triangle has area {g(A)} cm² and two sides {a} cm and {b} cm. Find the two possible values of the included angle, to 1 d.p.', f'{_dg(C1)} or {_dg(180 - C1)}',
                     f'sin C = 2 × {g(A)}/({a} × {b}) = {rsf(s, 4)} (M1 A1); {_dg(C1)} (A1); 180° − {_dg(C1)} (A1).', 4)
    side = 2 * A / (a * sind(C))
    return short(f'A triangle has area {g(A)} cm², one side {a} cm and an included angle of {C}°. Find the length of the other side enclosing the angle.', f'{rsf(side, 3)} cm',
                 f'{g(A)} = ½ × {a} × b × sin {C}° (M1); b = {rsf(side, 3)} cm (A1 A1).', 3)


@R.add('ch08-st4', 'C2', (2, 4), 'explain')
def area_explain(rng, slot):
    who = name(rng)
    a, b = rng.randint(5, 12), rng.randint(5, 12)
    C = rng.choice([30, 40, 50, 70])
    kind = rng.choice(['same', 'max', 'wrongangle'])
    if kind == 'same':
        return explain(f'Explain why triangles with sides {a} cm, {b} cm and included angles {C}° and {180 - C}° have the same area.',
                       f'sin {180 - C}° = sin {C}°, so ½ × {a} × {b} × sin C gives {rsf(0.5 * a * b * sind(C), 3)} cm² for both.', 'sin identity (R1); area (A1).', 2)
    if kind == 'max':
        return explain(f'{who} wants a triangular pen with two fences of {a} m and {b} m and the largest area. Explain which angle to use and find that area.',
                       f'Area = ½ab sin C is largest when sin C = 1, i.e. C = 90°: area = {g(0.5 * a * b)} m².', 'Max of sin (R1); area (A1).', 2)
    return explain(f'{who} finds the area of a triangle with sides {a} cm and {b} cm using an angle that is not between them. Explain why this is wrong.',
                   'The formula needs the included angle: b sin C is the height relative to side a only if C is between a and b.', 'Included angle (R1); height reasoning (R1).', 2)


@R.add('ch08-st4', 'C4', (3, 5), 'multi_step')
def area_task(rng, slot):
    city, country, cur, cname = place(rng)
    kind = rng.choice(['segment', 'quad', 'sail', 'hexagon'])
    if kind == 'segment':
        r = rng.randint(5, 20)
        th = rng.choice([40, 60, 80, 100, 120])
        sector = th / 360 * math.pi * r * r
        tri = 0.5 * r * r * sind(th)
        ans = f'(a) {rsf(sector, 4)} cm² (b) {rsf(tri, 4)} cm² (c) {rsf(sector - tri, 3)} cm² (d) {rsf((sector - tri) / (math.pi * r * r) * 100, 3)}% of the circle'
        q_ = (f'A logo in {city} is cut from a circle of radius {r} cm by a chord that subtends {th}° at the centre. (a) Find the area of the sector. (b) Find the area of the triangle formed by the chord and the radii. '
              f'(c) Find the area of the segment. (d) Express the segment as a percentage of the circle.')
    elif kind == 'quad':
        a, b, c, d = [rng.randint(20, 60) for _ in range(4)]
        A1, A2 = rng.randint(60, 120), rng.randint(60, 120)
        ar = 0.5 * a * b * sind(A1) + 0.5 * c * d * sind(A2)
        ans = f'(a) split along a diagonal into two triangles (b) {rsf(0.5 * a * b * sind(A1), 4)} m² and {rsf(0.5 * c * d * sind(A2), 4)} m² (c) {rsf(ar, 4)} m² (d) {cash(cur, ar * 4.5)} at {money(cur, 4.5)} per m²'
        q_ = (f'A plot in {city} is a quadrilateral ABCD with AB = {a} m, AD = {b} m, angle BAD = {A1}°, and CB = {c} m, CD = {d} m, angle BCD = {A2}°. (a) Explain how to split it to find its area. '
              f'(b) Find the area of each part. (c) Find the total area. (d) Find the cost of seeding it at {money(cur, 4.5)} per m².')
    elif kind == 'sail':
        a, b = rng.randint(3, 8), rng.randint(4, 10)
        C = rng.randint(35, 75)
        A = 0.5 * a * b * sind(C)
        third = math.sqrt(a * a + b * b - 2 * a * b * cosd(C))
        ans = f'(a) {rsf(A, 3)} m² (b) {rsf(third, 3)} m (c) {rsf(a + b + third, 3)} m of edging (d) at 90° the area would be {g(0.5 * a * b)} m², the largest possible'
        q_ = (f'A triangular sail for a boat in {city} has edges {a} m and {b} m meeting at {C}°. (a) Find the area. (b) Find the third edge. (c) Find the total length of edging tape. (d) Find the area if the angle were 90°, and comment.')
    else:
        s = rng.randint(4, 15)
        A = 6 * 0.5 * s * s * sind(60)
        ans = f'(a) 6 equilateral triangles (b) ½ × {s} × {s} × sin 60° = {rsf(A / 6, 4)} cm² (c) {rsf(A, 4)} cm² (d) exact: {sq(1, 3)} × {Fr(3 * s * s, 2)} = (3√3/2) × {s}² cm²'.replace(f'{sq(1, 3)} × {Fr(3 * s * s, 2)} = ', '')
        q_ = (f'A tile in {city} is a regular hexagon with side {s} cm. (a) Explain how to split it into congruent triangles. (b) Find the area of one triangle. (c) Find the area of the hexagon. (d) Write the area in exact form.')
    return short(q_, ans, f'{ans}. ½ab sin C applied (M1 A1); composite area organised (A1); context / exact value (D: R1); communication (C1).', 5, 'multi_step', 'G5')


R.facts('ch08-st5', F(
    terms=[('bearing', 'a direction measured clockwise from north, written as three digits, e.g. 075°'),
           ('back bearing', 'the bearing of the return journey: add or subtract 180°'),
           ('angle between a line and a plane', 'the angle between the line and its projection onto the plane')],
    facts=[('The bearing of A from B is 060°. The bearing of B from A is:', '240°', ['060°', '120°', '300°'], '60° + 180°.'),
           ('South-west is the bearing:', '225°', ['045°', '135°', '315°'], 'Halfway between 180° and 270°.'),
           ('In a cuboid, the space diagonal is found by:', 'Pythagoras twice', ['the sine rule only', 'adding the three edges', 'the area formula'], 'Base diagonal first, then the space diagonal.')],
    why=[('Explain why bearings are written with three figures.', 'It avoids confusion (e.g. 045° vs 45° vs 450°) and keeps a standard format from 000° to 359°.'),
         ('Explain why the back bearing differs by 180°.', 'Returning means facing the opposite direction, which is a half turn.'),
         ('Explain how to find the angle between a space diagonal and the base of a cuboid.', 'Form a right-angled triangle with the base diagonal and the vertical edge; use tan = height/base diagonal.')],
    misc=[('Bearings are measured anticlockwise from north.', 'They are measured clockwise from north.'),
          ('The bearing of A from B equals the bearing of B from A.', 'They differ by 180°.')],
))


def _brg(v):
    return f'{int(round(v)) % 360:03d}°'


@R.add('ch08-st5', 'C1', (1, 3), 'mcq')
def bearing_mcq(rng, slot):
    b = rng.randint(1, 35) * 10
    back = (b + 180) % 360
    return mcq(rng, f'The bearing of a lighthouse from a boat is {_brg(b)}. What is the bearing of the boat from the lighthouse?', _brg(back),
               [_brg(b), _brg(360 - b), _brg((b + 90) % 360)], f'{_brg(b)} ± 180°.')


@R.add('ch08-st5', 'C3', (1, 4), 'short')
def bearing_trip(rng, slot):
    city = rng.choice(SEA)
    d1, d2 = rng.randint(5, 40), rng.randint(5, 40)
    b1, b2 = rng.randint(0, 35) * 10, rng.randint(0, 35) * 10
    if (b2 - b1) % 180 == 0:
        return None
    x1, y1 = d1 * sind(b1), d1 * cosd(b1)
    x2, y2 = x1 + d2 * sind(b2), y1 + d2 * cosd(b2)
    dist = math.hypot(x2, y2)
    brg = math.degrees(math.atan2(x2, y2)) % 360
    back = (brg + 180) % 360
    return short(f'A yacht leaves a harbour near {city} and sails {d1} km on a bearing of {_brg(b1)}, then {d2} km on a bearing of {_brg(b2)}. Find its distance from the harbour and the bearing it must sail to return.',
                 f'{rsf(dist, 3)} km; bearing {_brg(back)}',
                 f'Angle in the triangle {r2(180 - abs((b2 - b1 + 180) % 360 - 180), 0)}° (M1); cosine rule {rsf(dist, 3)} km (A1); bearing of the yacht from the harbour {_brg(brg)} (A1); return bearing {_brg(back)} (A1).', 4)


@R.add('ch08-st5', 'C3', (2, 5), 'short')
def cuboid_3d(rng, slot):
    a, b, c = rng.randint(3, 15), rng.randint(3, 15), rng.randint(2, 12)
    base = math.hypot(a, b)
    sd = math.sqrt(a * a + b * b + c * c)
    ang = math.degrees(math.atan(c / base))
    obj, u = rng.choice([('shipping container', 'm'), ('storage room', 'm'), ('gift box', 'cm'), ('aquarium', 'dm'), ('lecture hall', 'm')])
    return short(f'{_a(obj).capitalize()} is a cuboid {a} {u} long, {b} {u} wide and {c} {u} high. Find the length of the space diagonal and the angle it makes with the base, to 3 s.f.',
                 f'{rsf(sd, 3)} {u}; {rsf(ang, 3)}°', f'Base diagonal √({a}² + {b}²) = {rsf(base, 4)} (M1 A1); space diagonal {rsf(sd, 3)} (A1); tan θ = {c}/{rsf(base, 4)}, θ = {rsf(ang, 3)}° (A1).', 4)


@R.add('ch08-st5', 'C2', (2, 4), 'explain')
def bearing_explain(rng, slot):
    who = name(rng)
    b = rng.randint(1, 17) * 10
    kind = rng.choice(['back', 'format', 'anticlock'])
    if kind == 'back':
        return explain(f'{who} says that if B is on a bearing of {_brg(b)} from A, then A is on a bearing of {_brg(b)} from B. Explain why this is wrong.',
                       f'The direction from B back to A is opposite, a half turn: {_brg(b + 180)}.', 'Opposite direction (R1); back bearing (A1).', 2)
    if kind == 'format':
        return explain(f'Explain why a navigator writes {_brg(b % 100 if b % 100 else 50)} rather than {b % 100 if b % 100 else 50}° for a bearing.', 'Bearings use three figures so that every direction has a standard, unambiguous form from 000° to 359°.', 'Three figures (R1); reason (R1).', 2)
    return explain(f'{who} measures a bearing of {_brg(b)} anticlockwise from north. Explain the error and the correct direction.',
                   f'Bearings are clockwise from north; {b}° anticlockwise is actually a bearing of {_brg(360 - b)}.', 'Convention (R1); corrected bearing (A1).', 2)


@R.add('ch08-st5', 'C4', (3, 5), 'multi_step')
def bearing_task(rng, slot):
    city = rng.choice(SEA)
    kind = rng.choice(['rescue', 'pyramid', 'flight', 'hill'])
    if kind == 'rescue':
        d1, d2 = rng.randint(10, 40), rng.randint(10, 40)
        b1, b2 = rng.choice([20, 40, 50, 70]), rng.choice([110, 130, 150, 160])
        ang = b2 - b1
        d = math.sqrt(d1 * d1 + d2 * d2 - 2 * d1 * d2 * cosd(ang))
        # bearing from boat A to boat B
        xa, ya = d1 * sind(b1), d1 * cosd(b1)
        xb, yb = d2 * sind(b2), d2 * cosd(b2)
        brg = math.degrees(math.atan2(xb - xa, yb - ya)) % 360
        ans = f'(a) {ang}° (b) {rsf(d, 3)} km (c) {_brg(brg)} (d) {rsf(d / 30 * 60, 3)} minutes at 30 km/h'
        q_ = (f'From a coastguard station near {city}, boat A is {d1} km away on a bearing of {_brg(b1)} and boat B is {d2} km away on a bearing of {_brg(b2)}. (a) Find the angle AOB at the station. '
              f'(b) Find the distance AB. (c) Find the bearing of B from A. (d) How long would A take to reach B at 30 km/h?')
    elif kind == 'pyramid':
        s, h = rng.randint(6, 20), rng.randint(5, 18)
        half_d = s * math.sqrt(2) / 2
        edge = math.hypot(half_d, h)
        ang = math.degrees(math.atan(h / half_d))
        face = math.degrees(math.atan(h / (s / 2)))
        ans = f'(a) {rsf(2 * half_d, 3)} m (b) {rsf(edge, 3)} m (c) {rsf(ang, 3)}° (d) {rsf(face, 3)}°'
        q_ = (f'A glass pyramid in {city} has a square base of side {s} m and its top is {h} m directly above the centre of the base. (a) Find the length of a diagonal of the base. (b) Find the length of a sloping edge. '
              f'(c) Find the angle between a sloping edge and the base. (d) Find the angle between a triangular face and the base.')
    elif kind == 'flight':
        d1, d2 = rng.randint(100, 400), rng.randint(100, 400)
        b1, b2 = rng.choice([(30, 120), (60, 150), (45, 160), (300, 40), (200, 290)])
        x = d1 * sind(b1) + d2 * sind(b2)
        yv = d1 * cosd(b1) + d2 * cosd(b2)
        dist = math.hypot(x, yv)
        brg = math.degrees(math.atan2(x, yv)) % 360
        ans = f'(a) a sketch with both legs (b) {rsf(dist, 3)} km (c) {_brg(brg)} (d) {_brg(brg + 180)}'
        q_ = (f'A drone flies {d1} m from a base in {city} on a bearing of {_brg(b1)}, then {d2} m on a bearing of {_brg(b2)}. (a) Sketch the journey. (b) Find the direct distance from the base. '
              f'(c) Find the bearing of the drone from the base. (d) Find the bearing it must fly to return.').replace('km', 'm')
        ans = ans.replace(' km', ' m')
    else:
        d = rng.randint(200, 800)
        e1, e2 = rng.randint(8, 15), rng.randint(18, 30)
        # observer walks d towards hill; elevations e1 then e2
        apex = e2 - e1
        L = d * sind(e1) / sind(apex)
        h = L * sind(e2)
        ans = f'(a) {apex}° (b) {rsf(L, 3)} m (c) {rsf(h, 3)} m (d) horizontal distance from the second point {rsf(L * cosd(e2), 3)} m'
        q_ = (f'A hiker near {city} sees the summit of a hill at an angle of elevation of {e1}°. After walking {d} m directly towards it on level ground, the angle is {e2}°. (a) Find the angle at the summit in the triangle formed. '
              f'(b) Find the distance from the second point to the summit. (c) Find the height of the hill. (d) Find the remaining horizontal distance to the point below the summit.')
    return short(q_, ans, f'{ans}. Diagram / angles correctly identified (A1); sine or cosine rule and Pythagoras applied (M1 A1); bearings in three-figure form (C1); interpretation (D: R1).', 6, 'multi_step', 'G5')


# =============================================================================================
# ch09 Trigonometric Functions and Graphs (Extended)
# =============================================================================================
R.facts('ch09-st1', F(
    terms=[('radian', 'the angle at the centre of a circle subtended by an arc equal in length to the radius; π radians = 180°'),
           ('arc length (radians)', 'the formula s = rθ, where θ is in radians'),
           ('sector area (radians)', 'A = ½r²θ, where θ is in radians')],
    facts=[('Convert 90° to radians.', 'π/2', ['π/4', '2π', '90π'], '90 × π/180.'),
           ('Convert 2π/3 radians to degrees.', '120°', ['60°', '240°', '150°'], '2/3 × 180.'),
           ('A sector has r = 6 cm and θ = 1.5 rad. Its arc length is:', '9 cm', ['27 cm', '4 cm', '54 cm'], 's = rθ.')],
    why=[('Explain why one full turn is 2π radians.', 'The whole circumference is 2πr, which is 2π radius-lengths of arc, so the angle is 2π radians.'),
         ('Explain why the arc-length formula is simpler in radians.', 'By definition an angle of θ radians cuts off an arc of θ radii, so s = rθ with no extra fraction of 360°.'),
         ('Explain why 1 radian is a little less than 60°.', '1 rad = 180°/π ≈ 57.3°, because π is a bit more than 3.')],
    misc=[('s = rθ works with θ in degrees.', 'θ must be in radians; in degrees use s = θ/360 × 2πr.'),
          ('π radians = 360°.', 'π radians = 180°; a full turn is 2π.')],
))


@R.add('ch09-st1', 'C1', (1, 3), 'mcq')
def radian_mcq(rng, slot):
    deg = rng.choice([30, 45, 60, 120, 135, 150, 210, 225, 240, 270, 300, 315])
    r = Fr(deg, 180)
    txt = lambda q: ('' if q.numerator == 1 else str(q.numerator)) + 'π' + ('' if q.denominator == 1 else f'/{q.denominator}')
    wr = [txt(Fr(deg, 360)), txt(Fr(180, deg)) if Fr(180, deg).numerator < 20 else txt(r * 2), txt(r * 2)]
    wr = [w for w in dict.fromkeys(wr) if w != txt(r)]
    while len(wr) < 3:
        wr.append(txt(r + Fr(1, 6)))
    return mcq(rng, f'Convert {deg}° to radians.', txt(r), wr[:3], f'{deg} × π/180 = {txt(r)}.')


def _pi(q) -> str:
    """Exact multiple of π, e.g. 4π, 3π/2, π/6."""
    q = Fr(q)
    n = '' if q.numerator == 1 else str(q.numerator)
    return f'{n}π' + ('' if q.denominator == 1 else f'/{q.denominator}')


@R.add('ch09-st1', 'C3', (1, 4), 'short')
def arc_sector(rng, slot):
    r = rng.randint(3, 25)
    th = round(rng.uniform(0.3, 5.5), 1) if rng.random() < 0.6 else None
    if th is None:
        q = rng.choice([Fr(1, 6), Fr(1, 4), Fr(1, 3), Fr(2, 3), Fr(3, 4), Fr(5, 6), Fr(5, 4)])
        tht = ('' if q.numerator == 1 else str(q.numerator)) + 'π' + ('' if q.denominator == 1 else f'/{q.denominator}')
        s, A = r * float(q) * math.pi, 0.5 * r * r * float(q) * math.pi
        return short(f'A sector has radius {r} cm and angle {tht} radians. Find the arc length and the area, in exact form and to 3 s.f.', f'arc {_pi(q * r)} ≈ {rsf(s, 3)} cm; area {_pi(q * r * r / 2)} ≈ {rsf(A, 3)} cm²',
                     f's = rθ = {r} × {tht} (M1) ≈ {rsf(s, 3)} cm (A1); A = ½r²θ (M1) ≈ {rsf(A, 3)} cm² (A1).', 4)
    s, A = r * th, 0.5 * r * r * th
    return short(f'A sector has radius {r} cm and angle {g(th)} radians. Find its arc length, area and perimeter.', f'arc {rsf(s, 3)} cm; area {rsf(A, 3)} cm²; perimeter {rsf(s + 2 * r, 3)} cm',
                 f's = {r} × {g(th)} (A1); A = ½ × {r}² × {g(th)} (A1); perimeter = s + 2r (A1).', 3)


@R.add('ch09-st1', 'C3', (2, 5), 'short')
def sector_reverse(rng, slot):
    r = rng.randint(4, 20)
    th = round(rng.uniform(0.4, 3), 2)
    if rng.random() < 0.5:
        s = round(r * th, 1)
        return short(f'An arc of length {g(s)} cm lies on a circle of radius {r} cm. Find the angle at the centre in radians (3 s.f.) and in degrees (1 d.p.).', f'{rsf(s / r, 3)} rad; {_dg(math.degrees(s / r))}',
                     f'θ = s/r = {g(s)}/{r} (M1) = {rsf(s / r, 3)} rad (A1); × 180/π = {_dg(math.degrees(s / r))} (A1).', 3)
    A = round(0.5 * r * r * th, 1)
    P = r * th + 2 * r
    return short(f'A sector of a circle of radius {r} cm has area {g(A)} cm². Find the angle in radians and the perimeter of the sector, to 3 s.f.', f'{rsf(2 * A / (r * r), 3)} rad; perimeter {rsf(r * 2 * A / (r * r) + 2 * r, 3)} cm',
                 f'θ = 2A/r² (M1) = {rsf(2 * A / (r * r), 3)} (A1); perimeter rθ + 2r = {rsf(r * 2 * A / (r * r) + 2 * r, 3)} cm (A1).', 3)


@R.add('ch09-st1', 'C2', (2, 4), 'explain')
def radian_explain(rng, slot):
    who = name(rng)
    r, d = rng.randint(4, 12), rng.choice([30, 45, 60, 90, 120])
    kind = rng.choice(['deg', 'def', 'compare'])
    if kind == 'deg':
        return explain(f'{who} finds the arc length of a {d}° sector of radius {r} cm as s = {r} × {d} = {r * d} cm. Explain the error and correct it.',
                       f's = rθ needs θ in radians: {d}° = {rsf(math.radians(d), 4)} rad, so s ≈ {rsf(r * math.radians(d), 3)} cm.', 'Units (R1); correct value (A1).', 2)
    if kind == 'def':
        return explain(f'Explain what an angle of 1 radian looks like on a circle of radius {r} cm.', f'It is the angle at the centre for an arc of length {r} cm – one radius laid along the circle.', 'Definition (R1); arc = radius (A1).', 2)
    return explain(f'Explain, without a calculator, whether 2 radians is more or less than 120°.', '1 rad ≈ 57.3°, so 2 rad ≈ 114.6°, which is less than 120°.', 'Conversion (A1); comparison (R1).', 2)


@R.add('ch09-st1', 'C4', (3, 5), 'multi_step')
def radian_task(rng, slot):
    city, country, cur, cname = place(rng)
    kind = rng.choice(['pizza', 'wiper', 'track', 'pendulum'])
    if kind == 'pizza':
        r = rng.choice([15, 18, 20, 23])
        n = rng.choice([6, 8, 10, 12])
        th = 2 * math.pi / n
        ans = f'(a) 2π/{n} = {rsf(th, 3)} rad (b) {rsf(0.5 * r * r * th, 3)} cm² (c) crust {rsf(r * th, 3)} cm (d) {cash(cur, rng.choice([12, 15, 18]) / n)} per slice'.replace('per slice', 'per slice')
        price = rng.choice([12, 15, 18])
        ans = f'(a) 2π/{n} ≈ {rsf(th, 3)} rad (b) {rsf(0.5 * r * r * th, 3)} cm² (c) crust {rsf(r * th, 3)} cm (d) {cash(cur, price / n)} per slice; {cash(cur, price / (math.pi * r * r) * 100)} per 100 cm²'
        q_ = (f'A pizzeria in {city} cuts a pizza of radius {r} cm into {n} equal slices and sells the pizza for {money(cur, price, 0)}. (a) Find the angle of each slice in radians. (b) Find the area of a slice. '
              f'(c) Find the length of crust on a slice. (d) Find the price per slice and per 100 cm².')
    elif kind == 'wiper':
        L, blade = rng.choice([(50, 40), (60, 45), (55, 35)])
        th = rng.choice([100, 110, 120, 135])
        t = math.radians(th)
        ans = f'(a) {rsf(t, 3)} rad (b) {rsf(L * t, 3)} cm (c) {rsf(0.5 * (L * L - (L - blade) ** 2) * t, 4)} cm² (d) the area is the difference of two sectors'
        q_ = (f'A windscreen wiper on a bus in {city} has an arm of length {L} cm, with a {blade} cm rubber blade at the outer end, and turns through {th}°. (a) Convert the angle to radians. (b) Find the distance moved by the tip. '
              f'(c) Find the area cleaned. (d) Explain your method for (c).')
    elif kind == 'track':
        r = rng.choice([30, 36, 40, 45])
        st = rng.choice([80, 85, 100])
        lap = 2 * st + 2 * math.pi * r
        ans = f'(a) each bend is π rad (b) {rsf(math.pi * r, 4)} m per bend (c) lap {rsf(lap, 4)} m (d) {rsf(lap + 2 * math.pi * 1.22, 4)} m for the next lane (radius +1.22 m): {rsf(2 * math.pi * 1.22, 3)} m longer'
        q_ = (f'A running track in {city} has two straights of {st} m and two semicircular bends of radius {r} m on the inside lane. (a) State the angle of each bend in radians. (b) Find the length of one bend. '
              f'(c) Find the length of a lap. (d) Find how much longer a lap is in a lane 1.22 m further out, and explain why staggered starts are used.')
    else:
        L = rng.choice([0.8, 1, 1.2, 1.5, 2])
        th = rng.choice([10, 15, 20, 25, 30])
        t = math.radians(2 * th)
        ans = f'(a) {2 * th}° = {rsf(t, 3)} rad (b) {rsf(L * t, 3)} m per swing (c) {rsf(L * t * 100, 3)} m in 100 swings (d) the swing angle decreases because of friction'
        q_ = (f'A pendulum in a science museum in {city} is {g(L)} m long and swings {th}° each side of the vertical. (a) Find the total angle of a swing in radians. (b) Find the arc length of one swing. '
              f'(c) Find the distance the bob travels in 100 swings. (d) Explain why this answer is an overestimate in practice.')
    return short(q_, ans, f'{ans}. Radians used (A1); arc / sector formulas (M1 A1 A1); interpreted in context (D: R1).', 5, 'multi_step', 'G5')


R.facts('ch09-st2', F(
    terms=[('amplitude', 'half the distance between the maximum and minimum values of a sinusoidal graph: |a| in y = a sin(b(x − c)) + d'),
           ('period', 'the horizontal length of one complete cycle: 360°/b (or 2π/b in radians)'),
           ('principal axis', 'the horizontal line y = d about which a sine or cosine graph oscillates')],
    facts=[('The amplitude of y = 3 sin 2x is:', '3', ['2', '6', '1.5'], '|a| = 3.'),
           ('The period of y = sin 3x (degrees) is:', '120°', ['3°', '360°', '1080°'], '360°/3.'),
           ('The principal axis of y = 2 cos x + 5 is:', 'y = 5', ['y = 2', 'y = 7', 'y = 0'], 'Vertical translation 5.')],
    why=[('Explain why y = sin x has period 360°.', 'The point on the unit circle returns to the same position after a full turn, so the values repeat every 360°.'),
         ('Explain why y = tan x has vertical asymptotes at x = 90° and 270°.', 'tan x = sin x/cos x and cos x = 0 there, so the function is undefined and its values grow without bound.'),
         ('Explain why the graph of y = cos x is the graph of y = sin x translated 90° to the left.', 'cos x = sin(x + 90°), so the cosine graph is the sine graph shifted 90° left.')],
    misc=[('y = sin 2x has period 720°.', 'Multiplying x by 2 compresses the graph: the period is 180°.'),
          ('The amplitude of y = −4 sin x is −4.', 'The amplitude is a distance, |−4| = 4; the minus reflects the graph.')],
))


@R.add('ch09-st2', 'C1', (1, 3), 'mcq')
def trig_graph_mcq(rng, slot):
    a, b, d = rng.choice([2, 3, 4, 5, 0.5]), rng.choice([2, 3, 4, 6]), rng.randint(-3, 6)
    fn = rng.choice(['sin', 'cos'])
    corr = f'amplitude {g(a)}, period {g(360 / b)}°, principal axis y = {m(d)}'
    wr = [f'amplitude {g(a)}, period {g(360 * b)}°, principal axis y = {m(d)}', f'amplitude {b}, period {g(360 / a, 4)}°, principal axis y = {m(d)}', f'amplitude {g(2 * a)}, period {g(360 / b)}°, principal axis y = 0']
    return mcq(rng, f'For y = {g(a)} {fn} {b}x{sgn(d) if d else ""} (x in degrees), which is correct?', corr, wr, f'a = {g(a)}, period 360°/{b}, axis y = {m(d)}.')


@R.add('ch09-st2', 'C3', (1, 4), 'short')
def trig_graph_features(rng, slot):
    a, b, d = rng.choice([2, 3, 4, 5, 10]), rng.choice([1, 2, 3, 4, Fr(1, 2)]), rng.randint(-4, 8)
    fn = rng.choice(['sin', 'cos'])
    rad = slot.d >= 3 and rng.random() < 0.5
    per = (Fr(2, 1) / Fr(b)) if rad else 360 / Fr(b)
    per_t = (f'{fx(per)}π'.replace('1π', 'π') if rad else f'{fx(per)}°')
    btxt = '' if b == 1 else (f'{fx(b)}' if Fr(b).denominator == 1 else f'({fx(b)})')
    return short(f'For y = {a} {fn}({btxt}x){sgn(d) if d else ""} (x in {"radians" if rad else "degrees"}), state the amplitude, period, principal axis, and the maximum and minimum values.',
                 f'amplitude {a}; period {per_t}; axis y = {m(d)}; max {m(d + a)}, min {m(d - a)}',
                 f'Amplitude (A1); period {"2π" if rad else "360°"}/{fx(b)} (A1); axis (A1); max/min (A1).', 4)


@R.add('ch09-st2', 'C3', (2, 5), 'short')
def trig_graph_from_info(rng, slot):
    mx = rng.randint(4, 20)
    mn = mx - 2 * rng.randint(1, 6)
    per = rng.choice([90, 120, 180, 360, 720])
    a, d, b = Fr(mx - mn, 2), Fr(mx + mn, 2), Fr(360, per)
    fn = rng.choice(['sin', 'cos'])
    return short(f'A {fn}-type graph y = a {fn}(bx) + d (x in degrees, a, b > 0) has maximum {mx}, minimum {mn} and period {per}°. Find a, b and d.', f'a = {fx(a)}, b = {fx(b)}, d = {fx(d)}',
                 f'a = ({mx} − {m(mn)})/2 (A1); d = ({mx} + {m(mn)})/2 (A1); b = 360/{per} (A1).', 3)


@R.add('ch09-st2', 'C2', (2, 4), 'explain')
def trig_graph_explain(rng, slot):
    who = name(rng)
    b = rng.choice([2, 3, 4])
    kind = rng.choice(['period', 'amp', 'tan'])
    if kind == 'period':
        return explain(f'{who} says y = sin {b}x has period {360 * b}°. Explain the error.', f'Multiplying x by {b} makes the cycle happen {b} times as fast: period 360°/{b} = {360 // b}°.', 'Effect of b (R1); period (A1).', 2)
    if kind == 'amp':
        a = rng.randint(2, 6)
        return explain(f'Explain why y = {a} sin x + {a + 1} never takes negative values.', f'sin x ranges from −1 to 1, so y ranges from {a + 1} − {a} = 1 to {2 * a + 1}; the minimum 1 is positive.', 'Range of sin (R1); min value (A1).', 2)
    return explain(f'Explain why y = tan x has period 180° rather than 360°.', 'tan(x + 180°) = sin(x + 180°)/cos(x + 180°) = (−sin x)/(−cos x) = tan x.', 'Signs (R1); conclusion (R1).', 2)


@R.add('ch09-st2', 'C4', (3, 5), 'multi_step')
def trig_graph_task(rng, slot):
    city = rng.choice(CITIES)
    kind = rng.choice(['family', 'ac', 'compare', 'tan'])
    if kind == 'family':
        bs = [1, 2, 3]
        ans = f'(a) periods 360°, 180°, 120° (b) period = 360°/b (c) b = {rng.choice([4, 5, 6])}: …'
        bb = rng.choice([4, 5, 6, 8])
        ans = f'(a) periods 360°, 180°, 120° (b) period = 360°/b (c) y = sin {bb}x has period {g(360 / bb, 4)}° (d) b = {g(360 / 72)} gives period 72°'
        q_ = (f'Investigate y = sin bx for b = {", ".join(map(str, bs))}. (a) Find the period of each. (b) Describe the pattern as a rule. (c) Predict the period of y = sin {bb}x. (d) Find b for a period of 72°.')
    elif kind == 'ac':
        V = rng.choice([230, 120, 240])
        f = rng.choice([50, 60])
        ans = f'(a) amplitude {V}√2 ≈ {rsf(V * math.sqrt(2), 3)} V (b) period 1/{f} s = {rsf(1000 / f, 3)} ms (c) b = 2π × {f} = {rsf(2 * math.pi * f, 4)} (d) V = {rsf(V * math.sqrt(2), 3)} sin({rsf(2 * math.pi * f, 4)}t)'
        q_ = (f'Mains electricity in a country visited from {city} is {V} V (rms) at {f} Hz; the peak voltage is √2 times the rms value. (a) Find the amplitude. (b) Find the period. '
              f'(c) Find b in V = a sin(bt) with t in seconds (radians). (d) Write the model.')
    elif kind == 'compare':
        a1, a2 = rng.randint(2, 5), rng.randint(2, 5)
        ans = f'(a) {a1} sin x: amplitude {a1}, period 360° (b) sin {a2}x: amplitude 1, period {g(360 / a2, 4)}° (c) {a1} is a vertical stretch; {a2} a horizontal stretch by 1/{a2} (d) y = {a1} sin {a2}x has amplitude {a1} and period {g(360 / a2, 4)}°'
        q_ = (f'Compare y = {a1} sin x and y = sin {a2}x. (a) State the amplitude and period of the first. (b) State them for the second. (c) Describe each as a transformation of y = sin x. (d) Predict the features of y = {a1} sin {a2}x.')
    else:
        b = rng.choice([2, 3])
        ans = f'(a) period 180°/{b} = {g(180 / b, 4)}° (b) asymptotes at x = {g(90 / b, 4)}° + k × {g(180 / b, 4)}° (c) zeros at x = k × {g(180 / b, 4)}° (d) tan has no amplitude because it is unbounded'
        q_ = (f'Investigate y = tan {b}x for x in degrees. (a) Find the period. (b) Find the equations of the asymptotes. (c) Find the zeros. (d) Explain why we do not state an amplitude for tan.')
    return short(q_, ans, f'{ans}. Amplitude / period / axis identified (A1 A1); rule generalised (B: R1); model or prediction (A1); communication (C1).', 5, 'multi_step', 'G5')


R.facts('ch09-st3', F(
    terms=[('periodic phenomenon', 'a real-world quantity that repeats in regular cycles, such as tides, daylight hours or a Ferris-wheel height'),
           ('sinusoidal model', 'a model of the form y = a sin(b(t − c)) + d or y = a cos(b(t − c)) + d'),
           ('phase shift', 'the horizontal translation c in y = a sin(b(t − c)) + d')],
    facts=[('For a tide with high water 5 m and low water 1 m, the amplitude is:', '2 m', ['4 m', '3 m', '6 m'], '(5 − 1)/2.'),
           ('For daylight hours repeating every 365 days, b (in degrees per day) is:', '360/365', ['365/360', '365', '1/365'], 'b = 360°/period.'),
           ('The principal axis of a tide model with max 5 m and min 1 m is:', 'y = 3', ['y = 2', 'y = 4', 'y = 5'], '(5 + 1)/2.')],
    why=[('Explain why a cosine model is often convenient when the data start at a maximum.', 'cos 0 = 1 is the maximum, so no horizontal shift is needed.'),
         ('Explain why the period of a tide model is not 24 hours.', 'Tides follow the Moon; high tides occur about every 12.4 hours.'),
         ('Explain how to find d from the maximum and minimum values.', 'The principal axis is halfway between them: d = (max + min)/2.')],
    misc=[('The amplitude of a model with max 20 and min 4 is 16.', 'Amplitude is half the range: 8.'),
          ('A sinusoidal model can predict the weather exactly years ahead.', 'It describes average periodic behaviour; real data vary.')],
))


@R.add('ch09-st3', 'C1', (1, 3), 'mcq')
def model_mcq(rng, slot):
    mx = rng.randint(6, 30)
    mn = rng.randint(0, mx - 2)
    return mcq(rng, f'A periodic quantity varies between a maximum of {mx} and a minimum of {mn}. What are the amplitude and principal axis?', f'amplitude {g((mx - mn) / 2)}, axis y = {g((mx + mn) / 2)}',
               [f'amplitude {mx - mn}, axis y = {g((mx + mn) / 2)}', f'amplitude {g((mx + mn) / 2)}, axis y = {g((mx - mn) / 2)}', f'amplitude {g((mx - mn) / 2)}, axis y = {mx - mn}'], 'Half the range; midpoint.')


@R.add('ch09-st3', 'C3', (1, 4), 'short')
def model_build(rng, slot):
    city = rng.choice(SEA)
    kind = rng.choice(['tide', 'wheel', 'daylight'])
    if kind == 'tide':
        hi, lo = round(rng.uniform(3, 7), 1), round(rng.uniform(0.3, 2), 1)
        per = 12
        t0 = rng.randint(0, 6)
        a, d = (hi - lo) / 2, (hi + lo) / 2
        return short(f'In the harbour at {city}, high tide is {g(hi)} m at {t0}:00 and low tide is {g(lo)} m six hours later; the pattern repeats every 12 hours. Write a model h = a cos(b(t − c)) + d, with t in hours and b in degrees per hour.',
                     f'h = {g(a, 3)} cos(30(t − {t0})) + {g(d, 3)}', f'a = {g(a, 3)} (A1); b = 360/12 = 30 (A1); c = {t0} (max) (A1); d = {g(d, 3)} (A1).', 4)
    if kind == 'wheel':
        r, hub, T = rng.choice([(20, 22, 10), (30, 33, 15), (16, 18, 8), (60, 65, 30)])
        return short(f'A Ferris wheel in {city} has radius {r} m, its hub is {hub} m above the ground and it turns once every {T} minutes. A rider starts at the bottom. Write a model for the height h after t minutes, with b in degrees per minute.',
                     f'h = −{r} cos({g(360 / T, 4)}t) + {hub}', f'a = {r}, reflected since it starts at the minimum (A1 R1); b = 360/{T} (A1); d = {hub} (A1).', 4)
    mx, mn = round(rng.uniform(13, 18), 1), round(rng.uniform(6, 11), 1)
    peak = rng.choice([172, 173, 355])
    return short(f'In {city} the daylight varies from {g(mx)} hours (day {peak}) to {g(mn)} hours, with a period of 365 days. Write a model D = a cos(b(t − c)) + d with b in degrees per day.',
                 f'D = {g((mx - mn) / 2, 3)} cos({g(360 / 365, 3)}(t − {peak})) + {g((mx + mn) / 2, 3)}', f'a (A1); b = 360/365 (A1); c = {peak} (A1); d (A1).', 4)


@R.add('ch09-st3', 'C3', (2, 5), 'short')
def model_use(rng, slot):
    a, d = rng.randint(2, 8), rng.randint(10, 20)
    T = rng.choice([12, 24, 10, 20])
    b = 360 / T
    t = rng.randint(1, T - 1)
    h = a * math.cos(math.radians(b * t)) + d
    level = d + rng.choice([-1, 1]) * round(a * rng.uniform(0.2, 0.8), 1)
    cnt = sum(1 for s in range(0, T * 100) if a * math.cos(math.radians(b * s / 100)) + d > level) / 100
    return short(f'The depth of water at a jetty is D = {a} cos({g(b, 4)}t) + {d} metres, t hours after midnight. (a) Find D at t = {t}. (b) For how long in each {T}-hour cycle is the depth more than {g(level)} m?',
                 f'(a) {rsf(h, 3)} m (b) about {rsf(cnt, 2)} hours', f'Substitution (A1); solve D = {g(level)} for the boundary times (M1 A1); duration (A1).', 4)


@R.add('ch09-st3', 'C2', (2, 4), 'explain')
def model_explain(rng, slot):
    who = name(rng)
    kind = rng.choice(['amp', 'period', 'start'])
    mx, mn = rng.randint(10, 30), rng.randint(1, 9)
    if kind == 'amp':
        return explain(f'{who} models a quantity with max {mx} and min {mn} using amplitude {mx - mn}. Explain the error.', f'The amplitude is half the distance from max to min: ({mx} − {mn})/2 = {g((mx - mn) / 2)}.', 'Definition (R1); value (A1).', 2)
    if kind == 'period':
        T = rng.choice([12, 24, 365])
        return explain(f'Explain how the period of {T} {"days" if T == 365 else "hours"} determines b in a model y = a sin(bt) + d with b in degrees.', f'One cycle must be 360°, so b × {T} = 360 and b = 360/{T} ≈ {rsf(360 / T, 3)}.', 'Cycle = 360° (R1); b (A1).', 2)
    return explain(f'A rider on a Ferris wheel starts at the lowest point. Explain why −a cos(bt) + d is a better model than a sin(bt) + d.',
                   'At t = 0, −cos 0 = −1 gives the minimum height d − a; sin 0 = 0 would start at the middle height.', 'Initial value (R1); comparison (R1).', 2)


@R.add('ch09-st3', 'C4', (3, 5), 'multi_step')
def model_task(rng, slot):
    city = rng.choice(SEA)
    kind = rng.choice(['temp', 'tide', 'wheel', 'spring'])
    if kind == 'temp':
        mx, mn = rng.randint(24, 34), rng.randint(2, 15)
        a, d = (mx - mn) / 2, (mx + mn) / 2
        m_ = rng.randint(1, 12)
        T = -a * math.cos(math.radians(30 * (m_ - 1))) + d
        ans = f'(a) a = {g(a)}, d = {g(d)} (b) b = 30 (c) T = −{g(a)} cos(30(t − 1)) + {g(d)} (d) month {m_}: {rsf(T, 3)} °C'
        q_ = (f'The mean monthly temperature in {city} ranges from {mn} °C in January (t = 1) to {mx} °C in July (t = 7). (a) Find the amplitude and principal axis. (b) Find b (degrees per month). '
              f'(c) Write a model using cosine. (d) Use it to estimate the temperature in month {m_}.')
    elif kind == 'tide':
        hi, lo = round(rng.uniform(4, 8), 1), round(rng.uniform(0.5, 2), 1)
        need = round((hi + lo) / 2 + rng.uniform(-0.8, 0.8), 1)
        a, d = (hi - lo) / 2, (hi + lo) / 2
        frac_ = math.degrees(math.acos((need - d) / a)) / 180
        dur = 12.4 * frac_
        ans = f'(a) h = {g(a, 3)} cos({g(360 / 12.4, 4)}t) + {g(d, 3)} (b) {rsf(dur, 3)} hours per cycle with h > {g(need)} m (c) safe windows start every 12.4 hours (d) weather and storm surges change the tide'
        q_ = (f'A ferry at {city} needs at least {g(need)} m of water. High tide ({g(hi)} m) is at t = 0 and low tide is {g(lo)} m; the period is 12.4 hours. (a) Write a model for the depth h. '
              f'(b) For how long in each cycle can the ferry enter? (c) Describe how often these windows occur. (d) Give one reason the model might be inaccurate.')
    elif kind == 'wheel':
        r, hub, T = rng.choice([(20, 22, 10), (30, 33, 15), (67.5, 70, 32)])
        t = rng.randint(1, T - 1)
        h = -r * math.cos(math.radians(360 / T * t)) + hub
        above = hub + r * 0.5
        frac_ = 1 / 3
        ans = f'(a) h = −{g(r)} cos({g(360 / T, 4)}t) + {g(hub)} (b) {rsf(h, 3)} m (c) above {g(above)} m for {rsf(T * frac_, 3)} minutes per turn (d) max {g(hub + r)} m at t = {g(T / 2)} min'
        q_ = (f'The wheel in {city} has radius {g(r)} m, hub {g(hub)} m above the ground and turns once every {T} minutes; you board at the bottom. (a) Write a model for your height. (b) Find the height after {t} minutes. '
              f'(c) For how long per turn are you more than {g(above)} m high? (d) State the maximum height and when it first occurs.')
    else:
        a, T = rng.choice([4, 5, 6]), rng.choice([2, 3, 4])
        ans = f'(a) a = {a} cm (b) b = 360/{T} = {g(360 / T, 4)} (c) y = {a} cos({g(360 / T, 4)}t) (d) in practice the amplitude decreases (damping)'
        q_ = (f'A mass on a spring in a physics lab in {city} is pulled {a} cm down and released; it oscillates with a period of {T} s. (a) State the amplitude. (b) Find b in degrees per second. '
              f'(c) Write a model for the displacement y below the rest position. (d) Explain one way the real motion differs from the model.')
    return short(q_, ans, f'{ans}. Parameters found from the context (A1 A1); model written (M1); used to answer the question (A1); limitations discussed (D: R1).', 6, 'multi_step', 'G5')


R.facts('ch09-st4', F(
    terms=[('trigonometric equation', 'an equation involving a trigonometric function of an unknown angle, such as 2 sin x = 1'),
           ('principal value', 'the value given by a calculator inverse function, e.g. sin⁻¹ gives an angle between −90° and 90°'),
           ('general solution in an interval', 'all solutions within a given domain, found using symmetry and the period')],
    facts=[('Solve sin x = 0.5 for 0° ≤ x ≤ 360°.', 'x = 30° or 150°', ['x = 30° only', 'x = 60° or 120°', 'x = 30° or 330°'], 'sin is positive in quadrants 1 and 2.'),
           ('Solve cos x = −1 for 0° ≤ x ≤ 360°.', 'x = 180°', ['x = 0°', 'x = 90°', 'x = 270°'], 'cos 180° = −1.'),
           ('tan x = 1 for 0° ≤ x ≤ 360° has solutions:', '45° and 225°', ['45° only', '45° and 135°', '45° and 315°'], 'Period 180°.')],
    why=[('Explain why sin x = 0.3 has two solutions between 0° and 360°.', 'Sine is positive in the first and second quadrants, so x = sin⁻¹ 0.3 and 180° − sin⁻¹ 0.3.'),
         ('Explain why sin x = 1.5 has no solutions.', 'The sine of any angle lies between −1 and 1.'),
         ('Explain how to solve sin 2x = 0.5 for 0° ≤ x ≤ 360°.', 'Let u = 2x with 0° ≤ u ≤ 720°; find all u (30°, 150°, 390°, 510°), then halve: x = 15°, 75°, 195°, 255°.')],
    misc=[('The calculator answer to sin⁻¹ 0.6 is the only solution.', 'In 0°–360° there is also 180° − 36.9° = 143.1°.'),
          ('cos x = 0.4 gives x = 66.4° and 180° − 66.4°.', 'For cosine the second solution is 360° − 66.4° = 293.6°.')],
))


def _solve_trig(fn, k, lo=0, hi=360):
    """All solutions of fn(x) = k (degrees) in [lo, hi], sorted."""
    if fn in ('sin', 'cos') and abs(k) > 1:
        return []
    if fn == 'sin':
        a = math.degrees(math.asin(k))
        base, step = [a, 180 - a], 360
    elif fn == 'cos':
        a = math.degrees(math.acos(k))
        base, step = [a, -a], 360
    else:
        base, step = [math.degrees(math.atan(k))], 180
    out = set()
    for b0 in base:
        for n in range(-3, 12):
            v = b0 + n * step
            if lo - 1e-9 <= v <= hi + 1e-9:
                out.add(round(v, 6))
    res = []
    for v in sorted(out):
        if not res or abs(v - res[-1]) > 1e-4:
            res.append(v)
    return res


@R.add('ch09-st4', 'C1', (1, 3), 'mcq')
def trig_eq_mcq(rng, slot):
    fn, k, ans = rng.choice([('sin', '1/2', '30° and 150°'), ('cos', '1/2', '60° and 300°'), ('sin', '√3/2', '60° and 120°'), ('cos', '√2/2', '45° and 315°'), ('tan', '√3', '60° and 240°'),
                             ('sin', '−1/2', '210° and 330°'), ('cos', '−1/2', '120° and 240°'), ('tan', '−1', '135° and 315°')])
    pool = ['30° and 150°', '60° and 300°', '60° and 120°', '45° and 315°', '60° and 240°', '210° and 330°', '120° and 240°', '135° and 315°', '30° and 330°', '45° and 135°']
    wr = rng.sample([p for p in pool if p != ans], 3)
    return mcq(rng, f'Solve {fn} x = {k} for 0° ≤ x ≤ 360°.', ans, wr, 'Use the exact value and the quadrants where the sign matches.')


@R.add('ch09-st4', 'C3', (1, 4), 'short')
def trig_eq_solve(rng, slot):
    fn = rng.choice(['sin', 'cos', 'tan'])
    a = rng.choice([1, 2, 3, 4, 5])
    c = rng.randint(-3, 3)
    k = round(rng.uniform(-0.9, 0.9), 2) if fn != 'tan' else round(rng.uniform(-3, 3), 1)
    rhs = a * k + c
    sols = _solve_trig(fn, k)
    lhs = f'{a if a > 1 else ""}{fn} x{sgn(c) if c else ""}'
    return short(f'Solve {lhs} = {g(rhs, 4)} for 0° ≤ x ≤ 360°, giving answers to 1 d.p.', ', '.join(_dg(s) for s in sols),
                 f'{fn} x = {g(k, 4)} (A1); principal value (A1); second solution from symmetry / period (M1 A1).', 4)


@R.add('ch09-st4', 'C3', (2, 5), 'short')
def trig_eq_multiple(rng, slot):
    fn = rng.choice(['sin', 'cos'])
    b = rng.choice([2, 3])
    k = rng.choice([0.5, -0.5, 0.2, 0.7, -0.3])
    u = _solve_trig(fn, k, 0, 360 * b)
    xs = [s / b for s in u]
    return short(f'Solve {fn} {b}x = {g(k)} for 0° ≤ x ≤ 360°, giving answers to 1 d.p. where necessary.', ', '.join(_dg(s) for s in xs),
                 f'Let u = {b}x, 0° ≤ u ≤ {360 * b}° (M1); u-values (A1); divide by {b} (A1); all {len(xs)} solutions (A1).', 4)


@R.add('ch09-st4', 'C2', (2, 4), 'explain')
def trig_eq_explain(rng, slot):
    who = name(rng)
    k = round(rng.uniform(0.2, 0.9), 1)
    kind = rng.choice(['sin', 'cos', 'none'])
    if kind == 'sin':
        a = math.degrees(math.asin(k))
        return explain(f'{who} solves sin x = {k} for 0° ≤ x ≤ 360° and gives only x = {_dg(a)}. Explain what is missing.', f'Sine is also positive in the second quadrant: x = 180° − {_dg(a)} = {_dg(180 - a)}.', 'Second quadrant (R1); value (A1).', 2)
    if kind == 'cos':
        a = math.degrees(math.acos(k))
        return explain(f'{who} solves cos x = {k} and writes x = {_dg(a)} or {_dg(180 - a)}. Explain the mistake.', f'cos(180° − x) = −cos x, so 180° − {_dg(a)} gives a negative cosine. The second solution is 360° − {_dg(a)} = {_dg(360 - a)}.', 'Symmetry of cos (R1); correct value (A1).', 2)
    return explain(f'Explain why 3 sin x = {g(3 + k)} has no solutions.', f'sin x = {rsf((3 + k) / 3, 3)} > 1, but −1 ≤ sin x ≤ 1.', 'Rearranged (A1); range of sine (R1).', 2)


@R.add('ch09-st4', 'C4', (3, 5), 'multi_step')
def trig_eq_task(rng, slot):
    city = rng.choice(SEA)
    kind = rng.choice(['ferris', 'temp', 'sound', 'tide'])
    if kind == 'ferris':
        r, hub, T = rng.choice([(20, 22, 10), (30, 33, 15)])
        H = hub + rng.choice([-0.5, 0.3, 0.6]) * r
        k = (hub - H) / r
        u = _solve_trig('cos', k, 0, 360)
        ts = [s / (360 / T) for s in u]
        ans = f'(a) h = −{r} cos({g(360 / T, 4)}t) + {hub} (b) cos({g(360 / T, 4)}t) = {rsf(k, 3)} (c) t = {", ".join(rsf(t, 3) for t in ts)} min (d) {rsf(abs(ts[1] - ts[0]) if len(ts) > 1 else 0, 3)} min {"above" if H > hub - r * 0 else "below"} the level per turn'
        q_ = (f'A Ferris wheel in {city} has radius {r} m and hub {hub} m above the ground, with one turn every {T} minutes; you board at the bottom. (a) Write the height model. (b) Form an equation for when you are {g(H, 3)} m high. '
              f'(c) Solve it for the first turn. (d) Find the time between these two moments and interpret it.')
    elif kind == 'temp':
        a, d = rng.randint(5, 10), rng.randint(15, 22)
        L = d + round(a * rng.uniform(0.2, 0.7))
        u = _solve_trig('cos', (L - d) / -a, 0, 360)
        ms = [1 + s / 30 for s in u]
        ans = f'(a) −{a} cos(30(t − 1)) + {d} = {L} (b) cos(30(t − 1)) = {rsf((L - d) / -a, 3)} (c) t ≈ {", ".join(rsf(v, 3) for v in ms)} (d) the temperature is above {L} °C for about {rsf(ms[1] - ms[0], 2)} months'
        q_ = (f'The mean temperature in {city} is modelled by T = −{a} cos(30(t − 1)) + {d}, t in months (t = 1 is January). (a) Write an equation for T = {L}. (b) Rearrange it. (c) Solve for 1 ≤ t ≤ 13. (d) Interpret the solutions.')
    elif kind == 'sound':
        b = rng.choice([2, 3, 4])
        u = _solve_trig('sin', 0.5, 0, 360 * b)
        xs = [s / b for s in u]
        ans = f'(a) u = {b}x, 0 ≤ u ≤ {360 * b} (b) u = {", ".join(_dg(s, 0) for s in u)} (c) x = {", ".join(_dg(s) for s in xs)} (d) {2 * b} solutions: the graph completes {b} cycles'
        q_ = (f'A sound engineer in {city} studies y = sin {b}x. (a) Make a substitution to solve sin {b}x = 0.5 for 0° ≤ x ≤ 360°. (b) Find all values of u. (c) Find all values of x. (d) Explain the number of solutions.')
    else:
        a, d = round(rng.uniform(1.5, 3), 1), round(rng.uniform(3, 5), 1)
        need = round(d + a * rng.uniform(-0.6, 0.6), 1)
        u = _solve_trig('cos', (need - d) / a, 0, 360)
        ts = [s / (360 / 12.4) for s in u]
        ans = f'(a) {g(a)} cos({g(360 / 12.4, 4)}t) + {g(d)} = {g(need)} (b) t ≈ {", ".join(rsf(t, 3) for t in ts)} h (c) safe from 0 to {rsf(ts[0], 3)} h and from {rsf(ts[-1], 3)} to 12.4 h (d) times shift each day as the tide period is not 12 h'
        q_ = (f'The depth of a harbour in {city} is h = {g(a)} cos({g(360 / 12.4, 4)}t) + {g(d)} metres, t hours after high tide. A boat needs {g(need)} m. (a) Write an equation for the critical depth. (b) Solve it for 0 ≤ t ≤ 12.4. '
              f'(c) State when the boat can use the harbour. (d) Explain why the times change from day to day.')
    return short(q_, ans, f'{ans}. Equation set up (M1); principal value and symmetry used (A1 A1); all solutions in the domain (A1); interpretation (D: R1).', 6, 'multi_step', 'G5')



# =============================================================================================
# ch10 Vectors (Extended)
# =============================================================================================
import statistics as _st


def cv(a, b) -> str:
    """Column vector text."""
    return f'({fx(a)} over {fx(b)})'


def mag(a, b) -> str:
    """Exact magnitude √(a² + b²) in simplest surd form."""
    n = int(a * a + b * b) if Fr(a).denominator == 1 and Fr(b).denominator == 1 else None
    if n is None:
        return rsf(math.hypot(float(a), float(b)), 3)
    return sq(1, n)


def _par(v) -> str:
    return f'({m(v)})' if v < 0 else m(v)


def _ij(a, b) -> str:
    """a i + b j with zero terms dropped and unit coefficients hidden."""
    parts = []
    for c, u in ((a, 'i'), (b, 'j')):
        if c == 0:
            continue
        t = f'{"" if abs(c) == 1 else abs(c)}{u}'
        parts.append(('−' if c < 0 else '') + t if not parts else (' − ' if c < 0 else ' + ') + t)
    return ''.join(parts) or '0'


def _sqp(v) -> str:
    """v² with brackets round a negative value."""
    return f'({m(v)})²' if v < 0 else f'{m(v)}²'


def _dir(a, b):
    """Angle of vector (a, b) measured anticlockwise from the positive x-axis, 0–360."""
    return math.degrees(math.atan2(b, a)) % 360


R.facts('ch10-st1', F(
    terms=[('vector', 'a quantity with both magnitude (size) and direction, such as a displacement or a velocity'),
           ('scalar', 'a quantity with magnitude only, such as distance, speed or mass'),
           ('magnitude of a vector', 'the length of the vector: |(a over b)| = √(a² + b²)'),
           ('unit vector', 'a vector of magnitude 1; i = (1 over 0) and j = (0 over 1) are the unit vectors along the axes')],
    facts=[('What is the magnitude of (6 over −8)?', '10', ['14', '−2', '100'], '√(36 + 64) = 10.'),
           ('Which of these is a vector quantity?', 'velocity', ['speed', 'mass', 'temperature'], 'Velocity has a direction.'),
           ('The vector 3i − 2j written as a column vector is:', '(3 over −2)', ['(−2 over 3)', '(3 over 2)', '(−3 over 2)'], 'i-component on top.')],
    why=[('Explain why the vectors (3 over 4) and (−3 over −4) have the same magnitude but are not equal.', 'Both have length √(9 + 16) = 5, but they point in opposite directions; equal vectors need the same magnitude and direction.'),
         ('Explain why the magnitude of a vector is found using Pythagoras\' theorem.', 'The components form the two shorter sides of a right-angled triangle whose hypotenuse is the vector.'),
         ('Explain the difference between distance and displacement.', 'Distance is the length travelled (a scalar); displacement is the straight-line change in position with a direction (a vector).')],
    misc=[('The magnitude of (−5 over 12) is −13 because one component is negative.', 'A magnitude is a length and is never negative: √(25 + 144) = 13.'),
          ('|(3 over 4)| = 3 + 4 = 7.', 'Use Pythagoras: √(9 + 16) = 5.')],
))


@R.add('ch10-st1', 'C1', (1, 3), 'mcq')
def vec_mag_mcq(rng, slot):
    a, b = rng.choice([(3, 4), (5, 12), (8, 15), (6, 8), (7, 24), (9, 12), (2, 3), (1, 5), (4, 7)])
    a, b = a * rng.choice([1, -1]), b * rng.choice([1, -1])
    if rng.random() < 0.5:
        a, b = b, a
    corr = mag(a, b)
    wr = [m(abs(a) + abs(b)), m(a + b), str(a * a + b * b)]
    wr = [w for w in dict.fromkeys(wr) if w != corr]
    while len(wr) < 3:
        wr.append(str(abs(a) + abs(b) + 1))
    return mcq(rng, f'Find the magnitude of the vector {cv(a, b)}.', corr, wr[:3], f'√({_sqp(a)} + {_sqp(b)}) = {corr}.')


@R.add('ch10-st1', 'C3', (1, 4), 'short')
def vec_from_points(rng, slot):
    A = (rng.randint(-8, 8), rng.randint(-8, 8))
    B = (rng.randint(-8, 8), rng.randint(-8, 8))
    if A == B:
        return None
    a, b = B[0] - A[0], B[1] - A[1]
    if slot.d <= 2:
        return short(f'A = {ptxt(A)} and B = {ptxt(B)}. Write the vector AB as a column vector and in i, j form.', f'{cv(a, b)}; {_ij(a, b)}',
                     f'B − A (M1); {cv(a, b)} (A1).', 2)
    return short(f'A = {ptxt(A)} and B = {ptxt(B)}. Find the vector AB, its exact magnitude and its direction measured anticlockwise from the positive x-axis (to 1 d.p.).', f'{cv(a, b)}; |AB| = {mag(a, b)}; {_dg(_dir(a, b))}',
                 f'AB = B − A (M1) = {cv(a, b)} (A1); magnitude √({a * a} + {b * b}) (A1); direction from tan⁻¹ with the correct quadrant (A1).', 4)


@R.add('ch10-st1', 'C3', (2, 5), 'short')
def vec_from_mag_dir(rng, slot):
    r = rng.randint(3, 25)
    th = rng.choice([v for v in range(5, 360, 5) if v % 90])
    a, b = r * cosd(th), r * sind(th)
    if rng.random() < 0.5:
        return short(f'A vector has magnitude {r} and makes an angle of {th}° anticlockwise with the positive x-axis. Write it as a column vector with components to 3 s.f.', f'({rsf(a, 3)} over {rsf(b, 3)})',
                     f'x = {r} cos {th}° (M1 A1); y = {r} sin {th}° (A1).', 3)
    p, q = rng.choice([(3, 4), (5, 12), (8, 6), (1, 2), (2, -1), (-4, 3), (12, -5), (1, 3)])
    p, q = (p, q) if rng.random() < 0.5 else (q, p)
    h = math.hypot(p, q)
    if h % 1 == 0:
        M = int(h) * rng.choice([2, 3, 4, 5]) + rng.choice([0, 0, 1, 2]) * int(h) // 1
        ansv = cv(Fr(M * p, int(h)), Fr(M * q, int(h)))
    else:
        M = rng.choice([2, 3, 4, 5, 6, 10])
        ansv = f'({rsf(M * p / h, 3)} over {rsf(M * q / h, 3)})'
    return short(f'Find a vector of magnitude {M} in the same direction as {cv(p, q)}{"" if h % 1 == 0 else ", giving components to 3 significant figures"}.', ansv,
                 f'|v| = {mag(p, q)} (A1); unit vector v/|v| (M1); × {M} (A1).', 3)


@R.add('ch10-st1', 'C2', (2, 4), 'explain')
def vec_explain(rng, slot):
    who = name(rng)
    a, b = rng.choice([(3, 4), (5, 12), (6, 8), (8, 15)])
    kind = rng.choice(['equal', 'neg', 'scalar'])
    if kind == 'equal':
        return explain(f'{who} says {cv(a, b)} and {cv(b, a)} are equal because they have the same magnitude. Explain why this is wrong.',
                       f'Both have magnitude {mag(a, b)}, but they point in different directions (the components differ), so the vectors are not equal.', 'Magnitude vs direction (R1); conclusion (A1).', 2)
    if kind == 'neg':
        return explain(f'Explain what the vector −{cv(a, b)} represents and how it relates to {cv(a, b)}.', f'−{cv(a, b)} = {cv(-a, -b)}: the same magnitude {mag(a, b)} but the opposite direction.', 'Components (A1); opposite direction (R1).', 2)
    v = rng.randint(30, 90)
    return explain(f'A car drives at {v} km/h. Explain whether this is a speed or a velocity, and what extra information would make it the other.', f'{v} km/h has no direction, so it is a speed (scalar); adding a direction, e.g. "{v} km/h due north", makes it a velocity.', 'Classification (A1); direction needed (R1).', 2)


@R.add('ch10-st1', 'C4', (3, 5), 'multi_step')
def vec_notation_task(rng, slot):
    city = rng.choice(CITIES)
    kind = rng.choice(['walk', 'drone', 'grid', 'compare'])
    if kind == 'walk':
        e, n_ = rng.randint(-12, 12), rng.randint(-12, 12)
        if e == 0 or n_ == 0:
            e, n_ = 5, -7
        ans = f'(a) {cv(e, n_)} (b) {mag(e, n_)} ≈ {rsf(math.hypot(e, n_), 3)} km (c) {_brg(math.degrees(math.atan2(e, n_)))} (d) the distance walked ({abs(e) + abs(n_)} km) is longer than the displacement'
        q_ = (f'A tourist in {city} walks {abs(e)} km {"east" if e > 0 else "west"} and then {abs(n_)} km {"north" if n_ > 0 else "south"}. (a) Write the displacement as a column vector (east, north). '
              f'(b) Find its magnitude. (c) Find the bearing of the final position from the start. (d) Compare the distance walked with the magnitude of the displacement.')
    elif kind == 'drone':
        r = rng.randint(50, 300)
        brg = rng.choice([30, 60, 120, 135, 210, 240, 300, 330])
        e, n_ = r * sind(brg), r * cosd(brg)
        ans = f'(a) east {rsf(e, 3)} m, north {rsf(n_, 3)} m (b) ({rsf(e, 3)} over {rsf(n_, 3)}) (c) check √({rsf(e, 3)}² + {rsf(n_, 3)}²) ≈ {r} m (d) the opposite vector ({rsf(-e, 3)} over {rsf(-n_, 3)}), bearing {_brg(brg + 180)}'
        q_ = (f'A delivery drone in {city} flies {r} m on a bearing of {_brg(brg)}. (a) Find the eastward and northward components. (b) Write its displacement as a column vector. '
              f'(c) Check your answer by finding the magnitude. (d) Write the vector for the return journey and its bearing.')
    elif kind == 'grid':
        pts = [(rng.randint(-5, 5), rng.randint(-5, 5)) for _ in range(3)]
        A, B, C = pts
        AB, BC, AC = (B[0] - A[0], B[1] - A[1]), (C[0] - B[0], C[1] - B[1]), (C[0] - A[0], C[1] - A[1])
        ans = f'(a) AB = {cv(*AB)}, BC = {cv(*BC)} (b) AC = {cv(*AC)} (c) AB + BC = AC (d) |AC| = {mag(*AC)} ≤ |AB| + |BC| ≈ {rsf(math.hypot(*AB) + math.hypot(*BC), 3)}'
        q_ = (f'On a map grid of {city}, A = {ptxt(A)}, B = {ptxt(B)}, C = {ptxt(C)}. (a) Write AB and BC as column vectors. (b) Write AC. (c) Describe the relationship between the three vectors. (d) Compare |AC| with |AB| + |BC|.')
    else:
        u = rng.choice([(3, 4), (5, 12), (6, 8)])
        v = (u[1], -u[0])
        ans = f'(a) both have magnitude {mag(*u)} (b) {cv(*u)} points at {_dg(_dir(*u))}, {cv(*v)} at {_dg(_dir(*v))} (c) they are perpendicular (90° apart) (d) (a, b) and (b, −a) are always perpendicular with equal magnitude'
        q_ = (f'Investigate the vectors {cv(*u)} and {cv(*v)}. (a) Find their magnitudes. (b) Find the direction of each from the positive x-axis. (c) Describe how they are related. (d) Generalise for (a over b) and (b over −a).')
    return short(q_, ans, f'{ans}. Vector components (A1 A1); magnitude / direction (M1 A1); interpretation or generalisation (B/D: R1).', 5, 'multi_step', 'G5')


R.facts('ch10-st2', F(
    terms=[('vector addition', 'adding corresponding components: (a over b) + (c over d) = (a + c over b + d); geometrically, joining the vectors nose to tail'),
           ('scalar multiplication', 'multiplying each component by a number k; it scales the magnitude by |k| and reverses the direction if k < 0'),
           ('resultant vector', 'the single vector equivalent to two or more vectors applied one after another'),
           ('parallel vectors', 'vectors that are scalar multiples of each other: u = kv')],
    facts=[('(2 over −3) + (4 over 5) =', '(6 over 2)', ['(6 over −8)', '(−2 over 8)', '(8 over −15)'], 'Add components.'),
           ('3(−2 over 1) =', '(−6 over 3)', ['(1 over 4)', '(−6 over 1)', '(−5 over 3)'], 'Multiply each component.'),
           ('Which vector is parallel to (2 over −5)?', '(−4 over 10)', ['(5 over −2)', '(2 over 5)', '(4 over 10)'], '(−4 over 10) = −2(2 over −5).')],
    why=[('Explain why a − b is the same as a + (−b).', 'Subtracting b means adding the vector of equal size in the opposite direction.'),
         ('Explain why vector addition is commutative.', 'Adding components is ordinary addition of numbers, which is commutative; geometrically both orders complete the same parallelogram.'),
         ('Explain why 2a is parallel to a.', '2a has the same direction as a with twice the length; scalar multiples are always parallel.')],
    misc=[('|a + b| = |a| + |b| for any vectors.', 'Only if a and b point in the same direction; otherwise |a + b| < |a| + |b|.'),
          ('−2(3 over 1) = (−6 over 1).', 'Every component is multiplied: (−6 over −2).')],
))


def _rv(rng, lo=-7, hi=7):
    while True:
        v = (rng.randint(lo, hi), rng.randint(lo, hi))
        if v != (0, 0):
            return v


@R.add('ch10-st2', 'C1', (1, 3), 'mcq')
def vec_ops_mcq(rng, slot):
    a, b = _rv(rng), _rv(rng)
    p, q = rng.choice([2, 3, -1, -2]), rng.choice([1, 2, -3, 3])
    r = (p * a[0] + q * b[0], p * a[1] + q * b[1])
    wr = [(p * a[0] - q * b[0], p * a[1] - q * b[1]), (a[0] + b[0], a[1] + b[1]), (p * a[0] + q * b[1], p * a[1] + q * b[0])]
    wr = [w for w in dict.fromkeys(wr) if w != r]
    while len(wr) < 3:
        wr.append((r[0] + 1, r[1] - 1))
    return mcq(rng, f'a = {cv(*a)} and b = {cv(*b)}. Find {coef(p)}a {"+" if q > 0 else "−"} {coef(abs(q))}b.', cv(*r), [cv(*w) for w in wr[:3]], f'Multiply then add components: {cv(*r)}.')


@R.add('ch10-st2', 'C3', (1, 4), 'short')
def vec_ops_calc(rng, slot):
    a, b = _rv(rng), _rv(rng)
    p, q = rng.choice([2, 3, 4, -1, -2]), rng.choice([1, 2, 3, -1, -3])
    r = (p * a[0] + q * b[0], p * a[1] + q * b[1])
    expr = f'{coef(p)}a {"+" if q > 0 else "−"} {coef(abs(q))}b'
    return short(f'a = {cv(*a)} and b = {cv(*b)}. Find {expr} and its exact magnitude.', f'{cv(*r)}; magnitude {mag(*r)}',
                 f'{coef(p)}a = {cv(p * a[0], p * a[1])}, {coef(q)}b = {cv(q * b[0], q * b[1])} (M1); {cv(*r)} (A1); magnitude {mag(*r)} (A1).', 3)


@R.add('ch10-st2', 'C3', (2, 5), 'short')
def vec_solve(rng, slot):
    a, b = _rv(rng, -5, 5), _rv(rng, -5, 5)
    if a[0] * b[1] - a[1] * b[0] == 0:
        return None
    s, t = rng.randint(-4, 4), rng.randint(-4, 4)
    c = (s * a[0] + t * b[0], s * a[1] + t * b[1])
    if rng.random() < 0.5:
        return short(f'a = {cv(*a)}, b = {cv(*b)} and c = {cv(*c)}. Find the scalars s and t such that sa + tb = c.', f's = {m(s)}, t = {m(t)}',
                     f'{m(a[0])}s + {m(b[0])}t = {m(c[0])} and {m(a[1])}s + {m(b[1])}t = {m(c[1])} (M1 A1); s = {m(s)}, t = {m(t)} (A1).', 3)
    k = rng.choice([v for v in range(-4, 5) if v not in (0, 1)])
    if a[0] == 0:
        return None
    return short(f'The vectors {cv(*a)} and ({fx(k * a[0])} over p) are parallel. Find p.', f'p = {m(k * a[1])}',
                 f'Second = k × first: k = {m(k)} from the x-components (M1 A1); p = {m(k)} × {_par(a[1])} = {m(k * a[1])} (A1).', 3)


@R.add('ch10-st2', 'C2', (2, 4), 'explain')
def vec_ops_explain(rng, slot):
    who = name(rng)
    a, b = _rv(rng, -6, 6), _rv(rng, -6, 6)
    kind = rng.choice(['mag', 'sub', 'par'])
    if kind == 'mag':
        s = (a[0] + b[0], a[1] + b[1])
        return explain(f'{who} says |a + b| = |a| + |b| for a = {cv(*a)} and b = {cv(*b)}. Check this and explain the result.',
                       f'|a + b| = |{cv(*s)}| ≈ {rsf(math.hypot(*s), 3)}, |a| + |b| ≈ {rsf(math.hypot(*a) + math.hypot(*b), 3)}; they are equal only if a and b point the same way – the third side of a triangle is shorter than the other two together.',
                       'Both values (A1); reason (R1).', 2)
    if kind == 'sub':
        return explain(f'{who} works out {cv(*a)} − {cv(*b)} as {cv(a[0] + b[0], a[1] + b[1])}. Explain the error and correct it.', f'Subtract each component: {cv(a[0] - b[0], a[1] - b[1])}; {who} added instead.', 'Error (R1); correct vector (A1).', 2)
    k = rng.choice([2, 3, -2])
    return explain(f'Explain how you can tell that {cv(*a)} and {cv(k * a[0], k * a[1])} are parallel.', f'The second is {k} times the first (each component), so it has the same line of action{" but the opposite direction" if k < 0 else ""}.', 'Scalar multiple (R1); direction comment (A1).', 2)


@R.add('ch10-st2', 'C4', (3, 5), 'multi_step')
def vec_ops_task(rng, slot):
    city = rng.choice(SEA)
    kind = rng.choice(['boat', 'forces', 'path', 'parallelogram'])
    if kind == 'boat':
        b, c = _rv(rng, 2, 9), (rng.randint(-4, 4), rng.randint(-4, 4))
        r = (b[0] + c[0], b[1] + c[1])
        ans = f'(a) {cv(*r)} km/h (b) {rsf(math.hypot(*r), 3)} km/h (c) {_brg(math.degrees(math.atan2(*r)))} (d) after 2 h: {cv(2 * r[0], 2 * r[1])} km from the start'
        q_ = (f'A boat near {city} moves through the water with velocity {cv(*b)} km/h (east, north) and the current is {cv(*c)} km/h. (a) Find the resultant velocity. (b) Find the resultant speed. '
              f'(c) Find the bearing of the boat’s actual course. (d) Find its displacement after 2 hours.')
    elif kind == 'forces':
        f1, f2 = _rv(rng, -8, 8), _rv(rng, -8, 8)
        r = (f1[0] + f2[0], f1[1] + f2[1])
        ans = f'(a) {cv(*r)} N (b) {rsf(math.hypot(*r), 3)} N (c) {cv(-r[0], -r[1])} N (d) the three forces then add to the zero vector, so the object is in equilibrium'
        q_ = (f'Two ropes pull a crate in a warehouse in {city} with forces {cv(*f1)} N and {cv(*f2)} N. (a) Find the resultant force. (b) Find its magnitude. (c) Find the third force that would keep the crate still. (d) Explain your answer to (c).')
    elif kind == 'path':
        legs = [_rv(rng, -6, 6) for _ in range(3)]
        tot = (sum(l[0] for l in legs), sum(l[1] for l in legs))
        ans = f'(a) {cv(*tot)} (b) {mag(*tot)} ≈ {rsf(math.hypot(*tot), 3)} (c) {cv(-tot[0], -tot[1])} (d) the order of the legs does not change the resultant'
        q_ = (f'A robot in a factory in {city} moves {", then ".join(cv(*l) for l in legs)} (metres). (a) Find its total displacement. (b) Find the straight-line distance from the start. (c) Write the vector that returns it to the start. (d) Explain whether the order of the moves matters for (a).')
    else:
        a, b = _rv(rng, -5, 5), _rv(rng, -5, 5)
        d1, d2 = (a[0] + b[0], a[1] + b[1]), (b[0] - a[0], b[1] - a[1])
        ans = f'(a) OC = a + b = {cv(*d1)} (b) AB = b − a = {cv(*d2)} (c) |OC| = {mag(*d1)}, |AB| = {mag(*d2)} (d) the diagonals are equal only if the parallelogram is a rectangle'
        q_ = (f'OACB is a parallelogram with OA = a = {cv(*a)} and OB = b = {cv(*b)}. (a) Find the diagonal OC. (b) Find the diagonal AB. (c) Find the length of each diagonal. (d) Comment on when the diagonals would be equal.')
    return short(q_, ans, f'{ans}. Vector operations correct (M1 A1 A1); magnitude/direction (A1); interpretation (D/B: R1).', 5, 'multi_step', 'G5')


R.facts('ch10-st3', F(
    terms=[('position vector', 'the vector from the origin O to a point P, written OP or p'),
           ('collinear points', 'points that lie on one straight line; A, B, C are collinear if AB = k AC for some scalar k'),
           ('midpoint vector', 'the position vector of the midpoint M of AB is ½(a + b)')],
    facts=[('If a and b are position vectors of A and B, AB =', 'b − a', ['a − b', 'a + b', '½(a + b)'], 'Go from A back to O then out to B.'),
           ('The midpoint of A(2, 6) and B(8, −4) has position vector:', '(5 over 1)', ['(10 over 2)', '(6 over −10)', '(3 over 5)'], '½(a + b).'),
           ('Points with AB = 3BC are:', 'collinear', ['perpendicular', 'never on a line', 'the vertices of a square'], 'Parallel vectors through the common point B.')],
    why=[('Explain why AB = b − a.', 'Going from A to B is the same as going from A to O (−a) and then from O to B (b).'),
         ('Explain why AB = kBC with a common point B proves that A, B and C are collinear.', 'The vectors are parallel, and they share point B, so they lie on the same straight line.'),
         ('Explain how vectors can show that a quadrilateral is a parallelogram.', 'Show that one pair of opposite sides are equal vectors (e.g. AB = DC): they are parallel and equal in length.')],
    misc=[('AB = a − b.', 'AB = b − a: from A to B.'),
          ('If AB is parallel to CD, then A, B, C and D are collinear.', 'Parallel lines need not be the same line; a common point is needed.')],
))


@R.add('ch10-st3', 'C1', (1, 3), 'mcq')
def posvec_mcq(rng, slot):
    A, B = _rv(rng, -8, 8), _rv(rng, -8, 8)
    corr = cv(B[0] - A[0], B[1] - A[1])
    wr = [cv(A[0] - B[0], A[1] - B[1]), cv(A[0] + B[0], A[1] + B[1]), cv(Fr(A[0] + B[0], 2), Fr(A[1] + B[1], 2))]
    wr = [w for w in dict.fromkeys(wr) if w != corr]
    while len(wr) < 3:
        wr.append(cv(B[0], A[1]))
    return mcq(rng, f'A has position vector {cv(*A)} and B has position vector {cv(*B)}. Find AB.', corr, wr[:3], 'AB = b − a.')


@R.add('ch10-st3', 'C3', (1, 4), 'short')
def posvec_midpoint(rng, slot):
    A, B = _rv(rng, -9, 9), _rv(rng, -9, 9)
    if rng.random() < 0.5:
        M = (Fr(A[0] + B[0], 2), Fr(A[1] + B[1], 2))
        return short(f'A and B have position vectors a = {cv(*A)} and b = {cv(*B)}. Find the position vector of the midpoint M of AB, and |AB|.', f'm = {cv(*M)}; |AB| = {mag(B[0] - A[0], B[1] - A[1])}',
                     f'm = ½(a + b) (M1) = {cv(*M)} (A1); AB = {cv(B[0] - A[0], B[1] - A[1])}, |AB| = {mag(B[0] - A[0], B[1] - A[1])} (A1).', 3)
    p, q = rng.choice([(1, 2), (1, 3), (2, 1), (3, 1), (2, 3)])
    P = (A[0] + Fr(p, p + q) * (B[0] - A[0]), A[1] + Fr(p, p + q) * (B[1] - A[1]))
    return short(f'A = {ptxt(A)} and B = {ptxt(B)}. P lies on AB with AP : PB = {p} : {q}. Find the position vector of P.', cv(*P),
                 f'AP = {p}/{p + q} AB (M1); AB = {cv(B[0] - A[0], B[1] - A[1])} (A1); OP = OA + AP = {cv(*P)} (A1).', 3)


@R.add('ch10-st3', 'C3', (2, 5), 'short')
def posvec_collinear(rng, slot):
    A = _rv(rng, -6, 6)
    d = _rv(rng, -4, 4)
    k = rng.choice([2, 3, -1, Fr(1, 2), Fr(3, 2)])
    B = (A[0] + d[0], A[1] + d[1])
    C = (A[0] + k * d[0], A[1] + k * d[1])
    if Fr(C[0]).denominator > 1 or Fr(C[1]).denominator > 1:
        k = 2
        C = (A[0] + 2 * d[0], A[1] + 2 * d[1])
    off = rng.random() < 0.4
    if off:
        C = (C[0], C[1] + 1)
    AB, AC = (B[0] - A[0], B[1] - A[1]), (C[0] - A[0], C[1] - A[1])
    col = AB[0] * AC[1] - AB[1] * AC[0] == 0
    return short(f'Use vectors to determine whether A{ptxt(A)}, B{ptxt(B)} and C{ptxt((int(C[0]), int(C[1])))} are collinear.',
                 f'AB = {cv(*AB)}, AC = {cv(*AC)}; ' + (f'AC = {fx(Fr(AC[0], AB[0]) if AB[0] else Fr(AC[1], AB[1]))} AB, so collinear' if col else 'not scalar multiples, so not collinear'),
                 'AB and AC found (A1 A1); scalar multiple tested with a common point (R1); conclusion (A1).', 4)


@R.add('ch10-st3', 'C2', (2, 4), 'explain')
def posvec_explain(rng, slot):
    who = name(rng)
    kind = rng.choice(['order', 'parallel', 'mid'])
    if kind == 'order':
        A, B = _rv(rng, -6, 6), _rv(rng, -6, 6)
        return explain(f'{who} finds AB for A{ptxt(A)} and B{ptxt(B)} as a − b = {cv(A[0] - B[0], A[1] - B[1])}. Explain the mistake.', f'AB goes from A to B: b − a = {cv(B[0] - A[0], B[1] - A[1])}; a − b is BA.', 'Direction (R1); correct vector (A1).', 2)
    if kind == 'parallel':
        return explain(f'{who} shows AB = 2CD and concludes A, B, C and D lie on one line. Explain why this is not proved.', 'AB = 2CD shows the lines are parallel, but without a common point they could be two different parallel lines.', 'Need a common point (R1); parallel only (R1).', 2)
    return explain('Explain why the position vector of the midpoint of AB is ½(a + b).', 'OM = OA + ½AB = a + ½(b − a) = ½a + ½b.', 'Route O → A → M (M1); simplification (A1).', 2)


@R.add('ch10-st3', 'C4', (3, 5), 'multi_step')
def posvec_task(rng, slot):
    kind = rng.choice(['midpoints', 'parallelogram', 'trapezium', 'ratio'])
    if kind == 'midpoints':
        A, B, C = _rv(rng, -6, 6), _rv(rng, -6, 6), _rv(rng, -6, 6)
        M = (Fr(A[0] + B[0], 2), Fr(A[1] + B[1], 2))
        N = (Fr(A[0] + C[0], 2), Fr(A[1] + C[1], 2))
        MN = (N[0] - M[0], N[1] - M[1])
        BC = (C[0] - B[0], C[1] - B[1])
        ans = f'(a) m = {cv(*M)}, n = {cv(*N)} (b) MN = {cv(*MN)}, BC = {cv(*BC)} (c) MN = ½BC, so MN ∥ BC and half its length (d) in general MN = ½(c − b) = ½BC'
        q_ = (f'Triangle ABC has A{ptxt(A)}, B{ptxt(B)}, C{ptxt(C)}. M and N are the midpoints of AB and AC. (a) Find the position vectors of M and N. (b) Find MN and BC. '
              f'(c) Describe the relationship. (d) Prove it for any triangle using a, b and c.')
    elif kind == 'parallelogram':
        A, B, d = _rv(rng, -5, 5), _rv(rng, -5, 5), _rv(rng, -4, 4)
        D = (A[0] + d[0], A[1] + d[1])
        C = (B[0] + d[0], B[1] + d[1])
        ans = f'(a) AB = {cv(B[0] - A[0], B[1] - A[1])}, DC = {cv(C[0] - D[0], C[1] - D[1])} (b) AB = DC, so ABCD is a parallelogram (c) midpoint of AC = midpoint of BD = {ptxt((fx(Fr(A[0] + C[0], 2)), fx(Fr(A[1] + C[1], 2))))} (d) the diagonals bisect each other'
        q_ = (f'A{ptxt(A)}, B{ptxt(B)}, C{ptxt(C)}, D{ptxt(D)}. (a) Find AB and DC. (b) Show ABCD is a parallelogram. (c) Find the midpoints of both diagonals. (d) State the property you have shown.')
    elif kind == 'trapezium':
        a, b = _rv(rng, -4, 4), _rv(rng, -4, 4)
        k = rng.choice([2, 3])
        ans = f'(a) AB = b − a (b) DC = {k}(b − a) (c) DC = {k}AB so AB ∥ DC; ABCD is a trapezium with DC {k} times AB (d) the other sides are not parallel unless k = 1'
        q_ = (f'OA = a, OB = b, OD = {k}a and OC = {k}b. (a) Find AB in terms of a and b. (b) Find DC. (c) Prove that ABCD (with A, B, C, D in order around O) is a trapezium. (d) Explain when it would be a parallelogram.')
    else:
        A, B = _rv(rng, -6, 6), _rv(rng, -6, 6)
        p, q = rng.choice([(1, 2), (2, 1), (1, 3), (3, 2)])
        P = (A[0] + Fr(p, p + q) * (B[0] - A[0]), A[1] + Fr(p, p + q) * (B[1] - A[1]))
        ans = f'(a) AB = {cv(B[0] - A[0], B[1] - A[1])} (b) AP = {p}/{p + q} AB (c) OP = {cv(*P)} (d) OP = ({coef(q)}a + {coef(p)}b)/{p + q}'
        q_ = (f'A{ptxt(A)} and B{ptxt(B)} are on a straight road; a bus stop P divides AB in the ratio {p} : {q}. (a) Find AB. (b) Express AP in terms of AB. (c) Find the position vector of P. (d) Write a general formula for OP in terms of a and b.')
    return short(q_, ans, f'{ans}. Vectors found (A1 A1); proof logically communicated (C1 R1); generalisation (B: A1).', 5, 'multi_step', 'G5')


R.facts('ch10-st4', F(
    terms=[('displacement vector', 'the change in position, final position minus initial position'),
           ('velocity vector', 'the rate of change of displacement; its magnitude is the speed'),
           ('position at time t', 'the vector r = r₀ + tv for an object starting at r₀ and moving with constant velocity v')],
    facts=[('A ship moves with velocity (3 over 4) km/h. Its speed is:', '5 km/h', ['7 km/h', '12 km/h', '25 km/h'], '√(9 + 16).'),
           ('Starting at (1, 2) with velocity (2 over −1) per hour, the position after 3 hours is:', '(7, −1)', ['(3, 1)', '(6, −3)', '(7, 5)'], 'r = r₀ + 3v.'),
           ('A plane flies with air velocity (200 over 0) and the wind is (0 over 30). Its ground velocity is:', '(200 over 30)', ['(230 over 0)', '(200 over −30)', '(170 over 0)'], 'Add the vectors.')],
    why=[('Explain why a plane must point slightly into a crosswind to fly in a straight line to its destination.', 'The wind adds a sideways velocity; the plane must have an opposite sideways component so the resultant points at the destination.'),
         ('Explain why speed is the magnitude of velocity.', 'Velocity tells how fast and in which direction; its length (magnitude) is just how fast.'),
         ('Explain how to find when two moving objects are at the same place.', 'Write each position as r₀ + tv and set them equal; both components must match at the same t.')],
    misc=[('Doubling the time doubles the position vector.', 'It doubles the displacement tv, not r₀ + tv, unless the start is the origin.'),
          ('If two ships have the same speed they have the same velocity.', 'They also need the same direction.')],
))


@R.add('ch10-st4', 'C1', (1, 3), 'mcq')
def velocity_mcq(rng, slot):
    a, b = rng.choice([(3, 4), (6, 8), (5, 12), (9, 12), (8, 15), (12, 16)])
    a, b = a * rng.choice([1, -1]), b * rng.choice([1, -1])
    sp_ = int(math.hypot(a, b))
    return mcq(rng, f'A ship has velocity {cv(a, b)} km/h. What is its speed?', f'{sp_} km/h', [f'{abs(a) + abs(b)} km/h', f'{a * a + b * b} km/h', f'{abs(a + b)} km/h'], f'√({_sqp(a)} + {_sqp(b)}) = {sp_}.')


@R.add('ch10-st4', 'C3', (1, 4), 'short')
def position_time(rng, slot):
    r0, v = _rv(rng, -10, 10), _rv(rng, -6, 6)
    t = rng.randint(2, 8)
    p = (r0[0] + t * v[0], r0[1] + t * v[1])
    city = rng.choice(SEA)
    return short(f'A ferry near {city} starts at {cv(*r0)} km and moves with constant velocity {cv(*v)} km/h. Find its position after {t} hours and its speed.', f'{cv(*p)} km; speed {mag(*v)} ≈ {rsf(math.hypot(*v), 3)} km/h',
                 f'r = r₀ + {t}v (M1) = {cv(*p)} (A1); speed |v| (A1).', 3)


@R.add('ch10-st4', 'C3', (2, 5), 'short')
def meet_or_wind(rng, slot):
    if rng.random() < 0.5:
        v1 = _rv(rng, -5, 5)
        v2 = _rv(rng, -5, 5)
        if v1 == v2:
            return None
        t = rng.randint(1, 6)
        P = _rv(rng, -10, 10)
        r1 = (P[0] - t * v1[0], P[1] - t * v1[1])
        r2 = (P[0] - t * v2[0], P[1] - t * v2[1])
        return short(f'Boat A starts at {cv(*r1)} with velocity {cv(*v1)} and boat B starts at {cv(*r2)} with velocity {cv(*v2)} (km and km/h). Show that they collide and find when and where.',
                     f't = {t} h at {cv(*P)}', 'Positions r₀ + tv for both (M1); equate both components (M1); same t from both equations (R1); t and point (A1).', 4)
    pv = rng.choice([150, 180, 200, 250])
    w = (rng.randint(-40, 40), rng.randint(-40, 40))
    g_ = (pv + w[0], w[1])
    return short(f'A light aircraft points due east with airspeed {pv} km/h; the wind velocity is {cv(*w)} km/h (east, north). Find the ground velocity, the ground speed and the bearing of the actual course.',
                 f'{cv(*g_)}; {rsf(math.hypot(*g_), 3)} km/h; {_brg(math.degrees(math.atan2(*g_)))}', f'Add vectors (M1 A1); speed (A1); bearing (A1).', 4)


@R.add('ch10-st4', 'C2', (2, 4), 'explain')
def velocity_explain(rng, slot):
    who = name(rng)
    v = rng.choice([(3, 4), (5, 12), (6, 8)])
    kind = rng.choice(['speed', 'same', 'cross'])
    if kind == 'speed':
        return explain(f'{who} says a cyclist with velocity {cv(*v)} m/s is going at {v[0] + v[1]} m/s. Explain the error.', f'Speed is the magnitude √({v[0]}² + {v[1]}²) = {int(math.hypot(*v))} m/s, not the sum of components.', 'Magnitude (R1); value (A1).', 2)
    if kind == 'same':
        return explain(f'Two runners both run at {int(math.hypot(*v))} m/s. Explain whether they must have the same velocity.', f'No: e.g. {cv(*v)} and {cv(-v[0], v[1])} have the same speed but different directions.', 'Direction needed (R1); example (A1).', 2)
    return explain('Explain why a swimmer crossing a river with a current lands downstream of the point directly opposite.', 'The current adds a velocity along the river; the resultant velocity has a downstream component, so the path is not straight across.', 'Vector addition (R1); effect (R1).', 2)


@R.add('ch10-st4', 'C4', (3, 5), 'multi_step')
def velocity_task(rng, slot):
    city = rng.choice(SEA)
    kind = rng.choice(['river', 'intercept', 'plane', 'closest'])
    if kind == 'river':
        w, c, s = rng.choice([40, 60, 80, 100]), Fr(rng.choice([1, 2, 3]), 2), Fr(rng.choice([2, 3, 4]))
        t = Fr(w) / s
        ans = f'(a) {cv(s, c)} m/s (b) {rsf(math.hypot(float(s), float(c)), 3)} m/s (c) {fx(t)} s; {fx(c * t)} m downstream (d) aim upstream at sin⁻¹({fx(c / s)}) ≈ {rsf(math.degrees(math.asin(float(c / s))), 3)}° to the straight-across line'
        q_ = (f'A swimmer near {city} swims straight across a river {w} m wide at {fx(s)} m/s relative to the water; the current flows at {fx(c)} m/s. (a) Write the swimmer’s resultant velocity as a column vector (across, downstream). '
              f'(b) Find the resultant speed. (c) Find the time to cross and how far downstream she lands. (d) In what direction should she aim to land directly opposite?')
    elif kind == 'intercept':
        v1 = _rv(rng, 1, 5)
        t = rng.randint(2, 5)
        P = (rng.randint(5, 20), rng.randint(5, 20))
        s1 = (P[0] - t * v1[0], P[1] - t * v1[1])
        s2 = (0, 0)
        v2 = (Fr(P[0], t), Fr(P[1], t))
        ans = f'(a) r = {cv(*s1)} + t{cv(*v1)} (b) {cv(*P)} at t = {t} (c) v = {cv(*v2)} km/h (d) speed {rsf(math.hypot(float(v2[0]), float(v2[1])), 3)} km/h'
        q_ = (f'A cargo ship near {city} is at {cv(*s1)} km and moves with velocity {cv(*v1)} km/h. A patrol boat leaves the harbour at the origin at the same time to meet it in {t} hours. (a) Write the ship’s position vector at time t. '
              f'(b) Find where the ship will be after {t} hours. (c) Find the velocity the patrol boat needs. (d) Find the patrol boat’s speed.')
    elif kind == 'plane':
        pv = rng.choice([180, 220, 250, 300])
        w = rng.choice([20, 30, 40, 50])
        ang = math.degrees(math.asin(w / pv))
        gs = math.sqrt(pv * pv - w * w)
        D = rng.choice([300, 450, 600])
        ans = f'(a) the plane must aim north of east to cancel the wind (b) sin θ = {w}/{pv}, θ ≈ {rsf(ang, 3)}° (c) ground speed √({pv}² − {w}²) ≈ {rsf(gs, 3)} km/h (d) {rsf(D / gs, 3)} hours'
        q_ = (f'A plane leaving {city} must fly due east to a city {D} km away; its airspeed is {pv} km/h and a wind blows from the north at {w} km/h. (a) Explain why the plane cannot simply point due east. '
              f'(b) Find the angle north of east at which it must point. (c) Find its ground speed. (d) Find the flight time.')
    else:
        r0 = (rng.randint(-10, -2), rng.randint(2, 10))
        v = (rng.randint(1, 4), rng.randint(-3, -1))
        tc = -(r0[0] * v[0] + r0[1] * v[1]) / (v[0] ** 2 + v[1] ** 2)
        pc = (r0[0] + tc * v[0], r0[1] + tc * v[1])
        ans = f'(a) r = {cv(*r0)} + t{cv(*v)} (b) |r|² = ({lin(v[0], r0[0], "t")})² + ({lin(v[1], r0[1], "t")})² (c) minimum at t ≈ {rsf(tc, 3)} h (d) closest distance ≈ {rsf(math.hypot(*pc), 3)} km'
        q_ = (f'A yacht near {city} starts at {cv(*r0)} km relative to a lighthouse at the origin and sails with velocity {cv(*v)} km/h. (a) Write its position at time t. (b) Write the square of its distance from the lighthouse. '
              f'(c) Find when it is closest to the lighthouse. (d) Find the closest distance.')
    return short(q_, ans, f'{ans}. Velocity / position vectors modelled (M1 A1); calculations (A1 A1); interpreted in context (D: R1).', 6, 'multi_step', 'G5')


# =============================================================================================
# ch11 Statistics: Correlation and Regression
# =============================================================================================
_PAIRS = [('hours of revision', 'test score (%)', 'pos', (1, 15), (30, 95)), ('outside temperature (°C)', 'heating bill', 'neg', (0, 25), (40, 160)),
          ('height (cm)', 'arm span (cm)', 'pos', (140, 190), (140, 190)), ('age of car (years)', 'value (thousands)', 'neg', (1, 12), (3, 30)),
          ('daily sunshine (hours)', 'ice creams sold', 'pos', (2, 12), (20, 200)), ('screen time (hours)', 'sleep (hours)', 'neg', (1, 8), (5, 10)),
          ('distance from the city centre (km)', 'house price (thousands)', 'neg', (1, 30), (150, 900)), ('shoe size', 'mathematics score', 'none', (35, 46), (40, 95)),
          ('training sessions per week', '5 km time (minutes)', 'neg', (1, 7), (18, 35)), ('engine size (litres)', 'fuel used (L per 100 km)', 'pos', (1, 4), (5, 14))]


def _biv(rng, n=8, kind=None, strength=None):
    xl, yl, k, (x0, x1), (y0, y1) = rng.choice(_PAIRS) if kind is None else next(p for p in _PAIRS if p[2] == kind)
    xs = sorted(rng.sample(range(x0, x1 + 1), min(n, x1 - x0 + 1)))
    s = strength if strength is not None else rng.choice([0.08, 0.15, 0.3])
    if k == 'none':
        ys = [rng.randint(y0, y1) for _ in xs]
    else:
        ys = []
        for t in xs:
            f = (t - x0) / max(1, x1 - x0)
            base = y0 + (y1 - y0) * (f if k == 'pos' else 1 - f)
            ys.append(int(round(base + rng.gauss(0, s * (y1 - y0)))))
    return xl, yl, k, xs, ys


def _pearson(xs, ys):
    try:
        return _st.correlation(xs, ys)
    except Exception:
        return 0.0


def _reg(xs, ys):
    sl, ic = _st.linear_regression(xs, ys)
    return sl, ic


def _describe_r(r):
    s = 'positive' if r > 0 else 'negative'
    a = abs(r)
    st = 'strong' if a >= 0.75 else 'moderate' if a >= 0.5 else 'weak' if a >= 0.25 else 'very weak / no'
    return f'{st} {s} correlation' if st != 'very weak / no' else 'very weak or no correlation'


def _data(xs, ys):
    return ', '.join(f'({a}, {b})' for a, b in zip(xs, ys))


R.facts('ch11-st1', F(
    terms=[('bivariate data', 'data with two variables measured for each item, which can be plotted as points (x, y)'),
           ('independent variable', 'the variable that is controlled or chosen, plotted on the horizontal axis'),
           ('dependent variable', 'the variable that responds, plotted on the vertical axis'),
           ('outlier', 'a data point that does not fit the general pattern of the others')],
    facts=[('Which is the best description of a scatter diagram whose points rise from left to right close to a line?', 'strong positive correlation', ['weak negative correlation', 'no correlation', 'strong negative correlation'], 'Rising and close together.'),
           ('In a study of revision time and test score, the dependent variable is:', 'the test score', ['the revision time', 'both', 'neither'], 'The score depends on revision.'),
           ('A scatter diagram shows points spread randomly. This suggests:', 'no correlation', ['positive correlation', 'negative correlation', 'causation'], 'No trend.')],
    why=[('Explain why correlation does not imply causation.', 'Two variables can move together because of a third (lurking) variable or by coincidence; a link in data does not show that one causes the other.'),
         ('Explain why an outlier should be investigated rather than just deleted.', 'It may be a recording error, but it may also be a genuine unusual case that tells you something important.'),
         ('Explain how the shape of a scatter diagram shows the strength of a correlation.', 'The closer the points lie to a straight line, the stronger the correlation.')],
    misc=[('Negative correlation means the data values are negative.', 'It means one variable tends to decrease as the other increases.'),
          ('A strong correlation proves that x causes y.', 'Correlation shows association, not cause.')],
))


@R.add('ch11-st1', 'C1', (1, 3), 'mcq')
def scatter_mcq(rng, slot):
    k = rng.choice(['pos', 'neg', 'none'])
    xl, yl, k, xs, ys = _biv(rng, kind=k, strength=0.08)
    r = _pearson(xs, ys)
    corr = _describe_r(r)
    pool = ['strong positive correlation', 'strong negative correlation', 'moderate positive correlation', 'moderate negative correlation', 'very weak or no correlation', 'weak positive correlation', 'weak negative correlation']
    wr = [p for p in pool if p != corr]
    rng.shuffle(wr)
    return mcq(rng, f'Data for {xl} (x) and {yl} (y): {_data(xs, ys)}. Which best describes the correlation?', corr, wr[:3], f'r ≈ {rsf(r, 2)}.')


@R.add('ch11-st1', 'C3', (1, 4), 'short')
def scatter_describe(rng, slot):
    xl, yl, k, xs, ys = _biv(rng)
    r = _pearson(xs, ys)
    city = rng.choice(CITIES)
    return short(f'A study in {city} recorded {xl} (x) and {yl} (y): {_data(xs, ys)}. Describe the correlation shown on a scatter diagram and interpret it in context.', _describe_r(r),
                 f'{_describe_r(r)} (A1 A1: direction and strength); interpretation – as {xl} increases, {yl} tends to {"increase" if r > 0.25 else "decrease" if r < -0.25 else "show no clear change"} (R1).', 3)


@R.add('ch11-st1', 'C3', (2, 5), 'short')
def scatter_outlier(rng, slot):
    xl, yl, k, xs, ys = _biv(rng, kind=rng.choice(['pos', 'neg']), strength=0.05)
    i = rng.randrange(1, len(xs) - 1)
    span = max(ys) - min(ys)
    ys[i] = ys[i] + (span if k == 'neg' else -span) if rng.random() < 0.5 else ys[i] + (-span if k == 'neg' else span)
    ys[i] = max(0, ys[i])
    r_all = _pearson(xs, ys)
    xs2, ys2 = xs[:i] + xs[i + 1:], ys[:i] + ys[i + 1:]
    r2_ = _pearson(xs2, ys2)
    return short(f'Data for {xl} (x) and {yl} (y): {_data(xs, ys)}. (a) Identify the outlier. (b) Calculate r with and without it, to 3 d.p. (c) Comment on its effect.',
                 f'(a) ({xs[i]}, {ys[i]}) (b) with: {r2(r_all, 3)}; without: {r2(r2_, 3)} (c) the outlier weakens the correlation',
                 'Outlier (A1); both r values from GDC (A1 A1); comment (R1).', 4)


@R.add('ch11-st1', 'C2', (2, 4), 'explain')
def scatter_explain(rng, slot):
    who = name(rng)
    pairs = [('ice-cream sales', 'sunburn cases', 'hot sunny weather'), ('number of firefighters at a fire', 'damage caused', 'the size of the fire'),
             ('shoe size of children', 'reading score', 'age'), ('number of TVs in a home', 'life expectancy in a country', 'national wealth'), ('umbrella sales', 'car accidents', 'rainy weather')]
    a, b, c = rng.choice(pairs)
    if rng.random() < 0.6:
        return explain(f'Data show a strong positive correlation between {a} and {b}. {who} concludes that {a} cause {b}. Explain why this conclusion may be wrong.',
                       f'Both are likely to be affected by {c} (a lurking variable); correlation does not show causation.', 'Correlation ≠ causation (R1); plausible third variable (R1).', 2)
    return explain(f'Explain why the variable you control (such as {rng.choice(["revision hours", "fertiliser added", "practice time"])}) is plotted on the horizontal axis of a scatter diagram.',
                   'It is the independent (explanatory) variable; the response is plotted vertically so the graph shows how y depends on x.', 'Independent variable (R1); dependence shown (R1).', 2)


@R.add('ch11-st1', 'C4', (3, 5), 'multi_step')
def scatter_task(rng, slot):
    city = rng.choice(CITIES)
    xl, yl, k, xs, ys = _biv(rng, n=10, kind=rng.choice(['pos', 'neg']))
    r = _pearson(xs, ys)
    ans = f'(a) independent: {xl}; dependent: {yl} (b) {_describe_r(r)} (r ≈ {r2(r, 2)}) (c) as {xl} increases, {yl} tends to {"increase" if r > 0 else "decrease"} (d) e.g. a lurking variable or a small sample of {len(xs)} – the data show association, not proof of cause'
    q_ = (f'A student project in {city} collected {xl} (x) and {yl} (y) for {len(xs)} cases: {_data(xs, ys)}. (a) Identify the independent and dependent variables. (b) Describe the correlation. '
          f'(c) Interpret it in context. (d) Explain one reason why you cannot conclude that x causes y.')
    return short(q_, ans, f'{ans}. Variables (A1); correlation described with direction and strength (A1 A1); interpretation (C1); critical reflection (D: R1).', 5, 'multi_step', 'G5')


R.facts('ch11-st2', F(
    terms=[('line of best fit', 'a straight line that best represents the trend of the points on a scatter diagram'),
           ('mean point', 'the point (x̄, ȳ); a line of best fit by eye should pass through it, and the regression line always does'),
           ('interpolation', 'predicting a value within the range of the data – usually reliable when the correlation is strong'),
           ('extrapolation', 'predicting a value outside the range of the data – often unreliable')],
    facts=[('A line of best fit has equation y = 2.5x + 10. The predicted y when x = 8 is:', '30', ['20', '28', '12.5'], '2.5 × 8 + 10.'),
           ('Predicting outside the range of the data is called:', 'extrapolation', ['interpolation', 'regression', 'correlation'], 'Extra = outside.'),
           ('In y = −3x + 50 (x = hours, y = battery %), the gradient means:', 'the battery falls by 3% per hour', ['the battery starts at 3%', 'the battery rises by 3% per hour', 'the battery lasts 3 hours'], 'Gradient = rate of change.')],
    why=[('Explain why the line of best fit should pass through the mean point.', 'The mean point is the "centre" of the data, so a line balancing the points above and below it goes through (x̄, ȳ).'),
         ('Explain why interpolation is usually more reliable than extrapolation.', 'Within the data we have evidence the trend holds; beyond the data the relationship might change.'),
         ('Explain what the y-intercept of a line of best fit means, and when it is not meaningful.', 'It is the predicted y when x = 0; if x = 0 is far outside the data or impossible, the intercept has no real meaning.')],
    misc=[('A line of best fit must go through the first and last points.', 'It follows the overall trend, passing through the mean point, not particular points.'),
          ('The regression line can be used to predict x from y in the same way.', 'The y-on-x line is designed to predict y; predicting x needs the x-on-y line.')],
))


@R.add('ch11-st2', 'C1', (1, 3), 'mcq')
def bestfit_mcq(rng, slot):
    a = round(rng.uniform(-4, 6), 1)
    if a == 0:
        a = 1.5
    b = rng.randint(5, 60)
    xv = rng.randint(2, 15)
    yv = a * xv + b
    return mcq(rng, f'The line of best fit is y = {g(a)}x + {b}. Predict y when x = {xv}.', g(yv, 5), [g(a + xv + b, 5), g(a * (xv + b), 5), g(b * xv + a, 5)], f'{g(a)} × {xv} + {b}.')


@R.add('ch11-st2', 'C3', (1, 4), 'short')
def bestfit_mean_point(rng, slot):
    xl, yl, k, xs, ys = _biv(rng, n=7, kind=rng.choice(['pos', 'neg']), strength=0.08)
    xb, yb = Fr(sum(xs), len(xs)), Fr(sum(ys), len(ys))
    sl, ic = _reg(xs, ys)
    xp = rng.randint(min(xs) + 1, max(xs) - 1)
    return short(f'Data for {xl} (x) and {yl} (y): {_data(xs, ys)}. (a) Find the mean point. (b) Use technology to find the regression line y = ax + b (a, b to 3 s.f.). (c) Estimate y when x = {xp}.',
                 f'(a) ({rsf(float(xb), 3)}, {rsf(float(yb), 3)}) (b) y = {rsf(sl, 3)}x {"+" if ic >= 0 else "−"} {rsf(abs(ic), 3)} (c) ≈ {rsf(sl * xp + ic, 3)}',
                 'Mean point (A1); regression line (A1 A1); estimate by substitution (A1).', 4)


@R.add('ch11-st2', 'C3', (2, 5), 'short')
def bestfit_interpret(rng, slot):
    xl, yl, k, xs, ys = _biv(rng, n=8, kind=rng.choice(['pos', 'neg']), strength=0.06)
    sl, ic = _reg(xs, ys)
    sl, ic = float(m(rsf(sl, 3)).replace('−', '-')), float(m(rsf(ic, 3)).replace('−', '-'))
    lo, hi = min(xs), max(xs)
    inside = rng.randint(lo + 1, hi - 1)
    outside = hi + rng.randint(max(2, (hi - lo) // 2), hi - lo + 5)
    return short(f'For data on {xl} (x) and {yl} (y) with x from {lo} to {hi}, the regression line is y = {rsf(sl, 3)}x {"+" if ic >= 0 else "−"} {rsf(abs(ic), 3)}. (a) Interpret the gradient. (b) Predict y for x = {inside} and x = {outside}. (c) Comment on the reliability of each prediction.',
                 f'(a) y {"increases" if sl > 0 else "decreases"} by about {rsf(abs(sl), 3)} for each unit increase in x (b) {rsf(sl * inside + ic, 3)}; {rsf(sl * outside + ic, 3)} (c) x = {inside} is interpolation (reliable); x = {outside} is extrapolation (unreliable)',
                 'Gradient in context (R1); both predictions (A1 A1); interpolation vs extrapolation (R1).', 4)


@R.add('ch11-st2', 'C2', (2, 4), 'explain')
def bestfit_explain(rng, slot):
    who = name(rng)
    a, b = round(rng.uniform(1.5, 4), 1), rng.randint(20, 40)
    kind = rng.choice(['extrap', 'intercept', 'reverse'])
    if kind == 'extrap':
        return explain(f'A line y = {g(a)}x + {b} models a child’s height (cm) from age x (data for ages 2–10). {who} predicts the height at age 40. Explain why this is unreliable.',
                       f'Age 40 is far outside the data (extrapolation); people stop growing, so the linear trend does not continue – the model would give {g(a * 40 + b, 4)} cm.', 'Extrapolation (R1); context reason (R1).', 2)
    if kind == 'intercept':
        return explain(f'The line y = −{g(a)}x + {b * 3} models the price of a used phone (y, in dollars) against its age in months (x, data from 6 to 30 months). Explain what the y-intercept means and whether it is reliable.',
                       f'It predicts a price of {b * 3} at age 0 (new); x = 0 is outside the data, so it is extrapolation and may not match the real new price.', 'Meaning (A1); reliability (R1).', 2)
    return explain(f'{who} uses the regression line of y on x to predict x from a given y. Explain why this may give a poor estimate.', 'The y-on-x line minimises vertical errors to predict y; predicting x needs the x-on-y line, which is different unless the correlation is perfect.', 'Purpose of the line (R1); difference (R1).', 2)


@R.add('ch11-st2', 'C4', (3, 5), 'multi_step')
def bestfit_task(rng, slot):
    city = rng.choice(CITIES)
    xl, yl, k, xs, ys = _biv(rng, n=9, kind=rng.choice(['pos', 'neg']), strength=0.08)
    sl, ic = _reg(xs, ys)
    xb, yb = sum(xs) / len(xs), sum(ys) / len(ys)
    xi = rng.randint(min(xs) + 1, max(xs) - 1)
    xo = max(xs) + max(3, (max(xs) - min(xs)))
    ans = f'(a) ({rsf(xb, 3)}, {rsf(yb, 3)}) (b) y = {rsf(sl, 3)}x {"+" if ic >= 0 else "−"} {rsf(abs(ic), 3)} (c) check: {rsf(sl, 3)} × {rsf(xb, 3)} {"+" if ic >= 0 else "−"} {rsf(abs(ic), 3)} ≈ {rsf(sl * xb + ic, 3)} = ȳ (d) x = {xi}: {rsf(sl * xi + ic, 3)} (interpolation); x = {xo}: {rsf(sl * xo + ic, 3)} (extrapolation – unreliable)'
    q_ = (f'Researchers in {city} recorded {xl} (x) and {yl} (y): {_data(xs, ys)}. (a) Find the mean point. (b) Find the equation of the regression line. (c) Show that the line passes through the mean point. '
          f'(d) Predict y for x = {xi} and x = {xo}, and comment on the reliability of each.')
    return short(q_, ans, f'{ans}. Mean point and line (A1 A1 A1); verification (R1); predictions with reliability discussed (D: A1 R1).', 6, 'multi_step', 'G5')


R.facts('ch11-st3', F(
    terms=[("Pearson's correlation coefficient", 'r, a number from −1 to 1 measuring the strength and direction of a linear relationship'),
           ('perfect correlation', 'the case r = 1 or r = −1: all points lie exactly on a straight line'),
           ('coefficient of determination', 'the value r², the proportion of the variation in y explained by the linear model')],
    facts=[('Which value of r shows the strongest correlation?', '−0.92', ['0.85', '0.5', '−0.3'], '|−0.92| is the largest.'),
           ('r = 0.05 suggests:', 'no linear correlation', ['strong positive correlation', 'perfect correlation', 'strong negative correlation'], 'Close to 0.'),
           ('r = −0.7 describes:', 'moderate to strong negative correlation', ['weak positive correlation', 'no correlation', 'perfect negative correlation'], 'Negative sign, |r| = 0.7.')],
    why=[('Explain why r = 0 does not mean the variables are unrelated.', 'r measures only linear relationships; the data could follow a curve, e.g. a parabola, with r ≈ 0.'),
         ('Explain why r has no units.', 'It is calculated from standardised values, so the units of x and y cancel; changing units does not change r.'),
         ('Explain why r is the same if x and y are swapped.', 'The formula is symmetric in x and y: it measures how they vary together.')],
    misc=[('r = −0.9 is weaker than r = 0.5 because it is smaller.', 'Strength depends on |r|: 0.9 > 0.5, so −0.9 is stronger.'),
          ('r = 0.8 means 80% of the points are on the line.', 'r measures closeness to a line overall; r² ≈ 0.64 is the proportion of variation explained.')],
))


@R.add('ch11-st3', 'C1', (1, 3), 'mcq')
def pearson_mcq(rng, slot):
    vals = rng.sample([-0.95, -0.82, -0.6, -0.35, -0.1, 0.05, 0.3, 0.55, 0.78, 0.91], 4)
    corr = max(vals, key=abs)
    return mcq(rng, 'Which value of r indicates the strongest linear correlation?', g(corr), [g(v) for v in vals if v != corr], f'|{g(corr)}| is largest.')


@R.add('ch11-st3', 'C3', (1, 4), 'short')
def pearson_calc(rng, slot):
    xl, yl, k, xs, ys = _biv(rng, n=rng.choice([6, 7, 8]))
    r = _pearson(xs, ys)
    return short(f'Use technology to find Pearson’s r for these data on {xl} (x) and {yl} (y): {_data(xs, ys)}. Give r to 3 d.p. and describe the correlation.', f'r = {r2(r, 3)}; {_describe_r(r)}',
                 f'r = {r2(r, 3)} (A1 A1); description in terms of strength and direction (A1).', 3)


@R.add('ch11-st3', 'C3', (2, 5), 'short')
def pearson_r2(rng, slot):
    xl, yl, k = rng.choice([(p[0], p[1], p[2]) for p in _PAIRS if p[2] != 'none'])
    r = round((1 if k == 'pos' else -1) * rng.uniform(0.3, 0.98), 2)
    return short(f'For data on {xl} and {yl}, r = {g(r)}. (a) Describe the correlation. (b) Find r² and interpret it.', f'(a) {_describe_r(r)} (b) r² = {r2(r * r, 3)}: about {rsf(r * r * 100, 2)}% of the variation in {yl} is explained by the linear relationship',
                 'Description (A1); r² (A1); interpretation (R1).', 3)


@R.add('ch11-st3', 'C2', (2, 4), 'explain')
def pearson_explain(rng, slot):
    who = name(rng)
    kind = rng.choice(['curve', 'units', 'strength'])
    if kind == 'curve':
        xs = list(range(-3, 4))
        ys = [t * t for t in xs]
        return explain(f'For the points {_data(xs, ys)}, r = {r2(_pearson(xs, ys), 2)}. {who} says the variables are unrelated. Explain why this is wrong.', 'The points lie exactly on y = x², a perfect non-linear relationship; r only measures linear association.', 'Non-linear pattern (R1); limitation of r (R1).', 2)
    if kind == 'units':
        return explain('Explain why changing the heights in a data set from centimetres to metres does not change the value of r.', 'r measures how closely the points fit a line relative to their spread; rescaling changes both by the same factor, so r is unchanged.', 'Scale invariance (R1); reason (R1).', 2)
    a, b = round(rng.uniform(-0.95, -0.7), 2), round(rng.uniform(0.3, 0.6), 2)
    return explain(f'{who} says r = {g(b)} shows a stronger correlation than r = {g(a)} because {g(b)} is larger. Explain the mistake.', f'Strength depends on |r|: |{g(a)}| = {g(abs(a))} > {g(b)}, so r = {g(a)} is stronger; the sign only gives the direction.', 'Absolute value (R1); conclusion (A1).', 2)


@R.add('ch11-st3', 'C4', (3, 5), 'multi_step')
def pearson_task(rng, slot):
    city = rng.choice(CITIES)
    xl, yl, k, xs, ys = _biv(rng, n=8, kind=rng.choice(['pos', 'neg']), strength=0.1)
    for _ in range(40):
        xl2, yl2, k2, xs2, ys2 = _biv(rng, n=8, kind='none')
        if abs(_pearson(xs2, ys2)) < 0.4:
            break
    else:
        return None
    r1, r2v = _pearson(xs, ys), _pearson(xs2, ys2)
    if abs(r1) < 0.7:
        return None
    ans = f'(a) r = {r2(r1, 3)} (b) r = {r2(r2v, 3)} (c) set 1: {_describe_r(r1)}; set 2: {_describe_r(r2v)} (d) a regression line is only useful for set 1, because |r| = {r2(abs(r1), 3)} shows a strong linear correlation, while |r| = {r2(abs(r2v), 3)} for set 2 is too weak for reliable predictions'
    q_ = (f'A school in {city} collected two data sets. Set 1, {xl} vs {yl}: {_data(xs, ys)}. Set 2, {xl2} vs {yl2}: {_data(xs2, ys2)}. (a) Find r for set 1. (b) Find r for set 2. '
          f'(c) Describe each correlation. (d) For which set is a line of best fit useful for prediction? Justify.')
    return short(q_, ans, f'{ans}. Both r values (A1 A1); descriptions (A1 A1); justified conclusion (D: R1).', 5, 'multi_step', 'G5')


R.facts('ch11-st4', F(
    terms=[('simple random sample', 'a sample in which every member of the population has an equal chance of being chosen, independently'),
           ('stratified sample', 'a sample in which the population is split into groups (strata) and each group is sampled in proportion to its size'),
           ('systematic sample', 'a sample chosen at regular intervals from an ordered list, e.g. every 10th person'),
           ('bias', 'a systematic tendency for a sample or question to give results that differ from the truth about the population')],
    facts=[('Choosing every 20th name on a register is:', 'systematic sampling', ['simple random sampling', 'stratified sampling', 'convenience sampling'], 'Regular intervals.'),
           ('Asking the first 30 people who walk past is:', 'convenience sampling', ['stratified sampling', 'systematic sampling', 'simple random sampling'], 'Easiest people to reach.'),
           ('A school has 300 boys and 200 girls. A stratified sample of 50 should include how many girls?', '20', ['25', '200', '10'], '200/500 × 50.')],
    why=[('Explain why a larger random sample usually gives more reliable results.', 'Random variation averages out over more data, so the sample statistics are closer to the population values.'),
         ('Explain why an online survey about internet use may be biased.', 'Only people who use the internet can respond, so heavy users are over-represented.'),
         ('Explain why stratified sampling can be better than simple random sampling.', 'It guarantees each group is represented in proportion, reducing the chance of an unrepresentative sample by luck.')],
    misc=[('A sample is unbiased as long as it is large.', 'A large sample chosen in a biased way is still biased; the method matters.'),
          ('Systematic sampling is always random.', 'It is only random if the starting point is random and the list has no pattern.')],
))


@R.add('ch11-st4', 'C1', (1, 3), 'mcq')
def sampling_mcq(rng, slot):
    city = rng.choice(CITIES)
    cases = [(f'A researcher in {city} numbers all 800 club members and uses a random number generator to choose 40.', 'simple random sampling'),
             (f'A café in {city} asks every 10th customer through the door.', 'systematic sampling'),
             (f'A school in {city} picks students from each grade in proportion to the grade sizes.', 'stratified sampling'),
             (f'A reporter in {city} interviews the people standing nearest to her.', 'convenience sampling'),
             (f'A survey in {city} chooses a fixed number of people from each age group, without random selection within groups.', 'quota sampling')]
    stem, corr = rng.choice(cases)
    pool = ['simple random sampling', 'systematic sampling', 'stratified sampling', 'convenience sampling', 'quota sampling']
    return mcq(rng, f'{stem} Which sampling method is this?', corr, rng.sample([p for p in pool if p != corr], 3), f'{corr.capitalize()}.')


@R.add('ch11-st4', 'C3', (1, 4), 'short')
def stratified_calc(rng, slot):
    city = rng.choice(CITIES)
    groups = rng.choice([('Grade 6', 'Grade 7', 'Grade 8', 'Grade 9'), ('under 18', '18–40', '41–65', 'over 65'), ('Science', 'Arts', 'Business', 'Engineering')])
    sizes = [rng.randint(40, 400) for _ in groups]
    n = rng.choice([40, 50, 60, 80, 100])
    T = sum(sizes)
    raw = [s * n / T for s in sizes]
    rounded = [int(rnd(v, 0)) for v in raw]
    if sum(rounded) != n:
        return None
    return short(f'A survey in {city} uses a stratified sample of {n} from a population with {", ".join(f"{s} in {gname}" for s, gname in zip(sizes, groups))}. How many should be chosen from each group?',
                 ', '.join(f'{gname}: {r}' for gname, r in zip(groups, rounded)) + (f' (total {sum(rounded)}; adjust one group by 1 to make {n})' if sum(rounded) != n else ''),
                 f'Each group: size/{T} × {n} (M1); {", ".join(rsf(v, 3) for v in raw)} (A1); rounded and total checked (A1).', 3)


@R.add('ch11-st4', 'C3', (2, 5), 'short')
def bias_identify(rng, slot):
    city = rng.choice(CITIES)
    cases = [(f'To estimate how often residents of {city} exercise, a researcher surveys people leaving a gym.', 'Selection bias: gym users exercise more than average.', 'Survey at random from the electoral or postal register.'),
             (f'A council in {city} asks: "Don’t you agree the new park is a waste of money?"', 'Leading question: it pushes respondents to agree.', 'Ask a neutral question, e.g. "How do you rate the new park from 1 to 5?"'),
             (f'A survey about school lunches in {city} is sent by email and only 12% reply.', 'Non-response bias: those who reply may have strong opinions.', 'Follow up non-responders or use a smaller random sample with interviews.'),
             (f'To find the average height of students in a school in {city}, the basketball team is measured.', 'Selection bias: basketball players tend to be taller.', 'Take a random sample from the whole school list.'),
             (f'A phone survey in {city} calls landlines during working hours.', 'Selection bias: people at work or without landlines are missed.', 'Use mixed methods and call at different times.')]
    stem, prob, fix = rng.choice(cases)
    return short(f'{stem} Identify the source of bias and suggest an improvement.', f'{prob} Improvement: {fix}', 'Bias identified and explained (R1 A1); sensible improvement (A1).', 3)


@R.add('ch11-st4', 'C2', (2, 4), 'explain')
def sampling_explain(rng, slot):
    who = name(rng)
    n = rng.choice([500, 1000, 2000])
    kind = rng.choice(['size', 'system', 'strat'])
    if kind == 'size':
        return explain(f'{who} surveys {n} people at a football match about national sports funding and says the large sample makes the result reliable. Explain why this may not be true.',
                       'The sample is biased towards football fans; size does not fix a biased method.', 'Bias identified (R1); size vs method (R1).', 2)
    if kind == 'system':
        return explain('A factory checks every 50th item on a production line. Explain how this systematic sample could be biased.', 'If a machine fault repeats with a cycle linked to 50 items, faulty items could always (or never) be selected.', 'Periodic pattern (R1); effect (R1).', 2)
    return explain('Explain why a stratified sample by grade is suitable for a survey on homework time in a school.', 'Homework time probably differs by grade; stratifying ensures each grade is represented in proportion.', 'Strata linked to variable (R1); proportional representation (R1).', 2)


@R.add('ch11-st4', 'C4', (3, 5), 'multi_step')
def sampling_task(rng, slot):
    city = rng.choice(CITIES)
    N = rng.choice([600, 800, 1200, 1500])
    n = rng.choice([40, 50, 60, 80])
    topic = rng.choice(['screen time', 'travel to school', 'sleep', 'part-time work', 'reading habits'])
    g1 = rng.randint(N // 5, N // 2)
    g2 = N - g1
    ans = f'(a) number the students 1–{N} and choose {n} different random numbers (b) {rsf(g1 * n / N, 3)} → {int(rnd(g1 * n / N, 0))} lower-school and {n - int(rnd(g1 * n / N, 0))} upper-school students (c) e.g. a question on {topic} with clear, non-overlapping options (d) e.g. non-response or untruthful answers; follow up and keep it anonymous'
    q_ = (f'A school in {city} with {N} students ({g1} lower school, {g2} upper school) wants to survey {topic}. (a) Describe how to select a simple random sample of {n}. (b) Find the numbers for a stratified sample of {n}. '
          f'(c) Write one unbiased question. (d) Identify one possible source of bias and how to reduce it.')
    return short(q_, ans, f'{ans}. Random method described (A1); stratified numbers (M1 A1); unbiased question (C1); bias discussed (D: R1).', 5, 'multi_step', 'G5')


R.facts('ch11-st5', F(
    terms=[('standard deviation', 'a measure of spread: roughly the typical distance of the data from the mean; σ = √(Σ(x − x̄)²/n)'),
           ('variance', 'the square of the standard deviation, σ²'),
           ('interquartile range', 'Q3 − Q1, the spread of the middle 50% of the data')],
    facts=[('Adding 5 to every value in a data set changes the standard deviation by:', 'nothing', ['+5', '×5', '+25'], 'Spread is unchanged.'),
           ('Multiplying every value by 3 multiplies the standard deviation by:', '3', ['9', '1', '√3'], 'Distances from the mean triple.'),
           ('The data 4, 4, 4, 4 have standard deviation:', '0', ['4', '1', '16'], 'No spread.')],
    why=[('Explain why the standard deviation is a better measure of spread than the range for most data sets.', 'It uses every value, not only the two extremes, so one outlier affects it less dramatically.'),
         ('Explain why a smaller standard deviation means more consistent data.', 'The values lie closer to the mean on average.'),
         ('Explain why the deviations are squared before averaging.', 'Positive and negative deviations would cancel to zero; squaring makes them all positive.')],
    misc=[('If two data sets have the same mean they have the same spread.', 'They can have very different standard deviations.'),
          ('Adding a constant to every value increases the standard deviation.', 'Every value moves equally, so the spread is unchanged.')],
))


def _sd(d):
    return _st.pstdev(d)


@R.add('ch11-st5', 'C1', (1, 3), 'mcq')
def sd_mcq(rng, slot):
    k = rng.randint(2, 9)
    s = round(rng.uniform(1.5, 8), 1)
    kind = rng.choice(['add', 'mult'])
    if kind == 'add':
        return mcq(rng, f'A data set has standard deviation {g(s)}. Every value is increased by {k}. What is the new standard deviation?', g(s), [g(s + k), g(s * k), g(s - k) if s > k else g(s + 2 * k)], 'Adding shifts but does not spread.')
    return mcq(rng, f'A data set has standard deviation {g(s)}. Every value is multiplied by {k}. What is the new standard deviation?', g(s * k, 4), [g(s, 4), g(s + k, 4), g(s * k * k, 4)], 'Spread scales by the factor.')


@R.add('ch11-st5', 'C3', (1, 4), 'short')
def sd_calc(rng, slot):
    city = rng.choice(CITIES)
    n = rng.choice([6, 7, 8])
    ctx = rng.choice(['daily rainfall (mm)', 'bus waiting times (minutes)', 'quiz scores', 'heights of seedlings (cm)', 'daily temperatures (°C)'])
    d = [rng.randint(2, 40) for _ in range(n)]
    return short(f'The {ctx} recorded in {city} were: {", ".join(map(str, d))}. Use technology to find the mean and the (population) standard deviation, to 3 s.f.', f'mean {rsf(_st.mean(d), 3)}; σ = {rsf(_sd(d), 3)}',
                 f'Mean {rsf(_st.mean(d), 3)} (A1); σ = {rsf(_sd(d), 3)} (A1 A1).', 3)


@R.add('ch11-st5', 'C3', (2, 5), 'short')
def sd_freq(rng, slot):
    vals = list(range(rng.randint(0, 3), rng.randint(0, 3) + 5))
    fr_ = [rng.randint(1, 12) for _ in vals]
    data = [v for v, f in zip(vals, fr_) for _ in range(f)]
    ctx = rng.choice(['number of goals per match', 'number of siblings', 'number of books borrowed', 'number of cars per household'])
    return short(f'The table shows the {ctx}: value {", ".join(map(str, vals))}; frequency {", ".join(map(str, fr_))}. Find the mean and standard deviation to 3 s.f.', f'mean {rsf(_st.mean(data), 3)}; σ = {rsf(_sd(data), 3)}',
                 f'Σf = {len(data)}, Σfx = {sum(data)} (M1); mean (A1); σ from GDC with frequencies (A1 A1).', 4)


@R.add('ch11-st5', 'C2', (2, 4), 'explain')
def sd_explain(rng, slot):
    who = name(rng)
    kind = rng.choice(['same_mean', 'add', 'outlier'])
    if kind == 'same_mean':
        m0 = rng.randint(10, 30)
        a = [m0 - 1, m0, m0, m0 + 1]
        b = [m0 - 8, m0 - 2, m0 + 2, m0 + 8]
        return explain(f'Sets A = {", ".join(map(str, a))} and B = {", ".join(map(str, b))} both have mean {m0}. Explain, using standard deviation, how they differ.',
                       f'σ_A ≈ {rsf(_sd(a), 3)} and σ_B ≈ {rsf(_sd(b), 3)}: B is much more spread out; the mean alone does not describe spread.', 'Both σ (A1); comparison (R1).', 2)
    if kind == 'add':
        k = rng.randint(2, 10)
        return explain(f'Every student’s test mark is increased by {k} after a marking error. {who} says the standard deviation also increases by {k}. Explain why this is wrong.', f'Every mark moves by {k}, so the mean moves by {k} too and the distances from the mean are unchanged; σ stays the same.', 'Distances unchanged (R1); conclusion (A1).', 2)
    return explain('Explain why one very large value affects the standard deviation more than it affects the interquartile range.', 'σ uses the squared distance of every value from the mean, so an extreme value adds a large squared term; the IQR uses only the middle 50%.', 'Squared deviation (R1); IQR ignores extremes (R1).', 2)


@R.add('ch11-st5', 'C4', (3, 5), 'multi_step')
def sd_task(rng, slot):
    city = rng.choice(CITIES)
    kind = rng.choice(['athletes', 'machines', 'cities', 'transform'])
    if kind in ('athletes', 'machines', 'cities'):
        n1, n2 = two_names(rng)
        lab = {'athletes': (f'{n1}’s 100 m times (s)', f'{n2}’s 100 m times (s)', 'choose for a relay', 'lower'),
               'machines': ('masses (g) of bags filled by machine A', 'masses (g) of bags filled by machine B', 'keep', 'closer to 500'),
               'cities': (f'daily maximum temperatures in {city} (°C)', 'daily maximum temperatures in a second city (°C)', 'describe', 'typical')}[kind]
        if kind == 'athletes':
            a = [round(rng.uniform(11.8, 12.6), 2) for _ in range(6)]
            b = [round(rng.uniform(11.3, 13.2), 2) for _ in range(6)]
        elif kind == 'machines':
            a = [500 + rng.randint(-3, 3) for _ in range(8)]
            b = [500 + rng.randint(-9, 9) for _ in range(8)]
        else:
            a = [rng.randint(20, 26) for _ in range(7)]
            b = [rng.randint(12, 34) for _ in range(7)]
        ma, mb, sa, sb = _st.mean(a), _st.mean(b), _sd(a), _sd(b)
        ans = f'(a) mean {rsf(ma, 4)}, σ = {rsf(sa, 3)} (b) mean {rsf(mb, 4)}, σ = {rsf(sb, 3)} (c) set {"A" if sa < sb else "B"} is more consistent (smaller σ) (d) a reasoned choice using both the mean and σ in context'
        q_ = (f'Data set A ({lab[0]}): {", ".join(g(v, 4) for v in a)}. Data set B ({lab[1]}): {", ".join(g(v, 4) for v in b)}. (a) Find the mean and standard deviation of A. (b) Repeat for B. '
              f'(c) Compare the consistency of the two sets. (d) Use both statistics to make a recommendation in context.')
    else:
        d = [rng.randint(10, 30) for _ in range(6)]
        k, c = rng.choice([2, 3, 10]), rng.randint(5, 20)
        ans = f'(a) mean {rsf(_st.mean(d), 3)}, σ {rsf(_sd(d), 3)} (b) adding {c}: mean {rsf(_st.mean(d) + c, 3)}, σ {rsf(_sd(d), 3)} (c) × {k}: mean {rsf(_st.mean(d) * k, 3)}, σ {rsf(_sd(d) * k, 3)} (d) adding shifts the mean only; multiplying scales both'
        q_ = (f'Investigate how transformations affect the mean and standard deviation of {", ".join(map(str, d))}. (a) Find the mean and σ. (b) Add {c} to every value and find them again. (c) Multiply every original value by {k} and find them again. (d) State general rules.')
    return short(q_, ans, f'{ans}. Statistics computed (A1 A1 A1); comparison / pattern (B/D: R1); communication (C1).', 6, 'multi_step', 'G5')


# =============================================================================================
# ch12 Further Probability (Extended)
# =============================================================================================
R.facts('ch12-st1', F(
    terms=[('union', 'A ∪ B: the outcomes in A or B (or both)'),
           ('intersection', 'A ∩ B: the outcomes in both A and B'),
           ('complement', "A′: the outcomes not in A; P(A′) = 1 − P(A)"),
           ('addition rule', 'P(A ∪ B) = P(A) + P(B) − P(A ∩ B)')],
    facts=[('If P(A) = 0.5, P(B) = 0.4 and P(A ∩ B) = 0.2, then P(A ∪ B) =', '0.7', ['0.9', '0.1', '0.2'], '0.5 + 0.4 − 0.2.'),
           ('Mutually exclusive events have:', 'P(A ∩ B) = 0', ['P(A ∩ B) = 1', 'P(A) = P(B)', 'P(A ∪ B) = 0'], 'They cannot both happen.'),
           ('n(U) = 30, n(A) = 12. n(A′) =', '18', ['12', '42', '30'], '30 − 12.')],
    why=[('Explain why P(A ∩ B) is subtracted in the addition rule.', 'Outcomes in both A and B are counted once in P(A) and again in P(B), so they must be removed once.'),
         ('Explain why P(A) + P(A′) = 1.', 'Every outcome is either in A or not in A, and not both, so the two probabilities cover everything exactly once.'),
         ('Explain why mutually exclusive events cannot overlap on a Venn diagram.', 'They cannot happen together, so there are no outcomes in the intersection.')],
    misc=[('P(A ∪ B) = P(A) + P(B) always.', 'Only for mutually exclusive events; otherwise subtract P(A ∩ B).'),
          ("A′ ∩ B′ means 'not in A and B'.", "It means in neither A nor B: (A ∪ B)′.")],
))


def _venn(rng):
    a_only, both, b_only = rng.randint(2, 20), rng.randint(1, 12), rng.randint(2, 20)
    neither = rng.randint(0, 12)
    return a_only, both, b_only, neither


@R.add('ch12-st1', 'C1', (1, 3), 'mcq')
def addition_rule_mcq(rng, slot):
    pa, pb = round(rng.uniform(0.2, 0.6), 2), round(rng.uniform(0.2, 0.6), 2)
    pab = round(rng.uniform(0.05, min(pa, pb) - 0.02), 2)
    u = pa + pb - pab
    return mcq(rng, f'P(A) = {g(pa)}, P(B) = {g(pb)} and P(A ∩ B) = {g(pab)}. Find P(A ∪ B).', r2(u, 2), [r2(pa + pb, 2), r2(pa * pb, 2), r2(pa + pb + pab, 2)], 'Addition rule.')


@R.add('ch12-st1', 'C3', (1, 4), 'short')
def venn_probs(rng, slot):
    a, b_, c, d = _venn(rng)
    T = a + b_ + c + d
    city = rng.choice(CITIES)
    A, B = rng.choice([('play football', 'play tennis'), ('study French', 'study Spanish'), ('own a bike', 'own a scooter'), ('like tea', 'like coffee'), ('take the bus', 'take the metro')])
    return short(f'In a group of {T} students in {city}, {a + b_} {A}, {b_ + c} {B} and {b_} do both. A student is chosen at random. Find (a) P(neither), (b) P(exactly one), (c) P(A ∪ B) where A = "{A}", B = "{B}".',
                 f'(a) {fx(Fr(d, T))} (b) {fx(Fr(a + c, T))} (c) {fx(Fr(a + b_ + c, T))}',
                 f'Venn regions {a}, {b_}, {c}, {d} (M1 A1); probabilities (A1 A1).', 4)


@R.add('ch12-st1', 'C3', (2, 5), 'short')
def venn_missing(rng, slot):
    a, b_, c, d = _venn(rng)
    T = a + b_ + c + d
    nA, nB = a + b_, b_ + c
    if rng.random() < 0.5:
        return short(f'n(U) = {T}, n(A) = {nA}, n(B) = {nB} and n(A ∪ B)′ = {d}. Find n(A ∩ B) and P(A ∩ B′).', f'n(A ∩ B) = {b_}; P(A ∩ B′) = {fx(Fr(a, T))}',
                     f'n(A ∪ B) = {T - d} (A1); {nA} + {nB} − n(A ∩ B) = {T - d} (M1) → {b_} (A1); A only = {a} (A1).', 4)
    pa, pb, pu = Fr(nA, T), Fr(nB, T), Fr(a + b_ + c, T)
    return short(f'P(A) = {fx(pa)}, P(B) = {fx(pb)} and P(A ∪ B) = {fx(pu)}. Find P(A ∩ B) and state, with a reason, whether A and B are mutually exclusive.', f'P(A ∩ B) = {fx(pa + pb - pu)}; {"not mutually exclusive" if pa + pb - pu else "mutually exclusive"}',
                 'Addition rule rearranged (M1); value (A1); conclusion with reason (R1).', 3)


@R.add('ch12-st1', 'C2', (2, 4), 'explain')
def venn_explain(rng, slot):
    who = name(rng)
    a, b_, c, d = _venn(rng)
    T = a + b_ + c + d
    kind = rng.choice(['double', 'me', 'comp'])
    if kind == 'double':
        return explain(f'In a class of {T}, {a + b_} play chess and {b_ + c} play guitar. {who} says {a + b_ + b_ + c} students play at least one. Explain the error.', f'The {b_} who do both are counted twice; at least one = {a + b_} + {b_ + c} − {b_} = {a + b_ + c}.', 'Double counting (R1); correct number (A1).', 2)
    if kind == 'me':
        return explain('Explain why "rolling an even number" and "rolling a 3" are mutually exclusive, but "rolling an even number" and "rolling a number greater than 3" are not.', 'No number is both even and 3; but 4 and 6 are both even and greater than 3, so those events overlap.', 'Empty intersection (R1); overlap example (R1).', 2)
    return explain(f'Explain why P(A′ ∩ B′) = 1 − P(A ∪ B).', 'A′ ∩ B′ is everything outside both circles, which is the complement of A ∪ B.', 'Complement of the union (R1); conclusion (R1).', 2)


@R.add('ch12-st1', 'C4', (3, 5), 'multi_step')
def venn_task(rng, slot):
    city = rng.choice(CITIES)
    a, b_, c, d = _venn(rng)
    T = a + b_ + c + d
    who, A, B, nb, one, ex = rng.choice([('tourists', 'visited the museum', 'visited the zoo', 'visited neither', 'visited at least one of the two', 'visited exactly one'),
                                         ('teenagers', 'use Instagram', 'use TikTok', 'use neither', 'uses at least one of the two apps', 'uses exactly one'),
                                         ('students', 'play an instrument', 'sing in a choir', 'do neither', 'does at least one of the two', 'does exactly one'),
                                         ('students', 'cycle to school on some days', 'walk to school on some days', 'do neither', 'does at least one of the two', 'does exactly one')])
    ans = f'(a) regions: A only {a}, both {b_}, B only {c}, neither {d} (b) P(A ∪ B) = {fx(Fr(a + b_ + c, T))} (c) {fx(Fr(a + b_, T))} + {fx(Fr(b_ + c, T))} − {fx(Fr(b_, T))} = {fx(Fr(a + b_ + c, T))} ✓ (d) P(exactly one) = {fx(Fr(a + c, T))}'
    q_ = (f'A survey of {T} {who} in {city} found that {a + b_} {A}, {b_ + c} {B} and {d} {nb}. Let A = "{A}" and B = "{B}". (a) Draw a Venn diagram and find every region. (b) Find the probability that one of the {who} chosen at random {one}. '
          f'(c) Verify your answer with the addition rule. (d) Find the probability that the person chosen {ex}.')
    return short(q_, ans, f'{ans}. Venn regions (M1 A1); probabilities (A1 A1); addition rule verified (R1 C1).', 6, 'multi_step', 'G5')


R.facts('ch12-st2', F(
    terms=[('conditional probability', 'P(A | B), the probability of A given that B has happened: P(A | B) = P(A ∩ B)/P(B)'),
           ('independent events', 'events where the occurrence of one does not change the probability of the other: P(A ∩ B) = P(A)P(B)'),
           ('two-way table', 'a table of counts classified by two variables, used to find joint and conditional probabilities')],
    facts=[('P(A ∩ B) = 0.12 and P(B) = 0.4. P(A | B) =', '0.3', ['0.048', '0.52', '0.28'], '0.12/0.4.'),
           ('If A and B are independent, P(A | B) =', 'P(A)', ['P(B)', 'P(A)P(B)', '0'], 'B gives no information about A.'),
           ('P(A) = 0.5, P(B) = 0.6, P(A ∩ B) = 0.3. A and B are:', 'independent', ['mutually exclusive', 'dependent', 'complementary'], '0.5 × 0.6 = 0.3.')],
    why=[('Explain why P(A | B) uses P(B) as the denominator.', 'Knowing B has happened restricts the sample space to B, so we divide by P(B).'),
         ('Explain why mutually exclusive events (with non-zero probabilities) cannot be independent.', 'If one happens the other cannot, so P(A | B) = 0 ≠ P(A): the events affect each other.'),
         ('Explain how to test two events for independence.', 'Check whether P(A ∩ B) = P(A) × P(B), or equivalently whether P(A | B) = P(A).')],
    misc=[('P(A | B) = P(B | A) always.', 'They have the same numerator but different denominators P(B) and P(A).'),
          ('Independent means the events cannot happen together.', 'That is mutually exclusive; independent means one does not affect the probability of the other.')],
))


def _twoway(rng):
    rows = rng.choice([('Grade 9', 'Grade 10'), ('boys', 'girls'), ('adults', 'children'), ('residents', 'tourists')])
    cols = rng.choice([('bus', 'bike', 'walk'), ('cinema', 'museum', 'park'), ('tea', 'coffee', 'juice'), ('football', 'swimming', 'dance')])
    t = [[rng.randint(4, 30) for _ in cols] for _ in rows]
    return rows, cols, t


def _tw_txt(rows, cols, t):
    return '; '.join(f'{r}: ' + ', '.join(f'{c} {v}' for c, v in zip(cols, row)) for r, row in zip(rows, t))


@R.add('ch12-st2', 'C1', (1, 3), 'mcq')
def cond_mcq(rng, slot):
    pab = round(rng.uniform(0.05, 0.3), 2)
    pb = round(rng.uniform(pab + 0.1, 0.8), 2)
    return mcq(rng, f'P(A ∩ B) = {g(pab)} and P(B) = {g(pb)}. Find P(A | B), to 3 s.f.', rsf(pab / pb, 3), [rsf(pab * pb, 3), rsf(pb / pab, 3), rsf(pb - pab, 3)], 'P(A ∩ B)/P(B).')


@R.add('ch12-st2', 'C3', (1, 4), 'short')
def cond_table(rng, slot):
    rows, cols, t = _twoway(rng)
    city = rng.choice(CITIES)
    i, j = rng.randrange(2), rng.randrange(3)
    rt, ct, T = sum(t[i]), sum(t[k][j] for k in range(2)), sum(map(sum, t))
    return short(f'A survey in {city} gave – {_tw_txt(rows, cols, t)}. A person is chosen at random. Find (a) P({cols[j]}), (b) P({cols[j]} | {rows[i]}), (c) P({rows[i]} | {cols[j]}).',
                 f'(a) {fx(Fr(ct, T))} (b) {fx(Fr(t[i][j], rt))} (c) {fx(Fr(t[i][j], ct))}',
                 f'Totals {T}, row {rt}, column {ct} (M1); (a) (A1); (b) restrict to the row (A1); (c) restrict to the column (A1).', 4)


@R.add('ch12-st2', 'C3', (2, 5), 'short')
def independence_test(rng, slot):
    if rng.random() < 0.5:
        pa = Fr(rng.randint(1, 9), 10)
        pb = Fr(rng.randint(1, 9), 10)
        indep = rng.random() < 0.5
        pab = pa * pb if indep else pa * pb + Fr(rng.choice([-1, 1]) * rng.randint(1, 3), 100)
        if pab <= 0 or pab > min(pa, pb):
            pab = pa * pb
            indep = True
        return short(f'P(A) = {g(float(pa))}, P(B) = {g(float(pb))} and P(A ∩ B) = {g(float(pab))}. Determine whether A and B are independent.',
                     f'P(A)P(B) = {g(float(pa * pb))} {"=" if pab == pa * pb else "≠"} P(A ∩ B): {"independent" if pab == pa * pb else "not independent"}',
                     'Product computed (M1 A1); compared and concluded (R1).', 3)
    rows, cols, t = _twoway(rng)
    j = rng.randrange(3)
    T = sum(map(sum, t))
    pj = Fr(sum(t[k][j] for k in range(2)), T)
    pj_r = Fr(t[0][j], sum(t[0]))
    return short(f'Using the table – {_tw_txt(rows, cols, t)} – determine whether choosing {cols[j]} is independent of being in the group "{rows[0]}".',
                 f'P({cols[j]}) = {fx(pj)} ≈ {rsf(float(pj), 3)}; P({cols[j]} | {rows[0]}) = {fx(pj_r)} ≈ {rsf(float(pj_r), 3)}; {"independent" if pj == pj_r else "not independent"}',
                 'Both probabilities (A1 A1); comparison and conclusion (R1).', 3)


@R.add('ch12-st2', 'C2', (2, 4), 'explain')
def cond_explain(rng, slot):
    who = name(rng)
    kind = rng.choice(['swap', 'me', 'medical'])
    if kind == 'swap':
        return explain(f'{who} says P(rain | cloudy) = P(cloudy | rain). Explain why this is usually false.', 'If it rains it is almost always cloudy (high), but cloudy days often have no rain (lower): the conditions restrict to different groups.', 'Different denominators (R1); context example (R1).', 2)
    if kind == 'me':
        return explain('Explain why two events with non-zero probabilities that are mutually exclusive cannot be independent.', 'P(A ∩ B) = 0 for mutually exclusive events, but P(A)P(B) > 0, so the independence condition fails.', 'Both conditions compared (R1 R1).', 2)
    p = rng.choice([1, 2, 5])
    return explain(f'A test for a condition affecting {p}% of people is 95% accurate. Explain why a positive result does not mean a 95% chance of having the condition.',
                   'Most people do not have the condition, so the false positives from the large healthy group can outnumber the true positives; P(condition | positive) is much less than 95%.', 'Base rate (R1); conditional reasoning (R1).', 2)


@R.add('ch12-st2', 'C4', (3, 5), 'multi_step')
def cond_task(rng, slot):
    city = rng.choice(CITIES)
    kind = rng.choice(['test', 'table'])
    if kind == 'test':
        prev = rng.choice([0.01, 0.02, 0.05, 0.1])
        sens, spec = rng.choice([0.9, 0.95, 0.99]), rng.choice([0.9, 0.95, 0.98])
        N = 10000
        D = prev * N
        tp, fp = D * sens, (N - D) * (1 - spec)
        ans = f'(a) {g(D)} have it, {g(N - D)} do not (b) true positives {g(tp)}, false positives {g(fp)} (c) P(condition | positive) = {g(tp)}/{g(tp + fp)} ≈ {rsf(tp / (tp + fp), 3)} (d) a second, independent test would reduce false alarms'
        q_ = (f'A clinic in {city} screens 10 000 people for a condition with prevalence {g(prev * 100)}%. The test detects {g(sens * 100)}% of people who have it and correctly clears {g(spec * 100)}% of those who do not. '
              f'(a) How many people have the condition? (b) Find the numbers of true and false positives. (c) Find the probability that a person who tests positive has the condition. (d) Suggest how to improve the reliability of a positive result.')
    else:
        rows, cols, t = _twoway(rng)
        T = sum(map(sum, t))
        j = rng.randrange(3)
        p_r0 = Fr(t[0][j], sum(t[0]))
        p_r1 = Fr(t[1][j], sum(t[1]))
        pj = Fr(t[0][j] + t[1][j], T)
        ans = f'(a) totals: {rows[0]} {sum(t[0])}, {rows[1]} {sum(t[1])}, {cols[j]} {t[0][j] + t[1][j]}, overall {T} (b) P({cols[j]} | {rows[0]}) = {fx(p_r0)} ≈ {rsf(float(p_r0), 3)}; P({cols[j]} | {rows[1]}) = {fx(p_r1)} ≈ {rsf(float(p_r1), 3)} (c) P({cols[j]}) = {fx(pj)} ≈ {rsf(float(pj), 3)} (d) {"independent" if p_r0 == pj else "not independent – the choice depends on the group"}'
        q_ = (f'Results of a survey in {city}: {_tw_txt(rows, cols, t)}. (a) Find the row, column and overall totals needed. (b) Find P({cols[j]} | {rows[0]}) and P({cols[j]} | {rows[1]}). '
              f'(c) Find P({cols[j]}). (d) Decide whether choosing {cols[j]} is independent of the group, and explain.')
    return short(q_, ans, f'{ans}. Counts organised (M1 A1); conditional probabilities (A1 A1); independence / context reasoning (D: R1 C1).', 6, 'multi_step', 'G5')


R.facts('ch12-st3', F(
    terms=[('with replacement', 'the item is put back before the next selection, so the probabilities stay the same for each pick'),
           ('without replacement', 'the item is not put back, so the total and some counts change for later picks'),
           ('tree diagram', 'a diagram of branches showing the outcomes and probabilities of successive events; multiply along branches, add between them')],
    facts=[('A bag has 3 red and 2 blue balls. Two are taken without replacement. P(both red) =', '3/10', ['9/25', '6/25', '1/2'], '3/5 × 2/4.'),
           ('The same bag with replacement: P(both red) =', '9/25', ['3/10', '6/20', '3/5'], '3/5 × 3/5.'),
           ('On a tree diagram, the probabilities on branches from one point add to:', '1', ['0', 'the number of branches', 'the total number of items'], 'All possibilities.')],
    why=[('Explain why the second-pick probabilities change when sampling without replacement.', 'One item has been removed, so there is one fewer item in total and possibly one fewer of the colour picked.'),
         ('Explain why you multiply along the branches of a tree diagram.', 'The probability of a sequence of events is the probability of the first times the conditional probability of the next.'),
         ('Explain why P(at least one) = 1 − P(none).', '"At least one" is everything except "none", so it is the complement.')],
    misc=[('Without replacement, P(two reds) from 4 red and 6 blue is (4/10)².', 'The second pick is 3/9: P = 4/10 × 3/9 = 2/15.'),
          ('P(one of each colour) = P(red then blue).', 'Also include blue then red: add both paths.')],
))


def _bag(rng):
    cols = rng.sample(['red', 'blue', 'green', 'yellow', 'white', 'black'], 2)
    return cols, rng.randint(2, 9), rng.randint(2, 9)


@R.add('ch12-st3', 'C1', (1, 3), 'mcq')
def replace_mcq(rng, slot):
    (c1, c2), a, b = _bag(rng)
    T = a + b
    wo = Fr(a, T) * Fr(a - 1, T - 1)
    w = Fr(a, T) ** 2
    rep = rng.random() < 0.5
    return mcq(rng, f'A bag holds {a} {c1} and {b} {c2} counters. Two are taken {"with" if rep else "without"} replacement. P(both {c1})?', fx(w if rep else wo),
               [fx(wo if rep else w), fx(Fr(a, T) * Fr(b, T)), fx(Fr(2 * a, T))] if Fr(2 * a, T) < 1 else [fx(wo if rep else w), fx(Fr(a, T) * Fr(b, T)), fx(Fr(a - 1, T))], 'Multiply along the branch.')


@R.add('ch12-st3', 'C3', (1, 4), 'short')
def replace_calc(rng, slot):
    (c1, c2), a, b = _bag(rng)
    T = a + b
    rep = rng.random() < 0.4
    p11 = Fr(a, T) * (Fr(a, T) if rep else Fr(a - 1, T - 1))
    p22 = Fr(b, T) * (Fr(b, T) if rep else Fr(b - 1, T - 1))
    p12 = 1 - p11 - p22
    obj = rng.choice(['marbles', 'sweets', 'tokens', 'cards'])
    return short(f'A jar has {a} {c1} and {b} {c2} {obj}. Two are taken at random {"with" if rep else "without"} replacement. Find (a) P(both {c1}), (b) P(one of each colour), (c) P(at least one {c2}).',
                 f'(a) {fx(p11)} (b) {fx(p12)} (c) {fx(1 - p11)}', f'Tree with {"same" if rep else "changed"} second-pick probabilities (M1); (a) (A1); (b) two paths added (A1); (c) 1 − P(both {c1}) (A1).', 4)


@R.add('ch12-st3', 'C3', (2, 5), 'short')
def replace_three(rng, slot):
    (c1, c2), a, b = _bag(rng)
    a += 2
    T = a + b
    p = Fr(a, T) * Fr(a - 1, T - 1) * Fr(a - 2, T - 2)
    if rng.random() < 0.5:
        return short(f'A team of 3 is chosen at random from {a} {c1}-shirt players and {b} {c2}-shirt players. Find the probability that all 3 wear {c1} and that at least one wears {c2}.'.replace(f'{c1}-shirt', f'{c1}-shirt').replace(f'{c2}-shirt', f'{c2}-shirt'),
                     f'{fx(p)}; {fx(1 - p)}', f'{a}/{T} × {a - 1}/{T - 1} × {a - 2}/{T - 2} (M1 A1); complement (A1).', 3)
    k = rng.randint(2, 4)
    q = Fr(a, T)
    return short(f'A spinner lands on {c1} with probability {fx(q)}. It is spun {k} times. Find P(no {c1}) and P(at least one {c1}).', f'{fx((1 - q) ** k)}; {fx(1 - (1 - q) ** k)}',
                 f'Independent spins: ({fx(1 - q)}){sup(k)} (M1 A1); complement (A1).', 3)


@R.add('ch12-st3', 'C2', (2, 4), 'explain')
def replace_explain(rng, slot):
    who = name(rng)
    (c1, c2), a, b = _bag(rng)
    T = a + b
    kind = rng.choice(['wo', 'order', 'big'])
    if kind == 'wo':
        return explain(f'A box has {a} {c1} and {b} {c2} pens. Two are taken without replacement. {who} says P(both {c1}) = ({a}/{T})². Explain the error.', f'After one {c1} pen is taken, {a - 1} {c1} remain out of {T - 1}: P = {a}/{T} × {a - 1}/{T - 1} = {fx(Fr(a * (a - 1), T * (T - 1)))}.', 'Changed denominator/numerator (R1); value (A1).', 2)
    if kind == 'order':
        return explain(f'Explain why P(one {c1} and one {c2}) needs two branches of the tree diagram.', f'The order can be {c1} then {c2}, or {c2} then {c1}; both sequences give one of each, so their probabilities are added.', 'Two orders (R1); add (R1).', 2)
    return explain('Explain why, for a very large population, sampling without replacement gives almost the same probabilities as with replacement.', 'Removing one item barely changes the totals, so the second-pick probabilities are almost unchanged.', 'Effect of size (R1); conclusion (R1).', 2)


@R.add('ch12-st3', 'C4', (3, 5), 'multi_step')
def replace_task(rng, slot):
    city = rng.choice(CITIES)
    kind = rng.choice(['quality', 'raffle', 'compare'])
    if kind == 'quality':
        N, d = rng.choice([20, 25, 30]), rng.randint(2, 5)
        p0 = Fr(N - d, N) * Fr(N - d - 1, N - 1)
        p0r = Fr(N - d, N) ** 2
        ans = f'(a) {fx(p0)} (b) {fx(1 - p0)} (c) with replacement: {fx(p0r)} – slightly larger chance of no faulty item (d) without replacement is realistic because inspected items are not put back'
        q_ = (f'A box of {N} phone chargers in a shop in {city} contains {d} faulty ones. An inspector tests 2 at random without replacement. (a) Find P(neither is faulty). (b) Find P(at least one is faulty). '
              f'(c) Compare with sampling with replacement. (d) Explain which model is realistic.')
    elif kind == 'raffle':
        N, w = rng.choice([50, 80, 100]), rng.choice([2, 3])
        k = rng.randint(2, 5)
        p_none = 1
        for i in range(w):
            p_none *= Fr(N - k - i, N - i)
        ans = f'(a) {fx(Fr(k, N))} (b) {fx(p_none)} (c) {fx(1 - p_none)} (d) buying more tickets increases the chance, but each extra ticket adds less than the last'
        q_ = (f'A charity raffle in {city} sells {N} tickets and draws {w} winners without replacement. Ana buys {k} tickets. (a) Find the probability that her ticket wins the first draw. (b) Find the probability that she wins nothing. '
              f'(c) Find the probability that she wins at least one prize. (d) Comment on buying more tickets.')
    else:
        (c1, c2), a, b = _bag(rng)
        T = a + b
        wo = Fr(a * (a - 1), T * (T - 1))
        w = Fr(a * a, T * T)
        ans = f'(a) with: {fx(w)} (b) without: {fx(wo)} (c) with replacement is larger, because without replacement there are fewer {c1} left (d) the difference shrinks as the numbers grow'
        q_ = (f'Investigate a bag of {a} {c1} and {b} {c2} balls. (a) Find P(two {c1}) with replacement. (b) Find it without replacement. (c) Explain which is larger and why. (d) Predict what happens to the difference for a bag with 10 times as many of each colour.')
    return short(q_, ans, f'{ans}. Tree / product rule (M1 A1); probabilities (A1 A1); comparison and context (D: R1 C1).', 6, 'multi_step', 'G5')


R.facts('ch12-st4', F(
    terms=[('product rule for counting', 'if one choice can be made in m ways and a second in n ways, together they can be made in m × n ways'),
           ('factorial', 'the product n! = n × (n − 1) × … × 2 × 1, the number of ways to arrange n different items in order'),
           ('expected value', 'E(X) = Σ x P(x), the long-run average value of a random variable'),
           ('fair game', 'a game in which the expected gain of each player is zero')],
    facts=[('How many ways can 4 different books be arranged on a shelf?', '24', ['16', '4', '10'], '4! = 24.'),
           ('A menu has 3 starters and 5 mains. How many two-course meals?', '15', ['8', '35', '53'], '3 × 5.'),
           ('A game pays $10 with probability 0.2 and nothing otherwise. E(winnings) =', '$2', ['$10', '$8', '$0.20'], '10 × 0.2.')],
    why=[('Explain why the number of 4-digit PINs is 10⁴.', 'Each of the 4 positions can be any of the 10 digits independently, so 10 × 10 × 10 × 10.'),
         ('Explain why a fair game has an expected gain of zero.', 'In the long run neither side wins or loses on average, so the average gain is 0.'),
         ('Explain why the expected value need not be a possible outcome.', 'It is a long-run average; e.g. the expected score of a dice is 3.5, which cannot be rolled.')],
    misc=[('The number of ways to arrange 5 people in a line is 5 × 5.', 'Choices reduce each time: 5 × 4 × 3 × 2 × 1 = 120.'),
          ('An expected value of $2 means you win $2 each time.', 'It is the average over many plays; single results vary.')],
))


@R.add('ch12-st4', 'C1', (1, 3), 'mcq')
def counting_mcq(rng, slot):
    kind = rng.choice(['arr', 'prod', 'pin'])
    if kind == 'arr':
        n = rng.randint(4, 7)
        return mcq(rng, f'In how many ways can {n} different trophies be arranged in a row?', str(math.factorial(n)), [str(n * n), str(n ** n), str(n * (n - 1))], f'{n}! = {math.factorial(n)}.')
    if kind == 'prod':
        a, b, c = rng.randint(2, 6), rng.randint(2, 6), rng.randint(2, 5)
        return mcq(rng, f'A café offers {a} drinks, {b} sandwiches and {c} desserts. How many meal deals of one of each?', str(a * b * c), [str(a + b + c), str(a * b + c), str((a + b) * c)], f'{a} × {b} × {c}.')
    k = rng.randint(3, 5)
    return mcq(rng, f'How many {k}-letter codes can be made from the 26 letters if letters may repeat?', big(26 ** k), [big(26 * k), big(math.perm(26, k)), big(k ** 26) if k ** 26 < 1e12 else big(26 * 25)], f'26{sup(k)}.')


@R.add('ch12-st4', 'C3', (1, 4), 'short')
def counting_calc(rng, slot):
    city = rng.choice(CITIES)
    kind = rng.choice(['perm', 'nopeat', 'plates', 'podium'])
    if kind == 'perm':
        n = rng.randint(5, 9)
        return short(f'In how many ways can {n} runners from a club in {city} line up for a photo? How many if two particular runners must stand at the ends?', f'{big(math.factorial(n))}; {big(2 * math.factorial(n - 2))}',
                     f'{n}! (M1 A1); 2 × {n - 2}! (A1).', 3)
    if kind == 'nopeat':
        d = rng.randint(3, 5)
        return short(f'How many {d}-digit PINs can be made if digits may repeat? How many if no digit is repeated?', f'{big(10 ** d)}; {big(math.perm(10, d))}', f'10{sup(d)} (A1); 10 × 9 × … ({d} factors) (M1 A1).', 3)
    if kind == 'plates':
        L, D = rng.randint(2, 3), rng.randint(3, 4)
        return short(f'Number plates in {city} have {L} letters followed by {D} digits (repeats allowed). How many plates are possible?', big(26 ** L * 10 ** D), f'26{sup(L)} × 10{sup(D)} (M1 A1) = {big(26 ** L * 10 ** D)} (A1).', 3)
    n = rng.randint(8, 20)
    return short(f'{n} students enter a competition in {city}. In how many ways can gold, silver and bronze be awarded?', big(n * (n - 1) * (n - 2)), f'{n} × {n - 1} × {n - 2} (M1 A1) = {big(n * (n - 1) * (n - 2))} (A1).', 3)


@R.add('ch12-st4', 'C3', (2, 5), 'short')
def expected_value(rng, slot):
    city, country, cur, cname = place(rng)
    cost = rng.choice([1, 2, 5])
    prizes = sorted(rng.sample([2, 5, 10, 20, 50], 2))
    ps = [Fr(rng.randint(1, 10), 100), Fr(rng.randint(1, 5), 100)]
    E = prizes[0] * ps[0] + prizes[1] * ps[1]
    gain = E - cost
    return short(f'A game at a festival in {city} costs {money(cur, cost, 0)}. You win {money(cur, prizes[0], 0)} with probability {g(float(ps[0]))} and {money(cur, prizes[1], 0)} with probability {g(float(ps[1]))}; otherwise nothing. Find the expected winnings and the expected gain per game. Is the game fair?',
                 f'E(winnings) = {cash(cur, E)}; expected gain {"−" if gain < 0 else ""}{cash(cur, abs(gain))}; {"fair" if gain == 0 else "not fair"}',
                 f'Σ x P(x) (M1) = {cash(cur, E)} (A1); minus the cost (A1); fairness (R1).', 4)


@R.add('ch12-st4', 'C2', (2, 4), 'explain')
def counting_explain(rng, slot):
    who = name(rng)
    n = rng.randint(4, 7)
    kind = rng.choice(['arr', 'ev', 'fair'])
    if kind == 'arr':
        return explain(f'{who} says {n} people can sit in a row of {n} chairs in {n} × {n} = {n * n} ways. Explain the error.', f'Once a person is seated they cannot be chosen again: {n} × {n - 1} × … × 1 = {n}! = {math.factorial(n)}.', 'Choices decrease (R1); value (A1).', 2)
    if kind == 'ev':
        return explain('Explain why the expected score when rolling a fair dice is 3.5 even though 3.5 cannot be rolled.', 'E = (1 + 2 + … + 6)/6 = 3.5 is the long-run average of many rolls, not a single outcome.', 'Long-run average (R1); calculation (A1).', 2)
    return explain('Explain how a charity can design a game that is unfair but still acceptable to players.', 'The expected gain for players is negative (the charity profits), but players accept this as a donation and for the enjoyment of the chance to win.', 'Negative expected value (R1); context (R1).', 2)


@R.add('ch12-st4', 'C4', (3, 5), 'multi_step')
def counting_task(rng, slot):
    city, country, cur, cname = place(rng)
    kind = rng.choice(['lottery', 'design', 'passwords'])
    if kind == 'lottery':
        n, k = rng.choice([(20, 3), (25, 3), (30, 3), (15, 4)])
        tot = math.comb(n, k)
        price, prize = rng.choice([1, 2]), rng.choice([500, 1000, 2000])
        E = Fr(prize, tot) - price
        ans = f'(a) {big(tot)} (b) 1/{big(tot)} (c) {cash(cur, float(Fr(prize, tot)))} winnings; gain {"−" if E < 0 else ""}{cash(cur, abs(float(E)))} per ticket (d) the prize should be {money(cur, price * tot, 0)} for a fair game'
        q_ = (f'A school lottery in {city} asks players to choose {k} different numbers from 1 to {n} (order does not matter). (a) Find the number of possible selections. (b) Find the probability of winning with one ticket. '
              f'(c) A ticket costs {money(cur, price, 0)} and the prize is {money(cur, prize, 0)}. Find the expected gain per ticket. (d) Find the prize that would make the game fair.')
    elif kind == 'design':
        cost = rng.choice([2, 3, 5])
        n = rng.choice([6, 8, 10])
        prize = cost * n // 2
        E = Fr(prize, n) - cost
        ans = f'(a) P(win) = 1/{n}, expected gain {"−" if E < 0 else ""}{cash(cur, abs(float(E)))} (b) profit about {cash(cur, -float(E) * 200)} from 200 players (c) a prize of {money(cur, cost * n, 0)} makes it fair (d) results vary; the stall can still lose on a given day'
        q_ = (f'A stall in {city} charges {money(cur, cost, 0)} to spin a fair {n}-sided spinner; one section wins {money(cur, prize, 0)}. (a) Find the expected gain for a player. (b) Estimate the stall’s profit from 200 players. '
              f'(c) Find the prize that makes the game fair. (d) Explain why the stall might still lose money.')
    else:
        L, D = rng.choice([(4, 2), (5, 1), (3, 3)])
        tot = 26 ** L * 10 ** D
        rate = rng.choice([1000, 10000, 100000])
        ans = f'(a) 26{sup(L)} × 10{sup(D)} = {big(tot)} (b) {rsf(tot / rate / 3600, 3)} hours at {big(rate)} guesses per second (c) adding capitals: 52{sup(L)} × 10{sup(D)} = {big(52 ** L * 10 ** D)} (d) longer passwords increase the count exponentially'
        q_ = (f'A website in {city} uses passwords of {L} lower-case letters followed by {D} digit{"s" if D > 1 else ""}. (a) Find the number of possible passwords. (b) How long would it take a computer to try them all at {big(rate)} guesses per second? '
              f'(c) Find the number if capital letters are also allowed. (d) Explain why length matters more than character types.')
    return short(q_, ans, f'{ans}. Counting principle applied (M1 A1); probability / expected value (A1 A1); fairness or security discussed in context (D: R1).', 6, 'multi_step', 'G5')

