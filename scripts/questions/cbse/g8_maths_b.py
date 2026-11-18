"""CBSE class 8 maths (Ganita Prakash) families, chapters 5-9."""
from __future__ import annotations

import math
from fractions import Fraction as Fr

from qbank import F, ar, mcq, num, sup, frac, name, two_names, inr, num_distractors, CITIES

S = 'cbse-g8-maths-ch'


def fr(x: Fr) -> str:
    return frac(x.numerator, x.denominator)


# ---------------- ch05 Number Play ----------------
# st1 Divisibility rules and reasoning

RULES = {3: 'the sum of its digits is divisible by 3', 9: 'the sum of its digits is divisible by 9', 4: 'the number formed by its last two digits is divisible by 4',
         8: 'the number formed by its last three digits is divisible by 8', 11: 'the difference between the sums of its alternate digits is 0 or divisible by 11',
         5: 'its last digit is 0 or 5', 6: 'it is divisible by both 2 and 3'}


def c5s1_rule(r):
    k = r.choice(list(RULES))
    others = [v for kk, v in RULES.items() if kk != k]
    return mcq(f'A number is divisible by {k} if …', RULES[k], r.sample(others, 3), f'Divisibility rule for {k}.', r)


def c5s1_check(r):
    k = r.choice([3, 4, 8, 9, 11, 6])
    n = r.randint(10000, 999999)
    if r.random() < 0.5:
        n -= n % k
    yes = n % k == 0
    return {'stem': f'Without dividing, decide whether {n} is divisible by {k}. Show the test you use.', 'answer': 'Yes' if yes else 'No',
            'key': f'Rule: {RULES[k]}. {n} ÷ {k} {"leaves no remainder" if yes else f"leaves remainder {n % k}"}.',
            'distractors': ['No' if yes else 'Yes', 'Only if it is even', 'Cannot be decided without dividing']}


def c5s1_digit(r):
    k = r.choice([3, 9, 11])
    base = r.randint(100, 999)
    s = str(base)
    pos = r.randint(1, 2)
    cands = []
    for d in range(10):
        t = int(s[:pos] + str(d) + s[pos:])
        if t % k == 0:
            cands.append(d)
    shown = s[:pos] + '□' + s[pos:]
    return {'stem': f'Find all possible digits for □ so that {shown} is divisible by {k}.', 'answer': ', '.join(map(str, cands)) if cands else 'none',
            'key': f'Apply the test for {k}: {RULES[k]}. Possible digits: {", ".join(map(str, cands)) or "none"}.'}


def c5s1_why9(r):
    n = r.randint(100, 999)
    a, b, c = (int(x) for x in str(n))
    return {'stem': f'Write {n} as {a} × 100 + {b} × 10 + {c} and use it to explain why the digit-sum test for 9 works.',
            'answer': f'{n} = 99 × {a} + 9 × {b} + ({a} + {b} + {c})',
            'key': '99a + 9b is always a multiple of 9, so n is divisible by 9 exactly when a + b + c is.'}


def c5s1_lcm_word(r):
    a, b = r.choice([(12, 18), (15, 20), (8, 12), (16, 24), (10, 15), (14, 21)])
    who = name(r)
    l = a * b // math.gcd(a, b)
    return {'stem': f'Two buses leave a depot in {r.choice(CITIES)} together at 7:00 a.m. One returns every {a} minutes and the other every {b} minutes. When will they next be at the depot together?',
            'answer': f'After {l} minutes', 'key': f'LCM({a}, {b}) = {l} minutes.'}


def c5s1_ar(r):
    n = r.randint(100, 999) * 9
    return ar(f'{n} is divisible by 3.', f'{n} is divisible by 9, and every multiple of 9 is a multiple of 3.', 'a', 'R explains A.')


def c5s1_claim(r):
    return {'stem': r.choice(['A student claims: "If a number is divisible by 4 and by 6, it must be divisible by 24." Test the claim and explain.',
                              'A student claims: "If a number is divisible by 2 and by 4, it must be divisible by 8." Test the claim and explain.']),
            'answer': 'False', 'key': 'Counter-example 12 (or 4): divisible by both but not by the product, because the divisors share a factor; the correct conclusion uses the LCM.'}


def c5s1_three_digit(r):
    k = r.choice([7, 11, 13])
    n = r.randint(100, 999)
    return {'stem': f'Take any three-digit number, e.g. {n}, and write it twice to form a six-digit number {n}{n}. Show that the result is always divisible by {k}.',
            'answer': f'{n}{n} = {n} × 1001 = {n} × 7 × 11 × 13', 'key': 'abcabc = abc × 1001 and 1001 = 7 × 11 × 13.'}


def c5s1_remainder(r):
    k = r.choice([3, 9])
    n = r.randint(1000, 99999)
    ds = sum(int(x) for x in str(n))
    return {'stem': f'Find the remainder when {n} is divided by {k}, using only its digit sum.', 'answer': str(n % k),
            'key': f'Digit sum {ds}; {ds} leaves remainder {ds % k} on division by {k}, so {n} leaves {n % k}.',
            'distractors': [str(x) for x in r.sample([x for x in range(k) if x != n % k] + [k], 3)]}


# st2 Number patterns, magic squares, puzzles

def c5s2_magic_sum(r):
    a = r.randint(1, 20)
    return {'stem': f'A 3 × 3 magic square uses the nine consecutive numbers {a} to {a + 8}, each once. What is the magic sum?',
            'answer': str(3 * (a + 4)), 'key': f'Total {9 * (a + 4)} split equally over 3 rows: {3 * (a + 4)}.',
            'distractors': num_distractors(3 * (a + 4), 9 * (a + 4), a + 4, 3 * (a + 8))}


def c5s2_centre(r):
    a = r.randint(1, 30)
    return {'stem': f'In a 3 × 3 magic square made of {a}, {a + 1}, …, {a + 8}, explain why the centre must be {a + 4}.',
            'answer': str(a + 4), 'key': 'The four lines through the centre (middle row, column, two diagonals) add to 4S and use the centre four times: 4S = total + 3 × centre gives centre = S/3.'}


def c5s2_complete(r):
    base = [[2, 7, 6], [9, 5, 1], [4, 3, 8]]
    k = r.randint(0, 10)
    sq = [[x + k for x in row] for row in base]
    hide = r.sample([(i, j) for i in range(3) for j in range(3) if (i, j) != (1, 1)], 3)
    grid = ' / '.join(' '.join('□' if (i, j) in hide else str(sq[i][j]) for j in range(3)) for i in range(3))
    return {'stem': f'Complete the magic square (rows separated by /): {grid}.', 'answer': ', '.join(str(sq[i][j]) for i, j in sorted(hide)),
            'key': f'Magic sum {3 * (5 + k)}; each missing entry = sum − the other two in its row or column.'}


