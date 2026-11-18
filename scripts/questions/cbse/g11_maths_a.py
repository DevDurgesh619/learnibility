"""CBSE class 11 maths (NCERT Mathematics XI) families, chapters 1-5, plus shared maths helpers."""
from __future__ import annotations

import math
from fractions import Fraction as Fr

from qbank import F, ar, mcq, num, sup, frac, name, two_names, inr, CITIES  # noqa: F401
from g11_physics_util import polish, sig, g, pool_mcq, pool_ar, pool_txt, term_mcq, tf_mcq  # noqa: F401

S = 'cbse-g11-maths-ch'


# ---------------------------------------------------------------- shared helpers

def fs(x) -> str:
    """Fraction or int to text: 3, −2, 5/7."""
    x = Fr(x)
    return frac(x.numerator, x.denominator)


def sq_split(n: int):
    """n = a² b with b square-free; returns (a, b)."""
    a, b, p = 1, n, 2
    while p * p <= b:
        while b % (p * p) == 0:
            b //= p * p
            a *= p
        p += 1
    return a, b


def surd(x) -> str:
    """√x for a non-negative Fraction x, simplified and rationalised: 2√5/5, 3/2, √3."""
    x = Fr(x)
    if x < 0:
        raise ValueError
    n, d = x.numerator, x.denominator
    a, b = sq_split(n * d)          # √(n/d) = √(nd)/d = a√b/d
    c = Fr(a, d)
    if b == 1:
        return fs(c)
    top = '' if c.numerator == 1 else str(c.numerator)
    s = f'{top}√{b}'
    return s if c.denominator == 1 else f'{s}/{c.denominator}'


def term(c, var: str, first: bool) -> str:
    c = Fr(c)
    if c == 0:
        return ''
    sgn = '−' if c < 0 else '+'
    a = abs(c)
    body = (fs(a) if (a != 1 or not var) else '') + var
    if first:
        return ('−' if c < 0 else '') + body
    return f' {sgn} {body}'


def poly(cs, v='x') -> str:
    """cs from highest power down: [3, 0, -2, 1] -> 3x³ − 2x + 1."""
    n = len(cs) - 1
    out = ''
    for i, c in enumerate(cs):
        p = n - i
        var = '' if p == 0 else (v if p == 1 else v + sup(p))
        t = term(c, var, out == '')
        out += t
    return out or '0'


def lin(a, b, v='x') -> str:
    return poly([a, b], v)


def setstr(xs) -> str:
    xs = list(xs)
    return '{' + ', '.join(fs(x) if isinstance(x, (int, Fr)) else str(x) for x in xs) + '}' if xs else 'φ'


def cplx(a, b) -> str:
    """a + bi with fractions."""
    a, b = Fr(a), Fr(b)
    if b == 0:
        return fs(a)
    ab_ = abs(b)
    if ab_.denominator == 1:
        bi = ('' if ab_ == 1 else fs(ab_)) + 'i'
    else:
        bi = ('' if ab_.numerator == 1 else str(ab_.numerator)) + f'i/{ab_.denominator}'
    if a == 0:
        return ('−' if b < 0 else '') + bi
    return f'{fs(a)} {"−" if b < 0 else "+"} {bi}'


def dis(r, ans: str, cands, k: int = 3):
    out, seen = [], {ans}
    for c in cands:
        if c not in seen:
            out.append(c)
            seen.add(c)
    return out[:max(k, 3)]


def ordn(n: int) -> str:
    if 10 <= n % 100 <= 20:
        return f'{n}th'
    return f'{n}{ {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th") }'


_MINUS = __import__('re').compile(r'(?<![A-Za-z0-9])-(?=[\d(√xyabk])|(?<=[\s(=,:])-(?=\d)')


def _mfix(t):
    return _MINUS.sub('−', t) if isinstance(t, str) else t


def mpolish(families: dict) -> dict:
    """Maths-wide text fix: ASCII hyphen-minus before a number or variable becomes a proper minus sign."""
    from functools import wraps
    for fams in families.values():
        for f in fams:
            if getattr(f.gen, '_mpolished', False):
                continue
            g0 = f.gen

            @wraps(g0)
            def gen(r, _g=g0):
                v = _g(r)
                for k in ('stem', 'answer', 'key'):
                    v[k] = _mfix(v[k])
                if v.get('options'):
                    v['options'] = [_mfix(o) for o in v['options']]
                if v.get('distractors'):
                    v['distractors'] = [_mfix(str(o)) for o in v['distractors']]
                return v
            gen._mpolished = True
            f.gen = gen
    return families


def Q(stem, ans, key, ds=None, **kw):
    d = {'stem': stem, 'answer': ans, 'key': key}
    if ds:
        d['distractors'] = [x for x in dict.fromkeys(ds) if x != ans][:5]
    d.update(kw)
    return d


# ======================================================== ch01 Sets
# st1 representations

def _primes(n):
    return [p for p in range(2, n) if all(p % q for q in range(2, int(p ** 0.5) + 1))]


def c1s1_roster(r):
    k = r.choice(['prime', 'even', 'odd', 'divisor', 'square', 'multiple'])
    n = r.randint(12, 30)
    if k == 'prime':
        xs, t = _primes(n), f'x is a prime number less than {n}'
    elif k == 'even':
        xs, t = list(range(2, n, 2)), f'x is an even natural number less than {n}'
    elif k == 'odd':
        n = r.randint(8, 16)
        xs, t = list(range(1, n, 2)), f'x is an odd natural number less than {n}'
    elif k == 'divisor':
        n = r.choice([12, 18, 20, 24, 28, 30, 36, 42])
        xs, t = [d for d in range(1, n + 1) if n % d == 0], f'x is a natural number and x divides {n}'
    elif k == 'square':
        n = r.choice([30, 50, 70, 100])
        xs, t = [i * i for i in range(1, 11) if i * i < n], f'x = n², n ∈ N and x < {n}'
    else:
        m = r.choice([3, 4, 6, 7])
        n = r.choice([25, 30, 40])
        xs, t = list(range(m, n, m)), f'x is a multiple of {m} and x < {n}, x ∈ N'
    ans = setstr(xs)
    wrong = [setstr(xs[:-1]), setstr(xs + [xs[-1] + (xs[-1] - xs[-2] if len(xs) > 1 else 1)]), setstr([1] + xs) if xs[0] != 1 else setstr(xs[1:])]
    return Q(f'Write the set {{x : {t}}} in roster form.', ans, f'List every element satisfying the property: {ans}.', wrong)


WORDS = ['MATHEMATICS', 'ALLAHABAD', 'ASSASSINATION', 'BANANA', 'KOLKATA', 'TRIGONOMETRY', 'PRINCIPAL', 'MISSISSIPPI', 'BHUBANESWAR', 'GUWAHATI', 'COMMITTEE', 'STATISTICS']


def c1s1_letters(r):
    w = r.choice(WORDS)
    s = list(dict.fromkeys(w))
    ans = '{' + ', '.join(s) + '}'
    return Q(f'Write the set of letters of the word "{w}" in roster form. How many elements does it have?', f'{ans}; {len(s)} elements',
             f'Each distinct letter is listed once: {ans}, so n = {len(s)}.', [f'{ans}; {len(w)} elements', '{' + ', '.join(w) + '}' + f'; {len(w)} elements', f'{ans}; {len(s) - 1} elements'])


def c1s1_builder(r):
    k = r.randint(4, 6)
    opts = [
        ([i * i for i in range(1, k + 1)], f'{{x : x = n², n ∈ N, n ≤ {k}}}'),
        ([i ** 3 for i in range(1, k + 1)], f'{{x : x = n³, n ∈ N, n ≤ {k}}}'),
        ([2 * i - 1 for i in range(1, k + 1)], f'{{x : x = 2n − 1, n ∈ N, n ≤ {k}}}'),
        ([2 * i for i in range(1, k + 1)], f'{{x : x = 2n, n ∈ N, n ≤ {k}}}'),
        ([5 * i for i in range(1, k + 1)], f'{{x : x = 5n, n ∈ N, n ≤ {k}}}'),
    ]
    i = r.randrange(len(opts))
    xs, right = opts[i]
    wrong = [o[1] for j, o in enumerate(opts) if j != i]
    return mcq(f'Which set-builder form represents {setstr(xs)}?', right, r.sample(wrong, 3), f'Check: the elements are exactly {setstr(xs)}.', r)


def c1s1_frac(r):
    k = r.randint(4, 7)
    f = r.choice([('n/(n + 1)', lambda n: Fr(n, n + 1)), ('(n − 1)/n', lambda n: Fr(n - 1, n) if n > 1 else None), ('1/n', lambda n: Fr(1, n)), ('n/(2n + 1)', lambda n: Fr(n, 2 * n + 1))])
    xs = [f[1](n) for n in range(1, k + 1) if f[1](n) is not None and f[1](n) != 0]
    t = ', '.join(fs(x) for x in xs)
    return Q(f'Write the set {{{t}}} in set-builder form.', f'{{x : x = {f[0]}, n ∈ N, n ≤ {k}}}' if f[0] != '(n − 1)/n' else f'{{x : x = {f[0]}, n ∈ N, 2 ≤ n ≤ {k}}}',
             'Find the pattern linking each element to its position n.', None)


def c1s1_int(r):
    a, b = r.randint(1, 4), r.randint(2, 5)
    kind = r.choice(['sq', 'range'])
    if kind == 'sq':
        k = r.choice([5, 10, 17, 26])
        xs = [x for x in range(-6, 7) if x * x < k]
        return Q(f'Write {{x : x ∈ Z and x² < {k}}} in roster form.', setstr(xs), f'x² < {k} ⇒ |x| ≤ {int((k - 1) ** 0.5)}: {setstr(xs)}.',
                 [setstr([x for x in xs if x >= 0]), setstr([x for x in xs if x > 0]), setstr(xs + [xs[-1] + 1])])
    xs = list(range(-a, b))
    return Q(f'Write {{x : x ∈ Z, −{a} ≤ x < {b}}} in roster form.', setstr(xs), f'Integers from −{a} up to {b - 1}: {setstr(xs)}.', [setstr(list(range(-a, b + 1))), setstr(list(range(-a + 1, b))), setstr(list(range(-a + 1, b + 1)))])


def c1s1_eq(r):
    a = r.choice([2, 3, 4, 5])
    b = r.randint(1, 9)
    c = b + a * r.randint(1, 6)
    x = Fr(c - b, a)
    return Q(f'Write {{x : x is a real number and {a}x + {b} = {c}}} in roster form.', f'{{{fs(x)}}}', f'{a}x = {c - b} ⇒ x = {fs(x)}; the set has one element.', [f'{{{fs(Fr(c + b, a))}}}', f'{{{c - b}}}', 'φ'])


c1s1_set = pool_mcq([
    ('Which of the following collections is a set?', 'the collection of vowels in the English alphabet', ['the collection of most talented writers of India', 'the collection of good cricketers', 'the collection of beautiful cities'], 'Only this collection is well defined.'),
    ('Which of the following collections is NOT a set?', 'the collection of interesting books', ['the collection of prime numbers less than 20', 'the collection of months with 31 days', 'the collection of planets of the solar system'], '"Interesting" is not well defined.'),
    ('Which of the following is a well-defined collection?', 'the collection of all natural numbers less than 100', ['the collection of difficult chapters of a book', 'the collection of tall students of a class', 'the collection of famous singers'], 'Membership can be decided without doubt.'),
    ('The symbol ∈ is read as', '"belongs to"', ['"is a subset of"', '"union"', '"for every"'], 'a ∈ A: a is an element of A.'),
])

c1s1_tf = tf_mcq('sets and their representation',
                 ['A set must be a well-defined collection of objects.', 'In roster form, elements are not repeated.', 'The order of listing elements of a set does not matter.',
                  'N ⊂ Z ⊂ Q ⊂ R.', 'The set of letters of "FOLLOW" is {F, O, L, W}.'],
                 ['In roster form, repeated elements must be listed each time.', 'The collection of good students is a set.', 'The order of elements changes a set.',
                  'Z ⊂ N.', '{1, 2, 3} and {3, 2, 1} are different sets.'])

c1s1_explain = pool_txt([
    ('Why is "the collection of the five most talented mathematicians of India" not a set?', 'Talent is subjective, so the collection is not well defined.', '2 marks: well-defined criterion explained.'),
    ('Write the set {x : x is a positive integer and x² < 40} in roster form and explain how you decided its elements.', '{1, 2, 3, 4, 5, 6}', '6² = 36 < 40 but 7² = 49 > 40 (1); roster (1).'),
    ('Explain the difference between roster form and set-builder form, with one example of each for the set of even natural numbers less than 10.', 'Roster {2, 4, 6, 8}; set-builder {x : x = 2n, n ∈ N, n ≤ 4}', '1 + 1 marks.'),
])

c1s1_ar = pool_ar([
    ('{1, 2, 2, 3} and {1, 2, 3} are equal sets.', 'Repeating an element does not change a set.', 'a', 'R explains A.'),
    ('The collection of all rich people in Mumbai is not a set.', 'A set must be a well-defined collection.', 'a', '"Rich" is not well defined; R explains A.'),
    ('The set of letters of "APPLE" has 5 elements.', 'In roster form each element is written only once.', 'd', 'A is false: {A, P, L, E} has 4 elements; R is true.'),
])


# st2 types of sets, subsets, power set

c1s2_types = pool_mcq([
    ('The set {x : x is a natural number, 3 < x < 4} is', 'an empty set', ['a singleton set', 'an infinite set', 'the universal set'], 'No natural number lies strictly between 3 and 4.'),
    ('The set of all points on a line is', 'infinite', ['finite', 'empty', 'a singleton'], 'A line has infinitely many points.'),
    ('The set {x : x is an even prime number} is', 'a singleton set', ['an empty set', 'an infinite set', 'a set with two elements'], 'Only 2.'),
    ('The set {x : x ∈ N and x² = 4} is', 'a singleton set', ['an empty set', 'an infinite set', '{−2, 2}'], 'x ∈ N, so only 2.'),
    ('The set of months of a year having less than 30 days is', 'a singleton set', ['an empty set', 'an infinite set', 'a set with 12 elements'], 'Only February.'),
    ('The set {x : x is a real number and x² + 1 = 0} is', 'an empty set', ['a singleton set', '{1, −1}', 'an infinite set'], 'x² = −1 has no real solution.'),
])

c1s2_terms = term_mcq([('empty set', 'a set with no elements, written φ or { }'), ('singleton set', 'a set with exactly one element'), ('equal sets', 'sets having exactly the same elements'),
                       ('power set of A', 'the set of all subsets of A'), ('proper subset', 'a subset B of A with B ≠ A'), ('universal set', 'the basic set that contains all sets under consideration')],
                      'Which of the following describes a(n) {a}?', 'Which term means {b}?', '{a}: {b}.')

c1s2_tf = tf_mcq('subsets and power sets',
                 ['The empty set is a subset of every set.', 'Every set is a subset of itself.', 'If n(A) = m, then n(P(A)) = 2ᵐ.', '{a} ∈ P({a, b}).', 'φ and {φ} are different sets.'],
                 ['The empty set has no subsets.', 'A set with 3 elements has 6 subsets.', '{a} ⊂ {{a}, b} is always true.', 'φ = {0}.', 'Every subset is a proper subset.'])

c1s2_explain = pool_txt([
    ('Is φ = {0}? Is φ = {φ}? Explain.', 'No in both cases: φ has no element, while {0} and {φ} each have one element.', '1 + 1 marks.'),
    ('Show that a set with 3 elements has 8 subsets by listing them for A = {1, 2, 3}.', 'φ, {1}, {2}, {3}, {1, 2}, {1, 3}, {2, 3}, {1, 2, 3}', '2 marks for the complete list.'),
    ('Explain why {x : x is a letter of "LOYAL"} and {x : x is a letter of "ALLOY"} are equal sets.', 'Both are {L, O, Y, A}: same elements.', '2 marks.'),
])

c1s2_ar = pool_ar([
    ('The power set of a set with 4 elements has 16 elements.', 'If n(A) = n, then n(P(A)) = 2ⁿ.', 'a', 'R explains A.'),
    ('φ is a subset of every set.', 'φ has no element which is not in the given set.', 'a', 'R explains A.'),
    ('{1, 2} is a proper subset of {1, 2}.', 'Every set is a subset of itself.', 'd', 'A is false: a proper subset must differ from the set; R is true.'),
])


def c1s2_power(r):
    n = r.randint(2, 8)
    return Q(f'A set A has {n} elements. How many elements does its power set P(A) have? How many proper subsets does A have?', f'{2 ** n}; {2 ** n - 1}',
             f'n(P(A)) = 2ⁿ = 2{sup(n)} = {2 ** n}; proper subsets = 2ⁿ − 1 = {2 ** n - 1}.', [f'{2 * n}; {2 * n - 1}', f'{n * n}; {n * n - 1}', f'{2 ** n}; {2 ** n - 2}'])


def c1s2_list(r):
    pool = r.choice([list('abcdeklmpqrsxyz'), [str(n) for n in range(0, 10)]])
    a, b, c = sorted(r.sample(pool, 3), key=lambda t: (len(t), t))
    ps = ['φ', f'{{{a}}}', f'{{{b}}}', f'{{{c}}}', f'{{{a}, {b}}}', f'{{{a}, {c}}}', f'{{{b}, {c}}}', f'{{{a}, {b}, {c}}}']
    return Q(f'Write the power set of A = {{{a}, {b}, {c}}}. How many of its elements are proper subsets of A?', '{' + ', '.join(ps) + '}; 7 proper subsets',
             'Subsets with 0, 1, 2 and 3 elements: 1 + 3 + 3 + 1 = 8 (2); all except A itself are proper: 7 (1).')


