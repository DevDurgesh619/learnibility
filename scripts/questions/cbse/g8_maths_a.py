"""CBSE class 8 maths (Ganita Prakash) families, chapters 1-4."""
from __future__ import annotations

import math

from qbank import F, ar, mcq, num, sup, frac, factorise, fstr, name, two_names, inr, num_distractors

S = 'cbse-g8-maths-ch'
NON_SQ_END = [2, 3, 7, 8]


# ---------------- ch01 A Square and a Cube ----------------
# st1 Perfect squares and their patterns

def c1s1_which_square(r):
    n = r.randint(11, 45)
    sq = n * n
    wrong = set()
    while len(wrong) < 3:
        w = sq + r.choice([-1, 1]) * r.randint(2, 2 * n - 1)
        if int(math.isqrt(w)) ** 2 != w:
            wrong.add(w)
    return mcq('Which of the following numbers is a perfect square?', str(sq), [str(w) for w in wrong],
               f'{sq} = {n}²; the others lie between consecutive squares.', r)


def c1s1_units(r):
    good = r.choice([1, 4, 5, 6, 9, 0])
    wrong = r.sample(NON_SQ_END, 3)
    return mcq('A perfect square can end in which of these digits?', str(good), [str(w) for w in wrong],
               f'Squares end only in 0, 1, 4, 5, 6 or 9, so {good} is possible; 2, 3, 7 and 8 never occur.', r)


def c1s1_not_square_explain(r):
    n = r.randint(100, 999) * 10 + r.choice(NON_SQ_END)
    return {'stem': f'Without finding its square root, explain why {n:,} cannot be a perfect square.'.replace(',', ''),
            'answer': f'It ends in {n % 10}; no perfect square ends in 2, 3, 7 or 8.',
            'key': f'1 mark: units digit {n % 10} named and the rule that squares end only in 0, 1, 4, 5, 6 or 9.'}


def c1s1_odd_sum(r):
    k = r.randint(6, 25)
    terms = ' + '.join(str(2 * i + 1) for i in range(4)) + f' + … + {2 * k - 1}'
    return {'stem': f'Find the sum {terms} without adding term by term.',
            'answer': f'{k * k}',
            'key': f'There are {k} odd numbers (since {2 * k - 1} = 2 × {k} − 1); the sum of the first n odd numbers is n², so {k}² = {k * k}.',
            'distractors': num_distractors(k * k, (k - 1) ** 2, k * (k + 1), 2 * k * k)}


def c1s1_between(r):
    n = r.randint(15, 99)
    return {'stem': f'How many non-square natural numbers lie between {n}² and {n + 1}²?',
            'answer': str(2 * n),
            'key': f'Between n² and (n + 1)² there are 2n numbers; 2 × {n} = {2 * n}.',
            'distractors': num_distractors(2 * n, 2 * n + 1, n, 2 * n - 1)}


def c1s1_square_by_pattern(r):
    base = r.choice([20, 30, 40, 50, 60, 70, 80, 90])
    d = r.choice([1, 2, 3, -1, -2])
    n = base + d
    sign = '+' if d > 0 else '−'
    return {'stem': f'Use the pattern ({base} {sign} {abs(d)})² to find {n}² without long multiplication.',
            'answer': str(n * n),
            'key': f'{base}² {sign} 2 × {base} × {abs(d)} + {d * d} = {base * base} {sign} {2 * base * abs(d)} + {d * d} = {n * n}.',
            'distractors': num_distractors(n * n, base * base + d * d, base * base + 2 * base * d, n * n + 10)}


def c1s1_ends_in_5(r):
    a = r.randint(3, 19)
    n = 10 * a + 5
    return {'stem': f'A shortcut says: to square a number ending in 5, multiply the tens part by the next number and write 25 after it. Use it to find {n}², and check it with (10a + 5)².',
            'answer': f'{n * n}',
            'key': f'{a} × {a + 1} = {a * (a + 1)}, so {n}² = {n * n}. Check: (10a + 5)² = 100a(a + 1) + 25.'}


def c1s1_units_of_square(r):
    n = r.randint(101, 989)
    u = (n % 10) ** 2 % 10
    return {'stem': f'What is the units digit of {n}²?', 'answer': str(u),
            'key': f'Only the units digit {n % 10} matters: {n % 10}² = {(n % 10) ** 2}, so the units digit is {u}.',
            'distractors': [str(x) for x in r.sample([d for d in range(10) if d != u], 3)]}


def c1s1_tiles(r):
    who = name(r)
    n = r.randint(12, 40)
    extra = r.randint(5, 2 * n - 1)
    total = n * n + extra
    return {'stem': f'{who} has {total} square tiles and wants to lay the largest possible square floor pattern with them. How many tiles will be left over, and what is the side of the square (in tiles)?',
            'answer': f'Side {n} tiles, {extra} left over',
            'key': f'{n}² = {n * n} ≤ {total} < {(n + 1) ** 2} = {n + 1}²; side {n}, left over {total} − {n * n} = {extra}.'}


def c1s1_consecutive_squares(r):
    n = r.randint(10, 40)
    s = n * n + (n + 1) ** 2
    return {'stem': f'The sum of the squares of two consecutive natural numbers is {s}. Find the numbers, showing how you narrowed the search.',
            'answer': f'{n} and {n + 1}',
            'key': f'Each square is about {s}/2 = {s / 2:g}, so the smaller number is near √{s // 2} ≈ {n}. Check: {n}² + {n + 1}² = {n * n} + {(n + 1) ** 2} = {s}.'}


def c1s1_ar(r):
    n = r.randint(11, 30)
    if r.random() < 0.5:
        return ar(f'{n * n} has an odd number of factors.', 'Every perfect square has an odd number of factors, because one factor pairs with itself.', 'a',
                  f'{n * n} = {n}², and factors of a square pair up except √n = {n}; R explains A.')
    m = n * n + 1
    return ar(f'{m} is a perfect square because it ends in {m % 10}.', 'Every perfect square ends in 0, 1, 4, 5, 6 or 9.', 'd',
              f'A is false ({n}² = {n * n} < {m} < {(n + 1) ** 2}); R is true, but the units-digit rule can only rule numbers out.')


def c1s1_pattern_case(r):
    k = r.randint(4, 9)
    return {'stem': (f'Look at the pattern: 1 = 1², 1 + 3 = 2², 1 + 3 + 5 = 3², …\n'
                     f'(i) Write the line that gives {k}². (ii) Which odd number must be added to {k}² to get {k + 1}²? '
                     f'(iii) Use the pattern to show that {2 * k + 1} + {2 * k + 3} = {(k + 2) ** 2} − {k * k}.'),
            'answer': f'(i) 1 + 3 + … + {2 * k - 1} = {k}² (ii) {2 * k + 1} (iii) {(k + 2) ** 2 - k * k}',
            'key': f'(i) {k} odd numbers ending at {2 * k - 1} (1 mark). (ii) (k + 1)² − k² = 2k + 1 = {2 * k + 1} (1 mark). (iii) adding the next two odd numbers moves from {k}² to {k + 2}²: {4 * k + 4} = {(k + 2) ** 2} − {k * k} (2 marks).'}


# st2 Square roots: prime factorisation and estimation

def _pf_square(r):
    while True:
        a = r.choice([2, 3, 5, 7, 11, 13])
        b = r.choice([2, 3, 5, 7])
        c = r.choice([1, 2, 3])
        root = a * b * c
        if 20 <= root <= 99:
            return root


def c1s2_rule(r):
    return mcq('In the prime-factorisation method, a number is a perfect square when …',
               'every prime appears an even number of times',
               ['every prime appears an odd number of times', 'the number has exactly two prime factors',
                'the number is divisible by 4'],
               'Primes must pair up, so every exponent is even.', r)


