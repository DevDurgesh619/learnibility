"""IB MYP 4 Mathematics (Standard & Extended) – ib-g9-maths.

Criteria language: A knowing & understanding, B investigating patterns, C communicating,
D applying mathematics in real-life contexts. Items use international contexts.
"""
from __future__ import annotations

import math
from fractions import Fraction as Fr

import sympy as sp

from _common import F, Registry, T, fmt, frac, mcq, name, num_distractors, pe, sup, two_names, CITIES

CONFIG = {'minutesPerMark': 1.25, 'mcqMinutes': 1.5}

# MYP 5 eAssessment-style paper (practised early in MYP 4): 3 tasks, 25 items, 100 marks.
MOCK = [
    dict(section='Task 1 – Knowing and understanding (criterion A)', count=10, c=['C1', 'C3'], d=[2, 2, 3], marks=3),
    dict(section='Task 2 – Investigating patterns (criterion B)', count=7, c=['C2', 'C3', 'C4'], d=[3, 3, 4], marks=4),
    dict(section='Task 3 – Applying mathematics in real-life contexts (criterion D)', count=8, c=['C3', 'C4'], d=[3, 4, 4, 5], marks=5),
]

R = Registry()
x, y = sp.symbols('x y')


def init(subject_id):
    pass


def templates(st):
    return R.build(st)


def _lin(a, b, v='x'):
    """a·x + b as text."""
    s = ('' if a == 1 else '−' if a == -1 else str(a)) + v
    if b > 0:
        s += f' + {b}'
    elif b < 0:
        s += f' − {-b}'
    return s.replace('-', '−') if s.startswith('-') else s


def m(s):
    return str(s).replace('-', '−')


# =============================================================================================
# ch01 Real Numbers and Surds
# =============================================================================================
R.facts('ch01-st1', F(
    terms=[('rational number', 'a number that can be written as p/q where p and q are integers and q ≠ 0'),
           ('irrational number', 'a real number that cannot be written as a fraction of two integers; its decimal neither terminates nor recurs'),
           ('integer', 'a whole number that may be positive, negative or zero'),
           ('real number', 'any number that can be placed on the number line, rational or irrational')],
    facts=[('Which of the following sets contains only rational numbers?', '{−3, 0.25, 4/7, 0.3̅}', ['{−3, √2, 4/7}', '{π, 0.25, 1}', '{√9, √10, 2}'], '√2, π and √10 are irrational; 0.3̅ = 1/3 is rational.'),
           ('Which statement about ℕ, ℤ and ℚ is true?', 'ℕ ⊂ ℤ ⊂ ℚ', ['ℚ ⊂ ℤ ⊂ ℕ', 'ℤ ⊂ ℕ ⊂ ℚ', 'ℕ and ℚ have no common elements'], 'Every natural number is an integer and every integer n can be written n/1.'),
           ('Which of these numbers is NOT rational?', '√12', ['√16', '0.12̅', '−7/3'], '12 is not a perfect square, so √12 = 2√3 is irrational.')],
    why=[('Explain why every terminating decimal is a rational number.', 'A terminating decimal with k decimal places equals an integer divided by 10ᵏ, which is a fraction p/q with integer p and q ≠ 0.'),
         ('Explain why 22/7 cannot be equal to π.', '22/7 is a ratio of two integers so it is rational; π is irrational, so they cannot be equal – 22/7 is only an approximation (≈ 3.1429 vs 3.1416).'),
         ('Explain why the square root of a prime number is always irrational.', 'If √p = a/b in lowest terms then p·b² = a², so p divides a; writing a = pk gives b² = pk², so p divides b too – contradicting lowest terms.'),
         ('Explain why a recurring decimal such as 0.4̅ is rational.', 'Let x = 0.444…; then 10x = 4.444…, so 9x = 4 and x = 4/9, a ratio of integers.')],
    misc=[('The sum of two irrational numbers is always irrational.', 'False: √2 + (−√2) = 0, which is rational. The sum can be rational or irrational.'),
          ('√16 is irrational because it is written with a root sign.', 'The root sign does not decide it: √16 = 4, an integer, so it is rational.'),
          ('0.101001000100001… is rational because it has a pattern.', 'It has a pattern but no block of digits repeats forever, so it neither terminates nor recurs – it is irrational.')],
    evaluate=[('Between any two rational numbers there is always an irrational number.', ['for a < b, a + (b − a)/√2 lies strictly between a and b and is irrational', 'this works for every pair, so the claim holds in general'], ['a student might try only "nice" decimals and wrongly find none'], 'True: a + (b − a)/√2 is always irrational and lies between a and b.')],
))


@R.add('ch01-st1', 'C1', (1, 2), 'mcq')
def irr_mcq(rng, slot):
    sq = rng.choice([4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144])
    ns = rng.choice([2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 15, 18, 20])
    p, q = rng.randint(1, 9), rng.choice([3, 7, 9, 11])
    return mcq(rng, 'Which one of the following numbers is irrational?', f'√{ns}',
               [f'√{sq}', f'{p}/{q}', f'0.{p}{q % 10}̅'], f'{ns} is not a perfect square, so √{ns} is irrational; √{sq} = {int(math.isqrt(sq))}.')


@R.add('ch01-st1', 'C3', (2, 3), 'short')
def recurring(rng, slot):
    if slot.d <= 2:
        ab = rng.randint(10, 98)
        fr = Fr(ab, 99)
        dec = f'0.{ab:02d}' + '̅'
        return dict(stem=f'Write the recurring decimal 0.{ab:02d}{ab:02d}{ab:02d}… as a fraction in its simplest form.',
                    answer=frac(fr), markingKey=f'Let x = 0.{ab:02d}…; 100x − x = {ab}, so x = {ab}/99 = {frac(fr)}. M1 for 100x − x, A1 simplest form.', marks=2)
    a, bc = rng.randint(1, 9), rng.randint(10, 98)
    # 0.a(bc)  = (abc - a)/990
    num = a * 100 + bc - a
    fr = Fr(num, 990)
    return dict(stem=f'Express 0.{a}{bc}{bc}{bc}… (the digits {bc} recur) as a fraction in its simplest form.',
                answer=frac(fr), markingKey=f'x = 0.{a}{bc}…; 1000x − 10x = {a}{bc} − {a} = {num}, so x = {num}/990 = {frac(fr)}. M1 correct multipliers, M1 subtraction, A1.', marks=3)


@R.add('ch01-st1', 'C3', (1, 3), 'short')
def between(rng, slot):
    a = rng.randint(2, 12)
    lo, hi = a * a - rng.randint(1, 3), (a + 1) ** 2 + rng.randint(1, 4)
    ints = [k for k in range(1, 40) if lo < k * k < hi]
    return dict(stem=f'List all the integers n such that √{lo} < n < √{hi}.', answer=', '.join(map(str, ints)),
                markingKey=f'Square the bounds: {lo} < n² < {hi}, so n = ' + ', '.join(map(str, ints)) + '. A1 for each correct value, −1 for any extra.', marks=2)


@R.add('ch01-st1', 'C4', (3, 5), 'multi_step')
def prove_irr(rng, slot):
    r = rng.choice([2, 3, 5, 7])
    p, q = rng.randint(1, 5), rng.randint(2, 6)
    return dict(stem=f'Given that √{r} is irrational, prove that {p} + {q}√{r} is irrational.',
                answer=f'Suppose {p} + {q}√{r} = a/b (rational). Then √{r} = (a/b − {p})/{q}, which is rational – a contradiction. Hence {p} + {q}√{r} is irrational.',
                markingKey=f'M1 assume rational; M1 rearrange to make √{r} the subject; R1 rational numbers are closed under +, −, ×, ÷ (non-zero); A1 contradiction stated. Criterion C: clear logical chain.', marks=4, gap='G5')


R.facts('ch01-st2', F(
    terms=[('surd', 'an irrational root such as √2 or ∛5 that is left in root form to keep the value exact'),
           ('simplest surd form', 'a surd written as a√b where b has no square factor other than 1')],
    why=[('Explain why √12 can be written as 2√3.', '√12 = √(4 × 3) = √4 × √3 = 2√3, using √(ab) = √a·√b and the square factor 4.'),
         ('Explain why √a × √a = a for a ≥ 0.', 'By definition √a is the non-negative number whose square is a, so √a × √a = (√a)² = a.'),
         ('Explain why it is helpful to take out the largest square factor when simplifying a surd.', 'Taking the largest square factor at once leaves no square factor inside, so the surd is fully simplified in one step (e.g. √72 = 6√2, not 2√18).')],
    misc=[('√(9 + 16) = √9 + √16 = 7.', '√(9 + 16) = √25 = 5. Roots multiply over products (√ab = √a√b) but do not split over sums.'),
          ('√50 in simplest form is 5√10.', '√50 = √(25 × 2) = 5√2. 5√10 = √250.'),
          ('√8 × √2 = √10.', '√8 × √2 = √16 = 4; the numbers under the root multiply, they do not add.')],
))


def _surd_parts(n):
    a = 1
    for k in range(int(math.isqrt(n)), 1, -1):
        if n % (k * k) == 0:
            a = k
            break
    return a, n // (a * a)


def _surd(a, b):
    if b == 1:
        return str(a)
    return f'{"" if a == 1 else a}√{b}'


@R.add('ch01-st2', 'C1', (1, 3), 'mcq')
def surd_simplify_mcq(rng, slot):
    a, b = rng.randint(2, 9), rng.choice([2, 3, 5, 6, 7, 10, 11])
    n = a * a * b
    wrong = [_surd(b, a * a) if a * a != b else f'{a + 1}√{b}', f'{a + 1}√{b}', f'{a}√{b * 2}', f'{a * a}√{b}']
    wrong = [w for w in wrong if w != _surd(a, b)][:3]
    return mcq(rng, f'Which of the following is √{n} written in simplest surd form?', _surd(a, b), wrong,
               f'√{n} = √({a * a} × {b}) = {a}√{b}.')


@R.add('ch01-st2', 'C3', (1, 3), 'short')
def surd_simplify(rng, slot):
    k = 1 if slot.d <= 1 else 2 if slot.d == 2 else 3
    parts = []
    for _ in range(k):
        a, b = rng.randint(2, 8), rng.choice([2, 3, 5, 7])
        parts.append((a, b))
    if k == 1:
        a, b = parts[0]
        return dict(stem=f'Simplify √{a * a * b}.', answer=_surd(a, b), markingKey=f'√{a * a * b} = √{a * a}·√{b} = {_surd(a, b)}. A1.', marks=1)
    a1, b1 = parts[0]
    a2 = rng.randint(2, 6)
    n1, n2 = a1 * a1 * b1, a2 * a2 * b1
    sign = rng.choice(['+', '−'])
    res = a1 + a2 if sign == '+' else a1 - a2
    ans = '0' if res == 0 else _surd(res, b1) if res > 0 else f'−{_surd(-res, b1)}'
    return dict(stem=f'Simplify √{n1} {sign} √{n2}, giving your answer in the form a√b.', answer=ans,
                markingKey=f'√{n1} = {_surd(a1, b1)}, √{n2} = {_surd(a2, b1)} (M1 each); combine like surds: {ans} (A1).', marks=3)


@R.add('ch01-st2', 'C3', (2, 4), 'short')
def surd_multiply(rng, slot):
    a, b, c, d_ = rng.randint(2, 6), rng.choice([2, 3, 5, 6]), rng.randint(2, 6), rng.choice([2, 3, 5, 6, 10])
    prod_coef, inside = a * c, b * d_
    s, t = _surd_parts(inside)
    ans = _surd(prod_coef * s, t)
    return dict(stem=f'Simplify {a}√{b} × {c}√{d_}, giving your answer in simplest form.', answer=ans,
                markingKey=f'{a}×{c} = {prod_coef}, √{b}×√{d_} = √{inside} = {_surd(s, t)} (M1); result {ans} (A1).', marks=2)


@R.add('ch01-st2', 'C2', (2, 4), 'explain')
def surd_compare(rng, slot):
    a, b = rng.randint(2, 7), rng.choice([2, 3, 5])
    c = rng.randint(2, 7)
    d_ = rng.choice([v for v in [2, 3, 5, 6, 7] if v != b])
    n1, n2 = a * a * b, c * c * d_
    big = f'{a}√{b}' if n1 > n2 else f'{c}√{d_}'
    if n1 == n2:
        return None
    return dict(stem=f'Without a calculator, explain which is larger: {a}√{b} or {c}√{d_}.', answer=big,
                markingKey=f'Write each as a single root: {a}√{b} = √{n1}, {c}√{d_} = √{n2}. Since {max(n1, n2)} > {min(n1, n2)}, {big} is larger. M1 converting both, R1 comparison.', type='explain', marks=2)


@R.add('ch01-st2', 'C4', (3, 5), 'multi_step')
def surd_area(rng, slot):
    a, b = rng.randint(2, 5), rng.choice([2, 3, 5])
    c = rng.randint(2, 6)
    w = rng.choice([2, 3, 5, 6, 7])
    return dict(stem=f'A rectangle has length √{a * a * b * w} cm and width √{c * c * b} cm. Find its exact area and its exact perimeter, simplifying both.',
                answer=f'Area = {_surd(*_surd_parts(a * a * b * w * c * c * b))} cm²; perimeter = 2({_surd(*_surd_parts(a * a * b * w))} + {_surd(c, b)}) cm',
                markingKey=f'Area = √{a * a * b * w} × √{c * c * b} = √{a * a * b * w * c * c * b} = {_surd(*_surd_parts(a * a * b * w * c * c * b))} (M1 A1). Perimeter = 2({_surd(*_surd_parts(a * a * b * w))} + {_surd(c, b)}) cm (M1 A1); combine further only if the surds are like.', marks=5, gap='G5')


R.facts('ch01-st3', F(
    terms=[('like surds', 'surds with the same number under the root, such as 3√5 and −7√5, which can be added or subtracted'),
           ('conjugate', 'the expression a − √b paired with a + √b; their product (a² − b) contains no surd')],
    why=[('Explain why 2√3 + 5√2 cannot be simplified to a single surd.', '√3 and √2 are unlike surds (different radicands), just as 2a + 5b cannot be combined; neither can be rewritten as a multiple of the other.'),
         ('Explain why (√a + √b)² is not equal to a + b.', '(√a + √b)² = a + 2√(ab) + b; the middle term 2√(ab) comes from expanding the brackets and is lost if you square each term separately.'),
         ('Explain why (3 + √2)(3 − √2) gives a whole number.', 'It is a difference of two squares: 3² − (√2)² = 9 − 2 = 7; the surd terms +3√2 and −3√2 cancel.')],
    misc=[('3√2 + 4√2 = 7√4 = 14.', 'Like surds add like algebraic terms: 3√2 + 4√2 = 7√2. The radicand does not change.'),
          ('(2 + √5)² = 4 + 5 = 9.', '(2 + √5)² = 4 + 4√5 + 5 = 9 + 4√5; the cross term 2 × 2 × √5 is missing.')],
))


@R.add('ch01-st3', 'C3', (1, 3), 'short')
def surd_expand(rng, slot):
    a, b = rng.randint(1, 6), rng.randint(1, 5)
    r = rng.choice([2, 3, 5, 7])
    if slot.d <= 2:
        c = rng.randint(2, 6)
        return dict(stem=f'Expand and simplify √{r}({c} + √{r}).', answer=f'{c}√{r} + {r}',
                    markingKey=f'√{r} × {c} = {c}√{r}; √{r} × √{r} = {r}. Answer {c}√{r} + {r}. A1 each term.', marks=2)
    c, d_ = rng.randint(1, 5), rng.randint(1, 4)
    # (a + b√r)(c + d√r) = ac + bd r + (ad + bc)√r
    const = a * c + b * d_ * r
    sc = a * d_ + b * c
    lhs = f'({a} + {"" if b == 1 else b}√{r})({c} + {"" if d_ == 1 else d_}√{r})'
    return dict(stem=f'Expand and simplify {lhs}, giving your answer in the form p + q√{r}.', answer=f'{const} + {sc}√{r}',
                markingKey=f'Four products: {a * c}, {a * d_}√{r}, {b * c}√{r}, {b * d_}×{r} = {b * d_ * r} (M1 for at least 3 correct). Collect: {const} + {sc}√{r} (A1 A1).', marks=3)


@R.add('ch01-st3', 'C3', (2, 4), 'short')
def surd_square(rng, slot):
    a, r = rng.randint(1, 6), rng.choice([2, 3, 5, 6, 7])
    sign = rng.choice(['+', '−'])
    const = a * a + r
    mid = 2 * a
    return dict(stem=f'Expand (√{r} {sign} {a})².', answer=f'{const} {sign} {mid}√{r}',
                markingKey=f'(√{r})² = {r}, 2 × √{r} × {a} = {mid}√{r}, {a}² = {a * a}. Answer {const} {sign} {mid}√{r}. M1 three terms, A1.', marks=2)


@R.add('ch01-st3', 'C2', (2, 3), 'explain')
def surd_like(rng, slot):
    a, b, r = rng.randint(2, 5), rng.randint(2, 5), rng.choice([2, 3, 5])
    n1, n2 = a * a * r, b * b * r
    return dict(stem=f'√{n1} and √{n2} do not look like like surds. Show that they are, and hence simplify √{n1} + √{n2}.',
                answer=f'{a + b}√{r}', markingKey=f'√{n1} = {a}√{r}, √{n2} = {b}√{r}: both are multiples of √{r} (R1), so the sum is {a + b}√{r} (A1).', type='explain', marks=2)


@R.add('ch01-st3', 'C4', (3, 5), 'multi_step')
def surd_solve(rng, slot):
    r = rng.choice([2, 3, 5])
    p, q = rng.randint(1, 4), rng.randint(1, 3)
    # (p + q√r)² = p² + q² r + 2pq √r = A + B√r
    A, B = p * p + q * q * r, 2 * p * q
    return dict(stem=f'Given that (a + b√{r})² = {A} + {B}√{r}, where a and b are positive integers, find a and b.',
                answer=f'a = {p}, b = {q}', markingKey=f'Expand: a² + {r}b² + 2ab√{r} (M1). Equate: a² + {r}b² = {A} and 2ab = {B} so ab = {p * q} (M1). Test factor pairs → a = {p}, b = {q} (A1 A1).', marks=5, gap='G5')


R.facts('ch01-st4', F(
    terms=[('rationalising the denominator', 'rewriting a fraction so that its denominator contains no surd, by multiplying top and bottom by a suitable surd or conjugate')],
    why=[('Explain why multiplying 5/√3 by √3/√3 does not change its value.', '√3/√3 = 1, and multiplying by 1 leaves the value unchanged while making the denominator √3 × √3 = 3.'),
         ('Explain why the conjugate is used to rationalise 1/(2 + √3).', 'Multiplying by (2 − √3)/(2 − √3) gives a denominator (2 + √3)(2 − √3) = 4 − 3 = 1, a difference of squares with no surd.'),
         ('Explain why rationalised answers are preferred in IB mark schemes.', 'They are in a standard simplest form, so equivalent answers can be compared easily, and they are easier to estimate or add to other surds.')],
    misc=[('To rationalise 4/(3 + √2) you multiply top and bottom by √2.', 'Multiplying by √2 gives 3√2 + 2 in the denominator – still a surd. Use the conjugate 3 − √2: denominator 9 − 2 = 7.'),
          ('6/√2 = 6√2/2 = 3, because the √2 cancels.', '6√2/2 = 3√2; only the 2 divides, the √2 stays in the numerator.')],
))


@R.add('ch01-st4', 'C3', (1, 3), 'short')
def rat_simple(rng, slot):
    r = rng.choice([2, 3, 5, 6, 7])
    k = rng.choice([1, 2, 3, 4]) * r if slot.d >= 2 else rng.randint(1, 9)
    num = k
    fr = Fr(num, r)
    if fr.denominator == 1:
        ans = f'{"" if fr.numerator == 1 else fr.numerator}√{r}'
    else:
        ans = f'{"" if fr.numerator == 1 else fr.numerator}√{r}/{fr.denominator}'
    return dict(stem=f'Rationalise the denominator of {num}/√{r}, simplifying fully.', answer=ans,
                markingKey=f'Multiply by √{r}/√{r}: {num}√{r}/{r} (M1) = {ans} (A1).', marks=2)


@R.add('ch01-st4', 'C3', (2, 4), 'short')
def rat_conj(rng, slot):
    a, r = rng.randint(2, 6), rng.choice([2, 3, 5, 7])
    if a * a == r:
        return None
    k = rng.randint(1, 6)
    den = a * a - r
    sign = rng.choice(['+', '−'])
    conj = '−' if sign == '+' else '+'
    # k/(a ± √r) = k(a ∓ √r)/den
    g = math.gcd(k, den)
    kk, dd = k // g, den // g
    if dd < 0:
        kk, dd = -kk, -dd
    inner = f'{a} {conj} √{r}'
    if dd == 1:
        ans = f'{kk if kk != 1 else ""}({inner})'.replace('-1(', '−(').replace('-', '−')
    else:
        ans = f'{kk if kk != 1 else ""}({inner})/{dd}'.replace('-', '−')
    return dict(stem=f'Rationalise the denominator of {k}/({a} {sign} √{r}).', answer=ans,
                markingKey=f'Multiply by ({inner})/({inner}) (M1); denominator {a}² − {r} = {den} (A1); answer {ans} (A1).', marks=3)


@R.add('ch01-st4', 'C4', (3, 5), 'multi_step')
def rat_combo(rng, slot):
    r = rng.choice([2, 3, 5])
    a = rng.randint(2, 4)
    if a * a == r:
        return None
    # 1/(a+√r) + 1/(a−√r) = 2a/(a² − r)
    den = a * a - r
    res = Fr(2 * a, den)
    return dict(stem=f'Show that 1/({a} + √{r}) + 1/({a} − √{r}) is rational, and find its value.', answer=frac(res),
                markingKey=f'Common denominator ({a} + √{r})({a} − √{r}) = {den} (M1 A1); numerator ({a} − √{r}) + ({a} + √{r}) = {2 * a} (A1); value {frac(res)}, rational because the surds cancel (R1).', marks=4, gap='G5')


@R.add('ch01-st4', 'C2', (2, 4), 'explain')
def rat_check(rng, slot):
    r = rng.choice([2, 3, 5, 7])
    k = rng.randint(2, 9)
    return dict(stem=f'{name(rng)} says that {k}/√{r} and {k}√{r}/{r} are equal. Explain whether this is correct, without using a calculator.',
                answer='Correct', markingKey=f'{k}/√{r} × √{r}/√{r} = {k}√{r}/{r}: multiplying by √{r}/√{r} = 1 does not change the value (R1). Alternatively cross-multiply: {k}·{r} = {k}√{r}·√{r} (R1).', type='explain', marks=2)


# =============================================================================================
# ch02 Indices and Standard Form
# =============================================================================================
R.facts('ch02-st1', F(
    terms=[('index (exponent)', 'the small raised number showing how many times the base is multiplied by itself'),
           ('base', 'the number or variable that is raised to a power')],
    why=[('Explain why a⁰ = 1 for any non-zero a.', 'aⁿ ÷ aⁿ = aⁿ⁻ⁿ = a⁰ by the division law, and any non-zero number divided by itself is 1.'),
         ('Explain why a⁻ⁿ = 1/aⁿ.', 'a⁰ ÷ aⁿ = a⁻ⁿ by the division law, and a⁰ ÷ aⁿ = 1/aⁿ, so the two are equal.'),
         ('Explain why (a³)⁴ = a¹² rather than a⁷.', '(a³)⁴ means a³ × a³ × a³ × a³; adding the four indices 3 + 3 + 3 + 3 gives 12, i.e. multiply the indices.')],
    misc=[('2³ × 3² = 6⁵.', 'The product law needs the same base: 2³ × 3² = 8 × 9 = 72, whereas 6⁵ = 7776.'),
          ('(2x)³ = 2x³.', 'The power applies to every factor in the bracket: (2x)³ = 8x³.'),
          ('5⁻² = −25.', 'A negative index means reciprocal, not a negative number: 5⁻² = 1/25.')],
))


@R.add('ch02-st1', 'C1', (1, 3), 'mcq')
def idx_mcq(rng, slot):
    a, b = rng.randint(2, 9), rng.randint(2, 9)
    base = rng.choice(['x', 'y', 'p', 'k'])
    op = rng.choice(['×', '÷', '()'])
    if op == '×':
        stem, ans, w = f'{base}{sup(a)} × {base}{sup(b)}', f'{base}{sup(a + b)}', [f'{base}{sup(a * b)}', f'{base}{sup(abs(a - b))}', f'{2}{base}{sup(a + b)}']
    elif op == '÷':
        if a == b:
            return None
        stem, ans, w = f'{base}{sup(a)} ÷ {base}{sup(b)}', f'{base}{sup(a - b)}', [f'{base}{sup(a + b)}', f'{base}{sup(b - a) if b != a else 1}', f'{base}{sup(round(a / b, 1)) if a % b == 0 else sup(a * b)}']
    else:
        stem, ans, w = f'({base}{sup(a)}){sup(b)}', f'{base}{sup(a * b)}', [f'{base}{sup(a + b)}', f'{base}{sup(a) + sup(b)}', f'{b}{base}{sup(a)}']
    return mcq(rng, f'Simplify {stem}.', ans, w, f'{stem} = {ans} by the laws of indices.')


@R.add('ch02-st1', 'C3', (2, 4), 'short')
def idx_simplify(rng, slot):
    a, b, c = rng.randint(2, 6), rng.randint(2, 6), rng.randint(1, 4)
    k1, k2 = rng.randint(2, 6), rng.randint(2, 4)
    if slot.d <= 2:
        return dict(stem=f'Simplify {k1}x{sup(a)} × {k2}x{sup(b)}.', answer=f'{k1 * k2}x{sup(a + b)}',
                    markingKey=f'Multiply coefficients {k1}×{k2} = {k1 * k2}; add indices {a}+{b} = {a + b}. A1 A1.', marks=2)
    p = rng.randint(2, 3)
    num_c, num_x, num_y = k1 ** p * k2, a * p + c, b * p
    den_c = rng.choice([d for d in [2, 3, 4, 6] if (num_c % d == 0)] or [1])
    den_x, den_y = rng.randint(1, a * p), rng.randint(1, b * p)
    res_c, rx, ry = num_c // den_c, num_x - den_x, num_y - den_y
    def term(v, e):
        return '' if e == 0 else v if e == 1 else f'{v}{sup(e)}'
    res = f'{res_c}{term("x", rx)}{term("y", ry)}'
    return dict(stem=f'Simplify ({k1}x{sup(a)}y{sup(b)}){sup(p)} × {k2}x{sup(c)} ÷ ({den_c}x{sup(den_x)}y{sup(den_y)}).', answer=res,
                markingKey=f'({k1}x{sup(a)}y{sup(b)}){sup(p)} = {k1 ** p}x{sup(a * p)}y{sup(b * p)} (M1); × {k2}x{sup(c)} → {num_c}x{sup(num_x)}y{sup(num_y)} (M1); ÷ → {res} (A1 A1).', marks=4)


@R.add('ch02-st1', 'C3', (2, 3), 'short')
def idx_negative(rng, slot):
    a, n = rng.choice([2, 3, 4, 5, 10]), rng.randint(1, 3)
    p, q = rng.randint(1, 5), rng.randint(2, 7)
    if math.gcd(p, q) != 1:
        return None
    val = Fr(q, p) ** n
    return dict(stem=f'Evaluate ({p}/{q}){sup(-n)}, giving your answer as a fraction.', answer=frac(val),
                markingKey=f'Negative index → reciprocal: ({q}/{p}){sup(n)} (M1) = {frac(val)} (A1).', marks=2)


@R.add('ch02-st1', 'C4', (3, 5), 'multi_step')
def idx_equation(rng, slot):
    b = rng.choice([2, 3, 5])
    p, q = rng.randint(2, 4), rng.randint(1, 5)
    k = rng.randint(1, 4)
    # (b^p)^(x) = b^(q x + k) -> p x = q x + k -> x = k/(p - q)
    if p == q:
        return None
    sol = Fr(k, p - q)
    return dict(stem=f'Solve {b ** p}ˣ = {b}^({q}x + {k}).', answer=f'x = {frac(sol)}',
                markingKey=f'Write {b ** p} as {b}{sup(p)} (M1): {b}^({p}x) = {b}^({q}x + {k}); equate indices {p}x = {q}x + {k} (M1); x = {frac(sol)} (A1).', marks=4, gap='G5')


@R.add('ch02-st1', 'C2', (2, 4), 'explain')
def idx_pattern(rng, slot):
    b = rng.choice([2, 3, 5])
    return dict(stem=f'Copy and complete the pattern {b}³ = {b ** 3}, {b}² = {b ** 2}, {b}¹ = {b}, {b}⁰ = ?, {b}⁻¹ = ?, {b}⁻² = ?. Describe the rule that links each term to the next and use it to justify your values (criterion B).',
                answer=f'{b}⁰ = 1, {b}⁻¹ = 1/{b}, {b}⁻² = 1/{b * b}',
                markingKey=f'Each step down in the index divides by {b} (B1 rule). So {b}⁰ = {b} ÷ {b} = 1, {b}⁻¹ = 1/{b}, {b}⁻² = 1/{b * b} (A1 A1). Justification refers to the rule (C1).', type='explain', marks=4)


R.facts('ch02-st2', F(
    terms=[('fractional index', 'an index of the form m/n meaning the n-th root raised to the power m: a^(m/n) = (ⁿ√a)ᵐ')],
    why=[('Explain why 9^(1/2) = 3.', '(9^(1/2))² = 9^(1/2 × 2) = 9¹ = 9, so 9^(1/2) is the positive number whose square is 9, i.e. 3.'),
         ('Explain why it is easier to find 8^(2/3) by taking the cube root first.', '8^(2/3) = (∛8)² = 2² = 4; rooting first keeps the numbers small, whereas 8² = 64 then ∛64 = 4 needs a bigger root.'),
         ('Explain why (−8)^(1/3) is defined but (−8)^(1/2) is not a real number.', 'A cube root of a negative number exists (−2 × −2 × −2 = −8) but no real number squared gives −8.')],
    misc=[('16^(1/2) = 8, because half of 16 is 8.', 'An index of 1/2 means square root, not halving: 16^(1/2) = 4.'),
          ('27^(−1/3) = −3.', 'The negative index means reciprocal: 27^(−1/3) = 1/∛27 = 1/3.')],
))