def c1s2_equal(r):
    pairs = [('{x : x is a letter of "FOLLOW"}', '{x : x is a letter of "WOLF"}', True), ('{x : x is a letter of "LOYAL"}', '{x : x is a letter of "ALLOY"}', True),
             ('{x : x is a letter of "CATARACT"}', '{x : x is a letter of "TRACT"}', True), ('{x : x ∈ N, x² = 9}', '{3}', True),
             ('{x : x ∈ Z, x² = 9}', '{3}', False), ('{x : x is a letter of "HEART"}', '{x : x is a letter of "EARTH"}', True),
             ('{0}', 'φ', False), ('{x : x is an even prime}', '{2, 4}', False), ('{1, 2, 3}', '{x : x ∈ N, x ≤ 4}', False)]
    a, b, eq = r.choice(pairs)
    return mcq(f'Are the sets A = {a} and B = {b} equal?', 'Yes, they have exactly the same elements' if eq else 'No, they do not have the same elements',
               ['No, they do not have the same elements' if eq else 'Yes, they have exactly the same elements', 'Yes, because they have the same number of letters', 'Cannot be decided'],
               'List both sets in roster form and compare.', r)


def c1s2_diff(r):
    a, b = r.choice([(7, 4), (6, 3), (5, 2), (8, 5), (6, 4), (7, 5), (9, 6)])
    d = 2 ** a - 2 ** b
    return Q(f'Set A has more elements than set B. The number of subsets of A exceeds the number of subsets of B by {d}. Find n(A) and n(B).', f'n(A) = {a}, n(B) = {b}',
             f'2ᵃ − 2ᵇ = 2ᵇ(2ᵃ⁻ᵇ − 1) = {d} (2); {d} = 2{sup(b)} × {2 ** (a - b) - 1}, and {2 ** (a - b) - 1} is odd (2); so b = {b}, a = {a} (1).',
             [f'n(A) = {a + 1}, n(B) = {b + 1}', f'n(A) = {b}, n(B) = {a}', f'n(A) = {a}, n(B) = {b - 1}'])


# st3 intervals

def _iv(a, b, lo, hi):
    return ('[' if lo else '(') + f'{fs(a)}, {fs(b)}' + (']' if hi else ')')


def c1s3_write(r):
    a = r.randint(-8, 3)
    b = a + r.randint(2, 9)
    lo, hi = r.random() < 0.5, r.random() < 0.5
    t = f'{{x : x ∈ R, {fs(a)} {"≤" if lo else "<"} x {"≤" if hi else "<"} {fs(b)}}}'
    ans = _iv(a, b, lo, hi)
    return Q(f'Write {t} in interval notation.', ans, f'"≤" gives a square bracket (endpoint included), "<" a round bracket: {ans}.',
             [_iv(a, b, not lo, hi), _iv(a, b, lo, not hi), _iv(a, b, not lo, not hi)])


def c1s3_set(r):
    a = r.randint(-6, 4)
    b = a + r.randint(2, 8)
    lo, hi = r.random() < 0.5, r.random() < 0.5
    iv = _iv(a, b, lo, hi)
    ans = f'{{x : {fs(a)} {"≤" if lo else "<"} x {"≤" if hi else "<"} {fs(b)}, x ∈ R}}'
    return Q(f'Write the interval {iv} in set-builder form. What is its length?', f'{ans}; length {b - a}', f'Brackets show which endpoints are included; length = {fs(b)} − ({fs(a)}) = {b - a}.',
             [f'{{x : {fs(a)} {"<" if lo else "≤"} x {"<" if hi else "≤"} {fs(b)}, x ∈ R}}; length {b - a}', f'{ans}; length {b - a + 1}', f'{ans}; length {abs(a) + abs(b) + 1}'])


def c1s3_cap(r):
    a, b = sorted(r.sample(range(-6, 10), 2))
    c, d = sorted(r.sample(range(-6, 10), 2))
    lo, hi = max(a, c), min(b, d)
    if lo >= hi:
        raise ValueError
    op = r.choice(['∩', '∪'])
    if op == '∪' and max(a, c) > min(b, d):
        raise ValueError
    if op == '∩':
        ans = f'[{lo}, {hi}]'
    else:
        ans = f'[{min(a, c)}, {max(b, d)}]'
    return Q(f'If A = [{a}, {b}] and B = [{c}, {d}], find A {op} B as an interval.'.replace('-', '−'), ans.replace('-', '−'),
             f'Mark both intervals on the number line; {"the overlap" if op == "∩" else "together they cover"} {ans}.'.replace('-', '−'),
             [f'[{lo}, {hi}]'.replace('-', '−') if op == '∪' else f'[{min(a, c)}, {max(b, d)}]'.replace('-', '−'), f'({lo}, {hi})'.replace('-', '−'), f'[{a}, {d}]'.replace('-', '−')])


c1s3_tf = tf_mcq('intervals',
                 ['(a, b) does not contain a or b.', '[a, b] contains both a and b.', '[a, b) contains a but not b.', 'The length of each of (a, b), [a, b], [a, b) and (a, b] is b − a.'],
                 ['(a, b) contains both a and b.', '[a, b) contains b but not a.', 'The length of [a, b] is b − a + 1.', 'An interval of real numbers is a finite set.'])

c1s3_ar = pool_ar([
    ('The interval (2, 5) is a subset of [2, 5].', 'Every element of (2, 5) is also in [2, 5].', 'a', 'R explains A.'),
    ('The intervals [1, 3] and (1, 3) have the same length.', 'The length of an interval is the difference of its endpoints.', 'a', 'R explains A.'),
    ('The interval (0, 1) contains only finitely many real numbers.', 'Between any two real numbers there is another real number.', 'd', 'A is false; R is true.'),
])

c1s3_explain = pool_txt([
    ('Explain the difference between the intervals (3, 7) and [3, 7] using the number line.', '(3, 7) excludes 3 and 7 (open dots); [3, 7] includes them (closed dots).', '2 marks.'),
    ('Is the set of real numbers between 0 and 1 finite or infinite? Express it as an interval.', 'Infinite; (0, 1).', '1 + 1 marks.'),
])


# st4 Venn diagrams, union, intersection, difference

def _sets(r):
    U = list(range(1, 13))
    A = sorted(r.sample(U, r.randint(4, 6)))
    B = sorted(r.sample(U, r.randint(4, 6)))
    return A, B


def c1s4_ops(r):
    A, B = _sets(r)
    op = r.choice(['∪', '∩', '−A', '−B'])
    if op == '∪':
        res, t = sorted(set(A) | set(B)), 'A ∪ B'
    elif op == '∩':
        res, t = sorted(set(A) & set(B)), 'A ∩ B'
    elif op == '−A':
        res, t = sorted(set(A) - set(B)), 'A − B'
    else:
        res, t = sorted(set(B) - set(A)), 'B − A'
    others = [sorted(set(A) | set(B)), sorted(set(A) & set(B)), sorted(set(A) - set(B)), sorted(set(B) - set(A)), sorted(set(A) ^ set(B))]
    ans = setstr(res)
    return Q(f'If A = {setstr(A)} and B = {setstr(B)}, find {t}.', ans, f'{t} = {ans}.', [setstr(o) for o in others])


def c1s4_count(r):
    a, b = r.randint(15, 40), r.randint(15, 40)
    i = r.randint(3, min(a, b) - 2)
    return Q(f'If n(A) = {a}, n(B) = {b} and n(A ∩ B) = {i}, find n(A ∪ B).', str(a + b - i), f'n(A ∪ B) = n(A) + n(B) − n(A ∩ B) = {a} + {b} − {i} = {a + b - i}.',
             [str(a + b), str(a + b + i), str(a + b - 2 * i)])