def c1s2_pf_root(r):
    root = _pf_square(r)
    n = root * root
    return {'stem': f'Find √{n} by prime factorisation.', 'answer': str(root),
            'key': f'{n} = {fstr(factorise(n))}; take one prime from each pair: √{n} = {fstr(factorise(root))} = {root}.',
            'distractors': num_distractors(root, root + 2, root - 2, n // 2)}


def c1s2_split_root(r):
    a = r.randint(2, 9)
    b = r.choice([10, 100])
    n = a * a * b * b
    return {'stem': f'Explain in one line how √(a × b) = √a × √b makes √{n} easy to find, and find it.',
            'answer': str(a * b), 'key': f'√{n} = √{a * a} × √{b * b} = {a} × {b} = {a * b}.'}


def c1s2_error(r):
    p, q = r.choice([(9, 16), (36, 64), (16, 9), (25, 144), (81, 144), (144, 25)])
    return {'stem': f'A student writes √({p} + {q}) = √{p} + √{q} = {int(math.isqrt(p)) + int(math.isqrt(q))}. Find the error with a check.',
            'answer': f'√{p + q} = {math.sqrt(p + q):g}, not {int(math.isqrt(p)) + int(math.isqrt(q))}',
            'key': f'√({p} + {q}) = √{p + q} = {math.sqrt(p + q):g}. A square root does not distribute over addition (it does over multiplication).',
            'gap': 'G2'}


def c1s2_estimate(r):
    n = r.choice([x for x in range(20, 400) if math.isqrt(x) ** 2 != x])
    lo = math.isqrt(n)
    est = round(math.sqrt(n), 1)
    return {'stem': f'Estimate √{n} to one decimal place without a calculator.',
            'answer': f'≈ {est}',
            'key': f'{lo}² = {lo * lo} and {lo + 1}² = {(lo + 1) ** 2}, so {lo} < √{n} < {lo + 1}; trial: {est}² = {est * est:.2f}, so √{n} ≈ {est}.',
            'distractors': [f'≈ {x}' for x in (round(est + 0.3, 1), round(est - 0.4, 1), round(n / 2, 1))]}


def c1s2_multiply_to_square(r):
    while True:
        core = r.choice([2, 3, 5, 7, 6, 10, 3 * 5])
        k = r.randint(4, 15)
        n = core * k * k
        if 150 <= n <= 3000:
            break
    f = factorise(n)
    mult = 1
    for p, e in f.items():
        if e % 2:
            mult *= p
    return {'stem': f'Find the smallest number by which {n} must be multiplied to make it a perfect square. Also find the square root of the new number.',
            'answer': f'Multiply by {mult}; √{n * mult} = {math.isqrt(n * mult)}',
            'key': f'{n} = {fstr(f)}; unpaired primes multiply to {mult}. {n} × {mult} = {n * mult} = {math.isqrt(n * mult)}².'}


def c1s2_subtract(r):
    n = r.randint(300, 5000)
    lo = math.isqrt(n)
    if lo * lo == n:
        n += 3
    return {'stem': f'Find the least number that must be subtracted from {n} to make it a perfect square, and give the square root of the result.',
            'answer': f'Subtract {n - lo * lo}; √{lo * lo} = {lo}',
            'key': f'{lo}² = {lo * lo} ≤ {n} < {(lo + 1) ** 2} = {lo + 1}²; {n} − {lo * lo} = {n - lo * lo}; root {lo}.'}


def c1s2_garden(r):
    s = r.choice([1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5])
    w = r.choice([0.5, 1, 1.5])
    return {'stem': f'A square garden has an area of {s * s:g} m². A path {w:g} m wide is built all around it, outside the garden. Find the area of the path.',
            'answer': f'{(s + 2 * w) ** 2 - s * s:g} m²',
            'key': f'Side = √{s * s:g} = {s:g} m; outer side = {s + 2 * w:g} m; path = {s + 2 * w:g}² − {s * s:g} = {(s + 2 * w) ** 2 - s * s:g} m².'}


def c1s2_chairs(r):
    n = r.randint(20, 45)
    extra = r.randint(5, 2 * n)
    ok = math.isqrt(n * n + extra) ** 2 == n * n + extra
    more = (n + 1) ** 2 - n * n - extra
    return {'stem': f'{n * n} chairs in a school hall are arranged with as many rows as columns. {extra} more chairs arrive. Can all the chairs still form a square arrangement? If not, how many more chairs are needed for the next square?',
            'answer': ('Yes' if ok else f'No; {more} more chairs'),
            'key': f'{n}² = {n * n}; {n * n} + {extra} = {n * n + extra}; {n + 1}² = {(n + 1) ** 2}, so {more if not ok else 0} more are needed.'}


def c1s2_ar(r):
    root = _pf_square(r)
    n = root * root
    return ar(f'√{n} = {root}.', f'{n} = {fstr(factorise(n))}, in which every prime occurs an even number of times.', 'a',
              f'Both true; pairing the primes gives the root {root}, so R explains A.')


def c1s2_decimal_root(r):
    k = r.randint(11, 39)
    n = k * k
    return {'stem': f'Given that √{n} = {k}, find √{n / 100:g} and √{n * 100}.',
            'answer': f'{k / 10:g} and {k * 10}',
            'key': f'√({n}/100) = {k}/10 = {k / 10:g}; √({n} × 100) = {k} × 10 = {k * 10}.',
            'distractors': [f'{k / 100:g} and {k * 100}', f'{k / 10:g} and {k * 100}', f'{k} and {k * 10}']}


# st3 Perfect cubes and cube roots

def c1s3_which_cube(r):
    n = r.randint(4, 15)
    c = n ** 3
    wrong = [c + r.randint(5, 40), c - r.randint(5, 30), n * n * (n + 1)]
    return mcq('Which of these is a perfect cube?', str(c), [str(w) for w in wrong], f'{c} = {n}³.', r)


def c1s3_cuberoot_pf(r):
    a, b = r.sample([2, 3, 5, 7], 2)
    root = a * b * r.choice([1, 1, 2])
    n = root ** 3
    return {'stem': f'Find ∛{n} by prime factorisation.', 'answer': str(root),
            'key': f'{n} = {fstr(factorise(n))}; group the primes in threes: ∛{n} = {fstr(factorise(root))} = {root}.',
            'distractors': num_distractors(root, root * root, root + 1, n // 3)}


def c1s3_divide_to_cube(r):
    p = r.choice([2, 3, 5])
    e = r.choice([4, 5, 7, 8])
    q = r.choice([1, 7, 11]) if p != 7 else 1
    n = p ** e * q ** 3
    rem = e % 3
    div = p ** rem
    return {'stem': f'Find the smallest number by which {n} must be divided to get a perfect cube.',
            'answer': str(div),
            'key': f'{n} = {fstr(factorise(n))}; {p}{sup(e)} leaves {p}{sup(rem) if rem > 1 else ""} unmatched, so divide by {div} to get {n // div} = {round((n // div) ** (1 / 3))}³.'}


def c1s3_double_side(r):
    k = r.choice([2, 3, 4])
    return {'stem': f'Explain why multiplying the side of a cube by {k} multiplies its volume by {k ** 3}, not by {k}.',
            'answer': f'({k}s)³ = {k ** 3}s³',
            'key': f'All three dimensions are multiplied by {k}: {k} × {k} × {k} = {k ** 3}.'}


def c1s3_units_cube(r):
    d = r.randint(0, 9)
    n = r.randint(10, 99) * 10 + d
    u = d ** 3 % 10
    return {'stem': f'What is the units digit of {n}³?', 'answer': str(u),
            'key': f'{d}³ = {d ** 3}, so the units digit is {u}.',
            'distractors': [str(x) for x in r.sample([x for x in range(10) if x != u], 3)]}


def c1s3_cuboids(r):
    a, b, c = r.choice([(5, 2, 5), (3, 3, 2), (2, 4, 4), (6, 3, 4), (2, 2, 6), (4, 3, 3)])
    v = a * b * c
    f = factorise(v)
    m = 1
    for p, e in f.items():
        m *= p ** ((3 - e % 3) % 3)
    side = round((v * m) ** (1 / 3))
    return {'stem': f'Cuboids measuring {a} cm × {b} cm × {c} cm are stacked to make the smallest possible solid cube. How many cuboids are needed, and what is the side of the cube?',
            'answer': f'{m} cuboids; side {side} cm',
            'key': f'Volume {v} = {fstr(f)}; make every exponent a multiple of 3: × {m} → {v * m} = {side}³. So {m} cuboids, side {side} cm.'}


def c1s3_ends_explain(r):
    return {'stem': 'Explain in one line why a perfect cube can end in any digit 0 to 9, while a perfect square cannot.',
            'answer': 'Cubes of 0 to 9 end in 0, 1, 8, 7, 4, 5, 6, 3, 2, 9: every digit appears.',
            'key': 'Listing the units digits of 0³ to 9³ shows all ten digits; squares end only in 0, 1, 4, 5, 6, 9.'}


def c1s3_hardy(r):
    pairs = [(1729, (1, 12), (9, 10)), (4104, (2, 16), (9, 15)), (13832, (2, 24), (18, 20))]
    n, p1, p2 = r.choice(pairs)
    return {'stem': f'{n} can be written as the sum of two cubes in two different ways. Find both ways.',
            'answer': f'{p1[0]}³ + {p1[1]}³ and {p2[0]}³ + {p2[1]}³',
            'key': f'{p1[0] ** 3} + {p1[1] ** 3} = {n}; {p2[0] ** 3} + {p2[1] ** 3} = {n}. (1729 is the Hardy–Ramanujan number.)'}


def c1s3_ar(r):
    n = r.randint(3, 12)
    return ar(f'The cube of {2 * n} is {8 * n ** 3}.', 'The cube of an even number is even.', 'b',
              f'({2 * n})³ = 8 × {n ** 3} = {8 * n ** 3}; R is true but it does not explain the value 8n³.')


def c1s3_cube_estimate(r):
    n = r.randint(2000, 90000)
    lo = round(n ** (1 / 3) - 0.5)
    while (lo + 1) ** 3 <= n:
        lo += 1
    while lo ** 3 > n:
        lo -= 1
    return {'stem': f'Between which two consecutive natural numbers does ∛{n} lie?',
            'answer': f'{lo} and {lo + 1}',
            'key': f'{lo}³ = {lo ** 3} and {lo + 1}³ = {(lo + 1) ** 3}.',
            'distractors': [f'{lo - 1} and {lo}', f'{lo + 1} and {lo + 2}', f'{lo * 2} and {lo * 2 + 1}']}


# st4 Pythagorean triplets and square-number puzzles

def c1s4_largest(r):
    return mcq('For a natural number m > 1, (2m, m² − 1, m² + 1) is a Pythagorean triplet. Which member is always the largest?',
               'm² + 1', ['2m', 'm² − 1', 'It depends on m'], 'm² + 1 exceeds both m² − 1 and 2m for m > 1.', r)


def c1s4_from_small(r):
    m = r.randint(3, 12)
    return {'stem': f'Use (2m, m² − 1, m² + 1) to write a Pythagorean triplet whose smallest even member is {2 * m}.',
            'answer': f'({2 * m}, {m * m - 1}, {m * m + 1})',
            'key': f'2m = {2 * m} → m = {m}; m² − 1 = {m * m - 1}, m² + 1 = {m * m + 1}. Check {4 * m * m} + {(m * m - 1) ** 2} = {(m * m + 1) ** 2}.'}


def c1s4_member(r):
    m = r.randint(3, 10)
    big = m * m + 1
    return {'stem': f'Find a Pythagorean triplet in which {big} is the largest member.',
            'answer': f'({2 * m}, {m * m - 1}, {big})',
            'key': f'm² + 1 = {big} → m = {m}; triplet ({2 * m}, {m * m - 1}, {big}).'}


def c1s4_is_triplet(r):
    base = r.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41)])
    k = r.randint(1, 4)
    a, b, c = (x * k for x in base)
    if r.random() < 0.4:
        c += 1
    ok = a * a + b * b == c * c
    return {'stem': f'Check whether ({a}, {b}, {c}) is a Pythagorean triplet.',
            'answer': 'Yes' if ok else 'No',
            'key': f'{a}² + {b}² = {a * a + b * b}; {c}² = {c * c}; {"equal" if ok else "not equal"}.',
            'distractors': ['Yes' if not ok else 'No', 'Only if they are sides of an equilateral triangle', 'Cannot be decided without a diagram']}


def c1s4_scale(r):
    base = r.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17)])
    k = r.randint(2, 6)
    return {'stem': f'Explain in one line why ({base[0]}, {base[1]}, {base[2]}) and ({k * base[0]}, {k * base[1]}, {k * base[2]}) are both Pythagorean triplets.',
            'answer': f'Multiplying all sides by {k} multiplies each square by {k * k}, so the equation still holds.',
            'key': f'({k}a)² + ({k}b)² = {k * k}(a² + b²) = {k * k}c² = ({k}c)².'}