@R.add('ch02-st2', 'C1', (1, 3), 'mcq')
def fracidx_mcq(rng, slot):
    r, n = rng.choice([(2, 3), (3, 2), (2, 2), (4, 2), (5, 2), (2, 4), (3, 3), (2, 5), (10, 2), (10, 3)]) if True else None
    base = r ** n
    return mcq(rng, f'What is the value of {base}^(1/{n})?', str(r), [str(base // n) if base % n == 0 else str(r + 1), str(r * n), str(base ** 2 if base < 20 else r - 1)],
               f'{base}^(1/{n}) is the {n}-th root of {base}, which is {r} because {r}{sup(n)} = {base}.')


@R.add('ch02-st2', 'C3', (2, 4), 'short')
def fracidx_eval(rng, slot):
    r, n = rng.choice([(2, 3), (3, 2), (2, 2), (4, 2), (5, 2), (2, 4), (3, 3), (2, 5), (4, 3), (3, 4)])
    mm = rng.choice([2, 3]) if slot.d >= 3 else rng.choice([1, 2])
    base = r ** n
    neg = slot.d >= 3 and rng.random() < 0.6
    val = Fr(r ** mm) if not neg else Fr(1, r ** mm)
    e = f'{"−" if neg else ""}{mm}/{n}'
    return dict(stem=f'Evaluate {base}^({e}) without a calculator.', answer=frac(val),
                markingKey=f'{n}-th root of {base} = {r} (M1); raise to power {mm}: {r ** mm} (M1)' + (f'; negative index → reciprocal {frac(val)} (A1).' if neg else f' = {frac(val)} (A1).'), marks=3 if neg else 2)


@R.add('ch02-st2', 'C4', (3, 5), 'multi_step')
def fracidx_solve(rng, slot):
    r = rng.choice([2, 3, 4, 5])
    n = rng.choice([2, 3])
    mm = rng.choice([2, 3])
    val = r ** mm  # x^(m/n) = val -> x = val^(n/m) = r^n
    return dict(stem=f'Solve x^({mm}/{n}) = {val} for x > 0.', answer=f'x = {r ** n}',
                markingKey=f'Raise both sides to the power {n}/{mm} (M1): x = {val}^({n}/{mm}) = ({mm}-th root of {val}){sup(n)} = {r}{sup(n)} (M1) = {r ** n} (A1). Check: ({n}-th root of {r ** n}){sup(mm)} = {r}{sup(mm)} = {val} (R1).', marks=4, gap='G5')


@R.add('ch02-st2', 'C2', (2, 4), 'explain')
def fracidx_rewrite(rng, slot):
    n = rng.choice([3, 4, 5])
    mm = rng.choice([2, 3])
    if math.gcd(n, mm) != 1:
        return None
    v = rng.choice(['x', 'a', 'y'])
    return dict(stem=f'Write the {n}-th root of {v}{sup(mm)} in index form and explain each part of the index.', answer=f'{v}^({mm}/{n})',
                markingKey=f'{v}^({mm}/{n}) (A1): the denominator {n} is the root, the numerator {mm} is the power (R1); valid because ({v}^({mm}/{n})){sup(n)} = {v}{sup(mm)} (R1).', type='explain', marks=3)


R.facts('ch02-st3', F(
    terms=[('standard form', 'a number written as a × 10ⁿ where 1 ≤ a < 10 and n is an integer'),
           ('order of magnitude', 'the power of ten nearest to the size of a number, used to compare very large or small quantities')],
    why=[('Explain why 45 × 10³ is not in standard form.', 'The front number must satisfy 1 ≤ a < 10; 45 is too big. Correct form: 4.5 × 10⁴.'),
         ('Explain why multiplying numbers in standard form involves adding the powers of ten.', '(a × 10ᵐ)(b × 10ⁿ) = ab × 10ᵐ × 10ⁿ = ab × 10ᵐ⁺ⁿ by the product law of indices.'),
         ('Explain why a negative power of ten means the number is less than 1.', '10⁻ⁿ = 1/10ⁿ, so a × 10⁻ⁿ with a < 10 is less than 10/10ⁿ ≤ 1.')],
    misc=[('0.00056 = 5.6 × 10⁴.', 'Small numbers have a negative power: 0.00056 = 5.6 × 10⁻⁴ (the point moves 4 places right).'),
          ('(3 × 10⁴) × (4 × 10⁵) = 12 × 10⁹, which is in standard form.', '12 × 10⁹ must be adjusted to 1.2 × 10¹⁰.')],
))


@R.add('ch02-st3', 'C1', (1, 3), 'mcq')
def sf_mcq(rng, slot):
    a = rng.randint(11, 99)
    n = rng.randint(3, 8)
    small = rng.random() < 0.5
    if small:
        num = '0.' + '0' * (n - 1) + str(a)
        ans = f'{a / 10} × 10{sup(-n)}'
        w = [f'{a / 10} × 10{sup(n)}', f'{a} × 10{sup(-n - 1)}', f'{a / 10} × 10{sup(-n + 1)}']
    else:
        num = f'{a * 10 ** (n - 1):,}'.replace(',', ' ')
        ans = f'{a / 10} × 10{sup(n)}'
        w = [f'{a / 10} × 10{sup(n - 1)}', f'{a} × 10{sup(n - 1)}', f'{a / 10} × 10{sup(-n)}']
    return mcq(rng, f'Write {num} in standard form.', ans, w, f'{num} = {ans}.')


@R.add('ch02-st3', 'C3', (2, 4), 'numerical')
def sf_calc(rng, slot):
    a, b = rng.randint(11, 95) / 10, rng.randint(11, 95) / 10
    m_, n_ = rng.randint(3, 9), rng.randint(-6, 6)
    op = rng.choice(['×', '÷'])
    v = a * 10 ** m_ * b * 10 ** n_ if op == '×' else a * 10 ** m_ / (b * 10 ** n_)
    e = math.floor(math.log10(v))
    mant = v / 10 ** e
    ans = f'{mant:.3g} × 10{sup(e)}'
    return dict(stem=f'Calculate ({a} × 10{sup(m_)}) {op} ({b} × 10{sup(n_)}), giving your answer in standard form to 3 significant figures.',
                answer=ans, markingKey=f'{"Multiply" if op == "×" else "Divide"} the numbers ({round(a * b if op == "×" else a / b, 4)}) and {"add" if op == "×" else "subtract"} the powers (M1); adjust so 1 ≤ a < 10: {ans} (A1).', type='numerical', marks=2)


@R.add('ch02-st3', 'C4', (3, 5), 'multi_step')
def sf_context(rng, slot):
    ctx = rng.choice([
        ('light travels at 3.00 × 10⁸ m/s', 'the Sun is 1.50 × 10¹¹ m from Earth', 'How long, in minutes, does light take to travel from the Sun to Earth?', 1.5e11 / 3e8 / 60, 'minutes'),
        ('a red blood cell has a diameter of 7.5 × 10⁻⁶ m', 'they are laid in a straight line touching', 'How many cells would fit along a line 3 cm long?', 0.03 / 7.5e-6, 'cells'),
        ('the mass of the Earth is 5.97 × 10²⁴ kg', 'the mass of the Moon is 7.35 × 10²² kg', 'How many times heavier is the Earth than the Moon?', 5.97e24 / 7.35e22, 'times'),
        ('a hard drive stores 2 × 10¹² bytes', 'one photo uses 4.8 × 10⁶ bytes', 'How many photos can it store (to the nearest thousand)?', 2e12 / 4.8e6, 'photos'),
        ('a country of 6.8 × 10⁷ people uses 2.9 × 10¹¹ kWh of electricity a year', 'the population is assumed constant', 'Find the average use per person per day.', 2.9e11 / 6.8e7 / 365, 'kWh per day'),
    ])
    a, b, q, val, unit = ctx
    return dict(stem=f'Given that {a} and {b}: {q} Show your working (criterion D).', answer=f'{val:.3g} {unit}',
                markingKey=f'Correct operation set up in standard form (M1); index laws applied correctly (M1); answer {val:.3g} {unit} (A1); answer interpreted in context with units (C1).', marks=4)


R.facts('ch02-st4', F(
    terms=[('upper bound', 'the smallest value that a rounded measurement cannot reach or exceed – half a unit above the rounded value'),
           ('lower bound', 'the smallest value that would round up to the given measurement – half a unit below it'),
           ('limits of accuracy', 'the interval LB ≤ x < UB of true values that round to the stated measurement')],
    why=[('Explain why the upper bound of 7.3 cm (to 1 d.p.) is written with a strict inequality x < 7.35.', 'A length of exactly 7.35 rounds up to 7.4, so it is not included; every value just below 7.35 rounds to 7.3.'),
         ('Explain why the maximum value of a − b uses the upper bound of a and the lower bound of b.', 'To make a difference as big as possible you take the largest a and subtract the smallest possible b.')],
    misc=[('If a length is 20 cm to the nearest 10 cm, the bounds are 19.5 cm and 20.5 cm.', 'Half of the rounding unit (10 cm) is 5 cm, so the bounds are 15 cm ≤ L < 25 cm.'),
          ('The upper bound of a ÷ b is UB(a) ÷ UB(b).', 'To make a quotient largest, divide the largest numerator by the smallest denominator: UB(a) ÷ LB(b).')],
))


@R.add('ch02-st4', 'C3', (1, 3), 'short')
def bounds_basic(rng, slot):
    acc = rng.choice([('1 decimal place', 0.1, 1), ('the nearest whole number', 1, 0), ('the nearest 10', 10, 0), ('2 decimal places', 0.01, 2)])
    label, unit, dp = acc
    v = round(rng.uniform(2, 90) / unit) * unit
    lo, hi = v - unit / 2, v + unit / 2
    f = lambda z: f'{z:.{dp + 1}f}' if dp or unit < 1 else f'{z:g}'
    thing = rng.choice(['A rope is', 'A runner’s time is', 'The mass of a parcel is', 'A plank is'])
    u = {'A rope is': 'm', 'A runner’s time is': 's', 'The mass of a parcel is': 'kg', 'A plank is': 'cm'}[thing]
    vs = f'{v:.{dp}f}'
    return dict(stem=f'{thing} {vs} {u}, correct to {label}. Write down the limits of accuracy as an inequality.', answer=f'{f(lo)} ≤ x < {f(hi)}',
                markingKey=f'Half the unit is {unit / 2:g}; lower bound {f(lo)}, upper bound {f(hi)} (A1 each); correct inequality signs (A1).', marks=2)


@R.add('ch02-st4', 'C4', (3, 5), 'multi_step')
def bounds_calc(rng, slot):
    l, w = rng.randint(12, 40), rng.randint(5, 20)
    if slot.d >= 4:
        d_ = rng.randint(100, 400)
        t = rng.randint(10, 40)
        ub = (d_ + 0.5) / (t - 0.5)
        lb = (d_ - 0.5) / (t + 0.5)
        return dict(stem=f'{name(rng)} cycles {d_} m, to the nearest metre, in {t} s, to the nearest second. Find the upper and lower bounds of the average speed, and give the speed to a suitable degree of accuracy.',
                    answer=f'UB = {ub:.3f} m/s, LB = {lb:.3f} m/s', markingKey=f'UB = {d_ + 0.5}/{t - 0.5} = {ub:.4f} (M1 A1); LB = {d_ - 0.5}/{t + 0.5} = {lb:.4f} (M1 A1); both round to {round(ub, 0) if round(ub) == round(lb) else round(ub, 1)}… so a justified accuracy is the value where the bounds agree (R1).', marks=6)
    return dict(stem=f'A rectangle measures {l} cm by {w} cm, both to the nearest cm. Calculate the upper bound and lower bound of its area.',
                answer=f'UB {(l + .5) * (w + .5):g} cm², LB {(l - .5) * (w - .5):g} cm²',
                markingKey=f'UB = {l + .5} × {w + .5} = {(l + .5) * (w + .5):g} (M1 A1); LB = {l - .5} × {w - .5} = {(l - .5) * (w - .5):g} (A1).', marks=4)


@R.add('ch02-st4', 'C2', (2, 4), 'explain')
def bounds_explain(rng, slot):
    a, b = rng.randint(30, 80), rng.randint(5, 25)
    return dict(stem=f'Two lengths are a = {a} cm and b = {b} cm, each to the nearest cm. {name(rng)} says the maximum value of a − b is {a + 0.5} − {b + 0.5}. Explain the mistake and give the correct maximum.',
                answer=f'{a + 0.5 - (b - 0.5):g} cm', markingKey=f'To maximise a difference subtract the smallest b: UB(a) − LB(b) (R1) = {a + 0.5} − {b - 0.5} = {a + 0.5 - (b - 0.5):g} cm (A1).', type='explain', marks=2)


# =============================================================================================
# ch03 Algebraic Expressions: Expansion and Factorisation
# =============================================================================================
def _poly(e):
    return pe(sp.expand(e)).replace('-', '−')


def _rand_lin(rng, lo=1, hi=7, allow_neg=True):
    a = rng.randint(1, 3) if rng.random() < 0.4 else 1
    b = rng.choice([i for i in range(-hi, hi + 1) if i != 0]) if allow_neg else rng.randint(lo, hi)
    return a * x + b


R.facts('ch03-st1', F(
    terms=[('binomial', 'an algebraic expression with two terms, such as x + 5 or 2a − 3b'),
           ('expand', 'remove brackets by multiplying every term inside by the term(s) outside')],
    why=[('Explain why (x + 3)² is not equal to x² + 9.', '(x + 3)² = (x + 3)(x + 3) = x² + 3x + 3x + 9 = x² + 6x + 9; the two cross terms 6x are missing from x² + 9.'),
         ('Use an area diagram to explain why (a + b)(c + d) = ac + ad + bc + bd.', 'A rectangle with sides (a + b) and (c + d) splits into four smaller rectangles with areas ac, ad, bc and bd; their total equals the whole area.'),
         ('Explain why (x − y)(x + y) has no xy term.', 'The cross terms are +xy and −xy, which cancel, leaving x² − y².')],
    misc=[('(x − 5)² = x² − 25.', '(x − 5)² = x² − 10x + 25; x² − 25 is (x − 5)(x + 5).'),
          ('−2(x − 4) = −2x − 8.', '−2 × −4 = +8, so −2(x − 4) = −2x + 8.')],
))


@R.add('ch03-st1', 'C3', (1, 3), 'short')
def expand_pair(rng, slot):
    e1, e2 = _rand_lin(rng), _rand_lin(rng)
    if slot.d <= 1:
        k = rng.choice([2, 3, 4, 5, -2, -3])
        e = k * e1
        return dict(stem=f'Expand {m(k)}({_poly(e1)}).', answer=_poly(e), markingKey=f'{_poly(e)} (A1 each term).', marks=1)
    return dict(stem=f'Expand and simplify ({_poly(e1)})({_poly(e2)}).', answer=_poly(e1 * e2),
                markingKey=f'Four terms from FOIL/grid (M1); collect like terms: {_poly(e1 * e2)} (A1 A1).', marks=3 if slot.d >= 3 else 2)


@R.add('ch03-st1', 'C1', (1, 3), 'mcq')
def expand_sq_mcq(rng, slot):
    b = rng.choice([i for i in range(-9, 10) if i not in (0, 1, -1)])
    e = (x + b) ** 2
    correct = _poly(e)
    w = [_poly(x ** 2 + b * b), _poly(x ** 2 + b * x + b * b), _poly(x ** 2 + 2 * b * x - b * b)]
    return mcq(rng, f'Which expression is equivalent to ({_poly(x + b)})²?', correct, w, f'({_poly(x + b)})² = x² + 2({m(b)})x + {b * b} = {correct}.')


@R.add('ch03-st1', 'C3', (3, 5), 'short')
def expand_three(rng, slot):
    e1, e2, e3 = x + rng.choice([1, 2, 3, -1, -2]), x + rng.choice([2, 3, 4, -3]), x + rng.choice([1, -1, 5, -4])
    e = sp.expand(e1 * e2 * e3)
    return dict(stem=f'Expand and simplify ({_poly(e1)})({_poly(e2)})({_poly(e3)}) (Extended).', answer=_poly(e),
                markingKey=f'Expand two brackets first (M1), multiply by the third (M1), collect: {_poly(e)} (A1 A1).', marks=4)


@R.add('ch03-st1', 'C4', (3, 5), 'multi_step')
def expand_area(rng, slot):
    a, b = rng.randint(2, 6), rng.randint(1, 5)
    c = rng.randint(1, 3)
    outer = (x + a) * (x + b)
    inner = (x - c) * (x)
    area = sp.expand(outer - inner)
    return dict(stem=f'A rectangular garden measures (x + {a}) m by (x + {b}) m. A pond measuring x m by (x − {c}) m is dug inside it. Show that the remaining area is {_poly(area)} m², and find the area when x = {c + 4}.',
                answer=f'{_poly(area)}; {area.subs(x, c + 4)} m²', markingKey=f'Garden: {_poly(outer)} (M1 A1); pond: {_poly(inner)} (A1); subtract → {_poly(area)} (A1); substitute x = {c + 4}: {area.subs(x, c + 4)} m² (A1).', marks=5)


@R.add('ch03-st1', 'C2', (2, 4), 'explain')
def expand_identity(rng, slot):
    n = rng.randint(21, 99)
    k = rng.choice([1, 2])
    return dict(stem=f'Use the expansion of (a + b)² or (a − b)² to work out {n}² without a calculator. Explain which expansion you chose and why.',
                answer=str(n * n), markingKey=f'Choose a round number: {n}² = ({(n // 10) * 10 if n % 10 < 5 else (n // 10 + 1) * 10} {"+" if n % 10 < 5 else "−"} {n % 10 if n % 10 < 5 else 10 - n % 10})² (R1); expand correctly (M1); {n * n} (A1).', type='explain', marks=3)


R.facts('ch03-st2', F(
    terms=[('factorise', 'write an expression as a product of its factors – the reverse of expanding'),
           ('highest common factor (HCF)', 'the largest factor (number and variables) that divides every term')],
    why=[('Explain how you can check a factorisation.', 'Expand the factorised form; if it gives back the original expression the factorisation is correct.'),
         ('Explain why factorising by grouping needs the same bracket to appear twice.', 'After taking a factor out of each pair, the common bracket is itself a factor of the whole expression; if the brackets differ there is no common factor to take out.')],
    misc=[('6x² + 9x = 3(2x² + 3x) is fully factorised.', 'x is still common to both terms: 6x² + 9x = 3x(2x + 3).'),
          ('4a − 8 = 4(a − 8).', 'Dividing −8 by 4 gives −2: 4a − 8 = 4(a − 2).')],
))


@R.add('ch03-st2', 'C3', (1, 3), 'short')
def fact_common(rng, slot):
    k = rng.choice([2, 3, 4, 5, 6])
    a, b = rng.randint(1, 5), rng.choice([i for i in range(-9, 10) if i])
    p = rng.choice([1, 2]) if slot.d >= 2 else 0
    hcf = k * x ** p
    inner = a * x ** (1 if p else 1) + b if True else 0
    e = sp.expand(hcf * (a * x + b))
    return dict(stem=f'Factorise fully {_poly(e)}.', answer=f'{pe(hcf)}({_poly(a * x + b)})',
                markingKey=f'HCF {pe(hcf)} (M1); {pe(hcf)}({_poly(a * x + b)}) (A1). Partial factorisation scores M1 only.', marks=2)


@R.add('ch03-st2', 'C3', (2, 4), 'short')
def fact_group(rng, slot):
    a, b = rng.randint(1, 5), rng.choice([i for i in range(-6, 7) if i])
    c = rng.choice([2, 3, 4, 5, -2, -3])
    # (x + b)(a y + c) = a x y + c x + a b y + b c
    e = sp.expand((x + b) * (a * y + c))
    return dict(stem=f'Factorise by grouping: {_poly(e)}.', answer=f'({_poly(x + b)})({_poly(a * y + c)})',
                markingKey=f'Group in pairs and factor each (M1); common bracket taken out (M1); ({_poly(x + b)})({_poly(a * y + c)}) (A1).', marks=3)


@R.add('ch03-st2', 'C4', (3, 5), 'multi_step')
def fact_numeric(rng, slot):
    a, b, c = rng.randint(11, 49), rng.randint(51, 99), rng.randint(2, 9)
    return dict(stem=f'Use factorisation to evaluate {c} × {a} + {c} × {b} − {c} × {a + b - 100} without a calculator, explaining each step (criterion C).',
                answer=str(c * 100), markingKey=f'Take out the common factor {c}: {c}({a} + {b} − {a + b - 100}) (M1) = {c} × 100 (A1) = {c * 100} (A1). Clear statement of the method (C1).', marks=4)


@R.add('ch03-st2', 'C2', (2, 4), 'explain')
def fact_check(rng, slot):
    k = rng.choice([2, 3, 4, 5])
    a, b = rng.randint(2, 6), rng.randint(1, 9)
    e = sp.expand(k * x * (a * x + b))
    wrong = f'{k}({a}x² + {b}x)'
    return dict(stem=f'{name(rng)} factorised {_poly(e)} as {wrong}. Explain why this is not fully factorised and give the full factorisation.',
                answer=f'{k}x({a}x + {b})', markingKey=f'x is a common factor of both terms in the bracket (R1); full answer {k}x({a}x + {b}) (A1).', type='explain', marks=2)


R.facts('ch03-st3', F(
    terms=[('quadratic trinomial', 'an expression of the form ax² + bx + c with three terms')],
    why=[('Explain how the numbers p and q are chosen when factorising x² + bx + c as (x + p)(x + q).', 'Expanding gives x² + (p + q)x + pq, so p and q must add to b and multiply to c.'),
         ('Explain why x² + 5x + 6 and x² − 5x + 6 have factors with different signs.', 'Both need a product of +6, so p and q have the same sign; the sum +5 needs both positive (2, 3), the sum −5 needs both negative (−2, −3).'),
         ('Explain why x² + x + 1 cannot be factorised over the integers.', 'No two integers multiply to 1 and add to 1 (only 1 × 1 or −1 × −1, which add to ±2).')],
    misc=[('x² − x − 12 = (x − 4)(x − 3).', '(x − 4)(x − 3) = x² − 7x + 12. Need product −12 and sum −1: (x − 4)(x + 3).'),
          ('2x² + 7x + 3 = (2x + 3)(x + 1).', '(2x + 3)(x + 1) = 2x² + 5x + 3. Correct: (2x + 1)(x + 3).')],
))


def _quad_from_roots(rng, lead=False):
    p = rng.choice([i for i in range(-9, 10) if i])
    q = rng.choice([i for i in range(-9, 10) if i and i != -p])
    a = rng.choice([2, 3]) if lead else 1
    return (a * x + p) * (x + q), a, p, q


@R.add('ch03-st3', 'C3', (1, 3), 'short')
def fact_quad(rng, slot):
    e, a, p, q = _quad_from_roots(rng, lead=False)
    return dict(stem=f'Factorise {_poly(e)}.', answer=f'({_poly(x + p)})({_poly(x + q)})',
                markingKey=f'Two numbers with product {p * q} and sum {p + q}: {m(p)} and {m(q)} (M1); ({_poly(x + p)})({_poly(x + q)}) (A1).', marks=2)


@R.add('ch03-st3', 'C3', (3, 5), 'short')
def fact_quad_a(rng, slot):
    e, a, p, q = _quad_from_roots(rng, lead=True)
    if sp.gcd(a * x + p, a) != 1:
        return None
    return dict(stem=f'Factorise {_poly(e)} (Extended).', answer=f'({_poly(a * x + p)})({_poly(x + q)})',
                markingKey=f'ac = {a * p * q}: split the middle term using two numbers with product {a * p * q} and sum {a * q + p} (M1); group (M1); ({_poly(a * x + p)})({_poly(x + q)}) (A1).', marks=3)


@R.add('ch03-st3', 'C1', (1, 3), 'mcq')
def fact_quad_mcq(rng, slot):
    e, a, p, q = _quad_from_roots(rng)
    correct = f'({_poly(x + p)})({_poly(x + q)})'
    w = [f'({_poly(x - p)})({_poly(x - q)})', f'({_poly(x + p)})({_poly(x - q)})', f'({_poly(x + p * q)})({_poly(x + 1)})']
    return mcq(rng, f'Which is the correct factorisation of {_poly(e)}?', correct, w, f'{m(p)} × {m(q)} = {p * q} and {m(p)} + {m(q)} = {p + q}.')


@R.add('ch03-st3', 'C4', (3, 5), 'multi_step')
def fact_quad_context(rng, slot):
    p, q = rng.randint(2, 9), rng.randint(2, 9)
    e = sp.expand((x + p) * (x + q))
    return dict(stem=f'The area of a rectangular tile is ({_poly(e)}) cm², where x > 0. (a) Factorise the expression to find possible expressions for the length and width. (b) Find the perimeter in terms of x. (c) Find the tile’s area and perimeter when x = 5.',
                answer=f'(x + {p})(x + {q}); perimeter {_poly(2 * (2 * x + p + q))} cm; area {e.subs(x, 5)} cm², perimeter {2 * (10 + p + q)} cm',
                markingKey=f'(a) (x + {p})(x + {q}) (M1 A1). (b) 2(x + {p} + x + {q}) = {_poly(2 * (2 * x + p + q))} (A1). (c) area {e.subs(x, 5)} cm² and perimeter {2 * (10 + p + q)} cm (A1 A1).', marks=5)


@R.add('ch03-st3', 'C2', (2, 4), 'explain')
def fact_quad_why(rng, slot):
    e, a, p, q = _quad_from_roots(rng)
    return dict(stem=f'Explain how you know, before factorising, whether the two numbers in the brackets of {_poly(e)} have the same sign or opposite signs. Then factorise it.',
                answer=f'({_poly(x + p)})({_poly(x + q)})', markingKey=f'The constant term {p * q} is {"positive, so same signs" if p * q > 0 else "negative, so opposite signs"} (R1); the sign of the x-coefficient {p + q} then decides which is larger/both signs (R1); ({_poly(x + p)})({_poly(x + q)}) (A1).', type='explain', marks=3)


R.facts('ch03-st4', F(
    terms=[('difference of two squares', 'an expression a² − b², which factorises as (a − b)(a + b)'),
           ('perfect square trinomial', 'an expression a² ± 2ab + b² that factorises as (a ± b)²')],
    why=[('Explain why x² + 9 is not a difference of two squares.', 'It is a sum, not a difference; (x + 3)(x − 3) = x² − 9, and x² + 9 has no real linear factors.'),
         ('Explain how to recognise that x² − 14x + 49 is a perfect square.', 'The first and last terms are squares (x², 7²) and the middle term is −2 × x × 7 = −14x, so it equals (x − 7)².')],
    misc=[('x² − 16 = (x − 4)².', '(x − 4)² = x² − 8x + 16. Correct: x² − 16 = (x − 4)(x + 4).'),
          ('4x² − 9 = (4x − 9)(4x + 9).', '4x² = (2x)² and 9 = 3², so 4x² − 9 = (2x − 3)(2x + 3).')],
))


@R.add('ch03-st4', 'C3', (1, 3), 'short')
def dots(rng, slot):
    a, b = rng.randint(1, 5), rng.randint(1, 12)
    if slot.d >= 3:
        k = rng.choice([2, 3, 5])
        e = k * (a * a * x ** 2 - b * b)
        return dict(stem=f'Factorise fully {_poly(e)}.', answer=f'{k}({_poly(a * x - b)})({_poly(a * x + b)})',
                    markingKey=f'Common factor {k} first (M1); then difference of two squares (M1); {k}({_poly(a * x - b)})({_poly(a * x + b)}) (A1).', marks=3)
    e = a * a * x ** 2 - b * b
    return dict(stem=f'Factorise {_poly(e)}.', answer=f'({_poly(a * x - b)})({_poly(a * x + b)})',
                markingKey=f'{pe(a * x)}² − {b}² (M1) = ({_poly(a * x - b)})({_poly(a * x + b)}) (A1).', marks=2)


@R.add('ch03-st4', 'C3', (2, 4), 'numerical')
def dots_numeric(rng, slot):
    a = rng.randint(51, 99)
    b = rng.randint(11, a - 20)
    return dict(stem=f'Use the difference of two squares to calculate {a}² − {b}² without a calculator.', answer=str(a * a - b * b),
                markingKey=f'({a} − {b})({a} + {b}) (M1) = {a - b} × {a + b} (A1) = {a * a - b * b} (A1).', type='numerical', marks=3)


@R.add('ch03-st4', 'C4', (3, 5), 'multi_step')
def dots_proof(rng, slot):
    return rng.choice([
        dict(stem='Prove that the difference between the squares of two consecutive odd numbers is always a multiple of 8.', answer='(2n + 1)² − (2n − 1)² = 8n',
             markingKey='Let the numbers be 2n − 1 and 2n + 1 (M1); difference of squares: (2n + 1 − (2n − 1))(2n + 1 + 2n − 1) = 2 × 4n (M1) = 8n (A1); conclusion stated: a multiple of 8 for all integers n (R1).', marks=4),
        dict(stem='Prove that the difference between the squares of any two consecutive integers is equal to their sum.', answer='(n + 1)² − n² = 2n + 1 = n + (n + 1)',
             markingKey='Let them be n and n + 1 (M1); (n + 1)² − n² = (n + 1 − n)(n + 1 + n) (M1) = 2n + 1 (A1) = n + (n + 1), their sum (R1).', marks=4),
        dict(stem='Show that 2¹⁶ − 1 is divisible by 255 by factorising it as a difference of two squares.', answer='2¹⁶ − 1 = (2⁸ − 1)(2⁸ + 1) = 255 × 257',
             markingKey='2¹⁶ − 1 = (2⁸)² − 1² (M1) = (2⁸ − 1)(2⁸ + 1) (M1) = 255 × 257 (A1); so 255 is a factor (R1).', marks=4),
        dict(stem='Prove that n³ − n is always divisible by 6 for any integer n.', answer='n³ − n = (n − 1)n(n + 1)',
             markingKey='n(n² − 1) = (n − 1)n(n + 1) (M1 A1); three consecutive integers contain a multiple of 2 and a multiple of 3 (R1), so the product is divisible by 6 (R1).', marks=4),
        dict(stem='A square of side a cm has a square of side b cm cut from one corner. By cutting and rearranging the remaining L-shape into a rectangle, show that a² − b² = (a − b)(a + b).', answer='The L-shape rearranges to a rectangle (a + b) by (a − b).',
             markingKey='Area of L-shape a² − b² (A1); cut along the extension of the inner edge into two rectangles a × (a − b) and b × (a − b) (M1); place them end to end: (a + b) × (a − b) (A1); conclusion (R1).', marks=4),
    ])


@R.add('ch03-st4', 'C1', (1, 2), 'mcq')
def dots_mcq(rng, slot):
    b = rng.randint(2, 11)
    a = rng.choice([1, 2, 3])
    e = a * a * x ** 2 - b * b
    correct = f'({_poly(a * x - b)})({_poly(a * x + b)})'
    w = [f'({_poly(a * x - b)})²', f'({_poly(a * x + b)})²', f'({_poly(a * x - b * b)})({_poly(x + 1)})']
    return mcq(rng, f'Which is a correct factorisation of {_poly(e)}?', correct, w, f'{_poly(e)} is a difference of two squares.')


R.facts('ch03-st5', F(
    terms=[('algebraic fraction', 'a fraction whose numerator and/or denominator contains algebraic expressions')],
    why=[('Explain why (x + 3)/3 cannot be simplified to x.', 'The 3 in the numerator is a term, not a factor; only common factors of the whole numerator and denominator may be cancelled.'),
         ('Explain why you should factorise before cancelling in an algebraic fraction.', 'Cancelling is dividing top and bottom by a common factor, so the factors must be visible; factorising reveals them.')],
    misc=[('(x² + 5x)/x = x² + 5.', 'Divide every term by x, or factorise: x(x + 5)/x = x + 5.'),
          ('1/x + 1/y = 2/(x + y).', 'Use a common denominator: 1/x + 1/y = (y + x)/(xy).')],
))


@R.add('ch03-st5', 'C3', (2, 4), 'short')
def algfrac_simplify(rng, slot):
    p, q, r_ = rng.choice([i for i in range(-7, 8) if i]), rng.choice([i for i in range(-7, 8) if i]), rng.choice([i for i in range(-7, 8) if i])
    if len({p, q, r_}) < 3:
        return None
    num = sp.expand((x + p) * (x + q))
    den = sp.expand((x + p) * (x + r_))
    return dict(stem=f'Simplify ({_poly(num)}) / ({_poly(den)}).', answer=f'({_poly(x + q)})/({_poly(x + r_)})',
                markingKey=f'Factorise numerator (x + {p})(x + {q}) and denominator (x + {p})(x + {r_}) (M1 M1); cancel (x + {p}): ({_poly(x + q)})/({_poly(x + r_)}) (A1).'.replace('+ -', '− '), marks=3)


@R.add('ch03-st5', 'C3', (1, 3), 'short')
def algfrac_add(rng, slot):
    a, b = rng.randint(2, 6), rng.randint(2, 6)
    if a == b:
        return None
    c, d_ = rng.randint(1, 5), rng.randint(1, 5)
    # (x + c)/a + (x − d)/b = (b(x+c) + a(x−d))/(ab)
    num = sp.expand(b * (x + c) + a * (x - d_))
    return dict(stem=f'Write as a single fraction: (x + {c})/{a} + (x − {d_})/{b}.', answer=f'({_poly(num)})/{a * b}',
                markingKey=f'Common denominator {a * b} (M1); numerator {b}(x + {c}) + {a}(x − {d_}) (M1) = {_poly(num)} (A1).', marks=3)


@R.add('ch03-st5', 'C4', (3, 5), 'multi_step')
def algfrac_hard(rng, slot):
    a = rng.randint(1, 6)
    b = rng.choice([i for i in range(1, 7) if i != a])
    # 1/(x − a) − 1/(x − b) = (a − b)/((x − a)(x − b))  -> simplified
    num = a - b
    den = sp.expand((x - a) * (x - b))
    return dict(stem=f'Show that 1/(x − {a}) − 1/(x − {b}) can be written as k/({_poly(den)}), and find k.', answer=f'k = {m(num)}',
                markingKey=f'Common denominator (x − {a})(x − {b}) = {_poly(den)} (M1 A1); numerator (x − {b}) − (x − {a}) = {m(num)} (M1 A1).', marks=4, gap='G5')


@R.add('ch03-st5', 'C2', (2, 4), 'explain')
def algfrac_cancel(rng, slot):
    a = rng.randint(2, 9)
    return dict(stem=f'{name(rng)} simplifies (x + {a})/({a}x) to 1/x by cancelling the {a}s. Explain why this is wrong, and test it with x = 1.',
                answer=f'Not equal: at x = 1, ({1 + a})/{a} ≠ 1', markingKey=f'{a} is a term in the numerator, not a factor, so it cannot cancel (R1); x = 1 gives {1 + a}/{a} on the left but 1 on the right (A1).', type='explain', marks=2)


# ---- top-ups for chapters 2-3 -----------------------------------------------------------------
@R.add('ch02-st3', 'C2', (2, 4), 'explain')
def sf_compare(rng, slot):
    a, b = rng.randint(11, 95) / 10, rng.randint(11, 95) / 10
    p = rng.randint(-8, 9)
    q = p - rng.randint(1, 3)
    va, vb = a * 10 ** p, b * 10 ** q
    big, small = (f'{a} × 10{sup(p)}', f'{b} × 10{sup(q)}') if va > vb else (f'{b} × 10{sup(q)}', f'{a} × 10{sup(p)}')
    ratio = max(va, vb) / min(va, vb)
    frame = rng.choice(['Without a calculator, explain which number is larger', 'Decide, with a reason, which of these quantities is greater', 'Compare the two numbers below and justify which is bigger'])
    return dict(stem=f'{frame}: {a} × 10{sup(p)} or {b} × 10{sup(q)}. By roughly what factor is it larger?', answer=f'{big}, about {ratio:.2g} times larger',
                markingKey=f'Compare powers of ten first, then the front numbers if needed (R1); {big} is larger (A1); factor ≈ {ratio:.2g} (A1).', type='explain', marks=3)


@R.add('ch02-st3', 'C4', (3, 5), 'multi_step')
def sf_context2(rng, slot):
    who = name(rng)
    k = rng.choice([
        (f'A virus particle is 1.2 × 10⁻⁷ m long and a dust mite is 2.5 × 10⁻⁴ m long.', 'How many times longer is the dust mite? Give your answer in standard form.', 2.5e-4 / 1.2e-7, ''),
        (f'{who}’s school uses 4.6 × 10⁵ sheets of paper a year. Each sheet is 1.0 × 10⁻⁴ m thick.', 'How tall, in metres, would the stack of one year’s paper be?', 4.6e5 * 1e-4, 'm'),
        (f'A streaming service has 2.3 × 10⁸ subscribers paying US$ 1.5 × 10¹ each per month.', 'Find the monthly revenue in standard form.', 2.3e8 * 15, 'US$'),
        (f'The Amazon river discharges about 2.09 × 10⁵ m³ of water every second.', 'How much water is discharged in one day? Give your answer in standard form.', 2.09e5 * 86400, 'm³'),
        (f'A bacterium has a mass of 9.5 × 10⁻¹⁶ kg. A sample contains 3.2 × 10¹¹ bacteria.', 'Find the total mass of the sample in kg.', 9.5e-16 * 3.2e11, 'kg'),
        (f'Mount Everest is 8.849 × 10³ m tall and the Mariana Trench is 1.0994 × 10⁴ m deep.', 'Find the vertical distance from the top of Everest to the bottom of the trench in standard form.', 8849 + 10994, 'm'),
        (f'A grain of rice has a mass of about 2.9 × 10⁻⁵ kg. {who}’s family eats 6 kg of rice a month.', 'Estimate how many grains they eat in a year.', 6 * 12 / 2.9e-5, 'grains'),
        (f'The International Space Station orbits at 7.66 × 10³ m/s.', 'How far does it travel in one 92-minute orbit? Give your answer in km in standard form.', 7.66e3 * 92 * 60 / 1000, 'km'),
    ])
    ctx, q, val, unit = k
    return dict(stem=f'{ctx} {q}', answer=f'{sci_txt(val)} {unit}'.strip(),
                markingKey=f'Correct operation chosen (M1); indices handled correctly (M1); {sci_txt(val)} {unit} (A1); sensible rounding/units stated (C1).', marks=4)


def sci_txt(v):
    e = math.floor(math.log10(abs(v)))
    return f'{v / 10 ** e:.3g} × 10{sup(e)}'


@R.add('ch03-st3', 'C4', (3, 5), 'multi_step')
def fact_quad_problem(rng, slot):
    p, q = rng.randint(1, 8), rng.randint(1, 8)
    if p == q:
        return None
    e = sp.expand((x + p) * (x + q))
    frames = [
        f'The product of two numbers is {_poly(e)}, where each number is of the form x + k for integer k. Find the two numbers and their sum in terms of x.',
        f'A photo frame has area ({_poly(e)}) cm². Its width is (x + {min(p, q)}) cm. Find its length and show that the difference between length and width is constant.',
        f'Show that {_poly(e)} − {p * q} can be factorised, and fully factorise both {_poly(e)} and {_poly(e - p * q)}.',
        f'{name(rng)} says that {_poly(e)} is never zero for positive x. Factorise the expression and use the factors to decide whether the claim is true.',
        f'Find the value of {_poly(e)} when x = 98 by factorising first and explain why this is quicker than substituting directly.',
    ]
    i = rng.randrange(len(frames))
    ans = [f'x + {p} and x + {q}; sum {_poly(2 * x + p + q)}', f'length x + {max(p, q)} cm; difference {abs(p - q)} cm', f'{_poly(e)} = (x + {p})(x + {q}); {_poly(e - p * q)} = x(x + {p + q})',
           f'(x + {p})(x + {q}) has both factors > 0 for x > 0, so true', f'(98 + {p})(98 + {q}) = {(98 + p) * (98 + q)}'][i]
    return dict(stem=frames[i], answer=ans, markingKey=f'Correct factorisation (x + {p})(x + {q}) (M1 A1); used to answer the question: {ans} (A1); reasoning communicated clearly (C1).', marks=4)


@R.add('ch03-st4', 'C2', (2, 4), 'explain')
def dots_explain(rng, slot):
    a = rng.randint(2, 12)
    k = rng.choice([2, 3, 4, 5])
    frames = [
        (f'Explain why x² − {a * a} factorises but x² + {a * a} does not (over the real numbers).', f'x² − {a * a} = (x − {a})(x + {a}); x² + {a * a} > 0 for all x so it has no real roots and no real linear factors.'),
        (f'Explain how you can tell that {k * k}x² − {a * a} is a difference of two squares, and factorise it.', f'Both terms are squares, ({k}x)² and {a}², and they are subtracted: ({k}x − {a})({k}x + {a}).'),
        (f'Is x² − {2 * a}x + {a * a} a perfect square? Explain how you know.', f'Yes: x² and {a * a} = {a}² are squares and the middle term is −2·x·{a}, so it is (x − {a})².'),
        (f'Explain why x² + {a}x + {a * a} is not a perfect square trinomial.', f'A perfect square would need middle term ±2·{a}·x = ±{2 * a}x, not {a}x.'),
    ]
    q, ans = rng.choice(frames)
    return dict(stem=q, answer=ans, markingKey=f'{ans} R1 for the recognition criterion, A1 for the result.', type='explain', marks=2)


@R.add('ch03-st4', 'C4', (3, 5), 'multi_step')
def dots_context(rng, slot):
    big, small = rng.randint(12, 30), rng.randint(3, 10)
    who = name(rng)
    frames = [
        (f'A square courtyard of side {big} m has a square fountain of side {small} m in the middle. {who} wants the paved area. Use the difference of two squares to find it without squaring {big}.', f'({big} − {small})({big} + {small}) = {(big - small) * (big + small)} m²'),
        (f'A square tile of side (x + {small}) cm has a square hole of side (x − {small}) cm. Show that the remaining area is a multiple of x and find it when x = {big}.', f'{4 * small}x cm²; {4 * small * big} cm²'),
        (f'Two square plots have sides {big} m and {small} m. {who} claims the difference in their areas equals the product of the sum and difference of their sides. Verify this and explain why it always works.', f'{big * big - small * small} = ({big} + {small})({big} − {small}); a² − b² = (a − b)(a + b)'),
    ]
    q, ans = rng.choice(frames)
    return dict(stem=q, answer=ans, markingKey=f'Recognise a² − b² (M1); factorised form used (M1); {ans} (A1); justification/units (C1).', marks=4)


# =============================================================================================
# ch04 Linear Equations, Inequalities and Simultaneous Equations
# =============================================================================================
R.facts('ch04-st1', F(
    terms=[('linear equation', 'an equation in which the unknown appears only to the power 1, such as 3x − 5 = 10'),
           ('inverse operation', 'the operation that undoes another, used on both sides to isolate the unknown')],
    why=[('Explain why you must do the same operation to both sides of an equation.', 'An equation states that two expressions are equal; changing both by the same operation keeps them equal, so the solution set is unchanged.'),
         ('Explain why multiplying both sides by the LCM of the denominators is a good first step for an equation with fractions.', 'It clears every fraction at once, turning the equation into an equivalent one with integer coefficients that is easier to solve.'),
         ('Explain how substituting your answer back into the original equation checks the solution.', 'If both sides give the same value, the number satisfies the equation; any slip in the working would usually make the sides unequal.')],
    misc=[('To solve x/3 + 2 = 5 you multiply only x/3 by 3 to get x + 2 = 5.', 'Every term must be multiplied: x + 6 = 15, so x = 9.'),
          ('From 4 − 2x = 10 we get 2x = 6 so x = 3.', 'Subtracting 4: −2x = 6, so x = −3. The sign of 2x was lost.')],
))


@R.add('ch04-st1', 'C3', (1, 3), 'short')
def lin_solve(rng, slot):
    sol = rng.randint(-9, 12)
    a, c = rng.randint(2, 9), rng.randint(1, 5)
    if slot.d <= 1:
        b = rng.randint(-15, 15)
        return dict(stem=f'Solve {_lin(a, b)} = {m(a * sol + b)}.', answer=f'x = {m(sol)}',
                    markingKey=f'{a}x = {m(a * sol)} (M1); x = {m(sol)} (A1).', marks=2)
    if a == c:
        return None
    b = rng.randint(-12, 12)
    d_ = a * sol + b - c * sol
    return dict(stem=f'Solve {_lin(a, b)} = {_lin(c, d_)}.', answer=f'x = {m(sol)}',
                markingKey=f'Collect x terms: {a - c}x = {m(d_ - b)} (M1 A1); x = {m(sol)} (A1).', marks=3)


@R.add('ch04-st1', 'C3', (3, 5), 'short')
def lin_frac(rng, slot):
    p, q = rng.choice([(2, 3), (3, 4), (2, 5), (4, 3), (5, 2), (3, 5)])
    sol = rng.randint(-6, 12)
    a, b = rng.randint(1, 4), rng.randint(-5, 6)
    c, d_ = rng.randint(1, 3), rng.randint(-5, 6)
    lhs = Fr(a * sol + b, p) - Fr(c * sol + d_, q)
    if lhs.denominator != 1:
        return None
    return dict(stem=f'Solve ({_lin(a, b)})/{p} − ({_lin(c, d_)})/{q} = {m(lhs.numerator)}.', answer=f'x = {m(sol)}',
                markingKey=f'Multiply every term by {p * q // math.gcd(p, q)} (M1); expand brackets with correct signs (M1); collect and solve x = {m(sol)} (A1 A1).', marks=4)


@R.add('ch04-st1', 'C4', (3, 5), 'multi_step')
def lin_context(rng, slot):
    who = name(rng)
    k = rng.randint(3, 9)
    frames = [
        (lambda: (lambda w: (f'The length of a rectangle is {k} cm more than twice its width. Its perimeter is {2 * (2 * w + k + w)} cm. Form and solve an equation to find its width and length.', f'width {w} cm, length {2 * w + k} cm'))(rng.randint(4, 15))),
        (lambda: (lambda a_: (f'{who} is {k} years older than her brother. In 5 years the sum of their ages will be {2 * a_ + k + 10}. Form an equation and find their current ages.', f'brother {a_}, {who} {a_ + k}'))(rng.randint(6, 20))),
        (lambda: (lambda n: (f'Three consecutive even numbers add up to {3 * n + 6}. Form and solve an equation to find them.', f'{n}, {n + 2}, {n + 4}'))(2 * rng.randint(5, 40))),
        (lambda: (lambda h: (f'A taxi charges a fixed fee of €{k} plus €1.80 per km. {who} paid €{k + 1.8 * h:.2f}. Write and solve an equation to find the distance travelled.', f'{h} km'))(rng.randint(4, 25))),
        (lambda: (lambda s: (f'The angles of a triangle are x°, (2x + {k})° and (3x − {k + 6})°. Find each angle.', f'{s}°, {2 * s + k}°, {3 * s - k - 6}°'))((180 + 6) // 6) if (180 + 6) % 6 == 0 else None),
    ]
    r = rng.choice(frames)()
    if not r:
        return None
    q, ans = r
    return dict(stem=q, answer=ans, markingKey=f'Correct equation formed (M1 A1); solved correctly (M1); answer in context: {ans} (A1); check against the conditions (C1).', marks=5)


R.facts('ch04-st2', F(
    terms=[('subject of a formula', 'the variable that stands alone on one side of the formula, e.g. v in v = u + at')],
    why=[('Explain why changing the subject of a formula uses the same steps as solving an equation.', 'Both apply inverse operations to both sides in the reverse order to the operations acting on the required letter.'),
         ('Explain why making r the subject of A = πr² gives r = √(A/π) and not r = A/π².', 'Undo the operations in reverse: divide by π first, then undo squaring by taking the square root of A/π.')],
    misc=[('If v = u + at, then t = v − u/a.', 'Subtract u first, then divide the whole of (v − u) by a: t = (v − u)/a.'),
          ('From y = 3x − 2, x = y/3 − 2.', 'Add 2 before dividing: x = (y + 2)/3.')],
))


@R.add('ch04-st2', 'C3', (1, 4), 'short')
def subj(rng, slot):
    forms = [
        ('v = u + at', 't', 't = (v − u)/a', 2),
        ('A = ½(a + b)h', 'h', 'h = 2A/(a + b)', 2),
        ('P = 2(l + w)', 'w', 'w = P/2 − l', 2),
        ('s = ut + ½at²', 'a', 'a = 2(s − ut)/t²', 3),
        ('V = πr²h', 'r', 'r = √(V/(πh))', 3),
        ('F = 9C/5 + 32', 'C', 'C = 5(F − 32)/9', 2),
        ('E = ½mv²', 'v', 'v = √(2E/m)', 3),
        ('y = (2x + 3)/(x − 1)', 'x', 'x = (y + 3)/(y − 2)', 4),
        ('T = 2π√(l/g)', 'l', 'l = gT²/(4π²)', 4),
        ('1/f = 1/u + 1/v', 'v', 'v = uf/(u − f)', 4),
        ('A = P(1 + r/100)', 'r', 'r = 100(A − P)/P', 3),
        ('k = (a − b)/c', 'b', 'b = a − kc', 2),
    ]
    lo = {1: 2, 2: 2, 3: 3, 4: 4, 5: 4}[slot.d]
    pool = [f_ for f_ in forms if (f_[3] == lo or (slot.d >= 4 and f_[3] >= 3))]
    fml, v, ans, mk = rng.choice(pool)
    return dict(stem=f'Make {v} the subject of the formula {fml}.', answer=ans,
                markingKey=f'Inverse operations in the correct order (M1 for each correct step); {ans} (A1).', marks=mk)


@R.add('ch04-st2', 'C4', (3, 5), 'multi_step')
def subj_use(rng, slot):
    u, a_, t = rng.randint(2, 15), rng.randint(2, 6), rng.randint(3, 12)
    v = u + a_ * t
    l = rng.choice([0.5, 1.0, 1.5, 2.0])
    frames = [
        (f'The formula v = u + at gives the final speed of a cyclist. (a) Make a the subject. (b) Find a when u = {u} m/s, v = {v} m/s and t = {t} s.', f'a = (v − u)/t; a = {a_} m/s²'),
        (f'The time for one swing of a pendulum is T = 2π√(l/g). (a) Rearrange to make l the subject. (b) Find l when T = {2 * math.pi * math.sqrt(l / 9.8):.3f} s and g = 9.8 m/s².', f'l = gT²/(4π²); l ≈ {l} m'),
        (f'The area of a trapezium is A = ½(a + b)h. A garden bed has area {(u + v) * t / 2} m² with parallel sides {u} m and {v} m. Rearrange and find h.', f'h = 2A/(a + b) = {t} m'),
    ]
    q, ans = rng.choice(frames)
    return dict(stem=q, answer=ans, markingKey=f'Correct rearrangement (M1 A1); substitution (M1); {ans} (A1).', marks=4)


@R.add('ch04-st2', 'C2', (2, 4), 'explain')
def subj_explain(rng, slot):
    k = rng.randint(2, 9)
    frames = [
        (f'{name(rng)} rearranges y = {k}(x − 3) to make x the subject and writes x = y/{k} − 3. Explain the error and correct it.', f'Divide by {k} first, then add 3: x = y/{k} + 3.'),
        (f'Explain why the formula A = πr² can be rearranged to give r but the answer has two possible signs only before considering the context.', 'Taking a square root gives ±√(A/π); a radius is a length so the negative value is rejected.'),
        (f'Explain the order of steps you would use to make x the subject of y = (x + {k})² − 1.', f'Add 1, square root (±), then subtract {k}: x = −{k} ± √(y + 1).'),
    ]
    q, ans = rng.choice(frames)
    return dict(stem=q, answer=ans, markingKey=f'{ans} (R1 for the reason, A1 for the corrected result)', type='explain', marks=2)


R.facts('ch04-st3', F(
    terms=[('inequality', 'a statement that one quantity is greater than (>), less than (<), at least (≥) or at most (≤) another'),
           ('interval notation', 'a way of writing a set of numbers between two end points, using [ ] for included and ( ) for excluded end points')],
    why=[('Explain why the inequality sign reverses when you multiply or divide by a negative number.', 'Multiplying by −1 reflects numbers in zero on the number line, which reverses their order: 2 < 5 but −2 > −5.'),
         ('Explain the difference between an open and a closed circle on a number line.', 'A closed circle means the end value is included (≤ or ≥); an open circle means it is excluded (< or >).')],
    misc=[('From −3x < 12 we get x < −4.', 'Dividing by −3 reverses the sign: x > −4.'),
          ('x ≥ 2 in interval notation is (2, ∞).', '2 is included, so the bracket is square: [2, ∞).')],
))


@R.add('ch04-st3', 'C3', (1, 4), 'short')
def ineq_solve(rng, slot):
    a = rng.choice([-5, -4, -3, -2, 2, 3, 4, 5])
    sol = rng.randint(-6, 8)
    b = rng.randint(-10, 10)
    sign = rng.choice(['<', '>', '≤', '≥'])
    rev = {'<': '>', '>': '<', '≤': '≥', '≥': '≤'}
    res_sign = sign if a > 0 else rev[sign]
    br = {'<': ')', '≤': ']'}
    interval = f'(−∞, {m(sol)}{")" if res_sign == "<" else "]"}' if res_sign in '<≤' else f'{"(" if res_sign == ">" else "["}{m(sol)}, ∞)'
    if slot.d >= 3:
        c = rng.randint(1, 4)
        if c == a:
            return None
        d_ = (a - c) * sol + b
        res_sign2 = sign if a - c > 0 else rev[sign]
        if a - c == 0:
            return None
        interval = f'(−∞, {m(sol)}{")" if res_sign2 == "<" else "]"}' if res_sign2 in '<≤' else f'{"(" if res_sign2 == ">" else "["}{m(sol)}, ∞)'
        return dict(stem=f'Solve {_lin(a, b)} {sign} {_lin(c, -d_ + b + 0) if False else _lin(c, b - d_ + (a - c) * sol - (a - c) * sol)} and write the solution in interval notation.'.replace('+ 0', ''),
                    answer=f'x {res_sign2} {m(sol)}; {interval}', markingKey=f'Collect x terms: {a - c}x {sign} {m(d_ - b) if False else m((a - c) * sol)} (M1); divide by {a - c}{", reversing the sign" if a - c < 0 else ""} (M1); x {res_sign2} {m(sol)} and {interval} (A1 A1).', marks=4)
    return dict(stem=f'Solve {_lin(a, b)} {sign} {m(a * sol + b)} and show the solution on a number line.', answer=f'x {res_sign} {m(sol)}',
                markingKey=f'{a}x {sign} {m(a * sol)} (M1); x {res_sign} {m(sol)}{" – sign reversed because dividing by a negative" if a < 0 else ""} (A1); number line with {"closed" if res_sign in "≤≥" else "open"} circle at {m(sol)} (A1).', marks=3)


@R.add('ch04-st3', 'C1', (1, 3), 'mcq')
def ineq_interval_mcq(rng, slot):
    a, b = sorted(rng.sample(range(-8, 10), 2))
    kinds = [(f'{m(a)} ≤ x < {m(b)}', f'[{m(a)}, {m(b)})'), (f'{m(a)} < x ≤ {m(b)}', f'({m(a)}, {m(b)}]'), (f'{m(a)} < x < {m(b)}', f'({m(a)}, {m(b)})'), (f'{m(a)} ≤ x ≤ {m(b)}', f'[{m(a)}, {m(b)}]')]
    i = rng.randrange(4)
    ineq, correct = kinds[i]
    w = [k[1] for j, k in enumerate(kinds) if j != i]
    return mcq(rng, f'Which interval represents {ineq}?', correct, w, 'Square brackets include an end point; round brackets exclude it.')


@R.add('ch04-st3', 'C4', (3, 5), 'multi_step')
def ineq_context(rng, slot):
    who = name(rng)
    fee, per = rng.randint(20, 60), rng.choice([4, 5, 6, 7.5, 8])
    budget = fee + per * rng.randint(6, 20) + rng.randint(1, int(per) - 1 if per > 2 else 1)
    n = int((budget - fee) // per)
    frames = [
        (f'{who} has €{budget} to spend at a climbing centre. Entry costs €{fee} and each climb costs €{per}. Write an inequality and find the greatest number of climbs.', f'{fee} + {per}c ≤ {budget}; c ≤ {(budget - fee) / per:.2f}, so at most {n} climbs'),
        (f'A phone plan costs ${fee} plus ${per} per GB. {who} wants the bill to stay below ${budget}. Form and solve an inequality for the number of whole GB she can use.', f'{fee} + {per}g < {budget}; at most {n if fee + per * n < budget else n - 1} GB'),
        (f'Find all integers x that satisfy both {2}x − 3 > {m(2 * (-2) - 3)} and x + {fee % 7} ≤ {fee % 7 + 4}, and represent them on a number line.', '−1, 0, 1, 2, 3, 4'),
    ]
    q, ans = rng.choice(frames)
    return dict(stem=q, answer=ans, markingKey=f'Correct inequality (M1 A1); solved (M1); answer interpreted for whole numbers in context: {ans} (A1).', marks=4)


@R.add('ch04-st3', 'C2', (2, 4), 'explain')
def ineq_explain(rng, slot):
    a = rng.randint(2, 9)
    q, ans = rng.choice([
        (f'Explain why x² > {a * a} does not mean x > {a} only.', f'Negative numbers also satisfy it: e.g. x = −{a + 1} gives {(a + 1) ** 2} > {a * a}. Solution: x < −{a} or x > {a}.'),
        (f'{name(rng)} says that if −x < {a} then x < −{a}. Test the claim with x = 0 and explain the correct result.', f'x = 0 satisfies −x < {a} but not x < −{a}; multiplying by −1 reverses the sign, giving x > −{a}.'),
        (f'Explain why the inequalities x > {a} and {a} < x describe the same set of numbers.', f'Both say x is to the right of {a} on the number line; reading an inequality from right to left reverses the symbol, not the meaning.'),
    ])
    return dict(stem=q, answer=ans, markingKey=f'{ans} R1 A1.', type='explain', marks=2)


R.facts('ch04-st4', F(
    terms=[('simultaneous equations', 'two or more equations with the same unknowns that are true at the same time'),
           ('elimination method', 'adding or subtracting multiples of the equations so that one unknown disappears')],
    why=[('Explain why the solution of two simultaneous linear equations is the intersection point of their graphs.', 'Each graph shows every (x, y) that satisfies that equation; only the intersection lies on both lines, so it satisfies both.'),
         ('Explain when substitution is a better method than elimination.', 'When one equation already gives one unknown in terms of the other (e.g. y = 2x − 1), substituting it removes that unknown immediately.'),
         ('Explain why some pairs of linear equations have no solution.', 'If the lines are parallel (same gradient, different intercepts) they never meet, so no (x, y) satisfies both.')],
    misc=[('To eliminate y from 2x + 3y = 12 and 5x − 3y = 9, subtract the equations.', 'The y terms have opposite signs (+3y and −3y), so you add the equations: 7x = 21.'),
          ('Once you find x you have solved the simultaneous equations.', 'You must also find y by substituting x back, and ideally check in the other equation.')],
))


def _sim(rng):
    xs, ys = rng.randint(-6, 8), rng.randint(-6, 8)
    a1, b1 = rng.randint(1, 6), rng.choice([i for i in range(-5, 6) if i])
    a2, b2 = rng.randint(1, 6), rng.choice([i for i in range(-5, 6) if i])
    if a1 * b2 - a2 * b1 == 0:
        return None
    return xs, ys, (a1, b1, a1 * xs + b1 * ys), (a2, b2, a2 * xs + b2 * ys)


def _eqn(a, b, c):
    s = f'{"" if a == 1 else a}x'
    s += f' + {"" if b == 1 else b}y' if b > 0 else f' − {"" if b == -1 else -b}y'
    return f'{s} = {m(c)}'


@R.add('ch04-st4', 'C3', (1, 4), 'short')
def sim_solve(rng, slot):
    r = _sim(rng)
    if not r:
        return None
    xs, ys, e1, e2 = r
    return dict(stem=f'Solve the simultaneous equations {_eqn(*e1)} and {_eqn(*e2)}.', answer=f'x = {m(xs)}, y = {m(ys)}',
                markingKey=f'Multiply to match coefficients and eliminate one unknown (M1); first value correct (A1); substitute back (M1); x = {m(xs)}, y = {m(ys)} (A1).', marks=4 if slot.d >= 3 else 3)


@R.add('ch04-st4', 'C3', (1, 3), 'short')
def sim_sub(rng, slot):
    xs, ys = rng.randint(-5, 7), rng.randint(-5, 7)
    k, c = rng.randint(2, 4), 0
    c = ys - k * xs
    a, b = rng.randint(1, 5), rng.randint(1, 5)
    return dict(stem=f'Use substitution to solve y = {_lin(k, c)} and {_eqn(a, b, a * xs + b * ys)}.', answer=f'x = {m(xs)}, y = {m(ys)}',
                markingKey=f'Substitute: {a}x + {b}({_lin(k, c)}) = {m(a * xs + b * ys)} (M1); x = {m(xs)} (A1); y = {m(ys)} (A1).', marks=3)


@R.add('ch04-st4', 'C2', (2, 4), 'explain')
def sim_count(rng, slot):
    k = rng.randint(2, 5)
    c1, c2 = rng.randint(1, 9), rng.randint(10, 20)
    q, ans = rng.choice([
        (f'Without solving, explain how many solutions the pair y = {k}x + {c1} and {2 * k}x − 2y = {m(-2 * c2)} has.', f'Rearranged, the second is y = {k}x + {c2}: same gradient, different intercept, so the lines are parallel and there are no solutions.'),
        (f'Explain how many solutions the equations y = {k}x + {c1} and {3 * k}x − 3y = {m(-3 * c1)} have.', f'The second rearranges to y = {k}x + {c1}: the same line, so there are infinitely many solutions.'),
        (f'Explain why the equations y = {k}x + {c1} and y = {-k}x + {c2} must have exactly one solution.', 'The gradients are different, so the lines are not parallel and cross at exactly one point.'),
    ])
    return dict(stem=q, answer=ans, markingKey=f'Rearrange to compare gradients/intercepts (M1); {ans} (R1).', type='explain', marks=2)


@R.add('ch04-st4', 'C4', (3, 5), 'multi_step')
def sim_tricky(rng, slot):
    xs, ys = rng.randint(1, 6), rng.randint(1, 6)
    a, b = rng.randint(2, 5), rng.randint(2, 5)
    q, ans, key = rng.choice([
        (f'Solve 1/x + 1/y = {frac(Fr(1, xs) + Fr(1, ys))} and 1/x − 1/y = {frac(Fr(1, xs) - Fr(1, ys))}.', f'x = {xs}, y = {ys}', 'Let p = 1/x, q = 1/y (M1); add/subtract to find p and q (M1 A1); invert to get x and y (A1).'),
        (f'The line y = mx + c passes through ({xs}, {a * xs + b}) and ({xs + 2}, {a * (xs + 2) + b}). Form two simultaneous equations and find m and c.', f'm = {a}, c = {b}', 'Two equations in m and c (M1 A1); eliminate c (M1); m and c correct (A1).'),
        (f'A point (p, q) satisfies p + q = {xs + ys}, and also {a}p − {b}q = {a * xs - b * ys}. Find p and q, and check that the point lies on both lines.', f'p = {xs}, q = {ys}', 'Elimination (M1); first value (A1); second value (A1); check in both equations (R1).'),
    ])
    return dict(stem=q, answer=ans, markingKey=key, marks=4, gap='G5')


R.facts('ch04-st5', F(
    terms=[('graphical solution', 'the coordinates of the point where the graphs of the two equations intersect')],
    why=[('Explain why a graphical solution may only be approximate.', 'It depends on reading coordinates from a scale; if the intersection is not at grid points the reading is limited by the scale.'),
         ('Explain why it is important to define your variables before forming simultaneous equations from a word problem.', 'Clear definitions (e.g. a = price of an adult ticket in €) make each equation interpretable and the final answer meaningful in context.')],
    misc=[('If 3 pens and 2 rulers cost $7, the equation is 3 + 2 = 7.', 'Use unknowns for the prices: 3p + 2r = 7.'),
          ('The solution x = 4, y = 2.5 to a ticket problem means 4 tickets and 2.5 tickets.', 'Check what the variables represent: here x and y were prices, so the answer is €4 and €2.50.')],
))


@R.add('ch04-st5', 'C3', (2, 5), 'short')
def sim_word(rng, slot):
    who, who2 = two_names(rng)
    p1, p2 = rng.choice([4, 5, 6, 7, 8, 9, 12]), rng.choice([2, 2.5, 3, 3.5, 4, 1.5])
    a1, b1, a2, b2 = rng.randint(2, 5), rng.randint(1, 4), rng.randint(1, 4), rng.randint(2, 6)
    if a1 * b2 == a2 * b1:
        return None
    ctx = rng.choice([
        (f'At a museum in {rng.choice(CITIES)}, {who} buys {a1} adult and {b1} child tickets for €{a1 * p1 + b1 * p2:g}. {who2} buys {a2} adult and {b2} child tickets for €{a2 * p1 + b2 * p2:g}.', 'Find the price of each ticket.', f'adult €{p1:g}, child €{p2:g}'),
        (f'{who} buys {a1} notebooks and {b1} pens for ${a1 * p1 + b1 * p2:g}; {who2} buys {a2} notebooks and {b2} pens for ${a2 * p1 + b2 * p2:g}.', 'Find the cost of one notebook and one pen.', f'notebook ${p1:g}, pen ${p2:g}'),
        (f'A café sells {a1} smoothies and {b1} muffins for £{a1 * p1 + b1 * p2:g}, and {a2} smoothies and {b2} muffins for £{a2 * p1 + b2 * p2:g}.', 'Find the price of a smoothie and of a muffin.', f'smoothie £{p1:g}, muffin £{p2:g}'),
    ])
    s, q, ans = ctx
    return dict(stem=f'{s} {q}', answer=ans, markingKey=f'Variables defined and two equations formed (M1 A1); solved (M1); {ans} (A1).', marks=4, gap='G7')


@R.add('ch04-st5', 'C3', (1, 3), 'short')
def sim_graph(rng, slot):
    xs, ys = rng.randint(-3, 5), rng.randint(-3, 6)
    m1, m2 = rng.choice([1, 2, -1]), rng.choice([-2, 3, 1 / 2 if False else -3])
    if m1 == m2:
        return None
    c1, c2 = ys - m1 * xs, ys - m2 * xs
    return dict(stem=f'The lines y = {_lin(m1, c1)} and y = {_lin(m2, c2)} are drawn on the same axes. Write down the coordinates of their point of intersection, and verify algebraically.', answer=f'({m(xs)}, {m(ys)})',
                markingKey=f'Intersection ({m(xs)}, {m(ys)}) (A1); verification: both equations give y = {m(ys)} when x = {m(xs)} (R1).', marks=2)


@R.add('ch04-st5', 'C4', (3, 5), 'multi_step')
def sim_word_hard(rng, slot):
    who = name(rng)
    a_, b_ = rng.randint(3, 12), rng.randint(2, 9)
    t = rng.randint(2, 5)
    frames = [
        (f'A two-digit number has digits that add up to {a_ % 9 + 4 if False else (lambda d1, d2: d1 + d2)(t, b_ % 9 + 1)}. When the digits are reversed, the new number is {9 * abs(t - (b_ % 9 + 1))} {"more" if (b_ % 9 + 1) > t else "less"} than the original. Find the number.', f'{10 * t + b_ % 9 + 1}'),
        (f'{who} paddles a kayak {a_ * t + b_ * t} km downstream in {t} hours and back upstream in {round((a_ * t + b_ * t) / (a_ - b_), 2) if a_ > b_ else "—"} hours. Find her speed in still water and the speed of the current.', f'{a_} km/h and {b_} km/h' if a_ > b_ else None),
        (f'Concert tickets cost €{a_ + 20} (standard) and €{a_ + 45} (VIP). {t * 50 + b_ * 10} tickets were sold for €{(a_ + 20) * (t * 50) + (a_ + 45) * (b_ * 10)}. How many of each were sold?', f'{t * 50} standard, {b_ * 10} VIP'),
    ]
    q, ans = rng.choice(frames)
    if ans is None or '—' in q or (b_ % 9 + 1) == t:
        return None
    return dict(stem=q, answer=ans, markingKey=f'Variables defined (C1); two correct equations (M1 A1); solved (M1); {ans} with check in context (A1).', marks=5, gap='G7')


@R.add('ch04-st5', 'C2', (2, 4), 'explain')
def sim_word_explain(rng, slot):
    a, b = rng.randint(2, 6), rng.randint(2, 6)
    q, ans = rng.choice([
        (f'The solution to a problem about numbers of coaches (c) and minibuses (m) is c = {a}.5, m = {b}. Explain why this cannot be accepted and what it suggests.', 'Vehicles come in whole numbers; a non-integer answer suggests an error in forming or solving the equations (or that the situation is impossible as stated).'),
        (f'Explain how you could use a graph to check the solution of x + y = {a + b} and x − y = {a - b}.', f'Draw both lines; they should cross at ({a}, {b}), the algebraic solution.'),
        (f'{name(rng)} forms the equations 2a + 3c = 31 and a + c = 12 for adult and child tickets. Explain what each equation represents in words.', 'The first says the total cost of 2 adult and 3 child tickets is 31; the second says the cost of one adult plus one child ticket is 12.'),
    ])
    return dict(stem=q, answer=ans, markingKey=f'{ans} (R1 R1)', type='explain', marks=2)


@R.add('ch04-st2', 'C1', (1, 3), 'mcq')
def subj_mcq(rng, slot):
    q = rng.choice([
        ('v = u + at', 'u', 'u = v − at', ['u = v + at', 'u = (v − t)/a', 'u = at − v']),
        ('P = 2l + 2w', 'l', 'l = (P − 2w)/2', ['l = P − w', 'l = P/2 − 2w', 'l = (P + 2w)/2']),
        ('y = mx + c', 'x', 'x = (y − c)/m', ['x = y/m − c', 'x = (y + c)/m', 'x = m(y − c)']),
        ('A = lw', 'w', 'w = A/l', ['w = A − l', 'w = l/A', 'w = Al']),
        ('d = st', 't', 't = d/s', ['t = ds', 't = s/d', 't = d − s']),
        ('C = 2πr', 'r', 'r = C/(2π)', ['r = 2πC', 'r = C − 2π', 'r = 2C/π']),
        ('V = lwh', 'h', 'h = V/(lw)', ['h = V − lw', 'h = Vlw', 'h = lw/V']),
        ('y = 5 − 2x', 'x', 'x = (5 − y)/2', ['x = (y − 5)/2', 'x = 5 − y/2', 'x = (5 + y)/2']),
    ])
    fml, v, a, w = q
    return mcq(rng, f'Which of the following correctly makes {v} the subject of {fml}?', a, w, f'Apply inverse operations: {a}.')


# =============================================================================================
# ch05 Quadratic Equations
# =============================================================================================
R.facts('ch05-st1', F(
    terms=[('quadratic equation', 'an equation that can be written ax² + bx + c = 0 with a ≠ 0'),
           ('root of an equation', 'a value of the unknown that makes the equation true; for a quadratic, an x-intercept of y = ax² + bx + c')],
    why=[('Explain why, if (x − 3)(x + 5) = 0, then x = 3 or x = −5.', 'If a product of two numbers is zero, at least one of them must be zero (null factor law), so x − 3 = 0 or x + 5 = 0.'),
         ('Explain why you must rearrange x² + 2x = 15 to equal zero before factorising.', 'The null factor law only works when the product equals zero; (x)(x + 2) = 15 gives no direct conclusion about either factor.'),
         ('Explain why dividing both sides of x² = 5x by x loses a solution.', 'Dividing by x assumes x ≠ 0, but x = 0 is a solution; factorising x(x − 5) = 0 keeps both x = 0 and x = 5.')],
    misc=[('x² = 9 has the single solution x = 3.', 'x = −3 also works: x² − 9 = (x − 3)(x + 3) = 0, so x = ±3.'),
          ('(x − 2)(x + 4) = 7 means x − 2 = 7 or x + 4 = 7.', 'The null factor law needs the product to be 0. Expand: x² + 2x − 15 = 0 → (x + 5)(x − 3) = 0.')],
))


@R.add('ch05-st1', 'C3', (1, 3), 'short')
def quad_fact_solve(rng, slot):
    p, q = rng.sample([i for i in range(-9, 10) if i], 2)
    a = 1 if slot.d <= 2 else rng.choice([2, 3])
    e = sp.expand((a * x - p) * (x - q))
    roots = sorted({Fr(p, a), Fr(q)})
    return dict(stem=f'Solve {_poly(e)} = 0 by factorising.', answer='x = ' + ' or x = '.join(m(frac(r)) for r in roots),
                markingKey=f'({_poly(a * x - p)})({_poly(x - q)}) = 0 (M1 A1); x = ' + ' or '.join(m(frac(r)) for r in roots) + ' (A1).', marks=3)


@R.add('ch05-st1', 'C1', (1, 3), 'mcq')
def quad_roots_mcq(rng, slot):
    p, q = rng.sample([i for i in range(-9, 10) if i], 2)
    correct = f'x = {m(p)} or x = {m(q)}'
    w = [f'x = {m(-p)} or x = {m(-q)}', f'x = {m(p)} or x = {m(-q)}', f'x = {m(p * q)} or x = 0']
    return mcq(rng, f'What are the solutions of (x − {m(p)})(x − {m(q)}) = 0?'.replace('− −', '+ '), correct, w, 'Set each factor equal to zero (null factor law).')


@R.add('ch05-st1', 'C4', (3, 5), 'multi_step')
def quad_fact_context(rng, slot):
    w = rng.randint(3, 12)
    k = rng.randint(2, 7)
    n = rng.randint(4, 15)
    frames = [
        (f'A rectangular poster is {k} cm longer than it is wide and has area {w * (w + k)} cm². Form a quadratic equation and solve it to find the dimensions. Explain why one solution is rejected.', f'{w} cm by {w + k} cm (reject x = −{w + k})'),
        (f'The product of two consecutive positive integers is {n * (n + 1)}. Form and solve an equation to find them.', f'{n} and {n + 1}'),
        (f'A ball is thrown so that its height is h = {k}t(… ) — more precisely h = {5 * w}t − 5t² metres. Find when it hits the ground again and its height after 1 second.', f't = {w} s; h(1) = {5 * w - 5} m'),
        (f'{name(rng)} thinks of a number, squares it and subtracts {k} times the number. The result is {n * n - k * n}. Find the possible numbers.', f'{n} or {k - n}'),
    ]
    q, ans = rng.choice(frames)
    q = q.replace(f'h = {k}t(… ) — more precisely ', '')
    return dict(stem=q, answer=ans, markingKey=f'Quadratic equation formed and rearranged to = 0 (M1 A1); factorised (M1); solutions found and interpreted/rejected in context: {ans} (A1 R1).', marks=5)


R.facts('ch05-st2', F(
    terms=[('completing the square', 'rewriting x² + bx + c as (x + b/2)² + (c − b²/4)'),
           ('vertex form', 'y = a(x − h)² + k, which shows the turning point (h, k) directly')],
    why=[('Explain why x² + 6x can be written as (x + 3)² − 9.', '(x + 3)² = x² + 6x + 9, which is 9 more than x² + 6x, so subtract 9.'),
         ('Explain why completing the square shows the minimum value of x² + bx + c.', 'In (x + p)² + q the square is never negative, so the least value is q, reached when x = −p.')],
    misc=[('x² + 8x + 5 = (x + 8)² + 5.', 'Halve the x-coefficient: (x + 4)² − 16 + 5 = (x + 4)² − 11.'),
          ('(x − 3)² = 5 gives x = 3 + √5 only.', 'Square roots give ±: x − 3 = ±√5, so x = 3 ± √5.')],
))


@R.add('ch05-st2', 'C3', (1, 4), 'short')
def cts(rng, slot):
    b = rng.choice([i for i in range(-10, 11) if i and i % 2 == 0]) if slot.d <= 2 else rng.choice([i for i in range(-9, 10) if i])
    c = rng.randint(-12, 12)
    h = Fr(b, 2)
    k = c - h * h
    hs = frac(abs(h))
    form = f'(x {"+" if h > 0 else "−"} {hs})² {"+" if k >= 0 else "−"} {frac(abs(k))}'
    return dict(stem=f'Write {_poly(x ** 2 + b * x + c)} in the form (x + p)² + q.', answer=form,
                markingKey=f'p = {frac(h)} (half of {b}) (M1 A1); q = {c} − ({frac(h)})² = {frac(k)} (A1).', marks=3)


@R.add('ch05-st2', 'C3', (2, 4), 'short')
def cts_solve(rng, slot):
    h = rng.randint(-6, 6)
    k = rng.choice([2, 3, 5, 6, 7, 10, 11])
    # (x - h)^2 = k -> x^2 - 2hx + h^2 - k = 0
    e = sp.expand((x - h) ** 2 - k)
    return dict(stem=f'Solve {_poly(e)} = 0 by completing the square, giving exact answers.', answer=f'x = {m(h)} ± √{k}',
                markingKey=f'(x {"−" if h > 0 else "+"} {abs(h)})² = {k} (M1 A1); x = {m(h)} ± √{k} (A1).', marks=3)


@R.add('ch05-st2', 'C4', (3, 5), 'multi_step')
def cts_minmax(rng, slot):
    h, k = rng.randint(1, 9), rng.randint(-20, 30)
    e = sp.expand((x - h) ** 2 + k)
    frames = [
        (f'By completing the square, find the minimum value of {_poly(e)} and the value of x where it occurs.', f'minimum {k} at x = {h}'),
        (f'The cost in dollars of producing x hundred units is C = {_poly(e + 50)}. Use completing the square to find the production level that minimises cost and the minimum cost.', f'x = {h} (hundred units), C = {k + 50}'),
        (f'Show that {_poly(e + abs(k) + 1 - k)} is positive for all real x.', f'= (x − {h})² + {abs(k) + 1} ≥ {abs(k) + 1} > 0'),
    ]
    q, ans = rng.choice(frames)
    return dict(stem=q, answer=ans, markingKey=f'Completed square form with h = {h} (M1 A1); argument that the square is ≥ 0 (R1); {ans} (A1).', marks=4)


@R.add('ch05-st2', 'C2', (2, 4), 'explain')
def cts_explain(rng, slot):
    b = rng.choice([4, 6, 8, 10, 12])
    return dict(stem=f'Use an area model (a square with a missing corner) to explain why x² + {b}x + {b * b // 4} is a perfect square.', answer=f'(x + {b // 2})²',
                markingKey=f'Split {b}x into two strips of {b // 2}x on two sides of the x by x square (M1); the missing corner is {b // 2} by {b // 2} = {b * b // 4} (R1); whole square has side x + {b // 2} (A1).', type='explain', marks=3)


R.facts('ch05-st3', F(
    terms=[('discriminant', 'Δ = b² − 4ac for ax² + bx + c = 0; its sign tells you how many real roots there are'),
           ('quadratic formula', 'x = (−b ± √(b² − 4ac)) / (2a), the solutions of ax² + bx + c = 0')],
    why=[('Explain why a negative discriminant means there are no real solutions.', 'The formula needs √(b² − 4ac); the square root of a negative number is not a real number.'),
         ('Explain why Δ = 0 gives exactly one (repeated) root.', 'With √0 = 0 the ± gives the same value, x = −b/(2a); the parabola just touches the x-axis.'),
         ('Explain why the quadratic formula works for every quadratic, even those that do not factorise.', 'It is derived by completing the square on the general ax² + bx + c = 0, so it applies to any a ≠ 0.')],
    misc=[('For 2x² − 3x − 5 = 0, b = 3 so −b = 3.', 'b = −3, so −b = +3 here – but the sign must come from b itself; students often drop the minus and write b = 3, then −b = −3.'),
          ('x = −b ± √(b² − 4ac)/2a, so only the square root is divided by 2a.', 'The whole numerator −b ± √(b² − 4ac) is divided by 2a.')],
))


@R.add('ch05-st3', 'C3', (2, 4), 'numerical')
def qformula(rng, slot):
    a, b, c = rng.randint(1, 4), rng.randint(-9, 9), rng.randint(-9, 9)
    D = b * b - 4 * a * c
    if D <= 0 or int(math.isqrt(D)) ** 2 == D:
        return None
    r1, r2 = (-b + math.sqrt(D)) / (2 * a), (-b - math.sqrt(D)) / (2 * a)
    return dict(stem=f'Solve {_poly(a * x ** 2 + b * x + c)} = 0 using the quadratic formula, giving answers to 3 significant figures.', answer=f'x = {r1:.3g} or x = {r2:.3g}',
                markingKey=f'a = {a}, b = {b}, c = {c} substituted correctly (M1); Δ = {D} (A1); x = {r1:.3g} or {r2:.3g} (A1 A1).', type='numerical', marks=4)


@R.add('ch05-st3', 'C1', (1, 3), 'mcq')
def discr_mcq(rng, slot):
    a, b, c = rng.randint(1, 5), rng.randint(-8, 8), rng.randint(-8, 8)
    D = b * b - 4 * a * c
    ans = 'two distinct real roots' if D > 0 else 'one repeated real root' if D == 0 else 'no real roots'
    w = [o for o in ['two distinct real roots', 'one repeated real root', 'no real roots', 'infinitely many roots'] if o != ans]
    return mcq(rng, f'The equation {_poly(a * x ** 2 + b * x + c)} = 0 has:', ans, w, f'Δ = ({b})² − 4({a})({c}) = {D}.')


@R.add('ch05-st3', 'C4', (3, 5), 'multi_step')
def discr_k(rng, slot):
    a, b = rng.randint(1, 3), rng.choice([2, 4, 6, 8, 10])
    # a x^2 + b x + k = 0 has equal roots when b^2 = 4 a k  -> k = b^2/(4a)
    k = Fr(b * b, 4 * a)
    frames = [
        (f'Find the value of k for which {_poly(a * x ** 2 + b * x)} + k = 0 has exactly one real root, and find that root.', f'k = {frac(k)}; x = {frac(Fr(-b, 2 * a))}'),
        (f'Find the range of values of k for which {_poly(a * x ** 2 + b * x)} + k = 0 has two distinct real roots.', f'k < {frac(k)}'),
        (f'For which values of k does the line y = k meet the curve y = {_poly(a * x ** 2 + b * x)} exactly once? Interpret your answer graphically.', f'k = {frac(-k)}: the line touches the vertex'),
    ]
    q, ans = rng.choice(frames)
    return dict(stem=q, answer=ans, markingKey=f'Use Δ = b² − 4ac with the correct condition (M1); {b}² − 4({a})(k) (A1); solve (M1); {ans} (A1).', marks=4, gap='G5')


@R.add('ch05-st3', 'C2', (2, 4), 'explain')
def discr_explain(rng, slot):
    a, c = rng.randint(1, 5), rng.randint(1, 9)
    return dict(stem=f'Without solving, explain why {a}x² + {c} = 0 has no real solutions, and confirm using the discriminant.', answer='No real solutions',
                markingKey=f'{a}x² ≥ 0 so {a}x² + {c} ≥ {c} > 0, never zero (R1); Δ = 0 − 4({a})({c}) = {-4 * a * c} < 0 (A1).', type='explain', marks=2)


R.facts('ch05-st4', F(
    terms=[('mathematical model', 'an equation or function that represents a real situation so it can be analysed')],
    why=[('Explain why you must check solutions of a quadratic word problem against the context.', 'The algebra may give values that are mathematically correct but impossible in context, e.g. a negative length or time.'),
         ('Explain why a quadratic model of a thrown ball has two times for most heights.', 'The ball passes each height once on the way up and once on the way down, matching the two roots.')],
    misc=[('A negative solution of a quadratic word problem means the student made an error.', 'Not necessarily: the equation may correctly have a negative root that is simply rejected in the context.')],
))


@R.add('ch05-st4', 'C3', (2, 5), 'short')
def quad_word(rng, slot):
    who = name(rng)
    w = rng.randint(3, 15)
    k = rng.randint(1, 8)
    frames = [
        (f'A garden is {k} m longer than it is wide. Its area is {w * (w + k)} m². Find the width.', f'{w} m'),
        (f'A square has its side increased by {k} cm and its area becomes {(w + k) ** 2} cm². Find the original side.', f'{w} cm'),
        (f'The sum of a number and its square is {w * w + w}. Find the positive number.', f'{w}'),
        (f'A right-angled triangle has legs x cm and (x + {k}) cm and area {w * (w + k) / 2:g} cm². Find x.', f'x = {w}'),
        (f'{who} cuts a {2 * (2 * w + k)} cm length of wire into a rectangle of area {w * (w + k)} cm². Find the sides.', f'{w} cm and {w + k} cm'),
    ]
    q, ans = rng.choice(frames)
    return dict(stem=q, answer=ans, markingKey=f'Quadratic equation formed (M1 A1); solved (M1); negative root rejected in context (R1); {ans} (A1).', marks=4, gap='G7')


@R.add('ch05-st4', 'C4', (3, 5), 'multi_step')
def quad_model(rng, slot):
    u = rng.choice([10, 15, 20, 25, 30])
    h0 = rng.choice([0, 1, 2, 5, 10])
    T = (u + math.sqrt(u * u + 20 * h0)) / 10
    tmax = u / 10
    hmax = h0 + u * tmax - 5 * tmax ** 2
    p = rng.choice([2, 3, 4, 5])
    frames = [
        (f'A ball is kicked from a height of {h0} m; its height after t seconds is h = {h0} + {u}t − 5t². (a) Find when it lands. (b) Find its maximum height.'.replace(' 0 + ', ' '), f'(a) t ≈ {T:.2f} s (b) {hmax:g} m at t = {tmax:g} s'),
        (f'A company’s profit in thousands of US$ is P = −{p}x² + {p * 2 * u // 2}x − {p * 20}, where x is the price in dollars. Find the prices that give zero profit and the price that maximises profit.', None),
    ]
    q, ans = rng.choice(frames)
    if ans is None:
        a_, b_, c_ = -p, p * u, -p * 20
        D = b_ * b_ - 4 * a_ * c_
        r1, r2 = sorted([(-b_ + math.sqrt(D)) / (2 * a_), (-b_ - math.sqrt(D)) / (2 * a_)])
        ans = f'zero profit at x ≈ {r1:.2f} and x ≈ {r2:.2f}; maximum at x = {u / 2:g}'
    return dict(stem=q, answer=ans, markingKey=f'Correct equation set equal to the condition (M1); solved with formula or factorising (M1 A1); turning point by symmetry/completing the square (M1); interpretation in context with units (C1). {ans}', marks=6)


@R.add('ch05-st4', 'C2', (2, 4), 'explain')
def quad_word_explain(rng, slot):
    w = rng.randint(3, 12)
    k = rng.randint(1, 6)
    return dict(stem=f'The width w of a rectangle satisfies w² + {k}w − {w * (w + k)} = 0, giving w = {w} or w = {-(w + k)}. Explain which value is valid and why.', answer=f'w = {w}',
                markingKey=f'A width must be positive, so w = −{w + k} is rejected (R1); w = {w} (A1).', type='explain', marks=2)


@R.add('ch05-st1', 'C2', (2, 4), 'explain')
def quad_null_explain(rng, slot):
    p, q = rng.sample(range(1, 10), 2)
    k = rng.randint(2, 9)
    q_, ans = rng.choice([
        (f'{name(rng)} solves x² = {k}x by dividing both sides by x and gets x = {k}. Explain what has gone wrong.', f'Dividing by x loses x = 0. Rearranging: x² − {k}x = 0, x(x − {k}) = 0, so x = 0 or x = {k}.'),
        (f'Explain why (x − {p})(x + {q}) = 0 has exactly two solutions but (x − {p})² = 0 has only one.', f'The first gives x = {p} or x = −{q}; the second has the same factor twice, so both give x = {p} (a repeated root).'),
        (f'Explain how the solutions of (x − {p})(x − {q}) = 0 relate to the graph of y = (x − {p})(x − {q}).', f'They are the x-intercepts: the graph crosses the x-axis at x = {p} and x = {q}.'),
        (f'Explain why (x − {p})(x − {q}) = {k} cannot be solved by writing x − {p} = {k} or x − {q} = {k}.', 'The null factor law only applies to a product equal to 0; many pairs of factors multiply to a non-zero number.'),
    ])
    return dict(stem=q_, answer=ans, markingKey=f'{ans} (R1 A1)', type='explain', marks=2)


@R.add('ch05-st2', 'C2', (2, 4), 'explain')
def cts_explain2(rng, slot):
    h, k = rng.randint(1, 8), rng.randint(1, 12)
    sign = rng.choice([1, -1])
    q_, ans = rng.choice([
        (f'Explain what the completed-square form (x {"−" if sign > 0 else "+"} {h})² + {k} tells you about the graph of the quadratic.', f'Turning point (minimum) at ({sign * h}, {k}); axis of symmetry x = {sign * h}; since {k} > 0 it never meets the x-axis.'),
        (f'Explain why the equation (x {"−" if sign > 0 else "+"} {h})² = −{k} has no real solutions.', 'A square of a real number is never negative, so it cannot equal a negative number.'),
        (f'{name(rng)} writes x² + {2 * h}x + {k} = (x + {2 * h})² + {k} − {4 * h * h}. Explain the error.', f'The bracket should contain half the x-coefficient: (x + {h})² + {k} − {h * h}.'),
    ])
    return dict(stem=q_, answer=ans, markingKey=f'{ans} (R1 A1)', type='explain', marks=2)


# =============================================================================================
# ch06 Functions and Their Graphs
# =============================================================================================
R.facts('ch06-st1', F(
    terms=[('function', 'a relation in which every input in the domain has exactly one output'),
           ('domain', 'the set of all allowed input values of a function'),
           ('range', 'the set of all output values a function actually takes'),
           ('relation', 'any set of ordered pairs linking inputs to outputs')],
    facts=[('Which mapping type is NOT a function?', 'one-to-many', ['one-to-one', 'many-to-one', 'a mapping where each input has a single output'], 'A one-to-many mapping gives some input two outputs.'),
           ('A graph represents a function if:', 'every vertical line meets it at most once', ['every horizontal line meets it at most once', 'it passes through the origin', 'it is a straight line'], 'The vertical line test: each x has only one y.')],
    why=[('Explain why a circle x² + y² = 25 is not the graph of a function of x.', 'For x = 3, both y = 4 and y = −4 lie on the circle, so one input has two outputs.'),
         ('Explain why the domain of f(x) = √x is x ≥ 0 for real outputs.', 'The square root of a negative number is not real, so only non-negative inputs give real outputs.'),
         ('Explain why f(x) = 1/x cannot have 0 in its domain.', 'Division by zero is undefined, so x = 0 has no output.')],
    misc=[('The range of f(x) = x² is all real numbers.', 'x² is never negative, so the range is y ≥ 0.'),
          ('A many-to-one mapping cannot be a function.', 'Many-to-one is allowed (e.g. f(x) = x² maps 2 and −2 to 4); one-to-many is not.')],
))


@R.add('ch06-st1', 'C3', (1, 4), 'short')
def dom_range(rng, slot):
    k = rng.randint(1, 9)
    cases = [
        (f'f(x) = √(x − {k})', f'domain x ≥ {k}; range f(x) ≥ 0'),
        (f'f(x) = 1/(x + {k})', f'domain x ≠ −{k}; range f(x) ≠ 0'),
        (f'f(x) = x² + {k}', f'domain all real x; range f(x) ≥ {k}'),
        (f'f(x) = {k} − x²', f'domain all real x; range f(x) ≤ {k}'),
        (f'f(x) = 2x + {k}, for −2 ≤ x ≤ 3', f'range {k - 4} ≤ f(x) ≤ {k + 6}'),
        (f'f(x) = (x − {k})² − 1', 'domain all real x; range f(x) ≥ −1'),
        (f'f(x) = √({k * k} − x²)', f'domain −{k} ≤ x ≤ {k}; range 0 ≤ f(x) ≤ {k}'),
    ]
    f_, ans = rng.choice(cases)
    return dict(stem=f'State the domain and range of {f_}.', answer=ans, markingKey=f'{ans} (A1 domain, A1 range; correct notation C1).', marks=2 if slot.d <= 2 else 3)


@R.add('ch06-st1', 'C3', (1, 2), 'short')
def mapping_check(rng, slot):
    xs = rng.sample(range(-4, 6), 4)
    is_f = rng.random() < 0.5
    pairs = [(a, rng.randint(-5, 9)) for a in xs]
    if not is_f:
        pairs.append((xs[0], pairs[0][1] + rng.randint(1, 4)))
    rng.shuffle(pairs)
    s = ', '.join(f'({a}, {b})' for a, b in pairs)
    return dict(stem=f'Does the set of ordered pairs {{{s}}} represent a function? Give a reason.', answer='Yes' if is_f else 'No',
                markingKey=('Yes: every first coordinate appears once (R1).' if is_f else f'No: the input {xs[0]} is paired with two different outputs (R1).') + ' A1 for the decision.', marks=2)


@R.add('ch06-st1', 'C4', (3, 5), 'multi_step')
def func_context(rng, slot):
    c = rng.choice([4, 5, 6, 8])
    cap = rng.choice([20, 30, 40, 50])
    who = name(rng)
    frames = [
        (f'A taxi fare in {rng.choice(CITIES)} is F(d) = {c} + 2.5d dollars for a distance of d km, and taxis will not take trips over {cap} km. State a sensible domain and the corresponding range of F, and explain why F is a function.', f'0 < d ≤ {cap}; {c} < F ≤ {c + 2.5 * cap:g}; each distance gives one fare'),
        (f'{who} rents bikes: the cost C(h) = {c}h euros for h whole hours, up to 8 hours. List the domain and range, and explain whether a graph of C should be drawn as a continuous line.', f'domain {{1, …, 8}}, range {{{c}, {2 * c}, …, {8 * c}}}; discrete points only'),
        (f'The temperature T (°C) of a cup of tea t minutes after pouring is modelled by T = 20 + 70(0.9)ᵗ for 0 ≤ t ≤ 30. Find the range of the model and explain what the lower limit means in context.', f'about 22.9 ≤ T ≤ 90 (T(30) ≈ {20 + 70 * 0.9 ** 30:.1f}); tea approaches room temperature 20 °C'),
    ]
    q, ans = rng.choice(frames)
    return dict(stem=q, answer=ans, markingKey=f'Domain justified from context (A1 R1); range found (A1); reasoning about function / continuity communicated (C1). {ans}', marks=4)


R.facts('ch06-st2', F(
    terms=[('function notation', 'writing f(x) for the output of the function f when the input is x'),
           ('composite function', 'f(g(x)), the result of applying g first and then f')],
    why=[('Explain the difference between f(2x) and 2f(x).', 'f(2x) doubles the input before applying f; 2f(x) applies f and then doubles the output. For f(x) = x², f(2x) = 4x² but 2f(x) = 2x².'),
         ('Explain why f(a + b) is not usually equal to f(a) + f(b).', 'Only linear functions through the origin behave like that; e.g. for f(x) = x², f(1 + 2) = 9 but f(1) + f(2) = 5.')],
    misc=[('If f(x) = 3x + 1, then f(x + 2) = 3x + 3.', 'Replace x by (x + 2): 3(x + 2) + 1 = 3x + 7.'),
          ('f(x) means f multiplied by x.', 'f(x) is the output of the function f at input x, not a product.')],
))


@R.add('ch06-st2', 'C3', (1, 3), 'short')
def f_eval(rng, slot):
    a, b, c = rng.randint(1, 4), rng.randint(-6, 6), rng.randint(-9, 9)
    v = rng.randint(-4, 5)
    f_ = a * x ** 2 + b * x + c
    if slot.d <= 1:
        g = rng.randint(2, 6) * x + rng.randint(-9, 9)
        return dict(stem=f'Given f(x) = {_poly(g)}, find f({m(v)}).', answer=m(g.subs(x, v)), markingKey=f'Substitute x = {m(v)}: {m(g.subs(x, v))} (A1).', marks=1)
    return dict(stem=f'Given f(x) = {_poly(f_)}, find f({m(v)}) and f(−{abs(v) + 1}).', answer=f'{m(f_.subs(x, v))} and {m(f_.subs(x, -(abs(v) + 1)))}',
                markingKey=f'Correct substitution with brackets for negatives (M1); f({m(v)}) = {m(f_.subs(x, v))}, f(−{abs(v) + 1}) = {m(f_.subs(x, -(abs(v) + 1)))} (A1 A1).', marks=3)


@R.add('ch06-st2', 'C3', (2, 4), 'short')
def f_solve(rng, slot):
    a, b = rng.randint(2, 7), rng.randint(-9, 9)
    t = rng.randint(-5, 9)
    g = a * x + b
    return dict(stem=f'f(x) = {_poly(g)}. Find the value of x for which f(x) = {m(a * t + b)}.', answer=f'x = {m(t)}',
                markingKey=f'{_poly(g)} = {m(a * t + b)} (M1); x = {m(t)} (A1).', marks=2)


@R.add('ch06-st2', 'C4', (3, 5), 'multi_step')
def f_compose(rng, slot):
    a, b = rng.randint(2, 5), rng.randint(-5, 6)
    c = rng.randint(-4, 5)
    f_ = a * x + b
    g = x ** 2 + c
    v = rng.randint(-3, 4)
    frames = [
        (f'f(x) = {_poly(f_)} and g(x) = {_poly(g)}. Find (a) f(g({m(v)})), (b) g(f(x)) in simplest form (Extended).', f'(a) {m(f_.subs(x, g.subs(x, v)))} (b) {_poly(g.subs(x, f_))}'),
        (f'f(x) = {_poly(f_)}. Find an expression for f(x + 1) − f(x) and explain what it tells you about the graph of f.', f'{a}: the gradient – f increases by {a} for every 1 increase in x'),
        (f'g(x) = {_poly(g)}. Solve g(x) = f(x) where f(x) = {_poly(f_)}.', None),
    ]
    q, ans = rng.choice(frames)
    if ans is None:
        sols = sp.solve(sp.Eq(g, f_), x)
        if not all(s.is_real for s in sols):
            return None
        ans = ' or '.join(f'x = {pe(sp.nsimplify(s))}' for s in sols)
    return dict(stem=q, answer=ans, markingKey=f'Correct substitution of one function into the other (M1); algebra simplified (M1 A1); {ans} (A1).', marks=4, gap='G5')


@R.add('ch06-st2', 'C2', (2, 4), 'explain')
def f_notation_explain(rng, slot):
    k = rng.randint(2, 6)
    q_, ans = rng.choice([
        (f'For f(x) = x², explain the difference between f({k}x) and {k}f(x) and evaluate both when x = 1.', f'f({k}x) = {k * k}x² (input scaled), {k}f(x) = {k}x² (output scaled); at x = 1: {k * k} and {k}.'),
        (f'Explain in words what f(3) = {k} means for a function f.', f'When the input is 3, the output is {k}; the point (3, {k}) lies on the graph of f.'),
        (f'Explain why, for f(x) = {k}x, f(a + b) = f(a) + f(b) is true, but for g(x) = {k}x + 1 it is false.', f'{k}(a + b) = {k}a + {k}b; but {k}(a + b) + 1 ≠ ({k}a + 1) + ({k}b + 1), which has an extra 1.'),
    ])
    return dict(stem=q_, answer=ans, markingKey=f'{ans} (R1 A1)', type='explain', marks=2)


R.facts('ch06-st3', F(
    terms=[('parabola', 'the U-shaped graph of a quadratic function'),
           ('vertex (turning point)', 'the highest or lowest point of a parabola, where it changes direction'),
           ('axis of symmetry', 'the vertical line through the vertex about which the parabola is symmetric, x = −b/(2a)')],
    why=[('Explain how the sign of a in y = ax² + bx + c tells you the shape of the parabola.', 'If a > 0 the x² term dominates positively for large |x|, so the parabola opens upward (minimum); if a < 0 it opens downward (maximum).'),
         ('Explain why the axis of symmetry lies halfway between the two x-intercepts.', 'A parabola is symmetric about its axis, so equal-height points – including the two roots – are equally far from it.'),
         ('Explain why y = (x − 2)² + 3 has no x-intercepts.', '(x − 2)² ≥ 0 so y ≥ 3 > 0 for all x; the graph never reaches the x-axis.')],
    misc=[('The vertex of y = (x + 4)² − 1 is (4, −1).', 'x + 4 = 0 when x = −4, so the vertex is (−4, −1).'),
          ('The y-intercept of y = 2x² − 3x + 5 is (0, 2).', 'Set x = 0: y = 5, so the y-intercept is (0, 5).')],
))


@R.add('ch06-st3', 'C3', (1, 4), 'short')
def parabola_features(rng, slot):
    p, q = rng.sample([i for i in range(-7, 8)], 2)
    a = rng.choice([1, -1, 2]) if slot.d >= 3 else 1
    e = sp.expand(a * (x - p) * (x - q))
    h = Fr(p + q, 2)
    k = Fr(a) * (h - p) * (h - q)
    return dict(stem=f'For y = {_poly(e)}, find the x-intercepts, the y-intercept, the axis of symmetry and the vertex.', answer=f'x = {m(p)} and {m(q)}; (0, {m(a * p * q)}); x = {m(frac(h))}; ({m(frac(h))}, {m(frac(k))})',
                markingKey=f'Factorise or formula for roots (A1); y-intercept {m(a * p * q)} (A1); axis x = {m(frac(h))} (A1); vertex ({m(frac(h))}, {m(frac(k))}) (A1).', marks=4)


@R.add('ch06-st3', 'C1', (1, 3), 'mcq')
def vertex_mcq(rng, slot):
    h, k = rng.randint(-6, 6), rng.randint(-8, 8)
    if h == 0:
        return None
    e = f'y = (x {"−" if h > 0 else "+"} {abs(h)})² {"+" if k >= 0 else "−"} {abs(k)}'
    return mcq(rng, f'What is the vertex of {e}?', f'({m(h)}, {m(k)})', [f'({m(-h)}, {m(k)})', f'({m(h)}, {m(-k)})', f'({m(-h)}, {m(-k)})'], f'Vertex form y = (x − h)² + k has vertex (h, k).')


@R.add('ch06-st3', 'C4', (3, 5), 'multi_step')
def parabola_find(rng, slot):
    p, q = rng.sample(range(-6, 7), 2)
    a = rng.choice([1, 2, -1, 3])
    t = rng.choice([v for v in range(-4, 5) if v not in (p, q)])
    yt = a * (t - p) * (t - q)
    frames = [
        (f'A parabola crosses the x-axis at x = {m(p)} and x = {m(q)} and passes through ({m(t)}, {m(yt)}). Find its equation in the form y = ax² + bx + c.', f'y = {_poly(a * (x - p) * (x - q))}'),
        (f'The arch of a bridge is modelled by a parabola meeting the road at x = {min(p, q) if a < 0 else 0} m and x = {abs(p - q) + 2} m, with maximum height {abs(yt) + 3} m. Find the equation of the arch, taking the road as y = 0.', None),
    ]
    q_, ans = rng.choice(frames)
    if ans is None:
        L = abs(p - q) + 2
        H = abs(yt) + 3
        ans = f'y = −{frac(Fr(4 * H, L * L))}x(x − {L})'
        q_ = f'The arch of a bridge is modelled by a parabola meeting the road at x = 0 m and x = {L} m, with maximum height {H} m. Find the equation of the arch, taking the road as y = 0.'
    return dict(stem=q_, answer=ans, markingKey=f'Use intercept form y = a(x − r₁)(x − r₂) (M1); substitute the extra point to find a (M1 A1); final equation {ans} (A1).', marks=4, gap='G5')


@R.add('ch06-st3', 'C2', (2, 4), 'explain')
def parabola_explain(rng, slot):
    p, q = rng.sample(range(-6, 8), 2)
    return dict(stem=f'A parabola has x-intercepts at {m(p)} and {m(q)}. Explain how you can find its axis of symmetry without knowing its equation.', answer=f'x = {frac(Fr(p + q, 2))}',
                markingKey=f'The axis is midway between the roots by symmetry (R1): x = ({m(p)} + {m(q)})/2 = {frac(Fr(p + q, 2))} (A1).', type='explain', marks=2)


R.facts('ch06-st4', F(
    terms=[('linear model', 'a function of the form y = mx + c used when a quantity changes at a constant rate'),
           ('quadratic model', 'a function y = ax² + bx + c used when the rate of change itself changes steadily, e.g. projectile height')],
    why=[('Explain how you can tell from a table of values whether a linear model is appropriate.', 'If equal steps in x give equal differences in y (constant first differences), the relationship is linear.'),
         ('Explain why a quadratic model of profit has a maximum.', 'With a negative x² coefficient the parabola opens downward, so it has a highest point – the price that maximises profit.')],
    misc=[('Because the data points lie close to a line for 0 ≤ x ≤ 10, the model will be accurate for x = 100.', 'Extrapolating far outside the data range is unreliable; the real relationship may change.')],
))


@R.add('ch06-st4', 'C3', (2, 5), 'short')
def model_choose(rng, slot):
    m_, c_ = rng.randint(2, 9), rng.randint(5, 40)
    a_ = rng.randint(1, 4)
    lin = rng.random() < 0.5
    xs = [0, 1, 2, 3, 4]
    ys = [m_ * v + c_ for v in xs] if lin else [a_ * v * v + c_ for v in xs]
    return dict(stem=f'The table shows x = 0, 1, 2, 3, 4 and y = {", ".join(map(str, ys))}. Decide whether a linear or quadratic model fits, find the model, and use it to predict y when x = 6.',
                answer=(f'linear: y = {m_}x + {c_}; y(6) = {6 * m_ + c_}' if lin else f'quadratic: y = {a_}x² + {c_}; y(6) = {36 * a_ + c_}'),
                markingKey=('Constant first differences of ' + str(m_) if lin else f'Constant second differences of {2 * a_}') + ' (R1); model (M1 A1); prediction (A1).', marks=4)


@R.add('ch06-st4', 'C4', (3, 5), 'multi_step')
def model_real(rng, slot):
    who = name(rng)
    fixed, per = rng.randint(200, 900), rng.randint(3, 12)
    price = per + rng.randint(5, 15)
    be = math.ceil(fixed / (price - per))
    frames = [
        (f'{who} starts a T-shirt printing business. Fixed costs are €{fixed} per month and each shirt costs €{per} to make. Shirts sell for €{price}. (a) Write linear models for cost and revenue. (b) Find the break-even number of shirts. (c) Comment on one limitation of the model.', f'C = {fixed} + {per}n, R = {price}n; break-even n = {be}; e.g. costs per shirt may fall with bulk buying'),
        (f'A phone plan A costs ${fixed // 20} plus $0.{per:02d} per minute; plan B costs ${fixed // 10} with unlimited minutes. Model both and find the number of minutes for which plan B becomes cheaper.', f'B cheaper when minutes > {math.floor((fixed // 10 - fixed // 20) / (per / 100)) + 0}'),
    ]
    q, ans = rng.choice(frames)
    return dict(stem=q, answer=ans, markingKey=f'Models written with correct gradient and intercept (M1 A1); solved (M1 A1); limitation or interpretation in context (C1 R1). {ans}', marks=6)


@R.add('ch06-st4', 'C2', (2, 4), 'explain')
def model_explain(rng, slot):
    m_, c_ = rng.randint(2, 9), rng.randint(10, 50)
    q_, ans = rng.choice([
        (f'A plumber charges C = {m_ * 10}h + {c_} dollars for h hours. Explain what {m_ * 10} and {c_} represent in context.', f'{m_ * 10} is the charge per hour (gradient); {c_} is a fixed call-out fee (intercept).'),
        (f'A linear model predicts a plant’s height h = {m_ / 10}t + {c_ // 10} cm after t days. Explain why it should not be used for t = 1000.', 'Plants stop growing at a constant rate; extrapolating so far outside the observed data is unreliable.'),
    ])
    return dict(stem=q_, answer=ans, markingKey=f'{ans} (R1 R1)', type='explain', marks=2)


# =============================================================================================
# ch07 Coordinate Geometry
# =============================================================================================
def _pts(rng, lo=-8, hi=9):
    while True:
        x1, y1, x2, y2 = (rng.randint(lo, hi) for _ in range(4))
        if x1 != x2 and (x1, y1) != (x2, y2):
            return x1, y1, x2, y2


R.facts('ch07-st1', F(
    terms=[('gradient', 'the steepness of a line: change in y divided by the corresponding change in x'),
           ('positive gradient', 'a line that rises from left to right, so y increases as x increases')],
    why=[('Explain why the gradient of a horizontal line is 0.', 'The y-value never changes, so the rise is 0 for any run; 0 ÷ run = 0.'),
         ('Explain why the gradient of a vertical line is undefined.', 'The run (change in x) is 0, and division by zero is undefined.'),
         ('Explain why it does not matter which point you call (x₁, y₁) when finding a gradient.', 'Swapping the points changes the sign of both the rise and the run, so their quotient is unchanged.')],
    misc=[('The gradient from (1, 2) to (4, 11) is (4 − 1)/(11 − 2) = 1/3.', 'Gradient is change in y over change in x: (11 − 2)/(4 − 1) = 3.'),
          ('A steeper line always has a larger gradient.', 'Steepness depends on the size of the gradient; a line with gradient −5 is steeper than one with gradient 2.')],
))


@R.add('ch07-st1', 'C3', (1, 3), 'short')
def grad2(rng, slot):
    x1, y1, x2, y2 = _pts(rng)
    g = Fr(y2 - y1, x2 - x1)
    return dict(stem=f'Find the gradient of the line through ({m(x1)}, {m(y1)}) and ({m(x2)}, {m(y2)}).', answer=m(frac(g)),
                markingKey=f'({m(y2)} − {m(y1)})/({m(x2)} − {m(x1)}) (M1) = {m(frac(g))} (A1).'.replace('− −', '+ '), marks=2)


@R.add('ch07-st1', 'C1', (1, 2), 'mcq')
def grad_mcq(rng, slot):
    x1, y1, x2, y2 = _pts(rng, 0, 9)
    g = Fr(y2 - y1, x2 - x1)
    w = [frac(1 / g) if g != 0 else '1', frac(-g) if g != 0 else '−1', frac(Fr(y2 + y1, x2 + x1)) if x1 + x2 else '2']
    return mcq(rng, f'What is the gradient of the line joining A({x1}, {y1}) and B({x2}, {y2})?', frac(g), w, f'(y₂ − y₁)/(x₂ − x₁) = {frac(g)}.')


@R.add('ch07-st1', 'C3', (2, 4), 'short')
def grad_unknown(rng, slot):
    x1, y1 = rng.randint(-5, 5), rng.randint(-5, 5)
    g = rng.choice([2, 3, -2, -1, Fr(1, 2), Fr(-3, 2)])
    dx = rng.choice([2, 4, 6])
    y2 = y1 + g * dx
    return dict(stem=f'The line through ({m(x1)}, {m(y1)}) and ({m(x1 + dx)}, k) has gradient {m(frac(g))}. Find k.', answer=f'k = {m(frac(y2))}',
                markingKey=f'(k − {m(y1)})/{dx} = {m(frac(g))} (M1); k = {m(frac(y2))} (A1).'.replace('− −', '+ '), marks=2)


@R.add('ch07-st1', 'C4', (3, 5), 'multi_step')
def grad_context(rng, slot):
    who = name(rng)
    h1, h2, d = rng.randint(100, 400), rng.randint(450, 900), rng.randint(2, 8) * 500
    rate = rng.choice([12, 15, 18, 20, 25])
    frames = [
        (f'A hiking trail climbs from an altitude of {h1} m to {h2} m over a horizontal distance of {d} m. (a) Find the average gradient. (b) Paths steeper than 0.15 need steps. Decide whether this path needs steps.', f'{(h2 - h1) / d:.3g}; {"yes" if (h2 - h1) / d > 0.15 else "no"}'),
        (f'{who}’s phone battery is at 92% at 08:00 and 92 − {rate}t% after t hours of use. Interpret the gradient and find when the battery reaches 20%.', f'−{rate}% per hour; after {72 / rate:.2g} hours'),
        (f'Three points A(1, 2), B(4, {2 + 3 * rate % 7 + 3}) and C(10, {2 + 3 * (rate % 7 + 1) * 3}) are given. Use gradients to decide whether A, B and C are collinear.', None),
    ]
    q, ans = rng.choice(frames)
    if ans is None:
        k = rate % 7 + 1
        yb, yc = 2 + 3 * k, 2 + 9 * k + rng.choice([0, 0, 1])
        g1, g2 = Fr(yb - 2, 3), Fr(yc - 2, 9)
        q = f'Three points A(1, 2), B(4, {yb}) and C(10, {yc}) are given. Use gradients to decide whether A, B and C lie on a straight line.'
        ans = f'm(AB) = {frac(g1)}, m(AC) = {frac(g2)}: {"collinear" if g1 == g2 else "not collinear"}'
    return dict(stem=q, answer=ans, markingKey=f'Gradient(s) calculated correctly (M1 A1); interpreted/compared in context (R1); conclusion {ans} (A1).', marks=4)


R.facts('ch07-st2', F(
    terms=[('gradient-intercept form', 'the equation y = mx + c, where m is the gradient and c the y-intercept'),
           ('general form of a line', 'the equation ax + by + d = 0 with integer a, b, d'),
           ('y-intercept', 'the point where a graph crosses the y-axis, where x = 0')],
    why=[('Explain how you can read the gradient and y-intercept from y = 3x − 7.', 'Comparing with y = mx + c: m = 3 and c = −7, so it rises 3 for every 1 across and crosses the y-axis at (0, −7).'),
         ('Explain why you must rearrange 2x + 3y = 6 before reading off the gradient.', 'Only in the form y = mx + c is the x-coefficient the gradient; rearranging gives y = −(2/3)x + 2, so m = −2/3, not 2.')],
    misc=[('The line 4x + 2y = 8 has gradient 4.', 'Rearrange: y = −2x + 4, so the gradient is −2.'),
          ('y = 5 is the equation of a vertical line.', 'y = 5 is horizontal (every point has y = 5); a vertical line has equation x = k.')],
))


@R.add('ch07-st2', 'C3', (1, 4), 'short')
def line_eq(rng, slot):
    x1, y1, x2, y2 = _pts(rng)
    g = Fr(y2 - y1, x2 - x1)
    c = y1 - g * x1
    ans = f'y = {m(frac(g))}x {"+" if c >= 0 else "−"} {frac(abs(c))}'
    if slot.d >= 3:
        L = g.denominator * c.denominator // math.gcd(g.denominator, c.denominator)
        a_, b_, d_ = int(-g * L), L, int(-c * L)
        if a_ < 0:
            a_, b_, d_ = -a_, -b_, -d_
        gen = f'{a_}x {"+" if b_ > 0 else "−"} {abs(b_)}y {"+" if d_ >= 0 else "−"} {abs(d_)} = 0'
        return dict(stem=f'Find the equation of the line through ({m(x1)}, {m(y1)}) and ({m(x2)}, {m(y2)}) in the form ax + by + d = 0, where a, b and d are integers.', answer=gen,
                    markingKey=f'Gradient {m(frac(g))} (A1); substitute a point (M1); {ans} (A1); rearranged to {gen} (A1).', marks=4)
    return dict(stem=f'Find the equation of the line through ({m(x1)}, {m(y1)}) and ({m(x2)}, {m(y2)}) in the form y = mx + c.', answer=ans,
                markingKey=f'Gradient {m(frac(g))} (A1); c found by substitution (M1); {ans} (A1).', marks=3)


@R.add('ch07-st2', 'C1', (1, 3), 'mcq')
def line_read_mcq(rng, slot):
    a, b, d_ = rng.randint(1, 6), rng.choice([2, 3, 4, 5]), rng.randint(-12, 12)
    g = Fr(-a, b)
    return mcq(rng, f'What is the gradient of the line {a}x + {b}y {"+" if d_ >= 0 else "−"} {abs(d_)} = 0?', m(frac(g)), [str(a), m(frac(Fr(b, a))), frac(Fr(a, b))],
               f'Rearrange: y = {m(frac(g))}x + …, so m = {m(frac(g))}.')


@R.add('ch07-st2', 'C4', (3, 5), 'multi_step')
def line_context(rng, slot):
    who = name(rng)
    v0, r = rng.randint(30, 80), rng.randint(2, 6)
    t1, t2 = 2, rng.randint(5, 9)
    frames = [
        (f'A water tank holds {v0 + r * t1} litres after {t1} minutes of filling and {v0 + r * t2} litres after {t2} minutes. Assuming a constant rate, find the equation linking volume V and time t, and state what the intercept means.', f'V = {r}t + {v0}; {v0} L were already in the tank'),
        (f'{who} records a candle’s height: {v0 / 2:g} cm at t = {t1} h and {v0 / 2 - 0.5 * r * (t2 - t1):g} cm at t = {t2} h. Find the linear model h = mt + c and predict when the candle burns out.', f'h = {m(-0.5 * r)}t + {v0 / 2 + 0.5 * r * t1:g}; burns out at t = {(v0 / 2 + 0.5 * r * t1) / (0.5 * r):.3g} h'),
    ]
    q, ans = rng.choice(frames)
    return dict(stem=q, answer=ans, markingKey=f'Gradient as a rate with units (M1 A1); intercept found (A1); interpretation/prediction in context (R1 A1). {ans}', marks=5)


@R.add('ch07-st2', 'C2', (2, 4), 'explain')
def line_explain(rng, slot):
    m_, c_ = rng.randint(-5, 6), rng.randint(-9, 9)
    if m_ == 0:
        return None
    px = rng.randint(-4, 5)
    on = rng.random() < 0.5
    py = m_ * px + c_ + (0 if on else rng.choice([1, -2, 3]))
    return dict(stem=f'Explain how to decide whether the point ({m(px)}, {m(py)}) lies on the line y = {_lin(m_, c_)}, and decide.', answer='Yes' if on else 'No',
                markingKey=f'Substitute x = {m(px)}: y = {m(m_ * px + c_)} (M1); compare with {m(py)} (R1): {"on the line" if on else "not on the line"} (A1).', type='explain', marks=3)


R.facts('ch07-st3', F(
    terms=[('parallel lines', 'lines in the same plane that never meet; they have equal gradients'),
           ('perpendicular lines', 'lines that meet at a right angle; their gradients multiply to −1 (for non-vertical lines)'),
           ('negative reciprocal', 'for a gradient m, the value −1/m, which is the gradient of a perpendicular line')],
    why=[('Explain why parallel lines must have the same gradient.', 'If the gradients differed, one line would rise faster than the other, so the gap between them would change and they would eventually meet.'),
         ('Explain, using a rotation of 90°, why perpendicular gradients multiply to −1.', 'Rotating a step "a across, b up" by 90° gives "b back, a up", so the gradients are b/a and −a/b, whose product is −1.')],
    misc=[('A line perpendicular to y = 2x + 1 has gradient −2.', 'The perpendicular gradient is the negative reciprocal: −1/2.'),
          ('y = 3x + 2 and y = 2x + 3 are parallel because they use the same numbers.', 'Parallel lines need equal gradients; here the gradients are 3 and 2.')],
))


@R.add('ch07-st3', 'C3', (1, 4), 'short')
def perp_line(rng, slot):
    g = rng.choice([2, 3, -2, Fr(1, 2), Fr(-1, 3), Fr(2, 3), 4, -1])
    px, py = rng.randint(-6, 6), rng.randint(-6, 6)
    kind = rng.choice(['parallel', 'perpendicular'])
    gg = g if kind == 'parallel' else -1 / Fr(g)
    c = py - gg * px
    return dict(stem=f'Find the equation of the line {kind} to y = {m(frac(Fr(g)))}x + 5 that passes through ({m(px)}, {m(py)}).', answer=f'y = {m(frac(gg))}x {"+" if c >= 0 else "−"} {frac(abs(c))}',
                markingKey=f'Gradient {m(frac(gg))} ({"equal" if kind == "parallel" else "negative reciprocal"}) (M1 A1); substitute point to find c = {m(frac(c))} (A1).', marks=3)


@R.add('ch07-st3', 'C1', (1, 3), 'mcq')
def perp_mcq(rng, slot):
    g = rng.choice([2, 3, 4, 5, Fr(1, 2), Fr(2, 3), Fr(3, 4), Fr(-2, 5)])
    g = Fr(g)
    return mcq(rng, f'A line has gradient {m(frac(g))}. What is the gradient of a line perpendicular to it?', m(frac(-1 / g)), [m(frac(1 / g)), m(frac(-g)), m(frac(g))],
               f'Perpendicular gradients multiply to −1: {m(frac(g))} × {m(frac(-1 / g))} = −1.')


@R.add('ch07-st3', 'C4', (3, 5), 'multi_step')
def perp_shape(rng, slot):
    a, b = rng.randint(1, 5), rng.randint(1, 5)
    ox, oy = rng.randint(-3, 3), rng.randint(-3, 3)
    A = (ox, oy)
    B = (ox + a, oy + b)
    C = (ox + a - b, oy + b + a)
    D = (ox - b, oy + a)
    shape = rng.choice(['square', 'rect'])
    if shape == 'rect':
        k = 2
        C = (ox + a - k * b, oy + b + k * a)
        D = (ox - k * b, oy + k * a)
    q = f'The points A{A}, B{B}, C{C} and D{D} form a quadrilateral. Use gradients to show that it is a {"square" if shape == "square" else "rectangle"} or explain why more information is needed.'.replace('(', '(').replace(', ', ', ')
    return dict(stem=q.replace('-', '−'), answer=f'm(AB) = {frac(Fr(b, a))}, m(BC) = {frac(Fr(-a, b))}: perpendicular; opposite sides parallel' + ('; equal side lengths → square' if shape == 'square' else '; adjacent sides unequal → rectangle'),
                markingKey='All four gradients found (M1 A1); product of adjacent gradients −1 → right angles (R1); opposite gradients equal → parallel (R1); lengths compared for square vs rectangle (A1).', marks=5, gap='G5')


@R.add('ch07-st3', 'C2', (2, 4), 'explain')
def perp_explain(rng, slot):
    a, b = rng.randint(1, 6), rng.randint(1, 6)
    return dict(stem=f'Explain whether the lines {a}x + {b}y = 7 and {b}x − {a}y = 2 are parallel, perpendicular or neither.', answer='perpendicular',
                markingKey=f'Gradients −{a}/{b} and {b}/{a} (M1 A1); product = −1 so perpendicular (R1).', type='explain', marks=3)


R.facts('ch07-st4', F(
    terms=[('midpoint', 'the point exactly halfway between two points, ((x₁ + x₂)/2, (y₁ + y₂)/2)'),
           ('distance formula', 'd = √((x₂ − x₁)² + (y₂ − y₁)²), which comes from Pythagoras’ theorem')],
    why=[('Explain why the distance formula is an application of Pythagoras’ theorem.', 'The horizontal and vertical changes form the two legs of a right-angled triangle whose hypotenuse is the segment.'),
         ('Explain why the midpoint is found by averaging coordinates.', 'Halfway along means half the change in x and half the change in y from the first point, which equals the mean of the coordinates.')],
    misc=[('The distance between (1, 2) and (4, 6) is (4 − 1) + (6 − 2) = 7.', 'Use Pythagoras: √(3² + 4²) = 5.'),
          ('The midpoint of (2, 8) and (6, 4) is (4, 4) because you subtract and halve.', 'Add and halve: ((2 + 6)/2, (8 + 4)/2) = (4, 6).')],
))


@R.add('ch07-st4', 'C3', (1, 3), 'short')
def mid_dist(rng, slot):
    x1, y1 = rng.randint(-6, 6), rng.randint(-6, 6)
    a, b = rng.choice([(3, 4), (5, 12), (6, 8), (8, 15), (1, 2), (2, 3), (4, 4), (7, 24), (2, 5)])
    x2, y2 = x1 + a * rng.choice([1, -1]), y1 + b * rng.choice([1, -1])
    d = math.sqrt(a * a + b * b)
    ds = str(int(d)) if d.is_integer() else f'√{a * a + b * b} ≈ {d:.3g}'
    return dict(stem=f'For A({m(x1)}, {m(y1)}) and B({m(x2)}, {m(y2)}), find the midpoint of AB and the length AB.', answer=f'({m(frac(Fr(x1 + x2, 2)))}, {m(frac(Fr(y1 + y2, 2)))}); {ds}',
                markingKey=f'Midpoint ({m(frac(Fr(x1 + x2, 2)))}, {m(frac(Fr(y1 + y2, 2)))}) (A1); distance √({a}² + {b}²) (M1) = {ds} (A1).', marks=3)


@R.add('ch07-st4', 'C3', (2, 4), 'short')
def mid_reverse(rng, slot):
    x1, y1, mx, my = rng.randint(-6, 6), rng.randint(-6, 6), rng.randint(-6, 6), rng.randint(-6, 6)
    return dict(stem=f'M({m(mx)}, {m(my)}) is the midpoint of PQ, where P is ({m(x1)}, {m(y1)}). Find the coordinates of Q.', answer=f'({m(2 * mx - x1)}, {m(2 * my - y1)})',
                markingKey=f'(x + {m(x1)})/2 = {m(mx)} and (y + {m(y1)})/2 = {m(my)} (M1); Q({m(2 * mx - x1)}, {m(2 * my - y1)}) (A1 A1).'.replace('+ −', '− '), marks=3)


@R.add('ch07-st4', 'C4', (3, 5), 'multi_step')
def dist_triangle(rng, slot):
    a, b = rng.choice([(3, 4), (6, 8), (5, 12), (2, 2)])
    ox, oy = rng.randint(-4, 4), rng.randint(-4, 4)
    A, B, C = (ox, oy), (ox + a, oy + b), (ox + 2 * a, oy)
    ab = math.sqrt(a * a + b * b)
    frames = [
        (f'Show that the triangle with vertices A{A}, B{B} and C{C} is isosceles, and find its perimeter and area.', f'AB = BC = {ab:g}, AC = {2 * a}; perimeter {2 * ab + 2 * a:g}; area {a * b}'),
        (f'A delivery drone flies from depot A{A} to B{B} and then to C{C} (units in km). Find the total distance flown and how much shorter the direct route A to C is.', f'{2 * ab:g} km; {2 * ab - 2 * a:g} km shorter'),
    ]
    q, ans = rng.choice(frames)
    return dict(stem=q.replace('-', '−'), answer=ans, markingKey=f'Distance formula applied to each side (M1 A1 A1); conclusion/area or comparison (A1 R1). {ans}', marks=5)


@R.add('ch07-st4', 'C2', (2, 4), 'explain')
def dist_explain(rng, slot):
    a, b = rng.randint(1, 9), rng.randint(1, 9)
    return dict(stem=f'{name(rng)} says the distance from (0, 0) to ({a}, {b}) is the same as the distance from (0, 0) to ({b}, {a}). Explain why this is true.', answer='True',
                markingKey=f'Both are √({a}² + {b}²) (M1); the squares are added so order does not matter / reflection in y = x preserves distance (R1).', type='explain', marks=2)


@R.add('ch07-st1', 'C2', (2, 4), 'explain')
def grad_explain(rng, slot):
    x1, y1, x2, y2 = _pts(rng, -5, 8)
    g = Fr(y2 - y1, x2 - x1)
    q_, ans = rng.choice([
        (f'Explain what the gradient {m(frac(g))} of the line through ({m(x1)}, {m(y1)}) and ({m(x2)}, {m(y2)}) tells you about how y changes with x.', f'For every 1 unit increase in x, y {"increases" if g > 0 else "decreases" if g < 0 else "does not change"} by {frac(abs(g))}.'),
        (f'Explain why the line through ({m(x1)}, {m(y1)}) and ({m(x2)}, {m(y2)}) has a {"positive" if g > 0 else "negative" if g < 0 else "zero"} gradient without calculating it.', 'Compare the direction: as x increases from the left point to the right point, y ' + ('rises.' if g > 0 else 'falls.' if g < 0 else 'stays the same.')),
        (f'{name(rng)} calculates the gradient through ({m(x1)}, {m(y1)}) and ({m(x2)}, {m(y2)}) as {m(frac(1 / g)) if g else "undefined"}. Explain the likely error.', 'They divided the change in x by the change in y; gradient is rise over run, (y₂ − y₁)/(x₂ − x₁) = ' + m(frac(g)) + '.'),
    ])
    if 'undefined' in q_:
        return None
    return dict(stem=q_.replace('− −', '+ '), answer=ans, markingKey=f'{ans} (R1 A1)', type='explain', marks=2)


@R.add('ch06-st1', 'C2', (2, 4), 'explain')
def func_explain(rng, slot):
    k = rng.randint(2, 9)
    q_, ans = rng.choice([
        (f'Explain why y² = {k}x does not define y as a function of x.', f'For x = {k}, y² = {k * k} gives y = {k} or y = −{k}: one input, two outputs.'),
        (f'Explain why f(x) = 1/(x − {k}) has a restricted domain and state it.', f'Division by zero is undefined at x = {k}; domain x ∈ ℝ, x ≠ {k}.'),
        (f'Explain why f(x) = (x − {k})² can never output a negative value.', 'A square of a real number is never negative, so f(x) ≥ 0.'),
        (f'Explain why the relation "each student in a class → their age" is a function but "each age → the students of that age" is not.', 'Each student has exactly one age (function); an age can map to several students (one-to-many, not a function).'),
    ])
    return dict(stem=q_, answer=ans, markingKey=f'{ans} (R1 A1)', type='explain', marks=2)


@R.add('ch01-st4', 'C4', (3, 5), 'multi_step')
def rat_geom(rng, slot):
    r = rng.choice([2, 3, 5, 6])
    a = rng.randint(2, 9)
    frames = [
        (f'A rectangle has area {a} cm² and length √{r} cm. Find the width, rationalising the denominator, and show that the perimeter is {frac(Fr(2 * a, r)) if False else ""}'.rstrip() + f' 2√{r}(1 + {frac(Fr(a, r))}) cm.', f'width {a}√{r}/{r} cm'),
        (f'A right-angled triangle has legs 1/√{r} and 1/(√{r} + 1). Find its area in rationalised form.', f'(√{r} − 1)/({2 * r} − 2√{r})·… = (√{r}·(√{r} − 1))/(2·{r}·({r} − 1))'),
        (f'Simplify (√{r} + 1)/(√{r} − 1), writing your answer in the form p + q√{r}.', f'{frac(Fr(r + 1, r - 1))} + {frac(Fr(2, r - 1))}√{r}'),
        (f'Show that {a}/(√{r + 1} − √{r}) = {a}(√{r + 1} + √{r}).', f'Denominator ({r + 1}) − {r} = 1 after multiplying by the conjugate'),
    ]
    q_, ans = rng.choice(frames[2:])
    return dict(stem=q_, answer=ans, markingKey=f'Multiply by the conjugate (M1); difference of squares in the denominator (A1); expand numerator (M1); simplified result {ans} (A1).', marks=4, gap='G5')


# =============================================================================================
# ch08 Similarity and Congruence
# =============================================================================================
R.facts('ch08-st1', F(
    terms=[('congruent', 'identical in shape and size; one figure maps exactly onto the other'),
           ('SAS', 'two sides and the included angle of one triangle equal two sides and the included angle of another'),
           ('RHS', 'right angle, hypotenuse and one other side equal – a congruence test for right-angled triangles'),
           ('ASA', 'two angles and the side between them equal in both triangles')],
    facts=[('Which of these is NOT a valid congruence test for triangles?', 'AAA', ['SSS', 'SAS', 'RHS'], 'AAA only proves similarity: triangles can have equal angles but different sizes.'),
           ('Which condition proves two right-angled triangles congruent using RHS?', 'equal hypotenuses and one equal pair of other sides', ['equal hypotenuses only', 'two equal acute angles', 'equal areas'], 'RHS needs the right angle, the hypotenuse and one other side.')],
    why=[('Explain why SSA (two sides and a non-included angle) is not a congruence test.', 'The third side can swing to two different positions, giving two different triangles with the same SSA data (the ambiguous case).'),
         ('Explain why AAA is not a congruence test.', 'Equal angles fix the shape but not the size: an enlargement keeps all angles but changes the sides.'),
         ('Explain why corresponding parts of congruent triangles are equal.', 'Congruent triangles map exactly onto each other, so every matching side and angle coincides.')],
    misc=[('Two triangles with three equal angles must be congruent.', 'They are similar but may differ in size; congruence needs at least one pair of equal sides as well (ASA/AAS).'),
          ('In SAS the angle can be any angle of the triangle.', 'The angle must be the included angle, between the two given sides.')],
))


@R.add('ch08-st1', 'C3', (1, 3), 'short')
def cong_identify(rng, slot):
    a, b = rng.randint(4, 12), rng.randint(4, 12)
    ang = rng.choice([35, 40, 48, 55, 62, 70, 75])
    cases = [
        (f'Triangle ABC has AB = {a} cm, BC = {b} cm and angle ABC = {ang}°. Triangle PQR has PQ = {a} cm, QR = {b} cm and angle PQR = {ang}°. State whether they are congruent and the test used.', 'congruent (SAS)'),
        (f'Triangles XYZ and LMN both have a right angle; XZ = LN = {max(a, b) + 3} cm are the hypotenuses and XY = LM = {min(a, b)} cm. Are they congruent? Name the test.', 'congruent (RHS)'),
        (f'Triangle ABC has angles {ang}°, {90 - ang // 2}° and {90 + ang // 2 - ang}°; triangle DEF has the same three angles. Can you conclude that they are congruent?', 'not necessarily – AAA proves similarity only'),
        (f'Triangle ABC has sides {a}, {b} and {a + b - 2} cm; triangle DEF has sides {b}, {a + b - 2} and {a} cm. Are they congruent? Name the test.', 'congruent (SSS)'),
        (f'In triangles ABC and DEF, angle A = angle D = {ang}°, angle B = angle E = {ang + 20}° and AB = DE = {a} cm. Are they congruent? Name the test.', 'congruent (ASA)'),
    ]
    q_, ans = rng.choice(cases)
    return dict(stem=q_, answer=ans, markingKey=f'{ans} (A1); correct matching of corresponding parts stated (R1).', marks=2)


@R.add('ch08-st1', 'C4', (3, 5), 'multi_step')
def cong_proof(rng, slot):
    q_, ans = rng.choice([
        ('ABCD is a parallelogram with diagonal AC. Prove that triangles ABC and CDA are congruent, and hence that opposite angles B and D are equal.', 'AB = CD and BC = DA (opposite sides of a parallelogram), AC common → SSS; corresponding angles B = D.'),
        ('M is the midpoint of AB and of CD (segments AB and CD cross at M). Prove that triangle AMC is congruent to triangle BMD and hence that AC is parallel to DB.', 'AM = MB, CM = MD, vertically opposite angles at M → SAS; so angle CAM = angle DBM (alternate angles) → AC ∥ DB.'),
        ('In isosceles triangle PQR, PQ = PR and S is the midpoint of QR. Prove that PS is perpendicular to QR.', 'PQ = PR, QS = SR, PS common → SSS; angles PSQ = PSR and they sum to 180°, so each is 90°.'),
        ('A kite ABCD has AB = AD and CB = CD. Prove that the diagonal AC bisects angle BAD.', 'AB = AD, CB = CD, AC common → triangles ABC ≅ ADC (SSS); so angle BAC = angle DAC.'),
        ('Two straight roads AB and CD of equal length cross at their common midpoint O. Prove that AC = BD.', 'AO = OB, CO = OD, vertically opposite angles AOC = BOD → SAS, so AC = BD.'),
    ])
    return dict(stem=q_, answer=ans, markingKey=f'Three correct pairs of equal parts with reasons (M1 M1 M1); correct test named (A1); conclusion from corresponding parts (R1). {ans}', marks=5, gap='G5')


@R.add('ch08-st1', 'C2', (2, 4), 'explain')
def cong_explain(rng, slot):
    a, b = rng.randint(5, 12), rng.randint(5, 12)
    ang = rng.choice([30, 40, 50])
    return dict(stem=f'{name(rng)} says two triangles with sides {a} cm and {b} cm and a {ang}° angle (not between those sides) must be congruent. Explain why this is not necessarily true.', answer='SSA is not a congruence test',
                markingKey='The angle is not included, so the third side can take two positions (ambiguous case) (R1); a sketch or example of two different triangles (R1).', type='explain', marks=2)


R.facts('ch08-st2', F(
    terms=[('similar figures', 'figures with the same shape: corresponding angles equal and corresponding sides in the same ratio'),
           ('scale factor', 'the ratio of a length in the image to the corresponding length in the original')],
    why=[('Explain why two triangles with two pairs of equal angles must be similar.', 'The third angles are then equal too (angle sum 180°), so all angles match (AA), which fixes the shape.'),
         ('Explain why you must match corresponding vertices when writing a similarity ratio.', 'The ratio compares sides opposite equal angles; pairing the wrong sides gives a wrong scale factor.')],
    misc=[('If triangle B has sides 3 cm longer than triangle A, they are similar.', 'Similarity needs sides in the same ratio (multiplied by the same factor), not increased by the same amount.'),
          ('All rectangles are similar because their angles are all 90°.', 'Equal angles are not enough for rectangles; the side ratios must also match (a 1 × 2 and a 1 × 3 rectangle are not similar).')],
))


@R.add('ch08-st2', 'C3', (1, 4), 'short')
def sim_side(rng, slot):
    a, b, c = rng.randint(3, 9), rng.randint(4, 12), rng.randint(5, 14)
    k = rng.choice([Fr(3, 2), Fr(2), Fr(5, 2), Fr(4, 3), Fr(3)])
    q_ = f'Triangles ABC and PQR are similar with AB = {a} cm, BC = {b} cm, AC = {c} cm and PQ = {frac(a * k)} cm (P↔A, Q↔B, R↔C). Find QR and PR.'
    return dict(stem=q_, answer=f'QR = {float(b * k):g} cm, PR = {float(c * k):g} cm',
                markingKey=f'Scale factor {frac(a * k)}/{a} = {frac(k)} (M1); QR = {float(b * k):g} cm (A1); PR = {float(c * k):g} cm (A1).', marks=3)


@R.add('ch08-st2', 'C3', (2, 5), 'short')
def sim_shadow(rng, slot):
    who = name(rng)
    h, s1 = rng.choice([1.5, 1.6, 1.7, 1.8]), rng.choice([1.2, 2.0, 2.4, 2.5, 3.0])
    S = rng.randint(6, 30)
    frames = [
        (f'{who}, who is {h} m tall, casts a shadow {s1} m long. At the same time a tree casts a shadow {S} m long. How tall is the tree?', f'{h * S / s1:.3g} m'),
        (f'A flagpole’s shadow is {S} m long when a {h} m post nearby casts a {s1} m shadow. Find the height of the flagpole.', f'{h * S / s1:.3g} m'),
        (f'To estimate the width of a river, {who} uses similar triangles: a 4 m baseline on the near bank corresponds to a {S * 2} m stretch, and a {s1} m sight line corresponds to the river width. Find the width.', f'{s1 * S * 2 / 4:.3g} m'),
    ]
    q_, ans = rng.choice(frames)
    return dict(stem=q_, answer=ans, markingKey=f'Similar triangles identified (R1); correct ratio set up (M1); {ans} (A1).', marks=3, gap='G7')


@R.add('ch08-st2', 'C4', (3, 5), 'multi_step')
def sim_parallel(rng, slot):
    a, b, c = rng.randint(3, 8), rng.randint(2, 6), rng.randint(4, 10)
    # triangle with DE parallel to BC: AD = a, DB = b, DE = c -> BC = c*(a+b)/a
    BC = Fr(c * (a + b), a)
    return dict(stem=f'In triangle ABC, D lies on AB and E lies on AC with DE parallel to BC. AD = {a} cm, DB = {b} cm and DE = {c} cm. (a) Prove that triangles ADE and ABC are similar. (b) Find BC. (c) Find the ratio of the area of ADE to the area of ABC.',
                answer=f'(b) BC = {float(BC):.3g} cm (c) {a * a} : {(a + b) ** 2}',
                markingKey=f'(a) angle A common; corresponding angles ADE = ABC (DE ∥ BC) → AA (R1 R1). (b) BC/DE = {a + b}/{a} (M1) → {float(BC):.3g} cm (A1). (c) area ratio = (length ratio)² = {a * a}:{(a + b) ** 2} (A1).', marks=5, gap='G5')


@R.add('ch08-st2', 'C2', (2, 4), 'explain')
def sim_explain(rng, slot):
    a, b = rng.randint(2, 6), rng.randint(7, 12)
    k = rng.randint(2, 4)
    return dict(stem=f'Rectangle A is {a} cm by {b} cm and rectangle B is {a * k} cm by {b + a * k - a} cm. Explain whether the rectangles are similar.', answer='similar' if (b + a * k - a) == b * k else 'not similar',
                markingKey=f'Compare ratios: {a * k}/{a} = {k} and {b + a * k - a}/{b} = {frac(Fr(b + a * k - a, b))} (M1); {"equal so similar" if (b + a * k - a) == b * k else "not equal so not similar"} (R1).', type='explain', marks=2)


R.facts('ch08-st3', F(
    terms=[('area scale factor', 'the square of the length scale factor, k², by which areas are multiplied in an enlargement'),
           ('volume scale factor', 'the cube of the length scale factor, k³, by which volumes are multiplied')],
    why=[('Explain why doubling the side of a square multiplies its area by 4.', 'Area = side × side, and both factors double, so area is multiplied by 2 × 2 = 4.'),
         ('Explain why a model car at scale 1:20 needs 8000 times less paint volume… no – 400 times less paint (area).', 'Paint covers surface area, which scales by k² = 20² = 400.')],
    misc=[('If two similar cylinders have heights in the ratio 1 : 3, their volumes are in the ratio 1 : 3.', 'Volumes scale by k³: 1 : 27.'),
          ('A photo enlarged to twice the width uses twice as much paper.', 'Both width and height double, so the area is 4 times as large.')],
))
R.f['ch08-st3'].why[1] = ('Explain why a 1:20 scale model of a car needs 400 times less paint than the real car.', 'Paint covers surface area, which scales by the square of the length factor: 20² = 400.')


@R.add('ch08-st3', 'C3', (1, 4), 'short')
def area_vol_ratio(rng, slot):
    a, b = rng.choice([(1, 2), (2, 3), (3, 4), (2, 5), (3, 5), (1, 3), (4, 5)])
    kind = rng.choice(['area', 'volume', 'length_from_area', 'length_from_volume'])
    A = rng.randint(10, 90)
    if kind == 'area':
        return dict(stem=f'Two similar shapes have lengths in the ratio {a} : {b}. The smaller has area {A} cm². Find the area of the larger.', answer=f'{A * b * b / (a * a):.4g} cm²',
                    markingKey=f'Area factor ({b}/{a})² = {frac(Fr(b * b, a * a))} (M1); {A * b * b / (a * a):.4g} cm² (A1).', marks=2)
    if kind == 'volume':
        return dict(stem=f'Two similar bottles have heights {a * 6} cm and {b * 6} cm. The smaller holds {A * 10} ml. How much does the larger hold?', answer=f'{A * 10 * b ** 3 / a ** 3:.4g} ml',
                    markingKey=f'Length factor {b}/{a}; volume factor ({b}/{a})³ = {frac(Fr(b ** 3, a ** 3))} (M1 A1); {A * 10 * b ** 3 / a ** 3:.4g} ml (A1).', marks=3)
    if kind == 'length_from_area':
        return dict(stem=f'Two similar triangles have areas {a * a * 4} cm² and {b * b * 4} cm². The shorter base is {a * 3} cm. Find the longer base.', answer=f'{b * 3} cm',
                    markingKey=f'Length factor √({b * b * 4}/{a * a * 4}) = {b}/{a} (M1 A1); {b * 3} cm (A1).', marks=3)
    return dict(stem=f'Two similar solid statues have masses {a ** 3 * 2} kg and {b ** 3 * 2} kg. The smaller is {a * 20} cm tall. How tall is the larger?', answer=f'{b * 20} cm',
                markingKey=f'Mass ∝ volume: factor {b ** 3}/{a ** 3}; length factor ∛ = {b}/{a} (M1 A1); {b * 20} cm (A1).', marks=3)


@R.add('ch08-st3', 'C4', (3, 5), 'multi_step')
def area_vol_context(rng, slot):
    k = rng.choice([2, 3, Fr(3, 2), Fr(5, 2)])
    k = Fr(k)
    p = rng.randint(4, 15)
    frames = [
        (f'A small tin of paint covers {p} m² and is {frac(10 * 1)} cm tall. A similar large tin is {frac(10 * k)} cm tall. (a) How much paint (by volume) does the large tin hold compared with the small? (b) If the small tin costs €{p}, explain whether a price of €{float(p * k ** 2):g} for the large tin is good value.', f'(a) {frac(k ** 3)} times (b) yes – you get {frac(k ** 3)}× the paint for {frac(k ** 2)}× the price'),
        (f'A pizza of diameter 20 cm costs ${p}. A similar pizza of diameter {float(20 * k):g} cm costs ${float(p * k * 1.5):g}. Which is better value per cm²? Show your reasoning.', None),
    ]
    q_, ans = rng.choice(frames)
    if ans is None:
        small = p / (math.pi * 100)
        big = float(p * k * Fr(3, 2)) / (math.pi * float(10 * k) ** 2)
        ans = f'{"large" if big < small else "small"} pizza: ${small * 100:.3g} vs ${big * 100:.3g} per 100 cm²'
    return dict(stem=q_, answer=ans, markingKey=f'Correct scale factor for length (A1); squared for area / cubed for volume (M1 A1); comparison per unit with conclusion (R1 C1). {ans}', marks=5)


@R.add('ch08-st3', 'C2', (2, 4), 'explain')
def area_vol_explain(rng, slot):
    k = rng.randint(2, 5)
    return dict(stem=f'A cube is enlarged by scale factor {k}. {name(rng)} says its surface area and volume are both multiplied by {k}. Explain why this is wrong and give the correct factors.', answer=f'area × {k * k}, volume × {k ** 3}',
                markingKey=f'Area involves two lengths → k² = {k * k} (R1); volume three lengths → k³ = {k ** 3} (R1).', type='explain', marks=2)


R.facts('ch08-st4', F(
    terms=[('proof', 'a logical argument in which each step follows from definitions, given facts or previously proven results'),
           ('corresponding parts', 'matching sides and angles of congruent or similar figures')],
    why=[('Explain why each statement in a geometric proof needs a reason.', 'A reason (e.g. "alternate angles, parallel lines") shows the step follows from an accepted fact, so the argument is valid for every case, not just a drawing.'),
         ('Explain why a measured diagram cannot prove a geometric result.', 'Measurements have errors and only test one case; a proof must hold for all figures meeting the conditions.')],
    misc=[('The diagram shows the angles look equal, so they are equal.', 'Appearance is not proof; equality must follow from a reason such as congruence or parallel-line angle facts.')],
))


@R.add('ch08-st4', 'C4', (2, 5), 'multi_step')
def proof_more(rng, slot):
    q_, ans = rng.choice([
        ('Prove that the diagonals of a parallelogram bisect each other.', 'Triangles formed by the diagonals: alternate angles equal (parallel sides), opposite sides equal → ASA congruence, so the halves of each diagonal are equal.'),
        ('In triangle ABC, the line through the midpoint M of AB parallel to BC meets AC at N. Prove that N is the midpoint of AC.', 'Triangles AMN and ABC are similar (corresponding angles) with ratio AM/AB = 1/2, so AN = AC/2.'),
        ('Prove that the base angles of an isosceles triangle are equal.', 'Draw the bisector of the apex angle; SAS gives two congruent triangles, so the base angles correspond and are equal.'),
        ('ABCD is a square. E is a point on BC and F a point on CD with BE = CF. Prove that AE = BF.', 'AB = BC, angle ABE = angle BCF = 90°, BE = CF → SAS, so AE = BF.'),
        ('Prove that in a right-angled triangle the altitude to the hypotenuse creates two triangles similar to the original.', 'Each small triangle shares an acute angle with the original and has a right angle → AA similarity.'),
    ])
    return dict(stem=q_, answer=ans, markingKey=f'Correct pairs of equal angles/sides with reasons (M1 M1); valid test named (A1); conclusion stated (R1); logical communication (C1). {ans}', marks=5, gap='G5')


@R.add('ch08-st4', 'C3', (2, 4), 'short')
def proof_reason(rng, slot):
    q_, ans = rng.choice([
        ('Lines AB and CD are parallel and a transversal makes an angle of x° with AB. State, with a reason, the angle it makes on the alternate side of CD.', 'x° (alternate angles are equal)'),
        ('Two triangles have all three pairs of sides equal. State the conclusion and the reason.', 'They are congruent (SSS).'),
        ('In a proof, triangle PQR ≅ triangle STU. State what you can conclude about angle Q and angle T.', 'Angle Q = angle T (corresponding parts of congruent triangles).'),
        ('Two triangles have two pairs of equal angles. State the conclusion and the reason.', 'They are similar (AA; the third angles are equal by the angle sum).'),
        ('In triangle ABC, AB = AC. State what you can conclude about angles B and C, with a reason.', 'Angle B = angle C (base angles of an isosceles triangle).'),
    ])
    return dict(stem=q_, answer=ans, markingKey=f'{ans} – A1 conclusion, R1 reason.', marks=2)


@R.add('ch08-st4', 'C1', (1, 3), 'mcq')
def proof_mcq(rng, slot):
    q_, a, w, why = rng.choice([
        ('Which reason justifies that vertically opposite angles are equal?', 'they are both supplementary to the same angle', ['they are alternate angles', 'they are corresponding angles', 'the triangle angle sum is 180°'], 'Each forms a straight line (180°) with the same adjacent angle.'),
        ('In a proof by congruence, which of these must be stated?', 'the three pairs of equal parts and the test used', ['only the test used', 'the measured lengths from the diagram', 'the areas of both triangles'], 'A congruence proof lists the equal parts with reasons, then names the test.'),
        ('Which statement is a valid reason in a geometric proof?', 'co-interior angles between parallel lines add to 180°', ['the angles look equal in the diagram', 'the lines appear perpendicular', 'I measured 90° with a protractor'], 'Only accepted facts can be used as reasons.'),
    ])
    return mcq(rng, q_, a, w, why)


# =============================================================================================
# ch09 Right-Angled Triangle Trigonometry
# =============================================================================================
def _sohcah(rng):
    ang = rng.choice([22, 28, 31, 35, 38, 42, 47, 53, 58, 63, 67, 72])
    return ang


R.facts('ch09-st1', F(
    terms=[('hypotenuse', 'the longest side of a right-angled triangle, opposite the right angle'),
           ('sine ratio', 'in a right-angled triangle, sin θ = opposite ÷ hypotenuse'),
           ('cosine ratio', 'in a right-angled triangle, cos θ = adjacent ÷ hypotenuse'),
           ('tangent ratio', 'in a right-angled triangle, tan θ = opposite ÷ adjacent')],
    why=[('Explain why sin θ can never be greater than 1 in a right-angled triangle.', 'sin θ = opposite ÷ hypotenuse and the hypotenuse is the longest side, so the fraction is less than 1.'),
         ('Explain why the trigonometric ratios of an angle do not depend on the size of the triangle.', 'All right-angled triangles with the same acute angle are similar, so their side ratios are equal.'),
         ('Explain why tan 45° = 1.', 'A right-angled triangle with a 45° angle is isosceles, so opposite = adjacent and their ratio is 1.')],
    misc=[('In a right-angled triangle the adjacent side is always the horizontal one.', 'The adjacent side is the side next to the angle being used (not the hypotenuse), whatever the orientation.'),
          ('sin 60° = sin 30° × 2 because 60 = 2 × 30.', 'Trig functions are not linear: sin 60° ≈ 0.866 but 2 sin 30° = 1.')],
))


@R.add('ch09-st1', 'C1', (1, 3), 'mcq')
def trig_ratio_mcq(rng, slot):
    a, b, c = rng.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41)])
    fn = rng.choice(['sin', 'cos', 'tan'])
    val = {'sin': f'{a}/{c}', 'cos': f'{b}/{c}', 'tan': f'{a}/{b}'}[fn]
    w = [v for v in [f'{a}/{c}', f'{b}/{c}', f'{a}/{b}', f'{b}/{a}', f'{c}/{a}'] if v != val][:3]
    return mcq(rng, f'In triangle ABC, angle C = 90°, BC = {a}, AC = {b} and AB = {c}. What is {fn} A?', val, w, f'For angle A: opposite = BC = {a}, adjacent = AC = {b}, hypotenuse = AB = {c}.')


@R.add('ch09-st1', 'C3', (1, 3), 'short')
def trig_label(rng, slot):
    a, b, c = rng.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (6, 8, 10), (9, 12, 15)])
    return dict(stem=f'A right-angled triangle has legs {a} cm and {b} cm and hypotenuse {c} cm. θ is the angle opposite the {a} cm side. Write down sin θ, cos θ and tan θ as fractions in simplest form.',
                answer=f'sin θ = {frac(Fr(a, c))}, cos θ = {frac(Fr(b, c))}, tan θ = {frac(Fr(a, b))}', markingKey='Opposite/hyp, adj/hyp, opp/adj correctly identified (A1 each).', marks=3)