def c5s2_next(r):
    kind = r.choice(['tri', 'sq', 'diff', 'fib'])
    if kind == 'tri':
        n = r.randint(3, 6)
        seq = [k * (k + 1) // 2 for k in range(n, n + 5)]
        rule = 'triangular numbers (add one more each time)'
    elif kind == 'sq':
        n = r.randint(2, 6)
        seq = [k * k for k in range(n, n + 5)]
        rule = 'consecutive squares (differences are consecutive odd numbers)'
    elif kind == 'diff':
        a, d, e = r.randint(1, 9), r.randint(2, 5), r.randint(1, 3)
        seq = [a]
        for i in range(4):
            seq.append(seq[-1] + d + e * i)
        rule = f'differences {d}, {d + e}, {d + 2 * e}, … increase by {e}'
    else:
        a, b = r.randint(1, 4), r.randint(2, 6)
        seq = [a, b]
        while len(seq) < 5:
            seq.append(seq[-1] + seq[-2])
        rule = 'each term is the sum of the two before it (Virahanka–Fibonacci)'
    nxt = seq[-1]
    shown = seq[:-1]
    return {'stem': f'Find the next number in the pattern {", ".join(map(str, shown))}, … and state the rule.', 'answer': str(nxt),
            'key': f'Rule: {rule}. Next term {nxt}.', 'distractors': num_distractors(nxt, nxt + 1, shown[-1] * 2, nxt - 2)}


def c5s2_virahanka(r):
    n = r.randint(6, 10)
    f = [1, 2]
    while len(f) < n:
        f.append(f[-1] + f[-2])
    return {'stem': f'A poem line of {n} beats is made of short syllables (1 beat) and long syllables (2 beats). Using Virahanka\'s method, how many different rhythms are possible?',
            'answer': str(f[n - 1]), 'key': f'Rhythms for n beats = rhythms for n − 1 (start short) + rhythms for n − 2 (start long): 1, 2, 3, 5, 8, … → {f[n - 1]}.'}


def c5s2_calendar(r):
    a = r.randint(1, 15)
    return {'stem': f'On a calendar, a 3 × 3 block of dates has {a} in its top-left corner. Without adding all nine, find the sum of the dates in the block and explain the shortcut.',
            'answer': str(9 * (a + 8)), 'key': f'The centre date is {a} + 8 = {a + 8}; the nine dates pair up around it, so the sum = 9 × {a + 8} = {9 * (a + 8)}.'}


def c5s2_ar(r):
    return ar('The magic sum of a 3 × 3 magic square using 1 to 9 is 15.', 'The numbers 1 to 9 add up to 45 and there are three rows.', 'a', '45 ÷ 3 = 15.')


def c5s2_kaprekar(r):
    while True:
        n = r.randint(1000, 9998)
        if len(set(str(n))) >= 2:
            break
    d = sorted(str(n))
    big, small = int(''.join(reversed(d))), int(''.join(d))
    return {'stem': f'Start with {n}. Arrange its digits to make the largest and the smallest numbers and subtract. Write the result, then repeat twice more. What famous number does this process always reach?',
            'answer': '6174', 'key': f'First step: {big} − {small} = {big - small}. Repeating always reaches 6174 (Kaprekar\'s constant) within 7 steps.'}


# st3 Letters for digits / cryptarithms

def c5s3_rules(r):
    return {'stem': 'State two basic rules followed in letters-for-digits puzzles.', 'answer': 'Each letter stands for one digit and different letters for different digits; a number cannot begin with 0.',
            'key': 'Any two correct rules.'}


def c5s3_simple(r):
    a = r.randint(1, 8)
    b = r.randint(0, 9)
    # AB + AB = ? style:  A B + B A = number
    x = 10 * a + b
    y = 10 * b + a
    return {'stem': f'In the sum  A B + B A = {x + y}, A and B are different digits and A = {a}. Find B and check.', 'answer': f'B = {b}',
            'key': f'AB + BA = 11(A + B) = {x + y} → A + B = {(x + y) // 11} → B = {b}. Check: {x} + {y} = {x + y}.'}


def c5s3_11(r):
    s = r.randint(4, 16)
    return {'stem': f'Explain why the two-digit number AB plus its reverse BA is always a multiple of 11. If AB + BA = {11 * s}, what is A + B?',
            'answer': f'A + B = {s}', 'key': f'(10A + B) + (10B + A) = 11(A + B); 11(A + B) = {11 * s} → A + B = {s}.'}


def c5s3_mult(r):
    a = r.randint(4, 9)
    p = a * a
    return {'stem': f'In the multiplication A × A = B{p % 10}, where B{p % 10} is a two-digit number and A, B are digits, find A and B.', 'answer': f'A = {a}, B = {p // 10}',
            'key': f'Only digits whose square ends in {p % 10} and is two-digit work: {a} × {a} = {p}.'}


def c5s3_carry(r):
    return {'stem': 'In the addition  A + A + A = BA  (BA is a two-digit number), find A and B, explaining each step.', 'answer': 'A = 5, B = 1',
            'key': '3A ends in A, so 2A ends in 0: A = 0 or 5. A = 0 gives 0, not a two-digit number; A = 5 gives 15, so B = 1.'}


def c5s3_classic(r):
    p = r.choice([('In SEND + MORE = MONEY (each letter a different digit), what must M be? Justify.', 'M = 1',
                   'Two four-digit numbers add to less than 20 000, so the carried digit M is 1.'),
                  ('In AB × 3 = CCC (CCC is a three-digit number with all digits equal), find AB and C.', 'AB = 37, C = 1',
                   'CCC = 111 × C = 3 × 37 × C; AB = 37C must be two-digit and C = 1 gives 37 × 3 = 111 (C = 2 gives 74 × 3 = 222 too, so both 37 and 74 work).'),
                  ('In AB × 9 = A0B (a three-digit number with middle digit 0), find A and B.', 'A = 4, B = 5', '45 × 9 = 405; checking other two-digit numbers shows no other solution.')])
    return {'stem': p[0], 'answer': p[1], 'key': p[2]}


def c5s3_ar(r):
    return ar('In AB + BA = 99, A + B = 9.', 'AB + BA = 11(A + B).', 'a', '11(A + B) = 99 gives A + B = 9.')


def c5s3_reverse(r):
    a = r.randint(2, 9)
    b = r.randint(1, a - 1)
    return {'stem': f'The difference between a two-digit number AB and its reverse BA is always a multiple of which number? Use {10 * a + b} to check.',
            'answer': '9', 'key': f'(10A + B) − (10B + A) = 9(A − B); {10 * a + b} − {10 * b + a} = {9 * (a - b)} = 9 × {a - b}.',
            'distractors': ['11', '10', '7']}


# ---------------- ch06 We Distribute, Yet Things Multiply ----------------
# st1 Distributive property with numbers

def c6s1_expand(r):
    a, b, c = r.randint(3, 19), r.randint(10, 90), r.randint(1, 9)
    return {'stem': f'Write {a} × ({b} + {c}) using the distributive property and evaluate.', 'answer': str(a * (b + c)),
            'key': f'{a} × {b} + {a} × {c} = {a * b} + {a * c} = {a * (b + c)}.', 'distractors': num_distractors(a * (b + c), a * b + c, a + b * c, a * b * c)}


def c6s1_mental(r):
    a = r.randint(12, 99)
    b = r.choice([99, 98, 101, 102, 999, 1001])
    near = round(b, -1) if b < 200 else round(b, -2)
    d = b - near
    return {'stem': f'Use the distributive property to find {a} × {b} mentally.', 'answer': str(a * b),
            'key': f'{a} × ({near} {"+" if d > 0 else "−"} {abs(d)}) = {a * near} {"+" if d > 0 else "−"} {a * abs(d)} = {a * b}.',
            'distractors': num_distractors(a * b, a * near, a * near + d, a * b + 10)}


def c6s1_common(r):
    a, b, c = r.randint(11, 99), r.randint(11, 60), r.randint(11, 60)
    return {'stem': f'Evaluate {a} × {b} + {a} × {c} by first taking the common factor out.', 'answer': str(a * (b + c)),
            'key': f'{a} × ({b} + {c}) = {a} × {b + c} = {a * (b + c)}.'}


def c6s1_area(r):
    a, b, c = r.randint(5, 15), r.randint(3, 9), r.randint(2, 8)
    return {'stem': f'A rectangle of width {a} cm is made of two smaller rectangles of lengths {b} cm and {c} cm placed side by side. Explain, using area, why {a} × ({b} + {c}) = {a} × {b} + {a} × {c}.',
            'answer': f'Both sides give the total area {a * (b + c)} cm².', 'key': 'Whole area = sum of the two part areas.'}


def c6s1_error(r):
    a, b, c = r.randint(3, 9), r.randint(10, 40), r.randint(2, 9)
    return {'stem': f'A student writes {a} × ({b} + {c}) = {a} × {b} + {c} = {a * b + c}. Explain the error and give the correct value.',
            'answer': str(a * (b + c)), 'key': f'The {a} must multiply both terms: {a * b} + {a * c} = {a * (b + c)}.'}


def c6s1_ar(r):
    a = r.randint(11, 30)
    return ar(f'{a} × 101 = {a * 101}.', f'{a} × 101 = {a} × 100 + {a} × 1.', 'a', 'Distributive property gives the value.')


def c6s1_shop(r):
    who = name(r)
    n = r.randint(12, 40)
    p1, p2 = r.randint(35, 90), r.randint(15, 60)
    return {'stem': f'{who} buys {n} notebooks at {inr(p1)} each and {n} pens at {inr(p2)} each. Show two ways of finding the total cost and explain why they agree.',
            'answer': inr(n * (p1 + p2)), 'key': f'{n} × {p1} + {n} × {p2} = {n} × ({p1} + {p2}) = {inr(n * (p1 + p2))}.'}


def c6s1_subtract(r):
    a, b = r.randint(15, 60), r.randint(101, 140)
    c = r.randint(2, 9)
    return {'stem': f'Evaluate {a} × {b} − {a} × {b - c * 10} using the distributive property.', 'answer': str(a * c * 10),
            'key': f'{a} × ({b} − {b - c * 10}) = {a} × {c * 10} = {a * c * 10}.'}


# st2 Algebraic expressions: terms, like terms, addition

V = ['x', 'y', 'a', 'b', 'm', 'p']


def term(c, v):
    if c == 1:
        return v
    if c == -1:
        return '−' + v
    return num(c) + v


def poly(terms):
    """[(coef, 'x²'), ...] -> '12x² + 3xy − y²' (drops zero terms, hides coefficient 1)."""
    out = []
    for c, v in terms:
        if c == 0:
            continue
        mag = '' if abs(c) == 1 and v else str(abs(c))
        sign = '−' if c < 0 else '+'
        out.append((sign, f'{mag}{v}'))
    if not out:
        return '0'
    first = ('−' if out[0][0] == '−' else '') + out[0][1]
    return ' '.join([first] + [f'{sg} {t}' for sg, t in out[1:]])


def c6s2_coeff(r):
    x, y = r.sample(V, 2)
    a, b, c = r.randint(2, 9), r.randint(2, 9), r.randint(2, 15)
    return {'stem': f'In {a}{x}²{y} − {b}{x}{y} + {c}, what is the coefficient of {x}{y} and what is the constant term?', 'answer': f'−{b}; {c}',
            'key': f'The term is −{b}{x}{y}, so its coefficient is −{b}; the constant term is {c}.',
            'distractors': [f'{b}; {c}', f'−{b}; 0', f'{a}; {c}']}


def c6s2_like(r):
    x, y = r.sample(V, 2)
    t = [f'{r.randint(2, 9)}{x}{y}', f'{r.randint(2, 9)}{x}²', f'{r.randint(2, 9)}{y}{x}', f'{r.randint(2, 9)}{x}', f'{r.randint(2, 9)}{x}{y}²']
    return mcq(f'Which pair consists of like terms?', f'{t[0]} and {t[2]}', [f'{t[1]} and {t[3]}', f'{t[0]} and {t[4]}', f'{t[1]} and {t[0]}'],
               f'{x}{y} and {y}{x} have the same variables with the same powers.', r)


def c6s2_add(r):
    x, y = r.sample(V, 2)
    a, b, c, d, e, f = (r.randint(1, 9) for _ in range(6))
    return {'stem': f'Add {a}{x}² − {b}{x}{y} + {c}{y}² and {d}{x}² + {e}{x}{y} − {f}{y}².',
            'answer': poly([(a + d, f'{x}²'), (e - b, f'{x}{y}'), (c - f, f'{y}²')]),
            'key': 'Group like terms and add their coefficients.'}


def c6s2_sub(r):
    x = r.choice(V)
    a, b, c, d = r.randint(3, 9), r.randint(1, 9), r.randint(1, 9), r.randint(1, 9)
    return {'stem': f'Subtract {c}{x} − {d} from {a}{x} + {b}.', 'answer': poly([(a - c, x), (b + d, '')]),
            'key': f'({a}{x} + {b}) − ({c}{x} − {d}) = {a}{x} + {b} − {c}{x} + {d}; the sign of every term in the bracket changes.',
            'gap': 'G3'}


def c6s2_explain(r):
    x = r.choice(V)
    return {'stem': f'Explain in one line why 3{x} + 2{x}² cannot be simplified to 5{x}³.', 'answer': f'3{x} and 2{x}² are unlike terms, so they cannot be combined.',
            'key': 'Only like terms (same variables, same powers) can be added.'}


def c6s2_perimeter(r):
    x = r.choice(['x', 'a', 'm'])
    a, b, c = r.randint(2, 6), r.randint(1, 9), r.randint(1, 5)
    return {'stem': f'The sides of a triangle are ({a}{x} + {b}) cm, ({a + 1}{x} − {c}) cm and ({x} + {b + c}) cm. Find its perimeter, and its value when {x} = {r.randint(2, 6)}.',
            'answer': f'({2 * a + 2}{x} + {2 * b}) cm', 'key': f'Add like terms: {a}{x} + {a + 1}{x} + {x} = {2 * a + 2}{x}; {b} − {c} + {b + c} = {2 * b}.'}


def c6s2_ar(r):
    x = r.choice(V)
    return ar(f'4{x}²y and 7y{x}² are like terms.', 'Like terms have the same variables raised to the same powers.', 'a', 'R is the definition that makes A true.')


def c6s2_age(r):
    who, other = two_names(r)
    k = r.randint(3, 9)
    return {'stem': f'{who} is x years old. {other} is {k} years older than twice {who}\'s age. Write an expression for (i) {other}\'s age, (ii) the sum of their ages in 5 years.',
            'answer': f'(i) 2x + {k} (ii) 3x + {k + 10}', 'key': f'(i) 2x + {k}. (ii) (x + 5) + (2x + {k} + 5) = 3x + {k + 10}.'}


# st3 Multiplying expressions (monomial × binomial, binomial × binomial)

def c6s3_mono(r):
    a, b = r.randint(2, 9), r.randint(2, 9)
    p, q = r.randint(1, 3), r.randint(1, 3)
    x = r.choice(['x', 'a', 'y'])
    return {'stem': f'Find ({a}{x}{sup(p) if p > 1 else ""})(−{b}{x}{sup(q) if q > 1 else ""}).', 'answer': f'−{a * b}{x}{sup(p + q)}',
            'key': f'Multiply coefficients ({a} × −{b} = −{a * b}) and add powers ({p} + {q} = {p + q}).',
            'distractors': [f'{a * b}{x}{sup(p + q)}', f'−{a * b}{x}{sup(p * q)}', f'−{a + b}{x}{sup(p + q)}']}


def c6s3_mono_bi(r):
    a, b, c = r.randint(2, 9), r.randint(2, 9), r.randint(1, 9)
    return {'stem': f'Multiply {a}x by ({b}x − {c}).', 'answer': f'{a * b}x² − {a * c}x', 'key': f'{a}x × {b}x − {a}x × {c} = {a * b}x² − {a * c}x.',
            'distractors': [f'{a * b}x² − {c}', f'{a * b}x − {a * c}x', f'{a * b}x² + {a * c}x']}


def c6s3_bi_bi(r):
    a, b, c, d = r.randint(1, 5), r.randint(1, 9), r.randint(1, 5), r.randint(1, 9)
    s1, s2 = r.choice([1, -1]), r.choice([1, -1])
    B, D = s1 * b, s2 * d
    mid = a * D + B * c
    const = B * D
    def sg(v, t=''):
        return f'{"+" if v >= 0 else "−"} {abs(v)}{t}'
    return {'stem': f'Multiply ({term(a, "x")} {sg(B)}) by ({term(c, "x")} {sg(D)}).',
            'answer': poly([(a * c, 'x²'), (mid, 'x'), (const, '')]),
            'key': f'FOIL: {a * c}x² + ({a}×{D} + {B}×{c})x + ({B})({D}).'}


def c6s3_area(r):
    a, b, c = r.randint(2, 6), r.randint(1, 7), r.randint(1, 5)
    return {'stem': f'A rectangular plot has length ({a}x + {b}) m and breadth (x + {c}) m. Find its area as an expression, and the area when x = {r.randint(2, 5)} m.',
            'answer': f'({a}x² + {a * c + b}x + {b * c}) m²', 'key': f'({a}x + {b})(x + {c}) = {a}x² + {a * c}x + {b}x + {b * c}.'}


def c6s3_error(r):
    a, b = r.randint(2, 9), r.randint(2, 9)
    return {'stem': f'A student writes (x + {a})(x + {b}) = x² + {a * b}. Find the mistake using x = 1.', 'answer': f'Missing middle term {a + b}x; correct x² + {a + b}x + {a * b}',
            'key': f'At x = 1: LHS = {(1 + a) * (1 + b)}, RHS = {1 + a * b}; the cross terms {a}x and {b}x were lost.'}


def c6s3_ar(r):
    a = r.randint(2, 9)
    return ar(f'(x + {a})(x − {a}) = x² − {a * a}.', 'The middle terms +' + f'{a}x and −{a}x cancel.', 'a', 'Expanding gives x² − ' + f'{a}x + {a}x − {a * a}.')


def c6s3_three(r):
    a, b = r.randint(1, 4), r.randint(1, 4)
    return {'stem': f'Simplify (x + {a})(x − {b}) + (x − {a})(x + {b}).', 'answer': f'2x² − {2 * a * b}',
            'key': f'First: x² + {a - b}x − {a * b}; second: x² + {b - a}x − {a * b}; sum 2x² − {2 * a * b}.'}


def c6s3_case(r):
    w = r.randint(2, 5)
    return {'stem': (f'A photo frame is x cm by (x + {w}) cm. A border of width 2 cm is added all round. '
                     f'(i) Write the outer length and breadth. (ii) Find the outer area as an expression. (iii) Find the area of the border alone.'),
            'answer': f'(i) (x + 4), (x + {w + 4}) (ii) x² + {w + 8}x + {4 * (w + 4)} (iii) 8x + {4 * (w + 4)}',
            'key': f'(iii) outer − inner = (x² + {w + 8}x + {4 * (w + 4)}) − (x² + {w}x) = 8x + {4 * (w + 4)}.'}


def c6s3_number(r):
    a = r.randint(21, 89)
    return {'stem': f'Use (x − 1)(x + 1) = x² − 1 to find {a} × {a + 2} mentally.', 'answer': str(a * (a + 2)),
            'key': f'({a + 1} − 1)({a + 1} + 1) = {a + 1}² − 1 = {(a + 1) ** 2} − 1 = {a * (a + 2)}.'}


# ---------------- ch07 Proportional Reasoning-1 ----------------
# st1 Ratio, unitary method and scaling

def c7s1_simplify(r):
    a, b = r.randint(2, 9), r.randint(2, 9)
    while math.gcd(a, b) != 1 or a == b:
        a, b = r.randint(2, 9), r.randint(2, 9)
    k = r.randint(3, 15)
    return {'stem': f'Simplify the ratio {a * k} : {b * k}.', 'answer': f'{a} : {b}', 'key': f'Divide both by the HCF {k}.',
            'distractors': [f'{b} : {a}', f'{a * k // math.gcd(a * k, 2)} : {b * k // math.gcd(a * k, 2)}' if (a * k) % 2 == 0 and (b * k) % 2 == 0 and k % 2 == 0 else f'{a + 1} : {b}', f'{a} : {b + 1}']}


def c7s1_unitary(r):
    n1 = r.randint(3, 12)
    p = r.randint(15, 95)
    n2 = r.randint(5, 30)
    item = r.choice(['notebooks', 'pens', 'kg of rice', 'litres of milk', 'mangoes'])
    return {'stem': f'If {n1} {item} cost {inr(n1 * p)}, what do {n2} {item} cost?', 'answer': inr(n2 * p),
            'key': f'One costs {inr(n1 * p)} ÷ {n1} = {inr(p)}; {n2} cost {inr(n2 * p)}.',
            'distractors': [inr(n1 * p + n2), inr(n2 * p + p), inr(round(n1 * p * n1 / n2))]}


def c7s1_share(r):
    a, b = r.randint(1, 5), r.randint(2, 7)
    k = r.randint(50, 400)
    who1, who2 = two_names(r)
    return {'stem': f'{who1} and {who2} share {inr((a + b) * k)} in the ratio {a} : {b}. How much does each get?', 'answer': f'{who1} {inr(a * k)}, {who2} {inr(b * k)}',
            'key': f'Total parts {a + b}; one part = {inr(k)}.'}


def c7s1_map(r):
    s = r.choice([25000, 50000, 100000, 200000])
    cm = round(r.uniform(2, 12), 1)
    km = cm * s / 100000
    return {'stem': f'A map has scale 1 : {s:,}. Two towns are {cm} cm apart on the map. What is the actual distance in km?'.replace(',', ' '),
            'answer': f'{num(km)} km', 'key': f'{cm} × {s} cm = {num(cm * s)} cm = {num(km)} km.'}


def c7s1_recipe(r):
    who = name(r)
    serves, want = r.choice([(4, 6), (4, 10), (6, 9), (5, 8), (3, 7)])
    rice = r.choice([200, 250, 300, 150])
    return {'stem': f'{who}\'s recipe for khichdi uses {rice} g of rice for {serves} people. How much rice is needed for {want} people?', 'answer': f'{num(rice * want / serves)} g',
            'key': f'{rice} ÷ {serves} × {want} = {num(rice * want / serves)} g.'}


def c7s1_compare(r):
    a1, b1 = r.randint(2, 7), r.randint(3, 9)
    a2, b2 = r.randint(2, 7), r.randint(3, 9)
    while a1 * b2 == a2 * b1:
        a2 += 1
    juice = r.choice(['mango pulp to water', 'sugar to lemon juice', 'cement to sand', 'red paint to white paint'])
    stronger = 'first' if a1 / b1 > a2 / b2 else 'second'
    return {'stem': f'Mixture 1 has {juice} in the ratio {a1} : {b1}; mixture 2 has it in the ratio {a2} : {b2}. Which mixture has the larger share of the first ingredient? Explain.',
            'answer': f'The {stronger} mixture',
            'key': f'Compare {a1}/{a1 + b1} = {a1 / (a1 + b1):.3f} with {a2}/{a2 + b2} = {a2 / (a2 + b2):.3f} (or {a1}/{b1} with {a2}/{b2}).'}


def c7s1_ar(r):
    return ar('The ratio 15 : 25 is equivalent to 3 : 5.', 'Multiplying or dividing both terms of a ratio by the same non-zero number gives an equivalent ratio.', 'a', 'Divide both by 5.')


def c7s1_scaling(r):
    w, h = r.choice([(4, 6), (5, 7), (8, 10), (3, 5)])
    k = r.choice([1.5, 2.5, 3])
    return {'stem': f'A {w} cm × {h} cm photo is enlarged so that its width becomes {num(w * k)} cm. What is the new height, and by what factor does the area change?',
            'answer': f'{num(h * k)} cm; area × {num(k * k)}', 'key': f'Scale factor {k}; lengths × {k}, area × {k}² = {num(k * k)}.'}


# st2 Direct proportion

def c7s2_const(r):
    return mcq('If x and y are in direct proportion, which quantity stays constant?', 'x ÷ y', ['x × y', 'x + y', 'x − y'], 'Direct proportion: x/y = k.', r)


def c7s2_table(r):
    k = r.randint(2, 15)
    xs = sorted(r.sample(range(2, 20), 3))
    miss = r.randint(25, 60)
    return {'stem': f'x and y are in direct proportion: x = {xs[0]}, {xs[1]}, {xs[2]}, {miss}; y = {xs[0] * k}, {xs[1] * k}, {xs[2] * k}, ?. Find the missing value.', 'answer': str(miss * k),
            'key': f'y/x = {k}; y = {k} × {miss} = {miss * k}.', 'distractors': num_distractors(miss * k, miss + k, miss * k + k, xs[2] * k + miss)}


def c7s2_fuel(r):
    km1 = r.randint(80, 240)
    l1 = r.choice([4, 5, 6, 8, 10, 12])
    l2 = r.randint(15, 40)
    who = name(r)
    return {'stem': f'{who}\'s family car covers {km1} km on {l1} litres of petrol. How far will it go on {l2} litres?', 'answer': f'{num(km1 * l2 / l1)} km',
            'key': f'{km1} ÷ {l1} = {num(km1 / l1)} km per litre; × {l2} = {num(km1 * l2 / l1)} km.'}


def c7s2_check(r):
    k = r.randint(2, 9)
    xs = sorted(r.sample(range(2, 15), 3))
    ys = [x * k for x in xs]
    if r.random() < 0.5:
        ys[2] += r.randint(1, 3)
    ok = all(y == x * k for x, y in zip(xs, ys))
    return {'stem': f'Is y directly proportional to x? x: {", ".join(map(str, xs))}; y: {", ".join(map(str, ys))}. Explain.', 'answer': 'Yes' if ok else 'No',
            'key': 'Check whether y/x is the same for every pair: ' + ', '.join(f'{y}/{x} = {num(y / x)}' for x, y in zip(xs, ys)) + '.'}


def c7s2_explain(r):
    return {'stem': r.choice(['Explain why the cost of petrol and the number of litres bought are in direct proportion, but a person\'s age and height are not.',
                              'Explain why the number of pages printed and the time a printer runs are in direct proportion, but the time taken and the number of workers are not.']),
            'answer': 'In direct proportion the ratio stays constant; the second pair does not keep a constant ratio.', 'key': 'Constant-ratio test applied to both situations.'}


def c7s2_ar(r):
    return ar('If 5 pens cost ₹60, then 8 pens cost ₹96.', 'Cost is directly proportional to the number of pens when the price per pen is fixed.', 'a', '60 ÷ 5 × 8 = 96.')


def c7s2_shadow(r):
    h1, s1 = r.choice([(6, 4), (12, 8), (15, 9), (3, 2)])
    s2 = r.randint(10, 30)
    return {'stem': f'At 4 p.m. a {h1} m pole casts a {s1} m shadow. At the same time a tree casts a {s2} m shadow. How tall is the tree?', 'answer': f'{num(h1 * s2 / s1)} m',
            'key': f'Height : shadow is constant: {h1}/{s1} × {s2} = {num(h1 * s2 / s1)} m.'}


def c7s2_case(r):
    rate = r.choice([45, 60, 75, 80])
    return {'stem': (f'An auto-rickshaw meter charges a fixed {inr(30)} plus {inr(rate // 5)} per km. '
                     f'(i) Find the fare for 5 km and for 10 km. (ii) Is the fare directly proportional to the distance? Explain. (iii) Which part of the fare is proportional to the distance?'),
            'answer': f'(i) {inr(30 + rate)}, {inr(30 + 2 * rate)} (ii) No (iii) the per-km part',
            'key': f'(ii) {30 + rate}/5 ≠ {30 + 2 * rate}/10 because of the fixed {inr(30)}; (iii) the distance charge {inr(rate // 5)} × km.'}


# st3 Inverse proportion

def c7s3_const(r):
    return mcq('If x and y are in inverse proportion, which quantity is constant?', 'x × y', ['x ÷ y', 'x + y', 'x − y'], 'Inverse proportion: xy = k.', r)


def c7s3_workers(r):
    w1 = r.randint(4, 15)
    d1 = r.randint(6, 30)
    w2 = r.choice([x for x in range(3, 40) if (w1 * d1) % x == 0 and x != w1])
    return {'stem': f'{w1} workers can build a wall in {d1} days. How many days will {w2} workers take, working at the same rate?', 'answer': f'{w1 * d1 // w2} days',
            'key': f'Worker-days = {w1} × {d1} = {w1 * d1}; ÷ {w2} = {w1 * d1 // w2}.',
            'distractors': [f'{round(d1 * w2 / w1)} days', f'{d1 + w1 - w2} days', f'{w1 * d1} days']}


def c7s3_speed(r):
    v1 = r.choice([40, 45, 50, 60])
    t1 = r.choice([3, 4, 5, 6])
    v2 = r.choice([v for v in (30, 36, 40, 48, 60, 72, 75, 80, 90) if (v1 * t1) % v == 0 and v != v1])
    return {'stem': f'A bus travelling at {v1} km/h takes {t1} hours from {r.choice(CITIES)} to the next city. How long will it take at {v2} km/h?', 'answer': f'{num(v1 * t1 / v2)} h',
            'key': f'Distance = {v1 * t1} km (constant); time = {v1 * t1} ÷ {v2}.'}


def c7s3_food(r):
    n1 = r.randint(30, 80)
    d1 = r.randint(20, 40)
    extra = r.choice([10, 20, 30, 40])
    n2 = n1 + extra
    d2 = n1 * d1 / n2
    return {'stem': f'A hostel has food for {n1} students for {d1} days. If {extra} more students join, how long will the food last?', 'answer': f'{num(round(d2, 1))} days',
            'key': f'Student-days {n1 * d1}; ÷ {n2} = {num(round(d2, 2))}.'}


def c7s3_identify(r):
    pairs = [('number of taps filling a tank and time to fill it', 'inverse'), ('number of pens and their cost', 'direct'),
             ('speed and time for a fixed journey', 'inverse'), ('length of cloth and its price', 'direct'),
             ('number of people sharing a pizza and the share each gets', 'inverse'), ('distance and fuel used at a steady speed', 'direct')]
    p, kind = r.choice(pairs)
    return {'stem': f'Are these in direct or inverse proportion: {p}? Give a reason.', 'answer': kind.capitalize(),
            'key': f'{"Ratio" if kind == "direct" else "Product"} stays constant.', 'distractors': ['Direct' if kind == 'inverse' else 'Inverse', 'Neither', 'Both']}


def c7s3_explain(r):
    return {'stem': 'A student says "if one quantity increases when the other decreases, they must be in inverse proportion." Give a counter-example.',
            'answer': 'e.g. y = 10 − x: y falls as x rises, but xy is not constant.', 'key': 'Inverse proportion needs xy constant, not just opposite movement.'}


def c7s3_ar(r):
    return ar('If 6 pipes fill a tank in 4 hours, 8 pipes fill it in 3 hours.', 'The number of pipes and the time taken are inversely proportional.', 'a', '6 × 4 = 8 × 3 = 24.')


def c7s3_mixed(r):
    w1, h1, d1 = r.choice([(8, 6, 10), (12, 8, 5), (10, 6, 9), (6, 8, 12)])
    w2, h2 = r.choice([(w1 + 4, h1), (w1, h1 + 2), (w1 * 2, h1 // 2 * 3)])
    d2 = w1 * h1 * d1 / (w2 * h2)
    return {'stem': f'{w1} workers working {h1} hours a day finish a job in {d1} days. How many days will {w2} workers working {h2} hours a day take?', 'answer': f'{num(round(d2, 2))} days',
            'key': f'Worker-hours = {w1} × {h1} × {d1} = {w1 * h1 * d1}; ÷ ({w2} × {h2}) = {num(round(d2, 2))}.'}


def c7s3_case(r):
    n = r.choice([24, 36, 48, 60])
    return {'stem': (f'A class trip needs {n} litres of water shared equally. (i) Copy and complete: 4 bottles → ? litres each, 6 bottles → ?, 8 bottles → ?. '
                     f'(ii) What stays constant? (iii) Sketch how litres per bottle changes as the number of bottles grows.'),
            'answer': f'(i) {num(n / 4)}, {num(n / 6)}, {num(n / 8)} (ii) bottles × litres = {n} (iii) a decreasing curve that never reaches 0',
            'key': 'Inverse proportion table, constant product, hyperbola-like curve.'}


# ---------------- ch08 Fractions in Disguise ----------------
# st1 Equivalent fractions, decimals and conversions

def c8s1_to_dec(r):
    n, d = r.choice([(3, 8), (5, 8), (7, 8), (3, 16), (7, 20), (9, 25), (13, 40), (11, 16), (17, 50), (7, 4)])
    return {'stem': f'Write {n}/{d} as a decimal.', 'answer': num(n / d, 4), 'key': f'{n} ÷ {d} = {num(n / d, 4)} (or make the denominator a power of 10).',
            'distractors': [num(d / n, 3), num(n / d * 10, 4), f'0.{n}{d}']}


def c8s1_to_frac(r):
    dec = r.choice([0.35, 0.125, 0.48, 0.075, 1.25, 2.4, 0.64, 0.875])
    f = Fr(str(dec))
    return {'stem': f'Write {num(dec, 3)} as a fraction in lowest terms.', 'answer': fr(f), 'key': f'{num(dec, 3)} = {int(dec * 1000)}/1000 = {fr(f)}.',
            'distractors': [frac(int(dec * 100), 100) if fr(f) != frac(int(dec * 100), 100) else frac(int(dec * 1000), 1000) + ' (not reduced)', fr(f + Fr(1, 10)), fr(1 / f) if f != 1 else '1/2']}


def c8s1_equiv(r):
    n, d = r.choice([(2, 3), (3, 5), (4, 7), (5, 9)])
    k = r.randint(3, 9)
    return {'stem': f'Find the missing number: {n}/{d} = ?/{d * k}.', 'answer': str(n * k), 'key': f'Denominator × {k}, so numerator × {k}.',
            'distractors': num_distractors(n * k, n + k, n * k + 1, d * k - n)}


def c8s1_percent(r):
    n, d = r.choice([(3, 8), (7, 20), (9, 40), (1, 16), (11, 25)])
    return {'stem': f'Write {n}/{d} as a decimal and as a percentage.', 'answer': f'{num(n / d, 4)}; {num(100 * n / d, 2)}%', 'key': f'{n} ÷ {d} = {num(n / d, 4)}; × 100.'}


def c8s1_explain(r):
    n, d = r.choice([(3, 4), (2, 5), (7, 10)])
    k = r.randint(2, 6)
    return {'stem': f'Explain, using a picture or the idea of sharing, why {n}/{d} and {n * k}/{d * k} are the same amount.',
            'answer': f'Cutting each of the {d} parts into {k} pieces gives {d * k} parts, of which {n * k} are shaded: same amount.', 'key': 'Multiplying numerator and denominator by the same number does not change the value.'}


def c8s1_ar(r):
    return ar('0.4 and 2/5 represent the same number.', '2/5 = 4/10.', 'a', 'Equivalent fraction with denominator 10 gives 0.4.')


def c8s1_money(r):
    who = name(r)
    total = r.choice([800, 1200, 1500, 2000, 2400])
    n, d = r.choice([(3, 8), (2, 5), (5, 12), (3, 10)])
    return {'stem': f'{who} spends {n}/{d} of a pocket-money of {inr(total)} on books and 0.25 of it on a trip. How much is left?',
            'answer': inr(total - total * n / d - total / 4), 'key': f'{n}/{d} × {total} = {num(total * n / d)}; 0.25 × {total} = {total // 4}; left {inr(total - total * n / d - total / 4)}.'}


def c8s1_egypt(r):
    n, d, parts = r.choice([(3, 4, '1/2 + 1/4'), (5, 6, '1/2 + 1/3'), (7, 12, '1/3 + 1/4'), (2, 3, '1/2 + 1/6'), (7, 10, '1/2 + 1/5')])
    return {'stem': f'Ancient Egyptians wrote fractions as sums of different unit fractions. Write {n}/{d} as a sum of two different unit fractions and check.',
            'answer': parts, 'key': f'Check: {parts} = {n}/{d}.'}


# st2 Terminating and recurring decimals

def c8s2_recurring(r):
    n, d = r.choice([(1, 3), (2, 3), (1, 6), (5, 6), (1, 9), (4, 9), (2, 11), (1, 7)])
    s = f'{n / d:.6f}'
    return {'stem': f'Write {n}/{d} as a decimal. Is it terminating or recurring?', 'answer': f'{s}…, recurring', 'key': f'Long division of {n} by {d} repeats.',
            'distractors': [f'{s[:4]}, terminating', f'{num(d / n, 3)}, recurring', f'{s[:5]}, terminating']}


def c8s2_predict(r):
    d = r.choice([8, 12, 15, 16, 20, 24, 25, 30, 40, 45, 48, 50, 60, 64, 75, 80])
    n = r.choice([x for x in range(1, d) if math.gcd(x, d) == 1])
    dd = d
    for p in (2, 5):
        while dd % p == 0:
            dd //= p
    term = dd == 1
    return {'stem': f'Without dividing, decide whether {n}/{d} has a terminating or a recurring decimal. Explain.', 'answer': 'Terminating' if term else 'Recurring',
            'key': f'{d} = {"×".join(str(p) for p in factor_list(d))}; {"only 2s and 5s" if term else "it has a prime factor other than 2 and 5"}.',
            'distractors': ['Recurring' if term else 'Terminating', 'Neither', 'Cannot tell without dividing']}


def factor_list(n):
    out, p = [], 2
    while p * p <= n:
        while n % p == 0:
            out.append(p)
            n //= p
        p += 1
    if n > 1:
        out.append(n)
    return out


def c8s2_to_frac(r):
    case = r.choice(['one', 'two', 'mixed'])
    if case == 'one':
        dgt = r.randint(1, 8)
        return {'stem': f'Write 0.{dgt}{dgt}{dgt}… (0.{dgt} recurring) as a fraction.', 'answer': frac(dgt, 9),
                'key': f'x = 0.{dgt}{dgt}…; 10x − x = {dgt} → x = {dgt}/9' + (f' = {frac(dgt, 9)}' if frac(dgt, 9) != f'{dgt}/9' else '') + '.'}
    if case == 'two':
        ab = r.randint(10, 98)
        return {'stem': f'Write 0.{ab}{ab}{ab}… (digits {ab} recurring) as a fraction in lowest terms.', 'answer': frac(ab, 99),
                'key': f'100x − x = {ab} → x = {ab}/99 = {frac(ab, 99)}.'}
    a, b = r.randint(1, 9), r.randint(1, 9)
    return {'stem': f'Write 0.{a}{b}{b}{b}… (only {b} recurring) as a fraction in lowest terms.', 'answer': frac(9 * a + b, 90),
            'key': f'x = 0.{a}{b}̄; 100x − 10x = {a}{b} − {a} = {10 * a + b - a} → x = {10 * a + b - a}/90 = {frac(9 * a + b, 90)}.'}


def c8s2_explain(r):
    d = r.choice([7, 11, 13])
    return {'stem': f'Explain why, when you divide any whole number by {d}, the decimal must either stop or start repeating within {d - 1} digits.',
            'answer': f'Only {d - 1} non-zero remainders are possible, so a remainder must repeat.', 'key': 'Remainders 1 to d − 1; once one repeats, the digits repeat.'}


def c8s2_ar(r):
    return ar('7/20 is a terminating decimal.', 'The denominator 20 = 2² × 5 has no prime factor other than 2 and 5.', 'a', '7/20 = 0.35.')


def c8s2_period(r):
    d, p = r.choice([(7, 6), (13, 6), (11, 2), (3, 1), (27, 3), (37, 3)])
    return {'stem': f'How many digits repeat in the decimal for 1/{d}? Divide to check.', 'answer': str(p), 'key': f'1/{d} = {1 / d:.8f}…; period {p}.',
            'distractors': num_distractors(p, p + 1, d - 1, p * 2)}


def c8s2_case(r):
    n = r.choice([1, 2, 3, 4, 5, 6])
    digits = f'{n / 7:.12f}'[2:]
    block = digits[:6]
    k = r.randint(13, 40)
    dk = block[(k - 1) % 6]
    return {'stem': (f'A calculator shows {n} ÷ 7 = {n / 7:.10f}. (i) Is this the exact value? (ii) Which block of digits repeats? '
                     f'(iii) Use the pattern to find digit number {k} after the decimal point.'),
            'answer': f'(i) No, it is rounded (ii) {block} (iii) {dk}',
            'key': f'(i) 1/7-type decimals recur, the display is cut off (1 mark). (ii) period 6: {block} (1 mark). (iii) {k} = 6 × {(k - 1) // 6} + {(k - 1) % 6 + 1}, so digit {(k - 1) % 6 + 1} of the block: {dk} (2 marks).'}


# st3 Comparing and ordering fractions/decimals

def c8s3_bigger(r):
    d = r.randint(5, 15)
    a, b = sorted(r.sample(range(1, d), 2))
    return mcq(f'Which is larger: {a}/{d} or {b}/{d}?', f'{b}/{d}', [f'{a}/{d}', 'They are equal', 'Cannot be decided'], 'Same denominator: compare numerators.', r)


def c8s3_order(r):
    vals = sorted(r.sample([0.7, 0.65, 0.703, 0.07, 0.675, 0.6, 0.72, 0.069, 0.709], 4))
    shown = vals[:]
    r.shuffle(shown)
    return {'stem': f'Arrange {", ".join(num(v, 3) for v in shown)} in increasing order.', 'answer': ' < '.join(num(v, 3) for v in vals),
            'key': 'Compare place by place after writing all with the same number of decimal places.'}


def c8s3_compare(r):
    a, b = r.choice([(3, 7), (5, 12), (4, 9), (7, 15), (5, 8)])
    c, d = r.choice([(2, 5), (3, 8), (5, 11), (4, 7)])
    if a * d == c * b:
        c += 1
    big = f'{a}/{b}' if a * d > c * b else f'{c}/{d}'
    return {'stem': f'Which is greater, {a}/{b} or {c}/{d}? Show your method.', 'answer': big, 'key': f'Cross-multiply: {a} × {d} = {a * d}, {c} × {b} = {c * b}.'}


def c8s3_mixed(r):
    items = [('3/5', 0.6), ('0.58', 0.58), ('5/8', 0.625), ('62%', 0.62), ('0.6̄', 2 / 3), ('11/20', 0.55)]
    pick = r.sample(items, 4)
    order = sorted(pick, key=lambda x: x[1])
    return {'stem': f'Arrange in ascending order: {", ".join(p[0] for p in pick)}.', 'answer': ' < '.join(p[0] for p in order),
            'key': 'Convert all to decimals: ' + ', '.join(f'{p[0]} = {p[1]:.3f}' for p in pick) + '.'}


def c8s3_ar(r):
    return ar('0.5 > 0.45', '0.5 has fewer decimal places than 0.45.', 'c', 'A is true (0.50 > 0.45) but R is not a valid reason; R as a general rule is false.')


def c8s3_between(r):
    a = round(r.uniform(0.2, 0.8), 2)
    return {'stem': f'Write a decimal between {num(a, 2)} and {num(a + 0.01, 2)}.', 'answer': num(a + 0.005, 3), 'key': f'e.g. {num(a + 0.005, 3)}; any value strictly between.',
            'distractors': [num(a + 0.02, 2), num(a - 0.005, 3), num(a + 0.1, 2)]}


def c8s3_race(r):
    names = r.sample(['Aarav', 'Diya', 'Kabir', 'Meera', 'Rohan', 'Tara'], 3)
    t = sorted(r.sample([12.5, 12.48, 12.05, 12.405, 12.54, 12.45], 3))
    data = list(zip(names, t))
    r.shuffle(data)
    return {'stem': f'In a 100 m race the times were {", ".join(f"{n} {num(v, 3)} s" for n, v in data)}. Who won and by how much did the winner beat the last runner?',
            'answer': f'{min(data, key=lambda x: x[1])[0]}, by {num(round(t[-1] - t[0], 3), 3)} s', 'key': 'Smallest time wins; difference = largest − smallest.'}


# ---------------- ch09 The Baudhayana-Pythagoras Theorem ----------------

TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (6, 8, 10), (9, 12, 15), (20, 21, 29), (12, 16, 20), (9, 40, 41), (15, 20, 25)]


def c9s1_state(r):
    return mcq('In a right-angled triangle with hypotenuse c and other sides a and b, which statement is the Baudhayana–Pythagoras theorem?', 'a² + b² = c²',
               ['a + b = c', 'a² − b² = c²', 'a² + c² = b²'], 'The square on the hypotenuse equals the sum of the squares on the other two sides.', r)


def c9s1_history(r):
    return mcq(r.choice(['The Baudhayana Shulba Sutra, which states the theorem, is a text about …', 'Baudhayana stated the theorem in the context of …']),
               'constructing fire altars with ropes', ['astronomy and eclipses', 'trade and taxes', 'music and rhythm'],
               'The Shulba Sutras (c. 800 BCE) give rope rules for building altars.', r)


def c9s1_verify(r):
    a, b, c = r.choice(TRIPLES)
    return {'stem': f'Verify the theorem for a right triangle with legs {a} cm and {b} cm and hypotenuse {c} cm.', 'answer': f'{a * a} + {b * b} = {c * c}',
            'key': f'{a}² + {b}² = {a * a + b * b} = {c}².'}


def c9s1_explain(r):
    return {'stem': 'Explain, using four copies of a right triangle arranged inside a big square, why a² + b² = c².',
            'answer': '(a + b)² = 4 × ½ab + c² → a² + 2ab + b² = 2ab + c² → a² + b² = c².', 'key': 'Area of big square counted two ways.'}


def c9s1_which(r):
    a, b, c = r.choice(TRIPLES)
    return {'stem': f'In a right triangle the sides are {a} cm, {b} cm and {c} cm. Which side is the hypotenuse, and where is the right angle?', 'answer': f'{c} cm; opposite the {c} cm side',
            'key': 'The hypotenuse is the longest side and lies opposite the right angle.', 'distractors': [f'{a} cm; opposite the {a} cm side', f'{b} cm; between the other two', f'{c} cm; between {a} cm and {c} cm']}


def c9s1_ar(r):
    return ar('In a right triangle the hypotenuse is the longest side.', 'The hypotenuse is opposite the largest angle, 90°.', 'a', 'The largest side is opposite the largest angle.')


def c9s1_rope(r):
    k = r.choice([1, 2, 3])
    return {'stem': f'A rope with {12 * k} equally spaced knots is pegged into a triangle with sides of {3 * k}, {4 * k} and {5 * k} spaces. Explain why the corner between the {3 * k} and {4 * k} sides is a right angle, as builders in ancient India and Egypt used.',
            'answer': 'Because 3² + 4² = 5², the converse of the theorem makes it a right angle.', 'key': f'({3 * k})² + ({4 * k})² = ({5 * k})².'}


def c9s1_area_squares(r):
    a, b = r.randint(3, 12), r.randint(3, 12)
    return {'stem': f'Squares are drawn on the two shorter sides of a right triangle; their areas are {a * a} cm² and {b * b} cm². What is the area of the square on the hypotenuse?',
            'answer': f'{a * a + b * b} cm²', 'key': 'Area on hypotenuse = sum of the other two areas.',
            'distractors': [f'{(a + b) ** 2} cm²', f'{abs(a * a - b * b)} cm²', f'{a * b} cm²']}


# st2 Finding an unknown side

def c9s2_hyp(r):
    a, b, c = r.choice(TRIPLES)
    return {'stem': f'A right triangle has legs {a} cm and {b} cm. Find the hypotenuse.', 'answer': f'{c} cm', 'key': f'√({a}² + {b}²) = √{a * a + b * b} = {c} cm.',
            'distractors': [f'{a + b} cm', f'{c + 1} cm', f'{num(round(math.sqrt(abs(b * b - a * a)), 2))} cm']}


def c9s2_leg(r):
    a, b, c = r.choice(TRIPLES)
    return {'stem': f'The hypotenuse of a right triangle is {c} cm and one side is {a} cm. Find the third side.', 'answer': f'{b} cm', 'key': f'√({c}² − {a}²) = √{c * c - a * a} = {b} cm.',
            'distractors': [f'{num(round(math.sqrt(c * c + a * a), 2))} cm', f'{c - a} cm', f'{b + 1} cm']}


def c9s2_surd(r):
    a, b = r.randint(2, 9), r.randint(2, 9)
    s = a * a + b * b
    return {'stem': f'A right triangle has legs {a} cm and {b} cm. Find the hypotenuse to one decimal place.', 'answer': f'{math.sqrt(s):.1f} cm',
            'key': f'√{s}; {math.isqrt(s)}² = {math.isqrt(s) ** 2} < {s} < {(math.isqrt(s) + 1) ** 2}; ≈ {math.sqrt(s):.1f} cm.'}


def c9s2_error(r):
    a, b, c = r.choice(TRIPLES)
    return {'stem': f'A student finds the third side of a right triangle with hypotenuse {c} cm and a side {a} cm as √({c}² + {a}²). Explain the mistake and find the correct length.',
            'answer': f'{b} cm', 'key': 'When the hypotenuse is known, subtract: √(c² − a²).', 'gap': 'G2'}


def c9s2_ladder(r):
    a, b, c = r.choice(TRIPLES[:6])
    k = r.choice([1, 0.5])
    who = name(r)
    return {'stem': f'{who} places a {num(c * k)} m ladder against a wall with its foot {num(a * k)} m from the wall. How high up the wall does it reach?',
            'answer': f'{num(b * k)} m', 'key': f'√({num(c * k)}² − {num(a * k)}²) = {num(b * k)} m.'}


def c9s2_diag(r):
    l, w = r.choice([(8, 6), (12, 5), (15, 8), (24, 7), (40, 9), (12, 9)])
    return {'stem': f'Find the length of the diagonal of a rectangular field {l} m by {w} m. How much shorter is walking along the diagonal than along two sides?',
            'answer': f'{num(math.hypot(l, w))} m; {num(l + w - math.hypot(l, w))} m shorter', 'key': f'√({l}² + {w}²) = {num(math.hypot(l, w))}; {l + w} − {num(math.hypot(l, w))}.'}


def c9s2_ar(r):
    a, b, c = r.choice(TRIPLES)
    return ar(f'The third side of a right triangle with hypotenuse {c} cm and one side {a} cm is {b} cm.', f'{c}² − {a}² = {b}².', 'a', 'Rearranged theorem gives the leg.')


def c9s2_two_step(r):
    (a, b, c), (p, q) = r.choice([((5, 12, 13), (9, 15)), ((6, 8, 10), (15, 17)), ((9, 12, 15), (16, 20)), ((5, 12, 13), (35, 37))])
    return {'stem': f'In triangle ABC, AD ⟂ BC with D on BC. AB = {c} cm, BD = {a} cm and DC = {p if (b * b + p * p) == q * q else p} cm. Find AD and AC.',
            'answer': f'AD = {b} cm; AC = {num(round(math.hypot(b, p), 2))} cm',
            'key': f'AD = √({c}² − {a}²) = {b} cm (2 marks); AC = √({b}² + {p}²) = {num(round(math.hypot(b, p), 2))} cm (2 marks).'}


def c9s2_tv(r):
    w, h, d = r.choice([(16, 12, 20), (32, 24, 40), (48, 36, 60), (24, 18, 30)])
    return {'stem': f'A TV screen is described as "{d} inches", which is the length of its diagonal. If its height is {h} inches, find its width.',
            'answer': f'{w} inches', 'key': f'√({d}² − {h}²) = √{d * d - h * h} = {w}.'}


def c9s2_case(r):
    a, b, c = r.choice([(6, 8, 10), (9, 12, 15), (12, 16, 20)])
    return {'stem': (f'A kite string is tied to a peg. The kite is directly above a point {a} m from the peg, at a height of {b} m. '
                     f'(i) Find the length of string. (ii) If the kite rises another {b // 2} m without moving sideways, does the string need to be more than {c + b // 2} m? '
                     f'(iii) Find the new string length to one decimal place.'),
            'answer': f'(i) {c} m (ii) No (iii) {math.hypot(a, b * 1.5):.1f} m', 'key': f'(iii) √({a}² + {num(b * 1.5)}²) = {math.hypot(a, b * 1.5):.1f} m < {c + b // 2} m.'}


# st3 Converse and real-life applications

def c9s3_converse(r):
    return mcq('Which statement is the converse of the Baudhayana–Pythagoras theorem?', 'If a² + b² = c² for the sides of a triangle, the angle opposite c is a right angle',
               ['In a right triangle, a² + b² = c²', 'If a triangle is right-angled, its sides are whole numbers', 'If a² + b² > c², the triangle is right-angled'], 'The converse swaps hypothesis and conclusion.', r)


def c9s3_check(r):
    a, b, c = r.choice(TRIPLES)
    if r.random() < 0.45:
        c += r.choice([1, -1])
    ok = a * a + b * b == c * c
    return {'stem': f'Is a triangle with sides {a} cm, {b} cm and {c} cm right-angled? Justify.', 'answer': 'Yes' if ok else 'No',
            'key': f'{a}² + {b}² = {a * a + b * b}; {c}² = {c * c}.', 'distractors': ['No' if ok else 'Yes', 'Only if it is isosceles', 'Cannot be decided']}


def c9s3_type(r):
    a, b, c = r.choice([(5, 6, 7), (4, 5, 7), (6, 7, 10), (5, 12, 14), (7, 8, 9), (3, 5, 7)])
    t = a * a + b * b - c * c
    kind = 'acute-angled' if t > 0 else ('obtuse-angled' if t < 0 else 'right-angled')
    return {'stem': f'Classify the triangle with sides {a}, {b} and {c} as acute-angled, right-angled or obtuse-angled.', 'answer': kind.capitalize(),
            'key': f'{a}² + {b}² = {a * a + b * b} {">" if t > 0 else "<" if t < 0 else "="} {c}² = {c * c}.',
            'distractors': [k.capitalize() for k in ('acute-angled', 'right-angled', 'obtuse-angled') if k != kind] + ['Equilateral']}


def c9s3_mason(r):
    a, b, c = r.choice([(3, 4, 5), (6, 8, 10), (9, 12, 15)])
    m = r.choice([0.1, 0.2])
    who = name(r)
    return {'stem': f'{who}, a mason, wants to check that a corner of a room is square. She marks {a} ft on one wall and {b} ft on the other and measures the distance between the marks as {num(c + m)} ft. Is the corner square? If not, is it more or less than 90°?',
            'answer': 'No; more than 90°', 'key': f'{a}² + {b}² = {c * c} < {num((c + m) ** 2)} = ({num(c + m)})², so the angle is obtuse.'}


def c9s3_coords(r):
    a, b, c = r.choice(TRIPLES[:5])
    return {'stem': f'Show that the points A(0, 0), B({a}, 0) and C({a}, {b}) form a right triangle and find AC.', 'answer': f'AC = {c}', 'key': f'AB horizontal, BC vertical → right angle at B; AC = √({a}² + {b}²) = {c}.'}


def c9s3_ar(r):
    return ar('A triangle with sides 8, 15 and 17 is right-angled.', 'If the square of the longest side equals the sum of the squares of the other two sides, the triangle is right-angled.', 'a', '64 + 225 = 289 = 17².')


def c9s3_explain(r):
    return {'stem': 'Explain why the converse of the theorem lets a builder make a right angle using only a measuring tape.',
            'answer': 'By marking lengths in a Pythagorean ratio (e.g. 3, 4, 5) the angle is forced to be 90°.', 'key': 'Uses the converse explicitly.'}


def c9s3_case(r):
    a, b, c = r.choice([(6, 8, 10), (5, 12, 13), (9, 12, 15)])
    return {'stem': (f'A school field is a rectangle {b * 10} m long and {a * 10} m wide. Students walk from one corner to the opposite corner along the diagonal instead of the edges. '
                     f'(i) Find the diagonal. (ii) How many metres do they save? (iii) Before marking the field, how can the PE teacher check the corners are right angles with a tape?'),
            'answer': f'(i) {c * 10} m (ii) {(a + b - c) * 10} m (iii) check the diagonals are equal / use a {a}-{b}-{c} triangle',
            'key': f'(i) √({b * 10}² + {a * 10}²) = {c * 10} (2 marks) (ii) {(a + b) * 10} − {c * 10} (1 mark) (iii) converse (1 mark).'}


def c9s3_distance(r):
    e = r.randint(3, 12)
    n = r.choice([4, 5, 9, 16, 8, 12])
    who = name(r)
    d = math.hypot(e, n)
    return {'stem': f'{who} cycles {e} km east and then {n} km north. How far is {who} from the starting point, in a straight line?', 'answer': f'{num(round(d, 2))} km',
            'key': f'√({e}² + {n}²) = √{e * e + n * n} ≈ {num(round(d, 2))} km.'}


FAMILIES = {
    # ch05
    S + '05-st1': [F('C1', 'D2', 'mcq', c5s1_rule), F('C1', 'D1', 'mcq', c5s1_remainder), F('C2', 'D2', 'explain', c5s1_why9), F('C2', 'D3', 'explain', c5s1_claim),
                   F('C2', 'D2', 'mcq', c5s1_ar, kinds=('ar',)), F('C3', 'D2', 'short', c5s1_check), F('C3', 'D3', 'short', c5s1_digit),
                   F('C3', 'D4', 'multi_step', c5s1_lcm_word, gap='G7'), F('C4', 'D4', 'explain', c5s1_three_digit)],
    S + '05-st2': [F('C1', 'D2', 'short', c5s2_magic_sum), F('C1', 'D1', 'mcq', c5s2_ar, kinds=('ar',)), F('C2', 'D2', 'explain', c5s2_calendar), F('C2', 'D3', 'explain', c5s2_centre),
                   F('C3', 'D2', 'short', c5s2_next), F('C3', 'D3', 'short', c5s2_complete), F('C3', 'D4', 'multi_step', c5s2_virahanka),
                   F('C4', 'D3', 'multi_step', c5s2_kaprekar)],
    S + '05-st3': [F('C1', 'D2', 'short', c5s3_rules), F('C1', 'D1', 'short', c5s3_mult), F('C2', 'D2', 'explain', c5s3_11), F('C2', 'D2', 'mcq', c5s3_ar, kinds=('ar',)),
                   F('C2', 'D3', 'short', c5s3_reverse), F('C3', 'D2', 'short', c5s3_simple), F('C3', 'D3', 'multi_step', c5s3_carry), F('C4', 'D4', 'multi_step', c5s3_classic)],
    # ch06
    S + '06-st1': [F('C1', 'D2', 'short', c6s1_expand), F('C1', 'D1', 'mcq', c6s1_ar, kinds=('ar',)), F('C2', 'D2', 'explain', c6s1_area), F('C2', 'D3', 'explain', c6s1_error),
                   F('C3', 'D2', 'numerical', c6s1_mental), F('C3', 'D3', 'numerical', c6s1_common), F('C3', 'D1', 'numerical', c6s1_subtract),
                   F('C4', 'D3', 'multi_step', c6s1_shop, gap='G7')],
    S + '06-st2': [F('C1', 'D2', 'short', c6s2_coeff), F('C1', 'D1', 'mcq', c6s2_like), F('C2', 'D2', 'explain', c6s2_explain), F('C2', 'D3', 'mcq', c6s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'short', c6s2_add), F('C3', 'D3', 'short', c6s2_sub), F('C3', 'D4', 'multi_step', c6s2_perimeter), F('C4', 'D4', 'multi_step', c6s2_age, gap='G7')],
    S + '06-st3': [F('C1', 'D2', 'short', c6s3_mono), F('C1', 'D1', 'short', c6s3_mono_bi), F('C2', 'D2', 'mcq', c6s3_ar, kinds=('ar',)), F('C2', 'D3', 'explain', c6s3_error),
                   F('C3', 'D2', 'numerical', c6s3_bi_bi), F('C3', 'D3', 'multi_step', c6s3_three), F('C3', 'D4', 'multi_step', c6s3_area),
                   F('C4', 'D3', 'numerical', c6s3_number), F('C4', 'D5', 'case', c6s3_case)],
    # ch07
    S + '07-st1': [F('C1', 'D2', 'short', c7s1_simplify), F('C1', 'D1', 'mcq', c7s1_ar, kinds=('ar',)), F('C2', 'D2', 'explain', c7s1_compare), F('C2', 'D3', 'explain', c7s1_scaling),
                   F('C3', 'D2', 'numerical', c7s1_unitary), F('C3', 'D3', 'numerical', c7s1_share), F('C3', 'D1', 'numerical', c7s1_recipe),
                   F('C3', 'D4', 'multi_step', c7s1_map, gap='G7')],
    S + '07-st2': [F('C1', 'D2', 'mcq', c7s2_const), F('C2', 'D2', 'explain', c7s2_explain), F('C2', 'D3', 'explain', c7s2_check), F('C2', 'D2', 'mcq', c7s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c7s2_table), F('C3', 'D3', 'numerical', c7s2_fuel, gap='G7'), F('C3', 'D1', 'numerical', c7s2_shadow),
                   F('C4', 'D4', 'case', c7s2_case)],
    S + '07-st3': [F('C1', 'D2', 'mcq', c7s3_const), F('C1', 'D1', 'short', c7s3_identify), F('C2', 'D2', 'explain', c7s3_explain), F('C2', 'D3', 'mcq', c7s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c7s3_workers), F('C3', 'D3', 'numerical', c7s3_speed), F('C3', 'D4', 'multi_step', c7s3_food, gap='G7'),
                   F('C4', 'D4', 'multi_step', c7s3_mixed), F('C4', 'D3', 'case', c7s3_case)],
    # ch08
    S + '08-st1': [F('C1', 'D2', 'short', c8s1_to_dec), F('C1', 'D1', 'short', c8s1_equiv), F('C2', 'D2', 'explain', c8s1_explain), F('C2', 'D2', 'mcq', c8s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'short', c8s1_to_frac), F('C3', 'D3', 'numerical', c8s1_percent), F('C3', 'D4', 'multi_step', c8s1_money, gap='G7'),
                   F('C4', 'D3', 'explain', c8s1_egypt)],
    S + '08-st2': [F('C1', 'D2', 'short', c8s2_recurring), F('C2', 'D2', 'short', c8s2_predict), F('C2', 'D3', 'explain', c8s2_explain), F('C2', 'D2', 'mcq', c8s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c8s2_to_frac), F('C3', 'D1', 'numerical', c8s2_period), F('C4', 'D4', 'case', c8s2_case)],
    S + '08-st3': [F('C1', 'D2', 'mcq', c8s3_bigger), F('C1', 'D1', 'short', c8s3_between), F('C2', 'D2', 'mcq', c8s3_ar, kinds=('ar',)), F('C3', 'D2', 'short', c8s3_order),
                   F('C3', 'D3', 'short', c8s3_compare), F('C4', 'D3', 'short', c8s3_mixed), F('C3', 'D4', 'multi_step', c8s3_race, gap='G7')],
    # ch09
    S + '09-st1': [F('C1', 'D2', 'mcq', c9s1_state), F('C1', 'D1', 'mcq', c9s1_history), F('C2', 'D2', 'short', c9s1_which), F('C2', 'D3', 'explain', c9s1_explain),
                   F('C2', 'D2', 'mcq', c9s1_ar, kinds=('ar',)), F('C3', 'D2', 'short', c9s1_verify), F('C3', 'D1', 'short', c9s1_area_squares), F('C4', 'D3', 'explain', c9s1_rope)],
    S + '09-st2': [F('C1', 'D2', 'short', c9s2_hyp), F('C1', 'D1', 'mcq', c9s2_ar, kinds=('ar',)), F('C2', 'D2', 'explain', c9s2_error), F('C3', 'D2', 'numerical', c9s2_leg),
                   F('C3', 'D3', 'numerical', c9s2_surd), F('C3', 'D4', 'multi_step', c9s2_ladder, gap='G7'), F('C3', 'D3', 'numerical', c9s2_tv),
                   F('C4', 'D3', 'multi_step', c9s2_diag), F('C4', 'D4', 'multi_step', c9s2_two_step), F('C4', 'D5', 'case', c9s2_case)],
    S + '09-st3': [F('C1', 'D2', 'mcq', c9s3_converse), F('C2', 'D2', 'explain', c9s3_explain), F('C2', 'D3', 'short', c9s3_type), F('C2', 'D2', 'mcq', c9s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'short', c9s3_check), F('C3', 'D1', 'numerical', c9s3_distance), F('C3', 'D3', 'multi_step', c9s3_coords),
                   F('C4', 'D4', 'multi_step', c9s3_mason, gap='G7'), F('C4', 'D3', 'case', c9s3_case)],
}