def c1s4_survey(r):
    city = r.choice(CITIES)
    tot = r.choice([40, 50, 60, 70])
    a = r.randint(tot // 3, tot // 2 + 10)
    b = r.randint(tot // 3, tot // 2 + 10)
    i = a + b - tot + r.randint(0, 5)
    if i < 2 or i > min(a, b):
        raise ValueError
    neither = tot - (a + b - i)
    return Q(f'In a class of {tot} students in {city}, {a} like cricket, {b} like football and {i} like both. Find how many like (i) cricket only, (ii) at least one of the two games, (iii) neither game.',
             f'(i) {a - i} (ii) {a + b - i} (iii) {neither}', f'(i) n(C) − n(C ∩ F) = {a - i} (1). (ii) n(C ∪ F) = {a} + {b} − {i} = {a + b - i} (1). (iii) {tot} − {a + b - i} = {neither} (1).',
             [f'(i) {a} (ii) {a + b} (iii) {tot - a - b if tot > a + b else 0}', f'(i) {a - i} (ii) {a + b} (iii) {neither - i}', f'(i) {b - i} (ii) {a + b - i} (iii) {neither + i}'])


def c1s4_find_i(r):
    a, b = r.randint(20, 50), r.randint(20, 50)
    i = r.randint(5, min(a, b) - 3)
    u = a + b - i
    return Q(f'n(A) = {a}, n(B) = {b} and n(A ∪ B) = {u}. Find n(A ∩ B), n(A − B) and n(B − A).', f'{i}; {a - i}; {b - i}', f'n(A ∩ B) = {a} + {b} − {u} = {i} (1); n(A − B) = {a} − {i} (1); n(B − A) = {b} − {i} (1).',
             [f'{i}; {b - i}; {a - i}', f'{a + b - u + 1}; {a - i - 1}; {b - i - 1}', f'{u - a}; {a - i}; {b - i}'])


c1s4_terms = term_mcq([('A ∪ B', 'the set of elements in A or in B or in both'), ('A ∩ B', 'the set of elements common to A and B'), ('A − B', 'the set of elements in A but not in B'),
                       ('disjoint sets', 'sets with no element in common, A ∩ B = φ'), ('symmetric difference (A − B) ∪ (B − A)', 'elements in exactly one of A and B')],
                      'Which of the following describes {a}?', 'Which of these is {b}?', '{a}: {b}.')

c1s4_tf = tf_mcq('operations on sets',
                 ['A ∪ B = B ∪ A.', 'A ∩ φ = φ.', 'A − B, A ∩ B and B − A are mutually disjoint.', 'A ∪ (B ∩ C) = (A ∪ B) ∩ (A ∪ C).', 'If A ⊂ B then A ∪ B = B.'],
                 ['A − B = B − A for all sets.', 'A ∪ φ = φ.', 'n(A ∪ B) = n(A) + n(B) always.', 'If A ⊂ B then A ∩ B = B.', 'A ∩ B is always non-empty.'])

c1s4_ar = pool_ar([
    ('If A and B are disjoint, then n(A ∪ B) = n(A) + n(B).', 'For disjoint sets, n(A ∩ B) = 0.', 'a', 'R explains A.'),
    ('A − B and B − A are disjoint.', 'An element of A − B is not in B.', 'a', 'R explains A.'),
    ('A − B = B − A for any two sets A and B.', 'A − B contains elements of A that are not in B.', 'd', 'A is false; R is true.'),
])

c1s4_explain = pool_txt([
    ('Using a Venn diagram, show that A − B, A ∩ B and B − A are disjoint and their union is A ∪ B.', 'The three regions do not overlap and together make up A ∪ B.', '2 marks.'),
    ('If A ⊂ B, what are A ∪ B and A ∩ B? Explain with a Venn diagram.', 'A ∪ B = B and A ∩ B = A.', '1 + 1 marks.'),
])


# st5 complement, De Morgan, practical problems

def c1s5_comp(r):
    n = r.randint(9, 12)
    U = list(range(1, n + 1))
    A = sorted(r.sample(U, r.randint(3, 6)))
    res = [x for x in U if x not in A]
    return Q(f'Let U = {setstr(U)} and A = {setstr(A)}. Find A′.', setstr(res), f'A′ = U − A = {setstr(res)}.', [setstr(A), setstr(res[1:]), setstr(res + [A[0]])])


def c1s5_dem(r):
    U = list(range(1, 11))
    A = sorted(r.sample(U, 4))
    B = sorted(r.sample(U, 4))
    lhs = sorted(set(U) - (set(A) | set(B)))
    which = r.random() < 0.5
    if which:
        res = lhs
        t = "(A ∪ B)′"
        k = f'A ∪ B = {setstr(sorted(set(A) | set(B)))}; (A ∪ B)′ = {setstr(res)} = A′ ∩ B′ (De Morgan).'
    else:
        res = sorted(set(U) - (set(A) & set(B)))
        t = "(A ∩ B)′"
        k = f'A ∩ B = {setstr(sorted(set(A) & set(B)))}; (A ∩ B)′ = {setstr(res)} = A′ ∪ B′ (De Morgan).'
    return Q(f'U = {setstr(U)}, A = {setstr(A)}, B = {setstr(B)}. Find {t} and verify De Morgan\'s law.', setstr(res), k,
             [setstr(sorted(set(U) - (set(A) & set(B)))) if which else setstr(lhs), setstr(sorted(set(A) | set(B))), setstr(sorted(set(A) & set(B)))])


def c1s5_three(r):
    a, b, c = r.randint(20, 40), r.randint(20, 40), r.randint(20, 40)
    ab, bc, ca = r.randint(6, 12), r.randint(6, 12), r.randint(6, 12)
    abc = r.randint(2, 5)
    u = a + b + c - ab - bc - ca + abc
    who = r.choice(['read newspapers H, T and I (as A, B, C)', 'study Physics, Chemistry and Maths (as A, B, C)', 'drink tea, coffee and milk (as A, B, C)'])
    return Q(f'In a survey, the numbers of people who {who} were: n(A) = {a}, n(B) = {b}, n(C) = {c}, n(A ∩ B) = {ab}, n(B ∩ C) = {bc}, n(C ∩ A) = {ca} and n(A ∩ B ∩ C) = {abc}. Find the number using at least one of them.',
             str(u), f'n(A ∪ B ∪ C) = Σn(A) − Σn(A ∩ B) + n(A ∩ B ∩ C) (2) = {a + b + c} − {ab + bc + ca} + {abc} (2) = {u} (1).', [str(u - abc), str(a + b + c), str(u + abc)])


def c1s5_exact(r):
    a, b, c = r.randint(25, 40), r.randint(25, 40), r.randint(25, 40)
    ab, bc, ca = r.randint(8, 12), r.randint(8, 12), r.randint(8, 12)
    abc = r.randint(3, 6)
    only = a + b + c - 2 * (ab + bc + ca) + 3 * abc
    return Q(f'In a group of students, {a} study French, {b} study German and {c} study Sanskrit; {ab} study French and German, {bc} German and Sanskrit, {ca} Sanskrit and French, and {abc} study all three. How many study exactly one of the three languages?',
             str(only), f'Exactly one = Σn(A) − 2Σn(A ∩ B) + 3n(A ∩ B ∩ C) (3) = {a + b + c} − {2 * (ab + bc + ca)} + {3 * abc} (1) = {only} (1).',
             [str(a + b + c - (ab + bc + ca) + abc), str(only + abc), str(a + b + c - 2 * (ab + bc + ca))])


def c1s5_neither(r):
    tot = r.choice([100, 120, 150, 200])
    a, b = r.randint(40, 80), r.randint(40, 80)
    i = a + b - tot + r.randint(5, 25)
    if i <= 0 or i > min(a, b):
        raise ValueError
    return Q(f'In a survey of {tot} people in {r.choice(CITIES)}, {a} read a Hindi newspaper, {b} read an English newspaper and {i} read both. How many read neither?', str(tot - a - b + i),
             f'n(H ∪ E) = {a} + {b} − {i} = {a + b - i}; neither = {tot} − {a + b - i} = {tot - a - b + i}.', [str(tot - a - b), str(tot - a - b + 2 * i), str(a + b - i)])


def c1s5_case(r):
    who = name(r)
    tot = r.choice([60, 80, 100])
    t, c = r.randint(tot // 3, tot // 2), r.randint(tot // 3, tot // 2)
    b = r.randint(5, 12)
    nei = tot - (t + c - b)
    if nei < 0:
        raise ValueError
    return {'stem': (f'{who}, the class representative, surveys the {tot} students of class XI about the morning drink they like. {t} like tea, {c} like coffee and {b} like both.\n'
                     '(i) How many like tea only? (ii) How many like at least one drink? (iii) How many like neither? (iv) Represent the data in a Venn diagram and name the region for "coffee but not tea".'),
            'answer': f'(i) {t - b} (ii) {t + c - b} (iii) {nei} (iv) C − T, with {c - b} students',
            'key': '(i) n(T) − n(T ∩ C) (1). (ii) n(T ∪ C) (1). (iii) n(U) − n(T ∪ C) (1). (iv) C − T (1).'}


c1s5_tf = tf_mcq("complements and De Morgan's laws",
                 ['(A ∪ B)′ = A′ ∩ B′.', '(A ∩ B)′ = A′ ∪ B′.', '(A′)′ = A.', 'A ∪ A′ = U.', 'φ′ = U.'],
                 ['(A ∪ B)′ = A′ ∪ B′.', 'A ∩ A′ = U.', 'U′ = U.', '(A ∩ B)′ = A′ ∩ B′.', 'A − B = A ∩ B.'])

c1s5_ar = pool_ar([
    ('(A ∪ B)′ = A′ ∩ B′.', 'An element is outside A ∪ B exactly when it is outside A and outside B.', 'a', 'R explains A.'),
    ('A − B = A ∩ B′.', 'Elements of A − B are in A and not in B.', 'a', 'R explains A.'),
    ('A ∩ A′ = U.', 'A and A′ together make up U.', 'd', 'A is false: A ∩ A′ = φ; R is true (A ∪ A′ = U).'),
])

c1s5_explain = pool_txt([
    ('Use a Venn diagram to illustrate (A ∪ B)′ = A′ ∩ B′.', 'The region outside both circles is the same in both cases.', '2 marks.'),
    ('Show that A − B = A ∩ B′.', 'x ∈ A − B ⇔ x ∈ A and x ∉ B ⇔ x ∈ A and x ∈ B′ ⇔ x ∈ A ∩ B′.', '2 marks.'),
])

c1s5_long = pool_txt([
    ('Prove that n(A ∪ B ∪ C) = n(A) + n(B) + n(C) − n(A ∩ B) − n(B ∩ C) − n(C ∩ A) + n(A ∩ B ∩ C).', 'Formula proved', 'Use n(X ∪ Y) = n(X) + n(Y) − n(X ∩ Y) with X = A ∪ B, Y = C (2); distributive law (2); simplify (1).'),
    ('Prove De Morgan\'s laws (A ∪ B)′ = A′ ∩ B′ and (A ∩ B)′ = A′ ∪ B′ by element method.', 'Both proved', 'Each inclusion both ways (2 + 2); conclusion (1).'),
])


# ======================================================== ch02 Relations and Functions
# st1 Cartesian product

def c2s1_n(r):
    m, n = r.randint(2, 6), r.randint(2, 6)
    return Q(f'If n(A) = {m} and n(B) = {n}, find n(A × B) and the number of relations from A to B.', f'{m * n}; 2{sup(m * n)}', f'n(A × B) = mn = {m * n}; relations are subsets of A × B: 2{sup(m * n)}.',
             [f'{m + n}; 2{sup(m + n)}', f'{m * n}; {2 * m * n}', f'{m * n}; {m * n}²'])


def c2s1_list(r):
    A = r.choice([['1', '2'], ['a', 'b'], ['p', 'q'], ['2', '3']])
    B = r.choice([['x', 'y', 'z'], ['3', '4', '5'], ['1', '3', '5'], ['r', 's', 't']])
    ps = ', '.join(f'({a}, {b})' for a in A for b in B)
    qs = ', '.join(f'({b}, {a})' for a in A for b in B)
    return Q(f'If A = {{{", ".join(A)}}} and B = {{{", ".join(B)}}}, write A × B. Is A × B = B × A?', f'{{{ps}}}; no', f'A × B = {{{ps}}} (1); B × A contains ({B[0]}, {A[0]}) ≠ ({A[0]}, {B[0]}), so not equal (1).',
             [f'{{{qs}}}; no', f'{{{ps}}}; yes', f'{{{qs}}}; yes'])


def c2s1_eq(r):
    a, b, c, d = r.randint(1, 6), r.randint(1, 6), r.randint(-3, 9), r.randint(-3, 9)
    k = r.choice([2, 3])
    t = r.choice(['plain', 'frac'])
    if t == 'plain':
        x, y = c - a, d + b
        return Q(f'If (x + {a}, y − {b}) = ({c}, {d}), find x and y.'.replace('-', '−'), f'x = {fs(x)}, y = {fs(y)}', f'Equal ordered pairs: x + {a} = {c}, y − {b} = {d} (1) ⇒ x = {fs(x)}, y = {fs(y)} (1).'.replace('-', '−'),
                 [f'x = {fs(c + a)}, y = {fs(d - b)}', f'x = {fs(y)}, y = {fs(x)}', f'x = {fs(x)}, y = {fs(d - b)}'])
    x, y = Fr(c - a, 1) * k, Fr(d + b, k)
    return Q(f'If (x/{k} + {a}, {k}y − {b}) = ({c}, {d}), find x and y.'.replace('-', '−'), f'x = {fs(x)}, y = {fs(y)}', f'x/{k} = {c} − {a} ⇒ x = {fs(x)} (1); {k}y = {d} + {b} ⇒ y = {fs(y)} (1).'.replace('-', '−'),
             [f'x = {fs(Fr(c - a, k))}, y = {fs((d + b) * k)}', f'x = {fs(x)}, y = {fs(Fr(d - b, k))}', f'x = {fs(y)}, y = {fs(x)}'])


def c2s1_find(r):
    A = sorted(r.sample(range(-2, 6), 3))
    p1 = (A[0], A[1])
    p2 = (A[2], A[0])
    rest = [(a, b) for a in A for b in A if (a, b) not in (p1, p2)]
    t = lambda p: f'({p[0]}, {p[1]})'.replace('-', '−')
    return Q(f'A × A has 9 elements, two of which are {t(p1)} and {t(p2)}. Find the set A and the remaining elements of A × A.', f'A = {setstr(A)}; remaining: ' + ', '.join(t(p) for p in rest),
             f'n(A × A) = 9 ⇒ n(A) = 3 (1); from the given pairs A contains {A[0]}, {A[1]}, {A[2]} (1); list all 9 pairs and remove the given two (2).'.replace('-', '−'))


c2s1_tf = tf_mcq('Cartesian products',
                 ['If A or B is empty, then A × B is empty.', 'n(A × B) = n(A) × n(B).', '(a, b) = (b, a) only if a = b.', 'A × B ≠ B × A in general.'],
                 ['A × B = B × A for all sets A and B.', 'n(A × B) = n(A) + n(B).', '(1, 2) = (2, 1).', 'A × φ = A.'])

c2s1_ar = pool_ar([
    ('If n(A) = 3 and n(B) = 2, then n(A × B) = 6.', 'n(A × B) = n(A) · n(B).', 'a', 'R explains A.'),
    ('(2, 3) and (3, 2) are equal ordered pairs.', 'The order of elements in an ordered pair matters.', 'd', 'A is false; R is true.'),
    ('A × φ = φ.', 'There is no element in φ to pair with elements of A.', 'a', 'R explains A.'),
])

c2s1_explain = pool_txt([
    ('Explain why (1, 2) and (2, 1) are different elements of N × N.', 'In an ordered pair the order matters: first components 1 and 2 differ.', '2 marks.'),
    ('If A × B = {(a, x), (a, y), (b, x), (b, y)}, find A and B, with reasons.', 'A = {a, b} (first components), B = {x, y} (second components).', '2 marks.'),
])


# st2 relations

def c2s2_dom(r):
    xs = sorted(r.sample(range(1, 10), r.randint(4, 5)))
    a, b = r.choice([1, 2, 3]), r.randint(-3, 5)
    R = [(x, a * x + b) for x in xs]
    pairs = ', '.join(f'({x}, {y})'.replace('-', '−') for x, y in R)
    rng = setstr([y for _, y in R])
    return Q(f'R = {{(x, y) : y = {lin(a, b)}, x ∈ {setstr(xs)}}}. Write R in roster form and find its domain and range.', f'R = {{{pairs}}}; domain {setstr(xs)}; range {rng}',
             f'Substitute each x (1); domain = set of first elements (1); range = set of second elements (1).', [f'R = {{{pairs}}}; domain {rng}; range {setstr(xs)}'])


def c2s2_count(r):
    m, n = r.randint(2, 4), r.randint(2, 4)
    return Q(f'A has {m} elements and B has {n} elements. How many relations are there from A to B?', f'2{sup(m * n)} = {2 ** (m * n)}', f'Relations from A to B are subsets of A × B, which has {m * n} elements: 2{sup(m * n)}.',
             [f'{m * n}', f'2{sup(m + n)} = {2 ** (m + n)}', f'{(m * n) ** 2}'])


def c2s2_div(r):
    A = sorted(r.sample(range(1, 13), 5))
    R = [(a, b) for a in A for b in A if b % a == 0 and a != b]
    if not R:
        raise ValueError
    pairs = ', '.join(f'({a}, {b})' for a, b in R)
    return Q(f'Let A = {setstr(A)}. Define R on A by R = {{(a, b) : a, b ∈ A, b is exactly divisible by a, a ≠ b}}. Write R in roster form and find its domain and range.',
             f'R = {{{pairs}}}; domain {setstr(sorted(set(a for a, _ in R)))}; range {setstr(sorted(set(b for _, b in R)))}', 'Check every ordered pair (2); read off first and second components (1).')


c2s2_terms = term_mcq([('relation from A to B', 'a subset of A × B'), ('domain of a relation', 'the set of first elements of its ordered pairs'),
                       ('range of a relation', 'the set of second elements of its ordered pairs'), ('codomain of a relation from A to B', 'the whole set B')],
                      'Which of the following describes the {a}?', 'Which term is {b}?', '{a}: {b}.')

c2s2_tf = tf_mcq('relations',
                 ['Every relation from A to B is a subset of A × B.', 'The range of a relation is a subset of its codomain.', 'The empty set is a relation from A to B.', 'A × B itself is a relation from A to B.'],
                 ['The codomain is always equal to the range.', 'A relation must contain every element of A × B.', 'The number of relations from A to B is n(A) · n(B).', 'A relation cannot be empty.'])

c2s2_ar = pool_ar([
    ('The range of a relation is a subset of its codomain.', 'The second components of the pairs all belong to the codomain.', 'a', 'R explains A.'),
    ('There are 2⁶ relations from a set of 2 elements to a set of 3 elements.', 'Each relation is a subset of A × B, which has 6 elements.', 'a', 'R explains A.'),
    ('The range of every relation equals its codomain.', 'The range is the set of second elements of the pairs.', 'd', 'A is false; R is true.'),
])

c2s2_explain = pool_txt([
    ('Distinguish between the codomain and the range of a relation, with an example.', 'Codomain is the whole set B; range is only the second elements actually used. For R = {(1, 2)} from {1} to {2, 3}: codomain {2, 3}, range {2}.', '2 marks.'),
    ('Explain why the number of relations from A to B is 2^(mn) when n(A) = m and n(B) = n.', 'Each relation is a subset of A × B, which has mn elements, so there are 2^(mn) subsets.', '2 marks.'),
])


# st3 functions and their graphs

def c2s3_val(r):
    a, b, c = r.randint(1, 4), r.randint(-6, 6), r.randint(-9, 9)
    k = r.randint(-4, 5)
    v = a * k * k + b * k + c
    return Q(f'If f(x) = {poly([a, b, c])}, find f({k}).'.replace('f(-', 'f(−'), fs(v), f'f({k}) = {a}({k})² + ({b})({k}) + ({c}) = {fs(v)}.'.replace('-', '−'), [fs(v + 2 * b * k), fs(a * k * k - b * k + c), fs(a * k + b * k + c)])


def c2s3_special(r):
    x = r.choice([Fr(-7, 2), Fr(-3, 2), Fr(-1, 3), Fr(5, 2), Fr(13, 4), Fr(-21, 5), Fr(9, 2)])
    k = r.choice(['gi', 'mod', 'sgn'])
    if k == 'gi':
        v, t, rule = math.floor(x), f'[{fs(x)}], where [x] is the greatest integer function', 'greatest integer ≤ x'
        ws = [math.ceil(x), int(x) if x < 0 else math.floor(x) + 1, math.floor(x) - 1]
    elif k == 'mod':
        v, t, rule = abs(x), f'|{fs(x)}|', 'distance from 0'
        ws = [-abs(x), x if x > 0 else -x + 1, 0]
    else:
        v, t, rule = 1 if x > 0 else -1, f'sgn({fs(x)}), where sgn is the signum function', 'sign of x'
        ws = [0, abs(x), x]
    return Q(f'Find the value of {t}.', fs(v), f'{rule}: {fs(v)}.', [fs(w) for w in ws if fs(w) != fs(v)])


def c2s3_isf(r):
    good = r.choice([[(2, 1), (5, 1), (8, 1), (11, 1)], [(1, 3), (2, 5), (3, 7)], [(-1, 1), (0, 0), (1, 1)], [(4, 2), (9, 3), (16, 4)]])
    bads = [[(2, 1), (2, 3), (5, 4)], [(1, 1), (1, -1), (4, 2)], [(3, 5), (4, 6), (3, 7)], [(0, 1), (0, 2), (1, 3)]]
    t = lambda R: '{' + ', '.join(f'({a}, {b})'.replace('-', '−') for a, b in R) + '}'
    if r.random() < 0.5:
        return mcq('Which of the following relations is a function?', t(good), [t(b) for b in r.sample(bads, 3)], 'In a function no first element is repeated with a different second element.', r)
    bad = r.choice(bads)
    goods = [[(2, 1), (5, 1), (8, 1)], [(1, 3), (2, 5), (3, 7)], [(-1, 1), (0, 0), (1, 1)], [(4, 2), (9, 3), (16, 4)]]
    return mcq('Which of the following relations is NOT a function?', t(bad), [t(g_) for g_ in r.sample(goods, 3)], 'A first element is paired with two different second elements.', r)


def c2s3_domain(r):
    p, q = r.sample(range(-6, 7), 2)
    b, c = -(p + q), p * q
    a = r.randint(1, 9)
    ans = f'R − {{{", ".join(fs(x) for x in sorted([p, q]))}}}'
    return Q(f'Find the domain of the real function f(x) = (x² + {a})/({poly([1, b, c])}).', ans, f'Denominator x² {term(b, "x", False).strip()} {term(c, "", False).strip()} = (x − {fs(p)})(x − {fs(q)}) = 0 at x = {fs(p)}, {fs(q)} (1); exclude them (1).'.replace('− −', '+ '),
             [f'R − {{{", ".join(fs(-x) for x in sorted([p, q]))}}}', 'R', f'R − {{{fs(p)}}}'])


def c2s3_range(r):
    a = r.randint(-5, 9)
    k = r.choice(['mod', 'sq', 'neg', 'sqrt'])
    if k == 'mod':
        return Q(f'Find the range of f(x) = |x − {a}| + {abs(a) + 1}, x ∈ R.'.replace('− -', '+ '), f'[{abs(a) + 1}, ∞)', f'|x − a| ≥ 0, with 0 attained at x = {a}; so f(x) ≥ {abs(a) + 1}.', [f'({abs(a) + 1}, ∞)', '[0, ∞)', 'R'])
    if k == 'sq':
        return Q(f'Find the range of f(x) = x² + {abs(a) + 2}, x ∈ R.', f'[{abs(a) + 2}, ∞)', f'x² ≥ 0 with minimum 0 at x = 0; so f(x) ≥ {abs(a) + 2}.', [f'({abs(a) + 2}, ∞)', 'R', '[0, ∞)'])
    if k == 'neg':
        return Q(f'Find the range of f(x) = {abs(a) + 2} − x², x ∈ R.', f'(−∞, {abs(a) + 2}]', f'−x² ≤ 0, so f(x) ≤ {abs(a) + 2}, with equality at x = 0.', [f'[{abs(a) + 2}, ∞)', f'(−∞, {abs(a) + 2})', 'R'])
    return Q(f'Find the domain and range of f(x) = √(x − {abs(a) + 1}).', f'domain [{abs(a) + 1}, ∞); range [0, ∞)', f'Need x − {abs(a) + 1} ≥ 0 (1); square root is ≥ 0 and takes every non-negative value (1).',
             [f'domain [0, ∞); range [{abs(a) + 1}, ∞)', f'domain ({abs(a) + 1}, ∞); range (0, ∞)', 'domain R; range R'])


c2s3_terms = term_mcq([('identity function', 'f(x) = x for every real x'), ('constant function', 'f(x) = c for every x'), ('modulus function', 'f(x) = |x|, with range [0, ∞)'),
                       ('signum function', 'f(x) = 1 for x > 0, 0 for x = 0, −1 for x < 0'), ('greatest integer function', 'f(x) = [x], the greatest integer less than or equal to x'),
                       ('polynomial function', 'f(x) = a₀ + a₁x + … + aₙxⁿ with n a non-negative integer')],
                      'Which of the following defines the {a}?', 'Which function is {b}?', '{a}: {b}.')

c2s3_tf = tf_mcq('real functions',
                 ['Every function is a relation, but not every relation is a function.', 'The range of the signum function is {−1, 0, 1}.', 'The graph of the modulus function is V-shaped.',
                  'The domain of f(x) = 1/x is R − {0}.', '[−2.5] = −3.'],
                 ['Every relation is a function.', 'The range of the modulus function is R.', '[−2.5] = −2.', 'The domain of f(x) = 1/x is R.', 'The signum function takes every real value.'])

c2s3_ar = pool_ar([
    ('f(x) = x² is a function from R to R.', 'Every real x has exactly one image x².', 'a', 'R explains A.'),
    ('{(1, 2), (1, 3), (2, 4)} is a function.', 'In a function each element of the domain has a unique image.', 'd', 'A is false: 1 has two images; R is true.'),
    ('The range of f(x) = |x| is [0, ∞).', '|x| ≥ 0 for every real x.', 'a', 'R explains A (and every non-negative value is attained).'),
])

c2s3_explain = pool_txt([
    ('Why is the relation {(x, y) : y² = x, x, y ∈ R, x ≥ 0} not a function of x?', 'For x = 4 there are two values y = 2 and y = −2.', '2 marks.'),
    ('Draw the graph of the greatest integer function for −2 ≤ x < 3 and describe it.', 'A step graph: horizontal segments of length 1, closed at the left end and open at the right.', '2 marks.'),
])


def c2s3_case(r):
    who = name(r)
    city = r.choice(CITIES)
    a, b = r.choice([(50, 15), (40, 12), (60, 18), (30, 10)])
    d = r.choice([8, 10, 12, 15])
    return {'stem': (f'An auto-rickshaw in {city} charges a fixed ₹{a} plus ₹{b} per km. {who} models the fare as f(x) = {a} + {b}x for a ride of x km.\n'
                     f'(i) Find f({d}). (ii) What is the domain of f in this context? (iii) For what distance is the fare ₹{a + b * (d + 4)}? (iv) Is f a linear function? Give its slope.'),
            'answer': f'(i) ₹{a + b * d} (ii) x ≥ 0 (non-negative real numbers) (iii) {d + 4} km (iv) yes, slope {b}',
            'key': '(i) substitute (1). (ii) distance cannot be negative (1). (iii) solve a + bx = fare (1). (iv) f(x) = mx + c with m = b (1).'}


c2s3_long = pool_txt([
    ('Define the modulus function. Draw its graph and write its domain and range.', 'f(x) = |x|; domain R; range [0, ∞)', 'Definition (1); graph (2); domain and range (2).'),
    ('Define the signum function, draw its graph, and write its domain and range.', 'sgn x = |x|/x (x ≠ 0), 0 at x = 0; domain R; range {−1, 0, 1}', 'Definition (1); graph (2); domain and range (2).'),
])


# st4 algebra of functions

def c2s4_ops(r):
    a, b, c, d = r.randint(1, 5), r.randint(-6, 6), r.randint(1, 5), r.randint(-6, 6)
    op = r.choice(['+', '−', '×'])
    if op == '+':
        res, t = poly([a + c, b + d]), '(f + g)(x)'
    elif op == '−':
        res, t = poly([a - c, b - d]), '(f − g)(x)'
    else:
        res, t = poly([a * c, a * d + b * c, b * d]), '(fg)(x)'
    return Q(f'If f(x) = {lin(a, b)} and g(x) = {lin(c, d)}, find {t}.', res, f'{t} = f(x) {op} g(x) = {res}.',
             [poly([a + c, b - d]), poly([a - c, b + d]), poly([a * c, b * d]), poly([a + c, b + d])])


def c2s4_val(r):
    a, b = r.randint(1, 4), r.randint(-5, 5)
    k = r.randint(-3, 4)
    fk = a * k * k + b
    gk = 2 * k + 1
    if gk == 0:
        raise ValueError
    op = r.choice(['+', '×', '/'])
    v = fk + gk if op == '+' else fk * gk if op == '×' else Fr(fk, gk)
    t = {'+': '(f + g)', '×': '(fg)', '/': '(f/g)'}[op]
    return Q(f'f(x) = {poly([a, 0, b])} and g(x) = 2x + 1. Find {t}({k}).'.replace('(-', '(−'), fs(v), f'f({k}) = {fk}, g({k}) = {gk}; {t}({k}) = {fs(v)}.'.replace('(-', '(−'),
             [fs(fk - gk), fs(fk * gk + 1), fs(Fr(gk, fk) if fk else gk + 1)])


def c2s4_dom(r):
    a, b = r.randint(1, 6), r.randint(-5, 5)
    p = r.randint(-6, 6)
    return Q(f'f(x) = x² + {a} and g(x) = x − {p}. Find (f/g)(x) and its domain.'.replace('− -', '+ '), f'(x² + {a})/(x − {p}), domain R − {{{fs(p)}}}'.replace('− -', '+ '),
             f'(f/g)(x) = f(x)/g(x) (1), defined where g(x) ≠ 0, i.e. x ≠ {fs(p)} (1).', [f'(x² + {a})/(x − {p}), domain R'.replace('− -', '+ '), f'(x − {p})/(x² + {a}), domain R'.replace('− -', '+ '), f'(x² + {a})/(x − {p}), domain R − {{{fs(-p)}}}'.replace('− -', '+ ')])


def c2s4_multi(r):
    a = r.randint(1, 4)
    b = r.randint(1, 5)
    fg = poly([2 * a, a, 0, 0])
    return Q(f'Let f(x) = {a}x² and g(x) = 2x + 1. Find (f + g)(x), (f − g)(x), (fg)(x) and (f/g)(x), giving the domain of f/g.',
             f'{poly([a, 2, 1])}; {poly([a, -2, -1])}; {fg}; {a}x²/(2x + 1), x ≠ −1/2', '(f + g) (1); (f − g) (1); fg = 2ax³ + ax² (1); f/g with 2x + 1 ≠ 0 (1); domain R − {−1/2} (1).')


c2s4_tf = tf_mcq('the algebra of real functions',
                 ['(f + g)(x) = f(x) + g(x).', 'f/g is not defined where g(x) = 0.', '(fg)(x) = f(x)·g(x).', 'The domain of f + g is the intersection of the domains of f and g.'],
                 ['(f/g)(x) is defined even where g(x) = 0.', '(f − g)(x) = g(x) − f(x).', '(fg)(x) = f(g(x)).', 'The domain of f + g is the union of the domains of f and g.'])

c2s4_ar = pool_ar([
    ('If f(x) = x and g(x) = x − 2, then f/g is not defined at x = 2.', 'Division by zero is not defined.', 'a', 'R explains A.'),
    ('(f − g)(x) = (g − f)(x) for all functions f and g.', '(f − g)(x) = f(x) − g(x).', 'd', 'A is false; R is true.'),
    ('(fg)(x) = (gf)(x) for real functions.', 'Multiplication of real numbers is commutative.', 'a', 'R explains A.'),
])

c2s4_explain = pool_txt([
    ('Explain why the domain of f/g excludes the zeros of g.', '(f/g)(x) = f(x)/g(x) and division by zero is undefined.', '2 marks.'),
    ('Is (fg)(x) the same as f(g(x))? Explain with f(x) = x², g(x) = x + 1.', 'No: (fg)(x) = x²(x + 1) while f(g(x)) = (x + 1)².', '2 marks.'),
])


# ======================================================== ch03 Trigonometric Functions
# st1 degree and radian measure

def c3s1_d2r(r):
    d = r.choice([15, 18, 20, 25, 30, 36, 40, 45, 60, 72, 75, 90, 105, 120, 135, 150, 210, 240, 270, 300, 315, 330, -45, -60, -120, 520])
    q = Fr(d, 180)
    num_ = q.numerator
    s = ('−' if num_ < 0 else '') + ('' if abs(num_) == 1 else str(abs(num_))) + 'π' + ('' if q.denominator == 1 else f'/{q.denominator}')
    return Q(f'Convert {d}° into radian measure.'.replace('-', '−'), s, f'Radian = degree × π/180 = {d} × π/180 = {s}.'.replace('-', '−'),
             [s.replace('π', '') + ('' if '/' in s else ''), f'{fs(Fr(d, 90))}π', f'{fs(Fr(d * 2, 180))}π'])


def c3s1_r2d(r):
    q = r.choice([Fr(1, 6), Fr(5, 12), Fr(7, 6), Fr(3, 4), Fr(5, 3), Fr(11, 18), Fr(-5, 4), Fr(7, 12)])
    d = q * 180
    s = ('−' if q < 0 else '') + ('' if abs(q.numerator) == 1 else str(abs(q.numerator))) + 'π/' + str(q.denominator)
    return Q(f'Convert {s} radians into degrees.', f'{fs(d)}°', f'Degree = radian × 180/π = {s} × 180/π = {fs(d)}°.', [f'{fs(d / 2)}°', f'{fs(d * 2)}°', f'{fs(q * 90)}°'])


def c3s1_r2dms(r):
    x = r.choice([2, 3, 4, 6])
    sign = r.choice([1, -1])
    tot = x * 180 * 7 / 22  # π = 22/7
    deg = int(tot)
    rem = (tot - deg) * 60
    mi = int(rem)
    se = round((rem - mi) * 60)
    if se == 60:
        mi, se = mi + 1, 0
    s = f'{"−" if sign < 0 else ""}{deg}° {mi}′ {se}″'
    return Q(f'Convert {"−" if sign < 0 else ""}{x} radians into degree measure (use π = 22/7).', s, f'{x} × 180/π = {x} × 180 × 7/22 = {num(tot, 4)}° (1); convert the decimal part to minutes and seconds (1) ⇒ {s}.',
             [f'{"−" if sign < 0 else ""}{deg}° {mi + 1}′ {se}″', f'{"−" if sign < 0 else ""}{deg + 1}° {mi}′', f'{"−" if sign < 0 else ""}{deg}° {se}′ {mi}″'])


def c3s1_arc(r):
    rr = r.choice([7, 14, 21, 35, 70])
    d = r.choice([30, 45, 60, 72, 90, 120, 150])
    l = Fr(rr) * Fr(d, 180) * Fr(22, 7)
    return Q(f'Find the length of an arc of a circle of radius {rr} cm which subtends an angle of {d}° at the centre. (π = 22/7)', f'{fs(l)} cm' if l.denominator <= 21 else f'{num(float(l), 2)} cm',
             f'θ = {d} × π/180 rad (1); l = rθ = {rr} × {fs(Fr(d, 180))} × 22/7 = {fs(l)} cm (1).', [f'{fs(l * 2)} cm', f'{fs(Fr(rr * d))} cm', f'{fs(l / 2)} cm'])


def c3s1_clock(r):
    t = r.choice([10, 15, 20, 25, 40, 45])
    L = r.choice([1.5, 2, 3, 7, 14, 21])
    ang = Fr(t * 6, 180)  # radians in units of π
    dist = float(ang) * math.pi * L
    s = ('' if ang.numerator == 1 else str(ang.numerator)) + 'π' + ('' if ang.denominator == 1 else f'/{ang.denominator}')
    return Q(f'The minute hand of a clock is {g(L)} cm long. How far does its tip move in {t} minutes? (take π = 3.14)', f'{num(float(ang) * 3.14 * L, 2)} cm',
             f'In 60 min the hand turns 2π, so in {t} min it turns {s} rad (2); distance = rθ = {g(L)} × {s} = {num(float(ang) * 3.14 * L, 2)} cm (1).',
             [f'{num(float(ang) * 3.14 * L * 2, 2)} cm', f'{num(t * 6 * L, 2)} cm', f'{num(float(ang) * 3.14 * L / 2, 2)} cm'])


def c3s1_wheel(r):
    rpm = r.choice([180, 300, 360, 450, 600, 720])
    w = Fr(rpm * 2, 60)
    return Q(f'A wheel makes {rpm} revolutions in one minute. Through how many radians does it turn in one second?', f'{fs(w)}π',
             f'Revolutions per second = {rpm}/60 = {fs(Fr(rpm, 60))} (1); each revolution is 2π rad (1); angle = {fs(Fr(rpm, 60))} × 2π = {fs(w)}π rad (1).',
             [f'{fs(w / 2)}π', f'{rpm * 2}π', f'{fs(Fr(rpm, 60))}π'])


c3s1_terms = term_mcq([('1 radian', 'the angle subtended at the centre by an arc equal in length to the radius'), ('1 degree', '1/360 of a complete revolution'),
                       ('π radians', '180°'), ('relation between arc, radius and angle', 'l = rθ, θ in radians'), ('1 minute (1′)', '1/60 of a degree')],
                      'Which of the following is {a}?', 'Which term is {b}?', '{a}: {b}.')

c3s1_tf = tf_mcq('degree and radian measure',
                 ['π radians = 180°.', '1 radian ≈ 57° 16′.', 'l = rθ holds only when θ is in radians.', 'A complete revolution is 2π radians.'],
                 ['1 radian = 1°.', 'π radians = 360°.', 'l = rθ holds when θ is in degrees.', '1° = π radians.'])

c3s1_ar = pool_ar([
    ('An arc of length 5 cm in a circle of radius 5 cm subtends 1 radian at the centre.', 'θ = l/r in radians.', 'a', 'R explains A.'),
    ('The minute hand of a clock turns through π radians in 30 minutes.', 'The minute hand turns through 2π radians in 60 minutes.', 'a', 'R explains A.'),
    ('1 radian is larger than 60°.', '1 radian ≈ 57.3°.', 'd', 'A is false; R is true.'),
])

c3s1_explain = pool_txt([
    ('Define one radian and show that π radians = 180°.', 'Angle subtended by an arc equal to the radius; full circle has arc 2πr, i.e. 2π rad = 360°.', '2 marks.'),
    ('Why must θ be in radians in the formula l = rθ?', 'The radian is defined as arc/radius; in degrees the formula needs a factor π/180.', '2 marks.'),
])


# st2 trigonometric functions of any angle

SPECIAL = {0: ('0', '1', '0'), 30: ('1/2', '√3/2', '1/√3'), 45: ('1/√2', '1/√2', '1'), 60: ('√3/2', '1/2', '√3'), 90: ('1', '0', 'not defined')}


def _neg(s):
    if s in ('0', 'not defined'):
        return s
    return s[1:] if s.startswith('−') else '−' + s


def _trig_val(fn, deg):
    """exact value of sin/cos/tan at deg (multiple of 30 or 45)."""
    d = deg % 360
    ref = {0: 0, 90: 90, 180: 0, 270: 90}.get(d)
    if ref is None:
        if d < 90:
            ref = d
        elif d < 180:
            ref = 180 - d
        elif d < 270:
            ref = d - 180
        else:
            ref = 360 - d
    i = {'sin': 0, 'cos': 1, 'tan': 2}[fn]
    v = SPECIAL[ref][i]
    s = math.sin(math.radians(d)) if fn == 'sin' else math.cos(math.radians(d)) if fn == 'cos' else (math.tan(math.radians(d)) if d % 180 != 90 else None)
    if v == 'not defined':
        return v
    if s is not None and s < -1e-9:
        v = _neg(v)
    return v


def c3s2_val(r):
    fn = r.choice(['sin', 'cos', 'tan'])
    base = r.choice([30, 45, 60, 120, 135, 150, 210, 225, 240, 300, 315, 330])
    k = r.choice([1, 2, 3, -1, -2])
    deg = base + 360 * k if r.random() < 0.6 else -base
    v = _trig_val(fn, deg)
    if v == 'not defined':
        raise ValueError
    ws = [_neg(v), _trig_val('cos' if fn == 'sin' else 'sin', deg), _trig_val(fn, deg + 90)]
    ws = [w for w in ws if w not in (v, 'not defined')] + ['0', '1', '−1', '1/2']
    return Q(f'Find the value of {fn} ({deg}°).'.replace('(-', '(−'), v, f'{deg}° = {deg % 360}° {"+" if deg - deg % 360 >= 0 else "−"} {abs(deg - deg % 360)}°, so {fn} {deg}° = {fn} {deg % 360}° = {v}.'.replace('-', '−'), ws)


def c3s2_sign(r):
    q = r.choice([1, 2, 3, 4])
    fn = r.choice(['sin', 'cos', 'tan'])
    pos = {1: {'sin', 'cos', 'tan'}, 2: {'sin'}, 3: {'tan'}, 4: {'cos'}}[q]
    ans = 'positive' if fn in pos else 'negative'
    return mcq(f'If x lies in the {ordn(q)} quadrant, the sign of {fn} x is', ans, ['negative' if ans == 'positive' else 'positive', 'zero', 'cannot be decided'],
               f'In quadrant {["I", "II", "III", "IV"][q - 1]} the positive functions are: {", ".join(sorted(pos))} (and their reciprocals).', r)


TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29)]


def c3s2_quad(r):
    a, b, c = r.choice(TRIPLES)
    q = r.choice([2, 3, 4])
    given = r.choice(['sin', 'cos', 'tan'])
    sx = Fr(a, c) * (1 if q in (1, 2) else -1)
    cx = Fr(b, c) * (1 if q in (1, 4) else -1)
    tx = sx / cx
    gv = {'sin': sx, 'cos': cx, 'tan': tx}[given]
    rest = [k for k in ('sin', 'cos', 'tan') if k != given]
    vals = {'sin': sx, 'cos': cx, 'tan': tx}
    ans = '; '.join(f'{k} x = {fs(vals[k])}' for k in rest) + f'; sec x = {fs(1 / cx)}'
    return Q(f'If {given} x = {fs(gv)} and x lies in the {ordn(q)} quadrant, find the values of the other trigonometric functions (state the remaining two of sin, cos, tan and sec x).', ans,
             f'Use sin²x + cos²x = 1 (or 1 + tan²x = sec²x) (1); the sign follows the quadrant (1); values (1).', ['; '.join(f'{k} x = {fs(abs(vals[k]))}' for k in rest) + f'; sec x = {fs(abs(1 / cx))}'])


c3s2_domain = term_mcq([('sin x', 'domain R, range [−1, 1]'), ('cos x', 'domain R, range [−1, 1], even function'), ('tan x', 'domain R − {(2n + 1)π/2}, range R'),
                        ('cosec x', 'domain R − {nπ}, range R − (−1, 1)'), ('sec x', 'domain R − {(2n + 1)π/2}, range R − (−1, 1)'), ('cot x', 'domain R − {nπ}, range R')],
                       'Which of the following gives the domain and range of {a}?', 'Which function has {b}?', '{a}: {b}.')

c3s2_tf = tf_mcq('trigonometric functions',
                 ['sin(−x) = −sin x.', 'cos(−x) = cos x.', 'sin x and cos x have period 2π.', 'tan x has period π.', 'sin²x + cos²x = 1 for every real x.'],
                 ['cos(−x) = −cos x.', 'tan x has period 2π only.', 'The range of sin x is R.', 'sec x can take the value 1/2.', 'tan x is defined at x = π/2.'])

c3s2_ar = pool_ar([
    ('sin 765° = 1/√2.', '765° = 2 × 360° + 45° and sine has period 360°.', 'a', 'R explains A.'),
    ('tan x is not defined at x = π/2.', 'cos(π/2) = 0.', 'a', 'tan x = sin x/cos x; R explains A.'),
    ('cos x is negative in the fourth quadrant.', 'In the fourth quadrant x-coordinates of points on the unit circle are positive.', 'd', 'A is false; R is true.'),
])

c3s2_explain = pool_txt([
    ('Why can sec x never lie strictly between −1 and 1?', '|cos x| ≤ 1, so |sec x| = 1/|cos x| ≥ 1.', '2 marks.'),
    ('Using the unit circle, explain why sin x is positive in the second quadrant but cos x is negative.', 'In quadrant II the point (cos x, sin x) has negative x-coordinate and positive y-coordinate.', '2 marks.'),
])


def c3s2_period(r):
    fn, k = r.choice([('sin', 2), ('cos', 3), ('tan', 2), ('sin', 4), ('cos', 2), ('tan', 3)])
    per = Fr(2, k) if fn != 'tan' else Fr(1, k)
    s = ('' if per.numerator == 1 else str(per.numerator)) + 'π' + ('' if per.denominator == 1 else f'/{per.denominator}')
    others = []
    for o in ['2π', 'π', f'{k}π', f'π/{2 * k}', f'2π/{k}', f'π/{k}', f'{2 * k}π']:
        if o != s and o not in others:
            others.append(o)
    return mcq(f'The fundamental period of {fn} {k}x is', s, r.sample(others[:5], 3), f'{"sin, cos" if fn != "tan" else "tan"} has period {"2π" if fn != "tan" else "π"}; dividing by {k} gives {s}.', r)


# st3 sum and difference formulae

EXACT = {
    ('sin', 75): '(√6 + √2)/4', ('cos', 75): '(√6 − √2)/4', ('sin', 15): '(√6 − √2)/4', ('cos', 15): '(√6 + √2)/4',
    ('tan', 15): '2 − √3', ('tan', 75): '2 + √3', ('sin', 105): '(√6 + √2)/4', ('cos', 105): '(√2 − √6)/4', ('tan', 105): '−(2 + √3)',
}


def c3s3_exact(r):
    (fn, d), v = r.choice(list(EXACT.items()))
    a, b = {15: (45, 30), 75: (45, 30), 105: (60, 45)}[d]
    op = '−' if d == 15 else '+'
    ws = [x for x in set(EXACT.values()) if x != v]
    return mcq(f'Find the exact value of {fn} {d}°.', v, r.sample(ws, 3), f'{d}° = {a}° {op} {b}°; apply the {fn}({"A − B" if op == "−" else "A + B"}) formula: {v}.', r)


def c3s3_combo(r):
    kind = r.choice(['sin+', 'cos+', 'cos-'])
    ang = r.choice([30, 45, 60, 90, 120, 135, 150])
    if kind == 'cos-':
        b = r.choice([5, 10, 15, 20, 25, 35, 40, 50, 55, 65, 70])
        a = ang + b
    else:
        a = r.choice([x for x in range(5, ang, 5) if 2 * x != ang and x % 15])
        b = ang - a
    if kind == 'sin+':
        t, ang, fn = f'sin {a}° cos {b}° + cos {a}° sin {b}°', a + b, 'sin'
    elif kind == 'cos+':
        t, ang, fn = f'cos {a}° cos {b}° − sin {a}° sin {b}°', a + b, 'cos'
    else:
        t, ang, fn = f'cos {a}° cos {b}° + sin {a}° sin {b}°', a - b, 'cos'
    if ang % 30 and ang % 45:
        raise ValueError
    v = _trig_val(fn, ang)
    return Q(f'Find the value of {t}.', v, f'This is {fn}({a}° {"+" if ang == a + b else "−"} {b}°) = {fn} {ang}° = {v}.', [_neg(v), _trig_val('cos' if fn == 'sin' else 'sin', ang), '1'])


def c3s3_given(r):
    (a1, b1, c1), (a2, b2, c2) = r.sample(TRIPLES[:4], 2)
    sA, cA = Fr(a1, c1), Fr(b1, c1)
    cB, sB = Fr(b2, c2), Fr(a2, c2)
    which = r.choice(['sin(A + B)', 'cos(A + B)', 'sin(A − B)', 'cos(A − B)'])
    v = {'sin(A + B)': sA * cB + cA * sB, 'cos(A + B)': cA * cB - sA * sB, 'sin(A − B)': sA * cB - cA * sB, 'cos(A − B)': cA * cB + sA * sB}[which]
    return Q(f'If sin A = {fs(sA)} and cos B = {fs(cB)}, where A and B are acute, find {which}.', fs(v),
             f'cos A = {fs(cA)}, sin B = {fs(sB)} (from sin² + cos² = 1, acute angles) (2); apply the formula (2) = {fs(v)} (1).',
             [fs(sA * cB + cA * sB) if which != 'sin(A + B)' else fs(sA * cB - cA * sB), fs(sA * sB + cA * cB) if which != 'cos(A − B)' else fs(cA * cB - sA * sB), fs(sA + cB)])


def c3s3_tan(r):
    a = Fr(r.randint(1, 5), r.choice([1, 2, 3]))
    b = Fr(r.randint(1, 5), r.choice([1, 2, 3, 4]))
    plus = r.random() < 0.5
    den = 1 - a * b if plus else 1 + a * b
    if den == 0:
        raise ValueError
    v = (a + b) / den if plus else (a - b) / den
    return Q(f'If tan A = {fs(a)} and tan B = {fs(b)}, find tan(A {"+" if plus else "−"} B).', fs(v),
             f'tan(A {"+" if plus else "−"} B) = (tan A {"+" if plus else "−"} tan B)/(1 {"−" if plus else "+"} tan A tan B) (1) = {fs(a + b if plus else a - b)}/{fs(den)} = {fs(v)} (2).',
             [fs((a + b) / (1 + a * b)) if plus else fs((a - b) / (1 - a * b)) if a * b != 1 else '0', fs(a + b if plus else a - b), fs(a * b)])


c3s3_terms = term_mcq([('sin(x + y)', 'sin x cos y + cos x sin y'), ('cos(x + y)', 'cos x cos y − sin x sin y'), ('sin(x − y)', 'sin x cos y − cos x sin y'),
                       ('cos(x − y)', 'cos x cos y + sin x sin y'), ('tan(x + y)', '(tan x + tan y)/(1 − tan x tan y)'), ('tan(x − y)', '(tan x − tan y)/(1 + tan x tan y)')],
                      'Which of the following equals {a}?', 'Which expression equals {b}?', '{a} = {b}.')

c3s3_tf = tf_mcq('compound angle formulae',
                 ['cos(π/2 − x) = sin x.', 'sin(π − x) = sin x.', 'cos(π + x) = −cos x.', 'tan(π + x) = tan x.', 'sin(x + y) ≠ sin x + sin y in general.'],
                 ['sin(x + y) = sin x + sin y.', 'cos(π − x) = cos x.', 'cos(x − y) = cos x cos y − sin x sin y.', 'tan(π − x) = tan x.', 'sin(π + x) = sin x.'])

c3s3_ar = pool_ar([
    ('cos 15° = (√6 + √2)/4.', 'cos(45° − 30°) = cos 45° cos 30° + sin 45° sin 30°.', 'a', 'R explains A.'),
    ('sin 75° = sin 45° + sin 30°.', 'sin(x + y) = sin x cos y + cos x sin y.', 'd', 'A is false; R is true.'),
    ('tan 45° + tan 0° = tan 45°.', 'tan 0° = 0.', 'a', 'R explains A.'),
])

c3s3_long = pool_txt([
    ('Prove that cos(x + y) = cos x cos y − sin x sin y using the unit circle.', 'Identity proved', 'Points on the unit circle (1); equal chords P₁P₃ = P₂P₄ (2); distance formula and simplify (2).'),
    ('Prove that sin(x + y)/sin(x − y) = (tan x + tan y)/(tan x − tan y).', 'Identity proved', 'Expand numerator and denominator (2); divide by cos x cos y (2); conclude (1).'),
    ('Prove that tan 3x tan 2x tan x = tan 3x − tan 2x − tan x.', 'Identity proved', 'tan 3x = tan(2x + x) (2); cross-multiply (2); rearrange (1).'),
])

c3s3_explain = pool_txt([
    ('Show that sin(π/2 + x) = cos x using the formula for sin(A + B).', 'sin(π/2)cos x + cos(π/2)sin x = cos x.', '2 marks.'),
    ('Why is sin(A + B) not equal to sin A + sin B? Give a counter-example.', 'A = B = 45°: sin 90° = 1 but sin 45° + sin 45° = √2.', '2 marks.'),
])


# st4 multiple angles, sum-to-product

def c3s4_double(r):
    a, b, c = r.choice(TRIPLES[:4])
    sx, cx = Fr(a, c), Fr(b, c)
    which = r.choice(['sin 2x', 'cos 2x', 'tan 2x'])
    v = {'sin 2x': 2 * sx * cx, 'cos 2x': cx * cx - sx * sx, 'tan 2x': 2 * (sx / cx) / (1 - (sx / cx) ** 2)}[which]
    return Q(f'If sin x = {fs(sx)} and x is acute, find {which}.', fs(v), f'cos x = {fs(cx)} (1); {which} = {"2 sin x cos x" if which == "sin 2x" else "cos²x − sin²x" if which == "cos 2x" else "2 tan x/(1 − tan²x)"} = {fs(v)} (1).',
             [fs(2 * sx), fs(sx * cx), fs(1 - 2 * cx * cx), fs(-v)])


def c3s4_triple(r):
    s = Fr(r.randint(1, 4), r.choice([3, 4, 5]))
    if s >= 1:
        raise ValueError
    which = r.choice(['sin', 'cos'])
    v = 3 * s - 4 * s ** 3 if which == 'sin' else 4 * s ** 3 - 3 * s
    return Q(f'If {which} x = {fs(s)}, find {which} 3x.', fs(v), f'{which} 3x = {"3 sin x − 4 sin³x" if which == "sin" else "4 cos³x − 3 cos x"} (1) = {fs(v)} (1).', [fs(3 * s), fs(-v), fs(3 * s + 4 * s ** 3)])


def c3s4_half(r):
    a, b, c = r.choice(TRIPLES[:4])
    q = r.choice([2, 3])
    cx = Fr(-b, c)
    lo = 90 if q == 2 else 180
    s_half = surd((1 - cx) / 2)
    c_half = surd((1 + cx) / 2)
    c_sign = '' if q == 2 else '−'
    return Q(f'If cos x = {fs(cx)} and x lies in the {ordn(q)} quadrant, find sin(x/2) and cos(x/2).', f'sin(x/2) = {s_half}, cos(x/2) = {c_sign}{c_half}',
             f'{lo}° < x < {lo + 90}° ⇒ {lo // 2}° < x/2 < {(lo + 90) // 2}°, so sin(x/2) > 0 and cos(x/2) {"> 0" if q == 2 else "< 0"} (1); sin²(x/2) = (1 − cos x)/2 = {fs((1 - cx) / 2)} (2); cos²(x/2) = (1 + cos x)/2 = {fs((1 + cx) / 2)} (2).',
             [f'sin(x/2) = {c_half}, cos(x/2) = {c_sign}{s_half}', f'sin(x/2) = −{s_half}, cos(x/2) = {c_half}', f'sin(x/2) = {fs((1 - cx) / 2)}, cos(x/2) = {fs((1 + cx) / 2)}'])


S2P = [('sin 75° + sin 15°', '2 sin 45° cos 30°', '√6/2'), ('sin 75° − sin 15°', '2 cos 45° sin 30°', '1/√2'), ('cos 75° + cos 15°', '2 cos 45° cos 30°', '√6/2'),
       ('cos 15° − cos 75°', '2 sin 45° sin 30°', '1/√2'), ('sin 105° + sin 15°', '2 sin 60° cos 45°', '√6/2'), ('cos 105° + cos 15°', '2 cos 60° cos 45°', '1/√2'),
       ('cos 20° + cos 100° + cos 140°', 'cos 20° + 2 cos 120° cos 20°', '0'), ('sin 50° − sin 70° + sin 10°', 'sin 10° − 2 cos 60° sin 10°', '0')]


def c3s4_s2p(r):
    e, step, v = r.choice(S2P)
    ws = [x for x in ('√6/2', '1/√2', '0', '√3/2', '1', '1/2') if x != v]
    return mcq(f'Using sum-to-product formulae, find the value of {e}.', v, r.sample(ws, 3), f'{e} = {step} = {v}.', r)


c3s4_terms = term_mcq([('sin 2x', '2 sin x cos x'), ('cos 2x', 'cos²x − sin²x = 1 − 2 sin²x'), ('tan 2x', '2 tan x/(1 − tan²x)'), ('sin 3x', '3 sin x − 4 sin³x'),
                       ('cos 3x', '4 cos³x − 3 cos x'), ('cos x + cos y', '2 cos((x + y)/2) cos((x − y)/2)'), ('sin x − sin y', '2 cos((x + y)/2) sin((x − y)/2)')],
                      'Which of the following equals {a}?', 'Which expression equals {b}?', '{a} = {b}.')

c3s4_tf = tf_mcq('multiple-angle formulae',
                 ['cos 2x = 2 cos²x − 1.', 'sin 2x = 2 tan x/(1 + tan²x).', '1 − cos 2x = 2 sin²x.', 'cos 2x = (1 − tan²x)/(1 + tan²x).'],
                 ['sin 2x = 2 sin x.', 'cos 2x = 2 sin²x − 1.', 'tan 2x = 2 tan x/(1 + tan²x).', 'sin 3x = 3 sin x + 4 sin³x.'])

c3s4_ar = pool_ar([
    ('sin 2x = 2 sin x cos x.', 'sin(x + x) = sin x cos x + cos x sin x.', 'a', 'R explains A.'),
    ('cos 2x can be negative.', 'cos 2x = 1 − 2 sin²x and sin²x can exceed 1/2.', 'a', 'R explains A.'),
    ('sin 2x = 2 sin x for all x.', 'sin 2x = 2 sin x cos x.', 'd', 'A is false; R is true.'),
])

c3s4_long = pool_txt([
    ('Prove that (cos 4x + cos 3x + cos 2x)/(sin 4x + sin 3x + sin 2x) = cot 3x.', 'Identity proved', 'Pair cos 4x + cos 2x = 2 cos 3x cos x (2); similarly sines (2); factor and cancel (1).'),
    ('Prove that cos²x + cos²(x + π/3) + cos²(x − π/3) = 3/2.', 'Identity proved', 'Use cos²θ = (1 + cos 2θ)/2 (2); sum-to-product on cos terms (2); simplify (1).'),
    ('Prove that sin 3x = 3 sin x − 4 sin³x.', 'Identity proved', 'sin(2x + x) expanded (2); substitute double-angle formulae (2); simplify (1).'),
])

c3s4_explain = pool_txt([
    ('Show that 2 sin²x = 1 − cos 2x and use it to find sin 15°... in surd form.', 'sin²15° = (1 − cos 30°)/2 = (2 − √3)/4 ⇒ sin 15° = √(2 − √3)/2.', '2 marks.'),
    ('Express sin 5x + sin 3x as a product.', '2 sin 4x cos x.', '2 marks.'),
])


def c3s4_case(r):
    who = name(r)
    a, b, c = r.choice(TRIPLES[:3])
    return {'stem': (f'{who} is designing a ramp. The ramp makes an acute angle x with the ground where sin x = {a}/{c}. A second, steeper ramp is to make angle 2x with the ground.\n'
                     '(i) Find cos x. (ii) Find sin 2x. (iii) Find cos 2x. (iv) Is angle 2x acute or obtuse? Give a reason.'),
            'answer': f'(i) {fs(Fr(b, c))} (ii) {fs(Fr(2 * a * b, c * c))} (iii) {fs(Fr(b * b - a * a, c * c))} (iv) {"acute" if b > a else "obtuse"}, since cos 2x is {"positive" if b > a else "negative"}',
            'key': '(i) Pythagoras (1). (ii) 2 sin x cos x (1). (iii) cos²x − sin²x (1). (iv) sign of cos 2x (1).'}


# ======================================================== ch04 Complex Numbers and Quadratic Equations
# st1 powers of i

def ipow(n):
    return ['1', 'i', '−1', '−i'][n % 4]


def c4s1_pow(r):
    n = r.choice([r.randint(5, 120), -r.randint(1, 40)])
    return Q(f'Evaluate i{sup(n)}.', ipow(n), f'i⁴ = 1, so i{sup(n)} = i{sup(n % 4)} = {ipow(n)} ({n} = 4 × {n // 4} + {n % 4}).', [ipow(n + 1), ipow(n + 2), ipow(n + 3)])


def c4s1_sum(r):
    ns = r.sample(range(5, 120), 4)
    vals = {'1': (1, 0), 'i': (0, 1), '−1': (-1, 0), '−i': (0, -1)}
    re = sum(vals[ipow(n)][0] for n in ns)
    im = sum(vals[ipow(n)][1] for n in ns)
    ans = cplx(re, im)
    return Q(f'Evaluate i{sup(ns[0])} + i{sup(ns[1])} + i{sup(ns[2])} + i{sup(ns[3])}.', ans, ' + '.join(ipow(n) for n in ns).replace('+ −', '− ') + f' = {ans}.', [cplx(re, -im), cplx(-re, im), cplx(im, re)])


def c4s1_series(r):
    n = r.choice([10, 11, 13, 20, 50, 101, 102, 103])
    s = [(1, 0), (1, 1), (0, 1), (0, 0)][n % 4]  # 1 + i + ... + i^n
    ans = cplx(*s)
    return Q(f'Find the value of 1 + i + i² + i³ + … + i{sup(n)}.', ans, f'Every four consecutive powers add to 0 (2); {n + 1} terms = 4 × {(n + 1) // 4} + {(n + 1) % 4} (1); the remaining terms give {ans} (2).',
             [cplx(s[1], s[0]), '0', cplx(-s[0], s[1])])


c4s1_tf = tf_mcq('the imaginary unit i',
                 ['i² = −1.', 'i⁴ⁿ = 1 for every integer n.', 'i + i² + i³ + i⁴ = 0.', '√(−4) = 2i.', '1/i = −i.'],
                 ['i² = 1.', '√(−4) × √(−9) = 6.', 'i³ = i.', '1/i = i.', 'i⁴ = −1.'])

c4s1_ar = pool_ar([
    ('√(−3) × √(−3) = −3.', '√(−a) = i√a for a > 0, and i² = −1.', 'a', 'R explains A.'),
    ('i¹⁰⁰ = 1.', '100 is a multiple of 4 and i⁴ = 1.', 'a', 'R explains A.'),
    ('√(−4) × √(−9) = −6.', '√a × √b = √(ab) holds when a and b are both negative.', 'c', 'A is true (2i × 3i = −6); R is false.'),
    ('i⁻¹ = i.', 'i × (−i) = 1.', 'd', 'A is false: i⁻¹ = −i; R is true.'),
])

c4s1_explain = pool_txt([
    ('Why do we need complex numbers? Give an example of an equation with no real solution.', 'x² + 1 = 0 has no real root since x² ≥ 0; i = √−1 gives roots ±i.', '2 marks.'),
    ('Explain the error in √(−4) × √(−9) = √36 = 6.', '√a√b = √(ab) needs a, b ≥ 0; correctly 2i × 3i = 6i² = −6.', '2 marks.'),
])


def c4s1_sqrt(r):
    a, b = r.choice([(4, 9), (16, 25), (4, 25), (9, 16), (1, 49), (36, 4)])
    p = int(math.isqrt(a * b))
    return mcq(f'Evaluate √(−{a}) × √(−{b}).', f'−{p}', [str(p), f'{p}i', f'−{p}i'], f'√(−{a}) = {int(math.isqrt(a))}i, √(−{b}) = {int(math.isqrt(b))}i; product = {p}i² = −{p}.', r)


# st2 algebra of complex numbers

def _rc(r):
    return Fr(r.randint(-6, 6)), Fr(r.choice([x for x in range(-6, 7) if x]))


def c4s2_add(r):
    a, b = _rc(r)
    c, d = _rc(r)
    op = r.choice(['+', '−'])
    re, im = (a + c, b + d) if op == '+' else (a - c, b - d)
    return Q(f'Express ({cplx(a, b)}) {op} ({cplx(c, d)}) in the form a + ib.', cplx(re, im), f'Add/subtract real and imaginary parts separately: {cplx(re, im)}.',
             [cplx(a + c, b - d) if op == '+' else cplx(a + c, b + d), cplx(re, -im), cplx(im, re)])


def c4s2_mul(r):
    a, b = _rc(r)
    c, d = _rc(r)
    re, im = a * c - b * d, a * d + b * c
    return Q(f'Express ({cplx(a, b)})({cplx(c, d)}) in the form a + ib.', cplx(re, im), f'(a + ib)(c + id) = (ac − bd) + i(ad + bc) = {cplx(re, im)}.',
             [cplx(a * c + b * d, a * d + b * c), cplx(a * c, b * d), cplx(re, -im)])


def c4s2_div(r):
    a, b = _rc(r)
    c, d = _rc(r)
    den = c * c + d * d
    re, im = (a * c + b * d) / den, (b * c - a * d) / den
    return Q(f'Express ({cplx(a, b)})/({cplx(c, d)}) in the form a + ib.', cplx(re, im),
             f'Multiply numerator and denominator by the conjugate {cplx(c, -d)} (1); denominator = {fs(den)} (1); result = {cplx(re, im)} (1).',
             [cplx((a * c - b * d) / den, (b * c + a * d) / den), cplx(a / c if c else a, b / d), cplx(re, -im)])


def c4s2_inv(r):
    a, b = _rc(r)
    if a == 0:
        a = Fr(r.randint(1, 5))
    den = a * a + b * b
    return Q(f'Find the multiplicative inverse of {cplx(a, b)}.', cplx(a / den, -b / den), f'z⁻¹ = z̄/|z|² = ({cplx(a, -b)})/{fs(den)} = {cplx(a / den, -b / den)}.',
             [cplx(a / den, b / den), cplx(-a, -b), cplx(1 / a, 1 / b)])


def c4s2_pow(r):
    n = r.choice([2, 3, 4, 5, 6, 8])
    sgn = r.choice([1, -1])
    z = complex(1, sgn) ** n
    ans = cplx(int(round(z.real)), int(round(z.imag)))
    return Q(f'Find ({cplx(1, sgn)}){sup(n)} in the form a + ib.', ans, f'({cplx(1, sgn)})² = {cplx(0, 2 * sgn)} (1); raise to the required power (1) ⇒ {ans}.',
             [cplx(int(round(z.real)), -int(round(z.imag))), cplx(2 ** (n // 2), 0), cplx(-int(round(z.real)), int(round(z.imag))) if z.real else cplx(int(round(z.imag)), 0)])


def c4s2_eq(r):
    x, y = Fr(r.randint(-5, 5)), Fr(r.randint(-5, 5))
    a, b = _rc(r)
    re, im = x * a - y * b, x * b + y * a
    return Q(f'Find real numbers x and y if (x + iy)({cplx(a, b)}) = {cplx(re, im)}.', f'x = {fs(x)}, y = {fs(y)}',
             f'Expand: ({term(a, "x", True)}{term(-b, "y", False)}) + i({term(b, "x", True)}{term(a, "y", False)}) (1); equate real and imaginary parts: '
             f'{term(a, "x", True)}{term(-b, "y", False)} = {fs(re)}, {term(b, "x", True)}{term(a, "y", False)} = {fs(im)} (2); solve the simultaneous equations (2).',
             [f'x = {fs(y)}, y = {fs(x)}', f'x = {fs(-x)}, y = {fs(y)}', f'x = {fs(x)}, y = {fs(-y)}'])


def c4s2_quad(r):
    p = r.randint(-6, 6)
    q = r.randint(1, 5)
    a = r.choice([1, 1, 2])
    b, c = -2 * p * a, a * (p * p + q * q)
    roots = f'{cplx(p, q)}, {cplx(p, -q)}' if p else f'±{"" if q == 1 else q}i'
    D = b * b - 4 * a * c
    return Q(f'Solve the quadratic equation {poly([a, b, c])} = 0.', f'x = {roots}', f'D = b² − 4ac = {D} < 0 (1); x = (−b ± √D)/2a = ({fs(-b)} ± {int(math.isqrt(-D))}i)/{2 * a} (1) ⇒ {roots} (1).',
             [f'x = {cplx(-p, q)}, {cplx(-p, -q)}' if p else f'x = ±{q}', f'x = {fs(p)} ± {q}', f'x = {cplx(q, p)}, {cplx(q, -p)}'])


c4s2_terms = term_mcq([('complex number', 'a number of the form a + ib, with a, b real and i² = −1'), ('real part of a + ib', 'a'), ('imaginary part of a + ib', 'b (not ib)'),
                       ('multiplicative inverse of z ≠ 0', 'z̄/|z|²'), ('equality of complex numbers', 'a + ib = c + id if and only if a = c and b = d')],
                      'Which of the following describes the {a}?', 'Which term is {b}?', '{a}: {b}.')

c4s2_tf = tf_mcq('the algebra of complex numbers',
                 ['The imaginary part of 3 − 4i is −4.', 'Addition of complex numbers is commutative.', 'Every non-zero complex number has a multiplicative inverse.',
                  'The roots of a real quadratic with D < 0 are complex conjugates.'],
                 ['The imaginary part of 3 − 4i is −4i.', 'Complex numbers can be ordered like real numbers: 2 + i > 1 + i.', 'The product of two complex numbers is always real.',
                  'A real quadratic with D < 0 has real roots.'])

c4s2_ar = pool_ar([
    ('The roots of x² + x + 1 = 0 are not real.', 'Its discriminant is negative.', 'a', 'R explains A.'),
    ('(1 + i)² = 2i.', '(1 + i)² = 1 + 2i + i².', 'a', 'R explains A.'),
    ('3 + 2i > 1 + 2i.', 'The real part 3 is greater than 1.', 'd', 'A is false: complex numbers are not ordered; R is true.'),
])

c4s2_explain = pool_txt([
    ('Why do the complex roots of a quadratic equation with real coefficients occur in conjugate pairs?', 'x = (−b ± i√(−D))/2a: the two roots differ only in the sign of the imaginary part.', '2 marks.'),
    ('Explain why we multiply by the conjugate of the denominator to divide complex numbers.', '(c + id)(c − id) = c² + d² is real, so the result separates into real and imaginary parts.', '2 marks.'),
])

c4s2_long = pool_txt([
    ('Find the real values of θ for which (3 + 2i sin θ)/(1 − 2i sin θ) is purely real.', 'θ = nπ, n ∈ Z', 'Multiply by conjugate (2); imaginary part 8 sin θ/(1 + 4 sin²θ) = 0 (2); sin θ = 0 ⇒ θ = nπ (1).'),
    ('If (x + iy)³ = u + iv, show that u/x + v/y = 4(x² − y²).', 'Proved', 'Expand (2); u = x³ − 3xy², v = 3x²y − y³ (2); divide and add (1).'),
    ('If (a + ib)/(c + id) = x + iy, prove that (a² + b²)/(c² + d²) = x² + y².', 'Proved', 'Take modulus of both sides (2); |z₁/z₂| = |z₁|/|z₂| (2); square (1).'),
])


# st3 modulus and conjugate

def c4s3_mod(r):
    a, b, c = r.choice(TRIPLES)
    sa, sb = r.choice([1, -1]), r.choice([1, -1])
    return Q(f'Find the modulus of {cplx(sa * a, sb * b)}.', str(c), f'|z| = √(a² + b²) = √({a * a} + {b * b}) = {c}.', [str(a + b), str(c * c), str(abs(a - b))])


def c4s3_conj(r):
    a, b = _rc(r)
    c, d = _rc(r)
    re, im = a * c - b * d, a * d + b * c
    return Q(f'Find the conjugate of ({cplx(a, b)})({cplx(c, d)}).', cplx(re, -im), f'Product = {cplx(re, im)} (1); conjugate changes the sign of the imaginary part: {cplx(re, -im)} (1).',
             [cplx(re, im), cplx(-re, im), cplx(-re, -im)])


def c4s3_quot(r):
    (a1, b1, c1), (a2, b2, c2) = r.sample(TRIPLES, 2)
    return Q(f'Find |({cplx(a1, b1)})/({cplx(a2, -b2)})|.', fs(Fr(c1, c2)), f'|z₁/z₂| = |z₁|/|z₂| = {c1}/{c2} = {fs(Fr(c1, c2))}.', [fs(Fr(c2, c1)), fs(Fr(a1 + b1, a2 + b2)), fs(Fr(c1 * c1, c2 * c2))])


def c4s3_zzbar(r):
    a, b = _rc(r)
    return Q(f'For z = {cplx(a, b)}, find z + z̄, z − z̄ and z z̄. Verify that z z̄ = |z|².', f'{fs(2 * a)}; {cplx(0, 2 * b)}; {fs(a * a + b * b)}',
             f'z̄ = {cplx(a, -b)} (1); z + z̄ = 2 Re z = {fs(2 * a)} (0.5); z − z̄ = 2i Im z = {cplx(0, 2 * b)} (0.5); z z̄ = a² + b² = {fs(a * a + b * b)} = |z|² (1).',
             [f'{fs(2 * a)}; {cplx(0, -2 * b)}; {fs(a * a - b * b)}', f'{cplx(0, 2 * b)}; {fs(2 * a)}; {fs(a * a + b * b)}', f'{fs(2 * a)}; {cplx(0, 2 * b)}; {fs(a * a - b * b)}'])


c4s3_terms = term_mcq([('modulus of a + ib', '√(a² + b²)'), ('conjugate of a + ib', 'a − ib'), ('z z̄', '|z|²'), ('|z₁z₂|', '|z₁||z₂|'), ('conjugate of z₁ + z₂', 'z̄₁ + z̄₂')],
                      'Which of the following equals the {a}?', 'Which quantity equals {b}?', '{a}: {b}.')

c4s3_tf = tf_mcq('modulus and conjugate',
                 ['|z| = |z̄|.', 'z + z̄ is always real.', 'z z̄ is always real and non-negative.', '|z₁z₂| = |z₁||z₂|.'],
                 ['|z₁ + z₂| = |z₁| + |z₂| always.', 'z − z̄ is always real.', 'The conjugate of a real number is its negative.', '|z| can be negative.'])

c4s3_ar = pool_ar([
    ('z z̄ is a non-negative real number.', 'z z̄ = a² + b² for z = a + ib.', 'a', 'R explains A.'),
    ('|3 + 4i| = 5.', '|a + ib| = √(a² + b²).', 'a', 'R explains A.'),
    ('|z₁ + z₂| = |z₁| + |z₂| for all z₁, z₂.', '|z₁z₂| = |z₁||z₂|.', 'd', 'A is false (only ≤ holds in general); R is true.'),
])

c4s3_explain = pool_txt([
    ('Show that a complex number z is real if and only if z = z̄.', 'z = a + ib = a − ib ⇔ 2ib = 0 ⇔ b = 0.', '2 marks.'),
    ('Show that |z₁z₂| = |z₁||z₂| for z₁ = 1 + i and z₂ = 1 − i.', 'z₁z₂ = 2; |z₁||z₂| = √2 × √2 = 2.', '2 marks.'),
])


# st4 Argand plane

def c4s4_quad(r):
    a, b = r.choice([x for x in range(-6, 7) if x]), r.choice([x for x in range(-6, 7) if x])
    q = 1 if a > 0 and b > 0 else 2 if a < 0 < b else 3 if a < 0 and b < 0 else 4
    return mcq(f'In the Argand plane, the point representing {cplx(a, b)} lies in the', f'{ordn(q)} quadrant', [f'{ordn(x)} quadrant' for x in (1, 2, 3, 4) if x != q],
               f'Point ({a}, {b}): signs of real and imaginary parts fix the quadrant.'.replace('-', '−'), r)


def c4s4_dist(r):
    (a, b, c) = r.choice(TRIPLES[:3])
    x1, y1 = r.randint(-4, 4), r.randint(-4, 4)
    x2, y2 = x1 + a * r.choice([1, -1]), y1 + b * r.choice([1, -1])
    return Q(f'Find the distance between the points representing z₁ = {cplx(x1, y1)} and z₂ = {cplx(x2, y2)} in the Argand plane.', str(c),
             f'|z₁ − z₂| = |{cplx(x1 - x2, y1 - y2)}| = √({a * a} + {b * b}) = {c}.', [str(a + b), str(c * c), str(abs(x1 + x2) + abs(y1 + y2))])


c4s4_mcq = pool_mcq([
    ('In the Argand plane, z and z̄ are', 'mirror images of each other in the real axis', ['mirror images in the imaginary axis', 'the same point', 'symmetric about the origin'], 'z̄ = a − ib.'),
    ('In the Argand plane, z and −z are', 'symmetric about the origin', ['mirror images in the real axis', 'mirror images in the imaginary axis', 'the same point'], '(a, b) and (−a, −b).'),
    ('|z| is the distance of the point z from', 'the origin', ['the real axis', 'the imaginary axis', 'the point 1'], '|z| = √(a² + b²).'),
    ('Purely imaginary numbers lie on', 'the imaginary (y) axis', ['the real axis', 'the line y = x', 'the unit circle'], 'Real part 0.'),
])

c4s4_tf = tf_mcq('the Argand plane',
                 ['The x-axis of the Argand plane is called the real axis.', 'The complex number 0 + ib lies on the imaginary axis.', 'The point for z̄ is the reflection of z in the real axis.',
                  '|z| is the distance of z from the origin.'],
                 ['The x-axis of the Argand plane is called the imaginary axis.', 'Real numbers lie on the imaginary axis.', 'z and z̄ are reflections in the imaginary axis.', '|z| is the sum of the coordinates.'])

c4s4_ar = pool_ar([
    ('The points z and z̄ are equidistant from the origin.', '|z| = |z̄|.', 'a', 'R explains A.'),
    ('The number 5 lies on the real axis of the Argand plane.', 'Its imaginary part is zero.', 'a', 'R explains A.'),
    ('The point −3 + 2i lies in the fourth quadrant.', 'Its real part is negative and its imaginary part is positive.', 'd', 'A is false: it is in the second quadrant; R is true.'),
])

c4s4_explain = pool_txt([
    ('Plot z = 2 + 3i, its conjugate and −z in the Argand plane and describe their positions.', 'z̄ = 2 − 3i is the reflection in the real axis; −z = −2 − 3i is the reflection in the origin.', '2 marks.'),
])


# ======================================================== ch05 Linear Inequalities
# st1 algebraic solution

def _iq(r):
    return r.choice(['<', '≤', '>', '≥'])


FLIP = {'<': '>', '>': '<', '≤': '≥', '≥': '≤'}


def c5s1_simple(r):
    a = r.randint(2, 9)
    b = r.randint(-9, 9)
    c = r.randint(-20, 30)
    s = _iq(r)
    x = Fr(c - b, a)
    return Q(f'Solve {lin(a, b)} {s} {c} for real x.'.replace(' -', ' −'), f'x {s} {fs(x)}', f'{a}x {s} {c - b} (1) ⇒ x {s} {fs(x)} (dividing by a positive number keeps the sign) (1).'.replace(' -', ' −'),
             [f'x {FLIP[s]} {fs(x)}', f'x {s} {fs(Fr(c + b, a))}', f'x {s} {fs(c - b)}'])


def c5s1_neg(r):
    a = -r.randint(2, 7)
    b = r.randint(-9, 9)
    c = r.randint(-20, 20)
    s = _iq(r)
    x = Fr(c - b, a)
    return Q(f'Solve {lin(a, b)} {s} {c} for real x.'.replace(' -', ' −'), f'x {FLIP[s]} {fs(x)}',
             f'{a}x {s} {c - b} (1); dividing by the negative number {a} reverses the sign (1): x {FLIP[s]} {fs(x)}.'.replace(' -', ' −'), [f'x {s} {fs(x)}', f'x {FLIP[s]} {fs(-x)}', f'x {s} {fs(-x)}'])


def c5s1_both(r):
    a, c = r.sample(range(-6, 9), 2)
    if a == c:
        raise ValueError
    b, d = r.randint(-10, 10), r.randint(-10, 10)
    s = _iq(r)
    k = a - c
    x = Fr(d - b, k)
    ss = s if k > 0 else FLIP[s]
    return Q(f'Solve {lin(a, b)} {s} {lin(c, d)}.'.replace(' -', ' −'), f'x {ss} {fs(x)}', f'({fs(a)} − ({fs(c)}))x {s} {d} − ({b}) ⇒ {k}x {s} {d - b} (1); {"divide by " + str(k) if k > 0 else "divide by the negative number " + str(k) + " and reverse the sign"} ⇒ x {ss} {fs(x)} (2).'.replace('-', '−'),
             [f'x {FLIP[ss]} {fs(x)}', f'x {ss} {fs(-x)}', f'x {ss} {fs(Fr(d + b, k))}'])


def c5s1_frac(r):
    p, q = r.sample([2, 3, 4, 5, 6], 2)
    c = r.randint(1, 8)
    s = r.choice(['≥', '<'])
    coef = Fr(1, p) + Fr(1, q)
    x = Fr(c) / coef
    return Q(f'Solve x/{p} + x/{q} {s} {c}.', f'x {s} {fs(x)}', f'LCM {p * q // math.gcd(p, q)}: ({fs(coef)})x {s} {c} (1) ⇒ x {s} {fs(x)} (2).', [f'x {FLIP[s]} {fs(x)}', f'x {s} {fs(Fr(c * p * q, p + q + 1))}', f'x {s} {fs(c * coef)}'])


def c5s1_double(r):
    a = r.choice([2, 3, 4, 5, -2, -3])
    b = r.randint(-6, 6)
    d = r.choice([2, 3, 4, 5])
    lo, hi = r.randint(-6, 0), r.randint(1, 7)
    x1, x2 = Fr(lo * d - b, a), Fr(hi * d - b, a)
    if a > 0:
        ans = f'{fs(x1)} ≤ x < {fs(x2)}, i.e. [{fs(x1)}, {fs(x2)})'
    else:
        ans = f'{fs(x2)} < x ≤ {fs(x1)}, i.e. ({fs(x2)}, {fs(x1)}]'
    return Q(f'Solve {lo} ≤ ({lin(a, b)})/{d} < {hi}.'.replace('-', '−'), ans,
             f'Multiply through by {d}: {lo * d} ≤ {lin(a, b)} < {hi * d} (1); subtract {b} (1); divide by {a}{", reversing both signs" if a < 0 else ""} (2); write as an interval (1).'.replace('-', '−'),
             [f'{fs(x1)} < x ≤ {fs(x2)}', f'{fs(Fr(lo - b, a))} ≤ x < {fs(Fr(hi - b, a))}', f'{fs(x2)} ≤ x < {fs(x1)}'])


def c5s1_int(r):
    a = r.randint(2, 6)
    b = r.randint(-5, 10)
    c = r.randint(10, 40)
    dom = r.choice(['N', 'Z'])
    xm = Fr(c - b, a)
    xs = [x for x in range(-3 if dom == 'Z' else 1, math.ceil(xm)) if a * x + b < c]
    if not xs:
        raise ValueError
    if dom == 'Z':
        ans = f'{{…, {", ".join(str(x) for x in range(max(xs) - 2, max(xs) + 1))}}}'.replace('-', '−')
    else:
        ans = setstr(xs) if xs else 'φ'
    return Q(f'Solve {lin(a, b)} < {c} when x ∈ {dom}.'.replace(' -', ' −'), ans if dom == 'N' else f'x ∈ Z, x ≤ {max(xs)}'.replace('-', '−'), f'x < {fs(xm)} (1); pick the {"natural numbers" if dom == "N" else "integers"} below it (1).',
             [setstr(xs + [max(xs) + 1]) if dom == 'N' else f'x ∈ Z, x < {max(xs)}', setstr(xs[:-1]) if dom == 'N' and len(xs) > 1 else f'x ∈ Z, x ≤ {max(xs) + 1}', f'x < {fs(xm)}'])


c5s1_terms = term_mcq([('linear inequality in one variable', 'an inequality of the form ax + b < 0 (or ≤, >, ≥) with a ≠ 0'),
                       ('rule for multiplying by a negative number', 'the inequality sign is reversed'), ('rule for adding a number to both sides', 'the inequality sign is unchanged'),
                       ('solution set of an inequality', 'the set of all values of the variable that satisfy it')],
                      'Which of the following describes the {a}?', 'Which term is {b}?', '{a}: {b}.')

c5s1_tf = tf_mcq('linear inequalities',
                 ['Multiplying both sides of an inequality by a negative number reverses the sign.', 'Adding the same number to both sides does not change the inequality.',
                  'The solution set of 2x > 6, x ∈ R, is (3, ∞).', 'x < 5 and x ≤ 5 have different solution sets in R.'],
                 ['Multiplying both sides by a negative number keeps the sign unchanged.', 'The solution of −3x > 9 is x > −3.', 'x < 5 and x ≤ 5 have the same solution set in R.',
                  'Dividing both sides by a negative number keeps the sign.'])

c5s1_ar = pool_ar([
    ('The solution of −2x > 8 is x < −4.', 'Dividing an inequality by a negative number reverses it.', 'a', 'R explains A.'),
    ('3x + 5 < 3x + 2 has no solution.', 'It reduces to 5 < 2, which is false.', 'a', 'R explains A.'),
    ('The solution of x/3 > −2 is x < −6.', 'Multiplying by a positive number keeps the inequality unchanged.', 'd', 'A is false: x > −6; R is true.'),
])

c5s1_explain = pool_txt([
    ('Why is the inequality sign reversed when both sides are multiplied by −1? Illustrate with 2 < 5.', '2 < 5 but −2 > −5: multiplying by −1 reflects the numbers about 0, reversing their order.', '2 marks.'),
    ('Explain why 2(x + 3) > 2x + 1 is true for every real x.', 'It simplifies to 6 > 1, which is always true; solution set R.', '2 marks.'),
])


# st2 number line, systems

def c5s2_line(r):
    a = r.randint(-5, 6)
    s = _iq(r)
    desc = {'<': 'an open circle at {a} and the line shaded to the left', '≤': 'a filled circle at {a} and the line shaded to the left',
            '>': 'an open circle at {a} and the line shaded to the right', '≥': 'a filled circle at {a} and the line shaded to the right'}
    right = desc[s].format(a=a).replace('-', '−')
    wrong = [desc[k].format(a=a).replace('-', '−') for k in desc if k != s]
    return mcq(f'The solution of x {s} {a} on the number line is shown by'.replace('-', '−'), right, wrong, 'Open circle: endpoint excluded; filled circle: included. "<" shades left.', r)


def c5s2_system(r):
    a1, b1 = r.randint(2, 5), r.randint(-6, 6)
    c1 = r.randint(-10, 15)
    a2, b2 = r.randint(2, 5), r.randint(-6, 6)
    c2 = r.randint(10, 40)
    lo = Fr(c1 - b1, a1)
    hi = Fr(c2 - b2, a2)
    if lo >= hi:
        return Q(f'Solve the system {lin(a1, b1)} ≥ {c1} and {lin(a2, b2)} < {c2}.'.replace(' -', ' −'), 'no solution', f'x ≥ {fs(lo)} and x < {fs(hi)} do not overlap.',
                 [f'[{fs(hi)}, {fs(lo)})', f'x ≥ {fs(lo)}', f'x < {fs(hi)}'])
    return Q(f'Solve the system {lin(a1, b1)} ≥ {c1} and {lin(a2, b2)} < {c2} and write the solution as an interval.'.replace(' -', ' −'), f'[{fs(lo)}, {fs(hi)})',
             f'First: x ≥ {fs(lo)} (1); second: x < {fs(hi)} (1); common part [{fs(lo)}, {fs(hi)}) (1).', [f'({fs(lo)}, {fs(hi)}]', f'[{fs(lo)}, {fs(hi)}]', f'({fs(lo)}, {fs(hi)})'])


c5s2_mcq = pool_mcq([
    ('The system x > 3 and x < 1 has', 'no solution', ['the solution 1 < x < 3', 'infinitely many solutions in (1, 3)', 'the solution x = 2'], 'The two half-lines do not overlap.'),
    ('The system x ≥ 2 and x ≤ 2 has the solution', 'x = 2 only', ['no solution', 'all real x', 'x > 2'], 'Only 2 satisfies both.'),
    ('The solution set of |x| < 3 written as an interval is', '(−3, 3)', ['[−3, 3]', '(−∞, 3)', '(3, ∞)'], '−3 < x < 3.'),
    ('The solution of x ≥ −1 and x < 4 is', '[−1, 4)', ['(−1, 4]', '(−1, 4)', '[−1, 4]'], 'Include −1, exclude 4.'),
])

c5s2_tf = tf_mcq('graphing inequalities on the number line',
                 ['A filled (dark) circle shows that the endpoint is included.', 'x > a is shown by shading to the right of a.', 'The solution of a system is the common part of the individual solutions.'],
                 ['An open circle shows that the endpoint is included.', 'x < a is shown by shading to the right of a.', 'The solution of a system is the union of the individual solutions.'])

c5s2_ar = pool_ar([
    ('The solution of x ≤ 5 on the number line is marked with a filled circle at 5.', '5 itself satisfies x ≤ 5.', 'a', 'R explains A.'),
    ('The system x > 4, x < 2 has no solution.', 'There is no real number that is both greater than 4 and less than 2.', 'a', 'R explains A.'),
    ('x < 3 is shown by shading to the right of 3.', 'Numbers less than 3 lie to the left of 3 on the number line.', 'd', 'A is false; R is true.'),
])

c5s2_explain = pool_txt([
    ('Show the solution of −2 < x ≤ 3 on the number line and explain the choice of circles.', 'Open circle at −2 (excluded), filled circle at 3 (included), segment between them shaded.', '2 marks.'),
])


# st3 word problems

def c5s3_marks(r):
    who = name(r)
    m1, m2 = r.randint(55, 85), r.randint(55, 85)
    avg = r.choice([60, 65, 70, 75, 80])
    need = 3 * avg - m1 - m2
    if need > 100 or need < 0:
        raise ValueError
    return Q(f'{who} scored {m1} and {m2} marks in the first two unit tests. Find the minimum marks needed in the third test to get an average of at least {avg}.', str(need),
             f'({m1} + {m2} + x)/3 ≥ {avg} (1) ⇒ x ≥ {3 * avg} − {m1 + m2} = {need} (2).', [str(need - 1), str(2 * avg - m1 - m2 + avg // 2), str(avg)])


def c5s3_consec(r):
    kind = r.choice(['odd', 'even'])
    lo = r.randint(5, 15)
    hi = r.randint(30, 50)
    if kind == 'odd':
        pairs = [(x, x + 2) for x in range(lo + 1, hi) if x % 2 and x > lo and x + x + 2 < hi]
    else:
        pairs = [(x, x + 2) for x in range(lo + 1, hi) if x % 2 == 0 and x > lo and x + x + 2 < hi]
    if not pairs:
        raise ValueError
    t = ', '.join(f'({a}, {b})' for a, b in pairs)
    return Q(f'Find all pairs of consecutive {kind} natural numbers, both of which are larger than {lo}, such that their sum is less than {hi}.', t,
             f'Let x and x + 2: x > {lo} and 2x + 2 < {hi} ⇒ {lo} < x < {fs(Fr(hi - 2, 2))} (2); list the {kind} values (1).')


def c5s3_temp(r):
    c1, c2 = r.choice([(30, 35), (25, 40), (20, 30), (35, 45), (10, 25)])
    f1, f2 = Fr(9, 5) * c1 + 32, Fr(9, 5) * c2 + 32
    return Q(f'The temperature in a city during a day stays between {c1} °C and {c2} °C. What is the range in degrees Fahrenheit? (F = 9C/5 + 32)', f'between {fs(f1)} °F and {fs(f2)} °F',
             f'{c1} < C < {c2}, C = 5(F − 32)/9 (1) ⇒ {c1} < 5(F − 32)/9 < {c2} (1) ⇒ {fs(f1)} < F < {fs(f2)} (1).', [f'between {fs(Fr(5, 9) * c1 + 32)} °F and {fs(Fr(5, 9) * c2 + 32)} °F', f'between {c1 + 32} °F and {c2 + 32} °F', f'between {fs(f1 - 32)} °F and {fs(f2 - 32)} °F'])


def c5s3_acid(r):
    V = r.choice([400, 600, 640, 800, 1000])
    p0 = r.choice([8, 9, 10])
    pa = r.choice([2, 3])
    lo, hi = r.choice([(4, 6), (5, 7), (4, 5)])
    if not (pa < lo < hi < p0):
        raise ValueError
    x_hi = Fr(V * (p0 - lo), lo - pa)
    x_lo = Fr(V * (p0 - hi), hi - pa)
    return Q(f'A solution of {V} litres has {p0}% acid. How many litres of a {pa}% acid solution must be added so that the acid content of the mixture is more than {lo}% but less than {hi}%?',
             f'more than {fs(x_lo)} L and less than {fs(x_hi)} L', f'Acid = {p0}% of {V} + {pa}% of x (1); {lo}% of ({V} + x) < acid < {hi}% of ({V} + x) (2); solve each side (1); combine (1).',
             [f'more than {fs(x_hi)} L and less than {fs(x_lo)} L', f'more than {fs(Fr(V * (p0 - lo), lo))} L', f'less than {fs(x_lo)} L'])


def c5s3_plan(r):
    who = name(r)
    a, b = r.choice([(199, 2), (149, 3), (249, 1.5)])
    c = r.choice([2.5, 3, 4])
    if c <= b:
        raise ValueError
    x = Fr(a) / Fr(str(c - b))
    return Q(f'{who} compares two mobile data plans: Plan A costs ₹{a} per month plus ₹{g(b)} per GB; Plan B has no fixed charge but costs ₹{g(c)} per GB. For how many GB per month is Plan A cheaper?', f'more than {num(float(x), 1)} GB',
             f'{a} + {g(b) if b != 1 else ""}x < {g(c)}x (1) ⇒ {g(c - b) if c - b != 1 else ""}x > {a} (1) ⇒ x > {num(float(x), 1)} GB (1).', [f'less than {num(float(x), 1)} GB', f'more than {num(a / c, 1)} GB', f'more than {num(a / b, 1)} GB'])


def c5s3_case(r):
    ca = r.choice([10, 12, 14])
    lo, hi = 80, 140
    return {'stem': (f'Intelligence Quotient is defined as IQ = (MA/CA) × 100, where MA is mental age and CA is chronological age. A school counsellor finds that for a group of {ca}-year-old children, 80 ≤ IQ ≤ 140.\n'
                     '(i) Write the inequality in terms of MA. (ii) Find the range of mental age of the group. (iii) What is the mental age of a child with IQ 100? (iv) Can a child in the group have MA = 20?'),
            'answer': f'(i) 80 ≤ (MA/{ca}) × 100 ≤ 140 (ii) {fs(Fr(lo * ca, 100))} ≤ MA ≤ {fs(Fr(hi * ca, 100))} (iii) {ca} (iv) {"no" if 20 > hi * ca / 100 else "yes"}',
            'key': '(i) substitute CA (1). (ii) multiply by CA/100 (1). (iii) MA = CA (1). (iv) compare with the upper limit (1).'}


c5s3_ar = pool_ar([
    ('To have an average of at least 60 in three tests after scoring 50 and 55, a student needs at least 75 in the third.', '(50 + 55 + x)/3 ≥ 60 gives x ≥ 75.', 'a', 'R explains A.'),
    ('The length of a rectangle is 3 cm more than its breadth; if the perimeter is at least 50 cm, the breadth is at least 11 cm.', '2(b + b + 3) ≥ 50 gives b ≥ 11.', 'a', 'R explains A.'),
    ('A number whose double is less than 10 must be negative.', '2x < 10 gives x < 5.', 'd', 'A is false; R is true.'),
])

c5s3_explain = pool_txt([
    ('A shopkeeper wants a profit of at least ₹500 by selling pens at ₹15 each that cost ₹10 each. Form and solve the inequality.', '5x ≥ 500 ⇒ x ≥ 100 pens.', '2 marks.'),
    ('The cost of a notebook is ₹40 and of a pen ₹15. Priya has ₹200 and must buy 2 notebooks. How many pens can she buy at most?', '80 + 15p ≤ 200 ⇒ p ≤ 8.', '2 marks.'),
])

c5s3_tf = tf_mcq('word problems on inequalities',
                 ['"At least" is written as ≥.', '"At most" is written as ≤.', '"More than" is written as >.', 'The number of objects must be a whole number, so the final answer is often a list of integers.'],
                 ['"At least" is written as ≤.', '"At most" is written as >.', '"Less than" is written as ≥.', 'A negative number of objects can be a valid answer.'])


# ======================================================== extra families (D4 coverage, D1 for word problems)

SB_PATTERNS = [
    ('k/(k + 1)', lambda k: Fr(k, k + 1)), ('k²', lambda k: Fr(k * k)), ('2k − 1', lambda k: Fr(2 * k - 1)), ('k³', lambda k: Fr(k ** 3)),
    ('3k', lambda k: Fr(3 * k)), ('1/k', lambda k: Fr(1, k)), ('2ᵏ', lambda k: Fr(2 ** k)), ('(2k − 1)/(2k)', lambda k: Fr(2 * k - 1, 2 * k)),
]


def c1s1_conv(r):
    pat, f = r.choice(SB_PATTERNS)
    n = r.randint(5, 7) if pat in ('k³', '2ᵏ') else r.randint(5, 9)
    xs = [f(k) for k in range(1, n + 1)]
    roster = '{' + ', '.join(fs(x) for x in xs) + '}'
    ans = f'{{x : x = {pat}, k ∈ N, k ≤ {n}}}'
    return Q(f'Write the set {roster} in set-builder form. How many elements does it have, and which of its elements are integers?',
             f'{ans}; {n} elements; integers: ' + (', '.join(fs(x) for x in xs if x.denominator == 1) or 'none'),
             f'Spot the pattern of the kth term: {pat} (2); k runs from 1 to {n} (1); pick out the whole-number elements (1).')


def c1s3_ops(r):
    a = r.randint(-8, 0)
    c = a + r.randint(1, 4)
    b = c + r.randint(1, 5)
    d = b + r.randint(1, 5)
    la, rb_, lc, rd = (r.random() < 0.5 for _ in range(4))
    A, B = _iv(a, b, la, rb_), _iv(c, d, lc, rd)
    union = _iv(a, d, la, rd)
    inter = _iv(c, b, lc, rb_)
    diff = _iv(a, c, la, not lc)
    return Q(f'If A = {A} and B = {B}, find A ∪ B, A ∩ B and A − B, each as an interval.', f'A ∪ B = {union}; A ∩ B = {inter}; A − B = {diff}',
             f'Mark both intervals on the number line (1); union runs from the left end of A to the right end of B (1); intersection is the overlap from {fs(c)} to {fs(b)} (1); '
             f'A − B stops where B starts, with the bracket at {fs(c)} reversed (1).',
             [f'A ∪ B = {union}; A ∩ B = {inter}; A − B = {_iv(a, c, la, lc)}', f'A ∪ B = {_iv(a, d, True, True)}; A ∩ B = {_iv(c, b, True, True)}; A − B = {diff}',
              f'A ∪ B = {union}; A ∩ B = {_iv(c, b, not lc, not rb_)}; A − B = {_iv(a, b, la, rb_)}'])


def c2s2_count_rel(r):
    m, n = r.randint(2, 4), r.randint(2, 4)
    return Q(f'A has {m} elements and B has {n} elements. Find (i) n(A × B), (ii) the number of relations from A to B, (iii) the number of relations from A to B that contain a given ordered pair (a, b).',
             f'(i) {m * n} (ii) 2{sup(m * n)} = {2 ** (m * n):,} (iii) 2{sup(m * n - 1)} = {2 ** (m * n - 1):,}'.replace(',', ','),
             f'(i) n(A × B) = {m} × {n} (1); (ii) every subset of A × B is a relation, so 2{sup(m * n)} (2); (iii) (a, b) is fixed and each of the other {m * n - 1} pairs is in or out: 2{sup(m * n - 1)} (1).',
             [f'(i) {m + n} (ii) 2{sup(m + n)} (iii) 2{sup(m + n - 1)}', f'(i) {m * n} (ii) {m * n} (iii) {m * n - 1}', f'(i) {m * n} (ii) {(m * n) ** 2} (iii) {m * n}'])


_RAT = {'0': Fr(0), '1': Fr(1), '−1': Fr(-1), '1/2': Fr(1, 2), '−1/2': Fr(-1, 2)}


def c3s2_eval(r):
    def pick():
        while True:
            fn = r.choice(['sin', 'cos', 'tan'])
            base = r.choice([30, 60, 90, 150, 180, 210, 270, 330, 0, 45, 135, 225, 315, 120, 240, 300])
            deg = base + 360 * r.choice([1, 2, 3, -1, -2, 4])
            v = _trig_val(fn, deg)
            if v in _RAT:
                return fn, deg, _RAT[v]
    (f1, d1, v1), (f2, d2, v2), (f3, d3, v3) = pick(), pick(), pick()
    tot = v1 + v2 * v3
    t = lambda f_, d_: f'{f_}({d_}°)'.replace('(-', '(−')
    return Q(f'Evaluate {t(f1, d1)} + {t(f2, d2)} × {t(f3, d3)}.', fs(tot),
             f'Reduce each angle by multiples of 360°: {t(f1, d1)} = {fs(v1)}, {t(f2, d2)} = {fs(v2)}, {t(f3, d3)} = {fs(v3)} (3); value = {fs(v1)} + ({fs(v2)})({fs(v3)}) = {fs(tot)} (1).',
             [fs(v1 + v2 + v3), fs(v1 - v2 * v3), fs(v1 * v2 * v3)])


def c4s4_plot(r):
    a, b = r.choice([x for x in range(-6, 7) if x]), r.choice([x for x in range(-6, 7) if x])
    q = lambda x, y: {(1, 1): 'I', (-1, 1): 'II', (-1, -1): 'III', (1, -1): 'IV'}[(1 if x > 0 else -1, 1 if y > 0 else -1)]
    z = cplx(a, b)
    return Q(f'Represent z = {z}, its conjugate z̄ and −z in the Argand plane. In which quadrant does each lie, and what is the distance between the points z and z̄?',
             f'z: ({fs(a)}, {fs(b)}) in quadrant {q(a, b)}; z̄: ({fs(a)}, {fs(-b)}) in quadrant {q(a, -b)}; −z: ({fs(-a)}, {fs(-b)}) in quadrant {q(-a, -b)}; distance {2 * abs(b)}',
             f'z = x + iy is the point (x, y) (1); z̄ is its reflection in the real axis and −z its reflection in the origin (2); |z − z̄| = |2iy| = {2 * abs(b)} (1).',
             [f'z in quadrant {q(a, b)}; z̄ in quadrant {q(-a, b)}; −z in quadrant {q(-a, -b)}; distance {2 * abs(a)}', f'z in quadrant {q(a, b)}; z̄ in quadrant {q(a, -b)}; −z in quadrant {q(a, -b)}; distance {abs(b)}'])


def c5s2_double(r):
    c = r.choice([2, 3, 4, 5])
    b = r.randint(-6, 8)
    d = r.choice([2, 3, 4, 5])
    lo, hi = sorted(r.sample(range(-8, 12), 2))
    # lo <= (b - c x)/d <= hi  ->  (b - d*hi)/c <= x <= (b - d*lo)/c
    xl, xh = Fr(b - d * hi, c), Fr(b - d * lo, c)
    return Q(f'Solve {fs(lo)} ≤ ({fs(b)} − {c}x)/{d} ≤ {fs(hi)} and show the solution on the number line.', f'{fs(xl)} ≤ x ≤ {fs(xh)}, i.e. [{fs(xl)}, {fs(xh)}]',
             f'Multiply by {d}: {fs(d * lo)} ≤ {fs(b)} − {c}x ≤ {fs(d * hi)} (1); subtract {pp(b)}: {fs(d * lo - b)} ≤ −{c}x ≤ {fs(d * hi - b)} (1); divide by −{c} and reverse the signs (1): '
             f'[{fs(xl)}, {fs(xh)}], drawn with filled circles at both ends (1).',
             [f'[{fs(-xh)}, {fs(-xl)}]', f'({fs(xl)}, {fs(xh)})', f'[{fs(Fr(d * lo - b, c))}, {fs(Fr(d * hi - b, c))}]'])


def c5s3_words(r):
    k = r.randint(10, 60)
    who = name(r)
    items = [
        (f"{who}'s age x is at least {k} years.", f'x ≥ {k}', [f'x ≤ {k}', f'x > {k}', f'x < {k}']),
        (f'The cost x of a ticket is at most ₹{k}.', f'x ≤ {k}', [f'x ≥ {k}', f'x < {k}', f'x > {k}']),
        (f'A lift can carry fewer than {k} people (x people).', f'x < {k}', [f'x ≤ {k}', f'x > {k}', f'x ≥ {k}']),
        (f'The marks x needed are more than {k}.', f'x > {k}', [f'x ≥ {k}', f'x < {k}', f'x ≤ {k}']),
        (f'Twice a number x is not more than {k}.', f'2x ≤ {k}', [f'2x ≥ {k}', f'2x < {k}', f'x ≤ 2 × {k}']),
    ]
    st, ans, wr = r.choice(items)
    return mcq(f'Which inequality represents the statement: "{st}"', ans, wr, '"At least" is ≥, "at most" and "not more than" are ≤, "more than" is >, "fewer/less than" is <.', r)


def pp(x):
    return fs(x) if Fr(x) >= 0 else f'({fs(x)})'


# ======================================================== families

FAMILIES = {
    S + '01-st1': [F('C1', 'D1', 'mcq', c1s1_set), F('C1', 'D2', 'mcq', c1s1_tf), F('C2', 'D2', 'explain', c1s1_explain), F('C2', 'D3', 'mcq', c1s1_ar, kinds=('ar',)),
                   F('C3', 'D1', 'short', c1s1_roster), F('C3', 'D2', 'short', c1s1_letters), F('C3', 'D2', 'mcq', c1s1_builder), F('C3', 'D1', 'short', c1s1_eq),
                   F('C3', 'D3', 'short', c1s1_int), F('C4', 'D3', 'numerical', c1s1_frac)],
    S + '01-st2': [F('C1', 'D1', 'mcq', c1s2_types), F('C1', 'D2', 'mcq', c1s2_terms), F('C1', 'D2', 'mcq', c1s2_tf), F('C2', 'D2', 'explain', c1s2_explain), F('C2', 'D3', 'mcq', c1s2_ar, kinds=('ar',)),
                   F('C3', 'D1', 'short', c1s2_power), F('C3', 'D2', 'mcq', c1s2_equal), F('C4', 'D3', 'multi_step', c1s2_list), F('C4', 'D5', 'multi_step', c1s2_diff)],
    S + '01-st3': [F('C1', 'D2', 'mcq', c1s3_tf), F('C2', 'D2', 'explain', c1s3_explain), F('C2', 'D3', 'mcq', c1s3_ar, kinds=('ar',)), F('C3', 'D1', 'short', c1s3_write),
                   F('C3', 'D2', 'short', c1s3_set), F('C4', 'D3', 'numerical', c1s3_cap)],
    S + '01-st4': [F('C1', 'D1', 'mcq', c1s4_terms), F('C1', 'D2', 'mcq', c1s4_tf), F('C2', 'D2', 'explain', c1s4_explain), F('C2', 'D3', 'mcq', c1s4_ar, kinds=('ar',)),
                   F('C3', 'D1', 'short', c1s4_ops), F('C3', 'D2', 'short', c1s4_count), F('C3', 'D3', 'numerical', c1s4_find_i), F('C4', 'D4', 'multi_step', c1s4_survey)],
    S + '01-st5': [F('C1', 'D2', 'mcq', c1s5_tf), F('C2', 'D2', 'explain', c1s5_explain), F('C2', 'D3', 'mcq', c1s5_ar, kinds=('ar',)), F('C2', 'D3', 'long', c1s5_long),
                   F('C3', 'D1', 'short', c1s5_comp), F('C3', 'D2', 'numerical', c1s5_dem), F('C3', 'D3', 'numerical', c1s5_neither), F('C4', 'D4', 'long', c1s5_three),
                   F('C4', 'D5', 'long', c1s5_exact), F('C3', 'D3', 'case', c1s5_case)],
    S + '02-st1': [F('C1', 'D2', 'mcq', c2s1_tf), F('C2', 'D2', 'explain', c2s1_explain), F('C2', 'D3', 'mcq', c2s1_ar, kinds=('ar',)), F('C3', 'D1', 'short', c2s1_n),
                   F('C3', 'D2', 'short', c2s1_list), F('C3', 'D2', 'numerical', c2s1_eq), F('C4', 'D4', 'multi_step', c2s1_find)],
    S + '02-st2': [F('C1', 'D1', 'mcq', c2s2_terms), F('C1', 'D2', 'mcq', c2s2_tf), F('C2', 'D2', 'explain', c2s2_explain), F('C2', 'D3', 'mcq', c2s2_ar, kinds=('ar',)),
                   F('C3', 'D1', 'short', c2s2_count), F('C3', 'D2', 'numerical', c2s2_dom), F('C4', 'D3', 'multi_step', c2s2_div)],
    S + '02-st3': [F('C1', 'D1', 'mcq', c2s3_terms), F('C1', 'D2', 'mcq', c2s3_tf), F('C2', 'D2', 'explain', c2s3_explain), F('C2', 'D3', 'mcq', c2s3_ar, kinds=('ar',)),
                   F('C2', 'D3', 'long', c2s3_long), F('C3', 'D1', 'short', c2s3_val), F('C3', 'D2', 'short', c2s3_special), F('C3', 'D2', 'mcq', c2s3_isf),
                   F('C4', 'D3', 'numerical', c2s3_domain), F('C4', 'D4', 'numerical', c2s3_range), F('C3', 'D3', 'case', c2s3_case)],
    S + '02-st4': [F('C1', 'D2', 'mcq', c2s4_tf), F('C2', 'D2', 'explain', c2s4_explain), F('C2', 'D3', 'mcq', c2s4_ar, kinds=('ar',)), F('C3', 'D1', 'short', c2s4_val),
                   F('C3', 'D2', 'short', c2s4_ops), F('C4', 'D3', 'numerical', c2s4_dom), F('C4', 'D4', 'long', c2s4_multi)],
    S + '03-st1': [F('C1', 'D1', 'mcq', c3s1_terms), F('C1', 'D2', 'mcq', c3s1_tf), F('C2', 'D2', 'explain', c3s1_explain), F('C2', 'D3', 'mcq', c3s1_ar, kinds=('ar',)),
                   F('C3', 'D1', 'short', c3s1_d2r), F('C3', 'D2', 'short', c3s1_r2d), F('C3', 'D3', 'numerical', c3s1_r2dms), F('C3', 'D2', 'numerical', c3s1_arc),
                   F('C4', 'D3', 'multi_step', c3s1_clock), F('C4', 'D4', 'multi_step', c3s1_wheel)],
    S + '03-st2': [F('C1', 'D1', 'mcq', c3s2_domain), F('C1', 'D2', 'mcq', c3s2_tf), F('C2', 'D2', 'explain', c3s2_explain), F('C2', 'D3', 'mcq', c3s2_ar, kinds=('ar',)),
                   F('C3', 'D1', 'mcq', c3s2_sign), F('C3', 'D2', 'short', c3s2_val), F('C3', 'D3', 'multi_step', c3s2_quad), F('C4', 'D3', 'mcq', c3s2_period)],
    S + '03-st3': [F('C1', 'D1', 'mcq', c3s3_terms), F('C1', 'D2', 'mcq', c3s3_tf), F('C2', 'D2', 'explain', c3s3_explain), F('C2', 'D3', 'mcq', c3s3_ar, kinds=('ar',)),
                   F('C2', 'D3', 'long', c3s3_long), F('C3', 'D1', 'short', c3s3_combo), F('C3', 'D2', 'mcq', c3s3_exact), F('C3', 'D3', 'numerical', c3s3_tan),
                   F('C4', 'D4', 'long', c3s3_given)],
    S + '03-st4': [F('C1', 'D1', 'mcq', c3s4_terms), F('C1', 'D2', 'mcq', c3s4_tf), F('C2', 'D2', 'explain', c3s4_explain), F('C2', 'D3', 'mcq', c3s4_ar, kinds=('ar',)),
                   F('C2', 'D3', 'long', c3s4_long), F('C3', 'D2', 'numerical', c3s4_double), F('C3', 'D3', 'mcq', c3s4_s2p), F('C4', 'D3', 'numerical', c3s4_triple),
                   F('C4', 'D4', 'long', c3s4_half), F('C3', 'D3', 'case', c3s4_case)],
    S + '04-st1': [F('C1', 'D2', 'mcq', c4s1_tf), F('C2', 'D2', 'explain', c4s1_explain), F('C2', 'D3', 'mcq', c4s1_ar, kinds=('ar',)), F('C3', 'D1', 'short', c4s1_pow),
                   F('C3', 'D2', 'short', c4s1_sum), F('C4', 'D3', 'mcq', c4s1_sqrt), F('C4', 'D4', 'long', c4s1_series)],
    S + '04-st2': [F('C1', 'D1', 'mcq', c4s2_terms), F('C1', 'D2', 'mcq', c4s2_tf), F('C2', 'D2', 'explain', c4s2_explain), F('C2', 'D3', 'mcq', c4s2_ar, kinds=('ar',)),
                   F('C3', 'D1', 'short', c4s2_add), F('C3', 'D2', 'short', c4s2_mul), F('C3', 'D3', 'numerical', c4s2_div), F('C3', 'D2', 'numerical', c4s2_inv),
                   F('C3', 'D3', 'numerical', c4s2_quad), F('C4', 'D3', 'numerical', c4s2_pow), F('C4', 'D4', 'long', c4s2_eq), F('C4', 'D5', 'long', c4s2_long)],
    S + '04-st3': [F('C1', 'D1', 'mcq', c4s3_terms), F('C1', 'D2', 'mcq', c4s3_tf), F('C2', 'D2', 'explain', c4s3_explain), F('C2', 'D3', 'mcq', c4s3_ar, kinds=('ar',)),
                   F('C3', 'D1', 'short', c4s3_mod), F('C3', 'D2', 'short', c4s3_conj), F('C4', 'D3', 'numerical', c4s3_quot), F('C4', 'D4', 'multi_step', c4s3_zzbar)],
    S + '04-st4': [F('C1', 'D2', 'mcq', c4s4_tf), F('C2', 'D2', 'explain', c4s4_explain), F('C2', 'D3', 'mcq', c4s4_ar, kinds=('ar',)), F('C3', 'D1', 'mcq', c4s4_quad),
                   F('C3', 'D2', 'short', c4s4_dist), F('C4', 'D3', 'mcq', c4s4_mcq)],
    S + '05-st1': [F('C1', 'D1', 'mcq', c5s1_terms), F('C1', 'D2', 'mcq', c5s1_tf), F('C2', 'D2', 'explain', c5s1_explain), F('C2', 'D3', 'mcq', c5s1_ar, kinds=('ar',)),
                   F('C3', 'D1', 'short', c5s1_simple), F('C3', 'D2', 'short', c5s1_neg), F('C3', 'D3', 'numerical', c5s1_both), F('C3', 'D2', 'numerical', c5s1_int),
                   F('C4', 'D3', 'numerical', c5s1_frac), F('C4', 'D4', 'long', c5s1_double)],
    S + '05-st2': [F('C1', 'D2', 'mcq', c5s2_tf), F('C2', 'D2', 'explain', c5s2_explain), F('C2', 'D3', 'mcq', c5s2_ar, kinds=('ar',)), F('C3', 'D1', 'mcq', c5s2_line),
                   F('C3', 'D3', 'numerical', c5s2_system), F('C4', 'D3', 'mcq', c5s2_mcq)],
    S + '05-st3': [F('C1', 'D2', 'mcq', c5s3_tf), F('C2', 'D2', 'explain', c5s3_explain), F('C2', 'D3', 'mcq', c5s3_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c5s3_marks),
                   F('C3', 'D3', 'multi_step', c5s3_consec), F('C4', 'D3', 'multi_step', c5s3_temp), F('C4', 'D4', 'multi_step', c5s3_plan), F('C4', 'D5', 'long', c5s3_acid),
                   F('C3', 'D3', 'case', c5s3_case)],
}

FAMILIES[S + '01-st1'].append(F('C4', 'D4', 'multi_step', c1s1_conv))
FAMILIES[S + '01-st3'].append(F('C4', 'D4', 'multi_step', c1s3_ops))
FAMILIES[S + '02-st2'].append(F('C4', 'D4', 'multi_step', c2s2_count_rel))
FAMILIES[S + '03-st2'].append(F('C4', 'D4', 'multi_step', c3s2_eval))
FAMILIES[S + '04-st4'].append(F('C4', 'D4', 'multi_step', c4s4_plot))
FAMILIES[S + '05-st2'].append(F('C4', 'D4', 'multi_step', c5s2_double))
FAMILIES[S + '05-st3'].append(F('C3', 'D1', 'mcq', c5s3_words))

FAMILIES = polish(mpolish(FAMILIES))