@R.add('ch09-st1', 'C4', (3, 5), 'multi_step')
def trig_identity(rng, slot):
    a, b, c = rng.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)])
    q_, ans = rng.choice([
        (f'Given sin θ = {a}/{c} for an acute angle θ, find cos θ and tan θ exactly without a calculator, and verify that sin²θ + cos²θ = 1.', f'cos θ = {b}/{c}, tan θ = {a}/{b}; ({a * a} + {b * b})/{c * c} = 1'),
        (f'Show that tan θ = sin θ / cos θ using a right-angled triangle, and check it for the triangle with sides {a}, {b}, {c}.', f'(opp/hyp)/(adj/hyp) = opp/adj; ({a}/{c})/({b}/{c}) = {a}/{b}'),
        (f'Explain, using similar triangles, why the value of tan θ for θ = {round(math.degrees(math.atan(a / b)), 1)}° is the same in a triangle with legs {a} and {b} and one with legs {3 * a} and {3 * b}.', f'Both give {a}/{b}; the triangles are similar so ratios are equal'),
    ])
    return dict(stem=q_, answer=ans, markingKey=f'Correct missing side by Pythagoras or similarity (M1 A1); ratios formed (A1); verification/explanation complete (R1). {ans}', marks=4)


@R.add('ch09-st1', 'C2', (2, 4), 'explain')
def trig_explain(rng, slot):
    ang = rng.choice([20, 30, 40, 50, 60, 70, 80])
    q_, ans = rng.choice([
        (f'Explain why cos {ang}° = sin {90 - ang}°.', f'In a right-angled triangle the two acute angles add to 90°; the side adjacent to {ang}° is opposite {90 - ang}°, so the two ratios are the same fraction.'),
        (f'Without a calculator, explain whether tan {ang}° is greater or less than 1.', f'{"Less" if ang < 45 else "Greater"} than 1: for angles {"below" if ang < 45 else "above"} 45° the opposite side is {"shorter" if ang < 45 else "longer"} than the adjacent side.'),
        (f'As θ increases from 0° to 90°, explain what happens to sin θ, using a triangle with a fixed hypotenuse.', 'The opposite side grows from 0 towards the length of the hypotenuse, so sin θ increases from 0 to 1.'),
    ])
    return dict(stem=q_, answer=ans, markingKey=f'{ans} (R1 R1)', type='explain', marks=2)