def c1s4_number_square(r):
    n = r.randint(6, 25)
    return {'stem': f'The sum of a natural number and its square is {n + n * n}. Find the number using a table of squares (no formulas).',
            'answer': str(n), 'key': f'{n}² + {n} = {n * n} + {n} = {n * n + n}.',
            'distractors': num_distractors(n, n + 1, n - 1, n * 2)}


def c1s4_ladder(r):
    a, b, c = r.choice([(6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17), (7, 24, 25)])
    who = name(r)
    return {'stem': f'{who} leans a {c} m ladder against a wall so that its foot is {a} m from the wall. Using a Pythagorean triplet, how high up the wall does the ladder reach?',
            'answer': f'{b} m', 'key': f'({a}, {b}, {c}) is a triplet: {a * a} + {b * b} = {c * c}.'}


def c1s4_not_formula(r):
    return {'stem': 'Is (5, 12, 13) produced by the formula (2m, m² − 1, m² + 1) for some natural number m? What does this tell you about the formula?',
            'answer': 'No; the formula does not give every triplet.',
            'key': '2m = 12 gives m = 6 but then m² − 1 = 35 ≠ 5; (5, 12, 13) is a triplet the formula misses, so it generates some but not all triplets.'}


def c1s4_ar(r):
    m = r.randint(3, 9)
    return ar(f'({2 * m}, {m * m - 1}, {m * m + 1}) is a Pythagorean triplet.', '(m² + 1)² − (m² − 1)² = 4m² = (2m)² for every m.', 'a',
              'The identity in R proves A.')


def c1s4_count_squares(r):
    n = r.randint(3, 8)
    tot = sum(k * k for k in range(1, n + 1))
    return {'stem': f'How many squares of all sizes are there in an {n} × {n} grid of unit squares? Explain the pattern you use.',
            'answer': str(tot),
            'key': f'1 × 1: {n}², 2 × 2: {n - 1}², …, {n} × {n}: 1²; total 1² + 2² + … + {n}² = {tot}.'}


# ---------------- ch02 Power Play ----------------
# st1 Exponent notation and laws of exponents

def c2s1_div(r):
    a = r.choice([2, 3, 5, 7])
    m, n = r.randint(5, 12), r.randint(2, 4)
    return mcq(f'Simplify {a}{sup(m)} ÷ {a}{sup(n)}.', f'{a}{sup(m - n)}',
               [f'{a}{sup(m + n)}', f'1{sup(m - n)}', f'{a}{sup(m * n)}'], 'Same base: subtract the exponents.', r)


def c2s1_pow_pow(r):
    a = r.choice([2, 3, 10])
    m, n = r.randint(2, 4), r.randint(2, 3)
    return {'stem': f'Explain in one line why ({a}{sup(m)}){sup(n)} is not equal to {a}{sup(m + n)}.',
            'answer': f'({a}{sup(m)}){sup(n)} = {a}{sup(m * n)}',
            'key': f'A power of a power multiplies exponents: {n} copies of {a}{sup(m)} give {a}{sup(m * n)} = {a ** (m * n)}, while {a}{sup(m + n)} = {a ** (m + n)}.'}


def c2s1_wrong_base(r):
    a, b = r.sample([2, 3, 5], 2)
    m, n = r.randint(2, 4), r.randint(2, 3)
    return {'stem': f'A student writes {a}{sup(m)} × {b}{sup(n)} = {a * b}{sup(m + n)}. Show why this is wrong.',
            'answer': f'{a}{sup(m)} × {b}{sup(n)} = {a ** m * b ** n}, but {a * b}{sup(m + n)} = {(a * b) ** (m + n)}',
            'key': 'aᵐ × aⁿ = aᵐ⁺ⁿ needs the SAME base; numerical check shows the values differ.'}


def c2s1_simplify(r):
    a = r.choice([2, 3, 5, 7])
    p, q, s = r.randint(3, 8), r.randint(2, 6), r.randint(2, 6)
    e = p + q - s
    if e < 0:
        s = p + q - 1
        e = 1
    return {'stem': f'Simplify ({a}{sup(p)} × {a}{sup(q)}) ÷ {a}{sup(s)} and write the value.',
            'answer': f'{a}{sup(e)} = {a ** e}',
            'key': f'{a}{sup(p + q)} ÷ {a}{sup(s)} = {a}{sup(e)} = {a ** e}.',
            'distractors': [f'{a}{sup(p * q - s)}', f'{a}{sup(p + q + s)}', f'{a ** (e + 1)}']}


def c2s1_mixed(r):
    x, y = r.randint(2, 4), r.randint(3, 6)
    return {'stem': f'Simplify (2{sup(x + 2)} × 3{sup(y)} × 4) ÷ (3{sup(y - 2)} × 2{sup(x + 4)}).',
            'answer': '9', 'key': f'4 = 2²: numerator 2{sup(x + 4)} × 3{sup(y)}; dividing leaves 3² = 9.'}


def c2s1_solve(r):
    b = r.choice([2, 3, 5])
    x = r.randint(2, 6)
    p = r.randint(2, 5)
    q = r.randint(1, 3)
    total = x + p + q
    return {'stem': f'If {b}ˣ × {b}{sup(p)} = {b}{sup(total)} ÷ {b}{sup(q)}, find x and then the value of {b}ˣ.',
            'answer': f'x = {x}; {b}ˣ = {b ** x}',
            'key': f'{b}^(x + {p}) = {b}{sup(total - q)} → x = {total - q - p} = {x}; {b}{sup(x)} = {b ** x}.'}


def c2s1_algebra(r):
    p, q, s = r.randint(2, 4), r.randint(1, 3), r.randint(2, 5)
    a_exp = 2 * p + s - (p + 1)
    b_exp = 2 * q - q
    return {'stem': f'Simplify [(a{sup(p)}b{sup(q)})² × a{sup(s)}] ÷ (a{sup(p + 1)}b{sup(q)}).',
            'answer': f'a{sup(a_exp)}b{sup(b_exp) if b_exp > 1 else ""}',
            'key': f'(a{sup(p)}b{sup(q)})² = a{sup(2 * p)}b{sup(2 * q)}; × a{sup(s)} → a{sup(2 * p + s)}b{sup(2 * q)}; ÷ a{sup(p + 1)}b{sup(q)} → a{sup(a_exp)}b{sup(b_exp) if b_exp > 1 else ""}.'}


def c2s1_bacteria(r):
    start = r.randint(2, 5)
    h = r.randint(3, 8)
    return {'stem': f'A bacteria colony doubles every hour. It starts with 2{sup(start)} bacteria. (i) After {h} hours the count is 2ⁿ; find n. (ii) After how many more hours will the count be 2{sup(start + h + 3)}?',
            'answer': f'(i) n = {start + h} (ii) 3 hours',
            'key': f'(i) 2{sup(start)} × 2{sup(h)} = 2{sup(start + h)}. (ii) each hour adds 1 to the exponent: {start + h + 3} − {start + h} = 3.'}


def c2s1_value(r):
    b = r.choice([2, 3, 4, 5])
    e = r.randint(2, 5) if b <= 3 else r.randint(2, 4)
    return mcq(f'What is the value of {b}{sup(e)}?', str(b ** e), [str(b * e), str(e ** b) if e ** b != b ** e else str(b ** e + b), str(b ** (e - 1))],
               f'{b}{sup(e)} = ' + ' × '.join([str(b)] * e) + f' = {b ** e}.', r)


def c2s1_ar(r):
    a = r.choice([2, 3, 5])
    m, n = r.randint(2, 5), r.randint(2, 5)
    return ar(f'{a}{sup(m)} × {a}{sup(n)} = {a}{sup(m + n)}.', 'When powers with the same base are multiplied, the exponents are added.', 'a', 'R is the product law that gives A.')


def c2s1_paper(r):
    k = r.randint(5, 9)
    t = r.choice([0.1, 0.05])
    return {'stem': f'A sheet of paper {t} mm thick is folded in half {k} times. Write the thickness of the folded stack as a power of 2 times {t} mm, and find it.',
            'answer': f'2{sup(k)} × {t} = {2 ** k * t:g} mm',
            'key': f'Each fold doubles the layers: 2{sup(k)} = {2 ** k} layers; {2 ** k} × {t} = {2 ** k * t:g} mm.'}


# st2 Zero and negative exponents

def c2s2_values(r):
    a = r.randint(3, 99)
    b = r.choice([2, 3, 4, 5])
    e = r.randint(2, 3)
    return {'stem': f'Write the values of {a}⁰ and {b}{sup(-e)}.', 'answer': f'1 and 1/{b ** e}',
            'key': f'Any non-zero number to the power 0 is 1; {b}{sup(-e)} = 1/{b}{sup(e)} = 1/{b ** e}.',
            'distractors': [f'0 and −{b ** e}', f'{a} and 1/{b ** e}', f'1 and −{b * e}']}


def c2s2_zero_explain(r):
    a = r.choice(['a', 'x', '7', '5'])
    k = r.randint(2, 6)
    return {'stem': f'Using {a}{sup(k)} ÷ {a}{sup(k)}, explain in one line why {a}⁰ = 1.',
            'answer': f'{a}{sup(k)} ÷ {a}{sup(k)} = {a}⁰ by the quotient law, and any non-zero number divided by itself is 1.',
            'key': 'Both readings of the same division must agree, so a⁰ = 1 (a ≠ 0).'}


