"""Cambridge International AS Mathematics 9709 (grade 11): Paper 1 Pure Mathematics 1 and
Paper 5 Probability & Statistics 1.

Chapters 1-9 follow the Pure 1 coursebook (quadratics, functions, coordinate geometry, circular
measure, trigonometry, series, differentiation, further differentiation, integration); chapters
10-17 follow Probability & Statistics 1 (representation of data, averages, measures of variation,
probability, permutations and combinations, discrete random variables, binomial and geometric
distributions, the normal distribution).

Conventions: exact answers where the syllabus expects them, otherwise 3 significant figures
(angles in degrees to 1 d.p.); mark schemes use M (method), A (accuracy, dependent on M),
B (independent) and DM (dependent method) marks. Item marks are read from the mark points in the
key (see _finalise at the end of the module).
"""
import math
import re
from fractions import Fraction as Fr
from ._lib import topic, mcq, compose, sf, sci, person, two_people, city, sup

PROFILE = {'mark_scale': {'long': (1.5, 1.5), 'case': (1.25, 1.25)}, 'wordy': False}
CHAPTERS = {}
MINUS = '−'


# ================================================================ formatting helpers

def num(x):
    """Exact number: ints, Fractions as a/b, floats without trailing zeros; unicode minus."""
    if isinstance(x, Fr):
        if x.denominator == 1:
            return num(int(x))
        return (MINUS if x < 0 else '') + f'{abs(x.numerator)}/{x.denominator}'
    if isinstance(x, float) and abs(x - round(x)) < 1e-9:
        x = int(round(x))
    if isinstance(x, int):
        return (MINUS if x < 0 else '') + str(abs(x))
    s = f'{abs(x):.6f}'.rstrip('0').rstrip('.')
    return (MINUS if x < 0 and s != '0' else '') + s


def n3(x):
    """3 significant figures with unicode minus (keeps trailing zeros, e.g. 2.50)."""
    if abs(x) < 1e-12:
        return '0'
    return (MINUS if x < 0 else '') + sf(abs(x), 3)


def n4(x):
    if abs(x) < 1e-12:
        return '0'
    return (MINUS if x < 0 else '') + sf(abs(x), 4)


def d1(x):
    """Angle in degrees to 1 d.p."""
    v = round(x + 0.0, 1)
    if v == 0:
        v = 0.0
    return (MINUS if v < 0 else '') + f'{abs(v):.1f}°'


def p4(x):
    """Probability to 4 d.p. (used for intermediate table values)."""
    return f'{x:.4f}'


def sg(x):
    """' + 3' or ' − 3' for appending a constant."""
    return f' + {num(x)}' if x >= 0 else f' − {num(-x)}'


def pw(n, v='x'):
    """v raised to n (n int or Fraction)."""
    n = Fr(n)
    if n == 0:
        return ''
    if n == 1:
        return v
    if n.denominator == 1:
        return v + sup(int(n))
    return f'{v}^({num(n)})'


def term(c, n, v='x', first=False):
    c = Fr(c)
    vv = pw(n, v)
    a = abs(c)
    body = (num(a) if (a != 1 or not vv) else '') + vv
    if a.denominator != 1 and vv:
        body = f'({num(a)}){vv}'
    if first:
        return (MINUS if c < 0 else '') + body
    return (' − ' if c < 0 else ' + ') + body


def poly(terms, v='x'):
    """terms: list of (coef, power) -> '3x² − 2x + 5'."""
    out = ''
    for c, n in terms:
        if c == 0:
            continue
        out += term(c, n, v, first=not out)
    return out or '0'


def quad(a, b, c, v='x'):
    return poly([(a, 2), (b, 1), (c, 0)], v)


def intq(a, b, c):
    """Scale a quadratic's coefficients to coprime integers with a > 0."""
    a, b, c = Fr(a), Fr(b), Fr(c)
    L = math.lcm(a.denominator, b.denominator, c.denominator)
    a, b, c = int(a * L), int(b * L), int(c * L)
    g = math.gcd(math.gcd(abs(a), abs(b)), abs(c)) or 1
    if a < 0:
        g = -g
    return a // g, b // g, c // g


def lin(a, b, v='x'):
    return poly([(a, 1), (b, 0)], v)


def br(p, v='x'):
    """(x + p) or (x − p)."""
    if p == 0:
        return v
    return f'({v}{sg(p)})'


def sq(p, v='x'):
    return f'({v}{sg(p)})²' if p != 0 else f'{v}²'


def line_eq(m, c):
    """y = mx + c with exact coefficients."""
    m, c = Fr(m), Fr(c)
    if m == 0:
        return f'y = {num(c)}'
    return 'y = ' + poly([(m, 1), (c, 0)])


def gen_line(a, b, c):
    """ax + by + c = 0 tidied: integer coefficients, positive x coefficient."""
    a, b, c = Fr(a), Fr(b), Fr(c)
    L = math.lcm(a.denominator, b.denominator, c.denominator)
    a, b, c = int(a * L), int(b * L), int(c * L)
    g = math.gcd(math.gcd(abs(a), abs(b)), abs(c)) or 1
    a, b, c = a // g, b // g, c // g
    if a < 0 or (a == 0 and b < 0):
        a, b, c = -a, -b, -c
    s = poly([(a, 1)], 'x') if a else ''
    if b:
        s += term(b, 1, 'y', first=not s)
    if c:
        s += term(c, 0, 'x', first=not s)
    return s + ' = 0'


def xk(k, v='x'):
    """'x − k' (just 'x' when k = 0)."""
    return v if k == 0 else f'{v}{sg(-k)}'


def inv_lin(a, b):
    """Inverse of ax + b as text."""
    if a > 0:
        return f'({xk(b)})/{num(a)}' if a != 1 else xk(b)
    return f'({num(b)} − x)/{num(-a)}' if a != -1 else f'{num(b)} − x'


def ordn(n):
    n = int(n)
    suf = 'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f'{n}{suf}'


def pt(x, y):
    return f'({num(x)}, {num(y)})'


def surd(n):
    """Simplified √n as (outside, inside)."""
    out, ins = 1, n
    k = 2
    while k * k <= ins:
        while ins % (k * k) == 0:
            ins //= k * k
            out *= k
        k += 1
    return out, ins


def rt(n):
    """√n simplified as a string (n positive int)."""
    o, i = surd(n)
    if i == 1:
        return str(o)
    return (str(o) if o > 1 else '') + f'√{i}'


def pi_frac(f):
    """Fraction f of π as text: 2π/3, π/6, 3π/2, π."""
    f = Fr(f)
    if f == 0:
        return '0'
    s = MINUS if f < 0 else ''
    f = abs(f)
    top = ('' if f.numerator == 1 else str(f.numerator)) + 'π'
    return s + (top if f.denominator == 1 else f'{top}/{f.denominator}')


def comb(n, k):
    return math.comb(n, k) if 0 <= k <= n else 0


def Phi(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def invPhi(p):
    lo, hi = -8.0, 8.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if Phi(mid) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def z3(z):
    """z rounded as in tables (3 d.p.)."""
    return f'{z:.3f}'.replace('-', MINUS)


def z2(z):
    return f'{z:.2f}'.replace('-', MINUS)


# ================================================================ question builders

_TOK = re.compile(r'(?<![A-Za-z])(?:DM|M|A|B)(\d)(?![\d])')
_BRK = re.compile(r'\[(\d+)\]')


def key_marks(key):
    m = _BRK.findall(key)
    if m:
        return sum(int(x) for x in m)
    return sum(int(x) for x in _TOK.findall(key))


def Q(stem, answer, key, **kw):
    d = {'stem': stem, 'answer': answer, 'key': key}
    m = key_marks(key)
    if m and 'marks' not in kw:
        d['marks'] = max(1, min(20, m))
        d['minutes'] = round(max(1.0, d['marks'] * 1.25) * 2) / 2
    d.update(kw)
    return d


def MC(r, stem, correct, distractors, key):
    """String MCQ; returns None (never raises) if fewer than 3 distinct distractors."""
    ds = []
    for x in distractors:
        if x != correct and x not in ds:
            ds.append(x)
    if len(ds) < 3:
        return None
    opts, ans = mcq(r, correct, ds)
    return {'stem': stem, 'options': opts, 'answer': ans, 'key': key}


def P(text, ans, key):
    """A compose part; marks = mark points in the key."""
    m = key_marks(key) or 1
    return lambda r: (text, ans, f'{key} [{m}]')


def PF(fn):
    """A compose part built lazily: fn(r) -> (text, ans, key) or None."""
    def g(r):
        x = fn(r)
        if not x:
            return None
        t, a, k = x
        return (t, a, f'{k} [{key_marks(k) or 1}]')
    return g


def cmp_(r, intro, parts, k=(2, 3, 4), type_='multi_step'):
    return compose(r, intro, parts, k=k, type_=type_)


def T(name, *extra):
    return topic(name, name.lower(), *extra)


def nz(r, lo, hi, excl=(0,)):
    while True:
        v = r.randint(lo, hi)
        if v not in excl:
            return v


CTXS = ['In a mathematics class in', 'A student in', 'During revision in', 'A teacher in', 'At a study group in']


def dn(x):
    """Statistics display: terminating fractions as decimals, others to 3 s.f."""
    x = Fr(x) if not isinstance(x, float) else x
    if isinstance(x, Fr):
        if x.denominator == 1:
            return num(int(x))
        d = x.denominator
        while d % 2 == 0:
            d //= 2
        while d % 5 == 0:
            d //= 5
        if d == 1:
            s = f'{abs(float(x)):.6f}'.rstrip('0').rstrip('.')
            return (MINUS if x < 0 else '') + s
        return n3(float(x))
    return num(x) if abs(x - round(x)) < 1e-9 else n3(x)


def pn(x):
    """Bracket a value if negative (for substitution in working)."""
    s = x if isinstance(x, str) else num(x)
    return f'({s})' if s.startswith(MINUS) or s.startswith('-') else s


# ================================================================ Chapter 1 Quadratics

def cs(a, p, q, v='x'):
    """a(x + p)² + q."""
    a = Fr(a)
    lead = '' if a == 1 else (MINUS if a == -1 else num(a))
    return f'{lead}{sq(p, v)}' + ('' if q == 0 else sg(q))


def cs_neg(q, a, p):
    """q − a(x + p)²."""
    lead = '' if a == 1 else num(a)
    return f'{num(q)} − {lead}{sq(p)}'


def ineq_out(u, v, strict=True, var='x'):
    lo, hi = min(u, v), max(u, v)
    s = '<' if strict else '≤'
    s2 = '>' if strict else '≥'
    return f'{var} {s} {num(lo)} or {var} {s2} {num(hi)}'


def ineq_in(u, v, strict=True, var='x'):
    lo, hi = min(u, v), max(u, v)
    s = '<' if strict else '≤'
    return f'{num(lo)} {s} {var} {s} {num(hi)}'


q11 = T('Completing the square and the vertex of a quadratic graph', 'completing the square', 'vertex of a quadratic')
q11.fixed('C1', (1, 2), [
    ('The curve y = (x − 3)² + 5 has a minimum point. What are its coordinates?', '(3, 5)', 'Minimum where (x − 3)² = 0, i.e. x = 3, y = 5.', ['(−3, 5)', '(3, −5)', '(5, 3)']),
    ('What is the least value of (x + 4)² − 7 as x varies?', '−7', '(x + 4)² ≥ 0, so the least value is 0 − 7 = −7, when x = −4.', ['−4', '7', '4']),
    ('What is the greatest value of 9 − (x − 2)²?', '9', '(x − 2)² ≥ 0 so 9 − (x − 2)² ≤ 9, with equality when x = 2.', ['2', '−9', '7']),
    ('The equation of the line of symmetry of y = (x + 6)² − 1 is', 'x = −6', 'The vertex is at (−6, −1); the axis of symmetry is the vertical line through it.', ['x = 6', 'y = −1', 'x = −1']),
    ('Which of these is x² + 10x in completed-square form?', '(x + 5)² − 25', 'Halve the coefficient of x: (x + 5)² = x² + 10x + 25, so subtract 25.', ['(x + 10)² − 100', '(x + 5)² + 25', '(x − 5)² − 25']),
    ('The curve y = −2(x − 1)² + 8 has', 'a maximum point at (1, 8)', 'The coefficient of the squared bracket is negative, so the curve is ∩-shaped with vertex (1, 8).', ['a minimum point at (1, 8)', 'a maximum point at (−1, 8)', 'a minimum point at (−1, −8)']),
])
q11.fixed('C2', (2, 3), [
    ('Explain why the least value of (x − p)² + q is q, and state the value of x at which it occurs.', 'A square is never negative, so (x − p)² ≥ 0 and the expression is at least q; it equals q only when x = p.', 'B1 (x − p)² ≥ 0; B1 least value q when x = p [2]'),
    ('Explain how completing the square on ax² + bx + c shows whether the graph has a maximum or a minimum point.', 'Writing it as a(x + p)² + q, the squared term is ≥ 0. If a > 0 the expression is least (minimum q) when x = −p; if a < 0 it is greatest (maximum q).', 'B1 sign of a decides min/max; B1 vertex (−p, q) from the completed square [2]'),
    ('Explain why the quadratic x² + 6x + 10 is positive for all real values of x.', 'x² + 6x + 10 = (x + 3)² + 1, and (x + 3)² ≥ 0, so the expression is at least 1 > 0.', 'B1 (x + 3)² + 1; B1 square ≥ 0 so ≥ 1 > 0 [2]'),
    ('Describe how the vertex of y = (x + p)² + q is related to the graph of y = x².', 'y = (x + p)² + q is y = x² translated by −p in the x-direction and q in the y-direction, so the vertex (0, 0) moves to (−p, q).', 'B1 translation by vector (−p, q); B1 vertex (−p, q) [2]'),
])


@q11.add('C1', (1, 2, 3))
def q11_c1(r, D):
    if D == 1:
        h, k = nz(r, -9, 9), nz(r, -12, 12)
        stem = f'Write down the coordinates of the vertex of the curve y = {cs(1, -h, k)}.'
        return MC(r, stem, pt(h, k), [pt(-h, k), pt(h, -k), pt(k, h), pt(-h, -k)], f'Vertex where the bracket is zero: x = {num(h)}, y = {num(k)}.')
    p, c = nz(r, -8, 8), nz(r, -15, 20)
    if D == 2:
        stem = f'Find the coordinates of the vertex of y = {quad(1, 2 * p, c)}.'
        return MC(r, stem, pt(-p, c - p * p), [pt(p, c - p * p), pt(-p, c + p * p), pt(-2 * p, c - 4 * p * p), pt(p, c + p * p)],
                  f'{quad(1, 2 * p, c)} = {cs(1, p, c - p * p)}, vertex ({num(-p)}, {num(c - p * p)}).')
    stem = f'Which expression is equal to {quad(1, 2 * p, c)}?'
    return MC(r, stem, cs(1, p, c - p * p), [cs(1, p, c + p * p), cs(1, 2 * p, c - 4 * p * p), cs(1, -p, c - p * p), cs(1, p, c - 2 * p)],
              f'Halve the coefficient of x: {sq(p)} = {quad(1, 2 * p, p * p)}, so subtract {p * p}: {cs(1, p, c - p * p)}.')


@q11.add('C2', (2, 3, 4), 'explain')
def q11_err(r, D):
    nm = person(r)
    f = r.choice(['a', 'sign', 'show']) if D >= 3 else r.choice(['a', 'sign'])
    if f == 'a':
        a, p, c = r.randint(2, 5), nz(r, -6, 6), r.randint(-9, 15)
        wrong, right = c - p * p, c - a * p * p
        stem = f'{nm} writes {quad(a, 2 * a * p, c)} = {cs(a, p, wrong)}. Explain the error and write the expression correctly in the form a(x + b)² + c.'
        return Q(stem, f'{nm} subtracted {p * p} instead of {a} × {p * p} = {a * p * p}: {cs(a, p, wrong)} expands to {quad(a, 2 * a * p, a * p * p + wrong)}. Correct: {cs(a, p, right)}.',
                 f'B1 explains the constant {p * p} must be multiplied by {a} (or expands to show the error); B1 {cs(a, p, right)}')
    if f == 'sign':
        p, q = nz(r, -9, 9), nz(r, -12, 12)
        stem = f'{nm} says that the minimum point of y = {cs(1, p, q)} is ({num(p)}, {num(q)}). Explain why {nm} is wrong and give the correct minimum point.'
        return Q(stem, f'The bracket {sq(p)[:-1]} is zero when x = {num(-p)}, not {num(p)}. Minimum point ({num(-p)}, {num(q)}).',
                 f'B1 bracket zero when x = {num(-p)}; B1 ({num(-p)}, {num(q)})')
    p, q = nz(r, -7, 7), r.randint(1, 12)
    stem = f'By completing the square, show that {quad(1, 2 * p, p * p + q)} > 0 for all real values of x.'
    return Q(stem, f'{quad(1, 2 * p, p * p + q)} = {cs(1, p, q)}; since {sq(p)} ≥ 0 the expression is ≥ {q} > 0.',
             f'M1 completes the square {cs(1, p, q)}; A1 states square ≥ 0 so expression ≥ {q} > 0')


@q11.add('C3', (1, 2, 3, 4, 5), 'numerical')
def q11_cs(r, D):
    if D <= 2:
        p, c = nz(r, -9, 9), r.randint(-20, 25)
        q = c - p * p
        stem = f'Express {quad(1, 2 * p, c)} in the form (x + a)² + b' + (', and hence state the coordinates of the vertex of y = ' + quad(1, 2 * p, c) + '.' if D == 2 else '.')
        key = f'B1 a = {num(p)}; B1 b = {num(q)}' + (f'; B1 vertex ({num(-p)}, {num(q)})' if D == 2 else '')
        return Q(stem, cs(1, p, q) + (f'; vertex ({num(-p)}, {num(q)})' if D == 2 else ''), key)
    if D == 3:
        b, c = r.choice([-9, -7, -5, -3, 3, 5, 7, 9, 11]), r.randint(-6, 12)
        p, q = Fr(b, 2), Fr(c) - Fr(b * b, 4)
        stem = f'Express {quad(1, b, c)} in the form (x + a)² + b, where a and b are constants, and state the least value of the expression.'
        return Q(stem, f'{cs(1, p, q)}; least value {num(q)}', f'B1 a = {num(p)}; B1 b = {num(q)}; B1 least value {num(q)} when x = {num(-p)}')
    if D == 4:
        a, p, q = r.randint(2, 5), nz(r, -5, 5), r.randint(-20, 20)
        c = a * p * p + q
        stem = f'Express {quad(a, 2 * a * p, c)} in the form a(x + b)² + c. Hence state the coordinates of the minimum point of y = {quad(a, 2 * a * p, c)}.'
        return Q(stem, f'{cs(a, p, q)}; minimum point ({num(-p)}, {num(q)})',
                 f'B1 a = {a}; B1 b = {num(p)}; M1 c = {c} − {a} × {p * p}; A1 c = {num(q)}; B1 minimum ({num(-p)}, {num(q)}) FT')
    a, p, q = r.randint(2, 4), nz(r, -5, 5), r.randint(5, 30)
    # q − a(x − p)² = −a x² + 2ap x + (q − a p²)
    c = q - a * p * p
    stem = f'Express {poly([(c, 0), (2 * a * p, 1), (-a, 2)])} in the form a − b(x + c)², where a, b and c are constants. Hence state the greatest value of the expression and the value of x at which it occurs.'
    return Q(stem, f'{cs_neg(q, a, -p)}; greatest value {q} when x = {num(p)}',
             f'B1 b = {a}; B1 c = {num(-p)}; M1 a = {num(c)} + {a} × {p * p}; A1 a = {q}; B1 greatest value {q} at x = {num(p)}')


@q11.add('C3', (2, 3, 4, 5), 'numerical')
def q11_find(r, D):
    f = r.choice(['vertex', 'range']) if D <= 3 else r.choice(['range', 'two'])
    if f == 'vertex':
        h, k = nz(r, -8, 8), nz(r, -15, 15)
        b, c = -2 * h, h * h + k
        stem = f'The curve y = x² + bx + c has its minimum point at ({num(h)}, {num(k)}). Find the values of b and c.'
        return Q(stem, f'b = {num(b)}, c = {num(c)}', f'M1 y = {cs(1, -h, k)}; M1 expands; A1 b = {num(b)}, c = {num(c)}')
    if f == 'range':
        a, p, q = (1 if D <= 3 else r.randint(2, 4)), nz(r, -7, 7), nz(r, -18, 18)
        c = a * p * p + q
        stem = f'The function f is defined by f(x) = {quad(a, 2 * a * p, c)} for x ∈ ℝ. By completing the square, find the range of f.'
        return Q(stem, f'f(x) ≥ {num(q)}', f'M1 f(x) = {cs(a, p, q)}; A1 least value {num(q)}; B1 range f(x) ≥ {num(q)}' + ('' if a == 1 else f'; B1 a = {a} and b = {num(p)} correct'))
    # 'two': f(x) = x² − 2kx + m has minimum value v at x = h  -> unknowns in both coefficients
    a = r.randint(2, 3)
    h, v = nz(r, -5, 5), nz(r, -12, 12)
    # f(x) = a x² + b x + c: vertex at h -> b = -2 a h; c = a h² + v
    b, c = -2 * a * h, a * h * h + v
    stem = f'The quadratic f(x) = {a}x² + px + q has a minimum value of {num(v)}, which occurs when x = {num(h)}. Find the values of p and q, and state the range of f for x ∈ ℝ.'
    return Q(stem, f'p = {num(b)}, q = {num(c)}; f(x) ≥ {num(v)}', f'M1 f(x) = {cs(a, -h, v)}; M1 expands; A1 p = {num(b)}; A1 q = {num(c)}; B1 f(x) ≥ {num(v)}')


def q11_c4(r, D):
    a = 1 if D <= 3 else r.randint(1, 3)
    p, q = nz(r, -6, 6), nz(r, -20, 12)
    c = a * p * p + q
    m = r.randint(1, 5)
    k = q + a * m * m
    f = quad(a, 2 * a * p, c)
    intro = f'The function f is defined by f(x) = {f} for x ∈ ℝ.'
    parts = [
        P(f'Express f(x) in the form {"" if a == 1 else "a"}(x + b)² + c.', cs(a, p, q), f'B1 b = {num(p)}; B1 c = {num(q)}'),
        P('Write down the coordinates of the vertex of the graph of y = f(x).', pt(-p, q), f'B1 FT ({num(-p)}, {num(q)})'),
        P('State the range of f.', f'f(x) ≥ {num(q)}', f'B1 f(x) ≥ {num(q)}'),
        P(f'Solve the equation f(x) = {num(k)}.', f'x = {num(-p - m)} or x = {num(-p + m)}',
          f'M1 {"" if a == 1 else num(a)}{sq(p)} = {num(k - q)}; M1 x{sg(p)} = ±{m}; A1 x = {num(-p - m)}, {num(-p + m)}'),
        P('Find the set of values of t for which the equation f(x) = t has no real roots.', f't < {num(q)}', f'B1 t < {num(q)} (graph never reaches below the vertex)'),
    ]
    if a == 1:
        parts.append(P('Describe fully the single transformation that maps the graph of y = x² onto the graph of y = f(x).', f'Translation by vector ({num(-p)}, {num(q)})',
                       f'B1 translation; B1 vector ({num(-p)}, {num(q)})'))
    return cmp_(r, intro, parts)


q11.add('C4', (2, 3, 4, 5))(q11_c4)


# ---------------------------------------------------------------- 1.2 discriminant
q12 = T('The discriminant and the nature of roots', 'discriminant', 'nature of roots')
q12.fixed('C1', (1, 2), [
    ('For the equation ax² + bx + c = 0, which condition gives two equal (repeated) real roots?', 'b² − 4ac = 0', 'Equal roots when the discriminant is zero.', ['b² − 4ac > 0', 'b² − 4ac < 0', 'b² + 4ac = 0']),
    ('The discriminant of a quadratic equation is −12. How many real roots does the equation have?', '0', 'A negative discriminant means no real roots.', ['1', '2', '4']),
    ('A line is a tangent to a curve. After eliminating y, the discriminant of the resulting quadratic in x is', 'equal to zero', 'A tangent meets the curve at exactly one point, so the quadratic has a repeated root.', ['greater than zero', 'less than zero', 'equal to one']),
    ('The graph of y = ax² + bx + c lies entirely above the x-axis. Which statement is true?', 'a > 0 and b² − 4ac < 0', 'U-shaped (a > 0) and never meets the x-axis (no real roots).', ['a < 0 and b² − 4ac < 0', 'a > 0 and b² − 4ac > 0', 'a > 0 and b² − 4ac = 0']),
    ('A quadratic equation has discriminant 49. Which describes its roots?', 'two distinct real (rational) roots', '49 > 0 gives two distinct roots; it is a perfect square so the roots are rational when a, b, c are integers.', ['two equal real roots', 'no real roots', 'one real root and one non-real root']),
])
q12.fixed('C2', (2, 3), [
    ('Explain why the equation ax² + bx + c = 0 must have two distinct real roots when a and c have opposite signs.', 'If ac < 0 then −4ac > 0, so b² − 4ac > b² ≥ 0 and the discriminant is positive.', 'B1 −4ac > 0; B1 b² ≥ 0 so discriminant > 0 [2]'),
    ('Explain how the discriminant of the quadratic obtained by eliminating y tells you whether a line meets a curve at two points, touches it, or does not meet it.', 'Discriminant > 0: two points of intersection; = 0: one repeated point, so the line is a tangent; < 0: no real solutions so no intersection.', 'B1 > 0 two points and < 0 no points; B1 = 0 tangent [2]'),
    ('Explain why the equation x² + 9 = 0 has no real roots, using the discriminant.', 'a = 1, b = 0, c = 9 so b² − 4ac = −36 < 0, so there are no real roots.', 'B1 discriminant −36; B1 negative so no real roots [2]'),
    ('Explain why a quadratic equation cannot have exactly three real roots.', 'A quadratic has at most two roots: the formula gives x = (−b ± √(b² − 4ac))/(2a), which gives at most two values.', 'B1 formula gives ± only; B1 at most two values [2]'),
])


@q12.add('C1', (1, 2, 3))
def q12_c1(r, D):
    a, b, c = (1 if D == 1 else nz(r, -5, 6)), nz(r, -9, 9), nz(r, -9, 9)
    d = b * b - 4 * a * c
    stem = f'Find the value of the discriminant of {quad(a, b, c)} = 0' + ('.' if D < 3 else ' and hence state the number of real roots.')
    nat = lambda x: '2' if x > 0 else ('1' if x == 0 else '0')
    if D < 3:
        return MC(r, stem, num(d), [num(b * b + 4 * a * c), num(-b * b - 4 * a * c), num(b - 4 * a * c), num(-d)], f'b² − 4ac = {num(b * b)} − 4({num(a)})({num(c)}) = {num(d)}.')
    return MC(r, stem, f'{num(d)}; {nat(d)} real roots', [f'{num(b * b + 4 * a * c)}; {nat(b * b + 4 * a * c)} real roots', f'{num(d)}; {nat(-d) if d else "2"} real roots',
                                                        f'{num(-d)}; {nat(-d)} real roots', f'{num(b - 4 * a * c)}; {nat(b - 4 * a * c)} real roots'],
              f'b² − 4ac = {num(d)}, so {nat(d)} real roots.')


@q12.add('C2', (2, 3, 4), 'explain')
def q12_err(r, D):
    nm = person(r)
    f = r.choice(['plus', 'show', 'all']) if D >= 3 else r.choice(['plus', 'show'])
    if f == 'plus':
        concl = lambda x: 'two distinct real roots' if x > 0 else ('two equal real roots' if x == 0 else 'no real roots')
        for _ in range(30):
            a, b, c = r.randint(1, 5), nz(r, -9, 9), nz(r, -9, 9)
            d, w = b * b - 4 * a * c, b * b + 4 * a * c
            if concl(d) != concl(w):
                break
        else:
            return None
        stem = f'{nm} works out the discriminant of {quad(a, b, c)} = 0 as {num(b * b)} + 4 × {a} × ({num(c)}) = {num(w)} and concludes that the equation has {concl(w)}. Explain the error and state the correct conclusion.'
        return Q(stem, f'The discriminant is b² − 4ac, not b² + 4ac: {num(b * b)} − 4({a})({num(c)}) = {num(d)}, so the equation has {concl(d)}.',
                 f'B1 identifies b² − 4ac; B1 {num(d)} so {concl(d)}')
    if f == 'show':
        for _ in range(30):
            a, b, c = r.randint(1, 6), nz(r, -9, 9), r.randint(1, 15)
            if b * b - 4 * a * c < 0:
                break
        else:
            return None
        stem = f'Show that the equation {quad(a, b, c)} = 0 has no real roots.'
        return Q(stem, f'b² − 4ac = {num(b * b)} − {4 * a * c} = {num(b * b - 4 * a * c)} < 0, so there are no real roots.',
                 f'M1 uses b² − 4ac with a = {a}, b = {num(b)}, c = {c}; A1 {num(b * b - 4 * a * c)} < 0 so no real roots')
    m = nz(r, -7, 7)
    stem = f'Show that the equation x² + (k{sg(m)})x{term(m, 1, "k")} = 0 has real roots for all real values of k.'
    return Q(stem, f'Discriminant = (k{sg(m)})²{term(-4 * m, 1, "k")} = (k{sg(-m)})² ≥ 0 for all k, so the roots are always real.',
             f'M1 discriminant (k{sg(m)})² − 4({num(m)}k); A1 = (k{sg(-m)})² ≥ 0 so real roots for all k')


@q12.add('C3', (1, 2, 3, 4, 5), 'numerical')
def q12_k(r, D):
    if D <= 2:
        s, a = r.randint(1, 9), (1 if D == 1 else r.choice([1, 4, 9]))
        c = s * s
        # a x² + kx + c: k² = 4ac
        k = 2 * s * int(math.isqrt(a))
        stem = f'Find the values of k for which the equation {"" if a == 1 else str(a)}x² + kx + {c} = 0 has two equal real roots.'
        return Q(stem, f'k = ±{k}', f'M1 k² − 4({a})({c}) = 0; A1 k = ±{k}')
    if D == 3:
        for _ in range(40):
            b, c = nz(r, -9, 9), nz(r, -12, 12)
            if (b * b) % c == 0:
                break
        else:
            return None
        k = Fr(b * b, c)
        stem = f'The equation kx² {"+" if 2 * b > 0 else "−"} {abs(2 * b)}x {"+" if c > 0 else "−"} {abs(c)} = 0, where k ≠ 0, has two equal real roots. Find the value of k and the repeated root.'
        root = Fr(-2 * b, 2 * k)
        return Q(stem, f'k = {num(k)}; x = {num(root)}', f'M1 {4 * b * b} − 4k({num(c)}) = 0; A1 k = {num(k)}; B1 x = −b/(2a) = {num(root)}')
    if D == 4:
        m, c, s_ = nz(r, -5, 5), r.randint(-10, 10), nz(r, -4, 4)
        b = m - 2 * s_
        k = c - s_ * s_
        y0 = m * s_ + k
        stem = f'The line y = {lin(m, 0)} + k is a tangent to the curve y = {quad(1, b, c)}. Find the value of k and the coordinates of the point of contact.'
        return Q(stem, f'k = {num(k)}; point ({num(s_)}, {num(y0)})', f'M1 forms {quad(1, b - m, c)} − k = 0; M1 discriminant = 0; A1 k = {num(k)}; M1 x = {num(s_)}; A1 ({num(s_)}, {num(y0)})')
    for _ in range(60):
        p = r.choice([1, 2, 3, -1, -2])
        u = r.randint(-10, 14)
        v = 4 * p - u
        if u != v and (u * v) % 4 == 0 and u * v < 0:
            break
    else:
        return None
    m = -u * v // 4
    stem = f'Find the set of values of k for which the equation x² + kx{term(p, 1, "k")}{sg(m)} = 0 has two distinct real roots.'
    return Q(stem, ineq_out(u, v, var='k'), f'M1 k² − 4({poly([(p, 1), (m, 0)], "k")}) > 0; A1 {poly([(1, 2), (-4 * p, 1), (-4 * m, 0)], "k")} > 0; M1 critical values {num(min(u, v))}, {num(max(u, v))}; A1 {ineq_out(u, v, var="k")}')


@q12.add('C3', (1, 2, 3, 4), 'numerical')
def q12_nat(r, D):
    if D <= 2:
        a, b, c = r.randint(1, 6), nz(r, -12, 12), nz(r, -10, 10)
        d = b * b - 4 * a * c
        concl = 'two distinct real roots' if d > 0 else ('two equal real roots' if d == 0 else 'no real roots')
        return Q(f'Use the discriminant to determine the nature of the roots of {quad(a, b, c)} = 0.', f'Discriminant {num(d)}: {concl}', f'M1 b² − 4ac = {num(d)}; A1 {concl}')
    a, b = r.randint(1, 5), nz(r, -12, 12)
    crit = Fr(b * b, 4 * a)
    want = r.choice(['no real roots', 'two distinct real roots'])
    ans = f'c > {num(crit)}' if want == 'no real roots' else f'c < {num(crit)}'
    stem = f'Find the set of values of the constant c for which the equation {quad(a, b, 0)} + c = 0 has {want}.'
    if D == 4:
        nm = person(r)
        stem = f'{nm} is told that the curve y = {quad(a, b, 0)} + c ' + ('lies entirely above the x-axis.' if want == 'no real roots' else 'crosses the x-axis at two distinct points.') + ' Find the set of possible values of c, explaining your method.'
    return Q(stem, ans, f'M1 discriminant {b * b} − {4 * a}c; M1 sets {"< 0" if want == "no real roots" else "> 0"}; A1 {ans}')


def q12_c4(r, D):
    b, m, c = nz(r, -8, 8), nz(r, -4, 6), r.randint(-6, 12)
    if (b - m) % 2:
        b += 1
    if b == m:
        b += 2
    k0 = c - Fr((b - m) ** 2, 4)
    x0 = Fr(m - b, 2)
    y0 = m * x0 + k0
    intro = f'A curve has equation y = {quad(1, b, c)} and a line has equation y = {lin(m, 0)} + k, where k is a constant.'
    cm = b - m
    parts = [
        P(f'Show that the x-coordinates of any points of intersection satisfy {quad(1, cm, c)} − k = 0.', 'Shown', f'B1 equates {quad(1, b, c)} = {lin(m, 0)} + k and rearranges'),
        P('Find the value of k for which the line is a tangent to the curve.', f'k = {num(k0)}', f'M1 ({num(cm)})² − 4(1)({num(c)} − k) = 0; A1 k = {num(k0)}'),
        P('Find the coordinates of the point of contact when the line is a tangent to the curve.', pt(x0, y0), f'M1 x = {num(x0)}; A1 ({num(x0)}, {num(y0)})'),
        P('Find the set of values of k for which the line meets the curve at two distinct points.', f'k > {num(k0)}', f'M1 discriminant > 0; A1 k > {num(k0)}'),
        P(f'State the number of points of intersection when k = {num(k0 - 3)}.', '0 (the line does not meet the curve)', f'B1 0 (discriminant negative since k < {num(k0)})'),
    ]
    return cmp_(r, intro, parts)


q12.add('C4', (2, 3, 4, 5))(q12_c4)


# ---------------------------------------------------------------- 1.3 quadratic inequalities
q13 = T('Solving quadratic inequalities', 'quadratic inequalities', 'inequalities')
q13.fixed('C1', (1, 2), [
    ('Which is the solution of x² > 16?', 'x < −4 or x > 4', 'Critical values ±4; the curve y = x² − 16 is above the x-axis outside the roots.', ['x > 4', '−4 < x < 4', 'x > ±4']),
    ('Which inequality is true for all real values of x?', 'x² + 1 > 0', 'x² ≥ 0 so x² + 1 ≥ 1 > 0.', ['x² − 1 > 0', 'x² + 1 < 0', 'x² > 1']),
    ('The curve y = (x + 1)(x − 3) lies below the x-axis when', '−1 < x < 3', 'U-shaped curve with roots −1 and 3: negative between the roots.', ['x < −1 or x > 3', 'x < 3', '−3 < x < 1']),
    ('Which is the solution of x² ≤ 9?', '−3 ≤ x ≤ 3', 'Critical values ±3; x² − 9 ≤ 0 between and at the roots.', ['x ≤ 3', 'x ≤ −3 or x ≥ 3', '−3 < x < 3']),
    ('What are the critical values of the inequality x² − 5x + 6 > 0?', '2 and 3', 'x² − 5x + 6 = (x − 2)(x − 3) = 0 when x = 2 or 3.', ['−2 and −3', '1 and 6', '−1 and 6']),
])
q13.fixed('C2', (2, 3), [
    ('Explain why the solution of (x − a)(x − b) < 0 with a < b is a single interval, while the solution of (x − a)(x − b) > 0 is two separate intervals.', 'y = (x − a)(x − b) is a U-shaped curve crossing the x-axis at a and b: it is below the axis only between the roots and above it on both sides.', 'B1 U-shaped sketch/roots a, b; B1 below between, above outside [2]'),
    ('Explain why it is wrong to solve x² < 4x by dividing both sides by x.', 'x may be negative or zero; dividing by a negative reverses the inequality, so information is lost. Rearrange to x(x − 4) < 0 to get 0 < x < 4.', 'B1 sign of x unknown; B1 correct method x(x − 4) < 0 giving 0 < x < 4 [2]'),
    ('Explain why x² > 25 cannot be written as x > ±5.', 'x² > 25 holds for x > 5 and also for x < −5 (e.g. x = −6); "x > ±5" would suggest x > −5, which includes 0 where 0² < 25.', 'B1 counter-example or both regions; B1 x < −5 or x > 5 [2]'),
    ('Describe how a sketch helps to solve a quadratic inequality such as 2x² − x − 3 ≥ 0.', 'Find the roots (−1 and 3/2), sketch the U-shaped curve through them, and read off where the curve is on or above the x-axis: x ≤ −1 or x ≥ 3/2.', 'B1 roots and sketch; B1 reads correct regions with ≥ included [2]'),
])


@q13.add('C1', (1, 2, 3))
def q13_c1(r, D):
    u = r.randint(-9, 8)
    v = u + r.randint(1, 9)
    op = r.choice(['<', '>', '≤', '≥'])
    strict = op in '<>'
    lhs = f'{br(-u)}{br(-v)}' if D < 3 else quad(1, -(u + v), u * v)
    stem = f'Which is the solution of {lhs} {op} 0?'
    inside = op in '<≤'
    c = ineq_in(u, v, strict) if inside else ineq_out(u, v, strict)
    ds = [ineq_out(u, v, strict) if inside else ineq_in(u, v, strict), ineq_in(-v, -u, strict) if inside else ineq_out(-v, -u, strict),
          ineq_in(u, v, not strict) if inside else ineq_out(u, v, not strict), f'x {op} {num(v)}']
    return MC(r, stem, c, ds, f'Critical values {num(u)} and {num(v)}; the U-shaped curve is {"below" if inside else "above"} the x-axis {"between" if inside else "outside"} them.')


@q13.add('C2', (2, 3, 4), 'explain')
def q13_err(r, D):
    nm = person(r)
    f = r.choice(['sqrt', 'div', 'wrongside'])
    if f == 'sqrt':
        k = r.randint(2, 12)
        op = r.choice(['>', '≥'])
        stem = f'{nm} solves x² {op} {k * k} and writes "x {op} {k}". Explain why this answer is incomplete and give the full solution.'
        return Q(stem, f'Negative values also work, e.g. x = −{k + 1} gives {(k + 1) ** 2} {op} {k * k}. Full solution: {ineq_out(-k, k, op == ">")}.',
                 f'B1 explains negative values (counter-example); B1 {ineq_out(-k, k, op == ">")}')
    if f == 'div':
        c = r.randint(2, 11)
        stem = f'{nm} solves x² < {c}x by dividing both sides by x to get x < {c}. Explain the error and find the correct solution set.'
        return Q(stem, f'x could be negative or zero (e.g. x = −1 satisfies x < {c} but 1 < −{c} is false). Correct: x(x − {c}) < 0 so 0 < x < {c}.',
                 f'B1 cannot divide by x of unknown sign (or counter-example); B1 0 < x < {c}')
    u = r.randint(-8, 6)
    v = u + r.randint(2, 9)
    stem = f'{nm} solves {quad(1, -(u + v), u * v)} > 0, finds the critical values {num(u)} and {num(v)}, and writes {ineq_in(u, v)}. Explain the error, using a sketch of y = {quad(1, -(u + v), u * v)}, and give the correct solution.'
    return Q(stem, f'The curve is U-shaped, so it is above the x-axis outside the roots; {nm} gave the region where it is negative. Correct: {ineq_out(u, v)}.',
             f'B1 U-shaped curve positive outside roots; B1 {ineq_out(u, v)}')


@q13.add('C3', (1, 2, 3, 4, 5), 'numerical')
def q13_solve(r, D):
    op = r.choice(['<', '>', '≤', '≥'])
    strict = op in '<>'
    inside = op in '<≤'
    if D <= 2:
        u = r.randint(-9, 8)
        v = u + r.randint(1, 10)
        lhs = quad(1, -(u + v), u * v)
        ans = ineq_in(u, v, strict) if inside else ineq_out(u, v, strict)
        return Q(f'Solve the inequality {lhs} {op} 0.', ans, f'M1 factorises {br(-u)}{br(-v)} or finds critical values {num(u)}, {num(v)}; A1 {ans}')
    if D == 3:
        p, q = r.randint(2, 5), r.choice([1, 2, 3])
        u, v = Fr(nz(r, -7, 7), p), Fr(nz(r, -7, 7), q)
        if u == v:
            return None
        # (p x − p u)(q x − q v)
        a, b, c = p * q, -(p * q) * (u + v), p * q * u * v
        if c.denominator != 1 or b.denominator != 1:
            return None
        lhs = quad(a, int(b), int(c))
        ans = ineq_in(u, v, strict) if inside else ineq_out(u, v, strict)
        return Q(f'Solve the inequality {lhs} {op} 0.', ans, f'M1 factorises or uses formula: critical values {num(min(u, v))} and {num(max(u, v))}; A1 both; A1 {ans}')
    u = r.randint(-9, 6)
    v = u + r.randint(1, 10)
    s = r.randint(-6, 6)
    # x(x + s) op t  where x² + s x − t = (x − u)(x − v) -> s = −(u+v), t = −uv
    if D == 4:
        s, t = -(u + v), -u * v
        lhs = f'x{br(s)}' if s else 'x²'
        ans = ineq_in(u, v, strict) if inside else ineq_out(u, v, strict)
        return Q(f'Find the set of values of x for which {lhs} {op} {num(t)}.', ans, f'M1 rearranges to {quad(1, s, -t)} {op} 0; M1 critical values {num(u)}, {num(v)}; A1 {ans}')
    # D5: both a quadratic inequality and a linear one; find integer values
    w = r.randint(u, v)
    ans_set = [x for x in range(u + 1, v) if x > w]
    if not ans_set:
        return None
    lhs = quad(1, -(u + v), u * v)
    return Q(f'Find the integer values of x that satisfy both {lhs} < 0 and {lin(2, -2 * w)} > 0.', ', '.join(num(x) for x in ans_set),
             f'M1 critical values {num(u)}, {num(v)}; A1 {ineq_in(u, v)}; B1 x > {num(w)}; M1 combines; A1 {", ".join(num(x) for x in ans_set)}')


@q13.add('C3', (3, 4, 5), 'numerical')
def q13_kset(r, D):
    b = r.randint(1, 6)
    for _ in range(30):
        dd = r.choice([x for x in range(1, b * b + 1) if (b * b) % x == 0])
        u, v = dd, -(b * b) // dd
        if r.random() < 0.5:
            u, v = -u, -v
        if u != v:
            break
    m = -(u + v)
    want = r.choice(['no real roots', 'two distinct real roots'])
    km = f'k{sg(m)}' if m else 'k'
    stem = f'Find the set of values of k for which the equation kx² + {2 * b}x + {km} = 0 has {want}.'
    if want == 'no real roots':
        ans = ineq_out(u, v, var='k')
    else:
        ans = ineq_in(u, v, var='k') + ', k ≠ 0'
    return Q(stem, ans, f'M1 discriminant {4 * b * b} − 4k({km}); M1 sets {"< 0" if want == "no real roots" else "> 0"} and simplifies to {poly([(1, 2), (m, 1), (-b * b, 0)], "k")} {">" if want == "no real roots" else "<"} 0; M1 critical values {num(min(u, v))}, {num(max(u, v))}; A1 {ans}')


def q13_c4(r, D):
    for _ in range(40):
        r1 = r.randint(-6, 4)
        r2 = r1 + 2 * r.randint(1, 4)
        x1 = r.randint(-6, 3)
        x2 = x1 + r.randint(2, 7)
        if {x1, x2} != {r1, r2}:
            break
    f = lambda x: (x - r1) * (x - r2)
    b, c = -(r1 + r2), r1 * r2
    m = x1 + x2 + b
    n = f(x1) - m * x1
    h = (r1 + r2) // 2
    intro = f'The curve C has equation y = {quad(1, b, c)} and the line L has equation y = {lin(m, n)}.' if m else f'The curve C has equation y = {quad(1, b, c)} and the line L has equation y = {num(n)}.'
    parts = [
        P('Find the x-coordinates of the points where L meets C.', f'x = {num(x1)} and x = {num(x2)}', f'M1 equates and rearranges to {quad(1, -(x1 + x2), x1 * x2)} = 0; A1 x = {num(x1)}, {num(x2)}'),
        P('Find the set of values of x for which C lies below L.', ineq_in(x1, x2), f'B1 FT {ineq_in(x1, x2)}'),
        P('Find the set of values of x for which y = ' + quad(1, b, c) + ' is negative.', ineq_in(r1, r2), f'M1 roots {num(r1)}, {num(r2)}; A1 {ineq_in(r1, r2)}'),
        P('By completing the square, find the least value of y on C.', num(f(h)), f'M1 {cs(1, -h, f(h))}; A1 least value {num(f(h))}'),
        P(f'Find the set of values of x for which {quad(1, b, c)} ≥ {num(f(h) + 9)}.', ineq_out(h - 3, h + 3, False), f'M1 {sq(-h)} ≥ 9; A1 {ineq_out(h - 3, h + 3, False)}'),
    ]
    return cmp_(r, intro, parts)


q13.add('C4', (2, 3, 4, 5))(q13_c4)


# ---------------------------------------------------------------- 1.4 simultaneous linear and quadratic
q14 = T('Simultaneous equations with one linear and one quadratic equation', 'simultaneous equations', 'one linear and one quadratic')
q14.fixed('C1', (1, 2), [
    ('To solve y = x + 1 and x² + y² = 25 simultaneously, the best first step is to', 'substitute y = x + 1 into x² + y² = 25', 'Substituting the linear equation into the quadratic gives one equation in x.', ['square both equations', 'add the two equations', 'substitute x² + y² = 25 into y = x + 1']),
    ('A line and a parabola are solved simultaneously and the resulting quadratic has discriminant 0. The line', 'is a tangent to the parabola', 'One repeated solution means exactly one point of contact.', ['crosses the parabola twice', 'does not meet the parabola', 'is parallel to the axis of symmetry']),
    ('What is the greatest possible number of solutions of a pair of simultaneous equations, one linear and one quadratic?', '2', 'Substitution gives a single quadratic equation, which has at most two roots.', ['1', '3', '4']),
    ('Substituting y = 2x into xy = 8 gives', '2x² = 8', 'x(2x) = 2x² = 8.', ['x + 2x = 8', '4x² = 8', '2x = 8']),
])
q14.fixed('C2', (2, 3), [
    ('Explain why, after solving a linear and a quadratic equation simultaneously, each x-value must be substituted into the linear equation to find y.', 'Each x-value gives one point of intersection; using the linear equation gives exactly one matching y for each x, whereas the quadratic may give extra values that are not solutions.', 'B1 pairs each x with its own y; B1 linear equation avoids spurious values [2]'),
    ('Explain what it means geometrically if, when solving y = mx + c and y = x² simultaneously, the quadratic in x has no real roots.', 'There are no real solutions, so the line and the curve do not meet.', 'B1 no real roots; B1 line does not intersect the curve [2]'),
    ('Explain why solutions to simultaneous equations should be written as coordinate pairs, such as (2, 5) and (−1, −1).', 'Each solution is a point that satisfies both equations; x = 2 goes only with y = 5, so pairing prevents mixing values.', 'B1 each pair satisfies both; B1 values must not be mixed [2]'),
])


def q14_sys(r, D):
    """Return (description dict) for a random linear-quadratic system with integer solutions."""
    kind = r.choice(['par', 'hyp', 'circ']) if D >= 3 else 'par'
    if kind == 'par':
        a = 1 if D <= 3 else r.randint(1, 3)
        b, c = r.randint(-6, 6), r.randint(-8, 8)
        x1 = r.randint(-5, 3)
        x2 = x1 + r.randint(1, 6)
        f = lambda x: a * x * x + b * x + c
        m = Fr(f(x2) - f(x1), x2 - x1)
        n = f(x1) - m * x1
        return {'curve': f'y = {quad(a, b, c)}', 'line': line_eq(m, n), 'pts': [(x1, f(x1)), (x2, f(x2))],
                'sub': f'{quad(a, b - m, c - n)} = 0' if True else '', 'kind': kind}
    if kind == 'hyp':
        for _ in range(50):
            k = r.choice([6, 8, 12, 18, 20, 24, 30, 36])
            ds = [d for d in range(-k, k + 1) if d and k % d == 0]
            p, q = r.sample(ds, 2)
            if (k // p - k // q) % (q - p) == 0 and q != p:
                break
        else:
            return None
        P1, P2 = (p, k // p), (q, k // q)
        m = Fr(P2[1] - P1[1], P2[0] - P1[0])
        n = P1[1] - m * P1[0]
        return {'curve': f'xy = {k}', 'line': line_eq(m, n), 'pts': [P1, P2], 'sub': f'{quad(*intq(m, n, -k))} = 0', 'kind': kind}
    R = r.choice([25, 50, 65, 85, 100, 125, 130, 145, 169, 170])
    lat = [(x, y) for x in range(-13, 14) for y in range(-13, 14) if x * x + y * y == R]
    for _ in range(50):
        P1, P2 = r.sample(lat, 2)
        if P1[0] != P2[0] and P1[1] != P2[1]:
            break
    else:
        return None
    m = Fr(P2[1] - P1[1], P2[0] - P1[0])
    n = P1[1] - m * P1[0]
    eq = gen_line(m, -1, n)
    A = 1 + m * m
    return {'curve': f'x² + y² = {R}', 'line': eq, 'pts': sorted([P1, P2]), 'sub': f'{quad(*intq(A, 2 * m * n, n * n - R))} = 0', 'kind': kind}


@q14.add('C1', (1, 2, 3))
def q14_c1(r, D):
    m, c, R = nz(r, -4, 4), nz(r, -6, 6), r.choice([10, 13, 20, 25, 29, 34, 40])
    stem = f'The line y = {lin(m, c)} meets the circle x² + y² = {R}. Which quadratic equation in x is obtained by substitution?'
    A, B, C = 1 + m * m, 2 * m * c, c * c - R
    return MC(r, stem, f'{quad(A, B, C)} = 0', [f'{quad(A, 0, C)} = 0', f'{quad(1 + m, B, C)} = 0', f'{quad(A, B, c - R)} = 0', f'{quad(A, -B, C)} = 0', f'{quad(A, m * c, C)} = 0'],
              f'x² + ({lin(m, c)})² = {R} → x² + {quad(m * m, 2 * m * c, c * c)} = {R} → {quad(A, B, C)} = 0.')


@q14.add('C2', (2, 3, 4), 'explain')
def q14_err(r, D):
    nm = person(r)
    f = r.choice(['square', 'pair', 'tangent'])
    if f == 'square':
        s, R = r.randint(2, 9), None
        R = r.choice([x for x in range(s * s // 2 + 1, s * s + 30) if x != s * s])
        stem = f'{nm} solves x + y = {s} and x² + y² = {R}. {nm} writes y = {s} − x and then x² + {s * s} − x² = {R}, so {s * s} = {R}, and concludes there are no solutions. Explain the error and write down the correct quadratic equation in x.'
        return Q(stem, f'({s} − x)² ≠ {s * s} − x²; it equals {quad(1, -2 * s, s * s)}. Correct equation: {quad(2, -2 * s, s * s - R)} = 0.',
                 f'B1 identifies ({s} − x)² expanded wrongly; B1 {quad(2, -2 * s, s * s - R)} = 0 (or simplified equivalent)')
    if f == 'pair':
        sy = q14_sys(r, 2)
        (x1, y1), (x2, y2) = sy['pts']
        stem = f'{nm} solves {sy["line"]} and {sy["curve"]} simultaneously and writes the answer as "x = {num(x1)} or {num(x2)}, y = {num(y1)} or {num(y2)}". Explain why this answer is not acceptable and state it correctly.'
        return Q(stem, f'The values must be paired as points; e.g. x = {num(x1)} does not go with y = {num(y2)}. Solutions: {pt(x1, y1)} and {pt(x2, y2)}.',
                 f'B1 explains pairing (mixing gives points not on both graphs); B1 {pt(x1, y1)} and {pt(x2, y2)}')
    m, b, c = nz(r, -4, 4), r.randint(-5, 5), r.randint(-6, 6)
    s = nz(r, -3, 3)
    b = m - 2 * s
    k = c - s * s
    stem = f'Show that the line y = {lin(m, k)} is a tangent to the curve y = {quad(1, b, c)}, and explain how your working shows this.'
    return Q(stem, f'Substitution gives {quad(1, -2 * s, s * s)} = 0, i.e. {sq(-s)} = 0, which has a repeated root x = {num(s)}; a single point of contact means the line is a tangent.',
             f'M1 eliminates y to get {quad(1, -2 * s, s * s)} = 0; A1 discriminant 0 / repeated root so tangent at x = {num(s)}')


@q14.add('C3', (1, 2, 3, 4, 5), 'numerical')
def q14_solve(r, D):
    sy = q14_sys(r, D)
    if not sy:
        return None
    (x1, y1), (x2, y2) = sy['pts']
    stem = f'Solve the simultaneous equations {sy["line"]} and {sy["curve"]}.'
    key = f'M1 substitutes to obtain {sy["sub"]}; M1 solves; A1 x = {num(x1)}, {num(x2)}; A1 y = {num(y1)}, {num(y2)}'
    if D >= 4:
        dist = (x2 - x1) ** 2 + (y2 - y1) ** 2
        stem = f'The line {sy["line"]} meets the curve {sy["curve"]} at the points A and B. Find the coordinates of A and B and the exact length of AB.'
        return Q(stem, f'{pt(x1, y1)} and {pt(x2, y2)}; AB = {rt(dist)}', key + f'; M1 √(({num(x2 - x1)})² + ({num(y2 - y1)})²); A1 {rt(dist)}')
    if D == 1:
        x1, d = r.randint(-4, 5), r.randint(-6, 6)
        x2 = 1 - x1
        if x1 == x2:
            return None
        c0 = d + x1 * (1 - x1)
        stem = f'Solve the simultaneous equations y = {lin(1, d)} and y = {quad(1, 0, c0)}.'
        return Q(stem, f'{pt(x1, x1 + d)} and {pt(x2, x2 + d)}', f'M1 {quad(1, -1, c0 - d)} = 0; A1 x = {num(x1)}, {num(x2)}; A1 y = {num(x1 + d)}, {num(x2 + d)}')
    return Q(stem, f'{pt(x1, y1)} and {pt(x2, y2)}', key)


@q14.add('C3', (2, 3, 4), 'numerical')
def q14_ctx(r, D):
    nm = person(r)
    # rectangle: perimeter 2(x + y) = P, area xy = A
    x, y = r.randint(3, 15), r.randint(3, 15)
    if x == y:
        y += 1
    what = r.choice(['garden plot', 'solar panel', 'sports pitch model', 'poster', 'tile', 'window'])
    P_, A_ = 2 * (x + y), x * y
    unit = 'm' if what in ('garden plot', 'sports pitch model') else 'cm'
    stem = f'{nm} designs a rectangular {what} with perimeter {P_} {unit} and area {A_} {unit}². By forming and solving a pair of simultaneous equations, find the length and width of the {what}.'
    if D >= 4:
        d2 = x * x + y * y
        stem = f'A rectangular {what} has a perimeter of {P_} {unit} and a diagonal of length {rt(d2)} {unit}. By forming and solving simultaneous equations, find the dimensions of the {what}.'
        return Q(stem, f'{max(x, y)} {unit} by {min(x, y)} {unit}', f'B1 x + y = {x + y}; B1 x² + y² = {d2}; M1 substitutes y = {x + y} − x; A1 {quad(2, -2 * (x + y), (x + y) ** 2 - d2)} = 0 (or simplified); A1 {max(x, y)} and {min(x, y)}')
    return Q(stem, f'{max(x, y)} {unit} by {min(x, y)} {unit}', f'B1 x + y = {x + y} and xy = {A_}; M1 substitutes to get {quad(1, -(x + y), A_)} = 0; A1 {max(x, y)} and {min(x, y)}')


def q14_c4(r, D):
    sy = q14_sys(r, max(D, 3))
    if not sy:
        return None
    (x1, y1), (x2, y2) = sy['pts']
    mx, my = Fr(x1 + x2, 2), Fr(y1 + y2, 2)
    dist = (x2 - x1) ** 2 + (y2 - y1) ** 2
    intro = f'The line {sy["line"]} intersects the curve {sy["curve"]} at the points A and B, where A has the smaller x-coordinate.'
    parts = [
        P('Find the coordinates of A and B.', f'A{pt(x1, y1)}, B{pt(x2, y2)}', f'M1 substitutes: {sy["sub"]}; M1 solves; A1 x-values; A1 both points'),
        P('Find the exact length of AB.', rt(dist), f'M1 distance formula; A1 {rt(dist)}'),
        P('Find the coordinates of the midpoint of AB.', pt(mx, my), f'B1 FT {pt(mx, my)}'),
    ]
    if y1 != y2:
        g = Fr(y2 - y1, x2 - x1)
        pm = -1 / g
        parts.append(P('Find the equation of the perpendicular bisector of AB, giving your answer in the form ax + by + c = 0.', gen_line(pm, -1, my - pm * mx), f'B1 gradient {num(pm)}; M1 line through midpoint {pt(mx, my)}; A1 {gen_line(pm, -1, my - pm * mx)}'))
    return cmp_(r, intro, parts)


q14.add('C4', (2, 3, 4, 5))(q14_c4)


# ---------------------------------------------------------------- 1.5 reducible to quadratic
q15 = T('Equations reducible to quadratic form, e.g. in x² or √x', 'equations reducible to quadratic form', 'quadratic form', 'disguised quadratic')
q15.fixed('C1', (1, 2), [
    ('Which substitution turns x⁴ − 13x² + 36 = 0 into a quadratic equation?', 'u = x²', 'x⁴ = (x²)², so with u = x² the equation is u² − 13u + 36 = 0.', ['u = x⁴', 'u = √x', 'u = 1/x']),
    ('Which substitution turns x − 5√x + 6 = 0 into a quadratic equation?', 'u = √x', 'x = (√x)², so with u = √x the equation is u² − 5u + 6 = 0.', ['u = x²', 'u = x − 5', 'u = 1/√x']),
    ('Using u = x², the equation x⁴ + 3x² − 4 = 0 becomes u² + 3u − 4 = 0 with roots u = 1, u = −4. How many real values of x are there?', '2', 'x² = 1 gives x = ±1; x² = −4 has no real solutions.', ['4', '1', '0']),
    ('Using u = √x, an equation gives u = 3 or u = −2. The solution of the original equation is', 'x = 9 only', '√x = 3 gives x = 9; √x = −2 is impossible since √x ≥ 0.', ['x = 9 or x = 4', 'x = 3 or x = −2', 'x = 9 or x = −4']),
    ('Which substitution turns 2x^(2/3) − 5x^(1/3) + 2 = 0 into a quadratic?', 'u = x^(1/3)', 'x^(2/3) = (x^(1/3))².', ['u = x^(2/3)', 'u = x³', 'u = x^(3/2)']),
])
q15.fixed('C2', (2, 3), [
    ('Explain why the substitution u = √x can lead to a value of u that must be rejected.', '√x denotes the non-negative square root, so a negative value of u (e.g. u = −2) gives no value of x.', 'B1 √x ≥ 0; B1 negative u rejected [2]'),
    ('Explain why x⁴ − 5x² + 4 = 0 has four real roots but x⁴ + 3x² − 4 = 0 has only two.', 'The first gives x² = 1 or 4, both positive, so x = ±1, ±2. The second gives x² = 1 or −4; x² = −4 has no real solution, leaving x = ±1.', 'B1 first: two positive values of x², four roots; B1 second: x² = −4 impossible, two roots [2]'),
    ('Explain why solving an equation in √x by squaring both sides can introduce roots that do not satisfy the original equation.', 'Squaring is not reversible: a = b and a = −b both give a² = b², so solutions of the squared equation must be checked in the original.', 'B1 squaring loses the sign; B1 must check solutions [2]'),
])


@q15.add('C1', (1, 2, 3))
def q15_c1(r, D):
    u1, u2 = r.sample([x for x in range(-6, 10) if x], 2)
    kind = r.choice(['x2', 'sqrt'])
    s, p = u1 + u2, u1 * u2
    if kind == 'x2':
        eq = poly([(1, 4), (-s, 2), (p, 0)])
        roots = sorted({x for u in (u1, u2) if u > 0 and math.isqrt(u) ** 2 == u for x in (math.isqrt(u), -math.isqrt(u))})
        if not roots:
            return None
        c = ', '.join(num(x) for x in roots)
        ds = [', '.join(num(u) for u in sorted((u1, u2))), ', '.join(num(x) for x in roots if x > 0) + ', ' + num(u1 * u1), ', '.join(num(x) for x in sorted({abs(u1), abs(u2), -abs(u1), -abs(u2)})), num(max(roots) + 1) + ', ' + num(-max(roots) - 1)]
        return MC(r, f'Find all the real roots of {eq} = 0.', c, ds, f'u = x²: {poly([(1, 2), (-s, 1), (p, 0)], "u")} = 0 gives u = {num(u1)}, {num(u2)}; x² must be ≥ 0 and x = ±√u.')
    if s == 0:
        return None
    eq = f'x{term(-s, Fr(1, 2))}{sg(p)} = 0'.replace('x^(1/2)', '√x')
    good = sorted(u * u for u in (u1, u2) if u >= 0)
    if not good:
        return None
    c = ' or '.join(f'x = {num(x)}' for x in good)
    ds = [' or '.join(f'x = {num(u)}' for u in sorted((u1, u2))), ' or '.join(f'x = {num(u * u)}' for u in sorted({u1, u2})) if len(good) == 1 else f'x = {num(good[0])} only',
          f'x = {num(max(u1, u2) ** 2 + 1)}', f'x = {num(-u1 * u1)} or x = {num(u2 * u2)}']
    return MC(r, f'Solve the equation {eq}.', c, ds, f'u = √x: u = {num(u1)} or {num(u2)}; √x ≥ 0, then square.')


@q15.add('C2', (2, 3, 4), 'explain')
def q15_err(r, D):
    nm = person(r)
    a, b = r.sample(range(1, 8), 2)
    if r.random() < 0.5:
        # √x equation with roots u = a, u = −b
        eq = f'x{term(b - a, Fr(1, 2))}{sg(-a * b)} = 0'.replace('x^(1/2)', '√x')
        stem = f'{nm} solves {eq} using u = √x, obtains u = {a} or u = −{b}, and gives the answer x = {a * a} or x = {b * b}. Explain the error.'
        return Q(stem, f'√x cannot be negative, so u = −{b} must be rejected; checking, x = {b * b} gives {2 * b * (b - a)} ≠ 0. Only x = {a * a}.',
                 f'B1 √x ≥ 0 so u = −{b} rejected (or checks x = {b * b} fails); B1 x = {a * a} only')
    eq = poly([(1, 4), (b * b - a * a, 2), (-(a * a) * (b * b), 0)])
    stem = f'{nm} solves {eq} = 0 with u = x², gets u = {a * a} or u = −{b * b}, and writes the solutions as x = {a} or x = −{b}. Explain what {nm} has done wrong and give the correct real solutions.'
    return Q(stem, f'u = x², so x² = {a * a} gives x = ±{a}; x² = −{b * b} has no real solutions (and u is not x). Correct: x = {a} or x = −{a}.',
             f'B1 x² = −{b * b} has no real roots; B1 x = ±{a}')


@q15.add('C3', (1, 2, 3, 4, 5), 'numerical')
def q15_solve(r, D):
    if D <= 2:
        a, b = r.sample(range(1, 8), 2)
        A, B = a * a, b * b
        eq = poly([(1, 4), (-(A + B), 2), (A * B, 0)])
        return Q(f'Solve the equation {eq} = 0.', f'x = ±{a} or x = ±{b}', f'M1 u = x²: u² − {A + B}u + {A * B} = 0; A1 u = {A}, {B}; A1 x = ±{a}, ±{b}')
    if D == 3:
        a, b = r.randint(1, 9), r.randint(1, 9)
        if r.random() < 0.5:
            s, p = a + b, a * b
            good = sorted({a * a, b * b})
            note = ''
        else:
            s, p = a - b, -a * b
            good = [a * a]
            note = f'; u = −{b} rejected since √x ≥ 0'
        if s == 0:
            return None
        eq = f'x{term(-s, Fr(1, 2))}{sg(p)} = 0'.replace('x^(1/2)', '√x')
        return Q(f'Solve the equation {eq}.', ' or '.join(f'x = {g}' for g in good), f'M1 u = √x: {poly([(1, 2), (-s, 1), (p, 0)], "u")} = 0; A1 u values{note}; A1 ' + ' or '.join(f'x = {g}' for g in good))
    if D == 4:
        # (2u − p)(u − q) with u = √x: 2x − (p + 2q)√x + pq = 0
        p, q = r.choice([1, 3, 5, 7]), r.randint(1, 6)
        eq = f'2x − {p + 2 * q}√x + {p * q} = 0'
        xs = sorted({Fr(p * p, 4), Fr(q * q)})
        return Q(f'Solve the equation {eq}, giving your answers as exact values.', ' or '.join(f'x = {num(x)}' for x in xs),
                 f'M1 u = √x: 2u² − {p + 2 * q}u + {p * q} = 0; M1 factorises ({"2u − " + str(p)})(u − {q}); A1 u = {num(Fr(p, 2))}, {q}; A1 ' + ' or '.join(f'x = {num(x)}' for x in xs))
    # D5: x^(2/3) or 1/x² forms
    if r.random() < 0.5:
        a, b = r.sample([-3, -2, -1, 1, 2, 3, 4], 2)
        s, p = a + b, a * b
        eq = f'x^(2/3){term(-s, Fr(1, 3))}{sg(p)} = 0'.replace(' + 0x', '').replace(' − 0x', '')
        if s == 0:
            return None
        return Q(f'Solve the equation {eq}.', f'x = {num(a ** 3)} or x = {num(b ** 3)}', f'M1 u = x^(1/3): {poly([(1, 2), (-s, 1), (p, 0)], "u")} = 0; A1 u = {num(a)}, {num(b)}; M1 cubes; A1 x = {num(a ** 3)}, {num(b ** 3)}')
    a, b = r.sample(range(1, 7), 2)
    # 1/x² form: (1/x²) ... use x² − k + m/x² = 0 -> x⁴ − k x² + m = 0 with x² = a², b²
    A, B = a * a, b * b
    eq = f'x² + {A * B}/x² = {A + B}'
    return Q(f'Solve the equation {eq}.', f'x = ±{a} or x = ±{b}', f'M1 × x²: x⁴ − {A + B}x² + {A * B} = 0; M1 u = x²; A1 u = {A}, {B}; A1 x = ±{a}, ±{b}')


def q15_c4(r, D):
    a, b = r.sample(range(1, 8), 2)
    s, p = a + b, a * b
    intro = f'The curve C has equation y = x − {s}√x + {p}, for x ≥ 0.'
    parts = [
        P('Using the substitution u = √x, find the coordinates of the points where C meets the x-axis.', f'({a * a}, 0) and ({b * b}, 0)',
          f'M1 u² − {s}u + {p} = 0; A1 u = {a}, {b}; A1 x = {a * a}, {b * b}'),
        P('Write down the coordinates of the point where C meets the y-axis.', f'(0, {p})', f'B1 (0, {p})'),
        P(f'Find the x-coordinates of the points where C meets the line y = {p - s + 1}.',
          f'x = 1 or x = {(s - 1) ** 2}', f'M1 u² − {s}u + {s - 1} = 0; A1 u = 1, {s - 1}; A1 x = 1, {(s - 1) ** 2}'),
        P(f'Solve the equation x⁴ − {a * a + b * b}x² + {a * a * b * b} = 0.', f'x = ±{a} or x = ±{b}', f'M1 u = x²; A1 u = {a * a}, {b * b}; A1 x = ±{a}, ±{b}'),
        P('By writing y in the form (√x − p)² + q, find the least value of y and the value of x at which it occurs.', f'least value {num(Fr(p) - Fr(s * s, 4))} when x = {num(Fr(s * s, 4))}',
          f'M1 (√x − {num(Fr(s, 2))})²{sg(Fr(p) - Fr(s * s, 4))}; A1 least value {num(Fr(p) - Fr(s * s, 4))}; A1 x = {num(Fr(s * s, 4))}'),
    ]
    return cmp_(r, intro, parts)


q15.add('C4', (2, 3, 4, 5))(q15_c4)

CHAPTERS[1] = [q11, q12, q13, q14, q15]


# ================================================================ Chapter 2 Functions

def fx_lin(a, b):
    return lin(a, b)


f21 = T('Domain and range of a function and mappings', 'domain and range', 'mappings', 'one-one')
f21.fixed('C1', (1, 2), [
    ('A mapping in which every element of the domain has exactly one image, and no two elements share an image, is called', 'one-one', 'Each input has one output and each output comes from only one input.', ['many-one', 'one-many', 'many-many']),
    ('The function f(x) = x² for x ∈ ℝ is', 'many-one', 'f(2) = f(−2) = 4, so two inputs share an image.', ['one-one', 'one-many', 'not a function']),
    ('What is the range of f(x) = x² + 3 for x ∈ ℝ?', 'f(x) ≥ 3', 'x² ≥ 0 so x² + 3 ≥ 3, and every value ≥ 3 is reached.', ['f(x) > 3', 'f(x) ≥ 0', 'f(x) ∈ ℝ']),
    ('What is the largest possible domain of f(x) = √(x − 4)?', 'x ≥ 4', 'The expression under the root must be non-negative: x − 4 ≥ 0.', ['x > 4', 'x ≥ 0', 'x ≤ 4']),
    ('What is the range of f(x) = 1/x for x > 0?', 'f(x) > 0', 'For positive x, 1/x is positive and takes every positive value; it is never 0.', ['f(x) ≥ 0', 'f(x) ∈ ℝ', 'f(x) > 1']),
    ('Which of these is not a function from ℝ to ℝ?', 'x ↦ ±√x', '±√x gives two images for x > 0 (and none for x < 0), so it is not a function.', ['x ↦ x³', 'x ↦ 2x − 5', 'x ↦ |x|']),
])
f21.fixed('C2', (2, 3), [
    ('Explain why f(x) = x² − 4x, x ∈ ℝ, is not a one-one function.', 'Different inputs give the same output: f(0) = f(4) = 0, so it is many-one (the graph is symmetrical about x = 2).', 'B1 example of two inputs with equal images; B1 hence many-one [2]'),
    ('Explain the difference between the domain and the range of a function.', 'The domain is the set of input values for which the function is defined; the range is the set of output values that the function actually takes.', 'B1 domain = inputs; B1 range = outputs/images [2]'),
    ('Explain how the horizontal line test shows whether a function is one-one.', 'If every horizontal line meets the graph at most once, no output comes from two inputs, so the function is one-one.', 'B1 horizontal line meets graph at most once; B1 links to each image having one input [2]'),
    ('Explain why the range of f(x) = (x − 3)² + 1 for x ≥ 5 is f(x) ≥ 5 and not f(x) ≥ 1.', 'For x ≥ 5 the function is increasing (the vertex x = 3 is outside the domain), so the least value is f(5) = 5.', 'B1 vertex not in domain / f increasing for x ≥ 5; B1 least value f(5) = 5 [2]'),
])


def lin_range(a, b, p, q):
    lo, hi = sorted((a * p + b, a * q + b))
    return lo, hi


@f21.add('C1', (1, 2, 3))
def f21_c1(r, D):
    a, b = nz(r, -5, 6), r.randint(-9, 9)
    p = r.randint(-5, 2)
    q = p + r.randint(2, 7)
    lo, hi = lin_range(a, b, p, q)
    s = '≤' if D < 3 else '<'
    stem = f'The function f is defined by f(x) = {lin(a, b)} for {num(p)} {s} x {s} {num(q)}. Find the range of f.'
    c = f'{num(lo)} {s} f(x) {s} {num(hi)}'
    ds = [f'{num(p)} {s} f(x) {s} {num(q)}', f'{num(lo - b)} {s} f(x) {s} {num(hi - b)}' if b else f'{num(lo)} {s} f(x) {s} {num(hi + 1)}', f'f(x) {"≥" if s == "≤" else ">"} {num(lo)}',
          f'{num(lo)} {"<" if s == "≤" else "≤"} f(x) {"<" if s == "≤" else "≤"} {num(hi)}']
    return MC(r, stem, c, ds, f'f is linear, so the extreme values occur at the ends: f({num(p)}) = {num(a * p + b)}, f({num(q)}) = {num(a * q + b)}.')


@f21.add('C2', (2, 3, 4), 'explain')
def f21_err(r, D):
    nm = person(r)
    h, k = r.randint(-4, 5), r.randint(-9, 9)
    f = lambda x: (x - h) ** 2 + k
    if r.random() < 0.55:
        a = h - r.randint(1, 4)
        b = h + r.randint(1, 5)
        lo_w, hi_w = sorted((f(a), f(b)))
        stem = f'The function f is defined by f(x) = {quad(1, -2 * h, h * h + k)} for {num(a)} ≤ x ≤ {num(b)}. {nm} says the range is {num(lo_w)} ≤ f(x) ≤ {num(hi_w)} because f({num(a)}) = {num(f(a))} and f({num(b)}) = {num(f(b))}. Explain why {nm} is wrong and state the correct range.'
        return Q(stem, f'The vertex x = {num(h)} lies inside the domain, so the least value is f({num(h)}) = {num(k)}, not an end value. Range {num(k)} ≤ f(x) ≤ {num(max(f(a), f(b)))}.',
                 f'B1 minimum at vertex ({num(h)}, {num(k)}) inside the domain; B1 {num(k)} ≤ f(x) ≤ {num(max(f(a), f(b)))}')
    c = h + r.randint(-3, 3)
    one = c >= h
    stem = f'The function g is defined by g(x) = {quad(1, -2 * h, h * h + k)} for x ≥ {num(c)}. Determine, with a reason, whether g is one-one.'
    if one:
        return Q(stem, f'Yes: g(x) = {cs(1, -h, k)} has its vertex at x = {num(h)}, and for x ≥ {num(c)} the function is increasing, so it is one-one.',
                 f'B1 vertex at x = {num(h)}; B1 domain lies on one side of the vertex so one-one')
    return Q(stem, f'No: the vertex is at x = {num(h)} > {num(c)}, so values on either side of x = {num(h)} give equal images, e.g. g({num(h - 1)}) = g({num(h + 1)}) = {num(k + 1)}.',
             f'B1 vertex at x = {num(h)} inside domain; B1 example of equal images so not one-one')


@f21.add('C3', (1, 2, 3, 4, 5), 'numerical')
def f21_range(r, D):
    if D <= 2:
        a, b = nz(r, -6, 6), r.randint(-12, 12)
        p = r.randint(-6, 3)
        q = p + r.randint(2, 8)
        lo, hi = lin_range(a, b, p, q)
        return Q(f'The function f is defined by f(x) = {lin(a, b)} for {num(p)} ≤ x ≤ {num(q)}. Find the range of f.', f'{num(lo)} ≤ f(x) ≤ {num(hi)}',
                 f'M1 evaluates f({num(p)}) and f({num(q)}); A1 {num(lo)} ≤ f(x) ≤ {num(hi)}')
    h, k = nz(r, -5, 5), r.randint(-12, 12)
    a = 1 if D <= 4 else r.randint(2, 3)
    f = lambda x: a * (x - h) ** 2 + k
    if D == 3:
        return Q(f'The function f is defined by f(x) = {quad(a, -2 * a * h, a * h * h + k)} for x ∈ ℝ. Find the range of f.', f'f(x) ≥ {num(k)}',
                 f'M1 completes the square {cs(a, -h, k)}; A1 f(x) ≥ {num(k)}')
    p = h - r.randint(1, 4)
    q = h + r.randint(1, 5)
    return Q(f'The function f is defined by f(x) = {quad(a, -2 * a * h, a * h * h + k)} for {num(p)} ≤ x ≤ {num(q)}. Find the range of f.',
             f'{num(k)} ≤ f(x) ≤ {num(max(f(p), f(q)))}', f'M1 completes the square {cs(a, -h, k)}; A1 least value {num(k)} at x = {num(h)}; M1 evaluates f({num(p)}) = {num(f(p))} and f({num(q)}) = {num(f(q))}; A1 {num(k)} ≤ f(x) ≤ {num(max(f(p), f(q)))}')


@f21.add('C3', (2, 3, 4), 'numerical')
def f21_onek(r, D):
    a = r.randint(1, 3)
    h, k = nz(r, -6, 6), r.randint(-10, 10)
    which = r.choice(['least', 'greatest'])
    rel = '≥' if which == 'least' else '≤'
    stem = f'The function f is defined by f(x) = {quad(a, -2 * a * h, a * h * h + k)} for x {rel} c. Find the {which} value of the constant c for which f is one-one' + (', and state the range of f for this value of c.' if D >= 3 else '.')
    key = f'M1 completes the square or finds vertex x = {num(h)}; A1 c = {num(h)}' + (f'; B1 range f(x) ≥ {num(k)}' if D >= 3 else '')
    return Q(stem, f'c = {num(h)}' + (f'; f(x) ≥ {num(k)}' if D >= 3 else ''), key)


def f21_c4(r, D):
    h, k = nz(r, -4, 4), r.randint(-9, 6)
    t = r.randint(2, 5)
    p = h - r.randint(1, 3)
    q = h + r.randint(2, 5)
    f = lambda x: (x - h) ** 2 + k
    intro = f'The function f is defined by f(x) = {quad(1, -2 * h, h * h + k)} for {num(p)} ≤ x ≤ {num(q)}.'
    hi = max(f(p), f(q))
    sols = [x for x in (h - t, h + t) if p <= x <= q]
    parts = [
        P('Express f(x) in the form (x − a)² + b.', cs(1, -h, k), f'B1 a = {num(h)}; B1 b = {num(k)}'),
        P('Find the range of f.', f'{num(k)} ≤ f(x) ≤ {num(hi)}', f'B1 least value {num(k)}; M1 checks both end values; A1 {num(k)} ≤ f(x) ≤ {num(hi)}'),
        P('Explain why f is not one-one.', f'The vertex x = {num(h)} lies inside the domain, so e.g. f({num(h - 1)}) = f({num(h + 1)}).', f'B1 vertex inside domain with equal images example'),
        P(f'The domain is changed to x ≥ m. Find the least value of m for which f is one-one.', f'm = {num(h)}', f'B1 m = {num(h)}'),
    ]
    if sols:
        parts.append(P(f'Solve the equation f(x) = {num(k + t * t)}.', ' or '.join(f'x = {num(x)}' for x in sols),
                       f'M1 (x{sg(-h)})² = {t * t}; A1 x = {num(h - t)}, {num(h + t)}; B1 rejects values outside the domain' if len(sols) == 1 else f'M1 (x{sg(-h)})² = {t * t}; A1 x = {num(h - t)}, {num(h + t)}'))
    return cmp_(r, intro, parts)


f21.add('C4', (2, 3, 4, 5))(f21_c4)


# ---------------------------------------------------------------- 2.2 composite functions
f22 = T('Composite functions and conditions for existence', 'composite functions', 'conditions for existence')
f22.fixed('C1', (1, 2), [
    ('The composite function fg(x) means', 'f(g(x)): apply g first, then f', 'In fg the function nearest x, g, acts first.', ['g(f(x)): apply f first, then g', 'f(x) × g(x)', 'f(x) + g(x)']),
    ('For the composite function fg to exist, which condition must hold?', 'the range of g lies within the domain of f', 'Every output of g must be a valid input of f.', ['the range of f lies within the domain of g', 'the domain of f equals the domain of g', 'f and g are both one-one']),
    ('f(x) = x + 3 and g(x) = 2x. Which expression is gf(x)?', '2x + 6', 'gf(x) = g(x + 3) = 2(x + 3) = 2x + 6.', ['2x + 3', '2x² + 6x', 'x + 6']),
    ('f(x) = x² and g(x) = x − 1. Which expression is fg(x)?', '(x − 1)²', 'fg(x) = f(x − 1) = (x − 1)².', ['x² − 1', 'x²(x − 1)', 'x − 1']),
    ('f(x) = 3x − 2. What is ff(x)?', '9x − 8', 'ff(x) = 3(3x − 2) − 2 = 9x − 8.', ['9x² − 4', '6x − 4', '9x − 2']),
])
f22.fixed('C2', (2, 3), [
    ('Explain why, in general, fg(x) ≠ gf(x), using f(x) = x² and g(x) = x + 1.', 'fg(x) = (x + 1)² = x² + 2x + 1 while gf(x) = x² + 1; the order of the functions changes the result.', 'B1 both composites correct; B1 states they differ so order matters [2]'),
    ('f(x) = √x for x ≥ 0 and g(x) = x − 5 for x ∈ ℝ. Explain why fg does not exist.', 'g can take negative values (e.g. g(0) = −5), which are not in the domain of f, so the range of g is not contained in the domain of f.', 'B1 range of g includes negatives; B1 not within domain of f [2]'),
    ('Explain why the domain of fg is the same as the domain of g when fg exists.', 'fg(x) = f(g(x)) starts by applying g, so x must be a valid input of g; if fg exists every g(x) is already in the domain of f.', 'B1 g acts first; B1 no further restriction when range g ⊆ domain f [2]'),
])


@f22.add('C1', (1, 2, 3))
def f22_c1(r, D):
    a, b, c = nz(r, -4, 5), nz(r, -7, 7), r.randint(-6, 6)
    t = nz(r, -4, 4)
    f = lambda x: a * x + b
    g = lambda x: x * x + c
    which = r.choice(['fg', 'gf'])
    val = f(g(t)) if which == 'fg' else g(f(t))
    other = g(f(t)) if which == 'fg' else f(g(t))
    stem = f'The functions f and g are defined for x ∈ ℝ by f(x) = {lin(a, b)} and g(x) = {quad(1, 0, c)}. Find {which}({num(t)}).'
    return MC(r, stem, num(val), [num(other), num(f(t) * g(t)), num(f(t) + g(t)), num(val + 2 * b)], f'{which}({num(t)}) = {"f(g(" if which == "fg" else "g(f("}{num(t)})) = {num(val)}.')


@f22.add('C2', (2, 3, 4), 'explain')
def f22_err(r, D):
    nm = person(r)
    fr = r.choice(['order', 'exist'])
    if fr == 'order':
        a, b, c = nz(r, 2, 5), nz(r, -7, 7), nz(r, -6, 6)
        stem = f'f(x) = {lin(a, b)} and g(x) = {quad(1, 0, c)} for x ∈ ℝ. {nm} writes fg(x) = {poly([(a * a, 2), (2 * a * b, 1), (b * b + c, 0)])}. Explain the error and find fg(x) correctly.'
        return Q(stem, f'{nm} found gf(x) = ({lin(a, b)})²{sg(c)} (applied f first). fg(x) = f(g(x)) = {a}({quad(1, 0, c)}){sg(b)} = {quad(a, 0, a * c + b)}.',
                 f'B1 identifies that g must be applied first ({nm} found gf); B1 fg(x) = {quad(a, 0, a * c + b)}')
    d = r.randint(-5, 6)
    q = d + r.choice([-3, -2, -1, 1, 2, 3])
    exists = q >= d
    stem = f'The functions f and g are defined by f(x) = {quad(1, 0, q)} for x ∈ ℝ and g(x) = √({xk(d)}) for x ≥ {num(d)}. Determine, with a reason, whether the composite function gf exists.'
    if exists:
        return Q(stem, f'Yes: the range of f is f(x) ≥ {num(q)}, which lies within the domain x ≥ {num(d)} of g, so gf exists.', f'B1 range of f is f(x) ≥ {num(q)}; B1 contained in domain of g so gf exists')
    return Q(stem, f'No: the range of f is f(x) ≥ {num(q)}, which includes values less than {num(d)} (e.g. f(0) = {num(q)}), and these are not in the domain of g.', f'B1 range of f is f(x) ≥ {num(q)}; B1 not contained in x ≥ {num(d)} so gf does not exist')


@f22.add('C3', (1, 2, 3, 4, 5), 'numerical')
def f22_calc(r, D):
    a, b = nz(r, -4, 5), nz(r, -8, 8)
    c = r.randint(-6, 6)
    fe, ge = lin(a, b), quad(1, 0, c)
    intro = f'The functions f and g are defined for x ∈ ℝ by f(x) = {fe} and g(x) = {ge}.'
    if D == 1:
        t = nz(r, -5, 5)
        return Q(f'{intro} Find gf({num(t)}).', num((a * t + b) ** 2 + c), f'M1 f({num(t)}) = {num(a * t + b)}; A1 gf({num(t)}) = {num((a * t + b) ** 2 + c)}')
    if D == 2:
        return Q(f'{intro} Find expressions for fg(x) and gf(x).', f'fg(x) = {quad(a, 0, a * c + b)}; gf(x) = {quad(a * a, 2 * a * b, b * b + c)}',
                 f'B1 fg(x) = {quad(a, 0, a * c + b)}; M1 ({fe})²{sg(c) if c else ""}; A1 gf(x) = {quad(a * a, 2 * a * b, b * b + c)}')
    if D == 3:
        # solve fg(x) = k : a(x² + c) + b = k -> x² = (k − b)/a − c = s²
        s = r.randint(1, 7)
        k = a * (s * s + c) + b
        return Q(f'{intro} Solve the equation fg(x) = {num(k)}.', f'x = ±{s}', f'B1 fg(x) = {quad(a, 0, a * c + b)}; M1 x² = {s * s}; A1 x = ±{s}')
    if D == 4:
        # solve gf(x) = k with two rational roots: (a x + b)² + c = k, (ax + b) = ±m
        m = r.randint(1, 6)
        k = m * m + c
        xs = sorted({Fr(m - b, a), Fr(-m - b, a)})
        return Q(f'{intro} Solve the equation gf(x) = {num(k)}.', ' or '.join(f'x = {num(x)}' for x in xs),
                 f'M1 gf(x) = ({fe})²{sg(c) if c else ""}; M1 ({fe})² = {m * m}; A1 {fe} = ±{m}; A1 ' + ', '.join(num(x) for x in xs))
    # D5: f(x) = ax + b, h(x) = px + q; find q such that fh = hf
    p = nz(r, 2, 6)
    if a == 1:
        return None
    # fh(x) = a(px + q) + b ; hf(x) = p(ax + b) + q -> aq + b = pb + q -> q(a − 1) = b(p − 1)
    q = Fr(b * (p - 1), a - 1)
    return Q(f'The functions f and h are defined for x ∈ ℝ by f(x) = {fe} and h(x) = {p}x + k, where k is a constant. Given that fh(x) = hf(x) for all x, find the value of k.', f'k = {num(q)}',
             f'M1 fh(x) = {a * p}x + {num(a)}k{sg(b)}; M1 hf(x) = {a * p}x{sg(p * b)} + k; M1 equates constants; A1 k = {num(q)}'.replace(' + −', ' − '))


def f22_c4(r, D):
    a, b = nz(r, 2, 4), nz(r, -6, 6)
    c = r.randint(1, 6)
    fe = lin(a, b)
    intro = f'The functions f and g are defined by f(x) = {fe} for x ∈ ℝ and g(x) = x² + {c} for x ≥ 0.'
    s = r.randint(1, 5)
    k = a * (s * s + c) + b
    m = r.randint(1, 4)
    parts = [
        P('Find an expression for fg(x).', quad(a, 0, a * c + b), f'B1 fg(x) = {quad(a, 0, a * c + b)}'),
        P('Find an expression for gf(x) and state why gf, defined for x ∈ ℝ, does not exist.', f'gf(x) = ({fe})² + {c}; f(x) takes negative values, which are outside the domain x ≥ 0 of g.',
          f'B1 ({fe})² + {c}; B1 range of f (ℝ) not within domain of g'),
        P(f'Solve the equation fg(x) = {num(k)}.', f'x = {s}', f'M1 {a}(x² + {c}){sg(b)} = {num(k)}; A1 x² = {s * s}; A1 x = {s} only (x ≥ 0)'),
        P('State the range of fg.', f'fg(x) ≥ {num(a * c + b)}', f'B1 fg(x) ≥ {num(a * c + b)}'),
        P(f'Find ff(x) and solve ff(x) = {num(a * (a * m + b) + b)}.', f'ff(x) = {lin(a * a, a * b + b)}; x = {m}', f'B1 ff(x) = {lin(a * a, a * b + b)}; B1 x = {m}'),
    ]
    return cmp_(r, intro, parts)


f22.add('C4', (2, 3, 4, 5))(f22_c4)


# ---------------------------------------------------------------- 2.3 inverse functions
f23 = T('Inverse functions and the graphs of f and f⁻¹', 'inverse functions', 'graphs of f and f⁻¹', 'inverse')
f23.fixed('C1', (1, 2), [
    ('The graph of y = f⁻¹(x) is the reflection of the graph of y = f(x) in', 'the line y = x', 'Inverting swaps x and y, which is reflection in y = x.', ['the x-axis', 'the y-axis', 'the line y = −x']),
    ('The domain of f⁻¹ is', 'the range of f', 'f⁻¹ takes the outputs of f as its inputs.', ['the domain of f', 'all real numbers', 'the range of f⁻¹']),
    ('Which condition must a function satisfy to have an inverse?', 'it must be one-one', 'Only a one-one function can be reversed uniquely.', ['it must be many-one', 'its domain must be ℝ', 'it must be linear']),
    ('f(x) = x³ + 1. What is f⁻¹(x)?', '∛(x − 1)', 'y = x³ + 1 ⇒ x = ∛(y − 1).', ['∛x − 1', '1/(x³ + 1)', '(x − 1)³']),
    ('If f(3) = 11 and f is one-one, then f⁻¹(11) =', '3', 'f⁻¹ undoes f.', ['11', '1/11', '1/3']),
])
f23.fixed('C2', (2, 3), [
    ('Explain why f(x) = x² for x ∈ ℝ has no inverse, and state how the domain could be restricted so that an inverse exists.', 'f is many-one (f(2) = f(−2)), so it cannot be reversed. Restricting the domain to x ≥ 0 makes it one-one.', 'B1 many-one with example; B1 suitable restriction e.g. x ≥ 0 [2]'),
    ('Explain why ff⁻¹(x) = x for every x in the domain of f⁻¹.', 'f⁻¹ maps x to the value whose image under f is x, so applying f afterwards returns x.', 'B1 f⁻¹ undoes f; B1 composition gives identity [2]'),
    ('Explain why the solutions of f(x) = f⁻¹(x) for an increasing function f lie on the line y = x.', 'The graphs are reflections of each other in y = x; for an increasing function they can only meet on that mirror line, so solving f(x) = x gives the intersections.', 'B1 reflection in y = x; B1 intersections on y = x for increasing f [2]'),
    ('Explain the difference between f⁻¹(x) and 1/f(x).', 'f⁻¹ is the inverse function, which undoes f; 1/f(x) is the reciprocal of the value of f. For f(x) = 2x, f⁻¹(x) = x/2 but 1/f(x) = 1/(2x).', 'B1 inverse undoes f vs reciprocal; B1 example showing they differ [2]'),
])


@f23.add('C1', (1, 2, 3))
def f23_c1(r, D):
    a, b = nz(r, -6, 7, (0, 1)), nz(r, -9, 9)
    stem = f'The function f is defined by f(x) = {lin(a, b)} for x ∈ ℝ. Find f⁻¹(x).'
    c = inv_lin(a, b)
    ds = [f'(x{sg(b)})/{num(a)}', f'1/({lin(a, b)})', f'{num(a)}x{sg(-b)}', f'x/{num(a)}{sg(-b)}']
    if D == 3:
        t = r.randint(-6, 8)
        val = a * t + b
        return MC(r, f'The function f is defined by f(x) = {lin(a, b)} for x ∈ ℝ. Find the value of f⁻¹({num(val)}).', num(t), [num(a * val + b), num(Fr(val + b, a)), num(-t), num(Fr(1, val) if val else 99)],
                  f'Solve {lin(a, b)} = {num(val)}: x = {num(t)}.')
    return MC(r, stem, c, ds, f'y = {lin(a, b)} ⇒ x = ({xk(b, "y")})/{num(a)}; swap x and y.')


@f23.add('C2', (2, 3, 4), 'explain')
def f23_err(r, D):
    nm = person(r)
    h, k = nz(r, -5, 5), r.randint(-8, 8)
    if r.random() < 0.5:
        stem = f'The function f is defined by f(x) = {cs(1, -h, k)} for x ≥ {num(h)}. {nm} finds f⁻¹(x) = {num(h)} − √({xk(k)}). Explain why this is incorrect and give f⁻¹(x) correctly, stating its domain.'
        return Q(stem, f'The range of f⁻¹ must be the domain of f, x ≥ {num(h)}, so the positive root is needed: f⁻¹(x) = {num(h)} + √({xk(k)}) for x ≥ {num(k)}.'.replace('0 + √', '√'),
                 f'B1 range of f⁻¹ = domain of f, x ≥ {num(h)}, so + root; B1 f⁻¹(x) = {num(h)} + √({xk(k)}), x ≥ {num(k)}'.replace('0 + √', '√'))
    a, b = nz(r, 2, 7), nz(r, -9, 9)
    stem = f'The function f is defined by f(x) = {lin(a, b)} for x ∈ ℝ. {nm} says that f⁻¹(x) = 1/({lin(a, b)}). Explain the error and find f⁻¹(x).'
    return Q(stem, f'{nm} has found the reciprocal 1/f(x), not the inverse. Solving y = {lin(a, b)} for x: f⁻¹(x) = (x{sg(-b)})/{a}.',
             f'B1 reciprocal is not the inverse (e.g. f⁻¹(f(0)) ≠ 0 with this formula); B1 f⁻¹(x) = (x{sg(-b)})/{a}')


@f23.add('C3', (1, 2, 3, 4, 5), 'numerical')
def f23_inv(r, D):
    if D <= 2:
        a, b, c = nz(r, 2, 7), nz(r, -9, 9), nz(r, 2, 5)
        stem = f'The function f is defined by f(x) = ({lin(a, b)})/{c} for x ∈ ℝ. Find an expression for f⁻¹(x).'
        return Q(stem, f'f⁻¹(x) = ({lin(c, -b)})/{a}', f'M1 y = ({lin(a, b)})/{c} ⇒ {c}y{sg(-b)} = {a}x; A1 f⁻¹(x) = ({lin(c, -b)})/{a}')
    if D == 3:
        a, b, c = nz(r, -5, 6), nz(r, -9, 9), nz(r, -6, 6)
        if b == -a * c:
            return None
        # f(x) = (ax + b)/(x − c); inverse (cx + b)/(x − a)
        stem = f'The function f is defined by f(x) = ({lin(a, b)})/({lin(1, -c)}) for x ≠ {num(c)}. Find f⁻¹(x) and state the value of x for which f⁻¹ is not defined.'
        return Q(stem, f'f⁻¹(x) = ({lin(c, b)})/({lin(1, -a)}); not defined at x = {num(a)}',
                 f'M1 y({lin(1, -c)}) = {lin(a, b)}; M1 collects x terms: x(y{sg(-a)}) = {lin(c, b, "y")}; A1 f⁻¹(x) = ({lin(c, b)})/({lin(1, -a)}); B1 x ≠ {num(a)}')
    a = 1 if D == 4 else r.randint(2, 4)
    h, k = nz(r, -5, 5), r.randint(-10, 10)
    f = quad(a, -2 * a * h, a * h * h + k)
    inside = xk(k) if a == 1 else f'({xk(k)})/{a}'
    stem = f'The function f is defined by f(x) = {f} for x ≥ {num(h)}. Find an expression for f⁻¹(x) and state the domain of f⁻¹.'
    ans = f'f⁻¹(x) = {num(h)} + √({inside}) for x ≥ {num(k)}'.replace('= 0 + √', '= √')
    return Q(stem, ans, f'M1 completes the square: {cs(a, -h, k)}; M1 rearranges y = {cs(a, -h, k)} for x; A1 {ans.split(" for")[0]}; B1 domain x ≥ {num(k)}')


@f23.add('C3', (2, 3, 4), 'numerical')
def f23_meet(r, D):
    a, b = r.choice([2, 3, 4, 5, -2, -3]), nz(r, -9, 9)
    # f(x) = f⁻¹(x) ⇔ f(x) = x for linear f: x = b/(1 − a)
    x0 = Fr(b, 1 - a)
    stem = f'The function f is defined by f(x) = {lin(a, b)} for x ∈ ℝ. Find f⁻¹(x) and solve the equation f(x) = f⁻¹(x).'
    return Q(stem, f'f⁻¹(x) = {inv_lin(a, b)}; x = {num(x0)}',
             f'B1 f⁻¹(x) = {inv_lin(a, b)}; M1 {lin(a, b)} = {inv_lin(a, b)} (or f(x) = x); A1 x = {num(x0)}')


def f23_c4(r, D):
    h = r.randint(-3, 3)
    t = h + r.randint(2, 5)
    k = t - (t - h) ** 2
    f = quad(1, -2 * h, h * h + k)
    other = 2 * h + 1 - t
    intro = f'The function f is defined by f(x) = {f} for x ≥ {num(h)}.'
    inv = f'{num(h)} + √({xk(k)})'.replace('0 + √', '√') if h != 0 else f'√({xk(k)})'
    parts = [
        P('Express f(x) in the form (x − a)² + b.', cs(1, -h, k), f'B1 a = {num(h)}; B1 b = {num(k)}'),
        P('State the range of f.', f'f(x) ≥ {num(k)}', f'B1 f(x) ≥ {num(k)}'),
        P('Find an expression for f⁻¹(x) and state its domain.', f'f⁻¹(x) = {inv}, x ≥ {num(k)}', f'M1 makes x the subject; A1 f⁻¹(x) = {inv}; B1 domain x ≥ {num(k)}'),
        P('Solve the equation f(x) = f⁻¹(x).', f'x = {num(t)}', f'M1 sets f(x) = x; A1 {quad(1, -(2 * h + 1), h * h + k)} = 0; A1 x = {num(t)} (x = {num(other)} rejected, not in domain)'),
        P('Describe how the graph of y = f⁻¹(x) is related to the graph of y = f(x).', 'It is the reflection of y = f(x) in the line y = x.', 'B1 reflection in y = x'),
    ]
    return cmp_(r, intro, parts)


f23.add('C4', (2, 3, 4, 5))(f23_c4)


# ---------------------------------------------------------------- 2.4 transformations
f24 = T('Transformations of graphs: translation, reflection and stretch', 'transformations of graphs', 'translation, reflection and stretch')
f24.fixed('C1', (1, 2), [
    ('Which transformation maps y = f(x) onto y = −f(x)?', 'reflection in the x-axis', 'Every y-coordinate changes sign.', ['reflection in the y-axis', 'reflection in y = x', 'translation by (0, −1)']),
    ('Which transformation maps y = f(x) onto y = f(−x)?', 'reflection in the y-axis', 'Every x-coordinate changes sign.', ['reflection in the x-axis', 'rotation by 180°', 'stretch with factor −1 parallel to the y-axis']),
    ('The point (4, 6) lies on y = f(x). Which point lies on y = f(2x)?', '(2, 6)', 'f(2x) is a stretch parallel to the x-axis with factor 1/2.', ['(8, 6)', '(4, 12)', '(4, 3)']),
    ('The point (4, 6) lies on y = f(x). Which point lies on y = 3f(x)?', '(4, 18)', 'Stretch parallel to the y-axis, factor 3.', ['(12, 6)', '(4, 9)', '(4/3, 6)']),
    ('y = f(x) is translated by the vector (0, −5). The new equation is', 'y = f(x) − 5', 'A translation parallel to the y-axis adds to the output.', ['y = f(x − 5)', 'y = f(x + 5)', 'y = −5f(x)']),
])
f24.fixed('C2', (2, 3), [
    ('Explain why y = f(x − 3) is a translation of y = f(x) by 3 units in the positive x-direction, not the negative direction.', 'The new graph takes at x the value f had at x − 3, i.e. 3 units earlier, so every point moves 3 units to the right.', 'B1 value at x equals old value at x − 3; B1 shift right by 3 [2]'),
    ('Explain why the order of the transformations matters when y = f(x) is transformed to y = 2f(x) + 3.', 'Stretching by 2 then translating by 3 gives 2f(x) + 3; translating first then stretching gives 2(f(x) + 3) = 2f(x) + 6, a different curve.', 'B1 stretch then translate; B1 other order gives 2f(x) + 6 [2]'),
    ('Describe the effect of the transformation y = f(x) → y = f(x/2) on the point (3, 5).', 'It is a stretch parallel to the x-axis with scale factor 2, so (3, 5) moves to (6, 5).', 'B1 stretch factor 2 in x-direction; B1 (6, 5) [2]'),
])

TRANS = [
    ('f(x){s}', 'translation by the vector (0, {a})'),
    ('f(x{s})', 'translation by the vector ({na}, 0)'),
    ('{a}f(x)', 'stretch parallel to the y-axis with scale factor {a}'),
    ('f({a}x)', 'stretch parallel to the x-axis with scale factor 1/{a}'),
]


def trans_desc(kind, a):
    if kind == 0:
        return f'y = f(x){sg(a)}', f'translation by the vector (0, {num(a)})'
    if kind == 1:
        return f'y = f(x{sg(a)})', f'translation by the vector ({num(-a)}, 0)'
    if kind == 2:
        return f'y = {num(a)}f(x)', f'stretch parallel to the y-axis with scale factor {num(a)}'
    if kind == 3:
        return f'y = f({num(a)}x)', f'stretch parallel to the x-axis with scale factor {num(Fr(1, a))}'
    if kind == 4:
        return 'y = −f(x)', 'reflection in the x-axis'
    return 'y = f(−x)', 'reflection in the y-axis'


def trans_pt(kind, a, p):
    x, y = p
    return [(x, y + a), (x - a, y), (x, a * y), (Fr(x, a), y), (x, -y), (-x, y)][kind]


@f24.add('C1', (1, 2, 3))
def f24_c1(r, D):
    kind = r.randint(0, 3)
    a = nz(r, -6, 6) if kind < 2 else r.randint(2, 5)
    eq, desc = trans_desc(kind, a)
    if D < 3:
        others = [trans_desc(k, a)[1] for k in range(4) if k != kind] + [trans_desc(kind, -a if kind < 2 else a)[1] if kind < 2 else trans_desc(3 if kind == 2 else 2, a)[1]]
        if kind == 1:
            others.append(f'translation by the vector ({num(a)}, 0)')
        if kind == 3:
            others.append(f'stretch parallel to the x-axis with scale factor {num(a)}')
        return MC(r, f'Describe the single transformation that maps the graph of y = f(x) onto the graph of {eq}.', desc, others[::-1], f'{eq}: {desc}.')
    p = (nz(r, -6, 6), nz(r, -6, 6))
    img = trans_pt(kind, a, p)
    wrong = [trans_pt(k, a, p) for k in range(4) if k != kind] + [(p[0] + a, p[1])]
    return MC(r, f'The point {pt(*p)} lies on the curve y = f(x). Find the corresponding point on the curve {eq}.', pt(*img), [pt(*w) for w in wrong], f'{desc}: {pt(*p)} → {pt(*img)}.')


@f24.add('C2', (2, 3, 4), 'explain')
def f24_err(r, D):
    nm = person(r)
    fr = r.choice(['dir', 'stretch', 'order'])
    a = r.randint(2, 7)
    if fr == 'dir':
        sgn_ = r.choice([1, -1])
        eq = f'y = f(x{sg(sgn_ * a)})'
        return Q(f'{nm} says that {eq} is the graph of y = f(x) translated {a} units to the {"right" if sgn_ > 0 else "left"}. Explain why {nm} is wrong and describe the transformation correctly.',
                 f'f(x{sg(sgn_ * a)}) takes at x the value f had at x{sg(sgn_ * a)}, so points move {a} units to the {"left" if sgn_ > 0 else "right"}: translation by vector ({num(-sgn_ * a)}, 0).',
                 f'B1 explains direction (e.g. point (x, y) moves to (x{sg(-sgn_ * a)}, y)); B1 translation ({num(-sgn_ * a)}, 0)')
    if fr == 'stretch':
        return Q(f'{nm} says that y = f({a}x) is a stretch of y = f(x) parallel to the x-axis with scale factor {a}. Explain the error and give the correct scale factor.',
                 f'At x the new curve takes the value f had at {a}x, so x-coordinates are divided by {a}: the scale factor is 1/{a}.',
                 f'B1 x-coordinates divided by {a} (e.g. ({a}, f({a})) → (1, f({a}))); B1 scale factor 1/{a}')
    b = nz(r, -6, 6)
    return Q(f'{nm} transforms y = f(x) by first translating by (0, {num(b)}) and then stretching parallel to the y-axis with scale factor {a}. {nm} writes the result as y = {a}f(x){sg(b)}. Explain the error and state the correct equation.',
             f'The stretch acts on the whole translated function: {a}(f(x){sg(b)}) = {a}f(x){sg(a * b)}. {nm}\'s equation corresponds to stretching first.',
             f'B1 stretch multiplies the constant too / order matters; B1 y = {a}f(x){sg(a * b)}')


@f24.add('C3', (1, 2, 3, 4, 5), 'numerical')
def f24_eq(r, D):
    b, c = r.randint(-6, 6), r.randint(-8, 8)
    fe = quad(1, b, c)
    f = lambda x: x * x + b * x + c
    if D <= 2:
        p = nz(r, -5, 5)
        q = nz(r, -6, 6)
        # y = f(x − p) + q
        A, B, C = 1, b - 2 * p, p * p - b * p + c + q
        return Q(f'The curve y = {fe} is translated by the vector ({num(p)}, {num(q)}). Find the equation of the new curve in the form y = ax² + bx + c.', f'y = {quad(A, B, C)}',
                 f'M1 replaces x by (x{sg(-p)}) and adds {num(q)}; A1 y = {quad(A, B, C)}')
    if D == 3:
        k = r.randint(2, 4)
        # reflect in x-axis then stretch y by k: y = −k f(x)
        return Q(f'The curve y = {fe} is reflected in the x-axis and then stretched parallel to the y-axis with scale factor {k}. Find the equation of the resulting curve.', f'y = {quad(-k, -k * b, -k * c)}',
                 f'B1 reflection gives y = −({fe}); M1 multiplies by {k}; A1 y = {quad(-k, -k * b, -k * c)}')
    if D == 4:
        x0, y0 = nz(r, -5, 5), nz(r, -6, 6)
        k, p, q = r.randint(2, 4), nz(r, -4, 4), nz(r, -5, 5)
        # y = k f(x − p) + q
        return Q(f'The point A{pt(x0, y0)} lies on the curve y = f(x). The curve is transformed to y = {k}f(x{sg(-p)}){sg(q)}. Find the coordinates of the image of A and describe the two transformations in order.',
                 f'{pt(x0 + p, k * y0 + q)}; stretch parallel to the y-axis, factor {k}, then translation ({num(p)}, {num(q)}) (or translation ({num(p)}, 0), stretch, translation (0, {num(q)}))',
                 f'B1 x-coordinate {num(x0 + p)}; B1 y-coordinate {num(k * y0 + q)}; B1 stretch factor {k} parallel to y-axis; B1 translation ({num(p)}, {num(q)}) after the stretch')
    h, k_, a = nz(r, -5, 5), nz(r, -9, 9), r.randint(2, 5)
    return Q(f'Describe fully a sequence of two transformations that maps the curve y = x² onto the curve y = {quad(a, -2 * a * h, a * h * h + k_)}.',
             f'Stretch parallel to the y-axis with scale factor {a}, followed by a translation by the vector ({num(h)}, {num(k_)}).',
             f'M1 completes the square: {cs(a, -h, k_)}; B1 stretch, y-direction, factor {a}; B1 translation; B1 vector ({num(h)}, {num(k_)}); B1 correct order')


def f24_c4(r, D):
    h, k = nz(r, -4, 4), nz(r, -8, 8)
    fe = quad(1, -2 * h, h * h + k)
    p, q = nz(r, -4, 4), nz(r, -5, 5)
    intro = f'The function f is defined by f(x) = {fe} for x ∈ ℝ.'
    g = quad(1, -2 * (h + p), (h + p) ** 2 + k + q)
    parts = [
        P('Express f(x) in the form (x − a)² + b and hence state the coordinates of the vertex of y = f(x).', f'{cs(1, -h, k)}; vertex {pt(h, k)}', f'B1 a = {num(h)}; B1 b = {num(k)}; B1 vertex {pt(h, k)}'),
        P(f'The graph of y = f(x) is translated by the vector ({num(p)}, {num(q)}) to give y = g(x). Find g(x) in the form x² + bx + c.', g, f'M1 g(x) = f(x{sg(-p)}){sg(q)}; A1 g(x) = {g}'),
        P(f'State the coordinates of the vertex of y = g(x).', pt(h + p, k + q), f'B1 FT {pt(h + p, k + q)}'),
        P('The graph of y = f(x) is reflected in the y-axis. Write down the equation of the new graph.', f'y = {quad(1, 2 * h, h * h + k)}', f'B1 y = f(−x) = {quad(1, 2 * h, h * h + k)}'),
        P('The graph of y = f(x) is stretched parallel to the y-axis with scale factor 3. Write down the coordinates of the new vertex.', pt(h, 3 * k), f'B1 {pt(h, 3 * k)}'),
    ]
    return cmp_(r, intro, parts)


f24.add('C4', (2, 3, 4, 5))(f24_c4)

CHAPTERS[2] = [f21, f22, f23, f24]


# ================================================================ Chapter 3 Coordinate geometry

def rand_pts(r, n=2, lo=-8, hi=9):
    while True:
        ps = [(r.randint(lo, hi), r.randint(lo, hi)) for _ in range(n)]
        if len(set(ps)) == n and len({p[0] for p in ps}) == n and len({p[1] for p in ps}) == n:
            return ps


def grad(A, B):
    return Fr(B[1] - A[1], B[0] - A[0])


def mid(A, B):
    return (Fr(A[0] + B[0], 2), Fr(A[1] + B[1], 2))


def d2(A, B):
    v = Fr((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2)
    return int(v) if v.denominator == 1 else v


def line_through(P, m):
    """Equation ax + by + c = 0 of the line through P with gradient m."""
    return gen_line(m, -1, P[1] - m * P[0])


def slope_form(m, P):
    return line_eq(m, P[1] - m * P[0])


g31 = T('Length, gradient and midpoint of a line segment and equations of straight lines', 'length, gradient and midpoint', 'equations of straight lines', 'line segment')
g31.fixed('C1', (1, 2), [
    ('What is the gradient of the line 2x + 3y = 12?', '−2/3', 'Rearrange: y = −(2/3)x + 4.', ['2/3', '−3/2', '2']),
    ('Where does the line 3x − 4y = 24 cross the y-axis?', '(0, −6)', 'Put x = 0: −4y = 24, y = −6.', ['(0, 6)', '(8, 0)', '(0, −8)']),
    ('The equation of the line through (2, 5) with gradient 3 is', 'y = 3x − 1', 'y − 5 = 3(x − 2) ⇒ y = 3x − 1.', ['y = 3x + 5', 'y = 3x + 1', 'y = 2x + 5']),
    ('Which formula gives the distance between (x₁, y₁) and (x₂, y₂)?', '√((x₂ − x₁)² + (y₂ − y₁)²)', 'Pythagoras on the horizontal and vertical differences.', ['(x₂ − x₁) + (y₂ − y₁)', '√((x₂ + x₁)² + (y₂ + y₁)²)', '((x₂ − x₁)² + (y₂ − y₁)²)/2']),
    ('A line has gradient 0. It is', 'parallel to the x-axis', 'Zero gradient means y is constant: a horizontal line.', ['parallel to the y-axis', 'the line y = x', 'undefined']),
])
g31.fixed('C2', (2, 3), [
    ('Explain how to show that three points A, B and C are collinear.', 'Show that the gradients of AB and BC are equal; since the lines share the point B, they are the same line.', 'B1 equal gradients AB and BC; B1 common point B [2]'),
    ('Explain why the gradient of a vertical line is undefined.', 'Between any two points on it the change in x is zero, and dividing the change in y by zero is undefined.', 'B1 Δx = 0; B1 division by zero [2]'),
    ('Explain why y − y₁ = m(x − x₁) is the equation of the line through (x₁, y₁) with gradient m.', 'For any other point (x, y) on the line, the gradient (y − y₁)/(x − x₁) must equal m; rearranging gives the equation, and (x₁, y₁) satisfies it.', 'B1 gradient between (x, y) and (x₁, y₁) equals m; B1 rearrangement [2]'),
])


@g31.add('C1', (1, 2, 3))
def g31_c1(r, D):
    A, B = rand_pts(r)
    kind = r.choice(['mid', 'grad']) if D < 3 else 'len'
    if kind == 'mid':
        M = mid(A, B)
        return MC(r, f'Find the midpoint of the line segment joining A{pt(*A)} and B{pt(*B)}.', pt(*M), [pt(Fr(B[0] - A[0], 2), Fr(B[1] - A[1], 2)), pt(A[0] + B[0], A[1] + B[1]), pt(M[1], M[0]), pt(-M[0], M[1])],
                  f'Midpoint = ((x₁ + x₂)/2, (y₁ + y₂)/2) = {pt(*M)}.')
    if kind == 'grad':
        g = grad(A, B)
        return MC(r, f'Find the gradient of the line through A{pt(*A)} and B{pt(*B)}.', num(g), [num(1 / g), num(-g), num(-1 / g), num(Fr(B[1] + A[1], B[0] + A[0]) if A[0] + B[0] else g + 1)],
                  f'Gradient = ({num(B[1])} − {num(A[1])})/({num(B[0])} − {num(A[0])}) = {num(g)}.'.replace('− −', '+ '))
    L = d2(A, B)
    return MC(r, f'Find the exact distance between A{pt(*A)} and B{pt(*B)}.', rt(L), [rt(abs(B[0] - A[0]) + abs(B[1] - A[1])) if abs(B[0] - A[0]) + abs(B[1] - A[1]) != L else rt(L + 1), str(L), rt((A[0] + B[0]) ** 2 + (A[1] + B[1]) ** 2) if (A[0] + B[0]) ** 2 + (A[1] + B[1]) ** 2 else '1', rt(L + 4)],
              f'AB² = ({num(B[0] - A[0])})² + ({num(B[1] - A[1])})² = {L}, AB = {rt(L)}.')


@g31.add('C2', (2, 3, 4), 'explain')
def g31_err(r, D):
    nm = person(r)
    fr = r.choice(['flip', 'collinear', 'midsign'])
    A, B = rand_pts(r)
    g = grad(A, B)
    if fr == 'flip' and abs(g) != 1:
        return Q(f'{nm} calculates the gradient of the line through {pt(*A)} and {pt(*B)} as ({num(B[0])} − {num(A[0])})/({num(B[1])} − {num(A[1])}) = {num(1 / g)}. Explain the error and find the correct gradient.'.replace('− −', '+ '),
                 f'Gradient is change in y over change in x; {nm} inverted it. Correct gradient {num(g)}.', f'B1 gradient = Δy/Δx; B1 {num(g)}')
    if fr == 'collinear' or abs(g) == 1:
        t = r.choice([2, 3, -1, -2])
        C = (A[0] + t * (B[0] - A[0]), A[1] + t * (B[1] - A[1]))
        return Q(f'Show that the points A{pt(*A)}, B{pt(*B)} and C{pt(*C)} are collinear.',
                 f'Gradient AB = {num(g)} and gradient AC = {num(grad(A, C))}; equal gradients through the common point A, so collinear.',
                 f'M1 finds two gradients (AB and AC, or AB and BC); A1 both {num(g)} with conclusion (common point)')
    M = mid(A, B)
    return Q(f'{nm} says the midpoint of A{pt(*A)} and B{pt(*B)} is {pt(Fr(B[0] - A[0], 2), Fr(B[1] - A[1], 2))}. Explain the error and find the correct midpoint.',
             f'{nm} halved the differences instead of averaging the coordinates; midpoint = {pt(*M)}.', f'B1 must add the coordinates and halve; B1 {pt(*M)}')


@g31.add('C3', (1, 2, 3, 4, 5), 'numerical')
def g31_line(r, D):
    A, B = rand_pts(r)
    g = grad(A, B)
    if D <= 2:
        return Q(f'Find the equation of the line through A{pt(*A)} and B{pt(*B)}, giving your answer in the form y = mx + c.', slope_form(g, A),
                 f'M1 gradient {num(g)}; A1 {slope_form(g, A)}')
    if D == 3:
        return Q(f'The points A{pt(*A)} and B{pt(*B)} are given. Find the equation of the line AB in the form ax + by + c = 0, where a, b and c are integers, and the exact length of AB.',
                 f'{line_through(A, g)}; AB = {rt(d2(A, B))}', f'M1 gradient {num(g)}; A1 {line_through(A, g)}; M1 distance formula; A1 {rt(d2(A, B))}')
    if D == 4:
        # find k with distance: A(x1, y1), B(k, y2), AB = √L  -> two values
        dx, dy = r.randint(1, 8), nz(r, -8, 8)
        x1, y1 = r.randint(-6, 6), r.randint(-6, 6)
        L = dx * dx + dy * dy
        ks = sorted((x1 - dx, x1 + dx))
        return Q(f'The point A has coordinates {pt(x1, y1)} and the point B has coordinates (k, {num(y1 + dy)}). Given that AB = {rt(L)}, find the possible values of k.',
                 f'k = {num(ks[0])} or k = {num(ks[1])}', f'M1 (k{sg(-x1)})² + {dy * dy} = {L}; A1 (k{sg(-x1)})² = {dx * dx}; A1 k = {num(ks[0])}, {num(ks[1])}'.replace('(k + 0)', 'k').replace('(k − 0)', 'k'))
    # D5: line meets axes, area of triangle with axes
    m = Fr(nz(r, -5, 5), r.choice([1, 2, 3]))
    c = nz(r, -9, 9)
    xint = -Fr(c) / m
    area = abs(Fr(c) * xint) / 2
    return Q(f'The line l passes through the point {pt(1, m + c)} and has gradient {num(m)}. The line meets the x-axis at P and the y-axis at Q. Find the area of triangle OPQ, where O is the origin.',
             num(area), f'M1 equation {line_eq(m, c)}; A1 Q(0, {num(c)}); A1 P({num(xint)}, 0); M1 ½ × |{num(xint)}| × |{num(c)}|; A1 {num(area)}')


def g31_c4(r, D):
    # right-angled triangle at B
    for _ in range(50):
        B = (r.randint(-4, 4), r.randint(-4, 4))
        u = (nz(r, -4, 4), nz(r, -4, 4))
        s, t = r.choice([1, 2]), r.choice([1, 2, 3])
        A = (B[0] + s * u[0], B[1] + s * u[1])
        C = (B[0] - t * u[1], B[1] + t * u[0])
        if A[0] != B[0] and C[0] != B[0] and A[0] != C[0]:
            break
    else:
        return None
    area = Fr(math.isqrt(d2(A, B) * d2(B, C)), 2) if math.isqrt(d2(A, B) * d2(B, C)) ** 2 == d2(A, B) * d2(B, C) else None
    intro = f'The points A{pt(*A)}, B{pt(*B)} and C{pt(*C)} are the vertices of a triangle.'
    parts = [
        P('Find the gradients of AB and BC and hence show that angle ABC = 90°.', f'm(AB) = {num(grad(A, B))}, m(BC) = {num(grad(B, C))}; product −1', f'B1 m(AB) = {num(grad(A, B))}; B1 m(BC) = {num(grad(B, C))}; B1 product = −1 so perpendicular'),
        P('Find the exact length of AC.', rt(d2(A, C)), f'M1 distance formula; A1 {rt(d2(A, C))}'),
        P('Find the coordinates of the midpoint M of AC.', pt(*mid(A, C)), f'B1 {pt(*mid(A, C))}'),
        P('Find the equation of the line AC in the form ax + by + c = 0.', line_through(A, grad(A, C)), f'M1 gradient {num(grad(A, C))}; A1 {line_through(A, grad(A, C))}'),
    ]
    if area is not None:
        parts.append(P('Find the area of triangle ABC.', num(area), f'M1 ½ × AB × BC; A1 {num(area)}'))
    return cmp_(r, intro, parts)


g31.add('C4', (2, 3, 4, 5))(g31_c4)


# ---------------------------------------------------------------- 3.2 parallel / perpendicular
g32 = T('Parallel and perpendicular lines and the perpendicular bisector', 'parallel and perpendicular lines', 'perpendicular bisector')
g32.fixed('C1', (1, 2), [
    ('Two lines with gradients m₁ and m₂ are perpendicular when', 'm₁m₂ = −1', 'Perpendicular gradients are negative reciprocals.', ['m₁ = m₂', 'm₁ + m₂ = 0', 'm₁m₂ = 1']),
    ('What is the gradient of a line perpendicular to y = 4x − 7?', '−1/4', 'Negative reciprocal of 4.', ['−4', '1/4', '4']),
    ('Which line is parallel to y = −2x + 5?', '4x + 2y = 3', '4x + 2y = 3 gives y = −2x + 3/2: same gradient −2.', ['y = 2x + 5', 'y = (1/2)x − 1', 'x − 2y = 5']),
    ('The perpendicular bisector of AB passes through', 'the midpoint of AB', 'It bisects AB, so it passes through the midpoint, at right angles to AB.', ['A', 'B', 'the origin']),
    ('A line is perpendicular to the line x = 3. It is', 'parallel to the x-axis', 'x = 3 is vertical, so a perpendicular line is horizontal.', ['parallel to the y-axis', 'the line y = 3', 'the line y = x']),
])
g32.fixed('C2', (2, 3), [
    ('Explain why every point on the perpendicular bisector of AB is the same distance from A as from B.', 'For a point P on it, the triangles PMA and PMB (M the midpoint) are congruent: PM common, MA = MB, right angles at M. So PA = PB.', 'B1 congruent triangles / Pythagoras with MA = MB; B1 PA = PB [2]'),
    ('Explain how to find the equation of the perpendicular bisector of the segment joining two given points.', 'Find the midpoint, find the gradient of the segment, take the negative reciprocal, and use y − y₁ = m(x − x₁) through the midpoint.', 'B1 midpoint and negative reciprocal gradient; B1 line equation through midpoint [2]'),
    ('Explain why the lines 3x − 2y = 5 and 6x − 4y = 1 never meet.', 'Both have gradient 3/2 but different y-intercepts (−5/2 and −1/4), so they are distinct parallel lines.', 'B1 equal gradients; B1 different intercepts so parallel and distinct [2]'),
])


@g32.add('C1', (1, 2, 3))
def g32_c1(r, D):
    a, b, c = r.randint(1, 7), nz(r, -7, 7), r.randint(-12, 12)
    m = Fr(-a, b)
    kind = r.choice(['perp', 'par'])
    eq = f'{lin(a, 0)}{term(b, 1, "y")} = {num(c)}'
    if kind == 'perp':
        return MC(r, f'Find the gradient of a line perpendicular to {eq}.', num(-1 / m), [num(m), num(1 / m), num(-m), num(Fr(b, 1) if b != -1 / m else Fr(a))],
                  f'Gradient of {eq} is {num(m)}; perpendicular gradient is {num(-1 / m)}.')
    return MC(r, f'Find the gradient of a line parallel to {eq}.', num(m), [num(-1 / m), num(1 / m), num(-m), num(Fr(a, b) if Fr(a, b) != m else 2 * m)],
              f'y = {num(m)}x + …, so the gradient is {num(m)}.')


@g32.add('C2', (2, 3, 4), 'explain')
def g32_err(r, D):
    nm = person(r)
    m = Fr(nz(r, -6, 6), r.choice([1, 2, 3, 5]))
    if abs(m) == 1:
        m = m * 2
    fr = r.choice(['neg', 'recip', 'check'])
    if fr == 'neg':
        return Q(f'{nm} says a line perpendicular to a line of gradient {num(m)} has gradient {num(-m)}. Explain the error and give the correct gradient.',
                 f'Perpendicular gradients satisfy m₁m₂ = −1; {num(m)} × {num(-m)} = {num(-m * m)} ≠ −1. Correct gradient {num(-1 / m)}.', f'B1 m₁m₂ = −1 (check fails); B1 {num(-1 / m)}')
    if fr == 'recip':
        return Q(f'{nm} says a line perpendicular to a line of gradient {num(m)} has gradient {num(1 / m)}. Explain the error and give the correct gradient.',
                 f'The reciprocal must also change sign: {num(m)} × {num(1 / m)} = 1, not −1. Correct gradient {num(-1 / m)}.', f'B1 negative reciprocal needed; B1 {num(-1 / m)}')
    M = (r.randint(-5, 5), r.randint(-5, 5))
    w = (nz(r, -4, 4), nz(r, -4, 4))
    A, B = (M[0] - w[0], M[1] - w[1]), (M[0] + w[0], M[1] + w[1])
    sc = r.choice([1, 2, -1, -2])
    C = (M[0] + sc * w[1], M[1] - sc * w[0])
    g = grad(A, B)
    return Q(f'The points A{pt(*A)} and B{pt(*B)} are given. Show that the point C{pt(*C)} lies on the perpendicular bisector of AB.',
             f'Midpoint M = {pt(*M)}; gradient AB = {num(g)}; gradient MC = {num(grad(M, C))}; product −1, so C lies on the perpendicular bisector (equivalently CA = CB).',
             f'M1 midpoint and gradients (or CA² and CB²); A1 product −1 (or CA² = CB² = {num(d2(C, A))}) with conclusion')


@g32.add('C3', (1, 2, 3, 4, 5), 'numerical')
def g32_calc(r, D):
    if D <= 2:
        a, b, c = nz(r, -6, 6), nz(r, -6, 6), r.randint(-10, 10)
        m = Fr(-a, b)
        P_ = (r.randint(-6, 6), r.randint(-6, 6))
        kind = r.choice(['parallel', 'perpendicular'])
        g = m if kind == 'parallel' else -1 / m
        eq = f'{lin(a, 0)}{term(b, 1, "y")} = {num(c)}'
        return Q(f'Find the equation of the line through {pt(*P_)} that is {kind} to the line {eq}. Give your answer in the form ax + by + c = 0.', line_through(P_, g),
                 f'B1 gradient {num(g)}; M1 line through {pt(*P_)}; A1 {line_through(P_, g)}')
    A, B = rand_pts(r)
    M = mid(A, B)
    g = grad(A, B)
    pb = line_through(M, -1 / g)
    if D == 3:
        return Q(f'Find the equation of the perpendicular bisector of the line joining A{pt(*A)} and B{pt(*B)}, giving your answer in the form ax + by + c = 0.', pb,
                 f'B1 midpoint {pt(*M)}; B1 gradient AB = {num(g)}; M1 perpendicular gradient {num(-1 / g)} through midpoint; A1 {pb}')
    if D == 4:
        # perpendicular bisector meets x-axis
        m2 = -1 / g
        if m2 == 0:
            return None
        X = M[0] - M[1] / m2
        return Q(f'The perpendicular bisector of the line joining A{pt(*A)} and B{pt(*B)} meets the x-axis at the point P. Find the coordinates of P.', pt(X, 0),
                 f'B1 midpoint {pt(*M)}; B1 perpendicular gradient {num(m2)}; M1 equation and y = 0; A1 {pt(X, 0)}')
    # D5 foot of perpendicular from point to line
    Pp = (r.randint(-6, 6), r.randint(-6, 6))
    m = Fr(nz(r, -4, 4), r.choice([1, 2]))
    c = r.randint(-8, 8)
    # line y = m x + c ; foot: solve
    m2 = -1 / m
    c2 = Pp[1] - m2 * Pp[0]
    X = (c2 - c) / (m - m2)
    Y = m * X + c
    return Q(f'Find the coordinates of the foot of the perpendicular from the point P{pt(*Pp)} to the line {line_eq(m, c)}, and hence find the exact shortest distance from P to the line.',
             f'{pt(X, Y)}; distance = √({num(d2(Pp, (X, Y)))})', f'B1 perpendicular gradient {num(m2)}; M1 equation through P: {line_eq(m2, c2)}; M1 solves simultaneously; A1 {pt(X, Y)}; A1 √({num(d2(Pp, (X, Y)))})')


def g32_c4(r, D):
    # kite / rhombus: A, C symmetric about perpendicular bisector of BD
    for _ in range(40):
        B, Dd = rand_pts(r, 2, -6, 7)
        if (B[0] - Dd[0]) % 2 == 0 and (B[1] - Dd[1]) % 2 == 0:
            break
    M = mid(B, Dd)
    if M[0].denominator != 1 or M[1].denominator != 1:
        return None
    g = grad(B, Dd)
    v = (Dd[1] - B[1], B[0] - Dd[0])
    k = r.choice([1, Fr(1, 2)])
    if (v[0] * k).denominator != 1 or (v[1] * k).denominator != 1:
        k = 1
    A = (M[0] + k * v[0], M[1] + k * v[1])
    intro = f'The points B{pt(*B)} and D{pt(*Dd)} are opposite vertices of a rhombus ABCD. The vertex A lies on the perpendicular bisector of BD.'
    C = (2 * M[0] - A[0], 2 * M[1] - A[1])
    pb = line_through(M, -1 / g)
    parts = [
        P('Find the equation of the perpendicular bisector of BD.', pb, f'B1 midpoint {pt(*M)}; B1 gradient {num(-1 / g)}; A1 {pb}'),
        P(f'Given that A has x-coordinate {num(A[0])}, find the y-coordinate of A.', num(A[1]), f'M1 substitutes into perpendicular bisector; A1 {num(A[1])}'),
        P(f'Given that A is {pt(*A)}, find the coordinates of C.', pt(*C), f'M1 uses midpoint of AC = midpoint of BD; A1 {pt(*C)}'),
        P(f'Given that A is {pt(*A)}, find the area of the rhombus.', num(Fr(math.isqrt(d2(A, C) * d2(B, Dd)), 2)) if math.isqrt(d2(A, C) * d2(B, Dd)) ** 2 == d2(A, C) * d2(B, Dd) else n3(math.sqrt(d2(A, C) * d2(B, Dd)) / 2),
          f'M1 ½ × AC × BD = ½ × {rt(d2(A, C))} × {rt(d2(B, Dd))}; A1 answer'),
    ]
    return cmp_(r, intro, parts)


g32.add('C4', (2, 3, 4, 5))(g32_c4)


# ---------------------------------------------------------------- 3.3 circles
g33 = T('Equation of a circle (x − a)² + (y − b)² = r² and tangents to circles', 'equation of a circle', 'tangents to circles', 'circle')
g33.fixed('C1', (1, 2), [
    ('What are the centre and radius of the circle (x − 2)² + (y + 5)² = 36?', 'centre (2, −5), radius 6', 'Compare with (x − a)² + (y − b)² = r².', ['centre (−2, 5), radius 6', 'centre (2, −5), radius 36', 'centre (2, 5), radius 6']),
    ('The tangent to a circle at a point P is', 'perpendicular to the radius at P', 'A tangent is at right angles to the radius at the point of contact.', ['parallel to the radius at P', 'through the centre', 'perpendicular to the x-axis']),
    ('What is the radius of the circle x² + y² − 6x + 8y = 0?', '5', '(x − 3)² + (y + 4)² = 9 + 16 = 25.', ['25', '10', '√10']),
    ('The angle in a semicircle is', '90°', 'The angle subtended by a diameter at the circumference is a right angle.', ['180°', '45°', '60°']),
    ('A circle has centre (0, 0) and passes through (3, 4). Its equation is', 'x² + y² = 25', 'r² = 3² + 4² = 25.', ['x² + y² = 5', 'x² + y² = 7', '(x − 3)² + (y − 4)² = 25']),
])
g33.fixed('C2', (2, 3), [
    ('Explain how to decide whether a point lies inside, on or outside a circle with centre C and radius r.', 'Find the distance d from the point to C: d < r inside, d = r on, d > r outside.', 'B1 compare distance to centre with radius; B1 all three cases [2]'),
    ('Explain why the perpendicular from the centre of a circle to a chord bisects the chord.', 'The centre is equidistant from the chord ends, so it lies on the perpendicular bisector of the chord; the perpendicular from the centre is that line, so it bisects the chord.', 'B1 centre equidistant from endpoints; B1 perpendicular bisector [2]'),
    ('Explain why x² + y² + 4x − 6y + 20 = 0 does not represent a circle.', 'Completing the square: (x + 2)² + (y − 3)² = 4 + 9 − 20 = −7, and r² cannot be negative.', 'B1 completes the square; B1 r² = −7 < 0 [2]'),
])

PY = {5: [(1, 2)], 10: [(1, 3)], 13: [(2, 3)], 17: [(1, 4)], 20: [(2, 4)], 25: [(3, 4), (0, 5)], 26: [(1, 5)], 29: [(2, 5)], 34: [(3, 5)], 41: [(4, 5)], 45: [(3, 6)], 50: [(1, 7), (5, 5)], 52: [(4, 6)], 58: [(3, 7)], 65: [(1, 8), (4, 7)], 85: [(2, 9), (6, 7)], 100: [(6, 8), (0, 10)]}


def circ_pt(r, R2):
    a, b = r.choice(PY[R2])
    if r.random() < 0.5:
        a, b = b, a
    return (a * r.choice([1, -1]), b * r.choice([1, -1]))


def circ_eq(a, b, R2):
    return f'{sq(-a)} + {sq(-b, "y")} = {R2}'


def circ_exp(a, b, R2):
    return poly([(1, 2), (-2 * a, 1)]) + term(1, 2, 'y') + term(-2 * b, 1, 'y') if b else poly([(1, 2), (-2 * a, 1)]) + term(1, 2, 'y')


@g33.add('C1', (1, 2, 3))
def g33_c1(r, D):
    a, b = nz(r, -8, 8), nz(r, -8, 8)
    R2 = r.choice(list(PY))
    if D < 3:
        rr = rt(R2)
        return MC(r, f'State the centre and radius of the circle {circ_eq(a, b, R2)}.', f'centre {pt(a, b)}, radius {rr}',
                  [f'centre {pt(-a, -b)}, radius {rr}', f'centre {pt(a, b)}, radius {R2}', f'centre {pt(b, a)}, radius {rr}', f'centre {pt(-a, b)}, radius {rr}'], f'(x − a)² + (y − b)² = r²: centre {pt(a, b)}, r = {rr}.')
    c = a * a + b * b - R2
    eqn = circ_exp(a, b, 0) + (sg(c) if c else '') + ' = 0'
    return MC(r, f'Find the centre and radius of the circle {eqn}.', f'centre {pt(a, b)}, radius {rt(R2)}',
              [f'centre {pt(-a, -b)}, radius {rt(R2)}', f'centre {pt(2 * a, 2 * b)}, radius {rt(R2)}', f'centre {pt(a, b)}, radius {rt(abs(c)) if c else "1"}', f'centre {pt(a, b)}, radius {R2}'],
              f'Complete the square: {circ_eq(a, b, R2)}.')


@g33.add('C2', (2, 3, 4), 'explain')
def g33_err(r, D):
    nm = person(r)
    a, b = nz(r, -7, 7), nz(r, -7, 7)
    R2 = r.choice(list(PY))
    fr = r.choice(['sign', 'r2', 'pos'])
    if fr == 'sign':
        return Q(f'{nm} says the circle {circ_eq(a, b, R2)} has centre {pt(-a, -b)}. Explain the error and state the correct centre and radius.',
                 f'The form is (x − a)² + (y − b)² = r², so the signs change: centre {pt(a, b)}, radius {rt(R2)}.', f'B1 sign error explained; B1 centre {pt(a, b)} and radius {rt(R2)}')
    if fr == 'r2':
        return Q(f'{nm} says the circle {circ_eq(a, b, R2)} has radius {R2}. Explain the error.',
                 f'The right-hand side is r², so r = √{R2} = {rt(R2)}.', f'B1 RHS is r²; B1 r = {rt(R2)}')
    P_ = (a + r.randint(-6, 6), b + r.randint(-6, 6))
    dd = d2(P_, (a, b))
    where = 'inside' if dd < R2 else ('on' if dd == R2 else 'outside')
    return Q(f'Determine whether the point {pt(*P_)} lies inside, on or outside the circle {circ_eq(a, b, R2)}, explaining your reasoning.',
             f'Distance² from centre {pt(a, b)} is {dd}, compared with r² = {R2}: the point is {where} the circle.', f'M1 distance² from centre = {dd}; A1 compares with {R2}: {where}')


@g33.add('C3', (1, 2, 3, 4, 5), 'numerical')
def g33_calc(r, D):
    a, b = r.randint(-7, 7), r.randint(-7, 7)
    R2 = r.choice(list(PY))
    if D == 1:
        return Q(f'Write down the equation of the circle with centre {pt(a, b)} and radius {rt(R2)}.', circ_eq(a, b, R2).replace('(x + 0)', 'x').replace('(y + 0)', 'y'), f'B1 {circ_eq(a, b, R2)}'.replace('(x + 0)', 'x').replace('(y + 0)', 'y'))
    if D == 2:
        c = a * a + b * b - R2
        eqn = circ_exp(a, b, 0) + (sg(c) if c else '') + ' = 0'
        return Q(f'Find the centre and the exact radius of the circle {eqn}.', f'centre {pt(a, b)}, radius {rt(R2)}', f'M1 completes the square for x and y; A1 centre {pt(a, b)}; A1 radius {rt(R2)}')
    if D == 3:
        u = circ_pt(r, R2)
        A = (a + u[0], b + u[1])
        B = (a - u[0], b - u[1])
        return Q(f'The points A{pt(*A)} and B{pt(*B)} are the ends of a diameter of a circle. Find the equation of the circle.', circ_eq(a, b, R2),
                 f'B1 centre = midpoint {pt(a, b)}; M1 r² = {R2} (from centre to A, or (AB/2)²); A1 {circ_eq(a, b, R2)}')
    u = circ_pt(r, R2)
    if u[1] == 0:
        u = (u[1], u[0])
    P_ = (a + u[0], b + u[1])
    m = Fr(-u[0], u[1])
    tan = line_through(P_, m)
    if D == 4:
        return Q(f'The point P{pt(*P_)} lies on the circle {circ_eq(a, b, R2)}. Find the equation of the tangent to the circle at P, in the form ax + by + c = 0.', tan,
                 f'B1 centre {pt(a, b)}; M1 gradient of radius {num(Fr(u[1], u[0])) if u[0] else "undefined"}; M1 tangent gradient {num(m)}; A1 {tan}')
    # D5 where tangent meets x-axis
    if m == 0:
        return None
    X = P_[0] - Fr(P_[1]) / m
    return Q(f'The point P{pt(*P_)} lies on the circle {circ_eq(a, b, R2)}. The tangent to the circle at P meets the x-axis at T. Find the coordinates of T and the exact length PT.',
             f'T{pt(X, 0)}; PT = √({num(d2(P_, (X, 0)))})', f'B1 centre; M1 perpendicular gradient {num(m)}; A1 tangent {tan}; M1 y = 0; A1 T{pt(X, 0)}; B1 PT = √({num(d2(P_, (X, 0)))})')


def g33_c4(r, D):
    a, b = r.randint(-5, 5), r.randint(-5, 5)
    R2 = r.choice([25, 50, 65, 85, 100, 13, 26])
    u = circ_pt(r, R2)
    if u[1] == 0 or u[0] == 0:
        u = (3, 4) if R2 == 25 else u
        if u[0] == 0 or u[1] == 0:
            return None
    A = (a + u[0], b + u[1])
    B = (a - u[0], b - u[1])
    c = a * a + b * b - R2
    eqn = circ_exp(a, b, 0) + (sg(c) if c else '') + ' = 0'
    intro = f'A circle has equation {eqn}.'
    m = Fr(-u[0], u[1])
    parts = [
        P('Find the centre and radius of the circle.', f'centre {pt(a, b)}, radius {rt(R2)}', f'M1 completes the square; A1 centre {pt(a, b)}; A1 r = {rt(R2)}'),
        P(f'Show that the point A{pt(*A)} lies on the circle.', 'Substitution gives 0 (or distance from centre = radius).', f'B1 substitutes A and obtains 0 / distance² = {R2}'),
        P(f'The point A{pt(*A)} lies on the circle. Find the coordinates of the other end of the diameter through A.', pt(*B), f'M1 centre is midpoint; A1 {pt(*B)}'),
        P(f'The point A{pt(*A)} lies on the circle. Find the equation of the tangent to the circle at A, in the form ax + by + c = 0.', line_through(A, m), f'B1 radius gradient {num(Fr(u[1], u[0]))}; M1 negative reciprocal {num(m)}; A1 {line_through(A, m)}'),
        P(f'The tangents at A{pt(*A)} and at the other end of that diameter are parallel. Explain why.', 'Both are perpendicular to the same diameter, so they have the same gradient.', 'B1 both perpendicular to the diameter AB'),
    ]
    return cmp_(r, intro, parts)


g33.add('C4', (2, 3, 4, 5))(g33_c4)


# ---------------------------------------------------------------- 3.4 intersections of lines and curves
g34 = T('Intersection of lines and curves', 'intersection of lines and curves', 'intersection')
g34.fixed('C1', (1, 2), [
    ('A line and a circle are solved simultaneously and the quadratic obtained has a negative discriminant. The line', 'does not meet the circle', 'No real roots, so no points of intersection.', ['is a tangent', 'cuts the circle twice', 'passes through the centre']),
    ('How many points of intersection do the lines y = 2x + 1 and y = 2x − 3 have?', '0', 'Same gradient, different intercepts: parallel lines.', ['1', '2', 'infinitely many']),
    ('Where does the line y = 2x − 4 meet the x-axis?', '(2, 0)', 'Set y = 0: 2x = 4.', ['(0, −4)', '(−2, 0)', '(4, 0)']),
    ('The curve y = x² and the line y = 4 meet at', '(−2, 4) and (2, 4)', 'x² = 4 gives x = ±2.', ['(2, 4) only', '(4, 16) and (−4, 16)', '(0, 4)']),
])
g34.fixed('C2', (2, 3), [
    ('Explain how to show that a line is a tangent to a circle without finding the point of contact.', 'Substitute the line into the circle to get a quadratic in x and show its discriminant is zero; alternatively show the distance from the centre to the line equals the radius.', 'B1 discriminant = 0 method; B1 or perpendicular distance equals radius [2]'),
    ('Explain why a straight line can meet a circle in at most two points.', 'Substituting the linear equation into the circle gives a quadratic equation, which has at most two real roots.', 'B1 quadratic after substitution; B1 at most two roots [2]'),
])


@g34.add('C1', (1, 2, 3))
def g34_c1(r, D):
    m1, m2 = r.sample(range(-5, 6), 2)
    c1, c2 = r.randint(-9, 9), r.randint(-9, 9)
    X = Fr(c2 - c1, m1 - m2)
    Y = m1 * X + c1
    return MC(r, f'Find the point of intersection of the lines y = {lin(m1, c1)} and y = {lin(m2, c2)}.'.replace('y = 0x', 'y = '), pt(X, Y), [pt(-X, Y), pt(X, -Y), pt(Y, X), pt(X, m2 * X + c1)],
              f'{lin(m1, c1)} = {lin(m2, c2)} ⇒ x = {num(X)}, y = {num(Y)}.')


@g34.add('C2', (2, 3, 4), 'explain')
def g34_show(r, D):
    m = r.choice([1, 2, 3])
    k = r.randint(1, 3)
    a, b = r.randint(-4, 4), r.randint(-4, 4)
    R2 = (1 + m * m) * k * k
    sgn_ = r.choice([1, -1])
    c = sgn_ * (1 + m * m) * k + b - m * a
    if r.random() < 0.5:
        return Q(f'Show that the line y = {lin(m, c)} is a tangent to the circle {circ_eq(a, b, R2)}.'.replace('(x + 0)', 'x').replace('(y + 0)', 'y'),
                 'Substitution gives a quadratic in x with discriminant 0 (repeated root), so the line touches the circle.',
                 f'M1 substitutes and forms a quadratic in x; A1 discriminant = 0 shown, conclusion tangent')
    c2 = c + sgn_ * r.randint(1, 4)
    return Q(f'Show that the line y = {lin(m, c2)} does not meet the circle {circ_eq(a, b, R2)}.'.replace('(x + 0)', 'x').replace('(y + 0)', 'y'),
             'Substitution gives a quadratic in x with negative discriminant, so there are no points of intersection.',
             f'M1 substitutes and forms a quadratic in x; A1 discriminant < 0 shown, conclusion')


@g34.add('C3', (1, 2, 3, 4, 5), 'numerical')
def g34_calc(r, D):
    if D <= 3:
        a, b = r.randint(-4, 4), r.randint(-4, 4)
        R2 = r.choice([25, 50, 65, 85, 100, 125, 130])
        lat = [(x, y) for x in range(-12, 13) for y in range(-12, 13) if x * x + y * y == R2]
        for _ in range(40):
            p, q = r.sample(lat, 2)
            if p[0] != q[0] and p[1] != q[1] and (p[0] != -q[0] or p[1] != -q[1]):
                break
        else:
            return None
        A, B = sorted([(a + p[0], b + p[1]), (a + q[0], b + q[1])])
        m = grad(A, B)
        eq = line_through(A, m)
        return Q(f'Find the coordinates of the points where the line {eq} meets the circle {circ_eq(a, b, R2)}.'.replace('(x + 0)', 'x').replace('(y + 0)', 'y'),
                 f'{pt(*A)} and {pt(*B)}', 'M1 makes x or y the subject and substitutes; M1 forms and solves a quadratic; A1 x-values; A1 both points')
    m = r.choice([1, 2, 3])
    k = r.randint(1, 4)
    a, b = r.randint(-4, 4), r.randint(-4, 4)
    R2 = (1 + m * m) * k * k
    cs_ = sorted([(1 + m * m) * k + b - m * a, -(1 + m * m) * k + b - m * a])
    stem = f'The line y = {m if m > 1 else ""}x + c is a tangent to the circle {circ_eq(a, b, R2)}. Find the possible values of c.'.replace('(x + 0)', 'x').replace('(y + 0)', 'y')
    if D == 5:
        stem = f'Find the set of values of c for which the line y = {m if m > 1 else ""}x + c meets the circle {circ_eq(a, b, R2)} at two distinct points.'.replace('(x + 0)', 'x').replace('(y + 0)', 'y')
        return Q(stem, ineq_in(cs_[0], cs_[1], var='c'), f'M1 substitutes; M1 discriminant > 0; A1 critical values {num(cs_[0])}, {num(cs_[1])}; A1 {ineq_in(cs_[0], cs_[1], var="c")}')
    return Q(stem, f'c = {num(cs_[0])} or c = {num(cs_[1])}', f'M1 substitutes to form a quadratic in x; M1 discriminant = 0; A1 c = {num(cs_[0])}, {num(cs_[1])}')


def g34_c4(r, D):
    sy = q14_sys(r, 3)
    if not sy:
        return None
    (x1, y1), (x2, y2) = sy['pts']
    intro = f'The line {sy["line"]} meets the curve {sy["curve"]} at the points P and Q.'
    M = mid((x1, y1), (x2, y2))
    parts = [
        P('Find the coordinates of P and Q.', f'{pt(x1, y1)} and {pt(x2, y2)}', f'M1 substitution gives {sy["sub"]}; A1 x-values; A1 points'),
        P('Find the exact length of PQ.', rt(d2((x1, y1), (x2, y2))), f'M1 distance formula; A1 {rt(d2((x1, y1), (x2, y2)))}'),
        P('Find the coordinates of the midpoint of PQ.', pt(*M), f'B1 {pt(*M)}'),
    ]
    if sy['kind'] == 'circ':
        parts.append(P('Show that the perpendicular bisector of PQ passes through the origin.', 'The origin is the centre of the circle, and the perpendicular bisector of any chord passes through the centre.', 'B1 chord property / verifies equation through (0, 0)'))
    return cmp_(r, intro, parts)


g34.add('C4', (2, 3, 4, 5))(g34_c4)

CHAPTERS[3] = [g31, g32, g33, g34]


# ================================================================ Chapter 4 Circular measure

def rad3(x):
    return n3(x) + ' rad'


EXACT_DEG = [15, 18, 20, 30, 36, 40, 45, 60, 72, 75, 90, 105, 108, 120, 135, 150, 160, 210, 225, 240, 270, 300, 315, 330, 135, 144, 165, 200]


c41 = T('Radian measure and converting between degrees and radians', 'radian measure', 'converting between degrees and radians', 'radians')
c41.fixed('C1', (1, 2), [
    ('One radian is the angle subtended at the centre of a circle by an arc whose length is', 'equal to the radius', 'Definition of the radian: arc length = radius.', ['equal to the diameter', 'π times the radius', 'one unit']),
    ('How many radians are there in 180°?', 'π', 'Half a turn: 2π/2 = π.', ['2π', 'π/2', '180']),
    ('Which is the best approximation to 1 radian in degrees?', '57.3°', '180°/π ≈ 57.3°.', ['60°', '3.14°', '90°']),
    ('A full turn, measured in radians, is', '2π', '360° = 2π radians.', ['π', '360π', '4π']),
    ('To convert an angle from radians to degrees, multiply by', '180/π', 'π rad = 180°, so 1 rad = 180/π degrees.', ['π/180', '360/π', '2π']),
])
c41.fixed('C2', (2, 3), [
    ('Explain why a full turn is 2π radians.', 'The arc for a full turn is the whole circumference 2πr; an angle of 1 radian has arc r, so the full turn is 2πr/r = 2π radians.', 'B1 circumference 2πr; B1 divide by r for each radian [2]'),
    ('Explain why the formula s = rθ only works when θ is measured in radians.', 'It comes from s/(2πr) = θ/(2π), i.e. the arc is the same fraction of the circumference as θ is of 2π; that is only true when the full turn is 2π, i.e. radians.', 'B1 fraction of circle argument; B1 full turn 2π only in radians [2]'),
    ('Explain why the radian is a natural unit for measuring angles.', 'It is defined by the circle itself (arc length = radius), not by an arbitrary division into 360, and it makes the arc and sector formulae simply s = rθ and A = ½r²θ.', 'B1 defined by arc = radius; B1 simpler formulae [2]'),
])


@c41.add('C1', (1, 2, 3))
def c41_c1(r, D):
    d = r.choice(EXACT_DEG)
    f = Fr(d, 180)
    if r.random() < 0.5 or D == 1:
        return MC(r, f'Express {d}° in radians, giving your answer as an exact multiple of π.', pi_frac(f),
                  [pi_frac(Fr(180, d)) if d != 180 else '2π', pi_frac(f * 2), pi_frac(Fr(d, 360)), pi_frac(f + Fr(1, 6))], f'{d} × π/180 = {pi_frac(f)}.')
    return MC(r, f'Express {pi_frac(f)} radians in degrees.', f'{d}°', [f'{num(Fr(d, 2))}°', f'{2 * d}°', f'{num(round(d * math.pi, 1))}°', f'{d + 30}°'], f'{pi_frac(f)} × 180/π = {d}°.')


@c41.add('C2', (2, 3, 4), 'explain')
def c41_err(r, D):
    nm = person(r)
    if r.random() < 0.5:
        d = r.choice([20, 25, 40, 50, 65, 80, 100, 110, 130, 140, 170])
        wrong = d * 180 / math.pi
        return Q(f'{nm} converts {d}° to radians by multiplying by 180/π and gets {n3(wrong)}. Explain the error and give the correct value to 3 significant figures.',
                 f'To convert degrees to radians multiply by π/180 (a radian is larger than a degree, so the number should get smaller): {d}° = {n3(d * math.pi / 180)} rad.',
                 f'B1 should multiply by π/180 (number must decrease); B1 {n3(d * math.pi / 180)}')
    x = r.choice([0.6, 0.8, 1.2, 1.5, 2.1, 2.4, 2.8, 3.5, 4.2, 5])
    return Q(f'{nm} says that an angle of {x} radians is smaller than an angle of {round(x * 50)}°. Is {nm} correct? Explain your answer.',
             f'{x} rad = {d1(x * 180 / math.pi)}, which is {"larger" if x * 180 / math.pi > round(x * 50) else "smaller"} than {round(x * 50)}°, so {nm} is {"wrong" if x * 180 / math.pi > round(x * 50) else "correct"}.',
             f'M1 converts {x} × 180/π = {d1(x * 180 / math.pi)}; A1 correct comparison and conclusion')


@c41.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c41_calc(r, D):
    if D == 1:
        d = r.choice([12, 24, 48, 54, 63, 84, 96, 112, 126, 154, 168, 200, 250, 290, 310, 345])
        return Q(f'Convert {d}° to radians, giving your answer correct to 3 significant figures.', rad3(d * math.pi / 180), f'M1 × π/180; A1 {n3(d * math.pi / 180)}')
    if D == 2:
        x = r.choice([0.35, 0.7, 1.1, 1.25, 1.9, 2.3, 2.75, 3.6, 4.4, 5.2, 0.45, 1.65])
        return Q(f'Convert {x} radians to degrees, giving your answer correct to 1 decimal place.', d1(x * 180 / math.pi), f'M1 × 180/π; A1 {d1(x * 180 / math.pi)}')
    if D == 3:
        t = r.choice([5, 10, 12, 15, 20, 25, 35, 40, 45, 50])
        hand = r.choice(['minute hand', 'hour hand'])
        frac_ = Fr(t, 60) if hand == 'minute hand' else Fr(t, 720)
        return Q(f'Find, as an exact multiple of π, the angle in radians turned through by the {hand} of a clock in {t} minutes.', pi_frac(2 * frac_),
                 f'M1 fraction of a full turn {num(frac_)}; A1 {num(frac_)} × 2π = {pi_frac(2 * frac_)}')
    if D == 4:
        h, m = r.randint(1, 11), r.choice([0, 10, 20, 30, 40, 50])
        ang = abs(Fr(30 * h) + Fr(m, 2) - 6 * m)
        if ang > 180:
            ang = 360 - ang
        return Q(f'Find, as an exact multiple of π, the smaller angle between the hour hand and the minute hand of a clock at {h}:{m:02d}.', pi_frac(ang / 180),
                 f'B1 hour hand {num(30 * h + Fr(m, 2))}° from 12; B1 minute hand {6 * m}°; M1 difference (smaller angle) {num(ang)}°; A1 {pi_frac(ang / 180)}')
    rev = r.choice([2.5, 3.25, 4.75, 6.5, 12, 15.5, 20])
    t = r.choice([2, 3, 4, 5, 8, 10])
    w = rev * 2 * math.pi / t
    return Q(f'A wheel of a bicycle in {city(r)} turns through {rev} revolutions in {t} seconds. Find the angle turned through in radians per second, correct to 3 significant figures, and the time to turn through 100 radians.',
             f'{n3(w)} rad/s; {n3(100 / w)} s', f'M1 {rev} × 2π = {n3(rev * 2 * math.pi)} rad; A1 ÷ {t} = {n3(w)} rad/s; B1 100/{n3(w)} = {n3(100 / w)} s')


def c41_c4(r, D):
    t = r.choice([8, 12, 16, 18, 24, 36, 40])
    L = r.choice([6, 8, 9, 10, 12, 15])
    nm = person(r)
    frac_ = Fr(t, 60)
    th = 2 * frac_
    intro = f'The minute hand of a clock in a station in {city(r)} has length {L} cm. {nm} watches it for {t} minutes.'
    parts = [
        P('Find, as an exact multiple of π, the angle in radians through which the minute hand turns.', pi_frac(th), f'M1 {t}/60 × 2π; A1 {pi_frac(th)}'),
        P('Convert this angle to degrees.', f'{num(th * 180)}°', f'B1 {num(th * 180)}°'),
        P('Find the exact distance travelled by the tip of the minute hand.', f'{pi_frac(th * L)} cm', f'M1 s = rθ = {L} × {pi_frac(th)}; A1 {pi_frac(th * L)} cm'),
        P('Find the exact area swept out by the minute hand.', f'{pi_frac(th * L * L / 2)} cm²', f'M1 ½r²θ; A1 {pi_frac(th * L * L / 2)} cm²'),
        P('Find the time, in minutes, for the minute hand to turn through 1 radian, correct to 3 significant figures.', f'{n3(60 / (2 * math.pi))} minutes', f'M1 60/(2π); A1 {n3(60 / (2 * math.pi))}'),
    ]
    return cmp_(r, intro, parts)


c41.add('C4', (2, 3, 4, 5))(c41_c4)


# ---------------------------------------------------------------- 4.2 arc length and sector area
c42 = T('Arc length s = rθ and sector area ½r²θ', 'arc length', 'sector area')
c42.fixed('C1', (1, 2), [
    ('A sector has radius 6 cm and angle 0.5 radians. What is its arc length?', '3 cm', 's = rθ = 6 × 0.5.', ['9 cm', '18 cm', '1.5 cm']),
    ('A sector has radius 4 cm and angle 1.5 radians. What is its area?', '12 cm²', '½ × 16 × 1.5 = 12.', ['6 cm²', '24 cm²', '9 cm²']),
    ('What is the perimeter of a sector with radius r and angle θ radians?', '2r + rθ', 'Two radii plus the arc.', ['r + rθ', '2r + ½r²θ', 'rθ']),
    ('A sector of radius 10 cm has area 30 cm². What is the angle at the centre?', '0.6 radians', '½ × 100 × θ = 30 ⇒ θ = 0.6.', ['0.3 radians', '3 radians', '6 radians']),
])
c42.fixed('C2', (2, 3), [
    ('Explain why the area of a sector of angle θ radians is ½r²θ.', 'The sector is the fraction θ/(2π) of the circle, so its area is (θ/(2π)) × πr² = ½r²θ.', 'B1 fraction θ/2π; B1 simplifies πr² × θ/2π [2]'),
    ('A sector and a circle have the same radius. Explain why the sector with angle 2π has the same area as the circle.', '½r²(2π) = πr², the area of the whole circle, since an angle of 2π is a full turn.', 'B1 substitution; B1 full turn [2]'),
])


@c42.add('C1', (1, 2, 3))
def c42_c1(r, D):
    R = r.choice([4, 5, 6, 8, 9, 10, 12, 15])
    if D == 1:
        th = r.choice([0.4, 0.6, 0.8, 1.2, 1.4, 1.6, 2.2, 2.5])
        s = R * th
        return MC(r, f'A sector has radius {R} cm and angle {th} radians. Find the arc length.', f'{num(round(s, 4))} cm', [f'{num(round(R * R * th / 2, 4))} cm', f'{num(round(R * th / 2, 4))} cm', f'{num(round(2 * R + s, 4))} cm', f'{num(round(s * 2, 4))} cm'], f's = rθ = {R} × {th} = {num(round(s, 4))} cm.')
    f = r.choice([Fr(1, 6), Fr(1, 4), Fr(1, 3), Fr(2, 3), Fr(5, 6), Fr(3, 4), Fr(1, 5), Fr(2, 5), Fr(1, 2)])
    A = Fr(R * R, 2) * f
    return MC(r, f'A sector has radius {R} cm and angle {pi_frac(f)} radians. Find the exact area of the sector.', f'{pi_frac(A)} cm²', [f'{pi_frac(R * f)} cm²', f'{pi_frac(A * 2)} cm²', f'{pi_frac(A / R)} cm²', f'{pi_frac(R * R * f * f)} cm²'], f'½r²θ = ½ × {R * R} × {pi_frac(f)} = {pi_frac(A)}.')


@c42.add('C2', (2, 3, 4), 'explain')
def c42_err(r, D):
    nm = person(r)
    R = r.choice([5, 6, 7, 8, 9, 10, 12])
    d = r.choice([40, 50, 70, 80, 100, 110, 130, 140])
    return Q(f'A sector has radius {R} cm and angle {d}°. {nm} calculates the arc length as {R} × {d} = {R * d} cm. Explain the error and find the correct arc length to 3 significant figures.',
             f's = rθ needs θ in radians: {d}° = {n3(d * math.pi / 180)} rad, so s = {n3(R * d * math.pi / 180)} cm.', f'B1 θ must be in radians; B1 {n3(R * d * math.pi / 180)} cm')


@c42.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c42_calc(r, D):
    R = r.choice([3.5, 4, 5, 6, 7.5, 8, 9, 10, 12, 14])
    th = r.choice([0.45, 0.7, 0.9, 1.2, 1.35, 1.8, 2.1, 2.6])
    if D == 1:
        return Q(f'A sector has radius {num(R)} cm and angle {th} radians. Find its perimeter.', f'{n3(2 * R + R * th)} cm', f'M1 2r + rθ; A1 {n3(2 * R + R * th)} cm')
    if D == 2:
        A = 0.5 * R * R * th
        return Q(f'A sector of a circle of radius {num(R)} cm has area {n3(A)} cm². Find the angle of the sector in radians.', f'{n3(th)} rad', f'M1 ½ × {num(R * R)} × θ = {n3(A)}; A1 θ = {n3(th)}')
    if D == 3:
        s = R * th
        return Q(f'A sector has arc length {n3(s)} cm and angle {th} radians. Find the radius and the area of the sector.', f'r = {n3(R)} cm; area {n3(0.5 * R * R * th)} cm²',
                 f'M1 r = s/θ; A1 {n3(R)}; M1 ½r²θ; A1 {n3(0.5 * R * R * th)} cm²')
    # D4/5: perimeter and area given -> solve for r and θ
    Ri, ti = r.choice([(4, Fr(3, 2)), (5, Fr(6, 5)), (6, Fr(2, 3)), (8, Fr(1, 2)), (10, Fr(4, 5)), (3, 2), (6, Fr(5, 3)), (5, 2)])
    Pp = 2 * Ri + Ri * ti
    A = Fr(Ri * Ri, 2) * ti
    # r² θ = 2A, 2r + rθ = P -> rθ = P − 2r -> r(P − 2r) = 2A -> 2r² − Pr + 2A = 0
    other = Fr(Pp, 2) - Ri
    oth_th = (Pp - 2 * other) / other if other else None
    ok = other > 0 and oth_th is not None and oth_th > 0 and oth_th < 2 * math.pi
    ans = f'r = {num(Ri)}, θ = {num(ti)}' + (f'; or r = {num(other)}, θ = {num(oth_th)}' if ok and other != Ri else '')
    return Q(f'A sector of a circle has perimeter {num(Pp)} cm and area {num(A)} cm². Find the possible values of the radius r and the angle θ in radians.', ans,
             f'B1 2r + rθ = {num(Pp)}; B1 ½r²θ = {num(A)}; M1 eliminates θ: 2r² − {num(Pp)}r + {num(2 * A)} = 0; A1 r values; A1 corresponding θ')


def c42_c4(r, D):
    R = r.choice([6, 8, 10, 12, 15])
    k = r.choice([2, 3, 4])
    th = r.choice([Fr(1, 3), Fr(1, 4), Fr(1, 6), Fr(2, 5)])
    nm = person(r)
    intro = f'A garden designer in {city(r)} draws a flower bed in the shape of a sector OAB of a circle with centre O, radius {R} m and angle AOB = {pi_frac(th)} radians.'
    s = R * th
    parts = [
        P('Find the exact length of the arc AB.', f'{pi_frac(s)} m', f'M1 rθ; A1 {pi_frac(s)} m'),
        P('Find the perimeter of the flower bed, correct to 3 significant figures.', f'{n3(2 * R + float(s) * math.pi)} m', f'M1 2 × {R} + arc; A1 {n3(2 * R + float(s) * math.pi)} m'),
        P('Find the exact area of the flower bed.', f'{pi_frac(Fr(R * R, 2) * th)} m²', f'M1 ½r²θ; A1 {pi_frac(Fr(R * R, 2) * th)} m²'),
        P(f'{nm} enlarges the bed by increasing the radius to {R + k} m, keeping the same angle. Find the exact increase in area.', f'{pi_frac(Fr((R + k) ** 2 - R * R, 2) * th)} m²',
          f'M1 ½({R + k}² − {R}²) × {pi_frac(th)}; A1 {pi_frac(Fr((R + k) ** 2 - R * R, 2) * th)} m²'),
        P('Find, in radians to 3 significant figures, the angle a sector of the same radius would need for an area of 20 m².', f'{n3(40 / (R * R))} rad', f'M1 ½ × {R * R} × θ = 20; A1 θ = {n3(40 / (R * R))}'),
    ]
    return cmp_(r, intro, parts)


c42.add('C4', (2, 3, 4, 5))(c42_c4)


# ---------------------------------------------------------------- 4.3 segments and triangles
c43 = T('Problems involving arcs, sectors, segments and triangles', 'problems involving arcs, sectors, segments and triangles', 'segments', 'segment')
c43.fixed('C1', (1, 2), [
    ('The area of a minor segment cut off by a chord subtending θ radians at the centre of a circle of radius r is', '½r²(θ − sin θ)', 'Sector ½r²θ minus triangle ½r² sin θ.', ['½r²(θ + sin θ)', '½r²θ', 'r²(θ − sin θ)']),
    ('A chord subtends an angle θ at the centre of a circle of radius r. The length of the chord is', '2r sin(θ/2)', 'Split the isosceles triangle into two right-angled triangles.', ['rθ', '2r cos(θ/2)', 'r sin θ']),
    ('The area of triangle OAB with OA = OB = r and angle AOB = θ is', '½r² sin θ', 'Area = ½ab sin C.', ['½r²θ', 'r² sin θ', '½r² cos θ']),
    ('A chord subtends an angle of π/3 at the centre of a circle of radius 8 cm. The chord has length', '8 cm', 'The triangle is equilateral.', ['4 cm', '8π/3 cm', '16 cm']),
])
c43.fixed('C2', (2, 3), [
    ('Explain why the area of a segment is found by subtracting the area of a triangle from the area of a sector.', 'The sector is made up of the triangle formed by the two radii and the chord, together with the segment between the chord and the arc.', 'B1 sector = triangle + segment; B1 so segment = sector − triangle [2]'),
    ('Explain why a calculator must be in radian mode when evaluating ½r²(θ − sin θ) with θ in radians.', 'θ is in radians in the formula, so sin θ must be evaluated for that same radian angle; in degree mode the calculator treats θ as degrees.', 'B1 θ is a radian measure; B1 degree mode gives sin of a different angle [2]'),
])


def chord(R, th):
    return 2 * R * math.sin(th / 2)


@c43.add('C1', (1, 2, 3))
def c43_c1(r, D):
    R = r.choice([5, 6, 8, 10, 12])
    th = r.choice([0.8, 1.2, 1.5, 2, 2.4])
    kind = r.choice(['chord', 'tri'])
    if kind == 'chord':
        c = chord(R, th)
        return MC(r, f'A chord AB of a circle with centre O and radius {R} cm subtends an angle of {th} radians at O. Find the length of AB, correct to 3 significant figures.', f'{n3(c)} cm',
                  [f'{n3(R * th)} cm', f'{n3(2 * R * math.cos(th / 2))} cm', f'{n3(R * math.sin(th))} cm', f'{n3(2 * R * math.sin(th))} cm'], f'AB = 2r sin(θ/2) = {n3(c)} cm.')
    A = 0.5 * R * R * math.sin(th)
    return MC(r, f'Triangle OAB has OA = OB = {R} cm and angle AOB = {th} radians. Find its area, correct to 3 significant figures.', f'{n3(A)} cm²',
              [f'{n3(0.5 * R * R * th)} cm²', f'{n3(R * R * math.sin(th))} cm²', f'{n3(abs(0.5 * R * R * math.cos(th)) + 1)} cm²', f'{n3(0.5 * R * R * (th - math.sin(th)))} cm²'], f'½r² sin θ = {n3(A)} cm².')


@c43.add('C2', (2, 3, 4), 'explain')
def c43_err(r, D):
    nm = person(r)
    R = r.choice([5, 6, 8, 9, 10, 12])
    th = r.choice([0.8, 1.1, 1.4, 1.7, 2.2, 2.5])
    seg = 0.5 * R * R * (th - math.sin(th))
    wrong = 0.5 * R * R * (th - math.sin(math.radians(th)))
    if r.random() < 0.5:
        return Q(f'A segment of a circle of radius {R} cm is cut off by a chord subtending {th} radians at the centre. {nm} obtains an area of {n3(wrong)} cm². Explain the likely error and find the correct area.',
                 f'{nm} evaluated sin {th} in degree mode; with radians the area is ½ × {R * R} × ({th} − sin {th}) = {n3(seg)} cm².', f'B1 calculator in degree mode / sin {th} must be in radians; B1 {n3(seg)} cm²')
    return Q(f'A chord subtends {th} radians at the centre of a circle of radius {R} cm. {nm} says the perimeter of the minor segment is the arc length {n3(R * th)} cm. Explain why this is incomplete and find the perimeter.',
             f'The segment is bounded by the arc and the chord: chord = 2 × {R} sin({th}/2) = {n3(chord(R, th))} cm, so perimeter = {n3(R * th + chord(R, th))} cm.',
             f'B1 must include the chord; B1 {n3(R * th + chord(R, th))} cm')


EXACT_TH = [(Fr(1, 3), '√3/2', math.sqrt(3) / 2), (Fr(2, 3), '√3/2', math.sqrt(3) / 2), (Fr(1, 6), '1/2', 0.5), (Fr(5, 6), '1/2', 0.5), (Fr(1, 2), '1', 1.0)]


@c43.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c43_calc(r, D):
    R = r.choice([4, 5, 6, 7, 8, 9, 10, 12, 15])
    if D <= 2:
        th = r.choice([0.6, 0.9, 1.1, 1.3, 1.6, 1.9, 2.3, 2.7])
        seg = 0.5 * R * R * (th - math.sin(th))
        return Q(f'A chord of a circle of radius {R} cm subtends an angle of {th} radians at the centre. Find the area of the minor segment.', f'{n3(seg)} cm²',
                 f'M1 sector ½ × {R * R} × {th}; M1 triangle ½ × {R * R} × sin {th}; A1 {n3(seg)} cm²')
    if D == 3:
        th = r.choice([0.6, 0.9, 1.1, 1.3, 1.6, 1.9, 2.3, 2.7])
        return Q(f'A chord AB of a circle with centre O and radius {R} cm subtends an angle of {th} radians at O. Find the perimeter of the minor segment cut off by AB.', f'{n3(R * th + chord(R, th))} cm',
                 f'B1 arc {n3(R * th)}; M1 chord 2 × {R} sin({th / 2}) or cosine rule; A1 {n3(chord(R, th))}; A1 {n3(R * th + chord(R, th))} cm')
    if D == 4:
        f, sv, _ = r.choice(EXACT_TH)
        Rs = R * R
        # exact segment area: ½R²(fπ − s)
        term_pi = pi_frac(Fr(Rs, 2) * f)
        sval = {'√3/2': f'{num(Fr(Rs, 4))}√3', '1/2': num(Fr(Rs, 4)), '1': num(Fr(Rs, 2))}[sv]
        return Q(f'A chord of a circle of radius {R} cm subtends an angle of {pi_frac(f)} radians at the centre. Find the exact area of the minor segment.', f'({term_pi} − {sval}) cm²',
                 f'M1 sector ½ × {Rs} × {pi_frac(f)} = {term_pi}; M1 triangle ½ × {Rs} × sin({pi_frac(f)}) with sin = {sv}; A1 {term_pi} − {sval}')
    # D5: tangent region: sector OAB, tangent at A meets OB extended at T
    th = r.choice([0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2])
    AT = R * math.tan(th)
    region = 0.5 * R * AT - 0.5 * R * R * th
    per = AT + (R / math.cos(th) - R) + R * th
    return Q(f'OAB is a sector of a circle with centre O, radius {R} cm and angle AOB = {th} radians. The tangent to the circle at A meets OB extended at T. Find the area and the perimeter of the region bounded by AT, TB and the arc AB.',
             f'area {n3(region)} cm²; perimeter {n3(per)} cm', f'B1 AT = {R} tan {th} = {n3(AT)}; M1 triangle OAT − sector; A1 area {n3(region)}; M1 OT = {R}/cos {th}, BT = OT − {R}; A1 perimeter {n3(per)}')


def c43_c4(r, D):
    R = r.choice([6, 8, 10, 12])
    f, sv, sf_ = r.choice(EXACT_TH[:4])
    th = float(f) * math.pi
    intro = f'A circle has centre O and radius {R} cm. The chord AB subtends an angle of {pi_frac(f)} radians at O.'
    ch = chord(R, th)
    parts = [
        P('Find the exact length of the arc AB.', f'{pi_frac(R * f)} cm', f'B1 {pi_frac(R * f)}'),
        P('Find the length of the chord AB, correct to 3 significant figures.', f'{n3(ch)} cm', f'M1 2r sin(θ/2); A1 {n3(ch)} cm'),
        P('Find the area of the minor segment, correct to 3 significant figures.', f'{n3(0.5 * R * R * (th - math.sin(th)))} cm²', f'M1 sector − triangle; A1 {n3(0.5 * R * R * (th - math.sin(th)))} cm²'),
        P('Find the perimeter of the minor segment, correct to 3 significant figures.', f'{n3(R * th + ch)} cm', f'M1 arc + chord; A1 {n3(R * th + ch)} cm'),
        P('Find the area of the major segment, correct to 3 significant figures.', f'{n3(math.pi * R * R - 0.5 * R * R * (th - math.sin(th)))} cm²', f'M1 circle − minor segment; A1 {n3(math.pi * R * R - 0.5 * R * R * (th - math.sin(th)))} cm²'),
    ]
    return cmp_(r, intro, parts)


c43.add('C4', (2, 3, 4, 5))(c43_c4)

CHAPTERS[4] = [c41, c42, c43]


# ================================================================ Chapter 5 Trigonometry

R2_, R3_ = math.sqrt(2), math.sqrt(3)
EXV = [(0.0, '0'), (0.5, '1/2'), (R2_ / 2, '√2/2'), (R3_ / 2, '√3/2'), (1.0, '1'), (R3_, '√3'), (1 / R3_, '1/√3')]


def exstr(v):
    for x, s in EXV:
        if abs(abs(v) - x) < 1e-9:
            return ('' if v >= -1e-12 or s == '0' else MINUS) + s
    return None


def trigv(fn, deg):
    t = math.radians(deg)
    if fn == 'tan':
        if abs(math.cos(t)) < 1e-12:
            return None
        return math.tan(t)
    return math.sin(t) if fn == 'sin' else math.cos(t)


def sols(fn, k, b=1, c=0, lo=0, hi=360):
    """x in [lo, hi] (degrees) with fn(b x + c) = k."""
    if fn in ('sin', 'cos') and abs(k) > 1 + 1e-12:
        return []
    k = max(-1.0, min(1.0, k)) if fn != 'tan' else k
    if fn == 'sin':
        a = math.degrees(math.asin(k)); base, per = [a, 180 - a], 360
    elif fn == 'cos':
        a = math.degrees(math.acos(k)); base, per = [a, -a], 360
    else:
        a = math.degrees(math.atan(k)); base, per = [a], 180
    U0, U1 = b * lo + c, b * hi + c
    out = set()
    for n in range(-8, 12):
        for be in base:
            u = be + n * per
            if U0 - 1e-7 <= u <= U1 + 1e-7:
                out.add(round((u - c) / b, 7))
    return sorted(out)


def dlist(xs):
    return ', '.join(d1(x) for x in xs) if xs else 'no solutions'


def rlist(xs):
    return ', '.join(n3(math.radians(x)) for x in xs) if xs else 'no solutions'


def tl(B, K, f='cos x'):
    """'B f + K' e.g. '3 cos x − 2'."""
    out = ''
    if B:
        out = (MINUS if B < 0 else '') + ('' if abs(B) == 1 else num(abs(B)) + ' ') + f
    if K:
        out += (sg(K) if out else num(K))
    return out or '0'


SPECIAL = [120, 135, 150, 210, 225, 240, 300, 315, 330, 30, 45, 60, 390, 405, 420, -30, -45, -60, -120, -150]


t51 = T('Graphs of sine, cosine and tangent and exact values', 'graphs of sine, cosine and tangent', 'exact values')
t51.fixed('C1', (1, 2), [
    ('What is the period of y = sin 2x (x in degrees)?', '180°', 'Period of sin x is 360°; sin 2x completes a cycle twice as fast.', ['720°', '360°', '90°']),
    ('What is the amplitude of y = 3 cos x − 1?', '3', 'The coefficient of cos x gives the amplitude; −1 is a vertical translation.', ['−1', '2', '4']),
    ('What is the period of y = tan x (x in degrees)?', '180°', 'tan x repeats every 180°.', ['360°', '90°', '720°']),
    ('Which equation describes the asymptotes of y = tan x for 0° ≤ x ≤ 360°?', 'x = 90° and x = 270°', 'tan x = sin x/cos x is undefined where cos x = 0.', ['x = 0° and x = 180°', 'x = 180° only', 'y = ±1']),
    ('The graph of y = cos x is the graph of y = sin x translated by', '90° in the negative x-direction', 'cos x = sin(x + 90°).', ['90° in the positive x-direction', '180° in the positive x-direction', '1 unit upwards']),
    ('What is the range of f(x) = 5 − 2 sin x?', '3 ≤ f(x) ≤ 7', 'sin x varies from −1 to 1, so 5 − 2 sin x varies from 3 to 7.', ['−2 ≤ f(x) ≤ 2', '5 ≤ f(x) ≤ 7', '−7 ≤ f(x) ≤ −3']),
])
t51.fixed('C2', (2, 3), [
    ('Explain, using the graph of y = sin x, why sin(180° − x) = sin x.', 'The graph of y = sin x for 0° ≤ x ≤ 180° is symmetrical about x = 90°, so angles x and 180° − x, equally spaced either side of 90°, have the same sine.', 'B1 symmetry about x = 90°; B1 x and 180° − x equidistant from 90° [2]'),
    ('Explain why cos x = 2 has no solutions.', 'The range of cos x is −1 ≤ cos x ≤ 1, so it can never equal 2.', 'B1 range −1 to 1; B1 2 outside range [2]'),
    ('Explain why tan 45° = 1 using a right-angled triangle.', 'In a right-angled isosceles triangle the two shorter sides are equal and the angles are 45°, so tan 45° = opposite/adjacent = 1.', 'B1 isosceles right triangle; B1 equal sides give ratio 1 [2]'),
])


@t51.add('C1', (1, 2, 3))
def t51_c1(r, D):
    for _ in range(30):
        fn = r.choice(['sin', 'cos', 'tan'])
        a = r.choice(SPECIAL)
        v = trigv(fn, a)
        if v is not None and exstr(v):
            break
    else:
        return None
    c = exstr(v)
    ang = f'{a}°' if D < 3 else pi_frac(Fr(a, 180))
    pool = ['1/2', '√2/2', '√3/2', '√3', '1/√3', '1', MINUS + '1/2', MINUS + '√3/2', MINUS + '√2/2', MINUS + '√3', MINUS + '1/√3', MINUS + '1']
    opp = c[1:] if c.startswith(MINUS) else MINUS + c
    others = [opp] + [p for p in r.sample(pool, len(pool)) if p not in (c, opp)]
    return MC(r, f'Find the exact value of {fn} {ang}.' if D < 3 else f'Find the exact value of {fn}({ang}).', c, others[:5], f'Use the related acute angle and the sign of {fn} in the quadrant: {fn} {a}° = {c}.')


@t51.add('C2', (2, 3, 4), 'explain')
def t51_err(r, D):
    nm = person(r)
    fr = r.choice(['period', 'sign', 'range'])
    if fr == 'period':
        b = r.randint(2, 6)
        fn = r.choice(['sin', 'cos'])
        return Q(f'{nm} says that the period of y = {fn} {b}x is {360 * b}°. Explain the error and state the correct period.',
                 f'Multiplying x by {b} compresses the graph horizontally (stretch factor 1/{b}), so the period is 360° ÷ {b} = {num(Fr(360, b))}°.', f'B1 stretch factor 1/{b} / cycles faster; B1 {num(Fr(360, b))}°')
    if fr == 'sign':
        for _ in range(30):
            fn = r.choice(['sin', 'cos', 'tan'])
            a = r.choice([120, 135, 150, 210, 225, 240, 300, 315, 330])
            v = trigv(fn, a)
            if v is not None and exstr(v) and v < 0:
                break
        else:
            return None
        return Q(f'{nm} says that {fn} {a}° = {exstr(-v)}. Explain why {nm} is wrong.', f'{a}° is in a quadrant where {fn} is negative, so {fn} {a}° = {exstr(v)}.',
                 f'B1 identifies quadrant / sign of {fn}; B1 {fn} {a}° = {exstr(v)}')
    a, b = r.randint(1, 8), r.randint(2, 6)
    fn = r.choice(['sin', 'cos'])
    return Q(f'{nm} says that the greatest value of f(x) = {a} − {b} {fn} x is {num(a - b)}, because the greatest value of {fn} x is 1. Explain the error and state the greatest and least values of f(x).',
             f'Because {fn} x is multiplied by −{b}, f is greatest when {fn} x is least (−1): greatest value {a + b}; least value {num(a - b)} (when {fn} x = 1).',
             f'B1 negative coefficient so greatest when {fn} x = −1; B1 greatest {a + b}, least {num(a - b)}')


@t51.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t51_calc(r, D):
    if D <= 2:
        a, b = r.randint(-5, 8), r.randint(2, 7)
        fn = r.choice(['sin', 'cos'])
        sgn_ = r.choice(['+', '−'])
        stem = f'The function f is defined by f(x) = {a} {sgn_} {b} {fn} x for 0 ≤ x ≤ 2π. State the range of f' + (' and the value of x at which f has its greatest value.' if D == 2 else '.')
        mx = {('sin', '+'): 'π/2', ('sin', '−'): '3π/2', ('cos', '+'): '0 and 2π', ('cos', '−'): 'π'}[(fn, sgn_)]
        return Q(stem, f'{num(a - b)} ≤ f(x) ≤ {num(a + b)}' + (f'; x = {mx}' if D == 2 else ''), f'B1 {num(a - b)}; B1 {num(a + b)}' + (f'; B1 x = {mx}' if D == 2 else ''))
    if D == 3:
        a, b, c = r.randint(1, 6), r.randint(2, 6), r.randint(-4, 5)
        fn = r.choice(['sin', 'cos'])
        return Q(f'For the curve y = {a} {fn} {b}x{sg(c) if c else ""}, where x is in degrees, state the amplitude, the period, and the greatest and least values of y.',
                 f'amplitude {a}; period {num(Fr(360, b))}°; greatest {num(c + a)}; least {num(c - a)}', f'B1 amplitude {a}; B1 period {num(Fr(360, b))}°; B1 greatest {num(c + a)} and least {num(c - a)}')
    if D == 4:
        a, b = r.randint(-4, 6), nz(r, -6, 6)
        x1, sv, s1 = r.choice([('π/6', 0.5, '1/2'), ('π/2', 1.0, '1'), ('5π/6', 0.5, '1/2'), ('3π/2', -1.0, '−1'), ('7π/6', -0.5, '−1/2')])
        x2, sv2 = ('π/2', 1.0) if x1 != 'π/2' else ('3π/2', -1.0)
        v1, v2 = a + b * sv, a + b * sv2
        return Q(f'The function f is defined by f(x) = a + b sin x for 0 ≤ x ≤ 2π. Given that f({x1}) = {num(v1)} and f({x2}) = {num(v2)}, find the values of the constants a and b.',
                 f'a = {num(a)}, b = {num(b)}', f'B1 sin {x1} = {s1}; M1 forms a + ({s1})b = {num(v1)} and a + ({num(int(sv2))})b = {num(v2)}; M1 solves; A1 a = {num(a)}, b = {num(b)}')
    a, b = r.randint(0, 6), r.randint(2, 6)
    k = r.choice([a - b, a + b, a, a - b + 1, a + b - 1])
    nsol = len(sols('cos', (a - k) / b if b else 0, 1, 0, 0, 360))
    return Q(f'The function f is defined by f(x) = {a} − {b} cos x for 0° ≤ x ≤ 360°. State the number of solutions of the equation f(x) = {num(k)}, justifying your answer.',
             str(nsol), f'M1 cos x = {num(Fr(a - k, b))}; M1 considers graph of y = cos x on 0° ≤ x ≤ 360°; A1 {nsol} solution{"s" if nsol != 1 else ""}')


def t51_c4(r, D):
    a, b = r.randint(1, 6), r.randint(2, 6)
    intro = f'The function f is defined by f(x) = {a} − {b} cos x for 0 ≤ x ≤ 2π.'
    parts = [
        P('State the range of f.', f'{num(a - b)} ≤ f(x) ≤ {num(a + b)}', f'B1 {num(a - b)}; B1 {num(a + b)}'),
        P('Write down the coordinates of the maximum point of the graph of y = f(x).', f'(π, {a + b})', f'B1 (π, {a + b})'),
        P(f'Solve the equation f(x) = {a}, giving exact answers.', 'x = π/2, 3π/2', 'M1 cos x = 0; A1 π/2, 3π/2'),
        P(f'Solve the equation f(x) = {num(Fr(2 * a - b, 2))}, giving exact answers.', 'x = π/3, 5π/3', 'M1 cos x = 1/2; A1 π/3; A1 5π/3'),
        P(f'Find the set of values of k for which the equation f(x) = k has exactly two solutions.', f'{num(a - b)} < k < {num(a + b)}', f'B1 {num(a - b)} < k < {num(a + b)} (ends give one solution each)'),
        P('Describe a sequence of transformations that maps y = cos x onto y = f(x).', f'Stretch parallel to the y-axis, factor {b}; reflection in the x-axis; translation (0, {a}).',
          f'B1 stretch factor {b} and reflection (or stretch factor −{b}); B1 translation (0, {a}) after'),
    ]
    return cmp_(r, intro, parts)


t51.add('C4', (2, 3, 4, 5))(t51_c4)


# ---------------------------------------------------------------- 5.2 inverse trig
ASIN = [('−1', Fr(-1, 2)), ('−√3/2', Fr(-1, 3)), ('−√2/2', Fr(-1, 4)), ('−1/2', Fr(-1, 6)), ('0', Fr(0)), ('1/2', Fr(1, 6)), ('√2/2', Fr(1, 4)), ('√3/2', Fr(1, 3)), ('1', Fr(1, 2))]
ATAN = [('−√3', Fr(-1, 3)), ('−1', Fr(-1, 4)), ('−1/√3', Fr(-1, 6)), ('0', Fr(0)), ('1/√3', Fr(1, 6)), ('1', Fr(1, 4)), ('√3', Fr(1, 3))]


def inv_val(fn, r):
    if fn == 'sin⁻¹':
        s, f = r.choice(ASIN)
        return s, f
    if fn == 'cos⁻¹':
        s, f = r.choice(ASIN)
        return s, Fr(1, 2) - f
    s, f = r.choice(ATAN)
    return s, f


t52 = T('Inverse trigonometric functions and their principal values', 'inverse trigonometric functions', 'principal values')
t52.fixed('C1', (1, 2), [
    ('What is the range of principal values of sin⁻¹ x?', '−π/2 ≤ sin⁻¹ x ≤ π/2', 'sin x is one-one on −π/2 ≤ x ≤ π/2.', ['0 ≤ sin⁻¹ x ≤ π', '−π < sin⁻¹ x < π', '0 ≤ sin⁻¹ x ≤ 2π']),
    ('What is the range of principal values of cos⁻¹ x?', '0 ≤ cos⁻¹ x ≤ π', 'cos x is one-one on 0 ≤ x ≤ π.', ['−π/2 ≤ cos⁻¹ x ≤ π/2', '−π ≤ cos⁻¹ x ≤ 0', '0 ≤ cos⁻¹ x ≤ 2π']),
    ('What is the range of principal values of tan⁻¹ x?', '−π/2 < tan⁻¹ x < π/2', 'tan x is one-one on −π/2 < x < π/2 (end points excluded).', ['−π/2 ≤ tan⁻¹ x ≤ π/2', '0 < tan⁻¹ x < π', '0 ≤ tan⁻¹ x ≤ 2π']),
    ('What is the domain of cos⁻¹ x?', '−1 ≤ x ≤ 1', 'The input of cos⁻¹ is a value of cosine.', ['0 ≤ x ≤ π', 'x ∈ ℝ', '−π/2 ≤ x ≤ π/2']),
    ('What is the domain of tan⁻¹ x?', 'x ∈ ℝ', 'tan takes every real value on −π/2 < x < π/2.', ['−1 ≤ x ≤ 1', 'x ≥ 0', '−π/2 < x < π/2']),
])
t52.fixed('C2', (2, 3), [
    ('Explain why the domain of sin x must be restricted before an inverse function sin⁻¹ x can be defined.', 'sin x is many-one on ℝ (e.g. sin 0 = sin π), so it has no inverse; on −π/2 ≤ x ≤ π/2 it is one-one, taking each value in [−1, 1] once.', 'B1 sin is many-one; B1 restricted interval where one-one [2]'),
    ('Explain why cos⁻¹(−x) = π − cos⁻¹ x for −1 ≤ x ≤ 1.', 'If cos⁻¹ x = θ then cos(π − θ) = −cos θ = −x, and π − θ lies in [0, π], so it is the principal value of cos⁻¹(−x).', 'B1 cos(π − θ) = −cos θ; B1 π − θ in principal range [2]'),
    ('Explain why sin⁻¹(sin 2π/3) is not equal to 2π/3.', 'sin⁻¹ gives a value in [−π/2, π/2]; sin 2π/3 = √3/2, and the principal value is π/3.', 'B1 principal range; B1 value π/3 [2]'),
])


@t52.add('C1', (1, 2, 3))
def t52_c1(r, D):
    fn = r.choice(['sin⁻¹', 'cos⁻¹', 'tan⁻¹'])
    s, f = inv_val(fn, r)
    c = pi_frac(f)
    ds = [pi_frac(-f) if f else 'π', pi_frac(f + 1) if fn != 'cos⁻¹' else pi_frac(f - 1), pi_frac(Fr(1, 2) - f) if Fr(1, 2) - f != f else pi_frac(f + Fr(1, 6)), pi_frac(2 * f) if f else 'π/2', pi_frac(f + Fr(1, 3))]
    return MC(r, f'Find the exact value of {fn}({s}).', c, ds, f'Principal value of {fn}: {c}.')


@t52.add('C2', (2, 3, 4), 'explain')
def t52_err(r, D):
    nm = person(r)
    s, f = r.choice(ASIN[1:4])
    if r.random() < 0.5:
        return Q(f'{nm} says that cos⁻¹({s}) = {pi_frac(-(Fr(1, 2) + f))}. Explain why this is not the principal value and give the correct value.',
                 f'Principal values of cos⁻¹ lie in [0, π], so the answer cannot be negative. cos⁻¹({s}) = {pi_frac(Fr(1, 2) - f)}.', f'B1 range 0 to π; B1 {pi_frac(Fr(1, 2) - f)}')
    return Q(f'{nm} says that sin⁻¹({s}) = {pi_frac(1 - f) if f > -Fr(1, 2) else pi_frac(Fr(3, 2))}, since the sine of this angle is {s}. Explain why this is not the principal value and give the correct value.',
             f'Principal values of sin⁻¹ lie in [−π/2, π/2]. sin⁻¹({s}) = {pi_frac(f)}.', f'B1 range −π/2 to π/2; B1 {pi_frac(f)}')


TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41)]


@t52.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t52_calc(r, D):
    if D <= 2:
        (s1, f1), (s2, f2) = r.sample(ASIN, 2)
        val = f1 + (Fr(1, 2) - f2)
        return Q(f'Find the exact value of sin⁻¹({s1}) + cos⁻¹({s2}).', pi_frac(val), f'B1 sin⁻¹({s1}) = {pi_frac(f1)}; B1 cos⁻¹({s2}) = {pi_frac(Fr(1, 2) - f2)}; B1 {pi_frac(val)}' if D == 2 else f'B1 both principal values; B1 {pi_frac(val)}')
    if D == 3:
        a, b, c = r.choice(TRIPLES)
        if r.random() < 0.5:
            return Q(f'Find the exact value of sin(cos⁻¹({a}/{c})).', f'{b}/{c}', f'M1 right-angled triangle with adjacent {a}, hypotenuse {c}; A1 opposite {b}; A1 {b}/{c}')
        return Q(f'Find the exact value of tan(sin⁻¹({a}/{c})).', f'{a}/{b}', f'M1 right-angled triangle with opposite {a}, hypotenuse {c}; A1 adjacent {b}; A1 {a}/{b}')
    a, b = r.randint(1, 5), r.randint(2, 5)
    if D == 4:
        stem = f'The function f is defined by f(x) = {a} + {b} sin x for −π/2 ≤ x ≤ π/2. Find an expression for f⁻¹(x) and state the domain of f⁻¹.'
        return Q(stem, f'f⁻¹(x) = sin⁻¹((x − {a})/{b}); domain {num(a - b)} ≤ x ≤ {num(a + b)}',
                 f'M1 sin x = (y − {a})/{b}; A1 f⁻¹(x) = sin⁻¹((x − {a})/{b}); B1 domain {num(a - b)} ≤ x ≤ {num(a + b)}')
    s, f = r.choice(ASIN[1:8])
    val = a + b * {'−1': -1, '−√3/2': -R3_ / 2, '−√2/2': -R2_ / 2, '−1/2': -0.5, '0': 0, '1/2': 0.5, '√2/2': R2_ / 2, '√3/2': R3_ / 2, '1': 1}[s]
    if s in ('−1/2', '0', '1/2'):
        vs = num(a + b * Fr({'−1/2': -1, '0': 0, '1/2': 1}[s], 2))
        return Q(f'The function f is defined by f(x) = {a} + {b} sin x for −π/2 ≤ x ≤ π/2. Find the exact value of f⁻¹({vs}).', pi_frac(f),
                 f'M1 sin x = ({vs} − {a})/{b} = {s}; A1 x = {pi_frac(f)} (in principal range)')
    return Q(f'The function f is defined by f(x) = {a} + {b} sin x for −π/2 ≤ x ≤ π/2. Find f⁻¹({n3(val)}), giving your answer to 3 significant figures.', n3(float(f) * math.pi),
             f'M1 sin x = ({n3(val)} − {a})/{b}; A1 x = {n3(float(f) * math.pi)}')


def t52_c4(r, D):
    a, b = r.randint(2, 6), r.randint(1, 4)
    intro = f'The function f is defined by f(x) = {a} − {b} cos x for 0 ≤ x ≤ π.'
    parts = [
        P('State the range of f.', f'{num(a - b)} ≤ f(x) ≤ {num(a + b)}', f'B1 {num(a - b)} ≤ f(x) ≤ {num(a + b)}'),
        P('Explain why f has an inverse.', 'cos x is decreasing on 0 ≤ x ≤ π, so −cos x is increasing and f is one-one.', 'B1 f is one-one (increasing) on the domain'),
        P('Find an expression for f⁻¹(x).', f'f⁻¹(x) = cos⁻¹(({a} − x)/{b})', f'M1 cos x = ({a} − y)/{b}; A1 f⁻¹(x) = cos⁻¹(({a} − x)/{b})'),
        P('State the domain of f⁻¹.', f'{num(a - b)} ≤ x ≤ {num(a + b)}', f'B1 {num(a - b)} ≤ x ≤ {num(a + b)}'),
        P(f'Find the exact value of f⁻¹({num(Fr(2 * a + b, 2))}).', '2π/3', f'M1 cos x = −1/2; A1 2π/3'),
        P(f'Solve the equation f(x) = {a}.', 'x = π/2', 'B1 cos x = 0 ⇒ x = π/2'),
    ]
    return cmp_(r, intro, parts)


t52.add('C4', (2, 3, 4, 5))(t52_c4)


# ---------------------------------------------------------------- 5.3 identities
t53 = T('Identities tan θ = sin θ / cos θ and sin²θ + cos²θ = 1', 'identities', 'sin²θ + cos²θ = 1', 'tan θ = sin θ / cos θ')
t53.fixed('C1', (1, 2), [
    ('Which expression is equal to 1 − cos²θ?', 'sin²θ', 'From sin²θ + cos²θ = 1.', ['cos²θ − 1', 'tan²θ', '1 + sin²θ']),
    ('Simplify sin θ / tan θ.', 'cos θ', 'sin θ ÷ (sin θ/cos θ) = cos θ.', ['sin²θ', '1/cos θ', 'tan θ']),
    ('Simplify (1 − sin²θ)/cos θ.', 'cos θ', '1 − sin²θ = cos²θ; cos²θ/cos θ = cos θ.', ['sin θ', '1/cos θ', 'tan θ']),
    ('Which is equal to tan θ cos θ?', 'sin θ', '(sin θ/cos θ) × cos θ = sin θ.', ['cos²θ', '1', 'sin θ/cos²θ']),
    ('Given that sin θ = 0.6 and θ is acute, cos θ =', '0.8', 'cos θ = √(1 − 0.36) = 0.8.', ['0.4', '0.64', '1.6']),
])
PROOFS = [
    ('Prove the identity (sin θ + cos θ)² + (sin θ − cos θ)² ≡ 2.', 'Expanding: 2sin²θ + 2cos²θ (cross terms cancel) = 2(sin²θ + cos²θ) = 2.', 'M1 expands both brackets; M1 cross terms cancel; A1 uses sin²θ + cos²θ = 1 [3]'),
    ('Prove the identity (1 − cos²θ)/(1 − sin²θ) ≡ tan²θ.', '(1 − cos²θ)/(1 − sin²θ) = sin²θ/cos²θ = tan²θ.', 'M1 numerator sin²θ; M1 denominator cos²θ; A1 tan²θ [3]'),
    ('Prove the identity tan θ + 1/tan θ ≡ 1/(sin θ cos θ).', 'sin θ/cos θ + cos θ/sin θ = (sin²θ + cos²θ)/(sin θ cos θ) = 1/(sin θ cos θ).', 'M1 writes in sin and cos; M1 common denominator; A1 uses identity [3]'),
    ('Prove the identity (1 + sin θ)(1 − sin θ) ≡ cos²θ.', '(1 + sin θ)(1 − sin θ) = 1 − sin²θ = cos²θ.', 'M1 difference of two squares; A1 1 − sin²θ = cos²θ [2]'),
    ('Prove the identity sin⁴θ − cos⁴θ ≡ sin²θ − cos²θ.', 'sin⁴θ − cos⁴θ = (sin²θ − cos²θ)(sin²θ + cos²θ) = sin²θ − cos²θ.', 'M1 difference of two squares; A1 uses sin²θ + cos²θ = 1 [2]'),
    ('Prove the identity cos θ/(1 − sin θ) − cos θ/(1 + sin θ) ≡ 2 tan θ.', 'Common denominator 1 − sin²θ = cos²θ; numerator cos θ(1 + sin θ) − cos θ(1 − sin θ) = 2 sin θ cos θ; result 2 sin θ cos θ/cos²θ = 2 tan θ.', 'M1 common denominator; M1 denominator cos²θ; A1 2 tan θ [3]'),
    ('Prove the identity (1 − sin θ)/cos θ ≡ cos θ/(1 + sin θ).', 'Cross-multiplying: (1 − sin θ)(1 + sin θ) = 1 − sin²θ = cos²θ = cos θ × cos θ, so the fractions are equal.', 'M1 multiplies numerator and denominator by (1 + sin θ) or cross-multiplies; A1 1 − sin²θ = cos²θ [2]'),
    ('Prove the identity (tan θ + 1)² ≡ 1/cos²θ + 2 tan θ.', '(tan θ + 1)² = tan²θ + 2 tan θ + 1 and tan²θ + 1 = (sin²θ + cos²θ)/cos²θ = 1/cos²θ.', 'M1 expands; M1 tan²θ + 1 = 1/cos²θ; A1 conclusion [3]'),
]
t53.fixed('C2', (2, 3, 4), PROOFS)


@t53.add('C1', (1, 2, 3))
def t53_c1(r, D):
    a, b, c = r.choice(TRIPLES)
    if r.random() < 0.5:
        a, b = b, a
    fn = r.choice(['cos', 'tan'])
    if fn == 'cos':
        return MC(r, f'Given that sin θ = {a}/{c} and θ is acute, find the exact value of cos θ.', f'{b}/{c}', [f'{a}/{b}', f'{b}/{a}', f'{c - a}/{c}', f'{MINUS}{b}/{c}'], f'cos θ = √(1 − {a * a}/{c * c}) = {b}/{c}.')
    if D == 3:
        return MC(r, f'Given that sin θ = {a}/{c} and θ is obtuse, find the exact value of tan θ.', f'{MINUS}{a}/{b}', [f'{a}/{b}', f'{MINUS}{b}/{a}', f'{MINUS}{a}/{c}', f'{b}/{a}'], f'cos θ = −{b}/{c} (obtuse), tan θ = sin θ/cos θ = −{a}/{b}.')
    return MC(r, f'Given that sin θ = {a}/{c} and θ is acute, find the exact value of tan θ.', f'{a}/{b}', [f'{b}/{a}', f'{a}/{c}', f'{b}/{c}', f'{MINUS}{a}/{b}'], f'cos θ = {b}/{c}, tan θ = sin θ/cos θ = {a}/{b}.')


def qt(A, B, C, fn='cos'):
    """'A cos²x + B cos x + C' with tidy signs."""
    out = ('' if A == 1 else (MINUS if A == -1 else num(A) + ' ')) + f'{fn}²x'
    if B:
        out += (' + ' if B > 0 else ' − ') + ('' if abs(B) == 1 else num(abs(B)) + ' ') + f'{fn} x'
    if C:
        out += sg(C)
    return out


def trig_quad(r):
    """Quadratic A c² + B c + C = 0 in c = cos x (or sin x) with one root in [−1, 1] (possibly two)."""
    roots = [Fr(1, 2), Fr(-1, 2), Fr(1, 3), Fr(2, 3), Fr(-1, 3), Fr(-2, 3), Fr(1, 4), Fr(3, 4), Fr(-1, 4), Fr(-3, 4), Fr(2, 5), Fr(-2, 5), Fr(1, 5), Fr(3, 5), Fr(-3, 5), Fr(1), Fr(-1)]
    bad = [Fr(2), Fr(-2), Fr(3), Fr(-3), Fr(3, 2), Fr(-3, 2), Fr(5, 2), Fr(-5, 2), Fr(4, 3), Fr(-4, 3), Fr(5, 3)]
    u = r.choice(roots)
    v = r.choice(bad) if r.random() < 0.6 else r.choice([x for x in roots if x != u])
    L = math.lcm(u.denominator, v.denominator)
    # (p c − q)(s c − t)
    p, q = u.denominator, u.numerator
    s_, t = v.denominator, v.numerator
    A, B, C = p * s_, -(p * t + q * s_), q * t
    return A, B, C, u, v


@t53.add('C2', (2, 3, 4), 'explain')
def t53_show(r, D):
    A, B, C, u, v = trig_quad(r)
    # A cos² + B cos + C = 0 ⇔ A(1 − sin²) + B cos + C = 0 ⇔ A sin²x = B cos x + (A + C)
    lhs = f'{num(A)} sin²x'
    rhs = tl(B, A + C)
    return Q(f'Show that the equation {lhs} = {rhs} can be written in the form {qt(A, B, C)} = 0.',
             f'Replace sin²x by 1 − cos²x: {num(A)} − {num(A)} cos²x = {rhs}, which rearranges to {qt(A, B, C)} = 0.',
             f'M1 uses sin²x = 1 − cos²x; A1 rearranges to the given form with correct signs')


@t53.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t53_calc(r, D):
    a, b, c = r.choice(TRIPLES)
    if r.random() < 0.5:
        a, b = b, a
    if D <= 2:
        return Q(f'Given that cos θ = {b}/{c} and 0° < θ < 90°, find the exact values of sin θ and tan θ.', f'sin θ = {a}/{c}; tan θ = {a}/{b}', f'M1 sin²θ = 1 − {b * b}/{c * c}; A1 sin θ = {a}/{c}; B1 tan θ = {a}/{b}')
    if D == 3:
        q = r.choice(['obtuse', 'reflex (180° < θ < 270°)', 'reflex (270° < θ < 360°)'])
        if q == 'obtuse':
            s_, co = f'{a}/{c}', f'{MINUS}{b}/{c}'
            given, find = f'sin θ = {a}/{c}', f'cos θ = {co}; tan θ = {MINUS}{a}/{b}'
        elif q.startswith('reflex (180'):
            given, find = f'tan θ = {a}/{b}', f'sin θ = {MINUS}{a}/{c}; cos θ = {MINUS}{b}/{c}'
        else:
            given, find = f'cos θ = {b}/{c}', f'sin θ = {MINUS}{a}/{c}; tan θ = {MINUS}{a}/{b}'
        return Q(f'Given that {given} and θ is {q}, find the exact values of the other two trigonometric ratios of θ.', find,
                 'M1 uses sin²θ + cos²θ = 1 (or a right-angled triangle); A1 correct magnitudes; A1 correct signs for the quadrant')
    if D == 4:
        k = r.choice([2, 3, 4, 5])
        # given tan θ = k, find (sinθ + cosθ)/(sinθ − cosθ) = (k + 1)/(k − 1)
        return Q(f'Given that tan θ = {k}, find the exact value of (sin θ + cos θ)/(sin θ − cos θ).', num(Fr(k + 1, k - 1)),
                 f'M1 divides numerator and denominator by cos θ; M1 (tan θ + 1)/(tan θ − 1); A1 {num(Fr(k + 1, k - 1))}')
    # D5: express a sin²θ + b cos²θ in terms of sin θ, then find range
    p, q = r.sample(range(1, 9), 2)
    lo, hi = min(p, q), max(p, q)
    return Q(f'Express {p} sin²θ + {q} cos²θ in the form a + b sin²θ, and hence find the greatest and least values of {p} sin²θ + {q} cos²θ.', f'{q} + {num(p - q)} sin²θ'.replace('+ −', '− ') + f'; greatest {hi}, least {lo}',
             f'M1 cos²θ = 1 − sin²θ; A1 {q} + ({num(p - q)})sin²θ; M1 uses 0 ≤ sin²θ ≤ 1; A1 greatest {hi}, least {lo}')


def t53_c4(r, D):
    A, B, C, u, v = trig_quad(r)
    lhs = f'{num(A)} sin²x'
    rhs = tl(B, A + C)
    xs = sorted(set(sols('cos', float(u))) | set(sols('cos', float(v)) if abs(v) <= 1 else set()))
    intro = f'The equation {lhs} = {rhs} is to be solved for 0° ≤ x ≤ 360°.'
    parts = [
        P('Show that the equation can be written as a quadratic equation in cos x.', f'{qt(A, B, C)} = 0', 'M1 sin²x = 1 − cos²x; A1 correct quadratic'),
        P('Solve the equation for 0° ≤ x ≤ 360°.', dlist(xs), f'M1 factorises/solves the quadratic: cos x = {num(u)}' + (f' or {num(v)}' if abs(v) <= 1 else f' (cos x = {num(v)} rejected)') + f'; A1 one angle; A1 all angles {dlist(xs)}'),
        P('Prove the identity (1 − cos x)(1 + cos x) ≡ sin²x.', 'Expand: 1 − cos²x = sin²x.', 'B1 expands and uses the identity'),
        P('Explain why, in this equation, any value of cos x outside −1 ≤ cos x ≤ 1 is rejected.', 'The range of cos x is −1 to 1, so such values give no angles.', 'B1 range of cosine'),
    ]
    return cmp_(r, intro, parts)


t53.add('C4', (2, 3, 4, 5))(t53_c4)


# ---------------------------------------------------------------- 5.4 solving equations
t54 = T('Solving trigonometric equations in a given interval', 'solving trigonometric equations', 'given interval', 'trigonometric equations')
t54.fixed('C1', (1, 2), [
    ('How many solutions does sin x = 0.4 have for 0° ≤ x ≤ 360°?', '2', 'sin x is positive in the first and second quadrants.', ['1', '3', '4']),
    ('Solve tan x = 1 for 0° ≤ x ≤ 360°.', '45°, 225°', 'Principal value 45°; tan has period 180°.', ['45° only', '45°, 135°', '45°, 315°']),
    ('Solve cos x = −1 for 0° ≤ x ≤ 360°.', '180°', 'cos x = −1 only at x = 180° in this interval.', ['0°, 360°', '90°, 270°', '270°']),
    ('How many solutions does sin 2x = 0.5 have for 0° ≤ x ≤ 360°?', '4', '2x ranges over 0° to 720°: two solutions per 360°.', ['2', '1', '8']),
    ('Solve sin x = 1/2 for 0 ≤ x ≤ 2π.', 'π/6, 5π/6', 'Principal value π/6; second solution π − π/6.', ['π/6, 7π/6', 'π/3, 2π/3', 'π/6, 11π/6']),
])
t54.fixed('C2', (2, 3), [
    ('Explain why dividing both sides of sin x cos x = sin x by sin x can lose solutions.', 'Solutions with sin x = 0 (x = 0°, 180°, 360°) are lost; instead factorise: sin x(cos x − 1) = 0.', 'B1 sin x may be 0; B1 factorise instead [2]'),
    ('Explain why the equation 3 sin x = 4 cos x can be solved by finding tan x.', 'cos x = 0 does not give a solution (then sin x = ±1 ≠ 0), so dividing by cos x is safe: tan x = 4/3.', 'B1 cos x ≠ 0 at a solution; B1 tan x = 4/3 [2]'),
    ('Explain how the graph of y = cos x shows that cos x = k (−1 < k < 1) has two solutions in 0° ≤ x ≤ 360°.', 'The horizontal line y = k crosses one complete cycle of the cosine curve exactly twice, at x and 360° − x.', 'B1 line crosses curve twice; B1 symmetry x and 360° − x [2]'),
])


@t54.add('C1', (1, 2, 3))
def t54_c1(r, D):
    for _ in range(30):
        fn = r.choice(['sin', 'cos', 'tan'])
        a = r.choice([30, 45, 60, 120, 135, 150, 210, 225, 240, 300, 315, 330])
        v = trigv(fn, a)
        if v is not None and exstr(v):
            break
    else:
        return None
    xs = sols(fn, v)
    rad = D == 3
    show = (lambda L: ', '.join(pi_frac(Fr(round(x), 180)) for x in L)) if rad else (lambda L: ', '.join(f'{round(x)}°' for x in L))
    c = show(xs)
    wrong = [show(sols(fn, -v)), show(xs[:1]), show(sols('sin' if fn != 'sin' else 'cos', v)) if sols('sin' if fn != 'sin' else 'cos', v) else show([round(xs[0] + 90)]), show([round(x + 180) % 360 for x in xs])]
    rng = '0 ≤ x ≤ 2π' if rad else '0° ≤ x ≤ 360°'
    return MC(r, f'Solve {fn} x = {exstr(v)} for {rng}.', c, wrong, f'Principal value then use the symmetry of the {fn} graph: {c}.')


@t54.add('C2', (2, 3, 4), 'explain')
def t54_err(r, D):
    nm = person(r)
    fr = r.choice(['one', 'divide', 'cos'])
    if fr == 'one':
        k = r.choice([0.3, 0.45, 0.6, 0.72, 0.85, -0.25, -0.4, -0.65])
        fn = r.choice(['sin', 'cos'])
        xs = sols(fn, k)
        p = math.degrees(math.asin(k) if fn == 'sin' else math.acos(k))
        return Q(f'{nm} solves {fn} x = {k} for 0° ≤ x ≤ 360° and gives the single answer x = {d1(p)}. Explain why this is incomplete and give all the solutions.',
                 f'The calculator gives only the principal value; {fn} x = {k} has two solutions in a full cycle: {dlist(xs)}.', f'B1 more than one solution in 0° to 360° (symmetry of graph); B1 {dlist(xs)}')
    if fr == 'divide':
        k = r.choice([Fr(1, 2), Fr(-1, 2), Fr(1, 3), Fr(2, 3), Fr(-1, 4)])
        a = k.denominator
        b = k.numerator
        xs = sorted(set(sols('cos', float(k))) | {0.0, 180.0, 360.0})
        return Q(f'{nm} solves {a} sin x cos x = {"" if b == 1 else ("−" if b == -1 else num(b) + " ")}sin x for 0° ≤ x ≤ 360° by dividing both sides by sin x. Explain why {nm} may lose solutions, and give all the solutions.',
                 f'Dividing by sin x loses the solutions of sin x = 0. sin x({a} cos x − {num(b)}) = 0: sin x = 0 gives 0°, 180°, 360°; cos x = {num(k)} gives the rest. All: {dlist(xs)}.'.replace('− −', '+ '),
                 f'B1 sin x = 0 solutions lost; M1 factorises; A1 {dlist(xs)}')
    k = r.choice([0.3, 0.45, 0.6, 0.75, 0.2])
    xs = sols('cos', -k)
    return Q(f'{nm} solves cos x = −{k} for 0° ≤ x ≤ 360° and writes x = {d1(math.degrees(math.acos(-k)))} or x = {d1(-math.degrees(math.acos(-k)))}. Explain the error and correct it.',
             f'{d1(-math.degrees(math.acos(-k)))} is outside the interval; the second solution is 360° − {d1(math.degrees(math.acos(-k)))} = {d1(xs[1])}. Solutions {dlist(xs)}.',
             f'B1 negative angle outside interval; B1 {dlist(xs)}')


@t54.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t54_calc(r, D):
    if D == 1:
        fn = r.choice(['sin', 'cos', 'tan'])
        k = r.choice([0.2, 0.35, 0.55, 0.7, 0.8, 0.9, -0.3, -0.45, -0.6, -0.75]) if fn != 'tan' else r.choice([0.5, 1.5, 2, 2.5, 3, -0.8, -1.5, -2, -3.2])
        xs = sols(fn, k)
        return Q(f'Solve the equation {fn} x = {num(k)} for 0° ≤ x ≤ 360°.', dlist(xs), f'M1 principal value {d1(math.degrees({"sin": math.asin, "cos": math.acos, "tan": math.atan}[fn](k)))}; A1 {dlist(xs)}')
    if D == 2:
        fn = r.choice(['sin', 'cos'])
        a, b = r.randint(2, 5), r.randint(-4, 4)
        c = r.choice([x for x in range(-a + 1 + b, a + b) if x != b] or [b + 1])
        k = (c - b) / a
        xs = sols(fn, k, lo=0, hi=360)
        return Q(f'Solve the equation {a} {fn} x{sg(b) if b else ""} = {c} for 0° ≤ x ≤ 360°.', dlist(xs), f'M1 {fn} x = {num(Fr(c - b, a))}; A1 one value; A1 {dlist(xs)}')
    if D == 3:
        fn = r.choice(['sin', 'cos', 'tan'])
        b = r.choice([2, 3]) if fn != 'tan' else 2
        c = r.choice([0, 0, 20, 30, 45, -30, -15])
        k = r.choice([0.3, 0.5, 0.65, -0.4, -0.7]) if fn != 'tan' else r.choice([0.5, 1.2, 2, -1.5, -0.7])
        xs = sols(fn, k, b, c, 0, 180 if b == 3 else 360)
        hi = 180 if b == 3 else 360
        arg = f'{b}x' + (f' + {c}°' if c > 0 else (f' − {-c}°' if c < 0 else ''))
        return Q(f'Solve the equation {fn}({arg}) = {num(k)} for 0° ≤ x ≤ {hi}°.', dlist(xs),
                 f'M1 principal value for {arg}; M1 further values of {arg} in range {num(c)}° to {num(b * hi + c)}°; M1 converts to x; A1 {dlist(xs)}')
    if D == 4:
        A, B, C, u, v = trig_quad(r)
        fn = r.choice(['sin', 'cos'])
        xs = sorted(set(sols(fn, float(u))) | (set(sols(fn, float(v))) if abs(v) <= 1 else set()))
        quadtxt = qt(A, B, C, fn)
        return Q(f'Solve the equation {quadtxt} = 0 for 0° ≤ x ≤ 360°.', dlist(xs),
                 f'M1 factorises as a quadratic in {fn} x; A1 {fn} x = {num(u)}' + (f' or {num(v)}' if abs(v) <= 1 else f' ({num(v)} rejected)') + f'; A1 one angle; A1 {dlist(xs)}')
    # D5: a sin x = b cos x  -> tan x = b/a, in radians −π ≤ x ≤ π
    a, b = nz(r, -7, 7), nz(r, -7, 7)
    xs = sols('tan', b / a, 1, 0, -180, 180)
    return Q(f'Solve the equation {num(a)} sin x = {num(b)} cos x for −π ≤ x ≤ π, giving your answers in radians correct to 3 significant figures.'.replace('1 sin', 'sin').replace('1 cos', 'cos'),
             rlist(xs), f'M1 tan x = {num(Fr(b, a))}; A1 principal value {n3(math.atan(b / a))}; A1 {rlist(xs)}')


def t54_c4(r, D):
    A, B, C, u, v = trig_quad(r)
    # tan form: A tan² + B tan + C = 0  -> roots any value, both valid
    xs_t = sorted(set(sols('tan', float(u))) | set(sols('tan', float(v))))
    k = r.choice([2, 3, 4, 5])
    p = r.choice([0.3, 0.45, 0.6, 0.8])
    xs2 = sols('sin', p, 2, 0, 0, 360)
    intro = 'Solve each of the following equations for 0° ≤ x ≤ 360°, giving answers correct to 1 decimal place.' if r.random() < 0.5 else 'In this question all angles are in degrees with 0° ≤ x ≤ 360°.'
    quadtxt = qt(A, B, C, 'tan')
    parts = [
        P(f'Solve {quadtxt} = 0.', dlist(xs_t), f'M1 factorises: tan x = {num(u)} or {num(v)}; A1 two angles; A1 all angles {dlist(xs_t)}'),
        P(f'Solve {k} sin x = cos x.', dlist(sols('tan', 1 / k)), f'M1 tan x = 1/{k}; A1 {dlist(sols("tan", 1 / k))}'),
        P(f'Solve sin 2x = {p}.', dlist(xs2), f'M1 principal value of 2x; M1 values of 2x in 0° to 720°; A1 {dlist(xs2)}'),
        P(f'Solve sin x tan x = {num(Fr(3, 2))}, using sin²x = 1 − cos²x to form a quadratic in cos x.', dlist(sols('cos', 0.5)),
          'M1 sin²x = (3/2) cos x; M1 2cos²x + 3cos x − 2 = 0; A1 cos x = 1/2 (−2 rejected); A1 60.0°, 300.0°'),
    ]
    return cmp_(r, intro, parts)


t54.add('C4', (2, 3, 4, 5))(t54_c4)

CHAPTERS[5] = [t51, t52, t53, t54]


# ================================================================ Chapter 6 Series

def binom_str(a, b, n, v='x'):
    """(a + bx)^n as text."""
    inner = poly([(a, 0), (b, 1)], v) if a != 0 else poly([(b, 1)], v)
    return f'({inner}){sup(n)}'


def coef(a, b, n, k):
    return comb(n, k) * Fr(a) ** (n - k) * Fr(b) ** k


s61 = T('Binomial expansion of (a + b)ⁿ for positive integer n', 'binomial expansion', 'binomial theorem')
s61.fixed('C1', (1, 2), [
    ('How many terms are there in the expansion of (a + b)⁸?', '9', 'An expansion of (a + b)ⁿ has n + 1 terms.', ['8', '16', '7']),
    ('What is the value of ⁶C₂?', '15', '⁶C₂ = 6!/(2!4!) = 15.', ['12', '30', '6']),
    ('Which row of Pascal’s triangle gives the coefficients in (a + b)⁴?', '1 4 6 4 1', 'Row 4: 1, 4, 6, 4, 1.', ['1 3 3 1', '1 5 10 10 5 1', '1 4 4 1']),
    ('What is the coefficient of x in the expansion of (1 + x)⁷?', '7', '⁷C₁ = 7.', ['1', '21', '14']),
    ('In the expansion of (a + b)ⁿ the general term is', 'ⁿCᵣ aⁿ⁻ʳ bʳ', 'Choose r of the n brackets to supply b.', ['ⁿCᵣ aʳ bʳ', 'n aⁿ⁻ʳ bʳ', 'ⁿCᵣ aⁿ bʳ']),
])
s61.fixed('C2', (2, 3), [
    ('Explain why the coefficients in the expansion of (a + b)ⁿ are symmetrical, i.e. ⁿCᵣ = ⁿCₙ₋ᵣ.', 'Choosing r brackets to give b is the same as choosing the n − r brackets that give a, so the counts are equal.', 'B1 choosing r ↔ leaving n − r; B1 so equal [2]'),
    ('Explain why (x + 1/x)⁵ has no term independent of x.', 'The general term is ⁵Cᵣ x⁵⁻ʳ x⁻ʳ = ⁵Cᵣ x⁵⁻²ʳ; 5 − 2r = 0 needs r = 2.5, which is not an integer.', 'B1 power 5 − 2r; B1 r not an integer [2]'),
    ('Explain why the expansion of (1 − x)ⁿ has alternating signs.', 'The general term is ⁿCᵣ(−x)ʳ, and (−1)ʳ is positive for even r and negative for odd r.', 'B1 (−x)ʳ; B1 sign (−1)ʳ alternates [2]'),
])


@s61.add('C1', (1, 2, 3))
def s61_c1(r, D):
    n = r.randint(4, 8)
    a = 1 if D == 1 else r.randint(1, 3)
    b = nz(r, -4, 4)
    k = r.randint(2, 3)
    c = coef(a, b, n, k)
    return MC(r, f'Find the coefficient of x{sup(k)} in the expansion of {binom_str(a, b, n)}.', num(c),
              [num(comb(n, k) * a ** (n - k) * b), num(comb(n, k) * Fr(b) ** k), num(n * a ** (n - k) * Fr(b) ** k), num(-c), num(comb(n, k - 1) * a ** (n - k + 1) * Fr(b) ** (k - 1))],
              f'{n}C{k} × {a}{sup(n - k)} × ({num(b)}){sup(k)} = {num(c)}.')


@s61.add('C2', (2, 3, 4), 'explain')
def s61_err(r, D):
    nm = person(r)
    n, a, b = r.randint(4, 7), r.randint(2, 3), r.choice([2, 3, -2, -3, 5])
    k = 2
    right = coef(a, b, n, k)
    wrong = comb(n, k) * a ** (n - k) * b
    if r.random() < 0.5:
        return Q(f'{nm} finds the coefficient of x² in {binom_str(a, b, n)} as {comb(n, k)} × {a}{sup(n - k)} × ({num(b)}) = {num(wrong)}. Explain the error and find the correct coefficient.',
                 f'The term is {comb(n, 2)} × {a}{sup(n - 2)} × ({num(b)}x)², so {num(b)} must be squared: coefficient {num(right)}.', f'B1 ({num(b)}x)² so {num(b)} squared; B1 {num(right)}')
    m = r.randint(1, 4)
    # show that coefficient of x in (1 + m x)^n is n m and of x² is nC2 m²
    return Q(f'Show that the coefficient of x² in the expansion of (1 + {m}x){sup(n)} is {num(comb(n, 2) * m * m)}.'.replace('(1 + 1x)', '(1 + x)'),
             f'Term in x² is {n}C2 (1){sup(n - 2)} ({m}x)² = {comb(n, 2)} × {m * m} x² = {comb(n, 2) * m * m}x².'.replace('(1x)', '(x)').replace(' × 1 x²', ' x²'), f'M1 {n}C2 × ({m}x)²; A1 {comb(n, 2) * m * m} shown'.replace('(1x)', '(x)'))


@s61.add('C3', (1, 2, 3, 4, 5), 'numerical')
def s61_calc(r, D):
    n = r.randint(4, 8)
    a, b = r.randint(1, 3), nz(r, -4, 4)
    if D <= 2:
        t = [coef(a, b, n, k) for k in range(3)]
        return Q(f'Find the first three terms, in ascending powers of x, of the expansion of {binom_str(a, b, n)}.', poly([(t[0], 0), (t[1], 1), (t[2], 2)]),
                 f'B1 {num(t[0])}; B1 {num(t[1])}x; B1 {num(t[2])}x²')
    if D == 3:
        p, q = nz(r, -3, 4), nz(r, -5, 5)
        c2 = p * coef(a, b, n, 2) + q * coef(a, b, n, 1)
        return Q(f'Find the coefficient of x² in the expansion of ({poly([(p, 0), (q, 1)])}){binom_str(a, b, n)}.', num(c2),
                 f'B1 x coefficient of {binom_str(a, b, n)} = {num(coef(a, b, n, 1))}; B1 x² coefficient = {num(coef(a, b, n, 2))}; M1 {num(p)} × {num(coef(a, b, n, 2))} + {pn(q)} × {num(coef(a, b, n, 1))}; A1 {num(c2)}')
    if D == 4:
        n = r.choice([3, 6, 9]) if r.random() < 0.5 else r.choice([4, 8])
        k = nz(r, -3, 3)
        # (x² + k/x)^n : power 2(n−r) − r = 2n − 3r = 0 -> r = 2n/3
        if (2 * n) % 3:
            n = 6
        rr = 2 * n // 3
        val = comb(n, rr) * Fr(k) ** rr
        return Q(f'Find the term independent of x in the expansion of (x² {"+" if k > 0 else "−"} {abs(k)}/x){sup(n)}.', num(val),
                 f'M1 general term {n}Cr (x²){sup(n)}⁻ʳ ({num(k)}/x)ʳ; M1 2({n} − r) − r = 0 ⇒ r = {rr}; A1 {n}C{rr} × ({num(k)}){sup(rr)}; A1 {num(val)}')
    m = r.randint(2, 5)
    V = comb(n, 2) * m * m
    return Q(f'The coefficient of x² in the expansion of (1 + ax){sup(n)} is {V}. Find the possible values of a, and the corresponding coefficients of x.',
             f'a = ±{m}; coefficient of x = ±{n * m}', f'M1 {n}C2 a² = {V}; A1 a² = {m * m}; A1 a = ±{m}; B1 coefficient of x = {n}a = ±{n * m}')


def s61_c4(r, D):
    n = r.randint(5, 7)
    a, b = r.randint(2, 3), nz(r, -3, 3)
    p = nz(r, -4, 4)
    t = [coef(a, b, n, k) for k in range(4)]
    intro = f'Consider the expansion of {binom_str(a, b, n)}.'
    parts = [
        P('Find the first three terms in ascending powers of x.', poly([(t[0], 0), (t[1], 1), (t[2], 2)]), f'B1 {num(t[0])}; B1 {num(t[1])}x; B1 {num(t[2])}x²'),
        P('Find the coefficient of x³.', num(t[3]), f'M1 {n}C3 × {a}{sup(n - 3)} × ({num(b)})³; A1 {num(t[3])}'),
        P(f'Find the coefficient of x² in the expansion of (1{sg(p)}x){binom_str(a, b, n)}.'.replace(' + 1x', ' + x').replace(' − 1x', ' − x'), num(t[2] + p * t[1]),
          f'M1 {num(t[2])} + ({num(p)}) × {num(t[1])}; A1 {num(t[2] + p * t[1])}'),
        P('State the number of terms in the full expansion.', str(n + 1), f'B1 {n + 1}'),
    ]
    return cmp_(r, intro, parts)


s61.add('C4', (2, 3, 4, 5))(s61_c4)


# ---------------------------------------------------------------- 6.2 arithmetic progressions
s62 = T('Arithmetic progressions: nth term and sum', 'arithmetic progressions', 'nth term and sum')
s62.fixed('C1', (1, 2), [
    ('The nth term of an arithmetic progression with first term a and common difference d is', 'a + (n − 1)d', 'Each term adds d; the nth term has had n − 1 additions.', ['a + nd', 'a(n − 1)d', 'an + d']),
    ('What is the sum of the first n terms of an AP with first term a and last term l?', '½n(a + l)', 'Pair first and last terms: n/2 pairs each summing to a + l.', ['n(a + l)', '½(a + l)', '½n(a − l)']),
    ('The terms 7, 11, 15, … form an AP. What is the common difference?', '4', '11 − 7 = 4.', ['7', '11/7', '3']),
    ('What is the sum of the integers from 1 to 100?', '5050', '½ × 100 × (1 + 100) = 5050.', ['5000', '10100', '4950']),
])
s62.fixed('C2', (2, 3), [
    ('Explain why the sum of the first n terms of an AP is ½n(2a + (n − 1)d).', 'Write the sum forwards and backwards and add: each of the n pairs sums to 2a + (n − 1)d, so 2Sₙ = n(2a + (n − 1)d).', 'B1 forwards/backwards pairing; B1 each pair 2a + (n − 1)d [2]'),
    ('Explain how to show that three numbers form an arithmetic progression.', 'Show that the difference between the second and first equals the difference between the third and second (equivalently the middle term is the mean of the other two).', 'B1 equal differences; B1 or middle = mean [2]'),
])


@s62.add('C1', (1, 2, 3))
def s62_c1(r, D):
    a, d, n = r.randint(-10, 20), nz(r, -7, 9), r.randint(8, 40)
    if D < 3:
        u = a + (n - 1) * d
        return MC(r, f'An arithmetic progression has first term {a} and common difference {d}. Find the {ordn(n)} term.', num(u), [num(a + n * d), num(a * n + d), num(n * d), num(a + (n - 2) * d)],
                  f'a + (n − 1)d = {a} + {n - 1} × {num(d)} = {num(u)}.')
    S = Fr(n, 2) * (2 * a + (n - 1) * d)
    return MC(r, f'An arithmetic progression has first term {a} and common difference {d}. Find the sum of the first {n} terms.', num(S),
              [num(n * (2 * a + (n - 1) * d)), num(Fr(n, 2) * (2 * a + n * d)), num(Fr(n, 2) * (a + (n - 1) * d)), num(a + (n - 1) * d)], f'Sₙ = ½n(2a + (n − 1)d) = {num(S)}.')


@s62.add('C2', (2, 3, 4), 'explain')
def s62_err(r, D):
    nm = person(r)
    a, d, n = r.randint(2, 15), r.randint(2, 9), r.randint(10, 30)
    if r.random() < 0.5:
        return Q(f'An AP has first term {a} and common difference {d}. {nm} says the {ordn(n)} term is {a} + {n} × {d} = {a + n * d}. Explain the error and find the correct {ordn(n)} term.',
                 f'The first term already counts as term 1, so only {n - 1} differences are added: {a} + {n - 1} × {d} = {a + (n - 1) * d}.', f'B1 (n − 1)d not nd; B1 {a + (n - 1) * d}')
    k = r.randint(2, 6)
    x = r.randint(2, 9)
    t1, t2, t3 = x, x + k * 2, x + k * 4
    return Q(f'Show that {t1}, {t2}, {t3} are consecutive terms of an arithmetic progression and find the next term.',
             f'{t2} − {t1} = {t3} − {t2} = {2 * k}, so the differences are equal; next term {t3 + 2 * k}.', f'B1 both differences {2 * k} with conclusion; B1 {t3 + 2 * k}')


@s62.add('C3', (1, 2, 3, 4, 5), 'numerical')
def s62_calc(r, D):
    a, d = r.randint(-12, 25), nz(r, -6, 8)
    if D == 1:
        n = r.randint(10, 50)
        return Q(f'Find the sum of the first {n} terms of the arithmetic progression {a}, {a + d}, {a + 2 * d}, ….', num(Fr(n, 2) * (2 * a + (n - 1) * d)), f'M1 ½ × {n} × (2 × {a} + {n - 1} × {num(d)}); A1 {num(Fr(n, 2) * (2 * a + (n - 1) * d))}')
    if D == 2:
        n = r.randint(10, 40)
        l = a + (n - 1) * d
        return Q(f'An arithmetic progression has first term {a} and last term {l}. There are {n} terms. Find the common difference and the sum of the progression.', f'd = {num(d)}; sum = {num(Fr(n, 2) * (a + l))}',
                 f'M1 {a} + {n - 1}d = {l}; A1 d = {num(d)}; B1 sum ½ × {n} × ({num(a)}{sg(l)}) = {num(Fr(n, 2) * (a + l))}')
    if D == 3:
        p, q = r.sample(range(2, 15), 2)
        up, uq = a + (p - 1) * d, a + (q - 1) * d
        n = r.randint(15, 40)
        return Q(f'The {ordn(p)} term of an arithmetic progression is {up} and the {ordn(q)} term is {uq}. Find the first term, the common difference and the sum of the first {n} terms.',
                 f'a = {a}, d = {num(d)}, S = {num(Fr(n, 2) * (2 * a + (n - 1) * d))}', f'M1 a + {p - 1}d = {up}, a + {q - 1}d = {uq}; A1 d = {num(d)}; A1 a = {a}; M1 sum formula; A1 {num(Fr(n, 2) * (2 * a + (n - 1) * d))}')
    if D == 4:
        a, d = r.randint(1, 15), r.randint(2, 6)
        n = r.randint(8, 30)
        S = n * (2 * a + (n - 1) * d) // 2 if (n * (2 * a + (n - 1) * d)) % 2 == 0 else None
        if S is None:
            return None
        other = Fr(-(2 * a - d) * 1, d) - n  # other root of d n² + (2a − d) n − 2S = 0
        return Q(f'An arithmetic progression has first term {a} and common difference {d}. The sum of the first n terms is {S}. Find the value of n.', f'n = {n}',
                 f'M1 ½n(2 × {a} + (n − 1) × {d}) = {S}; M1 {poly([(d, 2), (2 * a - d, 1), (-2 * S, 0)], 'n')} = 0; A1 n = {n} (negative root rejected)')
    k = r.choice([3, 4, 6, 7, 8, 9, 11, 12, 13])
    lo, hi = r.randint(10, 99), r.randint(200, 999)
    first = (lo // k + 1) * k
    last = (hi // k) * k
    if last == hi:
        last -= k
    n = (last - first) // k + 1
    S = n * (first + last) // 2
    return Q(f'Find the sum of all the integers between {lo} and {hi} that are multiples of {k}.', str(S),
             f'B1 first {first}, last {last}; M1 n = {n}; M1 ½ × {n} × ({first} + {last}); A1 {S}')


def s62_c4(r, D):
    nm = person(r)
    a, d = r.choice([2, 3, 4, 5]), r.choice([0.5, 0.25, 1, 0.75])
    n = r.choice([8, 10, 12, 15, 20])
    km = a + (n - 1) * d
    S = n / 2 * (2 * a + (n - 1) * d)
    target = r.choice([60, 80, 100, 150, 200])
    m = 1
    while m / 2 * (2 * a + (m - 1) * d) < target:
        m += 1
    intro = f'{nm} trains for a race in {city(r)}. On day 1 {nm} runs {num(a)} km, and each day runs {num(d)} km more than the day before.'
    parts = [
        P(f'Find the distance run on day {n}.', f'{num(km)} km', f'M1 {num(a)} + {n - 1} × {num(d)}; A1 {num(km)} km'),
        P(f'Find the total distance run in the first {n} days.', f'{num(S)} km', f'M1 ½ × {n} × (2 × {num(a)} + {n - 1} × {num(d)}); A1 {num(S)} km'),
        P(f'Find the first day on which the total distance run exceeds {target} km.', f'day {m}', f'M1 ½n(2 × {num(a)} + (n − 1){num(d)}) > {target}; M1 solves / trials; A1 day {m}'),
        P(f'Find the first day on which {nm} runs at least {num(km + 2 * d)} km.', f'day {n + 2}', f'M1 {num(a)} + (n − 1) × {num(d)} ≥ {num(km + 2 * d)}; A1 day {n + 2}'),
    ]
    return cmp_(r, intro, parts)


s62.add('C4', (2, 3, 4, 5))(s62_c4)


# ---------------------------------------------------------------- 6.3 geometric progressions
s63 = T('Geometric progressions: nth term and sum', 'geometric progressions', 'nth term and sum')
s63.fixed('C1', (1, 2), [
    ('The nth term of a geometric progression with first term a and common ratio r is', 'arⁿ⁻¹', 'Each term multiplies by r; the nth term has n − 1 multiplications.', ['arⁿ', 'a + (n − 1)r', '(ar)ⁿ⁻¹']),
    ('What is the common ratio of the GP 48, −24, 12, …?', '−1/2', '−24 ÷ 48 = −1/2.', ['1/2', '−24', '−2']),
    ('The sum of the first n terms of a GP with r ≠ 1 is', 'a(1 − rⁿ)/(1 − r)', 'Standard result from multiplying the sum by r and subtracting.', ['a(1 − rⁿ)/(1 + r)', 'a(rⁿ − 1)/r', 'n/2 (a + l)']),
    ('Which sequence is a geometric progression?', '5, 15, 45, 135', 'Each term is 3 times the previous one.', ['5, 10, 15, 20', '5, 15, 25, 35', '1, 4, 9, 16']),
])
s63.fixed('C2', (2, 3), [
    ('Explain why the formula Sₙ = a(1 − rⁿ)/(1 − r) cannot be used when r = 1, and state Sₙ in that case.', 'The denominator 1 − r would be 0. With r = 1 every term equals a, so Sₙ = na.', 'B1 division by zero; B1 Sₙ = na [2]'),
    ('Explain how to show that three non-zero numbers form a geometric progression.', 'Show that the ratio of the second to the first equals the ratio of the third to the second (equivalently the middle term squared equals the product of the other two).', 'B1 equal ratios; B1 or b² = ac [2]'),
])


@s63.add('C1', (1, 2, 3))
def s63_c1(r, D):
    a = r.choice([2, 3, 4, 5, 6, 8, 10, 12, 16, 24, 48, 81, 64, 96])
    rr = r.choice([2, 3, -2, Fr(1, 2), Fr(-1, 2), Fr(3, 2), Fr(2, 3), -3])
    n = r.randint(4, 8)
    u = a * rr ** (n - 1)
    if D < 3:
        return MC(r, f'A geometric progression has first term {a} and common ratio {num(rr)}. Find the {ordn(n)} term.', num(u), [num(a * rr ** n), num(a * rr ** (n - 2)), num((a * rr) ** (n - 1)), num(-u)],
                  f'arⁿ⁻¹ = {a} × ({num(rr)}){sup(n - 1)} = {num(u)}.')
    S = a * (1 - rr ** n) / (1 - rr)
    return MC(r, f'A geometric progression has first term {a} and common ratio {num(rr)}. Find the sum of the first {n} terms.', num(S),
              [num(a * (1 - rr ** (n - 1)) / (1 - rr)), num(a * (1 - rr ** n) / (1 + rr)) if rr != -1 else '0', num(u), num(S + a)], f'Sₙ = a(1 − rⁿ)/(1 − r) = {num(S)}.')


@s63.add('C2', (2, 3, 4), 'explain')
def s63_err(r, D):
    nm = person(r)
    a, rr = r.choice([2, 3, 4, 5, 6]), r.choice([2, 3, 4])
    t = [a * rr ** i for i in range(4)]
    if r.random() < 0.5:
        return Q(f'For the sequence {t[0]}, {t[1]}, {t[2]}, {t[3]}, … {nm} says the common ratio is {t[1] - t[0]}. Explain the error and state the correct common ratio.',
                 f'{nm} found a difference; the ratio is found by dividing consecutive terms: {t[1]} ÷ {t[0]} = {rr}.', f'B1 ratio = division, not subtraction; B1 r = {rr}')
    x = r.randint(2, 8)
    k = r.randint(2, 4)
    # x, x k, x k² : show b² = ac
    return Q(f'Show that {x}, {x * k}, {x * k * k} are consecutive terms of a geometric progression and find the next term.', f'{x * k}/{x} = {x * k * k}/{x * k} = {k}; next term {x * k ** 3}.',
             f'B1 equal ratios {k} (or {x * k}² = {x} × {x * k * k}); B1 {x * k ** 3}')


@s63.add('C3', (1, 2, 3, 4, 5), 'numerical')
def s63_calc(r, D):
    if D <= 2:
        a, rr, n = r.choice([3, 5, 6, 7, 10, 12]), r.choice([2, 3, Fr(1, 2), -2, Fr(1, 3)]), r.randint(5, 10)
        S = a * (1 - Fr(rr) ** n) / (1 - rr)
        return Q(f'Find the sum of the first {n} terms of the geometric progression {a}, {num(a * rr)}, {num(a * rr * rr)}, ….', num(S),
                 f'B1 r = {num(rr)}; M1 {a}(1 − ({num(rr)}){sup(n)})/(1 − {num(rr)}); A1 {num(S)}'.replace('− −', '+ '))
    if D == 3:
        a, rr = r.choice([2, 3, 4, 5, 6, 8]), r.choice([2, 3, -2, -3, Fr(1, 2), Fr(-1, 2)])
        u2, u5 = a * rr, a * rr ** 4
        n = r.randint(6, 9)
        return Q(f'The second term of a geometric progression is {num(u2)} and the fifth term is {num(u5)}. Find the common ratio, the first term and the sum of the first {n} terms.',
                 f'r = {num(rr)}, a = {a}, S = {num(a * (1 - Fr(rr) ** n) / (1 - rr))}', f'M1 r³ = {num(u5)} ÷ {num(u2)}; A1 r = {num(rr)}; A1 a = {a}; M1 sum formula; A1 {num(a * (1 - Fr(rr) ** n) / (1 - rr))}')
    if D == 4:
        P0 = r.choice([12000, 15000, 18000, 25000, 30000])
        pc = r.choice([4, 5, 8, 10, 12, 15])
        n = r.randint(5, 10)
        up = r.choice([True, False])
        f = 1 + pc / 100 if up else 1 - pc / 100
        what = 'salary increases' if up else 'value of a car decreases'
        val = P0 * f ** (n - 1)
        tot = P0 * (1 - f ** n) / (1 - f)
        if up:
            return Q(f'{person(r)} starts a job in {city(r)} with an annual salary of ${P0:,}. The salary increases by {pc}% each year. Find the salary in year {n} and the total earned over the first {n} years.',
                     f'${n3(val)}; ${n3(tot)}', f'B1 r = {f:.2f}; M1 {P0} × {f:.2f}{sup(n - 1)}; A1 ${n3(val)}; M1 {P0}(1 − {f:.2f}{sup(n)})/(1 − {f:.2f}) or ({f:.2f}{sup(n)} − 1)/({f:.2f} − 1) form; A1 ${n3(tot)}')
        return Q(f'A car bought in {city(r)} for ${P0:,} loses {pc}% of its value each year. Find its value after {n} years.', f'${n3(P0 * f ** n)}',
                 f'B1 r = {f:.2f}; M1 {P0} × {f:.2f}{sup(n)}; A1 ${n3(P0 * f ** n)}')
    # D5: AP/GP link: a, a + d, a + 3d are in GP (classic): (a + d)² = a(a + 3d) -> d = a
    a = r.randint(2, 9)
    d = a
    n = r.randint(10, 20)
    return Q(f'The first, second and fourth terms of an arithmetic progression with first term {a} and non-zero common difference d are the first three terms of a geometric progression. Find d, the common ratio of the geometric progression, and the sum of the first {n} terms of the arithmetic progression.',
             f'd = {d}; r = 2; S = {n * (2 * a + (n - 1) * d) // 2}', f'M1 ({a} + d)² = {a}({a} + 3d); A1 d² = {a}d ⇒ d = {d}; B1 r = {2 * a}/{a} = 2; M1 AP sum formula; A1 {n * (2 * a + (n - 1) * d) // 2}')


def s63_c4(r, D):
    a = r.choice([4, 5, 6, 8, 9, 10])
    rr = r.choice([Fr(3, 2), Fr(4, 3), Fr(5, 4), 2])
    n = r.randint(5, 8)
    intro = f'A bacteria culture in a laboratory in {city(r)} has a mass of {a} mg at the end of the first hour. The mass at the end of each hour is {num(rr)} times the mass at the end of the previous hour.'
    u = a * rr ** (n - 1)
    parts = [
        P(f'Find the mass at the end of hour {n}, correct to 3 significant figures.', f'{n3(float(u))} mg', f'M1 {a} × ({num(rr)}){sup(n - 1)}; A1 {n3(float(u))} mg'),
        P(f'Find the sum of the masses recorded at the end of the first {n} hours, correct to 3 significant figures.', f'{n3(float(a * (rr ** n - 1) / (rr - 1)))} mg',
          f'M1 {a}(({num(rr)}){sup(n)} − 1)/({num(rr)} − 1); A1 {n3(float(a * (rr ** n - 1) / (rr - 1)))} mg'),
        P('Explain why a sum to infinity does not exist for this progression.', f'The common ratio {num(rr)} > 1, so the terms grow without limit.', 'B1 |r| > 1 so the series diverges'),
        P(f'Find the first hour at which the mass exceeds {a * 10} mg.', f'hour {next(k for k in range(1, 60) if a * rr ** (k - 1) > a * 10)}',
          f'M1 {a}({num(rr)})ⁿ⁻¹ > {a * 10}; A1 hour {next(k for k in range(1, 60) if a * rr ** (k - 1) > a * 10)}'),
    ]
    return cmp_(r, intro, parts)


s63.add('C4', (2, 3, 4, 5))(s63_c4)


# ---------------------------------------------------------------- 6.4 sum to infinity
s64 = T('Sum to infinity of a convergent geometric progression', 'sum to infinity', 'convergent geometric progression')
s64.fixed('C1', (1, 2), [
    ('A geometric progression has a sum to infinity only if', '|r| < 1', 'rⁿ → 0 only when −1 < r < 1.', ['r > 1', 'r < 0', '|r| > 1']),
    ('What is the sum to infinity of 1 + 1/2 + 1/4 + 1/8 + …?', '2', 'a/(1 − r) = 1/(1/2) = 2.', ['1', '3/2', 'infinite']),
    ('The sum to infinity of a GP with first term a and common ratio r is', 'a/(1 − r)', 'Sₙ = a(1 − rⁿ)/(1 − r) and rⁿ → 0.', ['a/(1 + r)', 'a/(r − 1)', 'ar/(1 − r)']),
    ('Which geometric progression has a sum to infinity?', '9, −3, 1, …', 'r = −1/3, and |r| < 1.', ['1, 2, 4, …', '5, −5, 5, …', '2, 3, 4.5, …']),
])
s64.fixed('C2', (2, 3), [
    ('Explain why the sum to infinity of a GP with |r| < 1 is a/(1 − r).', 'Sₙ = a(1 − rⁿ)/(1 − r); as n → ∞, rⁿ → 0 when |r| < 1, so Sₙ → a/(1 − r).', 'B1 rⁿ → 0; B1 limit a/(1 − r) [2]'),
    ('Explain why the series 3 + 3 + 3 + … has no sum to infinity even though each term is finite.', 'r = 1, so Sₙ = 3n, which increases without limit; the formula needs |r| < 1.', 'B1 Sₙ = 3n unbounded; B1 r = 1 not < 1 [2]'),
])


@s64.add('C1', (1, 2, 3))
def s64_c1(r, D):
    a = r.choice([3, 4, 6, 8, 9, 12, 15, 20, 24, 30, 36, 45, 60])
    rr = r.choice([Fr(1, 2), Fr(1, 3), Fr(2, 3), Fr(-1, 2), Fr(-1, 3), Fr(3, 4), Fr(1, 4), Fr(-2, 3), Fr(2, 5), Fr(-1, 4)])
    S = a / (1 - rr)
    return MC(r, f'Find the sum to infinity of the geometric progression with first term {a} and common ratio {num(rr)}.', num(S),
              [num(a / (1 + rr)), num(a * rr / (1 - rr)), num(a / rr) if rr else '0', num(S * 2)], f'S∞ = a/(1 − r) = {a}/(1 − ({num(rr)})) = {num(S)}.')


@s64.add('C2', (2, 3, 4), 'explain')
def s64_err(r, D):
    nm = person(r)
    a, rr = r.choice([2, 3, 4, 5, 8]), r.choice([Fr(3, 2), 2, Fr(5, 4), Fr(-3, 2)])
    return Q(f'{nm} finds the sum to infinity of the geometric progression {a}, {num(a * rr)}, {num(a * rr * rr)}, … as {a}/(1 − {num(rr)}) = {num(a / (1 - rr))}. Explain why this is wrong.'.replace('− −', '+ '),
             f'The common ratio is {num(rr)}, and |r| ≥ 1, so the terms do not tend to zero and the series has no sum to infinity; the formula only applies for |r| < 1.',
             f'B1 r = {num(rr)} with |r| > 1; B1 series diverges so no sum to infinity')


@s64.add('C3', (1, 2, 3, 4, 5), 'numerical')
def s64_calc(r, D):
    if D <= 2:
        a = r.choice([5, 6, 8, 10, 12, 18, 20, 27, 36, 40])
        rr = r.choice([Fr(1, 2), Fr(1, 3), Fr(2, 3), Fr(-1, 2), Fr(3, 4), Fr(-1, 3), Fr(1, 5)])
        return Q(f'Find the sum to infinity of the geometric progression {a}, {num(a * rr)}, {num(a * rr * rr)}, ….', num(a / (1 - rr)), f'B1 r = {num(rr)}; M1 {a}/(1 − ({num(rr)})); A1 {num(a / (1 - rr))}')
    if D == 3:
        rr = r.choice([Fr(1, 2), Fr(1, 3), Fr(2, 3), Fr(3, 4), Fr(1, 4), Fr(2, 5), Fr(3, 5), Fr(-1, 2), Fr(-1, 3)])
        a = r.choice([4, 6, 8, 9, 12, 15, 16, 20])
        S = a / (1 - rr)
        return Q(f'A geometric progression has first term {a} and sum to infinity {num(S)}. Find the common ratio and the third term.', f'r = {num(rr)}; third term {num(a * rr * rr)}',
                 f'M1 {a}/(1 − r) = {num(S)}; A1 r = {num(rr)}; B1 third term {num(a * rr * rr)}')
    if D == 4:
        k = r.choice([2, 3, 4, 5, 6])
        rr = Fr(k - 1, k)
        return Q(f'The sum to infinity of a geometric progression is {k} times its first term. Find the common ratio, and find the sum of the first 3 terms as a fraction of the first term a.',
                 f'r = {num(rr)}; S₃ = {num(1 + rr + rr * rr)}a', f'M1 a/(1 − r) = {k}a; A1 r = {num(rr)}; M1 a(1 + r + r²); A1 {num(1 + rr + rr * rr)}a')
    d2_ = r.randint(10, 98)
    if d2_ % 11 == 0:
        d2_ += 1
    return Q(f'By writing the recurring decimal 0.{d2_:02d}{d2_:02d}{d2_:02d}… as a geometric series, express it as a fraction in its simplest form.', num(Fr(d2_, 99)),
             f'B1 a = {d2_}/100; B1 r = 1/100; M1 a/(1 − r) = {d2_}/99; A1 {num(Fr(d2_, 99))}')


def s64_c4(r, D):
    h = r.choice([2, 3, 4, 5, 6, 8])
    rr = r.choice([Fr(1, 2), Fr(2, 3), Fr(3, 4), Fr(3, 5), Fr(4, 5)])
    nm = person(r)
    intro = f'{nm} drops a ball from a height of {h} m onto a hard floor. After each bounce it rises to {num(rr)} of the height from which it last fell.'
    tot = h + 2 * h * rr / (1 - rr)
    k = 4
    parts = [
        P('Find the height reached after the third bounce.', f'{num(h * rr ** 3)} m', f'M1 {h} × ({num(rr)})³; A1 {num(h * rr ** 3)} m'),
        P('Find the total distance travelled by the ball before it comes to rest, assuming it bounces indefinitely.', f'{num(tot)} m', f'B1 down {h} m first; M1 2 × ({num(h * rr)})/(1 − {num(rr)}); A1 {num(tot)} m'),
        P(f'Find the total distance travelled by the ball when it hits the floor for the {["", "first", "second", "third", "fourth", "fifth"][k]} time.', f'{n3(float(h + 2 * h * rr * (1 - rr ** (k - 1)) / (1 - rr)))} m',
          f'M1 {h} + 2 × ({num(h * rr)})(1 − ({num(rr)})³)/(1 − {num(rr)}); A1 {n3(float(h + 2 * h * rr * (1 - rr ** (k - 1)) / (1 - rr)))} m'),
        P('State one reason why the model of indefinite bouncing is unrealistic.', 'The ball eventually stops after a finite number of bounces (energy lost to sound/heat; very small bounces not possible).', 'B1 valid reason'),
    ]
    return cmp_(r, intro, parts)


s64.add('C4', (2, 3, 4, 5))(s64_c4)

CHAPTERS[6] = [s61, s62, s63, s64]


# ================================================================ Chapter 7 Differentiation

def disp_term(c, n, first):
    """Display a single term c·xⁿ in exam style (√x, 1/x², …)."""
    c, n = Fr(c), Fr(n)
    sgn_ = (MINUS if c < 0 else '') if first else (' − ' if c < 0 else ' + ')
    a = abs(c)
    if n == 0:
        return sgn_ + num(a)
    if n > 0 and n.denominator == 1:
        return sgn_ + (('' if a == 1 else (f'({num(a)})' if a.denominator != 1 else num(a))) + pw(n))
    if n == Fr(1, 2):
        return sgn_ + ('' if a == 1 else (f'({num(a)})' if a.denominator != 1 else num(a))) + '√x'
    if n < 0 and n.denominator == 1 and a.denominator == 1:
        return sgn_ + f'{num(a)}/{pw(-n)}'
    if n == Fr(-1, 2) and a.denominator == 1:
        return sgn_ + f'{num(a)}/√x'
    if n.denominator == 2 and n > 0 and a.denominator == 1:
        k = n - Fr(1, 2)
        return sgn_ + ('' if a == 1 else num(a)) + pw(k) + '√x'
    return sgn_ + ('' if a == 1 else f'({num(a)})' if a.denominator != 1 else num(a)) + f'x^({num(n)})'


def disp(terms):
    out = ''
    for c, n in terms:
        if c == 0:
            continue
        out += disp_term(c, n, not out)
    return out or '0'


def idx(terms):
    """Index form, e.g. 3x² − 2x⁻² + (1/2)x^(−1/2)."""
    out = ''
    for c, n in terms:
        if c == 0:
            continue
        out += term(c, n, 'x', first=not out)
    return out or '0'


def deriv(terms):
    return [(Fr(c) * Fr(n), Fr(n) - 1) for c, n in terms if Fr(n) != 0 and c != 0]


def ev(terms, x):
    """Exact value where possible (integer powers, or half-integer powers at perfect squares)."""
    tot = Fr(0)
    for c, n in terms:
        n = Fr(n)
        if n.denominator == 1:
            tot += Fr(c) * Fr(x) ** int(n)
        elif n.denominator == 2 and x >= 0 and math.isqrt(int(x)) ** 2 == x:
            tot += Fr(c) * Fr(math.isqrt(int(x))) ** int(2 * n)
        else:
            return evf(terms, x)
    return tot


def evf(terms, x):
    return sum(float(c) * float(x) ** float(n) for c, n in terms)


def rpoly(r, deg=3, lo=-6, hi=6):
    return [(nz(r, lo, hi) if k == deg else r.randint(lo, hi), k) for k in range(deg, -1, -1)]


POWS = [Fr(-2), Fr(-1), Fr(1, 2), Fr(-1, 2), Fr(3, 2), Fr(3), Fr(4), Fr(2), Fr(-3), Fr(5, 2)]


def rterms(r, k=3):
    ps = r.sample(POWS, k)
    out = []
    for p in sorted(ps, reverse=True):
        c = nz(r, -6, 8)
        if p.denominator == 2 and c % 2:
            c *= 2
        out.append((c, p))
    if r.random() < 0.5:
        out.append((nz(r, -9, 9), 0))
    return out


def nice_x(terms, xs=(1, 4, 9, 16)):
    return [x for x in xs]


d71 = T('Gradient of a curve as a limit and derivative notation', 'gradient of a curve as a limit', 'derivative notation')
d71.fixed('C1', (1, 2), [
    ('The derivative dy/dx represents', 'the gradient of the tangent to the curve', 'dy/dx is the limit of chord gradients: the gradient of the curve at a point.', ['the area under the curve', 'the y-intercept', 'the gradient of a chord between two fixed points']),
    ('For y = x², the gradient of the chord from (3, 9) to (3 + h, (3 + h)²) is', '6 + h', '((3 + h)² − 9)/h = (6h + h²)/h = 6 + h.', ['6', '6h + h²', '9 + h']),
    ('As h → 0, the gradient 6 + h approaches', '6', 'The h term vanishes in the limit.', ['0', '6 + h', 'infinity']),
    ('Which notation is used for the derivative of f(x)?', 'f′(x)', 'f′(x) (read "f dash x") is the derivative.', ['f⁻¹(x)', 'f(x)²', '∫ f(x) dx']),
])
d71.fixed('C2', (2, 3), [
    ('Explain why the gradient of a curve at a point is defined as the limit of the gradients of chords.', 'A curve has no single gradient between two points; as the second point moves towards the first, the chord approaches the tangent, so the limit of the chord gradients is the gradient at the point.', 'B1 chord approaches tangent; B1 limit as h → 0 [2]'),
    ('Explain the difference between dy/dx and δy/δx.', 'δy/δx is the gradient of a chord for small finite changes δx and δy; dy/dx is the limit of δy/δx as δx → 0, the gradient of the tangent.', 'B1 δy/δx chord gradient; B1 dy/dx limit / tangent [2]'),
])


@d71.add('C1', (1, 2, 3))
def d71_c1(r, D):
    a, b = r.randint(-5, 6), r.randint(-6, 6)
    h = r.choice([0.1, 0.01, 0.5, 0.2, 0.001])
    # y = x² + bx, chord from x = a to a + h: 2a + h + b
    g = 2 * a + h + b
    return MC(r, f'For the curve y = {quad(1, b, 0)}, find the gradient of the chord joining the points with x-coordinates {a} and {num(a + h)}.', num(round(g, 6)),
              [num(round(2 * a + b, 6)), num(round(2 * a + 2 * h + b, 6)), num(round(g + 1, 6)), num(round((2 * a + h + b) * h, 6))], f'Gradient = (y₂ − y₁)/h = 2({a}) + {h}{sg(b) if b else ""} = {num(round(g, 6))}.')


@d71.add('C2', (2, 3, 4), 'explain')
def d71_show(r, D):
    a, b, c = r.randint(1, 4), r.randint(-6, 6), r.randint(-5, 5)
    x0 = r.randint(-3, 4)
    g = 2 * a * x0 + b
    return Q(f'The curve y = {quad(a, b, c)} passes through P where x = {x0}. Show that the gradient of the chord from P to the point where x = {x0} + h is {num(g)} + {a}h, and deduce the gradient of the curve at P.'.replace('+ 1h', '+ h'),
             f'[f({x0} + h) − f({x0})]/h = ({num(g)}h + {a}h²)/h = {num(g)} + {a}h; as h → 0 the gradient is {num(g)}.'.replace('+ 1h', '+ h'),
             f'M1 expands f({x0} + h) − f({x0}) = {num(g)}h + {a}h²; A1 divides by h; A1 limit {num(g)}'.replace('+ 1h', '+ h'))


@d71.add('C3', (1, 2, 3, 4, 5), 'numerical')
def d71_calc(r, D):
    a, b = r.randint(1, 4), r.randint(-6, 6)
    x0 = r.randint(-3, 5)
    hs = [0.1, 0.01, 0.001][: (2 if D <= 2 else 3)]
    f = lambda x: a * x * x + b * x
    vals = [(f(x0 + h) - f(x0)) / h for h in hs]
    stem = f'For the curve y = {quad(a, b, 0)}, calculate the gradients of the chords from the point where x = {x0} to the points where x = ' + ', '.join(num(round(x0 + h, 4)) for h in hs) + '. Hence suggest the gradient of the curve at x = ' + str(x0) + '.'
    return Q(stem, '; '.join(num(round(v, 6)) for v in vals) + f'; gradient {2 * a * x0 + b}',
             'M1 uses (y₂ − y₁)/(x₂ − x₁); ' + '; '.join(f'A1 {num(round(v, 6))}' for v in vals) + f'; B1 suggests {2 * a * x0 + b}')


def d71_c4(r, D):
    x0 = r.randint(1, 4)
    intro = f'P is the point ({x0}, {x0 ** 3}) on the curve y = x³, and Q is the point on the curve with x-coordinate {x0} + h.'
    parts = [
        P('Show that the gradient of the chord PQ is ' + f'{3 * x0 * x0} + {3 * x0}h + h².', 'Shown', f'M1 ({x0} + h)³ − {x0 ** 3} = {3 * x0 * x0}h + {3 * x0}h² + h³; A1 ÷ h'),
        P('Deduce the gradient of the curve at P.', str(3 * x0 * x0), f'B1 h → 0 gives {3 * x0 * x0}'),
        P('Find the gradient of the chord PQ when h = 0.1.', num(round(3 * x0 * x0 + 0.3 * x0 + 0.01, 4)), f'B1 {num(round(3 * x0 * x0 + 0.3 * x0 + 0.01, 4))}'),
        P('State the derivative of x³ and check it agrees with your gradient at P.', f'3x²; 3 × {x0}² = {3 * x0 * x0}', 'B1 3x² and agreement'),
    ]
    return cmp_(r, intro, parts)


d71.add('C4', (2, 3, 4, 5))(d71_c4)


# ---------------------------------------------------------------- 7.2 differentiating xⁿ
d72 = T('Differentiating xⁿ for rational n, sums and constant multiples', 'differentiating xⁿ', 'rational n', 'sums and constant multiples')
d72.fixed('C1', (1, 2), [
    ('What is the derivative of 1/x?', '−1/x²', '1/x = x⁻¹, derivative −x⁻².', ['1/x²', 'ln x', '−1/x']),
    ('What is the derivative of √x?', '1/(2√x)', 'x^(1/2) differentiates to (1/2)x^(−1/2).', ['2√x', '(1/2)√x', '√x/2x²']),
    ('What is the derivative of a constant?', '0', 'A constant has zero gradient.', ['1', 'the constant', 'x']),
    ('Differentiate 5x⁴.', '20x³', 'n x ⁿ⁻¹: 5 × 4x³.', ['5x³', '20x⁴', '4x³']),
    ('What is dy/dx when y = x^(3/2)?', '(3/2)x^(1/2)', 'Multiply by the power and reduce it by 1.', ['(2/3)x^(5/2)', 'x^(1/2)', '(3/2)x^(5/2)']),
])
d72.fixed('C2', (2, 3), [
    ('Explain why the derivative of 7 is 0 but the derivative of 7x is 7.', 'y = 7 is a horizontal line with zero gradient; y = 7x is a straight line with gradient 7 everywhere.', 'B1 constant: horizontal line, gradient 0; B1 7x: line gradient 7 [2]'),
    ('Explain why an expression such as (x² + 1)/√x must be rewritten before differentiating term by term.', 'The rules apply to sums of powers of x; dividing each term by x^(1/2) gives x^(3/2) + x^(−1/2), which can then be differentiated. Differentiating top and bottom separately is not valid.', 'B1 rewrite as sum of powers; B1 cannot differentiate numerator and denominator separately [2]'),
])


@d72.add('C1', (1, 2, 3))
def d72_c1(r, D):
    c = nz(r, -9, 9)
    n = r.choice([Fr(3), Fr(4), Fr(5), Fr(-1), Fr(-2), Fr(-3), Fr(1, 2), Fr(3, 2), Fr(-1, 2), Fr(5, 2), Fr(1, 3), Fr(2, 3)])
    if n.denominator == 2 and c % 2:
        c *= 2
    t = [(c, n)]
    right = idx(deriv(t))
    ds = [idx([(c, n - 1)]), idx([(c * n, n + 1)]), idx([(c * n, n)]), idx([(c * (n - 1), n - 1)]), idx([(-c * n, n - 1)])]
    return MC(r, f'Differentiate {disp(t)} with respect to x.', right, ds, f'd/dx(xⁿ) = nxⁿ⁻¹: {right}.')


@d72.add('C2', (2, 3, 4), 'explain')
def d72_err(r, D):
    nm = person(r)
    fr = r.choice(['recip', 'quot', 'const'])
    if fr == 'recip':
        c, k = nz(r, 2, 9), r.randint(2, 4)
        return Q(f'{nm} differentiates y = {c}/x{sup(k)} and writes dy/dx = {c}/({k}x{sup(k - 1)}). Explain the error and find dy/dx correctly.'.replace('x¹)', 'x)'),
                 f'{nm} differentiated the denominator separately. Write y = {idx([(c, -k)])}; then dy/dx = {idx([(-c * k, -k - 1)])} = −{c * k}/x{sup(k + 1)}.',
                 f'B1 rewrite as {idx([(c, -k)])}; B1 dy/dx = {idx([(-c * k, -k - 1)])}')
    if fr == 'quot':
        a, b = nz(r, 2, 6), nz(r, -9, 9)
        # (a x² + b)/x = a x + b/x -> a − b/x²
        return Q(f'{nm} differentiates y = ({quad(a, 0, b)})/x by differentiating the top and bottom separately to get {2 * a}x/1 = {2 * a}x. Explain why this is wrong and find dy/dx correctly.',
                 f'There is no such rule for a quotient. y = {a}x{sg(b)}/x = {idx([(a, 1), (b, -1)])}, so dy/dx = {idx([(a, 0), (-b, -2)])}.',
                 f'B1 must divide through first; B1 dy/dx = {idx([(a, 0), (-b, -2)])}')
    a, b, c = nz(r, 2, 6), nz(r, -9, 9), nz(r, -9, 9)
    return Q(f'{nm} says that the curves y = {quad(a, b, c)} and y = {quad(a, b, c + r.choice([3, 5, 7]))} have the same gradient at every value of x. Is {nm} right? Explain.',
             f'Yes: the curves differ only by a constant, whose derivative is 0, so both have dy/dx = {lin(2 * a, b)}.', f'B1 derivative of constant is 0; B1 both {lin(2 * a, b)}')


@d72.add('C3', (1, 2, 3, 4, 5), 'numerical')
def d72_calc(r, D):
    if D == 1:
        t = rpoly(r, 3)
        return Q(f'Find dy/dx when y = {disp(t)}.', idx(deriv(t)), f'B1 B1 correct terms of {idx(deriv(t))}'.replace('B1 B1', 'B2'))
    if D == 2:
        t = rterms(r, 2)
        return Q(f'Find dy/dx when y = {disp(t)}.', idx(deriv(t)), 'M1 writes terms as powers of x; A1 ' + idx(deriv(t)))
    if D == 3:
        t = rterms(r, 3)
        x0 = r.choice([1, 4, 9]) if any(Fr(n).denominator == 2 for _, n in t) else r.choice([1, 2, -1, -2])
        g = ev(deriv(t), x0)
        gv = num(g) if isinstance(g, Fr) else n3(g)
        return Q(f'Find the gradient of the curve y = {disp(t)} at the point where x = {x0}.', gv, f'M1 powers of x; A1 dy/dx = {idx(deriv(t))}; A1 {gv}')
    if D == 4:
        a, b, c = nz(r, -4, 5), r.randint(-6, 6), nz(r, -8, 8)
        # (a x² + b x + c)/√x = a x^(3/2) + b x^(1/2) + c x^(−1/2)
        t = [(a, Fr(3, 2)), (b, Fr(1, 2)), (c, Fr(-1, 2))]
        top = quad(a, b, c)
        return Q(f'Given that y = ({top})/√x, find dy/dx.', idx(deriv(t)), f'M1 divides each term by x^(1/2): {idx(t)}; A1 at least two terms correct; A1 {idx(deriv(t))}')
    # D5: points where gradient equals k on cubic
    p, q = r.sample(range(-4, 5), 2)
    a = r.choice([1, 2])
    # dy/dx = 3a(x − p)(x − q) + k  -> y = a x³ − (3a/2)(p+q) x² + 3a p q x + k x
    k = r.randint(-6, 6)
    if (3 * a * (p + q)) % 2:
        a = 2
    t = [(a, 3), (Fr(-3 * a * (p + q), 2), 2), (3 * a * p * q + k, 1), (r.randint(-5, 5), 0)]
    if any(Fr(c).denominator != 1 for c, _ in t):
        return None
    pts = sorted([(x, ev(t, x)) for x in (p, q)])
    return Q(f'Find the coordinates of the points on the curve y = {disp(t)} at which the gradient is {k}.', ' and '.join(pt(*z) for z in pts),
             f'B1 dy/dx = {idx(deriv(t))}; M1 sets = {k} and solves quadratic; A1 x = {num(min(p, q))}, {num(max(p, q))}; A1 both points')


def d72_c4(r, D):
    a = r.choice([2, 4, 6, 8])
    b = r.choice([1, 2, 3, 4, 6])
    t = [(a, Fr(1, 2)), (b, -1)]
    x0 = r.choice([1, 4, 9])
    g = evf(deriv(t), x0)
    intro = f'A curve has equation y = {disp(t)}, for x > 0.'
    gfr = Fr(a, 2) * Fr(1, math.isqrt(x0)) - Fr(b, x0 * x0)
    parts = [
        P('Find dy/dx.', idx(deriv(t)), f'B1 {idx([deriv(t)[0]])}; B1 {idx([deriv(t)[1]])}'),
        P(f'Find the gradient of the curve at the point where x = {x0}.', num(gfr), f'M1 substitutes x = {x0}; A1 {num(gfr)}'),
        P('Find d²y/dx².', idx(deriv(deriv(t))), f'B1 FT {idx(deriv(deriv(t)))}'),
        P(f'Determine whether y is increasing or decreasing at x = {x0}.', 'increasing' if gfr > 0 else 'decreasing', f'B1 gradient {num(gfr)} {"> 0 so increasing" if gfr > 0 else "< 0 so decreasing"}'),
    ]
    return cmp_(r, intro, parts)


d72.add('C4', (2, 3, 4, 5))(d72_c4)


# ---------------------------------------------------------------- 7.3 chain rule
d73 = T('The chain rule', 'chain rule', 'composite function differentiation')
d73.fixed('C1', (1, 2), [
    ('Differentiate (2x + 1)⁵.', '10(2x + 1)⁴', '5(2x + 1)⁴ × 2.', ['5(2x + 1)⁴', '10(2x + 1)⁵', '(2x + 1)⁴']),
    ('Differentiate √(4x − 3).', '2/√(4x − 3)', '(1/2)(4x − 3)^(−1/2) × 4.', ['1/(2√(4x − 3))', '4√(4x − 3)', '2√(4x − 3)']),
    ('The chain rule states that if y is a function of u and u is a function of x then dy/dx =', '(dy/du) × (du/dx)', 'Multiply the rates of change.', ['(dy/du) ÷ (du/dx)', '(dy/du) + (du/dx)', '(du/dy) × (du/dx)']),
    ('Differentiate 1/(3x + 2).', '−3/(3x + 2)²', '(3x + 2)⁻¹ → −(3x + 2)⁻² × 3.', ['3/(3x + 2)²', '−1/(3x + 2)²', '−3/(3x + 2)']),
])
d73.fixed('C2', (2, 3), [
    ('Explain why the derivative of (5x − 2)³ is not 3(5x − 2)².', 'The inner function 5x − 2 changes 5 times as fast as x, so by the chain rule the result must be multiplied by 5: 15(5x − 2)².', 'B1 inner derivative 5; B1 15(5x − 2)² [2]'),
    ('Explain how the chain rule can be used to differentiate (x² + 1)⁴ without expanding the bracket.', 'Let u = x² + 1 so y = u⁴; dy/du = 4u³ and du/dx = 2x, so dy/dx = 8x(x² + 1)³.', 'B1 substitution u; B1 product of derivatives [2]'),
])


def chain_d(a, b, n, k=1):
    """d/dx of k(ax + b)^n -> (coef, power) of (ax + b)."""
    return k * n * a, n - 1


def bstr(a, b):
    return f'({lin(a, b)})'


def cpow(k, a, b, n):
    """k(ax + b)^n displayed."""
    k, n = Fr(k), Fr(n)
    base = bstr(a, b)
    ks = '' if k == 1 else (MINUS if k == -1 else (f'({num(k)})' if k.denominator != 1 else num(k)))
    if n == 1:
        return f'{ks}{base}'
    if n.denominator == 1:
        return f'{ks}{base}{sup(int(n))}'
    return f'{ks}{base}^({num(n)})'


def cdisp(k, a, b, n):
    """Exam-style display: k/(ax + b)^m for negative n; k√(ax + b) for 1/2."""
    k, n = Fr(k), Fr(n)
    if n == Fr(1, 2):
        return ('' if k == 1 else num(k)) + f'√({lin(a, b)})'
    if n == Fr(-1, 2) and k.denominator == 1:
        return f'{num(k)}/√({lin(a, b)})'
    if n < 0 and n.denominator == 1 and k.denominator == 1:
        return f'{num(k)}/{bstr(a, b)}' + (sup(int(-n)) if n != -1 else '')
    return cpow(k, a, b, n)


@d73.add('C1', (1, 2, 3))
def d73_c1(r, D):
    a, b = nz(r, -5, 6), nz(r, -9, 9)
    n = r.choice([Fr(3), Fr(4), Fr(5), Fr(6), Fr(-1), Fr(-2), Fr(1, 2), Fr(-1, 2), Fr(3, 2)])
    k = nz(r, -4, 5)
    if n.denominator == 2 and (k * a) % 2:
        k *= 2
    c, m = chain_d(a, b, n, k)
    right = cpow(c, a, b, m)
    ds = [cpow(k * n, a, b, m), cpow(c, a, b, n), cpow(c * a, a, b, m) if a != 1 else cpow(c + 1, a, b, m), cpow(k * a, a, b, m) if k * a != c else cpow(-c, a, b, m), cpow(c, a, b, m - 1)]
    return MC(r, f'Differentiate {cdisp(k, a, b, n)} with respect to x.', right, ds, f'Chain rule: {num(k)} × {num(n)} × {cpow(1, a, b, n - 1)} × {a} = {right}.')


@d73.add('C2', (2, 3, 4), 'explain')
def d73_err(r, D):
    nm = person(r)
    a, b = nz(r, 2, 7), nz(r, -9, 9)
    n = r.choice([3, 4, 5, 6, -2, -3])
    right = cpow(n * a, a, b, n - 1)
    wrong = cpow(n, a, b, n - 1)
    return Q(f'{nm} differentiates y = {cdisp(1, a, b, n)} and obtains dy/dx = {wrong}. Explain the error and give the correct derivative.',
             f'{nm} forgot to multiply by the derivative of the inner function {lin(a, b)}, which is {a}. Correct: {right}.', f'B1 must multiply by d/dx({lin(a, b)}) = {a}; B1 {right}')


@d73.add('C3', (1, 2, 3, 4, 5), 'numerical')
def d73_calc(r, D):
    if D <= 2:
        a, b = nz(r, -5, 6), nz(r, -9, 9)
        n = r.choice([3, 4, 5, -1, -2])
        k = nz(r, -4, 5)
        c, m = chain_d(a, b, n, k)
        return Q(f'Find dy/dx when y = {cdisp(k, a, b, n)}.', cpow(c, a, b, m), f'M1 {cpow(k * n, a, b, m)} (power reduced); A1 × {a}: {cpow(c, a, b, m)}')
    if D == 3:
        a, s = r.randint(1, 4), r.randint(1, 5)
        x0 = r.randint(0, 4)
        b = s * s - a * x0
        k = r.choice([2, 4, 6, 8])
        # y = k√(ax + b): dy/dx = k a /(2√(ax+b)) at x0 = k a /(2 s)
        g = Fr(k * a, 2 * s)
        return Q(f'Find the gradient of the curve y = {cdisp(k, a, b, Fr(1, 2))} at the point where x = {x0}.', num(g),
                 f'M1 {num(Fr(k, 2))}({lin(a, b)})^(−1/2) × {a}; A1 dy/dx = {num(Fr(k * a, 2))}/√({lin(a, b)}); A1 {num(g)}')
    if D == 4:
        a, b = nz(r, 1, 4), r.randint(-5, 5)
        k = nz(r, 2, 12)
        x0 = r.randint(-2, 3)
        u = a * x0 + b
        if u == 0:
            return None
        g = Fr(-2 * k * a, u ** 3)
        return Q(f'A curve has equation y = {cdisp(k, a, b, -2)}. Find the gradient of the curve at the point where x = {x0}, and determine whether y is increasing or decreasing there.',
                 f'{num(g)}; {"increasing" if g > 0 else "decreasing"}', f'M1 {num(-2 * k)}{bstr(a, b)}⁻³ × {a}; A1 dy/dx = {cpow(-2 * k * a, a, b, -3)}; A1 {num(g)}; B1 {"increasing" if g > 0 else "decreasing"}')
    # D5: d²y/dx² of (ax+b)^n
    a, b = nz(r, 2, 5), nz(r, -6, 6)
    n = r.choice([4, 5, Fr(3, 2), -1])
    c1, m1 = chain_d(a, b, n)
    c2, m2 = chain_d(a, b, m1, c1)
    return Q(f'Given that y = {cdisp(1, a, b, n)}, find dy/dx and d²y/dx².', f'dy/dx = {cpow(c1, a, b, m1)}; d²y/dx² = {cpow(c2, a, b, m2)}',
             f'M1 chain rule; A1 {cpow(c1, a, b, m1)}; M1 differentiates again; A1 {cpow(c2, a, b, m2)}')


def d73_c4(r, D):
    a, s = r.randint(1, 4), r.randint(2, 5)
    x0 = r.randint(0, 3)
    b = s * s - a * x0
    k = r.choice([2, 4, 6])
    intro = f'A curve has equation y = {cdisp(k, a, b, Fr(1, 2))}.'
    g = Fr(k * a, 2 * s)
    y0 = k * s
    m = -1 / g
    parts = [
        P('Find dy/dx.', f'{num(Fr(k * a, 2))}/√({lin(a, b)})', f'M1 chain rule; A1 {num(Fr(k * a, 2))}/√({lin(a, b)})'),
        P(f'Find the gradient of the curve at the point P where x = {x0}.', num(g), f'B1 {num(g)}'),
        P(f'Find the equation of the tangent to the curve at the point P where x = {x0}.', line_eq(g, y0 - g * x0), f'B1 y = {y0}; M1 y − {y0} = {num(g)}(x − {x0}); A1 {line_eq(g, y0 - g * x0)}'),
        P(f'Find the equation of the normal to the curve at the point P where x = {x0}, in the form ax + by + c = 0.', gen_line(m, -1, y0 - m * x0), f'M1 gradient {num(m)}; A1 {gen_line(m, -1, y0 - m * x0)}'),
        P('Explain why the curve has no stationary points.', f'dy/dx = {num(Fr(k * a, 2))}/√({lin(a, b)}) is never 0 (the numerator is a non-zero constant).', 'B1 numerator non-zero so dy/dx ≠ 0'),
    ]
    return cmp_(r, intro, parts)


d73.add('C4', (2, 3, 4, 5))(d73_c4)


# ---------------------------------------------------------------- 7.4 tangents and normals
d74 = T('Tangents and normals to curves', 'tangents and normals', 'tangent', 'normal')
d74.fixed('C1', (1, 2), [
    ('The gradient of the tangent to y = x² at (3, 9) is', '6', 'dy/dx = 2x = 6.', ['9', '3', '1/6']),
    ('If the gradient of the tangent at a point is 4, the gradient of the normal is', '−1/4', 'Normal is perpendicular: m₁m₂ = −1.', ['4', '−4', '1/4']),
    ('A normal to a curve at a point P is', 'the line through P perpendicular to the tangent', 'Definition of the normal.', ['the line through P parallel to the tangent', 'the tangent at P', 'the line joining P to the origin']),
    ('The tangent to a curve at a stationary point is', 'horizontal', 'The gradient is zero.', ['vertical', 'the line y = x', 'undefined']),
])
d74.fixed('C2', (2, 3), [
    ('Explain how to find the equation of the normal to a curve at a given point.', 'Differentiate, substitute the x-coordinate to get the tangent gradient m, take −1/m as the normal gradient, and use y − y₁ = (−1/m)(x − x₁).', 'B1 gradient from derivative and negative reciprocal; B1 line through the point [2]'),
    ('Explain why the normal to a curve at a stationary point is a vertical line.', 'At a stationary point the tangent is horizontal (gradient 0); the perpendicular line is vertical, x = x₁.', 'B1 tangent horizontal; B1 normal vertical x = x₁ [2]'),
])


@d74.add('C1', (1, 2, 3))
def d74_c1(r, D):
    t = rpoly(r, 2 if D < 3 else 3, -5, 5)
    x0 = r.randint(-3, 3)
    g = ev(deriv(t), x0)
    if g == 0:
        return None
    if D < 3:
        return MC(r, f'Find the gradient of the tangent to y = {disp(t)} at the point where x = {x0}.', num(g), [num(-1 / g), num(ev(t, x0)), num(-g), num(g + 2 * t[0][0])],
                  f'dy/dx = {idx(deriv(t))}; at x = {x0}: {num(g)}.')
    return MC(r, f'Find the gradient of the normal to y = {disp(t)} at the point where x = {x0}.', num(-1 / g), [num(g), num(1 / g), num(-g), num(-1 / ev(t, x0)) if ev(t, x0) else '0'],
              f'Tangent gradient {num(g)}; normal gradient {num(-1 / g)}.')


@d74.add('C2', (2, 3, 4), 'explain')
def d74_err(r, D):
    nm = person(r)
    t = rpoly(r, 2, -5, 5)
    x0 = r.randint(-3, 3)
    y0 = ev(t, x0)
    g = ev(deriv(t), x0)
    if g == 0:
        return None
    if r.random() < 0.5:
        return Q(f'{nm} finds the equation of the tangent to y = {disp(t)} at x = {x0} as y − {num(y0)} = ({idx(deriv(t))})({xk(x0)}). Explain the error and find the correct equation.'.replace('y − −', 'y + '),
                 f'The gradient must be a number: substitute x = {x0} into dy/dx to get {num(g)}. Tangent: {line_eq(g, y0 - g * x0)}.', f'B1 must evaluate dy/dx at x = {x0}; B1 {line_eq(g, y0 - g * x0)}')
    return Q(f'{nm} finds the normal to y = {disp(t)} at x = {x0} using the gradient {num(-g)}. Explain the error and give the correct gradient of the normal.',
             f'The normal gradient is the negative reciprocal of the tangent gradient {num(g)}: −1/({num(g)}) = {num(-1 / g)}.', f'B1 negative reciprocal; B1 {num(-1 / g)}')


@d74.add('C3', (1, 2, 3, 4, 5), 'numerical')
def d74_calc(r, D):
    t = rpoly(r, 2 if D <= 2 else 3, -5, 5)
    x0 = r.randint(-3, 3)
    y0 = ev(t, x0)
    g = ev(deriv(t), x0)
    if g == 0:
        return None
    if D <= 2:
        return Q(f'Find the equation of the tangent to the curve y = {disp(t)} at the point where x = {x0}.', line_eq(g, y0 - g * x0),
                 f'B1 y = {num(y0)}; M1 dy/dx = {idx(deriv(t))} = {num(g)}; A1 {line_eq(g, y0 - g * x0)}')
    m = -1 / g
    if D == 3:
        return Q(f'Find the equation of the normal to the curve y = {disp(t)} at the point where x = {x0}, giving your answer in the form ax + by + c = 0.', gen_line(m, -1, y0 - m * x0),
                 f'B1 y = {num(y0)}; M1 dy/dx at x = {x0} is {num(g)}; M1 normal gradient {num(m)}; A1 {gen_line(m, -1, y0 - m * x0)}')
    if D == 4:
        X = x0 - y0 / g
        Y = y0 - g * x0
        A = abs(X * Y) / 2
        return Q(f'The tangent to the curve y = {disp(t)} at the point where x = {x0} meets the x-axis at A and the y-axis at B. Find the area of triangle OAB, where O is the origin.', num(A),
                 f'M1 gradient {num(g)}; A1 tangent {line_eq(g, Y)}; B1 A({num(X)}, 0); B1 B(0, {num(Y)}); A1 area {num(A)}')
    # D5: tangent with surd curve y = a√x + b/x at x = 4 or 1
    a, b = r.choice([2, 4, 6, 8]), nz(r, -8, 8)
    x0 = r.choice([1, 4])
    tt = [(a, Fr(1, 2)), (b, -1)]
    y0 = Fr(a) * math.isqrt(x0) + Fr(b, x0)
    g = Fr(a, 2 * math.isqrt(x0)) - Fr(b, x0 * x0)
    if g == 0:
        return None
    return Q(f'Find the equation of the tangent to the curve y = {disp(tt)} at the point where x = {x0}.', line_eq(g, y0 - g * x0),
             f'B1 y = {num(y0)}; M1 dy/dx = {idx(deriv(tt))}; A1 gradient {num(g)}; M1 line through ({x0}, {num(y0)}); A1 {line_eq(g, y0 - g * x0)}')


def d74_c4(r, D):
    for _ in range(80):
        t = rpoly(r, 3, -3, 3)
        x0 = r.randint(-2, 2)
        y0 = ev(t, x0)
        g = ev(deriv(t), x0)
        if g != 0 and abs(g) <= 4 and y0 != 0 and abs(y0) <= 12:
            break
    else:
        return None
    m = -1 / g
    intro = f'The curve C has equation y = {disp(t)}. The point P on C has x-coordinate {x0}.'
    Xt = x0 - y0 / g
    Xn = x0 - y0 / m
    parts = [
        P('Find dy/dx.', idx(deriv(t)), f'B1 {idx(deriv(t))}'),
        P('Find the equation of the tangent to C at P.', line_eq(g, y0 - g * x0), f'B1 P = ({x0}, {num(y0)}); M1 gradient {num(g)}; A1 {line_eq(g, y0 - g * x0)}'),
        P('Find the equation of the normal to C at P, in the form ax + by + c = 0.', gen_line(m, -1, y0 - m * x0), f'M1 gradient {num(m)}; A1 {gen_line(m, -1, y0 - m * x0)}'),
    ]
    if y0 != 0:
        parts.append(P('The tangent and the normal at P meet the x-axis at T and N respectively. Find the length TN.', num(abs(Xt - Xn)),
                       f'M1 T({num(Xt)}, 0); M1 N({num(Xn)}, 0); A1 TN = {num(abs(Xt - Xn))}'))
        parts.append(P('The tangent and the normal at P meet the x-axis at T and N respectively. Find the area of triangle PTN.', num(abs(Xt - Xn) * abs(y0) / 2),
                       f'M1 ½ × TN × |y-coordinate of P|; A1 {num(abs(Xt - Xn) * abs(y0) / 2)}'))
    return cmp_(r, intro, parts)


d74.add('C4', (2, 3, 4, 5))(d74_c4)

CHAPTERS[7] = [d71, d72, d73, d74]


# ================================================================ Chapter 8 Further differentiation

def xf(p):
    return 'x' if p == 0 else f'(x{sg(-p)})'


def cubic_sp(r, rng=4):
    """Cubic with stationary points at integer p < q: returns (terms, p, q)."""
    for _ in range(60):
        a = r.choice([1, 2, -1, -2, 1, 1])
        p, q = sorted(r.sample(range(-rng, rng + 1), 2))
        if (3 * a * (p + q)) % 2 == 0:
            d = r.randint(-8, 8)
            t = [(a, 3), (Fr(-3 * a * (p + q), 2), 2), (3 * a * p * q, 1), (d, 0)]
            return t, p, q, a
    return None


i81 = T('Increasing and decreasing functions and stationary points', 'increasing and decreasing functions', 'stationary points')
i81.fixed('C1', (1, 2), [
    ('A function f is increasing on an interval when', 'f′(x) > 0 on that interval', 'Positive gradient: y increases as x increases.', ['f(x) > 0 on that interval', 'f′(x) < 0 on that interval', 'f″(x) > 0 on that interval']),
    ('At a stationary point of a curve,', 'dy/dx = 0', 'The tangent is horizontal.', ['y = 0', 'd²y/dx² = 0', 'x = 0']),
    ('The function f(x) = x³ + 2x is', 'increasing for all x', "f′(x) = 3x² + 2 > 0 for all x.", ['decreasing for all x', 'increasing only for x > 0', 'stationary at x = 0']),
    ('Where is y = x² − 6x decreasing?', 'x < 3', 'dy/dx = 2x − 6 < 0 when x < 3.', ['x > 3', 'x < 0', '0 < x < 6']),
])
i81.fixed('C2', (2, 3), [
    ('Explain why a function can be positive but decreasing.', 'Being positive is about the value f(x) > 0, whereas decreasing depends on the gradient f′(x) < 0; e.g. f(x) = 1/x for x > 0 is positive and decreasing.', 'B1 value vs gradient; B1 example [2]'),
    ('Explain how to show that a function is increasing for all real x.', 'Find f′(x) and show it is positive for every x, e.g. by completing the square to get a(x + p)² + q with a > 0 and q > 0.', 'B1 f′(x) > 0 for all x; B1 method such as completing the square or discriminant < 0 [2]'),
])


@i81.add('C1', (1, 2, 3))
def i81_c1(r, D):
    res = cubic_sp(r)
    if not res:
        return None
    t, p, q, a = res
    if D < 3:
        return MC(r, f'Find the x-coordinates of the stationary points of y = {disp(t)}.', f'x = {num(p)} and x = {num(q)}',
                  [f'x = {num(-q)} and x = {num(-p)}', f'x = {num(p - 1)} and x = {num(q + 1)}', f'x = {num(2 * p)} and x = {num(2 * q)}', f'x = {num(p + 1)} and x = {num(q + 1)}'],
                  f'dy/dx = {idx(deriv(t))} = {num(3 * a)}{xf(p)}{xf(q)} = 0.')
    inside = a > 0
    c = ineq_in(p, q) if inside else ineq_out(p, q)
    return MC(r, f'Find the set of values of x for which y = {disp(t)} is decreasing.', c, [ineq_out(p, q) if inside else ineq_in(p, q), ineq_in(-q, -p), f'x < {num(p)}', f'x > {num(q)}'],
              f'dy/dx = {idx(deriv(t))} < 0 {"between" if inside else "outside"} the roots {num(p)} and {num(q)}.')


@i81.add('C2', (2, 3, 4), 'explain')
def i81_err(r, D):
    nm = person(r)
    h, k = nz(r, -4, 4), r.randint(1, 6)
    # f'(x) = 3(x − h)² + 3k = 3x² − 6hx + 3h² + 3k -> f(x) = x³ − 3h x² + (3h² + 3k)x + c
    c = r.randint(-9, 9)
    t = [(1, 3), (-3 * h, 2), (3 * h * h + 3 * k, 1), (c, 0)]
    if r.random() < 0.5:
        return Q(f'Show that the function f(x) = {disp(t)} is increasing for all values of x.',
                 f"f′(x) = {idx(deriv(t))} = 3(x{sg(-h)})² + {3 * k} > 0 for all x, so f is increasing.",
                 f"M1 f′(x) = {idx(deriv(t))}; M1 completes the square 3(x{sg(-h)})² + {3 * k} (or discriminant < 0); A1 > 0 for all x, conclusion")
    x0 = r.randint(-5, 5)
    return Q(f'{nm} says that the curve y = {quad(1, -2 * x0, x0 * x0 - 9)} has stationary points at x = {x0 - 3} and x = {x0 + 3}, because y = 0 there. Explain the error and find the stationary point.',
             f'Stationary points need dy/dx = 0, not y = 0 (those are the x-intercepts). dy/dx = {lin(2, -2 * x0)} = 0 gives the stationary point ({x0}, −9).',
             f'B1 stationary means dy/dx = 0; B1 ({x0}, −9)')


@i81.add('C3', (1, 2, 3, 4, 5), 'numerical')
def i81_calc(r, D):
    if D <= 1:
        a, b, c = nz(r, -4, 4), r.randint(-10, 10), r.randint(-9, 9)
        b = 2 * a * r.randint(-4, 4) if b % (2 * a) else b
        x0 = Fr(-b, 2 * a)
        return Q(f'Find the coordinates of the stationary point on the curve y = {quad(a, b, c)}.', pt(x0, a * x0 * x0 + b * x0 + c), f'M1 dy/dx = {lin(2 * a, b)} = 0; A1 {pt(x0, a * x0 * x0 + b * x0 + c)}')
    res = cubic_sp(r)
    if not res:
        return None
    t, p, q, a = res
    if D == 2:
        return Q(f'Find the x-coordinates of the stationary points of the curve y = {disp(t)}.', f'x = {num(p)}, x = {num(q)}', f'M1 dy/dx = {idx(deriv(t))} = 0; A1 x = {num(p)}, {num(q)}')
    if D == 3:
        return Q(f'Find the coordinates of the stationary points of the curve y = {disp(t)}.', f'{pt(p, ev(t, p))} and {pt(q, ev(t, q))}',
                 f'B1 dy/dx = {idx(deriv(t))}; M1 sets = 0 and solves; A1 x = {num(p)}, {num(q)}; A1 both y-coordinates')
    if D == 4:
        inc = r.choice([True, False])
        word = 'increasing' if inc else 'decreasing'
        pos_out = a > 0
        ans = (ineq_out(p, q) if pos_out else ineq_in(p, q)) if inc else (ineq_in(p, q) if pos_out else ineq_out(p, q))
        return Q(f'Find the set of values of x for which the function f(x) = {disp(t)} is {word}.', ans,
                 f'B1 f′(x) = {idx(deriv(t))}; M1 critical values {num(p)}, {num(q)}; A1 {ans}')
    # D5: find k so that f(x) = x³ + bx² + kx is increasing for all x  -> 3x² + 2bx + k ≥ 0 : 4b² − 12k ≤ 0 → k ≥ b²/3
    b = nz(r, -9, 9)
    A = r.choice([1, 1, 2, 3])
    if r.random() < 0.6:
        k0 = Fr(b * b, 3 * A)
        return Q(f'The function f is defined by f(x) = {term(A, 3, first=True)}{term(b, 2)} + kx, where k is a constant. Find the set of values of k for which f is an increasing function.', f'k ≥ {num(k0)}',
                 f'B1 f′(x) = {term(3 * A, 2, first=True)}{term(2 * b, 1)} + k; M1 requires f′(x) ≥ 0 for all x: discriminant ≤ 0; M1 {4 * b * b} − {12 * A}k ≤ 0; A1 k ≥ {num(k0)}')
    k0 = Fr(-b * b, 3 * A)
    return Q(f'The function f is defined by f(x) = {term(-A, 3, first=True)}{term(b, 2)} + kx, where k is a constant. Find the set of values of k for which f is a decreasing function.', f'k ≤ {num(k0)}',
             f'B1 f′(x) = {term(-3 * A, 2, first=True)}{term(2 * b, 1)} + k; M1 requires f′(x) ≤ 0 for all x: discriminant ≤ 0; M1 {4 * b * b} + {12 * A}k ≤ 0; A1 k ≤ {num(k0)}')


def i81_c4(r, D):
    res = cubic_sp(r)
    if not res:
        return None
    t, p, q, a = res
    intro = f'A curve has equation y = {disp(t)}.'
    yp, yq = ev(t, p), ev(t, q)
    lo_pt, hi_pt = ((p, yp), (q, yq)) if a < 0 else ((q, yq), (p, yp))
    parts = [
        P('Find dy/dx.', idx(deriv(t)), f'B1 {idx(deriv(t))}'),
        P('Find the coordinates of the stationary points.', f'{pt(p, yp)} and {pt(q, yq)}', f'M1 dy/dx = 0; A1 x-values {num(p)}, {num(q)}; A1 both points'),
        P('Find the set of values of x for which y increases as x increases.', ineq_out(p, q) if a > 0 else ineq_in(p, q), f'M1 dy/dx > 0; A1 {ineq_out(p, q) if a > 0 else ineq_in(p, q)}'),
        P('Determine the nature of each stationary point.', f'{pt(*hi_pt)} maximum; {pt(*lo_pt)} minimum', f'M1 second derivative {idx(deriv(deriv(t)))} or sign change; A1 both correct'),
        P(f'Find the gradient of the curve at the point where x = {q + 1}.', num(ev(deriv(t), q + 1)), f'B1 {num(ev(deriv(t), q + 1))}'),
    ]
    return cmp_(r, intro, parts)


i81.add('C4', (2, 3, 4, 5))(i81_c4)


# ---------------------------------------------------------------- 8.2 second derivative
i82 = T('Second derivative and the nature of stationary points', 'second derivative', 'nature of stationary points')
i82.fixed('C1', (1, 2), [
    ('At a stationary point, d²y/dx² < 0 indicates', 'a maximum point', 'The gradient is decreasing through zero.', ['a minimum point', 'a point of inflection', 'no conclusion']),
    ('If y = x⁴, what is d²y/dx²?', '12x²', 'dy/dx = 4x³, then 12x².', ['4x³', '12x³', '24x']),
    ('At a stationary point d²y/dx² > 0. The point is', 'a minimum', 'Gradient increasing through zero: minimum.', ['a maximum', 'a point of inflection', 'on the x-axis']),
    ('The second derivative of y = 6√x is', '−(3/2)x^(−3/2)', 'dy/dx = 3x^(−1/2), d²y/dx² = −(3/2)x^(−3/2).', ['3x^(−1/2)', '(3/2)x^(−3/2)', '−3x^(−3/2)']),
])
i82.fixed('C2', (2, 3), [
    ('Explain why the second derivative test fails at the stationary point of y = x⁴ at the origin, and how its nature can still be found.', 'd²y/dx² = 12x² = 0 at x = 0, so the test gives no conclusion; checking the gradient on either side (negative then positive) shows it is a minimum.', 'B1 d²y/dx² = 0 inconclusive; B1 sign of gradient either side shows minimum [2]'),
    ('Explain, in terms of the gradient, why d²y/dx² < 0 at a stationary point gives a maximum.', 'd²y/dx² < 0 means the gradient is decreasing; it passes from positive to zero to negative, so the curve rises then falls: a maximum.', 'B1 gradient decreasing; B1 positive to negative so maximum [2]'),
])


@i82.add('C1', (1, 2, 3))
def i82_c1(r, D):
    res = cubic_sp(r)
    if not res:
        return None
    t, p, q, a = res
    x0 = r.choice([p, q])
    v = ev(deriv(deriv(t)), x0)
    nat = 'maximum' if v < 0 else 'minimum'
    return MC(r, f'The curve y = {disp(t)} has a stationary point where x = {num(x0)}. Find the value of d²y/dx² there and state the nature of the point.', f'{num(v)}; {nat}',
              [f'{num(v)}; {"minimum" if v < 0 else "maximum"}', f'{num(-v)}; {"minimum" if v < 0 else "maximum"}', f'0; point of inflection', f'{num(ev(deriv(t), x0) + 1)}; {nat}'],
              f'd²y/dx² = {idx(deriv(deriv(t)))} = {num(v)} at x = {num(x0)}: {nat}.')


@i82.add('C2', (2, 3, 4), 'explain')
def i82_err(r, D):
    nm = person(r)
    res = cubic_sp(r)
    if not res:
        return None
    t, p, q, a = res
    x0 = p if r.random() < 0.5 else q
    v = ev(deriv(deriv(t)), x0)
    y0 = ev(t, x0)
    nat = 'maximum' if v < 0 else 'minimum'
    return Q(f'{nm} says the stationary point ({num(x0)}, {num(y0)}) of y = {disp(t)} is a {"minimum" if v < 0 else "maximum"} because its y-coordinate is {"less" if v < 0 else "greater"} than the y-coordinate of the other stationary point. Explain why this reasoning is not valid and determine the nature correctly.',
             f'Comparing y-values does not determine the nature. d²y/dx² = {idx(deriv(deriv(t)))} = {num(v)} at x = {num(x0)}, so it is a {nat}.',
             f'B1 must use d²y/dx² or the gradient either side; B1 {num(v)} so {nat}')


@i82.add('C3', (1, 2, 3, 4, 5), 'numerical')
def i82_calc(r, D):
    if D <= 3:
        res = cubic_sp(r)
        if not res:
            return None
        t, p, q, a = res
        vp, vq = ev(deriv(deriv(t)), p), ev(deriv(deriv(t)), q)
        nat = lambda v: 'maximum' if v < 0 else 'minimum'
        if D == 1:
            return Q(f'Given that y = {disp(t)}, find d²y/dx².', idx(deriv(deriv(t))), f'B1 dy/dx = {idx(deriv(t))}; B1 d²y/dx² = {idx(deriv(deriv(t)))}')
        return Q(f'Find the coordinates of the stationary points on the curve y = {disp(t)} and determine their nature.',
                 f'{pt(p, ev(t, p))} {nat(vp)}; {pt(q, ev(t, q))} {nat(vq)}',
                 f'B1 dy/dx; M1 = 0; A1 x = {num(p)}, {num(q)}; A1 y-values; M1 d²y/dx² = {idx(deriv(deriv(t)))}; A1 natures')
    # x + k²/x type: y = a x + b/x  (a, b > 0): stationary at x = ±√(b/a)
    m = r.randint(1, 5)
    a = r.randint(1, 4)
    b = a * m * m
    t = [(a, 1), (b, -1)]
    if D == 4:
        return Q(f'Find the coordinates of the stationary points of the curve y = {disp(t)} and determine their nature.', f'({m}, {2 * a * m}) minimum; ({-m}, {-2 * a * m}) maximum'.replace('(-', '(−').replace(', -', ', −'),
                 f'B1 dy/dx = {idx(deriv(t))}; M1 = 0 ⇒ x² = {m * m}; A1 x = ±{m}; A1 y = ±{2 * a * m}; M1 d²y/dx² = {idx(deriv(deriv(t)))}; A1 natures')
    fam = r.choice(['root', 'root', 'sq', 'kx'])
    if fam == 'root':
        k = 2 * r.randint(1, 10)
        x0, y0 = Fr(k * k, 4), Fr(k * k, 4)
        t = [(k, Fr(1, 2)), (-1, 1)]
        return Q(f'Find the coordinates of the stationary point of the curve y = {disp(t)}, x > 0, and determine its nature.', f'{pt(x0, y0)}; maximum',
                 f'B1 dy/dx = {idx(deriv(t))}; M1 = 0 ⇒ √x = {num(Fr(k, 2))}; A1 x = {num(x0)}; A1 y = {num(y0)}; M1 d²y/dx² = {idx(deriv(deriv(t)))} < 0; A1 maximum')
    if fam == 'sq':
        m = r.randint(1, 6)
        c = r.randint(1, 3)
        t = [(c, 2), (2 * c * m ** 3, -1)]
        return Q(f'Find the coordinates of the stationary point of the curve y = {disp(t)}, x > 0, and determine its nature.', f'{pt(m, 3 * c * m * m)}; minimum',
                 f'B1 dy/dx = {idx(deriv(t))}; M1 = 0 ⇒ x³ = {m ** 3}; A1 x = {m}; A1 y = {3 * c * m * m}; M1 d²y/dx² = {idx(deriv(deriv(t)))} > 0; A1 minimum')
    k = r.choice([3, 6, 9, 12, 15, 18])
    # dy/dx = 1.5 x^(1/2) − k = 0 -> x = (2k/3)²
    x0 = Fr(2 * k, 3) ** 2
    y0 = Fr(2 * k, 3) ** 3 - k * x0
    t = [(1, Fr(3, 2)), (-k, 1)]
    return Q(f'Find the coordinates of the stationary point of the curve y = {disp(t)}, x > 0, and show that it is a minimum.', f'{pt(x0, y0)}; minimum',
             f'B1 dy/dx = {idx(deriv(t))}; M1 √x = {num(Fr(2 * k, 3))}; A1 x = {num(x0)}; A1 y = {num(y0)}; M1 d²y/dx² = (3/4)x^(−1/2) > 0; A1 minimum')


def i82_c4(r, D):
    m = r.randint(1, 4)
    a = r.randint(1, 3)
    b = a * m * m * m * 2
    # y = a x² + b/x : dy/dx = 2a x − b/x² = 0 -> x³ = b/(2a) = m³
    t = [(a, 2), (b, -1)]
    y0 = a * m * m + Fr(b, m)
    intro = f'A curve has equation y = {disp(t)}, for x > 0.'
    parts = [
        P('Find dy/dx and d²y/dx².', f'{idx(deriv(t))}; {idx(deriv(deriv(t)))}', f'B1 {idx(deriv(t))}; B1 {idx(deriv(deriv(t)))}'),
        P('Find the coordinates of the stationary point.', pt(m, y0), f'M1 x³ = {m ** 3}; A1 x = {m}; A1 y = {num(y0)}'),
        P('Determine the nature of the stationary point.', 'minimum', f'M1 d²y/dx² at x = {m} = {num(ev(deriv(deriv(t)), m))}; A1 > 0 so minimum'),
        P('State the least value of y for x > 0.', num(y0), f'B1 {num(y0)}'),
        P(f'Find the gradient of the curve at the point where x = {2 * m}.', num(ev(deriv(t), 2 * m)), f'B1 {num(ev(deriv(t), 2 * m))}'),
    ]
    return cmp_(r, intro, parts)


i82.add('C4', (2, 3, 4, 5))(i82_c4)


# ---------------------------------------------------------------- 8.3 practical max/min
i83 = T('Practical maximum and minimum problems', 'practical maximum and minimum problems', 'optimisation', 'maximum and minimum')
i83.fixed('C1', (1, 2), [
    ('In an optimisation problem, after finding x with dA/dx = 0, the best way to confirm a maximum is to', 'show that d²A/dx² < 0 at that value', 'Negative second derivative at a stationary point gives a maximum.', ['show that A > 0', 'show that d²A/dx² > 0', 'substitute x = 0']),
    ('A rectangle has perimeter 20 cm. Its greatest possible area is', '25 cm²', 'Area x(10 − x) is greatest at x = 5.', ['20 cm²', '100 cm²', '24 cm²']),
    ('Two positive numbers have sum 12. Their product is greatest when the numbers are', '6 and 6', 'P = x(12 − x), dP/dx = 12 − 2x = 0.', ['1 and 11', '4 and 8', '3 and 9']),
])
i83.fixed('C2', (2, 3), [
    ('Explain why it is important to check the domain when solving a practical maximum problem.', 'The variable represents a physical quantity (e.g. a length), so only values in a realistic range are valid; a stationary point outside it, or an end point, may give the true answer.', 'B1 physical restrictions on the variable; B1 check end points / reject invalid values [2]'),
    ('Explain why, to find the maximum volume of an open box made by cutting squares of side x from the corners of a sheet, you only need to consider one stationary point.', 'Only values of x between 0 and half the side of the sheet make a box; the other stationary point lies outside this range (or gives zero volume).', 'B1 valid range of x; B1 other stationary point rejected [2]'),
])


@i83.add('C1', (1, 2, 3))
def i83_c1(r, D):
    S = r.choice([10, 14, 16, 18, 20, 24, 28, 30, 36, 40, 50])
    if r.random() < 0.5:
        return MC(r, f'Two positive numbers x and y have x + y = {S}. Find the greatest possible value of xy.', num(Fr(S * S, 4)), [num(Fr(S * S, 2)), num(S * S), num(S - 1), num(Fr(S * S, 4) - 1)],
                  f'xy = x({S} − x), maximum at x = {num(Fr(S, 2))}: {num(Fr(S * S, 4))}.')
    L = S * 2
    return MC(r, f'A farmer has {L} m of fencing to make three sides of a rectangular pen, the fourth side being a wall. Find the greatest possible area.', f'{num(Fr(L * L, 8))} m²',
              [f'{num(Fr(L * L, 16))} m²', f'{num(Fr(L * L, 4))} m²', f'{num(Fr(L * L, 9))} m²', f'{num(Fr(L * L, 6))} m²'], f'A = x({L} − 2x), dA/dx = {L} − 4x = 0, x = {num(Fr(L, 4))}, A = {num(Fr(L * L, 8))}.')


@i83.add('C2', (2, 3, 4), 'explain')
def i83_show(r, D):
    s = r.choice([12, 18, 24, 30, 36, 42, 48, 60])
    fr = r.choice(['box', 'cyl', 'fence', 'tank', 'sum'])
    if fr == 'box':
        return Q(f'A square sheet of card of side {s} cm has a square of side x cm cut from each corner and the sides are folded up to make an open box. Show that the volume V cm³ is given by V = {idx([(4, 3), (-4 * s, 2), (s * s, 1)])}.',
                 f'The base is ({s} − 2x) by ({s} − 2x) and the height is x, so V = x({s} − 2x)² = {idx([(4, 3), (-4 * s, 2), (s * s, 1)])}.',
                 f'B1 base side {s} − 2x and height x; B1 expands to the given form')
    if fr == 'cyl':
        V = r.choice([250, 500, 1000, 2000, 4000, 300, 600, 750])
        return Q(f'A closed cylinder has radius r cm and volume {V} cm³. Show that its total surface area A cm² is given by A = 2πr² + {2 * V}/r.',
                 f'πr²h = {V} so h = {V}/(πr²); A = 2πr² + 2πrh = 2πr² + 2πr × {V}/(πr²) = 2πr² + {2 * V}/r.', f'M1 h = {V}/(πr²); A1 substitutes into 2πr² + 2πrh to obtain the result')
    if fr == 'fence':
        L = r.choice([30, 40, 50, 60, 80, 90, 100, 120, 150])
        nm = person(r)
        return Q(f'{nm} uses {L} m of fencing for three sides of a rectangular enclosure beside a long wall in {city(r)}. Each side perpendicular to the wall has length x m. Show that the area A m² is A = {L}x − 2x², and explain why 0 < x < {num(Fr(L, 2))}.',
                 f'The side parallel to the wall is {L} − 2x, so A = x({L} − 2x) = {L}x − 2x². Both x and {L} − 2x must be positive, so 0 < x < {num(Fr(L, 2))}.',
                 f'B1 side {L} − 2x and A = {L}x − 2x²; B1 lengths positive so 0 < x < {num(Fr(L, 2))}')
    if fr == 'tank':
        V = r.choice([32, 108, 256, 500, 864, 2048])
        return Q(f'An open tank has a square base of side x m and height h m, and its volume is {V} m³. Show that the external surface area S m² (base and four sides) is S = x² + {4 * V}/x.',
                 f'x²h = {V} so h = {V}/x²; S = x² + 4xh = x² + 4x × {V}/x² = x² + {4 * V}/x.', f'M1 h = {V}/x²; A1 S = x² + 4xh simplified to the given form')
    S = r.choice([12, 15, 18, 20, 24, 30, 36])
    return Q(f'Two positive numbers x and y satisfy x + y = {S}. Show that P = xy² can be written as P = x({S} − x)², and state the set of possible values of x.',
             f'y = {S} − x, so P = xy² = x({S} − x)²; since x > 0 and y > 0, 0 < x < {S}.', f'B1 y = {S} − x substituted; B1 0 < x < {S}')


@i83.add('C3', (1, 2, 3, 4, 5), 'numerical')
def i83_calc(r, D):
    if D <= 2:
        L = r.choice([40, 48, 60, 80, 100, 120, 160, 200])
        nm = person(r)
        return Q(f'{nm} has {L} m of fencing to enclose a rectangular vegetable plot in {city(r)} against a straight wall, so only three sides need fencing. Taking x m as the length of each side perpendicular to the wall, find the value of x that maximises the area and the maximum area.',
                 f'x = {num(Fr(L, 4))}; area {num(Fr(L * L, 8))} m²', f'B1 A = x({L} − 2x); M1 dA/dx = {L} − 4x = 0; A1 x = {num(Fr(L, 4))}; A1 {num(Fr(L * L, 8))} m²')
    if D == 3:
        s = r.choice([12, 18, 24, 30, 36, 42, 48, 60])
        x0 = Fr(s, 6)
        Vm = x0 * (s - 2 * x0) ** 2
        return Q(f'A square sheet of metal of side {s} cm has a square of side x cm removed from each corner and is folded to make an open box with volume V = x({s} − 2x)². Find the value of x for which V is a maximum and the maximum volume.',
                 f'x = {num(x0)}; V = {num(Vm)} cm³', f'M1 expands and differentiates: dV/dx = 12x² − {8 * s}x + {s * s}; M1 = 0 ⇒ x = {num(x0)} or {num(Fr(s, 2))}; A1 x = {num(x0)} (x = {num(Fr(s, 2))} gives V = 0); M1 d²V/dx² < 0; A1 V = {num(Vm)}')
    if D == 4:
        V = r.choice([250, 500, 1000, 1500, 2000])
        r0 = (V / (2 * math.pi)) ** (1 / 3)
        A = 2 * math.pi * r0 ** 2 + 2 * V / r0
        return Q(f'A closed cylindrical can has volume {V} cm³ and radius r cm, so that its surface area is A = 2πr² + {2 * V}/r. Find the value of r that minimises A, and the minimum surface area, giving answers to 3 significant figures.',
                 f'r = {n3(r0)} cm; A = {n3(A)} cm²', f'M1 dA/dr = 4πr − {2 * V}/r²; M1 = 0 ⇒ r³ = {num(Fr(V, 2))}/π; A1 r = {n3(r0)}; M1 d²A/dr² > 0 (minimum); A1 A = {n3(A)}')
    if r.random() < 0.5:
        c2 = r.choice([1, 2, 3])
        c1 = r.choice([2, 3, 4, 5, 6])
        m = 2 * r.randint(1, 5)
        V = Fr(c1 * m ** 3, 2 * c2)
        if V.denominator != 1:
            return None
        V = int(V)
        C = c1 * m * m + Fr(4 * c2 * V, m)
        return Q(f'A closed box has a square base of side x m and a height chosen so that its volume is {V} m³. The base and the top each cost ${c1} per m² and the four sides cost ${2 * c2} per m². Show that the total cost is C = {2 * c1}x² + {8 * c2 * V}/x dollars, and find the value of x that minimises the cost.',
                 f'x = {m}; minimum cost ${num(2 * C)}', f'B1 height {V}/x²; B1 C = 2 × {c1}x² + {2 * c2} × 4x × {V}/x²; M1 dC/dx = {4 * c1}x − {8 * c2 * V}/x² = 0; A1 x = {m}; M1 d²C/dx² > 0; A1 ${num(2 * C)}')
    m = r.randint(2, 12)
    V = 4 * m ** 3
    x0 = 2 * m
    S = x0 * x0 + Fr(4 * V, x0)
    return Q(f'An open water tank has a square base of side x m and vertical sides, and holds {V} m³. The total area of the base and the four sides is S m². Show that S = x² + {4 * V}/x, and find the dimensions that minimise S.',
             f'x = {x0} m, height {num(Fr(V, x0 * x0))} m; S = {num(S)} m²', f'B1 height {V}/x²; B1 S = x² + 4x × {V}/x²; M1 dS/dx = 2x − {4 * V}/x² = 0; A1 x = {x0}; B1 height {num(Fr(V, x0 * x0))}; A1 S = {num(S)} (min by d²S/dx² > 0)')


def i83_c4(r, D):
    P_ = r.choice([4, 6, 8, 10, 12])
    nm = person(r)
    # window: rectangle x by y with semicircle on top of diameter x; perimeter P
    # P = x + 2y + πx/2 -> y = (P − x − πx/2)/2 ; A = xy + πx²/8 = (P x)/2 − x²/2 − πx²/4 + πx²/8 = Px/2 − x²(4 + π)/8
    x0 = 2 * P_ / (4 + math.pi)
    A = P_ * x0 / 2 - x0 * x0 * (4 + math.pi) / 8
    intro = f'{nm} designs a window for a building in {city(r)}. It is a rectangle of width x m and height y m with a semicircle of diameter x m on top. The total perimeter of the window is {P_} m.'
    parts = [
        P('Express y in terms of x.', f'y = ({P_} − x − πx/2)/2', f'B1 x + 2y + πx/2 = {P_}; B1 rearrangement'),
        P(f'Show that the area of the window is A = {num(Fr(P_, 2))}x − (4 + π)x²/8.', 'Shown', 'M1 A = xy + πx²/8; A1 simplifies to given form'),
        P('Find the value of x that maximises the area, correct to 3 significant figures.', f'x = {n3(x0)}', f'M1 dA/dx = {num(Fr(P_, 2))} − (4 + π)x/4 = 0; A1 {n3(x0)}'),
        P('Find the maximum area, correct to 3 significant figures, and show that it is a maximum.', f'{n3(A)} m²', f'B1 d²A/dx² = −(4 + π)/4 < 0; A1 {n3(A)} m²'),
    ]
    return cmp_(r, intro, parts)


i83.add('C4', (2, 3, 4, 5))(i83_c4)


# ---------------------------------------------------------------- 8.4 connected rates of change
i84 = T('Connected rates of change', 'connected rates of change', 'rates of change')
i84.fixed('C1', (1, 2), [
    ('The radius r of a circle increases at 2 cm s⁻¹. Which expression gives dA/dt?', '2πr × 2', 'dA/dt = (dA/dr)(dr/dt) = 2πr × 2.', ['πr² × 2', '2πr ÷ 2', '2 × 2']),
    ('If y = x³ and dx/dt = 0.5, then dy/dt when x = 2 is', '6', 'dy/dt = 3x² × 0.5 = 3 × 4 × 0.5 = 6.', ['12', '4', '1.5']),
    ('The chain rule for connected rates of change is', 'dy/dt = (dy/dx) × (dx/dt)', 'Multiply rates linked through x.', ['dy/dt = (dy/dx) ÷ (dx/dt)', 'dy/dt = (dx/dy) × (dx/dt)', 'dy/dt = dy/dx + dx/dt']),
])
i84.fixed('C2', (2, 3), [
    ('Explain why, when air is pumped into a spherical balloon at a constant rate, the radius increases more slowly as the balloon gets bigger.', 'dV/dt = 4πr² dr/dt; with dV/dt constant, dr/dt = (dV/dt)/(4πr²) decreases as r increases.', 'B1 dr/dt = (dV/dt)/(4πr²); B1 decreases as r increases [2]'),
    ('Explain the meaning of a negative value of dV/dt for a container of liquid.', 'The volume is decreasing with time, i.e. liquid is leaving the container.', 'B1 volume decreasing; B1 in context [2]'),
])


@i84.add('C1', (1, 2, 3))
def i84_c1(r, D):
    n = r.randint(2, 4)
    k = r.choice([0.5, 2, 3, 0.2, 4, 1.5])
    x0 = r.randint(1, 4)
    v = n * x0 ** (n - 1) * k
    return MC(r, f'Given that y = x{sup(n)} and x increases at a rate of {num(k)} units per second, find the rate of increase of y when x = {x0}.', num(round(v, 6)),
              [num(round(n * x0 ** (n - 1) / k, 6)), num(round(x0 ** n * k, 6)), num(round(n * x0 ** n * k, 6)), num(round(v / 2, 6))], f'dy/dt = {n}x{sup(n - 1)} × {num(k)} = {num(round(v, 6))}.'.replace('x¹', 'x'))


@i84.add('C2', (2, 3, 4), 'explain')
def i84_err(r, D):
    nm = person(r)
    R = r.choice([3, 4, 5, 6, 8, 10])
    k = r.choice([2, 3, 4, 5, 10])
    return Q(f'Oil spreads in a circular patch on water near {city(r)}. The radius increases at {k} cm s⁻¹. {nm} says dA/dt = πr² × {k} = {num(k * R * R)}π cm² s⁻¹ when r = {R}. Explain the error and find the correct rate.',
             f'{nm} multiplied the area, not its derivative dA/dr = 2πr, by dr/dt. dA/dt = 2π × {R} × {k} = {2 * R * k}π cm² s⁻¹.', f'B1 must use dA/dr = 2πr; B1 {2 * R * k}π')


@i84.add('C3', (1, 2, 3, 4, 5), 'numerical')
def i84_calc(r, D):
    if D <= 2:
        R, k = r.choice([2, 3, 4, 5, 6, 8, 10]), r.choice([0.5, 1.5, 2, 3, 4])
        return Q(f'The radius of a circle is increasing at {num(k)} cm s⁻¹. Find the rate of increase of the area when the radius is {R} cm, giving your answer in terms of π.', f'{num(2 * R * k)}π cm² s⁻¹',
                 f'M1 dA/dr = 2πr; M1 × {num(k)}; A1 {num(2 * R * k)}π')
    if D == 3:
        Q_, R = r.choice([20, 40, 50, 80, 100]), r.choice([2, 4, 5, 8, 10])
        v = Q_ / (4 * math.pi * R * R)
        return Q(f'Air is pumped into a spherical balloon at {Q_} cm³ s⁻¹. Find the rate of increase of the radius when the radius is {R} cm.', f'{n3(v)} cm s⁻¹',
                 f'B1 dV/dr = 4πr²; M1 dr/dt = {Q_}/(4π × {R * R}); A1 {n3(v)}')
    if D == 4:
        k = r.choice([2, 3, 5, 6, 8])
        h0 = r.choice([2, 3, 4, 5, 6])
        Q_ = r.choice([10, 12, 15, 20, 30])
        # V = k π h³/ 3 style: V = (π/3) k h³ ; dV/dh = π k h²
        v = Q_ / (math.pi * k * h0 * h0)
        return Q(f'Water is poured into a conical container at {Q_} cm³ s⁻¹. When the depth is h cm, the volume is V = ({k}/3)πh³ cm³. Find the rate at which the depth is increasing when h = {h0}.', f'{n3(v)} cm s⁻¹',
                 f'B1 dV/dh = {k}πh²; M1 dh/dt = {Q_} ÷ ({k}π × {h0 * h0}); A1 {n3(v)}')
    if r.random() < 0.5:
        R = r.choice([2, 3, 4, 5, 6, 8, 10, 12])
        Q_ = r.choice([10, 20, 30, 40, 50, 60, 80, 100, 120])
        dS = Fr(2 * Q_, R)
        return Q(f'The volume of a spherical balloon is increasing at {Q_} cm³ s⁻¹. Find the rate of increase of its surface area when the radius is {R} cm.', f'{num(dS) if dS.denominator == 1 else n3(float(dS))} cm² s⁻¹',
                 f'B1 dV/dr = 4πr²; M1 dr/dt = {Q_}/(4π × {R * R}); B1 dS/dr = 8πr; M1 dS/dt = 8π × {R} × dr/dt; A1 {num(dS) if dS.denominator == 1 else n3(float(dS))}')
    x0 = r.choice([2, 3, 4, 5, 6, 8, 10])
    Q_ = r.choice([6, 12, 18, 24, 30, 36, 48, 60, 90])
    dxdt = Fr(Q_, 3 * x0 * x0)
    dS = 12 * x0 * dxdt
    return Q(f'The volume of a cube is increasing at {Q_} cm³ s⁻¹. Find the rate of increase of its surface area when the edge length is {x0} cm.', f'{num(dS)} cm² s⁻¹',
             f'B1 dV/dx = 3x²; M1 dx/dt = {Q_}/{3 * x0 * x0} = {num(dxdt)}; B1 dS/dx = 12x; M1 dS/dt = 12 × {x0} × {num(dxdt)}; A1 {num(dS)}')


def i84_c4(r, D):
    a, b = r.randint(1, 3), r.randint(1, 6)
    k = r.choice([0.1, 0.2, 0.5, 0.05])
    x0 = r.randint(1, 4)
    t = [(a, 3), (b, 1)]
    g = ev(deriv(t), x0)
    intro = f'A point P moves along the curve y = {disp(t)} in such a way that the x-coordinate of P increases at a constant rate of {num(k)} units per second.'
    parts = [
        P(f'Find the rate at which the y-coordinate of P is increasing when x = {x0}.', num(round(float(g) * k, 6)), f'B1 dy/dx = {idx(deriv(t))}; M1 dy/dt = {num(g)} × {num(k)}; A1 {num(round(float(g) * k, 6))}'),
        P(f'Find the value of x at which the y-coordinate is increasing at {num(round(float(ev(deriv(t), x0 + 1)) * k, 6))} units per second (x > 0).', f'x = {x0 + 1}',
          f'M1 ({idx(deriv(t))}) × {num(k)} = {num(round(float(ev(deriv(t), x0 + 1)) * k, 6))}; A1 x = {x0 + 1}'),
        P('Explain why the y-coordinate is always increasing.', f'dy/dx = {idx(deriv(t))} > 0 for all x and dx/dt > 0, so dy/dt > 0.', 'B1 dy/dx > 0 and dx/dt > 0'),
        P(f'Find the rate of change of the gradient of the curve at P when x = {x0}.', num(round(float(ev(deriv(deriv(t)), x0)) * k, 6)),
          f'M1 d²y/dx² = {idx(deriv(deriv(t)))}; A1 × {num(k)} = {num(round(float(ev(deriv(deriv(t)), x0)) * k, 6))}'),
    ]
    return cmp_(r, intro, parts)


i84.add('C4', (2, 3, 4, 5))(i84_c4)

CHAPTERS[8] = [i81, i82, i83, i84]


# ================================================================ Chapter 9 Integration

def integ(terms):
    return [(Fr(c) / (Fr(n) + 1), Fr(n) + 1) for c, n in terms if c != 0]


def defint(terms, a, b):
    F = integ(terms)
    return ev(F, b) - ev(F, a)


n91 = T('Integration as the reverse of differentiation and indefinite integrals', 'integration as the reverse of differentiation', 'indefinite integrals')
n91.fixed('C1', (1, 2), [
    ('Find ∫ 6x² dx.', '2x³ + c', 'Increase the power by 1 and divide by the new power.', ['12x + c', '6x³ + c', '3x³ + c']),
    ('Why is a constant of integration added to an indefinite integral?', 'because many functions have the same derivative', 'Constants differentiate to zero, so the integral is only known up to a constant.', ['because the integral is always positive', 'to make the answer exact', 'because integration is approximate']),
    ('Find ∫ x⁻² dx.', '−x⁻¹ + c', 'x⁻¹/(−1) + c.', ['−2x⁻³ + c', 'x⁻¹ + c', '−x⁻³/3 + c']),
    ('Find ∫ √x dx.', '(2/3)x^(3/2) + c', 'x^(1/2) → x^(3/2)/(3/2).', ['(1/2)x^(−1/2) + c', '(3/2)x^(3/2) + c', 'x^(3/2) + c']),
    ('Which power of x cannot be integrated using ∫ xⁿ dx = xⁿ⁺¹/(n + 1) + c?', 'x⁻¹', 'n = −1 would give division by zero.', ['x⁰', 'x^(1/2)', 'x⁻²']),
])
n91.fixed('C2', (2, 3), [
    ('Explain why ∫ 2x dx = x² + c rather than just x².', 'Any function x² + c has derivative 2x, so the integral is the whole family of such functions; c is the constant of integration.', 'B1 derivative of a constant is zero; B1 family of curves [2]'),
    ('Explain how you can check the result of an indefinite integration.', 'Differentiate the answer; it should give back the original function (the integrand).', 'B1 differentiate; B1 obtain integrand [2]'),
])


@n91.add('C1', (1, 2, 3))
def n91_c1(r, D):
    c = nz(r, -9, 12)
    n = r.choice([Fr(2), Fr(3), Fr(4), Fr(-2), Fr(-3), Fr(1, 2), Fr(-1, 2), Fr(3, 2), Fr(1, 3), Fr(5)])
    if (c % (n + 1).numerator if (n + 1).denominator == 1 else 0) and D == 1:
        c = c * int(n + 1) if (n + 1).denominator == 1 else c
    t = [(c, n)]
    right = idx(integ(t)) + ' + c'
    ds = [idx([(c, n + 1)]) + ' + c', idx(deriv(t)) + ' + c', idx([(c * (n + 1), n + 1)]) + ' + c', idx([(c / n if n else c, n - 1)]) + ' + c', idx([(-c / (n + 1), n + 1)]) + ' + c']
    return MC(r, f'Find ∫ {disp(t)} dx.', right, ds, f'∫ xⁿ dx = xⁿ⁺¹/(n + 1) + c: {right}.')


@n91.add('C2', (2, 3, 4), 'explain')
def n91_err(r, D):
    nm = person(r)
    fr = r.choice(['noc', 'diff', 'recip'])
    t = rpoly(r, 2, -6, 6)
    if fr == 'noc':
        return Q(f'{nm} writes ∫ ({disp(t)}) dx = {idx(integ(t))}. Explain what is missing and why it matters.',
                 f'The constant of integration: the answer is {idx(integ(t))} + c, since any constant differentiates to zero.', 'B1 + c missing; B1 reason (constant differentiates to 0)')
    if fr == 'diff':
        return Q(f'{nm} is asked to find ∫ ({disp(t)}) dx and writes {idx(deriv(t))} + c. Explain the error and find the integral correctly.',
                 f'{nm} differentiated instead of integrating. ∫ = {idx(integ(t))} + c.', f'B1 differentiated not integrated; B1 {idx(integ(t))} + c')
    k, n = nz(r, 2, 9), r.randint(2, 4)
    return Q(f'{nm} says that ∫ {k}/x{sup(n)} dx cannot be found with the power rule because the power of x is in the denominator. Explain how to integrate it and give the result.',
             f'Write it as {idx([(k, -n)])}; then ∫ = {idx(integ([(k, -n)]))} + c (power rule works because n ≠ −1).', f'B1 rewrite as {idx([(k, -n)])}; B1 {idx(integ([(k, -n)]))} + c')


@n91.add('C3', (1, 2, 3, 4, 5), 'numerical')
def n91_calc(r, D):
    if D == 1:
        t = rpoly(r, 3)
        return Q(f'Find ∫ ({disp(t)}) dx.', idx(integ(t)) + ' + c', f'M1 increases powers by 1; A1 {idx(integ(t))}; B1 + c'.replace('; B1 + c', ' + c'))
    if D == 2:
        t = rterms(r, 2)
        if any(Fr(n) == -1 for _, n in t):
            return None
        return Q(f'Find ∫ ({disp(t)}) dx.', idx(integ(t)) + ' + c', f'M1 powers of x; A1 one term; A1 {idx(integ(t))} + c')
    if D == 3:
        a, b = nz(r, -5, 6), nz(r, -6, 6)
        # (a x + b)² expanded
        t = [(a * a, 2), (2 * a * b, 1), (b * b, 0)]
        return Q(f'Find ∫ ({lin(a, b)})² dx by first expanding the bracket.', idx(integ(t)) + ' + c', f'M1 expands to {idx(t)}; A1 {idx(integ(t))} + c')
    if D == 4:
        a, b, c = nz(r, -4, 5), r.randint(-6, 6), nz(r, -8, 8)
        t = [(a, Fr(3, 2)), (b, Fr(1, 2)), (c, Fr(-1, 2))]
        return Q(f'Find ∫ ({quad(a, b, c)})/√x dx.', idx(integ(t)) + ' + c', f'M1 divides: {idx(t)}; A1 two terms; A1 {idx(integ(t))} + c')
    # D5: curve through point
    t = rterms(r, 2)
    if any(Fr(n) == -1 for _, n in t):
        return None
    x0 = r.choice([1, 4]) if any(Fr(n).denominator == 2 for _, n in t) else r.choice([1, 2, -1])
    y0 = r.randint(-10, 10)
    F = integ(t)
    cc = y0 - ev(F, x0)
    if not isinstance(cc, Fr):
        return None
    return Q(f'A curve has gradient function dy/dx = {disp(t)} and passes through the point ({x0}, {y0}). Find the equation of the curve.', f'y = {idx(F + [(cc, 0)])}',
             f'M1 integrates; A1 {idx(F)} + c; M1 substitutes ({x0}, {y0}); A1 c = {num(cc)}')


def n91_c4(r, D):
    t = rpoly(r, 2, -6, 6)
    x0, y0 = r.randint(-2, 3), r.randint(-8, 8)
    F = integ(t)
    cc = y0 - ev(F, x0)
    eq = idx(F + [(cc, 0)])
    intro = f'A curve has gradient function dy/dx = {disp(t)} and passes through the point P({x0}, {y0}).'
    gP = ev(t, x0)
    parts = [
        P('Find ∫ (dy/dx) dx.', idx(F) + ' + c', f'M1 powers increased; A1 {idx(F)} + c'),
        P('Find the equation of the curve.', f'y = {eq}', f'M1 substitutes P; A1 c = {num(cc)}; A1 y = {eq}'),
        P('Find the gradient of the curve at P.', num(gP), f'B1 {num(gP)}'),
    ]
    if gP != 0:
        parts.append(P('Find the equation of the tangent to the curve at P.', line_eq(gP, y0 - gP * x0), f'M1 {'y' if y0 == 0 else 'y' + sg(-y0)} = {num(gP)}({xk(x0)}); A1 {line_eq(gP, y0 - gP * x0)}'))
    return cmp_(r, intro, parts)


n91.add('C4', (2, 3, 4, 5))(n91_c4)


# ---------------------------------------------------------------- 9.2 (ax+b)^n and curves from gradients
n92 = T('Integrating (ax + b)ⁿ and finding a curve from its gradient', 'integrating (ax + b)ⁿ', 'finding a curve from its gradient')
n92.fixed('C1', (1, 2), [
    ('Find ∫ (2x + 1)⁴ dx.', '(2x + 1)⁵/10 + c', '(2x + 1)⁵/(5 × 2) + c.', ['(2x + 1)⁵/5 + c', '8(2x + 1)³ + c', '2(2x + 1)⁵/5 + c']),
    ('Find ∫ (3x − 2)⁻² dx.', '−1/(3(3x − 2)) + c', '(3x − 2)⁻¹/(−1 × 3) + c.', ['−1/(3x − 2) + c', '−6(3x − 2)⁻³ + c', '1/(3(3x − 2)) + c']),
    ('Find ∫ √(4x + 1) dx.', '(1/6)(4x + 1)^(3/2) + c', '(4x + 1)^(3/2)/((3/2) × 4) + c.', ['(2/3)(4x + 1)^(3/2) + c', '(1/8)(4x + 1)^(−1/2) + c', '(3/8)(4x + 1)^(3/2) + c']),
    ('A curve has dy/dx = 2x and passes through (0, 3). Its equation is', 'y = x² + 3', 'y = x² + c with c = 3.', ['y = x² − 3', 'y = 2x + 3', 'y = x² + 3x']),
])
n92.fixed('C2', (2, 3), [
    ('Explain why ∫ (ax + b)ⁿ dx = (ax + b)ⁿ⁺¹/(a(n + 1)) + c, by differentiating the right-hand side.', 'By the chain rule, d/dx[(ax + b)ⁿ⁺¹/(a(n + 1))] = (n + 1)(ax + b)ⁿ × a/(a(n + 1)) = (ax + b)ⁿ.', 'B1 chain rule factor a; B1 simplifies to (ax + b)ⁿ [2]'),
    ('Explain why a point on the curve is needed to find the equation of a curve from its gradient function.', 'Integration gives a family y = F(x) + c of parallel curves; one point fixes the value of c.', 'B1 family of curves / unknown c; B1 point determines c [2]'),
])


@n92.add('C1', (1, 2, 3))
def n92_c1(r, D):
    a, b = nz(r, 2, 6), nz(r, -9, 9)
    n = r.choice([Fr(2), Fr(3), Fr(4), Fr(5), Fr(-2), Fr(-3), Fr(1, 2), Fr(-1, 2), Fr(3, 2)])
    k = nz(r, 1, 6)
    c = Fr(k) / (a * (n + 1))
    right = cpow(c, a, b, n + 1) + ' + c'
    ds = [cpow(Fr(k) / (n + 1), a, b, n + 1) + ' + c', cpow(Fr(k * a) / (n + 1), a, b, n + 1) + ' + c', cpow(k * n * a, a, b, n - 1) + ' + c', cpow(Fr(k) / a, a, b, n + 1) + ' + c']
    return MC(r, f'Find ∫ {cdisp(k, a, b, n)} dx.', right, ds, f'∫ (ax + b)ⁿ dx = (ax + b)ⁿ⁺¹/(a(n + 1)) + c: {right}.')


@n92.add('C2', (2, 3, 4), 'explain')
def n92_err(r, D):
    nm = person(r)
    a, b = nz(r, 2, 6), nz(r, -9, 9)
    n = r.choice([2, 3, 4, 5, -3])
    wrong = cpow(Fr(1, n + 1), a, b, n + 1)
    right = cpow(Fr(1, a * (n + 1)), a, b, n + 1)
    return Q(f'{nm} writes ∫ {cdisp(1, a, b, n)} dx = {wrong} + c. Explain the error, checking by differentiation, and give the correct integral.',
             f'Differentiating {wrong} gives {cpow(a, a, b, n)}, which is {a} times too big: {nm} forgot to divide by {a}, the coefficient of x. Correct: {right} + c.',
             f'B1 differentiation check shows factor {a}; B1 {right} + c')


@n92.add('C3', (1, 2, 3, 4, 5), 'numerical')
def n92_calc(r, D):
    a, b = nz(r, 1, 5), r.randint(-6, 6)
    if D <= 2:
        n = r.choice([2, 3, 4, -2, -3])
        k = nz(r, 1, 8)
        return Q(f'Find ∫ {cdisp(k, a, b, n)} dx.', cpow(Fr(k) / (a * (n + 1)), a, b, n + 1) + ' + c', f'M1 power {n + 1}; A1 {cpow(Fr(k) / (a * (n + 1)), a, b, n + 1)} + c')
    if D == 3:
        s = r.randint(1, 5)
        x0 = r.randint(0, 3)
        b = s * s - a * x0
        k = r.choice([3, 6, 9, 12])
        y0 = r.randint(-5, 10)
        # dy/dx = k/√(ax+b) -> y = (2k/a)√(ax+b) + c
        cc = y0 - Fr(2 * k, a) * s
        return Q(f'A curve has gradient dy/dx = {cdisp(k, a, b, Fr(-1, 2))} and passes through the point ({x0}, {y0}). Find the equation of the curve.', f'y = {num(Fr(2 * k, a))}√({lin(a, b)}){sg(cc) if cc else ""}',
                 f'M1 integrates to k(ax + b)^(1/2); A1 {num(Fr(2 * k, a))}√({lin(a, b)}) + c; M1 substitutes ({x0}, {y0}); A1 c = {num(cc)}')
    if D == 4:
        n = r.choice([2, 3])
        x0 = r.randint(-1, 3)
        u = a * x0 + b
        k = a * (n + 1) * r.randint(1, 3)
        y0 = r.randint(-10, 10)
        cc = y0 - Fr(k, a * (n + 1)) * u ** (n + 1)
        F = cpow(Fr(k, a * (n + 1)), a, b, n + 1)
        return Q(f'The gradient of a curve is given by dy/dx = {cdisp(k, a, b, n)}. The curve passes through ({x0}, {y0}). Find the equation of the curve.', f'y = {F}{sg(cc) if cc else ""}',
                 f'M1 ({lin(a, b)})^{n + 1} with ÷ {a}; A1 {F} + c; M1 uses ({x0}, {y0}); A1 c = {num(cc)}'.replace(f'^{n + 1}', sup(n + 1)))
    # D5: dy/dx = kx + m/x² with a stationary point at x = s (so m = −k s³), curve through (1, y0)
    k, s_ = r.randint(1, 3), r.choice([2, 3])
    m = -k * s_ ** 3
    y0 = r.randint(-6, 6)
    t = [(k, 1), (m, -2)]
    F = integ(t)
    cc = y0 - ev(F, 1)
    return Q(f'A curve has gradient dy/dx = kx {"−" if m < 0 else "+"} {abs(m)}/x², where k is a constant, and has a stationary point where x = {s_}. The curve passes through (1, {y0}). Find k and the equation of the curve.',
             f'k = {k}; y = {idx(F + [(cc, 0)])}', f'M1 {s_}k {"−" if m < 0 else "+"} {abs(m)}/{s_ * s_} = 0; A1 k = {k}; M1 integrates: {idx(F)} + c; M1 substitutes (1, {y0}); A1 y = {idx(F + [(cc, 0)])}')


def n92_c4(r, D):
    a = r.randint(1, 4)
    s = r.randint(2, 4)
    x0 = r.randint(0, 3)
    b = s * s - a * x0
    k = r.choice([2, 4, 6])
    y0 = r.randint(2, 12)
    G = Fr(2 * k, a)
    cc = y0 - G * s
    intro = f'A curve has gradient function dy/dx = {cdisp(k, a, b, Fr(-1, 2))} and passes through P({x0}, {y0}).'
    gP = Fr(k, s)
    parts = [
        P('Find the equation of the curve.', f'y = {num(G)}√({lin(a, b)}){sg(cc) if cc else ""}', f'M1 integrates; A1 {num(G)}√({lin(a, b)}); M1 uses P; A1 c = {num(cc)}'),
        P('Find the gradient of the curve at P.', num(gP), f'B1 {num(gP)}'),
        P('Find the equation of the normal to the curve at P, in the form ax + by + c = 0.', gen_line(-1 / gP, -1, y0 + x0 / gP), f'M1 gradient {num(-1 / gP)}; A1 {gen_line(-1 / gP, -1, y0 + x0 / gP)}'),
        P('Explain why the curve has no stationary points.', f'dy/dx = {k}/√({lin(a, b)}) is never zero.', 'B1 numerator non-zero'),
    ]
    return cmp_(r, intro, parts)


n92.add('C4', (2, 3, 4, 5))(n92_c4)


# ---------------------------------------------------------------- 9.3 definite integrals and area
n93 = T('Definite integration and area under and between curves', 'definite integration', 'area under and between curves')
n93.fixed('C1', (1, 2), [
    ('Evaluate ∫₀² 3x² dx.', '8', '[x³]₀² = 8.', ['12', '6', '24']),
    ('A definite integral ∫ₐᵇ f(x) dx gives a negative value when', 'the curve lies below the x-axis between a and b', 'Area below the axis is counted negatively.', ['the curve is decreasing', 'a < b', 'f(x) is a polynomial']),
    ('The area between y = f(x) and y = g(x) from x = a to x = b, where f(x) ≥ g(x), is', '∫ₐᵇ (f(x) − g(x)) dx', 'Subtract the lower curve from the upper.', ['∫ₐᵇ f(x) dx × ∫ₐᵇ g(x) dx', '∫ₐᵇ (f(x) + g(x)) dx', '∫ₐᵇ (g(x) − f(x)) dx']),
    ('Evaluate ∫₁⁴ x^(−1/2) dx.', '2', '[2√x]₁⁴ = 4 − 2 = 2.', ['1', '4', '3/2']),
])
n93.fixed('C2', (2, 3), [
    ('Explain why ∫₋₁¹ x³ dx = 0 even though the curve encloses regions with the x-axis.', 'The region for −1 ≤ x ≤ 0 is below the axis and gives a negative integral equal in size to the positive part for 0 ≤ x ≤ 1, so they cancel.', 'B1 part below axis negative; B1 equal and opposite cancel [2]'),
    ('Explain why there is no constant of integration in a definite integral.', 'The constant appears in both F(b) and F(a) and cancels when they are subtracted.', 'B1 F(b) − F(a); B1 c cancels [2]'),
])


@n93.add('C1', (1, 2, 3))
def n93_c1(r, D):
    t = rpoly(r, 2, -5, 5)
    a = r.randint(-2, 1)
    b = a + r.randint(1, 3)
    v = defint(t, a, b)
    F = integ(t)
    return MC(r, f'Evaluate ∫ from {a} to {b} of ({disp(t)}) dx.', num(v), [num(-v), num(ev(F, b)), num(ev(t, b) - ev(t, a)), num(v + ev(F, a) * 2 if ev(F, a) else v + 1)],
              f'[{idx(F)}] from {a} to {b} = {num(v)}.')


@n93.add('C2', (2, 3, 4), 'explain')
def n93_err(r, D):
    nm = person(r)
    p = r.randint(1, 4)
    q = p + r.randint(1, 3)
    # y = x(x − p)... area for 0..q where curve below axis on 0..p: y = x² − p x
    t = [(1, 2), (-p, 1)]
    A1 = abs(defint(t, 0, p))
    A2 = defint(t, p, q)
    net = defint(t, 0, q)
    return Q(f'{nm} finds the total area between the curve y = {disp(t)}, the x-axis and the lines x = 0 and x = {q} by calculating ∫₀^{q} ({disp(t)}) dx = {num(net)}. Explain why this does not give the total area and find the correct area.',
             f'The curve is below the x-axis for 0 < x < {p}, so that part of the integral is negative and cancels some positive area. Total area = {num(A1)} + {num(A2)} = {num(A1 + A2)}.',
             f'B1 curve crosses the axis at x = {p} (negative part); M1 splits the integral; A1 {num(A1 + A2)}')


@n93.add('C3', (1, 2, 3, 4, 5), 'numerical')
def n93_calc(r, D):
    if D == 1:
        t = rpoly(r, 2, -5, 6)
        a, b = sorted(r.sample(range(-2, 5), 2))
        return Q(f'Evaluate ∫ from {a} to {b} of ({disp(t)}) dx.', num(defint(t, a, b)), f'M1 integrates: {idx(integ(t))}; M1 substitutes limits; A1 {num(defint(t, a, b))}')
    if D == 2:
        k = r.choice([2, 4, 6, 8])
        c = nz(r, -6, 6)
        t = [(k, Fr(-1, 2)), (c, -2)]
        a, b = r.choice([(1, 4), (1, 9), (4, 9), (4, 16), (1, 16)])
        return Q(f'Evaluate ∫ from {a} to {b} of ({disp(t)}) dx.', num(defint(t, a, b)), f'M1 integrates: {idx(integ(t))}; M1 limits; A1 {num(defint(t, a, b))}')
    if D == 3:
        p = r.randint(1, 5)
        q = p + r.randint(1, 5)
        A = Fr((q - p) ** 3, 6)
        # y = −(x − p)(x − q), area between curve and x-axis
        t = [(-1, 2), (p + q, 1), (-p * q, 0)]
        return Q(f'Find the area of the region enclosed by the curve y = {disp(t)} and the x-axis.', num(A),
                 f'B1 roots x = {p}, {q}; M1 ∫ from {p} to {q}: [{idx(integ(t))}]; A1 {num(A)}')
    if D == 4:
        x1 = r.randint(-3, 2)
        x2 = x1 + r.randint(1, 5)
        b, c = r.randint(-4, 4), r.randint(-4, 6)
        f = lambda x: x * x + b * x + c
        m = x1 + x2 + b
        n = f(x1) - m * x1
        A = Fr((x2 - x1) ** 3, 6)
        return Q(f'The line y = {lin(m, n)} meets the curve y = {quad(1, b, c)} at two points. Find the area of the region enclosed between the line and the curve.'.replace('y = 0x', 'y = '), num(A),
                 f'M1 solves {quad(1, b - m, c - n)} = 0: x = {x1}, {x2}; M1 ∫ (line − curve) dx between these limits; A1 [{idx(integ([(-1, 2), (m - b, 1), (n - c, 0)]))}]; A1 {num(A)}')
    p = r.randint(1, 3)
    q = p + r.randint(1, 3)
    t = [(1, 3), (-(p + q), 2), (p * q, 1)]
    # y = x(x − p)(x − q): areas from 0..p (above) and p..q (below)
    A1 = defint(t, 0, p)
    A2 = -defint(t, p, q)
    return Q(f'The curve y = x(x − {p})(x − {q}) meets the x-axis at O, A and B. Find the total area of the two regions enclosed by the curve and the x-axis.', num(A1 + A2),
             f'B1 expands to {idx(t)}; M1 integrates; A1 ∫₀^{p} = {num(A1)}; A1 ∫ from {p} to {q} = {num(-A2)}; A1 total {num(A1 + A2)}')


def n93_c4(r, D):
    p = r.randint(1, 3)
    q = p + r.randint(2, 4)
    t = [(-1, 2), (p + q, 1), (-p * q, 0)]
    h = Fr(p + q, 2)
    ymax = -(h - p) * (h - q)
    intro = f'The curve C has equation y = {disp(t)}.'
    A = Fr((q - p) ** 3, 6)
    parts = [
        P('Find the coordinates of the points where C meets the x-axis.', f'({p}, 0) and ({q}, 0)', f'M1 factorises −(x − {p})(x − {q}); A1 both'),
        P('Find the coordinates of the maximum point of C.', pt(h, ymax), f'M1 dy/dx = {idx(deriv(t))} = 0; A1 {pt(h, ymax)}'),
        P('Find the area of the region enclosed by C and the x-axis.', num(A), f'M1 integrates; M1 limits {p} and {q}; A1 {num(A)}'),
        P('Find the area of the region bounded by C, the x-axis and the line x = 0, which lies below the x-axis.', num(abs(defint(t, 0, p))), f'M1 ∫₀^{p}; A1 {num(abs(defint(t, 0, p)))}'),
    ]
    return cmp_(r, intro, parts)


n93.add('C4', (2, 3, 4, 5))(n93_c4)


# ---------------------------------------------------------------- 9.4 improper integrals and volumes
n94 = T('Improper integrals and volumes of revolution about the x- and y-axes', 'improper integrals', 'volumes of revolution')
n94.fixed('C1', (1, 2), [
    ('The volume generated when y = f(x), a ≤ x ≤ b, is rotated through 360° about the x-axis is', '∫ₐᵇ πy² dx', 'Sum of discs of radius y and thickness dx.', ['∫ₐᵇ 2πy dx', '∫ₐᵇ πy dx', 'π∫ₐᵇ x² dy']),
    ('Evaluate ∫₁^∞ 1/x² dx.', '1', '[−1/x]₁^∞ = 0 − (−1) = 1.', ['∞', '0', '1/2']),
    ('Which integral is improper?', '∫₀¹ 1/√x dx', 'The integrand is undefined at x = 0.', ['∫₁² 1/√x dx', '∫₀¹ x² dx', '∫₁⁴ √x dx']),
    ('The volume generated by rotating x = g(y), c ≤ y ≤ d, about the y-axis is', '∫ πx² dy from c to d', 'Discs of radius x stacked along the y-axis.', ['∫ πy² dx from c to d', '∫ πx dy from c to d', '∫ 2πx² dy from c to d']),
])
n94.fixed('C2', (2, 3), [
    ('Explain why ∫₁^∞ 1/x dx does not have a finite value, whereas ∫₁^∞ 1/x² dx = 1.', 'For 1/x², ∫₁ᵗ = 1 − 1/t → 1 as t → ∞. For 1/x the integral grows without bound (it behaves like ln t), so it has no finite limit.', 'B1 limit 1 − 1/t → 1; B1 1/x integral unbounded [2]'),
    ('Explain why the formula for a volume of revolution about the x-axis uses y² rather than y.', 'Each thin slice is a disc of radius y, whose area is πy²; adding the discs gives ∫ πy² dx.', 'B1 cross-section is a disc radius y; B1 area πy² [2]'),
])


@n94.add('C1', (1, 2, 3))
def n94_c1(r, D):
    k, n = nz(r, 1, 9), r.randint(2, 4)
    a = r.choice([1, 2, 3])
    v = Fr(k, (n - 1) * a ** (n - 1))
    return MC(r, f'Evaluate the improper integral ∫ from {a} to ∞ of {k}/x{sup(n)} dx.', num(v), [num(Fr(k, n * a ** n)), num(Fr(k, (n - 1))), 'the integral does not converge', num(-v)],
              f'[−{k}/({n - 1}x{sup(n - 1)})] from {a} to ∞ = 0 + {num(v)} = {num(v)}.'.replace('x¹', 'x').replace('(1x)', 'x'))


@n94.add('C2', (2, 3, 4), 'explain')
def n94_err(r, D):
    nm = person(r)
    k = r.choice([2, 3, 4, 5, 6])
    b = r.randint(2, 5)
    V = Fr(k * k * b * b, 2) * 1  # ∫0^b π (k√x)² dx = π k² b²/2
    return Q(f'The region under y = {k}√x from x = 0 to x = {b} is rotated through 360° about the x-axis. {nm} calculates the volume as π∫₀^{b} {k}√x dx. Explain the error and find the correct volume in terms of π.',
             f'The volume uses y², not y: V = π∫₀^{b} {k * k}x dx = {pi_frac(V)}.', f'B1 must square y; B1 {pi_frac(V)}')


@n94.add('C3', (1, 2, 3, 4, 5), 'numerical')
def n94_calc(r, D):
    if D == 1:
        k = r.choice([2, 4, 6, 8, 10])
        a = r.choice([1, 4, 9])
        return Q(f'Evaluate ∫ from 0 to {a} of {k}/√x dx.', num(2 * k * math.isqrt(a)), f'M1 [{2 * k}√x]; A1 {2 * k * math.isqrt(a)} (limit at 0 is 0)')
    if D == 2:
        k, n, a = nz(r, 1, 9), r.randint(2, 4), r.choice([1, 2])
        v = Fr(k, (n - 1) * a ** (n - 1))
        return Q(f'Evaluate ∫ from {a} to ∞ of {k}/x{sup(n)} dx, showing how the infinite limit is dealt with.', num(v), f'M1 [{idx(integ([(k, -n)]))}]; M1 as x → ∞ term → 0; A1 {num(v)}')
    if D == 3:
        a, c = r.randint(1, 3), r.randint(1, 4)
        b = r.randint(1, 3)
        # y = a x + c from 0 to b about x-axis: π∫ (ax + c)² dx
        t = [(a * a, 2), (2 * a * c, 1), (c * c, 0)]
        V = defint(t, 0, b)
        return Q(f'The region bounded by y = {lin(a, c)}, the x-axis, the y-axis and the line x = {b} is rotated through 360° about the x-axis. Find the exact volume generated.', f'{pi_frac(V)}',
                 f'M1 π∫ ({lin(a, c)})² dx; A1 expands/integrates; A1 {pi_frac(V)}')
    if D == 4:
        # about y-axis: y = x² + k -> x² = y − k, from y = k to y = h
        k = r.randint(0, 3)
        h = k + r.randint(2, 6)
        V = Fr((h - k) ** 2, 2)
        return Q(f'The region bounded by the curve y = {quad(1, 0, k)}, the y-axis and the line y = {h}, for x ≥ 0, is rotated through 360° about the y-axis. Find the exact volume generated.', f'{pi_frac(V)}',
                 f'B1 x² = y{sg(-k) if k else ""}; M1 π∫ from {k} to {h} of (y{sg(-k) if k else ""}) dy; A1 {pi_frac(V)}')
    # D5: volume between two curves: y = x and y = x² rotated about x-axis from 0 to 1 scaled by k: y = kx, y = kx²
    k = r.randint(1, 4)
    V = Fr(k * k, 3) - Fr(k * k, 5)
    return Q(f'The region enclosed between the line y = {k if k > 1 else ""}x and the curve y = {k if k > 1 else ""}x² is rotated through 360° about the x-axis. Find the exact volume generated.', f'{pi_frac(V)}',
             f'B1 intersect at x = 0, 1; M1 π∫₀¹ ({k * k}x² − {k * k}x⁴) dx; A1 [{idx([(Fr(k * k, 3), 3), (Fr(-k * k, 5), 5)])}]; A1 {pi_frac(V)}'.replace('(1x² − 1x⁴)', '(x² − x⁴)'))


def n94_c4(r, D):
    k = r.choice([2, 3, 4, 6])
    a = r.choice([1, 2])
    b = r.choice([4, 6, 8])
    intro = f'The curve C has equation y = {k}/x for x > 0.'
    V1 = Fr(k * k) * (Fr(1, a) - Fr(1, b))
    parts = [
        P(f'Find the exact volume generated when the region bounded by C, the x-axis and the lines x = {a} and x = {b} is rotated through 360° about the x-axis.', f'{pi_frac(V1)}',
          f'M1 π∫ {k * k}/x² dx; A1 [−{k * k}/x]; A1 {pi_frac(V1)}'),
        P(f'Find the volume, in terms of π, generated when the region under C for x ≥ {a} is rotated about the x-axis.', f'{pi_frac(Fr(k * k, a))}', f'M1 improper integral to ∞; A1 {pi_frac(Fr(k * k, a))}'),
        P(f'Show that ∫ from {a} to ∞ of {k}/x dx does not converge, even though the volume does.', 'The integral grows without bound as the upper limit increases (it behaves like ln t).', 'B1 explains divergence'),
        P(f'Find the exact volume generated when the region bounded by C, the y-axis and the lines y = {k} and y = {2 * k} is rotated through 360° about the y-axis.', f'{pi_frac(Fr(k * k, k) - Fr(k * k, 2 * k))}',
          f'B1 x = {k}/y; M1 π∫ {k * k}/y² dy; A1 {pi_frac(Fr(k * k, k) - Fr(k * k, 2 * k))}'),
    ]
    return cmp_(r, intro, parts)


n94.add('C4', (2, 3, 4, 5))(n94_c4)

CHAPTERS[9] = [n91, n92, n93, n94]


# ================================================================ Chapter 10 Representation of data

def med(xs):
    xs = sorted(xs)
    n = len(xs)
    return Fr(xs[n // 2]) if n % 2 else Fr(xs[n // 2 - 1] + xs[n // 2], 2)


def quarts(xs):
    xs = sorted(xs)
    n = len(xs)
    lo, hi = xs[:n // 2], xs[(n + 1) // 2:]
    return med(lo), med(xs), med(hi)


def stemleaf(xs, unit='', key_note=None):
    xs = sorted(xs)
    stems = {}
    for x in xs:
        stems.setdefault(x // 10, []).append(x % 10)
    lo, hi = min(stems), max(stems)
    rows = []
    for s_ in range(lo, hi + 1):
        rows.append(f'{s_} | ' + ' '.join(str(l) for l in stems.get(s_, [])))
    k = xs[0]
    return '; '.join(rows) + f' (Key: {k // 10} | {k % 10} means {k}{unit})'


def backtoback(A, B, unit=''):
    A, B = sorted(A), sorted(B)
    sa, sb = {}, {}
    for x in A:
        sa.setdefault(x // 10, []).append(x % 10)
    for x in B:
        sb.setdefault(x // 10, []).append(x % 10)
    lo, hi = min(list(sa) + list(sb)), max(list(sa) + list(sb))
    rows = []
    for s_ in range(lo, hi + 1):
        left = ' '.join(str(l) for l in sorted(sa.get(s_, []), reverse=True))
        right = ' '.join(str(l) for l in sb.get(s_, []))
        rows.append(f'{left} | {s_} | {right}'.strip())
    return '; '.join(rows) + f' (Key: 5 | 3 | 2 means {35}{unit} for the left group and {32}{unit} for the right group)'


DATA_CTX = [('the times, in seconds, taken by {n} students to solve a puzzle', ' s'), ('the masses, in grams, of {n} apples from an orchard near {c}', ' g'),
            ('the scores of {n} students in a mathematics test in {c}', ''), ('the heights, in cm, of {n} seedlings in a greenhouse', ' cm'),
            ('the number of minutes {n} commuters in {c} spent travelling to work', ' min'), ('the pulse rates, in beats per minute, of {n} athletes', ' bpm')]


def rdata(r, n, lo=10, hi=79):
    return sorted(r.randint(lo, hi) for _ in range(n))


r101 = T('Stem-and-leaf diagrams and back-to-back stem-and-leaf diagrams', 'stem-and-leaf diagrams', 'back-to-back stem-and-leaf')
r101.fixed('C1', (1, 2), [
    ('Why must a stem-and-leaf diagram include a key?', 'to show how the stems and leaves combine to give the values', 'Without a key 3 | 5 could mean 35, 3.5 or 350.', ['to show the mean', 'to show the frequency', 'to order the leaves']),
    ('An advantage of a stem-and-leaf diagram over a grouped frequency table is that it', 'keeps the original data values', 'Each leaf is an actual value, so no information is lost.', ['shows the mean directly', 'can display any amount of data', 'removes outliers']),
    ('In a stem-and-leaf diagram with 23 values in order, the median is the', '12th value', '(23 + 1)/2 = 12.', ['11th value', '11.5th value', '23rd value']),
    ('In a back-to-back stem-and-leaf diagram, the leaves on the left-hand side are written', 'in increasing order moving away from the stem', 'Leaves increase outwards from the stem on both sides.', ['in decreasing order moving away from the stem', 'in any order', 'only for even values']),
])
r101.fixed('C2', (2, 3), [
    ('Explain why a back-to-back stem-and-leaf diagram is useful for comparing two data sets.', 'Both sets share the same stems, so their shapes, centres and spreads can be compared directly side by side while keeping all values.', 'B1 common stems; B1 compare shape/centre/spread directly [2]'),
    ('Explain why a stem-and-leaf diagram is not suitable for a data set of 500 values.', 'There would be far too many leaves on each stem, making it hard to draw and read; a grouped table or histogram is better.', 'B1 too many leaves; B1 alternative representation [2]'),
])


@r101.add('C1', (1, 2, 3))
def r101_c1(r, D):
    n = r.choice([11, 13, 15, 17, 19]) if D < 3 else r.choice([12, 14, 16, 18])
    xs = rdata(r, n)
    ctx, unit = r.choice(DATA_CTX)
    m = med(xs)
    kind = r.choice(['median', 'range'])
    stem = f'The stem-and-leaf diagram shows {ctx.format(n=n, c=city(r))}: {stemleaf(xs, unit)}. Find the {kind}.'
    if kind == 'median':
        return MC(r, stem, dn(m), [dn(Fr(sum(xs), n)) if Fr(sum(xs), n) != m else dn(m + 1), dn(xs[n // 2 + 1]), dn(Fr(xs[0] + xs[-1], 2)) if Fr(xs[0] + xs[-1], 2) != m else dn(m - 1), dn(xs[n // 2 - 1])], f'Median is the {"(n + 1)/2" if n % 2 else "mean of the two middle"} value(s): {dn(m)}.')
    R = xs[-1] - xs[0]
    return MC(r, stem, dn(R), [dn(xs[-1]), dn(xs[-1] - xs[1]), dn(xs[-2] - xs[0]), dn(R + 10)], f'Range = {xs[-1]} − {xs[0]} = {R}.')


@r101.add('C2', (2, 3, 4), 'explain')
def r101_cmp(r, D):
    n = r.choice([11, 13, 15])
    A = rdata(r, n, 20, 69)
    shift = r.choice([-12, -8, 8, 12])
    B = sorted(min(89, max(10, x + shift + r.randint(-4, 4))) for x in A)
    nm1, nm2 = two_people(r)
    qa, qb = quarts(A), quarts(B)
    ia, ib = qa[2] - qa[0], qb[2] - qb[0]
    return Q(f'The back-to-back stem-and-leaf diagram shows the scores of {n} students in class {nm1[0]} (left) and {n} students in class {nm2[0]} (right) in the same test: {backtoback(A, B)}. Compare the two sets of scores, giving two comparisons.',
             f'Class {nm1[0]} median {dn(qa[1])}, IQR {dn(ia)}; class {nm2[0]} median {dn(qb[1])}, IQR {dn(ib)}. Class {nm1[0] if qa[1] > qb[1] else nm2[0]} scored higher on average; class {nm1[0] if ia > ib else nm2[0]} scores were more spread out.',
             f'B1 comparison of an average (median {dn(qa[1])} vs {dn(qb[1])}) in context; B1 comparison of spread (IQR {dn(ia)} vs {dn(ib)} or range) in context')


@r101.add('C3', (1, 2, 3, 4, 5), 'numerical')
def r101_calc(r, D):
    n = r.choice([11, 13, 15, 17, 19, 21, 12, 14, 16])
    xs = rdata(r, n)
    ctx, unit = r.choice(DATA_CTX)
    c = city(r)
    q1, m, q3 = quarts(xs)
    sl = stemleaf(xs, unit)
    if D <= 2:
        return Q(f'The stem-and-leaf diagram shows {ctx.format(n=n, c=c)}: {sl}. Find the median and the range.', f'median {dn(m)}; range {xs[-1] - xs[0]}',
                 f'B1 median {dn(m)}; B1 range {xs[-1] - xs[0]}')
    if D == 3:
        return Q(f'The stem-and-leaf diagram shows {ctx.format(n=n, c=c)}: {sl}. Find the median and the interquartile range.', f'median {dn(m)}; IQR {dn(q3 - q1)}',
                 f'B1 median {dn(m)}; B1 Q1 = {dn(q1)}; B1 Q3 = {dn(q3)}; B1 IQR {dn(q3 - q1)}')
    if D == 4:
        lo_f, hi_f = q1 - Fr(3, 2) * (q3 - q1), q3 + Fr(3, 2) * (q3 - q1)
        xs2 = xs[:-1] + [min(99, int(hi_f) + r.randint(2, 12))]
        q1, m, q3 = quarts(xs2)
        hi_f = q3 + Fr(3, 2) * (q3 - q1)
        lo_f = q1 - Fr(3, 2) * (q3 - q1)
        outs = [x for x in xs2 if x > hi_f or x < lo_f]
        return Q(f'The stem-and-leaf diagram shows {ctx.format(n=n, c=c)}: {stemleaf(xs2, unit)}. An outlier is a value more than 1.5 × IQR above the upper quartile or below the lower quartile. Find the quartiles and determine whether there are any outliers.',
                 f'Q1 = {dn(q1)}, Q3 = {dn(q3)}; outliers: ' + (', '.join(str(x) for x in outs) if outs else 'none'),
                 f'B1 Q1 = {dn(q1)}; B1 Q3 = {dn(q3)}; M1 upper fence {dn(q3)} + 1.5 × {dn(q3 - q1)} = {dn(hi_f)}; A1 conclusion: ' + (', '.join(str(x) for x in outs) if outs else 'none'))
    A = rdata(r, n, 20, 69)
    B = sorted(min(89, max(10, x + r.choice([-10, 10]) + r.randint(-5, 5))) for x in A)
    qa, qb = quarts(A), quarts(B)
    return Q(f'The back-to-back stem-and-leaf diagram shows the reaction times, in hundredths of a second, of {n} people before (left) and after (right) drinking a cup of coffee: {backtoback(A, B)}. Find the median and interquartile range of each set and comment on what they show.',
             f'before: median {dn(qa[1])}, IQR {dn(qa[2] - qa[0])}; after: median {dn(qb[1])}, IQR {dn(qb[2] - qb[0])}; reaction times are {"longer" if qb[1] > qa[1] else "shorter"} on average after coffee',
             f'B1 both medians; B1 quartiles for one set; B1 both IQRs; B1 comment on average in context')


def r101_c4(r, D):
    n = r.choice([15, 17, 19, 16])
    A = rdata(r, n, 15, 75)
    B = sorted(min(89, max(10, x + r.choice([-9, 9, 12]) + r.randint(-6, 6))) for x in A)
    qa, qb = quarts(A), quarts(B)
    c1, c2 = r.sample(CITIES_, 2)
    intro = f'The back-to-back stem-and-leaf diagram shows the daily maximum temperature, in °F, on {n} days in {c1} (left) and in {c2} (right): {backtoback(A, B, "°F")}.'
    parts = [
        P(f'Find the median and the interquartile range for {c1}.', f'median {dn(qa[1])}; IQR {dn(qa[2] - qa[0])}', f'B1 median {dn(qa[1])}; B1 Q1 {dn(qa[0])}, Q3 {dn(qa[2])}; B1 IQR {dn(qa[2] - qa[0])}'),
        P(f'Find the median and the interquartile range for {c2}.', f'median {dn(qb[1])}; IQR {dn(qb[2] - qb[0])}', f'B1 median {dn(qb[1])}; B1 IQR {dn(qb[2] - qb[0])}'),
        P(f'Find the range of the temperatures in {c2}.', str(B[-1] - B[0]), f'B1 {B[-1] - B[0]}'),
        P('Make two comparisons between the temperatures in the two cities.', f'{c1 if qa[1] > qb[1] else c2} was warmer on average (higher median); {c1 if qa[2] - qa[0] > qb[2] - qb[0] else c2} had more variable temperatures (larger IQR).',
          'B1 average comparison in context; B1 spread comparison in context'),
    ]
    return cmp_(r, intro, parts)


CITIES_ = ['Nairobi', 'Lima', 'Dubai', 'Cape Town', 'Lisbon', 'Cairo', 'Hanoi', 'Doha', 'Jakarta', 'Toronto', 'Madrid', 'Seoul', 'Mumbai', 'Santiago']
r101.add('C4', (2, 3, 4, 5))(r101_c4)


# ---------------------------------------------------------------- 10.2 histograms
def rgroups(r):
    """Random unequal class boundaries and frequencies; frequency densities kept exact."""
    starts = r.choice([0, 10, 20, 40, 100, 150])
    widths = r.choice([[10, 10, 20, 20, 40], [5, 5, 10, 20, 30], [10, 20, 10, 30, 50], [20, 10, 10, 20, 40], [4, 6, 10, 20, 20], [5, 10, 15, 20, 30]])
    bounds = [starts]
    for w in widths:
        bounds.append(bounds[-1] + w)
    fds = [Fr(r.randint(2, 30), 10) * r.choice([1, 2, 5]) for _ in widths]
    freqs = [int(fd * w) for fd, w in zip(fds, widths)]
    freqs = [max(1, f) for f in freqs]
    return bounds, freqs


def gtable(bounds, freqs, var='t'):
    return '; '.join(f'{bounds[i]} ≤ {var} < {bounds[i + 1]}: {freqs[i]}' for i in range(len(freqs)))


HIST_CTX = [('the times, t minutes, that {n} customers spent in a shop in {c}', 't', 'minutes'), ('the masses, m kg, of {n} parcels at a depot in {c}', 'm', 'kg'),
            ('the lengths, l cm, of {n} fish caught near {c}', 'l', 'cm'), ('the distances, d km, travelled to work by {n} employees in {c}', 'd', 'km'),
            ('the ages, a years, of {n} visitors to a museum in {c}', 'a', 'years')]


r102 = T('Histograms with unequal class widths', 'histograms', 'unequal class widths', 'frequency density')
r102.fixed('C1', (1, 2), [
    ('In a histogram with unequal class widths, the height of each bar represents', 'frequency density', 'Frequency density = frequency ÷ class width.', ['frequency', 'cumulative frequency', 'class width']),
    ('In a histogram, the frequency of a class is proportional to', 'the area of its bar', 'Area = width × frequency density = frequency (× a constant).', ['the height of its bar', 'the width of its bar', 'the midpoint']),
    ('A class 20 ≤ x < 35 has frequency 45. Its frequency density is', '3', '45 ÷ 15 = 3.', ['45', '1.5', '2.25']),
    ('Which type of data is a histogram used for?', 'continuous data', 'Bars touch because the variable is continuous.', ['categorical data', 'qualitative data', 'paired data']),
])
r102.fixed('C2', (2, 3), [
    ('Explain why frequency density, rather than frequency, is plotted when class widths are unequal.', 'Wide classes would otherwise look too important; using frequency density makes the area of each bar proportional to its frequency.', 'B1 wide classes exaggerated; B1 area ∝ frequency [2]'),
    ('Explain why there are no gaps between the bars of a histogram.', 'The data are continuous and the classes are adjacent, so each class boundary is shared by neighbouring bars.', 'B1 continuous data; B1 adjacent class boundaries [2]'),
])


@r102.add('C1', (1, 2, 3))
def r102_c1(r, D):
    bounds, freqs = rgroups(r)
    i = r.randrange(len(freqs))
    w = bounds[i + 1] - bounds[i]
    fd = Fr(freqs[i], w)
    return MC(r, f'A class {bounds[i]} ≤ x < {bounds[i + 1]} in a grouped frequency table has frequency {freqs[i]}. Find the frequency density for this class.', dn(fd),
              [dn(Fr(w, freqs[i])), dn(freqs[i]), dn(Fr(freqs[i], bounds[i + 1])), dn(fd * 2)], f'{freqs[i]} ÷ {w} = {dn(fd)}.')


@r102.add('C2', (2, 3, 4), 'explain')
def r102_err(r, D):
    nm = person(r)
    bounds, freqs = rgroups(r)
    i = max(range(len(freqs)), key=lambda j: bounds[j + 1] - bounds[j])
    w = bounds[i + 1] - bounds[i]
    return Q(f'{nm} draws a histogram of the data {gtable(bounds, freqs, "x")} using the frequencies as the bar heights. Explain why the bar for {bounds[i]} ≤ x < {bounds[i + 1]} is misleading and state the correct height.',
             f'The class has width {w}, larger than others, so a height of {freqs[i]} makes its area too large; the height should be the frequency density {freqs[i]} ÷ {w} = {dn(Fr(freqs[i], w))}.',
             f'B1 area must represent frequency (wide class exaggerated); B1 frequency density {dn(Fr(freqs[i], w))}')


@r102.add('C3', (1, 2, 3, 4, 5), 'numerical')
def r102_calc(r, D):
    bounds, freqs = rgroups(r)
    n = sum(freqs)
    ctx, var, unit = r.choice(HIST_CTX)
    tab = gtable(bounds, freqs, var)
    desc = ctx.format(n=n, c=city(r))
    fds = [Fr(f, bounds[i + 1] - bounds[i]) for i, f in enumerate(freqs)]
    if D <= 2:
        return Q(f'The table summarises {desc}: {tab}. Calculate the frequency densities needed to draw a histogram.', ', '.join(dn(x) for x in fds),
                 'M1 frequency ÷ class width; A1 all correct')
    if D == 3:
        i, j = r.sample(range(len(freqs)), 2)
        h = r.choice([2, 3, 4, 5])
        hj = fds[j] * h / fds[i]
        return Q(f'The table summarises {desc}: {tab}. On a histogram the bar for {bounds[i]} ≤ {var} < {bounds[i + 1]} has height {h} cm. Find the height of the bar for {bounds[j]} ≤ {var} < {bounds[j + 1]}.',
                 f'{dn(hj)} cm' if Fr(hj).denominator in (1, 2, 4, 5, 10) else f'{n3(float(hj))} cm',
                 f'M1 frequency densities {dn(fds[i])} and {dn(fds[j])}; M1 scale {h}/{dn(fds[i])}; A1 {dn(hj) if Fr(hj).denominator in (1, 2, 4, 5, 10) else n3(float(hj))} cm')
    if D == 4:
        i = r.randrange(1, len(freqs) - 1)
        a = bounds[i] + (bounds[i + 1] - bounds[i]) // 2
        b = bounds[i + 2] if i + 2 < len(bounds) else bounds[-1]
        est = Fr(freqs[i] * (bounds[i + 1] - a), bounds[i + 1] - bounds[i]) + sum(freqs[k] for k in range(i + 1, len(freqs)) if bounds[k + 1] <= b)
        return Q(f'The table summarises {desc}: {tab}. Estimate the number of values with {a} ≤ {var} < {b}, assuming values are evenly spread within each class.', dn(est) if est.denominator == 1 else n3(float(est)),
                 f'M1 fraction of class {bounds[i]}–{bounds[i + 1]}: ({bounds[i + 1]} − {a})/{bounds[i + 1] - bounds[i]} × {freqs[i]}; M1 adds whole classes up to {b}; A1 {dn(est) if est.denominator == 1 else n3(float(est))}')
    # D5: missing frequency from fd and total
    i = r.randrange(len(freqs))
    known = [f for k, f in enumerate(freqs) if k != i]
    j = (i + 1) % len(freqs)
    return Q(f'A histogram represents {n} values of {var}. The classes are ' + ', '.join(f'{bounds[k]} ≤ {var} < {bounds[k + 1]}' for k in range(len(freqs))) +
             f'. The frequencies of all classes except {bounds[i]} ≤ {var} < {bounds[i + 1]} are ' + ', '.join(str(f) for f in known) +
             f' respectively. Find the frequency density of the class {bounds[i]} ≤ {var} < {bounds[i + 1]}, and the ratio of its bar height to that of the class {bounds[j]} ≤ {var} < {bounds[j + 1]}.',
             f'frequency {freqs[i]}; frequency density {dn(fds[i])}; ratio {dn(fds[i] / fds[j])}',
             f'M1 {n} − {sum(known)} = {freqs[i]}; A1 fd = {dn(fds[i])}; M1 fd of other class {dn(fds[j])}; A1 ratio {dn(fds[i] / fds[j])}')


def r102_c4(r, D):
    bounds, freqs = rgroups(r)
    n = sum(freqs)
    ctx, var, unit = r.choice(HIST_CTX)
    tab = gtable(bounds, freqs, var)
    fds = [Fr(f, bounds[i + 1] - bounds[i]) for i, f in enumerate(freqs)]
    mids = [Fr(bounds[i] + bounds[i + 1], 2) for i in range(len(freqs))]
    mean = sum(m * f for m, f in zip(mids, freqs)) / n
    mi = max(range(len(freqs)), key=lambda k: fds[k])
    cum = 0
    for k, f in enumerate(freqs):
        cum += f
        if cum >= Fr(n, 2):
            mc = k
            break
    intro = f'The table summarises {ctx.format(n=n, c=city(r))}: {tab}.'
    parts = [
        P('Calculate the frequency densities for a histogram.', ', '.join(dn(x) for x in fds), 'M1 f ÷ width; A1 all correct'),
        P('State the modal class.', f'{bounds[mi]} ≤ {var} < {bounds[mi + 1]}', 'B1 class with greatest frequency density'),
        P('Calculate an estimate of the mean.', n3(float(mean)), f'M1 uses midpoints {", ".join(dn(m) for m in mids)}; M1 Σfx/{n}; A1 {n3(float(mean))}'),
        P('State the class that contains the median.', f'{bounds[mc]} ≤ {var} < {bounds[mc + 1]}', f'B1 median is the {dn(Fr(n, 2))}th value: {bounds[mc]}–{bounds[mc + 1]}'),
        P('Explain why the mean is only an estimate.', 'The original values are not known; each value is assumed to be at the midpoint of its class.', 'B1 midpoints used / raw data unknown'),
    ]
    return cmp_(r, intro, parts)


r102.add('C4', (2, 3, 4, 5))(r102_c4)


# ---------------------------------------------------------------- 10.3 cumulative frequency and box plots
def cf_interp(bounds, freqs, target):
    cum = 0
    for i, f in enumerate(freqs):
        if cum + f >= target:
            return bounds[i] + Fr(target - cum, f) * (bounds[i + 1] - bounds[i])
        cum += f
    return Fr(bounds[-1])


r103 = T('Cumulative frequency graphs and box-and-whisker plots', 'cumulative frequency graphs', 'box-and-whisker plots')
r103.fixed('C1', (1, 2), [
    ('On a cumulative frequency graph, points are plotted at', 'the upper class boundaries', 'Cumulative frequency counts values up to the end of each class.', ['the class midpoints', 'the lower class boundaries', 'the frequency densities']),
    ('A box-and-whisker plot shows', 'the minimum, lower quartile, median, upper quartile and maximum', 'These are the five-number summary.', ['the mean and standard deviation', 'every data value', 'the mode and range']),
    ('For 80 values, the lower quartile is read from a cumulative frequency graph at a cumulative frequency of', '20', 'One quarter of 80.', ['40', '60', '25']),
    ('In a box plot, the length of the box represents', 'the interquartile range', 'The box runs from Q1 to Q3.', ['the range', 'the median', 'the standard deviation']),
])
r103.fixed('C2', (2, 3), [
    ('Explain one advantage and one disadvantage of a box-and-whisker plot compared with a histogram.', 'Advantage: it shows the median, quartiles and outliers clearly and is easy to compare between groups. Disadvantage: it hides the detailed shape of the distribution (e.g. two peaks).', 'B1 valid advantage; B1 valid disadvantage [2]'),
    ('Explain why the median read from a cumulative frequency graph of grouped data is an estimate.', 'The raw values are unknown; the graph assumes values are spread evenly within each class (straight lines or a smooth curve between points).', 'B1 raw data unknown; B1 assumption of even spread [2]'),
])


@r103.add('C1', (1, 2, 3))
def r103_c1(r, D):
    a = r.randint(5, 30)
    q1 = a + r.randint(5, 15)
    m = q1 + r.randint(3, 12)
    q3 = m + r.randint(3, 15)
    b = q3 + r.randint(5, 20)
    kind = r.choice(['iqr', 'range']) if D < 3 else 'out'
    summ = f'minimum {a}, lower quartile {q1}, median {m}, upper quartile {q3}, maximum {b}'
    if kind == 'iqr':
        return MC(r, f'A box-and-whisker plot has {summ}. Find the interquartile range.', str(q3 - q1), [str(b - a), str(q3 - m), str(m - q1 + 1), str(b - q1)], f'IQR = {q3} − {q1} = {q3 - q1}.')
    if kind == 'range':
        return MC(r, f'A box-and-whisker plot has {summ}. Find the range.', str(b - a), [str(q3 - q1), str(b), str(b - m), str(q3 - a)], f'Range = {b} − {a} = {b - a}.')
    fence = q3 + Fr(3, 2) * (q3 - q1)
    return MC(r, f'Data have lower quartile {q1} and upper quartile {q3}. Using the 1.5 × IQR rule, above which value is a data value an outlier?', dn(fence),
              [dn(q3 + (q3 - q1)), dn(q3 + 2 * (q3 - q1)), dn(Fr(3, 2) * (q3 - q1)), dn(fence + q1)], f'{q3} + 1.5 × {q3 - q1} = {dn(fence)}.')


@r103.add('C2', (2, 3, 4), 'explain')
def r103_cmp(r, D):
    g1, g2 = r.choice([('Boys', 'Girls'), ('Year 10', 'Year 11'), ('Team A', 'Team B'), ('Morning shift', 'Evening shift'), ('Group P', 'Group Q')])
    s1 = sorted(r.sample(range(10, 90), 5))
    s2 = sorted(r.sample(range(10, 90), 5))
    i1, i2 = s1[3] - s1[1], s2[3] - s2[1]
    if s1[2] == s2[2] or i1 == i2:
        return None
    what = r.choice(['test scores', 'times in seconds to complete a task', 'distances in metres in a long-jump competition'])
    return Q(f'Box-and-whisker plots of {what} give these summaries. {g1}: min {s1[0]}, Q1 {s1[1]}, median {s1[2]}, Q3 {s1[3]}, max {s1[4]}. {g2}: min {s2[0]}, Q1 {s2[1]}, median {s2[2]}, Q3 {s2[3]}, max {s2[4]}. Make two comparisons between the groups.',
             f'Median {g1} {s1[2]} vs {g2} {s2[2]}: {g1 if s1[2] > s2[2] else g2} higher on average. IQR {g1} {i1} vs {g2} {i2}: {g1 if i1 > i2 else g2} more varied.',
             'B1 compares medians in context; B1 compares IQR (or range) in context')


@r103.add('C3', (1, 2, 3, 4, 5), 'numerical')
def r103_calc(r, D):
    bounds, freqs = rgroups(r)
    n = sum(freqs)
    ctx, var, unit = r.choice(HIST_CTX)
    desc = ctx.format(n=n, c=city(r))
    tab = gtable(bounds, freqs, var)
    cum = [sum(freqs[:i + 1]) for i in range(len(freqs))]
    if D <= 2:
        return Q(f'The table summarises {desc}: {tab}. Write down the cumulative frequencies, and state the coordinates of the points that would be plotted for a cumulative frequency graph.', ', '.join(str(c) for c in cum) + '; points ' + ', '.join(f'({bounds[i + 1]}, {cum[i]})' for i in range(len(cum))),
                 'B1 cumulative frequencies; B1 plotted at upper boundaries with (' + str(bounds[0]) + ', 0)')
    m = cf_interp(bounds, freqs, Fr(n, 2))
    q1, q3 = cf_interp(bounds, freqs, Fr(n, 4)), cf_interp(bounds, freqs, Fr(3 * n, 4))
    f3 = lambda x: n3(float(x))
    if D == 3:
        return Q(f'The table summarises {desc}: {tab}. By linear interpolation within the classes, estimate the median.', f3(m),
                 f'B1 cumulative frequencies; M1 locates the {dn(Fr(n, 2))}th value in the correct class; A1 {f3(m)}')
    if D == 4:
        return Q(f'The table summarises {desc}: {tab}. Using linear interpolation, estimate the lower quartile, upper quartile and interquartile range.', f'Q1 ≈ {f3(q1)}; Q3 ≈ {f3(q3)}; IQR ≈ {f3(q3 - q1)}',
                 f'B1 cumulative frequencies; M1 positions {dn(Fr(n, 4))} and {dn(Fr(3 * n, 4))}; A1 Q1 {f3(q1)}; A1 Q3 {f3(q3)}; A1 IQR {f3(q3 - q1)}')
    v = bounds[2] + (bounds[3] - bounds[2]) // 2
    below = freqs[0] + freqs[1] + Fr(freqs[2] * (v - bounds[2]), bounds[3] - bounds[2])
    pc = 100 * (n - below) / n
    return Q(f'The table summarises {desc}: {tab}. Estimate the percentage of values that are at least {v}.', f'{n3(float(pc))}%',
             f'M1 {freqs[0] + freqs[1]} + ({v} − {bounds[2]})/{bounds[3] - bounds[2]} × {freqs[2]} = {f3(below)} below; M1 ({n} − {f3(below)})/{n} × 100; A1 {n3(float(pc))}%')


def r103_c4(r, D):
    n = r.choice([15, 19, 23, 13])
    xs = rdata(r, n, 20, 89)
    q1, m, q3 = quarts(xs)
    ctx, unit = r.choice(DATA_CTX)
    c = city(r)
    iq = q3 - q1
    up = q3 + Fr(3, 2) * iq
    lo = q1 - Fr(3, 2) * iq
    outs = [x for x in xs if x > up or x < lo]
    intro = f'The values below are {ctx.format(n=n, c=c)}, in order: ' + ', '.join(str(x) for x in xs) + '.'
    parts = [
        P('Find the median and the quartiles.', f'Q1 = {dn(q1)}, median {dn(m)}, Q3 = {dn(q3)}', f'B1 median {dn(m)}; B1 Q1 {dn(q1)}; B1 Q3 {dn(q3)}'),
        P('Show that there are no outliers, or identify any outliers, using the 1.5 × IQR rule.', 'outliers: ' + (', '.join(map(str, outs)) if outs else 'none'),
          f'M1 fences {dn(lo)} and {dn(up)}; A1 conclusion'),
        P('Describe the box-and-whisker plot you would draw.', f'whiskers from {xs[0]} to {xs[-1]} (or to the most extreme non-outliers), box from {dn(q1)} to {dn(q3)} with a line at {dn(m)}', 'B1 box Q1 to Q3 with median; B1 whiskers to extremes'),
        P('State, with a reason, whether the mean or the median is a better average for these data.',
          ('the median, because ' + ('there are outliers that would distort the mean' if outs else f'the data are skewed (mean {n3(sum(xs) / n)}, median {dn(m)})')) if (outs or abs(Fr(sum(xs), n) - m) > iq / 10) else f'the mean, because the data are roughly symmetric (mean {n3(sum(xs) / n)}, median {dn(m)}) with no outliers, and it uses all the values',
          'B1 choice with valid reason linked to skew/outliers'),
    ]
    return cmp_(r, intro, parts)


r103.add('C4', (2, 3, 4, 5))(r103_c4)


# ---------------------------------------------------------------- 10.4 choosing representations
r104 = T('Choosing and comparing data representations', 'choosing and comparing data representations', 'data representations')
r104.fixed('C1', (1, 2), [
    ('Which representation is most suitable for showing the shape of a large set of continuous data?', 'a histogram', 'Histograms summarise large continuous data sets.', ['a stem-and-leaf diagram', 'a pie chart', 'a list of values']),
    ('Which representation keeps every original value?', 'a stem-and-leaf diagram', 'Each leaf records a value exactly.', ['a histogram', 'a box-and-whisker plot', 'a cumulative frequency graph']),
    ('Which representation is best for comparing the medians and spreads of several groups at once?', 'box-and-whisker plots on a common scale', 'Medians, quartiles and ranges can be read off directly.', ['separate pie charts', 'a single stem-and-leaf diagram', 'a frequency table']),
    ('Which representation allows estimates of percentiles to be read directly?', 'a cumulative frequency graph', 'Percentiles are read at the corresponding cumulative frequency.', ['a histogram', 'a bar chart', 'a stem-and-leaf diagram with no key']),
])
REPS = [
    ('the heights of 600 adults', 'histogram (or cumulative frequency graph)', 'large set of continuous data; shape of distribution is shown'),
    ('the marks of 18 students in a quiz', 'stem-and-leaf diagram', 'small data set; keeps the raw data and shows shape'),
    ('the journey times of two groups of commuters', 'back-to-back stem-and-leaf diagram or two box plots on the same scale', 'direct comparison of two data sets'),
    ('the percentage of students in a school who passed their exam', 'cumulative frequency graph', 'percentiles and proportions above a mark can be read off'),
    ('the masses of 250 parcels, where the median and quartiles are needed', 'cumulative frequency graph then box plot', 'quartiles estimated from the graph; box plot summarises them'),
    ('the waiting times at five clinics, to compare medians and spreads', 'box-and-whisker plots on a common scale', 'easy to compare medians, IQRs and outliers'),
]
r104.fixed('C2', (2, 3), [(f'Suggest, with a reason, a suitable diagram to represent {a}.', f'{b}: {c}.', 'B1 suitable diagram; B1 valid reason [2]') for a, b, c in REPS])


@r104.add('C1', (1, 2, 3))
def r104_c1(r, D):
    n = r.choice([12, 15, 20, 25, 40, 60, 120, 300, 500, 1000])
    what = r.choice(['heights of trees', 'reaction times', 'daily rainfall amounts', 'masses of eggs', 'times to run 100 m'])
    if n <= 30:
        c, ds = 'a stem-and-leaf diagram', ['a pie chart', 'a cumulative frequency graph of grouped data', 'a bar chart of individual values']
        why = 'small data set, so the raw values can be kept and the shape seen.'
    else:
        c, ds = 'a histogram', ['a stem-and-leaf diagram', 'a list of the values', 'a pie chart']
        why = 'large continuous data set: group the data and show the shape.'
    return MC(r, f'A researcher has recorded the {what} for {n} cases in {city(r)}. Which representation is most suitable to show the distribution?', c, ds, f'{c}: {why}')


@r104.add('C2', (2, 3, 4), 'explain')
def r104_err(r, D):
    nm = person(r)
    n = r.choice([200, 350, 480, 800, 1200])
    fr = r.choice(['stem', 'bar', 'pie'])
    if fr == 'stem':
        return Q(f'{nm} wants to display the masses of {n} newborn babies in hospitals in {city(r)} and chooses a stem-and-leaf diagram. Explain why this is not a good choice and suggest a better representation.',
                 f'With {n} values there would be too many leaves to draw or read. A histogram or cumulative frequency graph of grouped data is better.', 'B1 too many values; B1 histogram/cumulative frequency suggested')
    if fr == 'bar':
        return Q(f'{nm} draws a bar chart with gaps between the bars to show the times taken by {n} runners in a marathon in {city(r)}, grouped in unequal classes. Give two criticisms of this diagram.',
                 'Time is continuous, so the bars should touch; with unequal class widths frequency density should be plotted (a histogram), not frequency.', 'B1 continuous data so no gaps; B1 unequal widths need frequency density')
    return Q(f'{nm} uses a pie chart to show the heights of {n} students in a school in {city(r)}, with one sector for each different height. Explain why this is unsuitable and suggest a better diagram.',
             'Height is continuous with many distinct values, so the pie chart would have too many sectors and would not show the distribution. A histogram (or cumulative frequency graph/box plot) is better.',
             'B1 continuous data with many values; B1 suitable alternative')


@r104.add('C3', (1, 2, 3, 4, 5), 'numerical')
def r104_calc(r, D):
    n = r.choice([11, 13, 15])
    A = rdata(r, n, 20, 79)
    q1, m, q3 = quarts(A)
    mean = Fr(sum(A), n)
    return Q(f'The {n} values ' + ', '.join(map(str, A)) + f' are to be summarised. Find the median, the interquartile range and the mean, and state which pair of measures a box plot displays.',
             f'median {dn(m)}; IQR {dn(q3 - q1)}; mean {n3(float(mean))}; a box plot shows the median and IQR (not the mean)',
             f'B1 median {dn(m)}; B1 IQR {dn(q3 - q1)}; B1 mean {n3(float(mean))}; B1 box plot shows median/quartiles')


def r104_c4(r, D):
    n = r.choice([11, 13, 15])
    A = rdata(r, n, 30, 79)
    B = sorted(min(89, max(10, x + r.choice([-10, -6, 6, 10]) + r.randint(-4, 4))) for x in A)
    qa, qb = quarts(A), quarts(B)
    intro = f'Two groups of {n} students sat the same test. Group X scores: ' + ', '.join(map(str, A)) + '. Group Y scores: ' + ', '.join(map(str, B)) + '.'
    parts = [
        P('Suggest a suitable diagram to compare the two groups, with a reason.', 'back-to-back stem-and-leaf diagram (small data sets, keeps values, direct comparison) or two box plots', 'B1 suitable diagram; B1 reason'),
        P('Find the median and IQR of each group.', f'X: median {dn(qa[1])}, IQR {dn(qa[2] - qa[0])}; Y: median {dn(qb[1])}, IQR {dn(qb[2] - qb[0])}', 'B1 medians; B1 quartiles; B1 IQRs'),
        P('Compare the performance of the two groups.', f'{"X" if qa[1] > qb[1] else "Y"} has the higher median, so performed better on average; {"X" if qa[2] - qa[0] > qb[2] - qb[0] else "Y"} is more spread out.', 'B1 average comparison; B1 spread comparison'),
    ]
    return cmp_(r, intro, parts)


r104.add('C4', (2, 3, 4, 5))(r104_c4)

CHAPTERS[10] = [r101, r102, r103, r104]


# ================================================================ Chapter 11 Measures of central tendency

def ftab(xs, fs, var='x'):
    return f'{var}: ' + ', '.join(map(str, xs)) + '; frequency: ' + ', '.join(map(str, fs))


def fmedian(xs, fs):
    n = sum(fs)
    vals = []
    for x, f in zip(xs, fs):
        vals += [x] * f
    return med(vals)


DISC_CTX = [('the number of goals scored by a football team in {n} matches', 'goals'), ('the number of people in each of {n} cars passing a junction in {c}', 'people'),
            ('the number of books read last month by {n} students in {c}', 'books'), ('the number of siblings of {n} children in a school in {c}', 'siblings'),
            ('the number of emails received by {n} office workers in {c} in one hour', 'emails'), ('the shoe sizes of {n} customers in a shop in {c}', 'size')]


def rdisc(r):
    x0 = r.choice([0, 1, 2, 3])
    k = r.choice([4, 5, 6])
    xs = list(range(x0, x0 + k))
    fs = [r.randint(1, 15) for _ in xs]
    return xs, fs


m111 = T('Mean, median and mode of ungrouped and grouped data', 'mean median mode', 'grouped data', 'estimate of the mean')
m111.fixed('C1', (1, 2), [
    ('When estimating the mean from a grouped frequency table, each value is assumed to equal', 'the midpoint of its class', 'Mean ≈ Σfx/Σf with x the class midpoint.', ['the lower class boundary', 'the upper class boundary', 'the class width']),
    ('For grouped data with unequal class widths, the modal class is the class with the highest', 'frequency density', 'Wider classes contain more values simply because they are wider.', ['frequency', 'class width', 'cumulative frequency']),
    ('For 40 values in order, the median is', 'the mean of the 20th and 21st values', 'n is even, so take the mean of the two middle values.', ['the 20th value', 'the 21st value', 'the 20.5th value rounded down']),
    ('Which measure of central tendency can be used for categorical data?', 'the mode', 'Only the mode makes sense for non-numerical categories.', ['the mean', 'the median', 'the interquartile range']),
])
m111.fixed('C2', (2, 3), [
    ('Explain why the mean calculated from a grouped frequency table is only an estimate.', 'The exact data values are not known; each value is assumed to lie at the midpoint of its class.', 'B1 raw data unknown; B1 midpoints assumed [2]'),
    ('Explain why the median of grouped data found by interpolation is only an estimate.', 'Interpolation assumes the values are spread evenly within the median class, which may not be true.', 'B1 values assumed evenly spread in class; B1 actual values unknown [2]'),
])


@m111.add('C1', (1, 2, 3))
def m111_c1(r, D):
    n = r.choice([7, 8, 9, 10, 11])
    xs = sorted(r.randint(1, 30) for _ in range(n))
    kind = r.choice(['mean', 'median', 'mode'])
    if kind == 'mode':
        x = r.choice(xs)
        xs = sorted(xs + [x, x])
        cnt = {v: xs.count(v) for v in xs}
        top = max(cnt.values())
        if list(cnt.values()).count(top) > 1:
            return None
        mo = max(cnt, key=cnt.get)
        return MC(r, 'Find the mode of the data ' + ', '.join(map(str, xs)) + '.', str(mo), [dn(med(xs)), dn(Fr(sum(xs), len(xs))), str(top), str(xs[-1])], f'{mo} occurs {top} times, more than any other value.')
    if kind == 'median':
        r.shuffle(xs)
        m = med(xs)
        return MC(r, 'Find the median of ' + ', '.join(map(str, xs)) + '.', dn(m), [dn(xs[len(xs) // 2]), dn(Fr(sum(xs), n)), dn(sorted(xs)[n // 2 - 1]), dn(m + 1)], f'In order the middle value(s) give {dn(m)}.')
    mean = Fr(sum(xs), n)
    return MC(r, 'Find the mean of ' + ', '.join(map(str, xs)) + (' correct to 3 significant figures.' if mean.denominator > 2 else '.'), dn(mean),
              [dn(Fr(sum(xs), n - 1)), dn(med(xs)), dn(Fr(sum(xs), n + 1)), dn(mean + 1)], f'Σx = {sum(xs)}, so mean = {sum(xs)}/{n} = {dn(mean)}.')


@m111.add('C1', (2, 3))
def m111_c1b(r, D):
    xs, fs = rdisc(r)
    n = sum(fs)
    mean = Fr(sum(x * f for x, f in zip(xs, fs)), n)
    return MC(r, f'The frequency table shows {ftab(xs, fs)}. Find the mean of x' + (', correct to 3 significant figures.' if mean.denominator not in (1, 2, 4, 5) else '.'), dn(mean),
              [dn(Fr(sum(xs), len(xs))), dn(Fr(n, len(xs))), dn(Fr(sum(x * f for x, f in zip(xs, fs)), len(xs))), dn(fmedian(xs, fs) + Fr(1, 2))],
              f'Σfx = {sum(x * f for x, f in zip(xs, fs))}, Σf = {n}; mean = {dn(mean)}.')


@m111.add('C2', (2, 3, 4), 'explain')
def m111_err(r, D):
    bounds, freqs = rgroups(r)
    var = r.choice(['t', 'm', 'x'])
    nm = person(r)
    mids = [Fr(bounds[i] + bounds[i + 1], 2) for i in range(len(freqs))]
    n = sum(freqs)
    mean = sum(m * f for m, f in zip(mids, freqs)) / n
    wrong = sum(mids) / len(mids)
    kind = r.choice(['mid', 'upper'])
    if kind == 'mid':
        return Q(f'For the grouped data {gtable(bounds, freqs, var)}, {nm} estimates the mean as the average of the class midpoints, giving {dn(wrong)}. Explain the error and find a correct estimate of the mean.',
                 f'The midpoints must be weighted by the frequencies: mean ≈ Σfx/Σf = {n3(float(mean))}.',
                 f'B1 frequencies ignored; M1 Σfx/Σf with midpoints; A1 {n3(float(mean))}')
    up = Fr(sum(bounds[i + 1] * freqs[i] for i in range(len(freqs))), n)
    return Q(f'For the grouped data {gtable(bounds, freqs, var)}, {nm} estimates the mean using the upper class boundaries, obtaining {dn(up)}. Explain why this overestimates the mean and find a better estimate.',
             f'Upper boundaries are the largest possible values in each class, so the estimate is too high; using midpoints gives {n3(float(mean))}.',
             f'B1 upper boundaries are maximum values; M1 midpoints with Σfx/Σf; A1 {n3(float(mean))}')


@m111.add('C2', (2, 3, 4), 'explain')
def m111_cmp(r, D):
    xs, fs = rdisc(r)
    _, ctxw = r.choice(DISC_CTX)
    n = sum(fs)
    mean = Fr(sum(x * f for x, f in zip(xs, fs)), n)
    md = fmedian(xs, fs)
    mo = xs[fs.index(max(fs))]
    if fs.count(max(fs)) > 1:
        return None
    nm = person(r)
    claim = r.choice(['mean', 'median'])
    val = mean if claim == 'mean' else md
    return Q(f'A frequency table of the number of {ctxw} gives {ftab(xs, fs)}. {nm} says that the mode is {max(fs)}. Explain the mistake, and find the mode and the {claim}.',
             f'{max(fs)} is the highest frequency, not a value of x; the mode is {mo} and the {claim} is {dn(val)}.',
             f'B1 mode is the value with the highest frequency, {mo}; B1 {claim} {dn(val)}')


@m111.add('C3', (1, 2, 3, 4, 5), 'numerical')
def m111_calc(r, D):
    if D <= 2:
        xs, fs = rdisc(r)
        ctx, _ = r.choice(DISC_CTX)
        n = sum(fs)
        sfx = sum(x * f for x, f in zip(xs, fs))
        mean = Fr(sfx, n)
        md = fmedian(xs, fs)
        return Q(f'The table shows {ctx.format(n=n, c=city(r))}: {ftab(xs, fs)}. Calculate the mean and find the median.',
                 f'mean {dn(mean)}; median {dn(md)}', f'M1 Σfx = {sfx}; A1 mean {dn(mean)}; B1 median {dn(md)}')
    if D == 3:
        xs, fs = rdisc(r)
        i = r.randrange(len(xs))
        n = sum(fs)
        sfx = sum(x * f for x, f in zip(xs, fs))
        mean = Fr(sfx, n)
        if mean.denominator not in (1, 2, 4, 5, 10, 20, 25):
            return None
        tab = f'x: ' + ', '.join(map(str, xs)) + '; frequency: ' + ', '.join('k' if j == i else str(f) for j, f in enumerate(fs))
        return Q(f'The frequency table is {tab}. The mean of x is {dn(mean)}. Find the value of k.', str(fs[i]),
                 f'M1 Σfx/Σf = {dn(mean)} with k; M1 solves linear equation; A1 k = {fs[i]}')
    bounds, freqs = rgroups(r)
    ctx, var, unit = r.choice(HIST_CTX)
    n = sum(freqs)
    mids = [Fr(bounds[i] + bounds[i + 1], 2) for i in range(len(freqs))]
    mean = sum(m * f for m, f in zip(mids, freqs)) / n
    m = cf_interp(bounds, freqs, Fr(n, 2))
    if D == 4:
        return Q(f'The table summarises {ctx.format(n=n, c=city(r))}: {gtable(bounds, freqs, var)}. Calculate an estimate of the mean.', f'{n3(float(mean))} {unit}',
                 f'M1 midpoints {", ".join(dn(x) for x in mids)}; M1 Σfx/{n}; A1 {n3(float(mean))}')
    return Q(f'The table summarises {ctx.format(n=n, c=city(r))}: {gtable(bounds, freqs, var)}. Calculate estimates of the mean and of the median.', f'mean {n3(float(mean))}; median {n3(float(m))}',
             f'M1 midpoints used; A1 mean {n3(float(mean))}; M1 interpolation in median class; A1 median {n3(float(m))}')


@m111.add('C3', (2, 3, 4), 'numerical')
def m111_new(r, D):
    n = r.randint(8, 30)
    mean = Fr(r.randint(20, 90 * 10), 10)
    kind = r.choice(['add', 'remove', 'target'])
    if kind == 'add':
        x = r.randint(10, 120)
        nm = (mean * n + x) / (n + 1)
        return Q(f'The mean mass of {n} parcels is {dn(mean)} kg. Another parcel of mass {x} kg is added. Find the new mean mass.', f'{dn(nm) if nm.denominator in (1, 2, 4, 5, 10, 20, 25, 50) else n3(float(nm))} kg',
                 f'M1 total {dn(mean * n)}; M1 ({dn(mean * n)} + {x}) ÷ {n + 1}; A1 {dn(nm) if nm.denominator in (1, 2, 4, 5, 10, 20, 25, 50) else n3(float(nm))}')
    if kind == 'remove':
        nm2 = Fr(r.randint(20, 900), 10)
        x = mean * n - nm2 * (n - 1)
        if x <= 0 or x.denominator not in (1, 2, 5, 10):
            return None
        return Q(f'The mean score of {n} students in a test is {dn(mean)}. When one student\'s score is removed the mean of the remaining scores is {dn(nm2)}. Find the score that was removed.', dn(x),
                 f'M1 {n} × {dn(mean)} = {dn(mean * n)}; M1 {n - 1} × {dn(nm2)} = {dn(nm2 * (n - 1))}; A1 {dn(x)}')
    n = r.randint(4, 12)
    mean = Fr(r.randint(400, 800), 10)
    tgt = mean + r.choice([1, 2, 3])
    x = tgt * (n + 1) - mean * n
    if x > 100:
        return None
    return Q(f'{person(r)} has a mean score of {dn(mean)} in {n} quizzes, each marked out of 100. Find the score needed in the next quiz to raise the mean to {dn(tgt)}.', dn(x),
             f'M1 {n + 1} × {dn(tgt)} − {n} × {dn(mean)}; A1 {dn(x)}')


def m111_c4(r, D):
    bounds, freqs = rgroups(r)
    ctx, var, unit = r.choice(HIST_CTX)
    n = sum(freqs)
    mids = [Fr(bounds[i] + bounds[i + 1], 2) for i in range(len(freqs))]
    sfx = sum(m * f for m, f in zip(mids, freqs))
    mean = sfx / n
    md = cf_interp(bounds, freqs, Fr(n, 2))
    fds = [Fr(freqs[i], bounds[i + 1] - bounds[i]) for i in range(len(freqs))]
    mc = fds.index(max(fds))
    if fds.count(max(fds)) > 1:
        return None
    cum = 0
    for i, f in enumerate(freqs):
        cum += f
        if cum >= Fr(n, 2):
            medc = i
            break
    intro = f'The table summarises {ctx.format(n=n, c=city(r))}: {gtable(bounds, freqs, var)}.'
    parts = [
        P('Calculate an estimate of the mean.', f'{n3(float(mean))} {unit}', f'M1 midpoints; M1 Σfx = {dn(sfx)} divided by {n}; A1 {n3(float(mean))}'),
        P('State the class that contains the median.', f'{bounds[medc]} ≤ {var} < {bounds[medc + 1]}', f'B1 the {dn(Fr(n, 2))}th value lies in {bounds[medc]}–{bounds[medc + 1]}'),
        P('Use interpolation to estimate the median.', n3(float(md)), f'M1 cumulative frequencies; M1 interpolation in median class; A1 {n3(float(md))}'),
        P('Identify the modal class, giving a reason.', f'{bounds[mc]} ≤ {var} < {bounds[mc + 1]}, since it has the highest frequency density ({dn(fds[mc])})', 'B1 class; B1 reason: highest frequency density (unequal widths)'),
        P('Explain why the estimate of the mean is not exact.', 'The raw data are not known, so each value is taken at its class midpoint.', 'B1 midpoints used / raw data unknown'),
    ]
    return cmp_(r, intro, parts)


m111.add('C4', (2, 3, 4, 5))(m111_c4)


@m111.add('C4', (3, 4, 5))
def m111_c4b(r, D):
    xs, fs = rdisc(r)
    ctx, w = r.choice(DISC_CTX)
    n = sum(fs)
    sfx = sum(x * f for x, f in zip(xs, fs))
    mean = Fr(sfx, n)
    md = fmedian(xs, fs)
    if fs.count(max(fs)) > 1:
        return None
    mo = xs[fs.index(max(fs))]
    extra = r.randint(2, 6)
    xe = xs[-1] + r.randint(2, 8)
    nmean = Fr(sfx + extra * xe, n + extra)
    intro = f'The table shows {ctx.format(n=n, c=city(r))}: {ftab(xs, fs)}.'
    parts = [
        P('Find the mode and the median.', f'mode {mo}; median {dn(md)}', f'B1 mode {mo}; B1 median {dn(md)}'),
        P('Calculate the mean.', dn(mean), f'M1 Σfx = {sfx}; A1 {dn(mean)}'),
        P(f'A further {extra} observations, each equal to {xe}, are added to the data. Calculate the new mean.', dn(nmean), f'M1 ({sfx} + {extra} × {xe}) ÷ {n + extra}; A1 {dn(nmean)}'),
        P(f'State, with a reason, which average would be least affected by adding {extra} observations each equal to {xe}.', 'the mode (or median): it depends only on the most common or middle values, whereas the mean uses every value',
          'B1 mode or median; B1 reason: mean affected by every value'),
    ]
    return cmp_(r, intro, parts)


m112 = T('Using Σ notation and coded data for the mean', 'sigma notation', 'coded data', 'Σx')
m112.fixed('C1', (1, 2), [
    ('If Σ(x − 20) = 0 for a set of data, the mean of x is', '20', 'Σ(x − 20) = Σx − 20n = 0, so x̄ = 20.', ['0', '−20', '10']),
    ('For n values, Σ(x − a) is equal to', 'Σx − na', 'Subtract a from each of the n values.', ['Σx − a', 'Σx + na', 'nΣx − a']),
    ('If y = x − 50 for every value, then the mean of y equals', 'the mean of x minus 50', 'Subtracting a constant shifts the mean by the same amount.', ['the mean of x', 'the mean of x plus 50', '50 times the mean of x']),
    ('If y = (x − 100)/5 and ȳ = 3, then x̄ is', '115', 'x̄ = 5ȳ + 100.', ['103', '85', '20.6']),
])
m112.fixed('C2', (2, 3), [
    ('Explain why coding data by subtracting a constant can make calculations of the mean easier.', 'The coded values are smaller and closer to zero, so sums are easier; the mean is then recovered by adding the constant back.', 'B1 smaller numbers; B1 add constant back to mean [2]'),
    ('Explain why Σ(x − x̄) = 0 for any data set.', 'Σ(x − x̄) = Σx − n x̄ = Σx − Σx = 0, since x̄ = Σx/n.', 'M1 expands to Σx − nx̄; A1 uses nx̄ = Σx [2]'),
])


@m112.add('C1', (1, 2, 3))
def m112_c1(r, D):
    n = r.randint(8, 60)
    a = r.choice([10, 20, 25, 30, 40, 50, 60, 100, 150, 200])
    s = r.randint(-5 * n, 5 * n)
    if s == 0:
        return None
    mean = a + Fr(s, n)
    return MC(r, f'For {n} values of x, Σ(x − {a}) = {num(s)}. Find the mean of x' + (', correct to 3 significant figures.' if mean.denominator not in (1, 2, 4, 5, 10, 20, 25, 50) else '.'), dn(mean),
              [dn(Fr(s, n)), dn(a - Fr(s, n)), dn(Fr(s, n) + Fr(a, n)), dn(Fr(s + a, n))], f'x̄ = {a} + {pn(s)}/{n} = {dn(mean)}.')


@m112.add('C1', (1, 2))
def m112_c1b(r, D):
    n = r.randint(10, 80)
    mean = Fr(r.randint(50, 999), 10)
    sx = mean * n
    return MC(r, f'For {n} observations, the mean is {dn(mean)}. Find Σx.', dn(sx), [dn(mean / n), dn(sx + mean), dn(mean * (n - 1)), dn(sx / 10)], f'Σx = n x̄ = {n} × {dn(mean)} = {dn(sx)}.')


@m112.add('C2', (2, 3, 4), 'explain')
def m112_err(r, D):
    n = r.randint(10, 50)
    a = r.choice([20, 30, 40, 50, 60, 100])
    s = r.randint(-4 * n, 4 * n)
    if s == 0:
        return None
    nm = person(r)
    mean = a + Fr(s, n)
    kind = r.choice(['forgot', 'sign'])
    if kind == 'forgot':
        return Q(f'For {n} values, Σ(x − {a}) = {num(s)}. {nm} says the mean of x is {dn(Fr(s, n))}. Explain the error and find the correct mean.',
                 f'{dn(Fr(s, n))} is the mean of x − {a}; {a} must be added back: x̄ = {dn(mean)}.', f'B1 that is the coded mean; B1 x̄ = {dn(mean)}')
    return Q(f'For {n} values, Σ(x − {a}) = {num(s)}. {nm} calculates the mean as {a} − {pn(s)}/{n} = {dn(a - Fr(s, n))}. Explain the error and find the correct mean.',
             f'x − {a} has mean {pn(s)}/{n}, so x̄ = {a} + {pn(s)}/{n} = {dn(mean)}; the sign was wrong.', f'B1 should add the coded mean; B1 x̄ = {dn(mean)}')


@m112.add('C2', (3, 4), 'explain')
def m112_show(r, D):
    n = r.randint(10, 40)
    a = r.choice([10, 20, 30, 50])
    mean = Fr(r.randint(a * 10 - 80, a * 10 + 80), 10)
    s = (mean - a) * n
    if s.denominator != 1 or s == 0:
        return None
    return Q(f'The mean of {n} values of x is {dn(mean)}. Show that Σ(x − {a}) = {num(int(s))}.', f'Σ(x − {a}) = Σx − {n} × {a} = {dn(mean * n)} − {n * a} = {num(int(s))}',
             f'M1 Σx = {n} × {dn(mean)} = {dn(mean * n)}; A1 subtracts {n} × {a} to obtain {num(int(s))}')


@m112.add('C3', (1, 2, 3, 4, 5), 'numerical')
def m112_calc(r, D):
    a = r.choice([10, 20, 30, 40, 50, 60, 100, 200])
    if D <= 2:
        n = r.randint(5, 8)
        xs = [a + r.randint(-9, 9) for _ in range(n)]
        cs = [x - a for x in xs]
        mean = Fr(sum(xs), n)
        if sum(cs) == 0:
            return None
        return Q(f'The values ' + ', '.join(map(str, xs)) + f' are coded using y = x − {a}. Find Σy and hence the mean of x.', f'Σy = {num(sum(cs))}; x̄ = {dn(mean)}',
                 f'B1 coded values; B1 Σy = {num(sum(cs))}; B1 x̄ = {a} + {pn(sum(cs))}/{n} = {dn(mean)}')
    if D == 3:
        n = r.randint(10, 60)
        s = r.randint(-6 * n, 6 * n)
        if s == 0:
            return None
        b = a + r.choice([-10, -5, 5, 10])
        mean = a + Fr(s, n)
        s2 = (mean - b) * n
        return Q(f'For {n} values of x, Σ(x − {a}) = {num(s)}. Find the mean of x and the value of Σ(x − {b}).', f'x̄ = {dn(mean)}; Σ(x − {b}) = {dn(s2)}',
                 f'M1 x̄ = {a} + {pn(s)}/{n}; A1 {dn(mean)}; M1 Σx = {dn(mean * n)}; A1 Σ(x − {b}) = {dn(s2)}')
    n1, n2 = r.randint(8, 30), r.randint(8, 30)
    s1, s2 = r.randint(-5 * n1, 5 * n1), r.randint(-5 * n2, 5 * n2)
    b = a + r.choice([5, 10, 20])
    if s1 == 0 or s2 == 0:
        return None
    nm1, nm2 = two_people(r)
    tot = a * n1 + s1 + b * n2 + s2
    cm = Fr(tot, n1 + n2)
    return Q(f'{nm1} records {n1} values of x with Σ(x − {a}) = {num(s1)}. {nm2} records {n2} values of x with Σ(x − {b}) = {num(s2)}. Find the mean of all {n1 + n2} values.', dn(cm),
             f'M1 Σx = {n1} × {a} + {pn(s1)} = {a * n1 + s1}; M1 Σx = {n2} × {b} + {pn(s2)} = {b * n2 + s2}; M1 total ÷ {n1 + n2}; A1 {dn(cm)}')


@m112.add('C3', (3, 4, 5), 'numerical')
def m112_scale(r, D):
    a = r.choice([100, 150, 200, 500, 1000])
    b = r.choice([2, 5, 10, 20])
    n = r.randint(10, 50)
    s = r.randint(-3 * n, 3 * n)
    if s == 0:
        return None
    ybar = Fr(s, n)
    mean = a + b * ybar
    return Q(f'The masses, x grams, of {n} bags of flour are coded using y = (x − {a})/{b}. Given that Σy = {num(s)}, find the mean mass of the bags.', f'{dn(mean)} g',
             f'M1 ȳ = {num(s)}/{n} = {dn(ybar)}; M1 x̄ = {b}ȳ + {a}; A1 {dn(mean)}')


def m112_c4(r, D):
    a = r.choice([20, 30, 40, 50, 60])
    n1, n2 = r.randint(10, 30), r.randint(10, 30)
    s1, s2 = r.randint(-4 * n1, 4 * n1), r.randint(-4 * n2, 4 * n2)
    if s1 == 0 or s2 == 0 or s1 * n2 == s2 * n1:
        return None
    m1, m2 = a + Fr(s1, n1), a + Fr(s2, n2)
    cm = a + Fr(s1 + s2, n1 + n2)
    c = city(r)
    intro = f'The times, x minutes, taken by workers to travel to two offices in {c} were recorded. For {n1} workers at office A, Σ(x − {a}) = {num(s1)}. For {n2} workers at office B, Σ(x − {a}) = {num(s2)}.'
    parts = [
        P('Find the mean time for the workers at office A.', dn(m1), f'M1 {a} + {pn(s1)}/{n1}; A1 {dn(m1)}'),
        P('Find the mean time for the workers at office B.', dn(m2), f'M1 {a} + {pn(s2)}/{n2}; A1 {dn(m2)}'),
        P('Find the mean time for all the workers.', dn(cm), f'M1 Σ(x − {a}) = {num(s1 + s2)} for {n1 + n2} workers; A1 {dn(cm)}'),
        P('Find Σx for all the workers.', num(a * (n1 + n2) + s1 + s2), f'M1 {a} × {n1 + n2} + {pn(s1 + s2)}; A1 {a * (n1 + n2) + s1 + s2}'),
        P('State which office has the longer mean journey time.', 'A' if m1 > m2 else 'B', 'B1 correct office from means'),
    ]
    return cmp_(r, intro, parts)


m112.add('C4', (2, 3, 4, 5))(m112_c4)

m113 = T('Choosing an appropriate average for a context', 'appropriate average', 'choosing an average')
m113.fixed('C1', (1, 2), [
    ('A shop wants to know which shoe size to stock most of. The most useful average is', 'the mode', 'The most common size is the one sold most.', ['the mean', 'the median', 'the range']),
    ('The salaries in a small firm include the director\'s very high salary. The most representative average is', 'the median', 'The median is not affected by an extreme value.', ['the mean', 'the mode', 'the maximum']),
    ('Which average uses every data value?', 'the mean', 'Mean = Σx/n uses all values.', ['the median', 'the mode', 'the lower quartile']),
    ('For a set of data with no outliers and a symmetric distribution, which average is usually preferred?', 'the mean', 'It uses all the data and is not distorted when there are no extreme values.', ['the mode', 'the range', 'the interquartile range']),
    ('The favourite colours of 30 students are recorded. Which average can be found?', 'the mode', 'Categorical data have no order or numerical value.', ['the mean', 'the median', 'the mean and the median']),
    ('For a positively skewed distribution, the mean is usually', 'greater than the median', 'The long upper tail pulls the mean upwards.', ['less than the median', 'equal to the median', 'equal to the mode']),
])
m113.fixed('C2', (2, 3), [
    ('Give one advantage and one disadvantage of using the median rather than the mean.', 'Advantage: it is not affected by outliers or extreme values. Disadvantage: it does not use all the data values.', 'B1 advantage; B1 disadvantage [2]'),
    ('Explain why the mode may not be a useful average for a small set of continuous data.', 'With continuous data the values may all be different, so there may be no mode or several modes, which does not represent the data.', 'B1 values all different / no unique mode; B1 not representative [2]'),
])

AVG_CTX = [('the annual salaries, in thousands of dollars, of {n} employees of a company in {c}', 'salary'), ('the prices, in thousands of dollars, of {n} houses sold in a street in {c}', 'price'),
           ('the times, in minutes, that {n} patients waited at a clinic in {c}', 'waiting time'), ('the ages, in years, of {n} people attending a class in {c}', 'age')]


def outlier_data(r, n):
    base = r.randint(20, 50)
    xs = sorted(base + r.randint(0, 15) for _ in range(n - 1))
    big = base + r.randint(80, 200)
    return sorted(xs + [big]), big


@m113.add('C1', (2, 3))
def m113_c1(r, D):
    n = r.choice([7, 8, 9, 10])
    xs, big = outlier_data(r, n)
    ctx, w = r.choice(AVG_CTX)
    return MC(r, f'The data are {ctx.format(n=n, c=city(r))}: ' + ', '.join(map(str, xs)) + '. Which average best represents a typical value?', 'the median',
              ['the mean', 'the range', 'the largest value'], f'{big} is an outlier that distorts the mean; the median ({dn(med(xs))}) is unaffected.')


@m113.add('C2', (2, 3, 4), 'explain')
def m113_exp(r, D):
    n = r.choice([7, 8, 9, 10, 11])
    xs, big = outlier_data(r, n)
    ctx, w = r.choice(AVG_CTX)
    mean = Fr(sum(xs), n)
    m = med(xs)
    nm = person(r)
    return Q(f'The data are {ctx.format(n=n, c=city(r))}: ' + ', '.join(map(str, xs)) + f'. {nm} says the mean, {n3(float(mean))}, is the best average to describe a typical {w}. Explain why {nm} is wrong and state a better average, giving its value.',
             f'The value {big} is an outlier which pulls the mean above most of the data; the median, {dn(m)}, is a better typical value.',
             f'B1 identifies outlier {big} raising the mean; B1 median {dn(m)}')


@m113.add('C2', (2, 3), 'explain')
def m113_ctx(r, D):
    xs, fs = rdisc(r)
    if fs.count(max(fs)) > 1:
        return None
    mo = xs[fs.index(max(fs))]
    item = r.choice(['dress sizes', 'shoe sizes', 'hat sizes'])
    n = sum(fs)
    xs2 = [x * 2 + 4 if item == 'dress sizes' else x + 3 for x in xs]
    mean = Fr(sum(x * f for x, f in zip(xs2, fs)), n)
    mo2 = xs2[fs.index(max(fs))]
    return Q(f'A shop records the {item} sold in one day: {ftab(xs2, fs, "size")}. The mean size is {n3(float(mean))}. Explain why the mode is a more useful average for the shop manager, and state its value.',
             f'Sizes are discrete and the shop needs the size it sells most; the mean {n3(float(mean))} is not an actual size. The mode is {mo2}.',
             f'B1 mean is not a stocked size / manager needs most popular; B1 mode {mo2}')


@m113.add('C3', (1, 2, 3, 4, 5), 'numerical')
def m113_calc(r, D):
    n = r.choice([8, 9, 10, 11, 12])
    xs, big = outlier_data(r, n)
    x = r.choice(xs[:-1])
    xs = sorted(xs + [x])
    n += 1
    cnt = {v: xs.count(v) for v in xs}
    top = max(cnt.values())
    if list(cnt.values()).count(top) > 1:
        return None
    mo = max(cnt, key=cnt.get)
    ctx, w = r.choice(AVG_CTX)
    mean = Fr(sum(xs), n)
    m = med(xs)
    return Q(f'The data are {ctx.format(n=n, c=city(r))}: ' + ', '.join(map(str, xs)) + '. Find the mean, median and mode, and state which is the most appropriate average to use, giving a reason.',
             f'mean {n3(float(mean))}, median {dn(m)}, mode {mo}; the median, since the outlier {big} distorts the mean',
             f'B1 mean {n3(float(mean))}; B1 median {dn(m)}; B1 mode {mo}; B1 median with reason (outlier {big})')


@m113.add('C3', (2, 3, 4), 'numerical')
def m113_effect(r, D):
    n = r.choice([7, 8, 9, 10])
    xs, big = outlier_data(r, n)
    rest = xs[:-1]
    m1, m2 = Fr(sum(xs), n), Fr(sum(rest), n - 1)
    d1_, d2_ = med(xs), med(rest)
    return Q(f'The data ' + ', '.join(map(str, xs)) + f' contain an outlier. Find the change in the mean and the change in the median when the outlier {big} is removed.',
             f'mean falls from {n3(float(m1))} to {n3(float(m2))} (by {n3(float(m1 - m2))}); median falls from {dn(d1_)} to {dn(d2_)} (by {dn(d1_ - d2_)})',
             f'B1 means {n3(float(m1))} and {n3(float(m2))}; B1 medians {dn(d1_)} and {dn(d2_)}; B1 mean changes much more than median')


def m113_c4(r, D):
    n = r.choice([9, 10, 11, 12])
    xs, big = outlier_data(r, n)
    mean = Fr(sum(xs), n)
    m = med(xs)
    c = city(r)
    intro = f'The annual salaries, in thousands of dollars, of the {n} employees of a small company in {c} are: ' + ', '.join(map(str, xs)) + '.'
    parts = [
        P('Calculate the mean salary.', n3(float(mean)), f'M1 Σx = {sum(xs)}; A1 {n3(float(mean))}'),
        P('Find the median salary.', dn(m), f'B1 {dn(m)}'),
        P('The company wants to attract new staff. State, with a reason, which average it might quote in an advertisement.', f'the mean ({n3(float(mean))}), since it is higher because of the large salary {big}', 'B1 mean; B1 reason: inflated by the high salary'),
        P('State which average best represents the salary of a typical employee, giving a reason.', f'the median ({dn(m)}), as it is not affected by the outlier {big}', 'B1 median; B1 not affected by the extreme value'),
        P(f'Find the mean salary of the other employees if the salary of {big} is excluded.', n3((sum(xs) - big) / (n - 1)), f'M1 ({sum(xs)} − {big}) ÷ {n - 1}; A1 {n3((sum(xs) - big) / (n - 1))}'),
    ]
    return cmp_(r, intro, parts)


m113.add('C4', (2, 3, 4, 5))(m113_c4)

CHAPTERS[11] = [m111, m112, m113]


# ================================================================ Chapter 12 Measures of variation

def var_(xs):
    n = len(xs)
    return Fr(sum(x * x for x in xs), n) - Fr(sum(xs), n) ** 2


def fvar(xs, fs):
    n = sum(fs)
    return Fr(sum(f * x * x for x, f in zip(xs, fs)), n) - Fr(sum(f * x for x, f in zip(xs, fs)), n) ** 2


def pct_pos(n, p):
    return Fr(p * n, 100)


v121 = T('Range, interquartile range and percentiles', 'range', 'interquartile range', 'percentiles')
v121.fixed('C1', (1, 2), [
    ('The interquartile range is', 'the upper quartile minus the lower quartile', 'IQR = Q3 − Q1.', ['the largest value minus the smallest', 'the median minus the lower quartile', 'the upper quartile plus the lower quartile']),
    ('The 50th percentile of a data set is the same as', 'the median', 'Half the data lie below it.', ['the mean', 'the upper quartile', 'the mode']),
    ('The 75th percentile is the same as', 'the upper quartile', 'Three quarters of the data lie below it.', ['the lower quartile', 'the median', 'the maximum']),
    ('Which measure of spread is least affected by outliers?', 'the interquartile range', 'It uses only the middle 50% of the data.', ['the range', 'the standard deviation', 'the variance']),
])
v121.fixed('C2', (2, 3), [
    ('Explain why the interquartile range is often preferred to the range as a measure of spread.', 'The range uses only the two extreme values, so an outlier changes it a lot; the IQR covers the middle half of the data and is not affected by extreme values.', 'B1 range depends on extremes; B1 IQR uses middle 50% / resistant to outliers [2]'),
    ('Explain what is meant by the 90th percentile of a set of test scores.', 'It is the score below which 90% of the scores lie, so only 10% of the students scored higher.', 'B1 90% below; B1 in context [2]'),
])


@v121.add('C1', (1, 2, 3))
def v121_c1(r, D):
    n = r.choice([7, 9, 11, 8, 10])
    xs = sorted(r.randint(5, 60) for _ in range(n))
    q1, m, q3 = quarts(xs)
    kind = r.choice(['range', 'iqr'])
    shown = list(xs)
    r.shuffle(shown)
    if kind == 'range':
        R = xs[-1] - xs[0]
        return MC(r, 'Find the range of ' + ', '.join(map(str, shown)) + '.', str(R), [str(xs[-1]), dn(q3 - q1), str(shown[-1] - shown[0]) if shown[-1] - shown[0] != R else str(R + 1), str(xs[-2] - xs[1])], f'{xs[-1]} − {xs[0]} = {R}.')
    return MC(r, 'Find the interquartile range of ' + ', '.join(map(str, xs)) + '.', dn(q3 - q1), [str(xs[-1] - xs[0]), dn(q3 - m), dn(m - q1), dn(q3 - q1 + 1)], f'Q1 = {dn(q1)}, Q3 = {dn(q3)}, IQR = {dn(q3 - q1)}.')


@v121.add('C1', (2, 3))
def v121_c1b(r, D):
    n = r.choice([40, 60, 80, 120, 200, 240, 300, 400])
    p = r.choice([10, 20, 30, 40, 60, 70, 80, 90])
    pos = pct_pos(n, p)
    return MC(r, f'Using a cumulative frequency graph for {n} values, at what cumulative frequency should the {ordn(p)} percentile be read?', dn(pos),
              [str(p), dn(Fr(n * (100 - p), 100)), dn(Fr(n, p)), dn(pos + 1)], f'{p}% of {n} = {dn(pos)}.')


@v121.add('C2', (2, 3, 4), 'explain')
def v121_err(r, D):
    n = r.choice([11, 13, 15])
    xs = sorted(r.randint(10, 60) for _ in range(n - 1))
    big = xs[-1] + r.randint(40, 90)
    xs.append(big)
    q1, m, q3 = quarts(xs)
    nm = person(r)
    return Q(f'{nm} says that the range of the data ' + ', '.join(map(str, xs)) + f' gives a good measure of the spread of the data. Comment on this claim, and find a more suitable measure of spread.',
             f'The range ({big - xs[0]}) is inflated by the outlier {big}; the interquartile range, {dn(q3 - q1)}, is more suitable.',
             f'B1 range distorted by outlier {big}; B1 IQR = {dn(q3)} − {dn(q1)} = {dn(q3 - q1)}')


@v121.add('C2', (3, 4), 'explain')
def v121_int(r, D):
    p = r.choice([10, 20, 80, 90, 95])
    v = r.randint(30, 90)
    ctx = r.choice([('a reading test', 'score'), ('a fitness test', 'time, in seconds,'), ('a national exam', 'mark')])
    n = r.choice([200, 400, 500, 800, 1000])
    k = n * (100 - p) // 100
    return Q(f'In {ctx[0]} taken by {n} students, the {ordn(p)} percentile of the {ctx[1]} is {v}. Interpret this value and find the number of students with a {ctx[1].split(",")[0]} above {v}.',
             f'{p}% of the students had a {ctx[1].split(",")[0]} below {v}; about {k} students scored above {v}.',
             f'B1 interpretation: {p}% below {v}; B1 {100 - p}% of {n} = {k}')


@v121.add('C3', (1, 2, 3, 4, 5), 'numerical')
def v121_calc(r, D):
    bounds, freqs = rgroups(r)
    ctx, var, unit = r.choice(HIST_CTX)
    n = sum(freqs)
    desc = ctx.format(n=n, c=city(r))
    if D <= 2:
        k = r.choice([11, 13, 15, 12, 14])
        xs = rdata(r, k)
        q1, m, q3 = quarts(xs)
        return Q('Find the range and the interquartile range of ' + ', '.join(map(str, xs)) + '.', f'range {xs[-1] - xs[0]}; IQR {dn(q3 - q1)}',
                 f'B1 range {xs[-1] - xs[0]}; B1 Q1 {dn(q1)} and Q3 {dn(q3)}; B1 IQR {dn(q3 - q1)}')
    if D == 3:
        p = r.choice([10, 20, 30, 70, 80, 90])
        v = cf_interp(bounds, freqs, pct_pos(n, p))
        return Q(f'The table summarises {desc}: {gtable(bounds, freqs, var)}. Use linear interpolation to estimate the {ordn(p)} percentile.', n3(float(v)),
                 f'M1 position {dn(pct_pos(n, p))}; M1 interpolation within the correct class; A1 {n3(float(v))}')
    if D == 4:
        q1 = cf_interp(bounds, freqs, Fr(n, 4))
        q3 = cf_interp(bounds, freqs, Fr(3 * n, 4))
        return Q(f'The table summarises {desc}: {gtable(bounds, freqs, var)}. Estimate the interquartile range.', n3(float(q3 - q1)),
                 f'M1 positions {dn(Fr(n, 4))} and {dn(Fr(3 * n, 4))}; A1 Q1 {n3(float(q1))}; A1 Q3 {n3(float(q3))}; A1 IQR {n3(float(q3 - q1))}')
    p10 = cf_interp(bounds, freqs, pct_pos(n, 10))
    p90 = cf_interp(bounds, freqs, pct_pos(n, 90))
    return Q(f'The table summarises {desc}: {gtable(bounds, freqs, var)}. Estimate the 10th to 90th interpercentile range.', n3(float(p90 - p10)),
             f'M1 positions {dn(pct_pos(n, 10))} and {dn(pct_pos(n, 90))}; A1 P10 {n3(float(p10))}; A1 P90 {n3(float(p90))}; A1 {n3(float(p90 - p10))}')


@v121.add('C3', (2, 3, 4), 'numerical')
def v121_above(r, D):
    bounds, freqs = rgroups(r)
    ctx, var, unit = r.choice(HIST_CTX)
    n = sum(freqs)
    i = r.randrange(1, len(freqs))
    v = bounds[i] + Fr(bounds[i + 1] - bounds[i], r.choice([2, 4, 5]))
    if v.denominator != 1:
        return None
    below = sum(freqs[:i]) + (v - bounds[i]) / (bounds[i + 1] - bounds[i]) * freqs[i]
    pc = below / n * 100
    return Q(f'The table summarises {ctx.format(n=n, c=city(r))}: {gtable(bounds, freqs, var)}. Estimate the percentage of values less than {dn(v)}, and hence state which percentile {dn(v)} approximately is.',
             f'{n3(float(pc))}%; about the {ordn(round(float(pc)))} percentile' if 1 <= round(float(pc)) <= 99 else f'{n3(float(pc))}%',
             f'M1 {sum(freqs[:i])} + fraction of class {bounds[i]}–{bounds[i + 1]}; M1 ÷ {n} × 100; A1 {n3(float(pc))}%')


def v121_c4(r, D):
    bounds, freqs = rgroups(r)
    ctx, var, unit = r.choice(HIST_CTX)
    n = sum(freqs)
    q1 = cf_interp(bounds, freqs, Fr(n, 4))
    m = cf_interp(bounds, freqs, Fr(n, 2))
    q3 = cf_interp(bounds, freqs, Fr(3 * n, 4))
    p = r.choice([10, 20, 80, 90])
    pv = cf_interp(bounds, freqs, pct_pos(n, p))
    cum = [sum(freqs[:i + 1]) for i in range(len(freqs))]
    intro = f'The table summarises {ctx.format(n=n, c=city(r))}: {gtable(bounds, freqs, var)}.'
    parts = [
        P('Write down the cumulative frequencies.', ', '.join(map(str, cum)), 'B1 all correct'),
        P('Estimate the median.', n3(float(m)), f'M1 position {dn(Fr(n, 2))}; A1 {n3(float(m))}'),
        P('Estimate the interquartile range.', n3(float(q3 - q1)), f'M1 Q1 {n3(float(q1))}; M1 Q3 {n3(float(q3))}; A1 {n3(float(q3 - q1))}'),
        P(f'Estimate the {ordn(p)} percentile.', n3(float(pv)), f'M1 position {dn(pct_pos(n, p))}; A1 {n3(float(pv))}'),
        P('State the range of the data, given that the smallest and largest values are at the extremes of the table.', str(bounds[-1] - bounds[0]), f'B1 {bounds[-1]} − {bounds[0]}'),
    ]
    return cmp_(r, intro, parts)


v121.add('C4', (2, 3, 4, 5))(v121_c4)


v122 = T('Variance and standard deviation from raw and grouped data', 'variance', 'standard deviation', 'grouped data')
v122.fixed('C1', (1, 2), [
    ('If the standard deviation of a data set is 4, the variance is', '16', 'Variance = (standard deviation)².', ['2', '8', '4']),
    ('Adding 10 to every value in a data set changes the standard deviation by', 'nothing; it is unchanged', 'The spread is unchanged by a shift.', ['adding 10', 'multiplying by 10', 'adding √10']),
    ('Multiplying every value by 3 multiplies the standard deviation by', '3', 'The spread scales by the same factor.', ['9', '√3', '1']),
    ('The variance of a data set can never be', 'negative', 'It is a mean of squared deviations.', ['zero', 'greater than the mean', 'a decimal']),
])
v122.fixed('C2', (2, 3), [
    ('Explain why the standard deviation calculated from a grouped frequency table is only an estimate.', 'The exact values are unknown; midpoints are used in place of the values in each class.', 'B1 raw data unknown; B1 midpoints used [2]'),
    ('Explain what a standard deviation of 0 tells you about a set of data.', 'All the values are equal to the mean, so there is no spread at all.', 'B1 all values equal; B1 no spread / all equal to mean [2]'),
])


def sm_data(r, n, lo=1, hi=20):
    return [r.randint(lo, hi) for _ in range(n)]


@v122.add('C1', (2, 3))
def v122_c1(r, D):
    n = r.choice([4, 5, 6])
    xs = sm_data(r, n, 1, 12)
    v = var_(xs)
    if v == 0:
        return None
    sd = math.sqrt(v)
    mean = Fr(sum(xs), n)
    return MC(r, 'Find the standard deviation of ' + ', '.join(map(str, xs)) + ', correct to 3 significant figures.', n3(sd),
              [n3(float(v)) if abs(float(v) - sd) > 1e-6 else n3(sd + 1), n3(math.sqrt(float(Fr(sum(x * x for x in xs), n)))), n3(math.sqrt(float(v) * n / (n - 1))), n3(math.sqrt(abs(float(Fr(sum(x * x for x in xs), n) - mean))))],
              f'Σx = {sum(xs)}, Σx² = {sum(x * x for x in xs)}; σ = √({sum(x * x for x in xs)}/{n} − {pn(dn(mean))}²) = {n3(sd)}.')


@v122.add('C1', (1, 2, 3))
def v122_c1b(r, D):
    sd = r.randint(2, 15)
    a = r.randint(2, 30)
    b = r.choice([2, 3, 4, 5])
    kind = r.choice(['add', 'mul', 'both'])
    if kind == 'add':
        return MC(r, f'A data set has standard deviation {sd}. Each value is increased by {a}. Find the new standard deviation.', str(sd), [str(sd + a), str(sd * a), str(sd + a * a)], 'Adding a constant does not change the spread.')
    if kind == 'mul':
        return MC(r, f'A data set has standard deviation {sd}. Each value is multiplied by {b}. Find the new variance.', str(sd * sd * b * b), [str(sd * b), str(sd * sd * b), str(sd * b * b)], f'New σ = {b} × {sd} = {sd * b}, so variance = {sd * sd * b * b}.')
    return MC(r, f'A data set has standard deviation {sd}. Each value is multiplied by {b} and then {a} is added. Find the new standard deviation.', str(sd * b), [str(sd * b + a), str(sd + a), str(sd * b * b)], f'Only the multiplication affects the spread: {b} × {sd} = {sd * b}.')


@v122.add('C2', (2, 3, 4), 'explain')
def v122_err(r, D):
    n = r.choice([5, 6, 7])
    xs = sm_data(r, n, 2, 20)
    v = var_(xs)
    if v == 0:
        return None
    nm = person(r)
    sxx = sum(x * x for x in xs)
    wrong = Fr(sxx, n) - Fr(sum(xs), n)
    kind = r.choice(['nosq', 'nosub'])
    if kind == 'nosq' and wrong > 0:
        return Q(f'{nm} finds the variance of ' + ', '.join(map(str, xs)) + f' as Σx²/n − x̄ = {dn(wrong) if wrong.denominator in (1, 2, 4, 5, 10, 20, 25, 50) else n3(float(wrong))}. Explain the error and find the correct standard deviation.',
                 f'The mean must be squared: variance = Σx²/n − x̄² = {n3(float(v))}, so σ = {n3(math.sqrt(v))}.', f'B1 x̄ should be squared; M1 {sxx}/{n} − {pn(dn(Fr(sum(xs), n)))}²; A1 σ = {n3(math.sqrt(v))}')
    return Q(f'{nm} says the standard deviation of ' + ', '.join(map(str, xs)) + f' is √(Σx²/n) = {n3(math.sqrt(sxx / n))}. Explain the error and find the correct standard deviation.',
             f'x̄² has not been subtracted: σ = √(Σx²/n − x̄²) = {n3(math.sqrt(v))}.', f'B1 must subtract x̄²; M1 correct formula; A1 {n3(math.sqrt(v))}')


@v122.add('C2', (2, 3, 4), 'explain')
def v122_cmp(r, D):
    m1, m2 = r.randint(40, 70), r.randint(40, 70)
    s1, s2 = Fr(r.randint(20, 150), 10), Fr(r.randint(20, 150), 10)
    if m1 == m2 or s1 == s2:
        return None
    g = r.choice([('Class A', 'Class B', 'test marks', 'for'), ('Machine P', 'Machine Q', 'masses, in grams, of packets filled', 'by'), ('Runner X', 'Runner Y', 'lap times, in seconds,', 'for')])
    return Q(f'The {g[2]} {g[3]} {g[0]} have mean {m1} and standard deviation {dn(s1)}; {g[3]} {g[1]} the mean is {m2} and the standard deviation is {dn(s2)}. Make two comparisons between the two sets of data.',
             f'{g[0] if m1 > m2 else g[1]} has the higher mean, so its values are larger on average; {g[0] if s1 > s2 else g[1]} has the larger standard deviation, so its values are more spread out (less consistent).',
             'B1 compares means in context; B1 compares standard deviations (consistency) in context')


@v122.add('C3', (1, 2, 3, 4, 5), 'numerical')
def v122_calc(r, D):
    if D <= 2:
        n = r.choice([5, 6, 7, 8])
        xs = sm_data(r, n, 1, 30)
        v = var_(xs)
        mean = Fr(sum(xs), n)
        return Q('Calculate the mean and the standard deviation of ' + ', '.join(map(str, xs)) + '.', f'mean {dn(mean)}; standard deviation {n3(math.sqrt(v))}',
                 f'B1 mean {dn(mean)}; M1 Σx² = {sum(x * x for x in xs)} used in Σx²/n − x̄²; A1 {n3(math.sqrt(v))}')
    if D == 3:
        xs, fs = rdisc(r)
        ctx, _ = r.choice(DISC_CTX)
        n = sum(fs)
        v = fvar(xs, fs)
        mean = Fr(sum(x * f for x, f in zip(xs, fs)), n)
        return Q(f'The table shows {ctx.format(n=n, c=city(r))}: {ftab(xs, fs)}. Calculate the mean and the standard deviation.', f'mean {dn(mean)}; standard deviation {n3(math.sqrt(v))}',
                 f'B1 mean {dn(mean)}; M1 Σfx² = {sum(f * x * x for x, f in zip(xs, fs))}; M1 Σfx²/Σf − x̄²; A1 {n3(math.sqrt(v))}')
    bounds, freqs = rgroups(r)
    ctx, var, unit = r.choice(HIST_CTX)
    n = sum(freqs)
    mids = [Fr(bounds[i] + bounds[i + 1], 2) for i in range(len(freqs))]
    v = fvar(mids, freqs)
    mean = sum(m * f for m, f in zip(mids, freqs)) / n
    return Q(f'The table summarises {ctx.format(n=n, c=city(r))}: {gtable(bounds, freqs, var)}. Calculate estimates of the mean and the standard deviation.', f'mean {n3(float(mean))}; standard deviation {n3(math.sqrt(v))}',
             f'M1 midpoints {", ".join(dn(x) for x in mids)}; A1 mean {n3(float(mean))}; M1 Σfx²/Σf − x̄²; A1 {n3(math.sqrt(v))}')


@v122.add('C3', (3, 4, 5), 'numerical')
def v122_unk(r, D):
    n = r.choice([4, 5])
    ys = sm_data(r, n - 1, 2, 20)
    x = r.randint(2, 20)
    tot = sum(ys) + x
    mean = Fr(tot, n)
    if mean.denominator not in (1, 2, 4, 5):
        return None
    allv = ys + [x]
    v = var_(allv)
    return Q(f'The values ' + ', '.join(map(str, ys)) + f' and x have mean {dn(mean)}. Find x and the standard deviation of the {n} values.', f'x = {x}; standard deviation {n3(math.sqrt(v))}',
             f'M1 {n} × {dn(mean)} − {sum(ys)}; A1 x = {x}; M1 Σx²/n − x̄²; A1 {n3(math.sqrt(v))}')


def v122_c4(r, D):
    bounds, freqs = rgroups(r)
    ctx, var, unit = r.choice(HIST_CTX)
    n = sum(freqs)
    c = city(r)
    mids = [Fr(bounds[i] + bounds[i + 1], 2) for i in range(len(freqs))]
    mean = sum(m * f for m, f in zip(mids, freqs)) / n
    v = fvar(mids, freqs)
    sd = math.sqrt(v)
    om = round(float(mean) + r.choice([-8, -5, 5, 8]), 1)
    osd = round(sd * r.choice([0.6, 0.8, 1.3, 1.5]), 1)
    intro = f'The table summarises {ctx.format(n=n, c=c)}: {gtable(bounds, freqs, var)}.'
    parts = [
        P('Calculate an estimate of the mean.', n3(float(mean)), 'M1 midpoints; A1 ' + n3(float(mean))),
        P('Calculate an estimate of the standard deviation.', n3(sd), f'M1 Σfx² = {dn(sum(f * m * m for m, f in zip(mids, freqs)))}; M1 Σfx²/{n} − x̄²; A1 {n3(sd)}'),
        P(f'A second sample of the same size from another city has mean {om} and standard deviation {osd}. Compare the two samples.', f'the second sample has a {"higher" if om > mean else "lower"} mean and is {"more" if osd > sd else "less"} spread out (mean {n3(float(mean))}, sd {n3(sd)} for the first sample)',
          'B1 compares means; B1 compares standard deviations'),
        P('Explain why your answer for the standard deviation is an estimate.', 'The raw data are not known; midpoints are used for each class.', 'B1 midpoints used'),
        P('State the class containing the median.', next(f'{bounds[i]} ≤ {var} < {bounds[i + 1]}' for i in range(len(freqs)) if sum(freqs[:i + 1]) >= Fr(n, 2)), f'B1 the {dn(Fr(n, 2))}th value'),
    ]
    return cmp_(r, intro, parts)


v122.add('C4', (2, 3, 4, 5))(v122_c4)


@v122.add('C4', (3, 4, 5))
def v122_c4b(r, D):
    n = r.choice([6, 7, 8])
    xs = sm_data(r, n, 5, 40)
    v = var_(xs)
    mean = Fr(sum(xs), n)
    if v == 0:
        return None
    a = r.randint(3, 20)
    b = r.choice([2, 3, 10])
    nm = person(r)
    intro = f'{nm} records the scores ' + ', '.join(map(str, xs)) + ' in a game.'
    parts = [
        P('Calculate the mean and standard deviation of the scores.', f'mean {dn(mean) if mean.denominator in (1, 2, 4, 5, 8) else n3(float(mean))}; sd {n3(math.sqrt(v))}', f'B1 mean; M1 Σx² = {sum(x * x for x in xs)}; A1 sd {n3(math.sqrt(v))}'),
        P(f'Every score is increased by {a} bonus points. State the new mean and standard deviation.', f'mean {n3(float(mean) + a)}; sd {n3(math.sqrt(v))} (unchanged)', f'B1 mean + {a}; B1 sd unchanged'),
        P(f'Instead, every original score is multiplied by {b}. State the new mean and standard deviation.', f'mean {n3(float(mean) * b)}; sd {n3(math.sqrt(v) * b)}', f'B1 mean × {b}; B1 sd × {b}'),
        P('Find the variance of the original scores.', n3(float(v)), f'B1 {n3(float(v))}'),
    ]
    return cmp_(r, intro, parts)


v123 = T('Standard deviation from Σx and Σx² and from coded data', 'Σx and Σx²', 'coded data', 'standard deviation')
v123.fixed('C1', (1, 2), [
    ('The variance of x is given by', 'Σx²/n − x̄²', 'Mean of the squares minus the square of the mean.', ['Σx²/n − x̄', '(Σx)²/n − x̄²', 'Σx²/n + x̄²']),
    ('If Σ(x − 20)² is used instead of Σx², the standard deviation of x', 'is found in the same way, since coding by subtraction does not change spread', 'σ of x − a equals σ of x.', ['is reduced by 20', 'is increased by 20', 'cannot be found']),
    ('If y = (x − a)/b with b > 0, then the standard deviation of x is', 'b times the standard deviation of y', 'Subtracting a does not affect spread; dividing by b scales it.', ['the standard deviation of y plus a', 'the standard deviation of y divided by b', 'b² times the standard deviation of y']),
    ('For 10 values, Σx = 50 and Σx² = 290. The variance is', '4', '290/10 − 5² = 4.', ['29', '2', '24']),
])
v123.fixed('C2', (2, 3), [
    ('Explain why Σ(x − a)² can be used in place of Σx² when calculating a standard deviation, provided Σ(x − a) is used for the mean.', 'Subtracting a shifts every value by the same amount, so the spread of x − a equals the spread of x; the formula is applied to the coded values.', 'B1 shift does not change spread; B1 apply formula to coded values consistently [2]'),
    ('Explain how to check that values of Σx and Σx² are consistent.', 'The variance Σx²/n − (Σx/n)² must be non-negative, so Σx² ≥ (Σx)²/n.', 'B1 variance ≥ 0; B1 inequality stated [2]'),
])


def sums_data(r, n, lo, hi):
    xs = [r.randint(lo, hi) for _ in range(n)]
    return xs, sum(xs), sum(x * x for x in xs)


@v123.add('C1', (1, 2, 3))
def v123_c1(r, D):
    n = r.randint(8, 40)
    xs, sx, sxx = sums_data(r, n, 2, 30)
    v = Fr(sxx, n) - Fr(sx, n) ** 2
    if v == 0:
        return None
    return MC(r, f'For {n} values, Σx = {sx} and Σx² = {sxx}. Find the variance' + (', correct to 3 significant figures.' if v.denominator not in (1, 2, 4, 5, 10, 20, 25, 50) else '.'), dn(v),
              [dn(Fr(sxx, n) - Fr(sx, n)), n3(math.sqrt(v)), dn(Fr(sxx, n)), dn(Fr(sxx, n - 1) - Fr(sx, n) ** 2)], f'{sxx}/{n} − {pn(dn(Fr(sx, n)))}² = {dn(v)}.')


@v123.add('C1', (2, 3))
def v123_c1b(r, D):
    n = r.randint(10, 50)
    a = r.choice([10, 20, 30, 50, 100])
    xs = [a + r.randint(-8, 8) for _ in range(n)]
    s = sum(x - a for x in xs)
    ss = sum((x - a) ** 2 for x in xs)
    v = Fr(ss, n) - Fr(s, n) ** 2
    if v == 0:
        return None
    sd = math.sqrt(v)
    return MC(r, f'For {n} values of x, Σ(x − {a}) = {num(s)} and Σ(x − {a})² = {ss}. Find the standard deviation of x.', n3(sd),
              [n3(math.sqrt(ss / n)), n3(float(v)), n3(sd + a), n3(math.sqrt(abs(ss / n - s / n)))], f'σ = √({ss}/{n} − {pn(dn(Fr(s, n)))}²) = {n3(sd)}.')


@v123.add('C2', (2, 3, 4), 'explain')
def v123_err(r, D):
    n = r.randint(10, 40)
    a = r.choice([20, 30, 50, 100])
    xs = [a + r.randint(-9, 9) for _ in range(n)]
    s = sum(x - a for x in xs)
    ss = sum((x - a) ** 2 for x in xs)
    v = Fr(ss, n) - Fr(s, n) ** 2
    if v == 0 or s == 0:
        return None
    nm = person(r)
    wrong = math.sqrt(v) + a
    return Q(f'For {n} values, Σ(x − {a}) = {num(s)} and Σ(x − {a})² = {ss}. {nm} finds the standard deviation of the coded values and then adds {a}, giving {n3(wrong)}. Explain the error and state the correct standard deviation of x.',
             f'Subtracting {a} does not change the spread, so {a} should not be added back to the standard deviation: σ = {n3(math.sqrt(v))}.',
             f'B1 shift does not affect standard deviation; B1 {n3(math.sqrt(v))}')


@v123.add('C2', (3, 4), 'explain')
def v123_check(r, D):
    n = r.randint(5, 20)
    sx = r.randint(20, 200)
    lo = Fr(sx * sx, n)
    good = r.random() < 0.5
    sxx = int(lo) + r.randint(1, 200) if good else max(1, int(lo) - r.randint(1, max(1, int(lo) // 4)))
    if Fr(sxx, n) - Fr(sx, n) ** 2 == 0:
        return None
    v = Fr(sxx, n) - Fr(sx, n) ** 2
    return Q(f'A student records n = {n}, Σx = {sx} and Σx² = {sxx}. Determine whether these values can be correct, explaining your reasoning.',
             f'variance = {sxx}/{n} − {pn(dn(Fr(sx, n)))}² = {n3(float(v))}; ' + ('this is positive, so the values are possible' if v > 0 else 'this is negative, which is impossible, so the values cannot be correct'),
             f'M1 variance = Σx²/n − x̄²; A1 {n3(float(v))} and conclusion')


@v123.add('C3', (1, 2, 3, 4, 5), 'numerical')
def v123_calc(r, D):
    if D <= 2:
        n = r.randint(10, 60)
        xs, sx, sxx = sums_data(r, n, 5, 60)
        v = Fr(sxx, n) - Fr(sx, n) ** 2
        return Q(f'For {n} values of x, Σx = {sx} and Σx² = {sxx}. Find the mean and the standard deviation of x.', f'mean {dn(Fr(sx, n))}; sd {n3(math.sqrt(v))}',
                 f'B1 mean {dn(Fr(sx, n))}; M1 {sxx}/{n} − x̄²; A1 {n3(math.sqrt(v))}')
    if D == 3:
        n = r.randint(10, 50)
        a = r.choice([10, 20, 30, 40, 50, 100])
        xs = [a + r.randint(-10, 10) for _ in range(n)]
        s = sum(x - a for x in xs)
        ss = sum((x - a) ** 2 for x in xs)
        v = Fr(ss, n) - Fr(s, n) ** 2
        if s == 0:
            return None
        return Q(f'For {n} values of x, Σ(x − {a}) = {num(s)} and Σ(x − {a})² = {ss}. Find the mean and the standard deviation of x.', f'mean {dn(a + Fr(s, n))}; sd {n3(math.sqrt(v))}',
                 f'B1 mean {a} + {pn(s)}/{n} = {dn(a + Fr(s, n))}; M1 {ss}/{n} − {pn(dn(Fr(s, n)))}²; A1 {n3(math.sqrt(v))}')
    if D == 4:
        n = r.randint(10, 40)
        mean = Fr(r.randint(100, 800), 10)
        sd = Fr(r.randint(10, 90), 10)
        sx = mean * n
        sxx = n * (sd * sd + mean * mean)
        return Q(f'A set of {n} values has mean {dn(mean)} and standard deviation {dn(sd)}. Find Σx and Σx².', f'Σx = {dn(sx)}; Σx² = {dn(sxx)}',
                 f'B1 Σx = {dn(sx)}; M1 Σx²/{n} − {dn(mean)}² = {dn(sd)}²; A1 Σx² = {dn(sxx)}')
    n1, n2 = r.randint(8, 25), r.randint(8, 25)
    a1, s1, ss1 = sums_data(r, n1, 10, 40)
    a2, s2, ss2 = sums_data(r, n2, 15, 50)
    N = n1 + n2
    v = Fr(ss1 + ss2, N) - Fr(s1 + s2, N) ** 2
    return Q(f'For a group of {n1} values, Σx = {s1} and Σx² = {ss1}. For a second group of {n2} values, Σx = {s2} and Σx² = {ss2}. Find the mean and standard deviation of all {N} values.',
             f'mean {n3(float(Fr(s1 + s2, N)))}; sd {n3(math.sqrt(v))}', f'M1 Σx = {s1 + s2}, Σx² = {ss1 + ss2}; A1 mean {n3(float(Fr(s1 + s2, N)))}; M1 Σx²/{N} − x̄²; A1 {n3(math.sqrt(v))}')


@v123.add('C3', (3, 4, 5), 'numerical')
def v123_combine(r, D):
    n1, n2 = r.randint(10, 30), r.randint(10, 30)
    m1, m2 = r.randint(20, 60), r.randint(20, 60)
    sd1, sd2 = r.randint(2, 12), r.randint(2, 12)
    sx = m1 * n1 + m2 * n2
    sxx = n1 * (sd1 ** 2 + m1 ** 2) + n2 * (sd2 ** 2 + m2 ** 2)
    N = n1 + n2
    v = Fr(sxx, N) - Fr(sx, N) ** 2
    g = r.choice([('boys', 'girls'), ('Year 12 students', 'Year 13 students'), ('morning candidates', 'afternoon candidates')])
    return Q(f'In a test, {n1} {g[0]} had mean mark {m1} and standard deviation {sd1}; {n2} {g[1]} had mean mark {m2} and standard deviation {sd2}. Find the mean and standard deviation of the marks of all {N} candidates.',
             f'mean {n3(float(Fr(sx, N)))}; sd {n3(math.sqrt(v))}',
             f'M1 Σx = {sx}; M1 Σx² = {n1}({sd1}² + {m1}²) + {n2}({sd2}² + {m2}²) = {sxx}; A1 mean {n3(float(Fr(sx, N)))}; M1 Σx²/{N} − x̄²; A1 {n3(math.sqrt(v))}')


def v123_c4(r, D):
    n = r.randint(12, 40)
    a = r.choice([20, 30, 40, 50, 60])
    xs = [a + r.randint(-10, 12) for _ in range(n)]
    s = sum(x - a for x in xs)
    ss = sum((x - a) ** 2 for x in xs)
    v = Fr(ss, n) - Fr(s, n) ** 2
    if v == 0:
        return None
    mean = a + Fr(s, n)
    sx = sum(xs)
    sxx = sum(x * x for x in xs)
    c = city(r)
    extra = a + r.randint(-5, 15)
    v2 = Fr(sxx + extra * extra, n + 1) - Fr(sx + extra, n + 1) ** 2
    intro = f'The ages, x years, of {n} members of a sports club in {c} are summarised by Σ(x − {a}) = {num(s)} and Σ(x − {a})² = {ss}.'
    parts = [
        P('Find the mean age.', dn(mean) if mean.denominator in (1, 2, 4, 5, 8, 10, 20, 25, 40) else n3(float(mean)), f'M1 {a} + {pn(s)}/{n}; A1 {dn(mean) if mean.denominator in (1, 2, 4, 5, 8, 10, 20, 25, 40) else n3(float(mean))}'),
        P('Find the standard deviation of the ages.', n3(math.sqrt(v)), f'M1 {ss}/{n} − {pn(dn(Fr(s, n)))}²; A1 {n3(math.sqrt(v))}'),
        P('Find Σx and Σx².', f'Σx = {sx}; Σx² = {sxx}', f'B1 Σx = {sx}; M1 Σx² = Σ(x − {a})² + 2 × {a}Σx − {n} × {a}²; A1 {sxx}'),
        P(f'A new member aged {extra} joins the club. Find the new standard deviation.', n3(math.sqrt(v2)), f'M1 new Σx = {sx + extra}, Σx² = {sxx + extra * extra}; M1 formula with n = {n + 1}; A1 {n3(math.sqrt(v2))}'),
    ]
    return cmp_(r, intro, parts)


v123.add('C4', (2, 3, 4, 5))(v123_c4)

CHAPTERS[12] = [v121, v122, v123]


# ================================================================ Chapter 13 Probability

def pr(x):
    """Probability display: short decimals exactly, otherwise a fraction (or 3 s.f. if the fraction is unwieldy)."""
    x = Fr(x)
    d = x.denominator
    t = d
    while t % 2 == 0:
        t //= 2
    while t % 5 == 0:
        t //= 5
    if t == 1 and len(f'{float(x):.6f}'.rstrip('0').split('.')[-1]) <= 3:
        return dn(x)
    if d < 10000:
        return num(x)
    return n3(float(x))


def prs(x):
    """Fraction with a 3 s.f. decimal alongside when it is not a short decimal."""
    s = pr(x)
    return s if '/' not in s else f'{s} (≈ {n3(float(x))})'


DICE = [(6, 'two fair six-sided dice'), (4, 'two fair four-sided dice, numbered 1 to 4,'), (5, 'two fair five-sided spinners, numbered 1 to 5,'), (8, 'two fair eight-sided dice, numbered 1 to 8,')]


def dice_events(s):
    ev = []
    for k in range(3, 2 * s):
        ev.append((f'the sum of the scores is {k}', lambda a, b, k=k: a + b == k))
    for k in range(3, 2 * s - 1):
        ev.append((f'the sum of the scores is greater than {k}', lambda a, b, k=k: a + b > k))
    for d in range(1, s - 1):
        ev.append((f'the difference between the scores is {d}', lambda a, b, d=d: abs(a - b) == d))
    ev += [('the product of the scores is even', lambda a, b: a * b % 2 == 0), ('the product of the scores is odd', lambda a, b: a * b % 2 == 1),
           ('both scores are the same', lambda a, b: a == b), (f'at least one score is {s}', lambda a, b: a == s or b == s),
           ('the first score is greater than the second', lambda a, b: a > b), ('both scores are odd', lambda a, b: a % 2 == 1 and b % 2 == 1),
           ('the sum of the scores is a prime number', lambda a, b: a + b in (2, 3, 5, 7, 11, 13)), ('the first score is even', lambda a, b: a % 2 == 0),
           ('the sum of the scores is a multiple of 3', lambda a, b: (a + b) % 3 == 0), ('the product of the scores is a square number', lambda a, b: int(math.isqrt(a * b)) ** 2 == a * b)]
    return ev


def dprob(s, f):
    return Fr(sum(1 for a in range(1, s + 1) for b in range(1, s + 1) if f(a, b)), s * s)


def two_events(r, s):
    ev = dice_events(s)
    for _ in range(30):
        (na, fa), (nb, fb) = r.sample(ev, 2)
        pa, pb = dprob(s, fa), dprob(s, fb)
        if 0 < pa < 1 and 0 < pb < 1:
            pab = dprob(s, lambda a, b: fa(a, b) and fb(a, b))
            return na, nb, pa, pb, pab
    return None


p131 = T('Sample spaces, mutually exclusive and exhaustive events', 'sample spaces', 'mutually exclusive', 'exhaustive events')
p131.fixed('C1', (1, 2), [
    ('Two events are mutually exclusive if', 'they cannot both happen at the same time', 'P(A ∩ B) = 0.', ['they are equally likely', 'one causes the other', 'P(A) + P(B) = 1']),
    ('A set of events is exhaustive if', 'together they include every possible outcome', 'Their union is the whole sample space.', ['they are all equally likely', 'none of them can happen', 'they are independent']),
    ('How many outcomes are in the sample space when two fair six-sided dice are thrown?', '36', '6 × 6 = 36.', ['12', '11', '21']),
    ('For mutually exclusive events A and B, P(A ∪ B) equals', 'P(A) + P(B)', 'There is no overlap to subtract.', ['P(A) × P(B)', 'P(A) + P(B) − 1', '1 − P(A) × P(B)']),
    ('If P(A) = 0.35, then P(A′) equals', '0.65', 'P(A′) = 1 − P(A).', ['0.35', '0.135', '1.35']),
])
p131.fixed('C2', (2, 3), [
    ('Explain why the events "a card is a heart" and "a card is a king" are not mutually exclusive when one card is drawn from a standard pack.', 'The king of hearts belongs to both events, so they can happen at the same time.', 'B1 identifies king of hearts; B1 so P(A ∩ B) ≠ 0 [2]'),
    ('Explain why the events "the score is even" and "the score is odd" for one throw of a die are both mutually exclusive and exhaustive.', 'A score cannot be both even and odd, and every score is one or the other, so P(even) + P(odd) = 1.', 'B1 cannot both occur; B1 cover all outcomes [2]'),
])


@p131.add('C1', (1, 2, 3))
def p131_c1(r, D):
    s, desc = r.choice(DICE[:2] if D < 3 else DICE)
    na, fa = r.choice(dice_events(s))
    p = dprob(s, fa)
    if not 0 < p < 1:
        return None
    return MC(r, f'{desc.capitalize()} are {'spun' if 'spinner' in desc else 'thrown'}. Find the probability that {na}.', pr(p),
              [pr(1 - p), pr(Fr(p.numerator, s * s) if p.denominator != s * s else p + Fr(1, s * s)), pr(Fr(sum(1 for a in range(1, s + 1) for b in range(1, s + 1) if fa(a, b)), 2 * s)) if sum(1 for a in range(1, s + 1) for b in range(1, s + 1) if fa(a, b)) < 2 * s else pr(p / 2), pr(p * p)],
              f'Count outcomes in the {s} × {s} sample space: {pr(p)}.')


@p131.add('C1', (1, 2))
def p131_c1b(r, D):
    k = r.choice([3, 4])
    ps = [Fr(r.randint(5, 30), 100) for _ in range(k - 1)]
    if sum(ps) >= 1:
        return None
    last = 1 - sum(ps)
    labels = ['red', 'blue', 'green', 'yellow'][:k]
    lst = lambda xs: ', '.join(xs[:-1]) + ' or ' + xs[-1]
    lsa = lambda xs: ', '.join(xs[:-1]) + ' and ' + xs[-1]
    return MC(r, 'A spinner can land on ' + lst(labels) + '. The probabilities of ' + lsa(labels[:-1]) + ' are ' + lsa([dn(p) for p in ps]) + f' respectively. Find the probability that it lands on {labels[-1]}.', dn(last),
              [dn(sum(ps)), dn(Fr(1, k)), dn(abs(last - Fr(1, 10))) if last != Fr(1, 10) else dn(last + Fr(1, 10)), dn(1 - ps[0])], f'The outcomes are exhaustive: 1 − {dn(sum(ps))} = {dn(last)}.')


@p131.add('C2', (2, 3, 4), 'explain')
def p131_me(r, D):
    s, desc = r.choice(DICE)
    x = two_events(r, s)
    if not x:
        return None
    na, nb, pa, pb, pab = x
    me = pab == 0
    return Q(f'{desc.capitalize()} are {'spun' if 'spinner' in desc else 'thrown'}. Event A is "{na}" and event B is "{nb}". Determine, with a reason, whether A and B are mutually exclusive.',
             'A and B are mutually exclusive, since no outcome satisfies both' if me else f'not mutually exclusive: P(A ∩ B) = {pr(pab)} ≠ 0, since some outcomes satisfy both',
             'B1 considers outcomes in both events; B1 correct conclusion with reason')


@p131.add('C2', (2, 3, 4), 'explain')
def p131_err(r, D):
    s, desc = r.choice(DICE[:2])
    x = two_events(r, s)
    if not x:
        return None
    na, nb, pa, pb, pab = x
    if pab == 0:
        return None
    nm = person(r)
    return Q(f'{desc.capitalize()} are {'spun' if 'spinner' in desc else 'thrown'}. {nm} says P({na} or {nb}) = {pr(pa)} + {pr(pb)} = {pr(pa + pb)}. Explain the error and find the correct probability.',
             f'The events are not mutually exclusive, so outcomes in both have been counted twice; P = {pr(pa)} + {pr(pb)} − {pr(pab)} = {pr(pa + pb - pab)}.',
             f'B1 not mutually exclusive / double counting; M1 subtracts P(A ∩ B) = {pr(pab)}; A1 {pr(pa + pb - pab)}')


@p131.add('C3', (1, 2, 3, 4, 5), 'numerical')
def p131_calc(r, D):
    if D <= 2:
        s, desc = r.choice(DICE[:2])
        ev = dice_events(s)
        (na, fa) = r.choice(ev)
        p = dprob(s, fa)
        if not 0 < p < 1:
            return None
        return Q(f'{desc.capitalize()} are {'spun' if 'spinner' in desc else 'thrown'}. Draw up the sample space, and find the probability that {na}.', pr(p),
                 f'M1 sample space of {s * s} equally likely outcomes; M1 counts {p * s * s} favourable outcomes; A1 {pr(p)}')
    if D == 3:
        k = r.choice([3, 4, 5])
        a = Fr(r.randint(1, 4))
        coeffs = [r.randint(1, 4) for _ in range(k)]
        tot = sum(coeffs)
        cons = [Fr(r.randint(0, 3), 20) for _ in range(k)]
        rem = 1 - sum(cons)
        if rem <= 0:
            return None
        p = rem / tot
        probs = [c * p + d for c, d in zip(coeffs, cons)]
        labels = ['A', 'B', 'C', 'D', 'E'][:k]
        desc = '; '.join(f'P({l}) = ' + (f'{c}p' if c > 1 else 'p') + (f' + {dn(d)}' if d else '') for l, c, d in zip(labels, coeffs, cons))
        return Q(f'The events {", ".join(labels[:-1])} and {labels[-1]} are mutually exclusive and exhaustive, with {desc}. Find p.', pr(p),
                 f'M1 probabilities sum to 1; M1 {tot}p + {dn(sum(cons))} = 1; A1 p = {pr(p)}')
    s, desc = r.choice(DICE)
    x = two_events(r, s)
    if not x:
        return None
    na, nb, pa, pb, pab = x
    return Q(f'{desc.capitalize()} are {'spun' if 'spinner' in desc else 'thrown'}. Event A is "{na}" and event B is "{nb}". Find P(A), P(B) and P(A ∪ B).', f'P(A) = {pr(pa)}; P(B) = {pr(pb)}; P(A ∪ B) = {pr(pa + pb - pab)}',
             f'B1 P(A) = {pr(pa)}; B1 P(B) = {pr(pb)}; M1 P(A) + P(B) − P(A ∩ B) with P(A ∩ B) = {pr(pab)}; A1 {pr(pa + pb - pab)}')


@p131.add('C3', (2, 3, 4), 'numerical')
def p131_cards(r, D):
    n = r.randint(8, 20)
    ev = [('a multiple of 3', lambda x: x % 3 == 0), ('a multiple of 4', lambda x: x % 4 == 0), ('a multiple of 5', lambda x: x % 5 == 0), ('even', lambda x: x % 2 == 0),
          ('a prime number', lambda x: x in (2, 3, 5, 7, 11, 13, 17, 19)), ('a square number', lambda x: x in (1, 4, 9, 16)), (f'greater than {n // 2}', lambda x: x > n // 2), ('odd', lambda x: x % 2 == 1)]
    (na, fa), (nb, fb) = r.sample(ev, 2)
    A = [x for x in range(1, n + 1) if fa(x)]
    B = [x for x in range(1, n + 1) if fb(x)]
    AB = [x for x in A if x in B]
    U = len(set(A) | set(B))
    return Q(f'A card is chosen at random from {n} cards numbered 1 to {n}. A is the event "the number is {na}" and B is the event "the number is {nb}". Find P(A ∪ B) and state whether A and B are mutually exclusive.',
             f'P(A ∪ B) = {pr(Fr(U, n))}; ' + ('mutually exclusive' if not AB else f'not mutually exclusive (both contain {", ".join(map(str, AB))})'),
             f'B1 lists A and B; M1 {len(A)}/{n} + {len(B)}/{n} − {len(AB)}/{n}; A1 {pr(Fr(U, n))}; B1 conclusion')


def p131_c4(r, D):
    s, desc = r.choice(DICE)
    x = two_events(r, s)
    if not x:
        return None
    na, nb, pa, pb, pab = x
    intro = f'{desc.capitalize()} are {'spun' if 'spinner' in desc else 'thrown'}. Event A is "{na}" and event B is "{nb}".'
    parts = [
        P('Write down the number of outcomes in the sample space.', str(s * s), f'B1 {s} × {s}'),
        P('Find P(A).', pr(pa), f'M1 counts outcomes; A1 {pr(pa)}'),
        P('Find P(B).', pr(pb), f'M1 counts outcomes; A1 {pr(pb)}'),
        P('Find P(A ∩ B).', pr(pab), f'B1 {pr(pab)}'),
        P('Find P(A ∪ B).', pr(pa + pb - pab), f'M1 P(A) + P(B) − P(A ∩ B); A1 {pr(pa + pb - pab)}'),
        P('State, with a reason, whether A and B are mutually exclusive.', 'yes, P(A ∩ B) = 0' if pab == 0 else f'no, P(A ∩ B) = {pr(pab)} ≠ 0', 'B1 conclusion with reason'),
    ]
    return cmp_(r, intro, parts)


p131.add('C4', (2, 3, 4, 5))(p131_c4)


p132 = T('Independent events and the addition and multiplication laws', 'independent events', 'addition law', 'multiplication law')
p132.fixed('C1', (1, 2), [
    ('Events A and B are independent if', 'P(A ∩ B) = P(A) × P(B)', 'The occurrence of one does not affect the other.', ['P(A ∩ B) = 0', 'P(A) + P(B) = 1', 'P(A ∪ B) = P(A) + P(B)']),
    ('The addition law states that P(A ∪ B) =', 'P(A) + P(B) − P(A ∩ B)', 'Subtract the overlap counted twice.', ['P(A) + P(B)', 'P(A) × P(B)', 'P(A) + P(B) + P(A ∩ B)']),
    ('If A and B are independent with P(A) = 0.5 and P(B) = 0.4, then P(A ∩ B) =', '0.2', '0.5 × 0.4.', ['0.9', '0.7', '0.1']),
    ('Two events with non-zero probabilities that are mutually exclusive', 'cannot be independent', 'P(A ∩ B) = 0 but P(A)P(B) > 0.', ['must be independent', 'have P(A) = P(B)', 'are always exhaustive']),
])
p132.fixed('C2', (2, 3), [
    ('Explain why two mutually exclusive events with non-zero probabilities cannot be independent.', 'If they are mutually exclusive then P(A ∩ B) = 0, but P(A) × P(B) > 0, so P(A ∩ B) ≠ P(A)P(B).', 'B1 P(A ∩ B) = 0; B1 compares with P(A)P(B) > 0 [2]'),
    ('Explain why the results of two separate throws of a fair coin are independent.', 'The coin has no memory: the outcome of the first throw does not change the probabilities for the second.', 'B1 first does not affect second; B1 probabilities unchanged [2]'),
])


def rp(r, lo=1, hi=9):
    return Fr(r.randint(lo, hi), 10)


@p132.add('C1', (1, 2, 3))
def p132_c1(r, D):
    pa, pb = Fr(r.randint(1, 19), 20), Fr(r.randint(1, 19), 20)
    kind = r.choice(['and', 'or', 'neither'])
    if kind == 'and':
        return MC(r, f'Events A and B are independent with P(A) = {dn(pa)} and P(B) = {dn(pb)}. Find P(A ∩ B).', dn(pa * pb), [dn(pa + pb) if pa + pb <= 1 else dn(abs(pa - pb)), dn(pa + pb - pa * pb), dn((1 - pa) * (1 - pb)), dn(pa * (1 - pb))], f'{dn(pa)} × {dn(pb)} = {dn(pa * pb)}.')
    if kind == 'or':
        return MC(r, f'Events A and B are independent with P(A) = {dn(pa)} and P(B) = {dn(pb)}. Find P(A ∪ B).', dn(pa + pb - pa * pb), [dn(pa * pb), dn(1 - pa * pb), dn((1 - pa) * (1 - pb)), dn(pa + pb) if pa + pb <= 1 else dn(1 - (1 - pa) * pb)], f'{dn(pa)} + {dn(pb)} − {dn(pa * pb)} = {dn(pa + pb - pa * pb)}.')
    return MC(r, f'Events A and B are independent with P(A) = {dn(pa)} and P(B) = {dn(pb)}. Find the probability that neither A nor B occurs.', dn((1 - pa) * (1 - pb)), [dn(1 - pa * pb), dn(pa * pb), dn(abs(1 - pa - pb)) if pa + pb != 1 else dn(pa * (1 - pb)), dn(pa + pb - pa * pb)], f'(1 − {dn(pa)})(1 − {dn(pb)}) = {dn((1 - pa) * (1 - pb))}.')


@p132.add('C1', (2, 3))
def p132_c1b(r, D):
    pa, pb = rp(r), rp(r)
    pab = rp(r, 1, 5) / 2
    if pab > min(pa, pb) or pa + pb - pab > 1:
        return None
    return MC(r, f'P(A) = {dn(pa)}, P(B) = {dn(pb)} and P(A ∩ B) = {dn(pab)}. Find P(A ∪ B).', dn(pa + pb - pab), [dn(pa + pb) if pa + pb <= 1 else dn(pa + pb - 2 * pab), dn(pa * pb), dn(pa + pb - pa * pb) if pa * pb != pab else dn(1 - pab), dn(1 - pab) if 1 - pab != pa + pb - pab else dn(pab)],
              f'{dn(pa)} + {dn(pb)} − {dn(pab)} = {dn(pa + pb - pab)}.')


@p132.add('C2', (2, 3, 4), 'explain')
def p132_test(r, D):
    if r.random() < 0.5:
        s, desc = r.choice(DICE)
        x = two_events(r, s)
        if not x:
            return None
        na, nb, pa, pb, pab = x
        ind = pab == pa * pb
        return Q(f'{desc.capitalize()} are {'spun' if 'spinner' in desc else 'thrown'}. Event A is "{na}" and event B is "{nb}". Determine whether A and B are independent, justifying your answer.',
                 f'P(A) = {pr(pa)}, P(B) = {pr(pb)}, P(A ∩ B) = {pr(pab)}; P(A) × P(B) = {pr(pa * pb)}, ' + ('equal, so independent' if ind else 'not equal, so not independent'),
                 f'M1 finds P(A ∩ B) = {pr(pab)} and P(A)P(B) = {pr(pa * pb)}; A1 correct conclusion')
    pa, pb = Fr(r.randint(1, 19), 20), Fr(r.randint(1, 19), 20)
    ind = r.random() < 0.5
    pab = pa * pb if ind else pa * pb + r.choice([Fr(1, 20), Fr(-1, 20), Fr(1, 10)])
    if pab <= 0 or pab > min(pa, pb) or pa + pb - pab > 1:
        return None
    return Q(f'For events A and B, P(A) = {dn(pa)}, P(B) = {dn(pb)} and P(A ∩ B) = {dn(pab)}. Determine whether A and B are independent.',
             f'P(A) × P(B) = {dn(pa * pb)}, ' + ('which equals P(A ∩ B), so A and B are independent' if ind else f'which is not equal to {dn(pab)}, so A and B are not independent'),
             f'M1 P(A) × P(B) = {dn(pa * pb)}; A1 compares with P(A ∩ B) and concludes')


@p132.add('C2', (2, 3), 'explain')
def p132_err(r, D):
    p = Fr(r.randint(1, 9), 10)
    n = r.choice([2, 3, 4, 5])
    nm = person(r)
    what = r.choice(['hits the target', 'passes a quality check', 'arrives on time', 'scores a goal from a penalty'])
    return Q(f'Each attempt independently {what} with probability {dn(p)}. {nm} says the probability of succeeding at least once in {n} attempts is {n} × {dn(p)} = {dn(n * p)}. Explain why this is wrong and find the correct probability.',
             f'Adding probabilities double counts outcomes with more than one success (and can exceed 1); P(at least one) = 1 − {dn(1 - p)}{sup(n)} = {n3(float(1 - (1 - p) ** n))}.',
             f'B1 events not mutually exclusive / double counting; M1 1 − (1 − {dn(p)}){sup(n)}; A1 {n3(float(1 - (1 - p) ** n))}')


@p132.add('C3', (1, 2, 3, 4, 5), 'numerical')
def p132_calc(r, D):
    if D <= 2:
        pa, pb = Fr(r.randint(1, 19), 20), Fr(r.randint(1, 19), 20)
        return Q(f'Events A and B are independent, with P(A) = {dn(pa)} and P(B) = {dn(pb)}. Find P(A ∪ B) and the probability that exactly one of A and B occurs.',
                 f'P(A ∪ B) = {dn(pa + pb - pa * pb)}; P(exactly one) = {dn(pa + pb - 2 * pa * pb)}',
                 f'M1 P(A ∩ B) = {dn(pa * pb)}; A1 P(A ∪ B) = {dn(pa + pb - pa * pb)}; M1 P(A ∩ B′) + P(A′ ∩ B); A1 {dn(pa + pb - 2 * pa * pb)}')
    if D == 3:
        pa = Fr(r.randint(1, 9), 10)
        pb = Fr(r.randint(1, 9), 10)
        u = pa + pb - pa * pb
        return Q(f'Events A and B are independent. P(A) = {dn(pa)} and P(A ∪ B) = {dn(u)}. Find P(B).', dn(pb),
                 f'M1 {dn(pa)} + p − {dn(pa)}p = {dn(u)}; M1 solves for p; A1 P(B) = {dn(pb)}')
    if D == 4:
        p = Fr(r.randint(5, 95), 100)
        n = r.randint(3, 8)
        what = r.choice(['a light bulb is faulty', 'a seed germinates', 'a train is late', 'a customer buys a coffee'])
        return Q(f'The probability that {what} is {dn(p)}, independently for each case. For {n} cases, find the probability that this happens at least once.', n4(float(1 - (1 - p) ** n)) if 1 - (1 - p) ** n > 0.9995 else n3(float(1 - (1 - p) ** n)),
                 f'M1 1 − P(none); M1 (1 − {dn(p)}){sup(n)}; A1 {n3(float(1 - (1 - p) ** n))}')
    p = Fr(r.randint(5, 60), 100)
    tgt = r.choice([Fr(9, 10), Fr(95, 100), Fr(99, 100)])
    n = 1
    while 1 - (1 - p) ** n < tgt:
        n += 1
    what = r.choice(['an archer hits the bullseye', 'a ticket wins a prize', 'a phone call is answered'])
    return Q(f'The probability that {what} is {dn(p)} on each independent attempt. Find the least number of attempts for the probability of at least one success to exceed {dn(tgt)}.', str(n),
             f'M1 1 − {dn(1 - p)}ⁿ > {dn(tgt)}; M1 trial or logarithms; A1 n = {n}')


@p132.add('C3', (2, 3, 4), 'numerical')
def p132_two(r, D):
    nm1, nm2 = two_people(r)
    p1, p2 = Fr(r.randint(2, 9), 10), Fr(r.randint(2, 9), 10)
    kind = r.choice(['exactly', 'atleast', 'first'])
    if kind == 'exactly':
        ans = p1 * (1 - p2) + p2 * (1 - p1)
        q = 'exactly one of them passes'
        k = f'M1 {dn(p1)} × {dn(1 - p2)} + {dn(1 - p1)} × {dn(p2)}; A1 {dn(ans)}'
    elif kind == 'atleast':
        ans = 1 - (1 - p1) * (1 - p2)
        q = 'at least one of them passes'
        k = f'M1 1 − {dn(1 - p1)} × {dn(1 - p2)}; A1 {dn(ans)}'
    else:
        ans = p1 * (1 - p2)
        q = f'{nm1} passes and {nm2} fails'
        k = f'M1 {dn(p1)} × {dn(1 - p2)}; A1 {dn(ans)}'
    return Q(f'{nm1} and {nm2} take a driving test independently. The probability that {nm1} passes is {dn(p1)} and the probability that {nm2} passes is {dn(p2)}. Find the probability that {q}.', dn(ans), k)


def p132_c4(r, D):
    s, desc = r.choice(DICE)
    x = two_events(r, s)
    if not x:
        return None
    na, nb, pa, pb, pab = x
    ind = pab == pa * pb
    intro = f'{desc.capitalize()} are {'spun' if 'spinner' in desc else 'thrown'}. Event A is "{na}" and event B is "{nb}".'
    parts = [
        P('Find P(A) and P(B).', f'{pr(pa)}, {pr(pb)}', f'B1 P(A) = {pr(pa)}; B1 P(B) = {pr(pb)}'),
        P('Find P(A ∩ B).', pr(pab), f'B1 {pr(pab)}'),
        P('Determine whether A and B are independent.', ('independent' if ind else 'not independent') + f': P(A)P(B) = {pr(pa * pb)}', 'M1 compares P(A ∩ B) with P(A)P(B); A1 conclusion'),
        P('Find P(A ∪ B).', pr(pa + pb - pab), f'M1 addition law; A1 {pr(pa + pb - pab)}'),
        P('Find P(A′ ∩ B′).', pr(1 - (pa + pb - pab)), f'M1 1 − P(A ∪ B); A1 {pr(1 - (pa + pb - pab))}'),
    ]
    return cmp_(r, intro, parts)


p132.add('C4', (2, 3, 4, 5))(p132_c4)


@p132.add('C4', (3, 4, 5))
def p132_c4b(r, D):
    pa = Fr(r.randint(1, 9), 10)
    pb = Fr(r.randint(1, 9), 10)
    pc = Fr(r.randint(1, 9), 10)
    nm = person(r)
    intro = f'{nm} takes three independent tests. The probabilities of passing them are {dn(pa)}, {dn(pb)} and {dn(pc)} respectively.'
    allp = pa * pb * pc
    none = (1 - pa) * (1 - pb) * (1 - pc)
    one = pa * (1 - pb) * (1 - pc) + (1 - pa) * pb * (1 - pc) + (1 - pa) * (1 - pb) * pc
    parts = [
        P(f'Find the probability that {nm} passes all three tests.', dn(allp), f'M1 product; A1 {dn(allp)}'),
        P(f'Find the probability that {nm} passes none of the tests.', dn(none), f'M1 {dn(1 - pa)} × {dn(1 - pb)} × {dn(1 - pc)}; A1 {dn(none)}'),
        P(f'Find the probability that {nm} passes exactly one test.', dn(one), f'M1 three cases; M1 sums products; A1 {dn(one)}'),
        P(f'Find the probability that {nm} passes at least one test.', dn(1 - none), f'M1 1 − P(none); A1 {dn(1 - none)}'),
    ]
    return cmp_(r, intro, parts)


p133 = T('Conditional probability P(A∣B) = P(A ∩ B)/P(B)', 'conditional probability', 'tree diagrams', 'P(A∣B)')
p133.fixed('C1', (1, 2), [
    ('P(A∣B) is defined as', 'P(A ∩ B)/P(B)', 'Restrict the sample space to B.', ['P(A ∩ B)/P(A)', 'P(A) × P(B)', 'P(B)/P(A)']),
    ('If A and B are independent then P(A∣B) equals', 'P(A)', 'Knowing B occurred does not change the probability of A.', ['P(B)', 'P(A ∩ B)', '1']),
    ('If P(A ∩ B) = 0.12 and P(B) = 0.4, then P(A∣B) =', '0.3', '0.12 ÷ 0.4.', ['0.048', '0.52', '0.28']),
    ('A bag has 3 red and 5 blue counters. One is taken and not replaced. Given that it was red, the probability that the next is red is', '2/7', 'Two reds remain out of seven counters.', ['3/8', '3/7', '2/8']),
])
p133.fixed('C2', (2, 3), [
    ('Explain the difference between P(A∣B) and P(B∣A) using the events A = "a person is a doctor" and B = "a person owns a stethoscope".', 'P(B∣A) is the probability that a doctor owns a stethoscope, which is high; P(A∣B) is the probability that a stethoscope owner is a doctor, which may be different.', 'B1 interprets both in context; B1 they are not equal in general [2]'),
    ('Explain how a tree diagram shows that the second selection depends on the first when counters are taken without replacement.', 'The probabilities on the second set of branches change depending on which counter was taken first, as there is one fewer of that colour.', 'B1 second-branch probabilities differ; B1 reason: one fewer of that colour [2]'),
])

TWOWAY = [('students', 'study Physics', 'do not study Physics', 'studies Physics', 'does not study Physics', 'boys', 'girls'),
          ('employees', 'cycle to work', 'do not cycle to work', 'cycles to work', 'does not cycle to work', 'full-time employees', 'part-time employees'),
          ('patients', 'had the vaccine', 'did not have the vaccine', 'had the vaccine', 'did not have the vaccine', 'patients under 50', 'patients aged 50 or over'),
          ('visitors', 'bought a ticket online', 'bought a ticket at the gate', 'bought a ticket online', 'bought a ticket at the gate', 'adults', 'children'),
          ('members of a gym', 'swim', 'do not swim', 'swims', 'does not swim', 'men', 'women')]


def twoway(r):
    a, b, c, d = (r.randint(5, 60) for _ in range(4))
    return a, b, c, d


@p133.add('C1', (1, 2, 3))
def p133_c1(r, D):
    pb = Fr(r.randint(2, 9), 10)
    pab = Fr(r.randint(1, 9), 100) * r.choice([1, 2, 5])
    if pab >= pb:
        return None
    return MC(r, f'P(A ∩ B) = {dn(pab)} and P(B) = {dn(pb)}. Find P(A∣B)' + (', correct to 3 significant figures.' if (pab / pb).denominator not in (1, 2, 4, 5, 8, 10, 20, 25, 40, 50, 100) else '.'), dn(pab / pb),
              [dn(pab * pb), dn(pb / pab) if pb / pab < 1 else dn(pb - pab), dn(pb - pab), dn(pab + pb) if pab + pb <= 1 else dn(1 - pab / pb)], f'{dn(pab)} ÷ {dn(pb)} = {dn(pab / pb)}.')


@p133.add('C1', (2, 3))
def p133_c1b(r, D):
    ctx = r.choice(TWOWAY)
    a, b, c, d = twoway(r)
    tot = a + b + c + d
    return MC(r, f'Of a group of {ctx[0]}, {a} {ctx[5]} and {c} {ctx[6]} {ctx[1]}; {b} {ctx[5]} and {d} {ctx[6]} {ctx[2]}. One of these {ctx[0]} is chosen at random. Given that the person chosen is one of the {ctx[5]}, find the probability that this person {ctx[3]}.',
              pr(Fr(a, a + b)), [pr(Fr(a, tot)), pr(Fr(a, a + c)), pr(Fr(b, a + b)), pr(Fr(a + b, tot))], f'{a} out of the {a + b} {ctx[5]}: {pr(Fr(a, a + b))}.')


@p133.add('C2', (2, 3, 4), 'explain')
def p133_err(r, D):
    ctx = r.choice(TWOWAY)
    a, b, c, d = twoway(r)
    nm = person(r)
    return Q(f'Of a group of {ctx[0]}, {a} {ctx[5]} and {c} {ctx[6]} {ctx[1]}; {b} {ctx[5]} and {d} {ctx[6]} {ctx[2]}. {nm} says that the probability that a randomly chosen person who {ctx[3]} is one of the {ctx[5]} is {pr(Fr(a, a + b))}. Explain the error and find the correct probability.',
             f'{nm} has divided by the {a + b} {ctx[5]}, finding the probability that one of the {ctx[5]} {ctx[3]}; the condition is that the person {ctx[3]}, so divide by {a + c}: {pr(Fr(a, a + c))}.',
             f'B1 conditioned on the wrong event; B1 {a}/{a + c} = {pr(Fr(a, a + c))}')


@p133.add('C2', (3, 4), 'explain')
def p133_ind(r, D):
    pa = Fr(r.randint(2, 8), 10)
    pb = Fr(r.randint(2, 8), 10)
    ind = r.random() < 0.5
    pab = pa * pb if ind else pa * pb + r.choice([Fr(1, 25), Fr(-1, 25)])
    if pab <= 0:
        return None
    cond = pab / pb
    return Q(f'For events A and B, P(A) = {dn(pa)}, P(B) = {dn(pb)} and P(A ∩ B) = {dn(pab)}. Find P(A∣B) and use it to decide whether A and B are independent.',
             f'P(A∣B) = {dn(cond) if cond.denominator in (1, 2, 4, 5, 8, 10, 20, 25, 40, 50, 100) else n3(float(cond))}; ' + ('this equals P(A), so independent' if ind else f'this is not equal to P(A) = {dn(pa)}, so not independent'),
             f'M1 {dn(pab)} ÷ {dn(pb)}; A1 compares with P(A) and concludes')


def tree(r):
    p = Fr(r.randint(1, 9), 10)
    q1 = Fr(r.randint(1, 19), 20)
    q2 = Fr(r.randint(1, 19), 20)
    return p, q1, q2


TREE_CTX = [('it rains on a given day', 'it does not rain', '{nm} is late for school', '{nm} is not late for school'),
            ('a component comes from factory A', 'it comes from factory B', 'the component is faulty', 'the component is not faulty'),
            ('{nm} takes the bus', '{nm} walks', '{nm} arrives before 8 am', '{nm} does not arrive before 8 am'),
            ('a patient has the condition', 'the patient does not have the condition', 'the test is positive', 'the test is negative'),
            ('{nm} revises for a test', '{nm} does not revise', '{nm} passes the test', '{nm} fails the test')]


@p133.add('C3', (1, 2, 3, 4, 5), 'numerical')
def p133_calc(r, D):
    nm = person(r)
    c = r.choice(TREE_CTX)
    p, q1, q2 = tree(r)
    if q1 == q2:
        return None
    ev1 = c[0].format(nm=nm)
    ev2 = c[2].format(nm=nm)
    pB = p * q1 + (1 - p) * q2
    stem = f'The probability that {ev1} is {dn(p)}. If so, the probability that {ev2} is {dn(q1)}; otherwise it is {dn(q2)}.'
    if D <= 2:
        return Q(stem + f' Find the probability that {ev2}.', dn(pB), f'M1 {dn(p)} × {dn(q1)} + {dn(1 - p)} × {dn(q2)}; A1 {dn(pB)}')
    if D == 3:
        return Q(stem + f' Find the probability that {ev1}, given that {ev2}.', prs(p * q1 / pB) if (p * q1 / pB).denominator > 1000 or '/' in pr(p * q1 / pB) else pr(p * q1 / pB),
                 f'M1 P(both) = {dn(p * q1)}; M1 P({ev2}) = {dn(pB)}; A1 {pr(p * q1 / pB)}')
    alt = (1 - p) * (1 - q2) / (1 - pB)
    return Q(stem + f' Find the probability that {c[1].format(nm=nm)}, given that {c[3].format(nm=nm)}.',
             pr(alt) if '/' not in pr(alt) else prs(alt), f'M1 P(neither event happens) = {dn(1 - p)} × {dn(1 - q2)} = {dn((1 - p) * (1 - q2))}; M1 P({c[3].format(nm=nm)}) = {dn(1 - pB)}; A1 {pr(alt)}')


@p133.add('C3', (2, 3, 4, 5), 'numerical')
def p133_bag(r, D):
    a, b = r.randint(2, 9), r.randint(2, 9)
    c1, c2 = r.choice([('red', 'blue'), ('green', 'yellow'), ('black', 'white')])
    tot = a + b
    kind = r.choice(['same', 'second', 'first_given_second'])
    if kind == 'same':
        ans = Fr(a * (a - 1) + b * (b - 1), tot * (tot - 1))
        return Q(f'A bag contains {a} {c1} and {b} {c2} counters. Two counters are taken at random without replacement. Find the probability that they are the same colour.', pr(ans),
                 f'M1 {a}/{tot} × {a - 1}/{tot - 1}; M1 + {b}/{tot} × {b - 1}/{tot - 1}; A1 {pr(ans)}')
    if kind == 'second':
        return Q(f'A bag contains {a} {c1} and {b} {c2} counters. Two counters are taken at random without replacement. Find the probability that the second counter is {c1}.', pr(Fr(a, tot)),
                 f'M1 {a}/{tot} × {a - 1}/{tot - 1} + {b}/{tot} × {a}/{tot - 1}; A1 {pr(Fr(a, tot))}')
    ans = Fr(a - 1, tot - 1)
    return Q(f'A bag contains {a} {c1} and {b} {c2} counters. Two counters are taken at random without replacement. Given that the second counter is {c1}, find the probability that the first counter was also {c1}.', pr(ans),
             f'M1 P(both {c1}) = {pr(Fr(a * (a - 1), tot * (tot - 1)))}; M1 P(second {c1}) = {pr(Fr(a, tot))}; A1 {pr(ans)}')


def p133_c4(r, D):
    nm = person(r)
    c = r.choice(TREE_CTX)
    p, q1, q2 = tree(r)
    if q1 == q2:
        return None
    ev1 = c[0].format(nm=nm)
    ev2 = c[2].format(nm=nm)
    pB = p * q1 + (1 - p) * q2
    intro = f'The probability that {ev1} is {dn(p)}. If so, the probability that {ev2} is {dn(q1)}; otherwise it is {dn(q2)}.'
    parts = [
        P('Draw a tree diagram and write the probability on each branch.', f'{dn(p)}, {dn(1 - p)}; then {dn(q1)}, {dn(1 - q1)} and {dn(q2)}, {dn(1 - q2)}', 'B1 first branches; B1 second branches'),
        P(f'Find the probability that {ev2}.', dn(pB), f'M1 sum of two products; A1 {dn(pB)}'),
        P(f'Find the probability that {ev1}, given that {ev2}.', pr(p * q1 / pB), f'M1 {dn(p * q1)} ÷ {dn(pB)}; A1 {pr(p * q1 / pB)}'),
        P('Find the probability that exactly one of the two events happens.', dn(p * (1 - q1) + (1 - p) * q2), f'M1 {dn(p)} × {dn(1 - q1)} + {dn(1 - p)} × {dn(q2)}; A1 {dn(p * (1 - q1) + (1 - p) * q2)}'),
    ]
    return cmp_(r, intro, parts)


p133.add('C4', (2, 3, 4, 5))(p133_c4)


@p133.add('C4', (3, 4, 5))
def p133_c4b(r, D):
    ctx = r.choice(TWOWAY)
    a, b, c, d = twoway(r)
    tot = a + b + c + d
    intro = f'Of a group of {tot} {ctx[0]}, {a} {ctx[5]} and {c} {ctx[6]} {ctx[1]}; {b} {ctx[5]} and {d} {ctx[6]} {ctx[2]}. One person is chosen at random.'
    parts = [
        P(f'Find the probability that the person chosen is one of the {ctx[5]}.', pr(Fr(a + b, tot)), f'B1 {a + b}/{tot}'),
        P(f'Find the probability that the person chosen is one of the {ctx[5]}, given that this person {ctx[3]}.', pr(Fr(a, a + c)), f'M1 {a}/{a + c}; A1 {pr(Fr(a, a + c))}'),
        P(f'Find the probability that the person chosen {ctx[4]}, given that this person is one of the {ctx[6]}.', pr(Fr(d, c + d)), f'M1 {d}/{c + d}; A1 {pr(Fr(d, c + d))}'),
        P(f'Determine whether the events "the person is one of the {ctx[5]}" and "the person {ctx[3]}" are independent.', 'independent' if Fr(a, a + c) == Fr(a + b, tot) else f'not independent, since {pr(Fr(a, a + c))} ≠ {pr(Fr(a + b, tot))}', 'M1 compares a conditional with an unconditional probability; A1 conclusion'),
    ]
    return cmp_(r, intro, parts)


CHAPTERS[13] = [p131, p132, p133]


# ================================================================ Chapter 14 Permutations and combinations

DISTINCT = [w for w in ['FRIDAY', 'PLANET', 'COUSIN', 'MONDAY', 'BRIGHT', 'NUMBER', 'FACTOR', 'GARDEN', 'JUMPING', 'DOLPHIN', 'CAMBRIDGE', 'TRIANGLE', 'QUESTION', 'EDUCATION', 'ALGORITHM',
                         'BLACKSMITH', 'COMPLEX', 'HISTORY', 'PICTURE', 'DANGER', 'SQUARE', 'FLIGHT', 'CHAPTER', 'ISLAND', 'CLIMATE', 'PLASTIC', 'ORANGE', 'FIGURE', 'MARBLE', 'CANDLE'] if len(set(w)) == len(w)]
REPEAT = ['STATISTICS', 'BANANA', 'PARALLEL', 'EXCELLENT', 'COMMITTEE', 'PEPPER', 'ADDRESSES', 'TOMORROW', 'BOOKKEEPER', 'ASSESSMENT', 'CHEESES', 'REFERENCE', 'ELEVEN', 'SUCCESS', 'BALLOON',
          'COCOON', 'GRAMMAR', 'HAPPINESS', 'MAMMAL', 'DIVIDED', 'LETTER', 'CINNAMON', 'ENGINEERING', 'POSSESSION', 'ACCOMMODATE', 'CALCULATOR', 'DISAPPEAR', 'PROBABILITY', 'EXPERIMENT', 'SEPARATE',
          'BOTTLE', 'COFFEE', 'GEOMETRY', 'MATHEMATICS', 'ARRANGEMENT', 'DIFFERENT', 'REPETITION', 'INTERNET', 'ELEPHANT', 'CARAVAN']
VOW = set('AEIOU')


def ms_perm(counts):
    n = sum(counts)
    res = math.factorial(n)
    for c in counts:
        res //= math.factorial(c)
    return res


def lcounts(w):
    d = {}
    for ch in w:
        d[ch] = d.get(ch, 0) + 1
    return d


def rep_desc(w):
    d = lcounts(w)
    reps = [f'{v} {k}s' if v > 1 else '' for k, v in sorted(d.items())]
    return ', '.join(x for x in reps if x)


def word_count(w):
    return ms_perm(list(lcounts(w).values()))


def vowels_together(w):
    vs = [c for c in w if c in VOW]
    cs = [c for c in w if c not in VOW]
    if len(vs) < 2 or not cs:
        return None
    return ms_perm(list(lcounts(''.join(cs)).values()) + [1]) * ms_perm(list(lcounts(''.join(vs)).values()))


def ends_with(w, a, b):
    lst = list(w)
    if a not in lst:
        return 0
    lst.remove(a)
    if b not in lst:
        return 0
    lst.remove(b)
    return ms_perm(list(lcounts(''.join(lst)).values()))


def letter_apart(w, L):
    d = lcounts(w)
    k = d.get(L, 0)
    if k < 2:
        return None
    others = [v for kk, v in d.items() if kk != L]
    m = len(w) - k
    return ms_perm(others) * comb(m + 1, k)


c141 = T('Factorial notation and arrangements of objects in a line', 'factorial notation', 'arrangements', 'n!')
c141.fixed('C1', (1, 2), [
    ('The value of 0! is', '1', 'By definition 0! = 1.', ['0', 'undefined', '−1']),
    ('The number of ways of arranging 5 different books in a line is', '120', '5! = 120.', ['25', '5', '60']),
    ('n!/(n − 1)! simplifies to', 'n', 'n! = n × (n − 1)!.', ['n − 1', '1', 'n!']),
    ('The number of arrangements of 4 different letters taken from 7 different letters is', '840', '7 × 6 × 5 × 4 = 840.', ['35', '28', '5040']),
])
c141.fixed('C2', (2, 3), [
    ('Explain why the number of ways of arranging n different objects in a line is n!.', 'There are n choices for the first place, n − 1 for the second, and so on down to 1 for the last, giving n × (n − 1) × … × 1 = n!.', 'B1 decreasing choices for each position; B1 product is n! [2]'),
    ('Explain why ⁿPᵣ = n!/(n − r)!.', 'Choosing r objects in order gives n(n − 1)…(n − r + 1) arrangements, which is n! with the (n − r)! factors for the unused positions cancelled.', 'B1 product of r decreasing terms; B1 equals n!/(n − r)! [2]'),
])


@c141.add('C1', (1, 2, 3))
def c141_c1(r, D):
    kind = r.choice(['fact', 'ratio', 'npr', 'word'])
    if kind == 'fact':
        n = r.randint(4, 9)
        return MC(r, f'Find the value of {n}!/{n - 2}!.', str(n * (n - 1)), [str(math.factorial(2)), str(n * (n - 2)), str(math.factorial(n) // 2), str(n - 2)], f'{n}!/{n - 2}! = {n} × {n - 1} = {n * (n - 1)}.')
    if kind == 'ratio':
        n = r.randint(5, 12)
        k = r.randint(2, 3)
        v = math.factorial(n) // math.factorial(n - k)
        return MC(r, f'Find the value of {n}!/({n - k}! × {k}!).', str(comb(n, k)), [str(v), str(comb(n, k + 1)), str(n * k), str(math.factorial(k))], f'This is ⁿCᵣ with n = {n}, r = {k}: {comb(n, k)}.')
    if kind == 'npr':
        n = r.randint(5, 10)
        k = r.randint(2, 4)
        v = math.factorial(n) // math.factorial(n - k)
        return MC(r, f'In how many ways can {k} different prizes be given to {k} of {n} students, with no student receiving more than one prize?', str(v), [str(comb(n, k)), str(n ** k), str(k ** n), str(math.factorial(n))], f'{n}P{k} = {v}.')
    w = r.choice(DISTINCT)
    n = len(w)
    return MC(r, f'Find the number of different arrangements of the letters of the word {w}.', str(math.factorial(n)), [str(math.factorial(n - 1)), str(n ** 2), str(math.factorial(n) // 2), str(n ** n) if n < 7 else str(2 * math.factorial(n))], f'{n} different letters: {n}! = {math.factorial(n)}.')


@c141.add('C2', (2, 3, 4), 'explain')
def c141_err(r, D):
    n = r.randint(5, 9)
    nm = person(r)
    kind = r.choice(['sq', 'sum'])
    if kind == 'sq':
        return Q(f'{nm} says that {n} different trophies can be arranged in a line on a shelf in {n}² = {n * n} ways. Explain the error and find the correct number.',
                 f'Each trophy can be used only once, so the number of choices decreases: {n}! = {math.factorial(n)}.', f'B1 choices decrease / no repetition; B1 {math.factorial(n)}')
    k = r.randint(2, 4)
    v = math.factorial(n) // math.factorial(n - k)
    return Q(f'{nm} says that the number of ways to choose a president, a secretary{" and a treasurer" if k == 3 else ""}{", a treasurer and a captain" if k == 4 else ""} from {n} people is {n}C{k} = {comb(n, k)}. Explain the error and find the correct number.',
             f'The positions are different, so order matters: {n}P{k} = {v}.', f'B1 order matters (different roles); B1 {v}')


@c141.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c141_calc(r, D):
    w = r.choice(DISTINCT)
    n = len(w)
    vs = [c for c in w if c in VOW]
    cs = [c for c in w if c not in VOW]
    if D <= 2:
        a, b = r.sample(list(w), 2)
        v = math.factorial(n - 2)
        return Q(f'Find the number of arrangements of the letters of the word {w} which begin with {a} and end with {b}.', str(v), f'M1 fixes the two end letters; M1 ({n} − 2)!; A1 {v}')
    if D == 3:
        if len(vs) < 2:
            return None
        v = math.factorial(len(cs) + 1) * math.factorial(len(vs))
        return Q(f'Find the number of arrangements of the letters of the word {w} in which the vowels are all together.', str(v),
                 f'M1 treats the {len(vs)} vowels as one unit; M1 {len(cs) + 1}! × {len(vs)}!; A1 {v}')
    if D == 4:
        if len(vs) < 1 or len(cs) < 2:
            return None
        v = len(cs) * (len(cs) - 1) * math.factorial(n - 2)
        return Q(f'Find the number of arrangements of the letters of the word {w} which begin and end with a consonant.', str(v),
                 f'M1 {len(cs)} × {len(cs) - 1} for the ends; M1 × {n - 2}!; A1 {v}')
    if len(vs) < 2 or len(vs) > len(cs) + 1:
        return None
    v = math.factorial(len(cs)) * math.factorial(len(cs) + 1) // math.factorial(len(cs) + 1 - len(vs))
    return Q(f'Find the number of arrangements of the letters of the word {w} in which no two vowels are next to each other.', str(v),
             f'M1 arranges consonants: {len(cs)}!; M1 places vowels in {len(cs) + 1} gaps: {len(cs) + 1}P{len(vs)}; A1 {v}')


@c141.add('C3', (2, 3, 4, 5), 'numerical')
def c141_people(r, D):
    n = r.randint(5, 9)
    nm1, nm2 = two_people(r)
    kind = r.choice(['together', 'apart', 'ends', 'digits'])
    if kind == 'together':
        v = 2 * math.factorial(n - 1)
        return Q(f'{n} people, including {nm1} and {nm2}, stand in a line. Find the number of arrangements in which {nm1} and {nm2} stand next to each other.', str(v), f'M1 treats pair as one: {n - 1}!; M1 × 2; A1 {v}')
    if kind == 'apart':
        v = math.factorial(n) - 2 * math.factorial(n - 1)
        return Q(f'{n} people, including {nm1} and {nm2}, stand in a line. Find the number of arrangements in which {nm1} and {nm2} are not next to each other.', str(v), f'M1 total {n}!; M1 subtracts 2 × {n - 1}!; A1 {v}')
    if kind == 'ends':
        v = 2 * math.factorial(n - 2)
        return Q(f'{n} people, including {nm1} and {nm2}, stand in a line. Find the number of arrangements in which {nm1} and {nm2} are at the two ends of the line.', str(v), f'M1 2 ways for the ends; M1 × {n - 2}!; A1 {v}')
    k = r.randint(3, 5)
    digs = sorted(r.sample(range(1, 10), r.randint(k + 1, 7)))
    ev = [d for d in digs if d % 2 == 0]
    if not ev:
        return None
    v = len(ev) * math.factorial(len(digs) - 1) // math.factorial(len(digs) - k)
    return Q(f'Find how many {k}-digit even numbers can be formed from the digits ' + ', '.join(map(str, digs)) + ' if no digit may be repeated.', str(v),
             f'M1 {len(ev)} choices for the last digit; M1 × {len(digs) - 1}P{k - 1}; A1 {v}')


def c141_c4(r, D):
    w = r.choice(DISTINCT)
    n = len(w)
    vs = [c for c in w if c in VOW]
    cs = [c for c in w if c not in VOW]
    if len(vs) < 2 or len(cs) < 2:
        return None
    a = r.choice(cs)
    vt = math.factorial(len(cs) + 1) * math.factorial(len(vs))
    intro = f'Consider the arrangements of the {n} letters of the word {w}.'
    parts = [
        P('Find the total number of arrangements.', str(math.factorial(n)), f'B1 {n}! = {math.factorial(n)}'),
        P(f'Find the number of arrangements that begin with {a}.', str(math.factorial(n - 1)), f'M1 fix {a}; A1 {n - 1}! = {math.factorial(n - 1)}'),
        P('Find the number of arrangements in which the vowels are all together.', str(vt), f'M1 vowel block; M1 {len(cs) + 1}! × {len(vs)}!; A1 {vt}'),
        P('Find the number of arrangements in which the vowels are not all together.', str(math.factorial(n) - vt), f'M1 total − together; A1 {math.factorial(n) - vt}'),
        P(f'Find the number of arrangements of 3 letters chosen from the letters of {w}.', str(n * (n - 1) * (n - 2)), f'M1 {n}P3; A1 {n * (n - 1) * (n - 2)}'),
    ]
    return cmp_(r, intro, parts)


c141.add('C4', (2, 3, 4, 5))(c141_c4)


c142 = T('Arrangements with repeated items and with restrictions', 'repeated items', 'restrictions', 'arrangements of letters')
c142.fixed('C1', (1, 2), [
    ('The number of arrangements of the letters of AAB is', '3', '3!/2! = 3.', ['6', '2', '1']),
    ('The number of arrangements of n objects of which p are identical is', 'n!/p!', 'Divide by p! for the identical objects.', ['n!', 'n!/(n − p)!', 'p!']),
    ('In how many ways can 3 identical red and 2 identical blue flags be arranged in a line?', '10', '5!/(3!2!) = 10.', ['120', '12', '60']),
    ('The number of arrangements of the letters of the word EGG is', '3', '3!/2! = 3.', ['6', '2', '9']),
])
c142.fixed('C2', (2, 3), [
    ('Explain why the number of arrangements of the letters of BOOK is 4!/2!.', 'The two Os are identical, so swapping them gives the same arrangement; each distinct arrangement is counted 2! times in 4!.', 'B1 identical Os; B1 each arrangement counted 2! times [2]'),
    ('Explain the method of finding the number of arrangements in which two particular letters are not next to each other.', 'Find the total number of arrangements and subtract the number in which the two letters are together (treated as a single unit).', 'B1 total minus together; B1 treat pair as one unit [2]'),
])


@c142.add('C1', (1, 2, 3))
def c142_c1(r, D):
    w = r.choice(REPEAT)
    if len(w) > 9 and D < 3:
        return None
    n = len(w)
    v = word_count(w)
    d = lcounts(w)
    return MC(r, f'Find the number of different arrangements of the letters of the word {w}.', f'{v:,}' if v >= 10000 else str(v),
              [f'{math.factorial(n):,}' if math.factorial(n) >= 10000 else str(math.factorial(n)), *(f'{x:,}' if x >= 10000 else str(x) for x in [v * 2, v // 2 if v % 2 == 0 else v * 3, math.factorial(n - 1) // max(1, max(math.factorial(c) for c in d.values()))])],
              f'{n}! divided by the factorials of the repeated letters ({rep_desc(w)}) = {v}.')


@c142.add('C2', (2, 3, 4), 'explain')
def c142_err(r, D):
    w = r.choice(REPEAT)
    n = len(w)
    v = word_count(w)
    nm = person(r)
    return Q(f'{nm} says that the letters of the word {w} can be arranged in {n}! = {math.factorial(n):,} different ways. Explain why this is wrong and find the correct number.',
             f'Some letters are repeated ({rep_desc(w)}); swapping identical letters gives the same arrangement, so divide: {v:,}.',
             f'B1 identifies repeated letters; B1 {v:,}')


@c142.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c142_calc(r, D):
    w = r.choice(REPEAT)
    n = len(w)
    d = lcounts(w)
    if D <= 2:
        v = word_count(w)
        return Q(f'Find the number of different arrangements of the letters of the word {w}.', f'{v:,}', f'M1 {n}! in numerator; M1 divides by factorials for {rep_desc(w)}; A1 {v:,}')
    if D == 3:
        a = w[0]
        b = r.choice(list(w))
        v = ends_with(w, a, b)
        return Q(f'Find the number of arrangements of the letters of the word {w} which begin with {a} and end with {b}.', f'{v:,}',
                 f'M1 removes {a} and {b}; M1 arranges remaining {n - 2} letters allowing for repeats; A1 {v:,}')
    if D == 4:
        v = vowels_together(w)
        if v is None:
            return None
        return Q(f'Find the number of arrangements of the letters of the word {w} in which all the vowels are together.', f'{v:,}',
                 f'M1 vowels as one unit; M1 arrangements of units allowing for repeats; M1 × arrangements of vowels within the unit; A1 {v:,}')
    L = r.choice([k for k, c in d.items() if c >= 2])
    v = letter_apart(w, L)
    return Q(f'Find the number of arrangements of the letters of the word {w} in which no two {L}s are next to each other.', f'{v:,}',
             f'M1 arranges the other {n - d[L]} letters; M1 chooses {d[L]} of the {n - d[L] + 1} gaps; A1 {v:,}')


@c142.add('C3', (2, 3, 4, 5), 'numerical')
def c142_obj(r, D):
    a, b, c = r.randint(2, 5), r.randint(2, 4), r.randint(1, 3)
    obj = r.choice([('red', 'blue', 'green', 'beads'), ('silver', 'gold', 'bronze', 'coins'), ('white', 'black', 'grey', 'tiles')])
    tot = ms_perm([a, b, c])
    kind = r.choice(['all', 'ends', 'together'])
    third = f'{c} identical {obj[2]}' if c > 1 else f'1 {obj[2]}'
    if kind == 'all':
        return Q(f'{a} identical {obj[0]}, {b} identical {obj[1]} and {third} {obj[3] if c > 1 else obj[3][:-1]} are arranged in a line. Find the number of different arrangements.', f'{tot:,}',
                 f'M1 {a + b + c}!/({a}! {b}! {c}!); A1 {tot:,}')
    if kind == 'ends':
        v = ms_perm([a - 2, b, c])
        return Q(f'{a} identical {obj[0]}, {b} identical {obj[1]} and {third} {obj[3] if c > 1 else obj[3][:-1]} are arranged in a line. Find the number of arrangements with a {obj[0]} {obj[3][:-1]} at each end.', f'{v:,}',
                 f'M1 places {obj[0]} at both ends; M1 {a + b + c - 2}!/({a - 2}! {b}! {c}!); A1 {v:,}')
    v = ms_perm([a, 1, c])
    return Q(f'{a} identical {obj[0]}, {b} identical {obj[1]} and {third} {obj[3] if c > 1 else obj[3][:-1]} are arranged in a line. Find the number of arrangements in which all the {obj[1]} {obj[3]} are together.', f'{v:,}',
             f'M1 treats the {b} {obj[1]} as one unit; M1 {a + c + 1}!/({a}! {c}!); A1 {v:,}')


def c142_c4(r, D):
    w = r.choice(REPEAT)
    n = len(w)
    d = lcounts(w)
    tot = word_count(w)
    vt = vowels_together(w)
    L = r.choice([k for k, c in d.items() if c >= 2])
    ap = letter_apart(w, L)
    intro = f'Consider the arrangements of the {n} letters of the word {w}.'
    parts = [
        P('Find the number of different arrangements.', f'{tot:,}', f'M1 divides by factorials of repeats; A1 {tot:,}'),
        P(f'Find the number of arrangements in which no two {L}s are next to each other.', f'{ap:,}', f'M1 arranges other letters; M1 gaps for the {L}s; A1 {ap:,}'),
        P(f'Find the number of arrangements in which the {d[L]} {L}s are all together.', f'{ms_perm([v for k, v in d.items() if k != L] + [1]):,}', f'M1 treats the {L}s as one unit; A1 {ms_perm([v for k, v in d.items() if k != L] + [1]):,}'),
    ]
    if vt:
        parts.append(P('Find the number of arrangements in which all the vowels are together.', f'{vt:,}', f'M1 vowel unit; M1 internal arrangements; A1 {vt:,}'))
    return cmp_(r, intro, parts)


c142.add('C4', (2, 3, 4, 5))(c142_c4)


c143 = T('Combinations nCr and selections with restrictions', 'combinations', 'nCr', 'selections')
c143.fixed('C1', (1, 2), [
    ('The number of ways of choosing 3 people from 7 is', '35', '⁷C₃ = 35.', ['210', '21', '343']),
    ('ⁿCᵣ is equal to', 'ⁿCₙ₋ᵣ', 'Choosing r to include is the same as choosing n − r to leave out.', ['ⁿPᵣ', 'ⁿCᵣ₊₁', 'r!']),
    ('The difference between a permutation and a combination is that', 'order matters in a permutation but not in a combination', 'Combinations are selections; permutations are arrangements.', ['a combination uses factorials', 'a permutation allows repetition', 'they are the same']),
    ('The value of ⁸C₀ is', '1', 'There is one way to choose nothing.', ['0', '8', '40320']),
])
c143.fixed('C2', (2, 3), [
    ('Explain why ⁿCᵣ = ⁿPᵣ/r!.', 'Each selection of r objects can be arranged in r! orders, so the number of ordered arrangements is r! times the number of selections.', 'B1 each selection gives r! arrangements; B1 divide nPr by r! [2]'),
    ('Explain why "at least one" problems are often answered by subtracting from the total.', 'The complement, "none", is a single case that is easy to count, whereas "at least one" includes many cases.', 'B1 complement is none; B1 fewer cases [2]'),
])


@c143.add('C1', (1, 2, 3))
def c143_c1(r, D):
    n = r.randint(6, 15)
    k = r.randint(2, 5)
    v = comb(n, k)
    what = r.choice([f'a team of {k} from {n} players', f'{k} books from a shelf of {n} different books', f'{k} questions to answer from {n}', f'a committee of {k} from {n} people'])
    return MC(r, f'In how many ways can {what} be chosen?', f'{v:,}', [f'{x:,}' for x in [math.factorial(n) // math.factorial(n - k), comb(n, k - 1), n * k, comb(n - 1, k)]], f'{n}C{k} = {v}.')


@c143.add('C2', (2, 3, 4), 'explain')
def c143_err(r, D):
    m, w = r.randint(4, 9), r.randint(4, 9)
    k = r.randint(3, 5)
    nm = person(r)
    tot = comb(m + w, k)
    none = comb(m, k)
    wrong = w * comb(m + w - 1, k - 1)
    return Q(f'A committee of {k} is chosen from {m} men and {w} women. {nm} says the number of committees with at least one woman is {w} × {m + w - 1}C{k - 1} = {wrong:,}, by choosing one woman and then anyone else. Explain the error and find the correct number.',
             f'Committees with more than one woman are counted more than once; the correct number is {m + w}C{k} − {m}C{k} = {tot - none:,}.',
             f'B1 multiple counting of committees with 2 or more women; M1 total − no women; A1 {tot - none:,}')


@c143.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c143_calc(r, D):
    m, w = r.randint(4, 10), r.randint(4, 10)
    k = r.randint(3, 6)
    g = r.choice([('men', 'women'), ('boys', 'girls'), ('teachers', 'students'), ('juniors', 'seniors')])
    stem = f'A group of {k} is to be chosen from {m} {g[0]} and {w} {g[1]}.'
    if D <= 2:
        j = r.randint(1, k - 1)
        if j > w or k - j > m:
            return None
        v = comb(w, j) * comb(m, k - j)
        return Q(stem + f' Find the number of groups that contain exactly {j} of the {g[1]}.', f'{v:,}', f'M1 {w}C{j} × {m}C{k - j}; A1 {v:,}')
    if D == 3:
        v = comb(m + w, k) - comb(m, k)
        return Q(stem + f' Find the number of groups that contain at least one of the {g[1]}.', f'{v:,}', f'M1 {m + w}C{k}; M1 − {m}C{k}; A1 {v:,}')
    if D == 4:
        j = r.randint(2, min(k - 1, w))
        v = sum(comb(w, i) * comb(m, k - i) for i in range(j, k + 1))
        return Q(stem + f' Find the number of groups that contain at least {j} {g[1]}.', f'{v:,}', f'M1 lists cases {j} to {k}; M1 sums products of combinations; A1 {v:,}')
    nm1, nm2 = two_people(r)
    v = comb(m + w, k) - comb(m + w - 2, k - 2)
    return Q(stem + f' {nm1} and {nm2} are two of the {g[1]} and refuse to be in the group together. Find the number of possible groups.', f'{v:,}',
             f'M1 total {m + w}C{k}; M1 subtract groups with both: {m + w - 2}C{k - 2}; A1 {v:,}')


@c143.add('C3', (2, 3, 4), 'numerical')
def c143_spec(r, D):
    n = r.randint(8, 14)
    k = r.randint(3, 6)
    nm = person(r)
    kind = r.choice(['must', 'not'])
    if kind == 'must':
        v = comb(n - 1, k - 1)
        return Q(f'A team of {k} is chosen from {n} players, one of whom is {nm}. Find the number of teams that include {nm}.', f'{v:,}', f'M1 {nm} chosen, then {k - 1} from {n - 1}; A1 {n - 1}C{k - 1} = {v:,}')
    v = comb(n - 1, k)
    return Q(f'A team of {k} is chosen from {n} players, one of whom is {nm}. Find the number of teams that do not include {nm}.', f'{v:,}', f'M1 {k} from the other {n - 1}; A1 {n - 1}C{k} = {v:,}')


def c143_c4(r, D):
    m, w = r.randint(5, 10), r.randint(5, 10)
    k = r.randint(4, 6)
    nm1, nm2 = two_people(r)
    tot = comb(m + w, k)
    j = r.randint(1, k - 1)
    ex = comb(w, j) * comb(m, k - j)
    al = tot - comb(m, k)
    mf = sum(comb(w, i) * comb(m, k - i) for i in range(0, k + 1) if i > k - i)
    intro = f'A committee of {k} people is to be chosen from {m} men and {w} women.'
    parts = [
        P('Find the total number of possible committees.', f'{tot:,}', f'B1 {m + w}C{k} = {tot:,}'),
        P(f'Find the number of committees with exactly {j} wom{"a" if j == 1 else "e"}n.', f'{ex:,}', f'M1 {w}C{j} × {m}C{k - j}; A1 {ex:,}'),
        P('Find the number of committees with at least one woman.', f'{al:,}', f'M1 total − all men; A1 {al:,}'),
        P('Find the number of committees with more women than men.', f'{mf:,}', f'M1 identifies cases; M1 sums; A1 {mf:,}'),
        P(f'{nm1} and {nm2} are a married couple among the {m + w} people, and must either both be on the committee or both be off it. Find the number of possible committees.', f'{comb(m + w - 2, k - 2) + comb(m + w - 2, k):,}',
          f'M1 both on: {m + w - 2}C{k - 2}; M1 both off: {m + w - 2}C{k}; A1 {comb(m + w - 2, k - 2) + comb(m + w - 2, k):,}'),
    ]
    return cmp_(r, intro, parts)


c143.add('C4', (2, 3, 4, 5))(c143_c4)


c144 = T('Using permutations and combinations to find probabilities', 'probability using combinations', 'permutations', 'combinations')
c144.fixed('C1', (1, 2), [
    ('If 3 people are chosen at random from 10, the probability that a particular person is chosen is', '3/10', '⁹C₂/¹⁰C₃ = 36/120.', ['1/10', '1/3', '1/120']),
    ('5 people stand in a random order in a line. The probability that a particular person is at the front is', '1/5', 'Each of the 5 is equally likely to be first.', ['1/120', '1/24', '4/5']),
    ('The letters of ABC are arranged at random. The probability that they spell ABC is', '1/6', 'One of 3! = 6 equally likely arrangements.', ['1/3', '1/27', '1/9']),
    ('Two people are chosen at random from 6. The probability that two particular people are both chosen is', '1/15', '1/⁶C₂.', ['1/36', '1/30', '2/15']),
])
c144.fixed('C2', (2, 3), [
    ('Explain why P(event) = (number of favourable selections)/(total number of selections) can be used when choosing a committee at random.', 'Choosing at random means every selection is equally likely, so the probability is the proportion of selections that are favourable.', 'B1 equally likely outcomes; B1 ratio of counts [2]'),
    ('Explain why the probability that two particular people are next to each other in a random line of n people is 2/n.', 'There are 2(n − 1)! arrangements with them together out of n! in total, and 2(n − 1)!/n! = 2/n.', 'M1 2(n − 1)! favourable; A1 divides by n! [2]'),
])


@c144.add('C1', (2, 3))
def c144_c1(r, D):
    n = r.randint(6, 12)
    k = r.randint(2, 5)
    return MC(r, f'{k} people are chosen at random from {n}, one of whom is {person(r)}. Find the probability that this person is chosen.', num(Fr(k, n)),
              [num(Fr(1, n)), num(Fr(1, comb(n, k))), num(Fr(k, n + 1)), num(Fr(1, k)) if Fr(1, k) != Fr(k, n) else num(Fr(k - 1, n))], f'{n - 1}C{k - 1}/{n}C{k} = {num(Fr(k, n))}.')


@c144.add('C1', (1, 2, 3))
def c144_c1b(r, D):
    n = r.randint(4, 9)
    return MC(r, f'{n} people, including two friends, stand in a line in a random order. Find the probability that the two friends stand next to each other.', num(Fr(2, n)),
              [num(Fr(1, n)), num(Fr(1, n - 1)), num(Fr(2, n - 1)), num(Fr(2, math.factorial(n)))], f'2 × {n - 1}!/{n}! = {num(Fr(2, n))}.')


@c144.add('C2', (2, 3, 4), 'explain')
def c144_err(r, D):
    m, w = r.randint(4, 9), r.randint(4, 9)
    k = r.randint(3, 5)
    j = r.randint(1, k - 1)
    if j > w or k - j > m:
        return None
    nm = person(r)
    p = Fr(comb(w, j) * comb(m, k - j), comb(m + w, k))
    wrong = Fr(w, m + w) ** j * Fr(m, m + w) ** (k - j)
    return Q(f'{k} people are chosen at random from {m} men and {w} women. {nm} calculates the probability of exactly {j} wom{"a" if j == 1 else "e"}n as ({w}/{m + w}){sup(j)} × ({m}/{m + w}){sup(k - j)}. Give two reasons why this is wrong, and find the correct probability.'.replace('¹ ', ' ').replace('¹.', '.'),
             f'The people are chosen without replacement, so the probabilities change; also the different orders of choosing are not counted. Correct: {w}C{j} × {m}C{k - j}/{m + w}C{k} = {prs(p)}.',
             f'B1 without replacement / not independent; B1 orders not counted; B1 {prs(p)}')


@c144.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c144_calc(r, D):
    m, w = r.randint(4, 9), r.randint(4, 9)
    k = r.randint(3, 5)
    g = r.choice([('men', 'women'), ('boys', 'girls'), ('red', 'blue', 'counters'), ('juniors', 'seniors')])
    stem = f'{k} people are chosen at random from {m} {g[0]} and {w} {g[1]}.' if len(g) == 2 else f'{k} counters are taken at random from a bag of {m} red and {w} blue counters.'
    g1 = g[1] if len(g) == 2 else 'blue counters'
    g0 = g[0] if len(g) == 2 else 'red counters'
    tot = comb(m + w, k)
    if D <= 2:
        j = r.randint(1, k - 1)
        if j > w or k - j > m:
            return None
        p = Fr(comb(w, j) * comb(m, k - j), tot)
        return Q(stem + f' Find the probability that exactly {j} {"is" if j == 1 else "are"} {g1}.' if len(g) == 3 else stem + f' Find the probability that exactly {j} of those chosen {"is one of the" if j == 1 else "are"} {g1}.', prs(p),
                 f'M1 {w}C{j} × {m}C{k - j}; M1 ÷ {m + w}C{k} = {tot}; A1 {prs(p)}')
    if D == 3:
        p = 1 - Fr(comb(m, k), tot)
        return Q(stem + f' Find the probability that at least one of those chosen is from the {g1}.', prs(p), f'M1 1 − P(no {g1}); M1 {m}C{k}/{m + w}C{k}; A1 {prs(p)}')
    if D == 4:
        p = Fr(comb(m, k) + comb(w, k), tot)
        return Q(stem + f' Find the probability that all those chosen are {g0} or all are {g1}.', prs(p), f'M1 {m}C{k} + {w}C{k}; M1 ÷ {tot}; A1 {prs(p)}')
    w_ = r.choice(REPEAT)
    vt = vowels_together(w_)
    if not vt:
        return None
    p = Fr(vt, word_count(w_))
    return Q(f'The letters of the word {w_} are arranged in a random order. Find the probability that all the vowels are together.', prs(p),
             f'M1 vowels-together count {vt:,}; M1 ÷ total {word_count(w_):,}; A1 {prs(p)}')


@c144.add('C3', (2, 3, 4, 5), 'numerical')
def c144_line(r, D):
    b, g = r.randint(2, 5), r.randint(2, 5)
    n = b + g
    kind = r.choice(['ends', 'alt', 'together'])
    if kind == 'ends':
        p = Fr(b * (b - 1), n * (n - 1))
        return Q(f'{b} boys and {g} girls stand in a line in a random order. Find the probability that there is a boy at each end of the line.', pr(p),
                 f'M1 {b} × {b - 1} × {n - 2}!; M1 ÷ {n}!; A1 {pr(p)}')
    if kind == 'alt':
        if abs(b - g) > 1:
            return None
        ways = math.factorial(b) * math.factorial(g) * (2 if b == g else 1)
        p = Fr(ways, math.factorial(n))
        return Q(f'{b} boys and {g} girls stand in a line in a random order. Find the probability that boys and girls alternate.', pr(p),
                 f'M1 {b}! × {g}!' + (' × 2' if b == g else '') + f' = {ways}; M1 ÷ {n}!; A1 {pr(p)}')
    p = Fr(math.factorial(g + 1) * math.factorial(b), math.factorial(n))
    return Q(f'{b} boys and {g} girls stand in a line in a random order. Find the probability that all the boys stand together.', pr(p),
             f'M1 boys as one unit: {g + 1}! × {b}!; M1 ÷ {n}!; A1 {pr(p)}')


def c144_c4(r, D):
    m, w = r.randint(5, 9), r.randint(5, 9)
    k = r.randint(3, 5)
    nm1, nm2 = two_people(r)
    tot = comb(m + w, k)
    j = r.randint(1, k - 1)
    pe = Fr(comb(w, j) * comb(m, k - j), tot)
    pal = 1 - Fr(comb(m, k), tot)
    pboth = Fr(comb(m + w - 2, k - 2), tot)
    intro = f'A team of {k} is chosen at random from {m} boys and {w} girls, including the friends {nm1} and {nm2}.'
    parts = [
        P(f'Find the probability that the team contains exactly {j} girl{"s" if j > 1 else ""}.', prs(pe), f'M1 {w}C{j} × {m}C{k - j}; M1 ÷ {tot}; A1 {prs(pe)}'),
        P('Find the probability that the team contains at least one girl.', prs(pal), f'M1 1 − {m}C{k}/{tot}; A1 {prs(pal)}'),
        P(f'Find the probability that both {nm1} and {nm2} are in the team.', prs(pboth), f'M1 {m + w - 2}C{k - 2}; A1 {prs(pboth)}'),
        P(f'The {k} members of the team then stand in a line in a random order. Find the probability that the team captain is at one end of the line.', pr(Fr(2, k)), f'M1 2 × {k - 1}!/{k}!; A1 {pr(Fr(2, k))}'),
    ]
    return cmp_(r, intro, parts)


c144.add('C4', (2, 3, 4, 5))(c144_c4)

CHAPTERS[14] = [c141, c142, c143, c144]


# ================================================================ Chapter 15 Discrete random variables

def ptab(xs, ps, var='x'):
    return f'{var}: ' + ', '.join(map(str, xs)) + f'; P(X = {var}): ' + ', '.join(ps)


def rdist(r, k=None):
    """Random distribution with probabilities in tenths or twentieths."""
    k = k or r.choice([3, 4, 5])
    den = r.choice([10, 20])
    while True:
        cuts = sorted(r.sample(range(1, den), k - 1))
        parts = [b - a for a, b in zip([0] + cuts, cuts + [den])]
        if min(parts) > 0:
            return [Fr(p, den) for p in parts]


def rxs(r, k):
    x0 = r.choice([0, 1, 2, -1, -2])
    step = r.choice([1, 1, 1, 2])
    return [x0 + step * i for i in range(k)]


def EX(xs, ps):
    return sum(x * p for x, p in zip(xs, ps))


def VX(xs, ps):
    return sum(x * x * p for x, p in zip(xs, ps)) - EX(xs, ps) ** 2


d151 = T('Probability distributions of discrete random variables', 'discrete random variables', 'probability distributions')
d151.fixed('C1', (1, 2), [
    ('For any probability distribution, the probabilities must', 'be between 0 and 1 and sum to 1', 'ΣP(X = x) = 1 with each 0 ≤ p ≤ 1.', ['sum to 0', 'all be equal', 'increase with x']),
    ('A discrete random variable', 'takes only certain separate values', 'For example 0, 1, 2, …', ['can take any value in an interval', 'must be positive', 'has a mean of 0']),
    ('If P(X = 0) = 0.2, P(X = 1) = 0.5 and X takes only the values 0, 1 and 2, then P(X = 2) =', '0.3', '1 − 0.2 − 0.5.', ['0.7', '0.5', '0.2']),
    ('For a discrete random variable, P(X ≤ 2) + P(X > 2) =', '1', 'The two events are complementary.', ['0', 'P(X = 2)', '2']),
])
d151.fixed('C2', (2, 3), [
    ('Explain why P(X = x) = x/10 for x = 1, 2, 3 does not define a probability distribution.', 'The probabilities 0.1, 0.2 and 0.3 sum to 0.6, not 1.', 'M1 sums the probabilities; A1 total ≠ 1 [2]'),
    ('Explain the difference between P(X < 3) and P(X ≤ 3) for a discrete random variable.', 'P(X ≤ 3) includes P(X = 3) but P(X < 3) does not; for a discrete variable P(X = 3) may be non-zero.', 'B1 inclusion of X = 3; B1 discrete so P(X = 3) can be non-zero [2]'),
])


@d151.add('C1', (1, 2, 3))
def d151_c1(r, D):
    ps = rdist(r)
    xs = rxs(r, len(ps))
    i = r.randrange(len(ps))
    shown = [dn(p) if j != i else 'k' for j, p in enumerate(ps)]
    if D <= 2:
        return MC(r, f'The random variable X has probability distribution {ptab(xs, shown)}. Find k.', dn(ps[i]),
                  [dn(1 - ps[i]), dn(Fr(1, len(ps))), dn(sum(ps) - ps[i]), dn(ps[i] + Fr(1, 10)) if ps[i] + Fr(1, 10) < 1 else dn(ps[i] / 2)], f'Probabilities sum to 1: k = {dn(ps[i])}.')
    a = r.choice(xs[1:-1]) if len(xs) > 2 else xs[0]
    pge = sum(p for x, p in zip(xs, ps) if x >= a)
    return MC(r, f'The random variable X has probability distribution {ptab(xs, [dn(p) for p in ps])}. Find P(X ≥ {num(a)}).', dn(pge),
              [dn(pge - ps[xs.index(a)]) if pge - ps[xs.index(a)] > 0 else dn(pge + Fr(1, 20)), dn(1 - pge) if 1 - pge != pge else dn(pge / 2), dn(ps[xs.index(a)]), dn(1 - pge + ps[xs.index(a)])], f'Sum of P(X = x) for x ≥ {num(a)}: {dn(pge)}.')


@d151.add('C2', (2, 3, 4), 'explain')
def d151_valid(r, D):
    ps = rdist(r)
    xs = rxs(r, len(ps))
    kind = r.choice(['sum', 'neg', 'ok'])
    if kind == 'sum':
        j = r.randrange(len(ps))
        ps = list(ps)
        ps[j] += r.choice([Fr(1, 10), Fr(-1, 20)]) if ps[j] > Fr(1, 10) else Fr(1, 10)
        tot = sum(ps)
        return Q(f'Determine, with a reason, whether {ptab(xs, [dn(p) for p in ps])} is a valid probability distribution.', f'not valid: the probabilities sum to {dn(tot)}, not 1',
                 f'M1 sums probabilities to {dn(tot)}; A1 not valid, sum ≠ 1')
    if kind == 'neg':
        ps = list(ps)
        j = r.randrange(len(ps))
        k = (j + 1) % len(ps)
        ps[j] += ps[k] + Fr(1, 10)
        ps[k] = Fr(-1, 10)
        return Q(f'A student claims that {ptab(xs, [dn(p) for p in ps])} is a probability distribution because the probabilities add up to 1. Explain why the student is wrong.', 'One probability is negative (−0.1); every probability must satisfy 0 ≤ p ≤ 1.',
                 'B1 identifies negative probability; B1 states 0 ≤ p ≤ 1 required')
    return Q(f'Determine, with a reason, whether {ptab(xs, [dn(p) for p in ps])} is a valid probability distribution.', 'valid: every probability is between 0 and 1 and they sum to 1',
             'M1 checks sum = 1; A1 valid with both conditions')


@d151.add('C3', (1, 2, 3, 4, 5), 'numerical')
def d151_calc(r, D):
    n = r.choice([3, 4, 5, 6])
    xs = list(range(1, n + 1))
    if D <= 2:
        kind = r.choice(['kx', 'kx1', 'k(n+1-x)'])
        f = {'kx': lambda x: x, 'kx1': lambda x: x + 1, 'k(n+1-x)': lambda x: n + 1 - x}[kind]
        lab = {'kx': 'kx', 'kx1': 'k(x + 1)', 'k(n+1-x)': f'k({n + 1} − x)'}[kind]
        tot = sum(f(x) for x in xs)
        k = Fr(1, tot)
        a = r.randint(2, n)
        pa = sum(k * f(x) for x in xs if x >= a)
        return Q(f'The random variable X takes the values {", ".join(map(str, xs))}, with P(X = x) = {lab}. Find the value of k and P(X ≥ {a}).', f'k = {num(k)}; P(X ≥ {a}) = {num(pa)}',
                 f'M1 sum of {lab} = {tot}k = 1; A1 k = {num(k)}; B1 P(X ≥ {a}) = {num(pa)}')
    if D == 3:
        tot = sum(x * x for x in xs)
        k = Fr(1, tot)
        a, b = sorted(r.sample(xs, 2))
        p = sum(k * x * x for x in xs if a < x <= b)
        return Q(f'The random variable X takes the values {", ".join(map(str, xs))}, with P(X = x) = kx². Find k and P({a} < X ≤ {b}).', f'k = {num(k)}; P = {num(p)}',
                 f'M1 k(1 + 4 + … ) = {tot}k = 1; A1 k = {num(k)}; M1 adds P(X = x) for {a} < x ≤ {b}; A1 {num(p)}')
    ps = rdist(r, 4)
    xs = rxs(r, 4)
    i, j = r.sample(range(4), 2)
    e = EX(xs, ps)
    shown = [('p' if t == i else 'q' if t == j else dn(pp)) for t, pp in enumerate(ps)]
    return Q(f'The random variable X has probability distribution {ptab(xs, shown)}. Given that E(X) = {dn(e)}, find p and q.', f'p = {dn(ps[i])}, q = {dn(ps[j])}',
             f'M1 p + q = {dn(ps[i] + ps[j])}; M1 Σx P(X = x) = {dn(e)}; M1 solves simultaneously; A1 p = {dn(ps[i])}, q = {dn(ps[j])}')


def d151_c4(r, D):
    ps = rdist(r, r.choice([4, 5]))
    xs = rxs(r, len(ps))
    i = r.randrange(len(ps))
    shown = [dn(p) if j != i else 'k' for j, p in enumerate(ps)]
    a = xs[1]
    b = xs[-2]
    intro = f'The random variable X has probability distribution {ptab(xs, shown)}.'
    parts = [
        P('Find k.', dn(ps[i]), f'M1 sum = 1; A1 k = {dn(ps[i])}'),
        P(f'Find P(X ≤ {num(a)}).', dn(sum(p for x, p in zip(xs, ps) if x <= a)), f'B1 {dn(sum(p for x, p in zip(xs, ps) if x <= a))}'),
        P(f'Find P({num(a)} ≤ X < {num(b)}).', dn(sum(p for x, p in zip(xs, ps) if a <= x < b)), f'B1 {dn(sum(p for x, p in zip(xs, ps) if a <= x < b))}'),
        P('Find E(X).', dn(EX(xs, ps)), f'M1 Σx P(X = x); A1 {dn(EX(xs, ps))}'),
        P('Find the most likely value of X.', num(xs[ps.index(max(ps))]) if ps.count(max(ps)) == 1 else ' and '.join(num(x) for x, p in zip(xs, ps) if p == max(ps)), 'B1 value(s) with the largest probability'),
    ]
    return cmp_(r, intro, parts)


d151.add('C4', (2, 3, 4, 5))(d151_c4)


d152 = T('Expectation E(X) and variance Var(X)', 'expectation', 'variance', 'E(X)', 'Var(X)')
d152.fixed('C1', (1, 2), [
    ('E(X) for a discrete random variable is', 'Σx P(X = x)', 'Weight each value by its probability.', ['Σx/n', 'ΣP(X = x)', 'Σx² P(X = x)']),
    ('Var(X) is given by', 'E(X²) − [E(X)]²', 'Σx²p − (Σxp)².', ['E(X²) − E(X)', '[E(X)]² − E(X²)', 'E(X²)']),
    ('If E(X) = 3 and E(X²) = 13, then Var(X) =', '4', '13 − 3² = 4.', ['10', '16', '2']),
    ('If Var(X) = 9, the standard deviation of X is', '3', '√9 = 3.', ['81', '9', '4.5']),
])
d152.fixed('C2', (2, 3), [
    ('Explain what E(X) represents for a random variable X.', 'It is the long-run mean value of X over many repetitions of the experiment.', 'B1 mean / average value; B1 in the long run [2]'),
    ('Explain why E(X) need not be a value that X can take.', 'E(X) is a weighted average of the possible values, so it can lie between them, e.g. 3.5 for a fair die.', 'B1 weighted average; B1 example or explanation [2]'),
])


@d152.add('C1', (1, 2, 3))
def d152_c1(r, D):
    ps = rdist(r)
    xs = rxs(r, len(ps))
    e = EX(xs, ps)
    if D < 3:
        return MC(r, f'The random variable X has probability distribution {ptab(xs, [dn(p) for p in ps])}. Find E(X).', dn(e),
                  [dn(Fr(sum(xs), len(xs))) if Fr(sum(xs), len(xs)) != e else dn(e + 1), dn(sum(x * x * p for x, p in zip(xs, ps))), dn(e + Fr(1, 2)), dn(e - Fr(1, 5))], f'Σx P(X = x) = {dn(e)}.')
    v = VX(xs, ps)
    e2 = sum(x * x * p for x, p in zip(xs, ps))
    return MC(r, f'The random variable X has probability distribution {ptab(xs, [dn(p) for p in ps])}. Find Var(X).', dn(v),
              [dn(e2), dn(e2 - e) if e2 - e != v else dn(v + 1), dn(e * e) if e * e != v else dn(v + 2), dn(abs(e2 - 2 * e)) if abs(e2 - 2 * e) != v else dn(v / 2)], f'E(X) = {dn(e)}, E(X²) = {dn(e2)}, Var = {dn(e2)} − {pn(dn(e))}² = {dn(v)}.')


@d152.add('C2', (2, 3, 4), 'explain')
def d152_err(r, D):
    ps = rdist(r)
    xs = rxs(r, len(ps))
    e = EX(xs, ps)
    e2 = sum(x * x * p for x, p in zip(xs, ps))
    v = e2 - e * e
    nm = person(r)
    if e == 0:
        return None
    kind = r.choice(['nosq', 'mean'])
    if kind == 'nosq':
        return Q(f'For the distribution {ptab(xs, [dn(p) for p in ps])}, {nm} gives Var(X) = Σx²P(X = x) = {dn(e2)}. Explain the error and find Var(X).',
                 f'{nm} has found E(X²) and not subtracted [E(X)]² = {dn(e * e)}; Var(X) = {dn(e2)} − {dn(e * e)} = {dn(v)}.', f'B1 must subtract [E(X)]²; M1 E(X) = {dn(e)}; A1 {dn(v)}')
    wrong = Fr(sum(xs), len(xs))
    if wrong == e:
        return None
    return Q(f'For the distribution {ptab(xs, [dn(p) for p in ps])}, {nm} says E(X) is the mean of the values of x, {dn(wrong)}. Explain the error and find E(X).',
             f'The values are not equally likely, so each must be weighted by its probability: E(X) = Σx P(X = x) = {dn(e)}.', f'B1 values must be weighted by probabilities; B1 {dn(e)}')


@d152.add('C3', (1, 2, 3, 4, 5), 'numerical')
def d152_calc(r, D):
    if D <= 3:
        ps = rdist(r, r.choice([3, 4, 5]))
        xs = rxs(r, len(ps))
        e = EX(xs, ps)
        v = VX(xs, ps)
        return Q(f'The random variable X has probability distribution {ptab(xs, [dn(p) for p in ps])}. Find E(X) and Var(X).', f'E(X) = {dn(e)}; Var(X) = {dn(v)}',
                 f'M1 Σx P(X = x); A1 E(X) = {dn(e)}; M1 Σx² P(X = x) − [E(X)]²; A1 Var(X) = {dn(v)}')
    if D == 4:
        n = r.choice([3, 4, 5])
        xs = list(range(1, n + 1))
        tot = sum(xs)
        k = Fr(1, tot)
        ps = [k * x for x in xs]
        e = EX(xs, ps)
        v = VX(xs, ps)
        return Q(f'The random variable X takes the values {", ".join(map(str, xs))} with P(X = x) = kx. Find k, E(X) and Var(X).', f'k = {num(k)}; E(X) = {num(e)}; Var(X) = {num(v)}',
                 f'B1 k = {num(k)}; M1 Σx P(X = x); A1 E(X) = {num(e)}; M1 E(X²) − [E(X)]²; A1 {num(v)}')
    ps = rdist(r, 3)
    xs = rxs(r, 3)
    xs = [xs[0], xs[1], None]
    x3 = xs[1] + r.randint(1, 4)
    xs[2] = x3
    e = EX(xs, ps)
    v = VX(xs, ps)
    return Q(f'The random variable X has probability distribution x: {num(xs[0])}, {num(xs[1])}, a; P(X = x): {dn(ps[0])}, {dn(ps[1])}, {dn(ps[2])}. Given that E(X) = {dn(e)}, find a and Var(X).', f'a = {num(x3)}; Var(X) = {dn(v)}',
             f'M1 {pn(xs[0])} × {dn(ps[0])} + {pn(xs[1])} × {dn(ps[1])} + {dn(ps[2])}a = {dn(e)}; A1 a = {num(x3)}; M1 E(X²) − [E(X)]²; A1 {dn(v)}')


@d152.add('C3', (2, 3, 4), 'numerical')
def d152_game(r, D):
    cost = r.choice([1, 2, 5])
    prizes = sorted(r.sample([0, 1, 2, 3, 5, 10, 20], 3))
    ps = sorted(rdist(r, 3), reverse=True)
    xs = [p - cost for p in prizes]
    e = EX(xs, ps)
    nm = person(r)
    return Q(f'{nm} pays ${cost} to play a game. The prize is ${prizes[0]}, ${prizes[1]} or ${prizes[2]} with probabilities {dn(ps[0])}, {dn(ps[1])} and {dn(ps[2])} respectively. Find the expected profit per game, and state whether the game is fair.',
             f'E(profit) = ${dn(e)}' + ('; the game is fair' if e == 0 else '; not fair (E(profit) ≠ 0)'),
             f'M1 profits {", ".join(num(x) for x in xs)}; M1 Σ profit × probability; A1 {dn(e)} and conclusion')


def d152_c4(r, D):
    ps = rdist(r, r.choice([4, 5]))
    xs = rxs(r, len(ps))
    e = EX(xs, ps)
    e2 = sum(x * x * p for x, p in zip(xs, ps))
    v = e2 - e * e
    a, b = r.choice([2, 3, 4]), r.choice([1, 3, 5])
    intro = f'The random variable X has probability distribution {ptab(xs, [dn(p) for p in ps])}.'
    parts = [
        P('Find E(X).', dn(e), f'M1 Σx P(X = x); A1 {dn(e)}'),
        P('Find E(X²).', dn(e2), f'M1 Σx² P(X = x); A1 {dn(e2)}'),
        P('Find Var(X).', dn(v), f'M1 E(X²) − [E(X)]² = {dn(e2)} − {pn(dn(e))}²; A1 {dn(v)}'),
        P('Find the standard deviation of X.', n3(math.sqrt(v)), f'B1 √{dn(v)} = {n3(math.sqrt(v))}'),
        P(f'Find P(X > E(X)).', dn(sum(p for x, p in zip(xs, ps) if x > e)), f'M1 values greater than {dn(e)}; A1 {dn(sum(p for x, p in zip(xs, ps) if x > e))}'),
    ]
    return cmp_(r, intro, parts)


d152.add('C4', (2, 3, 4, 5))(d152_c4)


d153 = T('Constructing probability distributions from contexts', 'constructing probability distributions', 'probability distribution table')
d153.fixed('C1', (1, 2), [
    ('Three fair coins are thrown and X is the number of heads. The possible values of X are', '0, 1, 2, 3', 'Between none and all three heads.', ['1, 2, 3', '0, 1, 2', '0, 3']),
    ('Three fair coins are thrown. P(exactly two heads) =', '3/8', 'HHT, HTH, THH out of 8 outcomes.', ['1/4', '1/2', '2/3']),
    ('Two counters are taken without replacement from a bag of 2 red and 3 blue counters. P(both red) =', '1/10', '2/5 × 1/4.', ['4/25', '1/5', '2/25']),
    ('When constructing a probability distribution, a useful check is that', 'the probabilities sum to 1', 'All possible values must be covered.', ['E(X) = 0', 'the probabilities are equal', 'Var(X) = 1']),
])
d153.fixed('C2', (2, 3), [
    ('Explain why, when two counters are taken from a bag without replacement, the number of red counters taken is not modelled by B(2, p).', 'The two selections are not independent: the probability of red changes after the first counter is removed.', 'B1 not independent; B1 probability changes [2]'),
    ('Explain how a sample space diagram can be used to find the probability distribution of the sum of two dice.', 'List all equally likely outcomes in a grid, record the sum in each cell, and divide the count for each sum by the total number of cells.', 'B1 grid of equally likely outcomes; B1 count ÷ total [2]'),
])

DRV_CTX = ['the larger of the two scores (or the common score if they are equal)', 'the smaller of the two scores (or the common score if they are equal)', 'the sum of the two scores', 'the positive difference between the two scores',
           'the number of sixes obtained', 'the number of even scores obtained']


def dice_dist(s, kind):
    d = {}
    for a in range(1, s + 1):
        for b in range(1, s + 1):
            if kind == 0:
                v = max(a, b)
            elif kind == 1:
                v = min(a, b)
            elif kind == 2:
                v = a + b
            elif kind == 3:
                v = abs(a - b)
            elif kind == 4:
                v = (a == s) + (b == s)
            else:
                v = (a % 2 == 0) + (b % 2 == 0)
            d[v] = d.get(v, 0) + 1
    xs = sorted(d)
    return xs, [Fr(d[x], s * s) for x in xs]


def bag_dist(a, b, k):
    """X = number of the first colour when k are taken without replacement from a + b."""
    tot = comb(a + b, k)
    xs = [x for x in range(0, k + 1) if x <= a and k - x <= b]
    return xs, [Fr(comb(a, x) * comb(b, k - x), tot) for x in xs]


def ctx_dist(r):
    t = r.choice(['dice', 'dice', 'bag', 'coin'])
    if t == 'dice':
        s = r.choice([4, 6]) if r.random() < 0.7 else 5
        kind = r.randrange(6)
        if s != 6 and kind == 4:
            kind = 0
        desc = {4: 'two fair four-sided dice, numbered 1 to 4,', 5: 'two fair five-sided dice, numbered 1 to 5,', 6: 'two fair six-sided dice'}[s]
        what = DRV_CTX[kind]
        xs, ps = dice_dist(s, kind)
        return f'{desc.capitalize()} are thrown. The random variable X is {what}.', xs, ps
    if t == 'bag':
        a, b = r.randint(2, 6), r.randint(2, 6)
        k = r.choice([2, 3])
        c1, c2 = r.choice([('red', 'blue'), ('green', 'white'), ('black', 'yellow')])
        xs, ps = bag_dist(a, b, k)
        return f'A bag contains {a} {c1} and {b} {c2} counters. {k} counters are taken at random without replacement. The random variable X is the number of {c1} counters taken.', xs, ps
    n = r.choice([3, 4])
    pH = r.choice([Fr(1, 2), Fr(1, 3), Fr(2, 5), Fr(3, 5), Fr(1, 4)])
    xs = list(range(n + 1))
    ps = [comb(n, x) * pH ** x * (1 - pH) ** (n - x) for x in xs]
    coin = 'a fair coin' if pH == Fr(1, 2) else f'a biased coin with P(head) = {num(pH)}'
    return f'{coin.capitalize()} is thrown {n} times. The random variable X is the number of heads obtained.', xs, ps


@d153.add('C1', (1, 2, 3))
def d153_c1(r, D):
    intro, xs, ps = ctx_dist(r)
    i = r.randrange(len(xs))
    p = ps[i]
    return MC(r, intro + f' Find P(X = {xs[i]}).', num(p), [num(1 - p) if 1 - p != p else num(p / 2), num(Fr(1, len(xs))) if Fr(1, len(xs)) != p else num(p * 2) if p * 2 < 1 else num(p / 3), num(ps[(i + 1) % len(xs)]) if ps[(i + 1) % len(xs)] != p else num(p + Fr(1, 36)), num(p * p)],
              f'P(X = {xs[i]}) = {num(p)}.')


@d153.add('C2', (2, 3, 4), 'explain')
def d153_err(r, D):
    intro, xs, ps = ctx_dist(r)
    nm = person(r)
    if len(set(ps)) == 1:
        return None
    return Q(intro + f' {nm} says that X takes the values {", ".join(map(str, xs))}, so each value has probability 1/{len(xs)}. Explain why {nm} is wrong, and find the correct value of P(X = {xs[0]}).',
             f'The values of X are not equally likely, since different numbers of outcomes give each value; P(X = {xs[0]}) = {num(ps[0])}.',
             f'B1 values not equally likely; B1 P(X = {xs[0]}) = {num(ps[0])}')


@d153.add('C3', (1, 2, 3, 4, 5), 'numerical')
def d153_calc(r, D):
    intro, xs, ps = ctx_dist(r)
    if len(xs) > 7:
        return None
    e = EX(xs, ps)
    tab = ptab(xs, [num(p) for p in ps])
    if D <= 3:
        return Q(intro + ' Draw up the probability distribution table for X.', tab,
                 f'B1 values {", ".join(map(str, xs))}; M1 method for at least two probabilities; A1 all correct, summing to 1')
    v = VX(xs, ps)
    return Q(intro + ' Draw up the probability distribution table for X and find E(X).', f'{tab}; E(X) = {prs(e)}',
             f'B1 values; M1 probabilities; A1 table; M1 Σx P(X = x); A1 E(X) = {prs(e)}')


def d153_c4(r, D):
    intro, xs, ps = ctx_dist(r)
    if len(xs) > 7:
        return None
    e = EX(xs, ps)
    v = VX(xs, ps)
    tab = ptab(xs, [num(p) for p in ps])
    k = xs[len(xs) // 2]
    parts = [
        P('Draw up the probability distribution table for X.', tab, 'B1 values; M1 probabilities; A1 all correct'),
        P('Find E(X).', prs(e), f'M1 Σx P(X = x); A1 {prs(e)}'),
        P('Find Var(X).', prs(v), f'M1 E(X²) − [E(X)]²; A1 {prs(v)}'),
        P(f'Find P(X ≥ {k}).', num(sum(p for x, p in zip(xs, ps) if x >= k)), f'B1 {num(sum(p for x, p in zip(xs, ps) if x >= k))}'),
    ]
    return cmp_(r, intro, parts)


d153.add('C4', (2, 3, 4, 5))(d153_c4)

CHAPTERS[15] = [d151, d152, d153]


# ================================================================ Chapter 16 The binomial and geometric distributions

def bpmf(n, p, x):
    return comb(n, x) * p ** x * (1 - p) ** (n - x)


def bcdf(n, p, x):
    return sum(bpmf(n, p, i) for i in range(0, x + 1))


BIN_CTX = [('{p}% of the seeds in a large batch fail to germinate', 'seeds', 'fail to germinate', 'fails to germinate', [5, 10, 15, 20, 25, 30]),
           ('{p}% of the light bulbs made by a factory are faulty', 'bulbs', 'are faulty', 'is faulty', [2, 4, 5, 6, 8, 10, 12, 15]),
           ('{p}% of the students at a large college walk to college', 'students', 'walk to college', 'walks to college', [15, 20, 25, 30, 35, 40, 45, 55, 60]),
           ('{p}% of the people in a city are left-handed', 'people', 'are left-handed', 'is left-handed', [8, 10, 12, 15]),
           ('{p}% of the apples from an orchard are bruised', 'apples', 'are bruised', 'is bruised', [5, 10, 15, 20, 25]),
           ('{p}% of the customers at a café order tea', 'customers', 'order tea', 'orders tea', [20, 25, 30, 35, 40, 45, 55, 60, 65, 70]),
           ('{p}% of the trains on a route arrive on time', 'trains', 'arrive on time', 'arrives on time', [60, 65, 70, 75, 80, 85, 90])]


def rbin(r):
    ctx = r.choice(BIN_CTX)
    n = r.randint(6, 20)
    pc = r.choice(ctx[4])
    return n, pc, Fr(pc, 100), ctx


def bv(ctx, x):
    return ctx[3] if x == 1 else ctx[2]


def xnear(r, n, p, lo=0, hi=None):
    hi = n if hi is None else hi
    x = int(round(float(n * p))) + r.randint(-2, 2)
    return max(lo, min(hi, x))


b161 = T('The binomial distribution B(n, p) and its probabilities', 'binomial distribution', 'B(n, p)')
b161.fixed('C1', (1, 2), [
    ('Which is a condition for a binomial model?', 'a fixed number of independent trials', 'Also two outcomes per trial and constant p.', ['the trials continue until a success', 'the probability of success changes each trial', 'there are more than two outcomes per trial']),
    ('If X ~ B(n, p), then P(X = r) =', 'ⁿCᵣ pʳ(1 − p)ⁿ⁻ʳ', 'Choose which r trials are successes.', ['pʳ(1 − p)ⁿ⁻ʳ', 'ⁿCᵣ pⁿ', '(1 − p)ʳ⁻¹p']),
    ('If X ~ B(4, 0.5), then P(X = 4) =', '0.0625', '0.5⁴.', ['0.5', '0.25', '0.125']),
    ('For X ~ B(n, p), P(X ≥ 1) =', '1 − (1 − p)ⁿ', 'Complement of no successes.', ['np', '1 − pⁿ', 'pⁿ']),
])
b161.fixed('C2', (2, 3), [
    ('State two conditions needed for the number of heads in 10 throws of a coin to be modelled by a binomial distribution.', 'The throws are independent, and the probability of a head is the same for each throw.', 'B1 independence; B1 constant probability [2]'),
    ('Explain why the number of aces in a hand of 5 cards dealt from a pack is not binomially distributed.', 'The cards are dealt without replacement, so the trials are not independent and the probability of an ace changes.', 'B1 without replacement; B1 not independent / p changes [2]'),
])


@b161.add('C1', (1, 2, 3))
def b161_c1(r, D):
    n = r.randint(3, 8)
    p = Fr(r.randint(1, 9), 10)
    x = r.randint(0, n)
    v = bpmf(n, p, x)
    return MC(r, f'X ~ B({n}, {dn(p)}). Find P(X = {x}), correct to 3 significant figures.', n3(float(v)),
              [n3(float(p ** x * (1 - p) ** (n - x))) if comb(n, x) > 1 else n3(float(bpmf(n, p, max(0, x - 1)))), n3(float(bcdf(n, p, x))) if x < n else n3(float(1 - v)), n3(float(comb(n, x) * p ** (n - x) * (1 - p) ** x)) if p != Fr(1, 2) else n3(float(bpmf(n, p, (x + 1) % (n + 1)))), n3(float(v) * 2)],
              f'{n}C{x} × {dn(p)}{sup(x)} × {dn(1 - p)}{sup(n - x)} = {n3(float(v))}.')


@b161.add('C2', (2, 3, 4), 'explain')
def b161_err(r, D):
    n, pc, p, ctx = rbin(r)
    x = xnear(r, n, p, 1, n - 1)
    nm = person(r)
    wrong = p ** x * (1 - p) ** (n - x)
    right = bpmf(n, p, x)
    return Q(f'{ctx[0].format(p=pc)}. A random sample of {n} {ctx[1]} is taken. {nm} says that the probability that exactly {x} {bv(ctx, x)} is {dn(p)}{sup(x)} × {dn(1 - p)}{sup(n - x)} = {sci(float(wrong)) if wrong < Fr(1, 1000) else n3(float(wrong))}. Explain the error and find the correct probability.',
             f'This is the probability of one particular order only; multiply by {n}C{x} = {comb(n, x)} for the different orders: {n3(float(right))}.',
             f'B1 must multiply by {n}C{x}; B1 {n3(float(right))}')


@b161.add('C2', (2, 3, 4), 'explain')
def b161_model(r, D):
    a, b = r.randint(5, 12), r.randint(5, 12)
    k = r.randint(3, 6)
    kind = r.choice(['without', 'with', 'large'])
    if kind == 'without':
        return Q(f'A bag contains {a} red and {b} blue beads. {k} beads are taken at random without replacement, and X is the number of red beads. Explain whether X can be modelled by B({k}, {num(Fr(a, a + b))}).',
                 'No: without replacement the selections are not independent and the probability of a red bead changes after each selection.', 'B1 not binomial; B1 not independent / p changes')
    if kind == 'with':
        return Q(f'A bag contains {a} red and {b} blue beads. {k} beads are taken at random with replacement, and X is the number of red beads. Explain whether X can be modelled by a binomial distribution, stating its parameters if so.',
                 f'Yes: with replacement the {k} selections are independent with constant probability {num(Fr(a, a + b))} of red, so X ~ B({k}, {num(Fr(a, a + b))}).', f'B1 independent, constant p; B1 B({k}, {num(Fr(a, a + b))})')
    return Q(f'In a large population, {a * 5}% of people have blood group B. A random sample of {k + 10} people is chosen without replacement. Explain why a binomial model is still reasonable for the number of people in the sample with blood group B.',
             'The population is very large compared with the sample, so removing a few people barely changes the probability; the selections are approximately independent.', 'B1 large population; B1 p approximately constant / approximately independent')


@b161.add('C3', (1, 2, 3, 4, 5), 'numerical')
def b161_calc(r, D):
    n, pc, p, ctx = rbin(r)
    stem = f'{ctx[0].format(p=pc)}. A random sample of {n} {ctx[1]} is taken.'
    if D <= 2:
        x = xnear(r, n, p, 1)
        v = bpmf(n, p, x)
        return Q(stem + f' Find the probability that exactly {x} {bv(ctx, x)}.', n3(float(v)), f'M1 {n}C{x} × {dn(p)}{sup(x)} × {dn(1 - p)}{sup(n - x)}; A1 {n3(float(v))}')
    if D == 3:
        x = max(1, min(n - 1, int(float(n * p)) - r.randint(0, 2)))
        v = bcdf(n, p, x)
        return Q(stem + f' Find the probability that at most {x} {bv(ctx, x)}.', n3(float(v)), f'M1 P(0) + … + P({x}); M1 binomial terms; A1 {n3(float(v))}')
    if D == 4:
        x = max(2, min(n - 1, math.ceil(float(n * p)) + r.randint(0, 2)))
        v = 1 - bcdf(n, p, x - 1)
        return Q(stem + f' Find the probability that at least {x} {bv(ctx, x)}.', n3(float(v)), f'M1 1 − P(X ≤ {x - 1}) or P(X = {x}) + … + P(X = {n}); M1 correct binomial terms; A1 {n3(float(v))}')
    if r.random() < 0.5:
        a = max(0, int(round(float(n * p))) - r.randint(1, 3))
        b = a + r.randint(3, 5)
        if b >= n:
            return None
        v = bcdf(n, p, b - 1) - bcdf(n, p, a)
        return Q(stem + f' Find the probability that more than {a} but fewer than {b} {ctx[2]}.', n3(float(v)), f'M1 P(X = {a + 1}) + … + P(X = {b - 1}); M1 binomial terms; A1 {n3(float(v))}')
    tgt = r.choice([Fr(9, 10), Fr(95, 100), Fr(99, 100)])
    m = 1
    while 1 - (1 - p) ** m <= tgt:
        m += 1
    return Q(f'{ctx[0].format(p=pc)}. Find the least number of {ctx[1]} that must be chosen at random so that the probability that at least one {ctx[3]} is greater than {dn(tgt)}.', str(m),
             f'M1 1 − {dn(1 - p)}ⁿ > {dn(tgt)}; M1 solves by logarithms or trial; A1 n = {m}')


def b161_c4(r, D):
    n, pc, p, ctx = rbin(r)
    x = max(1, min(n - 1, int(float(n * p)) + r.randint(0, 2)))
    days = r.randint(3, 6)
    pe = bpmf(n, p, x)
    pl = bcdf(n, p, x)
    pd = pl ** days
    intro = f'{ctx[0].format(p=pc)}. Random samples of {n} {ctx[1]} are taken.'
    parts = [
        P('State a condition needed for a binomial model to be valid here.', 'the items are independent of each other (or: constant probability for each item)', 'B1 independence or constant p in context'),
        P(f'Find the probability that, in one sample, exactly {x} {bv(ctx, x)}.', n3(float(pe)), f'M1 {n}C{x} × {dn(p)}{sup(x)} × {dn(1 - p)}{sup(n - x)}; A1 {n3(float(pe))}'),
        P(f'Find the probability that, in one sample, at most {x} {bv(ctx, x)}.', n3(float(pl)), f'M1 sum of P(0) to P({x}); A1 {n3(float(pl))}'),
        P(f'{days} samples are taken. Find the probability that every one of them has at most {x} that {ctx[2]}.', n3(float(pd)), f'M1 ({n3(float(pl))}){sup(days)}; A1 {n3(float(pd))}'),
    ]
    return cmp_(r, intro, parts)


b161.add('C4', (2, 3, 4, 5))(b161_c4)


b162 = T('Mean and variance of the binomial distribution', 'mean and variance of the binomial', 'np', 'np(1 − p)')
b162.fixed('C1', (1, 2), [
    ('If X ~ B(n, p), then E(X) =', 'np', 'Expected number of successes.', ['n(1 − p)', 'np(1 − p)', 'p/n']),
    ('If X ~ B(n, p), then Var(X) =', 'np(1 − p)', 'Var = npq.', ['np', 'np²', 'n²p(1 − p)']),
    ('If X ~ B(20, 0.3), then E(X) =', '6', '20 × 0.3.', ['4.2', '14', '0.3']),
    ('For any binomial distribution, the variance is', 'less than the mean', 'npq < np since q < 1.', ['greater than the mean', 'equal to the mean', 'equal to n']),
])
b162.fixed('C2', (2, 3), [
    ('Explain why a binomial distribution cannot have mean 4 and variance 5.', 'Variance = np(1 − p) = mean × (1 − p), which is less than the mean since 1 − p < 1; 5 > 4 is impossible.', 'B1 Var = mean × q; B1 q < 1 so Var < mean [2]'),
    ('Explain what E(X) = 7.5 means for X ~ B(25, 0.3), the number of successes in 25 trials.', 'In the long run the average number of successes per set of 25 trials is 7.5, although X itself takes only whole-number values.', 'B1 long-run average; B1 need not be a possible value [2]'),
])


@b162.add('C1', (1, 2, 3))
def b162_c1(r, D):
    n = r.randint(10, 80)
    p = Fr(r.randint(1, 19), 20)
    kind = r.choice(['mean', 'var', 'sd'])
    if kind == 'mean':
        return MC(r, f'X ~ B({n}, {dn(p)}). Find E(X).', dn(n * p), [dn(n * p * (1 - p)), dn(n * (1 - p)) if p != Fr(1, 2) else dn(n * p + 1), dn(p / n) if p / n != n * p else dn(n * p - 1), dn(n * p * p)], f'E(X) = np = {dn(n * p)}.')
    if kind == 'var':
        v = n * p * (1 - p)
        return MC(r, f'X ~ B({n}, {dn(p)}). Find Var(X).', dn(v), [dn(n * p), dn(n * p * p), n3(math.sqrt(v)) if n3(math.sqrt(v)) != dn(v) else dn(v + 1), dn(n * (1 - p) ** 2) if n * (1 - p) ** 2 != v else dn(v * 2)], f'np(1 − p) = {dn(v)}.')
    v = n * p * (1 - p)
    return MC(r, f'X ~ B({n}, {dn(p)}). Find the standard deviation of X.', n3(math.sqrt(v)), [n3(float(v)) if abs(float(v) - math.sqrt(v)) > 1e-9 else n3(float(v) + 1), n3(math.sqrt(n * p)), n3(math.sqrt(n) * float(p)), n3(math.sqrt(v) / 2)], f'√(np(1 − p)) = √{dn(v)} = {n3(math.sqrt(v))}.')


@b162.add('C2', (2, 3, 4), 'explain')
def b162_check(r, D):
    m = r.randint(3, 30)
    good = r.random() < 0.5
    if good:
        n = r.randint(m + 2, 4 * m + 10)
        p = Fr(m, n)
        v = n * p * (1 - p)
        return Q(f'A student claims that X ~ B(n, p) with E(X) = {m} and Var(X) = {dn(v) if v.denominator in (1, 2, 4, 5, 10, 20, 25, 50) else num(v)}. Determine whether this is possible, finding n and p if it is.',
                 f'Possible: 1 − p = Var/E = {num(1 - p)}, so p = {num(p)} and n = {m}/p = {n}.', f'M1 q = Var/mean; A1 p = {num(p)}; A1 n = {n}')
    v = m + r.randint(1, 5)
    return Q(f'A student claims that X ~ B(n, p) with E(X) = {m} and Var(X) = {v}. Explain why this is not possible.', f'Var(X) = E(X) × (1 − p) must be less than E(X), but {v} > {m}.', 'B1 Var = mean × q; B1 q < 1 so contradiction')


@b162.add('C3', (1, 2, 3, 4, 5), 'numerical')
def b162_calc(r, D):
    n = r.randint(8, 60)
    p = Fr(r.randint(1, 19), 20)
    v = n * p * (1 - p)
    if D <= 2:
        return Q(f'X ~ B({n}, {dn(p)}). Find E(X), Var(X) and the standard deviation of X.', f'E(X) = {dn(n * p)}; Var(X) = {dn(v)}; sd = {n3(math.sqrt(v))}',
                 f'B1 np = {dn(n * p)}; B1 np(1 − p) = {dn(v)}; B1 {n3(math.sqrt(v))}')
    if D <= 4:
        if v.denominator > 100:
            return None
        return Q(f'X ~ B(n, p) with E(X) = {dn(n * p)} and Var(X) = {dn(v)}. Find n and p.', f'n = {n}, p = {dn(p)}',
                 f'M1 1 − p = {dn(v)}/{dn(n * p)}; A1 p = {dn(p)}; M1 n = {dn(n * p)}/p; A1 n = {n}')
    n = r.randint(6, 15)
    p = Fr(r.randint(1, 9), 10)
    m = n * p
    lo = [x for x in range(n + 1) if x < m]
    pr_ = bcdf(n, p, max(lo)) if lo else 0
    return Q(f'X ~ B({n}, {dn(p)}). Find E(X), and the probability that X is less than its mean.', f'E(X) = {dn(m)}; P(X < {dn(m)}) = {n3(float(pr_))}',
             f'B1 E(X) = {dn(m)}; M1 P(X ≤ {max(lo) if lo else 0}); A1 {n3(float(pr_))}')


@b162.add('C3', (2, 3, 4), 'numerical')
def b162_ctx(r, D):
    n, pc, p, ctx = rbin(r)
    n = n * r.choice([5, 10])
    v = n * p * (1 - p)
    return Q(f'{ctx[0].format(p=pc)}. A random sample of {n} {ctx[1]} is taken, and X is the number of these that {ctx[2]}. Find the expected value and the standard deviation of X.', f'E(X) = {dn(n * p)}; sd = {n3(math.sqrt(v))}',
             f'B1 X ~ B({n}, {dn(p)}); B1 E(X) = {dn(n * p)}; M1 √(np(1 − p)); A1 {n3(math.sqrt(v))}')


def b162_c4(r, D):
    n = r.randint(6, 15)
    p = Fr(r.randint(1, 9), 10)
    m = n * p
    v = m * (1 - p)
    sd = math.sqrt(v)
    lo, hi = float(m) - sd, float(m) + sd
    within = sum(bpmf(n, p, x) for x in range(n + 1) if lo < x < hi)
    xm = math.floor(m)
    intro = f'The random variable X has the distribution B({n}, {dn(p)}).'
    parts = [
        P('Find E(X) and Var(X).', f'{dn(m)}, {dn(v)}', f'B1 {dn(m)}; B1 {dn(v)}'),
        P('Find the standard deviation of X.', n3(sd), f'B1 {n3(sd)}'),
        P('Find the probability that X lies within one standard deviation of its mean.', n3(float(within)), f'M1 identifies integers between {n3(lo)} and {n3(hi)}; M1 sums binomial probabilities; A1 {n3(float(within))}'),
        P(f'Find P(X = {xm}).', n3(float(bpmf(n, p, xm))), f'M1 {n}C{xm} × {dn(p)}{sup(xm)} × {dn(1 - p)}{sup(n - xm)}; A1 {n3(float(bpmf(n, p, xm)))}'),
    ]
    return cmp_(r, intro, parts)


b162.add('C4', (2, 3, 4, 5))(b162_c4)


b163 = T('The geometric distribution Geo(p) and its mean', 'geometric distribution', 'Geo(p)')
b163.fixed('C1', (1, 2), [
    ('If X ~ Geo(p), then P(X = r) =', '(1 − p)ʳ⁻¹p', 'r − 1 failures followed by a success.', ['ⁿCᵣ pʳ(1 − p)ⁿ⁻ʳ', 'pʳ⁻¹(1 − p)', '(1 − p)ʳp']),
    ('If X ~ Geo(p), then E(X) =', '1/p', 'Mean number of trials up to the first success.', ['p', '(1 − p)/p', 'np']),
    ('If X ~ Geo(p), then P(X > r) =', '(1 − p)ʳ', 'The first r trials are all failures.', ['1 − (1 − p)ʳ', 'pʳ', '(1 − p)ʳ⁻¹']),
    ('A fair die is thrown until a six appears. The expected number of throws is', '6', '1/(1/6).', ['3.5', '5', '1/6']),
])
b163.fixed('C2', (2, 3), [
    ('State the conditions under which the number of trials up to and including the first success has a geometric distribution.', 'The trials are independent, each with the same probability p of success, and they continue until the first success.', 'B1 independent trials; B1 constant p, stop at first success [2]'),
    ('Explain the difference between a binomial and a geometric random variable.', 'A binomial variable counts successes in a fixed number of trials; a geometric variable counts the trials needed to obtain the first success.', 'B1 binomial: fixed n, count successes; B1 geometric: trials until first success [2]'),
])

GEO_CTX = [('{nm} throws a fair die until a six is obtained', Fr(1, 6), 'throws'), ('{nm} keeps buying a cereal box until it contains a prize; each box contains a prize with probability {p}', None, 'boxes'),
           ('An archer shoots at a target until she hits the bullseye; each shot hits with probability {p}', None, 'shots'), ('{nm} keeps taking a driving test until passing; the probability of passing each attempt is {p}', None, 'attempts'),
           ('A machine produces items until a faulty one appears; each item is faulty with probability {p}', None, 'items'), ('{nm} throws a fair coin until a head is obtained', Fr(1, 2), 'throws')]


def rgeo(r):
    c = r.choice(GEO_CTX)
    p = c[1] or Fr(r.choice([1, 2, 3, 4, 5, 6, 8, 12, 15, 25, 30, 35, 40]), 100) * r.choice([1, 1, 2])
    if p >= 1:
        p = Fr(1, 4)
    return c[0].format(nm=person(r), p=dn(p)), p, c[2]


@b163.add('C1', (1, 2, 3))
def b163_c1(r, D):
    desc, p, unit = rgeo(r)
    k = r.randint(2, 6)
    kind = r.choice(['eq', 'mean', 'gt'])
    q = 1 - p
    if kind == 'mean':
        return MC(r, f'{desc}. Find the expected number of {unit}.', dn(1 / p) if (1 / p).denominator in (1, 2, 4, 5, 10) else n3(float(1 / p)),
                  [dn(p), dn(q / p) if (q / p).denominator in (1, 2, 4, 5, 10) else n3(float(q / p)), dn(1 / q) if (1 / q).denominator in (1, 2, 4, 5, 10) else n3(float(1 / q)), dn(2 / p) if (2 / p).denominator in (1, 2, 4, 5, 10) else n3(float(2 / p))], 'E(X) = 1/p.')
    if kind == 'eq':
        v = q ** (k - 1) * p
        return MC(r, f'{desc}. Find the probability that exactly {k} {unit} are needed.', n3(float(v)), [n3(float(q ** k * p)), n3(float(p ** (k - 1) * q)) if p != q else n3(float(p ** k)), n3(float(1 - q ** k)), n3(float(q ** (k - 1)))], f'({dn(q) if q.denominator in (1, 2, 4, 5, 10, 20, 25, 50, 100) else num(q)}){sup(k - 1)} × {dn(p) if p.denominator in (1, 2, 4, 5, 10, 20, 25, 50, 100) else num(p)} = {n3(float(v))}.')
    v = q ** k
    return MC(r, f'{desc}. Find the probability that more than {k} {unit} are needed.', n3(float(v)), [n3(float(1 - v)), n3(float(q ** (k - 1))), n3(float(q ** k * p)), n3(float(q ** (k + 1)))], f'P(X > {k}) = q{sup(k)} = {n3(float(v))}.')


@b163.add('C2', (2, 3, 4), 'explain')
def b163_err(r, D):
    desc, p, unit = rgeo(r)
    q = 1 - p
    k = r.randint(3, 7)
    nm = person(r)
    kind = r.choice(['pow', 'le'])
    if kind == 'pow':
        return Q(f'{desc}. {nm} says the probability that exactly {k} {unit} are needed is q{sup(k)} × p, where q = 1 − p. Explain the error and find the correct probability.',
                 f'Exactly {k} {unit} means {k - 1} failures followed by a success, so it is q{sup(k - 1)}p = {n3(float(q ** (k - 1) * p))}.', f'B1 only {k - 1} failures; B1 {n3(float(q ** (k - 1) * p))}')
    return Q(f'{desc}. {nm} says that P(at most {k} {unit} are needed) = q{sup(k)}, where q = 1 − p. Explain the error and find the correct probability.',
             f'q{sup(k)} is the probability that the first {k} {unit} are all failures, i.e. P(X > {k}); P(X ≤ {k}) = 1 − q{sup(k)} = {n3(float(1 - q ** k))}.', f'B1 q{sup(k)} = P(X > {k}); B1 {n3(float(1 - q ** k))}')


@b163.add('C3', (1, 2, 3, 4, 5), 'numerical')
def b163_calc(r, D):
    desc, p, unit = rgeo(r)
    q = 1 - p
    if D <= 2:
        k = r.randint(2, 8)
        return Q(f'{desc}. Find the probability that exactly {k} {unit} are needed.', n3(float(q ** (k - 1) * p)), f'M1 q{sup(k - 1)}p; A1 {n3(float(q ** (k - 1) * p))}')
    if D == 3:
        k = r.randint(3, 10)
        return Q(f'{desc}. Find the probability that at most {k} {unit} are needed.', n3(float(1 - q ** k)), f'M1 1 − q{sup(k)}; M1 q = {dn(q) if q.denominator in (1, 2, 4, 5, 10, 20, 25, 50, 100) else num(q)}; A1 {n3(float(1 - q ** k))}')
    if D == 4:
        a = r.randint(2, 5)
        b = a + r.randint(2, 5)
        v = q ** (a - 1) - q ** b
        return Q(f'{desc}. Find the probability that the number of {unit} needed is between {a} and {b} inclusive.', n3(float(v)), f'M1 P(X ≥ {a}) − P(X > {b}) = q{sup(a - 1)} − q{sup(b)}; M1 values; A1 {n3(float(v))}')
    tgt = r.choice([Fr(9, 10), Fr(95, 100), Fr(99, 100)])
    k = 1
    while 1 - q ** k <= tgt:
        k += 1
    return Q(f'{desc}. Find the least value of n such that the probability that at most n {unit} are needed is greater than {dn(tgt)}.', str(k),
             f'M1 1 − qⁿ > {dn(tgt)}; M1 logarithms or trial; A1 n = {k}')


@b163.add('C3', (2, 3, 4), 'numerical')
def b163_mean(r, D):
    m = r.choice([Fr(5, 2), 4, 5, Fr(10, 3), 8, 10, 20, Fr(25, 4)])
    m = Fr(m)
    p = 1 / m
    q = 1 - p
    k = r.randint(2, 6)
    nm = person(r)
    return Q(f'The number of attempts {nm} needs to solve a puzzle has a geometric distribution with mean {num(m) if m.denominator == 1 else dn(m) if m.denominator in (2, 4) else num(m)}. Find the probability of success on each attempt, and the probability that {nm} first succeeds on attempt {k}.',
             f'p = {pr(p)}; P(X = {k}) = {n3(float(q ** (k - 1) * p))}',
             f'B1 p = 1/{num(m)}; M1 q{sup(k - 1)}p; A1 {n3(float(q ** (k - 1) * p))}')


def b163_c4(r, D):
    desc, p, unit = rgeo(r)
    q = 1 - p
    k = r.randint(3, 6)
    j = r.randint(2, 5)
    intro = f'{desc}. X is the number of {unit} needed.'
    parts = [
        P('State the distribution of X, including its parameter.', f'X ~ Geo({dn(p) if p.denominator in (1, 2, 4, 5, 10, 20, 25, 50, 100) else num(p)})', 'B1 geometric with correct p'),
        P(f'Find P(X = {k}).', n3(float(q ** (k - 1) * p)), f'M1 q{sup(k - 1)}p; A1 {n3(float(q ** (k - 1) * p))}'),
        P(f'Find P(X ≤ {k}).', n3(float(1 - q ** k)), f'M1 1 − q{sup(k)}; A1 {n3(float(1 - q ** k))}'),
        P('Find E(X).', dn(1 / p) if (1 / p).denominator in (1, 2, 4, 5, 10) else n3(float(1 / p)), 'B1 1/p'),
        P(f'Find P(X > {j}).', n3(float(q ** j)), f'M1 q{sup(j)}; A1 {n3(float(q ** j))}'),
    ]
    return cmp_(r, intro, parts)


b163.add('C4', (2, 3, 4, 5))(b163_c4)

CHAPTERS[16] = [b161, b162, b163]


# ================================================================ Chapter 17 The normal distribution

def zr(x, mu, sg_):
    return round((x - mu) / sg_, 3)


def nf(x):
    """Format a parameter or boundary value compactly."""
    return num(x) if isinstance(x, int) or float(x).is_integer() else n3(float(x)) if abs(x) < 100 else f'{x:g}'


NORM_CTX = [('the heights of adult men in a city', 'cm', (165, 185), (5, 10)), ('the masses of bags of rice filled by a machine', 'g', (495, 1010), (3, 12)),
            ('the times taken by students to run 400 m', 's', (60, 95), (4, 12)), ('the lengths of leaves on a tree', 'mm', (40, 120), (5, 15)),
            ('the lifetimes of batteries of a certain type', 'hours', (200, 600), (20, 60)), ('the volumes of drinks dispensed by a machine', 'ml', (240, 510), (4, 15)),
            ('the masses of eggs laid by hens on a farm', 'g', (52, 68), (3, 7)), ('the daily rainfall totals in a region during the wet season', 'mm', (20, 40), (4, 8))]


def rnorm(r):
    c = r.choice(NORM_CTX)
    mu = r.randint(*c[2])
    s = r.randint(*c[3])
    return c, mu, s


def prob3(p):
    return n3(p) if p >= 0.0005 else sci(p)


n171 = T('The normal distribution and standardising using Z = (X − μ)/σ', 'normal distribution', 'standardising', 'Z = (X − μ)/σ')
n171.fixed('C1', (1, 2), [
    ('The normal distribution curve is', 'symmetrical about the mean', 'Mean = median = mode for a normal distribution.', ['skewed to the right', 'symmetrical about 0 for every μ', 'rectangular']),
    ('If Z ~ N(0, 1), then P(Z < 0) =', '0.5', 'By symmetry half of the distribution lies below 0.', ['0', '1', '0.3989']),
    ('For any continuous random variable X, P(X = 5) =', '0', 'Probabilities are areas; a single point has no width.', ['0.5', '1', 'Φ(5)']),
    ('If Z ~ N(0, 1), then P(Z > −a) for a > 0 equals', 'Φ(a)', 'By symmetry P(Z > −a) = P(Z < a).', ['1 − Φ(a)', 'Φ(−a)', '2Φ(a) − 1']),
    ('For X ~ N(μ, σ²), approximately what percentage of values lie within 2 standard deviations of the mean?', '95%', 'P(|Z| < 2) ≈ 0.954.', ['68%', '99.7%', '50%']),
])
n171.fixed('C2', (2, 3), [
    ('Explain why P(X < a) = P(X ≤ a) for a normally distributed random variable X.', 'X is continuous, so P(X = a) = 0; including or excluding the endpoint makes no difference.', 'B1 continuous; B1 P(X = a) = 0 [2]'),
    ('Explain the purpose of standardising a normal random variable.', 'Converting X to Z = (X − μ)/σ gives the standard normal N(0, 1), so a single table of Φ can be used for any normal distribution.', 'B1 transforms to N(0, 1); B1 allows use of tables [2]'),
])


@n171.add('C1', (1, 2, 3))
def n171_c1(r, D):
    kind = r.choice(['lt', 'gt', 'neg', 'z'])
    a = round(r.uniform(0.1, 2.5), 2)
    if kind == 'z':
        c, mu, s = rnorm(r)
        x = mu + r.choice([-1, 1]) * r.randint(1, 2 * s)
        z = (x - mu) / s
        return MC(r, f'X ~ N({mu}, {s}²). Find the value of z obtained when x = {x} is standardised.', z3(z), [z3((x - mu) / (s * s)), z3((mu - x) / s), z3((x + mu) / s / 10) if abs(z) > 0.05 else z3(z + 1), z3(z * 2)], f'z = ({x} − {mu})/{s} = {z3(z)}.')
    if kind == 'lt':
        p = Phi(a)
        return MC(r, f'Z ~ N(0, 1). Find P(Z < {a}).', p4(p), [p4(1 - p), p4(p - 0.5), p4(2 * p - 1)], f'Φ({a}) = {p4(p)}.')
    if kind == 'gt':
        p = 1 - Phi(a)
        return MC(r, f'Z ~ N(0, 1). Find P(Z > {a}).', p4(p), [p4(1 - p), p4(Phi(a) - 0.5), p4(2 * (1 - Phi(a)))], f'1 − Φ({a}) = {p4(p)}.')
    p = Phi(a)
    return MC(r, f'Z ~ N(0, 1). Find P(Z > {MINUS}{a}).', p4(p), [p4(1 - p), p4(p - 0.5), p4(2 * p - 1)], f'By symmetry P(Z > {MINUS}{a}) = Φ({a}) = {p4(p)}.')


@n171.add('C2', (2, 3, 4), 'explain')
def n171_err(r, D):
    c, mu, s = rnorm(r)
    x = mu + r.randint(1, 2 * s)
    nm = person(r)
    p = 1 - Phi((x - mu) / s)
    kind = r.choice(['var', 'side'])
    if kind == 'var':
        return Q(f'X ~ N({mu}, {s * s}). {nm} standardises x = {x} as ({x} − {mu})/{s * s} = {z3((x - mu) / (s * s))}. Explain the error and find P(X > {x}).',
                 f'{s * s} is the variance; divide by the standard deviation {s}: z = {z3((x - mu) / s)}, so P(X > {x}) = {prob3(p)}.',
                 f'B1 must divide by σ = √{s * s}; M1 1 − Φ({z3((x - mu) / s)}); A1 {prob3(p)}')
    return Q(f'X ~ N({mu}, {s}²). {nm} finds P(X > {x}) as Φ({z3((x - mu) / s)}) = {p4(Phi((x - mu) / s))}. Explain the error and find the correct probability.',
             f'Φ(z) gives the area to the left of z, i.e. P(X < {x}); P(X > {x}) = 1 − {p4(Phi((x - mu) / s))} = {prob3(p)}.',
             f'B1 Φ gives P(X < {x}); B1 {prob3(p)}')


@n171.add('C3', (1, 2, 3, 4, 5), 'numerical')
def n171_calc(r, D):
    c, mu, s = rnorm(r)
    if D <= 2:
        x = mu + r.choice([-1, 1]) * r.randint(1, 2 * s)
        z = (x - mu) / s
        if r.random() < 0.5:
            p = Phi(z)
            return Q(f'X ~ N({mu}, {s}²). Find P(X < {x}).', prob3(p), f'M1 standardises: ({x} − {mu})/{s} = {z3(z)}; A1 {prob3(p)}')
        p = 1 - Phi(z)
        return Q(f'X ~ N({mu}, {s * s}). Find P(X > {x}).', prob3(p), f'M1 ({x} − {mu})/{s} = {z3(z)}; M1 1 − Φ; A1 {prob3(p)}')
    if D == 3:
        a = mu - r.randint(1, 2 * s)
        b = mu + r.randint(1, 2 * s)
        p = Phi((b - mu) / s) - Phi((a - mu) / s)
        return Q(f'X ~ N({mu}, {s}²). Find P({a} < X < {b}).', prob3(p), f'M1 standardises both: {z3((a - mu) / s)} and {z3((b - mu) / s)}; M1 Φ({z3((b - mu) / s)}) − Φ({z3((a - mu) / s)}); A1 {prob3(p)}')
    if D == 4:
        pp = r.choice([0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.975, 0.99])
        z = round(invPhi(pp), 3)
        x = mu + z * s
        return Q(f'X ~ N({mu}, {s}²). Find the value of a such that P(X < a) = {pp}.', n3(x) if abs(x) < 1000 else n4(x),
                 f'B1 z = {z3(z)}; M1 (a − {mu})/{s} = {z3(z)}; A1 {n3(x) if abs(x) < 1000 else n4(x)}')
    k = r.choice([1, 1.5, 2, 0.5, 2.5])
    pk = 2 * Phi(k) - 1
    return Q(f'X ~ N({mu}, {s}²). Find P(|X − {mu}| < {nf(k * s)}).', n3(pk), f'M1 P({nf(mu - k * s)} < X < {nf(mu + k * s)}); M1 2Φ({k}) − 1; A1 {n3(pk)}')


@n171.add('C3', (2, 3, 4), 'numerical')
def n171_ctx(r, D):
    c, mu, s = rnorm(r)
    x = mu + r.choice([-1, 1]) * r.randint(1, 2 * s)
    z = (x - mu) / s
    side = r.choice(['more', 'less'])
    p = 1 - Phi(z) if side == 'more' else Phi(z)
    return Q(f'The random variable X represents {c[0]}, where X ~ N({mu}, {s}²) in {c[1]}. Find the probability that a randomly chosen value is {side} than {x} {c[1]}.', prob3(p),
             f'M1 z = ({x} − {mu})/{s} = {z3(z)}; M1 correct area; A1 {prob3(p)}')


def n171_c4(r, D):
    c, mu, s = rnorm(r)
    a = mu - r.randint(1, 2 * s)
    b = mu + r.randint(1, 2 * s)
    pp = r.choice([0.1, 0.2, 0.8, 0.9, 0.95])
    zq = round(invPhi(pp), 3)
    q = mu + zq * s
    intro = f'X ~ N({mu}, {s}²).'
    parts = [
        P(f'Find P(X > {b}).', prob3(1 - Phi((b - mu) / s)), f'M1 z = {z3((b - mu) / s)}; A1 {prob3(1 - Phi((b - mu) / s))}'),
        P(f'Find P(X < {a}).', prob3(Phi((a - mu) / s)), f'M1 z = {z3((a - mu) / s)}; A1 {prob3(Phi((a - mu) / s))}'),
        P(f'Find P({a} < X < {b}).', prob3(Phi((b - mu) / s) - Phi((a - mu) / s)), f'M1 difference of Φ values; A1 {prob3(Phi((b - mu) / s) - Phi((a - mu) / s))}'),
        P(f'Find the value of k such that P(X < k) = {pp}.', n3(q) if abs(q) < 1000 else n4(q), f'B1 z = {z3(zq)}; M1 k = {mu} + {pn(z3(zq))} × {s}; A1 {n3(q) if abs(q) < 1000 else n4(q)}'),
    ]
    return cmp_(r, intro, parts)


n171.add('C4', (2, 3, 4, 5))(n171_c4)


n172 = T('Finding μ and σ from given probabilities', 'finding μ and σ', 'unknown mean', 'unknown standard deviation')
n172.fixed('C1', (1, 2), [
    ('If P(Z < z) = 0.95, then z ≈', '1.645', 'From the critical values of N(0, 1).', ['1.96', '0.95', '2.326']),
    ('If P(Z < z) = 0.975, then z ≈', '1.960', 'From the critical values of N(0, 1).', ['1.645', '2.576', '0.975']),
    ('If P(X < a) = 0.3 for X ~ N(μ, σ²), then a is', 'below the mean', 'Less than half the distribution lies below a.', ['above the mean', 'equal to the mean', 'equal to σ']),
    ('If P(Z < z) = 0.1, then z ≈', '−1.282', 'By symmetry with Φ(1.282) = 0.9.', ['1.282', '−0.1', '0.539']),
])
n172.fixed('C2', (2, 3), [
    ('Explain why, if P(X > 60) = 0.2 for X ~ N(μ, σ²), the z-value used is positive.', 'Only 20% of values lie above 60, which is less than half, so 60 is above the mean and (60 − μ)/σ > 0.', 'B1 less than half above 60; B1 so 60 > μ [2]'),
    ('Explain why two probabilities are needed to find both μ and σ.', 'Each probability gives one linear equation in μ and σ, and two unknowns need two equations.', 'B1 one equation per probability; B1 two unknowns [2]'),
])


@n172.add('C1', (1, 2, 3))
def n172_c1(r, D):
    pp = r.choice([0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.92, 0.95, 0.97, 0.98, 0.99, 0.3, 0.25, 0.2, 0.15, 0.1, 0.05, 0.02])
    z = invPhi(pp)
    return MC(r, f'Z ~ N(0, 1) and P(Z < z) = {pp}. Find z, correct to 3 decimal places.', z3(z), [z3(-z), z3(invPhi(1 - pp / 2)) if abs(invPhi(1 - pp / 2) - z) > 0.001 and abs(invPhi(1 - pp / 2) + z) > 0.001 else z3(z + 0.5), z3(Phi(pp))], f'z = Φ⁻¹({pp}) = {z3(z)}.')


@n172.add('C1', (2, 3))
def n172_c1b(r, D):
    c, mu, s = rnorm(r)
    pp = r.choice([0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95])
    z = round(invPhi(pp), 3)
    x = round(mu + z * s)
    side = r.choice(['<', '>'])
    pr_ = pp if side == '<' else round(1 - pp, 2)
    return MC(r, f'X ~ N(μ, {s}²) and P(X {side} {x}) = {pr_}. Which equation is correct?', f'({x} − μ)/{s} = {z3(z)}',
              [f'({x} − μ)/{s} = {z3(-z)}', f'({x} − μ)/{s * s} = {z3(z)}', f'({x} − μ)/{s} = {pr_}'],
              f'P(X < {x}) = {pp}, so ({x} − μ)/{s} = Φ⁻¹({pp}) = {z3(z)}.')


@n172.add('C2', (2, 3, 4), 'explain')
def n172_err(r, D):
    c, mu, s = rnorm(r)
    pp = r.choice([0.1, 0.15, 0.2, 0.25, 0.3])
    z = round(invPhi(1 - pp), 3)
    x = round(mu + z * s)
    nm = person(r)
    return Q(f'X ~ N(μ, {s}²) and P(X > {x}) = {pp}. {nm} writes ({x} − μ)/{s} = {MINUS}{z3(z)}. Explain the error and find μ.',
             f'Since P(X > {x}) = {pp} < 0.5, {x} is above the mean, so the z-value is +{z3(z)}: μ = {x} − {z3(z)} × {s} = {n3(x - z * s) if abs(x - z * s) < 1000 else n4(x - z * s)}.',
             f'B1 z should be positive; M1 ({x} − μ)/{s} = {z3(z)}; A1 μ = {n3(x - z * s) if abs(x - z * s) < 1000 else n4(x - z * s)}')


@n172.add('C3', (1, 2, 3, 4, 5), 'numerical')
def n172_calc(r, D):
    c, mu, s = rnorm(r)
    if D <= 2:
        pp = r.choice([0.1, 0.2, 0.25, 0.3, 0.7, 0.75, 0.8, 0.9, 0.95])
        z = round(invPhi(pp), 3)
        x = round(mu + z * s)
        mu_ = x - z * s
        return Q(f'X ~ N(μ, {s}²) and P(X < {x}) = {pp}. Find μ.', n3(mu_) if abs(mu_) < 1000 else n4(mu_), f'B1 z = {z3(z)}; M1 ({x} − μ)/{s} = {z3(z)}; A1 μ = {n3(mu_) if abs(mu_) < 1000 else n4(mu_)}')
    if D == 3:
        pp = r.choice([0.05, 0.1, 0.15, 0.2, 0.25])
        z = round(invPhi(1 - pp), 3)
        x = mu + r.randint(1, 3 * s)
        s_ = (x - mu) / z
        return Q(f'X ~ N({mu}, σ²) and P(X > {x}) = {pp}. Find σ.', n3(s_), f'B1 z = {z3(z)}; M1 ({x} − {mu})/σ = {z3(z)}; A1 σ = {n3(s_)}')
    p1 = r.choice([0.05, 0.1, 0.15, 0.2, 0.25, 0.3])
    p2 = r.choice([0.05, 0.1, 0.15, 0.2, 0.25, 0.3])
    z1 = round(invPhi(p1), 3)
    z2_ = round(invPhi(1 - p2), 3)
    a = round(mu + z1 * s)
    b = round(mu + z2_ * s)
    if b <= a:
        return None
    sg_ = (b - a) / (z2_ - z1)
    mu_ = a - z1 * sg_
    return Q(f'X ~ N(μ, σ²). Given that P(X < {a}) = {p1} and P(X > {b}) = {p2}, find μ and σ.', f'μ = {n3(mu_) if abs(mu_) < 1000 else n4(mu_)}, σ = {n3(sg_)}',
             f'B1 z-values {z3(z1)} and {z3(z2_)}; M1 ({a} − μ)/σ = {z3(z1)}; M1 ({b} − μ)/σ = {z3(z2_)}; M1 solves simultaneously; A1 μ = {n3(mu_) if abs(mu_) < 1000 else n4(mu_)}, σ = {n3(sg_)}')


@n172.add('C3', (2, 3, 4, 5), 'numerical')
def n172_ctx(r, D):
    c, mu, s = rnorm(r)
    pp = r.choice([0.05, 0.1, 0.2, 0.25])
    z = round(invPhi(1 - pp), 3)
    pct = round(pp * 100)
    if r.random() < 0.5:
        x = mu + r.randint(1, 2 * s)
        s_ = (x - mu) / z
        return Q(f'{c[0].capitalize()} are normally distributed with mean {mu} {c[1]}. {pct}% of the values are greater than {x} {c[1]}. Find the standard deviation.', f'{n3(s_)} {c[1]}',
                 f'B1 z = {z3(z)}; M1 ({x} − {mu})/σ = {z3(z)}; A1 {n3(s_)}')
    x = mu - r.randint(1, 2 * s)
    mu_ = x + z * s
    return Q(f'{c[0].capitalize()} are normally distributed with standard deviation {s} {c[1]}. {pct}% of the values are less than {x} {c[1]}. Find the mean.', f'{n3(mu_) if abs(mu_) < 1000 else n4(mu_)} {c[1]}',
             f'B1 z = {MINUS}{z3(z)}; M1 ({x} − μ)/{s} = {MINUS}{z3(z)}; A1 {n3(mu_) if abs(mu_) < 1000 else n4(mu_)}')


def n172_c4(r, D):
    c, mu, s = rnorm(r)
    p1 = r.choice([0.1, 0.15, 0.2, 0.25])
    p2 = r.choice([0.05, 0.1, 0.2, 0.3])
    z1 = round(invPhi(p1), 3)
    z2_ = round(invPhi(1 - p2), 3)
    a = round(mu + z1 * s)
    b = round(mu + z2_ * s)
    if b <= a:
        return None
    sg_ = (b - a) / (z2_ - z1)
    mu_ = a - z1 * sg_
    x = round(mu_ + r.choice([-1, 1]) * sg_ * r.choice([0.5, 1, 1.5]))
    intro = f'{c[0].capitalize()} are modelled by X ~ N(μ, σ²) in {c[1]}. It is known that {round(p1 * 100)}% of values are less than {a} and {round(p2 * 100)}% are greater than {b}.'
    fm = n3(mu_) if abs(mu_) < 1000 else n4(mu_)
    parts = [
        P('Write down two equations in μ and σ.', f'({a} − μ)/σ = {z3(z1)}; ({b} − μ)/σ = {z3(z2_)}', f'B1 z = {z3(z1)}; B1 z = {z3(z2_)}; M1 both equations'),
        P('Find μ and σ.', f'μ = {fm}, σ = {n3(sg_)}', f'M1 solves simultaneously; A1 μ = {fm}; A1 σ = {n3(sg_)}'),
        P(f'Using μ = {fm} and σ = {n3(sg_)}, find P(X > {x}).', prob3(1 - Phi((x - mu_) / sg_)), f'M1 standardises; A1 {prob3(1 - Phi((x - mu_) / sg_))}'),
    ]
    return cmp_(r, intro, parts, k=(2, 3))


n172.add('C4', (2, 3, 4, 5))(n172_c4)


n173 = T('Modelling with the normal distribution', 'modelling with the normal distribution', 'normal model')
n173.fixed('C1', (1, 2), [
    ('Which variable is most suitably modelled by a normal distribution?', 'the heights of adult women', 'Continuous, symmetric and bell-shaped.', ['the number of heads in 3 coin throws', 'the score on a fair die', 'the number of cars owned by a household']),
    ('A normal model for times with mean 4 minutes and standard deviation 3 minutes is unsuitable because', 'it would give a substantial probability of negative times', 'P(T < 0) = Φ(−1.33) ≈ 0.09.', ['the mean is too small', 'times are discrete', 'the variance is 9']),
    ('If P(X > 70) = 0.12, the expected number of 200 people with X > 70 is', '24', '200 × 0.12.', ['12', '0.12', '176']),
    ('About what percentage of a normal distribution lies within one standard deviation of the mean?', '68%', '2Φ(1) − 1 ≈ 0.683.', ['50%', '95%', '34%']),
])
n173.fixed('C2', (2, 3), [
    ('Explain why a normal distribution may be a suitable model for the masses of apples from an orchard.', 'Mass is continuous, and masses are likely to cluster symmetrically around a mean value with few very light or very heavy apples.', 'B1 continuous; B1 symmetric, bell-shaped about the mean [2]'),
    ('Give one reason why a normal distribution may not be a good model for the number of children in a family.', 'The number of children is discrete and the distribution is likely to be skewed, with no negative values.', 'B1 discrete; B1 skewed / bounded below [2]'),
])


@n173.add('C1', (2, 3))
def n173_c1(r, D):
    c, mu, s = rnorm(r)
    x = mu + r.randint(1, 2 * s)
    N = r.choice([100, 200, 250, 400, 500, 800, 1000])
    p = 1 - Phi((x - mu) / s)
    e = N * p
    return MC(r, f'{c[0].capitalize()} are normally distributed with mean {mu} {c[1]} and standard deviation {s} {c[1]}. In a sample of {N}, how many would you expect to be greater than {x} {c[1]}?', str(round(e)),
              [str(round(N * (1 - p))), str(round(N * (Phi((x - mu) / s) - 0.5))) if round(N * (Phi((x - mu) / s) - 0.5)) != round(e) else str(round(e) + 10), str(round(e / 2)) if round(e / 2) != round(e) else str(round(e) + 5), str(round(e) + max(3, round(e * 0.3)))],
              f'P = 1 − Φ({z3((x - mu) / s)}) = {p4(p)}; {N} × {p4(p)} ≈ {round(e)}.')


@n173.add('C2', (2, 3, 4), 'explain')
def n173_suit(r, D):
    ctx = r.choice([('the times, in minutes, that customers wait at a bank', 'minutes'), ('the amounts, in dollars, spent by customers in a shop', 'dollars'), ('the distances, in km, that students travel to school', 'km')])
    s = r.randint(3, 10)
    bad = r.random() < 0.5
    mu = r.randint(s, 2 * s) if bad else r.randint(4 * s, 6 * s)
    p0 = Phi(-mu / s)
    return Q(f'It is suggested that {ctx[0]} are normally distributed with mean {mu} and standard deviation {s}. Comment on the suitability of this model.',
             (f'Unsuitable: P(X < 0) = Φ({z3(-mu / s)}) = {p4(p0)}, a substantial probability of negative {ctx[1]}, which is impossible.' if bad else
              f'Plausible: P(X < 0) = Φ({z3(-mu / s)}) ≈ {prob3(p0)} is negligible, so negative values are very unlikely; but the data might be skewed, which should be checked.'),
             'M1 considers P(X < 0) or μ − 3σ; A1 conclusion in context')


@n173.add('C3', (1, 2, 3, 4, 5), 'numerical')
def n173_calc(r, D):
    c, mu, s = rnorm(r)
    if D <= 2:
        x = mu + r.choice([-1, 1]) * r.randint(1, 2 * s)
        p = 1 - Phi((x - mu) / s)
        pc = p * 100
        return Q(f'{c[0].capitalize()} are normally distributed with mean {mu} {c[1]} and standard deviation {s} {c[1]}. Find the percentage of values greater than {x} {c[1]}.', f'{n3(pc)}%',
                 f'M1 z = {z3((x - mu) / s)}; M1 1 − Φ(z); A1 {n3(pc)}%')
    if D == 3:
        a = mu - r.randint(1, 2 * s)
        b = mu + r.randint(1, 2 * s)
        N = r.choice([200, 300, 500, 1000, 1200])
        p = Phi((b - mu) / s) - Phi((a - mu) / s)
        return Q(f'{c[0].capitalize()} are normally distributed with mean {mu} {c[1]} and standard deviation {s} {c[1]}. In a sample of {N}, estimate how many values lie between {a} and {b} {c[1]}.', str(round(N * p)),
                 f'M1 standardises {a} and {b}; A1 P = {n3(p)}; M1 × {N}; A1 {round(N * p)}')
    if D == 4:
        x = mu + r.randint(1, 2 * s)
        k = r.choice([2, 3, 4])
        p = 1 - Phi((x - mu) / s)
        return Q(f'{c[0].capitalize()} are normally distributed with mean {mu} {c[1]} and standard deviation {s} {c[1]}. {k} values are chosen at random. Find the probability that all {k} are greater than {x} {c[1]}.', prob3(p ** k),
                 f'M1 P(X > {x}) = {n3(p)}; M1 raised to power {k}; A1 {prob3(p ** k)}')
    x = mu + r.randint(1, 2 * s)
    N = r.randint(8, 15)
    p = 1 - Phi((x - mu) / s)
    pb = bcdf(N, p, 1) if p < 1 else 0
    return Q(f'{c[0].capitalize()} are normally distributed with mean {mu} {c[1]} and standard deviation {s} {c[1]}. A random sample of {N} is taken. Find the probability that at most 1 of them is greater than {x} {c[1]}.', prob3(pb),
             f'M1 P(X > {x}) = {n3(p)}; M1 binomial B({N}, {n3(p)}); M1 P(0) + P(1); A1 {prob3(pb)}')


def n173_c4(r, D):
    c, mu, s = rnorm(r)
    a = mu - r.randint(1, 2 * s)
    b = mu + r.randint(1, 2 * s)
    N = r.choice([200, 300, 500, 1000])
    p_in = Phi((b - mu) / s) - Phi((a - mu) / s)
    pp = r.choice([0.05, 0.1])
    z = round(invPhi(1 - pp), 3)
    lim = mu + z * s
    intro = f'{c[0].capitalize()} are modelled by a normal distribution with mean {mu} {c[1]} and standard deviation {s} {c[1]}.'
    parts = [
        P(f'Find the probability that a randomly chosen value is between {a} and {b} {c[1]}.', n3(p_in), f'M1 standardises both; M1 difference of Φ values; A1 {n3(p_in)}'),
        P(f'In a sample of {N}, estimate how many values lie between {a} and {b} {c[1]}.', str(round(N * p_in)), f'M1 {N} × {n3(p_in)}; A1 {round(N * p_in)}'),
        P(f'The largest {round(pp * 100)}% of values are classed as "large". Find the least value classed as large.', f'{n3(lim) if abs(lim) < 1000 else n4(lim)} {c[1]}', f'B1 z = {z3(z)}; M1 {mu} + {z3(z)} × {s}; A1 {n3(lim) if abs(lim) < 1000 else n4(lim)}'),
        P('State one assumption made in using this model.', 'the values are continuous and symmetrically distributed about the mean (normally distributed)', 'B1 valid assumption in context'),
    ]
    return cmp_(r, intro, parts)


n173.add('C4', (2, 3, 4, 5))(n173_c4)


n174 = T('Normal approximation to the binomial with continuity correction', 'normal approximation', 'continuity correction', 'binomial approximation')
n174.fixed('C1', (1, 2), [
    ('A normal approximation to B(n, p) is suitable when', 'np > 5 and n(1 − p) > 5', 'Both expected counts must be large enough.', ['n < 30', 'p > 0.5', 'np < 5']),
    ('Using a continuity correction, P(X ≤ 20) for a binomial X is approximated by', 'P(Y < 20.5)', 'Include the whole bar for 20.', ['P(Y < 19.5)', 'P(Y < 20)', 'P(Y > 20.5)']),
    ('Using a continuity correction, P(X > 15) for a binomial X is approximated by', 'P(Y > 15.5)', 'X > 15 means X ≥ 16, whose bar starts at 15.5.', ['P(Y > 14.5)', 'P(Y > 15)', 'P(Y < 15.5)']),
    ('If X ~ B(100, 0.4), the approximating normal distribution is', 'N(40, 24)', 'μ = np, σ² = np(1 − p).', ['N(40, 0.24)', 'N(40, 40)', 'N(60, 24)']),
    ('Using a continuity correction, P(X = 12) for a binomial X is approximated by', 'P(11.5 < Y < 12.5)', 'The bar for 12 runs from 11.5 to 12.5.', ['P(Y = 12)', 'P(Y < 12.5)', 'P(12 < Y < 13)']),
])
n174.fixed('C2', (2, 3), [
    ('Explain why a continuity correction is used when approximating a binomial distribution by a normal distribution.', 'The binomial is discrete and the normal is continuous; each integer value is represented by an interval of width 1 centred on it.', 'B1 discrete to continuous; B1 interval ± 0.5 [2]'),
    ('Explain why a normal approximation would not be suitable for B(20, 0.05).', 'np = 1, which is less than 5, so the distribution is very skewed and not close to normal.', 'B1 np = 1 < 5; B1 skewed [2]'),
])


def rapprox(r):
    for _ in range(20):
        n = r.choice([40, 50, 60, 80, 100, 120, 150, 200, 250, 300])
        p = Fr(r.choice([10, 15, 20, 25, 30, 35, 40, 45, 55, 60, 65, 70, 75, 80]), 100)
        if n * p > 5 and n * (1 - p) > 5:
            return n, p
    return 100, Fr(1, 2)


def cc(kind, k):
    """Continuity-corrected boundary and direction."""
    return {'le': (k + 0.5, '<'), 'lt': (k - 0.5, '<'), 'ge': (k - 0.5, '>'), 'gt': (k + 0.5, '>')}[kind]


SYM = {'le': '≤', 'lt': '<', 'ge': '≥', 'gt': '>'}


@n174.add('C1', (1, 2, 3))
def n174_c1(r, D):
    kind = r.choice(['le', 'lt', 'ge', 'gt'])
    k = r.randint(10, 80)
    b, d = cc(kind, k)
    wrong = [f'P(Y {d} {k})', f'P(Y {d} {nf(k - 0.5 if b > k else k + 0.5)})', f'P(Y {"<" if d == ">" else ">"} {nf(b)})']
    return MC(r, f'X ~ B(n, p) is approximated by Y, a normal random variable. Using a continuity correction, P(X {SYM[kind]} {k}) is approximated by', f'P(Y {d} {nf(b)})', wrong,
              f'X {SYM[kind]} {k} corresponds to Y {d} {nf(b)}.')


@n174.add('C1', (2, 3))
def n174_c1b(r, D):
    n, p = rapprox(r)
    m, v = n * p, n * p * (1 - p)
    return MC(r, f'X ~ B({n}, {dn(p)}). State the normal distribution used to approximate X.', f'N({dn(m)}, {dn(v)})', [f'N({dn(m)}, {dn(m)})', f'N({dn(m)}, {dn(p * (1 - p))})', f'N({dn(n * (1 - p))}, {dn(v)})' if p != Fr(1, 2) else f'N({dn(m)}, {n3(math.sqrt(v))})'],
              f'μ = np = {dn(m)}, σ² = np(1 − p) = {dn(v)}.')


@n174.add('C2', (2, 3, 4), 'explain')
def n174_err(r, D):
    n, p = rapprox(r)
    m, v = float(n * p), float(n * p * (1 - p))
    s = math.sqrt(v)
    k = int(m) + r.randint(1, max(2, int(s)))
    nm = person(r)
    right = 1 - Phi((k - 0.5 - m) / s)
    return Q(f'X ~ B({n}, {dn(p)}). {nm} approximates P(X ≥ {k}) by P(Y > {k}.5), where Y ~ N({dn(n * p)}, {dn(n * p * (1 - p))}). Explain the error and find the correct approximation.',
             f'X ≥ {k} includes {k}, whose interval is {k - 0.5} to {k + 0.5}, so use P(Y > {k - 0.5}) = {n3(right)}.',
             f'B1 continuity correction should be {k - 0.5}; M1 standardises ({k - 0.5} − {dn(n * p)})/√{dn(n * p * (1 - p))}; A1 {n3(right)}')


@n174.add('C2', (2, 3), 'explain')
def n174_just(r, D):
    n = r.choice([20, 30, 40, 50, 80, 100])
    p = Fr(r.choice([2, 5, 10, 15, 20, 40, 50, 70, 90, 95]), 100)
    ok = n * p > 5 and n * (1 - p) > 5
    return Q(f'Determine whether a normal approximation is suitable for X ~ B({n}, {dn(p)}), giving a reason.',
             f'np = {dn(n * p)} and n(1 − p) = {dn(n * (1 - p))}; ' + ('both exceed 5, so it is suitable' if ok else 'not both greater than 5, so it is not suitable'),
             'M1 calculates np and n(1 − p); A1 compares with 5 and concludes')


@n174.add('C3', (1, 2, 3, 4, 5), 'numerical')
def n174_calc(r, D):
    n, p = rapprox(r)
    m, v = float(n * p), float(n * p * (1 - p))
    s = math.sqrt(v)
    head = f'X ~ B({n}, {dn(p)}). Use a suitable approximation to find'
    if D <= 2:
        kind = r.choice(['le', 'lt'])
        k = int(m) + r.choice([-1, 1]) * r.randint(1, max(2, int(1.5 * s)))
        b, d = cc(kind, k)
        pr_ = Phi((b - m) / s)
        return Q(f'{head} P(X {SYM[kind]} {k}).', n3(pr_), f'B1 N({dn(n * p)}, {dn(n * p * (1 - p))}); M1 continuity correction {nf(b)}; M1 standardises; A1 {n3(pr_)}')
    if D == 3:
        kind = r.choice(['ge', 'gt'])
        k = int(m) + r.choice([-1, 1]) * r.randint(1, max(2, int(1.5 * s)))
        b, d = cc(kind, k)
        pr_ = 1 - Phi((b - m) / s)
        return Q(f'{head} P(X {SYM[kind]} {k}).', n3(pr_), f'B1 N({dn(n * p)}, {dn(n * p * (1 - p))}); M1 continuity correction {nf(b)}; M1 1 − Φ(z); A1 {n3(pr_)}')
    a = int(m) - r.randint(1, max(2, int(1.5 * s)))
    b = int(m) + r.randint(1, max(2, int(1.5 * s)))
    if D == 4:
        pr_ = Phi((b + 0.5 - m) / s) - Phi((a - 0.5 - m) / s)
        return Q(f'{head} P({a} ≤ X ≤ {b}).', n3(pr_), f'B1 mean and variance; M1 boundaries {a - 0.5} and {b + 0.5}; M1 standardises both; A1 {n3(pr_)}')
    pr_ = Phi((b - 0.5 - m) / s) - Phi((a + 0.5 - m) / s)
    return Q(f'{head} P({a} < X < {b}).', n3(pr_), f'B1 mean and variance; M1 boundaries {a + 0.5} and {b - 0.5}; M1 standardises both; A1 {n3(pr_)}')


@n174.add('C3', (2, 3, 4, 5), 'numerical')
def n174_ctx(r, D):
    n, p = rapprox(r)
    ctx = r.choice(BIN_CTX)
    pc = int(p * 100)
    m, v = float(n * p), float(n * p * (1 - p))
    s = math.sqrt(v)
    k = int(m) + r.choice([-1, 1]) * r.randint(1, max(2, int(1.5 * s)))
    side = r.choice(['fewer', 'more'])
    if side == 'fewer':
        pr_ = Phi((k - 0.5 - m) / s)
        b = k - 0.5
    else:
        pr_ = 1 - Phi((k + 0.5 - m) / s)
        b = k + 0.5
    return Q(f'{ctx[0].format(p=pc)}. A random sample of {n} {ctx[1]} is taken. Use a suitable approximation to find the probability that {side} than {k} {ctx[2]}.', n3(pr_),
             f'B1 N({dn(n * p)}, {dn(n * p * (1 - p))}); M1 continuity correction {nf(b)}; M1 standardises; A1 {n3(pr_)}')


def n174_c4(r, D):
    n, p = rapprox(r)
    m, v = float(n * p), float(n * p * (1 - p))
    s = math.sqrt(v)
    k = int(m) + r.randint(1, max(2, int(1.5 * s)))
    j = int(m) - r.randint(1, max(2, int(1.5 * s)))
    nm = person(r)
    intro = f'{nm} throws a biased coin {n} times. The probability of a head on each throw is {dn(p)}. X is the number of heads.'
    parts = [
        P('Show that a normal approximation is suitable.', f'np = {dn(n * p)} > 5 and n(1 − p) = {dn(n * (1 - p))} > 5', 'B1 both values found and compared with 5'),
        P('State the parameters of the approximating normal distribution.', f'N({dn(n * p)}, {dn(n * p * (1 - p))})', 'B1 mean; B1 variance'),
        P(f'Use the approximation to find P(X ≥ {k}).', n3(1 - Phi((k - 0.5 - m) / s)), f'M1 continuity correction {k - 0.5}; M1 standardises; A1 {n3(1 - Phi((k - 0.5 - m) / s))}'),
        P(f'Use the approximation to find P(X < {j}).', n3(Phi((j - 0.5 - m) / s)), f'M1 continuity correction {j - 0.5}; M1 standardises; A1 {n3(Phi((j - 0.5 - m) / s))}'),
    ]
    return cmp_(r, intro, parts)


n174.add('C4', (2, 3, 4, 5))(n174_c4)

CHAPTERS[17] = [n171, n172, n173, n174]


# ================================================================ finalise

_ASCII_MINUS = re.compile(r'(?<![\w)\]])-(?=\d)')


def _fixminus(t):
    return _ASCII_MINUS.sub(MINUS, t) if isinstance(t, str) else t


def _wrap(fn):
    def g(r, D):
        q = fn(r, D)
        if q:
            for f in ('stem', 'answer', 'key'):
                q[f] = _fixminus(q.get(f))
            if q.get('options'):
                q['options'] = [_fixminus(o) for o in q['options']]
        if q and 'marks' not in q and not q.get('options'):
            m = key_marks(q.get('key', ''))
            if m:
                q['marks'] = max(1, min(20, m))
                q['minutes'] = round(max(1.0, q['marks'] * 1.25) * 2) / 2
        return q
    g.__name__ = getattr(fn, '__name__', 'tpl')
    return g


def _finalise():
    for ts in CHAPTERS.values():
        for t in ts:
            for tp in t.templates:
                if not getattr(tp.fn, '_wrapped', False):
                    tp.fn = _wrap(tp.fn)
                    tp.fn._wrapped = True


_finalise()
