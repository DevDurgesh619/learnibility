"""CBSE class 11 maths (NCERT Mathematics XI) families, chapters 6-10."""
from __future__ import annotations

import math
import re
from collections import Counter
from fractions import Fraction as Fr
from math import comb, perm, factorial

from qbank import F, ar, mcq, num, sup, frac, name, two_names, inr, CITIES  # noqa: F401
from g11_physics_util import polish, sig, g, pool_mcq, pool_ar, pool_txt, term_mcq, tf_mcq  # noqa: F401
from g11_maths_a import fs, surd, poly, lin, setstr, Q, ordn, sq_split, term, mpolish

S = 'cbse-g11-maths-ch'
_M = re.compile(r'(?<![A-Za-z])-(?=[\d(√xyabk])')


def M(s: str) -> str:
    """ASCII minus before numbers/variables -> proper minus sign."""
    return _M.sub('−', s)


def ind(n) -> str:
    """Indian digit grouping without the rupee sign: 4752000 -> 47,52,000."""
    return inr(n).replace('₹', '')


def rs2(x) -> str:
    """rupees to the paisa with Indian grouping: ₹1,23,456.70."""
    x = round(float(x) + 1e-12, 2)
    ip = int(x)
    dp = round((x - ip) * 100)
    return '₹' + ind(ip) + f'.{dp:02d}'


def pp(x) -> str:
    """number for substitution: negative values in brackets."""
    return fs(x) if Fr(x) >= 0 else f'({fs(x)})'


def pt(*xs) -> str:
    return '(' + ', '.join(fs(x) for x in xs) + ')'


# ======================================================== ch06 Permutations and Combinations
# st1 fundamental principle of counting

def c6s1_outfit(r):
    who = name(r)
    s, t, k = r.randint(3, 8), r.randint(2, 6), r.choice([0, 0, r.randint(2, 4)])
    if k:
        ans = s * t * k
        stem = f'{who} has {s} shirts, {t} pairs of trousers and {k} pairs of shoes. In how many ways can {who} choose one of each to dress for a school function?'
        key = f'By the multiplication principle: {s} × {t} × {k} = {ans}.'
        ds = [str(s + t + k), str(s * t), str(s * t * k * 2)]
    else:
        ans = s * t
        stem = f'{who} has {s} shirts and {t} pairs of trousers. In how many ways can a shirt and a pair of trousers be chosen?'
        key = f'Each shirt can go with each pair of trousers: {s} × {t} = {ans}.'
        ds = [str(s + t), str(s ** t), str(t ** s)]
    return Q(stem, str(ans), key, ds)


def c6s1_letters(r):
    l, m = r.sample([2, 3, 4, 5, 6], 2)
    return mcq(f'In how many ways can {l} different letters be posted in {m} letter boxes (any box may receive any number of letters)?', f'{m}{sup(l)}',
               [f'{l}{sup(m)}', f'{l} × {m}', f'{l}!'],
               f'Each letter has {m} choices independently, so {m} × {m} × … ({l} times) = {m}{sup(l)}.', r)


def c6s1_code(r):
    digs = r.choice([10, 9, 8, 6, 5])
    n = r.randint(3, 5)
    rep = r.random() < 0.5
    src = 'the digits 0 to 9' if digs == 10 else f'the digits 1 to {digs}'
    if rep:
        ans = digs ** n
        key = f'Each of the {n} places can be filled in {digs} ways: {digs}{sup(n)} = {ans}.'
        ds = [str(perm(digs, n)), str(digs * n), str(n ** digs if n ** digs < 10 ** 8 else digs ** (n - 1))]
    else:
        ans = perm(digs, n)
        key = f'{" × ".join(str(digs - i) for i in range(n))} = {ans} (digits not repeated).'
        ds = [str(digs ** n), str(comb(digs, n)), str(digs * n)]
    return Q(f'A {n}-digit lock code is formed using {src}{" with repetition allowed" if rep else ", no digit being repeated"} (a code may begin with any of these digits). How many codes are possible?',
             str(ans), key, ds)


