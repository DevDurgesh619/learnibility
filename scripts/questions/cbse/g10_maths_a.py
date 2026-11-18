"""CBSE class 10 maths (NCERT Mathematics X) families, chapters 1-5."""
from __future__ import annotations

import math
from fractions import Fraction as Fr

from qbank import F, ar, mcq, num, frac, name, two_names, inr, num_distractors, factorise, fstr
from g9_maths_h import nz, Q, mcqbank, arbank, xbank, P, fn, rad, is_sq, poly, lin, term, triple, signed, bracket, ordinal, eq2, sub
import g9_maths_b as g9b
import g9_maths_c as g9c

S = 'cbse-g10-maths-ch'
PRIMES = [2, 3, 5, 7, 11, 13]


def comp(r, lo=60, hi=3000):
    while True:
        n = 1
        for p in r.sample([2, 3, 5, 7, 11, 13], r.randint(2, 3)):
            n *= p ** r.randint(1, 3)
        if lo <= n <= hi:
            return n


# ---------------- ch01 Real Numbers ----------------

def c1s1_pf(r):
    n = comp(r)
    f = factorise(n)
    return Q(f'Express {n} as a product of its prime factors.', fstr(f), f'Divide repeatedly by primes: {n} = {fstr(f)}.',
             [fstr({**f, min(f): f[min(f)] + 1}), ' × '.join(str(p) for p in sorted(f)), fstr({(2 if 2 not in f else 3): 1, **{k: v for k, v in f.items() if k != min(f)}})])


def c1s1_mcq(r):
    return mcqbank([
        ('The Fundamental Theorem of Arithmetic states that every composite number can be expressed as …', 'a product of primes, uniquely apart from the order of the factors',
         ['a sum of two primes', 'a product of two primes only', 'a power of a single prime'], 'Statement of the theorem.'),
        ('The number 6ⁿ, for a natural number n, can never end with the digit …', '0', ['6', '2', '8'], '6ⁿ = 2ⁿ3ⁿ has no factor 5, so it is not divisible by 10.'),
        ('If p is a prime and p divides a², then …', 'p divides a', ['p divides a³ only', 'a is prime', 'p = a'], 'Theorem used in irrationality proofs.'),
        ('Which of these is a composite number?', '7 × 11 × 13 + 13', ['13', '29', '2'], '13(7 × 11 + 1) = 13 × 78 has factors other than 1 and itself.'),
        ('The exponent of 2 in the prime factorisation of 144 is …', '4', ['2', '3', '6'], '144 = 2⁴ × 3².'),
    ])(r)


def c1s1_end0(r):
    b = r.choice([4, 6, 8, 12, 3, 9, 7, 14, 18, 21, 24, 27, 16, 22, 33, 36])
    return Q(f'Check whether {b}ⁿ can end with the digit 0 for any natural number n. Give a reason.', 'No',
             f'{b} = {fstr(factorise(b))}; {b}ⁿ has no prime factor 5, so it is not divisible by 10. By the uniqueness of prime factorisation, no other factorisation exists (2 marks).')


def c1s1_composite(r):
    a, b, c = r.sample([3, 5, 7, 11, 13], 3)
    k = r.choice([1, 2, 5])
    e = f'{a} × {b} × {c} + {c * k}' if k > 1 else f'{a} × {b} × {c} + {c}'
    return Q(f'Explain why {e} is a composite number.', f'It equals {c} × {a * b + k}', f'{e} = {c}({a} × {b} + {k}) = {c} × {a * b + k}; it has a factor other than 1 and itself (2 marks).')


def c1s1_ar(r):
    n = comp(r)
    return arbank([
        (f'{n} = {fstr(factorise(n))}.', 'Every composite number can be expressed as a product of primes in exactly one way, apart from order.', 'a', 'R is the theorem behind A.'),
        ('4ⁿ can end with the digit 0 for some natural number n.', 'Any number ending in 0 has 2 and 5 as prime factors.', 'd', '4ⁿ = 2²ⁿ has no factor 5; A false, R true.'),
        ('1 is neither prime nor composite.', 'A prime has exactly two distinct factors.', 'a', '1 has only one factor.'),
    ])(r)


def c1s1_find_missing(r):
    p, q = r.sample([2, 3, 5, 7], 2)
    a, b = r.randint(1, 3), r.randint(1, 3)
    n = p ** a * q ** b
    return Q(f'In a factor tree, {n} = {p}{sub_sup(a)} × x, where x is a power of a prime. Find x and write {n} in index form.',
             f'x = {q ** b}; {n} = {fstr({p: a, q: b})}', f'x = {n} ÷ {p ** a} = {q ** b}.')


def c1s1_case(r):
    a, b = r.sample([2, 3, 5, 7, 11], 2)
    n = a * a * b * r.choice([2, 3, 5])
    f = factorise(n)
    return Q((f'In a maths quiz, a team is given the number {n}. (i) Write its prime factorisation. (ii) How many prime factors (counted with repetition) does it have? '
              f'(iii) Find the smallest number by which {n} must be multiplied to make it a perfect square. (iv) Can {n} × 5ⁿ ever end in 0 for some n? Explain.'),
             f'(i) {fstr(f)} (ii) {sum(f.values())} (iii) {math.prod(p for p, e in f.items() if e % 2)} (iv) ' + ('yes, it already has factor 2, and 5ⁿ supplies 5' if 2 in f else 'no, it has no factor 2'),
             '1 mark each part.')


# st2 HCF and LCM

def two_nums(r):
    while True:
        g = r.choice([2, 3, 4, 5, 6, 7, 8, 9, 12, 14, 15, 18])
        x, y = r.sample(range(2, 30), 2)
        if math.gcd(x, y) == 1 and 20 <= g * x <= 999 and 20 <= g * y <= 999:
            return g * x, g * y, g


def c2_hcf_lcm(r):
    a, b, g = two_nums(r)
    l = a * b // g
    fa, fb = factorise(a), factorise(b)
    return Q(f'Find the HCF and LCM of {a} and {b} by the prime factorisation method.', f'HCF = {g}, LCM = {l}',
             f'{a} = {fstr(fa)}, {b} = {fstr(fb)}; HCF = product of smallest powers of common primes = {g}; LCM = product of greatest powers = {l}.',
             [f'HCF = {l}, LCM = {g}', f'HCF = {g}, LCM = {a * b}', f'HCF = {g * 2}, LCM = {l // 2}'])


def c2_product(r):
    a, b, g = two_nums(r)
    l = a * b // g
    return Q(f'Given HCF({a}, {b}) = {g}, find LCM({a}, {b}).', str(l), f'HCF × LCM = product ⇒ LCM = {a} × {b} ÷ {g} = {l}.', num_distractors(l, a * b, l * 2, a + b))


def c2_three(r):
    xs = r.sample([6, 8, 9, 10, 12, 14, 15, 18, 20, 21, 24, 25, 28, 30, 36], 3)
    g = math.gcd(math.gcd(*xs[:2]), xs[2])
    l = math.lcm(*xs)
    return Q(f'Find the HCF and LCM of {xs[0]}, {xs[1]} and {xs[2]} using prime factorisation.', f'HCF = {g}, LCM = {l}',
             '; '.join(f'{x} = {fstr(factorise(x))}' for x in xs) + f'; HCF = {g}, LCM = {l}.', [f'HCF = {l}, LCM = {g}', f'HCF = {g}, LCM = {xs[0] * xs[1] * xs[2]}', f'HCF = {g + 1}, LCM = {l}'])


def c2_mcq(r):
    p, q = r.sample([2, 3, 5, 7], 2)
    a, b, c, d = r.randint(1, 4), r.randint(1, 4), r.randint(1, 4), r.randint(1, 4)
    h = f'{p}{sub_sup(min(a, c))} × {q}{sub_sup(min(b, d))}'
    l = f'{p}{sub_sup(max(a, c))} × {q}{sub_sup(max(b, d))}'
    cands = [l, f'{p}{sub_sup(a + c)} × {q}{sub_sup(b + d)}', f'{p}{sub_sup(max(a, c))} × {q}{sub_sup(min(b, d))}',
             f'{p}{sub_sup(min(a, c))} × {q}{sub_sup(max(b, d))}', f'{p * q}']
    return mcq(f'If x = {p}{sub_sup(a)} × {q}{sub_sup(b)} and y = {p}{sub_sup(c)} × {q}{sub_sup(d)}, then HCF(x, y) is …', h,
               [w for w in dict.fromkeys(cands) if w != h][:3],
               'HCF takes the smaller power of each common prime.', r)


def sub_sup(n):
    from qbank import sup
    return '' if n == 1 else sup(n)


def c2_explain(r):
    return xbank([
        ('Explain why HCF(a, b) × LCM(a, b) = a × b for two positive integers, using prime factorisation.', 'For each prime, min(power) + max(power) = sum of the powers in a and b.', 'Use the exponents of each prime (2 marks).'),
        ('Can two numbers have HCF 16 and LCM 380? Give a reason.', 'No.', 'The HCF must divide the LCM; 380 ÷ 16 is not a whole number (2 marks).'),
        ('Explain why HCF × LCM = product does not hold for three numbers, with an example.', 'e.g. 2, 4, 8: HCF 2, LCM 8, product 16 ≠ 64.', '2 marks.'),
        ('If two numbers are co-prime, what is their HCF and what is their LCM? Explain.', 'HCF = 1 and LCM = their product.', 'No common prime factor (2 marks).'),
    ])(r)


def c2_ar(r):
    a, b, g = two_nums(r)
    return arbank([
        (f'HCF({a}, {b}) × LCM({a}, {b}) = {a * b}.', 'For any two positive integers, HCF × LCM equals the product of the numbers.', 'a', 'R explains A.'),
        ('The HCF of two numbers can be greater than their LCM.', 'The HCF divides the LCM.', 'd', 'HCF ≤ LCM; A false, R true.'),
        ('HCF of 17 and 23 is 1.', '17 and 23 are both prime.', 'a', 'Distinct primes are co-prime.'),
    ])(r)