@R.add('ch08-st4', 'C2', (2, 4), 'explain')
def proof_explain(rng, slot):
    q_, ans = rng.choice([
        ('Explain the difference between showing that a result is true for one diagram and proving it.', 'Checking one diagram tests a single case; a proof uses general reasons that hold for every figure satisfying the conditions.'),
        ('Explain why "the triangles look the same size" is not a valid step in a congruence proof.', 'Visual appearance can mislead; each equality must come from given information or an accepted fact.'),
        ('Explain why, after proving two triangles congruent, you may state that a pair of corresponding angles is equal.', 'Congruent triangles coincide exactly, so all corresponding parts are equal (CPCT).'),
        ('Explain why proving two triangles similar is enough to find a missing length but not enough to show two lengths are equal.', 'Similarity fixes ratios, not sizes; equal lengths need a scale factor of 1, i.e. congruence.'),
        ('Explain what a counter-example is and why one counter-example disproves a general claim.', 'A single case meeting the conditions where the claim fails shows the claim is not true in general.'),
        ('Explain why an angle-chasing proof must state which lines are parallel.', 'Alternate/corresponding angle facts only apply to parallel lines, so the reason depends on it.'),
        ('Explain why the order of letters matters when writing △ABC ≅ △PQR.', 'The order records which vertices correspond (A↔P, B↔Q, C↔R), and so which sides and angles are equal.'),
        ('Explain why the statement "all equilateral triangles are similar" is true but "all isosceles triangles are similar" is false.', 'Equilateral triangles all have angles 60°, 60°, 60°; isosceles triangles can have different apex angles.'),
        ('Explain how you could prove that a quadrilateral is a parallelogram using congruent triangles.', 'Draw a diagonal, prove the two triangles congruent so alternate angles are equal, which makes opposite sides parallel.'),
    ])
    return dict(stem=q_, answer=ans, markingKey=f'{ans} (R1 R1)', type='explain', marks=2)


