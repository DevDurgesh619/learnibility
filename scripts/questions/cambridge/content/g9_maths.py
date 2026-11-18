"""Cambridge IGCSE Mathematics 0580 Extended (2025-27), coursebook chapters 1-12 (grade 9).

Chapter order in the curriculum file (1-12) follows the CUP Core & Extended Coursebook:
number concepts; algebra; lines, angles and shapes; data; fractions, percentages and standard form;
equations, factors and formulae; perimeter, area and volume; probability; sequences, surds and sets;
straight lines and quadratics; Pythagoras and similarity; averages and spread.

Formatting helpers are shared with content/g10_maths.py (imported, not edited).
"""
import math
import re
from fractions import Fraction as Fr
from ._lib import topic, mcq, compose, sf, person, two_people, city, num_mcq, fmt, sup
from .g10_maths import num, n3, nn, expr, lin, quad, bracket, Q, MC, SMC, P, cmp_, ex, sgn, money, MINUS, art

PROFILE = {'mark_scale': {'long': (1.5, 1.5), 'case': (1.25, 1.25)}, 'wordy': False}
CHAPTERS = {}


# ------------------------------------------------------------------ local helpers

def primes_upto(n):
    s = [True] * (n + 1)
    s[0] = s[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            for j in range(i * i, n + 1, i):
                s[j] = False
    return [i for i, v in enumerate(s) if v]


PRIMES = primes_upto(400)


def is_prime(n):
    return n in PRIMES if n <= 400 else all(n % p for p in PRIMES if p * p <= n)


def factorise(n):
    out = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            out[d] = out.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def pf_str(n, index=True):
    f = factorise(n)
    if index:
        return ' × '.join(f'{p}{sup(e) if e > 1 else ""}' for p, e in sorted(f.items()))
    return ' × '.join(str(p) for p, e in sorted(f.items()) for _ in range(e))


def poly_mul(a, b):
    """Coefficient lists, highest power first."""
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def poly_str(c, v='x'):
    n = len(c) - 1
    terms = []
    for i, k in enumerate(c):
        p = n - i
        terms.append((k, '' if p == 0 else (v if p == 1 else v + sup(p))))
    return expr(*terms)


def lb(a, b, v='x'):
    """(ax + b) with brackets."""
    return '(' + lin(a, b, v) + ')'


def sq(n):
    return int(math.isqrt(n)) ** 2 == n


def ordinal(n):
    return f'{n}{"th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")}'


def lst(xs, f=None):
    f = f or num
    return ', '.join(f(x) for x in xs)


def median(xs):
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


def quartiles(xs):
    """Cambridge convention: LQ = median of lower half, UQ = median of upper half (median excluded when n odd)."""
    s = sorted(xs)
    n = len(s)
    lo, hi = s[:n // 2], s[(n + 1) // 2:]
    return median(lo), median(s), median(hi)


def modes(xs):
    c = {}
    for x in xs:
        c[x] = c.get(x, 0) + 1
    m = max(c.values())
    return [k for k, v in c.items() if v == m], m


def ff(x):
    """Fraction to 'a/b' or mixed number 'p q/r' for answers."""
    x = Fr(x)
    if x.denominator == 1:
        return num(int(x))
    if abs(x) > 1:
        w = int(abs(x))
        rem = abs(x) - w
        return (MINUS if x < 0 else '') + f'{w} {rem.numerator}/{rem.denominator}'
    return num(x)


PEOPLE_TEMP = ['Moscow', 'Oslo', 'Ulaanbaatar', 'Reykjavik', 'Helsinki', 'Ottawa', 'Astana', 'Anchorage', 'Harbin', 'Kyiv']


# =========================================================== 1 Reviewing number concepts
t11 = topic('Types of number: natural, integer, prime, square, cube, rational, irrational and reciprocal',
           'types of number: natural, integer, prime, square, cube, rational, irrational and reciprocal', 'types of number', 'rational irrational')
t11.fixed('C1', (1, 2), [
    ('Which of these numbers is irrational?', '√7', '√7 cannot be written as a fraction a/b; √9 = 3, 0.25 = 1/4 and 3/8 are rational.', ['√9', '0.25', '3/8']),
    ('Which of these is the reciprocal of 5?', '1/5', 'The reciprocal of n is 1/n, so 5 × 1/5 = 1.', ['−5', '0.5', '25']),
    ('Which of these numbers is both a square number and a cube number?', '64', '64 = 8² = 4³.', ['16', '27', '100']),
    ('Which of these is not a natural number?', '−3', 'Natural numbers are the counting numbers 1, 2, 3, … (some definitions include 0); −3 is negative.', ['7', '12', '1']),
    ('How many prime numbers are there between 20 and 40?', '4', 'They are 23, 29, 31 and 37.', ['3', '5', '6']),
    ('Which of these is a rational number?', '0.3̇', 'A recurring decimal can be written as a fraction: 0.3̇ = 1/3.', ['π', '√2', '√5']),
    ('What is the only even prime number?', '2', '2 has exactly two factors, 1 and 2; every other even number has 2 as an extra factor.', ['4', '0', '1']),
    ('Which of these numbers is an integer but not a natural number?', '−8', 'Integers include negative whole numbers; natural numbers do not.', ['8', '0.8', '8/3']),
    ('What is the reciprocal of 2/3?', '3/2', 'Invert the fraction: 2/3 × 3/2 = 1.', ['−2/3', '2/3', '6']),
    ('Why is 1 not a prime number?', 'It has only one factor', 'A prime has exactly two distinct factors, 1 and itself; 1 has only one factor.', ['It is odd', 'It is a square number', 'It is a factor of every number']),
])
t11.fixed('C2', (2, 3), [
    ('Explain why √16 is rational but √15 is irrational.', '√16 = 4 = 4/1, which is a fraction of integers; 15 is not a perfect square, so √15 is a non-terminating, non-recurring decimal and cannot be written as a/b.',
     'B1 √16 = 4 = 4/1 rational; B1 15 not a perfect square so √15 cannot be written as a/b [2]'),
    ('Explain why every integer is a rational number.', 'Any integer n can be written as the fraction n/1, which is a ratio of two integers.', 'B1 n = n/1; B1 definition of rational as a/b with integers [2]'),
    ('Explain why 0 has no reciprocal.', 'The reciprocal of n is 1/n, and division by 0 is undefined; no number multiplied by 0 gives 1.', 'B1 1/0 undefined; B1 no number × 0 = 1 [2]'),
    ('Explain why the product of two prime numbers can never be prime.', 'If p and q are prime then pq has factors 1, p, q and pq, so it has more than two factors.', 'B1 lists factors p and q; B1 more than two factors so not prime [2]'),
    ('Ana says that π = 22/7, so π is rational. Explain why she is wrong.', '22/7 is only an approximation of π (22/7 = 3.142857… while π = 3.14159…); π cannot be written exactly as a fraction, so it is irrational.',
     'B1 22/7 is an approximation; B1 π cannot be written exactly as a/b [2]'),
])

NUMTYPES = {
    'prime': lambda n: is_prime(n),
    'square': lambda n: sq(n),
    'cube': lambda n: round(n ** (1 / 3)) ** 3 == n,
    'multiple of 7': lambda n: n % 7 == 0,
    'factor of 72': lambda n: 72 % n == 0,
}


@t11.add('C1', (1, 2, 3))
def n1_which(r, D):
    kind = r.choice(['prime', 'square', 'cube', 'factor of 72'] if D > 1 else ['prime', 'square'])
    f = NUMTYPES[kind]
    hi = 60 if D == 1 else (120 if D == 2 else 220)
    good = [n for n in range(4, hi) if f(n)]
    bad = [n for n in range(9, hi) if not f(n) and (n % 2 == 1 or kind != 'prime')]
    if kind == 'prime':
        bad = [n for n in bad if n % 3 == 0 or n % 7 == 0 or n % 11 == 0]
    if kind == 'square':
        bad = [n for n in bad if any(abs(n - k * k) <= 3 for k in range(3, 16))]
    c = r.choice(good)
    ds = r.sample([b for b in bad if b != c], 3)
    why = {'prime': f'{c} has exactly two factors, 1 and {c}. ' + '; '.join(f'{d} = {pf_str(d, False)}' for d in ds) + '.',
           'square': f'{c} = {math.isqrt(c)}²; the others are not perfect squares.',
           'cube': f'{c} = {round(c ** (1 / 3))}³; the others are not cubes of integers.',
           'factor of 72': f'72 ÷ {c} = {72 // c}; the others do not divide 72 exactly.'}[kind]
    opts, ans = mcq(r, str(c), [str(d) for d in ds])
    return {'stem': f'Which of these numbers is {art(kind) + " number" if kind != "factor of 72" else "a factor of 72"}?', 'options': opts, 'answer': ans, 'key': why}


@t11.add('C1', (2, 3))
def n1_recip(r, D):
    if D == 2:
        a, b = r.choice([(3, 4), (2, 5), (5, 8), (4, 7), (7, 10), (3, 11)])
        x = Fr(a, b)
        c = Fr(b, a)
        return MC(r, f'Write down the reciprocal of {num(x)}.', c, [-x, x, Fr(a * a, b), Fr(b, 1), -c], f'Reciprocal of a/b is b/a: {num(x)} × {num(c)} = 1.', fmtf=num)
    v = r.choice([0.2, 0.25, 0.4, 0.125, 1.25, 2.5, 0.8])
    c = 1 / v
    return MC(r, f'Find the reciprocal of {ex(v)}.', c, [-v, v * 10, 1 - v, c * 10, c / 10], f'{ex(v)} = {num(Fr(v).limit_denominator(100))}, so the reciprocal is 1 ÷ {ex(v)} = {ex(c)}.', fmtf=ex)


@t11.add('C2', (2, 3, 4), 'explain')
def n1_err(r, D):
    nm = person(r)
    case = r.choice(['prime', 'irr', 'odd', 'square'])
    if case == 'prime':
        n = r.choice([51, 57, 87, 91, 111, 119, 133, 141, 161, 187, 203, 221])
        f = factorise(n)
        p = min(f)
        return Q(f'{nm} says that {n} is a prime number because it is odd and does not end in 5. Explain why {nm} is wrong.',
                 f'{n} = {p} × {n // p}, so it has factors other than 1 and {n}; it is not prime.', f'B1 finds a factor, e.g. {n} = {p} × {n // p}; B1 a prime has exactly two factors [2]')
    if case == 'irr':
        k = r.choice([4, 9, 25, 36, 49, 64, 81, 100, 121, 144])
        return Q(f'{nm} says that every square root is an irrational number. Use √{k} to show that {nm} is wrong, and give an example of a square root that is irrational.',
                 f'√{k} = {math.isqrt(k)} = {math.isqrt(k)}/1, which is rational. A square root of a non-square, e.g. √{k + 1}, is irrational.',
                 f'B1 √{k} = {math.isqrt(k)} is rational (counter-example); B1 valid irrational example such as √{k + 1} [2]')
    if case == 'odd':
        return Q(f'{nm} says "all prime numbers are odd and all odd numbers are prime". Give a counter-example to each part of the statement.',
                 f'2 is prime but even; {r.choice([9, 15, 21, 25, 27, 33, 35, 39])} is odd but not prime.', 'B1 2 is an even prime; B1 an odd composite number with its factor [2]')
    a, b = r.sample([12, 18, 20, 27, 32, 45, 50, 75, 98, 8, 3], 2)
    claim = 'is' if not sq(a * b) else 'is not'
    return Q(f'{nm} says that {a} × {b} = {a * b} {claim} a square number. Use prime factors to decide whether {nm} is correct.',
             f'{a * b} = {pf_str(a * b)}; ' + ('every index is even, so it is a square number and ' if sq(a * b) else 'not every index is even, so it is not a square number and ') + f'{nm} is wrong.',
             f'M1 prime factorisation {pf_str(a * b)}; A1 conclusion based on even/odd indices [2]')


@t11.add('C3', (1, 2, 3, 4))
def n1_sort(r, D):
    pool = [r.choice([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]), r.choice([16, 25, 36, 49, 81, 100, 121, 144]), r.choice([8, 27, 125, 216]),
            r.choice([15, 21, 33, 39, 51, 57]), r.choice([-4, -7, -12])]
    if D >= 3:
        pool += [r.choice(['√5', '√12', 'π', '√20']), r.choice(['0.4̇', '3/7', '1.25'])]
    r.shuffle(pool)
    s = ', '.join(x if isinstance(x, str) else num(x) for x in pool)
    ints = [x for x in pool if isinstance(x, int)]
    pr = [x for x in ints if x > 1 and is_prime(x)]
    sqs = [x for x in ints if x > 0 and sq(x)]
    cubes = [x for x in ints if x > 0 and round(x ** (1 / 3)) ** 3 == x]
    asks = [('prime', pr), ('square', sqs), ('cube', cubes)]
    if D >= 3:
        irr = [x for x in pool if x in ('√5', '√12', 'π', '√20')]
        asks.append(('irrational', irr))
        asks.append(('negative integer', [x for x in ints if x < 0]))
    picks = r.sample(asks, min(len(asks), 2 if D <= 2 else 3))
    q = ' '.join(f'({"abc"[i]}) ' + ('any negative integers' if k == 'negative integer' else f'any {k} numbers') for i, (k, _) in enumerate(picks))
    a = ' '.join(f'({"abc"[i]}) ' + (', '.join(x if isinstance(x, str) else num(x) for x in v) or 'none') for i, (k, v) in enumerate(picks))
    key = ' '.join(f'({"abc"[i]}) B1 ' + (', '.join(x if isinstance(x, str) else num(x) for x in v) or 'none') for i, (k, v) in enumerate(picks)) + f' [{len(picks)}]'
    return Q(f'From the list {s}, write down {q}.', a, key)


@t11.add('C3', (2, 3, 4, 5))
def n1_between(r, D):
    lo = r.randint(20, 60) if D <= 3 else r.randint(100, 250)
    hi = lo + r.choice([15, 20, 25]) if D <= 3 else lo + r.choice([30, 40])
    kind = r.choice(['prime', 'square', 'cube']) if D <= 3 else r.choice(['prime', 'square'])
    f = NUMTYPES[kind]
    vals = [n for n in range(lo + 1, hi) if f(n)]
    if not vals:
        return None
    if D >= 4:
        tot = sum(vals)
        return Q(f'Find the sum of all the {kind} numbers greater than {lo} and less than {hi}.', num(tot),
                 f'M1 lists {lst(vals)}; A1 sum = {num(tot)} [2]')
    return Q(f'Write down all the {kind} numbers between {lo} and {hi}.', lst(vals), f'B2 for {lst(vals)} (B1 for one error or omission) [2]')


def n1_c4(r, D):
    a = r.choice([12, 18, 20, 24, 28, 30, 36, 45])
    sqv = r.choice([49, 64, 81, 100, 121, 144, 169])
    cb = r.choice([27, 64, 125, 216, 343])
    pr = r.choice([53, 59, 61, 67, 71, 73, 79, 83])
    irr = r.choice(['√8', '√30', '√50', '∛20'])
    num_list = [a, sqv, cb, pr, f'{irr}']
    r.shuffle(num_list)
    lstr = ', '.join(str(x) for x in num_list)
    fr = Fr(r.choice([2, 3, 4, 5]), r.choice([7, 9, 11]))
    intro = f'Here is a list of numbers: {lstr}.'
    parts = [
        P('From the list, write down the prime number.', str(pr), f'B1 {pr}', 1),
        P('From the list, write down the irrational number.', irr, f'B1 {irr}', 1),
        P(f'From the list, write down a cube number and give its cube root.', f'{cb}; ∛{cb} = {round(cb ** (1 / 3))}', f'B1 {cb}; B1 {round(cb ** (1 / 3))}', 2),
        P(f'Write {a} as a product of its prime factors.', pf_str(a), f'M1 factor tree or repeated division; A1 {pf_str(a)}', 2),
        P(f'Find the reciprocal of {num(fr)} and show that the product of a number and its reciprocal is 1.', f'{num(1 / fr)}; {num(fr)} × {num(1 / fr)} = 1', f'B1 {num(1 / fr)}; B1 shows product = 1', 2),
        P(f'Explain why {sqv} is rational and {irr} is not.', f'{sqv} = {sqv}/1 is a ratio of integers; {irr} is a non-recurring, non-terminating decimal that cannot be written as a/b.',
          'B1 integer as fraction; B1 irrational cannot be a/b', 2),
    ]
    return cmp_(r, intro, parts)


t11.add('C4', (2, 3, 4, 5))(n1_c4)

# ---------------------------------------------------------------- prime factors, HCF, LCM
t12 = topic('Prime factors, HCF and LCM', 'prime factors, hcf and lcm', 'prime factors', 'hcf lcm')
t12.fixed('C1', (1, 2), [
    ('What is the highest common factor of 12 and 18?', '6', 'Factors of 12: 1, 2, 3, 4, 6, 12; factors of 18: 1, 2, 3, 6, 9, 18. Highest common = 6.', ['2', '3', '36']),
    ('What is the lowest common multiple of 4 and 6?', '12', 'Multiples of 4: 4, 8, 12…; multiples of 6: 6, 12… LCM = 12.', ['24', '2', '10']),
    ('Which of these is 60 written as a product of prime factors?', '2² × 3 × 5', '60 = 2 × 2 × 3 × 5.', ['2 × 3 × 10', '4 × 15', '2 × 3² × 5']),
    ('What does HCF stand for?', 'Highest common factor', 'The largest number that divides exactly into each of the numbers.', ['Highest common fraction', 'Half common factor', 'Lowest common multiple']),
    ('Which of these is a common multiple of 6 and 9?', '36', '36 = 6 × 6 = 9 × 4.', ['15', '27', '42']),
    ('The HCF of two different prime numbers is always', '1', 'Each prime has only the factors 1 and itself, so the only common factor is 1.', ['the smaller prime', 'their product', '2']),
])
t12.fixed('C2', (2, 3), [
    ('Explain the difference between the HCF and the LCM of two numbers.', 'The HCF is the largest number that divides into both; the LCM is the smallest number that both divide into.', 'B1 HCF largest common factor; B1 LCM smallest common multiple [2]'),
    ('Explain how prime factorisations of two numbers can be used to find their LCM.', 'Take every prime that appears in either number, each to the highest power that appears, and multiply them.', 'B1 all primes from either; B1 highest power of each [2]'),
    ('Explain why, for any two numbers, HCF × LCM equals the product of the two numbers.', 'Each prime power appears once at its lower index (in the HCF) and once at its higher index (in the LCM), which together give all prime factors of both numbers.',
     'B1 lower powers in HCF, higher in LCM; B1 together give all factors of the product [2]'),
    ('Two lighthouses flash every 8 seconds and every 12 seconds. Explain whether you would use the HCF or the LCM to find when they next flash together.', 'The LCM, because you need the first time that is a multiple of both 8 and 12 (24 seconds).', 'B1 LCM; B1 reason: common multiple of both times (24 s) [2]'),
])


def pair(r, D):
    if D <= 2:
        return r.choice([(12, 18), (16, 24), (20, 30), (15, 25), (18, 27), (14, 21), (24, 36), (28, 42)])
    if D == 3:
        return r.choice([(36, 48), (60, 84), (45, 75), (72, 90), (56, 98), (66, 110), (84, 126), (90, 150)])
    return r.choice([(120, 252), (168, 180), (140, 196), (126, 240), (210, 330), (144, 264), (180, 378), (175, 245)])


@t12.add('C1', (1, 2, 3))
def n2_pf(r, D):
    n = r.choice([24, 36, 40, 48, 54, 56, 72, 84, 90, 96] if D <= 2 else [120, 126, 150, 168, 180, 196, 240, 252, 300, 360])
    f = factorise(n)
    c = pf_str(n)
    wrong = []
    ps = sorted(f)
    # change an index
    for p in ps:
        g = dict(f)
        g[p] = g[p] + 1
        wrong.append(' × '.join(f'{q}{sup(e) if e > 1 else ""}' for q, e in sorted(g.items())))
        if g[p] > 2:
            g[p] -= 2
            wrong.append(' × '.join(f'{q}{sup(e) if e > 1 else ""}' for q, e in sorted(g.items())))
    wrong.append(f'{ps[0]} × {n // ps[0]}')
    return SMC(r, f'Which of these shows {n} written as a product of its prime factors?', c, wrong, f'{n} = {pf_str(n, False)} = {c}.')


@t12.add('C2', (2, 3, 4), 'explain')
def n2_err(r, D):
    a, b = pair(r, D)
    h, l = math.gcd(a, b), a * b // math.gcd(a, b)
    nm = person(r)
    case = r.choice(['swap', 'product', 'pf'])
    if case == 'swap':
        return Q(f'{nm} is asked for the HCF of {a} and {b} and writes {l}. Explain the mistake and find the HCF.',
                 f'{l} is the LCM (the smallest common multiple), not the HCF. HCF = {h}.', f'B1 identifies {l} as the LCM / too large to be a factor of {a}; B1 HCF = {h} [2]')
    if case == 'product':
        return Q(f'{nm} says that the LCM of {a} and {b} is {a} × {b} = {a * b}. Explain why this is not correct and find the LCM.',
                 f'{a * b} is a common multiple but not the lowest because {a} and {b} share the factor {h}. LCM = {a * b} ÷ {h} = {l}.',
                 f'B1 common factor {h} means a smaller common multiple exists; B1 LCM = {l} [2]')
    n = r.choice([84, 90, 120, 126, 150, 180, 196])
    m = r.choice(list(factorise(n)))
    wrong = f'{m} × {n // m}'
    return Q(f'{nm} writes {n} as a product of prime factors as {wrong}. Explain why this is not fully correct and write the correct prime factorisation.',
             f'{n // m} is not prime, so the factorisation is incomplete. {n} = {pf_str(n)}.', f'B1 {n // m} is not prime; B1 {pf_str(n)} [2]')


@t12.add('C3', (1, 2, 3, 4, 5))
def n2_hcf(r, D):
    a, b = pair(r, D)
    h, l = math.gcd(a, b), a * b // math.gcd(a, b)
    if D == 1:
        which = r.choice(['HCF', 'LCM'])
        c = h if which == 'HCF' else l
        return MC(r, f'Find the {which} of {a} and {b}.', c, [h, l, a * b, h * 2, l // 2, a + b], f'{a} = {pf_str(a)}, {b} = {pf_str(b)}; {which} = {c}.')
    if D <= 3:
        return Q(f'Write {a} and {b} as products of prime factors. Hence find (a) the HCF and (b) the LCM of {a} and {b}.',
                 f'{a} = {pf_str(a)}, {b} = {pf_str(b)}; (a) HCF = {h} (b) LCM = {l}',
                 f'B1 {pf_str(a)}; B1 {pf_str(b)}; (a) B1 {h} (lowest powers of common primes) (b) B1 {l} (highest powers of all primes) [4]', type='multi_step')
    c = r.choice([k for k in (6, 10, 14, 15, 21, 35) if math.gcd(k, a) > 1])
    h3, l3 = math.gcd(math.gcd(a, b), c), l * c // math.gcd(l, c)
    return Q(f'Find (a) the HCF and (b) the LCM of {a}, {b} and {c}. Show your prime factorisations.',
             f'(a) {h3} (b) {l3}', f'M1 {pf_str(a)}, {pf_str(b)}, {pf_str(c)}; (a) A1 {h3} (b) M1 highest powers; A1 {l3} [4]', type='multi_step')


@t12.add('C3', (2, 3, 4, 5))
def n2_ctx(r, D):
    nm = person(r)
    case = r.choice(['bus', 'tiles', 'packs', 'ribbon'])
    a, b = pair(r, min(D, 3))
    h, l = math.gcd(a, b), a * b // math.gcd(a, b)
    if case == 'bus':
        a, b = r.choice([(12, 18), (15, 20), (8, 14), (10, 25), (16, 24), (9, 12), (18, 30)])
        l = a * b // math.gcd(a, b)
        st = r.randint(6, 8) * 60 + r.choice([0, 15, 30])
        t = st + l
        return Q(f'At a bus station in {city(r)}, buses to the airport leave every {a} minutes and buses to the harbour leave every {b} minutes. Both leave together at {st // 60:02d}:{st % 60:02d}. Find the next time they leave together.',
                 f'{t // 60:02d}:{t % 60:02d}', f'M1 LCM of {a} and {b}; A1 {l} minutes; A1 {t // 60:02d}:{t % 60:02d} [3]')
    if case == 'tiles':
        return Q(f'{nm} wants to cover a rectangular floor {a} cm by {b} cm with identical square tiles, with no cutting. Find the largest possible side length of the tiles and the number of tiles needed.',
                 f'{h} cm; {(a // h) * (b // h)} tiles', f'M1 HCF of {a} and {b}; A1 {h} cm; M1 ({a} ÷ {h}) × ({b} ÷ {h}); A1 {(a // h) * (b // h)} [4]')
    if case == 'packs':
        a, b = r.choice([(6, 8), (8, 12), (10, 15), (12, 20), (9, 15), (14, 21), (16, 20)])
        l = a * b // math.gcd(a, b)
        it1, it2 = r.choice([('pencils', 'erasers'), ('cups', 'plates'), ('bread rolls', 'sausages'), ('stickers', 'cards')])
        return Q(f'{it1.capitalize()} are sold in packs of {a} and {it2} in packs of {b}. {nm} wants to buy exactly the same number of {it1} and {it2}. Find the least number of packs of each that {nm} must buy.',
                 f'{l // a} packs of {it1} and {l // b} packs of {it2}', f'M1 LCM of {a} and {b} = {l}; A1 {l // a} packs; A1 {l // b} packs [3]')
    return Q(f'Two pieces of ribbon of lengths {a} cm and {b} cm are cut into pieces that are all the same length, with nothing left over. Find the greatest possible length of each piece and the total number of pieces.',
             f'{h} cm; {a // h + b // h} pieces', f'M1 HCF; A1 {h} cm; A1 {a // h} + {b // h} = {a // h + b // h} [3]')


def n2_c4(r, D):
    p = r.choice([2, 3])
    q = r.choice([5, 7])
    A = p ** r.randint(2, 3) * q * r.choice([3, 1]) if p == 2 else p ** 2 * q * 2
    B = p * q ** 2 * r.choice([2, 4]) if p == 3 else p ** 2 * q ** 2
    if A == B:
        return None
    h, l = math.gcd(A, B), A * B // math.gcd(A, B)
    k = r.choice([4, 6, 8, 9, 10])
    intro = f'A = {pf_str(A)} and B = {pf_str(B)}.'
    parts = [
        P('Find the value of A.', num(A), f'B1 {A}', 1),
        P('Find the highest common factor of A and B, giving your answer as a product of prime factors.', pf_str(h), f'M1 lowest power of each common prime; A1 {pf_str(h)}', 2),
        P('Find the lowest common multiple of A and B, giving your answer as a product of prime factors.', pf_str(l), f'M1 highest power of every prime; A1 {pf_str(l)}', 2),
        P('Show that HCF × LCM = A × B.', f'{h} × {l} = {h * l} and {A} × {B} = {A * B}', f'M1 both products; A1 equal ({A * B})', 2),
        P(f'Find the smallest whole number n such that A × n is a square number.', str(next(n for n in range(1, 400) if sq(A * n))), f'M1 identifies odd indices in {pf_str(A)}; A1 {next(n for n in range(1, 400) if sq(A * n))}', 2),
        P(f'Explain why {l} is a multiple of both A and B.', f'{l} ÷ {A} = {l // A} and {l} ÷ {B} = {l // B}, both whole numbers.', 'B1 both divisions exact', 1),
    ]
    return cmp_(r, intro, parts)


t12.add('C4', (2, 3, 4, 5))(n2_c4)


def n2_c4b(r, D):
    a, b, c = r.choice([(6, 8, 10), (4, 6, 9), (8, 12, 15), (10, 12, 18), (9, 12, 20), (6, 10, 15)])
    l = a * b // math.gcd(a, b)
    l3 = l * c // math.gcd(l, c)
    st = r.choice([6, 7, 8]) * 60
    t = st + l3
    nm = person(r)
    intro = f'At a festival in {city(r)}, three sets of fireworks are launched from {st // 60:02d}:00. Set P is launched every {a} minutes, set Q every {b} minutes and set R every {c} minutes. All three are launched together at {st // 60:02d}:00.'
    parts = [
        P('Find when sets P and Q are next launched together.', f'after {l} minutes', f'M1 LCM of {a} and {b}; A1 {l} min', 2),
        P('Find the next time that all three sets are launched together.', f'{t // 60:02d}:{t % 60:02d}', f'M1 LCM of {a}, {b}, {c} = {l3}; A1 {t // 60:02d}:{t % 60:02d}', 2),
        P(f'{nm} says all three are launched together every {a * b * c} minutes. Explain whether {nm} is correct.', f'No: {a * b * c} is a common multiple, but the lowest is {l3} minutes, so they coincide every {l3} minutes.', f'B1 not the lowest; B1 {l3}', 2),
        P(f'Find how many times set R is launched after {st // 60:02d}:00 up to and including the next time all three are launched together.', str(l3 // c), f'B1 {l3} ÷ {c} = {l3 // c}', 1),
    ]
    return cmp_(r, intro, parts)


t12.add('C4', (3, 4, 5))(n2_c4b)

# ---------------------------------------------------------------- powers, roots, order of operations
t13 = topic('Powers, roots and the order of operations including calculator use', 'powers, roots and the order of operations including calculator use', 'order of operations', 'powers roots')
t13.fixed('C1', (1, 2), [
    ('What is the value of 2⁵?', '32', '2 × 2 × 2 × 2 × 2 = 32.', ['10', '25', '64']),
    ('What is the value of ∛125?', '5', '5 × 5 × 5 = 125.', ['25', '41.7', '15']),
    ('Work out 3 + 4 × 2.', '11', 'Multiplication before addition: 4 × 2 = 8, then 3 + 8 = 11.', ['14', '10', '24']),
    ('What is the value of 10⁰?', '1', 'Any non-zero number to the power 0 is 1.', ['0', '10', '100']),
    ('Work out (−3)².', '9', '(−3) × (−3) = 9.', ['−9', '−6', '6']),
    ('Which operation is carried out first in 20 − 12 ÷ 4 + 1?', 'Division', 'BIDMAS/BODMAS: division and multiplication before addition and subtraction.', ['Subtraction', 'Addition', 'It does not matter']),
    ('What is the value of √(9 + 16)?', '5', 'The root sign acts as a bracket: √25 = 5.', ['7', '25', '12.5']),
])
t13.fixed('C2', (2, 3), [
    ('Explain why −3² and (−3)² give different answers.', 'In −3² only 3 is squared, giving −9; in (−3)² the whole negative number is squared, giving 9.', 'B1 −3² = −9 with reason; B1 (−3)² = 9 [2]'),
    ('Explain why a calculator needs brackets to work out (12 + 8) ÷ 5 correctly.', 'Without brackets the calculator divides first (12 + 8 ÷ 5 = 13.6); brackets force the addition first, giving 20 ÷ 5 = 4.', 'B1 division before addition otherwise; B1 correct values 13.6 vs 4 [2]'),
    ('Explain why √(a + b) is not usually equal to √a + √b, using a = 9 and b = 16.', '√(9 + 16) = √25 = 5 but √9 + √16 = 3 + 4 = 7, so they are not equal.', 'B1 5; B1 7 and conclusion [2]'),
    ('Explain why the square root of a positive number has two values but its cube root has only one real value.', 'Both n × n and (−n) × (−n) give n², so there are two square roots; (−n)³ is negative, so only one real number cubes to a given positive number.',
     'B1 positive and negative squares equal; B1 negative cube is negative [2]'),
])


@t13.add('C1', (1, 2, 3))
def n3_eval(r, D):
    case = r.choice(['pow', 'root', 'bid'])
    if case == 'pow':
        b, e = r.choice([(2, 6), (3, 4), (4, 3), (5, 3), (2, 7), (6, 2), (10, 4), (3, 5)] if D > 1 else [(2, 3), (3, 3), (4, 2), (5, 2), (2, 4)])
        c = b ** e
        return MC(r, f'Work out the value of {b}{sup(e)}.', c, [b * e, b ** (e - 1), b ** (e + 1), e ** b, c + b], f'{b}{sup(e)} = ' + ' × '.join([str(b)] * e) + f' = {c}.')
    if case == 'root':
        k = r.choice([2, 3])
        v = r.randint(3, 12) if k == 2 else r.randint(2, 7)
        n = v ** k
        sym = '√' if k == 2 else '∛'
        return MC(r, f'Work out {sym}{n}.', v, [n / k, v + 1, v * k, v - 1, n / 10], f'{v}{sup(k)} = {n}, so {sym}{n} = {v}.')
    a, b, c = r.randint(2, 9), r.randint(2, 9), r.randint(2, 9)
    d = r.randint(1, 9)
    if D == 1:
        st = f'{a} + {b} × {c}'
        v = a + b * c
        ds = [(a + b) * c, a * b + c, a + b + c]
        k = f'Multiply first: {b} × {c} = {b * c}; then {a} + {b * c} = {v}.'
    else:
        st = f'{a * c} ÷ {c} + {b}² − {d}'
        v = a + b * b - d
        ds = [a * c / (c + b * b - d) if c + b * b - d else 1, a + 2 * b - d, (a * c / c + b) ** 2 - d, a + b * b + d]
        k = f'Indices first: {b}² = {b * b}; division: {a * c} ÷ {c} = {a}; then {a} + {b * b} − {d} = {v}.'
    return MC(r, f'Work out {st}.', v, ds, k, fmtf=lambda x: ex(round(x, 2)))


@t13.add('C2', (2, 3, 4), 'explain')
def n3_err(r, D):
    nm = person(r)
    a, b, c = r.randint(10, 30), r.randint(2, 6), r.randint(2, 5)
    case = r.choice(['left', 'sq', 'calc'])
    if case == 'left':
        v = a - b * c
        w = (a - b) * c
        return Q(f'{nm} works out {a} − {b} × {c} and gets {w}. Explain the mistake and give the correct answer.',
                 f'{nm} subtracted first. Multiplication must be done before subtraction: {b} × {c} = {b * c}, so {a} − {b * c} = {num(v)}.', f'B1 multiplication before subtraction; B1 {num(v)} [2]')
    if case == 'sq':
        return Q(f'{nm} says that −{b}² + {c * 5} = {b * b + c * 5}. Explain the mistake and find the correct value.',
                 f'Only {b} is squared, so −{b}² = −{b * b}; −{b * b} + {c * 5} = {num(c * 5 - b * b)}.', f'B1 −{b}² = −{b * b}; B1 {num(c * 5 - b * b)} [2]')
    x, y, z = r.choice([12.6, 18.4, 25.2, 9.8]), r.choice([3.4, 4.7, 6.1, 2.9]), r.choice([1.6, 2.5, 3.2, 4.4])
    right = (x + y) / z
    wrong = x + y / z
    return Q(f'{nm} uses a calculator to work out (({ex(x)} + {ex(y)}) ÷ {ex(z)}) by typing {ex(x)} + {ex(y)} ÷ {ex(z)} = and gets {n3(wrong)}. Explain the error and give the correct answer to 3 significant figures.',
             f'Without brackets the calculator divides {ex(y)} by {ex(z)} first. Correct: {ex(x + y)} ÷ {ex(z)} = {n3(right)}.', f'B1 needs brackets round the numerator; B1 {n3(right)} [2]')


@t13.add('C3', (1, 2, 3, 4, 5))
def n3_calc(r, D):
    if D <= 2:
        a, b, c = r.randint(2, 8), r.randint(2, 6), r.randint(3, 9)
        v = (a + b) ** 2 - c * b
        return Q(f'Work out ({a} + {b})² − {c} × {b}. Show your working.', num(v), f'M1 ({a + b})² = {(a + b) ** 2} and {c} × {b} = {c * b}; A1 {num(v)} [2]')
    if D == 3:
        a, b, c = r.choice([4.8, 6.25, 7.3, 12.9]), r.choice([2.6, 3.15, 1.85]), r.choice([1.4, 2.2, 0.75])
        v = math.sqrt(a ** 2 + b) / c
        return Q(f'Use your calculator to work out √({ex(a)}² + {ex(b)}) ÷ {ex(c)}. Write down all the figures on your calculator display, then give your answer correct to 3 significant figures.',
                 f'{v:.6f}… = {n3(v)}', f'B1 {v:.6f}… (at least 5 figures); B1 {n3(v)} [2]')
    a, b, c, d = r.choice([3.2, 5.6, 8.1]), r.choice([1.7, 2.4, 0.95]), r.choice([12.5, 18.2, 9.4]), r.choice([2, 3])
    v = (a ** d - b) / (math.sqrt(c) + b)
    return Q(f'Calculate ({ex(a)}{sup(d)} − {ex(b)}) ÷ (√{ex(c)} + {ex(b)}), giving your answer correct to 4 significant figures.', sf(v, 4),
             f'M1 numerator {ex(round(a ** d - b, 4))}; M1 denominator {sf(math.sqrt(c) + b, 5)}; A1 {sf(v, 4)} [3]')


@t13.add('C3', (2, 3, 4))
def n3_brackets(r, D):
    # insert brackets to make a statement true
    for _ in range(30):
        a, b, c, d = r.randint(2, 9), r.randint(2, 9), r.randint(2, 9), r.randint(1, 6)
        opts = {f'({a} + {b}) × {c} − {d}': (a + b) * c - d, f'{a} + {b} × ({c} − {d})': a + b * (c - d), f'({a} + {b} × {c}) − {d}': a + b * c - d}
        target_expr, target = r.choice([(k, v) for k, v in opts.items() if '(' in k[:1] or ' × (' in k][:2])
        plain = f'{a} + {b} × {c} − {d}'
        if target != a + b * c - d:
            break
    else:
        return None
    return Q(f'Insert one pair of brackets to make this statement true: {plain} = {num(target)}.', target_expr + f' = {num(target)}',
             f'B1 correct bracket position: {target_expr}; B1 checks value {num(target)} [2]')


def n3_c4(r, D):
    side = r.choice([3.6, 4.5, 5.2, 6.8, 7.4])
    vol = side ** 3
    area = r.choice([200, 250, 320, 450, 600])
    intro = f'A company in {city(r)} makes cube-shaped storage boxes.'
    s2 = math.sqrt(area)
    k = r.choice([2, 3, 4])
    parts = [
        P(f'A box has edge {ex(side)} cm. Calculate its volume.', f'{ex(round(vol, 3))} cm³', f'M1 {ex(side)}³; A1 {ex(round(vol, 3))}', 2),
        P(f'Another box has a volume of {k ** 3 * 125} cm³. Find the length of its edge without using a calculator.', f'{k * 5} cm', f'M1 ∛{k ** 3 * 125} = ∛{k ** 3} × ∛125; A1 {k * 5} cm', 2),
        P(f'The top face of a third box has an area of {area} cm². Find the edge length, correct to 3 significant figures.', f'{n3(s2)} cm', f'M1 √{area}; A1 {n3(s2)}', 2),
        P(f'Calculate the total surface area of the box in part (a), giving your answer correct to 3 significant figures.', f'{n3(6 * side ** 2)} cm²', f'M1 6 × {ex(side)}²; A1 {n3(6 * side ** 2)}', 2),
        P(f'Evaluate ({ex(side)}³ + {area}) ÷ √{area}, giving your answer to 3 significant figures.', n3((vol + area) / s2), f'M1 correct order with brackets; A1 {n3((vol + area) / s2)}', 2),
    ]
    return cmp_(r, intro, parts)


t13.add('C4', (2, 3, 4, 5))(n3_c4)

# ---------------------------------------------------------------- directed numbers
t14 = topic('Directed numbers in context', 'directed numbers in context', 'directed numbers', 'negative numbers')
t14.fixed('C1', (1, 2), [
    ('The temperature is −4 °C and rises by 9 °C. What is the new temperature?', '5 °C', '−4 + 9 = 5.', ['−13 °C', '13 °C', '−5 °C']),
    ('Work out −6 − (−10).', '4', 'Subtracting a negative is adding: −6 + 10 = 4.', ['−16', '16', '−4']),
    ('Work out −7 × −3.', '21', 'Negative × negative = positive.', ['−21', '−10', '10']),
    ('Work out −24 ÷ 6.', '−4', 'Negative ÷ positive = negative.', ['4', '−18', '−30']),
    ('Which of these temperatures is the lowest?', '−12 °C', 'On a number line −12 is furthest to the left.', ['−8 °C', '−3 °C', '0 °C']),
    ('A diver is 15 m below sea level and swims up 6 m. What is the new position?', '−9 m', '−15 + 6 = −9.', ['−21 m', '9 m', '−6 m']),
])
t14.fixed('C2', (2, 3), [
    ('Explain why subtracting a negative number gives the same result as adding the positive number.', 'Subtracting −n removes a debt of n (or moves the opposite way on the number line), so the value increases by n.', 'B1 opposite direction / removing negative; B1 example e.g. 3 − (−2) = 5 [2]'),
    ('Explain why the product of two negative numbers is positive, using the pattern −3 × 2 = −6, −3 × 1 = −3, −3 × 0 = 0.', 'Each step the answer increases by 3, so −3 × −1 = 3 and −3 × −2 = 6: the products become positive.', 'B1 pattern increases by 3; B1 continues to positive values [2]'),
    ('Explain why a temperature change from −5 °C to 3 °C is a rise of 8 °C and not 2 °C.', 'From −5 to 0 is 5 degrees and from 0 to 3 is 3 more, so the change is 3 − (−5) = 8.', 'B1 counts across zero; B1 3 − (−5) = 8 [2]'),
])


@t14.add('C1', (1, 2, 3))
def n4_ops(r, D):
    a, b = -r.randint(2, 15), r.randint(2, 12) * r.choice([1, -1])
    op = r.choice(['+', '−', '×', '÷'] if D > 1 else ['+', '−'])
    if op == '÷':
        a = a * abs(b) if abs(a) < 30 else a
        v = Fr(a, b)
        if v.denominator != 1:
            return None
        v = int(v)
        ds = [-v, a * b, a - b]
    elif op == '×':
        v = a * b
        ds = [-v, a + b, a - b]
    elif op == '+':
        v = a + b
        ds = [a - b, -(a + b), -a + b]
    else:
        v = a - b
        ds = [a + b, -(a - b), b - a + 1]
    bs = f'({num(b)})' if b < 0 else num(b)
    return MC(r, f'Work out {num(a)} {op} {bs}.', v, ds, f'{num(a)} {op} {bs} = {num(v)}' + (' (same signs give a positive, different signs a negative).' if op in '×÷' else '.'))


TEMPS = ['Moscow', 'Oslo', 'Ulaanbaatar', 'Reykjavik', 'Helsinki', 'Ottawa', 'Astana', 'Harbin', 'Kyiv', 'Toronto']


@t14.add('C2', (2, 3, 4), 'explain')
def n4_err(r, D):
    nm = person(r)
    lo, hi = -r.randint(3, 18), r.randint(2, 14)
    c = r.choice(TEMPS)
    case = r.choice(['diff', 'sub', 'mul'])
    if case == 'diff':
        return Q(f'At midnight in {c} the temperature was {num(lo)} °C. At noon it was {hi} °C. {nm} says the temperature rose by {num(hi + lo)} °C. Explain the mistake and find the correct rise.',
                 f'{nm} added {hi} and {num(lo)}. The rise is {hi} − ({num(lo)}) = {hi - lo} °C.', f'B1 must subtract the lower from the higher; B1 {hi - lo} °C [2]')
    if case == 'sub':
        return Q(f'{nm} writes {num(lo)} − ({num(-hi)}) = {num(lo - hi)}. Explain the error and give the correct answer.',
                 f'Subtracting a negative is adding: {num(lo)} + {hi} = {num(lo + hi)}.', f'B1 − (−{hi}) = + {hi}; B1 {num(lo + hi)} [2]')
    return Q(f'{nm} says that ({num(lo)})³ is positive because "a negative times a negative is positive". Explain why {nm} is wrong.',
             f'({num(lo)})³ = ({num(lo)}) × ({num(lo)}) × ({num(lo)}); the first two give {lo * lo}, then × ({num(lo)}) gives {num(lo ** 3)}, which is negative.',
             f'B1 three negative factors; B1 result {num(lo ** 3)} negative [2]')


@t14.add('C3', (1, 2, 3, 4, 5))
def n4_ctx(r, D):
    nm = person(r)
    case = r.choice(['bank', 'temp', 'lift', 'sea'])
    if case == 'bank':
        bal = r.randint(40, 300)
        w = bal + r.randint(20, 200)
        dep = r.randint(30, 150)
        cur = '$'
        v = bal - w + dep
        if D <= 2:
            return Q(f'{nm} has {cur}{bal} in a bank account and withdraws {cur}{w}. Find the new balance.', f'{MINUS}{cur}{w - bal}', f'M1 {bal} − {w}; A1 −{cur}{w - bal} [2]')
        fee = r.choice([5, 10, 15, 20])
        v -= fee
        return Q(f'{nm} has {cur}{bal} in a bank account. {nm} withdraws {cur}{w}, is charged an overdraft fee of {cur}{fee}, and then deposits {cur}{dep}. Find the final balance.',
                 (MINUS if v < 0 else '') + f'{cur}{abs(v)}', f'M1 {bal} − {w} − {fee}; M1 + {dep}; A1 {num(v)} [3]')
    if case == 'temp':
        c = r.choice(TEMPS)
        ts = [r.randint(-15, 8) for _ in range(5 if D <= 3 else 7)]
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][:len(ts)]
        tbl = ', '.join(f'{d} {num(t)} °C' for d, t in zip(days, ts))
        rng = max(ts) - min(ts)
        if D <= 3:
            return Q(f'The minimum temperatures in {c} one week were: {tbl}. Find the difference between the highest and lowest of these temperatures.', f'{rng} °C', f'M1 {max(ts)} − ({num(min(ts))}); A1 {rng} °C [2]')
        mean = Fr(sum(ts), len(ts))
        return Q(f'The minimum temperatures in {c} one week were: {tbl}. Calculate (a) the range and (b) the mean temperature, correct to 1 decimal place.',
                 f'(a) {rng} °C (b) {num(round(float(mean), 1))} °C', f'(a) B1 {rng} (b) M1 sum = {num(sum(ts))}; M1 ÷ {len(ts)}; A1 {num(round(float(mean), 1))} [4]', type='multi_step')
    if case == 'lift':
        st = r.randint(-3, 2)
        moves = [r.choice([1, -1]) * r.randint(2, 9) for _ in range(2 if D <= 2 else 4)]
        pos = st
        for m in moves:
            pos += m
        desc = ', then '.join(f'{"up" if m > 0 else "down"} {abs(m)} floors' for m in moves)
        return Q(f'A lift in a hotel in {city(r)} starts at floor {num(st)} (floor 0 is ground level and basement floors are negative). It goes {desc}. Which floor does it finish on?',
                 f'Floor {num(pos)}', f'M1 {num(st)} ' + ' '.join(f'{"+" if m > 0 else MINUS} {abs(m)}' for m in moves) + f'; A1 {num(pos)} [2]')
    h = r.randint(150, 900)
    dpt = -r.randint(20, 120)
    return Q(f'A bird is flying {h} m above sea level directly above a submarine at {num(dpt)} m. Find the vertical distance between them{" and the new distance if the submarine rises " + str(-dpt // 2) + " m" if D >= 3 else ""}.',
             f'{h - dpt} m' + (f'; {h - dpt + dpt // 2} m' if D >= 3 else ''), f'M1 {h} − ({num(dpt)}); A1 {h - dpt} m' + (f'; B1 {h - dpt + dpt // 2} m [3]' if D >= 3 else ' [2]'))


def n4_c4(r, D):
    c = r.choice(TEMPS)
    ts = [r.randint(-18, -2), r.randint(-10, 3), r.randint(-6, 8), r.randint(-14, 0)]
    times = ['03:00', '09:00', '15:00', '21:00']
    tbl = ', '.join(f'{t} {num(v)} °C' for t, v in zip(times, ts))
    drop = r.randint(4, 11)
    mean = Fr(sum(ts), 4)
    intro = f'The temperatures recorded at a weather station in {c} on one day were {tbl}.'
    parts = [
        P('Find the rise in temperature between 03:00 and 15:00.', f'{ts[2] - ts[0]} °C', f'M1 {num(ts[2])} − ({num(ts[0])}); A1 {ts[2] - ts[0]}', 2),
        P(f'By 23:00 the temperature had fallen {drop} °C below the 21:00 reading. Find the temperature at 23:00.', f'{num(ts[3] - drop)} °C', f'B1 {num(ts[3])} − {drop} = {num(ts[3] - drop)}', 1),
        P('Calculate the mean of the four recorded temperatures.', f'{ex(float(mean))} °C', f'M1 sum {num(sum(ts))}; A1 ÷ 4 = {ex(float(mean))}', 2),
        P('Find the range of the four recorded temperatures.', f'{max(ts) - min(ts)} °C', f'B1 {max(ts)} − ({num(min(ts))}) = {max(ts) - min(ts)}', 1),
        P(f'The temperature at the station on the next day was 2 times as far below zero as the lowest reading here. Find this temperature.', f'{num(2 * min(ts))} °C', f'B1 2 × ({num(min(ts))}) = {num(2 * min(ts))}', 1),
    ]
    return cmp_(r, intro, parts)


t14.add('C4', (2, 3, 4, 5))(n4_c4)
CHAPTERS[1] = [t11, t12, t13, t14]


# =========================================================== 2 Making sense of algebra
def mono(c, vs):
    """c and dict var->power -> '12x²y'."""
    body = ''.join(v + (sup(p) if p > 1 else '') for v, p in sorted(vs.items()) if p)
    if not body:
        return num(c)
    if c == 1:
        return body
    if c == -1:
        return MINUS + body
    return num(c) + body


t21 = topic('Using letters to represent unknowns and simplifying expressions', 'using letters to represent unknowns and simplifying expressions', 'simplifying expressions', 'like terms')
t21.fixed('C1', (1, 2), [
    ('Simplify 4a + 3b − a + 2b.', '3a + 5b', 'Collect like terms: 4a − a = 3a, 3b + 2b = 5b.', ['5a + 5b', '3a + b', '8ab']),
    ('Simplify 3x × 4y.', '12xy', 'Multiply the numbers and write the letters together: 3 × 4 = 12, x × y = xy.', ['7xy', '12x + y', '34xy']),
    ('Which expression means "5 less than three times n"?', '3n − 5', 'Three times n is 3n; 5 less means subtract 5.', ['5 − 3n', '3(n − 5)', '3 + n − 5']),
    ('Simplify 12p²q ÷ 4p.', '3pq', '12 ÷ 4 = 3; p² ÷ p = p; q stays.', ['3p²q', '8pq', '3p'] ),
    ('Which of these are like terms?', '5x²y and −2yx²', 'Like terms have exactly the same letters with the same powers; yx² is the same as x²y.', ['5x²y and 5xy²', '3x and 3x²', '4ab and 4a']),
    ('A pen costs p cents and a ruler costs r cents. Which expression gives the cost, in cents, of 3 pens and 2 rulers?', '3p + 2r', '3 pens cost 3p and 2 rulers cost 2r.', ['5pr', '6pr', '3r + 2p']),
    ('Simplify a × a × a × b.', 'a³b', 'a × a × a = a³.', ['3ab', 'a³ + b', '3a + b']),
])
t21.fixed('C2', (2, 3), [
    ('Explain why 3x + 2y cannot be simplified.', '3x and 2y are unlike terms (different letters), so they cannot be collected into a single term.', 'B1 unlike terms; B1 different variables cannot be combined [2]'),
    ('Explain the difference between an expression, an equation and a formula.', 'An expression is a collection of terms with no equals sign; an equation has an equals sign and can be solved for an unknown; a formula is a rule linking two or more variables.',
     'B1 expression no equals sign; B1 equation/formula distinguished [2]'),
    ('Explain why x² + x² = 2x² but x² × x² = x⁴.', 'Adding two lots of x² gives 2 lots of x²; multiplying means x × x × x × x, which is x⁴.', 'B1 addition collects like terms; B1 multiplication adds the indices [2]'),
])

VARS = ['x', 'y', 'a', 'b', 'p', 'q', 'm', 'n']


@t21.add('C1', (1, 2, 3))
def t21_collect(r, D):
    u, v = r.sample(VARS, 2)
    a, b, c, d = [r.choice([1, 2, 3, 4, 5, 6, 7, 8, 9]) * r.choice([1, 1, -1]) for _ in range(4)]
    if D >= 3:
        e = r.choice([2, 3, 4, 5])
        terms = [(a, u), (b, v), (c, u), (-d, v), (e, u + v)]
        cu, cv = a + c, b - d
        st = expr(*terms)
        cor = expr((cu, u), (cv, v), (e, u + v))
        ds = [expr((cu, u), (cv + e, v)), expr((a - c, u), (b + d, v), (e, u + v)), expr((cu + cv + e, u + v)), expr((cu, u), (b + d, v), (e, u + v))]
    else:
        terms = [(a, u), (b, v), (c, u), (-d, v)]
        cu, cv = a + c, b - d
        st = expr(*terms)
        cor = expr((cu, u), (cv, v))
        ds = [expr((a - c, u), (b + d, v)), expr((cu, u), (b + d, v)), expr((a - c, u), (cv, v)), expr((-cu, u), (cv, v))] + ([expr((cu + cv, u + v))] if abs(cu + cv) > 1 else [])
    if cu == 0 or cv == 0:
        return None
    opts, ans = mcq(r, cor, ds)
    return {'stem': f'Simplify {st}.', 'options': opts, 'answer': ans, 'key': f'Collect like terms: {u}-terms {num(a)} + {num(c)} = {num(cu)}; {v}-terms {num(b)} − {num(d)} = {num(cv)}.'}


@t21.add('C2', (2, 3, 4), 'explain')
def t21_err(r, D):
    nm = person(r)
    u, v = r.sample(VARS, 2)
    case = r.choice(['join', 'mult', 'sign'])
    a, b = r.randint(2, 9), r.randint(2, 9)
    if case == 'join':
        return Q(f'{nm} simplifies {a}{u} + {b}{v} to {a + b}{u}{v}. Explain why this is wrong.', f'{a}{u} and {b}{v} are unlike terms, so they cannot be added; {a}{u} + {b}{v} is already simplified. ({a + b}{u}{v} would mean {a + b} × {u} × {v}.)',
                 'B1 unlike terms cannot be collected; B1 states expression is already simplest [2]')
    if case == 'mult':
        return Q(f'{nm} simplifies {a}{u} × {b}{u} to {a * b}{u}. Explain the mistake and give the correct answer.', f'{u} × {u} = {u}², not {u}. Correct answer: {a * b}{u}².', f'B1 {u} × {u} = {u}²; B1 {a * b}{u}² [2]')
    c, d = r.randint(2, 9), r.randint(1, 9)
    wrong = expr((a - c, u), (b + d, v))
    return Q(f'{nm} simplifies {a}{u} + {b}{v} − {c}{u} − {d}{v} and writes {wrong}. Explain the mistake and give the correct simplified expression.',
             f'{nm} added {d}{v} instead of subtracting it. Correct: {expr((a - c, u), (b - d, v))}.', f'B1 sign error on −{d}{v}; B1 {expr((a - c, u), (b - d, v))} [2]') if b - d != 0 and a - c != 0 else None


@t21.add('C3', (1, 2, 3, 4))
def t21_mult(r, D):
    u, v = r.sample(['x', 'y', 'a', 'b', 'p', 'q'], 2)
    a, b = r.randint(2, 9), r.randint(2, 9)
    if D <= 2:
        p1, p2 = r.randint(1, 3), r.randint(1, 2)
        st = f'{mono(a, {u: p1})} × {mono(b, {u: p2, v: 1})}'
        ans = mono(a * b, {u: p1 + p2, v: 1})
        return Q(f'Simplify {st}.', ans, f'M1 {a} × {b} = {a * b}; A1 {ans} (add indices of {u}) [2]')
    if D == 3:
        k = r.randint(2, 6)
        c = a * k
        p1, q1 = r.randint(3, 5), r.randint(2, 4)
        p2, q2 = r.randint(1, p1 - 1), r.randint(1, q1)
        st = f'{mono(c, {u: p1, v: q1})} ÷ {mono(a, {u: p2, v: q2})}'
        ans = mono(k, {u: p1 - p2, v: q1 - q2})
        return Q(f'Simplify {st}.', ans, f'M1 {c} ÷ {a} = {k}; A1 {ans} (subtract indices) [2]')
    a1, b1, c1 = r.randint(2, 5), r.randint(2, 6), r.randint(2, 4)
    st = f'({mono(a1, {u: 2})} × {mono(b1, {u: 1, v: 3})}) ÷ {mono(c1 * a1, {v: 1})}' if (a1 * b1) % (c1 * a1) == 0 else None
    if not st:
        return None
    ans = mono(a1 * b1 // (c1 * a1), {u: 3, v: 2})
    return Q(f'Simplify fully {st}.', ans, f'M1 numerator {mono(a1 * b1, {u: 3, v: 3})}; M1 divide; A1 {ans} [3]')


@t21.add('C3', (1, 2, 3, 4, 5))
def t21_words(r, D):
    nm = person(r)
    case = r.choice(['age', 'shop', 'rect', 'tri', 'coins'])
    if case == 'age':
        k, d = r.randint(2, 4), r.randint(2, 9)
        a2 = r.randint(3, 8)
        if D <= 2:
            return Q(f'{nm} is x years old. {nm}\'s mother is {k} times as old as {nm}, and {nm}\'s brother is {d} years younger than {nm}. Write an expression for the brother\'s age and the mother\'s age.',
                     f'Brother: x − {d}; mother: {k}x', 'B1 x − ' + str(d) + f'; B1 {k}x [2]')
        tot = expr((k + 2, 'x'), (-d + a2, ''))
        return Q(f'{nm} is x years old. {nm}\'s mother is {k} times as old as {nm}, {nm}\'s brother is {d} years younger than {nm} and {nm}\'s cousin is {a2} years older than {nm}. Write a simplified expression for the total age of the brother, the mother and the cousin.',
                 tot, f'M1 (x − {d}) + {k}x + (x + {a2}); A1 {tot} [2]')
    if case == 'shop':
        a, b = r.randint(2, 8), r.randint(2, 6)
        it1, it2 = r.choice([('notebook', 'pen'), ('mango', 'apple'), ('coffee', 'muffin'), ('ticket', 'programme')])
        if D <= 2:
            return Q(f'A {it1} costs m dollars and a {it2} costs n dollars. Write an expression for the total cost of {a} {it1}s and {b} {it2}s.', f'{a}m + {b}n dollars', f'B1 {a}m; B1 + {b}n [2]')
        c = r.choice([20, 50, 100])
        return Q(f'A {it1} costs m dollars and a {it2} costs n dollars. {nm} buys {a} {it1}s and {b} {it2}s and pays with a ${c} note. Write an expression for the change {nm} receives.',
                 f'{c} − {a}m − {b}n dollars', f'M1 cost {a}m + {b}n; A1 {c} − ({a}m + {b}n) = {c} − {a}m − {b}n [2]')
    if case == 'rect':
        a, b = r.randint(2, 6), r.randint(1, 9)
        per = expr((2 + 2 * a, 'x'), (2 * b, ''))
        if D <= 3:
            return Q(f'A rectangle has width x cm and length ({a}x + {b}) cm. Write a simplified expression for its perimeter.', f'({per}) cm', f'M1 2(x) + 2({a}x + {b}); A1 {per} [2]')
        return Q(f'A rectangle has width x cm and its length is {b} cm more than {a} times its width. Write and simplify an expression for its perimeter in terms of x.', f'({per}) cm',
                                              f'B1 length {a}x + {b}; M1 2x + 2({a}x + {b}); A1 {per} [3]')
    if case == 'tri':
        a, b, c = r.randint(1, 4), r.randint(1, 9), r.randint(1, 9)
        per = expr((a + 2, 'y'), (b + c, ''))
        return Q(f'The sides of a triangle are y cm, ({expr((a, "y"), (b, ""))}) cm and (y + {c}) cm. Write an expression, in its simplest form, for the perimeter.', f'({per}) cm', f'M1 y + {expr((a, "y"), (b, ""))} + y + {c}; A1 {per} [2]')
    a, b = r.choice([(5, 10), (10, 20), (20, 50), (2, 5)])
    n1_, n2_ = r.randint(2, 9), r.randint(2, 9)
    return Q(f'{nm} has c coins worth {a} cents each. {nm} also has some coins worth {b} cents each, and there are {n1_} more of these than of the {a}-cent coins. Write a simplified expression for the total value of {nm}\'s coins in cents.',
             f'({a + b}c + {b * n1_}) cents', f'M1 {a}c + {b}(c + {n1_}); A1 {a + b}c + {b * n1_} [2]')


def t21_c4(r, D):
    a, b, c = r.randint(2, 5), r.randint(1, 8), r.randint(2, 6)
    nm = person(r)
    intro = f'{nm} designs a rectangular garden in {city(r)}. The garden is (x + {b}) m long and {a}x m wide. A square patio of side {c} m is in one corner of the garden; the rest of the garden is lawn.'
    per = expr((2 + 2 * a, 'x'), (2 * b, ''))
    area = expr((a, 'x²'), (a * b, 'x'))
    lawn = expr((a, 'x²'), (a * b, 'x'), (-c * c, ''))
    x = r.randint(3, 8)
    parts = [
        P('Write a simplified expression for the perimeter of the garden.', f'({per}) m', f'M1 2(x + {b}) + 2({a}x); A1 {per}', 2),
        P('Write an expression for the area of the garden, without brackets.', f'{area} m²', f'M1 {a}x(x + {b}); A1 {area}', 2),
        P('Write an expression for the area of the lawn.', f'{lawn} m²', f'B1 {area} − {c * c}', 1),
        P(f'Find the area of the lawn when x = {x}.', f'{a * x * x + a * b * x - c * c} m²', f'M1 substitutes x = {x}; A1 {a * x * x + a * b * x - c * c}', 2),
        P(f'{nm} says the perimeter is {2 + 2 * a + 2 * b}x. Explain the mistake.', f'{nm} has added the number term {2 * b} to the x-terms; they are unlike terms, so the perimeter is {per}.', 'B1 cannot add unlike terms; B1 correct expression', 2),
    ]
    return cmp_(r, intro, parts)


t21.add('C4', (2, 3, 4, 5))(t21_c4)

# ---------------------------------------------------------------- substitution
t22 = topic('Substituting into expressions and formulae', 'substituting into expressions and formulae', 'substitution', 'substituting')
t22.fixed('C1', (1, 2), [
    ('Find the value of 3a + 2b when a = 4 and b = −1.', '10', '3(4) + 2(−1) = 12 − 2 = 10.', ['14', '12', '9']),
    ('Find the value of x² when x = −5.', '25', '(−5)² = 25.', ['−25', '−10', '10']),
    ('Find the value of 2x² when x = 3.', '18', 'Square first: 3² = 9, then 2 × 9 = 18.', ['36', '12', '9']),
    ('Use the formula P = 2(l + w) to find P when l = 7 and w = 3.', '20', 'P = 2(7 + 3) = 2 × 10 = 20.', ['17', '21', '42']),
    ('Find the value of pq − r when p = −2, q = 6 and r = −3.', '−9', '(−2)(6) − (−3) = −12 + 3 = −9.', ['−15', '9', '15']),
    ('Find the value of (m − n)² when m = 2 and n = 7.', '25', '(2 − 7)² = (−5)² = 25.', ['−25', '45', '53']),
])
t22.fixed('C2', (2, 3), [
    ('Explain why 3x² and (3x)² give different values when x = 2.', '3x² = 3 × 4 = 12 (only x is squared), but (3x)² = 6² = 36 (the whole of 3x is squared).', 'B1 3x² = 12; B1 (3x)² = 36 with reason [2]'),
    ('Explain why it is useful to put a substituted negative number in brackets.', 'Brackets make the sign part of the number, so for example −x² with x = −3 is −(−3)² = −9, avoiding sign and squaring errors.', 'B1 keeps the sign with the number; B1 example [2]'),
    ('Explain why the formula v = u + at gives v = u when t = 0.', 'If t = 0, then at = a × 0 = 0, so v = u + 0 = u: at the start the velocity is the initial velocity.', 'B1 at = 0; B1 interpretation [2]'),
])

FORMULAE = [
    ('v = u + at', 'v', ['u', 'a', 't'], lambda u, a, t: u + a * t, 'velocity of a cyclist (m/s)'),
    ('s = ut + ½at²', 's', ['u', 'a', 't'], lambda u, a, t: u * t + 0.5 * a * t * t, 'distance travelled by a car (m)'),
    ('A = ½(a + b)h', 'A', ['a', 'b', 'h'], lambda a, b, h: 0.5 * (a + b) * h, 'area of a trapezium-shaped flower bed (m²)'),
    ('C = 5(F − 32) ÷ 9', 'C', ['F'], lambda F: 5 * (F - 32) / 9, 'temperature in degrees Celsius'),
    ('E = ½mv²', 'E', ['m', 'v'], lambda m, v: 0.5 * m * v * v, 'kinetic energy of a ball (J)'),
    ('T = 40m + 20', 'T', ['m'], lambda m: 40 * m + 20, 'roasting time in minutes for a chicken of mass m kg'),
    ('V = πr²h', 'V', ['r', 'h'], lambda r_, h: math.pi * r_ * r_ * h, 'volume of a cylindrical can (cm³)'),
]


@t22.add('C1', (1, 2, 3))
def t22_eval(r, D):
    a, b, c = [r.choice([-5, -4, -3, -2, -1, 2, 3, 4, 5, 6]) for _ in range(3)]
    forms = [
        (f'2a − 3b', lambda: 2 * a - 3 * b, [2 * a + 3 * b, -2 * a - 3 * b, 2 * a - 3 * abs(b)]),
        (f'a² + bc', lambda: a * a + b * c, [-a * a + b * c, a * a - b * c, 2 * a + b * c]),
        (f'abc', lambda: a * b * c, [-a * b * c, a + b + c, abs(a * b * c) + 1]),
        (f'(a + b)c', lambda: (a + b) * c, [a + b * c, -(a + b) * c, (a - b) * c]),
        (f'3a² − b', lambda: 3 * a * a - b, [(3 * a) ** 2 - b, 3 * a * a + b, 6 * a - b]),
    ]
    fstr, fn, ds = r.choice(forms[:3] if D == 1 else forms)
    v = fn()
    used = [f'{k} = {num(x)}' for k, x in (('a', a), ('b', b), ('c', c)) if k in fstr]
    return MC(r, f'Find the value of {fstr} when ' + ', '.join(used[:-1]) + f' and {used[-1]}.', v, ds + [v + 2, v - 2], f'Substitute with brackets: {fstr} = {num(v)}.')


@t22.add('C2', (2, 3, 4), 'explain')
def t22_err(r, D):
    nm = person(r)
    x = -r.randint(2, 7)
    k = r.randint(2, 5)
    c = r.randint(1, 9)
    case = r.choice(['sq', 'coef', 'sub'])
    if case == 'sq':
        return Q(f'{nm} is asked to find the value of x² + {c} when x = {num(x)}. {nm} writes {num(x)}² + {c} = {num(-x * x + c)}. Explain the mistake and find the correct value.',
                 f'{nm} has worked out −({abs(x)}²) instead of ({num(x)})². ({num(x)})² = {x * x}, so the value is {x * x + c}.', f'B1 must square the whole of {num(x)} (use brackets); B1 {x * x + c} [2]')
    if case == 'coef':
        return Q(f'{nm} finds the value of {k}x² when x = {abs(x)} by working out ({k} × {abs(x)})² = {(k * x) ** 2}. Explain the mistake and find the correct value.',
                 f'Only x is squared: {k} × {abs(x)}² = {k} × {x * x} = {k * x * x}.', f'B1 only x squared (index before multiplication); B1 {k * x * x} [2]')
    y = r.randint(2, 9)
    return Q(f'{nm} finds the value of {k}y − x when x = {num(x)} and y = {y} and gets {k * y + x}. Explain the error and find the correct value.',
             f'{nm} wrote {k * y} − {abs(x)}, ignoring that x is negative. {k * y} − ({num(x)}) = {k * y - x}.', f'B1 subtracting a negative; B1 {k * y - x} [2]')


@t22.add('C3', (1, 2, 3, 4, 5))
def t22_form(r, D):
    f, tgt, vs, fn, ctx = r.choice(FORMULAE)
    vals = {}
    for v in vs:
        vals[v] = {'u': r.choice([0, 2, 3, 5, 8, 12]), 'a': r.choice([2, 3, 4, 1.5, -2] if D >= 3 else [2, 3, 4]), 't': r.choice([3, 4, 5, 6, 8, 10]),
                   'b': r.choice([4, 6, 7, 9, 12]), 'h': r.choice([3, 4, 5, 8]), 'F': r.choice([50, 68, 77, 86, 104, 212, 14]),
                   'm': r.choice([0.5, 1.2, 2, 2.5, 3, 4.5]), 'v': r.choice([3, 4, 6, 8, 12, 15]), 'r': r.choice([3, 4, 5, 3.5, 6.2])}[v]
    if 'a' in vals and 'b' in vals and tgt == 'A':
        vals['a'] = r.choice([3, 5, 8, 10])
    res = fn(*[vals[v] for v in vs])
    given = ', '.join(f'{v} = {num(vals[v])}' for v in vs)
    ansv = n3(res) if tgt == 'V' else ex(round(res, 2))
    if D >= 4 and tgt in ('v', 's', 'E', 'T', 'A'):
        # reverse: find one variable given the result
        unk = vs[-1]
        k = vals[unk]
        others = ', '.join(f'{v} = {num(vals[v])}' for v in vs if v != unk)
        return Q(f'The formula {f} gives the {ctx}. Find {unk} when {tgt} = {ex(round(res, 2))} and {others}.', num(k),
                 f'M1 substitutes into {f}; M1 rearranges/solves; A1 {unk} = {num(k)} [3]')
    return Q(f'The formula {f} gives the {ctx}. Find {tgt} when {given}.' + (' Give your answer correct to 3 significant figures.' if tgt == 'V' else ''), ansv,
             f'M1 substitutes {given} into {f}; A1 {tgt} = {ansv} [2]')


def t22_c4(r, D):
    nm = person(r)
    base, per = r.choice([(3, 2), (4, 2.5), (2.5, 1.8), (5, 3)])
    intro = f'A taxi company in {city(r)} uses the formula C = {ex(base)} + {ex(per)}d to work out the cost C dollars of a journey of d kilometres.'
    d1 = r.choice([4, 6, 8, 12, 15])
    c2 = base + per * r.choice([10, 14, 20])
    d2 = (c2 - base) / per
    parts = [
        P(f'Find the cost of a journey of {d1} km.', money(base + per * d1), f'M1 {ex(base)} + {ex(per)} × {d1}; A1 {money(base + per * d1)}', 2),
        P(f'{nm} pays {money(c2)} for a journey. Find the length of the journey.', f'{ex(d2)} km', f'M1 {ex(base)} + {ex(per)}d = {ex(c2)}; M1 d = ({ex(c2)} − {ex(base)}) ÷ {ex(per)}; A1 {ex(d2)} km', 3),
        P(f'Explain what the number {ex(base)} represents in the formula.', f'A fixed charge of {money(base)} that is paid for every journey, even before any distance is travelled.', 'B1 fixed/starting charge', 1),
        P(f'A second company charges C = {ex(per + 0.5)}d. Find the journey length for which both companies charge the same.', f'{ex(base / 0.5)} km', f'M1 {ex(base)} + {ex(per)}d = {ex(per + 0.5)}d; A1 d = {ex(base / 0.5)}', 2),
    ]
    return cmp_(r, intro, parts)


t22.add('C4', (2, 3, 4, 5))(t22_c4)

# ---------------------------------------------------------------- expanding brackets
t23 = topic('Expanding brackets including products of two or more binomials', 'expanding brackets including products of two or more binomials', 'expanding brackets', 'binomials')
t23.fixed('C1', (1, 2), [
    ('Expand 4(2x − 3).', '8x − 12', 'Multiply each term inside by 4.', ['8x − 3', '6x − 7', '8x + 12']),
    ('Expand (x + 3)(x + 5).', 'x² + 8x + 15', 'x² + 5x + 3x + 15.', ['x² + 15', 'x² + 8x + 8', '2x + 8']),
    ('Expand (x − 4)².', 'x² − 8x + 16', '(x − 4)(x − 4) = x² − 4x − 4x + 16.', ['x² + 16', 'x² − 16', 'x² − 4x + 16']),
    ('Expand −3(a − 2b).', '−3a + 6b', '−3 × a = −3a; −3 × −2b = +6b.', ['−3a − 6b', '3a + 6b', '−3a − 2b']),
    ('Expand x(x + 7).', 'x² + 7x', 'x × x = x², x × 7 = 7x.', ['2x + 7', 'x² + 7', '8x']),
    ('Expand (x + 6)(x − 6).', 'x² − 36', 'x² − 6x + 6x − 36: the middle terms cancel.', ['x² − 12x − 36', 'x² + 36', 'x² − 12']),
])
t23.fixed('C2', (2, 3), [
    ('Explain why (x + 5)² is not equal to x² + 25.', '(x + 5)² = (x + 5)(x + 5) = x² + 5x + 5x + 25 = x² + 10x + 25; the two middle terms 10x are missing from x² + 25.', 'B1 writes as (x + 5)(x + 5); B1 shows the 10x term [2]'),
    ('Explain why expanding (x + a)(x − a) always gives an expression with only two terms.', 'The middle terms are −ax and +ax, which cancel, leaving x² − a² (the difference of two squares).', 'B1 middle terms −ax + ax = 0; B1 x² − a² [2]'),
    ('Explain how many terms you expect before simplifying when expanding (x + 1)(x + 2)(x + 3), and why.', 'Each of 2 terms × 2 terms × 2 terms gives 2 × 2 × 2 = 8 products before like terms are collected (giving x³ + 6x² + 11x + 6).', 'B1 8 products; B1 reason 2 × 2 × 2 [2]'),
])


def cfs_lin(r, D):
    a = 1 if D <= 2 else r.choice([1, 2, 3])
    c = 1 if D <= 3 else r.choice([1, 2, 3, 5])
    b = r.choice([-7, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 8])
    d = r.choice([-6, -5, -3, -2, -1, 1, 2, 3, 4, 7, 9])
    return a, b, c, d


@t23.add('C1', (1, 2, 3))
def t23_double(r, D):
    a, b, c, d = cfs_lin(r, D + 1)
    pr = poly_mul([a, b], [c, d])
    cor = poly_str(pr)
    ds = [poly_str([a * c, 0, b * d]), poly_str([a * c, b + d, b * d]) if a * c != 1 or (b + d) != pr[1] else poly_str([a * c, -pr[1], b * d]),
          poly_str([a * c, pr[1], -b * d]), poly_str([a * c, -pr[1], b * d]), poly_str([a + c, pr[1], b * d])]
    opts, ans = mcq(r, cor, ds)
    return {'stem': f'Expand and simplify {lb(a, b)}{lb(c, d)}.', 'options': opts, 'answer': ans,
            'key': f'Multiply every term in the first bracket by every term in the second: {mono(a * c, {"x": 2})}, {num(a * d)}x, {num(b * c)}x, {num(b * d)}; collect like terms: {cor}.'}


@t23.add('C2', (2, 3, 4), 'explain')
def t23_err(r, D):
    nm = person(r)
    b = r.choice([2, 3, 4, 5, 6, 7, 9])
    s_ = r.choice([1, -1])
    case = r.choice(['sq', 'sign', 'single'])
    if case == 'sq':
        cor = poly_str([1, 2 * s_ * b, b * b])
        return Q(f'{nm} writes ({lin(1, s_ * b)})² = x² {"+" if s_ > 0 else MINUS} {b * b}. Explain the mistake and write the correct expansion.',
                 f'Squaring a bracket means multiplying it by itself: ({lin(1, s_ * b)})({lin(1, s_ * b)}) = {cor}. {nm} has missed the two middle terms.', f'B1 missing middle terms {num(2 * s_ * b)}x; B1 {cor} [2]')
    if case == 'sign':
        k = r.randint(2, 6)
        c = r.randint(2, 9)
        wrong = expr((-k, 'x'), (-k * c, ''))
        cor = expr((-k, 'x'), (k * c, ''))
        return Q(f'{nm} expands −{k}(x − {c}) and writes {wrong}. Explain the error and give the correct expansion.', f'−{k} × −{c} = +{k * c}, not −{k * c}. Correct: {cor}.',
                 f'B1 negative × negative = positive; B1 {cor} [2]')
    p, q = r.randint(2, 7), r.randint(2, 7)
    return Q(f'{nm} says (x + {p})(x + {q}) = x² + {p * q}. Explain why {nm} is wrong by substituting x = 1.', f'Left side: {1 + p} × {1 + q} = {(1 + p) * (1 + q)}; right side: 1 + {p * q} = {1 + p * q}. They differ; the correct expansion is {poly_str([1, p + q, p * q])}.',
             f'M1 substitutes x = 1 into both sides; A1 shows {(1 + p) * (1 + q)} ≠ {1 + p * q} and gives {poly_str([1, p + q, p * q])} [2]')


@t23.add('C3', (1, 2, 3, 4, 5))
def t23_exp(r, D):
    if D == 1:
        k, a, b = r.randint(2, 9), r.randint(1, 6), r.choice([-7, -4, -3, 2, 5, 8])
        cor = expr((k * a, 'x'), (k * b, ''))
        return Q(f'Expand {k}({lin(a, b)}).', cor, f'B1 {num(k * a)}x; B1 {num(k * b)} [2]')
    if D == 2:
        k1, k2 = r.randint(2, 6), r.choice([-5, -4, -3, -2, 2, 3])
        a1, b1, a2, b2 = r.randint(1, 4), r.randint(-6, 6) or 1, r.randint(1, 4), r.randint(-6, 6) or 2
        cor = expr((k1 * a1 + k2 * a2, 'x'), (k1 * b1 + k2 * b2, ''))
        st = f'{k1}({lin(a1, b1)}) {"+" if k2 > 0 else MINUS} {abs(k2)}({lin(a2, b2)})'
        return Q(f'Expand and simplify {st}.', cor, f'M1 {expr((k1 * a1, "x"), (k1 * b1, ""))} and {expr((k2 * a2, "x"), (k2 * b2, ""))}; A1 {cor} [2]')
    if D == 3:
        a, b, c, d = cfs_lin(r, 4)
        pr = poly_mul([a, b], [c, d])
        return Q(f'Expand and simplify {lb(a, b)}{lb(c, d)}.', poly_str(pr), f'M1 at least three of the four terms {mono(a * c, {"x": 2})}, {num(a * d)}x, {num(b * c)}x, {num(b * d)}; A1 {poly_str(pr)} [2]')
    p, q, s_ = [r.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 6]) for _ in range(3)]
    a = 1 if D == 4 else r.choice([2, 3])
    pr = poly_mul(poly_mul([a, p], [1, q]), [1, s_])
    two = poly_str(poly_mul([a, p], [1, q]))
    return Q(f'Expand and simplify {lb(a, p)}{lb(1, q)}{lb(1, s_)}.', poly_str(pr), f'M1 expands two brackets: {two}; M1 multiplies by {lb(1, s_)}; A1 {poly_str(pr)} [3]')


@t23.add('C3', (2, 3, 4))
def t23_area(r, D):
    a, b = r.randint(2, 9), r.randint(1, 6)
    if D <= 3:
        pr = poly_mul([1, a], [1, b])
        return Q(f'A rectangle has length (x + {a}) cm and width (x + {b}) cm. Show that its area is ({poly_str(pr)}) cm².', 'Shown', f'M1 (x + {a})(x + {b}); A1 {expr((1, "x²"), (b, "x"), (a, "x"), (a * b, ""))} = {poly_str(pr)} [2]')
    c = r.randint(1, 3)
    big = poly_mul([2, a], [1, b])
    res = big[:]
    res[-1] -= c * c
    return Q(f'A rectangular rug measures (2x + {a}) m by (x + {b}) m. A square of side {c} m is cut out of it. Find an expanded expression for the remaining area.',
             f'{poly_str(res)} m²', f'M1 (2x + {a})(x + {b}) = {poly_str(big)}; M1 − {c * c}; A1 {poly_str(res)} [3]')


def t23_c4(r, D):
    a, b = r.randint(1, 5), r.randint(2, 6)
    intro = f'A box in the shape of a cuboid is (x + {a}) cm long, (x + {b}) cm wide and x cm high.'
    base = poly_mul([1, a], [1, b])
    vol = poly_mul(base, [1, 0])
    sa = [2 * 1 + 4, 2 * (a + b) + 2 * (a + b), 2 * a * b]  # 2(lw + lh + wh)
    sa = [x for x in [2 * 1 + 2 + 2, 2 * (a + b) + 2 * a + 2 * b, 2 * a * b]]
    xv = r.randint(2, 6)
    cube_side = lambda: None
    parts = [
        P('Write an expression for the area of the base, without brackets.', f'({poly_str(base)}) cm²', f'M1 (x + {a})(x + {b}); A1 {poly_str(base)}', 2),
        P('Show that the volume is (' + poly_str(vol) + ') cm³.', 'Shown', f'M1 x({poly_str(base)}); A1 {poly_str(vol)}', 2),
        P('Find an expanded expression for the total surface area.', f'({poly_str(sa)}) cm²', f'M1 2[(x + {a})(x + {b}) + x(x + {a}) + x(x + {b})]; M1 expansions; A1 {poly_str(sa)}', 3),
        P(f'Find the volume when x = {xv}.', f'{xv * (xv + a) * (xv + b)} cm³', f'B1 {xv} × {xv + a} × {xv + b} = {xv * (xv + a) * (xv + b)}', 1),
        P(f'Expand and simplify (x + {a})³.', poly_str(poly_mul(poly_mul([1, a], [1, a]), [1, a])), f'M1 (x + {a})² = {poly_str([1, 2 * a, a * a])}; A1 {poly_str(poly_mul(poly_mul([1, a], [1, a]), [1, a]))}', 2),
    ]
    return cmp_(r, intro, parts)


t23.add('C4', (2, 3, 4, 5))(t23_c4)

# ---------------------------------------------------------------- laws of indices
t24 = topic('Laws of indices in algebra including fractional indices', 'laws of indices in algebra including fractional indices', 'laws of indices', 'fractional indices')
t24.fixed('C1', (1, 2), [
    ('Simplify x⁵ × x³.', 'x⁸', 'Add the indices: 5 + 3 = 8.', ['x¹⁵', 'x²', '2x⁸']),
    ('Simplify y⁹ ÷ y³.', 'y⁶', 'Subtract the indices: 9 − 3 = 6.', ['y³', 'y¹²', 'y²⁷']),
    ('Simplify (a⁴)³.', 'a¹²', 'Multiply the indices: 4 × 3 = 12.', ['a⁷', 'a⁶⁴', '3a⁴']),
    ('What is the value of 25^(1/2)?', '5', 'A power of ½ means square root: √25 = 5.', ['12.5', '625', '1/5']),
    ('What is the value of 2⁻³?', '1/8', '2⁻³ = 1/2³ = 1/8.', ['−8', '−6', '8']),
    ('Simplify p⁰ (p ≠ 0).', '1', 'Any non-zero base to the power 0 is 1.', ['0', 'p', '−1']),
    ('What is the value of 8^(2/3)?', '4', '∛8 = 2, then 2² = 4.', ['16/3', '64', '2']),
])
t24.fixed('C2', (2, 3), [
    ('Explain why x⁰ = 1, using the rule xᵃ ÷ xᵇ = xᵃ⁻ᵇ.', 'xᵃ ÷ xᵃ = xᵃ⁻ᵃ = x⁰, but any non-zero number divided by itself is 1, so x⁰ = 1.', 'B1 xᵃ ÷ xᵃ = x⁰; B1 also equals 1 [2]'),
    ('Explain what the denominator and the numerator of a fractional index tell you, using 27^(2/3).', 'The denominator 3 means take the cube root (∛27 = 3); the numerator 2 means square it (3² = 9).', 'B1 denominator → root; B1 numerator → power, value 9 [2]'),
    ('Explain why a negative index does not make the value negative, using 4⁻².', '4⁻² = 1/4² = 1/16, which is positive: the negative index means the reciprocal.', 'B1 negative index is a reciprocal; B1 1/16 > 0 [2]'),
])


@t24.add('C1', (1, 2, 3))
def t24_law(r, D):
    v = r.choice(['x', 'y', 'a', 'm', 'p', 't'])
    m_, n_ = r.randint(2, 9), r.randint(2, 6)
    case = r.choice(['mul', 'div', 'pow'] if D <= 2 else ['mul', 'div', 'pow', 'neg'])
    if case == 'mul':
        return SMC(r, f'Simplify {v}{sup(m_)} × {v}{sup(n_)}.', f'{v}{sup(m_ + n_)}', [f'{v}{sup(m_ * n_)}', f'{v}{sup(abs(m_ - n_))}' if m_ != n_ else f'{v}', f'2{v}{sup(m_ + n_)}', f'{v}{sup(m_ + n_ + 1)}'], f'Add indices: {m_} + {n_} = {m_ + n_}.')
    if case == 'div':
        m_ = m_ + n_
        return SMC(r, f'Simplify {v}{sup(m_)} ÷ {v}{sup(n_)}.', f'{v}{sup(m_ - n_)}', [f'{v}{sup(m_ + n_)}', f'{v}{sup(m_ // n_) if m_ // n_ > 1 else ""}' if m_ % n_ == 0 else f'{v}{sup(m_ * n_)}', f'{v}{sup(m_ - n_ + 1)}', f'1{v}{sup(m_ - n_ - 1)}' if m_ - n_ > 2 else f'{v}⁻{sup(m_ - n_)}'], f'Subtract indices: {m_} − {n_} = {m_ - n_}.')
    if case == 'pow':
        k = r.randint(2, 5)
        return SMC(r, f'Simplify ({k}{v}{sup(m_)}){sup(n_)}.', f'{k ** n_}{v}{sup(m_ * n_)}', [f'{k}{v}{sup(m_ * n_)}', f'{k * n_}{v}{sup(m_ * n_)}', f'{k ** n_}{v}{sup(m_ + n_)}', f'{k * n_}{v}{sup(m_ + n_)}'],
                   f'Raise each factor: {k}{sup(n_)} = {k ** n_}; {v}{sup(m_)}{sup(n_)} = {v}{sup(m_ * n_)}.')
    return SMC(r, f'Write {v}⁻{sup(n_)} without a negative index.', f'1/{v}{sup(n_)}', [f'−{v}{sup(n_)}', f'{v}{sup(n_)}', f'−1/{v}{sup(n_)}', f'1/{v}⁻{sup(n_)}'], f'A negative index means the reciprocal: {v}⁻{sup(n_)} = 1/{v}{sup(n_)}.')


FRAC_BASES = [(4, 2), (9, 2), (16, 2), (25, 2), (36, 2), (49, 2), (64, 2), (81, 2), (100, 2), (8, 3), (27, 3), (64, 3), (125, 3), (1000, 3), (16, 4), (81, 4), (32, 5), (243, 5)]


@t24.add('C3', (1, 2, 3, 4))
def t24_frac(r, D):
    b, k = r.choice(FRAC_BASES)
    root = round(b ** (1 / k))
    if D <= 1:
        return Q(f'Find the value of {b}^(1/{k}).', str(root), f'B1 {b}^(1/{k}) = {"√" if k == 2 else ("∛" if k == 3 else f"{k}th root of ")}{b} = {root} [1]')
    p = r.choice([q for q in ([2, 3] if D <= 3 else [2, 3, 4]) if math.gcd(q, k) == 1] or [1])
    if D == 2:
        return Q(f'Find the value of {b}^({p}/{k}).', num(root ** p), f'M1 root first: {root}; A1 {root}{sup(p)} = {num(root ** p)} [2]')
    neg = Fr(1, root ** p)
    return Q(f'Find the value of {b}^(−{p}/{k}), giving your answer as a fraction.', num(neg), f'M1 negative index → reciprocal; M1 {b}^(1/{k}) = {root}; A1 1/{root}{sup(p)} = {num(neg)} [3]')


@t24.add('C3', (2, 3, 4, 5))
def t24_simp(r, D):
    v, w = r.sample(['x', 'y', 'a', 'b'], 2)
    if D <= 2:
        a, b = r.randint(2, 6), r.randint(2, 6)
        p1, p2, q1, q2 = r.randint(2, 6), r.randint(1, 5), r.randint(1, 4), r.randint(1, 4)
        ans = mono(a * b, {v: p1 + p2, w: q1 + q2})
        return Q(f'Simplify {mono(a, {v: p1, w: q1})} × {mono(b, {v: p2, w: q2})}.', ans, f'B1 coefficient {a * b}; B1 {ans} (add the indices of each letter) [2]')
    if D == 3:
        k = r.choice([8, 27, 64, 125])
        c = round(k ** (1 / 3))
        e1, e2 = r.choice([3, 6, 9, 12]), r.choice([3, 6, 9])
        ans = mono(c, {v: e1 // 3, w: e2 // 3})
        return Q(f'Simplify ({mono(k, {v: e1, w: e2})})^(1/3).', ans, f'M1 ∛{k} = {c}; A1 {ans} (divide each index by 3) [2]')
    k = r.choice([16, 81, 625])
    c = round(k ** 0.25)
    e = r.choice([8, 12, 4])
    p = 3
    ans = mono(c ** 3, {v: e * 3 // 4})
    return Q(f'Simplify ({k}{v}{sup(e)})^(3/4).', ans, f'M1 fourth root: {mono(c, {v: e // 4})}; M1 cube; A1 {ans} [3]')


@t24.add('C2', (2, 3, 4), 'explain')
def t24_err(r, D):
    nm = person(r)
    a, b = r.randint(2, 5), r.randint(2, 6)
    v = r.choice(['x', 'y', 'm'])
    case = r.choice(['pow', 'neg', 'frac', 'mul'])
    if case == 'pow':
        return Q(f'{nm} simplifies ({a}{v}{sup(b)})² to {a}{v}{sup(2 * b)}. Explain the mistake and give the correct answer.', f'The {a} must also be squared: ({a}{v}{sup(b)})² = {a * a}{v}{sup(2 * b)}.', f'B1 coefficient must be squared; B1 {a * a}{v}{sup(2 * b)} [2]')
    if case == 'neg':
        return Q(f'{nm} says that {a}⁻² = −{a * a}. Explain why this is wrong and give the correct value.', f'A negative index means a reciprocal, not a negative number: {a}⁻² = 1/{a}² = 1/{a * a}.', f'B1 reciprocal not negative; B1 1/{a * a} [2]')
    if case == 'frac':
        bb, k = r.choice([(8, 3), (27, 3), (16, 2), (25, 2), (64, 3)])
        rt = round(bb ** (1 / k))
        wrong = bb * 2 / k
        return Q(f'{nm} works out {bb}^(2/{k}) as {bb} × 2/{k} = {ex(round(wrong, 2))}. Explain the mistake and find the correct value.', f'A fractional index is not a multiplication: {bb}^(2/{k}) = ({"√" if k == 2 else "∛"}{bb})² = {rt}² = {rt * rt}.',
                 f'B1 denominator means root; B1 {rt * rt} [2]')
    return Q(f'{nm} simplifies {v}{sup(a)} × {v}{sup(b)} as {v}{sup(a * b)}. Explain the mistake and give the correct answer.', f'When multiplying powers of the same base you add the indices: {v}{sup(a + b)}.', f'B1 add indices (not multiply); B1 {v}{sup(a + b)} [2]')


def t24_c4(r, D):
    k = r.choice([2, 3, 5])
    p = r.randint(2, 4)
    q = r.randint(1, 3)
    n_ = p + q
    intro = f'Answer these questions about indices. Show your working.'
    a = r.choice([(4, 2), (9, 2), (8, 3), (27, 3)])
    rt = round(a[0] ** (1 / a[1]))
    x_sol = Fr(3 * a[1], 2)
    parts = [
        P(f'Simplify {k}{sup(p)} × {k}{sup(q)}, giving your answer as a power of {k}.', f'{k}{sup(n_)}', f'B1 {k}{sup(n_)}', 1),
        P(f'Find the value of n such that {k ** 2}ⁿ = {k}{sup(2 * n_)}.', str(n_), f'M1 {k ** 2} = {k}²; A1 n = {n_}', 2),
        P(f'Find x when {a[0]}ˣ = {rt ** 3}.', num(x_sol), f'M1 {a[0]} = {rt}{sup(a[1])}, {rt ** 3} = {rt}³; M1 {a[1]}x = 3; A1 x = {num(x_sol)}', 3),
        P(f'Simplify (16x⁸y⁴)^(1/4) × 2x⁻¹.', '4xy', 'M1 (16x⁸y⁴)^(1/4) = 2x²y; A1 4xy', 2),
        P(f'Write {k}⁻{sup(q)} × {k}{sup(p + q)} as an integer.', num(k ** p), f'M1 {k}^({p + q} − {q}) = {k}{sup(p)}; A1 {num(k ** p)}', 2),
    ]
    return cmp_(r, intro, parts)


t24.add('C4', (2, 3, 4, 5))(t24_c4)
CHAPTERS[2] = [t21, t22, t23, t24]

# =========================================================== 3 Lines, angles and shapes
t31 = topic('Angle properties: parallel lines, triangles and quadrilaterals', 'angle properties: parallel lines, triangles and quadrilaterals', 'angle properties', 'parallel lines')
t31.fixed('C1', (1, 2), [
    ('Two parallel lines are crossed by a transversal. What is the relationship between alternate angles?', 'They are equal', 'Alternate (Z) angles between parallel lines are equal.', ['They add up to 180°', 'They add up to 90°', 'One is double the other']),
    ('Co-interior angles between parallel lines add up to', '180°', 'Co-interior (C or allied) angles are supplementary.', ['90°', '360°', 'They are equal']),
    ('What is the sum of the interior angles of a quadrilateral?', '360°', 'A quadrilateral splits into two triangles: 2 × 180° = 360°.', ['180°', '540°', '720°']),
    ('An angle of 134° is', 'obtuse', 'Obtuse angles are between 90° and 180°.', ['acute', 'reflex', 'a right angle']),
    ('Angles on a straight line add up to', '180°', 'A straight line is half a full turn.', ['90°', '360°', '270°']),
    ('Which quadrilateral has exactly one pair of parallel sides?', 'Trapezium', 'A trapezium has one pair of parallel sides; a parallelogram has two.', ['Rhombus', 'Parallelogram', 'Kite']),
    ('In an isosceles triangle the two base angles are', 'equal', 'The angles opposite the equal sides are equal.', ['supplementary', 'complementary', 'both 60°']),
    ('The exterior angle of a triangle is equal to', 'the sum of the two interior opposite angles', 'Exterior angle = sum of interior opposite angles.', ['the adjacent interior angle', '180°', 'the largest interior angle']),
])
t31.fixed('C2', (2, 3), [
    ('Explain why the angles in a triangle add up to 180°, using a line drawn through one vertex parallel to the opposite side.', 'The two angles next to the vertex on the parallel line are alternate to the other two angles of the triangle, and the three angles at the vertex lie on a straight line, so they add up to 180°.',
     'B1 alternate angles equal; B1 angles on a straight line = 180° [2]'),
    ('Explain why opposite angles of a parallelogram are equal.', 'Adjacent angles are co-interior between parallel sides so each pair adds to 180°; each opposite angle is 180° minus the same angle, so opposite angles are equal.',
     'B1 co-interior angles supplementary; B1 deduces opposite angles equal [2]'),
    ('Explain why a triangle cannot have two obtuse angles.', 'Two obtuse angles would already add up to more than 180°, leaving no angle for the third vertex; the angle sum is only 180°.', 'B1 two obtuse > 180°; B1 angle sum 180° [2]'),
    ('Explain the difference between corresponding and alternate angles.', 'Corresponding angles are in matching positions at each intersection (an F shape); alternate angles are on opposite sides of the transversal between the parallel lines (a Z shape). Both pairs are equal.',
     'B1 corresponding F / same position; B1 alternate Z / opposite sides between lines [2]'),
])

PAIRS = [('alternate', 'equal'), ('corresponding', 'equal'), ('co-interior', 'supplementary'), ('vertically opposite', 'equal')]


@t31.add('C1', (1, 2, 3))
def t31_pair(r, D):
    x = r.randint(38, 142)
    kind, rel = r.choice(PAIRS)
    c = x if rel == 'equal' else 180 - x
    stem = (f'Two parallel lines are crossed by a transversal. One angle is {x}°. Find the size of the angle that is {kind} to it.' if kind != 'vertically opposite'
            else f'Two straight lines cross. One of the angles formed is {x}°. Find the angle vertically opposite to it.')
    return MC(r, stem, c, [180 - c, 360 - c, 90 - c if c < 90 else c - 90, c + 10], f'{kind.capitalize()} angles are {rel}' + ('' if rel == 'equal' else f': 180 − {x} = {c}') + '.', fmtf=lambda v: f'{num(v)}°')


@t31.add('C2', (2, 3, 4), 'explain')
def t31_reason(r, D):
    nm = person(r)
    x = r.randint(40, 130)
    case = r.choice(['iso', 'parallel', 'quad'])
    if case == 'iso':
        apex = r.choice([30, 36, 40, 44, 50, 52, 70, 76, 80, 100, 110, 120])
        b = (180 - apex) // 2 if (180 - apex) % 2 == 0 else None
        if b is None:
            return None
        return Q(f'Triangle PQR is isosceles with PQ = PR and angle QPR = {apex}°. {nm} says angle PQR = {180 - apex}°. Explain the mistake and find angle PQR, giving reasons.',
                 f'{nm} has not shared the remaining {180 - apex}° between the two equal base angles. Angle PQR = (180 − {apex}) ÷ 2 = {b}° (angles in a triangle sum to 180°; base angles of an isosceles triangle are equal).',
                 f'B1 base angles equal so divide by 2; B1 {b}° with both reasons [2]')
    if case == 'parallel':
        return Q(f'AB is parallel to CD. A transversal makes an angle of {x}° with AB. {nm} says the co-interior angle at CD is also {x}°. Explain whether {nm} is correct.',
                 f'No. Co-interior angles add up to 180°, so the angle is 180 − {x} = {180 - x}° (unless the angle is 90°).', f'B1 co-interior angles are supplementary; B1 {180 - x}° [2]')
    a, b, c = r.randint(70, 120), r.randint(60, 110), r.randint(50, 100)
    d = 360 - a - b - c
    if d <= 20 or d >= 180:
        return None
    return Q(f'Three angles of a quadrilateral are {a}°, {b}° and {c}°. {nm} says the fourth angle is {180 - (a + b + c - 180) if a + b + c > 180 else 180 - a - b - c}° using the angle sum of a triangle. Explain the error and find the fourth angle.',
             f'The angles of a quadrilateral add up to 360°, not 180°. Fourth angle = 360 − {a + b + c} = {d}°.', f'B1 quadrilateral sum 360°; B1 {d}° [2]')


@t31.add('C3', (1, 2, 3, 4, 5))
def t31_find(r, D):
    if D == 1:
        a, b = r.randint(30, 80), r.randint(30, 80)
        return Q(f'Two angles of a triangle are {a}° and {b}°. Find the third angle.', f'{180 - a - b}°', f'M1 180 − {a} − {b}; A1 {180 - a - b}° [2]')
    if D == 2:
        a = r.randint(35, 75)
        b = r.randint(30, 70)
        ext = a + b
        return Q(f'In triangle ABC, angle A = {a}° and angle B = {b}°. Side BC is extended to D. Find the exterior angle ACD, giving a reason.', f'{ext}°',
                 f'M1 exterior angle = sum of interior opposite angles (or 180 − {180 - ext}); A1 {ext}° [2]')
    if D == 3:
        k = r.choice([(1, 2, 3, 4), (2, 3, 4, 6), (3, 4, 5, 6), (1, 3, 4, 4), (2, 2, 3, 5)])
        tot = sum(k)
        if 360 % tot:
            return None
        u = 360 // tot
        return Q(f'The angles of a quadrilateral are in the ratio {":".join(map(str, k))}. Find the size of the largest angle.', f'{max(k) * u}°', f'M1 360 ÷ {tot} = {u}; M1 × {max(k)}; A1 {max(k) * u}° [3]')
    # algebraic
    a, b, c = r.randint(2, 4), r.randint(5, 30), r.randint(10, 40)
    # angles x, a x + b, 2x - c... in triangle
    x = Fr(180 - b + c, a + 1 + 2)
    if x.denominator != 1 or 2 * x - c <= 0 or x <= 0:
        return None
    x = int(x)
    angs = [x, a * x + b, 2 * x - c]
    stem = f'The angles of a triangle are x°, ({a}x + {b})° and (2x − {c})°. Form and solve an equation to find x, then find the largest angle.'
    return Q(stem, f'x = {x}; largest angle {max(angs)}°', f'M1 x + {a}x + {b} + 2x − {c} = 180; M1 {a + 3}x = {180 - b + c}; A1 x = {x}; A1 {max(angs)}° [4]')


@t31.add('C3', (2, 3, 4))
def t31_parallel(r, D):
    x = r.randint(40, 130)
    if D <= 2:
        return Q(f'AB and CD are parallel lines. A transversal crosses AB at P and CD at Q. Angle BPQ = {x}°. Find angle PQC and angle PQD, giving reasons.',
                 f'PQC = {x}° (alternate angles), PQD = {180 - x}° (angles on a straight line)', f'B1 {x}° alternate; B1 {180 - x}° with reason [2]')
    y = r.randint(30, 70)
    if x + y >= 180:
        return None
    return Q(f'AB is parallel to DC in the trapezium ABCD. Angle DAB = {x}° and angle ABC = {180 - y}°. Find angle ADC and angle BCD, giving reasons.',
             f'ADC = {180 - x}°, BCD = {y}°', f'M1 co-interior angles add to 180°; A1 ADC = {180 - x}°; A1 BCD = {y}° [3]')


def t31_c4(r, D):
    x = r.randint(25, 55)
    a = r.randint(50, 80)
    intro = f'Lines PQ and RS are parallel, with P and R on the left and Q and S on the right. Point A lies on PQ and point B lies on RS. Point C lies between the two lines, to the right of both A and B, so that ABC is a triangle. Angle QAC = {x}° and angle SBC = {a}°.'
    # angle ACB = x + a (zigzag rule) when C is between lines and angles measured appropriately
    parts = [
        P('Find angle ACB, giving reasons.', f'{x + a}°', f'M1 draw line through C parallel to PQ; M1 alternate angles {x}° and {a}°; A1 {x + a}°', 3),
        P(f'Triangle ABC is isosceles with CA = CB. Find angle CAB.', f'{ex((180 - x - a) / 2)}°', f'M1 (180 − {x + a}) ÷ 2; A1 {ex((180 - x - a) / 2)}°', 2),
        P('A line is drawn through C parallel to PQ. Name the type of angle pair formed by angle QAC and the angle between CA and this line.', 'Alternate angles', 'B1 alternate', 1),
        P('Find the reflex angle ACB.', f'{360 - x - a}°', f'B1 360 − {x + a} = {360 - x - a}° (angles at a point)', 1),
    ]
    return cmp_(r, intro, parts)


t31.add('C4', (2, 3, 4, 5))(t31_c4)


def t31_c4b(r, D):
    a = r.randint(60, 80)
    b = r.randint(95, 125)
    c = r.randint(50, 75)
    d = 360 - a - b - c
    if d <= 30 or d >= 175:
        return None
    nm = person(r)
    intro = f'{nm} draws a quadrilateral ABCD with angle A = {a}°, angle B = {b}° and angle C = {c}°. Side CD is extended beyond D to point E.'
    parts = [
        P('Find angle D (angle ADC).', f'{d}°', f'M1 360 − ({a} + {b} + {c}); A1 {d}°', 2),
        P('Find angle ADE.', f'{180 - d}°', f'B1 180 − {d} = {180 - d}° (angles on a straight line)', 1),
        P('Show that ABCD is not a parallelogram.', f'In a parallelogram opposite angles are equal, but A = {a}° and C = {c}° are not equal.', 'B1 opposite angles of parallelogram equal; B1 compares A and C', 2),
        P(f'{nm} changes the shape so that AB is parallel to DC, keeping angle B = {b}°. Find the new angle C.', f'{180 - b}°', f'M1 co-interior angles add to 180°; A1 {180 - b}°', 2),
    ]
    return cmp_(r, intro, parts)


t31.add('C4', (3, 4, 5))(t31_c4b)

# ---------------------------------------------------------------- polygons
t32 = topic('Angle sums of interior and exterior angles of polygons', 'angle sums of interior and exterior angles of polygons', 'interior and exterior angles', 'polygons')
t32.fixed('C1', (1, 2), [
    ('What is the sum of the exterior angles of any convex polygon?', '360°', 'Walking round the polygon you make one full turn.', ['180°', '540°', 'It depends on the number of sides']),
    ('What is the sum of the interior angles of a pentagon?', '540°', '(5 − 2) × 180 = 540°.', ['360°', '720°', '900°']),
    ('What is the size of each exterior angle of a regular hexagon?', '60°', '360 ÷ 6 = 60°.', ['120°', '30°', '720°']),
    ('What is the size of each interior angle of a regular octagon?', '135°', 'Exterior 360 ÷ 8 = 45°, interior 180 − 45 = 135°.', ['45°', '120°', '1080°']),
    ('What is the name of a polygon with 9 sides?', 'Nonagon', 'Nona = 9.', ['Octagon', 'Decagon', 'Heptagon']),
    ('An interior angle and its exterior angle at the same vertex add up to', '180°', 'They lie on a straight line.', ['90°', '360°', 'the number of sides × 180°']),
])
t32.fixed('C2', (2, 3), [
    ('Explain why the interior angles of an n-sided polygon add up to (n − 2) × 180°.', 'Drawing diagonals from one vertex splits the polygon into n − 2 triangles, each with an angle sum of 180°.', 'B1 n − 2 triangles from one vertex; B1 each 180° [2]'),
    ('Explain why a regular polygon cannot have an exterior angle of 50°.', '360 ÷ 50 = 7.2, which is not a whole number of sides.', 'B1 n = 360 ÷ exterior; B1 7.2 not an integer [2]'),
    ('Explain why regular hexagons tessellate but regular pentagons do not.', 'Each hexagon angle is 120° and 3 × 120 = 360°, so they fit round a point; each pentagon angle is 108° and 360 is not a multiple of 108.', 'B1 120 × 3 = 360; B1 108 does not divide 360 [2]'),
])

POLY = {3: 'triangle', 4: 'quadrilateral', 5: 'pentagon', 6: 'hexagon', 7: 'heptagon', 8: 'octagon', 9: 'nonagon', 10: 'decagon', 12: 'dodecagon', 15: '15-sided polygon', 18: '18-sided polygon', 20: '20-sided polygon', 24: '24-sided polygon', 30: '30-sided polygon', 36: '36-sided polygon'}
REG = [5, 6, 8, 9, 10, 12, 15, 18, 20, 24, 30, 36]


@t32.add('C1', (1, 2, 3))
def t32_q(r, D):
    n = r.choice([5, 6, 7, 8, 9, 10] if D <= 2 else [12, 15, 18, 20, 24])
    case = r.choice(['sum', 'ext', 'int'] if n in REG else ['sum'])
    if case == 'sum':
        c = (n - 2) * 180
        return MC(r, f'Find the sum of the interior angles of {"an" if POLY[n][:2] in ("18", "8-") else art(POLY[n]).split()[0]} {POLY[n]}.', c, [n * 180, (n - 1) * 180, (n - 3) * 180, 360], f'({n} − 2) × 180 = {c}°.', fmtf=lambda v: f'{num(v)}°')
    if case == 'ext':
        c = 360 // n
        return MC(r, f'Find the size of one exterior angle of a regular {POLY[n]}.', c, [180 - c, 180 // n if 180 % n == 0 else c + 5, c * 2, (n - 2) * 180], f'360 ÷ {n} = {c}°.', fmtf=lambda v: f'{num(v)}°')
    c = 180 - 360 // n
    return MC(r, f'Find the size of one interior angle of a regular {POLY[n]}.', c, [360 // n, (n - 2) * 180, c - 10, 180 - 180 // n if 180 % n == 0 else c + 6], f'Exterior = 360 ÷ {n} = {360 // n}°, interior = 180 − {360 // n} = {c}°.', fmtf=lambda v: f'{num(v)}°')


@t32.add('C2', (2, 3, 4), 'explain')
def t32_err(r, D):
    nm = person(r)
    case = r.choice(['ext', 'sum', 'reg'])
    n = r.choice(REG)
    if case == 'ext':
        return Q(f'{nm} says each exterior angle of a regular {POLY[n]} is {180 - 360 // n}°. Explain the mistake and give the correct exterior angle.', f'{180 - 360 // n}° is the interior angle. The exterior angle is 360 ÷ {n} = {360 // n}°.',
                 f'B1 confuses interior with exterior; B1 {360 // n}° [2]')
    if case == 'sum':
        n = r.randint(6, 14)
        return Q(f'{nm} says the interior angles of a polygon with {n} sides add up to {n} × 180 = {n * 180}°. Explain the mistake and find the correct sum.', f'The polygon divides into {n} − 2 = {n - 2} triangles, not {n}. Sum = {n - 2} × 180 = {(n - 2) * 180}°.',
                 f'B1 n − 2 triangles; B1 {(n - 2) * 180}° [2]')
    ang = r.choice([100, 130, 145, 155, 158, 165])
    ext = 180 - ang
    ok = 360 % ext == 0
    return Q(f'{nm} says a regular polygon can have an interior angle of {ang}°. Decide whether {nm} is correct, giving a reason.',
             f'Exterior angle = 180 − {ang} = {ext}°; 360 ÷ {ext} = {ex(round(360 / ext, 2))}' + (f', a whole number, so yes: it has {360 // ext} sides.' if ok else ', not a whole number, so no.'),
             f'M1 exterior {ext}° and 360 ÷ {ext}; A1 correct conclusion [2]')


@t32.add('C3', (1, 2, 3, 4, 5))
def t32_calc(r, D):
    if D <= 2:
        n = r.choice(REG)
        return Q(f'A regular polygon has an exterior angle of {360 // n}°. Find the number of sides and the sum of its interior angles.', f'{n} sides; {(n - 2) * 180}°',
                 f'M1 360 ÷ {360 // n}; A1 {n}; A1 ({n} − 2) × 180 = {(n - 2) * 180}° [3]')
    if D == 3:
        n = r.choice(REG[2:])
        ia = 180 - 360 // n
        return Q(f'Each interior angle of a regular polygon is {ia}°. Find the number of sides of the polygon.', f'{n}', f'M1 exterior = 180 − {ia} = {360 // n}; M1 360 ÷ {360 // n}; A1 {n} [3]')
    n = r.choice([5, 6, 7, 8])
    S = (n - 2) * 180
    k = r.randint(2, 5)
    known = [r.randint(95, 150) for _ in range(n - 2)]
    rest = S - sum(known)
    # two remaining angles x and kx
    x = Fr(rest, k + 1)
    if x.denominator != 1 or not (20 < x < 180) or k * x >= 180:
        return None
    return Q(f'{art(POLY[n]).capitalize()} has angles {", ".join(f"{a}°" for a in known)}, x° and {k}x°. Find the value of x.', f'x = {int(x)}',
             f'B1 angle sum ({n} − 2) × 180 = {S}°; M1 {sum(known)} + {k + 1}x = {S}; A1 x = {int(x)} [3]')


def t32_c4(r, D):
    n = r.choice([5, 6, 8, 9, 10, 12])
    ia, ea = 180 - 360 // n, 360 // n
    intro = f'A tile designer in {city(r)} is using regular polygons. The first tile is a regular {POLY[n]}.'
    parts = [
        P('Find the size of an exterior angle of the tile.', f'{ea}°', f'B1 360 ÷ {n} = {ea}°', 1),
        P('Find the size of an interior angle of the tile.', f'{ia}°', f'B1 180 − {ea} = {ia}°', 1),
        P('Find the sum of the interior angles of the tile.', f'{(n - 2) * 180}°', f'M1 ({n} − 2) × 180; A1 {(n - 2) * 180}°', 2),
        P('Decide whether these tiles can tessellate on their own, giving a reason.', ('Yes' if 360 % ia == 0 else 'No') + f': 360 ÷ {ia} = {ex(round(360 / ia, 2))}' + (', a whole number.' if 360 % ia == 0 else ', not a whole number.'),
          f'M1 360 ÷ {ia}; A1 conclusion', 2),
        P(f'Two of these tiles and one regular polygon with m sides fit exactly round a point. Find m.' if (360 - 2 * ia) > 0 and 360 % (180 - (360 - 2 * ia)) == 0 and 360 - 2 * ia < 180 else 'Find the number of diagonals that can be drawn from one vertex of the tile.',
          (f'm = {360 // (180 - (360 - 2 * ia))}' if (360 - 2 * ia) > 0 and 360 % (180 - (360 - 2 * ia)) == 0 and 360 - 2 * ia < 180 else f'{n - 3}'),
          (f'M1 remaining angle 360 − 2 × {ia} = {360 - 2 * ia}°; M1 exterior 180 − {360 - 2 * ia}; A1 m = {360 // (180 - (360 - 2 * ia))}' if (360 - 2 * ia) > 0 and 360 % (180 - (360 - 2 * ia)) == 0 and 360 - 2 * ia < 180 else f'B1 n − 3 = {n - 3}'),
          3 if (360 - 2 * ia) > 0 and 360 % (180 - (360 - 2 * ia)) == 0 and 360 - 2 * ia < 180 else 1),
    ]
    return cmp_(r, intro, parts)


t32.add('C4', (2, 3, 4, 5))(t32_c4)

# ---------------------------------------------------------------- circle theorems
t33 = topic('Circle theorems: angles in semicircle, tangent-radius, angle at centre, cyclic quadrilateral, alternate segment',
            'circle theorems: angles in semicircle, tangent-radius, angle at centre, cyclic quadrilateral, alternate segment', 'circle theorems', 'cyclic quadrilateral')
t33.fixed('C1', (1, 2), [
    ('The angle in a semicircle is', '90°', 'An angle subtended by a diameter at the circumference is a right angle.', ['180°', '45°', '60°']),
    ('The angle between a tangent and the radius at the point of contact is', '90°', 'A tangent is perpendicular to the radius at the point of contact.', ['180°', '45°', 'equal to the angle at the centre']),
    ('Opposite angles of a cyclic quadrilateral', 'add up to 180°', 'Opposite angles of a cyclic quadrilateral are supplementary.', ['are equal', 'add up to 360°', 'add up to 90°']),
    ('The angle at the centre of a circle is ___ the angle at the circumference subtended by the same arc.', 'twice', 'Angle at centre = 2 × angle at circumference.', ['half', 'equal to', 'three times']),
    ('Angles in the same segment of a circle are', 'equal', 'Angles subtended by the same chord in the same segment are equal.', ['supplementary', 'complementary', 'always 90°']),
    ('The alternate segment theorem says the angle between a tangent and a chord equals', 'the angle in the alternate segment', 'The tangent–chord angle equals the inscribed angle on the other side of the chord.', ['the angle at the centre', '90°', 'half the angle in the alternate segment']),
    ('Two tangents are drawn to a circle from an external point. The lengths from the point to the points of contact are', 'equal', 'Tangents from an external point are equal in length.', ['in the ratio 1 : 2', 'perpendicular', 'always equal to the radius']),
])
t33.fixed('C2', (2, 3), [
    ('Explain why the angle in a semicircle is 90°, using the angle at the centre theorem.', 'The diameter makes a straight angle of 180° at the centre; the angle at the circumference is half of this, 90°.', 'B1 angle at centre 180°; B1 half → 90° [2]'),
    ('Explain why triangle OAB is isosceles when O is the centre of a circle and A and B lie on the circle.', 'OA and OB are both radii, so they are equal in length.', 'B1 OA = OB radii; B1 isosceles so base angles equal [2]'),
    ('State the reason you would give for "angle OAT = 90°" when TA is a tangent at A and O is the centre.', 'The tangent is perpendicular to the radius at the point of contact.', 'B1 tangent; B1 perpendicular to radius [2]'),
])


@t33.add('C1', (1, 2, 3))
def t33_q(r, D):
    x = r.randint(25, 80)
    case = r.choice(['centre', 'cyclic', 'semi', 'tangent', 'segment'])
    if case == 'centre':
        return MC(r, f'Points A, B and C lie on a circle with centre O. Angle ACB = {x}°, with C on the major arc. Find angle AOB.', 2 * x, [x, x / 2, 180 - x, 180 - 2 * x],
                  'Angle at centre = 2 × angle at circumference.', fmtf=lambda v: f'{ex(v)}°')
    if case == 'cyclic':
        y = r.randint(60, 130)
        return MC(r, f'ABCD is a cyclic quadrilateral. Angle ABC = {y}°. Find angle ADC.', 180 - y, [y, 360 - y, 90 - y / 2 if y < 180 else y, 2 * y if 2 * y < 360 else y + 10], 'Opposite angles of a cyclic quadrilateral add up to 180°.', fmtf=lambda v: f'{ex(v)}°')
    if case == 'semi':
        return MC(r, f'AB is a diameter of a circle and C is a point on the circle. Angle CAB = {x}°. Find angle CBA.', 90 - x, [180 - x, x, 2 * x, 90 + x], f'Angle ACB = 90° (angle in a semicircle), so CBA = 180 − 90 − {x} = {90 - x}°.', fmtf=lambda v: f'{ex(v)}°')
    if case == 'tangent':
        return MC(r, f'TA is a tangent to a circle with centre O at the point A. Angle AOT = {x}°. Find angle ATO.', 90 - x, [180 - x, x, 2 * x, 90 + x], f'Angle OAT = 90° (tangent ⟂ radius), so ATO = 180 − 90 − {x} = {90 - x}°.', fmtf=lambda v: f'{ex(v)}°')
    return MC(r, f'A, B, C and D lie on a circle, with C and D on the same side of chord AB. Angle ACB = {x}°. Find angle ADB.', x, [180 - x, 2 * x, 90 - x, x / 2], 'Angles in the same segment are equal.', fmtf=lambda v: f'{ex(v)}°')


@t33.add('C2', (2, 3, 4), 'explain')
def t33_err(r, D):
    nm = person(r)
    x = r.randint(30, 75)
    case = r.choice(['centre', 'cyclic', 'alt'])
    if case == 'centre':
        return Q(f'A, B and C lie on a circle with centre O, with C on the major arc. Angle AOB = {2 * x}°. {nm} says angle ACB = {4 * x}° because "the angle at the circumference is double". Explain the mistake and find angle ACB.',
                 f'It is the angle at the centre that is double the angle at the circumference. Angle ACB = {2 * x} ÷ 2 = {x}°.', f'B1 centre angle is twice circumference angle; B1 {x}° [2]')
    if case == 'cyclic':
        y = r.randint(70, 120)
        return Q(f'PQRS is a cyclic quadrilateral with angle PQR = {y}°. {nm} says angle PSR = {y}° because opposite angles are equal. Explain the mistake and find angle PSR.',
                 f'Opposite angles of a cyclic quadrilateral add up to 180° (they are equal in a parallelogram, not in general). PSR = 180 − {y} = {180 - y}°.', f'B1 supplementary, not equal; B1 {180 - y}° [2]')
    return Q(f'TA is a tangent to a circle at A, and AB is a chord. Angle TAB = {x + 20}°. C is a point on the circle in the alternate segment. {nm} says angle ACB = {90 - x - 20 if 90 - x - 20 > 0 else 180 - x - 20}°. Explain which theorem should be used and find angle ACB.',
             f'The alternate segment theorem: the angle between the tangent and the chord equals the angle in the alternate segment, so ACB = {x + 20}°.', f'B1 names alternate segment theorem; B1 {x + 20}° [2]')


@t33.add('C3', (1, 2, 3, 4, 5))
def t33_calc(r, D):
    x = r.randint(25, 70)
    case = r.choice(['iso', 'cyc', 'tan2', 'semi2'] if D >= 3 else ['iso', 'cyc'])
    if case == 'iso':
        a = r.choice([40, 50, 64, 70, 76, 84, 96, 110, 120])
        return Q(f'A and B lie on a circle with centre O. Angle AOB = {a}°. Find angle OAB, giving reasons.', f'{(180 - a) // 2 if a % 2 == 0 else ex((180 - a) / 2)}°',
                 f'B1 OA = OB (radii) so triangle OAB is isosceles; M1 (180 − {a}) ÷ 2; A1 {ex((180 - a) / 2)}° [3]')
    if case == 'cyc':
        a, b = r.randint(70, 115), r.randint(65, 120)
        return Q(f'ABCD is a cyclic quadrilateral. Angle DAB = {a}° and angle ABC = {b}°. Find angle BCD and angle CDA, giving a reason.', f'BCD = {180 - a}°, CDA = {180 - b}°',
                 f'B1 opposite angles of a cyclic quadrilateral sum to 180°; B1 BCD = {180 - a}°; B1 CDA = {180 - b}° [3]')
    if case == 'tan2':
        t = r.randint(30, 80)
        return Q(f'From a point T outside a circle with centre O, two tangents TA and TB are drawn. Angle ATB = {t}°. Find angle AOB and angle TAB, giving reasons.',
                 f'AOB = {180 - t}°, TAB = {ex((180 - t) / 2)}°', f'B1 OAT = OBT = 90° (tangent ⟂ radius); M1 360 − 90 − 90 − {t}; A1 AOB = {180 - t}°; B1 TA = TB so TAB = {ex((180 - t) / 2)}° [4]')
    return Q(f'AB is a diameter of a circle with centre O. C is a point on the circle such that angle CAB = {x}°. D is a point on the circle on the opposite side of AB from C, with angle ABD = {x + 10}°. Find angle ACB, angle ABC and angle BAD, giving reasons.',
             f'ACB = 90°, ABC = {90 - x}°, BAD = {80 - x}°', f'B1 ACB = 90° (angle in semicircle); B1 ABC = {90 - x}°; M1 ADB = 90°; A1 BAD = {80 - x}° [4]')


def t33_c4(r, D):
    x = r.randint(28, 62)
    y = r.randint(35, 70)
    intro = f'A, B, C and D are points on a circle with centre O. TA is the tangent to the circle at A. Angle TAB = {x}° and angle ABD = {y}°, where D is on the opposite side of AB from T.'
    if x + y >= 150:
        return None
    parts = [
        P('Find angle ADB, giving a reason.', f'{x}°', f'B1 {x}°; B1 alternate segment theorem', 2),
        P('Find angle ACB, where C is on the same arc as D, giving a reason.', f'{x}°', f'B1 {x}° (angles in the same segment)', 1),
        P('Find angle AOB, giving a reason.', f'{2 * x}°', f'B1 {2 * x}° (angle at centre = 2 × angle at circumference)', 1),
        P('Find angle OAB.', f'{90 - x}°', f'M1 OAT = 90° (tangent ⟂ radius) or (180 − {2 * x}) ÷ 2; A1 {90 - x}°', 2),
        P('Find angle DAB.', f'{180 - x - y}°', f'M1 angle ADB = {x}° (alternate segment theorem), so 180 − {x} − {y}; A1 {180 - x - y}°', 2),
    ]
    return cmp_(r, intro, parts)


t33.add('C4', (2, 3, 4, 5))(t33_c4)

# ---------------------------------------------------------------- constructions
t34 = topic('Geometrical constructions with ruler and compasses', 'geometrical constructions with ruler and compasses', 'constructions', 'ruler and compasses')
t34.fixed('C1', (1, 2), [
    ('Which construction gives all the points that are the same distance from two points A and B?', 'The perpendicular bisector of AB', 'Points on the perpendicular bisector of AB are equidistant from A and B.', ['The bisector of angle AOB', 'A circle centre A', 'A line parallel to AB']),
    ('Which construction gives the points equidistant from two intersecting lines?', 'The angle bisector', 'Points on the bisector of the angle are the same distance from both arms.', ['The perpendicular bisector', 'A circle', 'A line parallel to one of the lines']),
    ('Which instruments are allowed for a "ruler and compasses" construction?', 'A straight edge and a pair of compasses', 'Protractors are not used; arcs must be left visible.', ['A protractor only', 'A ruler and a protractor', 'A set square only']),
    ('When constructing a triangle with sides 5 cm, 6 cm and 7 cm, how many arcs are needed after drawing the base?', '2', 'One arc from each end of the base, with radii equal to the other two sides.', ['1', '3', '4']),
    ('Which set of side lengths cannot form a triangle?', '3 cm, 4 cm, 8 cm', 'The two shorter sides must add to more than the longest: 3 + 4 < 8.', ['3 cm, 4 cm, 5 cm', '5 cm, 5 cm, 8 cm', '6 cm, 7 cm, 12 cm']),
    ('The locus of points that are exactly 3 cm from a fixed point P is', 'a circle of radius 3 cm centred at P', 'All points at a fixed distance from a point lie on a circle.', ['a straight line through P', 'a square of side 3 cm', 'the perpendicular bisector of P']),
])
t34.fixed('C2', (2, 3), [
    ('Describe how to construct the perpendicular bisector of a line segment AB using ruler and compasses.', 'With the compasses set to more than half of AB, draw arcs from A and from B above and below the line; join the two points where the arcs cross.',
     'B1 equal arcs (radius > ½AB) from A and B; B1 join the intersections [2]'),
    ('Describe how to bisect an angle ABC using ruler and compasses.', 'Draw an arc centre B cutting BA and BC; from these two points draw equal arcs that cross; join B to the crossing point.', 'B1 arc from B meeting both arms; B1 equal arcs and join to B [2]'),
    ('Explain why construction arcs should be left on a drawing.', 'They show the method was a genuine ruler-and-compasses construction, and examiners award marks for them.', 'B1 evidence of method; B1 marks/accuracy check [2]'),
    ('Explain why a triangle with sides 4 cm, 5 cm and 10 cm cannot be constructed.', 'The arcs of radius 4 cm and 5 cm from the ends of a 10 cm base do not meet, because 4 + 5 < 10.', 'B1 4 + 5 < 10; B1 arcs do not intersect [2]'),
])


@t34.add('C1', (1, 2, 3))
def t34_tri(r, D):
    for _ in range(40):
        a, b, c = sorted(r.sample(range(3, 15), 3))
        if a + b <= c:
            bad = (a, b, c)
            break
    else:
        return None
    goods = []
    while len(goods) < 3:
        x, y, z = sorted(r.sample(range(3, 15), 3))
        if x + y > z and (x, y, z) not in goods:
            goods.append((x, y, z))
    f = lambda t: f'{t[0]} cm, {t[1]} cm, {t[2]} cm'
    opts, ans = mcq(r, f(bad), [f(g) for g in goods])
    return {'stem': 'Which of these sets of lengths cannot be the sides of a triangle?', 'options': opts, 'answer': ans, 'key': f'{bad[0]} + {bad[1]} = {bad[0] + bad[1]} ≤ {bad[2]}, so the arcs would not meet.'}


@t34.add('C2', (2, 3, 4), 'explain')
def t34_desc(r, D):
    a, b, c = sorted(r.sample(range(4, 12), 3))
    if a + b <= c:
        return None
    nm = person(r)
    case = r.choice(['sss', 'locus', 'err'])
    if case == 'sss':
        return Q(f'Describe how {nm} should construct triangle PQR with PQ = {c} cm, QR = {a} cm and PR = {b} cm, using only a ruler and compasses.',
                 f'Draw PQ = {c} cm. With compasses set to {b} cm draw an arc centred at P; with compasses set to {a} cm draw an arc centred at Q. Join P and Q to R, the point where the arcs cross.',
                 f'B1 draws base {c} cm; B1 arcs radius {b} cm from P and {a} cm from Q; B1 joins to intersection [3]')
    if case == 'locus':
        return Q(f'A gardener in {city(r)} wants to plant a tree that is equidistant from two straight fences that meet at a corner, and exactly {a} m from the corner. Describe the constructions needed to find the position.',
                 f'Bisect the angle between the fences with ruler and compasses, then draw an arc of radius {a} m (to scale) centred at the corner; the tree is where the arc cuts the bisector.',
                 'B1 angle bisector; B1 arc/circle radius from corner; B1 intersection [3]')
    return Q(f'{nm} tries to construct the perpendicular bisector of a line AB of length {c} cm by drawing arcs of radius {ex(c / 2 - 1)} cm from A and B. Explain why this does not work.',
             f'The radius must be more than half of AB ({ex(c / 2)} cm); arcs of radius {ex(c / 2 - 1)} cm do not meet, so there are no intersection points to join.', f'B1 radius must exceed ½AB = {ex(c / 2)} cm; B1 arcs do not intersect [2]')


@t34.add('C3', (1, 2, 3, 4, 5))
def t34_calc(r, D):
    case = r.choice(['mid', 'scale', 'equi'] if D >= 3 else ['mid', 'scale'])
    if case == 'mid':
        x1, y1, x2, y2 = r.randint(-4, 6), r.randint(-3, 7), r.randint(-4, 8), r.randint(-3, 9)
        if (x1, y1) == (x2, y2) or (x1 + x2) % 2 or (y1 + y2) % 2:
            return None
        mx, my = (x1 + x2) // 2, (y1 + y2) // 2
        return Q(f'The perpendicular bisector of AB is constructed, where A is ({num(x1)}, {num(y1)}) and B is ({num(x2)}, {num(y2)}). Write down the coordinates of the point where the bisector crosses AB.',
                 f'({num(mx)}, {num(my)})', f'M1 midpoint method; A1 ({num(mx)}, {num(my)}) [2]')
    if case == 'scale':
        s = r.choice([50, 100, 200, 250, 500])
        d = r.choice([3.5, 4.2, 6.4, 7.5, 8.8, 5.6])
        return Q(f'A scale drawing of a park in {city(r)} uses a scale of 1 : {s * 100}. On the drawing, a path constructed between two gates is {ex(d)} cm long. Find the real length of the path in metres.',
                 f'{ex(d * s)} m', f'M1 {ex(d)} × {s * 100} = {ex(d * s * 100)} cm; A1 {ex(d * s)} m [2]')
    a = r.choice([6, 7, 8, 9, 10])
    h = a * math.sqrt(3) / 2
    return Q(f'An equilateral triangle with sides {a} cm is constructed using ruler and compasses. The perpendicular bisector of one side is then constructed. Calculate the length of this bisector inside the triangle (the height), correct to 3 significant figures.',
             f'{n3(h)} cm', f'M1 bisector meets the side at its midpoint, {ex(a / 2)} cm from each end; M1 √({a}² − {ex(a / 2)}²); A1 {n3(h)} cm [3]')


def t34_c4(r, D):
    a, b = r.choice([(6, 8), (5, 12), (8, 15), (9, 12), (7, 24)])
    c = math.isqrt(a * a + b * b)
    nm = person(r)
    intro = f'{nm} draws triangle ABC accurately, with AB = {c} cm, BC = {a} cm and AC = {b} cm.'
    parts = [
        P('Describe how to construct the triangle using ruler and compasses only.', f'Draw AB = {c} cm; arc radius {b} cm from A and arc radius {a} cm from B; C is where they meet.', f'B1 base; B1 both arcs with correct radii', 2),
        P('Show that angle ACB is a right angle.', f'{a}² + {b}² = {a * a + b * b} = {c}², so by the converse of Pythagoras the angle opposite AB is 90°.', f'M1 {a}² + {b}² and {c}²; A1 equal so 90°', 2),
        P('The perpendicular bisector of AB is constructed. Explain why it passes through the centre of the circle through A, B and C.', 'The centre is equidistant from A and B, so it lies on the perpendicular bisector of AB; because angle ACB = 90°, AB is a diameter and the centre is the midpoint of AB.',
          'B1 equidistant from A and B; B1 AB is a diameter (angle in semicircle)', 2),
        P('Find the radius of the circle through A, B and C.', f'{ex(c / 2)} cm', f'B1 ½ × {c} = {ex(c / 2)} cm', 1),
        P('The bisector of angle ACB is constructed. Write down the angle it makes with CA.', '45°', 'B1 90 ÷ 2 = 45°', 1),
    ]
    return cmp_(r, intro, parts)


t34.add('C4', (2, 3, 4, 5))(t34_c4)
@t32.add('C3', (2, 3, 4, 5))
def t32_ratio(r, D):
    k = r.choice([2, 3, 4, 5, 8, 9, 11] if D >= 3 else [2, 3, 5])
    ext = Fr(180, k + 1)
    n = 2 * (k + 1)
    nm = person(r)
    if D <= 3:
        return Q(f'Each interior angle of a regular polygon is {k} times the size of each exterior angle. Find the number of sides.', str(n),
                 f'M1 e + {k}e = 180; A1 e = {num(ext)}°; A1 n = 360 ÷ {num(ext)} = {n} [3]')
    d = r.choice([20, 30, 40, 60])
    # interior exceeds exterior by d: i - e = d, i + e = 180 -> e = (180 - d)/2
    e = Fr(180 - d, 2)
    if 360 % e != 0:
        return None
    n2 = int(360 / e)
    return Q(f'{nm} draws a regular polygon in which each interior angle is {d}° larger than each exterior angle. Find the number of sides and the sum of the interior angles.', f'{n2} sides; {(n2 - 2) * 180}°',
             f'M1 i + e = 180 and i − e = {d}; A1 e = {num(e)}°; A1 n = {n2}; B1 sum = {(n2 - 2) * 180}° [4]')


@t33.add('C3', (2, 3, 4, 5))
def t33_alg(r, D):
    for _ in range(30):
        a, b, c, d = r.randint(2, 5), r.randint(-20, 30), 1, r.randint(5, 40)
        if a == 2 * c:
            continue
        x = Fr(2 * d - b, a - 2 * c)
        if x.denominator == 1 and 10 < x < 70 and 0 < c * x + d < 90:
            break
    else:
        return None
    x = int(x)
    bs = sgn(b) if b else ''
    return Q(f'A, B and C lie on a circle with centre O, with C on the major arc AB. Angle AOB = ({a}x{bs})° and angle ACB = (x + {d})°. Find x and angle AOB, stating the circle theorem you use.',
             f'x = {x}; AOB = {a * x + b}°', f'B1 angle at centre = 2 × angle at circumference; M1 {a}x{bs} = 2(x + {d}); A1 x = {x}; A1 {a * x + b}° [4]')


@t34.add('C3', (2, 3, 4, 5))
def t34_locus(r, D):
    h, half = r.choice([(3, 4), (5, 12), (6, 8), (8, 15), (9, 12), (4, 3), (12, 5)])
    rad = math.isqrt(h * h + half * half)
    ab = 2 * half
    nm = person(r)
    if D <= 3:
        return Q(f'Points A and B are {ab} cm apart. {nm} constructs the perpendicular bisector of AB and marks a point P on it that is {rad} cm from A. Calculate the distance from P to the midpoint of AB.', f'{h} cm',
                 f'B1 PA = PB = {rad} and M is {half} cm from A; M1 √({rad}² − {half}²); A1 {h} cm [3]')
    return Q(f'Two radio masts A and B near {city(r)} are {ab} km apart. A new mast is to be built so that it is the same distance from A and from B, and exactly {rad} km from each. Describe the construction that locates the possible positions, and find how far each position is from the line AB.',
             f'Construct the perpendicular bisector of AB and arcs of radius {rad} km (to scale) from A; two positions, each {h} km from AB.',
             f'B1 perpendicular bisector; B1 arc radius {rad} from A; M1 √({rad}² − {half}²); A1 {h} km [4]')


CHAPTERS[3] = [t31, t32, t33, t34]


# =========================================================== 4 Collecting, organising and displaying data
VARIABLES = [('the number of goals scored in a match', 'discrete'), ('the mass of a newborn baby', 'continuous'), ('favourite colour', 'qualitative'),
             ('the time taken to run 100 m', 'continuous'), ('the number of pets in a household', 'discrete'), ('shoe size', 'discrete'),
             ('the height of a sunflower', 'continuous'), ('type of transport used to get to school', 'qualitative'), ('the number of cars passing a school gate in an hour', 'discrete'),
             ('the temperature at noon', 'continuous'), ('eye colour', 'qualitative'), ('the volume of water in a bottle', 'continuous'), ('the number of siblings a student has', 'discrete'),
             ('the brand of mobile phone owned', 'qualitative'), ('the length of a leaf', 'continuous'), ('the score on a dice', 'discrete'), ('country of birth', 'qualitative'),
             ('the number of text messages sent in a day', 'discrete'), ('the distance a ball is thrown', 'continuous'), ('favourite sport', 'qualitative')]

t41 = topic('Collecting and classifying data: discrete, continuous, qualitative', 'collecting and classifying data: discrete, continuous, qualitative', 'classifying data', 'discrete continuous')
t41.fixed('C1', (1, 2), [
    ('Data collected by the person who is going to use it is called', 'primary data', 'Primary data is first-hand; secondary data was collected by someone else.', ['secondary data', 'continuous data', 'qualitative data']),
    ('Which of these is an example of secondary data?', 'Rainfall figures downloaded from a weather website', 'It was collected by someone else.', ['Heights measured by the student', 'Answers to the student\'s own questionnaire', 'Traffic counted by the student']),
    ('Data that can take any value within a range is called', 'continuous', 'Measurements such as length, mass and time are continuous.', ['discrete', 'qualitative', 'primary']),
    ('Data described in words rather than numbers is called', 'qualitative (categorical)', 'Examples: colours, types of food.', ['quantitative', 'continuous', 'discrete']),
    ('A small group chosen from a population to represent it is called a', 'sample', 'A sample represents the whole population.', ['census', 'tally', 'frequency']),
    ('Collecting data from every member of a population is called a', 'census', 'A census surveys the whole population.', ['sample', 'questionnaire', 'pilot survey']),
])
t41.fixed('C2', (2, 3), [
    ('Explain why "How much TV do you watch?" is a poor survey question, and suggest an improvement.', 'It is vague (no time period, no units) so answers cannot be compared. Better: "How many hours of TV did you watch yesterday? 0–1, 1–2, 2–3, more than 3".',
     'B1 vague / no time frame or response boxes; B1 improved question with time period and non-overlapping options [2]'),
    ('Explain why asking only students in the school basketball team is a biased way to find the favourite sport of students in a school.', 'The sample is not representative: basketball players are much more likely to choose basketball.', 'B1 not representative/biased; B1 reason [2]'),
    ('Explain the difference between discrete and continuous data, with an example of each.', 'Discrete data can only take particular (often whole-number) values, e.g. number of children; continuous data can take any value in a range, e.g. height.', 'B1 definitions; B1 correct examples [2]'),
    ('Explain one advantage and one disadvantage of using a sample rather than a census.', 'A sample is cheaper and quicker; but it may not represent the whole population, so results may be less accurate.', 'B1 advantage; B1 disadvantage [2]'),
])


@t41.add('C1', (1, 2, 3))
def t41_class(r, D):
    v, t = r.choice(VARIABLES)
    opts, ans = mcq(r, t, [x for x in ['discrete', 'continuous', 'qualitative', 'secondary'] if x != t])
    return {'stem': f'Which word best describes the data: {v}?', 'options': opts, 'answer': ans,
            'key': {'discrete': 'Discrete: it can only take separate (whole-number) values.', 'continuous': 'Continuous: it is measured and can take any value in a range.', 'qualitative': 'Qualitative: it is described in words, not numbers.'}[t]}


@t41.add('C2', (2, 3, 4), 'explain')
def t41_bias(r, D):
    nm = person(r)
    topic_, where, why = r.choice([
        ('how often people in a town use public transport', 'at a bus station at 8 am', 'people at a bus station are already using public transport'),
        ('how much exercise adults do each week', 'outside a gym', 'people at a gym are likely to exercise more than average'),
        ('the favourite type of music of people in a city', 'at a classical concert', 'concert-goers will over-represent classical music'),
        ('how many books students read', 'in the school library at lunchtime', 'library users are likely to read more than other students'),
        ('opinions about a new shopping mall', 'inside the shopping mall', 'shoppers there are likely to be in favour of the mall'),
        ('the average height of students in a school', 'in the Year 11 classroom', 'older students are taller, so the sample is not representative of all ages'),
    ])
    n = r.choice([20, 25, 30, 40, 50])
    return Q(f'{nm} wants to find out about {topic_}. {nm} asks {n} people {where}. Give two reasons why this sample may not give reliable results, and suggest an improvement.',
             f'It is biased because {why}; a sample of {n} is small. Improvement: choose a larger random sample from different places and times.',
             'B1 bias with reason; B1 sample size or single time/place; B1 sensible improvement (random/larger/varied) [3]')


@t41.add('C3', (1, 2, 3, 4, 5))
def t41_sort(r, D):
    k = 3 if D <= 2 else 4
    picks = r.sample(VARIABLES, k)
    q = ' '.join(f'({"abcd"[i]}) {v}' for i, (v, _) in enumerate(picks))
    a = ' '.join(f'({"abcd"[i]}) {t}' for i, (_, t) in enumerate(picks))
    if D >= 4:
        nm = person(r)
        pop, samp = r.choice([(800, 50), (1200, 80), (600, 40), (1500, 100)])
        yes = r.randint(int(samp * 0.2), int(samp * 0.7))
        est = yes * pop // samp if (yes * pop) % samp == 0 else round(yes * pop / samp)
        return Q(f'{nm} surveys a random sample of {samp} students from a school of {pop}. {yes} of the sample walk to school. (a) Is the number of students who walk discrete or continuous? (b) Estimate the number of students in the whole school who walk to school. (c) State one assumption you have made.',
                 f'(a) discrete (b) {est} (c) the sample is representative of the whole school', f'(a) B1 discrete (b) M1 {yes}/{samp} × {pop}; A1 {est} (c) B1 representative/random sample [4]', type='multi_step')
    return Q(f'Classify each of these types of data as discrete, continuous or qualitative. {q}', a, ' '.join(f'({"abcd"[i]}) B1 {t}' for i, (_, t) in enumerate(picks)) + f' [{k}]')


@t41.add('C3', (2, 3, 4))
def t41_quest(r, D):
    nm = person(r)
    lo = r.choice([0, 1])
    bad = r.choice([('0–2, 2–4, 4–6', 'the groups overlap (2 and 4 are in two groups) and there is no box for more than 6'), ('1–3, 5–7, more than 8', 'there are gaps (4 and 8 are missing) and 0 is not included'),
                    ('less than 2, 2–5, 5 or more', 'the value 5 belongs to two groups, and the groups are too wide to give much detail'), ('0, 1–3, 3–5', 'the groups overlap at 3 and there is no box for more than 5')])
    thing = r.choice(['books read last month', 'portions of fruit eaten yesterday', 'text messages sent yesterday', 'visits to a café last week', 'films watched last month'])
    return Q(f'{nm} writes a questionnaire about the number of {thing}. The response boxes are: {bad[0]}. Give two problems with these response boxes and write improved boxes.',
             f'Problems: {bad[1]}. Improved: 0, 1–2, 3–4, 5–6, 7 or more (whole numbers, no overlaps or gaps).', 'B1 first problem; B1 second problem; B1 non-overlapping exhaustive boxes [3]')


def t41_c4(r, D):
    nm = person(r)
    q = r.choice([('Students in Year 9 spend more time on social media than students in Year 11.', 'time spent on social media', 'continuous'),
                  ('Taller students have longer arm spans.', 'height and arm span', 'continuous'),
                  ('Most students in the school prefer football to other sports.', 'favourite sport', 'qualitative'),
                  ('Families in the town have more cars than they did ten years ago.', 'number of cars per family', 'discrete')])
    intro = f'{nm} is planning a statistical investigation to test the hypothesis: "{q[0]}"'
    parts = [
        P('State what data needs to be collected and whether it is discrete, continuous or qualitative.', f'{q[1].capitalize()}; {q[2]}', 'B1 data; B1 type', 2),
        P('Suggest how the data could be collected and whether it is primary or secondary data.', 'A questionnaire/measurement by the student (primary) or published records (secondary), with a reason.', 'B1 method; B1 primary/secondary consistent', 2),
        P('Describe how a suitable sample could be chosen and explain why it should be random.', 'Choose a random sample (e.g. random numbers from a register) of a reasonable size, e.g. 50, from each relevant group so every member has an equal chance and bias is avoided.', 'B1 random selection method; B1 reason (avoid bias) ; B1 size/groups', 3),
        P('Give one way the results could be displayed.', r.choice(['A comparative bar chart', 'A back-to-back stem-and-leaf diagram', 'A pie chart for each group']), 'B1 suitable display', 1),
    ]
    return cmp_(r, intro, parts)


t41.add('C4', (2, 3, 4, 5))(t41_c4)

# ---------------------------------------------------------------- tables
t42 = topic('Organising data in tables, two-way tables and frequency tables', 'organising data in tables, two-way tables and frequency tables', 'two-way tables', 'frequency tables')
t42.fixed('C1', (1, 2), [
    ('In a tally chart, what does 卌 ||| represent?', '8', 'Each gate (four lines and a cross line) is 5; 5 + 3 = 8.', ['7', '9', '53']),
    ('A table that shows two sets of categories at once, such as gender and favourite subject, is called', 'a two-way table', 'Rows show one category and columns another.', ['a tally chart', 'a stem-and-leaf diagram', 'a pictogram']),
    ('In the grouped frequency table with classes 0 ≤ t < 10, 10 ≤ t < 20, …, which class contains t = 10?', '10 ≤ t < 20', 'The inequality 0 ≤ t < 10 excludes 10.', ['0 ≤ t < 10', 'Both classes', 'Neither class']),
    ('Why are grouped frequency tables used for continuous data?', 'There are too many different values to list individually', 'Grouping into class intervals summarises the data.', ['To make the data qualitative', 'To find the exact mean', 'Because continuous data has no mode']),
])
t42.fixed('C2', (2, 3), [
    ('Explain why the class intervals 10–20 and 20–30 are not suitable for recording heights of plants.', 'A height of 20 cm would belong to both classes; use 10 ≤ h < 20 and 20 ≤ h < 30 instead.', 'B1 overlapping at 20; B1 correct inequality notation [2]'),
    ('Explain one disadvantage of grouping data in a frequency table.', 'The original individual values are lost, so exact statistics such as the mean or range cannot be found.', 'B1 lose raw values; B1 consequence [2]'),
    ('Explain how you can check that a completed two-way table is correct.', 'The row totals and the column totals must both add up to the same grand total.', 'B1 row totals; B1 column totals equal grand total [2]'),
])


def twoway(r):
    rows, cols, ctx = r.choice([(['Boys', 'Girls'], ['Walk', 'Bus', 'Car'], 'students and how they travel to school'),
                               (['Adults', 'Children'], ['Swim', 'Gym', 'Tennis'], 'members of a sports club and their favourite activity'),
                               (['Year 9', 'Year 10'], ['Maths', 'Science', 'Art'], 'students and their favourite subject'),
                               (['Morning', 'Afternoon'], ['Tea', 'Coffee', 'Juice'], 'customers at a café and their drink'),
                               (['Local', 'Tourist'], ['Museum', 'Beach', 'Market'], 'visitors and where they went')])
    g = [[r.randint(5, 30) for _ in cols] for _ in rows]
    return rows, cols, ctx, g


def tw_text(rows, cols, g, hide):
    rt = [sum(x) for x in g]
    ct = [sum(g[i][j] for i in range(len(rows))) for j in range(len(cols))]
    tot = sum(rt)
    out = []
    for i, rn in enumerate(rows):
        cells = [('?' if (i, j) in hide else str(g[i][j])) for j in range(len(cols))]
        out.append(f'{rn}: ' + ', '.join(f'{c} {v}' for c, v in zip(cols, cells)) + f', total {"?" if (i, "T") in hide else rt[i]}')
    out.append('Total: ' + ', '.join(f'{c} {"?" if ("T", j) in hide else ct[j]}' for j, c in enumerate(cols)) + f', overall {"?" if ("T", "T") in hide else tot}')
    return '; '.join(out), rt, ct, tot


@t42.add('C1', (1, 2, 3))
def t42_read(r, D):
    rows, cols, ctx, g = twoway(r)
    txt, rt, ct, tot = tw_text(rows, cols, g, set())
    i, j = r.randrange(len(rows)), r.randrange(len(cols))
    if D <= 2:
        c = g[i][j]
        return MC(r, f'A two-way table shows {ctx}. {txt}. How many in the group {rows[i]} chose {cols[j]}?', c, [g[1 - i][j], rt[i], ct[j], g[i][(j + 1) % 3]], f'Read the cell in row {rows[i]}, column {cols[j]}: {c}.')
    c = Fr(ct[j], tot)
    return MC(r, f'A two-way table shows {ctx}. {txt}. What fraction of the total chose {cols[j].lower()}?', c, [Fr(g[i][j], tot), Fr(ct[j], rt[i]), Fr(g[i][j], ct[j]), Fr(ct[(j + 1) % 3], tot)], f'{ct[j]} out of {tot} = {num(c)}.')


@t42.add('C3', (1, 2, 3, 4, 5))
def t42_fill(r, D):
    rows, cols, ctx, g = twoway(r)
    hide = {(0, 1), (1, 2), ('T', 0)} if D <= 2 else {(0, 0), (1, 1), (0, 'T'), ('T', 2)}
    txt, rt, ct, tot = tw_text(rows, cols, g, hide)
    ans = []
    for h in sorted(hide, key=str):
        i, j = h
        val = rt[i] if j == 'T' else (ct[j] if i == 'T' else g[i][j])
        nm = (('Total' if i == 'T' else rows[i]) + '/' + ('total' if j == 'T' else cols[j]))
        ans.append(f'{nm} = {val}')
    stem = f'A two-way table shows {ctx}, with some values missing. {txt}. Find the missing values.'
    if D >= 4:
        j = r.randrange(3)
        p = Fr(g[1][j], tot)
        stem = f'A two-way table shows {ctx}, with some values missing. {txt}. (a) Find the missing values. (b) One person is chosen at random. Find the probability that they are in the group {rows[1]} and chose {cols[j]}.'
        return Q(stem, f'(a) {"; ".join(ans)} (b) {num(p)}', f'(a) B3 for all four values (B1 for each pair) (b) B1 {g[1][j]}/{tot} [4]', type='multi_step')
    return Q(stem, '; '.join(ans), f'B1 for each correct missing value, using row/column totals [{len(hide)}]')


@t42.add('C3', (1, 2, 3, 4))
def t42_freq(r, D):
    vals = [r.choice([0, 1, 1, 2, 2, 2, 3, 3, 4, 5]) for _ in range(20 if D <= 2 else 30)]
    what = r.choice(['number of goals scored in each match by a football team', 'number of siblings of each student in a class', 'number of books borrowed by each library visitor', 'number of eggs laid each day by a hen house'])
    f = {k: vals.count(k) for k in range(0, 6)}
    tb = ', '.join(f'{k}: {f[k]}' for k in f)
    if D <= 2:
        k = r.choice([k for k in f if f[k]])
        return Q(f'Here are data showing the {what}: {", ".join(map(str, vals))}. Complete a frequency table for the values 0 to 5 and write down the frequency of {k}.', f'{tb}; frequency of {k} = {f[k]}', f'B1 tallies correct for at least four values; B1 {f[k]} [2]')
    tot = sum(k * f[k] for k in f)
    return Q(f'Here are data showing the {what}: {", ".join(map(str, vals))}. Organise the data into a frequency table for the values 0 to 5, and use it to find the total of all the values.', f'{tb}; total = {tot}',
             f'B2 frequency table (B1 one error); M1 Σ value × frequency; A1 {tot} [4]')


@t42.add('C2', (2, 3, 4), 'explain')
def t42_err(r, D):
    nm = person(r)
    rows, cols, ctx, g = twoway(r)
    txt, rt, ct, tot = tw_text(rows, cols, g, set())
    j = r.randrange(3)
    return Q(
        f'A two-way table shows {ctx}. {txt}. {nm} compares the groups using the numbers who chose {cols[j]} ({g[0][j]} and {g[1][j]}). Explain why proportions are better than these numbers, and compare the groups using proportions.',
        f'The groups are different sizes ({rt[0]} and {rt[1]}). Proportions: {rows[0]} {g[0][j]}/{rt[0]} = {n3(g[0][j] / rt[0])}, {rows[1]} {g[1][j]}/{rt[1]} = {n3(g[1][j] / rt[1])}, so {rows[0] if g[0][j] / rt[0] > g[1][j] / rt[1] else rows[1]} have the higher proportion.',
        f'B1 different group sizes; M1 both proportions; A1 correct comparison [3]')


def t42_c4(r, D):
    rows, cols, ctx, g = twoway(r)
    txt, rt, ct, tot = tw_text(rows, cols, g, {(0, 2), (1, 0), ('T', 1)})
    j = r.randrange(3)
    intro = f'A two-way table shows {ctx}. Some values are missing. {txt}.'
    parts = [
        P(f'Find the number in the group {rows[0]} who chose {cols[2]}.', str(g[0][2]), f'B1 {rt[0]} − {g[0][0]} − {g[0][1]} = {g[0][2]}', 1),
        P(f'Find the number in the group {rows[1]} who chose {cols[0]}.', str(g[1][0]), f'B1 {ct[0]} − {g[0][0]} = {g[1][0]}', 1),
        P(f'Find the total who chose {cols[1]}.', str(ct[1]), f'B1 {g[0][1]} + {g[1][1]} = {ct[1]}', 1),
        P(f'What percentage of all those in the table chose {cols[j]}?', f'{nn(100 * ct[j] / tot)}%', f'M1 {ct[j]} ÷ {tot} × 100; A1 {nn(100 * ct[j] / tot)}%', 2),
        P(f'One person from the group {rows[1]} is chosen at random. Find the probability that they chose {cols[2]}.', num(Fr(g[1][2], rt[1])), f'M1 denominator {rt[1]}; A1 {num(Fr(g[1][2], rt[1]))}', 2),
    ]
    return cmp_(r, intro, parts)


t42.add('C4', (2, 3, 4, 5))(t42_c4)

# ---------------------------------------------------------------- displaying data
t43 = topic('Displaying data: bar charts, pictograms, pie charts and line graphs', 'displaying data: bar charts, pictograms, pie charts and line graphs', 'pie charts', 'bar charts pictograms')
t43.fixed('C1', (1, 2), [
    ('In a pie chart showing 60 people, how many degrees represent one person?', '6°', '360 ÷ 60 = 6°.', ['60°', '3°', '0.6°']),
    ('In a pictogram, one symbol represents 8 cars. How many cars do 3½ symbols represent?', '28', '3.5 × 8 = 28.', ['24', '32', '35']),
    ('Which type of graph is best for showing how a temperature changes over a day?', 'A line graph', 'Line graphs show change over time.', ['A pie chart', 'A pictogram', 'A two-way table']),
    ('In a bar chart for qualitative data, the bars should', 'have gaps between them and equal widths', 'Gaps show the categories are separate.', ['touch each other', 'have different widths', 'be drawn in order of size']),
    ('In a pie chart, a sector has angle 90°. What fraction of the data does it represent?', '1/4', '90 ÷ 360 = 1/4.', ['1/2', '1/3', '9/36']),
    ('Which display shows proportions of a whole most clearly?', 'A pie chart', 'Each sector is a fraction of the full circle.', ['A line graph', 'A scatter diagram', 'A stem-and-leaf diagram']),
])
t43.fixed('C2', (2, 3), [
    ('Explain why a pie chart cannot be used to compare the actual numbers in two groups of different sizes.', 'A pie chart only shows proportions; a larger sector in one chart might represent fewer people if that chart shows a smaller total.', 'B1 shows proportions; B1 totals differ [2]'),
    ('Explain why a bar chart whose vertical axis starts at 50 instead of 0 can be misleading.', 'The bars look much more different in height than the data really are, exaggerating differences.', 'B1 axis not from 0; B1 exaggerates differences [2]'),
    ('Explain why points on a line graph may be joined with straight lines.', 'Joining shows the trend over time and allows an estimate of values between readings, assuming the change is steady between them.', 'B1 shows trend; B1 estimate intermediate values [2]'),
])


def pie_data(r, D):
    tot = r.choice([24, 30, 36, 40, 45, 60, 72, 90, 120, 180])
    k = 4 if D <= 3 else 5
    for _ in range(50):
        cuts = sorted(r.sample(range(1, tot), k - 1))
        f = [b - a for a, b in zip([0] + cuts, cuts + [tot])]
        if all(x >= 2 for x in f) and all((x * 360) % tot == 0 for x in f):
            return tot, f
    return None, None


PIE_CTX = [('favourite fruits of students', ['Mango', 'Apple', 'Banana', 'Orange', 'Grape']), ('ways employees travel to work', ['Car', 'Train', 'Bus', 'Bicycle', 'Walk']),
           ('languages spoken at home by students', ['English', 'Spanish', 'Arabic', 'Hindi', 'French']), ('types of tree in a park', ['Oak', 'Palm', 'Pine', 'Maple', 'Cedar']),
           ('favourite sports of club members', ['Football', 'Cricket', 'Tennis', 'Basketball', 'Swimming'])]


@t43.add('C3', (1, 2, 3, 4, 5))
def t43_pie(r, D):
    tot, f = pie_data(r, D)
    if not tot:
        return None
    ctx, cats = r.choice(PIE_CTX)
    cats = cats[:len(f)]
    ang = [x * 360 // tot for x in f]
    tbl = ', '.join(f'{c} {x}' for c, x in zip(cats, f))
    if D <= 2:
        return Q(f'The table shows the {ctx}: {tbl}. Calculate the angle of each sector for a pie chart.', ', '.join(f'{c} {a}°' for c, a in zip(cats, ang)),
                 f'M1 360 ÷ {tot} = {ex(360 / tot)}° per item; A2 all angles correct (A1 for two) [3]')
    if D == 3:
        i = r.randrange(len(f))
        return Q(f'A pie chart shows the {ctx}. The sector for {cats[i]} has an angle of {ang[i]}° and represents {f[i]} people. Find the total number of people in the survey and the angle for a category containing {f[(i + 1) % len(f)]} people.',
                 f'{tot} people; {ang[(i + 1) % len(f)]}°', f'M1 {f[i]} ÷ {ang[i]} × 360; A1 {tot}; B1 {ang[(i + 1) % len(f)]}° [3]')
    i, j = r.sample(range(len(f)), 2)
    return Q(f'In a pie chart of the {ctx}, the angles are ' + ', '.join(f'{c} {("x" if k == i else str(a) + "")}°' for k, (c, a) in enumerate(zip(cats, ang))) + f'. {cats[j]} represents {f[j]} people. Find x and the number of people represented by {cats[i]}.',
             f'x = {ang[i]}; {f[i]} people', f'M1 360 − sum of others; A1 x = {ang[i]}; M1 {ang[i]} ÷ {ang[j]} × {f[j]} or {ang[i]} × {tot}/360; A1 {f[i]} [4]')


@t43.add('C1', (1, 2, 3))
def t43_picto(r, D):
    k = r.choice([4, 8, 12, 20]) if D >= 3 else r.choice([2, 4, 5, 6, 8, 10, 12, 20])
    sym = r.choice([2.25, 3.75, 4.25, 5.75, 6.5, 1.75]) if D >= 3 else (r.choice([1.5, 2.5, 3.5, 4.5, 5.5]) if D == 2 else r.choice([2, 3, 4, 5, 6]))
    if (sym * k) != int(sym * k):
        return None
    c = sym * k
    item, noun = r.choice([('ice creams sold', 'ice creams'), ('books borrowed', 'books'), ('cars washed', 'cars'), ('tickets sold', 'tickets'), ('emails received', 'emails')])
    return MC(r, f'In a pictogram showing {item}, one symbol represents {k} {noun}. A row shows {ex(sym)} symbols. How many {noun} does this represent?', c, [sym, sym * k + k, k * math.floor(sym), c / 2, c + k / 2], f'{ex(sym)} × {k} = {ex(c)}.', fmtf=ex)


@t43.add('C2', (2, 3, 4), 'explain')
def t43_err(r, D):
    nm = person(r)
    tot, f = pie_data(r, 3)
    if not tot:
        return None
    ctx, cats = r.choice(PIE_CTX)
    i = r.randrange(len(f))
    wrong = f[i] * 360 // 100 if f[i] * 360 % 100 == 0 else round(f[i] * 3.6)
    return Q(f'A survey of {tot} people records the {ctx}; {f[i]} chose {cats[i]}. {nm} draws a pie chart and uses an angle of {wrong}° for {cats[i]}, by working out {f[i]} × 3.6. Explain the mistake and find the correct angle.',
             f'Multiplying by 3.6 only works when the total is 100. Each person is 360 ÷ {tot} = {ex(360 / tot)}°, so the angle is {f[i]} × {ex(360 / tot)} = {f[i] * 360 // tot}°.',
             f'B1 total is {tot}, not 100; B1 {f[i] * 360 // tot}° [2]')


def t43_c4(r, D):
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    base = r.randint(18, 26)
    temps = [base + r.randint(-4, 6) for _ in days]
    c = city(r)
    tbl = ', '.join(f'{d} {t} °C' for d, t in zip(days, temps))
    rises = [(temps[i + 1] - temps[i], days[i], days[i + 1]) for i in range(6)]
    best = max(rises)
    intro = f'The maximum daily temperatures in {c} for one week were: {tbl}. The data are to be shown on a line graph.'
    parts = [
        P('State which variable goes on the horizontal axis and explain why.', 'The day (time), because it is the independent variable and line graphs show change over time.', 'B1 day; B1 reason', 2),
        P('Find the largest increase from one day to the next, and say between which days it happened.', f'{best[0]} °C, from {best[1]} to {best[2]}', f'M1 differences; A1 {best[0]} °C {best[1]}–{best[2]}', 2),
        P('Calculate the mean maximum temperature for the week, correct to 1 decimal place.', f'{ex(round(sum(temps) / 7, 1))} °C', f'M1 {sum(temps)} ÷ 7; A1 {ex(round(sum(temps) / 7, 1))}', 2),
        P('Explain why a line graph is more suitable than a pie chart for these data.', 'The data show change over time; a pie chart shows parts of a whole, and the temperatures are not parts of a total.', 'B1 change over time; B1 not parts of a whole', 2),
    ]
    return cmp_(r, intro, parts)


t43.add('C4', (2, 3, 4, 5))(t43_c4)

# ---------------------------------------------------------------- stem-and-leaf
t44 = topic('Stem-and-leaf diagrams and choosing an appropriate display', 'stem-and-leaf diagrams and choosing an appropriate display', 'stem-and-leaf', 'appropriate display')
t44.fixed('C1', (1, 2), [
    ('In a stem-and-leaf diagram with key 3 | 4 = 34, what value does 5 | 7 represent?', '57', 'Stem 5 (tens), leaf 7 (units).', ['5.7', '75', '12']),
    ('Why must a stem-and-leaf diagram have a key?', 'To show what the stems and leaves represent', 'For example 3 | 4 could mean 34 or 3.4.', ['To show the mode', 'To make it look neat', 'To count the data']),
    ('In a stem-and-leaf diagram, the leaves in each row should be', 'in order from smallest to largest', 'An ordered diagram makes the median easy to find.', ['in the order collected', 'in descending order of stems', 'added together']),
    ('Which display keeps all the original data values?', 'A stem-and-leaf diagram', 'Every value is shown as a stem and leaf.', ['A pie chart', 'A grouped frequency table', 'A bar chart of grouped data']),
    ('Which display is most suitable to compare the test marks of two classes while keeping every mark?', 'A back-to-back stem-and-leaf diagram', 'The two sets share stems and all values are kept.', ['Two pie charts', 'A pictogram', 'A line graph']),
])
t44.fixed('C2', (2, 3), [
    ('Explain one advantage of a stem-and-leaf diagram over a grouped frequency table.', 'It keeps the original data values, so the median, mode and range can be found exactly, while still showing the shape of the distribution.', 'B1 keeps raw data; B1 exact statistics/shape [2]'),
    ('Explain why a stem-and-leaf diagram is not suitable for showing the favourite colours of a class.', 'Favourite colour is qualitative data, which has no numerical values to split into stems and leaves.', 'B1 qualitative; B1 needs numerical data [2]'),
    ('Explain how to find the median from an ordered stem-and-leaf diagram with 25 values.', 'The median is the 13th value ((25 + 1) ÷ 2); count along the leaves from the smallest value to the 13th.', 'B1 13th value; B1 count from the smallest [2]'),
])


def stem_data(r, D, n=None):
    n = n or (r.randint(11, 15) if D <= 2 else r.randint(15, 21))
    lo = r.choice([1, 2, 3, 4])
    vals = sorted(r.randint(lo * 10, lo * 10 + 39) for _ in range(n))
    return vals


def stem_text(vals, key_unit=''):
    rows = {}
    for v in vals:
        rows.setdefault(v // 10, []).append(v % 10)
    lo, hi = min(rows), max(rows)
    out = ' ; '.join(f'{s} | {" ".join(map(str, rows.get(s, [])))}' for s in range(lo, hi + 1))
    return out


@t44.add('C3', (1, 2, 3, 4, 5))
def t44_read(r, D):
    vals = stem_data(r, D)
    what, unit = r.choice([('masses of parcels', 'kg'), ('ages of people at a concert', 'years'), ('test marks', 'marks'), ('times taken to finish a puzzle', 'seconds'), ('heights of seedlings', 'mm')])
    k = vals[0] // 10
    txt = stem_text(vals)
    stem = f'The stem-and-leaf diagram shows the {what} ({unit}): {txt} (key: {k} | 3 = {k}3 {unit}).'
    md, cnt = modes(vals)
    med = median(vals)
    rng = vals[-1] - vals[0]
    if D <= 2:
        return Q(stem + ' Find the range and the median.', f'range {rng} {unit}; median {ex(med)} {unit}', f'B1 range {vals[-1]} − {vals[0]} = {rng}; M1 ({len(vals)} + 1) ÷ 2 = {ex((len(vals) + 1) / 2)}th value; A1 median {ex(med)} [3]')
    if D == 3:
        a = ' or '.join(map(str, sorted(md))) if cnt > 1 else 'no single mode'
        return Q(stem + ' Find the number of values, the median and the mode.', f'{len(vals)} values; median {ex(med)}; mode {a}', f'B1 n = {len(vals)}; B1 median {ex(med)}; B1 mode {a} [3]')
    t = r.choice(vals[len(vals) // 3: 2 * len(vals) // 3])
    more = sum(1 for v in vals if v > t)
    return Q(stem + f' Find the median, the range and the percentage of values greater than {t} {unit}.', f'median {ex(med)}; range {rng}; {n3(100 * more / len(vals))}%',
             f'B1 median {ex(med)}; B1 range {rng}; M1 {more}/{len(vals)} × 100; A1 {n3(100 * more / len(vals))}% [4]')


@t44.add('C1', (1, 2, 3))
def t44_choose(r, D):
    sit, best, why = r.choice([
        ('showing how the population of a town changed every year from 2010 to 2024', 'line graph', 'it shows change over time'),
        ('showing what proportion of a budget is spent on each department', 'pie chart', 'it shows parts of a whole'),
        ('showing the exact marks of 30 students so that the median can be found', 'stem-and-leaf diagram', 'it keeps every value in order'),
        ('comparing the number of students choosing each of five sports', 'bar chart', 'it compares frequencies of categories'),
        ('showing the number of books sold each month with a picture of a book for every 10 books', 'pictogram', 'symbols represent a fixed number of items'),
    ])
    opts, ans = mcq(r, best, [x for x in ['line graph', 'pie chart', 'stem-and-leaf diagram', 'bar chart', 'pictogram'] if x != best])
    return {'stem': f'Which is the most appropriate display for {sit}?', 'options': opts, 'answer': ans, 'key': f'A {best}, because {why}.'}


@t44.add('C2', (2, 3, 4), 'explain')
def t44_err(r, D):
    nm = person(r)
    vals = stem_data(r, 2, n=r.choice([11, 13, 15]))
    unord = vals[:]
    r.shuffle(unord)
    txt = stem_text(vals)
    k = vals[0] // 10
    wrongmed = unord[len(unord) // 2]
    med = median(vals)
    if wrongmed == med:
        return None
    return Q(f'{nm} records these values: {", ".join(map(str, unord))}. {nm} says the median is {wrongmed} because it is the middle value of the list. Explain the error and use an ordered stem-and-leaf diagram to find the correct median.',
             f'The values must be put in order first. Ordered diagram: {txt} (key {k} | 3 = {k}3). The median is the {(len(vals) + 1) // 2}th value, {ex(med)}.',
             f'B1 data not ordered; B1 ordered diagram; B1 median {ex(med)} [3]')


def t44_c4(r, D):
    a, b = two_people(r)
    va = stem_data(r, 3, n=r.choice([13, 15]))
    vb = sorted(min(99, v + r.randint(-6, 12)) for v in stem_data(r, 3, n=len(va)))
    ma, mb = median(va), median(vb)
    ra, rb = va[-1] - va[0], vb[-1] - vb[0]
    what = r.choice(['scores in a quiz (out of 80)', 'times in seconds to complete an obstacle course', 'numbers of push-ups in one minute'])
    intro = f'{a}\'s class and {b}\'s class each recorded their {what}. {a}\'s class: {stem_text(va)}. {b}\'s class: {stem_text(vb)}. Key for both: 3 | 4 = 34.'
    parts = [
        P(f'Find the median for each class.', f'{a}: {ex(ma)}; {b}: {ex(mb)}', f'B1 {ex(ma)}; B1 {ex(mb)}', 2),
        P('Find the range for each class.', f'{a}: {ra}; {b}: {rb}', f'B1 {ra}; B1 {rb}', 2),
        P('Compare the two distributions.', f'{"" if ma == mb else (a if ma > mb else b) + "’s class has the higher median, so generally higher values; "}{((a if ra < rb else b) + "’s class") if ra != rb else "Both classes"} {"has" if ra != rb else "have"} the {"smaller" if ra != rb else "same"} range, so {"its values are more consistent" if ra != rb else "similar spread"}.',
          'B1 compares averages in context; B1 compares spread in context', 2),
        P('Name a display that would show both sets of data on one diagram while keeping every value.', 'A back-to-back stem-and-leaf diagram', 'B1 back-to-back stem-and-leaf diagram', 1),
    ]
    return cmp_(r, intro, parts)


t44.add('C4', (2, 3, 4, 5))(t44_c4)
CHAPTERS[4] = [t41, t42, t43, t44]


# =========================================================== 5 Fractions, percentages and standard form
def mixed(x):
    return ff(x)


def rfrac(r, D):
    d = r.choice([3, 4, 5, 6, 7, 8, 9, 10, 12])
    n = r.randint(1, d - 1)
    w = r.randint(1, 4) if D >= 3 else 0
    return Fr(n, d) + w


t51 = topic('Operations with fractions and mixed numbers', 'operations with fractions and mixed numbers', 'fractions', 'mixed numbers')
t51.fixed('C1', (1, 2), [
    ('Write 2 3/5 as an improper fraction.', '13/5', '2 × 5 + 3 = 13, so 13/5.', ['23/5', '6/5', '10/5']),
    ('Simplify 18/24.', '3/4', 'Divide numerator and denominator by 6.', ['9/12', '2/3', '6/8']),
    ('Work out 2/3 of 45.', '30', '45 ÷ 3 × 2 = 30.', ['15', '67.5', '22.5']),
    ('Which fraction is equivalent to 0.375?', '3/8', '375/1000 = 3/8.', ['3/75', '37/100', '3/5']),
    ('What is 1/4 + 1/3?', '7/12', '3/12 + 4/12 = 7/12.', ['2/7', '1/7', '2/12']),
    ('To divide by a fraction, you', 'multiply by its reciprocal', 'a ÷ b/c = a × c/b.', ['divide the numerators only', 'multiply by the fraction', 'subtract the denominators']),
    ('Which of these fractions is the largest?', '5/8', '5/8 = 0.625, 3/5 = 0.6, 4/7 ≈ 0.571, 7/12 ≈ 0.583.', ['3/5', '4/7', '7/12']),
])
t51.fixed('C2', (2, 3), [
    ('Explain why 1/3 + 1/4 is not equal to 2/7.', 'Fractions can only be added when the denominators are the same: 1/3 + 1/4 = 4/12 + 3/12 = 7/12. Adding numerators and denominators separately is not valid.', 'B1 common denominator needed; B1 7/12 [2]'),
    ('Explain why dividing by 1/2 gives a larger answer than the starting number.', 'Dividing by 1/2 asks how many halves fit into the number, which is twice the number (the same as multiplying by 2).', 'B1 how many halves; B1 equivalent to × 2 [2]'),
    ('Explain why you should change mixed numbers to improper fractions before multiplying them.', 'Multiplying the whole parts and the fraction parts separately misses the cross terms; e.g. 1½ × 1½ = 9/4 = 2¼, not 1¼.', 'B1 cannot multiply parts separately; B1 example or reason [2]'),
])


def fop(a, b, op):
    return {'+': a + b, '−': a - b, '×': a * b, '÷': a / b}[op]


@t51.add('C1', (1, 2, 3))
def t51_op(r, D):
    a, b = rfrac(r, D), rfrac(r, D)
    op = r.choice(['+', '−'] if D == 1 else ['+', '−', '×', '÷'])
    if op == '−' and a < b:
        a, b = b, a
    if a == b:
        return None
    c = fop(a, b, op)
    wrong = [Fr(a.numerator + b.numerator, a.denominator + b.denominator), fop(a, b, '×' if op == '÷' else ('÷' if op == '×' else ('−' if op == '+' else '+'))), c + Fr(1, max(2, c.denominator)), c * 2, Fr(a.numerator * b.denominator, b.numerator * a.denominator) if op != '÷' else a * b]
    return MC(r, f'Work out {mixed(a)} {op} {mixed(b)}, giving your answer in its simplest form.', c, wrong, f'{"Use a common denominator" if op in "+−" else ("Multiply numerators and denominators" if op == "×" else "Multiply by the reciprocal")}: {mixed(a)} {op} {mixed(b)} = {mixed(c)}.', fmtf=mixed)


@t51.add('C3', (1, 2, 3, 4, 5))
def t51_calc(r, D):
    a, b = rfrac(r, max(D, 3)), rfrac(r, max(D, 3))
    if a.denominator == b.denominator:
        return None
    op = r.choice(['+', '−', '×', '÷'])
    if op == '−' and a < b:
        a, b = b, a
    if a == b:
        return None
    c = fop(a, b, op)
    if D <= 3:
        ia, ib = f'{a.numerator}/{a.denominator}', f'{b.numerator}/{b.denominator}'
        steps = {'+': f'common denominator {a.denominator * b.denominator // math.gcd(a.denominator, b.denominator)}', '−': f'common denominator {a.denominator * b.denominator // math.gcd(a.denominator, b.denominator)}',
                 '×': f'{ia} × {ib}', '÷': f'{ia} × {b.denominator}/{b.numerator}'}[op]
        return Q(f'Without using a calculator, work out {mixed(a)} {op} {mixed(b)}. Show all your working and give your answer as a mixed number in its simplest form.', mixed(c),
                 f'B1 improper fractions {ia} and {ib}; M1 {steps}; A1 {mixed(c)} [3]')
    e = rfrac(r, 2)
    op2 = r.choice(['+', '−'])
    tot = fop(c, e, op2)
    if tot <= 0:
        return None
    return Q(f'Without using a calculator, work out ({mixed(a)} {op} {mixed(b)}) {op2} {mixed(e)}, giving your answer in its simplest form.', mixed(tot),
             f'M1 {mixed(a)} {op} {mixed(b)} = {mixed(c)}; M1 common denominator for {op2} {mixed(e)}; A1 {mixed(tot)} [3]')


@t51.add('C3', (2, 3, 4, 5))
def t51_ctx(r, D):
    nm = person(r)
    tot = r.choice([120, 180, 240, 360, 480, 600, 720])
    f1, f2 = r.choice([(Fr(1, 3), Fr(1, 4)), (Fr(2, 5), Fr(1, 3)), (Fr(1, 4), Fr(2, 3)), (Fr(3, 8), Fr(1, 5)), (Fr(1, 6), Fr(3, 5)), (Fr(2, 3), Fr(1, 4))])
    s1 = tot * f1
    rem = tot - s1
    s2 = rem * f2
    left = rem - s2
    if s1.denominator != 1 or s2.denominator != 1:
        return None
    what = r.choice(['dollars of birthday money', 'minutes of free time', 'kilograms of rice', 'litres of fuel'])
    a1, a2 = r.choice([('spends', 'saves'), ('uses', 'gives away'), ('sells', 'stores')])
    if D <= 3:
        return Q(f'{nm} has {tot} {what}. {nm} {a1} {num(f1)} of it and {a2} {num(f2)} of what is left. How much remains?', f'{num(int(left))}',
                 f'M1 {num(f1)} × {tot} = {num(int(s1))}; M1 {num(f2)} × {num(int(rem))} = {num(int(s2))}; A1 {num(int(left))} [3]')
    return Q(f'{nm} {a1} {num(f1)} of some {what.split(" of ")[-1] if " of " in what else what} and then {a2} {num(f2)} of the remainder. {nm} is left with {num(int(left))} {what}. How many {what} did {nm} start with?', str(tot),
             f'M1 fraction left = (1 − {num(f1)})(1 − {num(f2)}) = {num((1 - f1) * (1 - f2))}; M1 {num(int(left))} ÷ {num((1 - f1) * (1 - f2))}; A1 {tot} [3]')


@t51.add('C2', (2, 3, 4), 'explain')
def t51_err(r, D):
    nm = person(r)
    a, b = rfrac(r, 2), rfrac(r, 2)
    case = r.choice(['add', 'div', 'mixed'])
    if case == 'add':
        w = Fr(a.numerator + b.numerator, a.denominator + b.denominator)
        if a.denominator == b.denominator:
            return None
        return Q(f'{nm} writes {num(a)} + {num(b)} = {a.numerator + b.numerator}/{a.denominator + b.denominator}. Explain the mistake and find the correct answer.', f'{nm} added the denominators. Use a common denominator: {num(a)} + {num(b)} = {mixed(a + b)}.',
                 f'B1 cannot add denominators; B1 {mixed(a + b)} [2]')
    if case == 'div':
        return Q(f'{nm} works out {num(a)} ÷ {num(b)} by inverting the first fraction: {a.denominator}/{a.numerator} × {num(b)}. Explain the error and find the correct answer.', f'It is the divisor (the second fraction) that is inverted: {num(a)} × {b.denominator}/{b.numerator} = {mixed(a / b)}.',
                 f'B1 invert the second fraction; B1 {mixed(a / b)} [2]')
    w1, w2 = r.randint(1, 3), r.randint(1, 3)
    x, y = Fr(1, r.choice([2, 3, 4])), Fr(1, r.choice([2, 3, 5]))
    wrong = w1 * w2 + x * y
    right = (w1 + x) * (w2 + y)
    return Q(f'{nm} works out {mixed(w1 + x)} × {mixed(w2 + y)} by multiplying the whole numbers and the fractions separately to get {mixed(wrong)}. Explain why this is wrong and find the correct answer.',
             f'This misses the products of the whole numbers with the fractions. Convert to improper fractions: {num(w1 + x)} × {num(w2 + y)} = {mixed(right)}.', f'B1 explanation; B1 {mixed(right)} [2]')


def t51_c4(r, D):
    nm = person(r)
    L = r.choice([Fr(9, 2), Fr(21, 4), Fr(15, 2), Fr(25, 4), Fr(27, 4), Fr(23, 4), Fr(31, 4)])
    p = r.choice([Fr(3, 4), Fr(5, 8), Fr(2, 3), Fr(3, 8), Fr(5, 6)])
    if (L / p).denominator == 1:
        return None
    n = int(L / p)
    left = L - n * p
    intro = f'{nm} has a plank of wood {mixed(L)} m long for a shelf unit in a workshop in {city(r)}. Each shelf needs a piece {num(p)} m long.'
    a2 = r.choice([Fr(1, 3), Fr(2, 3), Fr(1, 4), Fr(3, 4), Fr(2, 5)])
    parts = [
        P('Find the greatest number of shelves that can be cut from the plank.', str(n), f'M1 {mixed(L)} ÷ {num(p)} = {mixed(L / p)}; A1 {n}', 2),
        P('Find the length of wood left over after cutting as many shelves as possible, as a fraction of a metre.', f'{num(left)} m', f'M1 {mixed(L)} − {n} × {num(p)}; A1 {num(left)}', 2),
        P(f'{nm} cuts as many shelves as possible and paints {num(a2)} of the length of each one. Find the total length of shelf that is painted.', f'{mixed(n * p * a2)} m', f'M1 {n} × {num(p)} × {num(a2)}; A1 {mixed(n * p * a2)}', 2),
        P(f'When as many shelves as possible are cut, what fraction of the original plank is used for shelves?', num(n * p / L), f'M1 {mixed(n * p)} ÷ {mixed(L)}; A1 {num(n * p / L)}', 2),
    ]
    return cmp_(r, intro, parts)


t51.add('C4', (2, 3, 4, 5))(t51_c4)

# ---------------------------------------------------------------- percentages
t52 = topic('Percentages: percentage of a quantity, percentage change and reverse percentages', 'percentages: percentage of a quantity, percentage change and reverse percentages', 'percentage change', 'reverse percentages')
t52.fixed('C1', (1, 2), [
    ('What is 15% of 80?', '12', '0.15 × 80 = 12.', ['15', '8', '5.33']),
    ('Which multiplier increases an amount by 7%?', '1.07', '100% + 7% = 107% = 1.07.', ['0.07', '1.7', '0.93']),
    ('Which multiplier decreases an amount by 12%?', '0.88', '100% − 12% = 88% = 0.88.', ['0.12', '1.12', '0.8']),
    ('Write 3/8 as a percentage.', '37.5%', '3 ÷ 8 = 0.375 = 37.5%.', ['38%', '3.8%', '0.375%']),
    ('A price rises from $40 to $50. What is the percentage increase?', '25%', 'Increase 10, 10/40 × 100 = 25%.', ['20%', '10%', '125%']),
    ('Write 0.035 as a percentage.', '3.5%', '0.035 × 100 = 3.5%.', ['35%', '0.35%', '350%']),
])
t52.fixed('C2', (2, 3), [
    ('Explain why a 10% increase followed by a 10% decrease does not return a price to its original value.', 'The decrease is 10% of the larger, increased price, so more is taken off than was added: × 1.1 × 0.9 = × 0.99, a 1% decrease overall.', 'B1 second percentage is of a different amount; B1 overall multiplier 0.99 [2]'),
    ('Explain how to find the original price before a 20% increase, given the new price.', 'The new price is 120% of the original, so divide the new price by 1.2 (not take off 20% of the new price).', 'B1 new price = 120%; B1 divide by 1.2 [2]'),
    ('Explain why the percentage change should be calculated using the original value as the denominator.', 'Percentage change compares the change with what you started with; using the new value would measure the change relative to the wrong amount.', 'B1 compares with original; B1 reason [2]'),
])


@t52.add('C1', (1, 2, 3))
def t52_of(r, D):
    p = r.choice([5, 10, 15, 20, 25, 30, 40, 60, 75] if D <= 2 else [12.5, 17.5, 2.5, 35, 4, 8, 65])
    q = r.choice([20, 40, 60, 80, 120, 160, 240, 360, 480])
    c = p * q / 100
    return MC(r, f'Find {ex(p)}% of {q}.', c, [q / p if p else 1, c * 10, c / 10, q - c, p * q / 10], f'{ex(p)}/100 × {q} = {ex(c)}.', fmtf=lambda v: ex(round(v, 2)))


@t52.add('C3', (1, 2, 3, 4, 5))
def t52_change(r, D):
    nm = person(r)
    cur = r.choice(['$', '€', '£'])
    case = r.choice(['inc', 'dec', 'pct', 'rev'] if D >= 3 else ['inc', 'dec', 'pct'])
    item = r.choice(['laptop', 'bicycle', 'phone', 'sofa', 'concert ticket', 'train pass', 'camera'])
    if case in ('inc', 'dec'):
        P0 = r.choice([45, 80, 120, 250, 360, 480, 640, 850, 1200])
        p = r.choice([5, 8, 12, 15, 20, 25, 30, 35])
        m = 1 + p / 100 if case == 'inc' else 1 - p / 100
        new = P0 * m
        word = 'increased' if case == 'inc' else 'reduced in a sale'
        return Q(f'The price of a {item} was {cur}{P0}. It is {word} by {p}%. Find the new price.', money(new, cur), f'M1 {P0} × {ex(m)} (or {P0} {"+" if case == "inc" else "−"} {ex(P0 * p / 100)}); A1 {money(new, cur)} [2]')
    if case == 'pct':
        a = r.choice([40, 50, 64, 80, 125, 160, 250, 320])
        b = a + r.choice([-1, 1]) * r.choice([2, 4, 5, 8, 10, 16, 20, 25])
        pc = (b - a) / a * 100
        word = 'increase' if b > a else 'decrease'
        thing = r.choice([('The number of members of a club', ''), ('The mass of a puppy', ' kg'), ('A monthly phone bill', ''), ('The population of a village', '')])
        val = (lambda v: f'{cur}{v}') if thing[0].startswith('A monthly') else (lambda v: f'{v}{thing[1]}')
        return Q(f'{thing[0]} changed from {val(a)} to {val(b)}. Calculate the percentage {word}.', f'{nn(abs(pc))}%', f'M1 {abs(b - a)} ÷ {a} × 100; A1 {nn(abs(pc))}% [2]')
    p = r.choice([10, 15, 20, 25, 30, 40])
    orig = r.choice([60, 80, 120, 160, 240, 320, 400, 480])
    up = r.random() < 0.5
    new = orig * (1 + p / 100) if up else orig * (1 - p / 100)
    m = 1 + p / 100 if up else 1 - p / 100
    st = f'After a {p}% {"increase" if up else "discount"}, the price of a {item} is {money(new, cur)}. Find the price before the {"increase" if up else "discount"}.'
    key = f'M1 {money(new, cur)} = {ex(m * 100)}% of the original; M1 {ex(new)} ÷ {ex(m)}; A1 {money(orig, cur)} [3]'
    if D >= 5:
        p2 = r.choice([5, 10])
        new2 = new * (1 + p2 / 100)
        st = f'The price of a {item} is {"increased by " + str(p) + "% and then by a further " if up else "reduced by " + str(p) + "% in a sale and then increased by "}{p2}%. The final price is {money(new2, cur)}. Find the original price.'
        key = f'M1 overall multiplier {ex(m)} × {ex(1 + p2 / 100)} = {ex(round(m * (1 + p2 / 100), 4))}; M1 {ex(round(new2, 2))} ÷ {ex(round(m * (1 + p2 / 100), 4))}; A1 {money(orig, cur)} [3]'
    return Q(st, money(orig, cur), key)


@t52.add('C2', (2, 3, 4), 'explain')
def t52_err(r, D):
    nm = person(r)
    p = r.choice([10, 20, 25, 15, 30])
    orig = r.choice([80, 120, 200, 240, 400])
    new = orig * (100 - p) // 100
    wrong = new * (100 + p) / 100
    case = r.choice(['rev', 'pct'])
    if case == 'rev':
        return Q(f'A coat costs ${new} after a {p}% discount. {nm} finds the original price by adding {p}% of ${new}, getting {money(wrong)}. Explain the mistake and find the original price.',
                 f'The {p}% discount was of the original price, not of ${new}. ${new} is {100 - p}% of the original, so original = {new} ÷ {ex((100 - p) / 100)} = ${orig}.', f'B1 percentage of the original, not the new price; B1 ${orig} [2]')
    a, b = r.choice([(40, 50), (80, 100), (60, 75), (120, 150), (200, 250)])
    return Q(f'A salary rises from ${a * 100} to ${b * 100}. {nm} says the percentage increase is {ex((b - a) / b * 100)}% because {b - a}00 ÷ {b}00 × 100 = {ex((b - a) / b * 100)}. Explain the mistake and find the correct percentage increase.',
             f'{nm} divided by the new salary. Use the original: {b - a}00 ÷ {a}00 × 100 = {ex((b - a) / a * 100)}%.', f'B1 must divide by the original; B1 {ex((b - a) / a * 100)}% [2]')


def t52_c4(r, D):
    nm = person(r)
    cur = r.choice(['$', '€'])
    cost = r.choice([200, 250, 320, 400, 480, 600])
    mark = r.choice([20, 25, 30, 40, 50])
    sell = cost * (1 + mark / 100)
    disc = r.choice([10, 15, 20, 25])
    sale = sell * (1 - disc / 100)
    profit = sale - cost
    intro = f'A shop in {city(r)} buys a television for {cur}{cost}. It marks up the price by {mark}% to set the selling price.'
    parts = [
        P('Find the selling price.', money(sell, cur), f'M1 {cost} × {ex(1 + mark / 100)}; A1 {money(sell, cur)}', 2),
        P(f'In a sale, the selling price is reduced by {disc}%. Find the sale price.', money(sale, cur), f'M1 {ex(sell)} × {ex(1 - disc / 100)}; A1 {money(sale, cur)}', 2),
        P('Find the percentage profit the shop makes when it sells the television at the sale price, based on what it paid.', f'{nn(profit / cost * 100)}%', f'M1 {ex(round(profit, 2))} ÷ {cost} × 100; A1 {nn(profit / cost * 100)}%', 2),
        P(f'{nm} says the overall change from the cost price is {mark - disc}%. Explain why {nm} is wrong.', f'The {disc}% is taken off the larger, marked-up price, so the overall multiplier is {ex(1 + mark / 100)} × {ex(1 - disc / 100)} = {ex(round((1 + mark / 100) * (1 - disc / 100), 4))}, a change of {nn(((1 + mark / 100) * (1 - disc / 100) - 1) * 100)}%.',
          'B1 percentages of different amounts; B1 correct overall change', 2),
        P(f'Another television has a sale price of {money(sell * (1 - disc / 100), cur)} after the same {disc}% reduction. Find its price before the sale.', money(sell, cur), f'M1 ÷ {ex(1 - disc / 100)}; A1 {money(sell, cur)}', 2),
    ]
    return cmp_(r, intro, parts)


t52.add('C4', (2, 3, 4, 5))(t52_c4)

# ---------------------------------------------------------------- standard form
def stdf(m, e):
    return f'{ex(m)} × 10{sup(e)}'


def to_std(x, n=4):
    if x == 0:
        return '0'
    e = int(math.floor(math.log10(abs(x))))
    m = round(x / 10 ** e, n - 1)
    if abs(m) >= 10:
        m /= 10
        e += 1
    return stdf(float(f'{m:.{n}g}'), e)


t53 = topic('Standard form: calculating with numbers in standard form', 'standard form: calculating with numbers in standard form', 'standard form', 'scientific notation')
t53.fixed('C1', (1, 2), [
    ('Write 45 000 in standard form.', '4.5 × 10⁴', '45 000 = 4.5 × 10 000.', ['45 × 10³', '4.5 × 10³', '0.45 × 10⁵']),
    ('Write 0.0062 in standard form.', '6.2 × 10⁻³', 'Move the decimal point 3 places right.', ['6.2 × 10³', '62 × 10⁻⁴', '6.2 × 10⁻²']),
    ('Which of these is written correctly in standard form?', '3.08 × 10⁷', 'The first number must be at least 1 and less than 10.', ['30.8 × 10⁶', '0.308 × 10⁸', '3.08 × 7¹⁰']),
    ('Write 7.1 × 10⁵ as an ordinary number.', '710 000', 'Multiply 7.1 by 100 000.', ['71 000', '7 100 000', '0.000071']),
    ('Write 2.4 × 10⁻⁴ as an ordinary number.', '0.00024', 'Divide 2.4 by 10 000.', ['0.0024', '24 000', '0.000024']),
    ('Which number is the largest?', '1.2 × 10⁵', 'Compare powers first: 10⁵ is the largest power.', ['9.8 × 10⁴', '99 × 10³', '1.2 × 10⁻⁵']),
])
t53.fixed('C2', (2, 3), [
    ('Explain why 25 × 10⁴ is not in standard form, and write it correctly.', 'The first number must be between 1 and 10; 25 × 10⁴ = 2.5 × 10⁵.', 'B1 25 not between 1 and 10; B1 2.5 × 10⁵ [2]'),
    ('Explain why you cannot simply add the powers when adding 3 × 10⁴ and 2 × 10³.', 'Adding is not multiplying; write both with the same power: 30 000 + 2000 = 32 000 = 3.2 × 10⁴.', 'B1 index laws apply to multiplication; B1 3.2 × 10⁴ [2]'),
    ('Explain how to tell, without converting, which of 4.7 × 10⁻³ and 3.9 × 10⁻² is larger.', '10⁻² = 0.01 is larger than 10⁻³ = 0.001, so 3.9 × 10⁻² is larger; the power matters more than the first number.', 'B1 compare powers; B1 3.9 × 10⁻² larger [2]'),
])


@t53.add('C1', (1, 2, 3))
def t53_conv(r, D):
    m = r.choice([1.2, 2.5, 3.07, 4.8, 5.06, 6.3, 7.25, 8.4, 9.1])
    e = r.choice([3, 4, 5, 6, 7]) if D <= 2 else r.choice([-2, -3, -4, -5, -6])
    x = m * 10 ** e
    ordn = ex(x, 9) if e < 0 else f'{round(x):,}'.replace(',', ' ')
    c = stdf(m, e)
    ds = [stdf(m, e + 1), stdf(m, e - 1), f'{ex(m * 10)} × 10{sup(e - 1)}', stdf(m, -e)]
    return SMC(r, f'Write {ordn} in standard form.', c, ds, f'{ordn} = {ex(m)} × 10{sup(e)} (1 ≤ {ex(m)} < 10).')


@t53.add('C3', (1, 2, 3, 4, 5))
def t53_calc(r, D):
    a, e1 = r.choice([1.5, 2, 2.4, 3, 3.6, 4, 4.5, 6, 7.2, 8]), r.randint(-6, 9)
    b, e2 = r.choice([1.2, 2, 2.5, 3, 4, 5, 6]), r.randint(-5, 8)
    op = r.choice(['×', '÷'] if D <= 3 else ['×', '÷', '+', '−'])
    if op == '×':
        v = a * b * 10 ** (e1 + e2)
    elif op == '÷':
        v = a / b * 10 ** (e1 - e2)
    elif op == '+':
        e2 = e1 - r.choice([1, 2])
        v = a * 10 ** e1 + b * 10 ** e2
    else:
        e2 = e1 - r.choice([1, 2])
        v = a * 10 ** e1 - b * 10 ** e2
    ans = to_std(v)
    calc = 'Without using a calculator, work' if D <= 3 else 'Work'
    return Q(f'{calc} out ({stdf(a, e1)}) {op} ({stdf(b, e2)}), giving your answer in standard form.', ans,
             f'M1 {"multiply" if op == "×" else ("divide" if op == "÷" else "same power of 10")} the numbers and {"add" if op == "×" else ("subtract" if op == "÷" else "align")} the indices; A1 {ans} [2]')


CONTEXTS_SF = [('The distance from the Earth to the Sun is about 1.5 × 10⁸ km. Light travels at about 3 × 10⁵ km per second.', 1.5e8 / 3e5, 'seconds for light to travel from the Sun to the Earth', 'M1 1.5 × 10⁸ ÷ 3 × 10⁵'),
               ('The mass of one grain of sand is about 6.7 × 10⁻⁴ g.', 6.7e-4 * 1e6, 'grams for one million (10⁶) grains', 'M1 6.7 × 10⁻⁴ × 10⁶'),
               ('A red blood cell has a diameter of about 7.5 × 10⁻⁶ m.', 7.5e-6 * 4e3, 'metres for 4000 cells placed in a line', 'M1 7.5 × 10⁻⁶ × 4 × 10³'),
               ('The population of a country is 5.6 × 10⁷ and the total area is 2.8 × 10⁵ km².', 5.6e7 / 2.8e5, 'people per km² (population density)', 'M1 5.6 × 10⁷ ÷ 2.8 × 10⁵'),
               ('A computer performs 2.4 × 10⁹ operations each second.', 2.4e9 * 3600, 'operations in one hour', 'M1 2.4 × 10⁹ × 3600'),
               ('The mass of the Earth is 5.97 × 10²⁴ kg and the mass of the Moon is 7.35 × 10²² kg.', 5.97e24 / 7.35e22, 'times heavier the Earth is than the Moon', 'M1 5.97 × 10²⁴ ÷ 7.35 × 10²²')]


@t53.add('C3', (2, 3, 4, 5))
def t53_ctx(r, D):
    ctx, v, q, m = r.choice(CONTEXTS_SF)
    ans = to_std(v, 3) if v >= 1e4 or v < 0.01 else n3(v)
    return Q(f'{ctx} Calculate the number of {q}. Give your answer {"in standard form" if (v >= 1e4 or v < 0.01) else "correct to 3 significant figures"}.', ans, f'{m}; A1 {ans} [2]')


@t53.add('C2', (2, 3, 4), 'explain')
def t53_err(r, D):
    nm = person(r)
    a, b = r.choice([(4, 5), (6, 3), (8, 2.5), (5, 6), (7, 4)])
    e1, e2 = r.randint(2, 6), r.randint(2, 5)
    case = r.choice(['mult', 'powers'])
    if case == 'mult':
        prod = a * b
        return Q(f'{nm} works out ({stdf(a, e1)}) × ({stdf(b, e2)}) and writes {ex(prod)} × 10{sup(e1 + e2)}. Explain why this answer is not in standard form and correct it.', f'{ex(prod)} is not between 1 and 10. {ex(prod)} × 10{sup(e1 + e2)} = {to_std(prod * 10 ** (e1 + e2))}.',
                 f'B1 first number ≥ 10; B1 {to_std(prod * 10 ** (e1 + e2))} [2]')
    return Q(f'{nm} says ({stdf(a, e1)}) × ({stdf(b, e2)}) = {ex(a * b)} × 10{sup(e1 * e2)} because "you multiply the powers". Explain the error.', f'When multiplying powers of 10 the indices are added: 10{sup(e1)} × 10{sup(e2)} = 10{sup(e1 + e2)}, so the answer is {to_std(a * b * 10 ** (e1 + e2))}.',
             f'B1 add indices when multiplying; B1 {to_std(a * b * 10 ** (e1 + e2))} [2]')


def t53_c4(r, D):
    planets = [('Mercury', 5.79e7), ('Venus', 1.08e8), ('Mars', 2.28e8), ('Jupiter', 7.79e8), ('Saturn', 1.43e9)]
    (p1, d1), (p2, d2) = r.sample(planets, 2)
    if d1 > d2:
        p1, d1, p2, d2 = p2, d2, p1, d1
    speed = r.choice([4e4, 5e4, 6e4])
    intro = f'The mean distance of {p1} from the Sun is {to_std(d1, 3)} km and the mean distance of {p2} from the Sun is {to_std(d2, 3)} km.'
    t = (d2 - d1) / speed
    parts = [
        P(f'Write the distance of {p1} from the Sun as an ordinary number.', f'{round(d1):,}'.replace(',', ' ') + ' km', f'B1 {round(d1):,} km'.replace(',', ' '), 1),
        P(f'Find the difference between the two distances, in standard form.', f'{to_std(d2 - d1, 3)} km', f'M1 {to_std(d2, 3)} − {to_std(d1, 3)}; A1 {to_std(d2 - d1, 3)}', 2),
        P(f'How many times further from the Sun is {p2} than {p1}? Give your answer to 3 significant figures.', n3(d2 / d1), f'M1 {to_std(d2, 3)} ÷ {to_std(d1, 3)}; A1 {n3(d2 / d1)}', 2),
        P(f'A probe travels in a straight line at {to_std(speed, 2)} km/h from the orbit of {p1} to the orbit of {p2} along the shortest path. Estimate the time taken in days, to 3 significant figures, assuming the planets are in line with the Sun on the same side.', f'{n3(t / 24)} days',
          f'M1 difference ÷ {to_std(speed, 2)} = {to_std(t, 3)} h; M1 ÷ 24; A1 {n3(t / 24)}', 3),
    ]
    return cmp_(r, intro, parts)


t53.add('C4', (2, 3, 4, 5))(t53_c4)

# ---------------------------------------------------------------- estimation and rounding
def rnd_dp(x, d):
    from decimal import Decimal, ROUND_HALF_UP
    q = Decimal(1).scaleb(-d)
    return str(Decimal(str(x)).quantize(q, rounding=ROUND_HALF_UP))


def rnd_sf(x, n):
    from decimal import Decimal, ROUND_HALF_UP
    d = Decimal(str(x))
    e = d.adjusted()
    q = Decimal(1).scaleb(e - n + 1)
    v = d.quantize(q, rounding=ROUND_HALF_UP)
    if e - n + 1 > 0:
        return f'{int(v):,}'.replace(',', ' ')
    return str(v)


t54 = topic('Estimation, rounding to decimal places and significant figures', 'estimation, rounding to decimal places and significant figures', 'significant figures', 'estimation rounding')
t54.fixed('C1', (1, 2), [
    ('Round 3.4762 to 2 decimal places.', '3.48', 'The third decimal digit is 6, so round up.', ['3.47', '3.5', '3.476']),
    ('Round 0.004 618 to 2 significant figures.', '0.0046', 'The first significant figure is 4; the next digit is 6 → 0.0046 (then check: 1 → stays).', ['0.0047', '0.00', '0.005']),
    ('Round 58 732 to 3 significant figures.', '58 700', 'Keep 587, next digit 3 rounds down; fill with zeros.', ['587', '58 800', '58 730']),
    ('How many significant figures does 0.0720 have?', '3', 'Leading zeros do not count; the final zero after 72 does.', ['2', '4', '5']),
    ('Estimate 49.7 × 3.08 by rounding each number to 1 significant figure.', '150', '50 × 3 = 150.', ['153', '120', '200']),
    ('Round 7.995 to 2 decimal places.', '8.00', 'The third decimal digit is 5, so 7.99 rounds up to 8.00.', ['7.99', '8.0', '7.90']),
])
t54.fixed('C2', (2, 3), [
    ('Explain why an estimate is useful even when you have a calculator.', 'It lets you check that the calculator answer is sensible and catch keying errors.', 'B1 checks reasonableness; B1 detects errors [2]'),
    ('Explain why 0.50 and 0.5 are the same number but give different information as measurements.', '0.50 is given to 2 decimal places (accurate to the nearest 0.01) while 0.5 is only to 1 decimal place; the trailing zero shows the accuracy.', 'B1 same value; B1 trailing zero shows accuracy [2]'),
    ('Explain whether the estimate 40 × 20 = 800 for 38.6 × 21.4 is an overestimate or underestimate.', 'Not certain from the rounding alone: 38.6 was rounded up and 21.4 rounded down. The exact value 826.04 shows 800 is an underestimate.', 'B1 one rounded up, one down; B1 exact value shows underestimate [2]'),
])


@t54.add('C1', (1, 2, 3))
def t54_round(r, D):
    x = r.randint(1001, 89999) / 10 ** 6 if (D >= 3 and r.random() < 0.5) else (r.randint(1, 999) * 10000 + r.randint(1, 9999)) / 10 ** 4
    if x * 10 ** 6 % 10 == 0 and x < 1 or (x > 1 and round(x * 10 ** 4) % 10 == 0):
        return None
    if r.random() < 0.5 and x > 1:
        d = r.choice([1, 2] if D == 1 else [1, 2, 3])
        c = rnd_dp(x, d)
        ds = [rnd_dp(x + 10 ** -d, d), rnd_dp(x - 10 ** -d, d) if x > 10 ** -d else rnd_dp(x, d + 1), rnd_dp(x, d + 1), rnd_dp(x, max(0, d - 1)) if d > 1 else rnd_sf(x, 2)]
        return SMC(r, f'Round {ex(x, 6)} to {d} decimal place{"s" if d > 1 else ""}.', c, ds, f'Look at the digit in the {ordinal(d + 1)} decimal place to decide whether to round up.')
    n = r.choice([1, 2, 3])
    c = rnd_sf(x, n)
    ds = [rnd_sf(x, n + 1), rnd_sf(x, n + 2), rnd_dp(x, n) if x < 1 else rnd_sf(x * 10, n), rnd_sf(x / 10, n)]
    return SMC(r, f'Round {ex(x, 6)} to {n} significant figure{"s" if n > 1 else ""}.', c, ds, f'Count {n} significant figure{"s" if n > 1 else ""} from the first non-zero digit and keep the place value: {c}.')


@t54.add('C3', (1, 2, 3, 4, 5))
def t54_est(r, D):
    a = round(r.uniform(11, 99), 1)
    b = round(r.uniform(2.1, 9.8), 2)
    c = r.choice([0.19, 0.21, 0.23, 0.48, 0.52, 0.47, 0.198, 0.213])
    ra, rb, rc = float(rnd_sf(a, 1).replace(' ', '')), float(rnd_sf(b, 1)), float(rnd_sf(c, 1))
    if D <= 2:
        est = ra * rb
        return Q(f'By rounding each number to 1 significant figure, estimate the value of {ex(a)} × {ex(b)}.', ex(est), f'M1 {ex(ra)} × {ex(rb)}; A1 {ex(est)} [2]')
    est = ra * rb / rc
    exact = a * b / c
    if D == 3:
        return Q(f'By rounding each number to 1 significant figure, estimate the value of ({ex(a)} × {ex(b)}) ÷ {ex(c)}. Show your working.', ex(round(est, 2)), f'M1 {ex(ra)} × {ex(rb)} ÷ {ex(rc)}; A1 {ex(round(est, 2))} [2]')
    return Q(f'(a) Estimate the value of ({ex(a)} × {ex(b)}) ÷ {ex(c)}, showing the values you use. (b) Use a calculator to find the exact value correct to 3 significant figures, and comment on your estimate.',
             f'(a) {ex(ra)} × {ex(rb)} ÷ {ex(rc)} = {ex(round(est, 2))} (b) {n3(exact)}; the estimate is {"an overestimate" if est > exact else "an underestimate"} but of the right order', f'(a) M1 rounded values; A1 {ex(round(est, 2))} (b) B1 {n3(exact)}; B1 comment [4]', type='multi_step')


@t54.add('C3', (2, 3, 4))
def t54_ctx(r, D):
    nm = person(r)
    n = r.randint(18, 48)
    price = round(r.uniform(2.1, 9.9), 2)
    est = float(rnd_sf(n, 1)) * float(rnd_sf(price, 1))
    item = r.choice(['notebooks', 'packs of pens', 'bottles of juice', 'tickets', 'sandwiches'])
    return Q(f'{nm} buys {n} {item} at ${ex(price)} each. Estimate the total cost by rounding each number to 1 significant figure, and decide whether ${ex(round(est * 1.6))} is enough money.',
             f'Estimate ${ex(est)}; exact ${ex(round(n * price, 2))}, so ${ex(round(est * 1.6))} is {"enough" if est * 1.6 >= n * price else "not enough"}',
             f'M1 {rnd_sf(n, 1)} × {rnd_sf(price, 1)}; A1 ${ex(est)}; B1 correct decision (exact ${ex(round(n * price, 2))}) [3]')


@t54.add('C2', (2, 3, 4), 'explain')
def t54_err(r, D):
    nm = person(r)
    x = round(r.uniform(0.001, 0.009), 5)
    case = r.choice(['sf0', 'big'])
    if case == 'sf0':
        return Q(f'{nm} rounds {ex(x, 6)} to 2 significant figures and writes 0.00. Explain the mistake and give the correct answer.', f'Leading zeros are not significant; the first significant figure is the first non-zero digit. Correct: {rnd_sf(x, 2)}.',
                 f'B1 leading zeros not significant; B1 {rnd_sf(x, 2)} [2]')
    y = r.randint(10000, 99999)
    return Q(f'{nm} rounds {f"{y:,}".replace(",", " ")} to 2 significant figures and writes {str(y)[:2]}. Explain the mistake and give the correct answer.', f'Place value must be kept by filling with zeros: {rnd_sf(y, 2)}.',
             f'B1 must keep place value; B1 {rnd_sf(y, 2)} [2]')


def t54_c4(r, D):
    r_ = round(r.uniform(3.1, 9.6), 2)
    h = round(r.uniform(10.2, 29.7), 1)
    V = math.pi * r_ * r_ * h
    rr, hr = float(rnd_sf(r_, 1)), float(rnd_sf(h, 1))
    est = 3 * rr * rr * hr
    intro = f'A cylindrical water tank in {city(r)} has radius {ex(r_)} m and height {ex(h)} m. The volume is V = πr²h.'
    parts = [
        P('Estimate the volume, using π ≈ 3 and rounding the radius and height to 1 significant figure.', f'{ex(est)} m³', f'M1 3 × {ex(rr)}² × {ex(hr)}; A1 {ex(est)}', 2),
        P('Calculate the volume, giving your answer correct to 3 significant figures.', f'{n3(V)} m³', f'M1 π × {ex(r_)}² × {ex(h)}; A1 {n3(V)}', 2),
        P('Calculate the volume, giving your answer correct to 1 decimal place.', f'{rnd_dp(round(V, 4), 1)} m³', f'M1 π × {ex(r_)}² × {ex(h)}; A1 {rnd_dp(round(V, 4), 1)}', 2),
        P(f'An estimate using π ≈ 3, r ≈ {ex(rr)} and h ≈ {ex(hr)} gives {ex(est)} m³. Explain why this estimate differs from the calculated volume, and state whether it is an overestimate or an underestimate.', f'π was rounded down to 3, the radius was rounded {"up" if rr > r_ else "down"} and the height was rounded {"up" if hr > h else "down"}; overall the estimate is {"an overestimate" if est > V else "an underestimate"}.', 'B1 identifies rounding effects; B1 over/under', 2),
    ]
    return cmp_(r, intro, parts)


t54.add('C4', (2, 3, 4, 5))(t54_c4)
CHAPTERS[5] = [t51, t52, t53, t54]


# =========================================================== 6 Equations, factors and formulae
t61 = topic('Solving linear equations including with brackets and fractions', 'solving linear equations including with brackets and fractions', 'linear equations', 'solving equations')
t61.fixed('C1', (1, 2), [
    ('Solve 3x + 7 = 22.', 'x = 5', '3x = 15, x = 5.', ['x = 29/3', 'x = 45', 'x = 15']),
    ('Solve x/4 = 9.', 'x = 36', 'Multiply both sides by 4.', ['x = 2.25', 'x = 13', 'x = 5']),
    ('Solve 5 − x = 12.', 'x = −7', '−x = 7, so x = −7.', ['x = 7', 'x = 17', 'x = −17']),
    ('What is the first step to solve 4(x − 3) = 20 most efficiently?', 'Divide both sides by 4', 'x − 3 = 5, so x = 8.', ['Add 3 to both sides', 'Subtract 4 from both sides', 'Multiply both sides by 4']),
    ('Solve 2x + 5 = x + 11.', 'x = 6', 'Subtract x and 5 from both sides: x = 6.', ['x = 16/3', 'x = 2', 'x = 5.5']),
    ('Which value of x satisfies 7x = −21?', 'x = −3', 'Divide both sides by 7.', ['x = 3', 'x = −14', 'x = −147']),
])
t61.fixed('C2', (2, 3), [
    ('Explain why you must do the same operation to both sides of an equation.', 'An equation is a balance: both sides are equal, so to keep them equal any change to one side must be made to the other.', 'B1 balance/equality; B1 same operation keeps it true [2]'),
    ('Explain how you can check a solution to an equation.', 'Substitute the value back into the original equation and check that both sides give the same number.', 'B1 substitute; B1 both sides equal [2]'),
    ('Explain why multiplying both sides of (x + 2)/3 = (x − 1)/2 by 6 is a useful first step.', '6 is the lowest common multiple of the denominators, so it clears both fractions: 2(x + 2) = 3(x − 1).', 'B1 LCM of denominators; B1 removes fractions [2]'),
])


def solve_lin(a, b, c, d):
    """ax + b = cx + d -> x"""
    if a == c:
        return None
    return Fr(d - b, a - c)


@t61.add('C1', (1, 2, 3))
def t61_basic(r, D):
    x = r.randint(-6, 12)
    a = r.randint(2, 9)
    b = r.randint(-15, 20)
    if D <= 2:
        st = f'{lin(a, b)} = {num(a * x + b)}'
        return MC(r, f'Solve {st}.', x, [x + 1, -x if x else 2, Fr(a * x + 2 * b, a), Fr(a * x + b + b, a), x * a], f'{a}x = {num(a * x + b)} {"−" if b >= 0 else "+"} {abs(b)} = {num(a * x)}, x = {num(x)}.', fmtf=lambda v: f'x = {num(v)}')
    k = r.randint(2, 5)
    c = r.randint(1, 6)
    rhs = k * (x - c)
    return MC(r, f'Solve {k}(x − {c}) = {num(rhs)}.', x, [Fr(rhs, k) - c, Fr(rhs - c, k), Fr(rhs + c, k), x + 2 * c], f'Divide by {k}: x − {c} = {num(Fr(rhs, k))}, so x = {num(x)}.', fmtf=lambda v: f'x = {num(v)}')


@t61.add('C3', (1, 2, 3, 4, 5))
def t61_solve(r, D):
    for _ in range(40):
        if D == 1:
            a, b, x = r.randint(2, 9), r.randint(-9, 15), r.randint(-5, 10)
            return Q(f'Solve {lin(a, b)} = {num(a * x + b)}.', f'x = {x}', f'M1 {a}x = {num(a * x)}; A1 x = {x} [2]')
        if D == 2:
            a, b, c = r.randint(3, 9), r.randint(-10, 10), r.randint(1, 2)
            d = r.randint(-12, 12)
            x = solve_lin(a, b, c, d)
            if x is not None and x.denominator == 1 and b and d:
                return Q(f'Solve {lin(a, b)} = {lin(c, d)}.', f'x = {num(x)}', f'M1 collects x terms: {expr((a - c, "x"))} = {num(d - b)}; A1 x = {num(x)} [2]')
        if D == 3:
            k1, k2 = r.randint(2, 5), r.randint(2, 4)
            p, q = r.randint(-6, 6), r.randint(-6, 6)
            # k1(x + p) = k2(x + q) + e
            e = r.randint(-10, 10)
            x = solve_lin(k1, k1 * p, k2, k2 * q + e)
            if x is not None and k1 != k2 and p and q and (x.denominator in (1, 2)):
                rhs = f'{k2}{lb(1, q)}' + (sgn(e) if e else '')
                return Q(f'Solve {k1}{lb(1, p)} = {rhs}.', f'x = {num(x)}', f'M1 expands both sides; M1 collects terms: {expr((k1 - k2, "x"))} = {num(k2 * q + e - k1 * p)}; A1 x = {num(x)} [3]')
        if D >= 4:
            d1, d2 = r.choice([(2, 3), (3, 4), (2, 5), (4, 3), (5, 2), (3, 5), (4, 6)])
            p, q = r.randint(-5, 7), r.randint(-5, 7)
            # (x + p)/d1 - (x + q)/d2 = rhs  or = (x)/...
            if D == 4:
                rhs = r.randint(1, 6)
                # d2(x + p) - ... use equation (x + p)/d1 = (x + q)/d2 + rhs? use form (x+p)/d1 + (x+q)/d2 = rhs
                x = Fr(rhs * d1 * d2 - d2 * p - d1 * q, d1 + d2)
                if x.denominator == 1 and p and q:
                    return Q(f'Solve ({lin(1, p)})/{d1} + ({lin(1, q)})/{d2} = {rhs}.', f'x = {num(x)}', f'M1 × {d1 * d2}: {d2}({lin(1, p)}) + {d1}({lin(1, q)}) = {rhs * d1 * d2}; M1 {d1 + d2}x = {num(rhs * d1 * d2 - d2 * p - d1 * q)}; A1 x = {num(x)} [3]')
            else:
                a2 = r.randint(2, 4)
                x = Fr(d1 * q - d2 * p, d2 - d1 * a2) if d2 != d1 * a2 else None
                # (x + p)/d1 = (a2 x + q)/d2
                if x is not None and x.denominator == 1 and p and q:
                    return Q(f'Solve ({lin(1, p)})/{d1} = ({lin(a2, q)})/{d2}.', f'x = {num(x)}', f'M1 cross-multiplies: {d2}({lin(1, p)}) = {d1}({lin(a2, q)}); M1 {expr((d2 - d1 * a2, "x"))} = {num(d1 * q - d2 * p)}; A1 x = {num(x)} [3]')
    return None


@t61.add('C2', (2, 3, 4), 'explain')
def t61_err(r, D):
    nm = person(r)
    a, b, x = r.randint(2, 7), r.randint(2, 12), r.randint(2, 9)
    case = r.choice(['order', 'sign', 'frac'])
    if case == 'order':
        rhs = a * x + b
        wrong = Fr(rhs, a) - b
        return Q(f'{nm} solves {a}x + {b} = {rhs} by dividing both sides by {a} first to get x + {b} = {num(Fr(rhs, a))}, then x = {num(wrong)}. Explain the mistake and solve the equation correctly.',
                 f'Dividing by {a} must divide every term, including {b}. Subtract {b} first: {a}x = {a * x}, so x = {x}.', f'B1 must divide all terms (or subtract first); B1 x = {x} [2]')
    if case == 'sign':
        c = r.randint(1, a - 1) if a > 2 else 1
        rhs = (a - c) * x
        return Q(f'{nm} solves {a}x = {expr((c, "x"))} + {rhs} and writes {a + c}x = {rhs}, so x = {num(Fr(rhs, a + c))}. Explain the error and find the correct solution.',
                 f'Subtracting {expr((c, "x"))} from both sides gives {expr((a - c, "x"))} = {rhs} (not adding). x = {x}.', f'B1 subtract {expr((c, "x"))} from both sides; B1 x = {x} [2]')
    d = r.choice([2, 3, 4, 5])
    q = r.randint(1, 6)
    rhs = r.randint(2, 8)
    xx = d * rhs - q
    return Q(f'{nm} solves (x + {q})/{d} = {rhs} by writing x + {q} = {rhs} ÷ {d}. Explain the mistake and find the correct solution.',
             f'To remove the division by {d} you multiply both sides by {d}: x + {q} = {d * rhs}, so x = {xx}.', f'B1 multiply (inverse of divide); B1 x = {xx} [2]')


def t61_c4(r, D):
    nm1, nm2 = two_people(r)
    a, b = r.randint(15, 40), r.randint(2, 6)
    c, d = r.randint(45, 90), r.randint(1, b - 1) if b > 2 else 1
    # savings: a + b w = c + d w -> w = (c - a)/(b - d)
    if b == d:
        return None
    w = Fr(c - a, b - d)
    if w.denominator != 1 or w <= 0:
        return None
    w = int(w)
    intro = f'{nm1} has ${a} and saves ${b} each week. {nm2} has ${c} and saves ${d} each week.'
    parts = [
        P(f'Write an expression for the amount {nm1} has after w weeks.', f'{a} + {b}w', f'B1 {a} + {b}w', 1),
        P(f'Form and solve an equation to find the number of weeks after which they have the same amount.', f'{w} weeks', f'M1 {a} + {b}w = {c} + {expr((d, "w"))}; M1 {expr((b - d, "w"))} = {c - a}; A1 w = {w}', 3),
        P('Find the amount each of them has at that time.', f'${a + b * w}', f'B1 {a} + {b} × {w} = {a + b * w}', 1),
        P(f'After how many complete weeks will {nm1} first have at least $20 more than {nm2}?', str(math.ceil(Fr(c - a + 20, b - d)) if (c - a + 20) % (b - d) else (c - a + 20) // (b - d)),
          f'M1 {a} + {b}w ≥ {c} + {expr((d, "w"))} + 20; A1 {math.ceil(Fr(c - a + 20, b - d))}', 2),
    ]
    return cmp_(r, intro, parts)


t61.add('C4', (2, 3, 4, 5))(t61_c4)

# ---------------------------------------------------------------- factorising
t62 = topic('Factorising: common factors, grouping, difference of two squares and quadratic trinomials', 'factorising: common factors, grouping, difference of two squares and quadratic trinomials', 'factorising', 'difference of two squares')
t62.fixed('C1', (1, 2), [
    ('Factorise completely 6x + 15.', '3(2x + 5)', 'HCF of 6 and 15 is 3.', ['6(x + 15)', '3(2x + 15)', '2(3x + 5)']),
    ('Factorise x² − 49.', '(x − 7)(x + 7)', 'Difference of two squares: x² − 7².', ['(x − 7)²', '(x + 7)²', 'x(x − 49)']),
    ('Factorise x² + 7x + 12.', '(x + 3)(x + 4)', '3 × 4 = 12 and 3 + 4 = 7.', ['(x + 2)(x + 6)', '(x + 12)(x + 1)', '(x − 3)(x − 4)']),
    ('Factorise completely 4x²y − 10xy².', '2xy(2x − 5y)', 'HCF is 2xy.', ['2(2x²y − 5xy²)', 'xy(4x − 10y)', '2xy(2x − 10y)']),
    ('Factorise x² − x − 20.', '(x − 5)(x + 4)', '−5 × 4 = −20 and −5 + 4 = −1.', ['(x + 5)(x − 4)', '(x − 10)(x + 2)', '(x − 20)(x + 1)']),
    ('Which expression is a difference of two squares?', '9a² − 16b²', '9a² = (3a)² and 16b² = (4b)².', ['9a² + 16b²', '9a² − 16b', 'a² − 8']),
])
t62.fixed('C2', (2, 3), [
    ('Explain what "factorise completely" means, using 12x + 18 as an example.', 'Take out the highest common factor so the bracket has no further common factor: 12x + 18 = 6(2x + 3), not 2(6x + 9).', 'B1 HCF; B1 6(2x + 3) [2]'),
    ('Explain how to check that a factorisation is correct.', 'Expand the brackets; the result should be the original expression.', 'B1 expand; B1 compare with original [2]'),
    ('Explain why x² + 9 cannot be factorised as a difference of two squares.', 'It is a sum, not a difference, of two squares; (x + 3)(x − 3) gives x² − 9.', 'B1 sum not difference; B1 (x + 3)(x − 3) = x² − 9 [2]'),
])


@t62.add('C1', (1, 2, 3))
def t62_tri(r, D):
    p, q = r.choice([-9, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8]), r.choice([-8, -6, -5, -4, -3, -2, 1, 2, 3, 4, 5, 6, 9])
    if p == q or p == -q:
        return None
    b, c = p + q, p * q
    cor = f'{bracket(p)}{bracket(q)}'
    ds = [f'{bracket(-p)}{bracket(-q)}', f'{bracket(p)}{bracket(-q)}', f'{bracket(-p)}{bracket(q)}', f'{bracket(c)}{bracket(1)}' if abs(c) > 1 else f'{bracket(p + 1)}{bracket(q - 1)}']
    ds = [d_ for d_ in ds if d_ != cor and d_ != f'{bracket(q)}{bracket(p)}']
    return SMC(r, f'Factorise {quad(1, b, c)}.', cor, ds, f'Find two numbers with product {num(c)} and sum {num(b)}: {num(p)} and {num(q)}.')


@t62.add('C3', (1, 2, 3, 4, 5))
def t62_fact(r, D):
    v = r.choice(['x', 'a', 'p', 'y'])
    if D == 1:
        k = r.randint(2, 9)
        a, b = r.randint(1, 6), r.randint(1, 9)
        if math.gcd(a, b) != 1:
            return None
        return Q(f'Factorise {expr((k * a, v), (k * b, ""))}.', f'{k}({lin(a, b, v)})', f'B1 {k}({lin(a, b, v)}) [1]')
    if D == 2:
        k = r.randint(2, 6)
        a, b = r.randint(1, 5), r.randint(1, 5)
        w = r.choice(['y', 'b', 'q'])
        if math.gcd(a, b) != 1:
            return None
        return Q(f'Factorise completely {mono(k * a, {v: 2, w: 1})} − {mono(k * b, {v: 1, w: 2})}.', f'{mono(k, {v: 1, w: 1})}({expr((a, v), (-b, w))})', f'B1 {mono(k, {v: 1, w: 1})} outside; B1 bracket {expr((a, v), (-b, w))} [2]')
    if D == 3:
        case = r.choice(['dots', 'tri'])
        if case == 'dots':
            a, b = r.randint(1, 5), r.randint(2, 9)
            return Q(f'Factorise {mono(a * a, {v: 2})} − {b * b}.', f'({mono(a, {v: 1})} − {b})({mono(a, {v: 1})} + {b})', f'M1 recognises ({mono(a, {v: 1})})² − {b}²; A1 ({mono(a, {v: 1})} − {b})({mono(a, {v: 1})} + {b}) [2]')
        p, q = r.randint(-9, 9) or 1, r.randint(-9, 9) or 2
        return Q(f'Factorise {quad(1, p + q, p * q, v)}.', f'{bracket(p, v)}{bracket(q, v)}', f'M1 two numbers with product {num(p * q)} and sum {num(p + q)}; A1 {bracket(p, v)}{bracket(q, v)} [2]')
    if D == 4:
        case = r.choice(['group', 'atri'])
        if case == 'group':
            a, b, c = r.randint(2, 6), r.randint(2, 7), r.choice(['y', 'b'])
            # ax + ay... use x(a + b) form: v*c + b*v + a*c + a*b ... (v + a)(c + b)
            return Q(f'Factorise {v}{c} + {b}{v} + {a}{c} + {a * b}.', f'({v} + {a})({c} + {b})', f'M1 {v}({c} + {b}) + {a}({c} + {b}); A1 ({v} + {a})({c} + {b}) [2]')
        A, p, q = r.choice([2, 3, 5]), r.randint(-6, 6) or 1, r.randint(-6, 6) or 3
        pr = poly_mul([A, p], [1, q])
        if math.gcd(math.gcd(pr[0], pr[1]), pr[2]) != 1:
            return None
        return Q(f'Factorise {poly_str(pr, v)}.', f'{lb(A, p, v)}{bracket(q, v)}', f'M1 splits the middle term or uses product {num(pr[0] * pr[2])}; A1 {lb(A, p, v)}{bracket(q, v)} [2]')
    k = r.randint(2, 5)
    a = r.randint(2, 9)
    return Q(f'Factorise completely {mono(k, {v: 3})} − {k * a * a}{v}.', f'{k}{v}({v} − {a})({v} + {a})', f'M1 {k}{v}({v}² − {a * a}); M1 difference of two squares; A1 {k}{v}({v} − {a})({v} + {a}) [3]')


@t62.add('C3', (2, 3, 4))
def t62_numeric(r, D):
    a = r.choice([97, 98, 99, 101, 102, 103, 51, 49, 999, 1001])
    b = r.choice([3, 2, 1]) if a < 200 else 1
    big = r.choice([(17.5, 2.5), (8.7, 1.3), (65, 35), (123, 77), (5.6, 4.4), (14.2, 5.8)])
    if r.random() < 0.5:
        x, y = big
        return Q(f'Use the difference of two squares to work out {ex(x)}² − {ex(y)}² without a calculator.', ex(round((x - y) * (x + y), 4)), f'M1 ({ex(x)} − {ex(y)})({ex(x)} + {ex(y)}) = {ex(round(x - y, 2))} × {ex(round(x + y, 2))}; A1 {ex(round((x - y) * (x + y), 4))} [2]')
    n = r.choice([23, 37, 47, 63, 86, 14, 58])
    m = r.choice([77, 63, 53, 37, 14, 86, 42])
    k = r.choice([13, 17, 19, 7, 11])
    return Q(f'Use factorisation to work out {k} × {n} + {k} × {m} without a calculator.', num(k * (n + m)), f'M1 {k}({n} + {m}); A1 {num(k * (n + m))} [2]')


@t62.add('C2', (2, 3, 4), 'explain')
def t62_err(r, D):
    nm = person(r)
    case = r.choice(['incomplete', 'sign', 'dots'])
    if case == 'incomplete':
        k, a, b = r.choice([(2, 6, 9), (3, 4, 8), (2, 10, 15), (4, 6, 9), (5, 4, 6)])
        g = math.gcd(a, b) * k
        return Q(f'{nm} factorises {k * a}x + {k * b} as {k}({a}x + {b}). Explain why this is not fully factorised and give the complete factorisation.', f'{a} and {b} still have a common factor {math.gcd(a, b)}. Complete: {g}({a // math.gcd(a, b)}x + {b // math.gcd(a, b)}).',
                 f'B1 bracket still has common factor; B1 {g}({a // math.gcd(a, b)}x + {b // math.gcd(a, b)}) [2]')
    if case == 'sign':
        p, q = r.randint(2, 7), r.randint(2, 7)
        if p == q:
            return None
        return Q(f'{nm} factorises {quad(1, -(p + q), p * q)} as (x + {p})(x + {q}). Explain the error and give the correct factorisation.', f'The middle term is negative, so both numbers must be negative: (x − {p})(x − {q}). Expanding (x + {p})(x + {q}) gives +{p + q}x.',
                 f'B1 sign of middle term requires negative numbers; B1 (x − {p})(x − {q}) [2]')
    a = r.randint(3, 9)
    return Q(f'{nm} says x² − {a * a} = (x − {a})². Show that {nm} is wrong and give the correct factorisation.', f'(x − {a})² = x² − {2 * a}x + {a * a}, not x² − {a * a}. Correct: (x − {a})(x + {a}).', f'M1 expands (x − {a})²; A1 (x − {a})(x + {a}) [2]')


def t62_c4(r, D):
    p, q = r.randint(2, 8), r.randint(1, 7)
    if p == q:
        return None
    intro = f'The area of a rectangle is ({quad(1, p + q, p * q)}) cm².'
    xv = r.randint(3, 9)
    parts = [
        P('Factorise the expression for the area.', f'{bracket(p)}{bracket(q)}', f'M1 product {p * q}, sum {p + q}; A1 {bracket(p)}{bracket(q)}', 2),
        P('Write down possible expressions for the length and width of the rectangle.', f'{bracket(max(p, q))} cm and {bracket(min(p, q))} cm', 'B1 both factors as dimensions', 1),
        P('Find an expression for the perimeter, in its simplest form.', f'({lin(4, 2 * (p + q))}) cm', f'M1 2({lin(1, p)} + {lin(1, q)}); A1 {lin(4, 2 * (p + q))}', 2),
        P(f'Find the area when x = {xv}, using your factorised form.', f'{(xv + p) * (xv + q)} cm²', f'B1 {xv + p} × {xv + q} = {(xv + p) * (xv + q)}', 1),
        P(f'A square has area (x² − {2 * p}x + {p * p}) cm². Find its side length in terms of x.', f'(x − {p}) cm', f'M1 (x − {p})²; A1 x − {p}', 2),
    ]
    return cmp_(r, intro, parts)


t62.add('C4', (2, 3, 4, 5))(t62_c4)

# ---------------------------------------------------------------- rearranging formulae
t63 = topic('Rearranging and changing the subject of formulae', 'rearranging and changing the subject of formulae', 'changing the subject', 'rearranging formulae')
t63.fixed('C1', (1, 2), [
    ('Make x the subject of y = x + 5.', 'x = y − 5', 'Subtract 5 from both sides.', ['x = y + 5', 'x = 5 − y', 'x = 5y']),
    ('Make r the subject of C = 2πr.', 'r = C/(2π)', 'Divide both sides by 2π.', ['r = 2πC', 'r = C − 2π', 'r = 2π/C']),
    ('Make t the subject of v = u + at.', 't = (v − u)/a', 'Subtract u then divide by a.', ['t = v − u/a', 't = (v + u)/a', 't = a(v − u)']),
    ('Make b the subject of A = ½bh.', 'b = 2A/h', 'Multiply by 2 then divide by h.', ['b = A/(2h)', 'b = 2Ah', 'b = Ah/2']),
    ('Make x the subject of y = 3x − 4.', 'x = (y + 4)/3', 'Add 4 then divide by 3.', ['x = (y − 4)/3', 'x = y/3 + 4', 'x = 3(y + 4)']),
    ('Make r the subject of A = πr².', 'r = √(A/π)', 'Divide by π then take the square root.', ['r = A/(2π)', 'r = √A/π', 'r = (A/π)²']),
])
t63.fixed('C2', (2, 3), [
    ('Explain why rearranging a formula uses the same steps as solving an equation.', 'In both cases you apply inverse operations to both sides, in reverse order, to isolate the required letter.', 'B1 inverse operations; B1 both sides / reverse order [2]'),
    ('Explain why, when making r the subject of A = πr², you take the positive square root only in a context such as area.', 'A radius is a length, so it must be positive; the negative root has no meaning here.', 'B1 length positive; B1 discard negative root [2]'),
    ('Explain what to do when the new subject appears twice in a formula, such as ax = b + cx.', 'Collect the terms containing x on one side, factorise out x, then divide: x(a − c) = b, so x = b/(a − c).', 'B1 collect terms; B1 factorise and divide [2]'),
])

REARR = [
    ('v = u + at', 'u', 'u = v − at'), ('v = u + at', 'a', 'a = (v − u)/t'), ('P = 2(l + w)', 'w', 'w = P/2 − l'), ('A = ½(a + b)h', 'h', 'h = 2A/(a + b)'),
    ('y = mx + c', 'm', 'm = (y − c)/x'), ('V = πr²h', 'h', 'h = V/(πr²)'), ('E = ½mv²', 'v', 'v = √(2E/m)'), ('F = 9C/5 + 32', 'C', 'C = 5(F − 32)/9'),
    ('s = (u + v)t/2', 't', 't = 2s/(u + v)'), ('T = 2π√(l/g)', 'l', 'l = gT²/(4π²)'), ('V = ⅓πr²h', 'r', 'r = √(3V/(πh))'), ('I = PRT/100', 'R', 'R = 100I/(PT)'),
]


@t63.add('C1', (2, 3))
def t63_pick(r, D):
    f, s_, ans = r.choice(REARR)
    others = [a for g, t, a in REARR if a.split(' = ')[0] == s_ and a != ans]
    wrong = {'u = v − at': ['u = v + at', 'u = (v − a)/t', 'u = at − v'], 'a = (v − u)/t': ['a = v − u/t', 'a = (v + u)/t', 'a = t(v − u)'], 'w = P/2 − l': ['w = P − 2l', 'w = 2P − l', 'w = (P − l)/2'],
             'h = 2A/(a + b)': ['h = A/(2(a + b))', 'h = 2A − (a + b)', 'h = (a + b)/(2A)'], 'm = (y − c)/x': ['m = y − c/x', 'm = (y + c)/x', 'm = x(y − c)'], 'h = V/(πr²)': ['h = Vπr²', 'h = πr²/V', 'h = V − πr²'],
             'v = √(2E/m)': ['v = 2E/m', 'v = √(E/2m)', 'v = (2E/m)²'], 'C = 5(F − 32)/9': ['C = 9(F − 32)/5', 'C = 5F/9 − 32', 'C = (F − 32)/9'], 't = 2s/(u + v)': ['t = s/(2(u + v))', 't = 2s(u + v)', 't = (u + v)/2s'],
             'l = gT²/(4π²)': ['l = gT/(2π)', 'l = T²/(4π²g)', 'l = g√T/(2π)'], 'r = √(3V/(πh))': ['r = 3V/(πh)', 'r = √(V/(3πh))', 'r = (3V/(πh))²'], 'R = 100I/(PT)': ['R = IPT/100', 'R = PT/(100I)', 'R = 100IPT']}[ans]
    return SMC(r, f'Make {s_} the subject of {f}.', ans, wrong, f'Use inverse operations in reverse order: {ans}.')


@t63.add('C3', (1, 2, 3, 4, 5))
def t63_make(r, D):
    if D <= 2:
        a, b = r.randint(2, 9), r.randint(1, 12)
        v1, v2 = r.choice([('y', 'x'), ('p', 'q'), ('A', 'r'), ('T', 'n')])
        op = r.choice(['+', '−'])
        return Q(f'Make {v2} the subject of {v1} = {a}{v2} {op} {b}.', f'{v2} = ({v1} {"−" if op == "+" else "+"} {b})/{a}', f'M1 {v1} {"−" if op == "+" else "+"} {b} = {a}{v2}; A1 {v2} = ({v1} {"−" if op == "+" else "+"} {b})/{a} [2]')
    if D == 3:
        f, s_, ans = r.choice(REARR[:9])
        return Q(f'Make {s_} the subject of the formula {f}.', ans, f'M1 first correct inverse step; A1 {ans} [2]')
    if D == 4:
        f, s_, ans = r.choice(REARR[6:])
        return Q(f'Make {s_} the subject of the formula {f}.', ans, f'M1 isolates the term containing {s_}; M1 deals with root/power correctly; A1 {ans} [3]')
    a, b = r.randint(2, 6), r.randint(1, 5)
    c = r.randint(2, 9)
    return Q(f'Make x the subject of {mono(a, {"x": 1})} − {c} = y(x + {b}).',
             f'x = ({b}y + {c})/({a} − y)', f'M1 expands: {a}x − {c} = xy + {b}y; M1 collects x terms: {a}x − xy = {b}y + {c}; M1 factorises x({a} − y); A1 x = ({b}y + {c})/({a} − y) [4]')


@t63.add('C3', (2, 3, 4))
def t63_use(r, D):
    f, s_, ans, fn, vals = r.choice([
        ('v = u + at', 't', 't = (v − u)/a', lambda v, u, a: (v - u) / a, {'v': [20, 25, 30, 32], 'u': [4, 5, 8, 2], 'a': [2, 2.5, 4]}),
        ('A = ½(a + b)h', 'h', 'h = 2A/(a + b)', lambda A, a, b: 2 * A / (a + b), {'A': [30, 45, 60, 84], 'a': [4, 5, 6], 'b': [8, 10, 9]}),
        ('V = πr²h', 'h', 'h = V/(πr²)', lambda V, r_: V / (math.pi * r_ * r_), {'V': [500, 750, 1000, 1500], 'r': [4, 5, 6, 3.5]}),
        ('E = ½mv²', 'v', 'v = √(2E/m)', lambda E, m: math.sqrt(2 * E / m), {'E': [200, 450, 900, 1250], 'm': [2, 4, 5, 8]}),
    ])
    keys = list(vals)[0:]
    chosen = {k: r.choice(v) for k, v in vals.items()}
    res = fn(*chosen.values())
    given = ', '.join(f'{k} = {num(v)}' for k, v in chosen.items())
    return Q(f'(a) Make {s_} the subject of {f}. (b) Find {s_} when {given}, giving your answer correct to 3 significant figures where necessary.', f'(a) {ans} (b) {s_} = {nn(res)}',
             f'(a) M1 inverse step; A1 {ans} (b) M1 substitution; A1 {nn(res)} [4]', type='multi_step')


@t63.add('C2', (2, 3, 4), 'explain')
def t63_err(r, D):
    nm = person(r)
    case = r.choice(['order', 'root', 'div'])
    if case == 'order':
        a, b = r.randint(2, 9), r.randint(1, 9)
        return Q(f'{nm} makes x the subject of y = {a}x + {b} and writes x = y/{a} − {b}. Explain the mistake and give the correct formula.', f'{nm} divided before subtracting {b}; the {b} must also be divided by {a}. Correct: x = (y − {b})/{a}.',
                 f'B1 order of inverse operations; B1 x = (y − {b})/{a} [2]')
    if case == 'root':
        return Q(f'{nm} rearranges A = πr² to get r = √A/π. Explain the mistake and give the correct formula.', 'Divide by π before taking the square root, so π must be inside the root: r = √(A/π).', 'B1 π inside root; B1 r = √(A/π) [2]')
    return Q(f'{nm} makes t the subject of v = u + at and writes t = v − u − a. Explain the mistake.', 'a multiplies t, so you must divide by a, not subtract it: t = (v − u)/a.', 'B1 a is a multiplier, so divide; B1 t = (v − u)/a [2]')


def t63_c4(r, D):
    intro = 'The formula F = 9C/5 + 32 converts a temperature of C degrees Celsius into F degrees Fahrenheit.'
    c1 = r.choice([15, 25, 35, -10, 40])
    f1 = r.choice([59, 77, 104, 23, 212])
    parts = [
        P(f'Find F when C = {num(c1)}.', num(Fr(9 * c1, 5) + 32), f'M1 9 × {num(c1)} ÷ 5 + 32; A1 {num(Fr(9 * c1, 5) + 32)}', 2),
        P('Make C the subject of the formula.', 'C = 5(F − 32)/9', 'M1 F − 32 = 9C/5; M1 × 5 ÷ 9; A1 C = 5(F − 32)/9', 3),
        P(f'Use your formula to find C when F = {f1}.', num(Fr(5 * (f1 - 32), 9)), f'B1 {num(Fr(5 * (f1 - 32), 9))}', 1),
        P('Find the temperature at which F and C have the same value.', '−40', 'M1 C = 9C/5 + 32; M1 −4C/5 = 32; A1 −40', 3),
    ]
    return cmp_(r, intro, parts)


t63.add('C4', (2, 3, 4, 5))(t63_c4)

# ---------------------------------------------------------------- constructing equations
t64 = topic('Constructing equations from words and geometric contexts', 'constructing equations from words and geometric contexts', 'constructing equations', 'forming equations')
t64.fixed('C1', (1, 2), [
    ('I think of a number, multiply it by 4 and subtract 7. The answer is 25. Which equation represents this?', '4n − 7 = 25', 'Multiply n by 4, then subtract 7.', ['4(n − 7) = 25', '7 − 4n = 25', 'n/4 − 7 = 25']),
    ('The perimeter of a square of side (x + 3) cm is 36 cm. Which equation is correct?', '4(x + 3) = 36', 'Perimeter = 4 × side.', ['(x + 3)² = 36', 'x + 12 = 36', '2(x + 3) = 36']),
    ('Two angles on a straight line are x° and (2x + 30)°. Which equation is correct?', '3x + 30 = 180', 'Angles on a straight line add to 180°.', ['3x + 30 = 360', '3x + 30 = 90', '2x + 30 = x']),
    ('Ali is 3 years older than Ben. Their ages add to 29. If Ben is b years old, which equation is correct?', '2b + 3 = 29', 'b + (b + 3) = 29.', ['b + 3 = 29', '3b = 29', '2b − 3 = 29']),
])
t64.fixed('C2', (2, 3), [
    ('Explain why you should define the letter you use when forming an equation from a problem.', 'It makes clear what the unknown represents (e.g. "let x be the width in cm"), so the solution can be interpreted correctly in context.', 'B1 states meaning/units; B1 interpret answer [2]'),
    ('Explain why a solution of x = −4 might be rejected when x is the width of a rectangle.', 'A width must be positive, so a negative value is not possible in this context.', 'B1 length positive; B1 reject in context [2]'),
])


@t64.add('C3', (1, 2, 3, 4, 5))
def t64_words(r, D):
    nm = person(r)
    case = r.choice(['think', 'ages', 'rect', 'angles', 'tri', 'coins'] if D >= 3 else ['think', 'ages', 'angles'])
    if case == 'think':
        n, a, b = r.randint(3, 15), r.randint(2, 7), r.randint(2, 12)
        res = a * (n + b) if D >= 3 else a * n - b
        st = f'add {b} and multiply the result by {a}' if D >= 3 else f'multiply it by {a} and subtract {b}'
        eq = f'{a}(n + {b}) = {res}' if D >= 3 else f'{a}n − {b} = {res}'
        return Q(f'{nm} thinks of a number, n. {nm} says: "I {st}. The answer is {res}." Form an equation in n and solve it.', f'{eq}; n = {n}', f'B1 {eq}; M1 solves; A1 n = {n} [3]')
    if case == 'ages':
        b = r.randint(5, 15)
        k = r.randint(2, 4)
        d = r.randint(2, 8)
        tot = b + k * b + (b + d)
        nm2, nm3 = two_people(r)
        return Q(f'{nm2} is x years old. {nm3} is {k} times as old as {nm2}, and {nm} is {d} years older than {nm2}. Their ages add up to {tot}. Form and solve an equation to find each age.',
                 f'{nm2} {b}, {nm3} {k * b}, {nm} {b + d}', f'B1 x + {k}x + x + {d} = {tot}; M1 {k + 2}x = {tot - d}; A1 x = {b}; A1 all three ages [4]')
    if case == 'angles':
        a, c = r.randint(2, 4), r.randint(10, 40)
        x = Fr(180 - c, a + 1)
        if x.denominator != 1:
            return None
        return Q(f'Two angles on a straight line are x° and ({a}x + {c})°. Form and solve an equation to find x.', f'x = {int(x)}', f'B1 x + {a}x + {c} = 180; M1 {a + 1}x = {180 - c}; A1 x = {int(x)} [3]')
    if case == 'rect':
        w = r.randint(3, 15)
        d = r.randint(2, 9)
        P_ = 2 * (w + w + d)
        return Q(f'A rectangle is {d} cm longer than it is wide. Its perimeter is {P_} cm. Form and solve an equation to find its area.', f'{w * (w + d)} cm²', f'B1 2(x + x + {d}) = {P_}; A1 x = {w}; M1 {w} × {w + d}; A1 {w * (w + d)} cm² [4]')
    if case == 'tri':
        x = r.randint(4, 12)
        a, b = r.randint(1, 3), r.randint(1, 7)
        P_ = x + (x + b) + (a * x)
        return Q(f'The sides of a triangle are x cm, (x + {b}) cm and {a if a > 1 else ""}x cm. The perimeter is {P_} cm. Form and solve an equation to find the length of the longest side.', f'{max(x + b, a * x)} cm',
                 f'B1 {a + 2}x + {b} = {P_}; A1 x = {x}; B1 longest {max(x + b, a * x)} cm [3]')
    c1, c2 = r.choice([(5, 10), (10, 20), (20, 50), (2, 5)])
    n = r.randint(6, 20)
    extra = r.randint(2, 9)
    tot = c1 * (n + extra) + c2 * n
    return Q(f'{nm} has only {c1}-cent and {c2}-cent coins. There are {extra} more {c1}-cent coins than {c2}-cent coins, and the total value is {tot} cents. Form and solve an equation to find the number of each coin.',
             f'{n} {c2}-cent coins and {n + extra} {c1}-cent coins', f'B1 {c1}(x + {extra}) + {c2}x = {tot}; M1 {c1 + c2}x = {tot - c1 * extra}; A1 x = {n}; A1 {n + extra} [4]')


@t64.add('C1', (1, 2, 3))
def t64_pick(r, D):
    a, b, res = r.randint(2, 6), r.randint(2, 9), r.randint(20, 60)
    cor = f'{a}(n + {b}) = {res}'
    ds = [f'{a}n + {b} = {res}', f'n + {a * b} = {res}', f'{a}n = {res} + {b}', f'(n + {a})/{b} = {res}']
    return SMC(r, f'I think of a number n, add {b}, then multiply by {a}. The result is {res}. Which equation is correct?', cor, ds, f'Add first, so the bracket (n + {b}) is multiplied by {a}.')


@t64.add('C2', (2, 3, 4), 'explain')
def t64_check(r, D):
    nm = person(r)
    w = r.randint(4, 12)
    d = r.randint(2, 6)
    P_ = 2 * (2 * w + d)
    wrong = Fr(P_ - d, 2)
    return Q(f'A rectangle has length (x + {d}) cm and width x cm. Its perimeter is {P_} cm. {nm} writes x + x + {d} = {P_}. Explain the mistake, then write and solve the correct equation.',
             f'{nm} has added only one length and one width; the perimeter has two of each. Correct: 2(2x + {d}) = {P_}, so x = {w}.', f'B1 perimeter needs 2 lengths + 2 widths; B1 2(2x + {d}) = {P_}; B1 x = {w} [3]')


def t64_c4(r, D):
    x = r.randint(8, 25)
    a, b = r.randint(2, 3), r.randint(5, 20)
    c = 180 - (x + a * x + b)
    if c <= 10 or c >= 120:
        return None
    nm = person(r)
    intro = f'Triangle ABC has angle A = x°, angle B = ({a}x + {b})° and angle C = {c}°.'
    parts = [
        P('Form an equation in x and show that it simplifies to ' + f'{a + 1}x = {180 - b - c}.', 'Shown', f'M1 x + {a}x + {b} + {c} = 180; A1 {a + 1}x = {180 - b - c}', 2),
        P('Solve the equation and find angle B.', f'x = {x}; B = {a * x + b}°', f'M1 x = {x}; A1 {a * x + b}°', 2),
        P('Decide whether the triangle is acute, right-angled or obtuse. Give a reason.', ('obtuse' if max(x, a * x + b, c) > 90 else ('right-angled' if max(x, a * x + b, c) == 90 else 'acute')) + f': the largest angle is {max(x, a * x + b, c)}°', f'B1 conclusion with largest angle {max(x, a * x + b, c)}°', 1),
        P(f'{nm} draws a second triangle whose angles are x°, 2x° and 3x°. Find the largest angle.', '90°', 'M1 6x = 180; A1 x = 30, largest 90°', 2),
    ]
    return cmp_(r, intro, parts)


t64.add('C4', (2, 3, 4, 5))(t64_c4)
CHAPTERS[6] = [t61, t62, t63, t64]


# =========================================================== 7 Perimeter, area and volume
PI = math.pi

t71 = topic('Perimeter and area of triangles, quadrilaterals and compound shapes', 'perimeter and area of triangles, quadrilaterals and compound shapes', 'area of compound shapes', 'perimeter area')
t71.fixed('C1', (1, 2), [
    ('What is the formula for the area of a trapezium with parallel sides a and b and height h?', '½(a + b)h', 'Average of the parallel sides × height.', ['(a + b)h', '½abh', 'a + b + h']),
    ('The area of a parallelogram with base 9 cm and perpendicular height 4 cm is', '36 cm²', 'Area = base × perpendicular height.', ['18 cm²', '26 cm', '13 cm²']),
    ('The area of a triangle with base 10 cm and height 7 cm is', '35 cm²', '½ × 10 × 7 = 35.', ['70 cm²', '17 cm²', '17.5 cm²']),
    ('Which of these is a unit of area?', 'm²', 'Area is measured in square units.', ['m', 'm³', 'ml']),
    ('The perimeter of a rectangle 8 cm by 5 cm is', '26 cm', '2(8 + 5) = 26.', ['40 cm', '13 cm', '26 cm²']),
    ('A rhombus has diagonals 6 cm and 10 cm. Its area is', '30 cm²', 'Area = ½ × d₁ × d₂.', ['60 cm²', '16 cm²', '15 cm²']),
])
t71.fixed('C2', (2, 3), [
    ('Explain why the area of a triangle is half the area of a rectangle with the same base and height.', 'Drawing the diagonal of the rectangle splits it into two identical triangles, each with that base and height.', 'B1 two congruent triangles; B1 so half [2]'),
    ('Explain why the slanted side of a parallelogram is not used to calculate its area.', 'Area needs the perpendicular height; the slanted side is longer than the height, so using it would overestimate the area.', 'B1 perpendicular height needed; B1 slant longer [2]'),
    ('Explain why two shapes with the same perimeter can have different areas, with an example.', 'Perimeter measures the boundary, area the space inside: a 1 × 9 rectangle and a 5 × 5 square both have perimeter 20, but areas 9 and 25.', 'B1 different measures; B1 valid example [2]'),
])


@t71.add('C1', (1, 2, 3))
def t71_area(r, D):
    shape = r.choice(['tri', 'para', 'trap'] if D > 1 else ['tri', 'para'])
    if shape == 'tri':
        b, h = r.randint(4, 20), r.randint(3, 15)
        c = b * h / 2
        return MC(r, f'A triangle has base {b} cm and perpendicular height {h} cm. Find its area.', c, [b * h, b + h, (b + h) / 2, b * h / 4], f'½ × {b} × {h} = {ex(c)} cm².', fmtf=lambda v: f'{ex(v)} cm²')
    if shape == 'para':
        b, h, s_ = r.randint(5, 18), r.randint(3, 12), r.randint(4, 15)
        if s_ <= h:
            s_ = h + 2
        return MC(r, f'A parallelogram has base {b} cm, slanted side {s_} cm and perpendicular height {h} cm. Find its area.', b * h, [b * s_, b * h / 2, 2 * (b + s_), b * s_ / 2], f'Area = base × perpendicular height = {b} × {h} = {b * h} cm².', fmtf=lambda v: f'{ex(v)} cm²')
    a, b, h = r.randint(3, 12), r.randint(8, 20), r.randint(3, 10)
    c = (a + b) * h / 2
    return MC(r, f'A trapezium has parallel sides {a} cm and {b} cm, and the distance between them is {h} cm. Find its area.', c, [(a + b) * h, a * b * h / 2, (a + b + h), b * h], f'½({a} + {b}) × {h} = {ex(c)} cm².', fmtf=lambda v: f'{ex(v)} cm²')


@t71.add('C3', (1, 2, 3, 4, 5))
def t71_compound(r, D):
    nm = person(r)
    if D <= 2:
        W, H = r.randint(8, 16), r.randint(6, 12)
        w, h = r.randint(2, W - 3), r.randint(2, H - 2)
        A = W * H - w * h
        P_ = 2 * (W + H)
        return Q(f'An L-shaped room is made by removing a {w} m by {h} m rectangle from one corner of a {W} m by {H} m rectangle. Find the area and the perimeter of the room.',
                 f'Area {A} m²; perimeter {P_} m', f'M1 {W} × {H} − {w} × {h}; A1 {A} m²; B1 perimeter {P_} m (same as the full rectangle) [3]')
    if D == 3:
        W, H = r.randint(6, 14), r.randint(4, 10)
        th = r.randint(3, 8)
        A = W * H + W * th / 2
        return Q(f'The end wall of a shed in {city(r)} is a rectangle {W} m wide and {H} m high with an isosceles triangle on top. The top of the triangle is {th} m above the top of the rectangle. Find the area of the end wall.',
                 f'{ex(A)} m²', f'M1 {W} × {H} = {W * H}; M1 ½ × {W} × {th} = {ex(W * th / 2)}; A1 {ex(A)} m² [3]')
    a, b, h = r.randint(4, 10), r.randint(11, 20), r.randint(4, 9)
    trap = (a + b) * h / 2
    pr = r.choice([12, 15, 18, 25, 30])
    pack = r.choice([5, 8, 10])
    n = math.ceil(trap / pack)
    return Q(f'{nm}\'s garden is a trapezium with parallel sides {a} m and {b} m, {h} m apart. Grass seed costs ${pr} per box and one box covers {pack} m². Find the cost of seeding the whole garden.',
             f'${n * pr}', f'M1 ½({a} + {b}) × {h} = {ex(trap)} m²; M1 ÷ {pack} = {ex(round(trap / pack, 2))}; A1 {n} boxes; A1 ${n * pr} [4]')


@t71.add('C3', (2, 3, 4))
def t71_reverse(r, D):
    shape = r.choice(['tri', 'trap', 'rect'])
    if shape == 'tri':
        b, h = r.randint(4, 16), r.randint(3, 14)
        return Q(f'A triangle has area {ex(b * h / 2)} cm² and base {b} cm. Find its perpendicular height.', f'{h} cm', f'M1 ½ × {b} × h = {ex(b * h / 2)}; A1 h = {h} cm [2]')
    if shape == 'trap':
        a, b, h = r.randint(3, 10), r.randint(8, 18), r.randint(2, 9)
        return Q(f'A trapezium has area {ex((a + b) * h / 2)} cm². Its parallel sides are {a} cm and {b} cm. Find the distance between the parallel sides.', f'{h} cm', f'M1 ½({a} + {b})h = {ex((a + b) * h / 2)}; A1 h = {h} [2]')
    l, w = r.randint(5, 20), r.randint(3, 12)
    return Q(f'A rectangle has perimeter {2 * (l + w)} cm and length {l} cm. Find its area.', f'{l * w} cm²', f'M1 width = ({2 * (l + w)} − {2 * l}) ÷ 2 = {w}; A1 {l * w} cm² [2]')


@t71.add('C2', (2, 3, 4), 'explain')
def t71_err(r, D):
    nm = person(r)
    case = r.choice(['tri', 'para', 'units'])
    if case == 'tri':
        b, h = r.randint(6, 18), r.randint(4, 12)
        return Q(f'{nm} says the area of a triangle with base {b} cm and height {h} cm is {b * h} cm². Explain the mistake and give the correct area.', f'{nm} forgot to halve: area = ½ × {b} × {h} = {ex(b * h / 2)} cm².', f'B1 missing ½; B1 {ex(b * h / 2)} cm² [2]')
    if case == 'para':
        b, h, s_ = r.randint(6, 15), r.randint(3, 8), r.randint(9, 14)
        return Q(f'A parallelogram has base {b} cm, slanted side {s_} cm and perpendicular height {h} cm. {nm} calculates the area as {b} × {s_} = {b * s_} cm². Explain the mistake and give the correct area.',
                 f'The perpendicular height must be used, not the slanted side: {b} × {h} = {b * h} cm².', f'B1 perpendicular height; B1 {b * h} cm² [2]')
    l, w = round(r.uniform(1.2, 4.8), 1), r.choice([30, 45, 60, 75, 80])
    return Q(f'{nm} finds the area of a rectangle {ex(l)} m long and {w} cm wide as {ex(l)} × {w} = {ex(l * w)} m². Explain the mistake and give the correct area in m².', f'The units are different; convert {w} cm to {ex(w / 100)} m: {ex(l)} × {ex(w / 100)} = {ex(round(l * w / 100, 4))} m².',
             f'B1 inconsistent units; B1 {ex(round(l * w / 100, 4))} m² [2]')


def t71_c4(r, D):
    L, W = r.randint(12, 25), r.randint(8, 15)
    pw = r.choice([1, 1.5, 2])
    nm = person(r)
    inner = (L - 2 * pw) * (W - 2 * pw)
    path = L * W - inner
    cost = r.choice([18, 22, 25, 32])
    intro = f'A rectangular park in {city(r)} measures {L} m by {W} m. A path {ex(pw)} m wide runs around the inside edge of the park; the rest is a lawn.'
    parts = [
        P('Find the area of the lawn.', f'{ex(inner)} m²', f'M1 ({L} − {ex(2 * pw)}) × ({W} − {ex(2 * pw)}); A1 {ex(inner)}', 2),
        P('Find the area of the path.', f'{ex(path)} m²', f'M1 {L * W} − {ex(inner)}; A1 {ex(path)}', 2),
        P(f'The path is paved at ${cost} per m². Find the cost of paving.', f'${ex(path * cost)}', f'B1 {ex(path)} × {cost} = {ex(path * cost)}', 1),
        P('Find the perimeter of the lawn.', f'{ex(2 * (L - 2 * pw + W - 2 * pw))} m', f'M1 2({ex(L - 2 * pw)} + {ex(W - 2 * pw)}); A1 {ex(2 * (L - 2 * pw + W - 2 * pw))}', 2),
        P(f'{nm} says that halving the width of the path would halve its area. Explain whether {nm} is correct.', f'No. With width {ex(pw / 2)} m the path area is {ex(L * W - (L - pw) * (W - pw))} m², which is not half of {ex(path)} m² because the corners overlap.',
          'M1 calculates new area; A1 conclusion with reason', 2),
    ]
    return cmp_(r, intro, parts)


t71.add('C4', (2, 3, 4, 5))(t71_c4)

# ---------------------------------------------------------------- circles, arcs, sectors
t72 = topic('Circles: arc length and area of a sector', 'circles: arc length and area of a sector', 'arc length', 'area of a sector')
t72.fixed('C1', (1, 2), [
    ('What is the formula for the circumference of a circle with radius r?', '2πr', 'C = 2πr = πd.', ['πr²', 'πr', '2πr²']),
    ('What fraction of a circle is a sector with angle 90°?', '1/4', '90 ÷ 360 = 1/4.', ['1/2', '1/3', '9/36']),
    ('The arc length of a sector with angle θ and radius r is', '(θ/360) × 2πr', 'A fraction θ/360 of the circumference.', ['(θ/360) × πr²', 'θ × r', '(θ/180) × πr²']),
    ('A semicircle has diameter 10 cm. Its area is', '12.5π cm²', '½ × π × 5² = 12.5π.', ['25π cm²', '50π cm²', '5π cm²']),
    ('The area of a sector with angle θ and radius r is', '(θ/360) × πr²', 'A fraction θ/360 of the area of the circle.', ['(θ/360) × 2πr', '½θr', 'θπr²']),
    ('A circle has area 49π cm². What is its radius?', '7 cm', 'πr² = 49π, r² = 49.', ['49 cm', '24.5 cm', '14 cm']),
])
t72.fixed('C2', (2, 3), [
    ('Explain why the perimeter of a sector is not just its arc length.', 'The perimeter is the whole boundary: the arc plus the two radii.', 'B1 includes two radii; B1 formula arc + 2r [2]'),
    ('Explain why doubling the radius of a circle multiplies its area by 4.', 'Area = πr²; replacing r by 2r gives π(2r)² = 4πr².', 'B1 area depends on r²; B1 2² = 4 [2]'),
    ('Explain how the formula for arc length comes from the circumference.', 'A sector with angle θ is the fraction θ/360 of the full circle, so its arc is θ/360 of the circumference 2πr.', 'B1 fraction θ/360; B1 × 2πr [2]'),
])


@t72.add('C1', (1, 2, 3))
def t72_basic(r, D):
    rad = r.randint(3, 15)
    case = r.choice(['circ', 'area'] if D <= 1 else ['circ', 'area', 'arc', 'sector'])
    th = r.choice([30, 45, 60, 72, 90, 120, 135, 150, 240])
    if case == 'circ':
        c = 2 * PI * rad
        return MC(r, f'Find the circumference of a circle with radius {rad} cm, correct to 3 significant figures.', c, [PI * rad, PI * rad * rad, 2 * PI * rad * rad, 4 * PI * rad], f'2 × π × {rad} = {n3(c)} cm.', fmtf=lambda v: f'{n3(v)} cm')
    if case == 'area':
        c = PI * rad * rad
        return MC(r, f'Find the area of a circle with radius {rad} cm, correct to 3 significant figures.', c, [2 * PI * rad, PI * rad, PI * (2 * rad) ** 2, PI * rad * rad / 2], f'π × {rad}² = {n3(c)} cm².', fmtf=lambda v: f'{n3(v)} cm²')
    if case == 'arc':
        c = th / 360 * 2 * PI * rad
        return MC(r, f'A sector has radius {rad} cm and angle {th}°. Find the arc length, correct to 3 significant figures.', c, [th / 360 * PI * rad * rad, th / 180 * 2 * PI * rad, c + 2 * rad, th / 360 * PI * rad], f'{th}/360 × 2π × {rad} = {n3(c)} cm.', fmtf=lambda v: f'{n3(v)} cm')
    c = th / 360 * PI * rad * rad
    return MC(r, f'A sector has radius {rad} cm and angle {th}°. Find its area, correct to 3 significant figures.', c, [th / 360 * 2 * PI * rad, PI * rad * rad, th / 180 * PI * rad * rad, th / 360 * PI * rad], f'{th}/360 × π × {rad}² = {n3(c)} cm².', fmtf=lambda v: f'{n3(v)} cm²')


@t72.add('C3', (1, 2, 3, 4, 5))
def t72_sector(r, D):
    rad = r.choice([4, 5, 6, 7.5, 8, 9, 10, 12, 15])
    th = r.choice([40, 45, 60, 72, 80, 100, 120, 135, 150, 210, 240, 300])
    arc = th / 360 * 2 * PI * rad
    area = th / 360 * PI * rad ** 2
    if D <= 2:
        return Q(f'A sector of a circle has radius {ex(rad)} cm and angle {th}°. Calculate (a) the arc length and (b) the area of the sector.', f'(a) {n3(arc)} cm (b) {n3(area)} cm²',
                 f'(a) M1 {th}/360 × 2π × {ex(rad)}; A1 {n3(arc)} (b) M1 {th}/360 × π × {ex(rad)}²; A1 {n3(area)} [4]', type='multi_step')
    if D == 3:
        return Q(f'A sector of a circle has radius {ex(rad)} cm and angle {th}°. Calculate the perimeter of the sector.', f'{n3(arc + 2 * rad)} cm', f'M1 arc {n3(arc)}; M1 + 2 × {ex(rad)}; A1 {n3(arc + 2 * rad)} cm [3]')
    if D == 4:
        return Q(f'A sector of a circle with radius {ex(rad)} cm has an arc length of {n3(arc)} cm. Calculate the angle of the sector.', f'{th}°', f'M1 θ/360 × 2π × {ex(rad)} = {n3(arc)}; M1 θ = {n3(arc)} × 360 ÷ (2π × {ex(rad)}); A1 {th}° [3]')
    return Q(f'A sector has angle {th}° and area {n3(area)} cm². Calculate the radius of the sector and hence its arc length.', f'r = {ex(rad)} cm; arc {n3(arc)} cm',
             f'M1 {th}/360 × πr² = {n3(area)}; M1 r² = {n3(rad * rad)}; A1 r = {ex(rad)}; A1 arc {n3(arc)} [4]')


@t72.add('C3', (2, 3, 4))
def t72_ctx(r, D):
    nm = person(r)
    case = r.choice(['wheel', 'pizza', 'track'])
    if case == 'wheel':
        d = r.choice([55, 60, 65, 70, 72])
        dist = r.choice([500, 800, 1000, 1500, 2000])
        turns = dist * 100 / (PI * d)
        return Q(f'A bicycle wheel has diameter {d} cm. {nm} rides {dist} m. Calculate the number of complete turns the wheel makes.', str(math.floor(turns)), f'M1 circumference π × {d} = {n3(PI * d)} cm; M1 {dist * 100} ÷ {n3(PI * d)}; A1 {math.floor(turns)} [3]')
    if case == 'pizza':
        d = r.choice([24, 28, 30, 32, 36])
        k = r.choice([6, 8, 10, 12])
        return Q(f'A circular pizza of diameter {d} cm is cut into {k} equal slices. Calculate the area of one slice and the length of its curved crust.', f'{n3(PI * (d / 2) ** 2 / k)} cm²; {n3(PI * d / k)} cm',
                 f'M1 π × {ex(d / 2)}² ÷ {k}; A1 {n3(PI * (d / 2) ** 2 / k)}; M1 π × {d} ÷ {k}; A1 {n3(PI * d / k)} [4]')
    L, R = r.choice([80, 85, 100]), r.choice([30, 32, 36])
    per = 2 * L + 2 * PI * R
    return Q(f'A running track has two straight sections of {L} m joined by two semicircles of radius {R} m. Calculate the total length of one lap.', f'{n3(per)} m', f'M1 2 × {L}; M1 2π × {R}; A1 {n3(per)} m [3]')


@t72.add('C2', (2, 3, 4), 'explain')
def t72_err(r, D):
    nm = person(r)
    d = r.choice([8, 10, 12, 14, 16, 20])
    case = r.choice(['diam', 'per'])
    if case == 'diam':
        return Q(f'{nm} finds the area of a circle with diameter {d} cm as π × {d}² = {n3(PI * d * d)} cm². Explain the mistake and give the correct area.', f'{nm} used the diameter instead of the radius. Area = π × {d // 2}² = {n3(PI * (d / 2) ** 2)} cm².',
                 f'B1 radius = {d // 2}; B1 {n3(PI * (d / 2) ** 2)} cm² [2]')
    th = r.choice([60, 90, 120])
    rad = d // 2
    arc = th / 360 * 2 * PI * rad
    return Q(f'{nm} says the perimeter of a sector of radius {rad} cm and angle {th}° is {n3(arc)} cm. Explain what {nm} has forgotten and give the correct perimeter.', f'{nm} gave only the arc length; the two radii must be added: {n3(arc)} + 2 × {rad} = {n3(arc + 2 * rad)} cm.',
             f'B1 two radii missing; B1 {n3(arc + 2 * rad)} cm [2]')


def t72_c4(r, D):
    R = r.choice([6, 8, 10, 12])
    th = r.choice([60, 90, 120, 150])
    rr = R // 2
    big = th / 360 * PI * R * R
    small = th / 360 * PI * rr * rr
    intro = f'A garden design in {city(r)} is a sector of a circle with radius {R} m and angle {th}°. A smaller sector with the same centre and angle, but radius {rr} m, is a pond; the rest of the large sector is grass.'
    parts = [
        P('Calculate the area of the large sector.', f'{n3(big)} m²', f'M1 {th}/360 × π × {R}²; A1 {n3(big)}', 2),
        P('Calculate the area of grass.', f'{n3(big - small)} m²', f'M1 {th}/360 × π × {rr}²; M1 subtract; A1 {n3(big - small)}', 3),
        P('Calculate the perimeter of the grass region.', f'{n3(th / 360 * 2 * PI * (R + rr) + 2 * (R - rr))} m', f'M1 both arcs; M1 + 2 × {R - rr}; A1 {n3(th / 360 * 2 * PI * (R + rr) + 2 * (R - rr))}', 3),
        P('Explain why the area of the pond is one quarter of the area of the large sector.', f'The radius is halved, and area depends on r², so the area is multiplied by (½)² = ¼.', 'B1 area ∝ r²; B1 (½)² = ¼', 2),
    ]
    return cmp_(r, intro, parts)


t72.add('C4', (2, 3, 4, 5))(t72_c4)

# ---------------------------------------------------------------- nets and surface area
t73 = topic('Nets and surface area of prisms, cylinders, pyramids, cones and spheres', 'nets and surface area of prisms, cylinders, pyramids, cones and spheres', 'surface area', 'nets')
t73.fixed('C1', (1, 2), [
    ('How many faces does a triangular prism have?', '5', '2 triangles and 3 rectangles.', ['6', '9', '4']),
    ('The curved surface area of a cylinder of radius r and height h is', '2πrh', 'The curved surface opens out to a rectangle 2πr by h.', ['πr²h', 'πrh', '2πr²']),
    ('The surface area of a sphere of radius r is', '4πr²', 'Surface area of a sphere = 4πr².', ['4/3πr³', '2πr²', 'πr²']),
    ('The curved surface area of a cone with radius r and slant height l is', 'πrl', 'Curved surface area of a cone = πrl.', ['πr²l', '2πrl', '⅓πr²l']),
    ('Which net folds to make a square-based pyramid?', 'A square with four triangles, one on each side', 'The base is a square and each side face is a triangle.', ['Six squares in a cross shape', 'Two circles and a rectangle', 'Two triangles and three rectangles']),
    ('How many edges does a cuboid have?', '12', '4 on top, 4 on the bottom and 4 vertical.', ['6', '8', '24']),
])
t73.fixed('C2', (2, 3), [
    ('Explain why the curved surface of a cylinder has area 2πrh.', 'When unrolled it is a rectangle whose length is the circumference 2πr and whose width is the height h.', 'B1 unrolls to a rectangle; B1 dimensions 2πr and h [2]'),
    ('Explain the difference between the slant height and the perpendicular height of a cone.', 'The slant height is measured along the sloping surface from the apex to the edge of the base; the perpendicular height is measured straight down from the apex to the centre of the base.', 'B1 slant along surface; B1 perpendicular to base [2]'),
    ('Explain why the total surface area of a closed cylinder is 2πr² + 2πrh.', 'It has two circular ends, each πr², and a curved surface of area 2πrh.', 'B1 two circles; B1 curved surface [2]'),
])


@t73.add('C3', (1, 2, 3, 4, 5))
def t73_sa(r, D):
    shape = r.choice(['cuboid', 'cyl'] if D <= 2 else ['cyl', 'cone', 'sphere', 'prism', 'pyr'])
    if shape == 'cuboid':
        l, w, h = r.randint(3, 12), r.randint(2, 9), r.randint(2, 8)
        S = 2 * (l * w + l * h + w * h)
        return Q(f'Find the total surface area of a cuboid measuring {l} cm by {w} cm by {h} cm.', f'{S} cm²', f'M1 2({l}×{w} + {l}×{h} + {w}×{h}); A1 {S} cm² [2]')
    if shape == 'cyl':
        rad, h = r.choice([3, 4, 5, 6, 7, 2.5, 3.5]), r.choice([5, 8, 10, 12, 15])
        S = 2 * PI * rad * rad + 2 * PI * rad * h
        if D <= 2:
            return Q(f'Find the curved surface area of a cylinder with radius {ex(rad)} cm and height {h} cm.', f'{n3(2 * PI * rad * h)} cm²', f'M1 2π × {ex(rad)} × {h}; A1 {n3(2 * PI * rad * h)} [2]')
        return Q(f'A closed cylindrical tin has radius {ex(rad)} cm and height {h} cm. Calculate its total surface area.', f'{n3(S)} cm²', f'M1 2π × {ex(rad)}²; M1 2π × {ex(rad)} × {h}; A1 {n3(S)} cm² [3]')
    if shape == 'cone':
        rad, hh = r.choice([(3, 4), (5, 12), (6, 8), (8, 15), (9, 12), (7, 24)])
        l = math.isqrt(rad * rad + hh * hh)
        S = PI * rad * l + PI * rad * rad
        if D >= 4:
            return Q(f'A solid cone has base radius {rad} cm and perpendicular height {hh} cm. Calculate its total surface area.', f'{n3(S)} cm²', f'M1 l = √({rad}² + {hh}²) = {l}; M1 π × {rad} × {l} + π × {rad}²; A1 {n3(S)} cm² [3]')
        return Q(f'A solid cone has base radius {rad} cm and slant height {l} cm. Calculate its total surface area.', f'{n3(S)} cm²', f'M1 π × {rad} × {l}; M1 + π × {rad}²; A1 {n3(S)} cm² [3]')
    if shape == 'sphere':
        rad = r.choice([2, 3, 4.5, 5, 6, 7.5, 10])
        S = 4 * PI * rad * rad
        if D >= 4:
            return Q(f'A sphere has surface area {n3(S)} cm². Calculate its radius.', f'{ex(rad)} cm', f'M1 4πr² = {n3(S)}; M1 r = √({n3(S)} ÷ 4π); A1 {ex(rad)} cm [3]')
        return Q(f'Calculate the surface area of a ball of radius {ex(rad)} cm.', f'{n3(S)} cm²', f'M1 4π × {ex(rad)}²; A1 {n3(S)} [2]')
    if shape == 'prism':
        a, b = r.choice([(3, 4), (6, 8), (5, 12), (9, 12)])
        c = math.isqrt(a * a + b * b)
        L = r.randint(5, 20)
        S = a * b + (a + b + c) * L
        return Q(f'A triangular prism has a right-angled triangle cross-section with sides {a} cm, {b} cm and {c} cm, and length {L} cm. Calculate its total surface area.', f'{S} cm²',
                 f'M1 two triangles 2 × ½ × {a} × {b} = {a * b}; M1 rectangles ({a} + {b} + {c}) × {L} = {(a + b + c) * L}; A1 {S} cm² [3]')
    s_, sh = r.choice([(6, 5), (8, 5), (10, 13), (12, 10), (10, 12)])
    S = s_ * s_ + 4 * (s_ * sh / 2)
    return Q(f'A square-based pyramid has base edge {s_} cm. Each triangular face has a perpendicular height of {sh} cm. Calculate the total surface area.', f'{ex(S)} cm²', f'M1 base {s_ * s_}; M1 4 × ½ × {s_} × {sh}; A1 {ex(S)} cm² [3]')


@t73.add('C1', (1, 2, 3))
def t73_net(r, D):
    shape, faces, desc = r.choice([('cube', 6, 'six squares'), ('cuboid', 6, 'six rectangles in three equal pairs'), ('triangular prism', 5, 'two triangles and three rectangles'),
                                   ('square-based pyramid', 5, 'one square and four triangles'), ('tetrahedron', 4, 'four triangles'), ('cylinder', 3, 'two circles and a rectangle'), ('hexagonal prism', 8, 'two hexagons and six rectangles')])
    return MC(r, f'How many faces (including curved surfaces) does the net of a {shape} have?', faces, [faces + 1, faces - 1, faces + 2, faces * 2], f'The net of a {shape} is {desc}: {faces} faces.', fmtf=str)


@t73.add('C2', (2, 3, 4), 'explain')
def t73_err(r, D):
    nm = person(r)
    rad, h = r.choice([3, 4, 5, 6]), r.choice([8, 10, 12, 15])
    case = r.choice(['ends', 'cone'])
    if case == 'ends':
        return Q(f'{nm} calculates the total surface area of a closed cylinder with radius {rad} cm and height {h} cm as 2π × {rad} × {h} = {n3(2 * PI * rad * h)} cm². Explain what {nm} has missed and give the correct total.',
                 f'{nm} found only the curved surface; the two circular ends (2 × π × {rad}²) must be added: {n3(2 * PI * rad * h + 2 * PI * rad * rad)} cm².', f'B1 two circular ends; B1 {n3(2 * PI * rad * h + 2 * PI * rad * rad)} [2]')
    rr, hh = r.choice([(3, 4), (6, 8), (5, 12)])
    l = math.isqrt(rr * rr + hh * hh)
    return Q(f'A cone has radius {rr} cm and perpendicular height {hh} cm. {nm} uses πrl with l = {hh} to get the curved surface area {n3(PI * rr * hh)} cm². Explain the mistake and find the correct curved surface area.',
             f'l is the slant height, √({rr}² + {hh}²) = {l} cm, not the perpendicular height. Curved surface area = π × {rr} × {l} = {n3(PI * rr * l)} cm².', f'B1 slant height {l}; B1 {n3(PI * rr * l)} cm² [2]')


def t73_c4(r, D):
    rad = r.choice([3, 4, 5, 6])
    h = r.choice([8, 10, 12])
    intro = f'A solid toy is made from a cylinder of radius {rad} cm and height {h} cm with a hemisphere of radius {rad} cm fixed on top.'
    cyl = 2 * PI * rad * h + PI * rad * rad
    hemi = 2 * PI * rad * rad
    tot = cyl + hemi
    cost = r.choice([0.02, 0.05, 0.03])
    parts = [
        P('Calculate the curved surface area of the hemisphere.', f'{n3(hemi)} cm²', f'M1 ½ × 4π × {rad}²; A1 {n3(hemi)}', 2),
        P('Calculate the total surface area of the toy.', f'{n3(tot)} cm²', f'M1 curved cylinder 2π × {rad} × {h}; M1 + base π × {rad}² + hemisphere; A1 {n3(tot)}', 3),
        P(f'Paint costs ${ex(cost)} per cm². Find the cost of painting 50 toys, to the nearest dollar.', f'${round(tot * cost * 50)}', f'M1 {n3(tot)} × {ex(cost)} × 50; A1 ${round(tot * cost * 50)}', 2),
        P('Explain why the area of the top of the cylinder is not included.', 'It is covered by the flat face of the hemisphere, so it is not on the outside of the toy.', 'B1 hidden face', 1),
    ]
    return cmp_(r, intro, parts)


t73.add('C4', (2, 3, 4, 5))(t73_c4)

# ---------------------------------------------------------------- volume
t74 = topic('Volume of prisms, cylinders, pyramids, cones and spheres', 'volume of prisms, cylinders, pyramids, cones and spheres', 'volume', 'volume of cones spheres')
t74.fixed('C1', (1, 2), [
    ('The volume of a prism is', 'area of cross-section × length', 'V = A × l for any prism.', ['½ × base × height', 'perimeter × length', 'area of cross-section × 3']),
    ('The volume of a pyramid is', '⅓ × base area × perpendicular height', 'V = ⅓Ah.', ['½ × base area × height', 'base area × height', '⅓ × base perimeter × height']),
    ('The volume of a sphere of radius r is', '(4/3)πr³', 'V = 4/3 πr³.', ['4πr²', '(2/3)πr³', 'πr³']),
    ('How many cm³ are there in 1 litre?', '1000', '1 litre = 1000 cm³.', ['100', '10', '1 000 000']),
    ('A cone and a cylinder have the same base and height. How does the volume of the cone compare?', 'It is one third of the cylinder', 'V_cone = ⅓πr²h.', ['It is half', 'It is the same', 'It is two thirds']),
    ('The volume of a cylinder with radius 2 cm and height 5 cm, in terms of π, is', '20π cm³', 'π × 2² × 5 = 20π.', ['10π cm³', '40π cm³', '25π cm³']),
])
t74.fixed('C2', (2, 3), [
    ('Explain why a cylinder can be treated as a prism when finding its volume.', 'It has the same circular cross-section all the way along its length, so V = πr² × h.', 'B1 constant cross-section; B1 πr²h [2]'),
    ('Explain why doubling the radius of a cylinder (keeping the height) multiplies the volume by 4, but doubling the height only doubles it.', 'V = πr²h: r is squared, so ×2 in r gives ×4; h is to the power 1, so ×2 in h gives ×2.', 'B1 r²; B1 h to power 1 [2]'),
    ('Explain why volume is measured in cubic units.', 'Volume measures three-dimensional space, found by multiplying three lengths together.', 'B1 three dimensions; B1 length × length × length [2]'),
])


@t74.add('C1', (1, 2, 3))
def t74_q(r, D):
    shape = r.choice(['cyl', 'cone', 'sphere', 'pyr'] if D >= 2 else ['cuboid', 'cyl'])
    if shape == 'cuboid':
        l, w, h = r.randint(2, 12), r.randint(2, 9), r.randint(2, 8)
        c = l * w * h
        return MC(r, f'Find the volume of a cuboid {l} cm by {w} cm by {h} cm.', c, [2 * (l * w + l * h + w * h), l + w + h, l * w, c / 2], f'{l} × {w} × {h} = {c} cm³.', fmtf=lambda v: f'{ex(v)} cm³')
    rad, h = r.choice([2, 3, 4, 5, 6]), r.choice([3, 6, 9, 12])
    if shape == 'cyl':
        c = rad * rad * h
        return MC(r, f'Find the volume of a cylinder of radius {rad} cm and height {h} cm, leaving your answer in terms of π.', c, [2 * rad * h, rad * h, c / 3, 2 * rad * rad * h], f'π × {rad}² × {h} = {c}π cm³.', fmtf=lambda v: f'{ex(v)}π cm³')
    if shape == 'cone':
        c = rad * rad * h / 3
        return MC(r, f'Find the volume of a cone of radius {rad} cm and perpendicular height {h} cm, leaving your answer in terms of π.', c, [rad * rad * h, rad * h / 3, rad * rad * h / 2, 2 * rad * h], f'⅓ × π × {rad}² × {h} = {ex(c)}π cm³.', fmtf=lambda v: f'{ex(v)}π cm³')
    if shape == 'sphere':
        rad = r.choice([3, 6, 9])
        c = Fr(4, 3) * rad ** 3
        return MC(r, f'Find the volume of a sphere of radius {rad} cm, leaving your answer in terms of π.', c, [4 * rad * rad, Fr(4, 3) * rad * rad, 4 * rad ** 3, Fr(2, 3) * rad ** 3], f'4/3 × π × {rad}³ = {num(c)}π cm³.', fmtf=lambda v: f'{num(v)}π cm³')
    b, h = r.choice([3, 6, 9]), r.choice([4, 5, 10])
    c = b * b * h / 3
    return MC(r, f'A square-based pyramid has base edge {b} cm and perpendicular height {h} cm. Find its volume.', c, [b * b * h, b * b * h / 2, b * h / 3, 4 * b * h], f'⅓ × {b}² × {h} = {ex(c)} cm³.', fmtf=lambda v: f'{ex(v)} cm³')


@t74.add('C3', (1, 2, 3, 4, 5))
def t74_vol(r, D):
    shape = r.choice(['prism', 'cyl'] if D <= 2 else ['cyl', 'cone', 'sphere', 'hemi', 'pyr'])
    if shape == 'prism':
        a, b, h = r.randint(3, 10), r.randint(6, 14), r.randint(3, 8)
        L = r.randint(5, 20)
        A = (a + b) * h / 2
        return Q(f'A prism has a trapezium cross-section with parallel sides {a} cm and {b} cm and height {h} cm. The prism is {L} cm long. Find its volume.', f'{ex(A * L)} cm³', f'M1 ½({a} + {b}) × {h} = {ex(A)}; A1 × {L} = {ex(A * L)} cm³ [2]')
    if shape == 'cyl':
        rad, h = r.choice([2.5, 3, 4, 5, 6.5, 7]), r.choice([8, 10, 12, 15, 20])
        V = PI * rad * rad * h
        if D >= 4:
            cap = float(n3(V / 1000))
            hh = cap * 1000 / (PI * rad * rad)
            return Q(f'A cylindrical can holds {ex(cap)} litres. Its radius is {ex(rad)} cm. Calculate its height, correct to 3 significant figures.', f'{n3(hh)} cm', f'B1 {ex(cap)} litres = {ex(cap * 1000)} cm³; M1 π × {ex(rad)}² × h = {ex(cap * 1000)}; A1 h = {n3(hh)} cm [3]')
        return Q(f'Calculate the volume of a cylinder with radius {ex(rad)} cm and height {h} cm.', f'{n3(V)} cm³', f'M1 π × {ex(rad)}² × {h}; A1 {n3(V)} cm³ [2]')
    if shape == 'cone':
        rad, h = r.choice([3, 4, 5, 6, 7.5]), r.choice([6, 8, 10, 12])
        V = PI * rad * rad * h / 3
        return Q(f'Calculate the volume of a cone with base radius {ex(rad)} cm and perpendicular height {h} cm.', f'{n3(V)} cm³', f'M1 ⅓ × π × {ex(rad)}² × {h}; A1 {n3(V)} cm³ [2]')
    if shape == 'sphere':
        rad = r.choice([2, 3.5, 4, 5, 6, 7.5])
        V = 4 / 3 * PI * rad ** 3
        if D >= 4:
            return Q(f'A sphere has volume {n3(V)} cm³. Calculate its radius.', f'{ex(rad)} cm', f'M1 4/3 πr³ = {n3(V)}; M1 r³ = {n3(rad ** 3)}; A1 r = {ex(rad)} cm [3]')
        return Q(f'Calculate the volume of a sphere of radius {ex(rad)} cm.', f'{n3(V)} cm³', f'M1 4/3 × π × {ex(rad)}³; A1 {n3(V)} [2]')
    if shape == 'hemi':
        rad = r.choice([3, 4, 5, 6, 9])
        V = 2 / 3 * PI * rad ** 3
        return Q(f'A bowl is a hemisphere with internal radius {rad} cm. Calculate how many litres of water it holds when full.', f'{n3(V / 1000)} litres', f'M1 ½ × 4/3 × π × {rad}³ = {n3(V)} cm³; M1 ÷ 1000; A1 {n3(V / 1000)} litres [3]')
    b, h = r.randint(4, 12), r.randint(5, 15)
    V = b * b * h / 3
    return Q(f'A square-based pyramid has volume {ex(V)} cm³ and base edge {b} cm. Find its perpendicular height.', f'{h} cm', f'M1 ⅓ × {b}² × h = {ex(V)}; A1 h = {h} [2]')


@t74.add('C3', (3, 4, 5))
def t74_melt(r, D):
    nm = person(r)
    R = r.choice([6, 9, 12])
    rr = r.choice([1, 1.5, 2, 3])
    n = (R / rr) ** 3
    if n != int(n):
        return None
    if D <= 3:
        return Q(f'A solid metal sphere of radius {R} cm is melted down and recast into small spheres of radius {ex(rr)} cm. How many small spheres can be made?', str(int(n)), f'M1 4/3π{R}³ ÷ 4/3π{ex(rr)}³; M1 = ({R}/{ex(rr)})³; A1 {int(n)} [3]')
    rad, h = r.choice([5, 6, 8]), r.choice([10, 12, 15])
    V = PI * rad * rad * h
    rs = (V * 3 / (4 * PI)) ** (1 / 3)
    return Q(f'A solid cylinder of radius {rad} cm and height {h} cm is melted and made into a single sphere. Calculate the radius of the sphere.', f'{n3(rs)} cm', f'M1 V = π × {rad}² × {h} = {n3(V)}; M1 4/3πr³ = {n3(V)}; A1 r = {n3(rs)} cm [3]')


@t74.add('C2', (2, 3, 4), 'explain')
def t74_err(r, D):
    nm = person(r)
    rad, h = r.choice([3, 4, 5, 6]), r.choice([6, 9, 12])
    case = r.choice(['cone', 'litre'])
    if case == 'cone':
        return Q(f'{nm} calculates the volume of a cone with radius {rad} cm and height {h} cm as π × {rad}² × {h} = {n3(PI * rad * rad * h)} cm³. Explain the mistake and give the correct volume.',
                 f'{nm} has found the volume of a cylinder; a cone is one third of this: {n3(PI * rad * rad * h / 3)} cm³.', f'B1 missing ⅓; B1 {n3(PI * rad * rad * h / 3)} cm³ [2]')
    V = PI * rad * rad * h
    return Q(f'A cylinder has volume {n3(V)} cm³. {nm} says it holds {n3(V / 100)} litres. Explain the mistake and give the correct capacity.', f'1 litre = 1000 cm³, not 100 cm³, so it holds {n3(V / 1000)} litres.', f'B1 1000 cm³ per litre; B1 {n3(V / 1000)} litres [2]')


def t74_c4(r, D):
    rad = r.choice([3, 4, 5])
    h = r.choice([10, 12, 15])
    ch = r.choice([4, 6, 8])
    intro = f'An ice-cream container is made of a cylinder of radius {rad} cm and height {h} cm, with a cone of the same radius and height {ch} cm joined to the bottom.'
    vc, vk = PI * rad * rad * h, PI * rad * rad * ch / 3
    l = math.sqrt(rad * rad + ch * ch)
    scoop = r.choice([2, 2.5])
    vs = 4 / 3 * PI * scoop ** 3
    parts = [
        P('Calculate the volume of the cylinder.', f'{n3(vc)} cm³', f'M1 π × {rad}² × {h}; A1 {n3(vc)}', 2),
        P('Calculate the total volume of the container.', f'{n3(vc + vk)} cm³', f'M1 π × {rad}² × {h} + ⅓ × π × {rad}² × {ch}; A1 {n3(vc + vk)}', 2),
        P(f'Ice cream is served in spherical scoops of radius {ex(scoop)} cm. Find how many complete scoops can be served from a full container.', str(math.floor((vc + vk) / vs + 1e-9)), f'M1 4/3 π × {ex(scoop)}³ = {n3(vs)}; M1 divide; A1 {math.floor((vc + vk) / vs + 1e-9)}', 3),
        P('Calculate the slant height of the cone.', f'{n3(l)} cm', f'M1 √({rad}² + {ch}²); A1 {n3(l)}', 2),
        P('Express the total volume in litres.', f'{n3((vc + vk) / 1000)} litres', 'B1 ÷ 1000', 1),
    ]
    return cmp_(r, intro, parts)


t74.add('C4', (2, 3, 4, 5))(t74_c4)
CHAPTERS[7] = [t71, t72, t73, t74]


# =========================================================== 8 Introduction to probability
BAGS = [('red', 'blue', 'green', 'yellow'), ('black', 'white', 'grey', 'purple')]
ITEMS = [('counters', 'bag'), ('marbles', 'jar'), ('beads', 'box'), ('balls', 'bag'), ('sweets', 'tin')]

t81 = topic('Basic probability and the probability scale', 'basic probability and the probability scale', 'probability scale', 'basic probability')
t81.fixed('C1', (1, 2), [
    ('Which word describes an event with probability 0?', 'Impossible', 'P = 0 means the event cannot happen.', ['Certain', 'Unlikely', 'Even chance']),
    ('A fair six-sided dice is rolled. What is the probability of rolling a number greater than 4?', '1/3', 'Outcomes 5 and 6: 2/6 = 1/3.', ['1/2', '2/3', '1/6']),
    ('The probability that it rains tomorrow is 0.35. What is the probability that it does not rain?', '0.65', 'P(not A) = 1 − P(A).', ['0.35', '0.75', '1.35']),
    ('Which of these cannot be a probability?', '1.2', 'Probabilities lie between 0 and 1 inclusive.', ['0', '0.99', '3/4']),
    ('A fair coin is tossed. What is the probability of a head?', '1/2', 'Two equally likely outcomes.', ['1', '0', '1/4']),
    ('Events that cannot happen at the same time are called', 'mutually exclusive', 'For example rolling a 2 and rolling a 5 on one roll.', ['independent', 'certain', 'equally likely']),
    ('A card is taken at random from a pack of 52 playing cards. What is the probability that it is a heart?', '1/4', '13 hearts out of 52 = 1/4.', ['1/13', '1/52', '1/2']),
])
t81.fixed('C2', (2, 3), [
    ('Explain why the probabilities of all the possible outcomes of an experiment add up to 1.', 'One of the outcomes is certain to happen, and they cannot happen together, so their probabilities together give a certain event, probability 1.', 'B1 one outcome certain; B1 mutually exclusive, total 1 [2]'),
    ('Explain what is meant by "outcomes are equally likely", using a fair dice.', 'Each outcome has the same chance of happening; on a fair dice each number 1–6 has probability 1/6.', 'B1 same chance; B1 example 1/6 [2]'),
    ('A spinner has red, blue and green sections. Explain why P(red) is not necessarily 1/3.', 'The sections may be different sizes, so the three outcomes need not be equally likely.', 'B1 sections may not be equal; B1 not equally likely [2]'),
])


@t81.add('C1', (1, 2, 3))
def t81_bag(r, D):
    cols = r.choice(BAGS)
    k = 3 if D <= 2 else 4
    ns = [r.randint(2, 9) for _ in range(k)]
    tot = sum(ns)
    it, cont = r.choice(ITEMS)
    desc = ', '.join(f'{n} {c}' for n, c in zip(ns, cols[:k]))
    i = r.randrange(k)
    if D <= 2:
        c = Fr(ns[i], tot)
        return MC(r, f'A {cont} contains {desc} {it}. One is taken at random. Find the probability that it is {cols[i]}.', c, [Fr(ns[i], tot - ns[i]), Fr(1, k), Fr(tot - ns[i], tot), Fr(ns[i], tot + 1)], f'{ns[i]} {cols[i]} out of {tot}: {num(c)}.')
    c = Fr(tot - ns[i], tot)
    return MC(r, f'A {cont} contains {desc} {it}. One is taken at random. Find the probability that it is not {cols[i]}.', c, [Fr(ns[i], tot), Fr(k - 1, k), Fr(tot - ns[i], tot - 1), Fr(1, tot)], f'1 − {ns[i]}/{tot} = {num(c)}.')


@t81.add('C3', (1, 2, 3, 4, 5))
def t81_table(r, D):
    outs = r.choice([['red', 'blue', 'green', 'yellow'], ['A', 'B', 'C', 'D'], ['1', '2', '3', '4', '5']])
    ps = [Fr(r.randint(5, 30), 100) for _ in outs[:-1]]
    if sum(ps) >= 1:
        return None
    if D >= 4:
        # two unknowns x and 2x
        rest = 1 - sum(ps[:-1])
        x = rest / 3
        tbl = ', '.join(f'{o}: {ex(float(p))}' for o, p in zip(outs[:-2], ps[:-1])) + f', {outs[-2]}: x, {outs[-1]}: 2x'
        if (x * 1000).denominator != 1:
            return None
        return Q(f'A biased spinner has these probabilities: {tbl}. Find the value of x and the probability that the spinner lands on {outs[-1]}{" or " + outs[0] if D == 5 else ""}.',
                 f'x = {ex(float(x))}; P({outs[-1]}{" or " + outs[0] if D == 5 else ""}) = {ex(float(2 * x + (ps[0] if D == 5 else 0)))}',
                 f'M1 {ex(float(sum(ps[:-1])))} + 3x = 1; A1 x = {ex(float(x))}; A1 {ex(float(2 * x + (ps[0] if D == 5 else 0)))} [3]')
    last = 1 - sum(ps)
    tbl = ', '.join(f'{o}: {ex(float(p))}' for o, p in zip(outs, ps)) + f', {outs[-1]}: ?'
    if D <= 2:
        return Q(f'A biased spinner has these probabilities: {tbl}. Find the probability that it lands on {outs[-1]}.', ex(float(last)), f'M1 1 − ({" + ".join(ex(float(p)) for p in ps)}); A1 {ex(float(last))} [2]')
    j = r.randrange(len(ps))
    return Q(f'A biased spinner has these probabilities: {tbl}. Find the probability that it lands on {outs[-1]}, and the probability that it does not land on {outs[j]}.', f'{ex(float(last))}; {ex(float(1 - ps[j]))}',
             f'M1 1 − sum; A1 {ex(float(last))}; B1 1 − {ex(float(ps[j]))} = {ex(float(1 - ps[j]))} [3]')


@t81.add('C3', (2, 3, 4))
def t81_ratio(r, D):
    it, cont = r.choice(ITEMS)
    a, b = r.randint(1, 5), r.randint(2, 7)
    k = r.randint(3, 8)
    if math.gcd(a, b) != 1:
        return None
    c1, c2 = r.sample(BAGS[0], 2)
    if D <= 2:
        return Q(f'A {cont} contains only {c1} and {c2} {it} in the ratio {a} : {b}. One is taken at random. Find the probability that it is {c1}.', num(Fr(a, a + b)), f'M1 {a} out of {a + b} parts; A1 {num(Fr(a, a + b))} [2]')
    n = (a + b) * k
    add = r.randint(2, 6)
    return Q(f'A {cont} contains {n} {it}, only {c1} and {c2}, in the ratio {a} : {b}. {add} more {c1} {it} are added. Find the probability that an {it[:-1]} taken at random is now {c1}.' if it[0] in 'aeiou' else
             f'A {cont} contains {n} {it}, only {c1} and {c2}, in the ratio {a} : {b}. {add} more {c1} {it} are added. Find the probability that one taken at random is now {c1}.', num(Fr(a * k + add, n + add)),
             f'M1 {c1} = {a * k}; M1 ({a * k} + {add})/({n} + {add}); A1 {num(Fr(a * k + add, n + add))} [3]')


@t81.add('C2', (2, 3, 4), 'explain')
def t81_err(r, D):
    nm = person(r)
    case = r.choice(['two', 'sum', 'bias'])
    if case == 'two':
        return Q(f'{nm} says: "Tomorrow it will either snow or not snow, so the probability that it snows is 1/2." Explain why {nm} is wrong.', 'The two outcomes are not equally likely, so the probability is not necessarily 1/2; it depends on the place and the season.', 'B1 outcomes not equally likely; B1 context [2]')
    if case == 'sum':
        a, b = r.choice([(0.4, 0.7), (0.55, 0.6), (0.3, 0.8), (0.45, 0.65)])
        return Q(f'A spinner can land on A or B only. {nm} says P(A) = {ex(a)} and P(B) = {ex(b)}. Explain why this cannot be correct.', f'The outcomes are mutually exclusive and exhaustive, so the probabilities must add to 1, but {ex(a)} + {ex(b)} = {ex(round(a + b, 2))}.',
                 f'B1 must add to 1; B1 shows sum {ex(round(a + b, 2))} [2]')
    n = r.choice([5, 6, 8])
    return Q(f'{nm} rolls a dice and gets {n} sixes in a row. {nm} says a six is less likely on the next roll because "it is due to be something else". Explain why {nm} is wrong if the dice is fair.', 'Each roll is independent; the dice has no memory, so P(six) is still 1/6 on the next roll.', 'B1 independent rolls; B1 probability still 1/6 [2]')


def t81_c4(r, D):
    it, cont = r.choice(ITEMS)
    c1, c2, c3 = r.sample(BAGS[0], 3)
    a, b = r.randint(3, 9), r.randint(2, 8)
    pc = r.choice([Fr(1, 4), Fr(1, 3), Fr(2, 5), Fr(1, 5)])
    # P(c3) = pc -> n3 = pc*(a+b+n3) -> n3 = pc(a+b)/(1-pc)
    n3_ = pc * (a + b) / (1 - pc)
    if n3_.denominator != 1:
        return None
    n3_ = int(n3_)
    tot = a + b + n3_
    intro = f'A {cont} contains {a} {c1} {it}, {b} {c2} {it} and some {c3} {it}. The probability of taking a {c3} one at random is {num(pc)}.'
    parts = [
        P(f'Find the number of {c3} {it}.', str(n3_), f'M1 {num(pc)} of the total = n; M1 n = {num(pc)}({a + b} + n); A1 {n3_}', 3),
        P(f'Find the probability of taking a {c1} one.', num(Fr(a, tot)), f'B1 {a}/{tot}', 1),
        P(f'Find the probability of taking one that is not {c2}.', num(Fr(tot - b, tot)), f'B1 1 − {b}/{tot}', 1),
        P(f'Mark the probability of taking a {c1} one on a probability scale and describe its likelihood in words.', f'{ex(round(a / tot, 2))} on the scale; {"unlikely" if a / tot < 0.5 else ("even chance" if a * 2 == tot else "likely")}', 'B1 position; B1 word', 2),
        P(f'How many {c1} {it} must be added so that the probability of taking a {c1} one is 1/2?', str(tot - 2 * a), f'M1 ({a} + k)/({tot} + k) = 1/2; A1 k = {tot - 2 * a}', 2) if tot > 2 * a else
        P(f'How many {c2} {it} must be removed so that the probability of taking a {c1} one is 1/2?', str(2 * a - tot), f'M1 {a}/({tot} − k) = 1/2; A1 k = {2 * a - tot}', 2) if 0 < 2 * a - tot <= b else
        P(f'Find the probability of taking a {c1} or a {c3} one.', num(Fr(a + n3_, tot)), f'B1 {a + n3_}/{tot}', 1),
    ]
    return cmp_(r, intro, parts)


t81.add('C4', (2, 3, 4, 5))(t81_c4)

# ---------------------------------------------------------------- relative and expected frequency
t82 = topic('Relative frequency and expected frequency', 'relative frequency and expected frequency', 'relative frequency', 'expected frequency')
t82.fixed('C1', (1, 2), [
    ('A drawing pin is dropped 200 times and lands point up 64 times. What is the relative frequency of landing point up?', '0.32', '64 ÷ 200 = 0.32.', ['0.64', '0.68', '64']),
    ('A fair dice is rolled 300 times. How many sixes would you expect?', '50', '300 × 1/6 = 50.', ['6', '60', '30']),
    ('Relative frequency gives a better estimate of probability when', 'the number of trials is larger', 'More trials reduce the effect of chance variation.', ['the number of trials is smaller', 'the experiment is done once', 'the results are rounded']),
    ('Relative frequency is calculated as', 'number of successes ÷ number of trials', 'It is the proportion of trials that are successful.', ['number of trials ÷ number of successes', 'successes × trials', 'successes − failures']),
])
t82.fixed('C2', (2, 3), [
    ('Explain the difference between theoretical probability and relative frequency.', 'Theoretical probability is worked out from equally likely outcomes; relative frequency is an estimate found from the results of an experiment.', 'B1 theoretical from outcomes; B1 relative frequency from experiment [2]'),
    ('Explain why a fair coin tossed 10 times may not give exactly 5 heads.', 'Results vary by chance; 5 heads is only the expected number, and over a small number of trials the actual result can differ.', 'B1 chance variation; B1 expected not guaranteed [2]'),
    ('Explain how relative frequency could show that a dice is biased.', 'Roll it many times; if the relative frequency of a number settles far from 1/6, the dice is likely to be biased.', 'B1 many trials; B1 compare with 1/6 [2]'),
])


@t82.add('C1', (1, 2, 3))
def t82_exp(r, D):
    p = r.choice([Fr(1, 4), Fr(1, 5), Fr(2, 5), Fr(3, 10), Fr(1, 8), Fr(3, 8), Fr(0.15).limit_denominator(100), Fr(0.35).limit_denominator(100)])
    n = r.choice([n for n in (40, 80, 120, 160, 200, 240, 400, 500, 600) if (p * n).denominator == 1])
    c = p * n
    ctx = r.choice(['a spinner lands on red', 'a seed germinates', 'a light bulb is faulty', 'a train is late', 'a patient has a side effect'])
    return MC(r, f'The probability that {ctx} is {num(p) if D <= 2 else ex(float(p))}. Out of {n} trials, how many times would you expect this to happen?', c, [n * (1 - p), n / p.denominator, c + 10, p * 100], f'Expected frequency = {num(p)} × {n} = {num(c)}.', fmtf=lambda v: num(Fr(v).limit_denominator(1000)))


@t82.add('C3', (1, 2, 3, 4, 5))
def t82_rf(r, D):
    nm = person(r)
    outs = ['1', '2', '3', '4', '5', '6']
    n = r.choice([60, 120, 150, 200, 300])
    for _ in range(30):
        f = [r.randint(n // 10, n // 4) for _ in range(5)]
        if sum(f) < n - 5:
            f.append(n - sum(f))
            break
    else:
        return None
    tbl = ', '.join(f'{o}: {x}' for o, x in zip(outs, f))
    i = r.randrange(6)
    rf = Fr(f[i], n)
    if D <= 2:
        return Q(f'{nm} rolls a dice {n} times. The results are {tbl}. Find the relative frequency of rolling a {outs[i]}.', f'{num(rf)} (= {ex(round(float(rf), 3))})', f'M1 {f[i]} ÷ {n}; A1 {num(rf)} [2]')
    N = r.choice([600, 900, 1200, 1500])
    exp = float(rf) * N
    if D == 3:
        return Q(f'{nm} rolls a dice {n} times. The results are {tbl}. Use the results to estimate how many times a {outs[i]} would be rolled in {N} rolls.', ex(round(exp, 1)), f'M1 {f[i]}/{n} × {N}; A1 {ex(round(exp, 1))} [2]')
    j = max(range(6), key=lambda k: abs(f[k] / n - 1 / 6))
    return Q(f'{nm} rolls a dice {n} times. The results are {tbl}. (a) Find the relative frequency of the score whose result is furthest from what you would expect for a fair dice. (b) Is there evidence that the dice is biased? Give a reason.',
             f'(a) {outs[j]}: {num(Fr(f[j], n))} ≈ {ex(round(f[j] / n, 3))} (b) {"Yes" if abs(f[j] / n - 1 / 6) > 0.06 else "Not strong evidence"}: expected relative frequency 1/6 ≈ 0.167 for each score; {outs[j]} differs by {ex(round(abs(f[j] / n - 1 / 6), 3))}.',
             f'(a) M1 {f[j]}/{n}; A1 (b) B1 compares with 1/6; B1 conclusion considering number of trials [4]', type='multi_step')


@t82.add('C3', (2, 3, 4))
def t82_ctx(r, D):
    nm = person(r)
    ctx = r.choice([('cars passing a school', 'red', 'cars'), ('customers in a café', 'order tea', 'customers'), ('seeds that were planted', 'germinate', 'seeds'), ('students in a survey', 'walk to school', 'students')])
    n = r.choice([50, 80, 120, 200, 250])
    k = r.randint(int(n * 0.15), int(n * 0.6))
    N = r.choice([1000, 1500, 2000, 3000])
    return Q(f'{nm} records {n} {ctx[0]} and finds that {k} {ctx[1]}. Estimate the probability that the next one will {ctx[1]}, and estimate how many out of {N} {ctx[2]} would {ctx[1]}.' if ctx[1][0] not in 'r' else
             f'{nm} records {n} {ctx[0]} and finds that {k} are {ctx[1]}. Estimate the probability that the next car is {ctx[1]}, and estimate how many of the next {N} {ctx[2]} would be {ctx[1]}.',
             f'{num(Fr(k, n))}; about {round(k / n * N)}', f'B1 {k}/{n} = {num(Fr(k, n))}; M1 × {N}; A1 {round(k / n * N)} [3]')


@t82.add('C2', (2, 3, 4), 'explain')
def t82_err(r, D):
    nm = person(r)
    n, k = r.choice([(10, 4), (12, 5), (8, 1), (20, 9)])
    return Q(f'{nm} spins a spinner {n} times and gets red {k} times. {nm} says the probability of red is exactly {num(Fr(k, n))}. Explain why this is only an estimate and how it could be improved.',
             f'{num(Fr(k, n))} is a relative frequency from only {n} trials; results vary by chance. Spin it many more times (e.g. 500) for a more reliable estimate.', 'B1 relative frequency/estimate from few trials; B1 more trials [2]')


def t82_c4(r, D):
    nm = person(r)
    n1, n2, n3_ = 50, 200, 500
    p = r.choice([0.2, 0.25, 0.3, 0.35, 0.4])
    k1, k2, k3 = round(n1 * p) + r.choice([-3, 2, 4]), round(n2 * p) + r.choice([-6, 5, 8]), round(n3_ * p) + r.choice([-4, 3, 6])
    intro = f'{nm} drops a paper cup and records whether it lands on its side. After 50 drops it landed on its side {k1} times, after 200 drops {k2} times and after 500 drops {k3} times.'
    parts = [
        P('Calculate the relative frequency of landing on its side after each set of drops.', f'{ex(k1 / 50)}, {ex(k2 / 200)}, {ex(k3 / 500)}', 'B2 all three (B1 for two)', 2),
        P('Which relative frequency gives the best estimate of the probability? Explain why.', f'{ex(k3 / 500)}, because it is based on the most trials.', 'B1 500 drops; B1 more trials more reliable', 2),
        P('Estimate the number of times the cup would land on its side in 2000 drops.', ex(round(k3 / 500 * 2000)), f'M1 {ex(k3 / 500)} × 2000; A1 {ex(round(k3 / 500 * 2000))}', 2),
        P('Estimate the probability that the cup does not land on its side.', ex(round(1 - k3 / 500, 3)), f'B1 1 − {ex(k3 / 500)}', 1),
    ]
    return cmp_(r, intro, parts)


t82.add('C4', (2, 3, 4, 5))(t82_c4)

# ---------------------------------------------------------------- sample spaces
t83 = topic('Probability of combined events using sample space diagrams', 'probability of combined events using sample space diagrams', 'sample space diagrams', 'combined events')
t83.fixed('C1', (1, 2), [
    ('Two fair coins are tossed. How many outcomes are in the sample space?', '4', 'HH, HT, TH, TT.', ['2', '3', '8']),
    ('Two fair dice are rolled. How many outcomes are in the sample space?', '36', '6 × 6 = 36.', ['12', '6', '18']),
    ('Two fair dice are rolled. What is the probability that both show a 6?', '1/36', 'Only (6, 6) out of 36.', ['1/6', '1/12', '2/36']),
    ('Two fair coins are tossed. What is the probability of exactly one head?', '1/2', 'HT and TH: 2 of 4.', ['1/4', '1/3', '3/4']),
    ('Two fair dice are rolled and the scores added. Which total is most likely?', '7', 'Six of the 36 outcomes give 7.', ['6', '12', '2']),
])
t83.fixed('C2', (2, 3), [
    ('Explain why the totals of two dice are not equally likely, even though each dice is fair.', 'Different totals can be made in different numbers of ways: 7 can be made in 6 ways but 2 only in 1 way, out of 36 equally likely pairs.', 'B1 different numbers of combinations; B1 example [2]'),
    ('Explain why a sample space diagram is useful for combined events.', 'It lists every equally likely outcome systematically, so none are missed and probabilities can be counted.', 'B1 lists all outcomes; B1 count favourable/total [2]'),
    ('Explain why HT and TH are counted as different outcomes when two coins are tossed.', 'The coins are distinct (first and second), so a head on the first and tail on the second is a different outcome from the reverse; this gives 4 equally likely outcomes.', 'B1 coins distinguishable; B1 4 equally likely [2]'),
])


def two_dice_count(cond, a=6, b=6):
    return sum(1 for i in range(1, a + 1) for j in range(1, b + 1) if cond(i, j))


CONDS = [('the total is {k}', lambda k: (lambda i, j: i + j == k), range(3, 12)),
         ('the total is greater than {k}', lambda k: (lambda i, j: i + j > k), range(6, 11)),
         ('the product is {k}', lambda k: (lambda i, j: i * j == k), [4, 6, 12]),
         ('the difference between the scores is {k}', lambda k: (lambda i, j: abs(i - j) == k), range(0, 5)),
         ('at least one score is {k}', lambda k: (lambda i, j: i == k or j == k), range(1, 7)),
         ('both scores are even', lambda k: (lambda i, j: i % 2 == 0 and j % 2 == 0), [0]),
         ('the product is odd', lambda k: (lambda i, j: (i * j) % 2 == 1), [0])]


@t83.add('C1', (1, 2, 3))
def t83_dice(r, D):
    txt, mk, ks = r.choice(CONDS)
    k = r.choice(list(ks))
    n = two_dice_count(mk(k))
    c = Fr(n, 36)
    return MC(r, f'Two fair six-sided dice are rolled. Find the probability that {txt.format(k=k)}.', c, [Fr(n, 12) if n < 12 else Fr(1, 6), Fr(n + 1, 36), Fr(36 - n, 36), Fr(1, 6) if c != Fr(1, 6) else Fr(1, 3)], f'{n} of the 36 equally likely outcomes: {num(c)}.')


@t83.add('C3', (1, 2, 3, 4, 5))
def t83_spin(r, D):
    a = r.choice([3, 4, 5])
    b = r.choice([4, 6]) if D >= 3 else 6
    nm = person(r)
    op = r.choice(['sum', 'product']) if D >= 3 else 'sum'
    vals = {}
    for i in range(1, a + 1):
        for j in range(1, b + 1):
            v = i + j if op == 'sum' else i * j
            vals[v] = vals.get(v, 0) + 1
    tot = a * b
    k = r.choice(sorted(vals))
    if D <= 2:
        return Q(f'{nm} spins a fair spinner numbered 1 to {a} and rolls a fair dice numbered 1 to {b}, and adds the two scores. Draw a sample space diagram and find the probability that the total is {k}.', num(Fr(vals[k], tot)),
                 f'M1 {tot} outcomes listed; A1 {vals[k]}/{tot} = {num(Fr(vals[k], tot))} [2]')
    thr = r.choice(sorted(vals)[len(vals) // 3: 2 * len(vals) // 3])
    more = sum(c for v, c in vals.items() if v > thr)
    stem = f'{nm} spins a fair spinner numbered 1 to {a} and a fair spinner numbered 1 to {b}, and finds the {op} of the two scores. Find the probability that the {op} is (a) {k} (b) greater than {thr}.'
    ans = f'(a) {num(Fr(vals[k], tot))} (b) {num(Fr(more, tot))}'
    key = f'M1 sample space of {tot} outcomes; (a) A1 {vals[k]}/{tot} (b) A1 {more}/{tot}'
    if D >= 4:
        N = r.choice([60, 120, 180, 240])
        if (N * more) % tot == 0:
            stem += f' (c) The game is played {N} times. How many times would you expect the {op} to be greater than {thr}?'
            ans += f' (c) {N * more // tot}'
            key += f' (c) B1 {N * more // tot}'
            return Q(stem, ans, key + ' [4]', type='multi_step')
    return Q(stem, ans, key + ' [3]', type='multi_step')


@t83.add('C2', (2, 3, 4), 'explain')
def t83_err(r, D):
    nm = person(r)
    case = r.choice(['totals', 'coins'])
    if case == 'totals':
        k = r.choice([2, 3, 4, 11, 12, 5])
        return Q(f'{nm} says that when two dice are rolled, the probability of a total of {k} is 1/11 because there are 11 possible totals (2 to 12). Explain why {nm} is wrong and find the correct probability.',
                 f'The 11 totals are not equally likely. There are 36 equally likely outcomes and {two_dice_count(lambda i, j: i + j == k)} of them give a total of {k}, so P = {num(Fr(two_dice_count(lambda i, j: i + j == k), 36))}.',
                 f'B1 totals not equally likely; B1 {num(Fr(two_dice_count(lambda i, j: i + j == k), 36))} [2]')
    return Q(f'{nm} tosses two coins and says P(one head and one tail) = 1/3 because the outcomes are "two heads, two tails, or one of each". Explain the mistake.',
             'These three outcomes are not equally likely; "one of each" can happen as HT or TH, so there are 4 equally likely outcomes and P = 2/4 = 1/2.', 'B1 not equally likely; B1 1/2 with HT, TH [2]')


def t83_c4(r, D):
    nm1, nm2 = two_people(r)
    k = r.choice([6, 7, 8])
    win = two_dice_count(lambda i, j: i + j >= k)
    pr = r.choice([1, 2])
    intro = f'In a game at a school fair in {city(r)}, two fair dice are rolled. {nm1} wins if the total is {k} or more; otherwise {nm2} wins.'
    dbl = two_dice_count(lambda i, j: i == j)
    parts = [
        P(f'Find the probability that {nm1} wins.', num(Fr(win, 36)), f'M1 counts {win} outcomes; A1 {num(Fr(win, 36))}', 2),
        P(f'Find the probability that {nm2} wins.', num(Fr(36 - win, 36)), f'B1 1 − {num(Fr(win, 36))}', 1),
        P('Is the game fair? Give a reason.', ('Yes' if win == 18 else 'No') + f': P({nm1}) = {num(Fr(win, 36))}' + (' = 1/2.' if win == 18 else ', not 1/2.'), 'B1 compares with 1/2', 1),
        P(f'The game is played 180 times. How many times would you expect {nm1} to win?', str(180 * win // 36), f'M1 {num(Fr(win, 36))} × 180; A1 {180 * win // 36}', 2),
        P('Find the probability of rolling a double.', num(Fr(dbl, 36)), 'B1 6/36 = 1/6', 1),
    ]
    return cmp_(r, intro, parts)


t83.add('C4', (2, 3, 4, 5))(t83_c4)
CHAPTERS[8] = [t81, t82, t83]


# =========================================================== 9 Sequences, surds and sets
t91 = topic('Sequences: nth term of linear, quadratic, cubic and exponential sequences', 'sequences: nth term of linear, quadratic, cubic and exponential sequences', 'nth term', 'sequences')
t91.fixed('C1', (1, 2), [
    ('What is the next term in the sequence 3, 7, 11, 15, …?', '19', 'The terms increase by 4.', ['18', '20', '21']),
    ('What is the nth term of 5, 8, 11, 14, …?', '3n + 2', 'Difference 3, so 3n; 3 × 1 + 2 = 5.', ['n + 3', '3n + 5', '5n + 3']),
    ('Which sequence is quadratic?', '2, 5, 10, 17, 26, …', 'First differences 3, 5, 7, 9; second differences are constant (2).', ['2, 4, 8, 16, 32, …', '2, 5, 8, 11, 14, …', '1, 8, 27, 64, 125, …']),
    ('The nth term of a sequence is n³. What is the 4th term?', '64', '4³ = 64.', ['12', '16', '81']),
    ('What is the next term in the sequence 3, 6, 12, 24, …?', '48', 'Each term is multiplied by 2.', ['30', '36', '27']),
    ('The nth term is 2n² − 1. What is the 3rd term?', '17', '2 × 9 − 1 = 17.', ['35', '11', '5']),
    ('In the sequence with nth term 7 − 2n, what is the 5th term?', '−3', '7 − 10 = −3.', ['3', '25', '−10']),
])
t91.fixed('C2', (2, 3), [
    ('Explain how to tell whether a sequence is linear or quadratic from its differences.', 'A linear sequence has constant first differences; a quadratic sequence has constant second differences.', 'B1 linear: constant first differences; B1 quadratic: constant second differences [2]'),
    ('Explain why the coefficient of n² in the nth term of a quadratic sequence is half the second difference.', 'For an² + bn + c the first differences are a(2n + 1) + b, which change by 2a each time; so the second difference is 2a.', 'B1 second difference = 2a; B1 so a = half [2]'),
    ('Explain how to decide whether 100 is a term of the sequence with nth term 3n + 4.', 'Solve 3n + 4 = 100: n = 32, a whole number, so 100 is the 32nd term. If n were not a whole number it would not be a term.', 'B1 solve equation; B1 n must be a positive integer [2]'),
])


@t91.add('C1', (1, 2, 3))
def t91_lin(r, D):
    a, b = r.choice([2, 3, 4, 5, 6, 7, -2, -3, -4]), r.randint(-9, 12)
    terms = [a * n + b for n in range(1, 5)]
    cor = lin(a, b, 'n')
    ds = [lin(b + a, a, 'n') if b + a != 0 else lin(a, -b, 'n'), lin(a, -b, 'n') if b else lin(a + 1, -1, 'n'), lin(1, a, 'n') if a != 1 else lin(2, b, 'n'), lin(a, terms[0], 'n')]
    return SMC(r, f'Find the nth term of the sequence {", ".join(num(t) for t in terms)}, …', cor, ds, f'Difference {num(a)}, so {num(a)}n; first term {num(terms[0])} = {num(a)} × 1{sgn(b)}: nth term {cor}.')


def quad_terms(a, b, c, n=5):
    return [a * k * k + b * k + c for k in range(1, n + 1)]


@t91.add('C3', (1, 2, 3, 4, 5))
def t91_nth(r, D):
    if D <= 2:
        a, b = r.choice([2, 3, 4, 5, 6, 7, 8, -3, -5]), r.randint(-8, 15)
        ts = [a * n + b for n in range(1, 6)]
        k = r.choice([20, 25, 50, 100])
        return Q(f'The first five terms of a sequence are {", ".join(num(t) for t in ts)}. (a) Find the nth term. (b) Find the {ordinal(k)} term.', f'(a) {lin(a, b, "n")} (b) {num(a * k + b)}',
                 f'(a) B1 {num(a)}n; B1 {lin(a, b, "n")} (b) B1 {num(a * k + b)} [3]', type='multi_step')
    if D == 3:
        a, b, c = r.choice([1, 2, 3]), r.randint(-4, 5), r.randint(-6, 8)
        ts = quad_terms(a, b, c)
        return Q(f'Find the nth term of the quadratic sequence {", ".join(num(t) for t in ts)}, …', quad(a, b, c, 'n'),
                 f'M1 second difference {2 * a} so {a if a > 1 else ""}n²; M1 subtract {a if a > 1 else ""}n² to get linear part {lin(b, c, "n")}; A1 {quad(a, b, c, "n")} [3]')
    if D == 4:
        kind = r.choice(['cubic', 'exp'])
        if kind == 'cubic':
            c = r.randint(-5, 10)
            ts = [n ** 3 + c for n in range(1, 6)]
            return Q(f'The sequence {", ".join(num(t) for t in ts)}, … is related to the cube numbers. Find its nth term and the 10th term.', f'n³ {sgn(c)[1:]}; {1000 + c}' if c else f'n³; 1000',
                     f'B1 compares with 1, 8, 27, 64, 125; B1 n³{sgn(c) if c else ""}; B1 {1000 + c} [3]')
        a, k = r.choice([2, 3, 5]), r.choice([2, 3])
        ts = [a * k ** (n - 1) for n in range(1, 6)]
        return Q(f'Find the nth term of the sequence {", ".join(num(t) for t in ts)}, …', f'{a} × {k}ⁿ⁻¹', f'B1 common ratio {k}; B1 first term {a}; B1 {a} × {k}ⁿ⁻¹ [3]')
    a, b, c = r.choice([1, 2, 3]), r.randint(-6, 6), r.randint(-5, 10)
    ts = quad_terms(a, b, c)
    target = r.choice([k for k in range(6, 15)])
    val = a * target ** 2 + b * target + c
    return Q(f'A quadratic sequence begins {", ".join(num(t) for t in ts)}, … (a) Find the nth term. (b) Show that {num(val)} is a term of the sequence and state its position.', f'(a) {quad(a, b, c, "n")} (b) n = {target}',
             f'(a) M1 second difference {2 * a}; M1 linear part; A1 {quad(a, b, c, "n")} (b) M1 {quad(a, b, c, "n")} = {num(val)}; A1 n = {target} [5]', type='multi_step')


@t91.add('C3', (2, 3, 4))
def t91_pattern(r, D):
    nm = person(r)
    a, b = r.choice([(3, 1), (4, 1), (5, 1), (2, 2), (6, 2), (4, 4)])
    ts = [a * n + b for n in range(1, 5)]
    what = r.choice([('matchsticks', 'pattern'), ('tiles', 'design'), ('dots', 'diagram'), ('beads', 'necklace')])
    N = r.choice([95, 125, 150, 200, 250])
    k = (N - b) // a
    return Q(f'{nm} makes a sequence of {what[1]}s from {what[0]}. {what[1].capitalize()} 1 uses {ts[0]}, {what[1]} 2 uses {ts[1]}, {what[1]} 3 uses {ts[2]} and {what[1]} 4 uses {ts[3]} {what[0]}. (a) Find an expression for the number of {what[0]} in {what[1]} n. (b) {nm} has {N} {what[0]}. Find the number of the largest {what[1]} {nm} can make.',
             f'(a) {lin(a, b, "n")} (b) {what[1]} {k}', f'(a) B1 {a}n; B1 {lin(a, b, "n")} (b) M1 {lin(a, b, "n")} ≤ {N}; A1 {k} [4]', type='multi_step')


@t91.add('C2', (2, 3, 4), 'explain')
def t91_err(r, D):
    nm = person(r)
    a, b = r.choice([3, 4, 5, 6, 7]), r.randint(1, 9)
    ts = [a * n + b for n in range(1, 5)]
    case = r.choice(['plus', 'term'])
    if case == 'plus':
        return Q(f'{nm} says the nth term of {", ".join(map(str, ts))}, … is n + {a} because "the sequence goes up in {a}s". Explain the mistake and find the correct nth term.',
                 f'Going up by {a} each time means the nth term contains {a}n (the {a} times table), not n + {a}. {a} × 1 = {a} and the first term is {ts[0]}, so nth term = {lin(a, b, "n")}.', f'B1 difference gives {a}n; B1 {lin(a, b, "n")} [2]')
    N = a * r.randint(10, 30) + b + r.randint(1, a - 1)
    return Q(f'{nm} says that {N} is a term of the sequence with nth term {lin(a, b, "n")}. Explain whether {nm} is correct.', f'{lin(a, b, "n")} = {N} gives n = {ex(round((N - b) / a, 3))}, which is not a whole number, so {N} is not a term.',
             f'M1 solves {lin(a, b, "n")} = {N}; A1 n not an integer, so not a term [2]')


def t91_c4(r, D):
    a, b, c = 1, r.randint(1, 4), r.randint(0, 5)
    ts = quad_terms(a, b, c, 4)
    nm = person(r)
    intro = f'{nm} builds rectangular patterns of square tiles. Pattern n is n tiles wide and (n + {b}) tiles long, with {c} extra tiles as a border feature. The first four patterns use {", ".join(map(str, ts))} tiles.' if c else \
        f'{nm} builds rectangular patterns of square tiles. Pattern n is n tiles wide and (n + {b}) tiles long. The first four patterns use {", ".join(map(str, ts))} tiles.'
    t5 = 25 + 5 * b + c
    parts = [
        P('Find the number of tiles in pattern 5.', str(t5), f'B1 {t5}', 1),
        P('Show that the second differences are constant.', f'First differences {", ".join(str(ts[i + 1] - ts[i]) for i in range(3))}; second differences 2, 2.', 'M1 first differences; A1 second differences 2', 2),
        P('Find an expression for the number of tiles in pattern n.', quad(1, b, c, 'n'), f'M1 n²; M1 linear part {lin(b, c, "n")}; A1 {quad(1, b, c, "n")}', 3),
        P(f'Explain why no pattern uses exactly {ts[-1] + 3} tiles.' if (ts[-1] + 3) not in quad_terms(1, b, c, 12) else 'Find the number of tiles in pattern 20.',
          f'Pattern 4 uses {ts[-1]} and pattern 5 uses {t5}, and the sequence is increasing, so no pattern uses {ts[-1] + 3}.' if (ts[-1] + 3) not in quad_terms(1, b, c, 12) else str(400 + 20 * b + c),
          'B1 consecutive terms either side; B1 increasing' if (ts[-1] + 3) not in quad_terms(1, b, c, 12) else f'B1 {400 + 20 * b + c}', 2 if (ts[-1] + 3) not in quad_terms(1, b, c, 12) else 1),
    ]
    return cmp_(r, intro, parts)


t91.add('C4', (2, 3, 4, 5))(t91_c4)

# ---------------------------------------------------------------- recurring decimals
t92 = topic('Rational and irrational numbers: recurring decimals as fractions', 'rational and irrational numbers: recurring decimals as fractions', 'recurring decimals', 'rational irrational')
t92.fixed('C1', (1, 2), [
    ('Write 0.4̇ as a fraction.', '4/9', 'x = 0.444…, 10x − x = 4, x = 4/9.', ['2/5', '4/10', '44/100']),
    ('Which fraction gives a recurring decimal?', '5/6', '6 has a prime factor 3, so 5/6 = 0.83̇.', ['3/8', '7/20', '9/25']),
    ('Write 0.2̇7̇ as a fraction in its simplest form.', '3/11', 'x = 0.2727…, 100x − x = 27, x = 27/99 = 3/11.', ['27/100', '2/7', '27/90']),
    ('Which of these is irrational?', '√10', '10 is not a perfect square.', ['√49', '0.1̇', '22/7']),
    ('The dot notation 0.1̇2̇ means', '0.121212…', 'The dots mark the first and last digits of the repeating block.', ['0.12222…', '0.1122…', '0.12']),
])
t92.fixed('C2', (2, 3), [
    ('Explain why every recurring decimal is a rational number.', 'It can always be written as a fraction: multiplying by a power of 10 and subtracting removes the repeating part, leaving an equation with an integer solution as a ratio.', 'B1 algebraic method; B1 gives a/b [2]'),
    ('Explain how you can tell whether a fraction in its simplest form gives a terminating decimal.', 'It terminates exactly when the denominator has no prime factors other than 2 and 5.', 'B1 prime factors of denominator; B1 only 2 and 5 [2]'),
    ('Explain why π + 1 is irrational.', 'If π + 1 were a fraction a/b then π = a/b − 1 would also be a fraction, which is false since π is irrational.', 'B1 assume rational; B1 contradiction [2]'),
])


def recur_str(intpart, nonrep, rep):
    """'0.' + nonrep + rep with dots on first and last of rep."""
    dot = '̇'
    if len(rep) == 1:
        rs = rep + dot
    else:
        rs = rep[0] + dot + rep[1:-1] + rep[-1] + dot
    return f'{intpart}.{nonrep}{rs}'


def recur_val(intpart, nonrep, rep):
    n, m = len(nonrep), len(rep)
    whole = int(nonrep + rep) - (int(nonrep) if nonrep else 0)
    return intpart + Fr(whole, 10 ** n * (10 ** m - 1))


@t92.add('C3', (1, 2, 3, 4, 5))
def t92_conv(r, D):
    if D <= 2:
        rep = str(r.randint(1, 8))
        non, ip = '', 0
    elif D == 3:
        rep = f'{r.randint(1, 9)}{r.randint(0, 9)}'
        non, ip = '', 0
        if rep[0] == rep[1]:
            return None
    elif D == 4:
        rep = str(r.randint(1, 8))
        non, ip = str(r.randint(1, 9)), 0
    else:
        rep = f'{r.randint(1, 9)}{r.randint(0, 9)}'
        non, ip = str(r.randint(0, 9)), r.randint(1, 3)
        if rep[0] == rep[1]:
            return None
    v = recur_val(ip, non, rep)
    s_ = recur_str(ip, non, rep)
    n, m = len(non), len(rep)
    expanded = f'{ip}.{non}{rep * (4 // m + 1)}…'
    mult1 = 10 ** (n + m)
    mult2 = 10 ** n
    key = f'M1 x = {expanded}; M1 {mult1}x − {mult2 if mult2 > 1 else ""}x to remove the recurring part; A1 {num(v) if ip == 0 else ff(v)} [3]'
    return Q(f'Show that the recurring decimal {s_} can be written as {"the fraction" if ip == 0 else "the mixed number"} {num(v) if ip == 0 else ff(v)}, using an algebraic method.' if D >= 4 else
             f'Write the recurring decimal {s_} as a fraction in its simplest form, showing your algebraic working.', num(v) if ip == 0 else ff(v), key)


@t92.add('C1', (1, 2, 3))
def t92_term(r, D):
    d = r.choice([3, 6, 7, 9, 11, 12, 15, 30])
    good = r.sample([2, 4, 5, 8, 10, 16, 20, 25, 40], 3)
    n = r.randint(1, d - 1)
    while math.gcd(n, d) != 1:
        n = r.randint(1, d - 1)
    c = f'{n}/{d}'
    ds = [f'{next(k for k in range(r.randint(1, g - 1) if g > 2 else 1, g + 1) if math.gcd(k, g) == 1)}/{g}' for g in good]
    return SMC(r, 'Which of these fractions is equal to a recurring decimal?', c, ds, f'{d} = {pf_str(d)} has a prime factor other than 2 or 5, so {c} recurs; the others have denominators made of 2s and 5s only.')


@t92.add('C2', (2, 3, 4), 'explain')
def t92_err(r, D):
    nm = person(r)
    rep = f'{r.randint(1, 9)}{r.randint(0, 9)}'
    if rep[0] == rep[1]:
        return None
    v = recur_val(0, '', rep)
    return Q(f'{nm} converts 0.{rep[0]}̇{rep[1]}̇ to a fraction by writing x = 0.{rep}{rep}…, 10x = {rep[0]}.{rep[1]}{rep}…, and subtracting. Explain why this does not remove the recurring part, and find the correct fraction.',
             f'The repeating block has 2 digits, so you must multiply by 100: 100x = {rep}.{rep}…, 100x − x = {int(rep)}, x = {int(rep)}/99 = {num(v)}.', f'B1 multiply by 100 for a 2-digit block; B1 {num(v)} [2]')


def t92_c4(r, D):
    a = r.randint(1, 8)
    rep = f'{r.randint(1, 9)}{r.randint(0, 9)}'
    if rep[0] == rep[1]:
        return None
    x = Fr(a, 9)
    y = recur_val(0, '', rep)
    intro = 'Answer these questions about rational and irrational numbers.'
    k = r.choice([2, 3, 5, 6, 7])
    parts = [
        P(f'Write 0.{a}̇ as a fraction.', num(x), f'M1 10x − x = {a}; A1 {num(x)}', 2),
        P(f'Write 0.{rep[0]}̇{rep[1]}̇ as a fraction in its simplest form.', num(y), f'M1 100x − x = {int(rep)}; A1 {num(y)}', 2),
        P(f'Find 0.{a}̇ + 0.{rep[0]}̇{rep[1]}̇ as a single fraction.', num(x + y), f'M1 common denominator; A1 {num(x + y)}', 2),
        P(f'Decide whether √{k} × √{k * 4} is rational or irrational. Show your working.', f'√{k} × √{4 * k} = √{4 * k * k} = {2 * k}, rational', f'M1 √{4 * k * k}; A1 {2 * k} rational', 2),
        P(f'Give an irrational number between 3 and 4.', r.choice(['√10', '√11', 'π', '√13', '√15']), 'B1 any valid surd or π', 1),
    ]
    return cmp_(r, intro, parts)


t92.add('C4', (2, 3, 4, 5))(t92_c4)

# ---------------------------------------------------------------- surds
def surd_simplify(n):
    k = 1
    for f in range(int(math.isqrt(n)), 1, -1):
        if n % (f * f) == 0:
            k = f
            break
    return k, n // (k * k)


def sstr(k, m):
    if m == 1:
        return num(k)
    return (num(k) if k not in (1, -1) else ('' if k == 1 else MINUS)) + f'√{m}'


t93 = topic('Surds: simplifying and rationalising the denominator', 'surds: simplifying and rationalising the denominator', 'surds', 'rationalising the denominator')
t93.fixed('C1', (1, 2), [
    ('Simplify √50.', '5√2', '√50 = √25 × √2.', ['25√2', '2√5', '10√5']),
    ('Simplify √3 × √12.', '6', '√36 = 6.', ['√15', '3√4', '36']),
    ('Simplify 2√5 + 3√5.', '5√5', 'Like surds: (2 + 3)√5.', ['5√10', '6√5', '√25']),
    ('Rationalise the denominator of 1/√2.', '√2/2', 'Multiply top and bottom by √2.', ['2/√2', '√2', '1/2']),
    ('Simplify (√7)².', '7', '√7 × √7 = 7.', ['49', '√14', '14']),
    ('Simplify √48.', '4√3', '√48 = √16 × √3.', ['3√4', '2√12', '16√3']),
])
t93.fixed('C2', (2, 3), [
    ('Explain why √2 + √3 cannot be simplified to √5.', '√2 and √3 are unlike surds; √a + √b ≠ √(a + b) in general (e.g. √2 + √3 ≈ 3.15 but √5 ≈ 2.24).', 'B1 unlike surds; B1 numerical check [2]'),
    ('Explain why multiplying the numerator and denominator by √3 does not change the value of 2/√3.', 'It is the same as multiplying by √3/√3 = 1, so the value is unchanged; only the form changes to 2√3/3.', 'B1 multiplying by 1; B1 2√3/3 [2]'),
    ('Explain why (3 + √2)(3 − √2) is a rational number.', 'It is a difference of two squares: 9 − (√2)² = 9 − 2 = 7, and the surd terms cancel.', 'B1 middle terms cancel; B1 7 [2]'),
])


@t93.add('C1', (1, 2, 3))
def t93_simp(r, D):
    m = r.choice([2, 3, 5, 6, 7])
    k = r.choice([2, 3, 4, 5, 6] if D <= 2 else [5, 6, 7, 8, 9, 10])
    n = k * k * m
    cor = sstr(k, m)
    ds = [sstr(m, k * k), sstr(k * k, m), sstr(2, n // 4) if n % 4 == 0 and n // 4 != m else sstr(k + 1, m), sstr(k, m + 1)]
    return SMC(r, f'Write √{n} in the form k√{m}.' if D == 1 else f'Simplify √{n}.', cor, ds, f'√{n} = √{k * k} × √{m} = {cor}.')


@t93.add('C3', (1, 2, 3, 4, 5))
def t93_calc(r, D):
    if D == 1:
        a, b = r.choice([(8, 18), (12, 27), (20, 45), (50, 8), (75, 12), (32, 18), (28, 63)])
        ka, ma = surd_simplify(a)
        kb, mb = surd_simplify(b)
        return Q(f'Simplify √{a} + √{b}.', sstr(ka + kb, ma), f'M1 √{a} = {sstr(ka, ma)} and √{b} = {sstr(kb, mb)}; A1 {sstr(ka + kb, ma)} [2]')
    if D == 2:
        k = r.choice([2, 3, 5, 6, 7, 10])
        a = r.randint(1, 9)
        return Q(f'Rationalise the denominator of {a}/√{k}, simplifying your answer.', (f'{num(Fr(a, k))}√{k}' if Fr(a, k).denominator == 1 else f'{a}√{k}/{k}' if math.gcd(a, k) == 1 else f'{a // math.gcd(a, k)}√{k}/{k // math.gcd(a, k)}'),
                 f'M1 × √{k}/√{k}; A1 {a}√{k}/{k} simplified [2]')
    if D == 3:
        a, b, m = r.randint(1, 6), r.choice([-4, -3, -2, -1, 1, 2, 3, 5]), r.choice([2, 3, 5, 7])
        c, d = r.randint(1, 5), r.choice([-3, -2, -1, 1, 2, 4])
        # (a + b√m)(c + d√m) = ac + bdm + (ad + bc)√m
        rat = a * c + b * d * m
        sc = a * d + b * c
        s1 = f'({a} {"+" if b > 0 else MINUS} {sstr(abs(b), m)})'
        s2 = f'({c} {"+" if d > 0 else MINUS} {sstr(abs(d), m)})'
        ans = f'{num(rat)}' + (f' {"+" if sc > 0 else MINUS} {sstr(abs(sc), m)}' if sc else '')
        return Q(f'Expand and simplify {s1}{s2}.', ans, f'M1 four terms {a * c}, {sstr(a * d, m)}, {sstr(b * c, m)}, {b * d * m}; A1 {ans} [2]')
    a, b, m = r.randint(1, 6), r.randint(1, 4), r.choice([2, 3, 5, 6, 7])
    den = a * a - b * b * m
    if den == 0:
        return None
    k = r.randint(1, 9)
    # k/(a + b√m) = k(a − b√m)/den
    g = math.gcd(math.gcd(k * a, k * b), abs(den))
    num_ = f'{num(k * a // g)} − {sstr(k * b // g, m)}'
    dd = den // g
    if dd < 0:
        num_ = f'{sstr(k * b // g, m)} − {num(k * a // g)}'
        dd = -dd
    ans = f'({num_})/{dd}' if dd != 1 else num_
    return Q(f'Rationalise the denominator of {k}/({a} + {sstr(b, m)}), simplifying your answer.', ans, f'M1 × ({a} − {sstr(b, m)}); M1 denominator {a}² − {b * b * m} = {num(den)}; A1 {ans} [3]')


@t93.add('C2', (2, 3, 4), 'explain')
def t93_err(r, D):
    nm = person(r)
    case = r.choice(['add', 'rat', 'sq'])
    if case == 'add':
        a, b = r.choice([(2, 7), (3, 5), (5, 11), (2, 3)])
        return Q(f'{nm} writes √{a} + √{b} = √{a + b}. Show that this is wrong.', f'√{a} + √{b} ≈ {ex(round(math.sqrt(a) + math.sqrt(b), 3))} but √{a + b} ≈ {ex(round(math.sqrt(a + b), 3))}; surds cannot be added like this.', 'M1 evaluates both; A1 not equal [2]')
    if case == 'rat':
        k = r.choice([3, 5, 7])
        return Q(f'{nm} rationalises 6/√{k} by multiplying the numerator only by √{k}, getting 6√{k}. Explain the error and give the correct answer.', f'Numerator and denominator must both be multiplied by √{k}: 6√{k}/{k}' + (f' = 2√{k}' if k == 3 else '') + '.',
                 f'B1 multiply top and bottom; B1 6√{k}/{k} simplified [2]')
    a, m = r.randint(2, 5), r.choice([2, 3, 5])
    return Q(f'{nm} says ({a} + √{m})² = {a * a} + {m} = {a * a + m}. Explain the mistake and give the correct expansion.', f'{nm} missed the middle terms: ({a} + √{m})² = {a * a} + {2 * a}√{m} + {m} = {a * a + m} + {2 * a}√{m}.', f'B1 middle term 2 × {a}√{m}; B1 {a * a + m} + {2 * a}√{m} [2]')


def t93_c4(r, D):
    a, b = r.choice([(2, 8), (3, 12), (5, 20), (2, 18), (3, 27)])
    ka, ma = surd_simplify(b)
    intro = f'A rectangle has length √{b} cm and width √{a} cm.'
    diag2 = a + b
    kd, md = surd_simplify(diag2)
    parts = [
        P('Find the area of the rectangle, giving your answer as an integer.', f'{math.isqrt(a * b)} cm²', f'M1 √{a * b}; A1 {math.isqrt(a * b)}', 2),
        P('Find the perimeter in the form k√m, where k and m are integers.', f'{sstr(2 * (ka + 1) if ma == a else 0, a)} cm', f'M1 √{b} = {sstr(ka, ma)}; A1 2({sstr(ka, ma)} + √{a}) = {sstr(2 * (ka + 1), a)}', 2),
        P('Find the length of a diagonal, as a simplified surd.', f'{sstr(kd, md)} cm', f'M1 √({a} + {b}) = √{diag2}; A1 {sstr(kd, md)}', 2),
        P(f'Find the ratio length : width in its simplest form.', f'{ka} : 1', f'M1 √{b} ÷ √{a} = √{b // a}; A1 {ka} : 1', 2),
        P(f'Rationalise and simplify 1/√{a} + 1/√{b}.', f'{num(Fr(1, a) + Fr(1, a * ka))}√{a}', f'M1 √{a}/{a} + √{b}/{b}; M1 common surd √{a}; A1 {num(Fr(1, a) + Fr(1, a * ka))}√{a}', 3),
    ]
    return cmp_(r, intro, parts)


t93.add('C4', (2, 3, 4, 5))(t93_c4)

# ---------------------------------------------------------------- sets
t94 = topic('Sets: notation, Venn diagrams, union, intersection and complement', 'sets: notation, venn diagrams, union, intersection and complement', 'sets', 'venn diagrams')
t94.fixed('C1', (1, 2), [
    ('What does A ∩ B mean?', 'The elements in both A and B', '∩ is the intersection.', ['The elements in A or B or both', 'The elements not in A', 'The number of elements in A']),
    ('What does A ∪ B mean?', 'The elements in A or B or both', '∪ is the union.', ['The elements in both A and B only', 'The elements in neither set', 'The elements in A but not B']),
    ('What does n(A) mean?', 'The number of elements in set A', 'n(A) counts the elements.', ['The nth element of A', 'The complement of A', 'The universal set']),
    ('If ℰ = {1, 2, …, 10} and A = {even numbers}, what is A′?', '{1, 3, 5, 7, 9}', 'The complement contains elements of ℰ not in A.', ['{2, 4, 6, 8, 10}', '{0, 1, 3, 5, 7, 9}', '∅']),
    ('Which symbol means "is an element of"?', '∈', '3 ∈ {1, 2, 3}.', ['⊂', '∪', '∩']),
    ('The empty set is written as', '∅', 'The empty set has no elements.', ['{0}', 'ℰ', '0']),
])
t94.fixed('C2', (2, 3), [
    ('Explain the difference between A ∪ B and A ∩ B, using A = {1, 2, 3} and B = {3, 4}.', 'A ∪ B = {1, 2, 3, 4} contains everything in either set; A ∩ B = {3} contains only what is in both.', 'B1 union with example; B1 intersection with example [2]'),
    ('Explain why n(A ∪ B) = n(A) + n(B) − n(A ∩ B).', 'Adding n(A) and n(B) counts the elements in the intersection twice, so they must be subtracted once.', 'B1 intersection counted twice; B1 subtract once [2]'),
    ('Explain what A ⊂ B means and give an example.', 'Every element of A is also an element of B; e.g. {2, 4} ⊂ {1, 2, 3, 4}.', 'B1 definition; B1 example [2]'),
])

SETDEF = [('multiples of 3', lambda n: n % 3 == 0), ('even numbers', lambda n: n % 2 == 0), ('prime numbers', lambda n: is_prime(n)), ('square numbers', lambda n: sq(n)),
          ('factors of 24', lambda n: 24 % n == 0), ('multiples of 4', lambda n: n % 4 == 0), ('odd numbers', lambda n: n % 2 == 1), ('factors of 36', lambda n: 36 % n == 0), ('multiples of 5', lambda n: n % 5 == 0)]


def setstr(s_):
    return '{' + ', '.join(map(str, sorted(s_))) + '}' if s_ else '∅'


@t94.add('C1', (1, 2, 3))
def t94_op(r, D):
    N = r.choice([12, 15, 16, 20])
    (an, af), (bn, bf) = r.sample(SETDEF, 2)
    U = set(range(1, N + 1))
    A, B = {n for n in U if af(n)}, {n for n in U if bf(n)}
    op = r.choice(['∩', '∪'] if D <= 2 else ['∩', '∪', "A′ ∩ B", "(A ∪ B)′"])
    res = {'∩': A & B, '∪': A | B, "A′ ∩ B": (U - A) & B, "(A ∪ B)′": U - (A | B)}[op]
    expr_ = {'∩': 'A ∩ B', '∪': 'A ∪ B'}.get(op, op)
    wrong = [A & B, A | B, (U - A) & B, U - (A | B), A - B, B - A, U - (A & B)]
    ds = [setstr(w) for w in wrong if w != res]
    return SMC(r, f'ℰ = {{1, 2, 3, …, {N}}}, A = {{{an}}} and B = {{{bn}}}. List the elements of {expr_}.', setstr(res), ds, f'A = {setstr(A)}, B = {setstr(B)}; {expr_} = {setstr(res)}.')


@t94.add('C3', (1, 2, 3, 4, 5))
def t94_venn(r, D):
    nm = person(r)
    s1, s2 = r.choice([('football', 'basketball'), ('French', 'Spanish'), ('a cat', 'a dog'), ('tea', 'coffee'), ('Science club', 'Drama club'), ('the piano', 'the guitar')])
    both = r.randint(3, 15)
    a_only, b_only = r.randint(4, 25), r.randint(4, 25)
    neither = r.randint(1, 12)
    tot = both + a_only + b_only + neither
    nA, nB = a_only + both, b_only + both
    verb = 'play' if s1 in ('football', 'basketball') else ('study' if s1 in ('French', 'Spanish') else ('have' if s1 == 'a cat' else ('drink' if s1 == 'tea' else ('belong to' if 'club' in s1 else 'play'))))
    stem = f'In a group of {tot} students in {city(r)}, {nA} {verb} {s1}, {nB} {verb} {s2} and {neither} {verb} neither.'
    if D <= 2:
        return Q(stem + f' Draw a Venn diagram and find how many students {verb} both.', str(both), f'M1 {nA} + {nB} + {neither} − {tot}; A1 {both} [2]')
    if D == 3:
        return Q(stem + f' Find how many students {verb} {s1} only, and the probability that a student chosen at random {verb}s exactly one of them.'.replace(' belong tos', ' belongs to').replace(' haves', ' has').replace(' studys', ' studies'),
                 f'{a_only}; {num(Fr(a_only + b_only, tot))}', f'M1 both = {both}; A1 {a_only}; M1 ({a_only} + {b_only})/{tot}; A1 {num(Fr(a_only + b_only, tot))} [4]')
    x = r.randint(2, 9)
    # algebra: both = x, A only = nA - x ... total equation
    return Q(f'In a group of {tot} students, {nA} {verb} {s1}, {nB} {verb} {s2}, and {neither} {verb} neither. Let x be the number who {verb} both. Write an equation in x, solve it, and find n(A′ ∩ B), where A is the set of students who {verb} {s1} and B is the set who {verb} {s2}.',
             f'({nA} − x) + x + ({nB} − x) + {neither} = {tot}; x = {both}; n(A′ ∩ B) = {b_only}', f'M1 equation; A1 x = {both}; B1 {b_only} [3]')


@t94.add('C2', (2, 3, 4), 'explain')
def t94_err(r, D):
    nm = person(r)
    a, b, both = r.randint(10, 25), r.randint(10, 25), r.randint(3, 9)
    tot = a + b - both + r.randint(0, 6)
    return Q(f'In a class, n(A) = {a}, n(B) = {b} and n(A ∩ B) = {both}. {nm} says n(A ∪ B) = {a + b}. Explain the mistake and find n(A ∪ B).', f'The {both} elements in A ∩ B have been counted twice. n(A ∪ B) = {a} + {b} − {both} = {a + b - both}.',
             f'B1 intersection counted twice; B1 {a + b - both} [2]')


def t94_c4(r, D):
    N = r.choice([15, 20, 24])
    (an, af), (bn, bf) = r.sample(SETDEF[:6], 2)
    U = set(range(1, N + 1))
    A, B = {n for n in U if af(n)}, {n for n in U if bf(n)}
    if not (A & B):
        return None
    intro = f'ℰ = {{x : x is an integer, 1 ≤ x ≤ {N}}}, A = {{{an}}} and B = {{{bn}}}.'
    k = r.choice(sorted(U))
    parts = [
        P('List the elements of A and of B.', f'A = {setstr(A)}; B = {setstr(B)}', 'B1 A; B1 B', 2),
        P('Find n(A ∩ B).', str(len(A & B)), f'B1 {len(A & B)}', 1),
        P('List the elements of (A ∪ B)′.', setstr(U - (A | B)), 'B2 (B1 one error)', 2),
        P('A number is chosen at random from ℰ. Find the probability that it is in A but not in B.', num(Fr(len(A - B), N)), f'M1 n(A ∩ B′) = {len(A - B)}; A1 {num(Fr(len(A - B), N))}', 2),
        P(f'State whether {k} ∈ A ∪ B, giving a reason.', ('Yes' if k in (A | B) else 'No') + (f': {k} is in ' + ('both A and B' if k in A and k in B else ('A' if k in A else 'B')) + '.' if k in (A | B) else f': {k} is in neither A nor B.'), 'B1 with reason', 1),
    ]
    return cmp_(r, intro, parts)


t94.add('C4', (2, 3, 4, 5))(t94_c4)
CHAPTERS[9] = [t91, t92, t93, t94]


# =========================================================== 10 Straight lines and quadratic equations
def pt(x, y):
    return f'({num(x)}, {num(y)})'


def line_eq(m, c):
    """y = mx + c with exact fractions."""
    m, c = Fr(m), Fr(c)
    if m == 0:
        return f'y = {num(c)}'
    ms = '' if m == 1 else (MINUS if m == -1 else num(m))
    if m.denominator != 1:
        ms = (MINUS if m < 0 else '') + f'({num(abs(m))})'
    cs = '' if c == 0 else (f' + {num(c)}' if c > 0 else f' − {num(-c)}')
    return f'y = {ms}x{cs}'


def lhs_mx(m, c):
    """'mx + c' (right-hand side of line_eq) for working lines."""
    return line_eq(m, c)[4:]


def nb(x):
    """Number, bracketed if negative (for squaring in working)."""
    return f'({num(x)})' if x < 0 else num(x)


t101 = topic('Straight-line graphs: gradient, y-intercept and y = mx + c', 'straight-line graphs: gradient, y-intercept and y = mx + c', 'gradient', 'y = mx + c')
t101.fixed('C1', (1, 2), [
    ('What is the gradient of the line y = 4x − 3?', '4', 'In y = mx + c the gradient is m.', ['−3', '3', '−4']),
    ('Where does the line y = 2x + 5 cross the y-axis?', '(0, 5)', 'The y-intercept is c = 5.', ['(5, 0)', '(0, 2)', '(−2.5, 0)']),
    ('Which line is parallel to the x-axis?', 'y = 3', 'y = constant is horizontal.', ['x = 3', 'y = 3x', 'y = x + 3']),
    ('A line slopes down from left to right. Its gradient is', 'negative', 'As x increases, y decreases.', ['positive', 'zero', 'undefined']),
    ('What is the gradient of the line through (1, 2) and (3, 8)?', '3', '(8 − 2) ÷ (3 − 1) = 3.', ['1/3', '6', '2']),
    ('Rearrange 2y = 6x + 4 into the form y = mx + c.', 'y = 3x + 2', 'Divide every term by 2.', ['y = 6x + 4', 'y = 3x + 4', 'y = 6x + 2']),
])
t101.fixed('C2', (2, 3), [
    ('Explain what the gradient of a straight line tells you.', 'How steep the line is: the change in y for every increase of 1 in x (positive slopes up, negative slopes down).', 'B1 change in y per unit x; B1 sign meaning [2]'),
    ('Explain why the line x = 4 cannot be written in the form y = mx + c.', 'It is vertical: every point has x = 4 whatever y is, so its gradient is undefined.', 'B1 vertical line; B1 gradient undefined [2]'),
    ('Explain how to check whether the point (2, 7) lies on the line y = 3x + 1.', 'Substitute x = 2: y = 3 × 2 + 1 = 7, which matches, so the point is on the line.', 'B1 substitute; B1 compare y-values [2]'),
])


def two_pts(r, D):
    for _ in range(50):
        x1, y1 = r.randint(-5, 6), r.randint(-6, 8)
        dx = r.choice([1, 2, 3, 4]) * r.choice([1, -1])
        dy = r.randint(-8, 9)
        if dy == 0:
            continue
        x2, y2 = x1 + dx, y1 + dy
        m = Fr(dy, dx)
        if D <= 2 and m.denominator != 1:
            continue
        return x1, y1, x2, y2, m
    return None


@t101.add('C1', (1, 2, 3))
def t101_grad(r, D):
    p = two_pts(r, D)
    if not p:
        return None
    x1, y1, x2, y2, m = p
    return MC(r, f'Find the gradient of the line joining {pt(x1, y1)} and {pt(x2, y2)}.', m, [1 / m if m else 1, -m if m else 2, Fr(x2 - x1, 1) if m.denominator == 1 else Fr(y2 + y1, x2 + x1 or 1), m + 1], f'(y₂ − y₁)/(x₂ − x₁) = {num(y2 - y1)}/{num(x2 - x1)} = {num(m)}.')


@t101.add('C3', (1, 2, 3, 4, 5))
def t101_eq(r, D):
    p = two_pts(r, D)
    if not p:
        return None
    x1, y1, x2, y2, m = p
    c = y1 - m * x1
    if D <= 2:
        mm, cc = r.choice([2, 3, -2, 4, -1, 5]), r.randint(-6, 8)
        x0 = r.randint(-3, 5)
        return Q(f'A line has gradient {num(mm)} and passes through {pt(x0, mm * x0 + cc)}. Find its equation in the form y = mx + c.', line_eq(mm, cc), f'M1 {num(mm * x0 + cc)} = {num(mm)} × {num(x0)} + c; A1 {line_eq(mm, cc)} [2]')
    if D == 3:
        return Q(f'Find the equation of the line passing through {pt(x1, y1)} and {pt(x2, y2)}. Give your answer in the form y = mx + c.', line_eq(m, c), f'M1 gradient {num(m)}; M1 substitutes a point; A1 {line_eq(m, c)} [3]')
    a, b = r.choice([2, 3, 4, 5]), r.choice([1, 2, 3, 4, 5, 6])
    k = r.randint(-12, 12)
    # ax + by = k  -> y = -a/b x + k/b
    mm, cc = Fr(-a, b), Fr(k, b)
    xi = Fr(k, a)
    return Q(f'The line L has equation {a}x + {b}y = {num(k)}. Find (a) the gradient of L (b) the coordinates of the points where L crosses the axes.', f'(a) {num(mm)} (b) {pt(0, cc)} and ({num(xi)}, 0)',
             f'(a) M1 rearranges to {line_eq(mm, cc)}; A1 {num(mm)} (b) B1 (0, {num(cc)}); B1 ({num(xi)}, 0) [4]', type='multi_step')


@t101.add('C3', (2, 3, 4))
def t101_ctx(r, D):
    nm = person(r)
    fix, rate = r.choice([(30, 0.12), (15, 0.2), (40, 0.08), (25, 0.15)])
    u1, u2 = r.choice([100, 150, 200]), r.choice([300, 400, 500])
    c1, c2 = fix + rate * u1, fix + rate * u2
    return Q(f'A phone plan in {city(r)} charges a fixed monthly fee plus a cost per minute. {nm} pays {money(c1)} for {u1} minutes and {money(c2)} for {u2} minutes. The cost C is a linear function of the number of minutes m. Find the equation of the line in the form C = am + b and interpret the gradient and intercept.',
             f'C = {ex(rate)}m + {fix}; gradient = {money(rate)} per minute, intercept = fixed fee {money(fix)}', f'M1 gradient ({money(c2)} − {money(c1)}) ÷ ({u2} − {u1}) = {ex(rate)}; A1 b = {fix}; B1 interpretation of both [3]')


@t101.add('C2', (2, 3, 4), 'explain')
def t101_err(r, D):
    nm = person(r)
    p = two_pts(r, 2)
    if not p:
        return None
    x1, y1, x2, y2, m = p
    if m == 0:
        return None
    case = r.choice(['flip', 'intercept'])
    if case == 'flip':
        return Q(f'{nm} finds the gradient of the line through {pt(x1, y1)} and {pt(x2, y2)} as ({num(x2)} − {nb(x1)}) ÷ ({num(y2)} − {nb(y1)}) = {num(1 / m)}. Explain the mistake and give the correct gradient.',
                 f'Gradient is change in y ÷ change in x, not the other way round: {nb(y2 - y1)} ÷ {nb(x2 - x1)} = {num(m)}.', f'B1 Δy/Δx; B1 {num(m)} [2]')
    a = r.choice([2, 3, 4])
    b = r.randint(1, 9)
    return Q(f'{nm} says the line {a}y = {a * b}x + {a * 3} has gradient {a * b} and y-intercept {a * 3}. Explain the mistake and give the correct values.', f'The equation must first be divided by {a} to give y = {b}x + 3; gradient {b}, intercept 3.', f'B1 must make y the subject; B1 gradient {b}, intercept (0, 3) [2]')


def t101_c4(r, D):
    p = two_pts(r, 3)
    if not p:
        return None
    x1, y1, x2, y2, m = p
    if m == 0:
        return None
    c = y1 - m * x1
    xk = r.randint(-4, 8)
    intro = f'A straight line passes through A{pt(x1, y1)} and B{pt(x2, y2)}.'
    parts = [
        P('Find the gradient of AB.', num(m), f'M1 {num(y2 - y1)}/{num(x2 - x1)}; A1 {num(m)}', 2),
        P('Find the equation of the line AB in the form y = mx + c.', line_eq(m, c), f'M1 substitutes; A1 {line_eq(m, c)}', 2),
        P(f'The point C({num(xk)}, k) lies on the line. Find k.', num(m * xk + c), f'B1 {num(m * xk + c)}', 1),
        P('Find the coordinates of the point where the line crosses the x-axis.', f'({num(-c / m)}, 0)', f'M1 0 = {lhs_mx(m, c)}; A1 ({num(-c / m)}, 0)', 2),
        P(f'Decide whether the point ({num(x1 + 2 * (x2 - x1))}, {num(y1 + 2 * (y2 - y1) + 1)}) lies on the line.', 'No', f'M1 substitutes x = {num(x1 + 2 * (x2 - x1))}: y = {num(y1 + 2 * (y2 - y1))}; A1 not equal so not on the line', 2),
    ]
    return cmp_(r, intro, parts)


t101.add('C4', (2, 3, 4, 5))(t101_c4)

# ---------------------------------------------------------------- midpoint and length
t102 = topic('Midpoint and length of a line segment', 'midpoint and length of a line segment', 'midpoint', 'length of a line segment')
t102.fixed('C1', (1, 2), [
    ('Find the midpoint of (2, 3) and (8, 7).', '(5, 5)', '((2 + 8)/2, (3 + 7)/2).', ['(6, 4)', '(10, 10)', '(3, 2)']),
    ('Find the length of the line joining (0, 0) and (3, 4).', '5', '√(3² + 4²) = 5.', ['7', '25', '√7']),
    ('The midpoint of AB is (4, 1) and A is (2, −3). What is B?', '(6, 5)', 'Add the step from A to M again: (4 + 2, 1 + 4).', ['(3, −1)', '(2, 4)', '(6, −1)']),
    ('Which theorem is used to find the length of a line segment from coordinates?', 'Pythagoras\' theorem', 'The horizontal and vertical changes are the shorter sides of a right-angled triangle.', ['The sine rule', 'The angle at the centre theorem', 'The midpoint theorem']),
])
t102.fixed('C2', (2, 3), [
    ('Explain why the length of a line segment uses (x₂ − x₁)² + (y₂ − y₁)².', 'The horizontal and vertical distances form the two shorter sides of a right-angled triangle with the segment as hypotenuse, so Pythagoras applies.', 'B1 right-angled triangle; B1 Pythagoras [2]'),
    ('Explain why the midpoint formula averages the coordinates.', 'The midpoint is halfway along in both directions, so each coordinate is the mean of the two end values.', 'B1 halfway in x and y; B1 mean [2]'),
])


@t102.add('C1', (1, 2, 3))
def t102_mid(r, D):
    x1, y1 = r.randint(-8, 8), r.randint(-8, 8)
    x2, y2 = r.randint(-8, 10), r.randint(-8, 10)
    if (x1, y1) == (x2, y2):
        return None
    if D <= 2 and ((x1 + x2) % 2 or (y1 + y2) % 2):
        return None
    mx, my = Fr(x1 + x2, 2), Fr(y1 + y2, 2)
    cor = pt(mx, my)
    ds = [pt(Fr(x2 - x1, 2), Fr(y2 - y1, 2)), pt(x1 + x2, y1 + y2), pt(mx, -my) if my else pt(mx + 1, my), pt(my, mx) if mx != my else pt(mx - 1, my)]
    return SMC(r, f'Find the midpoint of the line segment joining {pt(x1, y1)} and {pt(x2, y2)}.', cor, ds, f'Average the coordinates: ({num(x1)} + {num(x2)})/2 = {num(mx)}, ({num(y1)} + {num(y2)})/2 = {num(my)}.')


@t102.add('C3', (1, 2, 3, 4, 5))
def t102_len(r, D):
    x1, y1 = r.randint(-6, 6), r.randint(-6, 6)
    if D <= 2:
        dx, dy = r.choice([(3, 4), (6, 8), (5, 12), (8, 15), (9, 12), (4, 3), (12, 5)])
        dx *= r.choice([1, -1])
        dy *= r.choice([1, -1])
        L = math.isqrt(dx * dx + dy * dy)
        return Q(f'Find the length of the line segment joining {pt(x1, y1)} and {pt(x1 + dx, y1 + dy)}.', str(L), f'M1 √({nb(dx)}² + {nb(dy)}²); A1 {L} [2]')
    dx, dy = r.randint(-9, 9), r.randint(-9, 9)
    if dx == 0 or dy == 0:
        return None
    L2 = dx * dx + dy * dy
    if D == 3:
        return Q(f'Calculate the length of AB, where A is {pt(x1, y1)} and B is {pt(x1 + dx, y1 + dy)}. Give your answer correct to 3 significant figures.', n3(math.sqrt(L2)), f'M1 √({nb(dx)}² + {nb(dy)}²) = √{L2}; A1 {n3(math.sqrt(L2))} [2]')
    mx, my = Fr(2 * x1 + dx, 2), Fr(2 * y1 + dy, 2)
    if D == 4:
        return Q(f'A is {pt(x1, y1)} and the midpoint of AB is M{pt(mx, my)}. Find the coordinates of B and the length of AB, correct to 3 significant figures.', f'B{pt(x1 + dx, y1 + dy)}; AB = {n3(math.sqrt(L2))}',
                 f'M1 B = 2M − A; A1 {pt(x1 + dx, y1 + dy)}; M1 √({L2}); A1 {n3(math.sqrt(L2))} [4]', type='multi_step')
    k = r.choice([3, 4, 5, 6, 8, 10, 13])
    a = [x for x in [(3, 4), (4, 3), (6, 8), (8, 6), (5, 12), (12, 5)] if x[0] ** 2 + x[1] ** 2 == k * k] or None
    if not a:
        return None
    ax, ay = a[0]
    return Q(f'The points P{pt(x1, y1)} and Q({num(x1 + ax)}, t) are {k} units apart, where t > {num(y1)}. Find the value of t.', f't = {num(y1 + ay)}', f'M1 {ax}² + (t − {num(y1)})² = {k}²; M1 t − {num(y1)} = {ay}; A1 t = {num(y1 + ay)} [3]')


@t102.add('C2', (2, 3, 4), 'explain')
def t102_err(r, D):
    nm = person(r)
    x1, y1, x2, y2 = r.randint(-5, 3), r.randint(-5, 3), r.randint(4, 9), r.randint(4, 9)
    case = r.choice(['mid', 'len'])
    if case == 'mid':
        return Q(f'{nm} finds the midpoint of {pt(x1, y1)} and {pt(x2, y2)} as (({num(x2)} − {nb(x1)})/2, ({num(y2)} − {nb(y1)})/2) = {pt(Fr(x2 - x1, 2), Fr(y2 - y1, 2))}. Explain the mistake and find the correct midpoint.',
                 f'The coordinates must be added, not subtracted, before halving: {pt(Fr(x1 + x2, 2), Fr(y1 + y2, 2))}.', f'B1 add coordinates; B1 {pt(Fr(x1 + x2, 2), Fr(y1 + y2, 2))} [2]')
    dx, dy = x2 - x1, y2 - y1
    return Q(f'{nm} calculates the distance between {pt(x1, y1)} and {pt(x2, y2)} as {dx} + {dy} = {dx + dy}. Explain why this is wrong and find the correct distance to 3 significant figures.',
             f'Adding the horizontal and vertical distances gives the path along two sides, not the straight line. Use Pythagoras: √({dx}² + {dy}²) = {n3(math.hypot(dx, dy))}.', f'B1 must use Pythagoras; B1 {n3(math.hypot(dx, dy))} [2]')


def t102_c4(r, D):
    pts = [(r.randint(-5, 0), r.randint(-4, 2)), (r.randint(3, 8), r.randint(-4, 2)), (r.randint(0, 5), r.randint(4, 9))]
    (ax, ay), (bx, by), (cx, cy) = pts
    ab, bc, ca = math.hypot(bx - ax, by - ay), math.hypot(cx - bx, cy - by), math.hypot(ax - cx, ay - cy)
    mx, my = Fr(ax + bx, 2), Fr(ay + by, 2)
    intro = f'Triangle ABC has vertices A{pt(ax, ay)}, B{pt(bx, by)} and C{pt(cx, cy)}.'
    parts = [
        P('Find the midpoint M of AB.', pt(mx, my), 'B2 (B1 each coordinate)', 2),
        P('Calculate the length of AB, correct to 3 significant figures.', nn(ab), f'M1 √({nb(bx - ax)}² + {nb(by - ay)}²); A1 {nn(ab)}', 2),
        P('Calculate the perimeter of the triangle, correct to 3 significant figures.', n3(ab + bc + ca), f'M1 BC = {n3(bc)}, CA = {n3(ca)}; A1 {n3(ab + bc + ca)}', 2),
        P('Calculate the length of CM, correct to 3 significant figures.', n3(math.hypot(float(mx) - cx, float(my) - cy)), f'M1 Pythagoras with M; A1 {n3(math.hypot(float(mx) - cx, float(my) - cy))}', 2),
        P('Find the gradient of AB.', num(Fr(by - ay, bx - ax)), f'B1 {num(Fr(by - ay, bx - ax))}', 1),
    ]
    return cmp_(r, intro, parts)


t102.add('C4', (2, 3, 4, 5))(t102_c4)

# ---------------------------------------------------------------- parallel and perpendicular
t103 = topic('Equations of parallel and perpendicular lines', 'equations of parallel and perpendicular lines', 'parallel and perpendicular lines', 'perpendicular gradient')
t103.fixed('C1', (1, 2), [
    ('Which line is parallel to y = 3x + 1?', 'y = 3x − 5', 'Parallel lines have the same gradient.', ['y = −3x + 1', 'y = x/3 + 1', 'y = 1 − x/3']),
    ('What is the gradient of a line perpendicular to y = 2x − 7?', '−1/2', 'The product of perpendicular gradients is −1.', ['2', '−2', '1/2']),
    ('Two lines have gradients 4 and −1/4. The lines are', 'perpendicular', '4 × (−1/4) = −1.', ['parallel', 'the same line', 'neither parallel nor perpendicular']),
    ('What is the gradient of a line perpendicular to y = −(2/3)x + 4?', '3/2', 'Negative reciprocal of −2/3.', ['−3/2', '2/3', '−2/3']),
])
t103.fixed('C2', (2, 3), [
    ('Explain why parallel lines have the same gradient.', 'They never meet, so they must rise by the same amount for each unit across; that is, they have the same steepness.', 'B1 same steepness/never meet; B1 same gradient [2]'),
    ('Explain how to find the gradient of a line perpendicular to a line with gradient m.', 'Take the negative reciprocal, −1/m, because the product of the gradients of perpendicular lines is −1.', 'B1 −1/m; B1 product −1 [2]'),
])

GRADS = [Fr(2), Fr(3), Fr(-2), Fr(1, 2), Fr(-1, 3), Fr(4), Fr(-3), Fr(2, 3), Fr(-3, 4), Fr(5), Fr(-1, 2), Fr(1, 4)]


@t103.add('C1', (1, 2, 3))
def t103_perp(r, D):
    m = r.choice(GRADS)
    c = r.randint(-6, 6)
    p = -1 / m
    return MC(r, f'Find the gradient of a line perpendicular to {line_eq(m, c)}.', p, [m, -m, 1 / m, Fr(c) if Fr(c) not in (p, m) else m + 1], f'Negative reciprocal of {num(m)}: {num(p)}.')


@t103.add('C3', (1, 2, 3, 4, 5))
def t103_eq(r, D):
    m = r.choice(GRADS if D >= 3 else [Fr(2), Fr(3), Fr(-2), Fr(4), Fr(-3), Fr(5)])
    c = r.randint(-6, 6)
    x0, y0 = r.randint(-4, 6), r.randint(-5, 8)
    if D <= 2:
        cc = y0 - m * x0
        return Q(f'Find the equation of the line parallel to {line_eq(m, c)} that passes through {pt(x0, y0)}.', line_eq(m, cc), f'B1 gradient {num(m)}; M1 {num(y0)} = {num(m)} × {num(x0)} + c; A1 {line_eq(m, cc)} [3]')
    p = -1 / m
    if (p * x0).denominator != 1:
        x0 = x0 * p.denominator
    cc = y0 - p * x0
    if D == 3:
        return Q(f'Find the equation of the line perpendicular to {line_eq(m, c)} that passes through {pt(x0, y0)}.', line_eq(p, cc), f'B1 gradient {num(p)}; M1 substitutes {pt(x0, y0)}; A1 {line_eq(p, cc)} [3]')
    # perpendicular bisector
    for _ in range(30):
        ax, ay, bx, by = r.randint(-6, 4), r.randint(-5, 5), r.randint(-2, 8), r.randint(-3, 9)
        if (ax + bx) % 2 == 0 and (ay + by) % 2 == 0 and bx != ax and by != ay:
            break
    else:
        return None
    mab = Fr(by - ay, bx - ax)
    pp = -1 / mab
    mx, my = (ax + bx) // 2, (ay + by) // 2
    cc = my - pp * mx
    return Q(f'A is {pt(ax, ay)} and B is {pt(bx, by)}. Find the equation of the perpendicular bisector of AB.', line_eq(pp, cc),
             f'B1 midpoint {pt(mx, my)}; B1 gradient AB = {num(mab)}; M1 perpendicular gradient {num(pp)}; A1 {line_eq(pp, cc)} [4]')


@t103.add('C2', (2, 3, 4), 'explain')
def t103_check(r, D):
    nm = person(r)
    m = r.choice(GRADS)
    c1, c2 = r.randint(-5, 5), r.randint(-5, 5)
    case = r.choice(['recip', 'test'])
    if case == 'recip':
        return Q(f'{nm} says a line perpendicular to {line_eq(m, c1)} has gradient {num(1 / m)}. Explain the mistake and give the correct gradient.', f'{nm} took the reciprocal but forgot to change the sign. Perpendicular gradient = −1/({num(m)}) = {num(-1 / m)}.',
                 f'B1 negative reciprocal; B1 {num(-1 / m)} [2]')
    a, b = r.choice([(2, 1), (3, 1), (1, 2), (2, 3), (4, 1)])
    k = r.randint(1, 9)
    # line1: y = (a/b)x + c1 ; line2: a x + ... perpendicular: b x + a y = k -> y = -b/a x + k/a
    m2 = Fr(-b, a)
    return Q(f'Show that the lines {line_eq(Fr(a, b), c1)} and {expr((b, "x"), (a, "y"))} = {k} are perpendicular.', f'Gradients {num(Fr(a, b))} and {num(m2)}; product = {num(Fr(a, b) * m2)}, so perpendicular.',
             f'M1 rearranges to {line_eq(m2, Fr(k, a))}; A1 product of gradients −1 [2]')


def t103_c4(r, D):
    m = r.choice([Fr(2), Fr(-2), Fr(1, 2), Fr(3), Fr(-1, 3)])
    c = r.randint(-4, 6)
    x0 = r.randint(1, 6) * (m.denominator if (-1 / m).denominator != 1 else 1)
    p = -1 / m
    if (p * x0).denominator != 1:
        x0 *= p.denominator
    y0 = r.randint(-3, 8)
    if y0 == m * x0 + c:
        return None
    cc = y0 - p * x0
    xi = (cc - c) / (m - p)
    yi = m * xi + c
    intro = f'Line L₁ has equation {line_eq(m, c)}. Line L₂ is perpendicular to L₁ and passes through P{pt(x0, y0)}.'
    parts = [
        P('Write down the gradient of L₂.', num(p), f'B1 {num(p)}', 1),
        P('Find the equation of L₂ in the form y = mx + c.', line_eq(p, cc), f'M1 substitutes P; A1 {line_eq(p, cc)}', 2),
        P('Find the coordinates of the point where L₁ and L₂ intersect.', pt(xi, yi), f'M1 {lhs_mx(m, c)} = {lhs_mx(p, cc)}; A1 x = {num(xi)}; A1 y = {num(yi)}', 3),
        P(f'Find the equation of the line parallel to L₁ through P.', line_eq(m, y0 - m * x0), f'B1 {line_eq(m, y0 - m * x0)}', 1),
        P('Find the shortest distance from P to L₁, correct to 3 significant figures.', n3(math.hypot(float(xi) - x0, float(yi) - y0)), f'M1 distance from P to the intersection; A1 {n3(math.hypot(float(xi) - x0, float(yi) - y0))}', 2),
    ]
    return cmp_(r, intro, parts)


t103.add('C4', (2, 3, 4, 5))(t103_c4)

# ---------------------------------------------------------------- quadratic equations by factorising
t104 = topic('Solving quadratic equations by factorising', 'solving quadratic equations by factorising', 'quadratic equations', 'factorising quadratics')
t104.fixed('C1', (1, 2), [
    ('Solve (x − 3)(x + 5) = 0.', 'x = 3 or x = −5', 'One bracket must be zero.', ['x = −3 or x = 5', 'x = 3 or x = 5', 'x = −15']),
    ('Solve x² − 16 = 0.', 'x = 4 or x = −4', '(x − 4)(x + 4) = 0.', ['x = 4', 'x = 8 or x = −8', 'x = 16']),
    ('Solve x² − 5x = 0.', 'x = 0 or x = 5', 'x(x − 5) = 0.', ['x = 5', 'x = −5 or x = 0', 'x = √5']),
    ('If ab = 0, then', 'a = 0 or b = 0', 'The zero product property.', ['a = 0 and b = 0', 'a = b', 'a = 1 or b = 1']),
    ('Solve x² + 7x + 10 = 0.', 'x = −2 or x = −5', '(x + 2)(x + 5) = 0.', ['x = 2 or x = 5', 'x = −2 or x = 5', 'x = −10']),
])
t104.fixed('C2', (2, 3), [
    ('Explain why a quadratic equation must be rearranged to equal zero before factorising.', 'The method relies on the fact that if a product is zero one factor must be zero; this only works when the other side is 0.', 'B1 zero product property; B1 only works with 0 [2]'),
    ('Explain why you should not divide both sides of x² = 6x by x.', 'Dividing by x loses the solution x = 0. Instead write x² − 6x = 0, x(x − 6) = 0, so x = 0 or 6.', 'B1 loses x = 0; B1 correct solutions [2]'),
    ('Explain why some quadratic equations have only one distinct solution, using x² − 6x + 9 = 0.', '(x − 3)² = 0, so both factors give x = 3: a repeated root.', 'B1 perfect square; B1 repeated root x = 3 [2]'),
])


def roots_str(p, q, v='x'):
    a, b = Fr(p), Fr(q)
    if a == b:
        return f'{v} = {num(a)}'
    return f'{v} = {num(a)} or {v} = {num(b)}'


@t104.add('C1', (1, 2, 3))
def t104_pick(r, D):
    p, q = r.choice([-7, -5, -4, -3, -2, -1, 1, 2, 3, 4, 6]), r.choice([-6, -5, -3, -2, 1, 2, 3, 5, 7])
    if p == q or p == -q:
        return None
    cor = roots_str(-p, -q)
    ds = [roots_str(p, q), roots_str(-p, q), roots_str(p, -q), f'x = {num(p * q)}']
    return SMC(r, f'Solve {quad(1, p + q, p * q)} = 0.', cor, ds, f'{bracket(p)}{bracket(q)} = 0, so {cor}.')


@t104.add('C3', (1, 2, 3, 4, 5))
def t104_solve(r, D):
    if D == 1:
        k = r.randint(2, 9)
        return Q(f'Solve x² = {k * k}.', f'x = {k} or x = −{k}', f'B1 {k}; B1 −{k} [2]')
    if D == 2:
        p, q = r.randint(-9, 9) or 1, r.randint(-9, 9) or 2
        if p == q:
            return None
        return Q(f'Solve {quad(1, p + q, p * q)} = 0 by factorising.', roots_str(-p, -q), f'M1 {bracket(p)}{bracket(q)}; A1 {roots_str(-p, -q)} [2]')
    if D == 3:
        p, q = r.randint(-8, 8) or 3, r.randint(-8, 8) or 4
        # rearrange: x² + (p+q)x = -pq
        if p == q:
            return None
        rhs = -p * q
        lhs = expr((1, 'x²'), (p + q, 'x'))
        return Q(f'Solve {lhs} = {num(rhs)}.', roots_str(-p, -q), f'M1 rearranges to {quad(1, p + q, p * q)} = 0; M1 {bracket(p)}{bracket(q)}; A1 {roots_str(-p, -q)} [3]')
    A = r.choice([2, 3, 5])
    p, q = r.randint(-5, 5) or 1, r.randint(-6, 6) or 2
    pr = poly_mul([A, p], [1, q])
    if math.gcd(math.gcd(pr[0], pr[1]), pr[2]) != 1:
        return None
    if D == 4:
        return Q(f'Solve {poly_str(pr)} = 0.', roots_str(Fr(-p, A), -q), f'M1 {lb(A, p)}{bracket(q)}; A1 x = {num(Fr(-p, A))}; A1 x = {num(-q)} [3]')
    # fraction / context
    k = r.randint(2, 6)
    return Q(f'Solve the equation x + {k * (k + 1)}/x = {2 * k + 1}.', roots_str(k, k + 1),
             f'M1 multiplies by x: x² + {k * (k + 1)} = {2 * k + 1}x; M1 {quad(1, -(2 * k + 1), k * (k + 1))} = 0; M1 (x − {k})(x − {k + 1}) = 0; A1 {roots_str(k, k + 1)} [4]')


@t104.add('C3', (2, 3, 4, 5))
def t104_ctx(r, D):
    nm = person(r)
    case = r.choice(['rect', 'consec', 'tri'])
    if case == 'rect':
        w = r.randint(3, 12)
        d = r.randint(2, 7)
        A = w * (w + d)
        return Q(f'A rectangle has length (x + {d}) cm and width x cm. Its area is {A} cm². Form a quadratic equation and solve it to find the dimensions of the rectangle.',
                 f'{w} cm by {w + d} cm', f'B1 x(x + {d}) = {A}; M1 {quad(1, d, -A)} = 0; M1 (x − {w})(x + {w + d}) = 0; A1 x = {w} (reject −{w + d}), {w} by {w + d} [4]')
    if case == 'consec':
        n = r.randint(4, 15)
        return Q(f'The product of two consecutive positive integers is {n * (n + 1)}. Let the smaller integer be n. Form and solve an equation to find the integers.', f'{n} and {n + 1}',
                 f'B1 n(n + 1) = {n * (n + 1)}; M1 {quad(1, 1, -n * (n + 1), "n")} = 0; M1 (n − {n})(n + {n + 1}) = 0; A1 {n} and {n + 1} [4]')
    b = r.randint(2, 8)
    h = r.randint(4, 12)
    A = Fr(h * (h + b), 2)
    if A.denominator != 1:
        return None
    return Q(f'A triangle has base (x + {b}) cm and height x cm. Its area is {int(A)} cm². Show that x² + {b}x − {2 * int(A)} = 0 and solve it to find the height.', f'{h} cm',
             f'M1 ½x(x + {b}) = {int(A)}; A1 shown; M1 (x − {h})(x + {h + b}) = 0; A1 {h} cm [4]')


@t104.add('C2', (2, 3, 4), 'explain')
def t104_err(r, D):
    nm = person(r)
    case = r.choice(['div', 'nonzero', 'sign'])
    if case == 'div':
        k = r.randint(2, 9)
        return Q(f'{nm} solves x² = {k}x by dividing both sides by x to get x = {k}. Explain what {nm} has missed.', f'Dividing by x loses the solution x = 0. Correct: x² − {k}x = 0, x(x − {k}) = 0, so x = 0 or x = {k}.', f'B1 lost x = 0; B1 both solutions [2]')
    if case == 'nonzero':
        p, q = r.randint(1, 5), r.randint(1, 5)
        k = r.choice([2, 3, 6, 12])
        return Q(f'{nm} solves (x − {p})(x − {q}) = {k} by writing x − {p} = {k} or x − {q} = {k}. Explain why this method is wrong.', f'The zero product rule only works when the product is 0. Expand and rearrange: {quad(1, -(p + q), p * q - k)} = 0, then solve.',
                 'B1 only valid when product = 0; B1 expand and rearrange first [2]')
    p, q = r.randint(2, 8), r.randint(2, 8)
    if p == q:
        return None
    return Q(f'{nm} solves (x + {p})(x − {q}) = 0 and writes x = {p} or x = −{q}. Explain the mistake and give the correct solutions.', f'Each bracket is set to zero: x + {p} = 0 gives x = −{p} and x − {q} = 0 gives x = {q}.',
             f'B1 signs reversed; B1 x = −{p} or x = {q} [2]')


def t104_c4(r, D):
    t1, t2 = r.choice([(1, 3), (1, 4), (2, 3), (1, 5), (2, 4)])
    g = 5
    u = g * (t1 + t2)
    h0 = 0
    intro = f'A ball is thrown upwards. Its height h metres after t seconds is h = {u}t − 5t².'
    hmax_t = Fr(t1 + t2, 2)
    parts = [
        P(f'Find the times when the ball is at a height of {g * t1 * t2} m.', f't = {t1} or t = {t2}', f'M1 5t² − {u}t + {g * t1 * t2} = 0; M1 t² − {t1 + t2}t + {t1 * t2} = 0; M1 (t − {t1})(t − {t2}); A1 t = {t1} or {t2}', 4),
        P('Find when the ball hits the ground again.', f't = {t1 + t2} s', f'M1 5t({t1 + t2} − t) = 0; A1 t = {t1 + t2}', 2),
        P('Find the height of the ball after 1 second.', f'{u - 5} m', f'B1 {u} − 5 = {u - 5}', 1),
        P('Explain why there are two answers to the first part.', 'The ball passes that height once on the way up and once on the way down.', 'B1 up and down', 1),
        P('Find the greatest height of the ball.', f'{ex(float(u * hmax_t - 5 * hmax_t ** 2))} m', f'M1 t = {ex(float(hmax_t))} (midway between the roots); A1 {ex(float(u * hmax_t - 5 * hmax_t ** 2))}', 2),
    ]
    return cmp_(r, intro, parts)


t104.add('C4', (2, 3, 4, 5))(t104_c4)
CHAPTERS[10] = [t101, t102, t103, t104]


# =========================================================== 11 Pythagoras' theorem and similar shapes
TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41), (12, 35, 37)]


def triple(r, D):
    a, b, c = r.choice(TRIPLES[:3] if D <= 1 else TRIPLES)
    k = r.choice([1, 2, 3]) if c < 20 else 1
    if r.random() < 0.5:
        a, b = b, a
    return a * k, b * k, c * k


t111 = topic("Pythagoras' theorem and its applications including 3D", "pythagoras' theorem and its applications including 3d", "pythagoras' theorem", 'hypotenuse', '3D Pythagoras')
t111.fixed('C1', (1, 2), [
    ("In a right-angled triangle, which side is the hypotenuse?", 'The side opposite the right angle', 'The hypotenuse is the longest side, opposite the 90° angle.', ['The shortest side', 'The side next to the right angle', 'Any side of the triangle']),
    ("Which equation is Pythagoras' theorem for a right-angled triangle with hypotenuse c?", 'a² + b² = c²', 'The square on the hypotenuse equals the sum of the squares on the other two sides.', ['a + b = c', 'a² − b² = c²', 'a² + c² = b²']),
    ('A right-angled triangle has shorter sides 6 cm and 8 cm. How long is the hypotenuse?', '10 cm', '√(36 + 64) = √100 = 10.', ['14 cm', '100 cm', '√28 cm']),
    ('Which set of lengths could be the sides of a right-angled triangle?', '5, 12, 13', '25 + 144 = 169 = 13².', ['4, 5, 6', '6, 7, 9', '2, 3, 4']),
    ('A right-angled triangle has hypotenuse 13 cm and one side 5 cm. How long is the third side?', '12 cm', '√(169 − 25) = √144 = 12.', ['8 cm', '18 cm', '√194 cm']),
    ('The formula for the length of the space diagonal d of a cuboid with edges a, b and c is', 'd = √(a² + b² + c²)', "Apply Pythagoras' theorem twice: once on the base, then in the vertical triangle.", ['d = a + b + c', 'd = √(a² + b²) + c', 'd = a² + b² + c²']),
    ('A square has sides of 1 m. The length of its diagonal is', '√2 m', '√(1² + 1²) = √2.', ['2 m', '1 m', '1.5 m']),
])
t111.fixed('C2', (2, 3), [
    ("Explain how you can tell whether a triangle with sides 9 cm, 12 cm and 15 cm is right-angled.", 'Check whether the square of the longest side equals the sum of the squares of the other two: 9² + 12² = 81 + 144 = 225 = 15², so it is right-angled.', 'M1 compares 9² + 12² with 15²; A1 equal, so right-angled [2]'),
    ("Explain why the hypotenuse is always the longest side of a right-angled triangle.", 'c² = a² + b² is greater than a² and greater than b², since both squares are positive, so c is greater than a and b.', 'B1 c² = a² + b² > a², b²; B1 so c is longest [2]'),
    ("Explain how Pythagoras' theorem is used twice to find the longest rod that fits inside a cuboid.", 'First find the diagonal of the base from the length and width; then use that diagonal and the height as the shorter sides of a vertical right-angled triangle to find the space diagonal.', 'B1 base diagonal; B1 second triangle with height [2]'),
])


@t111.add('C1', (1, 2, 3))
def t111_hyp(r, D):
    a, b, c = triple(r, D)
    if D <= 2 or r.random() < 0.5:
        return MC(r, f'A right-angled triangle has shorter sides {a} cm and {b} cm. Find the length of the hypotenuse.', c, [a + b, a * a + b * b, abs(b - a) or c + 2, c + 1], f'√({a}² + {b}²) = √{c * c} = {c}.', unit=' cm')
    return MC(r, f'A right-angled triangle has hypotenuse {c} cm and one shorter side {a} cm. Find the length of the third side.', b, [c - a, c + a, round(math.sqrt(a * a + c * c), 1), b + 1], f'√({c}² − {a}²) = √{b * b} = {b}.', unit=' cm')


@t111.add('C3', (1, 2, 3, 4, 5))
def t111_calc(r, D):
    if D == 1:
        a, b, c = triple(r, 1)
        return Q(f'A right-angled triangle has shorter sides of length {a} cm and {b} cm. Calculate the length of the hypotenuse.', f'{c} cm', f'M1 {a}² + {b}² = {c * c}; A1 {c} cm [2]')
    if D == 2:
        a, b, c = triple(r, 2)
        return Q(f'In triangle PQR, angle Q = 90°, PR = {c} cm and PQ = {a} cm. Calculate QR.', f'{b} cm', f'M1 {c}² − {a}² = {b * b}; A1 {b} cm [2]')
    if D == 3:
        a, b = r.randint(23, 99) / 10, r.randint(23, 99) / 10
        if abs(a - b) < 0.5:
            return None
        if r.random() < 0.5:
            h = math.hypot(a, b)
            return Q(f'Triangle ABC has a right angle at B. AB = {ex(a)} m and BC = {ex(b)} m. Calculate AC, giving your answer correct to 3 significant figures.', f'{n3(h)} m', f'M1 {ex(a)}² + {ex(b)}²; A1 {n3(h)} m [2]')
        hi, lo = max(a, b), min(a, b)
        s = math.sqrt(hi * hi - lo * lo)
        return Q(f'Triangle ABC has a right angle at B. The hypotenuse AC = {ex(hi)} m and AB = {ex(lo)} m. Calculate BC, giving your answer correct to 3 significant figures.', f'{n3(s)} m', f'M1 {ex(hi)}² − {ex(lo)}²; A1 {n3(s)} m [2]')
    if D == 4:
        l, w, h = r.randint(4, 15), r.randint(3, 12), r.randint(2, 10)
        bd = math.hypot(l, w)
        d = math.sqrt(l * l + w * w + h * h)
        obj = r.choice(['box', 'storage container', 'fish tank', 'packing crate'])
        return Q(f'A cuboid-shaped {obj} measures {l} cm by {w} cm by {h} cm. Calculate the length of the longest straight rod that can fit inside it, correct to 3 significant figures.', f'{n3(d)} cm',
                 f'M1 base diagonal √({l}² + {w}²) = {n3(bd)}; M1 √({l}² + {w}² + {h}²); A1 {n3(d)} cm [3]', type='multi_step')
    s, e = r.randint(4, 12), r.randint(6, 16)
    if e * e <= s * s / 2 + 4:
        return None
    hd = s * math.sqrt(2) / 2
    h = math.sqrt(e * e - s * s / 2)
    return Q(f'A square-based pyramid has base edges of {s} cm. Each sloping edge from the apex to a corner of the base is {e} cm. The apex is vertically above the centre of the base. Calculate the vertical height of the pyramid, correct to 3 significant figures.', f'{n3(h)} cm',
             f'M1 base diagonal √({s}² + {s}²) = {n3(2 * hd)}; M1 half-diagonal {n3(hd)}; M1 √({e}² − {n3(hd)}²); A1 {n3(h)} cm [4]', type='multi_step')


@t111.add('C3', (2, 3, 4, 5))
def t111_ctx(r, D):
    nm = person(r)
    case = r.choice(['ladder', 'ship', 'field', 'screen'] + (['slide'] if D >= 4 else []))
    if case == 'ladder':
        L, d = r.choice([5, 6, 7, 8, 9]) + r.choice([0, 0.5]), r.choice([1.2, 1.5, 1.8, 2, 2.4])
        h = math.sqrt(L * L - d * d)
        return Q(f'{nm} leans a {ex(L)} m ladder against a vertical wall on level ground. The foot of the ladder is {ex(d)} m from the wall. Calculate how far up the wall the ladder reaches, correct to 3 significant figures.', f'{n3(h)} m', f'M1 {ex(L)}² − {ex(d)}²; A1 {n3(h)} m [2]')
    if case == 'ship':
        a, b = r.randint(12, 60), r.randint(12, 60)
        d1, d2 = r.choice([('north', 'east'), ('south', 'west'), ('east', 'south'), ('west', 'north')])
        h = math.hypot(a, b)
        return Q(f'A ship leaves the port of {city(r)} and sails {a} km due {d1}, then {b} km due {d2}. Calculate the direct distance of the ship from the port, correct to 3 significant figures.', f'{n3(h)} km', f'M1 √({a}² + {b}²); A1 {n3(h)} km [2]')
    if case == 'field':
        l, w = r.randint(60, 150), r.randint(30, 90)
        dg = math.hypot(l, w)
        sv = l + w - dg
        return Q(f'A rectangular park in {city(r)} is {l} m long and {w} m wide. {nm} walks diagonally across the park from one corner to the opposite corner instead of along two edges. Calculate how much shorter this route is, correct to 3 significant figures.', f'{n3(sv)} m',
                 f'M1 √({l}² + {w}²) = {n3(dg)}; M1 ({l} + {w}) − {n3(dg)}; A1 {n3(sv)} m [3]', type='multi_step')
    if case == 'screen':
        w, h = r.choice([(16, 9), (4, 3), (21, 9)])
        k = r.choice([4, 5, 6, 7, 8])
        W, H = w * k, h * k
        dg = math.hypot(W, H)
        return Q(f'A rectangular screen is {W} cm wide and {H} cm high. Screen sizes are given by the length of the diagonal. Calculate the screen size, correct to 3 significant figures.', f'{n3(dg)} cm', f'M1 √({W}² + {H}²); A1 {n3(dg)} cm [2]')
    L = r.choice([5, 6.5, 8, 10])
    d1 = r.choice([1.2, 1.5, 2])
    d2 = d1 + r.choice([0.5, 0.8, 1])
    h1, h2 = math.sqrt(L * L - d1 * d1), math.sqrt(L * L - d2 * d2)
    return Q(f'A {ex(L)} m ladder leans against a vertical wall with its foot {ex(d1)} m from the wall. The foot slips until it is {ex(d2)} m from the wall. Calculate how far the top of the ladder slides down the wall, correct to 3 significant figures.', f'{n3(h1 - h2)} m',
             f'M1 √({ex(L)}² − {ex(d1)}²) = {n3(h1)}; M1 √({ex(L)}² − {ex(d2)}²) = {n3(h2)}; A1 {n3(h1 - h2)} m [3]', type='multi_step')


@t111.add('C2', (2, 3, 4), 'explain')
def t111_err(r, D):
    nm = person(r)
    case = r.choice(['converse', 'add', 'longest'])
    if case == 'converse':
        a, b, c = triple(r, 2)
        if r.random() < 0.5:
            c += r.choice([1, -1])
        right = a * a + b * b == c * c
        return Q(f'A triangle has sides of {a} cm, {b} cm and {c} cm. Determine, showing your working, whether the triangle is right-angled.', ('Yes' if right else 'No') + f': {a}² + {b}² = {a * a + b * b} and {c}² = {c * c}' + (', which are equal.' if right else ', which are not equal.'),
                 f'M1 {a}² + {b}² = {a * a + b * b}; M1 {c}² = {c * c}; A1 correct conclusion [3]')
    if case == 'add':
        a, b, c = triple(r, 3)
        wrong = math.sqrt(c * c + a * a)
        return Q(f'A right-angled triangle has hypotenuse {c} cm and another side {a} cm. {nm} works out the third side as √({c}² + {a}²) = {n3(wrong)} cm. Explain the mistake and find the correct length.',
                 f'When finding a shorter side the squares must be subtracted: √({c}² − {a}²) = {b} cm. The answer {n3(wrong)} cm is longer than the hypotenuse, which is impossible.', f'B1 subtract when finding a shorter side; B1 {b} cm [2]')
    a, b = r.randint(5, 12), r.randint(13, 20)
    s = math.sqrt(b * b - a * a)
    h = math.hypot(a, b)
    return Q(f'A right-angled triangle has two sides of {a} cm and {b} cm. {nm} says the third side must be {n3(h)} cm. Explain why there is another possible answer, and find it.',
             f'{nm} assumed {b} cm is a shorter side. If {b} cm is the hypotenuse, the third side is √({b}² − {a}²) = {nn(s)} cm.', f'B1 {b} could be the hypotenuse; B1 {nn(s)} cm [2]')


def t111_c4(r, D):
    nm = person(r)
    if r.random() < 0.5:
        l, w, h = r.randint(20, 60), r.randint(15, 40), r.randint(10, 35)
        bd = math.hypot(l, w)
        sd = math.sqrt(l * l + w * w + h * h)
        rod = int(sd) + r.choice([-2, -1, 1, 2])
        fd = math.hypot(w, h)
        intro = f'{nm} has a cuboid-shaped box that measures {l} cm long, {w} cm wide and {h} cm high.'
        parts = [
            P('Calculate the length of the diagonal of the base of the box.', f'{n3(bd)} cm', f'M1 √({l}² + {w}²); A1 {n3(bd)}', 2),
            P('Calculate the length of the longest straight line that can be drawn inside the box, from a bottom corner to the opposite top corner.', f'{n3(sd)} cm', f'M1 √({l}² + {w}² + {h}²); A1 {n3(sd)}', 2),
            P(f'Decide whether a thin rod of length {rod} cm will fit inside the box. Show your working.', 'Yes' if rod <= sd else 'No', f'M1 compares {rod} with space diagonal {n3(sd)}; A1 {"fits" if rod <= sd else "does not fit"}', 2),
            P(f'Calculate the length of a diagonal of one of the {w} cm by {h} cm end faces.', f'{n3(fd)} cm', f'B1 √({w}² + {h}²) = {n3(fd)}', 1),
        ]
        return cmp_(r, intro, parts)
    b, s = r.randint(6, 20), r.randint(8, 25)
    if 2 * s <= b + 2:
        return None
    hgt = math.sqrt(s * s - (b / 2) ** 2)
    area = b * hgt / 2
    intro = f'A roof truss for a house in {city(r)} is in the shape of an isosceles triangle ABC with AB = AC = {s} m and base BC = {b} m. M is the midpoint of BC.'
    parts = [
        P('Explain why AM is perpendicular to BC.', 'Triangles ABM and ACM are congruent (SSS), so angles AMB and AMC are equal; they add to 180°, so each is 90°.', 'B1 congruent triangles or symmetry; B1 angles equal and sum to 180°', 2),
        P('Calculate the height AM of the truss.', f'{n3(hgt)} m', f'M1 √({s}² − {ex(b / 2)}²); A1 {n3(hgt)}', 2),
        P('Calculate the area of triangle ABC.', f'{n3(area)} m²', f'M1 ½ × {b} × {n3(hgt)}; A1 {n3(area)}', 2),
        P(f'A support runs from M to the midpoint N of AC. Calculate MN.', f'{ex(s / 2)} m', f'B1 MN = ½AB = {ex(s / 2)} (midpoint theorem) or by coordinates', 1),
    ]
    return cmp_(r, intro, parts)


t111.add('C4', (2, 3, 4, 5))(t111_c4)


# ---------------------------------------------------------------- similar triangles
t112 = topic('Similar triangles: scale factor and finding unknown lengths', 'similar triangles: scale factor and finding unknown lengths', 'similar triangles', 'scale factor')
t112.fixed('C1', (1, 2), [
    ('Two triangles are similar. Which statement must be true?', 'Their corresponding angles are equal', 'Similar shapes are enlargements of each other, so angles are unchanged.', ['Their corresponding sides are equal', 'Their areas are equal', 'Their perimeters are equal']),
    ('Triangle ABC is similar to triangle PQR, with AB = 4 cm and PQ = 12 cm. What is the scale factor from ABC to PQR?', '3', '12 ÷ 4 = 3.', ['1/3', '8', '16']),
    ('Which pair of shapes is always similar?', 'Two squares', 'All angles are 90° and all sides are in the same ratio.', ['Two rectangles', 'Two isosceles triangles', 'Two right-angled triangles']),
    ('A triangle has sides 3 cm, 4 cm and 5 cm. A similar triangle has shortest side 6 cm. Its longest side is', '10 cm', 'Scale factor 6 ÷ 3 = 2, so 5 × 2 = 10.', ['8 cm', '8 cm or 10 cm', '15 cm']),
    ('In triangle ABC, D is on AB and E is on AC with DE parallel to BC. Which two triangles are similar?', 'ADE and ABC', 'Corresponding angles ADE = ABC and AED = ACB, and angle A is common.', ['ADE and DBE', 'BDE and CDE', 'ABE and ACD']),
    ('Two triangles have angles of 40°, 60°, 80° and 80°, 40°, 60°. The triangles are', 'similar', 'All three pairs of angles are equal.', ['congruent', 'not similar', 'similar only if they have equal areas']),
])
t112.fixed('C2', (2, 3), [
    ('Explain why showing that two pairs of angles are equal is enough to prove two triangles are similar.', 'The angles of a triangle add to 180°, so the third pair of angles must also be equal; triangles with all corresponding angles equal are similar.', 'B1 third angles equal (angle sum 180°); B1 all angles equal so similar [2]'),
    ('Explain the difference between similar and congruent triangles.', 'Similar triangles have equal angles and sides in the same ratio (one is an enlargement of the other); congruent triangles are identical, with equal sides as well (scale factor 1).', 'B1 similar: same shape, sides in proportion; B1 congruent: same shape and size [2]'),
    ('Explain why two rectangles are not necessarily similar.', 'All their angles are 90°, but the ratio of length to width can differ (for example 2 cm by 1 cm and 3 cm by 1 cm), so the sides need not be in proportion.', 'B1 angles equal is not enough; B1 sides not in same ratio, with example [2]'),
])

TRI_SIDES = [(4, 6, 7), (5, 8, 10), (6, 9, 12), (3, 5, 7), (8, 10, 14), (4, 7, 9), (6, 8, 11), (5, 6, 9)]
SFS = [Fr(2), Fr(3), Fr(3, 2), Fr(5, 2), Fr(4), Fr(4, 3), Fr(5, 4), Fr(1, 2)]


def scaled(r, D):
    a, b, c = r.choice(TRI_SIDES)
    k = r.choice(SFS[:2] + [Fr(4)] if D <= 2 else SFS)
    if any((x * k).denominator != 1 and (x * k * 10).denominator != 1 for x in (a, b, c)):
        return None
    return (a, b, c), k


@t112.add('C1', (1, 2, 3))
def t112_sf(r, D):
    p = scaled(r, D)
    if not p:
        return None
    (a, b, c), k = p
    L = ['AB', 'BC', 'CA']
    M = ['PQ', 'QR', 'RP']
    i, j = r.sample(range(3), 2)
    s = (a, b, c)
    ans = s[j] * k
    return MC(r, f'Triangle ABC is similar to triangle PQR, with A, B and C corresponding to P, Q and R. AB = {a} cm, BC = {b} cm, CA = {c} cm and {M[i]} = {num(s[i] * k)} cm. Find {M[j]}.', ans,
              [s[j] + (s[i] * k - s[i]), s[j] / k, s[i] * k, ans + 1], f'Scale factor {num(s[i] * k)} ÷ {s[i]} = {num(k)}; {M[j]} = {s[j]} × {num(k)} = {num(ans)}.', fmtf=lambda x: ex(float(x)), unit=' cm')


@t112.add('C3', (1, 2, 3, 4, 5))
def t112_len(r, D):
    if D <= 3:
        p = scaled(r, D)
        if not p:
            return None
        (a, b, c), k = p
        if k < 1:
            k = 1 / k
            if any((x * k).denominator != 1 and (x * k * 10).denominator != 1 for x in (a, b, c)):
                return None
        sh = r.choice(['triangles', 'triangular flags', 'triangular tiles', 'triangular sails'])
        if D <= 2 and r.random() < 0.5:
            return Q(f'Two {sh} are similar. The smaller one has sides {a} cm, {b} cm and {c} cm. The longest side of the larger one is {ex(float(c * k))} cm. Calculate the lengths of its other two sides.', f'{ex(float(a * k))} cm and {ex(float(b * k))} cm',
                     f'M1 scale factor {ex(float(c * k))} ÷ {c} = {ex(float(k))}; A1 {ex(float(a * k))}; A1 {ex(float(b * k))} [3]')
        return Q(f'Two {sh} are similar. The larger one has sides {ex(float(a * k))} cm, {ex(float(b * k))} cm and {ex(float(c * k))} cm. The shortest side of the smaller one is {a} cm. Calculate the perimeter of the smaller one.', f'{a + b + c} cm',
                 f'M1 scale factor {ex(float(k))}; M1 divides lengths by {ex(float(k))}; A1 {a + b + c} cm [3]')
    # nested triangles DE ∥ BC
    ad, db = r.randint(2, 9), r.randint(2, 9)
    de = r.randint(3, 10)
    k = Fr(ad + db, ad)
    bc = de * k
    if (bc * 10).denominator != 1:
        return None
    ae = r.randint(2, 8)
    ac = ae * k
    if (ac * 10).denominator != 1:
        return None
    if D == 4:
        return Q(f'In triangle ABC, D lies on AB and E lies on AC so that DE is parallel to BC. AD = {ad} cm, DB = {db} cm, DE = {de} cm and AE = {ae} cm. Calculate (a) BC (b) EC.', f'(a) {ex(float(bc))} cm (b) {ex(float(ac - ae))} cm',
                     f'M1 triangles ADE and ABC similar; M1 scale factor {ad + db}/{ad}; A1 BC = {ex(float(bc))}; A1 EC = {ex(float(ac))} − {ae} = {ex(float(ac - ae))} [4]', type='multi_step')
    return Q(f'In triangle ABC, D lies on AB and E lies on AC so that DE is parallel to BC. AD = {ad} cm, DE = {de} cm and BC = {ex(float(bc))} cm. Calculate DB.', f'{db} cm',
             f'M1 scale factor {ex(float(bc))} ÷ {de}; M1 AB = {ad} × that = {ad + db}; A1 DB = {db} cm [3]')


@t112.add('C3', (2, 3, 4, 5))
def t112_ctx(r, D):
    nm = person(r)
    if D <= 3:
        h = r.choice([1.2, 1.5, 1.6, 1.8, 2])
        s = r.choice([0.8, 1.2, 1.5, 2, 2.4, 3])
        S = r.randint(6, 30)
        obj = r.choice(['tree', 'flagpole', 'lamp post', 'tower'])
        T = h * S / s
        return Q(f'At the same time of day in {city(r)}, a vertical stick of height {ex(h)} m casts a shadow {ex(s)} m long and a vertical {obj} casts a shadow {S} m long. Calculate the height of the {obj}, correct to 3 significant figures.', f'{n3(T)} m',
                 f'M1 similar triangles: height ÷ shadow equal; M1 {ex(h)} × {S} ÷ {ex(s)}; A1 {n3(T)} m [3]')
    p = r.choice([1.5, 1.6, 1.7, 1.8])
    d, s = r.randint(3, 9), r.choice([1.5, 2, 2.5, 3])
    L = p * (d + s) / s
    return Q(f'{nm}, who is {ex(p)} m tall, stands {d} m from the foot of a vertical street lamp. {nm}\'s shadow is {ex(s)} m long. Calculate the height of the lamp, correct to 3 significant figures.', f'{n3(L)} m',
             f'M1 similar triangles with bases {ex(s)} and {d} + {ex(s)} = {ex(d + s)}; M1 {ex(p)} × {ex(d + s)} ÷ {ex(s)}; A1 {n3(L)} m [3]', type='multi_step')


@t112.add('C2', (2, 3, 4), 'explain')
def t112_err(r, D):
    nm = person(r)
    case = r.choice(['add', 'part', 'why'])
    if case == 'add':
        a, b, c = r.choice([(4, 6, 8), (3, 5, 6), (5, 7, 9), (6, 8, 10)])
        d = r.choice([2, 3])
        return Q(f'Triangle X has sides {a} cm, {b} cm and {c} cm. Triangle Y has sides {a + d} cm, {b + d} cm and {c + d} cm. {nm} says the triangles are similar because every side has increased by {d} cm. Explain why {nm} is wrong.',
                 f'Similar shapes need sides in the same ratio, not the same difference: {a + d}/{a} = {n3((a + d) / a)} but {c + d}/{c} = {n3((c + d) / c)}, so the triangles are not similar.', f'B1 ratios must be equal; B1 shows two different ratios [2]')
    if case == 'part':
        ad, db, de = r.randint(2, 6), r.randint(2, 6), r.randint(3, 9)
        if ad == db:
            return None
        wrong = Fr(de * db, ad)
        right = Fr(de * (ad + db), ad)
        return Q(f'In triangle ABC, DE is parallel to BC with D on AB and E on AC. AD = {ad} cm, DB = {db} cm and DE = {de} cm. {nm} writes BC = {de} × {db}/{ad} = {ex(float(wrong))} cm. Explain the mistake and find BC.',
                 f'The scale factor compares AB with AD, and AB = {ad} + {db} = {ad + db}, not DB. BC = {de} × {ad + db}/{ad} = {ex(float(right))} cm.', f'B1 must use AB = {ad + db}; B1 BC = {ex(float(right))} cm [2]')
    a1, a2 = r.randint(30, 70), r.randint(40, 80)
    return Q(f'Triangle LMN has angle L = {a1}° and angle M = {a2}°. Triangle XYZ has angle X = {a1}° and angle Z = {180 - a1 - a2}°. Explain whether the triangles are similar.',
             f'Angle N = 180 − {a1} − {a2} = {180 - a1 - a2}° and angle Y = 180 − {a1} − {180 - a1 - a2} = {a2}°, so all three pairs of angles are equal and the triangles are similar.', f'B1 finds the missing angles; B1 all angles equal so similar [2]')


def t112_c4(r, D):
    k = r.choice([Fr(2), Fr(3, 2), Fr(5, 2), Fr(3), Fr(4, 3)])
    for _ in range(30):
        p, a, b = (r.randint(3, 9) * k.denominator for _ in range(3))
        if a + b > p and a + p > b and b + p > a and len({p, a, b}) == 3:
            break
    else:
        return None
    q, dx, cx = p * k, a * k, b * k
    intro = f'The lines AD and BC cross at X. AB is parallel to CD. AB = {p} cm, CD = {num(q)} cm, AX = {a} cm and CX = {num(cx)} cm.'
    parts = [
        P('Explain why triangles ABX and DCX are similar.', 'Angle BAX = angle CDX and angle ABX = angle DCX (alternate angles, AB ∥ CD); angles AXB and DXC are vertically opposite, so all angles are equal.', 'B1 alternate angles; B1 vertically opposite or third angle', 2),
        P('Find the scale factor of the enlargement from triangle ABX to triangle DCX.', num(k), f'B1 {num(q)} ÷ {p} = {num(k)}', 1),
        P('Calculate DX.', f'{num(dx)} cm', f'M1 {a} × {num(k)}; A1 {num(dx)}', 2),
        P('Calculate BX.', f'{num(b)} cm', f'M1 {num(cx)} ÷ {num(k)}; A1 {num(b)}', 2),
        P('Calculate the length of AD.', f'{num(a + dx)} cm', f'B1 {a} + {num(dx)} = {num(a + dx)}', 1),
    ]
    return cmp_(r, intro, parts)


t112.add('C4', (2, 3, 4, 5))(t112_c4)


# ---------------------------------------------------------------- areas and volumes of similar shapes
t113 = topic('Areas and volumes of similar shapes', 'areas and volumes of similar shapes', 'area scale factor', 'volume scale factor')
t113.fixed('C1', (1, 2), [
    ('Two similar shapes have lengths in the ratio 1 : 3. What is the ratio of their areas?', '1 : 9', 'Area ratio is the square of the length ratio.', ['1 : 3', '1 : 6', '1 : 27']),
    ('Two similar solids have lengths in the ratio 1 : 2. What is the ratio of their volumes?', '1 : 8', 'Volume ratio is the cube of the length ratio.', ['1 : 2', '1 : 4', '1 : 6']),
    ('Two similar cylinders have volumes in the ratio 8 : 27. What is the ratio of their heights?', '2 : 3', 'Take cube roots: ∛8 : ∛27.', ['8 : 27', '4 : 9', '64 : 729']),
    ('Every length of a solid is doubled. Its surface area is multiplied by', '4', 'Area scale factor = 2² = 4.', ['2', '6', '8']),
    ('Two similar solids have surface areas in the ratio 25 : 49. What is the ratio of their volumes?', '125 : 343', 'Length ratio 5 : 7, so volume ratio 5³ : 7³.', ['25 : 49', '5 : 7', '625 : 2401']),
    ('Two similar shapes have areas in the ratio 16 : 9. What is the ratio of their corresponding lengths?', '4 : 3', 'Take square roots.', ['16 : 9', '8 : 4.5', '64 : 27']),
])
t113.fixed('C2', (2, 3), [
    ('Explain why, if the lengths of a shape are multiplied by k, its area is multiplied by k².', 'Area is found by multiplying two lengths together, and each is multiplied by k, so the area is multiplied by k × k = k².', 'B1 area uses two lengths; B1 k × k = k² [2]'),
    ('Explain why two cylinders with the same height but different radii are not similar.', 'For similarity every length must be multiplied by the same scale factor; here the radius changes but the height does not.', 'B1 all lengths must be scaled; B1 height unchanged [2]'),
    ('Explain why the mass of a solid statue grows much faster than its height when similar statues are made larger.', 'Mass is proportional to volume, which scales by the cube of the length scale factor, whereas height scales only by the factor itself.', 'B1 mass ∝ volume; B1 volume factor k³ [2]'),
])

RATIOS = [(1, 2), (2, 3), (1, 3), (3, 4), (2, 5), (3, 5), (1, 4), (4, 5)]


@t113.add('C1', (1, 2, 3))
def t113_ratio(r, D):
    a, b = r.choice(RATIOS)
    what = r.choice(['area', 'volume'] if D >= 2 else ['area'])
    if what == 'area':
        cor = f'{a * a} : {b * b}'
        ds = [f'{a} : {b}', f'{a ** 3} : {b ** 3}', f'{2 * a} : {2 * b}']
    else:
        cor = f'{a ** 3} : {b ** 3}'
        ds = [f'{a} : {b}', f'{a * a} : {b * b}', f'{3 * a} : {3 * b}']
    sh = r.choice(['jugs', 'model cars', 'pyramids', 'statues', 'boxes'])
    return SMC(r, f'Two similar {sh} have heights in the ratio {a} : {b}. What is the ratio of their {"surface areas" if what == "area" else "volumes"}?', cor, ds,
               f'{"Square" if what == "area" else "Cube"} each part of the length ratio: {cor}.')


@t113.add('C3', (1, 2, 3, 4, 5))
def t113_calc(r, D):
    a, b = r.choice(RATIOS)
    k = Fr(b, a)
    if D == 1:
        A = r.randint(3, 20) * a * a
        sh = r.choice(['photographs', 'triangles', 'logos', 'maps'])
        return Q(f'Two similar {sh} have corresponding lengths of {2 * a} cm and {2 * b} cm. The smaller one has an area of {A} cm². Calculate the area of the larger one.',
                 f'{num(A * k * k)} cm²', f'M1 area factor ({b}/{a})² = {num(k * k)}; A1 {num(A * k * k)} cm² [2]')
    if D == 2:
        V = r.randint(2, 12) * a ** 3
        sh = r.choice(['cones', 'cylinders', 'prisms', 'pyramids'])
        return Q(f'Two similar {sh} have heights {3 * a} cm and {3 * b} cm. The volume of the smaller one is {V} cm³. Calculate the volume of the larger one.', f'{num(V * k ** 3)} cm³',
                 f'M1 volume factor ({b}/{a})³ = {num(k ** 3)}; A1 {num(V * k ** 3)} cm³ [2]')
    if D == 3:
        A1 = r.randint(2, 10) * a * a
        A2 = A1 * k * k
        h = r.randint(2, 9) * a
        return Q(f'Two similar cylinders have surface areas {num(A1)} cm² and {num(A2)} cm². The smaller cylinder has height {h} cm. Calculate the height of the larger cylinder.', f'{num(h * k)} cm',
                 f'M1 area factor {num(A2)} ÷ {num(A1)} = {num(k * k)}; M1 length factor √{num(k * k)} = {num(k)}; A1 {num(h * k)} cm [3]')
    if D == 4:
        V1 = r.randint(2, 6) * a ** 3
        V2 = V1 * k ** 3
        S1 = r.randint(3, 15) * a * a
        return Q(f'Two similar solids have volumes {num(V1)} cm³ and {num(V2)} cm³. The surface area of the smaller solid is {num(S1)} cm². Calculate the surface area of the larger solid.', f'{num(S1 * k * k)} cm²',
                 f'M1 volume factor {num(k ** 3)}; M1 length factor ∛{num(k ** 3)} = {num(k)}; M1 area factor {num(k * k)}; A1 {num(S1 * k * k)} cm² [4]', type='multi_step')
    c1 = r.choice([250, 330, 400, 500, 750])
    h1 = r.choice([12, 15, 16, 18, 20])
    c2 = r.choice([1000, 1500, 2000, 2500])
    kk = (c2 / c1) ** (1 / 3)
    h2 = h1 * kk
    item = r.choice(['bottles', 'jugs', 'vases'])
    return Q(f'Two mathematically similar {item} have capacities of {c1} ml and {ex(c2 / 1000)} litres. The smaller one is {h1} cm tall. Calculate the height of the larger one, correct to 3 significant figures.', f'{n3(h2)} cm',
             f'B1 {ex(c2 / 1000)} litres = {c2} ml; M1 volume factor {c2}/{c1} = {nn(c2 / c1)}; M1 length factor ∛({c2}/{c1}) = {n3(kk)}; A1 {n3(h2)} cm [4]', type='multi_step')


@t113.add('C2', (2, 3, 4), 'explain')
def t113_err(r, D):
    nm = person(r)
    a, b = r.choice(RATIOS)
    k = Fr(b, a)
    case = r.choice(['vol', 'area'])
    if case == 'vol':
        V = r.randint(2, 9) * a ** 3
        return Q(f'Two similar jars have heights {a * 5} cm and {b * 5} cm. The smaller jar holds {V} ml. {nm} says the larger jar holds {V} × {b}/{a} = {num(V * k)} ml. Explain the mistake and find the correct capacity.',
                 f'Capacity is a volume, so the length scale factor must be cubed: {V} × ({b}/{a})³ = {num(V * k ** 3)} ml.', f'B1 must cube the length factor; B1 {num(V * k ** 3)} ml [2]')
    A = r.randint(2, 9) * a * a
    return Q(f'Two similar shapes have areas {A} cm² and {num(A * k * k)} cm². {nm} says the length scale factor is {num(A * k * k)} ÷ {A} = {num(k * k)}. Explain the mistake and give the correct length scale factor.',
             f'{num(k * k)} is the area scale factor; the length scale factor is its square root, {num(k)}.', f'B1 area factor = k²; B1 k = {num(k)} [2]')


def t113_c4(r, D):
    a, b = r.choice([(1, 2), (2, 3), (3, 4), (2, 5), (3, 5)])
    k = Fr(b, a)
    h1 = 4 * a * r.randint(1, 3)
    h2 = h1 * k
    m1 = r.randint(2, 9) * a ** 3 * 10
    S1 = r.randint(5, 20) * a * a * 10
    cost = r.choice([0.02, 0.03, 0.05])
    item = r.choice(['statues', 'trophies', 'garden ornaments'])
    intro = f'A company in {city(r)} makes two mathematically similar solid {item} from the same metal. The small one is {h1} cm tall and the large one is {num(h2)} cm tall.'
    parts = [
        P('Write down the length scale factor from the small one to the large one.', num(k), f'B1 {num(h2)} ÷ {h1} = {num(k)}', 1),
        P(f'The surface area of the small one is {S1} cm². Calculate the surface area of the large one.', f'{num(S1 * k * k)} cm²', f'M1 × ({num(k)})²; A1 {num(S1 * k * k)}', 2),
        P(f'The small one has mass {m1} g. Calculate the mass of the large one.', f'{num(m1 * k ** 3)} g', f'M1 mass ∝ volume, × ({num(k)})³; A1 {num(m1 * k ** 3)}', 2),
        P(f'Polishing costs {money(cost)} per cm². Calculate the cost of polishing the large one.', money(float(S1 * k * k) * cost), f'M1 {num(S1 * k * k)} × {cost}; A1 {money(float(S1 * k * k) * cost)}', 2),
        P('Explain why doubling the height of a statue does not simply double its mass.', 'Mass depends on volume, and volume is multiplied by 2³ = 8 when every length is doubled.', 'B1 volume factor 8', 1),
    ]
    return cmp_(r, intro, parts)


t113.add('C4', (2, 3, 4, 5))(t113_c4)


# ---------------------------------------------------------------- congruent triangles
t114 = topic('Congruent triangles: conditions SSS, SAS, ASA, RHS', 'congruent triangles: conditions sss, sas, asa, rhs', 'congruent triangles', 'congruence conditions')
t114.fixed('C1', (1, 2), [
    ('Which of these is NOT a condition that proves two triangles congruent?', 'AAA', 'Equal angles give similar triangles, which may differ in size.', ['SSS', 'SAS', 'RHS']),
    ('Two triangles have all three pairs of corresponding sides equal. They are congruent by', 'SSS', 'Three sides fix the triangle.', ['SAS', 'ASA', 'RHS']),
    ('Two right-angled triangles have equal hypotenuses and one other pair of equal sides. They are congruent by', 'RHS', 'Right angle, hypotenuse, side.', ['SSS', 'SAS', 'ASA']),
    ('In the condition SAS, the angle must be', 'the angle between the two given sides', 'The included angle.', ['any angle of the triangle', 'a right angle', 'the angle opposite the longest side']),
    ('Congruent triangles are', 'identical in shape and size', 'All corresponding sides and angles are equal.', ['the same shape but a different size', 'equal in area only', 'always right-angled']),
    ('Triangle ABC is congruent to triangle PQR, with A, B and C corresponding to P, Q and R. Which side is equal to QR?', 'BC', 'Corresponding vertices give corresponding sides.', ['AB', 'AC', 'PR']),
    ('Two triangles have two pairs of equal angles and the sides between those angles equal. They are congruent by', 'ASA', 'Two angles and the included side.', ['SAS', 'SSS', 'RHS']),
])
t114.fixed('C2', (2, 3), [
    ('Explain why three pairs of equal angles are not enough to show that two triangles are congruent.', 'The triangles could be enlargements of each other: same angles but different side lengths, so they are similar but not necessarily congruent.', 'B1 same shape could be different size; B1 similar not congruent [2]'),
    ('Explain why a diagonal of a rectangle divides it into two congruent triangles.', 'Opposite sides of a rectangle are equal, the diagonal is common to both triangles, so the triangles are congruent by SSS (or SAS with the right angles).', 'B1 two pairs of equal sides plus common side; B1 SSS or SAS [2]'),
    ('Explain why two sides and a non-included angle do not always give congruent triangles.', 'With the angle not between the sides, the third side can sometimes swing to two different positions, giving two different triangles with the same given information.', 'B1 angle not included; B1 two possible triangles [2]'),
])

CONG = {
    'SSS': lambda r, s, a: f'AB = PQ = {s[0]} cm, BC = QR = {s[1]} cm and CA = RP = {s[2]} cm',
    'SAS': lambda r, s, a: f'AB = PQ = {s[0]} cm, BC = QR = {s[1]} cm and angle ABC = angle PQR = {a[0]}°',
    'ASA': lambda r, s, a: f'angle ABC = angle PQR = {a[0]}°, angle BCA = angle QRP = {a[1]}° and BC = QR = {s[1]} cm',
    'RHS': lambda r, s, a: f'angle ABC = angle PQR = 90°, hypotenuse AC = PR = {s[2] + 3} cm and AB = PQ = {s[0]} cm',
}


@t114.add('C1', (1, 2, 3))
def t114_which(r, D):
    s = sorted(r.sample(range(4, 15), 3))
    if s[0] + s[1] <= s[2]:
        return None
    a = (r.randint(35, 80), r.randint(30, 70))
    cond = r.choice(list(CONG))
    return SMC(r, f'In triangles ABC and PQR, {CONG[cond](r, s, a)}. Which condition shows that the triangles are congruent?', cond, [c for c in CONG if c != cond],
               {'SSS': 'Three pairs of equal sides.', 'SAS': 'Two sides and the included angle (angle B is between AB and BC).', 'ASA': 'Two angles and the included side (BC lies between angles B and C).', 'RHS': 'Right angle, hypotenuse and one other side.'}[cond])


@t114.add('C2', (2, 3, 4), 'explain')
def t114_decide(r, D):
    s = sorted(r.sample(range(4, 15), 3))
    if s[0] + s[1] <= s[2]:
        return None
    a1, a2 = r.randint(35, 75), r.randint(30, 70)
    case = r.choice(['AAA', 'SSA', 'SAS', 'AAS'])
    if case == 'AAA':
        info, ans, key = f'angle A = angle P = {a1}°, angle B = angle Q = {a2}° and angle C = angle R = {180 - a1 - a2}°', 'Not necessarily: equal angles only show the triangles are similar; no side is known to be equal, so they could be different sizes.', 'B1 not necessarily congruent; B1 no equal side, similar only [2]'
    elif case == 'SSA':
        info, ans, key = f'AB = PQ = {s[2]} cm, BC = QR = {s[0]} cm and angle BAC = angle QPR = {a1 - 10}°', 'Not necessarily: the equal angle is not between the two equal sides (SSA), so two different triangles may fit the information.', 'B1 not necessarily congruent; B1 angle not included [2]'
    elif case == 'SAS':
        info, ans, key = f'AB = PQ = {s[0]} cm, AC = PR = {s[1]} cm and angle BAC = angle QPR = {a1}°', 'Yes, congruent by SAS: the equal angle A is between the two pairs of equal sides.', 'B1 congruent; B1 SAS with included angle identified [2]'
    else:
        info, ans, key = f'angle A = angle P = {a1}°, angle B = angle Q = {a2}° and BC = QR = {s[1]} cm', f'Yes: the third angles are both {180 - a1 - a2}°, so angles B and C and the included side BC match, giving ASA.', 'B1 finds third angle; B1 ASA [2]'
    return Q(f'For triangles ABC and PQR, {info}. Decide whether the triangles must be congruent. Give a reason for your answer.', ans, key)


@t114.add('C3', (1, 2, 3, 4, 5))
def t114_use(r, D):
    L1, L2 = r.choice([('ABC', 'XYZ'), ('DEF', 'KLM'), ('PQR', 'STU'), ('JKL', 'UVW')])
    perm = r.sample(range(3), 3)
    corr = {L1[i]: L2[perm[i]] for i in range(3)}
    tri2 = ''.join(corr[c] for c in L1)
    s = sorted(r.sample(range(4, 16), 3))
    if s[0] + s[1] <= s[2]:
        return None
    A, B = r.randint(35, 80), r.randint(30, 70)
    C = 180 - A - B
    x, y, z = L1
    X, Y, Z = (corr[c] for c in L1)
    if D <= 2:
        return Q(f'Triangle {L1} is congruent to triangle {tri2} (vertices in corresponding order). {x}{y} = {s[0]} cm, {y}{z} = {s[1]} cm and angle {x}{y}{z} = {B}°. Write down the length of {Y}{Z} and the size of angle {X}{Y}{Z}.', f'{Y}{Z} = {s[1]} cm, angle {X}{Y}{Z} = {B}°',
                 f'B1 {s[1]} cm; B1 {B}° [2]')
    if D == 3:
        return Q(f'Triangle {L1} is congruent to triangle {tri2} (vertices in corresponding order). Angle {y}{x}{z} = {A}° and angle {x}{y}{z} = {B}°. Find angle {Y}{Z}{X}, giving a reason.', f'{C}°',
                 f'M1 angle {x}{z}{y} = 180 − {A} − {B} = {C}; A1 {C}°, corresponding angle in congruent triangle [2]')
    per = s[0] + s[1] + s[2]
    return Q(f'Triangle {L1} is congruent to triangle {tri2} (vertices in corresponding order). {x}{y} = {s[0]} cm, {y}{z} = {s[1]} cm and the perimeter of triangle {tri2} is {per} cm. Angle {x}{y}{z} = {B}° and angle {y}{z}{x} = {C}°. Find (a) {Z}{X} (b) angle {Z}{X}{Y}.',
             f'(a) {s[2]} cm (b) {A}°', f'M1 {Z}{X} = {z}{x} = {per} − {s[0]} − {s[1]}; A1 {s[2]} cm; M1 angle {z}{x}{y} = 180 − {B} − {C}; A1 {A}° [4]', type='multi_step')


def t114_c4(r, D):
    case = r.choice(['para', 'iso', 'kite', 'bisect'])
    if case == 'para':
        a1, a2 = r.randint(25, 60), r.randint(30, 70)
        ab = r.randint(5, 14)
        intro = f'ABCD is a parallelogram with diagonal BD. Angle ABD = {a1}° and angle ADB = {a2}°, and AB = {ab} cm.'
        parts = [
            P('Prove that triangle ABD is congruent to triangle CDB.', 'Angle ABD = angle CDB and angle ADB = angle CBD (alternate angles, AB ∥ DC and AD ∥ BC); BD is common, so the triangles are congruent (ASA).', 'B1 one pair of alternate angles; B1 second pair; B1 common side BD and ASA', 3),
            P('Write down the length of CD.', f'{ab} cm', f'B1 {ab} cm (corresponds to AB)', 1),
            P('Find angle BCD.', f'{180 - a1 - a2}°', f'M1 angle BAD = 180 − {a1} − {a2}; A1 angle BCD = {180 - a1 - a2}° (corresponds to angle DAB)', 2),
        ]
    elif case == 'iso':
        s, b = r.randint(8, 16), 2 * r.randint(3, 7)
        if s <= b // 2 + 1:
            return None
        h = math.sqrt(s * s - (b // 2) ** 2)
        intro = f'Triangle ABC is isosceles with AB = AC = {s} cm and BC = {b} cm. M is the midpoint of BC.'
        parts = [
            P('Prove that triangles ABM and ACM are congruent.', 'AB = AC (given), BM = CM (M is the midpoint), AM is common, so the triangles are congruent (SSS).', 'B1 AB = AC and BM = CM; B1 AM common; B1 SSS', 3),
            P('Use the congruence to explain why AM is perpendicular to BC.', 'Angles AMB and AMC are corresponding angles of congruent triangles, so they are equal; they lie on a straight line so each is 90°.', 'B1 equal angles; B1 sum 180° so 90°', 2),
            P('Calculate the length of AM, correct to 3 significant figures.', f'{n3(h)} cm', f'M1 √({s}² − {b // 2}²); A1 {n3(h)}', 2),
        ]
    elif case == 'kite':
        a, c = r.randint(40, 80), r.randint(60, 120)
        b = (360 - a - c) / 2
        if b != int(b):
            c += 1
            b = (360 - a - c) / 2
        intro = f'ABCD is a kite with AB = AD and CB = CD. Angle BAD = {a}° and angle BCD = {c}°.'
        parts = [
            P('Prove that triangles ABC and ADC are congruent.', 'AB = AD and CB = CD (given), and AC is common, so the triangles are congruent (SSS).', 'B1 two pairs of equal sides; B1 AC common; B1 SSS', 3),
            P('Find angle ABC, giving a reason.', f'{num(b)}°', f'M1 angle ABC = angle ADC (congruent triangles); M1 (360 − {a} − {c}) ÷ 2; A1 {num(b)}°', 3),
            P('Find angle BAC.', f'{num(Fr(a, 2))}°', f'B1 AC bisects angle BAD: {num(Fr(a, 2))}°', 1),
        ]
    else:
        am, cm_ = r.randint(4, 12), r.randint(4, 12)
        ang = r.randint(40, 130)
        intro = f'The line segments AB and CD cross at M, and M is the midpoint of both AB and CD. AM = {am} cm, CM = {cm_} cm and angle AMC = {ang}°.'
        parts = [
            P('Prove that triangles AMC and BMD are congruent.', 'AM = BM and CM = DM (M is the midpoint of both), and angle AMC = angle BMD (vertically opposite), so the triangles are congruent (SAS).', 'B1 AM = BM and CM = DM; B1 vertically opposite angles; B1 SAS', 3),
            P('Explain why AC is parallel to DB.', 'Angle MAC = angle MBD (corresponding angles of congruent triangles); these are alternate angles, so AC ∥ DB.', 'B1 equal angles from congruence; B1 alternate angles equal so parallel', 2),
            P('Write down the size of angle BMD and the length of AB.', f'{ang}°, {2 * am} cm', f'B1 {ang}°; B1 AB = 2 × {am} = {2 * am} cm', 2),
        ]
    return cmp_(r, intro, parts)


t114.add('C4', (2, 3, 4, 5))(t114_c4)
CHAPTERS[11] = [t111, t112, t113, t114]


# =========================================================== 12 Averages and measures of spread
RAW_CTX = [('number of goals scored in each of {n} football matches', '', 0, 9),
           ('masses, in grams, of {n} apples', 'g', 95, 160),
           ('marks scored by {n} students in a test out of 50', 'marks', 12, 50),
           ('number of emails {nm} received on each of {n} days', '', 3, 30),
           ('ages, in years, of {n} people in a choir', 'years', 14, 70),
           ('heights, in centimetres, of {n} tomato plants', 'cm', 20, 75),
           ('times, in minutes, that {n} students took to travel to school', 'minutes', 4, 45),
           ('number of passengers on {n} buses in {c}', '', 8, 52)]


def raw_ctx(r, n, nm=None, c=None):
    what, unit, lo, hi = r.choice(RAW_CTX)
    return what.format(n=n, nm=nm or person(r), c=c or city(r)), unit, lo, hi


def rawlist(r, n, lo, hi, mode=True):
    """n integers in [lo, hi]; if mode, exactly one value repeated (unique mode)."""
    if hi - lo + 1 < n:
        return None
    vals = r.sample(range(lo, hi + 1), n - 1 if mode else n)
    if mode:
        vals.append(r.choice(vals))
    r.shuffle(vals)
    return vals


def u_(x, unit):
    return f'{x} {unit}' if unit and unit not in ('marks',) else (f'{x} marks' if unit == 'marks' else str(x))


t121 = topic('Mean, median, mode and range from raw data', 'mean, median, mode and range from raw data', 'mean median mode', 'range')
t121.fixed('C1', (1, 2), [
    ('Which average is the value that occurs most often?', 'The mode', 'Mode = most frequent value.', ['The mean', 'The median', 'The range']),
    ('What is the range of 3, 9, 4, 12, 7?', '9', '12 − 3 = 9.', ['12', '7', '5']),
    ('What is the median of 2, 8, 5, 4, 9, 1?', '4.5', 'Ordered: 1, 2, 4, 5, 8, 9; median = (4 + 5) ÷ 2.', ['5', '4', '6.5']),
    ('Which average is most affected by one extreme value?', 'The mean', 'Every value contributes to the total.', ['The median', 'The mode', 'They are all affected equally']),
    ('Five numbers have a mean of 6. What is their total?', '30', 'Total = mean × number of values.', ['6', '11', '1.2']),
    ('The range of a set of data measures', 'how spread out the data are', 'Range = largest − smallest.', ['the typical value', 'the most common value', 'the middle value']),
])
t121.fixed('C2', (2, 3), [
    ('Explain why the median is often a better average than the mean for house prices in a city.', 'A few very expensive houses (extreme values) raise the mean a lot, while the median, the middle value, is not affected by them, so it better represents a typical price.', 'B1 extreme values/outliers affect the mean; B1 median unaffected so more typical [2]'),
    ('Explain why the mode is the most useful average for a shop deciding which shoe sizes to stock.', 'The shop needs to know which size sells most often; the mean or median could be a size that is not the most popular, or not even an actual shoe size.', 'B1 most common size; B1 mean may not be an actual size [2]'),
    ('Explain why the mean of a data set can be a value that does not appear in the data.', 'The mean is the total shared equally between the values, so it can be a value in between, or a decimal, even if no item has that value.', 'B1 total ÷ number; B1 need not be a data value [2]'),
])


@t121.add('C1', (1, 2, 3))
def t121_pick(r, D):
    n = r.randint(7, 10)
    vals = rawlist(r, n, 1, 30 if D >= 2 else 15)
    if not vals:
        return None
    s = sorted(vals)
    what = r.choice(['mode', 'median', 'range'])
    m = median(vals)
    mo = modes(vals)[0][0]
    rg = s[-1] - s[0]
    ans = {'mode': mo, 'median': m, 'range': rg}[what]
    ds = [x for x in [mo, m, rg, vals[n // 2], max(vals), sum(vals) / n] if x != ans]
    key = {'mode': f'{mo} occurs most often.', 'median': f'Ordered: {lst(s)}; median = {num(m)}.', 'range': f'{s[-1]} − {s[0]} = {rg}.'}[what]
    return MC(r, f'Find the {what} of these numbers: {lst(vals)}.', ans, ds[:4], key, fmtf=lambda x: ex(round(float(x), 2)))


@t121.add('C3', (1, 2, 3, 4, 5))
def t121_calc(r, D):
    nm = person(r)
    if D == 1:
        n = r.randint(5, 8)
        what, unit, lo, hi = raw_ctx(r, n, nm)
        vals = rawlist(r, n, lo, hi, mode=False)
        if not vals or sum(vals) % n:
            return None
        return Q(f'The {what} are: {lst(vals)}. Calculate the mean.', u_(sum(vals) // n, unit), f'M1 {sum(vals)} ÷ {n}; A1 {sum(vals) // n} [2]')
    if D == 2:
        n = r.randint(8, 12)
        what, unit, lo, hi = raw_ctx(r, n, nm)
        vals = rawlist(r, n, lo, hi)
        if not vals:
            return None
        s = sorted(vals)
        mn = sum(vals) / n
        return Q(f'The {what} are: {lst(vals)}. Find (a) the mode (b) the median (c) the range (d) the mean.', f'(a) {modes(vals)[0][0]} (b) {num(median(vals))} (c) {s[-1] - s[0]} (d) {nn(mn)}',
                 f'(a) B1 {modes(vals)[0][0]} (b) M1 orders the data; A1 {num(median(vals))} (c) B1 {s[-1] - s[0]} (d) M1 {sum(vals)} ÷ {n}; A1 {nn(mn)} [6]', type='multi_step')
    if D == 3:
        n = r.randint(5, 8)
        m = r.randint(8, 30)
        others = [r.randint(m - 6, m + 8) for _ in range(n - 1)]
        x = m * n - sum(others)
        if x < 1 or x in others:
            return None
        return Q(f'The mean of the {n} numbers {lst(others)} and x is {m}. Find the value of x.', str(x), f'M1 total = {m} × {n} = {m * n}; M1 {m * n} − {sum(others)}; A1 x = {x} [3]')
    if D == 4:
        n = r.randint(8, 20)
        u = r.randint(40, 80)
        v = u + r.choice([1, 2, -1, -2])
        w = v * (n + 1) - u * n
        what = r.choice([('mass', 'kg', 'members of a rowing team'), ('mark', 'marks', 'students in a class'), ('score', 'points', 'players in a golf club')])
        if w <= 0:
            return None
        return Q(f'The mean {what[0]} of {n} {what[2]} is {u} {what[1]}. Another person joins the group and the mean {what[0]} of all {n + 1} becomes {v} {what[1]}. Find the {what[0]} of the person who joined.', f'{w} {what[1]}',
                 f'M1 original total {u} × {n} = {u * n}; M1 new total {v} × {n + 1} = {v * (n + 1)}; A1 {w} [3]')
    n1, n2 = r.randint(10, 18), r.randint(10, 18)
    u1, u2 = r.randint(30, 70) + r.choice([0, 0.5]), r.randint(30, 70) + r.choice([0, 0.5])
    g = r.choice([('boys', 'girls', 'Mathematics test', 'marks'), ('workers at site A', 'workers at site B', 'productivity check', 'units'), ('adults', 'children', 'reaction-time game', 'points')])
    tot = n1 * u1 + n2 * u2
    return Q(f'In a {g[2]}, {n1} {g[0]} had a mean score of {ex(u1)} {g[3]} and {n2} {g[1]} had a mean score of {ex(u2)} {g[3]}. Calculate the mean score of all {n1 + n2} people, correct to 3 significant figures.', f'{nn(tot / (n1 + n2))} {g[3]}',
             f'M1 {n1} × {ex(u1)} = {ex(n1 * u1)}; M1 {n2} × {ex(u2)} = {ex(n2 * u2)}; M1 total ÷ {n1 + n2}; A1 {nn(tot / (n1 + n2))} [4]', type='multi_step')


@t121.add('C3', (1, 2, 3, 4))
def t121_temp(r, D):
    c = city(r)
    n = 7
    base = r.randint(-8, 4)
    vals = [base + r.randint(-6, 6) for _ in range(n)]
    if len(set(vals)) < 4 or min(vals) >= 0:
        return None
    s = sorted(vals)
    mn = sum(vals) / n
    days = 'Monday to Sunday'
    if D <= 2:
        return Q(f'The midday temperatures, in °C, in {c} from {days} were: {lst(vals)}. Find the range and the median temperature.', f'Range {s[-1] - s[0]} °C; median {num(median(vals))} °C',
                 f'M1 {num(s[-1])} − ({num(s[0])}); A1 range {s[-1] - s[0]}; B1 median {num(median(vals))} [3]')
    return Q(f'The midday temperatures, in °C, in {c} from {days} were: {lst(vals)}. Calculate the mean temperature, correct to 1 decimal place, and find the range.', f'Mean {rnd_dp(round(mn, 6), 1).replace("-", MINUS)} °C; range {s[-1] - s[0]} °C',
             f'M1 total {num(sum(vals))} ÷ 7; A1 {rnd_dp(round(mn, 6), 1).replace("-", MINUS)}; B1 range {s[-1] - s[0]} [3]')


@t121.add('C2', (2, 3, 4), 'explain')
def t121_err(r, D):
    nm = person(r)
    case = r.choice(['order', 'modefreq', 'best'])
    if case == 'order':
        n = r.choice([7, 9])
        vals = rawlist(r, n, 2, 40, mode=False)
        if not vals or vals[n // 2] == median(vals):
            return None
        return Q(f'{nm} is asked for the median of {lst(vals)} and answers {vals[n // 2]}, the middle number in the list. Explain the mistake and find the correct median.', f'The data must be put in order first: {lst(sorted(vals))}, so the median is {median(vals)}.',
                 f'B1 must order the data; B1 median {median(vals)} [2]')
    if case == 'modefreq':
        vals = rawlist(r, 9, 1, 12)
        if not vals:
            return None
        mo = modes(vals)[0][0]
        f = vals.count(mo)
        if f == mo:
            return None
        return Q(f'{nm} says the mode of {lst(vals)} is {f} because the most common value appears {f} times. Explain the mistake.', f'The mode is the value that occurs most often, {mo}, not the number of times it occurs ({f}).', f'B1 mode is the value not the frequency; B1 mode = {mo} [2]')
    what, unit, lo, hi = r.choice([('annual salaries, in thousands of dollars, of 7 employees at a small firm', 'thousand dollars', 22, 40), ('prices of 7 houses on a street', 'dollars', 0, 0)])
    if unit == 'dollars':
        vals = [r.randint(18, 30) * 10000 for _ in range(6)] + [r.randint(9, 15) * 100000]
        f = lambda x: '$' + f'{int(x):,}'.replace(',', ' ')
    else:
        vals = [r.randint(lo, hi) for _ in range(6)] + [r.randint(150, 300)]
        f = num
    r.shuffle(vals)
    mn, md = sum(vals) / 7, median(vals)
    return Q(f'The {what} are: {lst(vals, f)}. {nm} wants to describe a typical value. Explain whether the mean or the median is more suitable.', f'The median ({f(md)}) is better: one extreme value raises the mean to {f(round(mn))}, which is larger than all but one of the values.',
             'B1 median; B1 reason referring to the extreme value / mean distorted [2]')


def t121_c4(r, D):
    nm = person(r)
    n = r.choice([9, 10, 11, 12])
    what, unit, lo, hi = raw_ctx(r, n, nm)
    vals = rawlist(r, n, lo, hi)
    if not vals:
        return None
    s = sorted(vals)
    mo = modes(vals)[0][0]
    mn = sum(vals) / n
    target = math.ceil(mn) + r.randint(1, 3)
    need = target * (n + 1) - sum(vals)
    intro = f'The {what} are: {lst(vals)}.'
    parts = [
        P('Find the mode.', str(mo), f'B1 {mo}', 1),
        P('Find the median.', num(median(vals)), f'M1 orders: {lst(s)}; A1 {num(median(vals))}', 2),
        P('Calculate the mean.', nn(mn), f'M1 {sum(vals)} ÷ {n}; A1 {nn(mn)}', 2),
        P('Find the range.', str(s[-1] - s[0]), f'B1 {s[-1]} − {s[0]} = {s[-1] - s[0]}', 1),
        P(f'One more value is added and the mean of all {n + 1} values becomes {target}. Find the value that was added.', str(need), f'M1 {target} × {n + 1} = {target * (n + 1)}; M1 − {sum(vals)}; A1 {need}', 3),
    ]
    return cmp_(r, intro, parts)


t121.add('C4', (2, 3, 4, 5))(t121_c4)


# ---------------------------------------------------------------- frequency tables and grouped data
FT_CTX = [('Number of goals', 'football matches', [0, 1, 2, 3, 4, 5]), ('Number of brothers and sisters', 'students', [0, 1, 2, 3, 4]),
          ('Number of people in a car', 'cars', [1, 2, 3, 4, 5]), ('Shoe size', 'customers', [36, 37, 38, 39, 40, 41]),
          ('Number of pets', 'families', [0, 1, 2, 3, 4]), ('Score on a dice', 'throws', [1, 2, 3, 4, 5, 6]),
          ('Number of books read in a month', 'club members', [0, 1, 2, 3, 4, 5])]
GR_CTX = [('Time (t minutes)', 't', 'times spent on homework by students', 'minutes'), ('Mass (m kg)', 'm', 'masses of parcels at a post office', 'kg'),
          ('Height (h cm)', 'h', 'heights of sunflower plants', 'cm'), ('Distance (d km)', 'd', 'distances travelled to work by employees', 'km'),
          ('Speed (s km/h)', 's', 'speeds of cars passing a speed camera', 'km/h')]


def ftable(r):
    lab, who, xs = r.choice(FT_CTX)
    for _ in range(20):
        fs = [r.randint(1, 15) for _ in xs]
        if fs.count(max(fs)) == 1:
            return lab, who, xs, fs
    return None


def ft_text(lab, xs, fs):
    return f'{lab}: {lst(xs)}; Frequency: {lst(fs)}'


def ft_median(xs, fs):
    data = [x for x, f in zip(xs, fs) for _ in range(f)]
    return median(data), sum(fs)


def gtable(r, D):
    lab, v, what, unit = r.choice(GR_CTX)
    w = r.choice([5, 10, 20])
    start = r.choice([0, 0, 10, 20, 40]) if unit != 'km/h' else r.choice([30, 40])
    k = r.randint(4, 5 if D <= 4 else 6)
    edges = [start + i * w for i in range(k + 1)]
    fs = [r.randint(2, 18) for _ in range(k)]
    if fs.count(max(fs)) > 1:
        return None
    classes = [f'{a} < {v} ≤ {b}' for a, b in zip(edges, edges[1:])]
    mids = [Fr(a + b, 2) for a, b in zip(edges, edges[1:])]
    return lab, v, what, unit, edges, classes, mids, fs


def gt_text(lab, classes, fs):
    return f'{lab}: {", ".join(classes)}; Frequency: {lst(fs)}'


def median_class(classes, fs):
    n = sum(fs)
    pos = (n + 1) / 2
    c = 0
    for cl, f in zip(classes, fs):
        c += f
        if c >= pos:
            return cl
    return classes[-1]


t122 = topic('Averages from frequency tables and estimated mean of grouped data', 'averages from frequency tables and estimated mean of grouped data', 'frequency table', 'estimated mean', 'modal class')
t122.fixed('C1', (1, 2), [
    ('In a grouped frequency table, which value is used to represent each class when estimating the mean?', 'The midpoint of the class', 'The exact values are unknown, so the midpoint is used.', ['The upper boundary', 'The lower boundary', 'The frequency']),
    ('The modal class of a grouped frequency table is', 'the class with the highest frequency', 'Modal = most frequent.', ['the middle class', 'the class with the largest values', 'the class containing the mean']),
    ('In a frequency table, Σfx means', 'the sum of each value multiplied by its frequency', 'This gives the total of all the data values.', ['the sum of the frequencies', 'the number of rows in the table', 'the largest value times the largest frequency']),
    ('What is the midpoint of the class 20 < t ≤ 30?', '25', '(20 + 30) ÷ 2.', ['20', '30', '10']),
    ('A frequency table has total frequency 40. The median is', 'halfway between the 20th and 21st values', '(40 + 1) ÷ 2 = 20.5th value.', ['the 20th value', 'the 40th value', 'the value with frequency 20']),
])
t122.fixed('C2', (2, 3), [
    ('Explain why the mean calculated from a grouped frequency table is only an estimate.', 'The actual data values are not known; each value is assumed to be at the midpoint of its class.', 'B1 original values unknown; B1 midpoints used [2]'),
    ('Explain why you cannot find the exact range from a grouped frequency table.', 'Only the class limits are known, not the actual smallest and largest values.', 'B1 actual values unknown; B1 only class boundaries [2]'),
])


@t122.add('C1', (1, 2, 3))
def t122_mode(r, D):
    p = ftable(r)
    if not p:
        return None
    lab, who, xs, fs = p
    i = fs.index(max(fs))
    md, n = ft_median(xs, fs)
    ds = [max(fs), xs[len(xs) // 2] if xs[len(xs) // 2] != xs[i] else xs[0], md, xs[-1] if xs[-1] != xs[i] else xs[0]]
    return MC(r, f'The table shows data about {n} {who}. {ft_text(lab, xs, fs)}. What is the mode?', xs[i], ds, f'{xs[i]} has the highest frequency ({max(fs)}).', fmtf=lambda x: ex(float(x)))


@t122.add('C3', (1, 2, 3, 4, 5))
def t122_calc(r, D):
    if D <= 3:
        p = ftable(r)
        if not p:
            return None
        lab, who, xs, fs = p
        n = sum(fs)
        sfx = sum(x * f for x, f in zip(xs, fs))
        txt = ft_text(lab, xs, fs)
        if D == 1:
            used = [x for x, f in zip(xs, fs) if f]
            return Q(f'The table shows information about {n} {who}. {txt}. Write down the mode and calculate the mean.', f'Mode {xs[fs.index(max(fs))]}; mean {nn(sfx / n)}',
                     f'B1 mode {xs[fs.index(max(fs))]}; M1 Σfx = {sfx}; M1 ÷ {n}; A1 {nn(sfx / n)} [4]')
        if D == 2:
            return Q(f'The table shows information about {n} {who}. {txt}. Calculate the mean, giving your answer correct to 3 significant figures where necessary.', nn(sfx / n),
                     f'M1 Σfx = {" + ".join(f"{x} × {f}" for x, f in zip(xs, fs))} = {sfx}; M1 {sfx} ÷ {n}; A1 {nn(sfx / n)} [3]')
        md, _ = ft_median(xs, fs)
        return Q(f'The table shows information about {n} {who}. {txt}. Find the median and calculate the mean.', f'Median {num(md)}; mean {nn(sfx / n)}',
                 f'M1 median at position ({n} + 1) ÷ 2 = {ex((n + 1) / 2)}; A1 median {num(md)}; M1 {sfx} ÷ {n}; A1 {nn(sfx / n)} [4]', type='multi_step')
    p = gtable(r, D)
    if not p:
        return None
    lab, v, what, unit, edges, classes, mids, fs = p
    n = sum(fs)
    sfx = sum(m * f for m, f in zip(mids, fs))
    est = float(sfx) / n
    txt = gt_text(lab, classes, fs)
    if D == 4:
        return Q(f'The table shows the {what}. {txt}. Calculate an estimate of the mean.', f'{nn(est)} {unit}',
                 f'M1 midpoints {lst(mids, lambda m: ex(float(m)))}; M1 Σfx = {ex(float(sfx))}; M1 ÷ {n}; A1 {nn(est)} [4]', type='multi_step')
    return Q(f'The table shows the {what}. {txt}. (a) Write down the modal class. (b) Find the class that contains the median. (c) Calculate an estimate of the mean.',
             f'(a) {classes[fs.index(max(fs))]} (b) {median_class(classes, fs)} (c) {nn(est)} {unit}',
             f'(a) B1 {classes[fs.index(max(fs))]} (b) B1 {median_class(classes, fs)} ({ex((n + 1) / 2)}th value) (c) M1 midpoints; M1 Σfx = {ex(float(sfx))}; A1 {nn(est)} [5]', type='multi_step')


@t122.add('C2', (2, 3, 4), 'explain')
def t122_err(r, D):
    nm = person(r)
    p = ftable(r)
    if not p:
        return None
    lab, who, xs, fs = p
    n = sum(fs)
    sfx = sum(x * f for x, f in zip(xs, fs))
    k = len(xs)
    case = r.choice(['rows', 'sumf', 'midpt'])
    if case == 'rows':
        return Q(f'The table shows information about {n} {who}. {ft_text(lab, xs, fs)}. {nm} calculates the mean as {sfx} ÷ {k} = {nn(sfx / k)}. Explain the mistake and find the correct mean.',
                 f'{nm} divided by the number of columns ({k}) instead of the total frequency ({n}). Mean = {sfx} ÷ {n} = {nn(sfx / n)}.', f'B1 divide by total frequency {n}; B1 {nn(sfx / n)} [2]')
    if case == 'sumf':
        return Q(f'The table shows information about {n} {who}. {ft_text(lab, xs, fs)}. {nm} says the mean is {sum(xs)} ÷ {k} = {nn(sum(xs) / k)}. Explain the mistake and find the correct mean.',
                 f'{nm} found the mean of the values listed, ignoring how often each occurs. Mean = Σfx ÷ Σf = {sfx} ÷ {n} = {nn(sfx / n)}.', f'B1 frequencies must be used; B1 {nn(sfx / n)} [2]')
    g = gtable(r, 4)
    if not g:
        return None
    lab, v, what, unit, edges, classes, mids, fs = g
    n = sum(fs)
    wrong = sum(b * f for b, f in zip(edges[1:], fs)) / n
    right = float(sum(m * f for m, f in zip(mids, fs))) / n
    return Q(f'The table shows the {what}. {gt_text(lab, classes, fs)}. {nm} estimates the mean using the upper end of each class and gets {nn(wrong)} {unit}. Explain why this is not a good estimate and find a better one.',
             f'Using upper ends assumes every value is as large as possible, so it overestimates. Using midpoints gives {nn(right)} {unit}.', f'B1 should use midpoints / overestimates; B1 {nn(right)} [2]')


def t122_c4(r, D):
    g = gtable(r, 5)
    if not g:
        return None
    lab, v, what, unit, edges, classes, mids, fs = g
    n = sum(fs)
    sfx = sum(m * f for m, f in zip(mids, fs))
    est = float(sfx) / n
    above = fs[-1] + fs[-2]
    intro = f'The table shows the {what} in {city(r)}. {gt_text(lab, classes, fs)}.'
    parts = [
        P('Write down the modal class.', classes[fs.index(max(fs))], f'B1 {classes[fs.index(max(fs))]}', 1),
        P('Find the class that contains the median.', median_class(classes, fs), f'M1 position ({n} + 1) ÷ 2 = {ex((n + 1) / 2)}; A1 {median_class(classes, fs)}', 2),
        P('Calculate an estimate of the mean.', f'{nn(est)} {unit}', f'M1 midpoints {lst(mids, lambda m: ex(float(m)))}; M1 Σfx = {ex(float(sfx))}; A1 {nn(est)}', 3),
        P('Explain why a mean calculated from this table can only be an estimate.', 'The exact values are not known; each value is assumed to be at the midpoint of its class.', 'B1 midpoints / exact values unknown', 1),
        P(f'Calculate the percentage of the data greater than {edges[-3]} {unit}.', f'{nn(100 * above / n)}%', f'M1 {fs[-2]} + {fs[-1]} = {above}; M1 {above} ÷ {n} × 100; A1 {nn(100 * above / n)}%', 3),
    ]
    return cmp_(r, intro, parts)


t122.add('C4', (2, 3, 4, 5))(t122_c4)


# ---------------------------------------------------------------- quartiles and interquartile range
QN = [7, 11, 15, 19]


def qtext(lq, md, uq):
    return f'LQ = {num(lq)}, median = {num(md)}, UQ = {num(uq)}'


t123 = topic('Quartiles and interquartile range', 'quartiles and interquartile range', 'interquartile range', 'lower quartile', 'upper quartile')
t123.fixed('C1', (1, 2), [
    ('The interquartile range is', 'the upper quartile minus the lower quartile', 'IQR = UQ − LQ.', ['the largest value minus the smallest value', 'the median minus the lower quartile', 'the mean of the quartiles']),
    ('For a data set, LQ = 14 and UQ = 31. What is the interquartile range?', '17', '31 − 14.', ['45', '22.5', '31']),
    ('What fraction of the data lies between the lower and upper quartiles?', 'One half', 'Each quartile marks off a quarter of the data.', ['One quarter', 'Three quarters', 'All of it']),
    ('The ordered data are 3, 5, 6, 8, 10, 12, 15. What is the lower quartile?', '5', 'Median 8; lower half 3, 5, 6, so LQ = 5.', ['6', '3', '4']),
    ('Why is the interquartile range often a better measure of spread than the range?', 'It is not affected by extreme values', 'It uses the middle 50% of the data.', ['It is always larger', 'It uses every data value', 'It is easier to calculate']),
    ('The ordered data are 2, 4, 7, 9, 11, 14, 18. What is the upper quartile?', '14', 'Upper half 11, 14, 18; middle value 14.', ['11', '18', '12.5']),
])
t123.fixed('C2', (2, 3), [
    ('Explain why the interquartile range is less affected by an outlier than the range.', 'The IQR uses only the middle half of the data, between the quartiles, so a single extreme value at either end does not change it much, whereas the range uses the extreme values directly.', 'B1 IQR uses middle 50%; B1 range uses largest and smallest [2]'),
    ('Explain what a small interquartile range tells you about a set of data.', 'The middle half of the data are close together, so the data are consistent / not very spread out.', 'B1 middle 50% close together; B1 consistent / little spread [2]'),
])


def qdata(r, n, lo=10, hi=60):
    if hi - lo + 1 < n:
        return None
    return r.sample(range(lo, hi + 1), n)


@t123.add('C1', (1, 2, 3))
def t123_pick(r, D):
    n = r.choice([7, 11]) if D <= 2 else r.choice(QN[:3])
    vals = sorted(qdata(r, n, 1, 45))
    lq, md, uq = quartiles(vals)
    what = r.choice(['lower quartile', 'upper quartile', 'interquartile range'])
    ans = {'lower quartile': lq, 'upper quartile': uq, 'interquartile range': uq - lq}[what]
    ds = [x for x in [lq, uq, md, uq - lq, vals[-1] - vals[0], vals[n // 4]] if x != ans]
    return MC(r, f'The ordered data are: {lst(vals)}. Find the {what}.', ans, ds[:4], f'{qtext(lq, md, uq)}; IQR = {num(uq - lq)}.')


@t123.add('C3', (1, 2, 3, 4, 5))
def t123_calc(r, D):
    if D == 1:
        vals = sorted(qdata(r, 7, 2, 40))
        lq, md, uq = quartiles(vals)
        return Q(f'The ordered data are: {lst(vals)}. Find (a) the median (b) the lower quartile (c) the upper quartile.', f'(a) {md} (b) {lq} (c) {uq}', f'(a) B1 {md} (b) B1 {lq} (c) B1 {uq} [3]')
    if D == 2:
        n = 11
        what, unit, lo, hi = raw_ctx(r, n)
        vals = qdata(r, n, lo, hi)
        if not vals:
            return None
        lq, md, uq = quartiles(vals)
        return Q(f'The {what} are: {lst(vals)}. Find the interquartile range.', u_(uq - lq, unit), f'M1 orders data; M1 LQ = {lq} and UQ = {uq}; A1 IQR = {uq - lq} [3]')
    if D == 3:
        n = r.choice([15, 19])
        vals = stem_data(r, D, n)
        lq, md, uq = quartiles(vals)
        what, unit = r.choice([('masses of parcels, in kg,', 'kg'), ('ages of people at a concert, in years,', 'years'), ('test marks', 'marks'), ('times taken to finish a puzzle, in seconds,', 'seconds')])
        st = vals[n // 2] // 10
        return Q(f'The stem-and-leaf diagram shows the {what} of {n} people. {stem_text(vals)} (Key: {st} | {vals[n // 2] % 10} represents {vals[n // 2]}). Find the median and the interquartile range.', f'Median {num(md)}; IQR {num(uq - lq)}',
                 f'B1 median = {(n + 1) // 2}th value = {num(md)}; M1 LQ = {num(lq)}, UQ = {num(uq)}; A1 IQR {num(uq - lq)} [3]')
    if D == 4:
        p = ftable(r)
        if not p:
            return None
        lab, who, xs, fs = p
        n = sum(fs)
        if n % 4 != 3:
            return None
        data = [x for x, f in zip(xs, fs) for _ in range(f)]
        lq, md, uq = quartiles(data)
        return Q(f'The table shows information about {n} {who}. {ft_text(lab, xs, fs)}. Find the lower quartile, the upper quartile and the interquartile range.', f'LQ {num(lq)}, UQ {num(uq)}, IQR {num(uq - lq)}',
                 f'M1 LQ is the {(n + 1) // 4}th value, UQ the {3 * (n + 1) // 4}th; A1 LQ {num(lq)}; A1 UQ {num(uq)}; A1 IQR {num(uq - lq)} [4]', type='multi_step')
    # unknown value from IQR (n = 7: LQ = 2nd, UQ = 6th)
    for _ in range(30):
        s = sorted(r.sample(range(5, 60), 7))
        k = s[5] - s[1]
        if s[4] < s[5] < s[6]:
            break
    else:
        return None
    shown = s[:5] + ['x'] + [s[6]]
    return Q(f'The seven numbers {", ".join(str(t) for t in shown)} are in order of size. The interquartile range is {k}. Find the value of x, and the range of the data.', f'x = {s[5]}; range {s[6] - s[0]}',
             f'M1 LQ = {s[1]} (2nd value), UQ = x (6th value); M1 x − {s[1]} = {k}; A1 x = {s[5]}; B1 range {s[6]} − {s[0]} = {s[6] - s[0]} [4]', type='multi_step')


@t123.add('C3', (2, 3, 4))
def t123_ctx(r, D):
    nm = person(r)
    n = r.choice([11, 15])
    what, unit = r.choice([('times, in seconds, taken by {n} swimmers to swim 50 m', 's'), ('daily rainfall, in mm, at a weather station in {c} on {n} days', 'mm'), ('number of push-ups done in one minute by {n} athletes', ''), ('lengths, in mm, of {n} leaves from a tree', 'mm')])
    what = what.format(n=n, c=city(r))
    lo = r.randint(5, 30)
    vals = qdata(r, n, lo, lo + 40)
    out = r.random() < 0.5 and D >= 3
    if out:
        vals[r.randrange(n)] = lo + r.randint(70, 120)
    lq, md, uq = quartiles(vals)
    s = sorted(vals)
    tail = ' Find the range and the interquartile range, and explain which is the better measure of spread for these data.' if out else ' Find the median and the interquartile range.'
    ans = (f'Range {s[-1] - s[0]}, IQR {num(uq - lq)}; IQR is better because the value {s[-1]} is an outlier that inflates the range.' if out else f'Median {num(md)}; IQR {num(uq - lq)}')
    key = (f'B1 range {s[-1] - s[0]}; M1 LQ {num(lq)}, UQ {num(uq)}; A1 IQR {num(uq - lq)}; B1 IQR not affected by the outlier {s[-1]} [4]' if out else f'B1 median {num(md)}; M1 LQ {num(lq)}, UQ {num(uq)}; A1 IQR {num(uq - lq)} [3]')
    return Q(f'The {what} are: {lst(vals)}.{tail}', ans, key, **({'type': 'multi_step'} if out else {}))


@t123.add('C2', (2, 3, 4), 'explain')
def t123_err(r, D):
    nm = person(r)
    n = r.choice([7, 11])
    vals = qdata(r, n, 3, 50)
    lq, md, uq = quartiles(vals)
    case = r.choice(['order', 'range'])
    if case == 'order':
        # unordered: take 2nd and 6th (n = 7) or 3rd and 9th (n = 11) values as listed
        i1, i2 = (n + 1) // 4 - 1, 3 * (n + 1) // 4 - 1
        a, b = vals[i1], vals[i2]
        if (a, b) == (lq, uq) or abs(b - a) == uq - lq:
            return None
        return Q(f'{nm} is finding the interquartile range of {lst(vals)}. {nm} takes the {ordinal(i1 + 1)} and {ordinal(i2 + 1)} numbers in the list, {a} and {b}, and writes IQR = {abs(b - a)}. Explain the mistake and find the correct IQR.',
                 f'The data must be put in order first: {lst(sorted(vals))}. LQ = {lq}, UQ = {uq}, so IQR = {uq - lq}.', f'B1 data not ordered; B1 IQR {uq - lq} [2]')
    s = sorted(vals)
    return Q(f'For the data {lst(sorted(vals))}, {nm} says the interquartile range is {s[-1]} − {s[0]} = {s[-1] - s[0]}. Explain the mistake and find the correct interquartile range.',
             f'{s[-1] - s[0]} is the range (largest − smallest). IQR = UQ − LQ = {uq} − {lq} = {uq - lq}.', f'B1 range not IQR; B1 {uq - lq} [2]')


def t123_c4(r, D):
    n = 15
    vals = stem_data(r, 5, n)
    lq, md, uq = quartiles(vals)
    what = r.choice(['ages, in years, of 15 visitors to a museum in {c}', 'marks of 15 students in a science test', 'masses, in kg, of 15 suitcases checked in at the airport in {c}', 'lengths, in cm, of 15 fish caught in a lake'])
    what = what.format(c=city(r))
    st = vals[7] // 10
    above = sum(1 for v in vals if v > uq)
    intro = f'The stem-and-leaf diagram shows the {what}. {stem_text(vals)} (Key: {st} | {vals[7] % 10} represents {vals[7]}).'
    parts = [
        P('Find the median.', num(md), f'B1 8th value {num(md)}', 1),
        P('Find the lower quartile and the upper quartile.', f'LQ {num(lq)}, UQ {num(uq)}', f'B1 LQ = 4th value {num(lq)}; B1 UQ = 12th value {num(uq)}', 2),
        P('Calculate the interquartile range.', num(uq - lq), f'B1 {num(uq)} − {num(lq)} = {num(uq - lq)}', 1),
        P('Find the range.', num(vals[-1] - vals[0]), f'B1 {vals[-1]} − {vals[0]} = {vals[-1] - vals[0]}', 1),
        P('Write down how many values are greater than the upper quartile.', str(above), f'B1 {above}', 1),
        P('Explain what the interquartile range tells you about these data.', f'The middle half of the values are spread over {num(uq - lq)} units (between {num(lq)} and {num(uq)}).', 'B1 middle 50% spread with values', 1),
    ]
    return cmp_(r, intro, parts)


t123.add('C4', (2, 3, 4, 5))(t123_c4)


# ---------------------------------------------------------------- comparing distributions
CMP_CTX = [('two classes', 'Class A', 'Class B', 'test marks', 'marks', 'higher'),
           ('two shops', 'Shop P', 'Shop Q', 'daily customer numbers', 'customers', 'higher'),
           ('two archers', '{a}', '{b}', 'archery scores', 'points', 'higher'),
           ('two farms', 'Farm X', 'Farm Y', 'egg masses', 'g', 'higher'),
           ('two bus routes', 'Route 1', 'Route 2', 'journey times', 'minutes', 'lower')]


def cmp_ctx(r):
    a, b = two_people(r)
    g, A, B, what, unit, better = r.choice(CMP_CTX)
    return g, A.format(a=a, b=b), B.format(a=a, b=b), what, unit, better


def cmp_sentences(A, B, ma, mb, sa, sb, avg='median', spread='interquartile range'):
    if ma == mb:
        s1 = f'The {avg}s are the same ({num(ma)}), so on average they are similar.'
    else:
        hi, lo = (A, B) if ma > mb else (B, A)
        s1 = f'{hi} has a higher {avg} ({num(max(ma, mb))} compared with {num(min(ma, mb))}), so on average {hi}\'s values are higher.'
    if sa == sb:
        s2 = f'The {spread}s are equal ({num(sa)}), so the spread is the same.'
    else:
        c, o = (A, B) if sa < sb else (B, A)
        s2 = f'{c} has a smaller {spread} ({num(min(sa, sb))} compared with {num(max(sa, sb))}), so {c}\'s values are more consistent.'
    return s1 + ' ' + s2


t124 = topic('Comparing distributions using averages and spread', 'comparing distributions using averages and spread', 'comparing distributions', 'average and spread')
t124.fixed('C1', (1, 2), [
    ('To compare two distributions fully, you should compare', 'an average and a measure of spread', 'One comparison of typical value and one of consistency.', ['two averages', 'the largest values only', 'the number of data values']),
    ('Group A has IQR 4 and group B has IQR 12. Which statement is correct?', 'Group A is more consistent', 'A smaller spread means more consistent values.', ['Group B is more consistent', 'Group A has a higher average', 'Group B has a higher average']),
    ('Which pair of measures is best for comparing data sets that contain outliers?', 'Median and interquartile range', 'Neither is affected much by extreme values.', ['Mean and range', 'Mode and range', 'Mean and median']),
    ('Two runners have the same median time, but runner P has a much larger range. This means', 'runner P is less consistent', 'A larger spread means less consistency.', ['runner P is faster on average', 'runner P is slower on average', 'runner P is more consistent']),
])
t124.fixed('C2', (2, 3), [
    ('Explain why comparing only the means of two data sets may not be enough.', 'Two sets can have the same mean but very different spreads, so you also need a measure of spread (range or IQR) to compare how consistent they are.', 'B1 same average can hide different spread; B1 need a measure of spread [2]'),
    ('Explain what it means in context if the journey times on one bus route have a smaller interquartile range than another.', 'The journey times on that route vary less, so they are more reliable/predictable.', 'B1 times vary less; B1 more reliable in context [2]'),
])


@t124.add('C1', (1, 2, 3))
def t124_mcq(r, D):
    g, A, B, what, unit, better = cmp_ctx(r)
    ma, mb = r.sample(range(20, 80), 2)
    sa, sb = r.sample(range(3, 25), 2)
    hiA, conA = ma > mb, sa < sb
    opts = [f'{A} has a {"higher" if h else "lower"} median and is {"more" if c else "less"} consistent than {B}' for h, c in [(hiA, conA), (not hiA, conA), (hiA, not conA), (not hiA, not conA)]]
    return SMC(r, f'For {g}, the {what} are summarised. {A}: median {ma} {unit}, IQR {sa} {unit}. {B}: median {mb} {unit}, IQR {sb} {unit}. Which statement is correct?', opts[0], opts[1:],
               f'Median {ma} vs {mb}; IQR {sa} vs {sb} (smaller IQR = more consistent).')


@t124.add('C2', (2, 3, 4), 'explain')
def t124_two(r, D):
    g, A, B, what, unit, better = cmp_ctx(r)
    avg, spread = r.choice([('median', 'interquartile range'), ('mean', 'range')])
    ma, mb = r.sample(range(20, 80), 2)
    sa, sb = r.sample(range(4, 30), 2)
    ans = cmp_sentences(A, B, ma, mb, sa, sb, avg, spread)
    if better == 'lower':
        ans += f' (For {what}, a lower {avg} is better.)'
    return Q(f'The {what} for {g} are summarised. {A}: {avg} {ma} {unit}, {spread} {sa} {unit}. {B}: {avg} {mb} {unit}, {spread} {sb} {unit}. Make two comparisons between the {what} for {A} and {B}.', ans,
             f'B1 compares {avg}s in context; B1 compares {spread}s (consistency) in context [2]')


@t124.add('C3', (1, 2, 3, 4, 5))
def t124_calc(r, D):
    g, A, B, what, unit, better = cmp_ctx(r)
    n = 7 if D <= 3 else 11
    lo = r.randint(20, 50)
    va = qdata(r, n, lo, lo + 30)
    vb = qdata(r, n, lo + r.randint(-8, 8), lo + r.randint(15, 45))
    if not va or not vb:
        return None
    if D <= 2:
        ra, rb = max(va) - min(va), max(vb) - min(vb)
        ma, mb = Fr(sum(va), n), Fr(sum(vb), n)
        if ma.denominator != 1 or mb.denominator != 1:
            return None
        return Q(f'The {what} for {g} are: {A}: {lst(va)}; {B}: {lst(vb)}. Calculate the mean and range for each, and make two comparisons.', f'{A}: mean {num(ma)}, range {ra}; {B}: mean {num(mb)}, range {rb}. ' + cmp_sentences(A, B, ma, mb, ra, rb, 'mean', 'range'),
                 f'B1 both means; B1 both ranges; B1 compares means; B1 compares ranges [4]', type='multi_step')
    la, mda, ua = quartiles(va)
    lb_, mdb, ub = quartiles(vb)
    return Q(f'The {what} for {g} are: {A}: {lst(va)}; {B}: {lst(vb)}. Find the median and interquartile range for each, and use them to compare the two distributions.',
             f'{A}: median {num(mda)}, IQR {num(ua - la)}; {B}: median {num(mdb)}, IQR {num(ub - lb_)}. ' + cmp_sentences(A, B, mda, mdb, ua - la, ub - lb_),
             f'B1 both medians; M1 quartiles for each; A1 both IQRs; B1 compares medians; B1 compares IQRs [5]', type='multi_step')


@t124.add('C2', (2, 3, 4), 'explain')
def t124_err(r, D):
    nm = person(r)
    g, A, B, what, unit, better = cmp_ctx(r)
    ma, mb = r.sample(range(30, 70), 2)
    ra, rb = r.sample(range(10, 40), 2)
    big = A if ra > rb else B
    return Q(f'The {what} for {g} are summarised. {A}: mean {ma} {unit}, range {ra} {unit}. {B}: mean {mb} {unit}, range {rb} {unit}. {nm} says "{big} did better because its range is bigger." Explain why {nm}\'s reasoning is wrong.',
             f'A bigger range only shows the values are more spread out (less consistent); it does not show higher values. To compare which is higher on average, compare the means ({ma} and {mb}).', 'B1 range measures spread/consistency, not size; B1 should compare averages [2]')


def t124_c4(r, D):
    g, A, B, what, unit, better = cmp_ctx(r)
    n = 11
    lo = r.randint(20, 50)
    va = qdata(r, n, lo, lo + 30)
    vb = qdata(r, n, lo + r.randint(-5, 10), lo + r.randint(20, 50))
    if not va or not vb:
        return None
    la, mda, ua = quartiles(va)
    lb_, mdb, ub = quartiles(vb)
    if mda == mdb or ua - la == ub - lb_:
        return None
    pick = (A if (mda > mdb) == (better == 'higher') else B)
    intro = f'The {what} for {g} are recorded. {A}: {lst(va)}. {B}: {lst(vb)}.'
    parts = [
        P(f'Find the median and interquartile range for {A}.', f'median {num(mda)}, IQR {num(ua - la)}', f'B1 median {num(mda)}; M1 LQ {num(la)}, UQ {num(ua)}; A1 IQR {num(ua - la)}', 3),
        P(f'Find the median and interquartile range for {B}.', f'median {num(mdb)}, IQR {num(ub - lb_)}', f'B1 median {num(mdb)}; M1 LQ {num(lb_)}, UQ {num(ub)}; A1 IQR {num(ub - lb_)}', 3),
        P(f'Make two comparisons between the {what} for {A} and {B}.', cmp_sentences(A, B, mda, mdb, ua - la, ub - lb_), 'B1 compares medians in context; B1 compares IQRs in context', 2),
        P(f'Explain why the median and IQR are more suitable here than the mean and range if one recorded value was unusually {"large" if better == "higher" else "small"}.', 'The median and IQR are not affected by extreme values, whereas the mean and range are.', 'B1 not affected by outliers', 1),
        P(f'Using the medians, state which of {A} and {B} has the better results and give a reason.', f'{pick}, because its median is {"higher" if better == "higher" else "lower"} and {"higher" if better == "higher" else "lower"} {what} are better.', f'B1 {pick} with reason', 1),
    ]
    return cmp_(r, intro, parts)


t124.add('C4', (2, 3, 4, 5))(t124_c4)
CHAPTERS[12] = [t121, t122, t123, t124]


# ==== END OF CHAPTERS ====


# ---------------------------------------------------------------- robustness wrapper
# A parameterised draw can occasionally hit a degenerate case (e.g. too few distinct MCQ
# distractors). Retry with the same generator (whose state has advanced) before giving up.
def _key_marks(key):
    m = re.findall(r'\[(\d+)\]', key)
    if m:
        return sum(int(x) for x in m)
    m = re.findall(r'\b[MAB](\d)\b', key)
    return sum(int(x) for x in m)


def _with_marks(q):
    # Make the marks field agree with the marks shown in the marking key.
    if q and 'marks' not in q and not q.get('options'):
        k = _key_marks(q.get('key', ''))
        if k:
            q['marks'] = max(1, min(20, k))
    return q


def _robust(fn):
    def g(r, D):
        err = None
        for _ in range(12):
            try:
                q = fn(r, D)
                if q:
                    return _with_marks(q)
            except (ValueError, ZeroDivisionError, IndexError, StopIteration) as e:
                err = e
        if err:
            raise ValueError(str(err))
        return None
    g.__name__ = fn.__name__
    return g


for _tps in CHAPTERS.values():
    for _tp in _tps:
        for _t in _tp.templates:
            object.__setattr__(_t, 'fn', _robust(_t.fn))