def c2s2_sign(r):
    b = r.choice([2, 3, 5])
    return {'stem': f'Why is (−{b}){sup(-2)} positive but (−{b}){sup(-3)} negative?',
            'answer': f'(−{b}){sup(-2)} = 1/{b * b}; (−{b}){sup(-3)} = −1/{b ** 3}',
            'key': 'A negative exponent takes the reciprocal; the sign depends on whether the power is even or odd.'}


def c2s2_fraction(r):
    p, q = r.choice([(2, 3), (3, 4), (2, 5), (4, 5), (3, 7), (5, 6)])
    e = r.randint(2, 3)
    return {'stem': f'Evaluate ({p}/{q}){sup(-e)}.', 'answer': f'{q ** e}/{p ** e}',
            'key': f'({p}/{q}){sup(-e)} = ({q}/{p}){sup(e)} = {q ** e}/{p ** e}.',
            'distractors': [f'{p ** e}/{q ** e}', f'−{p ** e}/{q ** e}', f'{q * e}/{p * e}']}


def c2s2_simplify(r):
    b = r.choice([2, 3, 5])
    x, y, z = -r.randint(2, 5), r.randint(3, 7), -r.randint(1, 3)
    e = x + y - z
    return {'stem': f'Simplify {b}{sup(x)} × {b}{sup(y)} ÷ {b}{sup(z)}.', 'answer': f'{b}{sup(e)}' + (f' = {b ** e}' if 0 <= e <= 6 else ''),
            'key': f'Exponents: {num(x)} + {y} − ({num(z)}) = {e}.'}


def c2s2_solve(r):
    b = r.choice([2, 3])
    k = r.randint(2, 5)
    return {'stem': f'Find x if (1/{b})ˣ = {b ** k}.', 'answer': f'x = −{k}',
            'key': f'(1/{b})ˣ = {b}^(−x) = {b}{sup(k)} → −x = {k} → x = −{k}.',
            'distractors': [f'x = {k}', f'x = 1/{k}', f'x = {b * k}']}


def c2s2_reciprocal(r):
    b = r.choice([2, 3, 4, 5, 10])
    e = r.randint(1, 4)
    return mcq(f'{b}{sup(-e)} is equal to …', f'1/{b ** e}', [f'−{b ** e}', f'{b ** e}', f'−1/{b ** e}'], f'{b}{sup(-e)} = 1/{b}{sup(e)}.', r)


def c2s2_ar(r):
    b = r.choice([2, 3, 5])
    return ar(f'{b}{sup(-2)} is a negative number.', 'A negative exponent means the reciprocal of the positive power.', 'd',
              f'A is false ({b}{sup(-2)} = 1/{b * b} > 0); R is true.')


def c2s2_case(r):
    n = r.randint(3, 6)
    return {'stem': (f'A virus particle is about 10{sup(-7)} m long and a grain of sand about 10{sup(-3)} m. '
                     f'(i) How many times longer is the sand grain? (ii) Write 10{sup(-n)} m as a decimal. (iii) Which is larger: 10{sup(-n)} or 10{sup(-n - 1)}? Explain.'),
            'answer': f'(i) 10⁴ = 10000 times (ii) 0.{"0" * (n - 1)}1 m (iii) 10{sup(-n)}',
            'key': f'(i) 10{sup(-3)} ÷ 10{sup(-7)} = 10⁴ (ii) {n} decimal places (iii) 10{sup(-n)} = 10 × 10{sup(-n - 1)}.'}


# st3 Standard form for very large / small numbers

def _sf(r):
    m = round(r.uniform(1.1, 9.9), r.choice([1, 2]))
    e = r.randint(4, 9)
    return m, e


def c2s3_usual(r):
    m, e = _sf(r)
    val = round(m * 10 ** e)
    return {'stem': f'Write {num(m)} × 10{sup(e)} in usual form.', 'answer': f'{val:,}'.replace(',', ' '),
            'key': f'Move the decimal point {e} places right: {val:,}.'.replace(',', ' '),
            'distractors': [f'{round(m * 10 ** (e - 1)):,}'.replace(',', ' '), f'{round(m * 10 ** (e + 1)):,}'.replace(',', ' '), f'{num(m)}{"0" * e}']}


def c2s3_small(r):
    digits = r.randint(11, 99)
    zeros = r.randint(3, 7)
    s = '0.' + '0' * zeros + str(digits)
    e = -(zeros + 1)
    m = digits / 10
    return {'stem': f'Write {s} in standard form.', 'answer': f'{num(m)} × 10{sup(e)}',
            'key': f'Move the point {zeros + 1} places right to get {num(m)}, so the exponent is {e}.',
            'distractors': [f'{num(m)} × 10{sup(e + 1)}', f'{digits} × 10{sup(e - 1)}', f'{num(m)} × 10{sup(-e)}']}


def c2s3_why_not(r):
    a = r.randint(11, 99)
    e = r.randint(3, 8)
    return {'stem': f'Why is {a} × 10{sup(e)} not in standard form? Write it correctly.',
            'answer': f'{num(a / 10)} × 10{sup(e + 1)}', 'key': 'In standard form the number before the power of 10 must be at least 1 and less than 10.'}


def c2s3_compare(r):
    a = round(r.uniform(1.5, 9.5), 1)
    e = r.randint(3, 6)
    k = r.choice([2, 4, 5])
    b = a * 10 / k
    while b >= 10:
        k += 1
        b = a * 10 / k
    return {'stem': f'Which is larger, {num(a)} × 10{sup(-e)} or {num(b, 3)} × 10{sup(-e - 1)}, and by what factor?',
            'answer': f'{num(a)} × 10{sup(-e)}, {k} times',
            'key': f'{num(a)} × 10{sup(-e)} = {num(a * 10)} × 10{sup(-e - 1)}; {num(a * 10)} ÷ {num(b, 3)} = {k}.'}


def c2s3_light(r):
    d = r.choice([(1.5, 8, 'the Sun'), (3.84, 5, 'the Moon'), (2.28, 8, 'Mars at its average distance')])
    m, e, body = d
    t = m * 10 ** e / 3e5
    return {'stem': f'The distance from Earth to {body} is about {num(m)} × 10{sup(e)} km. Light travels at 3 × 10⁵ km/s. How long does light take to travel this distance? Give the answer in seconds.',
            'answer': f'≈ {t:.3g} s', 'key': f'{num(m)} × 10{sup(e)} ÷ (3 × 10⁵) = {num(m / 3, 3)} × 10{sup(e - 5)} ≈ {t:.3g} s.'}


def c2s3_atoms(r):
    mass, el = r.choice([(1.67, 'hydrogen'), (2.66, 'oxygen'), (1.99, 'carbon')])
    n = 1e-3 / (mass * 1e-27) / 1e23
    return {'stem': f'One {el} atom has a mass of about {mass} × 10⁻²⁷ kg. About how many atoms are there in 1 g of {el}? Give your answer in standard form to 2 significant figures.',
            'answer': f'≈ {n:.1f} × 10²³', 'key': f'1 g = 10⁻³ kg; 10⁻³ ÷ ({mass} × 10⁻²⁷) = {1 / mass:.3f} × 10²⁴ ≈ {n:.1f} × 10²³.'}


def c2s3_population(r):
    country, pop = r.choice([('India', 1.43e9), ('China', 1.41e9), ('the USA', 3.35e8), ('Indonesia', 2.78e8), ('Japan', 1.24e8)])
    m = pop / 10 ** int(math.log10(pop))
    e = int(math.log10(pop))
    return {'stem': f'The population of {country} is about {round(pop):,}. Write this number in standard form, rounded to 3 significant figures.'.replace(',', ' '),
            'answer': f'{m:.2f} × 10{sup(e)}', 'key': f'Place the point after the first digit: {m:.2f}; count {e} places.',
            'distractors': [f'{m:.2f} × 10{sup(e + 1)}', f'{m * 10:.1f} × 10{sup(e - 1)}', f'{m:.2f} × 10{sup(e - 1)}']}


def c2s3_ar(r):
    m, e = _sf(r)
    return ar(f'{num(m)} × 10{sup(e)} is written in standard form.', 'In standard form, the number before the power of 10 lies between 1 and 10 (1 ≤ a < 10).', 'a', 'R gives the condition A satisfies.')


def c2s3_product(r):
    a, b = round(r.uniform(2, 9), 1), round(r.uniform(2, 9), 1)
    e1, e2 = r.randint(3, 8), -r.randint(2, 6)
    p = a * b
    e = e1 + e2
    if p >= 10:
        p /= 10
        e += 1
    return {'stem': f'Find ({num(a)} × 10{sup(e1)}) × ({num(b)} × 10{sup(e2)}) and give the answer in standard form.',
            'answer': f'{num(round(p, 3), 3)} × 10{sup(e)}', 'key': f'{num(a)} × {num(b)} = {num(a * b, 3)}; exponents {e1} + ({e2}); adjust so 1 ≤ a < 10.'}


# ---------------- ch03 A Story of Numbers ----------------
# st1 Evolution of number systems and place value

ROMAN = [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]


def roman(n):
    s = ''
    for v, sy in ROMAN:
        while n >= v:
            s += sy
            n -= v
    return s


def c3s1_roman_read(r):
    n = r.randint(11, 89)
    return {'stem': f'What is the value of the Roman numeral {roman(n)}?', 'answer': str(n),
            'key': f'{roman(n)} = {n}.', 'distractors': num_distractors(n, n + 10, n - 2, n + 4)}


def c3s1_roman_write(r):
    n = r.randint(1500, 2999)
    return {'stem': f'Write {n} in Roman numerals.', 'answer': roman(n), 'key': f'{n} = {roman(n)}.',
            'distractors': [roman(n + 10), roman(n - 1), roman(n + 100)]}


def c3s1_roman_add(r):
    a = r.randint(1900, 1990)
    b = r.randint(10, 90)
    return {'stem': f'Convert {roman(a)} to Hindu-Arabic numerals, add {b}, and write the answer back in Roman numerals.',
            'answer': f'{roman(a + b)}', 'key': f'{roman(a)} = {a}; {a} + {b} = {a + b} = {roman(a + b)}.'}