def c2_other(r):
    a, b, g = two_nums(r)
    l = a * b // g
    return Q(f'The HCF of two numbers is {g} and their LCM is {l}. If one number is {a}, find the other.', str(b), f'Other = HCF × LCM ÷ {a} = {g} × {l} ÷ {a} = {b} (2 marks).',
             num_distractors(b, l // g, l - a, g * a))


# st3 word problems

def c3_bells(r):
    xs = r.sample([6, 8, 9, 10, 12, 15, 16, 18, 20, 24], 3)
    l = math.lcm(*xs)
    h, m = 8 + l // 3600, (l % 3600) // 60
    return Q(f'Three bells in a school in Shimla ring at intervals of {xs[0]}, {xs[1]} and {xs[2]} seconds. If they ring together at 8:00 a.m., after how many seconds will they next ring together?', f'{l} seconds',
             f'LCM({xs[0]}, {xs[1]}, {xs[2]}) = {l} s.', num_distractors(l, math.gcd(math.gcd(*xs[:2]), xs[2]), xs[0] * xs[1], l * 2))


def c3_tiles(r):
    g = r.choice([15, 20, 24, 25, 30, 40, 45, 50, 60])
    x, y = r.sample(range(2, 15), 2)
    while math.gcd(x, y) != 1:
        y += 1
    L, B = g * x * 10, g * y * 10
    return Q(f'A rectangular hall floor is {L // 100} m {L % 100} cm long and {B // 100} m {B % 100} cm wide. Find the side of the largest square tile that can pave it exactly, and the number of tiles needed.'.replace(' 0 cm', ''),
             f'{g * 10} cm; {x * y} tiles', f'Lengths in cm: {L} and {B}; HCF = {g * 10} cm; tiles = ({L}/{g * 10}) × ({B}/{g * 10}) = {x} × {y} = {x * y} (3 marks).')


def c3_army(r):
    a, b, g = two_nums(r)
    who = r.choice(['An army contingent', 'A school band', 'A group of NCC cadets'])
    return Q(f'{who} of {a} members is to march behind a band of {b} members in the same number of columns. What is the maximum number of columns in which they can march?', str(g),
             f'HCF({a}, {b}) = {g}.', num_distractors(g, a * b // g, g * 2, abs(a - b)))


def c3_which(r):
    sit = r.choice([('the smallest length that can be measured exactly by rods of two given lengths', 'LCM'), ('the greatest length of a tape that can measure two given lengths exactly', 'HCF'),
                    ('the next time two buses leaving every few minutes depart together', 'LCM'), ('the largest number of identical gift bags made from given numbers of pens and pencils', 'HCF'),
                    ('the least number of sweets that can be shared equally among groups of 12 or 18', 'LCM')])
    return Q(f'Do we need the HCF or the LCM to find {sit[0]}? Give a reason.', sit[1],
             'HCF: largest common divisor (splitting into equal groups/greatest measure). LCM: smallest common multiple (events coinciding/least common quantity).', ['HCF' if sit[1] == 'LCM' else 'LCM', 'Both HCF and LCM', 'Neither'])


def c3_remainder(r):
    xs = r.sample([12, 15, 18, 20, 24, 30, 36, 40, 45], 3)
    k = r.randint(2, 9)
    l = math.lcm(*xs)
    return Q(f'Find the smallest number which when divided by {xs[0]}, {xs[1]} and {xs[2]} leaves a remainder of {k} in each case.', str(l + k),
             f'LCM = {l}; add the remainder: {l} + {k} = {l + k} (3 marks).', num_distractors(l + k, l, l - k, l + 2 * k))


def c3_hcf_rem(r):
    g = r.randint(7, 40)
    r1, r2 = r.randint(1, g - 1), r.randint(1, g - 1)
    a, b = g * r.randint(5, 20) + r1, g * r.randint(5, 20) + r2
    if math.gcd(a - r1, b - r2) != g:
        raise ValueError
    return Q(f'Find the largest number that divides {a} and {b}, leaving remainders {r1} and {r2} respectively.', str(g),
             f'It divides {a} − {r1} = {a - r1} and {b} − {r2} = {b - r2}; HCF({a - r1}, {b - r2}) = {g} (3 marks).')


def c3_ar(r):
    return arbank([
        ('To find when two traffic lights changing every 45 s and 60 s next change together, we find their LCM.', 'The LCM is the smallest common multiple of the numbers.', 'a', 'R explains A.'),
        ('The greatest length that measures 6 m and 8 m exactly is 24 m.', 'Such a length is the HCF of the two lengths.', 'd', 'It is HCF = 2 m; A false, R true.'),
        ('The least number of mangoes that can be shared equally among 4, 6 or 10 children is 60.', 'LCM(4, 6, 10) = 60.', 'a', 'R explains A.'),
    ])(r)


def c3_case(r):
    a, b = r.choice([(36, 48), (40, 60), (45, 75), (32, 48), (54, 72), (60, 84)])
    g, l = math.gcd(a, b), a * b // math.gcd(a, b)
    return Q((f'Two athletes run laps around a circular track in a stadium in Chennai. Ravi takes {a} s and Sunita takes {b} s per lap. They start together from the same point in the same direction. '
              f'(i) After how many seconds will they meet again at the starting point? (ii) How many laps will each have completed then? (iii) Find HCF({a}, {b}) and verify HCF × LCM = {a} × {b}.'),
             f'(i) {l} s (ii) Ravi {l // a}, Sunita {l // b} (iii) HCF {g}; {g} × {l} = {a * b}', 'LCM (2), laps (1), check (1).')


# st4 irrationality

def c4_prove(r):
    p = r.choice([2, 3, 5, 7])
    return Q(f'Prove that √{p} is irrational.', 'Proof by contradiction.',
             f'Assume √{p} = a/b with a, b co-prime, b ≠ 0 (1). Then {p}b² = a² ⇒ {p} divides a² ⇒ {p} divides a; write a = {p}c (1). Then b² = {p}c² ⇒ {p} divides b (1). So {p} divides both a and b, contradicting co-primality; hence √{p} is irrational.')


def c4_combo(r):
    a, b, p = r.randint(1, 9), r.randint(2, 7), r.choice([2, 3, 5])
    s = r.choice(['+', '−'])
    return Q(f'Given that √{p} is irrational, prove that {a} {s} {b}√{p} is irrational.', 'Proof by contradiction.',
             f'Suppose {a} {s} {b}√{p} = r (rational). Then √{p} = {"(r − " + str(a) + ")" if s == "+" else "(" + str(a) + " − r)"}/{b}, which is rational, a contradiction (3 marks).')


def c4_mcq(r):
    return mcqbank([
        ('Which of the following is irrational?', '2 + √3', ['√49', '0.4̄', '22/7'], '√3 is irrational; rational + irrational is irrational.'),
        ('Which of the following is rational?', '(3 + √5)(3 − √5)', ['3 + √5', '√5/3', '√15'], '= 9 − 5 = 4.'),
        ('In the proof that √3 is irrational, we use the fact that if 3 divides a², then …', '3 divides a', ['9 divides a', 'a is odd', 'a = 3'], 'Since 3 is prime.'),
        ('The product of a non-zero rational number and an irrational number is …', 'always irrational', ['always rational', 'zero', 'sometimes rational'], 'If it were rational, dividing by the rational would make the irrational rational.'),
    ])(r)


def c4_ar(r):
    p = r.choice([2, 3, 5, 7])
    a = r.randint(2, 9)
    return arbank([
        (f'{a}√{p} is irrational.', 'The product of a non-zero rational and an irrational number is irrational.', 'a', 'R explains A.'),
        (f'(√{p} + {a})(√{p} − {a}) is rational.', '(x + y)(x − y) = x² − y².', 'a', f'It equals {p} − {a * a} = {p - a * a}.'),
        ('6 + √2 is irrational.', '√2 is irrational and 6 is rational.', 'a', 'Rational + irrational is irrational.'),
        (f'√{p * 4} is rational.', f'√{p * 4} = 2√{p}.', 'd', 'A false (2 × irrational), R true.'),
    ])(r)


def c4_explain(r):
    p = r.choice([2, 3, 5, 6, 7])
    return xbank([
        (f'Explain why, in the proof that √{p} is irrational, we start by assuming √{p} = a/b with a and b co-prime.', 'Any rational number can be written in lowest terms; the proof shows this leads to a common factor, a contradiction.', '2 marks.'),
        ('Show that 5 − √3 is irrational, given that √3 is irrational (outline the steps).', 'Assume 5 − √3 = r rational ⇒ √3 = 5 − r rational: contradiction.', '2 marks.'),
        ('Explain why 1/√2 is irrational.', '1/√2 = √2/2, a non-zero rational times an irrational.', '2 marks.'),
    ])(r)


def c4_rational_check(r):
    a, p = r.randint(2, 6), r.choice([2, 3, 5, 7])
    items = [(f'({a} + √{p})({a} − √{p})', 'Rational', f'= {a * a} − {p} = {a * a - p}'), (f'({a} + √{p})²', 'Irrational', f'= {a * a + p} + {2 * a}√{p}'),
             (f'√{p * a * a}', 'Irrational', f'= {a}√{p}'), (f'√{a * a * 4}/{a}', 'Rational', f'= {2}'), (f'{a}/√{p}', 'Irrational', f'= {a}√{p}/{p}' if a % p else f'= {a // p}√{p}')]
    e, ans, why = r.choice(items)
    return Q(f'Is {e} rational or irrational? Justify.', ans, f'{e} {why}.', ['Irrational' if ans == 'Rational' else 'Rational', 'Neither', 'Cannot be decided'])


def c4_case(r):
    p = r.choice([2, 3, 5])
    return Q((f'A teacher asks the class to show that √{p} is irrational. Ishita writes: "Suppose √{p} = a/b, where a and b are co-prime integers, b ≠ 0." '
              f'(i) Square both sides and write a² in terms of b². (ii) What can you conclude about a, and why? (iii) Substitute a = {p}c and conclude about b. (iv) Where is the contradiction?'),
             f'(i) a² = {p}b² (ii) {p} divides a² so {p} divides a ({p} is prime) (iii) b² = {p}c², so {p} divides b (iv) a and b have common factor {p}, contradicting co-primality',
             '1 mark each part.')


# ---------------- ch02 Polynomials ----------------

def quad_roots(r, rational=False):
    while True:
        a = r.choice([1, 1, 1, 2, 3]) if rational else 1
        p, q = nz(r, 1, 9), nz(r, 1, 9)
        if p != q and p != -q:
            break
    return a, p, q  # roots p and q (or p/a style later)


def coeffs_from_roots(a, al, be):
    return [a, -a * (al + be), a * al * be]


def c2s1_degree(r):
    return mcqbank([
        ('The degree of the polynomial 4x⁴ + 0x³ + 0x⁵ + 5x + 7 is …', '4', ['5', '3', '7'], 'The term 0x⁵ vanishes.'),
        ('A quadratic polynomial has degree …', '2', ['1', '3', '0'], 'Definition.'),
        ('The graph of a quadratic polynomial ax² + bx + c (a ≠ 0) is …', 'a parabola', ['a straight line', 'a circle', 'two straight lines'], 'Definition.'),
        ('A cubic polynomial can have at most … zeroes.', '3', ['2', '4', '1'], 'At most the degree.'),
        ('Which of these is a cubic polynomial?', '2x³ − 5x + 1', ['x² + x³⁄x', '√x³ + 1', '1/x³ + 2'], 'Highest power 3 with whole-number exponents.'),
    ])(r)


def c2s1_shape(r):
    a = nz(r, 1, 5)
    b, c = nz(r, 0, 9), nz(r, 0, 9)
    return Q(f'Does the parabola y = {poly([a, b, c])} open upwards or downwards? Give a reason.', 'Upwards' if a > 0 else 'Downwards',
             f'The coefficient of x² is {fn(a)}, which is {"positive" if a > 0 else "negative"}.', ['Downwards' if a > 0 else 'Upwards', 'It is a straight line', 'Neither'])


def c2s1_value(r):
    c = [nz(r, 1, 5), nz(r, 0, 9), nz(r, 0, 9)]
    k = nz(r, 1, 4)
    v = c[0] * k * k + c[1] * k + c[2]
    return Q(f'If p(x) = {poly(c)}, find p({fn(k)}).', fn(v), f'p({fn(k)}) = {fn(c[0])}({fn(k)})² {signed(c[1])}({fn(k)}) {signed(c[2])} = {fn(v)}.',
             num_distractors(v, c[0] * k * k - c[1] * k + c[2], c[0] * 2 * k + c[1] * k + c[2]))


def c2s1_explain(r):
    return xbank([
        ('Explain why a linear polynomial has exactly one zero but a quadratic polynomial may have 0, 1 or 2 zeroes.', 'A line (not parallel to the x-axis) cuts the x-axis once; a parabola may cut it twice, touch it once or miss it.', '2 marks.'),
        ('Explain the difference between the degree and the number of terms of a polynomial, with an example.', 'e.g. x³ + 1 has degree 3 but 2 terms.', '2 marks.'),
        ('Explain why the vertex of y = x² − 4 is at (0, −4) and whether the graph cuts the x-axis.', 'x² ≥ 0 so the least value is −4 at x = 0; it cuts the x-axis at x = ±2.', '2 marks.'),
    ])(r)


def c2s1_ar(r):
    return arbank([
        ('The graph of y = −2x² + 3 opens downwards.', 'If a < 0, the parabola y = ax² + bx + c opens downwards.', 'a', 'R explains A.'),
        ('x² + 1/x is a quadratic polynomial.', 'A quadratic polynomial has degree 2.', 'd', '1/x has a negative exponent; A false, R true.'),
        ('A cubic polynomial can have at most three zeroes.', 'A polynomial of degree n has at most n zeroes.', 'a', 'R explains A.'),
    ])(r)


def c2s1_case(r):
    h = r.choice([20, 30, 40, 45])
    k = r.choice([5, 10])
    return Q((f'The path of a ball thrown in a cricket ground is modelled by h(t) = −5t² + {k * 2}t + {h // 5}, where h is in metres and t in seconds. '
              f'(i) What type of polynomial is h(t)? (ii) Does its graph open upwards or downwards? (iii) Find h(1). (iv) What does the zero of h(t) with t > 0 represent?'),
             f'(i) quadratic (ii) downwards (a = −5 < 0) (iii) {-5 + 2 * k + h // 5} m (iv) the time when the ball reaches the ground', '1 mark each part.')


# st2 geometric meaning

def c2s2_count(r):
    k = r.randint(0, 3)
    desc = {0: 'does not meet the x-axis at all', 1: 'touches the x-axis at exactly one point', 2: 'cuts the x-axis at two points', 3: 'cuts the x-axis at three points'}[k]
    deg = 'cubic' if k == 3 else r.choice(['quadratic', 'cubic'])
    return Q(f'The graph of y = p(x), where p(x) is a {deg} polynomial, {desc}. How many zeroes does p(x) have?', str(k),
             'The number of zeroes equals the number of points where the graph meets the x-axis.', [str(v) for v in (0, 1, 2, 3) if v != k])


def c2s2_read(r):
    a, p, q = quad_roots(r)
    return Q(f'The graph of y = {poly(coeffs_from_roots(1, p, q))} cuts the x-axis at two points. Find these points.', f'{P(min(p, q), 0)} and {P(max(p, q), 0)}',
             f'Solve {poly(coeffs_from_roots(1, p, q))} = 0: (x {signed(-p)})(x {signed(-q)}) = 0 ⇒ x = {fn(p)}, {fn(q)}.',
             [f'{P(-min(p, q), 0)} and {P(-max(p, q), 0)}', f'{P(0, min(p, q))} and {P(0, max(p, q))}', f'{P(min(p, q), 0)} and {P(p * q, 0)}'])


def c2s2_mcq(r):
    return mcqbank([
        ('The zeroes of a polynomial p(x) are the … of the points where the graph of y = p(x) meets the x-axis.', 'x-coordinates', ['y-coordinates', 'slopes', 'distances from the origin'], 'At those points y = 0.'),
        ('If the graph of a quadratic polynomial does not meet the x-axis, it has …', 'no real zeroes', ['two equal zeroes', 'two distinct zeroes', 'infinitely many zeroes'], 'No point with y = 0.'),
        ('The graph of y = x² touches the x-axis at …', '(0, 0) only', ['(1, 0) and (−1, 0)', 'no point', '(0, 1)'], 'x² = 0 only at x = 0.'),
    ])(r)


def c2s2_explain(r):
    a, p, q = quad_roots(r)
    return Q(f'Explain how you would find the zeroes of {poly(coeffs_from_roots(1, p, q))} from its graph, and state them.', f'{fn(min(p, q))} and {fn(max(p, q))}',
             'Read the x-coordinates of the points where the parabola cuts the x-axis (2 marks).')


def c2s2_ar(r):
    return arbank([
        ('y = x² + 4 has no real zeroes.', 'The graph of y = x² + 4 lies entirely above the x-axis.', 'a', 'R explains A.'),
        ('A quadratic polynomial whose graph touches the x-axis has two equal zeroes.', 'Touching the x-axis gives one point of contact.', 'a', 'Repeated root at the point of contact.'),
        ('Every cubic polynomial has three real zeroes.', 'A cubic graph always crosses the x-axis at least once.', 'd', 'e.g. x³ + x has one real zero; A false, R true.'),
    ])(r)


def c2s2_case(r):
    a, p, q = quad_roots(r)
    p, q = abs(p), -abs(q)
    return Q((f'An engineer models a bridge arch with y = −(x {signed(-p)})(x {signed(-q)}) (in metres, x-axis along the road). (i) Find where the arch meets the road. '
              f'(ii) How wide is the arch at road level? (iii) Find the height of the arch above the point x = 0. (iv) How many zeroes does the polynomial have, and why?'),
             f'(i) x = {fn(q)} and x = {fn(p)} (ii) {p - q} m (iii) {fn(-(0 - p) * (0 - q))} m (iv) 2; the parabola cuts the x-axis twice', '1 mark each part.')


# st3 zeroes and coefficients

def c2s3_zeros(r):
    a = r.choice([1, 1, 2, 3])
    al, be = Fr(nz(r, 1, 9), r.choice([1, a])), Fr(nz(r, 1, 9), 1)
    if al == be:
        raise ValueError
    c = coeffs_from_roots(a, al, be)
    if any(Fr(x).denominator != 1 for x in c):
        raise ValueError
    c = [int(x) for x in c]
    if c[1] == 0:
        raise ValueError
    return Q(f'Find the zeroes of {poly(c)} and verify the relationship between the zeroes and the coefficients.', f'{fn(al)} and {fn(be)}',
             f'Factorise: zeroes {fn(al)}, {fn(be)}. Sum = {fn(al + be)} = −b/a = {fn(Fr(-c[1], c[0]))}; product = {fn(al * be)} = c/a = {fn(Fr(c[2], c[0]))} (3 marks).')


def c2s3_sum(r):
    c = [r.choice([1, 2, 3, 4]), nz(r, 1, 12), nz(r, 1, 12)]
    which = r.choice(['sum', 'product'])
    ans = Fr(-c[1], c[0]) if which == 'sum' else Fr(c[2], c[0])
    return mcq(f'The {which} of the zeroes of {poly(c)} is …', fn(ans), list(dict.fromkeys(w for w in [fn(-ans), fn(Fr(c[1], c[0])) if which == 'product' else fn(Fr(c[2], c[0])), fn(ans + 1), fn(Fr(c[0], c[2]) if c[2] else 2)] if w != fn(ans)))[:3],
               'Sum = −b/a, product = c/a.', r)


def c2s3_sym(r):
    a, p, q = quad_roots(r)
    s, pr = p + q, p * q
    which = r.choice(['α² + β²', '1/α + 1/β', '(α − β)²', 'α²β + αβ²'])
    v = {'α² + β²': Fr(s * s - 2 * pr), '1/α + 1/β': Fr(s, pr), '(α − β)²': Fr(s * s - 4 * pr), 'α²β + αβ²': Fr(pr * s)}[which]
    return Q(f'If α and β are the zeroes of {poly([1, -s, pr])}, find {which} without finding α and β.', fn(v),
             f'α + β = {fn(s)}, αβ = {fn(pr)}. ' + {'α² + β²': '(α + β)² − 2αβ', '1/α + 1/β': '(α + β)/αβ', '(α − β)²': '(α + β)² − 4αβ', 'α²β + αβ²': 'αβ(α + β)'}[which] + f' = {fn(v)} (3 marks).',
             num_distractors(float(v), s * s + 2 * pr, s * s, pr))


def c2s3_find_k(r):
    a = r.choice([1, 2, 3])
    al = nz(r, 1, 6)
    be = nz(r, 1, 6)
    c = coeffs_from_roots(a, al, be)
    return Q(f'If one zero of {poly([c[0], c[1]])} + k is {fn(al)}, find k and the other zero.'.replace(f'{poly([c[0], c[1]])} + k', f'{term(c[0], "x", first=True, power=2)}{term(c[1], "x")} + k'),
             f'k = {fn(c[2])}; other zero {fn(be)}', f'Put x = {fn(al)}: k = {fn(c[2])}; sum of zeroes = {fn(Fr(-c[1], c[0]))} ⇒ other = {fn(be)} (3 marks).')


def c2s3_explain(r):
    return xbank([
        ('Derive the relationship between the zeroes and coefficients of ax² + bx + c from its factorised form a(x − α)(x − β).', 'Expanding: a x² − a(α + β)x + aαβ; compare: α + β = −b/a, αβ = c/a.', '2 marks.'),
        ('If both zeroes of x² + bx + c are positive, what can you say about the signs of b and c? Explain.', 'b < 0, c > 0.', 'Sum −b > 0 and product c > 0 (2 marks).'),
        ('If one zero of ax² + bx + c is the reciprocal of the other, show that c = a.', 'αβ = 1 = c/a.', '2 marks.'),
    ])(r)


def c2s3_ar(r):
    a, p, q = quad_roots(r)
    return arbank([
        (f'The sum of the zeroes of {poly([1, -(p + q), p * q])} is {fn(p + q)}.', 'For ax² + bx + c, the sum of the zeroes is −b/a.', 'a', 'R explains A.'),
        (f'The product of the zeroes of {poly([1, -(p + q), p * q])} is {fn(-(p * q))}.', 'For ax² + bx + c, the product of the zeroes is c/a.', 'd', f'Product = {fn(p * q)}; A false, R true.'),
        ('If the zeroes of x² + kx + 9 are equal and positive, then k = −6.', 'Equal zeroes α, α give α² = 9 and 2α = −k.', 'a', 'α = 3, k = −6.'),
    ])(r)


def c2s3_cubic(r):
    roots = r.sample([n for n in range(-4, 5) if n], 3)
    a, b, c = roots
    co = [1, -(a + b + c), a * b + b * c + c * a, -(a * b * c)]
    return Q(f'Verify that {fn(a)}, {fn(b)} and {fn(c)} are the zeroes of the cubic polynomial {poly(co)}, and check the relationships between the zeroes and the coefficients.', 'Verified',
             f'p({fn(a)}) = p({fn(b)}) = p({fn(c)}) = 0. Sum {fn(a + b + c)} = −b/a; sum of products in pairs {fn(a * b + b * c + c * a)} = c/a; product {fn(a * b * c)} = −d/a (5 marks).')


def c2s3_case(r):
    a, p, q = quad_roots(r)
    p, q = abs(p) + 1, abs(q) + 2
    if p == q:
        q += 1
    return Q((f'A rectangular garden has area given by A(x) = {poly([1, -(p + q), p * q])} square metres for a design parameter x. The zeroes α, β of A(x) mark the design limits. '
              f'(i) Find α + β and αβ. (ii) Find the zeroes. (iii) Find α² + β². (iv) Write a quadratic polynomial whose zeroes are 2α and 2β.'),
             f'(i) {p + q}, {p * q} (ii) {p} and {q} (iii) {p * p + q * q} (iv) x² − {2 * (p + q)}x + {4 * p * q}', '1 mark each part.')


# st4 forming quadratics

def c2s4_form(r):
    s = Fr(nz(r, 1, 9), r.choice([1, 1, 2, 3, 4]))
    p = Fr(nz(r, 1, 9), r.choice([1, 1, 2, 3, 4]))
    d = math.lcm(s.denominator, p.denominator)
    co = [d, -s * d, p * d]
    co = [int(x) for x in co]
    return Q(f'Find a quadratic polynomial whose sum and product of zeroes are {fn(s)} and {fn(p)} respectively.', poly(co),
             f'k[x² − (sum)x + (product)] = k[x² − ({fn(s)})x + ({fn(p)})]; take k = {d}: {poly(co)}.',
             [poly([d, int(s * d), int(p * d)]), poly([d, int(-p * d), int(s * d)]), poly([d, int(-s * d), int(-p * d)])])


def c2s4_roots(r):
    a, p, q = quad_roots(r)
    co = [1, -(p + q), p * q]
    return mcq(f'A quadratic polynomial whose zeroes are {fn(p)} and {fn(q)} is …', poly(co), [poly([1, p + q, p * q]), poly([1, -(p + q), -(p * q)]), poly([1, p * q, -(p + q)])],
               'x² − (sum)x + product.', r)


def c2s4_surd(r):
    a, b = r.randint(1, 6), r.choice([2, 3, 5, 6, 7])
    return Q(f'Find a quadratic polynomial whose zeroes are {a} + √{b} and {a} − √{b}.', poly([1, -2 * a, a * a - b]),
             f'Sum = {2 * a}, product = {a * a} − {b} = {a * a - b}; x² − {2 * a}x {signed(a * a - b)} (3 marks).', [poly([1, 2 * a, a * a - b]), poly([1, -2 * a, a * a + b]), poly([1, -a, a * a - b])])


def c2s4_transform(r):
    a, p, q = quad_roots(r)
    k = r.choice([2, 3, -1])
    return Q(f'If α and β are the zeroes of {poly([1, -(p + q), p * q])}, find a quadratic polynomial whose zeroes are {k}α and {k}β.'.replace('−1α', '−α').replace('−1β', '−β'),
             poly([1, -k * (p + q), k * k * p * q]), f'New sum = {k}(α + β) = {fn(k * (p + q))}; new product = {k * k}αβ = {fn(k * k * p * q)} (3 marks).')


def c2s4_explain(r):
    return xbank([
        ('Explain why there are infinitely many quadratic polynomials with a given sum and product of zeroes.', 'k[x² − Sx + P] has the same zeroes for every non-zero k.', '2 marks.'),
        ('Explain how to find a quadratic polynomial when its zeroes α and β are known.', 'Use x² − (α + β)x + αβ, or any non-zero multiple of it.', '2 marks.'),
    ])(r)


def c2s4_ar(r):
    s, p = nz(r, 1, 9), nz(r, 1, 9)
    return arbank([
        (f'{poly([1, -s, p])} and {poly([2, -2 * s, 2 * p])} have the same zeroes.', 'Multiplying a polynomial by a non-zero constant does not change its zeroes.', 'a', 'R explains A.'),
        (f'A quadratic polynomial with sum of zeroes {fn(s)} and product {fn(p)} is x² + {fn(s)}x + {fn(p)}.'.replace('+ −', '− '), 'A quadratic polynomial with sum S and product P of zeroes is x² − Sx + P.', 'd', 'The middle sign is wrong; A false, R true.'),
    ])(r)


def c2s4_case(r):
    a, b = r.randint(2, 9), r.randint(2, 9)
    return Q((f'A student is asked to design a quiz question: "Find a quadratic polynomial whose zeroes are {a} and −{b}." '
              f'(i) Find the sum and product of the zeroes. (ii) Write the polynomial. (iii) Write another polynomial with the same zeroes. (iv) Check that x = {a} is a zero of your answer to (ii).'),
             f'(i) sum {fn(a - b)}, product {fn(-a * b)} (ii) {poly([1, -(a - b), -a * b])} (iii) e.g. {poly([2, -2 * (a - b), -2 * a * b])} (iv) {a * a} {signed(-(a - b) * a)} {signed(-a * b)} = 0',
             '1 mark each part.')


# ---------------- ch03 Pair of linear equations ----------------

def lin_pair(r, lo=-6, hi=8):
    while True:
        x, y = r.randint(lo, hi), r.randint(lo, hi)
        a1, b1, a2, b2 = nz(r, 1, 6), nz(r, 1, 6), nz(r, 1, 6), nz(r, 1, 6)
        if a1 * b2 - a2 * b1 != 0:
            return a1, b1, a1 * x + b1 * y, a2, b2, a2 * x + b2 * y, x, y


def c3s1_graph(r):
    a1, b1, c1, a2, b2, c2, x, y = lin_pair(r, -3, 6)
    return Q(f'Solve graphically: {eq2(a1, b1, c1)} and {eq2(a2, b2, c2)}. State the point of intersection.', f'x = {fn(x)}, y = {fn(y)}; lines meet at {P(x, y)}',
             f'Plot two points on each line; they intersect at {P(x, y)}. Check in both equations (3 marks).', [P(y, x) if x != y else P(x + 1, y), P(-x, y) if x else P(1, y), P(x, -y) if y else P(x, 2)])


def c3s1_mcq(r):
    return mcqbank([
        ('If the lines representing a pair of linear equations intersect at one point, the pair has …', 'a unique solution', ['no solution', 'infinitely many solutions', 'exactly two solutions'], 'One common point.'),
        ('If the lines are parallel, the pair of equations is …', 'inconsistent', ['consistent with a unique solution', 'dependent', 'consistent with infinitely many solutions'], 'No common point.'),
        ('If the lines coincide, the pair of equations has …', 'infinitely many solutions', ['no solution', 'a unique solution', 'two solutions'], 'Every point is common.'),
    ])(r)


def c3s1_vertices(r):
    a, b = r.randint(1, 4), r.randint(2, 8)
    c = a * b
    return Q(f'Draw the graphs of y = {a}x and x + y = {b + c}... find the vertices of the triangle formed by these lines and the x-axis.'.replace('... ', '; '),
             f'(0, 0), ({b + c}, 0), ({fn(Fr(b + c, a + 1))}, {fn(Fr(a * (b + c), a + 1))})',
             f'y = {a}x meets x + y = {b + c} where x = {fn(Fr(b + c, a + 1))}; the lines meet the x-axis at (0, 0) and ({b + c}, 0) (4 marks).')


def c3s1_explain(r):
    return xbank([
        ('Explain why the graphical method may not give an exact answer for 3x + 2y = 7, 2x − 3y = 1 type problems in general.', 'If the intersection has fractional coordinates, it cannot be read exactly from a graph; algebraic methods are exact.', '2 marks.'),
        ('Explain how the graph shows whether a pair of linear equations is consistent.', 'Intersecting or coincident lines ⇒ consistent; parallel lines ⇒ inconsistent.', '2 marks.'),
    ])(r)


def c3s1_ar(r):
    k = r.randint(2, 6)
    return arbank([
        (f'The lines x + y = {k} and 2x + 2y = {2 * k} coincide.', 'One equation is a non-zero multiple of the other.', 'a', 'R explains A.'),
        (f'The lines x + y = {k} and x + y = {k + 2} intersect at one point.', 'Lines with the same slope and different intercepts are parallel.', 'd', 'They are parallel; A false, R true.'),
        ('A pair of linear equations can have exactly two solutions.', 'Two distinct straight lines meet in at most one point.', 'd', 'A false, R true.'),
    ])(r)


def c3s1_case(r):
    p, q = r.choice([(10, 5), (20, 10), (15, 5), (12, 8)])
    x, y = r.randint(2, 8), r.randint(2, 8)
    return Q((f'In a school stationery shop, {x + y} items were sold: some pencils at ₹{q} each and some pens at ₹{p} each, for ₹{p * x + q * y} in all. '
              f'(i) Form the pair of linear equations (x pens, y pencils). (ii) Solve them graphically by listing two points on each line. (iii) How many pens were sold? (iv) What does the point of intersection represent?'),
             f'(i) x + y = {x + y}, {p}x + {q}y = {p * x + q * y} (ii) e.g. ({x + y}, 0), (0, {x + y}); (0, {fn(Fr(p * x + q * y, q))}), ({fn(Fr(p * x + q * y, p))}, 0) (iii) {x} (iv) the numbers of pens and pencils that satisfy both conditions',
             '1 mark each part.')


# st2 consistency

def c3s2_type(r):
    a1, b1 = nz(r, 1, 6), nz(r, 1, 6)
    k = r.choice([2, 3, -2, Fr(1, 2)])
    kind = r.choice(['unique', 'none', 'infinite'])
    c1 = nz(r, 1, 9)
    if kind == 'unique':
        a2, b2 = a1 * k, b1 * k + nz(r, 1, 3)
        c2 = nz(r, 1, 9)
    elif kind == 'none':
        a2, b2, c2 = a1 * k, b1 * k, c1 * k + nz(r, 1, 3)
    else:
        a2, b2, c2 = a1 * k, b1 * k, c1 * k
    if any(Fr(v).denominator != 1 for v in (a2, b2, c2)):
        raise ValueError
    a2, b2, c2 = int(a2), int(b2), int(c2)
    ans = {'unique': 'Intersecting lines; unique solution (consistent)', 'none': 'Parallel lines; no solution (inconsistent)', 'infinite': 'Coincident lines; infinitely many solutions (consistent, dependent)'}[kind]
    return Q(f'Compare the ratios a₁/a₂, b₁/b₂ and c₁/c₂ and say whether the lines {eq2(a1, b1, c1)} and {eq2(a2, b2, c2)} intersect, are parallel or coincide.', ans,
             f'a₁/a₂ = {fn(Fr(a1, a2))}, b₁/b₂ = {fn(Fr(b1, b2))}, c₁/c₂ = {fn(Fr(c1, c2))}.', [v for k_, v in {'unique': 'Intersecting lines; unique solution (consistent)', 'none': 'Parallel lines; no solution (inconsistent)', 'infinite': 'Coincident lines; infinitely many solutions (consistent, dependent)'}.items() if k_ != kind] + ['Perpendicular lines; two solutions'])


def c3s2_k(r):
    a1, b1 = r.randint(1, 5), r.randint(1, 5)
    m = r.choice([2, 3, 4])
    kind = r.choice(['no solution', 'infinitely many solutions'])
    c1 = r.randint(1, 9)
    c2 = c1 * m if kind == 'infinitely many solutions' else c1 * m + r.randint(1, 4)
    return Q(f'Find the value of k for which the pair {term(a1, "x", first=True)}{term(b1, "y")} = {c1} and {a1 * m}x + ky = {c2} has {kind}.', f'k = {b1 * m}',
             f'Need a₁/a₂ = b₁/b₂: {a1}/{a1 * m} = {b1}/k ⇒ k = {b1 * m}; then c₁/c₂ = {fn(Fr(c1, c2))} is {"equal" if kind.startswith("inf") else "not equal"} to {fn(Fr(1, m))} ✓ (3 marks).',
             [f'k = {b1}', f'k = {-b1 * m}', f'k = {b1 * m + 1}'])


def c3s2_mcq(r):
    return mcqbank([
        ('The pair a₁x + b₁y + c₁ = 0, a₂x + b₂y + c₂ = 0 has a unique solution if …', 'a₁/a₂ ≠ b₁/b₂', ['a₁/a₂ = b₁/b₂ ≠ c₁/c₂', 'a₁/a₂ = b₁/b₂ = c₁/c₂', 'c₁ = c₂'], 'Lines intersect.'),
        ('The pair has no solution if …', 'a₁/a₂ = b₁/b₂ ≠ c₁/c₂', ['a₁/a₂ ≠ b₁/b₂', 'a₁/a₂ = b₁/b₂ = c₁/c₂', 'a₁ = a₂ only'], 'Parallel lines.'),
        ('The pair is dependent (infinitely many solutions) if …', 'a₁/a₂ = b₁/b₂ = c₁/c₂', ['a₁/a₂ ≠ b₁/b₂', 'a₁/a₂ = b₁/b₂ ≠ c₁/c₂', 'b₁ = b₂ only'], 'Coincident lines.'),
    ])(r)


def c3s2_explain(r):
    return xbank([
        ('Explain why a₁/a₂ = b₁/b₂ means the two lines have the same slope.', 'Slope of a₁x + b₁y + c₁ = 0 is −a₁/b₁; equal ratios give −a₁/b₁ = −a₂/b₂.', '2 marks.'),
        ('Explain the difference between "inconsistent" and "dependent" pairs of equations.', 'Inconsistent: no common solution (parallel lines). Dependent: infinitely many solutions (coincident lines).', '2 marks.'),
    ])(r)


def c3s2_ar(r):
    return arbank([
        ('The pair x + 2y = 3, 2x + 4y = 7 is inconsistent.', 'For these equations a₁/a₂ = b₁/b₂ ≠ c₁/c₂.', 'a', '1/2 = 2/4 ≠ 3/7; R explains A.'),
        ('The pair 2x − 3y = 8, 4x − 6y = 9 has a unique solution.', 'a₁/a₂ ≠ b₁/b₂ gives a unique solution.', 'd', 'Here a₁/a₂ = b₁/b₂ (parallel); A false, R true.'),
        ('The pair x − y = 1, 3x − 3y = 3 has infinitely many solutions.', 'All three ratios are equal.', 'a', 'R explains A.'),
    ])(r)


def c3s2_case(r):
    a, b = r.randint(2, 5), r.randint(2, 5)
    c = r.randint(10, 30)
    return Q((f'Two friends describe the cost of {a} pens and {b} pencils: Meera says it is ₹{c}, and Arjun says {2 * a} pens and {2 * b} pencils cost ₹{2 * c + 4}. '
              f'(i) Write the two equations. (ii) Compare the ratios a₁/a₂, b₁/b₂, c₁/c₂. (iii) Are their statements consistent? (iv) What would Arjun\'s total have to be for the statements to agree?'),
             f'(i) {a}x + {b}y = {c}, {2 * a}x + {2 * b}y = {2 * c + 4} (ii) 1/2, 1/2, {fn(Fr(c, 2 * c + 4))} (iii) no; parallel lines (inconsistent) (iv) ₹{2 * c}', '1 mark each part.')


# st3 substitution, st4 elimination

def c3s3_sub(r):
    while True:
        x, y = r.randint(-5, 9), r.randint(-5, 9)
        m, k = nz(r, 1, 4), nz(r, 0, 9)
        a2, b2 = nz(r, 1, 6), nz(r, 1, 6)
        if a2 + b2 * m != 0 and y == m * x + k:
            break
        y = m * x + k
        if a2 + b2 * m != 0:
            break
    c2 = a2 * x + b2 * y
    return Q(f'Solve by substitution: y = {lin(m, k)} and {eq2(a2, b2, c2)}.', f'x = {fn(x)}, y = {fn(y)}',
             f'Substitute y: {term(a2, "x", first=True)} {"+" if b2 > 0 else "−"} {"" if abs(b2) == 1 else abs(b2)}({lin(m, k)}) = {fn(c2)} ⇒ x = {fn(x)}; y = {fn(y)} (3 marks).',
             [f'x = {fn(y)}, y = {fn(x)}', f'x = {fn(-x)}, y = {fn(-y)}', f'x = {fn(x + 1)}, y = {fn(m * (x + 1) + k)}'])


def c3s3_sub2(r):
    a1, b1, c1, a2, b2, c2, x, y = lin_pair(r)
    a1 = 1
    c1 = x + b1 * y
    if a2 * b1 - b2 == 0:
        raise ValueError
    return Q(f'Solve using the substitution method: {eq2(1, b1, c1)} and {eq2(a2, b2, c2)}.', f'x = {fn(x)}, y = {fn(y)}',
             f'From the first, x = {fn(c1)} {signed(-b1)}y; substitute in the second and solve: y = {fn(y)}, x = {fn(x)} (3 marks).',
             [f'x = {fn(y)}, y = {fn(x)}', f'x = {fn(x + 2)}, y = {fn(y - 1)}', f'x = {fn(-x)}, y = {fn(y)}'])


def c3s3_mcq(r):
    a1, b1, c1, a2, b2, c2, x, y = lin_pair(r)
    return mcq(f'The solution of {eq2(a1, b1, c1)} and {eq2(a2, b2, c2)} is …', P(x, y), [P(y, x) if x != y else P(x + 1, y - 1), P(-x, -y) if (x, y) != (0, 0) else P(1, 1), P(x + 1, y)],
               'Check each pair in both equations.', r) if all(not (a1 * px + b1 * py == c1 and a2 * px + b2 * py == c2) for px, py in [(y, x), (x + 1, y)]) else _raise()


def _raise():
    raise ValueError


def c3s4_elim(r):
    a1, b1, c1, a2, b2, c2, x, y = lin_pair(r)
    return Q(f'Solve by elimination: {eq2(a1, b1, c1)} and {eq2(a2, b2, c2)}.', f'x = {fn(x)}, y = {fn(y)}',
             f'Multiply to make the coefficients of one variable equal, subtract, solve: x = {fn(x)}, y = {fn(y)} (3 marks).',
             [f'x = {fn(y)}, y = {fn(x)}', f'x = {fn(x)}, y = {fn(-y)}' if y else f'x = {fn(x)}, y = 1', f'x = {fn(x + 1)}, y = {fn(y + 1)}'])


def c3s4_recip(r):
    u, v = r.choice([2, 3, 4, 5, Fr(1, 2), Fr(1, 3)]), r.choice([2, 3, 4, 5, Fr(1, 2)])
    a1, b1, a2, b2 = r.randint(1, 4), r.randint(1, 4), r.randint(1, 4), nz(r, 1, 4)
    if a1 * b2 - a2 * b1 == 0:
        raise ValueError
    # equations a1/x + b1/y = c1 with 1/x = p, 1/y = q
    p, q = 1 / Fr(u), 1 / Fr(v)
    c1, c2 = a1 * p + b1 * q, a2 * p + b2 * q
    return Q(f'Solve: {a1}/x + {b1}/y = {fn(c1)} and {a2}/x {"+" if b2 > 0 else "−"} {abs(b2)}/y = {fn(c2)} (x, y ≠ 0).', f'x = {fn(Fr(u))}, y = {fn(Fr(v))}',
             f'Put p = 1/x, q = 1/y: {term(a1, "p", first=True)}{term(b1, "q")} = {fn(c1)}, {term(a2, "p", first=True)}{term(b2, "q")} = {fn(c2)} ⇒ p = {fn(p)}, q = {fn(q)} ⇒ x = {fn(Fr(u))}, y = {fn(Fr(v))} (4 marks).')


def c3s4_explain(r):
    return xbank([
        ('Explain when the elimination method is more convenient than substitution.', 'When neither variable has coefficient 1 but the coefficients can be easily matched by multiplying.', '2 marks.'),
        ('In the elimination method, explain what it means if both variables are eliminated and you get a false statement such as 0 = 5.', 'The pair has no solution (inconsistent, parallel lines).', '2 marks.'),
        ('In the elimination method, what does a true statement such as 0 = 0 after eliminating both variables mean?', 'Infinitely many solutions (coincident lines).', '2 marks.'),
    ])(r)


def c3s4_ar(r):
    a1, b1, c1, a2, b2, c2, x, y = lin_pair(r)
    return arbank([
        (f'x = {fn(x)}, y = {fn(y)} is the solution of {eq2(a1, b1, c1)} and {eq2(a2, b2, c2)}.', 'A solution of a pair must satisfy both equations.', 'a', 'Substitution checks both; R explains A.'),
        ('Elimination can only be used when the coefficients of x are equal.', 'In elimination we make the coefficients of one variable numerically equal.', 'd', 'We can multiply first; A false, R true.'),
    ])(r)


def c3s3_ar(r):
    return arbank([
        ('In x + 2y = 7, 3x − y = 7, substitution is convenient.', 'The first equation gives x = 7 − 2y directly.', 'a', 'A coefficient of 1 makes substitution easy.'),
        ('Substitution and elimination can give different solutions for the same pair.', 'Both methods transform the equations without changing their solutions.', 'd', 'A false, R true.'),
    ])(r)


def c3s3_explain(r):
    return xbank([
        ('Explain the steps of the substitution method for solving a pair of linear equations.', 'Express one variable in terms of the other from one equation, substitute in the other, solve, then back-substitute.', '2 marks.'),
        ('While solving by substitution, a student gets 7 = 7. What does this tell you about the pair?', 'The equations are dependent: infinitely many solutions.', '2 marks.'),
    ])(r)


# st5 word problems

def c3s5_ages(r):
    who1, who2 = two_names(r)
    y = r.randint(5, 16)
    k = r.choice([4, 5, 6, 8, 10])
    m = r.choice([2, 3])
    x = m * (y + k) - k
    if not 22 <= x - y <= 40:
        raise ValueError
    s = x + y
    return Q(f'The sum of the ages of {who1}\'s mother and {who1} is {s} years. After {k} years, the mother will be {m} times as old as {who1}. Find their present ages.',
             f'Mother {x} years, {who1} {y} years', f'x + y = {s}; x + {k} = {m}(y + {k}) ⇒ solve: x = {x}, y = {y} (3 marks).')


def c3s5_digits(r):
    a, b = r.randint(1, 9), r.randint(1, 9)
    if a == b:
        raise ValueError
    n, rev = 10 * a + b, 10 * b + a
    return Q(f'The sum of the digits of a two-digit number is {a + b}. The number obtained by reversing the digits exceeds the original by {rev - n}.'.replace('exceeds the original by -', 'is less than the original by ') if rev > n else
             f'The sum of the digits of a two-digit number is {a + b}. The number obtained by reversing the digits is {n - rev} less than the original number. Find the number.', str(n),
             f'Let tens digit x, units y: x + y = {a + b}; (10x + y) − (10y + x) = {n - rev} ⇒ 9(x − y) = {n - rev} ⇒ x − y = {a - b}; x = {a}, y = {b}; number {n} (3 marks).') if rev < n else \
        Q(f'The sum of the digits of a two-digit number is {a + b}. The number obtained by reversing the digits exceeds the original number by {rev - n}. Find the number.', str(n),
          f'x + y = {a + b}; 9(y − x) = {rev - n} ⇒ y − x = {b - a}; x = {a}, y = {b}; number {n} (3 marks).')


def c3s5_cost(r):
    who = name(r)
    p, q = r.randint(10, 60), r.randint(5, 40)
    a, b, c, d = r.randint(1, 5), r.randint(1, 5), r.randint(1, 5), r.randint(1, 5)
    if a * d == b * c:
        raise ValueError
    it = r.choice([('bats', 'balls'), ('notebooks', 'pens'), ('kg of apples', 'kg of grapes'), ('chairs', 'stools')])
    return Q(f'{who} buys {a} {it[0]} and {b} {it[1]} for ₹{a * p * 10 + b * q * 10}; another customer buys {c} {it[0]} and {d} {it[1]} for ₹{c * p * 10 + d * q * 10}. Find the cost of one of each.',
             f'{it[0].split()[-1].rstrip("s") if not it[0].startswith("kg") else "1 kg of apples"}: ₹{p * 10}, {it[1].split()[-1].rstrip("s") if not it[1].startswith("kg") else "1 kg of grapes"}: ₹{q * 10}',
             f'{term(a, "x", first=True)}{term(b, "y")} = {a * p * 10 + b * q * 10}, {term(c, "x", first=True)}{term(d, "y")} = {c * p * 10 + d * q * 10}; solve: x = {p * 10}, y = {q * 10} (3 marks).')


def c3s5_boat(r):
    u, v = r.choice([(10, 2), (12, 3), (15, 5), (18, 2), (8, 2), (11, 1)])
    t1, t2 = r.choice([2, 3, 4]), r.choice([2, 3, 4, 5])
    return Q(f'A boat goes {(u - v) * t1} km upstream in {t1} hours and {(u + v) * t2} km downstream in {t2} hours. Find the speed of the boat in still water and the speed of the stream.',
             f'Boat {u} km/h, stream {v} km/h', f'u − v = {u - v}, u + v = {u + v} ⇒ u = {u}, v = {v} (3 marks).')


def c3s5_fraction(r):
    n, d = r.randint(2, 9), r.randint(5, 15)
    if n >= d or math.gcd(n, d) != 1:
        raise ValueError
    a, b = r.randint(1, 3), r.randint(1, 3)
    f1, f2 = Fr(n + a, d + a), Fr(n - b, d - b) if d - b != 0 else None
    if f2 is None or n - b <= 0:
        raise ValueError
    return Q(f'A fraction becomes {fn(f1)} if {a} is added to both the numerator and the denominator. If {b} is subtracted from both, it becomes {fn(f2)}. Find the fraction.', f'{n}/{d}',
             f'(x + {a})/(y + {a}) = {fn(f1)}, (x − {b})/(y − {b}) = {fn(f2)}; cross-multiply and solve: x = {n}, y = {d} (4 marks).')


def c3s5_case(r):
    f, k = r.choice([(40, 15), (50, 12), (30, 10), (60, 20)])
    d1, d2 = r.randint(5, 12), r.randint(13, 25)
    return Q((f'A taxi in Jaipur charges a fixed amount plus a charge per km. A journey of {d1} km costs ₹{f + k * d1} and a journey of {d2} km costs ₹{f + k * d2}. '
              f'(i) Form the pair of linear equations. (ii) Find the fixed charge and the charge per km. (iii) How much does a {d1 + d2} km journey cost? (iv) Which method did you use and why?'),
             f'(i) x + {d1}y = {f + k * d1}, x + {d2}y = {f + k * d2} (ii) fixed ₹{f}, ₹{k} per km (iii) ₹{f + k * (d1 + d2)} (iv) elimination: subtracting removes x at once', '1 mark each part.')


def c3s5_rect(r):
    l, b = r.randint(8, 30), r.randint(5, 20)
    a1, b1 = r.randint(1, 4), r.randint(1, 4)
    a2, b2 = r.randint(1, 4), r.randint(1, 4)
    A0 = l * b
    dA1 = (l - a1) * (b + b1) - A0
    dA2 = (l + a2) * (b + b2) - A0
    return Q(f'The area of a rectangle changes by {fn(dA1)} square units if its length is reduced by {a1} unit{"s" if a1 > 1 else ""} and its breadth increased by {b1} unit{"s" if b1 > 1 else ""}. If the length is increased by {a2} unit{"s" if a2 > 1 else ""} and the breadth by {b2} unit{"s" if b2 > 1 else ""}, the area increases by {dA2} square units. Find the length and breadth.'.replace('changes by −', 'decreases by ').replace('changes by ', 'increases by '),
             f'Length {l}, breadth {b}', f'(x − {a1})(y + {b1}) = xy {signed(dA1)} and (x + {a2})(y + {b2}) = xy + {dA2} give two linear equations in x and y; solve (5 marks).') if dA1 != 0 and (b1 * a2 + a1 * b2) != 0 else _raise()


# ---------------- ch04 Quadratic equations ----------------

def c4s1_check(r):
    return mcqbank([
        ('Which of the following is a quadratic equation?', '(x + 1)² = 2(x − 3)', ['x(x + 1) + 8 = (x + 2)(x − 2)', 'x² + 3x + 1 = (x − 2)²', '(x + 2)³ = x³ − 4'], 'Expand: x² + 2x + 1 = 2x − 6 ⇒ x² + 7 = 0 (degree 2).'),
        ('Which of the following is NOT a quadratic equation?', 'x(x + 1) + 8 = (x + 2)(x − 2)', ['(x − 2)² + 1 = 2x − 3', 'x(2x + 3) = x² + 1', '(x + 1)² = 2(x − 3)'], 'x² cancels: x + 8 = −4 is linear.'),
        ('The standard form of a quadratic equation is …', 'ax² + bx + c = 0, a ≠ 0', ['ax + b = 0', 'ax² + bx + c = 0, a = 0', 'ax³ + bx² + c = 0'], 'Definition.'),
    ])(r)


def c4s1_form(r):
    who = name(r)
    b = r.randint(3, 15)
    k = r.randint(1, 6)
    A = b * (b + k)
    ctx = r.choice([('rectangular plot', 'length', 'breadth', 'm', 'm²'), ('rectangular hall', 'length', 'breadth', 'm', 'm²')])
    return Q(f'The area of a {ctx[0]} is {A} {ctx[4]}. Its {ctx[1]} is {k} {ctx[3]} more than its {ctx[2]}. Represent this as a quadratic equation in the breadth x.', f'x² + {k}x − {A} = 0',
             f'x(x + {k}) = {A} ⇒ x² + {k}x − {A} = 0.', [f'x² − {k}x − {A} = 0', f'x² + {k}x + {A} = 0', f'2x + {k} = {A}'])


def c4s1_word(r):
    n = r.randint(5, 20)
    return Q(f'The product of two consecutive positive integers is {n * (n + 1)}. Write the quadratic equation satisfied by the smaller integer x.', f'x² + x − {n * (n + 1)} = 0',
             f'x(x + 1) = {n * (n + 1)}.', [f'x² − x − {n * (n + 1)} = 0', f'x² + 2x − {n * (n + 1)} = 0', f'x² + x + {n * (n + 1)} = 0'])


def c4s1_reduce(r):
    a, b, c = r.randint(1, 4), nz(r, 1, 6), nz(r, 1, 9)
    d = nz(r, 1, 6)
    # (x + a)(x + b)... give (x + a)² = something
    return Q(
        f'Is (x {signed(a)})² = {lin(2 * a + d, a * a + c)} a quadratic equation? Reduce it to standard form.', f'Yes: {poly([1, -d, -c])} = 0',
        f'Expand: x² + {2 * a}x + {a * a} = {lin(2 * a + d, a * a + c)} ⇒ {poly([1, -d, -c])} = 0, degree 2.')


def c4s1_explain(r):
    return xbank([
        ('Explain why (x + 2)² = x² + 3 is not a quadratic equation even though it contains x².', 'Expanding, the x² terms cancel: 4x + 1 = 0, which is linear.', '2 marks.'),
        ('Why must a ≠ 0 in ax² + bx + c = 0?', 'If a = 0 the equation becomes linear (degree 1).', '2 marks.'),
    ])(r)


def c4s1_ar(r):
    return arbank([
        ('x(x − 3) = x² + 5 is not a quadratic equation.', 'After simplifying, the x² terms cancel and the equation becomes −3x = 5.', 'a', 'R explains A.'),
        ('(x − 1)² = 2x + 1 is a quadratic equation.', 'After simplifying, it is x² − 4x = 0, of degree 2.', 'a', 'R explains A.'),
    ])(r)


def c4s1_case(r):
    s = r.randint(10, 25)
    t = r.randint(2, 6)
    return Q((f'A train travels {s * t * 10} km at a uniform speed. If the speed were 10 km/h more, it would take 1 hour less. '
              f'(i) Taking the speed as x km/h, write the time taken. (ii) Write the time at the higher speed. (iii) Form the equation and reduce it to standard form. (iv) Is the equation quadratic? Why?'),
             f'(i) {s * t * 10}/x h (ii) {s * t * 10}/(x + 10) h (iii) {s * t * 10}/x − {s * t * 10}/(x + 10) = 1 ⇒ x² + 10x − {s * t * 100} = 0 (iv) yes, degree 2', '1 mark each part.')


# st2 factorisation

def c4s2_solve(r):
    a = r.choice([1, 1, 2, 3, 2])
    p = Fr(nz(r, 1, 9), r.choice([1, a]))
    q = Fr(nz(r, 1, 9))
    if p == q:
        raise ValueError
    co = coeffs_from_roots(a, p, q)
    if any(Fr(x).denominator != 1 for x in co):
        raise ValueError
    co = [int(x) for x in co]
    if co[1] == 0:
        raise ValueError
    return Q(f'Find the roots of {poly(co)} = 0 by factorisation.', f'x = {fn(min(p, q))} or x = {fn(max(p, q))}',
             f'Split the middle term (product of a and c = {fn(co[0] * co[2])}); factorise and set each factor to 0: x = {fn(p)}, {fn(q)}.',
             [f'x = {fn(-min(p, q))} or x = {fn(-max(p, q))}', f'x = {fn(min(p, q))} or x = {fn(-max(p, q))}', f'x = {fn(p * q)} or x = {fn(p + q)}'])


def c4s2_mcq(r):
    p, q = r.sample([n for n in range(-9, 10) if n], 2)
    return mcq(f'The roots of {poly([1, -(p + q), p * q])} = 0 are …', f'{fn(min(p, q))} and {fn(max(p, q))}',
               [f'{fn(-max(p, q))} and {fn(-min(p, q))}', f'{fn(min(p, q))} and {fn(-max(p, q))}' if min(p, q) != -max(p, q) else f'{fn(p * q)} and 1', f'{fn(p + q)} and {fn(p * q)}'],
               '(x − α)(x − β) = 0.', r)


def c4s2_rational(r):
    a = r.randint(2, 12)
    return Q(f'Solve: x − {a * a}/x = 0 (x ≠ 0)... and also solve x + 1/x = {fn(Fr(a * a + 1, a))}.'.replace('... ', ', '),
             f'x = ±{a}; x = {a} or x = {fn(Fr(1, a))}', f'x² = {a * a}; for the second, multiply by {a}x: {a}x² − {a * a + 1}x + {a} = 0 ⇒ (x − {a})({a}x − 1) = 0 (4 marks).')


def c4s2_explain(r):
    return xbank([
        ('Explain why, if (x − 3)(x + 5) = 0, then x = 3 or x = −5.', 'If a product of two numbers is 0, at least one of them is 0.', '2 marks.'),
        ('A student divides both sides of x² = 5x by x and writes x = 5 as the only root. Explain the error.', 'Dividing by x loses the root x = 0; correct: x(x − 5) = 0 ⇒ x = 0 or 5.', '2 marks.'),
    ])(r)


def c4s2_ar(r):
    p, q = r.sample(range(1, 9), 2)
    return arbank([
        (f'The roots of x² − {p + q}x + {p * q} = 0 are {p} and {q}.', f'x² − {p + q}x + {p * q} = (x − {p})(x − {q}).', 'a', 'R explains A.'),
        (f'x = {p} is a root of x² − {p * p} = 0 and is the only root.', 'A quadratic equation has at most two roots.', 'd', f'x = −{p} is also a root; A false, R true.'),
    ])(r)


def c4s2_case(r):
    b = r.randint(5, 20)
    k = r.randint(2, 8)
    return Q((f'A rectangular garden in a society in Noida is {k} m longer than it is wide and has area {b * (b + k)} m². '
              f'(i) Form the quadratic equation in the width x. (ii) Solve it by factorisation. (iii) Why is one root rejected? (iv) Find the perimeter of the garden.'),
             f'(i) x² + {k}x − {b * (b + k)} = 0 (ii) x = {b} or x = −{b + k} (iii) a width cannot be negative (iv) {2 * (2 * b + k)} m', '1 mark each part.')


def c4s2_hard(r):
    a, b = r.randint(1, 6), r.randint(1, 6)
    if a == b:
        raise ValueError
    return Q(f'Solve for x: x² − {a + b}x + {a * b} = 0, and hence solve y⁴ − {a + b}y² + {a * b} = 0 for real y.',
             f'x = {a}, {b}; y = ±{rad(a)}, ±{rad(b)}', f'Factorise (x − {a})(x − {b}) = 0; put x = y² (4 marks).')


# st3 formula and discriminant

def c4s3_disc(r):
    a, b, c = nz(r, 1, 5), nz(r, 0, 9), nz(r, 1, 9)
    D = b * b - 4 * a * c
    nat = 'two distinct real roots' if D > 0 else ('two equal real roots' if D == 0 else 'no real roots')
    return Q(f'Find the discriminant of {poly([a, b, c])} = 0 and state the nature of its roots.', f'D = {fn(D)}; {nat}', f'D = b² − 4ac = {b * b} − {bracket(4 * a * c)} = {fn(D)}.',
             [f'D = {fn(b * b + 4 * a * c)}; ' + ('two distinct real roots' if b * b + 4 * a * c > 0 else 'no real roots'), f'D = {fn(D)}; ' + ('no real roots' if D > 0 else 'two distinct real roots'), f'D = {fn(b - 4 * a * c)}; two equal real roots'])


def c4s3_formula(r):
    a = r.randint(1, 3)
    b = nz(r, 1, 9)
    c = nz(r, 1, 9)
    D = b * b - 4 * a * c
    if D <= 0 or is_sq(D):
        raise ValueError
    s = rad(D)
    k = max(q for q in range(1, math.isqrt(D) + 1) if D % (q * q) == 0)
    m = D // (k * k)
    g = math.gcd(math.gcd(abs(b), k), 2 * a)
    root = f'{"" if k // g == 1 else k // g}√{m}'
    simp = f'{fn(-b // g)} ± {root}' if 2 * a // g == 1 else f'({fn(-b // g)} ± {root})/{2 * a // g}'
    return Q(f'Solve {poly([a, b, c])} = 0 using the quadratic formula.', f'x = {simp}',
             f'D = {D}; x = (−b ± √D)/2a = ({fn(-b)} ± √{D})/{2 * a}' + (f' = {simp}' if simp != f'({fn(-b)} ± √{D})/{2 * a}' else '') + ' (3 marks).',
             [f'x = ({fn(b)} ± {s})/{2 * a}', f'x = ({fn(-b)} ± {s})/{a}' if a > 1 else f'x = {fn(-b)} ± {s}', f'x = ({fn(-b)} ± {rad(D + 4 * a)})/{2 * a}'])


def c4s3_k(r):
    a = r.randint(1, 4)
    m = r.randint(1, 6)
    # equal roots of a x² + k x + c: k² = 4ac; choose c = a m² -> k = ±2am
    c = a * m * m
    return Q(f'Find the values of k for which {a if a > 1 else ""}x² + kx + {c} = 0 has two equal roots.', f'k = ±{2 * a * m}',
             f'D = k² − 4 × {a} × {c} = 0 ⇒ k² = {4 * a * c} ⇒ k = ±{2 * a * m} (3 marks).', [f'k = {2 * a * m} only', f'k = ±{a * m}', f'k = ±{4 * a * c}'])


def c4s3_mcq(r):
    return mcqbank([
        ('If the discriminant of a quadratic equation is negative, the equation has …', 'no real roots', ['two equal real roots', 'two distinct real roots', 'one real root'], 'D < 0.'),
        ('The roots of ax² + bx + c = 0 are given by …', 'x = (−b ± √(b² − 4ac))/2a', ['x = (b ± √(b² − 4ac))/2a', 'x = (−b ± √(b² + 4ac))/2a', 'x = −b/2a only'], 'Quadratic formula.'),
        ('The equation x² − 4x + 4 = 0 has …', 'two equal real roots', ['no real roots', 'two distinct real roots', 'three roots'], 'D = 16 − 16 = 0.'),
        ('The discriminant of 2x² − 4x + 3 = 0 is …', '−8', ['8', '40', '−40'], '16 − 24.'),
    ])(r)


def c4s3_explain(r):
    return xbank([
        ('Explain why a quadratic equation with D = 0 has two equal roots.', 'x = (−b ± 0)/2a gives the same value −b/2a twice.', '2 marks.'),
        ('Explain why x² + 1 = 0 has no real roots, using the discriminant.', 'D = 0 − 4 = −4 < 0, and the square root of a negative number is not real.', '2 marks.'),
        ('Derive the quadratic formula by completing the square (outline the steps).', 'Divide by a, move c/a, add (b/2a)² to both sides, take square roots: x = (−b ± √(b² − 4ac))/2a.', '3 marks.'),
    ])(r)


def c4s3_ar(r):
    a, c = r.randint(1, 5), r.randint(1, 5)
    return arbank([
        (f'{term(a, "x", first=True, power=2)} + {c} = 0 has no real roots.', 'Its discriminant 0 − 4ac is negative.', 'a', 'R explains A.'),
        ('x² − 2x + 1 = 0 has two distinct real roots.', 'Its discriminant is 0.', 'd', 'D = 0 gives equal roots; A false, R true.'),
        ('If a and c have opposite signs, ax² + bx + c = 0 has real roots.', 'Then −4ac > 0, so D = b² − 4ac > 0.', 'a', 'R explains A.'),
    ])(r)


def c4s3_case(r):
    who = name(r)
    k = r.choice([20, 24, 30, 36])
    return Q((f'{who} wants to make a rectangular garden with perimeter {2 * k} m. (i) If the length is x m, write the breadth. (ii) Can the area be {k * k // 4 + 4} m²? Use the discriminant. '
              f'(iii) Can the area be {k * k // 4} m²? Find the dimensions. (iv) What is the largest possible area?'),
             f'(i) ({k} − x) m (ii) x² − {k}x + {k * k // 4 + 4} = 0: D = {k * k - 4 * (k * k // 4 + 4)} < 0, so no (iii) yes: D = 0, a square of side {k // 2} m (iv) {k * k // 4} m²',
             '1 mark each part.')


# st4 word problems

def c4s4_consec(r):
    n = r.randint(5, 25)
    kind = r.choice(['squares', 'product'])
    if kind == 'squares':
        return Q(f'The sum of the squares of two consecutive positive integers is {n * n + (n + 1) ** 2}. Find the integers.', f'{n} and {n + 1}',
                 f'x² + (x + 1)² = {n * n + (n + 1) ** 2} ⇒ 2x² + 2x − {n * n + (n + 1) ** 2 - 1} = 0 ⇒ x = {n} (reject the negative root) (3 marks).')
    return Q(f'Find two consecutive odd positive integers whose product is {(2 * n - 1) * (2 * n + 1)}.', f'{2 * n - 1} and {2 * n + 1}',
             f'x(x + 2) = {(2 * n - 1) * (2 * n + 1)} ⇒ x² + 2x − {(2 * n - 1) * (2 * n + 1)} = 0 ⇒ x = {2 * n - 1} (3 marks).')


def c4s4_speed(r):
    while True:
        v = r.choice([30, 40, 45, 50, 60, 75, 80])
        d = r.choice([120, 150, 180, 200, 240, 300, 360, 400, 450, 480])
        k = r.choice([5, 10, 15, 20])
        t = Fr(d, v) - Fr(d, v + k)
        if t.denominator in (1, 2, 4) and t > 0:
            break
    return Q(f'A train travels {d} km at a uniform speed. If the speed had been {k} km/h more, it would have taken {fn(t)} hour{"s" if t != 1 else ""} less. Find the speed of the train.', f'{v} km/h',
             f'{d}/x − {d}/(x + {k}) = {fn(t)} ⇒ x² + {k}x − {fn(d * k / t)} = 0 ⇒ x = {v} (reject the negative root) (4 marks).')


def c4s4_age(r):
    who = name(r)
    x = r.randint(10, 30)
    a, b = r.randint(2, 6), r.randint(2, 6)
    p = (x - a) * (x + b)
    return Q(f'The product of {who}\'s age {a} years ago and {b} years from now is {p}. Find {who}\'s present age.', f'{x} years',
             f'(x − {a})(x + {b}) = {p} ⇒ {poly([1, b - a, -(a * b + p)])} = 0 ⇒ x = {x} (the other root is negative/inadmissible) (3 marks).')


def c4s4_rect(r):
    b = r.randint(5, 30)
    k = r.randint(1, 10)
    m = r.choice([2, 1])
    l = m * b + k
    return Q(f'The length of a rectangular field is {k} m more than {"twice " if m == 2 else ""}its breadth. Its area is {l * b} m². Find its length and breadth.', f'Length {l} m, breadth {b} m',
             f'x({term(m, "x", first=True)} + {k}) = {l * b} ⇒ {term(m, "x", first=True, power=2)} + {k}x − {l * b} = 0 ⇒ x = {b} (3 marks).')


def c4s4_ar(r):
    return arbank([
        ('In a word problem, a negative root for the length of a side is rejected.', 'A length cannot be negative.', 'a', 'R explains A.'),
        ('If the product of two consecutive integers is 56, the integers must be 7 and 8.', 'x(x + 1) = 56 has roots 7 and −8.', 'd', 'They can also be −8 and −7; A false, R true.'),
    ])(r)


def c4s4_explain(r):
    return xbank([
        ('In the problem "a train travels 360 km; 4 km/h faster it would take 1 hour less", explain why the equation is 360/x − 360/(x + 4) = 1.', 'Time = distance ÷ speed; the slower time minus the faster time is 1 hour.', '2 marks.'),
        ('Explain why both roots of a quadratic equation may be valid in a problem about numbers but not about ages.', 'Numbers can be negative; ages cannot.', '2 marks.'),
    ])(r)


def c4s4_case(r):
    n = r.randint(10, 30)
    c = r.randint(5, 20)
    total = n * (c + n)
    return Q((f'A cottage industry in Kutch makes pottery. On one day, the cost of production of each article (in ₹) was {c} more than the number of articles made, and the total cost was ₹{total}. '
              f'(i) Form the quadratic equation in x, the number of articles. (ii) Find the discriminant. (iii) Find the number of articles made. (iv) Find the cost of each article.'),
             f'(i) x² + {c}x − {total} = 0 (ii) {c * c + 4 * total} (iii) {n} (iv) ₹{n + c}', '1 mark each part.')


# ---------------- ch05 Arithmetic progressions ----------------

def apv(r):
    a = r.randint(-20, 30)
    d = nz(r, 1, 9)
    return a, d


def c5s1_is_ap(r):
    kind = r.randint(0, 3)
    if kind == 0:
        a, d = apv(r)
        seq, ok = [a + i * d for i in range(4)], True
    elif kind == 1:
        a = r.randint(1, 5)
        seq, ok = [a * 2 ** i for i in range(4)], False
    elif kind == 2:
        a = r.randint(1, 6)
        seq, ok = [(a + i) ** 2 for i in range(4)], False
    else:
        a = r.randint(1, 9)
        p = r.choice([2, 3, 5])
        seq, ok = None, True
        txt = f'√{p}, √{4 * p}, √{9 * p}, √{16 * p}'
        return Q(f'Is {txt}, … an AP? If so, find the common difference.', f'Yes; d = √{p}', f'They are √{p}, 2√{p}, 3√{p}, 4√{p}: d = √{p}.', ['No', f'Yes; d = {p}', f'Yes; d = √{3 * p}'])
    return Q(f'Is {", ".join(map(fn, seq))}, … an AP? If so, find the common difference.', f'Yes; d = {fn(seq[1] - seq[0])}' if ok else 'No',
             'Check whether aₖ₊₁ − aₖ is constant.' + ('' if ok else f' Differences {fn(seq[1] - seq[0])}, {fn(seq[2] - seq[1])} differ.'), ['No' if ok else f'Yes; d = {fn(seq[1] - seq[0])}', f'Yes; d = {fn(seq[0])}', f'Yes; d = {fn(seq[2] - seq[0])}'])


def c5s1_next(r):
    a, d = apv(r)
    return Q(f'Write the next two terms of the AP {", ".join(fn(a + i * d) for i in range(4))}, …', f'{fn(a + 4 * d)}, {fn(a + 5 * d)}', f'd = {fn(d)}.',
             [f'{fn(a + 4 * d)}, {fn(a + 6 * d)}', f'{fn(a + 3 * d + 1)}, {fn(a + 3 * d + 2)}', f'{fn(a + 5 * d)}, {fn(a + 6 * d)}'])


def c5s1_first_terms(r):
    a = Fr(r.randint(-10, 10), r.choice([1, 2]))
    d = Fr(nz(r, 1, 6), r.choice([1, 2, 3]))
    return Q(f'Write the first four terms of the AP whose first term is {fn(a)} and common difference is {fn(d)}.', ', '.join(fn(a + i * d) for i in range(4)), 'aₙ₊₁ = aₙ + d.',
             [', '.join(fn(a * (i + 1)) for i in range(4)), ', '.join(fn(a + i * d + d) for i in range(4)), ', '.join(fn(a - i * d) for i in range(4))])


def c5s1_explain(r):
    return xbank([
        ('Explain why the list 1, 1, 1, 1, … is an AP.', 'The difference between consecutive terms is always 0.', '2 marks.'),
        ('A taxi fare is ₹30 for the first km and ₹12 for each additional km. Explain why the fares for 1, 2, 3, … km form an AP.', 'Each fare is ₹12 more than the previous one: 30, 42, 54, …', '2 marks.'),
        ('The amount in a bank account with compound interest each year: does it form an AP? Explain.', 'No; it is multiplied by a constant each year, so the differences are not constant.', '2 marks.'),
    ])(r)


def c5s1_ar(r):
    a, d = apv(r)
    return arbank([
        (f'{fn(a)}, {fn(a + d)}, {fn(a + 2 * d)}, … is an AP with common difference {fn(d)}.', 'In an AP, each term after the first is obtained by adding a fixed number to the preceding term.', 'a', 'R explains A.'),
        ('The squares 1, 4, 9, 16, … form an AP.', 'Each term is a perfect square.', 'd', 'Differences 3, 5, 7 not constant; A false, R true.'),
        ('In an AP, d can be zero or negative.', 'd = aₙ₊₁ − aₙ can be any real number.', 'a', 'R explains A.'),
    ])(r)


def c5s1_case(r):
    a, d = r.choice([(150, 50), (200, 25), (100, 20), (500, 100)])
    return Q((f'A savings scheme for students: in week 1 Riya saves ₹{a}, and each week she saves ₹{d} more than the week before. '
              f'(i) Write the savings for the first 4 weeks. (ii) Is this an AP? Give a and d. (iii) How much does she save in week 10? (iv) If instead she doubled her savings each week, would it still be an AP?'),
             f'(i) {a}, {a + d}, {a + 2 * d}, {a + 3 * d} (ii) yes; a = {a}, d = {d} (iii) ₹{a + 9 * d} (iv) no; differences would not be constant', '1 mark each part.')


# st2 nth term — reuse class 9 AP families plus new ones

def c5s2_last(r):
    a, d = apv(r)
    n = r.randint(15, 40)
    l = a + (n - 1) * d
    k = r.randint(3, 10)
    return Q(f'Find the {ordinal(k)} term from the last term of the AP {fn(a)}, {fn(a + d)}, {fn(a + 2 * d)}, …, {fn(l)}.', fn(l - (k - 1) * d),
             f'Reverse the AP: first term {fn(l)}, d = {fn(-d)}; term = {fn(l)} + {k - 1} × {bracket(-d)} = {fn(l - (k - 1) * d)}.', num_distractors(l - (k - 1) * d, a + (k - 1) * d, l - k * d))


def c5s2_count(r):
    a, d = r.randint(10, 100), r.randint(2, 9)
    n = r.randint(15, 60)
    l = a + (n - 1) * d
    return Q(f'How many terms are there in the AP {a}, {a + d}, {a + 2 * d}, …, {l}?', str(n), f'{l} = {a} + (n − 1){d} ⇒ n = {n}.', num_distractors(n, n - 1, n + 1, (l - a) // d))


def c5s2_multiples(r):
    k = r.choice([3, 4, 6, 7, 9, 11, 13])
    lo, hi = r.choice([(10, 100), (100, 999), (10, 250), (50, 500)])
    first = ((lo + k - 1) // k) * k
    last = (hi // k) * k
    n = (last - first) // k + 1
    return Q(f'How many {"three" if (lo, hi) == (100, 999) else ""}{"-digit " if (lo, hi) == (100, 999) else ""}numbers {"between " + str(lo) + " and " + str(hi) + " " if (lo, hi) != (100, 999) else ""}are divisible by {k}?'.replace('  ', ' '), str(n),
             f'AP {first}, {first + k}, …, {last}; n = ({last} − {first})/{k} + 1 = {n}.', num_distractors(n, n - 1, n + 1, (hi - lo) // k))


def c5s2_three(r):
    a, d = r.randint(-5, 10), r.randint(1, 6)
    s, p = 3 * (a + d), (a) * (a + d) * (a + 2 * d)
    return Q(f'Three numbers in AP have sum {s} and product {p}. Find the numbers.', f'{a}, {a + d}, {a + 2 * d}',
             f'Take a − d, a, a + d: 3a = {s} ⇒ a = {a + d}; (a² − d²)a = {p} ⇒ d = ±{d}; numbers {a}, {a + d}, {a + 2 * d} (or in reverse) (4 marks).') if p != 0 else _raise()


def c5s2_explain(r):
    a, d = apv(r)
    return Q(
             f'Is 0 a term of the AP {fn(a)}, {fn(a + d)}, {fn(a + 2 * d)}, …? Explain.', 'Yes' if (-a) % d == 0 and (-a) // d >= 0 else 'No',
             f'0 = {fn(a)} + (n − 1){bracket(d)} ⇒ n − 1 = {fn(Fr(-a, d))}; it is a term only if this is a whole number.')


def c5s2_ar(r):
    a, d = apv(r)
    n = r.randint(10, 30)
    return arbank([
        (f'The {ordinal(n)} term of the AP {fn(a)}, {fn(a + d)}, … is {fn(a + (n - 1) * d)}.', 'aₙ = a + (n − 1)d.', 'a', 'R explains A.'),
        (f'The {ordinal(n)} term of the AP {fn(a)}, {fn(a + d)}, … is {fn(a + n * d)}.', 'aₙ = a + (n − 1)d.', 'd', f'aₙ = {fn(a + (n - 1) * d)}; A false, R true.'),
    ])(r)


def c5s2_case(r):
    a, d = r.choice([(1000, 500), (2000, 250), (500, 100), (1200, 300)])
    target = a + d * r.randint(10, 25)
    return Q((f'A company in Hyderabad pays a monthly bonus that starts at ₹{a} in the first month and increases by ₹{d} each month. '
              f'(i) Write the first three bonuses. (ii) Find the bonus in the 12th month. (iii) In which month will the bonus be ₹{target}? (iv) Write the general term aₙ.'),
             f'(i) {a}, {a + d}, {a + 2 * d} (ii) ₹{a + 11 * d} (iii) month {(target - a) // d + 1} (iv) aₙ = {a} + (n − 1){d}', '1 mark each part.')


# st3 sum

def c5s3_sum(r):
    a, d = apv(r)
    n = r.randint(10, 30)
    S = n * (2 * a + (n - 1) * d) // 2
    return Q(f'Find the sum of the first {n} terms of the AP {fn(a)}, {fn(a + d)}, {fn(a + 2 * d)}, …', fn(S),
             f'Sₙ = n/2 [2a + (n − 1)d] = {n}/2 [{fn(2 * a)} + {n - 1} × {bracket(d)}] = {fn(S)}.', num_distractors(S, n * (2 * a + n * d) // 2, n * (a + (n - 1) * d), S + a))


def c5s3_mcq(r):
    n = r.randint(10, 100)
    return mcq(f'The sum of the first {n} natural numbers is …', str(n * (n + 1) // 2), [str(n * n), str(n * (n - 1) // 2), str(n * (n + 1))], 'Sₙ = n(n + 1)/2.', r)


def c5s3_first_last(r):
    a, d = apv(r)
    n = r.randint(10, 40)
    l = a + (n - 1) * d
    return Q(f'An AP has {n} terms; its first term is {fn(a)} and its last term is {fn(l)}. Find the sum of all its terms.', fn(Fr(n * (a + l), 2)),
             f'Sₙ = n/2 (a + l) = {n}/2 ({fn(a)} + {bracket(l)}) = {fn(Fr(n * (a + l), 2))}.', num_distractors(float(Fr(n * (a + l), 2)), n * (a + l), n * l))


def c5s3_find_n(r):
    a, d = r.randint(1, 20), r.randint(1, 8)
    n = r.randint(6, 25)
    S = n * (2 * a + (n - 1) * d) // 2
    return Q(f'How many terms of the AP {a}, {a + d}, {a + 2 * d}, … must be taken to give a sum of {S}?', str(n),
             f'n/2 [{2 * a} + (n − 1){d}] = {S} ⇒ {poly([d, 2 * a - d, -2 * S], "n")} = 0 ⇒ n = {n} (reject the other root) (4 marks).')


def c5s3_sn(r):
    p, q = r.randint(1, 4), nz(r, 1, 9)
    n = r.randint(5, 20)
    a1 = p + q
    d = 2 * p
    return Q(f'The sum of the first n terms of an AP is Sₙ = {term(p, "n", first=True, power=2)}{term(q, "n")}. Find the first term, the common difference and the {ordinal(n)} term.',
             f'a = {fn(a1)}, d = {fn(d)}, a{sub(n)} = {fn(a1 + (n - 1) * d)}', f'a₁ = S₁ = {fn(a1)}; a₂ = S₂ − S₁ = {fn(a1 + d)}; d = {fn(d)}; aₙ = Sₙ − Sₙ₋₁ (4 marks).')


def c5s3_explain(r):
    return xbank([
        ('Explain Gauss\'s method for finding 1 + 2 + … + 100.', 'Write the sum forwards and backwards and add: 100 pairs each summing to 101, so 2S = 100 × 101, S = 5050.', '2 marks.'),
        ('Explain why Sₙ − Sₙ₋₁ = aₙ for an AP.', 'Sₙ is Sₙ₋₁ plus the nth term.', '2 marks.'),
        ('Explain why the sum of n terms of an AP can be found as (number of terms) × (average of first and last term).', 'Pairing terms from both ends gives equal sums a + l; there are n/2 pairs.', '2 marks.'),
    ])(r)


def c5s3_ar(r):
    n = r.randint(10, 50)
    return arbank([
        (f'The sum of the first {n} odd natural numbers is {n * n}.', 'The sum of the first n odd natural numbers is n².', 'a', 'R explains A.'),
        (f'The sum of the first {n} natural numbers is {n * n}.', 'Sₙ = n/2 [2a + (n − 1)d].', 'd', f'It is {n * (n + 1) // 2}; A false, R true.'),
    ])(r)


def c5s3_multiples(r):
    k = r.choice([3, 4, 5, 6, 7, 8, 9, 11])
    hi = r.choice([100, 200, 250, 500])
    n = hi // k
    S = k * n * (n + 1) // 2
    return Q(f'Find the sum of all multiples of {k} that are less than or equal to {hi}.', str(S),
             f'AP {k}, {2 * k}, …, {n * k} with n = {n}; S = {n}/2 ({k} + {n * k}) = {S} (3 marks).', num_distractors(S, S - n * k, k * n * n, S + k))


def c5s3_case(r):
    rows, first, d = r.randint(10, 25), r.randint(10, 30), r.randint(1, 4)
    return Q((f'An auditorium in Kolkata has {rows} rows of seats. The first row has {first} seats and each row has {d} more seat{"s" if d > 1 else ""} than the row in front. '
              f'(i) How many seats are in the last row? (ii) Find the total number of seats. (iii) How many seats are in the first 10 rows? (iv) If tickets cost ₹150, what is the collection when all seats are sold?'),
             f'(i) {first + (rows - 1) * d} (ii) {rows * (2 * first + (rows - 1) * d) // 2} (iii) {10 * (2 * first + 9 * d) // 2} (iv) {inr(150 * rows * (2 * first + (rows - 1) * d) // 2)}',
             '1 mark each part.')


# st4 real-life

def c5s4_savings(r):
    who = name(r)
    a, d, n = r.choice([5, 10, 20, 50]), r.choice([5, 10, 20]), r.randint(8, 20)
    S = n * (2 * a + (n - 1) * d) // 2
    return Q(f'{who} saves ₹{a} in the first week of the year and increases the savings by ₹{d} every week. How much will {who} have saved in {n} weeks?', inr(S),
             f'S{sub(n)} = {n}/2 [2 × {a} + {n - 1} × {d}] = {S}.', [inr(S + d), inr(a + (n - 1) * d), inr(n * a)])


def c5s4_loan(r):
    first, d, n = r.choice([1000, 1500, 2000]), r.choice([100, 200, 250]), r.randint(10, 24)
    total = n * (2 * first + (n - 1) * d) // 2
    return Q(f'A loan is repaid in {n} monthly instalments that form an AP. The first instalment is ₹{first:,} and each instalment is ₹{d} more than the previous one. Find the last instalment and the total amount repaid.'.replace(',', ','),
             f'Last {inr(first + (n - 1) * d)}; total {inr(total)}', f'aₙ = {first} + {n - 1} × {d}; Sₙ = n/2 (a + l) (4 marks).')


def c5s4_potato(r):
    n = r.randint(6, 12)
    gap = r.choice([2, 3, 4])
    start = r.choice([3, 5])
    total = sum(2 * (start + i * gap) for i in range(n))
    return Q(f'In a potato race, a bucket is placed at the starting point, {start} m from the first potato. The other potatoes are placed {gap} m apart in a straight line; there are {n} potatoes. Each competitor starts at the bucket, picks up the nearest potato, runs back to drop it, and so on. What is the total distance run?',
             f'{total} m', f'Distances: 2 × {start}, 2 × {start + gap}, …; AP with a = {2 * start}, d = {2 * gap}, n = {n}: S = {total} (4 marks).')


def c5s4_ar(r):
    return arbank([
        ('If a person saves ₹10 more every week than the week before, the weekly savings form an AP.', 'The difference between consecutive weekly savings is constant.', 'a', 'R explains A.'),
        ('If the value of a machine falls by 10% every year, its values do not form an AP.', 'A fixed percentage decrease subtracts a smaller amount each year.', 'a', 'Differences shrink; R explains A.'),
    ])(r)


def c5s4_explain(r):
    return xbank([
        ('A ladder has rungs whose lengths decrease uniformly from 45 cm at the bottom to 25 cm at the top. Explain why the lengths form an AP and what information is needed to find the total length of wood.', 'Uniform decrease means a constant difference; we need the number of rungs n, then S = n/2 (45 + 25).', '2 marks.'),
        ('Explain how to decide whether the 3rd and the 7th terms are enough to find any term of an AP.', 'Two terms give two equations in a and d, which fix the AP.', '2 marks.'),
    ])(r)


def c5s4_case(r):
    a, d = r.choice([(600, 100), (5000, 500), (1200, 150), (800, 50)])
    n = r.randint(8, 15)
    return Q((f'A TV manufacturer in Pune produced {a} sets in the 3rd year and {a + 4 * d} sets in the 7th year. Production increases uniformly every year. '
              f'(i) Find the production in the 1st year. (ii) Find the production in the {ordinal(n)} year. (iii) Find the total production in the first {n} years. (iv) In which year is the production {a + 10 * d}?'),
             f'(i) {a - 2 * d} (ii) {a - 2 * d + (n - 1) * d} (iii) {n * (2 * (a - 2 * d) + (n - 1) * d) // 2} (iv) year 13', '1 mark each part.')


FAMILIES = {
    S + '01-st1': [F('C1', 'D2', 'mcq', c1s1_mcq), F('C1', 'D1', 'short', c1s1_pf), F('C2', 'D2', 'explain', c1s1_end0), F('C2', 'D3', 'explain', c1s1_composite),
                   F('C2', 'D2', 'mcq', c1s1_ar, kinds=('ar',)), F('C3', 'D2', 'short', c1s1_pf), F('C3', 'D3', 'short', c1s1_find_missing), F('C3', 'D4', 'multi_step', c1s1_case),
                   F('C4', 'D3', 'case', c1s1_case), F('C4', 'D4', 'explain', c1s1_end0)],
    S + '01-st2': [F('C1', 'D2', 'mcq', c2_mcq), F('C1', 'D1', 'short', c2_product), F('C2', 'D2', 'explain', c2_explain), F('C2', 'D3', 'mcq', c2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c2_hcf_lcm), F('C3', 'D3', 'numerical', c2_three), F('C3', 'D3', 'numerical', c2_other), F('C4', 'D3', 'multi_step', c2_other),
                   F('C3', 'D2', 'numerical', g9c.c11s2_hcf)],
    S + '01-st3': [F('C1', 'D2', 'mcq', c3_which), F('C2', 'D2', 'mcq', c3_ar, kinds=('ar',)), F('C2', 'D3', 'explain', c3_which), F('C3', 'D1', 'numerical', c3_army),
                   F('C3', 'D2', 'numerical', c3_bells), F('C3', 'D3', 'multi_step', c3_tiles, gap='G7'), F('C3', 'D3', 'numerical', c3_remainder), F('C4', 'D3', 'case', c3_case),
                   F('C4', 'D4', 'multi_step', c3_hcf_rem, gap='G7')],
    S + '01-st4': [F('C1', 'D2', 'mcq', c4_mcq), F('C1', 'D1', 'short', c4_rational_check), F('C2', 'D2', 'explain', c4_explain), F('C2', 'D3', 'mcq', c4_ar, kinds=('ar',)),
                   F('C3', 'D2', 'short', c4_rational_check), F('C3', 'D3', 'long', c4_prove), F('C3', 'D4', 'multi_step', c4_combo), F('C4', 'D3', 'case', c4_case),
                   F('C4', 'D4', 'long', c4_prove)],
    S + '02-st1': [F('C1', 'D2', 'mcq', c2s1_degree), F('C1', 'D1', 'short', c2s1_shape), F('C2', 'D2', 'explain', c2s1_explain), F('C2', 'D3', 'mcq', c2s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'short', c2s1_value), F('C3', 'D3', 'short', c2s1_shape), F('C4', 'D3', 'case', c2s1_case)],
    S + '02-st2': [F('C1', 'D2', 'mcq', c2s2_mcq), F('C1', 'D1', 'short', c2s2_count), F('C2', 'D2', 'explain', c2s2_explain), F('C2', 'D3', 'mcq', c2s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'short', c2s2_read), F('C3', 'D3', 'short', c2s2_count), F('C4', 'D3', 'case', c2s2_case)],
    S + '02-st3': [F('C1', 'D2', 'mcq', c2s3_sum), F('C2', 'D2', 'explain', c2s3_explain), F('C2', 'D3', 'mcq', c2s3_ar, kinds=('ar',)), F('C3', 'D1', 'mcq', c2s3_sum),
                   F('C3', 'D2', 'numerical', c2s3_sym), F('C3', 'D3', 'multi_step', c2s3_zeros), F('C3', 'D4', 'multi_step', c2s3_find_k), F('C4', 'D3', 'case', c2s3_case),
                   F('C4', 'D4', 'long', c2s3_cubic), F('C4', 'D5', 'long', c2s3_cubic)],
    S + '02-st4': [F('C1', 'D2', 'mcq', c2s4_roots), F('C2', 'D2', 'explain', c2s4_explain), F('C2', 'D2', 'mcq', c2s4_ar, kinds=('ar',)), F('C3', 'D1', 'short', c2s4_roots),
                   F('C3', 'D2', 'numerical', c2s4_form), F('C3', 'D3', 'numerical', c2s4_surd), F('C4', 'D3', 'multi_step', c2s4_transform), F('C4', 'D4', 'case', c2s4_case)],
    S + '03-st1': [F('C1', 'D2', 'mcq', c3s1_mcq), F('C2', 'D2', 'explain', c3s1_explain), F('C2', 'D3', 'mcq', c3s1_ar, kinds=('ar',)), F('C3', 'D1', 'mcq', c3s3_mcq),
                   F('C3', 'D2', 'numerical', c3s1_graph), F('C3', 'D3', 'multi_step', c3s1_graph), F('C4', 'D3', 'long', c3s1_vertices), F('C4', 'D4', 'case', c3s1_case)],
    S + '03-st2': [F('C1', 'D2', 'mcq', c3s2_mcq), F('C2', 'D2', 'short', c3s2_type), F('C2', 'D3', 'mcq', c3s2_ar, kinds=('ar',)), F('C2', 'D2', 'explain', c3s2_explain),
                   F('C3', 'D2', 'numerical', c3s2_type), F('C3', 'D3', 'numerical', c3s2_k), F('C4', 'D3', 'case', c3s2_case)],
    S + '03-st3': [F('C1', 'D2', 'mcq', c3s3_mcq), F('C2', 'D2', 'explain', c3s3_explain), F('C2', 'D3', 'mcq', c3s3_ar, kinds=('ar',)), F('C3', 'D1', 'numerical', c3s3_sub),
                   F('C3', 'D2', 'numerical', c3s3_sub2), F('C3', 'D3', 'multi_step', c3s3_sub2), F('C4', 'D3', 'multi_step', c3s5_digits, gap='G7')],
    S + '03-st4': [F('C1', 'D2', 'mcq', c3s3_mcq), F('C2', 'D2', 'explain', c3s4_explain), F('C2', 'D3', 'mcq', c3s4_ar, kinds=('ar',)), F('C3', 'D1', 'numerical', c3s4_elim),
                   F('C3', 'D2', 'numerical', c3s4_elim), F('C3', 'D3', 'multi_step', c3s4_recip), F('C4', 'D3', 'multi_step', c3s5_boat, gap='G7'), F('C3', 'D4', 'multi_step', c3s4_recip)],
    S + '03-st5': [F('C1', 'D2', 'mcq', c3s1_mcq), F('C2', 'D2', 'explain', c3s3_explain), F('C2', 'D3', 'mcq', c3s1_ar, kinds=('ar',)), F('C3', 'D2', 'multi_step', c3s5_cost, gap='G7'),
                   F('C3', 'D3', 'multi_step', c3s5_ages, gap='G7'), F('C3', 'D4', 'multi_step', c3s5_digits, gap='G7'), F('C4', 'D3', 'case', c3s5_case, gap='G7'),
                   F('C4', 'D4', 'long', c3s5_fraction, gap='G7'), F('C4', 'D5', 'long', c3s5_rect, gap='G7'), F('C3', 'D1', 'numerical', c3s5_boat, gap='G7')],
    S + '04-st1': [F('C1', 'D2', 'mcq', c4s1_check), F('C1', 'D1', 'short', c4s1_word), F('C2', 'D2', 'explain', c4s1_explain), F('C2', 'D3', 'mcq', c4s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'short', c4s1_form), F('C3', 'D3', 'numerical', c4s1_reduce), F('C4', 'D3', 'case', c4s1_case, gap='G7')],
    S + '04-st2': [F('C1', 'D2', 'mcq', c4s2_mcq), F('C2', 'D2', 'explain', c4s2_explain), F('C2', 'D3', 'mcq', c4s2_ar, kinds=('ar',)), F('C3', 'D1', 'numerical', c4s2_solve),
                   F('C3', 'D2', 'numerical', c4s2_solve), F('C3', 'D3', 'numerical', c4s2_solve), F('C3', 'D4', 'multi_step', c4s2_rational), F('C4', 'D3', 'case', c4s2_case),
                   F('C4', 'D4', 'multi_step', c4s2_hard)],
    S + '04-st3': [F('C1', 'D2', 'mcq', c4s3_mcq), F('C2', 'D2', 'explain', c4s3_explain), F('C2', 'D3', 'mcq', c4s3_ar, kinds=('ar',)), F('C3', 'D1', 'short', c4s3_disc),
                   F('C3', 'D2', 'numerical', c4s3_disc), F('C3', 'D3', 'numerical', c4s3_formula), F('C3', 'D4', 'multi_step', c4s3_k), F('C4', 'D3', 'case', c4s3_case),
                   F('C4', 'D4', 'multi_step', c4s3_k)],
    S + '04-st4': [F('C1', 'D2', 'mcq', c4s4_ar, kinds=('ar',)), F('C2', 'D2', 'explain', c4s4_explain), F('C2', 'D3', 'mcq', c4s1_check), F('C3', 'D2', 'multi_step', c4s4_consec, gap='G7'),
                   F('C3', 'D3', 'multi_step', c4s4_rect, gap='G7'), F('C3', 'D4', 'multi_step', c4s4_age, gap='G7'), F('C4', 'D3', 'case', c4s4_case, gap='G7'),
                   F('C4', 'D4', 'long', c4s4_speed, gap='G7'), F('C3', 'D1', 'numerical', c4s4_rect, gap='G7'), F('C1', 'D2', 'short', c4s1_word)],
    S + '05-st1': [F('C1', 'D2', 'short', c5s1_is_ap), F('C1', 'D1', 'short', c5s1_next), F('C2', 'D2', 'explain', c5s1_explain), F('C2', 'D3', 'mcq', c5s1_ar, kinds=('ar',)),
                   F('C2', 'D2', 'mcq', g9b.c8s2_d), F('C3', 'D2', 'short', c5s1_first_terms), F('C3', 'D3', 'short', c5s1_is_ap), F('C4', 'D3', 'case', c5s1_case)],
    S + '05-st2': [F('C1', 'D2', 'mcq', g9b.c8s2_d), F('C1', 'D1', 'short', g9b.c8s2_nth), F('C2', 'D2', 'explain', c5s2_explain), F('C2', 'D3', 'mcq', c5s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', g9b.c8s2_which), F('C3', 'D3', 'numerical', c5s2_count), F('C3', 'D3', 'numerical', c5s2_last), F('C3', 'D4', 'multi_step', g9b.c8s2_two_terms),
                   F('C4', 'D3', 'case', c5s2_case), F('C4', 'D4', 'multi_step', c5s2_multiples), F('C4', 'D5', 'long', c5s2_three)],
    S + '05-st3': [F('C1', 'D2', 'mcq', c5s3_mcq), F('C2', 'D2', 'explain', c5s3_explain), F('C2', 'D3', 'mcq', c5s3_ar, kinds=('ar',)), F('C3', 'D1', 'numerical', c5s3_first_last),
                   F('C3', 'D2', 'numerical', c5s3_sum), F('C3', 'D3', 'numerical', c5s3_multiples), F('C3', 'D4', 'multi_step', c5s3_find_n), F('C4', 'D3', 'case', c5s3_case),
                   F('C4', 'D4', 'long', c5s3_sn), F('C4', 'D5', 'long', c5s3_find_n)],
    S + '05-st4': [F('C1', 'D2', 'mcq', c5s4_ar, kinds=('ar',)), F('C2', 'D2', 'explain', c5s4_explain), F('C2', 'D3', 'mcq', c5s3_mcq), F('C3', 'D2', 'numerical', c5s4_savings, gap='G7'),
                   F('C3', 'D3', 'multi_step', c5s4_loan, gap='G7'), F('C4', 'D3', 'case', c5s4_case, gap='G7'), F('C4', 'D4', 'long', c5s4_potato, gap='G7'), F('C3', 'D1', 'numerical', c5s4_savings, gap='G7')],
}
