"""IB DP Mathematics: Analysis & Approaches SL/HL (2019 guide), DP year 1 – ib-g11-maths.

Paper conventions used in the items (as in the year-2 pack, whose formatting helpers are reused):
  * Paper 1 (no calculator) – exact answers (surds, fractions, logarithms, π); tagged style 'p1'.
  * Paper 2 (GDC allowed)   – answers to 3 significant figures unless stated; style 'p2'.
  * Section B / extended    – multi-part structured questions; style 'ext'.
  * HL Paper 3              – extended problem-solving / generalising questions; style 'p3'.
Markschemes use M1 (method), A1 (accuracy), R1 (reasoning), AG (answer given), (M1)/(A1) for implied marks.
Every numerical answer is computed (sympy / fractions / math), never typed in by hand.
"""
from __future__ import annotations

import math
import re
from fractions import Fraction as Fr

import sympy as sp

from _common import F, Registry, name, CITIES
from ib_g12_maths import (P, nice, s3, sfig, sci, nz, who, mk, build_parts, mcq, fixminus, nsols, lst, line_eq, _SUP, _iv_txt,
                          pt, V, ijk, x, y, t, pi, r2, r3)

import ib_g12_maths as _g12

CONFIG = {'minutesPerMark': 1.1, 'mcqMinutes': 1.5}


def _tidy(s_):
    """year-1 display touches on top of the year-2 helpers: e^2 -> e², e^(−2) -> e⁻²"""
    if not isinstance(s_, str):
        return s_
    s_ = re.sub(r'e\^(\d+)(?![\d.])', lambda m_: 'e' + m_.group(1).translate(_SUP), s_)
    s_ = re.sub(r'e\^\(−(\d+)\)', lambda m_: 'e⁻' + m_.group(1).translate(_SUP), s_)
    s_ = re.sub(r'e\^x(?![\w(])', 'eˣ', s_)
    s_ = re.sub(r'(?<=[\d)])\^(−?\d+)(?![\d.])', lambda m_: m_.group(1).replace('−', '-').translate(_SUP), s_)
    return s_


def _tidy_item(d):
    if d:
        for k_ in ('stem', 'answer', 'markingKey'):
            if k_ in d:
                d[k_] = _tidy(d[k_])
        if d.get('options'):
            d['options'] = [_tidy(o) for o in d['options']]
    return d


def s3(v):
    return _g12.s3(round(float(v), 9))


def mk(*a, **kw):
    return _tidy_item(_g12.mk(*a, **kw))


def build_parts(*a, **kw):
    return _tidy_item(_g12.build_parts(*a, **kw))


def mcq(*a, **kw):
    return _tidy_item(_g12.mcq(*a, **kw))

# One mock = the three HL papers in miniature (26 items), as in examPattern: Paper 1 (no GDC) Section A short +
# Section B extended, Paper 2 (GDC) Section A short + Section B extended, Paper 3 extended problem-solving.
MOCK = [
    dict(section='Paper 1 Section A – short response, no calculator', count=9, c=['C2', 'C3', 'C3'], d=[2, 3, 3], type='short', marks=6, style='p1'),
    dict(section='Paper 1 Section B – extended response, no calculator', count=3, c=['C4'], d=[4, 4, 5], type='multi_step', marks=15, style='ext'),
    dict(section='Paper 2 Section A – short response, calculator allowed', count=9, c=['C3', 'C2', 'C3'], d=[2, 3, 3], type='short', marks=6, style='p2'),
    dict(section='Paper 2 Section B – extended response, calculator allowed', count=3, c=['C4'], d=[4, 5, 4], type='multi_step', marks=15, style='ext'),
    dict(section='Paper 3 – extended problem-solving (HL)', count=2, c=['C4'], d=[5], type='multi_step', marks=20, style='p3'),
]

R = Registry()
SUB = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')


def init(subject_id):
    pass


def templates(st):
    return R.build(st, {'eval_marks': 6, 'essay_marks': 8,
                        'markband': 'Criterion-referenced: clear mathematical reasoning, correct notation, a justified conclusion.'})


def sup(n):
    return str(n).translate(_SUP)


def sub(n):
    return str(n).translate(SUB)


def R_(v):
    """exact rational text"""
    return P(sp.nsimplify(v))


def stdf(v, sf=3):
    """standard form a × 10ᵏ to sf significant figures"""
    v = float(v)
    if v == 0:
        return '0'
    k = math.floor(math.log10(abs(v)))
    a = v / 10 ** k
    a = round(a, sf - 1)
    if abs(a) >= 10:
        a /= 10
        k += 1
    at = f'{a:.{sf - 1}f}'.replace('-', '−')
    return f'{at} × 10{sup(k)}'.replace('⁻', '⁻') if k != 0 else at


def ordn(n):
    n = int(n)
    suf = 'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f'{n}{suf}'


def money(v, cur='$'):
    return f'{cur}{v:,.2f}'


def poly_txt(e, var=x):
    """polynomial in descending powers"""
    p_ = sp.Poly(sp.expand(e), var)
    out = ''
    for (k,), c in sorted(p_.terms(), key=lambda tc: -tc[0][0]):
        c = sp.nsimplify(c)
        if c == 0:
            continue
        mag_ = abs(c)
        v = '' if k == 0 else (str(var) if k == 1 else f'{var}{sup(k)}')
        coef = P(mag_) if (mag_ != 1 or k == 0) else ''
        if coef and v and '/' in coef:
            coef = f'({coef})'
        term = coef + v
        if not out:
            out = ('−' if c < 0 else '') + term
        else:
            out += (' − ' if c < 0 else ' + ') + term
    return out or '0'


# =============================================================================================
# ch01 Sequences and series (SL 1.1–1.4, 1.8)
# =============================================================================================
R.facts('ch01-st1', F(
    terms=[('standard form (scientific notation)', 'writing a number as a × 10ᵏ with 1 ≤ a < 10 and k an integer'),
           ('significant figures', 'the digits of a number that carry meaning about its precision, counted from the first non-zero digit'),
           ('order of magnitude', 'the power of 10 in the standard form of a number, used to compare sizes')],
    facts=[('Which number is written in standard form?', '4.07 × 10⁻³', ['40.7 × 10⁻⁴', '0.407 × 10⁻²', '4.07 × 10^(−3.5)'], '1 ≤ a < 10 and the exponent is an integer.'),
           ('0.000 052 in standard form is', '5.2 × 10⁻⁵', ['5.2 × 10⁻⁴', '5.2 × 10⁵', '52 × 10⁻⁶'], 'Move the decimal point 5 places.'),
           ('(3 × 10⁴)(2 × 10⁵) =', '6 × 10⁹', ['6 × 10²⁰', '5 × 10⁹', '6 × 10¹'], 'Multiply the numbers, add the exponents.'),
           ('(8 × 10⁶) ÷ (4 × 10⁹) =', '2 × 10⁻³', ['2 × 10³', '2 × 10¹⁵', '4 × 10⁻³'], 'Divide the numbers, subtract the exponents.')],
    why=[('Explain why 34.5 × 10⁶ is not written in standard form, and correct it.', 'The number in front must satisfy 1 ≤ a < 10; 34.5 × 10⁶ = 3.45 × 10⁷.'),
         ('Explain why scientists write very large and very small quantities in standard form.', 'It shows the order of magnitude at a glance, avoids long strings of zeros and makes multiplication and division easy by adding or subtracting exponents.'),
         ('Explain how to add 3.2 × 10⁵ and 4.1 × 10⁴ in standard form.', 'Rewrite with the same power of ten: 3.2 × 10⁵ + 0.41 × 10⁵ = 3.61 × 10⁵; exponents are not simply added.')],
    misc=[('(2 × 10³) + (3 × 10³) = 5 × 10⁶.', 'Only the numbers are added when the powers are equal: 5 × 10³.'),
          ('6 × 10⁻⁴ is a negative number.', 'A negative exponent gives a small positive number: 6 × 10⁻⁴ = 0.0006.')],
))


def _sf_num(rng):
    a = rng.randint(11, 99) / 10
    k = rng.randint(-9, 12)
    return a, k


@R.add('ch01-st1', 'C1', (1, 3), 'mcq')
def sci_write_mcq(rng, slot):
    sig = rng.choice([rng.randint(11, 99), rng.randint(101, 999)])
    k = rng.choice([-7, -6, -5, -4, -3, 3, 4, 5, 6, 7, 8])
    v = Fr(sig) * Fr(10) ** k
    digits = len(str(sig))
    mant = sig / 10 ** (digits - 1)
    e = k + digits - 1
    txt = f'{v.numerator / v.denominator:.{max(0, -k)}f}' if k < 0 else f'{int(v):,}'.replace(',', ' ')
    mt = f'{mant:g}'
    right = f'{mt} × 10{sup(e)}'
    wr = [f'{mt} × 10{sup(e + 1)}', f'{mt} × 10{sup(e - 1)}', f'{mt} × 10{sup(-e)}']
    return mcq(rng, f'Write {txt} in the form a × 10ᵏ, where 1 ≤ a < 10 and k ∈ ℤ.', right, wr, f'The decimal point moves {abs(e)} places, so k = {e}.')


@R.add('ch01-st1', 'C3', (1, 4), 'short', style='p1')
def sci_ops(rng, slot):
    a1, k1 = rng.randint(2, 9), rng.randint(-6, 9)
    a2, k2 = rng.randint(2, 9), rng.randint(-6, 9)
    op = rng.choice(['×', '÷', '+'] if slot.d >= 3 else ['×', '÷'])
    A = Fr(a1) * Fr(10) ** k1
    B = Fr(a2) * Fr(10) ** k2
    if op == '+':
        if abs(k1 - k2) != 1:
            k2 = k1 - 1
            B = Fr(a2) * Fr(10) ** k2
        v = A + B
    else:
        v = A * B if op == '×' else A / B
    fv = v.numerator / v.denominator
    ans = stdf(fv, 3 if op != '+' else 2)
    ans = re.sub(r'\.?0+ ×', ' ×', ans) if '.' in ans.split(' ')[0] else ans
    return mk(f'Without a calculator, find ({a1} × 10{sup(k1)}) {op} ({a2} × 10{sup(k2)}), giving your answer in the form a × 10ᵏ where 1 ≤ a < 10, k ∈ ℤ.', ans,
              ('multiply/divide the numbers and add/subtract the indices (M1)' if op != '+' else 'rewrite with a common power of 10 (M1)') + f'; adjust so that 1 ≤ a < 10 (M1); {ans} (A1).', 3)


SCI_CTX = [
    ('Light travels at 3.00 × 10⁸ m s⁻¹. The mean distance from the Sun to {p} is {d} × 10{e} m. Find the time, in seconds, for light to travel from the Sun to {p}.',
     [('Mercury', 5.79, 10), ('Venus', 1.08, 11), ('Mars', 2.28, 11), ('Jupiter', 7.78, 11), ('Saturn', 1.43, 12), ('Neptune', 4.50, 12)], lambda d, e: d * 10 ** e / 3e8, 's'),
    ('The mass of one hydrogen atom is 1.67 × 10⁻²⁷ kg. Find the number of hydrogen atoms in {d} × 10{e} kg of hydrogen.',
     [(None, 2.5, -3), (None, 4.0, -2), (None, 1.2, 1), (None, 7.5, -4), (None, 3.6, 2)], lambda d, e: d * 10 ** e / 1.67e-27, 'atoms'),
    ('The population of {p} is about {d} × 10{e}. Its government debt is 1.24 × 10¹² US dollars. Find the debt per person.',
     [('Canada', 3.97, 7), ('Australia', 2.66, 7), ('Spain', 4.81, 7), ('Kenya', 5.51, 7), ('Peru', 3.40, 7), ('Malaysia', 3.43, 7)], lambda d, e: 1.24e12 / (d * 10 ** e), 'US dollars'),
    ('A red blood cell has a diameter of about 7.5 × 10⁻⁶ m. Find how many such cells would fit in a line of length {d} × 10{e} m.',
     [(None, 1.5, 0), (None, 3.0, -1), (None, 2.4, 1), (None, 9.0, -2), (None, 4.2, 3)], lambda d, e: d * 10 ** e / 7.5e-6, 'cells'),
]


@R.add('ch01-st1', 'C3', (2, 5), 'short', style='p2')
def sci_context(rng, slot):
    frame, data, fn, unit = rng.choice(SCI_CTX)
    p, d, e = rng.choice(data)
    v = fn(d, e)
    stem = frame.format(p=p, d=f'{d:.2f}' if d * 100 % 10 else f'{d:.1f}', e=sup(e))
    return mk(stem + ' Give your answer in the form a × 10ᵏ, where 1 ≤ a < 10, k ∈ ℤ, to 3 significant figures.', f'{stdf(v)} {unit}',
              f'Correct operation set up (M1); evaluate (A1); {stdf(v)} {unit} (A1).', 3)


@R.add('ch01-st1', 'C2', (2, 4), 'explain')
def sci_error_explain(rng, slot):
    a1, a2 = rng.randint(2, 9), rng.randint(2, 9)
    k1, k2 = rng.randint(2, 8), rng.randint(2, 8)
    kind = rng.choice(['mult', 'add'])
    if kind == 'mult':
        wrong = f'{a1 * a2} × 10{sup(k1 * k2)}'
        prod = a1 * a2
        right = stdf(prod * 10 ** (k1 + k2), 2 if prod >= 10 else 1)
        right = re.sub(r'\.0 ×', ' ×', right)
        return mk(f'{who(rng)} writes ({a1} × 10{sup(k1)}) × ({a2} × 10{sup(k2)}) = {wrong}. Explain the errors and give the correct answer in standard form.', right,
                  f'Indices should be added, not multiplied: 10{sup(k1)} × 10{sup(k2)} = 10{sup(k1 + k2)} (R1); {prod} must be rewritten so that 1 ≤ a < 10 if necessary (R1); {right} (A1).', 3, 'explain')
    k2 = k1
    return mk(f'{who(rng)} writes ({a1} × 10{sup(k1)}) + ({a2} × 10{sup(k2)}) = {a1 + a2} × 10{sup(2 * k1)}. Explain the error and give the correct answer in standard form.',
              re.sub(r'\.0 ×', ' ×', stdf((a1 + a2) * 10 ** k1, 2)), f'When adding, the powers of 10 are not added; factor out 10{sup(k1)} (R1 M1); {re.sub(r".0 ×", " ×", stdf((a1 + a2) * 10 ** k1, 2))} (A1).', 3, 'explain')


@R.add('ch01-st1', 'C4', (3, 5), 'multi_step', style='ext')
def sci_parts(rng, slot):
    name_, r_km, dist = rng.choice([('the Moon', 1.737e6, 3.84e8), ('Mars', 3.39e6, 2.25e11), ('Venus', 6.05e6, 4.14e10), ('Jupiter', 6.99e7, 6.29e11)])
    speed = rng.choice([1.1e4, 1.5e4, 2.0e4, 8.0e3])
    V_ = 4 / 3 * math.pi * r_km ** 3
    T_ = dist / speed
    days = T_ / 86400
    parts = [(f'The radius of {name_} is {stdf(r_km)} m. Find its volume, assuming it is a sphere.', f'{stdf(V_)} m³', 'V = (4/3)πr³ (M1) A1', 2, True),
             (f'A spacecraft travels {stdf(dist)} m to {name_} at an average speed of {stdf(speed, 2)} m s⁻¹. Find the time taken in seconds.', f'{stdf(T_)} s', 'time = distance ÷ speed (M1) A1', 2, True),
             ('Convert this time to days, to 3 significant figures.', s3(days) + ' days', '÷ 86 400 (M1) A1', 2, True),
             ('State the order of magnitude of the time in seconds.', f'10{sup(math.floor(math.log10(T_)))}', 'A1', 1, False),
             ('Explain why the answer to the time calculation is only an estimate.', 'speed and distance vary; the path is not a straight line', 'R1', 1, False)]
    return build_parts(rng, [f'This question is about a mission to {name_}. Give answers in standard form to 3 significant figures where appropriate.', f'Scientific notation is used to describe a journey to {name_}.'], parts, 3)


# ---------------------------------------------------------------------------------------------
R.facts('ch01-st2', F(
    terms=[('arithmetic sequence', 'a sequence with a constant difference d between consecutive terms: uₙ = u₁ + (n − 1)d'),
           ('common difference', 'the constant amount d = uₙ₊₁ − uₙ added to each term of an arithmetic sequence to get the next'),
           ('arithmetic series', 'the sum of the terms of an arithmetic sequence: Sₙ = (n/2)(2u₁ + (n − 1)d) = (n/2)(u₁ + uₙ)'),
           ('sigma notation', 'a compact way of writing a sum: Σ from r = 1 to n of f(r) means f(1) + f(2) + … + f(n)')],
    facts=[('The nth term of an arithmetic sequence is', 'u₁ + (n − 1)d', ['u₁ + nd', 'u₁dⁿ⁻¹', 'n(u₁ + d)'], 'Formula booklet.'),
           ('The common difference of 17, 13, 9, 5, … is', '−4', ['4', '−5', '13/17'], 'Subtract consecutive terms.'),
           ('Σ from r = 1 to 5 of (2r + 1) =', '35', ['11', '30', '25'], '3 + 5 + 7 + 9 + 11.'),
           ('The sum of the first 100 positive integers is', '5050', ['5000', '10 100', '4950'], '(100/2)(1 + 100).')],
    why=[('Explain why the formula Sₙ = (n/2)(u₁ + uₙ) works for an arithmetic series.', 'Writing the series forwards and backwards and adding pairs each term with its mirror term; every pair sums to u₁ + uₙ, there are n pairs, so 2Sₙ = n(u₁ + uₙ).'),
         ('Explain how to decide whether a sequence is arithmetic.', 'Check that the difference between every pair of consecutive terms is the same; a single constant difference d means the sequence is arithmetic.'),
         ('Explain why the graph of the terms of an arithmetic sequence against n lies on a straight line.', 'uₙ = dn + (u₁ − d) is a linear function of n with gradient d.')],
    misc=[('In 5, 8, 11, …, the 20th term is 5 + 20 × 3 = 65.', 'The 20th term is u₁ + 19d = 5 + 57 = 62.'),
          ('The sequence 2, 4, 8, 16, … is arithmetic because it increases.', 'The differences 2, 4, 8 are not constant; it is geometric with ratio 2.')],
))


def ap_terms(a, d, k=4):
    return ', '.join(R_(a + i * d) for i in range(k))


AP_CTX = [
    ('A theatre has {n} rows. The first row has {a} seats and each row has {d} more seats than the row in front.', 'seats', 'Find the number of seats in the last row.', 'Find the total number of seats.'),
    ('{who} saves {a} euros in the first week and increases the amount saved by {d} euros each week for {n} weeks.', 'euros', 'Find the amount saved in the final week.', 'Find the total amount saved.'),
    ('A pile of logs has {a} logs in the top layer, with each layer below having {d} more logs than the layer above. There are {n} layers.', 'logs', 'Find the number of logs in the bottom layer.', 'Find the total number of logs.'),
    ('A runner trains for {n} days, running {a} km on day 1 and increasing the distance by {d} km each day.', 'km', 'Find the distance run on the last day.', 'Find the total distance run.'),
]


@R.add('ch01-st2', 'C3', (1, 4), 'short', style='p1')
def ap_nth(rng, slot):
    a, d = rng.randint(-10, 20), nz(rng, -7, 9)
    kind = rng.choice(['nth', 'two', 'which'] if slot.d >= 2 else ['nth'])
    if kind == 'nth':
        n = rng.randint(12, 60)
        return mk(f'The first four terms of an arithmetic sequence are {ap_terms(a, d)}. Find the {ordn(n)} term.', R_(a + (n - 1) * d),
                  f'd = {d} (A1); u{sub(n)} = {a} + ({n} − 1)({d}) (M1); {a + (n - 1) * d} (A1).', 3)
    if kind == 'two':
        p, q = sorted(rng.sample(range(2, 15), 2))
        up, uq = a + (p - 1) * d, a + (q - 1) * d
        return mk(f'In an arithmetic sequence, u{sub(p)} = {up} and u{sub(q)} = {uq}. Find the first term and the common difference.', f'u₁ = {a}, d = {d}',
                  f'u₁ + {p - 1}d = {up}, u₁ + {q - 1}d = {uq} (M1 A1); subtract: {q - p}d = {uq - up} (M1); d = {d}, u₁ = {a} (A1 A1).', 5)
    n = rng.randint(15, 80)
    L = a + (n - 1) * d
    return mk(f'The arithmetic sequence {ap_terms(a, d)}, … has a term equal to {L}. Find which term it is.', f'the {ordn(n)} term',
              f'{a} + (n − 1)({d}) = {L} (M1); n − 1 = {n - 1} (A1); n = {n} (A1).', 3)


@R.add('ch01-st2', 'C3', (2, 5), 'short', style='p1')
def ap_sum(rng, slot):
    a, d = rng.randint(-8, 15), nz(rng, -5, 6)
    kind = rng.choice(['sum', 'findn', 'sigma', 'last'])
    if kind == 'sum':
        n = rng.randint(10, 40)
        S = Fr(n, 2) * (2 * a + (n - 1) * d)
        return mk(f'Find the sum of the first {n} terms of the arithmetic series {" + ".join(R_(a + i * d) for i in range(3))} + ….'.replace('+ −', '− '), R_(S),
                  f'd = {d} (A1); S{sub(n)} = ({n}/2)(2({a}) + {n - 1}({d})) (M1); {R_(S)} (A1).', 3)
    if kind == 'findn':
        if d < 0 or a <= 0:
            a, d = rng.randint(1, 9), rng.randint(1, 5)
        n = rng.randint(8, 30)
        S = n * (2 * a + (n - 1) * d) // 2 if (n * (2 * a + (n - 1) * d)) % 2 == 0 else None
        if S is None:
            return None
        return mk(f'The sum of the first n terms of the series {a} + {a + d} + {a + 2 * d} + … is {S}. Find n.', f'n = {n}',
                  f'(n/2)(2({a}) + (n − 1)({d})) = {S} (M1); {d}n² + {2 * a - d}n − {2 * S} = 0 (A1); solve, reject the negative root (M1 R1); n = {n} (A1).'.replace('+ −', '− '), 5)
    if kind == 'sigma':
        p, q = nz(rng, -5, 7), rng.randint(-9, 9)
        n = rng.randint(10, 30)
        S = sum(p * r + q for r in range(1, n + 1))
        return mk(f'Find the value of Σ from r = 1 to {n} of ({poly_txt(p * x + q).replace("x", "r")}).', str(S),
                  f'Arithmetic with u₁ = {p + q}, d = {p} (M1); S{sub(n)} = ({n}/2)({p + q} + {p * n + q}) (M1); {S} (A1).', 3)
    n = rng.randint(10, 30)
    L = a + (n - 1) * d
    S = Fr(n, 2) * (a + L)
    return mk(f'An arithmetic series has first term {a}, last term {L} and {n} terms. Find its sum and the common difference.', f'S = {R_(S)}, d = {d}',
              f'S = ({n}/2)({a} + {L}) (M1) = {R_(S)} (A1); {L} = {a} + {n - 1}d (M1); d = {d} (A1).', 4)


@R.add('ch01-st2', 'C3', (2, 4), 'short', style='p2')
def ap_context(rng, slot):
    frame, unit, q1, q2 = rng.choice(AP_CTX)
    a, d, n = rng.randint(8, 30), rng.randint(2, 6), rng.randint(12, 40)
    L = a + (n - 1) * d
    S = n * (a + L) // 2 if n * (a + L) % 2 == 0 else n * (a + L) / 2
    return mk(frame.format(a=a, d=d, n=n, who=who(rng)) + f' (a) {q1} (b) {q2}', f'(a) {L} {unit} (b) {S:g} {unit}',
              f'(a) u{sub(n)} = {a} + {n - 1}({d}) (M1) = {L} (A1). (b) S{sub(n)} = ({n}/2)({a} + {L}) (M1) = {S:g} (A1).', 4)


@R.add('ch01-st2', 'C1', (1, 3), 'mcq')
def ap_mcq(rng, slot):
    a, d = rng.randint(-5, 12), nz(rng, -6, 7)
    n = rng.randint(10, 30)
    right = a + (n - 1) * d
    wr = list(dict.fromkeys([a + n * d, a * n + d, a + (n - 2) * d, right + 2 * d]))
    wr = [w for w in wr if w != right][:3]
    return mcq(rng, f'The {ordn(n)} term of the arithmetic sequence {ap_terms(a, d)}, … is', str(right), [str(w) for w in wr], f'u{sub(n)} = u₁ + (n − 1)d = {a} + {n - 1}({d}).')


@R.add('ch01-st2', 'C2', (2, 4), 'explain')
def ap_check_explain(rng, slot):
    a, d = rng.randint(1, 12), rng.randint(2, 7)
    seq = [a + i * d for i in range(5)]
    if rng.random() < 0.5:
        j = rng.randint(2, 4)
        seq[j] += rng.choice([1, -1])
        diffs = [seq[i + 1] - seq[i] for i in range(4)]
        return mk(f'Explain whether the sequence {", ".join(map(str, seq))}, … could be arithmetic.', 'not arithmetic: differences are not constant',
                  f'Differences are {", ".join(map(str, diffs))} (M1); not all equal, so no common difference (R1); not arithmetic (A1).', 3, 'explain')
    return mk(f'Explain why the sequence {", ".join(map(str, seq))}, … appears to be arithmetic and write down a formula for its nth term.', f'uₙ = {poly_txt(d * x + a - d).replace("x", "n")}',
              f'Each difference is {d} (R1); u₁ = {a} (A1); uₙ = {a} + (n − 1){d} = {poly_txt(d * x + a - d).replace("x", "n")} (A1).', 3, 'explain')


@R.add('ch01-st2', 'C4', (3, 5), 'multi_step', style='ext')
def ap_parts(rng, slot):
    a, d = rng.randint(-20, -3), rng.randint(2, 6)
    n1 = rng.randint(10, 20)
    S1 = n1 * (2 * a + (n1 - 1) * d) // 2 if n1 * (2 * a + (n1 - 1) * d) % 2 == 0 else None
    if S1 is None:
        return None
    first_pos = next(n for n in range(1, 500) if a + (n - 1) * d > 0)
    M = rng.choice([500, 1000, 2000])
    nM = next(n for n in range(1, 2000) if n * (2 * a + (n - 1) * d) / 2 > M)
    u3, u7 = a + 2 * d, a + 6 * d
    parts = [(f'Given that u₃ = {u3} and u₇ = {u7}, find the first term and the common difference.', f'u₁ = {a}, d = {d}', 'two equations (M1); solve (A1 A1)', 3, True),
             (f'Find the sum of the first {n1} terms.', str(S1), 'M1 A1', 2, True),
             ('Find the first term of the sequence that is positive.', f'u{sub(first_pos)} = {a + (first_pos - 1) * d}', 'inequality u₁ + (n − 1)d > 0 (M1) A1', 2, True),
             (f'Find the least value of n for which Sₙ > {M}.', f'n = {nM}', 'set up quadratic inequality (M1); solve with GDC or algebra (M1) A1', 3, True),
             ('Write the sum of the first n terms in sigma notation.', f'Σ from r = 1 to n of ({poly_txt(d * x + a - d).replace("x", "r")})', 'A1', 1, False)]
    return build_parts(rng, ['An arithmetic sequence has terms u₁, u₂, u₃, … .', 'Consider an arithmetic sequence with first term u₁ and common difference d.'], parts, 4)


@R.add('ch01-st2', 'C4', (4, 5), 'multi_step', style='p3')
def ap_proof_parts(rng, slot):
    p, q = rng.randint(2, 6), rng.randint(-5, 9)
    n_ = sp.Symbol('n')
    S = sp.expand(sp.summation(p * sp.Symbol('r') + q, (sp.Symbol('r'), 1, n_)))
    N = rng.choice([20, 30, 50])
    parts = [('Prove that the sum of the first n terms of an arithmetic series is Sₙ = (n/2)(2u₁ + (n − 1)d).', 'proof', 'write Sₙ forwards and backwards (M1); add (M1); 2Sₙ = n(2u₁ + (n − 1)d) (A1) AG', 3, True),
             (f'A sequence is defined by uᵣ = {p}r {"+" if q >= 0 else "−"} {abs(q)}. Show that it is arithmetic.', 'shown', f'uᵣ₊₁ − uᵣ = {p}, a constant (M1 R1)', 2, True),
             (f'Find an expression for Σ from r = 1 to n of uᵣ in its simplest form.', P(S).replace('n', 'n'), 'M1 A1', 2, True),
             (f'Hence find Σ from r = {N + 1} to {2 * N} of uᵣ.', str(S.subs(n_, 2 * N) - S.subs(n_, N)), f'S{sub(2 * N)} − S{sub(N)} (M1) A1', 2, True),
             ('Prove that if a, b, c are consecutive terms of an arithmetic sequence then b = (a + c)/2.', 'proof', 'b − a = c − b (M1); rearrange (A1)', 2, False)]
    return build_parts(rng, ['This question investigates arithmetic series and their sums.', 'In this question you will prove and use results about arithmetic series.'], parts, 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch01-st3', F(
    terms=[('geometric sequence', 'a sequence in which each term is a constant multiple r of the previous one: uₙ = u₁rⁿ⁻¹'),
           ('common ratio', 'the constant r = uₙ₊₁/uₙ by which each term of a geometric sequence is multiplied'),
           ('geometric series', 'the sum of terms of a geometric sequence: Sₙ = u₁(rⁿ − 1)/(r − 1), r ≠ 1')],
    facts=[('The common ratio of 48, −24, 12, −6, … is', '−1/2', ['1/2', '−2', '−24'], 'Divide consecutive terms.'),
           ('The nth term of a geometric sequence is', 'u₁rⁿ⁻¹', ['u₁rⁿ', 'u₁ + (n − 1)r', 'u₁nʳ'], 'Formula booklet.'),
           ('The sum 1 + 2 + 4 + … + 2⁹ equals', '1023', ['1024', '512', '2047'], 'S₁₀ = (2¹⁰ − 1)/(2 − 1).')],
    why=[('Explain why logarithms are needed to find the number of terms of a geometric sequence that are less than a given value.', 'The unknown n appears in the exponent of rⁿ⁻¹; taking logarithms brings it down so the inequality can be solved (or a GDC table used).'),
         ('Explain why a geometric sequence with 0 < r < 1 and positive first term decreases but never becomes negative.', 'Each term is a positive fraction of the previous one, so terms get smaller but a positive number times a positive r stays positive.'),
         ('Explain how to show that three numbers form consecutive terms of a geometric sequence.', 'Show the ratio of the second to the first equals the ratio of the third to the second (equivalently b² = ac).')],
    misc=[('The 10th term of 3, 6, 12, … is 3 × 2¹⁰.', 'u₁₀ = 3 × 2⁹ = 1536; the power is n − 1.'),
          ('In a geometric sequence with r = −2, the terms always increase.', 'The signs alternate, so the terms are not increasing: 1, −2, 4, −8, …')],
))


def gp_terms(a, r, k=4):
    return ', '.join(R_(a * r ** i) for i in range(k))


@R.add('ch01-st3', 'C3', (1, 4), 'short', style='p1')
def gp_nth(rng, slot):
    a = rng.choice([1, 2, 3, 4, 5, 6, 8, 81, 64, 96, 243])
    r = rng.choice([2, 3, -2, Fr(1, 2), Fr(-1, 2), Fr(1, 3), Fr(3, 2)])
    kind = rng.choice(['nth', 'two', 'sum'] if slot.d >= 2 else ['nth'])
    if Fr(r).denominator > 1:
        a = Fr(r).denominator ** rng.choice([4, 5]) * rng.choice([1, 2, 3]) if Fr(r).denominator == 2 else Fr(r).denominator ** 4 * rng.choice([1, 2])
    if kind == 'nth':
        n = rng.randint(5, 9) if Fr(r).denominator == 1 else rng.randint(4, 5)
        return mk(f'Find the {ordn(n)} term of the geometric sequence {gp_terms(a, r)}, ….', R_(a * r ** (n - 1)),
                  f'r = {R_(r)} (A1); u{sub(n)} = {a}({R_(r)}){sup(n - 1)} (M1); {R_(a * r ** (n - 1))} (A1).', 3)
    if kind == 'two':
        p = rng.randint(2, 3)
        q = p + rng.choice([2, 3])
        up, uq = a * r ** (p - 1), a * r ** (q - 1)
        ok = (q - p) % 2 == 1
        return mk(f'In a geometric sequence, u{sub(p)} = {R_(up)} and u{sub(q)} = {R_(uq)}. Find the common ratio{"" if ok else ", given that r > 0" if r > 0 else ", given that r < 0"}, and the first term.',
                  f'r = {R_(r)}, u₁ = {R_(a)}', f'r{sup(q - p)} = {R_(uq)}/{R_(up)} = {R_(r ** (q - p))} (M1 A1); r = {R_(r)} (A1); u₁ = {R_(up)}/({R_(r)}){sup(p - 1)} = {R_(a)} (A1).', 4)
    n = rng.randint(5, 10) if Fr(r).denominator == 1 else rng.randint(4, 5)
    S = a * (r ** n - 1) / (r - 1)
    return mk(f'Find the exact sum of the first {n} terms of the geometric series {" + ".join(R_(a * r ** i) for i in range(3))} + ….'.replace('+ −', '− '), R_(S),
              f'r = {R_(r)} (A1); S{sub(n)} = {a}(({R_(r)}){sup(n)} − 1)/({R_(r)} − 1) (M1); {R_(S)} (A1).', 3)


GP_CTX = [
    ('The population of a town is {a} and increases by {p}% each year.', 'Find the population after {n} years.', 'Find the number of complete years until the population first exceeds {T}.'),
    ('A ball is dropped and each bounce reaches {p}% of the height of the previous one. The first bounce reaches {a} cm.', 'Find the height of the {nth} bounce.', 'Find the first bounce whose height is less than {T} cm.'),
    ('A company sells {a} units in its first month and sales grow by {p}% per month.', 'Find the sales in month {n}.', 'Find the first month in which sales exceed {T} units.'),
    ('The value of a painting is {a} pounds and rises by {p}% per year.', 'Find its value after {n} years.', 'Find how many complete years it takes for the value to exceed {T} pounds.'),
]


@R.add('ch01-st3', 'C3', (2, 5), 'short', style='p2')
def gp_context(rng, slot):
    i = rng.randrange(len(GP_CTX))
    frame, q1, q2 = GP_CTX[i]
    if i == 1:
        a, p = rng.choice([200, 150, 180, 250]), rng.choice([60, 70, 75, 80])
        r = p / 100
        T = rng.choice([10, 20, 5])
        n = rng.randint(4, 7)
        val = a * r ** (n - 1)
        k = next(m for m in range(1, 200) if a * r ** (m - 1) < T)
        return mk(frame.format(a=a, p=p) + f' (a) {q1.format(nth=ordn(n))} (b) {q2.format(T=T)}', f'(a) {s3(val)} cm (b) bounce {k}',
                  f'(a) {a} × {r}{sup(n - 1)} (M1) = {s3(val)} (A1). (b) {a}({r})ⁿ⁻¹ < {T} (M1); logarithms or table (M1); n = {k} (A1).', 5)
    a, p = rng.choice([1200, 5000, 8000, 25000, 450]), rng.choice([2, 3, 4, 5, 6, 8])
    r = 1 + p / 100
    n = rng.randint(4, 12)
    T = a * rng.choice([2, 3, 1.5])
    T = int(T)
    val = round(a * r ** n if i != 2 else a * r ** (n - 1))
    k = next(m for m in range(1, 500) if (a * r ** m if i != 2 else a * r ** (m - 1)) > T)
    return mk(frame.format(a=a, p=p) + f' (a) {q1.format(n=n)} (b) {q2.format(T=T)}', f'(a) {val:,}'.replace(',', ' ') + f' (b) {k}',
              f'(a) r = {r:g} (A1); {a} × {r:g}{sup(n if i != 2 else n - 1)} ≈ {val} (A1). (b) inequality with {r:g}ⁿ (M1); logarithms or GDC table (M1); {k} (A1).', 5)


@R.add('ch01-st3', 'C3', (3, 5), 'short', style='p2')
def gp_sum_exceed(rng, slot):
    a, r = rng.choice([2, 3, 5, 10]), rng.choice([1.1, 1.2, 1.5, 2, 3])
    M = rng.choice([1000, 5000, 10 ** 4, 10 ** 5])
    n = next(m for m in range(1, 500) if a * (r ** m - 1) / (r - 1) > M)
    return mk(f'A geometric series has first term {a} and common ratio {r:g}. Find the least number of terms needed for the sum to exceed {M}.', f'n = {n}',
              f'{a}({r:g}ⁿ − 1)/({r:g} − 1) > {M} (M1); {r:g}ⁿ > {s3(M * (r - 1) / a + 1)} (A1); n > {s3(math.log(M * (r - 1) / a + 1) / math.log(r))} (M1); n = {n} (A1).', 4)


@R.add('ch01-st3', 'C1', (1, 3), 'mcq')
def gp_mcq(rng, slot):
    a = rng.choice([2, 3, 5, 4, 7])
    r = rng.choice([2, 3, -2, -3])
    n = rng.randint(5, 8)
    right = a * r ** (n - 1)
    wr = list(dict.fromkeys([a * r ** n, (a * r) ** (n - 1), a + (n - 1) * r, -right]))
    wr = [str(w) for w in wr if w != right][:3]
    return mcq(rng, f'The {ordn(n)} term of {gp_terms(a, r)}, … is', str(right), wr, f'u{sub(n)} = {a} × ({r}){sup(n - 1)}.')


@R.add('ch01-st3', 'C2', (2, 4), 'explain')
def gp_explain(rng, slot):
    a = rng.randint(2, 6)
    k = rng.randint(2, 5)
    b, c = a * k, a * k * k
    kind = rng.choice(['check', 'find'])
    if kind == 'check':
        return mk(f'Show that {a}, {b}, {c} are consecutive terms of a geometric sequence, and explain what the common ratio represents.', f'r = {k}',
                  f'{b}/{a} = {k} and {c}/{b} = {k} (M1 A1); each term is {k} times the previous term (R1).', 3, 'explain')
    p_ = sp.Symbol('p')
    # p, p + a, 4p + ... choose terms x, x+m, x+3m style solved
    m = rng.randint(2, 6)
    sols = sp.solve(sp.Eq((p_ + m) ** 2, p_ * (p_ + 3 * m + k)), p_)
    sols = [s_ for s_ in sols if s_.is_rational]
    if not sols:
        return None
    pv = sols[0]
    return mk(f'The numbers p, p + {m} and p + {3 * m + k} are consecutive terms of a geometric sequence. Explain why (p + {m})² = p(p + {3 * m + k}), and hence find p.', f'p = {R_(pv)}',
              f'Ratios equal: (p + {m})/p = (p + {3 * m + k})/(p + {m}) (R1); cross-multiply (M1); p = {R_(pv)} (A1).', 3, 'explain')


@R.add('ch01-st3', 'C4', (3, 5), 'multi_step', style='ext')
def gp_parts(rng, slot):
    a, r = rng.choice([3, 4, 5, 6]), rng.choice([2, 3])
    n = rng.randint(5, 8)
    M = rng.choice([10 ** 4, 10 ** 5, 10 ** 6])
    nM = next(m for m in range(1, 200) if a * (r ** m - 1) / (r - 1) > M)
    A1, dA = rng.randint(50, 200), rng.randint(20, 80)
    cross = next(m for m in range(1, 200) if a * r ** (m - 1) > A1 + (m - 1) * dA)
    parts = [(f'Write down the first four terms of the geometric sequence with u₁ = {a} and r = {r}.', gp_terms(a, r), 'A1', 1, True),
             (f'Find u{sub(n)} and S{sub(n)}.', f'{a * r ** (n - 1)}, {a * (r ** n - 1) // (r - 1)}', 'M1 A1 A1', 3, True),
             (f'Find the smallest n for which Sₙ > {M}.', f'n = {nM}', 'inequality (M1); logs or GDC (M1) A1', 3, True),
             (f'An arithmetic sequence has v₁ = {A1} and common difference {dA}. Find the smallest n for which uₙ > vₙ.', f'n = {cross}', 'compare terms with GDC table (M1) A1', 2, True),
             ('Explain why the geometric sequence will eventually exceed any arithmetic sequence.', 'exponential growth rⁿ⁻¹ (r > 1) outgrows any linear expression', 'R1', 1, False)]
    return build_parts(rng, ['This question compares geometric and arithmetic growth.', f'A geometric sequence has first term {a} and common ratio {r}.'], parts, 4)


@R.add('ch01-st3', 'C4', (4, 5), 'multi_step', style='p3')
def ap_gp_parts(rng, slot):
    a, d = rng.choice([(2, 3), (1, 3), (4, 4), (3, 6), (2, 6), (5, 5)])
    # u1, u2, u4 of an AP in GP: (a+d)^2 = a(a+3d) -> d = a
    d = a * rng.choice([1, 2]) if False else a
    r = sp.Rational(a + d, a)
    k = rng.randint(5, 8)
    parts = [('The first, second and fourth terms of an arithmetic sequence with first term a and common difference d ≠ 0 form a geometric sequence. Show that d = a.', 'shown', '(a + d)² = a(a + 3d) (M1); expand and simplify d² = ad (A1); d ≠ 0 (R1) AG', 3, True),
             (f'Given that a = {a}, find the common ratio of the geometric sequence.', R_(r), 'A1', 1, True),
             (f'Find the {ordn(k)} term of the geometric sequence.', R_(a * r ** (k - 1)), 'M1 A1', 2, True),
             ('Show that the first, third and ninth terms of the arithmetic sequence also form a geometric sequence.', 'shown', f'a, 3a, 9a: ratio 3 (M1 A1)', 2, True),
             ('Generalise: find a condition on m so that the terms u₁, uₘ, u_{m²} of this arithmetic sequence form a geometric sequence, and prove it.', 'true for all m ≥ 2: a, ma, m²a', 'uₘ = ma (A1); ratio m (R1)', 2, False)]
    return build_parts(rng, ['This question explores sequences that are both arithmetic and geometric in parts.', 'Arithmetic and geometric sequences are linked in this question.'], parts, 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch01-st4', F(
    terms=[('compound interest', 'interest calculated on the principal and on interest already earned: FV = PV(1 + r/(100k))^(kn)'),
           ('depreciation', 'the decrease in value of an asset over time, often by a fixed percentage of its value each year'),
           ('present value', 'the amount invested or borrowed at the start of a financial calculation (PV)'),
           ('inflation', 'the general increase in prices over time, which reduces the real value (purchasing power) of money')],
    facts=[('$1000 invested at 5% per annum compounded annually is worth after 2 years', '$1102.50', ['$1100.00', '$1050.00', '$1105.00'], '1000 × 1.05².'),
           ('A car worth $20 000 depreciates by 15% per year. After one year it is worth', '$17 000', ['$3 000', '$23 000', '$19 850'], '20 000 × 0.85.'),
           ('Compounding monthly at 6% per annum uses the factor', '(1 + 0.06/12)¹²ⁿ', ['(1.06)¹²ⁿ', '(1 + 0.06)ⁿ/12', '(1 + 0.5)¹²ⁿ'], 'k = 12 periods per year.')],
    why=[('Explain why compound interest grows faster than simple interest.', 'In compound interest the interest earned is added to the principal, so later interest is calculated on a larger amount; simple interest is always on the original principal.'),
         ('Explain why more frequent compounding gives a slightly larger final value.', 'Interest is added sooner, so it begins earning interest itself earlier; the effective annual rate (1 + r/k)ᵏ − 1 increases with k.'),
         ('Explain why depreciation by a fixed percentage never reduces the value to zero.', 'Each year the value is multiplied by (1 − r/100), a positive factor less than 1, so it decreases geometrically towards 0 without reaching it.')],
    misc=[('Depreciating by 10% per year for 2 years reduces the value by 20%.', 'The value is multiplied by 0.9² = 0.81: a 19% decrease.'),
          ('An interest rate of 12% per annum compounded monthly means 12% is added each month.', 'The monthly rate is 12%/12 = 1%.')],
))

CURS = [('$', 'dollars'), ('€', 'euros'), ('£', 'pounds'), ('CHF ', 'Swiss francs'), ('¥', 'yen')]
COMP = {1: 'annually', 2: 'half-yearly', 4: 'quarterly', 12: 'monthly'}


@R.add('ch01-st4', 'C3', (2, 5), 'short', style='p2')
def compound_fv(rng, slot):
    PV = rng.choice([1500, 2000, 2500, 5000, 8000, 12000, 750])
    r = rng.choice([2.5, 3, 3.5, 4, 4.2, 5, 6.5])
    k = rng.choice([1, 2, 4, 12])
    n = rng.randint(3, 15)
    cur, _ = rng.choice(CURS)
    kind = rng.choice(['fv', 'years', 'rate'])
    FV = PV * (1 + r / (100 * k)) ** (k * n)
    nm = who(rng)
    if kind == 'fv':
        return mk(f'{nm} invests {cur}{PV} at {r}% per annum, compounded {COMP[k]}. Find the value of the investment after {n} years, to the nearest cent.', money(FV, cur),
                  f'FV = {PV}(1 + {r}/{100 * k})^({k * n}) (M1 A1); {money(FV, cur)} (A1).', 3)
    if kind == 'years':
        T = PV * rng.choice([1.5, 2, 3])
        yrs = next(m for m in range(1, 200) if PV * (1 + r / (100 * k)) ** (k * m) >= T)
        return mk(f'{nm} invests {cur}{PV} at {r}% per annum, compounded {COMP[k]}. Find the number of complete years needed for the investment to reach at least {cur}{T:g}.', f'{yrs} years',
                  f'{PV}(1 + {r}/{100 * k})^({k}n) ≥ {T:g} (M1); solve with GDC/logarithms (M1); n ≥ {s3(math.log(T / PV) / (k * math.log(1 + r / (100 * k))))} (A1); {yrs} years (A1).', 4)
    FVr = round(FV, 2)
    rr = 100 * k * ((FVr / PV) ** (1 / (k * n)) - 1)
    return mk(f'An investment of {cur}{PV}, compounded {COMP[k]}, is worth {money(FVr, cur)} after {n} years. Find the annual interest rate.', f'{s3(rr)}%',
              f'{PV}(1 + r/{100 * k})^({k * n}) = {FVr} (M1 A1); GDC solver r = {s3(rr)}% (A1).', 3)


@R.add('ch01-st4', 'C3', (2, 5), 'short', style='p2')
def depreciation(rng, slot):
    item, V0 = rng.choice([('a car', 24000), ('a laptop', 1800), ('a tractor', 65000), ('an industrial printer', 9500), ('a delivery van', 32000), ('a phone', 1100), ('a motorbike', 8600), ('a camera', 2400)])
    p = rng.choice([8, 10, 12, 15, 18, 20, 25])
    n = rng.randint(3, 8)
    cur, _ = rng.choice(CURS)
    kind = rng.choice(['value', 'years', 'rate'])
    if kind == 'value':
        v = V0 * (1 - p / 100) ** n
        return mk(f'{item[0].upper() + item[1:]} is bought for {cur}{V0} and depreciates by {p}% per year. Find its value after {n} years.', money(v, cur),
                  f'{V0}(1 − {p / 100:g}){sup(n)} (M1 A1); {money(v, cur)} (A1).', 3)
    if kind == 'years':
        T = V0 * rng.choice([0.5, 0.25, 0.4])
        yrs = next(m for m in range(1, 200) if V0 * (1 - p / 100) ** m < T)
        return mk(f'{item[0].upper() + item[1:]} worth {cur}{V0} depreciates by {p}% per year. Find the number of complete years until its value first falls below {cur}{T:g}.', f'{yrs} years',
                  f'{V0}({1 - p / 100:g})ⁿ < {T:g} (M1); GDC/logarithms (M1); {yrs} (A1).', 3)
    v = round(V0 * (1 - p / 100) ** n, 2)
    rate = 100 * (1 - (v / V0) ** (1 / n))
    return mk(f'{item[0].upper() + item[1:]} bought for {cur}{V0} is worth {money(v, cur)} after {n} years. Find the annual rate of depreciation.', f'{s3(rate)}%',
              f'{V0}(1 − r/100){sup(n)} = {v} (M1 A1); r = {s3(rate)}% (A1).', 3)


@R.add('ch01-st4', 'C2', (2, 4), 'explain')
def finance_compare_explain(rng, slot):
    r = rng.choice([4, 5, 6, 8, 12])
    eff = {k: ((1 + r / (100 * k)) ** k - 1) * 100 for k in (1, 4, 12)}
    k = rng.choice([4, 12])
    return mk(f'Bank A offers {r}% per annum compounded annually; Bank B offers {r}% per annum compounded {COMP[k]}. Explain which is better for a saver, using the effective annual rate.', f'Bank B: effective rate {s3(eff[k])}% > {r}%',
              f'Effective rate for B = (1 + {r}/{100 * k}){sup(k)} − 1 (M1) = {s3(eff[k])}% (A1); larger than {r}% because interest is compounded more often (R1).', 3, 'explain')


@R.add('ch01-st4', 'C1', (1, 3), 'mcq')
def finance_mcq(rng, slot):
    PV = rng.choice([100, 200, 500, 1000])
    r = rng.choice([2, 4, 5, 10])
    n = rng.choice([2, 3])
    right = PV * (1 + r / 100) ** n
    wr = [PV * (1 + r * n / 100), PV * (1 + r / 100) ** (n + 1), PV * (1 + r / 100) * n]
    return mcq(rng, f'{PV} dollars is invested at {r}% per annum compound interest (annual). After {n} years it is worth', f'${right:.2f}', [f'${w:.2f}' for w in wr], f'{PV} × {1 + r / 100:g}{sup(n)}.')


@R.add('ch01-st4', 'C4', (3, 5), 'multi_step', style='ext')
def finance_parts(rng, slot):
    PV = rng.choice([10000, 15000, 20000, 6000])
    rA, rB = rng.choice([(4.5, 4.3), (3.8, 3.7), (5.2, 5.0), (6.0, 5.85)])
    kB = rng.choice([4, 12])
    n = rng.choice([5, 8, 10])
    inf = rng.choice([2, 2.5, 3])
    A = PV * (1 + rA / 100) ** n
    B = PV * (1 + rB / (100 * kB)) ** (kB * n)
    best = 'A' if A > B else 'B'
    real = max(A, B) / (1 + inf / 100) ** n
    double = next(m for m in range(1, 300) if PV * (1 + rA / 100) ** m >= 2 * PV)
    cur, _ = rng.choice(CURS)
    parts = [(f'Find the value of Option A after {n} years.', money(A, cur), 'M1 A1', 2, True),
             (f'Find the value of Option B after {n} years.', money(B, cur), 'M1 A1', 2, True),
             ('State which option is better, giving a reason.', f'Option {best}: larger final value', 'R1', 1, True),
             (f'Inflation is {inf}% per year. Find the real value, in today\'s money, of the better option after {n} years.', money(real, cur), f'÷ (1 + {inf / 100:g}){sup(n)} (M1) A1', 2, True),
             ('Find the number of complete years for Option A to double the investment.', f'{double} years', 'M1 A1', 2, False)]
    return build_parts(rng, [f'{who(rng)} has {cur}{PV} to invest. Option A pays {rA}% per annum compounded annually. Option B pays {rB}% per annum compounded {COMP[kB]}.',
                             f'Two savings accounts are compared for an investment of {cur}{PV}: A at {rA}% p.a. (annual compounding) and B at {rB}% p.a. compounded {COMP[kB]}.'], parts, 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch01-st5', F(
    terms=[('infinite geometric series', 'the sum u₁ + u₁r + u₁r² + … continued indefinitely'),
           ('sum to infinity', 'the limit of Sₙ as n → ∞ for a convergent geometric series: S∞ = u₁/(1 − r), valid when |r| < 1'),
           ('convergent series', 'a series whose partial sums Sₙ approach a finite limit as n → ∞')],
    facts=[('The infinite geometric series 8 + 4 + 2 + … has sum', '16', ['14', '∞', '32'], '8/(1 − ½).'),
           ('An infinite geometric series converges if and only if', '|r| < 1', ['r < 1', 'r > 0', '|r| > 1'], 'rⁿ → 0 only when |r| < 1.'),
           ('0.3̇ (0.333…) as a fraction is', '1/3', ['3/10', '33/100', '3/9 + 1'], '0.3/(1 − 0.1).')],
    why=[('Explain why the sum to infinity of a geometric series exists only when |r| < 1.', 'Sₙ = u₁(1 − rⁿ)/(1 − r); rⁿ → 0 as n → ∞ only if |r| < 1, giving S∞ = u₁/(1 − r); otherwise rⁿ does not tend to a limit (or grows) and the partial sums do not converge.'),
         ('Explain why a recurring decimal can be written as a fraction using a geometric series.', 'The repeating blocks form a geometric series with ratio 10⁻ᵏ (k = block length), which has |r| < 1, so its sum is a rational number u₁/(1 − r).')],
    misc=[('The series 1 + 2 + 4 + … has sum to infinity 1/(1 − 2) = −1.', 'r = 2, so |r| > 1 and the series diverges; the formula is not valid.'),
          ('Since the terms of a series tend to zero, the series must converge.', 'This holds for geometric series with |r| < 1, but not in general (e.g. 1 + ½ + ⅓ + … diverges).')],
))


@R.add('ch01-st5', 'C3', (1, 4), 'short', style='p1')
def sinf_basic(rng, slot):
    kind = rng.choice(['sum', 'findr', 'finda', 'recur'])
    a = rng.choice([6, 8, 9, 12, 18, 24, 27, 30, 36, 40])
    r = rng.choice([Fr(1, 2), Fr(1, 3), Fr(2, 3), Fr(-1, 2), Fr(-1, 3), Fr(3, 4), Fr(1, 4), Fr(-2, 3)])
    S = Fr(a) / (1 - r)
    if kind == 'sum':
        return mk(f'Find the sum to infinity of the geometric series {" + ".join(R_(a * r ** i) for i in range(3))} + ….'.replace('+ −', '− '), R_(S),
                  f'r = {R_(r)}, |r| < 1 (A1 R1); S∞ = {a}/(1 − ({R_(r)})) (M1); {R_(S)} (A1).', 4)
    if kind == 'findr':
        return mk(f'An infinite geometric series has first term {a} and sum to infinity {R_(S)}. Find the common ratio.', f'r = {R_(r)}',
                  f'{a}/(1 − r) = {R_(S)} (M1); 1 − r = {R_(1 - r)} (A1); r = {R_(r)} (A1).', 3)
    if kind == 'finda':
        return mk(f'An infinite geometric series has common ratio {R_(r)} and sum to infinity {R_(S)}. Find the first term and the third term.', f'u₁ = {a}, u₃ = {R_(a * r * r)}',
                  f'u₁ = {R_(S)}(1 − ({R_(r)})) (M1) = {a} (A1); u₃ = {a}({R_(r)})² = {R_(a * r * r)} (A1).', 3)
    blk = rng.choice(['3', '7', '27', '45', '12', '81', '6'])
    k = len(blk)
    frac_ = Fr(int(blk), 10 ** k - 1)
    return mk(f'By writing it as an infinite geometric series, express 0.{blk}{blk}{blk}… as a fraction in its simplest form.', R_(frac_),
              f'0.{blk} + 0.{"0" * k}{blk} + … with u₁ = {int(blk)}/10{sup(k)}, r = 1/10{sup(k)} (M1 A1); S∞ = {R_(frac_)} (A1).', 3)


@R.add('ch01-st5', 'C3', (3, 5), 'short', style='p1')
def sinf_range(rng, slot):
    a, b = rng.choice([1, 2, 3]), rng.choice([1, 2, 3, 4, 5])
    c = rng.choice([2, 3, 4, 5])
    # ratio = (a x - b)/c  -> |ratio| < 1
    xr = sp.Symbol('xr', real=True)
    Sset = sp.solve_univariate_inequality(sp.Abs((a * xr - b) / c) < 1, xr, relational=False)
    lo, hi = Sset.start, Sset.end
    ratio = f'({poly_txt(a * x - b)})/{c}'
    return mk(f'The infinite geometric series 1 + {ratio} + ({ratio})² + … converges. Find the set of possible values of x.', f'{P(lo)} < x < {P(hi)}',
              f'|{ratio}| < 1 (M1); −{c} < {poly_txt(a * x - b)} < {c} (A1); {P(lo)} < x < {P(hi)} (A1 A1).', 4)


@R.add('ch01-st5', 'C1', (1, 3), 'mcq')
def sinf_mcq(rng, slot):
    a = rng.choice([4, 6, 10, 12, 20])
    r = rng.choice([Fr(1, 2), Fr(1, 4), Fr(1, 5), Fr(-1, 2), Fr(1, 3)])
    S = Fr(a) / (1 - r)
    wr = [R_(Fr(a) / (1 + r)), R_(a * r / (1 - r)), R_(Fr(a) * (1 - r))]
    if len({R_(S), *wr}) < 4:
        return None
    return mcq(rng, f'The sum to infinity of the geometric series with u₁ = {a} and r = {R_(r)} is', R_(S), wr, f'S∞ = {a}/(1 − {R_(r)}).')


@R.add('ch01-st5', 'C2', (2, 4), 'explain')
def sinf_explain(rng, slot):
    r = rng.choice([Fr(3, 2), Fr(-5, 4), 2, Fr(4, 3), -3])
    a = rng.randint(2, 9)
    return mk(f'{who(rng)} calculates the sum to infinity of the geometric series with first term {a} and common ratio {R_(r)} as {a}/(1 − {R_(r)}) = {R_(Fr(a) / (1 - Fr(r)))}. Explain why this is wrong.', 'the series diverges since |r| ≥ 1',
              f'|r| = {R_(abs(Fr(r)))} > 1 (R1); rⁿ does not tend to 0, so Sₙ has no finite limit (R1); the formula S∞ = u₁/(1 − r) requires |r| < 1 (R1).', 3, 'explain')


@R.add('ch01-st5', 'C4', (3, 5), 'multi_step', style='ext')
def bounce_parts(rng, slot):
    h = rng.choice([2, 3, 4, 5, 8, 10])
    p = rng.choice([Fr(1, 2), Fr(3, 4), Fr(2, 3), Fr(3, 5), Fr(4, 5)])
    n = rng.randint(3, 6)
    hn = h * p ** n
    D = h + 2 * h * p / (1 - p)
    parts = [(f'Find the height reached after the {ordn(n)} bounce.', f'{R_(hn)} m', 'M1 A1', 2, True),
             ('Show that the total distance travelled by the ball is given by an infinite geometric series and find its sum.', f'{R_(D)} m', f'{h} + 2({h}×{R_(p)} + {h}×{R_(p)}² + …) (M1 A1); S∞ (M1) A1', 4, True),
             ('Find the first bounce whose height is less than 1 cm.', str(next(m for m in range(1, 300) if h * float(p) ** m < 0.01)), 'inequality with logarithms (M1) A1', 2, True),
             ('Explain why the model cannot be completely realistic.', 'it predicts infinitely many bounces', 'R1', 1, False)]
    return build_parts(rng, [f'A ball is dropped from a height of {h} m. After each bounce it rises to {R_(p)} of its previous height.', f'A ball falls from {h} m and each rebound height is {R_(p)} of the height before.'], parts, 3)


@R.add('ch01-st5', 'C4', (4, 5), 'multi_step', style='p3')
def sinf_param_parts(rng, slot):
    a = rng.choice([2, 3, 4, 6])
    k = sp.Symbol('k')
    S_target = rng.choice([sp.Rational(9, 2), 6, 8, sp.Rational(16, 3), 9])
    # series a + a(x) + ... with r = x : find x so that S = target
    xv = 1 - sp.Rational(a, 1) / S_target
    if not (-1 < xv < 1):
        return None
    parts = [(f'Consider the series {a} + {a}x + {a}x² + …. State the values of x for which it converges.', '−1 < x < 1', 'A1', 1, True),
             ('Find an expression for the sum to infinity in terms of x.', f'{a}/(1 − x)', 'A1', 1, True),
             (f'Find the value of x for which the sum to infinity is {P(S_target)}.', P(xv), 'M1 A1', 2, True),
             ('Show that the sum to infinity can never be less than ' + P(sp.Rational(a, 2)) + '.', 'shown', f'1 − x < 2 so {a}/(1 − x) > {P(sp.Rational(a, 2))} (M1 R1)', 2, True),
             (f'Find the least n for which Sₙ is within 0.001 of S∞ when x = {P(xv)}.', str(next(m for m in range(1, 1000) if abs(float(S_target * xv ** m)) < 0.001)), 'S∞ − Sₙ = S∞xⁿ (M1); solve (M1) A1', 3, False)]
    return build_parts(rng, ['This question investigates the convergence of a geometric series with a variable ratio.', f'Let S(x) = {a} + {a}x + {a}x² + ….'], parts, 4)


# =============================================================================================
# ch02 Exponents and logarithms (SL 1.5, 1.7)
# =============================================================================================
A_, B_ = sp.symbols('a b', positive=True)


def Pl(e):
    return re.sub(r'ln\((\d+)\)', r'ln \1', P(e))


def mono_txt(e):
    """monomial / quotient of monomials in a, b with integer exponents, written without negative indices if asked"""
    return P(e)


R.facts('ch02-st1', F(
    terms=[('logarithm', 'the power x to which a must be raised to give b, written logₐb = x and meaning aˣ = b (a > 0, a ≠ 1, b > 0)'),
           ('natural logarithm', 'the logarithm to base e, written ln x = logₑx'),
           ('common logarithm', 'the logarithm to base 10, written log x = log₁₀x'),
           ('negative exponent', 'the rule a⁻ⁿ = 1/aⁿ for a ≠ 0')],
    facts=[('log₂ 32 =', '5', ['16', '6', '1/5'], '2⁵ = 32.'),
           ('log₁₀ 0.001 =', '−3', ['3', '−2', '1/3'], '10⁻³ = 0.001.'),
           ('2⁻³ =', '1/8', ['−8', '−6', '8'], 'a⁻ⁿ = 1/aⁿ.'),
           ('If log₃ x = 4, then x =', '81', ['12', '64', '4/3'], '3⁴ = 81.'),
           ('(x³)⁴ =', 'x¹²', ['x⁷', 'x⁸¹', '4x³'], 'Multiply the indices.')],
    why=[('Explain why log₂(−8) is undefined for real numbers.', '2ˣ > 0 for every real x, so no real power of 2 equals −8.'),
         ('Explain why a⁰ = 1 for any a ≠ 0.', 'aⁿ ÷ aⁿ = aⁿ⁻ⁿ = a⁰ by the index law, and aⁿ ÷ aⁿ = 1, so a⁰ = 1.'),
         ('Explain the connection between the graphs of y = 10ˣ and y = log x.', 'They are inverse functions, so each graph is the reflection of the other in the line y = x.')],
    misc=[('3² × 3⁴ = 9⁶.', 'The base stays the same: 3² × 3⁴ = 3⁶ = 729.'),
          ('log 100 = 10².', 'log 100 = 2 because 10² = 100.'),
          ('(2x)³ = 2x³.', 'Every factor is cubed: (2x)³ = 8x³.')],
))


@R.add('ch02-st1', 'C3', (1, 4), 'short', style='p1')
def index_simplify(rng, slot):
    c1, c2 = rng.choice([2, 3, 4, 5, 6]), rng.choice([1, 2, 3, 4])
    m1, m2, n1, n2 = rng.randint(-3, 5), rng.randint(-3, 4), rng.randint(-3, 5), rng.randint(-3, 4)
    p = rng.choice([2, 3]) if slot.d >= 2 else 1
    e = (c1 * A_ ** m1 * B_ ** n1) ** p / (c2 * A_ ** m2 * B_ ** n2)
    e = sp.simplify(e)
    if e.is_number:
        return None
    num, den = sp.fraction(sp.together(e))
    txt = P(num) if den == 1 else f'{P(num)}/{P(den)}' if not isinstance(den, sp.Mul) else f'{P(num)}/({P(den)})'
    stem_e = f'({c1}{"a" + sup(m1) if m1 not in (0, 1) else "a" if m1 == 1 else ""}{"b" + sup(n1) if n1 not in (0, 1) else "b" if n1 == 1 else ""}){sup(p) if p > 1 else ""} ÷ ({c2 if c2 > 1 else ""}{"a" + sup(m2) if m2 not in (0, 1) else "a" if m2 == 1 else ""}{"b" + sup(n2) if n2 not in (0, 1) else "b" if n2 == 1 else ""})'
    if '()' in stem_e:
        return None
    return mk(f'Simplify {stem_e}, giving your answer with positive indices only.', txt,
              f'Power of a product: each factor raised to the power {p} (M1); subtract indices when dividing (M1); {txt} (A1 A1).', 4)


@R.add('ch02-st1', 'C3', (1, 4), 'short', style='p1')
def log_eval(rng, slot):
    b = rng.choice([2, 3, 4, 5, 10, 8, 9])
    k = rng.choice([-3, -2, -1, 2, 3, 4, sp.Rational(1, 2), sp.Rational(3, 2)])
    val = sp.Integer(b) ** k
    if not val.is_rational:
        return None
    kind = rng.choice(['eval', 'solve', 'convert'])
    if kind == 'eval':
        return mk(f'Find the exact value of log{sub(b)} {R_(val)}.', R_(k), f'Write {R_(val)} as {b}^({R_(k)}) (M1); log{sub(b)} {R_(val)} = {R_(k)} (A1).', 2)
    if kind == 'solve':
        return mk(f'Solve log{sub(b)} x = {R_(k)}.', f'x = {R_(val)}', f'x = {b}^({R_(k)}) (M1); {R_(val)} (A1).', 2)
    return mk(f'Write {b}^({R_(k)}) = {R_(val)} in logarithmic form, and write log{sub(b)} {R_(val)} = {R_(k)} back in exponential form.'.replace('^(', '^(') if False else
              f'Write the equation {b}^({R_(k)}) = {R_(val)} in logarithmic form.', f'log{sub(b)} {R_(val)} = {R_(k)}', 'aˣ = b ⇔ logₐb = x (A1 A1).', 2)


@R.add('ch02-st1', 'C1', (1, 3), 'mcq')
def log_mcq(rng, slot):
    b = rng.choice([2, 3, 5, 10, 4])
    k = rng.choice([-2, -1, 2, 3, 4, 5])
    val = sp.Integer(b) ** k
    right = str(k).replace('-', '−')
    wr = [R_(val / b), R_(-k), R_(sp.Rational(1, k))]
    wr = [w for w in dict.fromkeys(wr) if w != right]
    if len(wr) < 3:
        wr.append(str(k + 1))
    return mcq(rng, f'log{sub(b)} {R_(val)} ='.replace(f' {R_(val)} =', f'({R_(val)}) =') if '/' in R_(val) else f'log{sub(b)} {R_(val)} =', right, wr[:3], f'{b}^{k} = {R_(val)}.')


@R.add('ch02-st1', 'C2', (2, 4), 'explain')
def index_error_explain(rng, slot):
    a, m, n = rng.randint(2, 5), rng.randint(2, 6), rng.randint(2, 5)
    kind = rng.choice(['mult', 'neg', 'pow'])
    if kind == 'mult':
        return mk(f'{who(rng)} writes {a}{sup(m)} × {a}{sup(n)} = {a * a}{sup(m * n)}. Explain the two errors and give the correct value as a power of {a}.', f'{a}{sup(m + n)}',
                  f'The base is not multiplied (R1); indices are added, not multiplied (R1); {a}{sup(m)} × {a}{sup(n)} = {a}{sup(m + n)} (A1).', 3, 'explain')
    if kind == 'neg':
        return mk(f'{who(rng)} claims that {a}⁻{sup(n)} is a negative number. Explain why this is incorrect and find its exact value.', R_(sp.Rational(1, a ** n)),
                  f'A negative index means a reciprocal, not a negative value (R1); {a}⁻{sup(n)} = 1/{a}{sup(n)} (M1) = {R_(sp.Rational(1, a ** n))} (A1).', 3, 'explain')
    return mk(f'{who(rng)} writes ({a}x{sup(m)}){sup(n)} = {a}x{sup(m + n)}. Explain the errors and simplify correctly.', f'{a ** n}x{sup(m * n)}',
              f'The coefficient {a} must also be raised to the power {n} (R1); indices multiply for a power of a power (R1); {a ** n}x{sup(m * n)} (A1).', 3, 'explain')


@R.add('ch02-st1', 'C4', (3, 5), 'multi_step', style='ext')
def exp_log_parts(rng, slot):
    b = rng.choice([2, 3, 5])
    k = rng.randint(2, 4)
    m = rng.randint(1, 3)
    parts = [(f'Write {b ** k} as a power of {b}.', f'{b}{sup(k)}', 'A1', 1, True),
             (f'Hence solve {b}^(x + {m}) = {b ** k}.', f'x = {k - m}', 'equate indices (M1) A1', 2, True),
             (f'Solve {b ** 2}ˣ = {b}^(x + {k}).', f'x = {k}', f'{b}^(2x) = {b}^(x + {k}) (M1); 2x = x + {k} (A1)', 2, True),
             (f'Find the exact value of log{sub(b)} ({b ** k} × {b}^{m}).', str(k + m), 'M1 A1', 2, True),
             (f'Sketch, on the same axes, y = {b}ˣ and y = log{sub(b)} x, stating their intercepts and asymptotes.', f'y = {b}ˣ: (0, 1), asymptote y = 0; y = log{sub(b)} x: (1, 0), asymptote x = 0', 'A1 A1 A1', 3, False)]
    return build_parts(rng, ['This question uses the laws of exponents and the definition of a logarithm.', f'In this question, all answers are exact. Let b = {b}.'], parts, 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch02-st2', F(
    terms=[('rational exponent', 'a power with a fractional index: a^(m/n) = (ⁿ√a)ᵐ = ⁿ√(aᵐ) for a > 0'),
           ('product law of logarithms', 'the law logₐ(xy) = logₐx + logₐy'),
           ('power law of logarithms', 'the law logₐ(xᵐ) = m logₐx'),
           ('change of base formula', 'the rule logₐx = log_b x / log_b a, e.g. logₐx = ln x / ln a')],
    facts=[('8^(2/3) =', '4', ['16/3', '2', '64/3'], '(∛8)² = 2² = 4.'),
           ('log 5 + log 20 =', '2', ['log 25', '100', '1'], 'log 100 = 2.'),
           ('log₄ 8 =', '3/2', ['2', '1/2', '2/3'], '4^(3/2) = 8.'),
           ('ln e⁵ =', '5', ['e⁵', '5e', '1/5'], 'ln and eˣ are inverses.'),
           ('2 log₃ 6 − log₃ 4 =', '2', ['log₃ 8', '3', 'log₃ 32'], 'log₃(36/4) = log₃ 9.')],
    why=[('Explain why log(x + y) is not equal to log x + log y in general.', 'The product law gives log x + log y = log(xy); a sum inside a logarithm has no simple expansion, e.g. log(1 + 1) ≠ log 1 + log 1 = 0.'),
         ('Explain how the change of base formula follows from the definition of a logarithm.', 'If y = logₐx then aʸ = x; taking log_b of both sides gives y log_b a = log_b x, so y = log_b x / log_b a.'),
         ('Explain why (−8)^(1/3) is defined but (−8)^(1/2) is not a real number.', 'A cube root of a negative number is real (−2), but no real number squared gives −8.')],
    misc=[('log 8 / log 2 = log 4.', 'log 8 / log 2 = log₂ 8 = 3; dividing logs is not the same as the log of a quotient.'),
          ('16^(−1/2) = −4.', 'A negative index gives the reciprocal: 16^(−1/2) = 1/√16 = 1/4.'),
          ('(log x)² = 2 log x.', 'The power law applies to log(x²) = 2 log x, not to (log x)².')],
))


@R.add('ch02-st2', 'C3', (1, 4), 'short', style='p1')
def rational_exp(rng, slot):
    base, root = rng.choice([(8, 3), (27, 3), (16, 4), (32, 5), (64, 3), (64, 2), (81, 4), (125, 3), (25, 2), (49, 2), (Fr(27, 8), 3), (Fr(16, 81), 4), (Fr(4, 9), 2)])
    m = rng.choice([1, 2, 3, -1, -2, -3]) if slot.d >= 2 else rng.choice([1, 2])
    if m % root == 0:
        return None
    v = sp.nsimplify(base) ** sp.Rational(m, root)
    return mk(f'Without a calculator, find the exact value of ({R_(base)})^({R_(sp.Rational(m, root))}).'.replace('(8)', '8').replace('(27)', '27'), R_(v),
              f'{root}th root of {R_(base)} = {R_(sp.nsimplify(base) ** sp.Rational(1, root))} (M1); raise to the power {abs(m)}' + (', reciprocal for the negative index' if m < 0 else '') + f' (M1); {R_(v)} (A1).', 3)


@R.add('ch02-st2', 'C3', (2, 5), 'short', style='p1')
def log_laws(rng, slot):
    kind = rng.choice(['express', 'combine', 'evaluate', 'single'])
    b = rng.choice([2, 3, 5, 10])
    if kind == 'express':
        p, q, r = rng.randint(1, 4), rng.randint(1, 3), rng.choice([2, 3])
        return mk(f'Given that p = log{sub(b)} x and q = log{sub(b)} y, express log{sub(b)}(x{sup(p) if p > 1 else ""}/{"" if r == 1 else ("√" if r == 2 else "∛")}y{sup(q) if q > 1 else ""}) in terms of p and q.',
                  f'{p if p > 1 else ""}p − {P(sp.Rational(q, r) * sp.Symbol("q"))}', f'quotient law (M1); power law for each term (M1); {p if p > 1 else ""}p − {P(sp.Rational(q, r) * sp.Symbol("q"))} (A1 A1).', 4)
    if kind == 'evaluate':
        k = rng.randint(2, 4)
        m = rng.choice([2, 3, 4, 6])
        A = b ** k * m
        return mk(f'Without a calculator, find the value of log{sub(b)} {A} − log{sub(b)} {m}.', str(k), f'log{sub(b)}({A}/{m}) (M1) = log{sub(b)} {b ** k} (A1) = {k} (A1).', 3)
    if kind == 'combine':
        m, n = rng.randint(2, 3), rng.randint(2, 9)
        c = rng.randint(2, 7)
        val = sp.Rational(n ** m, c)
        return mk(f'Write {m} log{sub(b)} {n} − log{sub(b)} {c} as a single logarithm.', f'log{sub(b)}({R_(val)})', f'power law: log{sub(b)} {n ** m} (M1); quotient law (M1); log{sub(b)}({R_(val)}) (A1).', 3)
    k = rng.randint(1, 3)
    return mk(f'Write {k} + log{sub(b)} x as a single logarithm.', f'log{sub(b)}({b ** k}x)', f'{k} = log{sub(b)} {b ** k} (M1); log{sub(b)}({b ** k}x) (A1).', 2)


@R.add('ch02-st2', 'C3', (2, 4), 'short', style='p2')
def change_base(rng, slot):
    b = rng.choice([3, 5, 6, 7, 12, 4])
    xv = rng.choice([17, 40, 250, 0.4, 1000, 9, 3.6])
    v = math.log(xv) / math.log(b)
    exact = rng.random() < 0.4
    if exact:
        a, k1, k2 = rng.choice([(2, 2, 3), (2, 3, 2), (3, 2, 3), (2, 3, 4), (5, 2, 3), (2, 4, 3)])
        val = sp.Rational(k2, k1)
        return mk(f'Use the change of base formula to find the exact value of log{sub(a ** k1)} {a ** k2}.', R_(val),
                  f'log{sub(a ** k1)} {a ** k2} = log{sub(a)} {a ** k2} / log{sub(a)} {a ** k1} (M1) = {k2}/{k1} (A1).', 2)
    return mk(f'Use the change of base formula to evaluate log{sub(b)} {xv:g} to 3 significant figures.', s3(v), f'ln {xv:g} / ln {b:g} (M1); {s3(v)} (A1).', 2)


@R.add('ch02-st2', 'C1', (1, 3), 'mcq')
def logs_law_mcq(rng, slot):
    b = rng.choice([2, 3, 5, 10])
    m, n = rng.randint(2, 6), rng.randint(2, 6)
    if m == n:
        return None
    return mcq(rng, f'log{sub(b)} {m} + log{sub(b)} {n} =', f'log{sub(b)} {m * n}', [f'log{sub(b)} {m + n}', f'log{sub(b)} {m} × log{sub(b)} {n}', f'log{sub(b * 2)} {m * n}'], 'Product law.')


@R.add('ch02-st2', 'C2', (2, 4), 'explain')
def logs_error_explain(rng, slot):
    m, n = rng.randint(2, 9), rng.randint(2, 9)
    b = rng.choice([2, 3, 10])
    kind = rng.choice(['sum', 'quot'])
    if kind == 'sum':
        return mk(f'{who(rng)} writes log{sub(b)}({m} + {n}) = log{sub(b)} {m} + log{sub(b)} {n}. Explain why this is wrong and state what log{sub(b)} {m} + log{sub(b)} {n} does equal.', f'log{sub(b)} {m * n}',
                  f'The product law applies to products, not sums (R1); log{sub(b)} {m} + log{sub(b)} {n} = log{sub(b)}({m} × {n}) (M1) = log{sub(b)} {m * n} (A1).', 3, 'explain')
    return mk(f'{who(rng)} writes log{sub(b)} {m * n} / log{sub(b)} {m} = log{sub(b)} {n}. Explain why this is wrong and simplify the quotient correctly.', f'log{sub(m)} {m * n}',
              f'A quotient of logarithms is not the logarithm of a quotient (R1); by change of base it equals log{sub(m)} {m * n} (M1 A1).', 3, 'explain')


@R.add('ch02-st2', 'C4', (3, 5), 'multi_step', style='ext')
def logs_parts(rng, slot):
    b = rng.choice([2, 3, 5])
    p_, q_ = rng.randint(2, 4), rng.randint(2, 3)
    parts = [(f'Given that log{sub(b)} x = p and log{sub(b)} y = q, express log{sub(b)}(x{sup(p_)}y) in terms of p and q.', f'{p_}p + q', 'M1 A1', 2, True),
             (f'Express log{sub(b)}({b}x/y{sup(q_)}) in terms of p and q.', f'1 + p − {q_}q', 'M1 A1', 2, True),
             (f'Express log{sub(b * b)} x in terms of p.', 'p/2', 'change of base (M1) A1', 2, True),
             (f'Given further that x = {b}y and p + q = {2 * q_ + 1}, find the exact values of p and q.', f'p = {q_ + 1}, q = {q_}', 'p = 1 + q (A1); solve (M1) A1', 3, True),
             ('Hence find x and y.', f'x = {b ** (q_ + 1)}, y = {b ** q_}', 'A1 A1', 2, False)]
    return build_parts(rng, ['This question uses the laws of logarithms.', f'Let x and y be positive real numbers, and let p = log{sub(b)} x, q = log{sub(b)} y.'], parts, 4)


@R.add('ch02-st2', 'C4', (4, 5), 'multi_step', style='p3')
def logs_chain_parts(rng, slot):
    a, b_, c = rng.choice([(2, 3, 5), (3, 5, 7), (2, 5, 9), (4, 7, 3), (5, 6, 11)])
    N = rng.randint(4, 9)
    prod = math.log(N + 1) / math.log(2)
    parts = [('Prove that logₐb × log_b c = logₐc for positive a, b, c (a, b ≠ 1).', 'proof', 'change of base to a common base (M1); cancel (A1) AG', 2, True),
             (f'Hence find the exact value of log{sub(a)} {b_} × log{sub(b_)} {c} × log{sub(c)} {a ** 3}.', '3', 'chain the result (M1) A1', 2, True),
             (f'Find the exact value of log₂ 3 × log₃ 4 × log₄ 5 × … × log{sub(N)} {N + 1}.', f'log₂ {N + 1}', 'telescoping product (M1) A1', 2, True),
             ('Prove that logₐb = 1 / log_b a.', 'proof', 'take c = a (M1) A1', 2, True),
             (f'Find the smallest integer n for which log₂ 3 × log₃ 4 × … × logₙ (n + 1) > 10.', '1024', 'log₂(n + 1) > 10 (M1); n + 1 > 1024 (A1); n = 1024 (A1)', 3, False)]
    return build_parts(rng, ['This question investigates products of logarithms.', 'In this question you will generalise a result about logarithms to different bases.'], parts, 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch02-st3', F(
    terms=[('exponential equation', 'an equation in which the unknown appears in an exponent, e.g. 3ˣ = 20'),
           ('equation of quadratic type', 'an equation such as e²ˣ − 5eˣ + 6 = 0 that becomes a quadratic with a substitution such as u = eˣ'),
           ('extraneous solution', 'a value obtained in solving that does not satisfy the original equation, e.g. one that makes the argument of a logarithm negative')],
    facts=[('The solution of 2ˣ = 10 is', 'x = log 10 / log 2', ['x = 5', 'x = log 5', 'x = 10/2'], 'Take logarithms.'),
           ('To solve 9ˣ − 4(3ˣ) + 3 = 0, substitute', 'u = 3ˣ', ['u = 9ˣ', 'u = x²', 'u = log x'], '9ˣ = (3ˣ)².'),
           ('The solution of eˣ = 7 is', 'x = ln 7', ['x = 7/e', 'x = e⁷', 'x = log 7'], 'Natural logarithm.')],
    why=[('Explain why solutions of logarithmic equations must be checked in the original equation.', 'Combining logarithms (e.g. log a + log b = log ab) can introduce values for which a or b is negative or zero; such values make the original logarithms undefined and must be rejected.'),
         ('Explain why the equation 2ˣ = −4 has no real solution.', '2ˣ is positive for every real x, so it can never equal a negative number.'),
         ('Explain why the substitution u = eˣ in e²ˣ − 3eˣ − 4 = 0 leads to one solution only.', 'u² − 3u − 4 = 0 gives u = 4 or u = −1; eˣ = −1 is impossible because eˣ > 0, so only x = ln 4.')],
    misc=[('From 3ˣ = 12 we get x = 12/3 = 4.', 'Taking logs: x = ln 12 / ln 3 ≈ 2.26.'),
          ('log(x − 1) + log(x + 2) = log 10 gives x − 1 + x + 2 = 10.', 'Use the product law: (x − 1)(x + 2) = 10.')],
))


@R.add('ch02-st3', 'C3', (2, 5), 'short', style='p1')
def exp_eq_exact(rng, slot):
    kind = rng.choice(['samebase', 'quad_e', 'quad_b', 'ln'])
    if kind == 'samebase':
        b = rng.choice([2, 3, 5])
        p, q = rng.choice([(2, 3), (3, 2), (2, 1), (3, 4), (4, 3)])
        m, n = rng.randint(-3, 4), rng.randint(-3, 4)
        sol = sp.solve(sp.Eq(p * (x + m), q * (x + n)), x)
        if not sol:
            return None
        return mk(f'Solve {b ** p}^(x {"+" if m >= 0 else "−"} {abs(m)}) = {b ** q}^(x {"+" if n >= 0 else "−"} {abs(n)}).'.replace(' + 0)', ')'), f'x = {R_(sol[0])}',
                  f'Write both sides as powers of {b} (M1); {p}(x {"+" if m >= 0 else "−"} {abs(m)}) = {q}(x {"+" if n >= 0 else "−"} {abs(n)}) (A1); x = {R_(sol[0])} (A1).', 3)
    if kind == 'quad_e':
        r1, r2_ = rng.sample([1, 2, 3, 4, 5, 6], 2)
        if rng.random() < 0.4:
            r2_ = -r2_
        coeffs = sp.expand((y - r1) * (y - r2_))
        sols = [sp.log(r) for r in (r1, r2_) if r > 0]
        return mk(f'Solve e^(2x) {poly_txt(coeffs - y ** 2, y).replace("y", "eˣ") if False else ""}'.strip() + '', '', '') if False else \
            mk(f'Solve e^(2x) − {r1 + r2_}eˣ + {r1 * r2_} = 0.'.replace('− −', '+ ').replace('+ −', '− ').replace(' 1eˣ', ' eˣ').replace('− 0eˣ ', ''), 'x = ' + ' or x = '.join(Pl(s_) for s_ in sols),
               f'Let u = eˣ: u² − {r1 + r2_}u + {r1 * r2_} = 0 (M1); u = {r1} or u = {r2_} (A1){"; eˣ = " + str(min(r1, r2_)) + " rejected since eˣ > 0 (R1)" if min(r1, r2_) < 0 else ""}; {", ".join(Pl(s_) for s_ in sols)} (A1).'.replace('− −', '+ ').replace('+ −', '− '), 4)
    if kind == 'quad_b':
        b = rng.choice([2, 3])
        k1, k2 = rng.sample([0, 1, 2, 3], 2)
        s1, s2 = b ** k1, b ** k2
        return mk(f'Solve {b * b}ˣ − {s1 + s2}({b}ˣ) + {s1 * s2} = 0.', f'x = {min(k1, k2)} or x = {max(k1, k2)}',
                  f'u = {b}ˣ, {b * b}ˣ = u² (M1); u² − {s1 + s2}u + {s1 * s2} = 0 (A1); u = {s1}, {s2} (A1); x = {k1}, {k2} (A1).', 4)
    a, c = rng.randint(2, 5), rng.randint(2, 9)
    k = rng.randint(1, 4)
    return mk(f'Solve {a}e^({k}x) = {a * c}, giving your answer in the form x = (ln p)/q.'.replace('e^(1x)', 'eˣ'), f'x = (ln {c})/{k}' if k > 1 else f'x = ln {c}',
              f'e^({k}x) = {c} (A1); {k}x = ln {c} (M1); x = ln({c})/{k} (A1).', 3)


@R.add('ch02-st3', 'C3', (2, 5), 'short', style='p2')
def exp_eq_gdc(rng, slot):
    kind = rng.choice(['one', 'two', 'model'])
    if kind == 'one':
        a, b, c = rng.randint(2, 9), rng.choice([1.05, 1.2, 1.5, 2.5, 0.8, 3]), rng.randint(20, 300)
        v = math.log(c / a) / math.log(b)
        return mk(f'Solve {a}({b:g})ˣ = {c}, giving your answer to 3 significant figures.', f'x = {s3(v)}', f'({b:g})ˣ = {c}/{a} (M1); x = ln({c}/{a})/ln {b:g} (M1); {s3(v)} (A1).', 3)
    if kind == 'two':
        a, b = rng.choice([2, 3, 5, 7]), rng.choice([2, 3, 4, 6])
        if a == b:
            return None
        k = rng.randint(1, 3)
        v = k * math.log(b) / (math.log(a) - math.log(b))
        return mk(f'Solve {a}ˣ = {b}^(x + {k}), giving your answer to 3 significant figures.', f'x = {s3(v)}',
                  f'x ln {a} = (x + {k}) ln {b} (M1); x(ln {a} − ln {b}) = {k} ln {b} (A1); x = {s3(v)} (A1).', 3)
    N0, k = rng.choice([500, 1200, 80, 3000]), rng.choice([0.04, 0.12, 0.25, 0.3])
    T = N0 * rng.choice([2, 5, 10])
    v = math.log(T / N0) / k
    return mk(f'The number of bacteria in a culture is N = {N0}e^({k}t), where t is in hours. Find the time when N = {T}.', f't = {s3(v)} hours',
              f'e^({k}t) = {T}/{N0} (M1); t = ln({T // N0})/{k} (M1); {s3(v)} hours (A1).', 3)


@R.add('ch02-st3', 'C3', (3, 5), 'short', style='p1')
def log_eq(rng, slot):
    b = rng.choice([2, 3, 5, 10])
    k = rng.randint(1, 3) if b > 3 else rng.randint(2, 4)
    N = b ** k
    pairs = [(u, N // u) for u in range(1, N + 1) if N % u == 0 and u < N // u]
    if not pairs:
        return None
    u, v = rng.choice(pairs)
    x0 = rng.randint(-3, 6)
    r_, s_ = u - x0, v - x0
    if r_ == s_ or abs(r_) > 30 or abs(s_) > 30:
        return None
    sols = sp.solve(sp.Eq((x + r_) * (x + s_), b ** k), x)
    good = [v for v in sols if v.is_real and v + r_ > 0 and v + s_ > 0]
    bad = [v for v in sols if v.is_real and v not in good]
    if not good or not all(v.is_rational for v in sols):
        return None
    return mk(f'Solve log{sub(b)}({poly_txt(x + r_)}) + log{sub(b)}({poly_txt(x + s_)}) = {k}.', 'x = ' + ', '.join(R_(v) for v in good),
              f'product law: log{sub(b)}(({poly_txt(x + r_)})({poly_txt(x + s_)})) = {k} (M1); ({poly_txt(x + r_)})({poly_txt(x + s_)}) = {b ** k} (A1); solve the quadratic (M1); '
              + (f'reject x = {", ".join(R_(v) for v in bad)} since the logarithms would be undefined (R1); ' if bad else '') + f'x = {", ".join(R_(v) for v in good)} (A1).', 5)


@R.add('ch02-st3', 'C1', (1, 3), 'mcq')
def exp_eq_mcq(rng, slot):
    b, c = rng.choice([2, 3, 5, 7]), rng.choice([10, 20, 50, 30, 12])
    return mcq(rng, f'The exact solution of {b}ˣ = {c} is', f'x = ln {c} / ln {b}', [f'x = {c}/{b}', f'x = ln({c}/{b})', f'x = ln {c} − ln {b}'], 'Take natural logarithms of both sides.')


@R.add('ch02-st3', 'C2', (2, 4), 'explain')
def exp_eq_explain(rng, slot):
    r1, r2_ = rng.randint(2, 7), rng.randint(1, 6)
    return mk(f'{who(rng)} solves e^(2x) − {r1 - r2_}eˣ − {r1 * r2_} = 0 and states the solutions x = ln {r1} and x = ln(−{r2_}). Explain the error and give the correct solution.'.replace('− 0eˣ', '').replace('− 1eˣ', '− eˣ').replace('− -', '+ '),
              f'x = ln {r1}', f'With u = eˣ, u = {r1} or u = −{r2_} (M1); eˣ > 0 so eˣ = −{r2_} has no solution and ln of a negative number is undefined (R1); only x = ln {r1} (A1).', 3, 'explain')


@R.add('ch02-st3', 'C4', (3, 5), 'multi_step', style='ext')
def exp_model_parts(rng, slot):
    sub_ = rng.choice(['caffeine', 'a medicine', 'iodine-131', 'carbon-11'])
    A0 = rng.choice([100, 200, 80, 400])
    h = rng.choice([5, 6, 8, 20.4]) if sub_ != 'iodine-131' else 8.02
    k = math.log(2) / h
    t1 = rng.choice([3, 10, 12, 24])
    A1 = A0 * math.exp(-k * t1)
    T = A0 * rng.choice([0.1, 0.05, 0.2])
    tT = math.log(A0 / T) / k
    parts = [(f'Show that k = ln 2 / {h:g}.', 'shown', f'½A₀ = A₀e^(−{h:g}k) (M1); take ln (A1) AG', 2, True),
             (f'Find the amount remaining after {t1} hours.', f'{s3(A1)} mg', 'M1 A1', 2, True),
             (f'Find the time taken for the amount to fall to {T:g} mg.', f'{s3(tT)} hours', 'ln (M1) A1', 2, True),
             ('Find the percentage of the substance that remains after each hour.', f'{s3(100 * math.exp(-k))}%', 'e^(−k) (M1) A1', 2, False),
             ('Explain why the amount never reaches zero according to this model.', 'e^(−kt) > 0 for all t', 'R1', 1, False)]
    return build_parts(rng, [f'The amount A mg of {sub_} in a sample is modelled by A = {A0}e^(−kt), where t is in hours. The half-life is {h:g} hours.',
                             f'The decay of {sub_} follows A(t) = {A0}e^(−kt) (t in hours), with half-life {h:g} hours.'], parts, 4)


# =============================================================================================
# ch03 Proof and the binomial theorem (SL 1.6, 1.9; AHL 1.10, 1.15)
# =============================================================================================
n_ = sp.Symbol('n', integer=True)

R.facts('ch03-st1', F(
    terms=[('identity', 'a statement that is true for all values of the variable, written with ≡, e.g. (x + 1)² ≡ x² + 2x + 1'),
           ('implication', 'the statement p ⇒ q, meaning that whenever p is true, q is true'),
           ('deductive proof', 'a chain of logical steps from known facts or definitions to the required result, e.g. working from the left-hand side to the right-hand side'),
           ('conjecture', 'a statement believed to be true but not yet proved')],
    facts=[('The symbol ≡ means', 'is identically equal to (true for all values)', ['is approximately equal to', 'implies', 'is defined as a function of'], 'Used for identities.'),
           ('"x = 2 ⇒ x² = 4" is', 'true, but the converse is false', ['false', 'true in both directions', 'meaningless'], 'x² = 4 also when x = −2.'),
           ('An even number can be written as', '2n, n ∈ ℤ', ['n + 2', '2n + 1, n ∈ ℤ', 'n²'], 'Definition of even.'),
           ('To prove an identity LHS ≡ RHS you should', 'start with one side and transform it into the other', ['substitute a few values', 'assume it is true and simplify both sides to 0 = 0', 'draw a graph'], 'Deductive proof.')],
    why=[('Explain why checking that an identity holds for several values of x does not prove it.', 'An identity must hold for every value of x; finitely many checks cannot rule out a value for which it fails.'),
         ('Explain why the statement "x² = 9 ⇒ x = 3" is false.', 'x = −3 also satisfies x² = 9, so x² = 9 does not force x = 3; the correct statement is x² = 9 ⇒ x = ±3.'),
         ('Explain the difference between "=" in x + 2 = 5 and "≡" in 2(x + 1) ≡ 2x + 2.', 'x + 2 = 5 is an equation true only for x = 3; the identity is true for every x.')],
    misc=[('The sum of two odd numbers is odd.', '(2m + 1) + (2n + 1) = 2(m + n + 1), which is even.'),
          ('To prove an identity, I square both sides and show they are equal.', 'Squaring can create equality where there was none (e.g. −2 and 2); work from one side to the other instead.')],
))


@R.add('ch03-st1', 'C3', (2, 5), 'short', style='p1')
def identity_proof(rng, slot):
    a, b = rng.randint(1, 6), rng.randint(1, 6)
    kind = rng.choice(['diffsq', 'prod', 'cube', 'frac'])
    if kind == 'diffsq':
        L, Rt = (x + a) ** 2 - (x - a) ** 2, 4 * a * x
        Ltxt = f'(x + {a})² − (x − {a})²'
    elif kind == 'prod':
        L, Rt = (x + a) * (x + b) - x * (x + a + b), a * b
        Ltxt = f'(x + {a})(x + {b}) − x(x + {a + b})'
    elif kind == 'cube':
        L, Rt = (x + a) ** 3 - (x - a) ** 3, 6 * a * x ** 2 + 2 * a ** 3
        Ltxt = f'(x + {a})³ − (x − {a})³'
    else:
        L, Rt = sp.Rational(1, 1) / (x - a) - sp.Rational(1, 1) / (x + a), 2 * a / (x ** 2 - a ** 2)
        Ltxt = f'1/(x − {a}) − 1/(x + {a})'
    assert sp.simplify(L - Rt) == 0
    Rtxt = poly_txt(Rt) if kind != 'frac' else f'{2 * a}/(x² − {a * a})'
    return mk(f'Show that {Ltxt} ≡ {Rtxt}.', 'shown', f'Expand/combine the left-hand side (M1); {P(sp.expand(L)) if kind != "frac" else "common denominator (x − " + str(a) + ")(x + " + str(a) + ")"} (A1); = RHS (A1) AG.', 3)


NUM_PROOFS = [
    ('the sum of any {k} consecutive integers is divisible by {k}', lambda k: k % 2 == 1, 'n + (n + 1) + … + (n + {k1}) = {k}n + {T} = {k}(n + {h})', 'R1: {k}(n + {h}) is a multiple of {k}'),
    ('the product of two consecutive even numbers is divisible by 8', None, '2n(2n + 2) = 4n(n + 1)', 'R1: n(n + 1) is even, so 4n(n + 1) is a multiple of 8'),
    ('the square of any odd number is one more than a multiple of 8', None, '(2n + 1)² = 4n² + 4n + 1 = 4n(n + 1) + 1', 'R1: n(n + 1) is even'),
    ('the difference between the squares of two consecutive odd numbers is a multiple of 8', None, '(2n + 1)² − (2n − 1)² = 8n', 'R1: 8n is a multiple of 8'),
    ('the sum of the squares of two consecutive integers is odd', None, 'n² + (n + 1)² = 2n² + 2n + 1 = 2(n² + n) + 1', 'R1: 2(n² + n) is even'),
    ('n³ − n is divisible by 6 for every integer n', None, 'n³ − n = (n − 1)n(n + 1)', 'R1: a product of three consecutive integers contains a multiple of 2 and a multiple of 3'),
]


@R.add('ch03-st1', 'C3', (2, 5), 'short', style='p1')
def number_proof(rng, slot):
    i = rng.randrange(len(NUM_PROOFS))
    stmt, cond, work, reason = NUM_PROOFS[i]
    k = rng.choice([3, 5, 7, 9])
    T = k * (k - 1) // 2
    fill = dict(k=k, k1=k - 1, T=T, h=T // k)
    frame = rng.choice(['Prove that {s}.', 'Show that {s}, using algebra.', 'Give a deductive proof that {s}.'])
    return mk(frame.format(s=stmt.format(**fill)), 'proof', f'Algebraic representation (M1); {work.format(**fill)} (A1); {reason.format(**fill)}.', 3)


@R.add('ch03-st1', 'C1', (1, 3), 'mcq')
def implies_mcq(rng, slot):
    a = rng.randint(2, 9)
    pool = [(f'x = {a} ⇒ x² = {a * a}', 'true'), (f'x² = {a * a} ⇒ x = {a}', f'false (x = −{a})'), (f'x > {a} ⇒ x > {a - 1}', 'true'), (f'x > {a - 1} ⇒ x > {a}', f'false (e.g. x = {a - 1}.5)'),
            (f'x² < {a * a} ⇒ x < {a}', 'true'), (f'x < {a} ⇒ x² < {a * a}', f'false (e.g. x = −{a + 1})')]
    st_, ans = rng.choice(pool)
    wr = ['true', 'false (x = 0)', f'false (x = {a + 1})', 'true only for x > 0', f'false (x = −{a})', f'false (e.g. x = {a - 1}.5)', f'false (e.g. x = −{a + 1})']
    wr = [w for w in wr if w != ans]
    rng.shuffle(wr)
    return mcq(rng, f'Which describes the statement "{st_}" for real x?', ans, wr[:3], 'An implication is false if one counterexample exists.')


@R.add('ch03-st1', 'C2', (2, 4), 'explain')
def proof_flaw_explain(rng, slot):
    a = rng.randint(2, 7)
    kind = rng.choice(['examples', 'converse', 'divide'])
    if kind == 'examples':
        return mk(f'{who(rng)} claims to prove that (x + {a})² ≡ x² + {2 * a}x + {a * a} by checking x = 0, 1 and 2. Explain why this is not a proof and give a valid proof.', 'expand the left side for general x',
                  'Checking values cannot show the result for all x (R1); expand (x + {a})(x + {a}) = x² + {2a}x + {a2} (M1 A1).'.format(a=a, **{'2a': 2 * a, 'a2': a * a}), 3, 'explain')
    if kind == 'converse':
        return mk(f'Explain why "n is a multiple of {2 * a} ⇒ n is a multiple of {a}" is true but its converse is false.', f'converse fails, e.g. n = {a}',
                  f'n = {2 * a}k = {a}(2k), a multiple of {a} (R1); converse: n = {a} is a multiple of {a} but not of {2 * a} (R1 A1).', 3, 'explain')
    return mk(f'A student "proves" that {a} = {a + 1} by writing x = 0, so {a}x = {a + 1}x, then dividing both sides by x. Explain the flaw.', 'division by zero',
              'x = 0, so dividing by x is not allowed (R1); the step {a}x = {b}x ⇒ {a} = {b} is only valid for x ≠ 0 (R1 R1).'.format(a=a, b=a + 1), 3, 'explain')


@R.add('ch03-st1', 'C4', (3, 5), 'multi_step', style='ext')
def proof_parts(rng, slot):
    a = rng.randint(1, 5)
    parts = [(f'Show that (n + {a})² − n² ≡ {2 * a}n + {a * a}.', 'shown', 'expand (M1) A1 AG', 2, True),
             (f'Hence prove that the difference between the squares of two integers that differ by {a} is {"odd" if a % 2 else "a multiple of " + str(4 if a % 4 == 2 else 8 if a % 8 == 4 else 2 * a)} when n is an integer.'.replace('a multiple of 8', 'a multiple of 8'),
              'proof', 'parity / factor argument (R1 R1)', 2, a % 2 == 1),
             ('Prove that the sum of any three consecutive integers is divisible by 3.', 'n + (n + 1) + (n + 2) = 3(n + 1)', 'M1 A1 R1', 3, True),
             ('Prove that for all integers n, n² + n is even.', 'n(n + 1) is a product of consecutive integers, one of which is even', 'M1 R1', 2, True),
             (f'Show that the statement "n² + n + {a + 10} is prime for all positive integers n" is false.', f'n = {a + 10}: {(a + 10) ** 2 + 2 * (a + 10)} = {a + 10} × {a + 12}', 'counterexample (M1) A1', 2, False)]
    return build_parts(rng, ['This question is about algebraic proof.', 'In this question, n denotes an integer.'], parts, 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch03-st2', F(
    terms=[('binomial theorem', '(a + b)ⁿ = Σ from r = 0 to n of ⁿCᵣ aⁿ⁻ʳbʳ for positive integer n'),
           ('binomial coefficient', 'ⁿCᵣ = n!/(r!(n − r)!), the coefficient of aⁿ⁻ʳbʳ in (a + b)ⁿ'),
           ("Pascal's triangle", 'a triangular array in which each entry is the sum of the two entries above it; row n gives ⁿC₀, ⁿC₁, …, ⁿCₙ')],
    facts=[('⁶C₂ =', '15', ['12', '30', '36'], '6!/(2!4!).'),
           ('The number of terms in the expansion of (x + 2)⁹ is', '10', ['9', '11', '18'], 'n + 1 terms.'),
           ('The coefficient of x² in (1 + x)⁵ is', '10', ['5', '20', '25'], '⁵C₂.'),
           ('ⁿCᵣ is equal to', 'ⁿCₙ₋ᵣ', ['ⁿCᵣ₊₁', 'ⁿ⁻¹Cᵣ', 'n!/r!'], 'Symmetry of Pascal\'s triangle.')],
    why=[('Explain why the coefficients in (a + b)ⁿ are the numbers ⁿCᵣ.', 'Expanding the n brackets, each term aⁿ⁻ʳbʳ arises by choosing b from r of the n brackets; there are ⁿCᵣ ways to choose which brackets.'),
         ('Explain why the terms in the expansion of (2 − x)⁵ alternate in sign.', 'Each term contains (−x)ʳ, which is positive for even r and negative for odd r.'),
         ('Explain why the sum of the entries in row n of Pascal\'s triangle is 2ⁿ.', 'Setting a = b = 1 in the binomial theorem gives (1 + 1)ⁿ = Σ ⁿCᵣ.')],
    misc=[('(x + 3)² = x² + 9.', 'The cross term is missing: (x + 3)² = x² + 6x + 9.'),
          ('The coefficient of x³ in (2x + 1)⁵ is ⁵C₃ = 10.', 'The factor 2³ is missing: ⁵C₃ × 2³ = 80.')],
))


def binom_term(a, b, n, r):
    """coefficient of term with b^r in (a + b)^n where a, b sympy expressions"""
    return sp.binomial(n, r) * a ** (n - r) * b ** r


@R.add('ch03-st2', 'C3', (1, 4), 'short', style='p1')
def binom_expand(rng, slot):
    a, b = rng.choice([1, 2, 3]), nz(rng, -3, 3)
    n = rng.randint(3, 5) if slot.d <= 2 else rng.randint(5, 8)
    e = sp.expand((a + b * x) ** n)
    if slot.d <= 2:
        return mk(f'Use the binomial theorem to expand ({a} {"+" if b > 0 else "−"} {abs(b) if abs(b) > 1 else ""}x){sup(n)} fully.', poly_txt(e)[::-1][::-1] if False else ' + '.join([]) or _asc(e),
                  f'Correct binomial coefficients {", ".join(str(sp.binomial(n, r)) for r in range(n + 1))} (A1); powers of {a} and {b}x (M1); fully correct (A1 A1).', 4)
    k = 4
    return mk(f'Find the first {k} terms, in ascending powers of x, of the expansion of ({a} {"+" if b > 0 else "−"} {abs(b) if abs(b) > 1 else ""}x){sup(n)}.', _asc(e, 3),
              f'ⁿCᵣ{a}ⁿ⁻ʳ({b}x)ʳ for r = 0, …, 3 (M1); {_asc(e, 3)} (A1 A1 A1).', 4)


def _asc(e, upto=None):
    p_ = sp.Poly(sp.expand(e), x)
    terms = sorted(p_.terms(), key=lambda tc: tc[0][0])
    if upto is not None:
        terms = [tc for tc in terms if tc[0][0] <= upto]
    out = ''
    for (k,), c in terms:
        v = '' if k == 0 else ('x' if k == 1 else f'x{sup(k)}')
        mag_ = abs(c)
        tm = P(mag_ * x ** k)
        out = (('−' if c < 0 else '') + tm) if not out else out + (' − ' if c < 0 else ' + ') + tm
    return out


@R.add('ch03-st2', 'C3', (2, 5), 'short', style='p1')
def binom_coeff(rng, slot):
    kind = rng.choice(['coef', 'const', 'findk'])
    n = rng.randint(4, 9)
    if kind == 'coef':
        a, b = rng.choice([1, 2, 3]), nz(rng, -4, 4)
        r = rng.randint(2, min(4, n))
        c = sp.binomial(n, r) * a ** (n - r) * b ** r
        return mk(f'Find the coefficient of x{sup(r)} in the expansion of ({a if a > 1 else ""}{"" if a > 1 else ""}{a if False else ""}{a} + {b}x){sup(n)}.'.replace('+ −', '− ').replace(f'({a}{a}', f'({a}'), str(c),
                  f'term ⁿCᵣ: {n}C{r} ({a}){sup(n - r)}({b}x){sup(r)} (M1 A1); {c} (A1).', 3)
    if kind == 'const':
        p = rng.choice([1, 2])
        n = rng.choice([v for v in range(3, 13) if (v * p) % (p + 1) == 0] or [6])
        a, b = rng.choice([1, 2, 3]), rng.choice([1, 2, -1, -2, 3])
        # (a x^p + b/x)^n : x power p(n-r) - r = 0 -> r = pn/(p+1)
        r = p * n // (p + 1)
        c = sp.binomial(n, r) * a ** (n - r) * b ** r
        xt = 'x' if p == 1 else f'x{sup(p)}'
        return mk(f'Find the term independent of x in the expansion of ({a if a > 1 else ""}{xt} {"+" if b > 0 else "−"} {abs(b)}/x){sup(n)}.', str(c),
                  f'general term ⁿCᵣ({a}{xt})ⁿ⁻ʳ({b}/x)ʳ (M1); power of x: {p}({n} − r) − r = 0 ⇒ r = {r} (M1 A1); {c} (A1).', 4)
    k = sp.Symbol('k')
    kv = nz(rng, -4, 5)
    r = 2
    c = sp.binomial(n, r) * kv ** r
    return mk(f'The coefficient of x² in the expansion of (1 + kx){sup(n)} is {c}. Find the possible values of k.', f'k = ±{abs(kv)}',
              f'{n}C2 k² = {c} (M1 A1); k² = {kv * kv} (A1); k = ±{abs(kv)} (A1).', 4)


@R.add('ch03-st2', 'C1', (1, 3), 'mcq')
def ncr_mcq(rng, slot):
    n = rng.randint(5, 12)
    r = rng.randint(2, min(5, n - 1))
    right = sp.binomial(n, r)
    wr = list(dict.fromkeys([sp.factorial(n) / sp.factorial(n - r), n * r, sp.binomial(n, r - 1), sp.binomial(n - 1, r)]))
    wr = [str(w) for w in wr if w != right][:3]
    return mcq(rng, f'The value of {n}C{r} is', str(right), wr, f'{n}!/({r}!{n - r}!).')


@R.add('ch03-st2', 'C2', (2, 4), 'explain')
def binom_explain(rng, slot):
    a, n, r = rng.choice([2, 3, 5]), rng.randint(4, 8), rng.randint(2, 3)
    return mk(f'{who(rng)} says that the coefficient of x{sup(r)} in ({a}x + 1){sup(n)} is {n}C{r} = {sp.binomial(n, r)}. Explain the mistake and find the correct coefficient.', str(sp.binomial(n, r) * a ** r),
              f'The term is {n}C{r}({a}x){sup(r)}, so {a}{sup(r)} must be included (R1 M1); {sp.binomial(n, r) * a ** r} (A1).', 3, 'explain')


@R.add('ch03-st2', 'C4', (3, 5), 'multi_step', style='ext')
def binom_approx_parts(rng, slot):
    n = rng.randint(6, 10)
    h = rng.choice([sp.Rational(1, 100), sp.Rational(2, 100), sp.Rational(1, 50), sp.Rational(3, 100)])
    e = sp.expand((1 + x) ** n)
    approx = sum(sp.binomial(n, r) * h ** r for r in range(3))
    true = (1 + h) ** n
    parts = [(f'Find the first three terms in the expansion of (1 + x){sup(n)} in ascending powers of x.', _asc(e, 2), 'M1 A1', 2, True),
             (f'Use your answer to find an approximation for {float(1 + h):g}{sup(n)}.', f'{float(approx):g}', f'x = {float(h):g} (M1) A1', 2, True),
             ('Find the percentage error of this approximation.', f'{s3(abs(float(true - approx)) / float(true) * 100)}%', 'GDC value (M1) A1', 2, True),
             (f'Find the coefficient of x³ in (1 + x){sup(n)}(2 − x).', str(2 * sp.binomial(n, 3) - sp.binomial(n, 2)), 'two contributions (M1) A1', 2, True),
             ('Explain why the approximation is good for small x.', 'higher powers of a small x are very small', 'R1', 1, False)]
    return build_parts(rng, ['This question uses the binomial theorem to approximate powers.', f'Consider the expansion of (1 + x){sup(n)}.'], parts, 4)


@R.add('ch03-st2', 'C4', (4, 5), 'multi_step', style='p3')
def binom_sum_parts(rng, slot):
    n = rng.randint(5, 9)
    parts = [(f'Write down the value of Σ from r = 0 to {n} of {n}Cᵣ.', str(2 ** n), 'set x = 1 in (1 + x)ⁿ (M1) A1', 2, True),
             (f'Show that Σ from r = 0 to {n} of (−1)ʳ {n}Cᵣ = 0.', 'shown', 'set x = −1 (M1) AG', 1, True),
             (f'Hence find {n}C₀ + {n}C₂ + {n}C₄ + ….', str(2 ** (n - 1)), 'add the two results (M1) A1', 2, True),
             (f'Find Σ from r = 0 to {n} of 2ʳ {n}Cᵣ.', str(3 ** n), 'x = 2 (M1) A1', 2, True),
             ('Prove that ⁿCᵣ + ⁿCᵣ₊₁ = ⁿ⁺¹Cᵣ₊₁ for 0 ≤ r < n.', 'proof', 'common denominator of factorials (M1 A1); simplify (A1)', 3, False)]
    return build_parts(rng, ['This question investigates sums of binomial coefficients.', 'In this question, results about ⁿCᵣ are found from the binomial theorem.'], parts, 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch03-st3', F(
    terms=[('permutation', 'an arrangement of objects in which order matters; ⁿPᵣ = n!/(n − r)!'),
           ('combination', 'a selection of objects in which order does not matter; ⁿCᵣ = n!/(r!(n − r)!)'),
           ('factorial', 'the product n! = n × (n − 1) × … × 2 × 1, with 0! = 1'),
           ('product principle', 'if one task can be done in m ways and a second in n ways, both can be done in m × n ways')],
    facts=[('The number of ways to arrange 5 different books in a row is', '120', ['25', '60', '5'], '5!.'),
           ('The number of ways to choose 3 people from 7 is', '35', ['210', '21', '343'], '⁷C₃.'),
           ('The number of arrangements of the letters of BOOK is', '12', ['24', '6', '4'], '4!/2!.'),
           ('0! =', '1', ['0', 'undefined', '−1'], 'By definition.')],
    why=[('Explain why the number of arrangements of n objects of which k are identical is n!/k!.', 'The k identical objects can be permuted among themselves in k! ways without producing a new arrangement, so each distinct arrangement is counted k! times in n!.'),
         ('Explain the difference between choosing a committee of 3 from 10 people and electing a president, secretary and treasurer from 10 people.', 'A committee is a combination (order irrelevant): ¹⁰C₃ = 120; officers are a permutation (roles distinguish order): ¹⁰P₃ = 720.'),
         ('Explain the method of treating two people who must sit together as a single unit.', 'Glue them into one block, arrange the block with the others, then multiply by 2! for the order within the block.')],
    misc=[('The number of ways to choose 2 from 6 is 6 × 5 = 30.', 'That counts ordered pairs; the number of selections is 30/2! = 15.'),
          ('The arrangements of MISS number 4! = 24.', 'The two S are identical: 4!/2! = 12.')],
))

WORDS = ['BANANA', 'LETTER', 'PEPPER', 'ALGEBRA', 'GEOMETRY', 'MISSISSIPPI', 'STATISTICS', 'CALCULUS', 'INDUCTION', 'PARALLEL', 'COMMITTEE', 'SUCCESS', 'BOOKKEEPER', 'TOMORROW']


@R.add('ch03-st3', 'C3', (1, 5), 'short')
def count_words(rng, slot):
    w = rng.choice(WORDS)
    from collections import Counter
    cnt = Counter(w)
    tot = math.factorial(len(w))
    den = 1
    for v in cnt.values():
        den *= math.factorial(v)
    N = tot // den
    rep = ', '.join(f'{k}×{v}' for k, v in cnt.items() if v > 1)
    if slot.d >= 3:
        L = w[0]
        cnt2 = Counter(w[1:])
        den2 = 1
        for v in cnt2.values():
            den2 *= math.factorial(v)
        N2 = math.factorial(len(w) - 1) // den2
        return mk(f'Find the number of different arrangements of the letters of the word {w} (a) in total (b) that begin with the letter {L}.', f'(a) {N} (b) {N2}',
                  f'(a) {len(w)}!/({" × ".join(str(v) + "!" for v in cnt.values() if v > 1)}) (M1) = {N} (A1). (b) fix {L}, arrange the remaining {len(w) - 1} letters (M1) = {N2} (A1).', 4)
    return mk(f'Find the number of different arrangements of the letters of the word {w}.', str(N), f'{len(w)}! ÷ (repeated letters {rep}) (M1 A1); {N} (A1).', 3)


@R.add('ch03-st3', 'C3', (2, 5), 'short')
def count_committee(rng, slot):
    m, w = rng.randint(4, 9), rng.randint(4, 9)
    k = rng.randint(3, 5)
    kind = rng.choice(['any', 'exact', 'atleast'])
    grp = rng.choice([('men', 'women'), ('boys', 'girls'), ('teachers', 'students'), ('juniors', 'seniors')])
    if kind == 'any':
        N = math.comb(m + w, k)
        return mk(f'A committee of {k} is chosen from {m} {grp[0]} and {w} {grp[1]}. Find the number of possible committees.', str(N), f'{m + w}C{k} (M1) = {N} (A1).', 2)
    if kind == 'exact':
        j = rng.randint(1, k - 1)
        N = math.comb(m, j) * math.comb(w, k - j)
        return mk(f'A committee of {k} is chosen from {m} {grp[0]} and {w} {grp[1]}. Find the number of committees with exactly {j} {grp[0]}.', str(N),
                  f'{m}C{j} × {w}C{k - j} (M1 A1) = {N} (A1).', 3)
    N = math.comb(m + w, k) - math.comb(w, k)
    return mk(f'A team of {k} is chosen from {m} {grp[0]} and {w} {grp[1]}. Find the number of teams that contain at least one of the {grp[0]}.', str(N),
              f'total {m + w}C{k} minus teams with no {grp[0]} {w}C{k} (M1 A1) = {N} (A1).', 3)


@R.add('ch03-st3', 'C3', (2, 5), 'short')
def count_row(rng, slot):
    n = rng.randint(5, 8)
    kind = rng.choice(['together', 'apart', 'ends', 'digits'])
    who1, who2 = name(rng), name(rng)
    if who1 == who2:
        return None
    if kind == 'together':
        N = 2 * math.factorial(n - 1)
        return mk(f'{n} friends, including {who1} and {who2}, sit in a row. Find the number of arrangements in which {who1} and {who2} sit next to each other.', str(N),
                  f'treat the pair as one unit: {n - 1}! (M1); × 2! (M1); {N} (A1).', 3)
    if kind == 'apart':
        N = math.factorial(n) - 2 * math.factorial(n - 1)
        return mk(f'{n} people, including {who1} and {who2}, stand in a line. Find the number of arrangements in which {who1} and {who2} are not next to each other.', str(N),
                  f'{n}! − 2 × {n - 1}! (M1 A1) = {N} (A1).', 3)
    if kind == 'ends':
        N = 2 * math.factorial(n - 2)
        return mk(f'{n} runners, including {who1} and {who2}, line up for a photo. Find the number of arrangements with {who1} and {who2} at the two ends.', str(N),
                  f'2 ways for the ends (A1); {n - 2}! for the rest (M1); {N} (A1).', 3)
    d = rng.choice([5, 6, 7])
    L = rng.choice([3, 4])
    N = math.perm(d, L)
    ev = sum(1 for _ in range(1))  # placeholder
    digs = list(range(1, d + 1))
    evens = [v for v in digs if v % 2 == 0]
    Ne = len(evens) * math.perm(d - 1, L - 1)
    return mk(f'{L}-digit numbers are formed from the digits {", ".join(map(str, digs))}, with no digit repeated. Find (a) how many numbers can be formed (b) how many of them are even.', f'(a) {N} (b) {Ne}',
              f'(a) {d}P{L} = {N} (M1 A1). (b) last digit even: {len(evens)} choices (M1); × {d - 1}P{L - 1} (M1); {Ne} (A1).', 5)


@R.add('ch03-st3', 'C1', (1, 3), 'mcq')
def perm_comb_mcq(rng, slot):
    n, r = rng.randint(6, 12), rng.randint(2, 4)
    kind = rng.choice(['perm', 'comb'])
    ctx = {'perm': f'In how many ways can gold, silver and bronze{" and fourth place" if r == 4 else ""} be awarded among {n} competitors?' if r >= 3 else f'In how many ways can a captain and vice-captain be chosen from {n} players?',
           'comb': f'In how many ways can {r} books be chosen from {n} different books?'}[kind]
    if kind == 'perm':
        r = 3 if 'bronze' in ctx and 'fourth' not in ctx else (4 if 'fourth' in ctx else 2)
    right = math.perm(n, r) if kind == 'perm' else math.comb(n, r)
    wr = [math.comb(n, r) if kind == 'perm' else math.perm(n, r), n ** r, n * r]
    wr = [str(w) for w in dict.fromkeys(wr) if w != right]
    return mcq(rng, ctx, str(right), wr[:3], 'Order matters → permutation; order irrelevant → combination.')


@R.add('ch03-st3', 'C2', (2, 4), 'explain')
def perm_comb_explain(rng, slot):
    n, r = rng.randint(6, 12), rng.randint(2, 4)
    task = rng.choice([('choosing {r} people to form a team from {n}', 'combination'), ('arranging {r} of {n} books on a shelf', 'permutation'),
                       ('selecting {r} toppings from {n} available', 'combination'), ('awarding {r} different prizes to {n} students, at most one each', 'permutation'),
                       ('forming a {r}-letter code from {n} different letters without repetition', 'permutation'), ('choosing {r} questions to answer from {n}', 'combination')])
    t_, kind = task
    val = math.comb(n, r) if kind == 'combination' else math.perm(n, r)
    return mk(f'Explain whether {t_.format(n=n, r=r)} is a permutation or a combination problem, and find the number of ways.', f'{kind}: {val}',
              f'{"order does not matter" if kind == "combination" else "order matters"} (R1); {n}{"C" if kind == "combination" else "P"}{r} (M1) = {val} (A1).', 3, 'explain')


@R.add('ch03-st3', 'C4', (3, 5), 'multi_step', style='ext')
def count_parts(rng, slot):
    g, b = rng.randint(4, 7), rng.randint(4, 7)
    k = rng.randint(4, 5)
    tot = math.comb(g + b, k)
    eq = math.comb(g, k // 2) * math.comb(b, k - k // 2)
    atl = tot - math.comb(b, k) - math.comb(g, k)
    nm1, nm2 = name(rng), name(rng)
    both_not = math.comb(g + b - 2, k) + 2 * math.comb(g + b - 2, k - 1)
    parts = [(f'Find the number of ways of choosing a team of {k} from the {g + b} students.', str(tot), 'M1 A1', 2, True),
             (f'Find the number of teams with {k // 2} girls and {k - k // 2} boys.', str(eq), 'product (M1) A1', 2, True),
             ('Find the number of teams that contain at least one girl and at least one boy.', str(atl), 'complement (M1) A1', 2, True),
             (f'Two of the students, {nm1} and {nm2}, refuse to be in the team together. Find the number of possible teams.', str(both_not), f'total − teams containing both {g + b - 2}C{k - 2} (M1) A1', 2, True),
             (f'The chosen team of {k} stands in a line for a photo. Find the number of arrangements.', str(math.factorial(k)), 'A1', 1, False)]
    return build_parts(rng, [f'A school has {g} girls and {b} boys available for a quiz team.', f'A team of {k} is selected from {g} girls and {b} boys.'], parts, 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch03-st4', F(
    terms=[('extended binomial theorem', '(1 + x)ⁿ = 1 + nx + n(n − 1)x²/2! + n(n − 1)(n − 2)x³/3! + … for n ∈ ℚ, valid for |x| < 1'),
           ('interval of validity', 'the set of x for which an infinite binomial expansion converges, e.g. |bx| < a for (a + bx)ⁿ')],
    facts=[('(1 + x)⁻¹ =', '1 − x + x² − x³ + …', ['1 + x + x² + …', '1 − x', '−1 − x − x² − …'], 'n = −1.'),
           ('The expansion of (1 − 2x)^(1/2) is valid for', '|x| < 1/2', ['|x| < 1', '|x| < 2', 'all x'], '|2x| < 1.'),
           ('The coefficient of x in (1 + x)^(1/3) is', '1/3', ['3', '1', '−1/3'], 'n x.')],
    why=[('Explain why the expansion of (1 + x)ⁿ is infinite when n is negative or fractional.', 'The coefficients n(n − 1)…(n − r + 1)/r! never become zero because n − r + 1 is never 0 for a non-negative integer r, so the series does not terminate.'),
         ('Explain why (4 + x)^(1/2) must be written as 2(1 + x/4)^(1/2) before expanding.', 'The extended binomial theorem is stated for (1 + x)ⁿ; factoring out 4^(1/2) = 2 gives that form, valid for |x/4| < 1, i.e. |x| < 4.')],
    misc=[('(2 + x)⁻¹ = 2⁻¹(1 + x)⁻¹.', '(2 + x)⁻¹ = 2⁻¹(1 + x/2)⁻¹: x must also be divided by 2.'),
          ('The expansion of (1 + 3x)⁻² is valid for |x| < 1.', 'Validity needs |3x| < 1, i.e. |x| < 1/3.')],
))


@R.add('ch03-st4', 'C3', (2, 5), 'short', style='p1')
def ext_binom(rng, slot):
    c = rng.choice([1, 1, 4, 9, 2, 8])
    b = nz(rng, -3, 3)
    p = rng.choice([-1, -2, sp.Rational(1, 2), sp.Rational(-1, 2), sp.Rational(1, 3), -3]) if c in (1, 2) else (rng.choice([sp.Rational(1, 2), sp.Rational(-1, 2)]) if c in (4, 9) else rng.choice([sp.Rational(1, 3), sp.Rational(-1, 3)]))
    f = (c + b * x) ** p
    ser = sp.series(f, x, 0, 3).removeO()
    txt = _asc(sp.expand(ser))
    lim = sp.Rational(c, abs(b))
    return mk(f'Find the first three terms in the expansion of ({c} {"+" if b > 0 else "−"} {abs(b) if abs(b) > 1 else ""}x)^({P(p)}) in ascending powers of x, and state the values of x for which the expansion is valid.', f'{txt}; |x| < {R_(lim)}',
              (f'({c})^({P(p)})(1 + {P(sp.Rational(b, c) * x)})^({P(p)}) (M1); ' if c != 1 else '') + f'n = {P(p)}: 1 + nx + n(n − 1)x²/2 with x → {P(sp.Rational(b, c) * x)} (M1); {txt} (A1 A1); |x| < {R_(lim)} (A1).', 5)


@R.add('ch03-st4', 'C3', (2, 5), 'short', style='p2')
def ext_binom_approx(rng, slot):
    kind = rng.choice([('√', sp.Rational(1, 2), [1.02, 0.98, 1.04, 1.06, 0.96]), ('∛', sp.Rational(1, 3), [1.03, 0.97, 1.09, 1.06]), ('1/', -1, [1.01, 1.05, 0.95, 1.02])])
    sym, p, vals = kind
    v = rng.choice(vals)
    h = sp.nsimplify(v) - 1
    ser = 1 + p * x + p * (p - 1) / 2 * x ** 2
    approx = float(ser.subs(x, h))
    true = v ** float(p)
    return mk(f'Use the first three terms of the expansion of (1 + x)^({P(p)}) to estimate {sym}{v:g}. Give your answer to 6 decimal places and state the error compared with the calculator value.', f'{approx:.6f}; error {sci(abs(true - approx))}',
              f'{P(1 + p * x + p * (p - 1) / 2 * x ** 2)} (M1 A1); x = {float(h):g} (M1); {approx:.6f} (A1); calculator {true:.6f} (A1).', 5)


@R.add('ch03-st4', 'C1', (1, 3), 'mcq')
def ext_binom_mcq(rng, slot):
    b = rng.choice([2, 3, 4, 5])
    p = rng.choice([-1, -2, sp.Rational(1, 2), sp.Rational(-1, 2)])
    right = f'|x| < 1/{b}'
    return mcq(rng, f'The expansion of (1 + {b}x)^({P(p)}) is valid for', right, [f'|x| < {b}', '|x| < 1', f'|x| > 1/{b}'], f'Need |{b}x| < 1.')


@R.add('ch03-st4', 'C2', (2, 4), 'explain')
def ext_binom_explain(rng, slot):
    c = rng.choice([4, 9, 16, 25])
    b = rng.randint(1, 5)
    return mk(f'Explain why the expansion of ({c} + {b}x)^(1/2) is valid only for |x| < {R_(sp.Rational(c, b))}, and write down its first two terms.', f'{P(sp.sqrt(c))} + {P(sp.Rational(b, 2) / sp.sqrt(c) * x)}',
              f'({c} + {b}x)^(1/2) = {P(sp.sqrt(c))}(1 + {P(sp.Rational(b, c) * x)})^(1/2) (M1); valid for |{P(sp.Rational(b, c) * x)}| < 1 (R1); {P(sp.sqrt(c))} + {P(sp.Rational(b, 2) / sp.sqrt(c) * x)} (A1).', 3, 'explain')


@R.add('ch03-st4', 'C4', (3, 5), 'multi_step', style='ext')
def ext_binom_parts(rng, slot):
    a, b = rng.choice([(1, 2), (1, 3), (2, 1), (1, 4)])
    f = (1 + a * x) / (1 - b * x)
    ser = _asc(sp.expand(sp.series(f, x, 0, 4).removeO()))
    xv = rng.choice([sp.Rational(1, 10), sp.Rational(1, 20), sp.Rational(1, 100)])
    approx = float(sp.series(f, x, 0, 4).removeO().subs(x, xv))
    parts = [(f'Expand (1 − {b if b > 1 else ""}x)⁻¹ as far as the term in x³.', _asc(sp.expand(sp.series(1 / (1 - b * x), x, 0, 4).removeO())), 'M1 A1', 2, True),
             (f'Hence find the expansion of (1 + {a if a > 1 else ""}x)/(1 − {b if b > 1 else ""}x) up to the term in x³.', ser, 'multiply (M1) A1 A1', 3, True),
             ('State the range of values of x for which the expansion is valid.', f'|x| < 1/{b}' if b > 1 else '|x| < 1', 'A1', 1, True),
             (f'Use your expansion with x = {R_(xv)} to estimate {R_(f.subs(x, xv))} as a decimal.', f'{approx:.6f}', 'M1 A1', 2, True),
             ('Explain why x = 1/2 would not give a reliable estimate.', f'|{b}x| = {R_(sp.Rational(b, 2))} ≥ 1, outside the interval of validity' if b >= 2 else 'convergence is slow; many terms needed', 'R1', 1, False)]
    return build_parts(rng, ['This question uses the extended binomial theorem.', f'Let f(x) = (1 + {a if a > 1 else ""}x)/(1 − {b if b > 1 else ""}x).'], parts, 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch03-st5', F(
    terms=[('proof by mathematical induction', 'prove P(1) (basis), then show that P(k) true ⇒ P(k + 1) true (inductive step); hence P(n) is true for all n ∈ ℤ⁺'),
           ('proof by contradiction', 'assume the negation of the statement and deduce a contradiction, so the statement must be true'),
           ('counterexample', 'a single example showing that a general statement is false')],
    facts=[('In proof by induction, the inductive step shows that', 'P(k) ⇒ P(k + 1)', ['P(k + 1) ⇒ P(k)', 'P(1) ⇒ P(2) only', 'P(k) is true for all k'], 'Together with the basis.'),
           ('To prove √2 is irrational by contradiction, assume', '√2 = p/q with p, q integers having no common factor', ['√2 is rational and p is odd', '√2 is irrational', '√2 = 1.414'], 'Negate the statement.'),
           ('A counterexample to "all primes are odd" is', '2', ['1', '9', '3'], '2 is prime and even.')],
    why=[('Explain why both the basis and the inductive step are needed in proof by induction.', 'The inductive step alone only shows truth passes from one case to the next; without a true starting case nothing is established. The basis alone proves one case.'),
         ('Explain the logic of proof by contradiction.', 'If assuming the statement is false leads to an impossible result, the assumption must be wrong, so the statement is true.'),
         ('Explain why one counterexample is enough to disprove a statement, but many examples cannot prove it.', 'A universal statement must hold in every case; one failure shows it is false, while examples cover only finitely many of infinitely many cases.')],
    misc=[('In the inductive step I assume P(k + 1) and prove P(k).', 'Assume P(k) and deduce P(k + 1).'),
          ('Because n² + n + 41 is prime for n = 1 to 10, it is always prime.', 'n = 40 gives 1681 = 41², a counterexample.')],
))

IND_SUMS = [
    ('Σ from r = 1 to n of r = n(n + 1)/2', lambda k: k * (k + 1) / 2),
    ('Σ from r = 1 to n of r² = n(n + 1)(2n + 1)/6', None),
    ('Σ from r = 1 to n of (2r − 1) = n²', None),
    ('Σ from r = 1 to n of r(r + 1) = n(n + 1)(n + 2)/3', None),
    ('Σ from r = 1 to n of 1/(r(r + 1)) = n/(n + 1)', None),
    ('Σ from r = 1 to n of r × r! = (n + 1)! − 1', None),
    ('Σ from r = 1 to n of r³ = n²(n + 1)²/4', None),
    ('Σ from r = 1 to n of r × 2ʳ = (n − 1)2ⁿ⁺¹ + 2', None),
]
IND_STEP = ['k(k + 1)/2 + (k + 1) = (k + 1)(k + 2)/2', 'k(k + 1)(2k + 1)/6 + (k + 1)² = (k + 1)(k + 2)(2k + 3)/6', 'k² + (2k + 1) = (k + 1)²',
            'k(k + 1)(k + 2)/3 + (k + 1)(k + 2) = (k + 1)(k + 2)(k + 3)/3', 'k/(k + 1) + 1/((k + 1)(k + 2)) = (k + 1)/(k + 2)', '(k + 1)! − 1 + (k + 1)(k + 1)! = (k + 2)! − 1',
            'k²(k + 1)²/4 + (k + 1)³ = (k + 1)²(k + 2)²/4', '(k − 1)2ᵏ⁺¹ + 2 + (k + 1)2ᵏ⁺¹ = k·2ᵏ⁺² + 2']


@R.add('ch03-st5', 'C3', (2, 5), 'short', style='p1')
def induction_sum(rng, slot):
    i = rng.randrange(len(IND_SUMS))
    stmt = IND_SUMS[i][0]
    frame = rng.choice(['Prove by mathematical induction that {s} for all n ∈ ℤ⁺.', 'Use mathematical induction to prove that {s}, n ≥ 1.'])
    return mk(frame.format(s=stmt), 'proof', f'Basis: n = 1 both sides equal (A1); assume true for n = k (M1); add the (k + 1)th term (M1); {IND_STEP[i]} (A1); true for k ⇒ true for k + 1, and true for n = 1, so true for all n ∈ ℤ⁺ (R1).', 6)


@R.add('ch03-st5', 'C3', (2, 5), 'short', style='p1')
def induction_div(rng, slot):
    kind = rng.choice(['an1', 'diff', 'mixed'])
    if kind == 'an1':
        a = rng.randint(3, 11)
        d = a - 1
        return mk(f'Prove by mathematical induction that {a}ⁿ − 1 is divisible by {d} for all n ∈ ℤ⁺.', 'proof',
                  f'n = 1: {a} − 1 = {d} (A1); assume {a}ᵏ − 1 = {d}m (M1); {a}ᵏ⁺¹ − 1 = {a}({a}ᵏ − 1) + {a - 1} = {d}({a}m + 1) (M1 A1); conclusion (R1).', 5)
    if kind == 'diff':
        a, b = rng.choice([(7, 3), (5, 1), (9, 5), (8, 3), (11, 4), (6, 2)])
        d = a - b
        return mk(f'Prove by induction that {a}ⁿ − {b}ⁿ is divisible by {d} for all n ∈ ℤ⁺.'.replace(' − 1ⁿ', ' − 1'), 'proof',
                  f'n = 1: {d} (A1); assume {a}ᵏ − {b}ᵏ = {d}m (M1); {a}ᵏ⁺¹ − {b}ᵏ⁺¹ = {a}({a}ᵏ − {b}ᵏ) + ({a} − {b}){b}ᵏ (M1 A1); both terms divisible by {d} (R1).', 5)
    c = rng.choice([(3, 2, 1, 'n³ − n', 6), (2, 3, 5, 'n³ + 2n', 3), (1, 1, 1, 'n³ + 5n', 6), (1, 1, 1, '5ⁿ + 3', 4)])
    _, _, _, expr, d = c
    return mk(f'Prove by mathematical induction that {expr} is divisible by {d} for all n ∈ ℤ⁺.', 'proof',
              f'Basis n = 1 (A1); assume true for n = k (M1); express the n = k + 1 case as (the n = k case) + (a multiple of {d}) (M1 A1); conclusion (R1).', 5)


@R.add('ch03-st5', 'C3', (2, 5), 'short')
def counterexample(rng, slot):
    pool = []
    for a in (11, 17, 41):
        m = next(n for n in range(1, 200) if not sp.isprime(n * n + n + a))
        pool.append((f'n² + n + {a} is prime for all n ∈ ℕ', f'n = {m}: {m * m + m + a} = {sp.factorint(m * m + m + a)}'))
    pool += [('2ⁿ + 1 is prime for all n ∈ ℤ⁺', 'n = 3: 9 = 3 × 3'), ('n² > n for all real n', 'n = 1/2: 1/4 < 1/2'), ('if a² = b² then a = b', 'a = 2, b = −2'),
             ('the sum of two irrational numbers is irrational', '√2 + (−√2) = 0'), ('2ⁿ > n² for all n ∈ ℤ⁺', 'n = 3: 8 < 9'), ('x² − 5x + 6 > 0 for all real x', 'x = 2.5: −0.25'),
             ('every odd number greater than 1 is prime', '9 = 3 × 3'), ('√(a + b) = √a + √b for a, b > 0', 'a = b = 1: √2 ≠ 2')]
    st_, ce = rng.choice(pool)
    ce = re.sub(r'\{(\d+): (\d+)\}', lambda m_: m_.group(1) + ('²' if m_.group(2) == '2' else ''), ce)
    ce = re.sub(r'\{(\d+): 1, (\d+): 1\}', r'\1 × \2', ce)
    return mk(f'Find a counterexample to show that the statement "{st_}" is false.', ce, f'Valid counterexample (M1): {ce} (A1); shows the statement fails (R1).', 3)


@R.add('ch03-st5', 'C3', (3, 5), 'short', style='p1')
def contradiction_proof(rng, slot):
    kind = rng.choice(['root', 'primes', 'even', 'log'])
    if kind == 'root':
        p = rng.choice([2, 3, 5, 7, 11, 13])
        return mk(f'Prove by contradiction that √{p} is irrational.', 'proof',
                  f'Assume √{p} = a/b in lowest terms (M1); a² = {p}b² so {p} divides a² and hence a (A1); a = {p}c gives b² = {p}c², so {p} divides b (A1); contradiction with lowest terms (R1).', 4)
    if kind == 'primes':
        return mk('Prove by contradiction that there are infinitely many prime numbers.', 'proof',
                  'Assume finitely many primes p₁, …, pₙ (M1); consider N = p₁p₂…pₙ + 1 (A1); N leaves remainder 1 on division by each pᵢ (A1); so N is prime or has a prime factor not in the list: contradiction (R1).', 4)
    if kind == 'log':
        a, b = rng.choice([(2, 3), (2, 5), (3, 5), (2, 7), (3, 7)])
        return mk(f'Prove by contradiction that log{sub(a)} {b} is irrational.', 'proof',
                  f'Assume log{sub(a)} {b} = p/q, p, q ∈ ℤ⁺ (M1); {a}^(p/q) = {b} so {a}ᵖ = {b}^q (A1); LHS is a power of {a}, RHS a power of {b}, impossible by unique factorisation (R1 A1).', 4)
    k = rng.randint(2, 6)
    return mk(f'Prove by contradiction that there are no integers m and n such that {2 * k}m + {2 * k + 2}n = 1.', 'proof',
              f'Assume such integers exist (M1); LHS = 2({k}m + {k + 1}n) is even (A1); 1 is odd: contradiction (R1).', 3)


@R.add('ch03-st5', 'C1', (1, 3), 'mcq')
def proof_type_mcq(rng, slot):
    pool = [('Σ from r = 1 to n of r³ = n²(n + 1)²/4 for all n ∈ ℤ⁺', 'mathematical induction'), ('√3 is irrational', 'contradiction'),
            ('every quadratic has two distinct real roots is false', 'a counterexample'), ('7ⁿ − 1 is divisible by 6 for all n ∈ ℤ⁺', 'mathematical induction'),
            ('there is no largest prime', 'contradiction'), ('"all triangles are acute" is false', 'a counterexample'), ('2ⁿ ≥ n + 1 for all n ∈ ℤ⁺', 'mathematical induction'),
            ('log₂ 5 is irrational', 'contradiction')]
    st_, ans = rng.choice(pool)
    wr = [w for w in ['mathematical induction', 'contradiction', 'a counterexample', 'checking cases n = 1 to 10'] if w != ans]
    return mcq(rng, f'The most appropriate method to establish that {st_} is', ans, wr, f'{ans[0].upper() + ans[1:]} suits this kind of statement.')


@R.add('ch03-st5', 'C2', (2, 4), 'explain')
def induction_flaw_explain(rng, slot):
    a = rng.randint(3, 9)
    kind = rng.choice(['nobasis', 'assume'])
    if kind == 'nobasis':
        return mk(f'A student "proves" that {a}ⁿ + 1 is divisible by {a - 1} for all n by showing only that if {a}ᵏ + 1 is divisible by {a - 1} then so is {a}ᵏ⁺¹ + 1. Explain why the argument fails.', 'the basis case is false',
                  f'n = 1: {a + 1} is not divisible by {a - 1} (R1 A1); the inductive step alone does not establish any case (R1).', 3, 'explain')
    return mk('In the inductive step of a proof, a student writes "assume the result is true for all n" and then shows it is true for n = k + 1. Explain the error.', 'assumes what is to be proved',
              'The assumption must be for a single value n = k only (R1); assuming it for all n is circular (R1); correct structure: P(k) ⇒ P(k + 1) (A1).', 3, 'explain')


@R.add('ch03-st5', 'C4', (4, 5), 'multi_step', style='p3')
def induction_ineq_parts(rng, slot):
    kind = rng.choice(['pow', 'fact'])
    if kind == 'pow':
        n0 = next(n for n in range(1, 50) if all(2 ** m > m * m for m in range(n, 60)))
        parts = [('Find 2ⁿ and n² for n = 1, 2, …, 6.', ', '.join(f'({2 ** m}, {m * m})' for m in range(1, 7)), 'A1 A1', 2, True),
                 ('Conjecture the values of n for which 2ⁿ > n².', f'n = 1 and n ≥ {n0}', 'A1', 1, True),
                 (f'Prove that 2ⁿ > n² for all integers n ≥ {n0}.', 'proof', f'basis n = {n0} (A1); assume 2ᵏ > k² (M1); 2ᵏ⁺¹ > 2k² (A1); 2k² ≥ (k + 1)² for k ≥ 3 (M1 R1); conclusion (R1)', 6, True),
                 ('Explain why the proof does not start at n = 1.', 'the statement is false for n = 2, 3, 4', 'R1', 1, True),
                 ('Show that 2k² ≥ (k + 1)² is equivalent to k² − 2k − 1 ≥ 0 and state the values of k for which it holds.', 'k ≥ 1 + √2', 'M1 A1', 2, False)]
        return build_parts(rng, ['This question compares the growth of 2ⁿ and n².', 'In this question you will conjecture and prove an inequality.'], parts, 4)
    b = rng.choice([2, 3])
    n0 = next(n for n in range(1, 50) if all(math.factorial(m) > b ** m for m in range(n, 40)))
    parts = [(f'Find n! and {b}ⁿ for n = 1, …, {n0 + 1}.', ', '.join(f'({math.factorial(m)}, {b ** m})' for m in range(1, n0 + 2)), 'A1 A1', 2, True),
             (f'Prove by induction that n! > {b}ⁿ for all integers n ≥ {n0}.', 'proof', f'basis n = {n0} (A1); assume k! > {b}ᵏ (M1); (k + 1)! = (k + 1)k! > (k + 1){b}ᵏ (A1); k + 1 > {b} (R1); conclusion (R1)', 5, True),
             (f'Explain why the result fails for n = {n0 - 1}.', f'{n0 - 1}! = {math.factorial(n0 - 1)} ≤ {b ** (n0 - 1)}', 'A1', 1, True),
             ('Generalise: for a positive integer b, explain why n! > bⁿ for all sufficiently large n.', 'once n + 1 > b each step multiplies the left by more than b', 'R1 R1', 2, False)]
    return build_parts(rng, ['This question investigates factorials and powers.', f'Let P(n) be the statement n! > {b}ⁿ.'], parts, 3)


@R.add('ch03-st5', 'C4', (3, 5), 'multi_step', style='ext')
def induction_parts(rng, slot):
    a = rng.choice([2, 3, 4, 5])
    n = rng.randint(4, 7)
    S = lambda m: sum(r * a ** (r - 1) for r in range(1, m + 1))
    parts = [(f'Find Σ from r = 1 to n of (2r − 1) for n = 1, 2, 3, 4.', '1, 4, 9, 16', 'A1', 1, True),
             ('Conjecture a formula and prove it by mathematical induction.', 'n²; proof', 'conjecture (A1); basis (A1); inductive step (M1 A1); conclusion (R1)', 5, True),
             (f'Prove by induction that {a + 1}ⁿ − 1 is divisible by {a} for n ∈ ℤ⁺.', 'proof', 'basis (A1); step (M1 A1); conclusion (R1)', 4, True),
             (f'Use a counterexample to show that "{a + 1}ⁿ − 1 is divisible by {a + 1 if a % 2 else a * 2}" is false.'.replace('divisible by', 'divisible by'), f'n = 1: {a}', 'A1', 1, False)]
    return build_parts(rng, ['This question is about proof by mathematical induction.', 'In this question n is a positive integer.'], parts, 3)


# =============================================================================================
# ch04 Complex numbers (SL 1.12–1.14 as listed; AHL 1.12–1.14)
# =============================================================================================
I_ = sp.I


def _imt(b):
    s_ = nice(b)
    if s_ == '1':
        return 'i'
    if ' ' in s_:
        return f'({s_})i'
    if '√' in s_:
        j = s_.index('√')
        return s_[:j] + 'i' + s_[j:]
    if '/' in s_:
        nu, de = s_.split('/', 1)
        return ('i' if nu == '1' else nu + 'i') + '/' + de
    return s_ + 'i'


def cz(z):
    """complex number a + bi as IB text"""
    z = sp.nsimplify(sp.expand(sp.radsimp(sp.expand_complex(z))))
    a, b = sp.simplify(sp.re(z)), sp.simplify(sp.im(z))
    if b == 0:
        return nice(a)
    it = _imt(abs(b)) if b.is_number and (b > 0 or b < 0) else _imt(b)
    if a == 0:
        return ('−' if b < 0 else '') + it
    return nice(a) + (' − ' if b < 0 else ' + ') + it


def ang(a):
    return P(sp.nsimplify(a))


def cis_txt(r, th, euler=False):
    r = sp.nsimplify(r)
    rt = '' if r == 1 else P(r)
    if '/' in rt or ' ' in rt:
        rt = f'({rt})'
    if euler:
        if th == 0:
            return rt or '1'
        at = ang(th)
        at = at.replace('π', 'πi') if 'π' in at else f'{at}i'
        return f'{rt}e^({at})'
    return f'{rt} cis({ang(th)})' if rt else f'cis({ang(th)})'


def nice_ang(th):
    """True if the exact cos/sin of th are simple surds (multiples of π/6 or π/4)"""
    k = sp.nsimplify(12 * th / pi)
    return k.is_integer and (int(k) % 2 == 0 or int(k) % 3 == 0)


def princ(th):
    th = sp.nsimplify(th)
    while th > pi:
        th -= 2 * pi
    while th <= -pi:
        th += 2 * pi
    return th


STD_ARG = [pi / 6, pi / 4, pi / 3, pi / 2, 2 * pi / 3, 3 * pi / 4, 5 * pi / 6, pi, -pi / 6, -pi / 4, -pi / 3, -pi / 2, -2 * pi / 3, -3 * pi / 4, -5 * pi / 6]


def _rand_z(rng, lo=-6, hi=6):
    return nz(rng, lo, hi) + nz(rng, lo, hi) * I_


R.facts('ch04-st1', F(
    terms=[('imaginary unit', 'the number i with i² = −1'),
           ('complex number (Cartesian form)', 'a number z = a + bi with a, b ∈ ℝ; a = Re(z) is the real part and b = Im(z) the imaginary part'),
           ('complex conjugate', 'the number z* = a − bi for z = a + bi; zz* = a² + b² is real'),
           ('Argand diagram', 'the complex plane, in which z = a + bi is plotted as the point (a, b)')],
    facts=[('i² =', '−1', ['1', 'i', '−i'], 'Definition of i.'),
           ('i³ =', '−i', ['i', '−1', '1'], 'i³ = i² × i.'),
           ('(2 + 3i)(2 − 3i) =', '13', ['4 − 9i²', '−5', '4 + 9i'], 'zz* = a² + b².'),
           ('Re(4 − 7i) =', '4', ['−7', '7', '4 − 7i'], 'Real part.'),
           ('The conjugate of −3 + 5i is', '−3 − 5i', ['3 − 5i', '3 + 5i', '5 − 3i'], 'Change the sign of the imaginary part.')],
    why=[('Explain why, to divide by a + bi, you multiply the numerator and denominator by a − bi.', '(a + bi)(a − bi) = a² + b² is real, so the denominator becomes real and the quotient can be written in the form x + iy.'),
         ('Explain why two complex numbers are equal only if their real parts and imaginary parts are both equal.', 'If a + bi = c + di then a − c = (d − b)i; a real number can equal an imaginary one only if both are 0, so a = c and b = d.'),
         ('Explain the geometric meaning of z* on an Argand diagram.', 'z* is the reflection of z in the real axis, since the real part is kept and the imaginary part changes sign.')],
    misc=[('√(−4) × √(−9) = √36 = 6.', '√(−4) = 2i and √(−9) = 3i, so the product is 6i² = −6; √a√b = √(ab) fails for negative a and b.'),
          ('|3 + 4i| = 3 + 4 = 7.', '|3 + 4i| = √(3² + 4²) = 5.')],
))


@R.add('ch04-st1', 'C1', (1, 3), 'mcq')
def cx_basic_mcq(rng, slot):
    kind = rng.choice(['pow', 'conj', 'prod', 'reim'])
    if kind == 'pow':
        n = rng.randint(5, 60)
        vals = {0: '1', 1: 'i', 2: '−1', 3: '−i'}
        return mcq(rng, f'i{sup(n)} =', vals[n % 4], [v for k_, v in vals.items() if k_ != n % 4], f'{n} = 4 × {n // 4} + {n % 4} and i⁴ = 1.')
    z = _rand_z(rng)
    if kind == 'conj':
        return mcq(rng, f'If z = {cz(z)}, then z* =', cz(sp.conjugate(z)), [cz(-z), cz(-sp.conjugate(z)), cz(I_ * z)], 'Change the sign of the imaginary part.')
    if kind == 'prod':
        w = _rand_z(rng, -4, 4)
        r = sp.expand(z * w)
        a, b = sp.re(z), sp.im(z)
        c, d = sp.re(w), sp.im(w)
        return mcq(rng, f'({cz(z)})({cz(w)}) =', cz(r), [cz(a * c + b * d + (a * d + b * c) * I_), cz(a * c + b * d * I_), cz(a * c - b * d - (a * d + b * c) * I_)], 'Expand and use i² = −1.')
    return mcq(rng, f'For z = {cz(z)}, Im(z) =', P(sp.im(z)), [cz(sp.im(z) * I_), P(sp.re(z)), P(-sp.im(z))], 'The imaginary part is the real coefficient of i.')


@R.add('ch04-st1', 'C3', (1, 4), 'short', style='p1')
def cx_arith(rng, slot):
    z, w = _rand_z(rng, -5, 5), _rand_z(rng, -4, 4)
    kind = rng.choice(['div', 'div', 'expr', 'sq'] if slot.d >= 2 else ['expr', 'sq', 'div'])
    if kind == 'div':
        q = sp.expand(sp.radsimp(z / w))
        return mk(f'Given z = {cz(z)} and w = {cz(w)}, find z/w in the form a + bi.', cz(q),
                  f'multiply by w* = {cz(sp.conjugate(w))}/({cz(sp.conjugate(w))}) (M1); numerator {cz(sp.expand(z * sp.conjugate(w)))}, denominator {sp.expand(w * sp.conjugate(w))} (A1); {cz(q)} (A1).', 3)
    if kind == 'sq':
        r = sp.expand(z ** 2 * sp.conjugate(w))
        return mk(f'Given z = {cz(z)} and w = {cz(w)}, find z²w* in the form a + bi.', cz(r), f'z² = {cz(sp.expand(z ** 2))} (A1); w* = {cz(sp.conjugate(w))} (A1); product {cz(r)} (A1).', 3)
    p, q = nz(rng, -3, 3), nz(rng, -3, 3)
    r = sp.expand(p * z + q * I_ * w)
    zt = f'{p}z' if p != 1 else 'z'
    return mk(f'Given z = {cz(z)} and w = {cz(w)}, find {zt} + {q}iw in the form a + bi.'.replace('+ −', '− ').replace(' 1iw', ' iw'), cz(r),
              f'{q}iw = {cz(sp.expand(q * I_ * w))} using i² = −1 (M1 A1); {cz(r)} (A1).', 3)


@R.add('ch04-st1', 'C3', (2, 5), 'short', style='p1')
def cx_equation(rng, slot):
    kind = rng.choice(['lin', 'conj', 'sqrt', 'quad'])
    if kind == 'quad':
        p, q = nz(rng, -5, 5), rng.randint(1, 6)
        b, c = -2 * p, p * p + q * q
        roots = [p + q * I_, p - q * I_]
        return mk(f'Solve the equation z² {"+" if b >= 0 else "−"} {abs(b)}z + {c} = 0, giving your answers in the form a + bi.'.replace(' + 0z', '').replace(' − 0z', ''),
                  f'z = {cz(roots[0])} or z = {cz(roots[1])}', f'discriminant {b * b - 4 * c} < 0 (M1); z = ({-b} ± √({b * b - 4 * c}))/2 (M1); √({b * b - 4 * c}) = {2 * q}i (A1); {cz(roots[0])}, {cz(roots[1])} (A1).', 4)
    if kind == 'sqrt':
        a, b = rng.randint(1, 6), nz(rng, -6, 6)
        w = sp.expand((a + b * I_) ** 2)
        return mk(f'Find the two square roots of {cz(w)} in the form a + bi, a, b ∈ ℝ.', f'±({cz(a + b * I_)})',
                  f'(a + bi)² = {cz(w)}: a² − b² = {sp.re(w)}, 2ab = {sp.im(w)} (M1 A1); solve, e.g. a⁴ − ({sp.re(w)})a² − {(sp.im(w) / 2) ** 2} = 0 (M1); ±({cz(a + b * I_)}) (A1).', 4)
    a, b = nz(rng, -5, 5), nz(rng, -5, 5)
    zt = a + b * I_
    if kind == 'lin':
        w = _rand_z(rng, -3, 3)
        c = sp.expand(w * zt + 2 * I_)
        return mk(f'Solve ({cz(w)})z + 2i = {cz(c)} for z, giving your answer in the form a + bi.', f'z = {cz(zt)}',
                  f'z = ({cz(c - 2 * I_)})/({cz(w)}) (M1); multiply by the conjugate (M1); {cz(zt)} (A1).', 3)
    p = rng.choice([2, 3, -2])
    rhs = sp.expand(zt + p * I_ * sp.conjugate(zt))
    return mk(f'Find the complex number z such that z {"+" if p > 0 else "−"} {abs(p)}iz* = {cz(rhs)}.', f'z = {cz(zt)}',
              f'let z = a + bi (M1); a + bi {"+" if p > 0 else "−"} {abs(p)}i(a − bi) gives {"" if p == 1 else p}b + a = {sp.re(rhs)} and b + {p}a = {sp.im(rhs)} (M1 A1); a = {a}, b = {b} (A1).'.replace('+ −', '− '), 4)


@R.add('ch04-st1', 'C3', (2, 4), 'short', style='p2')
def cx_plane(rng, slot):
    z, w = _rand_z(rng, -7, 7), _rand_z(rng, -7, 7)
    if z == w:
        return None
    kind = rng.choice(['dist', 'mod', 'mid'])
    if kind == 'dist':
        d = sp.sqrt(sp.expand((z - w) * sp.conjugate(z - w)))
        return mk(f'The points A and B on an Argand diagram represent z = {cz(z)} and w = {cz(w)}. Find the distance AB, to 3 significant figures.', s3(d),
                  f'AB = |z − w| = |{cz(z - w)}| (M1); √({sp.expand((z - w) * sp.conjugate(z - w))}) (A1); {s3(d)} (A1).', 3)
    if kind == 'mod':
        v = z * w
        m_ = sp.sqrt(sp.expand(v * sp.conjugate(v)))
        return mk(f'Let z = {cz(z)} and w = {cz(w)}. Find |zw| to 3 significant figures and verify that |zw| = |z||w|.', s3(m_),
                  f'zw = {cz(sp.expand(v))} (A1); |zw| = {s3(m_)} (A1); |z||w| = {s3(sp.sqrt(sp.expand(z * sp.conjugate(z))))} × {s3(sp.sqrt(sp.expand(w * sp.conjugate(w))))} = {s3(m_)} (R1).', 3)
    m_ = (z + w) / 2
    return mk(f'On an Argand diagram, P represents {cz(z)} and Q represents {cz(w)}. Find the complex number represented by the midpoint of PQ and its modulus, correct to 3 significant figures.',
              f'{cz(m_)}; {s3(sp.sqrt(sp.expand(m_ * sp.conjugate(m_))))}', f'(z + w)/2 (M1); {cz(m_)} (A1); modulus {s3(sp.sqrt(sp.expand(m_ * sp.conjugate(m_))))} (A1).', 3)


@R.add('ch04-st1', 'C2', (2, 4), 'explain')
def cx_explain(rng, slot):
    z = _rand_z(rng, -6, 6)
    kind = rng.choice(['zz', 'add'])
    a, b = sp.re(z), sp.im(z)
    if kind == 'zz':
        return mk(f'Show that z z* is real for z = {cz(z)}, and explain why this is true for every complex number.', str(a * a + b * b),
                  f'({cz(z)})({cz(sp.conjugate(z))}) = {a * a} + {b * b} = {a * a + b * b} (A1); in general (a + bi)(a − bi) = a² − b²i² = a² + b² (R1), which has no imaginary part (R1).', 3, 'explain')
    w = _rand_z(rng, -6, 6)
    return mk(f'On an Argand diagram, explain how the point representing z + w is found from the points representing z = {cz(z)} and w = {cz(w)}, and state z + w.', cz(z + w),
              f'z and w act like position vectors (R1); z + w is the fourth vertex of the parallelogram with sides 0z and 0w (R1); {cz(z + w)} (A1).', 3, 'explain')


@R.add('ch04-st1', 'C4', (3, 5), 'multi_step', style='ext')
def cx_parts(rng, slot):
    a, b = nz(rng, -4, 4), rng.randint(1, 5)
    z1 = a + b * I_
    p, q = -2 * a, a * a + b * b
    k = rng.randint(2, 4)
    w = sp.expand(k * I_ * z1)
    parts = [(f'Solve z² {"+" if p >= 0 else "−"} {abs(p)}z + {q} = 0.'.replace(' + 0z', ''), f'{cz(z1)}, {cz(sp.conjugate(z1))}', 'quadratic formula (M1) A1 A1', 3, True),
             ('Plot the two roots on an Argand diagram and describe the symmetry.', 'reflections of each other in the real axis', 'A1 R1', 2, True),
             (f'Let z₁ = {cz(z1)}. Find w = {k}iz₁ and show that |w| = {k}|z₁|.', f'w = {cz(w)}; |w| = {P(sp.sqrt(sp.expand(w * sp.conjugate(w))))}', 'A1 A1', 2, True),
             ('Describe the transformation that maps z₁ to w on the Argand diagram.', f'rotation of π/2 anticlockwise about 0 and enlargement scale factor {k}', 'A1 A1', 2, True),
             ('Find z₁/z₁* in the form a + bi.', cz(sp.radsimp(z1 / sp.conjugate(z1))), 'M1 A1', 2, False)]
    return build_parts(rng, ['This question is about complex numbers on an Argand diagram.', f'Consider the quadratic z² {"+" if p >= 0 else "−"} {abs(p)}z + {q}.'.replace(' + 0z', '')], parts, 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch04-st2', F(
    terms=[('modulus', '|z| = √(a² + b²), the distance of z from the origin on an Argand diagram'),
           ('argument', 'the angle θ = arg z from the positive real axis to the line joining 0 to z; the principal argument lies in −π < θ ≤ π'),
           ('modulus-argument (polar) form', 'writing z = r(cos θ + i sin θ) = r cis θ, where r = |z| and θ = arg z'),
           ('Euler form', 'writing z = re^(iθ), equivalent to r cis θ')],
    facts=[('|z₁z₂| =', '|z₁||z₂|', ['|z₁| + |z₂|', '|z₁|²|z₂|', '|z₁ + z₂|'], 'Moduli multiply.'),
           ('arg(z₁/z₂) =', 'arg z₁ − arg z₂', ['arg z₁ / arg z₂', 'arg z₁ + arg z₂', 'arg z₂ − arg z₁'], 'Arguments subtract (adjusted to the principal range).'),
           ('e^(iπ) =', '−1', ['1', 'i', '0'], 'cos π + i sin π.'),
           ('The principal argument of −2i is', '−π/2', ['π/2', '3π/2', 'π'], 'It lies on the negative imaginary axis.')],
    why=[('Explain why arg(z₁z₂) = arg z₁ + arg z₂.', 'Multiplying r₁ cis θ₁ by r₂ cis θ₂ and using the compound angle formulae gives r₁r₂ cis(θ₁ + θ₂), so the arguments add (possibly adjusted by 2π).'),
         ('Explain why arctan(b/a) does not always give arg(a + bi).', 'arctan gives values in (−π/2, π/2) only, so for points in the second or third quadrants π must be added or subtracted.'),
         ('Explain why multiplying by i rotates a point by π/2 about the origin.', 'i = cis(π/2) has modulus 1 and argument π/2, so multiplying adds π/2 to the argument without changing the modulus.')],
    misc=[('arg(−1 − i) = arctan(1) = π/4.', '−1 − i is in the third quadrant, so arg = −3π/4.'),
          ('2 cis(π/3) × 3 cis(π/6) = 5 cis(π/2).', 'The moduli multiply: 6 cis(π/2) = 6i.')],
))


def _std_z(rng):
    th = rng.choice(STD_ARG)
    r = rng.choice([1, 2, 3, 4, 2 * r2, 2 * r3, 6, sp.Rational(1, 2)])
    return r, th, sp.nsimplify(sp.expand(r * (sp.cos(th) + I_ * sp.sin(th))))


@R.add('ch04-st2', 'C1', (1, 3), 'mcq')
def modarg_mcq(rng, slot):
    r, th, z = _std_z(rng)
    if rng.random() < 0.5:
        wr = [ang(princ(th + pi)), ang(princ(-th)), ang(princ(pi / 2 - th))]
        wr = [w for w in dict.fromkeys(wr) if w != ang(th)]
        while len(wr) < 3:
            wr.append(ang(princ(th + pi / 2 * (len(wr) + 1))))
        return mcq(rng, f'The principal argument of {cz(z)} is', ang(th), wr[:3], 'Locate the quadrant, then use the reference angle.')
    return mcq(rng, f'{cis_txt(r, th)} in Cartesian form is', cz(z), [cz(sp.conjugate(z)), cz(-z), cz(I_ * z)], 'r cos θ + i r sin θ.')


@R.add('ch04-st2', 'C3', (1, 4), 'short', style='p1')
def modarg_convert(rng, slot):
    r, th, z = _std_z(rng)
    if rng.random() < 0.55:
        return mk(f'Write z = {cz(z)} in the form r cis θ and in the form re^(iθ), where r > 0 and −π < θ ≤ π.', f'{cis_txt(r, th)} = {cis_txt(r, th, True)}',
                  f'r = |z| = {P(r)} (A1); quadrant and reference angle (M1); θ = {ang(th)} (A1).', 3)
    return mk(f'Express {cis_txt(r, th, True)} in the form a + bi, where a, b ∈ ℝ, giving exact values.', cz(z),
              f'{P(r)}(cos({ang(th)}) + i sin({ang(th)})) (M1); exact values (A1); {cz(z)} (A1).'.replace('1(cos', '(cos'), 3)


@R.add('ch04-st2', 'C3', (2, 5), 'short', style='p1')
def modarg_ops(rng, slot):
    r1, t1 = rng.choice([2, 3, 4, 6, 8]), rng.choice(STD_ARG[:8])
    r2_, t2 = rng.choice([2, 3, 4, sp.Rational(1, 2)]), rng.choice(STD_ARG)
    kind = rng.choice(['prod', 'quot', 'mix'])
    if kind == 'prod':
        th = princ(t1 + t2)
        z = sp.nsimplify(sp.expand(r1 * r2_ * (sp.cos(th) + I_ * sp.sin(th))))
        if not nice_ang(th):
            return None
        return mk(f'Let z = {cis_txt(r1, t1)} and w = {cis_txt(r2_, t2)}. Find zw in the form r cis θ, −π < θ ≤ π, and hence in the form a + bi.', f'{cis_txt(r1 * r2_, th)} = {cz(z)}',
                  f'moduli multiply: {P(r1 * r2_)} (A1); arguments add: {ang(t1 + t2)}' + (f' → {ang(th)}' if th != sp.nsimplify(t1 + t2) else '') + f' (M1 A1); {cz(z)} (A1).', 4)
    if kind == 'quot':
        th = princ(t1 - t2)
        z = sp.nsimplify(sp.expand(sp.Rational(r1) / r2_ * (sp.cos(th) + I_ * sp.sin(th))))
        if not nice_ang(th):
            return None
        return mk(f'Let z = {cis_txt(r1, t1, True)} and w = {cis_txt(r2_, t2, True)}. Find z/w in the form re^(iθ), −π < θ ≤ π, and hence in the form a + bi.', f'{cis_txt(sp.Rational(r1) / r2_, th, True)} = {cz(z)}',
                  f'moduli divide: {P(sp.Rational(r1) / r2_)} (A1); arguments subtract (M1); θ = {ang(th)} (A1); {cz(z)} (A1).', 4)
    a, b = rng.choice([(1, 1), (1, r3), (r3, 1)])
    sa, sb = rng.choice([1, -1]), rng.choice([1, -1])
    u, v = sa * a + sb * b * I_, rng.choice([1 + I_, 1 - I_, r3 + I_, -1 + r3 * I_, I_])
    q = sp.radsimp(u / v)
    mq, aq = sp.sqrt(sp.nsimplify(sp.expand(q * sp.conjugate(q)))), sp.arg(q)
    return mk(f'Let u = {cz(u)} and v = {cz(v)}. By first writing u and v in modulus-argument form, find u/v in the form re^(iθ), −π < θ ≤ π.', cis_txt(sp.nsimplify(mq), sp.nsimplify(aq), True),
              f'u = {cis_txt(sp.sqrt(sp.expand(u * sp.conjugate(u))), sp.arg(u), True)} (A1); v = {cis_txt(sp.sqrt(sp.expand(v * sp.conjugate(v))), sp.arg(v), True)} (A1); divide moduli, subtract arguments (M1); {cis_txt(sp.nsimplify(mq), sp.nsimplify(aq), True)} (A1).', 4)


@R.add('ch04-st2', 'C3', (2, 4), 'short', style='p2')
def modarg_gdc(rng, slot):
    z = _rand_z(rng, -9, 9)
    a, b = sp.re(z), sp.im(z)
    if abs(a) == abs(b):
        return None
    m_ = math.hypot(int(a), int(b))
    th = math.atan2(int(b), int(a))
    q = 'first' if a > 0 and b > 0 else 'second' if a < 0 < b else 'third' if a < 0 and b < 0 else 'fourth'
    kind = rng.choice(['polar', 'power'])
    if kind == 'polar':
        return mk(f'Write z = {cz(z)} in the form re^(iθ), where −π < θ ≤ π. Give r and θ correct to 3 significant figures.', f'{s3(m_)}e^({s3(th)}i)',
                  f'r = √({a * a + b * b}) = {s3(m_)} (A1); z lies in the {q} quadrant (R1); θ = {s3(th)} (A1).', 3)
    n = rng.randint(3, 6)
    return mk(f'Let z = {cz(z)}. Find |z{sup(n)}| and arg(z{sup(n)}) with −π < arg ≤ π, giving your answers to 3 significant figures.', f'{s3(m_ ** n)}; {s3(math.remainder(n * th, 2 * math.pi))}',
              f'|z| = {s3(m_)}, arg z = {s3(th)} (A1); |zⁿ| = |z|ⁿ = {s3(m_ ** n)} (A1); arg = {n} × {s3(th)} adjusted by multiples of 2π: {s3(math.remainder(n * th, 2 * math.pi))} (M1 A1).', 4)


@R.add('ch04-st2', 'C2', (2, 4), 'explain')
def modarg_explain(rng, slot):
    a, b = rng.choice([(1, 1), (1, r3), (r3, 1), (2, 2), (1, 2), (3, 1)])
    sa, sb = rng.choice([(-1, 1), (-1, -1)])
    z = sa * a + sb * b * I_
    wrong = sp.atan(sp.nsimplify(b / a) * sa * sb)
    th = sp.arg(z)
    return mk(f'{who(rng)} says that arg({cz(z)}) = arctan({P(sp.nsimplify(sb * b / (sa * a)))}) = {P(sp.nsimplify(wrong))}. Explain the error and state the correct principal argument.',
              P(sp.nsimplify(th)) if sp.nsimplify(th).has(pi) and len(str(sp.nsimplify(th))) < 12 else P(th),
              f'{cz(z)} lies in the {"second" if sb > 0 else "third"} quadrant (R1); arctan gives an angle in the fourth/first quadrant (R1); correct value {P(th)} (A1).', 3, 'explain')


@R.add('ch04-st2', 'C4', (3, 5), 'multi_step', style='ext')
def modarg_parts(rng, slot):
    (u, tu), (v, tv) = rng.sample([(1 + r3 * I_, pi / 3), (1 + I_, pi / 4), (r3 + I_, pi / 6), (1 - I_, -pi / 4), (r3 - I_, -pi / 6), (-1 + I_, 3 * pi / 4)], 2)
    mu, mv = sp.sqrt(sp.expand(u * sp.conjugate(u))), sp.sqrt(sp.expand(v * sp.conjugate(v)))
    q = sp.expand(sp.radsimp(u / v))
    tq = sp.nsimplify(tu - tv)
    if abs(tq) > pi or tq in (0, pi / 2, -pi / 2, pi):
        return None
    cq = sp.radsimp(sp.re(q) / (mu / mv))
    parts = [(f'Write u = {cz(u)} and v = {cz(v)} in the form re^(iθ).', f'u = {cis_txt(mu, tu, True)}, v = {cis_txt(mv, tv, True)}', 'A1 A1 A1 A1', 4, True),
             ('Hence find u/v in the form re^(iθ).', cis_txt(mu / mv, tq, True), 'M1 A1', 2, True),
             ('Find u/v in the form a + bi by multiplying by the conjugate.', cz(q), 'M1 A1', 2, True),
             (f'Hence find the exact value of cos({ang(tq)}).', nice(cq), 'equate real parts (M1) A1', 2, True),
             (f'Find the smallest positive integer n for which (u/v)ⁿ is real.', str(next(n for n in range(1, 50) if sp.simplify(sp.sin(n * tq)) == 0)), 'n × arg is a multiple of π (M1) A1', 2, False)]
    return build_parts(rng, ['This question compares Cartesian and polar forms of complex numbers.', 'In this question give all answers exactly.'], parts, 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch04-st3', F(
    terms=[('conjugate root theorem', 'if a polynomial has real coefficients and a + bi is a root, then a − bi is also a root'),
           ("De Moivre's theorem", '[r(cos θ + i sin θ)]ⁿ = rⁿ(cos nθ + i sin nθ) for n ∈ ℤ (and in particular n ∈ ℤ⁺, proved by induction)'),
           ('quadratic factor from conjugate roots', '(z − (a + bi))(z − (a − bi)) = z² − 2az + a² + b², which has real coefficients')],
    facts=[('If 2 − 3i is a root of a real cubic, another root is', '2 + 3i', ['−2 + 3i', '3 − 2i', '−2 − 3i'], 'Conjugate root theorem.'),
           ('(cis θ)⁵ =', 'cis 5θ', ['5 cis θ', 'cis(θ⁵)', 'cis(θ + 5)'], "De Moivre's theorem."),
           ('A real quartic with roots 1 + i and 2i also has roots', '1 − i and −2i', ['−1 − i and −2i', '1 − i and 2', 'only 1 − i'], 'Each non-real root comes with its conjugate.'),
           ('(1 + i)⁸ =', '16', ['16i', '8', '−16'], '(√2)⁸ cis(2π) = 16.')],
    why=[('Explain why a cubic with real coefficients must have at least one real root.', 'Non-real roots occur in conjugate pairs, so the number of non-real roots is even; a cubic has three roots (with multiplicity), so at least one is real.'),
         ('Explain why the conjugate root theorem needs real coefficients.', 'Taking conjugates of p(a + bi) = 0 gives p*(a − bi) = 0; if the coefficients are real, p* = p so a − bi is a root. With complex coefficients this fails, e.g. z − i has only the root i.'),
         ("Explain why De Moivre's theorem makes high powers easy to compute.", 'In polar form the modulus is simply raised to the nth power and the argument multiplied by n, instead of expanding n brackets.')],
    misc=[('If 3 + i is a root of z³ − 7z² + 16z − 10 then −3 − i is also a root.', 'The conjugate 3 − i is the other root, not the negative.'),
          ('(2 cis θ)³ = 2 cis 3θ.', 'The modulus is also cubed: 8 cis 3θ.')],
))


def _cubic_txt(coefs, var='z'):
    e = sum(c * x ** k for k, c in enumerate(reversed(coefs)))
    return poly_txt(e).replace('x', var)


@R.add('ch04-st3', 'C1', (1, 3), 'mcq')
def conj_mcq(rng, slot):
    a, b = nz(rng, -5, 5), rng.randint(1, 5)
    kind = rng.choice(['quad', 'root'])
    if kind == 'quad':
        right = poly_txt(x ** 2 - 2 * a * x + a * a + b * b).replace('x', 'z')
        wr = [poly_txt(x ** 2 + 2 * a * x + a * a + b * b), poly_txt(x ** 2 - 2 * a * x + a * a - b * b), poly_txt(x ** 2 - a * x + a * a + b * b)]
        return mcq(rng, f'The quadratic factor with real coefficients having root {cz(a + b * I_)} is', right, [w.replace('x', 'z') for w in wr], 'z² − 2Re(z₀)z + |z₀|².')
    n = rng.choice([4, 6, 8, 12])
    v = sp.expand((1 + I_) ** n)
    return mcq(rng, f'(1 + i){sup(n)} =', cz(v), [cz(-v), cz(I_ * v), str(2 ** n)], f'(√2){sup(n)} cis({n}π/4).')


@R.add('ch04-st3', 'C3', (2, 5), 'short', style='p1')
def conj_roots(rng, slot):
    a, b = nz(rng, -4, 4), rng.randint(1, 4)
    r = nz(rng, -5, 5)
    qd = x ** 2 - 2 * a * x + a * a + b * b
    if rng.random() < 0.55:
        p_ = sp.expand((x - r) * qd)
        return mk(f'Given that {cz(a + b * I_)} is a root of the equation {poly_txt(p_).replace("x", "z")} = 0, find the other two roots.', f'{cz(a - b * I_)}, {r}',
                  f'conjugate {cz(a - b * I_)} is a root (A1); quadratic factor {poly_txt(qd).replace("x", "z")} (M1 A1); divide to get z {"−" if r > 0 else "+"} {abs(r)}, so z = {r} (A1).', 4)
    s_ = rng.randint(1, 3)
    other = x ** 2 + s_ * s_
    p_ = sp.expand(qd * other)
    return mk(f'Given that {cz(a + b * I_)} is a root of {poly_txt(p_).replace("x", "z")} = 0, find all the roots.', f'{cz(a + b * I_)}, {cz(a - b * I_)}, {cz(s_ * I_)}, {cz(-s_ * I_)}',
              f'conjugate is a root (A1); factor {poly_txt(qd).replace("x", "z")} (M1 A1); other factor {poly_txt(other).replace("x", "z")} (A1); ±{cz(s_ * I_)} (A1).', 5)


@R.add('ch04-st3', 'C3', (2, 5), 'short', style='p1')
def conj_coeffs(rng, slot):
    a, b = nz(rng, -3, 3), rng.randint(1, 4)
    r = nz(rng, -4, 4)
    qd = x ** 2 - 2 * a * x + a * a + b * b
    p_ = sp.Poly(sp.expand((x - r) * qd), x).all_coeffs()
    return mk(f'The equation z³ + pz² + qz + r = 0, where p, q, r ∈ ℝ, has roots {r} and {cz(a + b * I_)}. Find p, q and r.'.replace('r = 0, where p, q, r', 'c = 0, where p, q, c').replace('find p, q and r', 'find p, q and c').replace('Find p, q and r', 'Find p, q and c'),
              f'p = {P(p_[1])}, q = {P(p_[2])}, c = {P(p_[3])}', f'third root {cz(a - b * I_)} (A1); (z − {r})({poly_txt(qd).replace("x", "z")}) (M1); expand (M1); p = {P(p_[1])}, q = {P(p_[2])}, c = {P(p_[3])} (A1 A1).'.replace('− −', '+ '), 5)


@R.add('ch04-st3', 'C3', (2, 5), 'short', style='p1')
def demoivre_power(rng, slot):
    base, rr, th = rng.choice([(1 + r3 * I_, 2, pi / 3), (1 - I_, r2, -pi / 4), (r3 + I_, 2, pi / 6), (-1 + I_, r2, 3 * pi / 4), (-r3 + I_, 2, 5 * pi / 6), (1 + I_, r2, pi / 4), (-1 - r3 * I_, 2, -2 * pi / 3)])
    n = rng.randint(4, 12)
    v = sp.nsimplify(sp.expand(rr ** n * (sp.cos(n * th) + I_ * sp.sin(n * th))))
    return mk(f"Use De Moivre's theorem to find ({cz(base)}){sup(n)} in the form a + bi.", cz(v),
              f'{cz(base)} = {cis_txt(rr, th)} (A1); ({P(rr)}){sup(n)} cis({ang(n * th)}) (M1 A1); {cz(v)} (A1).', 4)


@R.add('ch04-st3', 'C3', (2, 4), 'short', style='p2')
def demoivre_gdc(rng, slot):
    a, b = rng.randint(1, 4), nz(rng, -4, 4)
    z = a + b * I_
    n = rng.randint(5, 9)
    v = sp.expand(z ** n)
    kind = rng.choice(['exact', 'polar'])
    if kind == 'exact':
        return mk(f'Let z = {cz(z)}. Find z{sup(n)} in the form a + bi, and verify your answer using |z{sup(n)}| = |z|{sup(n)}.', cz(v),
                  f'GDC or binomial expansion (M1); {cz(v)} (A1); |z|{sup(n)} = ({a * a + b * b})^({n}/2) = {s3(math.hypot(a, b) ** n)} = |{cz(v)}| (R1).', 3)
    m_, th = math.hypot(a, b), math.atan2(b, a)
    return mk(f'Let z = {cz(z)}. Use the polar form of z to find z{sup(n)} in the form re^(iθ), −π < θ ≤ π, giving r and θ to 3 significant figures.', f'{s3(m_ ** n)}e^({s3(math.remainder(n * th, 2 * math.pi))}i)',
              f'|z| = {s3(m_)}, arg z = {s3(th)} (A1); r = |z|{sup(n)} = {s3(m_ ** n)} (A1); θ = {n}arg z − 2kπ = {s3(math.remainder(n * th, 2 * math.pi))} (M1 A1).', 4)


@R.add('ch04-st3', 'C2', (2, 4), 'explain')
def conj_explain(rng, slot):
    a, b = nz(rng, -4, 4), rng.randint(1, 4)
    n = rng.choice([3, 5])
    return mk(f'A polynomial of degree {n} with real coefficients has roots {cz(a + b * I_)} and {cz(b * I_)}. Explain how many real roots it must have.', f'{n - 4}' if n == 5 else 'impossible: it would need 4 non-real roots',
              (f'conjugates {cz(a - b * I_)} and {cz(-b * I_)} are also roots (R1); 4 non-real roots of {n} (A1); remaining root must be real: exactly 1 real root (R1).' if n == 5 else
               f'conjugates {cz(a - b * I_)} and {cz(-b * I_)} are also roots (R1); this gives 4 roots but a cubic has only 3 (R1); so no such real cubic exists (A1).'), 3, 'explain')


@R.add('ch04-st3', 'C4', (3, 5), 'multi_step', style='ext')
def conj_parts(rng, slot):
    a, b = nz(rng, -3, 3), rng.randint(1, 3)
    r = nz(rng, -4, 4)
    qd = x ** 2 - 2 * a * x + a * a + b * b
    if a == r:
        return None
    p_ = sp.expand((x - r) * qd)
    pz = poly_txt(p_).replace('x', 'z')
    parts = [(f'Show that z = {r} is a root of p(z) = {pz}.', f'p({r}) = 0', 'substitution (M1) A1', 2, True),
             ('Hence factorise p(z) into a linear and a quadratic factor with real coefficients.', f'(z {"−" if r > 0 else "+"} {abs(r)})({poly_txt(qd).replace("x", "z")})', 'division (M1) A1', 2, True),
             ('Find all roots of p(z) = 0.', f'{r}, {cz(a + b * I_)}, {cz(a - b * I_)}', 'quadratic formula (M1) A1 A1', 3, True),
             ('The three roots are plotted on an Argand diagram. Find the area of the triangle they form.', P(sp.Rational(1, 2) * 2 * b * abs(a - r)), 'base 2b, height |a − r| (M1) A1', 2, True),
             ('Find the sum of the roots and verify it equals minus the coefficient of z².', str(r + 2 * a), 'A1', 1, False)]
    return build_parts(rng, ['This question is about a cubic polynomial with real coefficients.', f'Let p(z) = {pz}.'], parts, 4)


@R.add('ch04-st3', 'C4', (4, 5), 'multi_step', style='p3')
def demoivre_p3(rng, slot):
    th = rng.choice([pi / 12, pi / 8, pi / 6, pi / 4])
    ns = [n_ for n_ in (5, 6, 7, 8) if nice_ang(n_ * th)]
    if not ns:
        return None
    n = rng.choice(ns)
    parts = [("Prove by mathematical induction that (cos θ + i sin θ)ⁿ = cos nθ + i sin nθ for n ∈ ℤ⁺.", 'proof', 'basis (A1); assume for n = k (M1); multiply by cis θ and use compound angle identities (M1 A1); conclusion (R1)', 5, True),
             ('Show that the result also holds for n = −1.', '(cis θ)⁻¹ = cos θ − i sin θ = cis(−θ)', 'multiply by conjugate (M1) A1', 2, True),
             (f'Let z = cis({ang(th)}). Find z{sup(n)} in the form a + bi.', cz(sp.nsimplify(sp.cos(n * th) + I_ * sp.sin(n * th))), 'M1 A1', 2, True),
             (f'Find the smallest positive integer m for which z^m = 1.', str(next(m for m in range(1, 100) if sp.simplify(m * th / (2 * pi)).is_integer)), 'm × arg is a multiple of 2π (M1) A1', 2, True),
             ('Show that z + 1/z = 2cos θ and zⁿ + 1/zⁿ = 2cos nθ for z = cis θ.', 'proof', 'M1 A1 A1', 3, True),
             ('Generalise: describe the set of values zᵏ, k ∈ ℤ, on an Argand diagram.', f'the vertices of a regular polygon on the unit circle', 'R1 A1', 2, False)]
    return build_parts(rng, ["This question is about De Moivre's theorem.", 'In this question θ is a real number.'], parts, 5)


# ---------------------------------------------------------------------------------------------
R.facts('ch04-st4', F(
    terms=[('nth roots of a complex number', 'the n solutions of zⁿ = r cis θ: z = r^(1/n) cis((θ + 2kπ)/n), k = 0, 1, …, n − 1'),
           ('roots of unity', 'the n solutions of zⁿ = 1: cis(2kπ/n), k = 0, …, n − 1, forming a regular n-gon on the unit circle'),
           ('multiple-angle identity', 'an expression for cos nθ or sin nθ in powers of cos θ and sin θ, found by expanding (cos θ + i sin θ)ⁿ')],
    facts=[('The sum of the n nth roots of unity (n ≥ 2) is', '0', ['1', 'n', '−1'], 'They form a geometric series with ratio ω ≠ 1.'),
           ('The cube roots of 1 are 1, ω, ω² with ω =', 'cis(2π/3)', ['cis(π/3)', 'cis(π/6)', 'e^(iπ)'], 'Angles 2kπ/3.'),
           ('The roots of z⁴ = 16 have modulus', '2', ['4', '16', '1/2'], '16^(1/4).'),
           ('Using De Moivre, cos 2θ + i sin 2θ = (cos θ + i sin θ)² gives cos 2θ =', 'cos²θ − sin²θ', ['2 sin θ cos θ', 'cos²θ + sin²θ', '1 − cos²θ'], 'Real parts.')],
    why=[('Explain why the n nth roots of a complex number lie at the vertices of a regular n-gon.', 'They all have the same modulus r^(1/n), so they lie on a circle, and successive arguments differ by 2π/n, so they are equally spaced.'),
         ('Explain why zⁿ = w has exactly n distinct roots, not infinitely many.', 'Adding 2π to the argument of w gives a new root only up to k = n − 1; from k = n the arguments repeat after a full turn.'),
         ('Explain why the sum of the nth roots of unity is 0.', 'They are 1, ω, …, ωⁿ⁻¹ with ω ≠ 1, so their sum is (1 − ωⁿ)/(1 − ω) = 0 since ωⁿ = 1; equivalently they are the roots of zⁿ − 1, whose zⁿ⁻¹ coefficient is 0.')],
    misc=[('z³ = 8 has only the solution z = 2.', 'There are three cube roots: 2, 2cis(2π/3), 2cis(−2π/3).'),
          ('The square roots of 4 cis(π/3) are 2 cis(π/6) and 2 cis(π/3 + π).', 'The arguments are (π/3 + 2kπ)/2: π/6 and 7π/6 (or −5π/6).')],
))


@R.add('ch04-st4', 'C1', (1, 3), 'mcq')
def roots_mcq(rng, slot):
    n = rng.choice([3, 4, 5, 6, 8])
    r = rng.choice([1, 2, 3])
    kind = rng.choice(['mod', 'ang'])
    if kind == 'mod':
        w = r ** n
        return mcq(rng, f'The roots of z{sup(n)} = {w} each have modulus', str(r), [str(w), str(w // n) if w % n == 0 and w // n != r else str(r + 1), P(sp.Rational(1, r) if r > 1 else n)], f'{w}^(1/{n}).')
    return mcq(rng, f'The angle between successive roots of z{sup(n)} = {r ** n}i on an Argand diagram is', ang(2 * pi / n), [ang(pi / n), ang(2 * pi / (n + 1)), ang(pi / (2 * n))], f'2π/{n}.')


@R.add('ch04-st4', 'C3', (2, 5), 'short', style='p1')
def nth_roots(rng, slot):
    n = rng.choice([2, 3, 4, 3, 6])
    r = rng.choice([1, 2, 3]) if n != 6 else rng.choice([1, 2])
    th = rng.choice([0, pi, pi / 2, -pi / 2, pi / 3, 2 * pi / 3, pi / 4])
    w = sp.nsimplify(sp.expand(r ** n * (sp.cos(th) + I_ * sp.sin(th))))
    roots = [princ((th + 2 * k * pi) / n) for k in range(n)]
    roots = sorted(roots, key=lambda e: float(e))
    txt = ', '.join(cis_txt(r, a_, True) for a_ in roots)
    return mk(f'Solve z{sup(n)} = {cz(w)}, giving your answers in the form re^(iθ), r > 0, −π < θ ≤ π.', txt,
              f'{cz(w)} = {cis_txt(r ** n, th, True)} (A1); modulus {r} (A1); arguments ({ang(th)} + 2kπ)/{n} (M1); all {n} roots in range (A1 A1).', 5)


@R.add('ch04-st4', 'C3', (2, 5), 'short', style='p1')
def trig_identity(rng, slot):
    c_, s_ = sp.symbols('c s')
    n = rng.choice([2, 3, 4, 5])
    e = sp.expand((c_ + I_ * s_) ** n)
    re_, im_ = sp.re(e.subs({c_: sp.Symbol('c', real=True), s_: sp.Symbol('s', real=True)})), sp.im(e.subs({c_: sp.Symbol('c', real=True), s_: sp.Symbol('s', real=True)}))
    C, S = sp.Symbol('c', real=True), sp.Symbol('s', real=True)
    which = rng.choice(['cos', 'sin'])
    if which == 'cos':
        tgt = sp.expand(re_.subs(S ** 2, 1 - C ** 2).subs(S ** 4, (1 - C ** 2) ** 2))
        tgt = sp.expand(sp.expand(re_).subs(S, sp.sqrt(1 - C ** 2)))
        txt = poly_txt(tgt.subs(C, x)).replace('x', 'cos θ').replace('cos θ²', 'cos²θ').replace('cos θ³', 'cos³θ').replace('cos θ⁴', 'cos⁴θ').replace('cos θ⁵', 'cos⁵θ')
        return mk(f"Use De Moivre's theorem to express cos {n}θ in terms of cos θ.", f'cos {n}θ = {txt}',
                  f'(cos θ + i sin θ){sup(n)} = cos {n}θ + i sin {n}θ (M1); binomial expansion, real parts (M1 A1); replace sin²θ by 1 − cos²θ (M1); {txt} (A1).', 5)
    if n % 2 == 0:
        tgt = sp.expand(im_ / S)
        tgt = sp.expand(tgt.subs(S, sp.sqrt(1 - C ** 2)))
        txt = poly_txt(tgt.subs(C, x)).replace('x', 'cos θ').replace('cos θ²', 'cos²θ').replace('cos θ³', 'cos³θ')
        txt = f'sin θ({txt})' if ' ' in txt.replace('cos θ', 'C') else f'{txt} sin θ'
        return mk(f"Use De Moivre's theorem to show that sin {n}θ = sin θ × p(cos θ) for a polynomial p, and find p.", f'sin {n}θ = {txt}',
                  f'imaginary parts of (cos θ + i sin θ){sup(n)} (M1 A1); factor sin θ and replace sin²θ (M1); {txt} (A1).', 4)
    tgt = sp.expand(sp.expand(im_).subs(C, sp.sqrt(1 - S ** 2)))
    txt = poly_txt(tgt.subs(S, x)).replace('x', 'sin θ').replace('sin θ³', 'sin³θ').replace('sin θ⁵', 'sin⁵θ')
    return mk(f"Use De Moivre's theorem to express sin {n}θ in terms of sin θ.", f'sin {n}θ = {txt}',
              f'(cos θ + i sin θ){sup(n)} expanded (M1); imaginary parts (A1); replace cos²θ by 1 − sin²θ (M1); {txt} (A1).', 4)


@R.add('ch04-st4', 'C3', (2, 4), 'short', style='p2')
def roots_gdc(rng, slot):
    w = _rand_z(rng, -9, 9)
    n = rng.choice([3, 4, 5])
    m_, th = math.hypot(int(sp.re(w)), int(sp.im(w))), math.atan2(int(sp.im(w)), int(sp.re(w)))
    roots = sorted([math.remainder((th + 2 * k * math.pi) / n, 2 * math.pi) for k in range(n)])
    rr = m_ ** (1 / n)
    return mk(f'Find the {n} roots of z{sup(n)} = {cz(w)} in the form re^(iθ), −π < θ ≤ π, giving r and θ to 3 significant figures.', ', '.join(f'{s3(rr)}e^({s3(a_)}i)' for a_ in roots),
              f'|w| = {s3(m_)}, arg w = {s3(th)} (A1); r = {s3(m_)}^(1/{n}) = {s3(rr)} (A1); θ = (arg w + 2kπ)/{n} (M1); roots (A1 A1).', 5)


@R.add('ch04-st4', 'C2', (2, 4), 'explain')
def roots_explain(rng, slot):
    n = rng.choice([3, 4, 5, 6, 8])
    sm = '1 + ω + ω²' if n == 3 else '1 + ω + ω² + ω³' if n == 4 else f'1 + ω + ω² + … + ω{sup(n - 1)}'
    return mk(f'Explain why, if ω ≠ 1 is {"an" if n == 8 else "a"} {ordn(n)} root of unity, then {sm} = 0.', '0',
              f'geometric series with ratio ω ≠ 1 (R1); sum = (1 − ω{sup(n)})/(1 − ω) (M1); ω{sup(n)} = 1 so the sum is 0 (R1).', 3, 'explain')


@R.add('ch04-st4', 'C4', (3, 5), 'multi_step', style='ext')
def roots_parts(rng, slot):
    n = rng.choice([3, 4, 5, 6])
    r = rng.choice([1, 2, 3])
    w = r ** n
    roots = [cis_txt(r, princ(2 * k * pi / n), True) for k in range(n)]
    area = sp.nsimplify(sp.Rational(n, 2) * r * r * sp.sin(2 * pi / n))
    parts = [(f'Solve z{sup(n)} = {w}, giving the roots in the form re^(iθ), −π < θ ≤ π.', ', '.join(roots), 'modulus (A1); arguments 2kπ/n (M1); all roots (A1 A1)', 4, True),
             ('The roots are plotted on an Argand diagram. Describe the shape they form.', {3: 'an equilateral triangle', 4: 'a square', 5: 'a regular pentagon', 6: 'a regular hexagon'}[n] + ' centred at 0 with vertices on the circle |z| = ' + str(r), 'A1', 1, True),
             ('Find the exact area of this shape.', P(area), f'{n} triangles of area ½r²sin(2π/{n}) (M1) A1', 2, True),
             (f'Show that the sum of the roots is zero.', '0', 'geometric series / coefficient argument (M1 R1)', 2, True),
             (f'Hence, or otherwise, find the value of Σ from k = 0 to {n - 1} of cos(2kπ/{n}).', '0', 'real part of the sum (R1) A1', 2, False)]
    return build_parts(rng, ['This question is about the roots of a complex equation.', f'Consider the equation z{sup(n)} = {w}.'], parts, 4)


@R.add('ch04-st4', 'C4', (4, 5), 'multi_step', style='p3')
def roots_p3(rng, slot):
    k = rng.choice([3, 4, 5])
    parts = [('Let z = cis θ. Show that zⁿ − z⁻ⁿ = 2i sin nθ and zⁿ + z⁻ⁿ = 2cos nθ.', 'proof', 'M1 A1 A1', 3, True),
             (f'By expanding (z + z⁻¹){sup(k)}, express cos{sup(k)}θ in terms of cosines of multiples of θ.', {3: 'cos³θ = (cos 3θ + 3cos θ)/4', 4: 'cos⁴θ = (cos 4θ + 4cos 2θ + 3)/8', 5: 'cos⁵θ = (cos 5θ + 5cos 3θ + 10cos θ)/16'}[k], 'binomial expansion (M1); pair terms (M1); A1 A1', 4, True),
             (f'Hence find the exact value of ∫₀^(π/2) cos{sup(k)}θ dθ.', {3: '2/3', 4: '3π/16', 5: '8/15'}[k], 'integrate term by term (M1) A1', 2, True),
             ('Use the sum of the roots of z⁵ = 1 to show that cos(2π/5) + cos(4π/5) = −1/2.', 'proof', 'roots sum to 0 (M1); real parts, symmetric pairs (R1); AG', 3, True),
             ('Generalise: state Σ from k = 1 to n − 1 of cos(2kπ/n) for n ≥ 2.', '−1', 'R1 A1', 2, False)]
    return build_parts(rng, ['This question develops identities from complex numbers.', 'In this question z = cos θ + i sin θ.'], parts, 4)


# =============================================================================================
# ch05 Functions (SL 2.1–2.5)
# =============================================================================================
def gen_form(m, c):
    """ax + by + d = 0 with integer coefficients, a > 0"""
    m, c = sp.nsimplify(m), sp.nsimplify(c)
    den = sp.ilcm(sp.fraction(m)[1], sp.fraction(c)[1])
    a, b, d = m * den, -den, c * den
    if a < 0 or (a == 0 and b < 0):
        a, b, d = -a, -b, -d
    g = math.gcd(math.gcd(int(a), int(b)), int(d)) or 1
    a, b, d = a / g, b / g, d / g
    return poly_txt(a * x + b * y + d, x).replace(' ', ' ') if False else fixminus(P(sp.expand(a * x + b * y + d))) + ' = 0'


def _gf(a, b, d):
    e = a * x + b * y + d
    terms = []
    for coef, v in ((a, 'x'), (b, 'y'), (d, '')):
        if coef == 0:
            continue
        mag_ = abs(coef)
        tm = (str(mag_) if (mag_ != 1 or not v) else '') + v
        terms.append(('−' if coef < 0 else '+', tm))
    s_ = ('−' if terms[0][0] == '−' else '') + terms[0][1]
    for sg, tm in terms[1:]:
        s_ += f' {sg} {tm}'
    return s_ + ' = 0'


def genf(m, c):
    m, c = sp.nsimplify(m), sp.nsimplify(c)
    den = int(sp.ilcm(sp.fraction(m)[1], sp.fraction(c)[1]))
    a, b, d = int(m * den), -den, int(c * den)
    if a < 0 or (a == 0 and b > 0):
        a, b, d = -a, -b, -d
    g = math.gcd(math.gcd(a, b), d) or 1
    return _gf(a // g, b // g, d // g)


R.facts('ch05-st1', F(
    terms=[('gradient', 'the value m = (y₂ − y₁)/(x₂ − x₁), the change in y per unit increase in x along a line'),
           ('gradient–intercept form', 'the equation y = mx + c, where m is the gradient and c the y-intercept'),
           ('point–gradient form', 'the equation y − y₁ = m(x − x₁) for the line with gradient m through (x₁, y₁)'),
           ('general form of a line', 'the equation ax + by + d = 0 with a, b, d constants (often integers)')],
    facts=[('Parallel lines have gradients that are', 'equal', ['negative reciprocals', 'reciprocals', 'opposite in sign'], 'm₁ = m₂.'),
           ('A line perpendicular to one with gradient 2/3 has gradient', '−3/2', ['3/2', '−2/3', '2/3'], 'm₁m₂ = −1.'),
           ('The gradient of 3x + 4y − 12 = 0 is', '−3/4', ['3/4', '−4/3', '3'], 'y = −(3/4)x + 3.'),
           ('The x-intercept of y = 2x − 6 is', '3', ['−6', '6', '−3'], 'Set y = 0.')],
    why=[('Explain why the product of the gradients of perpendicular lines is −1.', 'Rotating a line through 90° maps a direction (1, m) to (−m, 1), whose gradient is −1/m; so m₁m₂ = −1 (for non-vertical lines).'),
         ('Explain why a vertical line has no gradient in the form y = mx + c.', 'Its x-change is 0, so (y₂ − y₁)/(x₂ − x₁) is undefined; it is written x = k.'),
         ('Explain how the gradient of a line can be interpreted in a real-life linear model.', 'It is the rate of change of the dependent variable per unit of the independent variable, e.g. cost per kilometre.')],
    misc=[('The gradient of 2x + 5y = 10 is 2.', 'Rearrange: y = −(2/5)x + 2, so the gradient is −2/5.'),
          ('Lines with gradients 3 and −3 are perpendicular.', 'Perpendicular gradients multiply to −1: 3 × (−1/3); 3 and −3 are not perpendicular.')],
))


@R.add('ch05-st1', 'C1', (1, 3), 'mcq')
def line_mcq(rng, slot):
    p, q = nz(rng, -6, 6), nz(rng, 1, 7)
    m = sp.Rational(p, q)
    if m in (1, -1):
        return None
    kind = rng.choice(['perp', 'par', 'grad'])
    if kind == 'perp':
        return mcq(rng, f'A line is perpendicular to y = {P(m * x)} + {rng.randint(1, 9)}. Its gradient is'.replace('+ −', '− '), P(-1 / m), [P(1 / m), P(-m), P(m)], 'm₁m₂ = −1.')
    if kind == 'par':
        c = nz(rng, -8, 8)
        return mcq(rng, f'Which line is parallel to {genf(m, c)}?', f'y = {P(m * x)} + {c + 3}'.replace('+ −', '− '), [f'y = {P(-m * x)} + {c}'.replace('+ −', '− '), f'y = {P(1 / m * x)} + {c}'.replace('+ −', '− '), f'y = {P(-1 / m * x)} + {c}'.replace('+ −', '− ')], 'Same gradient.')
    a, b = rng.randint(1, 6), nz(rng, -6, 6)
    return mcq(rng, f'The gradient of {_gf(a, b, nz(rng, -9, 9))} is', P(sp.Rational(-a, b)), [P(sp.Rational(a, b)), P(sp.Rational(-b, a)), P(sp.Rational(b, a))], 'Rearrange to y = mx + c.')


@R.add('ch05-st1', 'C3', (1, 4), 'short', style='p1')
def line_find(rng, slot):
    x1, y1 = nz(rng, -6, 6), nz(rng, -6, 6)
    kind = rng.choice(['two', 'perp', 'par', 'bisect'])
    if kind == 'two':
        x2, y2 = nz(rng, -6, 6), nz(rng, -6, 6)
        if x2 == x1:
            return None
        m = sp.Rational(y2 - y1, x2 - x1)
        c = y1 - m * x1
        return mk(f'Find the equation of the line through A({x1}, {y1}) and B({x2}, {y2}), giving your answer in the form ax + by + d = 0, where a, b, d ∈ ℤ.', genf(m, c),
                  f'gradient = {P(m)} (A1); y − {y1} = {P(m)}(x − {x1}) (M1); {genf(m, c)} (A1).'.replace('− −', '+ '), 3)
    a, b, d = rng.randint(1, 5), nz(rng, -5, 5), nz(rng, -9, 9)
    m0 = sp.Rational(-a, b)
    if kind == 'bisect':
        x2, y2 = x1 + 2 * nz(rng, -3, 3), y1 + 2 * nz(rng, -3, 3)
        mx, my = (x1 + x2) // 2, (y1 + y2) // 2
        m = -sp.Rational(x2 - x1, y2 - y1)
        c = my - m * mx
        return mk(f'Find the equation of the perpendicular bisector of the line segment joining P({x1}, {y1}) and Q({x2}, {y2}), in the form ax + by + d = 0.', genf(m, c),
                  f'midpoint ({mx}, {my}) (A1); gradient PQ = {P(sp.Rational(y2 - y1, x2 - x1))} so perpendicular gradient {P(m)} (M1 A1); {genf(m, c)} (A1).', 4)
    m = m0 if kind == 'par' else -1 / m0
    c = y1 - m * x1
    return mk(f'Find the equation of the line through ({x1}, {y1}) that is {"parallel" if kind == "par" else "perpendicular"} to {_gf(a, b, d)}. Give your answer in the form y = mx + c.', line_eq(m, c),
              f'gradient of given line {P(m0)} (A1); required gradient {P(m)} (M1); {line_eq(m, c)} (A1).', 3)


@R.add('ch05-st1', 'C3', (2, 4), 'short', style='p2')
def line_model(rng, slot):
    frames = [('A taxi charges a fixed fee plus a cost per kilometre. A {a}-km journey costs ${A} and a {b}-km journey costs ${B}.', 'cost per kilometre and fixed fee', 'km', '$'),
              ('The temperature of a liquid rises at a constant rate. After {a} minutes it is {A} °C and after {b} minutes it is {B} °C.', 'rate of temperature increase and initial temperature', 'minutes', '°C'),
              ('A phone plan charges a monthly fee plus a cost per GB of data. Using {a} GB costs €{A}; using {b} GB costs €{B}.', 'cost per GB and monthly fee', 'GB', '€')]
    fr, what, u, cu = rng.choice(frames)
    m = rng.choice([1.2, 1.5, 1.75, 2.4, 2.8, 3.5, 0.85])
    c = rng.choice([3.5, 4, 5.5, 12, 18, 20, 25])
    a, b = sorted(rng.sample(range(2, 30), 2))
    A, B = round(m * a + c, 2), round(m * b + c, 2)
    q = rng.randint(31, 60)
    return mk(fr.format(a=a, b=b, A=f'{A:.2f}', B=f'{B:.2f}') + f' Find the {what}, and hence predict the value for {q} {u}.', f'{m:g}; {c:g}; {round(m * q + c, 2):g}',
              f'gradient ({B:g} − {A:g})/({b} − {a}) = {m:g} (M1 A1); intercept {c:g} (A1); {m:g} × {q} + {c:g} = {round(m * q + c, 2):g} (A1).', 4)


@R.add('ch05-st1', 'C2', (2, 4), 'explain')
def line_explain(rng, slot):
    p, q = nz(rng, -5, 5), rng.randint(2, 6)
    m = sp.Rational(p, q)
    if abs(m) == 1:
        return None
    return mk(f'{who(rng)} says that a line perpendicular to y = {P(m * x)} + 1 has gradient {P(-m)}. Explain the mistake and give the correct gradient.', P(-1 / m),
              f'perpendicular gradients satisfy m₁m₂ = −1 (R1); {P(m)} × {P(-m)} ≠ −1 (R1); correct gradient {P(-1 / m)} (A1).', 3, 'explain')


@R.add('ch05-st1', 'C4', (3, 5), 'multi_step', style='ext')
def line_parts(rng, slot):
    A = (nz(rng, -5, 5), nz(rng, -5, 5))
    d1 = (rng.randint(1, 4), nz(rng, -4, 4))
    k = rng.randint(1, 3)
    B = (A[0] + d1[0] * k, A[1] + d1[1] * k)
    m = sp.Rational(d1[1], d1[0])
    mp = -1 / m
    s_ = rng.randint(1, 3)
    C = (B[0] - d1[1] * s_, B[1] + d1[0] * s_)
    c1 = A[1] - m * A[0]
    c2 = B[1] - mp * B[0]
    AB = sp.sqrt((B[0] - A[0]) ** 2 + (B[1] - A[1]) ** 2)
    BC = sp.sqrt((C[0] - B[0]) ** 2 + (C[1] - B[1]) ** 2)
    parts = [(f'Find the gradient of the line L₁ through A{A} and B{B}.', P(m), 'A1', 1, True),
             ('Find the equation of L₁ in the form y = mx + c.', line_eq(m, c1), 'M1 A1', 2, True),
             (f'L₂ is perpendicular to L₁ and passes through B. Find its equation.', line_eq(mp, c2), 'gradient (M1) A1', 2, True),
             (f'Show that C{C} lies on L₂.', 'substitution satisfies L₂', 'M1 AG', 1, True),
             ('Find the area of triangle ABC.', P(sp.nsimplify(AB * BC / 2)), 'right angle at B (R1); ½ × AB × BC (M1) A1', 3, True),
             ('Find the coordinates of the point D such that ABCD is a rectangle.', pt((A[0] + C[0] - B[0], A[1] + C[1] - B[1])), 'vector BA added to C (M1) A1', 2, False)]
    return build_parts(rng, ['This question is about straight lines in the plane.', 'Points A, B and C have integer coordinates.'], parts, 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch05-st2', F(
    terms=[('function', 'a relation in which each element of the domain is mapped to exactly one element of the range'),
           ('domain', 'the set of input values for which a function is defined'),
           ('range', 'the set of output values a function takes over its domain'),
           ('mapping notation', 'notation such as f: x ↦ 3x − 1, describing the rule that sends x to 3x − 1')],
    facts=[('The largest domain of f(x) = √(x − 3) is', 'x ≥ 3', ['x > 3', 'x ≥ 0', 'all real x'], 'Need x − 3 ≥ 0.'),
           ('The range of f(x) = x² + 4, x ∈ ℝ, is', 'f(x) ≥ 4', ['f(x) > 4', 'all real numbers', 'f(x) ≥ 0'], 'x² ≥ 0.'),
           ('The domain of f(x) = 1/(x + 2) is', 'x ≠ −2', ['x ≠ 2', 'x > −2', 'x ≠ 0'], 'Denominator non-zero.'),
           ('A graph represents a function if every vertical line meets it', 'at most once', ['exactly twice', 'at least once', 'never'], 'Vertical line test.')],
    why=[('Explain why the circle x² + y² = 9 is not the graph of a function of x.', 'For −3 < x < 3, a vertical line meets the circle twice, so one x-value maps to two y-values.'),
         ('Explain why the domain of ln(x − 2) is x > 2.', 'The logarithm is defined only for positive arguments, so x − 2 > 0.'),
         ('Explain why the range of a function depends on its domain.', 'The range is the set of outputs produced by the inputs in the domain; restricting the domain removes some outputs, e.g. x² on x ≥ 1 has range f(x) ≥ 1.')],
    misc=[('f(x) = 1/(x − 4) has domain x > 4.', 'Only x = 4 is excluded: domain x ∈ ℝ, x ≠ 4.'),
          ('The range of f(x) = 2x + 1, 0 ≤ x ≤ 3, is all real numbers.', 'With this domain, the range is 1 ≤ f(x) ≤ 7.')],
))


def _dom_fn(rng):
    a, b = nz(rng, -6, 6), rng.randint(1, 4)
    kind = rng.choice(['sqrt', 'recip', 'ln', 'sqrtneg', 'recip_sq', 'sqrt_quad'])
    if kind == 'sqrt':
        return f'√({poly_txt(b * x - a)})', f'x ≥ {P(sp.Rational(a, b))}', 'the expression under the root must be non-negative'
    if kind == 'sqrtneg':
        return f'√({poly_txt(a - b * x)})', f'x ≤ {P(sp.Rational(a, b))}', 'the expression under the root must be non-negative'
    if kind == 'recip':
        return f'{rng.randint(1, 9)}/({poly_txt(b * x - a)})', f'x ≠ {P(sp.Rational(a, b))}', 'the denominator cannot be zero'
    if kind == 'ln':
        return f'ln({poly_txt(b * x - a)})', f'x > {P(sp.Rational(a, b))}', 'the logarithm needs a positive argument'
    if kind == 'recip_sq':
        p = rng.randint(1, 6)
        return f'{rng.randint(1, 9)}/({poly_txt(x ** 2 - p * p)})', f'x ≠ ±{p}', 'the denominator cannot be zero'
    p = rng.randint(1, 6)
    return f'√({poly_txt(p * p - x ** 2)})', f'−{p} ≤ x ≤ {p}', 'the expression under the root must be non-negative'


@R.add('ch05-st2', 'C1', (1, 3), 'mcq')
def domain_mcq(rng, slot):
    f, d, why = _dom_fn(rng)
    alt = [d.replace('≥', '>'), d.replace('≥', '≤') if '≥' in d else d.replace('>', '<'), d.replace('x ≠', 'x =') if '≠' in d else 'all real x']
    alt = [a_ for a_ in dict.fromkeys(alt) if a_ != d]
    while len(alt) < 3:
        alt.append(['x ≥ 0', 'all real x', 'x > 0'][len(alt)])
    return mcq(rng, f'The largest possible domain of f(x) = {f} is', d, alt[:3], why[0].upper() + why[1:] + '.')


@R.add('ch05-st2', 'C3', (1, 4), 'short', style='p1')
def domain_range(rng, slot):
    kind = rng.choice(['dom', 'quad', 'lin', 'recip'])
    if kind == 'dom':
        f, d, why = _dom_fn(rng)
        return mk(f'Find the largest possible domain of f(x) = {f}.', d, f'{why} (R1); {d} (A1 A1).', 3)
    if kind == 'quad':
        a, h, k = rng.choice([1, 2, -1, -2, 3]), nz(rng, -5, 5), nz(rng, -9, 9)
        e = sp.expand(a * (x - h) ** 2 + k)
        lo = rng.choice([h - rng.randint(1, 3), None])
        if lo is None:
            rg = f'f(x) ≥ {k}' if a > 0 else f'f(x) ≤ {k}'
            return mk(f'Find the range of f(x) = {poly_txt(e)}, x ∈ ℝ.', rg, f'complete the square: {a if a not in (1, -1) else ("−" if a == -1 else "")}(x {"−" if h > 0 else "+"} {abs(h)})² {"+" if k >= 0 else "−"} {abs(k)} (M1 A1); vertex value {k} (A1); {rg} (A1).'.replace('−1(', '−('), 4)
        hi = h + rng.randint(1, 4)
        vals = [e.subs(x, lo), e.subs(x, hi), sp.Integer(k)]
        rg = f'{min(vals)} ≤ f(x) ≤ {max(vals)}'
        return mk(f'Find the range of f(x) = {poly_txt(e)} for {lo} ≤ x ≤ {hi}.', rg, f'vertex x = {h} lies in the domain (R1); f({lo}) = {vals[0]}, f({hi}) = {vals[1]}, f({h}) = {k} (A1 A1); {rg} (A1).', 4)
    if kind == 'lin':
        m, c = nz(rng, -5, 5), nz(rng, -9, 9)
        a, b = sorted(rng.sample(range(-6, 8), 2))
        v1, v2 = m * a + c, m * b + c
        rg = f'{min(v1, v2)} ≤ f(x) ≤ {max(v1, v2)}'
        return mk(f'The function f is defined by f(x) = {poly_txt(m * x + c)} for {a} ≤ x ≤ {b}. Find the range of f.', rg, f'linear, so extremes at endpoints (R1); f({a}) = {v1}, f({b}) = {v2} (A1); {rg} (A1).', 3)
    a, b, c = rng.randint(1, 9), nz(rng, -5, 5), nz(rng, -5, 5)
    return mk(f'For f(x) = {a}/(x {"−" if b > 0 else "+"} {abs(b)}) {"+" if c > 0 else "−"} {abs(c)}, state the largest possible domain and the range.', f'domain x ≠ {b}; range f(x) ≠ {c}',
              f'denominator zero at x = {b} (A1); {a}/(x − {b}) never equals 0 (R1); range f(x) ≠ {c} (A1).'.replace('− −', '+ '), 3)


@R.add('ch05-st2', 'C3', (2, 4), 'short', style='p2')
def fn_tech(rng, slot):
    kind = rng.choice(['cubic', 'exp', 'rational'])
    if kind == 'cubic':
        a, b, c = rng.choice([1, -1]), rng.randint(-4, 4), rng.randint(-9, 9)
        f = a * x ** 3 + b * x ** 2 - 5 * x + c
        lo, hi = -3, 3
    elif kind == 'exp':
        a, b = rng.choice([2, 3, 5]), rng.choice([0.5, 1, 1.5])
        f = a * sp.exp(-b * x) * x + rng.randint(1, 4)
        lo, hi = 0, 6
    else:
        a, b = rng.randint(2, 9), rng.randint(1, 5)
        f = a * x / (x ** 2 + b)
        lo, hi = -5, 5
    fl = sp.lambdify(x, f, 'math')
    xs_ = [lo + (hi - lo) * i / 6000 for i in range(6001)]
    vs = [fl(v) for v in xs_]
    mn, mx = min(vs), max(vs)
    return mk(f'Use your graphic display calculator to find the range of f(x) = {P(f)} for {lo} ≤ x ≤ {hi}, giving values to 3 significant figures.', f'{s3(mn)} ≤ f(x) ≤ {s3(mx)}',
              f'sketch on GDC over the domain (M1); least value {s3(mn)} (A1); greatest value {s3(mx)} (A1).', 3)


@R.add('ch05-st2', 'C2', (2, 4), 'explain')
def fn_explain(rng, slot):
    p = rng.randint(1, 6)
    kind = rng.choice(['rel', 'range'])
    if kind == 'rel':
        return mk(f'Explain whether the relation y² = x + {p} defines y as a function of x.', 'no',
                  f'for x > −{p} there are two values y = ±√(x + {p}) (R1); one input maps to two outputs (R1); not a function (A1).', 3, 'explain')
    return mk(f'{who(rng)} says the range of f(x) = x² − {p}, x ∈ ℝ, is f(x) ≥ 0 because squares are never negative. Explain the error and give the correct range.', f'f(x) ≥ −{p}',
              f'x² ≥ 0 so x² − {p} ≥ −{p} (R1); minimum at x = 0 (R1); f(x) ≥ −{p} (A1).', 3, 'explain')


@R.add('ch05-st2', 'C4', (3, 5), 'multi_step', style='ext')
def fn_parts(rng, slot):
    a, h, k = rng.choice([1, 2, -1]), nz(rng, -3, 3), nz(rng, -6, 6)
    e = sp.expand(a * (x - h) ** 2 + k)
    lo, hi = h - rng.randint(1, 3), h + rng.randint(2, 4)
    vals = [e.subs(x, lo), e.subs(x, hi), sp.Integer(k)]
    parts = [(f'Write f(x) = {poly_txt(e)} in the form a(x − h)² + k.', f'{a if a not in (1, -1) else ("−" if a == -1 else "")}(x {"−" if h > 0 else "+"} {abs(h)})² {"+" if k >= 0 else "−"} {abs(k)}', 'M1 A1', 2, True),
             ('State the coordinates of the vertex of the graph of f.', f'({h}, {k})', 'A1', 1, True),
             (f'The domain of f is {lo} ≤ x ≤ {hi}. Find the range of f.', f'{min(vals)} ≤ f(x) ≤ {max(vals)}', 'endpoints and vertex (M1) A1 A1', 3, True),
             (f'Find f({lo}) + f({hi}).', str(vals[0] + vals[1]), 'A1', 1, True),
             ('Explain why f has no inverse on this domain.', 'f is not one-to-one: it is not monotonic on the domain (the vertex is inside it)', 'R1', 1, True),
             (f'State the largest domain of the form x ≥ c on which f has an inverse.', f'x ≥ {h}', 'A1', 1, False)]
    return build_parts(rng, ['This question is about the domain and range of a quadratic function.', 'A function f is defined on a restricted domain.'], parts, 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch05-st3', F(
    terms=[('zero (root) of a function', 'a value of x for which f(x) = 0; an x-intercept of the graph'),
           ('local maximum / minimum', 'a point where the graph changes from increasing to decreasing (max) or decreasing to increasing (min)'),
           ('vertical asymptote', 'a line x = a which the graph approaches as f(x) → ±∞'),
           ('horizontal asymptote', 'a line y = b which the graph approaches as x → ±∞')],
    facts=[('The vertical asymptote of y = 3/(x − 5) is', 'x = 5', ['y = 5', 'x = −5', 'y = 3'], 'Denominator zero.'),
           ('The horizontal asymptote of y = 2 + 1/x is', 'y = 2', ['y = 0', 'x = 2', 'y = 1'], '1/x → 0.'),
           ('Solutions of f(x) = g(x) are the x-coordinates of', 'the intersection points of y = f(x) and y = g(x)', ['the zeros of f', 'the vertices of both graphs', 'the y-intercepts'], 'Equal y-values.'),
           ('The y-intercept of y = (x − 2)(x + 3) is', '−6', ['6', '2', '−3'], 'Set x = 0.')],
    why=[('Explain how to use a GDC to solve eˣ = 3 − x.', 'Graph y = eˣ and y = 3 − x (or y = eˣ + x − 3) and find the x-coordinate of the intersection (or zero).'),
         ('Explain why y = 1/(x − 2) has a vertical asymptote at x = 2.', 'As x → 2 the denominator → 0 while the numerator is 1, so |y| grows without bound.'),
         ('Explain why a quadratic can have at most two x-intercepts.', 'A polynomial of degree 2 has at most two roots, so the graph meets y = 0 at most twice.')],
    misc=[('y = (x + 1)/(x − 3) has a horizontal asymptote y = 0.', 'Numerator and denominator have equal degree, so the asymptote is y = 1.'),
          ('The graph of y = x² − 4 has a minimum at (−2, 0).', 'The minimum is at the vertex (0, −4); (±2, 0) are the zeros.')],
))


@R.add('ch05-st3', 'C1', (1, 3), 'mcq')
def asym_mcq(rng, slot):
    a, b, c, d = nz(rng, -6, 6), nz(rng, -6, 6), nz(rng, 1, 4), nz(rng, -6, 6)
    if a * d == b * c:
        return None
    va, ha = sp.Rational(-d, c), sp.Rational(a, c)
    fx = f'({poly_txt(a * x + b)})/({poly_txt(c * x + d)})'
    if rng.random() < 0.5:
        return mcq(rng, f'The vertical asymptote of y = {fx} is', f'x = {P(va)}', [f'x = {P(-va)}', f'y = {P(ha)}', f'x = {P(sp.Rational(-b, a))}' if sp.Rational(-b, a) != va else f'x = {P(va + 1)}'], 'Denominator zero.')
    return mcq(rng, f'The horizontal asymptote of y = {fx} is', f'y = {P(ha)}', [f'y = {P(sp.Rational(b, d))}' if sp.Rational(b, d) != ha else 'y = 0', f'x = {P(va)}', f'y = {P(-ha)}' if ha != 0 else 'y = 1'], 'Ratio of leading coefficients.')


@R.add('ch05-st3', 'C3', (2, 4), 'short', style='p2')
def features_gdc(rng, slot):
    kind = rng.choice(['inter', 'max', 'zeros', 'inter2'])
    if kind in ('inter', 'inter2'):
        pairs = [(sp.exp(x / 2), 5 - x), (sp.log(x + 2), 3 - x ** 2), (x ** 3 - 2 * x, sp.Integer(rng.randint(1, 3))), (2 ** x, x + 3), (sp.sqrt(x + 4), (x - 1) ** 2), (sp.exp(-x), x ** 2 - 2)]
        f, g = rng.choice(pairs)
        a_ = rng.randint(1, 3)
        f = f * a_ if kind == 'inter2' else f
        fl = sp.lambdify(x, f - g, 'math')
        lo = -1.99 if f.has(sp.log) else -3.99 if f.has(sp.sqrt) else -6
        try:
            roots = nsols(lambda v: fl(v), lo, 6)
        except (ValueError, ZeroDivisionError):
            return None
        if not roots:
            return None
        return mk(f'Use your GDC to find the x-coordinates of all points of intersection of y = {P(f)} and y = {P(g)}' + (' for x > −2' if f.has(sp.log) else '') + '.', lst3(roots) if False else ', '.join(s3(r_) for r_ in roots),
                  f'graph both functions (M1); intersections at x = {", ".join(s3(r_) for r_ in roots)} (A1 A1).', 3)
    if kind == 'max':
        a, b = rng.randint(2, 6), rng.choice([0.5, 1, 2])
        f = a * x * sp.exp(-b * x)
        xm = 1 / b
        return mk(f'Use your GDC to find the coordinates of the local maximum of y = {P(f)}.', f'({s3(xm)}, {s3(a / b / math.e)})', f'graph (M1); maximum at x = {s3(xm)} (A1); y = {s3(a / b / math.e)} (A1).', 3)
    c = [rng.randint(-4, 4) for _ in range(3)]
    f = x ** 3 + c[0] * x ** 2 + c[1] * x + c[2] - 0.5
    roots = nsols(sp.lambdify(x, f, 'math'), -10, 10)
    return mk(f'Use your GDC to find all the zeros of f(x) = {P(sp.nsimplify(f))}.', ', '.join(s3(r_) for r_ in roots), 'graph (M1); zeros (A1 A1).', 3)


@R.add('ch05-st3', 'C3', (1, 4), 'short', style='p1')
def features_exact(rng, slot):
    kind = rng.choice(['rational', 'quad', 'factored'])
    if kind == 'rational':
        a, b, c, d = nz(rng, -6, 6), nz(rng, -9, 9), nz(rng, 1, 3), nz(rng, -6, 6)
        if a * d == b * c:
            return None
        return mk(f'For y = ({poly_txt(a * x + b)})/({poly_txt(c * x + d)}), write down the equations of the asymptotes and the coordinates of the axis intercepts.',
                  f'x = {P(sp.Rational(-d, c))}, y = {P(sp.Rational(a, c))}; ({P(sp.Rational(-b, a))}, 0), (0, {P(sp.Rational(b, d))})',
                  'vertical asymptote (A1); horizontal asymptote (A1); x-intercept (A1); y-intercept (A1).', 4)
    if kind == 'quad':
        p, q = sorted(rng.sample(range(-6, 7), 2))
        a = rng.choice([1, -1, 2])
        e = sp.expand(a * (x - p) * (x - q))
        h = sp.Rational(p + q, 2)
        return mk(f'For the graph of y = {poly_txt(e)}, find the x-intercepts, the y-intercept and the coordinates of the vertex.', f'x = {p}, x = {q}; y = {e.subs(x, 0)}; vertex ({P(h)}, {P(e.subs(x, h))})',
                  f'factorise (M1); intercepts (A1 A1); vertex at x = {P(h)} midway between roots (M1); y = {P(e.subs(x, h))} (A1).', 5)
    r1, r2_, r3_ = sorted(rng.sample(range(-4, 5), 3))
    e = sp.expand((x - r1) * (x - r2_) * (x - r3_))
    return mk(f'The graph of y = {poly_txt(e)} crosses the x-axis at x = {r1}. Find the other x-intercepts and the y-intercept.', f'x = {r2_}, x = {r3_}; y = {e.subs(x, 0)}',
              f'divide by (x {"−" if r1 > 0 else "+"} {abs(r1)}) (M1); quadratic factor (A1); roots (A1); y-intercept {e.subs(x, 0)} (A1).'.replace('+ 0)', ')').replace('− 0)', ')'), 4)


@R.add('ch05-st3', 'C2', (2, 4), 'explain')
def features_explain(rng, slot):
    a, b = rng.randint(1, 6), nz(rng, -5, 5)
    return mk(f'Explain why the graph of y = {a}/(x {"−" if b > 0 else "+"} {abs(b)}) never crosses the line y = 0, and state the equation of its vertical asymptote.', f'x = {b}',
              f'{a}/(x − {b}) = 0 would need {a} = 0 (R1); so y = 0 is an asymptote, never reached (R1); x = {b} (A1).'.replace('− −', '+ '), 3, 'explain')


@R.add('ch05-st3', 'C4', (3, 5), 'multi_step', style='ext')
def features_parts(rng, slot):
    a, b = rng.randint(2, 9), rng.choice([1, 2, 3])
    k = rng.randint(1, 4)
    f = a * x / (x ** 2 + b * b)
    g = sp.Rational(k, 5) * x
    xm = b
    ym = sp.Rational(a, 2 * b)
    roots = nsols(sp.lambdify(x, f - g, 'math'), -10, 10)
    parts = [(f'Find the coordinates of the axis intercepts of y = f(x).', '(0, 0)', 'A1', 1, True),
             ('Write down the equation of the horizontal asymptote.', 'y = 0', 'A1', 1, True),
             ('Use your GDC to find the coordinates of the local maximum and local minimum.', f'max ({xm}, {P(ym)}), min ({-xm}, {P(-ym)})', 'A1 A1', 2, True),
             ('Hence write down the range of f.', f'{P(-ym)} ≤ f(x) ≤ {P(ym)}', 'A1', 1, True),
             (f'Find the x-coordinates of the points where y = f(x) meets y = {P(g)}.', ', '.join(s3(r_) for r_ in roots), 'GDC (M1) A1 A1', 3, True),
             ('Explain why f(x) = c has exactly two solutions for 0 < c < ' + P(ym) + '.', 'the line y = c meets the curve twice, between the asymptote and the maximum', 'R1', 1, False)]
    return build_parts(rng, [f'Let f(x) = {P(f)}, x ∈ ℝ.', f'Consider the function f(x) = {P(f)}.'], parts, 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch05-st4', F(
    terms=[('composite function', '(f ∘ g)(x) = f(g(x)): apply g first, then f'),
           ('inverse function', 'the function f⁻¹ that reverses f: f(f⁻¹(x)) = f⁻¹(f(x)) = x'),
           ('one-to-one function', 'a function for which each output comes from exactly one input; only such functions have inverses'),
           ('identity function', 'the function x ↦ x')],
    facts=[('The graph of y = f⁻¹(x) is the reflection of y = f(x) in', 'the line y = x', ['the x-axis', 'the y-axis', 'the line y = −x'], 'Swap x and y.'),
           ('If f(x) = 2x + 1 and g(x) = x², then f(g(3)) =', '19', ['49', '13', '10'], 'g(3) = 9, f(9) = 19.'),
           ('The domain of f⁻¹ is', 'the range of f', ['the domain of f', 'all real numbers', 'the range of f⁻¹'], 'Inputs and outputs swap.'),
           ('If f(x) = (x − 4)/3, then f⁻¹(x) =', '3x + 4', ['3x − 4', '(x + 4)/3', '1/(3x − 4)'], 'Swap and rearrange.')],
    why=[('Explain why f(x) = x², x ∈ ℝ, has no inverse function.', 'It is not one-to-one: f(2) = f(−2) = 4, so the inverse would map 4 to two values.'),
         ('Explain why, in general, f(g(x)) ≠ g(f(x)).', 'The order matters: f ∘ g applies g first. For example, with f(x) = x + 1 and g(x) = 2x, f(g(x)) = 2x + 1 but g(f(x)) = 2x + 2.'),
         ('Explain why a function and its inverse meet only on the line y = x when f is increasing.', 'If f is increasing, f(a) = b and f(b) = a with a ≠ b is impossible (a < b ⇒ f(a) < f(b) i.e. b < a), so any intersection has a = b.')],
    misc=[('f⁻¹(x) = 1/f(x).', 'f⁻¹ is the inverse function, not the reciprocal; e.g. f(x) = 2x gives f⁻¹(x) = x/2, not 1/(2x).'),
          ('(f ∘ g)(x) means f(x) × g(x).', 'It means f(g(x)), the composition.')],
))


def _lin_f(rng):
    a, b = nz(rng, -5, 5, (0, 1)), nz(rng, -9, 9)
    return a * x + b


@R.add('ch05-st4', 'C1', (1, 3), 'mcq')
def comp_mcq(rng, slot):
    f, g = _lin_f(rng), x ** 2 + nz(rng, -5, 5)
    v = nz(rng, -4, 4)
    fg, gf = f.subs(x, g.subs(x, v)), g.subs(x, f.subs(x, v))
    if fg == gf:
        return None
    return mcq(rng, f'f(x) = {poly_txt(f)} and g(x) = {poly_txt(g)}. (f ∘ g)({v}) =', str(fg), [str(gf), str(f.subs(x, v) * g.subs(x, v)), str(f.subs(x, v) + g.subs(x, v))], 'Apply g first.')


@R.add('ch05-st4', 'C3', (1, 4), 'short', style='p1')
def inverse_find(rng, slot):
    kind = rng.choice(['lin', 'rat', 'root', 'quad', 'exp'])
    y_ = sp.Symbol('y')
    if kind == 'lin':
        a, b, c = nz(rng, -6, 6, (0, 1)), nz(rng, -9, 9), rng.randint(2, 5)
        f = (a * x + b) / c
        inv = sp.solve(sp.Eq(f.subs(x, y_), x), y_)[0]
        return mk(f'Let f(x) = ({poly_txt(a * x + b)})/{c}. Find f⁻¹(x).', f'f⁻¹(x) = {P(sp.factor(inv))}', f'swap x and y (M1); rearrange (M1); {P(sp.factor(inv))} (A1).', 3)
    if kind == 'rat':
        a, b, c, d = nz(rng, -5, 5), nz(rng, -6, 6), 1, nz(rng, -6, 6)
        if a * d == b * c:
            return None
        f = (a * x + b) / (x + d)
        inv = sp.solve(sp.Eq(f.subs(x, y_), x), y_)[0]
        it = f'({poly_txt(sp.fraction(sp.together(inv))[0])})/({poly_txt(sp.fraction(sp.together(inv))[1])})'
        return mk(f'Let f(x) = ({poly_txt(a * x + b)})/({poly_txt(x + d)}), x ≠ {-d}. Find f⁻¹(x), stating its domain.', f'f⁻¹(x) = {it}, x ≠ {a}',
                  f'x(y + {d}) = {a}y + {b} (M1); collect y terms (M1); {it} (A1); x ≠ {a} (A1).'.replace('+ −', '− '), 4)
    if kind == 'root':
        a, b = rng.randint(1, 5), nz(rng, -6, 6)
        return mk(f'Let f(x) = √({poly_txt(a * x + b)}) for x ≥ {P(sp.Rational(-b, a))}. Find f⁻¹(x) and state its domain.', f'f⁻¹(x) = {P(sp.expand((x ** 2 - b) / a))}, x ≥ 0' if a == 1 else f'f⁻¹(x) = ({poly_txt(x ** 2 - b)})/{a}, x ≥ 0',
                  'x = √(ay + b) (M1); x² = ay + b (A1); rearrange (A1); domain is the range of f: x ≥ 0 (A1).', 4)
    if kind == 'quad':
        h, k = nz(rng, -5, 5), nz(rng, -9, 9)
        return mk(f'Let f(x) = (x {"−" if h > 0 else "+"} {abs(h)})² {"+" if k > 0 else "−"} {abs(k)} for x ≥ {h}. Find f⁻¹(x) and state its domain.', f'f⁻¹(x) = {h} + √(x {"−" if k > 0 else "+"} {abs(k)}), x ≥ {k}'.replace('−5 + √', '−5 + √'),
                  f'swap (M1); x {"−" if k > 0 else "+"} {abs(k)} = (y − {h})² (A1); positive root since y ≥ {h} (R1); domain x ≥ {k} (A1).'.replace('− −', '+ '), 4)
    a, b = rng.choice([2, 3, 5, 'e']), rng.randint(1, 5)
    if a == 'e':
        return mk(f'Let f(x) = e^(x) + {b}. Find f⁻¹(x) and state its domain.'.replace('e^(x)', 'eˣ'), f'f⁻¹(x) = ln(x − {b}), x > {b}', f'x − {b} = eʸ (M1); y = ln(x − {b}) (A1); x > {b} (A1).', 3)
    return mk(f'Let f(x) = {a}^(x − {b}). Find f⁻¹(x) and state its domain.', f'f⁻¹(x) = {b} + log{sub(a)} x, x > 0', f'take logs base {a} (M1); y − {b} = log{sub(a)} x (A1); x > 0 (A1).', 3)


@R.add('ch05-st4', 'C3', (2, 5), 'short', style='p1')
def composite_find(rng, slot):
    f, g = _lin_f(rng), rng.choice([x ** 2 + nz(rng, -5, 5), 1 / (x + nz(rng, -4, 4)), sp.sqrt(x + rng.randint(1, 6))])
    kind = rng.choice(['fg', 'gf', 'solve', 'ff'])
    if kind == 'fg':
        return mk(f'Let f(x) = {poly_txt(f)} and g(x) = {P(g)}. Find (f ∘ g)(x).', P(sp.expand(f.subs(x, g))) if not g.has(sp.sqrt) else P(f.subs(x, g)), 'substitute g(x) into f (M1); simplify (A1).', 2)
    if kind == 'gf':
        return mk(f'Let f(x) = {poly_txt(f)} and g(x) = {P(g)}. Find (g ∘ f)(x).', P(g.subs(x, f)) if not g.is_polynomial(x) else P(sp.expand(g.subs(x, f))), 'substitute f(x) into g (M1); simplify (A1).', 2)
    if kind == 'ff':
        return mk(f'Let f(x) = {poly_txt(f)}. Find (f ∘ f)(x) and solve (f ∘ f)(x) = x.', f'{poly_txt(sp.expand(f.subs(x, f)))}; x = {P(sp.solve(sp.expand(f.subs(x, f)) - x, x)[0])}',
                  f'f(f(x)) (M1); {poly_txt(sp.expand(f.subs(x, f)))} (A1); solve (A1).', 3)
    if not g.is_polynomial(x):
        return None
    c = rng.randint(1, 40)
    eq = sp.expand(f.subs(x, g)) - c
    sols = sp.solve(eq, x)
    sols = [s_ for s_ in sols if s_.is_real]
    if not sols:
        return None
    return mk(f'Let f(x) = {poly_txt(f)} and g(x) = {poly_txt(g)}. Solve (f ∘ g)(x) = {c}.', 'x = ' + ', '.join(P(s_) for s_ in sorted(sols, key=float)),
              f'(f ∘ g)(x) = {poly_txt(sp.expand(f.subs(x, g)))} (M1 A1); solve for x (M1); {", ".join(P(s_) for s_ in sorted(sols, key=float))} (A1).', 4)


@R.add('ch05-st4', 'C3', (2, 4), 'short', style='p2')
def inverse_gdc(rng, slot):
    a, b = rng.randint(2, 5), rng.randint(1, 4)
    kind = rng.choice(['val', 'meet'])
    f = a * sp.exp(x / b) - rng.randint(1, 3) if kind == 'val' else x ** 3 + a * x + b
    if kind == 'val':
        v = rng.randint(4, 30)
        xv = float(sp.solve(sp.Eq(f, v), x)[0])
        return mk(f'Let f(x) = {P(f)}. Find f⁻¹({v}) correct to 3 significant figures.', s3(xv), f'f⁻¹({v}) is the solution of f(x) = {v} (M1); GDC/logarithms (M1); {s3(xv)} (A1).', 3)
    v = rng.randint(5, 40)
    roots = nsols(sp.lambdify(x, f - v, 'math'), -10, 10)
    return mk(f'The function f(x) = {poly_txt(f)} is one-to-one. Find f⁻¹({v}), correct to 3 significant figures.', s3(roots[0]), f'solve {poly_txt(f)} = {v} (M1); GDC (M1); {s3(roots[0])} (A1).', 3)


@R.add('ch05-st4', 'C2', (2, 4), 'explain')
def inverse_explain(rng, slot):
    a, b = rng.randint(2, 6), nz(rng, -6, 6)
    return mk(f'{who(rng)} says that if f(x) = {a}x {"+" if b > 0 else "−"} {abs(b)} then f⁻¹(x) = 1/({a}x {"+" if b > 0 else "−"} {abs(b)}). Explain the error and find f⁻¹(x).', f'f⁻¹(x) = {P((x - b) / a)}' if False else f'f⁻¹(x) = (x {"−" if b > 0 else "+"} {abs(b)})/{a}',
              f'f⁻¹ reverses f; it is not the reciprocal (R1); check: f(1/({a}x + {b})) ≠ x (R1); (x − {b})/{a} (A1).'.replace('+ −', '− ').replace('− −', '+ '), 3, 'explain')


@R.add('ch05-st4', 'C4', (3, 5), 'multi_step', style='ext')
def inverse_parts(rng, slot):
    a, b = rng.randint(1, 4), nz(rng, -5, 5)
    c = rng.randint(1, 5)
    f = (a * x + b)
    g = x ** 2 + c
    v = rng.randint(1, 4)
    fg = sp.expand(f.subs(x, g))
    parts = [(f'Find (f ∘ g)({v}).', str(fg.subs(x, v)), 'A1', 1, True),
             ('Find (f ∘ g)(x) and (g ∘ f)(x).', f'{poly_txt(fg)}; {poly_txt(sp.expand(g.subs(x, f)))}', 'A1 A1', 2, True),
             (f'Find f⁻¹(x).', f'{P((x - b) / a)}' if a > 1 else poly_txt(x - b), 'M1 A1', 2, True),
             (f'Let h(x) = g(x) for x ≥ 0. Find h⁻¹(x) and state its domain and range.', f'√(x − {c}); x ≥ {c}; h⁻¹(x) ≥ 0', 'M1 A1 A1 A1', 4, True),
             (f'Solve (f ∘ g)(x) = (g ∘ f)(x).', 'x = ' + ', '.join(P(s_) for s_ in sorted([s_ for s_ in sp.solve(fg - sp.expand(g.subs(x, f)), x) if s_.is_real], key=float)) if [s_ for s_ in sp.solve(fg - sp.expand(g.subs(x, f)), x) if s_.is_real] else 'no real solutions', 'M1 A1', 2, False)]
    return build_parts(rng, [f'Let f(x) = {poly_txt(f)} and g(x) = {poly_txt(g)}, x ∈ ℝ.', f'The functions f and g are defined by f(x) = {poly_txt(f)} and g(x) = {poly_txt(g)}.'], parts, 4)


@R.add('ch05-st4', 'C4', (4, 5), 'multi_step', style='p3')
def selfinv_p3(rng, slot):
    a, k = nz(rng, -5, 5), rng.randint(1, 9)
    f = (a * x + k) / (x - a)
    parts = [(f'Let f(x) = ({poly_txt(a * x + k)})/(x {"−" if a > 0 else "+"} {abs(a)}), x ≠ {a}. Find (f ∘ f)(x) and simplify.', 'x', 'substitute (M1); simplify numerator and denominator (A1 A1)', 3, True),
             ('Hence state f⁻¹(x).', 'f⁻¹(x) = f(x)', 'R1', 1, True),
             ('Describe the symmetry of the graph of y = f(x) that this implies.', 'the graph is symmetric about the line y = x', 'R1', 1, True),
             ('Show that every function g(x) = (px + q)/(x − p), with p² + q ≠ 0, is self-inverse.', 'proof', 'M1 A1 A1 R1', 4, True),
             ('Find the conditions on b, c, d for g(x) = (x + b)/(cx + d) with c ≠ 0 to be self-inverse.', 'd = −1, with bc ≠ −1 so that g is not constant', 'compose (M1); compare coefficients (M1 A1)', 3, False),
             ('Find all linear functions h(x) = mx + n that are self-inverse.', 'h(x) = x, or h(x) = −x + n for any n', 'M1 A1 A1', 3, True)]
    return build_parts(rng, ['This question explores self-inverse functions.', 'A function f is called self-inverse if f ∘ f is the identity.'], parts, 5)


# =============================================================================================
# ch06 Quadratic functions (SL 2.6–2.7)
# =============================================================================================
def vform(a, h, k):
    at = '' if a == 1 else '−' if a == -1 else P(a)
    return f'{at}(x {"−" if h > 0 else "+"} {P(abs(h))})² {"+" if k >= 0 else "−"} {P(abs(k))}'.replace('(x + 0)', 'x').replace(' + 0', '') if True else ''


def fform(a, p, q):
    at = '' if a == 1 else '−' if a == -1 else P(a)
    fac = lambda r: f'(x {"−" if r > 0 else "+"} {P(abs(r))})'
    if p == q:
        return at + (fac(p) + '²' if p != 0 else 'x²')
    if p == 0:
        return at + 'x' + fac(q)
    if q == 0:
        return at + 'x' + fac(p)
    return at + fac(p) + fac(q)


R.facts('ch06-st1', F(
    terms=[('vertex form of a quadratic', 'the form f(x) = a(x − h)² + k, where (h, k) is the vertex'),
           ('intercept (factorised) form', 'the form f(x) = a(x − p)(x − q), where p and q are the x-intercepts'),
           ('axis of symmetry', 'the vertical line x = −b/(2a) through the vertex of the parabola y = ax² + bx + c'),
           ('completing the square', 'rewriting ax² + bx + c as a(x + b/(2a))² + c − b²/(4a)')],
    facts=[('The vertex of y = 2(x − 3)² + 5 is', '(3, 5)', ['(−3, 5)', '(3, −5)', '(2, 5)'], 'Read h and k.'),
           ('The axis of symmetry of y = x² − 8x + 1 is', 'x = 4', ['x = −4', 'x = 8', 'y = 4'], 'x = −b/(2a).'),
           ('The parabola y = −3x² + x + 2 opens', 'downwards', ['upwards', 'to the left', 'to the right'], 'a < 0.'),
           ('The y-intercept of y = 2(x + 1)(x − 4) is', '−8', ['8', '−4', '1'], 'Set x = 0.')],
    why=[('Explain why the axis of symmetry of y = a(x − p)(x − q) is x = (p + q)/2.', 'The parabola is symmetric about the vertical line through its vertex, and the two roots p and q are equidistant from it, so the axis is at their midpoint.'),
         ('Explain how the sign of a determines the shape of y = ax² + bx + c.', 'For large |x| the ax² term dominates: if a > 0 then y → +∞ and the parabola opens upwards (minimum vertex); if a < 0 it opens downwards (maximum).'),
         ('Explain why completing the square gives the vertex directly.', 'In a(x − h)² + k the squared term is 0 only at x = h and otherwise has the sign of a, so k is the minimum (a > 0) or maximum (a < 0) value, attained at x = h.')],
    misc=[('The vertex of y = (x + 2)² − 7 is (2, −7).', 'x + 2 = x − (−2), so the vertex is (−2, −7).'),
          ('x² + 6x + 1 = (x + 6)² − 35.', 'Halve the coefficient of x: (x + 3)² − 9 + 1 = (x + 3)² − 8.')],
))


@R.add('ch06-st1', 'C1', (1, 3), 'mcq')
def quad_form_mcq(rng, slot):
    a, h, k = rng.choice([1, 2, -1, 3, -2]), nz(rng, -6, 6), nz(rng, -9, 9)
    kind = rng.choice(['vertex', 'axis'])
    if kind == 'vertex':
        return mcq(rng, f'The vertex of y = {vform(a, h, k)} is', f'({h}, {k})', [f'({-h}, {k})', f'({h}, {-k})', f'({-h}, {-k})'], 'a(x − h)² + k has vertex (h, k).')
    e = sp.expand(a * (x - h) ** 2 + k)
    b = e.coeff(x, 1)
    return mcq(rng, f'The axis of symmetry of y = {poly_txt(e)} is', f'x = {h}', [f'x = {-h}', f'x = {P(b)}', f'y = {k}'], 'x = −b/(2a).')


@R.add('ch06-st1', 'C3', (1, 4), 'short', style='p1')
def complete_square(rng, slot):
    a = rng.choice([1, 1, 2, -1, 3, -2]) if slot.d >= 2 else 1
    h = sp.Rational(nz(rng, -7, 7), rng.choice([1, 1, 2])) if a == 1 else nz(rng, -5, 5)
    k = sp.Rational(nz(rng, -15, 15), 4 if h.q == 2 else 1) if hasattr(h, 'q') else nz(rng, -12, 12)
    e = sp.expand(a * (x - h) ** 2 + k)
    if not all(c.is_integer for c in sp.Poly(e, x).all_coeffs()):
        return None
    return mk(f'Write {poly_txt(e)} in the form a(x − h)² + k, and hence state the coordinates of the vertex of y = {poly_txt(e)}.', f'{vform(a, h, k)}; vertex ({P(h)}, {P(k)})',
              f'{"factor " + P(a) + " from the x terms (M1); " if a != 1 else ""}half the coefficient of x (M1); {vform(a, h, k)} (A1); vertex ({P(h)}, {P(k)}) (A1).', 3 if a == 1 else 4)


@R.add('ch06-st1', 'C3', (2, 5), 'short', style='p1')
def quad_from_info(rng, slot):
    kind = rng.choice(['vertex_pt', 'roots_pt', 'convert'])
    a = rng.choice([1, 2, -1, 3, -2, sp.Rational(1, 2)])
    if kind == 'vertex_pt':
        h, k = nz(rng, -5, 5), nz(rng, -8, 8)
        x0 = h + nz(rng, -3, 3)
        y0 = a * (x0 - h) ** 2 + k
        return mk(f'A parabola has vertex ({h}, {k}) and passes through ({x0}, {P(y0)}). Find its equation in the form y = ax² + bx + c.', f'y = {poly_txt(sp.expand(a * (x - h) ** 2 + k))}',
                  f'y = a(x − {h})² + {k} (M1); substitute ({x0}, {P(y0)}): a = {P(a)} (A1); expand (M1); {poly_txt(sp.expand(a * (x - h) ** 2 + k))} (A1).'.replace('− −', '+ ').replace('+ −', '− '), 4)
    if kind == 'roots_pt':
        p, q = sorted(rng.sample(range(-6, 7), 2))
        x0 = rng.choice([v for v in range(-6, 7) if v not in (p, q)])
        y0 = a * (x0 - p) * (x0 - q)
        e = sp.expand(a * (x - p) * (x - q))
        return mk(f'A parabola crosses the x-axis at x = {p} and x = {q} and passes through ({x0}, {P(y0)}). Find its equation in the form y = ax² + bx + c, and the coordinates of its vertex.',
                  f'y = {poly_txt(e)}; vertex ({P(sp.Rational(p + q, 2))}, {P(e.subs(x, sp.Rational(p + q, 2)))})',
                  f'y = a(x − {p})(x − {q}) (M1); a = {P(a)} (A1); expand (A1); vertex at x = {P(sp.Rational(p + q, 2))} (M1) (A1).'.replace('− −', '+ '), 5)
    p, q = sorted(rng.sample(range(-6, 7), 2))
    a = rng.choice([1, 2, -1, -3])
    e = sp.expand(a * (x - p) * (x - q))
    h = sp.Rational(p + q, 2)
    k = e.subs(x, h)
    return mk(f'Let f(x) = {fform(a, p, q)}. Write f(x) in the form ax² + bx + c and in the form a(x − h)² + k, and state the equation of the axis of symmetry.', f'{poly_txt(e)}; {vform(a, h, k)}; x = {P(h)}',
              f'expand (A1); axis at midpoint of roots x = {P(h)} (M1 A1); k = f({P(h)}) = {P(k)} (A1).', 4)


@R.add('ch06-st1', 'C3', (2, 4), 'short', style='p2')
def quad_model(rng, slot):
    kind = rng.choice(['ball', 'bridge', 'revenue'])
    if kind == 'ball':
        u, h0 = rng.choice([12, 14, 15, 18, 20, 22]), rng.choice([1.2, 1.5, 1.8, 2, 2.5])
        tm = u / 9.8
        hm = h0 + u * u / (2 * 9.8)
        land = (u + math.sqrt(u * u + 2 * 9.8 * h0)) / 9.8
        return mk(f'A ball is thrown upwards. Its height in metres after t seconds is h(t) = {h0:g} + {u}t − 4.9t². Find the maximum height, the time at which it occurs, and the time when the ball hits the ground, to 3 significant figures.',
                  f'{s3(hm)} m at t = {s3(tm)} s; lands at t = {s3(land)} s', f'vertex t = −b/(2a) = {s3(tm)} (M1 A1); h = {s3(hm)} (A1); solve h = 0, positive root {s3(land)} (M1 A1).', 5)
    if kind == 'bridge':
        w, hh = rng.choice([40, 50, 60, 80, 100]), rng.choice([8, 10, 12, 15, 20])
        a = -hh / (w / 2) ** 2
        d = rng.choice([5, 8, 10, 12, 15])
        hv = a * (d - w / 2) ** 2 + hh
        return mk(f'A parabolic arch spans {w} m at ground level and its highest point is {hh} m above the ground. Taking the origin at one foot of the arch, find the equation of the arch and the height of the arch {d} m from that foot, to 3 significant figures.',
                  f'y = {s3(a)}(x − {w // 2})² + {hh}; {s3(hv)} m', f'vertex ({w // 2}, {hh}) (A1); through (0, 0): a = {s3(a)} (M1 A1); y({d}) = {s3(hv)} (A1).', 4)
    p0, n0, dp, dn = rng.choice([(15, 200, 1, 40), (6, 400, 0.5, 100), (20, 300, 1, 30), (9, 300, 0.5, 60), (12, 150, 1, 25)])
    nmax = sp.Rational(p0 * dn + n0 * dp, 2 * dp * dn)
    px = p0 + float(nmax) * dp if False else None
    a_, b_ = -dp * dn, p0 * dn - n0 * dp
    xbest = -b_ / (2 * a_)
    price = p0 - xbest * dp
    rev = (p0 - xbest * dp) * (n0 + xbest * dn)
    return mk(f'A café sells {n0} drinks a day at ${p0:g} each. For every ${dp:g} decrease in price it sells {dn} more drinks. Write the daily revenue R as a function of the number x of ${dp:g} decreases, and find the price that maximises revenue.',
              f'R = ({p0:g} − {dp:g}x)({n0} + {dn}x); price ${price:.2f}, revenue ${rev:,.2f}', f'R(x) set up (M1 A1); vertex x = {s3(xbest)} (M1); price ${price:.2f} (A1).', 4)


@R.add('ch06-st1', 'C2', (2, 4), 'explain')
def quad_form_explain(rng, slot):
    p, q = sorted(rng.sample(range(-7, 8), 2))
    a = rng.choice([1, 2, -1])
    e = sp.expand(a * (x - p) * (x - q))
    return mk(f'Explain how the form y = {fform(a, p, q)} shows the x-intercepts and the axis of symmetry of the graph, and state them.', f'x = {p}, x = {q}; axis x = {P(sp.Rational(p + q, 2))}',
              f'y = 0 when either factor is 0 (R1); intercepts {p} and {q} (A1); symmetry means the axis is midway between the roots: x = {P(sp.Rational(p + q, 2))} (R1).', 3, 'explain')


@R.add('ch06-st1', 'C4', (3, 5), 'multi_step', style='ext')
def quad_parts(rng, slot):
    p, q = sorted(rng.sample(range(-5, 7), 2))
    a = rng.choice([1, 2, -1, -2])
    e = sp.expand(a * (x - p) * (x - q))
    h = sp.Rational(p + q, 2)
    k = e.subs(x, h)
    c = e.subs(x, 0)
    parts = [(f'Factorise f(x) = {poly_txt(e)}.', fform(a, p, q), 'A1 A1', 2, True),
             ('Write down the x-intercepts and the y-intercept of the graph of f.', f'x = {p}, {q}; y = {c}', 'A1 A1', 2, True),
             ('Find the equation of the axis of symmetry and the coordinates of the vertex.', f'x = {P(h)}; ({P(h)}, {P(k)})', 'M1 A1 A1', 3, True),
             ('Write f(x) in the form a(x − h)² + k.', vform(a, h, k), 'A1', 1, True),
             (f'The graph of f is translated by the vector ({rng.randint(1, 3)}, 0)ᵀ' if False else 'State the range of f.', f'f(x) {"≥" if a > 0 else "≤"} {P(k)}', 'A1', 1, True),
             (f'The line y = {c} meets the graph of f at two points. Find their x-coordinates.', f'x = 0, x = {P(2 * h)}', 'symmetry (R1) A1', 2, False)]
    return build_parts(rng, [f'Let f(x) = {poly_txt(e)}.', 'This question is about the three forms of a quadratic function.'], parts, 4)


@R.add('ch06-st1', 'C4', (4, 5), 'multi_step', style='p3')
def quad_family_p3(rng, slot):
    a = rng.choice([1, 2, 3])
    parts = [(f'For f_k(x) = {a if a > 1 else ""}x² − 2kx + k² + k, find the vertex of the graph in terms of k.', '(k, k)', 'complete the square (M1) A1 A1', 3, True),
             ('Show that the vertices of all graphs in the family lie on a straight line and state its equation.', 'y = x', 'R1 A1', 2, True),
             (f'Find the values of k for which f_k(x) = 0 has two distinct real roots.', 'k < 0', 'discriminant 4k² − 4·' + str(a) + '(k² + k) > 0 (M1 A1 A1)' if a == 1 else 'discriminant (M1 A1 A1)', 3, True),
             ('Find the value of k for which the graph passes through the origin, other than k = 0.', P(sp.Rational(-1, a)), f'{a if a > 1 else ""}k² + k = 0 (M1) A1', 2, True),
             ('Generalise: for g_k(x) = (x − k)² + mk, find the locus of the vertex and the values of k giving real roots.', 'y = mx; real roots when mk ≤ 0', 'A1 R1 A1', 3, True),
             ('Comment on how the family changes as k increases.', 'congruent parabolas translated along the line of vertices', 'R1', 1, False)]
    if a > 1:
        parts[0] = (f'For f_k(x) = {a}(x − k)² + k, find the vertex of the graph in terms of k.', '(k, k)', 'A1 A1', 2, True)
        parts[2] = ('Find the values of k for which f_k(x) = 0 has two distinct real roots.', 'k < 0', f'{a}(x − k)² = −k needs −k > 0 (M1 A1 A1)', 3, True)
    return build_parts(rng, ['This question investigates a family of quadratic functions.', 'In this question k is a real parameter.'], parts, 5)


# ---------------------------------------------------------------------------------------------
R.facts('ch06-st2', F(
    terms=[('discriminant', 'the quantity Δ = b² − 4ac for ax² + bx + c = 0, which determines the nature of the roots'),
           ('quadratic formula', 'the solution x = (−b ± √(b² − 4ac))/(2a) of ax² + bx + c = 0'),
           ('quadratic inequality', 'an inequality such as ax² + bx + c > 0, solved by finding the roots and using the shape of the parabola')],
    facts=[('If Δ < 0, the equation ax² + bx + c = 0 has', 'no real roots', ['two equal roots', 'two distinct real roots', 'one negative root'], 'Square root of a negative.'),
           ('The discriminant of 2x² − 3x + 5 = 0 is', '−31', ['49', '31', '−49'], '9 − 40.'),
           ('The solution of x² − 9 < 0 is', '−3 < x < 3', ['x < 3', 'x < −3 or x > 3', 'x > ±3'], 'Between the roots.'),
           ('x² − 5x + 6 = 0 has roots', '2 and 3', ['−2 and −3', '1 and 6', '−1 and 6'], '(x − 2)(x − 3).')],
    why=[('Explain why x² > 4 does not simply give x > ±2.', 'x² > 4 holds when |x| > 2, i.e. x < −2 or x > 2; "x > ±2" is meaningless and loses the negative branch.'),
         ('Explain why the discriminant tells you the number of x-intercepts of y = ax² + bx + c.', 'The x-intercepts are the real roots; in the quadratic formula √Δ is real and non-zero, zero, or not real according as Δ > 0, = 0, < 0, giving 2, 1 or 0 roots.'),
         ('Explain why you should not divide both sides of x² = 3x by x.', 'Dividing by x assumes x ≠ 0 and loses the root x = 0; factorise x(x − 3) = 0 instead.')],
    misc=[('If (x − 2)(x + 5) = 8 then x − 2 = 8 or x + 5 = 8.', 'The zero-product rule needs the product to be 0: expand to x² + 3x − 18 = 0, so x = 3 or x = −6.'),
          ('x² − 6x + 9 = 0 has no solution because Δ = 0.', 'Δ = 0 means one repeated real root, x = 3.')],
))


@R.add('ch06-st2', 'C1', (1, 3), 'mcq')
def disc_mcq(rng, slot):
    a, b, c = nz(rng, -4, 4), rng.randint(-9, 9), nz(rng, -9, 9)
    D = b * b - 4 * a * c
    nat = 'two distinct real roots' if D > 0 else 'two equal real roots' if D == 0 else 'no real roots'
    return mcq(rng, f'The equation {poly_txt(a * x ** 2 + b * x + c)} = 0 has', nat, [n_ for n_ in ['two distinct real roots', 'two equal real roots', 'no real roots', 'infinitely many roots'] if n_ != nat][:3], f'Δ = {D}.')


@R.add('ch06-st2', 'C3', (1, 4), 'short', style='p1')
def quad_solve(rng, slot):
    kind = rng.choice(['factor', 'formula', 'formula', 'hidden'])
    if kind == 'factor':
        a = rng.choice([1, 2, 3])
        p = sp.Rational(nz(rng, -6, 6), rng.choice([1, a]))
        q = nz(rng, -7, 7)
        e = sp.expand(a * (x - p) * (x - q) * (p.q))
        return mk(f'Solve {poly_txt(e)} = 0.', 'x = ' + ', '.join(P(r_) for r_ in sorted(set([p, sp.Integer(q)]), key=float)), 'factorise (M1 A1); roots (A1).', 3)
    if kind == 'formula':
        a, b, c = rng.choice([1, 2, 3]), rng.randint(-9, 9), nz(rng, -9, 9)
        D = b * b - 4 * a * c
        if D <= 0 or sp.sqrt(D).is_integer:
            return None
        r1, r2_ = sp.radsimp((-b - sp.sqrt(D)) / (2 * a)), sp.radsimp((-b + sp.sqrt(D)) / (2 * a))
        g = sp.gcd(sp.gcd(b, 2 * a), sp.sqrtdenest(sp.sqrt(D)).as_coeff_Mul()[0])
        sd = sp.sqrt(D)
        num = f'{-b} ± {P(sd)}' if b != 0 else f'±{P(sd)}'
        txt = f'({num})/{2 * a}'
        cc, rr = sd.as_coeff_Mul()
        g = math.gcd(math.gcd(int(b), 2 * a), int(cc))
        if g > 1:
            txt = f'({P(-b // g) if b else ""} ± {P(sd / g)})/{2 * a // g}'.replace('( ± ', '(±') if 2 * a // g != 1 else f'{P(-b // g)} ± {P(sd / g)}'
        return mk(f'Solve {poly_txt(a * x ** 2 + b * x + c)} = 0, giving your answers in exact form.', f'x = {txt}', f'Δ = {D} (A1); quadratic formula (M1); x = {txt} (A1).', 3)
    k = rng.choice(['exp', 'quartic', 'recip'])
    p, q = rng.sample([1, 2, 3, 4, 5, 6, 8, 9], 2)
    if k == 'exp':
        b_ = rng.choice([2, 3])
        p, q = b_ ** rng.randint(0, 3), b_ ** rng.randint(1, 3)
        if p == q:
            return None
        return mk(f'Solve {b_}^(2x) − {p + q}({b_}ˣ) + {p * q} = 0.', 'x = ' + ', '.join(str(int(round(math.log(v, b_)))) for v in sorted([p, q])),
                  f'let u = {b_}ˣ: u² − {p + q}u + {p * q} = 0 (M1); u = {p} or {q} (A1); x = log{sub(b_)} u (A1).', 3)
    if k == 'quartic':
        p, q = rng.sample([1, 4, 9, 16, 25], 2)
        roots = sorted([-int(math.isqrt(p)), int(math.isqrt(p)), -int(math.isqrt(q)), int(math.isqrt(q))])
        return mk(f'Solve x⁴ − {p + q}x² + {p * q} = 0.', 'x = ' + ', '.join(str(r_) for r_ in roots), f'let u = x²: (u − {p})(u − {q}) = 0 (M1 A1); x = ±√u (A1).', 3)
    a = rng.randint(1, 6)
    return mk(f'Solve x + {a * (a + 1)}/x = {2 * a + 1}, x ≠ 0.', f'x = {a}, x = {a + 1}', f'multiply by x: x² − {2 * a + 1}x + {a * (a + 1)} = 0 (M1 A1); x = {a}, {a + 1} (A1).', 3)


@R.add('ch06-st2', 'C3', (2, 5), 'short', style='p1')
def quad_ineq(rng, slot):
    p, q = sorted(rng.sample(range(-7, 8), 2))
    a = rng.choice([1, 1, 2, -1])
    e = sp.expand(a * (x - p) * (x - q))
    op = rng.choice(['>', '<', '≥', '≤'])
    inside = (op in '<≤') == (a > 0)
    st = '≤' if op in '≤≥' else '<'
    ans = f'{p} {st} x {st} {q}' if inside else f'x {"≤" if st == "≤" else "<"} {p} or x {"≥" if st == "≤" else ">"} {q}'
    rhs = rng.choice([0, 0, nz(rng, -6, 6)])
    lhs = poly_txt(e + rhs)
    return mk(f'Solve the inequality {lhs} {op} {rhs}.', ans, f'{"rearrange to " + poly_txt(e) + " " + op + " 0 (M1); " if rhs else ""}roots {p} and {q} (A1); parabola opens {"up" if a > 0 else "down"}, so the region is {"between" if inside else "outside"} the roots (M1); {ans} (A1).', 4)


@R.add('ch06-st2', 'C3', (2, 4), 'short', style='p2')
def quad_gdc(rng, slot):
    a, b, c = rng.choice([1.5, 2.3, -0.8, 0.6, 4.9, -1.2]), rng.choice([3.1, -2.7, 5.4, -6.2, 1.8]), rng.choice([-4.5, 2.2, -7.1, 3.3, -1.6])
    D = b * b - 4 * a * c
    if D <= 0:
        return None
    r = sorted([(-b - math.sqrt(D)) / (2 * a), (-b + math.sqrt(D)) / (2 * a)])
    kind = rng.choice(['eq', 'ineq'])
    if kind == 'eq':
        return mk(f'Solve {a:g}x² {"+" if b > 0 else "−"} {abs(b):g}x {"+" if c > 0 else "−"} {abs(c):g} = 0, giving your answers to 3 significant figures.', f'x = {s3(r[0])}, x = {s3(r[1])}', f'GDC or formula (M1); {s3(r[0])} (A1); {s3(r[1])} (A1).', 3)
    inside = a < 0
    ans = f'{s3(r[0])} < x < {s3(r[1])}' if not inside else f'x < {s3(r[0])} or x > {s3(r[1])}'
    return mk(f'Solve {a:g}x² {"+" if b > 0 else "−"} {abs(b):g}x {"+" if c > 0 else "−"} {abs(c):g} < 0, giving the boundary values to 3 significant figures.', ans, f'roots {s3(r[0])}, {s3(r[1])} (A1 A1); correct region from the graph (R1) (A1).', 4)


@R.add('ch06-st2', 'C2', (2, 4), 'explain')
def ineq_explain(rng, slot):
    p = rng.randint(2, 9)
    return mk(f'{who(rng)} solves x² < {p * p} and writes x < ±{p}. Explain why this is incorrect and give the correct solution.', f'−{p} < x < {p}',
              f'x² − {p * p} = (x − {p})(x + {p}) < 0 (M1); negative between the roots (R1); −{p} < x < {p} (A1).', 3, 'explain')


@R.add('ch06-st2', 'C4', (3, 5), 'multi_step', style='ext')
def quad_ineq_parts(rng, slot):
    p, q = sorted(rng.sample(range(-5, 7), 2))
    r1, r2_ = sorted(rng.sample(range(-6, 8), 2))
    f = sp.expand((x - p) * (x - q))
    g = sp.expand(f - (x - r1) * (x - r2_))
    if g.coeff(x, 1) == 0:
        return None
    roots = [sp.Integer(r1), sp.Integer(r2_)]
    parts = [(f'Solve f(x) = 0.', f'x = {p}, {q}', 'A1', 1, True),
             ('Solve f(x) < 0.', f'{p} < x < {q}', 'A1 A1', 2, True),
             (f'Find the x-coordinates of the points of intersection of y = f(x) and y = {poly_txt(g)}.', 'x = ' + ', '.join(P(r_) for r_ in roots), 'set equal (M1); solve (A1 A1)', 3, True),
             (f'Hence solve f(x) > {poly_txt(g)}.', f'x < {P(roots[0])} or x > {P(roots[1])}', 'R1 A1', 2, True),
             (f'Find the discriminant of f(x) − k = 0 and hence the set of values of k for which f(x) = k has two distinct real roots.', f'k > {P(sp.expand(f.subs(x, sp.Rational(p + q, 2))))}', 'M1 A1 A1', 3, False)]
    return build_parts(rng, [f'Let f(x) = {poly_txt(f)}.', f'The function f is defined by f(x) = {poly_txt(f)}, x ∈ ℝ.'], parts, 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch06-st3', F(
    terms=[('tangent to a parabola (from a line)', 'a line that meets the parabola at exactly one point, so the resulting quadratic has Δ = 0'),
           ('positive definite quadratic', 'a quadratic with ax² + bx + c > 0 for all x, i.e. a > 0 and Δ < 0'),
           ('parameter', 'a constant, such as k, whose value is to be found or which varies within a family of equations')],
    facts=[('y = mx + c is tangent to y = ax² + bx + c\' when ax² + (b − m)x + (c\' − c) = 0 has', 'Δ = 0', ['Δ > 0', 'Δ < 0', 'a = 0'], 'Exactly one intersection.'),
           ('x² + kx + 9 = 0 has equal roots when k =', '±6', ['9', '±3', '6 only'], 'k² − 36 = 0.'),
           ('x² + 2x + k > 0 for all x when', 'k > 1', ['k < 1', 'k > −1', 'k ≥ 0'], '4 − 4k < 0.'),
           ('A line meets a parabola in two points when the combined quadratic has', 'Δ > 0', ['Δ = 0', 'Δ < 0', 'Δ = 1'], 'Two distinct roots.')],
    why=[('Explain why the condition for y = mx + c to touch a parabola is a discriminant equal to zero.', 'Equating the two expressions gives a quadratic whose real roots are the x-coordinates of intersection points; touching means exactly one such point, a repeated root, so Δ = 0.'),
         ('Explain why a quadratic with a < 0 can never be positive for all x.', 'For large |x| the term ax² dominates and is negative, so the quadratic takes negative values.'),
         ('Explain why kx² + 4x + 1 = 0 needs separate consideration when k = 0.', 'When k = 0 the equation is linear (4x + 1 = 0) with exactly one root, and the discriminant method for quadratics does not apply.')],
    misc=[('kx² + 6x + k = 0 has real roots when 36 − 4k² > 0, so −3 < k < 3.', 'Real roots need Δ ≥ 0: −3 ≤ k ≤ 3 (and for k = 0 the equation is linear with one root).'),
          ('If x² + bx + c > 0 for all x, then c > 0 and b > 0.', 'The condition is b² − 4c < 0; b may be negative, e.g. x² − 2x + 5.')],
))


@R.add('ch06-st3', 'C1', (1, 3), 'mcq')
def param_mcq(rng, slot):
    c = rng.choice([1, 4, 9, 16, 25, 36])
    a = rng.choice([1, 4]) if c % 4 == 0 else 1
    k = 2 * int(math.isqrt(a * c))
    return mcq(rng, f'{poly_txt(a * x ** 2)} + kx + {c} = 0 has equal roots when k =', f'±{k}', [str(k), f'±{k // 2}', f'±{a * c}'], f'k² − {4 * a * c} = 0.')


@R.add('ch06-st3', 'C3', (2, 5), 'short', style='p1')
def param_disc(rng, slot):
    kind = rng.choice(['equal', 'real', 'none', 'kk'])
    if kind == 'kk':
        p, q = rng.randint(1, 4), rng.randint(1, 5)
        k = sp.Symbol('k')
        D = sp.expand((2 * p) ** 2 * 0 + (k + q) ** 2 - 4 * k * p)
        sols = sp.solve(D, k)
        if not all(s_.is_rational for s_ in sols):
            return None
        return mk(f'Find the values of k for which kx² + ({poly_txt(k + q, k).replace("x", "k")})x + {p} = 0 has equal roots.'.replace('(k + ', '(k + '), 'k = ' + ', '.join(P(s_) for s_ in sorted(sols, key=float)),
                  f'Δ = (k + {q})² − {4 * p}k (M1 A1); = 0 (M1); k = {", ".join(P(s_) for s_ in sorted(sols, key=float))} (A1).', 4)
    a, b = rng.randint(1, 4), nz(rng, -8, 8)
    crit = sp.Rational(b * b, 4 * a)
    ans = {'equal': f'k = {P(crit)}', 'real': f'k ≤ {P(crit)}', 'none': f'k > {P(crit)}'}[kind]
    phrase = {'equal': 'has two equal roots', 'real': 'has real roots', 'none': 'has no real roots'}[kind]
    return mk(f'Find the value(s) of k for which {poly_txt(a * x ** 2 + b * x)} + k = 0 {phrase}.', ans,
              f'Δ = {b * b} − {4 * a}k (A1); {"=" if kind == "equal" else "≥" if kind == "real" else "<"} 0 (M1); {ans} (A1).', 3)


@R.add('ch06-st3', 'C3', (2, 5), 'short', style='p1')
def tangent_line(rng, slot):
    a, b, c = rng.choice([1, 2, -1]), nz(rng, -6, 6), rng.randint(-6, 6)
    x0 = nz(rng, -4, 4)
    m = 2 * a * x0 + b
    cc = a * x0 ** 2 + b * x0 + c - m * x0
    kind = rng.choice(['c', 'm'])
    if kind == 'c':
        return mk(f'The line y = {P(m * x)} + k is a tangent to the curve y = {poly_txt(a * x ** 2 + b * x + c)}. Find the value of k and the coordinates of the point of contact.'.replace('y = 0 + k', 'y = k'),
                  f'k = {cc}; ({x0}, {a * x0 ** 2 + b * x0 + c})', f'{poly_txt(a * x ** 2 + (b - m) * x + c)} − k = 0 (M1); Δ = 0 (M1); k = {cc} (A1); point ({x0}, {a * x0 ** 2 + b * x0 + c}) (A1).', 4)
    if c - cc == 0:
        return None
    k = sp.Symbol('k')
    D = sp.expand((b - k) ** 2 - 4 * a * (c - cc))
    sols = sorted(sp.solve(D, k), key=float)
    if not all(s_.is_rational for s_ in sols):
        return None
    return mk(f'The line y = kx {"+" if cc >= 0 else "−"} {abs(cc)} is a tangent to y = {poly_txt(a * x ** 2 + b * x + c)}. Find the possible values of k.'.replace(' + 0 is', ' is'), 'k = ' + ', '.join(P(s_) for s_ in sols),
              f'{poly_txt(a * x ** 2)} + ({b} − k)x + {c - cc} = 0 (M1); Δ = ({b} − k)² − {4 * a * (c - cc)} = 0 (M1 A1); k = {", ".join(P(s_) for s_ in sols)} (A1).'.replace('+ −', '− '), 4)


@R.add('ch06-st3', 'C3', (2, 4), 'short', style='p2')
def param_gdc(rng, slot):
    a, b = rng.choice([0.5, 1.5, 2, 2.5, 3]), rng.choice([3, -4, 5, -6, 7])
    m = rng.choice([1, 2, -1, 0.5])
    kind = rng.choice(['tangent', 'range'])
    if kind == 'tangent':
        cc = -((b - m) ** 2) / (4 * a)
        return mk(f'The line y = {m:g}x + c is tangent to y = {a:g}x² {"+" if b > 0 else "−"} {abs(b)}x. Find c, correct to 3 significant figures.', f'c = {s3(cc)}',
                  f'{a:g}x² + ({b} − {m:g})x − c = 0 (M1); Δ = 0 (M1); c = {s3(cc)} (A1).', 3)
    lim = (b - m) ** 2 / (4 * a)
    return mk(f'Find the range of values of c for which the line y = {m:g}x + c meets y = {a:g}x² {"+" if b > 0 else "−"} {abs(b)}x at two distinct points. Give the boundary value to 3 significant figures.', f'c > {s3(-lim)}',
              f'combined quadratic (M1); Δ = ({b} − {m:g})² + {4 * a:g}c > 0 (M1); c > {s3(-lim)} (A1).', 3)


@R.add('ch06-st3', 'C2', (2, 4), 'explain')
def param_explain(rng, slot):
    a, b = rng.randint(1, 4), rng.randint(2, 8)
    return mk(f'Explain why x² {"+" if rng.random() < 0.5 else "−"} {2 * b}x + k > 0 for all real x if and only if k > {b * b}.', f'k > {b * b}',
              f'the quadratic has a > 0, so it is always positive iff it has no real roots (R1); Δ = {4 * b * b} − 4k < 0 (M1); k > {b * b} (A1).', 3, 'explain')


@R.add('ch06-st3', 'C4', (3, 5), 'multi_step', style='ext')
def param_parts(rng, slot):
    a, b = rng.choice([1, 2]), rng.randint(1, 6)
    m = rng.randint(1, 4)
    # curve y = a x^2 + b, line y = m x + k
    kcrit = sp.Rational(-(m * m), 4 * a) + b
    x0 = sp.Rational(m, 2 * a)
    parts = [(f'Show that the x-coordinates of the intersection points of y = {poly_txt(a * x ** 2 + b)} and y = {m}x + k satisfy {poly_txt(a * x ** 2 - m * x + b)} − k = 0.', 'shown', 'M1 AG', 1, True),
             ('Find the value of k for which the line is a tangent to the curve.', f'k = {P(kcrit)}', 'Δ = 0 (M1 A1) A1', 3, True),
             ('Find the coordinates of the point of contact.', f'({P(x0)}, {P(a * x0 ** 2 + b)})', 'M1 A1', 2, True),
             ('Find the values of k for which the line meets the curve at two points.', f'k > {P(kcrit)}', 'A1', 1, True),
             (f'For k = {P(kcrit + 2)}, find the exact x-coordinates of the intersection points.', 'x = ' + ', '.join(nice(r_) for r_ in sorted(sp.solve(a * x ** 2 - m * x + b - (kcrit + 2), x), key=float)), 'formula (M1) A1', 2, False)]
    return build_parts(rng, ['This question is about a line meeting a parabola.', f'A curve has equation y = {poly_txt(a * x ** 2 + b)} and a line has equation y = {m}x + k.'], parts, 4)


@R.add('ch06-st2', 'C2', (2, 4), 'explain')
def disc_explain(rng, slot):
    a, b, c = nz(rng, -3, 4), rng.randint(-8, 8), nz(rng, -9, 9)
    D = b * b - 4 * a * c
    n = 2 if D > 0 else 1 if D == 0 else 0
    return mk(f'Without solving, explain how many times the graph of y = {poly_txt(a * x ** 2 + b * x + c)} meets the x-axis.', str(n),
              f'Δ = ({b})² − 4({a})({c}) = {D} (A1); Δ {">" if D > 0 else "=" if D == 0 else "<"} 0 (R1); so {n} x-intercept{"s" if n != 1 else ""} (A1).', 3, 'explain')


@R.add('ch06-st3', 'C2', (2, 4), 'explain')
def tangency_explain(rng, slot):
    a, b = rng.randint(1, 3), rng.randint(1, 9)
    m = rng.randint(1, 6)
    c = b - sp.Rational(m * m, 4 * a) - rng.randint(1, 5)
    return mk(f'Explain why the line y = {m}x + {P(c)} does not meet the curve y = {poly_txt(a * x ** 2 + b)}.'.replace('+ −', '− '), 'Δ < 0',
              f'{poly_txt(a * x ** 2 - m * x)} + {P(b - c)} = 0 (M1); Δ = {m * m} − {P(4 * a * (b - c))} < 0 (R1); no real intersection (A1).', 3, 'explain')


# =============================================================================================
# ch07 Rational, exponential and logarithmic functions; solving equations (SL 2.8–2.10)
# =============================================================================================
def rat_txt(a, b, c, d):
    num = poly_txt(a * x + b) if a != 0 else str(b)
    den = poly_txt(c * x + d)
    return f'({num})/({den})' if (a != 0 and b != 0) or True else ''


R.facts('ch07-st1', F(
    terms=[('reciprocal function', 'the function f(x) = k/x, x ≠ 0, whose graph is a hyperbola with asymptotes x = 0 and y = 0'),
           ('rational function of linear form', 'a function f(x) = (ax + b)/(cx + d) with c ≠ 0 and ad − bc ≠ 0'),
           ('self-inverse function', 'a function with f⁻¹ = f, such as f(x) = 1/x')],
    facts=[('The asymptotes of y = (2x + 1)/(x − 3) are', 'x = 3 and y = 2', ['x = −3 and y = 2', 'x = 3 and y = 1/3', 'x = 2 and y = 3'], 'Denominator zero; ratio of leading coefficients.'),
           ('The graph of y = 4/x lies in quadrants', '1 and 3', ['2 and 4', '1 and 2', 'all four'], 'x and y have the same sign.'),
           ('The inverse of f(x) = 1/x is', '1/x', ['x', '−1/x', 'x²'], 'Self-inverse.'),
           ('The range of y = 3 + 2/(x − 1) is', 'y ≠ 3', ['y ≠ 1', 'y > 3', 'all real y'], 'The fraction is never zero.')],
    why=[('Explain why y = (ax + b)/(cx + d) approaches y = a/c for large |x|.', 'Dividing numerator and denominator by x gives (a + b/x)/(c + d/x); as |x| → ∞, b/x and d/x → 0, so y → a/c.'),
         ('Explain why f(x) = 1/x is its own inverse.', 'Solving y = 1/x for x gives x = 1/y, the same rule; equivalently f(f(x)) = 1/(1/x) = x, and the graph is symmetric in y = x.'),
         ('Explain why (2x + 4)/(x + 2) is not a genuine rational function of linear form.', 'It simplifies to 2 (for x ≠ −2), because ad − bc = 2·2 − 4·1 = 0; its graph is a horizontal line with a hole.')],
    misc=[('y = 3/(x + 2) has a vertical asymptote at x = 2.', 'The denominator is zero at x = −2.'),
          ('y = (x − 1)/(2x + 3) has horizontal asymptote y = 1.', 'The asymptote is y = 1/2, the ratio of the leading coefficients.')],
))


@R.add('ch07-st1', 'C1', (1, 3), 'mcq')
def recip_mcq(rng, slot):
    k = nz(rng, -9, 9)
    h, v = nz(rng, -5, 5), nz(rng, -5, 5)
    f = f'{k}/(x {"−" if h > 0 else "+"} {abs(h)}) {"+" if v > 0 else "−"} {abs(v)}'
    if rng.random() < 0.5:
        return mcq(rng, f'The range of y = {f} is', f'y ≠ {v}', [f'y ≠ {h}', f'y > {v}', f'y ≠ {-v}'], 'The fraction never equals zero.')
    return mcq(rng, f'The vertical asymptote of y = {f} is', f'x = {h}', [f'x = {-h}', f'y = {v}', f'x = {v}' if v != h else f'x = {k}'], 'Denominator zero.')


@R.add('ch07-st1', 'C3', (1, 4), 'short', style='p1')
def rational_lin(rng, slot):
    a, b, c, d = nz(rng, -6, 6), nz(rng, -9, 9), nz(rng, 1, 3), nz(rng, -6, 6)
    if a * d - b * c == 0:
        return None
    kind = rng.choice(['sketch', 'inverse', 'rewrite'])
    va, ha = sp.Rational(-d, c), sp.Rational(a, c)
    if kind == 'sketch':
        return mk(f'Sketch the graph of y = {rat_txt(a, b, c, d)}, showing the asymptotes and axis intercepts. State the equations of the asymptotes and the intercepts.',
                  f'x = {P(va)}; y = {P(ha)}; ({P(sp.Rational(-b, a))}, 0); (0, {P(sp.Rational(b, d))})', 'asymptotes (A1 A1); intercepts (A1 A1); correct shape in two branches (A1).', 5)
    if kind == 'inverse':
        y_ = sp.Symbol('y')
        inv = sp.solve(sp.Eq((a * y_ + b) / (c * y_ + d), x), y_)[0]
        nu, de = sp.fraction(sp.together(inv))
        if sp.Poly(de, x).LC() < 0:
            nu, de = -nu, -de
        it = f'({poly_txt(sp.expand(nu))})/({poly_txt(sp.expand(de))})'
        return mk(f'Let f(x) = {rat_txt(a, b, c, d)}, x ≠ {P(va)}. Find f⁻¹(x) and state the equations of the asymptotes of y = f⁻¹(x).', f'f⁻¹(x) = {it}; x = {P(ha)}, y = {P(va)}',
                  'swap x and y (M1); rearrange (M1); f⁻¹ (A1); asymptotes swap: x = a/c, y = −d/c (A1).', 4)
    q = sp.Rational(a, c)
    r = b - q * d
    return mk(f'Write {rat_txt(a, b, c, d)} in the form p + q/({poly_txt(c * x + d)}), and hence state the range of y = {rat_txt(a, b, c, d)}.', f'{P(q)} + {P(r)}/({poly_txt(c * x + d)}); y ≠ {P(q)}'.replace('+ −', '− '),
              f'divide: p = {P(q)} (M1 A1); q = {P(r)} (A1); range y ≠ {P(q)} (A1).', 4)


@R.add('ch07-st1', 'C3', (2, 4), 'short', style='p2')
def recip_model(rng, slot):
    kind = rng.choice(['boyle', 'cost'])
    if kind == 'boyle':
        k = rng.choice([120, 150, 240, 300, 360])
        v = rng.choice([1.5, 2.5, 3.2, 4.8, 7.5])
        return mk(f'At constant temperature, the pressure P (kPa) of a gas is inversely proportional to its volume V (litres). When V = {k // 60} litres, P = 60 kPa. Find P when V = {v:g} litres and the volume when P = 100 kPa, to 3 significant figures.',
                  f'P = {s3(k / v)} kPa; V = {s3(k / 100)} litres', f'P = k/V with k = {k} (M1 A1); P({v:g}) = {s3(k / v)} (A1); V = {s3(k / 100)} (A1).', 4)
    f0, cpu = rng.choice([(1200, 3.5), (5000, 2.4), (800, 6.25), (2500, 1.8)])
    n = rng.randint(50, 400)
    target = rng.choice([cpu + 2, cpu + 4, cpu * 2])
    nt = f0 / (target - cpu)
    return mk(f'A printer has fixed costs of ${f0} and each poster costs ${cpu:.2f} to print. The average cost per poster for n posters is A(n) = (f₀ + cn)/n. Find A({n}), state the horizontal asymptote of A, and find the least n for which A(n) < ${target:.2f}.',
              f'${(f0 + cpu * n) / n:.2f}; A = {cpu:g}; n = {math.floor(nt) + 1}', f'A({n}) = ({f0} + {cpu:g} × {n})/{n} (M1 A1); asymptote A = {cpu:g} (A1); solve A(n) = {target:.2f}: n = {s3(nt)}, so n = {math.floor(nt) + 1} (M1 A1).', 5)


@R.add('ch07-st1', 'C2', (2, 4), 'explain')
def rational_explain(rng, slot):
    a, c = rng.randint(1, 6), rng.randint(1, 4)
    k = rng.randint(1, 5)
    return mk(f'Explain why the graph of y = ({a * k}x + {a * k * 2})/({k}x + {2 * k}) is not a hyperbola, and describe the graph.', f'the line y = {a} with a hole at x = −2',
              f'ad − bc = {a * k * 2 * k} − {a * k * 2 * k} = 0 (R1); the fraction cancels to {a} for x ≠ −2 (A1); horizontal line with the point at x = −2 missing (R1).', 3, 'explain')


@R.add('ch07-st1', 'C4', (3, 5), 'multi_step', style='ext')
def rational_parts(rng, slot):
    a, b, c, d = nz(rng, 1, 5), nz(rng, -8, 8), 1, nz(rng, -5, 5)
    if a * d - b * c == 0:
        return None
    va, ha = -d, a
    kline = rng.randint(1, 4)
    sols = sorted([s_ for s_ in sp.solve((a * x + b) - kline * (x + d) * 1 - 0 * x, x)], key=float) if a != kline else []
    parts = [(f'Write down the equations of the asymptotes of the graph of f.', f'x = {va}, y = {ha}', 'A1 A1', 2, True),
             ('Find the coordinates of the points where the graph meets the axes.', f'({P(sp.Rational(-b, a))}, 0), (0, {P(sp.Rational(b, d))})', 'A1 A1', 2, True),
             ('Sketch the graph of y = f(x).', 'two branches with the asymptotes and intercepts above', 'A1 A1', 2, True),
             ('Find f⁻¹(x) and state its domain.', f'({poly_txt(-d * x + b)})/({poly_txt(x - a)}), x ≠ {a}', 'M1 A1 A1', 3, True),
             (f'Solve f(x) = {kline}.', ('x = ' + P(sols[0])) if sols else 'no solution (the line is the asymptote)', 'M1 A1', 2, False),
             ('Find the coordinates of the point where the asymptotes meet and explain why the graph is symmetric about this point.', f'({va}, {ha}); f(x) = {ha} + k/(x + {d}) is a translation of y = k/x, which has rotational symmetry about the origin', 'A1 R1', 2, False)]
    return build_parts(rng, [f'Let f(x) = {rat_txt(a, b, c, d)}, x ≠ {va}.'.replace('+ −', '− '), f'The function f is defined by f(x) = {rat_txt(a, b, c, d)}, x ≠ {va}.'], parts, 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch07-st2', F(
    terms=[('exponential function', 'a function f(x) = aˣ (a > 0, a ≠ 1) or more generally k·aˣ + c, with a horizontal asymptote'),
           ('natural exponential function', 'the function f(x) = eˣ, where e ≈ 2.718'),
           ('logarithmic function', 'the function f(x) = logₐ x, x > 0, the inverse of aˣ'),
           ('natural logarithm', 'the logarithm ln x = logₑ x, the inverse of eˣ')],
    facts=[('The graph of y = eˣ passes through', '(0, 1)', ['(1, 0)', '(0, e)', '(1, 1)'], 'e⁰ = 1.'),
           ('The horizontal asymptote of y = 3 + 2e^(−x) is', 'y = 3', ['y = 2', 'y = 0', 'x = 3'], 'e^(−x) → 0 as x → ∞.'),
           ('The domain of y = ln(x − 4) is', 'x > 4', ['x ≥ 4', 'x > 0', 'all real x'], 'Argument positive.'),
           ('The graph of y = ln x is the reflection of y = eˣ in', 'y = x', ['the x-axis', 'the y-axis', 'y = −x'], 'Inverse functions.')],
    why=[('Explain why y = logₐ x has a vertical asymptote at x = 0.', 'It is the inverse of aˣ, which has horizontal asymptote y = 0; reflecting in y = x turns this into x = 0, and logₐ x → −∞ as x → 0⁺ (for a > 1).'),
         ('Explain why exponential growth eventually exceeds any polynomial growth.', 'The ratio eˣ/xⁿ → ∞ as x → ∞ for every n, since each increase of x by 1 multiplies eˣ by e but multiplies xⁿ by a factor approaching 1.'),
         ('Explain why y = 2ˣ and y = (1/2)ˣ are reflections of each other in the y-axis.', '(1/2)ˣ = 2^(−x), which is f(−x) for f(x) = 2ˣ.')],
    misc=[('The range of y = eˣ − 5 is y > 0.', 'The graph is translated down 5, so the range is y > −5.'),
          ('ln(x + 3) is defined for x ≥ −3.', 'ln 0 is undefined, so x + 3 > 0, i.e. x > −3.')],
))


@R.add('ch07-st2', 'C1', (1, 3), 'mcq')
def explog_mcq(rng, slot):
    k, c = nz(rng, -5, 5), nz(rng, -6, 6)
    kind = rng.choice(['asym', 'dom', 'int'])
    if kind == 'asym':
        return mcq(rng, f'The horizontal asymptote of y = {k}e^(x) {"+" if c > 0 else "−"} {abs(c)} is'.replace('e^(x)', 'eˣ'), f'y = {c}', [f'y = {k}', 'y = 0', f'x = {c}'], 'eˣ → 0 as x → −∞.')
    if kind == 'dom':
        return mcq(rng, f'The vertical asymptote of y = ln(x {"−" if c > 0 else "+"} {abs(c)}) is', f'x = {c}', [f'x = {-c}', f'y = {c}', 'x = 0'], 'Argument zero.')
    return mcq(rng, f'The y-intercept of y = {k}e^(x) {"+" if c > 0 else "−"} {abs(c)} is'.replace('e^(x)', 'eˣ'), str(k + c), [str(c), str(k), str(k * c)], 'e⁰ = 1.')


@R.add('ch07-st2', 'C3', (1, 4), 'short', style='p1')
def explog_features(rng, slot):
    kind = rng.choice(['exp', 'log', 'inv'])
    a, c = nz(rng, -6, 6), nz(rng, -6, 6)
    b = rng.choice([1, 2, 3, -1, -2])
    if kind == 'exp':
        if a * c >= 0:
            xi = None
        else:
            xi = sp.log(sp.Rational(-c, a)) / b
        xt = f'({P(xi)}, 0)' if xi is not None else 'none'
        return mk(f'For y = {a}e^({P(b * x)}) {"+" if c > 0 else "−"} {abs(c)}, find the y-intercept, the x-intercept (if any) in exact form, and the equation of the horizontal asymptote.'.replace('e^(x)', 'eˣ'),
                  f'(0, {a + c}); {xt}; y = {c}', f'y-intercept {a} + {c} (A1); solve e^({P(b * x)}) = {P(sp.Rational(-c, a))} (M1) (A1); asymptote y = {c} (A1).', 4)
    if kind == 'log':
        p = rng.randint(1, 4)
        q = nz(rng, -6, 6)
        xi = sp.exp(sp.Rational(-c, a)) * 0 + (sp.exp(sp.Rational(-c, a)) - q) / p
        return mk(f'For y = {a} ln({poly_txt(p * x + q)}) {"+" if c > 0 else "−"} {abs(c)}, state the domain and the equation of the vertical asymptote, and find the exact x-intercept.',
                  f'x > {P(sp.Rational(-q, p))}; x = {P(sp.Rational(-q, p))}; x = {P(xi)}', f'{poly_txt(p * x + q)} > 0 (A1); asymptote (A1); ln({poly_txt(p * x + q)}) = {P(sp.Rational(-c, a))} (M1); x = {P(xi)} (A1).', 4)
    p = rng.randint(2, 5)
    return mk(f'Let f(x) = {p}e^(x − {abs(c)}) + {abs(a)}. Find f⁻¹(x), and state the domain and range of f⁻¹.', f'f⁻¹(x) = {abs(c)} + ln((x − {abs(a)})/{p}); x > {abs(a)}; f⁻¹(x) ∈ ℝ',
              f'swap and rearrange (M1); e^(y − {abs(c)}) = (x − {abs(a)})/{p} (A1); f⁻¹ (A1); domain is the range of f, x > {abs(a)} (A1).', 4)


@R.add('ch07-st2', 'C3', (2, 5), 'short', style='p2')
def exp_model(rng, slot):
    kind = rng.choice(['cool', 'decay', 'growth', 'loggrowth'])
    if kind == 'cool':
        Ta, T0, k = rng.choice([18, 20, 22]), rng.choice([85, 90, 95, 100]), rng.choice([0.04, 0.05, 0.06, 0.08])
        t1 = rng.choice([5, 10, 15])
        Tt = rng.choice([40, 45, 50, 60])
        return mk(f'The temperature of a cup of tea t minutes after it is made is T(t) = {Ta} + {T0 - Ta}e^(−{k:g}t) °C. Find T({t1}), the time for the tea to cool to {Tt} °C, and the temperature the tea approaches in the long run.',
                  f'{s3(Ta + (T0 - Ta) * math.exp(-k * t1))} °C; {s3(math.log((T0 - Ta) / (Tt - Ta)) / k)} min; {Ta} °C', f'substitute (A1); solve {Tt} = ... (M1 A1); asymptote {Ta} (A1).', 4)
    if kind == 'decay':
        m0, hl = rng.choice([50, 80, 120, 200]), rng.choice([5.3, 8, 12.5, 28.8, 30])
        k = math.log(2) / hl
        t1 = rng.randint(2, 40)
        return mk(f'A radioactive sample has mass m(t) = {m0}e^(−kt) grams, t in years. Its half-life is {hl:g} years. Find k and the mass after {t1} years, to 3 significant figures.',
                  f'k = {s3(k)}; {s3(m0 * math.exp(-k * t1))} g', f'e^(−{hl:g}k) = 1/2 (M1); k = ln 2/{hl:g} = {s3(k)} (A1); m({t1}) (M1) {s3(m0 * math.exp(-k * t1))} (A1).', 4)
    if kind == 'growth':
        P0, r = rng.choice([500, 1200, 2500, 40]), rng.choice([0.12, 0.2, 0.35, 0.08])
        target = P0 * rng.choice([3, 5, 10])
        return mk(f'A population of bacteria is modelled by N(t) = {P0}e^({r:g}t), where t is in hours. Find the time taken for the population to reach {target}, and the rate of increase as a percentage per hour.',
                  f'{s3(math.log(target / P0) / r)} hours; {s3((math.exp(r) - 1) * 100)}% per hour', f'solve e^({r:g}t) = {target // P0} (M1 A1); growth factor e^({r:g}) = {s3(math.exp(r))} (M1) (A1).', 4)
    a, b = rng.choice([(12, 3.5), (20, 4.2), (8, 6.1), (15, 2.8)])
    tt = rng.randint(2, 20)
    return mk(f'The height of a plant, in cm, t weeks after planting is modelled by h(t) = {a} + {b:g} ln(t + 1). Find h({tt}) and the time at which the plant reaches {a + 10} cm.', f'{s3(a + b * math.log(tt + 1))} cm; {s3(math.exp(10 / b) - 1)} weeks',
              f'substitute (A1); ln(t + 1) = {s3(10 / b)} (M1); t = e^({s3(10 / b)}) − 1 = {s3(math.exp(10 / b) - 1)} (A1).', 3)


@R.add('ch07-st2', 'C3', (2, 4), 'short', style='p1')
def explog_transform(rng, slot):
    a, h, k = rng.choice([2, 3, 'e']), nz(rng, -4, 4), nz(rng, -5, 5)
    base = 'e' if a == 'e' else str(a)
    lg = 'ln' if a == 'e' else f'log{sub(a)}'
    return mk(f'The graph of y = {base}ˣ is translated by the vector ({h}, {k})ᵀ. Write down the equation of the new graph, its horizontal asymptote, and the equation of the inverse of the new function.',
              f'y = {base}^(x {"−" if h > 0 else "+"} {abs(h)}) {"+" if k > 0 else "−"} {abs(k)}; y = {k}; y = {lg}(x {"−" if k > 0 else "+"} {abs(k)}) {"+" if h > 0 else "−"} {abs(h)}',
              f'replace x by x − {h} and add {k} (A1 A1); asymptote y = {k} (A1); swap and use {lg} (M1 A1).'.replace('− −', '+ '), 5)


@R.add('ch07-st2', 'C2', (2, 4), 'explain')
def explog_explain(rng, slot):
    a = rng.choice([2, 3, 5, 10])
    c = rng.randint(1, 6)
    return mk(f'Explain why the equation {a}ˣ + {c} = {c - rng.randint(1, 5)} has no real solution.', 'no solution',
              f'{a}ˣ > 0 for all x (R1); so {a}ˣ + {c} > {c} (R1); the right-hand side is less than {c} (A1).', 3, 'explain')


@R.add('ch07-st2', 'C4', (3, 5), 'multi_step', style='ext')
def explog_parts(rng, slot):
    a, b = rng.randint(2, 6), rng.choice([2, 3, 4])
    k = rng.choice([0.5, 1, 2])
    f = f'{a} − {b}e^(−{k:g}x)'.replace('−1x', '−x')
    xi = math.log(b / a) / -k
    parts = [(f'Find the y-intercept of the graph of f.', str(a - b), 'A1', 1, True),
             ('Find the x-intercept, giving your answer in exact form.', f'x = {P(sp.log(sp.Rational(b, a)) / sp.nsimplify(k))}' if a != b else 'x = 0', 'M1 A1', 2, True),
             ('Write down the equation of the horizontal asymptote.', f'y = {a}', 'A1', 1, True),
             ('Find f⁻¹(x) and state its domain.', (f'f⁻¹(x) = −ln(({a} − x)/{b}); x < {a}' if k == 1 else f'f⁻¹(x) = −{P(sp.nsimplify(1 / k))} ln(({a} − x)/{b}); x < {a}' if k < 1 else f'f⁻¹(x) = −(1/{int(k)}) ln(({a} − x)/{b}); x < {a}'), 'M1 A1 A1', 3, True),
             (f'Sketch y = f(x) and y = f⁻¹(x) on the same axes and find, using your GDC, the x-coordinates of their points of intersection.', ', '.join(s3(r_) for r_ in nsols(lambda v: a - b * math.exp(-k * v) - v, -3, 10)) or 'no points of intersection', 'symmetry in y = x (R1); GDC (A1 A1)', 3, False)]
    return build_parts(rng, [f'Let f(x) = {f}, x ∈ ℝ.', f'The function f is defined by f(x) = {f}.'], parts, 4)


@R.add('ch07-st2', 'C4', (4, 5), 'multi_step', style='p3')
def explog_p3(rng, slot):
    n = rng.choice([2, 3, 4])
    parts = [(f'Use your GDC to find the number of solutions of eˣ = x{sup(n)} and state them to 3 significant figures.', ', '.join(s3(r_) for r_ in nsols(lambda v: math.exp(v) - v ** n, -5, 15)), 'GDC (M1) A1 A1', 3, True),
             (f'Show that for x > 0, eˣ = x{sup(n)} is equivalent to x/ln x = {n} (x ≠ 1).', 'take ln of both sides: x = n ln x', 'M1 AG', 2, True),
             ('Let g(x) = x/ln x, x > 1. Find the minimum value of g using your GDC.', 'e at x = e', 'A1 A1', 2, True),
             (f'Hence explain why eˣ = xᵏ has two solutions with x > 1 if k > e and none if 1 < k < e.', 'g(x) = k has two solutions iff k > min g = e', 'R1 R1', 2, True),
             ('Decide, with a reason, which is larger: e^π or π^e.', 'e^π', 'compare π/ln π with e: π/ln π > e (R1) A1', 2, True),
             ('Generalise: for which positive integers n does eˣ = xⁿ have a negative solution?', 'all even n', 'R1 A1', 2, False)]
    return build_parts(rng, ['This question compares exponential and power functions.', 'In this question x is real.'], parts, 5)


# ---------------------------------------------------------------------------------------------
R.facts('ch07-st3', F(
    terms=[('analytic solution', 'a solution found exactly by algebraic manipulation, without technology'),
           ('graphical solution', 'a solution found as the x-coordinate of an intersection of graphs, usually with a GDC'),
           ('extraneous solution', 'a value produced by a method (e.g. squaring) that does not satisfy the original equation')],
    facts=[('To solve f(x) = g(x) graphically, find', 'the x-coordinates of the intersections of y = f(x) and y = g(x)', ['the y-intercepts', 'the zeros of f only', 'the vertex of f'], 'Equal y-values.'),
           ('Squaring both sides of √x = x − 2 may introduce', 'an extraneous solution', ['complex solutions', 'no solutions', 'a repeated root'], 'Check in the original.'),
           ('The equation eˣ = −2 has', 'no real solution', ['x = ln(−2)', 'x = −ln 2', 'two solutions'], 'eˣ > 0.'),
           ('A GDC finds solutions of f(x) = 0 as', 'zeros (roots) of the graph of y = f(x)', ['maximum points', 'y-intercepts', 'asymptotes'], 'Intersections with y = 0.')],
    why=[('Explain why solutions obtained by squaring both sides must be checked.', 'Squaring is not reversible: a = b and a = −b both give a² = b², so solutions of the squared equation may not satisfy the original.'),
         ('Explain when a graphical method is preferable to an analytic one.', 'When the equation mixes types (e.g. eˣ = x + 2) there is often no algebraic method, so the intersection is found numerically.'),
         ('Explain why x ln x = 0 has only one solution.', 'x ln x = 0 needs x = 0 or ln x = 0; ln x is undefined at x = 0, so the only solution is x = 1.')],
    misc=[('x² = 5x so x = 5.', 'Dividing by x loses x = 0: x(x − 5) = 0, so x = 0 or 5.'),
          ('√(x + 6) = x gives x² − x − 6 = 0, so x = 3 or x = −2.', 'x = −2 does not satisfy the original (√4 = 2 ≠ −2), so x = 3 only.')],
))


@R.add('ch07-st3', 'C1', (1, 3), 'mcq')
def solve_mcq(rng, slot):
    a = rng.randint(2, 9)
    kind = rng.choice(['ln', 'exp'])
    if kind == 'ln':
        return mcq(rng, f'The solution of ln x = {a} is', f'x = e{sup(a)}', [f'x = {a}e', f'x = ln {a}', f'x = 10{sup(a)}'], 'Exponentiate.')
    return mcq(rng, f'The solution of e^(2x) = {a} is', f'x = (ln {a})/2', [f'x = ln({a}/2)', f'x = 2 ln {a}', f'x = e^({a}/2)'], 'Take ln: 2x = ln a.')


@R.add('ch07-st3', 'C3', (2, 5), 'short', style='p1')
def solve_analytic(rng, slot):
    kind = rng.choice(['root', 'lnsum', 'expquad', 'abs'])
    if kind == 'root':
        r = rng.randint(1, 8)
        c = rng.randint(1, 6)
        # √(x + a) = x − c with x = r + c root, a = r² − c - r ... choose x0
        x0 = c + r
        a = r * r - x0
        other = sp.solve(sp.Eq(x + a, (x - c) ** 2), x)
        ext = [o for o in other if o != x0]
        if not ext or ext[0] - c >= 0:
            return None
        return mk(f'Solve √(x {"+" if a >= 0 else "−"} {abs(a)}) = x − {c}.'.replace(' + 0)', ')'), f'x = {x0}',
                  f'square: x {"+" if a >= 0 else "−"} {abs(a)} = (x − {c})² (M1); quadratic {poly_txt(sp.expand((x - c) ** 2 - x - a))} = 0 (A1); x = {x0}' + (f' or {P(ext[0])}' if ext else '') + f' (A1); reject {P(ext[0]) if ext else "none"} since x − {c} < 0 (R1).', 4)
    if kind == 'lnsum':
        p, q = rng.randint(1, 5), rng.randint(1, 6)
        r = rng.randint(1, 5)
        x0 = r
        rhs = (x0 + p) * (x0 - q) if x0 > q else (x0 + p) * (x0 + q)
        if x0 > q:
            sols = sp.solve((x + p) * (x - q) - rhs, x)
            good = [s_ for s_ in sols if s_ > q]
            return mk(f'Solve ln(x + {p}) + ln(x − {q}) = ln {rhs}.', 'x = ' + ', '.join(P(s_) for s_ in good),
                      f'ln((x + {p})(x − {q})) = ln {rhs} (M1); {poly_txt(sp.expand((x + p) * (x - q) - rhs))} = 0 (A1); solve (A1); reject roots with x ≤ {q} (R1).', 4)
        sols = sp.solve((x + p) * (x + q) - rhs, x)
        good = [s_ for s_ in sols if s_ > -min(p, q)]
        return mk(f'Solve ln(x + {p}) + ln(x + {q}) = ln {rhs}.', 'x = ' + ', '.join(P(s_) for s_ in good),
                  f'log law (M1); {poly_txt(sp.expand((x + p) * (x + q) - rhs))} = 0 (A1); solve (A1); reject the negative root (R1).', 4)
    if kind == 'expquad':
        p, q = rng.sample([1, 2, 3, 4, 5, 6], 2)
        return mk(f'Solve e^(2x) − {p + q}eˣ + {p * q} = 0, giving your answers in exact form.', 'x = ' + ', '.join(('0' if v == 1 else f'ln {v}') for v in sorted([p, q])),
                  f'u = eˣ: u² − {p + q}u + {p * q} = 0 (M1); u = {p}, {q} (A1); x = ln u (A1).', 3)
    a, b, c = rng.randint(1, 4), nz(rng, -6, 6), rng.randint(1, 9)
    s1, s2 = sp.Rational(c - b, a), sp.Rational(-c - b, a)
    return mk(f'Solve |{poly_txt(a * x + b)}| = {c}.', f'x = {P(min(s1, s2))}, x = {P(max(s1, s2))}', f'{poly_txt(a * x + b)} = ±{c} (M1); x = {P(s1)} (A1); x = {P(s2)} (A1).', 3)


@R.add('ch07-st3', 'C3', (2, 4), 'short', style='p2')
def solve_graph(rng, slot):
    pairs = [lambda a: (sp.exp(x) , x + a, f'eˣ = x + {a}'), lambda a: (sp.log(x), x - a, f'ln x = x − {a}'), lambda a: (x ** 3, a * x + 1, f'x³ = {a}x + 1'),
             lambda a: (sp.exp(-x), x ** 2 - a, f'e^(−x) = x² − {a}'), lambda a: (2 ** x, x ** 2 + a - 2, f'2ˣ = x² + {a - 2}'.replace('+ 0', '').replace('+ −', '− ')),
             lambda a: (sp.cos(x), x / a, f'cos x = x/{a}')]
    a = rng.randint(2, 5)
    f, g, txt = rng.choice(pairs)(a)
    lo = 0.001 if f.has(sp.log) else -6
    fl = sp.lambdify(x, f - g, 'math')
    try:
        roots = nsols(fl, lo, 8)
    except (ValueError, OverflowError):
        return None
    if not roots:
        return None
    rt = ', '.join(s3(r_) for r_ in roots)
    return mk(f'Use your GDC to solve {txt}' + (' for x > 0' if f.has(sp.log) else '') + '.', f'x = {rt}', f'graph both sides or y = f(x) − g(x) (M1); {len(roots)} solution{"s" if len(roots) > 1 else ""}: {rt} (A1 A1).', 3)


@R.add('ch07-st3', 'C2', (2, 4), 'explain')
def solve_explain(rng, slot):
    c = rng.randint(1, 6)
    r = rng.randint(1, 6)
    x0 = c + r
    a = r * r - x0
    ext = [o for o in sp.solve(sp.Eq(x + a, (x - c) ** 2), x) if o != x0]
    if not ext or ext[0] - c >= 0:
        return None
    return mk(f'{who(rng)} solves √(x {"+" if a >= 0 else "−"} {abs(a)}) = x − {c} by squaring and obtains x = {x0} and x = {P(ext[0])}. Explain which solution(s) are valid.'.replace(' + 0)', ')'), f'x = {x0} only',
              f'squaring can introduce extraneous roots (R1); check x = {P(ext[0])}: right-hand side {P(ext[0] - c)} < 0, but a square root is non-negative (R1); x = {x0} only (A1).', 3, 'explain')


@R.add('ch07-st3', 'C4', (3, 5), 'multi_step', style='ext')
def solve_parts(rng, slot):
    a, b = rng.randint(2, 5), rng.randint(1, 4)
    parts = [(f'Solve e^(2x) = {a}eˣ, giving your answer in exact form.', f'x = ln {a}', 'divide by eˣ > 0 (M1) A1', 2, True),
             (f'Explain why the solution in (a) is the only one.', 'eˣ ≠ 0, so dividing by eˣ loses no solution', 'R1', 1, True),
             (f'Solve e^(2x) − {a + b}eˣ + {a * b} = 0.', f'x = {"0" if b == 1 else "ln " + str(b)}, x = ln {a}' if a != b else f'x = ln {a}', 'substitution (M1) A1 A1', 3, True),
             (f'Use your GDC to solve e^(2x) = {a + b}eˣ − x.', ', '.join(s3(r_) for r_ in nsols(lambda v: math.exp(2 * v) - (a + b) * math.exp(v) + v, -6, 4)), 'GDC (M1) A1 A1', 3, True),
             ('Explain why an analytic method cannot be used for the equation in (d).', 'the equation mixes eˣ and x terms; no algebraic rearrangement isolates x', 'R1', 1, False)]
    return build_parts(rng, ['This question compares analytic and graphical methods.', 'In this question give exact answers where possible.'], parts, 4)


@R.add('ch07-st2', 'C4', (3, 5), 'multi_step', style='ext')
def log_fn_parts(rng, slot):
    p, q = rng.randint(1, 4), nz(rng, -6, 6)
    c = nz(rng, -3, 3)
    va = sp.Rational(-q, p)
    xi = (sp.exp(-c) - q) / p
    g_lin = rng.choice([1, 2])
    parts = [(f'State the largest possible domain of f.', f'x > {P(va)}', 'A1', 1, True),
             ('Write down the equation of the vertical asymptote of the graph of f.', f'x = {P(va)}', 'A1', 1, True),
             ('Find the exact x-intercept of the graph of f.', f'x = {P(xi)}', 'M1 A1', 2, True),
             ('Find the y-intercept, if it exists, in exact form.', f'{P(sp.log(q) + c)}' if q > 0 else 'none, since x = 0 is not in the domain', 'A1', 1, True),
             ('Find an expression for f⁻¹(x) and state its range.', f'f⁻¹(x) = ' + (lambda nu: nu if p == 1 else f'({nu})/{p}')(f'e^(x {"−" if c > 0 else "+"} {abs(c)}) {"−" if q > 0 else "+"} {abs(q)}') + f'; f⁻¹(x) > {P(va)}', 'M1 A1 A1', 3, True),
             (f'Use your GDC to solve f(x) = {g_lin + 3} − x.', ', '.join(s3(r_) for r_ in nsols(lambda v: math.log(p * v + q) + c - (g_lin + 3) + v, float(va) + 1e-9, 40)) or 'no solution', 'GDC (M1) A1', 2, False)]
    return build_parts(rng, [f'Let f(x) = ln({poly_txt(p * x + q)}) {"+" if c > 0 else "−"} {abs(c)}.', f'The function f is defined by f(x) = ln({poly_txt(p * x + q)}) {"+" if c > 0 else "−"} {abs(c)}.'], parts, 4)


# =============================================================================================
# ch08 Transformations of graphs (SL 2.11; AHL 2.14, 2.16)
# =============================================================================================
TR_DESC = {
    'tx': lambda k: (f'f(x {"−" if k > 0 else "+"} {abs(k)})', f'translation by ({k}, 0)ᵀ', lambda p: (p[0] + k, p[1])),
    'ty': lambda k: (f'f(x) {"+" if k > 0 else "−"} {abs(k)}', f'translation by (0, {k})ᵀ', lambda p: (p[0], p[1] + k)),
    'sy': lambda k: (f'{k}f(x)', f'vertical stretch, scale factor {k}', lambda p: (p[0], p[1] * k)),
    'sx': lambda k: (f'f({k}x)', f'horizontal stretch, scale factor 1/{k}', lambda p: (sp.Rational(p[0], k), p[1])),
    'rx': lambda k: ('−f(x)', 'reflection in the x-axis', lambda p: (p[0], -p[1])),
    'ry': lambda k: ('f(−x)', 'reflection in the y-axis', lambda p: (-p[0], p[1])),
}


R.facts('ch08-st1', F(
    terms=[('translation', 'a transformation that moves every point of a graph by the same vector; y = f(x − h) + k translates y = f(x) by (h, k)ᵀ'),
           ('vertical stretch', 'the transformation y = pf(x), multiplying every y-coordinate by p'),
           ('horizontal stretch', 'the transformation y = f(qx), multiplying every x-coordinate by 1/q'),
           ('reflection', 'the transformation y = −f(x) (reflection in the x-axis) or y = f(−x) (reflection in the y-axis)')],
    facts=[('y = f(x + 3) is a translation of y = f(x) by', '(−3, 0)ᵀ', ['(3, 0)ᵀ', '(0, 3)ᵀ', '(0, −3)ᵀ'], 'Replace x by x + 3.'),
           ('y = f(2x) is a horizontal stretch with scale factor', '1/2', ['2', '−2', '1/4'], 'x-coordinates halve.'),
           ('The point (4, 6) on y = f(x) maps on y = 3f(x) to', '(4, 18)', ['(12, 6)', '(4, 2)', '(4/3, 6)'], 'Multiply y by 3.'),
           ('y = −f(x) is a reflection of y = f(x) in', 'the x-axis', ['the y-axis', 'the line y = x', 'the origin'], 'y changes sign.')],
    why=[('Explain why y = f(x − 2) is a translation 2 units to the right, not to the left.', 'The new graph takes at x the value f had at x − 2, i.e. 2 units earlier, so every feature appears 2 units further right.'),
         ('Explain why the order of transformations can matter.', 'For example y = 2f(x) + 3 (stretch then translate) differs from y = 2(f(x) + 3) = 2f(x) + 6 (translate then stretch).'),
         ('Explain why a horizontal stretch y = f(qx) has scale factor 1/q.', 'A value f(a) now occurs where qx = a, i.e. at x = a/q, so all x-coordinates are multiplied by 1/q.')],
    misc=[('y = f(3x) stretches the graph horizontally by scale factor 3.', 'The scale factor is 1/3: the graph is compressed towards the y-axis.'),
          ('y = f(x) + 4 moves the graph 4 units left.', 'Adding 4 outside f is a vertical translation 4 units up.')],
))


@R.add('ch08-st1', 'C1', (1, 3), 'mcq')
def transf_mcq(rng, slot):
    kind = rng.choice(list(TR_DESC))
    k = nz(rng, -5, 5) if kind in ('tx', 'ty') else rng.randint(2, 5)
    eq, desc, _ = TR_DESC[kind](k)
    wr = [TR_DESC[o](k if o in ('tx', 'ty') else rng.randint(2, 5))[1] for o in TR_DESC if o != kind]
    if kind == 'tx':
        wr[0] = f'translation by ({-k}, 0)ᵀ'
    if kind == 'sx':
        wr[0] = f'horizontal stretch, scale factor {k}'
    rng.shuffle(wr)
    return mcq(rng, f'The graph of y = {eq} is obtained from y = f(x) by a', desc, wr[:3], 'Inside f acts on x (inversely); outside acts on y.')


@R.add('ch08-st1', 'C3', (1, 4), 'short', style='p1')
def transf_point(rng, slot):
    p0 = (nz(rng, -6, 6), nz(rng, -6, 6))
    ks = rng.sample(['tx', 'ty', 'sy', 'sx', 'rx', 'ry'], 2 if slot.d <= 2 else 3)
    pt_ = p0
    descs = []
    eq = 'f(x)'
    for kd in ks:
        k = nz(rng, -4, 4) if kd in ('tx', 'ty') else rng.randint(2, 3)
        _, d_, fn = TR_DESC[kd](k)
        pt_ = fn(pt_)
        descs.append(d_)
    return mk(f'The point A({p0[0]}, {p0[1]}) lies on the graph of y = f(x). The graph is transformed by the following, in order: ' + '; then '.join(descs) + '. Find the image of A.',
              f'({P(pt_[0])}, {P(pt_[1])})', 'apply each transformation to the coordinates in order (M1); ' + ' '.join('(A1)' for _ in ks) + '.', 1 + len(ks))


@R.add('ch08-st1', 'C3', (2, 5), 'short', style='p1')
def transf_equation(rng, slot):
    base, bt = rng.choice([(x ** 2, 'x²'), (x ** 3, 'x³'), (1 / x, '1/x'), (sp.sqrt(x), '√x'), (sp.exp(x), 'eˣ'), (sp.log(x), 'ln x')])
    h, k, a = nz(rng, -4, 4), nz(rng, -5, 5), rng.choice([2, 3, -1, -2, sp.Rational(1, 2)])
    g = a * base.subs(x, x - h) + k
    at = '' if a == 1 else '−' if a == -1 else P(a)
    order = f'a vertical stretch with scale factor {P(abs(a))}' + (' and a reflection in the x-axis' if a < 0 else '') if abs(a) != 1 else 'a reflection in the x-axis'
    desc_q = rng.random() >= 0.5
    return mk(f'The graph of y = {bt} is transformed by {order}, followed by a translation by the vector ({h}, {k})ᵀ. Write down the equation of the new graph.' if not desc_q else
              f'Describe a sequence of transformations that maps the graph of y = {bt} onto the graph of y = {P(g)}.',
              f'y = {P(g)}' if not desc_q else f'{order}, then a translation by ({h}, {k})ᵀ', f'{order} (A1 A1); translation ({h}, {k})ᵀ (A1 A1).', 4)


@R.add('ch08-st1', 'C3', (2, 4), 'short', style='p2')
def transf_gdc(rng, slot):
    a, b = rng.choice([2, 3, 0.5]), rng.randint(1, 4)
    h = nz(rng, -3, 3)
    f = sp.exp(-x ** 2 / 4) * 3 + x / 2
    fl = sp.lambdify(x, f, 'math')
    xs_ = [i / 1000 for i in range(-6000, 6001)]
    xm = max(xs_, key=fl)
    ym = fl(xm)
    return mk(f'Let f(x) = 3e^(−x²/4) + x/2. Use your GDC to find the coordinates of the local maximum of y = f(x), and hence write down the coordinates of the local maximum of y = {a:g}f(x {"−" if h > 0 else "+"} {abs(h)}) + {b}.',
              f'({s3(xm)}, {s3(ym)}); ({s3(xm + h)}, {s3(a * ym + b)})', f'GDC maximum (A1 A1); x shifts by {h} (A1); y = {a:g} × {s3(ym)} + {b} (A1).', 4)


@R.add('ch08-st1', 'C2', (2, 4), 'explain')
def transf_explain(rng, slot):
    k = rng.randint(2, 6)
    return mk(f'{who(rng)} says that the graph of y = f(x + {k}) is the graph of y = f(x) translated {k} units to the right. Explain the error.', f'it is translated {k} units to the left',
              f'f(x + {k}) at x equals f at x + {k} (R1); features occur {k} units earlier in x (R1); translation by ({-k}, 0)ᵀ (A1).', 3, 'explain')


@R.add('ch08-st1', 'C4', (3, 5), 'multi_step', style='ext')
def transf_parts(rng, slot):
    h, k = nz(rng, -3, 3), nz(rng, -4, 4)
    a = rng.choice([2, 3])
    f = x ** 2 - 2 * x  # vertex (1, −1)
    g = sp.expand(a * f.subs(x, x - h) + k)
    vx, vy = 1 + h, -a + k
    parts = [(f'Write down the coordinates of the vertex and the x-intercepts of y = f(x), where f(x) = x² − 2x.', '(1, −1); x = 0, 2', 'A1 A1', 2, True),
             (f'The graph of g is obtained by a vertical stretch scale factor {a} and then a translation by ({h}, {k})ᵀ. Find g(x) in the form ax² + bx + c.', poly_txt(g), 'M1 A1 A1', 3, True),
             ('Find the coordinates of the vertex of g.', f'({vx}, {vy})', 'A1 A1', 2, True),
             ('State the range of g.', f'g(x) ≥ {vy}', 'A1', 1, True),
             ('Explain whether doing the translation first and then the stretch gives the same graph.', f'no: that gives {a}(f(x − {h}) + {k}) = {a}f(x − {h}) + {a * k}', 'R1 A1', 2, False)]
    return build_parts(rng, ['This question is about transformations of a quadratic graph.', 'Let f(x) = x² − 2x.'], parts, 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch08-st2', F(
    terms=[('even function', 'a function with f(−x) = f(x) for all x; its graph is symmetric in the y-axis'),
           ('odd function', 'a function with f(−x) = −f(x) for all x; its graph has rotational symmetry of order 2 about the origin'),
           ('self-inverse function', 'a function for which f(f(x)) = x, so f⁻¹ = f and the graph is symmetric in y = x')],
    facts=[('Which function is even?', 'x⁴ − 3x²', ['x³ + x', 'x² + x', 'eˣ'], 'Only even powers.'),
           ('Which function is odd?', 'x³ − 5x', ['x³ − 5', 'x² + 1', 'cos x'], 'Only odd powers, no constant.'),
           ('f(x) = x² has an inverse if its domain is restricted to', 'x ≥ 0', ['x ∈ ℝ', '−1 ≤ x ≤ 1', 'x ≠ 0'], 'Make it one-to-one.'),
           ('An example of a self-inverse function is', 'f(x) = 5 − x', ['f(x) = 5x', 'f(x) = x²', 'f(x) = x + 5'], 'f(f(x)) = x.')],
    why=[('Explain why the graph of an odd function defined at 0 must pass through the origin.', 'f(−0) = −f(0) gives f(0) = −f(0), so f(0) = 0.'),
         ('Explain why a function must be one-to-one to have an inverse.', 'The inverse must map each output back to a single input; if two inputs share an output, the inverse would not be a function.'),
         ('Explain why most functions are neither odd nor even.', 'The conditions f(−x) = f(x) and f(−x) = −f(x) are special symmetries; e.g. x² + x has f(−x) = x² − x, which is neither f(x) nor −f(x).')],
    misc=[('f(x) = x³ + 1 is odd because x³ is odd.', 'f(−x) = −x³ + 1 ≠ −f(x) = −x³ − 1, so f is neither odd nor even.'),
          ('Every function is either odd or even.', 'Most functions are neither, e.g. eˣ.')],
))


def _oe_fn(rng):
    k = rng.choice(['even', 'odd', 'neither'])
    a, b = nz(rng, -5, 5), nz(rng, -5, 5)
    if k == 'even':
        f = rng.choice([a * x ** 4 + b * x ** 2, a * x ** 2 + b, sp.Integer(a) * sp.cos(x) + x ** 2, a / (x ** 2 + abs(b))])
    elif k == 'odd':
        f = rng.choice([a * x ** 3 + b * x, a * x ** 5 - b * x ** 3, a * sp.sin(x), a * x / (x ** 2 + abs(b))])
    else:
        f = rng.choice([a * x ** 3 + b, a * x ** 2 + b * x, sp.exp(x) + a, a * x ** 3 + b * x ** 2])
    return f, k


@R.add('ch08-st2', 'C1', (1, 3), 'mcq')
def oddeven_mcq(rng, slot):
    f, k = _oe_fn(rng)
    return mcq(rng, f'The function f(x) = {P(f)} is', k, [w for w in ['even', 'odd', 'neither', 'both odd and even'] if w != k][:3], 'Compare f(−x) with f(x) and −f(x).')


@R.add('ch08-st2', 'C3', (2, 4), 'short', style='p1')
def oddeven_show(rng, slot):
    f, k = _oe_fn(rng)
    fm = sp.expand(f.subs(x, -x))
    return mk(f'Determine, showing your working, whether f(x) = {P(f)} is odd, even or neither.', k,
              f'f(−x) = {P(fm)} (M1 A1); compare with f(x) and −f(x) = {P(sp.expand(-f))} (R1); {k} (A1).', 4)


@R.add('ch08-st2', 'C3', (2, 4), 'short', style='p1')
def restrict_domain(rng, slot):
    h, k = nz(rng, -5, 5), nz(rng, -6, 6)
    a = rng.choice([1, 2, -1])
    e = sp.expand(a * (x - h) ** 2 + k)
    side = rng.choice(['≥', '≤'])
    sign = '+' if (side == '≥') else '−'
    inv = f'{h} {sign} √({"x " + ("−" if k > 0 else "+") + " " + str(abs(k)) if a == 1 else ("(x " + ("−" if k > 0 else "+") + " " + str(abs(k)) + ")/" + str(a) if a > 0 else "(" + str(k) + " − x)" if a == -1 else "")})'.replace('√()', '')
    if a == -1:
        inv = f'{h} {sign} √({k} − x)'
    dom = f'x {"≥" if a > 0 else "≤"} {k}'
    return mk(f'The function f(x) = {poly_txt(e)} is defined for x {side} c. Find the least value of c (if x ≥ c) or greatest value of c (if x ≤ c) for which f has an inverse, and find f⁻¹(x) for that domain, stating its domain.'.replace('least value of c (if x ≥ c) or greatest value of c (if x ≤ c)', 'least value of c' if side == '≥' else 'greatest value of c'),
              f'c = {h}; f⁻¹(x) = {inv}, {dom}'.replace('+ −', '− '), f'vertex at x = {h} so c = {h} (A1); complete the square (M1); choose the {"positive" if sign == "+" else "negative"} root (R1); f⁻¹ and domain (A1 A1).', 5)


@R.add('ch08-st2', 'C2', (2, 4), 'explain')
def oddeven_explain(rng, slot):
    a, b = nz(rng, -5, 5), nz(rng, -6, 6)
    return mk(f'{who(rng)} says f(x) = {P(a * x ** 3 + b)} is odd because it contains x³. Explain whether this is correct.', 'incorrect: neither odd nor even',
              f'f(−x) = {P(-a * x ** 3 + b)} (A1); −f(x) = {P(-a * x ** 3 - b)} ≠ f(−x) because of the constant (R1); also f(−x) ≠ f(x), so neither (R1).', 3, 'explain')


@R.add('ch08-st2', 'C4', (3, 5), 'multi_step', style='ext')
def oddeven_parts(rng, slot):
    a, b = rng.randint(1, 4), rng.randint(1, 9)
    f = a * x / (x ** 2 + b)
    g = x ** 2 + b
    parts = [(f'Show that f(x) = {P(f)} is an odd function.', f'f(−x) = {P(f.subs(x, -x))} = −f(x)', 'M1 A1', 2, True),
             (f'Show that g(x) = {poly_txt(g)} is an even function.', 'g(−x) = g(x)', 'A1', 1, True),
             ('Determine whether the product f(x)g(x) is odd, even or neither.', 'odd', 'M1 A1', 2, True),
             ('Prove that the product of two odd functions is even.', 'h(−x) = (−p(x))(−q(x)) = p(x)q(x)', 'M1 A1', 2, True),
             (f'Given ∫₀² f(x) dx = k, write down ∫ from −2 to 2 of f(x) dx.', '0', 'odd symmetry (R1) A1', 2, False)]
    return build_parts(rng, ['This question is about odd and even functions.', 'In this question all functions have domain ℝ.'], parts, 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch08-st3', F(
    terms=[('graph of y = |f(x)|', 'the graph of y = f(x) with every part below the x-axis reflected in the x-axis'),
           ('graph of y = f(|x|)', 'the part of y = f(x) for x ≥ 0, together with its reflection in the y-axis'),
           ('graph of y = 1/f(x)', 'the reciprocal graph: zeros of f become vertical asymptotes, and points with f = ±1 are invariant'),
           ('graph of y = [f(x)]²', 'the squared graph: non-negative, touching the x-axis at the zeros of f')],
    facts=[('The graph of y = |f(x)| lies', 'on or above the x-axis', ['on or to the right of the y-axis', 'below the x-axis', 'above y = 1'], '|f(x)| ≥ 0.'),
           ('Where f(x) = 0, the graph of y = 1/f(x) has', 'a vertical asymptote', ['a zero', 'a maximum', 'a horizontal asymptote'], '1/0 is undefined.'),
           ('The graph of y = f(|x|) is always', 'symmetric in the y-axis', ['symmetric in the x-axis', 'above the x-axis', 'odd'], 'f(|−x|) = f(|x|).'),
           ('A local maximum of f with f > 0 becomes, on y = 1/f(x),', 'a local minimum', ['a local maximum', 'an asymptote', 'a zero'], 'Reciprocal reverses order for positive values.')],
    why=[('Explain why points where f(x) = 1 or f(x) = −1 lie on both y = f(x) and y = 1/f(x).', 'At such points 1/f(x) = 1/1 = 1 or 1/(−1) = −1, which equal f(x).'),
         ('Explain why y = [f(x)]² touches rather than crosses the x-axis at a zero of f.', '[f(x)]² ≥ 0 for all x and equals 0 at the zero, so the graph meets the axis at a minimum point without becoming negative.'),
         ('Explain why the graphs of y = f(|x|) and y = |f(x)| are generally different.', 'f(|x|) reflects the right-hand half in the y-axis (changing x), while |f(x)| reflects negative y-values in the x-axis (changing y).')],
    misc=[('y = |x − 3| has a vertical asymptote at x = 3.', 'It has a vertex (minimum) at (3, 0); there is no asymptote.'),
          ('As f(x) → ∞, 1/f(x) → ∞.', '1/f(x) → 0 as f(x) → ∞, giving a horizontal asymptote y = 0.')],
))


@R.add('ch08-st3', 'C1', (1, 3), 'mcq')
def modrecip_mcq(rng, slot):
    p, q = sorted(rng.sample(range(-6, 7), 2))
    f = f'(x {"−" if p > 0 else "+"} {abs(p)})(x {"−" if q > 0 else "+"} {abs(q)})'.replace('(x + 0)', 'x').replace('(x − 0)', 'x')
    return mcq(rng, f'The vertical asymptotes of y = 1/({f}) are', f'x = {p} and x = {q}', [f'x = {-p} and x = {-q}', f'y = {p} and y = {q}', f'x = {P(sp.Rational(p + q, 2))} only'], 'Zeros of the denominator.')


@R.add('ch08-st3', 'C3', (2, 4), 'short', style='p1')
def modulus_graph(rng, slot):
    kind = rng.choice(['abs', 'fabs', 'solve'])
    p, q = sorted(rng.sample(range(-5, 6), 2))
    e = sp.expand((x - p) * (x - q))
    if kind == 'abs':
        h = sp.Rational(p + q, 2)
        return mk(f'Let f(x) = {poly_txt(e)}. Sketch y = |f(x)| and state the coordinates of its local maximum and of the points where it meets the x-axis.', f'({P(h)}, {P(-e.subs(x, h))}); ({p}, 0), ({q}, 0)',
                  f'reflect the part between {p} and {q} in the x-axis (M1); vertex ({P(h)}, {P(e.subs(x, h))}) becomes a maximum ({P(h)}, {P(-e.subs(x, h))}) (A1); zeros unchanged (A1).', 3)
    if kind == 'fabs':
        ro = [r_ for r_ in (p, q) if r_ > 0]
        xs_ = sorted(set([r_ for r_ in ro] + [-r_ for r_ in ro]))
        return mk(f'Let f(x) = {poly_txt(e)}. Find the x-intercepts and the y-intercept of the graph of y = f(|x|).', ('x = ' + ', '.join(str(v) for v in xs_)) + f'; y = {e.subs(x, 0)}' if xs_ else f'no x-intercepts; y = {e.subs(x, 0)}',
                  f'keep the part with x ≥ 0 (M1); reflect it in the y-axis (M1); intercepts (A1).', 3)
    a, b, c = rng.randint(1, 4), nz(rng, -6, 6), rng.randint(1, 9)
    s1, s2 = sp.Rational(c - b, a), sp.Rational(-c - b, a)
    r1, r2_ = sorted([s1, s2])
    return mk(f'Solve |{poly_txt(a * x + b)}| < {c}.', f'{P(r1)} < x < {P(r2_)}', f'−{c} < {poly_txt(a * x + b)} < {c} (M1); {P(r1)} < x < {P(r2_)} (A1 A1).', 3)


@R.add('ch08-st3', 'C3', (2, 5), 'short', style='p1')
def recip_graph(rng, slot):
    p, q = sorted(rng.sample(range(-5, 6), 2))
    e = sp.expand((x - p) * (x - q))
    h = sp.Rational(p + q, 2)
    k = e.subs(x, h)
    inv = [r_ for r_ in sp.solve(e - 1, x) + sp.solve(e + 1, x) if r_.is_real]
    return mk(f'Let f(x) = {poly_txt(e)}. For the graph of y = 1/f(x), state the equations of the asymptotes, the y-intercept and the coordinates of the local maximum.',
              f'x = {p}, x = {q}, y = 0; {"(0, " + P(1 / e.subs(x, 0)) + ")" if e.subs(x, 0) != 0 else "no y-intercept"}; ({P(h)}, {P(1 / k)})',
              f'zeros of f give vertical asymptotes (A1 A1); f → ∞ gives y = 0 (A1); minimum ({P(h)}, {P(k)}) of f becomes maximum of 1/f (M1 A1).', 5)


@R.add('ch08-st3', 'C3', (2, 4), 'short', style='p2')
def modrecip_gdc(rng, slot):
    a, b = rng.randint(1, 3), rng.randint(2, 6)
    f = x ** 3 - a * b * x + 1
    fl = sp.lambdify(x, f, 'math')
    k = rng.randint(1, 4)
    roots = nsols(lambda v: abs(fl(v)) - k, -6, 6)
    return mk(f'Let f(x) = {poly_txt(f)}. Use your GDC to solve |f(x)| = {k}.', 'x = ' + ', '.join(s3(r_) for r_ in roots), f'f(x) = ±{k} (M1); graph y = |f(x)| and y = {k} (M1); all {len(roots)} solutions (A1 A1).', 4)


@R.add('ch08-st3', 'C2', (2, 4), 'explain')
def modrecip_explain(rng, slot):
    p = rng.randint(1, 6)
    return mk(f'Explain why the graph of y = 1/(x² + {p}) has no vertical asymptotes, and find its maximum value.', f'1/{p}',
              f'x² + {p} ≥ {p} > 0, so the denominator is never zero (R1); 1/f is largest where f is smallest (R1); at x = 0, y = 1/{p} (A1).', 3, 'explain')


@R.add('ch08-st3', 'C4', (3, 5), 'multi_step', style='ext')
def modrecip_parts(rng, slot):
    p, q = sorted(rng.sample(range(-4, 6), 2))
    e = sp.expand((x - p) * (x - q))
    h = sp.Rational(p + q, 2)
    k = e.subs(x, h)
    c0 = e.subs(x, 0)
    parts = [(f'Sketch y = f(x), showing the intercepts and the vertex.', f'({p}, 0), ({q}, 0), (0, {c0}); vertex ({P(h)}, {P(k)})', 'A1 A1 A1', 3, True),
             ('Sketch y = |f(x)| and state its range.', 'y ≥ 0', 'M1 A1', 2, True),
             ('Sketch y = 1/f(x), stating the equations of all asymptotes.', f'x = {p}, x = {q}, y = 0', 'A1 A1 A1', 3, True),
             (f'State the coordinates of the turning point of y = 1/f(x).', f'({P(h)}, {P(1 / k)})', 'A1', 1, True),
             ('Sketch y = [f(x)]² and state the coordinates of its local maximum.', f'({P(h)}, {P(k ** 2)})', 'A1', 1, False),
             (f'Sketch y = f(|x|) and state the number of x-intercepts.', str(len(set([abs(r_) for r_ in (p, q) if r_ > 0] + [-r_ for r_ in (p, q) if r_ > 0]))), 'A1', 1, False)]
    return build_parts(rng, [f'Let f(x) = {poly_txt(e)}.', f'The function f is defined by f(x) = {poly_txt(e)}, x ∈ ℝ.'], parts, 4)


BASES = [(x ** 2, 'x²'), (x ** 3, 'x³'), (sp.sqrt(x), '√x'), (1 / x, '1/x'), (sp.exp(x), 'eˣ'), (sp.log(x), 'ln x'), (2 ** x, '2ˣ'), (1 / x ** 2, '1/x²')]


@R.add('ch08-st1', 'C4', (3, 5), 'multi_step', style='ext')
def transf_parts2(rng, slot):
    base, bt = rng.choice(BASES)
    h, k = nz(rng, -4, 4), nz(rng, -5, 5)
    a = rng.choice([2, 3, -1, -2, sp.Rational(1, 2)])
    b = rng.choice([2, 3])
    g = a * base.subs(x, x - h) + k
    gt = P(g)
    p0 = rng.choice([(1, base.subs(x, 1)), (4, base.subs(x, 4)), (2, base.subs(x, 2))])
    img = (p0[0] + h, a * p0[1] + k)
    asym = {'1/x': f'x = {h}, y = {k}', '1/x²': f'x = {h}, y = {k}', 'eˣ': f'y = {k}', '2ˣ': f'y = {k}', 'ln x': f'x = {h}', '√x': 'none', 'x²': 'none', 'x³': 'none'}[bt]
    parts = [(f'Describe a sequence of two transformations that maps y = {bt} onto y = {gt}.', (f'vertical stretch scale factor {P(abs(a))}' if abs(a) != 1 else '') + (' and reflection in the x-axis' if a < 0 else '') + f'; translation ({h}, {k})ᵀ', 'A1 A1 A1', 3, True),
             (f'The point ({p0[0]}, {P(p0[1])}) lies on y = {bt}. Find its image on y = g(x).', f'({P(img[0])}, {P(img[1])})', 'A1 A1', 2, True),
             ('State the equations of any asymptotes of y = g(x).', asym, 'A1', 1, True),
             (f'The graph of g is then stretched horizontally with scale factor 1/{b}. Write down the equation of the resulting graph.', f'y = {P(g.subs(x, b * x))}', 'M1 A1', 2, False),
             (f'Find the y-intercept of y = g(x), if it exists.', P(g.subs(x, 0)) if g.subs(x, 0).is_real and g.subs(x, 0).is_finite else 'none', 'A1', 1, False)]
    return build_parts(rng, [f'Let g(x) = {gt}.', f'The function g is defined by g(x) = {gt}, where g is a transformation of y = {bt}.'], parts, 4)


@R.add('ch08-st1', 'C4', (3, 5), 'multi_step', style='ext')
def transf_parts3(rng, slot):
    pts = [(nz(rng, -5, 5), nz(rng, -5, 5)) for _ in range(3)]
    pts = sorted(set(pts))
    if len(pts) < 3:
        return None
    k, s_ = nz(rng, -4, 4), rng.choice([2, 3])
    nm = ['A', 'B', 'C']
    desc = ', '.join(f'{n}{p}' for n, p in zip(nm, pts))
    parts = [(f'Find the images of A, B and C on y = f(x − {abs(k)}).' if k > 0 else f'Find the images of A, B and C on y = f(x + {abs(k)}).', ', '.join(str((p[0] + k, p[1])) for p in pts), 'A1 A1', 2, True),
             (f'Find the images of A, B and C on y = {s_}f(x).', ', '.join(str((p[0], s_ * p[1])) for p in pts), 'A1', 1, True),
             (f'Find the images of A, B and C on y = f({s_}x).', ', '.join(f'({P(sp.Rational(p[0], s_))}, {p[1]})' for p in pts), 'A1 A1', 2, True),
             ('Find the images of A, B and C on y = −f(−x).', ', '.join(str((-p[0], -p[1])) for p in pts), 'A1', 1, True),
             (f'The graph of y = f(x) is mapped onto y = {s_}f(x) {"+" if k > 0 else "−"} {abs(k)}. Find which of A, B, C (if any) is invariant.', ', '.join(n for n, p in zip(nm, pts) if s_ * p[1] + k == p[1]) or 'none', 'M1 A1', 2, False)]
    return build_parts(rng, [f'The graph of y = f(x) passes through the points {desc}.', f'The points {desc} lie on the graph of y = f(x).'], parts, 4)


@R.add('ch08-st1', 'C2', (2, 4), 'explain')
def stretch_explain(rng, slot):
    k = rng.randint(2, 5)
    p0 = (nz(rng, -6, 6) * k, nz(rng, -6, 6))
    return mk(f'The point ({p0[0]}, {p0[1]}) lies on y = f(x). Explain why its image on y = f({k}x) is ({P(sp.Rational(p0[0], k))}, {p0[1]}) and not ({p0[0] * k}, {p0[1]}).', f'({P(sp.Rational(p0[0], k))}, {p0[1]})',
              f'f({k}x) takes the value f({p0[0]}) when {k}x = {p0[0]} (R1); i.e. at x = {P(sp.Rational(p0[0], k))} (A1); horizontal stretch with scale factor 1/{k} (R1).', 3, 'explain')


@R.add('ch08-st2', 'C4', (3, 5), 'multi_step', style='ext')
def restrict_parts(rng, slot):
    h, k = nz(rng, -4, 4), nz(rng, -6, 6)
    a = rng.choice([1, 2, 3])
    e = sp.expand(a * (x - h) ** 2 + k)
    v = h + rng.randint(1, 4)
    fv = e.subs(x, v)
    inv = f'{h} + √(x {"−" if k > 0 else "+"} {abs(k)})' if a == 1 else f'{h} + √((x {"−" if k > 0 else "+"} {abs(k)})/{a})'
    parts = [(f'Write f(x) = {poly_txt(e)} in the form a(x − h)² + k.', vform(a, h, k), 'M1 A1', 2, True),
             ('Explain why f does not have an inverse on ℝ.', 'f is not one-to-one, e.g. symmetric about the axis of symmetry', 'R1', 1, True),
             (f'The domain of f is restricted to x ≥ c. Find the least value of c for which f⁻¹ exists.', f'c = {h}', 'A1', 1, True),
             ('For this domain, find f⁻¹(x) and state its domain.', f'f⁻¹(x) = {inv}'.replace('+ −', '− ') + f', x ≥ {k}', 'M1 A1 A1', 3, True),
             (f'Find f⁻¹({P(fv)}).', str(v), 'A1', 1, True),
             ('Determine whether f is odd, even or neither on ℝ.', 'even' if h == 0 else 'neither', 'R1', 1, False)]
    return build_parts(rng, [f'Let f(x) = {poly_txt(e)}, x ∈ ℝ.', 'This question is about restricting a domain so that an inverse exists.'], parts, 4)


@R.add('ch08-st2', 'C4', (3, 5), 'multi_step', style='ext')
def selfinv_parts(rng, slot):
    a = nz(rng, -6, 6)
    c = rng.randint(1, 9)
    kind = rng.choice(['lin', 'rat'])
    if kind == 'lin':
        f = f'{a} − x'
        parts = [(f'Show that f(f(x)) = x for f(x) = {a} − x.', f'f({a} − x) = {a} − ({a} − x) = x', 'M1 A1', 2, True),
                 ('Hence write down f⁻¹(x).', f'{a} − x', 'A1', 1, True),
                 ('Describe the symmetry of the graph of y = f(x).', 'symmetric in the line y = x (it is perpendicular to y = x)', 'R1', 1, True),
                 (f'Find the point where y = f(x) meets y = x.', f'({P(sp.Rational(a, 2))}, {P(sp.Rational(a, 2))})', 'A1', 1, True),
                 ('Determine whether f is odd, even or neither.', 'odd' if a == 0 else 'neither', 'R1', 1, False)]
        return build_parts(rng, [f'Let f(x) = {a} − x.'.replace('0 − x', '−x'), 'This question is about self-inverse functions.'], parts, 3)
    parts = [(f'Show that f(x) = (x + {c})/(x − 1), x ≠ 1, satisfies f(f(x)) = x.', 'shown', 'M1 A1 A1', 3, True),
             ('Hence state f⁻¹ and its domain.', 'f⁻¹(x) = f(x), x ≠ 1', 'A1 A1', 2, True),
             ('Find the coordinates of the points where y = f(x) meets y = x.', f'x = 1 ± √{1 + c}'.replace(f'√{1 + c}', P(sp.sqrt(1 + c))), 'M1 A1', 2, True),
             ('Write down the equations of the asymptotes and explain how they show the self-inverse property.', 'x = 1 and y = 1: reflecting in y = x swaps them', 'A1 R1', 2, True),
             ('Determine whether f is odd, even or neither.', 'neither', 'R1', 1, False)]
    return build_parts(rng, [f'Let f(x) = (x + {c})/(x − 1), x ≠ 1.', 'This question is about self-inverse functions.'], parts, 4)


@R.add('ch08-st3', 'C4', (3, 5), 'multi_step', style='ext')
def modrecip_parts2(rng, slot):
    a, b = rng.randint(1, 4), nz(rng, -8, 8)
    f = a * x + b
    r = sp.Rational(-b, a)
    k = rng.randint(1, 6)
    s1, s2 = sorted([sp.Rational(k - b, a), sp.Rational(-k - b, a)])
    parts = [(f'Sketch y = |f(x)|, stating the coordinates of the vertex and the y-intercept.', f'({P(r)}, 0); (0, {abs(b)})', 'A1 A1', 2, True),
             (f'Solve |f(x)| = {k}.', f'x = {P(s1)}, {P(s2)}', 'M1 A1 A1', 3, True),
             (f'Hence solve |f(x)| > {k}.', f'x < {P(s1)} or x > {P(s2)}', 'R1 A1', 2, True),
             ('Sketch y = 1/f(x), stating its asymptotes.', f'x = {P(r)}, y = 0', 'A1 A1', 2, True),
             (f'Sketch y = f(|x|) and find the x-intercepts, if any.', ('x = ±' + P(r)) if r > 0 else 'none', 'A1 A1', 2, False),
             (f'Find the points that lie on both y = f(x) and y = 1/f(x).', ', '.join(f'({P(v)}, {P(f.subs(x, v))})' for v in sorted([sp.Rational(1 - b, a), sp.Rational(-1 - b, a)])), 'f(x) = ±1 (M1) A1', 2, False)]
    return build_parts(rng, [f'Let f(x) = {poly_txt(f)}.', f'The function f is defined by f(x) = {poly_txt(f)}, x ∈ ℝ.'], parts, 4)


@R.add('ch08-st3', 'C4', (3, 5), 'multi_step', style='ext')
def modrecip_parts3(rng, slot):
    r1, r2_, r3_ = sorted(rng.sample(range(-4, 5), 3))
    e = sp.expand((x - r1) * (x - r2_) * (x - r3_))
    parts = [(f'Write down the zeros of f.', f'{r1}, {r2_}, {r3_}', 'A1', 1, True),
             ('Sketch y = |f(x)| and state the intervals on which |f(x)| = −f(x).', f'x ≤ {r1} or {r2_} ≤ x ≤ {r3_}', 'A1 A1', 2, True),
             ('Write down the equations of the vertical asymptotes of y = 1/f(x).', f'x = {r1}, x = {r2_}, x = {r3_}', 'A1', 1, True),
             ('Sketch y = [f(x)]² and state the number of local minima.', '3', 'A1', 1, True),
             ('Sketch y = f(|x|) and state the number of x-intercepts.', str(len(set([abs(v) for v in (r1, r2_, r3_) if v > 0] + [-v for v in (r1, r2_, r3_) if v > 0] + ([0] if 0 in (r1, r2_, r3_) else [])))), 'A1', 1, False),
             (f'Use your GDC to find the local maximum value of y = [f(x)]² between {r1} and {r2_}.', s3(max(float(e.subs(x, r1 + (r2_ - r1) * i / 2000)) ** 2 for i in range(2001))), 'A1', 1, False)]
    return build_parts(rng, [f'Let f(x) = {poly_txt(e)}.', f'The cubic function f(x) = {poly_txt(e)} is given.'], parts, 4)


@R.add('ch08-st3', 'C2', (2, 4), 'explain')
def modabs_explain(rng, slot):
    p, q = sorted(rng.sample(range(-6, 7), 2))
    e = sp.expand((x - p) * (x - q))
    if abs(e.subs(x, -abs(p) - 1)) == e.subs(x, abs(p) + 1):
        return None
    return mk(f'For f(x) = {poly_txt(e)}, explain why the graphs of y = |f(x)| and y = f(|x|) are different, giving one point that lies on one graph but not the other.', f'e.g. x = {-abs(p) - 1}: |f| = {abs(e.subs(x, -abs(p) - 1))}, f(|x|) = {e.subs(x, abs(p) + 1)}',
              f'|f(x)| reflects negative y-values in the x-axis (R1); f(|x|) reflects the x ≥ 0 part in the y-axis (R1); a correct distinguishing point (A1).', 3, 'explain')


# =============================================================================================
# ch09 Polynomials, rational functions, inequalities, partial fractions, systems (AHL 1.11, 1.16, 2.12–2.13, 2.15)
# =============================================================================================
R.facts('ch09-st1', F(
    terms=[('factor theorem', 'the result that (x − a) is a factor of a polynomial p(x) if and only if p(a) = 0'),
           ('remainder theorem', 'the result that the remainder when p(x) is divided by (x − a) is p(a), and by (ax − b) is p(b/a)'),
           ('sum and product of roots', 'for aₙxⁿ + aₙ₋₁xⁿ⁻¹ + … + a₀ = 0 the roots have sum −aₙ₋₁/aₙ and product (−1)ⁿa₀/aₙ'),
           ('degree of a polynomial', 'the highest power of x with a non-zero coefficient')],
    facts=[('The remainder when x³ − 2x + 5 is divided by (x − 2) is', '9', ['5', '1', '−9'], 'p(2) = 8 − 4 + 5.'),
           ('If (x + 3) is a factor of p(x) then', 'p(−3) = 0', ['p(3) = 0', 'p(0) = 3', 'p(−3) = 3'], 'Factor theorem.'),
           ('The sum of the roots of 2x³ − 5x² + x − 7 = 0 is', '5/2', ['−5/2', '7/2', '−1/2'], '−b/a.'),
           ('The product of the roots of x³ + 4x² − x + 6 = 0 is', '−6', ['6', '−4', '1/6'], '(−1)³ × 6/1.')],
    why=[('Explain why the remainder when p(x) is divided by (x − a) equals p(a).', 'Write p(x) = (x − a)q(x) + r with r constant; substituting x = a gives p(a) = 0 × q(a) + r = r.'),
         ('Explain why a polynomial of degree n has at most n real roots.', 'Each real root a gives a factor (x − a); the product of more than n linear factors would have degree greater than n.'),
         ('Explain how the sum of the roots of ax² + bx + c = 0 follows from the factorised form.', 'a(x − α)(x − β) = ax² − a(α + β)x + aαβ; comparing coefficients gives α + β = −b/a and αβ = c/a.')],
    misc=[('The remainder when p(x) is divided by (2x − 1) is p(2).', 'The remainder is p(1/2), the value making 2x − 1 zero.'),
          ('For x³ − 6x² + 11x − 6 = 0, the product of the roots is −6.', 'For a cubic the product is −d/a = 6.')],
))


def _cubic(rng, monic=True):
    rs = sorted(rng.sample(range(-5, 6), 3))
    a = 1 if monic else rng.choice([1, 2, -1])
    return rs, a, sp.expand(a * (x - rs[0]) * (x - rs[1]) * (x - rs[2]))


@R.add('ch09-st1', 'C1', (1, 3), 'mcq')
def rem_mcq(rng, slot):
    c = [nz(rng, -5, 5)] + [rng.randint(-6, 6) for _ in range(3)]
    p_ = c[0] * x ** 3 + c[1] * x ** 2 + c[2] * x + c[3]
    a = nz(rng, -3, 3)
    r = p_.subs(x, a)
    return mcq(rng, f'The remainder when {poly_txt(p_)} is divided by (x {"−" if a > 0 else "+"} {abs(a)}) is', str(r), [str(p_.subs(x, -a)), str(c[3]), str(r + c[0])] if p_.subs(x, -a) != r else [str(r + 1), str(c[3]) if c[3] != r else str(r - 2), str(-r) if r else '1'], f'p({a}).')


@R.add('ch09-st1', 'C3', (2, 5), 'short', style='p1')
def factor_thm(rng, slot):
    kind = rng.choice(['factorise', 'findk', 'twoparams'])
    rs, a, p_ = _cubic(rng)
    if kind == 'factorise':
        return mk(f'Show that (x {"−" if rs[0] > 0 else "+"} {abs(rs[0])}) is a factor of p(x) = {poly_txt(p_)}, and hence factorise p(x) completely.'.replace('(x + 0)', 'x').replace('(x − 0)', 'x'),
                  ''.join(f'(x {"−" if r_ > 0 else "+"} {abs(r_)})' if r_ else 'x' for r_ in rs),
                  f'p({rs[0]}) = 0 (M1 A1); divide or compare coefficients (M1); quadratic factor (A1); fully factorised (A1).', 5)
    if kind == 'findk':
        k = p_.coeff(x, 1)
        q = p_ - k * x
        return mk(f'Given that (x {"−" if rs[1] > 0 else "+"} {abs(rs[1])}) is a factor of p(x) = {poly_txt(q)} + kx, find the value of k.'.replace('(x + 0)', 'x').replace('(x − 0)', 'x').replace('+ 0 + kx', '+ kx'),
                  f'k = {k}' if rs[1] != 0 else 'k can be any value', f'p({rs[1]}) = 0 (M1); {q.subs(x, rs[1])} + {rs[1]}k = 0 (A1); k = {k} (A1).', 3) if rs[1] != 0 else None
    b, c = p_.coeff(x, 2), p_.coeff(x, 1)
    d0 = p_.coeff(x, 0)
    if d0 == 0:
        return None
    r = rng.choice([v for v in range(-3, 4) if v not in rs and v != 0])
    rem = p_.subs(x, r)
    return mk(f'The polynomial p(x) = x³ + ax² + bx {"+" if d0 >= 0 else "−"} {abs(d0)} has a factor (x {"−" if rs[0] > 0 else "+"} {abs(rs[0])}) and leaves a remainder of {rem} when divided by (x {"−" if r > 0 else "+"} {abs(r)}). Find a and b.'.replace('(x + 0)', 'x').replace('(x − 0)', 'x'),
              f'a = {b}, b = {c}', f'p({rs[0]}) = 0 (M1 A1); p({r}) = {rem} (M1 A1); solve simultaneously (M1); a = {b}, b = {c} (A1).', 6)


@R.add('ch09-st1', 'C3', (2, 5), 'short', style='p1')
def roots_sum_prod(rng, slot):
    kind = rng.choice(['sp', 'new', 'quartic'])
    if kind == 'sp':
        c = [nz(rng, -5, 5)] + [rng.randint(-9, 9) for _ in range(3)]
        c[3] = c[3] or 1
        p_ = sum(ci * x ** (3 - i) for i, ci in enumerate(c))
        return mk(f'For the equation {poly_txt(p_)} = 0, find the sum and the product of the roots.', f'sum {P(sp.Rational(-c[1], c[0]))}; product {P(sp.Rational(-c[3], c[0]))}',
                  f'sum = −a₂/a₃ = {P(sp.Rational(-c[1], c[0]))} (A1); product = (−1)³a₀/a₃ = {P(sp.Rational(-c[3], c[0]))} (M1 A1).', 3)
    if kind == 'quartic':
        c = [nz(rng, -4, 4)] + [rng.randint(-9, 9) for _ in range(4)]
        c[4] = c[4] or 2
        p_ = sum(ci * x ** (4 - i) for i, ci in enumerate(c))
        return mk(f'For the equation {poly_txt(p_)} = 0, find the sum and the product of the roots.', f'sum {P(sp.Rational(-c[1], c[0]))}; product {P(sp.Rational(c[4], c[0]))}',
                  f'sum −a₃/a₄ (A1); product (−1)⁴a₀/a₄ = {P(sp.Rational(c[4], c[0]))} (M1 A1).', 3)
    a, b, c = rng.randint(1, 4), rng.randint(-9, 9), nz(rng, -9, 9)
    S, Pr = sp.Rational(-b, a), sp.Rational(c, a)
    k = rng.choice([2, 3])
    newS, newP = k * S, k * k * Pr
    return mk(f'The roots of {poly_txt(a * x ** 2 + b * x + c)} = 0 are α and β. Find a quadratic equation with integer coefficients whose roots are {k}α and {k}β.', poly_txt(sp.expand(a * (x ** 2 - newS * x + newP))) + ' = 0',
              f'α + β = {P(S)}, αβ = {P(Pr)} (A1); new sum {P(newS)}, new product {P(newP)} (M1 A1); equation (A1).', 4)


@R.add('ch09-st1', 'C3', (2, 4), 'short', style='p2')
def poly_gdc(rng, slot):
    c = [rng.choice([1, 2, -1])] + [rng.randint(-6, 6) for _ in range(2)] + [rng.randint(-9, 9) + 0.5]
    p_ = sum(sp.nsimplify(ci) * x ** (3 - i) for i, ci in enumerate(c))
    roots = nsols(sp.lambdify(x, p_, 'math'), -12, 12)
    if not roots:
        return None
    S = -c[1] / c[0]
    return mk(f'Use your GDC to find the real roots of {P(p_)} = 0.' + (' Verify that their sum equals −a₂/a₃ if all roots are real.' if len(roots) == 3 else ''), ', '.join(s3(r_) for r_ in roots),
              f'GDC zeros (M1) (A1 A1)' + (f'; sum {s3(sum(roots))} = {s3(S)} (R1).' if len(roots) == 3 else '.'), 4 if len(roots) == 3 else 3)


@R.add('ch09-st1', 'C2', (2, 4), 'explain')
def factor_explain(rng, slot):
    a = nz(rng, -5, 5)
    b = rng.randint(2, 5)
    return mk(f'{who(rng)} says that to find the remainder when p(x) is divided by ({b}x {"−" if a > 0 else "+"} {abs(a)}) you calculate p({a}). Explain the error.', f'calculate p({P(sp.Rational(a, b))})',
              f'remainder theorem uses the root of the divisor (R1); {b}x − {a} = 0 at x = {P(sp.Rational(a, b))} (A1); so the remainder is p({P(sp.Rational(a, b))}) (R1).'.replace('− −', '+ '), 3, 'explain')


@R.add('ch09-st1', 'C4', (3, 5), 'multi_step', style='ext')
def poly_parts(rng, slot):
    rs, a, p_ = _cubic(rng)
    r0 = rs[rng.randrange(3)]
    other = [r_ for r_ in rs if r_ != r0]
    q = rng.choice([v for v in range(-4, 5) if v not in rs])
    parts = [(f'Show that x = {r0} is a root of p(x) = 0.', f'p({r0}) = 0', 'M1 A1', 2, True),
             ('Hence find the other roots.', f'{other[0]}, {other[1]}', 'division (M1) A1 A1', 3, True),
             (f'Find the remainder when p(x) is divided by (x {"−" if q > 0 else "+"} {abs(q)}).'.replace('(x + 0)', 'x').replace('(x − 0)', 'x'), str(p_.subs(x, q)), 'A1', 1, True),
             ('Verify that the sum and product of the roots agree with the coefficients of p.', f'sum {sum(rs)}; product {rs[0] * rs[1] * rs[2]}', 'A1 A1', 2, True),
             ('Solve p(x) > 0.', f'{rs[0]} < x < {rs[1]} or x > {rs[2]}', 'sign diagram (M1) A1', 2, False)]
    return build_parts(rng, [f'Let p(x) = {poly_txt(p_)}.', f'Consider the cubic polynomial p(x) = {poly_txt(p_)}.'], parts, 4)


@R.add('ch09-st1', 'C4', (4, 5), 'multi_step', style='p3')
def roots_p3(rng, slot):
    a, d = rng.randint(1, 4), rng.randint(1, 3)
    # roots in arithmetic progression a−d, a, a+d
    rs = [a - d, a, a + d]
    p_ = sp.expand((x - rs[0]) * (x - rs[1]) * (x - rs[2]))
    c = p_.coeff(x, 2)
    parts = [(f'The roots of x³ {"+" if c >= 0 else "−"} {abs(c)}x² + px + q = 0 form an arithmetic sequence α − δ, α, α + δ. Use the sum of the roots to find α.', f'α = {a}', 'M1 A1', 2, True),
             (f'Given also that the product of the roots is {rs[0] * rs[1] * rs[2]}, find δ and hence p and q.', f'δ = ±{d}; p = {p_.coeff(x, 1)}, q = {p_.coeff(x, 0)}', 'M1 A1 A1 A1', 4, True),
             ('Show that, for any cubic x³ + bx² + cx + e = 0 whose roots are in arithmetic sequence, 2b³ − 9bc + 27e = 0.', 'proof', 'α = −b/3 is a root (M1); substitute (M1 A1); AG', 3, True),
             ('Use this condition to decide whether the roots of x³ − 6x² + 11x − 6 = 0 are in arithmetic sequence.', 'yes: 2(−216) − 9(−6)(11) + 27(−6) = 0; roots 1, 2, 3', 'M1 A1', 2, True),
             ('State and prove a similar condition for roots in geometric sequence.', 'c³ = b³e', 'middle root β with β³ = −e (M1); substitute (A1 A1)', 3, False)]
    return build_parts(rng, ['This question investigates cubic equations with roots in a sequence.', 'In this question all coefficients are real.'], parts, 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch09-st2', F(
    terms=[('rational function', 'a quotient p(x)/q(x) of two polynomials with q not the zero polynomial'),
           ('oblique asymptote', 'a non-horizontal straight-line asymptote y = mx + c, occurring when the degree of the numerator is one more than that of the denominator'),
           ('vertical asymptote of a rational function', 'a line x = a where the denominator is zero but the numerator is not')],
    facts=[('y = (x² + 1)/(x − 2) has an oblique asymptote because', 'the numerator has degree one more than the denominator', ['the denominator has no real roots', 'the degrees are equal', 'the numerator has no real roots'], 'Divide to get a linear part.'),
           ('The horizontal asymptote of y = (3x + 1)/(x² + 4) is', 'y = 0', ['y = 3', 'y = 1/4', 'x = 0'], 'Denominator has higher degree.'),
           ('The vertical asymptotes of y = x/(x² − 9) are', 'x = 3 and x = −3', ['x = 9', 'x = 0', 'y = 3'], 'x² − 9 = 0.'),
           ('y = (x² − 4)/(x − 2) has', 'a hole at x = 2 and no vertical asymptote', ['a vertical asymptote x = 2', 'an oblique asymptote y = x + 2 only', 'no graph'], 'Factor cancels.')],
    why=[('Explain why y = (x² + 3x + 1)/(x + 1) approaches the line y = x + 2 for large |x|.', 'Division gives x + 2 − 1/(x + 1); the fraction tends to 0 as |x| → ∞, so the curve approaches y = x + 2.'),
         ('Explain why y = (2x + 1)/(x² + 1) has no vertical asymptote.', 'x² + 1 > 0 for all real x, so the denominator is never zero.'),
         ('Explain why a common factor in numerator and denominator gives a hole, not an asymptote.', 'After cancelling, the function is finite near that x-value; it is only undefined at the single point, so the graph has a gap.')],
    misc=[('y = (x² + 1)/(x + 1) has horizontal asymptote y = 1.', 'The numerator has higher degree, so there is an oblique asymptote y = x − 1, not a horizontal one.'),
          ('Every zero of the denominator gives a vertical asymptote.', 'Not if it is also a zero of the numerator; then the factor may cancel to leave a hole.')],
))


@R.add('ch09-st2', 'C1', (1, 3), 'mcq')
def ratq_mcq(rng, slot):
    p, q = sorted(rng.sample(range(-6, 7), 2))
    a = nz(rng, -5, 5)
    den = sp.expand((x - p) * (x - q))
    return mcq(rng, f'The horizontal asymptote of y = ({poly_txt(a * x ** 2 + 1)})/({poly_txt(den)}) is', f'y = {a}', ['y = 0', f'y = {-a}', f'x = {p}'], 'Equal degrees: ratio of leading coefficients.')


@R.add('ch09-st2', 'C3', (2, 5), 'short', style='p1')
def oblique(rng, slot):
    m, c, k = nz(rng, -3, 3), rng.randint(-6, 6), nz(rng, -9, 9)
    d = nz(rng, -5, 5)
    num = sp.expand((m * x + c) * (x - d) + k)
    q_ = poly_txt(m * x + c) if c != 0 or m != 0 else '0'
    return mk(f'Find the equations of all asymptotes of the graph of y = ({poly_txt(num)})/(x {"−" if d > 0 else "+"} {abs(d)}).', f'x = {d}; y = {q_}',
              f'vertical asymptote x = {d} (A1); divide: {q_} + {k}/(x − {d}) (M1 A1); oblique asymptote y = {q_} (A1).'.replace('− −', '+ '), 4)


@R.add('ch09-st2', 'C3', (2, 5), 'short', style='p1')
def ratq_features(rng, slot):
    p, q = sorted(rng.sample(range(-5, 6), 2))
    a, b = nz(rng, -4, 4), rng.randint(-6, 6)
    if a * p + b == 0 or a * q + b == 0:
        return None
    den = sp.expand((x - p) * (x - q))
    f = (a * x + b) / den
    yi = sp.Rational(b, p * q) if p * q != 0 else None
    return mk(f'For y = ({poly_txt(a * x + b)})/({poly_txt(den)}), state the equations of the asymptotes and the coordinates of the axis intercepts.',
              f'x = {p}, x = {q}, y = 0; ({P(sp.Rational(-b, a))}, 0)' + (f', (0, {P(yi)})' if yi is not None else ''), 'vertical asymptotes (A1 A1); horizontal y = 0 (A1); intercepts (A1 A1).', 5)


@R.add('ch09-st2', 'C3', (2, 4), 'short', style='p2')
def ratq_gdc(rng, slot):
    a, b, c = rng.randint(1, 4), rng.randint(-5, 5), rng.randint(1, 6)
    f = (x ** 2 + b * x + c) / (x - a)
    if sp.Poly(x ** 2 + b * x + c, x).eval(a) == 0:
        return None
    fl = sp.lambdify(x, f, 'math')
    fp = sp.lambdify(x, sp.diff(f, x), 'math')
    st_ = nsols(fp, a + 0.01, a + 30) + nsols(fp, a - 30, a - 0.01)
    if len(st_) != 2:
        return None
    st_ = sorted(st_)
    return mk(f'Use your GDC to find the coordinates of the turning points of y = ({poly_txt(x ** 2 + b * x + c)})/(x − {a}), and hence state the range of the function.',
              f'max ({s3(st_[0])}, {s3(fl(st_[0]))}), min ({s3(st_[1])}, {s3(fl(st_[1]))}); y ≤ {s3(fl(st_[0]))} or y ≥ {s3(fl(st_[1]))}', 'GDC turning points (A1 A1); range (R1 A1).', 4)


@R.add('ch09-st2', 'C2', (2, 4), 'explain')
def ratq_explain(rng, slot):
    p = nz(rng, -6, 6)
    q = nz(rng, -6, 6, (0, p))
    return mk(f'Explain why y = (x² − {p * p})/((x {"−" if p > 0 else "+"} {abs(p)})(x {"−" if q > 0 else "+"} {abs(q)})) has only one vertical asymptote.', f'x = {q}',
              f'numerator = (x − {p})(x + {p}) (A1); the factor (x − {p}) cancels, giving a hole at x = {p} (R1); vertical asymptote x = {q} only (A1).'.replace('− −', '+ ').replace('+ −', '− '), 3, 'explain')


@R.add('ch09-st2', 'C4', (3, 5), 'multi_step', style='ext')
def ratq_parts(rng, slot):
    d = nz(rng, -4, 4)
    m, c, k = rng.choice([1, 2]), rng.randint(-4, 4), nz(rng, -6, 6)
    num = sp.expand((m * x + c) * (x - d) + k)
    f = num / (x - d)
    yi = f.subs(x, 0)
    roots = [r_ for r_ in sp.solve(num, x) if r_.is_real]
    parts = [(f'Show that f(x) can be written as {poly_txt(m * x + c)} + {k}/(x {"−" if d > 0 else "+"} {abs(d)}).'.replace('+ −', '− '), 'shown', 'division (M1) A1', 2, True),
             ('Write down the equations of the asymptotes.', f'x = {d}; y = {poly_txt(m * x + c)}', 'A1 A1', 2, True),
             ('Find the y-intercept and any x-intercepts, in exact form.', f'(0, {P(yi)}); ' + (', '.join(f'({nice(r_)}, 0)' for r_ in sorted(roots, key=float)) if roots else 'no x-intercepts'), 'A1 A1', 2, True),
             ('Find the coordinates of any turning points.', ', '.join(f'({nice(r_)}, {nice(sp.simplify(f.subs(x, r_)))})' for r_ in sorted([r_ for r_ in sp.solve(sp.diff(f, x), x) if r_.is_real], key=float)) or 'none', 'differentiate or GDC (M1) A1 A1', 3, False),
             ('Sketch the graph, showing the asymptotes and intercepts.', 'two branches approaching both asymptotes', 'A1 A1', 2, True)]
    return build_parts(rng, [f'Let f(x) = ({poly_txt(num)})/(x {"−" if d > 0 else "+"} {abs(d)}).', f'The function f is defined by f(x) = ({poly_txt(num)})/(x {"−" if d > 0 else "+"} {abs(d)}), x ≠ {d}.'], parts, 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch09-st3', F(
    terms=[('sign diagram', 'a number line showing where an expression is positive or negative, split at its zeros and asymptotes'),
           ('modulus |x|', 'the distance of x from 0: |x| = x for x ≥ 0 and −x for x < 0'),
           ('critical values', 'the values where an expression is zero or undefined, which divide the number line in solving inequalities')],
    facts=[('|x − 3| < 2 is equivalent to', '1 < x < 5', ['x < 5', 'x < 1 or x > 5', '−1 < x < 5'], '−2 < x − 3 < 2.'),
           ('(x − 1)(x + 2)(x − 4) > 0 holds for', '−2 < x < 1 or x > 4', ['x > 4 only', 'x < −2 or 1 < x < 4', '−2 < x < 4'], 'Sign diagram.'),
           ('|2x + 1| ≥ 5 is equivalent to', 'x ≤ −3 or x ≥ 2', ['−3 ≤ x ≤ 2', 'x ≥ 2', 'x ≤ −2 or x ≥ 3'], '2x + 1 ≤ −5 or ≥ 5.'),
           ('When multiplying an inequality by a negative number you must', 'reverse the inequality sign', ['keep the sign', 'square both sides', 'add 1'], 'Order reverses.')],
    why=[('Explain why you should not multiply both sides of (x + 1)/(x − 2) > 3 by (x − 2).', 'The sign of x − 2 is unknown; if it is negative the inequality would reverse. Multiply by (x − 2)² > 0 instead, or rearrange to one side.'),
         ('Explain why |x| < a (a > 0) is equivalent to −a < x < a.', '|x| is the distance from 0, so |x| < a means x is less than a units from 0 on either side.'),
         ('Explain how a sign diagram is used to solve a polynomial inequality.', 'The polynomial can only change sign at its zeros, so testing one value in each interval between zeros shows where it is positive or negative.')],
    misc=[('|x + 4| > 3 gives x > −1.', 'It also includes x + 4 < −3, so x < −7 or x > −1.'),
          ('x² > 9 means x > 3.', 'x² > 9 means x < −3 or x > 3.')],
))


@R.add('ch09-st3', 'C1', (1, 3), 'mcq')
def ineq_mcq(rng, slot):
    a, c = nz(rng, -6, 6), rng.randint(1, 6)
    lo, hi = a - c, a + c
    return mcq(rng, f'|x {"−" if a > 0 else "+"} {abs(a)}| ≤ {c} is equivalent to', f'{lo} ≤ x ≤ {hi}', [f'x ≤ {lo} or x ≥ {hi}', f'{-hi} ≤ x ≤ {-lo}', f'x ≤ {hi}'], 'Distance from a is at most c.')


@R.add('ch09-st3', 'C3', (2, 5), 'short', style='p1')
def poly_ineq(rng, slot):
    kind = rng.choice(['cubic', 'rational', 'modmod'])
    if kind == 'cubic':
        rs = sorted(rng.sample(range(-5, 6), 3))
        a = rng.choice([1, -1])
        e = sp.expand(a * (x - rs[0]) * (x - rs[1]) * (x - rs[2]))
        op = rng.choice(['>', '<', '≥', '≤'])
        pos = (op in '>≥')
        if a < 0:
            pos = not pos
        st = '≤' if op in '≤≥' else '<'
        st2 = '≥' if op in '≤≥' else '>'
        ans = f'{rs[0]} {st} x {st} {rs[1]} or x {st2} {rs[2]}' if pos else f'x {st} {rs[0]} or {rs[1]} {st} x {st} {rs[2]}'
        return mk(f'Solve {poly_txt(e)} {op} 0.', ans, f'factorise (M1): {a if a < 0 else ""}(x − {rs[0]})(x − {rs[1]})(x − {rs[2]}) (A1); sign diagram (M1); {ans} (A1).'.replace('−1(', '−(').replace('-1(', '−(').replace('− −', '+ ').replace('(x − 0)', 'x'), 4)
    if kind == 'rational':
        a, b, k = nz(rng, -5, 5), nz(rng, -5, 5), rng.randint(1, 4)
        if a == b:
            return None
        # (x − a)/(x − b) > k → ((1−k)x − a + kb)/(x − b) > 0
        crit = sp.Rational(a - k * b, 1 - k) if k != 1 else None
        if crit is None or crit == b:
            return None
        f = (x - a) / (x - b) - k
        lo, hi = sorted([crit, sp.Integer(b)])
        test = (lo + hi) / 2
        inside = f.subs(x, test) > 0
        ans = (f'{P(lo)} {"<" if lo == b else "<"} x < {P(hi)}' if inside else f'x < {P(lo)} or x > {P(hi)}')
        return mk(f'Solve (x {"−" if a > 0 else "+"} {abs(a)})/(x {"−" if b > 0 else "+"} {abs(b)}) > {k}.', ans,
                  f'rearrange to one side over a common denominator (M1); critical values x = {P(crit)} and x = {b} (A1 A1); sign diagram (M1); {ans} (A1).', 5)
    a, b = nz(rng, -4, 4), nz(rng, -4, 4)
    if a == b:
        return None
    c = sp.Rational(a + b, 2)
    ans = f'x > {P(c)}' if a < b else f'x < {P(c)}'
    return mk(f'Solve |x {"−" if a > 0 else "+"} {abs(a)}| > |x {"−" if b > 0 else "+"} {abs(b)}|.', ans,
              f'square both sides (both non-negative) (M1); {poly_txt(sp.expand((x - a) ** 2 - (x - b) ** 2))} > 0 (A1); {ans} (A1).', 3)


@R.add('ch09-st3', 'C3', (2, 4), 'short', style='p2')
def ineq_gdc(rng, slot):
    a, b = rng.randint(1, 4), rng.randint(1, 6)
    f = x ** 3 - a * x
    g = sp.Abs(x - b) if rng.random() < 0.5 else sp.Integer(b)
    fl = sp.lambdify(x, f - g, 'math')
    roots = nsols(fl, -8, 8)
    if not roots:
        return None
    intervals = []
    pts = [-50] + roots + [50]
    for i in range(len(pts) - 1):
        m_ = (pts[i] + pts[i + 1]) / 2
        if fl(m_) > 0:
            intervals.append((pts[i], pts[i + 1]))
    txt = ' or '.join((f'x > {s3(lo)}' if hi == 50 else f'x < {s3(hi)}' if lo == -50 else f'{s3(lo)} < x < {s3(hi)}') for lo, hi in intervals)
    gt = f'|x − {b}|' if g != b else str(b)
    return mk(f'Use your GDC to solve x³ − {a}x > {gt}.'.replace(' 1x', ' x'), txt, f'graph both sides (M1); intersections {", ".join(s3(r_) for r_ in roots)} (A1); correct intervals (A1 A1).', 4)


@R.add('ch09-st3', 'C2', (2, 4), 'explain')
def ineq_explain(rng, slot):
    k = rng.randint(2, 6)
    b = nz(rng, -4, 4)
    return mk(f'{who(rng)} solves (x + {k})/(x {"−" if b > 0 else "+"} {abs(b)}) > 1 by multiplying both sides by (x {"−" if b > 0 else "+"} {abs(b)}) and concludes that every x works. Explain the error and give the correct solution.',
              f'x > {b}' if k + b > 0 else f'x < {b}', f'x − {b} may be negative, which reverses the inequality (R1); (x + {k})/(x − {b}) − 1 = {k + b}/(x − {b}) > 0 (M1); {"x > " + str(b) if k + b > 0 else "x < " + str(b)} (A1).'.replace('− −', '+ '), 3, 'explain') if k + b != 0 else None


@R.add('ch09-st3', 'C4', (3, 5), 'multi_step', style='ext')
def ineq_parts(rng, slot):
    a, b = rng.randint(1, 4), nz(rng, -5, 5)
    c = rng.randint(1, 4)
    p_ = sp.expand((x - b) * (x ** 2 - c * c))
    rs = sorted(set([b, c, -c]))
    if len(rs) < 3:
        return None
    parts = [(f'Factorise p(x) = {poly_txt(p_)} completely.', f'(x {"−" if b > 0 else "+"} {abs(b)})(x − {c})(x + {c})', 'M1 A1', 2, True),
             ('Solve p(x) ≤ 0.', f'x ≤ {rs[0]} or {rs[1]} ≤ x ≤ {rs[2]}', 'sign diagram (M1) A1 A1', 3, True),
             (f'Solve |x − {b}| < {c}.', f'{b - c} < x < {b + c}', 'A1 A1', 2, True),
             (f'Find the values of x satisfying both p(x) ≤ 0 and |x − {b}| < {c}.', 'intersection of the two solution sets', 'M1 A1', 2, True),
             ('Solve |p(x)| = p(x).', f'{rs[0]} ≤ x ≤ {rs[1]} or x ≥ {rs[2]}', 'p(x) ≥ 0 (R1) A1', 2, False)]
    inter = sp.Intersection(sp.Union(sp.Interval(-sp.oo, rs[0]), sp.Interval(rs[1], rs[2])), sp.Interval.open(b - c, b + c))
    parts[3] = (parts[3][0], P(inter) if False else _set_txt(inter), parts[3][2], 2, True)
    return build_parts(rng, ['This question is about polynomial and modulus inequalities.', f'Let p(x) = {poly_txt(p_)}.'], parts, 4)


def _set_txt(S):
    if S == sp.EmptySet:
        return 'no values'
    parts = S.args if isinstance(S, sp.Union) else [S]
    out = []
    for I in parts:
        if isinstance(I, sp.FiniteSet):
            out += [f'x = {P(v)}' for v in I]
            continue
        lo, hi = I.start, I.end
        lt = '<' if I.left_open else '≤'
        rt = '<' if I.right_open else '≤'
        if lo == -sp.oo:
            out.append(f'x {rt} {P(hi)}')
        elif hi == sp.oo:
            out.append(f'x {"≥" if lt == "≤" else ">"} {P(lo)}')
        elif lo == hi:
            out.append(f'x = {P(lo)}')
        else:
            out.append(f'{P(lo)} {lt} x {rt} {P(hi)}')
    return ' or '.join(out)


# ---------------------------------------------------------------------------------------------
R.facts('ch09-st4', F(
    terms=[('partial fractions', 'writing a rational expression as a sum of simpler fractions, e.g. (5x + 1)/((x + 1)(x − 1)) = 2/(x + 1) + 3/(x − 1)'),
           ('proper fraction (algebraic)', 'a rational expression whose numerator has lower degree than its denominator'),
           ('cover-up method', 'finding A in A/(x − a) by substituting x = a into the rest of the expression after removing the factor (x − a)')],
    facts=[('(3x + 5)/((x + 1)(x + 2)) = A/(x + 1) + B/(x + 2) with A =', '2', ['1', '3', '−1'], 'x = −1: 2/1.'),
           ('Before splitting (x² + 1)/((x − 1)(x + 2)) into partial fractions you must', 'divide, since it is improper', ['factorise the numerator', 'multiply by x', 'nothing'], 'Equal degrees.'),
           ('1/(x(x + 1)) =', '1/x − 1/(x + 1)', ['1/x + 1/(x + 1)', '1/(x + 1) − 1/x', '2/x − 1/(x + 1)'], 'A = 1, B = −1.')],
    why=[('Explain why partial fractions are useful.', 'They turn one complicated fraction into simpler fractions that are easy to integrate, sum (telescoping series) or expand.'),
         ('Explain why the identity A(x + 2) + B(x − 1) ≡ 3x + 3 can be solved by substituting x = 1 and x = −2.', 'An identity holds for every x, so choosing values that make one bracket zero isolates each unknown.'),
         ('Explain why (2x + 3)/(x − 1)² cannot be written as A/(x − 1) + B/(x − 1) only.', 'Both terms have the same denominator, so they combine to a single (A + B)/(x − 1); a repeated factor needs A/(x − 1) + B/(x − 1)².')],
    misc=[('(x + 7)/((x − 1)(x + 2)) = 1/(x − 1) + 7/(x + 2).', 'Solve x + 7 ≡ A(x + 2) + B(x − 1): A = 8/3, B = −5/3.'),
          ('Partial fractions can be applied directly to (x² + 3)/((x + 1)(x − 2)).', 'It is improper (equal degrees): divide first to get 1 + (x + 5)/((x + 1)(x − 2)).')],
))


def _pf(rng):
    p, q = rng.sample(range(-5, 6), 2)
    A, B = nz(rng, -6, 6), nz(rng, -6, 6)
    num = sp.expand(A * (x - q) + B * (x - p))
    return p, q, A, B, num


def _lf(r):
    return f'(x {"−" if r > 0 else "+"} {abs(r)})' if r != 0 else 'x'


def _den2(p, q):
    return 'x' + _lf(p) if q == 0 else ('x' + _lf(q) if p == 0 else _lf(p) + _lf(q))


@R.add('ch09-st4', 'C1', (1, 3), 'mcq')
def pf_mcq(rng, slot):
    p, q, A, B, num = _pf(rng)
    if num.coeff(x, 1) == 0:
        return None
    return mcq(rng, f'If ({poly_txt(num)})/({_den2(p, q)}) = A/{_lf(p)} + B/{_lf(q)}, then A =', str(A), [str(B), str(-A), str(A + B) if A + B not in (A, B, -A) else str(A + 1)], f'Cover-up: put x = {p}.')


@R.add('ch09-st4', 'C3', (2, 5), 'short', style='p1')
def pf_split(rng, slot):
    kind = rng.choice(['two', 'two', 'improper', 'repeated'])
    p, q, A, B, num = _pf(rng)
    if kind == 'two':
        if num == 0:
            return None
        return mk(f'Express ({poly_txt(num)})/({_den2(p, q)}) in partial fractions.', f'{A}/{_lf(p)} + {B}/{_lf(q)}'.replace('+ −', '− '),
                  f'{poly_txt(num)} ≡ A{_lf(q)} + B{_lf(p)} (M1); x = {p}: A = {A} (A1); x = {q}: B = {B} (A1).', 3)
    if kind == 'improper':
        den = sp.expand((x - p) * (x - q))
        tot = sp.expand(den + num)
        return mk(f'Express ({poly_txt(tot)})/({poly_txt(den)}) in the form 1 + A/{_lf(p)} + B/{_lf(q)}.', f'1 + {A}/{_lf(p)} + {B}/{_lf(q)}'.replace('+ −', '− '),
                  f'divide: 1 + ({poly_txt(num)})/({poly_txt(den)}) (M1 A1); partial fractions A = {A}, B = {B} (M1 A1).', 4)
    a = nz(rng, -4, 4)
    A, B = nz(rng, -5, 5), nz(rng, -5, 5)
    num = sp.expand(A * (x - a) + B)
    return mk(f'Express ({poly_txt(num)})/{_lf(a)}² in the form A/{_lf(a)} + B/{_lf(a)}².', f'{A}/{_lf(a)} + {B}/{_lf(a)}²'.replace('+ −', '− '),
              f'{poly_txt(num)} ≡ A{_lf(a)} + B (M1); compare coefficients A = {A} (A1); x = {a}: B = {B} (A1).', 3)


@R.add('ch09-st4', 'C3', (2, 5), 'short', style='p1')
def pf_apply(rng, slot):
    k = rng.choice([1, 2, 3])
    n = rng.randint(5, 30)
    kind = rng.choice(['tele', 'tele'])
    S = sum(sp.Rational(1, r * (r + k)) for r in range(1, n + 1))
    return mk(f'Express 1/(r(r + {k})) in partial fractions and hence find Σ from r = 1 to {n} of 1/(r(r + {k})).', f'1/({k}r) − 1/({k}(r + {k})); {P(S)}'.replace('1/(1r)', '1/r').replace('1/(1(r + 1))', '1/(r + 1)'),
              f'A = 1/{k}, B = −1/{k} (A1 A1); terms cancel (telescoping) (M1); sum = {P(S)} (A1).', 4)


@R.add('ch09-st4', 'C2', (2, 4), 'explain')
def pf_explain(rng, slot):
    p, q, A, B, num = _pf(rng)
    if num == 0:
        return None
    return mk(f'Explain why substituting x = {p} into {poly_txt(num)} ≡ A{_lf(q)} + B{_lf(p)} gives A directly, and find A.', f'A = {A}',
              f'the identity holds for all x (R1); at x = {p} the B term vanishes (R1); {num.subs(x, p)} = A × {p - q}, A = {A} (A1).', 3, 'explain')


@R.add('ch09-st4', 'C4', (3, 5), 'multi_step', style='ext')
def pf_parts(rng, slot):
    p, q = sorted(rng.sample(range(1, 6), 2))
    A, B = nz(rng, -5, 5), nz(rng, -5, 5)
    num = sp.expand(A * (x + q) + B * (x + p))
    if num.coeff(x, 1) == 0:
        return None
    f = num / ((x + p) * (x + q))
    ser = _asc(sp.expand(sp.series(f, x, 0, 3).removeO()))
    parts = [(f'Express f(x) in partial fractions.', f'{A}/(x + {p}) + {B}/(x + {q})'.replace('+ −', '− '), 'M1 A1 A1', 3, True),
             ('Hence find f′(x).', (f'{-A}/(x + {p})²' + (f' + {-B}' if -B > 0 else f' − {B}') + f'/(x + {q})²'), 'A1 A1', 2, True),
             ('Use the extended binomial theorem to expand f(x) in ascending powers of x up to x².', ser, 'M1 A1 A1', 3, True),
             ('State the interval of validity of this expansion.', f'|x| < {p}', 'A1', 1, True),
             ('Find ∫₀¹ f(x) dx in exact form.', Pl(sp.simplify(sp.integrate(A / (x + p) + B / (x + q), (x, 0, 1)))), 'M1 A1', 2, False)]
    return build_parts(rng, [f'Let f(x) = ({poly_txt(num)})/((x + {p})(x + {q})).', 'This question applies partial fractions.'], parts, 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch09-st5', F(
    terms=[('system of linear equations', 'a set of linear equations in several unknowns to be satisfied simultaneously'),
           ('unique solution', 'the case where a system has exactly one solution; geometrically three planes meet at a single point'),
           ('inconsistent system', 'a system with no solutions'),
           ('row reduction (Gaussian elimination)', 'using row operations to reduce a system to triangular form before back-substituting')],
    facts=[('A system of three linear equations in three unknowns can have', '0, 1 or infinitely many solutions', ['exactly 3 solutions', 'exactly 1 solution always', '0 or 2 solutions'], 'Planes may meet in a point, a line or not at all.'),
           ('Row operations that preserve the solution set include', 'adding a multiple of one equation to another', ['squaring an equation', 'adding a constant to one side only', 'multiplying one side by 2'], 'Elementary operations.'),
           ('If elimination gives 0 = 5, the system', 'is inconsistent', ['has a unique solution', 'has infinitely many solutions', 'has the solution z = 5'], 'Contradiction.'),
           ('If elimination gives 0 = 0 for the last equation, the system', 'has infinitely many solutions (if consistent)', ['has no solution', 'has a unique solution', 'is wrong'], 'A free parameter remains.')],
    why=[('Explain why a GDC may report an error for a system with infinitely many solutions.', 'The equation-solver expects a unique solution; dependent equations give a singular coefficient matrix, so no single solution exists.'),
         ('Explain the geometric meaning of a system of three equations in x, y, z having no solution.', 'Each equation is a plane; no point lies on all three, e.g. two planes are parallel or the three form a triangular prism.'),
         ('Explain why a parameter is needed to describe infinitely many solutions.', 'After elimination one variable is free; the others are expressed in terms of it, e.g. z = λ, giving a line of solutions.')],
    misc=[('If two equations are the same, the system has no solution.', 'A repeated equation gives a dependent system, which usually has infinitely many solutions.'),
          ('Three equations in three unknowns always have a unique solution.', 'They may be inconsistent or dependent.')],
))


def _sys3(rng):
    sol = [nz(rng, -5, 5), rng.randint(-5, 5), nz(rng, -5, 5)]
    while True:
        M = [[rng.randint(-3, 4) for _ in range(3)] for _ in range(3)]
        if sp.Matrix(M).det() != 0 and all(any(r) for r in M):
            break
    rhs = [sum(M[i][j] * sol[j] for j in range(3)) for i in range(3)]
    return M, rhs, sol


def _eq3(row, r):
    e = row[0] * x + row[1] * y + row[2] * sp.Symbol('z')
    return f'{P(e)} = {r}'


@R.add('ch09-st5', 'C1', (1, 3), 'mcq')
def sys_mcq(rng, slot):
    M, rhs, sol = _sys3(rng)
    wr = [(sol[0], sol[2], sol[1]), (-sol[0], sol[1], sol[2]), (sol[1], sol[0], sol[2])]
    wr = [str(w) for w in wr if list(w) != sol]
    while len(wr) < 3:
        wr.append(str((sol[0] + 1, sol[1], sol[2])))
    return mcq(rng, 'The solution of ' + '; '.join(_eq3(M[i], rhs[i]) for i in range(3)) + ' is (x, y, z) =', str(tuple(sol)), wr[:3], 'Substitute to check.')


@R.add('ch09-st5', 'C3', (2, 5), 'short', style='p1')
def sys_solve(rng, slot):
    sol = [nz(rng, -4, 4), rng.randint(-4, 4), nz(rng, -4, 4)]
    a, b, c = nz(rng, -3, 3), nz(rng, -3, 3), nz(rng, -3, 3)
    M = [[1, a, b], [0, 1, c], [rng.randint(1, 3), rng.randint(-2, 2), 1]]
    if sp.Matrix(M).det() == 0:
        return None
    rhs = [sum(M[i][j] * sol[j] for j in range(3)) for i in range(3)]
    return mk('Solve, without a calculator, the system of equations ' + '; '.join(_eq3(M[i], rhs[i]) for i in range(3)) + '.', f'x = {sol[0]}, y = {sol[1]}, z = {sol[2]}',
              'eliminate one variable from two pairs (M1 A1); solve the 2 × 2 system (M1 A1); back-substitute (A1).', 5)


@R.add('ch09-st5', 'C3', (2, 4), 'short', style='p2')
def sys_gdc(rng, slot):
    kind = rng.choice(['ctx', 'plain'])
    if kind == 'plain':
        M, rhs, sol = _sys3(rng)
        return mk('Use your GDC to solve ' + '; '.join(_eq3(M[i], rhs[i]) for i in range(3)) + '.', f'x = {sol[0]}, y = {sol[1]}, z = {sol[2]}', 'GDC system solver (M1); all three correct (A2).', 3)
    pa, pb, pc = rng.choice([(2.5, 4, 1.5), (3, 1.25, 2), (1.8, 2.2, 3.5), (4.5, 2, 1)])
    na, nb, nc = rng.randint(2, 6), rng.randint(1, 5), rng.randint(2, 7)
    rows = [(na, nb, nc), (nb, nc, na), (nc + 1, na, nb + 1)]
    if sp.Matrix(rows).det() == 0:
        return None
    tots = [round(r[0] * pa + r[1] * pb + r[2] * pc, 2) for r in rows]
    nm_ = [who(rng) for _ in range(3)]
    return mk(f'At a market, {nm_[0]} buys {rows[0][0]} kg of apples, {rows[0][1]} kg of bananas and {rows[0][2]} kg of cherries for ${tots[0]:.2f}; {nm_[1]} buys {rows[1][0]}, {rows[1][1]} and {rows[1][2]} kg respectively for ${tots[1]:.2f}; {nm_[2]} buys {rows[2][0]}, {rows[2][1]} and {rows[2][2]} kg for ${tots[2]:.2f}. Find the price per kg of each fruit.',
              f'apples ${pa:.2f}, bananas ${pb:.2f}, cherries ${pc:.2f}', 'set up three equations (M1 A1); GDC (M1); prices (A1).', 4)


@R.add('ch09-st5', 'C2', (2, 4), 'explain')
def sys_explain(rng, slot):
    a, b, c = nz(rng, -4, 4), nz(rng, -4, 4), nz(rng, -4, 4)
    d, k = rng.randint(1, 9), rng.randint(2, 3)
    e1 = f'{P(a * x + b * y + c * sp.Symbol("z"))} = {d}'
    e2 = f'{P(k * a * x + k * b * y + k * c * sp.Symbol("z"))} = {k * d + rng.randint(1, 4)}'
    return mk(f'Explain why the system {e1}; {e2}; x + y + z = 1 has no solution.', 'inconsistent',
              f'the second equation\'s left side is {k} × the first (R1); but its right side is not {k} × {d} (R1); the planes are parallel, so no common point (A1).', 3, 'explain')


@R.add('ch09-st5', 'C4', (3, 5), 'multi_step', style='ext')
def sys_parts(rng, slot):
    a, b = nz(rng, -3, 3), nz(rng, -3, 3)
    z_ = sp.Symbol('z')
    c1, c2 = rng.randint(1, 6), rng.randint(1, 6)
    # rows r1, r2, r3 = r1 + r2 with k in place, rhs k
    r1 = (1, a, 1)
    r2 = (2, 1, b)
    r3 = (3, 1 + a, sp.Symbol('k'))
    kcrit = 1 + b
    rhs3 = c1 + c2
    lam = sp.Symbol('λ')
    sol_y = sp.solve([x + a * y + z_ - c1, 2 * x + y + b * z_ - c2], [x, y], dict=True)[0]
    parts = [(f'Find the value of k for which the system does not have a unique solution.', f'k = {kcrit}', 'determinant or elimination (M1) A1', 2, True),
             (f'For this value of k, show that the system has infinitely many solutions when m = {rhs3}.', 'third equation is the sum of the first two', 'R1 A1', 2, True),
             ('Find the general solution in terms of a parameter λ, with z = λ.', f'x = {P(sol_y[x].subs(z_, lam))}, y = {P(sol_y[y].subs(z_, lam))}, z = λ', 'M1 A1 A1', 3, True),
             (f'State the value of m for which the system has no solution when k = {kcrit}.', f'any m ≠ {rhs3}', 'A1', 1, True),
             ('Interpret the infinitely-many-solutions case geometrically.', 'three planes meeting in a common line', 'R1', 1, False)]
    sys_txt = f'x + {P(a * y)} + z = {c1}; 2x + y + {P(b * z_)} = {c2}; 3x + {P((1 + a) * y)} + kz = m'.replace('+ −', '− ').replace(' + 0y', '')
    return build_parts(rng, [f'Consider the system of equations {sys_txt}.', f'The system {sys_txt} is given, where k, m ∈ ℝ.'], parts, 4)


# =============================================================================================
# ch10 Statistics (SL 4.1–4.4, 4.10)
# =============================================================================================
def _med(v):
    v = sorted(v)
    n = len(v)
    return v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2


def quart(v):
    """Q1, median, Q3 by the halves method used by IB GDCs (median excluded when n is odd)"""
    v = sorted(v)
    n = len(v)
    lo, hi = v[:n // 2], v[(n + 1) // 2:]
    return _med(lo), _med(v), _med(hi)


def mean(v):
    return sum(v) / len(v)


def sdp(v):
    m = mean(v)
    return math.sqrt(sum((a - m) ** 2 for a in v) / len(v))


def g(v):
    """number text: integers without .0, otherwise 3 s.f."""
    return str(int(v)) if float(v).is_integer() else s3(v)


def _data(rng, n=None, lo=10, hi=60):
    n = n or rng.randint(9, 15)
    return sorted(rng.randint(lo, hi) for _ in range(n))


def dtxt(v):
    return ', '.join(str(a) for a in v)


R.facts('ch10-st1', F(
    terms=[('population', 'the entire group about which information is wanted'),
           ('sample', 'a subset of the population from which data are collected'),
           ('outlier', 'a value more than 1.5 × IQR below Q1 or above Q3'),
           ('discrete and continuous data', 'discrete data take separate (countable) values; continuous data can take any value in an interval, e.g. measurements')],
    facts=[('A sampling method in which every member has an equal chance of selection is', 'simple random sampling', ['convenience sampling', 'quota sampling', 'systematic sampling'], 'Definition.'),
           ('With Q1 = 20 and Q3 = 30, a value is an outlier if it exceeds', '45', ['40', '35', '50'], 'Q3 + 1.5 × IQR = 30 + 15.'),
           ('Selecting every 10th name on a list is', 'systematic sampling', ['stratified sampling', 'quota sampling', 'cluster sampling'], 'Fixed interval.'),
           ('The number of goals scored in a match is', 'discrete', ['continuous', 'qualitative', 'bivariate'], 'Countable values.')],
    why=[('Explain why a sample may be preferred to a census.', 'Collecting data on the whole population can be too costly, slow or destructive (e.g. testing products to failure); a well-chosen sample gives reliable estimates more cheaply.'),
         ('Explain why convenience sampling is likely to be biased.', 'Members are chosen because they are easy to reach, so they may systematically differ from the population, and not every member has a chance of selection.'),
         ('Explain why an outlier should not automatically be deleted.', 'It may be a genuine, important value; it should be removed only if it is shown to be an error (e.g. a recording mistake).')],
    misc=[('A stratified sample takes the same number from each group.', 'In a stratified sample each stratum is represented in proportion to its size in the population.'),
          ('Any value greater than the mean plus 10 is an outlier.', 'An outlier is usually defined as more than 1.5 × IQR beyond the quartiles.')],
))


@R.add('ch10-st1', 'C1', (1, 3), 'mcq')
def sampling_mcq(rng, slot):
    pool = [('A researcher surveys the first 30 people who enter a shopping centre.', 'convenience'), ('Each student in a school is given a number and 40 numbers are generated randomly.', 'simple random'),
            ('A teacher picks every 5th student from an alphabetical register, after a random start.', 'systematic'), ('A company samples employees from each department in proportion to department size.', 'stratified'),
            ('An interviewer must survey 20 men and 20 women but may choose whom to ask.', 'quota')]
    q, a = rng.choice(pool)
    return mcq(rng, q + ' The sampling method is', a + ' sampling', [w + ' sampling' for w in ['convenience', 'simple random', 'systematic', 'stratified', 'quota'] if w != a][:3], 'Match the description.')


@R.add('ch10-st1', 'C3', (2, 4), 'short', style='p2')
def outlier_check(rng, slot):
    v = _data(rng, rng.randint(10, 14), 20, 50)
    extra = rng.choice([v[-1] + rng.randint(20, 40), v[0] - rng.randint(15, 25), v[-1] + rng.randint(2, 6)])
    w = sorted(v + [extra])
    q1, m, q3 = quart(w)
    iqr = q3 - q1
    lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    outs = [a for a in w if a < lo or a > hi]
    return mk(f'The data set {dtxt(w)} is given. Find the quartiles and determine whether there are any outliers.', f'Q1 = {g(q1)}, Q3 = {g(q3)}; ' + (f'outlier(s): {", ".join(str(o) for o in outs)}' if outs else 'no outliers'),
              f'Q1 = {g(q1)}, Q3 = {g(q3)} (A1 A1); IQR = {g(iqr)}; fences {g(lo)} and {g(hi)} (M1); conclusion (A1).', 4)


@R.add('ch10-st1', 'C3', (2, 4), 'short', style='p1')
def stratified(rng, slot):
    groups = rng.choice([['Year 11', 'Year 12', 'Year 13'], ['full-time', 'part-time', 'contract'], ['under 18', '18–40', 'over 40'], ['science', 'arts', 'business', 'engineering']])
    k = rng.choice([20, 40, 50, 60])
    sizes = [rng.randint(2, 12) * 10 for _ in groups]
    N = sum(sizes)
    alloc = [s_ * k / N for s_ in sizes]
    if not all(abs(a - round(a)) < 1e-9 for a in alloc):
        return None
    txt = ', '.join(f'{gr}: {s_}' for gr, s_ in zip(groups, sizes))
    return mk(f'A population is made up of the groups {txt}. A stratified sample of size {k} is to be taken. Find the number to be sampled from each group.', ', '.join(f'{gr} {int(round(a))}' for gr, a in zip(groups, alloc)),
              f'proportion of each group × {k} (M1); ' + '; '.join(f'{s_}/{N} × {k} = {int(round(a))}' for s_, a in zip(sizes, alloc)) + ' (A2).', 3)


@R.add('ch10-st1', 'C2', (2, 4), 'explain')
def sampling_explain(rng, slot):
    ctx = rng.choice([('the average time students spend on homework', 'asking students in the library after school'), ('the proportion of voters who support a new park', 'asking people at the park'),
                      ('the mean height of adults in a city', 'measuring members of a basketball club'), ('customer satisfaction at a bank', 'surveying only customers who submit complaints')])
    return mk(f'To estimate {ctx[0]}, a researcher plans to collect data by {ctx[1]}. Explain why this sample is likely to be biased and suggest a better method.', 'not representative; use random/stratified sampling',
              'the sample over-represents a particular group (R1); not every member of the population has a chance of selection (R1); suggest random or stratified sampling from a full list (A1).', 3, 'explain')


@R.add('ch10-st1', 'C4', (3, 5), 'multi_step', style='ext')
def sampling_parts(rng, slot):
    v = _data(rng, 11, 30, 70)
    extra = v[-1] + rng.randint(25, 45)
    w = sorted(v + [extra])
    q1, m, q3 = quart(w)
    iqr = q3 - q1
    hi = q3 + 1.5 * iqr
    w2 = [a for a in w if a <= hi]
    parts = [(f'State whether the data are discrete or continuous.', 'discrete', 'A1', 1, True),
             ('Find the median and interquartile range.', f'{g(m)}; {g(iqr)}', 'A1 A1', 2, True),
             (f'Show that {extra} is an outlier.', f'{extra} > Q3 + 1.5 × IQR = {g(hi)}', 'M1 A1', 2, True),
             ('Find the mean with and without the outlier.', f'{s3(mean(w))}; {s3(mean(w2))}', 'A1 A1', 2, True),
             ('Explain which measure of centre is more appropriate for these data.', 'the median, as it is not affected by the outlier', 'R1', 1, True),
             ('The values were collected from the first 12 members to reply to an online survey. Comment on the reliability of conclusions drawn.', 'self-selected (convenience) sample; possible bias', 'R1', 1, False)]
    return build_parts(rng, [f'The numbers of minutes {rng.choice(["12 students", "12 commuters", "12 athletes"])} spent on an activity were recorded: {dtxt(w)}.', f'A small data set is given: {dtxt(w)}.'], parts, 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch10-st2', F(
    terms=[('cumulative frequency', 'the running total of frequencies up to the end of each class'),
           ('box-and-whisker plot', 'a diagram showing the minimum, Q1, median, Q3 and maximum (with outliers marked separately)'),
           ('histogram', 'a diagram for continuous grouped data in which bars of equal-width classes have heights equal to frequency'),
           ('interquartile range', 'the spread of the middle half of the data, IQR = Q3 − Q1')],
    facts=[('On a cumulative frequency graph for 80 values, the median is read at', 'a cumulative frequency of 40', ['a frequency of 40', 'the class with most values', 'x = 40'], 'n/2.'),
           ('The lower quartile for 200 values is read at cumulative frequency', '50', ['25', '100', '150'], 'n/4.'),
           ('A box plot whose right whisker is much longer than the left suggests', 'positive skew', ['negative skew', 'symmetry', 'no outliers'], 'Tail to the right.'),
           ('In a histogram with equal class widths, the bar height represents', 'frequency', ['cumulative frequency', 'the mean', 'class width'], 'Equal widths.')],
    why=[('Explain why the median and quartiles from a cumulative frequency graph are only estimates.', 'Grouped data lose individual values; the graph assumes values are spread evenly within each class, so readings are approximate.'),
         ('Explain why a box plot is useful for comparing two data sets.', 'It shows the median, spread (IQR, range) and skew on a common scale at a glance, making differences in centre and variability easy to see.'),
         ('Explain why cumulative frequency is plotted at the upper class boundary.', 'The cumulative frequency counts all values up to the end of the class, so it corresponds to the upper boundary.')],
    misc=[('The median of grouped data is the midpoint of the middle class.', 'It is estimated from the cumulative frequency graph at n/2, which need not be a class midpoint.'),
          ('A longer box means more data values in that half.', 'Each quarter contains the same number of values; a longer section means those values are more spread out.')],
))


def _grouped(rng):
    w = rng.choice([5, 10, 20])
    start = rng.choice([0, 10, 20, 40]) if w > 5 else rng.choice([0, 5, 10])
    k = rng.randint(5, 6)
    f = [rng.randint(2, 18) for _ in range(k)]
    return [(start + i * w, start + (i + 1) * w) for i in range(k)], f


@R.add('ch10-st2', 'C1', (1, 3), 'mcq')
def boxplot_mcq(rng, slot):
    v = _data(rng, rng.randint(9, 13))
    q1, m, q3 = quart(v)
    return mcq(rng, f'For the data {dtxt(v)}, the interquartile range is', g(q3 - q1), [g(v[-1] - v[0]), g(q3 - m), g(m - q1) if m - q1 != q3 - m else g(q3 - q1 + 1)], 'Q3 − Q1.')


@R.add('ch10-st2', 'C3', (2, 4), 'short', style='p2')
def cumfreq(rng, slot):
    cls, f = _grouped(rng)
    cf = [sum(f[:i + 1]) for i in range(len(f))]
    n = cf[-1]

    def interp(target):
        for i, c in enumerate(cf):
            if c >= target:
                prev = cf[i - 1] if i else 0
                lo, hi = cls[i]
                return lo + (target - prev) / f[i] * (hi - lo)
    kind = rng.choice(['median', 'iqr', 'pct'])
    table = '; '.join(f'{a} ≤ x < {b}: {fr}' for (a, b), fr in zip(cls, f))
    if kind == 'median':
        return mk(f'The grouped frequency table is: {table}. Write down the cumulative frequencies and estimate the median by linear interpolation.', f'{", ".join(str(c) for c in cf)}; median ≈ {s3(interp(n / 2))}',
                  f'cumulative frequencies (A1); median at cf = {n / 2:g} (M1); interpolate within the class (M1); {s3(interp(n / 2))} (A1).', 4)
    if kind == 'iqr':
        return mk(f'The grouped frequency table is: {table}. Estimate the interquartile range using linear interpolation on the cumulative frequency.', s3(interp(3 * n / 4) - interp(n / 4)),
                  f'Q1 at cf {n / 4:g}: {s3(interp(n / 4))} (A1); Q3 at cf {3 * n / 4:g}: {s3(interp(3 * n / 4))} (A1); IQR (A1).', 3)
    k = rng.choice(cls[2:])[0]
    below = sum(fr for (a, b), fr in zip(cls, f) if b <= k)
    return mk(f'The grouped frequency table is: {table}. Find the number and the percentage of values less than {k}.', f'{below}; {s3(100 * below / n)}%', f'cumulative frequency at {k} (M1); {below} (A1); {below}/{n} × 100 (A1).', 3)


@R.add('ch10-st2', 'C3', (2, 4), 'short', style='p1')
def boxplot_five(rng, slot):
    n = rng.choice([7, 9, 11, 8, 10, 12])
    v = _data(rng, n, 1, 40)
    q1, m, q3 = quart(v)
    return mk(f'For the data {dtxt(v)}, find the five-number summary and describe what a box-and-whisker plot of the data would show about its skewness.',
              f'min {v[0]}, Q1 {g(q1)}, median {g(m)}, Q3 {g(q3)}, max {v[-1]}; ' + ('positive skew' if (q3 - m) > (m - q1) else 'negative skew' if (q3 - m) < (m - q1) else 'roughly symmetric'),
              f'median {g(m)} (A1); quartiles {g(q1)}, {g(q3)} (A1 A1); compare box sections/whiskers (R1).', 4)


@R.add('ch10-st2', 'C2', (2, 4), 'explain')
def boxplot_explain(rng, slot):
    a = (rng.randint(10, 20), rng.randint(22, 30), rng.randint(32, 40), rng.randint(42, 50), rng.randint(55, 70))
    b = (rng.randint(5, 15), rng.randint(25, 30), rng.randint(31, 36), rng.randint(37, 42), rng.randint(60, 80))
    return mk(f'Box plots for two classes show five-number summaries A: {a} and B: {b} (min, Q1, median, Q3, max). Explain which class performed better on average and which was more consistent.',
              f'{"A" if a[2] > b[2] else "B"} higher median; {"A" if a[3] - a[1] < b[3] - b[1] else "B"} smaller IQR (more consistent)',
              f'compare medians {a[2]} and {b[2]} (R1); compare IQRs {a[3] - a[1]} and {b[3] - b[1]} (R1); conclusions in context (A1).', 3, 'explain')


@R.add('ch10-st2', 'C4', (3, 5), 'multi_step', style='ext')
def cumfreq_parts(rng, slot):
    cls, f = _grouped(rng)
    cf = [sum(f[:i + 1]) for i in range(len(f))]
    n = cf[-1]

    def interp(target):
        for i, c in enumerate(cf):
            if c >= target:
                prev = cf[i - 1] if i else 0
                lo, hi = cls[i]
                return lo + (target - prev) / f[i] * (hi - lo)
    mids = [(a + b) / 2 for a, b in cls]
    mu = sum(m_ * fr for m_, fr in zip(mids, f)) / n
    table = '; '.join(f'{a} ≤ t < {b}: {fr}' for (a, b), fr in zip(cls, f))
    k = cls[-2][0]
    parts = [('Complete a cumulative frequency table.', ', '.join(str(c) for c in cf), 'A1 A1', 2, True),
             ('Estimate the median and the interquartile range.', f'{s3(interp(n / 2))}; {s3(interp(3 * n / 4) - interp(n / 4))}', 'M1 A1 A1', 3, True),
             ('Calculate an estimate of the mean.', s3(mu), 'midpoints (M1) A1', 2, True),
             (f'Find the percentage of the times that are at least {k} minutes.', f'{s3(100 * sum(f[-2:]) / n)}%', 'A1', 1, True),
             ('Draw a box-and-whisker plot using the estimates, taking the minimum and maximum as the class limits.', f'{cls[0][0]}, {s3(interp(n / 4))}, {s3(interp(n / 2))}, {s3(interp(3 * n / 4))}, {cls[-1][1]}', 'A1 A1', 2, False)]
    return build_parts(rng, [f'The times, t minutes, taken by {n} people to complete a task are summarised: {table}.', f'A grouped frequency table of {n} times is given: {table}.'], parts, 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch10-st3', F(
    terms=[('mean', 'x̄ = Σx/n, the sum of the values divided by the number of values'),
           ('standard deviation', 'σ = √(Σ(x − x̄)²/n), a measure of spread about the mean'),
           ('variance', 'the square of the standard deviation, σ²'),
           ('mode and modal class', 'the most frequent value, or for grouped data the class with the highest frequency')],
    facts=[('If 5 is added to every value, the standard deviation', 'is unchanged', ['increases by 5', 'is multiplied by 5', 'increases by 25'], 'Spread is unchanged by a shift.'),
           ('If every value is multiplied by 3, the variance is multiplied by', '9', ['3', '1', '√3'], 'σ becomes 3σ.'),
           ('If every value is multiplied by 2 and then 4 is added, the new mean is', '2x̄ + 4', ['2x̄', 'x̄ + 4', '2(x̄ + 4)'], 'Apply to the mean.'),
           ('The mean of 4, 7, 7, 10, 12 is', '8', ['7', '7.5', '10'], '40/5.')],
    why=[('Explain why adding a constant to every value does not change the standard deviation.', 'Every value and the mean shift by the same amount, so each deviation x − x̄ is unchanged; hence σ is unchanged.'),
         ('Explain why the median may be a better average than the mean for income data.', 'Income data are usually positively skewed with a few very large values, which pull the mean up; the median is resistant to extreme values.'),
         ('Explain why standard deviation is measured in the same units as the data.', 'It is the square root of the mean of squared deviations, so the units of the squared deviations are square-rooted back to the original units.')],
    misc=[('Doubling every value doubles the variance.', 'The variance is multiplied by 4; the standard deviation is doubled.'),
          ('If the mean of 6 numbers is 10 and one number 22 is removed, the new mean is 10 − 22/6.', 'The new total is 60 − 22 = 38, so the new mean is 38/5 = 7.6.')],
))


@R.add('ch10-st3', 'C1', (1, 3), 'mcq')
def transform_stats_mcq(rng, slot):
    m, s_ = rng.randint(20, 80), rng.randint(3, 15)
    a, b = rng.randint(2, 5), nz(rng, -10, 10)
    if rng.random() < 0.5:
        return mcq(rng, f'A data set has mean {m} and standard deviation {s_}. Each value is multiplied by {a} and then {b} is added. The new standard deviation is'.replace('then −', 'then −'), str(a * s_), [str(a * s_ + b), str(s_), str(a * a * s_)], 'Only the multiplier affects spread.')
    return mcq(rng, f'A data set has mean {m} and standard deviation {s_}. Each value is multiplied by {a} and then {b} is added. The new mean is', str(a * m + b), [str(a * m), str(m + b), str(a * (m + b))], 'Apply the transformation to the mean.')


@R.add('ch10-st3', 'C3', (2, 4), 'short', style='p2')
def stats_gdc(rng, slot):
    kind = rng.choice(['raw', 'freq'])
    if kind == 'raw':
        v = _data(rng, rng.randint(8, 12), 5, 95)
        q1, m, q3 = quart(v)
        return mk(f'For the data {dtxt(v)}, use your GDC to find the mean, standard deviation, median and interquartile range.', f'{s3(mean(v))}; {s3(sdp(v))}; {g(m)}; {g(q3 - q1)}',
                  f'x̄ = {s3(mean(v))} (A1); σ = {s3(sdp(v))} (A1); median {g(m)} (A1); IQR {g(q3 - q1)} (A1).', 4)
    xs_ = sorted(rng.sample(range(0, 9), 5))
    fs = [rng.randint(1, 12) for _ in xs_]
    data = [a for a, fr in zip(xs_, fs) for _ in range(fr)]
    q1, m, q3 = quart(data)
    tab = ', '.join(f'{a} (f = {fr})' for a, fr in zip(xs_, fs))
    return mk(f'The number of books read by a group of students is: {tab}. Find the mean, the standard deviation and the median.', f'{s3(mean(data))}; {s3(sdp(data))}; {g(m)}',
              f'Σfx/Σf = {sum(a * fr for a, fr in zip(xs_, fs))}/{sum(fs)} (M1); {s3(mean(data))} (A1); σ {s3(sdp(data))} (A1); median {g(m)} (A1).', 4)


@R.add('ch10-st3', 'C3', (2, 5), 'short', style='p1')
def stats_algebra(rng, slot):
    kind = rng.choice(['missing', 'combine', 'transform', 'k'])
    if kind == 'missing':
        n, m = rng.randint(5, 9), rng.randint(10, 30)
        v = [rng.randint(m - 8, m + 8) for _ in range(n - 1)]
        last = n * m - sum(v)
        if last < 0:
            return None
        return mk(f'The mean of the {n} numbers {", ".join(str(a) for a in v)}, x is {m}. Find x.', f'x = {last}', f'total = {n} × {m} = {n * m} (M1); x = {n * m} − {sum(v)} (A1).', 2)
    if kind == 'combine':
        n1, m1, n2, m2 = rng.randint(10, 30), rng.randint(50, 80), rng.randint(10, 30), rng.randint(50, 80)
        M = sp.Rational(n1 * m1 + n2 * m2, n1 + n2)
        return mk(f'Class A has {n1} students with mean score {m1}; class B has {n2} students with mean score {m2}. Find the mean score of all {n1 + n2} students.', P(M) if M.q == 1 else f'{P(M)} ≈ {s3(M)}',
                  f'total {n1 * m1} + {n2 * m2} (M1); ÷ {n1 + n2} (A1).', 2)
    if kind == 'transform':
        m, s_ = rng.randint(20, 60), rng.randint(2, 9)
        a, b = rng.choice([2, 3, sp.Rational(1, 2), 5]), nz(rng, -15, 15)
        return mk(f'A set of data has mean {m} and standard deviation {s_}. Each value x is transformed to y = {P(a * x) if a != 1 else "x"} {"+" if b > 0 else "−"} {abs(b)}. Find the mean and the variance of the y-values.', f'mean {P(a * m + b)}; variance {P(a * a * s_ * s_)}',
                  f'mean {P(a)} × {m} {"+" if b > 0 else "−"} {abs(b)} (A1); σ_y = {P(a * s_)} (M1); variance {P(a * a * s_ * s_)} (A1).', 3)
    v = sorted(rng.sample(range(1, 15), 4))
    k = sp.Symbol('k')
    target = rng.randint(4, 12)
    kval = 5 * target - sum(v)
    if kval <= 0:
        return None
    return mk(f'The data {", ".join(str(a) for a in v)}, k have mean {target}. Find k and the variance of the data.', f'k = {kval}; variance {P(sp.Rational(sum((a - target) ** 2 for a in v + [kval]), 5))}',
              f'(Σ + k)/5 = {target} (M1); k = {kval} (A1); Σ(x − x̄)²/5 (M1); variance (A1).', 4)


@R.add('ch10-st3', 'C2', (2, 4), 'explain')
def stats_explain(rng, slot):
    a = rng.randint(2, 5)
    s_ = rng.randint(2, 9)
    return mk(f'{who(rng)} says that if every value in a data set with standard deviation {s_} is multiplied by {a}, the variance becomes {a * s_ * s_}. Explain the error and find the correct variance.', str(a * a * s_ * s_),
              f'deviations from the mean are multiplied by {a} (R1); squared deviations by {a * a} (R1); variance {a * a} × {s_ * s_} = {a * a * s_ * s_} (A1).', 3, 'explain')


@R.add('ch10-st3', 'C4', (3, 5), 'multi_step', style='ext')
def stats_parts(rng, slot):
    v = _data(rng, 10, 20, 80)
    m, s_ = mean(v), sdp(v)
    q1, med, q3 = quart(v)
    a, b = rng.choice([(1.8, 32), (2, 5), (1.5, 10), (0.5, 0)])
    parts = [('Find the mean and standard deviation.', f'{s3(m)}; {s3(s_)}', 'A1 A1', 2, True),
             ('Find the median and the interquartile range.', f'{g(med)}; {g(q3 - q1)}', 'A1 A1', 2, True),
             (f'Each value is converted using y = {a:g}x + {b}. Find the mean and standard deviation of the converted values.', f'{s3(a * m + b)}; {s3(a * s_)}', 'M1 A1 A1', 3, True),
             (f'Find the variance of the converted values.', s3((a * s_) ** 2), 'A1', 1, True),
             ('The largest value was recorded incorrectly and should be 10 less. State, with a reason, how the median and mean change.', 'median unchanged (it is not the middle value); mean decreases by 1', 'R1 A1', 2, False)]
    return build_parts(rng, [f'Ten values are recorded: {dtxt(v)}.', f'The following data were collected: {dtxt(v)}.'], parts, 4)


@R.add('ch10-st3', 'C4', (4, 5), 'multi_step', style='p3')
def stats_p3(rng, slot):
    n = rng.randint(5, 8)
    parts = [('Show that Σ(xᵢ − x̄)² = Σxᵢ² − n x̄².', 'proof', 'expand (M1); Σxᵢ = n x̄ (A1); AG', 3, True),
             ('Hence show that σ² = (Σx²)/n − x̄².', 'divide by n', 'A1', 1, True),
             (f'For the data 1, 2, …, {n}, find the mean and the variance in exact form.', f'{P(sp.Rational(n + 1, 2))}; {P(sp.Rational(n * n - 1, 12))}', 'M1 A1 A1', 3, True),
             ('Prove that, for the first n positive integers, σ² = (n² − 1)/12.', 'proof', 'Σr² = n(n + 1)(2n + 1)/6 (M1); simplify (A1 A1)', 3, True),
             ('Deduce the variance of the values a + d, a + 2d, …, a + nd.', 'd²(n² − 1)/12', 'R1 A1', 2, True),
             ('Comment on why the answer does not depend on a.', 'adding a constant does not change spread', 'R1', 1, False)]
    return build_parts(rng, ['This question develops a formula for the variance.', 'In this question σ denotes the population standard deviation.'], parts, 5)


# ---------------------------------------------------------------------------------------------
R.facts('ch10-st4', F(
    terms=[('Pearson product-moment correlation coefficient', 'the value r, −1 ≤ r ≤ 1, that measures the strength and direction of linear association'),
           ('regression line of y on x', 'the least-squares line y = ax + b used to predict y from a given x'),
           ('interpolation and extrapolation', 'predicting within the range of the data (reliable if r is strong) versus outside it (unreliable)'),
           ('bivariate data', 'data with two variables measured on each individual')],
    facts=[('r = −0.94 indicates', 'strong negative linear correlation', ['weak negative correlation', 'strong positive correlation', 'no correlation'], 'Close to −1.'),
           ('The regression line of y on x always passes through', '(x̄, ȳ)', ['(0, 0)', '(0, ȳ)', 'the first data point'], 'Least squares property.'),
           ('Correlation does not imply', 'causation', ['association', 'a straight line', 'r between −1 and 1'], 'A third variable may be involved.'),
           ('Using a regression line far outside the data range is called', 'extrapolation', ['interpolation', 'correlation', 'sampling'], 'Beyond the data.')],
    why=[('Explain why the regression line of y on x should not be used to predict x from y.', 'It minimises the squared vertical (y) residuals; predicting x needs the line that minimises horizontal residuals (x on y).'),
         ('Explain why extrapolation is unreliable.', 'The linear relationship is only supported within the range of the data; outside it the pattern may change.'),
         ('Explain why a value of r close to 0 does not mean there is no relationship.', 'r measures only linear association; a strong non-linear (e.g. quadratic) relationship can have r ≈ 0.')],
    misc=[('r = 0.9 means that 90% of the points lie on the line.', 'r measures the strength of linear association; it is not a percentage of points.'),
          ('Since r = 0.85 between ice-cream sales and drownings, ice cream causes drowning.', 'Correlation is not causation; both increase in hot weather.')],
))


def _bivar(rng, n=None):
    n = n or rng.randint(7, 10)
    a, b = rng.choice([1.5, 2.2, -1.8, 3.1, -0.7, 0.9]), rng.randint(5, 40)
    noise = rng.choice([0.1, 0.2, 0.3, 0.45]) * abs(a) * 15
    xs_ = sorted(rng.sample(range(1, 30), n))
    ys_ = [round(a * v + b + rng.uniform(-noise, noise)) for v in xs_]
    return xs_, ys_


def _reg(xs_, ys_):
    n = len(xs_)
    mx, my = mean(xs_), mean(ys_)
    sxy = sum((a - mx) * (b - my) for a, b in zip(xs_, ys_))
    sxx = sum((a - mx) ** 2 for a in xs_)
    syy = sum((b - my) ** 2 for b in ys_)
    r = sxy / math.sqrt(sxx * syy)
    a = sxy / sxx
    return r, a, my - a * mx, sxy / syy, mx - sxy / syy * my


def lin_txt(a, b, yv='y', xv='x'):
    return f'{yv} = {s3(a)}{xv} {"+" if b >= 0 else "−"} {s3(abs(b))}'


@R.add('ch10-st4', 'C1', (1, 3), 'mcq')
def corr_mcq(rng, slot):
    r = rng.choice([0.96, 0.82, 0.45, 0.08, -0.12, -0.55, -0.91])
    desc = ('strong' if abs(r) > 0.75 else 'moderate' if abs(r) > 0.4 else 'weak or no') + (' positive' if r > 0.3 else ' negative' if r < -0.3 else '')
    desc = desc.replace('weak or no', 'weak or no linear correlation').strip()
    if abs(r) > 0.3:
        desc += ' linear correlation'
    return mcq(rng, f'A correlation coefficient of r = {r} indicates', desc, [d_ for d_ in ['strong positive linear correlation', 'strong negative linear correlation', 'moderate positive linear correlation', 'moderate negative linear correlation', 'weak or no linear correlation'] if d_ != desc][:3], 'Interpret size and sign.')


@R.add('ch10-st4', 'C3', (2, 5), 'short', style='p2')
def regression(rng, slot):
    xs_, ys_ = _bivar(rng)
    r, a, b, _, _ = _reg(xs_, ys_)
    xp = rng.randint(min(xs_) + 1, max(xs_) - 1)
    tab = '; '.join(f'({u}, {v})' for u, v in zip(xs_, ys_))
    return mk(f'The data (x, y) are: {tab}. Find Pearson\'s correlation coefficient r, the equation of the regression line of y on x, and use it to estimate y when x = {xp}.', f'r = {s3(r)}; {lin_txt(a, b)}; y ≈ {s3(a * xp + b)}',
              f'GDC r = {s3(r)} (A1); a = {s3(a)}, b = {s3(b)} (A1 A1); substitute x = {xp} (M1); {s3(a * xp + b)} (A1).', 5)


@R.add('ch10-st4', 'C3', (2, 4), 'short', style='p1')
def regression_mean(rng, slot):
    a, b = rng.choice([2, 3, -2, sp.Rational(1, 2), 4]), rng.randint(-10, 20)
    mx = rng.randint(4, 20)
    my = a * mx + b
    kind = rng.choice(['mean', 'missing'])
    if kind == 'mean':
        return mk(f'The regression line of y on x for a data set is y = {P(a * x)} {"+" if b >= 0 else "−"} {abs(b)}, and x̄ = {mx}. Find ȳ, and explain why.', f'ȳ = {P(my)}',
                  f'the line passes through (x̄, ȳ) (R1); ȳ = {P(a)} × {mx} {"+" if b >= 0 else "−"} {abs(b)} = {P(my)} (A1).', 2)
    n = rng.randint(5, 8)
    sx = mx * n
    return mk(f'For {n} data points, Σx = {sx} and Σy = {P(my * n)}. The regression line of y on x has gradient {P(a)}. Find its equation.', f'y = {P(a * x)} {"+" if b >= 0 else "−"} {abs(b)}',
              f'x̄ = {mx}, ȳ = {P(my)} (A1); y − {P(my)} = {P(a)}(x − {mx}) (M1); y = {P(a * x)} {"+" if b >= 0 else "−"} {abs(b)} (A1).', 3)


@R.add('ch10-st4', 'C2', (2, 4), 'explain')
def corr_explain(rng, slot):
    xs_, ys_ = _bivar(rng)
    r, a, b, _, _ = _reg(xs_, ys_)
    xp = max(xs_) + rng.randint(20, 60)
    return mk(f'For data with x between {min(xs_)} and {max(xs_)}, the regression line is {lin_txt(a, b)} and r = {s3(r)}. Explain whether it is appropriate to use the line to predict y when x = {xp}.', 'not reliable: extrapolation',
              f'x = {xp} is outside the data range (R1); the linear pattern may not continue (R1); prediction unreliable despite r = {s3(r)} (A1).', 3, 'explain')


@R.add('ch10-st4', 'C4', (3, 5), 'multi_step', style='ext')
def regression_parts(rng, slot):
    ctx = rng.choice([('hours of revision', 'test score (%)'), ('temperature (°C)', 'drinks sold'), ('advertising spend ($1000s)', 'sales ($1000s)'), ('age of car (years)', 'value ($1000s)')])
    xs_, ys_ = _bivar(rng, 8)
    r, a, b, _, _ = _reg(xs_, ys_)
    xp = rng.randint(min(xs_) + 1, max(xs_) - 1)
    tab = '; '.join(f'({u}, {v})' for u, v in zip(xs_, ys_))
    parts = [(f'Find the value of r and interpret it in context.', f'r = {s3(r)}; ' + ('strong' if abs(r) > 0.75 else 'moderate') + (' positive' if r > 0 else ' negative') + ' linear correlation', 'A1 R1', 2, True),
             ('Find the equation of the regression line of y on x.', lin_txt(a, b), 'A1 A1', 2, True),
             ('Interpret the gradient of the line in context.', f'each extra unit of {ctx[0]} is associated with a change of {s3(a)} in {ctx[1]}', 'R1', 1, True),
             (f'Estimate y when x = {xp}.', s3(a * xp + b), 'M1 A1', 2, True),
             ('Write down the coordinates of the point (x̄, ȳ) and verify that it lies on the line.', f'({s3(mean(xs_))}, {s3(mean(ys_))})', 'A1', 1, True),
             (f'Explain why the line should not be used to estimate x when y = {round(a * xp + b)}.', 'use the x-on-y line; this line predicts y from x', 'R1', 1, False)]
    return build_parts(rng, [f'Data for x = {ctx[0]} and y = {ctx[1]} are: {tab}.', f'A study recorded x, {ctx[0]}, and y, {ctx[1]}: {tab}.'], parts, 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch10-st5', F(
    terms=[('regression line of x on y', 'the least-squares line x = cy + d, minimising horizontal residuals, used to predict x from y'),
           ('residual', 'the difference between an observed value and the value predicted by the regression line'),
           ('least squares', 'the principle of choosing the line that minimises the sum of the squared residuals')],
    facts=[('To estimate x from a given y, use', 'the regression line of x on y', ['the regression line of y on x', 'the mean of x', 'r'], 'Predict the variable on the left.'),
           ('The two regression lines intersect at', '(x̄, ȳ)', ['the origin', '(0, ȳ)', 'they never intersect'], 'Both pass through the means.'),
           ('If r = ±1, the two regression lines', 'coincide', ['are perpendicular', 'are parallel', 'meet at the origin'], 'Perfect correlation.')],
    why=[('Explain why there are two different regression lines.', 'The y-on-x line minimises vertical squared residuals and the x-on-y line minimises horizontal ones; unless r = ±1 these give different lines.'),
         ('Explain why the regression lines get closer together as |r| increases.', 'With stronger correlation the points lie closer to a line, so minimising vertical or horizontal residuals gives nearly the same line; they coincide when |r| = 1.')],
    misc=[('To predict x from y, rearrange y = ax + b.', 'Rearranging the y-on-x line is not the least-squares predictor of x; use the x-on-y line.'),
          ('The x-on-y line passes through (0, 0).', 'It passes through (x̄, ȳ), not necessarily the origin.')],
))


@R.add('ch10-st5', 'C1', (1, 3), 'mcq')
def xony_mcq(rng, slot):
    mx, my = rng.randint(5, 30), rng.randint(10, 60)
    return mcq(rng, f'The regression line of x on y for a data set with x̄ = {mx} and ȳ = {my} passes through', f'({mx}, {my})', [f'({my}, {mx})', '(0, 0)', f'(0, {my})'], 'Both lines pass through (x̄, ȳ).')


@R.add('ch10-st5', 'C3', (2, 5), 'short', style='p2')
def xony(rng, slot):
    xs_, ys_ = _bivar(rng)
    r, a, b, c, d = _reg(xs_, ys_)
    yp = round(mean(ys_) + rng.uniform(-1, 1) * sdp(ys_) * 0.6)
    tab = '; '.join(f'({u}, {v})' for u, v in zip(xs_, ys_))
    return mk(f'The data (x, y) are: {tab}. Find the regression line of x on y and use it to estimate x when y = {yp}.', f'{lin_txt(c, d, "x", "y")}; x ≈ {s3(c * yp + d)}',
              f'GDC with y as the independent variable (M1); c = {s3(c)}, d = {s3(d)} (A1 A1); substitute (A1).', 4)


@R.add('ch10-st5', 'C2', (2, 4), 'explain')
def xony_explain(rng, slot):
    xs_, ys_ = _bivar(rng)
    r, a, b, c, d = _reg(xs_, ys_)
    yp = round(mean(ys_))
    return mk(f'The regression line of y on x is {lin_txt(a, b)} (r = {s3(r)}). {who(rng)} rearranges it to estimate x when y = {yp}. Explain why this is not the correct method.', 'use the x-on-y line',
              f'the y-on-x line minimises vertical residuals, for predicting y (R1); predicting x requires the x-on-y line (R1); they differ unless r = ±1 (R1).', 3, 'explain')


@R.add('ch10-st5', 'C4', (3, 5), 'multi_step', style='ext')
def xony_parts(rng, slot):
    xs_, ys_ = _bivar(rng, 8)
    r, a, b, c, d = _reg(xs_, ys_)
    tab = '; '.join(f'({u}, {v})' for u, v in zip(xs_, ys_))
    xp = rng.randint(min(xs_), max(xs_))
    yp = round(mean(ys_))
    parts = [('Find r.', s3(r), 'A1', 1, True),
             ('Find the regression line of y on x.', lin_txt(a, b), 'A1 A1', 2, True),
             ('Find the regression line of x on y.', lin_txt(c, d, 'x', 'y'), 'A1 A1', 2, True),
             (f'Estimate y when x = {xp}, and estimate x when y = {yp}.', f'{s3(a * xp + b)}; {s3(c * yp + d)}', 'A1 A1', 2, True),
             ('Show that both lines pass through (x̄, ȳ).', f'({s3(mean(xs_))}, {s3(mean(ys_))})', 'M1 A1', 2, False)]
    return build_parts(rng, [f'Bivariate data (x, y) are given: {tab}.', f'Eight pairs of measurements were made: {tab}.'], parts, 4)


# =============================================================================================
# ch11 Probability (SL 4.5–4.6; AHL 4.13)
# =============================================================================================
def Fr_(v):
    return P(sp.nsimplify(v))


R.facts('ch11-st1', F(
    terms=[('sample space', 'the set U of all possible outcomes of a trial'),
           ('event', 'a subset of the sample space, i.e. a set of outcomes'),
           ('complementary event', "the event A′ that A does not occur, with P(A′) = 1 − P(A)"),
           ('expected number of occurrences', 'the value n × P(A) for n repeated trials')],
    facts=[('Two fair dice are thrown. The probability of a total of 7 is', '1/6', ['1/12', '7/36', '1/36'], '6 of 36 outcomes.'),
           ('If P(A) = 0.35 then P(A′) =', '0.65', ['0.35', '−0.35', '1.35'], '1 − P(A).'),
           ('A coin is tossed 3 times. The number of outcomes in the sample space is', '8', ['3', '6', '9'], '2³.'),
           ('A fair die is rolled 120 times. The expected number of sixes is', '20', ['6', '12', '24'], '120 × 1/6.')],
    why=[('Explain why probabilities of equally likely outcomes can be found by counting.', 'If all n outcomes are equally likely, each has probability 1/n, so an event containing k outcomes has probability k/n.'),
         ('Explain the difference between theoretical and experimental probability.', 'Theoretical probability is calculated from a model of equally likely outcomes; experimental probability is the relative frequency observed in trials, which approaches the theoretical value as the number of trials grows.'),
         ('Explain why the expected number of occurrences need not be a whole number.', 'It is a long-run average nP(A), not an actual count; e.g. 10 rolls of a die give an expected 10/6 ≈ 1.67 sixes.')],
    misc=[('Since a coin landed heads 5 times in a row, tails is more likely next.', 'Tosses are independent; P(tails) is still 1/2.'),
          ('Rolling two dice, a total of 2 and a total of 7 are equally likely because each is one total.', 'A total of 2 arises in 1 way, 7 in 6 ways, so P(7) = 6/36 > P(2) = 1/36.')],
))


@R.add('ch11-st1', 'C1', (1, 3), 'mcq')
def prob_basic_mcq(rng, slot):
    kind = rng.choice(['dice', 'cards', 'expect'])
    if kind == 'dice':
        t = rng.randint(2, 12)
        ways = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == t)
        return mcq(rng, f'Two fair six-sided dice are rolled. The probability that the total is {t} is', Fr_(sp.Rational(ways, 36)), [Fr_(sp.Rational(ways + 1, 36)), Fr_(sp.Rational(1, 11)), Fr_(sp.Rational(t, 36))] if ways + 1 != t else [Fr_(sp.Rational(ways + 2, 36)), Fr_(sp.Rational(1, 11)), Fr_(sp.Rational(t + 1, 36))], f'{ways} outcomes of 36.')
    if kind == 'cards':
        r, b = rng.randint(2, 9), rng.randint(2, 9)
        return mcq(rng, f'A bag contains {r} red and {b} blue counters. One counter is drawn at random. P(blue) =', Fr_(sp.Rational(b, r + b)), [Fr_(sp.Rational(r, r + b)), Fr_(sp.Rational(b, r)) if b != r else Fr_(sp.Rational(1, r + b)), Fr_(sp.Rational(1, b))], 'Favourable over total.')
    p, n = rng.choice([(sp.Rational(1, 4), 80), (sp.Rational(2, 5), 150), (sp.Rational(3, 8), 240), (sp.Rational(1, 6), 300)])
    return mcq(rng, f'An event has probability {Fr_(p)}. In {n} trials the expected number of occurrences is', str(p * n), [str(p * n + 10), str(n - p * n), Fr_(p)], 'nP(A).')


@R.add('ch11-st1', 'C3', (1, 4), 'short', style='p1')
def sample_space(rng, slot):
    kind = rng.choice(['dice', 'spinners', 'coins'])
    if kind == 'dice':
        op = rng.choice(['sum', 'product', 'difference'])
        f = {'sum': lambda a, b: a + b, 'product': lambda a, b: a * b, 'difference': lambda a, b: abs(a - b)}[op]
        vals = sorted(set(f(a, b) for a in range(1, 7) for b in range(1, 7)))
        cond = rng.choice(['prime', 'even', 'gt'])
        if cond == 'gt':
            k = rng.choice(vals[1:-1])
            ok = [(a, b) for a in range(1, 7) for b in range(1, 7) if f(a, b) > k]
            ct = f'greater than {k}'
        elif cond == 'prime':
            ok = [(a, b) for a in range(1, 7) for b in range(1, 7) if sp.isprime(f(a, b))]
            ct = 'a prime number'
        else:
            ok = [(a, b) for a in range(1, 7) for b in range(1, 7) if f(a, b) % 2 == 0]
            ct = 'even'
        return mk(f'Two fair six-sided dice are rolled and the {op} of the scores is recorded. Draw a sample space diagram and find the probability that the {op} is {ct}.', Fr_(sp.Rational(len(ok), 36)),
                  f'36 equally likely outcomes in a 6 × 6 grid (M1); {len(ok)} favourable (A1); {Fr_(sp.Rational(len(ok), 36))} (A1).', 3)
    if kind == 'spinners':
        a, b = rng.randint(3, 5), rng.randint(3, 6)
        tgt = rng.randint(3, a + b - 1)
        ok = sum(1 for i in range(1, a + 1) for j in range(1, b + 1) if i + j >= tgt)
        return mk(f'A fair spinner numbered 1 to {a} and a fair spinner numbered 1 to {b} are spun. Find the probability that the total is at least {tgt}.', Fr_(sp.Rational(ok, a * b)),
                  f'{a * b} equally likely outcomes (M1); {ok} with total ≥ {tgt} (A1); {Fr_(sp.Rational(ok, a * b))} (A1).', 3)
    n = rng.choice([3, 4])
    k = rng.randint(1, n - 1)
    cnt = math.comb(n, k)
    atl = sum(math.comb(n, j) for j in range(k, n + 1))
    return mk(f'A fair coin is tossed {n} times. List or count the sample space and find the probability of (i) exactly {k} heads, (ii) at least {k} heads.', f'(i) {Fr_(sp.Rational(cnt, 2 ** n))} (ii) {Fr_(sp.Rational(atl, 2 ** n))}',
              f'{2 ** n} outcomes (A1); {cnt} with exactly {k} heads (A1); {atl} with at least {k} (A1).', 3)


@R.add('ch11-st1', 'C3', (2, 4), 'short', style='p2')
def relfreq(rng, slot):
    n = rng.choice([200, 250, 400, 500])
    cats = rng.choice([['red', 'green', 'blue', 'yellow'], ['A', 'B', 'C', 'D'], ['walk', 'bus', 'car', 'cycle']])
    counts = [rng.randint(20, 120) for _ in cats[:-1]]
    if sum(counts) >= n:
        return None
    counts.append(n - sum(counts))
    i = rng.randrange(len(cats))
    m = rng.choice([1200, 1500, 2000, 3000])
    return mk(f'In {n} trials the outcomes were: ' + ', '.join(f'{c_} {k}' for c_, k in zip(cats, counts)) + f'. Estimate the probability of "{cats[i]}" and the expected number of "{cats[i]}" outcomes in {m} further trials.',
              f'{s3(counts[i] / n)}; {s3(counts[i] / n * m)}', f'relative frequency {counts[i]}/{n} (A1); × {m} (M1); {s3(counts[i] / n * m)} (A1).', 3)


@R.add('ch11-st1', 'C2', (2, 4), 'explain')
def prob_explain(rng, slot):
    n = rng.randint(4, 8)
    return mk(f'A fair coin shows heads {n} times in a row. {who(rng)} says the next toss is more likely to be tails. Explain whether this is correct.', 'incorrect: P(tails) = 1/2',
              'tosses are independent (R1); the coin has no memory, so previous results do not affect the next (R1); P(tails) = 1/2 (A1).', 3, 'explain')


@R.add('ch11-st1', 'C4', (3, 5), 'multi_step', style='ext')
def dice_game_parts(rng, slot):
    win = rng.randint(2, 5)
    cost = rng.choice([1, 2])
    ok = [(a, b) for a in range(1, 7) for b in range(1, 7) if a == b]
    sixes = [(a, b) for a in range(1, 7) for b in range(1, 7) if 6 in (a, b)]
    tot = rng.randint(8, 10)
    big = [(a, b) for a in range(1, 7) for b in range(1, 7) if a + b >= tot]
    parts = [('Find the probability that the two scores are equal.', '1/6', 'A1', 1, True),
             ('Find the probability that at least one score is a 6.', Fr_(sp.Rational(len(sixes), 36)), 'complement 1 − 25/36 (M1) A1', 2, True),
             (f'Find the probability that the total is at least {tot}.', Fr_(sp.Rational(len(big), 36)), 'A1', 1, True),
             (f'A player pays ${cost} to play and wins ${win} if the scores are equal. Find the expected number of wins in 60 games and the player\'s expected total gain.', f'10; {"−" if 10 * win - 60 * cost < 0 else ""}${abs(10 * win - 60 * cost)}', 'M1 A1 A1', 3, True),
             ('Find the probability that the scores are equal or at least one is a 6.', Fr_(sp.Rational(len(set(ok) | set(sixes)), 36)), 'addition rule, subtract overlap (M1) A1', 2, False)]
    return build_parts(rng, ['Two fair six-sided dice are rolled.', 'In a game, two fair six-sided dice are rolled once.'], parts, 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch11-st2', F(
    terms=[('Venn diagram', 'a diagram of overlapping regions within the sample space used to show events and their intersections'),
           ('tree diagram', 'a branching diagram for successive trials, on which probabilities along a path are multiplied'),
           ('mutually exclusive events', 'events that cannot happen together: P(A ∩ B) = 0'),
           ('combined events (addition rule)', 'the rule P(A ∪ B) = P(A) + P(B) − P(A ∩ B)')],
    facts=[('If P(A) = 0.5, P(B) = 0.4 and P(A ∩ B) = 0.2, then P(A ∪ B) =', '0.7', ['0.9', '0.2', '0.1'], 'Addition rule.'),
           ('For mutually exclusive A and B, P(A ∪ B) =', 'P(A) + P(B)', ['P(A)P(B)', 'P(A) + P(B) − P(A)P(B)', '1'], 'No overlap.'),
           ('On a tree diagram, probabilities along a branch path are', 'multiplied', ['added', 'subtracted', 'averaged'], 'Successive events.'),
           ('P(A ∩ B′) equals', 'P(A) − P(A ∩ B)', ['P(A) − P(B)', '1 − P(A ∩ B)', 'P(A)P(B)'], 'A only.')],
    why=[('Explain why P(A ∩ B) is subtracted in the addition rule.', 'Adding P(A) and P(B) counts the outcomes in both events twice, so the overlap is subtracted once.'),
         ('Explain why the probabilities on the branches from one point of a tree diagram add to 1.', 'They are the probabilities of all the possible outcomes of that stage, which are mutually exclusive and exhaustive.'),
         ('Explain why "without replacement" changes the second-stage probabilities on a tree diagram.', 'Removing an item changes the numbers left, so the probabilities at the second stage depend on what was drawn first.')],
    misc=[('If P(A) = 0.6 and P(B) = 0.7 then P(A ∪ B) = 1.3.', 'A probability cannot exceed 1; the events must overlap, P(A ∩ B) ≥ 0.3.'),
          ('Mutually exclusive events are independent.', 'If P(A), P(B) > 0, mutually exclusive events are dependent: P(A ∩ B) = 0 ≠ P(A)P(B).')],
))


@R.add('ch11-st2', 'C1', (1, 3), 'mcq')
def venn_mcq(rng, slot):
    a, b, ab = rng.choice([(0.5, 0.4, 0.2), (0.6, 0.3, 0.1), (0.45, 0.35, 0.15), (0.7, 0.5, 0.3), (0.3, 0.25, 0.05)])
    return mcq(rng, f'P(A) = {a}, P(B) = {b}, P(A ∩ B) = {ab}. P(A ∪ B) =', f'{a + b - ab:.2g}', [f'{a + b:.2g}', f'{a + b - 2 * ab:.2g}', f'{1 - (a + b - ab):.2g}'], 'Addition rule.')


@R.add('ch11-st2', 'C3', (1, 4), 'short', style='p1')
def venn_count(rng, slot):
    N = rng.choice([30, 40, 50, 60])
    a_only, b_only, both = rng.randint(3, 15), rng.randint(3, 15), rng.randint(2, 10)
    nei = N - a_only - b_only - both
    if nei < 0:
        return None
    sA, sB = rng.choice([('play football', 'play basketball'), ('study French', 'study Spanish'), ('own a cat', 'own a dog'), ('like tea', 'like coffee')])
    kind = rng.choice(['both', 'neither', 'cond'])
    stem = f'In a group of {N} students, {a_only + both} {sA}, {b_only + both} {sB} and {nei} do neither.'
    if kind == 'both':
        return mk(stem + f' Draw a Venn diagram and find the probability that a randomly chosen student does both.', Fr_(sp.Rational(both, N)),
                  f'n(A ∪ B) = {N - nei} (A1); n(A ∩ B) = {a_only + both} + {b_only + both} − {N - nei} = {both} (M1 A1); {Fr_(sp.Rational(both, N))} (A1).', 4)
    if kind == 'neither':
        return mk(stem + f' Find the probability that a randomly chosen student does exactly one of the two.', Fr_(sp.Rational(a_only + b_only, N)),
                  f'both = {both} (M1 A1); exactly one {a_only} + {b_only} = {a_only + b_only} (A1); {Fr_(sp.Rational(a_only + b_only, N))} (A1).', 4)
    return mk(stem + f' A student who does at least one is chosen at random. Find the probability that they {sA.split()[0]} {" ".join(sA.split()[1:])} but not {sB.split()[-1]}.', Fr_(sp.Rational(a_only, N - nei)),
              f'Venn diagram (M1); {a_only} in A only (A1); {Fr_(sp.Rational(a_only, N - nei))} (A1).', 3)


@R.add('ch11-st2', 'C3', (2, 5), 'short', style='p1')
def tree_noreplace(rng, slot):
    r, b = rng.randint(3, 8), rng.randint(2, 7)
    n = r + b
    kind = rng.choice(['same', 'diff', 'atleast'])
    rr = sp.Rational(r * (r - 1), n * (n - 1))
    bb = sp.Rational(b * (b - 1), n * (n - 1))
    if kind == 'same':
        return mk(f'A bag contains {r} red and {b} blue marbles. Two marbles are taken at random without replacement. Find the probability that they are the same colour.', Fr_(rr + bb),
                  f'tree diagram without replacement (M1); P(RR) = {Fr_(rr)} (A1); P(BB) = {Fr_(bb)} (A1); {Fr_(rr + bb)} (A1).', 4)
    if kind == 'diff':
        return mk(f'A bag contains {r} red and {b} blue marbles. Two marbles are taken at random without replacement. Find the probability that they are different colours.', Fr_(1 - rr - bb),
                  f'P(RB) + P(BR) = 2 × {r}/{n} × {b}/{n - 1} (M1 A1); {Fr_(1 - rr - bb)} (A1).', 3)
    return mk(f'A bag contains {r} red and {b} blue marbles. Two marbles are taken at random without replacement. Find the probability that at least one is blue.', Fr_(1 - rr),
              f'complement: 1 − P(RR) (M1); P(RR) = {r}/{n} × {r - 1}/{n - 1} (A1); {Fr_(1 - rr)} (A1).', 3)


@R.add('ch11-st2', 'C3', (2, 4), 'short', style='p2')
def tree_decimal(rng, slot):
    p1, p2, p3 = rng.choice([0.6, 0.7, 0.75, 0.8, 0.65]), rng.choice([0.85, 0.9, 0.7, 0.8]), rng.choice([0.3, 0.4, 0.25, 0.5])
    ctx = rng.choice([('it rains', 'the bus is late'), ('a student revises', 'they pass'), ('a machine is serviced', 'it works all day')])
    kind = rng.choice(['total', 'neither'])
    if kind == 'total':
        pt_ = p1 * p3 + (1 - p1) * (1 - p2) if False else p1 * p2 + (1 - p1) * p3
        return mk(f'The probability that {ctx[0]} is {p1}. If {ctx[0]}, the probability that {ctx[1]} is {p2}; otherwise it is {p3}. Draw a tree diagram and find the probability that {ctx[1]}.', s3(pt_) if len(f'{pt_:.4f}'.rstrip('0')) > 6 else f'{pt_:.4f}'.rstrip('0'),
                  f'tree diagram (M1); {p1} × {p2} + {1 - p1:.2f} × {p3} (M1 A1); {pt_:.4f} (A1).'.replace('0000', ''), 4)
    q = (1 - p1) * (1 - p3)
    return mk(f'The probability that {ctx[0]} is {p1}. If {ctx[0]}, the probability that {ctx[1]} is {p2}; otherwise it is {p3}. Find the probability that neither event happens.', f'{q:.4f}'.rstrip('0'),
              f'P(not first) × P(not second | not first) = {1 - p1:.2f} × {1 - p3:.2f} (M1 A1); {q:.4f} (A1).'.replace('0000', ''), 3)


@R.add('ch11-st2', 'C2', (2, 4), 'explain')
def venn_explain(rng, slot):
    a, b = rng.choice([(0.6, 0.7), (0.55, 0.65), (0.8, 0.4), (0.45, 0.75)])
    return mk(f'P(A) = {a} and P(B) = {b}. Explain why A and B cannot be mutually exclusive, and find the least possible value of P(A ∩ B).', f'{a + b - 1:.2g}',
              f'if mutually exclusive, P(A ∪ B) = {a + b:.2g} > 1, impossible (R1); P(A ∩ B) = P(A) + P(B) − P(A ∪ B) ≥ {a + b:.2g} − 1 (M1); {a + b - 1:.2g} (A1).', 3, 'explain')


@R.add('ch11-st2', 'C4', (3, 5), 'multi_step', style='ext')
def venn_parts(rng, slot):
    N = rng.choice([40, 50, 60, 80, 100])
    ab, a_, b_ = rng.randint(4, 12), rng.randint(5, 20), rng.randint(5, 20)
    nei = N - ab - a_ - b_
    if nei < 3:
        return None
    sA, sB = rng.choice([('swimming', 'tennis'), ('History', 'Geography'), ('a laptop', 'a tablet'), ('breakfast', 'lunch at school')])
    parts = [(f'Draw a Venn diagram to represent the information.', f'A only {a_}, both {ab}, B only {b_}, neither {nei}', 'A1 A1', 2, True),
             (f'Find the probability that a person chosen at random chooses {sA} or {sB}.', Fr_(sp.Rational(N - nei, N)), 'A1', 1, True),
             (f'Find the probability that a person chooses exactly one of them.', Fr_(sp.Rational(a_ + b_, N)), 'A1', 1, True),
             (f'Two people are chosen at random without replacement. Find the probability that both chose neither.', Fr_(sp.Rational(nei * (nei - 1), N * (N - 1))), 'M1 A1', 2, True),
             (f'Determine whether choosing {sA} and choosing {sB} are independent.', 'independent' if sp.Rational(ab, N) == sp.Rational(a_ + ab, N) * sp.Rational(b_ + ab, N) else 'not independent', 'compare P(A ∩ B) with P(A)P(B) (M1) A1', 2, False)]
    return build_parts(rng, [f'In a survey of {N} people, {a_ + ab} chose {sA}, {b_ + ab} chose {sB} and {ab} chose both.', f'{N} people were asked whether they choose {sA} and {sB}: {a_ + ab} choose {sA}, {b_ + ab} choose {sB} and {ab} choose both.'], parts, 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch11-st3', F(
    terms=[('conditional probability', 'the probability of A given that B has occurred: P(A | B) = P(A ∩ B)/P(B)'),
           ('independent events', 'events with P(A | B) = P(A), equivalently P(A ∩ B) = P(A)P(B)'),
           ('two-way table', 'a table of frequencies classified by two categorical variables, used to find joint and conditional probabilities')],
    facts=[('If A and B are independent with P(A) = 0.3, P(B) = 0.5, then P(A ∩ B) =', '0.15', ['0.8', '0.2', '0.65'], 'Multiply.'),
           ('P(A | B) =', 'P(A ∩ B)/P(B)', ['P(A ∩ B)/P(A)', 'P(A)P(B)', 'P(B | A)'], 'Definition.'),
           ('If P(A | B) = P(A), then A and B are', 'independent', ['mutually exclusive', 'complementary', 'impossible'], 'B does not affect A.'),
           ('If A and B are independent, so are', 'A and B′', ['A and A′', 'A ∩ B and A', 'none of these'], 'Independence passes to complements.')],
    why=[('Explain the difference between independent and mutually exclusive events.', 'Independent events do not affect each other\'s probabilities (P(A ∩ B) = P(A)P(B)); mutually exclusive events cannot occur together (P(A ∩ B) = 0).'),
         ('Explain why P(A | B) is generally not equal to P(B | A).', 'They divide the same joint probability P(A ∩ B) by different quantities, P(B) and P(A) respectively.'),
         ('Explain why conditioning on B reduces the sample space.', 'Given that B has occurred, only outcomes in B are possible, so probabilities are found relative to P(B).')],
    misc=[('P(A | B) = P(A ∩ B)/P(A).', 'The denominator is the probability of the given event: P(A ∩ B)/P(B).'),
          ('If P(A ∩ B) = 0.12, P(A) = 0.3 and P(B) = 0.5, then A and B are independent.', 'P(A)P(B) = 0.15 ≠ 0.12, so they are not independent.')],
))


@R.add('ch11-st3', 'C1', (1, 3), 'mcq')
def cond_mcq(rng, slot):
    pab, pb = rng.choice([(0.12, 0.4), (0.2, 0.5), (0.15, 0.6), (0.06, 0.3), (0.18, 0.45)])
    return mcq(rng, f'P(A ∩ B) = {pab} and P(B) = {pb}. P(A | B) =', f'{pab / pb:.3g}', [f'{pab * pb:.3g}', f'{pb - pab:.3g}', f'{pab + pb:.3g}'], 'P(A ∩ B)/P(B).')


@R.add('ch11-st3', 'C3', (2, 5), 'short', style='p1')
def cond_table(rng, slot):
    rows = rng.choice([('Year 11', 'Year 12'), ('male', 'female'), ('under 30', '30 or over')])
    cols = rng.choice([('walk', 'bus', 'car'), ('tea', 'coffee', 'juice'), ('science', 'arts', 'sport')])
    T = [[rng.randint(4, 25) for _ in cols] for _ in rows]
    N = sum(map(sum, T))
    i, j = rng.randrange(2), rng.randrange(3)
    kind = rng.choice(['given_row', 'given_col', 'indep'])
    tab = '; '.join(f'{rows[r]}: ' + ', '.join(f'{cols[c]} {T[r][c]}' for c in range(3)) for r in range(2))
    if kind == 'given_row':
        return mk(f'The table shows the choices of {N} people. {tab}. A person is chosen at random. Given that they are {rows[i]}, find the probability that they chose {cols[j]}.', Fr_(sp.Rational(T[i][j], sum(T[i]))),
                  f'restrict to {rows[i]}: {sum(T[i])} people (M1); {T[i][j]} chose {cols[j]} (A1); {Fr_(sp.Rational(T[i][j], sum(T[i])))} (A1).', 3)
    if kind == 'given_col':
        cs = T[0][j] + T[1][j]
        return mk(f'The table shows the choices of {N} people. {tab}. A person who chose {cols[j]} is selected at random. Find the probability that they are {rows[i]}.', Fr_(sp.Rational(T[i][j], cs)),
                  f'column total {cs} (M1); {T[i][j]} (A1); {Fr_(sp.Rational(T[i][j], cs))} (A1).', 3)
    pa = sp.Rational(sum(T[i]), N)
    pb = sp.Rational(T[0][j] + T[1][j], N)
    pab = sp.Rational(T[i][j], N)
    ind = pab == pa * pb
    return mk(f'The table shows the choices of {N} people. {tab}. Determine whether the events "{rows[i]}" and "chose {cols[j]}" are independent.', 'independent' if ind else 'not independent',
              f'P({rows[i]}) = {Fr_(pa)}, P({cols[j]}) = {Fr_(pb)} (A1); P(both) = {Fr_(pab)} (A1); compare with the product {Fr_(pa * pb)} (M1); conclusion (A1).', 4)


@R.add('ch11-st3', 'C3', (2, 5), 'short', style='p1')
def indep_algebra(rng, slot):
    pa, pb = rng.choice([(sp.Rational(1, 3), sp.Rational(1, 4)), (sp.Rational(2, 5), sp.Rational(1, 2)), (sp.Rational(3, 10), sp.Rational(2, 5)), (sp.Rational(1, 4), sp.Rational(3, 5)), (sp.Rational(2, 3), sp.Rational(1, 6))])
    kind = rng.choice(['union', 'findb', 'cond'])
    if kind == 'union':
        u = pa + pb - pa * pb
        return mk(f'A and B are independent events with P(A) = {Fr_(pa)} and P(B) = {Fr_(pb)}. Find P(A ∪ B) and P(A′ ∩ B).', f'{Fr_(u)}; {Fr_((1 - pa) * pb)}',
                  f'P(A ∩ B) = {Fr_(pa * pb)} (A1); P(A ∪ B) = {Fr_(u)} (M1 A1); P(A′)P(B) = {Fr_((1 - pa) * pb)} (A1).', 4)
    if kind == 'findb':
        u = pa + pb - pa * pb
        return mk(f'A and B are independent, P(A) = {Fr_(pa)} and P(A ∪ B) = {Fr_(u)}. Find P(B).', Fr_(pb),
                  f'{Fr_(u)} = {Fr_(pa)} + p − {Fr_(pa)}p (M1 A1); solve: p = {Fr_(pb)} (A1).', 3)
    pab = pa * pb * rng.choice([sp.Rational(1, 2), sp.Rational(3, 2), 1])
    if pab > min(pa, pb):
        return None
    return mk(f'P(A) = {Fr_(pa)}, P(B) = {Fr_(pb)} and P(A ∩ B) = {Fr_(pab)}. Find P(A | B) and P(B | A′), and state whether A and B are independent.', f'{Fr_(pab / pb)}; {Fr_((pb - pab) / (1 - pa))}; ' + ('independent' if pab == pa * pb else 'not independent'),
              f'P(A | B) = {Fr_(pab)}/{Fr_(pb)} (M1 A1); P(A′ ∩ B) = {Fr_(pb - pab)} (A1); P(B | A′) = {Fr_((pb - pab) / (1 - pa))} (A1); compare with P(A) (R1).', 5)


@R.add('ch11-st3', 'C3', (2, 4), 'short', style='p2')
def cond_gdc(rng, slot):
    pa, pb_a, pb_na = rng.choice([0.35, 0.4, 0.55, 0.62]), rng.choice([0.8, 0.72, 0.9]), rng.choice([0.25, 0.3, 0.15])
    pb = pa * pb_a + (1 - pa) * pb_na
    ctx = rng.choice([('a customer is a member', 'they buy coffee'), ('a day is a weekday', 'the train is crowded'), ('a student takes HL Maths', 'they take Physics')])
    return mk(f'The probability that {ctx[0]} is {pa}. If {ctx[0]}, the probability that {ctx[1]} is {pb_a}; otherwise it is {pb_na}. Find the probability that {ctx[1]}, and the probability that {ctx[0]} given that {ctx[1]}.', f'{s3(pb)}; {s3(pa * pb_a / pb)}',
              f'P(B) = {pa} × {pb_a} + {1 - pa:.2f} × {pb_na} = {s3(pb)} (M1 A1); P(A | B) = {s3(pa * pb_a)}/{s3(pb)} (M1); {s3(pa * pb_a / pb)} (A1).', 4)


@R.add('ch11-st3', 'C2', (2, 4), 'explain')
def indep_explain(rng, slot):
    pa, pb = rng.choice([(0.3, 0.4), (0.5, 0.2), (0.25, 0.6)])
    return mk(f'{who(rng)} says that events A and B with P(A) = {pa}, P(B) = {pb} and P(A ∩ B) = 0 are independent because "they don\'t affect each other". Explain why this is wrong.', 'they are mutually exclusive, hence dependent',
              f'independence requires P(A ∩ B) = P(A)P(B) = {pa * pb:.2g} (R1); here P(A ∩ B) = 0 ≠ {pa * pb:.2g} (A1); knowing A occurred means B cannot occur, so they are dependent (R1).', 3, 'explain')


@R.add('ch11-st3', 'C4', (3, 5), 'multi_step', style='ext')
def cond_parts(rng, slot):
    r, b = rng.randint(3, 7), rng.randint(3, 7)
    n = r + b
    rr = sp.Rational(r * (r - 1), n * (n - 1))
    rb = sp.Rational(r * b, n * (n - 1))
    parts = [('Draw a tree diagram to show the possible outcomes.', 'branches R/B then R/B with denominators n and n − 1', 'A1 A1', 2, True),
             ('Find the probability that the second sweet is red.', Fr_(rr + sp.Rational(b * r, n * (n - 1))), 'M1 A1', 2, True),
             ('Given that the second sweet is red, find the probability that the first was also red.', Fr_(rr / (rr + sp.Rational(b * r, n * (n - 1)))), 'conditional (M1) A1 A1', 3, True),
             ('Determine whether the events "first is red" and "second is red" are independent.', 'not independent', 'compare (M1) R1', 2, True),
             ('The sweets are now replaced after each draw. Find P(both red) and comment on independence.', f'{Fr_(sp.Rational(r * r, n * n))}; independent', 'A1 R1', 2, False)]
    return build_parts(rng, [f'A bag contains {r} red and {b} blue sweets. Two sweets are taken at random without replacement.', f'Two sweets are taken at random, one after the other without replacement, from a bag of {r} red and {b} blue sweets.'], parts, 4)


@R.add('ch11-st3', 'C4', (4, 5), 'multi_step', style='p3')
def prob_p3(rng, slot):
    n = rng.choice([3, 4, 5])
    parts = [(f'A fair coin is tossed {n} times. Let A be "the first toss is a head" and B be "there are more heads than tails". Find P(A), P(B) and P(A ∩ B).', None, 'A1 A1 A1', 3, True),
             ('Determine whether A and B are independent.', None, 'M1 R1', 2, True),
             ('Prove that if A and B are independent, then A′ and B′ are independent.', "P(A′ ∩ B′) = 1 − P(A ∪ B) = (1 − P(A))(1 − P(B))", 'M1 A1 A1', 3, True),
             ('Three events A, B, C are pairwise independent. Give an example (e.g. with two coin tosses) where P(A ∩ B ∩ C) ≠ P(A)P(B)P(C).', 'A: first head, B: second head, C: tosses match; P(A ∩ B ∩ C) = 1/4 ≠ 1/8', 'A1 R1 A1', 3, True),
             ('Generalise: for n tosses, show P(B) = 1/2 when n is odd.', 'symmetry between heads and tails', 'R1', 1, False)]
    from itertools import product
    outs = list(product('HT', repeat=n))
    A = [o for o in outs if o[0] == 'H']
    B = [o for o in outs if o.count('H') > o.count('T')]
    AB = [o for o in A if o in B]
    pa, pb, pab = sp.Rational(len(A), len(outs)), sp.Rational(len(B), len(outs)), sp.Rational(len(AB), len(outs))
    parts[0] = (parts[0][0], f'{Fr_(pa)}; {Fr_(pb)}; {Fr_(pab)}', parts[0][2], 3, True)
    parts[1] = (parts[1][0], 'independent' if pab == pa * pb else f'not independent: {Fr_(pab)} ≠ {Fr_(pa * pb)}', parts[1][2], 2, True)
    return build_parts(rng, ['This question explores independence.', 'In this question all coins are fair.'], parts, 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch11-st4', F(
    terms=[("Bayes' theorem", 'the formula P(A | B) = P(B | A)P(A)/[P(B | A)P(A) + P(B | A′)P(A′)], reversing a conditional probability'),
           ('false positive', 'a positive test result for someone who does not have the condition'),
           ('law of total probability', 'the rule P(B) = P(B | A)P(A) + P(B | A′)P(A′)')],
    facts=[("Bayes' theorem is used to find", 'P(A | B) from P(B | A)', ['P(A ∪ B)', 'P(A)P(B)', 'P(A′)'], 'Reverse conditioning.'),
           ('A rare disease and an accurate test often give', 'a low P(disease | positive)', ['P(disease | positive) = 1', 'no false positives', 'P(positive) = 0'], 'Many false positives relative to true ones.'),
           ('The denominator in Bayes\' theorem is', 'P(B)', ['P(A)', 'P(A ∩ B)', '1'], 'Total probability.')],
    why=[('Explain why a positive result from a 95% accurate test for a rare disease may still be unlikely to mean the person has the disease.', 'When the disease is rare, the healthy group is huge, so even a small false-positive rate produces more false positives than true positives.'),
         ("Explain how a tree diagram represents Bayes' theorem.", 'The numerator is one path (A then B); the denominator is the sum of all paths ending in B; the ratio gives P(A | B).')],
    misc=[('If P(positive | disease) = 0.99, then P(disease | positive) = 0.99.', 'These are different; P(disease | positive) also depends on how common the disease is and the false-positive rate.'),
          ('Bayes\' theorem: P(A | B) = P(B | A)/P(B).', 'The numerator is P(B | A)P(A).')],
))


@R.add('ch11-st4', 'C1', (1, 3), 'mcq')
def bayes_mcq(rng, slot):
    pa, pba, pbna = rng.choice([(0.5, 0.6, 0.2), (0.3, 0.8, 0.4), (0.4, 0.5, 0.25), (0.2, 0.9, 0.1)])
    pb = pa * pba + (1 - pa) * pbna
    ans = pa * pba / pb
    return mcq(rng, f'P(A) = {pa}, P(B | A) = {pba}, P(B | A′) = {pbna}. P(A | B) =', f'{ans:.3g}', [f'{pba:.3g}', f'{pa * pba:.3g}', f'{pb:.3g}'], 'Bayes: P(A)P(B|A)/P(B).')


@R.add('ch11-st4', 'C3', (2, 5), 'short', style='p2')
def bayes_test(rng, slot):
    prev = rng.choice([0.001, 0.005, 0.01, 0.02, 0.05])
    sens = rng.choice([0.9, 0.95, 0.98, 0.99])
    fp = rng.choice([0.02, 0.05, 0.08, 0.1])
    pb = prev * sens + (1 - prev) * fp
    post = prev * sens / pb
    return mk(f'A condition affects {prev * 100:g}% of a population. A test detects it in {sens * 100:g}% of people who have it, but gives a positive result for {fp * 100:g}% of people who do not. A person tests positive. Find the probability that they have the condition.', s3(post),
              f'P(+) = {prev} × {sens} + {1 - prev:g} × {fp} = {s3(pb)} (M1 A1); P(C | +) = {s3(prev * sens)}/{s3(pb)} (M1); {s3(post)} (A1).', 4)


@R.add('ch11-st4', 'C3', (2, 5), 'short', style='p1')
def bayes_exact(rng, slot):
    k = rng.choice([2, 3])
    names = ['A', 'B', 'C'][:k]
    shares = rng.choice([[sp.Rational(1, 2), sp.Rational(1, 2)], [sp.Rational(2, 5), sp.Rational(3, 5)], [sp.Rational(1, 4), sp.Rational(3, 4)]]) if k == 2 else rng.choice([[sp.Rational(1, 2), sp.Rational(1, 4), sp.Rational(1, 4)], [sp.Rational(1, 5), sp.Rational(3, 10), sp.Rational(1, 2)]])
    defect = [sp.Rational(rng.randint(1, 9), 100) for _ in names]
    pdef = sum(s_ * d for s_, d in zip(shares, defect))
    i = rng.randrange(k)
    post = shares[i] * defect[i] / pdef
    desc = '; '.join(f'machine {n} makes {Fr_(s_)} of the items, of which {int(d * 100)}% are faulty' for n, s_, d in zip(names, shares, defect))
    return mk(f'In a factory, {desc}. An item is chosen at random and found to be faulty. Find the probability that it was made by machine {names[i]}.', Fr_(post),
              f'P(faulty) = {" + ".join(f"{Fr_(s_)} × {Fr_(d)}" for s_, d in zip(shares, defect))} = {Fr_(pdef)} (M1 A1); P({names[i]} | faulty) = {Fr_(shares[i] * defect[i])}/{Fr_(pdef)} (M1); {Fr_(post)} (A1).', 4)


@R.add('ch11-st4', 'C2', (2, 4), 'explain')
def bayes_explain(rng, slot):
    prev, sens, fp = rng.choice([(0.01, 0.99, 0.05), (0.002, 0.95, 0.03), (0.005, 0.98, 0.02)])
    post = prev * sens / (prev * sens + (1 - prev) * fp)
    return mk(f'A test for a condition affecting {prev * 100:g}% of people is {sens * 100:g}% accurate for those who have it and gives false positives {fp * 100:g}% of the time. Explain why a positive result is far from certain to mean the condition is present.', f'P(condition | +) ≈ {s3(post)}',
              f'in 100 000 people about {prev * 100000 * sens:g} true positives (R1) versus about {(1 - prev) * 100000 * fp:g} false positives (R1); so P ≈ {s3(post)} (A1).', 3, 'explain')


@R.add('ch11-st4', 'C4', (3, 5), 'multi_step', style='ext')
def bayes_parts(rng, slot):
    p_r = rng.choice([0.2, 0.25, 0.3, 0.4])
    late_r, late_d = rng.choice([0.5, 0.6, 0.45]), rng.choice([0.1, 0.15, 0.05])
    pl = p_r * late_r + (1 - p_r) * late_d
    parts = [('Draw a tree diagram to represent this information.', 'rain/dry then late/on time', 'A1 A1', 2, True),
             ('Find the probability that the train is late on a given day.', s3(pl), 'M1 A1', 2, True),
             ('Given that the train is late, find the probability that it is raining.', s3(p_r * late_r / pl), 'M1 A1', 2, True),
             ('Given that the train is on time, find the probability that it is dry.', s3((1 - p_r) * (1 - late_d) / (1 - pl)), 'M1 A1', 2, True),
             ('Over 5 independent days, find the probability that the train is late on exactly 2 days.', s3(math.comb(5, 2) * pl ** 2 * (1 - pl) ** 3), 'binomial (M1) A1', 2, False)]
    return build_parts(rng, [f'On any day the probability of rain is {p_r}. If it rains, the probability that a train is late is {late_r}; if it is dry the probability is {late_d}.', f'The probability that it rains on a given day is {p_r}. The train is late with probability {late_r} on rainy days and {late_d} on dry days.'], parts, 4)


@R.add('ch11-st1', 'C4', (3, 5), 'multi_step', style='ext')
def spinner_parts(rng, slot):
    a, b = rng.randint(3, 6), rng.randint(3, 6)
    outs = [(i, j) for i in range(1, a + 1) for j in range(1, b + 1)]
    N = len(outs)
    k = rng.randint(4, a + b - 1)
    prod_even = sum(1 for i, j in outs if (i * j) % 2 == 0)
    tot_k = sum(1 for i, j in outs if i + j == k)
    gt = sum(1 for i, j in outs if i > j)
    n = rng.choice([60, 90, 120, 180])
    parts = [('Write down the number of outcomes in the sample space.', str(N), 'A1', 1, True),
             (f'Find the probability that the total is {k}.', Fr_(sp.Rational(tot_k, N)), 'A1', 1, True),
             ('Find the probability that the product of the scores is even.', Fr_(sp.Rational(prod_even, N)), 'M1 A1', 2, True),
             ('Find the probability that the first score is greater than the second.', Fr_(sp.Rational(gt, N)), 'M1 A1', 2, True),
             (f'The pair is spun {n} times. Find the expected number of times the total is {k}.', P(sp.Rational(tot_k * n, N)), 'A1', 1, True),
             ('Find the probability that the product is even given that the total is ' + str(k) + '.', Fr_(sp.Rational(sum(1 for i, j in outs if i + j == k and (i * j) % 2 == 0), tot_k)) if tot_k else '0', 'M1 A1', 2, False)]
    return build_parts(rng, [f'Two fair spinners are numbered 1 to {a} and 1 to {b}. Both are spun and the scores are recorded.', f'A fair {a}-sided spinner (1 to {a}) and a fair {b}-sided spinner (1 to {b}) are spun together.'], parts, 4)


@R.add('ch11-st3', 'C4', (3, 5), 'multi_step', style='ext')
def table_parts(rng, slot):
    rows = rng.choice([('Year 11', 'Year 12'), ('boys', 'girls'), ('morning shift', 'evening shift')])
    cols = rng.choice([('maths', 'science', 'languages'), ('football', 'swimming', 'music'), ('bus', 'bike', 'walk')])
    T = [[rng.randint(5, 30) for _ in cols] for _ in rows]
    N = sum(map(sum, T))
    j = rng.randrange(3)
    pr = sp.Rational(sum(T[0]), N)
    pc = sp.Rational(T[0][j] + T[1][j], N)
    pj = sp.Rational(T[0][j], N)
    tab = '; '.join(f'{rows[r]}: ' + ', '.join(f'{cols[c]} {T[r][c]}' for c in range(3)) for r in range(2))
    parts = [(f'Find the probability that a person chosen at random is in {rows[0]}.', Fr_(pr), 'A1', 1, True),
             (f'Find P({rows[0]} and {cols[j]}).', Fr_(pj), 'A1', 1, True),
             (f'Find P({cols[j]} | {rows[0]}).', Fr_(sp.Rational(T[0][j], sum(T[0]))), 'M1 A1', 2, True),
             (f'Find P({rows[1]} | {cols[j]}).', Fr_(sp.Rational(T[1][j], T[0][j] + T[1][j])), 'M1 A1', 2, True),
             (f'Determine whether "{rows[0]}" and "{cols[j]}" are independent.', 'independent' if pj == pr * pc else 'not independent', 'compare P(A ∩ B) with P(A)P(B) (M1) R1', 2, True),
             (f'Two different people are chosen at random. Find the probability that both chose {cols[j]}.', Fr_(sp.Rational((T[0][j] + T[1][j]) * (T[0][j] + T[1][j] - 1), N * (N - 1))), 'M1 A1', 2, False)]
    return build_parts(rng, [f'The table shows the choices of {N} people: {tab}.', f'A survey of {N} people gave the following results: {tab}.'], parts, 4)


@R.add('ch11-st3', 'C2', (2, 4), 'explain')
def cond_explain(rng, slot):
    pab, pa, pb = rng.choice([(0.1, 0.2, 0.5), (0.12, 0.3, 0.6), (0.06, 0.15, 0.4), (0.2, 0.25, 0.8)])
    return mk(f'P(A ∩ B) = {pab}, P(A) = {pa} and P(B) = {pb}. {who(rng)} says P(A | B) = P(B | A). Explain why this is false and find both values.', f'P(A | B) = {pab / pb:.3g}, P(B | A) = {pab / pa:.3g}',
              f'both use P(A ∩ B) but divide by different probabilities (R1); P(A | B) = {pab}/{pb} = {pab / pb:.3g} (A1); P(B | A) = {pab}/{pa} = {pab / pa:.3g} (A1).', 3, 'explain')


@R.add('ch11-st4', 'C2', (2, 4), 'explain')
def bayes_explain2(rng, slot):
    pa, pba, pbna = rng.choice([(0.3, 0.9, 0.2), (0.6, 0.5, 0.1), (0.2, 0.7, 0.4), (0.45, 0.8, 0.3)])
    pb = pa * pba + (1 - pa) * pbna
    return mk(f'P(A) = {pa}, P(B | A) = {pba} and P(B | A′) = {pbna}. {who(rng)} computes P(A | B) = {pba}/P(B). Explain the error and find P(A | B) correct to 3 significant figures.', s3(pa * pba / pb),
              f'the numerator must be P(A ∩ B) = P(B | A)P(A) = {pa * pba:.3g} (R1); P(B) = {s3(pb)} by total probability (M1); P(A | B) = {s3(pa * pba / pb)} (A1).', 3, 'explain')


@R.add('ch11-st4', 'C4', (3, 5), 'multi_step', style='ext')
def bayes_parts2(rng, slot):
    sA, sB = rng.choice([(sp.Rational(3, 5), sp.Rational(2, 5)), (sp.Rational(1, 4), sp.Rational(3, 4)), (sp.Rational(7, 10), sp.Rational(3, 10))])
    dA, dB = sp.Rational(rng.randint(1, 8), 100), sp.Rational(rng.randint(1, 8), 100)
    pd = sA * dA + sB * dB
    parts = [('Find the probability that a randomly chosen bulb is defective.', Fr_(pd), 'M1 A1', 2, True),
             ('Given that a bulb is defective, find the probability that it came from supplier A.', Fr_(sA * dA / pd), 'M1 A1', 2, True),
             ('Given that a bulb is not defective, find the probability that it came from supplier B.', Fr_(sB * (1 - dB) / (1 - pd)), 'M1 A1', 2, True),
             ('Two bulbs are chosen independently. Find the probability that exactly one is defective.', Fr_(2 * pd * (1 - pd)), 'M1 A1', 2, True),
             ('Explain whether "defective" and "from supplier A" are independent events.', 'independent' if dA == dB else 'not independent, since the defect rates differ', 'R1', 1, False)]
    return build_parts(rng, [f'A shop buys {Fr_(sA)} of its light bulbs from supplier A and the rest from supplier B. {int(dA * 100)}% of A\'s bulbs and {int(dB * 100)}% of B\'s bulbs are defective.',
                             f'Supplier A provides {Fr_(sA)} of a shop\'s bulbs, with defect rate {int(dA * 100)}%; supplier B provides the rest, with defect rate {int(dB * 100)}%.'], parts, 4)


# =============================================================================================
# ch12 Probability distributions (SL 4.7–4.9, 4.12; AHL 4.14)
# =============================================================================================
def ncdf(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def ninv(p):
    lo, hi = -10.0, 10.0
    for _ in range(200):
        m_ = (lo + hi) / 2
        if ncdf(m_) < p:
            lo = m_
        else:
            hi = m_
    return (lo + hi) / 2


def bpmf(n, p, k):
    return math.comb(n, k) * p ** k * (1 - p) ** (n - k)


def bcdf(n, p, k):
    return sum(bpmf(n, p, j) for j in range(0, k + 1))


R.facts('ch12-st1', F(
    terms=[('discrete random variable', 'a variable X taking countable values x with probabilities P(X = x) that sum to 1'),
           ('expected value', 'the long-run mean E(X) = Σ x P(X = x)'),
           ('fair game', 'a game in which the expected gain of each player is zero')],
    facts=[('For a probability distribution, Σ P(X = x) =', '1', ['0', 'E(X)', 'n'], 'Total probability.'),
           ('X takes values 0, 1, 2 with probabilities 0.2, 0.5, 0.3. E(X) =', '1.1', ['1', '1.5', '0.8'], '0 + 0.5 + 0.6.'),
           ('A game is fair if', 'the expected gain is 0', ['each outcome is equally likely', 'the expected gain is 1', 'nobody can lose'], 'Definition.')],
    why=[('Explain why E(X) need not be a value that X can take.', 'E(X) is a weighted average of the values, e.g. the expected score on a die is 3.5.'),
         ('Explain why the probabilities in a distribution must sum to 1.', 'The values of X cover all possible outcomes, which are mutually exclusive and exhaustive.'),
         ('Explain how to decide whether a game with a fee is worth playing in the long run.', 'Find the expected winnings minus the fee; if it is negative the player loses on average.')],
    misc=[('E(X) is the most likely value of X.', 'That is the mode; E(X) is the long-run mean.'),
          ('If P(X = x) = kx for x = 1, 2, 3 then k = 1/3.', 'k(1 + 2 + 3) = 1 gives k = 1/6.')],
))


@R.add('ch12-st1', 'C1', (1, 3), 'mcq')
def drv_mcq(rng, slot):
    ps = rng.choice([[0.1, 0.3, 0.4, 0.2], [0.25, 0.25, 0.3, 0.2], [0.15, 0.35, 0.3, 0.2], [0.4, 0.3, 0.2, 0.1]])
    e = sum(i * p for i, p in enumerate(ps))
    return mcq(rng, f'X takes values 0, 1, 2, 3 with probabilities {", ".join(str(p) for p in ps)}. E(X) =', f'{e:.3g}', [f'{e + 0.3:.3g}', '1.5', f'{sum(ps[1:]):.3g}'], 'Σ x P(X = x).')


@R.add('ch12-st1', 'C3', (2, 5), 'short', style='p1')
def drv_k(rng, slot):
    kind = rng.choice(['kx', 'table', 'game'])
    if kind == 'kx':
        vals = rng.choice([[1, 2, 3, 4], [1, 2, 3], [2, 3, 4, 5], [0, 1, 2, 3]])
        form = rng.choice(['kx', 'kx²', 'k(x + 1)'])
        w = [v if form == 'kx' else v * v if form == 'kx²' else v + 1 for v in vals]
        k = sp.Rational(1, sum(w))
        e = sum(v * wi * k for v, wi in zip(vals, w))
        return mk(f'A discrete random variable X has P(X = x) = {form} for x = {", ".join(map(str, vals))}. Find k and E(X).', f'k = {Fr_(k)}; E(X) = {Fr_(e)}',
                  f'k × {sum(w)} = 1 (M1); k = {Fr_(k)} (A1); Σ xP(X = x) (M1); E(X) = {Fr_(e)} (A1).', 4)
    if kind == 'table':
        vals = sorted(rng.sample(range(-2, 8), 4))
        ps = [sp.Rational(rng.randint(1, 4), 10) for _ in range(3)]
        rest = 1 - sum(ps)
        if rest <= 0:
            return None
        e = sum(v * p for v, p in zip(vals, ps + [rest]))
        return mk(f'X takes the values {", ".join(map(str, vals))} with probabilities {", ".join(Fr_(p) for p in ps)} and p respectively. Find p and E(X).', f'p = {Fr_(rest)}; E(X) = {Fr_(e)}',
                  f'sum to 1 (M1); p = {Fr_(rest)} (A1); E(X) (M1 A1).', 4)
    fee = rng.randint(2, 5)
    prizes = [0, rng.randint(2, 6), rng.randint(8, 20)]
    ps = [sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(1, 6)]
    eg = sum(a * p for a, p in zip(prizes, ps)) - fee
    return mk(f'A game costs ${fee} to play. A player wins $0 with probability 1/2, ${prizes[1]} with probability 1/3 and ${prizes[2]} with probability 1/6. Find the expected gain per game and state whether the game is fair.', f'{Fr_(eg)} dollars; ' + ('fair' if eg == 0 else 'not fair'),
              f'expected winnings {Fr_(eg + fee)} (M1 A1); subtract fee (M1); {Fr_(eg)} (A1).', 4)


@R.add('ch12-st1', 'C3', (2, 4), 'short', style='p2')
def drv_gdc(rng, slot):
    vals = sorted(rng.sample(range(1, 20), 4))
    ps = [round(rng.uniform(0.05, 0.35), 2) for _ in range(3)]
    rest = round(1 - sum(ps), 2)
    if rest <= 0:
        return None
    e = sum(v * p for v, p in zip(vals, ps + [rest]))
    n = rng.choice([50, 100, 250])
    return mk(f'A discrete random variable X takes the values {", ".join(map(str, vals))} with probabilities {", ".join(str(p) for p in ps)} and {rest}. Find E(X) and the expected total of {n} independent observations of X.', f'{s3(e)}; {s3(n * e)}',
              f'Σ xP(X = x) (M1); {s3(e)} (A1); {n} × E(X) (A1).', 3)


@R.add('ch12-st1', 'C2', (2, 4), 'explain')
def drv_explain(rng, slot):
    vals = [1, 2, 3]
    ps = rng.choice([(0.3, 0.4, 0.4), (0.5, 0.3, 0.3), (0.2, 0.2, 0.5)])
    return mk(f'Explain why the table X = 1, 2, 3 with P(X = x) = {ps[0]}, {ps[1]}, {ps[2]} cannot be a probability distribution.', f'probabilities sum to {sum(ps):.2g}',
              f'Σ P(X = x) = {sum(ps):.2g} (A1); a probability distribution must sum to 1 (R1); so the table is invalid (R1).', 3, 'explain')


@R.add('ch12-st1', 'C4', (3, 5), 'multi_step', style='ext')
def drv_parts(rng, slot):
    r, b = rng.randint(3, 6), rng.randint(2, 5)
    n = r + b
    # X = number of red in two draws without replacement
    p0 = sp.Rational(b * (b - 1), n * (n - 1))
    p2 = sp.Rational(r * (r - 1), n * (n - 1))
    p1 = 1 - p0 - p2
    e = p1 + 2 * p2
    prize = rng.choice([3, 4, 5])
    parts = [('Find the probability distribution of X.', f'P(X = 0) = {Fr_(p0)}, P(X = 1) = {Fr_(p1)}, P(X = 2) = {Fr_(p2)}', 'M1 A1 A1 A1', 4, True),
             ('Find E(X).', Fr_(e), 'M1 A1', 2, True),
             (f'A player pays $2 and receives ${prize} for each red counter drawn. Find the expected gain.', Fr_(prize * e - 2), 'M1 A1', 2, True),
             ('Find the fee that would make the game fair.', f'${Fr_(prize * e)}', 'A1', 1, True),
             ('Find P(X = 2 | X ≥ 1).', Fr_(p2 / (p1 + p2)), 'M1 A1', 2, False)]
    return build_parts(rng, [f'A bag contains {r} red and {b} blue counters. Two are drawn without replacement and X is the number of red counters drawn.', f'X is the number of red counters when two counters are drawn without replacement from a bag of {r} red and {b} blue counters.'], parts, 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch12-st2', F(
    terms=[('binomial distribution', 'the distribution X ~ B(n, p) of the number of successes in n independent trials, each with success probability p'),
           ('binomial conditions', 'a fixed number of trials, two outcomes per trial, independence, and a constant probability of success'),
           ('binomial mean and variance', 'the values E(X) = np and Var(X) = np(1 − p)')],
    facts=[('If X ~ B(10, 0.3), E(X) =', '3', ['0.3', '7', '2.1'], 'np.'),
           ('If X ~ B(20, 0.5), Var(X) =', '5', ['10', '2.5', '√5'], 'np(1 − p).'),
           ('P(X = k) for X ~ B(n, p) is', 'ⁿCₖ pᵏ(1 − p)ⁿ⁻ᵏ', ['pᵏ(1 − p)ⁿ⁻ᵏ', 'ⁿCₖ pⁿ', 'np'], 'Count arrangements.'),
           ('Drawing 3 cards without replacement from a small pack is not binomial because', 'the trials are not independent', ['there are 3 trials', 'p is a fraction', 'there are two outcomes'], 'Probabilities change.')],
    why=[('Explain why the binomial coefficient appears in P(X = k).', 'Each particular sequence with k successes has probability pᵏ(1 − p)ⁿ⁻ᵏ, and there are ⁿCₖ such sequences.'),
         ('Explain why P(X ≥ 1) is best found as 1 − P(X = 0).', 'The complement is a single term, (1 − p)ⁿ, which is quicker than adding n terms.'),
         ('Explain why the number of sixes in 10 rolls of a fair die is binomial.', 'There are 10 independent trials, each giving six or not six, with constant probability 1/6.')],
    misc=[('If X ~ B(8, 0.25), then P(X ≤ 2) = P(X = 2).', 'P(X ≤ 2) = P(0) + P(1) + P(2).'),
          ('P(X < 3) = P(X ≤ 3) for a binomial variable.', 'X is discrete: P(X < 3) = P(X ≤ 2).')],
))


@R.add('ch12-st2', 'C1', (1, 3), 'mcq')
def binom_mcq(rng, slot):
    n, p = rng.choice([(10, 0.4), (20, 0.25), (15, 0.2), (12, 0.5), (25, 0.6)])
    if rng.random() < 0.5:
        return mcq(rng, f'X ~ B({n}, {p}). E(X) =', f'{n * p:g}', [f'{n * p * (1 - p):g}', f'{p:g}', f'{n * (1 - p):g}'], 'np.')
    return mcq(rng, f'X ~ B({n}, {p}). Var(X) =', f'{n * p * (1 - p):g}', [f'{n * p:g}', f'{math.sqrt(n * p * (1 - p)):.3g}', f'{p * (1 - p):g}'], 'np(1 − p).')


@R.add('ch12-st2', 'C3', (2, 5), 'short', style='p2')
def binom_prob(rng, slot):
    n = rng.randint(6, 25)
    p = rng.choice([0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.6, 0.7])
    k = rng.randint(1, n - 2)
    kind = rng.choice(['eq', 'le', 'ge', 'lt', 'between'])
    ctx = rng.choice([f'A basketball player scores a free throw with probability {p}. She takes {n} throws.', f'The probability that a seed germinates is {p}. {n} seeds are planted.', f'Each component is faulty with probability {p}, independently. A box contains {n} components.'])
    if kind == 'eq':
        v, ph = bpmf(n, p, k), f'exactly {k}'
    elif kind == 'le':
        v, ph = bcdf(n, p, k), f'at most {k}'
    elif kind == 'ge':
        v, ph = 1 - bcdf(n, p, k - 1), f'at least {k}'
    elif kind == 'lt':
        v, ph = bcdf(n, p, k - 1), f'fewer than {k}'
    else:
        k2 = min(n, k + rng.randint(1, 3))
        v, ph = bcdf(n, p, k2) - bcdf(n, p, k - 1), f'between {k} and {k2} inclusive'
    what = 'successes' if 'scores' in ctx else 'germinate' if 'seed' in ctx else 'faulty'
    q = f'Find the probability that {ph} ' + ('are successful.' if what == 'successes' else 'germinate.' if what == 'germinate' else 'are faulty.')
    return mk(ctx + ' ' + q, s3(v), f'X ~ B({n}, {p}) (M1); correct region (M1); {s3(v)} (A1).', 3)


@R.add('ch12-st2', 'C3', (2, 5), 'short', style='p2')
def binom_inverse(rng, slot):
    p = rng.choice([0.05, 0.1, 0.2, 0.3, 1 / 6])
    target = rng.choice([0.9, 0.95, 0.99])
    kind = rng.choice(['n', 'mean'])
    pt_ = f'{p:g}' if p != 1 / 6 else '1/6'
    if kind == 'n':
        n = next(n for n in range(1, 500) if 1 - (1 - p) ** n >= target)
        return mk(f'The probability of success in a trial is {pt_}. Find the least number of independent trials needed for the probability of at least one success to exceed {target}.', str(n),
                  f'1 − (1 − {pt_})ⁿ > {target} (M1 A1); n > ln({1 - target:.2g})/ln({1 - p:.4g}) = {s3(math.log(1 - target) / math.log(1 - p))} (M1); n = {n} (A1).', 4)
    n = rng.randint(10, 40)
    m = n * p
    sd = math.sqrt(n * p * (1 - p))
    lo = m - sd
    hi = m + sd
    pr = sum(bpmf(n, p, k) for k in range(n + 1) if lo < k < hi)
    return mk(f'X ~ B({n}, {pt_}). Find E(X), the standard deviation of X, and P(E(X) − σ < X < E(X) + σ).', f'{s3(m)}; {s3(sd)}; {s3(pr)}',
              f'np = {s3(m)} (A1); σ = √(np(1 − p)) = {s3(sd)} (A1); integers strictly between {s3(lo)} and {s3(hi)} (M1); {s3(pr)} (A1).', 4)


@R.add('ch12-st2', 'C3', (2, 4), 'short', style='p1')
def binom_exact(rng, slot):
    n = rng.randint(3, 6)
    p = rng.choice([sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(1, 4), sp.Rational(2, 3), sp.Rational(1, 6)])
    k = rng.randint(1, n - 1)
    v = sp.binomial(n, k) * p ** k * (1 - p) ** (n - k)
    return mk(f'X ~ B({n}, {Fr_(p)}). Find P(X = {k}) exactly, and write down E(X).', f'{Fr_(v)}; {Fr_(n * p)}',
              f'{n}C{k} ({Fr_(p)}){sup(k)}({Fr_(1 - p)}){sup(n - k)} (M1); {Fr_(v)} (A1); E(X) = np = {Fr_(n * p)} (A1).', 3)


@R.add('ch12-st2', 'C2', (2, 4), 'explain')
def binom_explain(rng, slot):
    r, b = rng.randint(3, 8), rng.randint(3, 8)
    k = rng.randint(3, 5)
    return mk(f'{k} balls are drawn without replacement from a bag of {r} red and {b} blue balls, and X is the number of red balls. Explain why X does not follow a binomial distribution, and how the experiment could be changed so that it does.', 'trials not independent; draw with replacement',
              f'without replacement the probability of red changes after each draw (R1); trials are not independent (R1); replacing each ball keeps p = {r}/{r + b} constant, giving B({k}, {r}/{r + b}) (A1).', 3, 'explain')


@R.add('ch12-st2', 'C4', (3, 5), 'multi_step', style='ext')
def binom_parts(rng, slot):
    n, p = rng.randint(10, 20), rng.choice([0.15, 0.2, 0.25, 0.3, 0.35])
    k = round(n * p)
    m = 5
    q = 1 - bcdf(n, p, k)
    parts = [(f'State two assumptions needed to model the number of defective items with a binomial distribution.', 'independence; constant probability of defect', 'R1 R1', 2, True),
             (f'Find the probability that exactly {k} items in a box are defective.', s3(bpmf(n, p, k)), 'A1', 1, True),
             (f'Find the probability that more than {k} are defective.', s3(q), 'M1 A1', 2, True),
             ('Find the mean and variance of the number of defective items in a box.', f'{n * p:g}; {n * p * (1 - p):.4g}', 'A1 A1', 2, True),
             (f'An inspector checks {m} boxes. Find the probability that exactly 2 of them contain more than {k} defective items.', s3(math.comb(m, 2) * q ** 2 * (1 - q) ** (m - 2)), 'new binomial B(5, P) (M1) A1', 2, True),
             ('Find the most likely number of defective items in a box.', str(max(range(n + 1), key=lambda j: bpmf(n, p, j))), 'A1', 1, False)]
    return build_parts(rng, [f'Items are packed in boxes of {n}. Each item is defective with probability {p}, independently.', f'A factory packs {n} items per box; the probability that an item is defective is {p}.'], parts, 4)


@R.add('ch12-st2', 'C4', (4, 5), 'multi_step', style='p3')
def binom_p3(rng, slot):
    n = rng.choice([4, 5, 6])
    parts = [(f'For X ~ B({n}, p), write down P(X = 0) and P(X = 1) in terms of p.', f'(1 − p){sup(n)}; {n}p(1 − p){sup(n - 1)}', 'A1 A1', 2, True),
             (f'Find the value of p for which P(X = 0) = P(X = 1).', f'p = 1/{n + 1}', 'M1 A1', 2, True),
             ('Show that P(X = k + 1)/P(X = k) = ((n − k)/(k + 1)) × p/(1 − p).', 'proof', 'M1 A1 AG', 3, True),
             ('Hence show that P(X = k) increases while k < (n + 1)p − 1 and deduce the mode.', 'mode is the integer part of (n + 1)p (when not an integer)', 'R1 A1 A1', 3, True),
             (f'Prove that E(X) = np for X ~ B(n, p) using kⁿCₖ = nⁿ⁻¹Cₖ₋₁.', 'proof', 'M1 A1 A1', 3, True),
             ('Find the values of p for which the mode of B(10, p) is 3.', '3/11 < p < 4/11 (boundaries giving two modes)', 'M1 A1', 2, False)]
    return build_parts(rng, ['This question investigates the shape of the binomial distribution.', 'In this question X ~ B(n, p) with 0 < p < 1.'], parts, 5)


# ---------------------------------------------------------------------------------------------
R.facts('ch12-st3', F(
    terms=[('normal distribution', 'the continuous, symmetric, bell-shaped distribution X ~ N(μ, σ²)'),
           ('standardised value (z-score)', 'the value z = (x − μ)/σ, the number of standard deviations x is from the mean'),
           ('inverse normal calculation', 'finding the value x for which P(X < x) equals a given probability')],
    facts=[('For a normal distribution about 68% of values lie within', 'one standard deviation of the mean', ['two standard deviations', 'the interquartile range', '0.68 of the mean'], 'Empirical rule.'),
           ('If X ~ N(50, 4²), the z-score of 58 is', '2', ['8', '0.5', '−2'], '(58 − 50)/4.'),
           ('For any normal distribution, P(X < μ) =', '0.5', ['0', '0.68', '1'], 'Symmetry.'),
           ('About 95% of a normal distribution lies within', 'two standard deviations of the mean', ['one standard deviation', 'three standard deviations', 'the quartiles'], 'Empirical rule.')],
    why=[('Explain why P(X = a) = 0 for a normal random variable.', 'X is continuous; probability is area under the curve, and the area above a single point is zero.'),
         ('Explain why z-scores allow comparison between different normal distributions.', 'Standardising measures each value in standard deviations from its own mean, putting both on the common scale N(0, 1).'),
         ('Explain how symmetry gives P(X > μ + a) = P(X < μ − a).', 'The normal curve is symmetric about μ, so tail areas the same distance either side of the mean are equal.')],
    misc=[('If X ~ N(20, 9), then σ = 9.', 'N(μ, σ²) gives the variance: σ = 3.'),
          ('P(X ≤ 5) and P(X < 5) differ for a normal variable.', 'For a continuous variable they are equal since P(X = 5) = 0.')],
))


@R.add('ch12-st3', 'C1', (1, 3), 'mcq')
def normal_mcq(rng, slot):
    mu, sd = rng.randint(20, 80), rng.randint(2, 10)
    k = rng.choice([-2, -1, 1, 2, 3])
    xv = mu + k * sd
    return mcq(rng, f'X ~ N({mu}, {sd * sd}). The z-score of x = {xv} is', str(k), [str(-k), str(k * sd), P(sp.Rational(k, sd))], '(x − μ)/σ.')


@R.add('ch12-st3', 'C3', (2, 5), 'short', style='p2')
def normal_prob(rng, slot):
    ctx = rng.choice([('The masses of apples', 'g', 150, 12), ('The heights of students', 'cm', 165, 8), ('The times to complete a puzzle', 'minutes', 24, 4.5), ('The lifetimes of batteries', 'hours', 520, 35)])
    nm_, u, mu, sd = ctx
    a = round(mu + rng.uniform(-1.8, 1.8) * sd, 1 if sd < 10 else 0)
    b = round(mu + rng.uniform(0.2, 2.2) * sd, 1 if sd < 10 else 0)
    if b <= a:
        a, b = b - sd, a + sd
    kind = rng.choice(['lt', 'gt', 'between'])
    if kind == 'lt':
        v, ph = ncdf((a - mu) / sd), f'less than {a:g} {u}'
    elif kind == 'gt':
        v, ph = 1 - ncdf((a - mu) / sd), f'more than {a:g} {u}'
    else:
        v, ph = ncdf((b - mu) / sd) - ncdf((a - mu) / sd), f'between {a:g} and {b:g} {u}'
    n = rng.choice([200, 500, 1000])
    return mk(f'{nm_} are normally distributed with mean {mu} {u} and standard deviation {sd:g} {u}. Find the probability that a randomly chosen value is {ph}, and the expected number of such values in a sample of {n}.', f'{s3(v)}; {s3(n * v)}',
              f'X ~ N({mu}, {sd:g}²) (M1); GDC normal cdf (M1); {s3(v)} (A1); × {n} (A1).', 4)


@R.add('ch12-st3', 'C3', (2, 5), 'short', style='p2')
def normal_inverse(rng, slot):
    kind = rng.choice(['x', 'sigma', 'mu'])
    mu, sd = rng.randint(40, 90), rng.choice([3, 5, 6, 8, 12])
    p = rng.choice([0.05, 0.1, 0.2, 0.25, 0.8, 0.9, 0.95])
    z = ninv(p)
    if kind == 'x':
        top = rng.random() < 0.5
        xv = mu + ninv(1 - p if top else p) * sd
        return mk(f'X ~ N({mu}, {sd * sd}). Find the value of k such that P(X {">" if top else "<"} k) = {p}.', f'k = {s3(xv)}', f'inverse normal with area {1 - p if top else p:g} to the left (M1 A1); k = {s3(xv)} (A1).', 3)
    xv = round(mu + z * sd, 1)
    if kind == 'sigma':
        s_ = (xv - mu) / z
        return mk(f'X ~ N({mu}, σ²) and P(X < {xv:g}) = {p}. Find σ.', f'σ = {s3(s_)}', f'standardise: ({xv:g} − {mu})/σ = {s3(z)} (M1 A1); σ = {s3(s_)} (A1).', 3)
    m_ = xv - z * sd
    return mk(f'X ~ N(μ, {sd * sd}) and P(X < {xv:g}) = {p}. Find μ.', f'μ = {s3(m_)}', f'({xv:g} − μ)/{sd} = {s3(z)} (M1 A1); μ = {s3(m_)} (A1).', 3)


@R.add('ch12-st3', 'C3', (2, 4), 'short', style='p1')
def normal_symmetry(rng, slot):
    mu, sd = rng.randint(20, 80), rng.randint(2, 9)
    p = rng.choice([0.1, 0.15, 0.2, 0.3, 0.35, 0.4])
    k = rng.randint(1, 3) * sd
    return mk(f'X ~ N({mu}, {sd * sd}) and P(X < {mu - k}) = {p}. Without a calculator, find P(X > {mu + k}) and P({mu - k} < X < {mu + k}).', f'{p}; {1 - 2 * p:.2g}',
              f'symmetry about μ = {mu} (R1); P(X > {mu + k}) = {p} (A1); 1 − 2 × {p} = {1 - 2 * p:.2g} (A1).', 3)


@R.add('ch12-st3', 'C2', (2, 4), 'explain')
def normal_explain(rng, slot):
    m1, s1, m2, s2 = rng.randint(50, 70), rng.randint(5, 12), rng.randint(50, 70), rng.randint(5, 12)
    x1, x2 = m1 + rng.randint(5, 20), m2 + rng.randint(5, 20)
    z1, z2 = (x1 - m1) / s1, (x2 - m2) / s2
    if abs(z1 - z2) < 0.05:
        return None
    return mk(f'{who(rng)} scored {x1} in History (mean {m1}, s.d. {s1}) and {x2} in Biology (mean {m2}, s.d. {s2}). Both are normally distributed. Explain, using z-scores, in which subject the performance was relatively better.', 'History' if z1 > z2 else 'Biology',
              f'z = {s3(z1)} for History (A1); z = {s3(z2)} for Biology (A1); larger z is better relative to the cohort (R1).', 3, 'explain')


@R.add('ch12-st3', 'C4', (3, 5), 'multi_step', style='ext')
def normal_parts(rng, slot):
    mu, sd = rng.choice([(500, 8), (250, 5), (1000, 12), (330, 4)])
    lim = mu - rng.randint(1, 2) * sd + rng.randint(-2, 2)
    pl = ncdf((lim - mu) / sd)
    top = mu + ninv(0.95) * sd
    n = rng.choice([10, 12, 20])
    parts = [(f'Find the probability that a packet weighs less than {lim} g.', s3(pl), 'M1 A1', 2, True),
             ('Find the weight exceeded by 5% of packets.', f'{s3(top)} g', 'inverse normal (M1) A1', 2, True),
             (f'The machine is adjusted so that only 1% of packets weigh less than {lim} g, with the same standard deviation. Find the new mean.', f'{s3(lim - ninv(0.01) * sd)} g', 'z = −2.326 (M1) A1 A1', 3, True),
             (f'With the original settings, {n} packets are chosen at random. Find the probability that at least one weighs less than {lim} g.', s3(1 - (1 - pl) ** n), 'binomial complement (M1) A1', 2, True),
             (f'Find P(X < {lim} | X < {mu}).', s3(pl / 0.5), 'conditional (M1) A1', 2, False)]
    return build_parts(rng, [f'The weights of packets of rice are normally distributed with mean {mu} g and standard deviation {sd} g.', f'A machine fills packets whose weights X ~ N({mu}, {sd * sd}) grams.'], parts, 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch12-st4', F(
    terms=[('variance of a discrete random variable', 'the quantity Var(X) = E(X²) − [E(X)]² = Σ x²P(X = x) − μ²'),
           ('probability density function', 'a function f(x) ≥ 0 with ∫ f(x) dx = 1 over its domain; P(a ≤ X ≤ b) = ∫ₐᵇ f(x) dx'),
           ('linear transformation of a random variable', 'the rules E(aX + b) = aE(X) + b and Var(aX + b) = a²Var(X)'),
           ('median of a continuous random variable', 'the value m with ∫ f(x) dx from the lower limit to m equal to 1/2')],
    facts=[('Var(3X + 2) =', '9Var(X)', ['3Var(X) + 2', '9Var(X) + 2', '3Var(X)'], 'a² Var(X).'),
           ('For a pdf f on [0, 2], ∫₀² f(x) dx =', '1', ['0', '2', 'E(X)'], 'Total probability.'),
           ('E(X) for a continuous random variable with pdf f is', '∫ x f(x) dx', ['∫ f(x) dx', 'f(E(X))', '∫ x² f(x) dx'], 'Weighted average.'),
           ('If E(X) = 4 and E(X²) = 20, Var(X) =', '4', ['16', '20', '2'], '20 − 16.')],
    why=[('Explain why adding a constant to a random variable does not change its variance.', 'Every value and the mean shift by the same amount, so deviations from the mean are unchanged.'),
         ('Explain why a probability density function cannot take negative values.', 'Probabilities are areas under f; a negative f on an interval would give a negative probability.'),
         ('Explain why f(x) itself is not a probability for a continuous random variable.', 'Probabilities come from areas; f(x) is a density and can exceed 1, while P(X = x) = 0.')],
    misc=[('Var(2X − 3) = 2Var(X) − 3.', 'Var(2X − 3) = 4Var(X): constants do not affect spread and the multiplier is squared.'),
          ('If f(x) = kx on [0, 2] then k = 1/2 because f(2) must be 1.', '∫₀² kx dx = 2k = 1, so k = 1/2 here, but the reason is total area 1, not f(2) = 1.')],
))


@R.add('ch12-st4', 'C1', (1, 3), 'mcq')
def var_mcq(rng, slot):
    a, b, v = rng.randint(2, 5), nz(rng, -6, 6), rng.randint(2, 9)
    return mcq(rng, f'Var(X) = {v}. Var({a}X {"+" if b > 0 else "−"} {abs(b)}) =', str(a * a * v), [str(a * v), str(a * a * v + b), str(a * v + b)], 'a² Var(X).')


@R.add('ch12-st4', 'C3', (2, 5), 'short', style='p1')
def pdf_exact(rng, slot):
    kind = rng.choice(['lin', 'quad', 'const'])
    if kind == 'lin':
        b = rng.choice([1, 2, 3, 4])
        k = sp.Rational(2, b * b)
        f = k * x
    elif kind == 'quad':
        b = rng.choice([1, 2, 3])
        k = sp.Rational(3, b ** 3)
        f = k * x ** 2
    else:
        b = rng.choice([2, 3, 4])
        k = sp.Rational(3, 2 * b ** 3) * 0 + sp.Rational(6, b ** 3)
        f = k * x * (b - x)
    E = sp.integrate(x * f, (x, 0, b))
    V = sp.integrate(x ** 2 * f, (x, 0, b)) - E ** 2
    ftxt = {'lin': 'kx', 'quad': 'kx²', 'const': f'kx({b} − x)'}[kind]
    a_ = sp.Rational(b, 2)
    pr = sp.integrate(f, (x, 0, a_))
    return mk(f'A continuous random variable X has probability density function f(x) = {ftxt} for 0 ≤ x ≤ {b}, and 0 otherwise. Find k, E(X), Var(X) and P(X < {P(a_)}).', f'k = {Fr_(k)}; E(X) = {Fr_(E)}; Var(X) = {Fr_(V)}; {Fr_(pr)}',
              f'∫ f = 1 (M1); k = {Fr_(k)} (A1); E(X) = ∫ x f(x) dx = {Fr_(E)} (M1 A1); Var(X) = E(X²) − E(X)² = {Fr_(V)} (A1); P = {Fr_(pr)} (A1).', 6)


@R.add('ch12-st4', 'C3', (2, 5), 'short', style='p1')
def drv_variance(rng, slot):
    vals = sorted(rng.sample(range(0, 7), 3))
    ps = rng.choice([[sp.Rational(1, 4), sp.Rational(1, 2), sp.Rational(1, 4)], [sp.Rational(1, 5), sp.Rational(3, 10), sp.Rational(1, 2)], [sp.Rational(1, 3), sp.Rational(1, 6), sp.Rational(1, 2)], [sp.Rational(1, 10), sp.Rational(3, 5), sp.Rational(3, 10)]])
    E = sum(v * p for v, p in zip(vals, ps))
    E2 = sum(v * v * p for v, p in zip(vals, ps))
    V = E2 - E ** 2
    a, b = rng.randint(2, 4), nz(rng, -5, 5)
    return mk(f'X takes the values {", ".join(map(str, vals))} with probabilities {", ".join(Fr_(p) for p in ps)}. Find E(X), Var(X) and Var({a}X {"+" if b > 0 else "−"} {abs(b)}).', f'{Fr_(E)}; {Fr_(V)}; {Fr_(a * a * V)}',
              f'E(X) = {Fr_(E)} (A1); E(X²) = {Fr_(E2)} (A1); Var(X) = {Fr_(V)} (M1 A1); × {a * a} (A1).', 5)


@R.add('ch12-st4', 'C3', (2, 4), 'short', style='p2')
def pdf_gdc(rng, slot):
    a = rng.choice([1, 2, 3])
    f = sp.Rational(1, 1) * sp.sin(x) / 2 if a == 1 else None
    kind = rng.choice(['sin', 'exp'])
    if kind == 'sin':
        f, lo, hi = sp.sin(x) / 2, 0, pi
        ft = '(1/2) sin x'
    else:
        lam = rng.choice([sp.Rational(1, 2), 1, 2])
        hi = rng.choice([2, 3, 4])
        c = 1 / sp.integrate(sp.exp(-lam * x), (x, 0, hi))
        f, lo = c * sp.exp(-lam * x), 0
        ft = f'k e^({P(-lam * x)})'
    E = float(sp.integrate(x * f, (x, lo, hi)))
    fl = sp.lambdify(x, sp.integrate(f, (x, lo, x)) - sp.Rational(1, 2), 'math')
    med = nsols(fl, float(lo), float(hi))[0]
    if kind == 'sin':
        return mk(f'X has pdf f(x) = {ft} for 0 ≤ x ≤ π. Find E(X) and the median of X, to 3 significant figures.', f'{s3(E)}; {s3(med)}', f'∫ x f(x) dx (M1); {s3(E)} (A1); solve ∫₀ᵐ f = 0.5 (M1); {s3(med)} (A1).', 4)
    return mk(f'X has pdf f(x) = {ft} for 0 ≤ x ≤ {hi}, and 0 otherwise. Find k, E(X) and the median of X, to 3 significant figures.', f'{s3(float(c))}; {s3(E)}; {s3(med)}',
              f'∫ f = 1 (M1); k = {s3(float(c))} (A1); E(X) (M1 A1); median (A1).', 5)


@R.add('ch12-st4', 'C2', (2, 4), 'explain')
def var_explain(rng, slot):
    a, b, v = rng.randint(2, 5), rng.randint(1, 9), rng.randint(2, 9)
    return mk(f'{who(rng)} says that if Var(X) = {v} then Var({a}X − {b}) = {a * v - b}. Explain the error and give the correct value.', str(a * a * v),
              f'subtracting {b} shifts all values and does not change spread (R1); multiplying by {a} multiplies deviations by {a}, so the variance by {a * a} (R1); {a * a * v} (A1).', 3, 'explain')


@R.add('ch12-st4', 'C4', (3, 5), 'multi_step', style='ext')
def pdf_parts(rng, slot):
    b = rng.choice([2, 3, 4])
    k = sp.Rational(6, b ** 3)
    f = k * x * (b - x)
    E = sp.integrate(x * f, (x, 0, b))
    V = sp.integrate(x ** 2 * f, (x, 0, b)) - E ** 2
    q = sp.Rational(b, 4)
    pq = sp.integrate(f, (x, 0, q))
    parts = [(f'Show that k = {Fr_(k)}.', 'shown', 'integrate (M1) A1 AG', 2, True),
             ('Sketch the graph of f and use symmetry to write down E(X) and the median.', f'{Fr_(E)}; {Fr_(E)}', 'A1 R1', 2, True),
             ('Find Var(X).', Fr_(V), 'E(X²) (M1) A1 A1', 3, True),
             (f'Find P(X < {P(q)}).', Fr_(pq), 'M1 A1', 2, True),
             (f'Find P(X < {P(q)} | X < {Fr_(E)}).', Fr_(pq / sp.Rational(1, 2)), 'M1 A1', 2, False),
             ('Write down the mode of X.', Fr_(E), 'A1', 1, False)]
    return build_parts(rng, [f'A continuous random variable X has pdf f(x) = kx({b} − x) for 0 ≤ x ≤ {b}, and f(x) = 0 otherwise.', f'The pdf of X is f(x) = kx({b} − x), 0 ≤ x ≤ {b}.'], parts, 4)


@R.add('ch12-st4', 'C4', (3, 5), 'multi_step', style='ext')
def pdf_parts2(rng, slot):
    kind = rng.choice(['lin', 'quad'])
    b = rng.choice([1, 2, 3, 4, 5])
    if kind == 'lin':
        k = sp.Rational(2, b * b)
        f, ft = k * x, 'kx'
    else:
        k = sp.Rational(3, b ** 3)
        f, ft = k * x ** 2, 'kx²'
    E = sp.integrate(x * f, (x, 0, b))
    V = sp.integrate(x ** 2 * f, (x, 0, b)) - E ** 2
    m = [v for v in sp.solve(sp.integrate(f, (x, 0, x)) - sp.Rational(1, 2), x) if v.is_real and v > 0][0]
    a, c = rng.randint(2, 5), nz(rng, -5, 5)
    parts = [(f'Find the value of k.', Fr_(k), 'M1 A1', 2, True),
             ('Find E(X) and Var(X).', f'{Fr_(E)}; {Fr_(V)}', 'M1 A1 A1', 3, True),
             ('Find the exact median of X.', nice(m), 'M1 A1', 2, True),
             (f'Let Y = {a}X {"+" if c > 0 else "−"} {abs(c)}. Find E(Y) and Var(Y).', f'{Fr_(a * E + c)}; {Fr_(a * a * V)}', 'A1 A1', 2, True),
             ('Explain whether the mean is greater or less than the median.', 'less: the distribution is negatively skewed' if E < m else 'greater', 'R1', 1, False)]
    return build_parts(rng, [f'A continuous random variable X has pdf f(x) = {ft} for 0 ≤ x ≤ {b}, and 0 otherwise.', f'The random variable X has probability density function f(x) = {ft}, 0 ≤ x ≤ {b}.'], parts, 4)


@R.add('ch12-st4', 'C4', (3, 5), 'multi_step', style='ext')
def drv_var_parts(rng, slot):
    n = rng.choice([4, 5, 6])
    ps = [sp.Rational(1, n)] * n
    vals = list(range(1, n + 1))
    E = sp.Rational(n + 1, 2)
    V = sp.Rational(n * n - 1, 12)
    a, c = rng.randint(2, 6), rng.randint(1, 10)
    parts = [(f'Write down the probability distribution of X, the score on one roll.', f'P(X = x) = 1/{n} for x = 1, …, {n}', 'A1', 1, True),
             ('Find E(X) and E(X²).', f'{Fr_(E)}; {Fr_(sp.Rational(sum(v * v for v in vals), n))}', 'A1 A1', 2, True),
             ('Hence find Var(X).', Fr_(V), 'M1 A1', 2, True),
             (f'A player wins ${a} times the score minus ${c}. Find the expected winnings and their variance.', f'${Fr_(a * E - c)}; {Fr_(a * a * V)}', 'M1 A1 A1', 3, True),
             (f'Find the entry fee that makes the game fair.', f'${Fr_(a * E - c)}', 'A1', 1, False)]
    return build_parts(rng, [f'A fair {n}-sided die, numbered 1 to {n}, is rolled.', f'In a game a fair die with faces 1 to {n} is rolled once.'], parts, 4)


# =============================================================================================
# ch13 Geometry and trigonometry (SL 3.1–3.4)
# =============================================================================================
def dg(v):
    return s3(v) + '°'


def rad(d):
    return math.radians(d)


def brg(v):
    t_ = s3(v % 360)
    ip = t_.split('.')[0]
    return '0' * (3 - len(ip)) + t_ + '°'


R.facts('ch13-st1', F(
    terms=[('distance between points in 3D', 'the length d = √((x₂ − x₁)² + (y₂ − y₁)² + (z₂ − z₁)²)'),
           ('angle between a line and a plane', 'the angle between the line and its projection onto the plane'),
           ('right pyramid', 'a pyramid whose apex lies directly above the centre of its base'),
           ('surface area of a solid', 'the total area of all faces or curved surfaces of the solid')],
    facts=[('The volume of a cone with radius r and height h is', '(1/3)πr²h', ['πr²h', '(1/2)πr²h', '(4/3)πr³'], 'One third of the cylinder.'),
           ('The surface area of a sphere of radius r is', '4πr²', ['πr²', '(4/3)πr³', '2πr²'], 'Formula booklet.'),
           ('The midpoint of (2, 4, −6) and (8, 0, 2) is', '(5, 2, −2)', ['(6, −4, 8)', '(10, 4, −4)', '(3, 2, −4)'], 'Average the coordinates.'),
           ('The curved surface area of a cone with radius r and slant height l is', 'πrl', ['πr²l', '2πrl', 'πr(r + l)'], 'Formula booklet.')],
    why=[('Explain why the 3D distance formula follows from Pythagoras.', 'The horizontal distance is √(Δx² + Δy²); this and the vertical change Δz form a right triangle with the required distance as hypotenuse.'),
         ('Explain why a cone has one third the volume of the cylinder with the same base and height.', 'A pyramid or cone has volume (1/3) × base area × height; the cylinder has volume base area × height.'),
         ('Explain how to find the angle between a line and a plane.', 'Drop a perpendicular from a point of the line to the plane to form a right triangle; the angle at the plane between the line and its projection is found using trigonometry.')],
    misc=[('The volume of a sphere is 4πr².', 'That is its surface area; the volume is (4/3)πr³.'),
          ('The angle between a vertical edge of a cuboid and its base is 0°.', 'A vertical edge is perpendicular to the base: the angle is 90°.')],
))


@R.add('ch13-st1', 'C1', (1, 3), 'mcq')
def solid_mcq(rng, slot):
    A = [rng.randint(-5, 5) for _ in range(3)]
    d = rng.choice([(1, 2, 2), (2, 3, 6), (1, 4, 8), (2, 6, 9), (4, 4, 7)])
    B = [a + s_ * v for a, v, s_ in zip(A, d, [rng.choice([1, -1]) for _ in range(3)])]
    D = int(math.isqrt(sum(v * v for v in d)))
    return mcq(rng, f'The distance between A{tuple(A)} and B{tuple(B)} is', str(D), [str(sum(d)), str(D * D), str(D + 1)], '√(Δx² + Δy² + Δz²).')


@R.add('ch13-st1', 'C3', (2, 5), 'short', style='p2')
def solid_calc(rng, slot):
    kind = rng.choice(['cone', 'sphere', 'pyramid', 'cylhemi'])
    if kind == 'cone':
        r, h = rng.choice([3, 4, 5, 6, 7.5]), rng.choice([8, 10, 12, 9.6])
        l = math.hypot(r, h)
        return mk(f'A cone has base radius {r:g} cm and height {h:g} cm. Find its volume and its total surface area.', f'{s3(math.pi * r * r * h / 3)} cm³; {s3(math.pi * r * l + math.pi * r * r)} cm²',
                  f'V = (1/3)πr²h = {s3(math.pi * r * r * h / 3)} (A1); slant height l = {s3(l)} (M1); πrl + πr² = {s3(math.pi * r * l + math.pi * r * r)} (A1).', 3)
    if kind == 'sphere':
        V = rng.choice([500, 1000, 2500, 4000])
        r = (3 * V / (4 * math.pi)) ** (1 / 3)
        return mk(f'A sphere has volume {V} cm³. Find its radius and its surface area.', f'{s3(r)} cm; {s3(4 * math.pi * r * r)} cm²', f'(4/3)πr³ = {V} (M1); r = {s3(r)} (A1); 4πr² = {s3(4 * math.pi * r * r)} (A1).', 3)
    if kind == 'pyramid':
        a, h = rng.choice([6, 8, 10, 12]), rng.choice([7, 9, 12, 15])
        sl = math.hypot(a / 2, h)
        ang_ = math.degrees(math.atan(h / (a / math.sqrt(2))))
        return mk(f'A right pyramid has a square base of side {a} cm and height {h} cm. Find its volume, its total surface area, and the angle between a sloping edge and the base.', f'{g(a * a * h / 3)} cm³; {s3(a * a + 2 * a * sl)} cm²; {dg(ang_)}',
                  f'V = (1/3)a²h (A1); slant height of a face {s3(sl)} (M1); SA = {s3(a * a + 2 * a * sl)} (A1); tan θ = {h}/(half-diagonal {s3(a / math.sqrt(2))}) (M1); {dg(ang_)} (A1).', 5)
    r, h = rng.choice([2, 3, 4, 5]), rng.choice([6, 8, 10])
    V = math.pi * r * r * h + 2 / 3 * math.pi * r ** 3
    return mk(f'A solid consists of a cylinder of radius {r} m and height {h} m with a hemisphere of the same radius on top. Find its volume and its total surface area (including the base).', f'{s3(V)} m³; {s3(math.pi * r * r + 2 * math.pi * r * h + 2 * math.pi * r * r)} m²',
              f'πr²h + (2/3)πr³ (M1 A1); base + curved cylinder + hemisphere 2πr² (M1); {s3(math.pi * r * r + 2 * math.pi * r * h + 2 * math.pi * r * r)} (A1).', 4)


@R.add('ch13-st1', 'C3', (2, 4), 'short', style='p1')
def dist3d(rng, slot):
    A = [rng.randint(-6, 6) for _ in range(3)]
    B = [rng.randint(-6, 6) for _ in range(3)]
    if A == B:
        return None
    d2 = sum((a - b) ** 2 for a, b in zip(A, B))
    M = tuple(P(sp.Rational(a + b, 2)) for a, b in zip(A, B))
    return mk(f'Find the exact distance between A{tuple(A)} and B{tuple(B)}, and the coordinates of the midpoint of AB.', f'{P(sp.sqrt(d2))}; ({", ".join(M)})',
              f'√({" + ".join(str((a - b) ** 2) for a, b in zip(A, B))}) (M1); {P(sp.sqrt(d2))} (A1); midpoint (A1).', 3)


@R.add('ch13-st1', 'C2', (2, 4), 'explain')
def solid_explain(rng, slot):
    k = rng.choice([2, 3, 4])
    return mk(f'Explain what happens to the volume and the surface area of a sphere when its radius is multiplied by {k}.', f'volume × {k ** 3}; surface area × {k * k}',
              f'V = (4/3)πr³, so V scales by {k}³ = {k ** 3} (R1 A1); A = 4πr², so A scales by {k * k} (A1).', 3, 'explain')


@R.add('ch13-st1', 'C4', (3, 5), 'multi_step', style='ext')
def cuboid_parts(rng, slot):
    a, b, c = rng.choice([(3, 4, 12), (6, 8, 5), (4, 4, 7), (2, 6, 9), (5, 12, 8)])
    diag = math.sqrt(a * a + b * b + c * c)
    ang_ = math.degrees(math.atan(c / math.hypot(a, b)))
    parts = [(f'Find the length of the diagonal AG of the cuboid.', s3(diag) + ' cm', 'M1 A1', 2, True),
             ('Find the angle between AG and the base ABCD.', dg(ang_), 'identify angle (M1) A1', 2, True),
             ('Find the total surface area of the cuboid.', f'{2 * (a * b + b * c + a * c)} cm²', 'A1', 1, True),
             (f'With A at the origin and B, D, E on the positive x-, y- and z-axes, write down the coordinates of G and the midpoint M of EG.', f'G({a}, {b}, {c}); M({P(sp.Rational(a, 2))}, {P(sp.Rational(b, 2))}, {c})', 'A1 A1', 2, True),
             ('Find the angle between AM and the base.', dg(math.degrees(math.atan(c / math.hypot(a / 2, b / 2)))), 'M1 A1', 2, False)]
    return build_parts(rng, [f'A cuboid ABCDEFGH has AB = {a} cm, AD = {b} cm and AE = {c} cm, where E is vertically above A and G is opposite A.', f'ABCDEFGH is a cuboid with base ABCD, AB = {a} cm, AD = {b} cm and height AE = {c} cm.'], parts, 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch13-st2', F(
    terms=[('sine rule', 'the relation a/sin A = b/sin B = c/sin C in any triangle'),
           ('cosine rule', 'the relation a² = b² + c² − 2bc cos A in any triangle'),
           ('area of a triangle (trigonometric)', 'the formula Area = (1/2)ab sin C'),
           ('ambiguous case', 'the situation, given two sides and a non-included acute angle, in which two different triangles may fit the data')],
    facts=[('To find a side given two sides and the included angle, use', 'the cosine rule', ['the sine rule', 'SOHCAHTOA', 'the area formula'], 'SAS.'),
           ('The area of a triangle with sides 6 and 10 and included angle 30° is', '15', ['30', '60', '15√3'], '(1/2)(6)(10)(1/2).'),
           ('If sin B = 0.6, the possible values of B (0° < B < 180°) are', '36.9° and 143.1°', ['36.9° only', '53.1° and 126.9°', '36.9° and 323.1°'], 'sin(180° − B) = sin B.'),
           ('The cosine rule for angle C is', 'cos C = (a² + b² − c²)/(2ab)', ['cos C = (a² + b² + c²)/(2ab)', 'cos C = c/(a + b)', 'cos C = (c² − a² − b²)/(2ab)'], 'Rearrange.')],
    why=[('Explain why the sine rule can give two possible triangles.', 'sin θ = sin(180° − θ), so an angle found from its sine may be acute or obtuse; both are valid if the angle sum stays below 180°.'),
         ('Explain why the cosine rule reduces to Pythagoras when A = 90°.', 'cos 90° = 0, so the term −2bc cos A vanishes, leaving a² = b² + c².'),
         ('Explain why the cosine rule never gives an ambiguous angle.', 'cos θ is negative for obtuse and positive for acute angles in (0°, 180°), so each value of cos A gives exactly one angle.')],
    misc=[('In any triangle, a² = b² + c².', 'That is only for a right angle at A; in general a² = b² + c² − 2bc cos A.'),
          ('Area = (1/2) × a × b × sin A for sides a and b.', 'The angle must be the one included between the two sides: (1/2)ab sin C.')],
))


@R.add('ch13-st2', 'C1', (1, 3), 'mcq')
def trig_rule_mcq(rng, slot):
    a, b, C = rng.randint(4, 15), rng.randint(4, 15), rng.choice([30, 45, 60, 90, 150])
    area = sp.Rational(a * b, 2) * sp.sin(sp.pi * C / 180)
    return mcq(rng, f'A triangle has sides {a} cm and {b} cm with included angle {C}°. Its area is', P(sp.nsimplify(area)) + ' cm²', [P(a * b) + ' cm²', P(sp.nsimplify(area * 2)) + ' cm²', P(sp.Rational(a * b, 2)) + ' cm²' if C != 90 else P(a + b) + ' cm²'], '(1/2)ab sin C.')


@R.add('ch13-st2', 'C3', (2, 5), 'short', style='p2')
def triangle_solve(rng, slot):
    kind = rng.choice(['sas', 'sss', 'asa', 'amb'])
    if kind == 'sas':
        b, c, A = rng.randint(5, 20), rng.randint(5, 20), rng.randint(25, 140)
        a = math.sqrt(b * b + c * c - 2 * b * c * math.cos(rad(A)))
        return mk(f'In triangle ABC, AB = {c} cm, AC = {b} cm and angle BAC = {A}°. Find BC and the area of the triangle.', f'{s3(a)} cm; {s3(0.5 * b * c * math.sin(rad(A)))} cm²',
                  f'cosine rule (M1); BC = {s3(a)} (A1); (1/2)({b})({c}) sin {A}° (M1); {s3(0.5 * b * c * math.sin(rad(A)))} (A1).', 4)
    if kind == 'sss':
        a, b, c = sorted([rng.randint(4, 18) for _ in range(3)])
        if a + b <= c:
            return None
        C = math.degrees(math.acos((a * a + b * b - c * c) / (2 * a * b)))
        return mk(f'A triangle has sides {a} cm, {b} cm and {c} cm. Find its largest angle.', dg(C), f'largest angle is opposite the longest side (R1); cos C = ({a}² + {b}² − {c}²)/(2 × {a} × {b}) (M1); {dg(C)} (A1).', 3)
    if kind == 'asa':
        A, B = rng.randint(30, 80), rng.randint(30, 80)
        a = rng.randint(6, 20)
        b = a * math.sin(rad(B)) / math.sin(rad(A))
        return mk(f'In triangle ABC, angle A = {A}°, angle B = {B}° and BC = {a} cm. Find AC and AB.', f'AC = {s3(b)} cm; AB = {s3(a * math.sin(rad(180 - A - B)) / math.sin(rad(A)))} cm',
                  f'sine rule AC/sin {B}° = {a}/sin {A}° (M1); {s3(b)} (A1); C = {180 - A - B}° (A1); AB = {s3(a * math.sin(rad(180 - A - B)) / math.sin(rad(A)))} (A1).', 4)
    A = rng.randint(25, 50)
    a, b = rng.randint(6, 12), 0
    b = a / math.sin(rad(A)) * rng.uniform(0.55, 0.95)
    b = round(b, 1)
    sB = b * math.sin(rad(A)) / a
    if sB >= 1 or b <= a:
        return None
    B1 = math.degrees(math.asin(sB))
    B2 = 180 - B1
    return mk(f'In triangle ABC, angle A = {A}°, BC = {a} cm and AC = {b:g} cm. Find the two possible values of angle B.', f'{dg(B1)} or {dg(B2)}',
              f'sin B = {b:g} sin {A}°/{a} (M1); B = {dg(B1)} (A1); or 180° − {dg(B1)} = {dg(B2)}, valid since {A}° + {dg(B2)} < 180° (R1 A1).', 4)


@R.add('ch13-st2', 'C3', (2, 4), 'short', style='p1')
def triangle_exact(rng, slot):
    kind = rng.choice(['cos', 'area', 'sin'])
    if kind == 'cos':
        b, c = rng.randint(2, 8), rng.randint(2, 8)
        A = rng.choice([60, 120, 90])
        a2 = b * b + c * c - 2 * b * c * sp.cos(sp.pi * A / 180)
        return mk(f'Without a calculator, find the exact length of BC in triangle ABC where AB = {c}, AC = {b} and angle A = {A}°.', P(sp.sqrt(sp.nsimplify(a2))),
                  f'a² = {b}² + {c}² − 2({b})({c})cos {A}° (M1); cos {A}° = {P(sp.cos(sp.pi * A / 180))} (A1); a = {P(sp.sqrt(sp.nsimplify(a2)))} (A1).', 3)
    if kind == 'area':
        a, b, C = rng.randint(2, 10), rng.randint(2, 10), rng.choice([30, 45, 60, 120, 135, 150])
        ar = sp.nsimplify(sp.Rational(a * b, 2) * sp.sin(sp.pi * C / 180))
        return mk(f'Find the exact area of a triangle with sides {a} and {b} and included angle {C}°.', P(ar), f'(1/2)({a})({b}) sin {C}° (M1); sin {C}° = {P(sp.sin(sp.pi * C / 180))} (A1); {P(ar)} (A1).', 3)
    A, B = rng.choice([(30, 45), (45, 60), (30, 60), (45, 30), (60, 45)])
    a = rng.randint(2, 10)
    b = sp.nsimplify(a * sp.sin(sp.pi * B / 180) / sp.sin(sp.pi * A / 180))
    return mk(f'In triangle ABC, angle A = {A}°, angle B = {B}° and BC = {a}. Find the exact length of AC.', P(sp.radsimp(b)), f'sine rule (M1); AC = {a} sin {B}°/sin {A}° (A1); {P(sp.radsimp(b))} (A1).', 3)


@R.add('ch13-st2', 'C2', (2, 4), 'explain')
def trig_explain(rng, slot):
    A = rng.randint(25, 45)
    a = rng.randint(6, 12)
    b = round(a / math.sin(rad(A)) * 0.8, 1)
    if b <= a:
        return None
    return mk(f'In triangle ABC, angle A = {A}°, BC = {a} cm and AC = {b:g} cm. Explain why two different triangles satisfy this information.', 'ambiguous case: B acute or obtuse',
              f'sin B = {b:g} sin {A}°/{a} = {s3(b * math.sin(rad(A)) / a)} < 1 (M1); B or 180° − B both possible (R1); obtuse value plus {A}° is less than 180°, since BC < AC (R1).', 3, 'explain')


@R.add('ch13-st2', 'C4', (3, 5), 'multi_step', style='ext')
def triangle_parts(rng, slot):
    AB, BC, B = rng.randint(6, 15), rng.randint(6, 15), rng.randint(40, 130)
    AC = math.sqrt(AB * AB + BC * BC - 2 * AB * BC * math.cos(rad(B)))
    A = math.degrees(math.asin(BC * math.sin(rad(B)) / AC))
    area = 0.5 * AB * BC * math.sin(rad(B))
    h = 2 * area / AC
    parts = [('Find AC.', s3(AC) + ' m', 'cosine rule (M1) A1', 2, True),
             ('Find angle BAC.', dg(A), 'sine rule (M1) A1', 2, True),
             ('Find the area of triangle ABC.', s3(area) + ' m²', 'M1 A1', 2, True),
             ('Find the shortest distance from B to the line AC.', s3(h) + ' m', 'area = (1/2) × AC × h (M1) A1', 2, True),
             (f'The field is to be fenced. Find the total length of fencing needed.', s3(AB + BC + AC) + ' m', 'A1', 1, False)]
    return build_parts(rng, [f'A triangular field ABC has AB = {AB} m, BC = {BC} m and angle ABC = {B}°.', f'In a triangular plot ABC, AB = {AB} m, BC = {BC} m and the angle at B is {B}°.'], parts, 4)


@R.add('ch13-st2', 'C4', (4, 5), 'multi_step', style='p3')
def triangle_p3(rng, slot):
    a = rng.randint(5, 10)
    A = rng.choice([30, 35, 40])
    parts = [(f'In triangle ABC, angle A = {A}° and BC = a. AC = {a + 4} cm. Find the range of values of a for which two triangles exist.', f'{s3((a + 4) * math.sin(rad(A)))} < a < {a + 4}', 'height AC sin A (M1); conditions (A1 A1)', 3, True),
             (f'For a = {s3((a + 4) * math.sin(rad(A)) + 0.5)}, find both possible values of AB.', None, 'cosine rule quadratic in AB (M1 A1 A1)', 3, True),
             ('Show that the two values of AB found in (b) have sum 2 × AC × cos A.', 'sum of roots of the quadratic', 'R1 A1', 2, True),
             ('Generalise: show that the product of the two values equals AC² − a².', 'product of roots', 'R1 A1', 2, True),
             ('Prove the sine rule using the area formula.', '(1/2)bc sin A = (1/2)ac sin B ⇒ a/sin A = b/sin B', 'M1 A1', 2, False)]
    b = a + 4
    av = float(s3(b * math.sin(rad(A)) + 0.5))
    # AB = c: a² = b² + c² − 2bc cos A
    disc = (2 * b * math.cos(rad(A))) ** 2 - 4 * (b * b - av * av)
    c1 = (2 * b * math.cos(rad(A)) - math.sqrt(disc)) / 2
    c2 = (2 * b * math.cos(rad(A)) + math.sqrt(disc)) / 2
    parts[1] = (parts[1][0], f'{s3(c1)} cm or {s3(c2)} cm', parts[1][2], 3, True)
    return build_parts(rng, ['This question investigates the ambiguous case of the sine rule.', 'In this question all lengths are in centimetres.'], parts, 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch13-st3', F(
    terms=[('true bearing', 'a direction given as a three-figure angle measured clockwise from north'),
           ('angle of elevation', 'the angle above the horizontal from an observer to an object'),
           ('angle of depression', 'the angle below the horizontal from an observer to an object')],
    facts=[('The bearing of due west is', '270°', ['090°', '180°', '360°'], 'Clockwise from north.'),
           ('If the bearing of B from A is 070°, the bearing of A from B is', '250°', ['110°', '290°', '070°'], 'Add 180°.'),
           ('The angle of elevation of A from B equals', 'the angle of depression of B from A', ['90° minus the depression', 'twice the depression', 'the bearing'], 'Alternate angles.')],
    why=[('Explain why the back bearing differs from the bearing by 180°.', 'The two directions are opposite along the same line, and north lines at A and B are parallel, so the angles differ by 180°.'),
         ('Explain why an angle of depression equals the corresponding angle of elevation.', 'Both are measured from horizontal lines, which are parallel, so they are alternate angles.')],
    misc=[('A bearing of 45° is written 45°.', 'Bearings use three figures: 045°.'),
          ('Angles of elevation are measured from the vertical.', 'They are measured upwards from the horizontal.')],
))


@R.add('ch13-st3', 'C1', (1, 3), 'mcq')
def bearing_mcq(rng, slot):
    b = rng.randint(1, 35) * 10
    back = (b + 180) % 360
    return mcq(rng, f'The bearing of Q from P is {b:03d}°. The bearing of P from Q is', f'{back:03d}°', [f'{(360 - b) % 360:03d}°', f'{(b + 90) % 360:03d}°', f'{abs(180 - b):03d}°' if abs(180 - b) != back else f'{(b + 270) % 360:03d}°'], '± 180°.')


@R.add('ch13-st3', 'C3', (2, 5), 'short', style='p2')
def bearing_calc(rng, slot):
    d1, d2 = rng.randint(5, 30), rng.randint(5, 30)
    b1, b2 = rng.randint(1, 17) * 10, rng.randint(19, 34) * 10
    # positions
    x1, y1 = d1 * math.sin(rad(b1)), d1 * math.cos(rad(b1))
    x2, y2 = x1 + d2 * math.sin(rad(b2)), y1 + d2 * math.cos(rad(b2))
    dist = math.hypot(x2, y2)
    br = (math.degrees(math.atan2(-x2, -y2)) + 360) % 360
    return mk(f'A ship sails {d1} km on a bearing of {b1:03d}° from port P, then {d2} km on a bearing of {b2:03d}°. Find its distance from P and the bearing on which it must sail to return to P.', f'{s3(dist)} km; {brg(br)}',
              f'angle between the legs {abs(180 - abs(b2 - b1))}° (M1 A1); cosine rule {s3(dist)} (A1); bearing back {brg(br)} (M1 A1).', 5)


@R.add('ch13-st3', 'C3', (2, 5), 'short', style='p2')
def elevation(rng, slot):
    kind = rng.choice(['one', 'two', 'depr'])
    if kind == 'one':
        d, e = rng.randint(20, 120), rng.randint(15, 65)
        eye = rng.choice([1.5, 1.6, 1.8])
        return mk(f'From a point {d} m from the foot of a tower, the angle of elevation of the top is {e}°. The observer\'s eyes are {eye} m above the ground. Find the height of the tower.', f'{s3(d * math.tan(rad(e)) + eye)} m',
                  f'tan {e}° = h/{d} (M1); h = {s3(d * math.tan(rad(e)))} (A1); add {eye} (A1).', 3)
    if kind == 'two':
        e1, e2 = sorted(rng.sample(range(20, 70), 2))
        d = rng.randint(20, 80)
        h = d / (1 / math.tan(rad(e1)) - 1 / math.tan(rad(e2)))
        return mk(f'The angle of elevation of the top of a tree from A is {e1}°. From B, {d} m closer to the tree on the same level line, it is {e2}°. Find the height of the tree.', f'{s3(h)} m',
                  f'h/tan {e1}° − h/tan {e2}° = {d} (M1 A1); solve (M1); {s3(h)} (A1).', 4)
    h, e = rng.randint(30, 150), rng.randint(10, 50)
    return mk(f'From the top of a cliff {h} m high, the angle of depression of a boat is {e}°. Find the horizontal distance from the boat to the foot of the cliff, and the direct distance to the boat.', f'{s3(h / math.tan(rad(e)))} m; {s3(h / math.sin(rad(e)))} m',
              f'angle of elevation from the boat is {e}° (R1); {h}/tan {e}° (M1 A1); {h}/sin {e}° (A1).', 4)


@R.add('ch13-st3', 'C2', (2, 4), 'explain')
def bearing_explain(rng, slot):
    b = rng.randint(1, 17) * 10
    return mk(f'{who(rng)} says that if the bearing of B from A is {b:03d}°, then the bearing of A from B is {360 - b:03d}°. Explain the error and give the correct bearing.', f'{(b + 180) % 360:03d}°',
              f'the reverse direction is opposite, i.e. turned through 180° (R1); north lines are parallel so co-interior/alternate angles give ±180° (R1); {(b + 180) % 360:03d}° (A1).', 3, 'explain')


@R.add('ch13-st3', 'C4', (3, 5), 'multi_step', style='ext')
def bearing_parts(rng, slot):
    dAB, dBC = rng.randint(8, 25), rng.randint(8, 25)
    bAB, bBC = rng.randint(2, 8) * 10, rng.randint(11, 17) * 10
    xB, yB = dAB * math.sin(rad(bAB)), dAB * math.cos(rad(bAB))
    xC, yC = xB + dBC * math.sin(rad(bBC)), yB + dBC * math.cos(rad(bBC))
    AC = math.hypot(xC, yC)
    angB = 180 - (bBC - bAB)
    brAC = (math.degrees(math.atan2(xC, yC)) + 360) % 360
    area = 0.5 * dAB * dBC * math.sin(rad(angB))
    parts = [('Show that angle ABC = ' + f'{angB}°.', f'{angB}°', 'co-interior angles with north lines (M1 A1)', 2, True),
             ('Find the distance AC.', f'{s3(AC)} km', 'cosine rule (M1) A1', 2, True),
             ('Find the bearing of C from A.', brg(brAC), 'sine rule for angle BAC (M1); add to bearing (A1)', 2, True),
             ('Find the area of triangle ABC.', f'{s3(area)} km²', 'A1', 1, True),
             ('Find the bearing of A from C.', brg(brAC + 180), 'A1', 1, False)]
    return build_parts(rng, [f'A hiker walks {dAB} km from A to B on a bearing of {bAB:03d}°, then {dBC} km from B to C on a bearing of {bBC:03d}°.', f'B is {dAB} km from A on a bearing of {bAB:03d}°, and C is {dBC} km from B on a bearing of {bBC:03d}°.'], parts, 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch13-st4', F(
    terms=[('radian', 'the angle subtended at the centre of a circle by an arc equal in length to the radius; π radians = 180°'),
           ('arc length', 'the length l = rθ of part of the circumference, θ in radians'),
           ('area of a sector', 'the area A = (1/2)r²θ, θ in radians'),
           ('segment', 'the region between a chord and the arc it cuts off, area (1/2)r²(θ − sin θ)')],
    facts=[('120° in radians is', '2π/3', ['π/3', '3π/2', '2π'], '× π/180.'),
           ('π/5 radians in degrees is', '36°', ['72°', '18°', '5°'], '× 180/π.'),
           ('The arc length of a sector of radius 6 and angle 1.5 rad is', '9', ['4', '27', '13.5'], 'rθ.'),
           ('The area of a sector of radius 4 and angle π/4 is', '2π', ['π', '4π', 'π/2'], '(1/2)(16)(π/4).')],
    why=[('Explain why the arc length formula is l = rθ when θ is in radians.', 'The full circumference 2πr corresponds to 2π radians, so each radian gives arc length r.'),
         ('Explain why radians are preferred in calculus.', 'With radians, d(sin x)/dx = cos x exactly; in degrees an extra factor π/180 appears.'),
         ('Explain how to find the area of a segment.', 'Subtract the area of the triangle (1/2)r² sin θ from the sector area (1/2)r²θ.')],
    misc=[('A sector of radius 5 and angle 60° has arc length 5 × 60 = 300.', 'The angle must be in radians: 5 × π/3 = 5π/3.'),
          ('1 radian is about 1°.', '1 radian ≈ 57.3°.')],
))


@R.add('ch13-st4', 'C1', (1, 3), 'mcq')
def radian_mcq(rng, slot):
    k = rng.choice([1, 2, 3, 4, 5, 7, 8, 9, 10, 11])
    d = rng.choice([6, 4, 3, 12])
    deg_ = 180 * k // d if (180 * k) % d == 0 else None
    if deg_ is None:
        return None
    r_ = sp.Rational(k, d) * pi
    if rng.random() < 0.5:
        return mcq(rng, f'{deg_}° in radians is', P(r_), [P(r_ / 2), P(r_ * 2), P(pi - r_) if pi - r_ != r_ else P(r_ + pi)], '× π/180.')
    return mcq(rng, f'{P(r_)} radians in degrees is', f'{deg_}°', [f'{deg_ * 2}°', f'{deg_ // 2 if deg_ % 2 == 0 else deg_ + 30}°', f'{180 - deg_ if deg_ != 90 else 45}°'], '× 180/π.')


@R.add('ch13-st4', 'C3', (1, 4), 'short', style='p1')
def sector_exact(rng, slot):
    r = rng.randint(2, 12)
    th = rng.choice([pi / 6, pi / 4, pi / 3, pi / 2, 2 * pi / 3, 3 * pi / 4, 5 * pi / 6, 5 * pi / 4])
    kind = rng.choice(['both', 'perim', 'findtheta'])
    l, A = r * th, sp.Rational(r * r, 2) * th
    if kind == 'both':
        return mk(f'A sector has radius {r} cm and angle {P(th)} radians. Find, in exact form, the arc length and the area of the sector.', f'{P(l)} cm; {P(A)} cm²', f'l = rθ = {P(l)} (A1); A = (1/2)r²θ (M1); {P(A)} (A1).', 3)
    if kind == 'perim':
        return mk(f'A sector has radius {r} cm and angle {P(th)} radians. Find the exact perimeter of the sector.', f'{2 * r} + {P(l)} cm', f'arc {P(l)} (A1); add two radii (M1); {2 * r} + {P(l)} (A1).', 3)
    return mk(f'A sector of a circle of radius {r} cm has area {P(A)} cm². Find the angle of the sector in radians and in degrees.', f'{P(th)}; {int(th * 180 / pi)}°', f'(1/2)({r})²θ = {P(A)} (M1); θ = {P(th)} (A1); {int(th * 180 / pi)}° (A1).', 3)


@R.add('ch13-st4', 'C3', (2, 5), 'short', style='p2')
def segment_calc(rng, slot):
    r = rng.choice([4, 5, 6, 7.5, 8, 10, 12])
    th = rng.choice([0.8, 1.2, 1.5, 2.1, 2.5, 1.0])
    kind = rng.choice(['seg', 'chord', 'given_arc'])
    if kind == 'seg':
        return mk(f'A chord AB subtends an angle of {th:g} radians at the centre O of a circle of radius {r:g} cm. Find the area of the minor segment cut off by AB.', f'{s3(0.5 * r * r * (th - math.sin(th)))} cm²',
                  f'sector (1/2)r²θ = {s3(0.5 * r * r * th)} (A1); triangle (1/2)r² sin θ = {s3(0.5 * r * r * math.sin(th))} (M1 A1); difference {s3(0.5 * r * r * (th - math.sin(th)))} (A1).', 4)
    if kind == 'chord':
        return mk(f'In a circle of radius {r:g} cm, a chord subtends an angle of {th:g} radians at the centre. Find the chord length and the length of the minor arc.', f'{s3(2 * r * math.sin(th / 2))} cm; {s3(r * th)} cm',
                  f'chord 2r sin(θ/2) or cosine rule (M1 A1); arc rθ = {s3(r * th)} (A1).', 3)
    l = round(r * th, 1)
    return mk(f'A sector of radius {r:g} cm has arc length {l:g} cm. Find the angle of the sector in radians and the area of the sector.', f'{s3(l / r)} rad; {s3(0.5 * r * l)} cm²',
              f'θ = l/r (M1); {s3(l / r)} (A1); A = (1/2)rl or (1/2)r²θ = {s3(0.5 * r * l)} (A1).', 3)


@R.add('ch13-st4', 'C2', (2, 4), 'explain')
def radian_explain(rng, slot):
    r, d = rng.randint(3, 12), rng.choice([30, 45, 60, 90, 120])
    return mk(f'{who(rng)} finds the arc length of a sector with radius {r} cm and angle {d}° as {r} × {d} = {r * d} cm. Explain the error and find the correct arc length.', f'{P(r * sp.Rational(d, 180) * pi)} cm',
              f'l = rθ requires θ in radians (R1); {d}° = {P(sp.Rational(d, 180) * pi)} (A1); l = {P(r * sp.Rational(d, 180) * pi)} cm (A1).', 3, 'explain')


@R.add('ch13-st4', 'C4', (3, 5), 'multi_step', style='ext')
def sector_parts(rng, slot):
    r = rng.choice([5, 6, 8, 10])
    th = rng.choice([1.2, 1.4, 1.8, 2.2, 0.9])
    perim = 2 * r + r * th
    parts = [('Find the length of the arc AB.', f'{s3(r * th)} cm', 'A1', 1, True),
             ('Find the perimeter of the sector OAB.', f'{s3(perim)} cm', 'A1', 1, True),
             ('Find the area of the sector.', f'{s3(0.5 * r * r * th)} cm²', 'M1 A1', 2, True),
             ('Find the area of the shaded segment between the chord AB and the arc.', f'{s3(0.5 * r * r * (th - math.sin(th)))} cm²', 'M1 A1', 2, True),
             (f'A sector with the same perimeter {s3(perim)} cm has radius {r + 1} cm. Find its angle.', f'{s3((perim - 2 * (r + 1)) / (r + 1))} rad', 'M1 A1', 2, True),
             ('Find the angle in degrees of the original sector.', dg(math.degrees(th)), 'A1', 1, False)]
    return build_parts(rng, [f'OAB is a sector of a circle with centre O, radius {r} cm and angle AOB = {th:g} radians.', f'A sector OAB has radius {r} cm and centre angle {th:g} radians.'], parts, 4)


@R.add('ch13-st1', 'C4', (3, 5), 'multi_step', style='ext')
def cone_parts(rng, slot):
    r, h = rng.choice([(3, 4), (5, 12), (6, 8), (8, 15), (7, 24), (9, 12)])
    l = int(math.isqrt(r * r + h * h))
    k = rng.choice([2, 3])
    parts = [('Find the slant height of the cone.', f'{l} cm', 'A1', 1, True),
             ('Find the exact volume of the cone.', f'{P(sp.Rational(r * r * h, 3) * pi)} cm³', 'M1 A1', 2, True),
             ('Find the exact total surface area.', f'{P(r * l * pi + r * r * pi)} cm²', 'M1 A1', 2, True),
             ('Find the angle between the slant edge and the base.', dg(math.degrees(math.atan(h / r))), 'M1 A1', 2, True),
             (f'The cone is melted and recast as a sphere. Find the radius of the sphere.', f'{s3((r * r * h / 4) ** (1 / 3))} cm', '(4/3)πR³ = V (M1) A1', 2, True),
             (f'A similar cone has height {k * h} cm. Write down its volume.', f'{P(sp.Rational(r * r * h, 3) * pi * k ** 3)} cm³', 'scale factor cubed (R1) A1', 2, False)]
    return build_parts(rng, [f'A solid right circular cone has base radius {r} cm and height {h} cm.', f'A cone has radius {r} cm and perpendicular height {h} cm.'], parts, 4)


@R.add('ch13-st1', 'C2', (2, 4), 'explain')
def lineplane_explain(rng, slot):
    a, b, c = rng.randint(3, 10), rng.randint(3, 10), rng.randint(3, 10)
    return mk(f'In a cuboid with base {a} cm by {b} cm and height {c} cm, {who(rng)} says the angle between a space diagonal and the base is arctan({c}/{a}). Explain the error and find the correct angle.', dg(math.degrees(math.atan(c / math.hypot(a, b)))),
              f'the angle is between the diagonal and its projection, the base diagonal √({a}² + {b}²) = {s3(math.hypot(a, b))} (R1); tan θ = {c}/{s3(math.hypot(a, b))} (M1); {dg(math.degrees(math.atan(c / math.hypot(a, b))))} (A1).', 3, 'explain')