FACTS_NUM = [
    ('Which Indian mathematician first wrote down rules for calculating with zero?', 'Brahmagupta', ['Aryabhata', 'Bhaskara II', 'Ramanujan'], 'Brahmagupta, Brahmasphutasiddhanta (628 CE).'),
    ('The place-value system with zero that we use today first developed in …', 'India', ['Egypt', 'Rome', 'Greece'], 'The Indian place-value system was carried to the world through Arab scholars.'),
    ('How many different symbols does our place-value system need to write every whole number?', '10', ['9', '26', 'Infinitely many'], 'The digits 0 to 9.'),
    ('In the numeral 7 042, what is the place value of 7?', '7000', ['7', '700', '70 000'], '7 is in the thousands place.'),
    ('Which ancient people used a base-60 (sexagesimal) number system?', 'Babylonians', ['Romans', 'Egyptians', 'Mayans'], 'Base 60 survives in 60 minutes and 360°.'),
    ('The Maya number system used base …', '20', ['10', '60', '12'], 'The Maya counted in twenties (vigesimal).'),
    ('Which Roman numeral has the largest value?', 'M', ['D', 'C', 'L'], 'M = 1000.'),
]


def c3s1_fact(r):
    q, c, w, k = r.choice(FACTS_NUM)
    return mcq(q, c, w, k, r)


def c3s1_explain(r):
    n = r.choice([3888, 2888, 1888, 3999])
    return {'stem': f'Write {n} in Roman numerals, then explain in two lines why the place-value system makes calculation easier.',
            'answer': roman(n), 'key': f'{n} = {roman(n)} ({len(roman(n))} symbols). In place value, a digit\'s value depends on its position, so ten symbols and a zero write any number and column arithmetic works.'}


def c3s1_base(r):
    b = r.choice([2, 5])
    n = r.randint(9, 60)
    digits = ''
    m = n
    while m:
        digits = str(m % b) + digits
        m //= b
    return {'stem': f'In a base-{b} system only the digits 0 to {b - 1} are used and each place is worth {b} times the place to its right. Write {n} in base {b}, and check your answer.',
            'answer': digits, 'key': f'{n} = ' + ' + '.join(f'{d} × {b}{sup(i)}' for i, d in enumerate(reversed(digits)) if d != '0') + f' → {digits}.'}


def c3s1_ar(r):
    return ar('In 5 505 the three 5s have different values.', 'In a place-value system the value of a digit depends on its position.', 'a', 'R explains A: 5000, 500 and 5.')