@R.add('ch08-st4', 'C3', (1, 4), 'short')
def proof_angles(rng, slot):
    a = rng.randint(25, 75)
    b = rng.randint(20, 160 - a)
    q_, ans = rng.choice([
        (f'In triangle ABC, angle A = {a}° and angle B = {b}°. The line through C parallel to AB makes angles x and y with CA and CB. Find x and y, giving reasons.', f'x = {a}°, y = {b}° (alternate angles); hence angle C = {180 - a - b}°'),
        (f'Two parallel lines are cut by a transversal; one co-interior angle is {a + 40}°. Find the other and state the reason.', f'{140 - a}° (co-interior angles sum to 180°)'),
        (f'An isosceles triangle has apex angle {2 * a}°. Find each base angle, giving a reason.', f'{90 - a}° (base angles equal; angle sum 180°)'),
        (f'The exterior angle at C of triangle ABC is {a + b}° and angle A = {a}°. Find angle B, giving a reason.', f'{b}° (exterior angle = sum of the two interior opposite angles)'),
    ])
    return dict(stem=q_, answer=ans, markingKey=f'{ans}: A1 value(s), R1 reason(s).', marks=3)


@R.add('ch08-st1', 'C4', (3, 5), 'multi_step')
def cong_context(rng, slot):
    L, a = rng.randint(4, 12), rng.choice([30, 40, 45, 50, 60])
    who = name(rng)
    q_, ans = rng.choice([
        (f'{who} builds two triangular frames for a roof. Each has rafters of length {L} m meeting at {2 * a}° at the top. Explain why the frames are congruent and find the length of the base of each, to 3 s.f.', f'SAS; base = {2 * L * math.sin(math.radians(a)):.3g} m'),
        (f'A surveyor measures a lake: from point P, she walks to Q and R so that PQ = PR = {L * 10} m and angle QPR = {2 * a}°. Explain why triangles PQM and PRM are congruent, where M is the midpoint of QR, and find QR.', f'SSS (PQ = PR, QM = RM, PM common); QR = {2 * L * 10 * math.sin(math.radians(a)):.3g} m'),
        (f'Two ladders of equal length {L} m lean against parallel walls, each making {a + 10}° with the ground. Prove that they reach the same height and find it.', f'ASA/AAS congruent right triangles; height {L * math.sin(math.radians(a + 10)):.3g} m'),
    ])
    return dict(stem=q_, answer=ans, markingKey=f'Congruence test stated with three equal parts (R1 R1); calculation (M1 A1); communicated clearly (C1). {ans}', marks=5)