def c6s1_even(r):
    digs = sorted(r.sample(range(0, 10), r.randint(5, 6)))
    n = 3
    rep = r.random() < 0.4
    kind = r.choice(['even', 'odd', 'greater'])
    import itertools
    it = itertools.product(digs, repeat=n) if rep else itertools.permutations(digs, n)
    good = []
    for t in it:
        if t[0] == 0:
            continue
        v = 100 * t[0] + 10 * t[1] + t[2]
        if kind == 'even' and v % 2 == 0 or kind == 'odd' and v % 2 == 1 or kind == 'greater' and v > 500:
            good.append(v)
    if len(good) < 2:
        raise ValueError
    allc = sum(1 for t in (itertools.product(digs, repeat=n) if rep else itertools.permutations(digs, n)) if t[0] != 0)
    what = {'even': 'even numbers', 'odd': 'odd numbers', 'greater': 'numbers greater than 500'}[kind]
    return Q(f'How many 3-digit {what} can be formed from the digits {", ".join(map(str, digs))}, {"if digits may be repeated" if rep else "if no digit is repeated"}?',
             str(len(good)), f'Fill the restricted place(s) first ({"units digit" if kind != "greater" else "hundreds digit"}), then the others, remembering 0 cannot be the hundreds digit; count = {len(good)}.',
             [str(allc), str(allc - len(good)) if allc - len(good) != len(good) else str(allc // 2 + 1), str(len(good) + (len(digs) - 1))])


def c6s1_route(r):
    a, b = r.sample(CITIES, 2)
    c = r.choice([x for x in CITIES if x not in (a, b)])
    m, n = r.randint(2, 6), r.randint(2, 5)
    ans = m * n * (m - 1) * (n - 1)
    return Q(f'There are {m} bus routes from {a} to {b} and {n} routes from {b} to {c}. In how many ways can a person travel from {a} to {c} via {b} and return, if no route is used twice?',
             str(ans), f'Onward: {m} × {n} (1); return must use different routes: ({m} − 1) × ({n} − 1) (1); total = {m * n} × {(m - 1) * (n - 1)} = {ans} (1).',
             [str((m * n) ** 2), str(m * n), str(m * n * 2)])


def c6s1_signal(r):
    k = r.randint(4, 7)
    lo, hi = sorted(r.sample(range(2, min(k, 5) + 1), 2))
    tot = sum(perm(k, i) for i in range(lo, hi + 1))
    parts = ' + '.join(f'{perm(k, i)}' for i in range(lo, hi + 1))
    return Q(f'A ship has {k} flags of different colours. A signal is made by hoisting at least {lo} and at most {hi} flags one above the other. How many different signals can be made?',
             str(tot), f'Signals with i flags: {k}P i (order matters) (1 each); total = {parts} = {tot} (1).',
             [str(sum(comb(k, i) for i in range(lo, hi + 1))), str(perm(k, hi)), str(k ** hi)])


def c6s1_case(r):
    city = r.choice(CITIES)
    L = r.choice([2, 3])
    D = r.choice([3, 4])
    with_rep = 26 ** L * 10 ** D
    no_rep = perm(26, L) * perm(10, D)
    vowel = 5 * 26 ** (L - 1) * 10 ** D
    return {'stem': (f'The transport office in {city} issues number plates with {L} English letters followed by {D} digits.\n'
                     f'(i) How many plates are possible if letters and digits may repeat? (ii) How many if no letter and no digit is repeated? '
                     f'(iii) How many (with repetition) begin with a vowel? (iv) Which principle of counting is used, and why?'),
            'answer': f'(i) {ind(with_rep)} (ii) {ind(no_rep)} (iii) {ind(vowel)} (iv) multiplication principle: the places are filled one after another, independently',
            'key': f'(i) 26{sup(L)} × 10{sup(D)} (1). (ii) 26P{L} × 10P{D} (1). (iii) 5 × 26{sup(L - 1) if L > 2 else ""} × 10{sup(D)} (1). (iv) Fundamental principle of counting (1).'.replace('26 ×', '26 ×')}


c6s1_tf = tf_mcq('the fundamental principle of counting',
                 ['If one event can occur in m ways and, after it, another in n ways, both can occur in m × n ways.',
                  'The number of 3-letter codes from 26 letters with repetition is 26³.',
                  'The principle extends to any finite number of events.',
                  'Tossing a coin 4 times gives 2⁴ = 16 possible outcomes.'],
                 ['If one event can occur in m ways and another in n ways, both can occur in m + n ways.',
                  'The number of 2-digit numbers with distinct digits is 10 × 9 = 90.',
                  'Rolling two dice gives 6 + 6 = 12 outcomes.',
                  'The principle applies only to two events.'])

c6s1_ar = pool_ar([
    ('The number of 3-digit numbers that can be formed from 1, 2, 3, 4, 5 without repetition is 60.', 'There are 5, 4 and 3 choices for the three places.', 'a', 'R explains A by the multiplication principle.'),
    ('A coin tossed 3 times has 8 outcomes.', 'Each toss has 2 outcomes and the tosses are independent.', 'a', 'R explains A: 2³ = 8.'),
    ('There are 90 two-digit numbers.', 'The tens digit can be any of 10 digits and the units digit any of 9.', 'c', 'A is true (9 × 10 = 90); R is false: the tens digit cannot be 0.'),
    ('The number of ways to answer 5 true-false questions is 10.', 'Each question has 2 possible answers.', 'd', 'A is false (2⁵ = 32); R is true.'),
])

c6s1_explain = pool_txt([
    ('State the fundamental principle of counting and illustrate it with an example.', 'If an event can occur in m ways and, following it, another in n ways, together they occur in mn ways; e.g. 3 shirts and 2 trousers give 6 outfits.', '1 + 1 marks.'),
    ('Why is the number of 4-digit numbers with distinct digits 9 × 9 × 8 × 7 and not 10 × 9 × 8 × 7?', 'The thousands digit cannot be 0, so it has 9 choices; the next digit can be 0 but not the first digit, so 9 choices, then 8 and 7.', '2 marks.'),
    ('Explain the difference between the multiplication and the addition principle with one example each.', 'Multiplication: events in sequence (choose shirt and trousers). Addition: mutually exclusive alternatives (travel by bus or by train).', '2 marks.'),
])

# st2 factorials and nPr


def c6s2_fact(r):
    n = r.randint(6, 10)
    k = r.randint(2, n - 3)
    kind = r.choice(['ratio', 'pair'])
    if kind == 'ratio':
        v = factorial(n) // (factorial(k) * factorial(n - k))
        return Q(f'Evaluate {n}!/({k}! × {n - k}!).', str(v), f'{n}!/({k}! {n - k}!) = {" × ".join(str(n - i) for i in range(min(k, n - k)))}/{min(k, n - k)}! = {v}.',
                 [str(factorial(n) // factorial(n - k)), str(factorial(n - k)), str(v * 2)])
    v = factorial(n) // factorial(n - k)
    return Q(f'Evaluate {n}!/({n - k})!.', str(v), f'{n}!/({n - k})! = {" × ".join(str(n - i) for i in range(k))} = {v}.',
             [str(v // k if v % k == 0 and v // k != v else v + n), str(factorial(n - k)), str(comb(n, k))])


def c6s2_npr(r):
    n = r.randint(5, 12)
    k = r.randint(2, 4)
    v = perm(n, k)
    return mcq(f'The value of {n}P{k} is', str(v), [str(comb(n, k)), str(n ** k), str(perm(n, k - 1)) if perm(n, k - 1) != comb(n, k) else str(v + n)],
               f'{n}P{k} = {n}!/({n} − {k})! = {" × ".join(str(n - i) for i in range(k))} = {v}.', r)


def c6s2_x(r):
    k = r.randint(4, 9)
    x = (k + 2) ** 2
    return Q(f'If 1/{k}! + 1/{k + 1}! = x/{k + 2}!, find x.', str(x),
             f'Multiply by {k + 2}!: x = {k + 2}!/{k}! + {k + 2}!/{k + 1}! = {(k + 2) * (k + 1)} + {k + 2} = {x} (1 + 1 + 1).',
             [str((k + 2) * (k + 1)), str(k + 2), str(2 * k + 3)])


def c6s2_solve(r):
    n = r.randint(6, 12)
    a, b = r.choice([(4, 2), (5, 3), (3, 2), (4, 3)])
    k = perm(n, a) // perm(n, b)
    # unique n with nPa = k nPb ?
    sols = [m for m in range(a, 40) if perm(m, a) == k * perm(m, b)]
    if sols != [n]:
        raise ValueError
    rest = ' × '.join(f'(n − {i})' for i in range(b, a))
    return Q(f'Find n if nP{a} = {k} × nP{b}.', f'n = {n}', f'nP{a}/nP{b} = {rest} = {k} (2); solve and reject non-integer or negative values (1): n = {n}.',
             [f'n = {n + 1}', f'n = {n - 1}', f'n = {k}'])


def c6s2_r(r):
    for _ in range(50):
        n = r.randint(5, 12)
        rr = r.randint(2, n)
        num_ = (n - rr + 2) * (n - rr + 1)
        if num_ % (n + 1) == 0 and num_ // (n + 1) >= 1:
            k = num_ // (n + 1)
            sols = [t for t in range(1, n + 1) if perm(n, t) * 1 == k * perm(n + 1, t - 1)]
            if sols == [rr]:
                break
    else:
        raise ValueError
    ks = '' if k == 1 else f'{k} × '
    return Q(f'Find r if {n}P r = {ks}{n + 1}P (r − 1).'.replace('P r', 'Pᵣ').replace('P (r − 1)', 'Pᵣ₋₁'), f'r = {rr}',
             f'{n}!/({n} − r)! = {k} × {n + 1}!/({n + 2} − r)! (1) ⇒ ({n + 2} − r)({n + 1} − r) = {k * (n + 1)} (2); solving and keeping 1 ≤ r ≤ {n}: r = {rr} (1).',
             [f'r = {rr + 1}', f'r = {rr - 1}', f'r = {n - rr + 1}' if n - rr + 1 != rr else f'r = {rr + 2}'])


WORDS_DISTINCT = ['MONDAY', 'NUMBER', 'EQUATION', 'DAUGHTER', 'FRIEND', 'LOGARITHM', 'PLANET', 'COMPUTER', 'GARDEN', 'MANGO', 'TIGER', 'SUNDAY']


def c6s2_words(r):
    w = r.choice(WORDS_DISTINCT)
    n = len(w)
    k = r.randint(3, min(5, n))
    allw = r.random() < 0.3
    if allw:
        return Q(f'How many words, with or without meaning, can be formed using all the letters of the word {w}, each letter used exactly once?', f'{ind(factorial(n))}',
                 f'{n} distinct letters arranged in a row: {n}! = {ind(factorial(n))}.', [f'{ind(factorial(n - 1))}', f'{ind(n ** n)}', f'{ind(factorial(n) // 2)}'])
    v = perm(n, k)
    return Q(f'How many {k}-letter words, with or without meaning, can be formed from the letters of the word {w} if no letter is repeated?', f'{ind(v)}',
             f'{n} distinct letters, {k} places: {n}P{k} = {ind(v)}.', [f'{ind(comb(n, k))}', f'{ind(n ** k)}', f'{ind(factorial(n))}'])


c6s2_terms = term_mcq([('n!', 'the product 1 × 2 × 3 × … × n'), ('0!', 'defined to be 1'), ('nPr', 'n!/(n − r)!, the number of arrangements of r out of n distinct objects'),
                       ('nPn', 'n!, the number of arrangements of all n distinct objects'), ('n × (n − 1)!', 'another way of writing n!')],
                      'Which of the following correctly describes {a}?', 'Which symbol stands for {b}?', '{a} is {b}.')

c6s2_tf = tf_mcq('factorials and permutations',
                 ['0! = 1.', 'n! = n × (n − 1)! for n ≥ 1.', 'nP0 = 1.', 'nPn = n!.', '5P2 = 20.'],
                 ['0! = 0.', '(2 + 3)! = 2! + 3!.', '(2 × 3)! = 2! × 3!.', 'nP1 = 1.', '6P2 = 15.'])

c6s2_ar = pool_ar([
    ('0! = 1.', 'Defining 0! = 1 makes nPn = n!/0! agree with n!.', 'a', 'R explains why the definition is chosen.'),
    ('The number of arrangements of 5 books on a shelf is 120.', 'n distinct objects can be arranged in a row in n! ways.', 'a', 'R explains A: 5! = 120.'),
    ('(3 + 4)! = 3! + 4!.', 'n! grows faster than any polynomial in n.', 'd', 'A is false (7! = 5040, 3! + 4! = 30); R is true.'),
    ('nPr ≥ nCr for 0 ≤ r ≤ n.', 'nPr = r! × nCr and r! ≥ 1.', 'a', 'R explains A.'),
])

c6s2_explain = pool_txt([
    ('Show that nPr = n!/(n − r)!.', 'The r places can be filled in n, n − 1, …, n − r + 1 ways; the product equals n!/(n − r)!.', '2 marks.'),
    ('Why do we define 0! = 1?', 'So that formulas like nPn = n!/(n − n)! = n! and nC0 = 1 hold.', '2 marks.'),
])

# st3 repeated objects and restrictions

WORDS_REP = ['ALLAHABAD', 'INDEPENDENCE', 'MISSISSIPPI', 'ASSASSINATION', 'BANANA', 'PERMUTATIONS', 'MATHEMATICS', 'ARRANGE', 'COMMITTEE', 'INSTITUTE',
             'PARALLEL', 'ENGINEERING', 'BALLOON', 'SUCCESS', 'TOMATO', 'KOLKATA', 'HYDERABAD', 'CHANDIGARH', 'ASSAM']


def _arr(w):
    c = Counter(w)
    v = factorial(len(w))
    for x in c.values():
        v //= factorial(x)
    return v, c


def _rep_txt(c):
    return ' '.join(f'{k}: {v}' for k, v in sorted(c.items()) if v > 1)


def c6s3_word(r):
    w = r.choice(WORDS_REP)
    v, c = _arr(w)
    den = ' '.join(f'{x}!' for x in sorted(c.values(), reverse=True) if x > 1)
    return Q(f'Find the number of arrangements of the letters of the word {w}.', f'{ind(v)}',
             f'{len(w)} letters with repeats ({_rep_txt(c)}): {len(w)}!/({den}) = {ind(v)}.', [f'{ind(factorial(len(w)))}', f'{ind(v * 2)}', f'{ind(factorial(len(c)))}'])


def c6s3_digits(r):
    ms = r.choice([[1, 2, 2, 3, 3, 3], [1, 1, 2, 2, 2], [2, 2, 3, 3, 4, 4], [5, 5, 5, 7, 7], [1, 2, 2, 2, 3, 3, 4], [4, 4, 6, 6, 6, 6]])
    v, c = _arr(ms)
    return Q(f'How many {len(ms)}-digit numbers can be formed using all the digits {", ".join(map(str, ms))}?', f'{ind(v)}',
             f'{len(ms)}!/({" ".join(f"{x}!" for x in c.values() if x > 1)}) = {ind(v)}.', [f'{ind(factorial(len(ms)))}', f'{ind(v // 2 if v % 2 == 0 else v + 1)}', f'{ind(len(ms) ** len(ms))}'][:2] + [f'{ind(v * 3)}'])


def c6s3_start(r):
    w = r.choice(WORDS_DISTINCT)
    n = len(w)
    kind = r.choice(['start', 'both', 'notstart'])
    a, b = w[0], w[-1]
    if kind == 'start':
        v = factorial(n - 1)
        q = f'begin with {a}'
        key = f'Fix {a} in the first place; arrange the other {n - 1}: {n - 1}! = {ind(v)}.'
    elif kind == 'both':
        v = factorial(n - 2)
        q = f'begin with {a} and end with {b}'
        key = f'Fix both ends; arrange the middle {n - 2}: {n - 2}! = {ind(v)}.'
    else:
        v = factorial(n) - factorial(n - 1)
        q = f'do not begin with {a}'
        key = f'Total {n}! minus those beginning with {a}, {n - 1}!: {ind(factorial(n))} − {ind(factorial(n - 1))} = {ind(v)}.'
    return Q(f'How many arrangements of all the letters of the word {w} {q}?', f'{ind(v)}', key,
             [f'{ind(factorial(n))}', f'{ind(factorial(n - 1) if kind != "start" else factorial(n - 2))}', f'{ind(factorial(n - 1) * 2)}'])


VW = set('AEIOU')


def _together(w):
    """arrangements with all vowels together (as one block)."""
    vs = [ch for ch in w if ch in VW]
    cs = [ch for ch in w if ch not in VW]
    outer, _ = _arr(cs + ['#'])
    inner, _ = _arr(vs)
    return outer * inner, outer, inner, vs, cs


def c6s3_vowels(r):
    w = r.choice(['DAUGHTER', 'EQUATION', 'MONDAY', 'PLANET', 'COMPUTER', 'ARRANGE', 'GARDEN', 'MATHEMATICS', 'BANANA', 'INSTITUTE', 'TIGER', 'SUNDAY', 'KOLKATA'])
    tot, _ = _arr(w)
    tog, outer, inner, vs, cs = _together(w)
    if len(vs) < 2:
        raise ValueError
    notall = tot - tog
    return Q(f'In how many arrangements of the letters of the word {w} do (a) all the vowels come together, (b) the vowels not all come together?', f'(a) {ind(tog)} (b) {ind(notall)}',
             f'Vowels {", ".join(vs)} as one block with the consonants {", ".join(cs) if cs else "(none)"}: {ind(outer)} ways (1); vowels inside the block: {ind(inner)} arrangement{'s' if inner > 1 else ''} (1); (a) {ind(outer)} × {ind(inner)} = {ind(tog)} (1); '
             f'(b) total {ind(tot)} − {ind(tog)} = {ind(notall)} (1).',
             [f'(a) {ind(outer)} (b) {ind(tot - outer)}', f'(a) {ind(tog)} (b) {ind(tot)}', f'(a) {ind(inner)} (b) {ind(tot - inner)}'])


def c6s3_case(r):
    w = r.choice(['ASSASSINATION', 'INDEPENDENCE', 'PERMUTATIONS', 'MISSISSIPPI', 'ALLAHABAD', 'ENGINEERING'])
    who = name(r)
    tot, c = _arr(w)
    first = w[0]
    c2 = Counter(w)
    c2[first] -= 1
    v1 = factorial(len(w) - 1)
    for x in c2.values():
        v1 //= factorial(x)
    tog, *_ = _together(w)
    return {'stem': f'In a word-puzzle club, {who} studies the arrangements of the letters of {w}.\n(i) How many letters are there and which letters repeat? (ii) How many arrangements are there in all? '
                    f'(iii) How many arrangements begin with {first}? (iv) In how many arrangements are all the vowels together?',
            'answer': f'(i) {len(w)} letters; repeats {_rep_txt(c)} (ii) {ind(tot)} (iii) {ind(v1)} (iv) {ind(tog)}',
            'key': '(i) Count letters (1). (ii) n!/(p! q! …) (1). (iii) Fix the first letter and arrange the rest, allowing for repeats (1). (iv) Vowels as one block, then arrange inside the block (1).'}


c6s3_tf = tf_mcq('permutations with repetition and restriction',
                 ['The number of arrangements of n objects of which p are alike is n!/p!.', 'The letters of BANANA can be arranged in 60 ways.',
                  'To keep certain objects together, treat them as one object and then arrange them among themselves.', 'Arrangements of AAB are 3.'],
                 ['The letters of BANANA can be arranged in 720 ways.', 'Identical objects do not affect the count of arrangements.',
                  'The number of arrangements of n objects with p alike is n! × p!.', 'Arrangements of AAB are 6.'])

c6s3_ar = pool_ar([
    ('The letters of the word ALLAHABAD can be arranged in 7560 ways.', 'There are 9 letters with A repeated 4 times and L twice.', 'a', 'R explains A: 9!/(4! 2!) = 7560.'),
    ('The number of arrangements of the letters of the word TOMATO is 180.', 'T and O each occur twice in TOMATO.', 'a', 'R explains A: 6!/(2! 2!) = 180.'),
    ('In the word DAUGHTER, the arrangements with all vowels together number 3! × 6!.', 'When the vowels are kept together they are treated as one letter.', 'a', 'R explains A: 6 units arranged in 6! ways and the vowels in 3!.'),
    ('The letters of BOOK can be arranged in 24 ways.', 'BOOK has 4 letters.', 'd', 'A is false (4!/2! = 12); R is true.'),
])

c6s3_explain = pool_txt([
    ('Why is the number of arrangements of the letters of ROOT equal to 12 and not 24?', 'The two O\'s are identical; each arrangement is counted 2! times in 4!, so 24/2 = 12.', '2 marks.'),
    ('Explain the method of finding arrangements where certain objects must always be together.', 'Tie them into one unit, arrange the units, then multiply by the arrangements within the unit.', '2 marks.'),
])

# st4 combinations


def c6s4_val(r):
    n = r.randint(6, 15)
    k = r.randint(2, 5)
    v = comb(n, k)
    return Q(f'Evaluate {n}C{k}.', str(v), f'{n}C{k} = {n}!/({k}! {n - k}!) = {v}.', [str(perm(n, k)), str(comb(n, k - 1)), str(comb(n, k + 1)) if comb(n, k + 1) != v else str(v + 1)])


def c6s4_eq(r):
    a = r.randint(2, 9)
    b = r.randint(a + 1, 14)
    n = a + b
    k = r.randint(2, 4)
    return Q(f'If nC{a} = nC{b}, find n and hence nC{k}.', f'n = {n}; {n}C{k} = {ind(comb(n, k))}', f'nCa = nCb with a ≠ b ⇒ a + b = n, so n = {n} (1); {n}C{k} = {ind(comb(n, k))} (1).',
             [f'n = {b - a}; {b - a}C{k} = {ind(comb(b - a, k))}', f'n = {n}; {n}C{k} = {ind(perm(n, k))}', f'n = {a * b}; {n}C{k} = {ind(comb(n, k))}'])


def c6s4_comm(r):
    m, w = r.randint(5, 10), r.randint(4, 8)
    a, b = r.randint(2, 4), r.randint(1, 3)
    if a > m or b > w:
        raise ValueError
    v = comb(m, a) * comb(w, b)
    return Q(f'A committee of {a} boys and {b} girl{"s" if b > 1 else ""} is to be formed from {m} boys and {w} girls of a class. In how many ways can it be done?', f'{ind(v)}',
             f'{m}C{a} × {w}C{b} = {comb(m, a)} × {comb(w, b)} = {ind(v)}.', [f'{ind(comb(m + w, a + b))}', f'{ind(comb(m, a) + comb(w, b))}', f'{ind(perm(m, a) * perm(w, b))}'])


def c6s4_atleast(r):
    g, b = r.randint(3, 6), r.randint(4, 8)
    k = r.randint(4, 5)
    lo = r.randint(1, min(3, g))
    if k > g + b:
        raise ValueError
    terms = [(i, comb(g, i) * comb(b, k - i)) for i in range(lo, min(g, k) + 1) if k - i <= b]
    v = sum(t for _, t in terms)
    parts = ' + '.join(f'{g}C{i} × {b}C{k - i}' for i, _ in terms)
    return Q(f'A team of {k} is chosen from {g} girls and {b} boys. In how many ways can this be done if the team must have at least {lo} girl{"s" if lo > 1 else ""}?', f'{ind(v)}',
             f'Cases by number of girls: {parts} (3) = {ind(v)} (1).', [f'{ind(comb(g + b, k))}', f'{ind(terms[0][1])}', f'{ind(comb(g, lo) * comb(g + b - lo, k - lo))}'])


def c6s4_geom(r):
    n = r.randint(6, 15)
    kind = r.choice(['lines', 'tri', 'diag'])
    if kind == 'lines':
        v = comb(n, 2)
        return Q(f'How many straight lines can be drawn through {n} points in a plane, no three of which are collinear?', str(v), f'Each line is fixed by a pair of points: {n}C2 = {v}.',
                 [str(perm(n, 2)), str(comb(n, 3)), str(n * 2)])
    if kind == 'tri':
        v = comb(n, 3)
        return Q(f'How many triangles can be formed by joining {n} points in a plane, no three of which are collinear?', str(v), f'Each triangle is fixed by 3 points: {n}C3 = {v}.',
                 [str(perm(n, 3)), str(comb(n, 2)), str(n * 3)])
    v = comb(n, 2) - n
    return Q(f'How many diagonals does a polygon with {n} sides have?', str(v), f'Lines joining two vertices: {n}C2 = {comb(n, 2)}; remove the {n} sides: {v}.',
             [str(comb(n, 2)), str(n * (n - 3)), str(comb(n, 3))])


def c6s4_pascal(r):
    n = r.randint(5, 12)
    k = r.randint(1, n - 1)
    return mcq(f'{n}C{k} + {n}C{k - 1} equals', f'{n + 1}C{k}', [f'{n + 1}C{k - 1}' if k - 1 != n + 1 - k else f'{n}C{k + 1}', f'{n}C{2 * k - 1}' if 2 * k - 1 <= n and 2 * k - 1 not in (k, n - k) else f'{n - 1}C{k}', f'{n + 2}C{k}'],
               f'Pascal\'s rule: nCr + nCr−1 = (n + 1)Cr, so {n}C{k} + {n}C{k - 1} = {n + 1}C{k}.', r)


c6s4_terms = term_mcq([('nCr', 'n!/(r! (n − r)!), the number of selections of r objects from n'), ('nCr = nCn−r', 'choosing r objects is the same as leaving out n − r'),
                       ('nC0', 'equal to 1 (select nothing)'), ('nPr = r! × nCr', 'link between arrangements and selections'),
                       ('nCr + nCr−1 = (n + 1)Cr', "Pascal's rule")],
                      'Which of the following is correct about {a}?', 'Which result is {b}?', '{a}: {b}.')

c6s4_tf = tf_mcq('combinations',
                 ['nCr = nCn−r.', 'nC0 = nCn = 1.', 'In a combination the order of the selected objects does not matter.', '10C3 = 120.', 'nPr = r! × nCr.'],
                 ['nCr = nPr × r!.', 'nC1 = 1.', 'In a combination the order of the selected objects matters.', '10C3 = 720.', 'nCr + nCr−1 = nCr+1.'])

c6s4_ar = pool_ar([
    ('12C9 = 220.', 'nCr = nCn−r, so 12C9 = 12C3.', 'a', 'R explains A: 12C3 = 220.'),
    ('The number of handshakes when 10 people each shake hands once with every other is 45.', 'A handshake is a selection of 2 people out of 10.', 'a', 'R explains A: 10C2 = 45.'),
    ('The number of ways to choose 3 prefects from 8 students is 336.', 'In a selection the order does not matter.', 'd', 'A is false (8C3 = 56; 336 = 8P3 is for arrangements); R is true.'),
    ('nCr is always less than nPr.', 'nPr = r! × nCr.', 'd', 'A is false: they are equal when r = 0 or 1; R is true.'),
])

c6s4_explain = pool_txt([
    ('Prove that nCr = nCn−r.', 'nCn−r = n!/((n − r)! r!) = nCr; selecting r items is the same as rejecting n − r items.', '2 marks.'),
    ('Distinguish between a permutation and a combination with an example.', 'Permutation: arrangement, order matters (president and secretary from 5: 20). Combination: selection, order does not matter (2 members from 5: 10).', '2 marks.'),
    ('Show that nPr = r! × nCr.', 'Each selection of r objects can be arranged in r! ways, and every arrangement arises from exactly one selection.', '2 marks.'),
])

# st5 mixed problems


def c6s5_words(r):
    V, C = r.randint(3, 5), r.randint(4, 7)
    p, q = r.randint(2, min(3, V)), r.randint(2, 3)
    sel = comb(V, p) * comb(C, q)
    v = sel * factorial(p + q)
    return Q(f'How many words, each of {p} vowels and {q} consonants, can be formed from {V} vowels and {C} consonants (all letters different, none repeated)?', f'{ind(v)}',
             f'Select vowels: {V}C{p} = {comb(V, p)}; consonants: {C}C{q} = {comb(C, q)} (2); arrange the {p + q} chosen letters: {p + q}! = {factorial(p + q)} (2); total = {sel} × {factorial(p + q)} = {ind(v)} (1).',
             [f'{ind(sel)}', f'{ind(perm(V, p) * perm(C, q))}', f'{ind(comb(V + C, p + q) * factorial(p + q))}'])


def c6s5_cards(r):
    k = r.choice([4, 5])
    kind = r.choice(['suit', 'each', 'face', 'ace'])
    if kind == 'suit':
        v = 4 * comb(13, k)
        q, key = f'all {k} cards are of the same suit', f'Choose the suit (4 ways) and then {k} of its 13 cards: 4 × 13C{k} = {ind(v)}.'
    elif kind == 'each' and k == 4:
        v = 13 ** 4
        q, key = 'there is one card of each suit', f'13 choices from each suit: 13⁴ = {ind(v)}.'
    elif kind == 'face':
        v = comb(12, k)
        q, key = f'all {k} are face cards', f'There are 12 face cards: 12C{k} = {ind(v)}.'
    else:
        v = comb(4, 1) * comb(48, k - 1)
        q, key = 'exactly one is an ace', f'4C1 × 48C{k - 1} = {ind(v)}.'
    return Q(f'In how many ways can {k} cards be selected from a pack of 52 cards so that {q}?', f'{ind(v)}', key, [f'{ind(comb(52, k))}', f'{ind(v * factorial(k))}', f'{ind(v // 4 if v % 4 == 0 else v + 4)}'])


def c6s5_team(r):
    n = r.randint(14, 18)
    k = 11
    a = r.randint(1, 2)
    kind = r.choice(['in', 'out', 'inout'])
    if kind == 'in':
        v = comb(n - a, k - a)
        q, key = f'{a} particular player{"s are" if a > 1 else " is"} always included', f'Include them and choose the remaining {k - a} from {n - a}: {n - a}C{k - a} = {ind(v)}.'
    elif kind == 'out':
        v = comb(n - a, k)
        q, key = f'{a} particular player{"s are" if a > 1 else " is"} always excluded', f'Choose all {k} from the other {n - a}: {n - a}C{k} = {ind(v)}.'
    else:
        v = comb(n - 2, k - 1)
        q, key = 'one particular player is always included and another is always excluded', f'Include one, exclude one: choose {k - 1} from {n - 2}: {n - 2}C{k - 1} = {ind(v)}.'
    city = r.choice(CITIES)
    return Q(f'A school in {city} has {n} cricketers. In how many ways can a team of 11 be chosen if {q}? Also find the number of ways with no restriction.', f'{ind(v)}; without restriction {ind(comb(n, k))}',
             key + f' Without restriction: {n}C11 = {ind(comb(n, k))}.', [f'{ind(comb(n - a, k - a + 1) if kind == "in" else comb(n, k - 1))}; without restriction {ind(comb(n, k))}', f'{ind(comb(n - a, k - 1))}; without restriction {ind(comb(n, k))}', f'{ind(v * 11)}; without restriction {ind(comb(n, k))}'])


def c6s5_order(r):
    n = r.randint(6, 15)
    kind = r.choice(['ps', 'pair', 'medal', 'team'])
    if kind == 'ps':
        return mcq(f'In how many ways can a president and a secretary be chosen from {n} members?', str(perm(n, 2)), [str(comb(n, 2)), str(n * 2), str(n ** 2)],
                   f'The posts are different, so order matters: {n}P2 = {perm(n, 2)}.', r)
    if kind == 'pair':
        return mcq(f'In how many ways can 2 members be chosen from {n} members to attend a meeting?', str(comb(n, 2)), [str(perm(n, 2)), str(n * 2), str(n ** 2)],
                   f'Both get the same role, so order does not matter: {n}C2 = {comb(n, 2)}.', r)
    if kind == 'medal':
        return mcq(f'In a race with {n} runners, in how many ways can gold, silver and bronze medals be awarded?', str(perm(n, 3)), [str(comb(n, 3)), str(n ** 3), str(3 * n)],
                   f'Medals are different: {n}P3 = {perm(n, 3)}.', r)
    return mcq(f'In how many ways can a relay group of 3 be chosen (no running order yet) from {n} athletes?', str(comb(n, 3)), [str(perm(n, 3)), str(n ** 3), str(3 * n)],
               f'Only a selection: {n}C3 = {comb(n, 3)}.', r)


def c6s5_case(r):
    city = r.choice(CITIES)
    b, g = r.randint(6, 9), r.randint(4, 7)
    k = 5
    tot = comb(b + g, k)
    ex2 = comb(g, 2) * comb(b, 3)
    atl = tot - comb(b, k)
    capt = comb(b + g, k) * k
    return {'stem': f'A school in {city} has to send a quiz team of {k} students chosen from {b} boys and {g} girls.\n(i) In how many ways can the team be chosen? (ii) In how many ways if it has exactly 2 girls? '
                    f'(iii) In how many ways if it has at least one girl? (iv) After the team is chosen, a captain is to be named from it. How many ways are there to choose a team with a captain?',
            'answer': f'(i) {ind(tot)} (ii) {ind(ex2)} (iii) {ind(atl)} (iv) {ind(capt)}',
            'key': f'(i) {b + g}C5 (1). (ii) {g}C2 × {b}C3 (1). (iii) total − (all boys) = {ind(tot)} − {ind(comb(b, k))} (1). (iv) {b + g}C5 × 5C1 (1).'}


c6s5_tf = tf_mcq('selection and arrangement problems',
                 ['Choosing a team is a combination; arranging the team in a line is a permutation.', '"At least one" is often easier as total minus "none".',
                  'Selecting r objects and then arranging them gives nCr × r! = nPr.', 'If two objects must be included, select the rest from the remaining n − 2.'],
                 ['Choosing a captain and vice-captain is a combination problem.', '"At least one" equals "exactly one".',
                  'If an object must be excluded, choose from n + 1 objects.', 'Selecting a committee is a permutation because members have names.'])

c6s5_ar = pool_ar([
    ('The number of ways to choose a captain and a vice-captain from 11 players is 110.', 'The two posts are different, so order matters.', 'a', 'R explains A: 11P2 = 110.'),
    ('The number of 5-card hands with at least one ace is 52C5 − 48C5.', 'Hands with no ace are chosen from the 48 non-aces.', 'a', 'R explains A (complement).'),
    ('The number of ways of selecting 3 books from 7 and arranging them on a shelf is 35.', 'Selection of 3 from 7 is 7C3 = 35.', 'd', 'A is false: arranging gives 35 × 3! = 210; R is true.'),
])

c6s5_explain = pool_txt([
    ('Explain with an example why "at least" problems are often solved using the complement.', 'At least one girl = total − no girls; it avoids adding many cases.', '2 marks.'),
    ('How do you decide whether to use nPr or nCr in a word problem?', 'If the chosen objects get different positions or roles (order matters), use nPr; for pure selection use nCr.', '2 marks.'),
])

c6s5_kind = pool_mcq([
    ('Forming 4-digit PIN codes with distinct digits is a problem of', 'permutation', ['combination', 'neither', 'addition principle only'], 'Order of digits matters.'),
    ('Choosing 3 fruits from a basket of 10 different fruits is a problem of', 'combination', ['permutation', 'neither', 'circular arrangement'], 'Order does not matter in a selection.'),
    ('Seating 5 guests in 5 chairs in a row is a problem of', 'permutation', ['combination', 'neither', 'selection only'], 'Different seats, so order matters.'),
    ('Choosing 11 players from a squad of 15 is a problem of', 'combination', ['permutation', 'neither', 'arrangement'], 'Only a selection.'),
])


# ======================================================== ch07 Binomial Theorem
# st1 Pascal's triangle

def c7s1_row(r):
    n = r.randint(4, 9)
    row = [comb(n, k) for k in range(n + 1)]
    return Q(f'Write row n = {n} of Pascal\'s triangle (the coefficients of (a + b){sup(n)}).', ', '.join(map(str, row)),
             f'Each entry is the sum of the two entries above it; the row is {n}C0, {n}C1, …, {n}C{n}.',
             [', '.join(str(comb(n - 1, k)) for k in range(n)), ', '.join(str(comb(n + 1, k)) for k in range(n + 2)), ', '.join(map(str, row[:-1]))])


def c7s1_coef(r):
    n = r.randint(5, 10)
    k = r.randint(2, n - 2)
    v = comb(n, k)
    return mcq(f'The coefficient of a{sup(n - k)}b{sup(k)} in the expansion of (a + b){sup(n)} is', str(v),
               [str(perm(n, k)), str(comb(n, k - 1)) if comb(n, k - 1) != v else str(comb(n, k + 1) + 1), str(comb(n - 1, k)) if comb(n - 1, k) != v else str(v + n)],
               f'It is {n}C{k} = {v}.', r)


def c7s1_sum(r):
    n = r.randint(4, 12)
    kind = r.choice(['all', 'find', 'odd'])
    if kind == 'all':
        return Q(f'Find the sum of the binomial coefficients in the expansion of (1 + x){sup(n)}.', str(2 ** n), f'Put x = 1: {n}C0 + {n}C1 + … + {n}C{n} = 2{sup(n)} = {2 ** n}.',
                 [str(2 ** (n - 1)), str(n + 1), str(2 * n)])
    if kind == 'find':
        return Q(f'The sum of the binomial coefficients in (a + b)ⁿ is {2 ** n}. Find n.', f'n = {n}', f'2ⁿ = {2 ** n} ⇒ n = {n}.', [f'n = {n - 1}', f'n = {n + 1}', f'n = {2 ** n // 2}'])
    return Q(f'Find {n}C0 + {n}C2 + {n}C4 + … (the sum of the even-indexed coefficients in (1 + x){sup(n)}).', str(2 ** (n - 1)),
             f'Adding the expansions at x = 1 and x = −1 gives 2(sum of even-indexed) = 2{sup(n)}, so the sum is 2{sup(n - 1)} = {2 ** (n - 1)}.', [str(2 ** n), str(2 ** (n - 2)), str(n)])


def c7s1_terms_count(r):
    n = r.randint(5, 15)
    kind = r.choice(['plus', 'sum', 'diff'])
    if kind == 'plus':
        v = n + 1
        return Q(f'How many terms are there in the expansion of (2x + 3y){sup(n)}?', str(v), f'(a + b)ⁿ has n + 1 terms: {v}.', [str(n), str(n + 2), str(2 * n)])
    v = n // 2 + 1 if n % 2 == 0 else (n + 1) // 2
    if kind == 'diff':
        v = n // 2 if n % 2 == 0 else (n + 1) // 2
        return Q(f'How many terms are there in (x + a){sup(n)} − (x − a){sup(n)} after simplification?', str(v),
                 f'Terms with even powers of a cancel; those with odd powers of a (r = 1, 3, 5, …) double: {v} terms.', [str(n + 1), str(n // 2 + 1) if n // 2 + 1 != v else str(v + 1), str(2 * n)])
    return Q(f'How many terms are there in (x + a){sup(n)} + (x − a){sup(n)} after simplification?', str(v),
             f'Terms with odd powers of a cancel; those with even powers (r = 0, 2, 4, …) double: {v} terms.', [str(n + 1), str(2 * (n + 1)), str(v + 1)])


c7s1_tf = tf_mcq("Pascal's triangle",
                 ["Each number in Pascal's triangle is the sum of the two numbers just above it.", "Row n of Pascal's triangle gives nC0, nC1, …, nCn.",
                  "Pascal's triangle is symmetric about its middle.", 'The entries of row 4 are 1, 4, 6, 4, 1.'],
                 ["Each number in Pascal's triangle is the product of the two numbers above it.", 'The entries of row 4 are 1, 3, 3, 1.',
                  'The sum of the entries in row n is n².', 'Row n has n entries.'])

c7s1_terms = term_mcq([('binomial coefficient nCr', 'the coefficient of aⁿ⁻ʳbʳ in (a + b)ⁿ'), ("Pascal's rule", 'nCr + nCr−1 = (n + 1)Cr'),
                       ('sum of entries in row n', '2ⁿ'), ('number of terms in (a + b)ⁿ', 'n + 1'), ('symmetry of the triangle', 'nCr = nCn−r')],
                      'Which of the following matches "{a}"?', 'Which idea gives {b}?', '{a}: {b}.')

c7s1_ar = pool_ar([
    ("The 5th row of Pascal's triangle is 1, 5, 10, 10, 5, 1.", 'Each entry is the sum of the two entries above it in the previous row 1, 4, 6, 4, 1.', 'a', 'R explains A.'),
    ('The sum of the coefficients in (1 + x)⁸ is 256.', 'Putting x = 1 gives (1 + 1)⁸.', 'a', 'R explains A.'),
    ('(a + b)⁷ has 7 terms.', 'The powers of b run from 0 to 7.', 'd', 'A is false (8 terms); R is true.'),
])

c7s1_explain = pool_txt([
    ("Explain how Pascal's triangle is built and how it gives the coefficients of (a + b)ⁿ.", 'Start with 1; each entry is the sum of the two above; row n lists nC0 … nCn, the coefficients of (a + b)ⁿ.', '2 marks.'),
    ("Why is Pascal's triangle symmetric?", 'Because nCr = nCn−r: choosing r is the same as leaving out n − r.', '2 marks.'),
])

# st2 binomial theorem


def _bin_expand(a, b, n, v='x'):
    cs = [comb(n, k) * a ** (n - k) * b ** k for k in range(n + 1)]
    return poly(cs, v), cs


def c7s2_expand(r):
    a, b = r.choice([1, 2, 3]), r.choice([1, 2, -1, -2, 3, -3])
    n = r.randint(3, 5)
    if a == 1 and abs(b) == 1 and n == 3:
        n = 4
    s, cs = _bin_expand(a, b, n)
    wrong, _ = _bin_expand(a, -b, n)
    wrong2 = poly([a ** n] + [0] * (n - 1) + [b ** n])
    return Q(M(f'Expand ({lin(a, b)}){sup(n)} using the binomial theorem.'), s,
             f'Tᵣ₊₁ = {n}Cr ({fs(a) if a != 1 else ""}x){sup(n)}⁻ʳ ({fs(b)})ʳ for r = 0 to {n} (2); simplify each term (2).'.replace('⁻ʳ', '⁻ʳ'),
             [wrong, wrong2, poly([comb(n, k) for k in range(n + 1)])])


def c7s2_term(r):
    n = r.randint(5, 9)
    a, b = r.choice([1, 2, 3]), r.choice([-1, -2, 2, 3, -3])
    k = r.randint(2, n - 1)  # term number k+1
    c = comb(n, k) * a ** (n - k) * b ** k
    px, py = n - k, k
    mono = lambda c_, p, q: (fs(c_) if abs(c_) != 1 else ('−' if c_ < 0 else '')) + (f'x{sup(p) if p > 1 else ""}' if p else '') + (f'y{sup(q) if q > 1 else ""}' if q else '')
    ans = mono(c, px, py)
    return Q(M(f'Find the {ordn(k + 1)} term in the expansion of ({fs(a) if a != 1 else ""}x {"+" if b > 0 else "−"} {abs(b) if abs(b) != 1 else ""}y){sup(n)}.'), ans,
             f'Tᵣ₊₁ = {n}Cr ({fs(a) if a != 1 else ""}x)ⁿ⁻ʳ ({fs(b) if abs(b) != 1 else ('−' if b < 0 else '')}y)ʳ with r = {k} (1): {n}C{k} × {a ** (n - k)} × ({b ** k}) = {fs(c)} (1).'.replace('ⁿ⁻ʳ', sup(n) + '⁻ʳ'),
             [mono(-c, px, py), mono(comb(n, k), px, py), mono(comb(n, k + 1) * a ** (n - k - 1) * b ** (k + 1), px - 1, py + 1)])


def _gen_term(r):
    """(a x^p + b / x^q)^n ; returns (a, p, b, q, n)."""
    a = r.choice([1, 2, 3])
    b = r.choice([1, -1, 2, -2, 3, -3])
    p = r.choice([1, 2])
    q = r.choice([1, 1, 2])
    n = r.randint(4, 10)
    return a, p, b, q, n


def _gt_txt(a, p, b, q, n):
    left = (fs(a) if a != 1 else '') + 'x' + (sup(p) if p > 1 else '')
    right = f'{abs(b)}/x' + (sup(q) if q > 1 else '')
    return f'({left} {"+" if b > 0 else "−"} {right}){sup(n)}'


def c7s2_coef(r):
    a, p, b, q, n = _gen_term(r)
    # power of x in T_{r+1}: p(n - r) - q r
    pows = {p * (n - k) - q * k: k for k in range(n + 1)}
    cand = [e for e in pows if e != 0]
    e = r.choice(cand)
    k = pows[e]
    c = comb(n, k) * a ** (n - k) * b ** k
    return Q(f'Find the coefficient of x{sup(e) if e != 1 else ""} in the expansion of {_gt_txt(a, p, b, q, n)}.'.replace('x⁻', 'x⁻'), fs(c),
             f'Tᵣ₊₁ = {n}Cr ({a})ⁿ⁻ʳ ({fs(b)})ʳ x^({p}({n} − r) − {q if q > 1 else ''}r) (1); set the power = {fs(e)} ⇒ r = {k} (1); coefficient = {n}C{k} × {a ** (n - k)} × ({fs(b ** k)}) = {fs(c)} (1).'.replace('ⁿ⁻ʳ', sup(n) + '⁻ʳ'),
             [fs(-c), fs(comb(n, k)), fs(comb(n, k) * a ** (n - k) * abs(b) ** k + (1 if b > 0 else 0)) if b < 0 else fs(comb(n, k) * a ** k * b ** (n - k))])


def c7s2_indep(r):
    for _ in range(40):
        a, p, b, q, n = _gen_term(r)
        if (p * n) % (p + q) == 0:
            k = p * n // (p + q)
            break
    else:
        raise ValueError
    c = comb(n, k) * a ** (n - k) * b ** k
    return Q(f'Find the term independent of x in the expansion of {_gt_txt(a, p, b, q, n)}.', fs(c),
             f'General term Tᵣ₊₁ = {n}Cr ({a})ⁿ⁻ʳ ({fs(b)})ʳ x^({p * n} − {p + q}r) (2); for the term independent of x, {p * n} − {p + q}r = 0 ⇒ r = {k} (1); T{k + 1} = {n}C{k} × {a ** (n - k)} × ({fs(b ** k)}) = {fs(c)} (1).'.replace('ⁿ⁻ʳ', sup(n) + '⁻ʳ').replace(f'T{k + 1}', 'T' + ''.join('₀₁₂₃₄₅₆₇₈₉'[int(d)] for d in str(k + 1))),
             [fs(-c), fs(comb(n, k)), fs(comb(n, k + 1) * a ** (n - k - 1) * b ** (k + 1) if k < n else c + 1)])


def c7s2_middle(r):
    a = r.choice([1, 2, 3])
    b = r.choice([1, 2, 3, -1, -2])
    n = r.choice([4, 6, 8, 10])
    k = n // 2
    c = comb(n, k) * a ** (n - k) * b ** k
    left = (fs(a) if a != 1 else '') + 'x'
    ans = f'{fs(c)}x{sup(n - k) if n - k > 1 else ""}y{sup(k) if k > 1 else ""}'
    return Q(f'Find the middle term in the expansion of ({left} {"+" if b > 0 else "−"} {abs(b) if abs(b) != 1 else ""}y){sup(n)}.', ans,
             f'n = {n} is even, so there are {n + 1} terms and the middle one is T{"" if True else ""}({n}/2 + 1) = the {ordn(k + 1)} term (1); T = {n}C{k} ({left}){sup(k)} ({fs(b) if abs(b) != 1 else ('−' if b < 0 else '')}y){sup(k)} (2) = {ans} (1).',
             [f'{fs(comb(n, k))}x{sup(k)}y{sup(k)}', f'{fs(-c)}x{sup(k)}y{sup(k)}', f'{fs(comb(n, k - 1) * a ** (n - k + 1) * b ** (k - 1))}x{sup(k + 1)}y{sup(k - 1) if k > 2 else ""}'])


c7s2_tf = tf_mcq('the binomial theorem',
                 ['(a + b)ⁿ = Σ nCr aⁿ⁻ʳ bʳ, r = 0 to n.', 'The general term of (a + b)ⁿ is Tᵣ₊₁ = nCr aⁿ⁻ʳ bʳ.', 'If n is even, (a + b)ⁿ has one middle term.',
                  'In (a − b)ⁿ the terms alternate in sign.', 'The coefficients of terms equidistant from the ends are equal.'],
                 ['The general term of (a + b)ⁿ is Tᵣ = nCr aⁿ⁻ʳ bʳ.', 'If n is odd, (a + b)ⁿ has exactly one middle term.', 'In (a − b)ⁿ all terms are negative.',
                  '(a + b)ⁿ = aⁿ + bⁿ.', 'The sum of the indices of a and b in each term is n + 1.'])

c7s2_ar = pool_ar([
    ('(x + y)¹⁰ has two middle terms.', 'If n is odd, (a + b)ⁿ has two middle terms.', 'd', 'A is false: n = 10 is even, so there is one middle term; R is true.'),
    ('The 4th term of (a + b)⁶ is 20a³b³.', 'Tᵣ₊₁ = nCr aⁿ⁻ʳ bʳ and 6C3 = 20.', 'a', 'R explains A (r = 3).'),
    ('In each term of (a + b)ⁿ the powers of a and b add up to n.', 'Each term comes from choosing a or b from each of the n factors.', 'a', 'R explains A.'),
    ('The coefficient of x² in (1 + x)⁵ is 5.', 'The coefficient of xʳ in (1 + x)ⁿ is nCr.', 'd', 'A is false (5C2 = 10); R is true.'),
])

c7s2_explain = pool_txt([
    ('Write the general term of (a + b)ⁿ and explain how to find the term independent of x in (x + 1/x)⁶.', 'Tᵣ₊₁ = 6Cr x⁶⁻ʳ x⁻ʳ = 6Cr x⁶⁻²ʳ; set 6 − 2r = 0 ⇒ r = 3; term = 20.', '2 marks.'),
    ('Explain why (a − b)ⁿ has terms of alternating signs.', 'Tᵣ₊₁ = nCr aⁿ⁻ʳ (−b)ʳ = (−1)ʳ nCr aⁿ⁻ʳ bʳ; the sign changes with r.', '2 marks.'),
])

c7s2_long = pool_txt([
    ('State and prove the binomial theorem for a positive integer n using the principle of combinations (counting how terms arise in the product (a + b)(a + b)…(a + b)).',
     '(a + b)ⁿ = Σ nCr aⁿ⁻ʳ bʳ', 'Each term picks b from r factors and a from n − r factors (2); the number of ways is nCr (2); sum over r = 0 to n (1).'),
    ('Prove the binomial theorem by mathematical induction: assume it for n = k and show it for n = k + 1 using kCr + kCr−1 = (k + 1)Cr.',
     'Proved for all n ∈ N', 'Base case n = 1 (1); multiply the k-expansion by (a + b) (2); combine using Pascal\'s rule (2).'),
])

c7s2_nterms = pool_mcq([
    ('The number of terms in the expansion of (2x − 3y)⁹ is', '10', ['9', '11', '18'], '(a + b)ⁿ has n + 1 terms.'),
    ('The number of terms in the expansion of (1 + x)¹² is', '13', ['12', '11', '24'], 'n + 1 = 13.'),
    ('In (a + b)ⁿ, the sum of the indices of a and b in every term is', 'n', ['n + 1', 'n − 1', '2n'], 'aⁿ⁻ʳ bʳ: (n − r) + r = n.'),
    ('The general term of (a + b)ⁿ is', 'nCr aⁿ⁻ʳ bʳ', ['nCr aʳ bⁿ⁻ʳ⁺¹', 'nPr aⁿ⁻ʳ bʳ', 'nCr aⁿ bʳ'], 'Tᵣ₊₁ = nCr aⁿ⁻ʳ bʳ.'),
])

# st3 applications


def c7s3_eval(r):
    base = r.choice([100, 1000, 10])
    d = r.choice([1, 2, 3, -1, -2, -3])
    n = r.randint(3, 5) if base != 10 else r.randint(4, 6)
    if base == 10 and abs(d) > 2:
        d = 1 if d > 0 else -1
    x = base + d
    v = x ** n
    return Q(f'Using the binomial theorem, evaluate ({x}){sup(n)}.', f'{ind(v)}',
             f'({x}){sup(n)} = ({base} {"+" if d > 0 else "−"} {abs(d)}){sup(n)} (1); expand with the binomial theorem and add the terms (2) = {ind(v)} (1).',
             [f'{ind(base ** n + n * d * base ** (n - 1))}', f'{ind(v + 10)}', f'{ind((base - d) ** n)}'])


def c7s3_approx(r):
    x = r.choice([Fr(101, 100), Fr(99, 100), Fr(102, 100), Fr(98, 100), Fr(1001, 1000), Fr(999, 1000)])
    n = r.randint(4, 6)
    d = x - 1
    approx = 1 + n * d + comb(n, 2) * d * d
    dec = 4 if x.denominator == 100 else 6
    return Q(f'Find ({float(x):g}){sup(n)} correct to {dec} decimal places using the first three terms of the binomial expansion.', f'{float(approx):.{dec}f}',
             f'({float(x):g}){sup(n)} = (1 {"+" if d > 0 else "−"} {float(abs(d)):g}){sup(n)} ≈ 1 + {n}({float(d):g}) + {comb(n, 2)}({float(d):g})² (2) = {float(approx):.{dec}f} (1).'.replace('(-', '(−').replace('+ -', '− '),
             [f'{float(1 + n * d):.{dec}f}', f'{float(1 + n * d - comb(n, 2) * d * d):.{dec}f}', f'{float(1 + n * abs(d)):.{dec}f}' if d < 0 else f'{float(1 + d):.{dec}f}'])


def c7s3_rem(r):
    m = r.choice([5, 6, 7, 8, 9, 11, 12, 13])
    q = r.randint(1, 3)
    s = r.choice([1, -1])
    a = m * q + s
    n = r.randint(20, 99)
    v = pow(a, n, m)
    return Q(f'Using the binomial theorem, find the remainder when {a}{sup(n)} is divided by {m}.', str(v),
             f'{a} = {m * q} {"+" if s > 0 else "−"} 1 (1); every term of ({m * q} {"+" if s > 0 else "−"} 1){sup(n)} except the last is a multiple of {m}; the last is {"1" if s > 0 else f"(−1){sup(n)}"} (1) ⇒ remainder {v} (1).',
             [str((m - v) % m if (m - v) % m != v else 0), str(1 if v != 1 else m - 2), str(a % m if a % m != v else 2)])


def c7s3_divis(r):
    k = r.choice([4, 5, 6, 7, 8, 9])
    return Q(f'Using the binomial theorem, prove that {k + 1}ⁿ − {k}n − 1 is divisible by {k * k} for every natural number n.',
             f'{k + 1}ⁿ − {k}n − 1 = {k * k}[nC2 + nC3 × {k} + … + {k}ⁿ⁻²], a multiple of {k * k}',
             f'{k + 1}ⁿ = (1 + {k})ⁿ = 1 + n × {k} + nC2 × {k}² + nC3 × {k}³ + … (2); so {k + 1}ⁿ − {k}n − 1 = {k}²(nC2 + nC3 × {k} + …) (2); the bracket is an integer (1).')


def c7s3_compare(r):
    return pool_mcq([
        ('Which is larger, (1.01)¹⁰⁰⁰⁰⁰⁰ or 10,000?', '(1.01)¹⁰⁰⁰⁰⁰⁰', ['10,000', 'They are equal', 'Cannot be decided'], '(1 + 0.01)¹⁰⁰⁰⁰⁰⁰ > 1 + 1000000 × 0.01 = 10001 > 10000.'),
        ('Which is larger, (1.1)¹⁰⁰⁰⁰ or 1000?', '(1.1)¹⁰⁰⁰⁰', ['1000', 'They are equal', 'Cannot be decided'], '(1 + 0.1)¹⁰⁰⁰⁰ > 1 + 10000 × 0.1 = 1001 > 1000.'),
        ('Which is larger, (1.001)¹⁰⁰⁰⁰⁰ or 100?', '(1.001)¹⁰⁰⁰⁰⁰', ['100', 'They are equal', 'Cannot be decided'], '(1 + 0.001)¹⁰⁰⁰⁰⁰ > 1 + 100000 × 0.001 = 101 > 100.'),
        ('Which is larger, (1.02)⁵⁰⁰ or 10?', '(1.02)⁵⁰⁰', ['10', 'They are equal', 'Cannot be decided'], '(1 + 0.02)⁵⁰⁰ > 1 + 500 × 0.02 = 11 > 10.'),
    ])(r)


def c7s3_case(r):
    who = name(r)
    P = r.choice([10000, 20000, 25000, 50000])
    rate = r.choice([1, 2])
    n = r.choice([4, 5, 6])
    d = Fr(rate, 100)
    exact = P * (1 + d) ** n
    a3 = P * (1 + n * d + comb(n, 2) * d * d)
    a2 = P * (1 + n * d)
    return {'stem': f'{who} deposits ₹{ind(P)} in a bank that pays {rate}% interest per month, compounded monthly, for {n} months.\n'
                    f'(i) Write the amount as P(1 + r)ⁿ with the values filled in. (ii) Using the first two terms of the binomial expansion, estimate the amount. '
                    f'(iii) Using the first three terms, estimate the amount. (iv) Find the exact amount to the nearest rupee and say which estimate is closer.',
            'answer': f'(i) {ind(P)} × (1.{rate:02d}){sup(n)} (ii) {inr(round(float(a2)))} (iii) {rs2(float(a3))} (iv) ₹{ind(round(float(exact)))}; the three-term estimate',
            'key': f'(i) Amount = P(1 + r)ⁿ (1). (ii) P(1 + nr) (1). (iii) P(1 + nr + nC2 r²) (1). (iv) Exact value; adding more terms brings the estimate closer (1).'}


c7s3_tf = tf_mcq('applications of the binomial theorem',
                 ['(1 + x)ⁿ ≥ 1 + nx for x > 0 and n ∈ N.', '(99)³ can be evaluated as (100 − 1)³.', 'For small x, (1 + x)ⁿ ≈ 1 + nx.', 'Every term of (5 + 1)ⁿ except the last is a multiple of 5.'],
                 ['(1 + x)ⁿ ≤ 1 + nx for x > 0.', 'For small x, (1 + x)ⁿ ≈ 1 + x.', '(102)⁴ = 102 × 4.', '6ⁿ leaves remainder 0 when divided by 5.'])

c7s3_ar = pool_ar([
    ('9ⁿ − 8n − 1 is divisible by 64 for every natural number n.', '9ⁿ = (1 + 8)ⁿ = 1 + 8n + 64 × (an integer).', 'a', 'R explains A.'),
    ('(1.01)¹⁰⁰ > 2.', '(1 + 0.01)¹⁰⁰ > 1 + 100 × 0.01.', 'a', 'R explains A: the right side equals 2 and the other terms are positive.'),
    ('(101)⁵⁰ < (100)⁵⁰ + (99)⁵⁰.', 'The binomial theorem applies only to positive integral indices.', 'd', 'A is false: (101)⁵⁰ is larger; R is true for this chapter.'),
])

c7s3_explain = pool_txt([
    ('Explain how the binomial theorem helps to evaluate (98)⁵ without long multiplication.', 'Write 98 = 100 − 2 and expand (100 − 2)⁵; each term is easy to compute.', '2 marks.'),
    ('Show that 6ⁿ − 5n always leaves remainder 1 when divided by 25.', '6ⁿ = (1 + 5)ⁿ = 1 + 5n + 25(nC2 + …); so 6ⁿ − 5n = 1 + 25k.', '2 marks.'),
])


# ======================================================== ch08 Sequences and Series
# st1 general term and sigma notation

SEQS = [
    ('n(n + 2)', lambda n: Fr(n * (n + 2))), ('2n + 5', lambda n: Fr(2 * n + 5)), ('n/(n + 1)', lambda n: Fr(n, n + 1)), ('(2n − 3)/6', lambda n: Fr(2 * n - 3, 6)),
    ('(−1)ⁿ⁻¹ 5ⁿ⁺¹', lambda n: Fr((-1) ** (n - 1) * 5 ** (n + 1))), ('n² − 3n', lambda n: Fr(n * n - 3 * n)), ('(n² + 5)/4', lambda n: Fr(n * n + 5, 4)),
    ('3ⁿ − 2', lambda n: Fr(3 ** n - 2)), ('(−1)ⁿ n²', lambda n: Fr((-1) ** n * n * n)), ('4n − 3', lambda n: Fr(4 * n - 3)), ('n(n − 1)(n − 2)', lambda n: Fr(n * (n - 1) * (n - 2))),
]


def c8s1_first(r):
    s, f = r.choice(SEQS)
    xs = [f(n) for n in range(1, 5)]
    return Q(f'Write the first four terms of the sequence aₙ = {s}.', ', '.join(fs(x) for x in xs), f'Put n = 1, 2, 3, 4: ' + ', '.join(fs(x) for x in xs) + '.',
             [', '.join(fs(f(n)) for n in range(0, 4)), ', '.join(fs(f(n)) for n in range(2, 6)), ', '.join(fs(x * 2) for x in xs)])


def c8s1_nth(r):
    s, f = r.choice(SEQS)
    k = r.randint(5, 20)
    if '5ⁿ' in s or '3ⁿ' in s:
        k = r.randint(4, 7)
    v = f(k)
    return Q(f'Find the {ordn(k)} term of the sequence aₙ = {s}.', fs(v), f'a{"".join("₀₁₂₃₄₅₆₇₈₉"[int(d)] for d in str(k))} = {fs(v)} (substitute n = {k}).',
             [fs(f(k - 1)), fs(f(k + 1)), fs(v + 1)])


def c8s1_recur(r):
    a1 = r.randint(1, 5)
    kind = r.choice(['add', 'mul', 'fib'])
    if kind == 'add':
        d = r.randint(2, 6)
        xs = [a1]
        for _ in range(4):
            xs.append(xs[-1] + d)
        rule = f'a₁ = {a1}, aₙ = aₙ₋₁ + {d} (n ≥ 2)'
    elif kind == 'mul':
        m = r.randint(2, 4)
        xs = [a1]
        for _ in range(4):
            xs.append(xs[-1] * m + 1)
        rule = f'a₁ = {a1}, aₙ = {m}aₙ₋₁ + 1 (n ≥ 2)'
    else:
        a2 = r.randint(1, 5)
        xs = [a1, a2]
        for _ in range(3):
            xs.append(xs[-1] + xs[-2])
        rule = f'a₁ = {a1}, a₂ = {a2}, aₙ = aₙ₋₁ + aₙ₋₂ (n ≥ 3)'
    return Q(f'Write the first five terms of the sequence defined by {rule}.', ', '.join(map(str, xs)), 'Apply the rule term by term: ' + ', '.join(map(str, xs)) + '.',
             [', '.join(map(str, xs[:4] + [xs[4] + 1])), ', '.join(map(str, [a1] + xs[2:] + [xs[-1] * 2])), ', '.join(map(str, [x + 1 for x in xs]))])


def c8s1_sigma(r):
    a, b = r.randint(1, 5), r.randint(-3, 6)
    n = r.randint(5, 15)
    kind = r.choice(['lin', 'sq'])
    if kind == 'lin':
        v = a * n * (n + 1) // 2 + b * n
        t = lin(a, b, 'k')
        return mcq(M(f'The value of Σ ({t}), k = 1 to {n}, is'), str(v), [str(v - b * n + b), str(a * n * n + b * n), str(a * n + b)],
                   f'{a} × {n}({n} + 1)/2 {"+" if b >= 0 else "−"} {abs(b)} × {n} = {v}.', r)
    v = n * (n + 1) * (2 * n + 1) // 6
    return mcq(f'The value of Σ k², k = 1 to {n}, is', str(v), [str((n * (n + 1) // 2) ** 2), str(n * n), str(n * (n + 1) // 2)],
               f'Σk² = n(n + 1)(2n + 1)/6 = {v}.', r)


def c8s1_which(r):
    a, b = r.randint(1, 3), r.randint(-6, 8)
    k = r.randint(5, 25)
    v = a * k * k + b * k
    s = poly([a, b, 0], 'n')
    sols = [m for m in range(1, 200) if a * m * m + b * m == v]
    if sols != [k]:
        raise ValueError
    return Q(M(f'Which term of the sequence aₙ = {s} is {v}?'), f'the {ordn(k)} term', M(f'{s} = {v} ⇒ {poly([a, b, -v], "n")} = 0 (1); the positive integer root is n = {k} (1).'),
             [f'the {ordn(k + 1)} term', f'the {ordn(k - 1)} term', f'the {ordn(v // max(1, a * k) if v // max(1, a * k) not in (k, k + 1, k - 1) else k + 2)} term'])


c8s1_tf = tf_mcq('sequences and series',
                 ['A sequence is a function whose domain is the set of natural numbers (or a subset {1, 2, …, n}).', 'A series is the sum of the terms of a sequence.',
                  'The Fibonacci sequence is defined by a recurrence relation.', 'Σ (from k = 1 to n) of 1 is n.'],
                 ['Every sequence has a formula for its nth term.', 'A series is a list of numbers separated by commas.', 'A finite sequence has infinitely many terms.',
                  'Σ (from k = 1 to n) of k is n².'])

c8s1_terms = term_mcq([('finite sequence', 'a sequence with a definite number of terms'), ('infinite sequence', 'a sequence that never ends'),
                       ('series', 'the sum a₁ + a₂ + a₃ + … of the terms of a sequence'), ('recurrence relation', 'a rule giving each term from earlier terms'),
                       ('general term', 'the nth term aₙ written as a formula in n')],
                      'Which of the following describes a {a}?', 'Which term means {b}?', '{a}: {b}.')

c8s1_ar = pool_ar([
    ('The sequence aₙ = (−1)ⁿ has terms −1, 1, −1, 1, …', 'Odd powers of −1 equal −1 and even powers equal 1.', 'a', 'R explains A.'),
    ('The sequence of prime numbers has a simple formula for its nth term.', 'There are infinitely many primes.', 'd', 'A is false (no simple formula is known); R is true.'),
    ('Σ (from k = 1 to 10) of 2k = 110.', '2 + 4 + … + 20 = 2 × (10 × 11/2).', 'a', 'R explains A.'),
])

c8s1_explain = pool_txt([
    ('Distinguish between a sequence and a series with an example.', 'Sequence: an ordered list 1, 3, 5, …; series: the sum 1 + 3 + 5 + …', '2 marks.'),
    ('Why is a sequence called a function? State its domain.', 'Each natural number n is mapped to a term aₙ; the domain is N (or {1, 2, …, n}).', '2 marks.'),
])

# st2 AP and AM


def c8s2_am(r):
    a, b = r.randint(-10, 30), r.randint(-10, 50)
    if a == b:
        raise ValueError
    return Q(f'Find the arithmetic mean of {fs(a)} and {fs(b)}.', fs(Fr(a + b, 2)), f'A = (a + b)/2 = ({fs(a)} + {fs(b)})/2 = {fs(Fr(a + b, 2))}.'.replace('+ −', '− '),
             [fs(a + b), fs(Fr(abs(b - a), 2)), fs(Fr(a + b, 2) + 1)])


def c8s2_insert(r):
    a = r.randint(-5, 10)
    k = r.randint(3, 6)
    d = r.randint(2, 7) * r.choice([1, 1, -1])
    b = a + (k + 1) * d
    ms = [a + i * d for i in range(1, k + 1)]
    return Q(f'Insert {k} arithmetic means between {fs(a)} and {fs(b)}.', ', '.join(fs(x) for x in ms),
             f'{k + 2} terms in AP: {fs(b)} = {fs(a)} + {k + 1}d ⇒ d = {fs(d)} (1); means: ' + ', '.join(fs(x) for x in ms) + ' (1).',
             [', '.join(fs(a + i * Fr(b - a, k)) for i in range(1, k + 1)), ', '.join(fs(x + d) for x in ms), ', '.join(fs(a + i * (d + 1)) for i in range(1, k + 1))])


def c8s2_sum(r):
    a = r.randint(-5, 20)
    d = r.choice([2, 3, 4, 5, -2, -3, Fr(1, 2), Fr(3, 2)])
    n = r.randint(10, 30)
    s = Fr(n, 2) * (2 * a + (n - 1) * d)
    terms = ', '.join(fs(a + i * d) for i in range(3))
    return Q(f'Find the sum of the first {n} terms of the AP {terms}, …', fs(s), f'Sₙ = n/2 [2a + (n − 1)d] = {n}/2 [{2 * a} + {n - 1} × {fs(d)}] = {fs(s)}.'.replace('+ −', '− ').replace('[-', '[−'),
             [fs(Fr(n, 2) * (2 * a + n * d)), fs(Fr(n, 2) * (a + (n - 1) * d)), fs(a + (n - 1) * d)])


def c8s2_sn(r):
    p, q = r.randint(1, 5), r.randint(-4, 6)
    n0 = r.randint(8, 25)
    an = lambda n: p * (2 * n - 1) + q
    sn = poly([p, q, 0], 'n')
    return Q(M(f'The sum of the first n terms of an AP is {sn}. Find the nth term, the common difference and the {ordn(n0)} term.'), M(f'aₙ = {lin(2 * p, q - p, "n")}; d = {2 * p}; a{"".join("₀₁₂₃₄₅₆₇₈₉"[int(c)] for c in str(n0))} = {an(n0)}'),
             M(f'aₙ = Sₙ − Sₙ₋₁ (1) = {p}[n² − (n − 1)²] {"+" if q >= 0 else "−"} {abs(q)}[n − (n − 1)] (1) = {lin(2 * p, q - p, "n")} (1); d = {2 * p} (1); put n = {n0}: {an(n0)} (1).'),
             [M(f'aₙ = {lin(p, q, "n")}; d = {p}; a = {p * n0 + q}'), M(f'aₙ = {lin(2 * p, q, "n")}; d = {2 * p}; a = {2 * p * n0 + q}'), M(f'aₙ = {lin(2 * p, q - p, "n")}; d = {p}; a = {an(n0)}')])


def c8s2_salary(r):
    who = name(r)
    a = r.choice([18000, 20000, 25000, 30000, 32000])
    inc = r.choice([500, 800, 1000, 1200, 1500])
    yrs = r.randint(5, 12)
    last = a + (yrs - 1) * inc
    total = yrs * 12 * (a + last) // 2
    return Q(f'{who} starts a job at ₹{ind(a)} per month with an annual increment of ₹{ind(inc)} per month. Find the monthly salary in the {ordn(yrs)} year and the total salary earned in {yrs} years.',
             f'₹{ind(last)}; ₹{ind(total)}', f'Monthly salaries form an AP with a = {ind(a)}, d = {ind(inc)} (1); {ordn(yrs)} year: a + {yrs - 1}d = ₹{ind(last)} (1); total = 12 × {yrs}/2 × ({ind(a)} + {ind(last)}) = ₹{ind(total)} (2).',
             [f'₹{ind(a + yrs * inc)}; ₹{ind(12 * yrs * (2 * a + yrs * inc) // 2)}', f'₹{ind(last)}; ₹{ind(yrs * (a + last) // 2)}', f'₹{ind(last)}; ₹{ind(12 * yrs * a)}'])


def c8s2_case(r):
    city = r.choice(CITIES)
    first = r.choice([50, 60, 75, 80, 100])
    d = r.choice([5, 10, 15, 20])
    n = r.randint(15, 30)
    an = first + (n - 1) * d
    sn = n * (first + an) // 2
    target = r.choice([x for x in range(first + 5 * d, an, d)])
    k = (target - first) // d + 1
    return {'stem': f'A charity drive in {city} collects ₹{first} on day 1, and each day the collection is ₹{d} more than the day before. The drive lasts {n} days.\n'
                    f'(i) Show that the daily collections form an AP and write a and d. (ii) Find the collection on the last day. (iii) On which day is ₹{target} collected? (iv) Find the total amount collected.',
            'answer': f'(i) a = {first}, d = {d} (ii) ₹{an} (iii) day {k} (iv) ₹{ind(sn)}',
            'key': f'(i) Constant difference {d} (1). (ii) a + (n − 1)d (1). (iii) {first} + (k − 1){d} = {target} (1). (iv) n/2 (a + l) (1).'}


c8s2_tf = tf_mcq('arithmetic progressions',
                 ['The nth term of an AP is a + (n − 1)d.', 'The sum of n terms of an AP is n/2 [2a + (n − 1)d].', 'The AM of a and b is (a + b)/2.',
                  'If a constant is added to every term of an AP, the result is an AP.', 'If Sₙ is a quadratic in n with no constant term, the sequence is an AP.'],
                 ['The nth term of an AP is a + nd.', 'The AM of a and b is √(ab).', 'Multiplying each term of an AP by a constant destroys the AP.',
                  'The sum of n terms of an AP is n(a + l).', 'An AP cannot have a negative common difference.'])

c8s2_ar = pool_ar([
    ('The AM between 7 and 13 is 10.', 'The AM of a and b is (a + b)/2.', 'a', 'R explains A.'),
    ('The nth term of the sequence with Sₙ = 3n² + 2n is 6n − 1.', 'aₙ = Sₙ − Sₙ₋₁.', 'a', 'R explains A.'),
    ('The terms 2, 5, 8, 11, … form an AP with d = 3.', 'In an AP the ratio of consecutive terms is constant.', 'c', 'A is true; R is false (the difference is constant).'),
])

c8s2_explain = pool_txt([
    ('Derive the formula for the sum of the first n terms of an AP.', 'Write S forwards and backwards and add: 2S = n(2a + (n − 1)d).', '2 marks.'),
    ('Show that the sum of the n arithmetic means between a and b is n(a + b)/2.', 'The means with a and b form an AP; their sum = n × (first mean + last mean)/2 = n(a + b)/2.', '2 marks.'),
])

# st3 GP


def c8s3_nth(r):
    a = r.choice([1, 2, 3, 5, Fr(1, 2), Fr(5, 2), -3])
    q = r.choice([2, 3, -2, Fr(1, 2), Fr(-1, 2), Fr(3, 2)])
    n = r.randint(5, 10)
    v = a * q ** (n - 1)
    return Q(f'Find the {ordn(n)} term of the GP {fs(a)}, {fs(a * q)}, {fs(a * q * q)}, …', fs(v), f'aₙ = arⁿ⁻¹ with a = {fs(a)}, r = {fs(q)}: {fs(a)} × ({fs(q)}){sup(n - 1)} = {fs(v)}.',
             [fs(a * q ** n), fs(a * q ** (n - 2)), fs(-v)])


def c8s3_sum(r):
    a = r.choice([1, 2, 3, 5, 7])
    q = r.choice([2, 3, Fr(1, 2), Fr(1, 3), -2])
    n = r.randint(5, 9)
    s = a * (1 - q ** n) / (1 - q)
    return Q(f'Find the sum of the first {n} terms of the GP {fs(a)}, {fs(a * q)}, {fs(a * q * q)}, …', fs(s),
             f'Sₙ = a(rⁿ − 1)/(r − 1) (or a(1 − rⁿ)/(1 − r)) with a = {fs(a)}, r = {fs(q)}, n = {n} = {fs(s)}.', [fs(a * (1 - q ** (n + 1)) / (1 - q)), fs(a * q ** (n - 1)), fs(a * (1 - q ** (n - 1)) / (1 - q))])


def c8s3_which(r):
    a = r.choice([1, 2, 3, 5, Fr(1, 4)])
    q = r.choice([2, 3, Fr(1, 2)])
    n = r.randint(5, 11)
    v = a * q ** (n - 1)
    return Q(f'Which term of the GP {fs(a)}, {fs(a * q)}, {fs(a * q * q)}, … is {fs(v)}?', f'the {ordn(n)} term',
             f'{fs(a)} × ({fs(q)})ⁿ⁻¹ = {fs(v)} ⇒ ({fs(q)})ⁿ⁻¹ = {fs(v / a)} = ({fs(q)}){sup(n - 1)} (1) ⇒ n = {n} (1).',
             [f'the {ordn(n - 1)} term', f'the {ordn(n + 1)} term', f'the {ordn(2 * n)} term'])


def c8s3_find(r):
    a = r.choice([1, 2, 3, -2, Fr(1, 2)])
    q = r.choice([2, 3, -2, -3, Fr(1, 2)])
    p, s = sorted(r.sample(range(2, 9), 2))
    if s - p not in (2, 3):
        s = p + r.choice([2, 3])
    tp, ts = a * q ** (p - 1), a * q ** (s - 1)
    if (s - p) % 2 == 0 and q < 0:
        q = -q
        tp, ts = a * q ** (p - 1), a * q ** (s - 1)
    nn = r.randint(s + 1, s + 3)
    return Q(f'The {ordn(p)} term of a GP is {fs(tp)} and its {ordn(s)} term is {fs(ts)}. Find the first term, the common ratio and the {ordn(nn)} term.',
             f'a = {fs(a)}, r = {fs(q)}, a{"".join("₀₁₂₃₄₅₆₇₈₉"[int(c)] for c in str(nn))} = {fs(a * q ** (nn - 1))}',
             f'ar{sup(p - 1) if p > 2 else ""} = {fs(tp)}, ar{sup(s - 1)} = {fs(ts)} (1); divide: r{sup(s - p)} = {fs(ts / tp)} ⇒ r = {fs(q)} (1){" (taking the real root)" if (s - p) % 2 else ""}; a = {fs(a)} (1); term = {fs(a * q ** (nn - 1))} (1).',
             [f'a = {fs(a * q)}, r = {fs(q)}, a = {fs(a * q ** nn)}', f'a = {fs(a)}, r = {fs(-q)}, a = {fs(a * (-q) ** (nn - 1))}', f'a = {fs(a)}, r = {fs(q * q)}, a = {fs(a * q ** (2 * nn - 2))}'])


def c8s3_growth(r):
    kind = r.choice(['bact', 'money', 'pop'])
    if kind == 'bact':
        b0 = r.choice([20, 30, 50, 100])
        h = r.randint(4, 9)
        v = b0 * 2 ** h
        return Q(f'The number of bacteria in a culture doubles every hour. If there are {b0} bacteria at the start, how many will there be at the end of the {ordn(h)} hour?', f'{ind(v)}',
                 f'Counts form a GP {b0}, {2 * b0}, {4 * b0}, … ; after h hours: {b0} × 2{sup(h)} (1) = {ind(v)} (1).', [f'{ind(b0 * 2 ** (h - 1))}', f'{ind(b0 * 2 * h)}', f'{ind(b0 * 2 ** (h + 1))}'])
    if kind == 'money':
        P = r.choice([500, 1000, 2000, 5000])
        rt = r.choice([5, 10, 20])
        n = r.randint(3, 6)
        v = Fr(P) * Fr(100 + rt, 100) ** n
        return Q(f'₹{ind(P)} is deposited at {rt}% per annum compound interest. Find the amount at the end of {n} years (to the nearest paisa).', f'{rs2(float(v))}',
                 f'Amounts form a GP with r = {fs(Fr(100 + rt, 100))} (1); A = {P} × ({float(Fr(100 + rt, 100)):g}){sup(n)} = {rs2(float(v))} (1).',
                 [f'{rs2(P * (1 + rt * n / 100))}', f'{rs2(float(Fr(P) * Fr(100 + rt, 100) ** (n - 1)))}', f'{rs2(float(v) + P)}'])
    p0 = r.choice([10000, 20000, 50000])
    k = r.choice([10, 20])
    n = r.randint(2, 4)
    v = Fr(p0) * Fr(100 + k, 100) ** n
    town = r.choice(CITIES)
    return Q(f'The population of a locality in {town} is {ind(p0)} and grows by {k}% every year. Find the population after {n} years.', f'{ind(round(float(v)))}',
             f'Population after n years: {ind(p0)} × (1.{k:02d})ⁿ (GP) (1) = {ind(round(float(v)))} (1).'.replace('(1.10)', '(1.1)').replace('(1.20)', '(1.2)'),
             [f'{ind(round(p0 * (1 + k * n / 100)))}', f'{ind(round(float(Fr(p0) * Fr(100 + k, 100) ** (n + 1))))}', f'{ind(round(float(Fr(p0) * Fr(100 + k, 100) ** (n - 1))))}'])


def c8s3_case(r):
    who = name(r)
    first = r.choice([1, 2, 5])
    q = r.choice([2, 3])
    n = r.randint(6, 9)
    tn = first * q ** (n - 1)
    sn = first * (q ** n - 1) // (q - 1)
    return {'stem': f'{who} starts a savings challenge: put ₹{first} in a piggy bank on day 1 and each day put {"double" if q == 2 else "three times"} the previous day\'s amount.\n'
                    f'(i) Name the type of sequence formed and write its first term and common ratio. (ii) How much is put in on day {n}? (iii) What is the total saved in {n} days? '
                    f'(iv) Explain why this plan cannot go on for a whole month.',
            'answer': f'(i) GP, a = {first}, r = {q} (ii) ₹{ind(tn)} (iii) ₹{ind(sn)} (iv) amounts grow exponentially; day 30 alone would need ₹{first if first > 1 else ""}{" × " if first > 1 else ""}{q}²⁹, about ₹{sig(first * q ** 29, 2)}',
            'key': f'(i) Constant ratio (1). (ii) arⁿ⁻¹ (1). (iii) a(rⁿ − 1)/(r − 1) (1). (iv) {first} × {q}²⁹ is huge (1).'}


c8s3_tf = tf_mcq('geometric progressions',
                 ['The nth term of a GP is arⁿ⁻¹.', 'The sum of n terms of a GP with r ≠ 1 is a(rⁿ − 1)/(r − 1).', 'If each term of a GP is multiplied by a non-zero constant, the result is a GP.',
                  'In a GP the ratio of any term to the preceding term is constant.', 'The reciprocals of the terms of a GP also form a GP.'],
                 ['The nth term of a GP is arⁿ.', 'The sum of n terms of a GP is n/2 (a + l).', 'In a GP the difference of consecutive terms is constant.',
                  'A GP cannot have a negative common ratio.', 'The common ratio of a GP can be zero.'])

c8s3_ar = pool_ar([
    ('The 8th term of the GP 5, 10, 20, … is 640.', 'aₙ = arⁿ⁻¹ with a = 5, r = 2.', 'a', 'R explains A: 5 × 2⁷ = 640.'),
    ('If a, b, c are in GP then b² = ac.', 'b/a = c/b in a GP.', 'a', 'R explains A.'),
    ('The sequence 2, 4, 8, 14, … is a GP.', 'In a GP each term is obtained by multiplying the previous term by a fixed number.', 'd', 'A is false: 8/4 ≠ 14/8; R is true.'),
])

c8s3_explain = pool_txt([
    ('Derive the formula for the sum of the first n terms of a GP.', 'S = a + ar + … + arⁿ⁻¹; rS − S = arⁿ − a ⇒ S = a(rⁿ − 1)/(r − 1).', '2 marks.'),
    ('Why does the formula Sₙ = a(rⁿ − 1)/(r − 1) fail for r = 1, and what is the sum then?', 'Division by zero; with r = 1 all terms equal a, so Sₙ = na.', '2 marks.'),
])

# st4 GM and AM-GM


def c8s4_gm(r):
    k = r.choice([1, 2, 3, 5])
    m, n = r.sample([1, 2, 3, 4, 5, 6, 7], 2)
    a, b = k * m * m, k * n * n
    return Q(f'Find the geometric mean of {a} and {b}.', str(k * m * n), f'G = √(ab) = √({a} × {b}) = √{a * b} = {k * m * n}.',
             [fs(Fr(a + b, 2)), str(a * b), str(k * m * n + 1)])


def c8s4_insert(r):
    a = r.choice([1, 2, 3, 4, 5])
    q = r.choice([2, 3, -2])
    k = r.randint(2, 4)
    if q < 0 and k % 2 == 0:
        q = -q
    b = a * q ** (k + 1)
    ms = [a * q ** i for i in range(1, k + 1)]
    return Q(f'Insert {k} geometric means between {a} and {b}.', ', '.join(fs(x) for x in ms),
             f'{k + 2} terms in GP: {b} = {a} r{sup(k + 1)} ⇒ r{sup(k + 1)} = {fs(Fr(b, a))} ⇒ r = {q} (1); means ' + ', '.join(fs(x) for x in ms) + ' (1).',
             [', '.join(fs(a + i * Fr(b - a, k + 1)) for i in range(1, k + 1)), ', '.join(fs(x * q) for x in ms), ', '.join(fs(-x) for x in ms)])


def c8s4_ab(r):
    k = r.choice([1, 2, 3])
    m, n = sorted(r.sample([1, 2, 3, 4, 5, 6], 2))
    if (m + n) % 2 and k % 2:
        k *= 2 if r.random() < 0.5 else 1
    a, b = k * n * n, k * m * m
    A, G = Fr(a + b, 2), k * m * n
    return Q(f'The AM and GM of two positive numbers are {fs(A)} and {G} respectively. Find the numbers.', f'{a} and {b}',
             f'a + b = {fs(2 * A)}, ab = {G * G} (1); the numbers are roots of t² − {fs(2 * A)}t + {G * G} = 0 (1); (a − b)² = (a + b)² − 4ab ⇒ a − b = {a - b} (1); a = {a}, b = {b} (1).',
             [f'{a + 1} and {b - 1}', f'{fs(A)} and {G}', f'{a // k if k > 1 else a + b} and {b // k if k > 1 else 1}'])


def c8s4_min(r):
    k = r.choice([9, 16, 25, 36, 49])
    c = r.choice([1, 2, 3])
    v = 2 * c * math.isqrt(k)
    return mcq(f'For x > 0, the least value of {c if c > 1 else ""}x + {c * k if c > 1 else k}/x is', str(v),
               [str(c * k), str(math.isqrt(k)), str(v + c)], f'By AM ≥ GM, {c if c > 1 else ""}(x + {k}/x) ≥ {str(c) + " × " if c > 1 else ""}2√{k} = {v}, equality at x = {math.isqrt(k)}.', r)


def c8s4_ratio(r):
    p, q = sorted(r.sample([1, 2, 3, 4, 5, 6, 7], 2), reverse=True)
    if math.gcd(p, q) != 1:
        raise ValueError
    A, G = p * p + q * q, 2 * p * q
    g = math.gcd(A, G)
    A, G = A // g, G // g
    return Q(f'The ratio of the AM to the GM of two positive numbers a and b is {A} : {G}. Find a : b.', f'{p * p} : {q * q}',
             f'Let a = x², b = y² (x, y > 0); (x² + y²)/2 : xy = {A} : {G} (1) ⇒ {G}x² − {2 * A}xy + {G}y² = 0 (2); solving for x/y gives {fs(Fr(p, q))} (take the root > 1) (1) ⇒ a : b = {p * p} : {q * q} (1).',
             [f'{p} : {q}', f'{A} : {G}', f'{p * p + q * q} : {2 * p * q}'])


def c8s4_case(r):
    who = name(r)
    P = r.choice([16, 36, 64, 100, 144])
    s = math.isqrt(P)
    return {'stem': f'{who} wants to fence a rectangular kitchen garden of area {P} m² using the least length of fencing.\n'
                    f'(i) If the sides are x m and y m, write xy and the perimeter. (ii) Use AM ≥ GM to show that x + y ≥ {2 * s}. (iii) Find the least perimeter and the shape that gives it. '
                    f'(iv) If the fencing costs ₹{r.choice([150, 200, 250])} per metre, find the least cost.',
            'answer': f'(i) xy = {P}, perimeter 2(x + y) (ii) (x + y)/2 ≥ √(xy) = {s} (iii) {4 * s} m, square of side {s} m (iv) see key',
            'key': '(i) (1). (ii) AM ≥ GM (1). (iii) equality when x = y (1). (iv) least perimeter × rate (1).'}


def _c8s4_case(r):
    d = c8s4_case(r)
    rate = int(re.search(r'₹(\d+) per metre', d['stem']).group(1))
    s = int(re.search(r'\(iii\) (\d+) m', d['answer']).group(1))
    d['answer'] = d['answer'].replace('(iv) see key', f'(iv) ₹{ind(s * rate)}')
    return d


c8s4_tf = tf_mcq('geometric mean and the AM-GM inequality',
                 ['The GM of two positive numbers a and b is √(ab).', 'For positive a, b, (a + b)/2 ≥ √(ab).', 'AM = GM exactly when a = b.',
                  'If G is the GM of a and b, then a, G, b are in GP.', 'For x > 0, x + 1/x ≥ 2.'],
                 ['The GM of a and b is (a + b)/2.', 'For positive a, b, √(ab) > (a + b)/2.', 'AM = GM for all a, b.', 'The GM of 4 and 9 is 6.5.', 'For x > 0, x + 1/x ≤ 2.'])

c8s4_ar = pool_ar([
    ('For positive numbers a and b, (a + b)/2 ≥ √(ab).', '(√a − √b)² ≥ 0.', 'a', 'Expanding R gives A.'),
    ('The GM of 2 and 8 is 4.', 'G = √(ab).', 'a', 'R explains A.'),
    ('The AM of 4 and 16 is less than their GM.', 'AM ≥ GM for positive numbers.', 'd', 'A is false (AM 10, GM 8); R is true.'),
])

c8s4_explain = pool_txt([
    ('Prove that A ≥ G for two positive numbers a and b.', 'A − G = (a + b)/2 − √(ab) = (√a − √b)²/2 ≥ 0.', '2 marks.'),
    ('Show that the product of two positive numbers with a fixed sum is greatest when they are equal.', 'xy ≤ ((x + y)/2)² by AM ≥ GM, equality at x = y.', '2 marks.'),
])


# ======================================================== ch09 Straight Lines
# st1 slope

def _pts(r, lo=-6, hi=9):
    while True:
        x1, y1, x2, y2 = (r.randint(lo, hi) for _ in range(4))
        if x1 != x2 and (x1, y1) != (x2, y2):
            return x1, y1, x2, y2


def c9s1_slope(r):
    x1, y1, x2, y2 = _pts(r)
    m = Fr(y2 - y1, x2 - x1)
    return Q(f'Find the slope of the line through {pt(x1, y1)} and {pt(x2, y2)}.', fs(m), f'm = (y₂ − y₁)/(x₂ − x₁) = ({fs(y2)} − {pp(y1)})/({fs(x2)} − {pp(x1)}) = {fs(m)}.',
             [fs(1 / m) if m else '1', fs(-m) if m else '−1', fs(Fr(x2 - x1, y2 - y1)) if y2 != y1 and Fr(x2 - x1, y2 - y1) != 1 / m else fs(m + 1)])


ANG = {30: '1/√3', 45: '1', 60: '√3', 120: '−√3', 135: '−1', 150: '−1/√3', 0: '0'}


def c9s1_incl(r):
    t = r.choice([30, 45, 60, 120, 135, 150])
    rev = r.random() < 0.4
    if rev:
        return mcq(f'A line has slope {ANG[t]}. Its inclination (angle with the positive x-axis, 0° ≤ θ < 180°) is', f'{t}°',
                   [f'{x}°' for x in r.sample([a for a in ANG if a not in (t, 0)], 3)], f'tan θ = {ANG[t]} with 0° ≤ θ < 180° ⇒ θ = {t}°.', r)
    return mcq(f'The slope of a line inclined at {t}° to the positive x-axis is', ANG[t], [ANG[x] for x in r.sample([a for a in ANG if a not in (t, 0)], 3)],
               f'm = tan {t}° = {ANG[t]}.', r)


def c9s1_parperp(r):
    x1, y1, x2, y2 = _pts(r)
    m1 = Fr(y2 - y1, x2 - x1)
    kind = r.choice(['par', 'perp', 'neither'])
    if m1 == 0 and kind == 'perp':
        kind = 'par'
    if kind == 'par':
        m2 = m1
    elif kind == 'perp':
        m2 = -1 / m1
    else:
        m2 = m1 + r.choice([1, 2, -1])
        if m1 * m2 == -1:
            m2 += 1
    a, b = r.randint(-5, 5), r.randint(-5, 5)
    dx = m2.denominator * r.choice([1, 2])
    c, d = a + dx, b + m2 * dx
    ans = {'par': 'parallel', 'perp': 'perpendicular', 'neither': 'neither parallel nor perpendicular'}[kind]
    return mcq(f'The line through {pt(x1, y1)} and {pt(x2, y2)} and the line through {pt(a, b)} and {pt(c, d)} are', ans,
               [x for x in ['parallel', 'perpendicular', 'neither parallel nor perpendicular', 'the same line'] if x != ans],
               f'Slopes {fs(m1)} and {fs(m2)}; parallel if equal, perpendicular if the product is −1.', r)


def c9s1_angle(r):
    t = r.choice([30, 45, 60, 90])
    m1 = Fr(r.randint(-3, 4), r.choice([1, 1, 2]))
    tant = {30: None, 45: Fr(1), 60: None, 90: None}[t]
    if t == 90:
        if m1 == 0:
            raise ValueError
        m2 = -1 / m1
        val = 'θ = 90°'
        key = f'm₁m₂ = −1, so the lines are perpendicular.'
    else:
        # choose m2 to give a rational tan θ
        m2 = Fr(r.randint(-4, 5), r.choice([1, 2, 3]))
        if m1 == m2 or 1 + m1 * m2 == 0:
            raise ValueError
        tv = abs((m2 - m1) / (1 + m1 * m2))
        val = f'tan θ = {fs(tv)}'
        if tv == 1:
            val = 'θ = 45°'
        key = f'tan θ = |(m₂ − m₁)/(1 + m₁m₂)| = |({fs(m2)} − ({fs(m1)}))/(1 + ({fs(m1)})({fs(m2)}))| = {fs(tv)}' + (', so θ = 45°' if tv == 1 else '') + '.'
        return Q(f'Find the acute angle θ between the lines with slopes {fs(m1)} and {fs(m2)} (give tan θ, or θ if it is a standard angle).', val, key,
                 [f'tan θ = {fs(abs((m2 - m1) / (1 - m1 * m2)))}' if 1 - m1 * m2 != 0 else 'θ = 90°', f'tan θ = {fs(abs(m2 - m1))}', f'tan θ = {fs(abs((m2 + m1) / (1 + m1 * m2)))}'])
    return Q(f'Find the acute angle θ between the lines with slopes {fs(m1)} and {fs(m2)}.', val, key, ['θ = 45°', 'θ = 0°', 'θ = 60°'])


def c9s1_collinear(r):
    x1, y1 = r.randint(-5, 5), r.randint(-5, 5)
    dx, dy = r.choice([1, 2, 3, -1, -2]), r.randint(-4, 4)
    s, t = r.choice([2, 3, -1, -2]), r.choice([3, 4, -3])
    p2 = (x1 + s * dx, y1 + s * dy)
    p3x, p3y = x1 + t * dx, y1 + t * dy
    if r.random() < 0.5:
        stem = f'Find k so that the points {pt(x1, y1)}, {pt(*p2)} and (k, {fs(p3y)}) are collinear.'
        if dy == 0:
            raise ValueError
        ans = f'k = {fs(p3x)}'
        wrong = [f'k = {fs(p3x + dx)}', f'k = {fs(-p3x)}' if p3x else 'k = 1', f'k = {fs(p3y)}' if p3y != p3x else f'k = {fs(p3x + 2)}']
    else:
        stem = f'Find k so that the points {pt(x1, y1)}, {pt(*p2)} and ({fs(p3x)}, k) are collinear.'
        ans = f'k = {fs(p3y)}'
        wrong = [f'k = {fs(p3y + 1)}', f'k = {fs(-p3y)}' if p3y else 'k = 2', f'k = {fs(p3x)}' if p3x != p3y else f'k = {fs(p3y - 2)}']
    return Q(stem, ans, 'Collinear ⇔ slope of the first two points = slope of the first and third point (1); solve for k (1).', wrong)


def c9s1_perpk(r):
    a, b = r.randint(-4, 6), r.randint(-4, 6)
    c, d = a + r.choice([1, 2, 3, -2]), b + r.choice([1, 2, 3, -1, -3])
    m1 = Fr(d - b, c - a)
    if m1 == 0:
        raise ValueError
    m2 = -1 / m1
    x0, y0 = r.randint(-3, 5), r.randint(-3, 5)
    dx = r.choice([2, 3, 4, -2])
    y1 = y0 + m2 * dx
    k = x0 + dx
    return Q(f'Find k if the line through {pt(a, b)} and {pt(c, d)} is perpendicular to the line through ({fs(x0)}, {fs(y0)}) and (k, {fs(y1)}).', f'k = {fs(k)}',
             f'm₁ = {fs(m1)} (1); m₂ = ({fs(y1)} − {fs(y0)})/(k − {fs(x0)}) (1); m₁m₂ = −1 (1) ⇒ k = {fs(k)} (1).'.replace('− −', '+ '),
             [f'k = {fs(x0 - dx)}', f'k = {fs(x0 + m1 * dx)}' if x0 + m1 * dx != k else f'k = {fs(k + 1)}', f'k = {fs(-k)}' if k else 'k = 1'])


c9s1_tf = tf_mcq('the slope of a line',
                 ['Two non-vertical lines are parallel if and only if their slopes are equal.', 'Two non-vertical lines are perpendicular if and only if m₁m₂ = −1.',
                  'The slope of the x-axis is 0.', 'The slope of a vertical line is not defined.', 'Three points are collinear if the slopes of AB and BC are equal.'],
                 ['The slope of the y-axis is 0.', 'Perpendicular lines have equal slopes.', 'A line inclined at 135° has slope 1.', 'The slope of a line through (1, 2) and (3, 2) is not defined.',
                  'If m₁m₂ = 1, the lines are perpendicular.'])

c9s1_ar = pool_ar([
    ('Lines with slopes 2 and −1/2 are perpendicular.', 'Two non-vertical lines are perpendicular when the product of their slopes is −1.', 'a', 'R explains A.'),
    ('The points (1, 2), (3, 6) and (4, 8) are collinear.', 'The slopes of the segments joining them are equal (each is 2).', 'a', 'R explains A.'),
    ('A line making 120° with the positive x-axis has slope √3.', 'm = tan θ.', 'd', 'A is false: tan 120° = −√3; R is true.'),
])

c9s1_explain = pool_txt([
    ('Derive the formula for the angle between two lines with slopes m₁ and m₂.', 'θ = θ₂ − θ₁; tan θ = (tan θ₂ − tan θ₁)/(1 + tan θ₁ tan θ₂) = (m₂ − m₁)/(1 + m₁m₂).', '2 marks.'),
    ('Show that two non-vertical lines are perpendicular if and only if m₁m₂ = −1.', 'θ₂ = θ₁ + 90°, so tan θ₂ = −cot θ₁ = −1/m₁.', '2 marks.'),
])

# st2 forms of the equation


def _std(a, b, c):
    """ax + by + c = 0 with integer coefficients, a > 0 (or b > 0)."""
    a, b, c = Fr(a), Fr(b), Fr(c)
    L = math.lcm(a.denominator, b.denominator, c.denominator)
    a, b, c = int(a * L), int(b * L), int(c * L)
    g_ = math.gcd(math.gcd(abs(a), abs(b)), abs(c)) or 1
    a, b, c = a // g_, b // g_, c // g_
    if a < 0 or (a == 0 and b < 0):
        a, b, c = -a, -b, -c
    out = ''
    for co, v in ((a, 'x'), (b, 'y'), (c, '')):
        out += term(co, v, out == '')
    return (out or '0') + ' = 0', (a, b, c)


def c9s2_point(r):
    x0, y0 = r.randint(-5, 6), r.randint(-5, 6)
    m = r.choice([Fr(r.randint(-4, 4)), Fr(r.randint(-3, 3), r.choice([2, 3]))])
    eq, _ = _std(m, -1, y0 - m * x0)
    return Q(f'Find the equation of the line through {pt(x0, y0)} with slope {fs(m)}.', eq,
             f'y − y₀ = m(x − x₀): y − ({fs(y0)}) = {fs(m)}(x − ({fs(x0)})) ⇒ {eq}.', [_std(m, -1, y0 + m * x0)[0], _std(-m, -1, y0 + m * x0)[0], _std(1, -m, y0 - x0)[0]])


def c9s2_two(r):
    x1, y1, x2, y2 = _pts(r)
    m = Fr(y2 - y1, x2 - x1)
    eq, _ = _std(m, -1, y1 - m * x1)
    return Q(f'Find the equation of the line through {pt(x1, y1)} and {pt(x2, y2)}.', eq,
             f'm = {fs(m)} (1); y − {fs(y1)} = {fs(m)}(x − {fs(x1)}) ⇒ {eq} (1).'.replace('− −', '+ '),
             [_std(-m, -1, y1 + m * x1)[0], _std(1 / m if m else 1, -1, y1 - (1 / m if m else 1) * x1)[0], _std(m, -1, y2 - m * x1)[0] if y2 != y1 else _std(m, -1, y1 + 1)[0]])


def c9s2_int(r):
    a = r.choice([x for x in range(-6, 8) if x])
    b = r.choice([x for x in range(-6, 8) if x])
    kind = r.choice(['given', 'sum'])
    eq, _ = _std(Fr(1, a), Fr(1, b), -1)
    if kind == 'given':
        return Q(f'Find the equation of the line with x-intercept {fs(a)} and y-intercept {fs(b)}.', eq, f'x/a + y/b = 1: x/{fs(a)} + y/{fs(b)} = 1 ⇒ {eq}.',
                 [_std(Fr(1, b), Fr(1, a), -1)[0] if a != b else _std(1, -1, -a)[0], _std(a, b, -1)[0], _std(Fr(1, a), Fr(-1, b), -1)[0]])
    x0 = r.randint(-3, 6)
    s = r.randint(5, 12)
    # line with intercepts summing to s through (x0,y0): pick A, B first
    A = r.choice([x for x in range(1, s) if x])
    B = s - A
    x0 = r.randint(1, A - 1) if A > 1 else 0
    y0 = Fr(B) * (1 - Fr(x0, A))
    # other candidate solutions
    cands = []
    for A2 in range(1, 60):
        for sg in (1,):
            B2 = s - A2
            if B2 == 0:
                continue
            if Fr(x0, A2) + y0 / B2 == 1:
                cands.append((A2, B2))
    eqs = [_std(Fr(1, a_), Fr(1, b_), -1)[0] for a_, b_ in cands]
    ans = ' or '.join(eqs)
    return Q(f'Find the equation of a line through {pt(x0, y0)} whose intercepts on the axes add up to {s} (consider integer intercepts only).', ans,
             f'x/a + y/b = 1 with a + b = {s} (1); substitute the point and solve for a (2); equation(s): {ans} (1).',
             [_std(Fr(1, B), Fr(1, A), -1)[0] if A != B else _std(1, 1, -s - 1)[0], _std(1, 1, -s)[0], _std(Fr(1, A), Fr(-1, B), -1)[0]])


def c9s2_mid(r):
    h, k = r.choice([x for x in range(-5, 6) if x]), r.choice([x for x in range(-5, 6) if x])
    eq, _ = _std(k, h, -2 * h * k)
    return Q(f'Find the equation of the line whose segment intercepted between the axes is bisected at the point {pt(h, k)}.', eq,
             f'Intercepts are (2h, 0) = ({2 * h}, 0) and (0, 2k) = (0, {2 * k}) (1); x/{2 * h} + y/{2 * k} = 1 (1) ⇒ {eq} (1).'.replace('/-', '/−').replace('(-', '(−').replace(' -', ' −'),
             [_std(h, k, -2 * h * k)[0] if h != k else _std(1, -1, 0)[0], _std(k, h, -h * k)[0], _std(Fr(1, h), Fr(1, k), -1)[0]])


def c9s2_median(r):
    while True:
        A = (r.randint(-4, 6), r.randint(-4, 6))
        B = (r.randint(-4, 6), r.randint(-4, 6))
        C = (r.randint(-4, 6), r.randint(-4, 6))
        Mx, My = Fr(B[0] + C[0], 2), Fr(B[1] + C[1], 2)
        if (Mx, My) != A and len({A, B, C}) == 3 and (B[0] - A[0]) * (C[1] - A[1]) != (C[0] - A[0]) * (B[1] - A[1]):
            break
    if Mx == A[0]:
        eq = f'x {"−" if A[0] > 0 else "+"} {abs(A[0])} = 0' if A[0] else 'x = 0'
        eqh = 'vertical line'
    else:
        m = (My - A[1]) / (Mx - A[0])
        eq, _ = _std(m, -1, A[1] - m * A[0])
    alt_m = None
    if C[1] != B[1]:
        alt_m = -Fr(C[0] - B[0], C[1] - B[1])
    alt = _std(alt_m, -1, A[1] - alt_m * A[0])[0] if alt_m is not None else f'x − {A[0]} = 0'.replace('− -', '+ ')
    return Q(f'The vertices of triangle ABC are A{pt(*A)}, B{pt(*B)} and C{pt(*C)}. Find the equations of (i) the median through A and (ii) the altitude through A.', f'(i) {eq} (ii) {alt}',
             f'(i) Midpoint of BC is {pt(Mx, My)} (1); line through A and it (2): {eq}. (ii) Slope of BC, then the perpendicular slope through A (1): {alt} (1).',
             [f'(i) {alt} (ii) {eq}', f'(i) {eq} (ii) {_std(1, 1, -(A[0] + A[1]))[0]}', f'(i) {_std(1, -1, A[1] - A[0])[0]} (ii) {alt}'])


def c9s2_case(r):
    city = r.choice(CITIES)
    base = r.choice([25, 30, 40, 50])
    rate = r.choice([12, 14, 15, 16, 18])
    k1, k2 = sorted(r.sample(range(2, 12), 2))
    f1, f2 = base + rate * k1, base + rate * k2
    km = r.randint(14, 25)
    return {'stem': f'An auto-rickshaw in {city} charges ₹{f1} for a {k1} km ride and ₹{f2} for a {k2} km ride. The fare y (₹) is a linear function of the distance x (km).\n'
                    f'(i) Find the slope of the fare line and interpret it. (ii) Write the equation of the line. (iii) What is the fare for {km} km? (iv) What does the y-intercept represent?',
            'answer': f'(i) {rate}, the charge per km (₹{rate}/km) (ii) y = {rate}x + {base} (iii) ₹{base + rate * km} (iv) the fixed (minimum) charge ₹{base}',
            'key': '(i) (y₂ − y₁)/(x₂ − x₁) (1). (ii) two-point form (1). (iii) substitute x (1). (iv) value at x = 0 (1).'}


c9s2_tf = tf_mcq('forms of the equation of a line',
                 ['The point-slope form is y − y₀ = m(x − x₀).', 'The slope-intercept form is y = mx + c, where c is the y-intercept.', 'The intercept form is x/a + y/b = 1.',
                  'The equation of the x-axis is y = 0.', 'A line parallel to the y-axis at distance a from it is x = ±a.'],
                 ['The equation of the y-axis is y = 0.', 'In y = mx + c, c is the x-intercept.', 'The intercept form is x/a − y/b = 1.',
                  'The line through (2, 3) parallel to the x-axis is x = 2.', 'The two-point form needs the slope to be given.'])

c9s2_ar = pool_ar([
    ('The line x/3 + y/4 = 1 meets the y-axis at (0, 4).', 'In x/a + y/b = 1, b is the y-intercept.', 'a', 'R explains A.'),
    ('The equation of the line through (2, 3) with slope 0 is y = 3.', 'A line with slope 0 is parallel to the x-axis.', 'a', 'R explains A.'),
    ('y = 2x + 5 has x-intercept 5.', 'In y = mx + c, c is the y-intercept.', 'd', 'A is false (x-intercept is −5/2); R is true.'),
])

c9s2_explain = pool_txt([
    ('Derive the point-slope form of the equation of a line.', 'For any point (x, y) on the line, (y − y₀)/(x − x₀) = m ⇒ y − y₀ = m(x − x₀).', '2 marks.'),
    ('Derive the intercept form x/a + y/b = 1.', 'Line through (a, 0) and (0, b): slope −b/a; y = −(b/a)(x − a) ⇒ x/a + y/b = 1.', '2 marks.'),
])

# st3 general equation


def _gen_line(r):
    a = r.choice([x for x in range(-6, 7) if x])
    b = r.choice([x for x in range(-6, 7) if x])
    c = r.randint(-12, 12)
    return a, b, c


def _eqtxt(a, b, c):
    out = ''
    for co, v in ((a, 'x'), (b, 'y'), (c, '')):
        out += term(co, v, out == '')
    return out + ' = 0'


def c9s3_slope(r):
    a, b, c = _gen_line(r)
    m = Fr(-a, b)
    xi = fs(Fr(-c, a)) if c else '0'
    yi = fs(Fr(-c, b)) if c else '0'
    return Q(f'Find the slope and the intercepts on the axes of the line {_eqtxt(a, b, c)}.', f'slope {fs(m)}; x-intercept {xi}; y-intercept {yi}',
             f'Slope = −A/B = {fs(m)} (1); x-intercept −C/A = {xi}, y-intercept −C/B = {yi} (1).',
             [f'slope {fs(-m)}; x-intercept {xi}; y-intercept {yi}', f'slope {fs(Fr(b, a) if a else 1)}; x-intercept {yi}; y-intercept {xi}', f'slope {fs(m)}; x-intercept {fs(Fr(c, a))}; y-intercept {fs(Fr(c, b))}'])


NORM = [(3, 4, 5), (4, 3, 5), (5, 12, 13), (12, 5, 13), (8, 15, 17), (6, 8, 10), (1, 0, 1), (0, 1, 1)]


def c9s3_normal(r):
    a, b, hyp = r.choice(NORM)
    sa, sb = r.choice([1, -1]), r.choice([1, -1])
    a, b = a * sa, b * sb
    p = r.randint(1, 6)
    c = -p * hyp
    cw, sw = Fr(a, hyp), Fr(b, hyp)
    return Q(f'Reduce {_eqtxt(a, b, c)} to the normal form x cos ω + y sin ω = p and find p, cos ω and sin ω.', f'p = {p}; cos ω = {fs(cw)}, sin ω = {fs(sw)}',
             f'√(A² + B²) = {hyp} (1); divide by {hyp} and keep the constant on the right positive: ({fs(cw)})x + ({fs(sw)})y = {p} (1); read off p, cos ω and sin ω (1).',
             [f'p = {p * hyp}; cos ω = {fs(cw)}, sin ω = {fs(sw)}', f'p = {p}; cos ω = {fs(sw)}, sin ω = {fs(cw)}' if cw != sw else f'p = {p}; cos ω = {fs(-cw)}, sin ω = {fs(-sw)}', f'p = {p}; cos ω = {fs(-cw)}, sin ω = {fs(-sw)}'])


def c9s3_intersect(r):
    x0, y0 = r.randint(-5, 6), r.randint(-5, 6)
    while True:
        a1, b1, a2, b2 = (r.choice([x for x in range(-5, 6) if x]) for _ in range(4))
        if a1 * b2 - a2 * b1:
            break
    c1, c2 = -(a1 * x0 + b1 * y0), -(a2 * x0 + b2 * y0)
    return Q(f'Find the point of intersection of the lines {_eqtxt(a1, b1, c1)} and {_eqtxt(a2, b2, c2)}.', pt(x0, y0),
             f'Solve the two equations simultaneously (elimination) (1): x = {fs(x0)}, y = {fs(y0)} (1).', [pt(y0, x0) if x0 != y0 else pt(x0 + 1, y0), pt(-x0, -y0) if (x0, y0) != (0, 0) else pt(1, 1), pt(x0, -y0) if y0 else pt(x0, 1)])


def c9s3_through(r):
    a, b, c = _gen_line(r)
    x0, y0 = r.randint(-5, 6), r.randint(-5, 6)
    kind = r.choice(['par', 'perp'])
    if kind == 'par':
        eq = _eqtxt(a, b, -(a * x0 + b * y0))
        wrong = [_eqtxt(b, -a, -(b * x0 - a * y0)), _eqtxt(a, b, a * x0 + b * y0) if a * x0 + b * y0 else _eqtxt(a, b, 1), _eqtxt(a, -b, -(a * x0 - b * y0))]
    else:
        eq = _eqtxt(b, -a, -(b * x0 - a * y0))
        wrong = [_eqtxt(a, b, -(a * x0 + b * y0)), _eqtxt(b, -a, b * x0 - a * y0) if b * x0 - a * y0 else _eqtxt(b, -a, 1), _eqtxt(b, a, -(b * x0 + a * y0))]
    return Q(f'Find the equation of the line through {pt(x0, y0)} that is {"parallel" if kind == "par" else "perpendicular"} to {_eqtxt(a, b, c)}.', eq,
             f'A {"parallel" if kind == "par" else "perpendicular"} line has the form {"Ax + By" if kind == "par" else "Bx − Ay"} + k = 0 (1); substitute {pt(x0, y0)} to find k (1): {eq} (1).', wrong)


def c9s3_concur(r):
    x0, y0 = r.randint(-4, 5), r.randint(-4, 5)
    if x0 == 0:
        x0 = 2
    a1, b1 = r.choice([1, 2, 3]), r.choice([1, -1, 2, -3])
    a2, b2 = r.choice([1, -2, 3, 4]), r.choice([2, -1, 3, -2])
    if a1 * b2 == a2 * b1:
        raise ValueError
    c1, c2 = -(a1 * x0 + b1 * y0), -(a2 * x0 + b2 * y0)
    b3, c3 = r.choice([1, -1, 2, -2, 3]), r.randint(-9, 9)
    # third line kx + b3 y + c3 = 0 through (x0, y0)
    k = Fr(-(b3 * y0 + c3), x0)
    l3 = f'kx {"+" if b3 > 0 else "−"} {abs(b3) if abs(b3) != 1 else ""}y {"+" if c3 >= 0 else "−"} {abs(c3)} = 0'
    return Q(f'Find the value of k for which the lines {_eqtxt(a1, b1, c1)}, {_eqtxt(a2, b2, c2)} and {l3} are concurrent.', f'k = {fs(k)}',
             f'The first two lines meet at {pt(x0, y0)} (2); this point lies on the third line: {fs(x0)}k + ({fs(b3 * y0)}) + ({fs(c3)}) = 0 (1) ⇒ k = {fs(k)} (1).',
             [f'k = {fs(-k)}' if k else 'k = 1', f'k = {fs(Fr(-(b3 * x0 + c3), y0)) if y0 else fs(k + 1)}', f'k = {fs(k + 1)}'])


c9s3_tf = tf_mcq('the general equation of a line',
                 ['Every first-degree equation Ax + By + C = 0 (A, B not both zero) represents a straight line.', 'The slope of Ax + By + C = 0 (B ≠ 0) is −A/B.',
                  'The y-intercept of Ax + By + C = 0 is −C/B.', 'Lines A₁x + B₁y + C₁ = 0 and A₂x + B₂y + C₂ = 0 are parallel if A₁/A₂ = B₁/B₂ ≠ C₁/C₂.',
                  'In the normal form x cos ω + y sin ω = p, p is the length of the perpendicular from the origin.'],
                 ['The slope of Ax + By + C = 0 is A/B.', 'The x-intercept of Ax + By + C = 0 is C/A.', 'Every equation of degree two represents a straight line.',
                  'In the normal form, p can be negative.', 'Lines 2x + 3y = 5 and 3x + 2y = 5 are parallel.'])

c9s3_ar = pool_ar([
    ('The slope of 3x − 4y + 10 = 0 is 3/4.', 'The slope of Ax + By + C = 0 is −A/B.', 'a', 'R explains A: −3/(−4) = 3/4.'),
    ('The lines 2x + 3y = 7 and 4x + 6y = 9 are parallel.', 'Their coefficients of x and y are proportional but the constants are not.', 'a', 'R explains A.'),
    ('The line 3x + 4y − 15 = 0 is at distance 15 from the origin.', 'In the normal form the constant is divided by √(A² + B²).', 'd', 'A is false (distance 3); R is true.'),
])

c9s3_explain = pool_txt([
    ('How do you convert Ax + By + C = 0 into the intercept form? State when this is not possible.', 'Divide by −C: x/(−C/A) + y/(−C/B) = 1; not possible if C = 0 (line through origin) or A or B is 0.', '2 marks.'),
    ('Explain how to reduce √3x + y − 8 = 0 to normal form.', 'Divide by √(3 + 1) = 2: (√3/2)x + (1/2)y = 4, i.e. x cos 30° + y sin 30° = 4.', '2 marks.'),
])

# st4 distance


def _dist_txt(num_, den2):
    """|num| / √den2 simplified."""
    v = Fr(abs(num_)) / Fr(1)
    a, b = sq_split(den2)
    if b == 1:
        return fs(Fr(abs(num_), a))
    c = Fr(abs(num_), a * b)
    top = '' if c.numerator == 1 else str(c.numerator)
    return f'{top}√{b}' + ('' if c.denominator == 1 else f'/{c.denominator}')


def c9s4_dist(r):
    a, b, c = _gen_line(r)
    x0, y0 = r.randint(-5, 6), r.randint(-5, 6)
    if r.random() < 0.5:
        a, b, _ = r.choice(NORM[:6])
        a, b = a * r.choice([1, -1]), b * r.choice([1, -1])
    n_ = a * x0 + b * y0 + c
    if n_ == 0:
        raise ValueError
    d2 = a * a + b * b
    ans = _dist_txt(n_, d2)
    return Q(f'Find the perpendicular distance of the point {pt(x0, y0)} from the line {_eqtxt(a, b, c)}.', ans + ' units',
             f'd = |Ax₀ + By₀ + C|/√(A² + B²) = |{fs(n_)}|/√{d2} = {ans}.', [_dist_txt(n_ - 2 * c if n_ - 2 * c else 1, d2) + ' units', fs(abs(n_)) + ' units', _dist_txt(n_, abs(a) + abs(b) if abs(a) + abs(b) != d2 else d2 + 1) + ' units'])


def c9s4_par(r):
    a, b, hyp = r.choice(NORM[:6] + [(1, 1, 0), (1, 2, 0), (2, 3, 0)])
    c1, c2 = r.sample(range(-12, 13), 2)
    d2 = a * a + b * b
    ans = _dist_txt(c1 - c2, d2)
    k = r.choice([1, 2])
    return Q(f'Find the distance between the parallel lines {_eqtxt(a, b, c1)} and {_eqtxt(k * a, k * b, k * c2)}.', ans + ' units',
             f'{"Divide the second equation by " + str(k) + " so that the x and y coefficients match (1); " if k > 1 else ""}d = |C₁ − C₂|/√(A² + B²) = |{fs(c1 - c2)}|/√{d2} = {ans} (1).',
             [_dist_txt(c1 + c2 if c1 + c2 else 1, d2) + ' units', fs(abs(c1 - c2)) + ' units', _dist_txt(c1 - k * c2 if c1 - k * c2 else 1, d2) + ' units' if k > 1 else _dist_txt(c1 - c2, d2 + 1) + ' units'])


def c9s4_foot(r):
    a, b, _ = r.choice(NORM[:6] + [(1, 1, 0), (1, -1, 0), (1, 2, 0), (2, -1, 0)])
    a, b = a * r.choice([1, -1]), b
    fx, fy = r.randint(-4, 5), r.randint(-4, 5)
    c = -(a * fx + b * fy)
    t = r.choice([1, 2, -1])
    x0, y0 = fx + a * t, fy + b * t
    return Q(f'Find the coordinates of the foot of the perpendicular from {pt(x0, y0)} to the line {_eqtxt(a, b, c)}, and the image of the point in the line.', f'foot {pt(fx, fy)}; image {pt(2 * fx - x0, 2 * fy - y0)}',
             f'The perpendicular through the point has direction {pt(a, b)} (1); write (x, y) = {pt(x0, y0)} + t{pt(a, b)} and substitute in the line (1); t = {fs(-t)} gives the foot {pt(fx, fy)} (1); the image is at twice the distance: {pt(2 * fx - x0, 2 * fy - y0)} (1).',
             [f'foot {pt(fy, fx)}; image {pt(2 * fy - x0, 2 * fx - y0)}', f'foot {pt(fx, fy)}; image {pt(x0 - fx, y0 - fy)}', f'foot {pt(x0 - a, y0 - b)}; image {pt(x0 - 2 * a, y0 - 2 * b)}'])


def c9s4_onaxis(r):
    a, b, hyp = r.choice(NORM[:6])
    c = r.choice([x for x in range(-24, 25) if x])
    d = r.randint(1, 6)
    xs = sorted({Fr(-c + d * hyp, a), Fr(-c - d * hyp, a)})
    return Q(f'Find the points on the x-axis whose perpendicular distance from the line {_eqtxt(a, b, c)} is {d} units.', ' and '.join(pt(x, 0) for x in xs),
             f'Point (h, 0): |{a}h + ({c})|/{hyp} = {d} (1) ⇒ {a}h + ({c}) = ±{d * hyp} (1) ⇒ h = {" or ".join(fs(x) for x in xs)} (1).'.replace('(-', '(−'),
             [' and '.join(pt(0, x) for x in xs), ' and '.join(pt(Fr(-c + d, a), 0) for _ in [0]) + ' and ' + pt(Fr(-c - d, a), 0), pt(xs[0], 0) + ' only'])


def c9s4_case(r):
    vill = r.choice(['Rampur', 'Sitapur', 'Lakhanpur', 'Devgarh', 'Chandanpur'])
    a, b, hyp = r.choice(NORM[:6])
    x0, y0 = r.randint(1, 8), r.randint(1, 8)
    c = -r.randint(30, 60)
    n_ = a * x0 + b * y0 + c
    if n_ == 0:
        raise ValueError
    d = Fr(abs(n_), hyp)
    rate = r.choice([2, 3, 5])
    return {'stem': f'On a district map (1 unit = 1 km), the new highway is the line {_eqtxt(a, b, c)} and the village {vill} is at {pt(x0, y0)}. A straight link road is to be built from {vill} to the highway.\n'
                    f'(i) What should be the direction of the link road for it to be shortest? (ii) Find the length of the shortest link road. '
                    f'(iii) If the road costs ₹{rate} lakh per km, find the cost. (iv) Find the slope of the link road.',
            'answer': f'(i) perpendicular to the highway (ii) {fs(d)} km (iii) ₹{g(float(d * rate), 2)} lakh (iv) {fs(Fr(b, a))}',
            'key': f'(i) Shortest distance is along the perpendicular (1). (ii) |Ax₀ + By₀ + C|/√(A² + B²) (1). (iii) length × rate (1). (iv) negative reciprocal of {fs(Fr(-a, b))} (1).'}


c9s4_formula = pool_mcq([
    ('The distance of the point (x₁, y₁) from the line Ax + By + C = 0 is', '|Ax₁ + By₁ + C|/√(A² + B²)', ['(Ax₁ + By₁ + C)/(A² + B²)', '|Ax₁ + By₁|/√(A² + B²)', '√(Ax₁ + By₁ + C)'], 'Standard formula.'),
    ('The distance between the parallel lines Ax + By + C₁ = 0 and Ax + By + C₂ = 0 is', '|C₁ − C₂|/√(A² + B²)', ['|C₁ + C₂|/√(A² + B²)', '|C₁ − C₂|/(A² + B²)', '|C₁ − C₂|'], 'Standard formula.'),
    ('The distance of the origin from the line 3x + 4y = 10 is', '2', ['10', '5/2', '10/7'], '|−10|/5 = 2.'),
    ('The distance of the origin from x cos ω + y sin ω = p is', 'p', ['p²', '1/p', 'p cos ω'], 'p is the length of the normal from the origin.'),
])

c9s4_tf = tf_mcq('distances involving lines',
                 ['The perpendicular distance from (x₁, y₁) to Ax + By + C = 0 is |Ax₁ + By₁ + C|/√(A² + B²).', 'The distance of the origin from 5x + 12y = 26 is 2.',
                  'The shortest distance from a point to a line is along the perpendicular.', 'The distance between parallel lines is the same at every point.'],
                 ['The distance of the origin from 5x + 12y = 26 is 26.', 'The distance between 3x + 4y = 5 and 6x + 8y = 5 is 0.',
                  'The distance formula is (Ax₁ + By₁ + C)/(A + B).', 'Parallel lines meet at a point at a finite distance.'])

c9s4_ar = pool_ar([
    ('The distance between 3x + 4y = 9 and 6x + 8y = 15 is 3/10.', 'Before using |C₁ − C₂|/√(A² + B²) the coefficients of x and y must be made equal.', 'a', 'R explains A: 6x + 8y = 18 vs 15 gives 3/10.'),
    ('The point (2, 3) lies at distance 0 from the line x + y − 5 = 0.', 'The point satisfies the equation of the line.', 'a', 'R explains A.'),
    ('The distance of (1, 1) from 3x + 4y = 0 is 7.', 'd = |Ax₁ + By₁ + C|/√(A² + B²).', 'd', 'A is false (7/5); R is true.'),
])

c9s4_explain = pool_txt([
    ('Derive the formula for the distance between two parallel lines y = mx + c₁ and y = mx + c₂.', 'Take the point (0, c₁) on the first line and find its distance from the second: |c₁ − c₂|/√(1 + m²).', '2 marks.'),
    ('Explain why the shortest distance from a point to a line is the perpendicular distance.', 'Any other segment from the point is the hypotenuse of a right triangle with the perpendicular as one side, so it is longer.', '2 marks.'),
])


# ======================================================== ch10 Conic Sections
# st1 circle

def _circ_eq(h, k, rr2):
    g_, f_, c = -2 * h, -2 * k, h * h + k * k - rr2
    out = 'x² + y²'
    out += term(g_, 'x', False) + term(f_, 'y', False) + term(c, '', False)
    return out + ' = 0'


def c10s1_eq(r):
    h, k, rad = r.randint(-5, 6), r.randint(-5, 6), r.randint(1, 8)
    return Q(f'Find the equation of the circle with centre {pt(h, k)} and radius {rad}.', _circ_eq(h, k, rad * rad),
             f'(x − h)² + (y − k)² = r²: (x − ({fs(h)}))² + (y − ({fs(k)}))² = {rad * rad}; expanding gives {_circ_eq(h, k, rad * rad)}.',
             [_circ_eq(-h, -k, rad * rad) if (h, k) != (0, 0) else _circ_eq(0, 0, rad), _circ_eq(h, k, rad), _circ_eq(k, h, rad * rad) if h != k else _circ_eq(h, k, rad * rad + 1)])


def c10s1_cr(r):
    h, k = r.randint(-6, 6), r.randint(-6, 6)
    rad2 = r.choice([1, 4, 9, 16, 25, 36, 49, 2, 5, 10, 13, 20])
    a = r.choice([1, 1, 2, 3])
    eq0 = _circ_eq(h, k, rad2)
    if a > 1:
        g_, f_, c = -2 * h * a, -2 * k * a, (h * h + k * k - rad2) * a
        eq0 = f'{a}x² + {a}y²' + term(g_, 'x', False) + term(f_, 'y', False) + term(c, '', False) + ' = 0'
    rad = surd(rad2)
    return Q(f'Find the centre and the radius of the circle {eq0}.', f'centre {pt(h, k)}, radius {rad}',
             f'{"Divide by " + str(a) + "; " if a > 1 else ""}complete the squares: (x − {pp(h)})² + (y − {pp(k)})² = {rad2} (1) ⇒ centre {pt(h, k)}, radius √{rad2} = {rad} (1).',
             [f'centre {pt(-h, -k)}, radius {rad}' if (h, k) != (0, 0) else f'centre (1, 1), radius {rad}', f'centre {pt(h, k)}, radius {rad2}', f'centre {pt(2 * h, 2 * k)}, radius {rad}' if (h, k) != (0, 0) else f'centre {pt(h, k)}, radius {surd(rad2 + 1)}'])


def c10s1_diam(r):
    x1, y1, x2, y2 = (r.randint(-5, 7) for _ in range(4))
    if (x1, y1) == (x2, y2):
        raise ValueError
    h, k = Fr(x1 + x2, 2), Fr(y1 + y2, 2)
    rad2 = ((x1 - x2) ** 2 + (y1 - y2) ** 2) / Fr(4)
    eq = _circ_eq(h, k, rad2)
    return Q(f'Find the equation of the circle with the ends of a diameter at {pt(x1, y1)} and {pt(x2, y2)}.', eq,
             f'(x − x₁)(x − x₂) + (y − y₁)(y − y₂) = 0 (1) or centre {pt(h, k)}, r² = {fs(rad2)} (1): {eq} (1).',
             [_circ_eq(h, k, rad2 * 4), _circ_eq(-h, -k, rad2) if (h, k) != (0, 0) else _circ_eq(0, 0, rad2 + 1), _circ_eq(x1, y1, rad2 * 4)])


def c10s1_three(r):
    a = r.choice([x for x in range(-8, 9) if x])
    b = r.choice([x for x in range(-8, 9) if x])
    h, k = Fr(a, 2), Fr(b, 2)
    eq = _circ_eq(h, k, h * h + k * k)
    kind = r.choice(['axes', 'line'])
    if kind == 'axes':
        return Q(f'Find the equation of the circle passing through (0, 0), ({a}, 0) and (0, {b}).'.replace('(-', '(−').replace(' -', ' −'), eq,
                 f'Substitute the three points in x² + y² + 2gx + 2fy + c = 0 (1): c = 0 (1), g = {fs(-h)}, f = {fs(-k)} (2); equation {eq} (1).',
                 [_circ_eq(-h, -k, h * h + k * k), _circ_eq(a, b, a * a + b * b), _circ_eq(h, k, h * h + k * k + 1)])
    # through two points, centre on a line y = m x + q
    h, k = r.randint(-4, 5), r.randint(-4, 5)
    rr2 = r.choice([25, 50, 65, 85, 100, 130])
    pts_ = [(x, y) for x in range(-15, 16) for y in range(-15, 16) if (x - h) ** 2 + (y - k) ** 2 == rr2]
    if len(pts_) < 4:
        raise ValueError
    P1, P2 = r.sample(pts_, 2)
    if P1[0] + P2[0] == 2 * h and P1[1] + P2[1] == 2 * k:
        raise ValueError
    m = r.choice([1, -1, 2, -2, 3])
    q = k - m * h
    line = f'y = {m if abs(m) != 1 else ("" if m == 1 else "−")}x'.replace('y = -', 'y = −') + term(q, '', False)
    if m < -1:
        line = f'y = −{abs(m)}x' + term(q, '', False)
    eq = _circ_eq(h, k, rr2)
    return Q(f'Find the equation of the circle passing through {pt(*P1)} and {pt(*P2)} whose centre lies on the line {line}.', eq,
             f'Let the centre be (h, {fs(m)}h + {fs(q)}) (1); equate distances to the two points (2) ⇒ h = {fs(h)}, centre {pt(h, k)} (1); r² = {rr2}: {eq} (1).'.replace('+ -', '− '),
             [_circ_eq(-h, -k, rr2) if (h, k) != (0, 0) else _circ_eq(1, 1, rr2), _circ_eq(h, k, rr2 + 5), _circ_eq(k, h, rr2) if h != k else _circ_eq(h + 1, k, rr2)])


def c10s1_inside(r):
    h, k, rad = r.randint(-3, 3), r.randint(-3, 3), r.randint(3, 7)
    x0, y0 = r.randint(-8, 8), r.randint(-8, 8)
    d2 = (x0 - h) ** 2 + (y0 - k) ** 2
    ans = 'inside the circle' if d2 < rad * rad else 'on the circle' if d2 == rad * rad else 'outside the circle'
    return mcq(f'The point {pt(x0, y0)} lies, with respect to the circle {_circ_eq(h, k, rad * rad)},', ans,
               [x for x in ['inside the circle', 'on the circle', 'outside the circle', 'at the centre'] if x != ans][:3],
               f'Centre {pt(h, k)}, r² = {rad * rad}; the square of the distance of the point from the centre is {d2}, so it is {ans}.', r)


c10s1_sections = term_mcq([('circle', 'the cutting plane is perpendicular to the axis of the cone (β = 90°)'), ('ellipse', 'α < β < 90°, the plane cuts only one nappe across'),
                           ('parabola', 'β = α, the plane is parallel to a generator'), ('hyperbola', '0 ≤ β < α, the plane cuts both nappes')],
                          'When a double cone (semi-vertical angle α) is cut by a plane making angle β with the axis, a {a} is obtained when', 'Which conic is obtained when {b}?', '{a}: {b}.')

c10s1_tf = tf_mcq('circles',
                  ['The equation of a circle with centre (h, k) and radius r is (x − h)² + (y − k)² = r².', 'x² + y² + 2gx + 2fy + c = 0 has centre (−g, −f).',
                   'The radius of x² + y² + 2gx + 2fy + c = 0 is √(g² + f² − c).', 'A circle is a conic obtained when the plane is perpendicular to the axis of the cone.'],
                  ['x² + y² + 2gx + 2fy + c = 0 has centre (g, f).', 'The radius of x² + y² = 16 is 16.', 'x² + 2y² = 9 is a circle.', 'Every equation x² + y² + 2gx + 2fy + c = 0 represents a real circle.'])

c10s1_ar = pool_ar([
    ('x² + y² − 4x + 6y − 12 = 0 is a circle of radius 5.', 'Completing squares gives (x − 2)² + (y + 3)² = 25.', 'a', 'R explains A.'),
    ('The circle x² + y² = 25 passes through (3, 4).', '3² + 4² = 25.', 'a', 'R explains A.'),
    ('x² + y² + 2x + 2y + 5 = 0 represents a real circle.', 'For x² + y² + 2gx + 2fy + c = 0 the radius is √(g² + f² − c).', 'd', 'A is false: g² + f² − c = −3 < 0; R is true.'),
])

c10s1_explain = pool_txt([
    ('Derive the equation of a circle with centre (h, k) and radius r.', 'A point P(x, y) lies on it iff the distance CP = r ⇒ (x − h)² + (y − k)² = r².', '2 marks.'),
    ('Name the four conic sections and say how each arises from a double cone.', 'Circle (β = 90°), ellipse (α < β < 90°), parabola (β = α), hyperbola (0 ≤ β < α).', '2 marks.'),
])

# st2 parabola

PAR = {'y² = 4ax': ('x-axis, opening right', lambda a: (pt(a, 0), f'x = {fs(-a)}'), 'x'), 'y² = −4ax': ('x-axis, opening left', lambda a: (pt(-a, 0), f'x = {fs(a)}'), 'x'),
       'x² = 4ay': ('y-axis, opening up', lambda a: (pt(0, a), f'y = {fs(-a)}'), 'y'), 'x² = −4ay': ('y-axis, opening down', lambda a: (pt(0, -a), f'y = {fs(a)}'), 'y')}


def _par(r):
    form = r.choice(list(PAR))
    a = r.choice([1, 2, 3, 4, 5, Fr(3, 2), Fr(5, 4), Fr(1, 2)])
    k = 4 * a
    eq = form.replace('4a', fs(k) if k != 1 else '')
    return form, a, eq


def c10s2_focus(r):
    form, a, eq = _par(r)
    foc, dirx = PAR[form][1](a)
    return Q(f'Find the coordinates of the focus and the equation of the directrix of the parabola {eq}.', f'focus {foc}; directrix {dirx}',
             f'Compare with {form}: a = {fs(a)} (1); focus {foc}, directrix {dirx} (1).',
             [f'focus {PAR[form][1](4 * a)[0]}; directrix {PAR[form][1](4 * a)[1]}', f'focus {PAR[form][1](-a)[0]}; directrix {PAR[form][1](-a)[1]}', f'focus {foc}; directrix {PAR[form][1](-a)[1]}'])


def c10s2_lr(r):
    form, a, eq = _par(r)
    foc, dirx = PAR[form][1](a)
    ax = 'y = 0 (the x-axis)' if PAR[form][2] == 'x' else 'x = 0 (the y-axis)'
    return Q(f'For the parabola {eq}, find the length of the latus rectum and the axis of the parabola.', f'latus rectum {fs(4 * a)}; axis {ax}',
             f'a = {fs(a)}; latus rectum = 4a = {fs(4 * a)} (1); the parabola is symmetric about {ax} (1).',
             [f'latus rectum {fs(a)}; axis {ax}', f'latus rectum {fs(2 * a)}; axis {ax}', f'latus rectum {fs(4 * a)}; axis {"x = 0 (the y-axis)" if PAR[form][2] == "x" else "y = 0 (the x-axis)"}'])


def c10s2_eq(r):
    form, a, eq = _par(r)
    foc, dirx = PAR[form][1](a)
    kind = r.choice(['fd', 'vf'])
    stem = f'Find the equation of the parabola with focus {foc} and directrix {dirx}.' if kind == 'fd' else f'Find the equation of the parabola with vertex (0, 0) and focus {foc}.'
    return Q(stem, eq, f'The focus lies on the {PAR[form][2]}-axis, {PAR[form][0].split(", ")[1]} (1); a = {fs(a)} and the form is {form} (1): {eq} (1).',
             [form.replace('4a', fs(a) if a != 1 else ''), form.replace('4a', fs(2 * a)), list(PAR)[(list(PAR).index(form) + 1) % 4].replace('4a', fs(4 * a) if 4 * a != 1 else '')])


def pareq(sq, k, v):
    """sq² = k v with integer coefficients: pareq('y', Fr(-16, 5), 'x') -> 5y² = −16x."""
    k = Fr(k)
    d, n = k.denominator, k.numerator
    left = f'{d if d > 1 else ""}{sq}²'
    right = ('−' if n < 0 else '') + (str(abs(n)) if abs(n) != 1 else '') + v
    return f'{left} = {right}'


def c10s2_through(r):
    axis = r.choice(['x', 'y'])
    p, q = r.choice([x for x in range(-6, 7) if x]), r.choice([x for x in range(-6, 7) if x])
    if axis == 'x':
        k = Fr(q * q, p)
        eq = pareq('y', k, 'x')
        wrong = [pareq('x', Fr(p * p, q), 'y'), pareq('y', -k, 'x'), pareq('y', Fr(q, p), 'x')]
    else:
        k = Fr(p * p, q)
        eq = pareq('x', k, 'y')
        wrong = [pareq('y', Fr(q * q, p), 'x'), pareq('x', -k, 'y'), pareq('x', Fr(p, q), 'y')]
    return Q(f'Find the equation of the parabola with vertex at the origin, symmetric about the {axis}-axis and passing through {pt(p, q)}.', eq,
             f'Form {"y² = kx" if axis == "x" else "x² = ky"} (1); substitute {pt(p, q)}: k = {fs(k)} (1); equation {eq} (1).', wrong)


def c10s2_case(r):
    span = r.choice([8, 10, 12, 16, 20])
    h = r.choice([2, 3, 4, 5])
    x0 = r.choice([x for x in range(1, span // 2)])
    a4 = Fr((span // 2) ** 2, h)
    depth = Fr(x0 * x0, 1) / a4
    city = r.choice(CITIES)
    return {'stem': f'A dish antenna on a rooftop in {city} has a parabolic cross-section. The dish is {span} dm across at the rim and {h} dm deep. Take the vertex at the origin and the axis along the positive y-axis.\n'
                    f'(i) Write the form of the equation of the parabola. (ii) Find its equation. (iii) Where should the receiver be placed (focus)? (iv) Find the depth of the dish at {x0} dm from the axis.',
            'answer': f'(i) x² = 4ay (ii) {pareq('x', a4, 'y')} (iii) at (0, {fs(a4 / 4)}) dm, i.e. {fs(a4 / 4)} dm above the vertex (iv) {fs(depth)} dm',
            'key': f'(i) Opens upward (1). (ii) Rim point ({span // 2}, {h}) on it (1). (iii) Focus (0, a) (1). (iv) put x = {x0} in {pareq('x', a4, 'y')} (1).'}


def c10s2_tri(r):
    a = r.choice([1, 2, 3, 4, Fr(1, 2)])
    eq = f'y² = {fs(4 * a) if 4 * a != 1 else ""}x'
    side = 8 * a
    return Q(f'An equilateral triangle is inscribed in the parabola {eq} with one vertex at the vertex of the parabola. Find the length of its side.', f'{fs(side)}√3',
             f'Let the other vertices be (h, ±k) by symmetry (1); for 60° at the vertex, k/h = tan 30° = 1/√3 (1); k² = {fs(4 * a)}h gives h = {fs(12 * a)}, k = {fs(4 * a)}√3 (2); side = 2k = {fs(side)}√3 (1).',
             [f'{fs(4 * a)}√3', f'{fs(side)}', f'{fs(12 * a)}'])


c10s2_tf = tf_mcq('parabolas',
                  ['A parabola is the set of points equidistant from a fixed point (focus) and a fixed line (directrix).', 'For y² = 4ax, the focus is (a, 0).',
                   'The length of the latus rectum of y² = 4ax is 4a.', 'The eccentricity of a parabola is 1.', 'x² = −4ay opens downward.'],
                  ['For y² = 4ax, the directrix is x = a.', 'The latus rectum of y² = 12x has length 3.', 'x² = 4ay is symmetric about the x-axis.',
                   'The eccentricity of a parabola is 0.', 'y² = −8x opens to the right.'])

c10s2_ar = pool_ar([
    ('The focus of y² = 12x is (3, 0).', 'Comparing with y² = 4ax gives a = 3.', 'a', 'R explains A.'),
    ('The parabola x² = −16y opens downward.', 'For x² = −4ay with a > 0, y must be ≤ 0.', 'a', 'R explains A.'),
    ('The directrix of y² = 8x is x = 2.', 'For y² = 4ax the directrix is x = −a.', 'd', 'A is false (x = −2); R is true.'),
])

c10s2_explain = pool_txt([
    ('Derive the equation of the parabola with focus (a, 0) and directrix x = −a.', '√((x − a)² + y²) = |x + a| ⇒ y² = 4ax.', '2 marks.'),
    ('Explain why a parabolic reflector is used in car headlights.', 'Light from a source at the focus reflects off the parabola into a beam parallel to the axis.', '2 marks.'),
])

# st3 ellipse

ELL = [(5, 4, 3), (5, 3, 4), (13, 12, 5), (13, 5, 12), (10, 8, 6), (10, 6, 8), (17, 15, 8), (17, 8, 15), (25, 24, 7), (25, 7, 24), (3, 2, None), (4, 3, None), (6, 4, None)]


def _ell(r, int_c=True):
    while True:
        a, b, c = r.choice(ELL)
        if c is None and int_c:
            continue
        if c is None:
            c2 = a * a - b * b
        else:
            c2 = c * c
        return a, b, c2


def _ell_eq(a2, b2, major='x'):
    return f'x²/{fs(a2)} + y²/{fs(b2)} = 1' if major == 'x' else f'x²/{fs(b2)} + y²/{fs(a2)} = 1'


def c10s3_param(r):
    a, b, c2 = _ell(r, int_c=r.random() < 0.7)
    major = r.choice(['x', 'y'])
    c = surd(c2)
    e = surd(Fr(c2, a * a))
    lr = fs(Fr(2 * b * b, a))
    foci = f'(±{c}, 0)' if major == 'x' else f'(0, ±{c})'
    verts = f'(±{a}, 0)' if major == 'x' else f'(0, ±{a})'
    return Q(f'For the ellipse {_ell_eq(a * a, b * b, major)}, find the coordinates of the foci and the vertices, the eccentricity and the length of the latus rectum.',
             f'foci {foci}; vertices {verts}; e = {e}; latus rectum {lr}',
             f'a² = {a * a}, b² = {b * b} (major axis along the {major}-axis) (1); c = √(a² − b²) = {c} (1); e = c/a = {e}; latus rectum 2b²/a = {lr} (1).',
             [f'foci {verts}; vertices {foci}; e = {e}; latus rectum {lr}', f'foci {foci}; vertices {verts}; e = {surd(Fr(c2, b * b))}; latus rectum {fs(Fr(2 * a * a, b))}',
              f'foci {f"(±{surd(a * a + b * b)}, 0)" if major == "x" else f"(0, ±{surd(a * a + b * b)})"}; vertices {verts}; e = {surd(Fr(a * a + b * b, a * a))}; latus rectum {lr}'])


def c10s3_eq(r):
    a, b, c2 = _ell(r)
    c = math.isqrt(c2)
    major = r.choice(['x', 'y'])
    kind = r.choice(['vf', 'ea', 'lr'])
    eq = _ell_eq(a * a, b * b, major)
    on = 'x' if major == 'x' else 'y'
    P = (lambda v: f'(±{v}, 0)') if major == 'x' else (lambda v: f'(0, ±{v})')
    if kind == 'vf':
        stem = f'Find the equation of the ellipse with vertices {P(a)} and foci {P(c)}.'
        key = f'a = {a}, c = {c} (1); b² = a² − c² = {b * b} (1); {eq} (1).'
    elif kind == 'ea':
        stem = f'Find the equation of the ellipse with centre at the origin, major axis along the {on}-axis, length of the major axis {2 * a} and eccentricity {fs(Fr(c, a))}.'
        key = f'a = {a}, c = ae = {c} (1); b² = {b * b} (1); {eq} (1).'
    else:
        stem = f'Find the equation of the ellipse with foci {P(c)} and length of the minor axis {2 * b}.'
        key = f'c = {c}, b = {b} (1); a² = b² + c² = {a * a} (1); {eq} (1).'
    return Q(stem, eq, key, [_ell_eq(b * b, a * a, major), _ell_eq(a * a, c2, major), _ell_eq(a * a + c2, b * b, major) if kind != 'lr' else _ell_eq(b * b + c2 + 1, b * b, major)])


def c10s3_e(r):
    a, b, c2 = _ell(r)
    c = math.isqrt(c2)
    return Q(f'An ellipse has semi-major axis {a} and semi-minor axis {b}. Find its eccentricity.', fs(Fr(c, a)), f'c = √(a² − b²) = {c}; e = c/a = {fs(Fr(c, a))}.',
             [fs(Fr(b, a)), fs(Fr(c, b)), fs(Fr(a, c))])


def c10s3_through(r):
    # x²/A + y²/B = 1 through two points with integer coords
    a2, b2 = r.choice([(16, 9), (25, 9), (25, 16), (36, 16), (100, 25), (52, 13), (40, 10), (20, 5), (45, 20), (18, 8)])
    pts_ = [(x, y) for x in range(0, 11) for y in range(0, 11) if Fr(x * x, a2) + Fr(y * y, b2) == 1]
    if len(pts_) < 2:
        raise ValueError
    P1, P2 = r.sample(pts_, 2)
    eq = _ell_eq(a2, b2)
    return Q(f'Find the equation of the ellipse, with centre at the origin and axes along the coordinate axes, which passes through {pt(*P1)} and {pt(*P2)}.', eq,
             f'Let x²/A + y²/B = 1 (1); substitute both points to get two linear equations in 1/A and 1/B (2); solve: A = {a2}, B = {b2} (1); {eq} (1).',
             [_ell_eq(b2, a2), _ell_eq(a2 + b2, b2), _ell_eq(a2, a2 - b2) if a2 - b2 > 0 else _ell_eq(a2 + 1, b2)])


def c10s3_rod(r):
    L = r.choice([10, 12, 15, 16, 20])
    p = r.choice([x for x in range(2, L - 1) if 2 * x != L])
    return Q(f'A rod of length {L} cm moves with its ends always on the x- and y-axes. Find the equation of the locus of the point P on the rod that is {p} cm from the end in contact with the x-axis.',
             f'x²/{(L - p) ** 2} + y²/{p * p} = 1',
             f'Let the rod make angle θ with the x-axis (1); then P = ({L - p} cos θ, {p} sin θ) (2); eliminate θ using cos²θ + sin²θ = 1 (1): x²/{(L - p) ** 2} + y²/{p * p} = 1, an ellipse (1).',
             [f'x²/{p * p} + y²/{(L - p) ** 2} = 1', f'x² + y² = {L * L}', f'x²/{L - p} + y²/{p} = 1'])


def c10s3_case(r):
    a, b, c2 = _ell(r)
    c = math.isqrt(c2)
    sc = r.choice([1, 2])
    A, B, C = a * sc, b * sc, c * sc
    city = r.choice(CITIES)
    return {'stem': f'An elliptical garden in {city} has a fountain at each focus. The garden is {2 * A} m long and {2 * B} m wide. Take the centre at the origin and the long axis along the x-axis.\n'
                    f'(i) Write the equation of the boundary. (ii) How far from the centre is each fountain? (iii) Find the eccentricity. '
                    f'(iv) A gardener walks along the boundary. What is the sum of their distances from the two fountains at every point?',
            'answer': f'(i) x²/{A * A} + y²/{B * B} = 1 (ii) {C} m (iii) {fs(Fr(C, A))} (iv) {2 * A} m',
            'key': '(i) a = half length, b = half width (1). (ii) c = √(a² − b²) (1). (iii) e = c/a (1). (iv) Sum of focal distances = 2a (1).'}


c10s3_tf = tf_mcq('ellipses',
                  ['For an ellipse, the sum of the distances of any point from the two foci is constant (= 2a).', 'For x²/a² + y²/b² = 1 with a > b, c² = a² − b².',
                   'The eccentricity of an ellipse is less than 1.', 'The length of the latus rectum of x²/a² + y²/b² = 1 (a > b) is 2b²/a.', 'A circle is an ellipse with e = 0.'],
                  ['For an ellipse, c² = a² + b².', 'The eccentricity of an ellipse is greater than 1.', 'For x²/9 + y²/25 = 1, the major axis is along the x-axis.',
                   'The latus rectum of an ellipse is 2a²/b.', 'For an ellipse, the difference of focal distances is constant.'])

c10s3_ar = pool_ar([
    ('The foci of x²/25 + y²/9 = 1 are (±4, 0).', 'c² = a² − b² = 25 − 9.', 'a', 'R explains A.'),
    ('x²/16 + y²/36 = 1 has its major axis along the y-axis.', 'The larger denominator is under y².', 'a', 'R explains A.'),
    ('The eccentricity of x²/25 + y²/16 = 1 is 5/3.', 'e = c/a for an ellipse.', 'd', 'A is false: e = 3/5; R is true.'),
])

c10s3_explain = pool_txt([
    ('Show that for an ellipse x²/a² + y²/b² = 1 (a > b), the length of the latus rectum is 2b²/a.', 'At x = c, y² = b²(1 − c²/a²) = b⁴/a², so y = ±b²/a; length 2b²/a.', '2 marks.'),
    ('Explain why the eccentricity of an ellipse lies between 0 and 1.', 'e = c/a with 0 ≤ c < a; e = 0 gives a circle, e close to 1 a flat ellipse.', '2 marks.'),
])

# st4 hyperbola

HYP = [(3, 4, 5), (4, 3, 5), (5, 12, 13), (12, 5, 13), (8, 6, 10), (6, 8, 10), (8, 15, 17), (15, 8, 17), (2, 1, None), (3, 2, None), (1, 1, None), (4, 2, None)]


def _hyp_eq(a2, b2, trans='x'):
    return f'x²/{fs(a2)} − y²/{fs(b2)} = 1' if trans == 'x' else f'y²/{fs(a2)} − x²/{fs(b2)} = 1'


def c10s4_param(r):
    a, b, c = r.choice(HYP)
    c2 = a * a + b * b
    trans = r.choice(['x', 'y'])
    cs = surd(c2)
    e = surd(Fr(c2, a * a))
    lr = fs(Fr(2 * b * b, a))
    P = (lambda v: f'(±{v}, 0)') if trans == 'x' else (lambda v: f'(0, ±{v})')
    return Q(f'For the hyperbola {_hyp_eq(a * a, b * b, trans)}, find the foci, the vertices, the eccentricity and the length of the latus rectum.',
             f'foci {P(cs)}; vertices {P(a)}; e = {e}; latus rectum {lr}',
             f'a² = {a * a}, b² = {b * b} (transverse axis along the {trans}-axis) (1); c = √(a² + b²) = {cs} (1); e = c/a = {e}; latus rectum 2b²/a = {lr} (1).',
             [f'foci {P(surd(abs(a * a - b * b)) if a != b else "0")}; vertices {P(a)}; e = {surd(Fr(abs(a * a - b * b), a * a)) if a != b else "0"}; latus rectum {lr}',
              f'foci {P(cs)}; vertices {P(b)}; e = {surd(Fr(c2, b * b))}; latus rectum {fs(Fr(2 * a * a, b))}', f'foci {P(a)}; vertices {P(cs)}; e = {e}; latus rectum {lr}'])


def c10s4_eq(r):
    a, b, c = r.choice([h for h in HYP if h[2]])
    trans = r.choice(['x', 'y'])
    kind = r.choice(['vf', 'fe', 'ft'])
    P = (lambda v: f'(±{v}, 0)') if trans == 'x' else (lambda v: f'(0, ±{v})')
    eq = _hyp_eq(a * a, b * b, trans)
    if kind == 'vf':
        stem, key = f'Find the equation of the hyperbola with vertices {P(a)} and foci {P(c)}.', f'a = {a}, c = {c} (1); b² = c² − a² = {b * b} (1); {eq} (1).'
    elif kind == 'fe':
        stem, key = f'Find the equation of the hyperbola with foci {P(c)} and eccentricity {fs(Fr(c, a))}.', f'c = {c}, a = c/e = {a} (1); b² = {b * b} (1); {eq} (1).'
    else:
        stem, key = f'Find the equation of the hyperbola with foci {P(c)} and length of the transverse axis {2 * a}.', f'c = {c}, a = {a} (1); b² = c² − a² = {b * b} (1); {eq} (1).'
    return Q(stem, eq, key, [_hyp_eq(b * b, a * a, trans), _hyp_eq(a * a, c * c, trans), _ell_eq(c * c, b * b, trans) if c * c > b * b else _hyp_eq(c * c, b * b, trans)])


def c10s4_e(r):
    a, b, c = r.choice([h for h in HYP if h[2]])
    return Q(f'A hyperbola has semi-transverse axis {a} and semi-conjugate axis {b}. Find its eccentricity.', fs(Fr(c, a)), f'c = √(a² + b²) = {c}; e = c/a = {fs(Fr(c, a))}.',
             [fs(Fr(b, a)), fs(Fr(a, c)), fs(Fr(c, b)) if Fr(c, b) != Fr(c, a) else fs(Fr(c, a) + 1)])


def _hyp_pts():
    out = []
    for a2 in (1, 4, 9, 16, 25, 36, 49, 64, 5, 8, 12, 20):
        for b2 in (1, 4, 9, 16, 25, 36, 5, 12, 20, 45):
            c2 = a2 + b2
            if math.isqrt(c2) ** 2 != c2:
                continue
            ps = [(x, y) for x in range(1, 13) for y in range(1, 13) if Fr(x * x, a2) - Fr(y * y, b2) == 1]
            for p in ps:
                out.append((a2, b2, math.isqrt(c2), p))
    return out


HYP_PTS = _hyp_pts()


def c10s4_through(r):
    a2, b2, c, (x0, y0) = r.choice(HYP_PTS)
    eq = _hyp_eq(a2, b2)
    return Q(f'Find the equation of the hyperbola with foci (±{c}, 0) passing through {pt(x0, y0)}.', eq,
             f'x²/a² − y²/b² = 1 with a² + b² = {c * c} (1); substitute {pt(x0, y0)}: {x0 * x0}/a² − {y0 * y0}/({c * c} − a²) = 1 (2); solve for a² (reject the root greater than {c * c}): a² = {a2}, b² = {b2} (1); {eq} (1).',
             [_hyp_eq(b2, a2), f'x²/{a2} + y²/{b2} = 1', _hyp_eq(a2, c * c)])


c10s4_compare = term_mcq([('x²/a² + y²/b² = 1 (a > b)', 'an ellipse with foci on the x-axis and c² = a² − b²'), ('x²/a² − y²/b² = 1', 'a hyperbola with foci on the x-axis and c² = a² + b²'),
                          ('y² = 4ax', 'a parabola with focus (a, 0)'), ('x² + y² = a²', 'a circle with centre at the origin'), ('y²/a² − x²/b² = 1', 'a hyperbola with foci on the y-axis')],
                         'The equation {a} represents', 'Which equation represents {b}?', '{a}: {b}.')


def c10s4_case(r):
    a, b, c = r.choice([h for h in HYP if h[2]])
    k = r.choice([1, 2, 10])
    A, C = a * k, c * k
    return {'stem': f'Two radio stations S₁ and S₂ on a straight coast are {2 * C} km apart. A ship receives their signals and finds that it is always {2 * A} km farther from S₁ than from S₂. '
                    f'Take the midpoint of S₁S₂ as the origin and the coast as the x-axis.\n(i) Name the curve on which the ship lies. (ii) Find a, c and b². (iii) Write the equation of the curve. (iv) Find its eccentricity.',
            'answer': f'(i) a branch of a hyperbola with foci S₁, S₂ (ii) a = {A}, c = {C}, b² = {C * C - A * A} (iii) x²/{A * A} − y²/{C * C - A * A} = 1 (iv) {fs(Fr(C, A))}',
            'key': '(i) Constant difference of distances from two fixed points (1). (ii) 2a = difference, 2c = distance between foci, b² = c² − a² (1). (iii) Standard form (1). (iv) e = c/a (1).'}


c10s4_tf = tf_mcq('hyperbolas',
                  ['For a hyperbola, the difference of the distances of any point from the foci is constant (= 2a).', 'For x²/a² − y²/b² = 1, c² = a² + b².',
                   'The eccentricity of a hyperbola is greater than 1.', 'The latus rectum of x²/a² − y²/b² = 1 has length 2b²/a.', 'For x² − y² = a², the eccentricity is √2.'],
                  ['For a hyperbola, c² = a² − b².', 'The eccentricity of a hyperbola is less than 1.', 'For a hyperbola, the sum of the focal distances is constant.',
                   'y²/9 − x²/16 = 1 has its foci on the x-axis.', 'The hyperbola x²/9 − y²/16 = 1 has vertices (0, ±3).'])

c10s4_ar = pool_ar([
    ('The foci of x²/9 − y²/16 = 1 are (±5, 0).', 'For a hyperbola c² = a² + b².', 'a', 'R explains A.'),
    ('The eccentricity of a rectangular hyperbola x² − y² = a² is √2.', 'Here b = a, so c = a√2.', 'a', 'R explains A.'),
    ('The hyperbola y²/16 − x²/9 = 1 has vertices (±4, 0).', 'The transverse axis is along the axis of the positive term.', 'd', 'A is false: vertices (0, ±4); R is true.'),
])

c10s4_explain = pool_txt([
    ('Distinguish between an ellipse and a hyperbola using the focal-distance property and the eccentricity.', 'Ellipse: sum of focal distances 2a, e < 1. Hyperbola: difference 2a, e > 1.', '2 marks.'),
    ('Explain how to tell from the equation along which axis the transverse axis of a hyperbola lies.', 'It lies along the axis of the variable whose square has the positive coefficient.', '2 marks.'),
])


# ======================================================== extra families (D4 coverage)

def c7s1_ratio(r):
    for _ in range(60):
        n = r.randint(6, 60)
        k = r.randint(2, n - 2)
        a, b, c = comb(n, k - 1), comb(n, k), comb(n, k + 1)
        g_ = math.gcd(math.gcd(a, b), c)
        ra = (a // g_, b // g_, c // g_)
        if max(ra) <= 200:
            sols = [(m, j) for m in range(3, 120) for j in range(1, m - 1)
                    if comb(m, j - 1) * ra[1] == comb(m, j) * ra[0] and comb(m, j) * ra[2] == comb(m, j + 1) * ra[1]]
            if sols == [(n, k)]:
                break
    else:
        raise ValueError
    return Q(f'The coefficients of three consecutive terms in the expansion of (1 + a)ⁿ are in the ratio {ra[0]} : {ra[1]} : {ra[2]}. Find n.', f'n = {n}',
             f'Let the terms be nCr−1, nCr, nCr+1 (1); nCr−1/nCr = r/(n − r + 1) = {ra[0]}/{ra[1]} (1) and nCr/nCr+1 = (r + 1)/(n − r) = {ra[1]}/{ra[2]} (1); '
             f'solve the two linear equations: r = {k}, n = {n} (1).',
             [f'n = {n + 1}', f'n = {n - 1}', f'n = {ra[0] + ra[1] + ra[2]}'])


def c8s1_series(r):
    n = r.randint(8, 25)
    kind = r.choice(['kk1', 'sq', 'cube', 'odd2'])
    if kind == 'kk1':
        v = n * (n + 1) * (n + 2) // 3
        return Q(f'Find the sum to {n} terms of the series 1 × 2 + 2 × 3 + 3 × 4 + …', f'{ind(v)}',
                 f'kth term = k(k + 1) = k² + k (1); Σk² + Σk = n(n + 1)(2n + 1)/6 + n(n + 1)/2 (2) = n(n + 1)(n + 2)/3 = {ind(v)} (1).',
                 [f'{ind(n * (n + 1) * (2 * n + 1) // 6)}', f'{ind((n * (n + 1) // 2) ** 2)}', f'{ind(n * (n + 1) * (n + 2) // 6)}'])
    if kind == 'sq':
        v = n * (n + 1) * (2 * n + 1) // 6
        return Q(f'Find the sum 1² + 2² + 3² + … + {n}².', f'{ind(v)}', f'Σk² = n(n + 1)(2n + 1)/6 with n = {n} (2): {ind(v)} (2).',
                 [f'{ind((n * (n + 1) // 2) ** 2)}', f'{ind(n * (n + 1) // 2)}', f'{ind(n * n * (n + 1) // 2)}'])
    if kind == 'cube':
        v = (n * (n + 1) // 2) ** 2
        return Q(f'Find the sum 1³ + 2³ + 3³ + … + {n}³.', f'{ind(v)}', f'Σk³ = [n(n + 1)/2]² with n = {n} (2): {ind(v)} (2).',
                 [f'{ind(n * (n + 1) * (2 * n + 1) // 6)}', f'{ind(n * (n + 1) // 2)}', f'{ind(n ** 3)}'])
    v = n * (2 * n - 1) * (2 * n + 1) // 3
    return Q(f'Find the sum to {n} terms of the series 1² + 3² + 5² + …', f'{ind(v)}',
             f'kth term = (2k − 1)² = 4k² − 4k + 1 (1); sum = 4Σk² − 4Σk + n (2) = n(2n − 1)(2n + 1)/3 = {ind(v)} (1).',
             [f'{ind(n * (n + 1) * (2 * n + 1) // 6)}', f'{ind(4 * n * (n + 1) * (2 * n + 1) // 6)}', f'{ind(n * n)}'])


# ======================================================== families

FAMILIES = {
    S + '06-st1': [F('C1', 'D2', 'mcq', c6s1_tf), F('C2', 'D2', 'explain', c6s1_explain), F('C2', 'D3', 'mcq', c6s1_ar, kinds=('ar',)), F('C3', 'D1', 'short', c6s1_outfit),
                   F('C2', 'D1', 'mcq', c6s1_letters), F('C3', 'D2', 'numerical', c6s1_code), F('C3', 'D3', 'numerical', c6s1_even), F('C4', 'D3', 'multi_step', c6s1_route),
                   F('C4', 'D4', 'multi_step', c6s1_signal), F('C3', 'D3', 'case', c6s1_case)],
    S + '06-st2': [F('C1', 'D1', 'mcq', c6s2_terms), F('C1', 'D2', 'mcq', c6s2_tf), F('C2', 'D2', 'explain', c6s2_explain), F('C2', 'D3', 'mcq', c6s2_ar, kinds=('ar',)),
                   F('C3', 'D1', 'short', c6s2_fact), F('C3', 'D1', 'mcq', c6s2_npr), F('C3', 'D2', 'numerical', c6s2_words), F('C3', 'D3', 'numerical', c6s2_x),
                   F('C4', 'D3', 'numerical', c6s2_solve), F('C4', 'D4', 'multi_step', c6s2_r)],
    S + '06-st3': [F('C1', 'D2', 'mcq', c6s3_tf), F('C2', 'D2', 'explain', c6s3_explain), F('C2', 'D3', 'mcq', c6s3_ar, kinds=('ar',)), F('C3', 'D1', 'short', c6s3_digits),
                   F('C3', 'D2', 'numerical', c6s3_word), F('C3', 'D3', 'numerical', c6s3_start), F('C4', 'D4', 'multi_step', c6s3_vowels), F('C3', 'D3', 'case', c6s3_case)],
    S + '06-st4': [F('C1', 'D1', 'mcq', c6s4_terms), F('C1', 'D2', 'mcq', c6s4_tf), F('C2', 'D2', 'explain', c6s4_explain), F('C2', 'D3', 'mcq', c6s4_ar, kinds=('ar',)),
                   F('C3', 'D1', 'short', c6s4_val), F('C3', 'D2', 'mcq', c6s4_pascal), F('C3', 'D2', 'numerical', c6s4_comm), F('C3', 'D3', 'numerical', c6s4_eq),
                   F('C4', 'D3', 'numerical', c6s4_geom), F('C4', 'D4', 'multi_step', c6s4_atleast)],
    S + '06-st5': [F('C1', 'D1', 'mcq', c6s5_kind), F('C1', 'D2', 'mcq', c6s5_tf), F('C2', 'D2', 'explain', c6s5_explain), F('C2', 'D3', 'mcq', c6s5_ar, kinds=('ar',)),
                   F('C3', 'D2', 'mcq', c6s5_order), F('C3', 'D3', 'numerical', c6s5_cards), F('C4', 'D4', 'long', c6s5_words), F('C4', 'D5', 'long', c6s5_team),
                   F('C3', 'D3', 'case', c6s5_case)],
    S + '07-st1': [F('C1', 'D1', 'mcq', c7s1_terms), F('C1', 'D2', 'mcq', c7s1_tf), F('C2', 'D2', 'explain', c7s1_explain), F('C2', 'D3', 'mcq', c7s1_ar, kinds=('ar',)),
                   F('C3', 'D1', 'short', c7s1_row), F('C3', 'D2', 'mcq', c7s1_coef), F('C3', 'D2', 'numerical', c7s1_sum), F('C4', 'D3', 'numerical', c7s1_terms_count)],
    S + '07-st2': [F('C1', 'D1', 'mcq', c7s2_nterms), F('C1', 'D2', 'mcq', c7s2_tf), F('C2', 'D2', 'explain', c7s2_explain), F('C2', 'D3', 'mcq', c7s2_ar, kinds=('ar',)),
                   F('C2', 'D4', 'long', c7s2_long), F('C3', 'D2', 'short', c7s2_expand), F('C3', 'D2', 'numerical', c7s2_term), F('C3', 'D3', 'numerical', c7s2_coef),
                   F('C4', 'D4', 'multi_step', c7s2_indep), F('C4', 'D3', 'multi_step', c7s2_middle)],
    S + '07-st3': [F('C1', 'D2', 'mcq', c7s3_tf), F('C2', 'D2', 'explain', c7s3_explain), F('C2', 'D3', 'mcq', c7s3_ar, kinds=('ar',)), F('C3', 'D1', 'short', c7s3_eval),
                   F('C3', 'D3', 'numerical', c7s3_approx), F('C3', 'D2', 'numerical', c7s3_rem), F('C4', 'D3', 'mcq', c7s3_compare), F('C4', 'D5', 'long', c7s3_divis),
                   F('C3', 'D3', 'case', c7s3_case)],
    S + '08-st1': [F('C1', 'D1', 'mcq', c8s1_terms), F('C1', 'D2', 'mcq', c8s1_tf), F('C2', 'D2', 'explain', c8s1_explain), F('C2', 'D3', 'mcq', c8s1_ar, kinds=('ar',)),
                   F('C3', 'D1', 'short', c8s1_first), F('C3', 'D2', 'short', c8s1_nth), F('C3', 'D2', 'numerical', c8s1_recur), F('C3', 'D3', 'mcq', c8s1_sigma),
                   F('C4', 'D3', 'numerical', c8s1_which)],
    S + '08-st2': [F('C1', 'D2', 'mcq', c8s2_tf), F('C2', 'D2', 'explain', c8s2_explain), F('C2', 'D3', 'mcq', c8s2_ar, kinds=('ar',)), F('C3', 'D1', 'short', c8s2_am),
                   F('C3', 'D2', 'numerical', c8s2_sum), F('C3', 'D3', 'numerical', c8s2_insert), F('C4', 'D4', 'long', c8s2_sn), F('C4', 'D3', 'multi_step', c8s2_salary),
                   F('C3', 'D3', 'case', c8s2_case)],
    S + '08-st3': [F('C1', 'D2', 'mcq', c8s3_tf), F('C2', 'D2', 'explain', c8s3_explain), F('C2', 'D3', 'mcq', c8s3_ar, kinds=('ar',)), F('C3', 'D1', 'short', c8s3_nth),
                   F('C3', 'D2', 'numerical', c8s3_sum), F('C3', 'D3', 'numerical', c8s3_which), F('C4', 'D4', 'long', c8s3_find), F('C4', 'D3', 'numerical', c8s3_growth),
                   F('C3', 'D3', 'case', c8s3_case)],
    S + '08-st4': [F('C1', 'D2', 'mcq', c8s4_tf), F('C2', 'D2', 'explain', c8s4_explain), F('C2', 'D3', 'mcq', c8s4_ar, kinds=('ar',)), F('C3', 'D1', 'short', c8s4_gm),
                   F('C3', 'D3', 'numerical', c8s4_insert), F('C4', 'D4', 'multi_step', c8s4_ab), F('C4', 'D3', 'mcq', c8s4_min), F('C4', 'D5', 'long', c8s4_ratio),
                   F('C3', 'D3', 'case', _c8s4_case)],
    S + '09-st1': [F('C1', 'D1', 'mcq', c9s1_incl), F('C1', 'D2', 'mcq', c9s1_tf), F('C2', 'D2', 'explain', c9s1_explain), F('C2', 'D3', 'mcq', c9s1_ar, kinds=('ar',)),
                   F('C3', 'D1', 'short', c9s1_slope), F('C3', 'D2', 'mcq', c9s1_parperp), F('C3', 'D2', 'numerical', c9s1_collinear), F('C3', 'D3', 'numerical', c9s1_angle),
                   F('C4', 'D4', 'multi_step', c9s1_perpk)],
    S + '09-st2': [F('C1', 'D2', 'mcq', c9s2_tf), F('C2', 'D2', 'explain', c9s2_explain), F('C2', 'D3', 'mcq', c9s2_ar, kinds=('ar',)), F('C3', 'D1', 'short', c9s2_point),
                   F('C3', 'D2', 'short', c9s2_two), F('C3', 'D2', 'numerical', c9s2_int), F('C4', 'D3', 'numerical', c9s2_mid), F('C4', 'D4', 'long', c9s2_median),
                   F('C3', 'D3', 'case', c9s2_case)],
    S + '09-st3': [F('C1', 'D2', 'mcq', c9s3_tf), F('C2', 'D2', 'explain', c9s3_explain), F('C2', 'D3', 'mcq', c9s3_ar, kinds=('ar',)), F('C3', 'D1', 'short', c9s3_slope),
                   F('C3', 'D2', 'numerical', c9s3_intersect), F('C3', 'D3', 'numerical', c9s3_normal), F('C4', 'D3', 'numerical', c9s3_through), F('C4', 'D4', 'multi_step', c9s3_concur)],
    S + '09-st4': [F('C1', 'D1', 'mcq', c9s4_formula), F('C1', 'D2', 'mcq', c9s4_tf), F('C2', 'D2', 'explain', c9s4_explain), F('C2', 'D3', 'mcq', c9s4_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c9s4_dist), F('C3', 'D3', 'numerical', c9s4_par), F('C4', 'D4', 'multi_step', c9s4_foot), F('C4', 'D3', 'numerical', c9s4_onaxis),
                   F('C3', 'D3', 'case', c9s4_case)],
    S + '10-st1': [F('C1', 'D1', 'mcq', c10s1_sections), F('C1', 'D2', 'mcq', c10s1_tf), F('C2', 'D2', 'explain', c10s1_explain), F('C2', 'D3', 'mcq', c10s1_ar, kinds=('ar',)),
                   F('C3', 'D1', 'short', c10s1_eq), F('C3', 'D2', 'numerical', c10s1_cr), F('C3', 'D3', 'numerical', c10s1_diam), F('C4', 'D3', 'mcq', c10s1_inside),
                   F('C4', 'D4', 'long', c10s1_three)],
    S + '10-st2': [F('C1', 'D2', 'mcq', c10s2_tf), F('C2', 'D2', 'explain', c10s2_explain), F('C2', 'D3', 'mcq', c10s2_ar, kinds=('ar',)), F('C3', 'D1', 'short', c10s2_focus),
                   F('C3', 'D2', 'short', c10s2_lr), F('C3', 'D3', 'numerical', c10s2_eq), F('C4', 'D3', 'numerical', c10s2_through), F('C4', 'D5', 'long', c10s2_tri),
                   F('C3', 'D3', 'case', c10s2_case)],
    S + '10-st3': [F('C1', 'D2', 'mcq', c10s3_tf), F('C2', 'D2', 'explain', c10s3_explain), F('C2', 'D3', 'mcq', c10s3_ar, kinds=('ar',)), F('C3', 'D1', 'short', c10s3_e),
                   F('C3', 'D2', 'numerical', c10s3_param), F('C3', 'D3', 'numerical', c10s3_eq), F('C4', 'D4', 'long', c10s3_through), F('C4', 'D5', 'long', c10s3_rod),
                   F('C3', 'D3', 'case', c10s3_case)],
    S + '10-st4': [F('C1', 'D1', 'mcq', c10s4_compare), F('C1', 'D2', 'mcq', c10s4_tf), F('C2', 'D2', 'explain', c10s4_explain), F('C2', 'D3', 'mcq', c10s4_ar, kinds=('ar',)),
                   F('C3', 'D1', 'short', c10s4_e), F('C3', 'D2', 'numerical', c10s4_param), F('C3', 'D3', 'numerical', c10s4_eq), F('C4', 'D4', 'long', c10s4_through),
                   F('C3', 'D3', 'case', c10s4_case)],
}

FAMILIES[S + '07-st1'].append(F('C4', 'D4', 'multi_step', c7s1_ratio))
FAMILIES[S + '08-st1'].append(F('C4', 'D4', 'multi_step', c8s1_series))

FAMILIES = polish(mpolish(FAMILIES))
