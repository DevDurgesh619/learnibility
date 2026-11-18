"""IB MYP 3 Mathematics (Standard & Extended) – ib-g8-maths.

Criteria language: A knowing & understanding, B investigating patterns, C communicating,
D applying mathematics in real-life contexts. Items use international contexts; every
numerical answer is computed (fractions / sympy / decimal rounding), never typed in.
Structure follows the validated MYP 4 pack (ib_g9_maths.py).
"""
from __future__ import annotations

import math
import random
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as Fr

import sympy as sp

from _common import F, Registry, T, fmt, frac, mcq, name, num_distractors, pe, sup, two_names, CITIES
from ib_myp_maths_common import PLACES, place, money, m, lin, poly, sgn, fr, g, dp, ordinal, explain, short, x, y

CONFIG = {'minutesPerMark': 1.25, 'mcqMinutes': 1.5}

# MYP 3 has no external exam; the mock mirrors the MYP 5 eAssessment (3 tasks, 25 items) so it is practised early.
MOCK = [
    dict(section='Task 1 – Knowing and understanding (criterion A)', count=10, c=['C1', 'C3'], d=[2, 2, 3], marks=3),
    dict(section='Task 2 – Investigating patterns (criterion B)', count=7, c=['C2', 'C3', 'C4'], d=[3, 3, 4], marks=4),
    dict(section='Task 3 – Applying mathematics in real-life contexts (criterion D)', count=8, c=['C3', 'C4'], d=[3, 4, 4, 5], marks=5),
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


def rsf(v, sf):
    """Round half up to sf significant figures; returns a plain string."""
    d = Decimal(str(v))
    if d == 0:
        return '0'
    e = d.adjusted()
    q = Decimal(1).scaleb(e - sf + 1)
    r = d.quantize(q, rounding=ROUND_HALF_UP)
    if e - sf + 1 >= 0:
        return f'{int(r)}'
    return f'{r:f}'


def fx(v: Fr) -> str:
    """Fraction as text (mixed numbers avoided; improper is fine in MYP), typographic minus."""
    return m(frac(Fr(v)))


# =============================================================================================
# ch01 Rational Numbers and Number Sets
# =============================================================================================
R.facts('ch01-st1', F(
    terms=[('natural number', 'a counting number 1, 2, 3, … (the set ℕ; in some texts ℕ also contains 0)'),
           ('integer', 'a whole number that may be positive, negative or zero (the set ℤ)'),
           ('rational number', 'a number that can be written as a/b where a and b are integers and b ≠ 0 (the set ℚ)'),
           ('irrational number', 'a number such as √2 or π that cannot be written as a fraction of two integers')],
    facts=[('Which statement about number sets is true?', 'Every integer is a rational number', ['Every rational number is an integer', 'Every integer is a natural number', 'No negative number is rational'], 'Any integer n can be written as n/1, so ℤ ⊂ ℚ.'),
           ('Which of the following numbers is an integer but NOT a natural number?', '−6', ['6', '0.6', '6/5'], '−6 is a whole number but is negative, so it is not a counting number.'),
           ('Which symbol is used for the set of rational numbers?', 'ℚ', ['ℕ', 'ℤ', 'ℝ'], 'ℚ comes from "quotient": rationals are quotients of integers.'),
           ('Which of the following is NOT a rational number?', '√7', ['−3/4', '0.25', '√49'], '7 is not a square number, so √7 is irrational; √49 = 7 is rational.')],
    why=[('Explain why −5 is a rational number.', '−5 can be written as −5/1 (or −10/2), a ratio of two integers with a non-zero denominator, so it is rational.'),
         ('Explain why 0 is an integer but cannot be used as the denominator of a rational number.', '0 is a whole number so it is in ℤ; but division by zero is undefined, so a/0 has no value and the definition requires b ≠ 0.'),
         ('Explain why a terminating decimal such as 2.375 is rational.', '2.375 = 2375/1000 = 19/8, a ratio of two integers, so it is rational.'),
         ('Explain why the set of natural numbers is a subset of the set of integers.', 'Every counting number 1, 2, 3, … is also a whole number, so it is in ℤ as well; ℤ just adds 0 and the negatives.')],
    misc=[('Fractions are not integers, so 12/4 is not an integer.', '12/4 simplifies to 3, which is an integer; a number is classified by its value, not by how it is written.'),
          ('Negative numbers cannot be rational because a ratio must be positive.', 'A ratio of integers can be negative, e.g. −3/4 = (−3)/4, so negative fractions are rational.'),
          ('0.333… is not rational because its decimal never ends.', 'Its digits recur: 0.333… = 1/3, so it is rational. Only non-terminating, non-recurring decimals are irrational.')],
    contrast=[('natural numbers', 'integers', 'Natural numbers are the counting numbers 1, 2, 3, …; integers also include 0 and the negative whole numbers.'),
              ('rational numbers', 'irrational numbers', 'A rational number can be written as a/b with integers a, b (b ≠ 0) and has a terminating or recurring decimal; an irrational number cannot, and its decimal neither terminates nor recurs.')],
))


def _num_pool(rng):
    """Random mix of numbers with their classification (natural, integer, rational)."""
    pool = []
    nat = rng.randint(2, 30)
    pool.append((str(nat), 'N'))
    neg = -rng.randint(1, 20)
    pool.append((m(neg), 'Z'))
    a, b = rng.randint(1, 9), rng.choice([2, 3, 4, 5, 7, 8])
    if a % b == 0:
        a += 1
    pool.append((f'{a}/{b}' if rng.random() < 0.5 else f'−{a}/{b}', 'Q'))
    k = rng.randint(2, 6)
    pool.append((f'{k * rng.choice([2, 3, 4])}/{k}' if rng.random() < 0.5 else f'√{k * k}', 'N'))
    pool.append((f'{rng.randint(1, 9)}.{rng.randint(1, 99):02d}', 'Q'))
    ns = rng.choice([2, 3, 5, 6, 7, 10, 11])
    pool.append((f'√{ns}', 'I'))
    pool.append(('0', 'Z'))
    rng.shuffle(pool)
    return pool[:rng.randint(5, 7)]


@R.add('ch01-st1', 'C3', (1, 4), 'short')
def classify_list(rng, slot):
    pool = _num_pool(rng)
    nums = ', '.join(s for s, _ in pool)
    nat = [s for s, k in pool if k == 'N']
    ints = [s for s, k in pool if k in 'NZ']
    rat = [s for s, k in pool if k in 'NZQ']
    irr = [s for s, k in pool if k == 'I']
    if slot.d <= 2:
        which = rng.choice(['integers', 'rational numbers'])
        lst = ints if which == 'integers' else rat
        return short(f'From the list {nums}, write down all the {which}.', ', '.join(lst) or 'none',
                     f'{", ".join(lst)} (A1 all correct, A1 no extras). Values such as √a or a/b must be simplified before classifying.', 2)
    return short(f'Copy and complete: sort the numbers {nums} into natural numbers, integers that are not natural, rational numbers that are not integers, and irrational numbers.',
                 f'ℕ: {", ".join(nat) or "none"}; ℤ only: {", ".join(s for s, k in pool if k == "Z") or "none"}; ℚ only: {", ".join(s for s, k in pool if k == "Q") or "none"}; irrational: {", ".join(irr) or "none"}',
                 'A1 for each correctly completed group (4 groups). Simplify √(square) and whole-number fractions first (criterion C: correct set notation ℕ, ℤ, ℚ).', 4)


@R.add('ch01-st1', 'C3', (1, 3), 'short')
def order_rationals(rng, slot):
    vals = set()
    while len(vals) < (4 if slot.d <= 2 else 6):
        t = rng.choice(['int', 'frac', 'dec'])
        if t == 'int':
            vals.add(Fr(rng.randint(-9, 9)))
        elif t == 'frac':
            vals.add(Fr(rng.choice([-1, 1]) * rng.randint(1, 11), rng.choice([2, 3, 4, 5, 8])))
        else:
            vals.add(Fr(rng.randint(-95, 95), 10 if rng.random() < 0.5 else 100))
    vals = list(vals)
    rng.shuffle(vals)

    def show(v):
        if v.denominator == 1:
            return m(v.numerator)
        if v.denominator in (10, 100, 5, 2) and rng.random() < 0.6:
            return m(f'{float(v):g}')
        return fx(v)
    shown = [(show(v), v) for v in vals]
    asc = sorted(shown, key=lambda t: t[1])
    order = rng.choice(['ascending', 'descending'])
    res = asc if order == 'ascending' else asc[::-1]
    return short(f'Write these numbers in {order} order: {", ".join(s for s, _ in shown)}.', ', '.join(s for s, _ in res),
                 f'Convert to decimals to compare ({", ".join(f"{s} = {m(f'{float(v):.3g}')}" for s, v in shown)}) (M1); {", ".join(s for s, _ in res)} (A1).', 2)


@R.add('ch01-st1', 'C1', (1, 3), 'mcq')
def smallest_set_mcq(rng, slot):
    kind = rng.choice(['N', 'Z', 'Q', 'I'])
    if kind == 'N':
        k = rng.randint(2, 9)
        v = rng.choice([f'{k * k * 2}/{k * 2}' if False else f'{k * 3}/3', f'√{k * k}'])
        corr = 'ℕ (natural numbers)'
    elif kind == 'Z':
        v = m(-rng.randint(1, 40))
        corr = 'ℤ (integers)'
    elif kind == 'Q':
        a, b = rng.randint(1, 9), rng.choice([3, 7, 9, 11])
        v = rng.choice([f'{a}/{b}' if a % b else f'{a + 1}/{b}', f'−{rng.randint(1, 9)}.{rng.randint(1, 9)}'])
        corr = 'ℚ (rational numbers)'
    else:
        v = rng.choice(['π', f'√{rng.choice([2, 3, 5, 8, 10, 12])}'])
        corr = 'irrational numbers'
    opts = ['ℕ (natural numbers)', 'ℤ (integers)', 'ℚ (rational numbers)', 'irrational numbers']
    return mcq(rng, f'What is the smallest of these sets that contains the number {v}?', corr, [o for o in opts if o != corr],
               f'{v} belongs to {corr}; the sets are nested ℕ ⊂ ℤ ⊂ ℚ.')


@R.add('ch01-st1', 'C2', (2, 4), 'explain')
def show_rational(rng, slot):
    kind = rng.choice(['dec', 'int', 'mixed'])
    if kind == 'dec':
        d = Fr(rng.randint(101, 999), rng.choice([100, 1000]))
        dtxt = f'{float(d):g}'
        return explain(f'Show that {dtxt} is a rational number, writing it in the form a/b in simplest terms.', fx(d),
                       f'{dtxt} = {d.numerator * (1000 // d.denominator) if d.denominator <= 1000 else d.numerator}/{1000} … simplifies to {fx(d)} (M1 A1); a and b are integers with b ≠ 0 (R1).', 3)
    if kind == 'int':
        k = -rng.randint(2, 30)
        return explain(f'Explain why {m(k)} belongs to ℤ and to ℚ but not to ℕ.', f'{m(k)} is a whole number (ℤ), equals {m(k)}/1 (ℚ), but is negative so it is not a counting number (not ℕ).',
                       'R1 for each of the three parts of the reason.', 3)
    w, a, b = rng.randint(1, 5), rng.randint(1, 4), rng.choice([5, 6, 7, 9])
    v = Fr(w * b + a, b)
    return explain(f'Explain why the mixed number {w} {a}/{b} is rational but not an integer.', f'{w} {a}/{b} = {fx(v)}, a ratio of integers; it lies between {w} and {w + 1}, so it is not whole.',
                   f'Convert to {fx(v)} (M1); ratio of integers so rational (R1); between consecutive integers so not an integer (R1).', 3)


@R.add('ch01-st1', 'C4', (3, 5), 'multi_step')
def between_rationals(rng, slot):
    a, b = rng.randint(1, 5), rng.choice([3, 4, 5, 7])
    c, d_ = a + 1, b
    p, q = Fr(a, b), Fr(c, d_)
    mid = (p + q) / 2
    who = name(rng)
    frames = [
        (f'{who} claims there is no rational number between {fx(p)} and {fx(q)}. (a) Find the number exactly halfway between them. (b) Find two more rational numbers between them. (c) Explain why there is always another rational number between any two different rational numbers.',
         f'(a) {fx(mid)} (b) e.g. {fx((p + mid) / 2)} and {fx((mid + q) / 2)} (c) the mean of two rationals is rational and lies between them, so the process never ends'),
        (f'Investigate the pattern: the rational numbers halfway between 0 and 1, then between 0 and that number, and so on. Write the first five numbers, find the nth number and explain whether the list ever reaches 0.',
         '1/2, 1/4, 1/8, 1/16, 1/32; nth number 1/2ⁿ; it never reaches 0 because 1/2ⁿ > 0 for every n'),
        (f'The integers between −{a + 2} and {b} are written on cards. (a) How many cards are there? (b) How many of them are natural numbers? (c) A rational card {fx(Fr(-1, b))} is added – explain which set it belongs to and why it does not fit in the first group.',
         f'(a) {b + a + 2 - 1} (b) {b - 1} (c) {fx(Fr(-1, b))} is in ℚ but not ℤ, since it is a negative fraction between −1 and 0'),
    ]
    q_, ans = rng.choice(frames)
    return short(q_, ans, f'{ans}. Method/pattern described (B: M1 A1), general rule or reason stated (R1), clear communication with correct notation (C1).', 5, 'multi_step', 'G5')


R.facts('ch01-st2', F(
    terms=[('reciprocal', 'the number which multiplies by a given number to give 1; the reciprocal of a/b is b/a'),
           ('lowest common denominator', 'the smallest number that all the denominators divide into exactly, used to add or subtract fractions'),
           ('order of operations', 'the convention for evaluating expressions: brackets, then exponents, then multiplication and division (left to right), then addition and subtraction (left to right)')],
    facts=[('What is (−6) × (−4)?', '24', ['−24', '−10', '10'], 'Negative × negative = positive.'),
           ('What is −15 ÷ 3?', '−5', ['5', '−45', '−12'], 'Negative ÷ positive = negative.'),
           ('What is 2/3 ÷ 4/9?', '3/2', ['8/27', '6/12', '2/3'], 'Multiply by the reciprocal: 2/3 × 9/4 = 18/12 = 3/2.'),
           ('What is −3 − (−8)?', '5', ['−11', '11', '−5'], 'Subtracting a negative adds: −3 + 8 = 5.')],
    why=[('Explain why dividing by 1/4 gives the same result as multiplying by 4.', 'Dividing by 1/4 asks how many quarters fit into the number; there are 4 quarters in every 1, so the answer is 4 times the number.'),
         ('Explain why subtracting a negative number gives the same result as adding the positive number.', 'Subtracting −b removes a debt of b, which increases the value by b; on a number line, subtracting −b moves the same way as adding b.'),
         ('Explain why fractions must have a common denominator before they are added.', 'Only parts of the same size can be counted together; a common denominator rewrites both fractions in equal-sized parts.'),
         ('Explain why the product of an even number of negative factors is positive.', 'Negative factors can be paired; each pair multiplies to a positive number, and a product of positives is positive.')],
    misc=[('1/3 + 1/4 = 2/7', 'Denominators are not added: 1/3 + 1/4 = 4/12 + 3/12 = 7/12.'),
          ('−4² = 16', 'The exponent applies before the negative sign: −4² = −(4 × 4) = −16; (−4)² = 16.'),
          ('0.3 × 0.2 = 0.6', 'There are two decimal places in total, so 0.3 × 0.2 = 0.06.'),
          ('Dividing always makes a number smaller.', 'Dividing by a number between 0 and 1 makes it larger, e.g. 6 ÷ 0.5 = 12.')],
))


def _rfrac(rng, hi=9, neg=False):
    b = rng.choice([2, 3, 4, 5, 6, 8, 9, 10, 12])
    a = rng.randint(1, min(hi, 2 * b))
    v = Fr(a, b)
    if v.denominator == 1:
        v = Fr(a, b + 1)
    if neg and rng.random() < 0.4:
        v = -v
    return v


def _ftxt(v):
    t = frac(v)
    return f'({m(t)})' if v < 0 else t


@R.add('ch01-st2', 'C3', (1, 4), 'short')
def frac_ops(rng, slot):
    a, b = _rfrac(rng, neg=slot.d >= 3), _rfrac(rng, neg=slot.d >= 3)
    op = rng.choice(['+', '−', '×', '÷'])
    res = {'+': a + b, '−': a - b, '×': a * b, '÷': a / b}[op]
    if slot.d >= 4:
        c = _rfrac(rng)
        op2 = rng.choice(['+', '−'])
        res2 = res + c if op2 == '+' else res - c
        return short(f'Work out ({_ftxt(a)} {op} {_ftxt(b)}) {op2} {_ftxt(c)}, giving your answer as a fraction in its simplest form.', fx(res2),
                     f'Bracket first: {fx(res)} (M1 A1); then {op2} {frac(c)} using a common denominator (M1); {fx(res2)} (A1).', 4)
    how = {'+': 'common denominator', '−': 'common denominator', '×': 'multiply numerators and denominators', '÷': 'multiply by the reciprocal'}[op]
    return short(f'Calculate {_ftxt(a)} {op} {_ftxt(b)}, giving your answer in its simplest form.', fx(res),
                 f'{how[0].upper() + how[1:]} (M1); {fx(res)} (A1).', 2)


@R.add('ch01-st2', 'C3', (1, 4), 'short')
def neg_order_ops(rng, slot):
    a, b, c, d_ = [rng.choice([i for i in range(-12, 13) if i != 0]) for _ in range(4)]
    forms = [
        (f'{m(a)} − {m(b) if b > 0 else f"({m(b)})"} × {m(c) if c > 0 else f"({m(c)})"}', a - b * c),
        (f'({m(a)} + {m(b) if b > 0 else f"({m(b)})"})² ÷ {m(abs(c))}', Fr((a + b) ** 2, abs(c))),
        (f'{m(a)} × ({m(b)} − {m(c) if c > 0 else f"({m(c)})"}) + {m(d_) if d_ > 0 else f"({m(d_)})"}', a * (b - c) + d_),
        (f'({m(a * c)}) ÷ ({m(c)}) − ({m(b)})²', Fr(a * c, c) - b * b),
    ]
    e, v = rng.choice(forms[:2] if slot.d <= 2 else forms)
    return short(f'Without a calculator, evaluate {e}.', fx(Fr(v)),
                 f'Apply the order of operations (brackets, exponents, × ÷, + −) with the sign rules (M1 M1); {fx(Fr(v))} (A1).', 3 if slot.d >= 3 else 2)


@R.add('ch01-st2', 'C3', (2, 4), 'numerical')
def decimal_ops(rng, slot):
    a = Decimal(rng.randint(11, 999)) / Decimal(10 ** rng.randint(1, 2))
    b = Decimal(rng.randint(2, 99)) / Decimal(10 ** rng.randint(1, 2))
    op = rng.choice(['×', '÷'])
    if op == '÷':
        a = (a * b).normalize()
        res = (a / b).normalize()
    else:
        res = (a * b).normalize()
    if rng.random() < 0.4:
        a = -a
        res = -res
    return short(f'Without a calculator, work out {m(f"{a:f}")} {op} {m(f"{b:f}")}.', m(f'{res:f}'),
                 f'Work with whole numbers then place the decimal point ({"count decimal places" if op == "×" else "multiply both numbers by a power of 10 so the divisor is whole"}) (M1); sign rule (M1); {m(f"{res:f}")} (A1).', 3, 'numerical')


@R.add('ch01-st2', 'C1', (1, 3), 'mcq')
def sign_mcq(rng, slot):
    a, b = rng.randint(2, 12), rng.randint(2, 12)
    kind = rng.choice(['mul', 'div', 'sub', 'add'])
    if kind == 'mul':
        stem, v, w = f'(−{a}) × (−{b})', a * b, [-a * b, -(a + b), a + b]
    elif kind == 'div':
        stem, v, w = f'(−{a * b}) ÷ {b}', -a, [a, -a * b * b, a * b]
    elif kind == 'sub':
        stem, v, w = f'−{a} − (−{b})', -a + b, [-a - b, a + b, a - b]
    else:
        stem, v, w = f'−{a} + (−{b})', -a - b, [-a + b, a + b, a * b]
    return mcq(rng, f'What is the value of {stem}?', m(v), [m(t) for t in w], f'{stem} = {m(v)} using the sign rules.')


@R.add('ch01-st2', 'C2', (2, 4), 'explain')
def frac_error(rng, slot):
    a, b = _rfrac(rng), _rfrac(rng)
    who = name(rng)
    kind = rng.choice(['add', 'div', 'neg'])
    if kind == 'add' and a.denominator != b.denominator:
        wrong = Fr(a.numerator + b.numerator, a.denominator + b.denominator)
        return explain(f'{who} writes {frac(a)} + {frac(b)} = {a.numerator + b.numerator}/{a.denominator + b.denominator}. Explain the mistake and give the correct answer.', fx(a + b),
                       f'Numerators and denominators were added separately (R1); a common denominator is needed (M1); {fx(a + b)} (A1).', 3, 'G2')
    if kind == 'div':
        return explain(f'{who} works out {frac(a)} ÷ {frac(b)} by multiplying {frac(a)} by {frac(b)}. Explain why this is wrong and find the correct value.', fx(a / b),
                       f'Division by a fraction is multiplication by its reciprocal {frac(1 / b)} (R1); {fx(a / b)} (A1).', 2, 'G2')
    n = rng.randint(2, 9)
    return explain(f'{who} says that (−{n})³ and −{n}³ have different values. Explain whether this is correct.', f'Not correct: both equal −{n ** 3}.',
                   f'(−{n})³ = (−{n})(−{n})(−{n}) = −{n ** 3} (M1); −{n}³ = −({n ** 3}) (M1); they are equal for an odd power (R1).', 3)


@R.add('ch01-st2', 'C4', (2, 5), 'multi_step')
def neg_context(rng, slot):
    city, country, cur, cname = place(rng)
    who = name(rng)
    t0 = rng.randint(-8, 6)
    drops = [rng.randint(2, 7) for _ in range(3)]
    rise = rng.randint(3, 12)
    t_end = t0 - sum(drops) + rise
    serves, want = rng.choice([4, 6, 8]), rng.choice([3, 5, 10, 12])
    flour = Fr(rng.randint(1, 3) * 2 + 1, 4)
    need = flour * Fr(want, serves)
    bal = rng.randint(20, 70)
    spend = [rng.randint(25, 60) for _ in range(3)]
    dep = rng.randint(30, 90)
    endb = bal - sum(spend) + dep
    frames = [
        (f'At 18:00 the temperature in a mountain village near {city} was {m(t0)} °C. It fell by {drops[0]} °C, then {drops[1]} °C, then {drops[2]} °C overnight, and rose by {rise} °C by midday. (a) Find the lowest temperature. (b) Find the midday temperature. (c) Find the difference between the highest and lowest temperatures recorded.',
         f'(a) {m(t0 - sum(drops))} °C (b) {m(t_end)} °C (c) {max(t0, t_end) - (t0 - sum(drops))} °C'),
        (f'A recipe for {serves} people uses {frac(flour)} kg of flour. {who} wants to cook for {want} people. (a) How much flour is needed? (b) Flour is sold in 1/4 kg bags – how many bags must be bought?',
         f'(a) {fx(need)} kg (b) {math.ceil(need / Fr(1, 4))} bags'),
        (f'{who}’s bank account in {country} starts with {cur}{bal}. Three payments of {cur}{spend[0]}, {cur}{spend[1]} and {cur}{spend[2]} are made, then {cur}{dep} is paid in. (a) Write a single calculation with directed numbers and find the final balance. (b) Find the lowest balance reached, given that the payments came before the deposit, and explain what a negative balance means.',
         f'(a) {bal} − {spend[0]} − {spend[1]} − {spend[2]} + {dep} = {m(endb)} (b) {cur}{m(bal - sum(spend))} (overdrawn: the account owes the bank money)'),
    ]
    q_, ans = rng.choice(frames)
    return short(q_, ans, f'{ans}. Correct directed-number or fraction operations (M1 M1), each part answered (A1 A1), interpreted in context with units (D: R1).', 5, 'multi_step', 'G5')


R.facts('ch01-st3', F(
    terms=[('terminating decimal', 'a decimal with a finite number of digits, such as 0.375'),
           ('recurring decimal', 'a decimal in which a digit or block of digits repeats forever, such as 0.272727… = 0.2̅7̅'),
           ('percentage', 'a fraction with denominator 100, written with the symbol %')],
    facts=[('Which fraction is equal to 0.625?', '5/8', ['5/6', '6/25', '3/5'], '0.625 = 625/1000 = 5/8.'),
           ('Which of these fractions gives a recurring decimal?', '5/12', ['7/8', '3/20', '9/25'], '12 = 2² × 3 has a prime factor 3, so 5/12 = 0.41666… recurs.'),
           ('What is 0.4̅ (0.444…) as a fraction?', '4/9', ['4/10', '2/5', '44/100'], 'x = 0.444…, 10x − x = 4, so x = 4/9.'),
           ('What is 3/8 as a percentage?', '37.5%', ['38%', '3.8%', '0.375%'], '3/8 = 0.375 = 37.5%.')],
    why=[('Explain why 7/20 can be written as a terminating decimal.', '20 = 2² × 5 has only the prime factors 2 and 5, so 7/20 = 35/100 = 0.35 – an equivalent fraction with a power of 10 as denominator exists.'),
         ('Explain why 1/3 cannot be written as a terminating decimal.', 'No power of 10 is a multiple of 3, so 1/3 can never be rewritten with denominator 10, 100, 1000, …; the division 1 ÷ 3 leaves remainder 1 forever.'),
         ('Explain why multiplying by 10 helps convert 0.7̅ to a fraction.', 'x = 0.777… and 10x = 7.777… have the same recurring tail, so subtracting gives 9x = 7 with no decimals left.'),
         ('Explain why 0.9̅ (0.999…) is equal to 1.', 'x = 0.999…, 10x = 9.999…, so 9x = 9 and x = 1; alternatively 1/3 = 0.333…, and 3 × 1/3 = 1 = 0.999….')],
    misc=[('0.3̅ = 3/10', '3/10 = 0.3 exactly; 0.333… = 3/9 = 1/3.'),
          ('To change 0.045 to a percentage, write 0.045%.', 'Multiply by 100: 0.045 = 4.5%.'),
          ('2/7 is irrational because its decimal never ends.', 'Its decimal recurs (0.285714285714…), and it is a ratio of integers, so it is rational.')],
))


@R.add('ch01-st3', 'C3', (1, 4), 'short')
def recurring_to_frac(rng, slot):
    if slot.d <= 2:
        a = rng.randint(1, 8)
        fr_ = Fr(a, 9)
        return short(f'Write 0.{a}{a}{a}… (the digit {a} recurring) as a fraction in its simplest form, showing your method.', fx(fr_),
                     f'Let x = 0.{a}{a}…; 10x = {a}.{a}{a}… (M1); 9x = {a} so x = {fx(fr_)} (A1).', 2)
    if slot.d == 3:
        ab = rng.randint(10, 98)
        if ab % 11 == 0:
            ab += 1
        fr_ = Fr(ab, 99)
        return short(f'Express 0.{ab:02d}{ab:02d}{ab:02d}… as a fraction in its simplest form.', fx(fr_),
                     f'x = 0.{ab:02d}…; 100x − x = {ab} (M1); x = {ab}/99 = {fx(fr_)} (A1).', 2)
    a, b = rng.randint(1, 9), rng.randint(1, 9)
    if a == b:
        b = (b % 9) + 1
    fr_ = Fr(10 * a + b - a, 90)
    return short(f'Express 0.{a}{b}{b}{b}… (only the digit {b} recurs) as a fraction in its simplest form.', fx(fr_),
                 f'x = 0.{a}{b}̅: 100x = {a}{b}.{b}{b}…, 10x = {a}.{b}{b}… (M1); 90x = {10 * a + b} − {a} = {10 * a + b - a} (M1); x = {fx(fr_)} (A1).', 3)


@R.add('ch01-st3', 'C3', (1, 3), 'short')
def fdp_convert(rng, slot):
    b = rng.choice([4, 5, 8, 20, 25, 40, 50])
    a = rng.randint(1, b - 1)
    v = Fr(a, b)
    if v.denominator == 1:
        return None
    pct = v * 100
    pct_txt = f'{float(pct):g}%'
    dec_txt = f'{float(v):g}'
    kind = rng.choice(['f', 'd', 'p'])
    if kind == 'f':
        return short(f'Write {frac(v)} as (i) a decimal and (ii) a percentage.', f'(i) {dec_txt} (ii) {pct_txt}',
                     f'Equivalent fraction with denominator 100 or division (M1); {dec_txt} (A1); {pct_txt} (A1).', 3)
    if kind == 'd':
        return short(f'Write {dec_txt} as a fraction in its simplest form and as a percentage.', f'{frac(v)}; {pct_txt}',
                     f'{dec_txt} = {int(v * 10 ** len(dec_txt.split(".")[1]))}/{10 ** len(dec_txt.split(".")[1])} (M1) = {frac(v)} (A1); × 100 → {pct_txt} (A1).', 3)
    return short(f'Write {pct_txt} as a fraction in its simplest form and as a decimal.', f'{frac(v)}; {dec_txt}',
                 f'{pct_txt} = {float(pct):g}/100 (M1) = {frac(v)} (A1); {dec_txt} (A1).', 3)


@R.add('ch01-st3', 'C1', (1, 3), 'mcq')
def terminate_mcq(rng, slot):
    good = [Fr(a, b) for a, b in [(rng.randint(1, 7), 8), (rng.randint(1, 19), 20), (rng.randint(1, 24), 25), (rng.randint(1, 15), 16), (rng.randint(1, 39), 40)]]
    bad = [Fr(a, b) for a, b in [(rng.randint(1, 5), 6), (rng.randint(1, 6), 7), (rng.randint(1, 8), 9), (rng.randint(1, 11), 12), (rng.randint(1, 14), 15)]]
    good = [v for v in good if v.denominator not in (1, 2, 4, 5, 10)] or [Fr(3, 8)]
    bad = [v for v in bad if any(p not in (2, 5) for p in sp.factorint(v.denominator))]
    if rng.random() < 0.5:
        c = rng.choice(good)
        w = rng.sample(bad, 3) if len(bad) >= 3 else None
        if not w:
            return None
        return mcq(rng, 'Which of these fractions can be written as a terminating decimal?', frac(c), [frac(t) for t in w],
                   f'{frac(c)} has denominator {c.denominator} = {" × ".join(str(p) for p, e in sp.factorint(c.denominator).items() for _ in range(e))}, only 2s and 5s, so it terminates ({float(c):g}).')
    c = rng.choice(bad)
    w = rng.sample(good, 3) if len(good) >= 3 else None
    if not w:
        return None
    return mcq(rng, 'Which of these fractions gives a recurring decimal?', frac(c), [frac(t) for t in w],
               f'The denominator of {frac(c)} has a prime factor other than 2 or 5, so the decimal recurs.')


@R.add('ch01-st3', 'C2', (2, 4), 'explain')
def recur_pattern(rng, slot):
    kind = rng.choice(['ninths', 'elevenths', 'denoms'])
    if kind == 'ninths':
        a = rng.randint(1, 8)
        return explain(f'1/9 = 0.111…, 2/9 = 0.222…, 3/9 = 0.333…. Describe the pattern and use it to explain what {a}/9 is as a decimal. Then explain what happens for 9/9.',
                       f'{a}/9 = 0.{a}{a}{a}…; the numerator is the recurring digit; 9/9 = 0.999… = 1.',
                       'Pattern described (B1); applied correctly (A1); 9/9 = 0.999… = 1 justified (R1).', 3)
    if kind == 'elevenths':
        a = rng.randint(2, 10)
        d = f'{9 * a:02d}'
        return explain(f'1/11 = 0.090909… and 2/11 = 0.181818…. Describe the pattern in the repeating block and predict {a}/11 as a decimal. Check your prediction by division.',
                       f'{a}/11 = 0.{d}{d}{d}… (block {d} recurring); the repeating block is 9 × the numerator.',
                       f'Block is 9 × numerator (B1); {a}/11 = 0.{d}{d}… (A1); verified by division (R1).', 3)
    ds = rng.sample([6, 8, 12, 15, 16, 20, 24, 25, 30, 32, 40, 45], 4)
    term = [d for d in ds if all(p in (2, 5) for p in sp.factorint(d))]
    return explain(f'Without dividing, explain which of the fractions 1/{ds[0]}, 1/{ds[1]}, 1/{ds[2]} and 1/{ds[3]} give terminating decimals.',
                   f'Terminating: {", ".join(f"1/{d}" for d in term) or "none"}; the others recur.',
                   'Rule: in simplest form a fraction terminates exactly when the denominator has no prime factors other than 2 and 5 (R1); prime factorisations shown (M1); correct list (A1).', 3)


@R.add('ch01-st3', 'C4', (3, 5), 'multi_step')
def fdp_context(rng, slot):
    city, country, cur, cname = place(rng)
    a, b = rng.randint(30, 60), rng.randint(5, 9)
    f1 = Fr(rng.randint(2, 5), rng.choice([6, 7, 8, 9]))
    p2 = rng.randint(30, 70)
    d3 = Fr(rng.randint(30, 70), 100)
    names = rng.sample(['Team Kestrel', 'Team Orca', 'Team Baobab', 'Team Condor', 'Team Lotus'], 3)
    vals = [(names[0], f'{frac(f1)} of matches', f1), (names[1], f'{p2}% of matches', Fr(p2, 100)), (names[2], f'a win rate of {float(d3):g}', d3)]
    best = max(vals, key=lambda t: t[2])
    s1, s2 = rng.randint(2, 6), rng.randint(2, 6)
    frames = [
        (f'In a school football league in {city}, {vals[0][0]} won {vals[0][1]}, {vals[1][0]} won {vals[1][1]} and {vals[2][0]} had {vals[2][1]}. Convert all three to percentages (to 1 d.p. where needed), rank the teams and explain which form is easiest for comparing.',
         f'{", ".join(f"{n}: {float(v * 100):.1f}%" for n, _, v in vals)}; best is {best[0]}; percentages share a common denominator of 100'),
        (f'A survey of {a * 10} students in {city} found that {frac(f1)} walk to school, {p2}% take the bus and the rest cycle. (a) How many students cycle? (b) Express the cyclists as a fraction, a decimal and a percentage of the students.',
         None),
    ]
    q_, ans = rng.choice(frames)
    if ans is None:
        n = a * 10
        walk = f1 * n
        if walk.denominator != 1 or Fr(p2, 100) * n + walk >= n:
            return None
        bus = Fr(p2, 100) * n
        cyc = n - walk - bus
        if cyc.denominator != 1:
            return None
        cf = Fr(cyc, n)
        ans = f'(a) {cyc} (b) {frac(cf)} = {float(cf):.4g} = {float(cf * 100):.3g}%'
    return short(q_, ans, f'{ans}. Conversions correct (M1 A1), comparison/remaining amount found (M1 A1), conclusion communicated in context (C1).', 5, 'multi_step', 'G5')


R.facts('ch01-st4', F(
    terms=[('significant figures', 'the digits of a number that carry meaning about its size, counted from the first non-zero digit'),
           ('estimate', 'an approximate answer found by rounding the numbers in a calculation, usually to 1 significant figure'),
           ('decimal places', 'the number of digits after the decimal point')],
    facts=[('What is 0.04637 rounded to 2 significant figures?', '0.046', ['0.05', '0.0464', '0.04'], 'The first significant figure is 4; the next digit 6 rounds to 6, and 3 < 5 so 0.046.'),
           ('What is 3.8952 rounded to 2 decimal places?', '3.90', ['3.89', '3.9', '3.80'], 'The third decimal digit is 5, so 3.89 rounds up to 3.90; the zero shows 2 d.p.'),
           ('Which is the best estimate of 48.7 × 0.51?', '25', ['2.5', '250', '20'], '48.7 ≈ 50 and 0.51 ≈ 0.5, so 50 × 0.5 = 25.')],
    why=[('Explain why the zeros in 0.0072 are not significant figures.', 'They only fix the place value (the size) of the number; the first digit that carries meaning about the measurement is 7.'),
         ('Explain why it is useful to estimate before using a calculator.', 'A quick estimate shows the size of the answer, so keying errors (such as a misplaced decimal point) are spotted.'),
         ('Explain why 3.90 and 3.9 give different information when used as measurements.', '3.90 is correct to 2 d.p. (to the nearest 0.01), while 3.9 is only correct to the nearest 0.1, so 3.90 is more precise.')],
    misc=[('45 680 rounded to 2 significant figures is 46.', 'Place value must be kept: 45 680 ≈ 46 000 to 2 s.f.'),
          ('0.0508 has 4 significant figures.', 'Leading zeros are not significant: 0.0508 has 3 significant figures (5, 0, 8).')],
))


def _rand_num(rng, slot):
    kind = rng.choice(['big', 'mid', 'small'])
    if kind == 'big':
        return Decimal(rng.randint(10000, 999999))
    if kind == 'mid':
        return Decimal(rng.randint(10000, 999999)) / Decimal(1000)
    return Decimal(rng.randint(1000, 99999)) / Decimal(10 ** rng.randint(6, 7))


@R.add('ch01-st4', 'C3', (1, 3), 'short')
def round_sf_dp(rng, slot):
    v = _rand_num(rng, slot)
    sf = rng.randint(1, 3)
    vt = f'{v:f}'
    if v < 1000 and rng.random() < 0.5:
        k = rng.randint(1, 3)
        r = rnd(v, k)
        return short(f'Round {vt} to {k} decimal place{"s" if k > 1 else ""}.', f'{r:f}', f'Look at decimal digit {k + 1} to decide whether to round up (M1); {r:f} (A1).', 2)
    r = rsf(v, sf)
    return short(f'Round {vt} to {sf} significant figure{"s" if sf > 1 else ""}.', r,
                 f'Count from the first non-zero digit (M1); keep place value with zeros where needed: {r} (A1).', 2)


@R.add('ch01-st4', 'C3', (2, 4), 'short')
def estimate_calc(rng, slot):
    a = Decimal(rng.randint(110, 980)) / Decimal(10)
    b = Decimal(rng.randint(21, 89)) / Decimal(10)
    c = Decimal(rng.randint(11, 49)) / Decimal(10)
    ra, rb, rc = Decimal(rsf(a, 1)), Decimal(rsf(b, 1)), Decimal(rsf(c, 1))
    est = ra * rb / rc
    exact = a * b / c
    return short(f'By rounding each number to 1 significant figure, estimate the value of ({a} × {b}) ÷ {c}. State whether your estimate is likely to be higher or lower than the exact answer.',
                 f'≈ ({ra} × {rb}) ÷ {rc} = {g(float(est))}; exact {float(exact):.4g}, so the estimate is {"higher" if est > exact else "lower"}',
                 f'Each number rounded to 1 s.f. (M1); estimate {g(float(est))} (A1); comparison with reason (R1).', 3)


@R.add('ch01-st4', 'C1', (1, 3), 'mcq')
def sf_count_mcq(rng, slot):
    v = _rand_num(rng, slot)
    sf = rng.randint(1, 3)
    r = rsf(v, sf)
    w = {rsf(v, sf + 1), rsf(v, sf + 2), rsf(v, sf + 3)}
    if v >= 1000:
        w.add(rsf(v, sf)[:sf])  # place value lost
    elif v < 1:
        w.add(rsf(v * 10, sf))
    w.discard(r)
    if len(w) < 3:
        return None
    return mcq(rng, f'What is {v:f} correct to {sf} significant figure{"s" if sf > 1 else ""}?', r, sorted(w)[:3], f'Count {sf} digits from the first non-zero digit: {r}.')


@R.add('ch01-st4', 'C2', (2, 4), 'explain')
def rounding_reason(rng, slot):
    who = name(rng)
    v = Decimal(rng.randint(10, 99)) + Decimal(rng.randint(45, 49)) / Decimal(100)
    kind = rng.choice(['two', 'sense', 'cum'])
    if kind == 'two':
        return explain(f'{who} rounds {v:f} first to 1 decimal place and then rounds that answer to the nearest whole number. Explain why this "double rounding" can give a different answer from rounding {v:f} directly.',
                       f'Direct: {rnd(v, 0):f}; double: {rnd(rnd(v, 1), 0):f}. The first rounding can push a digit up to 5, which then rounds up again.',
                       'Both results found (A1); reason: the intermediate rounding changes the deciding digit (R1).', 2)
    if kind == 'sense':
        per = rng.choice([6, 8, 12])
        people = per * rng.randint(4, 9) + rng.randint(1, per // 2 - 1)
        return explain(f'A school trip needs {people} students to travel in minibuses that hold {per} each. {who} divides and rounds to the nearest whole number. Explain why this is not appropriate here.',
                       f'{people}/{per} = {people / per:.2f}, which rounds to {round(people / per)}, but that leaves {people - per * round(people / per)} students behind; you must round up to {math.ceil(people / per)} minibuses so that everyone travels.',
                       'Division correct (A1); context requires rounding up (R1).', 2)
    a = Decimal(rng.randint(21, 49)) / Decimal(10)
    return explain(f'The side of a square tile is measured as {a} cm (to 1 d.p.). {who} rounds it to {rnd(a, 0):f} cm before finding the area of 100 tiles. Explain why the area should be calculated from the unrounded length.',
                   f'Exact: {float(a * a * 100):g} cm²; rounded first: {float(rnd(a, 0) ** 2 * 100):g} cm². Rounding early creates an error that multiplication makes larger.',
                   'Both areas computed (A1); rounding should be done only at the end (R1).', 2)


@R.add('ch01-st4', 'C4', (3, 5), 'multi_step')
def estimate_context(rng, slot):
    city, country, cur, cname = place(rng)
    who = name(rng)
    L, H = Decimal(rng.randint(41, 89)) / 10, Decimal(rng.randint(22, 29)) / 10
    cover = rng.choice([9, 11, 12])
    price = Decimal(rng.randint(1850, 4990)) / 100
    area = L * H * 2
    tins = math.ceil(area / cover)
    km, eff = rng.randint(380, 890), Decimal(rng.randint(52, 79)) / 10
    fuel = Decimal(km) * eff / 100
    lp = Decimal(rng.randint(150, 220)) / 100
    frames = [
        (f'{who} in {city} wants to paint two walls, each {L} m long and {H} m high, with one coat. A tin covers about {cover} m² and costs {cur}{price}. (a) Estimate the total area by rounding to 1 s.f. (b) Calculate the exact area and the number of tins needed. (c) Find the cost and comment on whether the estimate was good enough.',
         f'(a) ≈ {Decimal(rsf(L, 1)) * Decimal(rsf(H, 1)) * 2} m² (b) {area} m²; {tins} tins (c) {cur}{price * tins:.2f}'),
        (f'A family drives {km} km from {city} on holiday. Their car uses {eff} litres of fuel per 100 km and fuel costs {cur}{lp} per litre. (a) Estimate the fuel cost using 1 s.f. values. (b) Calculate the cost to the nearest cent. (c) Explain why the estimate is useful.',
         f'(a) ≈ {cur}{Decimal(rsf(km, 1)) * Decimal(rsf(eff, 1)) / 100 * Decimal(rsf(lp, 1)):g} (b) {cur}{rnd(fuel * lp, 2)} (c) checks the calculator answer is the right size'),
    ]
    q_, ans = rng.choice(frames)
    return short(q_, ans, f'{ans}. Rounded values used for the estimate (M1 A1); accurate calculation (M1 A1); appropriate rounding in context and a reasoned comment (D: R1).', 5, 'multi_step', 'G5')


# =============================================================================================
# ch02 Powers and Roots
# =============================================================================================
R.facts('ch02-st1', F(
    terms=[('exponent (index)', 'the small raised number that shows how many times the base is used as a factor, e.g. the 4 in 3⁴'),
           ('base', 'the number or variable that is raised to a power, e.g. the 3 in 3⁴'),
           ('power', 'an expression made of a base and an exponent, such as 2⁵, meaning repeated multiplication')],
    facts=[('Which of the following is equal to 5⁴?', '5 × 5 × 5 × 5', ['5 × 4', '4 × 4 × 4 × 4 × 4', '5 + 5 + 5 + 5'], 'The exponent 4 means four factors of the base 5.'),
           ('Which law of exponents is correct?', 'aᵐ × aⁿ = aᵐ⁺ⁿ', ['aᵐ × aⁿ = aᵐⁿ', 'aᵐ × aⁿ = (2a)ᵐ⁺ⁿ', 'aᵐ + aⁿ = aᵐ⁺ⁿ'], 'Multiplying powers of the same base adds the exponents.'),
           ('What is (2³)²?', '2⁶', ['2⁵', '2⁹', '4⁵'], 'A power of a power multiplies the exponents: 3 × 2 = 6.')],
    why=[('Explain why a⁵ × a³ = a⁸ by writing out the factors.', 'a⁵ × a³ = (a·a·a·a·a)(a·a·a): there are 5 + 3 = 8 factors of a in total, so the product is a⁸.'),
         ('Explain why a⁷ ÷ a³ = a⁴.', 'Writing a⁷/a³ as seven factors of a over three factors of a, three pairs cancel, leaving 7 − 3 = 4 factors of a.'),
         ('Explain why (a³)⁴ = a¹².', '(a³)⁴ = a³ × a³ × a³ × a³; adding the exponents gives 3 + 3 + 3 + 3 = 3 × 4 = 12.'),
         ('Explain why 2³ × 3² cannot be simplified to 6⁵ using the laws of exponents.', 'The laws of exponents only combine powers with the same base; 2³ × 3² = 8 × 9 = 72, while 6⁵ = 7776.')],
    misc=[('3⁴ = 12', '3⁴ = 3 × 3 × 3 × 3 = 81; the exponent counts repeated factors, it does not multiply the base by 4.'),
          ('x³ × x⁴ = x¹²', 'Multiplying powers of the same base adds the exponents: x³ × x⁴ = x⁷.'),
          ('(2x)³ = 2x³', 'Every factor in the bracket is cubed: (2x)³ = 8x³.')],
))


@R.add('ch02-st1', 'C1', (1, 3), 'mcq')
def exp_law_mcq(rng, slot):
    b = rng.choice(['a', 'x', 'p', 'k', '7', '3', '5'])
    p, q = rng.randint(2, 9), rng.randint(2, 7)
    kind = rng.choice(['mul', 'div', 'pow'])
    if kind == 'mul':
        stem, c, w = f'{b}{sup(p)} × {b}{sup(q)}', p + q, [p * q, abs(p - q) or p + q + 1, p + q + 1]
    elif kind == 'div':
        p = p + q
        stem, c, w = f'{b}{sup(p)} ÷ {b}{sup(q)}', p - q, [p + q, p * q, max(1, p // q) if p // q != p - q else p - q + 1]
    else:
        stem, c, w = f'({b}{sup(p)}){sup(q)}', p * q, [p + q, p * q + 1, p ** q if p ** q < 100 else p * q - 1]
    return mcq(rng, f'Simplify {stem}.', f'{b}{sup(c)}', [f'{b}{sup(t)}' for t in w], f'{"Add" if kind == "mul" else "Subtract" if kind == "div" else "Multiply"} the exponents: {b}{sup(c)}.')


@R.add('ch02-st1', 'C3', (1, 4), 'short')
def exp_simplify(rng, slot):
    a, b = rng.randint(2, 6), rng.randint(2, 6)
    p, q, r_ = rng.randint(2, 7), rng.randint(2, 6), rng.randint(1, 4)
    v1, v2 = rng.sample(['x', 'y', 'a', 'b', 'm', 'n', 't'], 2)
    if slot.d <= 1:
        return short(f'Simplify {v1}{sup(p)} × {v1}{sup(q)} × {v1}.', f'{v1}{sup(p + q + 1)}', f'{p} + {q} + 1 = {p + q + 1} (M1); {v1}{sup(p + q + 1)} (A1).', 2)
    if slot.d == 2:
        return short(f'Simplify {a}{v1}{sup(p)} × {b}{v1}{sup(q)}.', f'{a * b}{v1}{sup(p + q)}', f'Multiply coefficients {a} × {b} = {a * b} (M1); add exponents (M1); {a * b}{v1}{sup(p + q)} (A1).', 2)
    if slot.d == 3:
        top = a * b
        return short(f'Simplify ({top}{v1}{sup(p + q)}{v2}{sup(r_ + 2)}) ÷ ({a}{v1}{sup(q)}{v2}{sup(r_)}).', f'{b}{v1}{sup(p)}{v2}²',
                     f'Divide coefficients {top} ÷ {a} = {b} (A1); subtract exponents for each variable (M1); {b}{v1}{sup(p)}{v2}² (A1).', 3)
    return short(f'Simplify ({a}{v1}{sup(p)}{v2})² × {b}{v1}{sup(q)}{v2}{sup(r_)}.', f'{a * a * b}{v1}{sup(2 * p + q)}{v2}{sup(2 + r_)}',
                 f'({a}{v1}{sup(p)}{v2})² = {a * a}{v1}{sup(2 * p)}{v2}² (M1 A1); multiply: {a * a * b}{v1}{sup(2 * p + q)}{v2}{sup(2 + r_)} (A1).', 3)


@R.add('ch02-st1', 'C3', (1, 3), 'short')
def exp_evaluate(rng, slot):
    b = rng.choice([2, 3, 5, 10])
    p, q = rng.randint(2, 6), rng.randint(2, 5)
    form = rng.choice(['mul', 'div', 'pow', 'mix'])
    if form == 'mul':
        e, k = f'{b}{sup(p)} × {b}{sup(q)}', p + q
    elif form == 'div':
        e, k = f'{b}{sup(p + q)} ÷ {b}{sup(q)}', p
    elif form == 'pow':
        q = 2
        p = min(p, 3)
        e, k = f'({b}{sup(p)})²', 2 * p
    else:
        e, k = f'({b}{sup(p)} × {b}{sup(q + 1)}) ÷ {b}{sup(q)}', p + 1
    if b ** k > 10 ** 7:
        return None
    return short(f'Write {e} as a single power of {b}, then evaluate it.', f'{b}{sup(k)} = {b ** k:,}'.replace(',', ' '),
                 f'Laws of exponents give {b}{sup(k)} (M1 A1); value {b ** k} (A1).', 3)


@R.add('ch02-st1', 'C2', (2, 4), 'explain')
def exp_pattern(rng, slot):
    b = rng.choice([2, 3, 4, 7, 9])
    n = rng.randint(20, 60)
    last = [pow(b, k, 10) for k in range(1, 9)]
    cyc = []
    for d_ in last:
        if d_ in cyc:
            break
        cyc.append(d_)
    L = len(cyc)
    ans = pow(b, n, 10)
    who = name(rng)
    kind = rng.choice(['last', 'compare'])
    if kind == 'last':
        return explain(f'Work out the last digits of {b}¹, {b}², {b}³, {b}⁴, {b}⁵, … Describe the pattern and use it to explain what the last digit of {b}{sup(n)} is.',
                       f'Last digits repeat {", ".join(map(str, cyc))} (cycle of {L}); {n} ÷ {L} leaves remainder {n % L or L} → last digit {ans}.',
                       f'Pattern of last digits found (B1); cycle length {L} identified (B1); applied to n = {n} with justification (R1 A1).', 4)
    p, q = rng.randint(2, 5), rng.randint(2, 5)
    return explain(f'{who} says that {b}{sup(p)} × {b}{sup(q)} = {b * b}{sup(p + q)}. Explain the mistake and give the correct answer as a power.',
                   f'The base stays {b}: {b}{sup(p)} × {b}{sup(q)} = {b}{sup(p + q)}; the bases are not multiplied.',
                   f'Error identified – bases multiplied (R1); correct {b}{sup(p + q)} (A1).', 2, 'G2')


@R.add('ch02-st1', 'C4', (3, 5), 'multi_step')
def exp_context(rng, slot):
    who = name(rng)
    city = rng.choice(CITIES)
    n0 = rng.choice([1, 2, 3, 5])
    hrs = rng.randint(4, 10)
    k = rng.choice([2, 3])
    frames = [
        (f'A laboratory in {city} grows bacteria. A sample of {n0} cell{"s" if n0 > 1 else ""} doubles every hour. (a) Write the number of cells after h hours using exponent notation. (b) How many cells are there after {hrs} hours? (c) After how many whole hours does the number first exceed 10 000?',
         f'(a) {n0} × 2ʰ (b) {n0 * 2 ** hrs} (c) {next(t for t in range(40) if n0 * 2 ** t > 10000)} hours'),
        (f'{who} sends a message to {k} friends, and each of them forwards it to {k} new friends, and so on. (a) Show that {k}{sup(hrs)} people receive it in round {hrs}. (b) Find the total number of people who have received it after {hrs} rounds. (c) Explain why the pattern cannot continue for long in a city of 2 million people.',
         f'(a) each round multiplies by {k}, so round n gives {k}ⁿ (b) {sum(k ** t for t in range(1, hrs + 1))} (c) {k}ⁿ grows so fast that it passes 2 000 000 by round {next(t for t in range(60) if k ** t > 2_000_000)}'),
        (f'A square sheet of paper is folded in half repeatedly. (a) Copy and complete a table of the number of layers after 1, 2, 3, 4 and 5 folds. (b) Write a rule for the number of layers after n folds. (c) If the paper is 0.1 mm thick, find the thickness after {hrs} folds in mm.',
         f'(a) 2, 4, 8, 16, 32 (b) 2ⁿ (c) {2 ** hrs * 0.1:g} mm'),
    ]
    q_, ans = rng.choice(frames)
    return short(q_, ans, f'{ans}. Pattern identified and written with exponents (B: M1 A1); evaluated correctly (A1); reasoning/limit explained (R1 C1).', 5, 'multi_step', 'G5')


R.facts('ch02-st2', F(
    terms=[('square number', 'the result of multiplying an integer by itself, such as 49 = 7²'),
           ('cube number', 'the result of using an integer as a factor three times, such as 64 = 4³'),
           ('square root', 'a number which, when squared, gives the original number; √x is the non-negative square root'),
           ('cube root', 'the number which, when cubed, gives the original number, e.g. ∛125 = 5')],
    facts=[('What is ∛216?', '6', ['72', '36', '14.7'], '6 × 6 × 6 = 216.'),
           ('Between which two integers does √70 lie?', '8 and 9', ['7 and 8', '9 and 10', '35 and 36'], '8² = 64 < 70 < 81 = 9².'),
           ('Which number is both a square number and a cube number?', '64', ['16', '27', '36'], '64 = 8² = 4³.'),
           ('What is ∛(−27)?', '−3', ['3', '−9', 'no real value'], '(−3)³ = −27; negative numbers have real cube roots.')],
    why=[('Explain why the square root of a negative number is not a real number, but the cube root is.', 'Any real number squared is ≥ 0, so no real number squares to a negative; but a negative number cubed is negative, e.g. (−2)³ = −8, so ∛(−8) = −2.'),
         ('Explain why every positive number has two square roots.', 'Both a and −a square to a², e.g. 5² = 25 and (−5)² = 25; the symbol √ means the positive one.'),
         ('Explain how to estimate √50 without a calculator.', '49 = 7² and 64 = 8², and 50 is just above 49, so √50 is just above 7 (about 7.07).')],
    misc=[('√(16 + 9) = √16 + √9 = 7', '√(16 + 9) = √25 = 5; square roots do not split over addition.'),
          ('The cube of 4 is 12.', '4³ = 4 × 4 × 4 = 64; 12 is 4 × 3.'),
          ('√0.09 = 0.03', '0.3² = 0.09, so √0.09 = 0.3.')],
))


@R.add('ch02-st2', 'C3', (1, 3), 'short')
def roots_eval(rng, slot):
    a, b = rng.randint(2, 15), rng.randint(2, 10)
    c = rng.randint(1, 9)
    forms = [
        (f'√{a * a} + ∛{b ** 3}', a + b),
        (f'√{a * a} × √{c * c}', a * c),
        (f'{b}³ − √{a * a}', b ** 3 - a),
        (f'∛{b ** 3} × {c}²', b * c * c),
        (f'√({a * a} − {a * a - c * c})', c),
    ]
    e, v = rng.choice(forms[:2] if slot.d <= 1 else forms)
    return short(f'Without a calculator, evaluate {e}.', m(v), f'Evaluate each power/root first (M1); {m(v)} (A1).', 2)


@R.add('ch02-st2', 'C3', (1, 4), 'short')
def root_between(rng, slot):
    n = rng.randint(5, 400)
    r = math.isqrt(n)
    if r * r == n:
        return None
    if slot.d >= 3:
        nc = rng.randint(10, 900)
        c = round(nc ** (1 / 3))
        while c ** 3 > nc:
            c -= 1
        while (c + 1) ** 3 <= nc:
            c += 1
        if c ** 3 == nc:
            return None
        return short(f'Without a calculator, find the two consecutive integers between which ∛{nc} lies, and state which one it is closer to.', f'{c} and {c + 1}; closer to {c if nc - c ** 3 < (c + 1) ** 3 - nc else c + 1}',
                     f'{c}³ = {c ** 3} < {nc} < {(c + 1) ** 3} = {c + 1}³ (M1 A1); compare distances {nc - c ** 3} and {(c + 1) ** 3 - nc} (R1).', 3)
    return short(f'Without a calculator, state the two consecutive whole numbers between which √{n} lies.', f'{r} and {r + 1}',
                 f'{r}² = {r * r} < {n} < {(r + 1) ** 2} = {r + 1}² (M1); {r} and {r + 1} (A1).', 2)


@R.add('ch02-st2', 'C1', (1, 3), 'mcq')
def sq_cube_mcq(rng, slot):
    kind = rng.choice(['sq', 'cube', 'root'])
    if kind == 'sq':
        k = rng.randint(11, 25)
        return mcq(rng, f'What is {k}²?', str(k * k), [str(2 * k), str(k * k + k), str((k + 1) * (k - 1) + 10)], f'{k} × {k} = {k * k}.')
    if kind == 'cube':
        k = rng.randint(3, 12)
        return mcq(rng, f'What is {k}³?', str(k ** 3), [str(3 * k), str(k * k), str(k ** 3 + k)], f'{k} × {k} × {k} = {k ** 3}.')
    sqs = rng.sample([k * k for k in range(6, 20)], 1)[0]
    others = rng.sample([v for v in range(30, 400) if math.isqrt(v) ** 2 != v], 3)
    return mcq(rng, 'Which of these is a square number?', str(sqs), [str(o) for o in others], f'{sqs} = {math.isqrt(sqs)}².')


@R.add('ch02-st2', 'C2', (2, 4), 'explain')
def sq_pattern(rng, slot):
    n = rng.randint(5, 12)
    kind = rng.choice(['odd', 'diff', 'last'])
    if kind == 'odd':
        s = ' + '.join(str(2 * k - 1) for k in range(1, 6))
        return explain(f'Work out 1, 1 + 3, 1 + 3 + 5, {s}. Describe the pattern and use it to explain the sum of the first {n} odd numbers.',
                       f'The totals are 1, 4, 9, 16, 25 – square numbers; the sum of the first {n} odd numbers is {n}² = {n * n}.',
                       f'Totals found (A1); pattern of square numbers described (B1); {n}² = {n * n} (A1); reason, e.g. each odd number adds an L-shaped layer to a square (R1).', 4)
    if kind == 'diff':
        return explain(f'Find the differences between consecutive square numbers 1, 4, 9, 16, 25, 36. Explain how you could use the pattern to find {n + 1}² from {n}² = {n * n}.',
                       f'Differences 3, 5, 7, 9, 11 (consecutive odd numbers); {n + 1}² = {n * n} + {2 * n + 1} = {(n + 1) ** 2}.',
                       f'Differences found (A1); pattern described (B1); (n + 1)² − n² = 2n + 1 applied (A1).', 3)
    return explain('List the last digits of the square numbers 1², 2², …, 10². Explain why no square number can end in the digit 7.',
                   'Last digits are 1, 4, 9, 6, 5, 6, 9, 4, 1, 0; the last digit of a square depends only on the last digit of the number, and none gives 7.',
                   'Last digits listed (A1); only the units digit determines the units digit of the square (R1); conclusion (R1).', 3)


@R.add('ch02-st2', 'C4', (3, 5), 'multi_step')
def sq_context(rng, slot):
    city, country, cur, cname = place(rng)
    s = rng.randint(6, 25)
    c = rng.randint(3, 9)
    price = rng.randint(12, 45)
    frames = [
        (f'A square courtyard in {city} has an area of {s * s} m². (a) Find the length of one side. (b) A path is laid around the edge – find its length. (c) Paving slabs cost {cur}{price} per m²; find the cost of paving the whole courtyard.',
         f'(a) {s} m (b) {4 * s} m (c) {cur}{price * s * s}'),
        (f'A cube-shaped water tank holds {c ** 3} m³. (a) Find the length of its edge. (b) Find the area of the base. (c) How deep is the water when the tank holds {c * c * (c - 1)} m³?',
         f'(a) {c} m (b) {c * c} m² (c) {c - 1} m'),
        (f'A square garden has an area of {s * s + rng.randint(5, 2 * s)} m². Without a calculator, estimate its side length to the nearest whole metre and explain how you know. Then use a calculator to give it to 2 d.p.',
         None),
    ]
    q_, ans = rng.choice(frames)
    if ans is None:
        A = int(q_.split('area of ')[1].split(' m²')[0])
        r = math.isqrt(A)
        near = r if A - r * r < (r + 1) ** 2 - A else r + 1
        ans = f'between {r} and {r + 1} m ({r * r} < {A} < {(r + 1) ** 2}); nearest whole metre {near}; √{A} = {math.sqrt(A):.2f} m'
    return short(q_, ans, f'{ans}. Correct inverse operation (root) used (M1 A1); further calculation (M1 A1); units and reasoning communicated (C1).', 5, 'multi_step', 'G5')


R.facts('ch02-st3', F(
    terms=[('zero exponent', 'any non-zero base raised to the power 0 equals 1, a⁰ = 1'),
           ('negative exponent', 'a power with a negative exponent means the reciprocal of the positive power, a⁻ⁿ = 1/aⁿ')],
    facts=[('What is 7⁰?', '1', ['0', '7', '70'], 'Any non-zero number to the power 0 is 1.'),
           ('What is 2⁻³?', '1/8', ['−8', '−6', '1/6'], '2⁻³ = 1/2³ = 1/8.'),
           ('Which is equal to 1/10 000?', '10⁻⁴', ['10⁴', '−10⁴', '10⁻³'], '10 000 = 10⁴, so its reciprocal is 10⁻⁴.')],
    why=[('Explain why a⁰ = 1 using the division law.', 'aⁿ ÷ aⁿ = 1 because any non-zero number divided by itself is 1; the law gives aⁿ⁻ⁿ = a⁰, so a⁰ = 1.'),
         ('Explain why 5⁻² = 1/25 by continuing the pattern 5², 5¹, 5⁰.', '5² = 25, 5¹ = 5, 5⁰ = 1: each step down divides by 5, so 5⁻¹ = 1/5 and 5⁻² = 1/25.'),
         ('Explain why a negative exponent does not make the answer negative.', 'The negative sign in the exponent means "take the reciprocal": 2⁻³ = 1/8, which is positive.')],
    misc=[('4⁻² = −16', '4⁻² = 1/4² = 1/16; a negative exponent gives a reciprocal, not a negative number.'),
          ('9⁰ = 0', 'Any non-zero number to the power 0 equals 1, so 9⁰ = 1.'),
          ('3⁻¹ = −3', '3⁻¹ is the reciprocal of 3, which is 1/3.')],
))


@R.add('ch02-st3', 'C3', (1, 4), 'short')
def neg_exp_eval(rng, slot):
    b = rng.choice([2, 3, 4, 5, 10])
    n = rng.randint(1, 4)
    if slot.d <= 2:
        return short(f'Evaluate {b}{sup(-n)}, giving your answer as a fraction.', f'1/{b ** n}', f'{b}{sup(-n)} = 1/{b}{sup(n)} (M1) = 1/{b ** n} (A1).', 2)
    p, q = Fr(rng.randint(1, 4), rng.choice([3, 5, 7])), rng.randint(2, 3)
    if p.numerator == p.denominator:
        return None
    if slot.d == 3:
        val = (1 / p) ** q
        return short(f'Evaluate ({frac(p)}){sup(-q)}.', fx(val), f'Reciprocal: ({frac(1 / p)}){sup(q)} (M1); {fx(val)} (A1).', 2)
    a, c = rng.randint(2, 5), rng.randint(1, 3)
    val = Fr(b) ** (-n) * a ** 0 + Fr(c) ** (-1)
    return short(f'Evaluate {b}{sup(-n)} × {a}⁰ + {c}⁻¹, giving your answer as a fraction in its simplest form.', fx(val),
                 f'{b}{sup(-n)} = 1/{b ** n}, {a}⁰ = 1, {c}⁻¹ = 1/{c} (M1 M1); sum {fx(val)} (A1).', 3)


@R.add('ch02-st3', 'C3', (2, 4), 'short')
def neg_exp_write(rng, slot):
    v = rng.choice(['x', 'a', 'n', 'k'])
    p, q = rng.randint(2, 6), rng.randint(3, 9)
    k = rng.randint(2, 7)
    kind = rng.choice(['pos', 'neg', 'div'])
    if kind == 'pos':
        return short(f'Write {k}{v}{sup(-p)} without a negative exponent.', f'{k}/{v}{sup(p)}', f'Only {v} has the negative exponent (R1): {k}/{v}{sup(p)} (A1).', 2)
    if kind == 'neg':
        return short(f'Write 1/{v}{sup(p)} as a single power of {v}.', f'{v}{sup(-p)}', f'{v}{sup(-p)} (A1); reciprocal ↔ negative exponent (R1).', 2)
    return short(f'Simplify {v}{sup(p)} ÷ {v}{sup(p + q)}, giving your answer (i) with a negative exponent and (ii) as a fraction.', f'(i) {v}{sup(-q)} (ii) 1/{v}{sup(q)}',
                 f'{p} − {p + q} = −{q} (M1); {v}{sup(-q)} (A1); 1/{v}{sup(q)} (A1).', 3)


@R.add('ch02-st3', 'C1', (1, 3), 'mcq')
def zero_neg_mcq(rng, slot):
    b, n = rng.choice([2, 3, 4, 5, 6, 10]), rng.randint(1, 3)
    if rng.random() < 0.3:
        k = rng.randint(2, 999)
        return mcq(rng, f'What is the value of {k}⁰?', '1', ['0', str(k), f'1/{k}'], 'Any non-zero base to the power 0 equals 1.')
    return mcq(rng, f'What is the value of {b}{sup(-n)}?', f'1/{b ** n}', [m(-b ** n), m(-b * n), f'1/{b * n}' if b * n != b ** n else f'{b}/{n + 1}'], f'{b}{sup(-n)} = 1/{b}{sup(n)} = 1/{b ** n}.')


@R.add('ch02-st3', 'C2', (2, 4), 'explain')
def neg_exp_table(rng, slot):
    b = rng.choice([2, 3, 4, 5, 10])
    vals = ', '.join(f'{b}{sup(k)} = {fx(Fr(b) ** k)}' for k in (3, 2, 1))
    return explain(f'Copy and continue the pattern {vals}, … down to {b}⁻³. Explain the rule that takes you from one line to the next and what it shows about {b}⁰ and {b}⁻³.',
                   f'Each step divides by {b}: {b}⁰ = 1, {b}⁻¹ = 1/{b}, {b}⁻² = 1/{b * b}, {b}⁻³ = 1/{b ** 3}.',
                   f'Rule "divide by {b}" stated (B1); {b}⁰ = 1 (A1); negative powers as reciprocals (A1); generalisation b⁻ⁿ = 1/bⁿ (R1).', 4)


@R.add('ch02-st3', 'C4', (3, 5), 'multi_step')
def neg_exp_context(rng, slot):
    k = rng.randint(2, 9)
    n = rng.randint(3, 7)
    who = name(rng)
    frames = [
        (f'A colony of yeast cells halves in size every hour after an antifungal treatment. There are {k * 2 ** n} cells now. (a) Write the number of cells t hours from now as {k * 2 ** n} × 2⁻ᵗ. Find the number after {n} hours. (b) What does t = −1 represent, and how many cells were there then?',
         f'(a) {k} (b) one hour before now; {k * 2 ** (n + 1)} cells'),
        (f'{who} investigates powers of 10 for metric prefixes: kilo = 10³, centi = 10⁻², milli = 10⁻³, micro = 10⁻⁶. (a) Write 1 mm in metres as a power of 10 and as a decimal. (b) How many micrometres are in {k} mm? (c) Explain why 10⁻⁶ m is smaller than 10⁻³ m.',
         f'(a) 10⁻³ m = 0.001 m (b) {k * 1000} µm (c) 10⁻⁶ = 1/1 000 000 < 1/1000 = 10⁻³'),
        (f'Investigate the values of {k}ⁿ for n = 2, 1, 0, −1, −2. (a) Show your results in a table. (b) Describe what happens to the value as n decreases. (c) Is {k}ⁿ ever zero or negative? Justify your answer.',
         f'(a) {k * k}, {k}, 1, 1/{k}, 1/{k * k} (b) it is divided by {k} each time and approaches 0 (c) no – each value is a positive number divided by {k}, which stays positive'),
    ]
    q_, ans = rng.choice(frames)
    return short(q_, ans, f'{ans}. Values found with correct exponent rules (M1 A1); pattern described (B1); conclusion justified (R1 C1).', 5, 'multi_step', 'G5')


R.facts('ch02-st4', F(
    terms=[('standard form', 'a way of writing a number as a × 10ⁿ where 1 ≤ a < 10 and n is an integer'),
           ('order of magnitude', 'the power of 10 that gives the approximate size of a number')],
    facts=[('Which number is written in standard form?', '4.7 × 10⁵', ['47 × 10⁴', '0.47 × 10⁶', '4.7 × 5¹⁰'], 'In standard form 1 ≤ a < 10 and the power is of 10.'),
           ('What is 0.000 32 in standard form?', '3.2 × 10⁻⁴', ['3.2 × 10⁴', '32 × 10⁻⁵', '3.2 × 10⁻³'], 'The decimal point moves 4 places to the right, so the exponent is −4.'),
           ('What is 6.1 × 10³ as an ordinary number?', '6100', ['610', '61 000', '0.0061'], 'Multiply 6.1 by 1000.')],
    why=[('Explain why scientists use standard form.', 'Very large or very small numbers are written compactly, their size can be compared from the power of 10, and the number of significant figures is clear.'),
         ('Explain why 23 × 10⁴ is not in standard form and how to correct it.', 'The number in front must be at least 1 and less than 10; 23 × 10⁴ = 2.3 × 10 × 10⁴ = 2.3 × 10⁵.'),
         ('Explain how the sign of the exponent tells you whether a number in standard form is large or small.', 'A positive exponent multiplies a number between 1 and 10 by a power of 10 greater than 1, so it is at least 10; a negative exponent divides it, so it is less than 1.')],
    misc=[('5 × 10⁻³ is a negative number.', '5 × 10⁻³ = 0.005, which is positive but small; the negative exponent means division by 1000.'),
          ('3 × 10⁴ + 2 × 10⁴ = 5 × 10⁸', 'Add like terms: 3 × 10⁴ + 2 × 10⁴ = 5 × 10⁴; exponents are only added when multiplying.')],
))


def _sf(v, k=3):
    """Number in standard form text (k s.f.) using exact Decimal."""
    d = Decimal(str(v))
    e = d.adjusted()
    mant = (d / Decimal(10) ** e).quantize(Decimal(1).scaleb(-(k - 1)), rounding=ROUND_HALF_UP)
    if mant >= 10:
        mant /= 10
        e += 1
    t = f'{mant.normalize():f}'
    return f'{t} × 10{sup(e)}'


def _plain(d):
    s = f'{Decimal(d).normalize():f}'
    if '.' not in s and len(s) > 4:
        s = f'{int(s):,}'.replace(',', ' ')
    return s


@R.add('ch02-st4', 'C3', (1, 3), 'short')
def to_standard(rng, slot):
    big = rng.random() < 0.5
    if big:
        mant = Decimal(rng.randint(101, 999)) / 100
        e = rng.randint(4, 9)
    else:
        mant = Decimal(rng.randint(11, 99)) / 10
        e = -rng.randint(3, 7)
    v = mant * Decimal(10) ** e
    if rng.random() < 0.5:
        return short(f'Write {_plain(v)} in standard form.', _sf(v), f'Place the decimal point after the first non-zero digit (M1); count the places moved: {_sf(v)} (A1).', 2)
    return short(f'Write {_sf(v)} as an ordinary number.', _plain(v), f'Move the decimal point {abs(e)} places {"right" if e > 0 else "left"} (M1); {_plain(v)} (A1).', 2)


@R.add('ch02-st4', 'C3', (2, 4), 'numerical')
def sf_ops(rng, slot):
    a, b = Decimal(rng.randint(11, 99)) / 10, Decimal(rng.randint(11, 99)) / 10
    p, q = rng.randint(-6, 9), rng.randint(-6, 9)
    A, B = a * Decimal(10) ** p, b * Decimal(10) ** q
    op = rng.choice(['×', '÷', '+'] if slot.d >= 3 else ['×', '÷'])
    if op == '+':
        q = p - rng.randint(0, 2)
        B = b * Decimal(10) ** q
        res = A + B
    else:
        res = A * B if op == '×' else A / B
    return short(f'Calculate ({_sf(A, 2)}) {op} ({_sf(B, 2)}), giving your answer in standard form.', _sf(res, 3),
                 f'{"Multiply the numbers and add the exponents" if op == "×" else "Divide the numbers and subtract the exponents" if op == "÷" else "Write both with the same power of 10 before adding"} (M1); adjust so 1 ≤ a < 10 (M1); {_sf(res, 3)} (A1).', 3, 'numerical')


@R.add('ch02-st4', 'C1', (1, 3), 'mcq')
def sf_order_mcq(rng, slot):
    vals = set()
    while len(vals) < 4:
        vals.add((rng.randint(11, 99), rng.randint(-5, 7)))
    vals = list(vals)
    big = max(vals, key=lambda t: t[0] * 10.0 ** t[1])
    txt = lambda t: f'{t[0] / 10:g} × 10{sup(t[1])}'
    return mcq(rng, 'Which of these numbers is the largest?', txt(big), [txt(t) for t in vals if t != big],
               f'Compare the powers of 10 first, then the numbers in front: {txt(big)} is largest.')


@R.add('ch02-st4', 'C2', (2, 4), 'explain')
def sf_check(rng, slot):
    who = name(rng)
    a, e = rng.randint(11, 99), rng.randint(3, 8)
    wrong = f'{a} × 10{sup(e)}'
    right = f'{a / 10:g} × 10{sup(e + 1)}'
    kind = rng.choice(['form', 'compare'])
    if kind == 'form':
        return explain(f'{who} gives the answer {wrong}. Explain why this is not in standard form and rewrite it correctly.', right,
                       f'{a} is not between 1 and 10 (R1); {a} = {a / 10:g} × 10, so {right} (A1).', 2, 'G2')
    p, q = rng.randint(2, 9), rng.randint(2, 9)
    e1, e2 = e, e - 1
    return explain(f'Without converting to ordinary numbers, explain which is larger: {p}.{q} × 10{sup(e2)} or {q / 10 + 1:g} × 10{sup(e1)}.',
                   f'{q / 10 + 1:g} × 10{sup(e1)} is larger: it has the higher power of 10, and both front numbers lie between 1 and 10.',
                   'Compare exponents first (R1); a higher power of 10 always wins when both are in standard form (R1).', 2)


@R.add('ch02-st4', 'C4', (3, 5), 'multi_step')
def sf_context(rng, slot):
    who = name(rng)
    frames = []
    d_sun = Decimal('1.496') * Decimal(10) ** 8
    c = Decimal(3) * Decimal(10) ** 5
    t = d_sun / c
    frames.append((f'The distance from the Earth to the Sun is about 1.496 × 10⁸ km and light travels about 3 × 10⁵ km per second. (a) Find the time for sunlight to reach the Earth in seconds, in standard form. (b) Convert this to minutes and seconds.',
                   f'(a) {_sf(t, 3)} s (b) about {int(rnd(t, 0)) // 60} min {int(rnd(t, 0)) % 60} s'))
    cell = Decimal(rng.randint(60, 90)) / 10
    n_ = Decimal(rng.randint(2, 9)) * Decimal(10) ** 3
    frames.append((f'A red blood cell is about {cell} × 10⁻⁶ m across. {who} imagines {_plain(n_)} cells placed side by side. (a) Find the total length in metres in standard form. (b) Write it in millimetres as an ordinary number.',
                   f'(a) {_sf(cell * Decimal(10) ** -6 * n_, 3)} m (b) {_plain(cell * Decimal(10) ** -6 * n_ * 1000)} mm'))
    pop = Decimal(rng.randint(15, 95)) / 10 * Decimal(10) ** rng.choice([6, 7])
    area = Decimal(rng.randint(12, 90)) / 10 * Decimal(10) ** rng.choice([3, 4, 5])
    city = rng.choice(CITIES)
    dens = pop / area
    frames.append((f'A region around {city} has a population of {_sf(pop, 2)} people and an area of {_sf(area, 2)} km². (a) Calculate the population density in people per km², giving your answer in standard form to 3 s.f. (b) Explain whether the answer is reasonable.',
                   f'(a) {_sf(dens, 3)} people per km² (b) it is about {_plain(dens.quantize(Decimal(1), rounding=ROUND_HALF_UP))} people per km², sensible compared with real cities and countryside'))
    q_, ans = rng.choice(frames)
    return short(q_, ans, f'{ans}. Correct operation chosen (M1); standard-form arithmetic (M1 A1); conversion/interpretation in context (A1 R1).', 5, 'multi_step', 'G5')


# =============================================================================================
# ch03 Percentages, Ratio and Proportion
# =============================================================================================
R.facts('ch03-st1', F(
    terms=[('percentage change', 'the change in a quantity as a percentage of its original value: (change ÷ original) × 100%'),
           ('multiplier', 'the single number you multiply by to apply a percentage change, e.g. 1.15 for a 15% increase'),
           ('percentage', 'a number of parts per hundred')],
    facts=[('What is the multiplier for a 12% decrease?', '0.88', ['1.12', '0.12', '0.012'], '100% − 12% = 88% = 0.88.'),
           ('A price rises from 50 to 60. What is the percentage increase?', '20%', ['10%', '16.7%', '60%'], 'Change 10 ÷ original 50 = 0.2 = 20%.'),
           ('What is 15% of 240?', '36', ['24', '16', '3.6'], '0.15 × 240 = 36.')],
    why=[('Explain why a 10% increase followed by a 10% decrease does not return to the original value.', 'The decrease is 10% of the larger, increased amount: × 1.1 × 0.9 = × 0.99, a 1% overall decrease.'),
         ('Explain why percentage change is always calculated using the original value.', 'Percentage change measures the change relative to where you started; using the new value would give a different, inconsistent answer.'),
         ('Explain why multiplying by 1.07 increases an amount by 7%.', '1.07 = 100% + 7% of the amount, so the result is the original plus 7% of it.')],
    misc=[('A rise from 80 to 100 is a 25% rise, so a fall from 100 to 80 is a 25% fall.', 'The fall is 20 out of 100 = 20%; the base (original value) is different.'),
          ('To find 30% of a number, divide it by 30.', 'Multiply by 30/100 = 0.3 (or find 10% and multiply by 3).')],
))


@R.add('ch03-st1', 'C3', (1, 3), 'short')
def pct_of(rng, slot):
    p = rng.choice([5, 10, 12, 15, 17.5, 20, 25, 30, 35, 40, 45, 60, 75, 120])
    amt = rng.choice([40, 60, 80, 120, 150, 240, 360, 480, 640, 850, 1200])
    v = Decimal(str(p)) * amt / 100
    unit = rng.choice(['kg', 'km', 'litres', 'students', 'g'])
    if unit == 'students' and v != int(v):
        return None
    return short(f'Find {p:g}% of {amt} {unit}.', f'{_plain(v)} {unit}', f'{p:g}/100 × {amt} (M1) = {_plain(v)} {unit} (A1).', 2)


@R.add('ch03-st1', 'C3', (1, 4), 'short')
def pct_change(rng, slot):
    city, country, cur, cname = place(rng)
    a = rng.randint(20, 400)
    p = rng.choice([4, 5, 8, 10, 12, 15, 20, 25, 30, 35])
    up = rng.random() < 0.5
    item = rng.choice(['a bicycle', 'a concert ticket', 'a monthly bus pass', 'a pair of trainers', 'a tablet'])
    if slot.d <= 2:
        new = Decimal(a) * (100 + (p if up else -p)) / 100
        return short(f'The price of {item} in {city} was {cur}{a}. It {"increases" if up else "decreases"} by {p}%. Find the new price.', money(cur, new),
                     f'Multiplier {(100 + (p if up else -p)) / 100:g} (M1); {cur}{a} × {(100 + (p if up else -p)) / 100:g} = {money(cur, new)} (A1).', 2)
    b = a + rng.choice([-1, 1]) * rng.randint(3, a // 2)
    ch = Fr(b - a, a) * 100
    return short(f'The price of {item} in {city} changed from {cur}{a} to {cur}{b}. Calculate the percentage {"increase" if b > a else "decrease"}, to 1 decimal place where necessary.',
                 f'{float(abs(ch)):.1f}%'.replace('.0%', '%'),
                 f'Change = {cur}{abs(b - a)} (M1); ÷ original {a} × 100 (M1); {float(abs(ch)):.1f}% (A1).', 3)


@R.add('ch03-st1', 'C3', (3, 5), 'short')
def reverse_pct(rng, slot):
    city, country, cur, cname = place(rng)
    orig = rng.randint(20, 300) * 5
    p = rng.choice([10, 15, 20, 25, 30, 40])
    up = rng.random() < 0.5
    new = Decimal(orig) * (100 + (p if up else -p)) / 100
    what = rng.choice(['a jacket in a sale', 'a train fare', 'a hotel room', 'a laptop'])
    phrase = f'after a {p}% {"increase" if up else "reduction"}'
    return short(f'In {city}, {what} costs {money(cur, new)} {phrase}. Find the original price.', f'{cur}{orig}',
                 f'{money(cur, new)} represents {100 + (p if up else -p)}% (M1); divide by {(100 + (p if up else -p)) / 100:g} (M1); {cur}{orig} (A1). Finding {p}% of the new price scores 0.', 3)


@R.add('ch03-st1', 'C1', (1, 3), 'mcq')
def multiplier_mcq(rng, slot):
    p = rng.randint(2, 45)
    up = rng.random() < 0.5
    c = (100 + p) / 100 if up else (100 - p) / 100
    w = [(100 - p) / 100 if up else (100 + p) / 100, p / 100, 1 + p / 1000 if up else 1 - p / 1000]
    return mcq(rng, f'Which multiplier {"increases" if up else "decreases"} an amount by {p}%?', f'{c:g}', [f'{t:g}' for t in w],
               f'{100 + p if up else 100 - p}% of the amount = {c:g} × amount.')


@R.add('ch03-st1', 'C2', (2, 4), 'explain')
def pct_successive(rng, slot):
    p, q = rng.choice([10, 20, 25, 30, 40, 50]), rng.choice([10, 20, 25, 30, 40, 50])
    who = name(rng)
    net = (1 + p / 100) * (1 - q / 100)
    ch = (net - 1) * 100
    return explain(f'A shop increases a price by {p}% and later decreases the new price by {q}%. {who} says the overall change is {"+" if p >= q else "−"}{abs(p - q)}%. Explain whether {who} is correct and find the true overall percentage change.',
                   f'Not correct: multiplier {1 + p / 100:g} × {1 - q / 100:g} = {net:g}, an overall {"increase" if ch > 0 else "decrease" if ch < 0 else "change"} of {abs(ch):g}%.',
                   'Percentages of different amounts cannot simply be added (R1); combined multiplier (M1); correct overall change (A1).', 3, 'G2')


@R.add('ch03-st1', 'C4', (3, 5), 'multi_step')
def pct_context(rng, slot):
    city, country, cur, cname = place(rng)
    a = rng.randint(800, 4000)
    r1, r2 = rng.choice([4, 6, 8, 10]), rng.choice([5, 7, 12, 15])
    pop = rng.randint(120, 900) * 1000
    g_ = rng.choice([2, 3, 4, 5])
    yrs = 3
    frames = [
        (f'A café in {city} took {cur}{a} in January. Takings rose by {r1}% in February and then by {r2}% in March. (a) Find the March takings. (b) Find the overall percentage increase from January to March. (c) Explain why this is not {r1 + r2}%.',
         f'(a) {money(cur, a * (1 + r1 / 100) * (1 + r2 / 100))} (b) {((1 + r1 / 100) * (1 + r2 / 100) - 1) * 100:.2f}% (c) the second increase is applied to the larger February amount'),
        (f'The population of a town near {city} was {pop:_} and grows by {g_}% each year. (a) Find the population after {yrs} years, to the nearest whole number. (b) Find the total percentage increase over the {yrs} years. (c) Comment on whether the model is realistic over 50 years.'.replace('_', ' '),
         f'(a) {round(pop * (1 + g_ / 100) ** yrs):_} (b) {((1 + g_ / 100) ** yrs - 1) * 100:.2f}% (c) growth rates usually change; housing, jobs and migration limit growth'.replace('_', ' ')),
        (f'A phone costs {cur}{a // 4} before tax. A sales tax of {r1}% is added and then a {r2}% discount is given on the price with tax. (a) Find the final price. (b) Would the customer pay less if the discount were applied before the tax? Justify your answer.',
         f'(a) {money(cur, a / 4 * (1 + r1 / 100) * (1 - r2 / 100))} (b) no – the order does not matter, because multiplication is commutative: {1 + r1 / 100:g} × {1 - r2 / 100:g} = {1 - r2 / 100:g} × {1 + r1 / 100:g}'),
    ]
    q_, ans = rng.choice(frames)
    return short(q_, ans, f'{ans}. Multipliers used correctly (M1 M1); accurate answers (A1 A1); reasoning in context communicated (D: R1).', 5, 'multi_step', 'G5')


R.facts('ch03-st2', F(
    terms=[('ratio', 'a comparison of two or more quantities of the same kind, written a : b'),
           ('simplest form of a ratio', 'a ratio whose parts are integers with no common factor other than 1'),
           ('unit ratio', 'a ratio written in the form 1 : n or n : 1')],
    facts=[('What is 24 : 36 in its simplest form?', '2 : 3', ['4 : 6', '3 : 2', '12 : 18'], 'Divide both parts by the HCF 12.'),
           ('Share 40 in the ratio 3 : 5. What is the larger share?', '25', ['24', '15', '8'], '40 ÷ 8 parts = 5; 5 × 5 = 25.'),
           ('What is 50 cm : 2 m in its simplest form?', '1 : 4', ['25 : 1', '50 : 2', '1 : 40'], 'Same units: 50 cm : 200 cm = 1 : 4.')],
    why=[('Explain why the units must be the same before a ratio is simplified.', 'A ratio compares quantities of the same kind; 30 cm : 1 m is really 30 : 100 = 3 : 10, not 30 : 1.'),
         ('Explain why the order of the numbers in a ratio matters.', 'a : b says there are a parts of the first quantity for every b of the second; swapping them describes a different mixture.'),
         ('Explain how a ratio a : b can be written as fractions of the whole.', 'There are a + b equal parts in total, so the first quantity is a/(a + b) of the whole and the second is b/(a + b).')],
    misc=[('If the ratio of boys to girls is 2 : 3, then 2/3 of the class are boys.', 'There are 5 parts altogether, so 2/5 of the class are boys; 2/3 compares boys to girls.'),
          ('Sharing 60 in the ratio 1 : 2 gives 30 and 30.', 'There are 3 parts, each worth 20, so the shares are 20 and 40.')],
))


@R.add('ch03-st2', 'C3', (1, 3), 'short')
def ratio_simplify(rng, slot):
    k = rng.randint(2, 12)
    a, b = rng.randint(1, 9), rng.randint(1, 9)
    if math.gcd(a, b) != 1 or a == b:
        return None
    if slot.d <= 1:
        return short(f'Write {a * k} : {b * k} in its simplest form.', f'{a} : {b}', f'Divide both by HCF {k} (M1); {a} : {b} (A1).', 2)
    if slot.d == 2:
        u = rng.choice([('cm', 'm', 100), ('g', 'kg', 1000), ('minutes', 'hours', 60), ('mL', 'L', 1000)])
        big = rng.randint(1, 5)
        small = rng.randint(1, (u[2] * big) // (u[2] // 20 if u[2] >= 100 else 5) - 1) * (u[2] // 20 if u[2] >= 100 else 5)
        gg = math.gcd(small, u[2] * big)
        return short(f'Write {small} {u[0]} : {big} {u[1]} in its simplest form.', f'{small // gg} : {u[2] * big // gg}',
                     f'Same units: {small} : {u[2] * big} (M1); ÷ {gg}: {small // gg} : {u[2] * big // gg} (A1).', 2)
    c = rng.randint(1, 9)
    gg = math.gcd(math.gcd(a, b), c)
    return short(f'Write the three-part ratio {a * k} : {b * k} : {c * k} in its simplest form, and then in the form 1 : n : p.',
                 f'{a // gg} : {b // gg} : {c // gg}; 1 : {fmt(b / a)} : {fmt(c / a)}',
                 f'Divide by the HCF {k * gg} (M1 A1); divide all parts by {a // gg} for the unit form (A1).', 3)


@R.add('ch03-st2', 'C3', (1, 4), 'short')
def ratio_share(rng, slot):
    city, country, cur, cname = place(rng)
    a, b = rng.randint(1, 7), rng.randint(1, 7)
    if a == b:
        return None
    parts = a + b
    each = rng.randint(5, 60)
    total = parts * each
    n1, n2 = two_names(rng)
    if slot.d <= 2:
        return short(f'{n1} and {n2} share {cur}{total} in the ratio {a} : {b}. How much does each receive?', f'{n1} {cur}{a * each}, {n2} {cur}{b * each}',
                     f'{a} + {b} = {parts} parts; one part = {cur}{each} (M1); {cur}{a * each} and {cur}{b * each} (A1 A1).', 3)
    diff = abs(a - b) * each
    return short(f'Paint is mixed from blue and white in the ratio {a} : {b}. The mixture contains {diff} mL more {"blue" if a > b else "white"} than {"white" if a > b else "blue"}. Find the total volume of paint.',
                 f'{total} mL', f'Difference of {abs(a - b)} parts = {diff} mL (M1), so 1 part = {each} mL (A1); total {parts} parts = {total} mL (A1).', 3)


@R.add('ch03-st2', 'C1', (1, 3), 'mcq')
def ratio_mcq(rng, slot):
    a, b = rng.randint(1, 9), rng.randint(1, 9)
    if math.gcd(a, b) != 1 or a == b:
        return None
    k = rng.randint(2, 9)
    return mcq(rng, f'Which ratio is equivalent to {a} : {b}?', f'{a * k} : {b * k}', [f'{a + k} : {b + k}', f'{b * k} : {a * k}', f'{a * k} : {b * k + 1}'],
               f'Multiply both parts by {k}.')


@R.add('ch03-st2', 'C2', (2, 4), 'explain')
def ratio_explain(rng, slot):
    a, b = rng.randint(1, 6), rng.randint(2, 7)
    if a == b:
        return None
    n = (a + b) * rng.randint(3, 8)
    who = name(rng)
    kind = rng.choice(['frac', 'add'])
    if kind == 'frac':
        return explain(f'In a youth orchestra in {rng.choice(CITIES)}, the ratio of string players to wind players is {a} : {b}. {who} says {a}/{b} of the players play strings. Explain the error and find the correct fraction. If there are {n} players, how many play strings?',
                       f'Strings are {a} of {a + b} parts: {fx(Fr(a, a + b))} of the players; {n * a // (a + b)} play strings.',
                       f'{a}/{b} compares the two groups, not a part to the whole (R1); fraction {fx(Fr(a, a + b))} (A1); {n * a // (a + b)} (A1).', 3, 'G2')
    k = rng.randint(2, 5)
    return explain(f'{who} says that adding {k} to both parts of {a} : {b} gives an equivalent ratio. Explain, with a numerical check, why this is wrong.',
                   f'{a + k} : {b + k} ≠ {a} : {b}, because {fx(Fr(a + k, b + k))} ≠ {fx(Fr(a, b))}; equivalent ratios multiply or divide both parts by the same number.',
                   'Counter-check with values (A1); correct rule stated (R1).', 2, 'G2')


@R.add('ch03-st2', 'C4', (3, 5), 'multi_step')
def ratio_context(rng, slot):
    city, country, cur, cname = place(rng)
    a, b, c = rng.randint(1, 5), rng.randint(1, 5), rng.randint(1, 5)
    k = rng.randint(20, 90)
    n1, n2, n3 = rng.sample(['Ana', 'Kwame', 'Mei', 'Lukas', 'Priya', 'Omar', 'Freya', 'Tariq'], 3)
    flour, water = rng.randint(3, 7), rng.randint(2, 5)
    have = rng.randint(400, 900)
    frames = [
        (f'{n1}, {n2} and {n3} invest {cur}{a * 1000}, {cur}{b * 1000} and {cur}{c * 1000} in a small business in {city}. Profits of {cur}{(a + b + c) * k * 10} are shared in the ratio of their investments. (a) Write the ratio in its simplest form. (b) Find each share. (c) {n3} argues the profit should be shared equally because everyone works the same hours. Comment on this.',
         f'(a) {a // math.gcd(math.gcd(a, b), c)} : {b // math.gcd(math.gcd(a, b), c)} : {c // math.gcd(math.gcd(a, b), c)} (b) {cur}{a * k * 10}, {cur}{b * k * 10}, {cur}{c * k * 10} (c) a fair argument either way: investment risk versus equal work'),
        (f'A bread recipe uses flour and water in the ratio {flour} : {water} by mass. (a) How much water is needed for {flour * k} g of flour? (b) {n1} has {have} g of flour and 300 g of water. Which ingredient runs out first, and what is the greatest total mass of dough (flour + water) they can make?',
         None),
    ]
    q_, ans = rng.choice(frames)
    if ans is None:
        need_w = Fr(have * water, flour)
        if need_w <= 300:
            tot = have + need_w
            ans = f'(a) {water * k} g (b) flour runs out first; dough {g(float(tot), 4)} g'
        else:
            fl = Fr(300 * flour, water)
            ans = f'(a) {water * k} g (b) water runs out first; dough {g(float(fl + 300), 4)} g'
    return short(q_, ans, f'{ans}. Ratio simplified/scaled (M1 A1); shares or limiting quantity found (M1 A1); reasoned comment in context (D: R1).', 5, 'multi_step', 'G5')


R.facts('ch03-st3', F(
    terms=[('direct proportion', 'two quantities are directly proportional when their ratio stays constant, so if one doubles the other doubles (y = kx)'),
           ('inverse proportion', 'two quantities are inversely proportional when their product stays constant, so if one doubles the other halves (y = k/x)'),
           ('unitary method', 'finding the value of one unit first and then multiplying to find the value of the required number of units')],
    facts=[('Which situation shows inverse proportion?', 'the number of workers and the time to build a wall', ['the number of tickets bought and the total cost', 'the distance travelled at constant speed and the time', 'the mass of apples and their price'], 'More workers means less time: the product (worker-days) stays constant.'),
           ('5 pens cost 4.50. How much do 8 pens cost?', '7.20', ['7.50', '0.90', '36'], 'One pen costs 0.90; 8 × 0.90 = 7.20.'),
           ('The graph of a direct proportion is:', 'a straight line through the origin', ['a curve that never touches the axes', 'a horizontal line', 'a straight line with a positive y-intercept'], 'y = kx is a straight line through (0, 0).')],
    why=[('Explain how you can tell from a table that two quantities are in direct proportion.', 'Divide each y-value by its x-value; if the ratio y/x is the same each time, the quantities are directly proportional.'),
         ('Explain why the number of people sharing a pizza and the size of each share are in inverse proportion.', 'The whole pizza stays the same, so number of people × size of share is constant: doubling the people halves each share.'),
         ('Explain why a taxi fare with a fixed starting charge is not directly proportional to distance.', 'At 0 km the fare is not 0, so the graph does not pass through the origin and the ratio fare/distance is not constant.')],
    misc=[('If 3 workers take 12 days, then 6 workers take 24 days.', 'This is inverse proportion: doubling the workers halves the time, so 6 workers take 6 days.'),
          ('Any straight-line graph shows direct proportion.', 'Only straight lines through the origin show direct proportion.')],
))


@R.add('ch03-st3', 'C3', (1, 4), 'short')
def direct_prop(rng, slot):
    city, country, cur, cname = place(rng)
    n1 = rng.randint(2, 9)
    unit = Decimal(rng.randint(35, 480)) / 100
    n2 = rng.randint(3, 25)
    if n2 == n1:
        return None
    item = rng.choice(['notebooks', 'bus tickets', 'mangoes', 'litres of juice', 'metres of rope'])
    frames = [
        f'{n1} {item} cost {money(cur, unit * n1)} in {city}. Find the cost of {n2} {item}.',
        f'At a market in {city}, the total cost is directly proportional to the quantity bought. If {n1} {item} cost {money(cur, unit * n1)}, how much would {n2} {item} cost?',
    ]
    return short(rng.choice(frames), money(cur, unit * n2), f'Cost of one: {money(cur, unit * n1)} ÷ {n1} = {money(cur, unit)} (M1); × {n2} = {money(cur, unit * n2)} (A1).', 2)


@R.add('ch03-st3', 'C3', (2, 4), 'short')
def inverse_prop(rng, slot):
    w1 = rng.randint(2, 8)
    t1 = rng.randint(3, 15)
    total = w1 * t1
    divs = [d for d in range(2, 30) if total % d == 0 and d != w1]
    if not divs:
        return None
    w2 = rng.choice(divs)
    frames = [
        (f'{w1} machines can pack an order in {t1} hours. How long would {w2} identical machines take?', f'{total // w2} hours', 'machine-hours'),
        (f'A water tank is emptied by {w1} identical pumps in {t1} minutes. How long would {w2} pumps take?', f'{total // w2} minutes', 'pump-minutes'),
        (f'Food stored for an expedition lasts {w1} climbers for {t1} days. How long would it last {w2} climbers?', f'{total // w2} days', 'climber-days'),
        (f'A journey takes {t1} hours at {w1 * 10} km/h. How long would it take at {w2 * 10} km/h?', f'{total // w2} hours', '(speed × time)'),
    ]
    q_, ans, what = rng.choice(frames)
    if ans.startswith('1 '):
        return None
    return short(q_, ans, f'Inverse proportion: total {what} = {w1} × {t1} = {total} (M1); ÷ {w2} = {ans} (A1).', 2)


@R.add('ch03-st3', 'C1', (1, 3), 'mcq')
def prop_table_mcq(rng, slot):
    k = rng.randint(2, 9)
    xs = sorted(rng.sample(range(1, 10), 3))
    direct = ', '.join(f'({a}, {k * a})' for a in xs)
    inv_k = 36
    inv = ', '.join(f'({a}, {fx(Fr(inv_k, a))})' for a in [2, 3, 4])
    lin_ = ', '.join(f'({a}, {k * a + 1})' for a in xs)
    sq = ', '.join(f'({a}, {a * a})' for a in xs)
    return mcq(rng, 'Which set of (x, y) pairs shows y directly proportional to x?', direct, [inv, lin_, sq],
               f'In {direct} the ratio y/x is always {k}.')


@R.add('ch03-st3', 'C2', (2, 4), 'explain')
def prop_decide(rng, slot):
    k = rng.randint(2, 9)
    c = rng.randint(1, 9)
    xs = [1, 2, 3, 4]
    kind = rng.choice(['direct', 'notdirect', 'inverse'])
    if kind == 'direct':
        ys = [k * a for a in xs]
        return explain(f'x: {", ".join(map(str, xs))}; y: {", ".join(map(str, ys))}. Explain whether y is directly proportional to x, and if so write a formula.',
                       f'Yes: y/x = {k} for every pair, so y = {k}x.', f'Ratios computed (M1); constant ratio ⇒ direct proportion (R1); y = {k}x (A1).', 3)
    if kind == 'notdirect':
        ys = [k * a + c for a in xs]
        return explain(f'x: {", ".join(map(str, xs))}; y: {", ".join(map(str, ys))}. y increases by {k} each time. Explain why y is NOT directly proportional to x.',
                       f'y/x is not constant ({ys[0]}/1 = {ys[0]}, {ys[1]}/2 = {fx(Fr(ys[1], 2))}); when x = 0, y = {c}, not 0.',
                       'Ratio test or intercept argument (R1 R1); clear conclusion (C1).', 3)
    P = k * 12
    ys = [fx(Fr(P, a)) for a in xs]
    return explain(f'x: {", ".join(map(str, xs))}; y: {", ".join(ys)}. Explain which type of proportion this shows and write a formula linking x and y.',
                   f'Inverse proportion: xy = {P} for every pair, so y = {P}/x.', f'Products computed (M1); constant product ⇒ inverse proportion (R1); y = {P}/x (A1).', 3)


def _hm(hours: Fr) -> str:
    mins = math.floor(hours * 60 + Fr(1, 2))
    return f'{mins // 60} h {mins % 60} min' if mins % 60 else f'{mins // 60} h'


@R.add('ch03-st3', 'C4', (3, 5), 'multi_step')
def prop_context(rng, slot):
    pair = rng.choice([(('Lisbon', 'euro', 'euros'), ('Geneva', 'Swiss franc', 'Swiss francs'), 0.94), (('Singapore', 'Singapore dollar', 'Singapore dollars'), ('Kuala Lumpur', 'ringgit', 'ringgit'), 3.45),
                       (('Toronto', 'Canadian dollar', 'Canadian dollars'), ('Mexico City', 'Mexican peso', 'Mexican pesos'), 13.2), (('Melbourne', 'Australian dollar', 'Australian dollars'), ('Mumbai', 'rupee', 'rupees'), 55.4),
                       (('London', 'pound', 'pounds'), ('Vienna', 'euro', 'euros'), 1.17), (('Vienna', 'euro', 'euros'), ('Nairobi', 'Kenyan shilling', 'Kenyan shillings'), 140.5),
                       (('Oslo', 'Norwegian krone', 'Norwegian kroner'), ('Tokyo', 'yen', 'yen'), 13.8), (('Dubai', 'dirham', 'dirhams'), ('Cairo', 'Egyptian pound', 'Egyptian pounds'), 13.1)])
    a, b = (pair[0][0], None, None, pair[0][2]), (pair[1][0], None, None, pair[1][2])
    rate = (Decimal(str(pair[2])) * (1 + Decimal(rng.randint(-4, 4)) / 100)).quantize(Decimal('0.01') if pair[2] < 50 else Decimal('0.1'), rounding=ROUND_HALF_UP)
    amt = rng.randint(5, 40) * 10
    back = int(rng.randint(3, 30) * 10 * max(1, float(rate)) // 10 * 10)
    who = name(rng)
    w1, d1 = rng.randint(3, 8), rng.randint(6, 20)
    w2 = w1 + rng.randint(1, 5)
    frames = [
        (f'{who} travels from {a[0]} to {b[0]}. The exchange rate is 1 {pair[0][1]} = {rate} {b[3]}. (a) How many {b[3]} does {who} get for {amt} {a[3]}? (b) On return, {who} changes {back} {b[3]} back. How many {a[3]} is that, to 2 d.p.? (c) Explain why exchange rate conversions are an example of direct proportion.',
         f'(a) {rate * amt:.2f} {b[3]} (b) {Decimal(back) / rate:.2f} {a[3]} (c) amount received = rate × amount changed, a constant multiplier (graph through origin)'),
        (f'{w1} volunteers can clear a stretch of beach near {a[0]} in {d1} hours. (a) How long would {w2} volunteers take, to the nearest minute? (b) How many volunteers are needed to finish in under {max(1, d1 // 2)} hours? (c) State one assumption you have made.',
         f'(a) {_hm(Fr(w1 * d1, w2))} (b) {math.floor(w1 * d1 / max(1, d1 // 2)) + 1} volunteers (c) all volunteers work at the same constant rate'),
    ]
    q_, ans = rng.choice(frames)
    return short(q_, ans, f'{ans}. Type of proportion identified (R1); unitary or product method (M1 A1); second calculation (A1); assumption or interpretation (D: R1).', 5, 'multi_step', 'G5')


R.facts('ch03-st4', F(
    terms=[('simple interest', 'interest calculated only on the original amount (principal): I = P × r × t / 100'),
           ('principal', 'the original amount of money borrowed or invested'),
           ('discount', 'a reduction from the marked price, often given as a percentage'),
           ('profit', 'the amount by which the selling price exceeds the cost price')],
    facts=[('What is the simple interest on 500 at 4% per year for 3 years?', '60', ['20', '560', '6'], 'I = 500 × 4 × 3 / 100 = 60.'),
           ('An item bought for 80 is sold for 100. What is the percentage profit?', '25%', ['20%', '80%', '125%'], 'Profit 20 ÷ cost 80 = 25%.'),
           ('A 20% discount on a marked price of 45 gives a sale price of:', '36', ['9', '25', '40'], '0.8 × 45 = 36.')],
    why=[('Explain why percentage profit is calculated using the cost price.', 'Profit measures the gain compared with what the seller paid, so the cost price is the original value for the percentage change.'),
         ('Explain why simple interest grows by the same amount each year.', 'Interest is always calculated on the original principal, which does not change, so each year adds P × r/100.'),
         ('Explain the difference between a discount of 15% and a discount of 15 currency units.', 'A 15% discount depends on the price (15 per 100), while a fixed discount of 15 is the same for every price; for prices above 100 the percentage discount is larger.')],
    misc=[('Selling at a 20% loss means the selling price is 20% of the cost price.', 'A 20% loss means the selling price is 80% of the cost price.'),
          ('Simple interest of 5% for 4 years means the money is multiplied by 5 × 4 = 20.', 'The interest is 5% × 4 = 20% of the principal, so the total is 1.2 × the principal.')],
))


@R.add('ch03-st4', 'C3', (1, 4), 'short')
def simple_interest(rng, slot):
    city, country, cur, cname = place(rng)
    P = rng.randint(4, 120) * 50
    r = rng.choice([1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 6])
    t = rng.randint(2, 8)
    I = Decimal(P) * Decimal(str(r)) * t / 100
    who = name(rng)
    if slot.d <= 2:
        return short(f'{who} invests {cur}{P} in a savings account in {city} paying {r:g}% simple interest per year. Find the interest earned after {t} years.', money(cur, I),
                     f'I = Prt/100 = {P} × {r:g} × {t} / 100 (M1) = {money(cur, I)} (A1).', 2)
    if slot.d == 3:
        return short(f'{who} invests {cur}{P} at {r:g}% simple interest per year. Find the total value of the investment after {t} years.', money(cur, P + I),
                     f'Interest {money(cur, I)} (M1 A1); total {money(cur, P + I)} (A1).', 3)
    return short(f'A loan of {cur}{P} at simple interest grows to {money(cur, P + I)} after {t} years. Find the annual interest rate.', f'{r:g}%',
                 f'Interest = {money(cur, I)} (A1); r = 100I/(Pt) = 100 × {I} / ({P} × {t}) (M1) = {r:g}% (A1).', 3)


@R.add('ch03-st4', 'C3', (1, 4), 'short')
def profit_loss(rng, slot):
    city, country, cur, cname = place(rng)
    cost = rng.randint(8, 400)
    p = rng.choice([5, 10, 12, 15, 20, 25, 30, 40])
    gain = rng.random() < 0.6
    sell = Decimal(cost) * (100 + (p if gain else -p)) / 100
    item = rng.choice(['handmade bags', 'second-hand bicycles', 'phone cases', 'potted plants', 'school calculators'])
    if slot.d <= 2:
        return short(f'A trader in {city} buys {item} for {cur}{cost} each and sells them for {money(cur, sell)}. Find the percentage {"profit" if gain else "loss"}.', f'{p}%',
                     f'{"Profit" if gain else "Loss"} = {money(cur, abs(sell - cost))} (M1); ÷ cost {cur}{cost} × 100 = {p}% (A1).', 2)
    mp = rng.randint(20, 300)
    dsc = rng.choice([10, 15, 20, 25, 30, 35])
    sp_ = Decimal(mp) * (100 - dsc) / 100
    return short(f'In a sale in {city}, {item} marked at {cur}{mp} are reduced by {dsc}%. The shop paid {money(cur, sp_ * Decimal("0.8"))} for each. Find (a) the sale price, (b) the percentage profit on the cost price.',
                 f'(a) {money(cur, sp_)} (b) 25%', f'(a) 0.{100 - dsc} × {mp} = {money(cur, sp_)} (M1 A1); (b) profit {money(cur, sp_ - sp_ * Decimal("0.8"))} ÷ {money(cur, sp_ * Decimal("0.8"))} = 25% (M1 A1).', 4)


@R.add('ch03-st4', 'C1', (1, 3), 'mcq')
def interest_mcq(rng, slot):
    P = rng.randint(2, 40) * 100
    r = rng.randint(2, 8)
    t = rng.randint(2, 6)
    I = P * r * t // 100
    return mcq(rng, f'What is the simple interest on {P} at {r}% per year for {t} years?', str(I), [str(P + I), str(P * r // 100), str(P * r * t // 10)],
               f'I = {P} × {r} × {t} ÷ 100 = {I}.')


@R.add('ch03-st4', 'C2', (2, 4), 'explain')
def fin_explain(rng, slot):
    city, country, cur, cname = place(rng)
    mp = rng.randint(40, 300)
    d1, d2 = rng.choice([10, 20, 25]), rng.choice([10, 15, 20])
    who = name(rng)
    kind = rng.choice(['double', 'compare'])
    if kind == 'double':
        final = Decimal(mp) * (100 - d1) * (100 - d2) / 10000
        return explain(f'A shop in {city} takes {d1}% off a {cur}{mp} coat and then a further {d2}% off at the till. {who} says this is the same as {d1 + d2}% off. Explain whether this is true.',
                       f'False: {cur}{mp} × {(100 - d1) / 100:g} × {(100 - d2) / 100:g} = {money(cur, final)}, a total discount of {100 - (100 - d1) * (100 - d2) / 100:g}%, not {d1 + d2}%.',
                       'Second discount applies to the reduced price (R1); final price (A1); overall % discount (A1).', 3, 'G2')
    fixed = rng.randint(10, 40)
    pc = rng.choice([10, 15, 20])
    be = Fr(fixed * 100, pc)
    return explain(f'A store offers either {pc}% off or {cur}{fixed} off any item. Explain how {who} should decide which offer is better for an item of price p.',
                   f'{pc}% off is better when {pc}% of p > {fixed}, i.e. p > {fx(be)}; below {cur}{fx(be)} the fixed {cur}{fixed} discount is better.',
                   f'Set up {pc}p/100 = {fixed} (M1); break-even price {fx(be)} (A1); correct decision rule (R1).', 3)


@R.add('ch03-st4', 'C4', (3, 5), 'multi_step')
def fin_context(rng, slot):
    city, country, cur, cname = place(rng)
    price = rng.randint(30, 150) * 10
    dep = rng.choice([10, 15, 20, 25])
    months = rng.choice([12, 18, 24])
    rate = rng.choice([4, 5, 6, 8])
    who = name(rng)
    cost, n = rng.randint(3, 12), rng.randint(40, 200)
    sell = cost + rng.randint(2, 8)
    fixed = rng.randint(50, 300)
    frames = [
        (f'{who} wants a scooter priced {cur}{price} in {city}. Option A: pay cash with a 5% discount. Option B: pay a {dep}% deposit, then the rest is borrowed at {rate}% simple interest per year and repaid in {months} equal monthly instalments. (a) Find the cost under each option. (b) Find the monthly instalment. (c) Advise {who}, giving one financial and one non-financial reason.',
         None),
        (f'A student enterprise in {city} buys {n} T-shirts at {cur}{cost} each, pays {cur}{fixed} for printing, and sells them at {cur}{sell} each. (a) Find the profit if all are sold. (b) Find the percentage profit on total costs. (c) What is the least number they must sell to break even?',
         f'(a) {cur}{n * sell - n * cost - fixed} (b) {(n * sell - n * cost - fixed) / (n * cost + fixed) * 100:.1f}% (c) {math.ceil((n * cost + fixed) / sell)} T-shirts'),
    ]
    q_, ans = rng.choice(frames)
    if ans is None:
        a_cost = Decimal(price) * Decimal('0.95')
        loan = Decimal(price) * (100 - dep) / 100
        interest = loan * rate * Decimal(months) / 12 / 100
        b_cost = Decimal(price) + interest
        inst = (loan + interest) / months
        ans = f'(a) A {money(cur, a_cost)}, B {money(cur, b_cost)} (b) {money(cur, inst)} per month (c) A is cheaper by {money(cur, b_cost - a_cost)}; B spreads the cost if savings are low'
    if '-' in ans.split('(b)')[0] and 'profit' in q_:
        return None
    return short(q_, ans, f'{ans}. Percentages/interest calculated (M1 A1); totals compared (M1 A1); justified recommendation in context (D: R1 C1).', 6, 'multi_step', 'G5')


# =============================================================================================
# ch04 Algebraic Expressions and Formulae
# =============================================================================================
def _sym(rng, k=1):
    names = rng.sample(['a', 'b', 'c', 'n', 'p', 'k', 'm', 't', 'x', 'y', 'w', 'h'], k)
    return [sp.Symbol(s) for s in names]


def _rc(rng, lo=1, hi=9, neg=True):
    v = rng.randint(lo, hi)
    return -v if neg and rng.random() < 0.35 else v


R.facts('ch04-st1', F(
    terms=[('variable', 'a letter or symbol that stands for a quantity that can change or is unknown'),
           ('term', 'a single number, variable, or product of numbers and variables, separated from other terms by + or − signs'),
           ('coefficient', 'the number multiplying a variable in a term, e.g. 7 in 7x'),
           ('expression', 'a combination of terms, such as 3n + 5, with no equals sign'),
           ('constant', 'a term with a fixed value that does not contain a variable')],
    facts=[('How many terms are in 4x² − 3x + 7?', '3', ['2', '4', '1'], 'The terms are 4x², −3x and 7.'),
           ('Which expression means "5 less than twice a number n"?', '2n − 5', ['5 − 2n', '2(n − 5)', 'n² − 5'], 'Twice n is 2n; 5 less than that subtracts 5.'),
           ('What is the coefficient of y in 6x − 9y + 2?', '−9', ['9', '6', '2'], 'The sign belongs to the term: the term is −9y.'),
           ('Which of these is an expression, not an equation?', '3a + 4b', ['3a + 4 = 10', 'y = 2x', '5 = n − 1'], 'An expression has no equals sign.')],
    why=[('Explain why 3n and n³ are different.', '3n = n + n + n (three lots of n), while n³ = n × n × n; for n = 2, 3n = 6 but n³ = 8.'),
         ('Explain why an expression such as 4p + 7 can take many different values.', 'Its value depends on the value of the variable p, which can change; for p = 1 it is 11, for p = 5 it is 27.'),
         ('Explain the difference between an expression and an equation.', 'An expression is a combination of terms with no equals sign; an equation states that two expressions are equal and can be solved.')],
    misc=[('n + n + n = n³', 'Adding three n’s gives 3n; n³ means multiplying three n’s.'),
          ('"6 less than x" is written 6 − x.', '"6 less than x" means start with x and subtract 6: x − 6.'),
          ('In 5 − 2a, the coefficient of a is 2.', 'The sign belongs to the term: the term is −2a, so the coefficient is −2.')],
))


@R.add('ch04-st1', 'C3', (1, 3), 'short')
def write_expr(rng, slot):
    k, c = rng.randint(2, 9), rng.randint(2, 20)
    v = rng.choice(['n', 'x', 'p', 't'])
    city, country, cur, cname = place(rng)
    cases = [
        (f'Write an expression for "{c} more than {k} times {v}".', f'{k}{v} + {c}'),
        (f'Write an expression for "{k} times the sum of {v} and {c}".', f'{k}({v} + {c})'),
        (f'Write an expression for "the square of {v}, decreased by {c}".', f'{v}² − {c}'),
        (f'Write an expression for "{v} divided by {k}, then add {c}".', f'{v}/{k} + {c}'),
        (f'A taxi in {city} charges {cur}{c} plus {cur}{k} per km. Write an expression for the cost of a journey of {v} km.', f'{c} + {k}{v} ({cur})'),
        (f'Cinema tickets cost {cur}{c} for an adult and {cur}{k} for a child. Write an expression for the cost of a adult tickets and {v} child tickets.', f'{c}a + {k}{v} ({cur})'),
        (f'{name(rng)} is {v} years old. Her brother is {c} years older and her mother is {k} times her age. Write an expression for the sum of all three ages.', f'{k + 2}{v} + {c}'),
    ]
    q_, ans = rng.choice(cases[:4] if slot.d <= 1 else cases)
    return short(q_, ans, f'{ans} (A1 correct operations, A1 correct order/brackets).', 2)


@R.add('ch04-st1', 'C3', (1, 3), 'short')
def identify_terms(rng, slot):
    a, b = _sym(rng, 2)
    c1, c2, c3 = _rc(rng), _rc(rng), _rc(rng, 1, 20)
    e = c1 * a ** 2 + c2 * a * b + c3
    terms = [f'{m(c1)}{a}²', f'{m(c2)}{a}{b}', m(c3)]
    return short(f'For the expression {poly(e)}: (a) how many terms are there? (b) state the coefficient of the term containing both {a} and {b}; (c) state the constant term.',
                 f'(a) 3 (b) {m(c2)} (c) {m(c3)}', f'Terms {", ".join(terms)} (A1); coefficient includes its sign: {m(c2)} (A1); constant {m(c3)} (A1).', 3)


@R.add('ch04-st1', 'C1', (1, 3), 'mcq')
def words_mcq(rng, slot):
    k, c = rng.randint(2, 9), rng.randint(2, 15)
    v = rng.choice(['n', 'x', 'y', 'm'])
    opts = [(f'{k} less than {v}', f'{v} − {k}', [f'{k} − {v}', f'{k}{v}', f'{v}/{k}']),
            (f'{v} multiplied by itself, plus {c}', f'{v}² + {c}', [f'2{v} + {c}', f'{v}({v} + {c})', f'{v}{sup(c)}']),
            (f'the product of {k} and {v}, subtracted from {c}', f'{c} − {k}{v}', [f'{k}{v} − {c}', f'{c} − {k} + {v}', f'{k}({v} − {c})']),
            (f'half of {v}, plus {c}', f'{v}/2 + {c}', [f'({v} + {c})/2', f'2{v} + {c}', f'{v} + {c}/2'])]
    phr, c_, w = rng.choice(opts)
    return mcq(rng, f'Which expression represents "{phr}"?', c_, w, f'"{phr}" translates to {c_}.')


@R.add('ch04-st1', 'C2', (2, 4), 'explain')
def expr_compare(rng, slot):
    k = rng.randint(2, 6)
    v = rng.choice(['n', 'x', 'p'])
    vals = [1, 2, 3, k + 1]
    kind = rng.choice(['pow', 'brack'])
    if kind == 'pow':
        return explain(f'Copy and complete a table of values of {k}{v} and {v}{sup(k)} for {v} = 1, 2, 3 and {k + 1}. Explain why the two expressions are not equivalent.',
                       f'{k}{v}: {", ".join(str(k * t) for t in vals)}; {v}{sup(k)}: {", ".join(str(t ** k) for t in vals)}. They differ for most values, so they are not equivalent.',
                       f'Table correct (A1 A1); equivalent expressions must be equal for every value of {v}; a single counter-example is enough (R1).', 3)
    c = rng.randint(2, 9)
    return explain(f'Explain why {k}({v} + {c}) and {k}{v} + {c} are not equivalent expressions. Use {v} = {c} to illustrate.',
                   f'{k}({v} + {c}) = {k}{v} + {k * c}; at {v} = {c}: {k * 2 * c} vs {k * c + c}.',
                   f'The {k} multiplies both terms in the bracket (R1); substitution shows different values (A1).', 2)


@R.add('ch04-st1', 'C4', (3, 5), 'multi_step')
def expr_pattern(rng, slot):
    k = rng.randint(3, 6)
    c = rng.randint(1, 4)
    n_ = rng.randint(10, 40)
    shape = {3: 'triangles', 4: 'squares', 5: 'pentagons', 6: 'hexagons'}[k]
    w, l = rng.randint(2, 6), rng.randint(3, 9)
    frames = [
        (f'Matchsticks are used to make a row of {shape} that share one side with the next. Pattern 1 uses {k} matches, pattern 2 uses {2 * k - 1}, pattern 3 uses {3 * k - 2}. (a) Write an expression for the number of matches in pattern n. (b) How many matches are in pattern {n_}? (c) Explain, using the shapes, why your expression works.',
         f'(a) {k - 1}n + 1 (b) {(k - 1) * n_ + 1} (c) each new {shape[:-1]} adds {k - 1} matches because one side is shared; the extra 1 is the first side'),
        (f'A rectangular garden has length (x + {l}) m and width {w} m. (a) Write an expression for its perimeter and simplify it. (b) Write an expression for its area. (c) Find the value of x if the perimeter is {2 * (n_ + l) + 2 * w} m.',
         f'(a) 2x + {2 * (l + w)} (b) {w}x + {w * l} (c) x = {n_}'),
        (f'A phone plan in {rng.choice(CITIES)} costs a fixed {c * 5} units per month plus {k} units per GB of data. (a) Write an expression for the monthly cost for g GB. (b) {name(rng)} uses {n_} GB. Find the cost. (c) Another plan costs {k + 2}g. Explain which is cheaper for small and large data use.',
         f'(a) {c * 5} + {k}g (b) {c * 5 + k * n_} (c) the second plan is cheaper when 2g < {c * 5}, i.e. g < {c * 5 / 2:g} GB; the first is cheaper for larger use'),
    ]
    q_, ans = rng.choice(frames)
    return short(q_, ans, f'{ans}. Expression formed from the pattern or context (B: M1 A1); evaluated (A1); general reasoning communicated (R1 C1).', 5, 'multi_step', 'G5')


R.facts('ch04-st2', F(
    terms=[('like terms', 'terms that contain exactly the same variables raised to the same powers, such as 3ab and −7ab'),
           ('expand', 'multiply out brackets so that the expression is written without them'),
           ('simplify', 'rewrite an expression in its shortest equivalent form by collecting like terms')],
    facts=[('Simplify 5x + 3y − 2x + y.', '3x + 4y', ['7xy', '3x + 3y', '8x + 4y'], 'Collect x terms: 5x − 2x = 3x; y terms: 3y + y = 4y.'),
           ('Expand −3(2a − 5).', '−6a + 15', ['−6a − 15', '6a − 15', '−6a − 5'], '−3 × 2a = −6a, −3 × −5 = +15.'),
           ('Which pair are like terms?', '4x²y and −x²y', ['4x²y and 4xy²', '3x and 3x²', '5ab and 5a'], 'Same variables with the same powers.')],
    why=[('Explain why 3x + 4y cannot be simplified.', '3x and 4y are unlike terms (different variables), so they cannot be collected into one term.'),
         ('Explain why 2x² and 3x are not like terms.', 'x² and x are different powers of x; they represent different quantities (an area and a length, for example).'),
         ('Explain how an area diagram shows that 4(x + 3) = 4x + 12.', 'A rectangle 4 by (x + 3) splits into a 4 by x rectangle (4x) and a 4 by 3 rectangle (12); the total area is 4x + 12.')],
    misc=[('3a + 2b = 5ab', '3a and 2b are unlike terms and cannot be combined; the expression stays 3a + 2b.'),
          ('5(x + 2) = 5x + 2', 'The 5 multiplies both terms: 5(x + 2) = 5x + 10.'),
          ('x × x = 2x', 'x × x = x²; 2x is x + x.')],
))


@R.add('ch04-st2', 'C3', (1, 3), 'short')
def collect_like(rng, slot):
    a, b = _sym(rng, 2)
    cs = [_rc(rng) for _ in range(4)]
    e = cs[0] * a + cs[1] * b + cs[2] * a + cs[3] * b
    if slot.d >= 3:
        e = e + _rc(rng) * a * b + _rc(rng) * a ** 2 + _rc(rng) * a * b
    raw = f'{m(cs[0])}{a} {sgn(cs[1]).strip()}{b} {sgn(cs[2]).strip()}{a} {sgn(cs[3]).strip()}{b}'.replace('+ ', '+ ').replace('  ', ' ')
    terms = [f'{m(cs[0])}{a}', f'{"+" if cs[1] > 0 else "−"} {abs(cs[1])}{b}', f'{"+" if cs[2] > 0 else "−"} {abs(cs[2])}{a}', f'{"+" if cs[3] > 0 else "−"} {abs(cs[3])}{b}']
    raw = ' '.join(terms)
    if slot.d >= 3:
        extra = sp.expand(e - (cs[0] * a + cs[1] * b + cs[2] * a + cs[3] * b))
        raw += ' + ' + poly(extra) if not poly(extra).startswith('−') else ' ' + poly(extra).replace('−', '− ', 1)
    raw = raw.replace('1' + str(a), str(a)) if False else raw
    res = poly(e)
    if res == '0':
        return None
    return short(f'Simplify {raw}.', res, f'Group like terms (M1); {res} (A1).', 2 if slot.d < 3 else 3)


@R.add('ch04-st2', 'C3', (1, 4), 'short')
def expand_simplify(rng, slot):
    (v,) = _sym(rng, 1)
    p, q, r_, s_ = _rc(rng, 2, 7), _rc(rng), _rc(rng, 2, 7), _rc(rng)
    t = rng.randint(1, 9)
    if slot.d <= 1:
        e = p * (v + q)
        return short(f'Expand {m(p)}({v} {sgn(q).strip()}).'.replace('( ', '('), poly(e), f'{m(p)} × {v} and {m(p)} × {m(q)} (M1); {poly(e)} (A1).', 2)
    if slot.d <= 3:
        e = p * (v + q) + r_ * (v + s_)
        return short(f'Expand and simplify {m(p)}({v}{sgn(q)}) {"+" if r_ > 0 else "−"} {abs(r_)}({v}{sgn(s_)}).', poly(e),
                     f'Expand each bracket with signs (M1 M1); collect: {poly(e)} (A1).', 3)
    e = p * v * (v + q) - r_ * (t * v + s_)
    return short(f'Expand and simplify {m(p)}{v}({v}{sgn(q)}) − {m(r_) if r_ > 0 else f"({m(r_)})"}({t if t > 1 else ""}{v}{sgn(s_)}).', poly(e),
                 f'Expand first bracket ({poly(p * v * (v + q))}) (M1); second bracket with the negative ({poly(-r_ * (t * v + s_))}) (M1); collect: {poly(e)} (A1).', 3)


@R.add('ch04-st2', 'C1', (1, 3), 'mcq')
def expand_mcq(rng, slot):
    (v,) = _sym(rng, 1)
    p, q = _rc(rng, 2, 9), _rc(rng)
    e = poly(p * (v + q))
    w = [poly(p * v + q), poly(p * v - p * q), poly(-p * v + p * q)]
    return mcq(rng, f'Which is the correct expansion of {m(p)}({v}{sgn(q)})?', e, w, f'Multiply both terms by {m(p)}: {e}.')


@R.add('ch04-st2', 'C2', (2, 4), 'explain')
def simplify_error(rng, slot):
    (v,) = _sym(rng, 1)
    p, q, r_ = rng.randint(2, 6), rng.randint(2, 9), rng.randint(2, 9)
    who = name(rng)
    kind = rng.choice(['neg', 'like', 'area'])
    if kind == 'neg':
        right = poly(p * v - r_ * (v - q))
        wrong = poly(p * v - r_ * v - r_ * q)
        return explain(f'{who} simplifies {p}{v} − {r_}({v} − {q}) and gets {wrong}. Explain the error and give the correct answer.', right,
                       f'−{r_} × −{q} = +{r_ * q}, not −{r_ * q} (R1); correct {right} (A1).', 2, 'G2')
    if kind == 'like':
        return explain(f'{who} writes {p}{v}² + {q}{v} = {p + q}{v}³. Explain why this is wrong.', f'{v}² and {v} are unlike terms, so {p}{v}² + {q}{v} cannot be simplified further.',
                       'Unlike terms identified (R1); numerical check e.g. ' + f'{v} = 1 gives {p + q} vs {p + q} but {v} = 2 gives {4 * p + 2 * q} vs {(p + q) * 8} (R1).', 2, 'G2')
    return explain(f'A rectangle is split into two parts with areas {p}{v} and {p * q}. Explain how this shows that {p}({v} + {q}) = {p}{v} + {p * q}.',
                   f'The rectangle has width {p} and length {v} + {q}; its area is {p}({v} + {q}), and it is also the sum of the parts {p}{v} + {p * q}.',
                   'Diagram dimensions identified (R1); two ways of finding the same area equated (R1).', 2)


@R.add('ch04-st2', 'C4', (3, 5), 'multi_step')
def expand_context(rng, slot):
    a, b, c = rng.randint(2, 6), rng.randint(1, 8), rng.randint(2, 5)
    who = name(rng)
    k = rng.randint(3, 9)
    frames = [
        (f'An L-shaped floor plan is made of a rectangle {a}x by (x + {b}) and a square of side x. (a) Write and simplify an expression for the total area. (b) Write and simplify an expression for the perimeter if the square is attached along part of the side of length {a}x. (c) Find the area when x = {c}.',
         f'(a) {poly(a * x * (x + b) + x ** 2)} (b) {poly(2 * a * x + 2 * (x + b) + 2 * x)} (c) {a * c * (c + b) + c * c}'),
        (f'{who} thinks of a number n, adds {k}, multiplies by {a}, subtracts {a * k} and then divides by {a}. (a) Write an expression for each step and simplify. (b) Explain why the answer is always the number {who} started with.',
         f'(a) n + {k} → {a}(n + {k}) = {a}n + {a * k} → {a}n → n (b) the steps undo each other: + {a * k} and − {a * k} cancel, and × {a} and ÷ {a} cancel'),
        (f'Investigate: choose three consecutive whole numbers n, n + 1, n + 2. (a) Show that their sum simplifies to 3(n + 1). (b) Explain what this tells you about the sum of any three consecutive whole numbers. (c) Does the sum of four consecutive whole numbers have a similar property?',
         '(a) n + n + 1 + n + 2 = 3n + 3 = 3(n + 1) (b) it is always a multiple of 3, equal to 3 × the middle number (c) 4n + 6 = 2(2n + 3): always even but never a multiple of 4'),
    ]
    q_, ans = rng.choice(frames)
    return short(q_, ans, f'{ans}. Expressions formed (M1); expanded and simplified correctly (M1 A1); generalisation justified algebraically (B/C: R1 C1).', 5, 'multi_step', 'G5')


R.facts('ch04-st3', F(
    terms=[('factorise', 'write an expression as a product of factors, the reverse of expanding'),
           ('highest common factor (HCF)', 'the largest number or term that divides exactly into every term of an expression'),
           ('fully factorised', 'factorised so that the terms left in the bracket have no common factor other than 1')],
    facts=[('Factorise 12x + 18.', '6(2x + 3)', ['3(4x + 6)', '6(2x + 18)', '12(x + 6)'], 'HCF of 12 and 18 is 6.'),
           ('What is the HCF of 8a²b and 12ab?', '4ab', ['4a²b', '2ab', '24a²b'], 'HCF of 8 and 12 is 4; lowest powers a and b.'),
           ('Factorise x² − 5x.', 'x(x − 5)', ['x(x − 5x)', '5x(x − 1)', 'x²(1 − 5)'], 'x is a factor of both terms.')],
    why=[('Explain how you can check that a factorisation is correct.', 'Expand the brackets: if you get back the original expression, the factorisation is correct.'),
         ('Explain why 4(3x + 6) is not fully factorised.', '3x + 6 still has a common factor of 3, so 4(3x + 6) = 12(x + 2).'),
         ('Explain why factorising is the reverse of expanding.', 'Expanding multiplies a factor into a bracket; factorising takes the common factor out of each term and puts it in front of a bracket.')],
    misc=[('6y + 9 = 3(2y + 9)', 'Divide each term by 3: 6y + 9 = 3(2y + 3).'),
          ('5a + 5 = 5a(1 + 1)', '5a(1 + 1) = 10a; the correct factorisation is 5(a + 1).')],
))


@R.add('ch04-st3', 'C3', (1, 4), 'short')
def factorise_common(rng, slot):
    (v,) = _sym(rng, 1)
    h = rng.randint(2, 9)
    p, q = rng.choice([(a_, b_) for a_ in range(1, 10) for b_ in range(1, 10) if math.gcd(a_, b_) == 1 and (a_, b_) != (1, 1)])
    sgn_ = rng.choice([1, -1])
    if slot.d <= 2:
        e = h * p * v + sgn_ * h * q
        ans = f'{h}({lin(p, sgn_ * q, str(v))})'
        return short(f'Factorise {poly(e)} completely.', ans, f'HCF {h} (M1); {ans} (A1).', 2)
    w = sp.Symbol(rng.choice([s for s in 'abkmpt' if s != str(v)]))
    e = h * p * v ** 2 * w + sgn_ * h * q * v * w
    inner = poly(p * v + sgn_ * q)
    ans = f'{h}{v}{w}({inner})'
    return short(f'Factorise fully {poly(e)}.', ans, f'HCF of the numbers {h} (A1); common variables {v}{w} (A1); {ans} (A1).', 3)


@R.add('ch04-st3', 'C3', (2, 4), 'numerical')
def factor_numeric(rng, slot):
    a, b = rng.randint(11, 99), rng.randint(11, 99)
    k = rng.choice([17, 23, 37, 43, 47, 63, 77, 99])
    c = 100 - a if rng.random() < 0.5 else rng.choice([10, 20, 30, 40]) - a % 10
    if c <= 0:
        c = 100 - a
    return short(f'Use factorisation to work out {k} × {a} + {k} × {c} without a calculator.', str(k * (a + c)),
                 f'{k}({a} + {c}) = {k} × {a + c} (M1) = {k * (a + c)} (A1).', 2, 'numerical')


@R.add('ch04-st3', 'C1', (1, 3), 'mcq')
def hcf_mcq(rng, slot):
    a, b = _sym(rng, 2)
    h = rng.randint(2, 6)
    p, q = rng.randint(2, 5), rng.randint(2, 5)
    while math.gcd(p, q) != 1:
        q += 1
    t1, t2 = poly(h * p * a ** 2 * b), poly(h * q * a * b ** 2)
    corr = poly(h * a * b)
    return mcq(rng, f'What is the highest common factor of {t1} and {t2}?', corr, [poly(h * a ** 2 * b ** 2), poly(a * b), poly(h * p * q * a * b)],
               f'HCF of {h * p} and {h * q} is {h}; lowest powers of {a} and {b} are {a}¹ and {b}¹.')


@R.add('ch04-st3', 'C2', (2, 4), 'explain')
def factor_explain(rng, slot):
    (v,) = _sym(rng, 1)
    h, p, q = rng.randint(2, 5), rng.randint(2, 4), rng.randint(1, 5)
    who = name(rng)
    full = h * p
    e = poly(full * h * v + full * q)
    partial = f'{h}({poly(full * v + p * q)})'
    return explain(f'{who} factorises {e} as {partial}. Explain why this is not fully factorised and give the full factorisation.',
                   f'The bracket {poly(full * v + p * q)} still has a common factor {p}; fully factorised: {full}({poly(h * v + q)}).',
                   f'Common factor remaining in the bracket identified (R1); {full}({poly(h * v + q)}) (A1).', 2, 'G2') if math.gcd(h, q) == 1 else None


@R.add('ch04-st3', 'C4', (3, 5), 'multi_step')
def factor_proof(rng, slot):
    k = rng.choice([2, 3, 5])
    who = name(rng)
    w = rng.randint(2, 9)
    frames = [
        (f'Investigate the sum of {k} consecutive whole numbers, starting with n. (a) Write and simplify the sum. (b) Factorise your answer. (c) Use the factorised form to explain what every such sum is divisible by.',
         {2: '(a) 2n + 1 (b) cannot be factorised: 2n + 1 (c) the sum of 2 consecutive whole numbers is always odd',
          3: '(a) 3n + 3 (b) 3(n + 1) (c) always divisible by 3',
          5: '(a) 5n + 10 (b) 5(n + 2) (c) always divisible by 5 (and equal to 5 × the middle number)'}[k]),
        (f'A rectangle has area {w}x² + {w * 3}x cm². (a) Factorise the expression. (b) {who} says the rectangle could be {w}x cm by (x + 3) cm or x cm by ({w}x + {3 * w}) cm. Explain whether both are possible. (c) Give one more pair of possible dimensions.',
         'RECT'),
        (f'Show that the sum of any two consecutive even numbers, 2n and 2n + 2, is always 2 more than a multiple of 4. Then use factorisation to explain what the sum of two consecutive odd numbers is always a multiple of.',
         '2n + 2n + 2 = 4n + 2 = 2(2n + 1) = 4n + 2 (2 more than a multiple of 4); odd numbers 2n + 1 and 2n + 3 sum to 4n + 4 = 4(n + 1), a multiple of 4'),
    ]
    q_, ans = rng.choice(frames)
    if ans == 'RECT':
        ans = f'(a) {w}x(x + 3) (b) yes – both have product {w}x² + {3 * w}x (c) e.g. {w}(x + 3) cm by x cm' + (f', or 2x cm by {fx(Fr(w, 2))}(x + 3) cm' if w % 2 == 0 else '')
    return short(q_, ans, f'{ans}. Algebraic expression formed (M1); factorised correctly (M1 A1); conclusion justified from the factorised form (B: R1 C1).', 5, 'multi_step', 'G5')


R.facts('ch04-st4', F(
    terms=[('formula', 'a rule, written with symbols, that connects two or more quantities, such as A = lw'),
           ('substitute', 'replace the variables in an expression or formula with given numbers'),
           ('subject of a formula', 'the variable on its own on one side of the formula, e.g. v in v = u + at'),
           ('rearrange', 'use inverse operations to change which variable is the subject of a formula')],
    facts=[('If a = 3 and b = −2, what is a² − 2b?', '13', ['5', '1', '−1'], '9 − 2(−2) = 9 + 4 = 13.'),
           ('Make x the subject of y = x + 7.', 'x = y − 7', ['x = y + 7', 'x = 7 − y', 'x = 7y'], 'Subtract 7 from both sides.'),
           ('Make r the subject of C = 2πr.', 'r = C/(2π)', ['r = 2πC', 'r = C − 2π', 'r = 2π/C'], 'Divide both sides by 2π.')],
    why=[('Explain why brackets help when substituting a negative number into a formula.', 'Brackets keep the sign with the number, so (−3)² = 9 is not confused with −3² = −9, and −(−3) is clearly +3.'),
         ('Explain why you must do the same operation to both sides when rearranging a formula.', 'A formula is an equation; doing the same thing to both sides keeps the two sides equal, so the relationship stays true.'),
         ('Explain why the order of inverse operations matters when rearranging y = 3x + 5.', 'x was multiplied by 3 and then 5 was added; undoing them in reverse order, subtract 5 first and then divide by 3, gives x = (y − 5)/3.')],
    misc=[('If y = 4x − 1, then x = y/4 − 1.', 'Add 1 first, then divide by 4: x = (y + 1)/4.'),
          ('Substituting x = −2 into x² gives −4.', '(−2)² = (−2)(−2) = 4.')],
))


@R.add('ch04-st4', 'C3', (1, 4), 'short')
def substitute(rng, slot):
    a, b = _rc(rng, 1, 8), _rc(rng, 1, 8)
    c = rng.randint(2, 6)
    s, t = sp.symbols('s t')
    forms = [
        (s * t + c, f'st + {c}'),
        (s ** 2 - c * t, f's² − {c}t'),
        (c * (s - t) ** 2, f'{c}(s − t)²'),
        ((s + c * t) / 2, f'(s + {c}t)/2'),
        (s ** 3 + t ** 2 - s * t, 's³ + t² − st'),
    ]
    e, txt = rng.choice(forms[:2] if slot.d <= 2 else forms)
    v = e.subs({s: a, t: b})
    return short(f'Given s = {m(a)} and t = {m(b)}, find the value of {txt}.', fr(v), f'Substitute with brackets for negatives (M1); {fr(v)} (A1).', 2)


@R.add('ch04-st4', 'C3', (1, 4), 'short')
def formula_use(rng, slot):
    who = name(rng)
    city = rng.choice(CITIES)
    kind = rng.choice(['temp', 'speed', 'kin', 'tri', 'bmi'])
    if kind == 'temp':
        C = rng.randint(-15, 40)
        Fv = Fr(9, 5) * C + 32
        return short(f'The formula F = 9C/5 + 32 converts degrees Celsius to Fahrenheit. The temperature in {city} is {m(C)} °C. Find it in °F.', f'{fx(Fv)} °F'.replace('/5', '/5'),
                     f'9 × {m(C)}/5 + 32 (M1) = {g(float(Fv), 4)} °F (A1).', 2)
    if kind == 'speed':
        d_, t_ = rng.randint(30, 600), rng.choice([0.5, 1.5, 2, 2.5, 3, 4])
        return short(f'Average speed is given by s = d/t. A train from {city} travels {d_} km in {t_:g} hours. Find its average speed.', f'{g(d_ / t_, 4)} km/h',
                     f'{d_} ÷ {t_:g} (M1) = {g(d_ / t_, 4)} km/h (A1).', 2)
    if kind == 'kin':
        u, a_, t_ = rng.randint(0, 20), rng.randint(-4, 6), rng.randint(2, 10)
        return short(f'Use v = u + at to find v when u = {u} m/s, a = {m(a_)} m/s² and t = {t_} s.', f'{m(u + a_ * t_)} m/s',
                     f'{u} + ({m(a_)})({t_}) (M1) = {m(u + a_ * t_)} m/s (A1).', 2)
    if kind == 'tri':
        b_, h_ = rng.randint(3, 25), rng.randint(2, 20)
        A = Fr(b_ * h_, 2)
        return short(f'The area of a triangle is A = ½bh. Find the base b when A = {g(float(A))} cm² and h = {h_} cm.', f'{b_} cm',
                     f'{g(float(A))} = ½ × b × {h_} (M1); b = 2A/h = {b_} cm (A1).', 2)
    mass, hgt = rng.randint(40, 90), Decimal(rng.randint(150, 190)) / 100
    bmi = Decimal(mass) / (hgt * hgt)
    return short(f'Body mass index is BMI = m/h², with m in kg and h in metres. Find the BMI of an adult with mass {mass} kg and height {hgt} m, to 1 decimal place.', f'{rnd(bmi, 1)}',
                 f'{mass} ÷ {hgt}² (M1) = {rnd(bmi, 1)} (A1).', 2)


@R.add('ch04-st4', 'C3', (2, 4), 'short')
def rearrange(rng, slot):
    k, c = rng.randint(2, 9), rng.randint(1, 15)
    forms = [
        (f'y = {k}x + {c}', 'x', f'x = (y − {c})/{k}'),
        (f'y = {k}x − {c}', 'x', f'x = (y + {c})/{k}'),
        (f'P = 2l + 2w', 'l', 'l = (P − 2w)/2'),
        (f'A = ½bh', 'h', 'h = 2A/b'),
        (f'v = u + at', 'a', 'a = (v − u)/t'),
        (f'C = {k}n + {c}', 'n', f'n = (C − {c})/{k}'),
        (f'T = {c} − {k}d', 'd', f'd = ({c} − T)/{k}'),
        (f'y = (x + {c})/{k}', 'x', f'x = {k}y − {c}'),
    ]
    f_, v, ans = rng.choice(forms[:2] if slot.d <= 2 else forms)
    return short(f'Make {v} the subject of the formula {f_}.', ans, f'Undo the operations in reverse order, doing the same to both sides (M1); {ans} (A1).', 2)


@R.add('ch04-st4', 'C1', (1, 3), 'mcq')
def subst_mcq(rng, slot):
    a = rng.randint(2, 6)
    b = -rng.randint(1, 5)
    v = 3 * a - b ** 2
    w = [3 * a + b ** 2, 3 * a - abs(b) * 2, 3 + a - b ** 2]
    return mcq(rng, f'If p = {a} and q = {m(b)}, what is the value of 3p − q²?', m(v), [m(t) for t in w], f'3({a}) − ({m(b)})² = {3 * a} − {b * b} = {m(v)}.')


@R.add('ch04-st4', 'C2', (2, 4), 'explain')
def rearr_error(rng, slot):
    k, c = rng.randint(2, 9), rng.randint(2, 12)
    who = name(rng)
    yv = rng.randint(20, 60)
    return explain(f'{who} rearranges y = {k}x + {c} to make x the subject and writes x = y/{k} − {c}. Explain the mistake, give the correct formula and check it with y = {yv}.',
                   f'{c} must be subtracted before dividing by {k}: x = (y − {c})/{k}; for y = {yv}, x = {fx(Fr(yv - c, k))} (check: {k} × {fx(Fr(yv - c, k))} + {c} = {yv}).',
                   'Wrong order of inverse operations identified (R1); correct formula (A1); numerical check (A1).', 3, 'G2')


@R.add('ch04-st4', 'C4', (3, 5), 'multi_step')
def formula_context(rng, slot):
    city, country, cur, cname = place(rng)
    who = name(rng)
    fixed, per = rng.randint(3, 8), Decimal(rng.randint(120, 320)) / 100
    budget = rng.randint(25, 60)
    km = (Decimal(budget) - fixed) / per
    age = rng.randint(14, 18)
    hr = 220 - age
    frames = [
        (f'A taxi in {city} charges C = {fixed} + {per}d ({cname}) for a journey of d km. (a) Find the cost of a {rng.randint(4, 15)} km journey. (b) Rearrange to make d the subject. (c) {who} has {cur}{budget}. How far can {who} travel, to the nearest 0.1 km?',
         None),
        (f'Sports coaches estimate maximum heart rate with H = 220 − A, where A is age in years, and a training zone of 0.6H to 0.8H. (a) Find the training zone for a {age}-year-old. (b) Rearrange H = 220 − A to make A the subject. (c) Explain one limitation of using a formula like this.',
         f'(a) {0.6 * hr:g} to {0.8 * hr:g} beats per minute (b) A = 220 − H (c) it is an average – individuals vary with fitness and health'),
    ]
    q_, ans = rng.choice(frames)
    if ans is None:
        dd = int(q_.split('cost of a ')[1].split(' km')[0])
        ans = f'(a) {money(cur, fixed + per * dd)} (b) d = (C − {fixed})/{per} (c) {rnd(km, 2) // Decimal("0.1") * Decimal("0.1"):.1f} km (round down so the fare does not exceed the budget)'
    return short(q_, ans, f'{ans}. Substitution (M1 A1); rearrangement with inverse operations (M1 A1); interpretation of the result in context (D: R1).', 5, 'multi_step', 'G5')


# =============================================================================================
# ch05 Linear Equations and Inequalities
# =============================================================================================
def _eq_txt(a, b, rhs, v='x'):
    return f'{lin(a, b, v)} = {m(rhs)}'


R.facts('ch05-st1', F(
    terms=[('equation', 'a statement that two expressions are equal, containing an unknown to be found'),
           ('solution', 'the value of the unknown that makes an equation true'),
           ('inverse operation', 'the operation that undoes another, e.g. subtraction undoes addition')],
    facts=[('Solve 3x + 5 = 20.', 'x = 5', ['x = 25/3', 'x = 15', 'x = 8.3'], '3x = 15, so x = 5.'),
           ('What is the first step to solve x/4 − 2 = 6?', 'add 2 to both sides', ['multiply only the x term by 4', 'subtract 6 from both sides', 'divide both sides by 4'], 'Undo the last operation (− 2) first.'),
           ('Which value of n satisfies 7 − n = 10?', 'n = −3', ['n = 3', 'n = 17', 'n = −17'], '7 − (−3) = 10.')],
    why=[('Explain why you must do the same operation to both sides of an equation.', 'An equation is like a balance; changing both sides in the same way keeps them equal, so the solution is unchanged.'),
         ('Explain how you can check the solution of an equation.', 'Substitute the value back into the original equation; if both sides are equal the solution is correct.'),
         ('Explain why the steps for solving 2x + 3 = 11 are "subtract 3, then divide by 2".', 'x was multiplied by 2 and then 3 was added; the inverse operations are applied in reverse order.')],
    misc=[('If 4x = 12, then x = 12 − 4 = 8.', '4x means 4 × x, so divide by 4: x = 3.'),
          ('x − 6 = 2, so x = −4.', 'Add 6 to both sides: x = 8.')],
))


@R.add('ch05-st1', 'C3', (1, 3), 'short')
def solve_two_step(rng, slot):
    v = rng.choice(['x', 'n', 'y', 'p', 'a'])
    sol = rng.randint(-9, 12)
    a, b = rng.randint(2, 9), _rc(rng, 1, 15)
    if slot.d <= 1:
        kind = rng.choice(['add', 'mul'])
        if kind == 'add':
            return short(f'Solve {v} {sgn(b).strip()} = {m(sol + b)}.', f'{v} = {m(sol)}', f'Inverse operation (M1); {v} = {m(sol)} (A1).', 1)
        return short(f'Solve {a}{v} = {m(a * sol)}.', f'{v} = {m(sol)}', f'Divide by {a} (M1); {v} = {m(sol)} (A1).', 1)
    if rng.random() < 0.3:
        rhs = Fr(sol, a) + b
        if rhs.denominator != 1:
            sol = a * rng.randint(-4, 5)
            rhs = Fr(sol, a) + b
        return short(f'Solve {v}/{a} {sgn(b).strip()} = {m(rhs)}.', f'{v} = {m(sol)}', f'{"Subtract" if b > 0 else "Add"} {abs(b)} (M1); multiply by {a} (M1); {v} = {m(sol)} (A1).', 2)
    rhs = a * sol + b
    return short(f'Solve {_eq_txt(a, b, rhs, v)}.', f'{v} = {m(sol)}', f'{a}{v} = {m(rhs - b)} (M1); {v} = {m(sol)} (A1).', 2)


@R.add('ch05-st1', 'C3', (2, 4), 'short')
def solve_frac_answer(rng, slot):
    a = rng.choice([2, 3, 4, 5, 6, 8])
    b = _rc(rng, 1, 12)
    rhs = rng.randint(-20, 30)
    sol = Fr(rhs - b, a)
    if sol.denominator == 1:
        return None
    return short(f'Solve {_eq_txt(a, b, rhs)}, giving your answer as a fraction or a decimal.', f'x = {fx(sol)} = {g(float(sol), 4)}',
                 f'{a}x = {m(rhs - b)} (M1); x = {fx(sol)} (A1).', 2)


@R.add('ch05-st1', 'C1', (1, 3), 'mcq')
def solve_mcq(rng, slot):
    a, sol = rng.randint(2, 9), rng.randint(-6, 10)
    b = _rc(rng, 1, 12)
    rhs = a * sol + b
    w = [Fr(rhs + b, a), Fr(rhs, a) - b, Fr(rhs - b) - a]
    return mcq(rng, f'What is the solution of {_eq_txt(a, b, rhs)}?', f'x = {m(sol)}', [f'x = {fx(t)}' for t in w], f'{a}x = {m(rhs - b)}, so x = {m(sol)}.')


@R.add('ch05-st1', 'C2', (2, 4), 'explain')
def solve_check(rng, slot):
    a, sol = rng.randint(2, 9), rng.randint(-5, 10)
    b = rng.randint(1, 12)
    rhs = a * sol - b
    who = name(rng)
    wrong = Fr(rhs - b, a)
    return explain(f'{who} solves {a}x − {b} = {m(rhs)} and gets x = {fx(wrong)}. By substituting, show that this is wrong, explain the error and find the correct solution.',
                   f'{a}({fx(wrong)}) − {b} = {fx(a * wrong - b)} ≠ {m(rhs)}; {who} subtracted {b} instead of adding it. Correct: x = {m(sol)}.',
                   'Substitution shows the error (M1); wrong inverse operation identified (R1); correct solution (A1).', 3, 'G2')


@R.add('ch05-st1', 'C4', (3, 5), 'multi_step')
def eq_context1(rng, slot):
    city, country, cur, cname = place(rng)
    who = name(rng)
    fee, per = rng.randint(5, 30), rng.randint(3, 15)
    n_ = rng.randint(4, 20)
    total = fee + per * n_
    a, sol = rng.randint(3, 8), rng.randint(5, 25)
    frames = [
        (f'A climbing gym in {city} charges a joining fee of {cur}{fee} plus {cur}{per} per visit. {who} has paid {cur}{total} in total. (a) Write an equation for the number of visits v. (b) Solve it. (c) A rival gym charges {cur}{per + 2} per visit with no fee. After how many visits is the first gym cheaper?',
         f'(a) {fee} + {per}v = {total} (b) v = {n_} (c) when {per + 2}v > {fee} + {per}v, i.e. v > {fee / 2:g}, so from {math.floor(fee / 2) + 1} visits'),
        (f'{who} thinks of a number, multiplies it by {a}, then subtracts {a + 3}. The result is {a * sol - a - 3}. (a) Write an equation and solve it to find the number. (b) Show that "multiply by {a} and subtract {a + 3}" can be undone by "add {a + 3} and divide by {a}" for any starting number.',
         f'(a) {a}n − {a + 3} = {a * sol - a - 3}, n = {sol} (b) ({a}n − {a + 3} + {a + 3})/{a} = {a}n/{a} = n'),
    ]
    q_, ans = rng.choice(frames)
    return short(q_, ans, f'{ans}. Equation formed from the context (M1 A1); solved with inverse operations (M1 A1); interpreted/justified (D/B: R1).', 5, 'multi_step', 'G5')


R.facts('ch05-st2', F(
    terms=[('unknowns on both sides', 'an equation such as 5x + 2 = 3x + 10 where the variable appears on both sides and must be collected on one side'),
           ('lowest common multiple (LCM) of denominators', 'the number used to multiply every term of an equation with fractions so that all the denominators disappear')],
    facts=[('Solve 5x + 2 = 3x + 10.', 'x = 4', ['x = 1.5', 'x = 6', 'x = 12/8'], '2x = 8, so x = 4.'),
           ('Solve 3(x − 2) = 12.', 'x = 6', ['x = 4.67', 'x = 2', 'x = 14/3'], 'x − 2 = 4, so x = 6.'),
           ('What should you multiply both sides of x/3 + x/4 = 7 by to clear the fractions?', '12', ['7', '3', '4'], '12 is the LCM of 3 and 4.')],
    why=[('Explain why it is usually best to collect the x terms on the side with the larger coefficient.', 'Subtracting the smaller x term leaves a positive coefficient, which avoids mistakes with negative signs.'),
         ('Explain why every term must be multiplied when clearing fractions from an equation.', 'Multiplying both sides by the same number keeps them equal; if one term is missed, the two sides are no longer multiplied by the same amount.'),
         ('Explain why the equation 2(x + 3) = 2x + 5 has no solution.', 'Expanding gives 2x + 6 = 2x + 5, so 6 = 5, which is never true; there is no value of x that works.')],
    misc=[('In 5x = 2x + 9, subtract 5x from 2x to get 3x = 9.', 'Subtract 2x from both sides: 3x = 9; you cannot subtract a term from one side only.'),
          ('To solve x/2 + 3 = 5, multiply the x term by 2 to get x + 3 = 5.', 'Every term must be multiplied: x + 6 = 10, so x = 4.')],
))


@R.add('ch05-st2', 'C3', (1, 4), 'short')
def solve_both_sides(rng, slot):
    sol = rng.randint(-8, 12)
    a, c = rng.sample(range(2, 10), 2)
    b = _rc(rng, 1, 15)
    d_ = a * sol + b - c * sol
    return short(f'Solve {lin(a, b)} = {lin(c, d_)}.', f'x = {m(sol)}', f'Collect x terms: {m(a - c)}x = {m(d_ - b)} (M1 A1); x = {m(sol)} (A1).', 3)


@R.add('ch05-st2', 'C3', (2, 4), 'short')
def solve_brackets(rng, slot):
    sol = rng.randint(-6, 10)
    p, q = rng.randint(2, 6), _rc(rng, 1, 9)
    r_, s_ = rng.randint(2, 5), _rc(rng, 1, 9)
    if slot.d <= 2:
        rhs = p * (sol + q)
        return short(f'Solve {p}(x{sgn(q)}) = {m(rhs)}.', f'x = {m(sol)}', f'Expand or divide by {p} (M1); x = {m(sol)} (A1).', 2)
    lhs = p * (sol + q)
    t = rng.randint(1, 4)
    rhs_c = lhs - r_ * (t * sol + s_)
    if r_ * t == p:
        return None
    sol_check = sp.solve(sp.Eq(p * (x + q), r_ * (t * x + s_) + rhs_c), x)
    if sol_check != [sol]:
        return None
    return short(f'Solve {p}(x{sgn(q)}) = {r_}({t if t > 1 else ""}x{sgn(s_)}){sgn(rhs_c) if rhs_c else ""}.', f'x = {m(sol)}',
                 f'Expand both sides (M1); collect like terms (M1); x = {m(sol)} (A1).', 3)


@R.add('ch05-st2', 'C3', (3, 5), 'short')
def solve_fractions(rng, slot):
    a, b = rng.sample([2, 3, 4, 5, 6], 2)
    sol = a * b * rng.randint(-3, 5)
    if slot.d <= 3:
        c = rng.randint(1, 9)
        rhs = Fr(sol, a) + c
        return short(f'Solve x/{a} + {c} = {fx(rhs)}.', f'x = {m(sol)}', f'x/{a} = {fx(rhs - c)} (M1); x = {m(sol)} (A1).', 2)
    rhs = Fr(sol, a) + Fr(sol, b)
    if rng.random() < 0.5:
        k = rng.randint(1, 5)
        rhs2 = Fr(sol + k, a)
        lhs_txt = f'(x + {k})/{a}'
        right = Fr(sol - k, b) if False else None
        sol2 = rng.randint(-5, 9)
        # (x + k)/a = (x - j)/b  -> b(x + k) = a(x - j)
        j = rng.randint(1, 6)
        if a == b:
            return None
        s = sp.solve(sp.Eq((x + k) / a, (x - j) / b), x)[0]
        return short(f'Solve (x + {k})/{a} = (x − {j})/{b}.', f'x = {fr(s)}', f'Cross-multiply: {b}(x + {k}) = {a}(x − {j}) (M1); expand and collect (M1); x = {fr(s)} (A1).', 3)
    return short(f'Solve x/{a} + x/{b} = {fx(rhs)}.', f'x = {m(sol)}', f'Multiply every term by {a * b // math.gcd(a, b)} (M1); collect (M1); x = {m(sol)} (A1).', 3)


@R.add('ch05-st2', 'C1', (1, 3), 'mcq')
def both_sides_mcq(rng, slot):
    sol = rng.randint(-5, 9)
    a, c = rng.sample(range(2, 10), 2)
    if a < c:
        a, c = c, a
    b = rng.randint(1, 12)
    d_ = a * sol + b - c * sol
    return mcq(rng, f'What is the first correct step to solve {lin(a, b)} = {lin(c, d_)}?', f'subtract {c}x from both sides to get {lin(a - c, b)} = {m(d_)}',
               [f'add {c}x to both sides to get {lin(a + c, b)} = {m(d_)}', f'divide both sides by {a} to get x + {b} = {m(d_)}', f'subtract {b} from the left side only to get {a}x = {lin(c, d_)}'],
               f'Collect the x terms on one side by subtracting {c}x from both sides.')


@R.add('ch05-st2', 'C2', (2, 4), 'explain')
def special_eq(rng, slot):
    a, b = rng.randint(2, 6), rng.randint(1, 9)
    c = rng.randint(1, 9)
    kind = rng.choice(['none', 'all'])
    if kind == 'none':
        return explain(f'Explain why the equation {a}(x + {b}) = {a}x + {a * b + c} has no solution.', f'{a}x + {a * b} = {a}x + {a * b + c} gives {a * b} = {a * b + c}, which is false for every x.',
                       'Expansion (M1); contradiction identified (R1).', 2)
    return explain(f'Explain why every value of x is a solution of {a}(x + {b}) − {c} = {a}x + {a * b - c}.', f'The left side expands to {a}x + {a * b - c}, identical to the right side, so the equation is an identity.',
                   'Expansion (M1); both sides identical ⇒ true for all x (R1).', 2)


@R.add('ch05-st2', 'C4', (3, 5), 'multi_step')
def eq_context2(rng, slot):
    city, country, cur, cname = place(rng)
    who = name(rng)
    a, b = rng.randint(10, 40), rng.randint(2, 6)
    c, d_ = a + rng.randint(5, 30), b - rng.randint(1, b - 1) if b > 1 else 1
    if (c - a) % (b - d_) != 0 or b == d_:
        return None
    n_ = (c - a) // (b - d_)
    w = rng.randint(3, 9)
    frames = [
        (f'Two streaming services are available in {city}: Service A costs {cur}{a} to join plus {cur}{b} per month; Service B costs {cur}{c} to join plus {cur}{d_} per month. (a) Write an equation for when the total costs are equal. (b) Solve it. (c) Advise {who}, who plans to subscribe for a year.',
         f'(a) {a} + {lin(b, 0, "m")} = {c} + {lin(d_, 0, "m")} (b) m = {n_} (c) after 12 months A costs {cur}{a + 12 * b}, B costs {cur}{c + 12 * d_}; choose {"A" if a + 12 * b < c + 12 * d_ else "B" if a + 12 * b > c + 12 * d_ else "either"}'),
        (f'The perimeter of a rectangle is the same as the perimeter of an equilateral triangle. The rectangle measures (x + {w}) cm by (2x − 1) cm and each side of the triangle is (x + {w + 3}) cm. (a) Form and solve an equation. (b) Find the perimeter. (c) Check that all lengths are positive.',
         None),
    ]
    q_, ans = rng.choice(frames)
    if ans is None:
        s = sp.solve(sp.Eq(2 * (x + w) + 2 * (2 * x - 1), 3 * (x + w + 3)), x)[0]
        per = 3 * (s + w + 3)
        ans = f'(a) 2(x + {w}) + 2(2x − 1) = 3(x + {w + 3}) ⇒ 6x + {2 * w - 2} = 3x + {3 * w + 9}, x = {fr(s)} (b) {fr(per)} cm (c) sides {fr(s + w)}, {fr(2 * s - 1)}, {fr(s + w + 3)} cm, all positive'
    return short(q_, ans, f'{ans}. Equation set up with brackets (M1 A1); solved (M1 A1); answer checked or interpreted in context (D: R1).', 5, 'multi_step', 'G5')


R.facts('ch05-st3', F(
    terms=[('forming an equation', 'translating a word problem into an equation by choosing a letter for the unknown and writing the relationship'),
           ('consecutive integers', 'integers that follow each other in order, such as n, n + 1, n + 2')],
    facts=[('The sum of a number and 9 is 23. Which equation represents this?', 'n + 9 = 23', ['9n = 23', 'n − 9 = 23', 'n = 23 + 9'], '"Sum" means addition.'),
           ('Three consecutive integers add to 48. What is the smallest?', '15', ['16', '14', '12'], 'n + n + 1 + n + 2 = 48 ⇒ 3n = 45.'),
           ('A rectangle is twice as long as it is wide; its perimeter is 36 cm. What is the width?', '6 cm', ['9 cm', '12 cm', '18 cm'], '2(2w + w) = 36 ⇒ 6w = 36.')],
    why=[('Explain why you should define what your letter stands for when forming an equation.', 'Stating "let n be the number of tickets" makes the meaning of the equation and its solution clear to the reader.'),
         ('Explain why you should check the answer to a word problem in the original words, not just in the equation.', 'If the equation was formed incorrectly, its solution will satisfy the wrong equation; checking in the story catches this and checks the answer is sensible.'),
         ('Explain why a solution such as 7.5 people must be rejected or interpreted.', 'The number of people must be a whole number, so the model or the question needs re-examining (e.g. round up for minibuses).')],
    misc=[('"5 less than a number is 12" gives 5 − n = 12.', 'Start with the number and take 5 away: n − 5 = 12, so n = 17.'),
          ('Ana is 3 years older than Ben, so if Ben is b, Ana is 3b.', 'Older by 3 means add 3: Ana is b + 3.')],
))


@R.add('ch05-st3', 'C3', (1, 4), 'short')
def word_eq(rng, slot):
    who, who2 = two_names(rng)
    city, country, cur, cname = place(rng)
    n_ = rng.randint(4, 30)
    k = rng.randint(2, 5)
    c = rng.randint(2, 12)
    cases = [
        (f'{who} is {k} times as old as {who2}. The sum of their ages is {(k + 1) * n_}. Form and solve an equation to find their ages.', f'{who2} {n_}, {who} {k * n_}', f'a + {k}a = {(k + 1) * n_} (M1); a = {n_} (A1); both ages stated (A1).'),
        (f'The sum of three consecutive integers is {3 * n_ + 3}. Form an equation and find the integers.', f'{n_}, {n_ + 1}, {n_ + 2}', f'n + (n + 1) + (n + 2) = {3 * n_ + 3} (M1); 3n + 3 = {3 * n_ + 3} (A1); {n_}, {n_ + 1}, {n_ + 2} (A1).'),
        (f'In {city}, a concert ticket costs {cur}{c} more than a cinema ticket. {who} buys 2 concert tickets and 3 cinema tickets for {cur}{5 * n_ + 2 * c}. Find the price of a cinema ticket.', f'{cur}{n_}', f'3t + 2(t + {c}) = {5 * n_ + 2 * c} (M1); 5t = {5 * n_} (A1); t = {cur}{n_} (A1).'),
        (f'A rectangle has length {k} cm more than its width. Its perimeter is {4 * n_ + 2 * k} cm. Find its width and length.', f'width {n_} cm, length {n_ + k} cm', f'2(w + w + {k}) = {4 * n_ + 2 * k} (M1); 4w = {4 * n_} (A1); dimensions (A1).'),
        (f'The angles of a triangle are x°, (x + {c})° and {k}x°. Find x.', None, None),
    ]
    q_, ans, key = rng.choice(cases)
    if ans is None:
        s = Fr(180 - c, k + 2)
        if s.denominator != 1:
            return None
        ans, key = f'x = {s}', f'x + x + {c} + {k}x = 180 (M1); {k + 2}x = {180 - c} (A1); x = {s} (A1).'
    return short(q_, ans, key, 3)


@R.add('ch05-st3', 'C1', (1, 3), 'mcq')
def form_mcq(rng, slot):
    k, c, t = rng.randint(2, 6), rng.randint(2, 15), rng.randint(20, 80)
    who = name(rng)
    stem = f'{who} doubles a number, then adds {c}, and gets {t}. Which equation is correct?' if k == 2 else f'{who} multiplies a number by {k}, then subtracts {c}, and gets {t}. Which equation is correct?'
    corr = f'2n + {c} = {t}' if k == 2 else f'{k}n − {c} = {t}'
    w = [f'2(n + {c}) = {t}', f'n² + {c} = {t}', f'2n = {t} + {c}'] if k == 2 else [f'{k}(n − {c}) = {t}', f'{c} − {k}n = {t}', f'{k}n = {t} − {c}']
    return mcq(rng, stem, corr, w, f'The operations happen in the order described: {corr}.')


@R.add('ch05-st3', 'C2', (2, 4), 'explain')
def form_explain(rng, slot):
    who = name(rng)
    n_ = rng.randint(5, 25)
    k = rng.choice([4, 6, 8, 12])
    seats = n_ * k + rng.randint(1, k - 1)
    sol = Fr(seats, k)
    return explain(f'A school in {rng.choice(CITIES)} needs to take {seats} students on a trip by minibus. Each minibus seats {k}. {who} solves {k}m = {seats} and gets m = {g(float(sol), 4)}. Explain how {who} should interpret this solution.',
                   f'm = {g(float(sol), 4)} is not a whole number of minibuses; round up to {math.ceil(sol)} so every student has a seat.',
                   'Solution interpreted in context (R1); rounding up justified (R1).', 2)


@R.add('ch05-st3', 'C4', (3, 5), 'multi_step')
def form_context(rng, slot):
    city, country, cur, cname = place(rng)
    who, who2 = two_names(rng)
    a = rng.randint(5, 20)
    s1, s2 = rng.randint(30, 60), rng.randint(60, 100)
    t = rng.randint(2, 5)
    total = s1 * t + s2 * t
    w_ = rng.randint(4, 12)
    frames = [
        (f'{who} and {who2} drive towards each other from two towns {total} km apart near {city}, starting at the same time. {who} drives at {s1} km/h and {who2} at {s2} km/h. (a) Form an equation for the time t hours until they meet. (b) Solve it. (c) How far from {who}’s town do they meet?',
         f'(a) {s1}t + {s2}t = {total} (b) t = {t} hours (c) {s1 * t} km'),
        (f'A garden in {city} is a rectangle whose length is 3 m more than twice its width. A fence around it costs {cur}{w_} per metre and the total cost is {cur}{w_ * (6 * a + 6)}. (a) Form an equation for the width w. (b) Solve it. (c) Find the area of the garden.',
         f'(a) {w_} × 2(w + 2w + 3) = {w_ * (6 * a + 6)} (b) w = {a} m (c) {a * (2 * a + 3)} m²'),
        (f'{who} is {a} years older than {who2}. In {t} years’ time {who} will be twice as old as {who2}. (a) Let {who2}’s age now be x and form an equation. (b) Solve it. (c) Check your answer in the words of the problem.',
         f'(a) x + {a} + {t} = 2(x + {t}) (b) x = {a - t} (c) now {a - t} and {2 * a - t}; in {t} years {a} and {2 * a} ✓'),
    ]
    q_, ans = rng.choice(frames)
    if 'x = ' in ans and a - t <= 0:
        return None
    return short(q_, ans, f'{ans}. Unknown defined and equation formed (M1 A1); solved (M1 A1); checked/interpreted in context (D: R1 C1).', 6, 'multi_step', 'G5')


R.facts('ch05-st4', F(
    terms=[('inequality', 'a statement that one quantity is less than (<), greater than (>), less than or equal to (≤) or greater than or equal to (≥) another'),
           ('solution set', 'all the values of the variable that make an inequality true'),
           ('open circle', 'the symbol on a number line showing that the end value is NOT included (< or >)'),
           ('closed circle', 'the filled symbol on a number line showing that the end value IS included (≤ or ≥)')],
    facts=[('Which inequality is shown by an open circle at 3 with an arrow to the left?', 'x < 3', ['x ≤ 3', 'x > 3', 'x ≥ 3'], 'Open circle: 3 not included; arrow left: smaller values.'),
           ('Solve 2x − 1 > 7.', 'x > 4', ['x < 4', 'x > 3', 'x ≥ 4'], '2x > 8 so x > 4.'),
           ('Solve −3x ≤ 12.', 'x ≥ −4', ['x ≤ −4', 'x ≥ 4', 'x ≤ 4'], 'Dividing by a negative reverses the sign.'),
           ('Which integers satisfy −2 < n ≤ 1?', '−1, 0, 1', ['−2, −1, 0, 1', '−1, 0', '−2, −1, 0'], '−2 is excluded, 1 is included.')],
    why=[('Explain why the inequality sign reverses when you multiply or divide by a negative number.', 'Multiplying by −1 reflects numbers in 0 on the number line, so their order is reversed: 2 < 5 but −2 > −5.'),
         ('Explain the difference between x < 4 and x ≤ 4.', 'x < 4 does not include 4 (open circle) while x ≤ 4 includes 4 (closed circle).'),
         ('Explain why an inequality usually has infinitely many solutions.', 'It describes a whole range of values, and between any two numbers in the range there are infinitely many more.')],
    misc=[('−2x > 6 gives x > −3.', 'Dividing by −2 reverses the sign: x < −3.'),
          ('x > 2 is shown with a closed circle at 2.', 'x > 2 does not include 2, so it uses an open circle.')],
))


def _ineq(rng):
    return rng.choice(['<', '>', '≤', '≥'])


FLIP = {'<': '>', '>': '<', '≤': '≥', '≥': '≤'}


@R.add('ch05-st4', 'C3', (1, 4), 'short')
def solve_ineq(rng, slot):
    s = _ineq(rng)
    a = rng.randint(2, 7)
    sol = rng.randint(-6, 9)
    b = _rc(rng, 1, 12)
    if slot.d >= 3 and rng.random() < 0.6:
        a = -a
    rhs = a * sol + b
    res = s if a > 0 else FLIP[s]
    circ = 'closed' if res in '≤≥' else 'open'
    dirn = 'right' if res in '>≥' else 'left'
    stem = f'Solve {lin(a, b)} {s} {m(rhs)} and describe how to show the solution on a number line.' if slot.d >= 2 else f'Solve {lin(a, b)} {s} {m(rhs)}.'
    return short(stem, f'x {res} {m(sol)}' + (f'; {circ} circle at {m(sol)}, arrow to the {dirn}' if slot.d >= 2 else ''),
                 f'{m(a)}x {s} {m(rhs - b)} (M1); {"divide by a negative: reverse the sign (R1); " if a < 0 else ""}x {res} {m(sol)} (A1)' + (f'; number line {circ} circle, arrow {dirn} (C1).' if slot.d >= 2 else '.'), 3 if slot.d >= 2 else 2)


@R.add('ch05-st4', 'C3', (2, 4), 'short')
def int_solutions(rng, slot):
    lo, hi = rng.randint(-8, 3), rng.randint(4, 10)
    s1, s2 = rng.choice(['<', '≤']), rng.choice(['<', '≤'])
    a, b = rng.randint(2, 5), rng.randint(-5, 5)
    ints = [n for n in range(lo - 1, hi + 2) if (n > lo if s1 == '<' else n >= lo) and (n < hi if s2 == '<' else n <= hi)]
    if slot.d >= 3:
        L, H = a * lo + b, a * hi + b
        return short(f'Find all the integers n that satisfy {m(L)} {s1} {lin(a, b, "n")} {s2} {m(H)}.', ', '.join(m(t) for t in ints),
                     f'Subtract {m(b)} and divide by {a} throughout: {m(lo)} {s1} n {s2} {m(hi)} (M1 A1); integers {", ".join(m(t) for t in ints)} (A1).', 3)
    return short(f'List the integers that satisfy {m(lo)} {s1} n {s2} {m(hi)}.', ', '.join(m(t) for t in ints),
                 f'{"Exclude" if s1 == "<" else "Include"} {m(lo)}, {"exclude" if s2 == "<" else "include"} {hi} (M1); {", ".join(m(t) for t in ints)} (A1).', 2)


@R.add('ch05-st4', 'C1', (1, 3), 'mcq')
def numline_mcq(rng, slot):
    v = rng.randint(-5, 8)
    s = _ineq(rng)
    circ = 'closed' if s in '≤≥' else 'open'
    dirn = 'right' if s in '>≥' else 'left'
    others = [t for t in ['<', '>', '≤', '≥'] if t != s]
    return mcq(rng, f'A number line shows a{"n" if circ == "open" else ""} {circ} circle at {m(v)} with an arrow pointing to the {dirn}. Which inequality does it show?', f'x {s} {m(v)}',
               [f'x {t} {m(v)}' for t in others], f'{circ.capitalize()} circle → {"included" if circ == "closed" else "not included"}; arrow {dirn} → {"greater" if dirn == "right" else "less"}.')


@R.add('ch05-st4', 'C2', (2, 4), 'explain')
def ineq_flip_explain(rng, slot):
    a = rng.randint(2, 6)
    c = rng.randint(1, 15)
    who = name(rng)
    t = rng.randint(1, 6)
    return explain(f'{who} solves {c} − {a}x > {m(c - a * t)} and writes x > {t}. Test the value x = {t + 1} to show that this is wrong, and explain the correct solution.',
                   f'At x = {t + 1}: {c} − {a * (t + 1)} = {m(c - a * (t + 1))}, which is not > {m(c - a * t)}. Correct: −{a}x > −{a * t}, dividing by −{a} reverses the sign, x < {t}.',
                   'Test value shows the claim fails (M1); reversal of the inequality sign explained (R1); x < ' + f'{t} (A1).', 3, 'G2')


@R.add('ch05-st4', 'C4', (3, 5), 'multi_step')
def ineq_context(rng, slot):
    city, country, cur, cname = place(rng)
    who = name(rng)
    budget = rng.randint(40, 120)
    fee, per = rng.randint(5, 15), rng.randint(3, 9)
    maxn = (budget - fee) // per
    cap, bag = rng.randint(400, 900), rng.randint(15, 30)
    lift = rng.randint(60, 90)
    frames = [
        (f'{who} has {cur}{budget} to spend at a fair in {city}. Entry is {cur}{fee} and each ride costs {cur}{per}. (a) Write an inequality for the number of rides r. (b) Solve it. (c) What is the greatest number of rides, and how much money is left over?',
         f'(a) {fee} + {per}r ≤ {budget} (b) r ≤ {fx(Fr(budget - fee, per))} (c) {maxn} rides, {cur}{budget - fee - per * maxn} left'),
        (f'A lift in a {city} office block has a safe load of {cap} kg. A worker of mass {lift} kg is moving boxes of {bag} kg each. (a) Write an inequality for the number of boxes b the worker can take in one trip. (b) Solve it and show the solution set on a number line. (c) Find the least number of trips to move 60 boxes.',
         f'(a) {lift} + {bag}b ≤ {cap} (b) b ≤ {fx(Fr(cap - lift, bag))}, so b ∈ {{0, 1, …, {(cap - lift) // bag}}} (whole numbers only) (c) {math.ceil(60 / ((cap - lift) // bag))} trips'),
    ]
    q_, ans = rng.choice(frames)
    if (cap - lift) // bag < 1:
        return None
    return short(q_, ans, f'{ans}. Inequality formed (M1 A1); solved (A1); integer answer interpreted in context (R1); number line/notation correct (C1).', 5, 'multi_step', 'G5')


# =============================================================================================
# ch06 Sequences, Coordinates and Straight-Line Graphs
# =============================================================================================
R.facts('ch06-st1', F(
    terms=[('sequence', 'an ordered list of numbers that follow a rule'),
           ('term-to-term rule', 'the rule that tells you how to get from one term of a sequence to the next'),
           ('nth term', 'a formula in n that gives any term of a sequence directly from its position n'),
           ('common difference', 'the constant amount added each time in a linear (arithmetic) sequence')],
    facts=[('What is the nth term of 5, 8, 11, 14, …?', '3n + 2', ['n + 3', '3n + 5', '5n + 3'], 'Difference 3, so 3n; 3(1) + 2 = 5.'),
           ('What is the 10th term of the sequence with nth term 4n − 7?', '33', ['47', '37', '−3'], '4(10) − 7 = 33.'),
           ('Which sequence is linear?', '17, 13, 9, 5, …', ['1, 4, 9, 16, …', '2, 4, 8, 16, …', '1, 1, 2, 3, 5, …'], 'It has a constant difference of −4.')],
    why=[('Explain why the nth term of a linear sequence with common difference d starts with dn.', 'Each step adds d, so the terms go up in the same way as the d-times table, dn; the constant adjusts for the starting value.'),
         ('Explain why an nth term rule is more useful than a term-to-term rule for finding the 100th term.', 'The nth term gives the 100th term directly by substituting n = 100, without working out the 99 terms before it.'),
         ('Explain how you can decide whether a number is a term of a linear sequence.', 'Set the nth term equal to the number and solve for n; it is a term only if n is a positive whole number.')],
    misc=[('The nth term of 4, 7, 10, 13, … is n + 3 because you add 3 each time.', 'Adding 3 each time gives 3n; 3(1) + 1 = 4, so the nth term is 3n + 1.'),
          ('The sequence 2, 6, 18, 54 is linear because it goes up each time.', 'The differences 4, 12, 36 are not constant (each term is multiplied by 3), so it is not linear.')],
))


@R.add('ch06-st1', 'C3', (1, 4), 'short')
def nth_term(rng, slot):
    d = rng.choice([i for i in range(-7, 10) if i not in (0, 1)])
    a1 = rng.randint(-10, 20)
    c = a1 - d
    terms = [a1 + d * k for k in range(5)]
    seq = ', '.join(m(t) for t in terms[:4]) + ', …'
    rule = lin(d, c, 'n')
    if slot.d <= 2:
        return short(f'Find the nth term of the sequence {seq}', rule, f'Common difference {m(d)} → {m(d)}n (M1); adjust: {rule} (A1).', 2)
    N = rng.randint(20, 100)
    return short(f'For the sequence {seq} find (a) the nth term, (b) the {ordinal(N)} term.', f'(a) {rule} (b) {m(d * N + c)}',
                 f'(a) {rule} (M1 A1); (b) {m(d)}({N}){sgn(c)} = {m(d * N + c)} (A1).', 3)


@R.add('ch06-st1', 'C3', (2, 4), 'short')
def is_term(rng, slot):
    d = rng.randint(2, 9)
    c = rng.randint(-6, 10)
    target = rng.randint(50, 300)
    n_ = Fr(target - c, d)
    seq = ', '.join(m(d * k + c) for k in range(1, 5)) + ', …'
    ok = n_.denominator == 1 and n_ > 0
    return short(f'Is {target} a term of the sequence {seq}? Show how you decide.', f'{"Yes" if ok else "No"}: {lin(d, c, "n")} = {target} gives n = {g(float(n_), 4)}{"" if ok else ", not a whole number"}',
                 f'nth term {lin(d, c, "n")} (A1); solve {lin(d, c, "n")} = {target} (M1); conclusion with reason (R1).', 3)


@R.add('ch06-st1', 'C1', (1, 3), 'mcq')
def nth_mcq(rng, slot):
    d = rng.randint(2, 9)
    c = rng.randint(-8, 8)
    seq = ', '.join(m(d * k + c) for k in range(1, 5))
    corr = lin(d, c, 'n')
    w = [lin(1, d, 'n') if lin(1, d, 'n') != corr else lin(d, c + 1, 'n'), lin(d, d * 1 + c, 'n'), lin(d * 1 + c, d, 'n') if d + c != d else lin(d, c - 1, 'n')]
    return mcq(rng, f'What is the nth term of {seq}, …?', corr, w, f'Difference {d} → {d}n; first term {d + c} = {d}(1){sgn(c)}.')


@R.add('ch06-st1', 'C2', (2, 4), 'explain')
def seq_explain(rng, slot):
    d, c = rng.randint(2, 7), rng.randint(1, 9)
    who = name(rng)
    seq = ', '.join(str(d * k + c) for k in range(1, 5))
    kind = rng.choice(['wrong', 'parity'])
    if kind == 'wrong':
        return explain(f'{who} says the nth term of {seq}, … is n + {d}. Explain why this is wrong and find the correct nth term.',
                       f'n + {d} gives {1 + d}, {2 + d}, … which go up by 1, not {d}; correct nth term {d}n + {c}.',
                       f'Test of n = 2 or the difference shows the error (R1); {d}n + {c} (A1).', 2, 'G2')
    dd = 2 * rng.randint(1, 4)
    seq2 = ', '.join(str(dd * k + 1) for k in range(1, 5))
    return explain(f'Explain why every term of the sequence {seq2}, … is odd.', f'nth term {dd}n + 1 = 2({dd // 2}n) + 1: one more than an even number, so always odd.',
                   f'nth term {dd}n + 1 found (A1); written as 2k + 1 with reason (R1).', 2)


@R.add('ch06-st1', 'C4', (3, 5), 'multi_step')
def seq_pattern(rng, slot):
    k = rng.randint(2, 5)
    c = rng.randint(1, 6)
    N = rng.randint(15, 50)
    city, country, cur, cname = place(rng)
    s0, inc = rng.randint(20, 80), rng.randint(3, 12)
    frames = [
        (f'Square tiles are arranged in patterns: pattern 1 has {k + c} tiles, pattern 2 has {2 * k + c}, pattern 3 has {3 * k + c}. (a) Find a formula for the number of tiles in pattern n. (b) How many tiles are in pattern {N}? (c) Which pattern uses exactly {k * (N + 7) + c} tiles? (d) Explain why no pattern uses {k * N + c + 1} tiles.',
         f'(a) {k}n + {c} (b) {k * N + c} (c) pattern {N + 7} (d) {k}n + {c} = {k * N + c + 1} gives n = {N} + 1/{k}, not a whole number'),
        ('SAVINGS', None),
    ]
    q_, ans = rng.choice(frames)
    if ans is None:
        q_ = f'{name(rng)} has {cur}{s0} saved after week 1 and adds {cur}{inc} every week, so the totals form the sequence {s0}, {s0 + inc}, {s0 + 2 * inc}, … (a) Find the nth term. (b) Find the total after {N} weeks. (c) In which week does the total first exceed {cur}{s0 + inc * N + 100}? (d) Explain why this is a linear sequence.'
        lim = s0 + inc * N + 100
        wk = next(n for n in range(1, 1000) if inc * n + s0 - inc > lim)
        ans = f'(a) {inc}n + {s0 - inc} (b) {cur}{inc * N + s0 - inc} (c) week {wk} (d) the same amount {cur}{inc} is added each week (constant difference)'
    return short(q_, ans, f'{ans}. Pattern described and generalised (B: M1 A1); rule used for a far term and inverted (A1 A1); justification (R1 C1).', 6, 'multi_step', 'G5')


R.facts('ch06-st2', F(
    terms=[('coordinates', 'an ordered pair (x, y) giving the position of a point: x horizontally from the origin, then y vertically'),
           ('quadrant', 'one of the four regions into which the x- and y-axes divide the coordinate plane'),
           ('origin', 'the point (0, 0) where the axes cross'),
           ('table of values', 'a table of chosen x-values and the matching y-values calculated from a rule, used to plot a graph')],
    facts=[('In which quadrant is the point (−3, 5)?', 'second', ['first', 'third', 'fourth'], 'x negative, y positive: top left, the second quadrant.'),
           ('Which point lies on the y-axis?', '(0, −4)', ['(−4, 0)', '(4, 4)', '(−4, −4)'], 'Points on the y-axis have x = 0.'),
           ('Which point lies on y = 2x − 1?', '(3, 5)', ['(5, 3)', '(2, 4)', '(0, 1)'], '2(3) − 1 = 5.')],
    why=[('Explain why (2, 5) and (5, 2) are different points.', 'Coordinates are ordered: the first number is the horizontal position and the second the vertical, so (2, 5) is 2 across and 5 up, but (5, 2) is 5 across and 2 up.'),
         ('Explain how to decide whether a point lies on a line given by an equation.', 'Substitute the x-coordinate into the equation; if the result equals the y-coordinate the point lies on the line.'),
         ('Explain why every point on the x-axis has y-coordinate 0.', 'The x-axis is the horizontal line through the origin; moving along it changes x but there is no vertical movement, so y = 0.')],
    misc=[('The point (−2, −3) is in the second quadrant.', 'Both coordinates are negative, so it is in the third quadrant (bottom left).'),
          ('To plot (4, −1), go 4 up and 1 left.', 'The x-coordinate comes first: 4 right, then 1 down.')],
))


@R.add('ch06-st2', 'C3', (1, 3), 'short')
def table_values(rng, slot):
    a = rng.choice([i for i in range(-4, 5) if i != 0])
    b = rng.randint(-6, 6)
    xs = list(range(-2, 3)) if slot.d <= 2 else [-3, -1, 0, 2, 4]
    ys = [a * t + b for t in xs]
    if slot.d >= 3 and rng.random() < 0.5:
        ys = [t * t + b for t in xs]
        rule = f'y = x²{sgn(b) if b else ""}'
    else:
        rule = f'y = {lin(a, b)}'
    return short(f'Complete a table of values for {rule} for x = {", ".join(m(t) for t in xs)}, and write the coordinates of the points to plot.', ', '.join(f'({m(p)}, {m(q)})' for p, q in zip(xs, ys)),
                 f'Each y found by substitution (M1); all correct (A1 A1).', 3)


@R.add('ch06-st2', 'C3', (1, 4), 'short')
def shape_coords(rng, slot):
    x1, y1 = rng.randint(-6, 1), rng.randint(-6, 1)
    w, h = rng.randint(2, 7), rng.randint(2, 7)
    kind = rng.choice(['rect', 'mid', 'para'])
    if kind == 'rect':
        return short(f'Three corners of a rectangle are ({m(x1)}, {m(y1)}), ({m(x1 + w)}, {m(y1)}) and ({m(x1 + w)}, {m(y1 + h)}). Find the fourth corner and the area of the rectangle.',
                     f'({m(x1)}, {m(y1 + h)}); {w * h} square units', f'Fourth vertex (A1); sides {w} and {h} (M1); area {w * h} (A1).', 3)
    if kind == 'mid':
        x2, y2 = x1 + 2 * rng.randint(1, 5), y1 + 2 * rng.randint(1, 5)
        return short(f'Find the coordinates of the midpoint of the line segment joining ({m(x1)}, {m(y1)}) and ({m(x2)}, {m(y2)}).', f'({m((x1 + x2) // 2)}, {m((y1 + y2) // 2)})',
                     'Mean of the x-coordinates and of the y-coordinates (M1); answer (A1).', 2)
    s = rng.randint(1, 4)
    return short(f'A parallelogram has vertices A({m(x1)}, {m(y1)}), B({m(x1 + w)}, {m(y1)}) and C({m(x1 + w + s)}, {m(y1 + h)}). Find D so that ABCD is a parallelogram, and state the quadrant(s) in which A lies.',
                 f'D({m(x1 + s)}, {m(y1 + h)}); A is ' + ({(True, True): 'in the first quadrant', (False, True): 'in the second quadrant', (False, False): 'in the third quadrant', (True, False): 'in the fourth quadrant'}[(x1 > 0, y1 > 0)] if x1 and y1 else 'on an axis, so in no quadrant'), f'Translation from B to C applied to A (M1); D({m(x1 + s)}, {m(y1 + h)}) (A1); quadrant of A stated from signs (A1).', 3)


@R.add('ch06-st2', 'C1', (1, 3), 'mcq')
def quadrant_mcq(rng, slot):
    p, q = rng.choice([-1, 1]) * rng.randint(1, 9), rng.choice([-1, 1]) * rng.randint(1, 9)
    quad = {(1, 1): 'first', (-1, 1): 'second', (-1, -1): 'third', (1, -1): 'fourth'}[(1 if p > 0 else -1, 1 if q > 0 else -1)]
    return mcq(rng, f'In which quadrant does the point ({m(p)}, {m(q)}) lie?', quad, [t for t in ['first', 'second', 'third', 'fourth'] if t != quad],
               f'x is {"positive" if p > 0 else "negative"} and y is {"positive" if q > 0 else "negative"}.')


@R.add('ch06-st2', 'C2', (2, 4), 'explain')
def on_line_explain(rng, slot):
    a, b = rng.randint(-4, 5), rng.randint(-6, 6)
    if a == 0:
        a = 2
    px = rng.randint(-4, 5)
    py = a * px + b + rng.choice([0, 0, 1, -2])
    on = py == a * px + b
    return explain(f'Explain, without drawing, whether the point ({m(px)}, {m(py)}) lies on the line y = {lin(a, b)}.', f'{"Yes" if on else "No"}: when x = {m(px)}, y = {m(a * px + b)}{"" if on else f", not {m(py)}"}.',
                   'Substitute the x-coordinate (M1); compare with the y-coordinate and conclude (R1).', 2)


@R.add('ch06-st2', 'C4', (3, 5), 'multi_step')
def coord_task(rng, slot):
    a, b = rng.randint(1, 4), rng.randint(-3, 5)
    city = rng.choice(CITIES)
    k = rng.randint(2, 5)
    frames = [
        (f'A map of a park in {city} uses a grid in kilometres. The café is at (−{k}, 2), the lake at (3, 2) and the gate at (3, −{k + 1}). (a) Describe the route café → lake → gate in terms of distances and directions. (b) Find the total distance walked. (c) Find the coordinates of a bench exactly halfway between the café and the gate.',
         f'(a) {3 + k} km east, then {k + 3} km south (b) {2 * (k + 3)} km (c) ({fr(Fr(3 - k, 2))}, {fr(Fr(2 - k - 1, 2))})'),
        (f'Investigate the points where x + y = {k + 3} for whole numbers x, y ≥ 0. (a) List all such points. (b) Describe what you notice when you plot them. (c) How many such points are there for x + y = n?',
         f'(a) {", ".join(f"({t}, {k + 3 - t})" for t in range(k + 4))} (b) they lie on a straight line with gradient −1 (c) n + 1 points'),
        (f'Complete a table of values for y = {a}x{sgn(b)} for x = −2 to 3. (a) Plot the graph and state where it crosses the y-axis. (b) Find the value of x when y = {a * 5 + b}. (c) Explain how the table shows that the points lie on a straight line.',
         f'(a) y-values {", ".join(m(a * t + b) for t in range(-2, 4))}; crosses the y-axis at (0, {m(b)}) (b) x = 5 (c) y increases by {a} for every increase of 1 in x (constant difference)'),
    ]
    q_, ans = rng.choice(frames)
    return short(q_, ans, f'{ans}. Coordinates and table used correctly (M1 A1); calculation (A1); pattern or feature described with correct notation (B/C: R1 C1).', 5, 'multi_step', 'G5')


R.facts('ch06-st3', F(
    terms=[('gradient', 'a measure of the steepness of a line: the change in y divided by the change in x'),
           ('y-intercept', 'the point where a line crosses the y-axis; c in y = mx + c'),
           ('parallel lines', 'lines that never meet and so have equal gradients')],
    facts=[('What is the gradient of y = 5 − 3x?', '−3', ['5', '3', '−5'], 'Rewrite as y = −3x + 5: m = −3.'),
           ('What is the y-intercept of y = 4x − 7?', '(0, −7)', ['(0, 4)', '(−7, 0)', '(7, 0)'], 'c = −7.'),
           ('Which line is parallel to y = 2x + 1?', 'y = 2x − 6', ['y = −2x + 1', 'y = x + 2', 'y = ½x + 1'], 'Parallel lines have the same gradient, 2.')],
    why=[('Explain what a negative gradient tells you about a straight line.', 'As x increases, y decreases: the line slopes down from left to right.'),
         ('Explain why the line y = 3 has gradient 0.', 'y stays 3 for every x, so the change in y is 0 and the gradient 0 ÷ (change in x) = 0; the line is horizontal.'),
         ('Explain how to find the gradient from two points on a line.', 'Divide the change in y-coordinates by the change in x-coordinates (rise ÷ run), subtracting in the same order.')],
    misc=[('The gradient of the line through (1, 2) and (3, 8) is 2/6.', 'Gradient = change in y ÷ change in x = 6/2 = 3.'),
          ('In y = 4 + 2x the gradient is 4.', 'The gradient is the coefficient of x: 2; 4 is the y-intercept.')],
))


@R.add('ch06-st3', 'C3', (1, 4), 'short')
def grad_two_pts(rng, slot):
    x1, y1 = rng.randint(-6, 5), rng.randint(-6, 5)
    dx = rng.choice([i for i in range(-6, 7) if i != 0])
    mm = Fr(rng.randint(-8, 8), rng.choice([1, 1, 2, 3]))
    dy = mm * dx
    if dy.denominator != 1:
        return None
    x2, y2 = x1 + dx, y1 + int(dy)
    grad = Fr(y2 - y1, x2 - x1)
    if slot.d <= 2:
        return short(f'Find the gradient of the line through ({m(x1)}, {m(y1)}) and ({m(x2)}, {m(y2)}).', fx(grad),
                     f'({m(y2)} − {m(y1) if y1 >= 0 else f"({m(y1)})"}) ÷ ({m(x2)} − {m(x1) if x1 >= 0 else f"({m(x1)})"}) (M1) = {fx(grad)} (A1).', 2)
    c = y1 - grad * x1
    return short(f'Find the equation of the line through ({m(x1)}, {m(y1)}) and ({m(x2)}, {m(y2)}) in the form y = mx + c.', f'y = {_mxc(grad, c)}',
                 f'Gradient {fx(grad)} (M1 A1); substitute a point to find c = {fx(c)} (M1); y = {_mxc(grad, c)} (A1).', 4)


def _mxc(mm, c):
    mm, c = Fr(mm), Fr(c)
    if mm == 0:
        return fx(c)
    mt = '' if mm == 1 else '−' if mm == -1 else fx(mm)
    s = f'{mt}x'
    if c > 0:
        s += f' + {fx(c)}'
    elif c < 0:
        s += f' − {fx(-c)}'
    return s


@R.add('ch06-st3', 'C3', (1, 3), 'short')
def read_mc(rng, slot):
    mm, c = rng.choice([i for i in range(-6, 7) if i != 0]), rng.randint(-9, 9)
    forms = [
        (f'y = {_mxc(mm, c)}', mm, c),
        (f'y = {m(c)} {"+" if mm > 0 else "−"} {abs(mm) if abs(mm) != 1 else ""}x', mm, c),
        (f'2y = {_mxc(2 * mm, 2 * c)}', mm, c),
        (f'y − {_mxc(mm, 0)} = {m(c)}'.replace('− −', '+ '), mm, c),
    ]
    e, a, b = rng.choice(forms[:2] if slot.d <= 1 else forms)
    return short(f'State the gradient and the y-intercept of the line {e}.', f'gradient {m(a)}, y-intercept (0, {m(b)})',
                 f'Rearrange to y = mx + c if needed (M1); gradient {m(a)} (A1); intercept (0, {m(b)}) (A1).', 2 if slot.d <= 1 else 3)


@R.add('ch06-st3', 'C1', (1, 3), 'mcq')
def grad_mcq(rng, slot):
    mm, c = rng.choice([i for i in range(-5, 6) if i not in (0, 1, -1)]), rng.randint(-8, 8)
    corr = f'y = {_mxc(mm, c)}'
    w = [f'y = {_mxc(c if c not in (0, mm) else mm + 1, mm)}', f'y = {_mxc(-mm, c)}', f'y = {_mxc(mm, -c if c else c + 2)}']
    return mcq(rng, f'Which line has gradient {m(mm)} and passes through (0, {m(c)})?', corr, w, f'y = mx + c with m = {m(mm)} and c = {m(c)}.')


@R.add('ch06-st3', 'C2', (2, 4), 'explain')
def grad_explain(rng, slot):
    m1, m2 = rng.sample([i for i in range(-5, 6) if i != 0], 2)
    c1, c2 = rng.randint(-5, 5), rng.randint(-5, 5)
    kind = rng.choice(['steeper', 'parallel', 'pattern'])
    if kind == 'steeper':
        st = f'y = {_mxc(m1, c1)}' if abs(m1) > abs(m2) else f'y = {_mxc(m2, c2)}'
        if abs(m1) == abs(m2):
            return None
        return explain(f'Explain which line is steeper, y = {_mxc(m1, c1)} or y = {_mxc(m2, c2)}, and describe the direction of each.',
                       f'{st} is steeper (larger |gradient|); y = {_mxc(m1, c1)} slopes {"up" if m1 > 0 else "down"} and y = {_mxc(m2, c2)} slopes {"up" if m2 > 0 else "down"} from left to right.',
                       'Steepness from the size of the gradient (R1); direction from the sign (R1).', 2)
    if kind == 'parallel':
        return explain(f'Explain why the lines y = {_mxc(m1, c1)} and y = {_mxc(m1, c1 + 3)} never meet.', f'Both have gradient {m(m1)} but different intercepts, so they are parallel and distinct.',
                       'Equal gradients (R1); different intercepts ⇒ no intersection (R1).', 2)
    c1 = abs(c1) or 4
    return explain(f'Using a graphing tool, {name(rng)} draws y = x + {c1}, y = 2x + {c1}, y = 3x + {c1}. Describe what is the same and what changes, and explain why.',
                   f'All pass through (0, {c1}) because c = {c1}; they get steeper as the gradient m increases.',
                   'Common intercept (B1); effect of m (B1); link to y = mx + c (R1).', 3)


@R.add('ch06-st3', 'C4', (3, 5), 'multi_step')
def line_task(rng, slot):
    p, q = rng.randint(1, 5), rng.randint(-4, 6)
    x1, x2 = rng.randint(-3, 0), rng.randint(2, 6)
    y1, y2 = p * x1 + q, p * x2 + q
    k = rng.randint(2, 5)
    frames = [
        (f'Points A({m(x1)}, {m(y1)}) and B({m(x2)}, {m(y2)}) lie on a straight line. (a) Find the gradient of AB. (b) Find the equation of the line. (c) Determine whether C({x2 + k}, {m(y2 + p * k + 1)}) lies on the line. (d) Write the equation of the parallel line through the origin.',
         f'(a) {p} (b) y = {_mxc(p, q)} (c) no: at x = {x2 + k}, y = {m(y2 + p * k)} (d) y = {_mxc(p, 0)}'),
        (f'Investigate the family of lines y = mx{sgn(q)}. (a) For m = 1, 2 and 3 find where each line crosses the x-axis. (b) Describe the pattern. (c) Find, in terms of m, where y = mx{sgn(q)} crosses the x-axis.',
         f'(a) x = {fx(Fr(-q, 1))}, {fx(Fr(-q, 2))}, {fx(Fr(-q, 3))} (b) the x-intercept moves towards 0 as m increases (c) x = {m(-q)}/m' if q else None),
    ]
    q_, ans = rng.choice(frames)
    if ans is None:
        return None
    return short(q_, ans, f'{ans}. Gradient and equation found (M1 A1); point tested or pattern generalised (B: M1 A1); clear notation (C1).', 5, 'multi_step', 'G5')


R.facts('ch06-st4', F(
    terms=[('conversion graph', 'a straight-line graph used to change between two units, such as currencies or temperature scales'),
           ('distance–time graph', 'a graph of distance from a starting point against time; its gradient is the speed'),
           ('speed', 'the rate at which distance changes with time: distance ÷ time')],
    facts=[('On a distance–time graph, what does a horizontal line segment show?', 'the object is stationary', ['the object is moving at constant speed', 'the object is accelerating', 'the object is returning'], 'Distance is not changing.'),
           ('On a distance–time graph, the gradient represents:', 'speed', ['distance', 'time', 'acceleration'], 'Gradient = distance ÷ time.'),
           ('A currency conversion graph passes through (0, 0) and (50, 65). How much is 20 in the second currency?', '26', ['13', '30', '32.5'], 'Rate 1.3: 20 × 1.3 = 26.')],
    why=[('Explain why a currency conversion graph passes through the origin.', 'Zero of one currency is worth zero of the other, and the amounts are in direct proportion.'),
         ('Explain why a steeper section of a distance–time graph means a higher speed.', 'A steeper line covers more distance in the same time, and speed is distance ÷ time.'),
         ('Explain what a line sloping down towards the time axis means on a distance–time graph.', 'The distance from the start is decreasing: the object is travelling back towards the starting point.')],
    misc=[('On a distance–time graph, a line going down means the object is slowing down.', 'It means the object is moving back towards the start; speed is shown by the steepness.'),
          ('A taxi fare graph that starts at 3 on the cost axis shows direct proportion.', 'It does not pass through the origin, so cost is not directly proportional to distance (there is a fixed charge).')],
))


@R.add('ch06-st4', 'C3', (1, 4), 'short')
def dt_graph(rng, slot):
    who = name(rng)
    city = rng.choice(CITIES)
    d1, t1 = rng.randint(2, 12), rng.choice([15, 20, 30, 40, 45, 60])
    rest = rng.choice([10, 15, 20, 30])
    t3 = rng.choice([20, 30, 40, 60])
    s1 = Fr(d1 * 60, t1)
    s3 = Fr(d1 * 60, t3)
    return short(f'{who} cycles from home in {city} to a park {d1} km away in {t1} minutes, rests for {rest} minutes, then returns home in {t3} minutes. (a) Describe the distance–time graph. (b) Find the speed on each moving section in km/h. (c) Find the average speed for the whole trip including the rest.',
                 f'(a) straight line up to ({t1}, {d1}), horizontal for {rest} min, straight line down to ({t1 + rest + t3}, 0) (b) {g(float(s1), 4)} km/h out, {g(float(s3), 4)} km/h back (c) {g(float(Fr(2 * d1 * 60, t1 + rest + t3)), 3)} km/h',
                 f'Graph features described (C1); speeds = distance ÷ time in hours (M1 A1 A1); total distance {2 * d1} km ÷ {t1 + rest + t3} min (M1 A1).', 6 if slot.d >= 3 else 4)


@R.add('ch06-st4', 'C3', (1, 3), 'short')
def conversion(rng, slot):
    pairs = [('kilometres', 'miles', 0.621371, 'km', 'mi'), ('kilograms', 'pounds (lb)', 2.20462, 'kg', 'lb'), ('litres', 'US gallons', 0.264172, 'L', 'gal')]
    a, b, k, ua, ub = rng.choice(pairs)
    v = rng.choice([10, 20, 25, 40, 50, 80, 100])
    if rng.random() < 0.5:
        cname, lo_, hi_ = rng.choice([('Singapore dollars', 140, 150), ('Canadian dollars', 145, 155), ('Australian dollars', 160, 172), ('Swiss francs', 92, 97), ('US dollars', 105, 115)])
        rate = Decimal(rng.randint(lo_, hi_)) / 100
        amt = rng.choice([20, 40, 50, 75, 120])
        return short(f'A conversion graph passes through (0, 0) and (100, {g(float(rate * 100), 4)}) for euros (x) and {cname} (y). Use it to convert {amt} euros to {cname}, and {g(float(rate * 200), 4)} {cname} to euros.', f'{g(float(rate * amt), 5)} {cname}; 200 euros',
                     f'Rate {rate} {cname} per euro (M1); {amt} × {rate} = {g(float(rate * amt), 5)} (A1); {g(float(rate * 200), 4)} ÷ {rate} = 200 (A1).', 3)
    return short(f'A straight-line conversion graph shows that 100 {ua} = {100 * k:.1f} {ub}. Use it to convert {v} {ua} to {ub}, giving your answer to 1 d.p.', f'{v * k:.1f} {ub}',
                 f'Read or scale: {v}/100 × {100 * k:.1f} (M1) = {v * k:.1f} {ub} (A1).', 2)


@R.add('ch06-st4', 'C1', (1, 3), 'mcq')
def dt_mcq(rng, slot):
    d, t = rng.randint(3, 30), rng.choice([2, 3, 4, 5, 6])
    sp_ = Fr(d * 10, t)
    return mcq(rng, f'A distance–time graph is a straight line from (0, 0) to ({t} h, {d * 10} km). What is the speed?', f'{g(float(sp_), 4)} km/h',
               [f'{d * 10 * t} km/h', f'{g(float(Fr(t, d * 10)), 3)} km/h', f'{d * 10 + t} km/h'], f'Gradient = {d * 10} ÷ {t} = {g(float(sp_), 4)} km/h.')


@R.add('ch06-st4', 'C2', (2, 4), 'explain')
def graph_story(rng, slot):
    who = name(rng)
    fix_, per = rng.randint(2, 6), Decimal(rng.randint(80, 250)) / 100
    kind = rng.choice(['taxi', 'story'])
    if kind == 'taxi':
        return explain(f'A graph of taxi fare against distance is a straight line starting at ({0}, {fix_}) with gradient {per}. Explain what the intercept and the gradient mean, and why fare is not directly proportional to distance.',
                       f'{fix_} is the fixed starting charge; {per} is the cost per km. Because the line does not pass through the origin, doubling the distance does not double the fare.',
                       'Intercept interpreted (R1); gradient interpreted (R1); proportion argument (R1).', 3)
    return explain(f'{who}’s distance–time graph has three sections: steep upward, then horizontal, then less steep upward. Write a short story that matches the graph and explain how you used the gradients.',
                   'E.g. runs quickly to a bus stop, waits, then walks the rest of the way more slowly; steep = fast, horizontal = stopped, less steep = slower.',
                   'Each section matched to a plausible motion (A1 A1); gradient ↔ speed explained (R1).', 3)


@R.add('ch06-st4', 'C4', (3, 5), 'multi_step')
def graph_compare(rng, slot):
    city, country, cur, cname = place(rng)
    a_fix, a_per = rng.randint(1, 5), Decimal(rng.randint(150, 300)) / 100
    b_fix, b_per = a_fix + rng.randint(3, 10), a_per - Decimal(rng.randint(30, 100)) / 100
    if b_per <= 0:
        return None
    be = (b_fix - a_fix) / (a_per - b_per)
    who, who2 = two_names(rng)
    v1, v2 = rng.randint(8, 16), rng.randint(14, 24)
    head = rng.choice([10, 15, 20, 30])
    tm = Fr(v1 * head, v2 - v1) if v2 > v1 else None
    frames = [
        (f'Two bike-hire companies in {city}: Company A charges {cur}{a_fix} plus {cur}{a_per} per km; Company B charges {cur}{b_fix} plus {cur}{b_per} per km. (a) Write an equation for each and describe their graphs. (b) Find the distance at which the costs are equal. (c) Advise a rider making a {int(be) + 5} km trip.',
         f'(a) A: C = {a_fix} + {a_per}d, B: C = {b_fix} + {b_per}d – straight lines, B steeper at first? no: A has the greater gradient, B the greater intercept (b) d = {be:.2f} km (c) B is cheaper for trips longer than {be:.2f} km, so choose B'),
        (f'{who} leaves {city} at 09:00 on a bike at {v1} km/h. {who2} leaves the same place {head} minutes later at {v2} km/h along the same road. (a) Sketch both distance–time graphs on the same axes. (b) At what time does {who2} catch up? (c) How far from {city} are they then?',
         None),
    ]
    q_, ans = rng.choice(frames)
    if ans is None:
        if tm is None:
            return None
        catch = Fr(head, 60) + Fr(tm, 60)
        mins = math.floor(catch * 60 + Fr(1, 2))
        ans = f'(a) two straight lines from the time axis, {who2}’s steeper and starting at 09:{head:02d} (b) {9 + mins // 60:02d}:{mins % 60:02d} (c) {g(float(v1 * catch), 4)} km'
    else:
        ans = ans.replace(' B steeper at first? no:', '')
    return short(q_, ans, f'{ans}. Linear models/graphs set up (M1 A1); intersection found algebraically or graphically (M1 A1); interpretation in context (D: R1).', 5, 'multi_step', 'G5')


# =============================================================================================
# ch07 Angles, Triangles and Polygons
# =============================================================================================
R.facts('ch07-st1', F(
    terms=[('angles on a straight line', 'angles that meet at a point on a straight line and add up to 180°'),
           ('angles at a point', 'angles that together make a full turn around a point and add up to 360°'),
           ('vertically opposite angles', 'the pairs of opposite angles formed where two straight lines cross; they are equal'),
           ('supplementary angles', 'two angles that add up to 180°'),
           ('complementary angles', 'two angles that add up to 90°')],
    facts=[('Two angles on a straight line are 3x and 2x. What is x?', '36°', ['18°', '72°', '30°'], '5x = 180°.'),
           ('Three angles at a point are 140°, 95° and y. What is y?', '125°', ['55°', '235°', '45°'], '360 − 140 − 95 = 125.'),
           ('What is the complement of 37°?', '53°', ['143°', '63°', '323°'], '90 − 37 = 53.')],
    why=[('Explain why vertically opposite angles are equal.', 'Each of the two angles forms a straight line (180°) with the same angle between them, so both equal 180° minus that angle.'),
         ('Explain why angles at a point add up to 360°.', 'Together they make one complete turn around the point, and a full turn is 360°.'),
         ('Explain why an angle and its supplement cannot both be obtuse.', 'Two obtuse angles are each more than 90°, so together they would be more than 180°; supplementary angles add to exactly 180°.')],
    misc=[('Vertically opposite angles add up to 180°.', 'Vertically opposite angles are equal; it is adjacent angles on a straight line that add up to 180°.'),
          ('Angles around a point add up to 180°.', 'They add up to 360° (a full turn); 180° is for angles on a straight line.')],
))


@R.add('ch07-st1', 'C3', (1, 3), 'short')
def angle_line_point(rng, slot):
    kind = rng.choice(['line', 'point', 'vert', 'alg'])
    if kind == 'line':
        a, b = rng.randint(20, 80), rng.randint(20, 70)
        return short(f'Three angles lie on a straight line: {a}°, {b}° and x. Find x, giving a reason.', f'x = {180 - a - b}°', f'x = 180 − {a} − {b} (M1) = {180 - a - b}° (A1); reason: angles on a straight line add to 180° (R1).', 3)
    if kind == 'point':
        a, b, c = rng.randint(60, 140), rng.randint(40, 110), rng.randint(20, 70)
        if a + b + c >= 350:
            return None
        return short(f'Four angles meet at a point: {a}°, {b}°, {c}° and y. Find y, giving a reason.', f'y = {360 - a - b - c}°', f'360 − {a} − {b} − {c} (M1) = {360 - a - b - c}° (A1); angles at a point add to 360° (R1).', 3)
    if kind == 'vert':
        a = rng.randint(25, 155)
        return short(f'Two straight lines cross. One of the angles formed is {a}°. Find the other three angles, giving reasons.', f'{a}°, {180 - a}°, {180 - a}°',
                     f'Vertically opposite {a}° (A1); adjacent angles {180 - a}° on a straight line (A1); reasons stated (R1).', 3)
    k1, k2, c = rng.randint(2, 5), rng.randint(1, 4), rng.choice([0, 10, 20, -10])
    xv = Fr(180 - c, k1 + k2)
    if xv.denominator != 1:
        return None
    return short(f'Two angles on a straight line are {k1}x° and ({lin(k2, c)})°. Find x and the size of each angle.', f'x = {xv}; {k1 * xv}° and {k2 * xv + c}°',
                 f'{k1}x + {lin(k2, c)} = 180 (M1); x = {xv} (A1); angles {k1 * xv}° and {k2 * xv + c}° (A1).', 3)


@R.add('ch07-st1', 'C1', (1, 3), 'mcq')
def comp_supp_mcq(rng, slot):
    a = rng.randint(12, 78)
    if rng.random() < 0.5:
        return mcq(rng, f'What is the supplement of {a}°?', f'{180 - a}°', [f'{90 - a}°', f'{360 - a}°', f'{a}°'], f'Supplementary angles add to 180°: 180 − {a} = {180 - a}.')
    return mcq(rng, f'What is the complement of {a}°?', f'{90 - a}°', [f'{180 - a}°', f'{360 - a}°', f'{90 + a}°'], f'Complementary angles add to 90°: 90 − {a} = {90 - a}.')


@R.add('ch07-st1', 'C2', (2, 4), 'explain')
def angle_proof1(rng, slot):
    a = rng.randint(25, 80)
    who = name(rng)
    kind = rng.choice(['prove', 'error', 'bisect'])
    if kind == 'prove':
        return explain(f'Two straight lines cross, forming angles a, b, c, d in order around the point, with a = {a}°. Prove, giving a reason for each step, that c = {a}°.',
                       f'a + b = 180° (straight line) so b = {180 - a}°; b + c = 180° (straight line) so c = 180 − {180 - a} = {a}°.',
                       'Each step with reason (R1 R1); conclusion (A1). Criterion C: logical, clearly set out.', 3)
    if kind == 'error':
        return explain(f'{who} says: "Two lines cross making an angle of {a}°, so the angle next to it is also {a}° because they are vertically opposite." Explain the mistake.',
                       f'The angle next to it is adjacent, not vertically opposite; it is 180 − {a} = {180 - a}°. The angle opposite is {a}°.',
                       'Adjacent vs vertically opposite distinguished (R1); correct value (A1).', 2, 'G2')
    return explain(f'A straight line is split into two angles by a ray, and each angle is then bisected. Explain why the angle between the two bisectors is always 90°, illustrating with one angle of {2 * a}°.',
                   f'Halves are {a}° and {90 - a}°; together half of 180° = 90°.',
                   'Halves of each angle (A1); sum is half of 180° (R1); general argument (R1).', 3)


@R.add('ch07-st1', 'C4', (3, 5), 'multi_step')
def angle_algebra(rng, slot):
    k = rng.randint(2, 6)
    c = rng.randint(5, 30)
    who = name(rng)
    frames = [
        (f'Around a point there are angles x°, {k}x°, (x + {c})° and (2x − {c // 2 * 2})°. (a) Form an equation. (b) Solve it for x. (c) Find the size of each angle and check they add to 360°.', None),
        (f'A pizza in {rng.choice(CITIES)} is cut into slices whose angles at the centre are in the ratio 1 : 2 : {k} : {k + 1}. (a) Find each angle. (b) {who} wonders whether a ratio of the form 1 : 2 : k : (k + 1), with k a whole number, can ever give a right-angled slice. Investigate and explain.',
         None),
    ]
    q_, ans = rng.choice(frames)
    if q_.startswith('Around'):
        cc = c // 2 * 2
        xv = Fr(360 - c + cc, 1 + k + 1 + 2)
        if xv.denominator != 1:
            return None
        ans = f'(a) x + {k}x + x + {c} + 2x − {cc} = 360 (b) x = {xv} (c) {xv}°, {k * xv}°, {xv + c}°, {2 * xv - cc}°'
    else:
        parts = 1 + 2 + k + k + 1
        ang = [Fr(360 * p, parts) for p in (1, 2, k, k + 1)]
        ans = f'(a) {", ".join(g(float(a_), 4) + "°" for a_ in ang)} (b) a 90° slice needs a part equal to 1/4 of the total; e.g. 2 parts out of 8 happens when k = 2.5, not a whole number, but k + 1 = (2k + 4)/4 gives k = 0 – not possible for whole k ≥ 1 except by checking each case'
        # careful check by computing cases
        poss = [kk for kk in range(1, 30) for p in (1, 2, kk, kk + 1) if Fr(360 * p, 2 * kk + 4) == 90]
        ans = f'(a) {", ".join(g(float(a_), 4) + "°" for a_ in ang)} (b) ' + (f'yes – for k = {", ".join(map(str, sorted(set(poss))))} one slice is 90°' if poss else 'no whole-number k gives a 90° slice')
    return short(q_, ans, f'{ans}. Angle fact used to form an equation (M1 A1); solved (A1); all angles found and checked (A1 C1).', 5, 'multi_step', 'G5')


R.facts('ch07-st2', F(
    terms=[('corresponding angles', 'angles in matching positions where a transversal crosses two parallel lines; they are equal (F-shape)'),
           ('alternate angles', 'angles on opposite sides of a transversal, between two parallel lines; they are equal (Z-shape)'),
           ('co-interior angles', 'angles on the same side of a transversal, between two parallel lines; they add to 180° (C-shape)'),
           ('transversal', 'a line that crosses two or more other lines')],
    facts=[('A transversal crosses two parallel lines. One alternate angle is 64°. The other is:', '64°', ['116°', '26°', '296°'], 'Alternate angles are equal.'),
           ('Co-interior angles between parallel lines are 3y and 2y. What is y?', '36°', ['18°', '72°', '45°'], '5y = 180°.'),
           ('Which angle pair is equal when lines are parallel?', 'corresponding angles', ['co-interior angles', 'adjacent angles on a line', 'complementary angles'], 'Corresponding angles are equal (F-shape).')],
    why=[('Explain why co-interior angles between parallel lines add to 180°.', 'One co-interior angle is equal to the corresponding angle of the other, which lies on a straight line with it; angles on a straight line add to 180°.'),
         ('Explain how you can use angles to test whether two lines are parallel.', 'Draw a transversal and measure; if corresponding (or alternate) angles are equal, or co-interior angles add to 180°, the lines are parallel.'),
         ('Explain why alternate angles are equal using corresponding and vertically opposite angles.', 'An alternate angle is vertically opposite to the angle that corresponds with the other, and both relationships give equality.')],
    misc=[('Co-interior angles are equal.', 'Co-interior angles add up to 180°; they are equal only if both are 90°.'),
          ('Alternate angles are always equal, even if the lines are not parallel.', 'The angle facts only hold for parallel lines; if the lines are not parallel, alternate angles differ.')],
))


@R.add('ch07-st2', 'C3', (1, 4), 'short')
def parallel_find(rng, slot):
    a = rng.randint(35, 145)
    pair = rng.choice(['corresponding', 'alternate', 'co-interior', 'vertical+alt'])
    if pair == 'corresponding':
        return short(f'A transversal crosses two parallel lines. An angle at the upper crossing is {a}°. Find the corresponding angle at the lower crossing, giving a reason.', f'{a}°', f'{a}° (A1); corresponding angles are equal (R1).', 2)
    if pair == 'alternate':
        return short(f'In a Z-shape formed by a transversal and two parallel lines, one angle is {a}°. Find the alternate angle and name the angle fact used.', f'{a}°; alternate angles are equal', f'{a}° (A1); alternate angles (R1).', 2)
    if pair == 'co-interior':
        return short(f'Two parallel lines are crossed by a transversal. Two co-interior angles are {a}° and y. Find y, giving a reason.', f'y = {180 - a}°', f'180 − {a} (M1) = {180 - a}° (A1); co-interior angles add to 180° (R1).', 3)
    return short(f'Lines AB and CD are parallel, and a transversal meets them at P and Q. Angle APQ = {a}°. Find angle PQD, explaining each step.', f'{a}°',
                 f'Angle APQ and angle PQD are alternate angles (R1), so angle PQD = {a}° (A1).', 2)


@R.add('ch07-st2', 'C3', (2, 5), 'short')
def parallel_algebra(rng, slot):
    k1, k2 = rng.randint(2, 5), rng.randint(1, 4)
    c1, c2 = rng.randint(-20, 30), rng.randint(-20, 30)
    kind = rng.choice(['equal', 'sum'])
    if kind == 'equal' and k1 != k2:
        xv = Fr(c2 - c1, k1 - k2)
        if xv.denominator != 1 or xv <= 0 or not (0 < k1 * xv + c1 < 180):
            return None
        return short(f'Two alternate angles between parallel lines are ({lin(k1, c1)})° and ({lin(k2, c2)})°. Find x and the size of the angle.', f'x = {xv}; angle {k1 * xv + c1}°',
                     f'Alternate angles are equal (R1): {lin(k1, c1)} = {lin(k2, c2)} (M1); x = {xv} (A1); angle (A1).', 4)
    xv = Fr(180 - c1 - c2, k1 + k2)
    if xv.denominator != 1 or xv <= 0 or not (0 < k1 * xv + c1 < 180 and 0 < k2 * xv + c2 < 180):
        return None
    return short(f'Two co-interior angles between parallel lines are ({lin(k1, c1)})° and ({lin(k2, c2)})°. Find x and both angles.', f'x = {xv}; {k1 * xv + c1}° and {k2 * xv + c2}°',
                 f'Co-interior angles add to 180° (R1); equation (M1); x = {xv} (A1); angles (A1).', 4)


@R.add('ch07-st2', 'C1', (1, 3), 'mcq')
def parallel_mcq(rng, slot):
    a = rng.randint(40, 140)
    kind = rng.choice(['co', 'corr', 'alt'])
    if kind == 'co':
        return mcq(rng, f'Two co-interior angles between parallel lines: one is {a}°. What is the other?', f'{180 - a}°', [f'{a}°', f'{360 - a}°', f'{abs(90 - a)}°' if abs(90 - a) not in (a, 180 - a) else f'{a + 10}°'], 'Co-interior angles add to 180°.')
    name_ = 'corresponding' if kind == 'corr' else 'alternate'
    return mcq(rng, f'An angle of {a}° is formed by a transversal and one of two parallel lines. What is the size of its {name_} angle?', f'{a}°', [f'{180 - a}°', f'{360 - a}°', f'{abs(90 - a) or 45}°'], f'{name_.capitalize()} angles are equal.')


@R.add('ch07-st2', 'C2', (2, 4), 'explain')
def parallel_test(rng, slot):
    a = rng.randint(50, 130)
    d_ = rng.choice([0, 0, rng.randint(1, 6)])
    b = 180 - a + d_
    return explain(f'A transversal crosses two lines. Two co-interior angles measure {a}° and {b}°. Explain whether the two lines are parallel.',
                   f'{"Yes" if d_ == 0 else "No"}: {a}° + {b}° = {a + b}°{", so co-interior angles are supplementary and the lines are parallel" if d_ == 0 else ", not 180°, so the lines are not parallel"}.',
                   'Sum computed (A1); converse of the co-interior fact applied (R1).', 2)


@R.add('ch07-st2', 'C4', (3, 5), 'multi_step')
def parallel_proof(rng, slot):
    a, b = rng.randint(30, 70), rng.randint(30, 70)
    frames = [
        (f'A triangle ABC has a line through A drawn parallel to BC. Angle ABC = {a}° and angle ACB = {b}°. (a) Use alternate angles to find the two angles the parallel line makes with AB and AC at A. (b) Hence find angle BAC. (c) Explain how this argument proves that the angles of any triangle add to 180°.',
         f'(a) {a}° and {b}° (b) {180 - a - b}° (c) the three angles at A lie on a straight line (180°) and two of them equal the base angles by alternate angles, for any triangle'),
        (f'A zig-zag path is made of segments between two parallel fences. At the first bend the path makes an angle of {a}° with the top fence, and at the second bend it makes an angle of {b}° with the bottom fence. (a) Find the angle between the two path segments at a bend that touches the bottom fence if the path then returns at {b}°. (b) Explain why the "Z" shape shows alternate angles. (c) Find the angle of the path at the top fence after returning.',
         f'(a) {180 - a - b}° (b) the segment crosses both parallel fences forming a Z, so the angle with each fence is equal on opposite sides (c) {b}°'),
    ]
    q_, ans = rng.choice(frames)
    return short(q_, ans, f'{ans}. Parallel-line angle facts named (R1 R1); angles calculated (A1 A1); general proof communicated logically (C1).', 5, 'multi_step', 'G5')


R.facts('ch07-st3', F(
    terms=[('angle sum of a triangle', 'the interior angles of any triangle add up to 180°'),
           ('angle sum of a quadrilateral', 'the interior angles of any quadrilateral add up to 360°'),
           ('isosceles triangle', 'a triangle with two equal sides and two equal base angles'),
           ('exterior angle of a triangle', 'the angle between one side and the extension of an adjacent side; it equals the sum of the two opposite interior angles')],
    facts=[('An isosceles triangle has a top angle of 40°. What is each base angle?', '70°', ['40°', '140°', '50°'], '(180 − 40) ÷ 2 = 70.'),
           ('Three angles of a quadrilateral are 85°, 110° and 95°. What is the fourth?', '70°', ['90°', '160°', '250°'], '360 − 290 = 70.'),
           ('A triangle has angles 50° and 60°. What is the exterior angle at the third vertex?', '110°', ['70°', '120°', '130°'], 'Exterior angle = sum of the opposite interior angles.')],
    why=[('Explain why the angles of a quadrilateral add up to 360°.', 'A diagonal splits the quadrilateral into two triangles, each with angle sum 180°, so the total is 2 × 180° = 360°.'),
         ('Explain why a triangle cannot have two obtuse angles.', 'Two obtuse angles would already add to more than 180°, leaving nothing for the third angle; the angle sum is exactly 180°.'),
         ('Explain why each angle of an equilateral triangle is 60°.', 'The three angles are equal (equal sides) and add to 180°, so each is 180 ÷ 3 = 60°.')],
    misc=[('The base angles of an isosceles triangle with apex 50° are 50° each.', 'The apex is the odd angle: base angles are (180 − 50)/2 = 65° each.'),
          ('The exterior angle of a triangle equals the adjacent interior angle.', 'It is supplementary to the adjacent interior angle and equals the sum of the two opposite interior angles.')],
))


@R.add('ch07-st3', 'C3', (1, 4), 'short')
def triangle_angles(rng, slot):
    kind = rng.choice(['tri', 'iso', 'ext', 'quad', 'alg'])
    if kind == 'tri':
        a, b = rng.randint(25, 90), rng.randint(20, 70)
        return short(f'A triangle has angles {a}° and {b}°. Find the third angle.', f'{180 - a - b}°', f'180 − {a} − {b} = {180 - a - b}° (A1); triangle angle sum (R1).', 2)
    if kind == 'iso':
        apex = rng.randint(10, 80) * 2
        if rng.random() < 0.5:
            return short(f'An isosceles triangle has an apex angle of {apex}°. Find each base angle.', f'{(180 - apex) // 2}°', f'(180 − {apex}) ÷ 2 (M1) = {(180 - apex) // 2}° (A1).', 2)
        base = rng.randint(30, 85)
        return short(f'An isosceles triangle has base angles of {base}° each. Find the apex angle.', f'{180 - 2 * base}°', f'180 − 2 × {base} (M1) = {180 - 2 * base}° (A1).', 2)
    if kind == 'ext':
        a, b = rng.randint(25, 80), rng.randint(25, 80)
        return short(f'In triangle PQR, angle P = {a}° and angle Q = {b}°. Side QR is extended beyond R. Find the exterior angle at R and angle PRQ.', f'exterior {a + b}°, angle PRQ = {180 - a - b}°',
                     f'Exterior angle = {a} + {b} = {a + b}° (A1 R1); interior {180 - a - b}° (A1).', 3)
    if kind == 'quad':
        a, b, c = rng.randint(60, 120), rng.randint(50, 130), rng.randint(60, 110)
        if a + b + c >= 345:
            return None
        return short(f'A quadrilateral has angles {a}°, {b}°, {c}° and d. Find d.', f'd = {360 - a - b - c}°', f'360 − {a + b + c} (M1) = {360 - a - b - c}° (A1).', 2)
    k = rng.randint(2, 4)
    c = rng.choice([10, 20, 30])
    xv = Fr(180 - c, 1 + k + 1)
    if xv.denominator != 1:
        return None
    return short(f'The angles of a triangle are x°, {k}x° and (x + {c})°. Find the largest angle.', f'{max(k * xv, xv + c)}°',
                 f'{k + 2}x + {c} = 180 (M1); x = {xv} (A1); largest angle {max(k * xv, xv + c)}° (A1).', 3)


@R.add('ch07-st3', 'C1', (1, 3), 'mcq')
def tri_type_mcq(rng, slot):
    a = rng.randint(20, 70)
    b = rng.randint(20, 160 - a)
    c = 180 - a - b
    if c <= 0:
        return None
    big = max(a, b, c)
    t = 'obtuse-angled' if big > 90 else 'right-angled' if big == 90 else 'acute-angled'
    return mcq(rng, f'A triangle has angles {a}° and {b}°. What type of triangle is it?', t, [o for o in ['obtuse-angled', 'right-angled', 'acute-angled', 'impossible – the angles are too large'] if o != t][:3],
               f'Third angle {c}°; largest angle {big}°.')


@R.add('ch07-st3', 'C2', (2, 4), 'explain')
def tri_explain(rng, slot):
    a, b = rng.randint(30, 80), rng.randint(30, 80)
    who = name(rng)
    kind = rng.choice(['ext', 'impossible', 'kite'])
    if kind == 'ext':
        return explain(f'In a triangle with interior angles {a}°, {b}° and c, show that the exterior angle next to c is equal to {a}° + {b}°. Explain why this is true for every triangle.',
                       f'c = 180 − {a} − {b} = {180 - a - b}°; exterior = 180 − c = {a + b}° = {a} + {b}. In general exterior = 180 − c = a + b because a + b + c = 180.',
                       'Numerical demonstration (A1); general argument (R1 R1).', 3)
    if kind == 'impossible':
        p, q = rng.randint(91, 120), rng.randint(70, 100)
        return explain(f'{who} says a triangle can have angles of {p}° and {q}°. Explain why this is impossible.', f'{p} + {q} = {p + q}° > 180°, leaving no room for a third angle.',
                       'Sum compared with 180° (R1); conclusion (R1).', 2, 'G2')
    return explain(f'A kite has two equal opposite angles of {a + 40}° and a third angle of {b}°. Explain how to find the fourth angle and find it.', f'360 − 2 × {a + 40} − {b} = {360 - 2 * (a + 40) - b}°',
                   'Quadrilateral angle sum (R1); kite symmetry (R1); answer (A1).', 3) if 360 - 2 * (a + 40) - b > 0 else None


@R.add('ch07-st3', 'C4', (3, 5), 'multi_step')
def tri_task(rng, slot):
    a = rng.randint(20, 70)
    k = rng.randint(2, 4)
    frames = [
        (f'A roof truss is an isosceles triangle with apex angle {2 * a + 20}°. A vertical support goes from the apex to the midpoint of the base. (a) Find each base angle. (b) Find the angles in each of the two smaller triangles. (c) Explain why the support meets the base at 90°.',
         f'(a) {(180 - 2 * a - 20) // 2}° (b) {(180 - 2 * a - 20) // 2}°, {a + 10}°, 90° (c) the two smaller triangles are congruent (SSS), so the two angles at the base are equal and lie on a straight line: each 90°'),
        (f'Investigate: draw any quadrilateral and its diagonal. (a) Explain why the angle sum is 360°. (b) A quadrilateral has angles in the ratio 1 : 2 : {k} : {k + 1}. Find the angles. (c) Is the quadrilateral likely to have a pair of parallel sides? Justify using co-interior angles.',
         None),
    ]
    p1, p2 = rng.randint(55, 80), rng.randint(95, 125)
    who = name(rng)
    frames.append((f'{who} designs a kite-shaped logo ABCD with AB = AD and CB = CD. Angle BAD = {p1}° and angle BCD = {p2}°. (a) Explain why angles ABC and ADC are equal. (b) Find angle ABC. (c) The diagonal AC is drawn; find angle BAC and angle ACB and check the angle sum of triangle ABC.',
                   f'(a) the kite is symmetric about AC (triangles ABC and ADC are congruent, SSS) (b) {g((360 - p1 - p2) / 2, 4)}° (c) BAC = {g(p1 / 2, 4)}°, ACB = {g(p2 / 2, 4)}°; {g(p1 / 2, 4)} + {g(p2 / 2, 4)} + {g((360 - p1 - p2) / 2, 4)} = 180'))
    e1 = rng.randint(100, 140)
    e2 = rng.randint(100, 150)
    if e1 + e2 > 270:
        frames.append((f'In triangle PQR the exterior angle at P is {e1}° and the exterior angle at Q is {e2}°. (a) Find the interior angles at P and Q. (b) Find the interior and exterior angles at R. (c) Show that the three exterior angles add up to 360° and explain why this is always true.',
                       f'(a) P = {180 - e1}°, Q = {180 - e2}° (b) R = {e1 + e2 - 180}°, exterior {360 - e1 - e2}° (c) {e1} + {e2} + {360 - e1 - e2} = 360; each exterior = 180 − interior, so the sum is 3 × 180 − 180 = 360'))
    q_, ans = rng.choice(frames)
    if ans is None:
        parts = 2 * k + 4
        ang = [Fr(360 * p, parts) for p in (1, 2, k, k + 1)]
        par = any(ang[i] + ang[(i + 1) % 4] == 180 for i in range(4))
        ans = f'(a) the diagonal makes two triangles: 2 × 180° (b) {", ".join(g(float(t), 4) + "°" for t in ang)} (c) ' + ('yes – two adjacent angles add to 180°, so the sides between them could be parallel (a trapezium)' if par else 'no adjacent pair adds to 180°, so no sides are parallel')
    return short(q_, ans, f'{ans}. Angle facts stated (R1); calculation (M1 A1 A1); general reasoning communicated (C1).', 5, 'multi_step', 'G5')


R.facts('ch07-st4', F(
    terms=[('polygon', 'a closed 2D shape made of straight sides'),
           ('regular polygon', 'a polygon with all sides equal and all interior angles equal'),
           ('interior angle', 'an angle inside a polygon at one of its vertices'),
           ('exterior angle of a polygon', 'the angle between one side and the extension of the next side; the exterior angles of any convex polygon add to 360°')],
    facts=[('What is the sum of the interior angles of a hexagon?', '720°', ['1080°', '360°', '540°'], '(6 − 2) × 180 = 720.'),
           ('Each exterior angle of a regular polygon is 30°. How many sides does it have?', '12', ['6', '30', '10'], '360 ÷ 30 = 12.'),
           ('What is each interior angle of a regular pentagon?', '108°', ['72°', '540°', '120°'], 'Exterior 72°, interior 180 − 72 = 108.')],
    why=[('Explain why the interior angles of an n-sided polygon add to (n − 2) × 180°.', 'Diagonals from one vertex split the polygon into n − 2 triangles, each with angle sum 180°.'),
         ('Explain why the exterior angles of any convex polygon add to 360°.', 'Walking around the polygon you turn through each exterior angle once and end facing your original direction: one full turn, 360°.'),
         ('Explain why a regular polygon cannot have an exterior angle of 50°.', '360 ÷ 50 = 7.2 is not a whole number, so no regular polygon has that many sides.')],
    misc=[('The interior angles of a pentagon add up to 5 × 180° = 900°.', 'A pentagon splits into 3 triangles: (5 − 2) × 180 = 540°.'),
          ('The bigger the regular polygon, the bigger each exterior angle.', 'Exterior angle = 360°/n, so it gets smaller as the number of sides increases.')],
))


def _a(w):
    return ('an ' if w[0] in 'aeiou' else 'a ') + w


POLY = {3: 'triangle', 4: 'quadrilateral', 5: 'pentagon', 6: 'hexagon', 7: 'heptagon', 8: 'octagon', 9: 'nonagon', 10: 'decagon', 12: 'dodecagon', 15: '15-sided polygon', 18: '18-sided polygon', 20: '20-sided polygon'}


@R.add('ch07-st4', 'C3', (1, 4), 'short')
def polygon_angles(rng, slot):
    n = rng.choice([5, 6, 8, 9, 10, 12, 15, 18, 20])
    kind = rng.choice(['sum', 'int', 'ext', 'sides', 'missing'])
    if kind == 'sum':
        return short(f'Find the sum of the interior angles of {_a(POLY[n])}.', f'{(n - 2) * 180}°', f'({n} − 2) × 180 (M1) = {(n - 2) * 180}° (A1).', 2)
    if kind == 'int':
        return short(f'Find the size of each interior angle of a regular {POLY[n]}.', f'{g((n - 2) * 180 / n, 4)}°', f'Exterior 360 ÷ {n} = {g(360 / n, 4)}° (M1); interior 180 − {g(360 / n, 4)} = {g((n - 2) * 180 / n, 4)}° (A1).', 2)
    if kind == 'ext':
        return short(f'Find the size of each exterior angle of a regular {POLY[n]}.', f'{g(360 / n, 4)}°', f'360 ÷ {n} (M1) = {g(360 / n, 4)}° (A1).', 2)
    if kind == 'sides':
        intr = Fr(180 * (n - 2), n)
        return short(f'Each interior angle of a regular polygon is {g(float(intr), 4)}°. How many sides does it have?', str(n),
                     f'Exterior angle 180 − {g(float(intr), 4)} = {g(360 / n, 4)}° (M1); 360 ÷ {g(360 / n, 4)} = {n} (A1).', 2)
    n = rng.choice([5, 6])
    known = [rng.randint(95, 150) for _ in range(n - 1)]
    miss = (n - 2) * 180 - sum(known)
    if not 30 < miss < 180:
        return None
    return short(f'{_a(POLY[n])[0].upper() + _a(POLY[n])[1:]} has interior angles {", ".join(f"{t}°" for t in known)} and x. Find x.', f'x = {miss}°',
                 f'Angle sum {(n - 2) * 180}° (M1); x = {(n - 2) * 180} − {sum(known)} = {miss}° (A1).', 3)


@R.add('ch07-st4', 'C1', (1, 3), 'mcq')
def polygon_mcq(rng, slot):
    n = rng.choice([5, 6, 8, 9, 10, 12])
    return mcq(rng, f'What is the sum of the interior angles of {_a(POLY[n])}?', f'{(n - 2) * 180}°', [f'{n * 180}°', f'{(n - 1) * 180}°', '360°' if n != 4 else '540°'],
               f'({n} − 2) × 180 = {(n - 2) * 180}°.')


@R.add('ch07-st4', 'C2', (2, 4), 'explain')
def tessellate_explain(rng, slot):
    n = rng.choice([3, 4, 5, 6, 8, 10, 12])
    intr = Fr(180 * (n - 2), n)
    ok = Fr(360, intr).denominator == 1
    return explain(f'Explain whether regular {POLY[n]}s can tessellate (fit together around a point with no gaps), using the interior angle.',
                   f'Interior angle {g(float(intr), 4)}°; 360 ÷ {g(float(intr), 4)} = {g(float(Fr(360) / intr), 4)}, {"a whole number, so they tessellate" if ok else "not a whole number, so they leave gaps or overlap"}.',
                   'Interior angle found (A1); condition 360 ÷ interior angle must be a whole number (R1); conclusion (A1).', 3)


@R.add('ch07-st4', 'C4', (3, 5), 'multi_step')
def polygon_investigate(rng, slot):
    n = rng.choice([7, 9, 11, 13])
    k = rng.choice([5, 6, 8, 10])
    frames = [
        (f'Investigate the interior angle sums of polygons. (a) Copy and complete a table for n = 3, 4, 5, 6 sides showing the number of triangles from one vertex and the angle sum. (b) Describe the pattern and write a formula for an n-sided polygon. (c) Use it to find the angle sum of a polygon with {n} sides. (d) Could a polygon have an angle sum of {180 * n + 90}°? Explain.',
         f'(a) triangles 1, 2, 3, 4; sums 180°, 360°, 540°, 720° (b) S = (n − 2) × 180° (c) {(n - 2) * 180}° (d) no – the angle sum is always a multiple of 180°'),
        (f'A designer in {rng.choice(CITIES)} makes a floor pattern with a regular octagon and squares. (a) Find the interior angle of a regular octagon. (b) Show that two octagons and one square fit exactly around a point. (c) Explain why regular pentagons cannot be used alone. (d) Find the exterior angle of a regular {k}-gon.',
         f'(a) 135° (b) 135 + 135 + 90 = 360° (c) the interior angle 108° does not divide 360 exactly (d) {g(360 / k, 4)}°'),
    ]
    e = rng.choice([10, 12, 15, 18, 20, 24, 30, 36, 40, 45, 60, 72])
    m_ = rng.randint(5, 9)
    known = [rng.randint(100, 160) for _ in range(m_ - 1)]
    miss = (m_ - 2) * 180 - sum(known)
    if 360 % (e + 7):
        frames.append((f'A regular polygon has exterior angles of {e}°. (a) How many sides does it have? (b) Find its interior angle sum in two different ways and show they agree. (c) Explain why no regular polygon has an exterior angle of {e + 7}°.',
                       f'(a) {360 // e} (b) ({360 // e} − 2) × 180 = {(360 // e - 2) * 180}° and {360 // e} × {180 - e} = {(360 // e) * (180 - e)}° (c) 360 ÷ {e + 7} = {g(360 / (e + 7), 4)} is not a whole number'))
    if 0 < miss < 180:
        frames.append((f'A field in {rng.choice(CITIES)} has the shape of an irregular polygon with {m_} sides. A surveyor measures {m_ - 1} of the interior angles as {", ".join(f"{t}°" for t in known)}. (a) Find the interior angle sum. (b) Find the remaining angle. (c) Find the exterior angle at that corner and explain what the surveyor could check using all the exterior angles.',
                       f'(a) {(m_ - 2) * 180}° (b) {miss}° (c) {180 - miss}°; the exterior angles must add up to 360°'))
    q_, ans = rng.choice(frames)
    return short(q_, ans, f'{ans}. Pattern described and generalised (B: M1 A1); formula applied (A1); justified conclusion (R1 C1).', 6, 'multi_step', 'G5')


R.facts('ch07-st5', F(
    terms=[('perpendicular bisector', 'the line that cuts a segment in half at right angles; every point on it is the same distance from both ends of the segment'),
           ('angle bisector', 'the line that divides an angle into two equal angles; every point on it is the same distance from both arms'),
           ('locus', 'the set of all points that satisfy a given rule'),
           ('construction', 'an accurate drawing made using only a straight edge (ruler) and compasses')],
    facts=[('Which construction gives the set of points equidistant from two points A and B?', 'the perpendicular bisector of AB', ['the angle bisector at A', 'a circle centred at A', 'a line parallel to AB'], 'Points on the perpendicular bisector are the same distance from A and B.'),
           ('Which angle can be constructed by bisecting a 60° angle?', '30°', ['45°', '20°', '15°'], 'Half of 60° is 30°.'),
           ('A triangle with sides 3 cm, 4 cm and 8 cm:', 'cannot be constructed', ['is right-angled', 'is isosceles', 'is equilateral'], '3 + 4 < 8, so the arcs never meet.')],
    why=[('Explain why the compass width must stay the same when constructing a perpendicular bisector.', 'The intersection points must be equal distances from both ends of the segment; equal arcs guarantee this, so the line through them is the perpendicular bisector.'),
         ('Explain why a 60° angle can be constructed with compasses alone (plus a straight edge).', 'Using the same radius from a point creates an equilateral triangle, whose angles are all 60°.'),
         ('Explain why a triangle can only be constructed if the sum of any two sides is greater than the third.', 'The two shorter sides must reach each other from the ends of the longest side; if they are too short together, the arcs do not intersect.')],
    misc=[('You can construct a triangle with sides 5 cm, 6 cm and 12 cm using compasses.', '5 + 6 = 11 < 12, so the arcs will not meet; no such triangle exists.'),
          ('An angle bisector divides the opposite side of a triangle in half.', 'It divides the angle in half; it only bisects the opposite side in special cases such as an isosceles triangle.')],
    apply=[('Describe the steps to construct the perpendicular bisector of a line segment AB of length 8 cm.', 'Set compasses to more than 4 cm; draw arcs from A and from B above and below AB; join the two intersection points with a straight line.', 3),
           ('Describe how to construct an angle of 45° using a ruler and compasses only.', 'Construct a perpendicular (90°) to a line at a point, then bisect the right angle to give 45°.', 3),
           ('Describe how to construct an angle of 60° at point P on a line.', 'With centre P draw an arc crossing the line at Q; with the same radius and centre Q draw an arc crossing the first arc at R; join PR: angle RPQ = 60°.', 3)],
))


@R.add('ch07-st5', 'C3', (1, 4), 'short')
def triangle_inequality(rng, slot):
    a, b = rng.randint(3, 12), rng.randint(3, 12)
    c = rng.randint(2, a + b + 3)
    ok = a + b > c and a + c > b and b + c > a
    return short(f'{name(rng)} wants to construct a triangle with sides {a} cm, {b} cm and {c} cm using a ruler and compasses. Decide whether this is possible, giving a reason.',
                 'possible' if ok else 'not possible', f'Check that the two shorter sides add to more than the longest: {" + ".join(map(str, sorted([a, b, c])[:2]))} = {sum(sorted([a, b, c])[:2])} {">" if ok else "≤"} {max(a, b, c)} (M1); conclusion (A1).', 2)


@R.add('ch07-st5', 'C3', (2, 4), 'short')
def construct_angles(rng, slot):
    ang = rng.choice([90, 45, 60, 30, 15, 120, 135, 150, 75, 105])
    steps = {90: 'construct a perpendicular to a line at a point', 45: 'construct 90° and bisect it', 60: 'construct an equilateral triangle (equal arcs)', 30: 'construct 60° and bisect it',
             15: 'construct 60°, bisect to 30°, then bisect again', 120: 'construct 60° and use the angle on the straight line next to it (180 − 60)', 135: 'construct 45° and use the adjacent angle on a straight line (180 − 45)',
             150: 'construct 30° and use the adjacent angle on a straight line (180 − 30)', 75: 'construct 60° and 90° next to each other and bisect the 30° between them, adding 15° to 60°', 105: 'construct 90° and add 15° (bisect the 30° between 60° and 90°)'}
    return short(f'Explain how to construct an angle of {ang}° using only a ruler and compasses.', steps[ang], f'{steps[ang]} (M1 for a valid sequence, A1 for accurate construction method, C1 for clear steps).', 3)


@R.add('ch07-st5', 'C1', (1, 3), 'mcq')
def construct_mcq(rng, slot):
    ang = rng.choice([30, 45, 15, 120])
    corr = {30: 'bisect a 60° angle', 45: 'bisect a 90° angle', 15: 'bisect a 30° angle', 120: 'construct 60° and take the adjacent angle on a straight line'}[ang]
    w = [v for k, v in {30: 'bisect a 60° angle', 45: 'bisect a 90° angle', 15: 'bisect a 30° angle', 120: 'construct 60° and take the adjacent angle on a straight line', 0: 'bisect a 120° angle twice'}.items() if k != ang]
    return mcq(rng, f'Which method constructs an angle of {ang}° with ruler and compasses?', corr, w[:3], f'{corr} gives {ang}°.')


@R.add('ch07-st5', 'C2', (2, 4), 'explain')
def locus_explain(rng, slot):
    d = rng.randint(2, 9)
    L = rng.randint(6, 15)
    kind = rng.choice(['two', 'dist', 'bisect'])
    if kind == 'two':
        return explain(f'Two mobile phone masts A and B are {L} km apart. Explain how to construct the set of points that are the same distance from both masts, and why your construction works.',
                       'Construct the perpendicular bisector of AB; its points are equidistant from A and B because the equal compass arcs from A and B meet on it.',
                       'Perpendicular bisector named (A1); construction steps (M1); reason (R1).', 3)
    if kind == 'dist':
        return explain(f'A goat is tied by a {d} m rope to a post in a field. Describe and explain the shape of the region the goat can reach.',
                       f'A disc (circle and its inside) of radius {d} m centred on the post: every point within {d} m can be reached.',
                       'Circle of radius named (A1); includes the interior (R1).', 2)
    return explain('Explain why every point on the bisector of an angle is the same distance from the two arms of the angle.',
                   'Drop perpendiculars from a point on the bisector to each arm: the two right-angled triangles share the hypotenuse and have equal angles, so they are congruent (AAS), and the perpendicular distances are equal.',
                   'Perpendicular distances (R1); congruent triangles (R1); conclusion (A1).', 3)


@R.add('ch07-st5', 'C4', (3, 5), 'multi_step')
def construct_task(rng, slot):
    a, b, c = sorted(rng.sample(range(4, 13), 3))
    if a + b <= c:
        return None
    city = rng.choice(CITIES)
    L = rng.randint(6, 12)
    frames = [
        (f'A triangular garden in {city} has sides {a} m, {b} m and {c} m. (a) Choose a scale and describe how to construct an accurate scale drawing using ruler and compasses. (b) Check that the triangle can be made. (c) A tree is to be planted the same distance from all three corners – describe how to find its position.',
         f'(a) e.g. 1 cm : 1 m; draw {c} cm, arcs of {a} cm and {b} cm from the ends (b) {a} + {b} = {a + b} > {c}, so it exists (c) construct the perpendicular bisectors of two sides; the tree goes where they cross'),
        (f'Two schools are {L} km apart. A new library must be equidistant from both schools and within {L - 2} km of the first school. (a) Describe the two loci. (b) Explain how the possible positions are found. (c) Explain why there are many possible positions, not just one.',
         f'(a) the perpendicular bisector of the line joining the schools; a circle of radius {L - 2} km centred on the first school (b) the part of the bisector inside the circle (c) the bisector crosses the circle, so a whole segment of points satisfies both conditions'),
    ]
    q_, ans = rng.choice(frames)
    return short(q_, ans, f'{ans}. Correct constructions/loci chosen (M1 A1); triangle inequality or intersection reasoning (R1); clear description of method (C1).', 4, 'multi_step', 'G5')


# =============================================================================================
# ch08 Pythagoras' Theorem
# =============================================================================================
def _root_txt(v2):
    """√v2 exact if square, else 'x.xx' and exact surd."""
    r = math.isqrt(v2)
    if r * r == v2:
        return str(r), True
    return f'{math.sqrt(v2):.2f}', False


R.facts('ch08-st1', F(
    terms=[('hypotenuse', 'the longest side of a right-angled triangle, opposite the right angle'),
           ("Pythagoras' theorem", 'in a right-angled triangle the square of the hypotenuse equals the sum of the squares of the other two sides: a² + b² = c²'),
           ('legs of a right-angled triangle', 'the two shorter sides that form the right angle')],
    facts=[('A right-angled triangle has legs 6 cm and 8 cm. What is the hypotenuse?', '10 cm', ['14 cm', '48 cm', '100 cm'], '√(36 + 64) = √100 = 10.'),
           ("Which equation is Pythagoras' theorem for a triangle with hypotenuse h and legs p and q?", 'h² = p² + q²', ['h = p + q', 'p² = h² + q²', 'h² = p² − q²'], 'The hypotenuse squared equals the sum of the squares of the legs.'),
           ('Which side is the hypotenuse in a right-angled triangle?', 'the side opposite the right angle', ['the side next to the right angle', 'the vertical side', 'the shortest side'], 'It is opposite the 90° angle and is the longest.')],
    why=[("Explain why the hypotenuse is always the longest side of a right-angled triangle.", 'c² = a² + b² is greater than a² and greater than b², so c is greater than a and b.'),
         ("Explain how squares drawn on the sides of a right-angled triangle illustrate Pythagoras' theorem.", 'The area of the square on the hypotenuse equals the total area of the squares on the other two sides, which is a² + b² = c².'),
         ("Explain why Pythagoras' theorem cannot be used on a triangle without a right angle.", 'The theorem is only true for right-angled triangles; for other triangles a² + b² is more or less than c².')],
    misc=[('The hypotenuse of a triangle with legs 5 and 12 is 17.', 'You must square, add and then square-root: √(25 + 144) = √169 = 13.'),
          ('In a right-angled triangle with legs 3 and 4, c² = 3 + 4 = 7.', 'Square each side first: c² = 9 + 16 = 25, so c = 5.')],
))

TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41), (6, 8, 10), (9, 12, 15), (12, 16, 20), (15, 20, 25), (10, 24, 26), (12, 35, 37)]


@R.add('ch08-st1', 'C3', (1, 4), 'numerical')
def hyp(rng, slot):
    if slot.d <= 2:
        a, b, c = rng.choice(TRIPLES)
        k = rng.choice([1, 1, 2, 3])
        a, b, c = a * k, b * k, c * k
        return short(f'A right-angled triangle has shorter sides {a} cm and {b} cm. Find the length of the hypotenuse.', f'{c} cm',
                     f'c² = {a}² + {b}² = {a * a + b * b} (M1); c = {c} cm (A1).', 2, 'numerical')
    a, b = Decimal(rng.randint(25, 150)) / 10, Decimal(rng.randint(25, 150)) / 10
    c2 = a * a + b * b
    c = math.sqrt(float(c2))
    return short(f'Find the hypotenuse of a right-angled triangle whose shorter sides are {a} m and {b} m. Give your answer to 3 significant figures.', f'{rsf(c, 3)} m',
                 f'c² = {a}² + {b}² = {c2} (M1 A1); c = √{c2} = {rsf(c, 3)} m (A1).', 3, 'numerical')


@R.add('ch08-st1', 'C3', (2, 4), 'numerical')
def hyp_context(rng, slot):
    city = rng.choice(CITIES)
    a, b = rng.randint(5, 40), rng.randint(5, 40)
    c = math.hypot(a, b)
    ctx = rng.choice([
        (f'A rectangular park in {city} measures {a} m by {b} m. How long is the diagonal path across it, to the nearest 0.1 m?', 'm'),
        (f'A TV screen is {a} inches wide and {b} inches high. Find the length of its diagonal, to the nearest 0.1 inch.', 'inches'),
        (f'A drone flies {a} km east and then {b} km north. How far is it from its starting point, to 1 decimal place?', 'km'),
    ])
    return short(ctx[0], f'{rnd(c, 1)} {ctx[1]}', f'Right angle identified (R1); √({a}² + {b}²) = √{a * a + b * b} (M1) = {rnd(c, 1)} {ctx[1]} (A1).', 3, 'numerical')


@R.add('ch08-st1', 'C1', (1, 3), 'mcq')
def hyp_mcq(rng, slot):
    a, b, c = rng.choice(TRIPLES)
    return mcq(rng, f'A right-angled triangle has legs {a} and {b}. What is the length of the hypotenuse?', str(c), [str(a + b), str(a * a + b * b), str(2 * c)],
               f'√({a * a} + {b * b}) = √{c * c} = {c}.')


@R.add('ch08-st1', 'C2', (2, 4), 'explain')
def hyp_explain(rng, slot):
    a, b = rng.randint(3, 12), rng.randint(3, 12)
    who = name(rng)
    c = math.hypot(a, b)
    kind = rng.choice(['add', 'estimate'])
    if kind == 'add':
        return explain(f'{who} says the hypotenuse of a right-angled triangle with legs {a} cm and {b} cm is {a + b} cm. Explain why this cannot be right and find the correct length.',
                       f'The sides would not form a triangle (a + b must be longer than c); c = √({a * a} + {b * b}) = {rsf(c, 3)} cm.',
                       'Reason (triangle inequality or squares not added) (R1); correct method and value (M1 A1).', 3, 'G2')
    return explain(f'Without a calculator, explain why the hypotenuse of a right-angled triangle with legs {a} and {b} lies between {math.isqrt(a * a + b * b)} and {math.isqrt(a * a + b * b) + 1}.',
                   f'c² = {a * a + b * b}; {math.isqrt(a * a + b * b)}² = {math.isqrt(a * a + b * b) ** 2} ≤ {a * a + b * b} < {(math.isqrt(a * a + b * b) + 1) ** 2}, so c lies between them.',
                   'c² found (A1); bounds by square numbers (R1).', 2) if math.isqrt(a * a + b * b) ** 2 != a * a + b * b else None


@R.add('ch08-st1', 'C4', (3, 5), 'multi_step')
def hyp_task(rng, slot):
    a, b, h = rng.randint(3, 12), rng.randint(3, 12), rng.randint(2, 9)
    city = rng.choice(CITIES)
    w, l = rng.randint(20, 60), rng.randint(40, 100)
    frames = [
        (f'A box is {a} cm long, {b} cm wide and {h} cm tall. (a) Find the length of the diagonal of the base. (b) Find the length of the longest straight rod that fits inside the box (the space diagonal). (c) Will a {rsf(math.sqrt(a * a + b * b + h * h) + 0.5, 3)} cm pencil fit? Explain.',
         f'(a) √{a * a + b * b} = {rsf(math.sqrt(a * a + b * b), 3)} cm (b) √{a * a + b * b + h * h} = {rsf(math.sqrt(a * a + b * b + h * h), 3)} cm (c) no – it is longer than the space diagonal'),
        (f'A football pitch in {city} is {l} m long and {w} m wide. (a) Find the diagonal distance from corner to corner. (b) A player runs along two sides instead. How much further is that? (c) Explain why the diagonal is always shorter than the two sides.',
         f'(a) {rsf(math.hypot(l, w), 4)} m (b) {rsf(l + w - math.hypot(l, w), 3)} m (c) the diagonal is the hypotenuse; c < a + b for any triangle'),
    ]
    q_, ans = rng.choice(frames)
    return short(q_, ans, f'{ans}. Right-angled triangle identified (R1); Pythagoras applied (M1 A1); second application / comparison (M1 A1); conclusion (C1).', 6, 'multi_step', 'G5')


R.facts('ch08-st2', F(
    terms=[('shorter side', 'one of the two legs of a right-angled triangle, found by a² = c² − b²'),
           ('right-angled triangle', 'a triangle with one angle of exactly 90°')],
    facts=[('A right-angled triangle has hypotenuse 13 cm and one leg 5 cm. What is the other leg?', '12 cm', ['8 cm', '13.9 cm', '18 cm'], '√(169 − 25) = √144 = 12.'),
           ('To find a shorter side you should:', 'subtract the squares', ['add the squares', 'subtract the sides', 'halve the hypotenuse'], 'a² = c² − b².'),
           ('A 5 m ladder reaches 4 m up a wall. How far is its foot from the wall?', '3 m', ['1 m', '6.4 m', '9 m'], '√(25 − 16) = 3.')],
    why=[('Explain why you subtract when finding a shorter side.', 'c² = a² + b², so a² = c² − b²: the shorter side squared is what remains when b² is taken away from c².'),
         ('Explain how you can check that your answer for a shorter side is sensible.', 'It must be less than the hypotenuse, and substituting back should satisfy a² + b² = c².'),
         ('Explain why a ladder leaning against a wall forms a right-angled triangle.', 'The wall is vertical and the ground is horizontal, so they meet at 90°; the ladder is the hypotenuse.')],
    misc=[('If the hypotenuse is 10 and a leg is 6, the other leg is √(100 + 36).', 'For a leg subtract: √(100 − 36) = √64 = 8.'),
          ('The shorter side of a right triangle with hypotenuse 9 and leg 4 is 9 − 4 = 5.', 'Square first: √(81 − 16) = √65 ≈ 8.06.')],
))


@R.add('ch08-st2', 'C3', (1, 4), 'numerical')
def short_side(rng, slot):
    if slot.d <= 2:
        a, b, c = rng.choice(TRIPLES)
        return short(f'A right-angled triangle has hypotenuse {c} cm and one shorter side {a} cm. Find the other side.', f'{b} cm',
                     f'b² = {c}² − {a}² = {c * c - a * a} (M1); b = {b} cm (A1).', 2, 'numerical')
    c = Decimal(rng.randint(80, 250)) / 10
    a = Decimal(rng.randint(20, int(c * 10) - 5)) / 10
    b = math.sqrt(float(c * c - a * a))
    return short(f'In a right-angled triangle the hypotenuse is {c} m and one shorter side is {a} m. Find the third side to 3 significant figures.', f'{rsf(b, 3)} m',
                 f'b² = {c}² − {a}² = {c * c - a * a} (M1 A1); b = {rsf(b, 3)} m (A1).', 3, 'numerical')


@R.add('ch08-st2', 'C3', (2, 5), 'numerical')
def pyth_problem(rng, slot):
    city = rng.choice(CITIES)
    L, h = rng.randint(4, 12), None
    foot = Decimal(rng.randint(8, int(L * 10 * 0.6))) / 10
    h = math.sqrt(L * L - float(foot) ** 2)
    s, base = rng.randint(6, 20), rng.randint(4, 16)
    slant = math.hypot(s, base / 2)
    frames = [
        (f'A {L} m ladder leans against a wall in {city} with its foot {foot} m from the wall. How high up the wall does it reach? Give your answer to 2 d.p.', f'{rnd(h, 2)} m',
         f'h² = {L}² − {foot}² (M1) = {L * L - foot * foot} (A1); h = {rnd(h, 2)} m (A1).'),
        (f'An isosceles triangle has equal sides of {rnd(slant, 1)} cm and a base of {base} cm. Find its perpendicular height and area, to 1 d.p.', None, None),
    ]
    q_, ans, key = rng.choice(frames)
    if ans is None:
        sl = float(rnd(slant, 1))
        hh = math.sqrt(sl * sl - (base / 2) ** 2)
        ans = f'height {rnd(hh, 1)} cm, area {rnd(0.5 * base * hh, 1)} cm²'
        key = f'Half the base = {base / 2:g} (M1); h = √({sl}² − {base / 2:g}²) = {rnd(hh, 1)} (A1); area ½ × {base} × h = {rnd(0.5 * base * hh, 1)} cm² (A1).'
    return short(q_, ans, key, 3, 'numerical')


@R.add('ch08-st2', 'C1', (1, 3), 'mcq')
def short_mcq(rng, slot):
    a, b, c = rng.choice(TRIPLES)
    return mcq(rng, f'A right-angled triangle has hypotenuse {c} and one leg {b}. What is the other leg?', str(a), [str(c - b), str(c + b), f'{math.sqrt(c * c + b * b):.1f}'],
               f'√({c * c} − {b * b}) = √{a * a} = {a}.')


@R.add('ch08-st2', 'C2', (2, 4), 'explain')
def which_side(rng, slot):
    a, b, c = rng.choice(TRIPLES)
    who = name(rng)
    return explain(f'{who} is told that a right-angled triangle has sides {b} cm and {c} cm and must find the third side. Explain why {who} needs to know which side is the hypotenuse, and find both possible answers.',
                   f'If {c} is the hypotenuse, the third side is √({c * c} − {b * b}) = {a} cm; if the third side is the hypotenuse, it is √({c * c} + {b * b}) = {rsf(math.sqrt(c * c + b * b), 3)} cm.',
                   'Two cases identified (R1); both values (A1 A1).', 3)


@R.add('ch08-st2', 'C4', (3, 5), 'multi_step')
def pyth_task2(rng, slot):
    city, country, cur, cname = place(rng)
    w, h = rng.randint(3, 8), rng.randint(2, 6)
    roof = rng.randint(1, 4)
    price = rng.randint(8, 30)
    d1, d2 = rng.randint(3, 15), rng.randint(3, 15)
    frames = [
        (f'A garden shed in {city} has a sloping roof. The front wall is {h + roof} m high, the back wall is {h} m high, and the shed is {w} m deep. (a) Find the length of the sloping roof edge. (b) The roof is {w + 1} m wide; find its area. (c) Roofing costs {cur}{price} per m². Find the cost.',
         None),
        (f'A ship leaves port near {city} and sails {d1} km north, then {d2} km west. (a) How far is it from port? (b) A second ship leaves at the same time and sails directly to the same point at 20 km/h. How long does it take, in minutes? (c) Explain why the second route is shorter.',
         f'(a) {rsf(math.hypot(d1, d2), 3)} km (b) {rsf(math.hypot(d1, d2) / 20 * 60, 3)} min (c) the direct route is the hypotenuse, shorter than the two legs together'),
    ]
    q_, ans = rng.choice(frames)
    if ans is None:
        e = math.hypot(w, roof)
        area = e * (w + 1)
        ans = f'(a) {rsf(e, 3)} m (b) {rsf(area, 3)} m² (c) {cur}{rnd(area * price, 2)}'
    return short(q_, ans, f'{ans}. Right-angled triangle identified in the context (R1); Pythagoras (M1 A1); further calculation (M1 A1); answer in context (D).', 6, 'multi_step', 'G5')


R.facts('ch08-st3', F(
    terms=[('Pythagorean triple', 'three whole numbers a, b, c with a² + b² = c², such as 3, 4, 5'),
           ("converse of Pythagoras' theorem", 'if the sides of a triangle satisfy a² + b² = c², then the triangle has a right angle opposite c')],
    facts=[('Which set is a Pythagorean triple?', '9, 40, 41', ['4, 5, 6', '5, 11, 12', '7, 8, 11'], '81 + 1600 = 1681 = 41².'),
           ('A triangle has sides 7, 8 and 11. Is it right-angled?', 'no, because 49 + 64 ≠ 121', ['yes, because 7 + 8 > 11', 'yes, because 11 is the longest side', 'no, because 7 + 8 ≠ 11'], '49 + 64 = 113 ≠ 121.'),
           ('Multiplying the triple 5, 12, 13 by 3 gives:', '15, 36, 39', ['8, 15, 16', '15, 36, 40', '5, 36, 39'], 'Multiples of a triple are also triples.')],
    why=[('Explain why any multiple of a Pythagorean triple is also a triple.', '(ka)² + (kb)² = k²(a² + b²) = k²c² = (kc)², so ka, kb, kc also satisfy the theorem.'),
         ("Explain how builders can use the converse of Pythagoras' theorem to check a right angle.", 'Measure 3 m along one wall and 4 m along the other; if the diagonal between the marks is 5 m, the corner is a right angle.'),
         ('Explain why you must use the longest side as c when testing whether a triangle is right-angled.', 'Only the hypotenuse can be the side opposite a right angle, and it is always the longest side.')],
    misc=[('6, 8, 10 is not a Pythagorean triple because 3, 4, 5 is the triple.', '36 + 64 = 100 = 10², so 6, 8, 10 is a triple (a multiple of 3, 4, 5).'),
          ('A triangle with sides 5, 12, 13 has the right angle opposite the 5 cm side.', 'The right angle is opposite the longest side, 13.')],
))


@R.add('ch08-st3', 'C3', (1, 4), 'short')
def converse_test(rng, slot):
    if rng.random() < 0.5:
        a, b, c = rng.choice(TRIPLES)
        k = rng.choice([1, 2, 3, Fr(1, 2)])
        a, b, c = a * k, b * k, c * k
    else:
        a, b = rng.randint(4, 20), rng.randint(4, 20)
        c = math.isqrt(a * a + b * b) + rng.choice([0, 1])
        if c * c == a * a + b * b:
            c += 1
    sides = [a, b, c]
    rng.shuffle(sides)
    s_ = sorted(sides)
    ok = s_[0] ** 2 + s_[1] ** 2 == s_[2] ** 2
    if not (s_[0] + s_[1] > s_[2]):
        return None
    txt = ', '.join(g(float(t)) for t in sides)
    lhs = s_[0] ** 2 + s_[1] ** 2
    return short(f'A triangle has sides {txt} cm. Use the converse of Pythagoras’ theorem to decide whether it is right-angled.', 'right-angled' if ok else 'not right-angled',
                 f'Longest side {g(float(s_[2]))}: {g(float(s_[2]))}² = {g(float(s_[2] ** 2))} (M1); {g(float(s_[0]))}² + {g(float(s_[1]))}² = {g(float(lhs))} (A1); {"equal" if ok else "not equal"} ⇒ {"right-angled" if ok else "not right-angled"} (R1).', 3)


@R.add('ch08-st3', 'C3', (2, 4), 'short')
def make_triples(rng, slot):
    mm, n = rng.randint(2, 7), rng.randint(1, 6)
    if n >= mm:
        mm, n = n + 1, mm
    a, b, c = mm * mm - n * n, 2 * mm * n, mm * mm + n * n
    return short(f'Use the formulas a = m² − n², b = 2mn, c = m² + n² with m = {mm} and n = {n} to generate three numbers, and verify that they form a Pythagorean triple.',
                 f'{a}, {b}, {c}', f'Substitution (M1); {a}² + {b}² = {a * a + b * b} = {c}² (A1 R1).', 3)


@R.add('ch08-st3', 'C1', (1, 3), 'mcq')
def triple_mcq(rng, slot):
    a, b, c = rng.choice(TRIPLES)
    k = rng.randint(1, 3)
    corr = f'{a * k}, {b * k}, {c * k}'
    w = [f'{a * k}, {b * k}, {c * k + 1}', f'{a * k + 1}, {b * k + 1}, {c * k + 1}', f'{a * k}, {b * k}, {a * k + b * k}']
    return mcq(rng, 'Which of these sets of numbers is a Pythagorean triple?', corr, w, f'{a * k}² + {b * k}² = {(c * k) ** 2} = {c * k}².')


@R.add('ch08-st3', 'C2', (2, 4), 'explain')
def triple_pattern(rng, slot):
    n = rng.choice([3, 5, 7, 9, 11, 13])
    b = (n * n - 1) // 2
    return explain(f'The triples 3, 4, 5 and 5, 12, 13 and 7, 24, 25 start with odd numbers and the last two numbers differ by 1. Describe the pattern and use it to find the triple starting with {n}.',
                   f'For odd n: b = (n² − 1)/2, c = b + 1; for n = {n}: {n}, {b}, {b + 1} (check {n * n} + {b * b} = {(b + 1) ** 2}).',
                   'Pattern described (B1); rule applied (A1); verification (R1).', 3)


@R.add('ch08-st3', 'C4', (3, 5), 'multi_step')
def converse_task(rng, slot):
    a, b, c = rng.choice(TRIPLES[:6])
    k = rng.randint(1, 3)
    err = rng.choice([0, 1, 2])
    who = name(rng)
    frames = [
        (f'{who} is marking out a rectangular basketball court. {who} measures two sides of a corner as {a * k} m and {b * k} m, and the diagonal as {c * k + err} m. (a) Is the corner a right angle? (b) If not, should the angle be bigger or smaller than 90°? Explain. (c) What should the diagonal measure?',
         f'(a) {"yes" if err == 0 else "no"}: {a * k}² + {b * k}² = {(c * k) ** 2}, diagonal² = {(c * k + err) ** 2} (b) ' + ('it is exactly 90°' if err == 0 else 'the diagonal is too long, so the angle is bigger than 90°') + f' (c) {c * k} m'),
        (f'Investigate whether triangles with sides n, n + 1, n + 2 can ever be right-angled. (a) Write the condition using Pythagoras. (b) Solve it. (c) State the triangle(s) that work.',
         '(a) n² + (n + 1)² = (n + 2)² (b) n² − 2n − 3 = 0, (n − 3)(n + 1) = 0, n = 3 (n > 0) (c) only 3, 4, 5'),
    ]
    q_, ans = rng.choice(frames)
    return short(q_, ans, f'{ans}. Converse applied with longest side (M1 A1); reasoning about the angle or algebra (R1 A1); conclusion communicated (C1).', 5, 'multi_step', 'G5')


R.facts('ch08-st4', F(
    terms=[('distance formula', 'the distance between (x₁, y₁) and (x₂, y₂) is √((x₂ − x₁)² + (y₂ − y₁)²), from Pythagoras'),
           ('line segment', 'the part of a line between two end points')],
    facts=[('What is the distance between (1, 2) and (4, 6)?', '5', ['7', '25', '3.6'], '√(3² + 4²) = 5.'),
           ('The distance between (0, 0) and (5, 12) is:', '13', ['17', '7', '169'], '√(25 + 144) = 13.'),
           ('Which calculation gives the distance between (−2, 3) and (4, −5)?', '√(6² + 8²)', ['√(2² + 2²)', '6 + 8', '√(6² − 8²)'], 'Differences are 6 and −8.')],
    why=[('Explain how Pythagoras’ theorem gives the distance between two points on a grid.', 'The horizontal and vertical differences form the legs of a right-angled triangle whose hypotenuse is the segment joining the points.'),
         ('Explain why it does not matter in which order you subtract the coordinates.', 'The differences are squared, and (−d)² = d², so the result is the same.'),
         ('Explain why the distance between two points is never negative.', 'It is the square root of a sum of squares, which is never negative.')],
    misc=[('The distance between (2, 1) and (5, 5) is 3 + 4 = 7.', 'Use Pythagoras: √(3² + 4²) = 5, the straight-line distance.'),
          ('The distance between (−3, 0) and (3, 0) is 0 because −3 + 3 = 0.', 'Subtract the coordinates: 3 − (−3) = 6, so the distance is 6.')],
))


@R.add('ch08-st4', 'C3', (1, 4), 'numerical')
def dist_pts(rng, slot):
    x1, y1 = rng.randint(-8, 8), rng.randint(-8, 8)
    if slot.d <= 2:
        a, b, c = rng.choice(TRIPLES[:6])
        dx, dy = rng.choice([-1, 1]) * a, rng.choice([-1, 1]) * b
        x2, y2 = x1 + dx, y1 + dy
        return short(f'Find the distance between A({m(x1)}, {m(y1)}) and B({m(x2)}, {m(y2)}).', str(c),
                     f'Differences {abs(dx)} and {abs(dy)} (M1); √({dx * dx} + {dy * dy}) = {c} (A1).', 2, 'numerical')
    x2, y2 = rng.randint(-8, 8), rng.randint(-8, 8)
    d2 = (x2 - x1) ** 2 + (y2 - y1) ** 2
    if d2 == 0:
        return None
    r = math.isqrt(d2)
    exact = str(r) if r * r == d2 else f'√{d2}'
    return short(f'Find the exact distance between P({m(x1)}, {m(y1)}) and Q({m(x2)}, {m(y2)}), and give it to 3 significant figures.', f'{exact} ≈ {rsf(math.sqrt(d2), 3)}',
                 f'({m(x2)} − {m(x1) if x1 >= 0 else f"({m(x1)})"})² + ({m(y2)} − {m(y1) if y1 >= 0 else f"({m(y1)})"})² = {d2} (M1 A1); {exact} ≈ {rsf(math.sqrt(d2), 3)} (A1).', 3, 'numerical')


@R.add('ch08-st4', 'C3', (2, 4), 'short')
def dist_shape(rng, slot):
    a, b, c = rng.choice(TRIPLES[:4])
    x0, y0 = rng.randint(-5, 2), rng.randint(-5, 2)
    A, B, C = (x0, y0), (x0 + a, y0), (x0 + a, y0 + b)
    pts = lambda P: f'({m(P[0])}, {m(P[1])})'
    return short(f'Triangle ABC has vertices A{pts(A)}, B{pts(B)} and C{pts(C)}. Find the lengths of all three sides and the perimeter of the triangle.', f'AB = {a}, BC = {b}, AC = {c}; perimeter {a + b + c}',
                 f'AB and BC by counting (A1); AC by Pythagoras √({a * a} + {b * b}) = {c} (M1 A1); perimeter (A1).', 4)


@R.add('ch08-st4', 'C1', (1, 3), 'mcq')
def dist_mcq(rng, slot):
    a, b, c = rng.choice(TRIPLES[:5])
    x1, y1 = rng.randint(-4, 4), rng.randint(-4, 4)
    return mcq(rng, f'What is the distance between ({m(x1)}, {m(y1)}) and ({m(x1 + a)}, {m(y1 + b)})?', str(c), [str(a + b), str(c * c), str(abs(b - a))], f'√({a}² + {b}²) = {c}.')


@R.add('ch08-st4', 'C2', (2, 4), 'explain')
def dist_explain(rng, slot):
    x1, y1 = rng.randint(-5, 5), rng.randint(-5, 5)
    dx, dy = rng.randint(2, 7), rng.randint(2, 7)
    who = name(rng)
    d2 = dx * dx + dy * dy
    return explain(f'{who} calculates the distance between ({m(x1)}, {m(y1)}) and ({m(x1 + dx)}, {m(y1 - dy)}) as √({dx}² − {dy}²). Explain the error and find the correct distance.',
                   f'The squares of the differences must be added: √({dx * dx} + {dy * dy}) = √{d2} ≈ {rsf(math.sqrt(d2), 3)}.',
                   'Error identified (R1); correct value (A1).', 2, 'G2')


@R.add('ch08-st4', 'C4', (3, 5), 'multi_step')
def dist_task(rng, slot):
    city = rng.choice(CITIES)
    pts_ = [(rng.randint(-6, 6), rng.randint(-6, 6)) for _ in range(3)]
    if len(set(pts_)) < 3:
        return None
    A, B, C = pts_
    d = lambda P, Q: math.hypot(P[0] - Q[0], P[1] - Q[1])
    d2 = lambda P, Q: (P[0] - Q[0]) ** 2 + (P[1] - Q[1]) ** 2
    s = sorted([d2(A, B), d2(B, C), d2(A, C)])
    right = s[0] + s[1] == s[2]
    iso = len(set(s)) < 3
    p = lambda P: f'({m(P[0])}, {m(P[1])})'
    frames = [
        (f'On a map of {city} with a 1 km grid, a school is at {p(A)}, a library at {p(B)} and a sports centre at {p(C)}. (a) Find the straight-line distance between each pair of places. (b) Which two places are closest? (c) Is the triangle they form right-angled or isosceles? Justify your answer.',
         f'(a) school–library {rsf(d(A, B), 3)} km, library–sports {rsf(d(B, C), 3)} km, school–sports {rsf(d(A, C), 3)} km (b) ' +
         min([('school and library', d(A, B)), ('library and sports centre', d(B, C)), ('school and sports centre', d(A, C))], key=lambda t: t[1])[0] +
         f' (c) {"right-angled" if right else "not right-angled"}{", isosceles" if iso else ", not isosceles"} (squared lengths {", ".join(map(str, s))})'),
    ]
    q_, ans = frames[0]
    return short(q_, ans, f'{ans}. Distance formula applied three times (M1 A1 A1); comparison (A1); converse of Pythagoras / equal sides reasoning (R1 C1).', 6, 'multi_step', 'G5')


# =============================================================================================
# ch09 Area, Surface Area and Volume
# =============================================================================================
R.facts('ch09-st1', F(
    terms=[('area', 'the amount of flat surface a 2D shape covers, measured in square units'),
           ('trapezium', 'a quadrilateral with exactly one pair of parallel sides; area = ½(a + b)h'),
           ('parallelogram', 'a quadrilateral with two pairs of parallel sides; area = base × perpendicular height'),
           ('compound shape', 'a shape made by joining or removing simpler shapes such as rectangles and triangles')],
    facts=[('What is the area of a triangle with base 10 cm and height 7 cm?', '35 cm²', ['70 cm²', '17 cm²', '35 cm'], '½ × 10 × 7 = 35 cm².'),
           ('A trapezium has parallel sides 6 m and 10 m and height 4 m. What is its area?', '32 m²', ['64 m²', '240 m²', '20 m²'], '½(6 + 10) × 4 = 32.'),
           ('A parallelogram has base 9 cm, slant side 5 cm and perpendicular height 4 cm. What is its area?', '36 cm²', ['45 cm²', '20 cm²', '18 cm²'], 'Base × perpendicular height = 9 × 4.')],
    why=[('Explain why the area of a triangle is half the area of a rectangle with the same base and height.', 'Two copies of the triangle can be rearranged to fill a parallelogram (or rectangle) with that base and height.'),
         ('Explain why the slant side is not used when finding the area of a parallelogram.', 'Cutting a triangle from one end and moving it to the other makes a rectangle whose height is the perpendicular height, not the slant side.'),
         ('Explain where the formula ½(a + b)h for a trapezium comes from.', 'Two identical trapeziums, one rotated, form a parallelogram with base a + b and height h; one trapezium is half of it.')],
    misc=[('The area of a triangle with base 8 and height 6 is 48.', 'Area = ½ × base × height = 24; 48 is the rectangle.'),
          ('Area and perimeter are measured in the same units.', 'Perimeter is a length (cm), area is in square units (cm²).')],
))


@R.add('ch09-st1', 'C3', (1, 4), 'short')
def area_basic(rng, slot):
    shape = rng.choice(['tri', 'para', 'trap', 'rev_tri', 'rev_trap'])
    a, b, h = rng.randint(3, 20), rng.randint(3, 20), rng.randint(2, 15)
    u = rng.choice(['cm', 'm', 'mm'])
    if shape == 'tri':
        return short(f'Find the area of a triangle with base {a} {u} and perpendicular height {h} {u}.', f'{g(a * h / 2)} {u}²', f'½ × {a} × {h} (M1) = {g(a * h / 2)} {u}² (A1).', 2)
    if shape == 'para':
        return short(f'A parallelogram has base {a} {u}, slant side {h + 2} {u} and perpendicular height {h} {u}. Find its area.', f'{a * h} {u}²', f'Base × perpendicular height (M1) = {a * h} {u}² (A1).', 2)
    if shape == 'trap':
        return short(f'A trapezium has parallel sides of {a} {u} and {b} {u} and a height of {h} {u}. Find its area.', f'{g((a + b) * h / 2)} {u}²', f'½({a} + {b}) × {h} (M1) = {g((a + b) * h / 2)} {u}² (A1).', 2)
    if shape == 'rev_tri':
        A = a * h
        return short(f'A triangle has area {A} {u}² and base {2 * a} {u}. Find its perpendicular height.', f'{h} {u}', f'{A} = ½ × {2 * a} × h (M1); h = {h} {u} (A1).', 2)
    A = Fr((a + b) * h, 2)
    return short(f'A trapezium has area {g(float(A))} {u}² and parallel sides {a} {u} and {b} {u}. Find its height.', f'{h} {u}', f'{g(float(A))} = ½({a + b})h (M1); h = {h} {u} (A1).', 2)


@R.add('ch09-st1', 'C3', (2, 5), 'short')
def compound_area(rng, slot):
    W, H = rng.randint(8, 20), rng.randint(6, 16)
    w, h = rng.randint(2, W - 3), rng.randint(2, H - 3)
    kind = rng.choice(['L', 'house', 'cut'])
    if kind == 'L':
        A = W * H - w * h
        return short(f'An L-shaped room is a {W} m by {H} m rectangle with a {w} m by {h} m rectangle removed from one corner. Find the area of the floor and its perimeter.', f'area {A} m², perimeter {2 * (W + H)} m',
                     f'{W * H} − {w * h} (M1) = {A} m² (A1); perimeter equals that of the full rectangle, 2({W} + {H}) = {2 * (W + H)} m (A1).', 3)
    if kind == 'house':
        rh = rng.randint(2, 8)
        A = W * H + W * rh / 2
        return short(f'The end wall of a house is a rectangle {W} m wide and {H} m high with a triangular gable {rh} m high on top. Find the area of the wall.', f'{g(A)} m²',
                     f'Rectangle {W * H} (A1) + triangle ½ × {W} × {rh} = {g(W * rh / 2)} (A1); total {g(A)} m² (A1).', 3)
    r_ = rng.randint(1, min(w, h))
    A = W * H - r_ * r_ * 4
    return short(f'A rectangular card measuring {W} cm by {H} cm has a {r_} cm square cut from each corner. Find the area of the remaining card.', f'{A} cm²', f'{W * H} − 4 × {r_ * r_} (M1) = {A} cm² (A1).', 2)


@R.add('ch09-st1', 'C1', (1, 3), 'mcq')
def area_formula_mcq(rng, slot):
    shape = rng.choice(['trapezium', 'triangle', 'parallelogram'])
    corr = {'trapezium': '½(a + b)h', 'triangle': '½bh', 'parallelogram': 'bh'}[shape]
    return mcq(rng, f'Which formula gives the area of a {shape}?', corr, [f for f in ['½(a + b)h', '½bh', 'bh', '2(a + b)', '(a + b)h'] if f != corr][:3],
               f'Area of a {shape} = {corr}.')


@R.add('ch09-st1', 'C2', (2, 4), 'explain')
def area_explain(rng, slot):
    a, h = rng.randint(4, 15), rng.randint(3, 12)
    who = name(rng)
    kind = rng.choice(['double', 'same'])
    if kind == 'double':
        return explain(f'A triangle has base {a} cm and height {h} cm. {who} says doubling both the base and the height doubles the area. Explain whether this is true.',
                       f'False: area goes from {g(a * h / 2)} cm² to {g(2 * a * 2 * h / 2)} cm², four times as big, because both dimensions are doubled.',
                       'Both areas calculated (A1); scale factor 2 × 2 = 4 explained (R1).', 2, 'G2')
    return explain(f'Explain why all triangles with base {a} cm whose top vertex lies on a line parallel to the base, {h} cm above it, have the same area.',
                   f'They all have the same base {a} cm and the same perpendicular height {h} cm, so each area is ½ × {a} × {h} = {g(a * h / 2)} cm².',
                   'Same base and perpendicular height (R1); area value (A1).', 2)


@R.add('ch09-st1', 'C4', (3, 5), 'multi_step')
def area_task(rng, slot):
    city, country, cur, cname = place(rng)
    a, b, h = rng.randint(8, 20), rng.randint(4, 12), rng.randint(5, 14)
    price = Decimal(rng.randint(150, 900)) / 100
    pack = rng.choice([2, 2.5, 5])
    A = (a + b) * h / 2
    frames = [
        (f'A school garden in {city} is a trapezium with parallel sides {a} m and {b} m, {h} m apart. (a) Find its area. (b) Grass seed is sold in boxes covering {pack:g} m² for {cur}{price}. How many boxes are needed and what is the cost? (c) Suggest why the gardener might buy one extra box.',
         f'(a) {g(A)} m² (b) {math.ceil(A / pack)} boxes, {cur}{math.ceil(A / pack) * price:.2f} (c) to allow for wastage or uneven sowing'),
        (f'Investigate rectangles with perimeter {2 * (a + b)} cm and whole-number sides. (a) List the possible dimensions. (b) Find the area of each. (c) Describe the pattern and state which rectangle has the largest area.',
         f'(a) 1 × {a + b - 1} up to {(a + b) // 2} × {(a + b) - (a + b) // 2} (b) areas from {a + b - 1} to {((a + b) // 2) * ((a + b) - (a + b) // 2)} cm² (c) the closer to a square, the larger the area; largest {(a + b) // 2} × {(a + b) - (a + b) // 2}'),
    ]
    q_, ans = rng.choice(frames)
    return short(q_, ans, f'{ans}. Correct area formula (M1 A1); rounding up / pattern recognised (B or D: M1 A1); justified conclusion (R1).', 5, 'multi_step', 'G5')


R.facts('ch09-st2', F(
    terms=[('circumference', 'the perimeter of a circle: C = πd = 2πr'),
           ('radius', 'the distance from the centre of a circle to its edge'),
           ('diameter', 'a chord through the centre; twice the radius'),
           ('π (pi)', 'the ratio of any circle’s circumference to its diameter, approximately 3.14159')],
    facts=[('What is the circumference of a circle of diameter 10 cm (to 1 d.p.)?', '31.4 cm', ['78.5 cm', '15.7 cm', '314 cm'], 'C = π × 10.'),
           ('What is the area of a circle of radius 3 m (to 1 d.p.)?', '28.3 m²', ['18.8 m²', '9.4 m²', '113.1 m²'], 'A = π × 3².'),
           ('If the radius of a circle doubles, its area:', 'is multiplied by 4', ['doubles', 'is multiplied by 8', 'stays the same'], 'Area depends on r².')],
    why=[('Explain why π is the same for every circle.', 'All circles are similar (enlargements of each other), so circumference and diameter scale by the same factor and their ratio is constant.'),
         ('Explain how cutting a circle into thin sectors shows that its area is πr².', 'The sectors rearrange into an almost-rectangle with height r and length half the circumference, πr, so the area is πr × r = πr².'),
         ('Explain why the area of a semicircle is ½πr² but its perimeter is not ½ × 2πr.', 'The perimeter also includes the straight diameter, so it is πr + 2r.')],
    misc=[('The area of a circle of diameter 8 is π × 8² = 64π.', 'Use the radius: r = 4, A = π × 4² = 16π.'),
          ('The circumference of a circle of radius 5 is π × 5 = 15.7.', 'C = 2πr = 10π ≈ 31.4; πr uses the radius instead of the diameter.')],
))


@R.add('ch09-st2', 'C3', (1, 4), 'numerical')
def circle_calc(rng, slot):
    r_ = rng.randint(2, 30)
    use_d = rng.random() < 0.5
    kind = rng.choice(['C', 'A', 'revC', 'revA', 'semi'])
    given = f'diameter {2 * r_} cm' if use_d else f'radius {r_} cm'
    if kind == 'C':
        return short(f'Find the circumference of a circle with {given}, to 1 d.p.', f'{rnd(2 * math.pi * r_, 1)} cm', f'C = π × {2 * r_} (M1) = {rnd(2 * math.pi * r_, 1)} cm (A1).', 2, 'numerical')
    if kind == 'A':
        return short(f'Find the area of a circle with {given}, to 1 d.p.', f'{rnd(math.pi * r_ * r_, 1)} cm²', f'r = {r_} (A1 if diameter given); A = π × {r_}² (M1) = {rnd(math.pi * r_ * r_, 1)} cm² (A1).', 2, 'numerical')
    if kind == 'revC':
        C = rnd(2 * math.pi * r_, 2)
        return short(f'A circular track has circumference {C} m. Find its radius to the nearest metre.', f'{r_} m', f'r = C ÷ 2π (M1) = {rnd(float(C) / (2 * math.pi), 2)} ≈ {r_} m (A1).', 2, 'numerical')
    if kind == 'revA':
        A = rnd(math.pi * r_ * r_, 1)
        return short(f'A circular pond has an area of {A} m². Find its diameter, to the nearest metre.', f'{2 * r_} m', f'r² = {A} ÷ π (M1); r ≈ {r_} (A1); d = {2 * r_} m (A1).', 3, 'numerical')
    per = math.pi * r_ + 2 * r_
    return short(f'Find the perimeter and the area of a semicircle with radius {r_} cm, to 1 d.p.', f'perimeter {rnd(per, 1)} cm, area {rnd(math.pi * r_ * r_ / 2, 1)} cm²',
                 f'Arc πr = {rnd(math.pi * r_, 2)} plus diameter {2 * r_} (M1) = {rnd(per, 1)} cm (A1); ½πr² = {rnd(math.pi * r_ * r_ / 2, 1)} cm² (A1).', 3, 'numerical')


@R.add('ch09-st2', 'C3', (2, 5), 'numerical')
def circle_compound(rng, slot):
    a = rng.randint(4, 20)
    kind = rng.choice(['ring', 'square', 'track'])
    if kind == 'ring':
        r1, r2 = a, a + rng.randint(1, 6)
        A = math.pi * (r2 * r2 - r1 * r1)
        return short(f'A circular path of width {r2 - r1} m surrounds a circular lawn of radius {r1} m. Find the area of the path to 1 d.p.', f'{rnd(A, 1)} m²',
                     f'π({r2}² − {r1}²) (M1 A1) = {rnd(A, 1)} m² (A1).', 3, 'numerical')
    if kind == 'square':
        A = a * a - math.pi * (a / 2) ** 2
        return short(f'The largest possible circle is cut from a square sheet of metal of side {a} cm. Find the area of metal wasted, to 1 d.p.', f'{rnd(A, 1)} cm²',
                     f'Radius {a / 2:g} (A1); {a * a} − π({a / 2:g})² (M1) = {rnd(A, 1)} cm² (A1).', 3, 'numerical')
    L = rng.randint(60, 120)
    per = 2 * L + math.pi * 2 * a
    return short(f'A running track has two straight sections of {L} m joined by two semicircular ends of radius {a} m. Find the length of one lap to the nearest metre.', f'{rnd(per, 0)} m',
                 f'Two semicircles make one circle: 2π × {a} (M1); + 2 × {L} (M1); {rnd(per, 0)} m (A1).', 3, 'numerical')


@R.add('ch09-st2', 'C1', (1, 3), 'mcq')
def circle_mcq(rng, slot):
    r_ = rng.randint(2, 12)
    if rng.random() < 0.5:
        return mcq(rng, f'What is the exact area of a circle of radius {r_} cm?', f'{r_ * r_}π cm²', [f'{2 * r_}π cm²', f'{r_}π cm²', f'{4 * r_ * r_}π cm²'], f'πr² = {r_ * r_}π.')
    return mcq(rng, f'What is the exact circumference of a circle of radius {r_} cm?', f'{2 * r_}π cm', [f'{r_ * r_}π cm', f'{r_}π cm', f'{4 * r_}π cm'], f'2πr = {2 * r_}π.')


@R.add('ch09-st2', 'C2', (2, 4), 'explain')
def circle_explain(rng, slot):
    r_ = rng.randint(2, 10)
    k = rng.choice([2, 3])
    who = name(rng)
    kind = rng.choice(['scale', 'pi'])
    if kind == 'scale':
        return explain(f'{who} says that if the radius of a circular pizza is multiplied by {k}, there is {k} times as much pizza. Explain whether this is correct, using r = {r_} cm.',
                       f'Not correct: area {r_ * r_}π → {(k * r_) ** 2}π cm², {k * k} times as much, because area depends on r².',
                       'Both areas (A1); factor k² explained (R1).', 2, 'G2')
    C = rnd(2 * math.pi * r_ * 10, 1)
    return explain(f'{who} measures the circumference of a plate as {C} mm and its diameter as {20 * r_} mm. Explain what the ratio of these measurements should be and why.',
                   f'{C} ÷ {20 * r_} ≈ {rnd(float(C) / (20 * r_), 3)} ≈ π, because circumference = π × diameter for every circle.',
                   'Ratio calculated (A1); link to π (R1).', 2)


@R.add('ch09-st2', 'C4', (3, 5), 'multi_step')
def circle_task(rng, slot):
    city, country, cur, cname = place(rng)
    d = Decimal(rng.randint(50, 80)) / 100
    dist = rng.randint(2, 10)
    r_ = rng.randint(3, 12)
    price = rng.randint(15, 60)
    frames = [
        (f'A bicycle wheel in {city} has a diameter of {d} m. (a) Find its circumference to 3 s.f. (b) How many complete turns does it make on a {dist} km ride? (c) Explain one reason why the real number of turns may differ.',
         f'(a) {rsf(math.pi * float(d), 3)} m (b) {int(dist * 1000 // (math.pi * float(d)))} complete turns (c) tyre pressure/wear changes the effective diameter; the path is not perfectly straight'),
        (f'A circular fountain of radius {r_} m is surrounded by a paved ring 1.5 m wide. (a) Find the area of the paved ring to 1 d.p. (b) Paving costs {cur}{price} per m². Find the cost. (c) A low fence goes around the outer edge – find its length.',
         f'(a) {rnd(math.pi * ((r_ + 1.5) ** 2 - r_ * r_), 1)} m² (b) {cur}{rnd(math.pi * ((r_ + 1.5) ** 2 - r_ * r_) * price, 2)} (c) {rnd(2 * math.pi * (r_ + 1.5), 1)} m'),
    ]
    q_, ans = rng.choice(frames)
    return short(q_, ans, f'{ans}. Correct circle formulae (M1 A1); multi-step calculation (M1 A1); interpretation / limitation in context (D: R1).', 5, 'multi_step', 'G5')


R.facts('ch09-st3', F(
    terms=[('surface area', 'the total area of all the faces (surfaces) of a 3D shape'),
           ('net', 'a 2D pattern that folds to make a 3D shape'),
           ('prism', 'a 3D shape with the same cross-section all along its length'),
           ('curved surface area of a cylinder', 'the area of the rectangle that wraps around it: 2πrh')],
    facts=[('What is the surface area of a cube of side 4 cm?', '96 cm²', ['64 cm²', '16 cm²', '48 cm²'], '6 × 4² = 96.'),
           ('Which is the total surface area of a closed cylinder?', '2πr² + 2πrh', ['πr²h', '2πrh', 'πr² + 2πrh'], 'Two circles plus the curved surface.'),
           ('A cuboid is 5 × 3 × 2 cm. What is its surface area?', '62 cm²', ['30 cm²', '31 cm²', '60 cm²'], '2(15 + 10 + 6) = 62.')],
    why=[('Explain why the curved surface of a cylinder has area 2πrh.', 'Unrolled, it is a rectangle whose width is the height h and whose length is the circumference 2πr.'),
         ('Explain why a net helps you find the surface area of a prism.', 'The net shows every face flattened out, so you can find each face area and add them without missing or double-counting.'),
         ('Explain why an open-topped box needs less material than a closed one of the same size.', 'One face (the top) is missing, so its area is subtracted from the total surface area.')],
    misc=[('The surface area of a cuboid 4 × 3 × 2 is 4 × 3 × 2 = 24.', 'That is the volume. Surface area = 2(12 + 8 + 6) = 52.'),
          ('The surface area of a closed cylinder is 2πrh.', 'That is only the curved surface; add the two circular ends 2πr².')],
))


@R.add('ch09-st3', 'C3', (1, 4), 'numerical')
def sa_prism(rng, slot):
    l, w, h = rng.randint(2, 15), rng.randint(2, 12), rng.randint(2, 10)
    kind = rng.choice(['cuboid', 'open', 'tri'])
    if kind == 'cuboid' or slot.d <= 1:
        sa = 2 * (l * w + l * h + w * h)
        return short(f'Find the total surface area of a cuboid measuring {l} cm by {w} cm by {h} cm.', f'{sa} cm²', f'2({l * w} + {l * h} + {w * h}) (M1 A1) = {sa} cm² (A1).', 3, 'numerical')
    if kind == 'open':
        sa = l * w + 2 * (l * h + w * h)
        return short(f'An open-topped box is {l} cm long, {w} cm wide and {h} cm high. Find the area of card needed to make it.', f'{sa} cm²',
                     f'Base {l * w} (A1); four sides 2({l * h} + {w * h}) (M1); total {sa} cm² (A1).', 3, 'numerical')
    a, b, c = rng.choice(TRIPLES[:4])
    L = rng.randint(5, 20)
    sa = a * b + (a + b + c) * L
    return short(f'A triangular prism has a right-angled triangle cross-section with sides {a} cm, {b} cm and {c} cm, and length {L} cm. Find its total surface area.', f'{sa} cm²',
                 f'Two triangles 2 × ½ × {a} × {b} = {a * b} (A1); three rectangles ({a} + {b} + {c}) × {L} = {(a + b + c) * L} (M1 A1); total {sa} cm² (A1).', 4, 'numerical')


@R.add('ch09-st3', 'C3', (2, 5), 'numerical')
def sa_cyl(rng, slot):
    r_, h = rng.randint(2, 15), rng.randint(3, 30)
    kind = rng.choice(['closed', 'curved', 'open'])
    if kind == 'closed':
        sa = 2 * math.pi * r_ * r_ + 2 * math.pi * r_ * h
        return short(f'Find the total surface area of a closed cylinder with radius {r_} cm and height {h} cm, to 3 s.f.', f'{rsf(sa, 3)} cm²',
                     f'2πr² = {rsf(2 * math.pi * r_ * r_, 4)} (A1); 2πrh = {rsf(2 * math.pi * r_ * h, 4)} (A1); total {rsf(sa, 3)} cm² (A1).', 3, 'numerical')
    if kind == 'curved':
        sa = 2 * math.pi * r_ * h
        return short(f'A label wraps exactly once around a can of radius {r_} cm and height {h} cm, with no overlap. Find the area of the label to 1 d.p.', f'{rnd(sa, 1)} cm²',
                     f'Curved surface 2πrh (M1) = {rnd(sa, 1)} cm² (A1).', 2, 'numerical')
    sa = math.pi * r_ * r_ + 2 * math.pi * r_ * h
    return short(f'A cylindrical plant pot (open at the top) has diameter {2 * r_} cm and height {h} cm. Find its outside surface area to 3 s.f.', f'{rsf(sa, 3)} cm²',
                 f'One base πr² (A1) + curved 2πrh (A1); total {rsf(sa, 3)} cm² (A1).', 3, 'numerical')


@R.add('ch09-st3', 'C1', (1, 3), 'mcq')
def sa_mcq(rng, slot):
    s = rng.randint(2, 12)
    return mcq(rng, f'What is the surface area of a cube with edges of {s} cm?', f'{6 * s * s} cm²', [f'{s ** 3} cm²', f'{4 * s * s} cm²', f'{12 * s} cm²'], f'6 faces × {s}² = {6 * s * s}.')


@R.add('ch09-st3', 'C2', (2, 4), 'explain')
def sa_explain(rng, slot):
    s = rng.randint(2, 9)
    who = name(rng)
    kind = rng.choice(['double', 'cubes'])
    if kind == 'double':
        return explain(f'{who} doubles every edge of a cube of side {s} cm. Explain how the surface area changes.', f'{6 * s * s} cm² → {24 * s * s} cm²: four times as big, because each face area is multiplied by 2² = 4.',
                       'Both surface areas (A1); scale factor squared (R1).', 2)
    return explain(f'Two cubes of side {s} cm are glued face to face to make a cuboid. Explain why the surface area of the cuboid is not twice the surface area of one cube, and find it.',
                   f'Two faces are hidden where they join: 2 × {6 * s * s} − 2 × {s * s} = {10 * s * s} cm².',
                   'Hidden faces identified (R1); correct area (A1).', 2)


@R.add('ch09-st3', 'C4', (3, 5), 'multi_step')
def sa_task(rng, slot):
    city, country, cur, cname = place(rng)
    r_, h = rng.randint(3, 8), rng.randint(8, 20)
    l, w, hh = rng.randint(20, 60), rng.randint(15, 40), rng.randint(10, 30)
    price = Decimal(rng.randint(2, 15)) / 10
    frames = [
        (f'A company in {city} sells drinks in cylindrical cans of radius {r_} cm and height {h} cm. (a) Find the area of aluminium in one closed can. (b) A designer suggests a can of radius {r_ + 1} cm and height {h - 4} cm. Compare the material needed. (c) Give one reason, other than material, why a company might choose a particular can shape.',
         f'(a) {rsf(2 * math.pi * r_ * (r_ + h), 3)} cm² (b) {rsf(2 * math.pi * (r_ + 1) * (r_ + 1 + h - 4), 3)} cm²; ' +
         ('the new can uses less' if (r_ + 1) * (r_ + 1 + h - 4) < r_ * (r_ + h) else 'the new can uses more') + ' (c) e.g. comfortable to hold, fits standard machines, stacks well'),
        (f'A storage box {l} cm × {w} cm × {hh} cm is to be covered in fabric costing {cur}{price:.2f} per 100 cm², including the lid. (a) Find the surface area. (b) Find the cost. (c) If the box had no lid, how much would be saved?',
         f'(a) {2 * (l * w + l * hh + w * hh)} cm² (b) {cur}{rnd(Decimal(2 * (l * w + l * hh + w * hh)) * price / 100, 2)} (c) {cur}{rnd(Decimal(l * w) * price / 100, 2)}'),
    ]
    q_, ans = rng.choice(frames)
    return short(q_, ans, f'{ans}. Correct faces identified (M1); surface areas calculated (A1 A1); comparison/cost (M1 A1); reasoned comment (D: R1).', 6, 'multi_step', 'G5')


R.facts('ch09-st4', F(
    terms=[('volume', 'the amount of space a 3D shape occupies, measured in cubic units'),
           ('cross-section', 'the 2D shape you see when a solid is sliced; for a prism it is the same all the way along'),
           ('capacity', 'the amount a container can hold, often measured in litres (1 L = 1000 cm³)')],
    facts=[('What is the volume of a cuboid 6 cm × 4 cm × 5 cm?', '120 cm³', ['30 cm³', '148 cm³', '15 cm³'], '6 × 4 × 5 = 120.'),
           ('Which formula gives the volume of a cylinder?', 'πr²h', ['2πrh', '2πr²h', '⅓πr²h'], 'Area of circular cross-section × height.'),
           ('A prism has cross-section area 12 cm² and length 10 cm. What is its volume?', '120 cm³', ['22 cm³', '1200 cm³', '60 cm³'], 'Volume = cross-section × length.')],
    why=[('Explain why the volume of any prism is the area of its cross-section times its length.', 'A prism is a stack of identical thin slices with the cross-section shape; adding them over the length gives area × length.'),
         ('Explain why volume is measured in cubic units.', 'Volume counts how many unit cubes (1 × 1 × 1) fill the solid, so the unit is length³.'),
         ('Explain why doubling the radius of a cylinder multiplies its volume by 4 but doubling its height only doubles it.', 'V = πr²h: r is squared, so ×2 gives ×4, while h appears once.')],
    misc=[('A cylinder with radius 3 and height 5 has volume π × 3 × 5.', 'The radius is squared: π × 3² × 5 = 45π.'),
          ('1 litre = 100 cm³.', '1 litre = 1000 cm³ (a 10 cm cube).')],
))


@R.add('ch09-st4', 'C3', (1, 4), 'numerical')
def volume_prism(rng, slot):
    kind = rng.choice(['cuboid', 'tri', 'trap', 'rev'])
    l, w, h = rng.randint(2, 20), rng.randint(2, 15), rng.randint(2, 12)
    if kind == 'cuboid' or slot.d <= 1:
        return short(f'Find the volume of a cuboid {l} cm long, {w} cm wide and {h} cm high.', f'{l * w * h} cm³', f'{l} × {w} × {h} (M1) = {l * w * h} cm³ (A1).', 2, 'numerical')
    if kind == 'tri':
        V = Fr(w * h, 2) * l
        return short(f'A triangular prism has a triangular cross-section with base {w} cm and height {h} cm, and length {l} cm. Find its volume.', f'{g(float(V))} cm³',
                     f'Cross-section ½ × {w} × {h} = {g(w * h / 2)} (A1); × {l} (M1) = {g(float(V))} cm³ (A1).', 3, 'numerical')
    if kind == 'trap':
        a, b = rng.randint(2, 10), rng.randint(3, 12)
        V = Fr((a + b) * h, 2) * l
        return short(f'A water trough is a prism with a trapezium cross-section: parallel sides {a} dm and {b} dm, depth {h} dm, and length {l} dm. Find its capacity in litres (1 dm³ = 1 L).', f'{g(float(V))} litres',
                     f'Cross-section ½({a} + {b}) × {h} = {g((a + b) * h / 2)} dm² (A1); × {l} = {g(float(V))} dm³ (M1) = {g(float(V))} L (A1).', 3, 'numerical')
    V = l * w * h
    return short(f'A cuboid has volume {V} cm³, length {l} cm and width {w} cm. Find its height.', f'{h} cm', f'{V} = {l} × {w} × h (M1); h = {h} cm (A1).', 2, 'numerical')


@R.add('ch09-st4', 'C3', (2, 5), 'numerical')
def volume_cyl(rng, slot):
    r_, h = rng.randint(2, 15), rng.randint(3, 30)
    kind = rng.choice(['V', 'litres', 'rev'])
    V = math.pi * r_ * r_ * h
    if kind == 'V':
        return short(f'Find the volume of a cylinder with radius {r_} cm and height {h} cm, to 3 s.f.', f'{rsf(V, 3)} cm³', f'π × {r_}² × {h} (M1) = {rsf(V, 3)} cm³ (A1).', 2, 'numerical')
    if kind == 'litres':
        return short(f'A cylindrical water tank has diameter {2 * r_ * 10} cm and height {h * 10} cm. How many litres does it hold, to the nearest litre?', f'{rnd(V, 0)} litres',
                     f'V = π × {r_ * 10}² × {h * 10} = {rsf(V * 1000, 4)} cm³ (M1 A1); ÷ 1000 = {rnd(V, 0)} L (A1).', 3, 'numerical')
    Vr = rnd(V, 1)
    return short(f'A cylinder has volume {Vr} cm³ and radius {r_} cm. Find its height to the nearest cm.', f'{h} cm', f'h = V ÷ πr² = {Vr} ÷ (π × {r_ * r_}) (M1) ≈ {h} cm (A1).', 2, 'numerical')


@R.add('ch09-st4', 'C1', (1, 3), 'mcq')
def volume_mcq(rng, slot):
    l, w, h = rng.randint(2, 10), rng.randint(2, 10), rng.randint(2, 10)
    V = l * w * h
    return mcq(rng, f'A cuboid measures {l} cm × {w} cm × {h} cm. What is its volume?', f'{V} cm³', [f'{2 * (l * w + l * h + w * h)} cm³', f'{l + w + h} cm³', f'{l * w} cm³'],
               f'{l} × {w} × {h} = {V} cm³.')


@R.add('ch09-st4', 'C2', (2, 4), 'explain')
def volume_explain(rng, slot):
    r_, h = rng.randint(2, 8), rng.randint(4, 15)
    who = name(rng)
    kind = rng.choice(['compare', 'cube'])
    if kind == 'compare':
        V1 = math.pi * r_ * r_ * (2 * h)
        V2 = math.pi * (2 * r_) ** 2 * h
        return explain(f'{who} has two cylinders: A has radius {r_} cm and height {2 * h} cm; B has radius {2 * r_} cm and height {h} cm. Explain which holds more, and how many times as much.',
                       f'A: {2 * r_ * r_ * h}π ≈ {rsf(V1, 3)} cm³; B: {4 * r_ * r_ * h}π ≈ {rsf(V2, 3)} cm³. B holds twice as much, because doubling the radius multiplies the volume by 4.',
                       'Both volumes (A1); comparison explained via r² (R1).', 3)
    s = rng.randint(2, 6)
    return explain(f'Explain why a cube of side {s * 10} cm has a volume of {s ** 3} litres.', f'{s * 10}³ = {(s * 10) ** 3} cm³ and 1 L = 1000 cm³, so {(s * 10) ** 3} ÷ 1000 = {s ** 3} L.',
                   'Volume in cm³ (A1); conversion explained (R1).', 2)


@R.add('ch09-st4', 'C4', (3, 5), 'multi_step')
def volume_task(rng, slot):
    city, country, cur, cname = place(rng)
    l, w, d = rng.randint(15, 30), rng.randint(6, 12), Decimal(rng.randint(12, 20)) / 10
    rate = rng.randint(200, 600)
    r_, h = rng.randint(3, 6), rng.randint(10, 18)
    cube = rng.randint(4, 8)
    frames = [
        (f'A swimming pool in {city} is {l} m long, {w} m wide and has a constant depth of {d} m. (a) Find its volume in m³ and in litres. (b) It is filled at {rate} litres per minute. How long does it take, in hours and minutes? (c) Why might the real time be different?',
         None),
        (f'Sugar cubes of side 1 cm are packed into a box {cube} cm × {cube} cm × {cube + 2} cm. (a) How many cubes fit? (b) The sugar is then poured into a cylindrical jar of radius {r_} cm and height {h} cm. Will it fit? (c) Explain why the sugar takes up less space when poured.',
         f'(a) {cube * cube * (cube + 2)} (b) jar volume {rsf(math.pi * r_ * r_ * h, 3)} cm³ ' + ('≥' if math.pi * r_ * r_ * h >= cube * cube * (cube + 2) else '<') + f' {cube * cube * (cube + 2)} cm³: ' + ('yes' if math.pi * r_ * r_ * h >= cube * cube * (cube + 2) else 'no') + ' (c) loose sugar can fill gaps, but the total volume of the sugar itself stays the same'),
    ]
    q_, ans = rng.choice(frames)
    if ans is None:
        V = Decimal(l * w) * d
        L_ = V * 1000
        mins = math.ceil(L_ / rate)
        ans = f'(a) {_plain(V)} m³ = {_plain(L_)} litres (b) {mins // 60} h {mins % 60} min (rounding up) (c) the flow rate may vary; pools are not usually filled to the brim'
    return short(q_, ans, f'{ans}. Volume calculated (M1 A1); unit conversion (A1); rate/comparison (M1 A1); interpretation (D: R1).', 6, 'multi_step', 'G5')


R.facts('ch09-st5', F(
    terms=[('square centimetre', 'the area of a square with side 1 cm; 1 cm² = 100 mm²'),
           ('cubic centimetre', 'the volume of a cube with edge 1 cm; 1 cm³ = 1000 mm³ = 1 mL'),
           ('hectare', 'a unit of land area equal to 10 000 m²')],
    facts=[('How many cm² are in 1 m²?', '10 000', ['100', '1000', '1 000 000'], '1 m² = 100 cm × 100 cm.'),
           ('How many cm³ are in 1 m³?', '1 000 000', ['1000', '100', '10 000'], '100 × 100 × 100.'),
           ('2.5 litres is how many cm³?', '2500', ['250', '25', '25 000'], '1 L = 1000 cm³.')],
    why=[('Explain why 1 m² is not equal to 100 cm².', 'A 1 m square is 100 cm by 100 cm, so its area is 100 × 100 = 10 000 cm²; both dimensions are converted.'),
         ('Explain why you multiply by 1000 to change m³ to litres.', '1 m³ = 100 × 100 × 100 cm³ = 1 000 000 cm³ and 1 L = 1000 cm³, so 1 m³ = 1000 L.'),
         ('Explain how the conversion factor for volume is related to the one for length.', 'Volume has three dimensions, so the length factor is cubed: 10 mm = 1 cm gives 10³ = 1000 mm³ = 1 cm³.')],
    misc=[('5 m² = 500 cm².', '1 m² = 10 000 cm², so 5 m² = 50 000 cm².'),
          ('3 cm³ = 30 mm³.', '1 cm³ = 1000 mm³, so 3 cm³ = 3000 mm³.')],
))

UNITS = [('m', 'cm', 100), ('cm', 'mm', 10), ('km', 'm', 1000), ('m', 'mm', 1000)]


@R.add('ch09-st5', 'C3', (1, 4), 'short')
def convert_units(rng, slot):
    big, small, k = rng.choice(UNITS)
    dim = rng.choice([1, 2, 3] if slot.d >= 2 else [1, 2])
    if dim == 3 and k == 1000 and big == 'km':
        dim = 2
    v = Decimal(rng.randint(2, 95)) / Decimal(rng.choice([1, 10]))
    f_ = Decimal(k) ** dim
    sup_ = {1: '', 2: '²', 3: '³'}[dim]
    if rng.random() < 0.5:
        res = v * f_
        return short(f'Convert {v} {big}{sup_} to {small}{sup_}.', f'{_plain(res)} {small}{sup_}', f'1 {big}{sup_} = {_plain(f_)} {small}{sup_} (M1); {_plain(res)} {small}{sup_} (A1).', 2)
    w_ = v * f_ / Decimal(rng.choice([10, 100]))
    res = w_ / f_
    return short(f'Convert {_plain(w_)} {small}{sup_} to {big}{sup_}.', f'{_plain(res)} {big}{sup_}', f'Divide by {_plain(f_)} (M1); {_plain(res)} {big}{sup_} (A1).', 2)


@R.add('ch09-st5', 'C3', (2, 4), 'short')
def capacity_convert(rng, slot):
    a, b, c = rng.randint(10, 80), rng.randint(10, 60), rng.randint(5, 50)
    kind = rng.choice(['L', 'mL', 'ha'])
    if kind == 'L':
        V = a * b * c
        return short(f'A fish tank measures {a} cm × {b} cm × {c} cm. Find its capacity in litres.', f'{_plain(Decimal(V) / 1000)} L', f'{V} cm³ (A1); ÷ 1000 (M1) = {_plain(Decimal(V) / 1000)} L (A1).', 3)
    if kind == 'mL':
        v = Decimal(rng.randint(2, 40)) / 10
        return short(f'How many 250 mL glasses can be filled from a {v} litre jug?', f'{int(v * 1000 // 250)} glasses', f'{v} L = {int(v * 1000)} mL (M1); ÷ 250 = {v * 1000 / 250:g}, so {int(v * 1000 // 250)} full glasses (A1).', 2)
    L, W = a * 10, b * 10
    return short(f'A farm field is a rectangle {L} m by {W} m. Find its area in m² and in hectares.', f'{L * W} m² = {_plain(Decimal(L * W) / 10000)} ha', f'{L} × {W} = {L * W} m² (A1); ÷ 10 000 (M1) = {_plain(Decimal(L * W) / 10000)} ha (A1).', 3)


@R.add('ch09-st5', 'C1', (1, 3), 'mcq')
def units_mcq(rng, slot):
    big, small, k = rng.choice(UNITS[:2])
    dim = rng.choice([2, 3])
    sup_ = '²' if dim == 2 else '³'
    corr = _plain(Decimal(k) ** dim)
    w = [_plain(Decimal(k)), _plain(Decimal(k) ** (5 - dim)) if dim == 2 else _plain(Decimal(k) ** 2), _plain(Decimal(k) * dim)]
    return mcq(rng, f'How many {small}{sup_} are in 1 {big}{sup_}?', corr, w, f'1 {big} = {k} {small}, so 1 {big}{sup_} = {k}{sup(dim)} = {corr} {small}{sup_}.')


@R.add('ch09-st5', 'C2', (2, 4), 'explain')
def units_explain(rng, slot):
    v = rng.randint(2, 9)
    who = name(rng)
    return explain(f'{who} says {v} m² = {v * 100} cm² because there are 100 cm in a metre. Explain the error, using a diagram of a 1 m square, and give the correct value.',
                   f'A 1 m square is 100 cm × 100 cm = 10 000 cm², so {v} m² = {v * 10000:_} cm²'.replace('_', ' ') + '; both dimensions must be converted.',
                   'Square diagram reasoning (R1); correct factor 10 000 (A1); value (A1).', 3, 'G2')


@R.add('ch09-st5', 'C4', (3, 5), 'multi_step')
def units_task(rng, slot):
    city, country, cur, cname = place(rng)
    L, W = rng.randint(3, 9), rng.randint(2, 6)
    tile = rng.choice([20, 25, 30, 40, 50])
    price = Decimal(rng.randint(150, 600)) / 100
    roof = rng.randint(40, 200)
    rain = rng.randint(5, 30)
    frames = [
        (f'A kitchen floor in {city} is {L} m by {W} m. Square tiles are {tile} cm by {tile} cm and cost {cur}{price} each. (a) Find the floor area in cm². (b) How many tiles are needed? (c) Find the cost. (d) Explain why converting to the same units first matters.',
         f'(a) {L * W * 10000:_} cm² (b) {math.ceil(L * 100 / tile) * math.ceil(W * 100 / tile)} tiles (c) {cur}{math.ceil(L * 100 / tile) * math.ceil(W * 100 / tile) * price:.2f} (d) areas in m² and cm² differ by a factor of 10 000, so mixing them gives answers that are wrong by that factor'.replace('_', ' ')),
        (f'A roof in {city} has a horizontal area of {roof} m². During a storm {rain} mm of rain falls. (a) Convert {rain} mm to metres. (b) Find the volume of water that falls on the roof in m³. (c) How many litres is that? (d) How many 200-litre barrels would it fill?',
         f'(a) {rain / 1000:g} m (b) {g(roof * rain / 1000, 4)} m³ (c) {roof * rain} L (d) {roof * rain // 200} full barrels'),
    ]
    q_, ans = rng.choice(frames)
    return short(q_, ans, f'{ans}. Consistent units (M1 A1); area/volume calculation (M1 A1); practical rounding and explanation (D: R1).', 6, 'multi_step', 'G5')


# =============================================================================================
# ch10 Transformations and Symmetry
# =============================================================================================
SHAPES_SYM = [('square', 4, 4), ('rectangle (not a square)', 2, 2), ('rhombus (not a square)', 2, 2), ('parallelogram (not a rectangle or rhombus)', 0, 2),
              ('kite', 1, 1), ('isosceles trapezium', 1, 1), ('equilateral triangle', 3, 3), ('isosceles triangle (not equilateral)', 1, 1),
              ('scalene triangle', 0, 1), ('circle', 'infinitely many', 'infinite')]

def _ln(L):
    return '1 line' if L == 1 else f'{L} lines'


R.facts('ch10-st1', F(
    terms=[('line of symmetry', 'a line that divides a shape into two halves that are mirror images of each other'),
           ('rotational symmetry', 'a shape has rotational symmetry if it looks the same after a rotation of less than 360° about its centre'),
           ('order of rotational symmetry', 'the number of times a shape looks the same during one full turn')],
    facts=[('How many lines of symmetry does a regular hexagon have?', '6', ['3', '12', '2'], 'A regular n-gon has n lines of symmetry.'),
           ('What is the order of rotational symmetry of a parallelogram?', '2', ['0', '1', '4'], 'It looks the same after a half turn.'),
           ('Which letter has rotational symmetry of order 2 but no line of symmetry?', 'S', ['A', 'H', 'T'], 'S looks the same after a half turn but cannot be folded onto itself.')],
    why=[('Explain why every shape has rotational symmetry of at least order 1.', 'Every shape looks the same after a full 360° turn, so the count is at least 1; "no rotational symmetry" means order 1.'),
         ('Explain why a parallelogram has no lines of symmetry even though it has rotational symmetry.', 'Folding along a diagonal or a midline does not make the halves match, but a half-turn about the centre maps it onto itself.'),
         ('Explain the link between the number of sides of a regular polygon and its symmetry.', 'A regular n-gon has n equal sides and angles, so it has n lines of symmetry and rotational symmetry of order n (it matches every 360°/n).')],
    misc=[('A rectangle has 4 lines of symmetry because it has 4 sides.', 'Only the two lines through the midpoints of opposite sides work; the diagonals are not lines of symmetry.'),
          ('A shape with no rotational symmetry has order 0.', 'The order is at least 1, because every shape fits onto itself after a full turn.')],
))


@R.add('ch10-st1', 'C3', (1, 3), 'short')
def symmetry_shape(rng, slot):
    if rng.random() < 0.5:
        nm, L, O = rng.choice(SHAPES_SYM)
        return short(f'State the number of lines of symmetry and the order of rotational symmetry of a {nm}.', f'{_ln(L)}; order {O}', f'Lines: {L} (A1); order {O} (A1).', 2)
    n = rng.randint(5, 12)
    return short(f'A regular polygon has {n} sides. State its number of lines of symmetry, its order of rotational symmetry, and the smallest angle of rotation that maps it onto itself.',
                 f'{n} lines; order {n}; {g(360 / n, 4)}°', f'{n} lines (A1); order {n} (A1); 360 ÷ {n} = {g(360 / n, 4)}° (A1).', 3)


@R.add('ch10-st1', 'C3', (2, 4), 'short')
def symmetry_grid(rng, slot):
    n = rng.choice([3, 4, 5, 6, 8])
    k = rng.randint(1, n - 1)
    who = name(rng)
    kind = rng.choice(['flag', 'complete'])
    if kind == 'flag':
        return short(f'A logo is made of {n} identical petals arranged evenly around a centre, each petal itself symmetric about the line through the centre. Find the order of rotational symmetry and the number of lines of symmetry.',
                     f'order {n}; {n} lines', f'Each petal maps to the next every {g(360 / n, 4)}° (R1): order {n} (A1); lines through each petal’s centre line ({n}) (A1).', 3)
    return short(f'{who} shades {k} of the {n} identical sectors of a circle cut into {n} equal sectors, all next to each other. State the order of rotational symmetry and the number of lines of symmetry of the pattern.',
                 f'order 1; 1 line', f'Shaded block of adjacent sectors only repeats after a full turn (R1): order 1 (A1); one line through the middle of the block (A1).', 3)


@R.add('ch10-st1', 'C1', (1, 3), 'mcq')
def symmetry_mcq(rng, slot):
    nm, L, O = rng.choice(SHAPES_SYM[:9])
    corr = f'{_ln(L)}, order {O}'
    pool = sorted({f'{_ln(a)}, order {b}' for _, a, b in SHAPES_SYM[:9]} | {'3 lines, order 1', '1 line, order 2', '4 lines, order 2'})
    pool = [p for p in pool if p != corr]
    rng.shuffle(pool)
    return mcq(rng, f'Which describes the symmetry of a {nm}?', corr, pool[:3], f'A {nm} has {_ln(L)} of symmetry and rotational symmetry of order {O}.')


@R.add('ch10-st1', 'C2', (2, 4), 'explain')
def symmetry_explain(rng, slot):
    n = rng.randint(5, 10)
    who = name(rng)
    kind = rng.choice(['reg', 'square'])
    if kind == 'reg':
        return explain(f'{who} says a regular {n}-sided polygon has rotational symmetry of order {n} because it fits onto itself every {g(360 / n, 4)}°. Explain why this reasoning is correct.',
                       f'All sides and angles are equal, so turning through 360° ÷ {n} = {g(360 / n, 4)}° takes each vertex to the next; this happens {n} times in a full turn.',
                       'Equal sides/angles (R1); angle 360/n and count (R1).', 2)
    return explain(f'Explain why the diagonals of a square are lines of symmetry but the diagonals of a rectangle (that is not a square) are not.',
                   'Folding a square along a diagonal matches equal adjacent sides; in a rectangle the adjacent sides have different lengths, so the halves do not match.',
                   'Square: equal adjacent sides (R1); rectangle: unequal sides (R1).', 2)


@R.add('ch10-st1', 'C4', (3, 5), 'multi_step')
def symmetry_investigate(rng, slot):
    city = rng.choice(CITIES)
    who = name(rng)
    kind = rng.choice(['table', 'hubcap', 'pinwheel', 'star'])
    if kind == 'table':
        k = rng.randint(7, 24)
        ans = f'(a) 3, 3; 4, 4; 5, 5; 6, 6 (b) a regular n-gon has n lines of symmetry and rotational symmetry of order n (c) {k} lines, order {k}, smallest angle {g(360 / k, 4)}°'
        q_ = (f'{who} investigates the symmetry of regular polygons. (a) Complete a table for the equilateral triangle, square, regular pentagon and regular hexagon showing the number of lines of symmetry and the order of rotational symmetry. '
              f'(b) Describe the pattern in words. (c) Predict the symmetry of a regular {k}-gon and the smallest angle of rotation that maps it onto itself.')
    elif kind == 'hubcap':
        n = rng.choice([6, 8, 10, 12])
        ans = f'(a) {g(360 / n, 4)}° (b) order {n}, {n} lines (c) order {n // 2}, {n // 2} lines; the colours only repeat every {g(720 / n, 4)}°'
        q_ = (f'A car-parts firm in {city} designs a wheel hubcap with {n} identical, evenly spaced spokes, each symmetric about its own centre line. (a) Find the angle between neighbouring spokes. '
              f'(b) State the order of rotational symmetry and the number of lines of symmetry. (c) The spokes are then painted alternately red and silver. Find the new order and number of lines, and explain the change.')
    elif kind == 'pinwheel':
        k = rng.randint(3, 8)
        angs = ', '.join(f'{g(360 * i / k, 4)}°' for i in range(1, k + 1))
        ans = f'(a) {k} identical arms, each turned {g(360 / k, 4)}° from the last (b) 0 lines – the arms are bent the same way, so no fold matches them (c) {angs}'
        q_ = (f'A design student in {city} wants a pinwheel logo with rotational symmetry of order {k} but no lines of symmetry. (a) Describe how many identical arms are needed and how they are placed. '
              f'(b) Explain why the logo has no lines of symmetry. (c) List every angle of rotation between 0° and 360° (inclusive) that maps the logo onto itself.')
    else:
        p = rng.randint(5, 12)
        ans = f'(a) {p} lines (b) order {p} (c) {g(360 / p, 4)}° (d) yes – each point maps onto the next after {g(360 / p, 4)}°, the same as for a regular {p}-gon'
        q_ = (f'A festival banner in {city} shows a regular star with {p} points. (a) State the number of lines of symmetry. (b) State the order of rotational symmetry. '
              f'(c) Find the angle at the centre between two neighbouring points. (d) Does the star have the same symmetry as a regular {p}-sided polygon? Justify your answer.')
    return short(q_, ans, f'{ans}. Symmetry correctly identified (A1 A1); pattern or design justified (B: R1); angles stated with correct notation (C1).', 4, 'multi_step', 'G5')


R.facts('ch10-st2', F(
    terms=[('translation', 'a transformation that slides every point of a shape the same distance in the same direction'),
           ('column vector', 'a vector (a over b) that describes a translation: a units right (left if negative) and b units up (down if negative)'),
           ('reflection', 'a transformation that flips a shape over a mirror line; each point and its image are the same distance from the line'),
           ('image', 'the shape (or point) produced by a transformation; the original is the object')],
    facts=[('The point (3, −2) is translated by the column vector (−5 over 4). What is its image?', '(−2, 2)', ['(8, −6)', '(−2, −6)', '(−15, −8)'], 'Add the components: 3 − 5 = −2, −2 + 4 = 2.'),
           ('What is the image of (4, 7) after reflection in the x-axis?', '(4, −7)', ['(−4, 7)', '(7, 4)', '(−4, −7)'], 'Reflection in the x-axis changes the sign of y.'),
           ('What is the image of (2, 5) after reflection in the line y = x?', '(5, 2)', ['(−2, 5)', '(2, −5)', '(−5, −2)'], 'Reflection in y = x swaps the coordinates.')],
    why=[('Explain why a translated shape is congruent to the original shape.', 'Every point moves by the same vector, so all lengths and angles stay the same; only the position changes.'),
         ('Explain why the mirror line is the perpendicular bisector of the line joining a point and its reflection.', 'A point and its image are the same distance from the mirror line on opposite sides, and the line joining them crosses the mirror at 90°.'),
         ('Explain why a reflection changes the orientation of a shape but a translation does not.', 'A reflection flips the shape over, so the order of vertices (clockwise/anticlockwise) is reversed; a translation only slides it.')],
    misc=[('The column vector (3 over −2) means 3 up and 2 left.', 'The top number is horizontal: 3 right; the bottom number is vertical: 2 down.'),
          ('Reflecting (5, 1) in the y-axis gives (5, −1).', 'Reflection in the y-axis changes the sign of x: (−5, 1).')],
))

REFL = {'the x-axis': lambda p, q: (p, -q), 'the y-axis': lambda p, q: (-p, q), 'the line y = x': lambda p, q: (q, p), 'the line y = −x': lambda p, q: (-q, -p)}


def _pt(p):
    return f'({m(p[0])}, {m(p[1])})'


def _par(v):
    return f'({m(v)})' if v < 0 else str(v)


def _vec(a, b):
    return f'({m(a)} over {m(b)})'


@R.add('ch10-st2', 'C3', (1, 4), 'short')
def translate_pts(rng, slot):
    a, b = rng.randint(-7, 7), rng.randint(-7, 7)
    if a == 0 and b == 0:
        return None
    pts = [(rng.randint(-6, 6), rng.randint(-6, 6)) for _ in range(3 if slot.d >= 2 else 1)]
    img = [(p + a, q + b) for p, q in pts]
    if slot.d <= 1:
        return short(f'The point {_pt(pts[0])} is translated by the column vector {_vec(a, b)}. Find the coordinates of its image.', _pt(img[0]), f'Add {m(a)} to x and {m(b)} to y (M1); {_pt(img[0])} (A1).', 2)
    if rng.random() < 0.5:
        return short(f'Triangle ABC has vertices A{_pt(pts[0])}, B{_pt(pts[1])} and C{_pt(pts[2])}. It is translated by {_vec(a, b)}. Find the vertices of the image A′B′C′.', ', '.join(_pt(t) for t in img),
                     'Vector added to each vertex (M1); all three correct (A1 A1).', 3)
    return short(f'A point moves from {_pt(pts[0])} to {_pt(img[0])}. Write down the column vector of the translation, and describe it in words.', f'{_vec(a, b)}: {abs(a)} {"right" if a >= 0 else "left"}, {abs(b)} {"up" if b >= 0 else "down"}',
                 f'Image − object: ({m(img[0][0])} − {_par(pts[0][0])}, {m(img[0][1])} − {_par(pts[0][1])}) (M1); vector (A1); description (C1).', 3)


@R.add('ch10-st2', 'C3', (1, 4), 'short')
def reflect_pts(rng, slot):
    p, q = rng.randint(-8, 8), rng.randint(-8, 8)
    if slot.d >= 3 and rng.random() < 0.6:
        k = rng.randint(-4, 5)
        if rng.random() < 0.5:
            img = (2 * k - p, q)
            line = f'x = {m(k)}'
        else:
            img = (p, 2 * k - q)
            line = f'y = {m(k)}'
        return short(f'Reflect the point {_pt((p, q))} in the line {line}. Give the coordinates of the image and explain your method.', _pt(img),
                     f'Distance from the point to the line is the same on the other side (M1); {_pt(img)} (A1); method explained (C1).', 3)
    line = rng.choice(list(REFL))
    img = REFL[line](p, q)
    return short(f'Find the image of {_pt((p, q))} after reflection in {line}.', _pt(img), f'Rule for reflection in {line} applied (M1); {_pt(img)} (A1).', 2)


@R.add('ch10-st2', 'C1', (1, 3), 'mcq')
def reflect_mcq(rng, slot):
    p, q = rng.randint(1, 8), rng.randint(1, 8)
    if p == q:
        q += 1
    if rng.random() < 0.3:
        p = -p
    line = rng.choice(list(REFL))
    img = REFL[line](p, q)
    others = list({REFL[l](p, q) for l in REFL if REFL[l](p, q) != img} | {(-p, -q)})
    others = [o for o in others if o != img]
    if len(others) < 3:
        return None
    return mcq(rng, f'What is the image of {_pt((p, q))} after reflection in {line}?', _pt(img), [_pt(o) for o in others[:3]], f'Reflection in {line} sends {_pt((p, q))} to {_pt(img)}.')


@R.add('ch10-st2', 'C2', (2, 4), 'explain')
def mirror_line(rng, slot):
    p, q = rng.randint(-6, 6), rng.randint(-6, 6)
    k = rng.randint(-3, 4)
    kind = rng.choice(['vertical', 'horizontal', 'diag'])
    if kind == 'vertical':
        img = (2 * k - p, q)
        if img == (p, q):
            return None
        return explain(f'A point P{_pt((p, q))} is reflected to P′{_pt(img)}. Find the equation of the mirror line and explain how you know.', f'x = {m(k)}',
                       f'The mirror line is halfway between P and P′ and perpendicular to PP′ (R1): midpoint x = ({m(p)} + {m(img[0])})/2 = {m(k)} (A1).', 2)
    if kind == 'horizontal':
        img = (p, 2 * k - q)
        if img == (p, q):
            return None
        return explain(f'A point A{_pt((p, q))} is reflected to A′{_pt(img)}. Find the equation of the mirror line and explain how you know.', f'y = {m(k)}',
                       f'Perpendicular bisector of AA′ (R1): y = ({m(q)} + {m(img[1])})/2 = {m(k)} (A1).', 2)
    if p == q:
        return None
    return explain(f'The point {_pt((p, q))} maps to {_pt((q, p))}. Explain which single reflection does this.', 'Reflection in the line y = x, which swaps the x- and y-coordinates.',
                   'Coordinates swapped (R1); line y = x (A1).', 2)


@R.add('ch10-st2', 'C4', (3, 5), 'multi_step')
def trans_combo(rng, slot):
    a, b = rng.randint(-5, 5), rng.randint(-5, 5)
    c, d = rng.randint(-5, 5), rng.randint(-5, 5)
    P = (rng.randint(-4, 4), rng.randint(-4, 4))
    frames = [
        (f'A robot on a warehouse grid starts at {_pt(P)}. It is moved by the translation {_vec(a, b)} and then by {_vec(c, d)}. (a) Find its final position. (b) Write a single column vector for the combined move. (c) Explain why the order of the two translations does not matter.',
         f'(a) {_pt((P[0] + a + c, P[1] + b + d))} (b) {_vec(a + c, b + d)} (c) vector addition is commutative: ({m(a)} + {m(c)}, {m(b)} + {m(d)}) is the same either way'),
        (f'Triangle T has vertices (1, 1), (4, 1) and (1, 3). (a) Reflect T in the y-axis to give T₁. (b) Reflect T₁ in the x-axis to give T₂. (c) Describe fully a single transformation that maps T to T₂.',
         '(a) (−1, 1), (−4, 1), (−1, 3) (b) (−1, −1), (−4, −1), (−1, −3) (c) rotation of 180° about the origin'),
        (f'Investigate reflecting the point {_pt(P)} in the line x = 1 and then in the line x = {1 + a if a else 4}. (a) Find both images. (b) Describe the single transformation from the original point to the final image. (c) Predict what happens for any two parallel mirror lines a distance k apart.',
         None),
    ]
    q_, ans = rng.choice(frames)
    if ans is None:
        k2 = 1 + a if a else 4
        i1 = (2 - P[0], P[1])
        i2 = (2 * k2 - i1[0], P[1])
        ans = f'(a) {_pt(i1)}, then {_pt(i2)} (b) a translation by {_vec(i2[0] - P[0], 0)} (c) two reflections in parallel lines k apart give a translation of 2k perpendicular to the lines'
    return short(q_, ans, f'{ans}. Each transformation applied (M1 A1 A1); combined transformation described fully with correct vocabulary (C1 R1).', 5, 'multi_step', 'G5')


R.facts('ch10-st3', F(
    terms=[('rotation', 'a transformation that turns a shape about a fixed point (the centre of rotation) through a given angle and direction'),
           ('centre of rotation', 'the fixed point that does not move during a rotation'),
           ('clockwise', 'turning in the same direction as the hands of a clock')],
    facts=[('What is the image of (3, 1) after a rotation of 90° clockwise about the origin?', '(1, −3)', ['(−1, 3)', '(−3, −1)', '(3, −1)'], '90° clockwise: (x, y) → (y, −x).'),
           ('A rotation of 180° about the origin maps (x, y) to:', '(−x, −y)', ['(y, x)', '(−y, x)', '(x, −y)'], 'A half turn reverses both signs.'),
           ('A rotation of 90° anticlockwise is the same as a rotation of:', '270° clockwise', ['90° clockwise', '180°', '360° clockwise'], '360 − 90 = 270.')],
    why=[('Explain why you must state the angle, the direction and the centre to describe a rotation fully.', 'The same angle about a different centre, or in the other direction, gives a different image; all three are needed to define it uniquely.'),
         ('Explain why a rotation of 180° does not need a direction.', 'Turning half a turn clockwise or anticlockwise ends in the same place.'),
         ('Explain why a rotated shape is congruent to the original.', 'Every point turns through the same angle about the centre, so distances and angles inside the shape are unchanged.')],
    misc=[('A rotation of 90° clockwise about the origin maps (2, 5) to (−2, 5).', '90° clockwise maps (x, y) to (y, −x), so the image is (5, −2).'),
          ('Rotating 90° clockwise twice is the same as a reflection.', 'Two quarter turns make a half-turn (180° rotation), which keeps the orientation; a reflection reverses it.')],
))

ROT = {'90° clockwise': lambda p, q: (q, -p), '90° anticlockwise': lambda p, q: (-q, p), '180°': lambda p, q: (-p, -q)}


@R.add('ch10-st3', 'C3', (1, 4), 'short')
def rotate_pts(rng, slot):
    p, q = rng.randint(-7, 7), rng.randint(-7, 7)
    if (p, q) == (0, 0):
        return None
    turn = rng.choice(list(ROT))
    if slot.d >= 3:
        cx, cy = rng.randint(-3, 3), rng.randint(-3, 3)
        dx, dy = ROT[turn](p - cx, q - cy)
        img = (cx + dx, cy + dy)
        return short(f'Rotate the point {_pt((p, q))} through {turn} about the centre {_pt((cx, cy))}. Find its image.', _pt(img),
                     f'Position relative to the centre {_pt((p - cx, q - cy))} (M1); rotated {_pt((dx, dy))} (A1); add back the centre: {_pt(img)} (A1).', 3)
    img = ROT[turn](p, q)
    return short(f'Find the image of {_pt((p, q))} after a rotation of {turn} about the origin.', _pt(img), f'Rule for {turn} (M1); {_pt(img)} (A1).', 2)


@R.add('ch10-st3', 'C3', (2, 4), 'short')
def rotate_shape(rng, slot):
    pts = [(rng.randint(1, 6), rng.randint(1, 6)) for _ in range(3)]
    if len(set(pts)) < 3:
        return None
    turn = rng.choice(list(ROT))
    img = [ROT[turn](*t) for t in pts]
    return short(f'Triangle PQR has vertices P{_pt(pts[0])}, Q{_pt(pts[1])} and R{_pt(pts[2])}. It is rotated {turn} about the origin. Find the image vertices and state the quadrant the image lies in.',
                 ', '.join(_pt(t) for t in img) + f'; {"fourth" if turn == "90° clockwise" else "second" if turn == "90° anticlockwise" else "third"} quadrant',
                 'Rotation rule applied to each vertex (M1 A1 A1); quadrant (A1).', 4)


@R.add('ch10-st3', 'C1', (1, 3), 'mcq')
def rotate_mcq(rng, slot):
    p, q = rng.randint(1, 8), rng.randint(1, 8)
    if p == q:
        q += 1
    turn = rng.choice(list(ROT))
    img = ROT[turn](p, q)
    others = [ROT[t](p, q) for t in ROT if t != turn] + [(q, p), (p, -q)]
    others = list(dict.fromkeys(o for o in others if o != img))
    return mcq(rng, f'What is the image of {_pt((p, q))} after a rotation of {turn} about the origin?', _pt(img), [_pt(o) for o in others[:3]], f'{turn}: {_pt((p, q))} → {_pt(img)}.')


@R.add('ch10-st3', 'C2', (2, 4), 'explain')
def rotation_describe(rng, slot):
    p, q = rng.randint(1, 7), rng.randint(1, 7)
    turn = rng.choice(list(ROT))
    img = ROT[turn](p, q)
    who = name(rng)
    if turn == '180°':
        return explain(f'A point moves from {_pt((p, q))} to {_pt(img)}. {who} describes this as "a half turn". Explain why this description is incomplete and give a full description.',
                       'It needs the centre of rotation (no direction is needed for a half turn): rotation of 180° about the origin (0, 0).',
                       'Missing centre identified (R1); full description (A1).', 2)
    return explain(f'A point moves from {_pt((p, q))} to {_pt(img)}. {who} describes this as "a rotation of 90°". Explain why this description is incomplete and give a full description.',
                   f'It needs the centre and the direction: rotation {turn} about the origin (0, 0).',
                   'Missing centre/direction identified (R1); full description (A1).', 2)


@R.add('ch10-st3', 'C4', (3, 5), 'multi_step')
def rotation_task(rng, slot):
    kind = rng.choice(['repeat', 'windmill', 'combine', 'wheel'])
    if kind == 'repeat':
        p, q = rng.randint(1, 7), rng.randint(1, 7)
        ans = f'(a) {_pt(ROT["90° clockwise"](p, q))}, {_pt((-p, -q))}, {_pt(ROT["90° anticlockwise"](p, q))}, {_pt((p, q))} (b) a square centred on the origin (c) four quarter turns make a full turn of 360°'
        q_ = (f'Investigate rotating the point A{_pt((p, q))} repeatedly by 90° clockwise about the origin. (a) Find the images A₁, A₂, A₃ and A₄. '
              f'(b) Describe the shape formed by A, A₁, A₂, A₃. (c) Explain why A₄ = A.')
    elif kind == 'windmill':
        n = rng.choice([3, 4, 5, 6, 8])
        r = rng.randint(6, 15)
        ctry = rng.choice(['the Netherlands', 'Denmark', 'Spain', 'Portugal', 'Greece', 'Germany'])
        ans = f'(a) {g(360 / n, 4)}° (b) order {n} (c) ({r}, 0)'
        q_ = (f'A windmill in {ctry} has {n} identical, evenly spaced sails. (a) Find the smallest angle of rotation that maps the sails onto themselves. (b) State the order of rotational symmetry. '
              f'(c) Taking the hub as the origin, one sail tip is at (0, {r}) metres. Find the position of that tip after the sails turn 90° clockwise about the hub.')
    elif kind == 'combine':
        cx, cy = rng.randint(-3, 3), rng.randint(-3, 3)
        p, q = cx + rng.randint(1, 5), cy + rng.randint(1, 5)
        d1 = (-(p - cx), -(q - cy))
        i1 = (cx + d1[0], cy + d1[1])
        d2 = ROT['90° clockwise'](*d1)
        i2 = (cx + d2[0], cy + d2[1])
        ans = f'(a) {_pt(i1)} (b) {_pt(i2)} (c) a rotation of 90° anticlockwise (270° clockwise) about {_pt((cx, cy))}; check: {_pt((p, q))} → {_pt(i2)}'
        q_ = (f'The point P{_pt((p, q))} is rotated 180° about C{_pt((cx, cy))} and then 90° clockwise about the same centre. (a) Find the image after the first rotation. '
              f'(b) Find the final image. (c) Describe fully the single rotation that has the same effect, and check it using P.')
    else:
        n = rng.choice([8, 10, 12, 16, 18, 20, 24])
        r = rng.choice([10, 12, 15, 20, 25])
        city = rng.choice(CITIES)
        t = rng.randint(2, n // 2 - 1)
        ans = f'(a) {g(360 / n, 4)}° (b) {g(360 * t / n, 4)}° (c) ({r}, 0)'
        q_ = (f'A Ferris wheel in {city} has {n} equally spaced cabins on a circle of radius {r} m. (a) Find the angle between neighbouring cabins, measured at the hub. (b) Find the angle the wheel turns while a cabin moves {t} places round. '
              f'(c) With the hub at the origin, a cabin starts at the bottom, (0, −{r}). Find its position after a rotation of 90° anticlockwise about the hub.')
    return short(q_, ans, f'{ans}. Rotation rules applied (M1 A1 A1); pattern / symmetry identified (B: R1); clear notation (C1).', 5, 'multi_step', 'G5')


R.facts('ch10-st4', F(
    terms=[('enlargement', 'a transformation that changes the size of a shape by a scale factor from a centre of enlargement; angles stay the same'),
           ('scale factor', 'the number by which every length is multiplied in an enlargement'),
           ('congruent', 'exactly the same shape and size; one can be mapped onto the other by translations, rotations and reflections'),
           ('similar', 'the same shape but possibly a different size; corresponding angles equal and sides in the same ratio')],
    facts=[('A triangle is enlarged by scale factor 3. A side of 4 cm becomes:', '12 cm', ['7 cm', '4 cm', '36 cm'], 'Lengths are multiplied by the scale factor.'),
           ('Which transformation does NOT always produce a congruent image?', 'enlargement', ['translation', 'rotation', 'reflection'], 'An enlargement changes the size (unless the scale factor is 1).'),
           ('Enlarging by scale factor 1/2 makes the shape:', 'half the size', ['twice the size', 'the same size', 'a reflection'], 'A scale factor between 0 and 1 reduces the shape.')],
    why=[('Explain why the angles of a shape do not change in an enlargement.', 'Every length is multiplied by the same factor, so the shape keeps its proportions and its angles; only the size changes.'),
         ('Explain why an enlargement with scale factor 2 multiplies the area by 4.', 'Both the length and the width are doubled, so the area is multiplied by 2 × 2 = 4.'),
         ('Explain how to find the centre of an enlargement from a shape and its image.', 'Draw straight lines through pairs of corresponding vertices; they all meet at the centre of enlargement.')],
    misc=[('An enlargement with scale factor 1/3 makes the shape bigger.', 'A scale factor between 0 and 1 makes the image smaller (one third of the lengths).'),
          ('Two squares are always congruent.', 'Two squares are always similar, but only congruent if their sides are equal.')],
))


@R.add('ch10-st4', 'C3', (1, 4), 'short')
def enlarge_pts(rng, slot):
    k = rng.choice([2, 3, Fr(1, 2), 4]) if slot.d >= 3 else rng.choice([2, 3])
    cx, cy = (0, 0) if slot.d <= 2 else (rng.randint(-3, 3), rng.randint(-3, 3))
    pts = [(cx + rng.randint(-4, 4) * (2 if k == Fr(1, 2) else 1), cy + rng.randint(-4, 4) * (2 if k == Fr(1, 2) else 1)) for _ in range(3)]
    if len(set(pts)) < 3:
        return None
    img = [(cx + k * (p - cx), cy + k * (q - cy)) for p, q in pts]
    imtxt = ', '.join(f'({fx(Fr(a))}, {fx(Fr(b))})' for a, b in img)
    return short(f'Triangle ABC has vertices {", ".join(_pt(t) for t in pts)}. Enlarge it by scale factor {frac(Fr(k))} with centre {_pt((cx, cy))}. Find the coordinates of the image.', imtxt,
                 f'Vector from the centre to each vertex multiplied by {frac(Fr(k))} (M1); all three images (A1 A1).', 3)


@R.add('ch10-st4', 'C3', (1, 4), 'short')
def enlarge_measure(rng, slot):
    k = rng.choice([2, 3, 4, 5, Fr(1, 2), Fr(3, 2)])
    a, b = rng.randint(2, 12), rng.randint(2, 12)
    ang = rng.randint(30, 120)
    kind = rng.choice(['len', 'area', 'sf'])
    if kind == 'len':
        return short(f'A rectangle {a} cm by {b} cm is enlarged by scale factor {frac(Fr(k))}. Find the dimensions and perimeter of the image.', f'{fx(k * a)} cm by {fx(k * b)} cm; perimeter {fx(2 * k * (a + b))} cm',
                     f'Each length × {frac(Fr(k))} (M1); dimensions (A1); perimeter (A1).', 3)
    if kind == 'area':
        return short(f'A triangle with an angle of {ang}° and area {a * b} cm² is enlarged by scale factor {frac(Fr(k))}. State the size of the corresponding angle and find the area of the image.', f'{ang}°; {fx(k * k * a * b)} cm²',
                     f'Angles unchanged (A1); area × ({frac(Fr(k))})² = × {frac(Fr(k) ** 2)} (M1); {fx(k * k * a * b)} cm² (A1).', 3)
    return short(f'A photo {a * 2} cm wide is enlarged to {fx(k * a * 2)} cm wide. Find the scale factor and the new height if the original height was {b * 2} cm.', f'scale factor {frac(Fr(k))}; height {fx(k * b * 2)} cm',
                 f'{fx(k * a * 2)} ÷ {a * 2} = {frac(Fr(k))} (M1 A1); {b * 2} × {frac(Fr(k))} = {fx(k * b * 2)} cm (A1).', 3)


@R.add('ch10-st4', 'C1', (1, 3), 'mcq')
def congruent_mcq(rng, slot):
    which = rng.choice(['cong', 'sim'])
    if which == 'cong':
        return mcq(rng, 'A shape is transformed and the image is congruent to the object. Which transformation could it NOT have been?', 'an enlargement with scale factor 2',
                   ['a reflection in y = x', 'a rotation of 90° about the origin', 'a translation by (3 over −1)'], 'Translations, rotations and reflections preserve size; an enlargement with scale factor 2 doubles lengths.')
    k = rng.randint(2, 5)
    return mcq(rng, f'A shape is enlarged by scale factor {k}. What happens to its angles?', 'they stay the same', [f'they are multiplied by {k}', f'they are divided by {k}', f'they are multiplied by {k * k}'],
               'Enlargement preserves angles.')


@R.add('ch10-st4', 'C2', (2, 4), 'explain')
def enlarge_explain(rng, slot):
    k = rng.randint(2, 4)
    a = rng.randint(2, 9)
    who = name(rng)
    kind = rng.choice(['area', 'cong'])
    if kind == 'area':
        return explain(f'{who} enlarges a square of side {a} cm by scale factor {k} and says its area is {k} times bigger. Explain the mistake and find the correct area.',
                       f'Both sides are multiplied by {k}, so the area is multiplied by {k}² = {k * k}: {a * a} cm² → {a * a * k * k} cm².',
                       f'Scale factor applies to both dimensions (R1); {a * a * k * k} cm² (A1).', 2, 'G2')
    return explain(f'Explain why two triangles with sides {a}, {a + 2}, {a + 3} cm and {k * a}, {k * (a + 2)}, {k * (a + 3)} cm are similar but not congruent.',
                   f'Corresponding sides are all in the ratio 1 : {k}, so one is an enlargement of the other (similar); the sides are not equal, so they are not congruent.',
                   'Common ratio (R1); congruent needs equal sides (R1).', 2)


@R.add('ch10-st4', 'C4', (3, 5), 'multi_step')
def enlarge_task(rng, slot):
    city = rng.choice(CITIES)
    w, h = rng.randint(3, 9), rng.randint(2, 6)
    k = rng.choice([2, 3, 4, 5])
    scale = rng.choice([50, 100, 200, 250])
    frames = [
        (f'A poster design is {w} cm by {h} cm. It is enlarged by scale factor {k} for a bus shelter in {city}. (a) Find the dimensions of the enlarged poster. (b) How many times more ink is needed (assuming ink is proportional to area)? (c) The printer offers scale factor {k + 1} for the same price. Explain the effect on the area.',
         f'(a) {k * w} cm by {k * h} cm (b) {k * k} times (c) the area would be {(k + 1) ** 2} × {w * h} = {(k + 1) ** 2 * w * h} cm², {(k + 1) ** 2} times the original'),
        (f'A scale model of a building in {city} is made with scale 1 : {scale}. (a) The model is {w * 10} cm tall. Find the real height in metres. (b) A window on the real building has area {h} m². Find its area on the model in cm². (c) Explain why the area scale factor is not 1 : {scale}.',
         f'(a) {g(w * 10 * scale / 100, 4)} m (b) {g(h * 10000 / scale ** 2, 4)} cm² (c) areas scale by the square of the length factor: 1 : {scale ** 2}'),
    ]
    q_, ans = rng.choice(frames)
    return short(q_, ans, f'{ans}. Length scale factor applied (M1 A1); area factor k² (M1 A1); reasoning communicated (R1).', 5, 'multi_step', 'G5')


# =============================================================================================
# ch11 Statistics: Data Collection, Displays and Averages
# =============================================================================================
R.facts('ch11-st1', F(
    terms=[('qualitative data', 'data that describe a quality or category, such as favourite sport or eye colour'),
           ('discrete data', 'numerical data that can only take particular (usually whole-number) values, such as the number of siblings'),
           ('continuous data', 'numerical data that can take any value in a range, such as height or time'),
           ('sample', 'a part of a population chosen to represent the whole population'),
           ('bias', 'a systematic distortion in data collection that makes results unrepresentative')],
    facts=[('Which of these is continuous data?', 'the time taken to run 100 m', ['the number of goals in a match', 'shoe size', 'favourite colour'], 'Time can take any value in a range.'),
           ('Which question is least likely to be biased?', '"How many hours of TV did you watch last week?"', ['"Don’t you agree TV is a waste of time?"', '"Most people watch too much TV – do you?"', '"You watch a lot of TV, don’t you?"'], 'It is neutral and does not lead the respondent.'),
           ('Which sample is most likely to represent all the students in a school?', 'a random sample from every year group', ['the first 30 students to arrive', 'the school football team', 'students in one class'], 'Random selection across the population reduces bias.')],
    why=[('Explain why a survey of shoppers at 10 a.m. on a weekday may be biased.', 'People at work or school are missing, so the sample over-represents retired people, parents with young children and shift workers.'),
         ('Explain why a larger random sample usually gives more reliable results.', 'Random variation averages out over more data, so the sample statistics are closer to the population values.'),
         ('Explain why response boxes in a questionnaire should not overlap.', 'If boxes overlap (e.g. 0–2 and 2–4), some answers fit two boxes and the data become ambiguous.')],
    misc=[('Shoe size is continuous because feet can be any length.', 'Shoe sizes only take set values (e.g. 38, 38.5, 39), so shoe size is discrete.'),
          ('Asking your friends is a good random sample of your school.', 'Friends share similar interests and year group, so the sample is biased; a random method is needed.')],
    contrast=[('qualitative data', 'quantitative data', 'Qualitative data are categories or descriptions (e.g. favourite fruit); quantitative data are numbers from counting or measuring.'),
              ('a population', 'a sample', 'A population is the whole group of interest; a sample is a smaller part of it used to draw conclusions about the whole.')],
    evaluate=[('An online poll is the best way to find out what all the people in a city think.', ['it is cheap and fast and can reach many people', 'responses are easy to analyse'], ['only people with internet access and interest respond (self-selection bias)', 'some people may vote many times'], 'It is useful but biased; a random sample with a well-designed questionnaire is more representative.')],
))


@R.add('ch11-st1', 'C3', (1, 3), 'short')
def classify_data(rng, slot):
    items = [('the number of pets each student owns', 'quantitative, discrete'), ('the mass of a newborn baby', 'quantitative, continuous'), ('favourite type of music', 'qualitative'),
             ('the temperature at noon in a city', 'quantitative, continuous'), ('the number of cars passing a school in an hour', 'quantitative, discrete'), ('country of birth', 'qualitative'),
             ('the time to complete a puzzle', 'quantitative, continuous'), ('the number of goals scored in a match', 'quantitative, discrete'), ('the colour of a car', 'qualitative'),
             ('the height of a sunflower', 'quantitative, continuous'), ('dress size', 'quantitative, discrete'), ('the distance from home to school', 'quantitative, continuous')]
    chosen = rng.sample(items, 3)
    return short(f'Classify each of the following as qualitative, quantitative discrete or quantitative continuous: (a) {chosen[0][0]}, (b) {chosen[1][0]}, (c) {chosen[2][0]}.',
                 '; '.join(f'({"abc"[i]}) {c[1]}' for i, c in enumerate(chosen)), 'A1 for each correct classification (continuous = measured, discrete = counted / set values).', 3)


@R.add('ch11-st1', 'C3', (2, 4), 'short')
def sample_size(rng, slot):
    years = rng.sample([7, 8, 9, 10, 11, 12], 3)
    counts = [rng.randint(6, 18) * 10 for _ in years]
    tot = sum(counts)
    n = rng.choice([30, 40, 50, 60])
    shares = [Fr(c * n, tot) for c in counts]
    rounded = [round(float(s)) for s in shares]
    return short(f'A school in {rng.choice(CITIES)} has {counts[0]} students in Grade {years[0]}, {counts[1]} in Grade {years[1]} and {counts[2]} in Grade {years[2]}. A sample of {n} students is chosen so that each grade is represented in proportion. How many students should be chosen from each grade?',
                 ', '.join(f'Grade {y}: {r}' for y, r in zip(years, rounded)), f'Fraction of the total for each grade × {n} (M1); {", ".join(g(float(s), 4) for s in shares)} rounded (A1); total {sum(rounded)} checked (A1).', 3)


@R.add('ch11-st1', 'C1', (1, 3), 'mcq')
def data_type_mcq2(rng, slot):
    cont = ['the length of a leaf', 'the time to boil a kettle', 'the mass of a parcel', 'the speed of a car', 'arm span']
    disc = ['the number of siblings', 'the number of goals scored', 'the number of pages in a book', 'the number of emails received', 'the number of people on a bus']
    qual = ['favourite fruit', 'eye colour', 'mode of transport to school', 'type of pet', 'country of birth']
    which = rng.choice(['continuous', 'discrete', 'qualitative'])
    corr = rng.choice({'continuous': cont, 'discrete': disc, 'qualitative': qual}[which])
    others = [o for k, lst in [('continuous', cont), ('discrete', disc), ('qualitative', qual)] if k != which for o in lst]
    return mcq(rng, f'Which of these is an example of {which} data?', corr, rng.sample(others, 3), f'{corr[0].upper() + corr[1:]} is {which}.')


@R.add('ch11-st1', 'C2', (2, 4), 'explain')
def survey_critique(rng, slot):
    who = name(rng)
    city = rng.choice(CITIES)
    cases = [
        (f'{who} wants to know how residents of {city} travel to work. She asks 20 people waiting at a bus stop. Explain two problems with this method.',
         'Everyone sampled already uses the bus (biased sample); 20 people is too small to represent the city; better: a random sample of residents.'),
        (f'A questionnaire asks: "How much do you spend on lunch? 0–5, 5–10, 10–15, more than 15." Explain two problems with the response boxes.',
         'Boxes overlap at 5 and 10, so some answers fit two boxes; there is no currency or time period (per day? per week?).'),
        (f'{who} surveys only the members of the school chess club to find the most popular after-school activity. Explain why the results may be biased.',
         'Chess club members are likely to favour chess; the sample is not representative of all students.'),
        (f'A sports shop in {city} asks customers "Do you agree that exercise is important?" Explain why this is a poor survey question.',
         'It is a leading question that encourages "yes"; it gives no measurable information; the sample (shop customers) is already interested in sport.'),
    ]
    q_, ans = rng.choice(cases)
    q_ = q_.replace('She asks', f'{who} asks')
    return explain(q_, ans, f'{ans} (R1 for each valid, explained problem; criterion C: clear explanation).', 2)


@R.add('ch11-st1', 'C4', (3, 5), 'multi_step')
def survey_design(rng, slot):
    city = rng.choice(CITIES)
    pop = rng.randint(6, 15) * 100
    n = rng.choice([40, 50, 60, 80])
    topic = rng.choice(['screen time', 'sleep', 'how students travel to school', 'how much water students drink', 'time spent reading'])
    return short(f'An international school in {city} has {pop} students. The student council wants to investigate {topic}. (a) Write one suitable, unbiased survey question with non-overlapping response boxes. (b) Describe how to choose a random sample of {n} students. (c) Explain one possible source of bias and how to reduce it. (d) State whether the data collected will be discrete, continuous or qualitative.',
                 f'(a) e.g. a clear question with a time period and non-overlapping options (b) number the students 1–{pop} and use a random number generator to pick {n} different numbers (c) e.g. only surveying one grade – stratify by grade (d) depends on the question: time/amount is continuous (often recorded in groups), travel mode is qualitative',
                 'Question unbiased with complete, non-overlapping options (A1 C1); random sampling method described (M1 A1); bias identified and addressed (R1); data type (A1).', 6, 'multi_step', 'G5')


R.facts('ch11-st2', F(
    terms=[('pie chart', 'a circle divided into sectors, where each sector angle is proportional to the frequency (frequency ÷ total × 360°)'),
           ('stem-and-leaf diagram', 'a display that splits each value into a stem (leading digits) and a leaf (last digit), keeping the original data'),
           ('bar chart', 'a chart of separated bars whose heights show the frequencies of categories or discrete values'),
           ('key', 'the explanation of how to read a diagram, e.g. 3 | 7 means 37')],
    facts=[('In a pie chart of 60 people, a sector of 90° represents how many people?', '15', ['90', '25', '30'], '90/360 × 60 = 15.'),
           ('In a stem-and-leaf diagram with key 4 | 2 = 42, what value does 5 | 8 represent?', '58', ['5.8', '13', '85'], 'Stem gives tens, leaf gives units.'),
           ('Which diagram keeps every original data value?', 'a stem-and-leaf diagram', ['a pie chart', 'a bar chart of grouped data', 'a pictogram'], 'Each leaf is one actual value.')],
    why=[('Explain why the angles in a pie chart must add up to 360°.', 'The whole circle represents the total frequency, and a full turn is 360°.'),
         ('Explain one advantage of a stem-and-leaf diagram over a bar chart.', 'It keeps the original values, so the median, mode and range can be found exactly, while still showing the shape of the distribution.'),
         ('Explain why a pie chart is not suitable for showing changes over time.', 'A pie chart compares parts of one whole at one time; changes over time are better shown by a line graph or bar chart.')],
    misc=[('A pie chart sector of 120° always represents 120 people.', 'The angle shows a fraction (120/360 = 1/3) of the total; the number depends on the total frequency.'),
          ('The bars of a bar chart for discrete data must touch.', 'Bars for categories or discrete values have gaps; touching bars are used for continuous data in histograms.')],
))


@R.add('ch11-st2', 'C3', (1, 4), 'short')
def pie_angles(rng, slot):
    cats = rng.sample(['walk', 'bus', 'car', 'bike', 'train', 'scooter'], 4)
    tot = rng.choice([24, 30, 36, 40, 45, 60, 72, 90, 120])
    k = Fr(360, tot)
    while True:
        f = [rng.randint(1, tot // 2) for _ in range(3)]
        if sum(f) < tot:
            break
    f.append(tot - sum(f))
    angs = [fi * k for fi in f]
    if any(a.denominator != 1 for a in angs):
        return None
    if slot.d >= 3 and rng.random() < 0.5:
        i = rng.randrange(4)
        return short(f'In a pie chart showing how {tot} students travel to school, the sector for "{cats[i]}" has angle {angs[i]}°. How many students {cats[i] if cats[i] != "walk" else "walk"}? Explain your method.',
                     str(f[i]), f'{angs[i]}/360 × {tot} (M1) = {f[i]} (A1); each student is {g(float(k), 4)}° (C1).', 3)
    return short(f'{tot} students were asked how they travel to school: ' + ', '.join(f'{c} {fi}' for c, fi in zip(cats, f)) + '. Calculate the angle of each sector for a pie chart.',
                 ', '.join(f'{c} {a}°' for c, a in zip(cats, angs)), f'Each student = 360 ÷ {tot} = {g(float(k), 4)}° (M1); all angles correct and total 360° (A1 A1).', 3)


@R.add('ch11-st2', 'C3', (1, 4), 'short')
def stem_leaf(rng, slot):
    n = rng.choice([11, 13, 15])
    data = sorted(rng.randint(20, 79) for _ in range(n))
    stems = list(range(data[0] // 10, data[-1] // 10 + 1))
    disp = '; '.join(f'{s} | ' + ' '.join(str(d % 10) for d in data if d // 10 == s) for s in stems)
    med = data[n // 2]
    rngv = data[-1] - data[0]
    modes = [v for v in set(data) if data.count(v) == max(data.count(t) for t in data)]
    mode_txt = ', '.join(map(str, sorted(modes))) if max(data.count(t) for t in data) > 1 else 'none'
    what = rng.choice(['times (seconds) for a swimming length', 'marks in a quiz', 'heart rates (beats per minute) after exercise'])
    return short(f'The stem-and-leaf diagram shows {what} for {n} students (key: 3 | 4 = 34): {disp}. Find the median, the range and the mode.', f'median {med}, range {rngv}, mode: {mode_txt}',
                 f'Median is the {ordinal((n + 1) // 2)} value (M1) = {med} (A1); range {data[-1]} − {data[0]} = {rngv} (A1); mode: {mode_txt} (A1).', 4)


@R.add('ch11-st2', 'C1', (1, 3), 'mcq')
def pie_mcq(rng, slot):
    tot = rng.choice([30, 40, 60, 90, 120, 180])
    ang = rng.choice([30, 45, 60, 90, 120])
    v = Fr(ang * tot, 360)
    if v.denominator != 1:
        return None
    return mcq(rng, f'A pie chart represents {tot} people. How many people does a sector of {ang}° represent?', str(v), [str(ang), str(Fr(ang, 360) * 100)[:5], str(tot - v)],
               f'{ang}/360 × {tot} = {v}.')


@R.add('ch11-st2', 'C2', (2, 4), 'explain')
def chart_choice(rng, slot):
    who = name(rng)
    kind = rng.choice(['pie', 'misleading', 'compare'])
    if kind == 'pie':
        return explain(f'{who} wants to show the monthly rainfall in {rng.choice(CITIES)} over a year. Explain why a pie chart is not a good choice and suggest a better display.',
                       'Rainfall each month is not part of a meaningful whole and the pattern over time is lost; use a bar chart or line graph with months in order.',
                       'Reason pie chart unsuitable (R1); suitable alternative with reason (R1).', 2)
    if kind == 'misleading':
        lo = rng.randint(40, 80)
        return explain(f'A bar chart of sales has a vertical axis that starts at {lo} instead of 0. Explain how this could mislead a reader.',
                       f'Starting at {lo} exaggerates differences: a small difference in sales looks like a large difference in bar heights.',
                       'Axis not from zero identified (R1); effect on perception explained (R1).', 2)
    a, b = 4 * rng.randint(25, 75), 4 * rng.randint(5, 20)
    return explain(f'Two pie charts show favourite sports in two schools of {a} and {b} students. In both, football has a 90° sector. {who} says the same number of students in each school chose football. Explain why this is wrong.',
                   f'90° is a quarter in both, but a quarter of {a} is {g(a / 4, 4)} and a quarter of {b} is {g(b / 4, 4)}.',
                   'Angles show proportions, not numbers (R1); calculation (A1).', 2, 'G2')


@R.add('ch11-st2', 'C4', (3, 5), 'multi_step')
def display_task(rng, slot):
    n = 12
    a = sorted(rng.randint(30, 79) for _ in range(n))
    b = sorted(rng.randint(30, 79) for _ in range(n))
    stems = sorted({d // 10 for d in a + b})
    disp = '; '.join(' '.join(str(d % 10) for d in reversed([t for t in a if t // 10 == s])) + f' | {s} | ' + ' '.join(str(d % 10) for d in b if d // 10 == s) for s in stems)
    med = lambda d: Fr(d[5] + d[6], 2)
    return short(f'A back-to-back stem-and-leaf diagram shows the reaction times (hundredths of a second) of 12 students before (left) and after (right) a training game (key: 3 | 4 means 34 on either side): {disp}. (a) Find the median and range for each group. (b) Compare the two distributions. (c) Explain why a back-to-back diagram is useful here.',
                 f'(a) before: median {g(float(med(a)), 4)}, range {a[-1] - a[0]}; after: median {g(float(med(b)), 4)}, range {b[-1] - b[0]} (b) {"times were lower (better) after" if med(b) < med(a) else "times were higher after" if med(b) > med(a) else "medians are equal"}; {"after is more consistent" if b[-1] - b[0] < a[-1] - a[0] else "before is more consistent" if b[-1] - b[0] > a[-1] - a[0] else "equal spread"} (c) both groups share stems, so shape and values can be compared directly',
                 'Medians and ranges (A1 A1 A1 A1); comparison of average and spread in context (R1 R1); communication (C1).', 7, 'multi_step', 'G5')


R.facts('ch11-st3', F(
    terms=[('mean', 'the sum of the values divided by the number of values'),
           ('median', 'the middle value when the data are in order (or the mean of the two middle values)'),
           ('mode', 'the value that occurs most often'),
           ('range', 'the difference between the largest and smallest values, a measure of spread')],
    facts=[('What is the median of 3, 9, 4, 7, 12, 5?', '6', ['7', '5', '6.7'], 'Ordered: 3, 4, 5, 7, 9, 12; middle two 5 and 7 → 6.'),
           ('The mean of four numbers is 8. What is their total?', '32', ['8', '2', '12'], 'Total = mean × number of values.'),
           ('Which average is most affected by one extreme value?', 'the mean', ['the median', 'the mode', 'they are all affected equally'], 'The mean uses the size of every value.')],
    why=[('Explain why the median can be a better average than the mean for house prices.', 'A few very expensive houses raise the mean a lot, while the median is the middle price and is not pulled by extreme values.'),
         ('Explain how to find the mean from a frequency table.', 'Multiply each value by its frequency, add these products to get the total, and divide by the total frequency.'),
         ('Explain why the mode is the only average that can be used for qualitative data.', 'Categories such as colours cannot be added or ordered, so a mean or median cannot be calculated; you can only find the most common one.')],
    misc=[('The median of 2, 8, 5 is 8 because it is in the middle of the list.', 'The data must be ordered first: 2, 5, 8, so the median is 5.'),
          ('To find the mean from a frequency table, add the frequencies and divide by the number of rows.', 'Divide Σ(value × frequency) by Σ(frequency).')],
))


def _mn(v):
    """Fraction → 2 d.p. rounded half up, trailing zeros dropped."""
    s = str(rnd(float(v), 2))
    return m(s.rstrip('0').rstrip('.') if '.' in s else s)


@R.add('ch11-st3', 'C3', (1, 3), 'short')
def averages_list(rng, slot):
    n = rng.choice([6, 7, 8, 9])
    data = [rng.randint(1, 30) for _ in range(n)]
    data[rng.randrange(n)] = data[0]
    s = sorted(data)
    mean = Fr(sum(data), n)
    med = Fr(s[n // 2]) if n % 2 else Fr(s[n // 2 - 1] + s[n // 2], 2)
    mx = max(data.count(t) for t in data)
    modes = sorted({t for t in data if data.count(t) == mx})
    ctx = rng.choice(['points scored by a netball shooter in recent matches', 'daily maximum temperatures (°C)', 'number of books read by students this term', 'minutes late of a train service'])
    return short(f'The {ctx} were: {", ".join(map(str, data))}. Find the mean, median, mode and range.',
                 f'mean {_mn(mean)}, median {g(float(med))}, mode {", ".join(map(str, modes))}, range {s[-1] - s[0]}',
                 f'Σ = {sum(data)}, ÷ {n} (M1) → mean {_mn(mean)} (A1); ordered list for median {g(float(med))} (A1); mode and range (A1).', 4)


@R.add('ch11-st3', 'C3', (2, 5), 'short')
def freq_table_mean(rng, slot):
    vals = list(range(rng.randint(0, 2), rng.randint(0, 2) + 5))
    f = [rng.randint(1, 12) for _ in vals]
    N = sum(f)
    tot = sum(v * fi for v, fi in zip(vals, f))
    mean = Fr(tot, N)
    cum = 0
    med = None
    for v, fi in zip(vals, f):
        cum += fi
        if cum >= (N + 1) / 2 and med is None:
            med = v
    if N % 2 == 0:
        # median = mean of N/2-th and N/2+1-th
        order = [v for v, fi in zip(vals, f) for _ in range(fi)]
        med = Fr(order[N // 2 - 1] + order[N // 2], 2)
    mode = vals[f.index(max(f))] if f.count(max(f)) == 1 else None
    if mode is None:
        return None
    ctx = rng.choice(['number of siblings', 'number of pets', 'number of times students visited the library last week', 'number of goals each player scored this season'])
    return short(f'The table shows the {ctx} for a group of students. Value: {", ".join(map(str, vals))}; frequency: {", ".join(map(str, f))}. Find the mean (to 2 d.p.), the median and the mode.',
                 f'mean {rnd(float(mean), 2)}, median {g(float(med))}, mode {mode}',
                 f'Σfx = {tot} (M1), Σf = {N} (A1); mean {rnd(float(mean), 2)} (A1); median position {(N + 1) / 2:g} → {g(float(med))} (A1); mode {mode} (A1).', 5)


@R.add('ch11-st3', 'C3', (2, 4), 'short')
def missing_value(rng, slot):
    n = rng.randint(4, 7)
    data = [rng.randint(5, 40) for _ in range(n - 1)]
    target = rng.randint(10, 35)
    miss = target * n - sum(data)
    if miss <= 0 or miss > 80:
        return None
    who = name(rng)
    return short(f'{who} has test scores {", ".join(map(str, data))} and one more test to take. What score is needed in the last test for a mean of {target} over all {n} tests?', str(miss),
                 f'Total needed {target} × {n} = {target * n} (M1); {target * n} − {sum(data)} = {miss} (A1).', 2)


@R.add('ch11-st3', 'C1', (1, 3), 'mcq')
def average_mcq(rng, slot):
    data = sorted(rng.sample(range(1, 40), 5))
    med = data[2]
    mean = Fr(sum(data), 5)
    if mean == med:
        return None
    return mcq(rng, f'What is the median of {", ".join(map(str, rng.sample(data, 5)))}?', str(med), [g(float(mean), 3), str(data[-1] - data[0]), str(data[1])], f'Order the data: {", ".join(map(str, data))}; the middle value is {med}.')


@R.add('ch11-st3', 'C2', (2, 4), 'explain')
def average_choose(rng, slot):
    salaries = sorted([rng.randint(28, 45) * 1000 for _ in range(6)] + [rng.randint(200, 400) * 1000])
    mean = sum(salaries) / 7
    med = salaries[3]
    city, country, cur, cname = place(rng)
    return explain(f'The annual salaries at a small company in {city} are ({cname}): {", ".join(f"{s:_}".replace("_", " ") for s in salaries)}. The manager says the "average salary" is {cur}{round(mean):_}. Explain why this may mislead job applicants and which average is better.'.replace('_', ' '),
                   f'The mean {cur}{round(mean):_} is pulled up by one very high salary; the median {cur}{med:_} better represents a typical worker.'.replace('_', ' '),
                   'Mean and median calculated (A1 A1); effect of the extreme value explained (R1).', 3)


@R.add('ch11-st3', 'C4', (3, 5), 'multi_step')
def average_task(rng, slot):
    a = [rng.randint(10, 30) for _ in range(8)]
    b = [rng.randint(5, 35) for _ in range(8)]
    n1, n2 = two_names(rng)
    mean = lambda d: Fr(sum(d), len(d))
    med = lambda d: Fr(sorted(d)[3] + sorted(d)[4], 2)
    k = rng.randint(3, 8)
    frames = [
        (f'{n1} and {n2} are basketball players. Points scored in their last 8 games: {n1}: {", ".join(map(str, a))}; {n2}: {", ".join(map(str, b))}. (a) Find the mean, median and range for each player. (b) Which player would you choose for an important match? Justify your answer using both an average and the range.',
         f'(a) {n1}: mean {_mn(mean(a))}, median {g(float(med(a)))}, range {max(a) - min(a)}; {n2}: mean {_mn(mean(b))}, median {g(float(med(b)))}, range {max(b) - min(b)} (b) choose the player with the higher average unless the other is much more consistent (smaller range) – any reasoned choice using both statistics'),
        (f'Investigate: the mean of the numbers 1, 2, 3, …, n for n = 3, 4, 5, 6. (a) Find each mean. (b) Describe the pattern and write a formula for the mean of 1 to n. (c) Use it to find the mean of 1 to {10 * k}. (d) What happens to the mean if every number is increased by {k}?',
         f'(a) 2, 2.5, 3, 3.5 (b) the mean increases by 0.5 each time: (n + 1)/2 (c) {g((10 * k + 1) / 2, 4)} (d) the mean also increases by {k}'),
    ]
    q_, ans = rng.choice(frames)
    return short(q_, ans, f'{ans}. Averages and range calculated (M1 A1 A1); pattern/comparison in context (B/D: R1 R1); conclusion communicated (C1).', 6, 'multi_step', 'G5')


R.facts('ch11-st4', F(
    terms=[('scatter diagram', 'a graph of plotted points showing the relationship between two numerical variables'),
           ('correlation', 'a relationship between two variables: positive (both increase), negative (one increases as the other decreases) or none'),
           ('line of best fit', 'a straight line drawn through the middle of the points on a scatter diagram to show the trend'),
           ('outlier', 'a point that does not fit the general pattern of the data')],
    facts=[('What type of correlation would you expect between temperature and ice-cream sales?', 'positive', ['negative', 'none', 'perfect negative'], 'Sales tend to rise as temperature rises.'),
           ('What type of correlation would you expect between the age of a car and its value?', 'negative', ['positive', 'none', 'positive and strong'], 'Value tends to fall as age rises.'),
           ('Which pair of variables probably has no correlation?', 'shoe size and test score', ['height and arm span', 'hours of revision and test score', 'distance and taxi fare'], 'There is no reason for one to affect the other.')],
    why=[('Explain why correlation does not prove that one variable causes the other.', 'Both variables may depend on a third factor (e.g. ice-cream sales and drownings both rise in hot weather), or the link may be coincidence.'),
         ('Explain why a line of best fit should not be used far outside the range of the data.', 'The trend may not continue beyond the data (extrapolation); predictions within the data range (interpolation) are more reliable.'),
         ('Explain what a strong correlation looks like on a scatter diagram.', 'The points lie close to a straight line; the closer they are, the stronger the correlation.')],
    misc=[('A line of best fit must pass through the origin.', 'It passes through the middle of the points (often through the mean point), not necessarily through (0, 0).'),
          ('Negative correlation means the values are negative.', 'It means that as one variable increases, the other tends to decrease; the values can be positive.')],
))


def _scatter(rng, kind, n=8):
    xs = sorted(rng.sample(range(1, 30), n))
    if kind == 'positive':
        ys = [round(2 * t + rng.randint(-4, 4) + 10) for t in xs]
    elif kind == 'negative':
        ys = [round(80 - 2 * t + rng.randint(-4, 4)) for t in xs]
    else:
        ys = [rng.randint(10, 60) for _ in xs]
    return xs, ys


@R.add('ch11-st4', 'C3', (1, 4), 'short')
def describe_corr(rng, slot):
    kind = rng.choice(['positive', 'negative', 'none'])
    xs, ys = _scatter(rng, kind)
    ctx = rng.choice([('hours of practice', 'score'), ('outside temperature (°C)', 'hot drinks sold'), ('age of a phone (months)', 'battery life (hours)'), ('height (cm)', 'mass (kg)')])
    pts = ', '.join(f'({a}, {b})' for a, b in zip(xs, ys))
    from statistics import correlation
    r = correlation(xs, ys)
    actual = 'positive' if r > 0.5 else 'negative' if r < -0.5 else 'little or no'
    return short(f'Data for {ctx[0]} (x) and {ctx[1]} (y): {pts}. Describe the correlation shown on a scatter diagram of these data and interpret it in context.',
                 f'{actual} correlation', f'{actual.capitalize()} correlation (A1); interpretation: ' + ({'positive': f'higher {ctx[0]} tends to go with higher {ctx[1]}', 'negative': f'higher {ctx[0]} tends to go with lower {ctx[1]}'}.get(actual.split()[0], 'no clear relationship')) + ' (R1).', 2)


@R.add('ch11-st4', 'C3', (2, 4), 'short')
def best_fit_predict(rng, slot):
    mm = rng.choice([2, 3, 4, 5])
    c = rng.randint(5, 30)
    xs = sorted(rng.sample(range(2, 20), 7))
    ys = [mm * t + c + rng.randint(-2, 2) for t in xs]
    xp = rng.randint(xs[0] + 1, xs[-1] - 1)
    xbar, ybar = Fr(sum(xs), 7), Fr(sum(ys), 7)
    pred = ybar + mm * (xp - xbar)
    return short(f'Data for revision hours (x) and test score (y): ' + ', '.join(f'({a}, {b})' for a, b in zip(xs, ys)) + f'. A line of best fit through the mean point has gradient {mm}. (a) Find the mean point. (b) Use the line to estimate the score for {xp} hours of revision.',
                 f'(a) ({g(float(xbar), 4)}, {g(float(ybar), 4)}) (b) about {g(float(pred), 3)}', f'Mean point (A1 A1); y − {g(float(ybar), 4)} = {mm}(x − {g(float(xbar), 4)}) (M1); estimate {g(float(pred), 3)} (A1).', 4)


@R.add('ch11-st4', 'C1', (1, 3), 'mcq')
def corr_mcq(rng, slot):
    pairs = [('the number of hours of sunshine and the number of umbrellas sold', 'negative'), ('the distance travelled by a taxi and the fare', 'positive'),
             ('a person’s height and their phone number', 'none'), ('the outside temperature and the cost of heating a home', 'negative'),
             ('the number of people at a concert and the money taken in ticket sales', 'positive'), ('the length of a student’s hair and their mathematics score', 'none')]
    p, c = rng.choice(pairs)
    return mcq(rng, f'What type of correlation would you expect between {p}?', c, [o for o in ['positive', 'negative', 'none', 'perfect positive'] if o != c][:3], f'{p[0].upper() + p[1:]}: {c} correlation expected.')


@R.add('ch11-st4', 'C2', (2, 4), 'explain')
def causation_explain(rng, slot):
    cases = [('In summer, both ice-cream sales and sunburn cases increase.', 'Both are caused by hot, sunny weather (a third variable); ice cream does not cause sunburn.'),
             ('Towns with more libraries have more crimes.', 'Larger towns have more of both; population size is the hidden variable.'),
             ('Students who own more books get higher grades.', 'Other factors (family support, interest in reading) may explain both; owning books does not automatically cause high grades.'),
             ('Countries that eat more chocolate win more Nobel prizes.', 'Wealthier countries can afford both more chocolate and more research funding; wealth is a confounding variable.')]
    claim, ans = rng.choice(cases)
    who = name(rng)
    return explain(f'{claim} {who} concludes that one causes the other. Explain why this conclusion may be wrong.', ans, f'{ans} (R1: correlation ≠ causation; R1: plausible third variable named).', 2, 'G2')


@R.add('ch11-st4', 'C4', (3, 5), 'multi_step')
def scatter_task(rng, slot):
    city = rng.choice(CITIES)
    xs = sorted(rng.sample(range(10, 35), 8))
    mm = Fr(rng.choice([3, 4, 5, 6]), 1)
    ys = [int(mm * t) + rng.randint(-10, 10) for t in xs]
    out_i = rng.randrange(8)
    ys[out_i] += -45 if ys[out_i] >= 60 and rng.random() < 0.5 else 45
    xbar = Fr(sum(xs) - xs[out_i], 7)
    ybar = Fr(sum(ys) - ys[out_i], 7)
    xp = rng.randint(xs[0] + 1, xs[-1] - 1)
    pred = ybar + mm * (xp - xbar)
    return short(f'A café in {city} records the maximum daily temperature (°C, x) and the number of cold drinks sold (y): ' + ', '.join(f'({a}, {b})' for a, b in zip(xs, ys)) + f'. (a) Describe the correlation. (b) Identify the outlier and suggest a reason for it. (c) Ignoring the outlier, the line of best fit has gradient about {mm} and passes through ({g(float(xbar), 4)}, {g(float(ybar), 4)}). Estimate sales on a day with a maximum of {xp} °C. (d) Explain why predicting sales on a 45 °C day is unreliable.',
                 f'(a) positive correlation (b) ({xs[out_i]}, {ys[out_i]}) – e.g. a holiday, a power cut or a special event (c) about {g(float(pred), 3)} drinks (d) 45 °C is outside the data range (extrapolation)',
                 'Correlation described in context (A1); outlier identified with a plausible reason (A1 R1); estimate from the line (M1 A1); extrapolation explained (R1).', 6, 'multi_step', 'G5')


# =============================================================================================
# ch12 Probability: Simple and Experimental
# =============================================================================================
R.facts('ch12-st1', F(
    terms=[('probability', 'a number from 0 to 1 measuring how likely an event is to happen'),
           ('equally likely outcomes', 'outcomes that each have the same chance of happening'),
           ('complement of an event', 'the event "A does not happen", with P(not A) = 1 − P(A)'),
           ('theoretical probability', 'number of favourable outcomes ÷ total number of equally likely outcomes')],
    facts=[('What is the probability of rolling a prime number on a fair six-sided dice?', '1/2', ['1/3', '2/3', '1/6'], 'Primes 2, 3, 5: 3 out of 6.'),
           ('P(rain) = 0.35. What is P(no rain)?', '0.65', ['0.35', '1.35', '0.5'], '1 − 0.35.'),
           ('Which probability describes an event that is certain?', '1', ['0', '0.5', '100'], 'Certain events have probability 1.')],
    why=[('Explain why a probability can never be greater than 1.', 'The number of favourable outcomes cannot exceed the total number of outcomes, so the fraction is at most 1.'),
         ('Explain why P(A) + P(not A) = 1.', 'Every outcome is either in A or not in A, and not both, so the two probabilities together cover all outcomes.'),
         ('Explain why the probability of getting a head on a fair coin is 1/2 even after five tails in a row.', 'Each toss is independent; the coin has no memory, so the two outcomes are still equally likely.')],
    misc=[('There are two outcomes – win or lose – so the probability of winning is 1/2.', 'The outcomes are not necessarily equally likely; probability depends on how many equally likely outcomes favour winning.'),
          ('A probability of 0.7 means the event will happen 7 times.', 'It means the event is expected about 70% of the time in the long run; it is not a fixed count.')],
))


@R.add('ch12-st1', 'C3', (1, 4), 'short')
def bag_prob(rng, slot):
    cols = rng.sample(['red', 'blue', 'green', 'yellow', 'white', 'black'], 3)
    nums = [rng.randint(1, 12) for _ in cols]
    tot = sum(nums)
    i = rng.randrange(3)
    container = rng.choice(['bag', 'box', 'jar'])
    obj = rng.choice(['counters', 'marbles', 'beads', 'sweets'])
    if slot.d <= 2:
        return short(f'A {container} contains {nums[0]} {cols[0]}, {nums[1]} {cols[1]} and {nums[2]} {cols[2]} {obj}. One is chosen at random. Find the probability that it is {cols[i]}.', fx(Fr(nums[i], tot)),
                     f'{nums[i]} favourable out of {tot} (M1); {fx(Fr(nums[i], tot))} (A1).', 2)
    j = (i + 1) % 3
    return short(f'A {container} contains {nums[0]} {cols[0]}, {nums[1]} {cols[1]} and {nums[2]} {cols[2]} {obj}. One is chosen at random. Find (a) P({cols[i]} or {cols[j]}), (b) P(not {cols[i]}).',
                 f'(a) {fx(Fr(nums[i] + nums[j], tot))} (b) {fx(Fr(tot - nums[i], tot))}', f'(a) ({nums[i]} + {nums[j]})/{tot} (M1 A1) (b) 1 − {nums[i]}/{tot} (A1).', 3)


@R.add('ch12-st1', 'C3', (1, 4), 'short')
def dice_card_prob(rng, slot):
    kind = rng.choice(['dice', 'spinner', 'cards'])
    if kind == 'dice':
        s = rng.choice([6, 8, 10, 12, 20])
        ev = rng.choice([('a multiple of 3', lambda v: v % 3 == 0), ('greater than 4', lambda v: v > 4), ('a square number', lambda v: math.isqrt(v) ** 2 == v), ('an odd number', lambda v: v % 2 == 1), ('a factor of 12', lambda v: 12 % v == 0)])
        fav = [v for v in range(1, s + 1) if ev[1](v)]
        return short(f'A fair {s}-sided dice numbered 1 to {s} is rolled. Find the probability of rolling {ev[0]}.', fx(Fr(len(fav), s)),
                     f'Favourable outcomes {", ".join(map(str, fav))} (M1); {len(fav)}/{s} = {fx(Fr(len(fav), s))} (A1).', 2)
    if kind == 'spinner':
        ps = [Fr(rng.randint(1, 4), 10) for _ in range(3)]
        rest = 1 - sum(ps)
        if rest <= 0:
            return None
        cols = rng.sample(['red', 'blue', 'green', 'orange'], 4)
        return short(f'A biased spinner lands on {cols[0]} with probability {float(ps[0]):g}, {cols[1]} with {float(ps[1]):g} and {cols[2]} with {float(ps[2]):g}. The only other colour is {cols[3]}. Find P({cols[3]}).', f'{float(rest):g}',
                     f'Probabilities add to 1 (R1); 1 − {float(sum(ps)):g} = {float(rest):g} (A1).', 2)
    n = rng.randint(1, 20)
    nums = list(range(1, n + 21))
    ev = rng.choice([('a prime number', lambda v: sp.isprime(v)), ('a multiple of 4', lambda v: v % 4 == 0), ('a two-digit number', lambda v: 10 <= v <= 99)])
    fav = [v for v in nums if ev[1](v)]
    return short(f'Cards numbered 1 to {len(nums)} are shuffled and one is taken at random. Find the probability that it is {ev[0]}.', fx(Fr(len(fav), len(nums))),
                 f'{len(fav)} favourable cards (M1); {fx(Fr(len(fav), len(nums)))} (A1).', 2)


@R.add('ch12-st1', 'C1', (1, 3), 'mcq')
def prob_scale_mcq(rng, slot):
    events = [('the sun rising tomorrow', 'certain'), ('rolling a 7 on a normal six-sided dice', 'impossible'), ('getting a head when tossing a fair coin', 'even chance'),
              ('rolling a number less than 6 on a fair dice', 'likely'), ('picking a red card from a full pack of playing cards', 'even chance'), ('rolling a 6 on a fair dice', 'unlikely')]
    e, c = rng.choice(events)
    return mcq(rng, f'Which word best describes the probability of {e}?', c, [w for w in ['certain', 'impossible', 'even chance', 'likely', 'unlikely'] if w != c][:3], f'{e[0].upper() + e[1:]} is {c}.')


@R.add('ch12-st1', 'C2', (2, 4), 'explain')
def prob_explain(rng, slot):
    a, b = rng.randint(2, 9), rng.randint(2, 9)
    who = name(rng)
    kind = rng.choice(['twoout', 'compare'])
    if kind == 'twoout':
        return explain(f'A bag has {a} red and {b} blue counters. {who} says "there are only two colours, so P(red) = 1/2". Explain the mistake.',
                       f'The colours are not equally likely: P(red) = {a}/{a + b} = {fx(Fr(a, a + b))}.',
                       'Outcomes not equally likely (R1); correct probability (A1).', 2, 'G2')
    c, d = rng.randint(2, 9), rng.randint(2, 9)
    p1, p2 = Fr(a, a + b), Fr(c, c + d)
    if p1 == p2:
        return None
    return explain(f'Bag A has {a} green and {b} white beads; bag B has {c} green and {d} white beads. Explain which bag gives the better chance of picking a green bead.',
                   f'P(green) A = {fx(p1)} ≈ {rnd(float(p1), 3)}, B = {fx(p2)} ≈ {rnd(float(p2), 3)}; bag {"A" if p1 > p2 else "B"} is better.',
                   'Both probabilities (A1 A1); comparison using a common form (R1).', 3)


@R.add('ch12-st1', 'C4', (3, 5), 'multi_step')
def prob_task1(rng, slot):
    r, b = rng.randint(2, 8), rng.randint(2, 8)
    k = rng.randint(1, 6)
    who = name(rng)
    frames = [
        (f'A bag contains {r} red and {b} blue marbles. (a) Find P(red). (b) {who} adds some red marbles so that P(red) becomes {fx(Fr(r + k, r + k + b))}. How many were added? (c) How many blue marbles would have to be added instead (to the original bag) to make P(red) = {fx(Fr(r, r + b + k))}?',
         f'(a) {fx(Fr(r, r + b))} (b) {k} (c) {k}'),
        (f'A spinner has 8 equal sectors: {r if r <= 6 else 3} are yellow and the rest are purple. (a) Find P(yellow) and P(purple). (b) Investigate how many sectors must be repainted yellow to make P(yellow) at least 3/4. (c) Explain why P(yellow) can never be 9/10 on this spinner.',
         None),
    ]
    q_, ans = rng.choice(frames)
    if ans is None:
        yv = r if r <= 6 else 3
        need = max(0, 6 - yv)
        ans = f'(a) {fx(Fr(yv, 8))}, {fx(Fr(8 - yv, 8))} (b) {need} (to make 6 yellow out of 8) (c) with 8 equal sectors every probability is a multiple of 1/8, and 9/10 is not'
    return short(q_, ans, f'{ans}. Probabilities as fractions (A1 A1); equation or systematic trial (B: M1 A1); reasoned conclusion (R1).', 5, 'multi_step', 'G5')


R.facts('ch12-st2', F(
    terms=[('sample space', 'the set of all possible outcomes of an experiment'),
           ('sample space diagram', 'a grid or list showing every combined outcome of two events'),
           ('two-way table', 'a table that shows the frequencies of two categorical variables at the same time')],
    facts=[('How many outcomes are there when two fair six-sided dice are rolled?', '36', ['12', '11', '6'], '6 × 6 = 36.'),
           ('What is the probability of getting two heads when two fair coins are tossed?', '1/4', ['1/2', '1/3', '2/4'], 'HH is 1 of 4 outcomes: HH, HT, TH, TT.'),
           ('When two dice are rolled, which total is most likely?', '7', ['6', '12', '2'], 'Six of the 36 outcomes give 7.')],
    why=[('Explain why HT and TH must be counted as different outcomes when two coins are tossed.', 'The coins are different (first and second), so "head then tail" and "tail then head" are separate equally likely outcomes.'),
         ('Explain why a sample space diagram helps to find probabilities for two dice.', 'It lists all 36 equally likely outcomes, so favourable outcomes can be counted without missing any.'),
         ('Explain how a two-way table can be used to find a probability.', 'Read the frequency in the relevant cell (or row/column total) and divide by the appropriate total.')],
    misc=[('When two dice are rolled, there are 11 possible totals, so P(total 7) = 1/11.', 'The 11 totals are not equally likely; out of 36 outcomes, 6 give 7, so P = 1/6.'),
          ('Tossing two coins: P(one head and one tail) = 1/3, since outcomes are 2H, 2T or 1 each.', 'There are four equally likely outcomes HH, HT, TH, TT; two give one of each, so P = 1/2.')],
))


@R.add('ch12-st2', 'C3', (1, 4), 'short')
def two_dice(rng, slot):
    a, b = rng.choice([4, 6, 6, 8]), rng.choice([4, 6, 6])
    ev = rng.choice([('the total is {t}', 'sum'), ('the product is even', 'prodeven'), ('both scores are the same', 'double'), ('the difference is {t}', 'diff'), ('the total is greater than {t}', 'gt')])
    t = rng.randint(2, a + b - 1) if ev[1] in ('sum', 'gt') else rng.randint(0, 3)
    outs = [(i, j) for i in range(1, a + 1) for j in range(1, b + 1)]
    test = {'sum': lambda i, j: i + j == t, 'prodeven': lambda i, j: (i * j) % 2 == 0, 'double': lambda i, j: i == j, 'diff': lambda i, j: abs(i - j) == t, 'gt': lambda i, j: i + j > t}[ev[1]]
    fav = sum(1 for i, j in outs if test(i, j))
    if fav == 0:
        return None
    desc = ev[0].format(t=t)
    dice = f'Two fair {a}-sided dice are' if a == b else f'A fair {a}-sided dice and a fair {b}-sided dice are'
    return short(f'{dice} rolled. Draw a sample space diagram and find the probability that {desc}.', fx(Fr(fav, a * b)),
                 f'{a} × {b} = {a * b} outcomes listed (M1); {fav} favourable (A1); {fx(Fr(fav, a * b))} (A1).', 3)


@R.add('ch12-st2', 'C3', (2, 5), 'short')
def two_way(rng, slot):
    cats = rng.choice([(('Grade 8', 'Grade 9'), ('football', 'swimming', 'tennis')), (('boys', 'girls'), ('bus', 'walk', 'car')), (('adults', 'children'), ('cinema', 'museum', 'park'))])
    rows, cols = cats
    f = [[rng.randint(3, 25) for _ in cols] for _ in rows]
    tot = sum(map(sum, f))
    i, j = rng.randrange(2), rng.randrange(3)
    rt = sum(f[i])
    ct = sum(f[r][j] for r in range(2))
    tbl = '; '.join(f'{rows[r]}: ' + ', '.join(f'{cols[c]} {f[r][c]}' for c in range(3)) for r in range(2))
    if slot.d <= 2:
        return short(f'A survey gave these results – {tbl}. One person is chosen at random. Find the probability that they are {rows[i]} and chose {cols[j]}.', fx(Fr(f[i][j], tot)),
                     f'Total {tot} (A1); {f[i][j]}/{tot} = {fx(Fr(f[i][j], tot))} (A1).', 2)
    return short(f'A survey gave these results – {tbl}. Find (a) the probability that a randomly chosen person chose {cols[j]}, (b) the probability that a person chosen from the {rows[i]} chose {cols[j]}.',
                 f'(a) {fx(Fr(ct, tot))} (b) {fx(Fr(f[i][j], rt))}', f'(a) column total {ct}/{tot} (M1 A1) (b) restricted to the row: {f[i][j]}/{rt} (M1 A1).', 4)


@R.add('ch12-st2', 'C1', (1, 3), 'mcq')
def sample_space_mcq(rng, slot):
    a, b = rng.choice([(2, 6), (6, 6), (2, 2), (4, 6), (3, 4), (2, 3)])
    names_ = {2: 'a coin' if rng.random() < 0.5 else 'a two-sided disc', 3: 'a three-colour spinner', 4: 'a four-sided dice', 6: 'a six-sided dice'}
    return mcq(rng, f'How many outcomes are in the sample space when {names_[a]} and {names_[b]} are used together?', str(a * b), [str(a + b), str(a * b + 1) if a * b + 1 != a + b else str(a * b * 2), str(max(a, b))],
               f'{a} × {b} = {a * b} outcomes.')


@R.add('ch12-st2', 'C2', (2, 4), 'explain')
def sample_space_explain(rng, slot):
    t = rng.randint(3, 11)
    ways = sum(1 for i in range(1, 7) for j in range(1, 7) if i + j == t)
    who = name(rng)
    return explain(f'{who} says that when two fair dice are rolled, a total of {t} is as likely as a total of 2. Explain why {who} is wrong, using the sample space.',
                   f'Total {t} can happen in {ways} ways out of 36 but total 2 only in 1 way (1, 1), so P({t}) = {fx(Fr(ways, 36))} > 1/36.' if ways > 1 else f'Both can happen in only 1 way, so here {who} is correct.',
                   'Sample space of 36 used (M1); outcomes counted (A1); comparison (R1).', 3)


@R.add('ch12-st2', 'C4', (3, 5), 'multi_step')
def sample_space_task(rng, slot):
    k = rng.randint(2, 5)
    who, who2 = two_names(rng)
    frames = [
        (f'{who} and {who2} play a game with two fair six-sided dice. {who} wins if the difference between the scores is 0, 1 or 2; otherwise {who2} wins. (a) Draw a sample space diagram of the differences. (b) Find P({who} wins). (c) Is the game fair? If not, suggest a change to make it fair.',
         f'(a) a 6 × 6 grid of differences (b) 24/36 = 2/3 (c) not fair; e.g. {who} wins on a difference of 0 or 1 or 2? no – try {who} wins on 0, 1 only (16/36) or on 1 or 2 only (18/36 = 1/2, fair)'),
        (f'A café in {rng.choice(CITIES)} offers a meal deal: one of {k} main courses and one of 3 drinks. (a) How many different meal deals are there? (b) List the sample space using letters. (c) If a deal is chosen at random, find the probability that it includes the first drink. (d) Explain how your answer to (a) would change if a choice of 2 desserts were added.',
         f'(a) {3 * k} (b) e.g. M1D1, M1D2, M1D3, … (c) 1/3 (d) it doubles to {6 * k} (multiply by 2)'),
    ]
    q_, ans = rng.choice(frames)
    ans = ans.replace(f'e.g. {who} wins on a difference of 0 or 1 or 2? no – try {who} wins on 0, 1 only (16/36) or on 1 or 2 only (18/36 = 1/2, fair)', f'e.g. {who} wins only on a difference of 1 or 2 (10 + 8 = 18 outcomes, 18/36 = 1/2), which is fair')
    return short(q_, ans, f'{ans}. Systematic sample space (M1 A1); probability (A1); fairness/change justified (R1 C1).', 5, 'multi_step', 'G5')


R.facts('ch12-st3', F(
    terms=[('relative frequency', 'the number of times an event happens divided by the number of trials; an estimate of probability'),
           ('experimental probability', 'a probability estimated from the results of an experiment or survey'),
           ('trial', 'one performance of an experiment, such as one roll of a dice')],
    facts=[('A drawing pin lands point-up 36 times in 120 throws. What is the relative frequency of point-up?', '0.3', ['0.36', '0.12', '3.33'], '36 ÷ 120 = 0.3.'),
           ('Which estimate of probability is most reliable?', 'one based on 1000 trials', ['one based on 10 trials', 'one based on 1 trial', 'one based on a guess'], 'More trials give a more reliable relative frequency.'),
           ('A fair coin is tossed 50 times and gives 31 heads. This means:', 'the result is possible for a fair coin; more trials are needed to judge', ['the coin must be biased', 'the next toss will be a tail', 'P(head) = 31'], 'Random variation is expected in small samples.')],
    why=[('Explain why relative frequency gets closer to the theoretical probability as the number of trials increases.', 'Random variations even out over many trials (the law of large numbers), so the proportion settles towards the true probability.'),
         ('Explain when you would use experimental probability rather than theoretical probability.', 'When outcomes are not equally likely or cannot be calculated, e.g. a biased dice or the chance of rain; you estimate from repeated trials or data.'),
         ('Explain why two students doing the same experiment can get different relative frequencies.', 'Each set of trials is random, so results vary; with few trials the differences can be large.')],
    misc=[('A dice landed on 6 three times in 10 rolls, so P(6) = 3/10 exactly.', '3/10 is only an estimate from a small number of trials; the theoretical probability for a fair dice is 1/6.'),
          ('After 100 rolls, a fair dice must have shown exactly 50 even numbers.', 'You expect about 50, but random variation means the actual number will usually be a little different.')],
))


@R.add('ch12-st3', 'C3', (1, 4), 'short')
def rel_freq(rng, slot):
    n = rng.choice([50, 80, 100, 120, 150, 200, 250, 400])
    k = rng.randint(n // 10, n * 9 // 10)
    who = name(rng)
    obj = rng.choice([('a drawing pin', 'lands point up'), ('a paper cup', 'lands on its side'), ('a biased coin', 'shows heads'), ('a spinner', 'lands on blue'), ('a bottle-flip', 'lands upright')])
    rf = Fr(k, n)
    if slot.d <= 2:
        return short(f'{who} throws {obj[0]} {n} times; it {obj[1]} {k} times. Find the relative frequency of this outcome as a decimal.', f'{float(rf):g}', f'{k} ÷ {n} (M1) = {float(rf):g} (A1).', 2)
    N = rng.choice([500, 1000, 2000, 3000])
    return short(f'{who} throws {obj[0]} {n} times; it {obj[1]} {k} times. (a) Estimate the probability that it {obj[1]}. (b) Estimate how many times it would {obj[1].split()[0].rstrip("s")} {" ".join(obj[1].split()[1:])} in {N} throws.',
                 f'(a) {float(rf):g} (b) about {g(float(rf * N), 4)}', f'(a) {k}/{n} (A1); (b) {float(rf):g} × {N} (M1) = {g(float(rf * N), 4)} (A1).', 3)


@R.add('ch12-st3', 'C3', (2, 4), 'short')
def biased_dice(rng, slot):
    n = rng.choice([60, 120, 180, 300, 600])
    exp = n // 6
    fr_ = [exp + rng.randint(-exp // 4, exp // 4) for _ in range(5)]
    fr_.append(n - sum(fr_))
    if fr_[-1] <= 0:
        return None
    big = max(range(6), key=lambda i: abs(fr_[i] - exp))
    return short(f'A dice is rolled {n} times with results 1: {fr_[0]}, 2: {fr_[1]}, 3: {fr_[2]}, 4: {fr_[3]}, 5: {fr_[4]}, 6: {fr_[5]}. (a) Find the relative frequency of a {big + 1}. (b) How many of each score would you expect from a fair dice? (c) Comment on whether the dice appears biased.',
                 f'(a) {fx(Fr(fr_[big], n))} ≈ {rnd(fr_[big] / n, 3)} (b) {exp} each (c) {"the frequencies are close to " + str(exp) + ", so there is no strong evidence of bias" if abs(fr_[big] - exp) <= exp * 0.2 else "the " + str(big + 1) + " differs noticeably from " + str(exp) + ", which suggests possible bias; more trials would help"}',
                 f'(a) {fr_[big]}/{n} (A1); (b) {n}/6 = {exp} (A1); (c) comparison with expected frequencies and a sensible conclusion (R1).', 3)


@R.add('ch12-st3', 'C1', (1, 3), 'mcq')
def rel_freq_mcq(rng, slot):
    n = rng.choice([40, 50, 80, 100, 200])
    k = rng.randint(n // 10, n // 2)
    return mcq(rng, f'A spinner lands on red {k} times in {n} spins. What is the relative frequency of red?', f'{float(Fr(k, n)):g}', [f'{float(Fr(n - k, n)):g}', str(k), f'{float(Fr(k, 100)):g}' if n != 100 else f'{float(Fr(k, 50)):g}'],
               f'{k} ÷ {n} = {float(Fr(k, n)):g}.')


@R.add('ch12-st3', 'C2', (2, 4), 'explain')
def rf_compare(rng, slot):
    a, b = two_names(rng)
    n1, n2 = rng.choice([20, 30, 40]), rng.choice([400, 500, 1000])
    k1, k2 = rng.randint(2, n1 // 2), rng.randint(n2 // 8, n2 // 4)
    return explain(f'{a} rolls a dice {n1} times and gets {k1} sixes. {b} rolls the same dice {n2} times and gets {k2} sixes. Explain whose results give the better estimate of P(six), and give that estimate.',
                   f'{b}’s, because {n2} trials is many more than {n1}; estimate {k2}/{n2} = {float(Fr(k2, n2)):.3g}.',
                   'More trials more reliable (R1); estimate (A1).', 2)


@R.add('ch12-st3', 'C4', (3, 5), 'multi_step')
def experiment_task(rng, slot):
    who = name(rng)
    ns = [10, 50, 100, 200, 500]
    p = rng.choice([0.25, 0.3, 0.4, 0.6])
    counts = [max(0, min(n, round(n * p + rng.randint(-2, 2) * math.sqrt(n * p * (1 - p)) / 2))) for n in ns]
    rfs = [Fr(c, n) for c, n in zip(counts, ns)]
    return short(f'{who} tests a home-made spinner and records the number of times it lands on green after 10, 50, 100, 200 and 500 spins (cumulative totals): {", ".join(map(str, counts))}. (a) Calculate the relative frequency after each number of spins. (b) Describe what happens to the relative frequency. (c) Give the best estimate of P(green) and explain your choice. (d) Estimate the number of greens in 2000 spins.',
                 f'(a) {", ".join(f"{float(r):.3g}" for r in rfs)} (b) it varies a lot at first and then settles down (c) {float(rfs[-1]):.3g}, from the largest number of trials (d) about {round(float(rfs[-1]) * 2000)}',
                 'Relative frequencies (M1 A1); trend described (B: R1); best estimate justified (R1); expected number (A1); communication (C1).', 6, 'multi_step', 'G5')


R.facts('ch12-st4', F(
    terms=[('expected frequency', 'the number of times an outcome is expected: probability × number of trials'),
           ('fair game', 'a game in which every player has the same chance of winning (or the expected gain is zero)'),
           ('biased', 'not fair: some outcomes are more likely than they should be')],
    facts=[('A fair dice is rolled 300 times. How many sixes are expected?', '50', ['60', '6', '30'], '1/6 × 300 = 50.'),
           ('P(win) = 0.15 for a game played 40 times. How many wins are expected?', '6', ['15', '4', '0.15'], '0.15 × 40 = 6.'),
           ('In a fair two-player game, each player’s chance of winning is:', '1/2', ['1/4', '1', '0'], 'Equal chances.')],
    why=[('Explain why the expected number of sixes in 60 rolls is 10, even though you might not get exactly 10.', 'Expected frequency = 1/6 × 60 = 10 is the long-run average; random variation means the actual count usually differs slightly.'),
         ('Explain how you can decide whether a game is fair.', 'Work out each player’s probability of winning (or expected gain); the game is fair if they are equal (or the expected gain is zero).'),
         ('Explain why a fairground stall that charges to play is usually not a fair game for the player.', 'The prizes are set so that, on average, the stall takes in more money than it pays out; the player’s expected gain is negative.')],
    misc=[('If P(rain) = 0.2, it will rain on exactly 6 days in a 30-day month.', 'Expected number is 0.2 × 30 = 6, but the actual number can vary.'),
          ('A game where you win on a 6 and lose otherwise is fair because there are two results.', 'P(win) = 1/6 and P(lose) = 5/6, so the game is not fair.')],
))


@R.add('ch12-st4', 'C3', (1, 4), 'short')
def expected_freq(rng, slot):
    kind = rng.choice(['dice', 'spinner', 'prob'])
    N = rng.choice([60, 120, 180, 240, 300, 600])
    if kind == 'dice':
        ev = rng.choice([('a 6', 1), ('an even number', 3), ('a number greater than 4', 2), ('a 1 or a 2', 2)])
        return short(f'A fair six-sided dice is rolled {N} times. How many times would you expect to roll {ev[0]}?', str(N * ev[1] // 6),
                     f'P = {fx(Fr(ev[1], 6))} (A1); × {N} = {N * ev[1] // 6} (M1 A1).', 2)
    if kind == 'spinner':
        s = rng.choice([5, 8, 10])
        k = rng.randint(1, s - 1)
        e = Fr(k * N, s)
        return short(f'A fair spinner has {s} equal sections, {k} of which are blue. It is spun {N} times. Find the expected number of blues.', g(float(e), 4),
                     f'{k}/{s} × {N} (M1) = {g(float(e), 4)} (A1).', 2)
    p = Fr(rng.randint(1, 19), 20)
    city = rng.choice(CITIES)
    days = rng.choice([30, 31, 90, 365])
    return short(f'The probability of a delayed train on a route in {city} is {float(p):g} on any day. Estimate the number of days with a delay over {days} days.', g(float(p * days), 4),
                 f'{float(p):g} × {days} (M1) = {g(float(p * days), 4)} (A1).', 2)


@R.add('ch12-st4', 'C3', (2, 5), 'short')
def fair_game(rng, slot):
    cost = rng.choice([1, 2, 5])
    prize = rng.choice([4, 5, 6, 8, 10, 12])
    s = 6
    win = rng.randint(1, 2)
    city, country, cur, cname = place(rng)
    plays = rng.choice([60, 120, 300])
    exp_gain = Fr(win, s) * prize - cost
    return short(f'At a school fair in {city} it costs {cur}{cost} to roll a fair dice. If you roll {"a 6" if win == 1 else "a 5 or a 6"}, you win {cur}{prize} (and your stake is kept by the stall). (a) Find the expected profit or loss for the stall from {plays} games. (b) Is the game fair for the player? Explain.',
                 f'(a) stall takes {cur}{cost * plays}, expected pay-out {cur}{g(float(Fr(win, s) * prize * plays), 5)}: {"profit" if exp_gain < 0 else "loss" if exp_gain > 0 else "break-even"} {cur}{g(abs(float(exp_gain * plays)), 5)} (b) ' + ('fair' if exp_gain == 0 else 'not fair – the expected gain per game for the player is ' + ('negative' if exp_gain < 0 else 'positive')),
                 f'Expected wins {fx(Fr(win, s))} × {plays} = {g(float(Fr(win * plays, s)))} (M1 A1); money in vs money out (M1 A1); conclusion on fairness (R1).', 5)


@R.add('ch12-st4', 'C1', (1, 3), 'mcq')
def expected_mcq(rng, slot):
    p = rng.choice([Fr(1, 4), Fr(1, 5), Fr(2, 5), Fr(3, 10), Fr(1, 3)])
    N = rng.choice([60, 90, 120, 150, 300])
    e = p * N
    if e.denominator != 1:
        return None
    return mcq(rng, f'An event has probability {frac(p)}. How many times would you expect it to happen in {N} trials?', str(e), [str(N - e), str(N // p.denominator + 1), str(p.numerator * 10)],
               f'{frac(p)} × {N} = {e}.')


@R.add('ch12-st4', 'C2', (2, 4), 'explain')
def fairness_explain(rng, slot):
    who, who2 = two_names(rng)
    kind = rng.choice(['sum', 'coins'])
    if kind == 'sum':
        return explain(f'{who} and {who2} roll two dice. {who} wins if the total is even and {who2} wins if it is odd. Explain whether this game is fair.',
                       'Fair: 18 of the 36 outcomes give an even total and 18 give an odd total, so each has probability 1/2.',
                       'Sample space used (M1); counts 18 and 18 (A1); conclusion (R1).', 3)
    return explain(f'{who} tosses two coins. {who} scores a point for two heads; {who2} scores a point for one head and one tail. Explain whether the game is fair.',
                   'Not fair: P(two heads) = 1/4 but P(one of each) = 2/4 = 1/2, so the second player is twice as likely to score.',
                   'Four outcomes listed (M1); probabilities (A1); conclusion (R1).', 3)


@R.add('ch12-st4', 'C4', (3, 5), 'multi_step')
def design_game(rng, slot):
    city, country, cur, cname = place(rng)
    cost = rng.choice([1, 2, 3])
    plays = rng.choice([100, 200, 300])
    return short(f'A charity stall in {city} charges {cur}{cost} per game. Players spin a fair spinner with 10 equal sections. (a) Design prizes so that the stall expects to make a profit of about {cur}{cost * plays // 4} from {plays} games, showing your calculations. (b) Explain why the stall could still lose money on a particular day. (c) Explain whether your game is fair to the players.',
                 f'(a) e.g. 1 winning section with a prize of {money(cur, cost * 10 * 3 / 4)}: expected pay-out per game {money(cur, cost * 3 / 4)}, profit {money(cur, cost / 4)} per game × {plays} = {cur}{cost * plays // 4} (b) the results are random; more winners than expected can occur (c) not fair – the player’s expected gain is negative (that is how the charity raises money)',
                 'Expected pay-out calculated (M1 A1); profit target met (A1); variability explained (R1); fairness discussed (R1 C1).', 6, 'multi_step', 'G5')