@R.add('ch09-st1', 'C3', (2, 4), 'short')
def trig_eval(rng, slot):
    ang = _sohcah(rng)
    fn = rng.choice(['sin', 'cos', 'tan'])
    v = getattr(math, fn)(math.radians(ang))
    h = rng.randint(5, 30)
    frames = [
        (f'Use your calculator to find {fn} {ang}° to 4 decimal places, and explain what this value means in a right-angled triangle.', f'{v:.4f}; ' + {'sin': 'opposite is', 'cos': 'adjacent is', 'tan': 'opposite is'}[fn] + f' {v:.4f} times the ' + {'sin': 'hypotenuse', 'cos': 'hypotenuse', 'tan': 'adjacent side'}[fn]),
        (f'A right-angled triangle has hypotenuse {h} cm and an angle of {ang}°. Find the side opposite this angle.', f'{h * math.sin(math.radians(ang)):.3g} cm'),
        (f'A right-angled triangle has hypotenuse {h} cm and an angle of {ang}°. Find the side adjacent to this angle.', f'{h * math.cos(math.radians(ang)):.3g} cm'),
    ]
    q_, ans = rng.choice(frames)
    return dict(stem=q_, answer=ans, markingKey=f'Correct ratio chosen (M1); {ans} (A1).', marks=2)


# =============================================================================================
# ch09 continued
# =============================================================================================
R.facts('ch09-st2', F(
    terms=[('inverse sine', 'sin⁻¹, the operation that gives the angle whose sine is a given ratio'),
           ('angle of a triangle from two sides', 'found with sin⁻¹, cos⁻¹ or tan⁻¹ of the ratio of the two known sides')],
    why=[('Explain how to choose which trigonometric ratio to use.', 'Label the sides opposite, adjacent and hypotenuse relative to the angle, then pick the ratio that links the side you know to the side you want (SOH CAH TOA).'),
         ('Explain why you use tan⁻¹ and not tan when finding an angle.', 'tan takes an angle and gives a ratio; to go from a ratio back to an angle you need the inverse function tan⁻¹.'),
         ('Explain why a calculator must be in degree mode for these problems.', 'Angles are measured in degrees here; in radian mode the calculator interprets the input as radians and gives different values.')],
    misc=[('To find x when sin 40° = 7/x, x = 7 × sin 40°.', 'Rearrange: x = 7/sin 40° ≈ 10.9; multiplying would give a side shorter than 7, impossible for the hypotenuse.'),
          ('sin⁻¹(x) means 1/sin(x).', 'sin⁻¹ is the inverse function (gives an angle); 1/sin x is the reciprocal (cosecant).')],
))


@R.add('ch09-st2', 'C3', (1, 4), 'short')
def trig_side(rng, slot):
    ang = _sohcah(rng)
    s = rng.randint(4, 25)
    fn = rng.choice(['sin', 'cos', 'tan'])
    known = rng.choice(['hyp', 'leg'])
    if fn == 'tan':
        if known == 'hyp':
            known = 'leg'
        ans = s * math.tan(math.radians(ang)) if rng.random() < 0.5 else s / math.tan(math.radians(ang))
        if abs(ans - s * math.tan(math.radians(ang))) < 1e-9:
            q_ = f'In a right-angled triangle the side adjacent to a {ang}° angle is {s} cm. Find the opposite side.'
        else:
            q_ = f'In a right-angled triangle the side opposite a {ang}° angle is {s} cm. Find the adjacent side.'
    else:
        if known == 'hyp':
            ans = s * getattr(math, fn)(math.radians(ang))
            q_ = f'A right-angled triangle has hypotenuse {s} cm. Find the side {"opposite" if fn == "sin" else "adjacent to"} the {ang}° angle.'
        else:
            ans = s / getattr(math, fn)(math.radians(ang))
            q_ = f'In a right-angled triangle the side {"opposite" if fn == "sin" else "adjacent to"} a {ang}° angle is {s} cm. Find the hypotenuse.'
    return dict(stem=q_, answer=f'{ans:.3g} cm', markingKey=f'Correct ratio ({fn}) (M1); correct rearrangement (M1); {ans:.3g} cm (A1).', marks=3 if slot.d >= 3 else 2)


@R.add('ch09-st2', 'C3', (1, 3), 'short')
def trig_angle(rng, slot):
    a, b = rng.randint(3, 20), rng.randint(3, 20)
    fn = rng.choice(['tan', 'sin', 'cos'])
    if fn != 'tan' and a >= b:
        a, b = min(a, b), max(a, b) + 1
    v = math.degrees({'tan': math.atan, 'sin': math.asin, 'cos': math.acos}[fn](a / b))
    desc = {'tan': f'the opposite side is {a} cm and the adjacent side is {b} cm', 'sin': f'the opposite side is {a} cm and the hypotenuse is {b} cm', 'cos': f'the adjacent side is {a} cm and the hypotenuse is {b} cm'}[fn]
    return dict(stem=f'In a right-angled triangle, {desc}. Find the angle θ to 1 decimal place.', answer=f'{v:.1f}°',
                markingKey=f'{fn} θ = {a}/{b} (M1); θ = {fn}⁻¹({a}/{b}) = {v:.1f}° (A1).', marks=2)


@R.add('ch09-st2', 'C1', (1, 3), 'mcq')
def trig_choose_mcq(rng, slot):
    known, want, ratio = rng.choice([('opposite and adjacent', 'the angle', 'tan'), ('adjacent and hypotenuse', 'the angle', 'cos'), ('opposite and hypotenuse', 'the angle', 'sin'),
                                     ('the angle and the hypotenuse', 'the opposite side', 'sin'), ('the angle and the adjacent side', 'the opposite side', 'tan'), ('the angle and the hypotenuse', 'the adjacent side', 'cos')])
    w = [r for r in ['sin', 'cos', 'tan', 'Pythagoras’ theorem'] if r != ratio]
    return mcq(rng, f'You know {known} in a right-angled triangle and want {want}. Which should you use?', ratio, w, f'{ratio} links {known} with {want}.')


