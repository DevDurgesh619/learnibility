"""Cambridge Lower Secondary Mathematics 0862, Stage 9 (CUP Learner's Book 9, 2nd ed.).

Checkpoint style (Paper 1 non-calculator, Paper 2 calculator): command words Work out, Calculate,
Show that, Explain, Write down, Tick, Give a reason. Marking keys use M (method), A (accuracy)
and B (independent) marks; multi-part items carry part marks as a trailing [n].
"""
import math
import unicodedata
from fractions import Fraction as Fr
from ._lib import topic, mcq, compose, sf, sup, person, two_people, city

PROFILE = {'mark_scale': {'long': (1.5, 1.5), 'case': (1.2, 1.2)}}
CHAPTERS = {}
MINUS = '−'


# ------------------------------------------------------------------ helpers
def N(x, dp=6):
    """Format a number: unicode minus, no trailing zeros, Fractions as a/b."""
    if isinstance(x, Fr):
        return fr(x)
    if isinstance(x, float) and abs(x - round(x)) < 1e-9:
        x = int(round(x))
    if isinstance(x, int):
        s = f'{abs(x):,}' if abs(x) >= 10000 else str(abs(x))
    else:
        s = f'{abs(x):.{dp}f}'.rstrip('0').rstrip('.')
        if s == '0':
            return '0'
    return (MINUS if x < 0 else '') + s


def fr(x):
    x = Fr(x)
    if x.denominator == 1:
        return N(int(x))
    return (MINUS if x < 0 else '') + f'{abs(x.numerator)}/{x.denominator}'


def mixed(x):
    x = Fr(x)
    if x.denominator == 1 or abs(x) < 1:
        return fr(x)
    w = int(abs(x)) * (1 if x > 0 else -1)
    rem = abs(x - w)
    return f'{N(w)} {rem.numerator}/{rem.denominator}'


def money(x, cur='$'):
    return f'{cur}{x:,.2f}'


def d2(x):
    return f'{x:.2f}'


def poly(*terms):
    """poly((3, 'x'), (-5, '')) -> '3x − 5'."""
    out = ''
    for c, v in terms:
        if c == 0:
            continue
        a = abs(c)
        body = (N(a) if (a != 1 or not v) else '') + v
        if not out:
            out = (MINUS if c < 0 else '') + body
        else:
            out += (f' {MINUS} ' if c < 0 else ' + ') + body
    return out or '0'


def lin(a, b, v='x'):
    return poly((a, v), (b, ''))


def par(x):
    """Wrap negatives in brackets for substitution lines."""
    s = N(x)
    return f'({s})' if s.startswith(MINUS) else s


def _k(s):
    return ' '.join(unicodedata.normalize('NFKC', str(s)).lower().split())


def mc(r, ans, cands):
    """4-option MCQ with options distinct after NFKC/case folding (matches the validator)."""
    seen = {_k(ans)}
    ds = []
    for c in cands:
        if c is None:
            continue
        kc = _k(c)
        if kc not in seen:
            seen.add(kc)
            ds.append(str(c))
    if len(ds) < 3:
        raise ValueError('not enough distractors')
    return mcq(r, ans, ds)


def Q(stem, answer, key, options=None, **kw):
    q = {'stem': stem, 'answer': answer, 'key': key}
    if options:
        q['options'] = options
    q.update({k: v for k, v in kw.items() if v is not None})
    return q


def MCQ(r, stem, ans, cands, key, **kw):
    try:
        opts, a = mc(r, ans, cands)
    except ValueError:
        return None
    return Q(stem, a, key, opts, **kw)


def nonsq(r, lo, hi):
    for _ in range(200):
        n = r.randint(lo, hi)
        if math.isqrt(n) ** 2 != n:
            return n
    return lo + 1


def icbrt(n):
    a = int(round(n ** (1 / 3)))
    while a ** 3 > n:
        a -= 1
    while (a + 1) ** 3 <= n:
        a += 1
    return a


def r1(x, dp=1):
    """Round half up (avoids banker's rounding in keys)."""
    from decimal import Decimal, ROUND_HALF_UP
    q = Decimal(1).scaleb(-dp)
    return float(Decimal(repr(x)).quantize(q, rounding=ROUND_HALF_UP))


def fdp(x, dp):
    return f'{r1(x, dp):.{dp}f}'


def sform(m, e):
    """Standard form string from mantissa m (1 <= m < 10) and exponent e."""
    return f'{N(m)} × 10{sup(e)}'


def to_sform(x, sig=6):
    if x == 0:
        return '0'
    e = int(math.floor(math.log10(abs(x))))
    m = round(x / 10 ** e, sig)
    if abs(m) >= 10:
        m = round(m / 10, sig)
        e += 1
    return sform(m, e)


def lead(r, opts):
    return r.choice(opts)


TICK = ['Tick (✓) the correct answer.', 'Choose the correct answer.', 'Select one answer.']


def art(w):
    return ('an ' if w[0].lower() in 'aeiou' else 'a ') + w


# =========================================================== 1 Number and calculation
t11 = topic('Irrational numbers and surds', 'irrational numbers', 'surds', 'approximate values')
t11.fixed('C1', (1, 2, 3), [
    ('Which of these numbers is irrational? 22/7, 3.14, √9, π', 'π', 'π cannot be written as a fraction of two integers; its decimal never ends and never repeats. 22/7 and 3.14 are rational approximations; √9 = 3. [1]', ['22/7', '3.14', '√9']),
    ('What can you say about the decimal expansion of an irrational number?', 'It never terminates and never repeats', 'An irrational number cannot be written as a/b with a, b integers, so its decimal expansion neither terminates nor recurs. [1]',
     ['It always terminates', 'It always recurs', 'It terminates after many digits']),
    ('Which of these is a surd? √16, √12, ∛27, √0.25', '√12', '12 is not a square number, so √12 is irrational (a surd). √16 = 4, ∛27 = 3, √0.25 = 0.5. [1]', ['√16', '∛27', '√0.25']),
    ('Write down the value of ∛64.', '4', '4 × 4 × 4 = 64. B1 [1]'),
    ('Write down a whole number n so that √n is a rational number between 6 and 8.', '49', '√49 = 7 is the only whole number root strictly between 6 and 8. B1 [1]'),
    ('Which of these is rational? √2, √(4/9), √(2/9), π/2', '√(4/9)', '√(4/9) = 2/3, a fraction. The others are irrational. [1]', ['√2', '√(2/9)', 'π/2']),
    ('Is 0.121121112... (the number of 1s keeps increasing) rational or irrational? Give a reason.', 'Irrational: the decimal never ends and has no repeating block.', 'B1 irrational with reason: no recurring block of digits. [1]'),
    ('Write down the value of (√7)².', '7', 'Squaring undoes the square root: (√7)² = 7. B1 [1]'),
])
t11.fixed('C2', (2, 3), [
    ('Explain why √50 is not a whole number.', '7² = 49 and 8² = 64, so √50 lies between 7 and 8 and cannot be a whole number.', 'M1 compares with 49 and 64; A1 conclusion between 7 and 8. [2]'),
    ('Explain why every recurring decimal is a rational number.', 'A recurring decimal can always be written as a fraction a/b (e.g. 0.333... = 1/3), and any number that can be written as a fraction of integers is rational.', 'B1 can be written as a fraction; B1 link to definition of rational. [2]'),
    ('Show that √2 × √18 is a rational number.', '√2 × √18 = √36 = 6, which is an integer and therefore rational.', 'M1 √(2 × 18) = √36; A1 = 6, rational. [2]'),
    ('Explain why ∛30 is between 3 and 4.', '3³ = 27 and 4³ = 64; 30 is between 27 and 64, so ∛30 is between 3 and 4.', 'M1 cubes 27 and 64; A1 conclusion. [2]'),
    ('A student says "π = 22/7 exactly, so π is rational." Explain the mistake.', '22/7 = 3.142857... is only an approximation to π = 3.141592...; π cannot be written exactly as a fraction, so it is irrational.', 'B1 22/7 is an approximation (values differ); B1 π cannot be written as a fraction. [2]'),
])


@t11.add('C1', (1, 2, 3))
def t11_pick(r, D):
    n = nonsq(r, 2, [0, 30, 80, 200][D])
    k = r.randint(2, 15)
    rats = [f'√{k * k}', f'∛{r.choice([8, 27, 64, 125, 216])}', f'{r.randint(1, 9)}/{r.choice([3, 7, 11, 13])}',
            f'0.{r.randint(10, 99)}', f'√{r.choice(["0.25", "0.04", "0.81", "1.44", "0.09"])}', f'{r.randint(2, 9)}.{r.randint(1, 9)}']
    ch = r.sample(rats, 3) + [f'√{n}']
    r.shuffle(ch)
    stem = r.choice(['Here are four numbers: {}. Which one is irrational?', 'Which of these numbers is irrational? {}',
                     'Only one of these numbers is irrational: {}. Which one?']).format(', '.join(ch))
    return MCQ(r, stem, f'√{n}', [c for c in ch if c != f'√{n}'] + rats,
               f'{n} is not a square number, so √{n} cannot be written as a fraction; the others are integers, fractions or terminating decimals. [1]')


@t11.add('C1', (1, 2, 3))
def t11_between(r, D):
    if D <= 2:
        n = nonsq(r, 5, 50 if D == 1 else 160)
        a = math.isqrt(n)
        s = f'√{n}'
        why = f'{a}² = {a * a} and {a + 1}² = {(a + 1) ** 2}'
    else:
        while True:
            n = r.randint(10, 900)
            a = icbrt(n)
            if a ** 3 != n:
                break
        s = f'∛{n}'
        why = f'{a}³ = {a ** 3} and {a + 1}³ = {(a + 1) ** 3}'
    stem = r.choice([f'{s} lies between two consecutive whole numbers. Which two?', f'Between which two consecutive integers does {s} lie?'])
    return MCQ(r, stem, f'{a} and {a + 1}', [f'{a - 1} and {a}', f'{a + 1} and {a + 2}', f'{n // 2} and {n // 2 + 1}', f'{n // 3} and {n // 3 + 1}'],
               f'{why}, and {n} lies between these. [1]')


@t11.add('C2', (1, 2, 3, 4), 'explain')
def t11_product(r, D):
    a, b = r.choice([(2, 8), (2, 18), (3, 12), (3, 27), (5, 20), (2, 32), (6, 24), (5, 45), (7, 28), (2, 50), (3, 48), (10, 40), (6, 54), (7, 63), (11, 44)])
    p = person(r)
    root = math.isqrt(a * b)
    if D <= 2 or r.random() < 0.5:
        stem = f'{p} says: "√{a} and √{b} are both irrational, so √{a} × √{b} must also be irrational." Show that {p} is wrong.'
    else:
        stem = f'{p} says: "If you multiply two surds the answer is always a surd." Use √{a} and √{b} to show that this statement is false.'
    return Q(stem, f'√{a} × √{b} = √{a * b} = {root}, which is rational, so the product of two surds need not be irrational.',
             f'M1 √{a} × √{b} = √{a * b}; A1 = {root}, rational, so the claim is false. [2]')


@t11.add('C2', (1, 2, 3, 4), 'explain')
def t11_closer(r, D):
    n = nonsq(r, 10, [0, 60, 150, 400, 900][D])
    a = math.isqrt(n)
    mid = a * a + a + 0.25
    near = a + 1 if n > mid else a
    stem = r.choice([f'Without using a calculator, decide whether √{n} is closer to {a} or to {a + 1}. Explain how you decided.',
                     f'Is √{n} nearer to {a} or to {a + 1}? Give a reason without using a calculator.'])
    return Q(stem, f'Closer to {near}. ({a}.5)² = {N(mid)} and {n} is {"more" if n > mid else "less"} than {N(mid)}.',
             f'M1 uses ({a}.5)² = {N(mid)} (or compares {a}² = {a * a} and {a + 1}² = {(a + 1) ** 2} with care); A1 {near} with correct reason. [2]')


@t11.add('C2', (1, 2, 3, 4), 'explain')
def t11_recurring_claim(r, D):
    f, dec = r.choice([('1/7', '0.142857142857...'), ('2/3', '0.666...'), ('5/11', '0.454545...'), ('4/9', '0.444...'), ('1/6', '0.1666...'),
                       ('7/12', '0.58333...'), ('3/7', '0.428571428571...'), ('8/11', '0.727272...'), ('5/6', '0.8333...'), ('2/9', '0.222...')])
    p = person(r)
    stem = r.choice([f'{p} says: "{f} is irrational because its decimal, {dec}, goes on for ever." Explain why {p} is wrong.',
                     f'{p} works out {f} = {dec} and decides that {f} is irrational. Is {p} correct? Give a reason.'])
    return Q(stem, f'No. {f} is a fraction of two integers, so it is rational. Its decimal recurs (repeats); irrational numbers never terminate AND never repeat.',
             'B1 it can be written as a fraction so it is rational; B1 recurring decimals are rational / irrational decimals do not repeat. [2]')


@t11.add('C2', (2, 3, 4), 'explain')
def t11_add_err(r, D):
    a, b = r.sample(range(2, 13), 2)
    p = person(r)
    s = a * a + b * b
    rs = f'√{s}' if math.isqrt(s) ** 2 != s else str(math.isqrt(s))
    return Q(f'{p} writes: √{a * a} + √{b * b} = √({a * a} + {b * b}) = {rs}. Explain the mistake and give the correct value.',
             f'Square roots cannot be added like this. √{a * a} + √{b * b} = {a} + {b} = {a + b}, but √{s} {"is irrational" if rs.startswith("√") else "= " + rs}, which is not {a + b}.',
             f'B1 √(x + y) ≠ √x + √y; B1 correct value {a + b}. [2]')


@t11.add('C3', (1, 2, 3, 4, 5))
def t11_estimate(r, D):
    if D <= 3:
        n = nonsq(r, 8, [0, 50, 120, 400][D])
        x = math.sqrt(n)
        a = math.isqrt(n)
        ans = fdp(x, 1)
        lo = float(ans) - 0.05
        stem = r.choice([f'Without a calculator, estimate √{n} to one decimal place. Show your working.',
                         f'Estimate the value of √{n}, correct to 1 decimal place, without using a calculator.',
                         f'A square has an area of {n} cm². Estimate its side length to one decimal place without a calculator.'])
        key = f'{a}² = {a * a}, {a + 1}² = {(a + 1) ** 2} so {a} < √{n} < {a + 1} (M1); trial: {fdp(lo, 2)}² = {fdp(lo * lo, 4)} and {fdp(lo + 0.1, 2)}² = {fdp((lo + 0.1) ** 2, 4)} (M1); √{n} ≈ {ans} (A1).'
        if D == 1:
            return MCQ(r, stem.replace('Show your working.', 'Choose the best estimate.'), ans, [fdp(x + 0.1, 1), fdp(x - 0.1, 1), N(n / 2), fdp(x + 1, 1), N(a)], key)
        return Q(stem, ans + (' cm' if 'cm²' in stem else ''), key)
    if D == 4:
        while True:
            n = r.randint(20, 700)
            if icbrt(n) ** 3 != n:
                break
        x = n ** (1 / 3)
        a = icbrt(n)
        return Q(f'Use trial and improvement to find ∛{n} correct to 1 decimal place. Show your trials.', fdp(x, 1),
                 f'{a}³ = {a ** 3}, {a + 1}³ = {(a + 1) ** 3} (M1); trials e.g. {fdp(x, 1)}³ = {fdp(r1(x, 1) ** 3, 3)}; check {fdp(r1(x, 1) - 0.05, 2)}³ = {fdp((r1(x, 1) - 0.05) ** 3, 3)} and {fdp(r1(x, 1) + 0.05, 2)}³ = {fdp((r1(x, 1) + 0.05) ** 3, 3)} lie either side of {n} (M1); ∛{n} ≈ {fdp(x, 1)} (A1).')
    a = nonsq(r, 10, 99)
    b = r.choice([8, 27, 64, 125, 20, 40, 50, 90, 100])
    v = math.sqrt(a) + b ** (1 / 3)
    return Q(f'Use a calculator to work out √{a} + ∛{b}. Give your answer correct to 2 decimal places.', fdp(v, 2),
             f'√{a} = {fdp(math.sqrt(a), 4)}..., ∛{b} = {fdp(b ** (1 / 3), 4)}... (M1); sum = {fdp(v, 4)}... = {fdp(v, 2)} (A1).')


@t11.add('C3', (1, 2, 3, 4))
def t11_simplify(r, D):
    kind = r.choice(['sq', 'prod', 'quot', 'mix'] if D >= 2 else ['sq', 'prod'])
    if kind == 'sq':
        n, k = nonsq(r, 2, 30), r.randint(2, 9)
        return Q(f'Work out the value of {k} × (√{n})².', str(k * n), f'(√{n})² = {n} (M1); {k} × {n} = {k * n} (A1).')
    if kind == 'prod':
        a, b = r.choice([(2, 8), (3, 12), (5, 20), (2, 18), (3, 27), (6, 24), (2, 32), (5, 45), (7, 28)])
        k = r.randint(2, 6)
        return Q(f'Work out {k}√{a} × √{b}. Give your answer as a whole number.', str(k * math.isqrt(a * b)), f'√{a} × √{b} = √{a * b} = {math.isqrt(a * b)} (M1); × {k} = {k * math.isqrt(a * b)} (A1).')
    if kind == 'quot':
        b = r.choice([2, 3, 5, 6, 7])
        m = r.randint(2, 7)
        a = b * m * m
        return Q(f'Work out √{a} ÷ √{b}.', str(m), f'√{a} ÷ √{b} = √({a} ÷ {b}) = √{m * m} (M1) = {m} (A1).')
    n = nonsq(r, 2, 15)
    a, b = r.randint(2, 5), r.randint(2, 5)
    return Q(f'Work out (√{n})² + (√{a * a})³ ÷ {a}, without a calculator.', N(n + a * a), f'(√{n})² = {n}; √{a * a} = {a} so {a}³ ÷ {a} = {a * a} (M1); total {n} + {a * a} = {n + a * a} (A1).')


def _surd_square(r, D):
    A = nonsq(r, 20, 200)
    a = math.isqrt(A)
    thing = r.choice(['floor tile', 'garden', 'piece of card', 'solar panel', 'table top'])
    s = math.sqrt(A)
    intro = r.choice([f'A square {thing} has an area of {A} cm².', f'{person(r)} has a square {thing}. Its area is {A} cm².'])
    parts = [
        lambda r: ('Explain why the side length of the square is an irrational number.', f'Side = √{A} and {A} is not a square number.', f'B1 side = √{A}, {A} not a perfect square [1]'),
        lambda r: ('Write down the two consecutive whole numbers that the side length lies between.', f'{a} and {a + 1}', f'B1 {a}² = {a * a} < {A} < {(a + 1) ** 2} [1]'),
        lambda r: ('Estimate the side length to 1 decimal place without a calculator.', f'{fdp(s, 1)} cm', f'M1 trial between {a} and {a + 1}; A1 {fdp(s, 1)} [2]'),
        lambda r: ('Calculate the perimeter of the square, giving your answer correct to 1 decimal place.', f'{fdp(4 * s, 1)} cm', f'M1 4 × √{A}; A1 {fdp(4 * s, 1)} cm [2]'),
        lambda r: ('A second square has sides twice as long. Work out the exact area of the second square.', f'{4 * A} cm²', f'M1 (2√{A})² = 4 × {A}; A1 {4 * A} cm² [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


def _number_list(r, D):
    k = r.randint(2, 9)
    n1, n2 = nonsq(r, 2, 40), nonsq(r, 41, 99)
    f = Fr(r.randint(1, 8), r.choice([3, 7, 9, 11]))
    nums = [(f'√{n1}', math.sqrt(n1), True), (f'√{k * k}', k, False), (fr(f), float(f), False), (f'√{n2}', math.sqrt(n2), True),
            ('π', math.pi, True), (f'{r.randint(1, 9)}.{r.randint(1, 9)}{r.randint(1, 9)}', None, False)]
    nums[5] = (nums[5][0], float(nums[5][0]), False)
    r.shuffle(nums)
    lst = ', '.join(x[0] for x in nums)
    irr = [x[0] for x in nums if x[2]]
    order = ', '.join(x[0] for x in sorted(nums, key=lambda x: x[1]))
    lo, hi = sorted([math.sqrt(n1), math.sqrt(n2)])
    intro = f'Here is a list of numbers: {lst}.'
    parts = [
        lambda r: ('Write down all the irrational numbers in the list.', ', '.join(irr), f'B2 all three ({", ".join(irr)}), B1 for two correct and no extras [2]'),
        lambda r: ('Write the numbers in order of size, starting with the smallest.', order, 'M1 converts each to a decimal estimate; A1 correct order [2]'),
        lambda r: (f'Write down a whole number that lies between √{n1} and √{n2}.', f'Any integer from {math.ceil(lo) if math.ceil(lo) > lo else int(lo) + 1} to {math.floor(hi)}', f'B1 any integer n with {n1} < n² < {n2} [1]'),
        lambda r: ('Explain why √' + str(k * k) + ' is rational.', f'√{k * k} = {k}, an integer.', 'B1 [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t11.add('C4', (2, 3, 4, 5), 'multi_step')(_surd_square)
t11.add('C4', (2, 3, 4), 'multi_step')(_number_list)


# ----------------------------------------------------------- standard form
t12 = topic('Standard form', 'standard form', 'large and small numbers')
t12.fixed('C1', (1, 2), [
    ('Which of these numbers is written in standard form? 35 × 10⁴, 3.5 × 10⁴, 0.35 × 10⁵, 3.5 × 4¹⁰', '3.5 × 10⁴', 'Standard form is A × 10ⁿ with 1 ≤ A < 10 and n an integer. [1]', ['35 × 10⁴', '0.35 × 10⁵', '3.5 × 4¹⁰']),
    ('A number is written in standard form as A × 10ⁿ. What condition must A satisfy?', '1 ≤ A < 10', 'A must be at least 1 and less than 10. [1]', ['0 < A < 1', '1 < A ≤ 10', 'A is a whole number']),
    ('A number in standard form has a negative power of 10. What does this tell you about the number?', 'It is between 0 and 1', 'A × 10⁻ⁿ with 1 ≤ A < 10 is less than 1 (and positive). [1]', ['It is negative', 'It is greater than 10', 'It is a whole number']),
    ('Write 1 million in standard form.', '1 × 10⁶', '1 000 000 = 1 × 10⁶. B1 [1]'),
])


def _sf_num(r, D, small=None):
    m = r.choice([1.2, 2.5, 3.4, 4.06, 5.7, 6.08, 7.25, 8.9, 9.1, 2.03, 3.75, 1.85, 6.4, 4.5])
    if small is None:
        small = D >= 2 and r.random() < 0.5
    e = -r.randint(2, 3 + D) if small else r.randint(3, 4 + 2 * D)
    return m, e, m * 10 ** e


def plain(m, e):
    """Ordinary decimal for m × 10^e without float noise."""
    from decimal import Decimal
    d = Decimal(repr(m)).scaleb(e)
    s = format(d.normalize(), 'f')
    if '.' in s:
        s = s.rstrip('0').rstrip('.')
    if '.' not in s and len(s) > 4:
        s = f'{int(s):,}'
    return s


@t12.add('C1', (1, 2, 3))
def t12_to(r, D):
    m, e, _ = _sf_num(r, D)
    p = plain(m, e)
    ans = sform(m, e)
    w = N(round(m * 10, 6))
    stem = r.choice([f'Write {p} in standard form.', f'Which of these shows {p} written in standard form?', f'{p} written in standard form is'])
    return MCQ(r, stem, ans, [sform(m, e + 1), sform(m, e - 1), f'{w} × 10{sup(e - 1)}', sform(m, -e), f'{N(m)} × 10{sup(e + 2)}'],
               f'Move the decimal point so 1 ≤ A < 10: {p} = {ans}. [1]')


@t12.add('C1', (1, 2, 3))
def t12_from(r, D):
    m, e, _ = _sf_num(r, D)
    ans = plain(m, e)
    stem = r.choice([f'Write {sform(m, e)} as an ordinary number.', f'What is {sform(m, e)} as an ordinary number?'])
    return MCQ(r, stem, ans, [plain(m, e + 1), plain(m, e - 1), plain(m, -e), plain(m, e + 2) if e > 0 else plain(m, e - 2)],
               f'{"Multiply" if e > 0 else "Divide"} {N(m)} by 10{sup(abs(e))}: {ans}. [1]')


@t12.add('C2', (1, 2, 3, 4), 'explain')
def t12_notsf(r, D):
    m, e, _ = _sf_num(r, D)
    p = plain(m, e)
    bad = r.choice(['big', 'small', 'sign']) if D >= 2 else 'big'
    who = person(r)
    if bad == 'big':
        w = f'{N(round(m * 10, 6))} × 10{sup(e - 1)}'
        why = f'{N(round(m * 10, 6))} is not between 1 and 10'
    elif bad == 'small':
        w = f'{N(round(m / 10, 6))} × 10{sup(e + 1)}'
        why = f'{N(round(m / 10, 6))} is less than 1'
    else:
        w = sform(m, -e)
        why = f'the power should be {N(e)}, not {N(-e)}; the {"number is greater than 1" if e > 0 else "number is less than 1"}'
    return Q(f'{who} writes {p} = {w} and says this is in standard form. Explain what is wrong and write the number correctly in standard form.',
             f'{why[0].upper() + why[1:]}. Correct: {sform(m, e)}.', f'B1 reason ({why}); B1 {sform(m, e)}. [2]')


@t12.add('C2', (1, 2, 3, 4), 'explain')
def t12_compare(r, D):
    m1, m2 = r.sample([1.5, 2.4, 3.6, 4.2, 5.8, 6.3, 7.7, 8.1, 9.4], 2)
    e1 = r.randint(-8, 9)
    e2 = e1 + r.choice([-1, 1, -2])
    big = sform(m1, e1) if m1 * 10 ** e1 > m2 * 10 ** e2 else sform(m2, e2)
    who = person(r)
    if max(m1, m2) == (m1 if e1 < e2 else m2) and r.random() < 0.6:
        lw = sform(m1, e1) if e1 < e2 else sform(m2, e2)
        stem = f'{who} says {lw} is larger than {sform(m2, e2) if lw == sform(m1, e1) else sform(m1, e1)} because {N(max(m1, m2))} is bigger than {N(min(m1, m2))}. Is {who} correct? Explain.'
    else:
        stem = f'Which is larger, {sform(m1, e1)} or {sform(m2, e2)}? Explain how you know without writing them as ordinary numbers.'
    return Q(stem, f'{big} is larger: compare the powers of 10 first; the number with the greater power of 10 is larger.',
             'B1 compares the powers of 10 first (the higher power is larger whatever A is); B1 correct number identified. [2]')


@t12.add('C3', (1, 2, 3, 4, 5))
def t12_order(r, D):
    vals = []
    seen = set()
    while len(vals) < 4:
        m = r.choice([1.2, 2.5, 3.4, 4.6, 5.7, 6.8, 7.3, 8.9, 9.05, 3.06])
        e = r.randint(-4, 6) if D >= 3 else r.randint(2, 6)
        if (m, e) in seen:
            continue
        seen.add((m, e))
        vals.append((m, e, m * 10 ** e))
    shown = [sform(m, e) if (i % 2 == 0 or D < 3) else plain(m, e) for i, (m, e, _) in enumerate(vals)]
    order = [s for _, s in sorted(zip([v[2] for v in vals], shown))]
    if D == 1:
        stem = f'Which of these numbers is the largest? {", ".join(shown)}'
        return MCQ(r, stem, order[-1], order[:-1], f'Compare powers of 10 first, then A: largest is {order[-1]}. [1]')
    return Q(f'Write these numbers in order of size, starting with the smallest: {", ".join(shown)}.', ', '.join(order),
             'M1 writes all in the same form (standard form or ordinary); A1 correct order. [2]')


SF_FACTS = [
    ('The distance from the Earth to the Sun is about {} km.', 149600000), ('The population of the world is about {} people.', 8100000000),
    ('The diameter of a red blood cell is about {} m.', 0.0000075), ('The mass of a dust particle is about {} g.', 0.00000075),
    ('The thickness of a sheet of paper is about {} mm.', 0.09), ('A human hair has a width of about {} m.', 0.00008),
    ('The area of the Pacific Ocean is about {} km².', 165250000), ('The speed of light is about {} m/s.', 299800000),
    ('The wavelength of red light is about {} m.', 0.0000007), ('A grain of sand has a mass of about {} kg.', 0.0000044),
    ('The number of seconds in a year is about {}.', 31540000), ('A virus has a length of about {} mm.', 0.00012),
]


@t12.add('C3', (1, 2, 3, 4))
def t12_context(r, D):
    txt, v = r.choice(SF_FACTS)
    e = int(math.floor(math.log10(v)))
    m = round(v / 10 ** e, 4)
    pl = plain(m, e)
    if r.random() < 0.5:
        return Q(txt.format(pl) + ' Write this number in standard form.', sform(m, e), f'1 ≤ A < 10: {pl} = {sform(m, e)} (B1). [1]')
    return Q(txt.format(sform(m, e)) + ' Write this number as an ordinary number.', pl, f'{sform(m, e)} = {pl} (B1). [1]')


def _sf_c4(r, D):
    m, e, _ = _sf_num(r, D, small=False)
    m2, e2, _ = _sf_num(r, D, small=True)
    who = person(r)
    intro = f'{who} is making a fact sheet. One number on it is {plain(m, e)}; another is {plain(m2, e2)}.'
    parts = [
        lambda r: ('Write both numbers in standard form.', f'{sform(m, e)} and {sform(m2, e2)}', 'B1 each [2]'),
        lambda r: (f'Write {sform(m, e + 1)} as an ordinary number.', plain(m, e + 1), 'B1 [1]'),
        lambda r: (f'{who} writes the second number as {N(round(m2 * 10, 5))} × 10{sup(e2 - 1)}. Explain why this is not standard form.', f'{N(round(m2 * 10, 5))} is not between 1 and 10.', 'B1 [1]'),
        lambda r: (f'How many times larger is 10{sup(e)} than 10{sup(e2)}? Give your answer as a power of 10.', f'10{sup(e - e2)}', f'M1 subtract powers {e} − ({e2}); A1 10{sup(e - e2)} [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t12.add('C4', (2, 3, 4), 'multi_step')(_sf_c4)


# ----------------------------------------------------------- laws of indices
t13 = topic('Laws of indices', 'laws of indices', 'zero and negative indices', 'indices')
t13.fixed('C1', (1, 2), [
    ('What is the value of 7⁰?', '1', 'Any non-zero number to the power 0 is 1. [1]', ['0', '7', '70']),
    ('Write 5⁻² as a fraction.', '1/25', '5⁻² = 1/5² = 1/25. [1]', ['−25', '−10', '1/10']),
    ('Which rule for indices is correct for any number a (a ≠ 0): aᵐ ÷ aⁿ = aᵐ⁻ⁿ, aᵐ ÷ aⁿ = aᵐ÷ⁿ, aᵐ × aⁿ = aᵐⁿ or (aᵐ)ⁿ = aᵐ⁺ⁿ?', 'aᵐ ÷ aⁿ = aᵐ⁻ⁿ', 'Dividing powers of the same base: subtract the indices. [1]', ['aᵐ ÷ aⁿ = aᵐ÷ⁿ', 'aᵐ × aⁿ = aᵐⁿ', '(aᵐ)ⁿ = aᵐ⁺ⁿ']),
    ('Write 1/8 as a power of 2.', '2⁻³', '8 = 2³ so 1/8 = 2⁻³. B1 [1]'),
    ('Write down the value of 10⁻³ as a decimal.', '0.001', '10⁻³ = 1/1000 = 0.001. B1 [1]'),
    ('Write down the reciprocal of 4 using a negative index.', '4⁻¹', 'The reciprocal of a is a⁻¹ = 1/a. B1 [1]'),
])
t13.fixed('C2', (2, 3), [
    ('Use the rule aᵐ ÷ aⁿ = aᵐ⁻ⁿ to explain why 3⁰ = 1.', '3² ÷ 3² = 3²⁻² = 3⁰, but 3² ÷ 3² = 9 ÷ 9 = 1, so 3⁰ = 1.', 'M1 uses a division such as 3ⁿ ÷ 3ⁿ; A1 both results compared to give 1. [2]'),
    ('Explain why 2⁻³ is not a negative number.', '2⁻³ = 1/2³ = 1/8, a positive number. A negative index means a reciprocal, not a negative value.', 'B1 2⁻³ = 1/8; B1 negative index means reciprocal. [2]'),
    ('Explain why 0⁰ is not used in the rule a⁰ = 1.', 'The rule comes from aⁿ ÷ aⁿ, which would mean 0 ÷ 0; division by zero is not defined, so a ≠ 0.', 'B1 derivation uses division; B1 cannot divide by 0. [2]'),
])


def _pw(b, n):
    return f'{b}{sup(n)}'


@t13.add('C1', (1, 2, 3))
def t13_law(r, D):
    b = r.choice(['a', 'x', 'y', 'p', 'm', 'n', '2', '3', '5', '7'])
    m, n = r.randint(2, 9), r.randint(2, 6)
    if D >= 3:
        n = -n
    kind = r.choice(['mul', 'div', 'pow'])
    if kind == 'mul':
        e, w = f'{_pw(b, m)} × {_pw(b, n)}', [m * n, m - n, m + n + 1]
        ans = m + n
    elif kind == 'div':
        e, w = f'{_pw(b, m)} ÷ {_pw(b, n)}', [m + n, m * n, n - m]
        ans = m - n
    else:
        e, w = f'({_pw(b, m)}){sup(n)}', [m + n, m - n, m * n + 1]
        ans = m * n
    stem = r.choice([f'Simplify {e}. Give your answer as a single power.', f'Which of these is equal to {e}?', f'Write {e} as a single power of {b}.'])
    rule = {'mul': 'add the indices', 'div': 'subtract the indices', 'pow': 'multiply the indices'}[kind]
    return MCQ(r, stem, _pw(b, ans), [_pw(b, x) for x in w] + [_pw(b, -ans)], f'Same base, {rule}: {_pw(b, ans)}. [1]')


@t13.add('C1', (1, 2, 3))
def t13_value(r, D):
    b = r.choice([2, 3, 4, 5, 6, 10])
    n = r.choice([0, 1, 2]) if D == 1 else r.choice([1, 2, 3])
    if n == 0:
        return MCQ(r, f'What is the value of {b * r.randint(1, 9)}⁰ + {b}⁰?' if D > 1 else f'What is the value of {_pw(b, 0)}?',
                   '2' if D > 1 else '1', ['0', str(b), '1' if D > 1 else '2', str(2 * b)], 'Any non-zero number to the power 0 is 1. [1]')
    ans = f'1/{b ** n}'
    return MCQ(r, r.choice([f'What is the value of {b}{sup(-n)}?', f'Write {b}{sup(-n)} as a fraction.']), ans,
               [f'{MINUS}{b ** n}', f'{MINUS}{b * n}', f'1/{b * n}', str(b ** n)], f'{b}{sup(-n)} = 1/{b}{sup(n)} = {ans}. [1]')


@t13.add('C2', (1, 2, 3, 4), 'explain')
def t13_error(r, D):
    v = r.choice(['x', 'a', 'y', 'n', 't'])
    m, n = r.randint(2, 7), r.randint(2, 6)
    k = r.randint(2, 5)
    p = person(r)
    kinds = ['mul', 'pow_coef', 'neg', 'zero'] if D >= 2 else ['mul', 'zero']
    kind = r.choice(kinds)
    if kind == 'mul':
        stem = f'{p} writes: {_pw(v, m)} × {_pw(v, n)} = {_pw(v, m * n)}. Explain the mistake and write the correct answer.'
        ans = f'When multiplying powers of the same base you add the indices, not multiply them: {_pw(v, m + n)}.'
        key = f'B1 should add indices; B1 {_pw(v, m + n)}. [2]'
    elif kind == 'pow_coef':
        stem = f'{p} writes: ({k}{_pw(v, m)})² = {k}{_pw(v, 2 * m)}. Explain the mistake and write the correct answer.'
        ans = f'The {k} must be squared as well: ({k}{_pw(v, m)})² = {k * k}{_pw(v, 2 * m)}.'
        key = f'B1 coefficient also squared; B1 {k * k}{_pw(v, 2 * m)}. [2]'
    elif kind == 'neg':
        stem = f'{p} says that {k}{sup(-n)} = {MINUS}{k ** n}. Explain why {p} is wrong and give the correct value.'
        ans = f'A negative index means the reciprocal: {k}{sup(-n)} = 1/{k}{sup(n)} = 1/{k ** n}.'
        key = f'B1 negative index = reciprocal; B1 1/{k ** n}. [2]'
    else:
        stem = f'{p} says that {_pw(v, m)} ÷ {_pw(v, m)} = 0 because the indices subtract to 0. Explain the error.'
        ans = f'{_pw(v, m)} ÷ {_pw(v, m)} = {_pw(v, 0)} = 1 (anything non-zero divided by itself is 1), not 0.'
        key = 'B1 index 0 gives v⁰; B1 value 1. [2]'
    return Q(stem, ans, key)


@t13.add('C2', (2, 3, 4), 'explain')
def t13_true(r, D):
    a, b = r.sample([2, 3, 5], 2) if r.random() < 0.5 else (2, 2)
    m, n = r.randint(2, 5), r.randint(2, 5)
    p = person(r)
    if a == b:
        stem = f'{p} says: "{a}{sup(m)} × {a}{sup(n)} = {a * a}{sup(m + n)} because you multiply the {a}s and add the powers." Is {p} correct? Explain.'
        ans = f'No. The base stays the same: {a}{sup(m)} × {a}{sup(n)} = {a}{sup(m + n)} = {a ** (m + n)}, but {a * a}{sup(m + n)} is much larger.'
    else:
        stem = f'{p} says: "{a}{sup(m)} × {b}{sup(m)} = {a * b}{sup(m)}." Is {p} correct? Explain.'
        ans = f'Yes. {a}{sup(m)} × {b}{sup(m)} = ({a} × {b}){sup(m)} = {a * b}{sup(m)} = {(a * b) ** m}, because each pair {a} × {b} = {a * b}.'
    return Q(stem, ans, 'B1 correct decision; B1 reason with values or index law. [2]')


@t13.add('C3', (1, 2, 3, 4, 5))
def t13_simplify(r, D):
    v = r.choice(['x', 'a', 'y', 'm', 'p'])
    a, b = r.randint(2, 6), r.randint(2, 5)
    m, n = r.randint(2, 8), r.randint(1, 6)
    if D >= 3:
        n = -n if r.random() < 0.5 else n
    kind = r.choice(['mul', 'div', 'pow'] + (['mix'] if D >= 4 else []))
    if kind == 'mul':
        e, ans = f'{a}{_pw(v, m)} × {b}{_pw(v, n)}', f'{a * b}{_pw(v, m + n)}'
        key = f'{a} × {b} = {a * b} (B1); {v}^({m} + {N(n)}) = {_pw(v, m + n)} (B1).'
    elif kind == 'div':
        e, ans = f'{a * b}{_pw(v, m)} ÷ {b}{_pw(v, n)}', f'{a}{_pw(v, m - n)}' if m != n else str(a)
        key = f'{a * b} ÷ {b} = {a} (B1); {v}^({m} − {par(n)}) = {_pw(v, m - n)} (B1).'
    elif kind == 'pow':
        e, ans = f'({a}{_pw(v, m)}){sup(3 if D >= 4 else 2)}', f'{a ** (3 if D >= 4 else 2)}{_pw(v, m * (3 if D >= 4 else 2))}'
        key = f'coefficient {a} raised to the power (B1); indices multiplied (B1): {ans}.'
    else:
        c = r.randint(2, 4)
        top = f'{a}{_pw(v, m)} × {b * c}{_pw(v, n)}'
        e, ans = f'({top}) ÷ {c}{_pw(v, m + n - 1)}', f'{a * b}{v}'
        key = f'numerator {a * b * c}{_pw(v, m + n)} (M1); divide: {a * b}{_pw(v, 1)} = {a * b}{v} (A1).'
    if ans.endswith(_pw(v, 1)):
        ans = ans[: -len(_pw(v, 1))] + v
    if ans.endswith(_pw(v, 0)):
        ans = ans[: -len(_pw(v, 0))]
    if D == 1:
        return MCQ(r, f'Simplify {e}.', ans, [f'{a + b}{_pw(v, m + n)}', f'{a * b}{_pw(v, m * n)}', f'{a}{_pw(v, m * n)}', f'{a * b}{_pw(v, m - n)}'], key)
    return Q(f'Simplify {e}.', ans, key)


@t13.add('C3', (1, 2, 3, 4, 5))
def t13_evaluate(r, D):
    kind = r.choice(['neg', 'frac', 'combo'] if D >= 3 else ['neg', 'combo'])
    if kind == 'neg':
        b, n = r.choice([2, 3, 4, 5, 10]), r.randint(1, 3)
        return Q(f'Work out the value of {b}{sup(-n)}, giving your answer as a fraction.', f'1/{b ** n}', f'{b}{sup(-n)} = 1/{b}{sup(n)} (M1) = 1/{b ** n} (A1).')
    if kind == 'frac':
        p, q = r.choice([(1, 2), (2, 3), (3, 4), (1, 5), (2, 5), (1, 3)])
        n = r.randint(1, 3)
        return Q(f'Work out ({p}/{q}){sup(-n)}.', fr(Fr(q, p) ** n), f'({p}/{q}){sup(-n)} = ({q}/{p}){sup(n)} (M1) = {fr(Fr(q, p) ** n)} (A1).')
    b = r.choice([2, 3, 4, 5])
    m, n = r.randint(2, 6), r.randint(3, 8)
    e = m - n
    val = Fr(b) ** e
    return Q(f'Work out {b}{sup(m)} × {b}{sup(-n)} ÷ {b}⁰. Give your answer as {"a fraction" if e < 0 else "a whole number"}.', fr(val),
             f'{b}{sup(m)} × {b}{sup(-n)} = {b}{sup(e)} (M1); ÷ {b}⁰ = ÷ 1; value {fr(val)} (A1).')


@t13.add('C3', (2, 3, 4, 5))
def t13_solve(r, D):
    b = r.choice([2, 3, 5])
    m = r.randint(2, 7)
    n = r.randint(-4, 6)
    if D <= 3:
        return Q(f'Find the value of n when {b}{sup(m)} × {b}ⁿ = {b}{sup(m + n)}.', N(n), f'Add indices: {m} + n = {m + n} (M1), n = {N(n)} (A1).')
    big = {2: [(4, 2), (8, 3), (16, 4)], 3: [(9, 2), (27, 3)], 5: [(25, 2), (125, 3)]}[b]
    B, k = r.choice(big)
    c = r.randint(1, 4)
    tot = k * c + n
    return Q(f'Find the value of n when {B}{sup(c)} × {b}ⁿ = {b}{sup(tot)}.', N(n), f'{B} = {b}{sup(k)}, so {B}{sup(c)} = {b}{sup(k * c)} (M1); {k * c} + n = {N(tot)} (M1); n = {N(n)} (A1).')


def _ind_c4(r, D):
    b = r.choice([2, 3])
    B1, k1 = (4, 2) if b == 2 else (9, 2)
    B2, k2 = (8, 3) if b == 2 else (27, 3)
    x, y = r.randint(2, 5), r.randint(1, 4)
    tot = k1 * x + k2 * y
    z = r.randint(2, 4)
    intro = r.choice([f'{person(r)} is working with powers of {b}.', f'This question is about powers of {b}.'])
    parts = [
        lambda r: (f'Write {B1}{sup(x)} × {B2}{sup(y)} as a single power of {b}.', f'{b}{sup(tot)}', f'M1 {B1} = {b}{sup(k1)}, {B2} = {b}{sup(k2)}; A1 {b}{sup(tot)} [2]'),
        lambda r: (f'Write 1/{B2} as a power of {b}.', f'{b}{sup(-k2)}', 'B1 [1]'),
        lambda r: (f'Find n if {b}ⁿ ÷ {b}{sup(z)} = {b}{sup(-1)}.', str(z - 1), f'M1 n − {z} = −1; A1 n = {z - 1} [2]'),
        lambda r: (f'Show that ({b}{sup(z)})⁰ × {b}{sup(-z)} × {b}{sup(z)} = 1.', f'(…)⁰ = 1 and {b}{sup(-z)} × {b}{sup(z)} = {b}⁰ = 1, so the product is 1.', 'M1 uses x⁰ = 1; A1 indices sum to 0 [2]'),
        lambda r: (f'Put these in order of size, smallest first: {b}{sup(-2)}, {b}⁰, {b}{sup(-1)}, {B1}{sup(-1)}.',
                   f'{B1}{sup(-1)} = {b}{sup(-2)}, {b}{sup(-1)}, {b}⁰ (the first two are equal)', 'M1 converts to fractions; A1 order noting equality [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t13.add('C4', (2, 3, 4, 5), 'multi_step')(_ind_c4)


# ----------------------------------------------------------- calculating with standard form
t14 = topic('Calculating with standard form', 'estimating and calculating with standard form', 'calculating standard form')
t14.fixed('C1', (1, 2), [
    ('Work out (2 × 10³) × (4 × 10⁵). Give your answer in standard form.', '8 × 10⁸', 'Multiply 2 × 4 = 8, add powers 3 + 5 = 8. [1]', ['8 × 10¹⁵', '6 × 10⁸', '8 × 10²']),
    ('Work out (9 × 10⁷) ÷ (3 × 10²).', '3 × 10⁵', '9 ÷ 3 = 3, 10⁷ ÷ 10² = 10⁵. [1]', ['3 × 10⁹', '6 × 10⁵', '3 × 10¹⁴']),
    ('What should you do first to add 3 × 10⁴ and 5 × 10³?', 'Write both with the same power of 10', 'For addition, numbers must be in the same power (or as ordinary numbers): 30 000 + 5 000 = 35 000 = 3.5 × 10⁴. [1]',
     ['Add the powers', 'Multiply the front numbers', 'Add the front numbers and keep 10⁴']),
])


def _sf_pair(r, D):
    ms = [1.2, 1.5, 2, 2.5, 3, 3.2, 4, 4.5, 5, 6, 7.5, 8]
    a, b = r.choice(ms), r.choice(ms)
    m, n = r.randint(-6, 9), r.randint(-6, 9)
    if D <= 2:
        m, n = r.randint(2, 8), r.randint(2, 7)
    return a, m, b, n


def sfstr(x):
    return to_sform(x, 6)


@t14.add('C3', (1, 2, 3, 4, 5))
def t14_muldiv(r, D):
    a, m, b, n = _sf_pair(r, D)
    if r.random() < 0.5:
        v = a * b * 10.0 ** (m + n)
        e = f'({sform(a, m)}) × ({sform(b, n)})'
        raw = f'{N(round(a * b, 6))} × 10{sup(m + n)}'
    else:
        a = round(a * b, 6) if D >= 2 else a * b
        v = a / b * 10.0 ** (m - n)
        e = f'({sform(a, m) if a < 10 else N(a) + " × 10" + sup(m)}) ÷ ({sform(b, n)})'
        raw = f'{N(round(a / b, 6))} × 10{sup(m - n)}'
        if a >= 10:
            a2, m2 = a / 10, m + 1
            e = f'({sform(round(a2, 6), m2)}) ÷ ({sform(b, n)})'
            v = a2 / b * 10.0 ** (m2 - n)
            raw = f'{N(round(a2 / b, 6))} × 10{sup(m2 - n)}'
    ans = sfstr(v)
    stem = r.choice([f'Work out {e}. Give your answer in standard form.', f'Without a calculator, work out {e}, giving your answer in standard form.'])
    key = f'Front numbers and powers separately: {raw} (M1); in standard form {ans} (A1).'
    if D == 1:
        ee = int(math.floor(math.log10(v)))
        mm = round(v / 10 ** ee, 6)
        return MCQ(r, stem, ans, [sform(mm, ee + 1), sform(mm, ee - 1), sform(round(mm * 2 % 9 + 1, 2), ee), raw], key)
    return Q(stem, ans, key)


@t14.add('C3', (2, 3, 4, 5))
def t14_add(r, D):
    a, b = r.choice([1.5, 2.4, 3.6, 4.2, 5.1, 6.3, 7.2]), r.choice([1.2, 2.5, 3.4, 4.8, 5.6, 8.1])
    m = r.randint(3, 8) if D <= 3 else r.randint(-7, -3)
    n = m - r.randint(1, 2)
    op = r.choice(['+', '−'])
    from decimal import Decimal
    v = Decimal(repr(a)).scaleb(m) + (1 if op == '+' else -1) * Decimal(repr(b)).scaleb(n)
    ans = to_sform(float(v), 6)
    return Q(f'Work out ({sform(a, m)}) {op} ({sform(b, n)}). Give your answer in standard form.', ans,
             f'Write with the same power: {plain(a, m)} {op} {plain(b, n)} = {plain(float(v), 0) if abs(v) >= 1 else format(v.normalize(), "f")} (M1); = {ans} (A1).')


@t14.add('C2', (1, 2, 3, 4), 'explain')
def t14_err(r, D):
    a, b = r.choice([(3, 4), (5, 6), (4, 7), (2, 8), (6, 9), (5, 5), (8, 3)])
    m, n = r.randint(2, 9), r.randint(2, 9)
    p = person(r)
    prod = a * b
    ans_sf = sform(prod / 10, m + n + 1)
    if r.random() < 0.5:
        stem = f'{p} works out ({sform(a, m)}) × ({sform(b, n)}) and writes the answer {prod} × 10{sup(m + n)}. Explain why this is not in standard form and correct it.'
        ans = f'{prod} is not between 1 and 10. {prod} × 10{sup(m + n)} = {ans_sf}.'
    else:
        stem = f'{p} works out ({sform(a, m)}) × ({sform(b, n)}) = {sform(prod / 10, m * n + 1) if prod >= 10 else sform(prod, m * n)}. Find the mistake and give the correct answer in standard form.'
        ans = f'The powers of 10 should be added ({m} + {n} = {m + n}), not multiplied. Correct answer: {ans_sf if prod >= 10 else sform(prod, m + n)}.'
    return Q(stem, ans, 'B1 identifies the error; B1 correct standard form answer. [2]')


@t14.add('C2', (1, 2, 3, 4), 'explain')
def t14_estimate(r, D):
    x = r.choice([3.87, 4.12, 6.03, 7.94, 2.09, 5.96, 8.11, 1.98])
    y = r.choice([2.03, 1.96, 4.07, 3.02, 5.1, 6.89])
    m, n = r.randint(3, 9), r.randint(-5, 6)
    rx, ry = round(x), round(y)
    est = rx * ry
    p = person(r)
    calc = sfstr(x * y * 10.0 ** (m + n))
    return Q(f'{p} uses a calculator to work out ({sform(x, m)}) × ({sform(y, n)}) and gets {calc}. Use an estimate to show whether this answer is reasonable.',
             f'Estimate: {rx} × 10{sup(m)} × {ry} × 10{sup(n)} = {sfstr(est * 10.0 ** (m + n))}, close to {calc}, so the answer is reasonable.',
             'M1 rounds each front number to 1 s.f.; A1 estimate compared with calculator answer. [2]')


SF_CTX = [
    ('The mass of the Earth is {a} kg and the mass of the Moon is {b} kg.', 5.97e24, 7.35e22, 'mass of the Earth', 'mass of the Moon'),
    ('Light travels at {a} m/s. The distance from the Sun to the Earth is {b} m.', 3e8, 1.5e11, None, None),
    ('A country has a population of {a} people and an area of {b} km².', 5.6e7, 2.4e5, None, None),
    ('A bacterium is {a} m long. A grain of rice is {b} m long.', 2e-6, 6e-3, None, None),
    ('A computer does {a} calculations per second. A task needs {b} calculations.', 4e9, 1.2e13, None, None),
]


def _sf_c4b(r, D):
    i = r.randrange(len(SF_CTX))
    txt, a, b, _, _ = SF_CTX[i]
    ma = r.choice([0.8, 1, 1.2, 1.5, 2]) if i != 0 else 1
    a = a * ma
    intro = txt.format(a=sfstr(a), b=sfstr(b))
    if i == 0:
        parts = [lambda r: ('How many times heavier is the Earth than the Moon? Give your answer to the nearest whole number.', str(round(a / b)), f'M1 {sfstr(a)} ÷ {sfstr(b)}; A1 {round(a / b)} [2]'),
                 lambda r: ('Work out the total mass of the Earth and the Moon in standard form.', sfstr(a + b), f'M1 same power of 10; A1 {sfstr(a + b)} kg [2]'),
                 lambda r: ('Write the mass of the Moon as an ordinary number of tonnes (1 tonne = 1000 kg) in standard form.', sfstr(b / 1000), f'B1 {sfstr(b / 1000)} tonnes [1]')]
    elif i == 1:
        parts = [lambda r: ('Calculate the time, in seconds, for light to travel from the Sun to the Earth.', f'{N(round(b / a))} s', f'M1 time = distance ÷ speed = {sfstr(b)} ÷ {sfstr(a)}; A1 {N(round(b / a))} s [2]'),
                 lambda r: ('Calculate the time for light to travel from the Sun to the Earth in minutes, correct to 1 decimal place.', f'{fdp(b / a / 60, 1)} minutes', 'B1 [1]'),
                 lambda r: ('Write the distance in kilometres, in standard form.', sfstr(b / 1000), 'B1 [1]')]
    elif i == 2:
        parts = [lambda r: ('Calculate the population density (people per km²). Give your answer to 3 significant figures.', sf(a / b, 3), f'M1 {sfstr(a)} ÷ {sfstr(b)}; A1 {sf(a / b, 3)} [2]'),
                 lambda r: ('The population increases by 1.5 × 10⁶. Write the new population in standard form.', sfstr(a + 1.5e6), 'M1 same powers; A1 [2]'),
                 lambda r: ('Write the area as an ordinary number.', plain(round(b / 10 ** int(math.log10(b)), 6), int(math.log10(b))), 'B1 [1]')]
    elif i == 3:
        parts = [lambda r: ('How many times longer is the grain of rice than the bacterium?', N(round(b / a)), f'M1 {sfstr(b)} ÷ {sfstr(a)}; A1 {N(round(b / a))} [2]'),
                 lambda r: ('Write the length of the bacterium in millimetres, in standard form.', sfstr(a * 1000), 'B1 [1]'),
                 lambda r: ('Work out the total length of 5000 of these bacteria placed end to end, in metres, in standard form.', sfstr(a * 5000), 'M1 × 5 × 10³; A1 [2]')]
    else:
        parts = [lambda r: ('Calculate the time the computer takes to complete the task, in seconds.', f'{N(round(b / a))} s', f'M1 {sfstr(b)} ÷ {sfstr(a)}; A1 {N(round(b / a))} [2]'),
                 lambda r: ('Calculate the time the computer takes to complete the task, in minutes, correct to 1 decimal place.', f'{fdp(b / a / 60, 1)} minutes', 'B1 [1]'),
                 lambda r: ('A new computer is 20 times faster. Write the number of calculations it does per second in standard form.', sfstr(a * 20), 'M1 × 2 × 10¹; A1 [2]')]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t14.add('C4', (2, 3, 4, 5), 'multi_step')(_sf_c4b)
t14.add('C4', (2, 3, 4), 'multi_step')(_sf_c4)
t12.add('C4', (2, 3, 4, 5), 'multi_step')(_sf_c4b)


@t14.add('C4', (3, 4, 5), 'multi_step')
def t14_planet(r, D):
    planets = [('Mercury', 5.79e7), ('Venus', 1.08e8), ('Mars', 2.28e8), ('Jupiter', 7.79e8), ('Saturn', 1.43e9)]
    (p1, d1), (p2, d2) = sorted(r.sample(planets, 2), key=lambda x: x[1])
    sp = r.choice([3e4, 4e4, 5e4, 6e4])
    diff = d2 - d1
    hrs = diff / sp
    return Q(f'The mean distance of {p1} from the Sun is {sfstr(d1)} km and that of {p2} is {sfstr(d2)} km. (a) Work out the difference between these distances in standard form. (b) A space probe travels at {sfstr(sp)} km/h. Assuming it travels in a straight line between the two orbits, calculate how many days the journey would take, to the nearest day.',
             f'(a) {sfstr(diff)} km (b) {round(hrs / 24)} days',
             f'(a) M1 same powers; A1 {sfstr(diff)} km [2] (b) M1 {sfstr(diff)} ÷ {sfstr(sp)} = {sf(hrs, 4)} hours; M1 ÷ 24; A1 {round(hrs / 24)} days [3]', marks=5)


CHAPTERS[1] = [t11, t12, t13, t14]


# =========================================================== 2 Expressions and formulae
t21 = topic('Substituting into expressions and formulae', 'substituting into expressions and formulae', 'substitution')
t21.fixed('C1', (1, 2), [
    ('What is the value of 5x² when x = 3?', '45', '5 × 3² = 5 × 9 = 45 (square first). [1]', ['225', '30', '15']),
    ('What is the value of −x² when x = −4?', '−16', '−(−4)² = −(16) = −16. [1]', ['16', '8', '−8']),
    ('What is the value of (2y)² when y = 5?', '100', '(2 × 5)² = 10² = 100. [1]', ['50', '20', '25']),
    ('Work out the value of a² + b² when a = −3 and b = 2.', '13', '(−3)² + 2² = 9 + 4 = 13. B1 [1]'),
    ('Write down the value of 7 − 2n when n = −3.', '13', '7 − 2(−3) = 7 + 6 = 13. B1 [1]'),
])
t21.fixed('C2', (2, 3), [
    ('Explain why the value of x² + 1 can never be negative.', 'x² is never negative (a square of a positive or negative number is positive or zero), so x² + 1 is at least 1.', 'B1 x² ≥ 0; B1 so x² + 1 ≥ 1. [2]'),
    ('A formula is A = ½bh. Explain what happens to A when b is doubled and h stays the same.', 'A doubles, because A is b multiplied by a fixed number (½h).', 'B1 A doubles; B1 reason: A is proportional to b. [2]'),
    ('Explain why 3x² and (3x)² have different values when x = 2.', '3x² = 3 × 4 = 12 (only x is squared) but (3x)² = 6² = 36 (the whole of 3x is squared).', 'B1 each value with the order of operations explained. [2]'),
])

FORMULAE = [
    ('v = u + at', 'v', ['u', 'a', 't'], lambda u, a, t: u + a * t, 'v = {u} + {a} × {t}'),
    ('s = ut + ½at²', 's', ['u', 'a', 't'], lambda u, a, t: u * t + Fr(1, 2) * a * t * t, 's = {u} × {t} + ½ × {a} × {t}²'),
    ('P = 2(l + w)', 'P', ['l', 'w'], lambda l, w: 2 * (l + w), 'P = 2({l} + {w})'),
    ('A = ½(a + b)h', 'A', ['a', 'b', 'h'], lambda a, b, h: Fr(1, 2) * (a + b) * h, 'A = ½({a} + {b}) × {h}'),
    ('F = 1.8C + 32', 'F', ['C'], lambda C: Fr(9, 5) * C + 32, 'F = 1.8 × {C} + 32'),
    ('y = mx + c', 'y', ['m', 'x', 'c'], lambda m, x, c: m * x + c, 'y = {m} × {x} + {c}'),
    ('T = 3p² − 2q', 'T', ['p', 'q'], lambda p, q: 3 * p * p - 2 * q, 'T = 3 × {p}² − 2 × {q}'),
    ('E = ½mv²', 'E', ['m', 'v'], lambda m, v: Fr(1, 2) * m * v * v, 'E = ½ × {m} × {v}²'),
    ('W = (a − b)/c', 'W', ['a', 'b', 'c'], None, 'W = ({a} − {b}) ÷ {c}'),
]


def _vals(r, D, names):
    out = {}
    for n in names:
        if D <= 1:
            out[n] = r.randint(2, 9)
        elif D == 2:
            out[n] = r.choice([v for v in range(-6, 10) if v not in (0, 1)])
        elif D == 3:
            out[n] = r.choice([v for v in range(-9, 13) if v not in (0, 1)])
        else:
            out[n] = r.choice([Fr(v, 2) for v in range(-9, 15) if v not in (0, 2)] + [r.randint(-12, 15) or 3])
    return out


@t21.add('C3', (1, 2, 3, 4, 5))
def t21_formula(r, D):
    for _ in range(30):
        f, subj, names, fn, sub = r.choice(FORMULAE)
        v = _vals(r, D, names)
        if fn is None:
            c = r.choice([2, 3, 4, 5])
            a = r.randint(-10, 20)
            b = a - c * r.randint(-5, 6)
            v = {'a': a, 'b': b, 'c': c}
            val = Fr(a - b, c)
        else:
            val = Fr(fn(*[v[n] for n in names]))
        if val.denominator <= 2 and abs(val) < 2000:
            break
    shown = ', '.join(f'{n} = {N(float(v[n])) if isinstance(v[n], Fr) else N(v[n])}' for n in names)
    vs = {n: par(float(v[n]) if isinstance(v[n], Fr) else v[n]) for n in names}
    ans = N(float(val)) if val.denominator != 1 else N(int(val))
    stem = r.choice([f'Use the formula {f} to work out the value of {subj} when {shown}.', f'{f}. Work out {subj} when {shown}.', f'Calculate the value of {subj} in the formula {f} when {shown}.'])
    key = f'Substitution {sub.format(**vs)} (M1); {subj} = {ans} (A1).'
    if D == 1:
        return MCQ(r, stem, ans, [N(float(val) + 2), N(float(val) * 2), N(float(val) - 1), N(-float(val))], key)
    return Q(stem, ans, key)


@t21.add('C1', (1, 2, 3))
def t21_quick(r, D):
    a, b = r.randint(2, 9), r.randint(2, 9)
    x = r.choice([-5, -4, -3, -2, 2, 3, 4, 5]) if D > 1 else r.randint(2, 6)
    form = r.choice(['ax2', 'a-bx', 'x3'])
    if form == 'ax2':
        e, val, w = f'{a}x²', a * x * x, [(a * x) ** 2, 2 * a * x, -a * x * x]
    elif form == 'a-bx':
        e, val, w = f'{a} − {b}x', a - b * x, [a + b * x, (a - b) * x, b * x - a]
    else:
        e, val, w = f'x³ + {a}', x ** 3 + a, [3 * x + a, -(x ** 3) + a, x * x + a]
    stem = r.choice([f'What is the value of {e} when x = {N(x)}?', f'Work out {e} when x = {N(x)}.'])
    return MCQ(r, stem, N(val), [N(v) for v in w] + [N(val + 1)], f'Substitute x = {par(x)}: {N(val)}. [1]')


@t21.add('C2', (1, 2, 3, 4), 'explain')
def t21_err(r, D):
    x = -r.randint(2, 7)
    a = r.randint(2, 6)
    p = person(r)
    kind = r.choice(['sq', 'minus', 'order'])
    if kind == 'sq':
        wrong = -a * x * x
        stem = f'{p} works out the value of {a}x² when x = {N(x)} and gets {N(wrong)}. Explain the mistake and give the correct value.'
        ans = f'{p} has treated ({N(x)})² as negative. ({N(x)})² = {x * x}, so {a}x² = {a} × {x * x} = {a * x * x}.'
    elif kind == 'minus':
        c = r.randint(8, 20)
        wrong = c + a * x
        stem = f'{p} substitutes x = {N(x)} into {c} − {a}x and gets {N(wrong)}. Explain the mistake and give the correct value.'
        ans = f'{c} − {a} × ({N(x)}) = {c} + {-a * x} = {c - a * x}; subtracting a negative is adding. {p} has subtracted instead.'
    else:
        b = r.randint(2, 5)
        y = r.randint(2, 6)
        stem = f'{p} says that when y = {y}, the value of {b}y² is {(b * y) ** 2}. Explain the mistake and give the correct value.'
        ans = f'Only y is squared: {b} × {y}² = {b} × {y * y} = {b * y * y}. {p} has worked out ({b}y)².'
    return Q(stem, ans, 'B1 identifies the error; B1 correct value. [2]')


@t21.add('C2', (2, 3, 4), 'explain')
def t21_compare(r, D):
    a, b = r.randint(2, 6), r.randint(1, 9)
    x = r.randint(2, 6)
    p, q = two_people(r)
    v1, v2 = a * x + b, a * (x + b)
    return Q(f'{p} and {q} are given x = {x}. {p} works out {a}x + {b} and {q} works out {a}(x + {b}). {q} says they must get the same answer. Is {q} right? Show working.',
             f'No. {a} × {x} + {b} = {v1} but {a}({x} + {b}) = {a} × {x + b} = {v2}. The bracket means add first, then multiply.',
             'M1 both values; A1 conclusion with reason about the order of operations. [2]')


def _sub_c4(r, D):
    p = person(r)
    a = r.choice([20, 25, 30, 35, 40, 45])
    b = r.choice([0.15, 0.2, 0.25, 0.3, 0.4])
    d = r.choice([80, 120, 150, 200, 240, 300])
    c2 = r.choice([10, 15]) + a
    b2 = round(b - 0.05, 2)
    cost = a + b * d
    target = a + b * r.choice([100, 160, 220, 260, 400])
    intro = f'A company in {city(r)} hires out cars. The cost, C dollars, of hiring a car and driving d km is given by the formula C = {a} + {N(b)}d.'
    brk = (c2 - a) / (b - b2)
    parts = [
        lambda r: (f'Work out the cost when {p} drives {d} km.', money(cost), f'M1 {a} + {N(b)} × {d}; A1 {money(cost)} [2]'),
        lambda r: (f'Another customer pays {money(target)}. Work out how far they drove.', f'{N((target - a) / b)} km', f'M1 {N(target)} − {a} = {N(b)}d; A1 {N((target - a) / b)} km [2]'),
        lambda r: ('Explain what the number ' + str(a) + ' represents in the formula.', f'A fixed charge of ${a} paid however far you drive.', 'B1 [1]'),
        lambda r: (f'A second company uses C = {c2} + {N(b2)}d. Find the distance for which the two companies charge the same.', f'{N(brk)} km',
                   f'M1 {a} + {N(b)}d = {c2} + {N(b2)}d; M1 {N(round(b - b2, 2))}d = {c2 - a}; A1 {N(brk)} km [3]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t21.add('C4', (2, 3, 4, 5), 'multi_step')(_sub_c4)


@t21.add('C4', (3, 4, 5), 'multi_step')
def t21_kinematic(r, D):
    u = r.randint(2, 12)
    a = r.choice([-3, -2, 2, 3, 4, 1.5, 2.5])
    t = r.randint(2, 8)
    v = u + a * t
    s = u * t + 0.5 * a * t * t
    return Q(f'The formulae v = u + at and s = ut + ½at² describe the motion of a cyclist. u = {u}, a = {N(a)} and t = {t}. (a) Work out v. (b) Work out s. (c) Show that s = ½(u + v)t gives the same value of s.',
             f'(a) {N(v)} (b) {N(s)} (c) ½({u} + {par(v)}) × {t} = {N(0.5 * (u + v) * t)}, the same.',
             f'(a) M1 {u} + {par(a)} × {t}; A1 {N(v)} [2] (b) M1 {u} × {t} + ½ × {par(a)} × {t}²; A1 {N(s)} [2] (c) B1 substitution giving {N(s)} [1]', marks=5)


# ----------------------------------------------------------- constructing expressions
t22 = topic('Constructing expressions and formulae', 'constructing expressions and formulae', 'constructing formulae')
WORDS = [
    ('multiply n by {a} and then subtract {b}', lambda a, b: lin(a, -b, 'n'), lambda a, b: [f'{a}(n {MINUS} {b})', lin(b, -a, 'n'), f'n {MINUS} {a * b}']),
    ('subtract {b} from n and then multiply by {a}', lambda a, b: f'{a}(n {MINUS} {b})', lambda a, b: [lin(a, -b, 'n'), f'{b} {MINUS} {a}n', f'{a}n {MINUS} {b}n']),
    ('add {b} to n and then divide by {a}', lambda a, b: f'(n + {b})/{a}', lambda a, b: [f'n + {b}/{a}', f'{a}(n + {b})', f'n/{a} + {b}']),
    ('square n and then add {a}', lambda a, b: f'n² + {a}', lambda a, b: [f'(n + {a})²', f'2n + {a}', f'{a}n²']),
    ('add {a} to n and then square the result', lambda a, b: f'(n + {a})²', lambda a, b: [f'n² + {a}', f'n² + {a * a}', f'2(n + {a})']),
    ('multiply n by itself and then multiply by {a}', lambda a, b: f'{a}n²', lambda a, b: [f'({a}n)²', f'{2 * a}n', f'n² + {a}']),
]


@t22.add('C1', (1, 2, 3))
def t22_words(r, D):
    w, f, ds = r.choice(WORDS)
    a, b = r.randint(2, 9), r.randint(2, 9)
    if a == b:
        b += 1
    stem = r.choice([f'Which expression means "{w.format(a=a, b=b)}"?', f'I think of a number n. I {w.format(a=a, b=b)}. Which expression shows my answer?'])
    return MCQ(r, stem, f(a, b), ds(a, b), f'Follow the order of the words: {f(a, b)}. [1]')


@t22.add('C1', (1, 2, 3))
def t22_ages(r, D):
    p, q = two_people(r)
    a = r.randint(2, 9)
    k = r.choice([2, 3, 4])
    kind = r.choice(['older', 'times', 'sum'])
    if kind == 'older':
        stem, ans, ds = f'{p} is x years old. {q} is {a} years older than {p}. Write an expression for {q}\'s age in {k} years\' time.', f'x + {a + k}', [f'x + {a}', f'{k}x + {a}', f'x {MINUS} {a} + {k}']
    elif kind == 'times':
        stem, ans, ds = f'A pen costs p cents and a book costs {k} times as much. Write an expression for the cost of {a} books and one pen.', f'{a * k}p + p = {a * k + 1}p', [f'{a + k}p', f'{a}p + {k}', f'{a * k}p']
        ans = f'{a * k + 1}p'
    else:
        stem, ans, ds = f'There are b boys and g girls in a club. Each child pays ${a}. Write an expression for the total amount paid.', f'{a}(b + g)', [f'{a}b + g', f'b + g + {a}', f'{a}bg']
    return MCQ(r, stem, ans, ds, f'{ans}. [1]')


@t22.add('C2', (1, 2, 3, 4), 'explain')
def t22_err(r, D):
    a, b = r.randint(2, 9), r.randint(5, 30)
    p = person(r)
    kind = r.choice(['ticket', 'perim', 'avg'])
    if kind == 'ticket':
        stem = f'Tickets for a concert cost ${a} each and there is a booking fee of ${b} per order. {p} writes the formula for the cost of an order of n tickets as C = n + {a} + {b}. Explain what is wrong and write the correct formula.'
        ans = f'The ticket price must be multiplied by n: C = {a}n + {b}.'
    elif kind == 'perim':
        stem = f'A rectangle has length (x + {a}) cm and width x cm. {p} says the perimeter is 2x + {a} cm. Explain the mistake and give the correct expression.'
        ans = f'{p} has added one length and one width only. Perimeter = 2(x + {a}) + 2x = 4x + {2 * a} cm.'
    else:
        stem = f'{p} says the mean of the three numbers x, x + {a} and x + {2 * a} is x + {a}/3. Explain the mistake and give the correct mean.'
        ans = f'The whole total must be divided by 3: (3x + {3 * a}) ÷ 3 = x + {a}.'
    return Q(stem, ans, 'B1 identifies the error; B1 correct expression or formula. [2]')


@t22.add('C3', (1, 2, 3, 4, 5))
def t22_formula(r, D):
    p = person(r)
    a, b, c = r.randint(3, 15), r.randint(2, 9), r.randint(10, 40)
    kind = r.choice(['tickets', 'bike', 'phone', 'tiles', 'taxi'])
    if kind == 'tickets':
        stem = f'Adult tickets for a museum in {city(r)} cost ${a} and child tickets cost ${b}. Write a formula for the total cost, T dollars, of x adult tickets and y child tickets.'
        ans, key = f'T = {a}x + {b}y', f'B1 {a}x + {b}y; B1 complete formula with T =.'
    elif kind == 'bike':
        stem = f'A bike hire shop charges ${c} plus ${b} for each hour. Write a formula for the cost, C dollars, of hiring a bike for h hours.'
        ans, key = f'C = {c} + {b}h', f'B1 {b}h; B1 C = {c} + {b}h.'
    elif kind == 'phone':
        stem = f'{p} pays ${c} a month for a phone plus {b} cents for each text. Write a formula for the monthly cost, M dollars, when {p} sends t texts.'
        ans, key = f'M = {c} + {N(b / 100)}t', f'B1 converts {b} cents to ${N(b / 100)}; B1 M = {c} + {N(b / 100)}t.'
    elif kind == 'tiles':
        stem = f'A pattern is made from tiles. Pattern n has {a} tiles in each of n rows plus {b} extra tiles. Write a formula for the total number of tiles, T, in pattern n.'
        ans, key = f'T = {a}n + {b}', f'B1 {a}n; B1 T = {a}n + {b}.'
    else:
        stem = f'A taxi in {city(r)} charges ${b} to start and then {money(a / 10)} per kilometre. Write a formula for the fare, F dollars, for a journey of k kilometres, and use it to find the fare for {c} km.'
        ans = f'F = {b} + {N(a / 10)}k; fare = {money(b + a / 10 * c)}'
        key = f'B1 formula; M1 {b} + {N(a / 10)} × {c}; A1 {money(b + a / 10 * c)}.'
    return Q(stem, ans, key)


@t22.add('C3', (2, 3, 4, 5))
def t22_shape(r, D):
    a, b = r.randint(1, 9), r.randint(2, 6)
    shape = r.choice(['tri', 'rect', 'lshape'])
    if shape == 'tri':
        stem = f'The sides of a triangle are x cm, (x + {a}) cm and ({b}x {MINUS} 1) cm. Write an expression, in its simplest form, for the perimeter of the triangle.'
        ans = f'({lin(b + 2, a - 1)}) cm'
        key = f'M1 x + x + {a} + {b}x − 1; A1 {lin(b + 2, a - 1)}.'
    elif shape == 'rect':
        stem = f'A rectangle has length {b}y cm and width (y + {a}) cm. Write expressions for (a) the perimeter and (b) the area of the rectangle. Simplify your answers.'
        ans = f'(a) ({lin(2 * b + 2, 2 * a, "y")}) cm (b) ({poly((b, "y²"), (a * b, "y"))}) cm²'
        key = f'(a) M1 2({b}y + y + {a}); A1 {lin(2 * b + 2, 2 * a, "y")} (b) M1 {b}y(y + {a}); A1 {poly((b, "y²"), (a * b, "y"))}.'
    else:
        stem = f'A square of side x cm has a square of side {a} cm cut from one corner. Write an expression for the area of the shape that is left, and find its value when x = {a + b + 3}.'
        ans = f'x² {MINUS} {a * a}; {(a + b + 3) ** 2 - a * a} cm²'
        key = f'B1 x² − {a * a}; M1 substitution {(a + b + 3)}² − {a * a}; A1 {(a + b + 3) ** 2 - a * a}.'
    return Q(stem, ans, key)


def _con_c4(r, D):
    a, b = r.randint(2, 6), r.randint(1, 8)
    x = r.randint(4, 15)
    P = (2 * a + 2) * x + 2 * b
    c = r.choice([5, 8, 12, 15])
    intro = f'A rectangular field has length ({a}x + {b}) m and width x m.'
    parts = [
        lambda r: ('Write an expression for the perimeter of the field. Simplify your answer.', f'({lin(2 * a + 2, 2 * b)}) m', f'M1 2({a}x + {b}) + 2x; A1 {lin(2 * a + 2, 2 * b)} [2]'),
        lambda r: (f'The perimeter is {P} m. Form and solve an equation to find x.', f'x = {mixed(x)}', f'M1 {lin(2 * a + 2, 2 * b)} = {P}; A1 x = {mixed(x)} [2]'),
        lambda r: ('Write an expression for the area of the field.', f'x({a}x + {b}) = ({poly((a, "x²"), (b, "x"))}) m²', 'B1 [1]'),
        lambda r: (f'Fencing costs ${c} per metre. Write a formula for the total cost, C dollars, of fencing the field.', f'C = {c}({lin(2 * a + 2, 2 * b)}) = {lin(c * (2 * a + 2), c * 2 * b)}', f'M1 {c} × perimeter; A1 [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t22.add('C4', (2, 3, 4, 5), 'multi_step')(_con_c4)


@t22.add('C4', (2, 3, 4, 5), 'multi_step')
def t22_consec(r, D):
    k = r.choice([3, 5])
    p = person(r)
    tot = r.choice([45, 60, 75, 90, 105, 120, 135, 150]) if k == 3 else r.choice([55, 65, 85, 95, 115, 135, 145])
    n = tot // k - (k // 2)
    terms = ' + '.join(['n'] + [f'(n + {i})' for i in range(1, k)])
    simple = f'{k}n + {k * (k - 1) // 2}'
    fact = f'{k}(n + {(k - 1) // 2})'
    intro = f'{p} adds {k} consecutive whole numbers. The smallest number is n.'
    parts = [
        lambda r: (f'Write an expression, in its simplest form, for the sum of the {k} numbers.', simple, f'M1 {terms}; A1 {simple} [2]'),
        lambda r: (f'Show that the sum is always a multiple of {k}.', f'{simple} = {fact}, which has a factor of {k}.', f'M1 factorises; A1 conclusion [2]'),
        lambda r: (f'The sum is {tot}. Find the {k} numbers.', ', '.join(str(n + i) for i in range(k)), f'M1 {simple} = {tot}; A1 n = {n} and all numbers [2]'),
        lambda r: (f'{p} says the sum of {k} consecutive numbers can be {tot + 1}. Explain why {p} is wrong.', f'{tot + 1} is not a multiple of {k}.', 'B1 [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t22.fixed('C2', (2, 3), [
    ('Explain the difference between an expression and a formula. Give an example of each.', 'An expression has no equals sign, e.g. 3x + 2. A formula shows how one variable is calculated from others, e.g. A = lw.', 'B1 difference; B1 correct examples. [2]'),
    ('A shop sells pens at p cents each. Explain why the cost in dollars of 12 pens is 0.12p, not 12p.', '12 pens cost 12p cents; there are 100 cents in a dollar, so 12p ÷ 100 = 0.12p dollars.', 'B1 12p cents; B1 ÷ 100. [2]'),
])
t22.fixed('C1', (1, 2), [
    ('Which of these is a formula? 3x + 2, A = lw, 5n − 1 = 9, 2(a + b)', 'A = lw', 'A formula links variables with an equals sign; 5n − 1 = 9 is an equation with one unknown. [1]', ['3x + 2', '5n − 1 = 9', '2(a + b)']),
    ('A square has side length s cm. Write a formula for its perimeter P cm.', 'P = 4s', 'B1 [1]'),
    ('Write an expression for the number of minutes in h hours.', '60h', 'B1 [1]'),
])


# ----------------------------------------------------------- expanding two brackets
t23 = topic('Expanding the product of two linear expressions', 'expanding the product of two linear expressions', 'expanding brackets')


def quad(a, b, c, v='x'):
    return poly((a, f'{v}²'), (b, v), (c, ''))


def br(a, b, v='x'):
    return f'({lin(a, b, v)})'


@t23.add('C1', (1, 2, 3))
def t23_mcq(r, D):
    a = r.choice([v for v in range(-7, 9) if v != 0])
    b = r.choice([v for v in range(-7, 9) if v != 0])
    if D == 1:
        a, b = abs(a), abs(b)
    e = f'{br(1, a)}{br(1, b)}'
    ans = quad(1, a + b, a * b)
    stem = r.choice([f'Expand and simplify {e}.', f'Which of these is the expansion of {e}?'])
    return MCQ(r, stem, ans, [quad(1, a * b, a + b), quad(1, 0, a * b), quad(1, a + b, a + b), quad(1, a - b, -a * b), quad(1, -(a + b), a * b)],
               f'x × x + {par(a)}x + {par(b)}x + {par(a)} × {par(b)} = {ans}. [1]')


@t23.add('C3', (1, 2, 3, 4, 5))
def t23_expand(r, D):
    v = r.choice(['x', 'y', 'n', 'a', 't'])
    nz = [x for x in range(-9, 10) if x != 0]
    if D <= 2:
        p, q = 1, 1
        a, b = r.choice(nz), r.choice(nz)
    elif D == 3:
        p, q = r.choice([1, 2, 3]), r.choice([2, 3, 4, 5])
        a, b = r.choice(nz), r.choice(nz)
    else:
        p, q = r.choice([2, 3, 4, -2]), r.choice([2, 3, 5, -3])
        a, b = r.choice(nz), r.choice(nz)
    sq = D >= 3 and r.random() < 0.3
    if sq:
        q, b = p, a
        e = f'{br(p, a, v)}²'
    else:
        e = f'{br(p, a, v)}{br(q, b, v)}'
    ans = quad(p * q, p * b + q * a, a * b, v)
    if D == 5:
        c = r.choice(nz)
        e2 = f'{e} {MINUS} {br(1, c, v)}²'
        ans = quad(p * q - 1, p * b + q * a - 2 * c, a * b - c * c, v)
        return Q(f'Expand and simplify {e2}.', ans, f'M1 expands first product to {quad(p * q, p * b + q * a, a * b, v)}; M1 {br(1, c, v)}² = {quad(1, 2 * c, c * c, v)}; A1 {ans}.')
    return Q(r.choice([f'Expand and simplify {e}.', f'Multiply out the brackets and simplify: {e}.']), ans,
             f'Four products: {N(p * q)}{v}², {N(p * b)}{v}, {N(q * a)}{v}, {N(a * b)} (M1); collect like terms: {ans} (A1).')


@t23.add('C2', (1, 2, 3, 4), 'explain')
def t23_sq_err(r, D):
    a = r.randint(2, 9)
    v = r.choice(['x', 'y', 'n', 'm'])
    p = person(r)
    sgn = r.choice([1, -1]) if D >= 2 else 1
    e = f'({v} {"+" if sgn > 0 else MINUS} {a})²'
    kind = r.choice(['sq', 'check'])
    right = quad(1, 2 * a * sgn, a * a, v)
    if kind == 'sq':
        return Q(f'{p} says that {e} = {v}² {"+" if sgn > 0 else MINUS} {a * a}. Explain why {p} is wrong and give the correct expansion.',
                 f'{e} = ({lin(1, sgn * a, v)})({lin(1, sgn * a, v)}); {p} has missed the two middle terms. Correct: {right}.',
                 'B1 explains missing middle terms (or shows a counter-example); B1 correct expansion. [2]')
    x = r.randint(1, 5)
    return Q(f'{p} says that {e} = {v}² {"+" if sgn > 0 else MINUS} {a * a}. Substitute {v} = {x} into both sides to show that {p} is wrong.',
             f'Left: ({x} {"+" if sgn > 0 else MINUS} {a})² = {(x + sgn * a) ** 2}. Right: {x * x} {"+" if sgn > 0 else MINUS} {a * a} = {N(x * x + sgn * a * a)}. They are different.',
             'M1 both values; A1 conclusion. [2]')


@t23.add('C2', (2, 3, 4), 'explain')
def t23_sign(r, D):
    a, b = r.randint(2, 9), r.randint(2, 9)
    v = 'x'
    p = person(r)
    wrong = quad(1, a + b, -a * b)
    right = quad(1, b - a, -a * b)
    return Q(f'{p} expands (x {MINUS} {a})(x + {b}) and gets {wrong}. Find {p}\'s mistake and write the correct answer.',
             f'The x terms are −{a}x and +{b}x, which give {lin(b - a, 0) if b != a else "0"}, not +{a + b}x. Correct: {right}.',
             'B1 identifies sign error in the x term; B1 correct expansion. [2]')


@t23.add('C3', (2, 3, 4, 5))
def t23_fill(r, D):
    a, b = r.randint(1, 9), r.randint(1, 9)
    s, pr = a + b, a * b
    if D >= 4:
        a = -a
        s, pr = a + b, a * b
    return Q(f'{br(1, a)}(x + p) = {quad(1, s, 0)} + q. Find the values of p and q.', f'p = {b}, q = {N(pr)}',
             f'M1 expands to x² + ({N(a)} + p)x + {par(a)}p, so {N(a)} + p = {N(s)}; A1 p = {b}; A1 q = {par(a)} × {b} = {N(pr)}.')


def _area_c4(r, D):
    a, b = r.randint(2, 7), r.randint(1, 6)
    xv = r.randint(3, 9)
    intro = r.choice([f'A rectangle has length (x + {a}) cm and width (x + {b}) cm.', f'A rectangular photo measures (x + {a}) cm by (x + {b}) cm.'])
    area = quad(1, a + b, a * b)
    parts = [
        lambda r: ('Show that the area of the rectangle is (' + area + ') cm².', f'(x + {a})(x + {b}) = x² + {b}x + {a}x + {a * b} = {area}', 'M1 four products; A1 simplified [2]'),
        lambda r: (f'Work out the area when x = {xv}.', f'{(xv + a) * (xv + b)} cm²', f'M1 substitution; A1 {(xv + a) * (xv + b)} [2]'),
        lambda r: ('A square of side x cm is cut out of the rectangle. Write an expression for the area that is left.', f'({lin(a + b, a * b)}) cm²', f'M1 {area} − x²; A1 {lin(a + b, a * b)} [2]'),
        lambda r: (f'The length and width are both increased by 1 cm. Find, in terms of x, how much the area increases.', f'({lin(2, a + b + 1)}) cm²',
                   f'M1 (x + {a + 1})(x + {b + 1}) − ({area}); A1 {lin(2, a + b + 1)} [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t23.add('C4', (2, 3, 4, 5), 'multi_step')(_area_c4)


@t23.add('C4', (3, 4, 5), 'multi_step')
def t23_proof(r, D):
    k = r.choice([1, 2, 3])
    p = person(r)
    if k == 1:
        return Q(f'{p} says: "If you multiply two numbers that differ by 2, the answer is always 1 less than the square of the number in between." Let the numbers be (n − 1) and (n + 1). Prove that {p} is right, and check with n = {r.randint(4, 12)}.',
                 '(n − 1)(n + 1) = n² − n + n − 1 = n² − 1, which is 1 less than n².', 'M1 expansion; A1 n² − 1; B1 numerical check; B1 conclusion. [4]', marks=4)
    if k == 2:
        a = r.randint(2, 6)
        return Q(f'Show that (n + {a})² − (n − {a})² = {4 * a}n, and hence explain why the answer is always a multiple of 4 when n is a whole number.',
                 f'(n² + {2 * a}n + {a * a}) − (n² − {2 * a}n + {a * a}) = {4 * a}n = 4 × {a}n, so it is a multiple of 4.', f'M1 expands both squares; M1 subtracts correctly; A1 {4 * a}n; B1 reason 4 × {a}n. [4]', marks=4)
    a = r.randint(1, 5)
    return Q(f'Show that (2n + {a})² − (2n)² is always an odd number when n is a whole number.', f'(2n + {a})² − 4n² = {4 * a}n + {a * a}. {4 * a}n is even and {a * a} is {"odd" if a % 2 else "even"}, so the result is {"odd" if a % 2 else "even"}.' if a % 2 else
             f'= {4 * a}n + {a * a}; this is even, so the statement is false for a = {a}.', 'M1 expansion; A1 simplified; B1 parity argument. [3]', marks=3) if a % 2 else None


t23.fixed('C1', (1, 2), [
    ('How many terms are there in the expansion of (x + 3)(x + 5) before you collect like terms?', '4', 'x², 5x, 3x, 15: four products. [1]', ['2', '3', '5']),
    ('What is the coefficient of x in the expansion of (x + 4)(x − 7)?', '−3', '4x − 7x = −3x. [1]', ['3', '−28', '11']),
    ('What is the constant term in the expansion of (x − 6)(x − 2)?', '12', '(−6) × (−2) = 12. [1]', ['−12', '−8', '8']),
    ('Expand x(x + 9).', 'x² + 9x', 'B1 [1]'),
])


# ----------------------------------------------------------- factorising
t24 = topic('Factorising by taking out common factors', 'factorising by taking out common factors', 'factorising')


def _fac_terms(r, D):
    vs = ['x', 'y', 'a', 'b', 'p', 'm']
    v, w = r.sample(vs, 2)
    h = r.choice([2, 3, 4, 5, 6, 7, 8])
    c1, c2 = r.sample([1, 2, 3, 5, 7], 2)
    if D <= 1:
        return f'{h * c1}{v} + {h * c2}', f'{h}({lin(c1, c2, v)})', h, v
    if D == 2:
        return f'{h * c1}{v} {MINUS} {h * c2}{v}{w}', f'{h}{v}({c1} {MINUS} {c2}{w})'.replace('(1 ', '(1 '), h, v
    if D == 3:
        return f'{h * c1}{v}² + {h * c2}{v}', f'{h}{v}({lin(c1, c2, v)})', h, v
    return f'{h * c1}{v}²{w} + {h * c2}{v}{w}²', f'{h}{v}{w}({poly((c1, v), (c2, w))})', h, v


def _clean1(s):
    return s.replace('(1x', '(x').replace(' 1x', ' x').replace('(1y', '(y').replace(' 1y', ' y')


@t24.add('C3', (1, 2, 3, 4, 5))
def t24_fac(r, D):
    e, ans, h, v = _fac_terms(r, min(D, 4))
    ans = _clean1(ans)
    stem = r.choice([f'Factorise completely {e}.', f'Factorise fully: {e}.', f'Write {e} as a product of factors.'])
    key = f'Highest common factor taken out (M1); {ans} (A1).'
    if D == 5:
        a, b, c = r.choice([(6, 9, 12), (4, 10, 14), (8, 12, 20), (10, 15, 25), (9, 12, 15)])
        g = math.gcd(a, math.gcd(b, c))
        e = f'{a}x³ + {b}x² {MINUS} {c}x'
        ans = f'{g}x({poly((a // g, "x²"), (b // g, "x"), (-c // g, ""))})'
        return Q(f'Factorise completely {e}.', _clean1(ans), f'HCF {g}x (M1); {_clean1(ans)} (A1).')
    if D == 1:
        h2 = h * 2
        c1, c2 = [int(x) if x.isdigit() else 1 for x in ans[len(str(h)) + 1:-1].replace(v, '').split(' + ')]
        return MCQ(r, stem, ans, [_clean1(f'{h}({c1}{v} + {h * c2})'), _clean1(f'{h}{v}({c1} + {c2})'), _clean1(f'{h * c1}({v} + {c2})'), _clean1(f'2({lin(h * c1 // 2, h * c2 // 2, v)})') if h % 2 == 0 and h > 2 else _clean1(f'{h}({c1}{v} + {c2 + 1})')], key)
    return Q(stem, ans, key)


@t24.add('C1', (1, 2, 3))
def t24_hcf(r, D):
    v = r.choice(['x', 'y', 'a'])
    h = r.choice([2, 3, 4, 5, 6])
    c1, c2 = r.sample([2, 3, 5, 7], 2)
    if D >= 2:
        t1, t2, ans = f'{h * c1}{v}²', f'{h * c2}{v}', f'{h}{v}'
        ds = [f'{h}', f'{h}{v}²', f'{h * c1 * c2}{v}', v]
    else:
        t1, t2, ans = f'{h * c1}{v}', f'{h * c2}', f'{h}'
        ds = [f'{h}{v}', f'{h * c1}', f'{h * c1 * h * c2}', '1']
    return MCQ(r, f'What is the highest common factor of {t1} and {t2}?', ans, ds, f'HCF of the numbers is {h}; ' + (f'both terms contain {v}.' if D >= 2 else 'only one term contains the letter.') + ' [1]')


@t24.add('C2', (1, 2, 3, 4), 'explain')
def t24_notfull(r, D):
    v = r.choice(['x', 'y', 'n'])
    h = r.choice([4, 6, 8, 9, 10, 12])
    c1, c2 = r.sample([1, 2, 3, 5], 2)
    small = [d for d in range(2, h) if h % d == 0]
    s = r.choice(small)
    p = person(r)
    if D >= 3:
        e = f'{h * c1}{v}² + {h * c2}{v}'
        partial = f'{s}({h * c1 // s}{v}² + {h * c2 // s}{v})'
        full = _clean1(f'{h}{v}({lin(c1, c2, v)})')
    else:
        e = f'{h * c1}{v} + {h * c2}'
        partial = f'{s}({h * c1 // s}{v} + {h * c2 // s})'
        full = _clean1(f'{h}({lin(c1, c2, v)})')
    return Q(f'{p} factorises {e} and writes {partial}. Explain why this is not fully factorised, and factorise it completely.',
             f'The terms inside the bracket still have a common factor. Fully factorised: {full}.',
             'B1 bracket still has a common factor; B1 correct full factorisation. [2]')


@t24.add('C2', (2, 3, 4), 'explain')
def t24_check(r, D):
    v = 'x'
    h = r.choice([3, 4, 5, 6])
    c1, c2 = r.sample([2, 3, 5, 7], 2)
    e = f'{h * c1}x + {h * c2}'
    wrong_c2 = c2 + r.choice([1, -1, h])
    p = person(r)
    return Q(f'{p} factorises {e} as {h}({c1}x + {wrong_c2}). Explain how expanding the brackets shows whether {p} is correct.',
             f'{h}({c1}x + {wrong_c2}) = {h * c1}x + {h * wrong_c2}, not {e}, so {p} is wrong. Correct: {h}({c1}x + {c2}).',
             'M1 expands the answer; A1 conclusion with correct factorisation. [2]')


def _fac_c4(r, D):
    h = r.choice([2, 3, 4, 5])
    a = r.randint(2, 6)
    intro = r.choice([f'The area of a rectangle is ({h * a}x² + {h}x) cm². Its width is {h}x cm.', f'A rectangle has area ({h}x² + {h * a}x) cm² and width x cm.'])
    if 'width is' in intro:
        L = lin(a, 1)
        parts = [lambda r: ('Factorise the expression for the area.', f'{h}x({L})', 'M1 HCF; A1 [2]'),
                 lambda r: ('Write down an expression for the length.', f'({L}) cm', 'B1 [1]'),
                 lambda r: ('Find an expression for the perimeter, in its simplest form.', f'({lin(2 * h + 2 * a, 2)}) cm', f'M1 2({h}x) + 2({L}); A1 [2]')]
    else:
        L = lin(h, h * a)
        parts = [lambda r: ('Factorise the expression for the area completely.', f'{h}x(x + {a})', 'M1; A1 [2]'),
                 lambda r: ('Write down an expression for the length.', f'({L}) cm', 'B1 [1]'),
                 lambda r: (f'Find the area when x = {a + 1}.', f'{h * (a + 1) ** 2 + h * a * (a + 1)} cm²', 'M1 substitution; A1 [2]')]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t24.add('C4', (2, 3, 4, 5), 'multi_step')(_fac_c4)


@t24.add('C4', (2, 3, 4, 5), 'multi_step')
def t24_even(r, D):
    k = r.choice([2, 4])
    p = person(r)
    a = r.choice([3, 5, 7]) if k == 2 else r.choice([6, 10, 14])
    nn = r.randint(3, 9)
    intro = f'{p} is investigating the expression {k * a}n + {k * 3} where n is a whole number.'
    parts = [
        lambda r: ('Factorise the expression completely.', f'{math.gcd(k * a, k * 3)}({k * a // math.gcd(k * a, k * 3)}n + {k * 3 // math.gcd(k * a, k * 3)})', 'M1; A1 [2]'),
        lambda r: (f'Use your factorisation to explain why the value is always a multiple of {math.gcd(k * a, k * 3)}.', f'It is {math.gcd(k * a, k * 3)} × a whole number.', 'B1 [1]'),
        lambda r: (f'Work out the value when n = {nn} and check that it is a multiple of {math.gcd(k * a, k * 3)}.', f'{k * a * nn + k * 3} = {math.gcd(k * a, k * 3)} × {(k * a * nn + k * 3) // math.gcd(k * a, k * 3)}', 'M1 substitution; A1 value shown as a multiple [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t24.fixed('C1', (1, 2), [
    ('What does it mean to factorise an expression?', 'Write it as a product, putting it into brackets with a common factor outside', 'Factorising is the reverse of expanding. [1]',
     ['Multiply out the brackets', 'Collect like terms', 'Substitute numbers for the letters']),
    ('Factorise 7x + 21.', '7(x + 3)', 'HCF is 7. [1]', ['7(x + 21)', '7x(1 + 3)', '3(7x + 7)']),
    ('Factorise x² − 5x.', 'x(x − 5)', 'B1 [1]'),
    ('Factorise 12ab + 18b.', '6b(2a + 3)', 'B1 HCF 6b [1]'),
])
t24.fixed('C2', (2, 3), [
    ('Explain how you can check that a factorisation is correct.', 'Expand the brackets again; you should get back the original expression.', 'B1 expand; B1 compare with the original. [2]'),
    ('Explain why 5x + 7y cannot be factorised.', '5 and 7 have no common factor other than 1, and the terms share no letter.', 'B1 numbers; B1 letters. [2]'),
])


# ----------------------------------------------------------- algebraic fractions
t25 = topic('Simplifying and adding algebraic fractions', 'simplifying and adding algebraic fractions', 'algebraic fractions')


def afr(num, den, v='x'):
    """num: coefficient of v (Fraction allowed) -> 'kx/d' simplified."""
    f = Fr(num, den)
    n, d = f.numerator, f.denominator
    t = (MINUS if n < 0 else '') + (str(abs(n)) if abs(n) != 1 else '') + v
    return t if d == 1 else f'{t}/{d}'


@t25.add('C1', (1, 2, 3))
def t25_add_mcq(r, D):
    a, b = r.sample([2, 3, 4, 5, 6, 7, 8], 2)
    p, q = (1, 1) if D == 1 else (r.randint(1, 4), r.randint(1, 4))
    v = r.choice(['x', 'y', 'a'])
    lhs = f'{(str(p) if p > 1 else "")}{v}/{a} + {(str(q) if q > 1 else "")}{v}/{b}'
    ans = afr(Fr(p, a) + Fr(q, b), 1, v) if (Fr(p, a) + Fr(q, b)).denominator == 1 else afr((Fr(p, a) + Fr(q, b)).numerator, (Fr(p, a) + Fr(q, b)).denominator, v)
    wrong1 = f'{p + q}{v}/{a + b}'
    wrong2 = f'{p + q}{v}/{a * b}'
    wrong3 = f'{v}²/{a * b}' if p == q == 1 else f'{p * q}{v}/{a * b}'
    return MCQ(r, f'Simplify {lhs}.', ans, [wrong1, wrong2, wrong3, f'{p * b + q * a}{v}/{a + b}'],
               f'Common denominator {a * b // math.gcd(a, b)}: {ans}. [1]')


@t25.add('C1', (1, 2, 3))
def t25_cancel(r, D):
    h = r.choice([2, 3, 4, 5, 6])
    a, b = r.sample([1, 2, 3, 5, 7], 2)
    v = r.choice(['x', 'y', 'm'])
    if D >= 2:
        e, ans = f'{h * a}{v}²/{h * b}{v}', afr(a, b, v)
        ds = [afr(a, b, v + '²'), f'{h * a}{v}/{h * b}', afr(a * h, b, v), afr(b, a, v)]
    else:
        e, ans = f'{h * a}{v}/{h * b}', afr(a, b, v)
        ds = [afr(b, a, v), afr(a * h, b, v), f'{a}/{b}', afr(a, b * h, v)]
    return MCQ(r, f'Simplify {e}.', ans, ds, f'Divide numerator and denominator by the common factor {h}{v if D >= 2 else ""}: {ans}. [1]')


@t25.add('C2', (1, 2, 3, 4), 'explain')
def t25_err(r, D):
    a, b = r.sample([2, 3, 4, 5, 7], 2)
    v = r.choice(['x', 'y'])
    p = person(r)
    kind = r.choice(['add', 'cancel']) if D >= 2 else 'add'
    if kind == 'add':
        right = afr((Fr(1, a) + Fr(1, b)).numerator, (Fr(1, a) + Fr(1, b)).denominator, v)
        return Q(f'{p} writes {v}/{a} + {v}/{b} = 2{v}/{a + b}. Explain the mistake and give the correct answer.',
                 f'You cannot add the denominators. Use a common denominator {a * b // math.gcd(a, b)}: {v}/{a} + {v}/{b} = {right}.',
                 'B1 must use a common denominator, not add denominators; B1 correct answer. [2]')
    c = r.randint(2, 9)
    return Q(f'{p} simplifies ({v} + {c})/{c} to {v}. Explain why this is wrong.',
             f'You can only cancel a common factor, not a term. ({v} + {c})/{c} = {v}/{c} + 1; for example {v} = {c} gives 2, not {c}.',
             'B1 only common factors cancel; B1 counter-example or correct form. [2]')


@t25.add('C3', (1, 2, 3, 4, 5))
def t25_combine(r, D):
    p, q = r.sample([2, 3, 4, 5, 6], 2)
    a = r.choice([v for v in range(-6, 8) if v != 0])
    b = r.choice([v for v in range(-6, 8) if v != 0])
    op = '+' if D <= 3 or r.random() < 0.5 else MINUS
    L = p * q // math.gcd(p, q)
    mp, mq = L // p, L // q
    sgn = 1 if op == '+' else -1
    cx = mp + sgn * mq
    cc = mp * a + sgn * mq * b
    num = lin(cx, cc)
    if D <= 1:
        return Q(f'Write x/{p} + x/{q} as a single fraction.', f'{afr(mp + mq, L)}', f'Common denominator {L} (M1); {mp}x/{L} + {mq}x/{L} = {afr(mp + mq, L)} (A1).')
    e = f'({lin(1, a)})/{p} {op} ({lin(1, b)})/{q}'
    return Q(f'Write {e} as a single fraction in its simplest form.', f'({num})/{L}',
             f'Common denominator {L} (M1); numerator {mp}({lin(1, a)}) {op} {mq}({lin(1, b)}) (M1); = ({num})/{L} (A1).')


@t25.add('C3', (2, 3, 4, 5))
def t25_muldiv(r, D):
    a, b, c, d = r.choice([2, 3, 4, 5]), r.choice([3, 5, 7]), r.choice([6, 9, 10, 12]), r.choice([2, 4, 8])
    v = r.choice(['x', 'y'])
    if r.random() < 0.5:
        res = Fr(a * c, b * d)
        return Q(f'Simplify {a}{v}/{b} × {c}/{d}{v}.', fr(res), f'Multiply numerators and denominators: {a * c}{v}/{b * d}{v} (M1); cancel {v}: {fr(res)} (A1).')
    res = Fr(a * d, b * c)
    return Q(f'Simplify {a}{v}/{b} ÷ {c}{v}/{d}.', fr(res), f'Multiply by the reciprocal: {a}{v}/{b} × {d}/{c}{v} (M1); = {fr(res)} (A1).')


def _af_c4(r, D):
    a, b, c = r.sample([2, 3, 4, 5, 6], 3)
    L = a * b * c // math.gcd(a, math.gcd(b, c))
    while L % a or L % b or L % c:
        L += 1
    from math import lcm
    L = lcm(a, b, c)
    s = Fr(1, a) + Fr(1, b) + Fr(1, c)
    P = r.choice([s.numerator * k for k in (2, 3, 4, 6)])
    xv = P / float(s)
    intro = f'The sides of a triangle are x/{a} cm, x/{b} cm and x/{c} cm.'
    parts = [
        lambda r: ('Write an expression for the perimeter as a single fraction.', f'{afr(s.numerator, s.denominator)} cm', f'M1 common denominator {lcm(a, b, c)}; A1 {afr(s.numerator, s.denominator)} [2]'),
        lambda r: (f'The perimeter is {P} cm. Find x.', f'x = {N(xv)}', f'M1 {afr(s.numerator, s.denominator)} = {P}; A1 {N(xv)} [2]'),
        lambda r: ('Write down the length of the longest side in terms of x.', f'x/{min(a, b, c)} cm', 'B1 smallest denominator gives the longest side [1]'),
        lambda r: (f'Find, as a single fraction, how much longer x/{min(a, b, c)} is than x/{max(a, b, c)}.', afr((Fr(1, min(a, b, c)) - Fr(1, max(a, b, c))).numerator, (Fr(1, min(a, b, c)) - Fr(1, max(a, b, c))).denominator), 'M1 subtract with common denominator; A1 [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t25.add('C4', (2, 3, 4, 5), 'multi_step')(_af_c4)


@t25.add('C4', (3, 4, 5), 'multi_step')
def t25_eq(r, D):
    p, q = r.sample([2, 3, 4, 5], 2)
    xv = p * q * r.randint(1, 5)
    a = r.randint(1, 6)
    rhs = Fr(xv + a, p) + Fr(xv, q)
    if rhs.denominator != 1:
        return None
    return Q(f'(a) Write (x + {a})/{p} + x/{q} as a single fraction. (b) Hence solve (x + {a})/{p} + x/{q} = {int(rhs)}.',
             f'(a) ({lin(p + q, q * a)})/{p * q} (b) x = {xv}',
             f'(a) M1 common denominator {p * q}; A1 ({lin(p + q, q * a)})/{p * q} [2] (b) M1 {lin(p + q, q * a)} = {int(rhs) * p * q}; M1 rearrange; A1 x = {xv} [3]', marks=5)


t25.fixed('C1', (1, 2), [
    ('What is the lowest common denominator of x/4 and x/6?', '12', 'LCM of 4 and 6 is 12. [1]', ['24', '10', '2']),
    ('Simplify 3x/3.', 'x', 'B1 [1]'),
    ('Write x/2 − x/5 as a single fraction.', '3x/10', '5x/10 − 2x/10 = 3x/10. B1 [1]'),
])
t25.fixed('C2', (2, 3), [
    ('Explain why x/3 + x/3 = 2x/3 but x/3 × x/3 = x²/9.', 'Adding: same denominator, so add numerators. Multiplying: multiply numerators (x × x = x²) and denominators (3 × 3 = 9).', 'B1 each correct explanation. [2]'),
    ('Explain why 2x/4 and x/2 are equivalent.', 'Dividing numerator and denominator of 2x/4 by 2 gives x/2.', 'B1 common factor 2; B1 conclusion. [2]'),
])

CHAPTERS[2] = [t21, t22, t23, t24, t25]


# =========================================================== 3 Decimals, percentages and rounding
from decimal import Decimal as Dec  # noqa: E402


def dshift(x, e):
    """x × 10^e exactly, formatted."""
    d = Dec(str(x)).scaleb(e).normalize()
    s = format(d, 'f')
    if '.' in s:
        s = s.rstrip('0').rstrip('.')
    return s


t31 = topic('Multiplying and dividing by powers of 10', 'multiplying and dividing by powers of 10', 'powers of 10')
t31.fixed('C1', (1, 2), [
    ('Multiplying by 0.01 gives the same answer as which of these: dividing by 100, multiplying by 100, dividing by 10 or dividing by 0.01?', 'Dividing by 100', '0.01 = 1/100, so × 0.01 = ÷ 100. [1]', ['Multiplying by 100', 'Dividing by 10', 'Dividing by 0.01']),
    ('Write 10⁻² as a decimal.', '0.01', '10⁻² = 1/100 = 0.01. [1]', ['0.001', '−100', '−20']),
    ('Dividing by 10⁻¹ is the same as doing what?', 'Multiplying by 10', '10⁻¹ = 0.1 and ÷ 0.1 = × 10. [1]', ['Dividing by 10', 'Multiplying by 0.1', 'Subtracting 10']),
    ('Write down the value of 4.7 × 10³.', '4700', 'B1 [1]'),
    ('Write down the value of 52 ÷ 10³.', '0.052', 'B1 [1]'),
])
t31.fixed('C2', (2, 3), [
    ('Explain why multiplying a positive number by 10⁻³ makes it smaller.', '10⁻³ = 1/1000, which is less than 1, so multiplying by it gives one thousandth of the number.', 'B1 10⁻³ = 0.001; B1 multiplying by a number less than 1 makes it smaller. [2]'),
    ('Explain why 3.6 ÷ 0.01 = 3.6 × 100.', '0.01 = 1/100; dividing by 1/100 is the same as multiplying by 100, so both give 360.', 'B1 0.01 = 1/100; B1 dividing by a fraction = multiplying by its reciprocal. [2]'),
])

DEC_BASE = [3.7, 0.45, 26.8, 0.072, 5.06, 81.3, 0.9, 412.5, 0.0368, 7.25, 64, 0.508, 1.93]


@t31.add('C1', (1, 2, 3))
def t31_mcq(r, D):
    x = r.choice(DEC_BASE)
    e = r.choice([1, 2, 3]) * (1 if D == 1 else r.choice([1, -1]))
    op = r.choice(['×', '÷'])
    eff = e if op == '×' else -e
    ans = dshift(x, eff)
    stem = f'Work out {N(x)} {op} 10{sup(e)}.' if D >= 2 else f'Work out {N(x)} {op} {10 ** e}.'
    return MCQ(r, stem, ans, [dshift(x, -eff), dshift(x, eff + 1), dshift(x, eff - 1), dshift(x, 2 * eff) if eff else None],
               f'{op} 10{sup(e)} moves the digits {abs(eff)} place{"s" if abs(eff) > 1 else ""} {"left" if eff > 0 else "right"} relative to the decimal point (place value {"increases" if eff > 0 else "decreases"}): {ans}. [1]')


@t31.add('C3', (1, 2, 3, 4, 5))
def t31_calc(r, D):
    x = r.choice(DEC_BASE)
    if D <= 2:
        e = r.choice([2, 3, -1, -2])
        op = r.choice(['×', '÷'])
        eff = e if op == '×' else -e
        return Q(r.choice([f'Work out {N(x)} {op} 10{sup(e)}.', f'Calculate {N(x)} {op} 10{sup(e)} without a calculator.']), dshift(x, eff),
                 f'{op} 10{sup(e)} is the same as {"×" if eff > 0 else "÷"} {10 ** abs(eff)} (M1); {dshift(x, eff)} (A1).')
    if D == 3:
        e = r.choice([2, 3, 4, -2, -3])
        target = dshift(x, e)
        return Q(f'Find the value of n when {N(x)} × 10ⁿ = {target}.', N(e), f'Digits move {abs(e)} places (M1); n = {N(e)} (A1).')
    a, b = r.choice([1, 2, 3]), r.choice([-1, -2, -3])
    y = r.choice(DEC_BASE)
    v = Dec(str(x)).scaleb(a) + Dec(str(y)).scaleb(b)
    s = format(v.normalize(), 'f')
    return Q(f'Work out {N(x)} × 10{sup(a)} + {N(y)} × 10{sup(b)}.', s, f'{dshift(x, a)} + {dshift(y, b)} (M1 each conversion) = {s} (A1).')


@t31.add('C2', (1, 2, 3, 4), 'explain')
def t31_err(r, D):
    x = r.choice(DEC_BASE)
    e = r.randint(1, 3)
    p = person(r)
    if r.random() < 0.5:
        wrong = dshift(x, -e)
        right = dshift(x, e)
        stem = f'{p} says that {N(x)} ÷ 10{sup(-e)} = {wrong}. Explain the mistake and write the correct answer.'
        ans = f'Dividing by 10{sup(-e)} (= {dshift(1, -e)}) is the same as multiplying by 10{sup(e)}, so the answer is {right}.'
    else:
        wrong = dshift(x, e)
        right = dshift(x, -e)
        stem = f'{p} works out {N(x)} × 10{sup(-e)} and gets {wrong}. Is {p} correct? Explain.'
        ans = f'No. 10{sup(-e)} = {dshift(1, -e)}, which is less than 1, so the answer must be smaller than {N(x)}: {right}.'
    return Q(stem, ans, 'B1 explains the meaning of the negative power; B1 correct answer. [2]')


@t31.add('C2', (2, 3, 4), 'explain')
def t31_same(r, D):
    x = r.choice(DEC_BASE)
    a = r.randint(1, 3)
    p, q = two_people(r)
    return Q(f'{p} works out {N(x)} × 10{sup(-a)}. {q} works out {N(x)} ÷ 10{sup(a)}. Will they get the same answer? Explain.',
             f'Yes. 10{sup(-a)} = 1/10{sup(a)}, so multiplying by 10{sup(-a)} is the same as dividing by 10{sup(a)}. Both get {dshift(x, -a)}.',
             'B1 equivalence explained; B1 value. [2]')


def _p10_c4(r, D):
    L = r.choice([2.5, 3.6, 4.8, 0.75, 1.25, 12.5])
    n = r.choice([100, 1000, 10000])
    th = r.choice([0.08, 0.12, 0.25, 0.04])
    intro = f'A factory in {city(r)} makes metal strips that are each {N(L)} m long and {N(th)} mm thick.'
    parts = [
        lambda r: (f'Write the length of one strip in millimetres.', f'{dshift(L, 3)} mm', f'B1 × 10³ [1]'),
        lambda r: (f'Work out the total length of {n:,} strips in kilometres.', f'{dshift(L * n, -3)} km', f'M1 {N(L)} × {n:,} = {N(L * n)} m; A1 ÷ 10³ [2]'),
        lambda r: (f'Write the thickness of a strip in metres, using standard form.', to_sform(th / 1000), f'M1 ÷ 10³; A1 {to_sform(th / 1000)} m [2]'),
        lambda r: (f'Strips are stacked flat on top of each other. Work out the height of a stack of {n:,} strips in centimetres.', f'{dshift(th * n, -1)} cm', f'M1 {N(th)} × {n:,} mm; A1 ÷ 10 [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t31.add('C4', (2, 3, 4, 5), 'multi_step')(_p10_c4)


@t31.add('C4', (3, 4, 5), 'multi_step')
def t31_chain(r, D):
    x = r.choice([0.36, 4.2, 0.075, 18.5, 0.6])
    a, b = r.randint(2, 4), r.randint(1, 3)
    v = Dec(str(x)).scaleb(a - (-b))
    return Q(f'(a) Work out {N(x)} × 10{sup(a)} ÷ 10{sup(-b)}. (b) Write your answer in standard form. (c) Find the value of k if {N(x)} × 10ᵏ = {dshift(x, -4)}.',
             f'(a) {format(v.normalize(), "f")} (b) {to_sform(float(v))} (c) k = −4',
             f'(a) M1 × 10{sup(a)} then × 10{sup(b)}; A1 [2] (b) B1 [1] (c) M1 digits moved 4 places right; A1 k = −4 [2]', marks=5)


# ----------------------------------------------------------- multiplying and dividing decimals
t32 = topic('Multiplying and dividing decimals', 'multiplying and dividing decimals', 'decimals')


def dmul(a, b):
    return format((Dec(str(a)) * Dec(str(b))).normalize(), 'f')


def ddiv(a, b):
    v = (Dec(str(a)) / Dec(str(b))).normalize()
    return format(v, 'f')


@t32.add('C1', (1, 2, 3))
def t32_mcq(r, D):
    a = r.choice([0.3, 0.4, 0.6, 0.7, 0.8, 0.9, 0.2, 0.5])
    b = r.choice([0.04, 0.06, 0.3, 0.7, 0.08, 0.9, 0.02, 0.5]) if D > 1 else r.choice([3, 4, 6, 7, 8, 9])
    ans = dmul(a, b)
    ds = [dmul(a * 10, b), dmul(a, b / 10) if D > 1 else dmul(a / 10, b), dmul(a * 10, b * 10), str(round(a + b, 4))]
    return MCQ(r, f'Work out {N(a)} × {N(b)}.', ans, ds, f'{int(a * 10)} × {N(b * 100) if b < 1 else N(b)} then place the decimal point: {ans}. [1]')


@t32.add('C3', (1, 2, 3, 4, 5))
def t32_calc(r, D):
    if r.random() < 0.5:
        a = r.choice([1.2, 2.4, 3.5, 0.45, 6.3, 0.16, 7.2, 12.5, 0.36])
        b = r.choice([0.3, 0.4, 0.06, 0.8, 1.5, 0.25, 0.7, 2.4]) if D >= 2 else r.choice([3, 4, 6, 8])
        ans = dmul(a, b)
        return Q(r.choice([f'Work out {N(a)} × {N(b)} without a calculator. Show your method.', f'Calculate {N(a)} × {N(b)}. Do not use a calculator.']), ans,
                 f'Ignore decimals: {str(a).replace(".", "").lstrip("0")} × {str(b).replace(".", "").lstrip("0")} (M1); total decimal places → {ans} (A1).')
    q = r.choice([4, 6, 8, 12, 15, 25, 30, 45, 120])
    b = r.choice([0.2, 0.4, 0.5, 0.06, 0.08, 0.3, 0.05, 0.12]) if D >= 2 else r.choice([2, 4, 5])
    a = dmul(q, b)
    return Q(r.choice([f'Work out {a} ÷ {N(b)} without a calculator.', f'Calculate {a} ÷ {N(b)}. Show your method.']), N(q),
             f'Multiply both numbers by {10 ** (len(str(b).split(".")[1]) if "." in str(b) else 0)} so you divide by a whole number (M1): {dshift(a, len(str(b).split(".")[1]) if "." in str(b) else 0)} ÷ {dshift(b, len(str(b).split(".")[1]) if "." in str(b) else 0)} = {q} (A1).')


@t32.add('C2', (1, 2, 3, 4), 'explain')
def t32_err(r, D):
    a, b = r.choice([(0.2, 0.3), (0.4, 0.2), (0.3, 0.3), (0.5, 0.7), (0.6, 0.4), (0.8, 0.3), (0.9, 0.2)])
    p = person(r)
    kind = r.choice(['mul', 'div']) if D >= 2 else 'mul'
    if kind == 'mul':
        wrong = N(round(a * b * 10, 4))
        return Q(f'{p} says {N(a)} × {N(b)} = {wrong}. Explain why {p} must be wrong and give the correct answer.',
                 f'Both numbers are less than 1, so the answer must be less than each of them; {wrong} is too big. {N(a)} × {N(b)} = {dmul(a, b)} (two decimal places).',
                 'B1 reason (estimate / place value); B1 correct answer. [2]')
    x = r.choice([12, 24, 36, 4.8, 7.5])
    return Q(f'{p} says: "Dividing always makes a number smaller, so {N(x)} ÷ {N(a)} is less than {N(x)}." Explain why {p} is wrong.',
             f'Dividing by a number between 0 and 1 makes the answer larger: {N(x)} ÷ {N(a)} = {ddiv(x, a) if len(ddiv(x, a)) < 9 else sf(x / a, 4)}.',
             'B1 dividing by a number less than 1 gives a larger answer; B1 supported by a value. [2]')


@t32.add('C2', (2, 3, 4), 'explain')
def t32_fact(r, D):
    a, b = r.choice([(23, 47), (36, 58), (19, 64), (72, 15), (43, 28), (125, 36), (64, 85)])
    p = a * b
    sa, sb = r.choice([(1, 2), (2, 1), (1, 1), (2, 2), (1, 3)])
    da, db = dshift(a, -sa), dshift(b, -sb)
    ans = dshift(p, -(sa + sb))
    if r.random() < 0.5:
        return Q(f'You are told that {a} × {b} = {p}. Use this fact to work out {da} × {db}. Explain how you placed the decimal point.', ans,
                 f'{da} = {a} ÷ 10{sup(sa)}, {db} = {b} ÷ 10{sup(sb)} (M1); so divide {p} by 10{sup(sa + sb)}: {ans} (A1). [2]')
    return Q(f'You are told that {a} × {b} = {p}. Use this to work out {ans} ÷ {db}. Explain your reasoning.', da,
             f'{ans} ÷ {db} = ({p} ÷ 10{sup(sa + sb)}) ÷ ({b} ÷ 10{sup(sb)}) (M1) = {a} ÷ 10{sup(sa)} = {da} (A1). [2]')


def _dec_c4(r, D):
    p = person(r)
    pr = r.choice([1.35, 2.45, 0.85, 3.6, 4.25, 1.8])
    kg = r.choice([0.4, 0.6, 1.5, 2.5, 0.75, 1.2])
    m = r.choice([0.25, 0.4, 0.8, 0.5])
    cost = Dec(str(pr)) * Dec(str(kg))
    budget = r.choice([10, 20, 15])
    intro = f'{p} buys food at a market in {city(r)}. Rice costs ${d2(pr)} per kilogram.'
    parts = [
        lambda r: (f'Work out the cost of {N(kg)} kg of rice.', money(float(cost)), f'M1 {d2(pr)} × {N(kg)}; A1 {money(float(cost))} [2]'),
        lambda r: (f'Work out how many {N(m)} kg bags can be filled from {N(m * 24)} kg of rice.', '24', f'M1 {N(m * 24)} ÷ {N(m)}; A1 24 [2]'),
        lambda r: (f'Work out the largest mass of rice, in kg, that {p} can buy with ${budget}, to the nearest 0.1 kg.', f'{N(math.floor(budget / pr * 10) / 10)} kg',
                   f'M1 {budget} ÷ {d2(pr)} = {sf(budget / pr, 4)}; A1 round down to {N(math.floor(budget / pr * 10) / 10)} kg [2]'),
        lambda r: (f'Explain why ${d2(pr)} × {N(m)} is less than ${d2(pr)}.', f'{N(m)} is less than 1, so multiplying by it gives a smaller answer.', 'B1 [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t32.add('C4', (2, 3, 4, 5), 'multi_step')(_dec_c4)


@t32.add('C4', (3, 4, 5), 'multi_step')
def t32_fence(r, D):
    L = r.choice([12.6, 8.4, 15.6, 9.6, 14.4])
    g = r.choice([1.2, 0.6, 0.8, 2.4, 0.4])
    while (Dec(str(L)) / Dec(str(g))) % 1 != 0:
        g = r.choice([1.2, 0.6, 0.8, 2.4, 0.4, 0.3])
    n = int(Dec(str(L)) / Dec(str(g)))
    c = r.choice([3.75, 4.5, 2.25, 6.2])
    return Q(f'A straight fence is {N(L)} m long. Posts are placed every {N(g)} m along it, with a post at each end. (a) How many posts are needed? (b) Each post costs ${d2(c)}. Work out the total cost of the posts. Do not use a calculator.',
             f'(a) {n + 1} (b) {money((n + 1) * c)}', f'(a) M1 {N(L)} ÷ {N(g)} = {n} gaps; A1 {n + 1} posts [2] (b) M1 {n + 1} × {d2(c)}; A1 {money((n + 1) * c)} [2]', marks=4)


t32.fixed('C1', (1, 2), [
    ('Work out 0.6 × 0.5.', '0.3', '6 × 5 = 30, two decimal places → 0.30 = 0.3. [1]', ['3', '0.03', '0.11']),
    ('Work out 4.8 ÷ 0.4.', '12', '48 ÷ 4 = 12. [1]', ['1.2', '0.12', '120']),
    ('Work out 0.07 × 0.2.', '0.014', '7 × 2 = 14, three decimal places. [1]', ['0.14', '0.0014', '1.4']),
    ('Write down the answer to 2.5 × 0.4.', '1', '25 × 4 = 100, two decimal places → 1.00. B1 [1]'),
])
t32.fixed('C2', (2, 3), [
    ('Explain why 3.6 ÷ 0.09 gives the same answer as 360 ÷ 9.', 'Multiplying both numbers by 100 does not change the answer of a division: 3.6 ÷ 0.09 = 360 ÷ 9 = 40.', 'B1 both multiplied by 100; B1 value 40. [2]'),
    ('Without working it out, explain whether 48 × 0.98 is more or less than 48.', 'Less: 0.98 is less than 1, so 48 × 0.98 is less than 48 × 1.', 'B1 less; B1 reason. [2]'),
])


# ----------------------------------------------------------- compound percentages
t33 = topic('Compound percentages and repeated percentage change', 'compound percentages', 'repeated percentage change', 'percentage change')


def mult(p):
    return N(round(1 + p / 100, 6))


@t33.add('C1', (1, 2, 3))
def t33_mult(r, D):
    p = r.choice([3, 4, 5, 8, 12, 15, 20, 25, 35, 2.5, 7.5, 1.5])
    up = r.random() < 0.5
    ans = mult(p if up else -p)
    stem = r.choice([f'Which number do you multiply by to {"increase" if up else "decrease"} an amount by {N(p)}%?',
                     f'What is the multiplier for a {N(p)}% {"increase" if up else "decrease"}?'])
    return MCQ(r, stem, ans, [mult(-p if up else p), N(p / 100), N(p), mult(p * 10 if up else -p * 10) if p < 10 else N(round(p / 1000 + 1, 6))],
               f'100% {"+" if up else "−"} {N(p)}% = {N(100 + (p if up else -p))}% → {ans}. [1]')


@t33.add('C1', (1, 2, 3))
def t33_years(r, D):
    p = r.choice([2, 3, 4, 5, 6, 8, 10])
    n = r.choice([2, 3, 4, 5, 6])
    P = r.choice([500, 800, 1200, 2000, 5000, 15000])
    up = r.random() < 0.6
    m = mult(p if up else -p)
    ans = f'{P:,} × {m}{sup(n)}'
    return MCQ(r, f'A {"savings account pays" if up else "car loses"} {p}% {"compound interest" if up else "of its value"} per year. Which calculation gives the value of ${P:,} after {n} years?',
               ans, [f'{P:,} × {m} × {n}', f'{P:,} × {N(p / 100)}{sup(n)}', f'{P:,} + {P:,} × {N(p * n / 100)}', f'{P:,} × {mult(-p if up else p)}{sup(n)}'],
               f'Each year multiply by {m}; for {n} years multiply by {m}{sup(n)}. [1]')


@t33.add('C2', (1, 2, 3, 4), 'explain')
def t33_updown(r, D):
    p = r.choice([10, 20, 25, 30, 40, 50])
    P = r.choice([40, 80, 120, 200, 250, 400])
    q = person(r)
    after = P * (1 + p / 100) * (1 - p / 100)
    return Q(f'A jacket costs ${P}. The price is increased by {p}% and later the new price is decreased by {p}%. {q} says the final price is ${P}. Is {q} correct? Explain.',
             f'No. ${P} × {mult(p)} = {money(P * (1 + p / 100))}, then × {mult(-p)} = {money(after)}. The decrease is {p}% of a larger amount, so the final price is less than ${P}.',
             f'M1 correct use of multipliers; A1 {money(after)} with explanation. [2]')


@t33.add('C2', (2, 3, 4), 'explain')
def t33_simple(r, D):
    p = r.choice([3, 4, 5, 6, 8, 10])
    n = r.choice([2, 3, 4, 5])
    q = person(r)
    tot = (1 + p / 100) ** n
    return Q(f'{q} says: "A population that grows by {p}% each year for {n} years grows by {p * n}% altogether." Explain why {q} is wrong, and work out the true overall percentage increase to 1 decimal place.',
             f'Each year\'s {p}% is of a bigger amount. Multiplier {mult(p)}{sup(n)} = {fdp(tot, 4)}, so the increase is {fdp((tot - 1) * 100, 1)}%, more than {p * n}%.',
             f'B1 growth is compound (percentage of a growing amount); M1 {mult(p)}{sup(n)}; A1 {fdp((tot - 1) * 100, 1)}%. [3]', marks=3)


@t33.add('C3', (1, 2, 3, 4, 5))
def t33_value(r, D):
    p = r.choice([2, 3, 4, 5, 6, 8, 12, 15, 2.5, 3.5])
    n = r.choice([2, 3, 4, 5, 6, 8, 10]) if D >= 3 else r.choice([2, 3])
    P = r.choice([400, 650, 1200, 2500, 3000, 8000, 12000, 18500])
    kind = r.choice(['invest', 'deprec', 'pop'])
    if kind == 'invest':
        v = P * (1 + p / 100) ** n
        stem = f'{person(r)} invests ${P:,} in a bank in {city(r)} at {N(p)}% compound interest per year. Calculate the value of the investment after {n} years.'
        ans = money(v)
        key = f'Multiplier {mult(p)} (M1); {P} × {mult(p)}{sup(n)} (M1); {money(v)} (A1).'
    elif kind == 'deprec':
        v = P * (1 - p / 100) ** n
        stem = f'A machine costs ${P:,}. Its value falls by {N(p)}% each year. Calculate its value after {n} years.'
        ans = money(v)
        key = f'Multiplier {mult(-p)} (M1); {P} × {mult(-p)}{sup(n)} (M1); {money(v)} (A1).'
    else:
        P = P * 10
        v = P * (1 + p / 100) ** n
        stem = f'The population of a town in {city(r)} is {P:,}. It increases by {N(p)}% each year. Estimate the population after {n} years, to the nearest whole number.'
        ans = f'{round(v):,}'
        key = f'{P:,} × {mult(p)}{sup(n)} (M1, M1); {round(v):,} (A1).'
    if D == 1:
        return Q(stem.replace(f'after {n} years', 'after 2 years').replace('Estimate', 'Calculate'),
                 money(P * (1 + p / 100) ** 2) if kind == 'invest' else (money(P * (1 - p / 100) ** 2) if kind == 'deprec' else f'{round(P * (1 + p / 100) ** 2):,}'),
                 'Multiply by the multiplier twice (M1); answer (A1).')
    return Q(stem, ans, key)


@t33.add('C3', (2, 3, 4, 5))
def t33_overall(r, D):
    a, b = r.choice([10, 20, 25, 30, 15, 40]), r.choice([10, 20, 25, 5, 15])
    up1, up2 = r.choice([(True, False), (False, True), (True, True), (False, False)])
    m = (1 + (a if up1 else -a) / 100) * (1 + (b if up2 else -b) / 100)
    ch = (m - 1) * 100
    w1, w2 = ('increased' if up1 else 'decreased'), ('increased' if up2 else 'decreased')
    return Q(f'The price of a phone is {w1} by {a}% and then the new price is {w2} by {b}%. Work out the overall percentage change.',
             f'{"An increase" if ch > 0 else "A decrease"} of {N(round(abs(ch), 4))}%' if abs(ch) > 1e-9 else 'No change',
             f'Multipliers {mult(a if up1 else -a)} × {mult(b if up2 else -b)} (M1) = {N(round(m, 6))} (A1); {"increase" if ch > 0 else "decrease"} of {N(round(abs(ch), 4))}% (A1).', marks=3)


def _cp_c4(r, D):
    P = r.choice([2000, 3000, 5000, 8000, 10000])
    a, b = r.choice([(4, 3), (5, 4), (3, 2), (6, 5)])
    sb = b + r.choice([1, 2])
    n = r.choice([3, 4, 5])
    vA = P * (1 + a / 100) ** n
    vB = P * (1 + sb * n / 100)
    target = P * r.choice([1.2, 1.25, 1.3, 1.5])
    yrs = 0
    v = P
    while v < target:
        v *= 1 + a / 100
        yrs += 1
    p = person(r)
    intro = f'{p} has ${P:,} to invest for {n} years. Bank A pays {a}% compound interest per year. Bank B pays {sb}% simple interest per year.'
    parts = [
        lambda r: ('Calculate the value of the investment in Bank A after ' + str(n) + ' years.', money(vA), f'M1 {P} × {mult(a)}{sup(n)}; A1 {money(vA)} [2]'),
        lambda r: (f'Calculate the value in Bank B after {n} years.', money(vB), f'M1 {P} × {sb / 100} × {n} = interest; A1 {money(vB)} [2]'),
        lambda r: ('Which bank should ' + p + ' choose? Give a reason.', f'Bank {"A" if vA > vB else "B"}: {money(max(vA, vB))} is more than {money(min(vA, vB))}.', 'B1 decision with values [1]'),
        lambda r: (f'In Bank A, after how many whole years will the investment first be worth more than {money(target)}?', f'{yrs} years', f'M1 repeated × {mult(a)} or trial; A1 {yrs} [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t33.add('C4', (2, 3, 4, 5), 'multi_step')(_cp_c4)


@t33.add('C4', (3, 4, 5), 'multi_step')
def t33_reverse(r, D):
    p = r.choice([5, 10, 15, 20, 25])
    n = r.choice([2, 3])
    orig = r.choice([4000, 6000, 8000, 12000, 20000])
    now = orig * (1 - p / 100) ** n
    return Q(f'A car loses {p}% of its value each year. After {n} years it is worth {money(now)}. (a) Work out its value when it was new. (b) Work out the total percentage loss in value over the {n} years.',
             f'(a) {money(orig)} (b) {N(round((1 - (1 - p / 100) ** n) * 100, 4))}%',
             f'(a) M1 {money(now)} ÷ {mult(-p)}{sup(n)}; A1 {money(orig)} [2] (b) M1 1 − {mult(-p)}{sup(n)}; A1 {N(round((1 - (1 - p / 100) ** n) * 100, 4))}% [2]', marks=4)


t33.fixed('C1', (1, 2), [
    ('What is 15% of $80?', '$12', '0.15 × 80 = 12. [1]', ['$15', '$68', '$92']),
    ('What single multiplier is used to increase an amount by 5% each year for 2 years?', '1.05²', 'Each year × 1.05, so × 1.05² = 1.1025. [1]', ['1.10', '1.05 × 2', '0.05²']),
    ('Write down the multiplier for a decrease of 7%.', '0.93', '100% − 7% = 93%. B1 [1]'),
])
t33.fixed('C2', (2, 3), [
    ('Explain the difference between simple interest and compound interest.', 'Simple interest is calculated on the original amount each year; compound interest is calculated on the amount at the start of each year, including interest already earned.', 'B1 simple on original; B1 compound includes previous interest. [2]'),
    ('Explain why multiplying by 0.8 twice is the same as decreasing by 36%, not by 40%.', '0.8 × 0.8 = 0.64, so 64% remains: a decrease of 36%. The second 20% is taken from a smaller amount.', 'M1 0.8² = 0.64; A1 explanation. [2]'),
])


# ----------------------------------------------------------- bounds
t34 = topic('Upper and lower bounds', 'upper and lower bounds', 'rounded values', 'bounds')
ACC = [('to the nearest whole number', 1), ('to the nearest 10', 10), ('to 1 decimal place', 0.1), ('to the nearest 100', 100), ('to 2 decimal places', 0.01), ('to the nearest 5', 5)]


def _bnds(r, D):
    acc, u = r.choice(ACC[:3] if D <= 2 else ACC)
    if u >= 1:
        v = u * r.randint(3, 99)
    else:
        v = round(r.randint(12, 999) * u, 2)
    lo, hi = Dec(str(v)) - Dec(str(u)) / 2, Dec(str(v)) + Dec(str(u)) / 2
    return acc, u, v, format(lo.normalize(), 'f'), format(hi.normalize(), 'f')


@t34.add('C1', (1, 2, 3))
def t34_mcq(r, D):
    acc, u, v, lo, hi = _bnds(r, D)
    unit = r.choice(['cm', 'kg', 'm', 'g', 'litres'])
    which = r.choice(['lower', 'upper'])
    ans = lo if which == 'lower' else hi
    other = hi if which == 'lower' else lo
    step = Dec(str(u)) / 10
    near = format((Dec(hi) - step).normalize(), 'f') if which == 'upper' else format((Dec(lo) + step).normalize(), 'f')
    return MCQ(r, f'A length is {N(v)} {unit}, correct {acc}. What is its {which} bound?', f'{ans} {unit}',
               [f'{other} {unit}', f'{near} {unit}', f'{format((Dec(str(v)) + (Dec(str(u)) if which == "upper" else -Dec(str(u)))).normalize(), "f")} {unit}', f'{format((Dec(str(v)) + (Dec(str(u)) / 10 * (1 if which == "upper" else -1))).normalize(), "f")} {unit}'],
               f'Half of {N(u)} is {N(u / 2)}; {which} bound = {N(v)} {"−" if which == "lower" else "+"} {N(u / 2)} = {ans}. [1]')


@t34.add('C3', (1, 2, 3, 4, 5))
def t34_interval(r, D):
    acc, u, v, lo, hi = _bnds(r, D)
    thing = r.choice([('The mass of a parcel', 'm', 'kg'), ('The height of a tree', 'h', 'm'), ('The time for a race', 't', 's'), ('The length of a rope', 'l', 'm'), ('The volume of a bottle', 'V', 'ml')])
    stem = r.choice([f'{thing[0]} is {N(v)} {thing[2]}, correct {acc}. Write down the error interval for {thing[1]}.',
                     f'{thing[0]}, {thing[1]} {thing[2]}, is measured as {N(v)} {thing[2]} {acc}. Complete the inequality: … ≤ {thing[1]} < …'])
    return Q(stem, f'{lo} ≤ {thing[1]} < {hi}', f'B1 lower bound {lo}; B1 upper bound {hi} with correct inequality signs.')


@t34.add('C2', (1, 2, 3, 4), 'explain')
def t34_why(r, D):
    acc, u, v, lo, hi = _bnds(r, D)
    p = person(r)
    nine = format((Dec(hi) - Dec(str(u)) / 100).normalize(), 'f')
    if r.random() < 0.5:
        return Q(f'A length is {N(v)} cm {acc}. {p} says the upper bound is {nine} cm because {hi} cm would round up to {format((Dec(str(v)) + Dec(str(u))).normalize(), "f")} cm. Explain why the upper bound is written as {hi} cm.',
                 f'Every number up to (but not including) {hi} rounds to {N(v)}; {nine} is not the largest such value (e.g. {format((Dec(nine) + Dec(str(u)) / 1000).normalize(), "f")} is larger). We use {hi} with a strict inequality: l < {hi}.',
                 'B1 there is no largest value below the bound; B1 strict inequality < used. [2]')
    return Q(f'{p} says that a mass of {N(v)} kg given {acc} could actually be {lo} kg but could not be {hi} kg. Explain why {p} is correct.',
             f'{lo} rounds up to {N(v)}, but {hi} rounds up to the next value, {format((Dec(str(v)) + Dec(str(u))).normalize(), "f")}. So {lo} ≤ m < {hi}.',
             'B1 explains rounding at each bound; B1 inequality. [2]')


@t34.add('C2', (2, 3, 4), 'explain')
def t34_discrete(r, D):
    n = r.choice([350, 1200, 4500, 780, 2600, 12000])
    u = 10 if n < 1000 else 100
    p = person(r)
    return Q(f'{n:,} people attended a festival in {city(r)}, correct to the nearest {u}. {p} says the upper bound is {n + u // 2:,}. Explain why, for a number of people, the largest possible value is {n + u // 2 - 1:,}.',
             f'The number of people is a whole number (discrete). {n + u // 2:,} would round to {n + u:,}, so the largest whole number that rounds to {n:,} is {n + u // 2 - 1:,}.',
             'B1 data discrete (whole numbers); B1 largest value explained. [2]')


@t34.add('C3', (2, 3, 4, 5))
def t34_perim(r, D):
    a = r.randint(4, 15)
    b = r.randint(3, 12)
    shape = r.choice(['rect', 'sum', 'diff']) if D >= 3 else 'rect'
    if shape == 'rect':
        return Q(f'A rectangle has length {a} cm and width {b} cm, both correct to the nearest centimetre. Work out the upper bound and lower bound of the perimeter.',
                 f'Upper {2 * (a + b) + 2} cm; lower {2 * (a + b) - 2} cm', f'M1 uses {a + 0.5}, {b + 0.5} (or {a - 0.5}, {b - 0.5}); A1 upper 2({N(a + 0.5)} + {N(b + 0.5)}) = {2 * (a + b) + 2}; A1 lower {2 * (a + b) - 2}.', marks=3)
    if shape == 'sum':
        m1, m2 = r.randint(20, 80), r.randint(20, 80)
        return Q(f'Two bags have masses {m1} kg and {m2} kg, each correct to the nearest kilogram. Work out the upper bound of their total mass.',
                 f'{m1 + m2 + 1} kg', f'M1 {N(m1 + 0.5)} + {N(m2 + 0.5)}; A1 {m1 + m2 + 1} kg.')
    L, cut = r.randint(30, 90), r.randint(5, 25)
    return Q(f'A plank is {L} cm long, to the nearest cm. A piece {cut} cm long, to the nearest cm, is cut off. Work out the greatest possible length of the piece that is left.',
             f'{N(L - cut + 1)} cm', f'M1 greatest = upper bound − lower bound = {N(L + 0.5)} − {N(cut - 0.5)}; A1 {N(L - cut + 1)} cm.', marks=3)


def _bnd_c4(r, D):
    load = r.choice([500, 600, 750, 800, 1000])
    m = r.choice([70, 75, 80, 85])
    n = r.randint(6, 10)
    hi = m + 2.5
    safe = int(load // hi)
    w = r.choice([1.5, 1.2, 2.4, 1.8])
    intro = f'A lift in a building in {city(r)} has a safe load limit of {load} kg. The masses of people are given to the nearest 5 kg.'
    parts = [
        lambda r: (f'A person has mass {m} kg to the nearest 5 kg. Write down the error interval for their mass.', f'{N(m - 2.5)} ≤ m < {N(hi)}', 'B1 B1 [2]'),
        lambda r: (f'Assume everyone has mass {m} kg to the nearest 5 kg. What is the largest number of people that can safely use the lift? Show your working.',
                   str(safe), f'M1 uses upper bound {N(hi)}; M1 {load} ÷ {N(hi)} = {sf(load / hi, 4)}; A1 {safe} (round down) [3]'),
        lambda r: (f'The lift door is {N(w)} m wide to 1 decimal place. A box is {N(round(w - 0.1, 2))} m wide to 1 decimal place. Explain whether the box will definitely fit through the door.',
                   f'Yes. The box is less than {N(round(w - 0.05, 2))} m wide and the door is at least {N(round(w - 0.05, 2))} m wide, so the box will always fit (only just, in the extreme case).',
                   'M1 compares lower bound of door with upper bound of box; A1 conclusion [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t34.add('C4', (2, 3, 4, 5), 'multi_step')(_bnd_c4)


@t34.add('C4', (3, 4, 5), 'multi_step')
def t34_speed(r, D):
    d = r.choice([100, 200, 400, 800, 1500])
    t = r.choice([12.4, 25.6, 58.2, 130.5, 248.3]) if d != 100 else 11.8
    p = person(r)
    vmax = (d + 0.5) / (t - 0.05)
    vmin = (d - 0.5) / (t + 0.05)
    return Q(f'{p} runs {d} m, measured to the nearest metre, in {N(t)} seconds, measured to the nearest 0.1 second. (a) Write down the bounds for the distance and the time. (b) Calculate the upper bound of {p}\'s average speed, giving your answer to 3 decimal places. (c) Calculate the lower bound of the speed to 3 decimal places.',
             f'(a) {N(d - 0.5)} ≤ d < {N(d + 0.5)}; {N(round(t - 0.05, 2))} ≤ t < {N(round(t + 0.05, 2))} (b) {fdp(vmax, 3)} m/s (c) {fdp(vmin, 3)} m/s',
             f'(a) B1 B1 [2] (b) M1 upper distance ÷ lower time = {N(d + 0.5)} ÷ {N(round(t - 0.05, 2))}; A1 {fdp(vmax, 3)} [2] (c) M1 {N(d - 0.5)} ÷ {N(round(t + 0.05, 2))}; A1 {fdp(vmin, 3)} [2]', marks=6)


t34.fixed('C1', (1, 2), [
    ('A mass is 8 kg to the nearest kilogram. What is the lower bound?', '7.5 kg', '8 − 0.5 = 7.5. [1]', ['7 kg', '7.9 kg', '7.95 kg']),
    ('A time is 3.6 s to 1 decimal place. What is the upper bound?', '3.65 s', '3.6 + 0.05 = 3.65. [1]', ['3.7 s', '3.69 s', '3.64 s']),
    ('To find the upper bound of a − b, which values should you use?', 'Upper bound of a and lower bound of b', 'Largest difference: largest a minus smallest b. [1]', ['Upper bounds of a and b', 'Lower bounds of a and b', 'Lower bound of a and upper bound of b']),
    ('A number rounds to 40 to the nearest 10. Write down the smallest possible value of the number.', '35', 'B1 [1]'),
])
t34.fixed('C2', (2, 3), [
    ('Explain why measurements such as length are given with bounds but a count of students in a class is not usually given with bounds.', 'Length is continuous and can only be measured to a degree of accuracy; a count of students is discrete and can be found exactly.', 'B1 continuous measured to an accuracy; B1 discrete counted exactly. [2]'),
    ('Explain how to find the lower bound of the area of a rectangle whose sides are given to the nearest cm.', 'Multiply the lower bound of the length by the lower bound of the width.', 'B1 lower bounds of both; B1 multiply. [2]'),
])

CHAPTERS[3] = [t31, t32, t33, t34]


# =========================================================== 4 Equations and inequalities
t41 = topic('Constructing and solving linear equations', 'constructing and solving linear equations', 'brackets and fractions', 'linear equations')
NZ = [v for v in range(-9, 10) if v != 0]


def _sol(r, D):
    if D <= 2:
        return r.randint(1, 12)
    if D == 3:
        return r.choice([v for v in range(-8, 15) if v != 0])
    return r.choice([Fr(v, 2) for v in range(-9, 15, 2)] + [r.randint(-9, 12) or 4])


@t41.add('C3', (1, 2, 3, 4, 5))
def t41_solve(r, D):
    x = Fr(_sol(r, D))
    form = r.choice(['ab', 'bracket', 'both', 'frac'] if D >= 3 else ['ab', 'bracket'])
    if D >= 4:
        form = r.choice(['both', 'frac', 'frac2', 'bracket2'])
    a = r.choice([2, 3, 4, 5, 6, 7])
    b = r.choice(NZ)
    if form == 'ab':
        rhs = a * x + b
        eq = f'{lin(a, b)} = {fr(rhs)}'
        steps = f'{a}x = {fr(rhs - b)} (M1); x = {fr(x)} (A1).'
    elif form == 'bracket':
        rhs = a * (x + b)
        eq = f'{a}({lin(1, b)}) = {fr(rhs)}'
        steps = f'Expand {lin(a, a * b)} = {fr(rhs)} or divide by {a} (M1); x = {fr(x)} (A1).'
    elif form == 'both':
        c = r.choice([v for v in range(1, 9) if v != a])
        d = (a - c) * x + b
        eq = f'{lin(a, b)} = {lin(c, d)}' if d.denominator == 1 else None
        if eq is None:
            return None
        steps = f'{lin(a - c, 0)} = {fr(d - b)} (M1, collect x terms); x = {fr(x)} (A1).'
    elif form == 'frac':
        k = r.choice([2, 3, 4, 5])
        rhs = (x + b) / k
        if rhs.denominator != 1:
            return None
        eq = f'({lin(1, b)})/{k} = {fr(rhs)}'
        steps = f'× {k}: {lin(1, b)} = {fr(rhs * k)} (M1); x = {fr(x)} (A1).'
    elif form == 'frac2':
        p, q = r.sample([2, 3, 4, 5], 2)
        lhs = x / p + x / q
        if lhs.denominator != 1:
            x = Fr(p * q * r.randint(1, 4))
            lhs = x / p + x / q
        eq = f'x/{p} + x/{q} = {fr(lhs)}'
        steps = f'× {p * q}: {q}x + {p}x = {fr(lhs * p * q)} (M1); {p + q}x = {fr(lhs * p * q)} (M1); x = {fr(x)} (A1).'
    else:
        c = r.choice([2, 3, 4])
        d = r.choice(NZ)
        rhs = a * (x + b) - c * (x + d)
        eq = f'{a}({lin(1, b)}) {MINUS} {c}({lin(1, d)}) = {fr(rhs)}'
        steps = f'Expand: {lin(a, a * b)} {MINUS} {c}x {"−" if c * d > 0 else "+"} {abs(c * d)} = {fr(rhs)} (M1); {lin(a - c, a * b - c * d)} = {fr(rhs)} (M1); x = {fr(x)} (A1).'
        if a == c:
            return None
    stem = r.choice([f'Solve {eq}.', f'Solve the equation {eq}. Show your working.', f'Find the value of x when {eq}.'])
    if D == 1:
        return MCQ(r, f'Solve {eq}.', f'x = {fr(x)}', [f'x = {fr(x + 1)}', f'x = {fr(-x)}', f'x = {fr(x * 2)}', f'x = {fr(x - 2)}'], steps)
    return Q(stem, f'x = {mixed(x) if x.denominator != 1 else fr(x)}', steps)


@t41.add('C2', (1, 2, 3, 4), 'explain')
def t41_err(r, D):
    a, b = r.randint(2, 6), r.randint(2, 9)
    x = r.randint(2, 9)
    p = person(r)
    kind = r.choice(['bracket', 'move', 'frac'])
    if kind == 'bracket':
        rhs = a * (x + b)
        wrong = Fr(rhs - b, a)
        stem = f'{p} solves {a}(x + {b}) = {rhs} like this: {a}x + {b} = {rhs}, so {a}x = {rhs - b}, so x = {mixed(wrong)}. Explain the mistake and solve the equation correctly.'
        ans = f'{p} did not multiply {b} by {a} when expanding. {a}x + {a * b} = {rhs}, {a}x = {rhs - a * b}, x = {x}.'
    elif kind == 'move':
        rhs = a * x - b
        stem = f'{p} solves {a}x {MINUS} {b} = {rhs} and writes {a}x = {rhs - b}. Explain the mistake and find the correct value of x.'
        ans = f'To remove −{b} you add {b} to both sides: {a}x = {rhs + b}, so x = {x}.'
    else:
        k = r.choice([2, 3, 4, 5])
        rhs = r.randint(2, 9)
        stem = f'{p} solves x/{k} + {b} = {rhs + b} by multiplying only x/{k} by {k}, getting x + {b} = {rhs + b}. Explain the mistake and solve the equation correctly.'
        ans = f'Every term must be multiplied by {k}: x + {b * k} = {(rhs + b) * k}, so x = {rhs * k}. (Or subtract {b} first: x/{k} = {rhs}.)'
    return Q(stem, ans, 'B1 identifies the error; B1 correct solution. [2]')


@t41.add('C2', (2, 3, 4), 'explain')
def t41_check(r, D):
    a, b, c = r.randint(2, 7), r.randint(1, 9), r.randint(1, 4)
    x = r.randint(2, 9)
    d = (a - c) * x + b
    if a == c:
        c += 1
        d = (a - c) * x + b
    claim = x + r.choice([1, -1, 2])
    p = person(r)
    return Q(f'{p} says that x = {claim} is the solution of {lin(a, b)} = {lin(c, d)}. Show how substitution can be used to check this, and decide whether {p} is right.',
             f'Left: {a} × {claim} + {b} = {a * claim + b}. Right: {c} × {claim} {"+" if d >= 0 else "−"} {abs(d)} = {c * claim + d}. They are not equal, so {p} is wrong (the solution is x = {x}).',
             'M1 substitutes into both sides; A1 conclusion with correct solution. [2]')


@t41.add('C1', (1, 2, 3))
def t41_form(r, D):
    p = person(r)
    a, b, n = r.randint(2, 6), r.randint(3, 15), r.randint(4, 15)
    kind = r.choice(['think', 'perim', 'age'])
    if kind == 'think':
        tot = a * n + b
        stem = f'{p} thinks of a number n, multiplies it by {a} and adds {b}. The answer is {tot}. Which equation shows this?'
        ans = f'{a}n + {b} = {tot}'
        ds = [f'{a}(n + {b}) = {tot}', f'n + {a} + {b} = {tot}', f'{b}n + {a} = {tot}']
    elif kind == 'perim':
        P = 2 * (n + n + b)
        stem = f'A rectangle has width w cm and length (w + {b}) cm. Its perimeter is {P} cm. Which equation is correct?'
        ans = f'4w + {2 * b} = {P}'
        ds = [f'2w + {b} = {P}', f'w(w + {b}) = {P}', f'4w + {b} = {P}']
    else:
        tot = 2 * n + a
        stem = f'{p} is x years old. Their brother is {a} years older. The sum of their ages is {tot}. Which equation is correct?'
        ans = f'2x + {a} = {tot}'
        ds = [f'x + {a} = {tot}', f'{a}x = {tot}', f'2x = {tot} + {a}']
    return MCQ(r, stem, ans, ds, f'{ans}. [1]')


ANG = ['angles on a straight line', 'angles in a triangle', 'angles around a point']


def _eq_c4(r, D):
    x = r.randint(8, 30)
    kind = r.choice(['tri', 'line', 'quad'])
    if kind == 'tri':
        a, b = r.randint(1, 3), r.randint(2, 4)
        c = 180 - (a * x + b * x + 10)
        if c <= 10:
            return None
        intro = f"The angles of a triangle are {lin(a, 0)}°, ({lin(b, 10)})° and {c}°."
        total, eq, angs = 180, f'{lin(a + b, 10 + c)} = 180', [a * x, b * x + 10, c]
    elif kind == 'line':
        a = r.randint(2, 5)
        b = 180 - a * x - x
        if b <= 0:
            return None
        intro = f'Two angles on a straight line are {a}x° and ({lin(1, b)})°.'
        total, eq, angs = 180, f'{lin(a + 1, b)} = 180', [a * x, x + b]
    else:
        a, b = r.randint(2, 4), r.randint(1, 3)
        rest = 360 - (a + b + 1) * x
        if rest <= 20:
            return None
        intro = f'The angles of a quadrilateral are {a}x°, {lin(b, 0)}°, x° and {rest}°.'
        total, eq, angs = 360, f'{lin(a + b + 1, rest)} = 360', [a * x, b * x, x, rest]
    parts = [
        lambda r: ('Write down an equation in x.', eq, f'B1 angle sum = {total} [1]'),
        lambda r: ('Solve your equation to find x.', f'x = {x}', f'M1 collect terms; A1 x = {x} [2]'),
        lambda r: ('Work out the size of the largest angle.', f'{max(angs)}°', f'M1 substitutes x = {x}; A1 {max(angs)}° [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t41.add('C4', (2, 3, 4, 5), 'multi_step')(_eq_c4)


@t41.add('C4', (2, 3, 4, 5), 'multi_step')
def t41_money(r, D):
    p, q = two_people(r)
    x = r.randint(5, 40)
    a = r.randint(2, 4)
    b = r.randint(3, 15)
    tot = x + a * x - b
    give = r.randint(1, 4)
    intro = f'{q} has ${b} less than {a} times the amount {p} has. Together they have ${tot}. Let {p} have $x.'
    parts = [
        lambda r: (f'Write an expression for the amount {q} has.', f'$({a}x − {b})', 'B1 [1]'),
        lambda r: ('Form an equation and solve it to find how much each person has.', f'{p} ${x}, {q} ${a * x - b}', f'M1 x + {a}x − {b} = {tot}; M1 {a + 1}x = {tot + b}; A1 both amounts [3]'),
        lambda r: (f'{q} gives {p} enough money so that they have the same amount. How much does {q} give?', money((a * x - b - x) / 2), f'M1 each has {money(tot / 2)}; A1 {money((a * x - b - x) / 2)} [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t41.fixed('C1', (1, 2), [
    ('Solve 5x = 35.', 'x = 7', 'Divide both sides by 5. [1]', ['x = 30', 'x = 40', 'x = 175']),
    ('Solve x/4 = 9.', 'x = 36', 'Multiply both sides by 4. [1]', ['x = 2.25', 'x = 13', 'x = 5']),
    ('What is the first step to solve 3(x − 2) = 15 in the most efficient way?', 'Divide both sides by 3', 'Dividing by 3 gives x − 2 = 5 straight away (expanding also works). [1]', ['Add 2 to both sides', 'Subtract 3 from both sides', 'Multiply both sides by 3']),
    ('Solve 2x + 9 = 1.', 'x = −4', '2x = −8. B1 [1]'),
])
t41.fixed('C2', (2, 3), [
    ('Explain why the equation 2(x + 3) = 2x + 5 has no solution.', '2(x + 3) = 2x + 6, so the equation becomes 2x + 6 = 2x + 5, which gives 6 = 5, which is never true.', 'M1 expands; A1 contradiction explained. [2]'),
    ('Explain the difference between an equation and an identity, using 3(x + 1) = 3x + 3 and 3x + 1 = 10.', '3(x + 1) = 3x + 3 is true for all x (identity); 3x + 1 = 10 is true only for x = 3 (equation).', 'B1 identity true for every value; B1 equation true for particular value(s). [2]'),
])


# ----------------------------------------------------------- simultaneous equations
t42 = topic('Simultaneous linear equations', 'solving simultaneous linear equations', 'simultaneous equations')


def _sim(r, D):
    for _ in range(100):
        x, y = r.choice(NZ if D >= 3 else range(1, 10)), r.choice(NZ if D >= 3 else range(1, 10))
        if D <= 2:
            a, b = r.randint(1, 5), r.randint(1, 4)
            c, d = a, -r.randint(1, 4) if r.random() < 0.5 else r.randint(1, 4)
            if d == b:
                continue
        elif D == 3:
            a, b, c, d = r.randint(1, 5), r.randint(1, 5), r.randint(1, 5), r.randint(1, 5)
            if a * d == b * c or (a != c and b != d and a != 1 and c != 1):
                continue
        else:
            a, b, c, d = r.randint(2, 7), r.choice([v for v in range(-5, 6) if v]), r.randint(2, 6), r.choice([v for v in range(-5, 6) if v])
            if a * d == b * c:
                continue
        return x, y, (a, b, a * x + b * y), (c, d, c * x + d * y)
    return 2, 3, (1, 1, 5), (1, -1, -1)


def eqs(e):
    a, b, c = e
    return f'{poly((a, "x"), (b, "y"))} = {N(c)}'


@t42.add('C3', (1, 2, 3, 4, 5))
def t42_solve(r, D):
    x, y, e1, e2 = _sim(r, D)
    stem = r.choice([f'Solve the simultaneous equations {eqs(e1)} and {eqs(e2)}.', f'Solve these simultaneous equations. {eqs(e1)}; {eqs(e2)}. Show your working.'])
    a, b, _ = e1
    c, d, _ = e2
    if a == c:
        m = 'Subtract the equations to eliminate x'
    elif b == d:
        m = 'Subtract the equations to eliminate y'
    elif b == -d:
        m = 'Add the equations to eliminate y'
    else:
        m = f'Multiply to match coefficients (e.g. first × {c}, second × {a}) then eliminate x'
    if D == 1:
        return MCQ(r, f'Which pair of values satisfies both {eqs(e1)} and {eqs(e2)}?', f'x = {N(x)}, y = {N(y)}',
                   [f'x = {N(y)}, y = {N(x)}', f'x = {N(x + 1)}, y = {N(y - 1)}', f'x = {N(-x)}, y = {N(y)}', f'x = {N(x)}, y = {N(-y)}'], f'Check both equations: {m}. [1]')
    return Q(stem, f'x = {N(x)}, y = {N(y)}', f'{m} (M1); first variable found (A1); substitute to find the second (M1); x = {N(x)}, y = {N(y)} (A1).', marks=4 if D >= 3 else 3)


@t42.add('C1', (1, 2, 3))
def t42_check(r, D):
    x, y, e1, e2 = _sim(r, min(D, 3))
    p = person(r)
    return MCQ(r, f'{p} solves {eqs(e1)} and {eqs(e2)}. Which of these is the solution?', f'x = {N(x)}, y = {N(y)}',
               [f'x = {N(y)}, y = {N(x)}', f'x = {N(x + 2)}, y = {N(y - 1)}', f'x = {N(x - 1)}, y = {N(y + 1)}', f'x = {N(-x)}, y = {N(-y)}'],
               f'Substitute into both equations: {e1[0]}({N(x)}) + {e1[1]}({N(y)}) = {N(e1[2])}. [1]')


@t42.add('C2', (1, 2, 3, 4), 'explain')
def t42_method(r, D):
    x, y, e1, e2 = _sim(r, 3)
    a, b, _ = e1
    c, d, _ = e2
    p = person(r)
    if a == c or b == d:
        what = 'x' if a == c else 'y'
        return Q(f'{p} wants to solve {eqs(e1)} and {eqs(e2)}. Explain why subtracting one equation from the other is a good first step, and find the solution.',
                 f'The coefficients of {what} are the same, so subtracting eliminates {what}. Solution: x = {N(x)}, y = {N(y)}.', 'B1 explanation of elimination; B1 correct solution. [2]')
    return Q(f'{p} wants to solve {eqs(e1)} and {eqs(e2)} by elimination. Explain what {p} should do first, and why.',
             f'Multiply the equations so that the coefficients of x (or y) are equal, e.g. first × {c} and second × {a}, then subtract to eliminate x. (Solution x = {N(x)}, y = {N(y)}.)',
             'B1 multiply to make coefficients equal; B1 then add/subtract to eliminate one variable. [2]')


@t42.add('C2', (2, 3, 4), 'explain')
def t42_err(r, D):
    x, y = r.randint(1, 8), r.randint(1, 8)
    a, b = r.randint(2, 5), r.randint(1, 4)
    e1, e2 = (a, b, a * x + b * y), (a, -b, a * x - b * y)
    p = person(r)
    return Q(f'{p} solves {eqs(e1)} and {eqs(e2)} by subtracting the equations, and gets 0 = {N(e1[2] - e2[2])}. Explain {p}\'s mistake and solve the equations correctly.',
             f'Subtracting gives {2 * b}y = {N(e1[2] - e2[2])}, not 0: the y terms are +{b}y and −{b}y, so they should be ADDED to eliminate y (giving {2 * a}x = {e1[2] + e2[2]}). x = {x}, y = {y}.',
             'B1 explains add when signs differ / y terms do not cancel on subtraction; B1 correct solution. [2]')


SIM_CTX = [
    ('A cinema in {c} sells adult tickets for $a and child tickets for $b.', 'adult ticket', 'child ticket'),
    ('At a café in {c}, a coffee costs $a and a muffin costs $b.', 'coffee', 'muffin'),
    ('In a shop in {c}, a notebook costs $a and a pen costs $b.', 'notebook', 'pen'),
]


def _sim_c4(r, D):
    txt, A, B = r.choice(SIM_CTX)
    a, b = r.choice([(8, 5), (12, 7), (6, 4), (9, 6), (3.5, 2), (4.5, 2.5), (2.4, 1.5)])
    n1, m1 = r.randint(2, 5), r.randint(1, 4)
    n2, m2 = r.randint(1, 4), r.randint(2, 6)
    if n1 * m2 == n2 * m1:
        return None
    t1, t2 = n1 * a + m1 * b, n2 * a + m2 * b
    p, q = two_people(r)
    intro = txt.replace('$a', 'x dollars').replace('$b', 'y dollars').format(c=city(r)) + f' {p} buys {n1} {A}s and {m1} {B}{"s" if m1 > 1 else ""} for {money(t1)}. {q} buys {n2} {A}{"s" if n2 > 1 else ""} and {m2} {B}s for {money(t2)}.'
    parts = [
        lambda r: ('Write down two equations in x and y.', f'{n1}x + {m1}y = {N(t1)}; {n2}x + {m2}y = {N(t2)}', 'B1 each [2]'),
        lambda r: ('Solve the equations to find x and y.', f'x = {N(a)}, y = {N(b)}', 'M1 eliminates one variable; A1 first value; A1 second value [3]'),
    ]
    k3, k2 = r.choice([3, 4, 5]), r.choice([2, 3])
    parts.append(lambda r: (f'Using your values of x and y, work out the cost of {k3} {A}s and {k2} {B}s.', money(k3 * a + k2 * b), f'M1 {k3}x + {k2}y; A1 {money(k3 * a + k2 * b)} [2]'))
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t42.add('C4', (2, 3, 4, 5), 'multi_step')(_sim_c4)


@t42.add('C4', (3, 4, 5), 'multi_step')
def t42_line(r, D):
    m1, c1 = r.choice([1, 2, 3, -1]), r.randint(-5, 6)
    m2 = r.choice([v for v in (-3, -2, -1, 1, 2, 4) if v != m1])
    x = r.randint(-4, 5)
    y = m1 * x + c1
    c2 = y - m2 * x
    return Q(f'The lines y = {lin(m1, c1)} and y = {lin(m2, c2)} cross at the point P. (a) Explain why the coordinates of P satisfy both equations. (b) Find the coordinates of P by solving the equations simultaneously. (c) Check your answer by substitution.',
             f'(a) P lies on both lines. (b) P = ({N(x)}, {N(y)}) (c) {lin(m1, c1).replace("x", f"({N(x)})")} = {N(y)} and {lin(m2, c2).replace("x", f"({N(x)})")} = {N(y)}',
             f'(a) B1 [1] (b) M1 {lin(m1, c1)} = {lin(m2, c2)}; M1 x = {N(x)}; A1 ({N(x)}, {N(y)}) [3] (c) B1 [1]', marks=5)


t42.fixed('C1', (1, 2), [
    ('How many solutions do two different straight lines that are parallel have when solved simultaneously?', 'None', 'Parallel lines never meet, so there is no point on both lines. [1]', ['One', 'Two', 'Infinitely many']),
    ('x + y = 10 and x − y = 4. What is the value of x?', '7', 'Add: 2x = 14. [1]', ['3', '6', '14']),
    ('2x + y = 11 and x = 3. Write down the value of y.', '5', 'B1 [1]'),
])
t42.fixed('C2', (2, 3), [
    ('Explain how the solution of two simultaneous linear equations can be seen on a graph.', 'Draw both lines; the coordinates of the point where they cross give the solution, because that point is on both lines.', 'B1 draw both lines; B1 intersection gives the solution. [2]'),
    ('Explain why x + y = 6 and 2x + 2y = 12 do not have a single solution.', 'The second equation is just the first multiplied by 2, so they are the same line; every point on it is a solution.', 'B1 same line / equivalent; B1 infinitely many solutions. [2]'),
])


# ----------------------------------------------------------- inequalities
t43 = topic('Linear inequalities', 'representing and solving linear inequalities', 'inequalities')
SGN = ['<', '≤', '>', '≥']
FLIP = {'<': '>', '>': '<', '≤': '≥', '≥': '≤'}


@t43.add('C3', (1, 2, 3, 4, 5))
def t43_solve(r, D):
    s = r.choice(SGN)
    x = r.randint(-5, 12)
    a = r.choice([2, 3, 4, 5])
    b = r.choice(NZ)
    if D >= 4 and r.random() < 0.6:
        a = -a
        rhs = a * x + b
        eq = f'{lin(a, b)} {s} {N(rhs)}'
        ans = f'x {FLIP[s]} {N(x)}'
        key = f'{lin(a, 0)} {s} {N(rhs - b)} (M1); divide by {N(a)} and reverse the sign (M1); {ans} (A1).'
    elif D >= 3:
        c = r.choice([v for v in range(1, 6) if v != a])
        d = (a - c) * x + b
        eq = f'{lin(a, b)} {s} {lin(c, d)}'
        ans = f'x {s if a > c else FLIP[s]} {N(x)}'
        key = f'Collect x terms: {lin(a - c, 0)} {s} {N(d - b)} (M1); {ans} (A1).'
    else:
        rhs = a * x + b
        eq = f'{lin(a, b)} {s} {N(rhs)}'
        ans = f'x {s} {N(x)}'
        key = f'{a}x {s} {N(rhs - b)} (M1); {ans} (A1).'
    if D == 5:
        lo = r.randint(-6, 2)
        hi = lo + r.randint(3, 8)
        a, b = r.choice([2, 3]), r.randint(-5, 5)
        eq = f'{N(a * lo + b)} < {lin(a, b)} ≤ {N(a * hi + b)}'
        ints = list(range(lo + 1, hi + 1))
        return Q(f'Solve {eq} and list the integer values of x that satisfy it.', f'{lo} < x ≤ {hi}; integers {", ".join(N(i) for i in ints)}',
                 f'Subtract {N(b)} from each part (M1); divide by {a} (M1); {lo} < x ≤ {hi} (A1); integers listed (B1).', marks=4)
    return Q(r.choice([f'Solve the inequality {eq}.', f'Solve {eq}. Show your working.']), ans, key)


@t43.add('C1', (1, 2, 3))
def t43_ints(r, D):
    lo = r.randint(-5, 3)
    hi = lo + r.randint(2, 5)
    s1, s2 = r.choice(['<', '≤']), r.choice(['<', '≤'])
    ints = [i for i in range(lo - 1, hi + 2) if (i > lo if s1 == '<' else i >= lo) and (i < hi if s2 == '<' else i <= hi)]
    ans = ', '.join(N(i) for i in ints)
    wrong1 = ', '.join(N(i) for i in range(lo, hi + 1))
    wrong2 = ', '.join(N(i) for i in range(lo + 1, hi))
    wrong3 = ', '.join(N(i) for i in range(lo, hi))
    wrong4 = ', '.join(N(i) for i in range(lo + 1, hi + 1))
    return MCQ(r, f'List all the integers n such that {N(lo)} {s1} n {s2} {N(hi)}.' if D > 1 else f'Which integers satisfy {N(lo)} {s1} n {s2} {N(hi)}?', ans,
               [wrong1, wrong2, wrong3, wrong4], f'< excludes the end value, ≤ includes it: {ans}. [1]')


@t43.add('C1', (1, 2, 3))
def t43_line(r, D):
    v = r.randint(-6, 8)
    s = r.choice(SGN)
    circle = 'an open (empty) circle' if s in '<>' else 'a closed (filled) circle'
    arrow = 'left' if s in '<≤' else 'right'
    ans = f'{circle[0].upper() + circle[1:]} at {N(v)} with an arrow to the {arrow}'
    c2 = 'A closed (filled) circle' if s in '<>' else 'An open (empty) circle'
    a2 = 'right' if arrow == 'left' else 'left'
    return MCQ(r, f'How is the inequality x {s} {N(v)} shown on a number line?', ans,
               [f'{c2} at {N(v)} with an arrow to the {arrow}', f'{circle[0].upper() + circle[1:]} at {N(v)} with an arrow to the {a2}', f'{c2} at {N(v)} with an arrow to the {a2}'],
               f'{"Strict inequality: open circle" if s in "<>" else "Includes the value: closed circle"}; arrow towards the values that satisfy it. [1]')


@t43.add('C2', (1, 2, 3, 4), 'explain')
def t43_flip(r, D):
    a = r.choice([2, 3, 4, 5])
    b = r.randint(1, 9)
    x = r.randint(-3, 8)
    s = r.choice(SGN)
    rhs = -a * x + b
    p = person(r)
    t = x + r.choice([1, 2, -1, -2])
    ok = {'<': -a * t + b < rhs, '≤': -a * t + b <= rhs, '>': -a * t + b > rhs, '≥': -a * t + b >= rhs}[s]
    return Q(f'{p} solves {lin(-a, b)} {s} {N(rhs)} and gets x {s} {N(x)}. Explain the mistake. Use the value x = {N(t)} to show that {p}\'s answer cannot be right.',
             f'When dividing by −{a} the inequality sign must be reversed: x {FLIP[s]} {N(x)}. Check x = {N(t)}: {lin(-a, b)} = {N(-a * t + b)}, which {"does" if ok else "does not"} satisfy {s} {N(rhs)}, while {p}\'s answer says it {"does not" if ok else "does"}.',
             'B1 sign must reverse when dividing by a negative; B1 check with the value. [2]')


@t43.add('C2', (2, 3, 4), 'explain')
def t43_compare(r, D):
    v = r.randint(2, 9)
    p = person(r)
    return Q(f'{p} says that x > {v} and x ≥ {v + 1} describe the same set of numbers. Is this true if x must be an integer? Is it true if x can be any number? Explain.',
             f'For integers, yes: both give {v + 1}, {v + 2}, …. For any number, no: x = {N(v + 0.5)} satisfies x > {v} but not x ≥ {v + 1}.',
             'B1 integer case; B1 counter-example for real numbers. [2]')


def _ineq_c4(r, D):
    p = person(r)
    fee = r.choice([5, 8, 10, 12, 15])
    per = r.choice([3, 4, 6, 7.5, 2.5])
    budget = r.choice([60, 75, 80, 100, 120])
    nmax = int((budget - fee) // per)
    intro = f'{p} hires a bike in {city(r)}. There is a fixed charge of ${fee} and then {money(per)} per hour. {p} has ${budget} to spend. Let h be the number of whole hours.'
    parts = [
        lambda r: ('Write an inequality in h.', f'{fee} + {N(per)}h ≤ {budget}', 'B1 [1]'),
        lambda r: (f'Solve the inequality {fee} + {N(per)}h ≤ {budget}.', f'h ≤ {N(round((budget - fee) / per, 2))}', f'M1 {N(per)}h ≤ {budget - fee}; A1 [2]'),
        lambda r: ('Write down the greatest number of whole hours ' + p + ' can hire the bike for.', str(nmax), 'B1 rounds down [1]'),
        lambda r: ('Show the solution set for h on a number line, in words.', f'Closed circle at {N(round((budget - fee) / per, 2))}, line to the left down to 0.', 'B1 [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t43.add('C4', (2, 3, 4, 5), 'multi_step')(_ineq_c4)


@t43.add('C4', (3, 4, 5), 'multi_step')
def t43_double(r, D):
    a = r.randint(2, 4)
    b = r.randint(1, 6)
    w1 = r.randint(3, 6)
    P_lo, P_hi = 2 * ((a + 1) * w1 + b), 2 * ((a + 1) * (w1 + r.randint(2, 4)) + b)
    lo = Fr(P_lo - 2 * b, 2 * (a + 1))
    hi = Fr(P_hi - 2 * b, 2 * (a + 1))
    return Q(f'A rectangle has width w cm and length ({a}w + {b}) cm. Its perimeter is more than {P_lo} cm but no more than {P_hi} cm. (a) Write this information as a double inequality in w. (b) Solve the inequality. (c) Write down the possible whole-number values of w.',
             f'(a) {P_lo} < {lin(2 * a + 2, 2 * b, "w")} ≤ {P_hi} (b) {fr(lo)} < w ≤ {fr(hi)} (c) ' + ', '.join(str(i) for i in range(int(lo) + 1, int(hi) + 1)),
             f'(a) B1 [1] (b) M1 subtract {2 * b}; M1 ÷ {2 * a + 2}; A1 [3] (c) B1 [1]', marks=5)


t43.fixed('C1', (1, 2), [
    ('What does the symbol ≥ mean?', 'Greater than or equal to', 'B1 [1]', ['Greater than', 'Less than or equal to', 'Not equal to']),
    ('Which number satisfies 3x − 1 > 11? 3, 4, 4.5 or 0', '4.5', '3x > 12, x > 4. [1]', ['3', '4', '0']),
    ('Write down the largest integer that satisfies x < 6.', '5', 'B1 [1]'),
])
t43.fixed('C2', (2, 3), [
    ('Explain why multiplying both sides of 2 < 5 by −1 reverses the inequality.', '−2 > −5: multiplying by a negative reflects numbers through 0, so their order on the number line is reversed.', 'B1 example; B1 reason. [2]'),
    ('Explain why −3 < x < 2 has four integer solutions but −3 ≤ x ≤ 2 has six.', 'The strict inequalities exclude −3 and 2, leaving −2, −1, 0, 1 (four); the second includes both ends: −3, −2, −1, 0, 1, 2 (six).', 'B1 strict excludes ends; B1 correct count. [2]'),
])


# ----------------------------------------------------------- changing the subject
t44 = topic('Changing the subject of a formula', 'changing the subject of a formula', 'rearranging formulae')
REARR = [
    ('v = u + at', 'a', 'a = (v − u)/t', ['a = v − u − t', 'a = (v + u)/t', 'a = vt − u'], 'Subtract u, then divide by t.'),
    ('v = u + at', 'u', 'u = v − at', ['u = v + at', 'u = (v − a)/t', 'u = at − v'], 'Subtract at from both sides.'),
    ('P = 2l + 2w', 'l', 'l = (P − 2w)/2', ['l = P − 2w', 'l = (P − w)/2', 'l = P/2 + w'], 'Subtract 2w, then divide by 2.'),
    ('A = ½bh', 'h', 'h = 2A/b', ['h = A/2b', 'h = 2b/A', 'h = A − ½b'], 'Multiply by 2, then divide by b.'),
    ('y = mx + c', 'x', 'x = (y − c)/m', ['x = y − c − m', 'x = (y + c)/m', 'x = ym − c'], 'Subtract c, then divide by m.'),
    ('F = 1.8C + 32', 'C', 'C = (F − 32)/1.8', ['C = F/1.8 − 32', 'C = 1.8(F − 32)', 'C = (F + 32)/1.8'], 'Subtract 32, then divide by 1.8.'),
    ('s = d/t', 'd', 'd = st', ['d = s/t', 'd = t/s', 'd = s + t'], 'Multiply both sides by t.'),
    ('s = d/t', 't', 't = d/s', ['t = ds', 't = s/d', 't = d − s'], 'Multiply by t, then divide by s.'),
    ('A = πr²', 'r', 'r = √(A/π)', ['r = A/π²', 'r = √A/π', 'r = (A/π)²'], 'Divide by π, then square root.'),
    ('E = ½mv²', 'm', 'm = 2E/v²', ['m = E/2v²', 'm = 2Ev²', 'm = √(2E/v)'], 'Multiply by 2, divide by v².'),
    ('V = lwh', 'w', 'w = V/(lh)', ['w = V − lh', 'w = Vlh', 'w = lh/V'], 'Divide by lh.'),
    ('C = 2πr', 'r', 'r = C/(2π)', ['r = 2πC', 'r = C − 2π', 'r = 2π/C'], 'Divide by 2π.'),
    ('T = 5(n − 3)', 'n', 'n = T/5 + 3', ['n = T/5 − 3', 'n = 5T + 3', 'n = (T − 3)/5'], 'Divide by 5, then add 3.'),
    ('y = (x + 4)/3', 'x', 'x = 3y − 4', ['x = 3y + 4', 'x = y/3 − 4', 'x = (y − 4)/3'], 'Multiply by 3, then subtract 4.'),
]


@t44.add('C1', (1, 2, 3))
def t44_mcq(r, D):
    f, s, ans, ds, how = r.choice(REARR)
    stem = r.choice([f'Make {s} the subject of {f}.', f'Which formula shows {f} rearranged to make {s} the subject?', f'{f}. Rearrange to make {s} the subject.'])
    return MCQ(r, stem, ans, ds, how + ' [1]')


@t44.add('C3', (1, 2, 3, 4, 5))
def t44_param(r, D):
    a, b = r.randint(2, 9), r.randint(2, 12)
    v = r.choice(['p', 'q', 'k', 't', 'w'])
    kind = r.choice(['lin', 'frac', 'brack'] + (['sq', 'both'] if D >= 4 else []))
    if kind == 'lin':
        f, ans, key = f'y = {a}{v} + {b}', f'{v} = (y − {b})/{a}', f'Subtract {b} (M1); divide by {a} (A1).'
    elif kind == 'frac':
        f, ans, key = f'y = {v}/{a} − {b}', f'{v} = {a}(y + {b})', f'Add {b} (M1); multiply by {a} (A1).'
    elif kind == 'brack':
        f, ans, key = f'y = {a}({v} − {b})', f'{v} = y/{a} + {b}', f'Divide by {a} (M1); add {b} (A1).'
    elif kind == 'sq':
        f, ans, key = f'y = {a}{v}² + {b}', f'{v} = √((y − {b})/{a})', f'Subtract {b} (M1); divide by {a} (M1); square root (A1).'
    else:
        f, ans, key = f'{a}{v} + y = {b}{v} + x' if a < b else f'{b}{v} + y = {a}{v} + x', f'{v} = (y − x)/{abs(b - a)}', f'Collect {v} terms: {abs(b - a)}{v} = y − x (M1, M1); {v} = (y − x)/{abs(b - a)} (A1).'
        if a == b:
            return None
    return Q(r.choice([f'Make {v} the subject of the formula {f}.', f'Rearrange {f} to make {v} the subject.']), ans, key)


@t44.add('C2', (1, 2, 3, 4), 'explain')
def t44_err(r, D):
    a, b = r.randint(2, 9), r.randint(2, 12)
    p = person(r)
    kind = r.choice(['order', 'partial', 'sqrt'])
    if kind == 'order':
        return Q(f'{p} rearranges y = {a}x + {b} to make x the subject and writes x = y/{a} − {b}. Explain the mistake and write the correct formula.',
                 f'{p} divided by {a} before subtracting {b}, but only the y was divided. Correct: x = (y − {b})/{a} (or y/{a} − {N(Fr(b, a))}).',
                 'B1 explains error (must divide every term / subtract first); B1 correct formula. [2]')
    if kind == 'partial':
        return Q(f'{p} makes r the subject of A = {a}r + {b}s and writes r = A − {b}s ÷ {a}. Explain why this is not correct as written.',
                 f'Without brackets it means A − ({b}s ÷ {a}). The whole of A − {b}s must be divided: r = (A − {b}s)/{a}.',
                 'B1 brackets needed; B1 correct formula. [2]')
    return Q(f'{p} makes r the subject of A = {a}r² and writes r = √A ÷ {a}. Use A = {a * 9} to show that {p} is wrong, and give the correct formula.',
             f'When A = {a * 9}, r = 3 (since {a} × 9 = {a * 9}), but √{a * 9} ÷ {a} = {N(round(math.sqrt(a * 9) / a, 3))}. Correct: r = √(A/{a}).',
             'M1 test with the value; A1 correct formula. [2]')


@t44.add('C2', (2, 3, 4), 'explain')
def t44_inverse(r, D):
    f, s, ans, _, how = r.choice(REARR)
    return Q(f'Explain, step by step, how to rearrange {f} to make {s} the subject.', f'{how} {ans}', 'B1 correct inverse operations in order; B1 final formula. [2]')


def _subj_c4(r, D):
    kind = r.choice(['temp', 'speed', 'area'])
    if kind == 'temp':
        C = r.choice([15, 20, 25, 30, 35, 40, -10, -5])
        F = 1.8 * C + 32
        intro = f'The formula F = 1.8C + 32 converts a temperature in degrees Celsius (C) to degrees Fahrenheit (F). The temperature in {city(r)} one day is {N(F)} °F.'
        parts = [lambda r: ('Make C the subject of the formula.', 'C = (F − 32)/1.8', 'M1 subtract 32; A1 ÷ 1.8 [2]'),
                 lambda r: ('Find the temperature in degrees Celsius.', f'{N(C)} °C', f'M1 ({N(F)} − 32)/1.8; A1 [2]'),
                 lambda r: ('Find the temperature at which C and F are equal.', '−40', 'M1 C = 1.8C + 32; A1 −40 [2]')]
    elif kind == 'speed':
        s, t = r.choice([45, 60, 72, 80, 90]), r.choice([1.5, 2.5, 0.75, 3.2])
        intro = f'The formula s = d/t links average speed s (km/h), distance d (km) and time t (hours). A train travels at {s} km/h.'
        parts = [lambda r: ('Make t the subject of the formula.', 't = d/s', 'M1 × t; A1 ÷ s [2]'),
                 lambda r: (f'Find the time for a journey of {N(s * t)} km.', f'{N(t)} hours', 'M1; A1 [2]'),
                 lambda r: (f'Make d the subject and find the distance travelled in {N(t + 1)} hours.', f'd = st = {N(s * (t + 1))} km', 'B1 formula; B1 value [2]')]
    else:
        b, A = r.choice([4, 5, 6, 8]), r.choice([24, 30, 36, 48, 60])
        intro = f'The area of a trapezium is A = ½(a + b)h. A trapezium has area {A} cm², with parallel sides a cm and {b} cm and height h cm.'
        parts = [lambda r: ('Make h the subject of the formula.', 'h = 2A/(a + b)', 'M1 × 2; A1 ÷ (a + b) [2]'),
                 lambda r: (f'Find h when a = {b + 2}.', f'{sf(2 * A / (2 * b + 2), 3)} cm', f'M1 2 × {A} ÷ ({b + 2} + {b}); A1 {sf(2 * A / (2 * b + 2), 3)} [2]'),
                 lambda r: ('Make a the subject of the formula.', 'a = 2A/h − b', 'M1; A1 [2]')]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t44.add('C4', (2, 3, 4, 5), 'multi_step')(_subj_c4)


@t44.add('C4', (3, 4, 5), 'multi_step')
def t44_circle(r, D):
    A = r.choice([50, 100, 150, 200, 314, 500])
    rr = math.sqrt(A / math.pi)
    return Q(f'The area of a circular pond in {city(r)} is {A} m². (a) Make r the subject of A = πr². (b) Calculate the radius of the pond, to 1 decimal place. (c) Calculate the circumference of the pond, to 1 decimal place.',
             f'(a) r = √(A/π) (b) {fdp(rr, 1)} m (c) {fdp(2 * math.pi * rr, 1)} m',
             f'(a) M1 ÷ π; A1 √ [2] (b) M1 √({A}/π); A1 {fdp(rr, 1)} [2] (c) M1 2π × r; A1 {fdp(2 * math.pi * rr, 1)} [2]', marks=6)


t44.fixed('C1', (1, 2), [
    ('What is the subject of the formula A = lw?', 'A', 'The subject is the variable on its own on one side. [1]', ['l', 'w', 'lw']),
    ('Make x the subject of y = x − 7.', 'x = y + 7', 'Add 7 to both sides. B1 [1]'),
    ('Make b the subject of a = 4b.', 'b = a/4', 'B1 [1]'),
])
t44.fixed('C2', (2, 3), [
    ('Explain why changing the subject of a formula is like solving an equation.', 'You use the same inverse operations on both sides, in reverse order, to get the required letter on its own.', 'B1 inverse operations on both sides; B1 reverse order. [2]'),
])

CHAPTERS[4] = [t41, t42, t43, t44]


# =========================================================== 5 Angles
t51 = topic('Angles and parallel lines', 'parallel lines', 'alternate corresponding co-interior angles', 'calculating angles')
PAR_INTRO = 'Lines AB and CD are parallel, with A and C on the left. A straight line EF crosses AB at P and CD at Q, with E above AB and F below CD.'
PAR_ANG = {
    'PQD': (lambda a: a, 'alternate angles (with angle APQ)'),
    'CQP': (lambda a: 180 - a, 'co-interior angles add up to 180°'),
    'EPB': (lambda a: a, 'vertically opposite angles'),
    'BPQ': (lambda a: 180 - a, 'angles on a straight line add up to 180°'),
    'EPA': (lambda a: 180 - a, 'angles on a straight line (EPQ) add up to 180°'),
    'CQF': (lambda a: a, 'corresponding angles (with angle APQ)'),
}


@t51.add('C3', (1, 2, 3, 4))
def t51_find(r, D):
    a = r.randint(35, 145)
    if a == 90:
        a = 72
    name = r.choice(list(PAR_ANG))
    f, why = PAR_ANG[name]
    stem = f'{PAR_INTRO} Angle APQ = {a}°. Work out the size of angle {name}. Give a reason for your answer.'
    if D == 1:
        return MCQ(r, f'{PAR_INTRO} Angle APQ = {a}°. What is angle {name}?', f'{f(a)}°', [f'{180 - f(a)}°', f'{360 - a}°', f'{90 - a % 90 if a % 90 else 45}°', f'{f(a) + 10}°'], f'{name} = {f(a)}° ({why}). [1]')
    return Q(stem, f'{f(a)}°; {why}', f'B1 {f(a)}°; B1 reason: {why}.')


PAIRS = [('alternate', 'equal'), ('corresponding', 'equal'), ('co-interior', 'add up to 180°'), ('vertically opposite', 'equal')]


@t51.add('C1', (1, 2, 3))
def t51_pair(r, D):
    a = r.randint(40, 140)
    kind, rel = r.choice(PAIRS[:3])
    other = a if rel == 'equal' else 180 - a
    if a == 90:
        return None
    return MCQ(r, f'Two angles are {kind} angles between parallel lines. One of them is {a}°. What is the other angle?', f'{other}°',
               [f'{180 - other}°', f'{360 - a}°', f'{abs(90 - a)}°', f'{other + 5}°'], f'{kind.capitalize()} angles {rel}: {other}°. [1]')


@t51.add('C2', (1, 2, 3, 4), 'explain')
def t51_err(r, D):
    a = r.randint(40, 140)
    if a == 90:
        a = 75
    p = person(r)
    kind = r.choice(['co', 'alt', 'name'])
    if kind == 'co':
        return Q(f'{PAR_INTRO} Angle APQ = {a}°. {p} says angle CQP is also {a}° because they are alternate angles. Explain the mistake and give the correct size of angle CQP.',
                 f'APQ and CQP are on the same side of the transversal, between the parallel lines: they are co-interior, so they add up to 180°. CQP = {180 - a}°.',
                 'B1 identifies co-interior (not alternate); B1 180° − a. [2]')
    if kind == 'alt':
        return Q(f'{PAR_INTRO} {p} says that angle APQ and angle PQD add up to 180°. Is {p} correct? Explain.',
                 'No. APQ and PQD are alternate angles (a Z shape) on opposite sides of the transversal, so they are equal.', 'B1 alternate; B1 equal, not supplementary. [2]')
    return Q(f'Two lines are crossed by a transversal. A pair of corresponding angles are {a}° and {a + r.choice([2, 4, 5])}°. {p} says the two lines are parallel. Explain why {p} is wrong.',
             'If the lines were parallel the corresponding angles would be equal. They are not equal, so the lines are not parallel.', 'B1 corresponding angles equal for parallel lines; B1 conclusion. [2]')


@t51.add('C3', (2, 3, 4, 5))
def t51_alg(r, D):
    x = r.randint(8, 30)
    kind = r.choice(['eq', 'co'])
    a, b = r.randint(2, 5), r.randint(1, 4)
    if kind == 'eq':
        if a == b:
            a += 1
        c = r.randint(5, 40)
        d = a * x + c - b * x
        if d <= 0:
            return None
        ang = a * x + c
        stem = f'Two parallel lines are crossed by a transversal. A pair of alternate angles are ({lin(a, c)})° and ({lin(b, d)})°. Find x and the size of each angle.'
        ans = f'x = {x}; each angle is {ang}°'
        key = f'Alternate angles are equal: {lin(a, c)} = {lin(b, d)} (M1); collect terms: {lin(a - b, 0)} = {d - c} (M1); x = {x} (A1); angle = {a} × {x} + {c} = {ang}° (A1).'
    else:
        c = r.randint(5, 30)
        rest = 180 - (a + b) * x - c
        if rest <= 0:
            return None
        stem = f'Two parallel lines are crossed by a transversal. A pair of co-interior angles are ({lin(a, c)})° and ({lin(b, rest)})°. Find the value of x.'
        ans = f'x = {x}'
        key = f'Co-interior angles add to 180°: {lin(a + b, c + rest)} = 180 (M1); {a + b}x = {180 - c - rest} (M1); x = {x} (A1).'
    return Q(stem, ans, key)


def _par_c4(r, D):
    a, b = r.randint(35, 75), r.randint(35, 75)
    intro = f'Lines AB and CD are parallel. Triangle PQR has P on AB and both Q and R on CD, with Q to the left of R. Angle APQ = {a}° and angle BPR = {b}°.'
    parts = [
        lambda r: ('Work out angle PQR, giving a reason.', f'{a}° (alternate with angle APQ)', 'B1 value; B1 reason [2]'),
        lambda r: ('Work out angle PRQ, giving a reason.', f'{b}° (alternate with angle BPR)', 'B1 value; B1 reason [2]'),
        lambda r: ('Work out angle QPR.', f'{180 - a - b}°', f'M1 180 − {a} − {b} (angles on a straight line at P, or angle sum of triangle); A1 [2]'),
        lambda r: ('Use your answers to explain why the angles in a triangle add up to 180°.', 'Angles APQ, QPR and BPR lie on the straight line AB so add to 180°; APQ = PQR and BPR = PRQ (alternate), so the three angles of the triangle add to 180°.', 'B1 straight line; B1 alternate angles [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t51.add('C4', (2, 3, 4, 5), 'multi_step')(_par_c4)


@t51.add('C4', (3, 4, 5), 'multi_step')
def t51_zig(r, D):
    a, b = r.randint(25, 70), r.randint(25, 70)
    return Q(f'Lines AB and CD are parallel, with AB above CD. A point X lies between the lines. Angle ABX = {a}° and angle XDC = {b}°, where B and D are both on the right of X. Draw a line through X parallel to AB and use it to work out angle BXD. Give reasons.',
             f'{a + b}°', f'Line through X parallel to AB splits angle BXD into {a}° (alternate with ABX) [2] and {b}° (alternate with XDC) [2]; total {a + b}° [1].', marks=5)


t51.fixed('C1', (1, 2), [
    ('Which pair of angles between parallel lines are equal and form a Z shape?', 'Alternate angles', 'Alternate angles lie on opposite sides of the transversal, between the parallels. [1]', ['Co-interior angles', 'Corresponding angles', 'Angles on a straight line']),
    ('Which pair of angles between parallel lines add up to 180°?', 'Co-interior angles', 'Co-interior (allied) angles form a C or U shape. [1]', ['Alternate angles', 'Corresponding angles', 'Vertically opposite angles']),
    ('Corresponding angles form which shape?', 'An F shape', 'Corresponding angles are in matching positions at each intersection. [1]', ['A Z shape', 'A C shape', 'An X shape']),
    ('Write down the sum of angles on a straight line.', '180°', 'B1 [1]'),
])
t51.fixed('C2', (2, 3), [
    ('Explain how you can use corresponding angles to show that two lines are parallel.', 'Measure (or calculate) a pair of corresponding angles; if they are equal, the lines are parallel.', 'B1 corresponding angles; B1 equal implies parallel. [2]'),
    ('Explain why co-interior angles add up to 180°, using alternate angles.', 'One co-interior angle and its neighbour on the straight line add to 180°; that neighbour equals the other co-interior angle (alternate angles), so the co-interior angles add to 180°.', 'B1 straight line; B1 alternate angles. [2]'),
])


# ----------------------------------------------------------- polygons
t52 = topic('Interior and exterior angles of polygons', 'interior and exterior angles of polygons', 'polygons')
POLY = {3: 'triangle', 4: 'quadrilateral', 5: 'pentagon', 6: 'hexagon', 7: 'heptagon', 8: 'octagon', 9: 'nonagon', 10: 'decagon', 12: 'dodecagon'}
REG = [3, 4, 5, 6, 8, 9, 10, 12, 15, 18, 20, 24, 30, 36]


@t52.add('C1', (1, 2, 3))
def t52_sum(r, D):
    n = r.choice(list(POLY)[1:] if D > 1 else [4, 5, 6])
    s = (n - 2) * 180
    return MCQ(r, f'What is the sum of the interior angles of {art(POLY[n])}?', f'{s}°', [f'{n * 180}°', f'{(n - 1) * 180}°', f'{(n - 3) * 180 if n > 3 else 90}°', '360°'],
               f'({n} − 2) × 180° = {s}°. [1]')


@t52.add('C1', (1, 2, 3))
def t52_ext(r, D):
    n = r.choice(REG[1:])
    e = Fr(360, n)
    name = f'regular {POLY[n]}' if n in POLY else f'regular polygon with {n} sides'
    return MCQ(r, f'What is the size of each exterior angle of a {name}?', f'{fr(e)}°', [f'{fr(180 - e)}°', f'{fr(Fr(180, n))}°', f'{(n - 2) * 180}°', f'{fr(e * 2)}°'],
               f'Exterior angles add up to 360°: 360 ÷ {n} = {fr(e)}°. [1]')


@t52.add('C3', (1, 2, 3, 4, 5))
def t52_calc(r, D):
    n = r.choice(REG[2:])
    e = 360 // n
    i = 180 - e
    kind = r.choice(['int', 'sides_ext', 'sides_int'] if D >= 2 else ['int'])
    if kind == 'int':
        return Q(f'Work out the size of each interior angle of a regular polygon with {n} sides.', f'{i}°', f'Exterior = 360 ÷ {n} = {e}° (M1); interior = 180 − {e} = {i}° (A1).')
    if kind == 'sides_ext':
        return Q(f'Each exterior angle of a regular polygon is {e}°. How many sides does the polygon have?', str(n), f'360 ÷ {e} (M1) = {n} (A1).')
    return Q(f'Each interior angle of a regular polygon is {i}°. Work out the number of sides.', str(n), f'Exterior angle = 180 − {i} = {e}° (M1); 360 ÷ {e} = {n} (A1).')


@t52.add('C3', (2, 3, 4, 5))
def t52_missing(r, D):
    n = r.choice([5, 6, 7, 8])
    S = (n - 2) * 180
    angs = [r.randint(95, 165) for _ in range(n - 1)]
    miss = S - sum(angs)
    if not 40 < miss < 175:
        return None
    if D >= 4:
        k = r.randint(2, 3)
        known = angs[:n - 2]
        rest = S - sum(known)
        if rest % (k + 1):
            return None
        x = rest // (k + 1)
        if not 40 < x < 175 or not 40 < k * x < 179:
            return None
        return Q(f'A {POLY[n]} has angles {", ".join(str(a) + "°" for a in known)}, x° and {k}x°. Find the value of x.', f'x = {x}',
                 f'Sum = ({n} − 2) × 180 = {S}° (M1); {sum(known)} + {k + 1}x = {S} (M1); x = {x} (A1).')
    return Q(f'{n - 1} of the interior angles of a {POLY[n]} are {", ".join(str(a) + "°" for a in angs)}. Work out the size of the remaining angle.', f'{miss}°',
             f'Sum = ({n} − 2) × 180 = {S}° (M1); {S} − {sum(angs)} = {miss}° (A1).')


@t52.add('C2', (1, 2, 3, 4), 'explain')
def t52_possible(r, D):
    e = r.choice([25, 35, 50, 70, 80, 16, 14, 26])
    i = r.choice([100, 130, 145, 155, 125])
    p = person(r)
    if r.random() < 0.5:
        ok = 360 % e == 0
        return Q(f'{p} says it is possible to draw a regular polygon with an exterior angle of {e}°. Is {p} correct? Explain.',
                 f'{"Yes" if ok else "No"}: 360 ÷ {e} = {N(round(360 / e, 3))}, which {"is" if ok else "is not"} a whole number{f", so it has {360 // e} sides" if ok else ", so it cannot be the number of sides"}.',
                 'M1 360 ÷ exterior angle; A1 conclusion about whole number of sides. [2]')
    e2 = 180 - i
    ok = 360 % e2 == 0
    return Q(f'Can a regular polygon have interior angles of {i}°? Give a reason.',
             f'{"Yes" if ok else "No"}: exterior angle = {e2}° and 360 ÷ {e2} = {N(round(360 / e2, 3))}, {"a whole number" if ok else "not a whole number"}.',
             'M1 finds exterior angle and divides into 360; A1 conclusion. [2]')


@t52.add('C2', (2, 3, 4), 'explain')
def t52_err(r, D):
    n = r.choice([5, 6, 7, 8, 9, 10])
    p = person(r)
    return Q(f'{p} says the interior angles of a {POLY[n]} add up to {n} × 180° = {n * 180}° because it can be split into {n} triangles. Explain the mistake and give the correct total.',
             f'Joining one vertex to all the others splits the {POLY[n]} into {n - 2} triangles, not {n}, so the sum is ({n} − 2) × 180° = {(n - 2) * 180}°. (Splitting from a centre point gives {n} triangles but the 360° at the centre must be subtracted.)',
             'B1 explains n − 2 triangles (or subtract 360°); B1 correct total. [2]')


def _poly_c4(r, D):
    n = r.choice([5, 6, 8, 10, 12])
    e = Fr(360, n)
    i = 180 - e
    intro = r.choice([f'{person(r)} draws a regular {POLY[n]}.', f'A tile is in the shape of a regular {POLY[n]}.'])
    parts = [
        lambda r: ('Work out the size of one exterior angle.', f'{fr(e)}°', 'M1 360 ÷ n; A1 [2]'),
        lambda r: ('Work out the size of one interior angle.', f'{fr(i)}°', 'M1 180 − exterior; A1 [2]'),
        lambda r: ('Work out the sum of the interior angles.', f'{(n - 2) * 180}°', 'M1 (n − 2) × 180; A1 [2]'),
        lambda r: (f'Explain whether regular {POLY[n]}s will tessellate on their own.', f'{"Yes" if 360 % i == 0 else "No"}: 360 ÷ {fr(i)} = {sf(360 / float(i), 4)}, {"a whole number" if 360 % i == 0 else "not a whole number, so they leave gaps"}.', 'M1 360 ÷ interior angle; A1 conclusion [2]'),
        lambda r: (f'Two vertices next to each other are joined to the centre of the {POLY[n]}. Work out the angle at the centre.', f'{fr(e)}°', 'B1 360 ÷ n [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t52.add('C4', (2, 3, 4, 5), 'multi_step')(_poly_c4)


@t52.add('C4', (3, 4, 5), 'multi_step')
def t52_combo(r, D):
    a, b = r.sample([(3, 60), (4, 90), (6, 120), (8, 135), (12, 150), (5, 108), (10, 144)], 2)
    gap = 360 - a[1] - b[1]
    ok = gap > 0 and 360 % (180 - gap) == 0 if gap < 180 else False
    m = 360 // (180 - gap) if ok else None
    return Q(f'A regular {POLY[a[0]]} and a regular {POLY[b[0]]} are placed side by side so they meet at a point with no overlap. (a) Work out the angle needed to fill the gap at the point. (b) Could the gap be filled exactly by the interior angle of another regular polygon? If so, how many sides does it have?',
             f'(a) {gap}° (b) ' + (f'Yes, {m} sides (interior angle {gap}°).' if ok else 'No: no regular polygon has that interior angle.'),
             f'(a) M1 360 − {a[1]} − {b[1]}; A1 {gap}° [2] (b) M1 exterior = 180 − {gap}; M1 360 ÷ exterior; A1 conclusion [3]', marks=5) if gap > 0 else None


t52.fixed('C1', (1, 2), [
    ('What do the exterior angles of any convex polygon add up to?', '360°', 'Walking around the polygon you make one full turn. [1]', ['180°', '540°', 'It depends on the number of sides']),
    ('What do an interior angle and the exterior angle at the same vertex of a polygon add up to?', '180°', 'They form a straight line. [1]', ['90°', '360°', '270°']),
    ('Write down the size of each interior angle of a regular hexagon.', '120°', 'B1 [1]'),
])
t52.fixed('C2', (2, 3), [
    ('Explain why the interior angles of a quadrilateral add up to 360°.', 'A diagonal splits the quadrilateral into two triangles, each with angle sum 180°, so the total is 2 × 180° = 360°.', 'B1 two triangles; B1 2 × 180. [2]'),
    ('Explain why each interior angle of a regular polygon must be less than 180°.', 'Each exterior angle is 360 ÷ n, which is greater than 0, so the interior angle 180 − 360/n is less than 180°.', 'B1 exterior > 0; B1 conclusion. [2]'),
])


# ----------------------------------------------------------- constructions
t53 = topic('Constructions: perpendicular and angle bisectors', 'constructions', 'perpendicular bisectors', 'angle bisectors')
t53.fixed('C1', (1, 2, 3), [
    ('What is true about every point on the perpendicular bisector of AB?', 'It is the same distance from A and from B', 'Definition of the perpendicular bisector. [1]', ['It lies on the line AB', 'It is closer to A than to B', 'It is twice as far from A as from B']),
    ('What is true about every point on the bisector of angle ABC?', 'It is the same distance from the lines BA and BC', 'The angle bisector is the locus of points equidistant from the two arms. [1]', ['It is the same distance from A and C', 'It lies on the line AC', 'It is closer to B than to A']),
    ('Which equipment is needed to construct a perpendicular bisector?', 'A ruler and a pair of compasses', 'Construction uses a straight edge and compasses only. [1]', ['A protractor only', 'A protractor and ruler', 'A set square only']),
    ('What angle does the perpendicular bisector of AB make with AB?', '90°', 'It is perpendicular. [1]', ['45°', '180°', '60°']),
    ('Where does the perpendicular bisector of AB cross the line segment AB?', 'At the midpoint of AB', 'B1 [1]'),
    ('An angle of 84° is bisected. Write down the size of each of the two angles formed.', '42°', 'B1 [1]'),
])
t53.fixed('C2', (2, 3, 4), [
    ('When constructing the perpendicular bisector of AB, explain why the compasses must be set to more than half the length of AB.', 'If the radius is half AB or less, the arcs from A and B will not cross (or will only touch on AB), so there are no two points to join.', 'B1 arcs must intersect; B1 reason with half AB. [2]'),
    ('Explain why the compass width must stay the same for both arcs when constructing a perpendicular bisector.', 'The crossing points must be the same distance from A and from B; with equal radii they are, so they lie on the perpendicular bisector.', 'B1 equal radii; B1 equidistant points. [2]'),
    ('Explain why joining the two crossing points of equal arcs from A and B gives a line perpendicular to AB.', 'The four points A, B and the two crossing points form a rhombus (all sides equal radius); the diagonals of a rhombus bisect each other at right angles.', 'B1 rhombus; B1 diagonals perpendicular bisectors. [2]'),
    ('A student bisects an angle but changes the compass width between drawing the arcs from the two arms. Explain why the line drawn may not bisect the angle.', 'The construction needs the point where the arcs meet to be the same distance from both arms; with different radii it is not, so the angles formed are not equal.', 'B1 equal radii needed; B1 consequence. [2]'),
    ('Explain how to construct an angle of 45° using only a ruler and compasses.', 'Construct a perpendicular (90°) to a line, for example with the perpendicular bisector, then bisect the 90° angle to get 45°.', 'B1 construct 90°; B1 bisect it. [2]'),
])


@t53.add('C1', (1, 2, 3))
def t53_which(r, D):
    a, b = r.sample(['school', 'hospital', 'bus station', 'library', 'market', 'park'], 2)
    road1, road2 = r.sample(['North Road', 'River Road', 'Hill Street', 'Main Street', 'Station Road'], 2)
    if r.random() < 0.5:
        return MCQ(r, f'A new shop in {city(r)} must be the same distance from the {a} and the {b}. Which construction shows where the shop could be?',
                   f'The perpendicular bisector of the line joining the {a} and the {b}', [f'The bisector of the angle at the {a}', f'A circle centred on the {a}', f'The line joining the {a} and the {b}'],
                   'Points equidistant from two points lie on the perpendicular bisector. [1]')
    return MCQ(r, f'A lamp post must be the same distance from {road1} and {road2}, which meet at a junction. Which construction shows where it could be?',
               f'The bisector of the angle between {road1} and {road2}', [f'The perpendicular bisector of {road1}', f'A circle centred at the junction', f'A line parallel to {road1}'],
               'Points equidistant from two lines lie on the angle bisector. [1]')


@t53.add('C3', (1, 2, 3, 4, 5))
def t53_coord(r, D):
    vertical = r.random() < 0.5
    k = r.randint(-3, 6)
    p1, p2 = sorted(r.sample(range(-6, 12), 2))
    if (p2 - p1) % 2:
        p2 += 1
    m = (p1 + p2) // 2
    if vertical:
        A, B, line = (k, p1), (k, p2), f'y = {N(m)}'
    else:
        A, B, line = (p1, k), (p2, k), f'x = {N(m)}'
    stem = r.choice([f'A is the point ({N(A[0])}, {N(A[1])}) and B is the point ({N(B[0])}, {N(B[1])}). Write down the equation of the perpendicular bisector of AB.',
                     f'Find the equation of the line of points that are the same distance from ({N(A[0])}, {N(A[1])}) and ({N(B[0])}, {N(B[1])}).'])
    if D == 1:
        return MCQ(r, stem, line, [f'{"x" if vertical else "y"} = {N(m)}', f'{"y" if vertical else "x"} = {N(k)}', f'{"x" if vertical else "y"} = {N(k)}', f'y = x + {N(m)}'], f'AB is {"vertical" if vertical else "horizontal"}; midpoint has {"y" if vertical else "x"} = {N(m)}. [1]')
    return Q(stem, line, f'Midpoint of AB = ({N((A[0] + B[0]) / 2)}, {N((A[1] + B[1]) / 2)}) (M1); AB is {"vertical so the bisector is horizontal" if vertical else "horizontal so the bisector is vertical"}: {line} (A1).')


@t53.add('C3', (2, 3, 4))
def t53_steps(r, D):
    kind = r.choice(['perp', 'angle', 'point'])
    L = r.choice([6, 7, 8, 9, 10, 11])
    if kind == 'perp':
        return Q(f'Describe how to construct the perpendicular bisector of a line AB of length {L} cm, using only a ruler and compasses.',
                 f'Open the compasses to more than {N(L / 2)} cm. Draw arcs above and below AB from A, then with the same radius from B. Join the two points where the arcs cross.',
                 f'B1 radius more than half AB ({N(L / 2)} cm); B1 equal arcs from A and B; B1 join intersections.', marks=3)
    if kind == 'angle':
        a = r.choice([50, 64, 72, 80, 110, 124])
        return Q(f'Describe how to bisect an angle of {a}° at vertex B using a ruler and compasses, and state the size of the angles you will make.',
                 f'Arc from B cutting both arms; from these two points draw equal arcs that cross; join B to the crossing point. Each angle is {a // 2}°.',
                 f'B1 arc from vertex; B1 equal arcs from arm points and join; B1 {a // 2}°.', marks=3)
    return Q(f'Describe how to construct the perpendicular from a point P to a line, where P is {L} cm away from the line.',
             'Draw an arc centred at P cutting the line at two points; from these points draw equal arcs that cross on the other side; join P to the crossing point.',
             'B1 arc from P cutting line twice; B1 equal arcs from the two points; B1 join.', marks=3)


@t53.add('C2', (1, 2, 3, 4), 'explain')
def t53_locus(r, D):
    a, b = r.sample(['A', 'B', 'C', 'D'], 2)
    d = r.randint(3, 9)
    p = person(r)
    if r.random() < 0.5:
        return Q(f'{p} says that point X is on the perpendicular bisector of {a}{b} because X{a} = {d} cm and X{b} = {d + 1} cm. Explain whether {p} is correct.',
                 f'No. Points on the perpendicular bisector are equidistant from {a} and {b}; X{a} ≠ X{b}, so X is not on it.', 'B1 equidistant property; B1 conclusion. [2]')
    return Q(f'Point Y is {d} cm from line {a}{b} and {d} cm from line {a}C. Explain why Y lies on the bisector of angle {b}{a}C.',
             f'Y is the same distance from both arms of angle {b}{a}C, and every such point lies on the angle bisector.', 'B1 equal distances from both arms; B1 link to angle bisector. [2]')


@t53.add('C4', (2, 3, 4, 5), 'multi_step')
def t53_treasure(r, D):
    m = r.randint(3, 9)
    k = r.choice([1, 2, 10, 11])
    y1, y2 = m - r.randint(2, 5), None
    y2 = 2 * m - y1
    intro = f'On a coordinate grid, a tree stands at T({k}, {y1}) and a well at W({k}, {y2}). A treasure is buried at a point that is the same distance from T and W, and the same distance from the x-axis and the y-axis (in the first quadrant).'
    parts = [
        lambda r: ('Write down the equation of the perpendicular bisector of TW.', f'y = {m}', f'M1 midpoint ({k}, {m}); A1 y = {m} [2]'),
        lambda r: ('Write down the equation of the line of points equidistant from the x-axis and the y-axis in the first quadrant.', 'y = x', 'B1 bisector of the angle between the axes [1]'),
        lambda r: ('Find the coordinates of the treasure.', f'({m}, {m})', f'M1 intersect y = {m} with y = x; A1 ({m}, {m}) [2]'),
        lambda r: ('Explain which two constructions you would use to find the treasure on a map.', 'The perpendicular bisector of TW and the bisector of the angle between the axes.', 'B1 B1 [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


@t53.add('C4', (3, 4, 5), 'multi_step')
def t53_region(r, D):
    a, b = two_people(r)
    d = r.choice([4, 5, 6])
    AB = r.choice([8, 10, 12])
    return Q(f'Two radio masts, P and Q, are {AB} km apart. A phone signal is received from the nearer mast. (a) Describe the line on which the signal is equally strong from both masts. (b) A house is {d} km from P and {AB - d + r.choice([1, 2])} km from Q. Which mast does it receive its signal from? (c) Describe the region of points that are within {d} km of P and closer to Q than to P.',
             f'(a) The perpendicular bisector of PQ. (b) Mast P (it is nearer to P). (c) The part of the circle of radius {d} km centred at P that lies on Q\'s side of the perpendicular bisector.',
             f'(a) B1 perpendicular bisector [1] (b) M1 compare distances; A1 P [2] (c) B1 circle radius {d} km centre P; B1 side of bisector nearer Q [2]', marks=5)


# ----------------------------------------------------------- Pythagoras
t54 = topic("Pythagoras' theorem", "pythagoras' theorem", 'right-angled triangles', 'pythagoras')
TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (6, 8, 10), (9, 12, 15), (20, 21, 29), (9, 40, 41), (12, 16, 20), (15, 20, 25), (10, 24, 26)]


@t54.add('C1', (1, 2, 3))
def t54_right(r, D):
    a, b, c = r.choice(TRIPLES)
    k = r.choice([1, 1, 2]) if D > 1 else 1
    good = (a * k, b * k, c * k)
    bads = []
    for x, y, z in r.sample(TRIPLES, 4):
        z2 = z + r.choice([1, -1])
        if x * x + y * y != z2 * z2:
            bads.append(f'{x}, {y}, {z2}')
    opts, ans = mc(r, f'{good[0]}, {good[1]}, {good[2]}', bads)
    return Q('Which set of side lengths, in cm, makes a right-angled triangle? ' + '; '.join(opts), ans,
               f'{good[0]}² + {good[1]}² = {good[0] ** 2 + good[1] ** 2} = {good[2]}². [1]', opts)


@t54.add('C3', (1, 2, 3, 4, 5))
def t54_calc(r, D):
    find = r.choice(['hyp', 'short'])
    if D <= 2:
        a, b, c = r.choice(TRIPLES)
        exact = True
    else:
        a, b = r.randint(3, 15), r.randint(4, 20)
        c = math.hypot(a, b)
        exact = False
        if D >= 4:
            a, b = round(r.uniform(2, 12), 1), round(r.uniform(3, 15), 1)
            c = math.hypot(a, b)
    lab = r.choice([('AB', 'BC', 'AC', 'B'), ('PQ', 'QR', 'PR', 'Q'), ('XY', 'YZ', 'XZ', 'Y')])
    if find == 'hyp':
        stem = f'Triangle {lab[2][0]}{lab[3]}{lab[2][1]} has a right angle at {lab[3]}. {lab[0]} = {N(a)} cm and {lab[1]} = {N(b)} cm. Calculate the length of {lab[2]}' + ('.' if exact else ', giving your answer to 1 decimal place.')
        ans = f'{N(c) if exact else fdp(c, 1)} cm'
        key = f'{lab[2]}² = {N(a)}² + {N(b)}² = {N(round(a * a + b * b, 4))} (M1); {lab[2]} = √{N(round(a * a + b * b, 4))} = {ans} (A1).'
    else:
        if not exact:
            c = round(max(a, b) + r.uniform(1, 6), 1)
            short = math.sqrt(c * c - a * a)
        else:
            short = b
        stem = f'Triangle {lab[2][0]}{lab[3]}{lab[2][1]} has a right angle at {lab[3]}. The hypotenuse {lab[2]} = {N(c)} cm and {lab[0]} = {N(a)} cm. Calculate the length of {lab[1]}' + ('.' if exact else ', correct to 1 decimal place.')
        ans = f'{N(short) if exact else fdp(short, 1)} cm'
        key = f'{lab[1]}² = {N(c)}² − {N(a)}² = {N(round(c * c - a * a, 4))} (M1); {lab[1]} = {ans} (A1).'
    if D == 1:
        v = c if find == 'hyp' else short
        return MCQ(r, stem, ans, [f'{N(a + b)} cm', f'{N(round(math.sqrt(abs(c * c - a * a)) if find == "hyp" else math.hypot(c, a), 1))} cm', f'{N(round(v + 1, 1))} cm', f'{N(round((a * a + b * b) / 2, 1))} cm'], key)
    return Q(stem, ans, key)


@t54.add('C3', (2, 3, 4, 5))
def t54_coords(r, D):
    x1, y1 = r.randint(-5, 5), r.randint(-5, 5)
    a, b, c = r.choice(TRIPLES[:6]) if D <= 3 else (r.randint(1, 8), r.randint(1, 8), None)
    sx, sy = r.choice([1, -1]), r.choice([1, -1])
    x2, y2 = x1 + sx * a, y1 + sy * b
    d = math.hypot(a, b)
    ans = N(d) if c else fdp(d, 2)
    return Q(f'Calculate the distance between the points ({N(x1)}, {N(y1)}) and ({N(x2)}, {N(y2)})' + ('.' if c else ', correct to 2 decimal places.'), ans,
             f'Horizontal {a}, vertical {b} (M1); √({a}² + {b}²) = √{a * a + b * b} (M1); {ans} (A1).')


@t54.add('C2', (1, 2, 3, 4), 'explain')
def t54_err(r, D):
    a, b, c = r.choice(TRIPLES)
    p = person(r)
    kind = r.choice(['add', 'check', 'notsq'])
    if kind == 'add':
        wrong = math.sqrt(c * c + a * a)
        return Q(f'A right-angled triangle has hypotenuse {c} cm and another side {a} cm. {p} works out the third side as √({c}² + {a}²) = {fdp(wrong, 1)} cm. Explain the mistake and find the correct length.',
                 f'The missing side is shorter than the hypotenuse, so subtract: √({c}² − {a}²) = √{c * c - a * a} = {b} cm.', 'B1 should subtract for a shorter side; B1 correct length. [2]')
    if kind == 'check':
        x, y, z = a, b, c + 1
        return Q(f'{p} says a triangle with sides {x} cm, {y} cm and {z} cm is right-angled. Use Pythagoras\' theorem to decide whether {p} is correct.',
                 f'{x}² + {y}² = {x * x + y * y} but {z}² = {z * z}. They are not equal, so the triangle is not right-angled.', 'M1 compares sum of squares of shorter sides with square of longest; A1 conclusion. [2]')
    return Q(f'{p} says: "In a right-angled triangle with shorter sides {a} cm and {b} cm, the hypotenuse is {a} + {b} = {a + b} cm." Explain why this cannot be true.',
             f'The hypotenuse must be shorter than the sum of the other two sides (triangle inequality). By Pythagoras it is √({a}² + {b}²) = {c} cm.', 'B1 reason; B1 correct value. [2]')


def _pyth_c4(r, D):
    kind = r.choice(['ladder', 'tv', 'iso', 'field'])
    if kind == 'ladder':
        L = r.choice([5, 6, 6.5, 7, 8])
        f = r.choice([1.2, 1.5, 1.8, 2, 2.5])
        h = math.sqrt(L * L - f * f)
        intro = f'A ladder {N(L)} m long leans against a vertical wall in {city(r)}. The foot of the ladder is {N(f)} m from the base of the wall on horizontal ground.'
        parts = [lambda r: ('Calculate how high up the wall the ladder reaches, to 2 decimal places.', f'{fdp(h, 2)} m', f'M1 {N(L)}² − {N(f)}²; A1 {fdp(h, 2)} [2]'),
                 lambda r: ('Safety rules say the height should be about 4 times the distance from the wall. Is the ladder safe? Explain.', f'{"Yes" if h / f >= 3.8 else "No"}: {fdp(h, 2)} ÷ {N(f)} = {fdp(h / f, 2)}', 'M1 ratio; A1 conclusion [2]'),
                 lambda r: (f'The foot of the ladder slips until the top is 0.3 m lower down the wall. Calculate the new distance of the foot from the wall, to 2 decimal places.', f'{fdp(math.sqrt(L * L - (h - 0.3) ** 2), 2)} m', f'M1 {N(L)}² − ({fdp(h - 0.3, 2)})²; A1 {fdp(math.sqrt(L * L - (h - 0.3) ** 2), 2)} [2]')]
    elif kind == 'tv':
        w, hh = r.choice([(48, 27), (64, 36), (80, 45), (96, 54), (112, 63)])
        dg = math.hypot(w, hh)
        intro = f'A television screen is a rectangle {w} cm wide and {hh} cm high.'
        parts = [lambda r: ('Calculate the length of the diagonal of the screen, to the nearest centimetre.', f'{round(dg)} cm', f'M1 {w}² + {hh}²; A1 {round(dg)} [2]'),
                 lambda r: ('Screen sizes are given in inches (1 inch = 2.54 cm). Work out the screen size to the nearest inch.', f'{round(dg / 2.54)} inches', 'M1 ÷ 2.54; A1 [2]'),
                 lambda r: ('Calculate the area of the screen.', f'{w * hh} cm²', 'B1 [1]')]
    elif kind == 'iso':
        b = r.choice([6, 8, 10, 12, 16])
        s = r.choice([b // 2 + 3, b // 2 + 5, b])
        h = math.sqrt(s * s - (b / 2) ** 2)
        intro = f'An isosceles triangle has two sides of length {s} cm and a base of {b} cm.'
        parts = [lambda r: ('Calculate the perpendicular height of the triangle, to 2 decimal places.', f'{fdp(h, 2)} cm', f'M1 {s}² − {b // 2}²; A1 {fdp(h, 2)} [2]'),
                 lambda r: ('Calculate the area of the triangle, to 1 decimal place.', f'{fdp(0.5 * b * h, 1)} cm²', 'M1 ½ × base × height; A1 [2]'),
                 lambda r: ('Write down the perimeter of the triangle.', f'{2 * s + b} cm', 'B1 [1]')]
    else:
        a, b = r.choice([(60, 80), (45, 60), (90, 120), (50, 120), (80, 150)])
        dg = math.hypot(a, b)
        intro = f'A rectangular park is {a} m by {b} m. {person(r)} walks from one corner to the opposite corner.'
        parts = [lambda r: ('Calculate the distance saved by walking along the diagonal instead of along two sides.', f'{N(a + b - dg)} m', f'M1 √({a}² + {b}²) = {N(dg)}; A1 {a + b} − {N(dg)} = {N(a + b - dg)} [2]'),
                 lambda r: ('Walking at 1.5 m/s, how many seconds does the diagonal route take?', f'{N(round(dg / 1.5, 1))} s', 'M1; A1 [2]'),
                 lambda r: ('Explain why the diagonal is always shorter than the two sides added together.', 'The straight line is the shortest path; in a triangle any side is shorter than the sum of the other two.', 'B1 [1]')]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t54.add('C4', (2, 3, 4, 5), 'multi_step')(_pyth_c4)


@t54.add('C4', (3, 4, 5), 'multi_step')
def t54_cuboid(r, D):
    l, w, h = r.choice([(3, 4, 12), (6, 8, 24), (2, 3, 6), (4, 4, 7), (5, 12, 84)])
    base = math.hypot(l, w)
    sp = math.hypot(base, h)
    return Q(f'A cuboid measures {l} cm by {w} cm by {h} cm. (a) Calculate the length of the diagonal of the {l} cm by {w} cm base. (b) Calculate the length of the longest straight rod that fits inside the cuboid (from one corner to the opposite corner).',
             f'(a) {N(round(base, 2))} cm (b) {N(round(sp, 2))} cm', f'(a) M1 √({l}² + {w}²); A1 {N(round(base, 2))} [2] (b) M1 √(base diagonal² + {h}²); M1 √({N(round(base * base, 4))} + {h * h}); A1 {N(round(sp, 2))} [3]', marks=5)


t54.fixed('C1', (1, 2), [
    ('In a right-angled triangle, which side is the hypotenuse?', 'The side opposite the right angle', 'The hypotenuse is the longest side, opposite the 90° angle. [1]', ['The shortest side', 'Any side next to the right angle', 'The base of the triangle']),
    ("Which equation is Pythagoras' theorem for a right-angled triangle with hypotenuse c and other sides a and b?", 'a² + b² = c²', 'B1 [1]', ['a + b = c', 'a² − b² = c²', 'a² + c² = b²']),
    ('A right-angled triangle has shorter sides 6 cm and 8 cm. Write down the length of the hypotenuse.', '10 cm', '36 + 64 = 100. B1 [1]'),
])
t54.fixed('C2', (2, 3), [
    ("Explain how to use Pythagoras' theorem to check whether a triangle with sides 9 cm, 12 cm and 15 cm is right-angled.", '9² + 12² = 81 + 144 = 225 = 15², so the triangle is right-angled (the converse of Pythagoras).', 'M1 squares of the two shorter sides added; A1 compared with longest side squared. [2]'),
    ('Explain why the hypotenuse is always the longest side of a right-angled triangle.', 'c² = a² + b² is bigger than a² and bigger than b², so c is bigger than a and b.', 'B1 c² is the sum of two positive squares; B1 conclusion. [2]'),
])

CHAPTERS[5] = [t51, t52, t53, t54]


# =========================================================== 6 Statistical investigations
# (question, variables, hypothesis, method, source, population)
INV = [
    ('whether students who sleep more get higher test scores', 'hours of sleep and test scores', 'Students who sleep more hours get higher test scores.', 'a questionnaire about sleep, with scores from the latest test', 'primary', 'students in the school'),
    ('whether Stage 9 boys are taller than Stage 9 girls', 'heights of boys and girls', 'Stage 9 boys are taller on average than Stage 9 girls.', 'measuring heights with a tape measure', 'primary', 'Stage 9 students'),
    ('whether the population of {c} has grown faster than the national population since 2000', 'population figures for each year', 'The population of {c} has grown faster than the national population.', 'census records from a government website', 'secondary', 'all the years since 2000'),
    ('which sport is the most popular among students', 'favourite sport of each student', 'Football is the most popular sport among students.', 'a questionnaire with a list of sports', 'primary', 'students in the school'),
    ('whether hotter days mean more ice creams are sold at a café in {c}', 'daily temperature and number of ice creams sold', 'More ice creams are sold on hotter days.', "the café's sales records and weather data", 'secondary', 'days in one summer'),
    ('how long people wait for a bus at a stop in {c}', 'waiting times in minutes', 'Most people wait less than 10 minutes for a bus.', 'observing and timing people at the bus stop', 'primary', 'people using the bus stop'),
    ('whether people with longer arms also have longer legs', 'arm length and leg length', 'People with longer arms have longer legs.', 'measuring a sample of people', 'primary', 'adults in the town'),
    ('how many books teenagers read each month', 'number of books read per month', 'Most teenagers read fewer than 3 books a month.', 'a questionnaire', 'primary', 'teenagers in the town'),
    ('whether a six-sided dice is biased', 'the score on each roll', 'The dice lands on 6 more often than on the other numbers.', 'an experiment rolling the dice many times', 'primary', 'all possible rolls of the dice'),
    ('whether older cars use more fuel per kilometre', 'age of the car and fuel used per 100 km', 'Older cars use more fuel per 100 km.', 'a database of car test results', 'secondary', 'cars on the road'),
    ('whether students who use a phone more spend less time on homework', 'daily phone time and daily homework time', 'Students with more phone time do less homework.', 'a questionnaire or a one-week diary', 'primary', 'students in Stage 9'),
    ('how much rain falls in {c} in each month', 'monthly rainfall in mm', 'Most rain falls in the middle of the year.', 'weather records from the national weather service', 'secondary', 'months over the last 10 years'),
    ('whether people can estimate one minute more accurately with practice', 'estimated times before and after practice', 'Estimates are closer to 60 seconds after practice.', 'an experiment with a stopwatch', 'primary', 'students in the class'),
    ('whether bigger houses in {c} cost more to rent', 'floor area and monthly rent', 'Houses with a larger floor area have higher rents.', 'property websites', 'secondary', 'houses for rent in the city'),
    ('which colour of car is most common in a car park', 'colour of each car', 'White is the most common car colour.', 'observing and tallying cars', 'primary', 'cars in the car park'),
]
VARS = [
    ('the number of goals scored in a match', 'Discrete'), ('the time taken to run 100 m', 'Continuous'), ('the colour of a car', 'Categorical'),
    ('the mass of a newborn baby', 'Continuous'), ('the number of people in a household', 'Discrete'), ('a person\'s favourite fruit', 'Categorical'),
    ('the height of a sunflower', 'Continuous'), ('shoe size', 'Discrete'), ('the number of text messages sent in a day', 'Discrete'),
    ('the temperature at noon', 'Continuous'), ('the country a person was born in', 'Categorical'), ('the volume of water in a bottle', 'Continuous'),
    ('the number of pets owned', 'Discrete'), ('the type of transport used to get to school', 'Categorical'), ('the length of a leaf', 'Continuous'),
    ('the score on a dice', 'Discrete'), ('the distance travelled to school', 'Continuous'), ('the month in which a person was born', 'Categorical'),
]
DIAG = {
    'hours of sleep and test scores': 'A scatter graph, because both variables are numerical and we want to see whether they are related',
    'heights of boys and girls': 'Two frequency polygons on the same axes (or a back-to-back stem-and-leaf diagram), to compare the two distributions',
    'population figures for each year': 'A time series graph, because the data change over time',
    'favourite sport of each student': 'A bar chart or pie chart, because the data are categorical',
    'daily temperature and number of ice creams sold': 'A scatter graph, because both variables are numerical and we want to see whether they are related',
    'waiting times in minutes': 'A frequency diagram or frequency polygon, because the times are continuous data that can be grouped',
    'arm length and leg length': 'A scatter graph, because both variables are numerical and we want to see whether they are related',
    'number of books read per month': 'A bar chart, because the data are discrete',
    'the score on each roll': 'A bar chart of the frequency of each score, because the data are discrete',
    'age of the car and fuel used per 100 km': 'A scatter graph, because both variables are numerical and we want to see whether they are related',
    'daily phone time and daily homework time': 'A scatter graph, because both variables are numerical and we want to see whether they are related',
    'monthly rainfall in mm': 'A time series graph (or a bar chart by month), to show how rainfall changes through the year',
    'estimated times before and after practice': 'A back-to-back stem-and-leaf diagram or two frequency polygons, to compare before and after practice',
    'floor area and monthly rent': 'A scatter graph, because both variables are numerical and we want to see whether they are related',
    'colour of each car': 'A bar chart or pie chart, because the data are categorical',
}
PEOPLE_POP = ('students in the school', 'Stage 9 students', 'people using the bus stop', 'adults in the town', 'teenagers in the town', 'students in Stage 9', 'students in the class')
DTYPE_WHY = {'Discrete': 'it can only take separate values (it is counted)', 'Continuous': 'it is measured and can take any value in a range',
             'Categorical': 'it is a description or category, not a number'}


def _inv(r):
    q, v, h, m, s, pop = r.choice(INV)
    c = city(r)
    return q.format(c=c), v, h.format(c=c), m, s, pop


t61 = topic('Planning a statistical investigation', 'planning a statistical investigation', 'choosing data to collect')


@t61.add('C1', (1, 2, 3))
def t61_dtype(r, D):
    v, t = r.choice(VARS)
    stem = r.choice([f'What type of data is {v}?', f'{person(r)} records {v}. What type of data is this?'])
    return MCQ(r, stem, t, [x for x in ('Discrete', 'Continuous', 'Categorical') if x != t] + ['Secondary'], f'{t}: {DTYPE_WHY[t]}. [1]')


@t61.add('C1', (1, 2, 3))
def t61_source(r, D):
    q, v, h, m, s, pop = _inv(r)
    p = person(r)
    ans = 'Primary data' if s == 'primary' else 'Secondary data'
    return MCQ(r, f'{p} investigates {q} using {m}. What kind of data is this?', ans, ['Secondary data' if s == 'primary' else 'Primary data', 'Categorical data only', 'Biased data'],
               f'{"Collected by the investigator" if s == "primary" else "Collected by someone else"} → {ans.lower()}. [1]')


@t61.add('C2', (1, 2, 3, 4), 'explain')
def t61_hyp(r, D):
    q, v, h, m, s, pop = _inv(r)
    p = person(r)
    stem = r.choice([f'{p} wants to investigate {q}. Write a hypothesis that {p} could test.',
                     f'{p} is planning an investigation into {q}. Write down a suitable hypothesis and state what data {p} needs to collect.'])
    return Q(stem, f'Hypothesis, e.g. "{h}" Data: {v}.', 'B1 testable statement (not a question); B1 data identified. [2]')


@t61.add('C2', (1, 2, 3, 4), 'explain')
def t61_method(r, D):
    q, v, h, m, s, pop = _inv(r)
    p = person(r)
    stem = r.choice([f'{p} is investigating {q}. {p} plans to use {m}. Explain whether this will give {s} or {"secondary" if s == "primary" else "primary"} data, and give one advantage of this method.',
                     f'To investigate {q}, {p} decides to use {m}. Is this primary or secondary data? Give one advantage and one disadvantage of using it.'])
    adv = 'collected for exactly this purpose, so it fits the question and you know how it was collected' if s == 'primary' else 'quick and cheap to obtain, often a large amount of data'
    dis = 'it takes time and effort to collect' if s == 'primary' else 'it may not be exactly what is needed, may be out of date, and you do not know how carefully it was collected'
    return Q(stem, f'{s.capitalize()} data. Advantage: {adv}. Disadvantage: {dis}.', 'B1 correct type with reason; B1 sensible advantage (and disadvantage). [2]')


@t61.add('C2', (2, 3, 4), 'explain')
def t61_dtype_explain(r, D):
    v, t = r.choice(VARS)
    p = person(r)
    wrong = r.choice([x for x in ('Discrete', 'Continuous', 'Categorical') if x != t])
    return Q(f'{p} says that {v} is {wrong.lower()} data. Is {p} correct? Explain your answer.', f'No. It is {t.lower()} data because {DTYPE_WHY[t]}.',
             'B1 correct type; B1 reason. [2]')


@t61.add('C2', (2, 3, 4), 'explain')
def t61_question(r, D):
    q, v, h, m, s, pop = _inv(r)
    p = person(r)
    return Q(f'{p} is investigating {q}. Explain why the question "{r.choice(["Is this a good topic?", "What do you think about it?", "Do you agree with the hypothesis?"])}" would not be a useful question to ask, and suggest a better one.',
             f'It is vague and will not give data that can be analysed. A better question asks for specific data on {v}, with clear answer options or a number.', 'B1 reason (vague / not measurable); B1 improved specific question. [2]')


@t61.add('C3', (1, 2, 3, 4, 5))
def t61_classes(r, D):
    lo = r.choice([140, 2, 10, 30, 0, 45])
    w = r.choice([5, 10, 2, 4, 20])
    n = r.choice([4, 5, 6])
    hi = lo + w * n - r.randint(1, w)
    unit, what = r.choice([('cm', 'heights'), ('minutes', 'journey times'), ('kg', 'masses'), ('seconds', 'reaction times')])
    classes = [f'{N(lo + i * w)} ≤ x < {N(lo + (i + 1) * w)}' for i in range(n)]
    return Q(f'{person(r)} collects the {what} of 40 students. The smallest is {lo} {unit} and the largest is {hi} {unit}. Design {n} equal class intervals of width {w} {unit} for a frequency table, starting at {lo} {unit}.',
             '; '.join(classes), 'B1 correct width and start; B1 classes do not overlap and cover the range (use ≤ x <).')


@t61.add('C3', (2, 3, 4, 5))
def t61_plan(r, D):
    q, v, h, m, s, pop = _inv(r)
    p = person(r)
    return Q(f'{p} wants to investigate {q}. Describe a plan for the investigation. Include (i) a hypothesis, (ii) the data to collect, (iii) how to collect it, (iv) how to present the results.',
             f'(i) {h} (ii) {v} (iii) {m}, using a sample of a sensible size from {pop} (iv) a suitable diagram (e.g. bar chart for categories, scatter graph for two measured variables, frequency polygon for grouped data) and averages.',
             'B1 hypothesis; B1 data; B1 method and sample; B1 presentation. [4]', marks=4)


@t61.add('C3', (2, 3, 4))
def t61_sheet(r, D):
    q, v, h, m, s, pop = _inv(r)
    return Q(f'Design a data collection sheet that could be used in an investigation into {q}.', f'A table with columns for {v} (and a tally/frequency column if grouped), with space for each person or item.',
             'B1 suitable headings; B1 suitable categories or groups / space for values. [2]', marks=2)


def _plan_c4(r, D):
    q, v, h, m, s, pop = _inv(r)
    p = person(r)
    n = r.choice([30, 40, 50, 60, 80, 100])
    intro = f'{p} is investigating {q}.'
    parts = [
        lambda r: ('Write a hypothesis for the investigation.', h, 'B1 [1]'),
        lambda r: ('State the data that needs to be collected and whether it is primary or secondary.', f'{v}; {s} data', 'B1 data; B1 type [2]'),
        lambda r: (f'{p} uses a sample of size {n}. Give one reason why this is better than a sample of size 10.', 'A larger sample is more reliable / representative and reduces the effect of unusual values.', 'B1 [1]'),
        lambda r: ('Suggest a suitable diagram to display the results and give a reason.', DIAG[v], 'B1 diagram; B1 reason linked to data type [2]'),
        lambda r: ('Describe one problem that could happen when collecting the data, and how to reduce it.', 'e.g. people give inaccurate answers / measurements are inaccurate; use clear questions, repeat measurements, use a larger random sample.', 'B1 problem; B1 solution [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t61.add('C4', (2, 3, 4, 5), 'multi_step')(_plan_c4)
t61.fixed('C1', (1, 2), [
    ('What is a hypothesis in a statistical investigation?', 'A statement that can be tested using data', 'A hypothesis is a testable statement, not a question. [1]', ['A question you ask people', 'A table of results', 'A diagram of the data']),
    ('A student uses data downloaded from a government website. What type of data is this?', 'Secondary data', 'It was collected by someone else. [1]', ['Primary data', 'Biased data', 'Continuous data']),
    ('Write down one example of continuous data.', 'e.g. height, mass, time, temperature', 'B1 any measured quantity [1]'),
    ('Write down the four main stages of the data-handling cycle.', 'Plan (specify the problem), collect data, process and represent the data, interpret and discuss the results.', 'B1 all four in order [1]'),
])
t61.fixed('C2', (2, 3), [
    ('Explain why it is important to write the hypothesis before collecting data.', 'It decides what data to collect and how; without it the data may not answer the question.', 'B1 guides data collection; B1 consequence. [2]'),
    ('Explain the difference between primary and secondary data, giving an example of each.', 'Primary data is collected by the person doing the investigation (e.g. a class survey); secondary data was collected by someone else (e.g. census data).', 'B1 each with example. [2]'),
])


# ----------------------------------------------------------- sampling
t62 = topic('Sampling methods and sample size', 'sampling methods', 'sample size')
GROUPS = [('boys', 'girls'), ('Stage 7 students', 'Stage 8 students'), ('full-time workers', 'part-time workers'), ('adults', 'children'), ('day students', 'boarding students')]


@t62.add('C3', (1, 2, 3, 4, 5))
def t62_prop(r, D):
    a, b = r.choice(GROUPS)
    k = r.choice([2, 4, 5, 10, 20])
    na, nb = r.randint(6, 40) * k, r.randint(6, 40) * k
    tot = na + nb
    from math import gcd
    g = gcd(na, nb)
    n = (tot // g) * r.choice([1, 2]) if tot // g <= 60 else None
    if not n:
        n = r.choice([40, 50, 60])
        if (na * n) % tot:
            return None
    sa, sb = na * n // tot, nb * n // tot
    if D >= 4:
        c3 = r.randint(6, 30) * k
        tot3 = tot + c3
        if (na * n) % tot3 or (nb * n) % tot3 or (c3 * n) % tot3:
            return None
        return Q(f'A club has {na} {a}, {nb} {b} and {c3} visitors. A sample of {n} members is chosen so that each group is represented in proportion to its size. How many of each should be chosen?',
                 f'{na * n // tot3} {a}, {nb * n // tot3} {b}, {c3 * n // tot3} visitors', f'Total {tot3} (M1); each group × {n}/{tot3} (M1); {na * n // tot3}, {nb * n // tot3}, {c3 * n // tot3} (A1).', marks=3)
    return Q(f'A school in {city(r)} has {na} {a} and {nb} {b}. {person(r)} takes a sample of {n} students in proportion to the size of each group. How many {a} and how many {b} should be in the sample?',
             f'{sa} {a} and {sb} {b}', f'{na}/{tot} × {n} (M1) = {sa}; {nb}/{tot} × {n} = {sb} (A1).')


@t62.add('C3', (1, 2, 3, 4))
def t62_system(r, D):
    N_ = r.choice([200, 300, 400, 500, 600, 800, 1200])
    n = r.choice([20, 25, 40, 50])
    k = N_ // n
    start = r.randint(1, k)
    return Q(f'A list of {N_} customers is numbered 1 to {N_}. A sample of {n} is taken by choosing a random starting number from 1 to {k} and then every {k}th customer. The starting number is {start}. Write down the first four customers in the sample, and explain why every customer had the same chance of being chosen.',
             f'{start}, {start + k}, {start + 2 * k}, {start + 3 * k}. Each starting number from 1 to {k} is equally likely, and each customer belongs to exactly one starting group.',
             f'B1 interval {N_} ÷ {n} = {k}; B1 four numbers; B1 reason.', marks=3)


@t62.add('C1', (1, 2, 3))
def t62_mcq(r, D):
    for _ in range(50):
        q, v, h, m, s, pop = _inv(r)
        if pop in PEOPLE_POP:
            break
    n = r.choice([5, 8, 10])
    return MCQ(r, f'{person(r)} is investigating {q}. Which sample is likely to give the most reliable results?', f'A random sample of {n * 10} from {pop}',
               [f'The first {n} people {person(r)} meets', f'A random sample of {n} from {pop}', f'{n * 10} of {person(r)}\'s friends', f'Everyone who volunteers on the first day'],
               'Large and random → more representative and reliable. [1]')


@t62.add('C1', (1, 2, 3))
def t62_def(r, D):
    q, v, h, m, s, pop = _inv(r)
    return MCQ(r, f'In an investigation into {q}, what is the population?', pop.capitalize(), ['The people who answer the questionnaire', 'Only the first 10 results', 'The mean of the data'],
               'The population is the whole group the investigation is about. [1]')


@t62.add('C2', (1, 2, 3, 4), 'explain')
def t62_size(r, D):
    q, v, h, m, s, pop = _inv(r)
    n = r.choice([4, 5, 6, 8, 10])
    p = person(r)
    stem = r.choice([f'{p} investigates {q}, using a sample of {n}. Explain why this sample size is not suitable, and suggest a better sample size.',
                     f'{p} collects data from only {n} cases to investigate {q}. Give one reason why {p}\'s conclusion might not be reliable.'])
    return Q(stem, f'A sample of {n} is too small: a few unusual results have a large effect, so it may not represent {pop}. A sample of about 30 to 100 (or more) would be better.',
             'B1 too small / unrepresentative; B1 sensible larger size or consequence. [2]')


@t62.add('C2', (1, 2, 3, 4), 'explain')
def t62_why_sample(r, D):
    q, v, h, m, s, pop = _inv(r)
    p = person(r)
    return Q(f'{p} is investigating {q}. Give two reasons why {p} might use a sample rather than collecting data from all of {pop}.',
             'A sample is quicker and cheaper; it may be impossible or impractical to reach every member of the population (or testing may destroy items).',
             'B1 B1 two valid reasons (time, cost, practicality). [2]')


@t62.add('C2', (2, 3, 4), 'explain')
def t62_random(r, D):
    N_ = r.choice([300, 450, 600, 900, 1200])
    n = r.choice([30, 40, 50, 60])
    p = person(r)
    return Q(f'A school has {N_} students. {p} wants a random sample of {n}. Describe how {p} could choose the sample so that every student has an equal chance of being selected.',
             f'Number the students 1 to {N_}; use a random number generator (or names in a hat) to pick {n} different numbers; ignore repeats.',
             'B1 numbered list; B1 random selection method with no repeats. [2]')


@t62.add('C2', (2, 3, 4), 'explain')
def t62_compare(r, D):
    a, b = r.choice(GROUPS)
    na, nb = r.randint(100, 500), r.randint(100, 500)
    p = person(r)
    return Q(f'A college has {na} {a} and {nb} {b}. {p} takes a sample of 50 {a} and 50 {b}. Explain why this sample does not represent the college fairly.',
             f'The groups are different sizes ({na} and {nb}), so taking equal numbers over-represents the smaller group. The sample should be in proportion: about {round(100 * na / (na + nb))} {a} and {100 - round(100 * na / (na + nb))} {b}.',
             'B1 groups different sizes; B1 proportional sizes suggested. [2]')


def _samp_c4(r, D):
    a, b = r.choice(GROUPS)
    na, nb = r.choice([120, 180, 240, 300, 360]), r.choice([80, 120, 160, 200, 240])
    tot = na + nb
    n = r.choice([20, 40, 60])
    if (na * n) % tot:
        n = tot // 10 if tot % 10 == 0 else 50
    sa = round(na * n / tot)
    q, v, h, m, s, pop = _inv(r)
    p = person(r)
    intro = f'{p} is investigating {q}. The population is made up of {na} {a} and {nb} {b}.'
    parts = [
        lambda r: (f'{p} wants a sample of {n}. Work out how many {a} should be in the sample if the groups are represented in proportion.', str(sa), f'M1 {na}/{tot} × {n}; A1 {sa} [2]'),
        lambda r: (f'Describe how {p} could choose the {a} at random.', f'Number the {na} {a}; use random numbers to choose the required number, ignoring repeats.', 'B1 B1 [2]'),
        lambda r: ('Explain why a sample of 5 would not be suitable.', 'Too small to be representative; results unreliable.', 'B1 [1]'),
        lambda r: (f'{p} asks only people who arrive first in the morning. Explain why this sample may be biased.', 'Early arrivals may share habits or characteristics; not everyone has an equal chance of selection.', 'B1 [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t62.add('C4', (2, 3, 4, 5), 'multi_step')(_samp_c4)
t62.fixed('C1', (1, 2), [
    ('What is a random sample?', 'A sample in which every member of the population has an equal chance of being chosen', 'Definition. [1]', ['A sample of your friends', 'A sample chosen by the investigator', 'The whole population']),
    ('What usually happens to the results when the size of a random sample is increased?', 'They become more reliable', 'Larger samples reduce the effect of chance variation. [1]', ['They become less reliable', 'They become biased', 'They become exactly the same as the population']),
    ('Write down one way of selecting a random sample.', 'Random number generator / names drawn from a hat', 'B1 [1]'),
])
t62.fixed('C2', (2, 3), [
    ('Explain why a sample that is very large is not always better.', 'It costs more time and money to collect and process; beyond a certain size the extra reliability is small. A large biased sample is still biased.', 'B1 cost/time; B1 bias not removed by size. [2]'),
    ('Explain the difference between a population and a sample.', 'The population is the whole group being studied; a sample is the part of it from which data is actually collected.', 'B1 B1. [2]'),
])


# ----------------------------------------------------------- bias
t63 = topic('Recognising and reducing bias', 'bias', 'data collection', 'reducing bias')
BIASED = [
    ('asks people at a gym how often they exercise, to find out how much exercise people in {c} do', 'People at a gym exercise more than average, so the sample is not representative.', 'Ask a random sample of people from the whole city, e.g. using the electoral list or at several different places and times.'),
    ('asks members of a football club which sport is the most popular in the school', 'Football club members are likely to choose football.', 'Choose a random sample from the whole school register.'),
    ('puts an online survey on a technology website to find out how many people in {c} own a smartphone', 'People visiting a technology website are more likely to own a smartphone; people without internet access cannot answer.', 'Use a random sample of the whole population, including people without internet access.'),
    ('asks only the students in their own class about the school canteen', 'One class may not represent the whole school (one age group, same timetable).', 'Take a random sample from every year group.'),
    ('stands outside a bookshop to ask how many books people read each year', 'Bookshop customers probably read more than average.', 'Ask people at different locations and times, chosen at random.'),
    ('asks people at 10 a.m. on a weekday how they travel to work', 'Many workers are already at work at that time, so the sample misses them.', 'Ask at different times and days, or use a random sample from a list.'),
    ('surveys people leaving a vegetarian restaurant about their favourite meal', 'Vegetarians are over-represented; meat dishes are unlikely to be chosen.', 'Survey a random sample from the general population.'),
    ('asks the first 10 people who walk past about local transport', 'Only 10 people, and they are all in one place at one time.', 'Use a larger random sample at different times and places.'),
]
LEADING = [
    ('Do you agree that our school canteen serves unhealthy food?', 'It suggests the answer (leading question).', 'How would you rate the healthiness of the school canteen food? Very healthy / Healthy / Unhealthy / Very unhealthy'),
    ("Don't you think the new park is a waste of money?", 'It is a leading question that pushes the person to agree.', 'What is your opinion of the new park? Very good / Good / Poor / Very poor'),
    ('How much do you spend on lunch?', 'It is vague: no time period, no response boxes.', 'How much do you usually spend on lunch each day? $0–$2 / more than $2 up to $4 / more than $4 up to $6 / more than $6'),
    ('Most people prefer cats. Which pet do you prefer?', 'The first sentence influences the answer.', 'Which of these pets do you prefer? Cat / Dog / Fish / Other / None'),
    ('Do you exercise a lot?', '"A lot" means different things to different people.', 'How many hours do you exercise in a typical week? 0 / more than 0 up to 2 / more than 2 up to 4 / more than 4'),
    ('Scientists say sugar is bad. Do you eat too much sugar?', 'It is leading and embarrassing, so people may not answer honestly.', 'How many sugary drinks do you have in a typical day? 0 / 1 / 2 / 3 or more'),
]


@t63.add('C2', (1, 2, 3, 4), 'explain')
def t63_sample(r, D):
    what, why, fix = r.choice(BIASED)
    p = person(r)
    c = city(r)
    stem = r.choice([f'{p} {what.format(c=c)}. Explain why {p}\'s sample is likely to be biased.',
                     f'{p} {what.format(c=c)}. Give one reason why the results may be biased and suggest how {p} could improve the sample.'])
    return Q(stem, f'{why} Improvement: {fix}', 'B1 reason for bias; B1 sensible improvement. [2]')


@t63.add('C2', (1, 2, 3, 4), 'explain')
def t63_question(r, D):
    q, why, better = r.choice(LEADING)
    p = person(r)
    stem = r.choice([f'{p} writes this question for a survey: "{q}" Explain what is wrong with the question.', f'Here is a question from {p}\'s questionnaire: "{q}" Give one criticism of the question and write a better question.'])
    return Q(stem, f'{why} Better: "{better}"', 'B1 criticism; B1 improved, neutral question with suitable responses. [2]')


@t63.add('C1', (1, 2, 3))
def t63_mcq(r, D):
    q, why, better = r.choice(LEADING)
    return MCQ(r, f'A questionnaire includes: "{q}" What is the main problem with this question?', why.split('(')[0].strip().rstrip('.') + '.',
               ['It has too many response boxes.', 'It is too short.', 'It asks for numerical data.', 'There is nothing wrong with it.'], f'{why} [1]')


@t63.add('C1', (1, 2, 3))
def t63_which(r, D):
    what, why, fix = r.choice(BIASED)
    p = person(r)
    return MCQ(r, f'{p} {what.format(c=city(r))}. Why is the sample biased?', why, ['The sample is too large.', 'The question is open.', 'The data is continuous.', 'Secondary data was used.'],
               f'{why} [1]')


@t63.add('C3', (1, 2, 3, 4, 5))
def t63_boxes(r, D):
    lo = r.choice([0, 1, 2, 5])
    w = r.choice([1, 2, 5, 10])
    unit = r.choice(['hours of TV per week', 'dollars spent on snacks per week', 'minutes spent travelling to school', 'books read last year'])
    edges = [lo + i * w for i in range(4)]
    bad = ', '.join(f'{edges[i]}–{edges[i + 1]}' for i in range(3))
    good = f'less than {edges[0]}' if edges[0] > 0 else ''
    fixed = [f'{edges[0]} up to but not including {edges[1]}' if i == 0 else f'{edges[i]} up to but not including {edges[i + 1]}' for i in range(3)] + [f'{edges[3]} or more']
    p = person(r)
    return Q(f'{p} uses these response boxes for a question about {unit}: {bad}. Identify two problems with the boxes and write a better set of boxes.',
             f'The boxes overlap (e.g. {edges[1]} is in two boxes) and there is no box for values above {edges[3]}' + (f' or below {edges[0]}' if edges[0] > 0 else '') + f'. Better: {"; ".join(fixed)}' + (f'; less than {edges[0]}' if edges[0] > 0 else '') + '.',
             'B1 overlap; B1 gaps/not exhaustive; B1 non-overlapping exhaustive set.', marks=3)


@t63.add('C3', (2, 3, 4, 5))
def t63_rewrite(r, D):
    q, why, better = r.choice(LEADING)
    what, why2, fix = r.choice(BIASED)
    p = person(r)
    return Q(f'{p} {what.format(c=city(r))}, using the question "{q}" Describe two different sources of bias in {p}\'s survey and explain how to reduce each one.',
             f'Sample: {why2} → {fix} Question: {why} → use a neutral question such as "{better}"',
             'B1 sampling bias; B1 its fix; B1 question bias; B1 its fix. [4]', marks=4)


def _bias_c4(r, D):
    what, why, fix = r.choice(BIASED)
    q, qwhy, better = r.choice(LEADING)
    p = person(r)
    n = r.choice([10, 12, 15, 20])
    intro = f'{p} {what.format(c=city(r))}. {p} asks {n} people the question "{q}"'
    parts = [
        lambda r: ('Give two reasons why the results may be biased.', f'{why} Also the question: {qwhy}', 'B1 B1 [2]'),
        lambda r: ('Rewrite the question so that it is not biased.', better, 'B1 neutral wording; B1 suitable response options [2]'),
        lambda r: (f'Explain why a sample of {n} people is not enough.', 'Too small to be reliable or representative.', 'B1 [1]'),
        lambda r: ('Describe how to choose a better sample.', fix, 'B1 B1 [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t63.add('C4', (2, 3, 4, 5), 'multi_step')(_bias_c4)
t63.fixed('C1', (1, 2), [
    ('What is bias in data collection?', 'Something that makes the results unrepresentative or unfair in one direction', 'Bias distorts results systematically. [1]', ['Rounding the data', 'Using a large sample', 'Drawing a bar chart']),
    ('Which of these is a leading question? "How many hours do you sleep?", "You sleep too little, don\'t you?", "What time do you go to bed?", "Do you have a bedtime?"', 'You sleep too little, don\'t you?', 'It suggests the answer. [1]', ['How many hours do you sleep?', 'What time do you go to bed?', 'Do you have a bedtime?']),
    ('Write down one way to reduce bias when choosing a sample.', 'Choose the sample randomly (and make it large enough).', 'B1 [1]'),
])
t63.fixed('C2', (2, 3), [
    ('Explain why response boxes in a questionnaire should not overlap.', 'If they overlap, some answers fit two boxes, so a person could tick either and the results would be unclear.', 'B1 values in two boxes; B1 consequence. [2]'),
    ('Explain why a large sample can still be biased.', 'If it is chosen in a way that favours one group (e.g. only gym members), increasing its size does not fix this.', 'B1 selection method matters; B1 example. [2]'),
    ('Explain how a pilot survey can help to reduce bias.', 'Trying the questionnaire on a few people first shows which questions are unclear, leading or missing options, so they can be improved before the main survey.', 'B1 test on small group; B1 improve questions. [2]'),
])

CHAPTERS[6] = [t61, t62, t63]


# =========================================================== 7 Shapes and measurements
PI = math.pi
t71 = topic('Circumference and area of a circle', 'circumference and area of a circle', 'circles')


@t71.add('C3', (1, 2, 3, 4, 5))
def t71_calc(r, D):
    rad = r.choice([3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 2.5, 4.5, 6.5, 7.2, 11.4])
    give_d = r.random() < 0.5
    what = r.choice(['area', 'circumference'])
    obj = r.choice(['circle', 'circular table top', 'circular pond', 'coin', 'pizza', 'clock face'])
    unit = 'mm' if obj == 'coin' else ('m' if obj == 'circular pond' else 'cm')
    meas = f'diameter {N(2 * rad)} {unit}' if give_d else f'radius {N(rad)} {unit}'
    if D <= 2 and isinstance(rad, int):
        v = (f'{N(rad * rad)}π {unit}²' if what == 'area' else f'{N(2 * rad)}π {unit}')
        stem = f'A {obj} has {meas}. Work out its {what}, giving your answer in terms of π.'
        key = f'{"A = πr²" if what == "area" else "C = πd"}' + (f'; r = {N(rad)}' if give_d and what == 'area' else '') + f' (M1); {v} (A1).'
        if D == 1:
            alt = [f'{N(2 * rad)}π {unit}²', f'{N(4 * rad * rad)}π {unit}²', f'{N(rad)}π {unit}²', f'{N(rad * rad)}π {unit}'] if what == 'area' else [f'{N(rad)}π {unit}', f'{N(rad * rad)}π {unit}', f'{N(4 * rad)}π {unit}', f'{N(2 * rad)}π {unit}²']
            return MCQ(r, f'A {obj} has {meas}. What is its {what}, in terms of π?', v, alt, key)
        return Q(stem, v, key)
    val = PI * rad * rad if what == 'area' else 2 * PI * rad
    stem = f'A {obj} has {meas}. Calculate its {what}. Give your answer correct to {"1 decimal place" if D < 4 else "3 significant figures"}.'
    ans = (fdp(val, 1) if D < 4 else sf(val, 3)) + f' {unit}' + ('²' if what == 'area' else '')
    key = (f'r = {N(rad)} (B1 if from diameter); ' if give_d else '') + (f'π × {N(rad)}² (M1)' if what == 'area' else f'π × {N(2 * rad)} (M1)') + f' = {fdp(val, 3)}… → {ans} (A1).'
    return Q(stem, ans, key)


@t71.add('C3', (2, 3, 4, 5))
def t71_reverse(r, D):
    rad = r.choice([3, 4, 5, 6, 7, 8, 9, 10, 12, 2.5, 4.5, 6.4])
    if r.random() < 0.5:
        A = PI * rad * rad
        return Q(f'A circle has area {fdp(A, 1)} cm². Calculate its radius, correct to 1 decimal place.', f'{fdp(math.sqrt(r1(A, 1) / PI), 1)} cm',
                 f'πr² = {fdp(A, 1)} (M1); r² = {fdp(A, 1)} ÷ π = {fdp(r1(A, 1) / PI, 3)} (M1); r = {fdp(math.sqrt(r1(A, 1) / PI), 1)} cm (A1).', marks=3)
    C = 2 * PI * rad
    return Q(f'The circumference of a circular flower bed is {fdp(C, 1)} m. Calculate its diameter, correct to 1 decimal place.', f'{fdp(r1(C, 1) / PI, 1)} m',
             f'C = πd (M1); d = {fdp(C, 1)} ÷ π = {fdp(r1(C, 1) / PI, 1)} m (A1).')


@t71.add('C1', (1, 2, 3))
def t71_formula(r, D):
    rad = r.randint(2, 12)
    which = r.choice(['C', 'A'])
    if which == 'C':
        return MCQ(r, f'A circle has radius {rad} cm. Which expression gives its circumference?', f'2 × π × {rad}', [f'π × {rad}²', f'π × {rad}', f'2 × π × {rad}²', f'π × {2 * rad}²'], f'C = 2πr. [1]')
    return MCQ(r, f'A circle has diameter {2 * rad} cm. Which expression gives its area?', f'π × {rad}²', [f'π × {2 * rad}²', f'2 × π × {rad}', f'π × {2 * rad}', f'2 × π × {rad}²'], f'A = πr² with r = {rad}. [1]')


@t71.add('C2', (1, 2, 3, 4), 'explain')
def t71_err(r, D):
    d = r.choice([6, 8, 10, 12, 14, 20])
    p = person(r)
    kind = r.choice(['diam', 'double', 'sq'])
    if kind == 'diam':
        return Q(f'A circle has diameter {d} cm. {p} works out its area as π × {d}² = {fdp(PI * d * d, 1)} cm². Explain the mistake and find the correct area to 1 decimal place.',
                 f'{p} used the diameter instead of the radius. r = {d // 2} cm, so A = π × {d // 2}² = {fdp(PI * (d / 2) ** 2, 1)} cm².', 'B1 must use radius; B1 correct area. [2]')
    if kind == 'double':
        return Q(f'{p} says: "If you double the radius of a circle, its area doubles." Use a circle of radius {d // 2} cm to show that {p} is wrong.',
                 f'r = {d // 2}: A = {(d // 2) ** 2}π. r = {d}: A = {d * d}π, which is 4 times as big. The area depends on r², so doubling r multiplies the area by 4.', 'M1 both areas; A1 conclusion (× 4). [2]')
    return Q(f'{p} calculates the area of a circle of radius {d // 2} cm by working out (π × {d // 2})². Explain why this is wrong.',
             f'Only the radius is squared: A = π × {d // 2}² = {(d // 2) ** 2}π. (π × {d // 2})² squares π as well.', 'B1 only r squared; B1 correct expression. [2]')


@t71.add('C2', (2, 3, 4), 'explain')
def t71_pi(r, D):
    d = r.choice([7, 14, 21, 28, 35])
    p = person(r)
    return Q(f'{p} uses π ≈ 22/7 to work out the circumference of a circle of diameter {d} cm and gets {22 * d // 7} cm. A calculator gives {fdp(PI * d, 2)} cm. Explain why the answers are different and which is more accurate.',
             'π is irrational; 22/7 = 3.142857… is only an approximation, slightly larger than π = 3.14159…. The calculator value is more accurate.', 'B1 22/7 approximation; B1 calculator more accurate. [2]')


def _circ_c4(r, D):
    kind = r.choice(['wheel', 'path', 'track'])
    if kind == 'wheel':
        dia = r.choice([50, 60, 64, 66, 70, 72])
        dist = r.choice([1, 1.5, 2, 3, 5])
        C = PI * dia
        rev = dist * 100000 / C
        intro = f'The wheels of {person(r)}\'s bicycle have a diameter of {dia} cm.'
        parts = [lambda r: ('Calculate the circumference of a wheel, to 1 decimal place.', f'{fdp(C, 1)} cm', f'M1 π × {dia}; A1 {fdp(C, 1)} [2]'),
                 lambda r: (f'Calculate how many complete turns each wheel makes in a journey of {N(dist)} km.', str(int(rev)), f'M1 {N(dist)} km = {N(dist * 100000)} cm; M1 ÷ {fdp(C, 1)}; A1 {int(rev)} [3]'),
                 lambda r: ('Explain why the answer must be rounded down.', 'Only complete turns are counted; the last turn is not finished.', 'B1 [1]')]
    elif kind == 'path':
        rad = r.choice([3, 4, 5, 6, 8])
        w = r.choice([1, 1.5, 2])
        ring = PI * ((rad + w) ** 2 - rad ** 2)
        intro = f'A circular pond of radius {rad} m in a park in {city(r)} is surrounded by a path {N(w)} m wide.'
        parts = [lambda r: ('Calculate the area of the path, to 1 decimal place.', f'{fdp(ring, 1)} m²', f'M1 π × {N(rad + w)}²; M1 − π × {rad}²; A1 {fdp(ring, 1)} [3]'),
                 lambda r: ('Calculate the length of the outer edge of the path, to 1 decimal place.', f'{fdp(2 * PI * (rad + w), 1)} m', 'M1; A1 [2]'),
                 lambda r: (f'Paving costs $35 per m². Work out the cost of paving the path.', money(r1(ring, 1) * 35), 'M1; A1 [2]')]
    else:
        L, dia = r.choice([(80, 60), (100, 64), (84.4, 73)])
        per = 2 * L + PI * dia
        intro = f'A running track has two straight sides of length {N(L)} m joined by two semicircles of diameter {N(dia)} m.'
        parts = [lambda r: ('Calculate the total length of the track, to the nearest metre.', f'{round(per)} m', f'M1 π × {N(dia)}; M1 + 2 × {N(L)}; A1 {round(per)} [3]'),
                 lambda r: ('Calculate the area enclosed by the track, to the nearest m².', f'{round(L * dia + PI * (dia / 2) ** 2)} m²', 'M1 rectangle + circle; A1 [2]'),
                 lambda r: (f'How many complete laps are needed to run at least 5 km?', str(math.ceil(5000 / per)), 'M1 5000 ÷ length; A1 round up [2]')]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t71.add('C4', (2, 3, 4, 5), 'multi_step')(_circ_c4)
t71.fixed('C1', (1, 2), [
    ('What is the name of the distance around a circle?', 'Circumference', 'B1 [1]', ['Diameter', 'Radius', 'Area']),
    ('The diameter of a circle is 18 cm. What is its radius?', '9 cm', 'Radius = diameter ÷ 2. [1]', ['36 cm', '18π cm', '81 cm']),
    ('Write down the formula for the area of a circle with radius r.', 'A = πr²', 'B1 [1]'),
])
t71.fixed('C2', (2, 3), [
    ('Explain why π is the same for every circle.', 'All circles are similar (enlargements of each other), so circumference ÷ diameter is always the same number, π.', 'B1 similar/enlargements; B1 ratio C/d constant. [2]'),
    ('Explain why an answer in terms of π, such as 25π cm², is more accurate than 78.5 cm².', 'π is irrational, so any decimal value is rounded; 25π is exact.', 'B1 exact; B1 decimal is rounded. [2]'),
])


# ----------------------------------------------------------- compound shapes, semicircles, sectors
t72 = topic('Areas of compound shapes, semicircles and sectors', 'areas of compound shapes', 'semicircles and sectors', 'sectors')


@t72.add('C3', (1, 2, 3, 4, 5))
def t72_semi(r, D):
    d = r.choice([6, 8, 10, 12, 14, 16, 20, 9, 15])
    what = r.choice(['area', 'perimeter'])
    rad = d / 2
    if what == 'area':
        v = PI * rad * rad / 2
        return Q(f'A semicircle has diameter {d} cm. Calculate its area, correct to 1 decimal place.', f'{fdp(v, 1)} cm²', f'½ × π × {N(rad)}² (M1) = {fdp(v, 1)} cm² (A1).')
    v = PI * d / 2 + d
    return Q(f'A semicircle has diameter {d} cm. Calculate its perimeter, correct to 1 decimal place.', f'{fdp(v, 1)} cm',
             f'Curved part ½ × π × {d} = {fdp(PI * d / 2, 2)} (M1); + diameter {d} (M1); {fdp(v, 1)} cm (A1).', marks=3)


@t72.add('C3', (2, 3, 4, 5))
def t72_sector(r, D):
    ang = r.choice([30, 40, 45, 60, 72, 90, 120, 135, 150, 210, 240, 270])
    rad = r.choice([4, 5, 6, 8, 9, 10, 12])
    f = Fr(ang, 360)
    if r.random() < 0.5 or D <= 2:
        v = float(f) * PI * rad * rad
        return Q(f'A sector of a circle has radius {rad} cm and angle {ang}°. Calculate the area of the sector, to 1 decimal place.', f'{fdp(v, 1)} cm²',
                 f'{ang}/360 = {fr(f)} of the circle (M1); {fr(f)} × π × {rad}² (M1) = {fdp(v, 1)} cm² (A1).', marks=3)
    arc = float(f) * 2 * PI * rad
    return Q(f'A sector has radius {rad} cm and angle {ang}°. Calculate (a) the arc length and (b) the perimeter of the sector, each to 1 decimal place.',
             f'(a) {fdp(arc, 1)} cm (b) {fdp(arc + 2 * rad, 1)} cm', f'(a) M1 {fr(f)} × 2π × {rad}; A1 [2] (b) M1 arc + 2 × {rad}; A1 [2]', marks=4)


@t72.add('C3', (2, 3, 4, 5))
def t72_compound(r, D):
    kind = r.choice(['rect_semi', 'sq_quarter', 'rect_minus_semi', 'two_semis'])
    a = r.choice([6, 8, 10, 12, 14])
    b = r.choice([5, 7, 9, 11, 15])
    if kind == 'rect_semi':
        v = a * b + PI * (a / 2) ** 2 / 2
        return Q(f'A window is a rectangle {a} cm wide and {b} cm tall with a semicircle on top. The diameter of the semicircle is the width of the rectangle. Calculate the total area of the window, to 1 decimal place.',
                 f'{fdp(v, 1)} cm²', f'Rectangle {a * b} (B1); semicircle ½ × π × {N(a / 2)}² = {fdp(PI * (a / 2) ** 2 / 2, 2)} (M1); total {fdp(v, 1)} (A1).', marks=3)
    if kind == 'sq_quarter':
        v = a * a - PI * a * a / 4
        return Q(f'A quarter circle of radius {a} cm is cut from a square of side {a} cm, with the centre of the circle at one corner. Calculate the area that is left, to 1 decimal place.',
                 f'{fdp(v, 1)} cm²', f'Square {a * a} (B1); quarter circle ¼ × π × {a}² = {fdp(PI * a * a / 4, 2)} (M1); {fdp(v, 1)} (A1).', marks=3)
    if kind == 'rect_minus_semi':
        if a >= 2 * b:
            return None
        v = a * b - PI * (a / 2) ** 2 / 2
        return Q(f'A semicircle of diameter {a} cm is cut out of one side of a rectangle {a} cm by {b} cm (the diameter lies along the {a} cm side). Calculate the remaining area, to 1 decimal place.',
                 f'{fdp(v, 1)} cm²', f'{a * b} − ½π × {N(a / 2)}² (M1, M1) = {fdp(v, 1)} (A1).', marks=3)
    v = PI * (a / 2) ** 2
    return Q(f'A shape is made from a square of side {a} cm with a semicircle on two opposite sides, each with diameter {a} cm. Calculate (a) the area and (b) the perimeter of the shape, to 1 decimal place.',
             f'(a) {fdp(a * a + v, 1)} cm² (b) {fdp(PI * a + 2 * a, 1)} cm', f'(a) M1 two semicircles = one circle radius {N(a / 2)}; A1 {fdp(a * a + v, 1)} [2] (b) M1 π × {a} + 2 × {a}; A1 {fdp(PI * a + 2 * a, 1)} [2]', marks=4)


@t72.add('C1', (1, 2, 3))
def t72_frac(r, D):
    ang = r.choice([30, 36, 40, 45, 60, 72, 90, 120, 135, 150, 240, 270, 300])
    f = Fr(ang, 360)
    return MCQ(r, f'What fraction of a full circle is a sector with angle {ang}°?', fr(f), [fr(Fr(ang, 180)), fr(Fr(ang, 100)) if ang < 100 else fr(Fr(360 - ang, 360)), fr(Fr(1, ang // 10)) if ang // 10 > 1 else '1/2', fr(Fr(ang, 90)) if ang < 90 else fr(Fr(90, ang))],
               f'{ang}/360 = {fr(f)}. [1]')


@t72.add('C2', (1, 2, 3, 4), 'explain')
def t72_err(r, D):
    d = r.choice([8, 10, 12, 14, 20])
    p = person(r)
    if r.random() < 0.5:
        return Q(f'{p} works out the perimeter of a semicircle with diameter {d} cm as ½ × π × {d} = {fdp(PI * d / 2, 1)} cm. Explain what {p} has forgotten and give the correct perimeter.',
                 f'{p} has only found the curved part; the straight diameter ({d} cm) must be added: {fdp(PI * d / 2 + d, 1)} cm.', 'B1 diameter missing; B1 correct value. [2]')
    ang, rad = r.choice([(60, 6), (90, 8), (120, 9), (45, 4)])
    return Q(f'{p} says the area of a sector with angle {ang}° and radius {rad} cm is {ang} × π × {rad}². Explain the mistake.',
             f'The angle must be written as a fraction of 360°: area = {ang}/360 × π × {rad}² = {fdp(ang / 360 * PI * rad * rad, 1)} cm².', 'B1 fraction of 360; B1 correct calculation. [2]')


@t72.add('C2', (2, 3, 4), 'explain')
def t72_split(r, D):
    a, b = r.choice([(10, 6), (12, 8), (14, 6), (16, 10)])
    c = r.choice([3, 4, 5])
    p = person(r)
    return Q(f'An L-shape is made by removing a {c} cm by {c} cm square from one corner of a {a} cm by {b} cm rectangle. Explain two different ways to work out its area, and show they give the same answer.',
             f'(1) Big rectangle minus square: {a * b} − {c * c} = {a * b - c * c} cm². (2) Split into two rectangles: {a - c} × {b} + {c} × {b - c} = {(a - c) * b + c * (b - c)} cm².',
             'B1 subtraction method; B1 splitting method, same answer. [2]')


def _comp_c4(r, D):
    a = r.choice([10, 12, 14, 16, 20])
    b = r.choice([6, 8, 10])
    intro = f'A garden in {city(r)} is a rectangle {a} m by {b} m with a semicircular flower bed on one of the {b} m sides, outside the rectangle.'
    semi = PI * (b / 2) ** 2 / 2
    parts = [
        lambda r: ('Calculate the total area of the garden, to 1 decimal place.', f'{fdp(a * b + semi, 1)} m²', f'M1 semicircle ½π × {N(b / 2)}²; A1 {fdp(a * b + semi, 1)} [2]'),
        lambda r: ('Calculate the length of fence needed to go around the whole garden, to 1 decimal place.', f'{fdp(2 * a + b + PI * b / 2, 1)} m', f'M1 curved part ½π × {b}; M1 + {a} + {a} + {b}; A1 [3]'),
        lambda r: (f'Grass seed covers 25 m² per box. How many boxes are needed for the rectangular part only?', str(math.ceil(a * b / 25)), f'M1 {a * b} ÷ 25; A1 round up [2]'),
        lambda r: ('What percentage of the garden is flower bed? Give your answer to 1 decimal place.', f'{fdp(100 * semi / (a * b + semi), 1)}%', 'M1; A1 [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t72.add('C4', (2, 3, 4, 5), 'multi_step')(_comp_c4)


@t72.add('C4', (3, 4, 5), 'multi_step')
def t72_logo(r, D):
    R = r.choice([6, 8, 10, 12])
    ang = r.choice([60, 90, 120])
    return Q(f'A logo is a circle of radius {R} cm. A sector with angle {ang}° is shaded blue and the rest is white. (a) Calculate the area of the blue sector. (b) Calculate the white area. (c) Calculate the perimeter of the blue sector. Give answers to 1 decimal place.',
             f'(a) {fdp(ang / 360 * PI * R * R, 1)} cm² (b) {fdp((360 - ang) / 360 * PI * R * R, 1)} cm² (c) {fdp(ang / 360 * 2 * PI * R + 2 * R, 1)} cm',
             f'(a) M1 {fr(Fr(ang, 360))} × π × {R}²; A1 [2] (b) B1 [1] (c) M1 arc {fr(Fr(ang, 360))} × 2π × {R}; M1 + 2 × {R}; A1 [3]', marks=6)


t72.fixed('C1', (1, 2), [
    ('Which formula gives the area of a semicircle of radius r?', '½πr²', 'Half of πr². [1]', ['πr²', '2πr', '½πr']),
    ('Which formula gives the arc length of a sector with angle θ° and radius r?', 'θ/360 × 2πr', 'Fraction of the circumference. [1]', ['θ/360 × πr²', 'θ × 2πr', '360/θ × 2πr']),
    ('Write down the area of a quarter circle of radius 2 cm, in terms of π.', 'π cm²', '¼ × π × 4. B1 [1]'),
])
t72.fixed('C2', (2, 3), [
    ('Explain why the area of a sector with angle 90° is one quarter of the area of the circle.', '90° is 90/360 = 1/4 of the full turn at the centre, so the sector is a quarter of the circle.', 'B1 90/360; B1 = 1/4. [2]'),
])


# ----------------------------------------------------------- converting units of area and volume
t73 = topic('Converting units of area and volume', 'converting between large and small units of area and volume', 'units of area and volume')
CONV = [
    ('m²', 'cm²', 10000), ('cm²', 'mm²', 100), ('km²', 'm²', 1000000), ('m³', 'cm³', 1000000), ('cm³', 'mm³', 1000),
    ('litres', 'cm³', 1000), ('m³', 'litres', 1000), ('hectares', 'm²', 10000), ('litres', 'ml', 1000),
]
LINF = {('m²', 'cm²'): 100, ('cm²', 'mm²'): 10, ('km²', 'm²'): 1000, ('m³', 'cm³'): 100, ('cm³', 'mm³'): 10}


@t73.add('C1', (1, 2, 3))
def t73_mcq(r, D):
    big, small, f = r.choice(CONV)
    lin_f = LINF.get((big, small), 10)
    wrong = [N(f // 100) if f >= 1000 else '10', N(f * 10), N(lin_f)]
    return MCQ(r, f'How many {small} are there in 1 {big[:-1] if big.endswith("s") else big}?', N(f), wrong + [N(f // 10)], f'1 {big} = {N(f)} {small}. [1]')


@t73.add('C3', (1, 2, 3, 4, 5))
def t73_calc(r, D):
    big, small, f = r.choice(CONV)
    x = r.choice([2.5, 3.6, 0.45, 1.2, 7, 0.08, 12.5, 0.6, 4.25])
    if r.random() < 0.5:
        ans = dshift(x, int(round(math.log10(f))))
        return Q(f'Convert {N(x)} {big} to {small}.', f'{ans} {small}', f'1 {big} = {N(f)} {small} (M1); {N(x)} × {N(f)} = {ans} (A1).')
    y = dshift(x, int(round(math.log10(f))))
    return Q(f'Convert {y} {small} to {big}.', f'{N(x)} {big}', f'1 {big} = {N(f)} {small} (M1); {y} ÷ {N(f)} = {N(x)} (A1).')


@t73.add('C3', (2, 3, 4, 5))
def t73_box(r, D):
    l, w, h = r.choice([(40, 30, 25), (50, 20, 20), (60, 40, 30), (80, 50, 40), (25, 20, 12)])
    V = l * w * h
    return Q(f'A fish tank is a cuboid measuring {l} cm by {w} cm by {h} cm. Work out how many litres of water it holds when full.', f'{N(V / 1000)} litres',
             f'V = {l} × {w} × {h} = {V:,} cm³ (M1); 1 litre = 1000 cm³ (M1); {N(V / 1000)} litres (A1).', marks=3)


@t73.add('C2', (1, 2, 3, 4), 'explain')
def t73_err(r, D):
    big, small, f = r.choice(CONV[:5])
    lin_f = LINF[(big, small)]
    x = r.choice([3, 4.5, 6, 2.4, 8])
    p = person(r)
    return Q(f'{p} says that {N(x)} {big} = {N(x * lin_f)} {small} because there are {lin_f} {small[:-1]} in 1 {big[:-1]}. Explain the mistake and give the correct answer.',
             f'Area/volume units must be squared/cubed: 1 {big} = {lin_f}{"²" if "²" in big else "³"} = {N(f)} {small}, so {N(x)} {big} = {N(x * f)} {small}.',
             'B1 explains squaring/cubing the length factor; B1 correct answer. [2]')


@t73.add('C2', (2, 3, 4), 'explain')
def t73_why(r, D):
    big, small, f = r.choice(CONV[:5])
    lin_f = LINF[(big, small)]
    kind = 'square' if '²' in big else 'cube'
    return Q(f'Explain why 1 {big} = {N(f)} {small}. You may use a sketch of a {kind}.',
             f'A {kind} of side 1 {big[:-1]} has side {lin_f} {small[:-1]}, so its {"area" if kind == "square" else "volume"} is {lin_f}{"²" if kind == "square" else "³"} = {N(f)} {small}.',
             f'B1 1 {big[:-1]} = {lin_f} {small[:-1]}; B1 {"squared" if kind == "square" else "cubed"} gives {N(f)}. [2]')


def _units_c4(r, D):
    l, w = r.choice([(120, 80), (250, 150), (400, 300), (60, 45)])
    d = r.choice([1.2, 1.5, 2, 2.5])
    intro = f'A rectangular swimming pool in {city(r)} is {l // 10} m long and {w // 10} m wide. The water is {N(d)} m deep everywhere.'
    A = (l // 10) * (w // 10)
    V = A * d
    parts = [
        lambda r: ('Work out the area of the surface of the water in cm².', f'{N(A * 10000)} cm²', f'M1 {A} m² × 10 000; A1 [2]'),
        lambda r: ('Work out the volume of water in m³.', f'{N(V)} m³', f'B1 {A} × {N(d)} [1]'),
        lambda r: ('Work out the volume of water in litres.', f'{N(V * 1000)} litres', 'M1 × 1000; A1 [2]'),
        lambda r: (f'Water is pumped in at 500 litres per minute. How many hours does it take to fill the pool? Give your answer to 1 decimal place.', f'{fdp(V * 1000 / 500 / 60, 1)} hours', 'M1 ÷ 500; M1 ÷ 60; A1 [3]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t73.add('C4', (2, 3, 4, 5), 'multi_step')(_units_c4)


@t73.add('C4', (3, 4, 5), 'multi_step')
def t73_paint(r, D):
    l, h = r.choice([(4, 2.5), (5, 2.4), (6, 3), (3.5, 2.5)])
    cov = r.choice([8, 10, 12])
    tin = r.choice([1, 2.5])
    area = 2 * l * h + 2 * (l - 1) * h
    litres = area / cov
    tins = math.ceil(litres / tin)
    return Q(f'A room has four walls. Two walls are {N(l)} m by {N(h)} m and two are {N(l - 1)} m by {N(h)} m. One litre of paint covers {cov} m². Paint is sold in {N(tin)} litre tins. (a) Work out the total area of the walls. (b) Write this area in cm². (c) How many tins of paint are needed for one coat?',
             f'(a) {N(area)} m² (b) {N(area * 10000)} cm² (c) {tins}', f'(a) M1 sum of four walls; A1 {N(area)} [2] (b) B1 × 10 000 [1] (c) M1 {N(area)} ÷ {cov} = {N(round(litres, 2))} litres; A1 {tins} tin{"s" if tins > 1 else ""} (round up) [2]', marks=5)


t73.fixed('C1', (1, 2), [
    ('How many cm³ are there in 1 litre?', '1000', '1 litre = 1000 cm³ = 1000 ml. [1]', ['100', '10', '10 000']),
    ('Which is the largest area: 1 m², 1000 cm², 100 000 mm², 0.5 m²?', '1 m²', '1 m² = 10 000 cm² = 1 000 000 mm². [1]', ['1000 cm²', '100 000 mm²', '0.5 m²']),
    ('Write down the number of m² in 1 hectare.', '10 000', 'B1 [1]'),
])
t73.fixed('C2', (2, 3), [
    ('Explain why 1 cm³ of water is the same as 1 ml.', '1 litre = 1000 cm³ and 1 litre = 1000 ml, so 1 cm³ = 1 ml.', 'B1 both facts; B1 conclusion. [2]'),
])

CHAPTERS[7] = [t71, t72, t73]


# =========================================================== 8 Fractions
t81 = topic('Fractions and recurring decimals', 'fractions and recurring decimals', 'recurring decimals')


def recur(f, maxlen=12):
    """Decimal expansion of a fraction, recurring part shown with '…' after two repeats."""
    f = Fr(f)
    n, d = f.numerator, f.denominator
    ip = n // d
    rem = n % d
    seen = {}
    digs = ''
    while rem and rem not in seen:
        seen[rem] = len(digs)
        rem *= 10
        digs += str(rem // d)
        rem %= d
    if not rem:
        return f'{ip}.{digs}' if digs else str(ip), False
    st = seen[rem]
    pre, rep = digs[:st], digs[st:]
    s = f'{ip}.{pre}{rep * (2 if len(rep) < 4 else 1)}'
    if len(rep) == 1:
        s += rep
    return s + '…', True


def terminates(d):
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    return d == 1


@t81.add('C1', (1, 2, 3))
def t81_term(r, D):
    dens_t = [8, 16, 20, 25, 40, 50, 80, 125]
    dens_r = [3, 6, 7, 9, 11, 12, 15, 30, 45]
    dt = r.choice(dens_t)
    nt = r.choice([n for n in range(1, dt) if math.gcd(n, dt) == 1])
    ans = f'{nt}/{dt}'
    ds = []
    for d in r.sample(dens_r, 3):
        n = r.choice([n for n in range(1, d) if math.gcd(n, d) == 1])
        ds.append(f'{n}/{d}')
    if r.random() < 0.5:
        opts, a = mc(r, ans, ds)
        return Q(f'Which of these fractions can be written as a terminating decimal? {", ".join(opts)}', a, f'{dt} has only 2 and 5 as prime factors, so {ans} = {recur(Fr(nt, dt))[0]}. [1]', opts)
    d = r.choice(dens_r)
    n = r.choice([n for n in range(1, d) if math.gcd(n, d) == 1])
    s, _ = recur(Fr(n, d))
    return MCQ(r, f'Write {n}/{d} as a decimal.', s, [f'0.{n}{d}', f'{d}.{n}', recur(Fr(n, d + 1))[0], recur(Fr(n + 1, d))[0], s.replace('…', '')[:4]],
               f'{n} ÷ {d} = {s} (recurring). [1]')


@t81.add('C3', (1, 2, 3, 4, 5))
def t81_to_frac(r, D):
    kind = r.choice(['one', 'two'] if D <= 3 else ['two', 'mixed', 'three'])
    if kind == 'one':
        a = r.randint(1, 8)
        f = Fr(a, 9)
        dec = f'0.{str(a) * 4}…'
        key = f'x = {dec}; 10x = {a}.{str(a) * 3}… (M1); 9x = {a} (M1); x = {fr(f)} (A1).'
    elif kind == 'two':
        ab = r.choice([12, 15, 18, 27, 36, 45, 54, 63, 72, 81, 23, 47, 13, 31])
        f = Fr(ab, 99)
        dec = f'0.{str(ab).zfill(2) * 3}…'
        key = f'x = {dec}; 100x = {ab}.{str(ab).zfill(2) * 2}… (M1); 99x = {ab} (M1); x = {fr(f)} (A1).'
    elif kind == 'mixed':
        a, b = r.randint(1, 9), r.randint(1, 9)
        if a == b:
            b = (b % 9) + 1
        f = Fr(10 * a + b - a, 90)
        dec = f'0.{a}{str(b) * 4}…'
        key = f'x = {dec}; 10x = {a}.{str(b) * 3}…, 100x = {a}{b}.{str(b) * 2}… (M1); 90x = {10 * a + b - a} (M1); x = {fr(f)} (A1).'
    else:
        abc = r.choice([123, 108, 135, 270, 405, 571, 142])
        f = Fr(abc, 999)
        dec = f'0.{str(abc).zfill(3) * 2}…'
        key = f'1000x − x = {abc} (M1, M1); x = {abc}/999 = {fr(f)} (A1).'
    return Q(r.choice([f'Write the recurring decimal {dec} as a fraction in its simplest form.', f'Show that {dec} = {fr(f)}.' if D >= 3 else f'Convert {dec} to a fraction.']), fr(f), key, marks=3)


@t81.add('C3', (1, 2, 3, 4))
def t81_divide(r, D):
    d = r.choice([3, 6, 7, 9, 11, 12, 13, 15, 22, 27])
    n = r.choice([k for k in range(1, d) if math.gcd(k, d) == 1])
    s, _ = recur(Fr(n, d))
    return Q(f'Use division to write {n}/{d} as a recurring decimal.', s, f'{n}.000… ÷ {d} by short division (M1); {s} with the repeating block identified (A1).')


@t81.add('C2', (1, 2, 3, 4), 'explain')
def t81_why(r, D):
    a = r.choice([3, 7, 11, 13])
    dt = r.choice([20, 40, 25, 50, 8, 16])
    dr = dt * a // math.gcd(dt, a)
    n = 1
    while math.gcd(n, dr) != 1 or math.gcd(n, dt) != 1:
        n += 1
    return Q(f'Without dividing, explain why {n}/{dt} is a terminating decimal but {n}/{dr} is a recurring decimal.',
             f'{dt} has only 2 and 5 as prime factors, so it divides a power of 10. {dr} = {dt} × {a} has the prime factor {a}, which does not divide any power of 10, so the decimal recurs.',
             'B1 prime factors 2 and 5 only terminate; B1 other prime factor gives recurring. [2]')


@t81.add('C2', (2, 3, 4), 'explain')
def t81_err(r, D):
    a = r.randint(1, 8)
    p = person(r)
    if r.random() < 0.5:
        return Q(f'{p} says that 0.{str(a) * 4}… = {a}/10. Explain the mistake and give the correct fraction.',
                 f'{a}/10 = 0.{a} exactly, which terminates. The recurring decimal is bigger: x = 0.{a}{a}{a}…, 10x − x = {a}, so x = {fr(Fr(a, 9))}.', 'B1 explains error; B1 correct fraction. [2]')
    return Q(f'{p} says that 0.999… is less than 1. Use algebra to show that 0.999… = 1.', 'Let x = 0.999…; 10x = 9.999…; 10x − x = 9, so 9x = 9 and x = 1.', 'M1 10x − x; A1 x = 1. [2]')


def _rec_c4(r, D):
    a, b = r.choice([(1, 3), (2, 9), (4, 11), (5, 6), (7, 12), (3, 7)])
    ab = r.choice([27, 36, 45, 18, 81])
    s, _ = recur(Fr(a, b))
    intro = f'This question is about the fraction {a}/{b} and the recurring decimal 0.{str(ab) * 3}….'
    parts = [
        lambda r: (f'Write {a}/{b} as a decimal.', s, 'B1 [1]'),
        lambda r: (f'Write 0.{str(ab) * 3}… as a fraction in its simplest form.', fr(Fr(ab, 99)), 'M1 100x − x; A1 [2]'),
        lambda r: (f'Which is larger, {a}/{b} or 0.{str(ab) * 3}…? Show how you decide.', f'{a}/{b} = {s} and 0.{str(ab) * 3}… = {fr(Fr(ab, 99))}; the larger is {"the fraction " + str(a) + "/" + str(b) if Fr(a, b) > Fr(ab, 99) else "0." + str(ab) * 3 + "…"}', 'M1 compare in same form; A1 [2]'),
        lambda r: (f'Work out {a}/{b} + 0.{str(ab) * 3}… as a fraction.', fr(Fr(a, b) + Fr(ab, 99)), 'M1 common denominator; A1 [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t81.add('C4', (2, 3, 4, 5), 'multi_step')(_rec_c4)
t81.fixed('C1', (1, 2), [
    ('Which fraction is equal to 0.333…?', '1/3', '1 ÷ 3 = 0.333…. [1]', ['3/10', '33/100', '3/9 + 1/10']),
    ('What is 1/11 as a decimal?', '0.090909…', '1 ÷ 11 = 0.0909…. [1]', ['0.11', '0.111…', '0.0111…']),
    ('Write 5/8 as a decimal.', '0.625', 'B1 [1]'),
    ('Write 2/9 as a recurring decimal.', '0.222…', 'B1 [1]'),
])
t81.fixed('C2', (2, 3), [
    ('Explain why the decimal for any fraction must either terminate or recur.', 'When dividing by d, the remainder can only be 0, 1, …, d − 1; if it is never 0, a remainder must repeat, and then the digits repeat.', 'B1 finite number of remainders; B1 repeat → recurring. [2]'),
])


# ----------------------------------------------------------- order of operations with fractions
t82 = topic('Fractions and the order of operations', 'fractions and the correct order of operations', 'order of operations')
FRS = [Fr(1, 2), Fr(1, 3), Fr(2, 3), Fr(1, 4), Fr(3, 4), Fr(2, 5), Fr(3, 5), Fr(1, 6), Fr(5, 6), Fr(3, 8), Fr(5, 8), Fr(4, 9), Fr(7, 10), Fr(5, 12)]


def _ops(r, D):
    a, b, c = r.sample(FRS, 3)
    forms = [
        (f'{fr(a)} + {fr(b)} × {fr(c)}', a + b * c, f'{fr(b)} × {fr(c)} = {fr(b * c)} first', (a + b) * c),
        (f'{fr(a)} − {fr(b)} ÷ {fr(c)}', a - b / c, f'{fr(b)} ÷ {fr(c)} = {fr(b / c)} first', (a - b) / c),
        (f'({fr(a)} + {fr(b)}) × {fr(c)}', (a + b) * c, f'bracket first: {fr(a + b)}', a + b * c),
        (f'{fr(a)} × {fr(b)} + {fr(c)}', a * b + c, f'{fr(a)} × {fr(b)} = {fr(a * b)} first', a * (b + c)),
        (f'({fr(a)})² + {fr(b)}', a * a + b, f'({fr(a)})² = {fr(a * a)} first', 2 * a + b),
        (f'{fr(a)} ÷ ({fr(b)} + {fr(c)})', a / (b + c), f'bracket first: {fr(b + c)}', a / b + c),
    ]
    if D >= 4:
        forms.append((f'({fr(a)} − {fr(b)})² ÷ {fr(c)}', (a - b) ** 2 / c, f'bracket {fr(a - b)}, square {fr((a - b) ** 2)}', (a - b) ** 2 * c))
    return r.choice(forms)


@t82.add('C3', (1, 2, 3, 4, 5))
def t82_eval(r, D):
    e, v, step, wrong = _ops(r, D)
    if D == 1:
        return MCQ(r, f'Work out {e}.', mixed(v), [mixed(wrong), mixed(v + 1), mixed(v * 2) if v * 2 != wrong else mixed(v / 2), fr(Fr(v.numerator + 1, v.denominator))], f'{step}; answer {mixed(v)}. [1]')
    return Q(r.choice([f'Work out {e}. Give your answer as a fraction in its simplest form.', f'Without a calculator, work out {e}.']), mixed(v),
             f'{step} (M1); then the remaining operation with a common denominator (M1); {mixed(v)} (A1).', marks=3 if D >= 3 else 2)


@t82.add('C2', (1, 2, 3, 4), 'explain')
def t82_err(r, D):
    a, b, c = r.sample(FRS[:10], 3)
    p = person(r)
    w = (a + b) * c
    v = a + b * c
    return Q(f'{p} works out {fr(a)} + {fr(b)} × {fr(c)} and gets {mixed(w)}. Explain {p}\'s mistake and find the correct answer.',
             f'{p} added first. Multiplication comes before addition: {fr(b)} × {fr(c)} = {fr(b * c)}, then {fr(a)} + {fr(b * c)} = {mixed(v)}.', 'B1 order of operations; B1 correct answer. [2]')


@t82.add('C1', (1, 2, 3))
def t82_first(r, D):
    a, b, c = r.sample(FRS, 3)
    forms = [(f'{fr(a)} + {fr(b)} × {fr(c)}', 'Multiplication'), (f'({fr(a)} + {fr(b)}) ÷ {fr(c)}', 'Addition (in the bracket)'),
             (f'{fr(a)} − {fr(b)} ÷ {fr(c)}', 'Division'), (f'{fr(a)} × ({fr(b)})²', 'Squaring')]
    e, ans = r.choice(forms)
    return MCQ(r, f'Which operation should be done first in {e}?', ans, [x for _, x in forms if x != ans] + ['Subtraction'], f'Brackets, then indices, then × and ÷, then + and −. [1]')


@t82.add('C2', (2, 3, 4), 'explain')
def t82_brackets(r, D):
    a, b, c = r.sample(FRS[:10], 3)
    v1, v2 = a - b * c, (a - b) * c
    if v1 == v2:
        return None
    return Q(f'Explain why {fr(a)} − {fr(b)} × {fr(c)} and ({fr(a)} − {fr(b)}) × {fr(c)} give different answers. Work out both.',
             f'Without brackets you multiply first: {mixed(v1)}. With brackets you subtract first: {mixed(v2)}.', 'B1 explanation; B1 both values. [2]')


def _ops_c4(r, D):
    p = person(r)
    L = r.choice([Fr(3, 4), Fr(2, 3), Fr(5, 6), Fr(7, 8)])
    used = r.choice([Fr(1, 3), Fr(1, 4), Fr(2, 5)])
    k = r.choice([2, 3, 4])
    intro = f'{p} has {fr(L)} of a litre of juice. {p} drinks {fr(used)} of it and then shares the rest equally between {k} friends.'
    rest = L * (1 - used)
    parts = [
        lambda r: ('Write a single calculation, using brackets, for the amount each friend gets.', f'{fr(L)} × (1 − {fr(used)}) ÷ {k}', 'B1 [1]'),
        lambda r: ('Work out how much each friend gets, as a fraction of a litre.', f'{fr(rest / k)} litre', f'M1 {fr(L)} × {fr(1 - used)} = {fr(rest)}; A1 ÷ {k} [2]'),
        lambda r: ('Convert your answer to millilitres, to the nearest ml.', f'{round(float(rest / k) * 1000)} ml', 'B1 [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t82.add('C4', (2, 3, 4, 5), 'multi_step')(_ops_c4)


@t82.add('C4', (3, 4, 5), 'multi_step')
def t82_target(r, D):
    a, b, c = r.sample(FRS[:10], 3)
    vals = {'+': lambda x, y: x + y, '−': lambda x, y: x - y, '×': lambda x, y: x * y, '÷': lambda x, y: x / y}
    o1, o2 = r.sample(list(vals), 2)
    pri = {'+': 0, '−': 0, '×': 1, '÷': 1}
    if pri[o2] > pri[o1]:
        v = vals[o1](a, vals[o2](b, c))
    else:
        v = vals[o2](vals[o1](a, b), c)
    br = vals[o1](a, vals[o2](b, c)) if pri[o2] <= pri[o1] else vals[o2](vals[o1](a, b), c)
    if br == v:
        return None
    return Q(f'(a) Work out {fr(a)} {o1} {fr(b)} {o2} {fr(c)}. (b) Show where to put brackets in the same calculation to change the answer, and work out the new value.',
             f'(a) {mixed(v)} (b) ' + (f'{fr(a)} {o1} ({fr(b)} {o2} {fr(c)}) = {mixed(br)}' if pri[o2] <= pri[o1] else f'({fr(a)} {o1} {fr(b)}) {o2} {fr(c)} = {mixed(br)}'),
             '(a) M1 correct order; A1 [2] (b) B1 bracket placement; M1 working; A1 value [3]', marks=5)


t82.fixed('C1', (1, 2), [
    ('Work out 1/2 + 1/2 × 1/2.', '3/4', '1/2 × 1/2 = 1/4 first, then 1/2 + 1/4. [1]', ['1/2', '1/8', '1']),
    ('Work out (1/3)² × 9.', '1', '1/9 × 9. [1]', ['3', '1/3', '9']),
    ('Work out 2 − 1/4 × 4.', '1', '1/4 × 4 = 1, 2 − 1 = 1. B1 [1]'),
])
t82.fixed('C2', (2, 3), [
    ('Explain why 3/4 ÷ 1/2 + 1/4 is not the same as 3/4 ÷ (1/2 + 1/4).', 'First: 3/2 + 1/4 = 7/4. Second: 3/4 ÷ 3/4 = 1. Division before addition unless brackets say otherwise.', 'B1 both values; B1 reason. [2]'),
])


# ----------------------------------------------------------- multiplying and dividing fractions
t83 = topic('Multiplying and dividing fractions and mixed numbers', 'multiplying and dividing fractions and mixed numbers', 'mixed numbers')
MIX = [Fr(3, 2), Fr(5, 2), Fr(7, 4), Fr(9, 4), Fr(4, 3), Fr(5, 3), Fr(7, 3), Fr(11, 4), Fr(13, 5), Fr(7, 2), Fr(6, 5), Fr(8, 3), Fr(15, 4), Fr(11, 3)]


@t83.add('C3', (1, 2, 3, 4, 5))
def t83_calc(r, D):
    a, b = r.sample(MIX if D >= 2 else FRS, 2)
    op = r.choice(['×', '÷'])
    v = a * b if op == '×' else a / b
    show = mixed if D >= 2 else fr
    if D >= 4:
        c = r.choice(MIX)
        op2 = r.choice(['×', '÷'])
        v = (a * b if op == '×' else a / b)
        v = v * c if op2 == '×' else v / c
        return Q(f'Work out {mixed(a)} {op} {mixed(b)} {op2} {mixed(c)}. Give your answer as a mixed number.', mixed(v),
                 f'Improper fractions {fr(a)}, {fr(b)}, {fr(c)} (M1); {"multiply by reciprocals for ÷ " if "÷" in op + op2 else ""}(M1); {mixed(v)} (A1).', marks=3)
    key = f'Change to improper fractions: {fr(a)} {op} {fr(b)} (M1); ' + (f'multiply by the reciprocal {fr(1 / b)} ' if op == '÷' else '') + f'= {fr(v)}' + (f' = {mixed(v)}' if mixed(v) != fr(v) else '') + ' (A1).'
    if D == 1:
        w = [fr(a + b), fr(Fr(a.numerator * b.numerator, a.denominator + b.denominator)), fr(b / a if op == '÷' else a / b), fr(a * b if op == '÷' else a / b)]
        return MCQ(r, f'Work out {show(a)} {op} {show(b)}.', fr(v), w, key)
    return Q(r.choice([f'Work out {show(a)} {op} {show(b)}. Give your answer as a mixed number in its simplest form.', f'Calculate {show(a)} {op} {show(b)} without a calculator.']), mixed(v), key)


@t83.add('C1', (1, 2, 3))
def t83_recip(r, D):
    a = r.choice(MIX)
    return MCQ(r, f'What is the reciprocal of {mixed(a)}?', fr(1 / a), [mixed(a).split(' ')[0] + ' ' + f'{a.denominator}/{a.numerator % a.denominator}' if a.numerator % a.denominator else '1', fr(a), f'1/{a.denominator}', f'{a.denominator}/{a.numerator % a.denominator}'],
               f'{mixed(a)} = {fr(a)}; reciprocal {fr(1 / a)}. [1]')


@t83.add('C2', (1, 2, 3, 4), 'explain')
def t83_err(r, D):
    w1, w2 = r.randint(1, 4), r.randint(1, 4)
    f1, f2 = r.choice([Fr(1, 2), Fr(1, 3), Fr(1, 4), Fr(2, 3), Fr(3, 4)]), r.choice([Fr(1, 2), Fr(1, 3), Fr(1, 4), Fr(2, 5)])
    a, b = w1 + f1, w2 + f2
    p = person(r)
    if r.random() < 0.5:
        wrong = w1 * w2 + f1 * f2
        return Q(f'{p} works out {mixed(a)} × {mixed(b)} by multiplying the whole numbers and the fractions separately: {w1} × {w2} + {fr(f1)} × {fr(f2)} = {mixed(wrong)}. Explain why this is wrong and find the correct answer.',
                 f'This misses the products {w1} × {fr(f2)} and {fr(f1)} × {w2}. Correct: {fr(a)} × {fr(b)} = {mixed(a * b)}.', 'B1 explanation (missing cross terms / use improper fractions); B1 correct answer. [2]')
    return Q(f'{p} works out {mixed(a)} ÷ {mixed(b)} by turning the first fraction upside down: {fr(1 / a)} × {fr(b)}. Explain the mistake and find the correct answer.',
             f'You multiply by the reciprocal of the SECOND fraction (the divisor): {fr(a)} × {fr(1 / b)} = {mixed(a / b)}.', 'B1 reciprocal of divisor; B1 correct answer. [2]')


@t83.add('C2', (2, 3, 4), 'explain')
def t83_est(r, D):
    a, b = r.sample(MIX, 2)
    p = person(r)
    v = a * b
    return Q(f'Without working it out exactly, explain why {mixed(a)} × {mixed(b)} must be between {math.floor(a) * math.floor(b)} and {math.ceil(a) * math.ceil(b)}.',
             f'{mixed(a)} is between {math.floor(a)} and {math.ceil(a)}, and {mixed(b)} is between {math.floor(b)} and {math.ceil(b)}, so the product is between {math.floor(a) * math.floor(b)} and {math.ceil(a) * math.ceil(b)} (it is {mixed(v)}).',
             'B1 bounds for each number; B1 conclusion. [2]')


def _mix_c4(r, D):
    p = person(r)
    L = r.choice([Fr(15, 2), Fr(25, 4), Fr(27, 2), Fr(35, 4), Fr(21, 2)])
    piece = r.choice([Fr(3, 4), Fr(5, 4), Fr(3, 2), Fr(5, 8)])
    n = int(L / piece)
    left = L - n * piece
    w = r.choice(MIX[:6])
    intro = f'{p} has a ribbon {mixed(L)} m long.'
    parts = [
        lambda r: (f'How many pieces of length {fr(piece)} m can be cut from the ribbon?', str(n), f'M1 {mixed(L)} ÷ {fr(piece)} = {mixed(L / piece)}; A1 {n} [2]'),
        lambda r: (f'Work out the length of ribbon left over after cutting as many {fr(piece)} m pieces as possible.', f'{fr(left)} m', f'M1 {mixed(L)} − {n} × {fr(piece)}; A1 [2]'),
        lambda r: (f'{p} uses the ribbon to go round a rectangle {mixed(w)} m long and {fr(Fr(1, 2) * w)} m wide. Is the ribbon long enough? Show your working.',
                   f'Perimeter = {mixed(3 * w)} m; {"yes" if 3 * w <= L else "no"} ({mixed(L)} {"≥" if 3 * w <= L else "<"} {mixed(3 * w)})', 'M1 perimeter; A1 comparison [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t83.add('C4', (2, 3, 4, 5), 'multi_step')(_mix_c4)


@t83.add('C4', (3, 4, 5), 'multi_step')
def t83_recipe(r, D):
    flour = r.choice(MIX)
    serves = r.choice([4, 6, 8])
    new = r.choice([s for s in (3, 5, 9, 10, 12) if s != serves])
    return Q(f'A recipe for {serves} people uses {mixed(flour)} cups of flour. (a) Work out how much flour is needed for {new} people. (b) A bag holds 10 cups. How many times can the recipe for {serves} people be made from a full bag?',
             f'(a) {mixed(flour * new / serves)} cups (b) {int(10 / flour)} times', f'(a) M1 {mixed(flour)} × {new}/{serves}; A1 {mixed(flour * new / serves)} [2] (b) M1 10 ÷ {mixed(flour)} = {mixed(10 / flour)}; A1 {int(10 / flour)} [2]', marks=4)


t83.fixed('C1', (1, 2), [
    ('Work out 2/3 × 9/10.', '3/5', '18/30 = 3/5. [1]', ['11/13', '27/20', '2/9']),
    ('Work out 3/4 ÷ 3/8.', '2', '3/4 × 8/3 = 2. [1]', ['9/32', '1/2', '6/12']),
    ('Write 3 2/5 as an improper fraction.', '17/5', 'B1 [1]'),
])
t83.fixed('C2', (2, 3), [
    ('Explain why dividing by 1/4 is the same as multiplying by 4.', 'There are 4 quarters in every 1, so the number of quarters in x is 4x.', 'B1 B1. [2]'),
])


# ----------------------------------------------------------- strategies
t84 = topic('Making calculations easier using fraction strategies', 'making calculations easier', 'fraction strategies')
EQUIV = [(0.5, Fr(1, 2)), (0.25, Fr(1, 4)), (0.75, Fr(3, 4)), (0.2, Fr(1, 5)), (0.125, Fr(1, 8)), (0.375, Fr(3, 8)), (0.4, Fr(2, 5)), (0.6, Fr(3, 5)), (1.5, Fr(3, 2)), (1.25, Fr(5, 4)), (0.05, Fr(1, 20)), (0.875, Fr(7, 8))]


@t84.add('C1', (1, 2, 3))
def t84_eq(r, D):
    d, f = r.choice(EQUIV)
    return MCQ(r, f'Which fraction is equal to {N(d)}?', fr(f), [fr(Fr(int(d * 100), 1000)) if d < 1 else fr(f + 1), fr(Fr(f.denominator, f.numerator)), fr(Fr(1, int(1 / d) + 1)) if d < 1 else fr(f - Fr(1, 4)), fr(f / 2)],
               f'{N(d)} = {fr(f)}. [1]')


@t84.add('C3', (1, 2, 3, 4, 5))
def t84_calc(r, D):
    d, f = r.choice(EQUIV)
    kind = r.choice(['mul', 'div', 'pct', 'cancel'])
    if kind == 'mul':
        x = f.denominator * r.randint(3, 40)
        return Q(f'Work out {N(d)} × {x} without a calculator. Show the strategy you use.', N(f * x), f'{N(d)} = {fr(f)} (M1); {fr(f)} of {x} = {N(f * x)} (A1).')
    if kind == 'div':
        x = f.numerator * r.randint(2, 30)
        return Q(f'Work out {x} ÷ {N(d)} without a calculator.', N(x / f), f'÷ {fr(f)} = × {fr(1 / f)} (M1); {x} × {fr(1 / f)} = {N(x / f)} (A1).')
    if kind == 'pct':
        p, pf = r.choice([(12.5, Fr(1, 8)), (37.5, Fr(3, 8)), (15, Fr(3, 20)), (35, Fr(7, 20)), (62.5, Fr(5, 8)), (5, Fr(1, 20))])
        x = pf.denominator * r.randint(3, 25)
        return Q(f'Use a fraction to work out {N(p)}% of {x}.', N(pf * x), f'{N(p)}% = {fr(pf)} (M1); {fr(pf)} × {x} = {N(pf * x)} (A1).')
    a, b = r.choice([(Fr(14, 15), Fr(25, 28)), (Fr(9, 16), Fr(8, 27)), (Fr(21, 25), Fr(10, 49)), (Fr(12, 35), Fr(14, 18)), (Fr(15, 32), Fr(24, 25))])
    return Q(f'Work out {fr(a)} × {fr(b)} by cancelling common factors first.', fr(a * b), f'Cancel common factors across numerators and denominators (M1); {fr(a * b)} (A1).')


@t84.add('C2', (1, 2, 3, 4), 'explain')
def t84_why(r, D):
    d, f = r.choice(EQUIV)
    x = f.denominator * r.randint(4, 30)
    p, q = two_people(r)
    return Q(f'{p} works out {N(d)} × {x} using long multiplication. {q} says it is easier to work out {fr(f)} of {x}. Explain why {q}\'s method works, and use it.',
             f'{N(d)} = {fr(f)}, so multiplying by {N(d)} is the same as finding {fr(f)} of the number: {x} ÷ {f.denominator} × {f.numerator} = {N(f * x)}.',
             'B1 equivalence; B1 correct answer. [2]')


@t84.add('C2', (2, 3, 4), 'explain')
def t84_div(r, D):
    d, f = r.choice([(0.25, Fr(1, 4)), (0.2, Fr(1, 5)), (0.5, Fr(1, 2)), (0.125, Fr(1, 8)), (0.05, Fr(1, 20))])
    x = r.randint(6, 60)
    p = person(r)
    return Q(f'{p} says that dividing {x} by {N(d)} gives a smaller answer than {x}. Explain why {p} is wrong, using fractions.',
             f'{N(d)} = {fr(f)}; dividing by {fr(f)} is the same as multiplying by {f.denominator}, so {x} ÷ {N(d)} = {x * f.denominator}, which is larger.',
             'B1 reciprocal; B1 value. [2]')


def _strat_c4(r, D):
    p = person(r)
    price = r.choice([24, 32, 40, 48, 64, 72, 80, 96])
    pct, pf = r.choice([(12.5, Fr(1, 8)), (25, Fr(1, 4)), (37.5, Fr(3, 8)), (20, Fr(1, 5))])
    n = r.choice([4, 8, 12])
    intro = f'A shop in {city(r)} sells jackets for ${price}. In a sale all prices are reduced by {N(pct)}%.'
    parts = [
        lambda r: (f'Write {N(pct)}% as a fraction in its simplest form.', fr(pf), 'B1 [1]'),
        lambda r: ('Use your fraction to work out the sale price of a jacket, without a calculator.', money(price * (1 - float(pf))), f'M1 {fr(pf)} × {price} = {N(pf * price)}; A1 {money(price * (1 - float(pf)))} [2]'),
        lambda r: (f'Work out the total sale price of {n} jackets, explaining a quick method.', money(n * price * (1 - float(pf))), f'M1 × {n} (or {fr(1 - pf)} of {n * price}); A1 [2]'),
        lambda r: (f'The sale price is then reduced by a further 0.5 of the sale price. Work out the final price.', money(price * (1 - float(pf)) / 2), 'M1 halve; A1 [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t84.add('C4', (2, 3, 4, 5), 'multi_step')(_strat_c4)


@t84.add('C4', (3, 4, 5), 'multi_step')
def t84_combo(r, D):
    x = r.choice([48, 64, 72, 96, 120, 144])
    return Q(f'Without a calculator, work out (a) 0.375 × {x}, (b) {x} ÷ 0.125, (c) 1.25 × {x} − 0.75 × {x}. Explain the strategy you use in each part.',
             f'(a) {N(Fr(3, 8) * x)} (b) {x * 8} (c) {x // 2}', f'(a) M1 3/8 of {x}; A1 [2] (b) B1 × 8 [1] (c) M1 (1.25 − 0.75) × {x} = 0.5 × {x}; A1 {x // 2} [2]', marks=5)


t84.fixed('C1', (1, 2), [
    ('Which calculation gives the same answer as 36 × 0.25?', '36 ÷ 4', '0.25 = 1/4. [1]', ['36 × 4', '36 ÷ 25', '36 − 25']),
    ('Which calculation gives the same answer as 18 ÷ 0.5?', '18 × 2', '÷ 1/2 = × 2. [1]', ['18 ÷ 2', '18 × 0.2', '18 − 0.5']),
    ('Write 0.125 as a fraction in its simplest form.', '1/8', 'B1 [1]'),
])
t84.fixed('C2', (2, 3), [
    ('Explain how to work out 16 × 2.5 quickly in your head.', '2.5 = 5/2, so 16 × 2.5 = 16 ÷ 2 × 5 = 40 (or 16 × 10 ÷ 4).', 'B1 strategy; B1 40. [2]'),
])

CHAPTERS[8] = [t81, t82, t83, t84]


# =========================================================== 9 Sequences and functions
def seqs(f, n=5, start=1):
    return ', '.join(N(f(k)) for k in range(start, start + n))


t91 = topic('Term-to-term and position-to-term rules', 'generating sequences', 'term-to-term', 'position-to-term rules')


@t91.add('C1', (1, 2, 3))
def t91_next(r, D):
    a = r.randint(-5, 20)
    kind = r.choice(['add', 'mul', 'sub'] if D < 3 else ['mul', 'twostep', 'sub'])
    if kind == 'add':
        d = r.randint(2, 9)
        terms = [a + d * i for i in range(4)]
        nxt, rule = a + 4 * d, f'add {d}'
        ds = [nxt + d, nxt - 1, terms[-1] * 2]
    elif kind == 'sub':
        d = r.randint(2, 9)
        terms = [a + 30 - d * i for i in range(4)]
        nxt, rule = terms[-1] - d, f'subtract {d}'
        ds = [terms[-1] + d, nxt - d, nxt + 1]
    elif kind == 'mul':
        m = r.choice([2, 3, -2])
        a = r.randint(1, 5)
        terms = [a * m ** i for i in range(4)]
        nxt, rule = terms[-1] * m, f'multiply by {N(m)}'
        ds = [terms[-1] + (terms[-1] - terms[-2]), nxt + m, -nxt]
    else:
        m, c = r.choice([2, 3]), r.choice([-1, 1, 2, -3])
        a = r.randint(1, 4)
        terms = [a]
        for _ in range(3):
            terms.append(terms[-1] * m + c)
        nxt, rule = terms[-1] * m + c, f'multiply by {m} then {"add" if c > 0 else "subtract"} {abs(c)}'
        ds = [terms[-1] * m, terms[-1] + (terms[-1] - terms[-2]), nxt + 1]
    return MCQ(r, f'The term-to-term rule of a sequence is "{rule}". The sequence starts {", ".join(N(t) for t in terms)}, … What is the next term?' if D >= 2 else f'What is the next term in the sequence {", ".join(N(t) for t in terms)}, …?',
               N(nxt), [N(x) for x in ds] + [N(nxt + 2)], f'Rule: {rule} → {N(nxt)}. [1]')


@t91.add('C1', (1, 2, 3))
def t91_pos(r, D):
    a, b = r.randint(2, 9), r.randint(-9, 9)
    if D >= 3 and r.random() < 0.5:
        f = lambda n: n * n + b
        e = f'n² {"+" if b >= 0 else MINUS} {abs(b)}' if b else 'n²'
        ds = [seqs(lambda n: 2 * n + b, 4), seqs(lambda n: n * n, 4) if b else seqs(lambda n: n * n + 1, 4), seqs(lambda n: (n + 1) ** 2 + b, 4)]
    else:
        f = lambda n: a * n + b
        e = lin(a, b, 'n')
        ds = [seqs(lambda n: a * n + b + a, 4), seqs(lambda n: n + a + b, 4), seqs(lambda n: b * n + a, 4) if b else seqs(lambda n: a * n + 1, 4)]
    return MCQ(r, f'The nth term of a sequence is {e}. What are the first four terms?', seqs(f, 4), ds + [seqs(lambda n: f(n) + 1, 4)], f'Substitute n = 1, 2, 3, 4: {seqs(f, 4)}. [1]')


@t91.add('C3', (1, 2, 3, 4, 5))
def t91_gen(r, D):
    kind = r.choice(['pos', 'tt', 'term'] if D >= 2 else ['pos', 'tt'])
    if kind == 'pos':
        a, b = r.randint(2, 9), r.randint(-12, 12)
        if D >= 4:
            c = r.randint(-6, 6)
            f = lambda n: a * n * n + c if a < 4 else n * n + b * n + c
            e = (f'{a}n² {"+" if c >= 0 else MINUS} {abs(c)}' if a < 4 else poly((1, 'n²'), (b, 'n'), (c, '')))
        else:
            f = lambda n: a * n + b
            e = lin(a, b, 'n')
        return Q(f'Write down the first four terms of the sequence with nth term {e}.', seqs(f, 4), f'n = 1, 2, 3, 4 substituted (M1); {seqs(f, 4)} (A1).')
    if kind == 'tt':
        s = r.randint(-3, 12)
        m, c = r.choice([(1, 7), (1, -4), (2, 1), (2, -3), (3, -5), (-1, 10), (1, 13)])
        terms = [s]
        for _ in range(4):
            terms.append(terms[-1] * m + c)
        rule = (f'add {c}' if c > 0 else f'subtract {-c}') if m == 1 else f'multiply by {N(m)} then {"add" if c > 0 else "subtract"} {abs(c)}'
        return Q(f'The first term of a sequence is {N(s)}. The term-to-term rule is "{rule}". Write down the next four terms.', ', '.join(N(t) for t in terms[1:]),
                 f'Apply the rule repeatedly (M1): {", ".join(N(t) for t in terms[1:])} (A1).')
    a, b = r.randint(2, 9), r.randint(-12, 12)
    k = r.choice([20, 25, 50, 100])
    return Q(f'The nth term of a sequence is {lin(a, b, "n")}. Work out the {k}th term.', N(a * k + b), f'{a} × {k} {"+" if b >= 0 else "−"} {abs(b)} (M1) = {N(a * k + b)} (A1).')


@t91.add('C2', (1, 2, 3, 4), 'explain')
def t91_inseq(r, D):
    a, b = r.randint(3, 9), r.randint(-5, 9)
    x = r.randint(20, 120)
    p = person(r)
    ok = (x - b) % a == 0 and (x - b) // a >= 1
    return Q(f'The nth term of a sequence is {lin(a, b, "n")}. {p} says {x} is a term in the sequence. Is {p} correct? Explain.',
             f'{"Yes" if ok else "No"}: {lin(a, b, "n")} = {x} gives n = ({x} {"−" if b >= 0 else "+"} {abs(b)}) ÷ {a} = {N(Fr(x - b, a)) if ok else mixed(Fr(x - b, a))}, which {"is" if ok else "is not"} a positive whole number.',
             'M1 forms and solves an equation (or lists terms); A1 conclusion with reason. [2]')


@t91.add('C2', (1, 2, 3, 4), 'explain')
def t91_err(r, D):
    d = r.randint(2, 9)
    a = r.randint(-4, 12)
    terms = [a + d * i for i in range(4)]
    p = person(r)
    return Q(f'The sequence {", ".join(N(t) for t in terms)}, … has term-to-term rule "add {d}". {p} says the position-to-term rule is n + {d}. Explain why {p} is wrong and give the correct rule.',
             f'n + {d} gives {1 + d}, {2 + d}, {3 + d}, … which goes up by 1 each time. Going up by {d} means {d}n; since the first term is {N(a)}, the rule is {lin(d, a - d, "n")}.',
             'B1 explanation (difference gives coefficient of n); B1 correct nth term. [2]')


@t91.add('C2', (2, 3, 4), 'explain')
def t91_compare(r, D):
    a, b = r.randint(2, 6), r.randint(1, 9)
    c, d = a + r.randint(1, 3), b - r.randint(4, 15)
    n0 = math.floor(Fr(b - d, c - a)) + 1
    p, q = two_people(r)
    return Q(f'{p}\'s sequence has nth term {lin(a, b, "n")}. {q}\'s sequence has nth term {lin(c, d, "n")}. Explain why {q}\'s terms will eventually be larger than {p}\'s, and find the first position where this happens.',
             f'{q}\'s sequence increases by {c} each time, {p}\'s by {a}, so {q}\'s catches up. {lin(c, d, "n")} > {lin(a, b, "n")} when n > {mixed(Fr(b - d, c - a))}, so first at n = {n0}.',
             'B1 compares differences; B1 first position. [2]')


def _pattern_c4(r, D):
    a, b = r.randint(2, 6), r.randint(1, 5)
    item = r.choice(['matchsticks', 'tiles', 'counters', 'squares'])
    f = lambda n: a * n + b
    big = r.choice([20, 30, 50])
    have = r.choice([100, 150, 200, 250])
    nmax = (have - b) // a
    intro = f'Pattern 1 uses {f(1)} {item}, pattern 2 uses {f(2)} {item} and pattern 3 uses {f(3)} {item}. The number of {item} increases by the same amount each time.'
    parts = [
        lambda r: ('Write down the term-to-term rule.', f'Add {a}', 'B1 [1]'),
        lambda r: (f'Find an expression for the number of {item} in pattern n.', lin(a, b, 'n'), f'M1 {a}n; A1 {lin(a, b, "n")} [2]'),
        lambda r: (f'How many {item} are in pattern {big}?', str(f(big)), f'M1 {a} × {big} + {b}; A1 [2]'),
        lambda r: (f'{person(r)} has {have} {item}. What is the largest pattern that can be made?', f'Pattern {nmax}', f'M1 {lin(a, b, "n")} ≤ {have}; A1 {nmax} [2]'),
        lambda r: (f'Explain why no pattern uses exactly {f(5) + 1} {item}.', f'{f(5) + 1} − {b} = {f(5) + 1 - b} is not a multiple of {a}.', 'B1 [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t91.add('C4', (2, 3, 4, 5), 'multi_step')(_pattern_c4)
t91.fixed('C1', (1, 2), [
    ('What is a term-to-term rule?', 'A rule that tells you how to get from one term to the next', 'B1 [1]', ['A rule that gives a term from its position', 'The first term of a sequence', 'The difference between the first and last terms']),
    ('The position-to-term rule of a sequence is 4n. What is the 10th term?', '40', '4 × 10. [1]', ['14', '44', '410']),
    ('Write down the first three terms of the sequence with nth term 2n + 5.', '7, 9, 11', 'B1 [1]'),
])
t91.fixed('C2', (2, 3), [
    ('Explain why a position-to-term rule is more useful than a term-to-term rule for finding the 100th term.', 'With a position-to-term rule you substitute n = 100 directly; with a term-to-term rule you must work out all 99 previous terms.', 'B1 B1. [2]'),
])


# ----------------------------------------------------------- nth term
t92 = topic('Finding and using the nth term', 'finding and using the nth term', 'linear and quadratic sequences', 'nth term')


@t92.add('C1', (1, 2, 3))
def t92_mcq(r, D):
    d = r.choice([2, 3, 4, 5, 6, 7, -2, -3]) if D > 1 else r.randint(2, 7)
    a = r.randint(-5, 15)
    terms = [a + d * i for i in range(4)]
    ans = lin(d, a - d, 'n')
    return MCQ(r, f'Which expression is the nth term of the sequence {", ".join(N(t) for t in terms)}, …?', ans,
               [lin(1, d, 'n'), lin(d, a, 'n'), lin(a, d, 'n') if a != d else lin(d, a + d, 'n'), lin(-d, a - d, 'n')], f'Difference {N(d)} → {N(d)}n; first term {N(a)} → {ans}. [1]')


@t92.add('C3', (1, 2, 3, 4, 5))
def t92_find(r, D):
    if D <= 3 or r.random() < 0.4:
        d = r.choice([2, 3, 4, 5, 6, 7, 8, 9] + ([-2, -3, -4, -5, 0.5, 1.5] if D >= 3 else []))
        a = r.randint(-8, 20)
        terms = [a + d * i for i in range(5)]
        ans = poly((d, 'n'), (a - d, ''))
        return Q(r.choice([f'Find an expression for the nth term of the sequence {", ".join(N(t) for t in terms)}, …', f'Here are the first five terms of a sequence: {", ".join(N(t) for t in terms)}. Find the nth term.']),
                 ans, f'Common difference {N(d)} (M1); {N(d)}n + ({N(a)} − {par(d)}) = {ans} (A1).')
    k = r.choice([1, 2, 3])
    c = r.randint(-6, 8)
    sh = r.choice([0, 0, 1]) if k == 1 else 0
    f = lambda n: k * (n + sh) ** 2 + c
    terms = [f(n) for n in range(1, 6)]
    e = (f'{"" if k == 1 else k}' + (f'(n + {sh})²' if sh else 'n²') + (f' {"+" if c >= 0 else MINUS} {abs(c)}' if c else ''))
    return Q(f'Find an expression for the nth term of the quadratic sequence {", ".join(N(t) for t in terms)}, …', e,
             f'Second difference {2 * k} so the n² coefficient is {k} (M1); compare with {"" if k == 1 else k}n²: {seqs(lambda n: k * n * n, 5)} (M1); nth term {e} (A1).', marks=3)


@t92.add('C3', (2, 3, 4, 5))
def t92_which(r, D):
    d, a = r.randint(3, 9), r.randint(-5, 10)
    n = r.randint(12, 60)
    v = d * n + a - d
    return Q(f'A sequence starts {", ".join(N(a + d * i) for i in range(4))}, … Which term in the sequence is equal to {v}?', f'The {n}th term',
             f'nth term {lin(d, a - d, "n")} (M1); {lin(d, a - d, "n")} = {v} (M1); n = {n} (A1).', marks=3)


@t92.add('C2', (1, 2, 3, 4), 'explain')
def t92_explain(r, D):
    d, a = r.randint(2, 9), r.randint(-5, 15)
    terms = [a + d * i for i in range(4)]
    return Q(f'Explain why the nth term of {", ".join(N(t) for t in terms)}, … is {lin(d, a - d, "n")}.',
             f'The terms increase by {d}, so they are related to the {d} times table ({d}n: {seqs(lambda n: d * n, 4)}). Each term is {N(a - d)} {"more" if a - d >= 0 else "less"} than {d}n, so nth term = {lin(d, a - d, "n")}.',
             'B1 difference links to coefficient; B1 adjustment explained. [2]')


@t92.add('C2', (2, 3, 4), 'explain')
def t92_quad(r, D):
    c = r.randint(-5, 9)
    terms = [n * n + c for n in range(1, 6)]
    p = person(r)
    return Q(f'{p} says the sequence {", ".join(N(t) for t in terms)}, … is linear. Explain how you can tell that it is quadratic, and give its nth term.',
             f'The first differences are {", ".join(str(terms[i + 1] - terms[i]) for i in range(4))}, which are not constant; the second differences are all 2, so it is quadratic. nth term n² {"+" if c >= 0 else "−"} {abs(c)}.',
             'B1 differences not constant / second difference constant; B1 nth term. [2]')


@t92.add('C2', (2, 3, 4), 'explain')
def t92_err(r, D):
    d = r.randint(2, 9)
    a = r.randint(d + 1, d + 15)
    terms = [a - d * i for i in range(4)]
    p = person(r)
    return Q(f'{p} says the nth term of {", ".join(N(t) for t in terms)}, … is {lin(d, a + d, "n")}. Explain the mistake and find the correct nth term.',
             f'The sequence decreases by {d}, so the coefficient of n is −{d}, not {d}. nth term = {lin(-d, a + d, "n")}.', 'B1 negative difference; B1 correct nth term. [2]')


def _nth_c4(r, D):
    d1, a1 = r.randint(2, 6), r.randint(1, 10)
    d2, a2 = d1 + r.randint(1, 3), a1 - r.randint(5, 20)
    s1 = [a1 + d1 * i for i in range(4)]
    s2 = [a2 + d2 * i for i in range(4)]
    n0 = Fr(a1 - d1 - (a2 - d2), d2 - d1)
    first = math.floor(n0) + 1 if n0.denominator != 1 else int(n0) + 1
    intro = f'Sequence A is {", ".join(N(t) for t in s1)}, … and sequence B is {", ".join(N(t) for t in s2)}, …'
    parts = [
        lambda r: ('Find the nth term of sequence A.', lin(d1, a1 - d1, 'n'), 'M1; A1 [2]'),
        lambda r: ('Find the nth term of sequence B.', lin(d2, a2 - d2, 'n'), 'M1; A1 [2]'),
        lambda r: ('Find the first position where the term in B is greater than the term in A.', f'n = {first}', f'M1 {lin(d2, a2 - d2, "n")} > {lin(d1, a1 - d1, "n")}; A1 [2]'),
        lambda r: ('Is there a position where the two sequences have the same term? Explain.', ('Yes, at n = ' + N(n0)) if n0.denominator == 1 else f'No: they would be equal at n = {mixed(n0)}, which is not a whole number.', 'M1 solves equation; A1 conclusion [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t92.add('C4', (2, 3, 4, 5), 'multi_step')(_nth_c4)


@t92.add('C4', (3, 4, 5), 'multi_step')
def t92_dots(r, D):
    c = r.randint(1, 5)
    f = lambda n: n * n + c
    k = r.randint(10, 20)
    return Q(f'A pattern of dots has {f(1)}, {f(2)}, {f(3)} and {f(4)} dots in the first four diagrams. (a) Show that the sequence is quadratic. (b) Find the nth term. (c) Work out the number of dots in diagram {k}. (d) Which diagram has {f(k + 3)} dots?',
             f'(a) Second differences are constant (2). (b) n² + {c} (c) {f(k)} (d) Diagram {k + 3}',
             f'(a) B1 [1] (b) M1 n²; A1 n² + {c} [2] (c) B1 [1] (d) M1 n² = {f(k + 3) - c}; A1 [2]', marks=6)


t92.fixed('C1', (1, 2), [
    ('What is the nth term of the square numbers 1, 4, 9, 16, …?', 'n²', 'B1 [1]', ['2n', 'n + 3', '4n − 3']),
    ('The nth term of a sequence is 20 − 3n. What is the common difference?', '−3', 'Coefficient of n. [1]', ['3', '20', '17']),
    ('What is the second difference of a sequence with nth term n² + 4?', '2', 'B1 [1]'),
])
t92.fixed('C2', (2, 3), [
    ('Explain how you can tell from its nth term whether a sequence is linear or quadratic.', 'Linear sequences have nth term an + b (no n²); quadratic sequences have an n² term.', 'B1 B1. [2]'),
])


# ----------------------------------------------------------- functions and inverses
t93 = topic('Functions and inverse functions', 'functions as mappings', 'inverse functions', 'functions')


def fm(a, b):
    """mapping string x -> ax + b"""
    return f'x → {lin(a, b)}'


def inv(a, b):
    if a == 1:
        return f'x → {lin(1, -b)}'
    if b == 0:
        return f'x → x/{a}'
    return f'x → (x {"−" if b > 0 else "+"} {abs(b)})/{a}'


@t93.add('C1', (1, 2, 3))
def t93_out(r, D):
    a, b = r.randint(2, 7), r.choice(NZ)
    x = r.randint(-5, 10) if D > 1 else r.randint(1, 9)
    return MCQ(r, f'A function is {fm(a, b)}. What is the output when the input is {N(x)}?', N(a * x + b), [N(a * (x + b)), N(x + a + b), N(a * x - b), N(Fr(x - b, a)) if (x - b) % a == 0 else N(a * x)],
               f'{a} × {par(x)} {"+" if b > 0 else "−"} {abs(b)} = {N(a * x + b)}. [1]')


@t93.add('C1', (1, 2, 3))
def t93_inv_mcq(r, D):
    a, b = r.choice([1, 2, 3, 4, 5]), r.choice(NZ)
    if D == 1:
        a = 1
    ans = inv(a, b)
    ds = [f'x → {lin(a, -b)}' if a > 1 else f'x → {lin(1, b)}', f'x → x/{a} {"−" if b > 0 else "+"} {abs(b)}' if a > 1 else f'x → {lin(-1, b)}', f'x → {lin(-a, -b)}', f'x → (x {"+" if b > 0 else "−"} {abs(b)})/{a}' if a > 1 else f'x → {lin(2, -b)}']
    return MCQ(r, f'What is the inverse of the function {fm(a, b)}?', ans, ds, f'Reverse the operations in reverse order: {ans}. [1]')


@t93.add('C3', (1, 2, 3, 4, 5))
def t93_calc(r, D):
    a, b = r.randint(2, 9), r.choice(NZ)
    kind = r.choice(['inv', 'input', 'table'] if D < 4 else ['inv', 'input', 'two'])
    if kind == 'inv':
        return Q(r.choice([f'Find the inverse of the function {fm(a, b)}.', f'f(x) = {lin(a, b)}. Write down the inverse function.']), inv(a, b),
                 f'Write y = {lin(a, b)} and make x the subject (M1): {inv(a, b)} (A1).')
    if kind == 'input':
        y = a * r.randint(-6, 12) + b
        return Q(f'A function maps x to {lin(a, b)}. The output is {N(y)}. Work out the input.', N(Fr(y - b, a)), f'{lin(a, b)} = {N(y)} or use the inverse (M1); x = {N(Fr(y - b, a))} (A1).')
    if kind == 'table':
        xs = r.sample(range(-3, 8), 4)
        xs.sort()
        return Q(f'Complete the table of outputs for the function {fm(a, b)} for the inputs {", ".join(N(x) for x in xs)}.', ', '.join(N(a * x + b) for x in xs),
                 f'Substitute each input (M1); {", ".join(N(a * x + b) for x in xs)} (A1).')
    c, d = r.randint(2, 5), r.choice(NZ)
    return Q(f'A function machine first multiplies by {a} and adds {N(b)}, then multiplies the result by {c}. (a) Write the function as x → … (b) Find the inverse function.',
             f'(a) x → {c}({lin(a, b)}) = {lin(a * c, b * c)} (b) x → (x/{c} {"−" if b > 0 else "+"} {abs(b)})/{a}',
             f'(a) B1 [1] (b) M1 reverse order: ÷ {c}, {"subtract" if b > 0 else "add"} {abs(b)}, ÷ {a}; A1 [2]', marks=3)


@t93.add('C2', (1, 2, 3, 4), 'explain')
def t93_err(r, D):
    a, b = r.randint(2, 7), r.randint(1, 9)
    p = person(r)
    return Q(f'{p} says the inverse of {fm(a, b)} is x → x/{a} − {b}. Test {p}\'s answer with an input of 2, and explain the mistake.',
             f'{fm(a, b)} maps 2 to {2 * a + b}. {p}\'s inverse maps {2 * a + b} to {N(Fr(2 * a + b, a) - b)}, not 2. The operations must be reversed in reverse order: subtract {b} first, then divide by {a}: x → (x − {b})/{a}.',
             'M1 tests a value through both; A1 explains order and gives correct inverse. [2]')


@t93.add('C2', (2, 3, 4), 'explain')
def t93_self(r, D):
    c = r.randint(3, 15)
    p = person(r)
    return Q(f'{p} says the function x → {c} − x is its own inverse. Is {p} correct? Explain.',
             f'Yes. Applying it twice: x → {c} − x → {c} − ({c} − x) = x, so it undoes itself.', 'M1 applies twice or finds inverse; A1 conclusion. [2]')


def _fn_c4(r, D):
    a, b = r.randint(2, 6), r.choice(NZ)
    x1 = r.randint(1, 6)
    y = a * r.randint(3, 10) + b
    intro = f'A function is defined by f: {fm(a, b)}.'
    fixed = Fr(-b, a - 1)
    parts = [
        lambda r: (f'Work out the output when the input is {x1}.', N(a * x1 + b), 'B1 [1]'),
        lambda r: ('Find the inverse function.', inv(a, b), 'M1 reverse operations; A1 [2]'),
        lambda r: (f'Use the inverse to find the input that gives an output of {N(y)}.', N(Fr(y - b, a)), 'M1; A1 [2]'),
        lambda r: ('Find the input that gives an output equal to the input.', mixed(fixed), f'M1 {lin(a, b)} = x; A1 [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t93.add('C4', (2, 3, 4, 5), 'multi_step')(_fn_c4)


@t93.add('C4', (3, 4, 5), 'multi_step')
def t93_temp(r, D):
    C = r.choice([10, 20, 25, 30, 35])
    return Q(f'The function x → 1.8x + 32 converts temperatures from °C to °F. (a) Convert {C} °C to °F. (b) Find the inverse function. (c) Use the inverse to convert {N(1.8 * (C + 15) + 32)} °F to °C. (d) Explain what the inverse function does.',
             f'(a) {N(1.8 * C + 32)} °F (b) x → (x − 32)/1.8 (c) {C + 15} °C (d) It converts °F back to °C.',
             '(a) B1 [1] (b) M1; A1 [2] (c) M1; A1 [2] (d) B1 [1]', marks=6)


t93.fixed('C1', (1, 2), [
    ('What is the inverse of x → x + 9?', 'x → x − 9', 'B1 [1]', ['x → 9 − x', 'x → x/9', 'x → 9x']),
    ('What is the inverse of x → 4x?', 'x → x/4', 'B1 [1]', ['x → x − 4', 'x → 4/x', 'x → −4x']),
    ('A function maps 3 to 11 and 5 to 17. Write down the output for 4.', '14', 'Linear function x → 3x + 2. B1 [1]'),
])
t93.fixed('C2', (2, 3), [
    ('Explain what an inverse function does.', 'It reverses the function: it maps each output back to the input that produced it.', 'B1 B1. [2]'),
])

CHAPTERS[9] = [t91, t92, t93]


# =========================================================== 10 Graphs
t101 = topic('Functions and their linear graphs', 'functions and their linear graphs', 'linear graphs')


@t101.add('C3', (1, 2, 3, 4, 5))
def t101_table(r, D):
    m = r.choice([1, 2, 3, -1, -2, 0.5, 4]) if D >= 2 else r.choice([1, 2, 3])
    c = r.randint(-5, 6)
    xs = [-2, -1, 0, 1, 2, 3]
    ys = [m * x + c for x in xs]
    e = f'y = {poly((m, "x"), (c, ""))}'
    return Q(r.choice([f'Complete the table of values for {e} for x = −2, −1, 0, 1, 2, 3.', f'Work out the values of y for the graph of {e} when x = −2, −1, 0, 1, 2 and 3.']),
             ', '.join(N(y) for y in ys), f'Substitute each x (M1); y = {", ".join(N(y) for y in ys)} (A1).')


@t101.add('C1', (1, 2, 3))
def t101_point(r, D):
    m, c = r.choice([1, 2, 3, -1, -2, 4]), r.randint(-6, 6)
    x = r.randint(-4, 5)
    ans = f'({N(x)}, {N(m * x + c)})'
    return MCQ(r, f'Which point lies on the line y = {poly((m, "x"), (c, ""))}?', ans, [f'({N(m * x + c)}, {N(x)})' if m * x + c != x else f'({N(x)}, {N(m * x + c + 1)})', f'({N(x)}, {N(m * x - c)})' if c else f'({N(x)}, {N(m * x + 2)})', f'({N(x + 1)}, {N(m * x + c)})', f'({N(x)}, {N(m * (x + c))})' if c else f'({N(x)}, {N(m * x - 3)})'],
               f'When x = {N(x)}, y = {N(m * x + c)}. [1]')


@t101.add('C2', (1, 2, 3, 4), 'explain')
def t101_check(r, D):
    m, c = r.choice([2, 3, -2, 4, 5]), r.randint(-6, 6)
    x = r.randint(-5, 8)
    y = m * x + c + r.choice([0, 0, 1, -1, 2])
    p = person(r)
    on = y == m * x + c
    return Q(f'{p} says the point ({N(x)}, {N(y)}) lies on the line y = {poly((m, "x"), (c, ""))}. Show how to check whether {p} is right.',
             f'Substitute x = {N(x)}: y = {m} × {par(x)} {"+" if c >= 0 else "−"} {abs(c)} = {N(m * x + c)}. This {"equals" if on else "is not"} {N(y)}, so the point {"does" if on else "does not"} lie on the line.',
             'M1 substitution; A1 conclusion. [2]')


@t101.add('C2', (2, 3, 4), 'explain')
def t101_horiz(r, D):
    k = r.randint(-6, 8)
    p = person(r)
    if r.random() < 0.5:
        return Q(f'{p} says the line y = {N(k)} is vertical. Explain why {p} is wrong.', f'Every point on y = {N(k)} has the same y-coordinate, e.g. (0, {N(k)}), (5, {N(k)}); the line is horizontal.', 'B1 y constant; B1 horizontal. [2]')
    return Q(f'Explain why the graph of x = {N(k)} cannot be written in the form y = mx + c.', f'x = {N(k)} is a vertical line: x stays the same while y changes, so y is not a function of x; its gradient is undefined.', 'B1 vertical; B1 gradient undefined / not a function of x. [2]')


@t101.add('C1', (1, 2, 3))
def t101_rule(r, D):
    m, c = r.choice([2, 3, 4, -1, -2]), r.randint(-5, 6)
    xs = [0, 1, 2, 3]
    pts = ', '.join(f'({x}, {N(m * x + c)})' for x in xs)
    ans = f'y = {poly((m, "x"), (c, ""))}'
    return MCQ(r, f'The points {pts} lie on a straight line. What is its equation?', ans, [f'y = {poly((c, "x"), (m, ""))}' if c else f'y = {m + 1}x', f'y = {poly((m, "x"), (-c, ""))}' if c else f'y = x + {m}', f'y = {poly((1, "x"), (c, ""))}' if m != 1 else 'y = 2x', f'y = {poly((-m, "x"), (c, ""))}'],
               f'y increases by {N(m)} for each 1 in x; when x = 0, y = {N(c)}. [1]')


def _lin_c4(r, D):
    a = r.choice([20, 25, 30, 40, 50])
    b = r.choice([2, 3, 4, 5, 8])
    intro = f'A plumber in {city(r)} charges a call-out fee of ${a} plus ${b} per minute. The charge is C dollars for t minutes.'
    tt = r.choice([15, 30, 45, 60])
    budget = a + b * r.choice([20, 35, 50])
    parts = [
        lambda r: ('Write a formula for C in terms of t.', f'C = {a} + {b}t', 'B1 [1]'),
        lambda r: (f'Work out the values of C for t = 0, 10, 20 and 30.', f'{a}, {a + 10 * b}, {a + 20 * b}, {a + 30 * b}', 'B1 [1]'),
        lambda r: ('Describe what the graph of C against t looks like, including its gradient and where it crosses the C-axis.', f'A straight line with gradient {b} crossing the C-axis at {a}.', 'B1 gradient; B1 intercept [2]'),
        lambda r: (f'A customer pays ${budget}. How long did the job take?', f'{(budget - a) // b} minutes', 'M1; A1 [2]'),
        lambda r: (f'Work out the charge for a {tt}-minute job.', money(a + b * tt), 'B1 [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t101.add('C4', (2, 3, 4, 5), 'multi_step')(_lin_c4)
t101.fixed('C1', (1, 2), [
    ('What shape is the graph of y = 3x − 2?', 'A straight line', 'Linear function. [1]', ['A curve', 'A circle', 'A U shape']),
    ('Where does the line y = 5x + 4 cross the y-axis?', '(0, 4)', 'When x = 0, y = 4. [1]', ['(4, 0)', '(0, 5)', '(5, 4)']),
    ('Write down the equation of the x-axis.', 'y = 0', 'B1 [1]'),
])
t101.fixed('C2', (2, 3), [
    ('Explain why you only need two points to draw a straight-line graph, but it is sensible to plot three.', 'Two points fix a straight line; a third point acts as a check for mistakes.', 'B1 B1. [2]'),
])


# ----------------------------------------------------------- plotting graphs, non-linear
t102 = topic('Plotting linear and simple non-linear graphs', 'plotting graphs of linear and simple non-linear functions', 'non-linear graphs', 'quadratic graphs')


@t102.add('C3', (1, 2, 3, 4, 5))
def t102_quad_table(r, D):
    a = 1 if D <= 3 else r.choice([1, 2, -1])
    b = r.choice([0, 0, -2, 2, -4]) if D >= 3 else 0
    c = r.randint(-6, 5)
    xs = [-3, -2, -1, 0, 1, 2, 3]
    f = lambda x: a * x * x + b * x + c
    e = f'y = {poly((a, "x²"), (b, "x"), (c, ""))}'
    return Q(f'Complete the table of values for {e} for x = −3, −2, −1, 0, 1, 2, 3.', ', '.join(N(f(x)) for x in xs),
             f'Square first, e.g. x = −3: {a if a != 1 else ""}(−3)² = {a * 9} (M1); y values {", ".join(N(f(x)) for x in xs)} (A1).')


@t102.add('C1', (1, 2, 3))
def t102_shape(r, D):
    eqs_ = [('y = x² + 3', 'A U-shaped curve (parabola)'), ('y = 4 − x²', 'An upside-down U-shaped curve'), ('y = 2x + 1', 'A straight line'), ('y = 6/x', 'Two separate curves (a reciprocal graph)'), ('y = x³', 'An S-shaped curve (cubic)')]
    e, ans = r.choice(eqs_)
    return MCQ(r, f'Which description matches the graph of {e}?', ans, [a for _, a in eqs_ if a != ans], f'{e}: {ans.lower()}. [1]')


@t102.add('C1', (1, 2, 3))
def t102_val(r, D):
    c = r.randint(-6, 6)
    x = r.choice([-4, -3, -2, 2, 3, 4])
    v = x * x + c
    return MCQ(r, f'The graph of y = x² {"+" if c >= 0 else "−"} {abs(c)} is drawn. What is the value of y when x = {N(x)}?', N(v), [N(-x * x + c), N(2 * x + c), N(x + c), N(v + 1)], f'({N(x)})² {"+" if c >= 0 else "−"} {abs(c)} = {N(v)}. [1]')


@t102.add('C2', (1, 2, 3, 4), 'explain')
def t102_sym(r, D):
    c = r.randint(-5, 6)
    p = person(r)
    if r.random() < 0.5:
        return Q(f'Explain why the graph of y = x² {"+" if c >= 0 else "−"} {abs(c)} is symmetrical about the y-axis.', f'x and −x give the same value of x², e.g. (−3)² = 3² = 9, so the points (x, y) and (−x, y) are both on the graph.', 'B1 (−x)² = x²; B1 reflected points. [2]')
    x = r.randint(2, 4)
    return Q(f'{p} works out y for y = x² {"+" if c >= 0 else "−"} {abs(c)} when x = −{x} and gets {N(-x * x + c)}. Explain the mistake.',
             f'(−{x})² = {x * x}, not −{x * x}; squaring a negative number gives a positive. y = {N(x * x + c)}.', 'B1 squaring a negative; B1 correct value. [2]')


@t102.add('C2', (2, 3, 4), 'explain')
def t102_linnon(r, D):
    xs = [0, 1, 2, 3, 4]
    if r.random() < 0.5:
        c = r.randint(1, 6)
        ys = [x * x + c for x in xs]
        return Q(f'A table of values has x = 0, 1, 2, 3, 4 and y = {", ".join(map(str, ys))}. Explain how you know the graph is not a straight line.',
                 f'The y values increase by {", ".join(str(ys[i + 1] - ys[i]) for i in range(4))}: the differences are not equal, so the graph is a curve.', 'B1 differences; B1 not constant so non-linear. [2]')
    m, c = r.randint(2, 5), r.randint(-3, 6)
    ys = [m * x + c for x in xs]
    return Q(f'A table of values has x = 0, 1, 2, 3, 4 and y = {", ".join(N(y) for y in ys)}. Explain how you know the points lie on a straight line, and give its equation.',
             f'y increases by {m} each time x increases by 1 (constant difference), so it is linear: y = {poly((m, "x"), (c, ""))}.', 'B1 constant difference; B1 equation. [2]')


def _plot_c4(r, D):
    c = r.randint(-9, -1)
    xs = [-3, -2, -1, 0, 1, 2, 3]
    ys = [x * x + c for x in xs]
    root = math.sqrt(-c)
    intro = f'This question is about the graph of y = x² − {abs(c)} for values of x from −3 to 3.'
    parts = [
        lambda r: ('Complete a table of values for x = −3, −2, −1, 0, 1, 2, 3.', ', '.join(N(y) for y in ys), 'B2 all correct, B1 at least 5 [2]'),
        lambda r: ('Write down the coordinates of the lowest point of the graph.', f'(0, {N(c)})', 'B1 [1]'),
        lambda r: ('Write down the equation of the line of symmetry.', 'x = 0', 'B1 [1]'),
        lambda r: ('Estimate, to 1 decimal place, the values of x where the graph crosses the x-axis.', f'x = {fdp(root, 1)} and x = −{fdp(root, 1)}', f'M1 x² = {abs(c)}; A1 ±{fdp(root, 1)} [2]'),
        lambda r: (f'The line y = 2x is drawn on the same axes. Find, by trial or by solving, the positive x-coordinate where it meets the curve, to 1 decimal place.', f'x = {fdp(1 + math.sqrt(1 - c), 1)}', 'M1 x² − 2x − ' + str(abs(c)) + ' = 0 / trials; A1 [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t102.add('C4', (2, 3, 4, 5), 'multi_step')(_plot_c4)
t102.fixed('C1', (1, 2), [
    ('What is the name of the curve given by y = x²?', 'A parabola', 'B1 [1]', ['A hyperbola', 'A straight line', 'A circle']),
    ('Which of these graphs passes through the origin? y = x² + 1, y = 3x, y = x − 2, y = 5', 'y = 3x', 'When x = 0, y = 0. [1]', ['y = x² + 1', 'y = x − 2', 'y = 5']),
    ('Write down the coordinates of the lowest point of the graph of y = x² + 4.', '(0, 4)', 'B1 [1]'),
])
t102.fixed('C2', (2, 3), [
    ('Explain why you should join the points of a quadratic graph with a smooth curve, not straight lines.', 'The function has values between the plotted points which follow a curve, not straight segments.', 'B1 B1. [2]'),
])


# ----------------------------------------------------------- gradient and intercept
t103 = topic('Gradient and intercept: y = mx + c', 'gradient and intercept', 'y = mx + c', 'gradient')


@t103.add('C1', (1, 2, 3))
def t103_read(r, D):
    m, c = r.choice([2, 3, -2, -1, 0.5, 4, -3]), r.randint(-7, 7)
    which = r.choice(['gradient', 'y-intercept'])
    form = f'y = {poly((m, "x"), (c, ""))}'
    if D >= 3:
        k = r.choice([2, 3])
        form = f'{k}y = {poly((k * m, "x"), (k * c, ""))}'
    ans = N(m) if which == 'gradient' else N(c)
    return MCQ(r, f'What is the {which} of the line {form}?', ans, [N(c) if which == 'gradient' else N(m), N(-m) if which == 'gradient' else N(-c), N(m * 2), N(c + m)],
               f'Write as y = mx + c: gradient {N(m)}, y-intercept {N(c)}. [1]')


@t103.add('C3', (1, 2, 3, 4, 5))
def t103_two(r, D):
    m = r.choice([1, 2, 3, -1, -2, 4, Fr(1, 2), Fr(-3, 2)] if D >= 3 else [1, 2, 3, 4])
    m = Fr(m)
    x1 = r.randint(-4, 3)
    x2 = x1 + (m.denominator * r.randint(1, 3))
    c = r.randint(-6, 6)
    y1, y2 = m * x1 + c, m * x2 + c
    if D <= 2:
        return Q(f'Work out the gradient of the line through ({N(x1)}, {fr(y1)}) and ({N(x2)}, {fr(y2)}).', fr(m),
                 f'Gradient = ({fr(y2)} − {par(float(y1)) if y1.denominator == 1 else fr(y1)}) ÷ ({N(x2)} − {par(x1)}) (M1) = {fr(m)} (A1).')
    return Q(f'Find the equation of the straight line through ({N(x1)}, {fr(y1)}) and ({N(x2)}, {fr(y2)}). Give your answer in the form y = mx + c.',
             f'y = {poly((m, "x"), (c, ""))}', f'Gradient = {fr(y2 - y1)}/{x2 - x1} = {fr(m)} (M1, A1); substitute a point to find c = {N(c)} (M1); y = {poly((m, "x"), (c, ""))} (A1).', marks=4)


@t103.add('C3', (2, 3, 4, 5))
def t103_par(r, D):
    m, c = r.choice([2, 3, -2, -1, 4, 5]), r.randint(-6, 6)
    x, y = r.randint(-3, 5), r.randint(-5, 9)
    c2 = y - m * x
    return Q(f'Find the equation of the line parallel to y = {poly((m, "x"), (c, ""))} that passes through ({N(x)}, {N(y)}).', f'y = {poly((m, "x"), (c2, ""))}',
             f'Parallel lines have the same gradient, {N(m)} (B1); {N(y)} = {N(m)} × {par(x)} + c (M1); c = {N(c2)}, y = {poly((m, "x"), (c2, ""))} (A1).', marks=3)


@t103.add('C2', (1, 2, 3, 4), 'explain')
def t103_err(r, D):
    a, b, k = r.choice([2, 3, 4, 6]), r.randint(-9, 9), r.choice([2, 3])
    p = person(r)
    if r.random() < 0.5:
        return Q(f'{p} says the gradient of {k}y = {poly((k * a, "x"), (k * b, ""))} is {k * a}. Explain the mistake and give the correct gradient.',
                 f'The equation must be written as y = …: divide by {k} to get y = {poly((a, "x"), (b, ""))}, so the gradient is {a}.', 'B1 rearrange to y = mx + c; B1 gradient. [2]')
    x1, x2 = r.randint(0, 3), r.randint(5, 9)
    y1, y2 = a * x1 + b, a * x2 + b
    return Q(f'{p} works out the gradient of the line through ({x1}, {N(y1)}) and ({x2}, {N(y2)}) as ({x2} − {x1}) ÷ ({N(y2)} − {par(y1)}) = {fr(Fr(x2 - x1, y2 - y1))}. Explain the mistake and give the correct gradient.',
             f'Gradient is change in y ÷ change in x, not the other way round: ({N(y2)} − {par(y1)}) ÷ ({x2} − {x1}) = {a}.', 'B1 rise over run; B1 correct gradient. [2]')


@t103.add('C2', (2, 3, 4), 'explain')
def t103_meaning(r, D):
    m, c = r.choice([(2.5, 10), (0.8, 3), (1.2, 25), (15, 40), (0.05, 2)])
    ctx, xu, yu = r.choice([('the cost, y dollars, of a taxi journey of x km', 'km', 'dollars'), ('the height, y cm, of a plant after x weeks', 'week', 'cm'), ('the total cost, y dollars, of printing x posters', 'poster', 'dollars')])
    return Q(f'The graph of y = {N(m)}x + {N(c)} shows {ctx}. Explain what the gradient and the y-intercept represent.',
             f'Gradient {N(m)}: the increase in y ({yu}) for each extra {xu}. Intercept {N(c)}: the value of y when x = 0 (the starting amount / fixed charge).', 'B1 gradient as rate; B1 intercept as starting value. [2]')


def _grad_c4(r, D):
    m1, c1 = r.choice([2, 3, -1, 1]), r.randint(-4, 5)
    m2 = r.choice([v for v in (-2, -1, 1, 3, 4) if v != m1])
    x = r.randint(-3, 4)
    y = m1 * x + c1
    c2 = y - m2 * x
    intro = f'Line L₁ has equation y = {poly((m1, "x"), (c1, ""))}. Line L₂ passes through (0, {N(c2)}) and ({N(x)}, {N(y)}).'
    parts = [
        lambda r: ('Write down the gradient of L₁.', N(m1), 'B1 [1]'),
        lambda r: ('Find the equation of L₂.', f'y = {poly((m2, "x"), (c2, ""))}', 'M1 gradient; A1 [2]'),
        lambda r: ('Write down the coordinates of the point where L₁ and L₂ meet.', f'({N(x)}, {N(y)})', 'B1 [1]'),
        lambda r: ('Write down the equation of the line parallel to L₁ that passes through the origin.', f'y = {poly((m1, "x"))}', 'B1 [1]'),
        lambda r: (f'Explain whether the point ({N(x + 2)}, {N(m1 * (x + 2) + c1)}) lies on L₂.', f'{"Yes" if m2 * (x + 2) + c2 == m1 * (x + 2) + c1 else "No"}: on L₂, x = {N(x + 2)} gives y = {N(m2 * (x + 2) + c2)}', 'M1 substitution; A1 [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t103.add('C4', (2, 3, 4, 5), 'multi_step')(_grad_c4)
t103.fixed('C1', (1, 2), [
    ('What is the gradient of a horizontal line?', '0', 'No change in y. [1]', ['1', 'Undefined', '−1']),
    ('Which line is parallel to y = 3x + 1? y = 3x − 4, y = x + 3, y = −3x + 1, y = 1/3 x', 'y = 3x − 4', 'Same gradient, 3. [1]', ['y = x + 3', 'y = −3x + 1', 'y = 1/3 x']),
    ('Write down the equation of the line with gradient 5 and y-intercept −2.', 'y = 5x − 2', 'B1 [1]'),
])
t103.fixed('C2', (2, 3), [
    ('Explain what a negative gradient tells you about a straight-line graph.', 'The line slopes downwards from left to right: y decreases as x increases.', 'B1 B1. [2]'),
])


# ----------------------------------------------------------- real-life graphs
t104 = topic('Real-life graphs and distance-time graphs', 'interpreting real-life graphs', 'distance-time graphs')


def _journey(r):
    p = person(r)
    d1 = r.choice([6, 8, 10, 12, 15, 20])
    t1 = r.choice([20, 30, 40, 60])
    stop = r.choice([10, 15, 20, 30])
    d2 = r.choice([4, 6, 8, 10])
    t2 = r.choice([15, 20, 30])
    back = r.choice([30, 40, 45, 60])
    return p, d1, t1, stop, d2, t2, back


def _jdesc(p, d1, t1, stop, d2, t2, back, start='10:00'):
    return (f'{p} leaves home at {start}. A distance-time graph of the journey shows: a straight line from (0 min, 0 km) to ({t1} min, {d1} km); a horizontal line for {stop} minutes; '
            f'a straight line to {d1 + d2} km over the next {t2} minutes; then a straight line back to home taking {back} minutes.')


@t104.add('C3', (1, 2, 3, 4, 5))
def t104_speed(r, D):
    p, d1, t1, stop, d2, t2, back = _journey(r)
    seg = r.choice(['first', 'third', 'back'])
    if seg == 'first':
        v = d1 / (t1 / 60)
        q = 'Calculate the speed, in km/h, for the first part of the journey.'
        key = f'{d1} km in {t1} min = {N(t1 / 60)} h (M1); {d1} ÷ {N(t1 / 60)} = {N(round(v, 2))} km/h (A1).'
    elif seg == 'third':
        v = d2 / (t2 / 60)
        q = 'Calculate the speed, in km/h, for the third part of the journey.'
        key = f'{d2} km in {t2} min (M1); {N(round(v, 2))} km/h (A1).'
    else:
        v = (d1 + d2) / (back / 60)
        q = 'Calculate the speed, in km/h, on the way back home.'
        key = f'{d1 + d2} km in {back} min (M1); {N(round(v, 2))} km/h (A1).'
    return Q(_jdesc(p, d1, t1, stop, d2, t2, back) + ' ' + q, f'{N(round(v, 2))} km/h', key)


@t104.add('C1', (1, 2, 3))
def t104_flat(r, D):
    what = r.choice([('horizontal line', 'The object is not moving (stationary)'), ('straight line sloping upwards', 'Moving away at a constant speed'),
                     ('steeper straight line', 'Moving at a greater constant speed'), ('straight line sloping down to the time axis', 'Returning to the start at a constant speed')])
    others = ['The object is not moving (stationary)', 'Moving away at a constant speed', 'Moving at a greater constant speed', 'Returning to the start at a constant speed', 'Speeding up']
    obj = r.choice(['a cyclist', 'a bus', 'a runner', 'a delivery van', 'a train'])
    return MCQ(r, f'On a distance-time graph for {obj}, what does a {what[0]} show?', what[1], [o for o in others if o != what[1]], f'{what[1]}. [1]')


@t104.add('C2', (1, 2, 3, 4), 'explain')
def t104_compare(r, D):
    p, d1, t1, stop, d2, t2, back = _journey(r)
    v1, v3 = d1 / t1, d2 / t2
    return Q(_jdesc(p, d1, t1, stop, d2, t2, back) + ' Was the first part or the third part of the journey faster? Explain how you can tell from the graph.',
             f'{"First" if v1 > v3 else "Third" if v3 > v1 else "Both the same"}: the steeper line shows the greater speed ({N(round(60 * v1, 2))} km/h compared with {N(round(60 * v3, 2))} km/h).',
             'B1 steeper = faster (gradient = speed); B1 correct part with values. [2]')


@t104.add('C2', (2, 3, 4), 'explain')
def t104_err(r, D):
    p = person(r)
    k = r.choice([15, 20, 30])
    return Q(f'{p} says that a horizontal section lasting {k} minutes on a distance-time graph shows the car travelling at a steady speed. Explain why {p} is wrong.',
             'A horizontal line means the distance from the start is not changing, so the car is stationary for that time.', 'B1 distance constant; B1 stationary. [2]')


@t104.add('C3', (2, 3, 4, 5))
def t104_conv(r, D):
    rate = r.choice([(1.1, 'euros', 'dollars'), (0.8, 'pounds', 'dollars'), (3.67, 'dirhams', 'dollars'), (1.35, 'Singapore dollars', 'US dollars')])
    k, a, b = rate
    x = r.choice([20, 40, 50, 80, 150])
    return Q(f'A conversion graph is a straight line through (0, 0) and (100, {N(round(100 * k, 2))}), with {b} on the horizontal axis and {a} on the vertical axis. (a) Use the graph to convert {x} {b} to {a}. (b) Convert {N(round(k * x * 2, 2))} {a} to {b}. (c) Explain why the graph passes through the origin.',
             f'(a) {N(round(k * x, 2))} {a} (b) {2 * x} {b} (c) 0 {b} is worth 0 {a}.', f'(a) M1 gradient {N(k)}; A1 [2] (b) M1 ÷ {N(k)}; A1 [2] (c) B1 [1]', marks=5)


def _dt_c4(r, D):
    p, d1, t1, stop, d2, t2, back = _journey(r)
    intro = _jdesc(p, d1, t1, stop, d2, t2, back, start='09:00')
    total = t1 + stop + t2 + back
    hh, mm = divmod(9 * 60 + total, 60)
    parts = [
        lambda r: ('How far from home was ' + p + ' at the furthest point?', f'{d1 + d2} km', 'B1 [1]'),
        lambda r: (f'At what time did {p} get home?', f'{hh:02d}:{mm:02d}', f'M1 total {total} minutes; A1 [2]'),
        lambda r: ('Calculate the average speed for the whole journey, in km/h, including the stop.', f'{N(round(2 * (d1 + d2) / (total / 60), 2))} km/h', f'M1 {2 * (d1 + d2)} km ÷ {N(round(total / 60, 4))} h; A1 [2]'),
        lambda r: ('Describe what happened during the second part of the journey.', f'{p} stopped (stationary) for {stop} minutes.', 'B1 [1]'),
        lambda r: ('On which part of the journey was the speed greatest? Give a reason.', ['first', 'third', 'return'][max(range(3), key=lambda i: [d1 / t1, d2 / t2, (d1 + d2) / back][i])] + ' part: the steepest line', 'M1 compares speeds; A1 [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t104.add('C4', (2, 3, 4, 5), 'multi_step')(_dt_c4)
t104.fixed('C1', (1, 2), [
    ('On a distance-time graph, what does the gradient of a line represent?', 'Speed', 'Gradient = distance ÷ time = speed. [1]', ['Distance', 'Time', 'Acceleration']),
    ('A car travels 150 km in 2 hours. What is its average speed?', '75 km/h', '150 ÷ 2. [1]', ['300 km/h', '152 km/h', '1.33 km/h']),
    ('Write down the formula linking speed, distance and time.', 'speed = distance ÷ time', 'B1 [1]'),
])
t104.fixed('C2', (2, 3), [
    ('Explain why a distance-time graph can never slope backwards (to the left).', 'Time always moves forward, so the graph cannot go back to an earlier time.', 'B1 B1. [2]'),
    ('Explain what a curved line on a distance-time graph shows.', 'The speed is changing: the gradient is changing, so the object is speeding up or slowing down.', 'B1 B1. [2]'),
])

CHAPTERS[10] = [t101, t102, t103, t104]


# =========================================================== 11 Ratio and proportion
t111 = topic('Using ratios and dividing in a ratio', 'using ratios', 'dividing a quantity in a given ratio', 'ratio')


def rat(*xs):
    return ' : '.join(N(x) for x in xs)


@t111.add('C1', (1, 2, 3))
def t111_simp(r, D):
    a, b = r.sample([1, 2, 3, 4, 5, 7], 2)
    k = r.randint(2, 12)
    if D >= 3:
        c = r.choice([v for v in (1, 2, 3, 5) if v not in (a, b)])
        g = math.gcd(math.gcd(a, b), c)
        a, b, c = a // g, b // g, c // g
        return MCQ(r, f'Write {rat(a * k, b * k, c * k)} in its simplest form.', rat(a, b, c), [rat(b, a, c), rat(a * 2, b * 2, c * 2) if k % 2 == 0 else rat(a + 1, b, c), rat(a, b, c + 1), rat(a * k, b * k, c)], f'Divide each part by {k}. [1]')
    g = math.gcd(a, b)
    a, b = a // g, b // g
    unit = r.choice([('cm', 'm', 100), ('g', 'kg', 1000), ('minutes', 'hours', 60)]) if D == 2 else None
    if unit:
        x = a * k
        y_big = Fr(b * k, unit[2])
        if y_big.denominator != 1 and y_big.denominator > 4:
            return MCQ(r, f'Write {rat(a * k, b * k)} in its simplest form.', rat(a, b), [rat(b, a), rat(a * k, b), rat(a + b, b), rat(a, a + b)], f'Divide both parts by {k}. [1]')
        return MCQ(r, f'Write the ratio {a * k * unit[2]} {unit[0]} : {N(Fr(b * k, 1))} {unit[1]} in its simplest form.', rat(Fr(a * k * unit[2], math.gcd(a * k * unit[2], b * k * unit[2])), Fr(b * k * unit[2], math.gcd(a * k * unit[2], b * k * unit[2]))),
                   [rat(a * k * unit[2], b * k), rat(a * k, b * k), rat(b, a), rat(a, b * unit[2])], f'Same units first: {b * k} {unit[1]} = {b * k * unit[2]} {unit[0]}; then simplify. [1]')
    return MCQ(r, f'Write {rat(a * k, b * k)} in its simplest form.', rat(a, b), [rat(b, a), rat(a * k, b), rat(a + b, b), rat(a, a + b)], f'Divide both parts by the HCF {k}. [1]')


@t111.add('C3', (1, 2, 3, 4, 5))
def t111_share(r, D):
    parts_ = r.choice([(2, 3), (3, 5), (1, 4), (4, 7), (2, 5), (5, 3)] if D <= 3 else [(2, 3, 5), (1, 2, 4), (3, 4, 5), (2, 5, 6)])
    k = r.randint(4, 30)
    tot = sum(parts_) * k
    names = r.sample(PEOPLE_, len(parts_))
    shares = [p * k for p in parts_]
    if D >= 4 and r.random() < 0.5:
        diff = shares[-1] - shares[0]
        return Q(f'{", ".join(names[:-1])} and {names[-1]} share some money in the ratio {rat(*parts_)}. {names[-1]} gets ${diff} more than {names[0]}. How much money is shared altogether?',
                 f'${tot}', f'Difference {parts_[-1] - parts_[0]} parts = ${diff} (M1); 1 part = ${k} (M1); total {sum(parts_)} parts = ${tot} (A1).', marks=3)
    return Q(r.choice([f'Share ${tot} between {", ".join(names[:-1])} and {names[-1]} in the ratio {rat(*parts_)}.', f'{", ".join(names[:-1])} and {names[-1]} share ${tot} in the ratio {rat(*parts_)}. How much does each person get?']),
             ', '.join(f'{n} ${s}' for n, s in zip(names, shares)), f'{sum(parts_)} parts (M1); 1 part = {tot} ÷ {sum(parts_)} = ${k} (M1); {", ".join("$" + str(s) for s in shares)} (A1).', marks=3 if D >= 2 else 2)


PEOPLE_ = ['Amara', 'Lucas', 'Sofia', 'Kenji', 'Zara', 'Mateo', 'Aisha', 'Noah', 'Leila', 'Priya', 'Omar', 'Mei']


@t111.add('C3', (2, 3, 4, 5))
def t111_known(r, D):
    a, b = r.choice([(2, 3), (3, 5), (4, 7), (5, 8), (3, 4), (2, 9)])
    k = r.randint(3, 25)
    thing = r.choice([('red beads', 'blue beads', ''), ('boys', 'girls', ''), ('kg of cement', 'kg of sand', ''), ('ml of juice', 'ml of water', '')])
    return Q(f'The ratio of {thing[0]} to {thing[1]} is {a} : {b}. There are {a * k} {thing[0]}. How many {thing[1]} are there, and what is the total?',
             f'{b * k} {thing[1]}; total {(a + b) * k}', f'1 part = {a * k} ÷ {a} = {k} (M1); {thing[1]} = {b} × {k} = {b * k} (A1); total {(a + b) * k} (A1).', marks=3)


@t111.add('C2', (1, 2, 3, 4), 'explain')
def t111_err(r, D):
    a, b = r.choice([(2, 3), (3, 5), (1, 4), (3, 7), (2, 5)])
    k = r.randint(5, 20)
    tot = (a + b) * k
    p = person(r)
    if r.random() < 0.5:
        return Q(f'{p} shares ${tot} in the ratio {a} : {b} and says the first share is {money(tot / a)}. Explain the mistake and find both shares.',
                 f'{p} divided by {a} instead of by the total number of parts ({a + b}). 1 part = {tot} ÷ {a + b} = ${k}; shares ${a * k} and ${b * k}.',
                 'B1 must divide by total parts; B1 correct shares. [2]')
    return Q(f'In a class the ratio of boys to girls is {a} : {b}. {p} says that {N(Fr(100 * a, b))}% of the class are boys. Explain the mistake and give the correct percentage.',
             f'{p} compared boys with girls, not with the whole class. Boys are {a} out of {a + b} parts = {N(round(100 * a / (a + b), 1))}%.', 'B1 fraction of total; B1 correct percentage. [2]')


@t111.add('C2', (2, 3, 4), 'explain')
def t111_compare(r, D):
    a1, b1 = r.choice([(2, 3), (3, 5), (1, 2)])
    a2, b2 = r.choice([(3, 4), (5, 8), (2, 5), (3, 7)])
    if Fr(a1, a1 + b1) == Fr(a2, a2 + b2):
        return None
    p, q = two_people(r)
    s1, s2 = Fr(a1, a1 + b1), Fr(a2, a2 + b2)
    return Q(f'{p} mixes paint in the ratio red : white = {a1} : {b1}. {q} mixes red : white = {a2} : {b2}. Whose paint is redder? Explain.',
             f'{p}: red is {fr(s1)} = {N(round(float(s1) * 100, 1))}% of the paint; {q}: {fr(s2)} = {N(round(float(s2) * 100, 1))}%. {p if s1 > s2 else q}\'s paint is redder.',
             'M1 compares fractions of red (common form); A1 conclusion. [2]')


def _ratio_c4(r, D):
    a, b, c = r.choice([(2, 3, 5), (1, 3, 4), (3, 4, 5), (2, 5, 3)])
    k = r.choice([4, 5, 6, 8, 10, 12])
    tot = (a + b + c) * k
    ns = r.sample(PEOPLE_, 3)
    intro = f'{ns[0]}, {ns[1]} and {ns[2]} share ${tot} in the ratio {rat(a, b, c)}.'
    parts = [
        lambda r: ('How much does each person get?', f'${a * k}, ${b * k}, ${c * k}', f'M1 {tot} ÷ {a + b + c}; A1 all three [2]'),
        lambda r: (f'What fraction of the money does {ns[1]} get?', fr(Fr(b, a + b + c)), 'B1 [1]'),
        lambda r: (f'{ns[2]} gives ${k} to {ns[0]}. Write the new ratio of their amounts in its simplest form.', rat(*(lambda x, y, z: (x // math.gcd(math.gcd(x, y), z), y // math.gcd(math.gcd(x, y), z), z // math.gcd(math.gcd(x, y), z)))((a + 1) * k, b * k, (c - 1) * k)), 'M1 new amounts; A1 simplified [2]'),
        lambda r: (f'What percentage of the total does {ns[0]} receive at first?', f'{N(round(100 * a / (a + b + c), 1))}%', 'B1 [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t111.add('C4', (2, 3, 4, 5), 'multi_step')(_ratio_c4)


@t111.add('C4', (3, 4, 5), 'multi_step')
def t111_change(r, D):
    a, b = r.choice([(3, 5), (2, 3), (4, 5), (5, 7)])
    k = r.randint(4, 12)
    add = r.randint(2, 8)
    na, nb = a * k, b * k + add
    g = math.gcd(na, nb)
    return Q(f'A club has boys and girls in the ratio {a} : {b}. There are {(a + b) * k} members. Then {add} more girls join. (a) How many boys and girls were there at first? (b) Write the new ratio of boys to girls in its simplest form.',
             f'(a) {a * k} boys, {b * k} girls (b) {rat(na // g, nb // g)}', f'(a) M1 {(a + b) * k} ÷ {a + b}; A1 [2] (b) M1 {na} : {nb}; A1 {rat(na // g, nb // g)} [2]', marks=4)


t111.fixed('C1', (1, 2), [
    ('Which ratio is equivalent to 4 : 6?', '10 : 15', 'Both simplify to 2 : 3. [1]', ['6 : 4', '8 : 10', '5 : 7']),
    ('In a bag, red : green = 1 : 3. What fraction of the counters are red?', '1/4', '1 out of 4 parts. [1]', ['1/3', '3/4', '1/2']),
    ('Write 2.5 : 4 as a ratio of whole numbers in its simplest form.', '5 : 8', '× 2 → 5 : 8. B1 [1]'),
])
t111.fixed('C2', (2, 3), [
    ('Explain why the ratio 3 : 2 is not the same as the ratio 2 : 3.', 'The order matters: 3 : 2 means the first quantity is larger; 2 : 3 means the second is larger.', 'B1 B1. [2]'),
])


# ----------------------------------------------------------- direct and inverse proportion
t112 = topic('Direct and inverse proportion', 'direct and inverse proportion', 'proportion')
DIRECT = [('{n} pens cost ${c}.', 'pens', 'cost', '$'), ('{n} litres of fuel cost ${c}.', 'litres', 'cost', '$'), ('A car uses {c} litres of fuel to travel {n} km.', 'km', 'fuel', ''),
          ('{n} metres of fabric cost ${c}.', 'metres', 'cost', '$'), ('A printer prints {c} pages in {n} minutes.', 'minutes', 'pages', '')]
INVERSE = [('{a} workers take {b} days to build a wall.', 'workers', 'days'), ('{a} pumps empty a tank in {b} hours.', 'pumps', 'hours'),
           ('A journey takes {b} hours at {a} km/h.', 'km/h', 'hours'), ('Food for a group lasts {b} days for {a} people.', 'people', 'days'), ('{a} machines complete an order in {b} hours.', 'machines', 'hours')]


@t112.add('C3', (1, 2, 3, 4, 5))
def t112_direct(r, D):
    txt, xu, yu, cur = r.choice(DIRECT)
    n = r.choice([4, 5, 6, 8, 12, 15])
    unit_c = r.choice([0.6, 0.75, 1.2, 1.5, 2.4, 3.5, 0.85]) if cur else r.choice([0.08, 0.06, 0.05])
    if not cur:
        if 'pages' in yu:
            unit_c = r.choice([12, 15, 18, 20])
        c = round(n * unit_c, 4)
    else:
        c = round(n * unit_c, 2)
    m = r.choice([3, 7, 9, 10, 18, 20, 25])
    val = unit_c * m
    stem = txt.format(n=n, c=d2(c) if cur else N(c)) + f' Work out the {yu} for {m} {xu}.' if 'fuel' not in yu else txt.format(n=n * 10, c=N(round(n * 10 * unit_c, 2))) + f' How much fuel is needed for {m * 10} km?'
    if 'fuel' in yu:
        val = unit_c * m * 10
        key = f'Fuel for 1 km = {N(round(n * 10 * unit_c, 2))} ÷ {n * 10} = {N(unit_c)} litres (M1); × {m * 10} = {N(round(val, 2))} litres (A1).'
        return Q(stem, f'{N(round(val, 2))} litres', key)
    ans = money(val) if cur else N(round(val, 2))
    return Q(stem, ans, f'Unitary method: 1 {xu[:-1] if xu.endswith("s") else xu} → {N(unit_c)} (M1); × {m} = {ans} (A1).')


@t112.add('C3', (1, 2, 3, 4, 5))
def t112_inverse(r, D):
    txt, xu, yu = r.choice(INVERSE)
    a = r.choice([2, 3, 4, 5, 6, 8, 10, 12, 60, 80])
    b = r.choice([3, 4, 5, 6, 8, 9, 10, 12, 15])
    if xu == 'km/h':
        a = r.choice([40, 50, 60, 80, 90, 100])
    k = a * b
    choices = [x for x in (2, 3, 4, 5, 6, 8, 10, 12, 15, 16, 20, 24, 30, 40, 45, 50, 60, 75, 80, 90, 100, 120) if k % x == 0 and x != a]
    if not choices:
        return None
    a2 = r.choice(choices)
    b2 = Fr(k, a2)
    return Q(txt.format(a=a, b=b) + (f' Time is inversely proportional to speed. How many hours would the journey take at {a2} km/h?' if xu == 'km/h' else f' Assuming all the {xu} work at the same rate, how many {yu} would it take with {a2} {xu}?'),
             f'{mixed(b2)} {yu}', f'{xu.capitalize()} × {yu} is constant: {a} × {b} = {k} (M1); {k} ÷ {a2} = {mixed(b2)} (A1).')


@t112.add('C1', (1, 2, 3))
def t112_which(r, D):
    items = [('The number of identical books and their total mass', 'Direct proportion'), ('The number of people sharing a pizza equally and the amount each gets', 'Inverse proportion'),
             ('The speed of a car and the time for a fixed journey', 'Inverse proportion'), ('The number of hours worked at a fixed hourly rate and the pay', 'Direct proportion'),
             ('A person\'s age and their height', 'Neither'), ('The number of taps filling a bath and the time to fill it', 'Inverse proportion'), ('The length of a side of a square and its perimeter', 'Direct proportion'),
             ('The side length of a square and its area', 'Neither')]
    e, ans = r.choice(items)
    return MCQ(r, f'Which type of relationship is this? "{e}"', ans, ['Direct proportion', 'Inverse proportion', 'Neither', 'Both direct and inverse'], f'{ans}. [1]')


@t112.add('C2', (1, 2, 3, 4), 'explain')
def t112_err(r, D):
    txt, xu, yu = r.choice(INVERSE)
    a, b = r.choice([(2, 12), (3, 8), (4, 6), (6, 10), (5, 12)])
    if xu == 'km/h':
        a, b = r.choice([(60, 3), (80, 2), (50, 4)])
    p = person(r)
    a2 = a * 2
    return Q(txt.format(a=a, b=b) + f' {p} says that with {a2} {xu} it would take {2 * b} {yu}. Explain why {p} is wrong and give the correct answer.',
             f'This is inverse proportion: doubling the {xu} halves the {yu}. It would take {N(Fr(b, 2))} {yu}.', 'B1 inverse proportion; B1 correct value. [2]')


@t112.add('C2', (2, 3, 4), 'explain')
def t112_test(r, D):
    xs = r.sample([2, 3, 4, 5, 6, 8, 10], 3)
    xs.sort()
    k = r.choice([3, 4, 12, 24, 60, 120])
    inverse = r.random() < 0.5
    ys = [Fr(k, x) if inverse else k * x for x in xs]
    return Q(f'A table shows x = {", ".join(map(str, xs))} and y = {", ".join(mixed(y) for y in ys)}. Is y directly proportional or inversely proportional to x? Explain how you know.',
             (f'Inverse: x × y = {k} each time.' if inverse else f'Direct: y ÷ x = {k} each time (and the graph would be a straight line through the origin).'), 'M1 tests product or quotient; A1 conclusion. [2]')


def _prop_c4(r, D):
    w = r.choice([4, 5, 6, 8])
    d = r.choice([12, 15, 18, 20, 24])
    rate = r.choice([80, 95, 120, 150])
    k = w * d
    w2 = r.choice([x for x in (3, 6, 8, 9, 10, 12, 15, 16, 20) if k % x == 0 and x != w] or [w * 2])
    intro = f'A building company estimates that {w} workers take {d} days to complete a job. Each worker is paid ${rate} per day.'
    parts = [
        lambda r: (f'How many days would {w2} workers take, working at the same rate?', f'{N(Fr(k, w2))} days', f'M1 {w} × {d} = {k} worker-days; A1 [2]'),
        lambda r: ('Work out the total wage bill for the job with ' + str(w) + ' workers.', money(k * rate), f'M1 {k} worker-days × {rate}; A1 [2]'),
        lambda r: (f'Explain why the total wage bill is the same with {w2} workers.', f'The number of worker-days ({k}) stays the same, so the total pay is the same.', 'B1 [1]'),
        lambda r: (f'The job must be finished in {d // 2} days. How many workers are needed?', str(math.ceil(k / (d // 2))), 'M1; A1 [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t112.add('C4', (2, 3, 4, 5), 'multi_step')(_prop_c4)


@t112.add('C4', (3, 4, 5), 'multi_step')
def t112_best(r, D):
    s1, p1 = r.choice([(250, 2.40), (300, 2.85), (400, 3.60), (500, 4.40)])
    s2, p2 = r.choice([(750, 6.30), (1000, 8.20), (600, 5.10), (1200, 9.90)])
    u1, u2 = p1 / s1 * 100, p2 / s2 * 100
    return Q(f'A small jar of coffee holds {s1} g and costs {money(p1)}. A large jar holds {s2} g and costs {money(p2)}. (a) Work out the cost per 100 g of each jar. (b) Which jar is better value? (c) How much would 2 kg of coffee cost at the better rate?',
             f'(a) Small {money(u1)}, large {money(u2)} per 100 g (to the nearest cent) (b) {"Small" if u1 < u2 else "Large"} (c) {money(min(u1, u2) * 20)}',
             '(a) M1 unit cost; A1 both [2] (b) B1 [1] (c) M1 × 20; A1 [2]', marks=5)


t112.fixed('C1', (1, 2), [
    ('If y is directly proportional to x and x is doubled, what happens to y?', 'y is doubled', 'y = kx. [1]', ['y is halved', 'y stays the same', 'y is squared']),
    ('If y is inversely proportional to x and x is doubled, what happens to y?', 'y is halved', 'xy = k. [1]', ['y is doubled', 'y stays the same', 'y is quartered']),
    ('5 kg of rice cost $8. Write down the cost of 10 kg.', '$16', 'B1 [1]'),
])
t112.fixed('C2', (2, 3), [
    ('Explain how a graph shows that two quantities are in direct proportion.', 'The graph is a straight line through the origin.', 'B1 straight line; B1 through origin. [2]'),
])


# ----------------------------------------------------------- compound measures
t113 = topic('Compound measures: speed, density and rates', 'compound measures', 'speed density and rates')


@t113.add('C3', (1, 2, 3, 4, 5))
def t113_speed(r, D):
    find = r.choice(['s', 'd', 't'])
    s = r.choice([30, 40, 45, 48, 60, 72, 80, 90, 12, 15])
    t = r.choice([0.5, 1.5, 2, 2.5, 3, 0.75, 1.25, 4])
    d = s * t
    p = person(r)
    tm = f'{int(t)} hour{"s" if int(t) > 1 else ""} {int(round((t % 1) * 60))} minutes' if t % 1 and t > 1 else (f'{int(round(t * 60))} minutes' if t < 1 else f'{N(t)} hours')
    if find == 's':
        return Q(f'{p} drives {N(d)} km in {tm}. Calculate the average speed in km/h.', f'{N(s)} km/h', f'Time = {N(t)} h (B1 if converted); speed = {N(d)} ÷ {N(t)} (M1) = {N(s)} km/h (A1).')
    if find == 'd':
        return Q(f'A train travels at an average speed of {s} km/h for {tm}. How far does it travel?', f'{N(d)} km', f'distance = speed × time (M1) = {s} × {N(t)} = {N(d)} km (A1).')
    return Q(f'A cyclist rides {N(d)} km at an average speed of {s} km/h. How long does the journey take? Give your answer in hours and minutes.', tm,
             f'time = {N(d)} ÷ {s} = {N(t)} h (M1); = {tm} (A1).')


@t113.add('C3', (2, 3, 4, 5))
def t113_density(r, D):
    mats = [('aluminium', 2.7), ('iron', 7.9), ('copper', 8.96), ('gold', 19.3), ('wood', 0.6), ('glass', 2.5), ('ice', 0.92)]
    m_, rho = r.choice(mats)
    V = r.choice([10, 20, 25, 40, 50, 80, 125, 200])
    mass = rho * V
    find = r.choice(['rho', 'm', 'V'])
    if find == 'rho':
        return Q(f'A block of {m_} has a volume of {V} cm³ and a mass of {N(round(mass, 2))} g. Calculate the density of {m_}.', f'{N(rho)} g/cm³', f'density = mass ÷ volume (M1) = {N(round(mass, 2))} ÷ {V} = {N(rho)} g/cm³ (A1).')
    if find == 'm':
        return Q(f'The density of {m_} is {N(rho)} g/cm³. Calculate the mass of a piece with volume {V} cm³.', f'{N(round(mass, 2))} g', f'mass = density × volume (M1) = {N(round(mass, 2))} g (A1).')
    return Q(f'The density of {m_} is {N(rho)} g/cm³. A piece has mass {N(round(mass, 2))} g. Calculate its volume.', f'{V} cm³', f'volume = mass ÷ density (M1) = {V} cm³ (A1).')


@t113.add('C3', (2, 3, 4, 5))
def t113_units(r, D):
    v = r.choice([36, 54, 72, 90, 108, 18, 126])
    if r.random() < 0.5:
        return Q(f'Convert a speed of {v} km/h to m/s.', f'{N(v / 3.6)} m/s', f'{v} km/h = {v * 1000} m per 3600 s (M1); {v * 1000} ÷ 3600 = {N(v / 3.6)} m/s (A1).')
    ms = v / 3.6
    return Q(f'A sprinter runs at {N(ms)} m/s. Convert this speed to km/h.', f'{v} km/h', f'× 3600 ÷ 1000 (M1); {v} km/h (A1).')


@t113.add('C1', (1, 2, 3))
def t113_formula(r, D):
    items = [('density', 'mass ÷ volume', ['volume ÷ mass', 'mass × volume', 'mass − volume']), ('average speed', 'total distance ÷ total time', ['total time ÷ total distance', 'distance × time', 'distance + time']),
             ('time', 'distance ÷ speed', ['speed ÷ distance', 'speed × distance', 'distance − speed']), ('rate of flow (litres per minute)', 'volume ÷ time', ['time ÷ volume', 'volume × time', 'volume + time']),
             ('population density', 'population ÷ area', ['area ÷ population', 'population × area', 'population − area'])]
    w, ans, ds = r.choice(items)
    return MCQ(r, f'Which of these calculates {w}?', ans.capitalize(), [d.capitalize() for d in ds], f'{w.capitalize()} = {ans}. [1]')


@t113.add('C2', (1, 2, 3, 4), 'explain')
def t113_avg(r, D):
    d = r.choice([30, 60, 90, 120])
    s1, s2 = r.choice([(30, 60), (40, 60), (20, 30), (60, 90)])
    t1, t2 = d / s1, d / s2
    avg = 2 * d / (t1 + t2)
    p = person(r)
    return Q(f'{p} drives {d} km at {s1} km/h and then another {d} km at {s2} km/h. {p} says the average speed for the whole journey is {(s1 + s2) // 2} km/h. Explain why {p} is wrong and find the correct average speed.',
             f'More time is spent at the slower speed, so you cannot average the speeds. Total time = {N(t1)} + {N(t2)} = {N(t1 + t2)} h; average = {2 * d} ÷ {N(t1 + t2)} = {N(round(avg, 2))} km/h.',
             'B1 explanation; B1 correct average using total distance ÷ total time. [2]')


@t113.add('C2', (2, 3, 4), 'explain')
def t113_float(r, D):
    m, V = r.choice([(450, 500), (600, 800), (1200, 1000), (900, 750), (300, 400)])
    rho = m / V
    return Q(f'An object has mass {m} g and volume {V} cm³. Water has density 1 g/cm³. Will the object float in water? Explain.',
             f'Density = {m} ÷ {V} = {N(round(rho, 3))} g/cm³, which is {"less" if rho < 1 else "more"} than 1, so it will {"float" if rho < 1 else "sink"}.', 'M1 density; A1 comparison with 1 g/cm³. [2]')


def _rate_c4(r, D):
    p = person(r)
    km = r.choice([180, 240, 300, 360])
    s1 = r.choice([60, 80, 90])
    stop = r.choice([15, 20, 30])
    eff = r.choice([12, 14, 15, 16])
    cost = r.choice([1.2, 1.35, 1.5, 1.8])
    t = km / s1 + stop / 60
    intro = f'{p} drives {km} km from {city(r)} to the coast at an average driving speed of {s1} km/h, with one stop of {stop} minutes. The car travels {eff} km per litre of fuel.'
    parts = [
        lambda r: ('Work out the total time for the journey, including the stop, in hours and minutes.', f'{int(t)} h {round((t % 1) * 60)} min', f'M1 {km} ÷ {s1}; A1 [2]'),
        lambda r: ('Work out the average speed for the whole journey including the stop, to 1 decimal place.', f'{fdp(km / t, 1)} km/h', 'M1 total distance ÷ total time; A1 [2]'),
        lambda r: (f'Fuel costs {money(cost)} per litre. Work out the cost of the fuel for the journey.', money(km / eff * cost), f'M1 {km} ÷ {eff} litres; A1 [2]'),
        lambda r: ('Work out the rate of fuel use in litres per hour of driving.', f'{N(round(s1 / eff, 2))} litres per hour', 'M1; A1 [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t113.add('C4', (2, 3, 4, 5), 'multi_step')(_rate_c4)


@t113.add('C4', (3, 4, 5), 'multi_step')
def t113_tank(r, D):
    l, w, h = r.choice([(2, 1.5, 1), (3, 2, 1.2), (4, 2.5, 1.5)])
    rate = r.choice([20, 25, 40, 50])
    V = l * w * h * 1000
    return Q(f'A water tank is a cuboid {N(l)} m long, {N(w)} m wide and {N(h)} m high. Water flows in at {rate} litres per minute. (a) Work out the capacity of the tank in litres. (b) How long does it take to fill the empty tank? Give your answer in hours and minutes. (c) Work out the rate of flow in m³ per hour.',
             f'(a) {N(V)} litres (b) {int(V / rate // 60)} h {round(V / rate % 60)} min (c) {N(rate * 60 / 1000)} m³/h',
             f'(a) M1 {N(l * w * h)} m³ × 1000; A1 [2] (b) M1 {N(V)} ÷ {rate} = {N(V / rate)} min; A1 [2] (c) B1 [1]', marks=5)


t113.fixed('C1', (1, 2), [
    ('What is the unit of density when mass is in grams and volume is in cm³?', 'g/cm³', 'B1 [1]', ['cm³/g', 'g cm³', 'g/cm²']),
    ('A car travels 90 km in 1.5 hours. What is its average speed?', '60 km/h', '90 ÷ 1.5. [1]', ['135 km/h', '45 km/h', '91.5 km/h']),
    ('A tap fills a 12 litre bucket in 3 minutes. Write down the rate of flow.', '4 litres per minute', 'B1 [1]'),
])
t113.fixed('C2', (2, 3), [
    ('Explain what is meant by a compound measure, giving an example.', 'A measure made from two different quantities, e.g. speed = distance ÷ time (km/h).', 'B1 B1. [2]'),
])

CHAPTERS[11] = [t111, t112, t113]


# =========================================================== 12 Probability
BAGS = [('red', 'blue', 'green'), ('yellow', 'white', 'black'), ('orange', 'purple', 'pink')]


t121 = topic('Mutually exclusive events', 'mutually exclusive events', 'sum of probabilities')


@t121.add('C1', (1, 2, 3))
def t121_comp(r, D):
    p = Fr(r.randint(1, 19), 20) if D > 1 else Fr(r.randint(1, 9), 10)
    ev = r.choice(['it will rain tomorrow', 'a bus is late', 'a team wins its next match', 'a seed germinates', 'a light bulb lasts a year'])
    style = r.choice(['dec', 'frac'])
    ps = N(float(p)) if style == 'dec' else fr(p)
    ans = N(float(1 - p)) if style == 'dec' else fr(1 - p)
    return MCQ(r, f'The probability that {ev} is {ps}. What is the probability that this does not happen?', ans, [ps, N(float(1 / p)) if style == 'dec' else fr(1 / p), N(round(float(p) * 2, 2)) if p < 0.5 else '0', '1'], f'1 − {ps} = {ans}. [1]')


@t121.add('C3', (1, 2, 3, 4, 5))
def t121_missing(r, D):
    cols = r.choice(BAGS) + ('white',)
    n = 4 if D >= 3 else 3
    vals = [Fr(r.randint(1, 4), 10) for _ in range(n - 1)]
    if sum(vals) >= 1:
        return None
    miss = 1 - sum(vals)
    names = list(cols[:n])
    shown = ', '.join(f'P({c}) = {N(float(v))}' for c, v in zip(names, vals))
    if D >= 4:
        x = r.choice([2, 3])
        a, b = vals[0], vals[1]
        rest = 1 - a - b
        if rest <= 0 or (rest * 10) % (x + 1):
            return None
        u = rest / (x + 1)
        return Q(f'A spinner can land on {names[0]}, {names[1]}, {names[2]} or {names[3] if n == 4 else "white"}. P({names[0]}) = {N(float(a))}, P({names[1]}) = {N(float(b))}. It is {x} times as likely to land on {names[2]} as on {names[3] if n == 4 else "white"}. Work out P({names[2]}).',
                 N(float(x * u)), f'Remaining probability 1 − {N(float(a))} − {N(float(b))} = {N(float(rest))} (M1); split in ratio {x} : 1 (M1); P({names[2]}) = {N(float(x * u))} (A1).', marks=3)
    return Q(f'A bag contains {", ".join(names[:-1])} and {names[-1]} counters only. {shown}. Work out P({names[-1]}).', N(float(miss)),
             f'Probabilities of mutually exclusive outcomes add to 1 (M1); 1 − {N(float(sum(vals)))} = {N(float(miss))} (A1).')


@t121.add('C3', (2, 3, 4, 5))
def t121_or(r, D):
    a, b, c = r.randint(2, 9), r.randint(2, 9), r.randint(2, 9)
    cols = r.choice(BAGS)
    tot = a + b + c
    return Q(f'A bag contains {a} {cols[0]}, {b} {cols[1]} and {c} {cols[2]} balls. One ball is taken at random. Work out the probability that it is {cols[0]} or {cols[2]}.',
             fr(Fr(a + c, tot)), f'Mutually exclusive: P({cols[0]}) + P({cols[2]}) = {a}/{tot} + {c}/{tot} (M1) = {fr(Fr(a + c, tot))} (A1).')


@t121.add('C2', (1, 2, 3, 4), 'explain')
def t121_me(r, D):
    pairs = [('getting an even number', 'getting a 3', True, 'a dice'), ('getting an even number', 'getting a number greater than 4', False, 'a dice'),
             ('picking a king', 'picking a heart', False, 'a pack of cards'), ('picking a red card', 'picking a club', True, 'a pack of cards'),
             ('getting a prime number', 'getting an even number', False, 'a dice'), ('getting a 1', 'getting a 6', True, 'a dice')]
    e1, e2, me, obj = r.choice(pairs)
    p = person(r)
    return Q(f'{p} uses {obj}. Are the events "{e1}" and "{e2}" mutually exclusive? Explain.',
             f'{"Yes" if me else "No"}: ' + ('they cannot both happen at the same time.' if me else 'there is an outcome that is in both events, so they can happen together.'),
             'B1 decision; B1 reason (shared outcome or none). [2]')


@t121.add('C2', (2, 3, 4), 'explain')
def t121_err(r, D):
    a, b = r.choice([(0.4, 0.7), (0.5, 0.6), (0.35, 0.8), (0.45, 0.65)])
    p = person(r)
    return Q(f'{p} says that for a spinner, P(red) = {N(a)} and P(not red) = {N(b)}. Explain why {p} must be wrong.',
             f'An event and its complement are mutually exclusive and cover all outcomes, so they must add to 1. {N(a)} + {N(b)} = {N(round(a + b, 2))}, not 1.', 'B1 must add to 1; B1 shows sum. [2]')


def _me_c4(r, D):
    cols = ['red', 'blue', 'green', 'yellow']
    ps = [0.3, 0.25, None, 0.15]
    r.shuffle(ps)
    k = ps.index(None)
    ps[k] = round(1 - sum(x for x in ps if x is not None), 2)
    n = r.choice([100, 200, 400, 500])
    intro = 'A spinner has four colours. The table gives probabilities: ' + ', '.join(f'P({c}) = {N(p) if i != k else "x"}' for i, (c, p) in enumerate(zip(cols, ps))) + '.'
    parts = [
        lambda r: ('Work out the value of x.', N(ps[k]), 'M1 sum = 1; A1 [2]'),
        lambda r: ('Work out the probability that the spinner lands on red or blue.', N(round(ps[0] + ps[1], 2)), 'M1 add; A1 [2]'),
        lambda r: ('Work out the probability that it does not land on yellow.', N(round(1 - ps[3], 2)), 'B1 [1]'),
        lambda r: (f'The spinner is spun {n} times. How many times would you expect it to land on green?', N(round(ps[2] * n, 2)), f'M1 {N(ps[2])} × {n}; A1 [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t121.add('C4', (2, 3, 4, 5), 'multi_step')(_me_c4)
t121.fixed('C1', (1, 2), [
    ('What do the probabilities of all the mutually exclusive outcomes of an experiment add up to?', '1', 'B1 [1]', ['0', '100', '0.5']),
    ('What does "mutually exclusive" mean?', 'The events cannot happen at the same time', 'B1 [1]', ['The events always happen together', 'The events are equally likely', 'One event causes the other']),
    ('P(A) = 0.2 and P(B) = 0.5, and A and B are mutually exclusive. Write down P(A or B).', '0.7', 'B1 [1]'),
])
t121.fixed('C2', (2, 3), [
    ('Explain why you cannot simply add P(even) and P(greater than 3) for one roll of a dice to find P(even or greater than 3).', 'The events are not mutually exclusive: 4 and 6 are in both, so they would be counted twice.', 'B1 not mutually exclusive; B1 double counting. [2]'),
])


# ----------------------------------------------------------- independent events
t122 = topic('Independent events and the multiplication rule', 'independent events', 'multiplication rule')


@t122.add('C3', (1, 2, 3, 4, 5))
def t122_mult(r, D):
    a = Fr(r.randint(1, 9), 10)
    b = Fr(r.randint(1, 9), 10)
    e1, e2 = r.choice([('a train is on time', 'it rains'), ('Team A wins', 'Team B wins'), ('a bus is late', 'a lift is out of order'), ('a seed grows', 'a second seed grows')])
    kind = r.choice(['both', 'neither', 'one'] if D >= 3 else ['both'])
    if kind == 'both':
        v = a * b
        q = 'both events happen'
        key = f'Independent: {N(float(a))} × {N(float(b))} (M1) = {N(float(v))} (A1).'
    elif kind == 'neither':
        v = (1 - a) * (1 - b)
        q = 'neither event happens'
        key = f'(1 − {N(float(a))}) × (1 − {N(float(b))}) = {N(float(1 - a))} × {N(float(1 - b))} (M1) = {N(float(v))} (A1).'
    else:
        v = a * (1 - b) + (1 - a) * b
        q = 'exactly one of the events happens'
        key = f'{N(float(a))} × {N(float(1 - b))} + {N(float(1 - a))} × {N(float(b))} (M1, M1) = {N(float(v))} (A1).'
    return Q(f'The probability that {e1} is {N(float(a))}. The probability that {e2} is {N(float(b))}. The events are independent. Work out the probability that {q}.', N(float(v)), key)


@t122.add('C1', (1, 2, 3))
def t122_coins(r, D):
    n = r.choice([2, 3]) if D > 1 else 2
    obj = r.choice(['coin', 'dice'])
    if obj == 'coin':
        ans = f'1/{2 ** n}'
        return MCQ(r, f'A fair coin is thrown {n} times. What is the probability of getting heads every time?', ans, [f'1/{2 * n}' if n != 2 else '1/3', f'1/{n}', '1/8' if n == 2 else '1/6', f'1/{2 ** n + 1}'], f'(1/2){sup(n)} = {ans}. [1]')
    k = r.randint(1, 6)
    return MCQ(r, f'A fair dice is rolled twice. What is the probability of getting {k} both times?', '1/36', ['1/12', '1/6', '2/6', '1/18'], '1/6 × 1/6 = 1/36. [1]')


@t122.add('C2', (1, 2, 3, 4), 'explain')
def t122_indep(r, D):
    items = [('rolling a 6 on a dice', 'getting heads on a coin', True), ('it is cloudy', 'it rains on the same day', False), ('taking a red sweet from a bag and eating it', 'taking a red sweet from the same bag next', False),
             ('a student is good at maths', 'the same student is good at physics', False), ('spinning a 2 on a spinner', 'spinning a 2 on the next spin', True)]
    e1, e2, ind = r.choice(items)
    return Q(f'Are the events "{e1}" and "{e2}" independent? Explain.', ('Yes: the outcome of one does not affect the probability of the other.' if ind else 'No: the first event changes the probability of the second.'),
             'B1 decision; B1 reason. [2]')


@t122.add('C2', (2, 3, 4), 'explain')
def t122_err(r, D):
    p = person(r)
    n = r.randint(4, 8)
    return Q(f'A fair coin lands on heads {n} times in a row. {p} says the next throw is more likely to be tails because "tails is due". Explain why {p} is wrong.',
             'The throws are independent; the coin has no memory. P(tails) on the next throw is still 1/2.', 'B1 independence; B1 probability still 1/2. [2]')


@t122.add('C2', (2, 3, 4), 'explain')
def t122_add(r, D):
    a, b = r.choice([(0.6, 0.7), (0.5, 0.8), (0.4, 0.9), (0.75, 0.6)])
    p = person(r)
    return Q(f'P(A) = {N(a)} and P(B) = {N(b)} for two independent events. {p} says P(A and B) = {N(a)} + {N(b)} = {N(round(a + b, 2))}. Explain why this must be wrong and give the correct value.',
             f'A probability cannot be more than 1. For independent events multiply: {N(a)} × {N(b)} = {N(round(a * b, 4))}.', 'B1 reason; B1 correct value. [2]')


def _ind_c4(r, D):
    a = r.choice([0.6, 0.7, 0.8, 0.75, 0.9])
    b = r.choice([0.5, 0.6, 0.65, 0.4])
    p = person(r)
    intro = f'{p} takes a bus and then a train to school. The probability the bus is on time is {N(a)}. The probability the train is on time is {N(b)}. The events are independent.'
    parts = [
        lambda r: ('Work out the probability that both are on time.', N(round(a * b, 4)), 'M1; A1 [2]'),
        lambda r: ('Work out the probability that both are late.', N(round((1 - a) * (1 - b), 4)), 'M1; A1 [2]'),
        lambda r: ('Work out the probability that at least one of them is late.', N(round(1 - a * b, 4)), 'M1 1 − P(both on time); A1 [2]'),
        lambda r: (f'There are 190 school days. On how many days would you expect both to be on time?', N(round(a * b * 190, 2)), 'M1; A1 [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t122.add('C4', (2, 3, 4, 5), 'multi_step')(_ind_c4)
t122.fixed('C1', (1, 2), [
    ('For independent events A and B, which rule gives P(A and B)?', 'P(A) × P(B)', 'Multiplication rule. [1]', ['P(A) + P(B)', 'P(A) − P(B)', 'P(A) ÷ P(B)']),
    ('A coin is thrown and a dice is rolled. What is P(heads and a 6)?', '1/12', '1/2 × 1/6. [1]', ['2/3', '1/8', '7/12']),
    ('Write down what is meant by independent events.', 'The outcome of one does not affect the probability of the other.', 'B1 [1]'),
])


# ----------------------------------------------------------- sample spaces and tree diagrams
t123 = topic('Sample spaces and tree diagrams', 'combined events', 'sample spaces', 'tree diagrams')


@t123.add('C3', (1, 2, 3, 4, 5))
def t123_dice(r, D):
    s1, s2 = r.choice([(6, 6), (4, 6), (6, 8), (4, 4), (5, 5)])
    kind = r.choice(['sum', 'diff', 'prod'])
    target = None
    outs = [(a, b) for a in range(1, s1 + 1) for b in range(1, s2 + 1)]
    if kind == 'sum':
        target = r.randint(4, s1 + s2 - 2)
        fav = [o for o in outs if o[0] + o[1] == target]
        q = f'the total is {target}'
    elif kind == 'diff':
        target = r.randint(0, 3)
        fav = [o for o in outs if abs(o[0] - o[1]) == target]
        q = f'the difference between the scores is {target}'
    else:
        target = r.choice([6, 8, 12, 4])
        fav = [o for o in outs if o[0] * o[1] > target]
        q = f'the product of the scores is greater than {target}'
    return Q(f'A fair {s1}-sided spinner numbered 1 to {s1} and a fair {s2}-sided spinner numbered 1 to {s2} are spun. Use a sample space diagram to find the probability that {q}.',
             fr(Fr(len(fav), len(outs))), f'{len(outs)} equally likely outcomes (M1); {len(fav)} favourable (M1); {len(fav)}/{len(outs)} = {fr(Fr(len(fav), len(outs)))} (A1).', marks=3)


@t123.add('C3', (2, 3, 4, 5))
def t123_tree(r, D):
    a, b = r.randint(3, 9), r.randint(2, 8)
    cols = r.choice(BAGS)
    tot = a + b
    rep = D <= 3 or r.random() < 0.5
    if rep:
        same = Fr(a, tot) ** 2 + Fr(b, tot) ** 2
        txt = 'replaced'
        key = f'Tree diagram with ({a}/{tot}, {b}/{tot}) on both sets of branches (M1); ({a}/{tot})² + ({b}/{tot})² (M1) = {fr(same)} (A1).'
    else:
        same = Fr(a, tot) * Fr(a - 1, tot - 1) + Fr(b, tot) * Fr(b - 1, tot - 1)
        txt = 'not replaced'
        key = f'Second branches change: {a}/{tot} × {a - 1}/{tot - 1} + {b}/{tot} × {b - 1}/{tot - 1} (M1, M1) = {fr(same)} (A1).'
    return Q(f'A bag has {a} {cols[0]} and {b} {cols[1]} counters. A counter is taken at random and {txt}, then a second counter is taken. Use a tree diagram to work out the probability that both counters are the same colour.',
             fr(same), key, marks=3)


@t123.add('C1', (1, 2, 3))
def t123_count(r, D):
    s1, s2 = r.choice([(2, 6), (6, 6), (3, 4), (2, 2), (4, 5), (2, 3)])
    names = {2: 'a coin', 6: 'a dice', 3: 'a 3-sided spinner', 4: 'a 4-sided spinner', 5: 'a 5-sided spinner'}
    return MCQ(r, f'{names[s1].capitalize()} and {names[s2]} are used together. How many possible outcomes are there in the sample space?', str(s1 * s2), [str(s1 + s2), str(max(s1, s2)), str(s1 * s2 * 2), str(s1 * s2 - 1)],
               f'{s1} × {s2} = {s1 * s2}. [1]')


@t123.add('C2', (1, 2, 3, 4), 'explain')
def t123_err(r, D):
    p = person(r)
    t = r.choice([2, 3, 7, 12])
    ways = [(a, b) for a in range(1, 7) for b in range(1, 7) if a + b == t]
    return Q(f'Two fair dice are rolled. {p} says that the possible totals are 2 to 12, so P(total = {t}) = 1/11. Explain why {p} is wrong and give the correct probability.',
             f'The 11 totals are not equally likely. There are 36 equally likely outcomes and {len(ways)} give a total of {t}, so P = {fr(Fr(len(ways), 36))}.', 'B1 totals not equally likely; B1 correct probability. [2]')


@t123.add('C2', (2, 3, 4), 'explain')
def t123_tree_err(r, D):
    a, b = r.randint(3, 7), r.randint(2, 6)
    tot = a + b
    p = person(r)
    return Q(f'A bag has {a} red and {b} blue sweets. {p} takes one sweet and eats it, then takes another. On the tree diagram {p} writes {a}/{tot} for red on both sets of branches. Explain the mistake.',
             f'The first sweet is not replaced, so for the second sweet there are {tot - 1} left. If the first is red, P(red) = {a - 1}/{tot - 1}; if blue, P(red) = {a}/{tot - 1}.', 'B1 not replaced; B1 correct second-branch probabilities. [2]')


def _tree_c4(r, D):
    pa = r.choice([0.6, 0.7, 0.8, 0.4])
    pb_given = r.choice([0.9, 0.8, 0.75])
    pb_not = r.choice([0.5, 0.4, 0.3])
    p = person(r)
    intro = f'The probability that {p} revises for a test is {N(pa)}. If {p} revises, the probability of passing is {N(pb_given)}. If {p} does not revise, the probability of passing is {N(pb_not)}.'
    parts = [
        lambda r: ('Draw a tree diagram and write the probability on each branch. (Describe the branches.)', f'Revise {N(pa)}, not {N(round(1 - pa, 2))}; then pass {N(pb_given)}/fail {N(round(1 - pb_given, 2))} and pass {N(pb_not)}/fail {N(round(1 - pb_not, 2))}', 'B1 first set; B1 second sets [2]'),
        lambda r: (f'Work out the probability that {p} revises and passes.', N(round(pa * pb_given, 4)), 'M1; A1 [2]'),
        lambda r: (f'Work out the probability that {p} passes.', N(round(pa * pb_given + (1 - pa) * pb_not, 4)), 'M1 two paths; M1 add; A1 [3]'),
        lambda r: (f'Work out the probability that {p} fails.', N(round(1 - (pa * pb_given + (1 - pa) * pb_not), 4)), 'B1 [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t123.add('C4', (2, 3, 4, 5), 'multi_step')(_tree_c4)


@t123.add('C4', (3, 4, 5), 'multi_step')
def t123_game(r, D):
    s = r.choice([4, 5, 6])
    win = r.randint(s + 2, 2 * s - 1)
    outs = [(a, b) for a in range(1, s + 1) for b in range(1, s + 1)]
    fav = [o for o in outs if o[0] + o[1] >= win]
    pr = Fr(len(fav), len(outs))
    cost, prize = r.choice([(1, 3), (2, 5), (1, 4)])
    plays = 60
    return Q(f'In a game, two fair spinners each numbered 1 to {s} are spun. A player wins if the total is {win} or more. It costs ${cost} to play and a win pays ${prize}. (a) Work out the probability of winning. (b) In {plays} games, how many wins would you expect? (c) Would the organiser expect to make money over {plays} games? Show your working.',
             f'(a) {fr(pr)} (b) {N(float(pr * plays))} (c) Takes ${cost * plays}, pays about ${N(float(pr * plays * prize))}: {"yes" if cost * plays > pr * plays * prize else "no"}.',
             f'(a) M1 sample space {len(outs)} outcomes; A1 {fr(pr)} [2] (b) B1 [1] (c) M1 compares income and expected payout; A1 [2]', marks=5)


t123.fixed('C1', (1, 2), [
    ('What is a sample space?', 'A list or table of all the possible outcomes', 'B1 [1]', ['The most likely outcome', 'A probability of 1', 'A bar chart of results']),
    ('In a tree diagram, what do the probabilities on each set of branches from one point add up to?', '1', 'B1 [1]', ['0', 'The number of branches', '100']),
    ('Two coins are thrown. Write down the probability of one head and one tail.', '1/2', 'HT, TH out of 4. B1 [1]'),
])
t123.fixed('C2', (2, 3), [
    ('Explain why, on a tree diagram, you multiply along the branches and add between paths.', 'Along a path the events happen one after the other (A and then B), so multiply; different paths are mutually exclusive outcomes, so add their probabilities.', 'B1 multiply for and; B1 add for or. [2]'),
])


# ----------------------------------------------------------- relative frequency and expected outcomes
t124 = topic('Relative frequency and expected outcomes', 'chance experiments', 'relative frequency', 'expected outcomes')


@t124.add('C3', (1, 2, 3, 4, 5))
def t124_rf(r, D):
    n = r.choice([50, 80, 100, 120, 200, 250, 400, 500])
    k = r.randint(n // 10, n // 2)
    ev = r.choice(['a drawing pin lands point up', 'a spinner lands on red', 'a piece of toast lands butter side down', 'a bottle top lands upside down'])
    m = r.choice([300, 600, 1000, 1500])
    rf = Fr(k, n)
    if D <= 2:
        return Q(f'In an experiment, {ev} {k} times out of {n} trials. Work out the relative frequency.', N(round(float(rf), 4)) if (rf * 10000).denominator == 1 else fr(rf), f'{k} ÷ {n} (M1) = {fr(rf)} (A1).')
    return Q(f'In an experiment, {ev} {k} times out of {n} trials. Estimate how many times this would happen in {m} trials.', N(round(float(rf) * m, 2)),
             f'Relative frequency {k}/{n} (M1); × {m} = {N(round(float(rf) * m, 2))} (A1).')


@t124.add('C1', (1, 2, 3))
def t124_exp(r, D):
    p = r.choice([Fr(1, 6), Fr(1, 4), Fr(1, 2), Fr(1, 3), Fr(1, 5), Fr(3, 10)])
    n = p.denominator * r.randint(5, 40)
    what = r.choice(['a fair dice shows 6' if p == Fr(1, 6) else None, 'a spinner lands on blue', 'a coin lands heads' if p == Fr(1, 2) else None]) or 'a spinner lands on blue'
    return MCQ(r, f'The probability that {what} is {fr(p)}. It is used {n} times. How many times would you expect this to happen?', N(p * n), [N(n - p * n), N(p * n + p.denominator), N(n // p.denominator + 1) if p.numerator > 1 else N(p * n * 2), N(p.denominator)],
               f'{fr(p)} × {n} = {N(p * n)}. [1]')


@t124.add('C2', (1, 2, 3, 4), 'explain')
def t124_reliable(r, D):
    p, q = two_people(r)
    n1, n2 = r.choice([(20, 200), (10, 500), (30, 300), (25, 1000)])
    return Q(f'{p} and {q} each throw the same drawing pin to estimate the probability it lands point up. {p} throws it {n1} times and {q} throws it {n2} times. Whose estimate is more reliable? Explain.',
             f'{q}\'s: more trials give a more reliable estimate of the probability (relative frequency settles down as the number of trials increases).', 'B1 decision; B1 reason. [2]')


@t124.add('C2', (2, 3, 4), 'explain')
def t124_bias(r, D):
    n = r.choice([60, 120, 300, 600])
    k6 = int(n / 6 * r.choice([1.0, 1.1, 1.8, 2.2]))
    p = person(r)
    exp = n // 6
    biased = k6 > exp * 1.5
    return Q(f'{p} rolls a dice {n} times and gets a 6 on {k6} rolls. Do the results suggest the dice is biased? Explain.',
             f'Expected about {exp} sixes for a fair dice. {k6} is {"much more than" if biased else "close to"} {exp}, so {"the dice may be biased" if biased else "there is no strong evidence of bias"}.', 'M1 expected frequency; A1 conclusion with comparison. [2]')


def _rf_c4(r, D):
    cols = ['red', 'blue', 'green', 'yellow']
    n = r.choice([100, 200, 400])
    fr_ = [r.randint(10, 40) for _ in range(3)]
    fr_.append(n - sum(int(f * n / 100) for f in fr_))
    counts = [int(f * n / 100) for f in fr_[:3]] + [fr_[3]]
    if counts[3] <= 0:
        return None
    intro = f'A spinner with four colours is spun {n} times. The results are: ' + ', '.join(f'{c} {k}' for c, k in zip(cols, counts)) + '.'
    m = r.choice([500, 1000, 2000])
    parts = [
        lambda r: ('Work out the relative frequency of blue.', N(counts[1] / n), 'B1 [1]'),
        lambda r: (f'Estimate how many times it would land on green in {m} spins.', N(counts[2] / n * m), 'M1; A1 [2]'),
        lambda r: ('Do the results suggest that the spinner is fair? Explain.', ('Probably not: ' if max(counts) > 1.4 * n / 4 or min(counts) < 0.6 * n / 4 else 'Possibly fair: ') + f'a fair spinner would give about {n // 4} for each colour.', 'B1 expected; B1 conclusion [2]'),
        lambda r: ('Explain how to get a more reliable estimate of the probability of yellow.', 'Spin the spinner many more times.', 'B1 [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t124.add('C4', (2, 3, 4, 5), 'multi_step')(_rf_c4)
t124.fixed('C1', (1, 2), [
    ('What is the relative frequency of an event?', 'The number of times it happens divided by the number of trials', 'B1 [1]', ['The number of trials divided by the number of successes', 'The theoretical probability', 'The number of successes']),
    ('A fair coin is thrown 300 times. About how many heads would you expect?', '150', '1/2 × 300. [1]', ['300', '100', '200']),
    ('Write down when it is better to use relative frequency than theoretical probability.', 'When outcomes are not equally likely or the probabilities cannot be calculated (e.g. a drawing pin).', 'B1 [1]'),
])

CHAPTERS[12] = [t121, t122, t123, t124]


# =========================================================== 13 Position and transformation
def brg(x):
    return f'{int(x) % 360:03d}°'


t131 = topic('Bearings and scale drawings', 'bearings', 'scale drawings')


@t131.add('C1', (1, 2, 3))
def t131_back(r, D):
    b = r.randint(10, 350)
    if D == 1:
        b = r.choice([30, 45, 60, 70, 110, 135, 150, 200, 225, 250, 300, 315])
    back = (b + 180) % 360
    a, c = r.sample(['A', 'B', 'P', 'Q', 'X', 'Y'], 2)
    return MCQ(r, f'The bearing of {c} from {a} is {brg(b)}. What is the bearing of {a} from {c}?', brg(back), [brg(360 - b), brg(b + 90), brg(abs(180 - b)) if abs(180 - b) != back else brg(b + 270), brg(b)],
               f'Back bearing = {brg(b)} {"+" if b < 180 else "−"} 180° = {brg(back)}. [1]')


@t131.add('C1', (1, 2, 3))
def t131_compass(r, D):
    d = r.choice([('north-east', 45), ('east', 90), ('south-east', 135), ('south', 180), ('south-west', 225), ('west', 270), ('north-west', 315)])
    return MCQ(r, f'What is the three-figure bearing of the direction {d[0]}?', brg(d[1]), [brg(360 - d[1]) if d[1] != 180 else '360°', brg(d[1] + 90), brg(d[1] - 45), f'{d[1] // 10}°'], f'Measured clockwise from north: {brg(d[1])}. [1]')


@t131.add('C3', (1, 2, 3, 4, 5))
def t131_scale(r, D):
    sc = r.choice([25000, 50000, 100000, 200000, 250000])
    cm = r.choice([2.5, 3, 4, 4.8, 6, 7.5, 8.2, 12])
    km = cm * sc / 100000
    if r.random() < 0.5:
        return Q(f'A map has a scale of 1 : {sc:,}. Two towns are {N(cm)} cm apart on the map. Work out the real distance between them in kilometres.', f'{N(km)} km',
                 f'{N(cm)} × {sc:,} = {N(cm * sc)} cm (M1); ÷ 100 000 = {N(km)} km (A1).')
    return Q(f'A map has a scale of 1 : {sc:,}. The real distance between two villages is {N(km)} km. How far apart are they on the map, in cm?', f'{N(cm)} cm',
             f'{N(km)} km = {N(km * 100000)} cm (M1); ÷ {sc:,} = {N(cm)} cm (A1).')


@t131.add('C3', (2, 3, 4, 5))
def t131_angle(r, D):
    b1 = r.randint(20, 160)
    turn = r.randint(20, 100)
    kind = r.choice(['back', 'turn'])
    if kind == 'back':
        b = r.randint(181, 340)
        return Q(f'A ship sails from port P on a bearing of {brg(b)} to a lighthouse L. Work out the bearing it must sail on to return from L to P. Explain your method.', brg(b - 180),
                 f'The return is in the opposite direction, so subtract 180° (M1): {b} − 180 = {brg(b - 180)} (A1).')
    nb = (b1 + turn) % 360
    return Q(f'A plane flies on a bearing of {brg(b1)}. It then turns {turn}° clockwise. Write down the new bearing, and the bearing that would take it straight back the way it has just come.', f'{brg(nb)}; {brg(nb + 180)}',
             f'{b1} + {turn} = {brg(nb)} (B1); back bearing {brg(nb)} {"+" if nb < 180 else "−"} 180 = {brg(nb + 180)} (B1).')


@t131.add('C2', (1, 2, 3, 4), 'explain')
def t131_err(r, D):
    b = r.randint(200, 340)
    p = person(r)
    if r.random() < 0.5:
        return Q(f'The bearing of B from A is {brg(b)}. {p} says the bearing of A from B is {brg(b + 180)} = {b + 180}°. Explain the mistake.',
                 f'Bearings are less than 360°. Since {b} > 180, subtract 180: the bearing of A from B is {brg(b - 180)}.', 'B1 cannot exceed 360°; B1 correct back bearing. [2]')
    a = r.choice([30, 45, 60, 75])
    return Q(f'{p} measures a bearing of {a}° anticlockwise from north and writes it as {brg(a)}. Explain the mistake and give the correct bearing.',
             f'Bearings are measured clockwise from north. {a}° anticlockwise is {360 - a}° clockwise, so the bearing is {brg(360 - a)}.', 'B1 clockwise from north; B1 correct value. [2]')


@t131.add('C2', (2, 3, 4), 'explain')
def t131_why(r, D):
    sc = r.choice([50, 100, 200, 500])
    L = r.choice([6, 8, 12, 15])
    return Q(f'A plan of a classroom is drawn using a scale of 1 : {sc}. A wall is {L} m long. Explain how to work out the length of the wall on the plan, and give the answer in cm.',
             f'Convert {L} m to {L * 100} cm and divide by {sc}: {N(L * 100 / sc)} cm.', 'B1 converts units; B1 divides by scale factor and gives value. [2]')


def _bear_c4(r, D):
    a = r.choice([3, 4, 5, 6, 8, 12])
    dirs = r.choice([('east', 'north', 225), ('east', 'south', 315), ('west', 'north', 135), ('west', 'south', 45)])
    dist = math.sqrt(2) * a
    p = person(r)
    sc = r.choice([1, 2])
    intro = f'A boat leaves harbour H and sails {a} km due {dirs[0]} to point B, then {a} km due {dirs[1]} to point C.'
    parts = [
        lambda r: ('Calculate the direct distance from C back to H, to 2 decimal places.', f'{fdp(dist, 2)} km', f'M1 √({a}² + {a}²); A1 {fdp(dist, 2)} [2]'),
        lambda r: ('Explain why angle BCH is 45°.', 'Triangle HBC is right-angled at B and isosceles (HB = BC), so the other two angles are each 45°.', 'B1 B1 [2]'),
        lambda r: ('Work out the bearing of H from C.', brg(dirs[2]), 'M1 uses 45°; A1 [2]'),
        lambda r: (f'A scale drawing uses 1 cm to represent {sc} km. How long is the line HB on the drawing?', f'{N(a / sc)} cm', 'B1 [1]'),
        lambda r: ('Write down the bearing of B from H.', brg({'east': 90, 'west': 270}[dirs[0]]), 'B1 [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t131.add('C4', (2, 3, 4, 5), 'multi_step')(_bear_c4)
t131.fixed('C1', (1, 2), [
    ('From which direction are bearings measured?', 'Clockwise from north', 'B1 [1]', ['Anticlockwise from north', 'Clockwise from east', 'Anticlockwise from south']),
    ('A scale is 1 cm to 5 km. What real distance does 7 cm represent?', '35 km', '7 × 5. [1]', ['12 km', '1.4 km', '3.5 km']),
    ('Write down the bearing of due west.', '270°', 'B1 [1]'),
])
t131.fixed('C2', (2, 3), [
    ('Explain why the bearing of A from B and the bearing of B from A always differ by 180°.', 'They are opposite directions along the same line, and opposite directions differ by half a turn, 180°.', 'B1 B1. [2]'),
])


# ----------------------------------------------------------- midpoints and dividing a line segment
t132 = topic('Midpoints and dividing a line segment in a ratio', 'points on a line segment', 'midpoints', 'dividing in a ratio')


def pt(x, y):
    return f'({N(x)}, {N(y)})'


@t132.add('C1', (1, 2, 3))
def t132_mid(r, D):
    x1, y1, x2, y2 = [r.randint(-8, 10) for _ in range(4)]
    if D == 1:
        x1, y1, x2, y2 = [r.randint(0, 10) for _ in range(4)]
    mx, my = Fr(x1 + x2, 2), Fr(y1 + y2, 2)
    ans = f'({N(float(mx))}, {N(float(my))})'
    return MCQ(r, f'What is the midpoint of the line segment from {pt(x1, y1)} to {pt(x2, y2)}?', ans,
               [f'({N(float(Fr(x2 - x1, 2)))}, {N(float(Fr(y2 - y1, 2)))})', f'({N(x1 + x2)}, {N(y1 + y2)})', f'({N(float(my))}, {N(float(mx))})', f'({N(float(mx))}, {N(float(my) + 1)})'],
               f'Average the coordinates: {ans}. [1]')


@t132.add('C3', (1, 2, 3, 4, 5))
def t132_calc(r, D):
    x1, y1 = r.randint(-6, 8), r.randint(-6, 8)
    kind = r.choice(['mid', 'end', 'ratio'] if D >= 3 else ['mid', 'end'])
    if kind == 'mid':
        x2, y2 = r.randint(-6, 12), r.randint(-6, 12)
        return Q(f'Find the midpoint of AB where A is {pt(x1, y1)} and B is {pt(x2, y2)}.', f'({N((x1 + x2) / 2)}, {N((y1 + y2) / 2)})',
                 f'(({N(x1)} + {N(x2)})/2, ({N(y1)} + {N(y2)})/2) (M1) = ({N((x1 + x2) / 2)}, {N((y1 + y2) / 2)}) (A1).')
    if kind == 'end':
        mx, my = r.randint(-4, 8), r.randint(-4, 8)
        return Q(f'M {pt(mx, my)} is the midpoint of AB. A is {pt(x1, y1)}. Find the coordinates of B.', pt(2 * mx - x1, 2 * my - y1),
                 f'B = (2 × {N(mx)} − {par(x1)}, 2 × {N(my)} − {par(y1)}) (M1) = {pt(2 * mx - x1, 2 * my - y1)} (A1).')
    m, n = r.choice([(1, 2), (1, 3), (2, 1), (3, 1), (2, 3), (1, 4), (3, 2)])
    k = m + n
    dx, dy = k * r.randint(-3, 4), k * r.randint(-3, 4)
    if dx == 0 and dy == 0:
        dx = k
    x2, y2 = x1 + dx, y1 + dy
    px, py = x1 + dx * m // k, y1 + dy * m // k
    return Q(f'A is {pt(x1, y1)} and B is {pt(x2, y2)}. Point P lies on AB so that AP : PB = {m} : {n}. Find the coordinates of P.', pt(px, py),
             f'P is {m}/{k} of the way from A to B (M1); A + {m}/{k} × ({N(dx)}, {N(dy)}) (M1) = {pt(px, py)} (A1).', marks=3)


@t132.add('C2', (1, 2, 3, 4), 'explain')
def t132_err(r, D):
    x1, y1, x2, y2 = r.randint(1, 6), r.randint(1, 6), r.randint(7, 14), r.randint(7, 14)
    p = person(r)
    if r.random() < 0.5:
        return Q(f'{p} says the midpoint of {pt(x1, y1)} and {pt(x2, y2)} is ({N((x2 - x1) / 2)}, {N((y2 - y1) / 2)}). Explain the mistake and give the correct midpoint.',
                 f'{p} halved the differences instead of averaging the coordinates. Midpoint = ({N((x1 + x2) / 2)}, {N((y1 + y2) / 2)}).', 'B1 add then halve; B1 correct midpoint. [2]')
    return Q(f'A is {pt(x1, y1)} and B is {pt(x1 + 4, y1 + 8)}. {p} says the point that divides AB in the ratio 1 : 3 is the midpoint of A and the midpoint of AB. Is {p} correct? Explain.',
             f'Yes. The midpoint of AB is half way; the midpoint of A and that point is 1/4 of the way, which is AP : PB = 1 : 3. P = {pt(x1 + 1, y1 + 2)}.', 'B1 1/4 of the way; B1 coordinates. [2]')


@t132.add('C2', (2, 3, 4), 'explain')
def t132_check(r, D):
    x1, y1 = r.randint(-5, 5), r.randint(-5, 5)
    dx, dy = 2 * r.randint(1, 5), 2 * r.randint(1, 5)
    off = r.choice([0, 1])
    M = (x1 + dx // 2 + off, y1 + dy // 2)
    p = person(r)
    return Q(f'{p} says {pt(*M)} is the midpoint of {pt(x1, y1)} and {pt(x1 + dx, y1 + dy)}. Explain how to check this and say whether {p} is right.',
             f'The midpoint is (({N(x1)} + {N(x1 + dx)})/2, ({N(y1)} + {N(y1 + dy)})/2) = {pt(x1 + dx // 2, y1 + dy // 2)}, so {p} is {"right" if off == 0 else "wrong"}.', 'M1 method; A1 conclusion. [2]')


def _seg_c4(r, D):
    ax, ay = r.randint(-4, 2), r.randint(-4, 2)
    bx, by = ax + 2 * r.randint(2, 5), ay + 2 * r.randint(1, 4)
    cx, cy = bx + r.randint(-2, 3), by + 2 * r.randint(2, 4)
    dx_, dy_ = ax + (cx - bx), ay + (cy - by)
    intro = f'ABCD is a parallelogram with A{pt(ax, ay)}, B{pt(bx, by)} and C{pt(cx, cy)}.'
    parts = [
        lambda r: ('Find the midpoint of the diagonal AC.', f'({N((ax + cx) / 2)}, {N((ay + cy) / 2)})', 'M1; A1 [2]'),
        lambda r: ('The diagonals of a parallelogram bisect each other. Use this to find the coordinates of D.', pt(dx_, dy_), 'M1 midpoint of BD = midpoint of AC; A1 [2]'),
        lambda r: ('Point Q lies on AB so that AQ : QB = 1 : 3. Find the coordinates of Q.', f'({N(ax + (bx - ax) / 4)}, {N(ay + (by - ay) / 4)})', 'M1 1/4 of the way from A; A1 [2]'),
        lambda r: (f'Point P lies on AB so that AP : PB = 3 : 1. Find the coordinates of P.', f'({N(ax + 3 * (bx - ax) / 4)}, {N(ay + 3 * (by - ay) / 4)})', 'M1 3/4 of the way; A1 [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t132.add('C4', (2, 3, 4, 5), 'multi_step')(_seg_c4)
t132.fixed('C1', (1, 2), [
    ('What is the midpoint of (0, 0) and (8, 6)?', '(4, 3)', 'Halve each coordinate. [1]', ['(8, 6)', '(16, 12)', '(3, 4)']),
    ('Point P divides AB in the ratio 1 : 1. Where is P?', 'At the midpoint of AB', 'B1 [1]', ['At A', 'At B', 'One third of the way from A']),
    ('Write down the midpoint of (2, 5) and (2, 11).', '(2, 8)', 'B1 [1]'),
])


# ----------------------------------------------------------- transformations
t133 = topic('Transformations', 'transformations', 'reflection rotation translation', 'combined transformations')
TRANS = [
    ('reflection in the x-axis', lambda x, y: (x, -y)), ('reflection in the y-axis', lambda x, y: (-x, y)), ('reflection in the line y = x', lambda x, y: (y, x)),
    ('reflection in the line y = −x', lambda x, y: (-y, -x)), ('rotation of 90° clockwise about the origin', lambda x, y: (y, -x)),
    ('rotation of 90° anticlockwise about the origin', lambda x, y: (-y, x)), ('rotation of 180° about the origin', lambda x, y: (-x, -y)),
]


def _trans(r, D):
    if D >= 3 and r.random() < 0.4:
        k = r.randint(-3, 4)
        if r.random() < 0.5:
            return f'reflection in the line x = {N(k)}', (lambda x, y, k=k: (2 * k - x, y))
        return f'reflection in the line y = {N(k)}', (lambda x, y, k=k: (x, 2 * k - y))
    if r.random() < 0.25:
        a, b = r.randint(-6, 6), r.randint(-6, 6)
        return f'translation by the vector ({N(a)}, {N(b)})', (lambda x, y, a=a, b=b: (x + a, y + b))
    return r.choice(TRANS)


@t133.add('C1', (1, 2, 3))
def t133_point(r, D):
    x, y = r.choice([v for v in range(-6, 7) if v]), r.choice([v for v in range(-6, 7) if v])
    if abs(x) == abs(y):
        y += 1 if y > 0 else -1
    name, f = _trans(r, D)
    ans = pt(*f(x, y))
    cands = [pt(*g(x, y)) for _, g in TRANS] + [pt(x + 1, y), pt(y, -x)]
    return MCQ(r, f'The point {pt(x, y)} is transformed by a {name}. What are the coordinates of its image?', ans, cands, f'{name.capitalize()}: {pt(x, y)} → {ans}. [1]')


@t133.add('C3', (1, 2, 3, 4, 5))
def t133_tri(r, D):
    P = [(r.randint(1, 5), r.randint(1, 5)) for _ in range(3)]
    if (P[1][0] - P[0][0]) * (P[2][1] - P[0][1]) == (P[2][0] - P[0][0]) * (P[1][1] - P[0][1]):
        return None
    name, f = _trans(r, D)
    img = [f(*p) for p in P]
    if D >= 4:
        name2, g = _trans(r, D)
        img2 = [g(*q) for q in img]
        return Q(f'Triangle T has vertices {", ".join(pt(*p) for p in P)}. T is transformed by a {name}, and then the image is transformed by a {name2}. Write down the coordinates of the final image.',
                 ', '.join(pt(*q) for q in img2), f'First image {", ".join(pt(*q) for q in img)} (M1, A1); final image {", ".join(pt(*q) for q in img2)} (A1).', marks=3)
    return Q(f'Triangle A has vertices {", ".join(pt(*p) for p in P)}. Write down the coordinates of the vertices of the image of triangle A after a {name}.',
             ', '.join(pt(*q) for q in img), f'Apply the rule to each vertex (M1); {", ".join(pt(*q) for q in img)} (A1).')


@t133.add('C3', (2, 3, 4, 5))
def t133_describe(r, D):
    P = [(r.randint(1, 6), r.randint(1, 6)) for _ in range(3)]
    if (P[1][0] - P[0][0]) * (P[2][1] - P[0][1]) == (P[2][0] - P[0][0]) * (P[1][1] - P[0][1]):
        return None
    name, f = r.choice(TRANS + [('translation by the vector (−4, 3)', lambda x, y: (x - 4, y + 3)), ('translation by the vector (5, −2)', lambda x, y: (x + 5, y - 2))])
    img = [f(*p) for p in P]
    if set(img) == set(P):
        return None
    return Q(f'Triangle P has vertices {", ".join(pt(*p) for p in P)}. Triangle Q has vertices {", ".join(pt(*q) for q in img)}. Describe fully the single transformation that maps P onto Q.',
             name[0].upper() + name[1:], 'B1 type of transformation; B1 full detail (mirror line / angle, direction and centre / vector).')


@t133.add('C2', (1, 2, 3, 4), 'explain')
def t133_err(r, D):
    x, y = r.randint(1, 6), r.randint(1, 6)
    if x == y:
        x += 1
    p = person(r)
    kind = r.choice(['rot', 'refl', 'desc'])
    if kind == 'rot':
        return Q(f'{p} rotates the point {pt(x, y)} through 90° clockwise about the origin and gets {pt(-y, x)}. Explain the mistake and give the correct image.',
                 f'{pt(-y, x)} is the result of a 90° ANTICLOCKWISE rotation. Clockwise: (x, y) → (y, −x), giving {pt(y, -x)}.', 'B1 direction confused; B1 correct image. [2]')
    if kind == 'refl':
        return Q(f'{p} reflects {pt(x, y)} in the x-axis and gets {pt(-x, y)}. Explain the mistake.',
                 f'Reflecting in the x-axis keeps x the same and changes the sign of y: {pt(x, -y)}. {p} has reflected in the y-axis.', 'B1 explanation; B1 correct image. [2]')
    return Q(f'{p} describes a transformation as "a rotation of 90°". Explain why this description is not complete.',
             'A rotation must give the angle, the direction (clockwise or anticlockwise) and the centre of rotation.', 'B1 direction; B1 centre. [2]')


@t133.add('C2', (2, 3, 4), 'explain')
def t133_combo(r, D):
    pairs = [('reflection in the x-axis', 'reflection in the y-axis', 'rotation of 180° about the origin'),
             ('reflection in the y-axis', 'reflection in the x-axis', 'rotation of 180° about the origin'),
             ('rotation of 90° clockwise about the origin', 'rotation of 90° clockwise about the origin', 'rotation of 180° about the origin'),
             ('translation by the vector (2, 3)', 'translation by the vector (−5, 1)', 'translation by the vector (−3, 4)'),
             ('reflection in the line y = x', 'reflection in the line y = x', 'no change (the shape returns to where it started)')]
    a, b, c = r.choice(pairs)
    x, y = r.randint(1, 5), r.randint(2, 6)
    return Q(f'A shape is transformed by a {a} followed by a {b}. Describe the single transformation that has the same effect. Check your answer with the point {pt(x, y)}.',
             c[0].upper() + c[1:] + '.', 'B1 correct single transformation; B1 check with the point. [2]')


def _tr_c4(r, D):
    P = [(1, 1), (r.randint(3, 5), 1), (1, r.randint(2, 4))]
    nA, fA = r.choice(TRANS[:4])
    nB, fB = r.choice(TRANS[4:])
    A = [fA(*p) for p in P]
    B = [fB(*p) for p in A]
    intro = f'Triangle T has vertices {", ".join(pt(*p) for p in P)}. T is mapped onto triangle A by a {nA}. Triangle A is then mapped onto triangle B by a {nB}.'
    parts = [
        lambda r: ('Write down the coordinates of the vertices of triangle A.', ', '.join(pt(*q) for q in A), 'B2 (B1 for two correct) [2]'),
        lambda r: ('Write down the coordinates of the vertices of triangle B.', ', '.join(pt(*q) for q in B), 'M1; A1 [2]'),
        lambda r: ('Explain why triangle B is congruent to triangle T.', 'Reflections and rotations do not change lengths or angles.', 'B1 [1]'),
        lambda r: ('Explain how to decide whether a single transformation maps T onto B.', 'Compare the coordinates of T and B and test a rule (e.g. reflection in y = x swaps coordinates).', 'B1 [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t133.add('C4', (2, 3, 4, 5), 'multi_step')(_tr_c4)
t133.fixed('C1', (1, 2), [
    ('Which transformation does not change the orientation of a shape?', 'Translation', 'A translation slides the shape without turning or flipping. [1]', ['Reflection', 'Rotation of 90°', 'Reflection in y = x']),
    ('What stays the same in a reflection, rotation or translation?', 'Lengths and angles (the shapes are congruent)', 'B1 [1]', ['Only the area', 'The position of every point', 'Only the orientation']),
    ('Write down the image of (3, −2) after a translation by the vector (−1, 4).', '(2, 2)', 'B1 [1]'),
])


# ----------------------------------------------------------- enlargement
t134 = topic('Enlargement', 'enlarging shapes', 'positive and fractional scale factors', 'enlargement')
SFS = [2, 3, 4, Fr(1, 2), Fr(1, 3), Fr(3, 2), Fr(1, 4)]


@t134.add('C3', (1, 2, 3, 4, 5))
def t134_coords(r, D):
    k = Fr(r.choice(SFS[:3] if D <= 2 else SFS))
    cx, cy = (0, 0) if D <= 2 else (r.randint(-2, 3), r.randint(-2, 3))
    den = k.denominator
    P = [(cx + den * r.randint(1, 3), cy + den * r.randint(0, 3)) for _ in range(3)]
    (x1, y1), (x2, y2), (x3, y3) = P
    if (x2 - x1) * (y3 - y1) == (x3 - x1) * (y2 - y1):
        return None
    img = [(cx + k * (x - cx), cy + k * (y - cy)) for x, y in P]
    cen = 'the origin' if (cx, cy) == (0, 0) else pt(cx, cy)
    return Q(f'Triangle A has vertices {", ".join(pt(*p) for p in P)}. Triangle A is enlarged by scale factor {fr(k)} with centre {cen}. Write down the coordinates of the image.',
             ', '.join(pt(int(x), int(y)) for x, y in img), f'Vector from centre to each vertex × {fr(k)} (M1); image {", ".join(pt(int(x), int(y)) for x, y in img)} (A1).')


@t134.add('C1', (1, 2, 3))
def t134_sf(r, D):
    a = r.randint(2, 12)
    k = Fr(r.choice(SFS))
    b = a * k
    if b.denominator != 1:
        a *= b.denominator
        b = a * k
    return MCQ(r, f'A side of length {a} cm becomes {fr(b)} cm after an enlargement. What is the scale factor?', fr(k), [fr(1 / k), fr(b - a) if b != a else '0', fr(k * 2), fr(k + 1)], f'{fr(b)} ÷ {a} = {fr(k)}. [1]')


@t134.add('C2', (1, 2, 3, 4), 'explain')
def t134_area(r, D):
    k = r.choice([2, 3, 4, Fr(1, 2)])
    A = r.choice([6, 8, 10, 12, 20])
    p = person(r)
    return Q(f'A rectangle with area {A} cm² is enlarged by scale factor {fr(k)}. {p} says the new area is {N(A * k)} cm². Explain why {p} is wrong and give the correct area.',
             f'Both the length and the width are multiplied by {fr(k)}, so the area is multiplied by {fr(k)}² = {fr(k * k)}: {N(A * k * k)} cm².', 'B1 area factor k²; B1 correct area. [2]')


@t134.add('C2', (2, 3, 4), 'explain')
def t134_frac(r, D):
    k = r.choice([Fr(1, 2), Fr(1, 3), Fr(2, 3), Fr(1, 4)])
    p = person(r)
    return Q(f'{p} says that an enlargement always makes a shape bigger. Use an enlargement with scale factor {fr(k)} to explain why this is not true.',
             f'With scale factor {fr(k)} (between 0 and 1) every length is multiplied by {fr(k)}, so the image is smaller. It is still called an enlargement.', 'B1 lengths × k < original; B1 conclusion. [2]')


@t134.add('C3', (2, 3, 4, 5))
def t134_find(r, D):
    k = r.choice([2, 3])
    cx, cy = r.randint(-2, 2), r.randint(-2, 2)
    P = [(cx + r.randint(1, 3), cy + r.randint(1, 3)) for _ in range(3)]
    if (P[1][0] - P[0][0]) * (P[2][1] - P[0][1]) == (P[2][0] - P[0][0]) * (P[1][1] - P[0][1]):
        return None
    img = [(cx + k * (x - cx), cy + k * (y - cy)) for x, y in P]
    return Q(f'Triangle P has vertices {", ".join(pt(*p) for p in P)}. Triangle Q has vertices {", ".join(pt(*q) for q in img)}. Q is an enlargement of P. Find the scale factor and the centre of enlargement.',
             f'Scale factor {k}; centre {pt(cx, cy)}', f'Compare corresponding lengths: scale factor {k} (B1); draw lines through corresponding vertices and find where they meet (M1); centre {pt(cx, cy)} (A1).', marks=3)


def _enl_c4(r, D):
    k = r.choice([2, 3, Fr(1, 2)])
    w, h = 2 * r.randint(2, 5), 2 * r.randint(1, 4)
    intro = f'A rectangle measures {w} cm by {h} cm. It is enlarged by scale factor {fr(k)}.'
    parts = [
        lambda r: ('Work out the dimensions of the image.', f'{N(w * k)} cm by {N(h * k)} cm', 'B1 [1]'),
        lambda r: ('Work out the perimeter of the image and compare it with the original perimeter.', f'{N(2 * (w + h) * k)} cm; it is {fr(k)} times the original {2 * (w + h)} cm', 'M1; A1 [2]'),
        lambda r: ('Work out the area of the image and compare it with the original area.', f'{N(w * h * k * k)} cm²; {fr(k * k)} times the original {w * h} cm²', 'M1; A1 [2]'),
        lambda r: ('Explain why the angles of the image are the same as the angles of the original.', 'Enlargement keeps the shape the same (similar shapes); only the lengths change.', 'B1 [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t134.add('C4', (2, 3, 4, 5), 'multi_step')(_enl_c4)
t134.fixed('C1', (1, 2), [
    ('What happens to a shape enlarged by scale factor 1/2?', 'Each length is halved', 'B1 [1]', ['Each length is doubled', 'The area is halved', 'The shape is reflected']),
    ('A shape is enlarged by scale factor 3. By what factor is its area multiplied?', '9', '3² = 9. [1]', ['3', '6', '27']),
    ('Write down the image of (4, 6) after an enlargement with scale factor 1/2, centre the origin.', '(2, 3)', 'B1 [1]'),
])

CHAPTERS[13] = [t131, t132, t133, t134]


# =========================================================== 14 Volume, surface area and symmetry
QUADS = {
    'square': {'4 equal sides', '4 right angles', 'diagonals equal', 'diagonals perpendicular', 'diagonals bisect each other', '2 pairs of parallel sides'},
    'rectangle': {'4 right angles', 'diagonals equal', 'diagonals bisect each other', '2 pairs of parallel sides'},
    'rhombus': {'4 equal sides', 'diagonals perpendicular', 'diagonals bisect each other', '2 pairs of parallel sides'},
    'parallelogram': {'diagonals bisect each other', '2 pairs of parallel sides'},
    'kite': {'diagonals perpendicular', 'exactly one line of symmetry'},
    'trapezium': {'exactly one pair of parallel sides'},
}
QSYM = {'square': (4, 4), 'rectangle': (2, 2), 'rhombus': (2, 2), 'parallelogram': (0, 2), 'kite': (1, 1), 'isosceles trapezium': (1, 1)}
t141 = topic('Properties of quadrilaterals and polygons', 'properties of quadrilaterals and polygons', 'quadrilaterals')


@t141.add('C1', (1, 2, 3))
def t141_name(r, D):
    for _ in range(40):
        q = r.choice(list(QUADS))
        props = r.sample(sorted(QUADS[q]), min(2, len(QUADS[q])))
        others = [o for o in QUADS if o != q and set(props) <= QUADS[o]]
        if not others:
            break
    else:
        return None
    nots = [p for p in ['4 equal sides', '4 right angles', 'diagonals equal'] if p not in QUADS[q]]
    desc = ' and '.join(props) + (f', but not {nots[0]}' if nots and q != 'trapezium' else '')
    others_ok = [o for o in QUADS if o != q and set(props) <= QUADS[o] and (not nots or nots[0] not in QUADS[o])]
    if others_ok:
        return None
    return MCQ(r, f'A quadrilateral has {desc}. Which quadrilateral is it?', q.capitalize(), [o.capitalize() for o in QUADS if o != q], f'Only a {q} has all these properties. [1]')


@t141.add('C1', (1, 2, 3))
def t141_sym(r, D):
    q = r.choice(list(QSYM))
    lines, order = QSYM[q]
    which = r.choice(['lines of symmetry', 'order of rotational symmetry'])
    v = lines if which.startswith('lines') else order
    return MCQ(r, f'How many {which} does {art(q)} have?' if which.startswith('lines') else f'What is the order of rotational symmetry of {art(q)}?', str(v), [str(x) for x in range(5) if x != v],
               f'{q.capitalize()}: {lines} lines, order {order}. [1]')


@t141.add('C2', (1, 2, 3, 4), 'explain')
def t141_claim(r, D):
    claims = [('Every square is a rhombus.', True, 'A square has 4 equal sides, which is the definition of a rhombus.'),
              ('Every rhombus is a square.', False, 'A rhombus need not have right angles, e.g. one with angles 60° and 120°.'),
              ('Every rectangle is a parallelogram.', True, 'A rectangle has two pairs of parallel sides.'),
              ('The diagonals of a rectangle are perpendicular.', False, 'Only when the rectangle is a square; e.g. a 6 cm by 2 cm rectangle has diagonals that are not at 90°.'),
              ('A kite has two pairs of parallel sides.', False, 'A kite has two pairs of equal adjacent sides and in general no parallel sides.'),
              ('A parallelogram has rotational symmetry of order 2.', True, 'A half turn about the point where the diagonals cross maps it onto itself.'),
              ('Every parallelogram has a line of symmetry.', False, 'A general parallelogram (not a rhombus or rectangle) has no lines of symmetry.'),
              ('The diagonals of a rhombus cross at right angles.', True, 'Its diagonals are perpendicular bisectors of each other.')]
    c, ok, why = r.choice(claims)
    p = person(r)
    return Q(f'{p} says: "{c}" Is {p} correct? Give a reason.', f'{"Yes" if ok else "No"}. {why}', 'B1 decision; B1 reason or counter-example. [2]')


@t141.add('C3', (1, 2, 3, 4, 5))
def t141_angles(r, D):
    q = r.choice(['parallelogram', 'kite', 'isosceles trapezium', 'rhombus'])
    a = r.randint(40, 80)
    if q in ('parallelogram', 'rhombus'):
        return Q(f'One angle of a {q} is {a}°. Work out the sizes of the other three angles. Give reasons.', f'{180 - a}°, {a}°, {180 - a}°',
                 f'Opposite angles equal (B1); co-interior / adjacent angles add to 180° (M1); {180 - a}°, {a}°, {180 - a}° (A1).', marks=3)
    if q == 'kite':
        b = r.randint(50, 120)
        e = (360 - a - b) / 2
        return Q(f'In a kite, the two angles between the pairs of unequal sides are equal. The other two angles are {a}° and {b}°. Work out the size of each equal angle.', f'{N(e)}°',
                 f'Angle sum 360° (M1); (360 − {a} − {b}) ÷ 2 (M1) = {N(e)}° (A1).', marks=3)
    return Q(f'An isosceles trapezium has two angles of {a}° at the ends of its longer parallel side. Work out the other two angles.', f'{180 - a}° each',
             f'Co-interior angles between the parallel sides add to 180° (M1); {180 - a}° (A1).')


@t141.add('C3', (2, 3, 4, 5))
def t141_coords(r, D):
    shape = r.choice(['square', 'rectangle', 'parallelogram', 'kite'])
    x, y = r.randint(-3, 3), r.randint(-3, 3)
    a, b = r.randint(2, 5), r.randint(1, 4)
    if shape == 'square':
        V = [(x, y), (x + a, y), (x + a, y + a), (x, y + a)]
    elif shape == 'rectangle':
        if a == b + 1:
            b += 1
        V = [(x, y), (x + a, y), (x + a, y + b + 1), (x, y + b + 1)]
    elif shape == 'parallelogram':
        V = [(x, y), (x + a, y), (x + a + b, y + 3), (x + b, y + 3)]
    else:
        V = [(x, y), (x + a, y + a + b), (x, y + 2 * a + 2 * b), (x - a, y + a + b)]
        V = [(x, y), (x + a, y + b + 2), (x, y + 2 * b + 4 + a), (x - a, y + b + 2)]
    return Q(f'The points {", ".join(pt(*v) for v in V)} are joined in order. Name the quadrilateral formed and give one property that confirms your answer.', shape.capitalize(),
             'B1 correct name; B1 property supported by the coordinates (side lengths, parallel sides, right angles or symmetry).')


def _quad_c4(r, D):
    a = r.randint(55, 80)
    s = r.randint(5, 12)
    intro = f'ABCD is a rhombus with sides of length {s} cm and angle DAB = {a}°.'
    parts = [
        lambda r: ('Work out angle ABC. Give a reason.', f'{180 - a}° (co-interior angles between parallel sides add to 180°)', 'B1 value; B1 reason [2]'),
        lambda r: ('Work out angle BAC, where AC is a diagonal. Give a reason.', f'{N(a / 2)}° (the diagonals of a rhombus bisect its angles)', 'B1; B1 [2]'),
        lambda r: ('Write down the perimeter of the rhombus.', f'{4 * s} cm', 'B1 [1]'),
        lambda r: ('Write down the size of the angle between the diagonals.', '90°', 'B1 [1]'),
        lambda r: ('State the number of lines of symmetry and the order of rotational symmetry of the rhombus.', '2 lines; order 2', 'B1 B1 [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t141.add('C4', (2, 3, 4, 5), 'multi_step')(_quad_c4)
t141.fixed('C1', (1, 2), [
    ('Which quadrilateral has exactly one pair of parallel sides?', 'Trapezium', 'B1 [1]', ['Parallelogram', 'Kite', 'Rhombus']),
    ('Which of these has diagonals that are equal in length but not perpendicular?', 'Rectangle (not a square)', 'B1 [1]', ['Rhombus (not a square)', 'Kite', 'Square']),
    ('Write down the sum of the interior angles of any quadrilateral.', '360°', 'B1 [1]'),
])
t141.fixed('C2', (2, 3), [
    ('Explain why a square is a special type of rectangle.', 'A rectangle has four right angles and opposite sides equal; a square has these properties and also all four sides equal.', 'B1 B1. [2]'),
])


# ----------------------------------------------------------- nets, plans and elevations
SOLIDS = [('cube', 6, 12, 8), ('cuboid', 6, 12, 8), ('triangular prism', 5, 9, 6), ('square-based pyramid', 5, 8, 5), ('tetrahedron', 4, 6, 4), ('pentagonal prism', 7, 15, 10), ('hexagonal prism', 8, 18, 12), ('hexagonal pyramid', 7, 12, 7), ('octahedron', 8, 12, 6)]
t142 = topic('Nets, plans and elevations', 'nets', 'plans and elevations', '3d shapes')
NG = {3: 'triangular', 4: 'square', 5: 'pentagonal', 6: 'hexagonal', 7: 'heptagonal', 8: 'octagonal', 10: 'decagonal'}


@t142.add('C1', (1, 2, 3))
def t142_fev(r, D):
    s, f, e, v = r.choice(SOLIDS)
    which = r.choice(['faces', 'edges', 'vertices'])
    val = {'faces': f, 'edges': e, 'vertices': v}[which]
    return MCQ(r, f'How many {which} does {art(s)} have?', str(val), [str(x) for x in (f, e, v, val + 1, val - 1, val + 2) if x != val], f'{s.capitalize()}: {f} faces, {e} edges, {v} vertices. [1]')


@t142.add('C3', (1, 2, 3, 4, 5))
def t142_n(r, D):
    n = r.choice(list(NG))
    kind = r.choice(['prism', 'pyramid'])
    if kind == 'prism':
        F, E, V = n + 2, 3 * n, 2 * n
        nm = f'{NG[n]} prism'
    else:
        F, E, V = n + 1, 2 * n, n + 1
        nm = f'{NG[n]}-based pyramid' if n != 3 else 'triangular-based pyramid'
    return Q(f'Work out the number of faces, edges and vertices of {art(nm)}, and show that they satisfy Euler\'s formula F + V − E = 2.', f'F = {F}, E = {E}, V = {V}; {F} + {V} − {E} = 2',
             f'B1 faces; B1 edges and vertices; B1 Euler check {F} + {V} − {E} = 2.', marks=3)


@t142.add('C1', (1, 2, 3))
def t142_view(r, D):
    items = [('cylinder standing on its base', 'plan', 'A circle'), ('cylinder standing on its base', 'front elevation', 'A rectangle'), ('cone standing on its base', 'front elevation', 'A triangle'),
             ('cone standing on its base', 'plan', 'A circle (with a dot at the centre)'), ('square-based pyramid', 'plan', 'A square with its diagonals'), ('triangular prism lying on a rectangular face', 'front elevation (looking at a triangular end)', 'A triangle'),
             ('sphere', 'plan', 'A circle'), ('cuboid', 'plan', 'A rectangle')]
    s, view, ans = r.choice(items)
    return MCQ(r, f'What is the {view} of a {s}?', ans, [x for x in ['A circle', 'A rectangle', 'A triangle', 'A square with its diagonals', 'A trapezium', 'A pentagon'] if x != ans], f'{ans}. [1]')


@t142.add('C2', (1, 2, 3, 4), 'explain')
def t142_net(r, D):
    s, f, e, v = r.choice(SOLIDS[:5])
    p = person(r)
    wrong = f + r.choice([1, -1])
    return Q(f'{p} draws a net of {art(s)} with {wrong} faces. Explain why this cannot be a correct net.', f'{art(s).capitalize()} has {f} faces, so its net must have exactly {f} faces.', 'B1 number of faces; B1 conclusion. [2]')


@t142.add('C2', (2, 3, 4), 'explain')
def t142_euler(r, D):
    F, V = r.randint(5, 12), r.randint(5, 12)
    E = F + V - 2 + r.choice([0, 1])
    p = person(r)
    ok = F + V - E == 2
    return Q(f'{p} says a solid with straight edges has {F} faces, {V} vertices and {E} edges. Use Euler\'s formula to decide whether this is possible.',
             f'F + V − E = {F} + {V} − {E} = {F + V - E}. ' + ('This is 2, so it is possible.' if ok else 'This is not 2, so the solid cannot exist.'), 'M1 substitution; A1 conclusion. [2]')


def _net_c4(r, D):
    l, w, h = r.randint(3, 10), r.randint(2, 8), r.randint(2, 6)
    intro = f'A cuboid measures {l} cm by {w} cm by {h} cm.'
    parts = [
        lambda r: ('Describe the net of the cuboid: how many rectangles, and of what sizes?', f'6 rectangles: two {l} × {w}, two {l} × {h}, two {w} × {h}', 'B1 count; B1 sizes [2]'),
        lambda r: ('Work out the total area of the net.', f'{2 * (l * w + l * h + w * h)} cm²', 'M1; A1 [2]'),
        lambda r: ('Describe the plan view of the cuboid when it stands on its ' + f'{l} × {w} face.', f'A rectangle {l} cm by {w} cm', 'B1 [1]'),
        lambda r: ('Describe the front elevation when viewed from the ' + f'{l} cm side.', f'A rectangle {l} cm by {h} cm', 'B1 [1]'),
        lambda r: ('Write down the number of edges and vertices.', '12 edges, 8 vertices', 'B1 [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t142.add('C4', (2, 3, 4, 5), 'multi_step')(_net_c4)
t142.fixed('C1', (1, 2), [
    ('What is the name of the view of a 3D shape seen from directly above?', 'Plan', 'B1 [1]', ['Front elevation', 'Side elevation', 'Net']),
    ('A net folds to make a closed box with two square faces and four rectangular faces. What is the shape?', 'A cuboid with square ends', 'B1 [1]', ['A cube', 'A square-based pyramid', 'A triangular prism']),
    ("Write down Euler's formula connecting faces F, vertices V and edges E.", 'F + V − E = 2', 'B1 [1]'),
])


# ----------------------------------------------------------- volume and surface area
t143 = topic('Volume and surface area of prisms and cylinders', 'volume and surface area of prisms and cylinders', 'volume', 'surface area')


@t143.add('C3', (1, 2, 3, 4, 5))
def t143_cyl(r, D):
    rad = r.choice([2, 3, 4, 5, 6, 7, 8, 10, 2.5, 3.5])
    h = r.choice([5, 8, 10, 12, 15, 20, 7.5])
    what = r.choice(['volume', 'surface area'])
    if what == 'volume':
        v = PI * rad * rad * h
        return Q(f'A cylinder has radius {N(rad)} cm and height {N(h)} cm. Calculate its volume, correct to 1 decimal place.', f'{fdp(v, 1)} cm³',
                 f'V = πr²h = π × {N(rad)}² × {N(h)} (M1) = {fdp(v, 1)} cm³ (A1).')
    sa = 2 * PI * rad * rad + 2 * PI * rad * h
    return Q(f'A closed cylinder has radius {N(rad)} cm and height {N(h)} cm. Calculate its total surface area, correct to 1 decimal place.', f'{fdp(sa, 1)} cm²',
             f'Two circles 2 × π × {N(rad)}² (M1); curved surface 2π × {N(rad)} × {N(h)} (M1); total {fdp(sa, 1)} cm² (A1).', marks=3)


@t143.add('C3', (1, 2, 3, 4, 5))
def t143_prism(r, D):
    kind = r.choice(['tri', 'trap', 'L'])
    L = r.choice([5, 8, 10, 12, 15, 20])
    if kind == 'tri':
        b, h = r.choice([(6, 4), (8, 5), (10, 6), (3, 4), (5, 12)])
        A = b * h / 2
        desc = f'a right-angled triangle with shorter sides {b} cm and {h} cm'
    elif kind == 'trap':
        a, b, h = r.choice([(4, 8, 5), (6, 10, 4), (3, 7, 6), (5, 9, 3)])
        A = (a + b) * h / 2
        desc = f'a trapezium with parallel sides {a} cm and {b} cm and height {h} cm'
    else:
        A = 5 * 4 - 3 * 2
        desc = 'an L-shape made from a 5 cm by 4 cm rectangle with a 3 cm by 2 cm rectangle removed from one corner'
    v = A * L
    return Q(f'A prism has a cross-section that is {desc}. The prism is {L} cm long. Calculate its volume.', f'{N(v)} cm³',
             f'Area of cross-section = {N(A)} cm² (M1); × {L} (M1) = {N(v)} cm³ (A1).', marks=3 if D >= 3 else 2)


@t143.add('C3', (2, 3, 4, 5))
def t143_reverse(r, D):
    rad = r.choice([3, 4, 5, 6, 10])
    V = r.choice([500, 750, 1000, 1500, 2000])
    h = V / (PI * rad * rad)
    return Q(f'A cylindrical can has radius {rad} cm and holds {V} cm³ when full. Calculate the height of the can, to 1 decimal place.', f'{fdp(h, 1)} cm',
             f'πr²h = {V} (M1); h = {V} ÷ (π × {rad}²) (M1) = {fdp(h, 1)} cm (A1).', marks=3)


@t143.add('C1', (1, 2, 3))
def t143_formula(r, D):
    items = [('the volume of any prism', 'Area of cross-section × length', ['Area of cross-section + length', 'Perimeter of cross-section × length', 'Length × width']),
             ('the volume of a cylinder', 'πr²h', ['2πrh', 'πr²', '2πr²h']), ('the curved surface area of a cylinder', '2πrh', ['πr²h', 'πrh', '2πr²']),
             ('the volume of a cube with side a', 'a³', ['6a²', '3a', 'a²'])]
    w, ans, ds = r.choice(items)
    return MCQ(r, f'Which formula gives {w}?', ans, ds, f'{ans}. [1]')


@t143.add('C2', (1, 2, 3, 4), 'explain')
def t143_err(r, D):
    rad, h = r.choice([(3, 10), (4, 6), (5, 8), (2, 15)])
    p = person(r)
    if r.random() < 0.5:
        return Q(f'{p} works out the volume of a cylinder with diameter {2 * rad} cm and height {h} cm as π × {2 * rad}² × {h}. Explain the mistake and calculate the correct volume to 1 d.p.',
                 f'The radius ({rad} cm), not the diameter, must be squared: π × {rad}² × {h} = {fdp(PI * rad * rad * h, 1)} cm³.', 'B1 radius; B1 correct volume. [2]')
    return Q(f'{p} says that the surface area of a closed cylinder of radius {rad} cm and height {h} cm is 2π × {rad} × {h}. Explain what {p} has missed.',
             f'This is only the curved surface. The two circular ends, 2 × π × {rad}², must be added: total {fdp(2 * PI * rad * h + 2 * PI * rad * rad, 1)} cm².', 'B1 ends missing; B1 correct total. [2]')


@t143.add('C2', (2, 3, 4), 'explain')
def t143_double(r, D):
    p = person(r)
    what = r.choice(['radius', 'height'])
    return Q(f'{p} doubles the {what} of a cylinder and keeps the {"height" if what == "radius" else "radius"} the same. {p} says the volume doubles. Is {p} correct? Explain.',
             ('No: V = πr²h, so doubling r multiplies the volume by 2² = 4.' if what == 'radius' else 'Yes: V = πr²h is proportional to h, so doubling h doubles the volume.'), 'B1 decision; B1 reason using the formula. [2]')


def _vol_c4(r, D):
    rad, h = r.choice([(3, 10), (4, 12), (5, 15), (3.5, 11)])
    V = PI * rad * rad * h
    boxw = 2 * rad
    intro = f'A cylindrical tin of soup has radius {N(rad)} cm and height {N(h)} cm. Tins are packed upright in a box with a base {N(4 * boxw)} cm by {N(3 * boxw)} cm and height {N(h)} cm.'
    parts = [
        lambda r: ('Calculate the volume of the tin, to the nearest cm³.', f'{round(V)} cm³', 'M1; A1 [2]'),
        lambda r: ('Calculate the area of the paper label that covers the curved surface, to 1 decimal place.', f'{fdp(2 * PI * rad * h, 1)} cm²', 'M1 2πrh; A1 [2]'),
        lambda r: ('How many millilitres of soup does the tin hold when full? (1 cm³ = 1 ml)', f'{round(V)} ml', 'B1 [1]'),
        lambda r: ('How many tins fit in one layer of the box?', '12', f'M1 {N(4 * boxw)} ÷ {N(boxw)} and {N(3 * boxw)} ÷ {N(boxw)}; A1 12 [2]'),
        lambda r: ('What percentage of the volume of the box is filled by one layer of tins? Give your answer to 1 decimal place.', f'{fdp(100 * PI / 4, 1)}%', 'M1 12V ÷ box volume; A1 [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t143.add('C4', (2, 3, 4, 5), 'multi_step')(_vol_c4)


@t143.add('C4', (3, 4, 5), 'multi_step')
def t143_pool(r, D):
    L, w, d1, d2 = r.choice([(20, 8, 1, 2), (25, 10, 1.2, 2.4), (15, 6, 0.8, 1.6)])
    A = (d1 + d2) / 2 * L
    V = A * w
    return Q(f'A swimming pool is a prism. Its cross-section is a trapezium: the pool is {L} m long, {N(d1)} m deep at the shallow end and {N(d2)} m deep at the deep end. It is {w} m wide. (a) Calculate the area of the cross-section. (b) Calculate the volume of the pool. (c) How many litres of water does it hold when full?',
             f'(a) {N(A)} m² (b) {N(V)} m³ (c) {N(V * 1000)} litres', f'(a) M1 ½({N(d1)} + {N(d2)}) × {L}; A1 [2] (b) M1 × {w}; A1 [2] (c) B1 × 1000 [1]', marks=5)


t143.fixed('C1', (1, 2), [
    ('What is the volume of a cuboid 2 cm by 3 cm by 5 cm?', '30 cm³', 'B1 [1]', ['10 cm³', '62 cm²', '31 cm³']),
    ('What is the surface area of a cube with edges 3 cm?', '54 cm²', '6 × 9. [1]', ['27 cm²', '9 cm²', '36 cm²']),
    ('Write down the unit for the volume of a prism measured in metres.', 'm³', 'B1 [1]'),
])


# ----------------------------------------------------------- planes of symmetry
t144 = topic('Planes of symmetry in 3D shapes', 'planes of symmetry', '3d symmetry')
PLANES = [('cube', '9'), ('cuboid with three different edge lengths', '3'), ('cuboid with two square faces (not a cube)', '5'), ('square-based pyramid (regular)', '4'),
          ('cylinder', 'infinitely many'), ('cone', 'infinitely many'), ('sphere', 'infinitely many'), ('triangular prism with an equilateral cross-section', '4'), ('regular tetrahedron', '6')]


@t144.add('C1', (1, 2, 3))
def t144_mcq(r, D):
    s, n = r.choice(PLANES)
    return MCQ(r, f'How many planes of symmetry does a {s} have?', n, [x for x in ['1', '2', '3', '4', '5', '6', '9', 'infinitely many'] if x != n], f'{s.capitalize()}: {n}. [1]')


@t144.add('C3', (1, 2, 3, 4, 5))
def t144_ngon(r, D):
    n = r.choice([3, 4, 5, 6, 8, 10])
    kind = r.choice(['prism', 'pyramid'])
    nm = f'{NG[n]} prism' if kind == 'prism' else f'{NG[n]}-based pyramid'
    planes = n + 1 if kind == 'prism' else n
    return Q(f'A right prism or pyramid has a regular polygon as its base. Work out the number of planes of symmetry of a regular {nm}, and explain your answer.', str(planes),
             f'Each of the {n} lines of symmetry of the regular {NG[n]} base gives a vertical plane (M1)' + (' plus one horizontal plane half way up the prism' if kind == 'prism' else '') + f'; total {planes} (A1).')


@t144.add('C2', (1, 2, 3, 4), 'explain')
def t144_explain(r, D):
    items = [('a cuboid with three different edge lengths has exactly 3 planes of symmetry', 'Each plane passes through the centre parallel to a pair of faces; diagonal planes do not work because adjacent faces are different sizes.'),
             ('a cylinder has infinitely many planes of symmetry', 'Any vertical plane through the central axis cuts it into two mirror-image halves, and there are infinitely many such planes (plus the horizontal one).'),
             ('a square-based pyramid has 4 planes of symmetry, not 5', 'The vertical planes through the apex match the 4 lines of symmetry of the square base; there is no horizontal plane because the top and bottom are different.'),
             ('a cube has more planes of symmetry than a cuboid with three different edge lengths', 'Besides the 3 planes parallel to the faces, a cube also has 6 diagonal planes through opposite edges, because all faces are squares.')]
    c, why = r.choice(items)
    p = person(r)
    return Q(f'Explain why {c}.', why, 'B1 identifies the planes; B1 explains why others do not work / why the count is as given. [2]') if r.random() < 0.6 else \
        Q(f'{p} says that {c.replace("exactly 3", "6").replace("4 planes of symmetry, not 5", "5 planes of symmetry").replace("infinitely many", "2").replace("more planes of symmetry than", "the same number of planes of symmetry as")}. Explain why {p} is wrong.', why, 'B1 correct count; B1 reason. [2]')


@t144.add('C2', (2, 3, 4), 'explain')
def t144_plane_vs_line(r, D):
    return Q(f'Explain the difference between a line of symmetry and a plane of symmetry, using {r.choice(["a square and a cube", "a rectangle and a cuboid", "a circle and a cylinder", "an isosceles triangle and a triangular prism"])} as examples.',
             'A line of symmetry divides a 2D shape into two mirror-image halves; a plane of symmetry is a flat surface that divides a 3D solid into two mirror-image halves.', 'B1 line for 2D; B1 plane for 3D with examples. [2]')


def _sym_c4(r, D):
    a, b = r.choice([(4, 4), (3, 6), (5, 5), (2, 7)])
    c = r.choice([8, 10, 12])
    sq = a == b
    intro = f'A cuboid measures {a} cm by {b} cm by {c} cm.'
    parts = [
        lambda r: ('How many planes of symmetry does it have?', '5' if sq else '3', 'B1 [1]'),
        lambda r: ('Calculate its volume and surface area.', f'{a * b * c} cm³; {2 * (a * b + a * c + b * c)} cm²', 'B1; M1 A1 [3]'),
        lambda r: ('A second cuboid has all edges equal to ' + str(a) + ' cm. How many planes of symmetry does it have?', '9', 'B1 [1]'),
        lambda r: ('Explain why your answer to the number of planes depends on whether two edges are equal.', 'Equal edges give square faces, which add diagonal planes of symmetry.', 'B1 [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t144.add('C4', (2, 3, 4, 5), 'multi_step')(_sym_c4)
t144.fixed('C1', (1, 2), [
    ('What is a plane of symmetry?', 'A flat surface that cuts a solid into two mirror-image halves', 'B1 [1]', ['A line that cuts a 2D shape in half', 'The base of a prism', 'A face of a cube']),
    ('How many planes of symmetry does a regular hexagonal prism have?', '7', '6 vertical + 1 horizontal. [1]', ['6', '12', '8']),
    ('Write down the number of planes of symmetry of a cube.', '9', 'B1 [1]'),
])

CHAPTERS[14] = [t141, t142, t143, t144]


# =================================================================== chapter 15
# Interpreting and discussing results

def fv(x):
    """Format an exact Fraction/float value (no rounding)."""
    return N(float(x))


def fd(x, dp):
    return fdp(x, dp).replace('-', MINUS)


def f1(x):
    """Exact if it terminates within 2 dp, otherwise 1 dp."""
    x = Fr(x)
    if (x * 100).denominator == 1:
        return N(float(x))
    return fd(float(x), 1)


GCTX = [
    ('{n} students recorded the time, {v} minutes, they took to travel to school.', 't', 'minutes', 'Time', 'students', (0,), (5, 10)),
    ('A post office in {c} weighed {n} parcels. The mass of each parcel is {v} kg.', 'm', 'kg', 'Mass', 'parcels', (0,), (2, 4, 5)),
    ('{p} measured the heights, {v} cm, of {n} tomato plants.', 'h', 'cm', 'Height', 'plants', (10, 20, 30), (5, 10)),
    ('An office in {c} recorded the lengths, {v} minutes, of {n} phone calls.', 'L', 'minutes', 'Length', 'calls', (0,), (5, 10)),
    ('The distances, {v} metres, of {n} javelin throws were recorded at a competition in {c}.', 'd', 'm', 'Distance', 'throws', (20, 30), (5, 10)),
    ('A farmer weighed {n} apples. The mass of each apple is {v} grams.', 'm', 'g', 'Mass', 'apples', (80, 100), (10, 20)),
    ('A weather station in {c} recorded the rainfall, {v} mm, on {n} days.', 'r', 'mm', 'Rainfall', 'days', (0,), (4, 5, 10)),
]


def gdata(r, D, k=None, ctx=None):
    sent, v, u, lab, things, starts, widths = ctx or r.choice(GCTX)
    a = r.choice(starts)
    w = r.choice(widths)
    k = k or (3 if D <= 1 else 4 if D <= 3 else 5)
    cls = [(a + i * w, a + (i + 1) * w) for i in range(k)]
    for _ in range(100):
        fs = [r.randint(2, 6 + 3 * D) for _ in range(k)]
        if fs.count(max(fs)) == 1:
            break
    n = sum(fs)
    mids = [Fr(lo + hi, 2) for lo, hi in cls]
    S = sum(m * f for m, f in zip(mids, fs))
    g = dict(v=v, u=u, lab=lab, things=things, cls=cls, fs=fs, n=n, w=w, mids=mids, S=S, mean=S / n,
             ctx=(sent, v, u, lab, things, starts, widths))
    g['sent'] = sent.format(n=n, v=v, c=city(r), p=person(r))
    g['sent'] = g['sent'][0].upper() + g['sent'][1:]
    return g


def cname(g, i):
    lo, hi = g['cls'][i]
    return f'{N(lo)} < {g["v"]} ≤ {N(hi)}'


def gtab(g, fs=None):
    fs = fs or g['fs']
    return (f'{g["lab"]} ({g["u"]}): ' + ' | '.join(cname(g, i) for i in range(len(g['cls'])))
            + '. Frequency: ' + ' | '.join(str(f) for f in fs) + '.')


def gintro(g):
    return f'{g["sent"]} The results are shown in the grouped frequency table. {gtab(g)}'


def med_class(fs):
    n = sum(fs)
    pos = [(n + 1) // 2, (n + 2) // 2]
    cum, out = 0, []
    for i, f in enumerate(fs):
        for p_ in pos:
            if cum < p_ <= cum + f:
                out.append(i)
        cum += f
    return out[0] if len(set(out)) == 1 else None


def cumf(fs):
    c, out = 0, []
    for f in fs:
        c += f
        out.append(c)
    return out


# ------------------------------------------------- frequency tables / polygons
t151 = topic('Interpreting and drawing frequency tables, frequency polygons and diagrams',
             'frequency tables', 'frequency polygons', 'grouped frequency', 'diagrams')


@t151.add('C1', (1, 2, 3))
def t151_modal(r, D):
    g = gdata(r, D, k=r.choice([4, 5]))
    i = g['fs'].index(max(g['fs']))
    return MCQ(r, gintro(g) + ' Which is the modal class?', cname(g, i), [cname(g, j) for j in range(len(g['cls'])) if j != i],
               f'Highest frequency is {max(g["fs"])}. [1]')


@t151.add('C1', (1, 2, 3))
def t151_mid(r, D):
    w = r.choice([2, 4, 5, 10, 20, 25])
    lo = w * r.randint(1, 12)
    hi = lo + w
    v = r.choice(['x', 't', 'm', 'h', 'd'])
    m = Fr(lo + hi, 2)
    return MCQ(r, f'A grouped frequency table has the class {lo} < {v} ≤ {hi}. What is the midpoint of this class?', fv(m),
               [str(lo), str(hi), str(lo + hi), str(w), fv(m + 1)], f'({lo} + {hi}) ÷ 2 = {fv(m)}. [1]')


@t151.add('C1', (1, 2, 3))
def t151_more(r, D):
    g = gdata(r, D, k=4)
    j = r.randint(1, 3)
    lo = g['cls'][j][0]
    ans = sum(g['fs'][j:])
    return Q(gintro(g) + f' How many {g["things"]} had {g["v"]} > {N(lo)}?', str(ans), f'{" + ".join(str(f) for f in g["fs"][j:])} = {ans}. B1 [1]')


t151.fixed('C1', (1, 2), [
    ('On a frequency polygon, which value of each class is used to plot the points?', 'The midpoint of the class', 'B1 [1]',
     ['The upper class boundary', 'The lower class boundary', 'The class width']),
    ('In a grouped frequency table, what is the modal class?', 'The class with the highest frequency', 'B1 [1]',
     ['The class containing the middle value', 'The class with the largest values', 'The class in the middle of the table']),
    ('Write down the midpoint of the class 20 < x ≤ 30.', '25', 'B1 [1]'),
])
t151.fixed('C2', (2, 3), [
    ('Explain why a mean worked out from a grouped frequency table is only an estimate.',
     'The exact data values are not known; each value is assumed to be at the midpoint of its class.', 'B1 values unknown; B1 midpoint assumption. [2]'),
    ('Explain why the points of a frequency polygon are plotted at the midpoints of the classes.',
     'The values in each class are spread across the class, so the midpoint is used to represent all of them.', 'B1 midpoint represents the class; B1 values unknown/spread. [2]'),
])


@t151.add('C2', (1, 2, 3, 4), 'explain')
def t151_err(r, D):
    g = gdata(r, max(D, 2))
    p = person(r)
    kind = r.choice(['classes', 'upper', 'mids'])
    if kind == 'classes':
        wrong = g['S'] / len(g['cls'])
        work = f'Σ(midpoint × frequency) = {fv(g["S"])}, then {fv(g["S"])} ÷ {len(g["cls"])} = {f1(wrong)}'
        why = f'{p} divided by the number of classes ({len(g["cls"])}) instead of the total frequency ({g["n"]}).'
    elif kind == 'upper':
        Su = sum(hi * f for (lo, hi), f in zip(g['cls'], g['fs']))
        wrong = Fr(Su, g['n'])
        work = f'Σ(upper class boundary × frequency) ÷ {g["n"]} = {Su} ÷ {g["n"]} = {f1(wrong)}'
        why = f'{p} used the upper class boundaries instead of the midpoints.'
    else:
        wrong = sum(g['mids']) / len(g['mids'])
        work = f'({" + ".join(fv(m) for m in g["mids"])}) ÷ {len(g["mids"])} = {f1(wrong)}'
        why = f'{p} found the mean of the midpoints and ignored the frequencies.'
    if f1(wrong) == fd(float(g['mean']), 1):
        return None
    return Q(gintro(g) + f' {p} estimates the mean like this: {work}. Explain {p}\'s mistake and work out a correct estimate of the mean, to 1 decimal place.',
             f'{why} Correct estimate = {fv(g["S"])} ÷ {g["n"]} = {fd(float(g["mean"]), 1)} {g["u"]}.',
             'B1 identifies the error; M1 Σ(midpoint × f) ÷ total frequency; A1 value. [3]', marks=3)


@t151.add('C2', (2, 3, 4), 'explain')
def t151_medclaim(r, D):
    g = gdata(r, D, k=5)
    mi = med_class(g['fs'])
    if mi is None:
        return None
    p = person(r)
    modal = g['fs'].index(max(g['fs']))
    if mi != 2:
        claim, reason = 2, 'it is the middle class of the table'
    elif modal != mi:
        claim, reason = modal, 'it has the highest frequency'
    else:
        return None
    pos = f'{(g["n"] + 1) // 2}th' if g['n'] % 2 else f'{g["n"] // 2}th and {g["n"] // 2 + 1}th'
    return Q(gintro(g) + f' {p} says the median is in the class {cname(g, claim)} because {reason}. Explain why {p} is wrong and find the class that contains the median.',
             f'The median is the {pos} value. Cumulative frequencies are {", ".join(str(c) for c in cumf(g["fs"]))}, so the median is in the class {cname(g, mi)}.',
             'B1 median position; M1 cumulative frequencies; A1 correct class. [3]', marks=3)


@t151.add('C2', (1, 2, 3, 4), 'explain')
def t151_polyerr(r, D):
    g = gdata(r, D, k=r.choice([3, 4]))
    p = person(r)
    pts = ', '.join(pt(hi, f) for (lo, hi), f in zip(g['cls'], g['fs']))
    good = ', '.join(f'({fv(m)}, {f})' for m, f in zip(g['mids'], g['fs']))
    return Q(gintro(g) + f' To draw a frequency polygon, {p} plots the points {pts}. Explain {p}\'s mistake and write down the points {p} should plot.',
             f'{p} used the upper class boundaries; the points should be plotted at the midpoints: {good}.', 'B1 midpoints not upper bounds; B1 correct points. [2]')


@t151.add('C2', (2, 3, 4), 'explain')
def t151_fair(r, D):
    ctx = r.choice(GCTX)
    for _ in range(200):
        g = gdata(r, D, k=4, ctx=ctx)
        nB = g['n'] + r.randint(8, 30)
        topB = g['fs'][-1] + r.randint(1, 6)
        rest = nB - topB
        if rest < 6:
            continue
        a = r.randint(1, rest - 2)
        b = r.randint(1, rest - a - 1)
        fB = [a, b, rest - a - b, topB]
        if Fr(topB, nB) < Fr(g['fs'][-1], g['n']):
            break
    else:
        return None
    p = person(r)
    pa, pb = fd(100 * g['fs'][-1] / g['n'], 1), fd(100 * topB / nB, 1)
    return Q(f'Data were collected for two groups, A and B. {g["lab"]} ({g["u"]}): ' + ' | '.join(cname(g, i) for i in range(4))
             + f'. Group A frequency: {" | ".join(map(str, g["fs"]))}. Group B frequency: {" | ".join(map(str, fB))}. '
             f'{p} says that a greater proportion of group B is in the top class because {topB} > {g["fs"][-1]}. Explain why {p} is wrong.',
             f'The groups are different sizes ({g["n"]} and {nB}), so compare proportions: A {g["fs"][-1]}/{g["n"]} = {pa}%, B {topB}/{nB} = {pb}%. Group A has the greater proportion.',
             'B1 different totals; M1 converts to proportions or percentages; A1 correct conclusion. [3]', marks=3)


@t151.add('C3', (1, 2, 3, 4, 5))
def t151_mean(r, D):
    g = gdata(r, D)
    mids = ', '.join(fv(m) for m in g['mids'])
    ans = fd(float(g['mean']), 1)
    key = f'M1 midpoints {mids}; M1 Σfx = {fv(g["S"])}; M1 ÷ {g["n"]}; A1 {ans}.'
    stem = gintro(g) + f' Calculate an estimate of the mean {g["lab"].lower()}. Give your answer to 1 decimal place.'
    if D == 1:
        Su = sum(hi * f for (lo, hi), f in zip(g['cls'], g['fs']))
        return MCQ(r, stem, ans, [fd(float(g['S'] / len(g['cls'])), 1), fd(Su / g['n'], 1), fd(float(sum(g['mids']) / len(g['mids'])), 1),
                                  fd(float(g['mean']) + g['w'] / 2, 1)], key)
    return Q(stem, f'{ans} {g["u"]}', key)


@t151.add('C3', (1, 2, 3, 4, 5))
def t151_median(r, D):
    for _ in range(30):
        g = gdata(r, D, k=4 if D <= 2 else 5)
        mi = med_class(g['fs'])
        if mi is not None:
            break
    else:
        return None
    stem = gintro(g) + ' Find the class that contains the median.'
    key = f'M1 median is value number {fv(Fr(g["n"] + 1, 2))}; M1 cumulative frequencies {", ".join(map(str, cumf(g["fs"])))}; A1 {cname(g, mi)}.'
    if D >= 4:
        mo = g['fs'].index(max(g['fs']))
        return Q(gintro(g) + ' Write down the modal class and find the class that contains the median.',
                 f'Modal class {cname(g, mo)}; median class {cname(g, mi)}', 'B1 modal class; ' + key, marks=4)
    return Q(stem, cname(g, mi), key)


@t151.add('C3', (1, 2, 3, 4, 5))
def t151_points(r, D):
    g = gdata(r, D)
    good = ', '.join(f'({fv(m)}, {f})' for m, f in zip(g['mids'], g['fs']))
    extra = ''
    ans = good
    if D >= 3:
        extra = ' Then write down the modal class.'
        ans += f'; modal class {cname(g, g["fs"].index(max(g["fs"])))}'
    return Q(gintro(g) + f' {g["lab"]} is to be shown on a frequency polygon. Write down the coordinates of the points that should be plotted.' + extra,
             ans, 'M1 midpoints as x-coordinates; A1 all points correct' + ('; B1 modal class.' if D >= 3 else '.'))


@t151.add('C3', (2, 3, 4, 5))
def t151_pct(r, D):
    g = gdata(r, D)
    k = len(g['cls'])
    if D >= 4:
        a = r.randint(0, k - 3)
        b = r.randint(a + 1, k - 1)
        cnt = sum(g['fs'][a:b + 1])
        cond = f'{N(g["cls"][a][0])} < {g["v"]} ≤ {N(g["cls"][b][1])}'
    else:
        a = r.randint(1, k - 1)
        cnt = sum(g['fs'][a:])
        cond = f'{g["v"]} > {N(g["cls"][a][0])}'
    pc = 100 * Fr(cnt, g['n'])
    return Q(gintro(g) + f' What percentage of the {g["things"]} had {cond}? Give your answer to 1 decimal place where necessary.',
             f'{f1(pc)}%', f'M1 {cnt} ÷ {g["n"]}; M1 × 100; A1 {f1(pc)}%.')


@t151.add('C3', (3, 4, 5))
def t151_missing(r, D):
    ctx = r.choice(GCTX)
    for _ in range(300):
        g = gdata(r, D, k=4 if D < 5 else 5, ctx=ctx)
        if (g['mean'] * 10).denominator == 1:
            break
    else:
        return None
    j = r.randrange(len(g['cls']))
    if g['mids'][j] == g['mean']:
        return None
    fs = [str(f) if i != j else 'f' for i, f in enumerate(g['fs'])]
    tab = gtab(g, fs)
    n0 = g['n'] - g['fs'][j]
    S0 = g['S'] - g['mids'][j] * g['fs'][j]
    sent = g['ctx'][0].format(n='some', v=g['v'], c=city(r), p=person(r))
    sent = sent[0].upper() + sent[1:]
    return Q(f'{sent} {tab} An estimate of the mean is {fv(g["mean"])} {g["u"]}. Work out the value of f.',
             str(g['fs'][j]), f'M1 ({fv(S0)} + {fv(g["mids"][j])}f) ÷ ({n0} + f) = {fv(g["mean"])}; M1 rearranges; A1 f = {g["fs"][j]}.', marks=4)


def _freq_c4(r, D):
    for _ in range(30):
        g = gdata(r, D, k=5)
        mi = med_class(g['fs'])
        if mi is not None:
            break
    else:
        return None
    mo = g['fs'].index(max(g['fs']))
    a = r.randint(2, 4)
    cnt = sum(g['fs'][a:])
    parts = [
        lambda r: ('Write down the modal class.', cname(g, mo), 'B1 [1]'),
        lambda r: ('Calculate an estimate of the mean, to 1 decimal place.', f'{fd(float(g["mean"]), 1)} {g["u"]}', f'M1 midpoints; M1 Σfx = {fv(g["S"])}; M1 ÷ {g["n"]}; A1 [4]'),
        lambda r: ('Find the class that contains the median.', cname(g, mi), 'M1 cumulative frequencies; A1 [2]'),
        lambda r: (f'Work out the percentage of the {g["things"]} with {g["v"]} > {N(g["cls"][a][0])}, to 1 decimal place where necessary.', f'{f1(100 * Fr(cnt, g["n"]))}%', f'M1 {cnt} ÷ {g["n"]} × 100; A1 [2]'),
        lambda r: ('Write down the coordinates of the first two points you would plot on a frequency polygon.', f'({fv(g["mids"][0])}, {g["fs"][0]}), ({fv(g["mids"][1])}, {g["fs"][1]})', 'B1 midpoints; B1 frequencies [2]'),
        lambda r: ('Explain why the mean can only be estimated from this table.', 'The exact values are not known; the midpoints are used to represent each class.', 'B1 [1]'),
    ]
    return compose(r, gintro(g), parts, k=(2, 3, 4), type_='multi_step')


t151.add('C4', (2, 3, 4, 5), 'multi_step')(_freq_c4)


@t151.add('C4', (3, 4, 5), 'multi_step')
def t151_two(r, D):
    ctx = r.choice(GCTX)
    gA = gdata(r, D, k=4, ctx=ctx)
    for _ in range(50):
        fB = [r.randint(2, 6 + 3 * D) for _ in range(4)]
        if fB.count(max(fB)) == 1:
            break
    nB = sum(fB)
    SB = sum(m * f for m, f in zip(gA['mids'], fB))
    mA, mB = fd(float(gA['mean']), 1), fd(float(SB / nB), 1)
    if mA == mB:
        return None
    a, b = r.choice([('the morning', 'the afternoon'), ('last year', 'this year'), ('March', 'September'), ('the first week', 'the second week')])
    hiA = float(gA['mean']) > float(SB / nB)
    moA, moB = cname(gA, gA['fs'].index(max(gA['fs']))), cname(gA, fB.index(max(fB)))
    return Q(f'Two sets of data were collected, one in {a} and one in {b}. {gA["lab"]} ({gA["u"]}): ' + ' | '.join(cname(gA, i) for i in range(4))
             + f'. Frequency in {a}: {" | ".join(map(str, gA["fs"]))}. Frequency in {b}: {" | ".join(map(str, fB))}. '
             f'(a) Calculate an estimate of the mean for each set of data, to 1 decimal place. (b) Write down the modal class for each set of data. (c) Compare the two distributions.',
             f'(a) {a}: {mA} {gA["u"]}; {b}: {mB} {gA["u"]} (b) {a}: {moA}; {b}: {moB} (c) On average the values were greater in {a if hiA else b} (higher estimated mean).',
             f'(a) M1 midpoints; M1 Σfx ÷ n for one set; A1 A1 [4] (b) B1 B1 [2] (c) B1 comparison of averages in context [1]', marks=7)


t151.fixed('C1', (1, 2), [
    ('A grouped frequency table has classes 0 < t ≤ 10, 10 < t ≤ 20 and 20 < t ≤ 30. In which class does the value 20 belong?', '10 < t ≤ 20', 'B1 [1]',
     ['0 < t ≤ 10', '20 < t ≤ 30', 'Both 10 < t ≤ 20 and 20 < t ≤ 30']),
])


# ------------------------------------------------------------- time series
t152 = topic('Time series graphs and moving trends', 'time series graphs', 'moving averages', 'trends')

QCTX = [
    ('A sportswear shop in {c} records its sales, in thousands of dollars, each quarter.', 'sales'),
    ('A museum in {c} records the number of visitors, in hundreds, each quarter.', 'visitor numbers'),
    ('A school in {c} records the electricity it uses, in hundreds of kWh, each quarter.', 'electricity use'),
    ('A hotel in {c} records the number of nights booked, in hundreds, each quarter.', 'bookings'),
    ('A garden centre in {c} records its sales, in thousands of dollars, each quarter.', 'sales'),
]
WCTX = [
    ('A school records the number of students absent each week for {m} weeks.', 'absences'),
    ('A bakery in {c} records the number of loaves it sells each week for {m} weeks.', 'loaf sales'),
    ('A cinema in {c} records the number of tickets sold each week for {m} weeks.', 'ticket sales'),
    ('A website records the number of downloads, in hundreds, each week for {m} weeks.', 'downloads'),
]


def mav(vals, k):
    return [Fr(sum(vals[i:i + k]), k) for i in range(len(vals) - k + 1)]


def qseries(r, years, t=None, seasonal_ok=None):
    for _ in range(200):
        t = t if t is not None else r.choice([1, 2, 3, -1, -2])
        b = r.randint(30, 60) + (30 if t < 0 else 0)
        s = [r.randint(-9, 9) for _ in range(3)]
        s.append(-sum(s))
        if abs(s[3]) > 12 or max(s) - min(s) < 8:
            continue
        vals = [b + t * i + s[i % 4] + r.choice([-1, 0, 0, 1]) for i in range(4 * years)]
        if min(vals) < 5:
            continue
        if seasonal_ok and not seasonal_ok(vals):
            continue
        return vals, t
    return None, t


def wseries(r, m):
    t = r.choice([2, 3, 4, -2, -3])
    b = r.randint(40, 90) + (30 if t < 0 else 0)
    vals = [b + t * i + r.randint(-4, 4) for i in range(m)]
    return vals, t


def qtext(vals, y0):
    rows = []
    for y in range(len(vals) // 4):
        rows.append(f'{y0 + y}: Q1 {vals[4 * y]}, Q2 {vals[4 * y + 1]}, Q3 {vals[4 * y + 2]}, Q4 {vals[4 * y + 3]}')
    return '; '.join(rows) + '.'


def wtext(vals):
    return ', '.join(f'week {i + 1}: {v}' for i, v in enumerate(vals)) + '.'


def trend_word(ms):
    return 'upward (increasing)' if ms[-1] > ms[0] else 'downward (decreasing)'


@t152.add('C1', (1, 2, 3))
def t152_first(r, D):
    k = r.choice([3, 4])
    if k == 4:
        vals, _ = qseries(r, 2)
        if vals is None:
            return None
        ctx = r.choice(QCTX)[0].format(c=city(r))
        data = qtext(vals, r.randint(2019, 2023))
    else:
        vals, _ = wseries(r, 6)
        ctx = r.choice(WCTX)[0].format(c=city(r), m=6)
        data = wtext(vals)
    m = Fr(sum(vals[:k]), k)
    stem = f'{ctx} {data} Work out the first {k}-point moving average.' + (' Give your answer to 1 decimal place.' if k == 3 else '')
    fm = (lambda x: fd(float(x), 1)) if k == 3 else fv
    cands = [Fr(sum(vals[:k])), Fr(sum(vals[:k]), k - 1), Fr(sum(vals[1:k + 1]), k), Fr(sum(vals[:k + 1]), k + 1), m + 2, m - 2]
    cands = [fm(x) for x in cands if abs(x - m) >= Fr(1, 2)]
    return MCQ(r, stem, fm(m), cands,
               f'({" + ".join(map(str, vals[:k]))}) ÷ {k} = {fm(m)}. [1]')


PERIODS = [
    ('the number of customers at a café, open every day of the week, each day for 6 weeks', '7-point'),
    ('the sales of a shop each quarter for 3 years', '4-point'),
    ('the rainfall in {c} each month for 4 years', '12-point'),
    ('the attendance at a school, open 5 days a week, each school day for 8 weeks', '5-point'),
    ('the number of visitors to a park in {c} each quarter from 2021 to 2024', '4-point'),
    ('the electricity used by a factory in {c} each month for 3 years', '12-point'),
    ('the number of tickets sold at a cinema in {c} each day for 5 weeks', '7-point'),
    ('the number of passengers using a train station in {c} each quarter for 5 years', '4-point'),
    ('the mean monthly temperature in {c} for 6 years', '12-point'),
]


@t152.add('C1', (1, 2, 3))
def t152_period(r, D):
    ctx, ans = r.choice(PERIODS)
    p = person(r)
    return MCQ(r, f'{p} has data for {ctx.format(c=city(r))}. Which moving average is most suitable for showing the trend?', ans,
               [x for x in ['3-point', '4-point', '5-point', '7-point', '12-point'] if x != ans],
               f'One full cycle of the pattern contains {ans.split("-")[0]} values. [1]')


@t152.add('C1', (1, 2, 3))
def t152_trend(r, D):
    kind = r.choice(['up', 'down', 'flat'])
    b = Fr(r.randint(120, 400), 4)
    ms = [b]
    for _ in range(r.randint(3, 5)):
        step = Fr(r.randint(1, 6), 4)
        if kind == 'up':
            ms.append(ms[-1] + step)
        elif kind == 'down':
            ms.append(ms[-1] - step)
        else:
            ms.append(b + Fr(r.choice([-1, 0, 1]), 4))
    if kind == 'flat' and len(set(ms)) == 1:
        ms[-1] += Fr(1, 4)
    ans = {'up': 'The trend is upward (increasing)', 'down': 'The trend is downward (decreasing)', 'flat': 'There is no clear upward or downward trend'}[kind]
    return MCQ(r, f'The 4-point moving averages for a set of quarterly data are {", ".join(fv(x) for x in ms)}. Which statement best describes the trend?', ans,
               [x for x in ['The trend is upward (increasing)', 'The trend is downward (decreasing)', 'There is no clear upward or downward trend'] if x != ans]
               + ['The data have no seasonal variation'], 'Look at how the moving averages change. [1]')


t152.fixed('C1', (1, 2), [
    ('On a time series graph, what is plotted on the horizontal axis?', 'Time', 'B1 [1]', ['Frequency', 'The moving average', 'The trend']),
    ('What does a moving average help to show?', 'The trend of the data, with seasonal variation smoothed out', 'B1 [1]',
     ['The highest value in each year', 'The mode of the data', 'The exact value of the next data point']),
    ('Write down how many values are added together to work out each 4-point moving average.', '4', 'B1 [1]'),
])
t152.fixed('C2', (2, 3), [
    ('Explain why each moving average is plotted at the middle of the time period it covers.',
     'The moving average represents all the values in that period, so it is plotted at the centre of the period.', 'B1 represents the whole period; B1 centre. [2]'),
    ('Explain the difference between the trend and the seasonal variation in a time series.',
     'The trend is the general long-term direction of the data; seasonal variation is a pattern that repeats in every cycle (for example each year).', 'B1 trend; B1 seasonal. [2]'),
])


@t152.add('C2', (1, 2, 3, 4), 'explain')
def t152_err(r, D):
    vals, _ = qseries(r, 2)
    if vals is None:
        return None
    ctx = r.choice(QCTX)[0].format(c=city(r))
    y0 = r.randint(2019, 2023)
    p = person(r)
    if r.random() < 0.5:
        wrong = Fr(sum(vals[:4]), 3)
        return Q(f'{ctx} {qtext(vals, y0)} {p} works out the first 4-point moving average as ({" + ".join(map(str, vals[:4]))}) ÷ 3 = {fd(float(wrong), 2)}. Explain the mistake and give the correct value.',
                 f'Four values are added, so {p} should divide by 4: {sum(vals[:4])} ÷ 4 = {fv(Fr(sum(vals[:4]), 4))}.', 'B1 divide by 4; B1 correct value. [2]')
    second = Fr(sum(vals[1:5]), 4)
    return Q(f'{ctx} {qtext(vals, y0)} {p} says the second 4-point moving average uses the four quarters of {y0 + 1}. Explain why {p} is wrong and work out the second 4-point moving average.',
             f'Moving averages overlap: each one moves on by one quarter, so the second uses Q2 to Q4 of {y0} and Q1 of {y0 + 1}: ({" + ".join(map(str, vals[1:5]))}) ÷ 4 = {fv(second)}.',
             'B1 overlapping values; B1 correct value. [2]')


@t152.add('C2', (2, 3, 4), 'explain')
def t152_claim(r, D):
    vals, _ = qseries(r, 2, t=r.choice([1, 2, 3]), seasonal_ok=lambda v: v[7] < v[6] and v[3] < v[2] and v[7] > v[3])
    if vals is None:
        return None
    ctx = r.choice(QCTX)[0].format(c=city(r))
    y0 = r.randint(2019, 2023)
    p = person(r)
    ms = mav(vals, 4)
    return Q(f'{ctx} {qtext(vals, y0)} {p} says: "The values fell from Q3 to Q4 of {y0 + 1}, so the long-term trend is downward." Explain why {p} is wrong.',
             f'The fall from Q3 to Q4 also happened in {y0}, so it is seasonal variation. Q4 {y0 + 1} ({vals[7]}) is higher than Q4 {y0} ({vals[3]}), and the 4-point moving averages rise from {fv(ms[0])} to {fv(ms[-1])}, so the trend is upward.',
             'B1 seasonal pattern; B1 evidence of upward trend (same-quarter comparison or moving averages). [2]')


@t152.add('C2', (1, 2, 3, 4), 'explain')
def t152_why4(r, D):
    ctx = r.choice(QCTX)[0].format(c=city(r))
    y0 = r.randint(2015, 2022)
    yrs = r.randint(2, 5)
    return Q(f'{ctx} The data cover {y0} to {y0 + yrs - 1}. Explain why a 4-point moving average, rather than a 3-point moving average, should be used to show the trend.',
             'There are four quarters in a year, so each 4-point moving average contains every season exactly once; this removes the seasonal variation and shows the trend.',
             'B1 four quarters in a cycle; B1 removes seasonal effect. [2]')


@t152.add('C3', (1, 2, 3, 4, 5))
def t152_ma(r, D):
    if D <= 2:
        m = 5 if D == 1 else 7
        vals, t = wseries(r, m)
        ctx = r.choice(WCTX)[0].format(c=city(r), m=m)
        ms = mav(vals, 3)
        ans = ', '.join(fd(float(x), 1) for x in ms)
        return Q(f'{ctx} {wtext(vals)} Calculate the 3-point moving averages. Give your answers to 1 decimal place.', ans,
                 f'M1 ({vals[0]} + {vals[1]} + {vals[2]}) ÷ 3; A1 all {len(ms)} correct.')
    vals, t = qseries(r, 3 if D == 5 else 2)
    if vals is None:
        return None
    ctx = r.choice(QCTX)[0].format(c=city(r))
    ms = mav(vals, 4)
    ans = ', '.join(fv(x) for x in ms)
    stem = f'{ctx} {qtext(vals, r.randint(2018, 2022))} Calculate the 4-point moving averages.'
    key = f'M1 ({" + ".join(map(str, vals[:4]))}) ÷ 4; A1 all {len(ms)} correct'
    if D >= 4:
        stem += ' Use them to describe the trend.'
        ans += f'. The trend is {trend_word(ms)}.'
        key += '; B1 trend'
    return Q(stem, ans, key + '.')


@t152.add('C3', (2, 3, 4, 5))
def t152_missing(r, D):
    p = person(r)
    if D <= 3:
        a, b = r.randint(20, 80), r.randint(20, 80)
        x = r.randint(20, 80)
        x += (-(a + b + x)) % 3
        m = (a + b + x) // 3
        return Q(f'{p} records the number of emails received on three days: {a}, {b} and an unknown number x. The 3-point moving average for these days is {m}. Work out x.',
                 str(x), f'M1 3 × {m} = {3 * m}; M1 {3 * m} − {a} − {b}; A1 {x}.')
    vals, _ = qseries(r, 2)
    if vals is None:
        return None
    j = r.randrange(4)
    m = Fr(sum(vals[:4]), 4)
    ctx = r.choice(QCTX)[0].format(c=city(r))
    y0 = r.randint(2019, 2023)
    shown = ', '.join(f'Q{i + 1} {vals[i] if i != j else "x"}' for i in range(4))
    nxt = ''
    ans = str(vals[j])
    key = f'M1 4 × {fv(m)} = {sum(vals[:4])}; M1 subtract the other three values; A1 {vals[j]}'
    if D == 5:
        nxt = f' Q1 of {y0 + 1} is {vals[4]}. Work out the second 4-point moving average.'
        ans += f'; {fv(Fr(sum(vals[1:5]), 4))}'
        key += f'; M1 A1 second moving average {fv(Fr(sum(vals[1:5]), 4))}'
    return Q(f'{ctx} In {y0}: {shown}. The first 4-point moving average is {fv(m)}. Work out x.' + nxt, ans, key + '.')


@t152.add('C3', (3, 4, 5))
def t152_change(r, D):
    vals, t = qseries(r, 3 if D == 5 else 2)
    if vals is None:
        return None
    ms = mav(vals, 4)
    ch = (ms[-1] - ms[0]) / (len(ms) - 1)
    ctx = r.choice(QCTX)[0].format(c=city(r))
    return Q(f'{ctx} The 4-point moving averages are {", ".join(fv(x) for x in ms)}. Work out the mean change in the moving average per quarter, to 2 decimal places, and describe the trend.',
             f'{fd(float(ch), 2)} per quarter; the trend is {trend_word(ms)}.', f'M1 ({fv(ms[-1])} − {fv(ms[0])}) ÷ {len(ms) - 1}; A1 {fd(float(ch), 2)}; B1 trend.', marks=3)


def _ts_c4(r, D):
    vals, t = qseries(r, 2)
    if vals is None:
        return None
    ctx = r.choice(QCTX)[0].format(c=city(r))
    y0 = r.randint(2019, 2023)
    ms = mav(vals, 4)
    hiq = [max(range(4), key=lambda i: vals[4 * y + i]) for y in range(2)]
    parts = [
        lambda r: ('Calculate the 4-point moving averages.', ', '.join(fv(x) for x in ms), f'M1 first ({" + ".join(map(str, vals[:4]))}) ÷ 4; A2 all correct (A1 for 3 correct) [3]'),
        lambda r: ('Use the moving averages to describe the trend.', f'The trend is {trend_word(ms)}.', 'B1 [1]'),
        lambda r: (f'Explain why a 4-point moving average is suitable for these data.', 'There are four quarters in a year, so each moving average includes every season once.', 'B1 [1]'),
        lambda r: (f'Work out the difference between the first and last 4-point moving averages.', fv(abs(ms[-1] - ms[0])), f'M1 {fv(ms[-1])} − {fv(ms[0])}; A1 [2]'),
        (lambda r: ('Write down the quarter with the highest value in each year, and say what this suggests about the data.',
                    f'Q{hiq[0] + 1} in both years; there is a seasonal pattern.', 'B1 quarter; B1 seasonal [2]')) if hiq[0] == hiq[1] else (lambda r: None),
    ]
    return compose(r, f'{ctx} {qtext(vals, y0)}', parts, k=(2, 3), type_='multi_step')


t152.add('C4', (2, 3, 4, 5), 'multi_step')(_ts_c4)


@t152.add('C4', (2, 3, 4, 5), 'multi_step')
def t152_weekly(r, D):
    m = 8 if D <= 3 else 10
    vals, t = wseries(r, m)
    ctx = r.choice(WCTX)[0].format(c=city(r), m=m)
    ms = mav(vals, 3)
    nxt = vals[-1] + t + r.randint(-3, 3)
    nm = Fr(vals[-2] + vals[-1] + nxt, 3)
    return Q(f'{ctx} {wtext(vals)} (a) Calculate the 3-point moving averages, to 1 decimal place. (b) Describe the trend. (c) In week {m + 1} the value is {nxt}. Work out the next 3-point moving average, to 1 decimal place.',
             f'(a) {", ".join(fd(float(x), 1) for x in ms)} (b) The trend is {trend_word(ms)}. (c) {fd(float(nm), 1)}',
             f'(a) M1 first average ({vals[0]} + {vals[1]} + {vals[2]}) ÷ 3; A2 all correct [3] (b) B1 [1] (c) M1 ({vals[-2]} + {vals[-1]} + {nxt}) ÷ 3; A1 [2]', marks=6)


# ---------------------------------------------- stem-and-leaf diagrams
t153 = topic('Stem-and-leaf diagrams and comparing distributions', 'stem-and-leaf diagrams', 'comparing distributions', 'back-to-back')

SLCTX = [
    ('the times, in seconds, taken by {n} students to run 200 m', 'seconds', (2, 5), False),
    ('the marks scored by {n} students in a science test', 'marks', (1, 5), False),
    ('the masses, in kg, of {n} suitcases checked in at {c} airport', 'kg', (1, 3), False),
    ('the lengths, in cm, of {n} leaves collected by {p}', 'cm', (2, 6), True),
    ('the lengths, in cm, of {n} fish caught in a lake', 'cm', (1, 4), False),
    ('the ages of {n} people at a sports club in {c}', 'years', (1, 6), False),
    ('the heights, in m, of {n} young trees in a park in {c}', 'm', (1, 4), True),
    ('the numbers of goals scored by a hockey club in {n} seasons', 'goals', (2, 5), False),
]


def sldata(r, n, ctx=None):
    desc, u, (s0, s1), dec = ctx or r.choice(SLCTX)
    lo, hi = s0 * 10, s1 * 10 + 9
    vals = sorted(r.randint(lo, hi) for _ in range(n))
    return dict(vals=vals, u=u, dec=dec, desc=desc.format(n=n, c=city(r), p=person(r)), ctx=(desc, u, (s0, s1), dec))


def slv(d, x):
    return N(x / 10) if d['dec'] else N(x)


def sltext(d, vals=None):
    vals = vals or d['vals']
    rows = []
    for s in range(min(vals) // 10, max(vals) // 10 + 1):
        lv = ' '.join(str(v % 10) for v in vals if v // 10 == s)
        rows.append(f'{s} | {lv}'.rstrip())
    k = vals[len(vals) // 2]
    return '; '.join(rows) + f'. Key: {k // 10} | {k % 10} means {slv(d, k)} {d["u"]}'


def sl_intro(d):
    return f'The stem-and-leaf diagram shows {d["desc"]}. {sltext(d)}.'


def median(vals):
    n = len(vals)
    return Fr(vals[n // 2]) if n % 2 else Fr(vals[n // 2 - 1] + vals[n // 2], 2)


def mval(d, x):
    return N(float(x) / 10) if d['dec'] else fv(x)


def slmode(vals):
    c = {v: vals.count(v) for v in vals}
    m = max(c.values())
    ms = [v for v in c if c[v] == m]
    return ms[0] if m >= 2 and len(ms) == 1 else None


@t153.add('C1', (1, 2, 3))
def t153_read(r, D):
    dec = r.random() < 0.5
    s, l = r.randint(1, 8), r.randint(0, 9)
    s2, l2 = r.randint(1, 9), r.randint(1, 9)
    if (s2, l2) == (s, l) or s2 == l2:
        return None
    u = r.choice(['cm', 'kg', 'seconds', 'm'])
    v = (lambda a, b: N((10 * a + b) / 10)) if dec else (lambda a, b: str(10 * a + b))
    ans = v(s2, l2)
    c = [str(10 * l2 + s2), N((10 * s2 + l2) / 10) if not dec else str(10 * s2 + l2), str(s2 + l2), N((10 * l2 + s2) / 10)]
    return MCQ(r, f'In a stem-and-leaf diagram, the key is {s} | {l} means {v(s, l)} {u}. What value does {s2} | {l2} represent?', f'{ans} {u}',
               [f'{x} {u}' for x in c], f'Stem {s2}, leaf {l2}: {ans} {u}. [1]')


@t153.add('C1', (1, 2, 3))
def t153_range(r, D):
    d = sldata(r, r.randint(7, 10), ctx=r.choice([c for c in SLCTX if not c[3]]))
    v = d['vals']
    rg = v[-1] - v[0]
    c = [str(v[-1]), str(abs(v[-1] % 10 - v[0] % 10)), str((v[-1] // 10 - v[0] // 10) * 10), str(rg + 1), str(v[-1] - v[1])]
    return MCQ(r, sl_intro(d) + ' What is the range?', str(rg), c, f'{v[-1]} − {v[0]} = {rg}. [1]')


@t153.add('C1', (1, 2, 3))
def t153_mode(r, D):
    for _ in range(50):
        d = sldata(r, r.randint(9, 13))
        mo = slmode(d['vals'])
        if mo is not None:
            break
    else:
        return None
    return Q(sl_intro(d) + ' Write down the mode.', f'{slv(d, mo)} {d["u"]}', f'{slv(d, mo)} appears most often. B1 [1]')


t153.fixed('C1', (1, 2), [
    ('In a stem-and-leaf diagram, how should the leaves in each row be written?', 'In order, from smallest to largest', 'B1 [1]',
     ['In the order the data were collected', 'From largest to smallest', 'In any order']),
    ('Which of these is a measure of spread?', 'The range', 'B1 [1]', ['The median', 'The mode', 'The mean']),
    ('Write down the number of values shown in this stem-and-leaf diagram: 1 | 2 4; 2 | 0 5 8; 3 | 1.', '6', 'B1 [1]'),
])
t153.fixed('C2', (2, 3), [
    ('Explain why a stem-and-leaf diagram must have a key.', 'Without a key you cannot tell what the stem and leaf represent, for example whether 3 | 4 means 34 or 3.4.', 'B1 meaning of values; B1 example. [2]'),
    ('Explain one advantage of a stem-and-leaf diagram compared with a grouped frequency table.', 'It keeps the original data values, so the exact median, mode and range can be found.', 'B1 original data kept; B1 exact statistics. [2]'),
])


@t153.add('C2', (1, 2, 3, 4), 'explain')
def t153_err(r, D):
    d = sldata(r, r.choice([9, 11, 13]), ctx=r.choice([c for c in SLCTX if not c[3]]))
    v = d['vals']
    p = person(r)
    if r.random() < 0.5:
        wrong = max(x % 10 for x in v) - min(x % 10 for x in v)
        if wrong == v[-1] - v[0]:
            return None
        return Q(sl_intro(d) + f' {p} says the range is {wrong} because the largest leaf is {max(x % 10 for x in v)} and the smallest leaf is {min(x % 10 for x in v)}. Explain {p}\'s mistake and find the correct range.',
                 f'The range uses the largest and smallest data values, not the leaves: {v[-1]} − {v[0]} = {v[-1] - v[0]} {d["u"]}.', 'B1 uses values not leaves; B1 correct range. [2]')
    stems = list(range(v[0] // 10, v[-1] // 10 + 1))
    ms = stems[len(stems) // 2]
    row = [x for x in v if x // 10 == ms]
    if not row:
        return None
    wrong = row[len(row) // 2]
    if wrong == v[len(v) // 2]:
        return None
    return Q(sl_intro(d) + f' {p} says the median is {wrong}, the middle leaf of the middle row. Explain {p}\'s mistake and find the correct median.',
             f'The median is the middle value of all {len(v)} values, the {(len(v) + 1) // 2}th value when counted in order: {v[len(v) // 2]} {d["u"]}.', 'B1 counts all values; B1 correct median. [2]')


@t153.add('C2', (2, 3, 4), 'explain')
def t153_claim(r, D):
    a, b = two_people(r)
    subj = r.choice(['test marks', 'times to complete a puzzle (seconds)', 'scores in a quiz', 'distances jumped (cm)'])
    mA, mB = r.randint(30, 70), r.randint(30, 70)
    rA, rB = r.randint(10, 40), r.randint(10, 40)
    if mA == mB or abs(rA - rB) < 4:
        return None
    hi = 'A' if mA > mB else 'B'
    lo_r = 'A' if rA < rB else 'B'
    wrong = 'B' if lo_r == 'A' else 'A'
    return Q(f'Two groups were compared using their {subj}. Group A: median {mA}, range {rA}. Group B: median {mB}, range {rB}. {a} says group {hi} is more consistent because its median is higher. Explain why {a} is wrong.'
             if hi != lo_r else
             f'Two groups were compared using their {subj}. Group A: median {mA}, range {rA}. Group B: median {mB}, range {rB}. {a} says group {wrong} is more consistent because its range is larger. Explain why {a} is wrong.',
             f'Consistency is measured by the spread, not the average. Group {lo_r} has the smaller range ({min(rA, rB)}), so group {lo_r} is more consistent.',
             'B1 consistency means spread/range; B1 correct group with evidence. [2]')


@t153.add('C2', (1, 2, 3), 'explain')
def t153_order(r, D):
    p = person(r)
    s = r.randint(1, 8)
    leaves = [r.randint(0, 9) for _ in range(r.randint(4, 6))]
    if leaves == sorted(leaves):
        return None
    return Q(f'{p} draws one row of a stem-and-leaf diagram as {s} | {" ".join(map(str, leaves))}. Explain what is wrong with this row and write it correctly.',
             f'The leaves must be in order from smallest to largest: {s} | {" ".join(map(str, sorted(leaves)))}.', 'B1 leaves in order; B1 correct row. [2]')


@t153.add('C3', (1, 2, 3, 4, 5))
def t153_stats(r, D):
    n = {1: r.choice([7, 9]), 2: r.choice([10, 12]), 3: r.choice([11, 13, 15]), 4: r.choice([12, 14]), 5: r.choice([13, 15, 16])}[D]
    ctx = r.choice([c for c in SLCTX if c[3] == (D == 4)])
    d = sldata(r, n, ctx=ctx)
    v = d['vals']
    md = median(v)
    stem = sl_intro(d) + ' Find the median and the range.'
    ans = f'Median {mval(d, md)} {d["u"]}; range {slv(d, v[-1] - v[0])} {d["u"]}'
    key = f'M1 median is value number {fv(Fr(n + 1, 2))}; A1 {mval(d, md)}; B1 range {slv(d, v[-1] - v[0])}'
    if D == 5:
        mean = Fr(sum(v), n) / (10 if d['dec'] else 1)
        stem = sl_intro(d) + ' Find the median, the range and the mean (to 1 decimal place).'
        ans += f'; mean {fd(float(mean), 1)} {d["u"]}'
        key += f'; M1 sum ÷ {n}; A1 mean {fd(float(mean), 1)}'
    return Q(stem, ans, key + '.', marks=None if D < 5 else 5)


@t153.add('C3', (1, 2, 3, 4, 5))
def t153_draw(r, D):
    n = 8 + 2 * D
    d = sldata(r, n, ctx=r.choice([c for c in SLCTX if c[3] == (D >= 4)]))
    raw = d['vals'][:]
    r.shuffle(raw)
    stem = f'Here are {d["desc"]}: {", ".join(slv(d, x) for x in raw)}. Draw an ordered stem-and-leaf diagram for these data, including a key.'
    ans = sltext(d)
    key = 'B1 correct stems; B1 leaves correct and in order; B1 key'
    if D >= 3:
        stem += ' Use your diagram to find the median.'
        ans += f'. Median {mval(d, median(d["vals"]))} {d["u"]}'
        key += f'; B1 median {mval(d, median(d["vals"]))}'
    return Q(stem, ans, key + '.')


def btbtext(dA, dB, la, lb):
    allv = dA['vals'] + dB['vals']
    rows = []
    for s in range(min(allv) // 10, max(allv) // 10 + 1):
        a = ' '.join(str(v % 10) for v in reversed(dA['vals']) if v // 10 == s)
        b = ' '.join(str(v % 10) for v in dB['vals'] if v // 10 == s)
        rows.append(f'{a} | {s} | {b}'.strip())
    both = [s for s in range(min(allv) // 10, max(allv) // 10 + 1) if any(v // 10 == s for v in dA['vals']) and any(v // 10 == s for v in dB['vals'])]
    s = both[len(both) // 2] if both else dA['vals'][0] // 10
    x = next((v for v in dA['vals'] if v // 10 == s), s * 10 + 5)
    yb = next((v for v in dB['vals'] if v // 10 == s), s * 10 + 2)
    kk = f'{x % 10} | {s} | {yb % 10} means {slv(dA, x)} {dA["u"]} for {la} and {slv(dA, yb)} {dA["u"]} for {lb}'
    return '; '.join(rows) + f'. Key: {kk}'


BTB = [
    ('the marks of students in two classes in a mathematics test', 'Class A', 'Class B', 'marks', (3, 8), 'higher'),
    ('the times, in seconds, that two groups of students took to solve a puzzle', 'Group 1', 'Group 2', 'seconds', (2, 6), 'lower'),
    ('the pulse rates, in beats per minute, of two teams after exercise', 'Team P', 'Team Q', 'beats per minute', (6, 9), 'lower'),
    ('the masses, in grams, of apples from two farms', 'Farm X', 'Farm Y', 'g', (8, 12), 'higher'),
]


def btbdata(r, D):
    desc, la, lb, u, (s0, s1), better = r.choice(BTB)
    nA, nB = r.randint(9, 11 + D), r.randint(9, 11 + D)
    shift = r.choice([-8, -5, 5, 8])
    lo, hi = s0 * 10, s1 * 10 + 9
    A = sorted(r.randint(lo, hi - 10) for _ in range(nA))
    B = sorted(min(hi, max(lo, x + shift + r.randint(-6, 6))) for x in r.sample(A + A, nB))
    dA = dict(vals=A, u=u, dec=False)
    dB = dict(vals=B, u=u, dec=False)
    return desc, la, lb, u, better, dA, dB


@t153.add('C3', (2, 3, 4, 5))
def t153_btb(r, D):
    desc, la, lb, u, better, dA, dB = btbdata(r, D)
    A, B = dA['vals'], dB['vals']
    mA, mB = median(A), median(B)
    if mA == mB:
        return None
    stem = f'The back-to-back stem-and-leaf diagram shows {desc}. {la} leaves are on the left and {lb} leaves are on the right. {btbtext(dA, dB, la, lb)}. Find the median and the range for each group.'
    ans = f'{la}: median {fv(mA)}, range {A[-1] - A[0]}; {lb}: median {fv(mB)}, range {B[-1] - B[0]}'
    key = 'M1 median position for each; A1 A1 medians; B1 both ranges'
    if D >= 4:
        top = la if (mA > mB) == (better == 'higher') else lb
        stem += f' Compare the two distributions.'
        ans += f'. On average {top} did better ({better} median); the group with range {min(A[-1] - A[0], B[-1] - B[0])} is more consistent.'
        key += '; B1 compares medians in context; B1 compares ranges'
    return Q(stem, ans, key + '.', marks=4 if D < 4 else 6)


@t153.add('C3', (1, 2, 3, 4, 5))
def t153_above(r, D):
    d = sldata(r, 9 + 2 * D, ctx=r.choice([c for c in SLCTX if not c[3]]))
    v = d['vals']
    x = r.choice(v[2:-2])
    cnt = sum(1 for y in v if y > x)
    if D <= 2:
        return Q(sl_intro(d) + f' How many values are greater than {x}?', str(cnt), f'Count the leaves after {x}. B1 {cnt}.')
    pc = 100 * Fr(cnt, len(v))
    return Q(sl_intro(d) + f' What percentage of the values are greater than {x}? Give your answer to 1 decimal place where necessary.',
             f'{f1(pc)}%', f'M1 {cnt} ÷ {len(v)}; M1 × 100; A1 {f1(pc)}%.')


def _sl_c4(r, D):
    desc, la, lb, u, better, dA, dB = btbdata(r, D)
    A, B = dA['vals'], dB['vals']
    mA, mB = median(A), median(B)
    rA, rB = A[-1] - A[0], B[-1] - B[0]
    if mA == mB or rA == rB:
        return None
    top = la if (mA > mB) == (better == 'higher') else lb
    cons = la if rA < rB else lb
    x = r.choice(A[2:-2])
    cnt = sum(1 for y in A if y >= x)
    intro = f'The back-to-back stem-and-leaf diagram shows {desc}. {la} leaves are on the left and {lb} leaves are on the right. {btbtext(dA, dB, la, lb)}.'
    parts = [
        lambda r: (f'Find the median for {la}.', fv(mA), 'M1 position; A1 [2]'),
        lambda r: (f'Find the median for {lb}.', fv(mB), 'M1 position; A1 [2]'),
        lambda r: ('Find the range for each group.', f'{la} {rA}; {lb} {rB}', 'B1 B1 [2]'),
        lambda r: (f'Which group did better on average? Give a reason.', f'{top}: it has the {better} median ({la} {fv(mA)}, {lb} {fv(mB)}).', 'B1 group; B1 reason [2]'),
        lambda r: ('Which group is more consistent? Give a reason.', f'{cons}: it has the smaller range ({min(rA, rB)}).', 'B1 [1]'),
        lambda r: (f'How many members of {la} had a value of {x} or more?', str(cnt), 'B1 [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t153.add('C4', (2, 3, 4, 5), 'multi_step')(_sl_c4)


@t153.add('C4', (3, 4, 5), 'multi_step')
def t153_full(r, D):
    ctx = r.choice([c for c in SLCTX if not c[3]])
    d = sldata(r, r.choice([11, 13, 15]), ctx=ctx)
    v = d['vals']
    raw = v[:]
    r.shuffle(raw)
    md = median(v)
    rg = v[-1] - v[0]
    om = md + r.choice([-6, -4, 4, 6])
    orng = rg + r.choice([-8, -5, 5, 8])
    if orng <= 0:
        return None
    return Q(f'Here are {d["desc"]}: {", ".join(map(str, raw))}. (a) Draw an ordered stem-and-leaf diagram, with a key. (b) Find the median. (c) Find the range. '
             f'(d) A second set of data has median {fv(om)} and range {orng}. Make two comparisons between the two sets of data.',
             f'(a) {sltext(d)} (b) {fv(md)} (c) {rg} (d) The first set has a {"higher" if md > om else "lower"} median, so its values are {"greater" if md > om else "smaller"} on average; '
             f'the first set has a {"smaller" if rg < orng else "larger"} range, so it is {"more" if rg < orng else "less"} consistent.',
             '(a) B2 correct ordered diagram (B1 one error); B1 key [3] (b) B1 [1] (c) B1 [1] (d) B1 average comparison; B1 spread comparison [2]', marks=7)


# ---------------------------------------------- scatter graphs
t154 = topic('Scatter graphs, correlation and lines of best fit', 'scatter graphs', 'correlation', 'lines of best fit')

SC = [
    dict(x='number of hours of revision', y='test mark (%)', s='students', sign=1, xs=(1, 12), f=lambda x: 25 + 5 * x, e=5, lo=0, hi=100),
    dict(x='age of the car (years)', y='value of the car ($ thousands)', s='cars', sign=-1, xs=(1, 10), f=lambda x: 32 - 2.5 * x, e=2, lo=1, hi=60),
    dict(x='midday temperature (°C)', y='number of hot drinks sold', s='days', sign=-1, xs=(5, 30), f=lambda x: 130 - 3 * x, e=7, lo=0, hi=200),
    dict(x='midday temperature (°C)', y='number of ice creams sold', s='days', sign=1, xs=(12, 35), f=lambda x: 4 * x - 30, e=8, lo=0, hi=200),
    dict(x='height (cm)', y='arm span (cm)', s='students', sign=1, xs=(140, 185), f=lambda x: 1.05 * x - 8, e=4, lo=100, hi=220),
    dict(x='distance from home to school (km)', y='journey time (minutes)', s='students', sign=1, xs=(1, 15), f=lambda x: 4 * x + 5, e=5, lo=1, hi=120),
    dict(x='number of hours of sunshine', y='number of umbrellas sold', s='days', sign=-1, xs=(0, 12), f=lambda x: 60 - 4 * x, e=4, lo=0, hi=100),
    dict(x='shoe size', y='mark in a mathematics test', s='students', sign=0, xs=(3, 11), ys=(30, 95)),
    dict(x='number of letters in first name', y='height (cm)', s='students', sign=0, xs=(3, 10), ys=(140, 180)),
]


def pearson(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    sxx = sum((a - mx) ** 2 for a in xs)
    syy = sum((b - my) ** 2 for b in ys)
    if sxx == 0 or syy == 0:
        return 0
    return sxy / math.sqrt(sxx * syy)


def scdata(r, n, sign=None, outlier=False):
    pool = [c for c in SC if sign is None or c['sign'] == sign]
    c = r.choice(pool)
    for _ in range(100):
        lo, hi = c['xs']
        if hi - lo + 1 < n:
            return None
        xs = sorted(r.sample(range(lo, hi + 1), n))
        if c['sign'] == 0:
            ys = [r.randint(*c['ys']) for _ in xs]
            if abs(pearson(xs, ys)) < 0.25:
                return dict(c=c, xs=xs, ys=ys, out=None)
            continue
        ys = [int(min(c['hi'], max(c['lo'], round(c['f'](x) + r.uniform(-c['e'], c['e']))))) for x in xs]
        rr = pearson(xs, ys)
        if rr * c['sign'] < 0.85:
            continue
        out = None
        if outlier:
            i = r.randint(2, n - 3)
            off = r.choice([-1, 1]) * r.randint(4, 6) * c['e']
            yo = int(round(c['f'](xs[i]) + off))
            if not c['lo'] <= yo <= c['hi']:
                continue
            ys[i] = yo
            out = i
        return dict(c=c, xs=xs, ys=ys, out=out)
    return None


def sctab(d):
    c = d['c']
    return f'{c["x"][0].upper() + c["x"][1:]}: {" | ".join(map(str, d["xs"]))}. {c["y"][0].upper() + c["y"][1:]}: {" | ".join(map(str, d["ys"]))}.'


def corr_opts(x, y):
    return {1: f'Positive correlation: as the {x} increases, the {y} tends to increase',
            -1: f'Negative correlation: as the {x} increases, the {y} tends to decrease',
            0: 'No correlation',
            9: f'Negative correlation: as the {x} increases, the {y} tends to increase'}


def cname_x(c, k):
    return c[k].split(' (')[0]


CTXS = [
    ('height of a person', 'shoe size of the person', 1), ('age of a car', 'value of the car', -1),
    ('outdoor temperature', 'number of hot drinks sold at a café', -1), ('outdoor temperature', 'number of ice creams sold', 1),
    ('number of hours of revision', 'test mark', 1), ('shoe size of a student', 'test mark of the student', 0),
    ('height above sea level', 'air temperature', -1), ('arm span of a person', 'height of the person', 1),
    ('house number', 'number of people living in the house', 0), ('number of hours spent gaming each night', 'hours of sleep each night', -1),
    ('distance travelled by a taxi', 'cost of the journey', 1), ('number of workers building a wall', 'time taken to build the wall', -1),
    ('price of a concert ticket', 'number of tickets sold', -1), ('month of birth', 'mass of a student', 0),
]


@t154.add('C1', (1, 2, 3))
def t154_type(r, D):
    x, y, s = r.choice(CTXS)
    p = person(r)
    o = corr_opts(x, y)
    return MCQ(r, f'{p} collects data in {city(r)} on the {x} and the {y}. Which statement best describes the correlation you would expect?', o[s],
               [o[k] for k in (1, -1, 0, 9) if k != s], 'B1 [1]')


@t154.add('C1', (2, 3))
def t154_data(r, D):
    d = scdata(r, r.randint(6, 8))
    if d is None:
        return None
    c = d['c']
    o = corr_opts(cname_x(c, 'x'), cname_x(c, 'y'))
    return MCQ(r, f'The table shows the {c["x"]} and the {c["y"]} for {len(d["xs"])} {c["s"]}. {sctab(d)} Which statement describes the correlation shown by these data?',
               o[c['sign']], [o[k] for k in (1, -1, 0, 9) if k != c['sign']], 'B1 [1]')


@t154.add('C1', (1, 2, 3))
def t154_read(r, D):
    m = r.choice([2, 3, 4, 5, -2, -3, Fr(1, 2), Fr(3, 2), Fr(-3, 2)])
    x1 = r.randint(0, 10)
    x2 = x1 + 2 * r.randint(2, 5)
    y1 = r.randint(20, 60)
    y2 = y1 + m * (x2 - x1)
    x0 = r.randint(x1 + 1, x2 - 1)
    y0 = y1 + m * (x0 - x1)
    return Q(f'A line of best fit on a scatter graph passes through the points ({x1}, {y1}) and ({x2}, {fv(y2)}). Use the line to estimate the value of y when x = {x0}.',
             fv(y0), f'Gradient {fv(m)}; {y1} + {fv(m)} × {x0 - x1} = {fv(y0)}. B1 [1]')


t154.fixed('C1', (1, 2), [
    ('What is an outlier on a scatter graph?', 'A point that does not fit the general pattern of the data', 'B1 [1]',
     ['The point with the largest x-value', 'A point that lies on the line of best fit', 'The mean of the data']),
    ('A line of best fit is drawn on a scatter graph. Which point should it pass through or close to?', 'The mean point (mean of x, mean of y)', 'B1 [1]',
     ['The origin', 'The point with the smallest x-value', 'The highest point']),
    ('Write down the type of correlation shown when the points lie close to a straight line sloping downwards from left to right.', 'Negative correlation', 'B1 [1]'),
])
t154.fixed('C2', (2, 3), [
    ('Explain why a strong correlation between two variables does not prove that one causes the other.',
     'Correlation only shows that the variables change together; a third factor could affect both, or the link could be coincidence.', 'B1 relationship is not cause; B1 third factor or coincidence. [2]'),
    ('Explain the difference between interpolation and extrapolation when using a line of best fit.',
     'Interpolation estimates a value inside the range of the data and is usually reliable; extrapolation estimates outside the range and may be unreliable because the pattern may not continue.', 'B1 inside vs outside the range; B1 reliability. [2]'),
])


@t154.add('C2', (1, 2, 3, 4), 'explain')
def t154_extrap(r, D):
    c = r.choice([c for c in SC if c['sign'] != 0])
    lo, hi = c['xs']
    p = person(r)
    far = hi + r.randint(2, 4) * (hi - lo) // 2 + 1
    return Q(f'{p} collects data on the {c["x"]} and the {c["y"]} of some {c["s"]}. The x-values range from {lo} to {hi}. {p} draws a line of best fit and uses it to estimate the {cname_x(c, "y")} when the {cname_x(c, "x")} is {far}. Explain why this estimate may not be reliable.',
             f'{far} is outside the range of the data ({lo} to {hi}), so this is extrapolation; the pattern may not continue beyond the data.', 'B1 outside the range; B1 pattern may not continue. [2]')


CAUSE = [
    ('ice cream sales', 'number of people with sunburn', 'hot, sunny weather'),
    ('number of fire engines at a fire', 'amount of damage caused', 'the size of the fire'),
    ('shoe size of children', 'reading score of children', 'the age of the children'),
    ('number of umbrellas sold', 'number of road accidents', 'rainy weather'),
    ('number of teachers in a city', 'number of shops in the city', 'the population of the city'),
    ('number of hot chocolates sold', 'number of people wearing scarves', 'cold weather'),
]


@t154.add('C2', (1, 2, 3, 4), 'explain')
def t154_cause(r, D):
    a, b, z = r.choice(CAUSE)
    p = person(r)
    return Q(f'Data from {city(r)} show a strong positive correlation between the {a} and the {b}. {p} says: "An increase in the {a} causes an increase in the {b}." Explain why {p} may be wrong.',
             f'Correlation does not prove causation. Both are probably affected by a third factor: {z}.', 'B1 correlation is not causation; B1 suitable third factor. [2]')


LOBF_ERR = [
    ('makes the line pass through the origin (0, 0)', 'A line of best fit does not have to pass through the origin; it should follow the trend of the points, with about the same number of points on each side.'),
    ('joins the first point to the last point', 'The line should follow all the points, with about the same number on each side, not just join the end points.'),
    ('draws the line so that all the points are above it', 'The line should pass through the middle of the points, with roughly equal numbers of points on each side.'),
    ('draws a line of best fit for data that show no correlation', 'When there is no correlation there is no linear pattern, so a line of best fit should not be drawn.'),
]


@t154.add('C2', (1, 2, 3, 4), 'explain')
def t154_lobf(r, D):
    c = r.choice(SC)
    p = person(r)
    e, why = r.choice(LOBF_ERR)
    return Q(f'{p} plots a scatter graph of the {c["x"]} against the {c["y"]} for some {c["s"]}. {p} {e}. Explain what is wrong.', why, 'B1 identifies the problem; B1 correct method. [2]')


@t154.add('C2', (2, 3, 4), 'explain')
def t154_outlier(r, D):
    d = scdata(r, r.randint(7, 9), sign=r.choice([1, -1]), outlier=True)
    if d is None:
        return None
    c, i = d['c'], d['out']
    return Q(f'The table shows the {c["x"]} and the {c["y"]} for some {c["s"]}. {sctab(d)} One pair of values is an outlier. Write down the outlier and give a reason for your answer.',
             f'({d["xs"][i]}, {d["ys"][i]}): it does not follow the {"positive" if c["sign"] > 0 else "negative"} correlation shown by the other points.', 'B1 outlier; B1 reason. [2]')


@t154.add('C3', (1, 2, 3, 4, 5))
def t154_points(r, D):
    d = scdata(r, 6 + D, outlier=D >= 3 and r.random() < 0.7)
    if d is None:
        return None
    c = d['c']
    if c['sign'] == 0 and D >= 3:
        d = scdata(r, 6 + D, sign=r.choice([1, -1]), outlier=True)
        if d is None:
            return None
        c = d['c']
    x, y = cname_x(c, 'x'), cname_x(c, 'y')
    desc = {1: f'Positive correlation: as the {x} increases, the {y} tends to increase.', -1: f'Negative correlation: as the {x} increases, the {y} tends to decrease.',
            0: f'No correlation: there is no clear relationship between the {x} and the {y}.'}[c['sign']]
    stem = f'The table shows the {c["x"]} and the {c["y"]} for {len(d["xs"])} {c["s"]}. {sctab(d)} Describe the correlation and interpret it in context.'
    ans, key, mk = desc, 'B1 type of correlation; B1 interpretation in context', None
    if d['out'] is not None:
        stem += ' Identify the outlier.'
        ans += f' Outlier ({d["xs"][d["out"]]}, {d["ys"][d["out"]]}).'
        key += '; B1 outlier'
        mk = 3
    if D >= 4:
        mx, my = Fr(sum(d['xs']), len(d['xs'])), Fr(sum(d['ys']), len(d['ys']))
        stem += ' Work out the mean point, to 1 decimal place where necessary.'
        ans += f' Mean point ({f1(mx)}, {f1(my)}).'
        key += '; M1 A1 mean point'
        mk = (mk or 2) + 2
    return Q(stem, ans, key + '.', marks=mk)


@t154.add('C3', (1, 2, 3, 4, 5))
def t154_est(r, D):
    c = r.choice([c for c in SC if c['sign'] != 0])
    lo, hi = c['xs']
    span = hi - lo
    x1 = lo + r.randint(0, span // 4)
    x2 = hi - r.randint(0, span // 4)
    if x2 - x1 < 4:
        return None
    m = Fr(round(c['f'](x2) - c['f'](x1)), x2 - x1)
    y1 = round(c['f'](x1))
    y2 = y1 + m * (x2 - x1)
    if y2.denominator != 1:
        return None
    x0 = r.randint(x1 + 1, x2 - 1)
    y0 = y1 + m * (x0 - x1)
    X, Y = cname_x(c, 'x'), cname_x(c, 'y')
    intro = f'A scatter graph shows the {c["x"]} and the {c["y"]} for some {c["s"]}. The line of best fit passes through ({x1}, {y1}) and ({x2}, {fv(y2)}).'
    if D <= 2:
        return Q(intro + f' Use the line of best fit to estimate the {Y} when the {X} is {x0}. Give your answer to 1 decimal place where necessary.',
                 f1(y0), f'M1 gradient ({fv(y2)} − {y1}) ÷ {x2 - x1}; A1 {f1(y0)}.')
    if D == 3:
        yt = r.randint(int(min(y1, y2)) + 1, int(max(y1, y2)) - 1)
        xt = x1 + (yt - y1) / m
        return Q(intro + f' Use the line of best fit to estimate the {X} when the {Y} is {yt}. Give your answer to 1 decimal place where necessary.',
                 f1(xt), f'M1 gradient; M1 ({yt} − {y1}) ÷ gradient; A1 {f1(xt)}.')
    if D == 4:
        return Q(intro + f' Work out the gradient of the line of best fit, to 2 decimal places where necessary, and explain what it means in context.',
                 f'{fd(float(m), 2) if (m * 100).denominator != 1 else fv(m)}: the {Y} {"increases" if m > 0 else "decreases"} by about {fd(abs(float(m)), 2) if (abs(m) * 100).denominator != 1 else fv(abs(m))} for each extra unit of {X}.',
                 'M1 change in y ÷ change in x; A1; B1 interpretation.', marks=3)
    cc = y1 - m * x1
    eq = f'y = {f1(m)}x {"+" if cc >= 0 else MINUS} {f1(abs(cc))}'
    return Q(intro + f' Find the equation of the line of best fit in the form y = mx + c (give values to 1 decimal place where necessary), and use it to estimate the {Y} when the {X} is {x0}.',
             f'{eq}; estimate {f1(y0)}', 'M1 gradient; M1 substitutes a point to find c; A1 equation; B1 estimate.', marks=4)


@t154.add('C3', (2, 3, 4, 5))
def t154_mean(r, D):
    d = scdata(r, 4 + D, sign=r.choice([1, -1]))
    if d is None:
        return None
    c = d['c']
    mx, my = Fr(sum(d['xs']), len(d['xs'])), Fr(sum(d['ys']), len(d['ys']))
    return Q(f'The table shows the {c["x"]} and the {c["y"]} for {len(d["xs"])} {c["s"]}. {sctab(d)} Work out the coordinates of the mean point, to 1 decimal place where necessary. Explain why this point is useful when drawing a line of best fit.',
             f'({f1(mx)}, {f1(my)}); the line of best fit should pass through the mean point.', f'M1 {sum(d["xs"])} ÷ {len(d["xs"])}; M1 {sum(d["ys"])} ÷ {len(d["ys"])}; A1; B1 line passes through it.', marks=4)


def _sc_c4(r, D):
    d = scdata(r, 8, sign=r.choice([1, -1]), outlier=True)
    if d is None:
        return None
    c, i = d['c'], d['out']
    X, Y = cname_x(c, 'x'), cname_x(c, 'y')
    xs = [x for j, x in enumerate(d['xs']) if j != i]
    ys = [y for j, y in enumerate(d['ys']) if j != i]
    mx, my = Fr(sum(xs), len(xs)), Fr(sum(ys), len(ys))
    lo, hi = c['xs']
    far = hi + (hi - lo)
    intro = f'The table shows the {c["x"]} and the {c["y"]} for 8 {c["s"]}. {sctab(d)}'
    parts = [
        lambda r: ('Describe the type of correlation.', 'Positive correlation' if c['sign'] > 0 else 'Negative correlation', 'B1 [1]'),
        lambda r: ('Write down the coordinates of the outlier.', pt(d['xs'][i], d['ys'][i]), 'B1 [1]'),
        lambda r: (f'Leave out the outlier. Work out the mean point of the other 7 pairs of values, to 1 decimal place where necessary.', f'({f1(mx)}, {f1(my)})', 'M1 M1 A1 [3]'),
        lambda r: (f'Explain why a line of best fit should not be used to estimate the {Y} when the {X} is {far}.', f'{far} is outside the range of the data, so the pattern may not continue (extrapolation).', 'B1 [1]'),
        lambda r: (f'Interpret the correlation in context.', f'As the {X} increases, the {Y} tends to {"increase" if c["sign"] > 0 else "decrease"}.', 'B1 [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t154.add('C4', (2, 3, 4, 5), 'multi_step')(_sc_c4)


@t154.add('C4', (3, 4, 5), 'multi_step')
def t154_full(r, D):
    c = r.choice([c for c in SC if c['sign'] != 0])
    lo, hi = c['xs']
    x1 = lo + (hi - lo) // 4
    x2 = hi - (hi - lo) // 4
    y1 = round(c['f'](x1))
    m = Fr(round(c['f'](x2)) - y1, x2 - x1)
    y2 = y1 + m * (x2 - x1)
    x0 = r.randint(x1 + 1, x2 - 1)
    y0 = y1 + m * (x0 - x1)
    far = hi + (hi - lo)
    X, Y = cname_x(c, 'x'), cname_x(c, 'y')
    return Q(f'{person(r)} draws a scatter graph of the {c["x"]} and the {c["y"]} for some {c["s"]}. The data have x-values from {lo} to {hi}. The line of best fit passes through ({x1}, {y1}) and ({x2}, {fv(y2)}). '
             f'(a) What type of correlation does the line show? (b) Work out the gradient of the line, to 2 decimal places where necessary. (c) Estimate the {Y} when the {X} is {x0}, to 1 decimal place where necessary. '
             f'(d) Explain whether it is sensible to use the line to estimate the {Y} when the {X} is {far}.',
             f'(a) {"Positive" if m > 0 else "Negative"} correlation (b) {fv(m) if (m * 100).denominator == 1 else fd(float(m), 2)} (c) {f1(y0)} '
             f'(d) No: {far} is outside the range {lo} to {hi}, so this would be extrapolation and the pattern may not continue.',
             '(a) B1 [1] (b) M1 A1 [2] (c) M1 A1 [2] (d) B1 [1]', marks=6)


CHAPTERS[15] = [t151, t152, t153, t154]