def c3s1_place(r):
    n = r.randint(10000, 999999)
    s = str(n)
    i = r.randint(0, len(s) - 2)
    d = int(s[i])
    while d == 0:
        i = (i + 1) % (len(s) - 1)
        d = int(s[i])
    pv = d * 10 ** (len(s) - 1 - i)
    return {'stem': f'What is the place value of the digit {d} (at position {i + 1} from the left) in {n}?', 'answer': str(pv),
            'key': f'{d} × 10{sup(len(s) - 1 - i)} = {pv}.', 'distractors': num_distractors(pv, d, pv * 10, pv // 10 if pv >= 10 else pv + 5)}


# st2 Rational numbers: representation and properties

def c3s2_define(r):
    return mcq('Which of the following is NOT a rational number?', '√2', [r.choice(['0', '−3']), r.choice(['3/7', '−5/9']), r.choice(['0.75', '2.5'])],
               '√2 cannot be written as p/q with integers p, q (q ≠ 0); the others can.', r)


def c3s2_add(r):
    a, b = r.randint(1, 7), r.choice([3, 4, 5, 6, 8])
    c, d = r.randint(1, 9), r.choice([6, 9, 10, 12])
    return {'stem': f'Compute {a}/{b} + (−{c}/{d}).', 'answer': frac(a * d - c * b, b * d),
            'key': f'LCM method: {a}/{b} − {c}/{d} = {frac(a * d - c * b, b * d)}.',
            'distractors': [frac(a - c, b + d), frac(a * d + c * b, b * d), frac(c * b - a * d, b * d)]}


def c3s2_closure(r):
    return {'stem': 'Explain in one line, with an example, why rational numbers are closed under subtraction but natural numbers are not.',
            'answer': 'e.g. 2 − 5 = −3 is not natural, but the difference of two rationals is always rational.',
            'key': 'Example for naturals failing (1 mark) + p/q − r/s = (ps − rq)/qs is rational (1 mark).'}


def c3s2_assoc(r):
    a, b, c = r.choice([(8, 4, 2), (12, 6, 3), (16, 4, 2), (18, 6, 3)])
    return {'stem': 'Give an example showing that division of rational numbers is not associative.',
            'answer': f'({a} ÷ {b}) ÷ {c} = {frac(a, b * c)} but {a} ÷ ({b} ÷ {c}) = {frac(a * c, b)}',
            'key': 'Any correct pair of computations showing different results.'}


def c3s2_inverses(r):
    p, q = r.randint(2, 9), r.randint(2, 11)
    if p == q:
        q += 1
    return {'stem': f'Find the additive inverse and the multiplicative inverse of −{p}/{q}, then multiply the two inverses.',
            'answer': f'{p}/{q}; −{q}/{p}; product −1',
            'key': f'Additive inverse {p}/{q}; reciprocal −{q}/{p}; ({p}/{q}) × (−{q}/{p}) = −1.'}


def c3s2_distrib(r):
    a, b = r.randint(2, 9), r.randint(3, 9)
    c, d, e = r.randint(1, 7), r.randint(1, 7), r.choice([6, 8, 10, 12])
    return {'stem': f'Use the distributive property to evaluate {a}/{b} × (−{c}/{e}) + {a}/{b} × {c + d}/{e}.',
            'answer': frac(a * d, b * e), 'key': f'{a}/{b} × (−{c}/{e} + {c + d}/{e}) = {a}/{b} × {d}/{e} = {frac(a * d, b * e)}.'}


def c3s2_tank(r):
    full = r.choice([(3, 5), (2, 3), (3, 4), (5, 6)])
    used = r.choice([(1, 4), (1, 6), (1, 5)])
    add = r.choice([(2, 15), (1, 10), (1, 12)])
    cap = r.choice([600, 1200, 1800, 2400])
    from fractions import Fraction as Fr
    left = Fr(*full) - Fr(*used) + Fr(*add)
    litres = left * cap
    return {'stem': f'A water tank of capacity {cap} litres was {full[0]}/{full[1]} full. {used[0]}/{used[1]} of the capacity was used, then {add[0]}/{add[1]} of the capacity was added. What fraction of the tank is now full, and how many litres is that?',
            'answer': f'{left.numerator}/{left.denominator}; {num(float(litres))} litres',
            'key': f'{full[0]}/{full[1]} − {used[0]}/{used[1]} + {add[0]}/{add[1]} = {left.numerator}/{left.denominator}; × {cap} = {num(float(litres))} L.'}


def c3s2_mixed(r):
    a, b = r.choice([(2, 3), (3, 4), (4, 5)])
    c, d = r.choice([(6, 7), (5, 9), (3, 8)])
    from fractions import Fraction as Fr
    v = Fr(a, b) * Fr(-c, d) + Fr(-1, 2) - Fr(1, 4) / Fr(-1, 2)
    return {'stem': f'Simplify {a}/{b} × (−{c}/{d}) + (−1/2) − 1/4 ÷ (−1/2).',
            'answer': frac(v.numerator, v.denominator),
            'key': f'BODMAS: {frac((Fr(a, b) * Fr(-c, d)).numerator, (Fr(a, b) * Fr(-c, d)).denominator)} − 1/2 + 1/2 = {frac(v.numerator, v.denominator)}.'}


def c3s2_ar(r):
    return ar('0 is a rational number.', '0 can be written as 0/1, with integers in the numerator and a non-zero denominator.', 'a', 'R shows why A is true.')


def c3s2_standard(r):
    p, q = r.randint(2, 9), r.randint(2, 9)
    k = r.randint(2, 6)
    return {'stem': f'Write −{p * k}/{q * k} in standard form (lowest terms, positive denominator).'.replace('−', '') if r.random() < 0.3 else f'Write {p * k}/(−{q * k}) in standard form.',
            'answer': frac(-p, q) if True else '', 'key': f'Divide by the HCF {k} and move the sign to the numerator.',
            'distractors': [frac(p, q), f'{p}/(−{q})', frac(-q, p)]}


# st3 Rational numbers on the number line; numbers between two rationals

def c3s3_count(r):
    a, b = r.choice([(1, 3), (2, 5), (1, 4), (3, 7)])
    c, d = a + 1, b
    return mcq(f'How many rational numbers lie between {a}/{b} and {c}/{d}?', 'Infinitely many', ['None', 'Exactly one', f'Exactly {d - 1}'],
               'Between any two rationals there are infinitely many rationals (keep taking means).', r)


def c3s3_mean(r):
    a, b, c, d = r.choice([(1, 3, 1, 2), (1, 4, 1, 3), (2, 5, 1, 2), (3, 4, 4, 5)])
    from fractions import Fraction as Fr
    m = (Fr(a, b) + Fr(c, d)) / 2
    return {'stem': f'Find a rational number between {a}/{b} and {c}/{d} using their mean, and explain why the mean always works.',
            'answer': f'{m.numerator}/{m.denominator}', 'key': 'The mean of two numbers is always between them; (x + y)/2 is rational when x, y are.'}


def c3s3_order_neg(r):
    a, b = r.choice([(3, 4), (2, 3), (5, 6), (4, 5)])
    c, d = 1, 2
    return {'stem': f'A student says −{a}/{b} lies to the right of −{c}/{d} on the number line because {a} > {c}. Correct the student.',
            'answer': f'−{a}/{b} < −{c}/{d}; it lies to the LEFT.', 'key': f'−{a}/{b} = {num(round(-a / b, 2))} is further from 0 on the negative side than −0.5.'}


def c3s3_locate(r):
    q = r.choice([3, 4, 5, 6])
    p = r.randint(q + 1, 3 * q - 1)
    if p % q == 0:
        p += 1
    w = p // q
    return {'stem': f'Between which two integers does {p}/{q} lie? Where is it on a number line in which each unit is divided into {q} equal parts?',
            'answer': f'Between {w} and {w + 1}, at the {p - w * q}th mark after {w}',
            'key': f'{p}/{q} = {w} {p - w * q}/{q}.'}


def c3s3_three(r):
    a, b = r.choice([(-2, 5), (-1, 3), (1, 5), (-3, 4)])
    c, d = r.choice([(1, 5), (2, 3), (3, 5), (1, 4)])
    return {'stem': f'Write three rational numbers between {frac(a, b)} and {frac(c, d)}.',
            'answer': 'Any three correct values', 'key': f'e.g. convert to a common denominator {b * d * 2}: {frac(a, b)} = {a * d * 2}/{b * d * 2}, {frac(c, d)} = {c * b * 2}/{b * d * 2}; any three numerators strictly between.'}


def c3s3_five(r):
    a, b = r.choice([(3, 5), (1, 4), (2, 7), (5, 9)])
    return {'stem': f'Write five rational numbers between {a}/{b} and {a + 1}/{b} in increasing order.',
            'answer': ' < '.join(f'{6 * a + i}/{6 * b}' for i in range(1, 6)),
            'key': f'Multiply numerator and denominator by 6: {6 * a}/{6 * b} and {6 * a + 6}/{6 * b}; the numerators {6 * a + 1} to {6 * a + 5} fit between.'}


def c3s3_compare(r):
    pairs = [(-3, 5, -2, 3), (5, 8, 7, 12), (-7, 9, -4, 5), (2, 7, 3, 10), (-5, 6, -7, 9)]
    a, b, c, d = r.choice(pairs)
    big = frac(a, b) if a / b > c / d else frac(c, d)
    return {'stem': f'Which is greater: {frac(a, b)} or {frac(c, d)}?', 'answer': big,
            'key': f'Cross-multiply with positive denominators: {a} × {d} = {a * d}, {c} × {b} = {c * b}.',
            'distractors': [frac(c, d) if big == frac(a, b) else frac(a, b), 'They are equal', 'Cannot be compared']}


def c3s3_ar(r):
    return ar('There is no rational number between 1/3 and 1/2.', 'Between two consecutive integers there is no integer.', 'd',
              'A is false (5/12 lies between them); R is true but about integers, not rationals.')


def c3s3_temps(r):
    t = sorted(r.sample([-7, -5, -3, -1, 2, 4, -9], 4))
    cities = r.sample(['Leh', 'Kargil', 'Shimla', 'Srinagar', 'Manali', 'Gulmarg'], 4)
    data = list(zip(cities, t))
    r.shuffle(data)
    txt = ', '.join(f'{c} {num(v)}/2 °C'.replace('/2 °C', ' °C') for c, v in data)
    return {'stem': f'Night temperatures (°C) on a winter day: {", ".join(f"{c} {num(v / 2)}" for c, v in data)}. Mark them on a number line and list the cities from coldest to warmest. Which two cities differ by the most?',
            'answer': ', '.join(c for c, v in sorted(data, key=lambda x: x[1])),
            'key': f'Order by value; the largest difference is between the coldest and warmest: {num((t[-1] - t[0]) / 2)} °C.'}


# ---------------- ch04 Quadrilaterals ----------------

QUAD = {
    'square': 'four equal sides and four right angles',
    'rectangle': 'opposite sides equal and four right angles',
    'rhombus': 'four equal sides, opposite angles equal',
    'parallelogram': 'both pairs of opposite sides parallel',
    'trapezium': 'exactly one pair of parallel sides',
    'kite': 'two pairs of equal adjacent sides',
}


def c4s1_name(r):
    k = r.choice(list(QUAD))
    others = [x for x in QUAD if x != k]
    return mcq(f'A quadrilateral with {QUAD[k]} is called a …', k.capitalize(), [o.capitalize() for o in r.sample(others, 3)], f'Definition of a {k}.', r)


def c4s1_every(r):
    a, b, why = r.choice([('square', 'rhombus', 'both have four equal sides; a square also needs four right angles'),
                          ('square', 'rectangle', 'both have four right angles; a square also needs four equal sides'),
                          ('rectangle', 'parallelogram', 'a rectangle has both pairs of opposite sides parallel; a parallelogram need not have right angles'),
                          ('rhombus', 'parallelogram', 'a rhombus has opposite sides parallel; a parallelogram need not have all sides equal')])
    return {'stem': f'In one line: why is every {a} a {b}, but not every {b} a {a}?', 'answer': why,
            'key': f'Shared property named (1 mark) and the extra condition the {a} needs (1 mark).'}


def c4s1_identify(r):
    a, b = r.choice([(5, 8), (6, 9), (4, 7), (7, 10)])
    return {'stem': f'A quadrilateral has sides {a}, {a}, {b}, {b} cm with the equal sides adjacent; its diagonals are unequal and one bisects the other at right angles. Name it.',
            'answer': 'Kite', 'key': 'Two pairs of equal adjacent sides with perpendicular diagonals: kite.',
            'distractors': ['Rhombus', 'Parallelogram', 'Rectangle']}


def c4s1_diagonals(r):
    k, prop = r.choice([('Square', 'are equal and bisect each other at right angles'), ('Rhombus', 'bisect each other at right angles but are not equal'),
                        ('Rectangle', 'are equal and bisect each other, but are not perpendicular'), ('Parallelogram', 'bisect each other but are neither equal nor perpendicular')])
    others = [x for x in ['Square', 'Rhombus', 'Rectangle', 'Parallelogram', 'Kite'] if x != k]
    return mcq(f'Name the quadrilateral whose diagonals {prop}.', k, r.sample(others, 3), f'{k}.', r)


def c4s1_venn(r):
    return {'stem': 'Draw a family tree (or Venn diagram) showing how square, rectangle, rhombus, parallelogram, trapezium and kite are related. Use it to decide: is a square a kite? Justify.',
            'answer': 'Yes, a square is a kite.', 'key': 'Diagram with square inside rectangle and rhombus, both inside parallelogram (2 marks). A square has two pairs of equal adjacent sides, so it is a kite (1 mark).'}


def c4s1_ar(r):
    return ar('Every square is a rhombus.', 'A rhombus has four equal sides, and a square has four equal sides.', 'a', 'R gives the defining property shared.')


def c4s1_kite_rhombus(r):
    return {'stem': 'A kite has two pairs of equal ADJACENT sides. Explain why a rhombus is a special kind of kite.',
            'answer': 'In a rhombus all four sides are equal, so both pairs of adjacent sides are equal.', 'key': 'Uses the definition of a kite and the rhombus\'s four equal sides.'}


def c4s1_coord(r):
    a, b = r.randint(2, 6), r.randint(1, 4)
    pts = [(0, 0), (a, 0), (a + b, a), (b, a)]
    return {'stem': f'Plot A(0, 0), B({a}, 0), C({a + b}, {a}) and D({b}, {a}). Name the quadrilateral ABCD and justify using side lengths or parallel sides.',
            'answer': 'Parallelogram (AB ∥ DC and AD ∥ BC)' if b * b + a * a != a * a else 'Rhombus',
            'key': f'AB and DC are horizontal of length {a}; AD and BC have the same slope; opposite sides parallel → parallelogram. AD = √({b * b + a * a}) {"= AB, so rhombus" if b * b + a * a == a * a else "≠ AB"}.'}


# st2 Angle-sum and exterior angle properties

def c4s2_sum(r):
    n = r.choice([5, 6, 7, 8, 9, 10, 12])
    names = {5: 'pentagon', 6: 'hexagon', 7: 'heptagon', 8: 'octagon', 9: 'nonagon', 10: 'decagon', 12: 'dodecagon'}
    s = (n - 2) * 180
    return {'stem': f'What is the sum of the interior angles of a {names[n]}?', 'answer': f'{s}°',
            'key': f'(n − 2) × 180° = {n - 2} × 180° = {s}°.', 'distractors': [f'{n * 180}°', f'{(n - 1) * 180}°', '360°']}


def c4s2_missing(r):
    a, b, c = r.randint(60, 120), r.randint(60, 120), r.randint(50, 110)
    x = 360 - a - b - c
    if not 30 < x < 170:
        a, b, c = 80, 95, 100
        x = 85
    return {'stem': f'The angles of a quadrilateral are {a}°, {b}°, {c}° and x. Find x.', 'answer': f'{x}°',
            'key': f'x = 360° − ({a} + {b} + {c})° = {x}°.', 'distractors': [f'{180 - (a + b + c) % 180}°', f'{x + 10}°', f'{360 - a - b}°']}


def c4s2_regular_ext(r):
    n = r.choice([5, 6, 8, 9, 10, 12, 15, 18, 20, 24, 30, 36])
    return {'stem': f'Each exterior angle of a regular polygon is {360 // n}°. How many sides does it have?', 'answer': str(n),
            'key': f'Exterior angles sum to 360°: 360 ÷ {360 // n} = {n}.', 'distractors': num_distractors(n, n + 2, 180 // (360 // n) if 180 % (360 // n) == 0 else n - 1, n * 2)}


def c4s2_ratio(r):
    rs = r.choice([(2, 3, 4, 6), (1, 2, 3, 4), (3, 4, 5, 6), (2, 3, 5, 8), (1, 3, 5, 6), (4, 5, 6, 9)])
    k = 360 / sum(rs)
    angs = [round(x * k, 1) for x in rs]
    trap = any(abs(angs[i] + angs[(i + 1) % 4] - 180) < 1e-6 for i in range(4))
    return {'stem': f'The angles of a quadrilateral, taken in order, are in the ratio {" : ".join(map(str, rs))}. Find the angles. Can this quadrilateral be a trapezium? Explain.',
            'answer': ', '.join(f'{num(a)}°' for a in angs) + ('; yes' if trap else '; no'),
            'key': f'Each part = 360 ÷ {sum(rs)} = {num(k)}°. A trapezium needs two adjacent (co-interior) angles adding to 180°: {"found" if trap else "none do"}.'}


def c4s2_explain(r):
    return {'stem': r.choice(['Using one diagonal, explain in one line why the angle sum of a quadrilateral is 360°.',
                              'Explain, using triangles, why the interior angles of a pentagon add up to 540°.']),
            'answer': 'A diagonal (or diagonals from one vertex) splits it into triangles, each with angle sum 180°.',
            'key': 'Number of triangles × 180°.'}


def c4s2_ext_sum(r):
    return {'stem': 'Why is the sum of the exterior angles of ANY convex polygon 360°, whatever the number of sides?',
            'answer': 'Walking once around the polygon you turn through each exterior angle and finish facing the start direction: one full turn.',
            'key': 'Full-turn argument, or n × 180° − (n − 2) × 180° = 360°.'}


def c4s2_interior_regular(r):
    n = r.choice([5, 6, 8, 9, 10, 12])
    return {'stem': f'Find the measure of each interior angle of a regular polygon with {n} sides.', 'answer': f'{num((n - 2) * 180 / n)}°',
            'key': f'({n} − 2) × 180 ÷ {n} = {num((n - 2) * 180 / n)}°, or 180° − 360°/{n}.',
            'distractors': [f'{num(360 / n)}°', f'{(n - 2) * 180}°', f'{num(180 - 180 / n)}°']}


def c4s2_possible(r):
    a = r.choice([100, 110, 130, 135, 145, 155, 165])
    ok = 360 % (180 - a) == 0
    return {'stem': f'Is it possible to have a regular polygon each of whose interior angles is {a}°? Justify.',
            'answer': f'{"Yes, " + str(360 // (180 - a)) + " sides" if ok else "No"}',
            'key': f'Exterior angle = {180 - a}°; 360 ÷ {180 - a} = {360 / (180 - a):.2f} {"is a whole number" if ok else "is not a whole number"}.'}


def c4s2_ar(r):
    return ar('Each exterior angle of a regular hexagon is 60°.', 'The exterior angles of any polygon add up to 360°.', 'a', '360° ÷ 6 = 60°.')


def c4s2_tile(r):
    who = name(r)
    a = r.randint(65, 85)
    b = r.randint(95, 120)
    return {'stem': f'{who} cuts a quadrilateral tile with angles {a}°, {b}°, {180 - a}° and x°. Find x and say whether the tile could be a parallelogram.',
            'answer': f'x = {360 - b - 180}°; ' + ('parallelogram possible' if 360 - b - 180 == b else 'not a parallelogram (opposite angles not equal)'),
            'key': f'x = 360 − {a} − {b} − {180 - a} = {180 - b}°. A parallelogram needs both pairs of opposite angles equal.'}


# st3 Parallelogram family: sides, angles, diagonals

def c4s3_prop(r):
    return mcq('Which diagonal property does a rectangle have that a general parallelogram does not?', 'Its diagonals are equal in length',
               ['Its diagonals bisect each other', 'Its diagonals are parallel', 'Its diagonals bisect each other at right angles'],
               'Both bisect each other; only the rectangle\'s diagonals are always equal.', r)


def c4s3_opposite(r):
    return {'stem': 'In one line: why are the opposite angles of a parallelogram equal?',
            'answer': 'Adjacent angles are co-interior angles between parallel lines, so each pair adds to 180°; two angles supplementary to the same angle are equal.',
            'key': 'Uses co-interior angles (1 mark) and the conclusion (1 mark).'}


def c4s3_counter(r):
    return {'stem': "A student says 'a quadrilateral with equal diagonals must be a rectangle.' Give a counter-example.",
            'answer': 'An isosceles trapezium (or a kite with equal diagonals).', 'key': 'Any correct non-rectangle with equal diagonals.'}


def c4s3_angles(r):
    a = r.randint(48, 85)
    return {'stem': f'One angle of a parallelogram is {a}°. Find the other three angles.', 'answer': f'{180 - a}°, {a}°, {180 - a}°',
            'key': f'Adjacent angles are supplementary: 180 − {a} = {180 - a}; opposite angles are equal.',
            'distractors': [f'{a}°, {a}°, {360 - 3 * a}°', f'{90 - a if a < 90 else a - 90}°, {a}°, {180 - a}°', f'{180 - a}°, {180 - a}°, {a}°']}


def c4s3_expr(r):
    a, b = r.randint(2, 5), r.randint(10, 40)
    c = r.randint(1, a - 1) if a > 1 else 1
    x = r.randint(10, 30)
    d = a * x + b - c * x
    return {'stem': f'In parallelogram PQRS, ∠P = ({a}x + {b})° and ∠R = ({c}x + {d})°. Find x and all four angles.',
            'answer': f'x = {x}; ∠P = ∠R = {a * x + b}°, ∠Q = ∠S = {180 - a * x - b}°',
            'key': f'Opposite angles equal: {a}x + {b} = {c}x + {d} → x = {x}; adjacent = 180 − {a * x + b}.'}


def c4s3_diag(r):
    d1, d2 = r.randint(6, 20), r.randint(6, 20)
    if d1 == d2:
        d2 += 2
    side = math.sqrt((d1 / 2) ** 2 + (d2 / 2) ** 2)
    nice = abs(side - round(side)) < 1e-9
    if not nice:
        d1, d2 = r.choice([(6, 8), (10, 24), (16, 12), (18, 24), (16, 30)])
        side = math.sqrt((d1 / 2) ** 2 + (d2 / 2) ** 2)
    return {'stem': f'The diagonals of a rhombus are {d1} cm and {d2} cm. Find the length of each side.', 'answer': f'{num(side)} cm',
            'key': f'Diagonals bisect at right angles: side = √({d1 // 2}² + {d2 // 2}²) = {num(side)} cm.'}


def c4s3_rect_diag(r):
    l, b = r.choice([(8, 6), (12, 5), (15, 8), (24, 7), (12, 9)])
    return {'stem': f'The diagonals of rectangle ABCD meet at O. If AB = {l} cm and BC = {b} cm, find OA.', 'answer': f'{num(math.hypot(l, b) / 2)} cm',
            'key': f'AC = √({l}² + {b}²) = {num(math.hypot(l, b))}; diagonals of a rectangle are equal and bisect each other, so OA = {num(math.hypot(l, b) / 2)} cm.'}


def c4s3_ar(r):
    return ar('The diagonals of a rhombus bisect each other.', 'A rhombus is a parallelogram.', 'a', 'Every parallelogram\'s diagonals bisect each other; R explains A.')


def c4s3_perimeter(r):
    a, b = r.randint(4, 15), r.randint(4, 15)
    who = name(r)
    return {'stem': f'{who} uses {2 * (a + b)} cm of ribbon to border a parallelogram-shaped card exactly once. One side is {a} cm. Find the other sides.',
            'answer': f'{a} cm, {b} cm, {a} cm, {b} cm', 'key': f'Opposite sides equal: 2({a} + x) = {2 * (a + b)} → x = {b}.'}


def c4s3_bisector(r):
    a = r.choice([60, 70, 80, 100, 110, 120])
    return {'stem': f'In parallelogram ABCD, ∠A = {a}°. The bisectors of ∠A and ∠B meet at P. Find ∠APB and explain why the answer does not depend on ∠A.',
            'answer': '90°', 'key': f'∠A + ∠B = 180°, so half of each adds to 90°; in triangle APB, ∠APB = 180° − 90° = 90°.'}


# st4 Constructing quadrilaterals from given data

def c4s4_min(r):
    return mcq('What is the minimum number of independent measurements needed to construct a unique quadrilateral?', 'Five', ['Three', 'Four', 'Six'],
               'Four sides alone do not fix the shape; a fifth measurement (e.g. a diagonal) is needed.', r)


def c4s4_why_four(r):
    return {'stem': 'Explain why four side lengths alone are not enough to construct a unique quadrilateral.',
            'answer': 'A quadrilateral with fixed sides can flex (e.g. a square can be pushed into a rhombus); a diagonal or angle fixes it.',
            'key': 'Flexing argument or two different shapes with the same four sides.'}


def c4s4_steps(r):
    p, q, s, d = r.randint(4, 7), r.randint(4, 7), r.randint(4, 7), r.randint(6, 9)
    return {'stem': f'Write the steps of construction for quadrilateral ABCD with AB = {p} cm, BC = {q} cm, CD = {s} cm, DA = {r.randint(4, 7)} cm and AC = {d} cm.',
            'answer': 'Draw triangle ABC from three sides, then triangle ACD on the other side of AC; join.',
            'key': f'Construct ΔABC (AB = {p}, BC = {q}, AC = {d}); with centre C radius {s} and centre A radius DA cut arcs on the other side of AC to get D; join CD and DA.'}


def c4s4_possible(r):
    a, b = r.randint(3, 5), r.randint(3, 5)
    d = a + b + r.randint(1, 3)
    return {'stem': f'Can a quadrilateral ABCD be constructed with AB = {a} cm, BC = {b} cm and diagonal AC = {d} cm? Explain.',
            'answer': 'No', 'key': f'Triangle ABC would need AB + BC > AC, but {a} + {b} = {a + b} < {d}.',
            'distractors': ['Yes', 'Only if ABCD is a square', 'Only if CD = AC']}


def c4s4_special(r):
    k, data = r.choice([('rhombus', 'side 5 cm and one diagonal 8 cm'), ('square', 'diagonal 6 cm'), ('rectangle', 'sides 5 cm and 3 cm'),
                        ('parallelogram', 'sides 6 cm and 4 cm and the angle between them 60°')])
    return {'stem': f'Only two or three measurements are given for a {k}: {data}. Explain why these are enough to construct it.',
            'answer': f'The {k}\'s own properties supply the other measurements.', 'key': f'e.g. equal sides / right angles / bisecting diagonals of a {k} fill in the missing data.'}


def c4s4_ar(r):
    return ar('A square can be constructed if only the length of its diagonal is known.', 'The diagonals of a square are equal and bisect each other at right angles.', 'a',
              'Draw the two equal perpendicular bisecting diagonals and join their ends.')


def c4s4_case(r):
    w, h = r.randint(5, 9), r.randint(3, 6)
    return {'stem': (f'A carpenter wants a rectangular frame {w} dm by {h} dm. He measures the four sides correctly but the frame still looks slanted. '
                     f'(i) Why can the frame still be slanted? (ii) What single measurement should he check, and what should it read? (iii) Name the property of rectangles this uses.'),
            'answer': f'(i) four sides do not fix the angles (ii) a diagonal, √({w}² + {h}²) ≈ {math.hypot(w, h):.1f} dm (iii) diagonals of a rectangle are equal',
            'key': '1 + 2 + 1 marks.'}


def c4s4_angles_given(r):
    a = r.randint(4, 7)
    return {'stem': f'To construct quadrilateral PQRS you are given PQ = {a} cm, ∠P = 75°, ∠Q = 105°, ∠R = 120°. What extra measurement is needed, and what kind of quadrilateral is formed if PS ∥ QR?',
            'answer': 'One more side, e.g. QR; trapezium', 'key': '∠P + ∠Q = 180° shows PS ∥ QR is consistent: trapezium. Five independent measurements are needed.'}


FAMILIES = {
    # ch01
    S + '01-st1': [F('C1', 'D1', 'mcq', c1s1_which_square), F('C1', 'D2', 'mcq', c1s1_units), F('C2', 'D2', 'explain', c1s1_not_square_explain),
                   F('C2', 'D3', 'mcq', c1s1_ar, kinds=('ar',)), F('C3', 'D1', 'short', c1s1_units_of_square), F('C3', 'D2', 'numerical', c1s1_odd_sum),
                   F('C3', 'D2', 'numerical', c1s1_square_by_pattern), F('C3', 'D3', 'numerical', c1s1_between), F('C3', 'D4', 'multi_step', c1s1_tiles, gap='G7'),
                   F('C4', 'D3', 'explain', c1s1_ends_in_5), F('C4', 'D4', 'multi_step', c1s1_consecutive_squares), F('C4', 'D3', 'case', c1s1_pattern_case)],
    S + '01-st2': [F('C1', 'D2', 'mcq', c1s2_rule), F('C1', 'D1', 'short', c1s2_decimal_root), F('C2', 'D2', 'explain', c1s2_split_root), F('C2', 'D3', 'explain', c1s2_error),
                   F('C2', 'D3', 'mcq', c1s2_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c1s2_pf_root), F('C3', 'D3', 'numerical', c1s2_estimate),
                   F('C3', 'D4', 'multi_step', c1s2_garden, gap='G7'), F('C4', 'D3', 'multi_step', c1s2_multiply_to_square), F('C4', 'D3', 'multi_step', c1s2_subtract),
                   F('C4', 'D5', 'multi_step', c1s2_chairs, gap='G7')],
    S + '01-st3': [F('C1', 'D2', 'mcq', c1s3_which_cube), F('C1', 'D1', 'short', c1s3_units_cube), F('C2', 'D2', 'explain', c1s3_ends_explain), F('C2', 'D3', 'explain', c1s3_double_side),
                   F('C2', 'D3', 'mcq', c1s3_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c1s3_cuberoot_pf), F('C3', 'D3', 'numerical', c1s3_divide_to_cube),
                   F('C3', 'D1', 'short', c1s3_cube_estimate), F('C4', 'D4', 'multi_step', c1s3_cuboids), F('C4', 'D5', 'multi_step', c1s3_hardy)],
    S + '01-st4': [F('C1', 'D2', 'mcq', c1s4_largest), F('C1', 'D1', 'short', c1s4_is_triplet), F('C2', 'D2', 'explain', c1s4_scale), F('C2', 'D3', 'explain', c1s4_not_formula),
                   F('C2', 'D2', 'mcq', c1s4_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c1s4_from_small), F('C3', 'D3', 'numerical', c1s4_member),
                   F('C3', 'D4', 'multi_step', c1s4_ladder, gap='G7'), F('C4', 'D3', 'numerical', c1s4_number_square), F('C4', 'D5', 'multi_step', c1s4_count_squares)],
    # ch02
    S + '02-st1': [F('C1', 'D2', 'mcq', c2s1_div), F('C1', 'D1', 'mcq', c2s1_value), F('C2', 'D2', 'explain', c2s1_pow_pow), F('C2', 'D3', 'explain', c2s1_wrong_base),
                   F('C2', 'D2', 'mcq', c2s1_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c2s1_simplify), F('C3', 'D3', 'numerical', c2s1_mixed),
                   F('C3', 'D4', 'multi_step', c2s1_solve), F('C4', 'D3', 'multi_step', c2s1_algebra), F('C4', 'D4', 'multi_step', c2s1_bacteria, gap='G7'),
                   F('C4', 'D3', 'case', c2s1_paper)],
    S + '02-st2': [F('C1', 'D2', 'short', c2s2_values), F('C1', 'D1', 'mcq', c2s2_reciprocal), F('C2', 'D2', 'explain', c2s2_zero_explain), F('C2', 'D3', 'explain', c2s2_sign),
                   F('C2', 'D3', 'mcq', c2s2_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c2s2_fraction), F('C3', 'D3', 'numerical', c2s2_simplify),
                   F('C4', 'D3', 'numerical', c2s2_solve), F('C4', 'D4', 'case', c2s2_case)],
    S + '02-st3': [F('C1', 'D2', 'short', c2s3_usual), F('C1', 'D1', 'mcq', c2s3_population), F('C2', 'D2', 'explain', c2s3_why_not), F('C2', 'D3', 'explain', c2s3_compare),
                   F('C2', 'D2', 'mcq', c2s3_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c2s3_small), F('C3', 'D3', 'numerical', c2s3_product),
                   F('C3', 'D4', 'multi_step', c2s3_light, gap='G7'), F('C4', 'D4', 'multi_step', c2s3_atoms)],
    # ch03
    S + '03-st1': [F('C1', 'D1', 'short', c3s1_roman_read), F('C1', 'D2', 'mcq', c3s1_fact), F('C2', 'D2', 'explain', c3s1_explain), F('C2', 'D2', 'mcq', c3s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'short', c3s1_roman_write), F('C3', 'D1', 'short', c3s1_place), F('C4', 'D2', 'multi_step', c3s1_roman_add), F('C4', 'D4', 'multi_step', c3s1_base)],
    S + '03-st2': [F('C1', 'D2', 'mcq', c3s2_define), F('C1', 'D1', 'short', c3s2_standard), F('C2', 'D2', 'explain', c3s2_closure), F('C2', 'D3', 'explain', c3s2_assoc),
                   F('C2', 'D2', 'mcq', c3s2_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c3s2_add), F('C3', 'D3', 'numerical', c3s2_inverses),
                   F('C3', 'D4', 'multi_step', c3s2_mixed), F('C4', 'D3', 'multi_step', c3s2_distrib), F('C4', 'D4', 'case', c3s2_tank, gap='G7')],
    S + '03-st3': [F('C1', 'D2', 'mcq', c3s3_count), F('C1', 'D1', 'short', c3s3_compare), F('C2', 'D2', 'explain', c3s3_mean), F('C2', 'D3', 'explain', c3s3_order_neg),
                   F('C2', 'D3', 'mcq', c3s3_ar, kinds=('ar',)), F('C3', 'D2', 'short', c3s3_locate), F('C3', 'D3', 'short', c3s3_three),
                   F('C4', 'D3', 'multi_step', c3s3_five), F('C4', 'D4', 'case', c3s3_temps, gap='G7')],
    # ch04
    S + '04-st1': [F('C1', 'D2', 'mcq', c4s1_name), F('C1', 'D1', 'mcq', c4s1_diagonals), F('C2', 'D2', 'explain', c4s1_every), F('C2', 'D3', 'explain', c4s1_kite_rhombus),
                   F('C2', 'D2', 'mcq', c4s1_ar, kinds=('ar',)), F('C3', 'D3', 'short', c4s1_identify), F('C3', 'D4', 'multi_step', c4s1_coord), F('C4', 'D3', 'long', c4s1_venn)],
    S + '04-st2': [F('C1', 'D2', 'short', c4s2_sum), F('C1', 'D1', 'mcq', c4s2_ar, kinds=('ar',)), F('C2', 'D2', 'explain', c4s2_explain), F('C2', 'D3', 'explain', c4s2_ext_sum),
                   F('C3', 'D2', 'numerical', c4s2_missing), F('C3', 'D3', 'numerical', c4s2_regular_ext), F('C3', 'D1', 'numerical', c4s2_interior_regular),
                   F('C4', 'D3', 'multi_step', c4s2_ratio), F('C4', 'D4', 'explain', c4s2_possible), F('C3', 'D4', 'multi_step', c4s2_tile, gap='G7')],
    S + '04-st3': [F('C1', 'D2', 'mcq', c4s3_prop), F('C2', 'D2', 'explain', c4s3_opposite), F('C2', 'D3', 'explain', c4s3_counter), F('C2', 'D2', 'mcq', c4s3_ar, kinds=('ar',)),
                   F('C3', 'D1', 'numerical', c4s3_angles), F('C3', 'D2', 'numerical', c4s3_perimeter), F('C3', 'D3', 'multi_step', c4s3_expr),
                   F('C3', 'D4', 'numerical', c4s3_diag), F('C4', 'D3', 'numerical', c4s3_rect_diag), F('C4', 'D5', 'multi_step', c4s3_bisector)],
    S + '04-st4': [F('C1', 'D2', 'mcq', c4s4_min), F('C2', 'D2', 'explain', c4s4_why_four), F('C2', 'D3', 'explain', c4s4_special), F('C2', 'D2', 'mcq', c4s4_ar, kinds=('ar',)),
                   F('C3', 'D2', 'long', c4s4_steps), F('C3', 'D1', 'mcq', c4s4_possible), F('C3', 'D3', 'explain', c4s4_angles_given), F('C4', 'D4', 'case', c4s4_case)],
}