@R.add('ch09-st2', 'C4', (3, 5), 'multi_step')
def trig_two_step(rng, slot):
    a1, a2 = rng.choice([30, 35, 40, 42]), rng.choice([50, 55, 60, 65])
    d = rng.randint(10, 40)
    h1 = d * math.tan(math.radians(a1))
    h2 = d * math.tan(math.radians(a2))
    who = name(rng)
    frames = [
        (f'From a point {d} m from the base of a building, the angles of elevation to the bottom and top of a flagpole on its roof are {a1}° and {a2}°. Find the height of the flagpole.', f'{h2 - h1:.3g} m'),
        (f'A ramp rises at {a1 // 3}° to reach a platform {round(d / 10, 1)} m high. Building rules say ramps must be shorter than 12 m. Find the ramp length and decide whether {who}’s design is allowed.', None),
        (f'A ladder {d / 4:g} m long leans against a wall. Its foot is {d / 10:g} m from the wall. Find the angle with the ground and how far up the wall it reaches.', f'{math.degrees(math.acos((d / 10) / (d / 4))):.1f}°; {math.sqrt((d / 4) ** 2 - (d / 10) ** 2):.3g} m'),
    ]
    q_, ans = rng.choice(frames)
    if ans is None:
        L = (d / 10) / math.sin(math.radians(a1 // 3))
        ans = f'{L:.3g} m; {"allowed" if L < 12 else "not allowed"}'
    return dict(stem=q_, answer=ans, markingKey=f'Correct right-angled triangle(s) identified (M1); ratio(s) set up (M1 A1); answer {ans} (A1); conclusion/units in context (C1).', marks=5, gap='G7')


@R.add('ch09-st2', 'C2', (2, 4), 'explain')
def trig_error(rng, slot):
    ang, s = _sohcah(rng), rng.randint(5, 20)
    q_, ans = rng.choice([
        (f'{name(rng)} finds the hypotenuse h from sin {ang}° = {s}/h and writes h = {s} × sin {ang}° = {s * math.sin(math.radians(ang)):.2f}. Explain why the answer cannot be right.', f'The hypotenuse must be longer than {s}; correct h = {s}/sin {ang}° = {s / math.sin(math.radians(ang)):.3g}.'),
        (f'Explain why, in a right-angled triangle, an angle found by tan⁻¹ of a ratio greater than 1 must be more than 45°.', 'tan 45° = 1 and tan increases on 0°–90°, so a larger ratio gives a larger angle.'),
        (f'Explain why cos⁻¹({s + 3}/{s}) gives an error on a calculator.', 'cos of an angle in a right-angled triangle is adjacent/hypotenuse ≤ 1; the ratio here is greater than 1.'),
    ])
    return dict(stem=q_, answer=ans, markingKey=f'{ans} (R1 A1)', type='explain', marks=2)


R.facts('ch09-st3', F(
    terms=[('angle of elevation', 'the angle measured upward from the horizontal to a line of sight'),
           ('angle of depression', 'the angle measured downward from the horizontal to a line of sight'),
           ('three-figure bearing', 'a direction measured clockwise from north, written with three digits, e.g. 045°')],
    why=[('Explain why the angle of depression from A to B equals the angle of elevation from B to A.', 'The horizontals at A and B are parallel, so the two angles are alternate angles and are equal.'),
         ('Explain why bearings are always written with three figures.', 'Writing 045° rather than 45° avoids ambiguity and keeps a standard format used in navigation.'),
         ('Explain how to find the bearing of A from B if you know the bearing of B from A is less than 180°.', 'Add 180°: the back bearing points in the opposite direction.')],
    misc=[('The angle of depression is measured from the vertical.', 'It is measured from the horizontal, downwards.'),
          ('The bearing of B from A is 070°, so the bearing of A from B is 070° as well.', 'The reverse bearing is 070° + 180° = 250°.')],
))


@R.add('ch09-st3', 'C3', (1, 4), 'short')
def elev(rng, slot):
    who = name(rng)
    ang = rng.choice([12, 18, 24, 27, 32, 36, 41, 48, 55])
    d = rng.randint(15, 120)
    frames = [
        (f'{who} stands {d} m from the foot of a tower. The angle of elevation of the top is {ang}°. Find the height of the tower (ignore her height).', f'{d * math.tan(math.radians(ang)):.3g} m'),
        (f'From the top of a cliff {d} m high, the angle of depression of a boat is {ang}°. How far is the boat from the foot of the cliff?', f'{d / math.tan(math.radians(ang)):.3g} m'),
        (f'A kite string is {d} m long and makes an angle of elevation of {ang}°. Find the height of the kite.', f'{d * math.sin(math.radians(ang)):.3g} m'),
        (f'A drone hovers {d} m above the ground. From a point on the ground the angle of elevation is {ang}°. Find the horizontal distance to the point under the drone.', f'{d / math.tan(math.radians(ang)):.3g} m'),
    ]
    q_, ans = rng.choice(frames)
    return dict(stem=q_, answer=ans, markingKey=f'Correct diagram with the angle from the horizontal (M1); correct ratio (M1); {ans} (A1).', marks=3, gap='G7')


@R.add('ch09-st3', 'C3', (2, 5), 'short')
def bearings(rng, slot):
    b = rng.choice([35, 50, 70, 110, 125, 140, 220, 235, 300, 320])
    d = rng.randint(5, 60)
    e, n = d * math.sin(math.radians(b)), d * math.cos(math.radians(b))
    q_, ans = rng.choice([
        (f'A ship sails {d} km on a bearing of {b:03d}°. How far east (or west) and north (or south) of its start is it?', f'{abs(e):.3g} km {"east" if e > 0 else "west"}, {abs(n):.3g} km {"north" if n > 0 else "south"}'),
        (f'The bearing of a lighthouse L from a port P is {b:03d}°. Find the bearing of P from L.', f'{(b + 180) % 360:03d}°'),
    ])
    return dict(stem=q_, answer=ans, markingKey=f'Diagram with north line and clockwise angle (M1); correct trig/back-bearing (M1); {ans} (A1).', marks=3)


@R.add('ch09-st3', 'C4', (3, 5), 'multi_step')
def bearings_two_leg(rng, slot):
    d1, d2 = rng.randint(5, 30), rng.randint(5, 30)
    b1 = rng.choice([0, 90, 180, 270])
    b2 = (b1 + 90) % 360
    dist = math.hypot(d1, d2)
    e = d1 * math.sin(math.radians(b1)) + d2 * math.sin(math.radians(b2))
    n = d1 * math.cos(math.radians(b1)) + d2 * math.cos(math.radians(b2))
    brg = (math.degrees(math.atan2(e, n)) + 360) % 360
    who = name(rng)
    return dict(stem=f'{who} hikes {d1} km on a bearing of {b1:03d}° and then {d2} km on a bearing of {b2:03d}°. (a) How far is she from her starting point? (b) On what bearing must she walk to return directly to the start?',
                answer=f'(a) {dist:.3g} km (b) {(brg + 180) % 360:.0f}°', markingKey=f'Right angle between the legs identified (R1); distance by Pythagoras {dist:.3g} km (M1 A1); angle at start by tan (M1); return bearing {(brg + 180) % 360:.0f}° (A1).', marks=5, gap='G5')


@R.add('ch09-st3', 'C2', (2, 4), 'explain')
def elev_explain(rng, slot):
    a = rng.randint(15, 70)
    return dict(stem=f'From the top of a lighthouse the angle of depression of a boat is {a}°. Explain why the angle of elevation of the lighthouse top from the boat is also {a}°, using a diagram description.', answer=f'{a}°',
                markingKey='The horizontal at the top and the sea level are parallel (R1); the line of sight is a transversal, so the angles are alternate and equal (R1).', type='explain', marks=2)


R.facts('ch09-st4', F(
    terms=[('space diagonal', 'a line joining opposite corners of a cuboid through its interior'),
           ('angle between a line and a plane', 'the angle between the line and its projection onto the plane')],
    why=[('Explain why you find the diagonal of the base first when finding the space diagonal of a cuboid.', 'The space diagonal is the hypotenuse of a right-angled triangle whose legs are the base diagonal and the height; the base diagonal is found by Pythagoras first.'),
         ('Explain why drawing the right-angled triangle separately helps in 3D problems.', 'It turns the 3D situation into a 2D right-angled triangle where Pythagoras and SOH CAH TOA apply directly.')],
    misc=[('The space diagonal of a 3 × 4 × 12 cuboid is 3 + 4 + 12 = 19.', 'Use Pythagoras twice: √(3² + 4² + 12²) = 13.')],
))


@R.add('ch09-st4', 'C3', (2, 4), 'short')
def cuboid_diag(rng, slot):
    a, b, c = rng.choice([(3, 4, 12), (2, 3, 6), (1, 4, 8), (2, 6, 9), (6, 6, 7), (4, 4, 7), (2, 10, 11)]) if rng.random() < 0.5 else (rng.randint(2, 12), rng.randint(2, 12), rng.randint(2, 12))
    d = math.sqrt(a * a + b * b + c * c)
    ang = math.degrees(math.atan(c / math.hypot(a, b)))
    q_, ans = rng.choice([
        (f'A cuboid measures {a} cm by {b} cm by {c} cm. Find the length of its space diagonal.', f'{d:.3g} cm'),
        (f'A box is {a} cm long, {b} cm wide and {c} cm high. Find the angle between the space diagonal and the base.', f'{ang:.1f}°'),
        (f'Will a rod {math.floor(d) + rng.choice([-1, 1])} cm long fit inside a box measuring {a} × {b} × {c} cm? Justify your answer.', None),
    ])
    if ans is None:
        L = int(q_.split('rod ')[1].split(' cm')[0])
        ans = f'{"yes" if L <= d else "no"}: longest rod {d:.3g} cm'
    return dict(stem=q_, answer=ans, markingKey=f'Base diagonal √({a}² + {b}²) (M1); second right-angled triangle (M1); {ans} (A1).', marks=3)


@R.add('ch09-st4', 'C4', (3, 5), 'multi_step')
def pyramid_3d(rng, slot):
    s, h = rng.randint(4, 16), rng.randint(5, 20)
    half_d = s * math.sqrt(2) / 2
    edge = math.hypot(half_d, h)
    ang = math.degrees(math.atan(h / half_d))
    slant = math.hypot(s / 2, h)
    q_, ans = rng.choice([
        (f'A square-based pyramid has base side {s} cm and vertical height {h} cm. Find (a) the length of a sloping edge, (b) the angle between a sloping edge and the base.', f'(a) {edge:.3g} cm (b) {ang:.1f}°'),
        (f'A tent is a square-based pyramid with base {s / 2:g} m and height {h / 5:g} m. Find the slant height of a triangular face and the total area of canvas for the four faces.', f'slant {math.hypot(s / 4, h / 5):.3g} m; canvas {4 * 0.5 * (s / 2) * math.hypot(s / 4, h / 5):.3g} m²'),
        (f'A square pyramid has base {s} cm and slant height (face height) {slant:.3g} cm. Find its vertical height and the angle a face makes with the base.', f'{h} cm; {math.degrees(math.atan(h / (s / 2))):.1f}°'),
    ])
    return dict(stem=q_, answer=ans, markingKey=f'Correct 2D right-angled triangle(s) extracted (M1 M1); Pythagoras/trig applied (A1 A1); answer with units and accuracy (C1). {ans}', marks=5, gap='G5')


@R.add('ch09-st4', 'C2', (2, 4), 'explain')
def three_d_explain(rng, slot):
    a, b, c = rng.randint(2, 9), rng.randint(2, 9), rng.randint(2, 9)
    q_, ans = rng.choice([
        (f'Explain why the space diagonal of a {a} × {b} × {c} cuboid equals √({a}² + {b}² + {c}²).', f'Base diagonal² = {a}² + {b}² (Pythagoras); space diagonal² = base diagonal² + {c}² (Pythagoras again).'),
        (f'Explain why the angle between the space diagonal and the base of a cuboid is not the same as the angle between a face diagonal and the base.', 'They lie in different right-angled triangles with different horizontal legs (base diagonal vs base edge), so the tangent ratios differ.'),
        (f'Explain why all four sloping edges of a right square-based pyramid are equal.', 'The apex is directly above the centre, which is the same distance from all four corners; with the same height, Pythagoras gives equal edges.'),
    ])
    return dict(stem=q_, answer=ans, markingKey=f'{ans} (R1 R1)', type='explain', marks=2)


# =============================================================================================
# ch10 Circles and Mensuration
# =============================================================================================
R.facts('ch10-st1', F(
    terms=[('sector', 'the region of a circle bounded by two radii and the arc between them'),
           ('arc length', 'the distance along the curved part of a circle between two points: (θ/360) × 2πr'),
           ('minor arc', 'the shorter of the two arcs joining two points on a circle')],
    why=[('Explain why the area of a sector with angle θ is (θ/360) × πr².', 'The sector is the fraction θ/360 of the full turn, so it has that fraction of the whole circle’s area πr².'),
         ('Explain why doubling the radius of a sector doubles its arc length but quadruples its area.', 'Arc length is proportional to r, while area is proportional to r².'),
         ('Explain why the perimeter of a sector is not the same as its arc length.', 'The perimeter includes the two straight radii as well as the arc: P = arc + 2r.')],
    misc=[('The area of a 90° sector of radius 4 cm is (90/360) × 2π × 4.', 'That is the arc length formula; area uses πr²: (90/360) × π × 16 = 4π cm².'),
          ('A sector with a 180° angle has perimeter πr.', 'πr is the arc only; the perimeter is πr + 2r.')],
))


@R.add('ch10-st1', 'C3', (1, 4), 'short')
def sector(rng, slot):
    r_, th = rng.randint(3, 20), rng.choice([30, 40, 45, 60, 72, 80, 100, 120, 135, 150, 210, 240, 300])
    arc = th / 360 * 2 * math.pi * r_
    area = th / 360 * math.pi * r_ * r_
    kind = rng.choice(['arc', 'area', 'perim'] if slot.d <= 2 else ['perim', 'angle', 'radius'])
    if kind == 'arc':
        return dict(stem=f'Find the length of an arc of a circle with radius {r_} cm subtending an angle of {th}° at the centre.', answer=f'{arc:.3g} cm', markingKey=f'({th}/360) × 2π × {r_} (M1) = {arc:.3g} cm (A1).', marks=2)
    if kind == 'area':
        return dict(stem=f'Find the area of a sector of radius {r_} cm and angle {th}°.', answer=f'{area:.3g} cm²', markingKey=f'({th}/360) × π × {r_}² (M1) = {area:.3g} cm² (A1).', marks=2)
    if kind == 'perim':
        return dict(stem=f'Find the perimeter of a sector of radius {r_} cm and angle {th}°.', answer=f'{arc + 2 * r_:.3g} cm', markingKey=f'Arc {arc:.3g} (M1) + 2 × {r_} (M1) = {arc + 2 * r_:.3g} cm (A1).', marks=3)
    if kind == 'angle':
        return dict(stem=f'A sector of radius {r_} cm has arc length {arc:.2f} cm. Find the angle of the sector.', answer=f'{th}°', markingKey=f'θ/360 × 2π × {r_} = {arc:.2f} (M1); θ = {th}° (A1).', marks=3)
    return dict(stem=f'A sector with angle {th}° has area {area:.2f} cm². Find its radius.', answer=f'{r_} cm', markingKey=f'({th}/360)πr² = {area:.2f} (M1); r² = {r_ * r_} (A1); r = {r_} cm (A1).', marks=3)


@R.add('ch10-st1', 'C4', (3, 5), 'multi_step')
def sector_context(rng, slot):
    r_ = rng.randint(5, 25)
    th = rng.choice([60, 72, 90, 120, 135])
    who = name(rng)
    frames = [
        (f'A pizza of radius {r_} cm is cut into equal slices with angle {th}°. (a) How many slices are there? (b) Find the area and the length of crust (arc) of one slice.', f'(a) {360 // th if 360 % th == 0 else round(360 / th, 2)} (b) {th / 360 * math.pi * r_ ** 2:.3g} cm², {th / 360 * 2 * math.pi * r_:.3g} cm'),
        (f'A garden sprinkler sprays water a distance of {r_ / 2:g} m through an angle of {th}°. {who} wants to know the watered area and the length of the curved edge.', f'{th / 360 * math.pi * (r_ / 2) ** 2:.3g} m², {th / 360 * 2 * math.pi * (r_ / 2):.3g} m'),
        (f'A windscreen wiper arm of length {r_ + 30} cm has a rubber blade along its outer {r_} cm and turns through {th + 20}°. Find the area wiped.', f'{(th + 20) / 360 * math.pi * ((r_ + 30) ** 2 - 30 ** 2):.3g} cm²'),
        (f'A paper cone is made by rolling a sector of radius {r_} cm and angle {th}°. Find the radius of the cone’s base.', f'{r_ * th / 360:.3g} cm'),
    ]
    q_, ans = rng.choice(frames)
    return dict(stem=q_, answer=ans, markingKey=f'Correct fraction of the circle (M1); correct formula(s) (M1 A1); answer with units {ans} (A1); interpretation (C1).', marks=5)


@R.add('ch10-st1', 'C2', (2, 4), 'explain')
def sector_explain(rng, slot):
    th = rng.choice([45, 60, 90, 120])
    r_ = rng.randint(2, 10)
    q_, ans = rng.choice([
        (f'Explain why a {th}° sector of a circle of radius {r_} has arc length {frac(Fr(th, 180))}π{"" if r_ == 1 else ""}·{r_}.', f'Arc = ({th}/360) × 2π × {r_} = {frac(Fr(th, 180))} × π × {r_}.'),
        (f'Two sectors have the same angle {th}° but radii {r_} cm and {2 * r_} cm. Explain how their areas compare.', 'The larger area is 4 times the smaller, because area scales with r².'),
        (f'Explain why the arc length of a sector is always less than the circumference of its circle unless the angle is 360°.', 'The arc is the fraction θ/360 of the circumference, which is less than 1 for θ < 360°.'),
    ])
    return dict(stem=q_, answer=ans, markingKey=f'{ans} (R1 A1)', type='explain', marks=2)


R.facts('ch10-st2', F(
    terms=[('angle at the centre theorem', 'the angle subtended by an arc at the centre is twice the angle it subtends at any point on the remaining circumference'),
           ('angle in a semicircle', 'an angle subtended by a diameter at the circumference, which is always 90°'),
           ('cyclic quadrilateral', 'a quadrilateral whose four vertices lie on a circle; its opposite angles sum to 180°')],
    why=[('Explain why the angle in a semicircle is 90°, using the angle at the centre theorem.', 'The diameter subtends a straight angle of 180° at the centre, so at the circumference it subtends half of that, 90°.'),
         ('Explain why angles in the same segment are equal.', 'Each is half the angle subtended at the centre by the same arc, so they are all equal.'),
         ('Explain why opposite angles of a cyclic quadrilateral add to 180°.', 'The two opposite angles stand on arcs that together make the whole circle; their centre angles add to 360°, so the angles add to 180°.')],
    misc=[('The angle at the centre is half the angle at the circumference.', 'It is the other way round: the angle at the centre is twice the angle at the circumference.'),
          ('Any triangle drawn inside a circle has a right angle.', 'Only when one side is a diameter (angle in a semicircle).')],
))


@R.add('ch10-st2', 'C3', (1, 4), 'short')
def circle_thm(rng, slot):
    a = rng.randint(20, 80)
    q_, ans, why = rng.choice([
        (f'O is the centre of a circle. Points A, B and C lie on the circle and angle ACB = {a}°. Find angle AOB.', f'{2 * a}°', 'angle at the centre is twice the angle at the circumference'),
        (f'O is the centre. Angle AOB = {2 * a}°, where A and B are on the circle. P is on the major arc. Find angle APB.', f'{a}°', 'angle at the centre = 2 × angle at circumference'),
        (f'AB is a diameter of a circle and C is on the circle. Angle CAB = {a}°. Find angle CBA.', f'{90 - a}°', 'angle in a semicircle is 90°, then angle sum of a triangle'),
        (f'ABCD is a cyclic quadrilateral with angle A = {a + 40}°. Find angle C.', f'{140 - a}°', 'opposite angles of a cyclic quadrilateral sum to 180°'),
        (f'Points P, Q, R, S lie on a circle. Angle PRQ = {a}°. Find angle PSQ, where S is in the same segment as R.', f'{a}°', 'angles in the same segment are equal'),
    ])
    return dict(stem=q_, answer=ans, markingKey=f'{ans} (A1); reason: {why} (R1).', marks=2)


@R.add('ch10-st2', 'C4', (3, 5), 'multi_step')
def circle_thm_multi(rng, slot):
    a = rng.randint(25, 65)
    b = rng.randint(20, 60)
    q_, ans = rng.choice([
        (f'O is the centre of a circle through A, B and C. Angle OAB = {a}°. Find angle ACB, giving reasons for each step.', f'{90 - a}°: OA = OB so angle OBA = {a}°, angle AOB = {180 - 2 * a}°, angle ACB = half = {90 - a}°'),
        (f'ABCD is cyclic. AB is a diameter, angle BAC = {a}° and angle CAD = {b if a + b < 90 else 90 - a - 5}°. Find angles ABC and BCD.', None),
        (f'In a circle with centre O, chord AB subtends angle AOB = {2 * a}°. Tangents at A and B meet at T. Find angle ATB.', f'{180 - 2 * a}° (tangent ⊥ radius, angles in quadrilateral OATB sum to 360°)'),
    ])
    if ans is None:
        bb = b if a + b < 90 else 90 - a - 5
        ans = f'ABC = {90 - a}° (angle in semicircle, angle sum); BCD = {180 - (a + bb)}° (opposite angles of cyclic quadrilateral: BAD = {a + bb}°)'
        q_ = f'ABCD is a cyclic quadrilateral. AB is a diameter, angle BAC = {a}° and angle CAD = {bb}°. Find angles ABC and BCD, giving reasons.'
    return dict(stem=q_, answer=ans, markingKey=f'Each angle found with a correct theorem as reason (M1 R1 per step); final values {ans} (A1); clear communication (C1).', marks=5, gap='G5')


@R.add('ch10-st2', 'C1', (1, 3), 'mcq')
def circle_thm_mcq(rng, slot):
    q_, a, w, why = rng.choice([
        ('An angle subtended at the circumference by a diameter is:', '90°', ['180°', '45°', 'half the angle at the centre of 90°'], 'Angle in a semicircle theorem.'),
        ('In a cyclic quadrilateral, opposite angles are:', 'supplementary (sum to 180°)', ['equal', 'complementary (sum to 90°)', 'always right angles'], 'Opposite angles of a cyclic quadrilateral sum to 180°.'),
        ('Compared with the angle at the circumference on the same arc, the angle at the centre is:', 'twice as large', ['half as large', 'equal', '90° larger'], 'Angle at the centre theorem.'),
        ('Angles subtended by the same arc in the same segment are:', 'equal', ['supplementary', 'complementary', 'in the ratio 2 : 1'], 'Angles in the same segment theorem.'),
    ])
    return mcq(rng, q_, a, w, why)


@R.add('ch10-st2', 'C2', (2, 4), 'explain')
def circle_thm_explain(rng, slot):
    a = rng.randint(20, 80)
    q_, ans = rng.choice([
        (f'{name(rng)} says angle AOB = {a}° because angle ACB = {2 * a}°, where O is the centre. Explain the error.', f'The centre angle is double the circumference angle, not half: angle AOB = {4 * a}° if angle ACB = {2 * a}° (or the values are swapped).'),
        (f'Explain how the isosceles triangle formed by two radii helps in circle-angle problems.', 'Two radii are equal, so the base angles of that triangle are equal; this links angles at the centre to angles at the chord.'),
        (f'Explain why a quadrilateral with angles {a}°, {a + 30}°, {180 - a}° and {150 - a}° (in order) is cyclic.', 'Opposite angles sum to 180° ({a} + {180 - a} and {a + 30} + {150 - a}), which is the condition for a cyclic quadrilateral.'),
    ])
    return dict(stem=q_, answer=ans, markingKey=f'{ans} (R1 R1)', type='explain', marks=2)


R.facts('ch10-st3', F(
    terms=[('tangent', 'a straight line that touches a circle at exactly one point'),
           ('chord', 'a straight line segment joining two points on a circle')],
    why=[('Explain why the tangent at a point is perpendicular to the radius at that point.', 'The radius is the shortest distance from the centre to the tangent line; the shortest distance from a point to a line is perpendicular to it.'),
         ('Explain why the two tangents from an external point to a circle are equal in length.', 'Joining the point and the centre forms two right-angled triangles with a common hypotenuse and equal radii, so they are congruent (RHS) and the tangent lengths are equal.'),
         ('Explain why the perpendicular from the centre to a chord bisects the chord.', 'The two triangles formed with the radii are congruent (RHS: common perpendicular, equal radii), so the two halves of the chord are equal.')],
    misc=[('A tangent cuts a circle at two points.', 'A line meeting a circle at two points is a secant; a tangent touches it at exactly one point.')],
))


@R.add('ch10-st3', 'C3', (1, 4), 'short')
def tangent_calc(rng, slot):
    r_, t = rng.choice([(5, 12), (3, 4), (8, 15), (7, 24), (6, 8), (9, 12), (20, 21)])
    q_, ans = rng.choice([
        (f'A tangent from point P touches a circle of radius {r_} cm at T. PT = {t} cm. Find the distance from P to the centre O.', f'{math.hypot(r_, t):g} cm'),
        (f'A chord is {2 * t} cm long in a circle of radius {math.hypot(r_, t):g} cm. Find the perpendicular distance from the centre to the chord.', f'{r_} cm'),
        (f'P is {math.hypot(r_, t):g} cm from the centre of a circle of radius {r_} cm. Find the length of a tangent from P.', f'{t} cm'),
    ])
    return dict(stem=q_, answer=ans, markingKey=f'Right angle identified (tangent ⊥ radius or perpendicular bisects chord) (R1); Pythagoras (M1); {ans} (A1).', marks=3)


@R.add('ch10-st3', 'C4', (3, 5), 'multi_step')
def tangent_multi(rng, slot):
    r_, t = rng.choice([(5, 12), (3, 4), (8, 15), (6, 8), (7, 24)])
    ang = math.degrees(math.atan(r_ / t))
    return dict(stem=f'Two tangents are drawn from P to a circle with centre O and radius {r_} cm, touching it at A and B. PA = {t} cm. (a) Find OP. (b) Find angle APB. (c) Find the area of quadrilateral OAPB.',
                answer=f'(a) {math.hypot(r_, t):g} cm (b) {2 * ang:.1f}° (c) {r_ * t} cm²', markingKey=f'(a) Pythagoras (M1 A1); (b) tan(APO) = {r_}/{t}, doubled (M1 A1); (c) two congruent right triangles each ½ × {r_} × {t} (A1).', marks=5, gap='G5')


@R.add('ch10-st3', 'C2', (2, 4), 'explain')
def tangent_explain(rng, slot):
    q_, ans = rng.choice([
        ('Explain how you would locate the centre of a circular plate using two chords.', 'Draw the perpendicular bisector of each chord; each passes through the centre, so they meet at the centre.'),
        ('Explain why the angle between a tangent and a radius is used so often in circle problems.', 'It gives a guaranteed right angle, allowing Pythagoras and trigonometry.'),
        ('Explain why a line from the centre to the midpoint of a chord is perpendicular to the chord.', 'Triangles formed with the two radii are congruent (SSS), so the two angles at the midpoint are equal and sum to 180°, so each is 90°.'),
        ('Explain why tangents at the two ends of a diameter are parallel.', 'Both tangents are perpendicular to the same diameter, so they are parallel.'),
    ])
    return dict(stem=q_, answer=ans, markingKey=f'{ans} (R1 R1)', type='explain', marks=2)


@R.add('ch10-st3', 'C1', (1, 3), 'mcq')
def tangent_mcq(rng, slot):
    q_, a, w, why = rng.choice([
        ('The angle between a tangent and the radius at the point of contact is:', '90°', ['45°', '180°', 'equal to the angle at the centre'], 'Tangent ⊥ radius.'),
        ('Two tangents drawn to a circle from the same external point are:', 'equal in length', ['perpendicular', 'parallel', 'always 90° apart'], 'Tangents from an external point are equal.'),
        ('The perpendicular from the centre of a circle to a chord:', 'bisects the chord', ['is always a diameter', 'is a tangent', 'doubles the chord'], 'Perpendicular from the centre bisects the chord.'),
    ])
    return mcq(rng, q_, a, w, why)


R.facts('ch10-st4', F(
    terms=[('slant height', 'the distance from the apex of a cone or pyramid down its sloping surface to the edge of the base'),
           ('volume of a cone', '⅓πr²h, one third of the cylinder with the same base and height'),
           ('surface area of a sphere', '4πr²')],
    why=[('Explain why the volume of a cone is one third of the volume of the cylinder with the same base and height.', 'Three cones of the same base and height fill the cylinder exactly (this can be shown by filling experiments or by calculus).'),
         ('Explain why the slant height l of a cone satisfies l² = r² + h².', 'The radius, vertical height and slant height form a right-angled triangle with l as the hypotenuse.'),
         ('Explain why units for volume are cubed while units for surface area are squared.', 'Volume multiplies three lengths; area multiplies two.')],
    misc=[('The curved surface area of a cone is πrh.', 'It uses the slant height: πrl, not the vertical height h.'),
          ('The volume of a sphere is 4πr².', '4πr² is the surface area; the volume is (4/3)πr³.')],
))


@R.add('ch10-st4', 'C3', (1, 4), 'numerical')
def solids(rng, slot):
    r_, h = rng.randint(2, 15), rng.randint(3, 25)
    l = math.hypot(r_, h)
    shape = rng.choice(['cone_v', 'cone_sa', 'sphere_v', 'sphere_sa', 'pyr_v', 'hemi'])
    if shape == 'cone_v':
        v = math.pi * r_ * r_ * h / 3
        return dict(stem=f'Find the volume of a cone with base radius {r_} cm and height {h} cm.', answer=f'{v:.4g} cm³', markingKey=f'⅓π({r_})²({h}) (M1) = {v:.4g} cm³ (A1).', type='numerical', marks=2)
    if shape == 'cone_sa':
        sa = math.pi * r_ * l + math.pi * r_ * r_
        return dict(stem=f'Find the total surface area of a solid cone with radius {r_} cm and vertical height {h} cm.', answer=f'{sa:.4g} cm²', markingKey=f'l = √({r_}² + {h}²) = {l:.3g} (M1 A1); πrl + πr² (M1) = {sa:.4g} cm² (A1).', type='numerical', marks=4)
    if shape == 'sphere_v':
        v = 4 / 3 * math.pi * r_ ** 3
        return dict(stem=f'Find the volume of a sphere of radius {r_} cm.', answer=f'{v:.4g} cm³', markingKey=f'(4/3)π({r_})³ (M1) = {v:.4g} cm³ (A1).', type='numerical', marks=2)
    if shape == 'sphere_sa':
        sa = 4 * math.pi * r_ ** 2
        return dict(stem=f'A sphere has surface area {sa:.2f} cm². Find its radius.', answer=f'{r_} cm', markingKey=f'4πr² = {sa:.2f} (M1); r² = {r_ * r_} (A1); r = {r_} cm (A1).', type='numerical', marks=3)
    if shape == 'pyr_v':
        v = r_ * r_ * h / 3
        return dict(stem=f'Find the volume of a square-based pyramid with base side {r_} cm and height {h} cm.', answer=f'{v:.4g} cm³', markingKey=f'⅓ × {r_}² × {h} (M1) = {v:.4g} cm³ (A1).', type='numerical', marks=2)
    v = 2 / 3 * math.pi * r_ ** 3
    return dict(stem=f'Find the volume of a hemisphere of diameter {2 * r_} cm.', answer=f'{v:.4g} cm³', markingKey=f'r = {r_} (A1); ½ × (4/3)π({r_})³ (M1) = {v:.4g} cm³ (A1).', type='numerical', marks=3)


@R.add('ch10-st4', 'C4', (3, 5), 'multi_step')
def solids_context(rng, slot):
    r_, h = rng.randint(3, 10), rng.randint(6, 20)
    who = name(rng)
    frames = [
        (f'An ice-cream cone has radius {r_} cm and height {h} cm and is topped with a hemisphere of ice cream of the same radius. Find the total volume of ice cream if the cone is also full.', f'{math.pi * r_ * r_ * h / 3 + 2 / 3 * math.pi * r_ ** 3:.4g} cm³'),
        (f'{who} melts a solid metal sphere of radius {r_} cm and recasts it into a cone of base radius {r_} cm. Find the height of the cone.', f'{4 * r_} cm'),
        (f'A grain silo is a cylinder of radius {r_} m and height {h} m with a cone of height {r_} m on top. Find its capacity and the area of metal sheet needed for the curved surfaces.', f'{math.pi * r_ * r_ * h + math.pi * r_ * r_ * r_ / 3:.4g} m³; {2 * math.pi * r_ * h + math.pi * r_ * math.hypot(r_, r_):.4g} m²'),
        (f'Spherical beads of radius 0.{r_} cm are made from a cube of glass of side {h} cm. How many whole beads can be made?', f'{int(h ** 3 // (4 / 3 * math.pi * (r_ / 10) ** 3))}'),
    ]
    q_, ans = rng.choice(frames)
    return dict(stem=q_, answer=ans, markingKey=f'Correct formulas chosen for each solid (M1 M1); combined correctly (M1); {ans} with units (A1); method communicated (C1).', marks=5)


@R.add('ch10-st4', 'C2', (2, 4), 'explain')
def solids_explain(rng, slot):
    r_ = rng.randint(2, 9)
    q_, ans = rng.choice([
        (f'A cylinder and a cone have the same radius {r_} cm and height. Explain how their volumes compare.', 'The cone’s volume is one third of the cylinder’s.'),
        (f'Explain why a sphere of radius {r_} and a cylinder of radius {r_} and height {2 * r_} have curved surface areas that are equal.', f'Sphere 4π({r_})² = {4 * r_ * r_}π; cylinder 2π({r_})({2 * r_}) = {4 * r_ * r_}π.'),
        (f'{name(rng)} uses the vertical height instead of the slant height to find the curved surface area of a cone. Explain why the answer is too small.', 'The slant height is the hypotenuse of the right triangle, so it is longer than the vertical height; πrh underestimates πrl.'),
    ])
    return dict(stem=q_, answer=ans, markingKey=f'{ans} (R1 A1)', type='explain', marks=2)


# =============================================================================================
# ch11 Statistics: Grouped Data
# =============================================================================================
def _grouped(rng, width=None, k=5):
    w = width or rng.choice([5, 10, 20])
    start = rng.choice([0, 10, 20, 40, 100, 150])
    f = [rng.randint(2, 18) for _ in range(k)]
    classes = [(start + i * w, start + (i + 1) * w) for i in range(k)]
    return classes, f


def _gtable(classes, f, var='x'):
    return '; '.join(f'{a} ≤ {var} < {b}: {fi}' for (a, b), fi in zip(classes, f))


R.facts('ch11-st1', F(
    terms=[('continuous data', 'data that can take any value in a range, such as height or time'),
           ('class interval', 'a range of values used to group data, e.g. 20 ≤ t < 30'),
           ('histogram', 'a chart for continuous grouped data with bars touching, where bar area represents frequency')],
    why=[('Explain why the bars of a histogram for continuous data touch.', 'The classes run continuously with no gaps between them, so the bars must too.'),
         ('Explain why class boundaries such as 10 ≤ x < 20 use one strict inequality.', 'It makes every value belong to exactly one class; a value of 20 goes into the next class.')],
    misc=[('A bar chart and a histogram are the same thing.', 'A bar chart shows discrete categories with gaps; a histogram shows continuous classes with touching bars.')],
))


@R.add('ch11-st1', 'C3', (1, 3), 'short')
def gtable_read(rng, slot):
    classes, f = _grouped(rng)
    i = rng.randrange(len(f))
    q_, ans = rng.choice([
        (f'The times (s) taken by students to solve a puzzle are grouped: {_gtable(classes, f, "t")}. How many students took at least {classes[i][0]} s?', str(sum(f[i:]))),
        (f'Heights (cm) of seedlings are grouped: {_gtable(classes, f, "h")}. How many seedlings were measured, and what fraction were in the class {classes[i][0]} ≤ h < {classes[i][1]}?', f'{sum(f)}; {frac(Fr(f[i], sum(f)))}'),
    ])
    return dict(stem=q_, answer=ans, markingKey=f'Correct frequencies identified (M1); {ans} (A1).', marks=2)


@R.add('ch11-st1', 'C4', (3, 5), 'multi_step')
def histogram_task(rng, slot):
    classes, f = _grouped(rng, k=4)
    w = classes[0][1] - classes[0][0]
    who = name(rng)
    return dict(stem=f'{who} records the masses (g) of {sum(f)} apples: {_gtable(classes, f, "m")}. (a) Describe how to draw an accurate histogram of these data, including the axes. (b) Identify the modal class. (c) Estimate how many apples weigh more than {classes[1][0] + w // 2} g, stating your assumption.',
                answer=f'(b) {classes[f.index(max(f))][0]} ≤ m < {classes[f.index(max(f))][1]} (c) {f[1] / 2 + sum(f[2:]):g}',
                markingKey=f'(a) continuous scale on the x-axis with class boundaries, frequency (density) on the y-axis, touching bars (C1 A1). (b) modal class (A1). (c) half of class 2 (assume values spread evenly) plus classes above: {f[1] / 2 + sum(f[2:]):g} (M1 A1).', marks=5)


@R.add('ch11-st1', 'C2', (2, 4), 'explain')
def grouped_explain(rng, slot):
    q_, ans = rng.choice([
        ('Explain one advantage and one disadvantage of grouping data into classes.', 'Advantage: a large data set becomes easier to read and display; disadvantage: the exact values are lost, so statistics can only be estimated.'),
        ('Explain why "age last birthday" is usually treated as discrete in a table but as continuous in a histogram of actual age.', 'Actual age changes continuously with time; "age last birthday" records only whole numbers.'),
        ('Explain why classes of unequal width can make a frequency histogram misleading.', 'A wider class collects more values and looks bigger even if values are less concentrated; frequency density corrects this.'),
        ('Explain why the classes 0–10, 10–20 are ambiguous and how to fix them.', 'A value of 10 could fit in both; use 0 ≤ x < 10, 10 ≤ x < 20.'),
    ])
    return dict(stem=q_, answer=ans, markingKey=f'{ans} (R1 R1)', type='explain', marks=2)


@R.add('ch11-st1', 'C1', (1, 3), 'mcq')
def data_type_mcq(rng, slot):
    cont = ['the time to run 100 m', 'the mass of a parcel', 'the height of a sunflower', 'the temperature at noon', 'the length of a leaf']
    disc = ['the number of siblings', 'shoe sizes sold', 'the number of goals scored', 'the number of cars in a car park', 'the number of pages in a book']
    c = rng.choice(cont)
    return mcq(rng, 'Which of these is an example of continuous data?', c, rng.sample(disc, 3), f'{c} can take any value in a range.')


R.facts('ch11-st2', F(
    terms=[('estimated mean', 'the mean of grouped data found using the midpoint of each class: Σ(f × midpoint) ÷ Σf'),
           ('modal class', 'the class with the highest frequency'),
           ('median class', 'the class containing the middle value of the ordered data')],
    why=[('Explain why the mean of grouped data is only an estimate.', 'The exact values are unknown; using midpoints assumes values in each class average to the midpoint.'),
         ('Explain how to find which class contains the median.', 'Find the position (n + 1)/2 and add frequencies cumulatively until that position is reached.')],
    misc=[('The estimated mean is the midpoint of the modal class.', 'The mean uses all classes: Σ(f × midpoint)/Σf.'),
          ('To find the mean of grouped data divide Σ(f × midpoint) by the number of classes.', 'Divide by the total frequency Σf, not the number of classes.')],
))


@R.add('ch11-st2', 'C3', (1, 4), 'numerical')
def gmean(rng, slot):
    classes, f = _grouped(rng)
    mids = [(a + b) / 2 for a, b in classes]
    mean = sum(fi * mi for fi, mi in zip(f, mids)) / sum(f)
    n = sum(f)
    pos = (n + 1) / 2
    cum = 0
    med = None
    for (a, b), fi in zip(classes, f):
        cum += fi
        if cum >= pos:
            med = f'{a} ≤ x < {b}'
            break
    q_ = f'The table shows the distance (km) travelled to school by {n} students: {_gtable(classes, f)}. Calculate an estimate of the mean'
    if slot.d >= 3:
        q_ += ' and state the median class.'
        ans = f'mean ≈ {mean:.3g} km; median class {med}'
    else:
        q_ += '.'
        ans = f'{mean:.3g} km'
    return dict(stem=q_, answer=ans, markingKey=f'Midpoints {", ".join(f"{m_:g}" for m_ in mids)} (M1); Σfx = {sum(fi * mi for fi, mi in zip(f, mids)):g} (M1); ÷ {n} = {mean:.3g} (A1)' + (f'; median position {pos:g} → {med} (A1).' if slot.d >= 3 else '.'), type='numerical', marks=4 if slot.d >= 3 else 3)


@R.add('ch11-st2', 'C1', (1, 3), 'mcq')
def modal_mcq(rng, slot):
    classes, f = _grouped(rng, k=4)
    if f.count(max(f)) > 1:
        return None
    i = f.index(max(f))
    opts = [f'{a} ≤ x < {b}' for a, b in classes]
    return mcq(rng, f'Frequencies: {_gtable(classes, f)}. What is the modal class?', opts[i], [o for j, o in enumerate(opts) if j != i], 'The modal class has the highest frequency.')


@R.add('ch11-st2', 'C4', (3, 5), 'multi_step')
def gmean_compare(rng, slot):
    classes, f1 = _grouped(rng, k=4)
    f2 = [max(1, fi + rng.randint(-5, 5)) for fi in f1]
    mids = [(a + b) / 2 for a, b in classes]
    m1 = sum(a * b for a, b in zip(f1, mids)) / sum(f1)
    m2 = sum(a * b for a, b in zip(f2, mids)) / sum(f2)
    a_, b_ = two_names(rng)
    return dict(stem=f'Two athletics clubs record training times (min) per session. {a_}’s club: {_gtable(classes, f1, "t")}. {b_}’s club: {_gtable(classes, f2, "t")}. Estimate each mean and comment on which club trains for longer on average, giving one reason why your comparison may be unreliable.',
                answer=f'{m1:.3g} min vs {m2:.3g} min; {a_ if m1 > m2 else b_}’s club longer', markingKey=f'Both estimated means correct (M1 A1 A1); valid comparison in context (R1); limitation: grouped estimates / different sample sizes {sum(f1)} vs {sum(f2)} (R1).', marks=5)


@R.add('ch11-st2', 'C2', (2, 4), 'explain')
def gmean_explain(rng, slot):
    classes, f = _grouped(rng, k=4)
    return dict(stem=f'For the grouped data {_gtable(classes, f)}, explain why the estimated mean could be higher or lower than the true mean.', answer='Values in a class may cluster above or below the midpoint.',
                markingKey='Midpoints assume an even spread in each class (R1); if values cluster near the lower/upper boundary the estimate is too high/low (R1).', type='explain', marks=2)


R.facts('ch11-st3', F(
    terms=[('cumulative frequency', 'the running total of frequencies up to the upper boundary of each class'),
           ('quartiles', 'the values that split ordered data into four equal parts: Q1 (25%), median (50%), Q3 (75%)'),
           ('box-and-whisker plot', 'a diagram showing minimum, Q1, median, Q3 and maximum')],
    why=[('Explain why cumulative frequency is plotted at the upper class boundary.', 'The running total counts all values up to the end of each class, so it belongs at the upper boundary.'),
         ('Explain why a cumulative frequency graph never decreases.', 'Each new class adds a non-negative frequency to the running total.')],
    misc=[('The median is read off the cumulative frequency graph at the middle of the x-axis.', 'Go across from n/2 on the cumulative frequency (vertical) axis, then read down to the x-axis.')],
))


@R.add('ch11-st3', 'C3', (1, 4), 'short')
def cumfreq(rng, slot):
    classes, f = _grouped(rng, k=5)
    cum = []
    t = 0
    for fi in f:
        t += fi
        cum.append(t)
    q_ = f'Complete a cumulative frequency table for: {_gtable(classes, f)}, and state the plotting points.'
    ans = '; '.join(f'({b}, {c})' for (a, b), c in zip(classes, cum))
    if slot.d >= 3:
        n = cum[-1]
        q_ = f'For the data {_gtable(classes, f)}, find the cumulative frequencies and state in which class the upper quartile lies.'
        pos = 0.75 * n
        cls = next(f'{a} ≤ x < {b}' for (a, b), c in zip(classes, cum) if c >= pos)
        ans = f'cumulative frequencies {", ".join(map(str, cum))}; Q3 in {cls}'
    return dict(stem=q_, answer=ans, markingKey=f'Running totals {", ".join(map(str, cum))} (A1); upper class boundaries used (A1).', marks=2 if slot.d < 3 else 3)


@R.add('ch11-st3', 'C3', (2, 4), 'short')
def boxplot(rng, slot):
    data = sorted(rng.randint(10, 90) for _ in range(rng.choice([7, 11, 15])))
    n = len(data)
    med = data[n // 2]
    lower, upper = data[:n // 2], data[n // 2 + 1:]
    q1, q3 = lower[len(lower) // 2], upper[len(upper) // 2]
    return dict(stem=f'The scores of {n} students are {", ".join(map(str, data))}. Find the five-number summary needed for a box-and-whisker plot.', answer=f'min {data[0]}, Q1 {q1}, median {med}, Q3 {q3}, max {data[-1]}',
                markingKey=f'Median {med} (A1); Q1 {q1} and Q3 {q3} (A1 A1); min and max (A1).', marks=4)


@R.add('ch11-st3', 'C4', (3, 5), 'multi_step')
def cf_interpret(rng, slot):
    n = rng.choice([40, 60, 80, 100, 120])
    q1, med, q3 = sorted(rng.sample(range(20, 80), 3))
    p90 = q3 + rng.randint(3, 12)
    who = name(rng)
    return dict(stem=f'A cumulative frequency curve for the reaction times (ms) of {n} drivers gives Q1 = {q1}, median = {med}, Q3 = {q3}, and shows that {int(0.9 * n)} drivers responded within {p90} ms. (a) Find the interquartile range. (b) What percentage responded in more than {p90} ms? (c) {who} says "half the drivers responded between {q1} and {q3} ms". Is she right? Explain.',
                answer=f'(a) {q3 - q1} ms (b) 10% (c) yes – the IQR contains the middle 50%', markingKey=f'(a) Q3 − Q1 = {q3 - q1} (A1); (b) {n - int(0.9 * n)}/{n} = 10% (M1 A1); (c) middle 50% lies between the quartiles (R1 C1).', marks=5)


@R.add('ch11-st3', 'C2', (2, 4), 'explain')
def cf_explain(rng, slot):
    q_, ans = rng.choice([
        ('Explain what a steep section of a cumulative frequency curve tells you about the data.', 'Many values fall in that interval: the data are concentrated there.'),
        ('Explain why the median from a cumulative frequency graph is an estimate.', 'The curve is drawn through grouped points assuming values are spread within classes; the exact data are unknown.'),
        ('Explain what the length of the box in a box-and-whisker plot represents.', 'The interquartile range: the spread of the middle 50% of the data.'),
    ])
    return dict(stem=q_, answer=ans, markingKey=f'{ans} (R1 R1)', type='explain', marks=2)


R.facts('ch11-st4', F(
    terms=[('interquartile range (IQR)', 'Q3 − Q1, the spread of the middle 50% of the data, not affected by extreme values'),
           ('range', 'the difference between the largest and smallest values'),
           ('outlier', 'a value far from the rest of the data, often taken as more than 1.5 × IQR beyond a quartile')],
    why=[('Explain why the IQR is often a better measure of spread than the range.', 'The range uses only the two extreme values, which may be outliers; the IQR ignores the top and bottom quarters.'),
         ('Explain why you should compare both an average and a spread when comparing two distributions.', 'Two groups can have the same average but very different consistency; the spread shows how varied the values are.')],
    misc=[('If two classes have the same median, their results are the same.', 'They may differ greatly in spread (IQR/range) and shape.')],
))


@R.add('ch11-st4', 'C3', (2, 4), 'short')
def compare_dist(rng, slot):
    a_, b_ = two_names(rng)
    m1, m2 = rng.randint(40, 70), rng.randint(40, 70)
    i1, i2 = rng.randint(5, 25), rng.randint(5, 25)
    if m1 == m2 or i1 == i2:
        return None
    return dict(stem=f'Test results: {a_}’s class has median {m1} and IQR {i1}; {b_}’s class has median {m2} and IQR {i2}. Make two comparisons in context.', answer=f'{a_ if m1 > m2 else b_}’s class scored higher on average; {a_ if i1 < i2 else b_}’s class was more consistent',
                markingKey=f'Comparison of medians in context (A1); comparison of IQRs (consistency) in context (A1).', marks=2)


@R.add('ch11-st4', 'C4', (3, 5), 'multi_step')
def outlier_task(rng, slot):
    data = sorted(rng.randint(20, 40) for _ in range(10)) + [rng.randint(70, 95)]
    data.sort()
    n = len(data)
    q1, med, q3 = data[2], data[5], data[8]
    iqr = q3 - q1
    upper = q3 + 1.5 * iqr
    return dict(stem=f'The waiting times (minutes) at a clinic were {", ".join(map(str, data))}. (a) Find the median and IQR. (b) Using the 1.5 × IQR rule, decide whether {data[-1]} is an outlier. (c) Explain which average best represents a typical wait.',
                answer=f'(a) median {med}, IQR {iqr} (b) upper fence {upper:g}: {"outlier" if data[-1] > upper else "not an outlier"} (c) median – not affected by the extreme value',
                markingKey=f'(a) quartiles {q1}, {q3} (M1), median and IQR (A1 A1); (b) fence Q3 + 1.5 × IQR (M1), conclusion (A1); (c) reasoned choice (R1).', marks=6)


@R.add('ch11-st4', 'C2', (2, 4), 'explain')
def spread_explain(rng, slot):
    a, b = rng.randint(10, 40), rng.randint(50, 90)
    return dict(stem=f'A data set has range {b - a + 40} but IQR {rng.randint(6, 15)}. Explain what this suggests about the data.', answer='There are extreme values (possible outliers); most data are tightly grouped.',
                markingKey='The middle 50% is close together (R1) while the extremes are far away, suggesting outliers (R1).', type='explain', marks=2)


# =============================================================================================
# ch12 Probability: Venn and Tree Diagrams
# =============================================================================================
R.facts('ch12-st1', F(
    terms=[('universal set', 'the set ξ (or U) of all elements under consideration'),
           ('intersection', 'A ∩ B, the elements that are in both A and B'),
           ('union', 'A ∪ B, the elements that are in A or B or both'),
           ('complement', 'A′, the elements of the universal set that are not in A')],
    why=[('Explain why n(A ∪ B) = n(A) + n(B) − n(A ∩ B).', 'Adding n(A) and n(B) counts the elements in both sets twice, so the intersection is subtracted once.'),
         ('Explain the difference between A ∩ B = ∅ and A = B.', 'A ∩ B = ∅ means the sets share no elements (disjoint); A = B means they have exactly the same elements.')],
    misc=[('A ∪ B means only the elements in both A and B.', 'That is A ∩ B; A ∪ B includes elements in either set.'),
          ('n(A′) = n(A) − n(ξ).', 'n(A′) = n(ξ) − n(A).')],
))


@R.add('ch12-st1', 'C3', (1, 4), 'short')
def venn_counts(rng, slot):
    a_only, b_only, both, neither = rng.randint(2, 15), rng.randint(2, 15), rng.randint(1, 10), rng.randint(0, 9)
    n = a_only + b_only + both + neither
    sport, music = rng.choice([('play football (F)', 'play an instrument (M)'), ('study French (F)', 'study Mandarin (M)'), ('own a bike (F)', 'own a pet (M)')])
    q_ = f'In a group of {n} students, {a_only + both} {sport}, {b_only + both} {music} and {neither} do neither. Draw a Venn diagram and find how many do both.'
    return dict(stem=q_, answer=f'{both}', markingKey=f'n(F ∪ M) = {n} − {neither} = {n - neither} (M1); {a_only + both} + {b_only + both} − {n - neither} = {both} (A1); Venn regions {a_only}, {both}, {b_only}, {neither} (A1).', marks=3)


@R.add('ch12-st1', 'C1', (1, 3), 'mcq')
def set_mcq(rng, slot):
    U = list(range(1, 13))
    A = sorted(rng.sample(U, 5))
    B = sorted(rng.sample(U, 5))
    op = rng.choice(['∩', '∪', "A′"])
    if op == '∩':
        res = sorted(set(A) & set(B))
        w = [sorted(set(A) | set(B)), sorted(set(A) - set(B)), sorted(set(B) - set(A))]
    elif op == '∪':
        res = sorted(set(A) | set(B))
        w = [sorted(set(A) & set(B)), sorted(set(A)), sorted(set(U) - set(A) - set(B))]
    else:
        res = sorted(set(U) - set(A))
        w = [sorted(set(A)), sorted(set(U) - set(B)), sorted(set(A) & set(B))]
    fmt_ = lambda s: '{' + ', '.join(map(str, s)) + '}' if s else '∅'
    stem = f'ξ = {{1, 2, …, 12}}, A = {fmt_(A)}, B = {fmt_(B)}. Find ' + ('A ∩ B.' if op == '∩' else 'A ∪ B.' if op == '∪' else 'A′.')
    return mcq(rng, stem, fmt_(res), [fmt_(x) for x in w], 'Use the definitions of intersection, union and complement.')


@R.add('ch12-st1', 'C4', (3, 5), 'multi_step')
def venn_three(rng, slot):
    abc, ab, ac, bc = rng.randint(1, 5), rng.randint(1, 6), rng.randint(1, 6), rng.randint(1, 6)
    a, b, c = rng.randint(3, 12), rng.randint(3, 12), rng.randint(3, 12)
    none = rng.randint(0, 8)
    n = abc + ab + ac + bc + a + b + c + none
    return dict(stem=f'{n} students were asked whether they like Art (A), Biology (B) and Chemistry (C). {abc} like all three; {ab + abc} like A and B; {ac + abc} like A and C; {bc + abc} like B and C; {a + ab + ac + abc} like A; {b + ab + bc + abc} like B; {c + ac + bc + abc} like C. (a) Complete a three-set Venn diagram. (b) How many like none? (c) How many like exactly one subject?',
                answer=f'(b) {none} (c) {a + b + c}', markingKey=f'Centre {abc}, pairwise-only regions {ab}, {ac}, {bc} (M1 A1); single regions {a}, {b}, {c} (A1); none = {n} − {n - none} = {none} (A1); exactly one = {a + b + c} (A1).', marks=5, gap='G5')


@R.add('ch12-st1', 'C2', (2, 4), 'explain')
def set_explain(rng, slot):
    q_, ans = rng.choice([
        ('Explain why (A ∪ B)′ is the same as A′ ∩ B′, using a Venn diagram.', 'Both describe the region outside both circles: not in A or B is the same as not in A and not in B.'),
        ('Explain why, for any sets, n(A ∩ B) ≤ n(A).', 'A ∩ B contains only elements that are also in A, so it cannot have more elements than A.'),
        ('Explain what it means for two sets to be disjoint, and how this looks on a Venn diagram.', 'They have no common elements (A ∩ B = ∅); the circles do not overlap.'),
    ])
    return dict(stem=q_, answer=ans, markingKey=f'{ans} (R1 R1)', type='explain', marks=2)


R.facts('ch12-st2', F(
    terms=[('probability of A or B', 'P(A ∪ B) = P(A) + P(B) − P(A ∩ B)'),
           ('mutually exclusive events', 'events that cannot happen at the same time, so P(A ∩ B) = 0'),
           ('complementary events', 'A and A′, with P(A′) = 1 − P(A)')],
    why=[('Explain why P(A) + P(A′) = 1.', 'Every outcome is either in A or not in A, and not both, so together they cover the whole sample space.'),
         ('Explain why you subtract P(A ∩ B) when finding P(A ∪ B).', 'Outcomes in both A and B are counted in P(A) and in P(B), so they are counted twice.')],
    misc=[('P(A ∪ B) = P(A) + P(B) for any events.', 'Only for mutually exclusive events; otherwise subtract P(A ∩ B).')],
))


@R.add('ch12-st2', 'C3', (1, 4), 'short')
def venn_prob(rng, slot):
    a_only, b_only, both, neither = rng.randint(2, 15), rng.randint(2, 15), rng.randint(1, 10), rng.randint(1, 9)
    n = a_only + b_only + both + neither
    ask = rng.choice(['A ∩ B', 'A ∪ B', "A′", "A ∩ B′", "(A ∪ B)′"])
    val = {'A ∩ B': both, 'A ∪ B': a_only + b_only + both, "A′": b_only + neither, "A ∩ B′": a_only, "(A ∪ B)′": neither}[ask]
    return dict(stem=f'A Venn diagram shows A only: {a_only}, A and B: {both}, B only: {b_only}, neither: {neither}. A person is chosen at random. Find P({ask}).', answer=frac(Fr(val, n)),
                markingKey=f'Correct region(s) identified: {val} (M1); total {n} (A1); P = {frac(Fr(val, n))} (A1).', marks=3)


@R.add('ch12-st2', 'C1', (1, 3), 'mcq')
def prob_union_mcq(rng, slot):
    pa, pb = Fr(rng.randint(2, 6), 10), Fr(rng.randint(2, 6), 10)
    pab = Fr(rng.randint(1, min(int(pa * 10), int(pb * 10)) ), 10)
    ans = pa + pb - pab
    return mcq(rng, f'P(A) = {float(pa):g}, P(B) = {float(pb):g} and P(A ∩ B) = {float(pab):g}. Find P(A ∪ B).', f'{float(ans):g}', [f'{float(pa + pb):g}', f'{float(pa * pb):g}', f'{float(pa + pb + pab):g}'], f'{float(pa):g} + {float(pb):g} − {float(pab):g} = {float(ans):g}.')


@R.add('ch12-st2', 'C4', (3, 5), 'multi_step')
def prob_venn_context(rng, slot):
    n = rng.choice([50, 60, 80, 100, 120])
    pa, pb = rng.randint(20, 45), rng.randint(15, 40)
    both = rng.randint(5, min(pa, pb) - 2)
    who = name(rng)
    return dict(stem=f'At a school in {rng.choice(CITIES)}, {n} students were surveyed: {pa} take the bus (B), {pb} cycle on some days (C), and {both} do both. (a) Draw a Venn diagram. (b) Find the probability that a randomly chosen student does neither. (c) Given that a student takes the bus, find the probability that they also cycle. (d) {who} says B and C are mutually exclusive. Is she right?',
                answer=f'(b) {frac(Fr(n - pa - pb + both, n))} (c) {frac(Fr(both, pa))} (d) no – {both} students do both', markingKey=f'Regions {pa - both}, {both}, {pb - both}, {n - pa - pb + both} (M1 A1); (b) (A1); (c) restricted sample space of {pa} (M1 A1); (d) reason (R1).', marks=6, gap='G5')


@R.add('ch12-st2', 'C2', (2, 4), 'explain')
def mutex_explain(rng, slot):
    q_, ans = rng.choice([
        ('Explain whether "rolling an even number" and "rolling a 5" on a fair die are mutually exclusive.', 'Yes: 5 is not even, so they cannot both happen.'),
        ('Explain whether "drawing a heart" and "drawing a king" from a standard pack are mutually exclusive.', 'No: the king of hearts belongs to both events.'),
        ('Explain how a Venn diagram shows that two events are mutually exclusive.', 'The circles do not overlap: the intersection is empty, P(A ∩ B) = 0.'),
    ])
    return dict(stem=q_, answer=ans, markingKey=f'{ans} (R1 A1)', type='explain', marks=2)


R.facts('ch12-st3', F(
    terms=[('independent events', 'events where the outcome of one does not change the probability of the other: P(A ∩ B) = P(A)P(B)'),
           ('dependent events', 'events where the outcome of one changes the probability of the other, e.g. drawing without replacement'),
           ('tree diagram', 'a branching diagram showing the outcomes of successive events with their probabilities on the branches')],
    why=[('Explain why you multiply along the branches of a tree diagram.', 'Following a path means the first event AND the second happen; for successive events P(A and B) = P(A) × P(B | A).'),
         ('Explain why the probabilities on branches from one point must add to 1.', 'They cover all possible outcomes at that stage, exactly one of which must happen.'),
         ('Explain why drawing two counters without replacement makes the events dependent.', 'The first counter is not returned, so the number and mix of counters changes for the second draw.')],
    misc=[('For two draws without replacement from 3 red and 2 blue, P(red then red) = 3/5 × 3/5.', 'After one red is removed there are 2 red out of 4: 3/5 × 2/4 = 3/10.'),
          ('You add along branches and multiply between branches.', 'Multiply along a path; add the probabilities of different paths.')],
))


@R.add('ch12-st3', 'C3', (1, 4), 'short')
def tree(rng, slot):
    r_, b = rng.randint(2, 8), rng.randint(2, 8)
    n = r_ + b
    replace = rng.random() < 0.5 if slot.d <= 2 else False
    ask = rng.choice(['both red', 'one of each colour', 'at least one blue'])
    if replace:
        pr, pb = Fr(r_, n), Fr(b, n)
        p = {'both red': pr * pr, 'one of each colour': 2 * pr * pb, 'at least one blue': 1 - pr * pr}[ask]
    else:
        p_rr = Fr(r_, n) * Fr(r_ - 1, n - 1)
        p_rb = Fr(r_, n) * Fr(b, n - 1)
        p_br = Fr(b, n) * Fr(r_, n - 1)
        p = {'both red': p_rr, 'one of each colour': p_rb + p_br, 'at least one blue': 1 - p_rr}[ask]
    return dict(stem=f'A bag contains {r_} red and {b} blue counters. Two are taken at random {"with" if replace else "without"} replacement. Using a tree diagram, find the probability of {ask}.', answer=frac(p),
                markingKey=f'Correct branch probabilities {"(same for both draws)" if replace else "(second draw out of " + str(n - 1) + ")"} (M1 A1); multiply along paths and add as needed (M1); {frac(p)} (A1).', marks=4 if slot.d >= 3 else 3)


@R.add('ch12-st3', 'C4', (3, 5), 'multi_step')
def tree_context(rng, slot):
    p_rain = Fr(rng.randint(2, 6), 10)
    p_late_r, p_late_n = Fr(rng.randint(3, 7), 10), Fr(rng.randint(1, 2), 10)
    who = name(rng)
    p_late = p_rain * p_late_r + (1 - p_rain) * p_late_n
    frames = [
        (f'The probability that it rains on a school day is {float(p_rain):g}. If it rains, the probability that {who}’s bus is late is {float(p_late_r):g}; otherwise it is {float(p_late_n):g}. (a) Draw a tree diagram. (b) Find the probability that the bus is late. (c) Given the bus is late, find the probability that it rained.', f'(b) {float(p_late):.3g} (c) {float(p_rain * p_late_r / p_late):.3g}'),
        (f'{who} takes a penalty kick twice. The probability she scores the first is 0.{rng.randint(5, 8)}. If she scores, the probability she scores the next rises by 0.1; if she misses it falls by 0.2. Find the probability she scores exactly once.', None),
    ]
    q_, ans = rng.choice(frames)
    if ans is None:
        p1 = float(q_.split('first is ')[1].split('.')[0] + '.' + q_.split('first is 0.')[1][0])
        ans = f'{p1 * (1 - (p1 + 0.1)) + (1 - p1) * (p1 - 0.2):.3g}'
    return dict(stem=q_, answer=ans, markingKey=f'Tree with correct conditional branches (M1 A1); multiply along paths (M1); add relevant paths (M1); {ans} (A1).', marks=5, gap='G5')


@R.add('ch12-st3', 'C2', (2, 4), 'explain')
def indep_explain(rng, slot):
    p = rng.randint(2, 8)
    q_, ans = rng.choice([
        ('Explain why tossing a coin and rolling a die are independent events.', 'The coin’s result has no effect on the die’s outcomes, so P(die outcome) stays the same.'),
        (f'A fair coin has landed heads {p} times in a row. {name(rng)} says tails is now more likely. Explain the error.', 'Each toss is independent; P(tails) is still ½ (gambler’s fallacy).'),
        ('Explain how you can test whether two events A and B are independent using probabilities.', 'Check whether P(A ∩ B) = P(A) × P(B); if equal, they are independent.'),
    ])
    return dict(stem=q_, answer=ans, markingKey=f'{ans} (R1 R1)', type='explain', marks=2)


R.facts('ch12-st4', F(
    terms=[('conditional probability', 'P(A | B), the probability of A given that B has happened: P(A ∩ B)/P(B)'),
           ('two-way table', 'a table showing frequencies for two categorical variables at once')],
    why=[('Explain why, in a two-way table, P(A | B) uses the B row (or column) total as the denominator.', 'Given B has happened, only the outcomes in B are possible, so the sample space shrinks to B.'),
         ('Explain why P(A | B) and P(B | A) are usually different.', 'They use different denominators: the number in B versus the number in A.')],
    misc=[('P(A | B) = P(A) × P(B).', 'P(A | B) = P(A ∩ B)/P(B); it equals P(A) only if A and B are independent.')],
))


@R.add('ch12-st4', 'C3', (1, 4), 'short')
def twoway(rng, slot):
    a, b, c, d = (rng.randint(5, 40) for _ in range(4))
    rows, cols = rng.choice([(('Year 9', 'Year 10'), ('walk', 'bus')), (('boys', 'girls'), ('vegetarian', 'not vegetarian')), (('morning', 'evening'), ('on time', 'delayed'))])
    n = a + b + c + d
    ask = rng.choice(['joint', 'cond_row', 'cond_col'])
    if ask == 'joint':
        q, ans = f'P({rows[0]} and {cols[1]})', frac(Fr(b, n))
    elif ask == 'cond_row':
        q, ans = f'P({cols[0]} | {rows[1]})', frac(Fr(c, c + d))
    else:
        q, ans = f'P({rows[0]} | {cols[0]})', frac(Fr(a, a + c))
    return dict(stem=f'A two-way table: {rows[0]}: {cols[0]} {a}, {cols[1]} {b}; {rows[1]}: {cols[0]} {c}, {cols[1]} {d}. Find {q}.', answer=ans,
                markingKey=f'Correct numerator and denominator from the table (M1 A1); {ans} (A1).', marks=3)


@R.add('ch12-st4', 'C4', (3, 5), 'multi_step')
def twoway_indep(rng, slot):
    a, b = rng.randint(10, 40), rng.randint(10, 40)
    k = rng.choice([1, 2, 3])
    c, d = a * k, b * k + rng.choice([0, 0, 3, -2])
    n = a + b + c + d
    pA = Fr(a + b, n)
    pB = Fr(a + c, n)
    pAB = Fr(a, n)
    indep = pAB == pA * pB
    return dict(stem=f'A survey in {rng.choice(CITIES)} records whether people exercise weekly (E) by age group. Under 30: E {a}, not E {b}. 30 and over: E {c}, not E {d}. (a) Find P(E | under 30) and P(E | 30 and over). (b) Decide, with a reason, whether exercising weekly is independent of age group.',
                answer=f'(a) {frac(Fr(a, a + b))} and {frac(Fr(c, c + d))} (b) {"independent" if indep else "not independent"}', markingKey=f'(a) conditional probabilities (M1 A1 A1); (b) compare the conditional probabilities or test P(E ∩ U) = P(E)P(U) (M1); conclusion (R1).', marks=5, gap='G5')


@R.add('ch12-st4', 'C2', (2, 4), 'explain')
def cond_explain(rng, slot):
    q_, ans = rng.choice([
        ('A test detects a condition 95% of the time. Explain why P(positive | condition) is not the same as P(condition | positive).', 'They condition on different groups; P(condition | positive) also depends on how common the condition is and on false positives.'),
        ('Explain how a two-way table makes conditional probability easier to calculate.', 'You can read the reduced sample space directly as a row or column total, then take the cell inside it.'),
        ('Explain why P(A | B) = P(A) means that A and B are independent.', 'Knowing B happened does not change the probability of A.'),
    ])
    return dict(stem=q_, answer=ans, markingKey=f'{ans} (R1 R1)', type='explain', marks=2)


@R.add('ch08-st4', 'C4', (2, 5), 'multi_step')
def proof_more2(rng, slot):
    q_, ans = rng.choice([
        ('Prove that the angle subtended at the centre of a circle is twice the angle at the circumference (case where the centre lies inside the angle).', 'Join the point on the circumference to the centre and extend; two isosceles triangles; exterior angle = 2 × base angle in each; add.'),
        ('Prove that the opposite angles of a parallelogram are equal.', 'Draw a diagonal; alternate angles and the common side give congruent triangles (ASA); corresponding angles are equal.'),
        ('Prove that the line joining the midpoints of two sides of a triangle is half the length of the third side.', 'Similar triangles with scale factor 2 (SAS similarity: common angle, sides in ratio 1 : 2).'),
        ('In triangle ABC, AD bisects angle A and AD ⊥ BC. Prove that triangle ABC is isosceles.', 'Triangles ABD and ACD: angle BAD = CAD, AD common, angles at D both 90° → ASA, so AB = AC.'),
    ])
    return dict(stem=q_, answer=ans, markingKey=f'Key construction/identification (M1); equal parts with reasons (M1 M1); conclusion (R1); logical presentation (C1). {ans}', marks=5, gap='G5')


# ---- C2 top-ups ---------------------------------------------------------------------------------
R.f['ch10-st3'].why += [
    ('Explain why a chord that passes through the centre is the longest chord of a circle.', 'It is a diameter, length 2r; any other chord is the base of an isosceles triangle with two radii, so it is shorter than r + r.'),
    ('Explain why equal chords of a circle are the same distance from the centre.', 'Each forms a right-angled triangle with a radius as hypotenuse and half the chord as a leg; equal chords give equal legs, so the third sides (distances) are equal.'),
    ('Explain why a tangent cannot pass through the inside of a circle.', 'Every point on the tangent other than the contact point is further than r from the centre, so it lies outside the circle.'),
]
R.f['ch11-st1'].why += [
    ('Explain why frequency density, not frequency, is used on the vertical axis when class widths differ.', 'Frequency density = frequency ÷ class width makes the bar area proportional to frequency, so wide classes are not exaggerated.'),
    ('Explain why a frequency table loses information compared with the raw data.', 'Only the class of each value is kept, not its exact value, so exact statistics cannot be recovered.'),
    ('Explain how to choose a sensible number of classes for a grouped frequency table.', 'Usually 5–10 classes: too few hides the shape, too many leaves classes nearly empty.'),
]
R.f['ch11-st3'].why += [
    ('Explain why the median from a cumulative frequency curve is read at n/2 on the vertical axis.', 'The median is the value with half of the data below it, i.e. a cumulative frequency of n/2.'),
    ('Explain what the two whiskers of a box plot show.', 'They run from the box to the minimum and maximum, showing the spread of the lowest and highest quarters.'),
    ('Explain why a box plot is useful for comparing two distributions.', 'It shows the median, IQR and range side by side, so centre and spread can be compared at a glance.'),
    ('Explain why a cumulative frequency curve is drawn as a smooth curve rather than straight lines between points in many textbooks.', 'It models a gradual build-up of values within classes; either is acceptable if stated, but the curve better represents continuous data.'),
]
R.f['ch12-st2'].why += [
    ('Explain why probabilities from a Venn diagram can be found by dividing region counts by the total.', 'Each person is equally likely to be chosen, so P(event) = number in the region ÷ total number.'),
    ('Explain the difference between P(A ∩ B′) and P(A′ ∩ B).', 'The first is A but not B (A only); the second is B but not A (B only).'),
    ('Explain why P(A ∪ B) can never be less than P(A).', 'A ∪ B contains every outcome of A (and possibly more).'),
    ('Explain why P(A ∩ B) can never be greater than P(A) or P(B).', 'A ∩ B is contained in both A and B.'),
]
R.f['ch12-st4'].why += [
    ('Explain why the row totals of a two-way table must add to the grand total.', 'Every item belongs to exactly one row, so the rows partition the whole data set.'),
    ('Explain how to find P(B | A) from a Venn diagram.', 'Use the region A ∩ B as the numerator and the whole of A as the denominator.'),
    ('Explain why conditional probabilities are important when interpreting medical test results.', 'The probability of having the condition given a positive result depends on how common it is; ignoring this leads to over-estimating risk.'),
    ('Explain why selecting "given that" reduces the sample space.', 'The condition rules out every outcome not in the given event, leaving only that event as the possible outcomes.'),
]
R.f['ch10-st3'].evaluate = [('The tangent to a circle at any point is unique.', ['tangent must be perpendicular to the radius at that point', 'only one line through a point is perpendicular to a given line'], ['at a corner of a non-smooth curve tangents are not unique, but a circle has none'], 'True for a circle: the perpendicular to the radius at the point is the only tangent.')]
