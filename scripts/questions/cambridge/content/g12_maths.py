"""Cambridge International A Level Mathematics 9709 (grade 12): Paper 3 Pure Mathematics 3 and
Paper 4 Mechanics (A2 content, staged route).

Chapters 1-11 follow Pure 3 (algebra, logarithms and exponentials, trigonometry, differentiation,
integration, numerical solution of equations, further algebra, further calculus, vectors,
differential equations, complex numbers); chapters 12-20 follow Mechanics (kinematics, forces and
Newton's laws, forces in two dimensions, friction, connected particles, general motion in a
straight line, momentum, work and energy, the work-energy principle and power).

Conventions: exact answers where the syllabus expects them, otherwise 3 significant figures
(angles in degrees to 1 d.p., or to 2 d.p. where the paper asks for it); g = 10 m s⁻² in
mechanics as on 9709 papers. Mark schemes use M (method), A (accuracy), B (independent) and
DM (dependent method) marks; item marks are read from the mark points in the key and written as
a trailing [n]. Computed answers are checked numerically inside the templates (quadrature,
numerical differentiation, Runge-Kutta, iteration); a template whose check fails returns None.
"""
import cmath
import math
import re
from fractions import Fraction as Fr

from ._lib import topic, mcq, compose, sf, person, two_people, city, sup
from .g11_maths import (num, n3, n4, d1, sg, pw, term, poly, quad, lin, br, sq, pt, rt, pi_frac, Q, MC, P, PF,
                        cmp_, T, nz, pn, key_marks, MINUS, ordn, ineq_in, ineq_out, sols, dlist, tl, exstr, surd)

PROFILE = {'mark_scale': {'long': (1.5, 1.5), 'case': (1.25, 1.25)}, 'wordy': False}
CHAPTERS = {}
CHECK_FAILS = []
G = 10


# ================================================================ checking helpers

def ok(a, b, tag='', tol=1e-6):
    """Record and report a failed numerical check (a template then returns None)."""
    try:
        good = abs(a - b) <= tol * max(1.0, abs(a), abs(b))
    except TypeError:
        good = False
    if not good:
        CHECK_FAILS.append((tag, a, b))
    return good


def simpson(f, a, b, n=2000):
    if n % 2:
        n += 1
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(a + i * h)
    return s * h / 3


def ndiff(f, x, h=1e-5):
    return (f(x + h) - f(x - h)) / (2 * h)


def rk4(f, x0, y0, x1, n=2000):
    h = (x1 - x0) / n
    x, y = x0, y0
    for _ in range(n):
        k1 = f(x, y)
        k2 = f(x + h / 2, y + h * k1 / 2)
        k3 = f(x + h / 2, y + h * k2 / 2)
        k4 = f(x + h, y + h * k3)
        y += h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        x += h
    return y


def bisect(f, a, b, it=200):
    fa = f(a)
    for _ in range(it):
        m = (a + b) / 2
        fm = f(m)
        if (fm < 0) == (fa < 0):
            a, fa = m, fm
        else:
            b = m
    return (a + b) / 2


# ================================================================ formatting helpers

def n2(x):
    """2 decimal places with unicode minus."""
    s = f'{abs(x):.2f}'
    return (MINUS if x < 0 and s != '0.00' else '') + s


def dp(x, k):
    s = f'{abs(x):.{k}f}'
    return (MINUS if x < 0 and float(s) != 0 else '') + s


def d2(x):
    """Angle in degrees to 2 d.p."""
    return dp(x, 2) + '°'


def fx(x):
    """Exact Fraction or 3 s.f. float."""
    if isinstance(x, (int, Fr)):
        return num(Fr(x))
    if abs(x - round(x)) < 1e-9:
        return num(int(round(x)))
    return n3(x)


def ex(a, b=0, v='x'):
    """e raised to (a v + b): e²ˣ, e⁻ˣ, e^(3x − 1), e^(x/2)."""
    a, b = Fr(a), Fr(b)
    if b == 0 and a.denominator == 1 and v == 'x':
        ai = int(a)
        return 'e' + ('' if ai == 1 else ('⁻' if ai == -1 else sup(ai))) + 'ˣ'
    if b == 0 and a.denominator == 1 and v == 't':
        ai = int(a)
        return 'e' + ('' if ai == 1 else ('⁻' if ai == -1 else sup(ai))) + 'ᵗ'
    if b == 0 and a.denominator != 1 and abs(a.numerator) == 1:
        return f'e^({MINUS if a < 0 else ""}{v}/{a.denominator})'
    return f'e^({lin(a, b, v)})'


def ek(k):
    """e to a constant power: e², e⁻¹, e^(1/2)."""
    k = Fr(k)
    if k == 1:
        return 'e'
    if k.denominator == 1:
        return 'e' + sup(int(k))
    return f'e^({num(k)})'


def coef(c, s):
    """c·s with 1 and −1 suppressed: 3 sin x, − sin x."""
    c = Fr(c)
    if c == 1:
        return s
    if c == -1:
        return MINUS + s
    return f'{num(c)}{s}' if not s[0].isalpha() or len(s) == 1 else f'{num(c)} {s}' if s[:3] in ('sin', 'cos', 'tan', 'sec', 'cot', 'cos', 'ln ') else f'{num(c)}{s}'


def addt(terms):
    """Join already-formatted signed terms: [('+', '3x'), ('−', 'sin x')]."""
    out = ''
    for c, s in terms:
        c = Fr(c)
        if c == 0:
            continue
        body = s if abs(c) == 1 and s else (f'{num(abs(c))}{s}' if s and (s[0].isalpha() and len(s) <= 2 or s[0] in 'e(√π') else (f'{num(abs(c))} {s}' if s else num(abs(c))))
        if not out:
            out = (MINUS if c < 0 else '') + body
        else:
            out += (' − ' if c < 0 else ' + ') + body
    return out or '0'


def frs(x):
    """Fraction in a/b form (always), for coefficients inside expressions."""
    return num(Fr(x))


def lnr(fr_):
    """ln of a positive Fraction, written ln(7/3) or ln 5."""
    fr_ = Fr(fr_)
    return f'ln {num(fr_)}' if fr_.denominator == 1 else f'ln({num(fr_)})'


def cf(c, s):
    """Coefficient times a symbol with a space: (1/2) ln 3, 2 ln 3, −ln 3."""
    c = Fr(c)
    if c == 0:
        return '0'
    if c == 1:
        return s
    if c == -1:
        return MINUS + s
    if c.denominator != 1:
        return (MINUS if c < 0 else '') + f'({num(abs(c))}){s}' if not s[0].isdigit() else (MINUS if c < 0 else '') + f'({num(abs(c))}) × {s}'
    return f'{num(c)}{s}' if s[0] in 'eπ√(' else f'{num(c)} {s}'


def plus(a, b):
    """'a + b' with b possibly negative text starting with −."""
    if b.startswith(MINUS):
        return f'{a} − {b[1:]}'
    return f'{a} + {b}'


def rnd_name(r):
    return person(r)


LEADS = ['', 'In an examination question, ', 'On a revision worksheet, ', 'In a homework task, ']


def lead(r):
    return r.choice(LEADS)


# ================================================================ polynomial helpers (coefficients highest power first)

def ptrim(p):
    p = [Fr(c) for c in p]
    while len(p) > 1 and p[0] == 0:
        p = p[1:]
    return p


def pmul(p, q):
    out = [Fr(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += Fr(a) * Fr(b)
    return out


def padd(p, q):
    n = max(len(p), len(q))
    p = [Fr(0)] * (n - len(p)) + [Fr(c) for c in p]
    q = [Fr(0)] * (n - len(q)) + [Fr(c) for c in q]
    return ptrim([a + b for a, b in zip(p, q)])


def pval(p, x):
    s = Fr(0) if not isinstance(x, float) else 0.0
    for c in p:
        s = s * x + c
    return s


def pdiv(p, d):
    p = [Fr(c) for c in p]
    d = [Fr(c) for c in d]
    q = []
    rem = p[:]
    while len(rem) >= len(d):
        c = rem[0] / d[0]
        q.append(c)
        for i in range(len(d)):
            rem[i] -= c * d[i]
        rem = rem[1:]
    return ptrim(q or [0]), ptrim(rem or [0])


def pstr(p, v='x'):
    p = ptrim(p)
    n = len(p) - 1
    return poly([(c, n - i) for i, c in enumerate(p)], v)


def lf(a, b, v='x'):
    """Linear factor (ax + b) with brackets."""
    return f'({lin(a, b, v)})'


def prod_lin(lead_, facs):
    """lead × Π (a x + b)."""
    p = [Fr(lead_)]
    for a, b in facs:
        p = pmul(p, [a, b])
    return p


def deriv_p(p):
    n = len(p) - 1
    return ptrim([c * (n - i) for i, c in enumerate(p[:-1])]) if n > 0 else [Fr(0)]


# ================================================================ vectors and complex numbers

def vstr(v, unit=('i', 'j', 'k')):
    out = ''
    for c, u in zip(v, unit):
        c = Fr(c)
        if c == 0:
            continue
        body = ('' if abs(c) == 1 else num(abs(c))) + u
        if not out:
            out = (MINUS if c < 0 else '') + body
        else:
            out += (' − ' if c < 0 else ' + ') + body
    return out or '0'


def vcol(v):
    return '(' + ', '.join(num(Fr(c)) for c in v) + ')'


def vadd(a, b):
    return [x + y for x, y in zip(a, b)]


def vsub(a, b):
    return [x - y for x, y in zip(a, b)]


def vmul(k, a):
    return [k * x for x in a]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def mag2(a):
    return sum(x * x for x in a)


def sqrt_str(n):
    """√n simplified, n a non-negative integer or Fraction."""
    n = Fr(n)
    if n.denominator != 1:
        # √(p/q) = √(pq)/q
        p, q = n.numerator, n.denominator
        o, i = surd(p * q)
        top = (str(o) if o > 1 or i == 1 else '') + (f'√{i}' if i > 1 else '')
        g = math.gcd(o, q)
        if i == 1:
            return num(Fr(o, q))
        o2, q2 = o // g, q // g
        top = (str(o2) if o2 > 1 else '') + f'√{i}'
        return top if q2 == 1 else f'{top}/{q2}'
    return rt(int(n)) if n > 0 else '0'


def cstr(a, b, v='i'):
    """a + bi with exact parts."""
    a, b = Fr(a), Fr(b)
    if b == 0:
        return num(a)
    bs = ('' if abs(b) == 1 else (num(abs(b)) if b.denominator == 1 else f'({num(abs(b))})')) + v
    if a == 0:
        return (MINUS if b < 0 else '') + bs
    return f'{num(a)} {"−" if b < 0 else "+"} {bs}'


def carg(a, b):
    return math.atan2(b, a)


def rad3(x):
    return n3(x)


# ================================================================ finalise wrapper

_ASCII_MINUS = re.compile(r'(?<![\w)\]])-(?=\d)')


def _fixminus(t):
    return _ASCII_MINUS.sub(MINUS, t) if isinstance(t, str) else t


def _wrap(fn):
    def g(r, D):
        try:
            q = fn(r, D)
        except (ZeroDivisionError, OverflowError, ValueError, IndexError):
            return None
        if not q:
            return None
        for f in ('stem', 'answer', 'key'):
            q[f] = _fixminus(q.get(f))
        if q.get('options'):
            q['options'] = [_fixminus(o) for o in q['options']]
            if len(set(o.lower() for o in q['options'])) != 4 or q['answer'] not in q['options']:
                return None
        elif not re.search(r'\[\d+\]', q.get('key', '')):
            m = key_marks(q.get('key', '')) or q.get('marks') or 0
            if m:
                q['key'] = q['key'].rstrip(' .;') + f' [{m}]'
                q['marks'] = max(1, min(20, m))
                q['minutes'] = round(max(1.0, q['marks'] * 1.25) * 2) / 2
        if 'marks' not in q and not q.get('options'):
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


def tsum(terms):
    """Signed sum of (coefficient, symbol) pairs: [(3, 'tan²θ'), (−1, 'sec θ'), (5, '')] -> '3tan²θ − sec θ + 5'.
    A space is put between a number and a symbol starting with a function name."""
    out = ''
    for c, s in terms:
        c = Fr(c) if not isinstance(c, float) else c
        if c == 0:
            continue
        a = abs(c)
        cs = num(a) if not isinstance(a, float) else num(a)
        if isinstance(a, Fr) and a.denominator != 1 and s:
            cs = f'({cs})'
        if s:
            body = s if a == 1 else (f'{cs} {s}' if re.match(r'(sin|cos|tan|sec|cosec|cot|ln)', s) and not s.endswith('²θ') else f'{cs}{s}')
        else:
            body = cs
        if not out:
            out = (MINUS if c < 0 else '') + body
        else:
            out += (' − ' if c < 0 else ' + ') + body
    return out or '0'


def sg3(x):
    """' + 0.368' / ' − 1.25' to 3 s.f.; '' if zero."""
    if abs(x) < 1e-12:
        return ''
    return (' − ' if x < 0 else ' + ') + sf(abs(x), 3)


def line3(m, c, v='x'):
    """y = mx + c with 3 s.f. coefficients."""
    if abs(m) < 1e-12:
        return f'y = {n3(c)}'
    return f'y = {n3(m)}{v}{sg3(c)}'


# ================================================================ exact values made of π, surds, logs and powers of e

def _xterm(c, kind, arg):
    """Unsigned text for |c| × symbol."""
    c = abs(Fr(c))
    if kind == 'r':
        return num(c)
    sym = {'pi': 'π', 'sq': f'√{arg}', 'ln': f'ln {arg}', 'e': ek(arg) if kind == 'e' else ''}[kind]
    if kind in ('pi', 'sq'):
        top = ('' if c.numerator == 1 else str(c.numerator)) + sym
        return top if c.denominator == 1 else f'{top}/{c.denominator}'
    if kind == 'ln':
        if c == 1:
            return sym
        return (f'{c.numerator} ' if c.denominator == 1 else f'({num(c)}) ') + sym
    # e-powers
    if c == 1:
        return sym
    return (str(c.numerator) if c.denominator == 1 else f'({num(c)})') + sym


def xval(parts):
    v = 0.0
    for c, kind, arg in parts:
        c = float(c)
        v += c * {'r': 1.0, 'pi': math.pi, 'sq': math.sqrt(arg) if kind == 'sq' else 0, 'ln': math.log(arg) if kind == 'ln' else 0, 'e': math.exp(float(arg)) if kind == 'e' else 0}[kind]
    return v


def xstr(parts):
    """parts: list of (coef, kind, arg) with kind in r, pi, sq, ln, e."""
    # merge like terms
    acc = {}
    order = []
    for c, kind, arg in parts:
        key = (kind, arg if kind != 'r' else None)
        if key not in acc:
            acc[key] = Fr(0)
            order.append(key)
        acc[key] += Fr(c)
    out = ''
    for key in order:
        c = acc[key]
        if c == 0:
            continue
        body = _xterm(c, key[0], key[1])
        if not out:
            out = (MINUS if c < 0 else '') + body
        else:
            out += (' − ' if c < 0 else ' + ') + body
    return out or '0'


_HENCE = re.compile(r'(\(a\) |(?<=\. ))Hence (\w)')


def cmp_(r, intro, parts, k=(2, 3, 4), type_='multi_step'):
    """compose() with 'Hence' removed from a part that ends up first."""
    q = compose(r, intro, parts, k=k, type_=type_)
    if q:
        q['stem'] = _HENCE.sub(lambda m: m.group(1) + m.group(2).upper(), q['stem'])
    return q


def lnco(c, arg):
    """c ln(arg) text: ln 3, −ln 3, 2 ln 3, (1/2) ln 3."""
    c = Fr(c)
    a = abs(c)
    body = f'ln{arg}' if arg.startswith('|') or arg.startswith('(') else f'ln {arg}'
    body = body if a == 1 else (f'{num(a)} {body}' if a.denominator == 1 else f'({num(a)}) {body}')
    return (MINUS if c < 0 else '') + body


# ================================================================ Chapter 1 Algebra

def absl(a, b, v='x'):
    return f'|{lin(a, b, v)}|'


def abs_eq_sols(a, b, c, d):
    """Solutions of |ax + b| = |cx + d|."""
    out = set()
    if a != c:
        out.add(Fr(d - b, a - c))
    if a != -c:
        out.add(Fr(-(b + d), a + c))
    return sorted(out)


def abs_lin_sols(a, b, m, c):
    """Solutions of |ax + b| = mx + c, with validity."""
    cand, out = [], []
    if a != m:
        cand.append(Fr(c - b, a - m))
    if a != -m:
        cand.append(Fr(-(b + c), a + m))
    for x in cand:
        if m * x + c >= 0 and abs(a * x + b) == m * x + c and x not in out:
            out.append(x)
    return sorted(out), cand


def xs_list(xs, v='x'):
    return ' or '.join(f'{v} = {num(x)}' for x in xs) if xs else 'no solutions'


m11 = T('The modulus function: graphs of y = ∣ax + b∣ and solving modulus equations and inequalities', 'modulus function', 'modulus equations')
m11.fixed('C1', (1, 2), [
    ('What is the value of |3 − 8|?', '5', '|3 − 8| = |−5| = 5.', ['−5', '11', '−11']),
    ('Which of these is the graph of y = |x| ?', 'a V shape with vertex at the origin', 'For x ≥ 0, y = x; for x < 0, y = −x, giving a V with vertex (0, 0).', ['a straight line through the origin with gradient 1', 'a U-shaped parabola through the origin', 'an inverted V with vertex at the origin']),
    ('For which values of x is |x| = −x ?', 'x ≤ 0', '|x| = −x exactly when x is zero or negative.', ['x ≥ 0', 'x = 0 only', 'no values of x']),
    ('How many solutions has the equation |x − 2| = −3 ?', '0', 'A modulus is never negative, so there are no solutions.', ['1', '2', 'infinitely many']),
    ('Which inequality is equivalent to |x| < 4 ?', '−4 < x < 4', '|x| < 4 means x lies within 4 of zero.', ['x < 4', 'x < −4 or x > 4', '0 < x < 4']),
])
m11.fixed('C2', (2, 3), [
    ('Explain why the equation |2x + 5| = −1 has no solutions.', 'The modulus of any real number is zero or positive, so |2x + 5| ≥ 0 and can never equal −1.', 'B1 |2x + 5| ≥ 0 for all x; B1 so cannot equal a negative number [2]'),
    ('Explain why squaring both sides is a valid method for solving |f(x)| = |g(x)| but may introduce extra solutions when solving |f(x)| = g(x).', 'Both sides of |f| = |g| are non-negative, so squaring is reversible. With |f(x)| = g(x), squaring also gives solutions of |f(x)| = −g(x), which must be rejected if g(x) < 0.', 'B1 both sides non-negative so squaring is reversible; B1 for |f| = g, solutions with g(x) < 0 must be rejected [2]'),
    ('Describe how the graph of y = |f(x)| is obtained from the graph of y = f(x).', 'Parts of the graph on or above the x-axis are unchanged; parts below the x-axis are reflected in the x-axis.', 'B1 parts above unchanged; B1 parts below reflected in the x-axis [2]'),
    ('Explain why |x − a| < b, where b > 0, can be written as a − b < x < a + b.', '|x − a| is the distance of x from a on the number line, so x is less than b away from a, i.e. between a − b and a + b.', 'B1 distance interpretation (or −b < x − a < b); B1 a − b < x < a + b [2]'),
])


@m11.add('C1', (1, 2, 3))
def m11_c1(r, D):
    if D == 1:
        a, b = nz(r, -9, 9), r.randint(1, 12)
        return MC(r, f'Solve the equation |x{sg(-a)}| = {b}.', f'x = {num(a - b)} or x = {num(a + b)}',
                  [f'x = {num(a + b)} only', f'x = {num(-a - b)} or x = {num(-a + b)}', f'x = {num(b - a)} only', f'x = {num(a - b)} only'],
                  f'x{sg(-a)} = ±{b}, so x = {num(a - b)} or {num(a + b)}.')
    a, b = r.randint(2, 6), nz(r, -9, 9)
    if D == 2:
        c = r.randint(1, 15)
        x1, x2 = Fr(-c - b, a), Fr(c - b, a)
        return MC(r, f'Solve the equation {absl(a, b)} = {c}.', f'x = {num(x1)} or x = {num(x2)}',
                  [f'x = {num(x2)} only', f'x = {num(Fr(c + b, a))} or x = {num(Fr(-c + b, a))}', f'x = {num(Fr(c - b, 1))} or x = {num(Fr(-c - b, 1))}', f'x = {num(x1)} only'],
                  f'{lin(a, b)} = ±{c}, so x = {num(x1)} or {num(x2)}.')
    c = r.randint(1, 15)
    lo, hi = Fr(-c - b, a), Fr(c - b, a)
    return MC(r, f'Which of the following is the solution of the inequality {absl(a, b)} < {c}?', ineq_in(lo, hi),
              [ineq_out(lo, hi), f'x < {num(hi)}', ineq_in(Fr(-c + b, a), Fr(c + b, a)), f'x > {num(lo)}'],
              f'−{c} < {lin(a, b)} < {c}, so {ineq_in(lo, hi)}.')


@m11.add('C2', (1, 2, 3, 4), 'explain')
def m11_err(r, D):
    nm = person(r)
    f = r.choice(['lower', 'invalid', 'vertex']) if D >= 2 else r.choice(['lower', 'vertex'])
    if f == 'lower':
        a, b, c = r.randint(1, 5), nz(r, -9, 9), r.randint(2, 14)
        lo, hi = Fr(-c - b, a), Fr(c - b, a)
        stem = f'{nm} solves the inequality {absl(a, b)} < {c} and writes the answer x < {num(hi)}. Explain what is wrong with this answer and give the correct solution.'
        return Q(stem, f'{nm} has only used {lin(a, b)} < {c} and ignored {lin(a, b)} > −{c}. Correct solution: {ineq_in(lo, hi)}.',
                 f'B1 must also have {lin(a, b)} > −{c} (or −{c} < {lin(a, b)} < {c}); B1 {ineq_in(lo, hi)}')
    if f == 'vertex':
        a, b = r.randint(2, 6), nz(r, -12, 12)
        if b % a == 0:
            b += 1
        stem = f'{nm} says that the graph of y = {absl(a, b)} has its vertex at ({num(b)}, 0). Explain why {nm} is wrong and state the coordinates of the vertex and of the point where the graph crosses the y-axis.'
        return Q(stem, f'The vertex is where {lin(a, b)} = 0, i.e. x = {num(Fr(-b, a))}, not x = {num(b)}. Vertex ({num(Fr(-b, a))}, 0); y-intercept (0, {abs(b)}).',
                 f'B1 vertex where {lin(a, b)} = 0, ({num(Fr(-b, a))}, 0); B1 (0, {abs(b)})')
    for _ in range(40):
        a, b, m, c = r.randint(1, 4), nz(r, -8, 8), r.choice([-3, -2, -1, 1, 2, 3]), nz(r, -9, 9)
        good, cand = abs_lin_sols(a, b, m, c)
        if len(cand) == 2 and len(good) == 1 and cand[0] != cand[1]:
            bad = [x for x in cand if x not in good][0]
            break
    else:
        return None
    rhs = lin(m, c)
    stem = f'{nm} solves the equation {absl(a, b)} = {rhs} by squaring both sides and obtains x = {num(cand[0])} and x = {num(cand[1])}. Explain why one of these values must be rejected, and state the solution.'
    return Q(stem, f'At x = {num(bad)} the right-hand side {rhs} = {num(m * bad + c)}, which is negative, but a modulus cannot be negative. Solution: x = {num(good[0])}.',
             f'M1 substitutes into {rhs} (or checks both sides); A1 x = {num(bad)} rejected since {rhs} < 0; B1 x = {num(good[0])} only' if D >= 3 else
             f'B1 x = {num(bad)} gives {rhs} < 0 so rejected; B1 x = {num(good[0])} only')


@m11.add('C3', (1, 2, 3, 4, 5), 'numerical')
def m11_solve(r, D):
    if D == 1:
        a, b, c = r.randint(2, 7), nz(r, -9, 9), r.randint(1, 15)
        x1, x2 = Fr(-c - b, a), Fr(c - b, a)
        return Q(f'Solve the equation {absl(a, b)} = {c}.', f'x = {num(x1)} or x = {num(x2)}', f'M1 {lin(a, b)} = ±{c}; A1 both values')
    if D == 2:
        a, b, c = r.randint(1, 6), nz(r, -9, 9), r.randint(1, 13)
        lo, hi = Fr(-c - b, a), Fr(c - b, a)
        s = r.choice(['<', '>', '≤', '≥'])
        ans = ineq_in(lo, hi, s == '<') if s in '<≤' else ineq_out(lo, hi, s == '>')
        return Q(f'Solve the inequality {absl(a, b)} {s} {c}.', ans, f'M1 critical values from {lin(a, b)} = ±{c}; A1 {num(lo)}, {num(hi)}; A1 {ans}')
    for _ in range(60):
        a, b, c, d = r.randint(1, 5), nz(r, -9, 9), r.randint(1, 5), nz(r, -9, 9)
        if a != c and (a, b) != (c, d) and len(abs_eq_sols(a, b, c, d)) == 2:
            break
    else:
        return None
    sol = abs_eq_sols(a, b, c, d)
    L, R = absl(a, b), absl(c, d)
    if D == 3:
        return Q(f'Solve the equation {L} = {R}.', xs_list(sol),
                 f'M1 squares both sides or forms {lin(a, b)} = ±({lin(c, d)}); A1 x = {num(sol[0])}; A1 x = {num(sol[1])}')
    if D == 4:
        s = r.choice(['<', '>'])
        inside = (a * a > c * c) == (s == '<')
        ans = ineq_in(sol[0], sol[1]) if inside else ineq_out(sol[0], sol[1])
        return Q(f'Solve the inequality {L} {s} {R}.', ans,
                 f'M1 squares to obtain a quadratic inequality (or solves the two linear equations); A1 critical values {num(sol[0])} and {num(sol[1])}; A1 {ans}')
    for _ in range(60):
        a, b, m, c = r.randint(1, 5), nz(r, -9, 9), r.choice([-2, -1, 1, 2, 3]), nz(r, -9, 9)
        good, cand = abs_lin_sols(a, b, m, c)
        if good and len(cand) == 2:
            break
    else:
        return None
    rej = [x for x in cand if x not in good]
    return Q(f'Solve the equation {absl(a, b)} = {lin(m, c)}.', xs_list(good),
             f'M1 forms {lin(a, b)} = {lin(m, c)} and {lin(a, b)} = −({lin(m, c)}); A1 candidate values {", ".join(num(x) for x in cand)}; M1 checks {lin(m, c)} ≥ 0; A1 '
             + xs_list(good) + (f' (x = {num(rej[0])} rejected)' if rej else ''))


def m11_c4(r, D):
    for _ in range(60):
        a, b, c, d = r.randint(1, 4), nz(r, -8, 8), r.randint(1, 4), nz(r, -8, 8)
        if a != c and len(abs_eq_sols(a, b, c, d)) == 2 and b % a:
            break
    else:
        return None
    sol = abs_eq_sols(a, b, c, d)
    s = r.choice(['<', '>'])
    inside = (a * a > c * c) == (s == '<')
    ans = ineq_in(sol[0], sol[1]) if inside else ineq_out(sol[0], sol[1])
    k = r.randint(1, 9)
    intro = f'The functions f and g are defined for all real x by f(x) = {absl(a, b)} and g(x) = {absl(c, d)}.'
    parts = [
        P('Sketch, on the same diagram, the graphs of y = f(x) and y = g(x), stating the coordinates of the points where each graph meets the axes.',
          f'V-shaped graphs: y = f(x) meets the axes at ({num(Fr(-b, a))}, 0) and (0, {abs(b)}); y = g(x) at ({num(Fr(-d, c))}, 0) and (0, {abs(d)}).',
          f'B1 V shape for f with vertex ({num(Fr(-b, a))}, 0) and (0, {abs(b)}); B1 V shape for g with vertex ({num(Fr(-d, c))}, 0) and (0, {abs(d)})'),
        P('Solve the equation f(x) = g(x).', xs_list(sol), f'M1 squares or uses ±; A1 x = {num(sol[0])}; A1 x = {num(sol[1])}'),
        P(f'Hence solve the inequality f(x) {s} g(x).', ans, f'B1 FT {ans} using the graphs or the quadratic'),
        P(f'State the number of solutions of the equation f(x) = {k}, giving a reason.', '2', f'B1 2, since the horizontal line y = {k} cuts the V-shaped graph twice ({k} > 0)'),
    ]
    good, cand = abs_lin_sols(a, b, 1, k)
    if good:
        parts.append(P(f'Solve the equation f(x) = x + {k}.', xs_list(good), f'M1 forms two linear equations; M1 rejects any value with x + {k} < 0; A1 {xs_list(good)}'))
    return cmp_(r, intro, parts)


m11.add('C4', (2, 3, 4, 5))(m11_c4)


# ---------------------------------------------------------------- 1.2 division, remainder theorem

def rcubic(r, lo=-6, hi=7):
    return [Fr(r.choice([1, 1, 2, 3])), Fr(nz(r, lo, hi, ())), Fr(nz(r, lo, hi, ())), Fr(nz(r, lo, hi))]


def divisor(a, b=1):
    """(b x − a) i.e. root a/b."""
    return f'({lin(b, -a)})'


m12 = T('Division of polynomials and the remainder theorem', 'remainder theorem', 'division of polynomials')
m12.fixed('C1', (1, 2), [
    ('When a polynomial p(x) is divided by (x − a), the remainder is', 'p(a)', 'Remainder theorem: p(x) = (x − a)q(x) + R, so R = p(a).', ['p(−a)', 'p(0)', 'a']),
    ('When a polynomial p(x) is divided by (2x + 1), the remainder is', 'p(−1/2)', 'Put 2x + 1 = 0: x = −1/2, so the remainder is p(−1/2).', ['p(1/2)', 'p(−1)', 'p(2)']),
    ('A cubic polynomial is divided by a quadratic. What is the greatest possible degree of the remainder?', '1', 'The remainder has degree less than the divisor, so at most 1 (linear).', ['0', '2', '3']),
    ('A quartic polynomial is divided by (x − 3). What is the degree of the quotient?', '3', 'Degree 4 − 1 = 3.', ['4', '2', '1']),
])
m12.fixed('C2', (2, 3), [
    ('Explain why the remainder when p(x) is divided by (x − a) is p(a).', 'p(x) = (x − a)q(x) + R for a quotient q(x) and constant R. Putting x = a makes the first term zero, so p(a) = R.', 'B1 p(x) = (x − a)q(x) + R; B1 substitute x = a gives R = p(a) [2]'),
    ('Explain why, when a polynomial is divided by (x − 1)(x + 2), the remainder can be written in the form px + q.', 'The remainder must have degree less than the degree of the divisor, which is 2, so it is at most linear: px + q.', 'B1 degree of remainder < degree of divisor; B1 divisor degree 2 so remainder linear [2]'),
    ('Explain how the remainder theorem can be used to find the remainder when p(x) is divided by (3x − 2) without long division.', 'Find the value of x making the divisor zero, x = 2/3, and evaluate p(2/3); this equals the remainder.', 'B1 x = 2/3 from 3x − 2 = 0; B1 remainder = p(2/3) [2]'),
])


@m12.add('C1', (1, 2, 3))
def m12_c1(r, D):
    p = rcubic(r)
    a = nz(r, -4, 4)
    if D <= 2:
        R = pval(p, a)
        return MC(r, f'Find the remainder when {pstr(p)} is divided by (x{sg(-a)}).', num(R),
                  [num(pval(p, -a)), num(p[-1]), num(R + 2 * a), num(-R)], f'Remainder = p({num(a)}) = {num(R)}.')
    b = r.choice([2, 3])
    a = r.choice([x for x in (-2, -1, 1, 2) if math.gcd(abs(x), b) == 1])
    R = pval(p, Fr(a, b))
    return MC(r, f'Find the remainder when {pstr(p)} is divided by {divisor(a, b)}.', num(R),
              [num(pval(p, Fr(-a, b))), num(pval(p, Fr(b, a))), num(pval(p, Fr(a))), num(-R)], f'Remainder = p({num(Fr(a, b))}) = {num(R)}.')


@m12.add('C2', (1, 2, 3, 4), 'explain')
def m12_err(r, D):
    nm = person(r)
    p = rcubic(r)
    a = nz(r, -5, 5)
    f = r.choice(['sign', 'frac', 'deg'] if D >= 3 else ['sign', 'deg'])
    if f == 'sign':
        stem = f'{nm} says that the remainder when p(x) = {pstr(p)} is divided by (x{sg(a)}) is p({num(a)}) = {num(pval(p, a))}. Explain the error and find the correct remainder.'
        return Q(stem, f'The divisor is zero when x = {num(-a)}, so the remainder is p({num(-a)}) = {num(pval(p, -a))}.',
                 f'B1 x{sg(a)} = 0 gives x = {num(-a)}; B1 remainder {num(pval(p, -a))}')
    if f == 'frac':
        b = r.choice([2, 3])
        a = r.choice([x for x in (-2, -1, 1, 2) if math.gcd(abs(x), b) == 1])
        stem = f'{nm} finds the remainder when {pstr(p)} is divided by {divisor(a, b)} by evaluating p({a}). Explain the error and find the correct remainder.'
        return Q(stem, f'The divisor {lin(b, -a)} is zero at x = {num(Fr(a, b))}, not x = {a}. Remainder = p({num(Fr(a, b))}) = {num(pval(p, Fr(a, b)))}.',
                 f'B1 uses x = {num(Fr(a, b))}; M1 substitutes; A1 {num(pval(p, Fr(a, b)))}')
    stem = f'{nm} divides p(x) = {pstr(p)} by (x² + 1) and says the remainder is the constant {num(p[-1] - p[1])}. Explain why the remainder could be linear, and find the correct remainder.'
    q, rem = pdiv(p, [1, 0, 1])
    return Q(stem, f'The divisor has degree 2, so the remainder has degree at most 1. p(x) = {plus(f'(x² + 1)({pstr(q)})', pstr(rem))}; remainder {pstr(rem)}.',
             f'B1 remainder degree < 2 so of the form px + q; B1 remainder {pstr(rem)}')


@m12.add('C3', (1, 2, 3, 4, 5), 'numerical')
def m12_calc(r, D):
    p = rcubic(r)
    a = nz(r, -4, 4)
    if D == 1:
        return Q(f'Find the remainder when {pstr(p)} is divided by (x{sg(-a)}).', num(pval(p, a)), f'M1 substitutes x = {num(a)}; A1 {num(pval(p, a))}')
    if D == 2:
        # unknown coefficient k in x term
        k = nz(r, -9, 9)
        p[2] = Fr(k)
        R = pval(p, a)
        sh = pstr([p[0], p[1], 0, 0]) + ' + kx' + sg(p[3])
        stem = f'When {sh} is divided by (x{sg(-a)}), the remainder is {num(R)}. Find the value of the constant k.'
        return Q(stem, f'k = {k}', f'M1 substitutes x = {num(a)} and equates to {num(R)}; A1 k = {k}')
    if D == 3:
        b = r.choice([1, 1, 2])
        aa = a if b == 1 else r.choice([-1, 1, 3, -3])
        q, rem = pdiv(p, [b, -aa])
        return Q(f'Find the quotient and remainder when {pstr(p)} is divided by {divisor(aa, b)}.', f'quotient {pstr(q)}, remainder {num(rem[0])}',
                 f'M1 long division (or equating coefficients) to a quadratic quotient; A1 quotient {pstr(q)}; A1 remainder {num(rem[0])}')
    if D == 4:
        A, B = nz(r, -6, 6), nz(r, -9, 9)
        c0 = nz(r, -8, 8)
        base = [Fr(r.choice([1, 2])), Fr(A), Fr(B), Fr(c0)]
        u, v = r.sample([x for x in range(-3, 4) if x], 2)
        R1, R2 = pval(base, u), pval(base, v)
        stem = (f'The polynomial p(x) = {pstr([base[0], 0, 0, 0])} + ax² + bx{sg(c0)}, where a and b are constants. When p(x) is divided by (x{sg(-u)}) the remainder is {num(R1)}, '
                f'and when p(x) is divided by (x{sg(-v)}) the remainder is {num(R2)}. Find the values of a and b.')
        return Q(stem, f'a = {A}, b = {B}', f'M1 p({u}) = {num(R1)}; M1 p({v}) = {num(R2)}; M1 solves simultaneous equations; A1 a = {A}; A1 b = {B}')
    quart = [Fr(1), Fr(nz(r, -5, 5, ())), Fr(nz(r, -6, 6, ())), Fr(nz(r, -9, 9, ())), Fr(nz(r, -9, 9, ()))]
    d = [Fr(1), Fr(nz(r, -3, 3, ())), Fr(nz(r, -4, 4))]
    q, rem = pdiv(quart, d)
    if len(rem) < 2 or rem[0] == 0:
        return None
    return Q(f'Find the quotient and remainder when {pstr(quart)} is divided by ({pstr(d)}).', f'quotient {pstr(q)}, remainder {pstr(rem)}',
             f'M1 division to a quadratic quotient; A1 quotient {pstr(q)}; M1 subtracts to find the remainder; A1 remainder {pstr(rem)}')


def m12_c4(r, D):
    for _ in range(50):
        A, B, C = nz(r, -6, 6), nz(r, -12, 12), nz(r, -12, 12)
        p = [Fr(2 if D >= 4 else 1), Fr(A), Fr(B), Fr(C)]
        u, v = r.sample([x for x in range(-3, 4) if x], 2)
        if pval(p, u) != 0 or True:
            break
    R1 = pval(p, u)
    R2 = pval(p, v)
    intro = (f'The polynomial p(x) is defined by p(x) = {num(p[0]) if p[0] != 1 else ""}x³ + ax² + bx{sg(C)}, where a and b are constants. '
             f'When p(x) is divided by (x{sg(-u)}) the remainder is {num(R1)}, and when p(x) is divided by (x{sg(-v)}) the remainder is {num(R2)}.')
    q, rem = pdiv(p, [1, 0, 1])
    w = r.choice([x for x in range(-3, 4) if x not in (u, v, 0)])
    parts = [
        P('Find the values of a and b.', f'a = {A}, b = {B}', f'M1 p({u}) = {num(R1)}; M1 p({v}) = {num(R2)}; M1 solves; A1 a = {A}, b = {B}'),
        P(f'Find the remainder when p(x) is divided by (x{sg(-w)}).', num(pval(p, w)), f'M1 p({w}); A1 {num(pval(p, w))}'),
        P('Find the quotient and remainder when p(x) is divided by (x² + 1).', f'quotient {pstr(q)}, remainder {pstr(rem)}', f'M1 division; A1 quotient {pstr(q)}; A1 remainder {pstr(rem)}'),
        P('Find the remainder when p(x) is divided by (2x − 1).', num(pval(p, Fr(1, 2))), f'M1 p(1/2); A1 {num(pval(p, Fr(1, 2)))}'),
    ]
    return cmp_(r, intro, parts, k=(2, 3, 4))


m12.add('C4', (2, 3, 4, 5))(m12_c4)


# ---------------------------------------------------------------- 1.3 factor theorem

def rroots(r, n=3, lo=-5, hi=5, distinct=True):
    while True:
        xs = [nz(r, lo, hi) for _ in range(n)]
        if not distinct or len(set(xs)) == n:
            return xs


def fac_str(facs, lead_=1):
    s = ''.join(lf(a, b) for a, b in facs)
    return (num(lead_) if lead_ != 1 else '') + s


def roots_fac(roots):
    """[(1, −a) ...] for integer roots, sorted."""
    return [(1, -x) for x in sorted(roots)]


m13 = T('The factor theorem and factorising cubic and quartic polynomials', 'factor theorem', 'factorising cubic and quartic')
m13.fixed('C1', (1, 2), [
    ('If p(3) = 0 for a polynomial p(x), which must be a factor of p(x)?', '(x − 3)', 'Factor theorem: p(a) = 0 ⇔ (x − a) is a factor.', ['(x + 3)', '(3x − 1)', '(3x + 1)']),
    ('Given that (2x − 1) is a factor of p(x), which statement is true?', 'p(1/2) = 0', '2x − 1 = 0 when x = 1/2.', ['p(−1/2) = 0', 'p(2) = 0', 'p(1) = 0']),
    ('Which value of x should be tested to show that (x + 4) is a factor of p(x)?', 'x = −4', 'x + 4 = 0 when x = −4.', ['x = 4', 'x = 1/4', 'x = 0']),
    ('A cubic polynomial with integer coefficients has leading coefficient 1 and constant term 6. Which could NOT be an integer root?', '4', 'Integer roots must divide the constant term 6.', ['−3', '2', '−6']),
])
m13.fixed('C2', (2, 3), [
    ('Explain why, if p(a) = 0, then (x − a) is a factor of p(x).', 'By the remainder theorem p(x) = (x − a)q(x) + p(a). If p(a) = 0 the remainder is zero, so (x − a) divides p(x) exactly.', 'B1 p(x) = (x − a)q(x) + p(a); B1 remainder zero so (x − a) is a factor [2]'),
    ('Explain why an integer root of x³ + bx² + cx + d = 0 (b, c, d integers) must be a factor of d.', 'If x = k is a root then k³ + bk² + ck = −d, so k(k² + bk + c) = −d and k divides d.', 'B1 rearranges to k(k² + bk + c) = −d; B1 so k divides d [2]'),
    ('Explain why a cubic polynomial with real coefficients must have at least one real linear factor.', 'A cubic tends to +∞ at one end and −∞ at the other, so its graph crosses the x-axis at least once; at that root a, (x − a) is a factor by the factor theorem.', 'B1 opposite end behaviour so crosses x-axis; B1 factor theorem gives linear factor [2]'),
])


@m13.add('C1', (1, 2, 3))
def m13_c1(r, D):
    roots = rroots(r)
    p = prod_lin(1, roots_fac(roots))
    if D == 3:
        b = r.choice([2, 3])
        a = r.choice([x for x in (-2, -1, 1, 2) if math.gcd(abs(x), b) == 1])
        p = prod_lin(1, [(b, -a)] + roots_fac(roots[:2]))
        cands = [f'({lin(b, a)})', f'({lin(a, b)})' if a != b else f'({lin(1, a)})', f'(x{sg(-a * b)})', f'(x{sg(a)})']
        cands = [c for c in cands if c != f'({lin(b, -a)})']
        return MC(r, f'Which of the following is a factor of {pstr(p)}?', f'({lin(b, -a)})', cands, f'p({num(Fr(a, b))}) = 0, so ({lin(b, -a)}) is a factor.')
    k = r.choice(roots)
    bad = [x for x in range(-6, 7) if pval(p, x) != 0 and x != 0]
    ds = [f'(x{sg(-x)})' for x in r.sample(bad, 3)]
    if -k not in roots and k != 0:
        ds[0] = f'(x{sg(k)})'
    return MC(r, f'Which of the following is a factor of p(x) = {pstr(p)}?', f'(x{sg(-k)})', ds, f'p({k}) = 0, so (x{sg(-k)}) is a factor by the factor theorem.')


@m13.add('C2', (1, 2, 3, 4), 'explain')
def m13_show(r, D):
    nm = person(r)
    roots = rroots(r)
    lead_ = r.choice([1, 1, 2])
    p = prod_lin(lead_, roots_fac(roots))
    k = r.choice(roots)
    f = r.choice(['show', 'wrong']) if -k not in roots else 'show'
    if f == 'show' or k == 0:
        terms = ' + '.join(f'({num(c)})({pn(k)})^{len(p) - 1 - i}' for i, c in enumerate(p[:-1]))
        stem = f'Show that (x{sg(-k)}) is a factor of {pstr(p)}' + (', and hence find the other two linear factors.' if D >= 3 else '.')
        q, _ = pdiv(p, [1, -k])
        other = [x for x in roots]
        other.remove(k)
        ans = f'p({num(k)}) = 0, so (x{sg(-k)}) is a factor' + (f'; other factors {lf(1, -other[0])}{lf(1, -other[1])}' + (f' (with factor {lead_})' if lead_ != 1 else '') if D >= 3 else '.')
        key = f'M1 substitutes x = {num(k)}; A1 p({num(k)}) = 0 with conclusion' + (f'; M1 divides to obtain {pstr(q)}; A1 {lf(1, -other[0])}{lf(1, -other[1])}' if D >= 3 else '')
        return Q(stem, ans, key)
    val = pval(p, -k)
    stem = f'{nm} finds that p({num(k)}) = 0 for p(x) = {pstr(p)}, and concludes that (x{sg(k)}) is a factor. Explain the error and state the correct factor.'
    return Q(stem, f'p({num(k)}) = 0 means x = {num(k)} is a root, so the factor is (x{sg(-k)}); (x{sg(k)}) would need p({num(-k)}) = 0, but p({num(-k)}) = {num(val)}.',
             f'B1 root x = {num(k)} gives factor (x{sg(-k)}); B1 p({num(-k)}) ≠ 0 or correct factor stated')


@m13.add('C3', (1, 2, 3, 4, 5), 'numerical')
def m13_calc(r, D):
    if D == 1:
        roots = rroots(r)
        p = prod_lin(1, roots_fac(roots))
        k = roots[0]
        c = p[2]
        shown = pstr([p[0], p[1], 0, 0]) + ' + ax' + sg(p[3])
        return Q(f'Given that (x{sg(-k)}) is a factor of {shown}, find the value of the constant a.', f'a = {num(c)}',
                 f'M1 substitutes x = {num(k)} and equates to 0; A1 a = {num(c)}')
    if D == 2:
        roots = rroots(r)
        lead_ = r.choice([1, 1, 2, 3])
        p = prod_lin(lead_, roots_fac(roots))
        k = roots[0]
        f = (num(lead_) if lead_ != 1 else '') + ''.join(lf(1, -x) for x in sorted(roots))
        return Q(f'Given that (x{sg(-k)}) is a factor of p(x) = {pstr(p)}, factorise p(x) completely.', f'p(x) = {f}',
                 f'M1 divides by (x{sg(-k)}) to obtain a quadratic; A1 correct quadratic factor; A1 {f}')
    if D == 3:
        b = r.choice([2, 3])
        a = r.choice([x for x in (-3, -1, 1, 3, 5) if math.gcd(abs(x), b) == 1])
        roots = rroots(r, 2)
        p = prod_lin(1, [(b, -a)] + roots_fac(roots))
        k = roots[0]
        f = lf(b, -a) + ''.join(lf(1, -x) for x in sorted(roots))
        return Q(f'Show that (x{sg(-k)}) is a factor of p(x) = {pstr(p)}. Hence factorise p(x) completely.', f'p({k}) = 0; p(x) = {f}',
                 f'B1 p({k}) = 0; M1 divides to obtain a quadratic; A1 quadratic factor; A1 {f}')
    if D == 4:
        roots = rroots(r, 4, -4, 4)
        p = prod_lin(1, roots_fac(roots))
        u, v = roots[0], roots[1]
        f = ''.join(lf(1, -x) for x in sorted(roots))
        return Q(f'The polynomial p(x) = {pstr(p)} has factors (x{sg(-u)}) and (x{sg(-v)}). Factorise p(x) completely.', f'p(x) = {f}',
                 f'M1 divides by (x{sg(-u)})(x{sg(-v)}) = {pstr(pmul([1, -u], [1, -v]))}; A1 quadratic quotient; M1 factorises the quotient; A1 {f}')
    roots = rroots(r)
    lead_ = r.choice([1, 2])
    p = prod_lin(lead_, roots_fac(roots))
    u, v = roots[0], roots[1]
    shown = (num(lead_) if lead_ != 1 else '') + 'x³ + ax² + bx' + sg(p[3])
    f = (num(lead_) if lead_ != 1 else '') + ''.join(lf(1, -x) for x in sorted(roots))
    return Q(f'The polynomial {shown}, where a and b are constants, has factors (x{sg(-u)}) and (x{sg(-v)}). Find the values of a and b and hence factorise the polynomial completely.',
             f'a = {num(p[1])}, b = {num(p[2])}; {f}', f'M1 p({u}) = 0; M1 p({v}) = 0; A1 a = {num(p[1])}; A1 b = {num(p[2])}; B1 {f}')


def m13_c4(r, D):
    roots = rroots(r)
    lead_ = r.choice([1, 2]) if D >= 4 else 1
    p = prod_lin(lead_, roots_fac(roots))
    u = roots[0]
    w = r.choice([x for x in range(-4, 5) if x and x not in roots])
    R = pval(p, w)
    shown = (num(lead_) if lead_ != 1 else '') + 'x³ + ax² + bx' + sg(p[3])
    f = (num(lead_) if lead_ != 1 else '') + ''.join(lf(1, -x) for x in sorted(roots))
    intro = f'The polynomial p(x) = {shown}, where a and b are constants. It is given that (x{sg(-u)}) is a factor of p(x), and that when p(x) is divided by (x{sg(-w)}) the remainder is {num(R)}.'
    rs = sorted(roots)
    parts = [
        P('Find the values of a and b.', f'a = {num(p[1])}, b = {num(p[2])}', f'M1 p({u}) = 0; M1 p({w}) = {num(R)}; M1 solves; A1 a = {num(p[1])}, b = {num(p[2])}'),
        P('Hence factorise p(x) completely.', f, f'M1 divides by (x{sg(-u)}); A1 {f}'),
        P('Solve the equation p(x) = 0.', ', '.join(f'x = {x}' for x in rs), 'B1 FT all three roots'),
        P('Solve the inequality p(x) < 0.', f'x < {rs[0]} or {rs[1]} < x < {rs[2]}', f'M1 uses sign of p between roots (positive leading coefficient); A1 x < {rs[0]} or {rs[1]} < x < {rs[2]}'),
    ]
    return cmp_(r, intro, parts)


m13.add('C4', (2, 3, 4, 5))(m13_c4)


# ---------------------------------------------------------------- 1.4 solving polynomial equations, sketching

def quad_roots_str(b, c):
    """Roots of x² + bx + c = 0 as exact text (real), or None."""
    disc = b * b - 4 * c
    if disc < 0:
        return None
    o, i = surd(disc) if disc > 0 else (0, 1)
    if i == 1:
        return [num(Fr(-b - o, 2)), num(Fr(-b + o, 2))]
    g = math.gcd(math.gcd(abs(b), o), 2)
    if g == 2:
        cb, co, den = -b // 2, o // 2, 1
    else:
        cb, co, den = -b, o, 2
    s = f'√{i}' if co == 1 else f'{co}√{i}'
    if den == 1:
        base = f'{num(cb)} ± {s}' if cb else f'±{s}'
        return [base]
    return [f'({num(cb)} ± {s})/2' if cb else f'±{s}/2']


m14 = T('Solving polynomial equations and sketching polynomial graphs', 'solving polynomial equations', 'sketching polynomial graphs')
m14.fixed('C1', (1, 2), [
    ('The graph of y = (x − 2)²(x + 1) meets the x-axis at x = 2. What happens there?', 'The curve touches the x-axis', 'A repeated factor (x − 2)² gives a repeated root, where the curve touches the axis.', ['The curve crosses the x-axis', 'The curve has an asymptote', 'The curve has a point of inflection on the axis at x = −1']),
    ('For large positive x, the curve y = −2x³ + 5x² + 1 behaves like', 'y → −∞', 'The leading term −2x³ dominates.', ['y → +∞', 'y → 0', 'y → 1']),
    ('What is the y-intercept of y = (x − 3)(x + 2)(2x − 1)?', '6', 'Put x = 0: (−3)(2)(−1) = 6.', ['−6', '3', '−3']),
    ('How many real roots does (x − 1)(x² + 4) = 0 have?', '1', 'x² + 4 = 0 has no real roots, so only x = 1.', ['3', '2', '0']),
])
m14.fixed('C2', (2, 3), [
    ('Explain how the sign of the leading coefficient of a cubic determines the shape of its graph for large |x|.', 'For large |x| the term ax³ dominates. If a > 0 the curve goes from bottom-left to top-right; if a < 0 it goes from top-left to bottom-right.', 'B1 leading term dominates; B1 correct description for a > 0 and a < 0 [2]'),
    ('Explain why the graph of y = (x + 1)²(x − 4) touches the x-axis at x = −1 but crosses it at x = 4.', '(x + 1)² does not change sign either side of x = −1, so y keeps the same sign and the curve touches; (x − 4) changes sign at x = 4, so the curve crosses.', 'B1 squared factor does not change sign; B1 single factor changes sign [2]'),
    ('Explain why a cubic equation with real coefficients can have exactly one, two or three distinct real roots but not zero.', 'A cubic has opposite signs for large positive and large negative x, so its continuous graph crosses the axis at least once; it can have at most three roots.', 'B1 opposite end behaviour so at least one root; B1 at most three roots [2]'),
])


@m14.add('C1', (1, 2, 3))
def m14_c1(r, D):
    a, b, c = rroots(r, 3, -6, 6)
    lead_ = r.choice([1, -1, 2])
    p = prod_lin(lead_, [(1, -a), (1, -b), (1, -c)])
    f = (MINUS if lead_ == -1 else (num(lead_) if lead_ != 1 else '')) + lf(1, -a) + lf(1, -b) + lf(1, -c)
    if D == 1:
        return MC(r, f'Where does the curve y = {f} cross the y-axis?', f'(0, {num(p[3])})', [f'(0, {num(-p[3])})', f'(0, {num(a * b * c)})' if lead_ != 1 else f'(0, {num(a + b + c)})', f'(0, {num(lead_)})', f'({num(p[3])}, 0)'],
                  f'Put x = 0: y = {num(p[3])}.')
    if D == 2:
        rs = sorted({a, b, c})
        return MC(r, f'Find the x-coordinates of the points where the curve y = {f} meets the x-axis.', ', '.join(num(x) for x in rs),
                  [', '.join(num(-x) for x in sorted(rs, reverse=True)), ', '.join(num(x) for x in sorted([a, -b, c])), ', '.join(num(x) for x in sorted([-a, b, -c])), ', '.join(num(x) for x in sorted([a * lead_, b, c]))],
                  'Each factor equal to zero gives a root.')
    p = prod_lin(1, [(1, -a), (1, -a), (1, -b)])
    rs = sorted([a, b])
    return MC(r, f'How many distinct real roots has the equation {pstr(p)} = 0, given that it can be written as (x{sg(-a)})²(x{sg(-b)}) = 0?', '2',
              ['3', '1', '0'], f'Roots x = {num(a)} (repeated) and x = {num(b)}: two distinct roots.') if a != b else None


@m14.add('C2', (1, 2, 3, 4), 'explain')
def m14_err(r, D):
    nm = person(r)
    a, b, c = rroots(r, 3, -6, 6)
    f = r.choice(['divide', 'end', 'touch'])
    if f == 'divide':
        p = prod_lin(1, [(1, 0), (1, -a), (1, -b)]) if a and b else None
        if not p:
            return None
        stem = f'{nm} solves {pstr(p)} = 0 by dividing every term by x and solving the resulting quadratic, obtaining x = {num(min(a, b))} and x = {num(max(a, b))}. Explain what is wrong and give all the solutions.'
        return Q(stem, f'Dividing by x loses the solution x = 0 (x is a factor). Solutions: x = 0, {num(min(a, b))}, {num(max(a, b))}.',
                 'B1 dividing by x loses the root x = 0 (factorise instead); B1 all three solutions')
    if f == 'end':
        stem = f'{nm} sketches y = {MINUS}{lf(1, -a)}{lf(1, -b)}{lf(1, -c)} starting at the bottom left and finishing at the top right. Explain the error.'
        return Q(stem, 'The leading coefficient is negative (−x³), so y → +∞ as x → −∞ and y → −∞ as x → +∞; the curve goes from top left to bottom right.',
                 'B1 leading term −x³; B1 correct end behaviour described')
    p = prod_lin(1, [(1, -a), (1, -a), (1, -b)])
    if a == b:
        return None
    stem = f'{nm} says the graph of y = {pstr(p)} crosses the x-axis at three points. Given that y = (x{sg(-a)})²(x{sg(-b)}), explain why {nm} is wrong and describe what happens at each point where the graph meets the x-axis.'
    return Q(stem, f'(x{sg(-a)})² is a repeated factor: the curve touches the x-axis at ({num(a)}, 0) and crosses it at ({num(b)}, 0); it meets the axis at only two points.',
             f'B1 repeated root at x = {num(a)}, touches; B1 crosses at x = {num(b)}; only two points')


@m14.add('C3', (1, 2, 3, 4, 5), 'numerical')
def m14_calc(r, D):
    if D <= 2:
        roots = rroots(r)
        p = prod_lin(1, roots_fac(roots))
        k = roots[0]
        rs = sorted(roots)
        return Q(f'Given that x = {k} is a root of the equation {pstr(p)} = 0, find the other roots.' if D == 2 else f'Solve the equation {pstr(p)} = 0, given that x = {k} is one root.',
                 ', '.join(f'x = {x}' for x in rs), f'M1 divides by (x{sg(-k)}); A1 quadratic factor; A1 remaining roots')
    k = nz(r, -4, 4)
    for _ in range(40):
        b, c = nz(r, -6, 6, ()), nz(r, -9, 9)
        disc = b * b - 4 * c
        if disc > 0 and surd(disc)[1] > 1:
            break
    else:
        return None
    p = pmul([1, -k], [1, b, c])
    rs = quad_roots_str(b, c)
    if D == 3:
        return Q(f'Show that x = {k} is a root of {pstr(p)} = 0, and find the other two roots in exact form.', f'x = {k}; x = {rs[0]}',
                 f'B1 p({k}) = 0; M1 divides to obtain {pstr([1, b, c])}; M1 quadratic formula; A1 x = {rs[0]}')
    if D == 4:
        lead_ = r.choice([2, 3])
        p2 = pmul([lead_, -lead_ * k + 1], [1, b, c])
        rr = Fr(lead_ * k - 1, lead_)
        return Q(f'Show that x = {num(rr)} is a root of the equation {pstr(p2)} = 0. Hence solve the equation completely, giving the other roots in exact form.',
                 f'x = {num(rr)}; x = {rs[0]}', f'B1 p({num(rr)}) = 0; M1 divides by ({lin(lead_, -lead_ * k + 1)}); A1 {pstr([1, b, c])}; A1 x = {rs[0]}')
    roots = rroots(r)
    a_, b_, c_ = sorted(roots)
    p = prod_lin(1, roots_fac(roots))
    return Q(f'Solve the inequality {pstr(p)} > 0, given that x = {roots[1]} is a root of {pstr(p)} = 0.', f'{a_} < x < {b_} or x > {c_}',
             f'M1 factorises completely; A1 roots {a_}, {b_}, {c_}; M1 sign diagram or sketch; A1 {a_} < x < {b_} or x > {c_}')


def m14_c4(r, D):
    roots = rroots(r, 3, -5, 5)
    p = prod_lin(1, roots_fac(roots))
    k = roots[0]
    rs = sorted(roots)
    m = nz(r, -3, 3)
    intro = f'The curve C has equation y = {pstr(p)}.'
    parts = [
        P(f'Show that (x{sg(-k)}) is a factor of {pstr(p)}.', f'p({k}) = 0', f'M1 substitutes x = {k}; A1 = 0 shown'),
        P('Find the coordinates of the points where C meets the x-axis.', ', '.join(f'({x}, 0)' for x in rs), 'M1 divides and factorises; A1 all three points'),
        P('State the coordinates of the point where C meets the y-axis.', f'(0, {num(p[3])})', f'B1 (0, {num(p[3])})'),
        P('Sketch C, showing the behaviour for large |x|.', f'Positive cubic through ({rs[0]}, 0), ({rs[1]}, 0), ({rs[2]}, 0) and (0, {num(p[3])}), rising from bottom left to top right.',
          'B1 correct cubic shape (positive leading coefficient); B1 intercepts marked'),
        P('Solve the inequality y ≤ 0.', f'x ≤ {rs[0]} or {rs[1]} ≤ x ≤ {rs[2]}', f'B1 FT x ≤ {rs[0]} or {rs[1]} ≤ x ≤ {rs[2]}'),
    ]
    return cmp_(r, intro, parts, k=(2, 3, 4))


m14.add('C4', (2, 3, 4, 5))(m14_c4)

CHAPTERS[1] = [m11, m12, m13, m14]


# ================================================================ Chapter 2 Logarithmic and exponential functions

SUB = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')


def lg(b):
    return 'log' + str(b).translate(SUB)


def pq(i, j, op='+'):
    return f'{"" if i == 1 else i}p {op} {"" if j == 1 else j}q'


def rpow(b, k):
    return Fr(b) ** k


def factor_pairs(n):
    return [(d, n // d) for d in range(1, int(math.isqrt(n)) + 1) if n % d == 0]


l21 = T('Logarithms and the laws of logarithms', 'laws of logarithms', 'logarithms')
l21.fixed('C1', (1, 2), [
    ('Which of these is equal to log₃ 81?', '4', '3⁴ = 81.', ['27', '3', '1/4']),
    ('Which statement is a law of logarithms?', 'logₐ x + logₐ y = logₐ(xy)', 'Adding logs of the same base gives the log of the product.', ['logₐ x + logₐ y = logₐ(x + y)', 'logₐ x × logₐ y = logₐ(xy)', 'logₐ x − logₐ y = logₐ x / logₐ y']),
    ('Write y = 5ˣ in logarithmic form.', 'x = log₅ y', 'aˣ = y ⇔ x = logₐ y.', ['y = log₅ x', 'x = log_y 5', '5 = logₓ y']),
    ('What is the value of logₐ 1, for any base a > 0, a ≠ 1?', '0', 'a⁰ = 1.', ['1', 'a', 'undefined']),
    ('Which of these is equal to 3 log 2 − log 4?', 'log 2', '3 log 2 − log 4 = log 8 − log 4 = log 2.', ['log 2 − 1', 'log 4', 'log(3/2)']),
])
l21.fixed('C2', (2, 3), [
    ('Explain why log₁₀(−5) is not defined for real numbers.', '10ˣ > 0 for every real x, so no real power of 10 equals −5.', 'B1 10ˣ is always positive; B1 so no real x gives −5 [2]'),
    ('Explain why logₐ(xy) = logₐ x + logₐ y, using the laws of indices.', 'Let x = aᵖ and y = a^q. Then xy = a^(p + q), so logₐ(xy) = p + q = logₐ x + logₐ y.', 'B1 writes x = aᵖ, y = a^q; B1 uses aᵖ × a^q = a^(p + q) [2]'),
    ('Explain why logₐ a = 1 and logₐ(1/a) = −1.', 'a¹ = a so logₐ a = 1; a⁻¹ = 1/a so logₐ(1/a) = −1.', 'B1 a¹ = a; B1 a⁻¹ = 1/a [2]'),
])


@l21.add('C1', (1, 2, 3))
def l21_c1(r, D):
    b = r.choice([2, 3, 4, 5, 10])
    if D == 1:
        k = r.choice([x for x in range(-3, 6) if x != 0 and abs(b ** abs(x)) <= 100000])
        v = Fr(b) ** k
        return MC(r, f'Find the value of {lg(b)} {num(v) if v.denominator == 1 else "(" + num(v) + ")"}.', num(k), [num(-k), num(k + 1), num(Fr(1, k)) if k not in (1, -1) else num(k * b), num(v / b)],
                  f'{b}{sup(k)} = {num(v)}, so the logarithm is {k}.')
    if D == 2:
        while True:
            x, y = r.randint(2, 12), r.randint(2, 12)
            z = r.choice([d for d in range(2, 10) if (x * y) % d == 0])
            if x * y // z > 1:
                break
        return MC(r, f'Express log {x} + log {y} − log {z} as a single logarithm.', f'log {x * y // z}',
                  [f'log {x + y - z}', f'log {num(Fr(x * y, 1) - z)}', f'log {num(Fr(x, y * z))}' if Fr(x, y * z).denominator > 1 else f'log {x * y * z}', f'log {x * y * z}'],
                  f'log {x} + log {y} = log {x * y}; subtract log {z}: log({x * y}/{z}) = log {x * y // z}.')
    i, j = r.randint(1, 3), r.randint(1, 3)
    n = 2 ** i * 3 ** j
    return MC(r, f'Given that logₐ 2 = p and logₐ 3 = q, express logₐ {n} in terms of p and q.', f'{"" if i == 1 else i}p + {"" if j == 1 else j}q',
              [f'{"" if j == 1 else j}p + {"" if i == 1 else i}q' if i != j else f'{i + 1}p + {j}q', f'{i * j}pq', f'{"" if i == 1 else i}p − {"" if j == 1 else j}q', f'p{sup(i)} + q{sup(j)}'],
              f'{n} = 2{sup(i)} × 3{sup(j)}, so logₐ {n} = {pq(i, j)}.')


@l21.add('C2', (1, 2, 3, 4), 'explain')
def l21_err(r, D):
    nm = person(r)
    f = r.choice(['sum', 'quot', 'pow'])
    b = r.choice([2, 3, 10])
    if f == 'sum':
        i, j = r.sample([1, 2, 3, 4], 2)
        x, y = b ** i, b ** j
        stem = f'{nm} writes {lg(b)} {x} + {lg(b)} {y} = {lg(b)} {x + y}. Explain the error and find the correct value of {lg(b)} {x} + {lg(b)} {y}.'
        return Q(stem, f'Adding logarithms multiplies the numbers: {lg(b)} {x} + {lg(b)} {y} = {lg(b)} {x * y} = {i + j}, not {lg(b)} {x + y}.',
                 f'B1 log x + log y = log(xy), not log(x + y); B1 {lg(b)} {x * y} = {i + j}')
    if f == 'quot':
        k = r.randint(2, 9)
        m = r.choice([2, 3, 4, 5])
        stem = f'{nm} writes log {k * m} − log {m} = (log {k * m})/(log {m}). Explain the error and simplify log {k * m} − log {m} correctly.'
        return Q(stem, f'Subtracting logarithms gives the log of the quotient: log {k * m} − log {m} = log({k * m}/{m}) = log {k}. It is not a quotient of logarithms.',
                 f'B1 log a − log b = log(a/b); B1 log {k}')
    n, k = r.randint(2, 5), r.randint(2, 9)
    stem = f'{nm} writes {n} log x = log({n}x) and so solves {n} log x = log {k ** n} by putting {n}x = {k ** n}. Explain the error and solve the equation correctly.'
    return Q(stem, f'n log x = log(xⁿ), not log(nx). So log x{sup(n)} = log {k ** n}, x{sup(n)} = {k ** n}, x = {k}.',
             f'B1 {n} log x = log x{sup(n)}; B1 x = {k}')


@l21.add('C3', (1, 2, 3, 4, 5), 'numerical')
def l21_calc(r, D):
    if D == 1:
        b = r.choice([2, 3, 5])
        k = r.randint(2, 4)
        m = r.randint(2, 9)
        stem = f'Without using a calculator, find the value of {lg(b)} {m * b ** k} − {lg(b)} {m}.'
        return Q(stem, str(k), f'M1 {lg(b)}({m * b ** k}/{m}) = {lg(b)} {b ** k}; A1 {k}')
    if D == 2:
        b = r.choice([2, 3, 5, 10])
        n = r.randint(1, 4 if b < 10 else 3)
        p, q = r.randint(2, 7), nz(r, -9, 9)
        x = Fr(b ** n - q, p)
        if x <= 0 or p * x + q <= 0:
            return None
        return Q(f'Solve the equation {lg(b)}({lin(p, q)}) = {n}.', f'x = {num(x)}', f'M1 {lin(p, q)} = {b}{sup(n)}; A1 x = {num(x)}')
    if D == 3:
        b = r.choice([2, 3, 2, 10])
        n = r.randint(3, 6) if b == 2 else (r.randint(2, 4) if b == 3 else 2)
        N = b ** n
        prs = [(d, e) for d, e in factor_pairs(N) if e > d]
        if not prs:
            return None
        x0, x1 = r.choice(prs)
        k = x1 - x0
        stem = f'Solve the equation {lg(b)} x + {lg(b)}(x + {k}) = {n}.'
        return Q(stem, f'x = {x0}', f'M1 {lg(b)}(x(x + {k})) = {n}; M1 x² + {k}x − {N} = 0; A1 x = {x0}; A1 rejects x = {-x1} (log of negative)')
    if D == 4:
        for _ in range(60):
            m = r.randint(2, 9)
            x1 = r.randint(m + 1, m + 12)
            x2 = m - x1
            if (-x1 * x2) % m == 0:
                k = -x1 * x2 // m
                if k > 0:
                    break
        else:
            return None
        base = r.choice(['log', 'ln', lg(r.choice([2, 3, 5]))])
        stem = f'Solve the equation 2 {base} x − {base}(x + {k}) = {base} {m}.'
        return Q(stem, f'x = {x1}', f'M1 {base}(x²/(x + {k})) = {base} {m}; M1 x² − {m}x − {m * k} = 0; A1 x = {x1}; A1 rejects x = {num(x2)}')
    b = r.choice([2, 3, 5])
    c = 3 * r.randint(1, 3)
    k = Fr(2 * c, 3)
    stem = f'Solve the equation {lg(b)} x + {lg(b * b)} x = {c}.'
    return Q(stem, f'x = {num(Fr(b) ** int(k))}', f'M1 {lg(b * b)} x = ({lg(b)} x)/{lg(b)} {b * b} = (1/2){lg(b)} x; A1 (3/2){lg(b)} x = {c}; M1 {lg(b)} x = {num(k)}; A1 x = {num(Fr(b) ** int(k))}')


def l21_c4(r, D):
    b = r.choice([2, 3, 5, 10])
    i, j = r.randint(1, 3), r.randint(1, 3)
    n = 2 ** i * 3 ** j
    m = r.randint(2, 4)
    x0, x1 = r.choice([(d, e) for d, e in factor_pairs(b ** m) if e > d] or [(1, b ** m)])
    k = x1 - x0
    intro = f'It is given that {lg(b)} 2 = p and {lg(b)} 3 = q.'
    parts = [
        P(f'Express {lg(b)} {n} in terms of p and q.', f'{pq(i, j)}', f'M1 {n} = 2{sup(i)} × 3{sup(j)}; A1 {pq(i, j)}'),
        P(f'Express {lg(b)}({num(Fr(2 ** i, 3 ** j))}) in terms of p and q.', f'{pq(i, j, '−')}', f'B1 {pq(i, j, '−')}'),
        P(f'Express {lg(b)}({b * 6}) in terms of p and q.', 'p + q + 1', f'M1 {lg(b)} {b} = 1; A1 p + q + 1'),
        P(f'Solve the equation {lg(b)} x + {lg(b)}(x + {k}) = {m}.', f'x = {x0}', f'M1 combines logs; M1 x² + {k}x − {b ** m} = 0; A1 x = {x0} only'),
    ]
    return cmp_(r, intro, parts)


l21.add('C4', (2, 3, 4, 5))(l21_c4)


# ---------------------------------------------------------------- 2.2 e^x and ln x

l22 = T('The exponential function eˣ and natural logarithm ln x', 'exponential function', 'natural logarithm')
l22.fixed('C1', (1, 2), [
    ('What is the value of ln e?', '1', 'ln is the logarithm to base e and e¹ = e.', ['0', 'e', '10']),
    ('Which equation is the asymptote of y = eˣ − 3?', 'y = −3', 'eˣ → 0 as x → −∞, so y → −3.', ['x = −3', 'y = 3', 'y = 0']),
    ('Which function is the inverse of f(x) = eˣ?', 'f⁻¹(x) = ln x', 'ln and exp are inverse functions.', ['f⁻¹(x) = e⁻ˣ', 'f⁻¹(x) = 1/eˣ', 'f⁻¹(x) = log₁₀ x']),
    ('Where does y = ln x cross the x-axis?', '(1, 0)', 'ln 1 = 0.', ['(0, 0)', '(e, 0)', '(0, 1)']),
    ('Simplify e^(3 ln 2).', '8', 'e^(3 ln 2) = e^(ln 8) = 8.', ['6', '9', '3 ln 2']),
])
l22.fixed('C2', (2, 3), [
    ('Explain why the graphs of y = eˣ and y = ln x are reflections of each other in the line y = x.', 'They are inverse functions: if b = eᵃ then a = ln b, so (a, b) on one graph corresponds to (b, a) on the other.', 'B1 inverse functions; B1 coordinates swap so reflection in y = x [2]'),
    ('Explain why the equation eˣ = −2 has no real solution.', 'eˣ > 0 for all real x, so it can never equal a negative number.', 'B1 eˣ > 0; B1 so no solution [2]'),
    ('Explain why e^(2x) − 5eˣ + 6 = 0 can be solved as a quadratic equation.', 'e^(2x) = (eˣ)², so with u = eˣ the equation is u² − 5u + 6 = 0, a quadratic in u.', 'B1 e^(2x) = (eˣ)²; B1 substitution u = eˣ gives a quadratic [2]'),
])


@l22.add('C1', (1, 2, 3))
def l22_c1(r, D):
    if D == 1:
        k = nz(r, -6, 9)
        f = r.choice(['ln', 'e'])
        if f == 'ln':
            return MC(r, f'Simplify ln({ek(k)}).', num(k), [ek(k), num(-k), f'{num(k)}e'], f'ln and e cancel: ln({ek(k)}) = {num(k)}.')
        k = r.randint(2, 15)
        return MC(r, f'Simplify e^(ln {k}).', str(k), [f'ln {k}', f'e{sup(k)}', f'{k}e'], f'e^(ln {k}) = {k}.')
    if D == 2:
        k = r.randint(2, 20)
        f = r.choice(['ex', 'ln'])
        if f == 'ex':
            return MC(r, f'Solve eˣ = {k}, giving the answer in exact form.', f'x = ln {k}', [f'x = e{sup(k)}', f'x = {k}/e', f'x = log {k}'], f'Take natural logarithms: x = ln {k}.')
        return MC(r, f'Solve ln x = {k}, giving the answer in exact form.', f'x = e{sup(k)}', [f'x = ln {k}', f'x = {k}e', f'x = 10{sup(k)}'], f'x = e{sup(k)}.')
    c = nz(r, -6, 6)
    a = r.choice([1, -1, 2, -2])
    return MC(r, f'State the equation of the asymptote and the y-intercept of y = {ex(a)}{sg(c)}.', f'y = {num(c)}; (0, {num(1 + c)})',
              [f'x = {num(c)}; (0, {num(1 + c)})', f'y = {num(c)}; (0, {num(c)})', f'y = {num(-c)}; (0, {num(1 - c)})', f'y = 0; (0, {num(1 + c)})'],
              f'{ex(a)} → 0 so y → {num(c)}; at x = 0, y = 1{sg(c)} = {num(1 + c)}.')


@l22.add('C2', (1, 2, 3, 4), 'explain')
def l22_err(r, D):
    nm = person(r)
    f = r.choice(['div', 'sq', 'neg'])
    if f == 'div':
        a, k = r.randint(2, 5), r.randint(3, 20)
        stem = f'{nm} solves {ex(a)} = {k} and writes x = ln({k}/{a}). Explain the error and give the correct solution in exact form.'
        return Q(stem, f'Taking ln of both sides gives {a}x = ln {k}, so x = (ln {k})/{a} = {n3(math.log(k) / a)}; ln({k}/{a}) = ln {k} − ln {a} is different.',
                 f'B1 {a}x = ln {k}; B1 x = (1/{a}) ln {k}')
    if f == 'sq':
        k = r.randint(2, 6)
        stem = f'{nm} writes ln(x²) = (ln x)² and so solves ln(x²) = {2 * k} by putting ln x = √{2 * k}. Explain the error and solve the equation for x > 0.'
        return Q(stem, f'ln(x²) = 2 ln x, not (ln x)². So 2 ln x = {2 * k}, ln x = {k}, x = e{sup(k)}.', f'B1 ln(x²) = 2 ln x; B1 x = e{sup(k)}')
    p, q = r.randint(1, 6), r.randint(1, 6)
    if p == q:
        return None
    stem = f'{nm} solves e^(2x) + {p + q}eˣ + {p * q} = 0 by factorising to (eˣ + {p})(eˣ + {q}) = 0 and writes x = ln({MINUS}{p}) or x = ln({MINUS}{q}). Explain why the equation has no real solutions.'
    return Q(stem, f'eˣ > 0 for all real x, so eˣ = −{p} and eˣ = −{q} are impossible; ln of a negative number is undefined. Hence there are no real solutions.',
             'B1 eˣ > 0 always; B1 so neither factor can be zero: no real solutions')


@l22.add('C3', (1, 2, 3, 4, 5), 'numerical')
def l22_calc(r, D):
    if D == 1:
        a, b, c = nz(r, -4, 4), nz(r, -5, 5), r.randint(2, 30)
        x = (math.log(c) - b) / a
        return Q(f'Solve the equation e^({lin(a, b)}) = {c}, giving your answer correct to 3 significant figures.', f'x = {n3(x)}',
                 f'M1 {lin(a, b)} = ln {c}; A1 x = {n3(x)}')
    if D == 2:
        a, b, c = r.randint(2, 6), nz(r, -9, 9), Fr(r.randint(1, 8), r.choice([1, 2]))
        x = (math.exp(c) - b) / a
        if a * x + b <= 0:
            return None
        return Q(f'Solve the equation ln({lin(a, b)}) = {num(c)}, giving your answer correct to 3 significant figures.', f'x = {n3(x)}',
                 f'M1 {lin(a, b)} = {ek(c)}; A1 x = {n3(x)}')
    if D == 3:
        p, q = r.sample(range(1, 10), 2)
        if r.random() < 0.4:
            q = -q
        s, pr = p + q, p * q
        mid = '' if s == 0 else (' − ' if s > 0 else ' + ') + ('' if abs(s) == 1 else str(abs(s))) + 'eˣ'
        stem = f'Solve the equation e^(2x){mid}{sg(pr)} = 0, giving your answers in exact form.'
        roots = [x for x in (p, q) if x > 0]
        ans = ' or '.join(f'x = ln {x}' if x != 1 else 'x = 0' for x in sorted(roots))
        return Q(stem, ans, f'M1 {pstr([1, -s, pr], "u")} = 0 with u = eˣ; A1 u = {p}, {q}; A1 {ans}' + ('' if len(roots) == 2 else f' (eˣ = {min(p, q)} rejected)'))
    if D == 4:
        for _ in range(60):
            x0 = r.randint(1, 9)
            a, b = r.randint(1, 8), r.randint(1, 8)
            c = (x0 + a) * (x0 + b)
            # other root of (x + a)(x + b) = c
            other = -(a + b) - x0
            if a != b:
                break
        stem = f'Solve the equation ln(x + {a}) + ln(x + {b}) = ln {c}.'
        return Q(stem, f'x = {x0}', f'M1 ln((x + {a})(x + {b})) = ln {c}; M1 {pstr([1, a + b, a * b - c])} = 0; A1 x = {x0}; A1 rejects x = {other}')
    p = r.randint(2, 9)
    s = r.randint(1, 9)
    m, k = 3 * p - s, p * s
    stem = f'Solve the equation 3eˣ − {k}e⁻ˣ = {m}, giving your answer in exact form.' if m > 0 else (f'Solve the equation 3eˣ − {k}e⁻ˣ + {-m} = 0, giving your answer in exact form.' if m < 0 else None)
    if not stem:
        return None
    return Q(stem, f'x = ln {p}', f'M1 multiplies by eˣ: 3u² {"−" if m >= 0 else "+"} {abs(m)}u − {k} = 0; M1 solves; A1 u = {p} (u = {num(Fr(-s, 3))} rejected); A1 x = ln {p}')


def l22_c4(r, D):
    A = r.choice([200, 250, 400, 500, 800, 1200])
    k = Fr(r.randint(2, 9), r.choice([10, 20, 50]))
    grow = r.random() < 0.5
    ctx = r.choice([('the number of bacteria in a culture', 'hours'), ('the number of fish in a lake', 'years'), ('the value of an investment, in dollars', 'years'), ('the number of users of a new app', 'weeks')] if grow else
                   [('the mass, in grams, of a radioactive substance', 'days'), ('the number of fish in a polluted lake', 'years'), ('the concentration, in mg per litre, of a drug in the blood', 'hours'), ('the temperature excess, in °C, of a cooling liquid above room temperature', 'minutes')])
    sgn = 1 if grow else -1
    t1 = r.randint(2, 6)
    N1 = A * math.exp(sgn * float(k) * t1)
    target = A * (r.choice([2, 3, 5]) if grow else r.choice([Fr(1, 2), Fr(1, 4), Fr(1, 5)]))
    tt = math.log(float(target) / A) / (sgn * float(k))
    intro = f'A model for {ctx[0]} is N = {A}e^({MINUS if not grow else ""}{num(float(k))}t), where t is the time in {ctx[1]}.'
    parts = [
        P('State the value of N when t = 0.', str(A), f'B1 {A}'),
        P(f'Find the value of N when t = {t1}.', n3(N1), f'M1 substitutes t = {t1}; A1 {n3(N1)}'),
        P(f'Find the value of t when N = {num(float(target))}.', n3(tt), f'M1 {num(Fr(target, A))} = e^({MINUS if not grow else ""}{num(float(k))}t); M1 takes ln; A1 t = {n3(tt)}'),
        P('Describe what happens to N in the long term according to this model.', 'N increases without limit' if grow else 'N decreases towards 0',
          'B1 increases without limit (exponential growth)' if grow else 'B1 N → 0 (but never reaches 0)'),
    ]
    return cmp_(r, intro, parts)


l22.add('C4', (2, 3, 4, 5))(l22_c4)


# ---------------------------------------------------------------- 2.3 a^x = b

l23 = T('Solving equations and inequalities of the form aˣ = b using logarithms', 'equations and inequalities of the form', 'using logarithms')
l23.fixed('C1', (1, 2), [
    ('Which expression gives the solution of 3ˣ = 7?', 'x = ln 7 / ln 3', 'Take logs: x ln 3 = ln 7.', ['x = ln(7/3)', 'x = 7/3', 'x = ln 3 / ln 7']),
    ('When solving 0.6ⁿ < 0.01 by taking logarithms, what happens to the inequality sign when dividing by ln 0.6?', 'It reverses, because ln 0.6 < 0', 'Dividing by a negative number reverses an inequality.', ['It stays the same', 'It reverses, because ln 0.6 > 0', 'It becomes an equals sign']),
    ('Solve 2ˣ = 1/8.', 'x = −3', '1/8 = 2⁻³.', ['x = 3', 'x = −1/3', 'x = 1/3']),
])
l23.fixed('C2', (2, 3), [
    ('Explain why taking logarithms is needed to solve 5ˣ = 12 but not to solve 5ˣ = 125.', '125 = 5³, so the second can be solved by matching powers; 12 is not an integer power of 5, so the unknown index must be brought down using logarithms.', 'B1 125 is a power of 5; B1 12 is not, so logs are needed to bring down x [2]'),
    ('Explain why the inequality sign reverses when solving (1/2)ⁿ < 0.001 using logarithms.', 'n ln(1/2) < ln 0.001; ln(1/2) is negative, so dividing by it reverses the inequality: n > ln 0.001 / ln 0.5.', 'B1 ln(1/2) < 0; B1 dividing by a negative reverses the inequality [2]'),
])


@l23.add('C1', (1, 2, 3))
def l23_c1(r, D):
    if D == 1:
        b = r.choice([2, 3, 4, 5])
        k = nz(r, -4, 6)
        v = Fr(b) ** k
        return MC(r, f'Solve the equation {b}ˣ = {num(v)}.', f'x = {k}', [f'x = {-k}', f'x = {num(v / b)}', f'x = {num(Fr(1, k)) if abs(k) > 1 else k + 1}'], f'{num(v)} = {b}{sup(k)}.')
    if D == 2:
        a, b = r.randint(2, 9), r.randint(2, 60)
        if math.log(b) % math.log(a) < 1e-9:
            return None
        x = math.log(b) / math.log(a)
        return MC(r, f'Solve {a}ˣ = {b}, giving x correct to 3 significant figures.', n3(x), [n3(math.log(b / a)), n3(b / a), n3(math.log(a) / math.log(b))], f'x = ln {b} / ln {a} = {n3(x)}.')
    a, b = r.sample([2, 3, 5, 7], 2)
    c = r.randint(1, 3)
    # a^x = b^(x - c) -> x ln a = (x - c) ln b -> x = -c ln b / (ln a - ln b) = c ln b /(ln b - ln a)
    x = c * math.log(b) / (math.log(b) - math.log(a))
    return MC(r, f'Solve {a}ˣ = {b}^(x − {c}), giving x correct to 3 significant figures.', n3(x),
              [n3(-x), n3(c * math.log(a) / (math.log(b) - math.log(a))), n3(c * math.log(b) / (math.log(b) + math.log(a)))], f'x ln {a} = (x − {c}) ln {b}, so x = {'' if c == 1 else str(c) + ' '}ln {b}/(ln {b} − ln {a}) = {n3(x)}.')


@l23.add('C2', (1, 2, 3, 4), 'explain')
def l23_err(r, D):
    nm = person(r)
    f = r.choice(['sign', 'div'])
    if f == 'sign':
        q = Fr(r.randint(5, 9), 10)
        e = r.choice([Fr(1, 100), Fr(1, 20), Fr(1, 10), Fr(1, 50)])
        bound = math.log(e) / math.log(q)
        n0 = math.floor(bound) + 1
        stem = f'{nm} solves {num(float(q))}ⁿ < {num(float(e))} by taking logarithms and writes n < ln {num(float(e))} / ln {num(float(q))} = {n3(bound)}. Explain the error and find the smallest integer n satisfying the inequality.'
        return Q(stem, f'ln {num(float(q))} is negative, so dividing by it reverses the inequality: n > {n3(bound)}. Smallest integer n = {n0}.',
                 f'B1 ln {num(float(q))} < 0 so the sign reverses; B1 n = {n0}')
    a = r.randint(2, 6)
    m = r.randint(2, 6)
    v = r.randint(2, 40) * a
    x = math.log(v / a) / math.log(m)
    stem = f'{nm} solves {a} × {m}ˣ = {v} by writing {a * m}ˣ = {v}. Explain the error and solve the equation correctly, giving x to 3 significant figures.'
    return Q(stem, f'{a} × {m}ˣ is not ({a} × {m})ˣ; divide first: {m}ˣ = {v // a}, x = ln {v // a} / ln {m} = {n3(x)}.',
             f'B1 must divide by {a} first (only {m} is raised to the power x); M1 x = ln {v // a}/ln {m}; A1 {n3(x)}')


@l23.add('C3', (1, 2, 3, 4, 5), 'numerical')
def l23_calc(r, D):
    if D == 1:
        a, b = r.randint(2, 9), r.randint(2, 99)
        if abs(math.log(b) / math.log(a) - round(math.log(b) / math.log(a))) < 1e-9:
            return None
        return Q(f'Solve the equation {a}ˣ = {b}, giving your answer correct to 3 significant figures.', f'x = {n3(math.log(b) / math.log(a))}', f'M1 x ln {a} = ln {b}; A1 {n3(math.log(b) / math.log(a))}')
    if D == 2:
        a, p, q, b = r.randint(2, 7), r.randint(2, 4), nz(r, -3, 3), r.randint(5, 90)
        x = (math.log(b) / math.log(a) - q) / p
        return Q(f'Solve the equation {a}^({lin(p, q)}) = {b}, giving your answer correct to 3 significant figures.', f'x = {n3(x)}', f'M1 ({lin(p, q)}) ln {a} = ln {b}; A1 x = {n3(x)}')
    if D == 3:
        a, b = r.sample([2, 3, 5, 6, 7], 2)
        c = r.randint(1, 3)
        x = c * math.log(b) / (math.log(a) - math.log(b))
        return Q(f'Solve the equation {a}ˣ = {b}^(x + {c}), giving your answer correct to 3 significant figures.', f'x = {n3(x)}',
                 f'M1 x ln {a} = (x + {c}) ln {b}; M1 collects x terms; A1 x = {n3(x)}')
    if D == 4:
        a = r.choice([2, 3, 5])
        p, q = r.sample([x for x in range(2, 12) if abs(math.log(x) / math.log(a) - round(math.log(x) / math.log(a))) > 1e-9] + [a], 2)
        xs = sorted(math.log(v) / math.log(a) for v in (p, q))
        return Q(f'Solve the equation {a}^(2x) − {p + q}({a}ˣ) + {p * q} = 0, giving your answers correct to 3 significant figures where appropriate.',
                 ' or '.join(f'x = {n3(x)}' if abs(x - round(x)) > 1e-9 else f'x = {round(x)}' for x in xs),
                 f'M1 quadratic in u = {a}ˣ: u² − {p + q}u + {p * q} = 0; A1 u = {p}, {q}; M1 x = ln u / ln {a}; A1 both values')
    f = r.choice(['decay', 'growth'])
    if f == 'decay':
        P0 = r.choice([5000, 8000, 12000, 20000, 25000])
        d = r.choice([8, 10, 12, 15, 18, 20])
        lim = r.choice([1000, 1500, 2000, 2500])
        if lim >= P0:
            return None
        q = 1 - d / 100
        n = math.floor(math.log(lim / P0) / math.log(q)) + 1
        ok(P0 * q ** n < lim and P0 * q ** (n - 1) >= lim, True, 'l23 decay')
        thing = r.choice(['car', 'machine', 'laptop fleet', 'tractor'])
        stem = f'A {thing} bought for ${P0} loses {d}% of its value each year. Find the smallest whole number of years after which its value is less than ${lim}.'
        return Q(stem, f'{n} years', f'M1 {P0} × {num(q)}ⁿ < {lim}; M1 takes logs; M1 reverses inequality on dividing by ln {num(q)}; A1 n > {n3(math.log(lim / P0) / math.log(q))}; A1 {n} years')
    P0 = r.choice([1000, 2000, 5000, 10000])
    i = r.choice([2, 3, 4, 5, 6])
    k = r.choice([2, 3, Fr(3, 2)])
    n = math.floor(math.log(float(k)) / math.log(1 + i / 100)) + 1
    stem = f'{person(r)} invests ${P0} in an account paying {i}% compound interest per year. Find the smallest number of complete years after which the investment is worth more than ${num(P0 * k)}.'
    return Q(stem, f'{n} years', f'M1 {P0} × {num(1 + i / 100)}ⁿ > {num(P0 * k)}; M1 takes logs; A1 n > {n3(math.log(float(k)) / math.log(1 + i / 100))}; A1 {n} years')


def l23_c4(r, D):
    a, b = r.sample([2, 3, 5, 7], 2)
    c = r.randint(1, 3)
    x3 = c * math.log(b) / (math.log(a) - math.log(b))
    q = Fr(r.randint(6, 9), 10)
    e = r.choice([Fr(1, 100), Fr(1, 20), Fr(1, 10)])
    n0 = math.floor(math.log(e) / math.log(q)) + 1
    p_, q_ = r.sample(range(2, 10), 2)
    xs = sorted(math.log(v) / math.log(a) for v in (p_, q_))
    intro = 'Use logarithms to answer the following, giving non-exact answers correct to 3 significant figures.'
    parts = [
        P(f'Solve the equation {a}ˣ = {b}^(x + {c}).', f'x = {n3(x3)}', f'M1 x ln {a} = (x + {c}) ln {b}; A1 {n3(x3)}'),
        P(f'Find the smallest integer n such that {num(float(q))}ⁿ < {num(float(e))}.', f'n = {n0}', f'M1 n ln {num(float(q))} < ln {num(float(e))}; M1 sign reverses; A1 n = {n0}'),
        P(f'Solve the equation {a}^(2x) − {p_ + q_}({a}ˣ) + {p_ * q_} = 0.', ' or '.join(f'x = {n3(x)}' for x in xs), f'M1 quadratic in {a}ˣ; A1 {a}ˣ = {p_}, {q_}; A1 both x values'),
    ]
    return cmp_(r, intro, parts, k=(2, 3))


l23.add('C4', (2, 3, 4, 5))(l23_c4)


# ---------------------------------------------------------------- 2.4 reduction to linear form

l24 = T('Using logarithms to reduce relationships to linear form', 'reduce relationships to linear form', 'linear form')
l24.fixed('C1', (1, 2), [
    ('Variables x and y satisfy y = kxⁿ. Which graph is a straight line?', 'ln y against ln x', 'ln y = ln k + n ln x.', ['ln y against x', 'y against ln x', 'y against xⁿ⁻¹']),
    ('Variables x and y satisfy y = A bˣ. Which graph is a straight line?', 'ln y against x', 'ln y = ln A + x ln b.', ['ln y against ln x', 'y against ln x', 'ln y against 1/x']),
    ('For y = kxⁿ, the graph of ln y against ln x has gradient', 'n', 'ln y = n ln x + ln k.', ['k', 'ln k', 'ln n']),
    ('For y = Ae^(bx), the graph of ln y against x has intercept on the vertical axis equal to', 'ln A', 'ln y = ln A + bx.', ['A', 'b', 'e^A']),
])
l24.fixed('C2', (2, 3), [
    ('Explain why plotting ln y against ln x is useful for testing whether data fit a model y = kxⁿ.', 'Taking logs gives ln y = n ln x + ln k, which is of the form Y = mX + c; if the points lie close to a straight line the model fits, and n and k can be read from the gradient and intercept.', 'B1 ln y = n ln x + ln k is linear in ln x; B1 straight line confirms model, gradient n and intercept ln k [2]'),
    ('Explain how to tell, from the graph of ln y against x, whether y = Abˣ describes growth or decay.', 'ln y = ln A + x ln b. If the gradient ln b is positive then b > 1 (growth); if negative then 0 < b < 1 (decay).', 'B1 gradient = ln b; B1 positive gives growth, negative gives decay [2]'),
])


def l24_line(r):
    """Return model data: kind, k (or A), n (or b), two points (X1, Y1), (X2, Y2) rounded to 2 d.p."""
    kind = r.choice(['power', 'exp', 'base'])
    if kind == 'power':
        n = r.choice([Fr(x, 10) for x in range(-25, 31, 5) if x != 0] + [Fr(3, 2), Fr(-1, 2), Fr(2, 3)])
        k = round(r.uniform(1.5, 12), 1)
    elif kind == 'exp':
        n = Fr(r.choice([-12, -8, -5, -3, 3, 4, 6, 9]), 10)
        k = round(r.uniform(2, 40), 1)
    else:
        n = r.choice([1.5, 2, 2.5, 3, 0.5, 0.8, 1.2])
        k = round(r.uniform(2, 20), 1)
    X1, X2 = round(r.uniform(0.2, 1.5), 2), round(r.uniform(2.5, 4.5), 2)
    if kind == 'base':
        Y = lambda X: math.log(k) + X * math.log(n)
    else:
        Y = lambda X: math.log(k) + float(n) * X
    return kind, k, n, (X1, round(Y(X1), 2)), (X2, round(Y(X2), 2))


def l24_solve(kind, P1, P2):
    m = (P2[1] - P1[1]) / (P2[0] - P1[0])
    c = P1[1] - m * P1[0]
    if kind == 'base':
        return math.exp(c), math.exp(m), m, c
    return math.exp(c), m, m, c


L24_TXT = {'power': ('y = kxⁿ', 'ln y', 'ln x', 'k and n'), 'exp': ('y = Ae^(bx)', 'ln y', 'x', 'A and b'), 'base': ('y = Abˣ', 'ln y', 'x', 'A and b')}


@l24.add('C1', (1, 2, 3))
def l24_c1(r, D):
    if D <= 2:
        m = r.choice([Fr(x, 2) for x in range(-7, 8) if x not in (0, 2, -2)]) if D == 2 else r.choice([-3, -2, 2, 3, 4, 5])
        c = r.choice([x / 10 for x in range(3, 30) if x % 10])
        E = lambda v: n3(math.exp(v))
        xp = lambda v: ('x' + sup(int(v)) if v != 1 else 'x') if Fr(v).denominator == 1 else f'x^({num(v)})'
        kind = r.choice(['power', 'exp'])
        if kind == 'power':
            return MC(r, f'The graph of ln y against ln x is a straight line with gradient {num(m)} and intercept {num(c)} on the ln y axis. Which equation relates x and y?',
                      f'y = {E(c)}{xp(m)}', [f'y = {num(c)}{xp(m)}', f'y = {E(-c)}{xp(m)}', f'y = {E(c)}{ex(m)}', f'y = {E(c)}{xp(-m)}'], f'ln y = {num(m) if Fr(m).denominator == 1 else "(" + num(m) + ")"} ln x + {num(c)}, so y = e^{num(c)} × {xp(m)} = {E(c)}{xp(m)}.')
        return MC(r, f'The graph of ln y against x is a straight line with gradient {num(m)} and intercept {num(c)} on the ln y axis. Which equation relates x and y?',
                  f'y = {E(c)}{ex(m)}', [f'y = {num(c)}{ex(m)}', f'y = {E(c)}{xp(m)}', f'y = {E(-c)}{ex(m)}', f'y = {E(c)}{ex(-m)}'], f'ln y = {lin(m, 0)} + {num(c)}, so y = e^{num(c)} × {ex(m)} = {E(c)}{ex(m)}.')
    kind, k, n, P1, P2 = l24_line(r)
    mod, Yn, Xn, _ = L24_TXT[kind]
    grad = (P2[1] - P1[1]) / (P2[0] - P1[0])
    return MC(r, f'For the model {mod}, the graph of {Yn} against {Xn} passes through ({n2(P1[0])}, {n2(P1[1])}) and ({n2(P2[0])}, {n2(P2[1])}). Find the gradient of the line, correct to 3 significant figures.',
              n3(grad), [n3(-grad), n3(1 / grad) if abs(grad) > 1e-6 else '0', n3((P2[1] + P1[1]) / (P2[0] + P1[0]))], f'Gradient = ({n2(P2[1])} − {pn(n2(P1[1]))})/({n2(P2[0])} − {n2(P1[0])}) = {n3(grad)}.')


@l24.add('C2', (1, 2, 3, 4), 'explain')
def l24_err(r, D):
    nm = person(r)
    kind, k, n, P1, P2 = l24_line(r)
    K, Nn, m, c = l24_solve(kind, P1, P2)
    if kind == 'power':
        stem = f'For the model y = kxⁿ, the graph of ln y against ln x is a straight line through ({n2(P1[0])}, {n2(P1[1])}) and ({n2(P2[0])}, {n2(P2[1])}). {nm} finds the intercept {n3(c)} and states that k = {n3(c)}. Explain the error and find k.'
        return Q(stem, f'The intercept is ln k, not k. ln k = {n3(c)}, so k = e^{n3(c)} = {n3(K)}.', f'B1 intercept = ln k; B1 k = {n3(K)}')
    if kind == 'base':
        stem = f'For the model y = Abˣ, the graph of ln y against x is a straight line through ({n2(P1[0])}, {n2(P1[1])}) and ({n2(P2[0])}, {n2(P2[1])}). {nm} says that b equals the gradient, {n3(m)}. Explain the error and find b.'
        return Q(stem, f'The gradient is ln b, not b. ln b = {n3(m)}, so b = e^{n3(m)} = {n3(Nn)}.', f'B1 gradient = ln b; B1 b = {n3(Nn)}')
    stem = f'{nm} wants to find A and b for the model y = Ae^(bx) and plots ln y against ln x. Explain why this is not the correct graph and state which graph should be plotted and what its gradient and intercept represent.'
    return Q(stem, 'ln y = ln A + bx is linear in x, not in ln x; plot ln y against x: gradient b, intercept ln A.', 'B1 ln y = ln A + bx so plot ln y against x; B1 gradient b and intercept ln A')


@l24.add('C3', (1, 2, 3, 4, 5), 'numerical')
def l24_calc(r, D):
    kind, k, n, P1, P2 = l24_line(r)
    if D == 1:
        kind = r.choice(['power', 'exp'])
    K, Nn, m, c = l24_solve(kind, P1, P2)
    mod, Yn, Xn, what = L24_TXT[kind]
    stem = f'The variables x and y satisfy {mod}. The graph of {Yn} against {Xn} is a straight line passing through the points ({n2(P1[0])}, {n2(P1[1])}) and ({n2(P2[0])}, {n2(P2[1])}). Find the values of {what}, correct to 3 significant figures.'
    a1, a2 = what.split(' and ')
    if D >= 4:
        x0 = round(r.uniform(1.5, 6), 1)
        y0 = K * x0 ** Nn if kind == 'power' else (K * math.exp(Nn * x0) if kind == 'exp' else K * Nn ** x0)
        stem = stem[:-1] + f', and hence estimate the value of y when x = {num(x0)}.'
        return Q(stem, f'{a1} = {n3(K)}, {a2} = {n3(Nn)}; y ≈ {n3(y0)}',
                 f'M1 gradient = {n3(m)}; A1 {a2} = {n3(Nn)}; M1 intercept = {n3(c)}; A1 {a1} = {n3(K)}; B1 y ≈ {n3(y0)}')
    return Q(stem, f'{a1} = {n3(K)}, {a2} = {n3(Nn)}', f'M1 gradient = {n3(m)}; A1 {a2} = {n3(Nn)}; M1 intercept {n3(c)} = ln {a1}; A1 {a1} = {n3(K)}')


def l24_c4(r, D):
    kind = r.choice(['power', 'base'])
    _, k, n, P1, P2 = l24_line(r)
    while _ != kind:
        _, k, n, P1, P2 = l24_line(r)
    K, Nn, m, c = l24_solve(kind, P1, P2)
    mod, Yn, Xn, what = L24_TXT[kind]
    a1, a2 = what.split(' and ')
    x0 = round(r.uniform(1.5, 5), 1)
    y0 = K * x0 ** Nn if kind == 'power' else K * Nn ** x0
    intro = f'Two variables x and y are believed to satisfy a relationship of the form {mod}, where {what} are constants. The graph of {Yn} against {Xn} is a straight line passing through ({n2(P1[0])}, {n2(P1[1])}) and ({n2(P2[0])}, {n2(P2[1])}).'
    parts = [
        P(f'Show that {Yn} = {"n ln x + ln k" if kind == "power" else "x ln b + ln A"}.', f'Taking natural logarithms of {mod}.', 'M1 takes ln of both sides; A1 uses ln(uv) = ln u + ln v and ln(uᶜ) = c ln u'),
        P(f'Find the values of {what}.', f'{a1} = {n3(K)}, {a2} = {n3(Nn)}', f'M1 gradient {n3(m)}; A1 {a2} = {n3(Nn)}; M1 intercept {n3(c)}; A1 {a1} = {n3(K)}'),
        P(f'Estimate the value of y when x = {num(x0)}.', n3(y0), f'B1 FT {n3(y0)}'),
        P(f'State one reason why an estimate of y found from this line when x = {num(x0)} may be unreliable.', 'If x lies outside the range of the data (extrapolation) or the points do not lie exactly on the line, the estimate may be unreliable.', 'B1 extrapolation or scatter about the line'),
    ]
    return cmp_(r, intro, parts)


l24.add('C4', (2, 3, 4, 5))(l24_c4)

CHAPTERS[2] = [l21, l22, l23, l24]


# ================================================================ Chapter 3 Trigonometry

R2, R3, R6 = math.sqrt(2), math.sqrt(3), math.sqrt(6)
EXACT = [(0.0, '0'), (0.5, '1/2'), (R2 / 2, '√2/2'), (R3 / 2, '√3/2'), (1.0, '1'), (R3, '√3'), (R3 / 3, '√3/3'), (2.0, '2'), (R2, '√2'),
         (2 * R3 / 3, '2√3/3'), ((R6 + R2) / 4, '(√6 + √2)/4'), ((R6 - R2) / 4, '(√6 − √2)/4'), (2 + R3, '2 + √3'), (2 - R3, '2 − √3')]


def exact_val(v):
    for x, s in EXACT:
        if abs(abs(v) - x) < 1e-9:
            if v < -1e-12 and s != '0':
                return MINUS + (s if not ('+' in s or '−' in s) or s.startswith('(') else f'({s})')
            return s
    return None


def tf(fn, deg):
    t = math.radians(deg)
    s, c = math.sin(t), math.cos(t)
    if fn == 'sin':
        return s
    if fn == 'cos':
        return c
    if fn == 'tan':
        return None if abs(c) < 1e-12 else s / c
    if fn == 'sec':
        return None if abs(c) < 1e-12 else 1 / c
    if fn == 'cosec':
        return None if abs(s) < 1e-12 else 1 / s
    if fn == 'cot':
        return None if abs(s) < 1e-12 else c / s


TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41)]


def triple(r):
    a, b, c = r.choice(TRIPLES)
    if r.random() < 0.5:
        a, b = b, a
    return a, b, c


def angs(xs):
    return dlist(xs)


def recip_sols(fn, s, lo=0, hi=360):
    """Solutions of sec θ = s (fn='cos') or cosec θ = s (fn='sin')."""
    if abs(s) < 1:
        return []
    return sols(fn, 1 / s, 1, 0, lo, hi)


SETR = [Fr(2), Fr(-2), Fr(3, 2), Fr(-3, 2), Fr(4, 3), Fr(5, 4), Fr(-5, 4), Fr(3), Fr(-3), Fr(5, 2), Fr(-4, 3)]
SETBAD = [Fr(1, 2), Fr(-1, 2), Fr(1, 3), Fr(-1, 3), Fr(2, 3), Fr(-2, 3), Fr(3, 4), Fr(-3, 4)]


def quad_with_roots(s1, s2):
    """Integer A, B, C with A s² + B s + C = k(s − s1)(s − s2), A > 0."""
    s1, s2 = Fr(s1), Fr(s2)
    L = math.lcm(s1.denominator, s2.denominator)
    A = L
    B = -A * (s1 + s2)
    C = A * s1 * s2
    if B.denominator != 1 or C.denominator != 1:
        A *= math.lcm(B.denominator, C.denominator)
        B = -A * (s1 + s2)
        C = A * s1 * s2
    return A, int(B), int(C)


t31 = T('Secant, cosecant and cotangent and their graphs', 'secant, cosecant and cotangent', 'cosecant')
t31.fixed('C1', (1, 2), [
    ('Which identity is correct for all θ where both sides are defined?', '1 + tan²θ = sec²θ', 'Divide sin²θ + cos²θ = 1 by cos²θ.', ['1 + sec²θ = tan²θ', '1 + cot²θ = sec²θ', 'sec²θ − 1 = cot²θ']),
    ('What are the equations of the asymptotes of y = sec x for 0° ≤ x ≤ 360°?', 'x = 90° and x = 270°', 'sec x = 1/cos x is undefined where cos x = 0.', ['x = 0°, 180° and 360°', 'y = 1 and y = −1', 'x = 180° only']),
    ('What is the range of y = cosec x?', 'y ≤ −1 or y ≥ 1', 'sin x lies between −1 and 1, so its reciprocal has modulus at least 1.', ['−1 ≤ y ≤ 1', 'y ≥ 1', 'all real y']),
    ('Which of these is equal to cot θ?', 'cos θ / sin θ', 'cot θ = 1/tan θ = cos θ/sin θ.', ['sin θ / cos θ', '1/cos θ', '1/sin θ']),
    ('What is the period of y = cot x, in degrees?', '180°', 'cot x = 1/tan x has the same period as tan x.', ['360°', '90°', '720°']),
])
t31.fixed('C2', (2, 3), [
    ('Explain why the equation sec θ = 0.6 has no solutions.', 'sec θ = 1/cos θ and −1 ≤ cos θ ≤ 1, so |sec θ| ≥ 1; 0.6 lies between −1 and 1.', 'B1 |sec θ| ≥ 1 because |cos θ| ≤ 1; B1 0.6 not in the range [2]'),
    ('Show that 1 + cot²θ ≡ cosec²θ.', 'Divide sin²θ + cos²θ ≡ 1 by sin²θ: 1 + cos²θ/sin²θ ≡ 1/sin²θ, i.e. 1 + cot²θ ≡ cosec²θ.', 'M1 divides sin²θ + cos²θ = 1 by sin²θ; A1 completes using cot θ = cos θ/sin θ [2]'),
    ('Explain why y = cot x has asymptotes at x = 0° and x = 180°, but y = tan x does not.', 'cot x = cos x/sin x is undefined where sin x = 0, i.e. at 0° and 180°; tan x = sin x/cos x is defined there (tan 0° = tan 180° = 0).', 'B1 sin x = 0 at 0°, 180° so cot undefined; B1 tan defined there [2]'),
    ('Show that sec θ − cos θ ≡ sin θ tan θ.', 'sec θ − cos θ = (1 − cos²θ)/cos θ = sin²θ/cos θ = sin θ tan θ.', 'M1 common denominator cos θ; A1 uses 1 − cos²θ = sin²θ to complete [2]'),
])

SPECIAL = [30, 45, 60, 120, 135, 150, 210, 225, 240, 300, 315, 330]


@t31.add('C1', (1, 2, 3))
def t31_c1(r, D):
    if D == 1:
        fn = r.choice(['sec', 'cosec', 'cot'])
        a = r.choice(SPECIAL)
        v = tf(fn, a)
        if v is None:
            return None
        c = exact_val(v)
        ds = [exact_val(x) for x in (-v, 1 / v if v else None, tf('sin', a), tf('cos', a)) if x is not None and exact_val(x)]
        return MC(r, f'Find the exact value of {fn} {a}°.', c, ds + ['2', '√2', '1/2'], f'{fn} {a}° = {c}.')
    a, b, c = triple(r)
    fn = r.choice(['sec', 'cosec', 'cot'])
    if D == 2:
        val = {'sec': Fr(c, b), 'cosec': Fr(c, a), 'cot': Fr(b, a)}[fn]
        return MC(r, f'Given that tan θ = {num(Fr(a, b))} and θ is acute, find the exact value of {fn} θ.', num(val),
                  [num(1 / val), num(-val), num(Fr(a, c)), num(Fr(b, c)), num(Fr(c, a + b))], f'Right-angled triangle with sides {a}, {b}, {c}: {fn} θ = {num(val)}.')
    val = {'sec': Fr(-c, b), 'cosec': Fr(c, a), 'cot': Fr(-b, a)}[fn]
    return MC(r, f'Given that sin θ = {num(Fr(a, c))} and 90° < θ < 180°, find the exact value of {fn} θ.', num(val),
              [num(-val), num(1 / val), num(Fr(b, c)), num(Fr(-a, b))], f'cos θ = −{b}/{c} in the second quadrant, so {fn} θ = {num(val)}.')


@t31.add('C2', (1, 2, 3, 4), 'explain')
def t31_err(r, D):
    nm = person(r)
    f = r.choice(['recip', 'range', 'sign'])
    if f == 'recip':
        a = r.choice([30, 60, 120, 150, 210, 240, 300, 330])
        wrong, right = exact_val(1 / tf('sin', a)), exact_val(1 / tf('cos', a))
        if wrong == right:
            return None
        stem = f'{nm} evaluates sec {a}° as 1/sin {a}° = {wrong}. Explain the error and give the correct exact value.'
        return Q(stem, f'sec θ = 1/cos θ, not 1/sin θ. sec {a}° = 1/cos {a}° = {right}.', f'B1 sec θ = 1/cos θ; B1 {right}')
    if f == 'range':
        k = r.choice(SETBAD)
        fn = r.choice(['sec', 'cosec'])
        stem = f'{nm} tries to solve {fn} θ = {num(k)} for 0° ≤ θ ≤ 360° and writes {"cos" if fn == "sec" else "sin"} θ = {num(1 / k)}. Explain why there are no solutions.'
        return Q(stem, f'{"cos" if fn == "sec" else "sin"} θ = {num(1 / k)} is impossible because the value lies outside −1 ≤ {"cos" if fn == "sec" else "sin"} θ ≤ 1, so {fn} θ can never equal {num(k)} (|{fn} θ| ≥ 1).',
                     f'B1 {num(1 / k)} outside [−1, 1]; B1 conclusion: no solutions')
    a, b, c = triple(r)
    stem = f'Given that cos θ = {MINUS}{num(Fr(b, c))} and 180° < θ < 270°, {nm} says cot θ = {MINUS}{num(Fr(b, a))}. Explain the error and give the correct value of cot θ.'
    return Q(stem, f'In the third quadrant sin θ is also negative (sin θ = −{a}/{c}), so cot θ = cos θ/sin θ is positive: cot θ = {num(Fr(b, a))}.',
             f'B1 sin θ < 0 in third quadrant; B1 cot θ = {num(Fr(b, a))}')


@t31.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t31_calc(r, D):
    if D <= 2:
        fn = r.choice(['sec', 'cosec', 'cot'])
        k = r.choice(SETR + [Fr(5, 3), Fr(-5, 3), Fr(7, 2)])
        if fn == 'cot':
            xs = sols('tan', float(1 / k))
            inv = f'tan θ = {num(1 / k)}'
        else:
            xs = recip_sols('cos' if fn == 'sec' else 'sin', float(k))
            inv = f'{"cos" if fn == "sec" else "sin"} θ = {num(1 / k)}'
        if D == 1:
            return Q(f'Solve the equation {fn} θ = {num(k)} for 0° ≤ θ ≤ 360°.', angs(xs), f'M1 {inv}; A1 one correct angle; A1 second angle and no extras')
        m = r.randint(2, 4)
        rhs = m * k
        return Q(f'Solve the equation {m} {fn} θ = {num(rhs)} for 0° ≤ θ ≤ 360°.', angs(xs), f'M1 {inv}; A1 one correct angle; A1 second angle and no extras')
    fn, inv, ident = (('sec', 'cos', 'tan²θ = sec²θ − 1') if D in (3, 5) else ('cosec', 'sin', 'cot²θ = cosec²θ − 1'))
    sq_ = 'tan²θ' if fn == 'sec' else 'cot²θ'
    s1 = r.choice(SETR)
    s2 = r.choice(SETBAD + SETR)
    if s1 == s2:
        return None
    A, B, C = quad_with_roots(s1, s2)
    # A sec² + B sec + C = 0 with sec² = tan² + 1  ->  A tan² + B sec + (C + A) = 0
    lo, hi = (0, 360) if D != 5 else (-180, 180)
    xs = sorted(set(recip_sols(inv, float(s1), lo, hi) + recip_sols(inv, float(s2), lo, hi)))
    stem = f'Solve the equation {tsum([(A, sq_), (B, fn + " θ"), (C + A, "")])} = 0 for {lo}° ≤ θ ≤ {hi}°.'
    rej = [s for s in (s1, s2) if abs(s) < 1]
    return Q(stem, angs(xs), f'M1 uses {ident}; A1 {pstr([A, B, C], fn[0])} = 0 in {fn} θ; A1 {fn} θ = {num(s1)}, {num(s2)}' + (f' ({num(rej[0])} rejected)' if rej else '')
             + f'; M1 {inv} θ = 1/({fn} θ); A1 {angs(xs)}')


def t31_c4(r, D):
    s1 = r.choice(SETR)
    s2 = r.choice(SETBAD)
    A, B, C = quad_with_roots(s1, s2)
    xs = recip_sols('cos', float(s1))
    a, b, c = triple(r)
    eq = f'{tsum([(A, "tan²θ"), (B, "sec θ"), (C + A, "")])} = 0'
    intro = f'In this question, angles are in degrees and 0° ≤ θ ≤ 360°.'
    parts = [
        P('Sketch the graph of y = sec θ, stating the equations of the asymptotes.', 'U-shaped branches with minimum (0, 1)/(360, 1) and maximum (180, −1); asymptotes θ = 90° and θ = 270°.',
          'B1 correct shape with turning points at (0°, 1), (180°, −1), (360°, 1); B1 asymptotes θ = 90°, 270°'),
        P(f'Show that the equation {eq} can be written as {pstr([A, B, C], "s")} = 0, where s = sec θ.', 'Replace tan²θ by sec²θ − 1 and simplify.', 'M1 uses tan²θ = sec²θ − 1; A1 simplifies to the given quadratic'),
        P(f'Solve the equation {eq}.', angs(xs), f'M1 solves the quadratic: sec θ = {num(s1)} or {num(s2)}; A1 rejects {num(s2)}; A1 {angs(xs)}'),
        P(f'Given that tan α = {num(Fr(a, b))} and α is acute, find the exact value of cosec α.', num(Fr(c, a)), f'M1 uses a {a}-{b}-{c} triangle or 1 + cot²α = cosec²α; A1 {num(Fr(c, a))}'),
    ]
    return cmp_(r, intro, parts)


t31.add('C4', (2, 3, 4, 5))(t31_c4)


# ---------------------------------------------------------------- 3.2 compound angles

def sc_of(a, b, c, quad_):
    """(sin, cos) Fractions of an angle with sin = a/c (acute) placed in quadrant quad_ (1 or 2)."""
    return (Fr(a, c), Fr(b, c)) if quad_ == 1 else (Fr(a, c), Fr(-b, c))


t32 = T('Compound angle formulae for sin(A ± B), cos(A ± B) and tan(A ± B)', 'compound angle formulae', 'sin(a ± b)')
t32.fixed('C1', (1, 2), [
    ('Which is the correct expansion of cos(A − B)?', 'cos A cos B + sin A sin B', 'cos(A − B) = cos A cos B + sin A sin B.', ['cos A cos B − sin A sin B', 'cos A − cos B', 'sin A cos B − cos A sin B']),
    ('Which is the correct expansion of sin(A + B)?', 'sin A cos B + cos A sin B', 'Standard compound angle formula.', ['sin A + sin B', 'sin A sin B + cos A cos B', 'sin A cos B − cos A sin B']),
    ('Which is the correct expansion of tan(A + B)?', '(tan A + tan B)/(1 − tan A tan B)', 'Standard compound angle formula.', ['(tan A + tan B)/(1 + tan A tan B)', 'tan A + tan B', '(tan A − tan B)/(1 + tan A tan B)']),
    ('sin 50° cos 20° − cos 50° sin 20° is equal to', 'sin 30°', 'sin(A − B) with A = 50°, B = 20°.', ['sin 70°', 'cos 30°', 'cos 70°']),
])
t32.fixed('C2', (2, 3), [
    ('Show that sin(θ + 90°) ≡ cos θ using a compound angle formula.', 'sin(θ + 90°) = sin θ cos 90° + cos θ sin 90° = sin θ × 0 + cos θ × 1 = cos θ.', 'M1 expands; A1 uses cos 90° = 0, sin 90° = 1 [2]'),
    ('Show that cos(A + B) + cos(A − B) ≡ 2 cos A cos B.', 'Expanding: (cos A cos B − sin A sin B) + (cos A cos B + sin A sin B) = 2 cos A cos B.', 'M1 expands both; A1 sin terms cancel [2]'),
    ('Use a compound angle formula to show that tan 15° = 2 − √3.', 'tan(45° − 30°) = (1 − 1/√3)/(1 + 1/√3) = (√3 − 1)/(√3 + 1) = (√3 − 1)²/2 = 2 − √3.', 'M1 tan(45° − 30°) with exact values; A1 rationalises to 2 − √3 [2]'),
])

C_ANG = [15, 75, 105, 165, 195, 255, 285, 345]


@t32.add('C1', (1, 2, 3))
def t32_c1(r, D):
    if D <= 2:
        a = r.choice(C_ANG)
        fn = r.choice(['sin', 'cos', 'tan'])
        v = tf(fn, a)
        c = exact_val(v)
        if not c:
            return None
        pool = [exact_val(s * x) for x in ((R6 + R2) / 4, (R6 - R2) / 4, 2 + R3, 2 - R3) for s in (1, -1)]
        pool = [p for p in pool if p and p != c]
        r.shuffle(pool)
        split = {15: '45° − 30°', 75: '45° + 30°', 105: '60° + 45°', 165: '120° + 45°', 195: '150° + 45°', 255: '210° + 45°', 285: '240° + 45°', 345: '300° + 45°'}[a]
        return MC(r, f'Use a compound angle formula to find the exact value of {fn} {a}°.', c, pool, f'Write {a}° = {split} and expand: {fn} {a}° = {c}.')
    a, b, c = triple(r)
    p, q, s = triple(r)
    sA, cA = Fr(a, c), Fr(b, c)
    sB, cB = Fr(p, s), Fr(q, s)
    fn = r.choice(['sin(A + B)', 'cos(A + B)', 'sin(A − B)', 'cos(A − B)'])
    val = {'sin(A + B)': sA * cB + cA * sB, 'cos(A + B)': cA * cB - sA * sB, 'sin(A − B)': sA * cB - cA * sB, 'cos(A − B)': cA * cB + sA * sB}[fn]
    alt = [sA * cB + cA * sB, cA * cB - sA * sB, sA * cB - cA * sB, cA * cB + sA * sB, sA + sB, cA * cB]
    return MC(r, f'Angles A and B are acute, with sin A = {num(sA)} and cos B = {num(cB)}. Find the exact value of {fn}.', num(val), [num(x) for x in alt],
              f'cos A = {num(cA)}, sin B = {num(sB)}; {fn} = {num(val)}.')


@t32.add('C2', (1, 2, 3, 4), 'explain')
def t32_err(r, D):
    nm = person(r)
    f = r.choice(['sum', 'tan'])
    if f == 'sum':
        A, B = r.choice([(30, 60), (60, 30), (45, 45), (30, 30), (60, 60), (45, 30), (30, 45), (60, 45), (45, 60)])
        fn = r.choice(['sin', 'cos'])
        wrong = tf(fn, A) + tf(fn, B)
        right = tf(fn, A + B)
        ws = f'{exact_val(tf(fn, A))} + {exact_val(tf(fn, B))}'
        stem = f'{nm} claims that {fn}({A}° + {B}°) = {fn} {A}° + {fn} {B}°. Show, by evaluating both sides exactly, that this is false, and state the correct expansion of {fn}(A + B).'
        exp_ = 'sin A cos B + cos A sin B' if fn == 'sin' else 'cos A cos B − sin A sin B'
        return Q(stem, f'{fn} {A + B}° = {exact_val(right)}, but {fn} {A}° + {fn} {B}° = {ws} ≈ {n3(wrong)}, so they are not equal. {fn}(A + B) = {exp_}.',
                 f'B1 both sides evaluated and shown unequal; B1 {exp_}')
    tA, tB = r.choice([Fr(1, 2), Fr(1, 3), Fr(2, 3), Fr(3, 4), Fr(1, 4), Fr(2)]), r.choice([Fr(1, 5), Fr(1, 3), Fr(1, 2), Fr(3, 5), Fr(1, 7)])
    if tA * tB == 1 or tA == tB:
        return None
    wrong = (tA + tB) / (1 + tA * tB)
    right = (tA + tB) / (1 - tA * tB)
    stem = f'Given that tan A = {num(tA)} and tan B = {num(tB)}, {nm} calculates tan(A + B) = ({num(tA)} + {num(tB)})/(1 + {num(tA)} × {num(tB)}) = {num(wrong)}. Explain the error and find the correct exact value.'
    return Q(stem, f'The denominator of tan(A + B) is 1 − tan A tan B. tan(A + B) = ({num(tA + tB)})/({num(1 - tA * tB)}) = {num(right)}.', f'B1 denominator 1 − tan A tan B; B1 {num(right)}')


@t32.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t32_calc(r, D):
    if D <= 2:
        a, b, c = triple(r)
        p, q, s = triple(r)
        qa = 1 if D == 1 else 2
        sA, cA = sc_of(a, b, c, qa)
        sB, cB = Fr(p, s), Fr(q, s)
        fn = r.choice(['sin(A + B)', 'cos(A + B)', 'sin(A − B)', 'cos(A − B)', 'tan(A + B)', 'tan(A − B)'] if D == 2 else ['sin(A + B)', 'cos(A + B)', 'sin(A − B)', 'cos(A − B)'])
        tA, tB = sA / cA, sB / cB
        val = {'sin(A + B)': sA * cB + cA * sB, 'cos(A + B)': cA * cB - sA * sB, 'sin(A − B)': sA * cB - cA * sB, 'cos(A − B)': cA * cB + sA * sB,
               'tan(A + B)': (tA + tB) / (1 - tA * tB) if tA * tB != 1 else None, 'tan(A − B)': (tA - tB) / (1 + tA * tB)}[fn]
        if val is None:
            return None
        cond = 'A is acute' if qa == 1 else '90° < A < 180°'
        stem = f'It is given that sin A = {num(sA)}, where {cond}, and cos B = {num(cB)}, where B is acute. Find the exact value of {fn}.'
        return Q(stem, num(val), f'B1 cos A = {num(cA)}; B1 sin B = {num(sB)}; M1 correct expansion of {fn}; A1 {num(val)}')
    if D == 3:
        tA = r.choice([Fr(1, 2), Fr(1, 3), Fr(2, 3), Fr(3, 4), Fr(1, 4), Fr(2), Fr(3)])
        k = r.choice([Fr(1), Fr(2), Fr(3), Fr(-1), Fr(1, 2), Fr(4, 3), Fr(5)])
        if 1 + k * tA == 0:
            return None
        tB = (k - tA) / (1 + k * tA)
        stem = f'Given that tan(A + B) = {num(k)} and tan A = {num(tA)}, find the exact value of tan B.'
        return Q(stem, f'tan B = {num(tB)}', f'M1 ({num(tA)} + t)/(1 − {num(tA)}t) = {num(k)}; M1 rearranges for t; A1 tan B = {num(tB)}')
    al = r.choice([30, 45, 60])
    sa, ca = math.sin(math.radians(al)), math.cos(math.radians(al))
    if D == 4:
        k = r.choice([1, 2, 3, -1, -2, 4])
        m = r.choice([1, 2])
        tt = (k - m * sa) / (m * ca)
        xs = sols('tan', tt)
        lhs = f'{"" if m == 1 else m}sin(θ + {al}°)'
        return Q(f'Solve the equation {lhs} = {coefk(k)}cos θ for 0° ≤ θ ≤ 360°.', angs(xs),
                 f'M1 expands sin(θ + {al}°); M1 divides by cos θ to obtain tan θ = {n4(tt)}; A1 {d1(xs[0])}; A1 {d1(xs[1])}')
    k = r.choice([2, 3, 4, 5])
    m = r.choice([1, 2])
    if abs(k - m * sa) < 1e-9:
        return None
    tt = m * ca / (k - m * sa)
    xs = sols('tan', tt)
    return Q(f'Solve the equation {"" if m == 1 else m}cos(θ − {al}°) = {k} sin θ for 0° ≤ θ ≤ 360°.', angs(xs),
             f'M1 expands cos(θ − {al}°) with exact values; M1 tan θ = {n4(tt)}; A1 {d1(xs[0])}; A1 {d1(xs[1])}')


def coefk(k):
    if k == 1:
        return ''
    if k == -1:
        return MINUS
    return (num(k) if Fr(k).denominator == 1 else num(float(k))) + ' '


def t32_c4(r, D):
    a, b, c = triple(r)
    p, q, s = triple(r)
    sA, cA = Fr(a, c), Fr(b, c)
    sB, cB = Fr(-p, s), Fr(-q, s)  # B in third quadrant
    tA, tB = sA / cA, sB / cB
    if tA * tB == 1:
        return None
    intro = f'Angles A and B are such that sin A = {num(sA)} with 0° < A < 90°, and cos B = {num(cB)} with 180° < B < 270°.'
    parts = [
        P('Find the exact value of sin B.', num(sB), f'M1 Pythagoras or identity; A1 {num(sB)} (negative in third quadrant)'),
        P('Find the exact value of sin(A + B).', num(sA * cB + cA * sB), f'M1 sin A cos B + cos A sin B; A1 {num(sA * cB + cA * sB)}'),
        P('Find the exact value of cos(A − B).', num(cA * cB + sA * sB), f'M1 cos A cos B + sin A sin B; A1 {num(cA * cB + sA * sB)}'),
        P('Find the exact value of tan(A + B).', num((tA + tB) / (1 - tA * tB)), f'B1 tan A = {num(tA)}, tan B = {num(tB)}; M1 formula; A1 {num((tA + tB) / (1 - tA * tB))}'),
    ]
    return cmp_(r, intro, parts)


t32.add('C4', (2, 3, 4, 5))(t32_c4)


# ---------------------------------------------------------------- 3.3 double angles, identities

IDENTS = [
    ('Prove the identity (sin 2θ)/(1 + cos 2θ) ≡ tan θ.', 'sin 2θ/(1 + cos 2θ) = 2 sin θ cos θ/(2cos²θ) = sin θ/cos θ = tan θ.', 'M1 sin 2θ = 2 sin θ cos θ and 1 + cos 2θ = 2cos²θ; A1 simplifies to tan θ [2]'),
    ('Prove the identity (1 − cos 2θ)/sin 2θ ≡ tan θ.', '(1 − cos 2θ)/sin 2θ = 2sin²θ/(2 sin θ cos θ) = sin θ/cos θ = tan θ.', 'M1 1 − cos 2θ = 2sin²θ; A1 cancels to tan θ [2]'),
    ('Prove the identity cos⁴θ − sin⁴θ ≡ cos 2θ.', 'cos⁴θ − sin⁴θ = (cos²θ − sin²θ)(cos²θ + sin²θ) = cos 2θ × 1.', 'M1 difference of two squares; A1 uses cos²θ + sin²θ = 1 and cos 2θ = cos²θ − sin²θ [2]'),
    ('Prove the identity (cos θ + sin θ)² ≡ 1 + sin 2θ.', '(cos θ + sin θ)² = cos²θ + sin²θ + 2 sin θ cos θ = 1 + sin 2θ.', 'M1 expands; A1 uses both identities [2]'),
    ('Prove the identity tan θ + cot θ ≡ 2 cosec 2θ.', 'tan θ + cot θ = (sin²θ + cos²θ)/(sin θ cos θ) = 1/(sin θ cos θ) = 2/sin 2θ = 2 cosec 2θ.', 'M1 common denominator; A1 uses sin 2θ = 2 sin θ cos θ [2]'),
    ('Prove the identity cot θ − tan θ ≡ 2 cot 2θ.', '(cos²θ − sin²θ)/(sin θ cos θ) = cos 2θ/((1/2) sin 2θ) = 2 cot 2θ.', 'M1 common denominator; A1 uses cos 2θ and sin 2θ [2]'),
    ('Prove the identity sin 3θ ≡ 3 sin θ − 4 sin³θ.', 'sin(2θ + θ) = sin 2θ cos θ + cos 2θ sin θ = 2 sin θ cos²θ + (1 − 2sin²θ) sin θ = 2 sin θ(1 − sin²θ) + sin θ − 2sin³θ = 3 sin θ − 4 sin³θ.', 'M1 sin(2θ + θ) expanded with double angle formulae; A1 uses cos²θ = 1 − sin²θ to reach the result [2]'),
    ('Prove the identity cos 3θ ≡ 4 cos³θ − 3 cos θ.', 'cos(2θ + θ) = cos 2θ cos θ − sin 2θ sin θ = (2cos²θ − 1) cos θ − 2 sin²θ cos θ = 2cos³θ − cos θ − 2cos θ(1 − cos²θ) = 4cos³θ − 3 cos θ.', 'M1 expands cos(2θ + θ) with double angle formulae; A1 uses sin²θ = 1 − cos²θ to reach the result [2]'),
    ('Prove the identity (2 tan θ)/(1 + tan²θ) ≡ sin 2θ.', '2 tan θ/sec²θ = 2 (sin θ/cos θ) cos²θ = 2 sin θ cos θ = sin 2θ.', 'M1 1 + tan²θ = sec²θ; A1 simplifies to sin 2θ [2]'),
    ('Prove the identity cosec 2θ + cot 2θ ≡ cot θ.', '(1 + cos 2θ)/sin 2θ = 2cos²θ/(2 sin θ cos θ) = cos θ/sin θ = cot θ.', 'M1 combines into (1 + cos 2θ)/sin 2θ; A1 simplifies [2]'),
]

t33 = T('Double angle formulae and proving identities', 'double angle formulae', 'proving identities')
t33.fixed('C1', (1, 2), [
    ('Which of these is NOT equal to cos 2θ?', '2 cos²θ + 1', 'cos 2θ = cos²θ − sin²θ = 2cos²θ − 1 = 1 − 2sin²θ.', ['cos²θ − sin²θ', '1 − 2 sin²θ', '2 cos²θ − 1']),
    ('Which of these is equal to sin 2θ?', '2 sin θ cos θ', 'Put A = B = θ in sin(A + B).', ['2 sin θ', 'sin²θ − cos²θ', 'sin θ cos θ']),
    ('Which expression is equal to sin²θ?', '(1 − cos 2θ)/2', 'From cos 2θ = 1 − 2sin²θ.', ['(1 + cos 2θ)/2', '(cos 2θ − 1)/2', '1 − cos 2θ']),
    ('Which expression is equal to tan 2θ?', '2 tan θ/(1 − tan²θ)', 'Put A = B = θ in tan(A + B).', ['2 tan θ/(1 + tan²θ)', '2 tan θ', 'tan²θ/(1 − 2 tan θ)']),
])
t33.fixed('C2', (2, 3, 4), IDENTS)


@t33.add('C1', (1, 2, 3))
def t33_c1(r, D):
    a, b, c = triple(r)
    if D == 1:
        p = r.choice([Fr(1, 3), Fr(2, 3), Fr(1, 4), Fr(3, 4), Fr(2, 5), Fr(3, 5), Fr(1, 5), Fr(-1, 3), Fr(-2, 5)])
        return MC(r, f'Given that cos θ = {num(p)}, find the exact value of cos 2θ.', num(2 * p * p - 1), [num(2 * p), num(1 - 2 * p * p), num(2 * p * p + 1), num(p * p - 1)], f'cos 2θ = 2cos²θ − 1 = {num(2 * p * p - 1)}.')
    if D == 2:
        return MC(r, f'Given that sin θ = {num(Fr(a, c))} and θ is acute, find the exact value of sin 2θ.', num(Fr(2 * a * b, c * c)),
                  [num(Fr(2 * a, c)), num(Fr(a * b, c * c)), num(Fr(b * b - a * a, c * c)), num(Fr(-2 * a * b, c * c))], f'cos θ = {b}/{c}; sin 2θ = 2({a}/{c})({b}/{c}) = {num(Fr(2 * a * b, c * c))}.')
    t = Fr(a, b)
    if t == 1:
        return None
    return MC(r, f'Given that tan θ = {num(t)}, find the exact value of tan 2θ.', num(2 * t / (1 - t * t)), [num(2 * t), num(2 * t / (1 + t * t)), num(-2 * t / (1 - t * t)), num(t * t)],
              f'tan 2θ = 2t/(1 − t²) = {num(2 * t / (1 - t * t))}.')


@t33.add('C2', (1, 2, 3, 4), 'explain')
def t33_err(r, D):
    nm = person(r)
    f = r.choice(['double', 'divide'])
    if f == 'double':
        a = r.choice([30, 45, 60, 90, 120, 135, 150])
        fn = r.choice(['sin', 'cos'])
        right, wrong = exact_val(tf(fn, 2 * a)), exact_val(2 * tf(fn, a)) or n3(2 * tf(fn, a))
        if right is None or right == wrong:
            return None
        stem = f'{nm} says that {fn} 2θ = 2 {fn} θ, and so {fn} {2 * a}° = 2 {fn} {a}° = {wrong}. Explain why this is wrong and give the correct value of {fn} {2 * a}°.'
        formula = '2 sin θ cos θ' if fn == 'sin' else 'cos²θ − sin²θ'
        return Q(stem, f'{fn} 2θ = {formula}, not 2 {fn} θ. {fn} {2 * a}° = {right}.', f'B1 correct double angle formula; B1 {fn} {2 * a}° = {right}')
    k = r.choice([Fr(1), Fr(-1), Fr(1, 2), Fr(-1, 2), Fr(3, 2), Fr(6, 5)])
    xs = sols('cos', float(k / 2))
    all_ = sorted(set([0.0, 180.0, 360.0] + xs))
    stem = f'{nm} solves sin 2θ = {coefk(k)}sin θ for 0° ≤ θ ≤ 360° by writing 2 sin θ cos θ = {coefk(k)}sin θ, dividing by sin θ and solving cos θ = {num(float(k / 2))}. Explain what is wrong with this method and give all the solutions.'
    return Q(stem, f'Dividing by sin θ loses the solutions of sin θ = 0. Factorise: sin θ(2 cos θ{sg(-float(k)) if Fr(k).denominator != 1 else sg(-k)}) = 0, giving {angs(all_)}.',
             f'B1 dividing by sin θ loses sin θ = 0 (factorise instead); B1 0°, 180°, 360°; B1 {angs(xs)}' if D >= 3 else f'B1 dividing by sin θ loses sin θ = 0; B1 all solutions {angs(all_)}')


@t33.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t33_calc(r, D):
    a, b, c = triple(r)
    if D == 1:
        t = Fr(a, b)
        if t == 1:
            return None
        return Q(f'Given that tan θ = {num(t)}, find the exact value of tan 2θ.', num(2 * t / (1 - t * t)), f'M1 2t/(1 − t²); A1 {num(2 * t / (1 - t * t))}')
    if D == 2:
        s, cc = Fr(a, c), Fr(-b, c)
        return Q(f'Given that sin θ = {num(s)} and 90° < θ < 180°, find the exact values of sin 2θ and cos 2θ.', f'sin 2θ = {num(2 * s * cc)}, cos 2θ = {num(1 - 2 * s * s)}',
                 f'B1 cos θ = {num(cc)}; M1 2 sin θ cos θ; A1 {num(2 * s * cc)}; A1 cos 2θ = {num(1 - 2 * s * s)}')
    if D in (3, 5):
        fn = 'sin' if D == 3 else 'cos'
        s1 = r.choice([Fr(1, 2), Fr(-1, 2), Fr(1, 3), Fr(-1, 3), Fr(3, 4), Fr(-1, 4), Fr(2, 3), Fr(1, 4)])
        s2 = r.choice([Fr(2), Fr(-2), Fr(3, 2), Fr(-3, 2), Fr(1), Fr(-1), Fr(1, 2), Fr(-1, 2)])
        if s1 == s2:
            return None
        # k cos 2θ + a f + b = 0, with cos 2θ = 1 − 2 sin² (fn=sin) or 2cos² − 1 (fn=cos)
        A, B, C = quad_with_roots(s1, s2)   # A s² + B s + C
        if A % 2:
            A, B, C = 2 * A, 2 * B, 2 * C
        k = A // 2
        if fn == 'sin':
            # k(1 − 2s²) + a s + b = −(A s² + B s + C)  ->  a = −B, b = −C − k
            aa, bb, kk = -B, -C - k, k
        else:
            # k(2c² − 1) + a c + b = A c² + B c + C  ->  a = B, b = C + k
            aa, bb, kk = B, C + k, k
        xs = sorted(set(sols(fn, float(s1)) + sols(fn, float(s2))))
        stem = f'Solve the equation {tsum([(kk, "cos 2θ"), (aa, fn + " θ"), (bb, "")])} = 0 for 0° ≤ θ ≤ 360°.'
        return Q(stem, angs(xs), f'M1 uses cos 2θ = {"1 − 2sin²θ" if fn == "sin" else "2cos²θ − 1"}; A1 {pstr([A, B, C], "s")} = 0 (s = {fn} θ) or equivalent; A1 {fn} θ = {num(s1)}, {num(s2)}; A1 {angs(xs)}')
    k = r.choice([Fr(1), Fr(-1), Fr(1, 2), Fr(-1, 2), Fr(3, 2), Fr(6, 5), Fr(-6, 5)])
    xs = sorted(set([90.0, 270.0] + sols('sin', float(k / 2))))
    return Q(f'Solve the equation sin 2θ = {coefk(k)}cos θ for 0° ≤ θ ≤ 360°.', angs(xs),
             f'M1 2 sin θ cos θ = {coefk(k)}cos θ; M1 factorises cos θ(2 sin θ{sg(-float(k)) if Fr(k).denominator != 1 else sg(-k)}) = 0; A1 90°, 270°; A1 {angs(sols("sin", float(k / 2)))}')


def t33_c4(r, D):
    s1 = r.choice([Fr(1, 2), Fr(-1, 2), Fr(1, 3), Fr(3, 4), Fr(-1, 4), Fr(2, 3)])
    s2 = r.choice([Fr(2), Fr(-2), Fr(3, 2), Fr(-3, 2)])
    A, B, C = quad_with_roots(s1, s2)
    if A % 2:
        A, B, C = 2 * A, 2 * B, 2 * C
    k = A // 2
    aa, bb = -B, -C - k
    xs = sols('sin', float(s1))
    eq = f'{tsum([(k, "cos 2θ"), (aa, "sin θ"), (bb, "")])} = 0'
    idn = r.choice(IDENTS)
    intro = 'In this question, 0° ≤ θ ≤ 360°.'
    parts = [
        P(f'Show that the equation {eq} can be written in the form {pstr([A, B, C], "s")} = 0, where s = sin θ.', 'Use cos 2θ = 1 − 2sin²θ and rearrange.', 'M1 uses cos 2θ = 1 − 2sin²θ; A1 rearranges to the given form'),
        P(f'Solve the equation {eq}.', angs(xs), f'M1 sin θ = {num(s1)} or {num(s2)}; A1 rejects {num(s2)}; A1 {angs(xs)}'),
        P(idn[0], idn[1], idn[2].replace(' [2]', '')),
    ]
    return cmp_(r, intro, parts, k=(2, 3))


t33.add('C4', (2, 3, 4, 5))(t33_c4)


# ---------------------------------------------------------------- 3.4 R sin(θ ± α)

RFORMS = {
    'sin+': ('{a} sin θ + {b} cos θ', 'R sin(θ + α)', 'sin', 1),
    'sin-': ('{a} sin θ − {b} cos θ', 'R sin(θ − α)', 'sin', -1),
    'cos+': ('{a} cos θ − {b} sin θ', 'R cos(θ + α)', 'cos', 1),
    'cos-': ('{a} cos θ + {b} sin θ', 'R cos(θ − α)', 'cos', -1),
}


def rform(r):
    kind = r.choice(list(RFORMS))
    a, b = r.randint(1, 8), r.randint(1, 8)
    if a == b:
        b += 1
    R = math.sqrt(a * a + b * b)
    al = math.degrees(math.atan2(b, a))
    tmpl, form, fn, sg_ = RFORMS[kind]
    expr = tmpl.format(a=a, b=b).replace('1 sin', 'sin').replace('1 cos', 'cos') if True else ''
    expr = re.sub(r'(?<![\d])1 (sin|cos)', r'\1', tmpl.format(a=a, b=b))
    return kind, a, b, R, al, expr, form, fn, sg_


def rsub(form, R, al):
    return form.replace('R', sqrt_str(int(round(R * R)))).replace('α', d2(al))


def r_eval(kind, R, al, th):
    fn, sg_ = RFORMS[kind][2], RFORMS[kind][3]
    u = math.radians(th + sg_ * al)
    return R * (math.sin(u) if fn == 'sin' else math.cos(u))


def r_solve(kind, R, al, c, lo=0, hi=360, mult=1):
    fn, sg_ = RFORMS[kind][2], RFORMS[kind][3]
    return sols(fn, c / R, mult, sg_ * al, lo, hi)


t34 = T('Expressing a sin θ + b cos θ as R sin(θ ± α)', 'r sin(θ ± α)', 'a sin θ + b cos θ')
t34.fixed('C1', (1, 2), [
    ('3 sin θ + 4 cos θ is written as R sin(θ + α). What is the value of R?', '5', 'R = √(3² + 4²) = 5.', ['7', '1', '25']),
    ('What is the greatest value of 5 sin(θ + 30°) + 2?', '7', 'Greatest value of sin is 1: 5 + 2 = 7.', ['5', '3', '2']),
    ('a cos θ + b sin θ = R cos(θ − α) with a, b > 0. Which gives tan α?', 'b/a', 'R cos α = a and R sin α = b, so tan α = b/a.', ['a/b', 'ab', 'a/R']),
])
t34.fixed('C2', (2, 3), [
    ('Explain why the greatest value of 7 sin θ + 24 cos θ is 25.', 'It equals 25 sin(θ + α) with R = √(7² + 24²) = 25, and the greatest value of sin is 1.', 'B1 R = 25; B1 sin ≤ 1 [2]'),
    ('Explain why the equation 2 sin θ + 3 cos θ = 4 has no solutions.', 'The left side can be written as √13 sin(θ + α), whose greatest value is √13 ≈ 3.61 < 4.', 'B1 R = √13; B1 √13 < 4 so no solutions [2]'),
])


@t34.add('C1', (1, 2, 3))
def t34_c1(r, D):
    kind, a, b, R, al, expr, form, fn, sg_ = rform(r)
    R2_ = a * a + b * b
    if D == 1:
        return MC(r, f'The expression {expr} is written in the form {form}, where R > 0. Find the exact value of R.', sqrt_str(R2_),
                  [str(a + b), sqrt_str(abs(a * a - b * b)) if a * a != b * b else str(R2_), str(R2_), sqrt_str(a * a + b)], f'R = √({a}² + {b}²) = {sqrt_str(R2_)}.')
    if D == 2:
        return MC(r, f'The expression {expr} is written in the form {form}, where R > 0 and 0° < α < 90°. Find α correct to 2 decimal places.', d2(al),
                  [d2(90 - al), d2(math.degrees(math.atan(a / b)) + 1), d2(math.degrees(math.asin(min(1, b / (a + b))))), d2(al + 90)], f'tan α = {b}/{a}, α = {d2(al)}.')
    c = r.randint(1, 9)
    return MC(r, f'Find the greatest value of {c} + {expr}.', plus(str(c), sqrt_str(R2_)) if surd(R2_)[1] > 1 else str(c + int(round(R))),
              [str(c + a + b), plus(str(c), str(R2_)), str(c), f'{c} − {sqrt_str(R2_)}' if surd(R2_)[1] > 1 else str(c - int(round(R)))], f'Greatest value of {expr} is R = {sqrt_str(R2_)}.')


@t34.add('C2', (1, 2, 3, 4), 'explain')
def t34_err(r, D):
    nm = person(r)
    kind, a, b, R, al, expr, form, fn, sg_ = rform(r)
    f = r.choice(['tan', 'recip'])
    if f == 'tan':
        wrong = math.degrees(math.atan2(a, b))
        stem = f'{nm} writes {expr} in the form {form} and obtains α = tan⁻¹({a}/{b}) = {d2(wrong)}. Explain the error and find the correct value of α.'
        return Q(stem, f'Comparing coefficients gives R cos α = {a} and R sin α = {b}, so tan α = {b}/{a}: α = {d2(al)}.', f'B1 tan α = {b}/{a} from comparing coefficients; B1 α = {d2(al)}')
    m = int(R) + r.randint(2, 6)
    stem = f'{nm} says that the greatest value of {m}/({m} + {expr}) is {m}/({m} + {sqrt_str(a * a + b * b)}). Explain the error and state the correct greatest value.'
    return Q(stem, f'The fraction is greatest when the denominator is least, i.e. when {expr} takes its least value −{sqrt_str(a * a + b * b)}. Greatest value = {m}/({m} − {sqrt_str(a * a + b * b)}) = {n3(m / (m - R))}.',
             f'B1 denominator must be least; B1 {m}/({m} − {sqrt_str(a * a + b * b)}) ≈ {n3(m / (m - R))}')


@t34.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t34_calc(r, D):
    kind, a, b, R, al, expr, form, fn, sg_ = rform(r)
    Rs = sqrt_str(a * a + b * b)
    if D == 1:
        return Q(f'Express {expr} in the form {form}, where R > 0 and 0° < α < 90°. Give the exact value of R and the value of α correct to 2 decimal places.', f'{rsub(form, R, al)}',
                 f'B1 R = {Rs}; M1 tan α = {b}/{a}; A1 α = {d2(al)}')
    if D in (2, 3):
        c = round(r.uniform(-0.9, 0.9) * R, 1) if D == 3 else r.choice([x for x in range(-int(R), int(R) + 1) if x])
        if c == 0:
            return None
        xs = r_solve(kind, R, al, c)
        if not xs:
            return None
        # verify
        if not all(ok(r_eval(kind, R, al, x), c, 'R form') for x in xs):
            return None
        return Q(f'Express {expr} in the form {form}, where R > 0 and 0° < α < 90°. Hence solve the equation {expr} = {num(c)} for 0° ≤ θ ≤ 360°.', f'{rsub(form, R, al)}; θ = {angs(xs)}',
                 f'B1 R = {Rs}; M1 tan α = {b}/{a}; A1 α = {d2(al)}; M1 {fn}(θ {"+" if sg_ > 0 else "−"} α) = {num(c)}/{Rs}; A1 {angs(xs)}')
    if D == 4:
        m = int(R) + r.randint(1, 6)
        k = r.randint(2, 30)
        mx, mn = k / (m - R), k / (m + R)
        # θ at which the denominator is least: expression = −R
        th = r_solve(kind, R, al, -R * (1 - 1e-12))
        return Q(f'Express {expr} in the form {form}, where R > 0 and 0° < α < 90°. Hence find the greatest and least values of {k}/({m} + {expr}) as θ varies.',
                 f'{rsub(form, R, al)}; greatest {n3(mx)}, least {n3(mn)}', f'B1 R = {Rs}; A1 α = {d2(al)}; M1 uses {expr} varies from −{Rs} to {Rs}; A1 greatest {k}/({m} − {Rs}) = {n3(mx)}; A1 least {k}/({m} + {Rs}) = {n3(mn)}')
    c = round(r.uniform(-0.9, 0.9) * R, 1)
    xs = r_solve(kind, R, al, c, 0, 180, 2)
    expr2 = expr.replace('θ', '2θ')
    if not xs or not all(ok(r_eval(kind, R, al, 2 * x), c, 'R form 2') for x in xs):
        return None
    return Q(f'Express {expr} in the form {form}, where R > 0 and 0° < α < 90°. Hence solve the equation {expr2} = {num(c)} for 0° ≤ θ ≤ 180°.', f'{rsub(form, R, al)}; θ = {angs(xs)}',
             f'B1 R = {Rs}; A1 α = {d2(al)}; M1 {fn}(2θ {"+" if sg_ > 0 else "−"} α) = {num(c)}/{Rs}; M1 correct order of operations for 2θ; A1 {angs(xs)}')


def t34_c4(r, D):
    kind, a, b, R, al, expr, form, fn, sg_ = rform(r)
    Rs = sqrt_str(a * a + b * b)
    c = round(r.uniform(-0.9, 0.9) * R, 1) or 1
    xs = r_solve(kind, R, al, c)
    if not xs:
        return None
    m = int(R) + r.randint(1, 5)
    # θ for maximum of expression in [0, 360)
    thmax = r_solve(kind, R, al, R * (1 - 1e-12))
    intro = f'The expression f(θ) is defined by f(θ) = {expr}, for 0° ≤ θ ≤ 360°.'
    parts = [
        P(f'Express f(θ) in the form {form}, where R > 0 and 0° < α < 90°, giving α correct to 2 decimal places.', rsub(form, R, al), f'B1 R = {Rs}; M1 tan α = {b}/{a}; A1 α = {d2(al)}'),
        P(f'Solve the equation f(θ) = {num(c)}.', angs(xs), f'M1 {fn}(θ {"+" if sg_ > 0 else "−"} α) = {num(c)}/{Rs}; A1 first angle; A1 second angle'),
        P(f'State the greatest value of {m} − f(θ) and the least value of {m} − f(θ).', f'greatest {m} + {Rs}, least {m} − {Rs}', f'B1 {m} + {Rs}; B1 {m} − {Rs}'),
    ]
    if thmax:
        parts.append(P('Find the value of θ for which f(θ) is greatest.', d1(round(thmax[0], 4) % 360), f'M1 sets the angle equal to {"90°" if fn == "sin" else "0°"}; A1 {d1(round(thmax[0], 4) % 360)}'))
    return cmp_(r, intro, parts)


t34.add('C4', (2, 3, 4, 5))(t34_c4)

CHAPTERS[3] = [t31, t32, t33, t34]


# ================================================================ Chapter 4 Differentiation

def xpow(n, v='x'):
    n = Fr(n)
    if n == 0:
        return ''
    if n == 1:
        return v
    if n.denominator == 1:
        return v + sup(int(n))
    return f'{v}^({num(n)})'


def trigarg(k, v='x', b=0):
    k = Fr(k)
    s = (('' if k == 1 else (MINUS if k == -1 else num(k))) + v) if k.denominator == 1 else f'({num(k)}){v}'
    if b:
        return f'({s}{sg(b)})'
    return s if k == 1 else s


def prod_family(r, D):
    """Product/quotient rule functions: (y text, dy/dx text, f, f')."""
    kind = r.choice(['xe', 'xln', 'xsin', 'xcos', 'quot', 'equot', 'lnq'])
    n = r.randint(1, 4) if D >= 2 else r.randint(1, 3)
    k = nz(r, -3, 3)
    if kind == 'xe':
        y = f'{xpow(n)}{ex(k)}'
        dy = f'{xpow(n - 1)}{ex(k)}({lin(k, n)})' if n > 1 else f'{ex(k)}({lin(k, 1)})'
        f = lambda x: x ** n * math.exp(k * x)
        fp = lambda x: x ** (n - 1) * math.exp(k * x) * (n + k * x)
    elif kind == 'xln':
        y = f'{xpow(n)} ln x'
        dy = f'{xpow(n - 1)}({n} ln x + 1)' if n > 1 else 'ln x + 1'
        f = lambda x: x ** n * math.log(x)
        fp = lambda x: x ** (n - 1) * (n * math.log(x) + 1)
    elif kind in ('xsin', 'xcos'):
        k = abs(k)
        fn = kind[1:]
        y = f'{xpow(n)} {fn} {trigarg(k)}'
        c1 = f'{"" if n == 1 else n}{xpow(n - 1)}'
        c2 = f'{"" if k == 1 else k}{xpow(n)}'
        if fn == 'sin':
            dy = f'{c1 or "1"} sin {trigarg(k)} + {c2} cos {trigarg(k)}' if c1 else f'sin {trigarg(k)} + {c2} cos {trigarg(k)}'
            f = lambda x: x ** n * math.sin(k * x)
            fp = lambda x: n * x ** (n - 1) * math.sin(k * x) + k * x ** n * math.cos(k * x)
        else:
            dy = f'{c1} cos {trigarg(k)} − {c2} sin {trigarg(k)}' if c1 else f'cos {trigarg(k)} − {c2} sin {trigarg(k)}'
            f = lambda x: x ** n * math.cos(k * x)
            fp = lambda x: n * x ** (n - 1) * math.cos(k * x) - k * x ** n * math.sin(k * x)
    elif kind == 'quot':
        a, b, c, d = r.randint(1, 6), nz(r, -7, 7), r.randint(1, 5), nz(r, -7, 7)
        if a * d - b * c == 0:
            return None
        y = f'({lin(a, b)})/({lin(c, d)})'
        dy = f'{num(a * d - b * c)}/({lin(c, d)})²'
        f = lambda x: (a * x + b) / (c * x + d)
        fp = lambda x: (a * d - b * c) / (c * x + d) ** 2
    elif kind == 'equot':
        a = nz(r, -4, 4)
        y = f'{ex(k)}/(x{sg(a)})'
        dy = f'{ex(k)}({lin(k, k * a - 1)})/(x{sg(a)})²'
        f = lambda x: math.exp(k * x) / (x + a)
        fp = lambda x: math.exp(k * x) * (k * (x + a) - 1) / (x + a) ** 2
    else:
        y = f'(ln x)/{xpow(n)}'
        dy = f'(1 − {"" if n == 1 else n}ln x)/{xpow(n + 1)}'.replace('− ln', '− ln')
        f = lambda x: math.log(x) / x ** n
        fp = lambda x: (1 - n * math.log(x)) / x ** (n + 1)
    for x0 in (0.7, 1.3, 2.1):
        try:
            if not ok(ndiff(f, x0), fp(x0), 'prod ' + kind, 1e-5):
                return None
        except (ValueError, ZeroDivisionError):
            pass
    return kind, y, dy, f, fp


d41 = T('Product and quotient rules', 'product and quotient rules', 'quotient rule')
d41.fixed('C1', (1, 2), [
    ('Which is the product rule for y = uv?', 'dy/dx = u dv/dx + v du/dx', 'Differentiate each factor in turn, keeping the other fixed.', ['dy/dx = (du/dx)(dv/dx)', 'dy/dx = u dv/dx − v du/dx', 'dy/dx = (v du/dx − u dv/dx)/v²']),
    ('Which is the quotient rule for y = u/v?', 'dy/dx = (v du/dx − u dv/dx)/v²', 'Standard quotient rule.', ['dy/dx = (u dv/dx − v du/dx)/v²', 'dy/dx = (du/dx)/(dv/dx)', 'dy/dx = (v du/dx + u dv/dx)/v²']),
    ('Differentiate y = x eˣ.', 'eˣ(1 + x)', 'Product rule: 1 × eˣ + x eˣ.', ['eˣ', 'x eˣ', 'eˣ + x']),
])
d41.fixed('C2', (2, 3), [
    ('Explain why d/dx(x² sin x) is not equal to 2x cos x.', 'x² sin x is a product, so the product rule is needed: 2x sin x + x² cos x. Multiplying the separate derivatives is not valid.', 'B1 product needs product rule; B1 correct derivative 2x sin x + x² cos x [2]'),
    ('Show, using the quotient rule, that the derivative of tan x = sin x/cos x is sec²x.', '(cos x cos x − sin x(−sin x))/cos²x = (cos²x + sin²x)/cos²x = 1/cos²x = sec²x.', 'M1 quotient rule correctly applied; A1 uses cos²x + sin²x = 1 [2]'),
])


@d41.add('C1', (1, 2, 3))
def d41_c1(r, D):
    fam = prod_family(r, D)
    if not fam:
        return None
    kind, y, dy, f, fp = fam
    wrong = {'xe': f'{"" if True else ""}{xpow(1) if False else ""}', 'xln': '', 'xsin': '', 'xcos': '', 'quot': '', 'equot': '', 'lnq': ''}
    # distractors: one-term derivatives and sign slips
    ds = []
    if kind == 'quot':
        num_ = dy.split('/')[0]
        ds = [f'{num(-Fr(num_.replace(MINUS, "-")))}{dy[len(num_):]}', dy.replace('²', ''), f'{num_}/{dy.split("/(")[1][:-2]}' if '/(' in dy else dy + '²', dy.replace('²', '³')]
    else:
        ds = [dy.replace(' + ', ' − ', 1) if ' + ' in dy else dy.replace(' − ', ' + ', 1), dy.replace('+ 1)', ')').replace('(1 − ', '(1 + '), y.replace(' ln x', '').replace('ln x', '1/x') + ' ln x' if 'ln' in y else dy.split('(')[0] + '(' + dy.split('(')[1].split(' ')[0] + ')' if '(' in dy else y]
        ds += [y, dy + ' + 1']
    return MC(r, f'Differentiate y = {y} with respect to x.', dy, ds, f'{"Quotient" if "/" in y else "Product"} rule: dy/dx = {dy}.')


@d41.add('C2', (1, 2, 3, 4), 'explain')
def d41_err(r, D):
    nm = person(r)
    f = r.choice(['prod', 'quot'])
    if f == 'prod':
        n, k = r.randint(2, 4), nz(r, -3, 3)
        wrong = f'{coefk(n * k).strip()}{xpow(n - 1)}{ex(k)}'
        right = f'{xpow(n - 1)}{ex(k)}({lin(k, n)})'
        stem = f'{nm} differentiates y = {xpow(n)}{ex(k)} and writes dy/dx = {n}{xpow(n - 1)} × {coefk(k).strip()}{ex(k)} = {wrong}. Explain the error and find the correct derivative.'
        return Q(stem, f'The derivative of a product is not the product of the derivatives. Using the product rule: dy/dx = {tsum([(n, xpow(n - 1) + ex(k)), (k, xpow(n) + ex(k))])} = {right}.',
                 f'B1 product rule required; B1 dy/dx = {right}')
    a, b, c, d = r.randint(1, 6), nz(r, -7, 7), r.randint(1, 5), nz(r, -7, 7)
    if a * d - b * c == 0:
        return None
    stem = f'{nm} differentiates y = ({lin(a, b)})/({lin(c, d)}) using the quotient rule and obtains dy/dx = {num(b * c - a * d)}/({lin(c, d)})². Explain the error and give the correct derivative.'
    return Q(stem, f'The numerator should be v du/dx − u dv/dx = {coefk(a).strip()}({lin(c, d)}) − {coefk(c).strip()}({lin(a, b)}) = {num(a * d - b * c)}; {nm} subtracted in the wrong order. dy/dx = {num(a * d - b * c)}/({lin(c, d)})².',
             f'B1 order of subtraction v du/dx − u dv/dx; B1 {num(a * d - b * c)}/({lin(c, d)})²')


@d41.add('C3', (1, 2, 3, 4, 5), 'numerical')
def d41_calc(r, D):
    if D <= 2:
        fam = prod_family(r, D)
        if not fam:
            return None
        kind, y, dy, f, fp = fam
        if D == 1:
            return Q(f'Differentiate y = {y} with respect to x.', f'dy/dx = {dy}', f'M1 {"quotient" if "/" in y else "product"} rule with both terms; A1 dy/dx = {dy}')
        x0 = r.choice([0.5, 1, 1.5, 2, 3]) if kind not in ('quot', 'equot') else r.choice([0, 1, 2, 3, -1])
        try:
            g = fp(x0)
            f(x0)
        except (ValueError, ZeroDivisionError):
            return None
        return Q(f'Find the gradient of the curve y = {y} at the point where x = {num(x0)}, giving your answer correct to 3 significant figures where appropriate.', fx(g),
                 f'M1 {"quotient" if "/" in y else "product"} rule; A1 dy/dx = {dy}; A1 {fx(g)}')
    if D == 3:
        n, k = r.randint(1, 4), nz(r, -3, 3)
        xs = -Fr(n, k)
        yv = float(xs) ** n * math.exp(k * float(xs))
        if not ok(fp_xe(n, k, float(xs)), 0, 'xe stat'):
            return None
        pts = [f'({num(xs)}, {n3(yv)})'] + (['(0, 0)'] if n > 1 else [])
        return Q(f'Find the coordinates of the stationary points of the curve y = {xpow(n)}{ex(k)}, giving the y-coordinates correct to 3 significant figures.',
                 ' and '.join(pts), f'M1 product rule; A1 {xpow(n - 1)}{ex(k)}({lin(k, n)}); M1 sets = 0 ({ex(k)} ≠ 0); A1 ' + ' and '.join(pts))
    if D == 4:
        a, b, c, d = r.randint(1, 6), nz(r, -7, 7), r.randint(1, 5), nz(r, -7, 7)
        x0 = r.randint(-2, 3)
        if a * d - b * c == 0 or c * x0 + d == 0:
            return None
        m = Fr(a * d - b * c, (c * x0 + d) ** 2)
        y0 = Fr(a * x0 + b, c * x0 + d)
        cc = y0 - m * x0
        return Q(f'Find the equation of the tangent to the curve y = ({lin(a, b)})/({lin(c, d)}) at the point where x = {x0}, giving your answer in the form y = mx + c.',
                 f'y = {poly([(m, 1), (cc, 0)])}', f'M1 quotient rule; A1 dy/dx = {num(a * d - b * c)}/({lin(c, d)})²; A1 gradient {num(m)} at ({x0}, {num(y0)}); M1 line through the point; A1 y = {poly([(m, 1), (cc, 0)])}')
    k = r.choice([1, 2, 3, Fr(1, 2)])
    a = nz(r, -4, 4)
    xs = 1 / Fr(k) - a
    if xs + a == 0:
        return None
    ys = math.exp(float(k * xs)) / float(xs + a)
    # nature: f'' sign by numerical second derivative
    F = lambda x: math.exp(float(k) * x) / (x + a)
    f2 = (F(float(xs) + 1e-3) - 2 * F(float(xs)) + F(float(xs) - 1e-3)) / 1e-6
    nat = 'minimum' if f2 > 0 else 'maximum'
    return Q(f'The curve y = {ex(k)}/(x{sg(a)}) has one stationary point. Find its coordinates, giving the y-coordinate correct to 3 significant figures, and determine its nature.',
             f'({num(xs)}, {n3(ys)}); {nat}', f'M1 quotient rule; A1 {ex(k)}({lin(k, k * a - 1)})/(x{sg(a)})²; M1 sets numerator = 0; A1 x = {num(xs)}, y = {n3(ys)}; B1 {nat} (sign of gradient either side or second derivative)')


def fp_xe(n, k, x):
    return x ** (n - 1) * math.exp(k * x) * (n + k * x)


def d41_c4(r, D):
    n = r.randint(1, 3)
    k = -r.randint(1, 3)
    xs = Fr(n, -k)
    ysv = float(xs) ** n * math.exp(k * float(xs))
    x1 = r.choice([x for x in (1, 2, 3) if x != xs])
    g1 = fp_xe(n, k, x1)
    y1 = x1 ** n * math.exp(k * x1)
    intro = f'The curve C has equation y = {xpow(n)}{ex(k)}.'
    parts = [
        P('Find dy/dx.', f'{xpow(n - 1)}{ex(k)}({lin(k, n)})', f'M1 product rule; A1 {xpow(n - 1)}{ex(k)}({lin(k, n)})'),
        P('Find the exact coordinates of the stationary point of C for which x > 0.', f'({num(xs)}, {cexp(xs ** n, -n)})', f'M1 sets dy/dx = 0; A1 x = {num(xs)}; A1 y = {cexp(xs ** n, -n)}'),
        P(f'Find the equation of the tangent to C at the point where x = {x1}, giving numerical coefficients correct to 3 significant figures.',
          line3(g1, y1 - g1 * x1), f'M1 gradient {n3(g1)}; M1 y − {n3(y1)} = {n3(g1)}(x − {x1}); A1 {line3(g1, y1 - g1 * x1)}'),
        P('Describe the behaviour of y as x → ∞.', 'y → 0', f'B1 {ex(k)} → 0 faster than {xpow(n)} grows, so y → 0'),
    ]
    return cmp_(r, intro, parts)


def cexp(c, k):
    c = Fr(c)
    e = ek(k)
    if c == 1:
        return e
    return (num(c) if c.denominator == 1 else f'({num(c)})') + e


d41.add('C4', (2, 3, 4, 5))(d41_c4)


# ---------------------------------------------------------------- 4.2 standard derivatives

def std_family(r):
    kind = r.choice(['exp', 'ln', 'sin', 'cos', 'tan', 'lnq', 'sin2', 'expq'])
    a, b = nz(r, -5, 5), nz(r, -6, 6)
    if kind == 'exp':
        y, dy = ex(a, b), f'{num(a)}{ex(a, b)}'.replace(f'{MINUS}1e', MINUS + 'e').replace('1e', 'e', 1) if abs(a) == 1 else f'{num(a)}{ex(a, b)}'
        f, fp = (lambda x: math.exp(a * x + b)), (lambda x: a * math.exp(a * x + b))
    elif kind == 'ln':
        a = abs(a)
        y, dy = f'ln({lin(a, b)})', f'{a}/({lin(a, b)})'
        f, fp = (lambda x: math.log(a * x + b)), (lambda x: a / (a * x + b))
    elif kind in ('sin', 'cos'):
        a = abs(a)
        y = f'{kind}({lin(a, b)})'
        if kind == 'sin':
            dy = f'{"" if a == 1 else a}cos({lin(a, b)})' if a != 1 else f'cos({lin(a, b)})'
            f, fp = (lambda x: math.sin(a * x + b)), (lambda x: a * math.cos(a * x + b))
        else:
            dy = f'{MINUS}{"" if a == 1 else a}sin({lin(a, b)})'
            f, fp = (lambda x: math.cos(a * x + b)), (lambda x: -a * math.sin(a * x + b))
        dy = dy.replace(f'{a}cos', f'{a} cos').replace(f'{a}sin', f'{a} sin')
    elif kind == 'tan':
        a = abs(a)
        y, dy = f'tan {trigarg(a)}', f'{"" if a == 1 else str(a) + " "}sec²{trigarg(a)}'
        f, fp = (lambda x: math.tan(a * x)), (lambda x: a / math.cos(a * x) ** 2)
    elif kind == 'lnq':
        c = r.randint(1, 9)
        y, dy = f'ln(x² + {c})', f'2x/(x² + {c})'
        f, fp = (lambda x: math.log(x * x + c)), (lambda x: 2 * x / (x * x + c))
    elif kind == 'sin2':
        y, dy = 'sin²x', '2 sin x cos x (= sin 2x)'
        f, fp = (lambda x: math.sin(x) ** 2), (lambda x: math.sin(2 * x))
    else:
        c = abs(a)
        y, dy = f'e^({poly([(1, 2), (b, 1)])})', f'({lin(2, b)})e^({poly([(1, 2), (b, 1)])})'
        f, fp = (lambda x: math.exp(x * x + b * x)), (lambda x: (2 * x + b) * math.exp(x * x + b * x))
    for x0 in (0.3, 0.9, 1.4):
        try:
            if not ok(ndiff(f, x0), fp(x0), 'std ' + kind, 1e-5):
                return None
        except (ValueError, ZeroDivisionError):
            pass
    return kind, y, dy, f, fp


d42 = T('Derivatives of eˣ, ln x, sin x, cos x and tan x', 'derivatives of eˣ, ln x', 'derivative of tan x')
d42.fixed('C1', (1, 2), [
    ('What is the derivative of ln x?', '1/x', 'Standard result.', ['ln x', 'eˣ', 'x ln x − x']),
    ('What is the derivative of tan x?', 'sec²x', 'Standard result (x in radians).', ['sec x tan x', '−cosec²x', 'cot x']),
    ('Why must x be measured in radians when we use d/dx(sin x) = cos x?', 'The result relies on sin h/h → 1 as h → 0, which is true only in radians', 'In degrees an extra factor π/180 appears.', ['Degrees are not accurate enough', 'Calculators only work in radians', 'cos x is undefined in degrees']),
    ('What is the derivative of e^(5x)?', '5e^(5x)', 'Chain rule: multiply by 5.', ['e^(5x)', '5x e^(5x − 1)', 'e^(5x)/5']),
])
d42.fixed('C2', (2, 3), [
    ('Explain why d/dx(ln 7x) = d/dx(ln x).', 'ln 7x = ln 7 + ln x, and ln 7 is a constant with derivative 0, so both derivatives equal 1/x.', 'B1 ln 7x = ln 7 + ln x; B1 constant differentiates to 0 [2]'),
    ('Explain why the curve y = eˣ − x has a stationary point at x = 0 and determine its nature.', 'dy/dx = eˣ − 1 = 0 when eˣ = 1, i.e. x = 0; d²y/dx² = eˣ = 1 > 0 so it is a minimum.', 'B1 eˣ − 1 = 0 gives x = 0; B1 second derivative positive, minimum [2]'),
])


@d42.add('C1', (1, 2, 3))
def d42_c1(r, D):
    kind, y, dy, f, fp = std_family(r)
    ds = [y, dy.replace(MINUS, '', 1) if dy.startswith(MINUS) else MINUS + dy]
    if kind == 'sin2':
        ds = ['2 sin x', 'cos²x', '2 cos x', f'{MINUS}2 sin x cos x']
    elif kind == 'exp':
        ds.append(ex(1, 0) if False else f'{ex(r.choice([1, 2]), 0)}')
        ds.append(f'{y}/{num(abs(Fr(dy.split("e")[0].replace(MINUS, "-") or 1)))}' if dy[0] != 'e' else y + ' + 1')
    elif kind == 'ln':
        ds += [f'1/({y[3:-1]})', f'{y[3]}/x' if y[3].isdigit() else '1/x']
    elif kind in ('sin', 'cos'):
        ds += [dy.replace('cos', 'X').replace('sin', 'cos').replace('X', 'sin'), f'{"cos" if kind == "sin" else MINUS + "sin"}({y[4:-1]})']
    else:
        ds += [dy + ' + 1', dy.replace('2', '', 1)]
    return MC(r, f'Find dy/dx when y = {y}.', dy, ds, f'Chain rule: dy/dx = {dy}.')


@d42.add('C2', (1, 2, 3, 4), 'explain')
def d42_err(r, D):
    nm = person(r)
    f = r.choice(['chain', 'ln', 'deg'])
    if f == 'chain':
        a, b = r.randint(2, 6), nz(r, -6, 6)
        fn = r.choice(['sin', 'cos', 'e'])
        if fn == 'e':
            y, wrong, right = ex(a, b), ex(a, b), f'{a}{ex(a, b)}'
        else:
            y = f'{fn}({lin(a, b)})'
            wrong = ('cos' if fn == 'sin' else MINUS + 'sin') + f'({lin(a, b)})'
            right = (f'{a} cos' if fn == 'sin' else f'{MINUS}{a} sin') + f'({lin(a, b)})'
        stem = f'{nm} writes d/dx({y}) = {wrong}. Explain the error and write down the correct derivative.'
        return Q(stem, f'The chain rule requires multiplying by the derivative of the inner function {lin(a, b)}, which is {a}. Correct: {right}.', f'B1 chain rule factor {a} missing; B1 {right}')
    if f == 'ln':
        a, b = r.randint(2, 9), nz(r, -9, 9)
        stem = f'{nm} writes d/dx(ln({lin(a, b)})) = 1/({lin(a, b)}). Explain the error and correct it.'
        return Q(stem, f'By the chain rule d/dx ln(u) = u′/u, and u′ = {a}. Correct: {a}/({lin(a, b)}).', f'B1 multiply by derivative of inner function; B1 {a}/({lin(a, b)})')
    a = r.choice([30, 45, 60, 20, 50])
    stem = f'{nm} finds the gradient of y = sin x at x = {a}° by evaluating cos {a}° = {n3(math.cos(math.radians(a)))}. Explain why this is not the gradient when x is measured in degrees, and state the correct gradient.'
    g = math.pi / 180 * math.cos(math.radians(a))
    return Q(stem, f'd/dx(sin x) = cos x only when x is in radians. In degrees, sin x° = sin(πx/180), so the gradient is (π/180) cos {a}° = {n3(g)}.',
             f'B1 result valid only in radians; B1 gradient (π/180) cos {a}° = {n3(g)}')


@d42.add('C3', (1, 2, 3, 4, 5), 'numerical')
def d42_calc(r, D):
    if D == 1:
        kind, y, dy, f, fp = std_family(r)
        return Q(f'Differentiate {y} with respect to x.', dy, f'M1 correct form; A1 {dy}')
    if D == 2:
        kind, y, dy, f, fp = std_family(r)
        x0 = r.choice([0, 0.5, 1, 2]) if kind not in ('ln',) else r.choice([1, 2, 3])
        try:
            g = fp(x0)
            f(x0)
        except (ValueError, ZeroDivisionError):
            return None
        return Q(f'Find the gradient of the curve y = {y} at the point where x = {num(x0)}, giving your answer correct to 3 significant figures where appropriate.', fx(g), f'M1 dy/dx = {dy}; A1 {fx(g)}')
    if D == 3:
        a = r.choice([1, 2, 3])
        k = r.choice([x for x in range(2, 10) if x != a])
        xs = math.log(k / a) / a
        ys = math.exp(a * xs) - k * xs
        exact_x = lnr(Fr(k, a)) if a == 1 else f'(1/{a}) {lnr(Fr(k, a))}'
        return Q(f'Find the exact x-coordinate of the stationary point of the curve y = {ex(a)} − {k}x, and determine whether it is a maximum or a minimum.', f'x = {exact_x}; minimum',
                 f'M1 dy/dx = {"" if a == 1 else a}{ex(a)} − {k}; A1 x = {exact_x}; M1 d²y/dx² = {a * a if a > 1 else ""}{ex(a)} > 0; A1 minimum')
    if D == 4:
        a, b = r.randint(1, 6), nz(r, -5, 5)
        x0 = r.randint(1, 4)
        if a * x0 + b <= 0:
            return None
        m = Fr(a, a * x0 + b)
        y0 = math.log(a * x0 + b)
        nm_ = -1 / m
        return Q(f'Find the equation of the normal to the curve y = ln({lin(a, b)}) at the point where x = {x0}. Give your answer in the form y = mx + c, with c correct to 3 significant figures.',
                 f'y = {poly([(nm_, 1)])}{sg3(y0 - float(nm_) * x0)}',
                 f'M1 dy/dx = {a}/({lin(a, b)}); A1 tangent gradient {num(m)}; M1 normal gradient {num(nm_)}; A1 y − {n3(y0)} = {num(nm_)}(x − {x0}) leading to the given form')
    a, b = r.randint(1, 6), r.randint(1, 6)
    # y = a sin x + b cos x on 0 < x < π/2 has a maximum where tan x = a/b
    xs = math.atan2(a, b)
    ys = math.hypot(a, b)
    return Q(f'Find the x-coordinate of the stationary point of y = {coefk(a)}sin x + {coefk(b)}cos x for 0 < x < π/2, giving your answer correct to 3 significant figures, and show that it is a maximum.',
             f'x = {n3(xs)}; maximum (y = {sqrt_str(a * a + b * b)})', f'M1 dy/dx = {coefk(a)}cos x − {coefk(b)}sin x; M1 tan x = {num(Fr(a, b))}; A1 x = {n3(xs)}; M1 d²y/dx² = −y < 0; A1 maximum')


def d42_c4(r, D):
    k = r.randint(2, 9)
    xs = math.log(k)
    ys = k - k * math.log(k)
    x1 = r.choice([0, 1, 2])
    g1 = math.exp(x1) - k
    y1 = math.exp(x1) - k * x1
    intro = f'The curve C has equation y = eˣ − {k}x.'
    parts = [
        P('Find dy/dx and d²y/dx².', f'dy/dx = eˣ − {k}; d²y/dx² = eˣ', 'B1 dy/dx; B1 d²y/dx²'),
        P('Find the exact coordinates of the stationary point of C.', f'(ln {k}, {k} − {k} ln {k})', f'M1 eˣ = {k}; A1 x = ln {k}; A1 y = {k} − {k} ln {k}'),
        P('Determine the nature of the stationary point.', 'minimum', 'M1 d²y/dx² = eˣ > 0; A1 minimum'),
        P(f'Find the gradient of C at the point where x = {x1}, giving your answer correct to 3 significant figures.', fx(g1), f'B1 {fx(g1)}'),
        P('Explain why C has no points of inflection.', 'd²y/dx² = eˣ > 0 for all x, so it is never zero and the curve is always concave upwards.', 'B1 eˣ never zero'),
    ]
    return cmp_(r, intro, parts)


d42.add('C4', (2, 3, 4, 5))(d42_c4)


# ---------------------------------------------------------------- 4.3 implicit differentiation

def implicit_curve(r):
    kind = r.choice(['quad', 'quad', 'cube', 'lny'])
    p, q = nz(r, -4, 4), nz(r, -4, 4)
    if kind == 'quad':
        a, b = nz(r, -4, 4), r.randint(1, 3)
        c = p * p + a * p * q + b * q * q
        if c == 0:
            return None
        eq = f'x²{sg(a)}xy{sg(b) if b != 1 else " + "}y² = {c}'.replace(f'{sg(a)}xy', (' + ' if a > 0 else ' − ') + ('' if abs(a) == 1 else str(abs(a))) + 'xy').replace(' + 1y²', ' + y²')
        eq = f'x²{(" + " if a > 0 else " − ") + ("" if abs(a) == 1 else str(abs(a)))}xy + {"" if b == 1 else b}y² = {c}'
        Nx = lambda x, y: -(2 * x + a * y)
        Dx = lambda x, y: (a * x + 2 * b * y)
        dytxt = f'−({lin(2, 0)}{sg(a)}y)/({lin(a, 0)} + {2 * b}y)'.replace(f'{sg(a)}y', (' + ' if a > 0 else ' − ') + ('' if abs(a) == 1 else str(abs(a))) + 'y')
        dytxt = f'−(2x {"+" if a > 0 else "−"} {"" if abs(a) == 1 else abs(a)}y)/({"" if a == 1 else (MINUS if a == -1 else a)}x + {2 * b}y)'
        F = lambda x, y: x * x + a * x * y + b * y * y - c
        return kind, eq, dytxt, Nx, Dx, (p, q), F
    if kind == 'cube':
        c = p * p * q + q ** 3
        if c == 0:
            return None
        eq = f'x²y + y³ = {c}'
        Nx = lambda x, y: -2 * x * y
        Dx = lambda x, y: x * x + 3 * y * y
        F = lambda x, y: x * x * y + y ** 3 - c
        return kind, eq, '−2xy/(x² + 3y²)', Nx, Dx, (p, q), F
    eq = f'xy + ln y = {p}'
    Nx = lambda x, y: -y * y
    Dx = lambda x, y: x * y + 1
    F = lambda x, y: x * y + math.log(y) - p
    return kind, eq, '−y²/(xy + 1)', Nx, Dx, (p, 1), F


def implicit_grad(c):
    kind, eq, dytxt, Nx, Dx, (p, q), F = c
    d = Dx(p, q)
    if d == 0:
        return None
    g = Fr(Nx(p, q), d)
    # numeric check: implicit function theorem via partial derivatives
    h = 1e-6
    Fx = (F(p + h, q) - F(p - h, q)) / (2 * h)
    Fy = (F(p, q + h) - F(p, q - h)) / (2 * h)
    if abs(F(p, q)) > 1e-9 or abs(Fy) < 1e-9 or not ok(-Fx / Fy, float(g), 'implicit'):
        return None
    return g


d43 = T('Implicit differentiation', 'implicit differentiation', 'implicit')
d43.fixed('C1', (1, 2), [
    ('What is d/dx(y²)?', '2y dy/dx', 'Chain rule: d/dy(y²) × dy/dx.', ['2y', '2x', 'y² dy/dx']),
    ('What is d/dx(xy)?', 'y + x dy/dx', 'Product rule.', ['x dy/dx', 'dy/dx', 'xy dy/dx']),
    ('What is d/dx(ln y)?', '(1/y) dy/dx', 'Chain rule.', ['1/y', '1/x', 'ln y dy/dx']),
    ('What is d/dx(e^y)?', 'e^y dy/dx', 'Chain rule.', ['e^y', 'y e^(y − 1)', 'e^x']),
])
d43.fixed('C2', (2, 3), [
    ('Explain why, when differentiating y³ with respect to x, the result is 3y² dy/dx rather than 3y².', 'y is a function of x, so by the chain rule d/dx(y³) = d/dy(y³) × dy/dx = 3y² dy/dx.', 'B1 y depends on x; B1 chain rule gives the factor dy/dx [2]'),
    ('Explain how to find the points on an implicitly defined curve where the tangent is parallel to the y-axis.', 'The tangent is vertical where dy/dx is undefined, i.e. where the denominator of dy/dx is zero (and the numerator is not); solve this with the curve equation.', 'B1 denominator of dy/dx = 0; B1 solve simultaneously with the curve equation [2]'),
])


@d43.add('C1', (1, 2, 3))
def d43_c1(r, D):
    if D == 1:
        n = r.randint(2, 5)
        k = r.randint(2, 6)
        return MC(r, f'Find d/dx({k}y{sup(n)}).', f'{k * n}y{sup(n - 1) if n > 2 else ""} dy/dx', [f'{k * n}y{sup(n - 1) if n > 2 else ""}', f'{k * n}x{sup(n - 1) if n > 2 else ""}', f'{k}y{sup(n)} dy/dx'],
                  f'Chain rule: {k * n}y{sup(n - 1) if n > 2 else ""} dy/dx.')
    if D == 2:
        a, n = r.randint(2, 6), r.randint(2, 3)
        return MC(r, f'Find d/dx({a}x{"" if n == 1 else sup(n)}y).', f'{a * n}x{sup(n - 1) if n > 2 else ""}y + {a}x{sup(n)} dy/dx',
                  [f'{a * n}x{sup(n - 1) if n > 2 else ""} dy/dx', f'{a}x{sup(n)} dy/dx', f'{a * n}x{sup(n - 1) if n > 2 else ""}y'], 'Product rule with d/dx(y) = dy/dx.')
    c = implicit_curve(r)
    if not c:
        return None
    g = implicit_grad(c)
    if g is None:
        return None
    p, q = c[5]
    return MC(r, f'Find the gradient of the curve {c[1]} at the point ({p}, {q}).', num(g), [num(-g), num(1 / g) if g else '1', num(-1 / g) if g else '−1', num(g + 1)], f'dy/dx = {c[2]} = {num(g)} at ({p}, {q}).')


@d43.add('C2', (1, 2, 3, 4), 'explain')
def d43_err(r, D):
    nm = person(r)
    a, b = r.randint(2, 6), r.randint(2, 6)
    n = r.randint(2, 4)
    f = r.choice(['dydx', 'prod'])
    if f == 'dydx':
        stem = f'{nm} differentiates {a}x² + {b}y{sup(n)} = 20 implicitly and writes {2 * a}x + {b * n}y{sup(n - 1) if n > 2 else ""} = 0. Explain the error and find dy/dx correctly.'
        return Q(stem, f'd/dx({b}y{sup(n)}) = {b * n}y{sup(n - 1) if n > 2 else ""} dy/dx (chain rule). So dy/dx = −{2 * a}x/({b * n}y{sup(n - 1) if n > 2 else ""}).',
                 f'B1 missing dy/dx factor from the chain rule; B1 dy/dx = −{2 * a}x/({b * n}y{sup(n - 1) if n > 2 else ""})')
    stem = f'{nm} differentiates {a}xy = x² + {b} implicitly and writes {a}x dy/dx = 2x. Explain the error and find dy/dx in terms of x and y.'
    return Q(stem, f'{a}xy is a product, so its derivative is {a}y + {a}x dy/dx. Then {a}y + {a}x dy/dx = 2x, so dy/dx = (2x − {a}y)/({a}x).', f'B1 product rule needed for xy; B1 dy/dx = (2x − {a}y)/({a}x)')


@d43.add('C3', (1, 2, 3, 4, 5), 'numerical')
def d43_calc(r, D):
    c = implicit_curve(r)
    if not c:
        return None
    kind, eq, dytxt, Nx, Dx, (p, q), F = c
    g = implicit_grad(c)
    if g is None:
        return None
    if D == 1:
        return Q(f'The curve C has equation {eq}. Find dy/dx in terms of x and y.', f'dy/dx = {dytxt}', 'M1 differentiates implicitly (product rule and chain rule); A1 correct dy/dx')
    if D == 2:
        return Q(f'Find the gradient of the curve {eq} at the point ({p}, {q}).', num(g), f'M1 implicit differentiation; A1 dy/dx = {dytxt}; A1 {num(g)}')
    if D == 3:
        cc = q - g * p
        return Q(f'Find the equation of the tangent to the curve {eq} at the point ({p}, {q}). Give your answer in the form ax + by + c = 0.', gen_line(g, -1, cc),
                 f'M1 implicit differentiation; A1 dy/dx = {dytxt}; A1 gradient {num(g)}; A1 {gen_line(g, -1, cc)}')
    if D == 4:
        if g == 0:
            return None
        m = -1 / g
        cc = q - m * p
        return Q(f'Find the equation of the normal to the curve {eq} at the point ({p}, {q}). Give your answer in the form ax + by + c = 0.', gen_line(m, -1, cc),
                 f'M1 implicit differentiation; A1 tangent gradient {num(g)}; M1 normal gradient {num(m)}; A1 {gen_line(m, -1, cc)}')
    # points where tangent parallel to x-axis for x² + axy + by² = c: 2x + ay = 0
    for _ in range(80):
        a = r.choice([-4, -2, 2, 4])
        b = r.randint(1, 4)
        t = r.randint(1, 4)
        # y = -2x/a ; x² + a x(-2x/a) + b(4x²/a²) = c -> x²(-1 + 4b/a²) = c
        coefx = Fr(-1) + Fr(4 * b, a * a)
        if coefx <= 0:
            continue
        c = coefx * t * t
        if c.denominator != 1:
            continue
        c = int(c)
        pts = [(t, Fr(-2 * t, a)), (-t, Fr(2 * t, a))]
        break
    else:
        return None
    eq = f'x²{(" + " if a > 0 else " − ") + ("" if abs(a) == 1 else str(abs(a)))}xy + {"" if b == 1 else b}y² = {c}'
    for (x, y) in pts:
        if not ok(x * x + a * x * y + b * y * y, c, 'implicit horizontal'):
            return None
    return Q(f'Find the coordinates of the points on the curve {eq} at which the tangent is parallel to the x-axis.', ' and '.join(pt(x, y) for x, y in pts),
             f'M1 implicit differentiation; A1 dy/dx = −(2x {"+" if a > 0 else "−"} {abs(a)}y)/(…); M1 sets 2x {"+" if a > 0 else "−"} {abs(a)}y = 0 and substitutes into the curve; A1 x = ±{t}; A1 both points')


def gen_line(m, n_, c):
    from .g11_maths import gen_line as gl
    return gl(m, n_, c)


def d43_c4(r, D):
    c = None
    for _ in range(20):
        c = implicit_curve(r)
        if c and c[0] == 'quad' and implicit_grad(c) not in (None, 0):
            break
    else:
        return None
    kind, eq, dytxt, Nx, Dx, (p, q), F = c
    g = implicit_grad(c)
    cc = q - g * p
    m = -1 / g
    intro = f'The curve C has equation {eq}.'
    parts = [
        P(f'Verify that the point ({p}, {q}) lies on C.', 'Substitution gives the right-hand side.', 'B1 correct substitution shown'),
        P('Find dy/dx in terms of x and y.', f'dy/dx = {dytxt}', 'M1 product rule on the xy term; M1 chain rule on y²; A1 correct expression'),
        P(f'Find the equation of the tangent to C at ({p}, {q}), giving your answer in the form ax + by + c = 0.', gen_line(g, -1, cc), f'M1 gradient {num(g)}; A1 {gen_line(g, -1, cc)}'),
        P(f'Find the equation of the normal to C at ({p}, {q}).', gen_line(m, -1, q - m * p), f'M1 gradient {num(m)}; A1 {gen_line(m, -1, q - m * p)}'),
    ]
    return cmp_(r, intro, parts)


d43.add('C4', (2, 3, 4, 5))(d43_c4)


# ---------------------------------------------------------------- 4.4 parametric differentiation

def param_curve(r):
    kind = r.choice(['poly', 'poly', 'trig', 'exp'])
    if kind == 'poly':
        p, q, rr, s = nz(r, -3, 3), nz(r, -5, 5), nz(r, -2, 2), nz(r, -6, 6)
        xt = f'{"" if p == 1 else (MINUS if p == -1 else p)}t²{sg(q)}'
        yt = f'{"" if rr == 1 else (MINUS if rr == -1 else rr)}t³{sg(s)}t'.replace(' 1t', ' t')
        dx = lambda t: 2 * p * t
        dy = lambda t: 3 * rr * t * t + s
        X = lambda t: p * t * t + q
        Y = lambda t: rr * t ** 3 + s * t
        dytxt = f'({poly([(3 * rr, 2), (s, 0)], "t")})/({2 * p}t)'
        return kind, xt, yt, X, Y, dx, dy, dytxt, [1, 2, -1, 3, -2]
    if kind == 'trig':
        a, b = r.randint(1, 6), r.randint(1, 6)
        X = lambda t: a * math.cos(t)
        Y = lambda t: b * math.sin(t)
        dx = lambda t: -a * math.sin(t)
        dy = lambda t: b * math.cos(t)
        return kind, f'{coefk(a)}cos t', f'{coefk(b)}sin t', X, Y, dx, dy, f'−{num(Fr(b, a)) if Fr(b, a) != 1 else ""} cot t'.replace('− cot', '−cot'), [math.pi / 6, math.pi / 4, math.pi / 3, 2 * math.pi / 3]
    k = r.randint(1, 6)
    X = lambda t: math.exp(t)
    Y = lambda t: math.exp(2 * t) - k * t
    dx = lambda t: math.exp(t)
    dy = lambda t: 2 * math.exp(2 * t) - k
    return kind, 'eᵗ', f'e^(2t) − {coefk(k).strip()}t', X, Y, dx, dy, f'(2e^(2t) − {k})/eᵗ = 2eᵗ − {coefk(k).strip()}e⁻ᵗ', [0, 1, math.log(2), math.log(3)]


def tval(t):
    for v, s in ((math.pi / 6, 'π/6'), (math.pi / 4, 'π/4'), (math.pi / 3, 'π/3'), (2 * math.pi / 3, '2π/3'), (math.log(2), 'ln 2'), (math.log(3), 'ln 3')):
        if abs(t - v) < 1e-12:
            return s
    return num(t)


d44 = T('Parametric differentiation', 'parametric differentiation', 'parametric')
d44.fixed('C1', (1, 2), [
    ('For a curve given parametrically by x = f(t), y = g(t), dy/dx equals', '(dy/dt) ÷ (dx/dt)', 'Chain rule: dy/dx = (dy/dt)(dt/dx).', ['(dx/dt) ÷ (dy/dt)', '(dy/dt) × (dx/dt)', 'dy/dt − dx/dt']),
    ('A curve has parametric equations x = 2t, y = t². What is dy/dx?', 't', 'dy/dt = 2t, dx/dt = 2.', ['2t', '1/t', 't/2']),
    ('A curve has parametric equations x = cos t, y = sin t. What curve is this?', 'A circle of radius 1 centred at the origin', 'cos²t + sin²t = 1 gives x² + y² = 1.', ['A parabola', 'A straight line', 'An ellipse with semi-axes 1 and 2']),
])
d44.fixed('C2', (2, 3), [
    ('Explain how to find the points on a parametric curve where the tangent is parallel to the x-axis.', 'The tangent is horizontal where dy/dx = 0, i.e. where dy/dt = 0 (with dx/dt ≠ 0); solve for t and substitute into x and y.', 'B1 dy/dt = 0 with dx/dt ≠ 0; B1 substitute t to find the points [2]'),
    ('Explain why the parametric equations x = 3 cos t, y = 3 sin t and x = 3 sin t, y = 3 cos t describe the same curve.', 'In both cases x² + y² = 9 cos²t + 9 sin²t = 9, the same circle; only the starting point and direction of travel differ.', 'B1 both give x² + y² = 9; B1 differ only in starting point/direction [2]'),
])


@d44.add('C1', (1, 2, 3))
def d44_c1(r, D):
    c = param_curve(r)
    kind, xt, yt, X, Y, dx, dy, dytxt, ts = c
    t0 = r.choice(ts)
    if abs(dx(t0)) < 1e-9:
        return None
    g = Fr(dy(t0), dx(t0)) if kind == 'poly' else dy(t0) / dx(t0)
    if D == 1:
        return MC(r, f'A curve is given by x = {xt}, y = {yt}. Find dy/dx in terms of t.', dytxt,
                  [dytxt.split('/')[1].strip('()') + '/' + dytxt.split('/')[0].strip('()') if '/' in dytxt else dytxt + '²', dytxt.replace('−', '+', 1) if '−' in dytxt else MINUS + dytxt, xt + ' ÷ ' + yt], f'dy/dx = (dy/dt)/(dx/dt) = {dytxt}.')
    return MC(r, f'A curve is given by x = {xt}, y = {yt}. Find the gradient of the curve at the point where t = {tval(t0)}.', fx(g) if kind == 'poly' else n3(g),
              [fx(1 / g) if g else '1', fx(-g) if g else '−1', fx(dy(t0)), fx(dx(t0))] if kind == 'poly' else [n3(1 / g) if g else '1', n3(-g) if g else '−1', n3(dy(t0)), n3(dx(t0))], f'dy/dx = {dytxt} = {fx(g)} at t = {tval(t0)}.')


@d44.add('C2', (1, 2, 3, 4), 'explain')
def d44_err(r, D):
    nm = person(r)
    c = param_curve(r)
    kind, xt, yt, X, Y, dx, dy, dytxt, ts = c
    t0 = r.choice(ts)
    if abs(dx(t0)) < 1e-9 or abs(dy(t0)) < 1e-9:
        return None
    g = dy(t0) / dx(t0)
    stem = f'For the curve x = {xt}, y = {yt}, {nm} calculates the gradient at t = {tval(t0)} as (dx/dt)/(dy/dt) = {n3(1 / g)}. Explain the error and find the correct gradient.'
    return Q(stem, f'dy/dx = (dy/dt)/(dx/dt), not the reciprocal. Correct gradient = {n3(g)}.', f'B1 dy/dx = (dy/dt) ÷ (dx/dt); B1 {n3(g)}')


@d44.add('C3', (1, 2, 3, 4, 5), 'numerical')
def d44_calc(r, D):
    c = param_curve(r)
    kind, xt, yt, X, Y, dx, dy, dytxt, ts = c
    t0 = r.choice(ts)
    if abs(dx(t0)) < 1e-9:
        return None
    g = Fr(dy(t0), dx(t0)) if kind == 'poly' else dy(t0) / dx(t0)
    x0, y0 = X(t0), Y(t0)
    # numeric check of the gradient via a tiny step along the curve
    h = 1e-6
    if not ok((Y(t0 + h) - Y(t0 - h)) / (X(t0 + h) - X(t0 - h)), g, 'param grad', 1e-5):
        return None
    intro = f'A curve has parametric equations x = {xt}, y = {yt}.'
    if D == 1:
        return Q(f'{intro} Find dy/dx in terms of t.', f'dy/dx = {dytxt}', 'M1 differentiates x and y with respect to t; A1 dy/dx correct')
    if D == 2:
        return Q(f'{intro} Find the gradient of the curve at the point where t = {tval(t0)}.', fx(g) if kind == 'poly' else n3(g), f'M1 dy/dx = {dytxt}; A1 {fx(g) if kind == "poly" else n3(g)}')
    if D == 3:
        if kind == 'poly':
            m, cc = Fr(dy(t0), dx(t0)), Fr(Y(t0)) - Fr(dy(t0), dx(t0)) * Fr(X(t0))
            ans = f'y = {poly([(m, 1), (cc, 0)])}'
        else:
            ans = line3(g, y0 - g * x0)
        return Q(f'{intro} Find the equation of the tangent to the curve at the point where t = {tval(t0)}.', ans,
                 f'M1 dy/dx = {dytxt}; A1 gradient; B1 point ({fx(x0)}, {fx(y0)}); A1 {ans}')
    if D == 4:
        if abs(g) < 1e-9:
            return None
        if kind == 'poly':
            m = -Fr(dx(t0), dy(t0))
            cc = Fr(Y(t0)) - m * Fr(X(t0))
            ans = f'y = {poly([(m, 1), (cc, 0)])}'
        else:
            m = -1 / g
            ans = line3(m, y0 - m * x0)
        return Q(f'{intro} Find the equation of the normal to the curve at the point where t = {tval(t0)}.', ans,
                 f'M1 dy/dx = {dytxt}; A1 tangent gradient {fx(g) if kind == "poly" else n3(g)}; M1 normal gradient −1/(dy/dx); A1 {ans}')
    # stationary points: dy/dt = 0
    if kind == 'poly':
        p_, q_, rr_, s_ = None, None, None, None
        sol = [t for t in [math.sqrt(-dy(0) / (dy(1) - dy(0)))] if True] if (dy(1) - dy(0)) and -dy(0) / (dy(1) - dy(0)) > 0 else []
        if not sol:
            return None
        tt = sol[0]
        pts = [(X(tt), Y(tt)), (X(-tt), Y(-tt))]
        return Q(f'{intro} Find the coordinates of the points on the curve at which the tangent is parallel to the x-axis, giving your answers correct to 3 significant figures where appropriate.',
                 ' and '.join(f'({fx(a)}, {fx(b)})' for a, b in pts), f'M1 dy/dt = 0; A1 t = ±{fx(tt)}; M1 substitutes into x and y; A1 both points')
    if kind == 'exp':
        k = int(round(-(dy(0) - 2)))
        tt = math.log(k / 2) / 2
        return Q(f'{intro} Find the exact coordinates of the point on the curve at which the tangent is parallel to the x-axis.',
                 f'({fx(math.exp(tt))}, {fx(Y(tt))})', f'M1 dy/dt = 2e^(2t) − {k} = 0; A1 t = (1/2) ln({num(Fr(k, 2))}); M1 substitutes; A1 x = {fx(math.exp(tt))}, y = {fx(Y(tt))}')
    return None


def d44_c4(r, D):
    for _ in range(10):
        c = param_curve(r)
        if c[0] == 'poly':
            break
    kind, xt, yt, X, Y, dx, dy, dytxt, ts = c
    t0 = r.choice([1, 2, -1])
    if dx(t0) == 0:
        return None
    m = Fr(dy(t0), dx(t0))
    cc = Fr(Y(t0)) - m * Fr(X(t0))
    intro = f'A curve has parametric equations x = {xt}, y = {yt}.'
    parts = [
        P('Find dy/dx in terms of t.', dytxt, 'M1 dx/dt and dy/dt; A1 dy/dx'),
        P(f'Find the equation of the tangent to the curve at the point where t = {t0}.', f'y = {poly([(m, 1), (cc, 0)])}', f'B1 point ({num(X(t0))}, {num(Y(t0))}); M1 gradient {num(m)}; A1 y = {poly([(m, 1), (cc, 0)])}'),
        P('Find the value of t at which the tangent to the curve is parallel to the y-axis.', 't = 0', 'M1 dx/dt = 0 with dy/dt ≠ 0; A1 t = 0'),
    ]
    if m != 0:
        nn = -1 / m
        parts.append(P(f'Find the equation of the normal to the curve at the point where t = {t0}.', f'y = {poly([(nn, 1), (Fr(Y(t0)) - nn * Fr(X(t0)), 0)])}', f'M1 gradient {num(nn)}; A1 y = {poly([(nn, 1), (Fr(Y(t0)) - nn * Fr(X(t0)), 0)])}'))
    return cmp_(r, intro, parts)


d44.add('C4', (2, 3, 4, 5))(d44_c4)

CHAPTERS[4] = [d41, d42, d43, d44]


# ================================================================ Chapter 5 Integration

def cf2(c, sym):
    """Coefficient c (Fraction) times a symbol: 3e²ˣ, (3/2) sin 2x, −(1/2)e⁻ˣ, ln|x|."""
    c = Fr(c)
    sgn = MINUS if c < 0 else ''
    a = abs(c)
    spc = ' ' if re.match(r'(sin|cos|tan|ln|sec)', sym) else ''
    if a == 1:
        return sgn + sym
    if a.denominator == 1:
        return f'{sgn}{a.numerator}{spc}{sym}'
    return f'{sgn}({num(a)}){spc}{sym}'


def trig_exact(fn, f):
    """Exact value of fn(fπ) as xstr parts (fn sin/cos/tan), f a Fraction."""
    t = float(f) * math.pi
    v = {'sin': math.sin(t), 'cos': math.cos(t), 'tan': math.tan(t)}[fn]
    for x, parts in ((0, []), (0.5, [(Fr(1, 2), 'r', None)]), (R2 / 2, [(Fr(1, 2), 'sq', 2)]), (R3 / 2, [(Fr(1, 2), 'sq', 3)]), (1, [(Fr(1), 'r', None)]),
                     (R3 / 3, [(Fr(1, 3), 'sq', 3)]), (R3, [(Fr(1), 'sq', 3)])):
        if abs(abs(v) - x) < 1e-9:
            return [(c * (-1 if v < 0 else 1), k, a) for c, k, a in parts]
    return None


def scale(parts, k):
    return [(Fr(c) * Fr(k), kind, arg) for c, kind, arg in parts]


def piarg(f, a=1):
    """Text for the limit fπ (divided by a)."""
    return pi_frac(Fr(f) / a)


def int_family(r):
    kind = r.choice(['exp', 'recip', 'sin', 'cos', 'sec2'])
    k = r.choice([1, 2, 3, 4, 5, 6, -1, -2, -3])
    a = r.choice([1, 2, 3, 4, -1, -2])
    b = r.choice([0, 1, -1, 2, 3, -3])
    if kind == 'exp':
        fx_ = f'{cf2(k, ex(a, b))}'
        Fx = f'{cf2(Fr(k, a), ex(a, b))}'
        f = lambda x: k * math.exp(a * x + b)
        F = lambda x: k / a * math.exp(a * x + b)
    elif kind == 'recip':
        a = abs(a)
        if b == 0:
            b = r.choice([1, 2, 3, -1])
        fx_ = f'{k}/({lin(a, b)})'
        Fx = cf2(Fr(k, a), f'ln|{lin(a, b)}|')
        f = lambda x: k / (a * x + b)
        F = lambda x: k / a * math.log(abs(a * x + b))
    elif kind in ('sin', 'cos'):
        a = abs(a)
        arg = f'({lin(a, b)})' if b else trigarg(a)
        fx_ = cf2(k, f'{kind} {arg}' if not b else f'{kind}{arg}')
        if kind == 'sin':
            Fx = cf2(Fr(-k, a), f'cos {arg}' if not b else f'cos{arg}')
            f = lambda x: k * math.sin(a * x + b)
            F = lambda x: -k / a * math.cos(a * x + b)
        else:
            Fx = cf2(Fr(k, a), f'sin {arg}' if not b else f'sin{arg}')
            f = lambda x: k * math.cos(a * x + b)
            F = lambda x: k / a * math.sin(a * x + b)
    else:
        a = abs(a)
        fx_ = cf2(k, f'sec²{trigarg(a)}' if a != 1 else 'sec²x')
        Fx = cf2(Fr(k, a), f'tan {trigarg(a)}')
        f = lambda x: k / math.cos(a * x) ** 2
        F = lambda x: k / a * math.tan(a * x)
    for x0 in (0.13, 0.31, 0.47):
        try:
            if not ok(ndiff(F, x0), f(x0), 'int ' + kind, 1e-5):
                return None
        except (ValueError, ZeroDivisionError):
            pass
    return kind, fx_, Fx, f, F


n51 = T('Integrating eˣ, 1/x, sin x, cos x and sec²x', 'integrating eˣ, 1/x', 'sec²x')
n51.fixed('C1', (1, 2), [
    ('Find ∫ 1/x dx.', 'ln|x| + c', 'Standard integral; the modulus allows negative x.', ['1/x² + c', '−1/x² + c', 'x ln x + c']),
    ('Find ∫ sec²x dx.', 'tan x + c', 'd/dx(tan x) = sec²x.', ['sec x tan x + c', 'sec³x/3 + c', '−cot x + c']),
    ('Find ∫ sin x dx.', '−cos x + c', 'd/dx(cos x) = −sin x.', ['cos x + c', '−sin x + c', 'sin²x/2 + c']),
    ('Find ∫ e^(4x) dx.', '(1/4)e^(4x) + c', 'Divide by the coefficient of x.', ['4e^(4x) + c', 'e^(4x) + c', 'e^(4x + 1)/(4x + 1) + c']),
])
n51.fixed('C2', (2, 3), [
    ('Explain why ∫ 1/x dx is written ln|x| + c rather than ln x + c.', 'ln x is only defined for x > 0, but 1/x is defined for x < 0 too; d/dx ln|x| = 1/x for all x ≠ 0.', 'B1 ln x undefined for x ≤ 0; B1 ln|x| differentiates to 1/x for negative x too [2]'),
    ('Explain why ∫ e^(3x) dx = (1/3)e^(3x) + c by differentiating the answer.', 'd/dx[(1/3)e^(3x)] = (1/3) × 3e^(3x) = e^(3x), by the chain rule.', 'M1 differentiates using the chain rule; A1 shows the result is e^(3x) [2]'),
])


@n51.add('C1', (1, 2, 3))
def n51_c1(r, D):
    fam = int_family(r)
    if not fam:
        return None
    kind, fx_, Fx, f, F = fam
    wrong = Fx.replace('cos', 'X').replace('sin', 'cos').replace('X', 'sin') if kind in ('sin', 'cos') else Fx
    ds = [wrong + ' + c' if wrong != Fx else fx_ + ' + c', (Fx[1:] if Fx.startswith(MINUS) else MINUS + Fx) + ' + c', fx_ + ' + c', Fx.replace('ln|', 'ln(').replace('|', ')') + 'x + c' if 'ln' in Fx else 'x' + fx_ + ' + c']
    return MC(r, f'Find ∫ {fx_} dx.', Fx + ' + c', ds, f'∫ {fx_} dx = {Fx} + c.')


@n51.add('C2', (1, 2, 3, 4), 'explain')
def n51_err(r, D):
    nm = person(r)
    f = r.choice(['recip', 'sin', 'exp'])
    a, b = r.randint(2, 6), r.randint(1, 9)
    if f == 'recip':
        stem = f'{nm} writes ∫ 1/({lin(a, b)}) dx = ln|{lin(a, b)}| + c. Explain the error and give the correct integral.'
        return Q(stem, f'Differentiating ln|{lin(a, b)}| gives {a}/({lin(a, b)}), so a factor 1/{a} is needed: (1/{a}) ln|{lin(a, b)}| + c.', f'B1 checks by differentiating (chain rule factor {a}); B1 (1/{a}) ln|{lin(a, b)}| + c')
    if f == 'sin':
        stem = f'{nm} writes ∫ sin {a}x dx = (1/{a}) cos {a}x + c. Explain the error and give the correct integral.'
        return Q(stem, f'd/dx(cos {a}x) = −{a} sin {a}x, so the integral is −(1/{a}) cos {a}x + c; the sign is wrong.', f'B1 derivative of cos is −sin, so sign error; B1 −(1/{a}) cos {a}x + c')
    stem = f'{nm} writes ∫ e^({lin(a, b)}) dx = e^({lin(a, b)})/({lin(a, b)}) + c, treating it like a power of x. Explain the error and give the correct integral.'
    return Q(stem, f'The exponential is not a power xⁿ; d/dx e^({lin(a, b)}) = {a}e^({lin(a, b)}), so ∫ e^({lin(a, b)}) dx = (1/{a})e^({lin(a, b)}) + c.', f'B1 power rule not applicable; B1 (1/{a})e^({lin(a, b)}) + c')


SPEC_F = [Fr(1, 6), Fr(1, 4), Fr(1, 3), Fr(1, 2), Fr(2, 3), Fr(3, 4), Fr(5, 6), Fr(1)]


@n51.add('C3', (1, 2, 3, 4, 5), 'numerical')
def n51_calc(r, D):
    if D == 1:
        fam = int_family(r)
        if not fam:
            return None
        kind, fx_, Fx, f, F = fam
        return Q(f'Find ∫ {fx_} dx.', Fx + ' + c', f'M1 correct form; A1 {Fx} + c')
    if D == 2:
        a, k, b = r.randint(1, 4), r.randint(1, 6), r.randint(1, 3)
        parts = [(Fr(k, a), 'e', a * b), (Fr(-k, a), 'r', None)]
        val = xval(parts)
        if not ok(simpson(lambda x: k * math.exp(a * x), 0, b), val, 'n51 exp'):
            return None
        return Q(f'Find the exact value of ∫_0^{b} {cf2(k, ex(a))} dx.', xstr(parts), f'M1 [{cf2(Fr(k, a), ex(a))}]; M1 substitutes limits; A1 {xstr(parts)}')
    if D == 3:
        p, q = r.randint(1, 5), r.randint(1, 6)
        lo, hi = r.sample(range(0, 6), 2)
        lo, hi = min(lo, hi), max(lo, hi)
        k = p * r.randint(1, 3)
        R = Fr(p * hi + q, p * lo + q)
        if R.denominator != 1 and R.numerator != 1:
            pass
        val = k / p * math.log(float(R))
        if not ok(simpson(lambda x: k / (p * x + q), lo, hi), val, 'n51 recip'):
            return None
        ans = f'{"" if k // p == 1 else str(k // p) + " "}ln({num(R)})' if R.denominator != 1 else f'{"" if k // p == 1 else str(k // p) + " "}ln {num(R)}'
        ans2 = lnr(R ** (k // p))
        return Q(f'Show that ∫_{lo}^{hi} {k}/({lin(p, q)}) dx = {ans2}.', f'{ans} = {ans2}', f'M1 [{cf2(Fr(k, p), "ln|" + lin(p, q) + "|")}]; M1 substitutes limits and uses ln a − ln b = ln(a/b); A1 {ans2} shown')
    if D == 4:
        a = r.randint(1, 4)
        fn = r.choice(['sin', 'cos'])
        th = r.choice([Fr(1, 6), Fr(1, 4), Fr(1, 3), Fr(1, 2), Fr(2, 3)])
        k = r.randint(1, 6)
        # ∫_0^{θ/a} k cos(ax) dx = (k/a) sin θ ; ∫ k sin(ax) = (k/a)(1 − cos θ)
        if fn == 'cos':
            parts = scale(trig_exact('sin', th), Fr(k, a))
        else:
            parts = [(Fr(k, a), 'r', None)] + scale(trig_exact('cos', th), Fr(-k, a))
        val = xval(parts)
        g = (lambda x: k * math.cos(a * x)) if fn == 'cos' else (lambda x: k * math.sin(a * x))
        if not ok(simpson(g, 0, float(th) * math.pi / a), val, 'n51 trig'):
            return None
        return Q(f'Find the exact value of ∫_0^({piarg(th, a)}) {cf2(k, fn + " " + trigarg(a))} dx.', xstr(parts), f'M1 [{cf2(Fr(k if fn == "cos" else -k, a), ("sin " if fn == "cos" else "cos ") + trigarg(a))}]; M1 exact values at the limits; A1 {xstr(parts)}')
    a = r.randint(1, 3)
    c = r.randint(2, 12)
    # ∫_0^K e^(ax) dx = c  ->  (e^(aK) − 1)/a = c  ->  K = ln(ac + 1)/a
    K = math.log(a * c + 1) / a
    if not ok(simpson(lambda x: math.exp(a * x), 0, K), c, 'n51 findk'):
        return None
    exact = f'ln {a * c + 1}' if a == 1 else f'(1/{a}) ln {a * c + 1}'
    return Q(f'Given that ∫_0^k {ex(a)} dx = {c}, find the exact value of k.', f'k = {exact}', f'M1 [{cf2(Fr(1, a), ex(a))}]₀^k = {c}; A1 {ek(1) if False else ""}e^({a if a > 1 else ""}k) = {a * c + 1}; A1 k = {exact}'.replace('A1 e^(', 'A1 e^('))


def n51_c4(r, D):
    a = r.randint(1, 3)
    b = r.randint(1, 3)
    c = r.randint(1, 4)
    # area under y = e^(ax) + c/x from 1 to b+1
    hi = b + 1
    parts = [(Fr(1, a), 'e', a * hi), (Fr(-1, a), 'e', a), (Fr(c), 'ln', hi)]
    val = xval(parts)
    if not ok(simpson(lambda x: math.exp(a * x) + c / x, 1, hi), val, 'n51 c4'):
        return None
    k = r.randint(2, 5)
    intro = f'The function f is defined by f(x) = {ex(a)} + {c}/x for x > 0.'
    parts_ = [
        P('Find ∫ f(x) dx.', f'{cf2(Fr(1, a), ex(a))} + {cf2(c, "ln x")} + c', f'B1 {cf2(Fr(1, a), ex(a))}; B1 {cf2(c, "ln x")}'),
        P(f'Find the exact area of the region bounded by the curve y = f(x), the x-axis and the lines x = 1 and x = {hi}.', xstr(parts), f'M1 substitutes limits; A1 {xstr(parts)}'),
        P(f'Give the area of the region bounded by the curve y = f(x), the x-axis and the lines x = 1 and x = {hi} correct to 3 significant figures.', n3(val), f'B1 {n3(val)}'),
        P(f'Find ∫ {k} sec²{trigarg(a)} dx.', f'{cf2(Fr(k, a), "tan " + trigarg(a))} + c', f'B1 {cf2(Fr(k, a), "tan " + trigarg(a))} + c'),
    ]
    return cmp_(r, intro, parts_)


n51.add('C4', (2, 3, 4, 5))(n51_c4)


# ---------------------------------------------------------------- 5.2 trigonometric identities in integration

n52 = T('Using trigonometric identities in integration', 'trigonometric identities in integration', 'using trigonometric identities')
n52.fixed('C1', (1, 2), [
    ('Which identity is used to integrate cos²x?', 'cos²x = (1 + cos 2x)/2', 'Rearranging cos 2x = 2cos²x − 1.', ['cos²x = 1 − sin²x', 'cos²x = (1 − cos 2x)/2', 'cos²x = 2 cos x − 1']),
    ('Which identity is used to integrate tan²x?', 'tan²x = sec²x − 1', 'From 1 + tan²x = sec²x; then ∫ sec²x dx = tan x.', ['tan²x = sec²x + 1', 'tan²x = 1 − sec²x', 'tan²x = (1 − cos 2x)/(1 + cos 2x) only']),
    ('Find ∫ sin x cos x dx.', '−(1/4) cos 2x + c', 'sin x cos x = (1/2) sin 2x.', ['(1/2) sin²x cos²x + c', 'cos 2x + c', '−sin x cos x + c']),
])
n52.fixed('C2', (2, 3), [
    ('Explain why ∫ sin²x dx is not equal to (1/3) sin³x + c.', 'd/dx[(1/3) sin³x] = sin²x cos x, not sin²x. Instead write sin²x = (1 − cos 2x)/2 and integrate to x/2 − (1/4) sin 2x + c.', 'B1 differentiating sin³x/3 gives an extra cos x factor; B1 correct method with the double angle identity [2]'),
    ('Explain how to integrate (sin x + cos x)².', 'Expand to sin²x + 2 sin x cos x + cos²x = 1 + sin 2x, then integrate: x − (1/2) cos 2x + c.', 'B1 expands and uses sin² + cos² = 1 and sin 2x; B1 x − (1/2) cos 2x + c [2]'),
])


def sq_integral(fn, a):
    """∫ fn²(ax) dx text."""
    a = Fr(a)
    if fn == 'sin':
        return f'(1/2)x − {cf2(Fr(1, 4 * a), "sin " + trigarg(2 * a))}'
    if fn == 'cos':
        return f'(1/2)x + {cf2(Fr(1, 4 * a), "sin " + trigarg(2 * a))}'
    return f'{cf2(Fr(1, a), "tan " + trigarg(a))} − x'


def sq_def(fn, a, th):
    """Exact ∫_0^{θπ/a} fn²(ax) dx as parts."""
    if fn == 'sin':
        return [(Fr(th) / (2 * a), 'pi', None)] + scale(trig_exact('sin', 2 * th), Fr(-1, 4 * a))
    if fn == 'cos':
        return [(Fr(th) / (2 * a), 'pi', None)] + scale(trig_exact('sin', 2 * th), Fr(1, 4 * a))
    return scale(trig_exact('tan', th), Fr(1, a)) + [(-Fr(th) / a, 'pi', None)]


@n52.add('C1', (1, 2, 3))
def n52_c1(r, D):
    fn = r.choice(['sin', 'cos', 'tan'])
    a = r.randint(1, 5)
    k = r.choice([1, 1, 2, 3, 4, 6])
    sc_ = lambda t: t if k == 1 else f'{k}({t})'
    ans = sc_(sq_integral(fn, a)) + ' + c'
    other = {'sin': 'cos', 'cos': 'sin', 'tan': 'sin'}[fn]
    ds = [sc_(sq_integral(other, a)) + ' + c', f'({num(Fr(k, 3))}){fn}³{trigarg(a)} + c', sc_(sq_integral(fn, Fr(1, a))) + ' + c' if a != 1 else f'{k}x + c', f'({num(Fr(k, 2))})x + c']
    return MC(r, f'Find ∫ {cf2(k, fn + "²" + trigarg(a))} dx.', ans, ds, f'Use the identity for {fn}²: ∫ = {ans}.')


@n52.add('C2', (1, 2, 3, 4), 'explain')
def n52_err(r, D):
    nm = person(r)
    a = r.randint(1, 4)
    f = r.choice(['power', 'tan', 'sign'])
    if f == 'power':
        fn = r.choice(['sin', 'cos'])
        stem = f'{nm} writes ∫ {fn}²{trigarg(a)} dx = (1/3){fn}³{trigarg(a)} + c. Explain why this is wrong and find the correct integral.'
        return Q(stem, f'Differentiating {fn}³{trigarg(a)}/3 gives an extra factor from the chain rule, so it is not {fn}²{trigarg(a)}. Using the double angle identity: {sq_integral(fn, a)} + c.',
                 f'B1 explains the reverse chain rule fails; M1 uses {fn}²u = (1 {"−" if fn == "sin" else "+"} cos 2u)/2; A1 {sq_integral(fn, a)} + c')
    if f == 'tan':
        stem = f'{nm} writes ∫ tan²{trigarg(a)} dx = {cf2(Fr(1, a), "sec²" + trigarg(a))} + c. Explain the error and find the correct integral.'
        return Q(stem, f'tan²u = sec²u − 1, and it is sec²u that integrates to tan u. ∫ tan²{trigarg(a)} dx = {sq_integral("tan", a)} + c.', f'B1 uses tan² = sec² − 1; B1 {sq_integral("tan", a)} + c')
    stem = f'{nm} writes cos²x = (1 − cos 2x)/2 and hence ∫ cos²x dx = x/2 − (1/4) sin 2x + c. Explain the error and give the correct integral.'
    return Q(stem, 'The identity is cos²x = (1 + cos 2x)/2 (it is sin²x that has the minus sign). ∫ cos²x dx = x/2 + (1/4) sin 2x + c.', 'B1 correct identity; B1 x/2 + (1/4) sin 2x + c')


@n52.add('C3', (1, 2, 3, 4, 5), 'numerical')
def n52_calc(r, D):
    fn = r.choice(['sin', 'cos', 'tan'])
    a = r.randint(1, 3)
    if D == 1:
        return Q(f'Find ∫ {fn}²{trigarg(a)} dx.', sq_integral(fn, a) + ' + c', f'M1 uses the appropriate identity; A1 {sq_integral(fn, a)} + c')
    if D in (2, 3, 4):
        th = r.choice([Fr(1, 6), Fr(1, 4), Fr(1, 3)] if fn == 'tan' else [Fr(1, 6), Fr(1, 4), Fr(1, 3), Fr(1, 2), Fr(2, 3)])
        k = 1 if D == 2 else r.randint(2, 6)
        parts = scale(sq_def(fn, a, th), k)
        val = xval(parts)
        g = {'sin': lambda x: math.sin(a * x) ** 2, 'cos': lambda x: math.cos(a * x) ** 2, 'tan': lambda x: math.tan(a * x) ** 2}[fn]
        if not ok(simpson(lambda x: k * g(x), 0, float(th) * math.pi / a), val, 'n52 def'):
            return None
        intg = cf2(k, f'{fn}²{trigarg(a)}')
        if D == 4:
            return Q(f'Show that ∫_0^({piarg(th, a)}) {intg} dx = {xstr(parts)}.', xstr(parts), f'M1 uses identity for {fn}²; A1 correct integral; M1 substitutes limits with exact values; A1 {xstr(parts)} shown')
        return Q(f'Find the exact value of ∫_0^({piarg(th, a)}) {intg} dx.', xstr(parts), f'M1 uses identity for {fn}²; A1 {cf2(k, "(" + sq_integral(fn, a) + ")") if k != 1 else sq_integral(fn, a)}; M1 exact values at limits; A1 {xstr(parts)}')
    th = r.choice([Fr(1, 6), Fr(1, 4), Fr(1, 3), Fr(1, 2)])
    # ∫_0^{θπ/a} (sin ax + cos ax)² dx = θπ/a − (cos 2θπ − 1)/(2a)
    parts = [(Fr(th) / a, 'pi', None), (Fr(1, 2 * a), 'r', None)] + scale(trig_exact('cos', 2 * th), Fr(-1, 2 * a))
    val = xval(parts)
    if not ok(simpson(lambda x: (math.sin(a * x) + math.cos(a * x)) ** 2, 0, float(th) * math.pi / a), val, 'n52 sq'):
        return None
    return Q(f'Find the exact value of ∫_0^({piarg(th, a)}) (sin {trigarg(a)} + cos {trigarg(a)})² dx.', xstr(parts),
             f'M1 expands to 1 + sin {trigarg(2 * a)}; A1 [x − {cf2(Fr(1, 2 * a), "cos " + trigarg(2 * a))}]; M1 limits; A1 {xstr(parts)}')


def n52_c4(r, D):
    a = r.randint(1, 3)
    th = r.choice([Fr(1, 6), Fr(1, 4), Fr(1, 3)])
    k = r.randint(2, 5)
    p1 = sq_def('cos', a, th)
    p2 = sq_def('tan', a, th)
    intro = f'In this question, x is in radians.'
    parts = [
        P(f'Show that cos²{trigarg(a)} ≡ (1/2)(1 + cos {trigarg(2 * a)}).', 'From cos 2u = 2cos²u − 1.', 'B1 uses cos 2u = 2cos²u − 1 and rearranges'),
        P(f'Find the exact value of ∫_0^({piarg(th, a)}) cos²{trigarg(a)} dx.', xstr(p1), f'M1 integrates (1/2)(1 + cos {trigarg(2 * a)}); A1 {xstr(p1)}'),
        P(f'Find the exact value of ∫_0^({piarg(th, a)}) tan²{trigarg(a)} dx.', xstr(p2), f'M1 uses tan² = sec² − 1; A1 {xstr(p2)}'),
        P(f'Find ∫ {k} sin {trigarg(a)} cos {trigarg(a)} dx.', f'{cf2(Fr(-k, 4 * a), "cos " + trigarg(2 * a))} + c', f'M1 uses sin 2u = 2 sin u cos u; A1 {cf2(Fr(-k, 4 * a), "cos " + trigarg(2 * a))} + c'),
    ]
    if not ok(simpson(lambda x: math.cos(a * x) ** 2, 0, float(th) * math.pi / a), xval(p1), 'n52 c4'):
        return None
    return cmp_(r, intro, parts)


n52.add('C4', (2, 3, 4, 5))(n52_c4)


# ---------------------------------------------------------------- 5.3 trapezium rule

TRAP_F = [
    ('√(1 + x³)', lambda x: math.sqrt(1 + x ** 3), (0, 3)),
    ('ln(1 + x²)', lambda x: math.log(1 + x * x), (0, 3)),
    ('e^(−x²)', lambda x: math.exp(-x * x), (0, 2)),
    ('1/(1 + x²)', lambda x: 1 / (1 + x * x), (0, 2)),
    ('√(x + 4)', lambda x: math.sqrt(x + 4), (0, 5)),
    ('x eˣ', lambda x: x * math.exp(x), (0, 2)),
    ('ln x', lambda x: math.log(x), (1, 5)),
    ('1/(2 + x)', lambda x: 1 / (2 + x), (0, 4)),
    ('sec x', lambda x: 1 / math.cos(x), (0, 1)),
    ('√(sin x)', lambda x: math.sqrt(max(0.0, math.sin(x))), (0.5, 1.5)),
    ('x/(1 + eˣ)', lambda x: x / (1 + math.exp(x)), (0, 2)),
    ('e^(√x)', lambda x: math.exp(math.sqrt(x)), (1, 4)),
]


def hstr(h):
    if abs(h * 1000 - round(h * 1000)) < 1e-9:
        return num(round(h, 3))
    return num(Fr(h).limit_denominator(100))


def trap(f, a, b, n):
    h = (b - a) / n
    ys = [f(a + i * h) for i in range(n + 1)]
    return h / 2 * (ys[0] + ys[-1] + 2 * sum(ys[1:-1])), ys, h


def concavity(f, a, b):
    vals = []
    for i in range(1, 40):
        x = a + (b - a) * i / 40
        h = 1e-3
        vals.append((f(x + h) - 2 * f(x) + f(x - h)) / (h * h))
    if all(v > 1e-6 for v in vals):
        return 'over'
    if all(v < -1e-6 for v in vals):
        return 'under'
    return None


def trap_setup(r):
    txt, f, (lo, hi) = r.choice(TRAP_F)
    n = r.choice([2, 3, 4, 5, 6])
    span = r.choice([x for x in (1, 1.5, 2, 2.5, 3, 4) if lo + x <= hi + 1e-9] or [hi - lo])
    if txt == 'sec x':
        span = r.choice([0.6, 0.8, 1.0])
    if txt == '√(sin x)':
        span = 1
    a = lo if r.random() < 0.7 or txt in ('sec x', '√(sin x)') else lo + 0.5
    b = a + span
    est, ys, h = trap(f, a, b, n)
    return txt, f, a, b, n, est, ys, h


n53 = T('The trapezium rule and over- or under-estimation', 'trapezium rule', 'over- or under-estimation')
n53.fixed('C1', (1, 2), [
    ('The trapezium rule with n strips of width h uses how many ordinates?', 'n + 1', 'Each strip has two ends; adjacent strips share one.', ['n', 'n − 1', '2n']),
    ('For a curve that is concave upwards (convex) on the interval, the trapezium rule gives', 'an over-estimate', 'The chords lie above the curve.', ['an under-estimate', 'the exact value', 'an estimate that may be either']),
    ('Which change usually improves the accuracy of a trapezium rule estimate?', 'Using more strips of smaller width', 'The chords then follow the curve more closely.', ['Using fewer, wider strips', 'Rounding the ordinates to 1 d.p.', 'Using only the end ordinates']),
])
n53.fixed('C2', (2, 3), [
    ('Explain why the trapezium rule over-estimates ∫₀¹ eˣ dx.', 'y = eˣ is concave upwards (d²y/dx² = eˣ > 0), so each chord lies above the curve and each trapezium has more area than the region under the curve.', 'B1 curve concave upwards (convex); B1 chords lie above the curve [2]'),
    ('Explain why doubling the number of strips generally improves a trapezium rule estimate.', 'Narrower strips mean the straight chords stay closer to the curve, so the gaps between chords and curve (the error) are smaller.', 'B1 narrower strips; B1 chords closer to the curve so smaller error [2]'),
])


@n53.add('C1', (1, 2, 3))
def n53_c1(r, D):
    txt, f, a, b, n, est, ys, h = trap_setup(r)
    if D == 1:
        return MC(r, f'The trapezium rule with {n} strips is used to estimate ∫_{num(a)}^{num(b)} {txt} dx. What is the width h of each strip?', hstr(h),
                  [hstr((b - a) / (n + 1)), hstr((b - a) / (n - 1)) if n > 1 else hstr(b - a), hstr(b - a), hstr(n / (b - a))], f'h = ({num(b)} − {num(a)})/{n} = {hstr(h)}.')
    if D == 2:
        cv = concavity(f, a, b)
        if not cv:
            return None
        return MC(r, f'The trapezium rule is used to estimate ∫_{num(a)}^{num(b)} {txt} dx. The curve y = {txt} is concave {"upwards" if cv == "over" else "downwards"} on this interval. The estimate is',
                  'an over-estimate' if cv == 'over' else 'an under-estimate', ['an under-estimate' if cv == 'over' else 'an over-estimate', 'exact', 'impossible to classify', 'zero'],
                  'Concave upwards: chords above curve, over-estimate.' if cv == 'over' else 'Concave downwards: chords below curve, under-estimate.')
    wrong = h * (sum(ys))
    return MC(r, f'Use the trapezium rule with {n} strips to estimate ∫_{num(a)}^{num(b)} {txt} dx, giving your answer correct to 3 significant figures.', n3(est),
              [n3(wrong), n3(est * 2), n3(h / 2 * (ys[0] + ys[-1])), n3(est / 2)], f'(h/2)[y₀ + 2(y₁ + … + y{str(n - 1).translate(SUB)}) + y{str(n).translate(SUB)}] = {n3(est)}.')


@n53.add('C2', (1, 2, 3, 4), 'explain')
def n53_err(r, D):
    nm = person(r)
    txt, f, a, b, n, est, ys, h = trap_setup(r)
    cv = concavity(f, a, b)
    fr_ = r.choice(['h', 'conc'] if cv else ['h'])
    if fr_ == 'h':
        hw = (b - a) / (n + 1)
        stem = f'{nm} uses the trapezium rule with {n} strips to estimate ∫_{num(a)}^{num(b)} {txt} dx and takes h = ({num(b)} − {num(a)})/{n + 1} = {n3(hw)} because there are {n + 1} ordinates. Explain the error and find the correct estimate.'
        return Q(stem, f'h is the strip width: (b − a)/(number of strips) = {hstr(h)}. Correct estimate {n3(est)}.', f'B1 h = (b − a)/n = {num(h)}; B1 {n3(est)}')
    wrongword = 'under-estimate' if cv == 'over' else 'over-estimate'
    stem = f'{nm} says that the trapezium rule estimate of ∫_{num(a)}^{num(b)} {txt} dx is an {wrongword}. Using a sketch of y = {txt} or its second derivative, explain whether {nm} is right.'
    return Q(stem, f'{nm} is wrong: the curve is concave {"upwards" if cv == "over" else "downwards"} on [{num(a)}, {num(b)}], so the chords lie {"above" if cv == "over" else "below"} the curve and the rule gives an {"over" if cv == "over" else "under"}-estimate.',
             f'B1 concave {"upwards" if cv == "over" else "downwards"} on the interval; B1 so {"over" if cv == "over" else "under"}-estimate')


@n53.add('C3', (1, 2, 3, 4, 5), 'numerical')
def n53_calc(r, D):
    txt, f, a, b, n, est, ys, h = trap_setup(r)
    tab = ', '.join(f'{n4(y)}' for y in ys)
    if D <= 3:
        return Q(f'Use the trapezium rule with {n} intervals to estimate the value of ∫_{num(a)}^{num(b)} {txt} dx, giving your answer correct to 3 significant figures.', n3(est),
                 f'B1 h = {hstr(h)}; M1 ordinates {tab}; M1 correct formula; A1 {n3(est)}')
    cv = concavity(f, a, b)
    if not cv:
        return None
    return Q(f'Use the trapezium rule with {n} intervals to estimate the value of ∫_{num(a)}^{num(b)} {txt} dx, giving your answer correct to 3 significant figures. Explain, with reference to the shape of the curve, whether the estimate is an over-estimate or an under-estimate.',
             f'{n3(est)}; {"over" if cv == "over" else "under"}-estimate', f'B1 h = {hstr(h)}; M1 ordinates {tab}; M1 formula; A1 {n3(est)}; B1 curve concave {"up" if cv == "over" else "down"}, so {"over" if cv == "over" else "under"}-estimate')


def n53_c4(r, D):
    kind = r.choice(['exp', 'recip'])
    n = r.choice([2, 3, 4])
    if kind == 'exp':
        k = r.choice([1, 2, Fr(1, 2)])
        b = r.choice([1, 2])
        f = lambda x: math.exp(float(k) * x)
        txt = ex(k)
        exact = [(1 / Fr(k), 'e', k * b), (-1 / Fr(k), 'r', None)]
        a = 0
    else:
        c = r.randint(1, 4)
        a, b = 0, r.choice([2, 3, 4])
        f = lambda x: 1 / (x + c)
        txt = f'1/(x + {c})'
        R = Fr(b + c, c)
        exact = [(Fr(1), 'ln', int(R))] if R.denominator == 1 else [(Fr(1), 'ln', b + c), (Fr(-1), 'ln', c)]
    est, ys, h = trap(f, a, b, n)
    ev = xval(exact)
    if not ok(simpson(f, a, b), ev, 'n53 exact'):
        return None
    err = abs(est - ev) / ev * 100
    cv = concavity(f, a, b)
    intro = f'The region R is bounded by the curve y = {txt}, the x-axis and the lines x = {a} and x = {b}.'
    parts = [
        P(f'Use the trapezium rule with {n} strips to estimate the area of R, giving your answer correct to 4 significant figures.', n4(est), f'B1 h = {hstr(h)}; M1 correct formula; A1 {n4(est)}'),
        P('Find the exact area of R.', xstr(exact), f'M1 integrates; A1 {xstr(exact)}'),
        P(f'Calculate the percentage error in the estimate of the area of R obtained using the trapezium rule with {n} strips.', f'{n3(err)}%', f'M1 |estimate − exact| ÷ exact × 100; A1 {n3(err)}%'),
    ]
    if cv == 'over':
        parts.append(P('Explain why the trapezium rule gives an over-estimate of the area of R.', 'The curve is concave upwards, so the chords lie above it.', 'B1 concave upwards (d²y/dx² > 0), chords above the curve'))
    elif cv == 'under':
        parts.append(P('Explain why the trapezium rule gives an under-estimate of the area of R.', 'The curve is concave downwards, so the chords lie below it.', 'B1 concave downwards (d²y/dx² < 0), chords below the curve'))
    return cmp_(r, intro, parts)


n53.add('C4', (2, 3, 4, 5))(n53_c4)


# ---------------------------------------------------------------- 5.4 definite integrals

n54 = T('Definite integrals of exponential, logarithmic and trigonometric functions', 'definite integrals of exponential', 'definite integrals')
n54.fixed('C1', (1, 2), [
    ('What is the exact value of ∫_1^e 1/x dx?', '1', '[ln x] from 1 to e = 1 − 0.', ['e − 1', '0', '1/e']),
    ('What is the exact value of ∫_0^(π/2) cos x dx?', '1', '[sin x] from 0 to π/2 = 1 − 0.', ['0', 'π/2', '−1']),
    ('What is the exact value of ∫_0^1 eˣ dx?', 'e − 1', '[eˣ]₀¹ = e − 1.', ['e', '1', 'e + 1']),
    ('What is the exact value of ∫_0^π sin x dx?', '2', '[−cos x]₀^π = 1 + 1.', ['0', '1', 'π']),
])
n54.fixed('C2', (2, 3), [
    ('Explain why ∫_0^(2π) sin x dx = 0 even though the curve y = sin x encloses a non-zero area with the x-axis.', 'The part from π to 2π lies below the axis and contributes a negative value that cancels the positive part from 0 to π; the total area is 4.', 'B1 negative contribution below the axis; B1 cancels; area requires separate integrals [2]'),
    ('Explain why ∫₋₁¹ 1/x dx cannot be evaluated as [ln|x|]₋₁¹ = 0.', '1/x is undefined at x = 0, which lies within the interval, so the integral is improper and the standard result cannot be applied across the discontinuity.', 'B1 discontinuity at x = 0 in the interval; B1 so the result is not valid [2]'),
])


@n54.add('C1', (1, 2, 3))
def n54_c1(r, D):
    if D == 1:
        k = r.randint(2, 9)
        return MC(r, f'Find the exact value of ∫_1^{k} 1/x dx.', f'ln {k}', [f'{num(1 - Fr(1, k))}', f'1/{k}', f'ln {k - 1}'], f'[ln x]₁^{k} = ln {k}.')
    if D == 2:
        a, b = r.randint(1, 4), r.randint(1, 3)
        parts = [(Fr(1, a), 'e', a * b), (Fr(-1, a), 'r', None)]
        return MC(r, f'Find the exact value of ∫_0^{b} {ex(a)} dx.', xstr(parts), [xstr([(Fr(1), 'e', a * b), (Fr(-1), 'r', None)]), xstr([(Fr(a), 'e', a * b), (Fr(-a), 'r', None)]), xstr([(Fr(1, a), 'e', a * b)]), xstr([(Fr(1, a), 'e', a * b), (Fr(1, a), 'r', None)])],
                  f'[{cf2(Fr(1, a), ex(a))}]₀^{b} = {xstr(parts)}.')
    a = r.randint(1, 3)
    th = r.choice([Fr(1, 6), Fr(1, 4), Fr(1, 3), Fr(1, 2)])
    parts = scale(trig_exact('sin', th), Fr(1, a))
    alt = [scale(trig_exact('cos', th), Fr(1, a)), scale(trig_exact('sin', th), Fr(a)), trig_exact('sin', th) + [(Fr(-1), 'r', None)], [(Fr(th, a), 'pi', None)]]
    return MC(r, f'Find the exact value of ∫_0^({piarg(th, a)}) cos {trigarg(a)} dx.', xstr(parts), [xstr(p) for p in alt], f'[{cf2(Fr(1, a), "sin " + trigarg(a))}] = {xstr(parts)}.')


@n54.add('C2', (1, 2, 3, 4), 'explain')
def n54_err(r, D):
    nm = person(r)
    f = r.choice(['area', 'ln'])
    if f == 'area':
        k = r.randint(1, 4)
        stem = f'{nm} calculates the total area between y = sin {trigarg(k)} and the x-axis for 0 ≤ x ≤ {pi_frac(Fr(2, k))} as ∫_0^({pi_frac(Fr(2, k))}) sin {trigarg(k)} dx = 0. Explain the error and find the correct area.'
        return Q(stem, f'Half of the region lies below the x-axis and its integral is negative, cancelling the positive part. Area = 2 × ∫_0^({pi_frac(Fr(1, k))}) sin {trigarg(k)} dx = 2 × {num(Fr(2, k))} = {num(Fr(4, k))}.',
                 f'B1 region below the axis gives a negative integral; M1 integrates separately over each half; A1 {num(Fr(4, k))}')
    p, q = r.randint(2, 5), r.randint(1, 6)
    hi = r.randint(1, 4)
    R = Fr(p * hi + q, q)
    stem = f'{nm} evaluates ∫_0^{hi} 1/({lin(p, q)}) dx as [ln({lin(p, q)})]₀^{hi} = {lnr(R)}. Explain the error and give the correct exact value.'
    return Q(stem, f'The integral of 1/({lin(p, q)}) is (1/{p}) ln({lin(p, q)}); the factor 1/{p} is missing. Correct value (1/{p}) {lnr(R)}.', f'B1 missing factor 1/{p}; B1 (1/{p}) {lnr(R)}')


@n54.add('C3', (1, 2, 3, 4, 5), 'numerical')
def n54_calc(r, D):
    if D == 1:
        k, a = r.randint(1, 6), r.randint(1, 3)
        b = r.randint(1, 2)
        parts = [(Fr(k, a), 'e', a * b), (Fr(-k, a), 'r', None)]
        if not ok(simpson(lambda x: k * math.exp(a * x), 0, b), xval(parts), 'n54 e'):
            return None
        return Q(f'Find the exact value of ∫_0^{b} {cf2(k, ex(a))} dx.', xstr(parts), f'M1 [{cf2(Fr(k, a), ex(a))}]; A1 {xstr(parts)}')
    if D == 2:
        a, b = r.randint(1, 3), r.randint(1, 3)
        # ∫_0^b (e^(ax) + e^(−ax)) dx = (e^(ab) − e^(−ab))/a
        parts = [(Fr(1, a), 'e', a * b), (Fr(-1, a), 'e', -a * b)]
        if not ok(simpson(lambda x: math.exp(a * x) + math.exp(-a * x), 0, b), xval(parts), 'n54 cosh'):
            return None
        return Q(f'Find the exact value of ∫_0^{b} ({ex(a)} + {ex(-a)}) dx.', xstr(parts), f'M1 integrates both terms; A1 [{cf2(Fr(1, a), ex(a))} − {cf2(Fr(1, a), ex(-a))}]; A1 {xstr(parts)}')
    if D == 3:
        k = r.randint(2, 6)
        p, q = r.randint(1, 4), r.randint(1, 5)
        lo, hi = 0, r.randint(1, 5)
        R = Fr(p * hi + q, q)
        parts = [(Fr(k, p), 'ln', int(R))] if R.denominator == 1 else [(Fr(k, p), 'ln', p * hi + q), (Fr(-k, p), 'ln', q)]
        if not ok(simpson(lambda x: k / (p * x + q), lo, hi), xval(parts), 'n54 ln'):
            return None
        return Q(f'Find the exact value of ∫_0^{hi} {k}/({lin(p, q)}) dx.', xstr(parts), f'M1 [{cf2(Fr(k, p), "ln(" + lin(p, q) + ")")}]; M1 limits; A1 {xstr(parts)}')
    if D == 4:
        a = r.randint(1, 3)
        th1, th2 = sorted(r.sample([Fr(1, 6), Fr(1, 4), Fr(1, 3), Fr(1, 2)], 2))
        k = r.randint(1, 4)
        # ∫ k sin(ax) from θ1π/a to θ2π/a = (k/a)(cos θ1 − cos θ2)
        parts = scale(trig_exact('cos', th1), Fr(k, a)) + scale(trig_exact('cos', th2), Fr(-k, a))
        if not ok(simpson(lambda x: k * math.sin(a * x), float(th1) * math.pi / a, float(th2) * math.pi / a), xval(parts), 'n54 sin'):
            return None
        return Q(f'Find the exact value of ∫_({piarg(th1, a)})^({piarg(th2, a)}) {cf2(k, "sin " + trigarg(a))} dx.', xstr(parts), f'M1 [{cf2(Fr(-k, a), "cos " + trigarg(a))}]; M1 exact values; A1 {xstr(parts)}')
    k = r.randint(2, 6)
    c = r.randint(2, 6)
    # ∫_1^a k/x dx = c -> a = e^(c/k)
    return Q(f'Given that ∫_1^a {k}/x dx = {c}, where a > 1, find the exact value of a.', f'a = {ek(Fr(c, k))}', f'M1 {k} ln a = {c}; A1 a = {ek(Fr(c, k))}')


def n54_c4(r, D):
    a = r.randint(1, 3)
    k = r.randint(1, 4)
    th = r.choice([Fr(1, 2), Fr(1)])
    # region under y = k sin(ax) from 0 to π/a : area 2k/a
    area = Fr(2 * k, a)
    p, q = r.randint(1, 3), r.randint(1, 4)
    hi = r.randint(1, 3)
    R = Fr(p * hi + q, q)
    lnparts = [(Fr(1, p), 'ln', int(R))] if R.denominator == 1 else [(Fr(1, p), 'ln', p * hi + q), (Fr(-1, p), 'ln', q)]
    b = r.randint(1, 2)
    eparts = [(Fr(1, 2), 'e', 2 * b), (Fr(-1, 2), 'r', None)]
    intro = 'Give exact answers to the following.'
    parts = [
        P(f'Find the area of the region between the curve y = {cf2(k, "sin " + trigarg(a))} and the x-axis for 0 ≤ x ≤ {pi_frac(Fr(1, a))}.', num(area), f'M1 [{cf2(Fr(-k, a), "cos " + trigarg(a))}]; A1 {num(area)}'),
        P(f'Find the value of ∫_0^{hi} 1/({lin(p, q)}) dx.', xstr(lnparts), f'M1 (1/{p}) ln({lin(p, q)}); A1 {xstr(lnparts)}'),
        P(f'Find the value of ∫_0^{b} e^(2x) dx.', xstr(eparts), f'M1 (1/2)e^(2x); A1 {xstr(eparts)}'),
        P(f'Find the total area enclosed between y = {cf2(k, "sin " + trigarg(a))} and the x-axis for 0 ≤ x ≤ {pi_frac(Fr(2, a))}.', num(2 * area), f'M1 considers the part below the axis separately; A1 {num(2 * area)}'),
    ]
    return cmp_(r, intro, parts)


n54.add('C4', (2, 3, 4, 5))(n54_c4)

CHAPTERS[5] = [n51, n52, n53, n54]


# ================================================================ Chapter 6 Numerical solutions of equations

def num_family(r):
    """An equation f(x) = 0 with a convergent rearrangement x = F(x). Returns dict or None."""
    kind = r.choice(['cubic', 'cubic2', 'explin', 'lnquad', 'cos', 'expsq', 'recip'])
    if kind == 'cubic':
        p, q = r.randint(2, 9), r.randint(3, 30)
        d = dict(eq=f'x³ + {p}x − {q} = 0', f=lambda x: x ** 3 + p * x - q, F=lambda x: math.copysign(abs(q - p * x) ** (1 / 3), q - p * x),
                 Ft=f'∛({q} − {p}x)', rearr=f'x³ = {q} − {p}x', bad=f'x = ({q} − x³)/{p}', Fbad=lambda x: (q - x ** 3) / p)
    elif kind == 'cubic2':
        k = r.randint(2, 20)
        d = dict(eq=f'x³ − x − {k} = 0', f=lambda x: x ** 3 - x - k, F=lambda x: (x + k) ** (1 / 3), Ft=f'∛(x + {k})', rearr=f'x³ = x + {k}',
                 bad=f'x = x³ − {k}', Fbad=lambda x: x ** 3 - k)
    elif kind == 'explin':
        k = r.randint(3, 12)
        d = dict(eq=f'eˣ + x − {k} = 0', f=lambda x: math.exp(x) + x - k, F=lambda x: math.log(k - x), Ft=f'ln({k} − x)', rearr=f'eˣ = {k} − x',
                 bad=f'x = {k} − eˣ', Fbad=lambda x: k - math.exp(x))
    elif kind == 'lnquad':
        k = r.randint(3, 15)
        d = dict(eq=f'ln x + x² − {k} = 0', f=lambda x: math.log(x) + x * x - k, F=lambda x: math.sqrt(k - math.log(x)), Ft=f'√({k} − ln x)', rearr=f'x² = {k} − ln x',
                 bad=f'x = e^({k} − x²)', Fbad=lambda x: math.exp(k - x * x))
    elif kind == 'cos':
        k = r.choice([Fr(1, 2), Fr(3, 4), Fr(2, 3), Fr(1, 3), Fr(4, 5)])
        kf = float(k)
        d = dict(eq=f'x − {num(k)} cos x = 0', f=lambda x: x - kf * math.cos(x), F=lambda x: kf * math.cos(x), Ft=f'{num(k)} cos x', rearr=f'x = {num(k)} cos x',
                 bad=f'x = cos⁻¹({num(1 / k)}x)', Fbad=lambda x: math.acos(max(-1, min(1, x / kf))))
    elif kind == 'expsq':
        k = r.randint(2, 9)
        d = dict(eq=f'x² − e^(−x) − {k} = 0', f=lambda x: x * x - math.exp(-x) - k, F=lambda x: math.sqrt(k + math.exp(-x)), Ft=f'√({k} + e^(−x))', rearr=f'x² = {k} + e^(−x)',
                 bad=f'x = −ln(x² − {k})', Fbad=lambda x: -math.log(x * x - k) if x * x > k else 0)
    else:
        k = r.randint(2, 9)
        d = dict(eq=f'x³ − {k}x − 1 = 0', f=lambda x: x ** 3 - k * x - 1, F=lambda x: math.sqrt(k + 1 / x), Ft=f'√({k} + 1/x)', rearr=f'x³ = {k}x + 1',
                 bad=f'x = (x³ − 1)/{k}', Fbad=lambda x: (x ** 3 - 1) / k)
    f, F = d['f'], d['F']
    # locate the positive root by scanning
    lo = 0.05 if kind in ('lnquad', 'recip') else 0.0
    xs = [lo + i * 0.05 for i in range(200)]
    root = None
    for a_, b_ in zip(xs, xs[1:]):
        try:
            if f(a_) == 0 or (f(a_) < 0) != (f(b_) < 0):
                root = bisect(f, a_, b_)
                break
        except (ValueError, ZeroDivisionError):
            continue
    if root is None or root < 0.2:
        return None
    try:
        dF = ndiff(F, root, 1e-6)
        if not ok(F(root), root, 'iter fixed point ' + kind, 1e-7) or abs(dF) >= 0.8:
            return None
    except (ValueError, ZeroDivisionError):
        return None
    d.update(kind=kind, root=root, dF=dF)
    lo_i = math.floor(root * 2) / 2
    d['int'] = (lo_i, lo_i + 0.5)
    try:
        d['fa'], d['fb'] = f(d['int'][0]), f(d['int'][1])
    except (ValueError, ZeroDivisionError):
        return None
    if d['int'][0] <= 0 and kind in ('lnquad', 'recip'):
        return None
    return d


def iterate(F, x0, dp_=2, maxit=30):
    xs = [x0]
    for _ in range(maxit):
        xs.append(F(xs[-1]))
        if len(xs) >= 3 and round(xs[-1], dp_) == round(xs[-2], dp_) and abs(xs[-1] - xs[-2]) < 0.5 * 10 ** -(dp_ + 1):
            break
    return xs


def ivals(xs):
    return ', '.join(f'{x:.4f}' for x in xs)


s61 = T('Locating roots by sign change and graphically', 'locating roots by sign change', 'sign change')
s61.fixed('C1', (1, 2), [
    ('f is continuous and f(1) = −0.4, f(2) = 1.3. What can be concluded?', 'There is at least one root of f(x) = 0 between 1 and 2', 'A continuous function changing sign must cross zero.', ['There is exactly one root between 1 and 2', 'There is no root between 1 and 2', 'The root is at 1.5']),
    ('How many roots has the equation eˣ = −x?', '1', 'y = eˣ is increasing and y = −x is decreasing, so they meet exactly once.', ['0', '2', '3']),
    ('Which condition is needed for the sign-change method to guarantee a root in [a, b]?', 'f is continuous on [a, b]', 'A discontinuity can produce a sign change without a root.', ['f is increasing on [a, b]', 'f(a) > 0', 'f is a polynomial']),
])
s61.fixed('C2', (2, 3), [
    ('Explain why f(x) = 1/(x − 2) changes sign between x = 1 and x = 3 but f(x) = 0 has no root there.', 'f has a vertical asymptote (discontinuity) at x = 2, so it jumps from negative to positive without passing through zero; 1/(x − 2) is never 0.', 'B1 discontinuity at x = 2; B1 1/(x − 2) ≠ 0 for any x [2]'),
    ('Explain why there may be roots of f(x) = 0 between a and b even when f(a) and f(b) have the same sign.', 'There could be two roots (or a repeated root) in the interval, so the graph crosses the axis twice (or touches it) and returns to the same sign.', 'B1 even number of roots or a repeated root; B1 sign returns to the original [2]'),
])


@s61.add('C1', (1, 2, 3))
def s61_c1(r, D):
    d = num_family(r)
    if not d:
        return None
    a, b = d['int']
    if D == 1:
        lo = math.floor(d['root'])
        opts = [f'{lo} and {lo + 1}', f'{lo + 1} and {lo + 2}', f'{max(0, lo - 1)} and {max(1, lo)}' if lo >= 1 else f'{lo + 2} and {lo + 3}', f'{lo + 3} and {lo + 4}']
        return MC(r, f'The equation {d["eq"]} has one positive root α. Between which pair of consecutive integers does α lie?', opts[0], opts[1:], f'f({lo}) and f({lo + 1}) have opposite signs.')
    return MC(r, f'For f(x) = {d["eq"][:-4]}, f({num(a)}) = {n3(d["fa"])} and f({num(b)}) = {n3(d["fb"])}. Which conclusion is correct?', f'f(x) = 0 has a root between {num(a)} and {num(b)}',
              [f'f(x) = 0 has no root between {num(a)} and {num(b)}', f'the root is {num((a + b) / 2)}', f'f(x) = 0 has a root greater than {num(b)} only', f'f(x) = 0 has two roots between {num(a)} and {num(b)}'],
              'f is continuous and changes sign, so there is a root in the interval.')


@s61.add('C2', (1, 2, 3, 4), 'explain')
def s61_err(r, D):
    nm = person(r)
    f = r.choice(['asym', 'double', 'conc'])
    if f == 'asym':
        c = r.randint(1, 6)
        k = r.randint(1, 5)
        stem = f'{nm} evaluates f(x) = {k}/(x − {c}) at x = {c - 1} and x = {c + 1}, finds a change of sign and concludes that f(x) = 0 has a root between {c - 1} and {c + 1}. Explain why this conclusion is wrong.'
        return Q(stem, f'f is not continuous: it has a vertical asymptote at x = {c}, where it jumps from −∞ to +∞. {k}/(x − {c}) is never zero, so there is no root.', f'B1 discontinuity at x = {c}; B1 f(x) ≠ 0 for all x')
    if f == 'double':
        p = r.randint(1, 5)
        q = r.choice([x for x in range(-3, 9) if x not in (p, 0)])
        lo, hi = p - 1, p + 1
        if lo < q < hi:
            return None
        g = lambda x: (x - p) ** 2 * (x - q)
        if (g(lo) < 0) != (g(hi) < 0):
            return None
        stem = f'{nm} finds that f(x) = (x − {p})²(x{sg(-q)}) has f({lo}) = {num(g(lo))} and f({hi}) = {num(g(hi))}, which have the same sign, and concludes that there is no root between {lo} and {hi}. Explain why {nm} is wrong.'
        return Q(stem, f'x = {p} is a repeated root: the graph touches the x-axis at x = {p} without crossing, so f does not change sign even though there is a root in the interval.',
                 f'B1 repeated root at x = {p}; B1 graph touches without crossing, so no sign change')
    d = num_family(r)
    if not d:
        return None
    a, b = d['int']
    stem = f'Explain how the values f({num(a)}) = {n3(d["fa"])} and f({num(b)}) = {n3(d["fb"])} show that the equation {d["eq"]} has a root between {num(a)} and {num(b)}.'
    return Q(stem, f'f is continuous for the values considered, and f({num(a)}) and f({num(b)}) have opposite signs, so f(x) = 0 somewhere in between.', 'B1 opposite signs; B1 f continuous so a root lies in the interval')


@s61.add('C3', (1, 2, 3, 4, 5), 'numerical')
def s61_calc(r, D):
    d = num_family(r)
    if not d:
        return None
    a, b = d['int']
    if D <= 2:
        return Q(f'Show by calculation that the equation {d["eq"]} has a root between x = {num(a)} and x = {num(b)}.', f'f({num(a)}) = {n3(d["fa"])}, f({num(b)}) = {n3(d["fb"])}: change of sign',
                 f'M1 evaluates f({num(a)}) and f({num(b)}); A1 values {n3(d["fa"])} and {n3(d["fb"])} with correct conclusion')
    if D in (3, 4):
        lo = math.floor(d['root'] * 10) / 10
        hi = lo + 0.1
        f = d['f']
        return Q(f'Show that the equation {d["eq"]} has a root α between {num(a)} and {num(b)}, and by considering a further sign change, show that α lies between {num(round(lo, 1))} and {num(round(hi, 1))}.',
                 f'f({num(a)}) = {n3(d["fa"])}, f({num(b)}) = {n3(d["fb"])}; f({num(round(lo, 1))}) = {n3(f(lo))}, f({num(round(hi, 1))}) = {n3(f(hi))}',
                 f'M1 sign change on [{num(a)}, {num(b)}]; A1 conclusion; M1 evaluates at {num(round(lo, 1))} and {num(round(hi, 1))}; A1 values and conclusion')
    kind = r.choice(['explin', 'lnx'])
    k = r.randint(2, 9)
    if kind == 'explin':
        g = lambda x: math.exp(-x) - (x - k) ** 2 / k
        desc = f'e^(−x) = (x − {k})²/{k}'
        curves = f'y = e^(−x) and y = (x − {k})²/{k}'
    else:
        g = lambda x: math.log(x) - (k - x * x) if x > 0 else -1e9
        desc = f'ln x = {k} − x²'
        curves = f'y = ln x and y = {k} − x²'
    grid = [0.01 + i * 0.01 for i in range(1, 2000)]
    cnt = sum(1 for p, q in zip(grid, grid[1:]) if (g(p) < 0) != (g(q) < 0))
    if kind == 'explin':
        grid2 = [-10 + i * 0.01 for i in range(1, 1000)]
        cnt += sum(1 for p, q in zip(grid2, grid2[1:]) if (g(p) < 0) != (g(q) < 0))
    return Q(f'By sketching the graphs of {curves} on the same diagram, state the number of roots of the equation {desc}.', str(cnt),
             f'B1 correct sketch of each curve; B1 {cnt} point{"s" if cnt != 1 else ""} of intersection; B1 states {cnt} root{"s" if cnt != 1 else ""}')


def s61_c4(r, D):
    d = num_family(r)
    if not d:
        return None
    a, b = d['int']
    f = d['f']
    lo = math.floor(d['root'] * 100) / 100
    intro = f'The equation {d["eq"]} has exactly one positive root, α.'
    parts = [
        P(f'Show by calculation that α lies between {num(a)} and {num(b)}.', f'f({num(a)}) = {n3(d["fa"])}, f({num(b)}) = {n3(d["fb"])}', 'M1 evaluates both; A1 sign change and conclusion'),
        P(f'Show that the equation can be written in the form x = {d["Ft"]}.', f'{d["rearr"]}, hence x = {d["Ft"]}', 'M1 rearranges; A1 correct form shown'),
        P(f'Use the iterative formula xₙ₊₁ = {d["Ft"].replace("x", "xₙ")} with x₁ = {num(a)} to find α correct to 2 decimal places.', f'α = {d["root"]:.2f}',
          f'M1 uses the iteration correctly at least once; A1 final answer {d["root"]:.2f}; B1 shows sufficient iterations to justify 2 d.p.'),
        P(f'Verify by a sign change that α = {d["root"]:.2f} correct to 2 decimal places.', f'f({lo + 0.005:.3f}) and f({lo + 0.005 + 0.01:.3f}) differ in sign' if round(d['root'], 2) == round(lo, 2) else 'sign change on [α − 0.005, α + 0.005]',
          'M1 evaluates f at the bounds of the rounding interval; A1 sign change shown'),
    ]
    rr = round(d['root'], 2)
    if abs(d['root'] - (math.floor(d['root'] * 100) + 0.5) / 100) < 2e-4:
        return None
    parts[3] = P(f'Verify by a sign change that α = {rr:.2f} correct to 2 decimal places.', f'f({rr - 0.005:.3f}) = {n3(f(rr - 0.005))}, f({rr + 0.005:.3f}) = {n3(f(rr + 0.005))}: sign change',
                 'M1 evaluates f at the bounds of the rounding interval; A1 sign change shown')
    return cmp_(r, intro, parts)


s61.add('C4', (2, 3, 4, 5))(s61_c4)


# ---------------------------------------------------------------- 6.2 iterative formulae and convergence

s62 = T('Iterative formulae xₙ₊₁ = F(xₙ) and convergence', 'iterative formulae', 'convergence')
s62.fixed('C1', (1, 2), [
    ('If the iteration xₙ₊₁ = F(xₙ) converges to α, which equation does α satisfy?', 'α = F(α)', 'Taking limits on both sides.', ['F(α) = 0', 'F′(α) = 0', 'α = F′(α)']),
    ('Which condition near the root α usually makes xₙ₊₁ = F(xₙ) converge?', '|F′(α)| < 1', 'The error is multiplied by roughly F′(α) each step.', ['|F′(α)| > 1', 'F(α) = 0', 'F′(α) = 1']),
    ('On a cobweb or staircase diagram, the iteration xₙ₊₁ = F(xₙ) is shown using which two graphs?', 'y = F(x) and y = x', 'Successive values bounce between the curve and the line y = x.', ['y = F(x) and y = 0', 'y = F′(x) and y = x', 'y = F(x) and x = 0']),
])
s62.fixed('C2', (2, 3), [
    ('Explain why an iteration xₙ₊₁ = F(xₙ) with F′(α) slightly less than 0 produces a cobweb rather than a staircase diagram.', 'A negative gradient means successive iterates fall alternately above and below α, so the diagram spirals (cobweb) rather than approaching from one side.', 'B1 negative gradient gives oscillation about α; B1 cobweb [2]'),
    ('Explain why two different rearrangements of the same equation can behave differently under iteration.', 'Each rearrangement x = F(x) has a different function F; convergence depends on |F′(α)|, which can be less than 1 for one rearrangement and greater than 1 for another.', 'B1 different F; B1 convergence depends on |F′(α)| < 1 [2]'),
])


@s62.add('C1', (1, 2, 3))
def s62_c1(r, D):
    d = num_family(r)
    if not d:
        return None
    x0 = d['int'][0] if d['int'][0] > 0 else d['int'][1]
    x1 = d['F'](x0)
    if D == 1:
        return MC(r, f'The iterative formula xₙ₊₁ = {d["Ft"].replace("x", "xₙ")} is used with x₁ = {num(x0)}. Find x₂, correct to 4 decimal places.', f'{x1:.4f}',
                  [f'{d["F"](x1):.4f}', f'{d["f"](x0):.4f}', f'{x0 + d["f"](x0):.4f}', f'{x1 + 0.01:.4f}'], f'x₂ = F({num(x0)}) = {x1:.4f}.')
    if D == 2:
        return MC(r, f'The sequence defined by xₙ₊₁ = {d["Ft"].replace("x", "xₙ")} converges to α. Which equation is satisfied by α?', d['eq'].replace('x', 'α'),
                  [d['eq'].replace('x', 'α').replace(' − ', ' + ', 1), f'α = 0', d['eq'].replace('x', 'α').replace(' = 0', ' = 1')], 'At the limit, α = F(α); rearrange.')
    return MC(r, f'For the iteration xₙ₊₁ = {d["Ft"].replace("x", "xₙ")} converging to α ≈ {d["root"]:.3f}, the value of F′(α) is about {n3(d["dF"])}. How do the iterates approach α?',
              'oscillating about α (cobweb)' if d['dF'] < 0 else 'from one side (staircase)', ['oscillating about α (cobweb)' if d['dF'] >= 0 else 'from one side (staircase)', 'they diverge', 'they reach α after one step', 'they move away from α then return'],
              'Negative F′ gives a cobweb; positive gives a staircase; |F′| < 1 so it converges.')


@s62.add('C2', (1, 2, 3, 4), 'explain')
def s62_err(r, D):
    nm = person(r)
    d = num_family(r)
    if not d:
        return None
    f = r.choice(['show', 'diverge'])
    if f == 'show':
        return Q(f'Show that the equation {d["eq"]} can be rearranged into the form x = {d["Ft"]}.', f'{d["eq"]} ⇒ {d["rearr"]} ⇒ x = {d["Ft"]}', 'M1 rearranges correctly; A1 reaches the given form with no errors')
    try:
        g = ndiff(d['Fbad'], d['root'], 1e-6)
    except (ValueError, ZeroDivisionError):
        return None
    if abs(g) <= 1.05:
        return None
    stem = f'{nm} tries to find the positive root α ≈ {d["root"]:.2f} of {d["eq"]} using the rearrangement {d["bad"]} and finds that the iterates move away from α. Explain why, and suggest a rearrangement that converges.'
    return Q(stem, f'For F(x) = {d["bad"][4:]}, |F′(α)| ≈ {n3(abs(g))} > 1, so errors grow each step. Use x = {d["Ft"]}, for which |F′(α)| ≈ {n3(abs(d["dF"]))} < 1.',
             f'B1 |F′(α)| > 1 for {nm}’s rearrangement (≈ {n3(abs(g))}); B1 suggests x = {d["Ft"]} with |F′(α)| < 1')


@s62.add('C3', (1, 2, 3, 4, 5), 'numerical')
def s62_calc(r, D):
    d = num_family(r)
    if not d:
        return None
    x0 = d['int'][1]
    F = d['F']
    xs = [x0]
    for _ in range(3):
        xs.append(F(xs[-1]))
    if D <= 2:
        return Q(f'Use the iterative formula xₙ₊₁ = {d["Ft"].replace("x", "xₙ")} with x₁ = {num(x0)} to find x₂, x₃ and x₄, giving each to 4 decimal places.', ivals(xs[1:]),
                 f'M1 correct use of the formula; A1 x₂ = {xs[1]:.4f}; A1 x₃ and x₄')
    if D == 3:
        return Q(f'The sequence defined by xₙ₊₁ = {d["Ft"].replace("x", "xₙ")} converges to α. State an equation satisfied by α and show that it is equivalent to {d["eq"]}.',
                 f'α = {d["Ft"].replace("x", "α")}; rearranging gives {d["eq"].replace("x", "α")}', 'B1 α = F(α); M1 rearranges; A1 shows equivalence')
    dF = d['dF']
    return Q(f'The iteration xₙ₊₁ = {d["Ft"].replace("x", "xₙ")} converges to α = {d["root"]:.3f} (to 3 d.p.). By finding F′(α), explain why the iteration converges and state whether the iterates approach α from one side or oscillate about it.',
             f'F′(α) ≈ {n3(dF)}; |F′(α)| < 1 so it converges; {"oscillates (cobweb)" if dF < 0 else "approaches from one side (staircase)"}',
             f'M1 differentiates F; A1 F′(α) ≈ {n3(dF)}; B1 |F′(α)| < 1; B1 {"negative so cobweb" if dF < 0 else "positive so staircase"}')


def s62_c4(r, D):
    d = num_family(r)
    if not d:
        return None
    x0 = d['int'][1]
    xs = iterate(d['F'], x0, 3)
    if abs(round(xs[-1], 3) - round(d['root'], 3)) > 1e-9:
        return None
    intro = f'The equation {d["eq"]} has one positive root α.'
    parts = [
        P(f'Show that α lies between {num(d["int"][0])} and {num(d["int"][1])}.', f'f({num(d["int"][0])}) = {n3(d["fa"])}, f({num(d["int"][1])}) = {n3(d["fb"])}', 'M1 evaluates; A1 sign change'),
        P(f'Show that the equation can be written as x = {d["Ft"]}.', d['rearr'], 'B1 correct rearrangement'),
        P(f'Use the iterative formula xₙ₊₁ = {d["Ft"].replace("x", "xₙ")} with x₁ = {num(x0)} to find α correct to 3 decimal places. Give the result of each iteration to 5 decimal places.',
          f'α = {d["root"]:.3f}', f'M1 iterates correctly; A1 {d["root"]:.3f}; B1 sufficient iterations shown ({", ".join(f"{x:.5f}" for x in xs[1:5])}, …)'),
        P('Explain, with reference to F′(α), why the iteration converges.', f'|F′(α)| ≈ {n3(abs(d["dF"]))} < 1', f'B1 F′(α) ≈ {n3(d["dF"])}, |F′(α)| < 1'),
    ]
    return cmp_(r, intro, parts)


s62.add('C4', (2, 3, 4, 5))(s62_c4)


# ---------------------------------------------------------------- 6.3 iteration to a given accuracy

s63 = T('Using iteration to solve equations to a given accuracy', 'using iteration to solve equations', 'given accuracy')
s63.fixed('C1', (1, 2), [
    ('An iteration gives x₅ = 1.2347 and x₆ = 1.2351. What is the root correct to 2 decimal places, assuming convergence?', '1.23', 'Both round to 1.23.', ['1.24', '1.235', '1.2']),
    ('To confirm that α = 2.47 correct to 2 d.p. using f(x) = 0, which values should be checked for a sign change?', 'f(2.465) and f(2.475)', 'These are the bounds of the rounding interval.', ['f(2.46) and f(2.48)', 'f(2.47) and f(2.48)', 'f(2.4) and f(2.5)']),
    ('Iterates are given to 4 d.p. to find a root correct to 2 d.p. Why?', 'To show that the iterates have settled to 2 d.p. without rounding errors affecting the result', 'More figures than required are kept until the end.', ['Because the answer must be given to 4 d.p.', 'Because the iteration diverges otherwise', 'Because calculators show 4 d.p.']),
])
s63.fixed('C2', (2, 3), [
    ('Explain why stopping an iteration as soon as two successive values agree to 2 d.p. is usually, but not always, enough to give the root to 2 d.p.', 'Successive agreement suggests the iterates have settled, but if the root is very close to a rounding boundary, later iterates could round differently; a sign-change check on [α − 0.005, α + 0.005] confirms it.', 'B1 agreement indicates convergence to that accuracy; B1 confirm with a sign change at the rounding bounds [2]'),
])


@s63.add('C1', (1, 2, 3))
def s63_c1(r, D):
    d = num_family(r)
    if not d:
        return None
    rr = round(d['root'], 2)
    if D <= 2:
        xs = iterate(d['F'], d['int'][1], 2)
        a, b = xs[-2], xs[-1]
        return MC(r, f'Successive iterates of xₙ₊₁ = {d["Ft"].replace("x", "xₙ")} are {a:.4f} and {b:.4f}. State the root of {d["eq"]} correct to 2 decimal places.', f'{rr:.2f}',
                  [f'{rr + 0.01:.2f}', f'{rr - 0.01:.2f}', f'{b:.3f}', f'{round(rr, 1):.1f}'], f'Both iterates round to {rr:.2f}.')
    return MC(r, f'To verify that the root of {d["eq"]} is {rr:.2f} correct to 2 decimal places, which values of x should be substituted?', f'{rr - 0.005:.3f} and {rr + 0.005:.3f}',
              [f'{rr - 0.01:.2f} and {rr + 0.01:.2f}', f'{rr:.2f} and {rr + 0.01:.2f}', f'{rr - 0.05:.2f} and {rr + 0.05:.2f}'], 'Use the bounds of the interval that rounds to the stated value.')


@s63.add('C2', (1, 2, 3, 4), 'explain')
def s63_err(r, D):
    nm = person(r)
    d = num_family(r)
    if not d:
        return None
    xs = iterate(d['F'], d['int'][1], 2)
    rr = round(d['root'], 2)
    if len(xs) < 4:
        return None
    early = xs[2]
    if round(early, 2) == rr:
        early = xs[1]
    if round(early, 2) == rr:
        return None
    stem = f'{nm} uses xₙ₊₁ = {d["Ft"].replace("x", "xₙ")} with x₁ = {num(d["int"][1])}, stops at x = {early:.4f} and states that the root of {d["eq"]} is {early:.2f} correct to 2 decimal places. Explain why this is not justified and give the root correct to 2 decimal places.'
    return Q(stem, f'One value is not enough: iteration must continue until successive values agree to 2 d.p. (iterates: {ivals(xs[1:])}). Root = {rr:.2f}.',
             f'B1 must continue until successive iterates agree to 2 d.p. (or check a sign change); B1 {rr:.2f}')


@s63.add('C3', (1, 2, 3, 4, 5), 'numerical')
def s63_calc(r, D):
    d = num_family(r)
    if not d:
        return None
    dp_ = 2 if D <= 3 else 3
    x0 = d['int'][1] if D % 2 else d['int'][0]
    if x0 <= 0:
        x0 = d['int'][1]
    xs = iterate(d['F'], x0, dp_)
    rr = round(d['root'], dp_)
    if round(xs[-1], dp_) != rr:
        return None
    # avoid roots too close to a rounding boundary
    if abs(d['root'] * 10 ** dp_ - math.floor(d['root'] * 10 ** dp_) - 0.5) < 0.02:
        return None
    half = 0.5 * 10 ** -dp_
    f = d['f']
    if (f(rr - half) < 0) == (f(rr + half) < 0):
        return None
    shown = ', '.join(f'{x:.{dp_ + 2}f}' for x in xs[1:6]) + (', …' if len(xs) > 6 else '')
    stem = (f'Use the iterative formula xₙ₊₁ = {d["Ft"].replace("x", "xₙ")} with x₁ = {num(x0)} to determine the root of {d["eq"]} correct to {dp_} decimal places. '
            f'Give the result of each iteration to {dp_ + 2} decimal places.')
    if D == 5:
        stem += ' Verify your answer by considering a change of sign.'
        return Q(stem, f'{rr:.{dp_}f}', f'M1 iterates correctly ({shown}); A1 {rr:.{dp_}f}; B1 sufficient iterations; M1 f({rr - half:.{dp_ + 1}f}) and f({rr + half:.{dp_ + 1}f}); A1 opposite signs')
    return Q(stem, f'{rr:.{dp_}f}', f'M1 iterates correctly ({shown}); A1 {rr:.{dp_}f}; B1 shows enough iterations to justify the accuracy')


def s63_c4(r, D):
    d = num_family(r)
    if not d:
        return None
    xs = iterate(d['F'], d['int'][1], 2)
    rr = round(d['root'], 2)
    if round(xs[-1], 2) != rr or abs(d['root'] * 100 - math.floor(d['root'] * 100) - 0.5) < 0.05:
        return None
    f = d['f']
    intro = f'The equation {d["eq"]} has one positive root α.'
    parts = [
        P(f'Show by calculation that α lies between {num(d["int"][0])} and {num(d["int"][1])}.', f'f({num(d["int"][0])}) = {n3(d["fa"])}, f({num(d["int"][1])}) = {n3(d["fb"])}', 'M1 evaluates both; A1 sign change and conclusion'),
        P(f'Show that α satisfies x = {d["Ft"]}.', d['rearr'], 'B1 correct rearrangement'),
        P(f'Use the iterative formula xₙ₊₁ = {d["Ft"].replace("x", "xₙ")} to determine α correct to 2 decimal places, giving each iterate to 4 decimal places.', f'{rr:.2f}',
          f'M1 iterates from a value in the interval ({ivals(xs[1:5])}, …); A1 {rr:.2f}; B1 sufficient iterations'),
        P(f'Verify that α = {rr:.2f} correct to 2 decimal places.', f'f({rr - 0.005:.3f}) = {n3(f(rr - 0.005))}, f({rr + 0.005:.3f}) = {n3(f(rr + 0.005))}', 'M1 evaluates at the bounds; A1 sign change'),
    ]
    return cmp_(r, intro, parts)


s63.add('C4', (2, 3, 4, 5))(s63_c4)

CHAPTERS[6] = [s61, s62, s63]


# ================================================================ Chapter 7 Further algebra

def lf2(u, v, v_='x'):
    """Linear factor text: x, 2x, (x − 3), (2x + 1)."""
    if v == 0:
        return v_ if u == 1 else f'{u}{v_}'
    return f'({lin(u, v, v_)})'


def fpow(t, k):
    return t if k == 1 else (f'{t}{sup(k)}' if t.startswith('(') or len(t) == 1 else f'({t}){sup(k)}')


def ser(N, Dn, n):
    """Maclaurin coefficients c0..cn (low to high) of N(x)/D(x); polynomials given high to low."""
    Nl = [Fr(c) for c in reversed(ptrim(N))]
    Dl = [Fr(c) for c in reversed(ptrim(Dn))]
    if Dl[0] == 0:
        raise ValueError('D(0) = 0')
    out = []
    for k in range(n + 1):
        s = (Nl[k] if k < len(Nl) else Fr(0)) - sum(out[j] * (Dl[k - j] if k - j < len(Dl) else 0) for j in range(k))
        out.append(s / Dl[0])
    return out


def asc(cs, v='x'):
    """Ascending-power polynomial text from low-to-high coefficients."""
    return poly([(c, i) for i, c in enumerate(cs)], v)


def sumfr(items):
    """Join signed fractional terms [(coef, 'text over den')] -> '3/(x − 1) − 2/(x + 2)'."""
    out = ''
    for c, den in items:
        if c == 0:
            continue
        body = f'{num(abs(Fr(c)))}/{den}'
        if not out:
            out = (MINUS if c < 0 else '') + body
        else:
            out += (' − ' if c < 0 else ' + ') + body
    return out


def pf_case(r, D, kind=None):
    """A rational function with linear (possibly repeated) factors. Returns dict with N (high to low),
    den text, terms [(coef, u, v, power)], const c, answer text, f (float) and g (float, PF form)."""
    kind = kind or {1: 'two', 2: r.choice(['two', 'xfac']), 3: r.choice(['nonunit', 'three']), 4: r.choice(['rep', 'rep', 'three']), 5: r.choice(['improper', 'reprep', 'rep'])}[D]
    pool = [x for x in range(-5, 6) if x != 0]
    c0 = 0
    if kind in ('two', 'improper'):
        p, q = r.sample(pool, 2)
        facs = [(1, p, 1), (1, q, 1)]
    elif kind == 'xfac':
        q = r.choice(pool)
        facs = [(1, 0, 1), (1, q, 1)]
    elif kind == 'nonunit':
        u = r.choice([2, 3])
        v = r.choice([x for x in pool if math.gcd(x, u) == 1])
        q = r.choice(pool)
        facs = [(u, v, 1), (1, q, 1)]
    elif kind == 'three':
        p, q, s = r.sample([x for x in range(-4, 5)], 3)
        facs = [(1, p, 1), (1, q, 1), (1, s, 1)]
    elif kind == 'rep':
        p, q = r.sample(pool, 2)
        facs = [(1, p, 1), (1, q, 2)]
    else:
        u = r.choice([2, 3])
        v = r.choice([x for x in pool if math.gcd(x, u) == 1])
        q = r.choice(pool)
        facs = [(u, v, 1), (1, q, 2)] if r.random() < 0.5 else [(1, q, 1), (u, v, 2)]
    terms = []
    for (u, v, m) in facs:
        for k in range(1, m + 1):
            terms.append([nz(r, -6, 6), u, v, k])
    if kind == 'improper':
        c0 = nz(r, -4, 4)
    den = [Fr(1)]
    for (u, v, m) in facs:
        for _ in range(m):
            den = pmul(den, [u, v])
    N = [Fr(c0) * x for x in den]
    for c, u, v, k in terms:
        part = [Fr(c)]
        for (u2, v2, m2) in facs:
            reps = m2 - (k if (u2, v2) == (u, v) else 0)
            for _ in range(reps):
                part = pmul(part, [u2, v2])
        N = padd(N, part)
    N = ptrim(N)
    if N == [0]:
        return None
    # numerator must not share a factor with the denominator (else the PF form would be reducible)
    for (u, v, m) in facs:
        if pval(N, Fr(-v, u)) == 0:
            return None
    dtxt = ''.join(fpow(lf2(u, v), m) for (u, v, m) in facs)
    items = [(c, fpow(lf2(u, v), k)) for c, u, v, k in terms]
    ans = sumfr(items)
    if c0:
        ans = num(c0) + (' + ' + ans if not ans.startswith(MINUS) else ' − ' + ans[1:])
    f = lambda x: float(pval(N, x)) / float(pval(den, x))
    g = lambda x: c0 + sum(c / (u * x + v) ** k for c, u, v, k in terms)
    for x in (0.37, 1.91, -2.73):
        try:
            if not ok(f(x), g(x), 'pf ' + kind, 1e-9):
                return None
        except ZeroDivisionError:
            continue
    form = ' + '.join(f'{"ABCD"[i]}/{fpow(lf2(u, v), k)}' for i, (c, u, v, k) in enumerate(terms))
    if c0:
        form = 'A + ' + ' + '.join(f'{"BCDE"[i]}/{fpow(lf2(u, v), k)}' for i, (c, u, v, k) in enumerate(terms))
    return dict(N=N, den=den, dtxt=dtxt, ftxt=f'({pstr(N)})/({dtxt})' if len(N) > 1 else f'{num(N[0])}/({dtxt})', terms=terms, c0=c0, ans=ans,
                f=f, g=g, facs=facs, kind=kind, form=form)


def ftext(d):
    return d['ftxt'].replace('/((', '/(').replace('))', ')') if d['dtxt'].count('(') == 1 and d['dtxt'].startswith('(') and d['dtxt'].endswith(')') and '²' not in d['dtxt'] else d['ftxt']


m71 = T('Partial fractions with linear and repeated linear denominators', 'partial fractions', 'repeated linear factor')
m71.fixed('C1', (1, 2), [
    ('Which is the correct form of the partial fractions for (3x + 1)/((x − 2)(x + 1)²)?', 'A/(x − 2) + B/(x + 1) + C/(x + 1)²', 'A repeated factor (x + 1)² needs terms in both (x + 1) and (x + 1)².',
     ['A/(x − 2) + B/(x + 1)²', 'A/(x − 2) + (Bx + C)/(x + 1)²', 'A/(x − 2) + B/(x + 1)']),
    ('Before writing (x² + 3)/((x − 1)(x + 2)) in partial fractions, what must be done first?', 'Divide, because the degree of the numerator is not less than the degree of the denominator', 'The fraction is improper.',
     ['Nothing; write A/(x − 1) + B/(x + 2) directly', 'Factorise the numerator', 'Multiply the numerator by x']),
    ('In the identity 5x − 1 ≡ A(x + 1) + B(x − 2), which value of x gives B directly?', 'x = −1', 'Substituting x = −1 makes the A term zero.', ['x = 2', 'x = 1', 'x = 0']),
])
m71.fixed('C2', (2, 3), [
    ('Explain why the "cover-up" method gives the coefficient of 1/(x − 3) in (2x + 1)/((x − 3)(x + 4)) as 7/7 = 1.', 'Multiplying by (x − 3) and setting x = 3 removes the other term: A = (2·3 + 1)/(3 + 4) = 7/7 = 1.', 'B1 multiplies through and substitutes x = 3; B1 obtains 1 [2]'),
    ('Explain why a repeated factor (x − a)² in a denominator needs two partial fractions, A/(x − a) and B/(x − a)².', 'With only B/(x − a)² the combined numerator over (x − a)² would be constant, so a numerator of the form A(x − a) + B, a general linear expression, could not be matched.', 'B1 only constant numerator otherwise; B1 two terms give a general linear numerator [2]'),
])


@m71.add('C1', (1, 2, 3))
def m71_c1(r, D):
    d = pf_case(r, min(D + 1, 4))
    if not d:
        return None
    if D == 1 or len(d['terms']) == 2:
        c, u, v, k = d['terms'][0]
        x0 = Fr(-v, u)
        return MC(r, f'Given that {ftext(d)} ≡ A/{fpow(lf2(u, v), k)} + …, find A.', num(c),
                  [num(-c), num(c + 1), num(c * 2) if c != 0 else '2', num(c - 1), num(pval(d['N'], x0))], f'Cover up {lf2(u, v)} and substitute x = {num(x0)}.')
    wrong = [d['form'].replace('²', ''), d['form'].split(' + ')[0] + ' + ' + d['form'].split(' + ')[-1], d['form'].replace('B/', '(Bx + C)/', 1).replace(' + C/', ' + D/')]
    return MC(r, f'Which is the correct form of the partial fractions for {ftext(d)}?', d['form'], wrong, 'One term for each linear factor, and one for each power of a repeated factor.')


@m71.add('C2', (1, 2, 3, 4), 'explain')
def m71_err(r, D):
    nm = person(r)
    d = pf_case(r, max(2, min(D + 1, 5)))
    if not d:
        return None
    f = r.choice(['wrongval', 'missrep', 'check'])
    if f == 'missrep' and any(k == 2 for _, _, _, k in d['terms']):
        bad = ' + '.join(t for t in d['form'].split(' + ') if not ('/(' in t and t.split('/')[1].endswith(')') and t.split('/')[1] + '²' in d['form']))
        return Q(f'{nm} writes {ftext(d)} ≡ {bad}. Explain why this form cannot work and state the correct form.',
                 f'The repeated factor needs a term for each power, otherwise the identity cannot hold for all x. Correct form: {d["form"]}.',
                 'B1 a term is missing for the repeated factor; B1 correct form stated')
    c, u, v, k = d['terms'][0]
    x0 = Fr(-v, u)
    if f == 'wrongval' and k == 1:
        w = c + r.choice([-2, -1, 1, 2])
        return Q(f'{nm} claims that the coefficient of 1/{lf2(u, v)} in the partial fractions of {ftext(d)} is {num(w)}. Without finding the other coefficients, show that {nm} is wrong.',
                 f'Multiply by {lf2(u, v)} and substitute x = {num(x0)}: the coefficient is {num(c)}, not {num(w)}.', f'M1 substitutes x = {num(x0)} after multiplying through; A1 obtains {num(c)}')
    return Q(f'Show that {d["ans"]} can be written as {ftext(d)}.', f'Combining over the common denominator {d["dtxt"]} gives numerator {pstr(d["N"])}.',
             'M1 common denominator; A1 numerator simplified correctly')


@m71.add('C3', (1, 2, 3, 4, 5), 'numerical')
def m71_calc(r, D):
    d = pf_case(r, D)
    if not d:
        return None
    n = len(d['terms']) + (1 if d['c0'] else 0)
    key = ('M1 divides first; ' if d['c0'] else '') + 'B1 correct form; M1 a valid method for the coefficients; ' + ' '.join(['A1'] * min(n, 3)) + ' coefficients'
    return Q(f'Express {ftext(d)} in partial fractions.', d['ans'], key)


def m71_c4(r, D):
    d = pf_case(r, r.choice([1, 2, 4]) if D < 4 else r.choice([4, 5]))
    if not d or d['c0'] or any(v == 0 for _, _, v, _ in d['terms']):
        return None
    cs = ser(d['N'], d['den'], 2)
    k = len(d['terms'])
    mn = min(abs(Fr(v, u)) for _, u, v, _ in d['terms'])
    nm = 'f(x)'
    intro = f'Let {nm} = {ftext(d)}.'
    parts = [
        P(f'Express {nm} in partial fractions.', d['ans'], 'B1 correct form; M1 method for coefficients; ' + ' '.join(['A1'] * min(k, 3))),
        P(f'Hence obtain the expansion of {nm} in ascending powers of x, up to and including the term in x².', asc(cs), 'M1 binomial expansion of each term; A1 two terms correct; A1 all correct'),
        P('State the set of values of x for which the expansion is valid.', f'|x| < {num(mn)}', 'B1 the smallest bound'),
        P(f'Find the value of {nm} when x = 0 and use it to check your expansion.', f'{num(cs[0])}', 'B1 constant term matches f(0)'),
    ]
    # numerical check of the series
    xs = 0.01 * float(mn)
    if not ok(d['f'](xs), float(cs[0] + cs[1] * Fr(xs) + cs[2] * Fr(xs) ** 2), 'm71 series', 1e-4 * max(1, abs(float(cs[0])))):
        return None
    return cmp_(r, intro, parts)


m71.add('C4', (2, 3, 4, 5))(m71_c4)


# ---------------------------------------------------------------- 7.2 quadratic factor

def pfq_case(r, D):
    """A/(ux + v) + (Bx + C)/(x² + k), optionally improper."""
    pool = [x for x in range(-5, 6) if x != 0]
    u = 1 if D <= 3 else r.choice([1, 2, 3])
    v = r.choice([x for x in range(-5, 6) if math.gcd(x, u) == 1 or x == 0]) if D >= 2 else r.choice(pool)
    if u > 1 and v == 0:
        v = 1
    k = r.choice([1, 2, 3, 4, 5, 9])
    A = nz(r, -5, 5)
    B = r.randint(-4, 4) if D >= 2 else 0
    C = r.randint(-5, 5)
    if B == 0 and C == 0:
        C = r.choice([1, 2, -1, 3])
    c0 = nz(r, -3, 3) if D == 5 and r.random() < 0.5 else 0
    q = [Fr(1), Fr(0), Fr(k)]
    den = pmul([u, v], q)
    N = padd(padd(pmul([A], q), pmul([B, C], [u, v])), [c0 * x for x in den])
    N = ptrim(N)
    if pval(N, Fr(-v, u)) == 0:
        return None
    lt = lf2(u, v)
    qt = f'(x² + {k})'
    dtxt = lt + qt
    first = f'{num(A)}/{lt}'
    if B < 0 or (B == 0 and C < 0):
        second = f' − ({lin(-B, -C)})/{qt}' if B != 0 else f' − {num(-C)}/{qt}'
    else:
        second = f' + ({lin(B, C)})/{qt}' if B != 0 else f' + {num(C)}/{qt}'
    ans = first + second
    if c0:
        ans = num(c0) + (' + ' + ans if A > 0 else ' − ' + ans[1:])
    f = lambda x: float(pval(N, x)) / float(pval(den, x))
    g = lambda x: c0 + A / (u * x + v) + (B * x + C) / (x * x + k)
    for x in (0.37, 1.91, -2.73):
        try:
            if not ok(f(x), g(x), 'pfq', 1e-9):
                return None
        except ZeroDivisionError:
            continue
    return dict(N=N, den=den, dtxt=dtxt, ftxt=(f'({pstr(N)})/({dtxt})' if len(N) > 1 else f'{num(N[0])}/({dtxt})'), A=A, B=B, C=C, k=k, u=u, v=v, c0=c0, ans=ans, f=f, lt=lt, qt=qt,
                form=('A + B/' + lt + ' + (Cx + D)/' + qt) if c0 else ('A/' + lt + ' + (Bx + C)/' + qt))


m72 = T('Partial fractions with a quadratic factor in the denominator', 'quadratic factor', 'partial fractions with a quadratic factor')
m72.fixed('C1', (1, 2), [
    ('Which is the correct form of the partial fractions for (x² + 5)/((x − 1)(x² + 4))?', 'A/(x − 1) + (Bx + C)/(x² + 4)', 'The numerator over an irreducible quadratic is linear.',
     ['A/(x − 1) + B/(x² + 4)', 'A/(x − 1) + B/(x + 2) + C/(x − 2)', 'A/(x − 1) + B/(x² + 4) + C/(x² + 4)²']),
    ('Why is x² + 9 left as a single factor in partial fractions?', 'It has no real linear factors (its discriminant is negative)', 'x² + 9 = 0 has no real roots.',
     ['Because it is a perfect square', 'Because 9 is odd', 'Because the numerator is quadratic']),
])
m72.fixed('C2', (2, 3), [
    ('Explain why the partial fraction over x² + k (k > 0) must have numerator Bx + C rather than just B.', 'The numerator over a quadratic denominator can be any polynomial of degree less than 2, so a general linear numerator Bx + C is needed for the identity to hold for all x.', 'B1 degree of numerator less than the degree of the denominator; B1 so a linear numerator Bx + C [2]'),
])


@m72.add('C1', (1, 2, 3))
def m72_c1(r, D):
    d = pfq_case(r, max(2, D))
    if not d:
        return None
    if D == 1:
        return MC(r, f'Which is the correct form of the partial fractions for {d["ftxt"]}?', d['form'],
                  [f'A/{d["lt"]} + B/{d["qt"]}', f'(Ax + B)/{d["lt"]} + C/{d["qt"]}', f'A/{d["lt"]} + B/(x + {rt(d["k"])}) + C/(x − {rt(d["k"])})' if d['k'] in (1, 4, 9) else f'A/{d["lt"]} + Bx/{d["qt"]}'],
                  'Linear numerator over the irreducible quadratic.')
    return MC(r, f'Given that {d["ftxt"]} ≡ A/{d["lt"]} + (Bx + C)/{d["qt"]}, find A.' if not d['c0'] else f'Given that {d["ftxt"]} ≡ A + B/{d["lt"]} + (Cx + D)/{d["qt"]}, find B.',
              num(d['A']), [num(-d['A']), num(d['A'] + 1), num(d['A'] - 1), num(pval(d['N'], Fr(-d['v'], d['u'])))], f'Multiply through by {d["lt"]} and put x = {num(Fr(-d["v"], d["u"]))}.')


@m72.add('C2', (1, 2, 3, 4), 'explain')
def m72_err(r, D):
    nm = person(r)
    d = pfq_case(r, max(2, min(D + 1, 4)))
    if not d or d['B'] == 0:
        return None
    f = r.choice(['constnum', 'show', 'compare'])
    if f == 'constnum':
        return Q(f'{nm} tries to write {d["ftxt"]} ≡ A/{d["lt"]} + B/{d["qt"]} and finds that the equations for A and B are inconsistent. Explain why, and state the form {nm} should use.',
                 f'Over x² + {d["k"]} the numerator must be linear; with only B the identity cannot match all coefficients. Use A/{d["lt"]} + (Bx + C)/{d["qt"]}.',
                 'B1 numerator over the quadratic must be linear; B1 correct form')
    if f == 'compare':
        return Q(f'In finding the partial fractions of {d["ftxt"]} in the form A/{d["lt"]} + (Bx + C)/{d["qt"]}, explain how comparing the coefficients of x² gives B once A = {num(d["A"])} is known.',
                 f'The x² terms of A(x² + {d["k"]}) + (Bx + C){d["lt"]} are (A + {num(d["u"]) if d["u"] != 1 else ""}B)x²; equating to the coefficient {num(d["N"][0] if len(d["N"]) == 3 else 0)} gives B = {num(d["B"])}.',
                 'M1 identifies the x² coefficients; A1 B found')
    return Q(f'Show that {d["ans"]} ≡ {d["ftxt"]}.', f'Common denominator {d["dtxt"]}; numerator {pstr(d["N"])}.', 'M1 common denominator; A1 numerator correct')


@m72.add('C3', (1, 2, 3, 4, 5), 'numerical')
def m72_calc(r, D):
    d = pfq_case(r, D)
    if not d:
        return None
    return Q(f'Express {d["ftxt"]} in partial fractions.', d['ans'], ('M1 divides first; ' if d['c0'] else '') + 'B1 correct form; M1 method for the coefficients; A1 A; A1 B and C')


def m72_c4(r, D):
    d = pfq_case(r, max(2, min(D, 4)))
    if not d or d['v'] == 0:
        return None
    cs = ser(d['N'], d['den'], 2)
    mn = min(abs(Fr(d['v'], d['u'])), Fr(math.isqrt(d['k'])) if math.isqrt(d['k']) ** 2 == d['k'] else Fr(99))
    lim = num(mn) if mn != 99 else None
    if math.isqrt(d['k']) ** 2 != d['k'] and abs(Fr(d['v'], d['u'])) > math.sqrt(d['k']):
        lim = f'√{d["k"]}'
    intro = f'Let f(x) = {d["ftxt"]}.'
    parts = [
        P('Express f(x) in partial fractions.', d['ans'], 'B1 correct form; M1 method for the coefficients; A1 A; A1 B and C'),
        P('Hence obtain the expansion of f(x) in ascending powers of x, up to and including the term in x².', asc(cs), 'M1 binomial expansion of each term; A1 two terms correct; A1 all correct'),
        P('State the set of values of x for which the expansion is valid.', f'|x| < {lim}', 'B1 the smaller bound'),
    ]
    xs = 0.005
    if not ok(d['f'](xs), float(cs[0] + cs[1] * Fr(xs) + cs[2] * Fr(xs) ** 2), 'm72 series', 1e-4 * max(1, abs(float(cs[0])))):
        return None
    return cmp_(r, intro, parts)


m72.add('C4', (2, 3, 4, 5))(m72_c4)


# ---------------------------------------------------------------- 7.3 binomial expansion for rational n

def gbin(n, k):
    c = Fr(1)
    for i in range(k):
        c *= (n - i)
    return c / math.factorial(k)


BN = [Fr(-1), Fr(-2), Fr(-3), Fr(1, 2), Fr(-1, 2), Fr(1, 3), Fr(-1, 3), Fr(3, 2), Fr(-3, 2), Fr(2, 3)]


def bin_case(r, D):
    n = r.choice(BN[:5] if D <= 2 else BN)
    if D <= 2:
        a = 1
    else:
        a = r.choice({1: [1, 2, 3], 2: [1, 4, 9], 3: [1, 8, 27]}[n.denominator] + ([1] if D == 3 else []))
    b = r.choice([x for x in range(-4, 5) if x != 0]) if D >= 2 else r.choice([-3, -2, 2, 3, 4, -4])
    if D == 5 and r.random() < 0.4:
        b = Fr(r.choice([1, -1, 3, -3]), r.choice([2, 3]))
    root = round(a ** (1 / n.denominator))
    if root ** n.denominator != a:
        return None
    an = Fr(root) ** n.numerator
    cs = [an * gbin(n, k) * (Fr(b) / a) ** k for k in range(5)]
    base = poly([(a, 0), (b, 1)])
    if n == Fr(1, 2):
        txt = f'√({base})'
    elif n == Fr(-1, 2):
        txt = f'1/√({base})'
    elif n == -1:
        txt = f'1/({base})'
    elif n.denominator == 1:
        txt = f'1/({base}){sup(-n.numerator)}' if r.random() < 0.5 else f'({base}){sup(n.numerator)}'
    else:
        txt = f'({base})^({num(n)})'
    lim = Fr(a) / abs(Fr(b))
    f = lambda x: (a + float(b) * x) ** float(n)
    x = 0.001 * float(lim)
    if not ok(f(x), float(sum(c * Fr(x) ** i for i, c in enumerate(cs))), 'binomial', 1e-9):
        return None
    return dict(n=n, a=a, b=b, an=an, cs=cs, txt=txt, base=base, lim=lim, f=f)


m73 = T('Binomial expansion of (1 + x)ⁿ for any rational n and validity', 'binomial expansion', 'validity', 'rational n')
m73.fixed('C1', (1, 2), [
    ('For which values of x is the expansion of (1 + x)^(1/2) valid?', '|x| < 1', 'For non-integer n the series converges only for |x| < 1.', ['all x', 'x > −1', '|x| ≤ 2']),
    ('What is the coefficient of x² in the expansion of (1 + x)⁻¹?', '1', '(1 + x)⁻¹ = 1 − x + x² − …', ['−1', '2', '1/2']),
    ('How many terms does the expansion of (1 + x)^(1/3) have?', 'infinitely many', 'The binomial coefficients never become zero when n is not a positive integer.', ['4', '3', '1/3']),
])
m73.fixed('C2', (2, 3), [
    ('Explain why (1 + x)⁻¹ = 1 − x + x² − x³ + … cannot be used to find 1/(1 + 2) = 1/3.', 'Putting x = 2 gives 1 − 2 + 4 − 8 + …, which diverges; the expansion is valid only for |x| < 1.', 'B1 terms grow without limit; B1 valid only for |x| < 1 [2]'),
    ('Explain why (4 + x)^(1/2) must be written as 2(1 + x/4)^(1/2) before using the binomial expansion.', 'The standard series is for (1 + y)ⁿ; taking out 4^(1/2) = 2 gives that form with y = x/4, valid for |x| < 4.', 'B1 the series requires the form (1 + y)ⁿ; B1 factor 2 and validity |x| < 4 [2]'),
])


@m73.add('C1', (1, 2, 3))
def m73_c1(r, D):
    d = bin_case(r, D + 1)
    if not d:
        return None
    if r.random() < 0.4:
        return MC(r, f'For which values of x is the expansion of {d["txt"]} in ascending powers of x valid?', f'|x| < {num(d["lim"])}',
                  [f'|x| < {num(1 / d["lim"])}' if d['lim'] != 1 else '|x| < 2', f'|x| < {num(d["lim"] * 2)}', 'all real x', f'x > {num(-d["lim"])}'], f'Need |{term(Fr(d["b"]) / d["a"], 1, first=True)}| < 1.')
    c = d['cs'][1]
    return MC(r, f'Find the coefficient of x in the expansion of {d["txt"]} in ascending powers of x.', num(c),
              [num(-c), num(d['n'] * d['b']) if d['a'] != 1 else num(c * 2), num(c / 2) if c != 0 else '1', num(d['n'])], f'Coefficient = {num(d["an"])} × {num(d["n"])} × ({num(Fr(d["b"]) / d["a"])}).')


@m73.add('C2', (1, 2, 3, 4), 'explain')
def m73_err(r, D):
    nm = person(r)
    d = bin_case(r, max(3, D + 1))
    if not d:
        return None
    f = r.choice(['nofactor', 'valid', 'sign'])
    if f == 'nofactor' and d['a'] != 1:
        w = d['an'] * d['n'] * d['b']
        return Q(f'{nm} writes {d["txt"]} ≈ {num(d["an"])}{term(w, 1)} + … , treating it like (1 + bx)ⁿ with b = {num(d["b"])}. Explain the error and give the correct first two terms.',
                 f'The bracket must first be written as {d["base"] if False else ""}{"(" + num(d["an"]) + ")" if d["an"].denominator != 1 else num(d["an"])}({poly([(1, 0), (Fr(d["b"]) / d["a"], 1)])})^({num(d["n"])}), so the coefficient of x is {num(d["cs"][1])}: {asc(d["cs"][:2])}.',
                 'B1 must take out the factor so the bracket starts with 1; B1 correct first two terms')
    if f == 'valid':
        w = abs(Fr(d['b']))
        if w == d['lim']:
            return None
        return Q(f'{nm} says the expansion of {d["txt"]} is valid for |x| < {num(w)}. Explain why this is wrong and state the correct interval.',
                 f'Validity needs |{term(Fr(d["b"]) / d["a"], 1, first=True)}| < 1, i.e. |x| < {num(d["lim"])}.', 'M1 uses |(b/a)x| < 1; A1 correct interval')
    c2 = d['cs'][2]
    return Q(f'{nm} finds the coefficient of x² in the expansion of {d["txt"]} as {num(-c2) if c2 != 0 else "1"}. Find the correct coefficient and explain the likely error.',
             f'Coefficient = {num(d["an"])} × {pn(d["n"])} × {pn(d["n"] - 1)}/2! × ({num(Fr(d["b"]) / d["a"])})² = {num(c2)}; {nm} probably made a sign error in n − 1 or in the squared term.',
             'M1 correct general term n(n − 1)/2!; A1 correct coefficient')


@m73.add('C3', (1, 2, 3, 4, 5), 'numerical')
def m73_calc(r, D):
    d = bin_case(r, D)
    if not d:
        return None
    if D <= 2:
        return Q(f'Expand {d["txt"]} in ascending powers of x, up to and including the term in x².', asc(d['cs'][:3]), 'M1 correct use of the expansion for rational n; A1 two terms; A1 third term')
    if D == 3:
        return Q(f'Expand {d["txt"]} in ascending powers of x, up to and including the term in x², and state the set of values of x for which the expansion is valid.',
                 f'{asc(d["cs"][:3])}; |x| < {num(d["lim"])}', 'M1 takes out the factor; A1 two terms; A1 third term; B1 validity')
    if D == 4:
        return Q(f'Find the coefficient of x³ in the expansion of {d["txt"]}.', num(d['cs'][3]), 'M1 correct general term; A1 correct value')
    c, e = nz(r, -3, 3), nz(r, -4, 4)
    if Fr(c) * d['b'] == Fr(e) * d['a']:
        return None
    cs = d['cs']
    out = [c * cs[0], c * cs[1] + e * cs[0], c * cs[2] + e * cs[1]]
    txt = f'({poly([(c, 0), (e, 1)])})/{d["txt"][2:]}' if d['txt'].startswith('1/') else f'({poly([(c, 0), (e, 1)])}){d["txt"]}'
    return Q(f'Expand {txt} in ascending powers of x, up to and including the term in x².',
             asc(out), 'M1 expands the bracket; M1 multiplies out; A1 two terms; A1 third term')


def m73_c4(r, D):
    d = bin_case(r, max(3, D))
    if not d:
        return None
    # choose x that gives a recognisable value
    xv = Fr(r.choice([1, 2, 3, 5]), 100) * (1 if d['b'] > 0 else -1)
    if abs(xv) >= d['lim'] / 3:
        return None
    approx = sum(c * xv ** i for i, c in enumerate(d['cs'][:3]))
    true = d['f'](float(xv))
    inner = Fr(d['a']) + Fr(d['b']) * xv
    intro = f'Consider the expansion of {d["txt"]} in ascending powers of x.'
    parts = [
        P('Find the first three terms of the expansion.', asc(d['cs'][:3]), 'M1 correct form for rational n; A1 two terms; A1 third term'),
        P('State the set of values of x for which the expansion is valid.', f'|x| < {num(d["lim"])}', 'B1 correct interval'),
        P(f'Use your expansion with x = {num(xv)} to find an approximation to {d["txt"].replace(d["base"], num(float(inner)))}, giving your answer to 5 decimal places.',
          f'{float(approx):.5f}', f'M1 substitutes x = {num(xv)}; A1 {float(approx):.5f}'),
        P(f'Find the percentage error when the first three terms of the expansion, with x = {num(xv)}, are used to approximate {d["txt"].replace(d["base"], num(float(inner)))}.', f'{n3(abs(float(approx) - true) / abs(true) * 100)}%', 'M1 (|approx − true|/true) × 100; A1 answer'),
    ]
    if abs(float(approx) - true) / abs(true) < 1e-9:
        parts = parts[:3]
    return cmp_(r, intro, parts)


m73.add('C4', (2, 3, 4, 5))(m73_c4)

CHAPTERS[7] = [m71, m72, m73]


# ================================================================ Chapter 8 Further calculus

def sub_family(r, D):
    """Definite integral by substitution with an exact value."""
    kinds = {1: ['poly', 'trig2'], 2: ['poly', 'exp', 'trig2', 'lnpow'], 3: ['root', 'invroot', 'exp', 'trig', 'lnpow'], 4: ['root', 'invroot', 'trig', 'lnln', 'poly2'], 5: ['root', 'invroot', 'lnln', 'poly2', 'trig']}[D]
    kind = r.choice(kinds)
    if kind in ('poly', 'poly2'):
        k = r.randint(1, 5)
        n = r.randint(2, 4) if kind == 'poly' else r.choice([Fr(1, 2), Fr(-1, 2), Fr(3, 2), Fr(-2)])
        c = r.randint(1, 3)
        if kind == 'poly2':
            # x(x² + k)^n with k + c² a perfect square
            opts = [(cc, kk) for cc in (1, 2, 3, 4) for kk in range(1, 10) if math.isqrt(cc * cc + kk) ** 2 == cc * cc + kk and math.isqrt(kk) ** 2 == kk]
            c, k = r.choice(opts) if n.denominator == 2 else (c, k)
        u1, u2 = Fr(k), Fr(c * c + k)
        m = n + 1
        if n.denominator == 2:
            s1, s2 = math.isqrt(k), math.isqrt(c * c + k)
            val = (Fr(s2) ** m.numerator - Fr(s1) ** m.numerator) / (2 * m)
        else:
            val = (u2 ** int(m) - u1 ** int(m)) / (2 * m)
        nt = sup(n) if n.denominator == 1 else f'^({num(n)})'
        it = f'x(x² + {k}){nt}' if n != Fr(1, 2) else f'x√(x² + {k})'
        if n == Fr(-1, 2):
            it = f'x/√(x² + {k})'
        f = lambda x: x * (x * x + k) ** float(n)
        d = dict(it=it, a=0, b=c, at='0', bt=str(c), u=f'u = x² + {k}', du='du = 2x dx', ul=(num(u1), num(u2)), gu=f'(1/2)u{nt}' if n != Fr(1, 2) else '(1/2)√u',
                 ans=num(val), val=val, wrong=None)
    elif kind in ('root', 'invroot'):
        k = r.randint(1, 8)
        s1 = r.choice([s for s in range(1, 4) if s * s - k >= 0] or [0])
        if s1 * s1 - k < 0:
            return None
        s2 = r.randint(s1 + 1, s1 + 2)
        a, b = s1 * s1 - k, s2 * s2 - k
        if kind == 'root':
            val = Fr(2, 5) * (s2 ** 5 - s1 ** 5) - Fr(2 * k, 3) * (s2 ** 3 - s1 ** 3)
            it, f, gu = f'x√(x + {k})', (lambda x: x * math.sqrt(x + k)), f'(u − {k})√u'
        else:
            val = Fr(2, 3) * (s2 ** 3 - s1 ** 3) - 2 * k * (s2 - s1)
            it, f, gu = f'x/√(x + {k})', (lambda x: x / math.sqrt(x + k)), f'(u − {k})/√u'
        d = dict(it=it, a=a, b=b, at=str(a), bt=str(b), u=f'u = x + {k}', du='du = dx', ul=(str(s1 * s1), str(s2 * s2)), gu=gu, ans=num(val), val=val)
    elif kind == 'exp':
        k = r.randint(1, 6)
        m = r.randint(2, 6)
        val = None
        it = f'eˣ/(eˣ + {k})'
        f = lambda x: math.exp(x) / (math.exp(x) + k)
        d = dict(it=it, a=0, b=math.log(m), at='0', bt=f'ln {m}', u=f'u = eˣ + {k}', du='du = eˣ dx', ul=(str(1 + k), str(m + k)), gu='1/u',
                 ans=lnr(Fr(m + k, 1 + k)), val=math.log((m + k) / (1 + k)))
    elif kind in ('trig', 'trig2'):
        n = r.randint(2, 5)
        if kind == 'trig2':
            up = r.choice([(Fr(1, 2), 1), (Fr(1, 6), Fr(1, 2))])
            val = (Fr(up[1]) ** (n + 1)) / (n + 1)
            it, f = f'cos x sin{sup(n)}x', (lambda x: math.cos(x) * math.sin(x) ** n)
            d = dict(it=it, a=0, b=float(up[0]) * math.pi, at='0', bt=pi_frac(up[0]), u='u = sin x', du='du = cos x dx', ul=('0', num(up[1])), gu=f'u{sup(n)}', ans=num(val), val=val)
        else:
            up = r.choice([(Fr(1, 3), Fr(1, 2)), (Fr(1, 2), Fr(0))])
            val = (1 - Fr(up[1]) ** (n + 1)) / (n + 1)
            it, f = f'sin x cos{sup(n)}x', (lambda x: math.sin(x) * math.cos(x) ** n)
            d = dict(it=it, a=0, b=float(up[0]) * math.pi, at='0', bt=pi_frac(up[0]), u='u = cos x', du='du = −sin x dx', ul=('1', num(up[1])), gu=f'−u{sup(n)}', ans=num(val), val=val)
    elif kind == 'lnpow':
        n = r.randint(1, 4)
        val = Fr(1, n + 1)
        it = f'(ln x){sup(n)}/x' if n > 1 else 'ln x/x'
        f = lambda x: math.log(x) ** n / x
        d = dict(it=it, a=1, b=math.e, at='1', bt='e', u='u = ln x', du='du = (1/x) dx', ul=('0', '1'), gu=f'u{sup(n)}' if n > 1 else 'u', ans=num(val), val=val)
    else:
        k = r.randint(2, 5)
        f = lambda x: 1 / (x * math.log(x))
        d = dict(it='1/(x ln x)', a=math.e, b=math.e ** k, at='e', bt=ek(k), u='u = ln x', du='du = (1/x) dx', ul=('1', str(k)), gu='1/u', ans=f'ln {k}', val=math.log(k))
    d['kind'] = kind
    d['f'] = f
    if not ok(simpson(f, float(d['a']), float(d['b'])), float(d['val']), 'sub ' + kind, 1e-6):
        return None
    return d


f81 = T('Integration by substitution', 'integration by substitution', 'substitution')
f81.fixed('C1', (1, 2), [
    ('Using u = x² + 1, what does ∫ 2x(x² + 1)³ dx become?', '∫ u³ du', 'du = 2x dx.', ['∫ 2x u³ du', '∫ u³ dx', '∫ (1/2)u³ du']),
    ('In ∫₀² x√(x² + 5) dx with u = x² + 5, what are the new limits?', '5 and 9', 'x = 0 gives u = 5; x = 2 gives u = 9.', ['0 and 2', '0 and 4', '5 and 7']),
    ('Which substitution is most suitable for ∫ cos x sin⁴x dx?', 'u = sin x', 'du = cos x dx removes the cos x factor.', ['u = cos x', 'u = sin⁴x', 'u = x⁴']),
])
f81.fixed('C2', (2, 3), [
    ('Explain why, after a substitution in a definite integral, the limits must be changed (or the answer converted back to x).', 'The new integral is in terms of u, so the limits must be the corresponding values of u; using the old x-limits in a u-expression gives the wrong value.', 'B1 limits must be values of u; B1 or substitute back before using x-limits [2]'),
])


@f81.add('C1', (1, 2, 3))
def f81_c1(r, D):
    d = sub_family(r, D + 1)
    if not d:
        return None
    if r.random() < 0.5:
        return MC(r, f'Using the substitution {d["u"]}, find the new limits for ∫ from {d["at"]} to {d["bt"]} of {d["it"]} dx.', f'{d["ul"][0]} and {d["ul"][1]}',
                  [f'{d["at"]} and {d["bt"]}', f'{d["ul"][0]} and {d["bt"]}', f'{d["at"]} and {d["ul"][1]}', f'{d["ul"][1]} and {d["ul"][0]}x'], 'Substitute each x-limit into the expression for u.')
    return MC(r, f'Using {d["u"]}, ∫ {d["it"]} dx becomes ∫ g(u) du. What is g(u)?', d['gu'],
              [d['gu'].replace('(1/2)', '2') if '(1/2)' in d['gu'] else d['gu'] + ' × x', d['gu'].replace('−', '') if '−' in d['gu'] else '−' + d['gu'], 'u', f'{d["gu"]}²' if len(d['gu']) < 4 else 'u²'],
              f'{d["du"]}.')


@f81.add('C2', (1, 2, 3, 4), 'explain')
def f81_err(r, D):
    nm = person(r)
    d = sub_family(r, max(2, D + 1))
    if not d:
        return None
    f = r.choice(['limits', 'dx', 'show'])
    if f == 'limits':
        return Q(f'{nm} evaluates ∫ from {d["at"]} to {d["bt"]} of {d["it"]} dx using {d["u"]}, integrates in terms of u, and then substitutes u = {d["at"]} and u = {d["bt"]}. Explain the mistake and state the correct value.',
                 f'The u-integral needs u-limits {d["ul"][0]} and {d["ul"][1]}, not the x-limits. Correct value: {d["ans"]}.', 'B1 limits must be in terms of u; B1 correct value')
    if f == 'dx' and d['kind'] in ('root', 'invroot'):
        k = d['u'].split('+ ')[1]
        return Q(f'{nm} uses {d["u"]} and writes ∫ {d["it"]} dx as ∫ {d["it"].replace("(x + " + k + ")", "u")} du, leaving an x in the integrand. Explain how to complete the substitution.',
                 f'Every x must be written in terms of u: x = u − {k}, and {d["du"]}; the integrand becomes {d["gu"]}.', f'B1 x = u − {k}; B1 correct integrand {d["gu"]}')
    if f == 'dx':
        return Q(f'{nm} uses {d["u"]} to write ∫ {d["it"]} dx as ∫ {d["gu"].replace("(1/2)", "").replace("−", "")} du without changing dx. Explain what is missing.',
                 f'dx must be replaced using {d["du"]}; the correct integrand is {d["gu"]}.', f'B1 must use {d["du"]}; B1 correct integrand {d["gu"]}')
    return Q(f'Show that the substitution {d["u"]} transforms ∫ from {d["at"]} to {d["bt"]} of {d["it"]} dx into ∫ from {d["ul"][0]} to {d["ul"][1]} of {d["gu"]} du.',
             f'{d["du"]}; x-limits {d["at"]}, {d["bt"]} give u = {d["ul"][0]}, {d["ul"][1]}.', 'M1 replaces dx correctly; A1 integrand and limits correct')


@f81.add('C3', (1, 2, 3, 4, 5), 'numerical')
def f81_calc(r, D):
    d = sub_family(r, D)
    if not d:
        return None
    return Q(f'Use the substitution {d["u"]} to find the exact value of ∫ from {d["at"]} to {d["bt"]} of {d["it"]} dx.', d['ans'],
             'M1 substitutes fully including dx; M1 integrates; M1 correct limits; A1 exact answer')


def f81_c4(r, D):
    d = sub_family(r, max(2, D))
    if not d:
        return None
    intro = f'The region R is bounded by the curve y = {d["it"]}, the x-axis and the lines x = {d["at"]} and x = {d["bt"]}.'
    approx = float(d['val'])
    parts = [
        P(f'Use the substitution {d["u"]} to show that the area of R is ∫ from {d["ul"][0]} to {d["ul"][1]} of {d["gu"]} du.', f'{d["du"]}; new limits {d["ul"][0]} and {d["ul"][1]}', 'M1 replaces dx; A1 integrand; B1 limits'),
        P('Hence find the exact area of R.', d['ans'], 'M1 integrates; A1 exact answer'),
        P('Give the area correct to 3 significant figures.', n3(approx), 'B1 value'),
    ]
    if approx <= 0:
        return None
    return cmp_(r, intro, parts)


f81.add('C4', (2, 3, 4, 5))(f81_c4)


# ---------------------------------------------------------------- 8.2 integration by parts

def parts_family(r, D):
    kinds = {1: ['xe', 'xsin'], 2: ['xe', 'xsin', 'xcos', 'lnx'], 3: ['xlne', 'xln2', 'xcos', 'xe'], 4: ['x2e', 'xln2', 'lnx2', 'xe'], 5: ['x2e', 'lnx2', 'xln2', 'x2em']}[D]
    kind = r.choice(kinds)
    if kind == 'xe':
        k = r.choice([1, 2, 3, Fr(1, 2), -1])
        it = f'x{ex(k)}'
        F = f'{ex(k)}({lin(Fr(1) / k, -Fr(1) / k ** 2)})'
        ex_ = [(Fr(1) / k - Fr(1) / k ** 2, 'e', k), (Fr(1) / k ** 2, 'r', None)]
        a, b, at, bt = 0, 1, '0', '1'
        f = lambda x: x * math.exp(float(k) * x)
        uv = ('x', ex(k))
    elif kind in ('xsin', 'xcos'):
        k = r.choice([1, 2, 3])
        kt = '' if k == 1 else str(k)
        fn = 'sin' if kind == 'xsin' else 'cos'
        it = f'x {fn} {kt}x'
        if kind == 'xsin':
            F = tsum([(-Fr(1, k), f'x cos {kt}x'), (Fr(1, k * k), f'sin {kt}x')])
            ex_ = [(Fr(1, k * k), 'r', None)]
            f = lambda x: x * math.sin(k * x)
        else:
            F = tsum([(Fr(1, k), f'x sin {kt}x'), (Fr(1, k * k), f'cos {kt}x')])
            ex_ = [(Fr(1, 2 * k * k), 'pi', None), (-Fr(1, k * k), 'r', None)]
            f = lambda x: x * math.cos(k * x)
        a, b, at, bt = 0, math.pi / (2 * k), '0', pi_frac(Fr(1, 2 * k))
        uv = ('x', f'{fn} {kt}x')
    elif kind == 'lnx':
        m = r.randint(2, 6)
        it, F = 'ln x', 'x ln x − x'
        ex_ = [(m, 'ln', m), (-(m - 1), 'r', None)]
        a, b, at, bt = 1, m, '1', str(m)
        f = math.log
        uv = ('ln x', '1')
    elif kind in ('xlne', 'xln2', 'lnx2'):
        n = r.randint(1, 3) if kind != 'lnx2' else -2
        if kind == 'lnx2':
            it, F = 'ln x/x²', '−(ln x)/x − 1/x'
            m = r.choice([2, 3, 4])
            ex_ = [(-Fr(1, m), 'ln', m), (1 - Fr(1, m), 'r', None)]
            a, b, at, bt = 1, m, '1', str(m)
            f = lambda x: math.log(x) / (x * x)
            uv = ('ln x', '1/x²')
        else:
            it = f'{pw(n)} ln x'
            F = f'{"(" + num(Fr(1, n + 1)) + ")" if n + 1 > 1 else ""}{pw(n + 1)} ln x − {"(" + num(Fr(1, (n + 1) ** 2)) + ")"}{pw(n + 1)}'
            if kind == 'xlne':
                ex_ = [(Fr(n, (n + 1) ** 2), 'e', n + 1), (Fr(1, (n + 1) ** 2), 'r', None)]
                a, b, at, bt = 1, math.e, '1', 'e'
            else:
                ex_ = [(Fr(2 ** (n + 1), n + 1), 'ln', 2), (-Fr(2 ** (n + 1) - 1, (n + 1) ** 2), 'r', None)]
                a, b, at, bt = 1, 2, '1', '2'
            f = lambda x: x ** n * math.log(x)
            uv = ('ln x', pw(n))
    else:
        k = 1 if kind == 'x2e' else -1
        it = f'x²{ex(k)}'
        if k == 1:
            F, ex_ = f'eˣ(x² − 2x + 2)', [(1, 'e', 1), (-2, 'r', None)]
        else:
            F, ex_ = f'−e⁻ˣ(x² + 2x + 2)', [(2, 'r', None), (-5, 'e', -1)]
        a, b, at, bt = 0, 1, '0', '1'
        f = lambda x: x * x * math.exp(k * x)
        uv = ('x²', ex(k))
    ex_.sort(key=lambda t: t[0] < 0)
    val = xval(ex_)
    if not ok(simpson(f, float(a), float(b)), val, 'parts ' + kind, 1e-7):
        return None
    return dict(kind=kind, it=it, F=F, ans=xstr(ex_), val=val, a=a, b=b, at=at, bt=bt, f=f, uv=uv, twice=kind in ('x2e', 'x2em'))


f82 = T('Integration by parts', 'integration by parts', 'by parts')
f82.fixed('C1', (1, 2), [
    ('In ∫ x eˣ dx by parts, which choice is best?', 'u = x, dv/dx = eˣ', 'Differentiating x simplifies it, and eˣ integrates easily.', ['u = eˣ, dv/dx = x', 'u = x eˣ, dv/dx = 1', 'u = 1, dv/dx = x eˣ']),
    ('Which is the integration by parts formula?', '∫ u (dv/dx) dx = uv − ∫ v (du/dx) dx', 'From the product rule.', ['∫ u (dv/dx) dx = uv + ∫ v (du/dx) dx', '∫ uv dx = ∫ u dx × ∫ v dx', '∫ u (dv/dx) dx = (du/dx)v − ∫ uv dx']),
    ('To find ∫ ln x dx by parts, what is taken as dv/dx?', '1', 'Write ln x as 1 × ln x and differentiate ln x.', ['ln x', '1/x', 'x']),
])
f82.fixed('C2', (2, 3), [
    ('Explain why, in ∫ x² ln x dx, it is better to take u = ln x than u = x².', 'ln x is hard to integrate but easy to differentiate (1/x), and x² integrates easily; the new integral ∫ (x³/3)(1/x) dx is simple.', 'B1 ln x differentiates to 1/x; B1 resulting integral is simpler [2]'),
    ('Explain why integration by parts must be applied twice to find ∫ x² eˣ dx.', 'After one application the remaining integral is ∫ 2x eˣ dx, which still contains a power of x and needs parts again.', 'B1 first step leaves ∫ 2x eˣ dx; B1 a second application removes x [2]'),
])


@f82.add('C1', (1, 2, 3))
def f82_c1(r, D):
    d = parts_family(r, D + 1)
    if not d:
        return None
    if r.random() < 0.4:
        u, v = d['uv']
        return MC(r, f'To find ∫ {d["it"]} dx by parts, which choice of u and dv/dx is most appropriate?', f'u = {u}, dv/dx = {v}',
                  [f'u = {v}, dv/dx = {u}', f'u = {d["it"]}, dv/dx = 1', f'u = 1, dv/dx = {d["it"]}'], 'Choose u to become simpler when differentiated.')
    w1 = d['F'].replace(' − ', ' + ', 1) if ' − ' in d['F'] else d['F'] + ' + x'
    return MC(r, f'Find ∫ {d["it"]} dx.', d['F'] + ' + c', [w1 + ' + c', d['F'].replace('ln x', 'x', 1) + ' + c' if 'ln x' in d['F'] else d['F'].replace('x', 'x²', 1) + ' + c',
              f'{d["uv"][0]} × ∫ {d["uv"][1]} dx + c', f'(1/2)x² × {d["uv"][1]} + c' if d['uv'][0] != 'x²' else f'(1/3)x³{d["uv"][1]} + c'], 'Use uv − ∫ v du/dx dx.')


@f82.add('C2', (1, 2, 3, 4), 'explain')
def f82_err(r, D):
    nm = person(r)
    d = parts_family(r, max(2, D + 1))
    if not d:
        return None
    u, v = d['uv']
    f = r.choice(['swap', 'sign', 'diff'])
    if f == 'swap' and v != '1':
        return Q(f'{nm} tries to find ∫ {d["it"]} dx by parts with u = {v} and dv/dx = {u}, and finds that the new integral is harder than the original. Explain why, and state a better choice.',
                 f'Integrating {u} raises its power (or is hard), while differentiating {v} does not simplify it; take u = {u} and dv/dx = {v}, giving {d["F"]} + c.',
                 'B1 explains why the new integral is harder; B1 correct choice of u and dv/dx')
    if f == 'sign':
        return Q(f'{nm} uses the formula ∫ u (dv/dx) dx = uv + ∫ v (du/dx) dx to integrate {d["it"]}. Explain the error and give the correct result.',
                 f'The formula has a minus sign: uv − ∫ v (du/dx) dx, from the product rule. Correct result: {d["F"]} + c.', 'B1 sign in the formula; B1 correct result')
    return Q(f'By differentiating {d["F"]}, show that it is an integral of {d["it"]}.', f'The product rule gives terms that cancel, leaving {d["it"]}.', 'M1 product rule; A1 simplifies to the integrand')


@f82.add('C3', (1, 2, 3, 4, 5), 'numerical')
def f82_calc(r, D):
    d = parts_family(r, D)
    if not d:
        return None
    if D == 1 and r.random() < 0.5:
        return Q(f'Find ∫ {d["it"]} dx.', d['F'] + ' + c', 'M1 parts with a sensible choice; A1 first stage; A1 complete')
    return Q(f'Find the exact value of ∫ from {d["at"]} to {d["bt"]} of {d["it"]} dx.', d['ans'],
             ('M1 parts once; M1 parts again; ' if d['twice'] else 'M1 parts with a sensible choice; A1 correct indefinite integral; ') + 'M1 substitutes limits; A1 exact answer')


def f82_c4(r, D):
    d = parts_family(r, max(2, D))
    if not d or d['val'] <= 0:
        return None
    intro = f'The region R is bounded by the curve y = {d["it"]}, the x-axis and the lines x = {d["at"]} and x = {d["bt"]}; the curve lies on or above the x-axis there.'
    parts = [
        P(f'Find ∫ {d["it"]} dx.', d['F'] + ' + c', ('M1 parts twice; ' if d['twice'] else 'M1 parts; ') + 'A1 correct integral'),
        P('Hence find the exact area of R.', d['ans'], 'M1 uses the limits; A1 exact area'),
        P('Give the area correct to 3 significant figures.', n3(d['val']), 'B1 value'),
        P('Use the trapezium rule with 2 intervals to estimate the area, and state whether it is an over- or under-estimate.',
          (lambda h: f'{n3(h / 2 * (d["f"](float(d["a"]) + 1e-12) + 2 * d["f"]((float(d["a"]) + float(d["b"])) / 2) + d["f"](float(d["b"]))))}; ' +
           ('overestimate' if h / 2 * (d["f"](float(d["a"]) + 1e-12) + 2 * d["f"]((float(d["a"]) + float(d["b"])) / 2) + d["f"](float(d["b"]))) > d['val'] else 'underestimate'))((float(d['b']) - float(d['a'])) / 2),
          'M1 trapezium rule; A1 value; B1 compares with the exact area'),
    ]
    return cmp_(r, intro, parts)


f82.add('C4', (2, 3, 4, 5))(f82_c4)


# ---------------------------------------------------------------- 8.3 integration using partial fractions

def pfint(r, D):
    d = pf_case(r, {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}[D], kind={1: 'two', 2: r.choice(['two', 'xfac']), 3: 'nonunit', 4: 'rep', 5: r.choice(['rep', 'improper', 'reprep'])}[D])
    if not d:
        return None
    poles = [Fr(-v, u) for (u, v, m) in d['facs']]
    cands = [(a, b) for a in range(0, 5) for b in range(a + 1, a + 4) if all(not (a <= p <= b) for p in poles)]
    if not cands:
        return None
    a, b = r.choice(cands)
    exx = []
    if d['c0']:
        exx.append((d['c0'] * (b - a), 'r', None))
    lnc = {}
    for c, u, v, k in d['terms']:
        if k == 1:
            A, B = abs(u * b + v), abs(u * a + v)
            for arg, s in ((A, 1), (B, -1)):
                if arg != 1:
                    lnc[arg] = lnc.get(arg, Fr(0)) + s * Fr(c, u)
        else:
            exx.append((Fr(-c, u) * (Fr(1, u * b + v) - Fr(1, u * a + v)), 'r', None))
    pr = {}
    for arg, c in lnc.items():
        n_, q_ = arg, 2
        while n_ > 1:
            while n_ % q_ == 0:
                pr[q_] = pr.get(q_, Fr(0)) + c
                n_ //= q_
            q_ += 1
    lnc = {q_: c for q_, c in sorted(pr.items()) if c != 0}
    for arg, c in lnc.items():
        exx.append((c, 'ln', arg))
    val = xval(exx)
    if not ok(simpson(d['f'], a, b), val, 'pfint', 1e-7):
        return None
    # single-log form when all log coefficients are integers
    single = None
    if all(c.denominator == 1 for c in lnc.values()) and lnc:
        q = Fr(1)
        for arg, c in lnc.items():
            q *= Fr(arg) ** int(c)
        rat = sum((c for c, kd, _ in exx if kd == 'r'), Fr(0))
        if q != 1 and max(q.numerator, q.denominator) <= 2000:
            single = lnr(q) + (f' + {num(rat)}' if rat > 0 else (f' − {num(-rat)}' if rat < 0 else ''))
    indef = []
    for c, u, v, k in d['terms']:
        lt = lf2(u, v)
        if k == 1:
            lt2 = lt if lt.startswith('(') else lt
            indef.append((Fr(c, u), f'ln|{lt2.strip("()")}|'))
        else:
            indef.append((Fr(-c, u * (k - 1)), f'/{fpow(lt, k - 1)}' if k > 2 else f'/{lt}'))
    it = tsum([(cc, s) for cc, s in indef if not s.startswith('/')])
    for cc, s in indef:
        if s.startswith('/'):
            it += (' − ' if cc < 0 else ' + ') + num(abs(cc)) + s
    if d['c0']:
        it = term(d['c0'], 1, first=True) + (' + ' + it if not it.startswith(MINUS) else ' − ' + it[1:])
    d['pfa'] = d['ans']
    d.update(a=a, b=b, ans=xstr(exx), single=single, val=val, indef=it + ' + c')
    return d


f83 = T('Integrating using partial fractions', 'integrating using partial fractions', 'partial fractions integration')
f83.fixed('C1', (1, 2), [
    ('Find ∫ 3/(x − 2) dx.', '3 ln|x − 2| + c', 'Standard log integral.', ['3/(x − 2)² + c', '−3/(x − 2)² + c', 'ln|3x − 6| + 3 + c']),
    ('Find ∫ 4/(2x + 1) dx.', '2 ln|2x + 1| + c', 'Divide by the coefficient of x.', ['4 ln|2x + 1| + c', '8 ln|2x + 1| + c', 'ln|2x + 1| + c']),
    ('Find ∫ 1/(x + 3)² dx.', '−1/(x + 3) + c', '∫ (x + 3)⁻² dx = −(x + 3)⁻¹ + c.', ['ln (x + 3)² + c', '1/(x + 3) + c', '2 ln|x + 3| + c']),
])
f83.fixed('C2', (2, 3), [
    ('Explain why ∫ 1/(x − 1)² dx is not a logarithm, while ∫ 1/(x − 1) dx is.', '1/(x − 1)² = (x − 1)⁻², which integrates by the power rule to −(x − 1)⁻¹; only the power −1 gives a logarithm.', 'B1 power rule applies for power −2; B1 log only for power −1 [2]'),
])


@f83.add('C1', (1, 2, 3))
def f83_c1(r, D):
    d = pfint(r, D)
    if not d:
        return None
    c, u, v, k = d['terms'][0]
    lt = lf2(u, v)
    if k == 1:
        right = f'{"(" + num(Fr(c, u)) + ") " if Fr(c, u).denominator != 1 else (num(Fr(c, u)) + " " if abs(Fr(c, u)) != 1 else ("−" if c < 0 else ""))}ln|{lt.strip("()")}| + c'
        return MC(r, f'Find ∫ {num(c)}/{lt} dx.', right, [f'{num(c)} ln|{lt.strip("()")}| + c' if u != 1 else f'{num(-c)} ln|{lt.strip("()")}| + c', f'{num(c * u)} ln|{lt.strip("()")}| + c' if u != 1 else f'{num(c)}/{lt}² + c',
                  f'−{num(abs(c))}/{lt}² + c', f'{num(c)} ln|{lt.strip("()")}|² + c'], 'Divide by the coefficient of x inside the logarithm.')
    return None


@f83.add('C2', (1, 2, 3, 4), 'explain')
def f83_err(r, D):
    nm = person(r)
    d = pfint(r, max(2, min(D + 1, 5)))
    if not d:
        return None
    f = r.choice(['coef', 'log', 'show'])
    nu = [t for t in d['terms'] if t[1] != 1 and t[3] == 1]
    rep = [t for t in d['terms'] if t[3] == 2]
    if f == 'coef' and nu:
        c, u, v, k = nu[0]
        return Q(f'{nm} writes ∫ {num(c)}/{lf2(u, v)} dx = {lnco(c, '|' + lin(u, v) + '|')} + c. Explain the error and correct it.',
                 f'By the chain rule d/dx ln|{lin(u, v)}| = {u}/{lf2(u, v)}, so the integral is {lnco(Fr(c, u), '|' + lin(u, v) + '|')} + c.', 'B1 explains the factor 1/' + str(u) + '; B1 correct integral')
    if f == 'log' and rep:
        c, u, v, k = rep[0]
        return Q(f'{nm} integrates {num(c)}/{fpow(lf2(u, v), 2)} to obtain {lnco(c, '|' + lin(u, v) + '|²')} + c. Explain the error and correct it.',
                 f'{num(c)}/{fpow(lf2(u, v), 2)} = {"" if c == 1 else ("−" if c == -1 else num(c))}{lf2(u, v)}⁻², which integrates by the power rule: {num(Fr(-c, u))}/{lf2(u, v)} + c.', 'B1 power rule not logarithm; B1 correct integral')
    return Q(f'Show that ∫ from {d["a"]} to {d["b"]} of {ftext(d)} dx = {d["single"] or d["ans"]}.', f'Partial fractions: {pf_ans(d)}; integral {d["indef"]}; the limits give {d["single"] or d["ans"]}.',
             'M1 partial fractions; M1 integrates to logarithms; A1 uses limits to obtain the given answer')


@f83.add('C3', (1, 2, 3, 4, 5), 'numerical')
def f83_calc(r, D):
    d = pfint(r, D)
    if not d:
        return None
    tail = f' giving your answer in the form ln k' if (d['single'] and d['single'].startswith('ln') and ' ' not in d['single'][3:]) else ', giving your answer in an exact form'
    if D <= 2:
        return Q(f'Given that {ftext(d)} ≡ {d["form"]}, find A and B and hence find ∫ from {d["a"]} to {d["b"]} of {ftext(d)} dx{tail}.',
                 d['single'] or d['ans'], 'M1 finds A and B; A1 both correct; M1 integrates to logarithms; A1 exact answer')
    return Q(f'Find the exact value of ∫ from {d["a"]} to {d["b"]} of {ftext(d)} dx.', d['single'] or d['ans'],
             ('M1 divides first; ' if d['c0'] else '') + 'B1 correct partial fractions; M1 integrates to logarithms; M1 uses limits; A1 exact answer')


def f83_c4(r, D):
    d = pfint(r, max(2, D))
    if not d:
        return None
    intro = f'Let f(x) = {ftext(d)}.'
    parts = [
        P('Express f(x) in partial fractions.', pf_ans(d), 'B1 correct form; M1 method; A1 A1 coefficients'),
        P('Find ∫ f(x) dx.', d['indef'], 'M1 integrates each term; A1 correct'),
        P(f'Show that ∫ from {d["a"]} to {d["b"]} of f(x) dx = {d["single"] or d["ans"]}.', d['single'] or d['ans'], 'M1 uses limits; A1 given answer obtained'),
        P(f'Give the value of ∫ from {d["a"]} to {d["b"]} of f(x) dx correct to 3 significant figures.', n3(d['val']), 'B1 value'),
    ]
    return cmp_(r, intro, parts)


def pf_ans(d):
    return d.get('pfa', d['ans'])


f83.add('C4', (2, 3, 4, 5))(f83_c4)


# ---------------------------------------------------------------- 8.4 inverse tangent

f84 = T('Inverse tangent: derivative and integration of 1/(a² + x²)', 'inverse tangent', 'tan⁻¹', '1/(a² + x²)')
f84.fixed('C1', (1, 2), [
    ('What is d/dx (tan⁻¹ x)?', '1/(1 + x²)', 'If y = tan⁻¹ x, then x = tan y and dx/dy = sec²y = 1 + x².', ['sec²x', '1/(1 − x²)', '−1/(1 + x²)']),
    ('Find ∫ 1/(1 + x²) dx.', 'tan⁻¹ x + c', 'Standard result.', ['ln(1 + x²) + c', '(1/2)ln(1 + x²) + c', 'sec²x + c']),
    ('Find ∫₀¹ 1/(1 + x²) dx.', 'π/4', 'tan⁻¹ 1 − tan⁻¹ 0 = π/4.', ['π/2', 'ln 2', '1/2']),
])
f84.fixed('C2', (2, 3), [
    ('Explain why ∫ x/(4 + x²) dx is a logarithm but ∫ 1/(4 + x²) dx is an inverse tangent.', 'x is (half) the derivative of 4 + x², so the first is (1/2) ln(4 + x²) + c; the second has a constant numerator and is (1/2) tan⁻¹(x/2) + c.', 'B1 numerator is a multiple of the derivative of the denominator; B1 inverse tangent for constant numerator [2]'),
    ('Show that d/dx (tan⁻¹ x) = 1/(1 + x²).', 'Let y = tan⁻¹ x, so tan y = x; then sec²y dy/dx = 1, and sec²y = 1 + tan²y = 1 + x², so dy/dx = 1/(1 + x²).', 'M1 implicit differentiation of tan y = x; A1 uses sec²y = 1 + x² [2]'),
])

ATAN_LIM = [(Fr(1), Fr(1, 4)), (Fr(1, 1), Fr(1, 4))]


def atan_case(r, D):
    a = r.choice([1, 2, 3, 4, 5]) if D <= 2 else r.choice([2, 3, 4, 5, 6])
    b = 1 if D <= 3 else r.choice([1, 2, 3])
    c = r.choice([1, 2, 3, 4, 5, 6])
    # upper limit as a multiple of a/b: 1 (π/4), √3 (π/3), 1/√3 (π/6)
    lim = r.choice(['1', 'r3', 'ir3']) if D >= 3 else '1'
    angle = {'1': Fr(1, 4), 'r3': Fr(1, 3), 'ir3': Fr(1, 6)}[lim]
    upv = a / b * {'1': 1, 'r3': math.sqrt(3), 'ir3': 1 / math.sqrt(3)}[lim]
    if math.gcd(a, b) > 1:
        return None
    ab = Fr(a, b)
    if lim == '1':
        upt = num(ab)
    elif lim == 'r3':
        upt = (num(ab) if ab != 1 else '') + '√3' if ab.denominator == 1 else f'({num(ab)})√3'
    else:
        upt = f'{num(ab)}/√3' if ab.denominator == 1 else f'{a}/({b}√3)'
    den = f'{a * a} + {"" if b == 1 else b * b}x²'
    it = f'{c}/({den})'
    val = Fr(c, a * b) * angle
    f = lambda x: c / (a * a + b * b * x * x)
    if not ok(simpson(f, 0, upv), float(val) * math.pi, 'atan', 1e-8):
        return None
    coef = Fr(c, a * b)
    anti = f'{"(" + num(coef) + ")" if coef.denominator != 1 else (num(coef) if coef != 1 else "")}tan⁻¹({"" if b == 1 else b}x/{a})'
    return dict(a=a, b=b, c=c, it=it, upt=upt, ans=xstr([(val, 'pi', None)]), val=float(val) * math.pi, anti=anti, f=f, upv=upv, den=den)


@f84.add('C1', (1, 2, 3))
def f84_c1(r, D):
    d = atan_case(r, D)
    if not d:
        return None
    if r.random() < 0.5:
        return MC(r, f'Find ∫ {d["it"]} dx.', d['anti'] + ' + c', [d['anti'].replace(f'/{d["a"]})', ')') + ' + c', f'{lnco(d["c"], "(" + d["den"] + ")")} + c', f'{d["c"] if d["c"] != 1 else ""}tan⁻¹({"" if d["b"] == 1 else d["b"]}x/{d["a"]}) + c' if d['c'] != d['a'] * d['b'] else f'{2 * d["c"]}tan⁻¹ x + c',
                  f'({num(Fr(d["c"], d["a"] * d["a"]))})tan⁻¹ x + c'], 'Use ∫ 1/(a² + x²) dx = (1/a) tan⁻¹(x/a) + c.')
    k = r.choice([2, 3, 4, 5])
    return MC(r, f'Find d/dx [tan⁻¹({k}x)].', f'{k}/(1 + {k * k}x²)', [f'1/(1 + {k * k}x²)', f'{k}/(1 + {k}x²)', f'{k}sec²({k}x)', f'1/(1 + {k}x²)'], 'Chain rule: k/(1 + (kx)²).')


@f84.add('C2', (1, 2, 3, 4), 'explain')
def f84_err(r, D):
    nm = person(r)
    d = atan_case(r, max(2, D))
    if not d:
        return None
    f = r.choice(['noa', 'ln', 'deriv'])
    if f == 'noa':
        return Q(f'{nm} writes ∫ 1/({d["a"] * d["a"]} + x²) dx = tan⁻¹(x/{d["a"]}) + c. By differentiating, show that this is wrong and correct it.',
                 f'd/dx tan⁻¹(x/{d["a"]}) = (1/{d["a"]})/(1 + x²/{d["a"] * d["a"]}) = {d["a"]}/({d["a"] * d["a"]} + x²), so the answer needs a factor 1/{d["a"]}: (1/{d["a"]})tan⁻¹(x/{d["a"]}) + c.',
                 'M1 differentiates using the chain rule; A1 correct integral')
    if f == 'ln':
        return Q(f'{nm} writes ∫ {d["it"]} dx = {lnco(d["c"], "(" + d["den"] + ")")} + c. Explain why this is wrong and find the correct integral.',
                 f'The numerator is not a multiple of the derivative of {d["den"]}; the correct integral is {d["anti"]} + c.', 'B1 numerator is not a multiple of the derivative; B1 correct inverse tangent')
    k = r.choice([2, 3, 4])
    return Q(f'Show that the gradient of y = tan⁻¹({k}x) at x = {num(Fr(1, k))} is {num(Fr(k, 2))}.', f'dy/dx = {k}/(1 + {k * k}x²) = {k}/2 at x = {num(Fr(1, k))}.', 'M1 chain rule; A1 substitutes to obtain the value')


@f84.add('C3', (1, 2, 3, 4, 5), 'numerical')
def f84_calc(r, D):
    d = atan_case(r, D)
    if not d:
        return None
    if D == 5 and r.random() < 0.5:
        p = nz(r, 1, 4)
        exx = [(Fr(p, 2 * d['b'] * d['b']), 'ln', 2), (Fr(d['c'], d['a'] * d['b']) * Fr(1, 4), 'pi', None)]
        up = Fr(d['a'], d['b'])
        f = lambda x: (p * x + d['c']) / (d['a'] ** 2 + d['b'] ** 2 * x * x)
        if not ok(simpson(f, 0, float(up)), xval(exx), 'atan mix', 1e-8):
            return None
        return Q(f'Find the exact value of ∫ from 0 to {num(up)} of ({lin(p, d["c"])})/({d["den"]}) dx.', xstr(exx), 'M1 splits the fraction; A1 log term; A1 inverse tangent term; A1 exact answer')
    return Q(f'Find the exact value of ∫ from 0 to {d["upt"]} of {d["it"]} dx.', d['ans'], 'M1 (1/a)tan⁻¹ form; A1 correct integral; M1 limits; A1 exact answer')


def f84_c4(r, D):
    d = atan_case(r, max(3, D))
    if not d:
        return None
    a, b, c = d['a'], d['b'], d['c']
    k = r.choice([2, 3])
    intro = f'Let y = tan⁻¹({"" if b == 1 else b}x/{a}).'
    parts = [
        P('Find dy/dx.', f'{a * b}/({d["den"]})', 'M1 chain rule; A1 simplified'),
        P(f'Find ∫ {d["it"]} dx.', d['anti'] + ' + c', 'M1 uses the derivative of y; A1 correct constant factor'),
        P(f'Find the exact value of ∫ from 0 to {d["upt"]} of {d["it"]} dx.', d['ans'], 'M1 limits; A1 exact answer'),
        P(f'Find the gradient of the curve y = tan⁻¹({"" if b == 1 else b}x/{a}) at x = {a * k}{"" if b == 1 else "/" + str(b)}.', num(Fr(a * b, a * a + a * a * k * k)), 'B1 value'),
    ]
    return cmp_(r, intro, parts)


f84.add('C4', (3, 4, 5))(f84_c4)

CHAPTERS[8] = [f81, f82, f83, f84]


# ================================================================ Chapter 9 Vectors

NICE3 = [(1, 2, 2), (2, 3, 6), (2, 6, 9), (1, 4, 8), (4, 4, 7), (2, 10, 11), (6, 6, 7), (3, 4, 12), (2, 2, 1), (4, 8, 1), (6, 2, 3), (9, 6, 2), (8, 4, 1), (12, 4, 3)]


def rvec(r, lo=-6, hi=6, dim=3, nonzero=True):
    while True:
        v = [r.randint(lo, hi) for _ in range(dim)]
        if not nonzero or any(v):
            return v


def nice_vec(r):
    v = list(r.choice(NICE3))
    r.shuffle(v)
    return [x * r.choice([1, -1]) for x in v]


def vt(v, r=None, style=None):
    """Vector text: ijk or column form."""
    style = style or ('ijk' if (r is None or r.random() < 0.5) else 'col')
    return vstr(v) if style == 'ijk' else vcol(v)


def pvec(v, i, s='p'):
    """Vector text with component i replaced by a symbol: pi − 2j + 3k."""
    out = ''
    for j, (x, u) in enumerate(zip(v, 'ijk')):
        if j == i:
            body, neg = f'{s}{u}', False
        elif x == 0:
            continue
        else:
            body, neg = ('' if abs(x) == 1 else num(abs(x))) + u, x < 0
        out += ((MINUS if neg else '') + body) if not out else ((' − ' if neg else ' + ') + body)
    return out


def mag_str(v):
    return sqrt_str(mag2(v))


def unit_str(v):
    m2 = mag2(v)
    o, i = surd(m2)
    if i == 1:
        return f'(1/{o})({vstr(v)})' if o != 1 else vstr(v)
    return f'(1/{sqrt_str(m2)})({vstr(v)})'


def ang(a, b):
    c = dot(a, b) / math.sqrt(mag2(a) * mag2(b))
    return math.degrees(math.acos(max(-1, min(1, c))))


def pts(r, n=3):
    return [rvec(r, -5, 6, nonzero=False) for _ in range(n)]


v91 = T('Vectors in two and three dimensions: magnitude and unit vectors', 'magnitude', 'unit vectors', 'vectors in three dimensions')
v91.fixed('C1', (1, 2), [
    ('What is the magnitude of 2i − j + 2k?', '3', '√(4 + 1 + 4) = 3.', ['5', '√5', '9']),
    ('Points A and B have position vectors a and b. Which vector is AB?', 'b − a', 'AB = OB − OA.', ['a − b', 'a + b', '(a + b)/2']),
    ('Which vector is parallel to 2i − 4j + 6k?', '−i + 2j − 3k', 'It is −1/2 times the vector.', ['i − 2j − 3k', '2i + 4j + 6k', 'i + 2j + 3k']),
])
v91.fixed('C2', (2, 3), [
    ('Explain why a vector divided by its own magnitude is a unit vector in the same direction.', 'Dividing by the positive scalar |v| keeps the direction and gives magnitude |v|/|v| = 1.', 'B1 positive scalar multiple keeps direction; B1 magnitude 1 [2]'),
    ('Explain how to show that points A, B and C are collinear using vectors.', 'Show that AB is a scalar multiple of AC (or BC); since they share point A, the points lie on one straight line.', 'B1 AB = k AC; B1 common point so collinear [2]'),
])


@v91.add('C1', (1, 2, 3))
def v91_c1(r, D):
    if D == 1:
        v = nice_vec(r) if r.random() < 0.7 else rvec(r)
        m = mag_str(v)
        return MC(r, f'Find the magnitude of the vector {vt(v, r)}.', m, [num(sum(abs(x) for x in v)), sqrt_str(abs(sum(v))) if sum(v) else '0', num(mag2(v)), sqrt_str(mag2(v) + 2)],
                  f'√({" + ".join(str(x * x) for x in v if x)}).')
    a, b = pts(r, 2)
    ab = vsub(b, a)
    if not any(ab):
        return None
    if D == 2:
        return MC(r, f'The points A and B have position vectors {vt(a, r)} and {vt(b, r)}. Find the vector AB.', vstr(ab), [vstr(vsub(a, b)), vstr(vadd(a, b)), vstr([x if i else -x for i, x in enumerate(ab)])], 'AB = b − a.')
    v = nice_vec(r)
    k = r.choice([2, 3, 5, 10, 14])
    m = math.isqrt(mag2(v))
    tgt = [Fr(k * x, m) for x in v]
    if any(x.denominator != 1 for x in tgt):
        k = m * r.choice([1, 2, 3])
        tgt = [Fr(k * x, m) for x in v]
    return MC(r, f'Find the vector of magnitude {k} in the direction of {vstr(v)}.', vstr(tgt), [vstr(vmul(k, v)), vstr([-x for x in tgt]), vstr([x + (1 if i == 0 else 0) for i, x in enumerate(tgt)])],
              f'|v| = {m}, so multiply the unit vector by {k}.')


@v91.add('C2', (1, 2, 3, 4), 'explain')
def v91_err(r, D):
    nm = person(r)
    v = nice_vec(r)
    f = r.choice(['sum', 'ab', 'unit', 'coll'])
    if f == 'sum':
        w = sum(v)
        return Q(f'{nm} says the magnitude of {vstr(v)} is {num(w)}, by adding the components. Explain the error and find the correct magnitude.',
                 f'Magnitude is √(sum of squares of the components) = √{mag2(v)} = {mag_str(v)}, not the sum of the components.', 'B1 uses Pythagoras in 3D; B1 correct magnitude')
    if f == 'ab':
        a, b = pts(r, 2)
        if a == b:
            return None
        return Q(f'{nm} finds AB for A{pt(*a[:2])[:-1]}, {num(a[2])}) and B{pt(*b[:2])[:-1]}, {num(b[2])}) as {vstr(vsub(a, b))}. Explain the error and give the correct vector.',
                 f'AB = OB − OA = {vstr(vsub(b, a))}; {nm} has found BA.', 'B1 AB = b − a; B1 correct vector')
    if f == 'unit':
        return Q(f'{nm} says that the unit vector in the direction of {vstr(v)} is {vstr([x // abs(x) if x else 0 for x in v])}. Explain why this is wrong and find the correct unit vector.',
                 f'Its magnitude is not 1 and its direction differs; the unit vector is {unit_str(v)}.', 'B1 explains magnitude/direction; B1 correct unit vector')
    a = rvec(r)
    k = r.choice([2, 3, -2])
    b = vadd(a, vmul(k, v))
    c = vadd(a, vmul(k + r.choice([1, 2]), v))
    return Q(f'Points A, B and C have position vectors {vstr(a)}, {vstr(b)} and {vstr(c)}. Show that A, B and C are collinear.',
             f'AB = {vstr(vsub(b, a))} and AC = {vstr(vsub(c, a))} are both multiples of {vstr(v)}, so they are parallel with A common.', 'M1 finds AB and AC; A1 shows one is a multiple of the other with a common point')


@v91.add('C3', (1, 2, 3, 4, 5), 'numerical')
def v91_calc(r, D):
    a = rvec(r, -5, 6, nonzero=False)
    if D <= 2:
        v = nice_vec(r) if D == 1 else rvec(r)
        b = vadd(a, v)
        return Q(f'The points A and B have position vectors {vt(a, r)} and {vt(b, r)}. Find the distance AB, giving your answer exactly.', mag_str(v), 'M1 AB = b − a; A1 exact length')
    if D == 3:
        v = rvec(r)
        b = vadd(a, v)
        return Q(f'The points A and B have position vectors {vt(a, r)} and {vt(b, r)}. Find the unit vector in the direction of AB.', unit_str(v), 'M1 AB; M1 divides by |AB|; A1 correct unit vector')
    if D == 4:
        v = nice_vec(r)
        p = r.randint(1, 4)
        q = r.randint(1, 4)
        if math.gcd(p, q) > 1:
            return None
        b = vadd(a, vmul(p + q, v))
        pnt = vadd(a, vmul(p, v))
        return Q(f'A and B have position vectors {vstr(a)} and {vstr(b)}. The point P lies on AB with AP : PB = {p} : {q}. Find the position vector of P.', vstr(pnt), 'M1 OP = OA + (p/(p + q))AB; A1 correct vector')
    v = rvec(r, -4, 4)
    i = r.randrange(3)
    tgt = mag2(v)
    c = v[i]
    # find the values of t so that |v with component i replaced by t| = √(tgt + extra)
    extra = r.choice([0, 5, 12, 16, 21])
    t2 = c * c + extra
    t = math.isqrt(t2)
    if t * t != t2 or t == 0:
        return None
    w = list(v)
    comp = ['i', 'j', 'k'][i]
    txt = pvec(v, i, 't')
    return Q(f'The vector {txt} has magnitude {sqrt_str(tgt + extra)}. Find the possible values of t.', f't = ±{t}', 'M1 forms an equation using the magnitude; A1 both values')


def v91_c4(r, D):
    a = rvec(r, -4, 5, nonzero=False)
    u = nice_vec(r)
    w = nice_vec(r)
    if math.isqrt(mag2(u)) != math.isqrt(mag2(w)) and r.random() < 0.5:
        w = list(u)
        r.shuffle(w)
        w = [x * r.choice([1, -1]) for x in w]
    b, c = vadd(a, u), vadd(a, w)
    if b == c or not any(cross(u, w)):
        return None
    dvec = vadd(a, vsub(c, b)) if False else vsub(vadd(b, c), a)
    intro = f'The points A, B and C have position vectors {vstr(a)}, {vstr(b)} and {vstr(c)} respectively.'
    iso = mag2(u) == mag2(w)
    parts = [
        P('Find the vectors AB and AC.', f'AB = {vstr(u)}, AC = {vstr(w)}', 'B1 AB; B1 AC'),
        P('Find the lengths AB and AC.', f'AB = {mag_str(u)}, AC = {mag_str(w)}', 'M1 magnitude; A1 both'),
        P('Find the position vector of the point D such that ABDC is a parallelogram.', vstr(dvec), 'M1 OD = OB + AC; A1 correct'),
        P('Find the unit vector in the direction of BC.', unit_str(vsub(c, b)), 'M1 BC; A1 unit vector'),
    ]
    if iso:
        parts.insert(2, P('Show that triangle ABC is isosceles.', f'|AB| = |AC| = {mag_str(u)}', 'B1 equal lengths shown'))
    return cmp_(r, intro, parts)


v91.add('C4', (2, 3, 4, 5))(v91_c4)


# ---------------------------------------------------------------- 9.2 scalar product

v92 = T('Scalar product and the angle between two vectors', 'scalar product', 'angle between two vectors')
v92.fixed('C1', (1, 2), [
    ('If a · b = 0 for non-zero vectors a and b, what can be concluded?', 'a and b are perpendicular', 'cos θ = 0 gives θ = 90°.', ['a and b are parallel', 'a = b', 'a or b is a unit vector']),
    ('Find (2i + 3j − k) · (i − j + 4k).', '−5', '2 − 3 − 4 = −5.', ['5', '−1', '3']),
    ('Which formula gives the angle θ between vectors a and b?', 'cos θ = a·b/(|a||b|)', 'From a·b = |a||b| cos θ.', ['sin θ = a·b/(|a||b|)', 'cos θ = |a||b|/a·b', 'tan θ = a·b']),
])
v92.fixed('C2', (2, 3), [
    ('Explain why a negative scalar product means the angle between the vectors is obtuse.', 'a·b = |a||b| cos θ with |a|, |b| > 0, so a·b < 0 exactly when cos θ < 0, i.e. 90° < θ ≤ 180°.', 'B1 magnitudes positive; B1 cos θ < 0 means obtuse [2]'),
    ('Explain why, to find angle BAC, the vectors AB and AC must be used rather than BA and AC.', 'The angle at A is between the two vectors pointing away from A; using BA reverses one direction and gives 180° minus the required angle.', 'B1 both vectors from A; B1 BA gives the supplement [2]'),
])


@v92.add('C1', (1, 2, 3))
def v92_c1(r, D):
    a, b = rvec(r), rvec(r)
    if D == 1:
        d = dot(a, b)
        return MC(r, f'Find the scalar product of {vt(a, r)} and {vt(b, r)}.', num(d), [num(-d) if d else '1', num(sum(abs(x * y) for x, y in zip(a, b))), num(d + 2), vstr([x * y for x, y in zip(a, b)])], 'Sum of the products of corresponding components.')
    if D == 2:
        i = r.randrange(3)
        others = sum(a[j] * b[j] for j in range(3) if j != i)
        if b[i] == 0 or others % b[i]:
            return None
        p = -others // b[i]
        txt = vstr([x if j != i else 0 for j, x in enumerate(a)])
        aa = pvec(a, i)
        return MC(r, f'The vectors {aa} and {vstr(b)} are perpendicular. Find p.', num(p), [num(-p) if p else '1', num(p + 1), num(others), num(p - 2)], 'Set the scalar product equal to 0.')
    if not dot(a, b):
        return None
    th = ang(a, b)
    return MC(r, f'The angle between {vstr(a)} and {vstr(b)} is θ. Which statement is true?', 'θ is obtuse' if dot(a, b) < 0 else 'θ is acute',
              ['θ is acute' if dot(a, b) < 0 else 'θ is obtuse', 'θ = 90°', 'θ = 0°', 'the vectors are parallel'], f'a·b = {num(dot(a, b))}; θ ≈ {d1(th)}.')


@v92.add('C2', (1, 2, 3, 4), 'explain')
def v92_err(r, D):
    nm = person(r)
    a, b, c = pts(r, 3)
    ab, ac = vsub(b, a), vsub(c, a)
    if not any(ab) or not any(ac) or not any(cross(ab, ac)):
        return None
    f = r.choice(['ba', 'parallel', 'acute'])
    th = ang(ab, ac)
    if f == 'ba':
        return Q(f'For A{tuple(a)}, B{tuple(b)} and C{tuple(c)}, {nm} finds angle BAC using the vectors BA and AC and obtains {d1(180 - th)}. Explain the error and find the correct angle.'.replace(', ', ', ').replace('(-', '(−').replace(' -', ' −'),
                 f'Both vectors must point away from A: AB = {vstr(ab)}, AC = {vstr(ac)}; angle BAC = {d1(th)}.', 'B1 uses AB and AC; B1 correct angle')
    if f == 'parallel':
        p = rvec(r)
        q = [p[1], -p[0], 0] if p[0] or p[1] else [1, 0, 0]
        if not any(q):
            return None
        return Q(f'{nm} finds that the scalar product of {vstr(p)} and {vstr(q)} is 0 and concludes that the vectors are parallel. Explain the error.',
                 'A zero scalar product means cos θ = 0, so the vectors are perpendicular, not parallel.', 'B1 cos θ = 0; B1 perpendicular')
    u, v = rvec(r), rvec(r)
    if dot(u, v) >= 0:
        return None
    t = ang(u, v)
    return Q(f'{nm} is asked for the acute angle between the lines with directions {vstr(u)} and {vstr(v)}, and gives {d1(t)}. Explain why this is not the required answer and find it.',
             f'{d1(t)} is obtuse because the scalar product is negative; the acute angle between the lines is 180° − {d1(t)} = {d1(180 - t)}.', 'B1 recognises the obtuse angle; B1 acute angle')


@v92.add('C3', (1, 2, 3, 4, 5), 'numerical')
def v92_calc(r, D):
    if D <= 2:
        a, b = rvec(r), rvec(r)
        if not dot(a, b) or not any(cross(a, b)):
            return None
        return Q(f'Find the angle between the vectors {vt(a, r)} and {vt(b, r)}.', d1(ang(a, b)), 'M1 scalar product; M1 magnitudes; A1 angle')
    if D == 3:
        a = rvec(r)
        b = rvec(r)
        i = r.randrange(3)
        if b[i] == 0:
            return None
        others = sum(a[j] * b[j] for j in range(3) if j != i)
        p = Fr(-others, b[i])
        aa = pvec(a, i)
        return Q(f'Find the value of p for which the vectors {aa} and {vstr(b)} are perpendicular.', f'p = {num(p)}', 'M1 scalar product = 0; A1 value')
    a, b, c = pts(r, 3)
    ab, ac = vsub(b, a), vsub(c, a)
    if not any(ab) or not any(ac) or not any(cross(ab, ac)):
        return None
    th = ang(ab, ac)
    if D == 4:
        return Q(f'The points A, B and C have position vectors {vstr(a) if any(a) else "0"}, {vstr(b) if any(b) else "0"} and {vstr(c) if any(c) else "0"}. Find angle BAC.', d1(th), 'M1 AB and AC; M1 scalar product; A1 angle')
    area = 0.5 * math.sqrt(mag2(ab) * mag2(ac)) * math.sin(math.radians(th))
    if not ok(area, 0.5 * math.sqrt(mag2(cross(ab, ac))), 'area', 1e-7):
        return None
    return Q(f'The points A, B and C have position vectors {vstr(a) if any(a) else "0"}, {vstr(b) if any(b) else "0"} and {vstr(c) if any(c) else "0"}. Find angle BAC and hence the area of triangle ABC.',
             f'{d1(th)}; area = {n3(area)}', 'M1 scalar product; A1 angle; M1 (1/2)|AB||AC| sin A; A1 area')


def v92_c4(r, D):
    a = rvec(r, -3, 4, nonzero=False)
    u = rvec(r, -4, 4)
    # build w perpendicular to u sometimes
    if r.random() < 0.4:
        w = cross(u, rvec(r, -2, 2))
        if not any(w) or max(abs(x) for x in w) > 12:
            return None
    else:
        w = rvec(r, -4, 4)
    if not any(cross(u, w)):
        return None
    b, c = vadd(a, u), vadd(a, w)
    th = ang(u, w)
    area = 0.5 * math.sqrt(mag2(cross(u, w)))
    intro = f'Relative to the origin O, the points A, B and C have position vectors {vstr(a) if any(a) else "0"}, {vstr(b)} and {vstr(c)}.'
    parts = [
        P('Find AB · AC.', num(dot(u, w)), 'M1 AB and AC; A1 scalar product'),
        P('Find angle BAC.', d1(th), 'M1 uses cos θ = a·b/(|a||b|); A1 angle'),
        P('Find the area of triangle ABC.', n3(area), 'M1 (1/2)|AB||AC| sin A; A1 area'),
    ]
    if dot(u, w) == 0:
        parts[1] = P('Show that angle BAC is a right angle.', 'AB · AC = 0', 'B1 scalar product zero shown')
        parts[2] = P('Find the exact area of triangle ABC.', f'(1/2) × {mag_str(u)} × {mag_str(w)} = {sqrt_str(Fr(mag2(u) * mag2(w), 4))}', 'M1 (1/2)|AB||AC|; A1 exact area')
    return cmp_(r, intro, parts)


v92.add('C4', (2, 3, 4, 5))(v92_c4)


# ---------------------------------------------------------------- 9.3 vector equation of a line

def lstr(a, d, p='λ'):
    return f'r = {vstr(a) if any(a) else "0"} + {p}({vstr(d)})'


def meet_case(r):
    P0 = rvec(r, -5, 6, nonzero=False)
    d1_, d2_ = rvec(r, -3, 3), rvec(r, -3, 3)
    if not any(cross(d1_, d2_)):
        return None
    l0, m0 = nz(r, -3, 3), nz(r, -3, 3)
    a1 = vsub(P0, vmul(l0, d1_))
    a2 = vsub(P0, vmul(m0, d2_))
    if a1 == a2:
        return None
    return dict(P=P0, a1=a1, d1=d1_, a2=a2, d2=d2_, l=l0, m=m0)


v93 = T('Vector equation of a line and intersection of lines', 'vector equation of a line', 'intersection of lines')
v93.fixed('C1', (1, 2), [
    ('In r = a + λd, what does d represent?', 'a direction vector of the line', 'λ varies along the line in the direction d.', ['the position vector of a point on the line', 'the distance from the origin', 'a normal to the line']),
    ('Two lines in three dimensions are neither parallel nor intersecting. What are they called?', 'skew', 'Skew lines exist only in three dimensions.', ['perpendicular', 'coincident', 'collinear']),
])
v93.fixed('C2', (2, 3), [
    ('Explain why, when testing whether two lines in three dimensions intersect, values of λ and μ found from two of the component equations must be checked in the third.', 'Two equations can always be solved for λ and μ; the lines meet only if these values also satisfy the third equation.', 'B1 two equations always solvable; B1 third must be consistent [2]'),
    ('Explain why different parameters (λ and μ) must be used for two different lines when finding their intersection.', 'The point of intersection generally corresponds to different parameter values on the two lines; using the same letter forces them equal and may wrongly suggest no intersection.', 'B1 parameters independent; B1 same letter gives wrong conclusion [2]'),
])


@v93.add('C1', (1, 2, 3))
def v93_c1(r, D):
    m = meet_case(r)
    if not m:
        return None
    a, d = m['a1'], m['d1']
    if D == 1:
        lam = nz(r, -3, 3)
        p = vadd(a, vmul(lam, d))
        return MC(r, f'The line l has equation {lstr(a, d)}. Find the position vector of the point on l where λ = {lam}.', vstr(p) if any(p) else '0',
                  [vstr(vadd(d, vmul(lam, a))) if any(vadd(d, vmul(lam, a))) else 'i', vstr(vsub(a, vmul(lam, d))) if any(vsub(a, vmul(lam, d))) else 'j', vstr(vmul(lam, d))], 'Substitute λ into r = a + λd.')
    if D == 2:
        k = r.choice([2, -1, 3, -2])
        return MC(r, f'Which line is parallel to {lstr(a, d)}?', lstr(m['a2'], vmul(k, d), 'μ'),
                  [lstr(m['a2'], m['d2'], 'μ'), lstr(m['a2'], [d[1], d[0], d[2]] if [d[1], d[0], d[2]] != d else [d[0], d[2], d[1]], 'μ'), lstr(d, a, 'μ') if any(a) else lstr(m['a2'], vadd(d, [1, 0, 0]), 'μ')],
                  'Parallel lines have direction vectors that are scalar multiples.')
    b = vadd(a, vmul(r.choice([2, 3, -1]), d))
    return MC(r, f'Find a vector equation of the line through A({", ".join(num(x) for x in a)}) and B({", ".join(num(x) for x in b)}).', lstr(a, vsub(b, a)),
              [lstr(a, b), lstr(b, a) if any(a) else lstr(b, vadd(b, [1, 1, 0])), lstr(vsub(b, a), a) if any(a) else lstr(a, vadd(b, a))], 'r = OA + λAB.')


@v93.add('C2', (1, 2, 3, 4), 'explain')
def v93_err(r, D):
    nm = person(r)
    m = meet_case(r)
    if not m:
        return None
    f = r.choice(['same', 'onl', 'third'])
    if f == 'same':
        return Q(f'{nm} tries to find where the lines {lstr(m["a1"], m["d1"])} and {lstr(m["a2"], m["d2"], "λ")} meet by equating components, and finds no single value of λ. {nm} concludes that the lines do not intersect. Explain the error.',
                 f'The two lines need different parameters; with μ for the second line, λ = {m["l"]} and μ = {m["m"]} satisfy all three equations, so the lines meet at {vstr(m["P"]) if any(m["P"]) else "the origin"}.',
                 'B1 different parameters needed; B1 correct conclusion with point')
    if f == 'onl':
        lam = nz(r, -3, 3)
        p = vadd(m['a1'], vmul(lam, m['d1']))
        q = list(p)
        q[2] += r.choice([1, -1, 2])
        return Q(f'Determine whether the points P({", ".join(num(x) for x in p)}) and Q({", ".join(num(x) for x in q)}) lie on the line {lstr(m["a1"], m["d1"])}, explaining your reasoning.',
                 f'P: λ = {lam} satisfies all three components, so P is on the line. Q: no single λ satisfies all three components, so Q is not on the line.', 'M1 finds λ from one component and checks the others; A1 P on the line; A1 Q not on the line')
    return Q(f'Show that the lines {lstr(m["a1"], m["d1"])} and {lstr(m["a2"], m["d2"], "μ")} intersect.',
             f'Solving two component equations gives λ = {m["l"]}, μ = {m["m"]}, and these satisfy the third, so the lines meet.', 'M1 equates components; A1 λ and μ; A1 checks the third equation')


@v93.add('C3', (1, 2, 3, 4, 5), 'numerical')
def v93_calc(r, D):
    m = meet_case(r)
    if not m:
        return None
    if D == 1:
        b = vadd(m['a1'], vmul(r.choice([1, 2, -1]), m['d1']))
        return Q(f'Find a vector equation of the line through the points with position vectors {vstr(m["a1"]) if any(m["a1"]) else "0"} and {vstr(b)}.', lstr(m['a1'], vsub(b, m['a1'])), 'M1 direction vector b − a; A1 equation')
    if D == 2:
        lam = nz(r, -3, 3)
        p = vadd(m['a1'], vmul(lam, m['d1']))
        i = r.randrange(3)
        q = ['', '', '']
        txt = ', '.join(num(x) if j != i else 'k' for j, x in enumerate(p))
        if m['d1'][i] == 0:
            return None
        return Q(f'The point ({txt}) lies on the line {lstr(m["a1"], m["d1"])}. Find k.', f'k = {num(p[i])}', 'M1 finds λ from a known component; A1 k')
    return Q(f'Find the position vector of the point of intersection of the lines {lstr(m["a1"], m["d1"])} and {lstr(m["a2"], m["d2"], "μ")}.', vstr(m['P']) if any(m['P']) else '0',
             'M1 equates two components; A1 λ and μ; B1 checks the third; A1 point')


def v93_c4(r, D):
    m = meet_case(r)
    if not m:
        return None
    b = vadd(m['a1'], vmul(r.choice([1, 2]), m['d1']))
    th = ang(m['d1'], m['d2'])
    acute = th if th <= 90 else 180 - th
    intro = f'The line l passes through A({", ".join(num(x) for x in m["a1"])}) and B({", ".join(num(x) for x in b)}). The line m has equation {lstr(m["a2"], m["d2"], "μ")}.'
    parts = [
        P('Find a vector equation for l.', lstr(m['a1'], vsub(b, m['a1'])), 'M1 direction AB; A1 equation'),
        P('Show that l and m intersect and find the position vector of the point of intersection.', vstr(m['P']) if any(m['P']) else '0', 'M1 equates components; A1 parameters; B1 third equation checked; A1 point'),
        P('Find the acute angle between l and m.', d1(acute), 'M1 scalar product of the direction vectors; A1 angle'),
    ]
    return cmp_(r, intro, parts)


v93.add('C4', (2, 3, 4, 5))(v93_c4)


# ---------------------------------------------------------------- 9.4 perpendicular distance and skew lines

def perp_case(r):
    a = rvec(r, -4, 5, nonzero=False)
    d = rvec(r, -3, 3)
    w = cross(d, rvec(r, -2, 2))
    if not any(w):
        return None
    g = math.gcd(math.gcd(abs(w[0]), abs(w[1])), abs(w[2]))
    w = [x // g for x in w]
    w = vmul(r.choice([1, 2, -1]), w)
    l0 = nz(r, -3, 3)
    F = vadd(a, vmul(l0, d))
    P_ = vadd(F, w)
    if not ok(dot(vsub(P_, F), d), 0, 'perp'):
        return None
    return dict(a=a, d=d, F=F, P=P_, w=w, l=l0)


def skew_case(r):
    d1_, d2_ = rvec(r, -3, 3), rvec(r, -3, 3)
    n = cross(d1_, d2_)
    if not any(n):
        return None
    a1 = rvec(r, -4, 4, nonzero=False)
    a2 = vadd(a1, vadd(vmul(nz(r, -2, 2), d1_), vmul(nz(r, -2, 2), d2_)))
    a2 = vadd(a2, [x // max(1, math.gcd(math.gcd(abs(n[0]), abs(n[1])), abs(n[2]))) for x in n])
    if dot(vsub(a2, a1), n) == 0:
        return None
    return dict(a1=a1, d1=d1_, a2=a2, d2=d2_)


v94 = T('Perpendicular distance from a point to a line and skew lines', 'perpendicular distance', 'skew lines', 'foot of the perpendicular')
v94.fixed('C1', (1, 2), [
    ('F is the foot of the perpendicular from P to the line r = a + λd. Which condition fixes λ?', 'PF · d = 0', 'PF is perpendicular to the line direction.', ['PF · a = 0', '|PF| = |d|', 'PF = d']),
    ('Two lines are skew. Which statement is true?', 'They are not parallel and do not intersect', 'Skew lines lie in different planes.', ['They are parallel', 'They intersect at right angles', 'They lie in the same plane']),
])
v94.fixed('C2', (2, 3), [
    ('Explain why two lines in a plane (two dimensions) cannot be skew.', 'In a plane, two non-parallel lines always meet; skew lines need a third dimension so that they can pass without meeting.', 'B1 non-parallel lines in a plane meet; B1 skew needs 3D [2]'),
    ('Explain why the shortest distance from a point P to a line is measured along the perpendicular.', 'For any other point Q on the line, PQ is the hypotenuse of a right-angled triangle with PF as one side, so PQ > PF.', 'B1 right-angled triangle; B1 hypotenuse longer [2]'),
])


@v94.add('C1', (1, 2, 3))
def v94_c1(r, D):
    if D <= 2:
        s = skew_case(r)
        if not s:
            return None
        return MC(r, f'The lines {lstr(s["a1"], s["d1"])} and {lstr(s["a2"], s["d2"], "μ")} are not parallel and do not intersect. How are they described?', 'skew',
                  ['perpendicular', 'coincident', 'intersecting'], 'Neither parallel nor intersecting lines in 3D are skew.') if D == 1 else \
            MC(r, f'For the lines {lstr(s["a1"], s["d1"])} and {lstr(s["a2"], s["d2"], "μ")}, what is the first check in showing that they are skew?', 'the direction vectors are not multiples of each other',
               ['the position vectors are equal', 'the scalar product of the position vectors is zero', 'λ = μ'], 'Skew lines are not parallel; then show there is no intersection.')
    p = perp_case(r)
    if not p:
        return None
    return MC(r, f'The foot of the perpendicular from P to the line {lstr(p["a"], p["d"])} is F, where λ = {p["l"]}. Find the length PF.', mag_str(p['w']),
              [num(mag2(p['w'])), mag_str(vsub(p['P'], p['a'])) if any(vsub(p['P'], p['a'])) else '1', sqrt_str(mag2(p['w']) + 1)], f'P = ({", ".join(num(x) for x in p["P"])}); F = ({", ".join(num(x) for x in p["F"])}).'
              ) if False else MC(r, f'P is the point ({", ".join(num(x) for x in p["P"])}) and F is the point on the line {lstr(p["a"], p["d"])} with λ = {p["l"]}. Given that PF is perpendicular to the line, find the perpendicular distance from P to the line.',
                                 mag_str(p['w']), [num(mag2(p['w'])), mag_str(vsub(p['P'], p['a'])) if any(vsub(p['P'], p['a'])) and mag2(vsub(p['P'], p['a'])) != mag2(p['w']) else sqrt_str(mag2(p['w']) + 3), sqrt_str(mag2(p['w']) + 1)],
                                 f'F = ({", ".join(num(x) for x in p["F"])}); PF = {vstr(p["w"])}.')


@v94.add('C2', (1, 2, 3, 4), 'explain')
def v94_err(r, D):
    nm = person(r)
    f = r.choice(['twoeq', 'notperp', 'show'])
    if f in ('twoeq', 'show'):
        s = skew_case(r)
        if not s:
            return None
        if f == 'twoeq':
            return Q(f'{nm} solves two of the component equations for the lines {lstr(s["a1"], s["d1"])} and {lstr(s["a2"], s["d2"], "μ")}, finds values of λ and μ, and concludes that the lines intersect. Explain what {nm} has not done.',
                     'The values must also satisfy the third component equation; here they do not, so the lines do not intersect (and as they are not parallel, they are skew).', 'B1 must check the third equation; B1 conclusion skew')
        return Q(f'Show that the lines {lstr(s["a1"], s["d1"])} and {lstr(s["a2"], s["d2"], "μ")} are skew.',
                 'Directions are not multiples, so not parallel; solving two component equations gives λ and μ that fail the third, so no intersection: the lines are skew.', 'B1 not parallel; M1 solves two equations; A1 third inconsistent; A1 conclusion')
    p = perp_case(r)
    if not p:
        return None
    wrong = vsub(p['P'], p['a'])
    if dot(wrong, p['d']) == 0:
        return None
    return Q(f'{nm} says the perpendicular distance from P({", ".join(num(x) for x in p["P"])}) to the line {lstr(p["a"], p["d"])} is AP = {mag_str(wrong)}, where A is the point with λ = 0. Explain the error and find the correct distance.',
             f'AP is not perpendicular to the line (AP · d = {num(dot(wrong, p["d"]))} ≠ 0). The foot F has λ = {p["l"]}; the distance is |PF| = {mag_str(p["w"])}.', 'B1 AP not perpendicular; M1 finds the foot; A1 distance')


@v94.add('C3', (1, 2, 3, 4, 5), 'numerical')
def v94_calc(r, D):
    p = perp_case(r)
    if not p:
        return None
    pt_ = f'P({", ".join(num(x) for x in p["P"])})'
    if D <= 2:
        return Q(f'Find the position vector of the foot of the perpendicular from {pt_} to the line {lstr(p["a"], p["d"])}.', vstr(p['F']) if any(p['F']) else '0', 'M1 general point on the line; M1 PF · d = 0; A1 λ; A1 foot')
    if D <= 4:
        return Q(f'Find the perpendicular distance from {pt_} to the line {lstr(p["a"], p["d"])}.', mag_str(p['w']) + (f' ≈ {n3(math.sqrt(mag2(p["w"])))}' if math.isqrt(mag2(p['w'])) ** 2 != mag2(p['w']) else ''),
                 'M1 general point; M1 scalar product zero; A1 λ; A1 distance')
    refl = vadd(p['F'], p['F'])
    refl = vsub(refl, p['P'])
    return Q(f'Find the position vector of the reflection of {pt_} in the line {lstr(p["a"], p["d"])}.', vstr(refl) if any(refl) else '0', 'M1 finds the foot F; A1 F; M1 OP′ = 2OF − OP; A1 reflection')


def v94_c4(r, D):
    p = perp_case(r)
    if not p:
        return None
    pt_ = f'P({", ".join(num(x) for x in p["P"])})'
    intro = f'The line l has equation {lstr(p["a"], p["d"])} and the point {pt_} does not lie on l.'
    refl = vsub(vadd(p['F'], p['F']), p['P'])
    parts = [
        P('Find the position vector of the foot of the perpendicular from P to l.', vstr(p['F']) if any(p['F']) else '0', 'M1 PF · d = 0; A1 λ; A1 foot'),
        P('Find the perpendicular distance from P to l.', mag_str(p['w']), 'M1 |PF|; A1 exact distance'),
        P('Find the position vector of the reflection of P in l.', vstr(refl) if any(refl) else '0', 'M1 2OF − OP; A1 reflection'),
        P(f'Find the acute angle between OP and the line l, where O is the origin.', d1(min(ang(p['P'], p['d']), 180 - ang(p['P'], p['d'])) if any(p['P']) else 0), 'M1 scalar product; A1 angle'),
    ]
    if not any(p['P']):
        parts = parts[:3]
    return cmp_(r, intro, parts)


v94.add('C4', (2, 3, 4, 5))(v94_c4)

CHAPTERS[9] = [v91, v92, v93, v94]


# ================================================================ Chapter 10 Differential equations

def kd(k):
    return num(float(k)) if isinstance(k, Fr) and k.denominator != 1 else num(k)


DE_CTX = [
    # (statement, variable, DE text, sign, kind)
    ('the rate of increase of the population P of a colony of bacteria is proportional to P', 'P', 'dP/dt = kP', 'growth'),
    ('the mass m of a radioactive substance decreases at a rate proportional to m', 'm', 'dm/dt = −km', 'decay'),
    ('the temperature θ °C of a cup of coffee in a room at {a} °C decreases at a rate proportional to the difference between θ and {a}', 'θ', 'dθ/dt = −k(θ − {a})', 'cool'),
    ('the volume V of water in a leaking tank decreases at a rate proportional to √V', 'V', 'dV/dt = −k√V', 'root'),
    ('the number x of people who have heard a rumour in a town of {a} people increases at a rate proportional to the number who have not yet heard it', 'x', 'dx/dt = k({a} − x)', 'limit'),
    ('the height h of a plant increases at a rate inversely proportional to h', 'h', 'dh/dt = k/h', 'inv'),
    ('the number N of fish in a lake increases at a rate proportional to the product of N and ({a} − N)', 'N', 'dN/dt = kN({a} − N)', 'logistic'),
    ('the radius r of a circular oil slick increases at a rate inversely proportional to r²', 'r', 'dr/dt = k/r²', 'inv2'),
]


def de_ctx(r):
    s, v, de, kind = r.choice(DE_CTX)
    a = r.choice([15, 18, 20, 22, 25]) if kind == 'cool' else r.choice([500, 1000, 2000, 5000, 800])
    return dict(s=s.format(a=a), v=v, de=de.format(a=a), kind=kind, a=a)


def de_rate(kind, k, X, a):
    return {'growth': k * X, 'decay': -k * X, 'cool': -k * (X - a), 'root': -k * math.sqrt(X), 'limit': k * (a - X), 'inv': k / X, 'logistic': k * X * (a - X), 'inv2': k / X ** 2}[kind]


e101 = T('Forming differential equations from a context', 'forming differential equations', 'rate of change model')
e101.fixed('C1', (1, 2), [
    ('The rate of decrease of y is proportional to y. Which equation models this (k > 0)?', 'dy/dt = −ky', 'Decrease means a negative rate.', ['dy/dt = ky', 'dy/dt = −k/y', 'y = −kt']),
    ('The gradient of a curve at (x, y) is proportional to x²y. Which differential equation is this?', 'dy/dx = kx²y', '"Gradient" means dy/dx.', ['dy/dx = kx² + y', 'y = kx²', 'dx/dy = kx²y']),
])
e101.fixed('C2', (2, 3), [
    ('Explain why, in a model dN/dt = −kN with k > 0, the minus sign is needed for a decreasing quantity.', 'With N > 0 and k > 0, −kN is negative, so dN/dt < 0 and N decreases; without the minus sign the model would describe growth.', 'B1 −kN < 0 for N > 0; B1 so N decreases [2]'),
    ('Explain the meaning of "the rate of change of x with respect to t".', 'It is dx/dt: how fast x changes per unit time, the gradient of the graph of x against t.', 'B1 dx/dt; B1 change per unit time / gradient [2]'),
])


@e101.add('C1', (1, 2, 3))
def e101_c1(r, D):
    c = de_ctx(r)
    v = c['v']
    wrongs = {'growth': [f'd{v}/dt = −k{v}', f'd{v}/dt = k', f'{v} = kt'], 'decay': [f'd{v}/dt = km', f'd{v}/dt = −k', f'd{v}/dt = −k/m'],
              'cool': [f'dθ/dt = k(θ − {c["a"]})', f'dθ/dt = −kθ', f'dθ/dt = −k(θ + {c["a"]})'], 'root': ['dV/dt = k√V', 'dV/dt = −kV²', 'dV/dt = −k/√V'],
              'limit': [f'dx/dt = kx', f'dx/dt = k({c["a"]} + x)', f'dx/dt = −k({c["a"]} − x)'], 'inv': ['dh/dt = kh', 'dh/dt = −k/h', 'dh/dt = k/h²'],
              'logistic': [f'dN/dt = kN + ({c["a"]} − N)', f'dN/dt = k({c["a"]} − N)', f'dN/dt = kN/({c["a"]} − N)'], 'inv2': ['dr/dt = kr²', 'dr/dt = k/r', 'dr/dt = −k/r²']}[c['kind']]
    return MC(r, f'In a model, {c["s"]}. Which differential equation (with k a positive constant) describes this?', c['de'], wrongs, 'Translate the statement directly; a decrease gives a negative rate.')


@e101.add('C2', (1, 2, 3, 4), 'explain')
def e101_err(r, D):
    nm = person(r)
    c = de_ctx(r)
    f = r.choice(['sign', 'interp', 'units'])
    if f == 'sign' and c['de'].count('−') >= 1 and c['kind'] in ('decay', 'cool', 'root'):
        wrong = c['de'].replace('= −k', '= k')
        return Q(f'In a model, {c["s"]}. {nm} writes {wrong}, with k > 0. Explain the error and correct it.',
                 f'The quantity is decreasing, so the rate must be negative for positive k: {c["de"]}.', 'B1 rate must be negative; B1 correct equation')
    if f == 'interp':
        return Q(f'In a model, {c["s"]}, giving {c["de"]} with k > 0. Explain what the sign of d{c["v"]}/dt tells you about {c["v"]} and how the rate behaves as {c["v"]} changes.',
                 {'growth': 'positive: P increases, and faster as P grows', 'decay': 'negative: m decreases, more slowly as m gets smaller', 'cool': f'negative while θ > {c["a"]}: θ falls, more slowly as θ approaches {c["a"]}',
                  'root': 'negative: V falls, more slowly as V decreases', 'limit': f'positive while x < {c["a"]}: x increases, more slowly as x approaches {c["a"]}', 'inv': 'positive: h increases, more slowly as h grows',
                  'logistic': f'positive for 0 < N < {c["a"]}: N increases; the rate is small near 0 and near {c["a"]}', 'inv2': 'positive: r increases, more slowly as r grows'}[c['kind']],
                 'B1 sign and direction of change; B1 how the rate depends on the variable')
    k = r.choice([Fr(1, 10), Fr(1, 20), Fr(1, 50), Fr(2, 5), Fr(1, 4)])
    X = r.choice([4, 9, 16, 25, 36, 49]) if c['kind'] == 'root' else r.choice([2, 4, 5, 10, 40, 100])
    if c['kind'] == 'cool':
        X = c['a'] + r.choice([20, 40, 60])
    if c['kind'] in ('limit', 'logistic'):
        X = c['a'] // r.choice([2, 4, 5])
    rate = de_rate(c['kind'], float(k), X, c['a'])
    return Q(f'In a model, {c["s"]}, so {c["de"]}. When {c["v"]} = {X}, the rate of change of {c["v"]} is {n3(rate)} per unit time. Show that k = {kd(k)}.',
             f'Substituting {c["v"]} = {X}: {n3(rate)} = {n3(rate / float(k))}k, so k = {kd(k)}.',
             'M1 substitutes the values; A1 k shown')


@e101.add('C3', (1, 2, 3, 4, 5), 'numerical')
def e101_calc(r, D):
    if D >= 4:
        # connected rates: a cylinder / cone leaking
        A = r.choice([2, 3, 4, 5, 8])
        c = r.choice([Fr(1, 10), Fr(1, 5), Fr(3, 10), Fr(1, 2)])
        h = r.choice([4, 9, 16, 25])
        if D == 4:
            rate = float(c) * math.sqrt(h) / A
            return Q(f'Water leaks from a tank with constant cross-sectional area {A} m². The volume V m³ satisfies dV/dt = −{num(c)}√h, where h m is the depth. Form a differential equation for h and find the rate at which h is decreasing when h = {h}.',
                     f'dh/dt = −({num(c / A)})√h; {n3(rate)} m per unit time', 'M1 V = ' + str(A) + 'h so dV/dt = ' + str(A) + ' dh/dt; A1 differential equation; A1 rate')
        rad = r.choice([1, 2, 3])
        k = r.choice([2, 3, 4, 5])
        rate = k / (4 * math.pi * rad ** 2)
        return Q(f'A spherical balloon is inflated so that its volume increases at a constant rate of {k} cm³ s⁻¹. Form a differential equation for the radius r cm and find dr/dt when r = {rad}.',
                 f'dr/dt = {k}/(4πr²); {n3(rate)} cm s⁻¹', 'M1 dV/dr = 4πr²; M1 chain rule; A1 equation; A1 value')
    c = de_ctx(r)
    k = r.choice([Fr(1, 10), Fr(1, 20), Fr(1, 50), Fr(2, 5), Fr(1, 4), Fr(3, 10)])
    X = r.choice([4, 9, 16, 25, 36, 49]) if c['kind'] == 'root' else r.choice([2, 4, 5, 8, 10, 20, 40])
    if c['kind'] == 'cool':
        X = c['a'] + r.choice([20, 30, 40, 60])
    if c['kind'] in ('limit', 'logistic'):
        X = c['a'] // r.choice([2, 4, 5])
    rate = de_rate(c['kind'], float(k), X, c['a'])
    if c['kind'] == 'logistic':
        k = Fr(1, r.choice([1000, 2000, 5000, 10000]))
        rate = de_rate(c['kind'], float(k), X, c['a'])
    if D <= 2:
        return Q(f'In a model, {c["s"]}. Write down a differential equation for {c["v"]} in terms of t and a positive constant k, and find k given that the rate of change of {c["v"]} is {n3(rate)} per unit time when {c["v"]} = {X}.',
                 f'{c["de"]}; k = {n3(float(k))}', 'B1 differential equation; M1 substitutes; A1 k')
    X2 = X * 2 if c['kind'] not in ('limit', 'logistic', 'cool') else (c['a'] + 2 * (X - c['a']) if c['kind'] == 'cool' else X // 2)
    r2 = de_rate(c['kind'], float(k), X2, c['a'])
    return Q(f'In a model, {c["s"]}, so that {c["de"]}. When {c["v"]} = {X} the rate of change is {n3(rate)} per unit time. Find k and the rate of change when {c["v"]} = {X2}.',
             f'k = {n3(float(k))}; rate = {n3(r2)} per unit time', 'M1 substitutes to find k; A1 k; A1 rate')


def e101_c4(r, D):
    c = de_ctx(r)
    if c['kind'] not in ('growth', 'decay', 'cool', 'limit'):
        return None
    v = c['v']
    k = r.choice([Fr(1, 10), Fr(1, 20), Fr(1, 5), Fr(1, 4), Fr(3, 10)])
    a = c['a']
    if c['kind'] == 'growth':
        X0 = r.choice([100, 200, 500])
        sol = lambda t: X0 * math.exp(float(k) * t)
        ptxt = f'{v} = {X0}e^({kd(k)}t)'
    elif c['kind'] == 'decay':
        X0 = r.choice([50, 80, 100, 200])
        sol = lambda t: X0 * math.exp(-float(k) * t)
        ptxt = f'{v} = {X0}e^(−{kd(k)}t)'
    elif c['kind'] == 'cool':
        X0 = a + r.choice([60, 70, 75])
        sol = lambda t: a + (X0 - a) * math.exp(-float(k) * t)
        ptxt = f'{v} = {a} + {X0 - a}e^(−{kd(k)}t)'
    else:
        X0 = 0
        sol = lambda t: a - a * math.exp(-float(k) * t)
        ptxt = f'{v} = {a}(1 − e^(−{kd(k)}t))'
    rate0 = de_rate(c['kind'], float(k), X0, a)
    t1 = r.choice([5, 10, 15, 20])
    num_ = rk4(lambda t, x: de_rate(c['kind'], float(k), x, a), 0, X0, t1)
    if not ok(num_, sol(t1), 'e101 sol', 1e-6 * max(1, abs(sol(t1)))):
        return None
    intro = f'In a model, {c["s"]}. Initially {v} = {X0}{" and its rate of change is " + n3(rate0) + " per unit time" if rate0 else ""}.'
    if not rate0:
        return None
    parts = [
        P(f'Write down a differential equation relating {v} and t.', c['de'], 'B1 equation'),
        P('Find the value of the constant k.', f'k = {kd(k)}', 'M1 substitutes the initial values; A1 k'),
        P(f'Solve the differential equation to find {v} in terms of t.', ptxt, 'M1 separates variables; A1 integrates; M1 uses initial condition; A1 particular solution'),
        P(f'Find {v} when t = {t1}.', n3(sol(t1)), 'B1 value'),
    ]
    return cmp_(r, intro, parts)


e101.add('C4', (2, 3, 4, 5))(e101_c4)


# ---------------------------------------------------------------- 10.2 separating variables

def sep_family(r, D):
    kinds = {1: ['ky', 'kxy'], 2: ['ky', 'kxy', 'xy2', 'yx'], 3: ['xy2', 'exy', 'yx', 'cos'], 4: ['exy', 'cos', 'atan', 'lin'], 5: ['atan', 'lin', 'pf', 'cos']}[D]
    kind = r.choice(kinds)
    if kind == 'ky':
        k = r.choice([2, 3, Fr(1, 2), -1, -2, Fr(-1, 2)])
        x0, y0 = 0, r.choice([2, 3, 4, 5])
        de, sep = f'dy/dx = {kd(k) if abs(k) != 1 else ("−" if k < 0 else "")}y'.replace('= 1/2y', '= y/2').replace('= −1/2y', '= −y/2'), f'∫ (1/y) dy = ∫ {kd(k)} dx'
        gen = f'y = A{ex(k)}'
        F = lambda x: y0 * math.exp(float(k) * x)
        part = f'y = {y0}{ex(k)}'
        rhs = lambda x, y: float(k) * y
    elif kind == 'kxy':
        k = r.choice([1, 2, 4, -2, -1])
        x0, y0 = 0, r.choice([1, 2, 3, 5])
        de = f'dy/dx = {"" if k == 1 else ("−" if k == -1 else kd(k))}xy'
        sep = f'∫ (1/y) dy = ∫ {"" if k == 1 else kd(k)}x dx'
        gen = f'y = A{ex(Fr(k, 2), 0, "x²")}'
        F = lambda x: y0 * math.exp(k * x * x / 2)
        part = f'y = {"" if y0 == 1 else y0}{ex(Fr(k, 2), 0, "x²")}'
        rhs = lambda x, y: k * x * y
    elif kind == 'xy2':
        x0 = 0
        y0 = r.choice([1, 2, Fr(1, 2)])
        de, sep = 'dy/dx = xy²', '∫ y⁻² dy = ∫ x dx'
        gen = '−1/y = x²/2 + c'
        c = -1 / Fr(y0)
        F = lambda x: 1 / (-(x * x / 2) - float(c))
        part = f'y = 2/({num(-2 * c)} − x²)'
        rhs = lambda x, y: x * y * y
    elif kind == 'yx':
        a = r.choice([1, 2, 3, -1, -2])
        x0, y0 = 1, r.choice([y for y in (2, 3, 5, 6) if y != -a])
        de, sep = f'x dy/dx = y{sg(a)}', f'∫ 1/(y{sg(a)}) dy = ∫ (1/x) dx'
        gen = f'y = Ax{sg(-a)}'
        A = y0 + a
        F = lambda x: A * x - a
        part = f'y = {A}x{sg(-a)}' if A != 1 else f'y = x{sg(-a)}'
        rhs = lambda x, y: (y + a) / x
    elif kind == 'exy':
        x0, y0 = 0, 0
        de, sep = 'dy/dx = e^(x − y)', '∫ eʸ dy = ∫ eˣ dx'
        gen = 'eʸ = eˣ + c'
        F = lambda x: math.log(math.exp(x))
        part = 'y = x'
        k = r.choice([2, 3, 4])
        x0, y0 = 0, math.log(k)
        F = lambda x: math.log(math.exp(x) + k - 1)
        part = f'y = ln(eˣ + {k - 1})'
        rhs = lambda x, y: math.exp(x - y)
        y0t = f'ln {k}'
    elif kind == 'cos':
        x0 = 0
        y0 = r.choice([1, Fr(1, 2), Fr(1, 3)])
        de, sep = 'dy/dx = y² cos x', '∫ y⁻² dy = ∫ cos x dx'
        gen = '−1/y = sin x + c'
        c = -1 / Fr(y0)
        F = lambda x: -1 / (math.sin(x) + float(c))
        part = f'y = 1/({num(-c)} − sin x)'
        rhs = lambda x, y: y * y * math.cos(x)
    elif kind == 'atan':
        x0, y0 = 0, 0
        de, sep = 'dy/dx = x(1 + y²)', '∫ 1/(1 + y²) dy = ∫ x dx'
        gen = 'tan⁻¹ y = x²/2 + c'
        y0 = 1
        F = lambda x: math.tan(x * x / 2 + math.pi / 4)
        part = 'y = tan(x²/2 + π/4)'
        rhs = lambda x, y: x * (1 + y * y)
    elif kind == 'lin':
        N = r.choice([20, 50, 100])
        k = r.choice([Fr(1, 2), Fr(1, 4), Fr(1, 5), 2])
        x0, y0 = 0, r.choice([0, N // 2, N * 2])
        if y0 == N:
            return None
        de, sep = f'dy/dx = {kd(k)}({N} − y)'.replace('= 2(', '= 2('), f'∫ 1/({N} − y) dy = ∫ {kd(k)} dx'
        gen = f'y = {N} − Ae^(−{kd(k)}x)'
        F = lambda x: N - (N - y0) * math.exp(-float(k) * x)
        part = f'y = {N} − {num(N - y0)}e^(−{kd(k)}x)' if N - y0 > 0 else f'y = {N} + {num(y0 - N)}e^(−{kd(k)}x)'
        rhs = lambda x, y: float(k) * (N - y)
    else:
        # dy/dx = y / (x(x + 1)), x > 0: ln y = ln x − ln(x + 1) + c, y = Ax/(x + 1)
        x0, y0 = 1, r.choice([1, 2, 3, 4])
        de, sep = 'x(x + 1) dy/dx = y', '∫ (1/y) dy = ∫ 1/(x(x + 1)) dx'
        gen = 'y = Ax/(x + 1)'
        F = lambda x: 2 * y0 * x / (x + 1)
        part = f'y = {2 * y0}x/(x + 1)'
        rhs = lambda x, y: y / (x * (x + 1))
    x1 = float(x0) + r.choice([0.5, 1, 1.5]) if kind not in ('xy2', 'cos', 'atan') else float(x0) + 0.5
    try:
        yr = rk4(rhs, float(x0), float(y0), x1)
        ye = F(x1)
    except (ValueError, ZeroDivisionError, OverflowError):
        return None
    if not ok(yr, ye, 'sep ' + kind, 1e-6 * max(1, abs(ye))) or not ok(F(float(x0)), float(y0), 'sep ic ' + kind, 1e-9):
        return None
    y0t = locals().get('y0t') or num(y0)
    return dict(kind=kind, de=de, sep=sep, gen=gen, part=part, x0=x0, y0=y0, y0t=y0t, x1=x1, y1=ye, F=F)


e102 = T('Solving first-order differential equations by separating variables', 'separating variables', 'first-order differential equations')
e102.fixed('C1', (1, 2), [
    ('What is the general solution of dy/dx = 3y?', 'y = Ae³ˣ', 'ln|y| = 3x + c.', ['y = 3x + c', 'y = e³ˣ + c', 'y = (3/2)y² + c']),
    ('Separating the variables in dy/dx = x²/y gives which equation?', '∫ y dy = ∫ x² dx', 'Multiply by y and by dx.', ['∫ (1/y) dy = ∫ x² dx', '∫ y dx = ∫ x² dy', '∫ x² y dx = 0']),
])
e102.fixed('C2', (2, 3), [
    ('Explain why ln|y| = 2x + c leads to y = Ae²ˣ, where A is a constant.', '|y| = e²ˣ⁺ᶜ = eᶜ e²ˣ; writing A = ±eᶜ (a constant) gives y = Ae²ˣ.', 'B1 exponentiates; B1 constant A = ±eᶜ [2]'),
    ('Explain why only one arbitrary constant is needed when solving a first-order differential equation by separating the variables.', 'Constants from integrating both sides can be combined into a single constant, and a first-order equation needs one condition to fix it.', 'B1 constants combine; B1 one condition gives the particular solution [2]'),
])


@e102.add('C1', (1, 2, 3))
def e102_c1(r, D):
    d = sep_family(r, D)
    if not d:
        return None
    if r.random() < 0.5:
        return MC(r, f'Which of the following is obtained by separating the variables in {d["de"]}?', d['sep'],
                  [d['sep'].replace('∫ ', '∫ (', 1).replace(' dy', ') dx', 1).replace(' dx', ' dy', 1) if False else d['sep'].replace(' dy', ' dQ').replace(' dx', ' dy').replace(' dQ', ' dx'),
                   d['sep'].replace('= ∫', '= −∫'), d['sep'].split(' = ')[0] + ' = 0'], 'Collect y-terms with dy and x-terms with dx.')
    return MC(r, f'Find the general solution of {d["de"]}.', d['gen'], [d['gen'].replace('A', '').replace('= e', '= e').strip() + ' + A' if 'A' in d['gen'] else d['gen'].replace(' + c', ''),
              d['gen'].replace('−', '+') if '−' in d['gen'] else d['gen'].replace('= ', '= −', 1), d['de'].split(' = ')[1] + ' + c' if 'dy/dx = ' in d['de'] else 'y = Ax'], 'Separate, integrate both sides, include one constant.')


@e102.add('C2', (1, 2, 3, 4), 'explain')
def e102_err(r, D):
    nm = person(r)
    d = sep_family(r, max(2, D))
    if not d:
        return None
    f = r.choice(['noconst', 'late', 'show'])
    if f == 'noconst':
        return Q(f'{nm} solves {d["de"]} by separating the variables but omits the constant of integration, then cannot satisfy the condition y = {d["y0t"]} when x = {num(d["x0"])}. Explain the problem and give the correct particular solution.',
                 f'Without a constant only one curve is found; including it gives {d["gen"]}, and the condition gives {d["part"]}.', 'B1 constant needed for the family of solutions; B1 correct particular solution')
    if f == 'late':
        return Q(f'{nm} solves {d["de"]} and writes the answer without using the condition y = {d["y0t"]} when x = {num(d["x0"])}. Explain the difference between the general and particular solutions here.',
                 f'General: {d["gen"]} (a family of curves). Particular: the condition fixes the constant, giving {d["part"]}.', 'B1 general solution is a family; B1 particular solution found')
    return Q(f'Show that {d["part"]} satisfies {d["de"]} and the condition y = {d["y0t"]} when x = {num(d["x0"])}.', 'Differentiate and substitute: both sides agree; substituting x gives the stated value of y.',
             'M1 differentiates and substitutes; A1 both conditions verified')


@e102.add('C3', (1, 2, 3, 4, 5), 'numerical')
def e102_calc(r, D):
    d = sep_family(r, D)
    if not d:
        return None
    if r.random() < 0.5:
        return Q(f'Solve the differential equation {d["de"]}, given that y = {d["y0t"]} when x = {num(d["x0"])}. Give y in terms of x.', d['part'],
                 'M1 separates variables; A1 correct integration of both sides; M1 uses the condition; A1 particular solution')
    return Q(f'Given that y = {d["y0t"]} when x = {num(d["x0"])}, solve {d["de"]} and find the value of y when x = {num(d["x1"])}, giving your answer to 3 significant figures.',
             f'{d["part"]}; y = {n3(d["y1"])}', 'M1 separates variables; A1 integrates; M1 uses the condition; A1 solution; A1 value')


def e102_c4(r, D):
    d = sep_family(r, max(2, D))
    if not d:
        return None
    intro = f'The variables x and y satisfy the differential equation {d["de"]}, and y = {d["y0t"]} when x = {num(d["x0"])}.'
    parts = [
        P('Find the general solution.', d['gen'], 'M1 separates; A1 integrates both sides; A1 general solution'),
        P('Find the particular solution, giving y in terms of x.', d['part'], 'M1 uses the condition; A1 particular solution'),
        P(f'Find the value of y when x = {num(d["x1"])}.', n3(d['y1']), 'B1 value'),
    ]
    return cmp_(r, intro, parts)


e102.add('C4', (2, 3, 4, 5))(e102_c4)


# ---------------------------------------------------------------- 10.3 interpreting solutions

def model_case(r):
    kind = r.choice(['cool', 'decay', 'growth', 'limit'])
    k = r.choice([Fr(1, 10), Fr(1, 20), Fr(1, 5), Fr(1, 4), Fr(1, 25), Fr(3, 20)])
    kf = float(k)
    if kind == 'cool':
        a = r.choice([15, 18, 20, 22])
        X0 = a + r.choice([50, 60, 70, 75])
        s = f'The temperature θ °C of a liquid t minutes after it is placed in a room is given by θ = {a} + {X0 - a}e^(−{kd(k)}t)'
        v, unit, lim = 'θ', 'minutes', a
        f = lambda t: a + (X0 - a) * math.exp(-kf * t)
        targ = a + (X0 - a) * r.choice([0.5, 0.25, 0.4])
        de = f'dθ/dt = −{kd(k)}(θ − {a})'
    elif kind == 'decay':
        X0 = r.choice([40, 60, 80, 100, 200])
        s = f'The mass m grams of a radioactive substance after t days is given by m = {X0}e^(−{kd(k)}t)'
        v, unit, lim = 'm', 'days', 0
        f = lambda t: X0 * math.exp(-kf * t)
        targ = X0 * r.choice([0.5, 0.25, 0.1])
        de = f'dm/dt = −{kd(k)}m'
    elif kind == 'growth':
        X0 = r.choice([100, 250, 500, 1000])
        s = f'The number of bacteria N in a culture after t hours is modelled by N = {X0}e^({kd(k)}t)'
        v, unit, lim = 'N', 'hours', None
        f = lambda t: X0 * math.exp(kf * t)
        targ = X0 * r.choice([2, 3, 5, 10])
        de = f'dN/dt = {kd(k)}N'
    else:
        a = r.choice([200, 500, 1000, 2000])
        X0 = 0
        s = f'The number x of people in a town of {a} who have heard a rumour after t days is modelled by x = {a}(1 − e^(−{kd(k)}t))'
        v, unit, lim = 'x', 'days', a
        f = lambda t: a * (1 - math.exp(-kf * t))
        targ = a * r.choice([0.5, 0.75, 0.9])
        de = f'dx/dt = {kd(k)}({a} − x)'
    tt = bisect(lambda t: f(t) - targ, 0, 2000)
    if not ok(f(tt), targ, 'model t', 1e-6 * max(1, targ)):
        return None
    return dict(kind=kind, s=s, v=v, unit=unit, lim=lim, f=f, targ=targ, t=tt, X0=X0, k=k, de=de)


e103 = T('Interpreting general and particular solutions in context', 'general and particular solutions', 'interpreting solutions in context')
e103.fixed('C1', (1, 2), [
    ('What distinguishes a particular solution from a general solution of a differential equation?', 'The constant has been fixed using a given condition', 'A general solution contains an arbitrary constant.', ['It has no exponential terms', 'It is valid only at one point', 'It is found without integration']),
    ('θ = 20 + 60e^(−0.1t). What happens to θ as t becomes very large?', 'θ approaches 20', 'e^(−0.1t) → 0.', ['θ approaches 80', 'θ approaches 0', 'θ increases without limit']),
])
e103.fixed('C2', (2, 3), [
    ('Explain why a model N = 500e^(0.2t) for a population cannot be valid for all t.', 'It predicts unlimited growth; in reality limited food and space slow the growth, so the model only applies for a limited time.', 'B1 unlimited growth predicted; B1 real limits on resources [2]'),
])


@e103.add('C1', (1, 2, 3))
def e103_c1(r, D):
    m = model_case(r)
    if not m:
        return None
    if D <= 2 and m['lim'] is not None:
        return MC(r, f'{m["s"]}. What value does {m["v"]} approach in the long term?', num(m['lim']), [num(m['X0']) if m['X0'] != m['lim'] else '1', num(m['lim'] + 10), 'it increases without limit', 'it decreases without limit'], 'The exponential term tends to 0.')
    return MC(r, f'{m["s"]}. What is the initial value of {m["v"]}?', num(m['X0']), [num(m['X0'] + 1) if m['X0'] else '1', num(m['lim']) if m['lim'] not in (None, m['X0']) else num(m['X0'] * 2 + 1), num(float(m['k'])) if m['X0'] != float(m['k']) else '5', num(m['X0'] * 2 + 3)],
              'Substitute t = 0.')


@e103.add('C2', (1, 2, 3, 4), 'explain')
def e103_err(r, D):
    nm = person(r)
    m = model_case(r)
    if not m:
        return None
    f = r.choice(['limit', 'realism', 'meaning'])
    if f == 'limit' and m['lim'] is not None:
        bad = m['X0'] if m['X0'] else m['lim'] * 2
        return Q(f'{m["s"]}. {nm} claims that {m["v"]} will eventually reach {num(bad) if m["lim"] != bad else num(bad + 5)}. Explain why this is wrong and state the long-term behaviour.',
                 f'As t → ∞ the exponential term tends to 0, so {m["v"]} approaches {num(m["lim"])} but never reaches it.', 'B1 exponential term → 0; B1 limiting value stated')
    if f == 'meaning':
        return Q(f'{m["s"]}. Explain the significance of the constant {kd(m["k"])} in this model.',
                 f'It is the rate constant in {m["de"]}: a larger value makes {m["v"]} change faster.', 'B1 links to the differential equation; B1 larger constant means faster change')
    return Q(f'{m["s"]}. State one limitation of this model.', {'cool': 'it assumes the room temperature is constant', 'decay': 'it treats mass as continuous although it consists of atoms; it is accurate for large amounts',
                                                                  'growth': 'it predicts unlimited growth, ignoring limited food and space', 'limit': 'it assumes everyone eventually hears; it treats x as continuous'}[m['kind']],
             'B1 a valid limitation; B1 reason linked to the context')


@e103.add('C3', (1, 2, 3, 4, 5), 'numerical')
def e103_calc(r, D):
    m = model_case(r)
    if not m:
        return None
    if D <= 2:
        t = r.choice([5, 10, 20])
        return Q(f'{m["s"]}. Find the value of {m["v"]} when t = {t}.', n3(m['f'](t)), 'M1 substitutes; A1 value')
    if D <= 4:
        return Q(f'{m["s"]}. Find the time taken for {m["v"]} to reach {n3(m["targ"])}.', f'{n3(m["t"])} {m["unit"]}', 'M1 rearranges; M1 takes logarithms; A1 time')
    rate = ndiff(m['f'], m['t'])
    return Q(f'{m["s"]}. Find the rate of change of {m["v"]} at the moment when {m["v"]} = {n3(m["targ"])}.', f'{n3(rate)} per {m["unit"][:-1]}', 'M1 differentiates or uses the differential equation; M1 finds the time or substitutes directly; A1 rate')


def e103_c4(r, D):
    m = model_case(r)
    if not m:
        return None
    intro = f'A quantity {m["v"]} satisfies the differential equation {m["de"]}, where t is the time in {m["unit"]}, and {m["v"]} = {m["X0"]} when t = 0.'
    sol = m['s'].split(' is given by ')[-1].split(' is modelled by ')[-1]
    parts = [
        P(f'Solve the differential equation, obtaining {m["v"]} in terms of t.', sol, 'M1 separates; A1 integrates; M1 uses the initial condition; A1 solution'),
        P(f'Find the time when {m["v"]} = {n3(m["targ"])}.', f'{n3(m["t"])} {m["unit"]}', 'M1 logarithms; A1 time'),
        P(f'State what happens to {m["v"]} as t becomes large.', f'{m["v"]} → {num(m["lim"])}' if m['lim'] is not None else f'{m["v"]} increases without limit', 'B1 long-term behaviour'),
    ]
    return cmp_(r, intro, parts)


e103.add('C4', (2, 3, 4, 5))(e103_c4)

CHAPTERS[10] = [e101, e102, e103]


# ================================================================ Chapter 11 Complex numbers

def cz(r, lo=-6, hi=6, nonreal=True):
    while True:
        a, b = r.randint(lo, hi), r.randint(lo, hi)
        if (b != 0 or not nonreal) and (a or b):
            return complex(a, b)


def cs(z):
    return cstr(Fr(z.real).limit_denominator(1000), Fr(z.imag).limit_denominator(1000))


def cfr(a, b):
    return cstr(a, b)


def cdiv(a, b, c, d):
    """(a + bi)/(c + di) exactly."""
    den = c * c + d * d
    return Fr(a * c + b * d, den), Fr(b * c - a * d, den)


def argt(z):
    """Argument in radians to 3 s.f."""
    return n3(math.atan2(z.imag, z.real))


c111 = T('Complex numbers: Cartesian form, arithmetic and conjugates', 'complex numbers', 'conjugates', 'Cartesian form')
c111.fixed('C1', (1, 2), [
    ('What is i⁴?', '1', 'i² = −1, so i⁴ = (−1)² = 1.', ['−1', 'i', '−i']),
    ('What is the complex conjugate of 3 − 4i?', '3 + 4i', 'Change the sign of the imaginary part.', ['−3 + 4i', '−3 − 4i', '4 − 3i']),
    ('What is (2 + i)(2 − i)?', '5', '4 − i² = 5.', ['3', '4 − i', '5 − 4i']),
])
c111.fixed('C2', (2, 3), [
    ('Explain why multiplying the numerator and denominator of a fraction by the conjugate of the denominator gives a real denominator.', '(c + di)(c − di) = c² + d², which is real, so the result can be written in the form x + iy.', 'B1 (c + di)(c − di) = c² + d²; B1 real so x + iy form [2]'),
    ('Explain why z + z* is always real for any complex number z.', 'If z = x + iy then z* = x − iy, so z + z* = 2x, which is real.', 'B1 writes z and z*; B1 imaginary parts cancel [2]'),
])


@c111.add('C1', (1, 2, 3))
def c111_c1(r, D):
    a, b, c, d = r.randint(-5, 5), nz(r, -5, 5), r.randint(-5, 5), nz(r, -5, 5)
    if D == 1:
        return MC(r, f'Find ({cstr(a, b)}) + ({cstr(c, d)}).', cstr(a + c, b + d), [cstr(a - c, b - d), cstr(a + c, b - d), cstr(a * c, b * d), cstr(a + b, c + d)], 'Add real and imaginary parts separately.')
    if D == 2:
        re_, im = a * c - b * d, a * d + b * c
        return MC(r, f'Find ({cstr(a, b)})({cstr(c, d)}).', cstr(re_, im), [cstr(a * c + b * d, im), cstr(a * c, b * d), cstr(re_, -im), cstr(a * c - b * d, a * d - b * c)], 'Expand and use i² = −1.')
    x, y = cdiv(a, b, c, d)
    return MC(r, f'Find the real part of ({cstr(a, b)})/({cstr(c, d)}).', num(x), [num(y), num(Fr(a, c)) if c else num(x + 1), num(-x) if x else '1', num(Fr(a * c - b * d, c * c + d * d))],
              'Multiply numerator and denominator by the conjugate of the denominator.')


@c111.add('C2', (1, 2, 3, 4), 'explain')
def c111_err(r, D):
    nm = person(r)
    a, b, c, d = r.randint(-5, 5), nz(r, -5, 5), r.randint(-5, 5), nz(r, -5, 5)
    f = r.choice(['isq', 'div', 'conj'])
    if f == 'isq':
        w = (a * c + b * d, a * d + b * c)
        return Q(f'{nm} expands ({cstr(a, b)})({cstr(c, d)}) and obtains {cstr(*w)}. Explain the error and give the correct product.',
                 f'{nm} has used i² = 1; with i² = −1 the product is {cstr(a * c - b * d, a * d + b * c)}.', 'B1 identifies i² = −1; B1 correct product')
    if f == 'div':
        x, y = cdiv(a, b, c, d)
        return Q(f'{nm} writes ({cstr(a, b)})/({cstr(c, d)}) = {cstr(Fr(a, c) if c else a, Fr(b, d))} by dividing the real parts and the imaginary parts. Show that this is wrong and find the correct quotient.',
                 f'Multiplying by ({cstr(c, -d)})/({cstr(c, -d)}) gives {cstr(x, y)}.', 'M1 multiplies by the conjugate; A1 correct quotient')
    x, y = r.randint(-5, 5), nz(r, -5, 5)
    k = r.choice([2, 3, -2])
    rhs = (x + k * x, y - k * y)
    if rhs[1] == 0:
        return None
    return Q(f'Show that the equation z + {num(k) if k > 0 else "(" + num(k) + ")"}z* = {cstr(*rhs)} has the solution z = {cstr(x, y)}.',
             f'With z = {cstr(x, y)}, z* = {cstr(x, -y)}: z + {num(k) if k > 0 else "(" + num(k) + ")"}z* = {cstr(*rhs)}.', 'M1 substitutes z and z*; A1 verifies')


@c111.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c111_calc(r, D):
    a, b, c, d = r.randint(-6, 6), nz(r, -6, 6), r.randint(-6, 6), nz(r, -6, 6)
    if D == 1:
        return Q(f'Given z = {cstr(a, b)} and w = {cstr(c, d)}, find zw in the form x + iy.', cstr(a * c - b * d, a * d + b * c), 'M1 expands with i² = −1; A1 answer')
    if D == 2:
        x, y = cdiv(a, b, c, d)
        return Q(f'Express ({cstr(a, b)})/({cstr(c, d)}) in the form x + iy, where x and y are real.', cstr(x, y), 'M1 multiplies by the conjugate; A1 real part; A1 imaginary part')
    if D == 3:
        x, y = r.randint(-5, 5), nz(r, -5, 5)
        k = r.choice([2, 3, -2, -3, 4])
        rhs = (x + k * x, y - k * y)
        if rhs[1] == 0 or rhs[0] == 0 and k == -1:
            return None
        return Q(f'Solve the equation z + {num(k) if k > 0 else "(" + num(k) + ")"}z* = {cstr(*rhs)}, giving z in the form x + iy.', cstr(x, y), 'M1 sets z = x + iy; M1 equates real and imaginary parts; A1 answer')
    if D == 4:
        p, q = r.randint(-4, 4), r.randint(1, 5)
        # z² − 2pz + (p² + q²) = 0
        return Q(f'Solve the equation z² {"+" if -2 * p >= 0 else "−"} {abs(2 * p)}z + {p * p + q * q} = 0, giving your answers in the form x + iy.'.replace(' + 0z', '').replace(' − 0z', ''),
                 f'z = {cstr(p, q)} or z = {cstr(p, -q)}', 'M1 formula or completing the square; A1 both roots')
    x, y = cdiv(a, b, c, d)
    w = complex(a, b) * complex(c, -d)
    m = Fr(a * a + b * b, c * c + d * d)
    return Q(f'Given z = {cstr(a, b)} and w = {cstr(c, d)}, find z/w in the form x + iy, and verify that |z/w| = |z|/|w|.', f'{cstr(x, y)}; |z/w| = √({num(x * x + y * y)}) and |z|/|w| = √{a * a + b * b}/√{c * c + d * d} = √({num(m)}), so they are equal', 'M1 conjugate; A1 quotient; M1 moduli; A1 verified')


def c111_c4(r, D):
    p, q = r.randint(-4, 4), r.randint(1, 5)
    c, d = r.randint(-4, 4), nz(r, -4, 4)
    z = (p, q)
    intro = f'The complex numbers z and w are given by z = {cstr(p, q)} and w = {cstr(c, d)}.'
    zz = (p * p - q * q, 2 * p * q)
    x, y = cdiv(p, q, c, d)
    parts = [
        P('Find z² in the form x + iy.', cstr(*zz), 'M1 expands; A1 answer'),
        P('Find z/w in the form x + iy.', cstr(x, y), 'M1 multiplies by the conjugate; A1 answer'),
        P('Find z + z* and zz*.', f'z + z* = {num(2 * p)}, zz* = {p * p + q * q}', 'B1 B1'),
        P('Hence find a quadratic equation with real coefficients that has z as a root.', f'z² {"−" if 2 * p >= 0 else "+"} {abs(2 * p)}z + {p * p + q * q} = 0'.replace(' − 0z', '').replace(' + 0z', ''), 'M1 uses sum and product of roots; A1 equation'),
    ]
    return cmp_(r, intro, parts)


c111.add('C4', (2, 3, 4, 5))(c111_c4)


# ---------------------------------------------------------------- 11.2 Argand diagram, modulus and argument

def mco(m):
    """Modulus as a coefficient: '' for 1, (2/3) for fractions."""
    m = Fr(m)
    return '' if m == 1 else (num(m) if m.denominator == 1 else f'({num(m)})')


def eit(m, f):
    """m e^(fπ i) text, e.g. 3e^(−πi/6)."""
    return f'{mco(m)}e^({pi_frac(f).replace("π", "πi")})'


def polt(m, f):
    return f'{mco(m)}(cos({pi_frac(f)}) + i sin({pi_frac(f)}))' if m != 1 else f'cos({pi_frac(f)}) + i sin({pi_frac(f)})'


SPEC_ARG = [Fr(1, 6), Fr(1, 4), Fr(1, 3), Fr(1, 2), Fr(2, 3), Fr(3, 4), Fr(5, 6), Fr(1), Fr(-1, 6), Fr(-1, 4), Fr(-1, 3), Fr(-1, 2), Fr(-2, 3), Fr(-3, 4), Fr(-5, 6)]


def sq_val(q, k):
    """Text and value for q√k (k in 1, 2, 3)."""
    q = Fr(q)
    if q == 0:
        return '0', 0.0
    if k == 1:
        return num(q), float(q)
    a = abs(q)
    body = ('' if a.numerator == 1 else str(a.numerator)) + f'√{k}' + ('' if a.denominator == 1 else f'/{a.denominator}')
    return (MINUS if q < 0 else '') + body, float(q) * math.sqrt(k)


def cs_exact(f):
    """cos and sin of fπ for special f as (q, k) pairs (value q√k)."""
    deg = round(float(f) * 180)
    table = {0: ((1, 1), (0, 1)), 30: ((Fr(1, 2), 3), (Fr(1, 2), 1)), 45: ((Fr(1, 2), 2), (Fr(1, 2), 2)), 60: ((Fr(1, 2), 1), (Fr(1, 2), 3)), 90: ((0, 1), (1, 1))}
    s1 = 1 if deg >= 0 else -1
    a = abs(deg)
    if a <= 90:
        (c, s) = table[a]
        cs_ = 1
    else:
        (c, s) = table[180 - a]
        cs_ = -1
    return (cs_ * Fr(c[0]), c[1]), (s1 * Fr(s[0]), s[1])


def polar_z(r, mod=None, f=None):
    mod = mod or r.choice([1, 2, 3, 4, 6])
    f = f if f is not None else r.choice(SPEC_ARG)
    (cq, ck), (sq_, sk) = cs_exact(f)
    re_t, re_v = sq_val(mod * cq, ck)
    im_t, im_v = sq_val(mod * sq_, sk)
    if im_v == 0:
        zt = re_t
    elif re_v == 0:
        it = im_t.lstrip('−')
        it = '' if it == '1' else (f'({it})' if '/' in it else it)
        zt = ('−' if im_v < 0 else '') + (it + 'i' if '√' not in it or '/' in it else 'i' + it)
    else:
        it = im_t.lstrip('−')
        it = '' if it == '1' else (f'({it})' if '/' in it else it)
        zt = f'{re_t} {"−" if im_v < 0 else "+"} {it + "i" if "√" not in it or "/" in it else "i" + it}'
    return dict(mod=mod, f=f, zt=zt, z=complex(re_v, im_v), pol=polt(mod, f), exp=eit(mod, f))


c112 = T('Argand diagrams, modulus and argument and polar form', 'argand diagram', 'modulus and argument', 'polar form')
c112.fixed('C1', (1, 2), [
    ('In which range is the principal argument θ of a complex number given?', '−π < θ ≤ π', 'The principal argument is measured from the positive real axis.', ['0 ≤ θ < π', '0 < θ ≤ 2π', '−π/2 < θ < π/2']),
    ('What is the modulus of 5 − 12i?', '13', '√(25 + 144) = 13.', ['7', '17', '√119']),
    ('What is the argument of −3?', 'π', '−3 lies on the negative real axis.', ['0', '−π/2', '3π/2']),
])
c112.fixed('C2', (2, 3), [
    ('Explain why arg(−1 − i) is not tan⁻¹(1) = π/4.', '−1 − i lies in the third quadrant, so its argument is −π + π/4 = −3π/4; tan⁻¹ only gives angles between −π/2 and π/2.', 'B1 third quadrant; B1 −3π/4 [2]'),
])


@c112.add('C1', (1, 2, 3))
def c112_c1(r, D):
    z = cz(r)
    if D == 1:
        m2 = int(z.real ** 2 + z.imag ** 2)
        return MC(r, f'Find the modulus of {cs(z)}.', sqrt_str(m2), [num(int(abs(z.real) + abs(z.imag))), num(m2), sqrt_str(abs(int(z.real ** 2 - z.imag ** 2))) if z.real ** 2 != z.imag ** 2 else '0', sqrt_str(m2 + 1)], 'Modulus = √(x² + y²).')
    if D == 2:
        q = ('first' if z.real > 0 and z.imag > 0 else 'second' if z.real < 0 < z.imag else 'third' if z.real < 0 and z.imag < 0 else 'fourth')
        if z.real == 0:
            return None
        return MC(r, f'On an Argand diagram, in which quadrant does {cs(z)} lie?', q, [x for x in ['first', 'second', 'third', 'fourth'] if x != q], 'Real part is the x-coordinate; imaginary part the y-coordinate.')
    p = polar_z(r)
    return MC(r, f'Find the argument of {p["zt"]}.', pi_frac(p['f']), [pi_frac(-p['f']) if p['f'] != 1 else '0', pi_frac(1 - p['f']) if p['f'] > 0 else pi_frac(-1 - p['f']), pi_frac(Fr(1, 2) - p['f']) if abs(Fr(1, 2) - p['f']) <= 1 and Fr(1, 2) != p['f'] * 2 else pi_frac(p['f'] / 2)],
              'Find the quadrant first, then the angle from the positive real axis.')


@c112.add('C2', (1, 2, 3, 4), 'explain')
def c112_err(r, D):
    nm = person(r)
    z = cz(r)
    if z.real >= 0:
        z = complex(-z.real if z.real else -2, z.imag)
    f = r.choice(['quad', 'deg', 'show'])
    wrong = math.atan(z.imag / z.real)
    if f == 'quad':
        return Q(f'{nm} finds arg({cs(z)}) = tan⁻¹({num(Fr(int(z.imag), int(z.real)))}) = {n3(wrong)}. Explain why this is wrong and find the correct argument.',
                 f'{cs(z)} is in the {"second" if z.imag > 0 else "third"} quadrant, so arg = {n3(wrong)} {"+" if z.imag > 0 else "−"} π = {argt(z)}.', 'B1 identifies the quadrant; B1 correct argument')
    if f == 'deg':
        return Q(f'{nm} gives the argument of {cs(z)} as {d1(math.degrees(math.atan2(z.imag, z.real)))}. Explain why this should be converted, and give the argument in radians.',
                 f'Arguments are normally given in radians in the range −π < θ ≤ π: arg = {argt(z)}.', 'B1 radians expected; B1 value')
    p = polar_z(r)
    return Q(f'Show that {p["zt"]} can be written as {p["pol"]}.', f'|z| = {p["mod"]}, arg z = {pi_frac(p["f"])}.', 'M1 modulus; A1 argument and polar form')


@c112.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c112_calc(r, D):
    if D <= 2:
        z = cz(r)
        m2 = int(z.real ** 2 + z.imag ** 2)
        return Q(f'Find the modulus and argument of {cs(z)}, giving the argument in radians to 3 significant figures.', f'|z| = {sqrt_str(m2)}, arg z = {argt(z)}', 'B1 modulus; M1 correct quadrant; A1 argument')
    if D == 3:
        p = polar_z(r)
        return Q(f'Express {p["zt"]} in the form r(cos θ + i sin θ), where r > 0 and −π < θ ≤ π, giving exact values.', p['pol'], 'B1 r; M1 quadrant; A1 θ exact')
    if D == 4:
        p = polar_z(r)
        return Q(f'The complex number z has modulus {p["mod"]} and argument {pi_frac(p["f"])}. Find z in the form x + iy, giving exact values.', p['zt'], 'M1 x = r cos θ, y = r sin θ; A1 exact answer')
    z = cz(r, -5, 5)
    w = z * z
    return Q(f'The complex number z = {cs(z)}. Find |z²| and arg(z²), giving the argument in radians to 3 significant figures, in the range −π < θ ≤ π.',
             f'|z²| = {int(round(abs(w)))}, arg(z²) = {argt(w)}', 'M1 squares or uses |z|²; A1 modulus; M1 2 arg z adjusted to the range; A1 argument')


def c112_c4(r, D):
    p = polar_z(r)
    z = p['z']
    w = z.conjugate()
    intro = f'The complex number z is given by z = {p["zt"]}.'
    if z.imag == 0:
        return None
    parts = [
        P('Find the modulus and argument of z, giving exact values.', f'|z| = {p["mod"]}, arg z = {pi_frac(p["f"])}', 'B1 modulus; B1 argument'),
        P('Express z in the form r(cos θ + i sin θ).', p['pol'], 'B1 polar form'),
        P('State the modulus and argument of z*, and describe the position of z* on an Argand diagram relative to z.', f'|z*| = {p["mod"]}, arg z* = {pi_frac(-p["f"])}; reflection of z in the real axis', 'B1 modulus and argument; B1 reflection in the real axis'),
        P('Express z in the form re^(iθ).', p['exp'], 'B1 exponential form'),
    ]
    return cmp_(r, intro, parts)


c112.add('C4', (2, 3, 4, 5))(c112_c4)


# ---------------------------------------------------------------- 11.3 polar and exponential multiplication

def redarg(f):
    f = Fr(f)
    while f > 1:
        f -= 2
    while f <= -1:
        f += 2
    return f


c113 = T('Multiplying and dividing in polar and exponential form', 'polar form multiplication', 'exponential form', 'multiplying and dividing complex numbers')
c113.fixed('C1', (1, 2), [
    ('If |z| = 3 and |w| = 4, what is |zw|?', '12', '|zw| = |z||w|.', ['7', '1', '3/4']),
    ('If arg z = π/3 and arg w = π/6, what is arg(z/w)?', 'π/6', 'arg(z/w) = arg z − arg w.', ['π/2', 'π/18', '2']),
    ('What is e^(iπ)?', '−1', 'cos π + i sin π = −1.', ['1', 'i', '−i']),
])
c113.fixed('C2', (2, 3), [
    ('Explain why multiplying a complex number by i rotates its point on an Argand diagram by π/2 anticlockwise.', 'i has modulus 1 and argument π/2; multiplying multiplies moduli (by 1) and adds arguments (π/2), which is a rotation through π/2.', 'B1 |i| = 1 and arg i = π/2; B1 arguments add so rotation [2]'),
])


@c113.add('C1', (1, 2, 3))
def c113_c1(r, D):
    m1, m2 = r.choice([2, 3, 4, 5]), r.choice([2, 3, 4, 6])
    f1, f2 = r.choice(SPEC_ARG), r.choice(SPEC_ARG)
    if D == 1:
        return MC(r, f'z = {m1}(cos({pi_frac(f1)}) + i sin({pi_frac(f1)})) and w = {m2}(cos({pi_frac(f2)}) + i sin({pi_frac(f2)})). Find |zw|.', str(m1 * m2), [str(m1 + m2), num(Fr(m1, m2)), str(m1 * m2 * 2)], 'Moduli multiply.')
    if D == 2:
        a = redarg(f1 + f2)
        return MC(r, f'z = {eit(m1, f1)} and w = {eit(m2, f2)}. Find arg(zw) in the range −π < θ ≤ π.', pi_frac(a), [pi_frac(redarg(f1 - f2)), pi_frac(redarg(f1 * f2)) if redarg(f1 * f2) != a else pi_frac(redarg(a + Fr(1, 2))), pi_frac(f1 + f2) if f1 + f2 != a else pi_frac(redarg(a + 1))],
                  'Arguments add; then adjust into the range.')
    a = redarg(f1 - f2)
    return MC(r, f'z = {eit(m1, f1)} and w = {eit(m2, f2)}. Find z/w in exponential form.', eit(Fr(m1, m2), a),
              [eit(m1 * m2, a), eit(Fr(m1, m2), redarg(f1 + f2)), eit(m1 + m2, a)], 'Divide moduli, subtract arguments.')


@c113.add('C2', (1, 2, 3, 4), 'explain')
def c113_err(r, D):
    nm = person(r)
    m1, m2 = r.choice([2, 3, 4, 5]), r.choice([2, 3, 4, 6])
    f1, f2 = r.choice(SPEC_ARG), r.choice(SPEC_ARG)
    f = r.choice(['add', 'range', 'power'])
    if f == 'add':
        return Q(f'{nm} says that if z = {eit(m1, f1)} and w = {eit(m2, f2)}, then zw = {eit(m1 + m2, redarg(f1 + f2))}. Explain the error.',
                 f'Moduli multiply rather than add: zw = {eit(m1 * m2, redarg(f1 + f2))}.', 'B1 moduli multiply; B1 correct product')
    if f == 'range':
        s = f1 + f2
        if -1 < s <= 1:
            return None
        return Q(f'{nm} gives arg(zw) = {pi_frac(s)} for arg z = {pi_frac(f1)} and arg w = {pi_frac(f2)}. Explain why this is not the principal argument and correct it.',
                 f'{pi_frac(s)} is outside −π < θ ≤ π; subtract or add 2π to obtain {pi_frac(redarg(s))}.', 'B1 outside the range; B1 corrected value')
    n = r.choice([2, 3, 4])
    return Q(f'Given z = {eit(m1, f1)}, explain how to find zⁿ for n = {n} without expanding brackets, and give the answer in exponential form.',
             f'Raise the modulus to the power {n} and multiply the argument by {n}: z{sup(n)} = {eit(m1 ** n, redarg(n * f1))}.', 'B1 method; B1 answer with argument in range')


@c113.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c113_calc(r, D):
    p, q = polar_z(r), polar_z(r)
    if D <= 2:
        a = redarg(p['f'] + q['f'])
        return Q(f'Given z = {p["pol"]} and w = {q["pol"]}, find zw in the form r(cos θ + i sin θ) with −π < θ ≤ π.', polt(p['mod'] * q['mod'], a), 'M1 multiplies moduli; M1 adds arguments; A1 in range')
    if D == 3:
        a = redarg(p['f'] - q['f'])
        mm = Fr(p['mod'], q['mod'])
        return Q(f'Given z = {p["exp"]} and w = {q["exp"]}, find z/w in exponential form re^(iθ) with −π < θ ≤ π.', eit(mm, a), 'M1 divides moduli; M1 subtracts arguments; A1 answer')
    a = redarg(p['f'] + q['f'])
    prod = p['z'] * q['z']
    w = polar_z(r, p['mod'] * q['mod'], a) if ((a * 6).denominator == 1 or (a * 4).denominator == 1) else None
    if not w:
        return None
    if not ok(abs(w['z'] - prod), 0, 'c113 product', 1e-9):
        return None
    return Q(f'Given z = {p["zt"]} and w = {q["zt"]}, find the modulus and argument of z and of w, and hence find zw in the form x + iy, giving exact values.',
             f'|z| = {p["mod"]}, arg z = {pi_frac(p["f"])}; |w| = {q["mod"]}, arg w = {pi_frac(q["f"])}; zw = {w["zt"]}', 'B1 z; B1 w; M1 multiplies moduli and adds arguments; A1 zw')


C113_PAIRS = [((1, 3), (1, 1)), ((1, 3), (1, -1)), ((3, 1), (1, 1)), ((1, 1), (3, -1)), ((3, 1), (1, -1)), ((1, 3), (3, -1))]


def c113_c4(r, D):
    # z = 1 + i√3 type and w = 1 + i: deduce exact trig values of the sum
    (zr, zk), (wr, wk) = r.choice([((Fr(1), Fr(1, 3)), (Fr(1), Fr(1, 4))), ((Fr(1), Fr(1, 6)), (Fr(1), Fr(1, 4))), ((Fr(1), Fr(1, 3)), (Fr(1), Fr(-1, 4))), ((Fr(1), Fr(1, 6)), (Fr(1), Fr(-1, 4)))])
    m1, m2 = r.choice([1, 2]), 1
    p = polar_z(r, 2 * m1, zk)
    q = polar_z(r, 1, wk)
    q_ = complex(round(q['z'].real * math.sqrt(2)), round(q['z'].imag * math.sqrt(2)))
    qt = cs(q_)
    a = zk + wk
    prod = p['z'] * q_
    # exact parts of the product: p = (2m1)(cos + i sin); for these pairs z = m1(1 + i√3) or m1(√3 + i)
    zr_, zi_ = p['z'].real, p['z'].imag
    wr_, wi_ = q_.real, q_.imag
    re_v, im_v = zr_ * wr_ - zi_ * wi_, zr_ * wi_ + zi_ * wr_
    # text: product is m1[(c1 ∓ c2√3)] etc; build from integer combinations of 1 and √3
    def lin3(v):
        a3 = round(v / math.sqrt(3)) if False else None
        for a_ in range(-12, 13):
            for b_ in range(-12, 13):
                if abs(a_ + b_ * math.sqrt(3) - v) < 1e-9:
                    return a_, b_
        return None
    rp, ip = lin3(re_v), lin3(im_v)
    if not rp or not ip:
        return None

    def t3(ab):
        a_, b_ = ab
        if b_ == 0:
            return num(a_)
        bt = ('' if abs(b_) == 1 else str(abs(b_))) + '√3'
        if a_ == 0:
            return ('−' if b_ < 0 else '') + bt
        return f'{a_} {"−" if b_ < 0 else "+"} {bt}'
    zw = f'({t3(rp)}) + ({t3(ip)})i'
    mod = 2 * m1 * math.sqrt(2)
    cosv = re_v / mod
    if not ok(cosv, math.cos(float(a) * math.pi), 'c113 cos', 1e-9):
        return None
    intro = f'The complex numbers z and w are given by z = {p["zt"]} and w = {qt}.'
    parts = [
        P('Find the modulus and argument of each of z and w.', f'|z| = {2 * m1}, arg z = {pi_frac(zk)}; |w| = √2, arg w = {pi_frac(wk)}', 'B1 z; B1 w'),
        P('Find zw in the form x + iy, where x and y are exact.', zw, 'M1 expands; A1 answer'),
        P('State the modulus and argument of zw.', f'|zw| = {2 * m1}√2, arg zw = {pi_frac(a)}', 'B1 modulus; B1 argument'),
        P(f'Deduce the exact value of cos({pi_frac(a)}).', f'({t3(rp)})/({2 * m1}√2)', 'M1 equates real part to |zw| cos(arg); A1 exact value'),
    ]
    return cmp_(r, intro, parts)


c113.add('C4', (2, 3, 4, 5))(c113_c4)


# ---------------------------------------------------------------- 11.4 loci

def circ_case(r):
    a, b = r.randint(-5, 5), r.randint(-5, 5)
    rad = r.randint(1, 5)
    return a, b, rad


def zminus(a, b):
    """'z − (a + bi)' simplified: z − 3 + 2i style."""
    out = 'z'
    if a:
        out += f' − {num(a)}' if a > 0 else f' + {num(-a)}'
    if b:
        bi = ('' if abs(b) == 1 else num(abs(b))) + 'i'
        out += f' − {bi}' if b > 0 else f' + {bi}'
    return out


c114 = T('Loci in the Argand diagram', 'loci', 'argand diagram loci')
c114.fixed('C1', (1, 2), [
    ('What is the locus of z satisfying |z − 2i| = 3?', 'a circle with centre (0, 2) and radius 3', '|z − a| = r is a circle centre a, radius r.', ['a circle with centre (0, −2) and radius 3', 'a circle with centre (2, 0) and radius 3', 'a straight line']),
    ('What is the locus of z satisfying |z − 1| = |z + i|?', 'the perpendicular bisector of the points 1 and −i', 'Equal distances from two fixed points.', ['a circle through 1 and −i', 'the line through 1 and −i', 'a half-line from 1']),
    ('What is the locus of z satisfying arg(z − 2) = π/4?', 'a half-line from (2, 0) at angle π/4 to the positive real axis', 'arg(z − a) = θ is a half-line starting at a, excluding a.', ['a full line through (2, 0)', 'a circle centre (2, 0)', 'a half-line from the origin']),
])
c114.fixed('C2', (2, 3), [
    ('Explain why the point z = 2 itself is not on the locus arg(z − 2) = π/3.', 'At z = 2, z − 2 = 0 and the argument of 0 is undefined, so the half-line starts at 2 but excludes it.', 'B1 z − 2 = 0; B1 argument of 0 undefined [2]'),
])


@c114.add('C1', (1, 2, 3))
def c114_c1(r, D):
    a, b, rad = circ_case(r)
    if D <= 2:
        return MC(r, f'The locus of z is given by |{zminus(a, b)}| = {rad}. State the centre and radius.', f'centre ({num(a)}, {num(b)}), radius {rad}',
                  [f'centre ({num(-a)}, {num(-b)}), radius {rad}', f'centre ({num(a)}, {num(b)}), radius {rad * rad}', f'centre ({num(b)}, {num(a)}), radius {rad}' if a != b else f'centre ({num(a)}, {num(-b)}), radius {rad}'],
                  '|z − (a + bi)| = r: centre (a, b), radius r.')
    m2 = a * a + b * b
    if m2 == 0:
        return None
    big = math.sqrt(m2) + rad
    return MC(r, f'z lies on the circle |{zminus(a, b)}| = {rad}. Find the greatest value of |z|.', n3(big), [n3(abs(math.sqrt(m2) - rad)), n3(math.sqrt(m2)), n3(m2 + rad)], 'Greatest |z| = distance of centre from O + radius.')


@c114.add('C2', (1, 2, 3, 4), 'explain')
def c114_err(r, D):
    nm = person(r)
    a, b, rad = circ_case(r)
    if a == 0 and b == 0:
        return None
    f = r.choice(['centre', 'least', 'bisect'])
    if f == 'centre':
        return Q(f'{nm} says that |{zminus(a, b)}| = {rad} is a circle with centre ({num(-a)}, {num(-b)}). Explain the error.',
                 f'|z − w| is the distance from w; here w = {cstr(a, b)}, so the centre is ({num(a)}, {num(b)}), radius {rad}.', 'B1 writes in the form |z − w|; B1 correct centre')
    if f == 'least':
        d = math.hypot(a, b)
        if d <= rad:
            return None
        return Q(f'Explain why the least value of |z| for points on the circle |{zminus(a, b)}| = {rad} is {n3(d - rad)}.',
                 f'The nearest point of the circle to O lies on the line from O to the centre; its distance is |centre| − radius = √{a * a + b * b} − {rad} = {n3(d - rad)}.', 'B1 nearest point on the line through O and the centre; B1 distance − radius')
    c, d = r.randint(-5, 5), r.randint(-5, 5)
    if (c, d) == (a, b):
        return None
    return Q(f'Explain why the locus |{zminus(a, b)}| = |{zminus(c, d)}| is a straight line, and describe it.',
             f'It is the set of points equidistant from ({num(a)}, {num(b)}) and ({num(c)}, {num(d)}): their perpendicular bisector.', 'B1 equidistant from two fixed points; B1 perpendicular bisector')


@c114.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c114_calc(r, D):
    a, b, rad = circ_case(r)
    if D <= 2:
        c, d = r.randint(-5, 5), r.randint(-5, 5)
        if (c, d) == (a, b):
            return None
        # |z − A|² = |z − B|²: −2ax − 2by + a² + b² = −2cx − 2dy + c² + d²
        A_, B_, C_ = 2 * (c - a), 2 * (d - b), (c * c + d * d) - (a * a + b * b)
        g = math.gcd(math.gcd(abs(A_), abs(B_)), abs(C_))
        A_, B_, C_ = A_ // g, B_ // g, C_ // g
        if A_ < 0 or (A_ == 0 and B_ < 0):
            A_, B_, C_ = -A_, -B_, -C_
        eq = poly([(A_, 1)], 'x') if A_ else ''
        lhs = (eq + (term(B_, 1, 'y', first=not eq) if B_ else '')).strip()
        return Q(f'Find the Cartesian equation of the locus |{zminus(a, b)}| = |{zminus(c, d)}|, in the form px + qy = r.', f'{lhs} = {num(C_)}', 'M1 writes z = x + iy and squares; M1 expands and simplifies; A1 equation')
    d0 = math.hypot(a, b)
    if D == 3:
        if d0 == 0:
            return None
        return Q(f'The complex number z satisfies |{zminus(a, b)}| = {rad}. Find the greatest and least possible values of |z|.', f'greatest {n3(d0 + rad)}, least {n3(abs(d0 - rad))}', 'M1 distance of centre from O; A1 greatest; A1 least')
    if d0 <= rad or d0 == 0:
        return None
    th = math.atan2(b, a)
    da = math.asin(rad / d0)
    mx, mn = th + da, th - da
    if not (-math.pi < mn and mx <= math.pi):
        return None
    return Q(f'The complex number z satisfies |{zminus(a, b)}| = {rad}. Find the greatest and least values of arg z, in radians to 3 significant figures.', f'greatest {n3(mx)}, least {n3(mn)}',
             'M1 tangents from O; M1 sin⁻¹(r/d); A1 greatest; A1 least')


def c114_c4(r, D):
    a, b, rad = circ_case(r)
    d0 = math.hypot(a, b)
    if d0 <= rad:
        return None
    k = r.choice([Fr(1, 4), Fr(1, 3), Fr(1, 6), Fr(-1, 4), Fr(3, 4), Fr(2, 3)])
    intro = f'The complex number z satisfies |{zminus(a, b)}| ≤ {rad}.'
    parts = [
        P('Describe the region in which z lies.', f'the inside and boundary of the circle with centre ({num(a)}, {num(b)}) and radius {rad}', 'B1 circle; B1 centre and radius; B1 region inside'),
        P('Find the greatest value of |z|.', n3(d0 + rad), 'M1 |centre| + r; A1 value'),
        P('Find the least value of |z|.', n3(d0 - rad), 'M1 |centre| − r; A1 value'),
        P('Find the greatest value of arg z for points in the region, in radians to 3 significant figures.', n3(math.atan2(b, a) + math.asin(rad / d0)), 'M1 tangent from O; A1 value') if math.atan2(b, a) + math.asin(rad / d0) <= math.pi else None,
    ]
    return cmp_(r, intro, [p for p in parts if p])


c114.add('C4', (2, 3, 4, 5))(c114_c4)


# ---------------------------------------------------------------- 11.5 roots of polynomials and square roots

c115 = T('Complex roots of polynomial equations and square roots of complex numbers', 'complex roots', 'square roots of complex numbers', 'conjugate roots')
c115.fixed('C1', (1, 2), [
    ('A polynomial with real coefficients has 2 + 3i as a root. Which other number must be a root?', '2 − 3i', 'Non-real roots of real polynomials occur in conjugate pairs.', ['−2 + 3i', '−2 − 3i', '3 + 2i']),
    ('What are the roots of z² + 9 = 0?', '3i and −3i', 'z² = −9.', ['3 and −3', '9i and −9i', '3i only']),
    ('How many roots (counted with multiplicity) does a cubic equation have in the complex numbers?', '3', 'A polynomial of degree n has n complex roots.', ['1', '2', 'at most 2']),
])
c115.fixed('C2', (2, 3), [
    ('Explain why a cubic equation with real coefficients must have at least one real root.', 'Non-real roots come in conjugate pairs, so the number of non-real roots is even; with 3 roots in total, at least one must be real.', 'B1 conjugate pairs; B1 odd degree so a real root [2]'),
])


def sqrt_case(r):
    x, y = nz(r, -6, 6), nz(r, -6, 6)
    return x, y, x * x - y * y, 2 * x * y


def cubic_case(r):
    p, q = r.randint(-3, 3), r.randint(1, 4)
    c = nz(r, -4, 4)
    # (z² − 2pz + p² + q²)(z − c)
    Q2 = [1, -2 * p, p * p + q * q]
    cub = pmul(Q2, [1, -c])
    return p, q, c, Q2, cub


@c115.add('C1', (1, 2, 3))
def c115_c1(r, D):
    if D == 1:
        p, q = r.randint(-4, 4), r.randint(1, 5)
        return MC(r, f'The equation z² + bz + c = 0, with b and c real, has a root {cstr(p, q)}. What is the other root?', cstr(p, -q), [cstr(-p, q), cstr(-p, -q), cstr(q, p) if q != p else cstr(p, 2 * q)], 'Conjugate root theorem.')
    if D == 2:
        p, q = r.randint(-4, 4), r.randint(1, 5)
        return MC(r, f'Which quadratic equation with real coefficients has roots {cstr(p, q)} and {cstr(p, -q)}?', f'z² {"−" if 2 * p >= 0 else "+"} {abs(2 * p)}z + {p * p + q * q} = 0'.replace(' − 0z', '').replace(' + 0z', ''),
                  [f'z² {"+" if 2 * p >= 0 else "−"} {abs(2 * p)}z + {p * p + q * q} = 0'.replace(' + 0z', '').replace(' − 0z', '') if p else f'z² − {q * q} = 0',
                   f'z² {"−" if 2 * p >= 0 else "+"} {abs(2 * p)}z + {p * p - q * q} = 0'.replace(' − 0z', '').replace(' + 0z', ''),
                   f'z² {"−" if p >= 0 else "+"} {abs(p)}z + {p * p + q * q} = 0'.replace(' − 0z', '').replace(' + 0z', '') if p else f'z² + {q} = 0'], 'Sum of roots 2p, product p² + q².')
    x, y, a, b = sqrt_case(r)
    return MC(r, f'Which of the following is a square root of {cstr(a, b)}?', cstr(x, y), [cstr(x, -y), cstr(y, x) if abs(y) != abs(x) else cstr(x + 1, y), cstr(a / 2 if a % 2 == 0 else a, b // 2 if b % 2 == 0 else b)], f'({cstr(x, y)})² = {cstr(a, b)}.')


@c115.add('C2', (1, 2, 3, 4), 'explain')
def c115_err(r, D):
    nm = person(r)
    f = r.choice(['conj', 'sqrt', 'show'])
    if f == 'conj':
        p, q = r.randint(-4, 4), r.randint(1, 5)
        return Q(f'{nm} says that a cubic equation with real coefficients could have roots {cstr(p, q)}, {cstr(-p, q) if p else cstr(1, q)} and 2. Explain why this is impossible.',
                 f'Non-real roots of a polynomial with real coefficients occur in conjugate pairs, so {cstr(p, -q)} would also have to be a root, giving more than 3 roots (or the roots listed cannot all occur).', 'B1 conjugate pairs; B1 conclusion')
    if f == 'sqrt':
        x, y, a, b = sqrt_case(r)
        return Q(f'{nm} finds one square root of {cstr(a, b)} to be {cstr(x, y)} and says the other square root is {cstr(x, -y)}. Explain the error.',
                 f'The two square roots are negatives of each other: {cstr(x, y)} and {cstr(-x, -y)}; ({cstr(x, -y)})² = {cstr(a, -b)}.', 'B1 square roots are ±w; B1 shows the conjugate does not work')
    p, q, c, Q2, cub = cubic_case(r)
    return Q(f'Show that z = {cstr(p, q)} is a root of {pstr(cub, "z")} = 0.', f'Substituting gives 0 (or z² {"−" if 2 * p >= 0 else "+"} {abs(2 * p)}z + {p * p + q * q} is a factor).'.replace(' − 0z', '').replace(' + 0z', ''), 'M1 substitutes and expands; A1 shows equal to 0')


@c115.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c115_calc(r, D):
    if D <= 2:
        x, y, a, b = sqrt_case(r)
        return Q(f'Find the square roots of {cstr(a, b)}, giving your answers in the form x + iy.', f'{cstr(x, y)} and {cstr(-x, -y)}', 'M1 (x + iy)² = given; M1 equates parts; A1 both roots')
    p, q, c, Q2, cub = cubic_case(r)
    if D == 3:
        return Q(f'Given that {cstr(p, q)} is a root of {pstr(cub, "z")} = 0, find the other two roots.', f'{cstr(p, -q)} and {num(c)}', 'B1 conjugate root; M1 quadratic factor; M1 divides; A1 real root')
    if D == 4:
        # unknown coefficients
        a1, a0 = cub[2], cub[3]
        return Q(f'The equation {poly([(1, 3), (cub[1], 2)], "z")} + az + b = 0, where a and b are real, has a root {cstr(p, q)}. Find a and b, and the third root.',
                 f'a = {num(a1)}, b = {num(a0)}; third root {num(c)}', 'B1 conjugate root; M1 quadratic factor; M1 compares coefficients; A1 a and b; A1 third root')
    # quartic: two conjugate pairs
    p2, q2 = r.randint(-3, 3), r.randint(1, 3)
    if (p2, q2) == (p, q):
        return None
    quart = pmul(Q2, [1, -2 * p2, p2 * p2 + q2 * q2])
    return Q(f'Given that {cstr(p, q)} is a root of {pstr(quart, "z")} = 0, find the other three roots.', f'{cstr(p, -q)}, {cstr(p2, q2)} and {cstr(p2, -q2)}', 'B1 conjugate; M1 quadratic factor; M1 division; M1 solves the other quadratic; A1 roots')


def c115_c4(r, D):
    p, q, c, Q2, cub = cubic_case(r)
    intro = f'The polynomial p(z) is given by p(z) = {pstr(cub, "z")}.'
    parts = [
        P(f'Show that {cstr(p, q)} is a root of p(z) = 0.', 'substitution gives 0', 'M1 substitutes; A1 shown'),
        P('Find the other two roots of p(z) = 0.', f'{cstr(p, -q)} and {num(c)}', 'B1 conjugate; M1 quadratic factor; A1 real root'),
        P('Find the modulus and argument of the root with positive imaginary part, giving the argument in radians to 3 significant figures.', f'{sqrt_str(p * p + q * q)}, {n3(math.atan2(q, p))}', 'B1 modulus; B1 argument'),
        P(f'Find the square roots of ({cstr(p, q)})².', f'{cstr(p, q)} and {cstr(-p, -q)}', 'B1 both'),
    ]
    return cmp_(r, intro, parts)


c115.add('C4', (2, 3, 4, 5))(c115_c4)

CHAPTERS[11] = [c111, c112, c113, c114, c115]


# ================================================================ Mechanics helpers (g = 10 m s⁻²)

def u3(x):
    """Exact if (nearly) an integer or a short decimal, else 3 s.f."""
    if isinstance(x, Fr):
        x = float(x)
    if abs(x - round(x)) < 1e-9:
        return num(int(round(x)))
    if abs(x * 10 - round(x * 10)) < 1e-9 and abs(x) < 1000:
        return num(round(x, 1))
    if abs(x * 100 - round(x * 100)) < 1e-9 and abs(x) < 100:
        return num(round(x, 2))
    return n3(x * (1 + 1e-12))


MS, MS2 = 'm s⁻¹', 'm s⁻²'
BODIES = ['a car', 'a van', 'a train', 'a particle P', 'a lorry', 'a tram', 'a motorcyclist', 'a bus']
FALLERS = ['a ball', 'a stone', 'a particle', 'a small package', 'a pebble']


def body(r):
    return r.choice(BODIES)


def cap(s):
    return s[:1].upper() + s[1:]


# ================================================================ Chapter 12 Kinematics

def vt_case(r, D):
    """Trapezium (or triangle) velocity-time graph: accelerate u→V over t1, constant for t2, decelerate to 0 over t3."""
    V = r.choice([8, 10, 12, 15, 16, 20, 24, 25, 30])
    t1 = r.choice([4, 5, 6, 8, 10, 12, 15, 20])
    t2 = r.choice([0, 10, 20, 30, 40, 60]) if D >= 2 else r.choice([10, 20, 30])
    t3 = r.choice([4, 5, 6, 8, 10, 16, 20])
    u = 0 if D <= 3 else r.choice([0, 2, 4, 5])
    if u >= V:
        u = 0
    a1 = Fr(V - u, t1)
    a3 = Fr(-V, t3)
    dist = Fr(u + V, 2) * t1 + V * t2 + Fr(V, 2) * t3
    T_ = t1 + t2 + t3
    return dict(V=V, t1=t1, t2=t2, t3=t3, u=u, a1=a1, a3=a3, dist=dist, T=T_, b=body(r))


k121 = T('Displacement, velocity and acceleration and displacement-time and velocity-time graphs', 'velocity-time graphs', 'displacement-time graphs', 'displacement, velocity and acceleration')
k121.fixed('C1', (1, 2), [
    ('What does the gradient of a velocity-time graph represent?', 'acceleration', 'Acceleration is the rate of change of velocity.', ['displacement', 'distance travelled', 'speed']),
    ('What does the area under a velocity-time graph represent?', 'displacement', 'Area = ∫ v dt.', ['acceleration', 'average velocity', 'time taken']),
    ('What does a horizontal line on a displacement-time graph show?', 'the object is at rest', 'Zero gradient means zero velocity.', ['constant velocity', 'constant acceleration', 'the object is at the origin']),
])
k121.fixed('C2', (2, 3), [
    ('Explain the difference between distance travelled and displacement for a particle that moves 5 m forwards and then 3 m backwards.', 'Distance travelled is the total length of path, 8 m; displacement is the change in position, 2 m forwards.', 'B1 distance 8 m; B1 displacement 2 m [2]'),
    ('Explain why areas below the time axis on a velocity-time graph count as negative displacement.', 'Below the axis the velocity is negative, so the particle moves in the negative direction; the displacement for that interval is negative, though distance travelled counts it as positive.', 'B1 negative velocity; B1 displacement negative but distance positive [2]'),
])


@k121.add('C1', (1, 2, 3))
def k121_c1(r, D):
    d = vt_case(r, D)
    if D == 1:
        return MC(r, f'{cap(d["b"])} accelerates uniformly from rest to {d["V"]} {MS} in {d["t1"]} s. Find its acceleration.', f'{u3(d["a1"])} {MS2}',
                  [f'{u3(d["V"] * d["t1"])} {MS2}', f'{u3(Fr(d["t1"], d["V"]))} {MS2}', f'{u3(Fr(d["V"] * d["t1"], 2))} {MS2}', f'{u3(d["a1"] * 2)} {MS2}'], 'a = (v − u)/t.')
    if D == 2:
        s = Fr(d['V'], 2) * d['t1']
        return MC(r, f'A velocity-time graph for {d["b"]} is a straight line from (0, 0) to ({d["t1"]}, {d["V"]}). Find the distance travelled in this time.', f'{u3(s)} m',
                  [f'{u3(d["V"] * d["t1"])} m', f'{u3(d["a1"])} m', f'{u3(s / 2)} m', f'{u3(s + d["V"])} m'], 'Area of the triangle = (1/2) × base × height.')
    return MC(r, f'{cap(d["b"])} travels at a constant {d["V"]} {MS} for {d["t2"] or 10} s and then decelerates uniformly to rest in {d["t3"]} s. Find the deceleration.', f'{u3(-d["a3"])} {MS2}',
              [f'{u3(d["V"] * d["t3"])} {MS2}', f'{u3(Fr(d["t3"], d["V"]))} {MS2}', f'{u3(Fr(d["V"], (d["t2"] or 10) + d["t3"]))} {MS2}', f'{u3(-d["a3"] * 2)} {MS2}'], 'Deceleration = V/t₃.')


@k121.add('C2', (1, 2, 3, 4), 'explain')
def k121_err(r, D):
    nm = person(r)
    d = vt_case(r, D)
    f = r.choice(['gradarea', 'avg', 'neg'])
    if f == 'gradarea':
        return Q(f'{cap(d["b"])} accelerates uniformly from rest to {d["V"]} {MS} in {d["t1"]} s. {nm} says the distance travelled is {d["V"]} × {d["t1"]} = {d["V"] * d["t1"]} m. Explain the error and find the correct distance.',
                 f'The speed is not {d["V"]} {MS} throughout; distance is the area under the graph, a triangle: (1/2) × {d["t1"]} × {d["V"]} = {u3(Fr(d["V"] * d["t1"], 2))} m.', 'B1 area of the triangle, not rectangle; B1 correct distance')
    if f == 'avg':
        avg = d['dist'] / d['T']
        return Q(f'{cap(d["b"])} accelerates from rest to {d["V"]} {MS} in {d["t1"]} s, travels at {d["V"]} {MS} for {d["t2"]} s and decelerates to rest in {d["t3"]} s. {nm} says its average speed is {u3(Fr(d["V"], 2))} {MS}. Explain why this is wrong and find the average speed.',
                 f'Average speed = total distance ÷ total time = {u3(d["dist"])} ÷ {d["T"]} = {u3(avg)} {MS}, not the mean of the speeds.', 'B1 total distance ÷ total time; B1 correct value')
    v1, v2 = r.randint(3, 10), r.randint(2, 8)
    t1, t2 = r.randint(2, 6), r.randint(2, 6)
    return Q(f'A particle moves with velocity {v1} {MS} for {t1} s and then with velocity −{v2} {MS} for {t2} s. {nm} says its displacement and distance travelled are both {v1 * t1 + v2 * t2} m. Explain the error.',
             f'Distance travelled = {v1 * t1} + {v2 * t2} = {v1 * t1 + v2 * t2} m, but displacement = {v1 * t1} − {v2 * t2} = {v1 * t1 - v2 * t2} m because the second motion is in the opposite direction.', 'B1 distance correct; B1 displacement subtracts')


@k121.add('C3', (1, 2, 3, 4, 5), 'numerical')
def k121_calc(r, D):
    d = vt_case(r, D)
    stem = f'{cap(d["b"])} starts {"from rest" if d["u"] == 0 else "with speed " + str(d["u"]) + " " + MS} and accelerates uniformly to {d["V"]} {MS} in {d["t1"]} s'
    stem += f', travels at this speed for {d["t2"]} s' if d['t2'] else ''
    stem += f' and then decelerates uniformly to rest in {d["t3"]} s.'
    if D <= 2:
        return Q(stem + ' Find the total distance travelled.', f'{u3(d["dist"])} m', 'M1 area under the velocity-time graph; A1 distance')
    if D == 3:
        return Q(stem + ' Find the acceleration in the first stage and the total distance travelled.', f'{u3(d["a1"])} {MS2}; {u3(d["dist"])} m', 'B1 acceleration; M1 area; A1 distance')
    if D == 4:
        # find t2 given total distance
        if not d['t2']:
            return None
        s0 = d['dist']
        st = f'{cap(d["b"])} starts {"from rest" if d["u"] == 0 else "with speed " + str(d["u"]) + " " + MS} and accelerates uniformly to {d["V"]} {MS} in {d["t1"]} s, travels at this speed for T s and then decelerates uniformly to rest in {d["t3"]} s. The total distance is {u3(s0)} m.'
        return Q(st + ' Find T.', f'T = {d["t2"]}', 'M1 area expression in T; A1 equation; A1 T')
    if not d['t2']:
        return None
    # time to cover half the distance
    half = d['dist'] / 2
    s1 = Fr(d['u'] + d['V'], 2) * d['t1']
    if half <= s1 or half > s1 + d['V'] * d['t2']:
        return None
    th = d['t1'] + (half - s1) / d['V']
    return Q(stem + ' Find the time taken to travel half of the total distance.', f'{u3(th)} s', 'M1 total distance; M1 first-stage distance; M1 constant-speed stage; A1 time')


def k121_c4(r, D):
    d = vt_case(r, max(2, D))
    if not d['t2']:
        return None
    intro = f'{cap(d["b"])} starts {"from rest" if d["u"] == 0 else "with speed " + str(d["u"]) + " " + MS} and accelerates uniformly to {d["V"]} {MS} in {d["t1"]} s. It travels at this speed for {d["t2"]} s and then decelerates uniformly to rest in {d["t3"]} s.'
    parts = [
        P('Sketch the velocity-time graph and state its main features.', f'trapezium: rises to {d["V"]} at t = {d["t1"]}, constant to t = {d["t1"] + d["t2"]}, falls to 0 at t = {d["T"]}', 'B1 shape; B1 values marked'),
        P('Find the acceleration and the deceleration.', f'{u3(d["a1"])} {MS2} and {u3(-d["a3"])} {MS2}', 'B1 B1'),
        P('Find the total distance travelled.', f'{u3(d["dist"])} m', 'M1 area; A1 distance'),
        P('Find the average speed for the whole journey.', f'{u3(d["dist"] / d["T"])} {MS}', 'M1 distance ÷ time; A1 value'),
    ]
    return cmp_(r, intro, parts)


k121.add('C4', (2, 3, 4, 5))(k121_c4)


# ---------------------------------------------------------------- 12.2 suvat

def suvat(r, D):
    u = r.choice([0, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20])
    a = r.choice([Fr(1, 2), 1, Fr(3, 2), 2, Fr(5, 2), 3, 4, -1, -2, Fr(-1, 2), Fr(-5, 2)])
    t = r.choice([2, 3, 4, 5, 6, 8, 10])
    v = u + a * t
    if v < 0:
        return None
    s = u * t + Fr(1, 2) * a * t * t
    if not ok(float(v * v), float(u * u + 2 * a * s), 'suvat'):
        return None
    return dict(u=Fr(u), a=Fr(a), t=Fr(t), v=v, s=s, b=body(r))


k122 = T('Constant acceleration equations (suvat)', 'suvat', 'constant acceleration')
k122.fixed('C1', (1, 2), [
    ('Which equation does not involve the time t?', 'v² = u² + 2as', 'The other suvat equations contain t.', ['v = u + at', 's = ut + (1/2)at²', 's = (1/2)(u + v)t']),
    ('Which equation does not involve the acceleration a?', 's = (1/2)(u + v)t', 'It uses the average of u and v.', ['v = u + at', 'v² = u² + 2as', 's = vt − (1/2)at²']),
])
k122.fixed('C2', (2, 3), [
    ('Explain why the suvat equations cannot be used when the acceleration varies with time.', 'They are derived assuming a is constant (straight-line velocity-time graph); with variable acceleration calculus must be used instead.', 'B1 derived for constant a; B1 use calculus otherwise [2]'),
])


@k122.add('C1', (1, 2, 3))
def k122_c1(r, D):
    d = suvat(r, D)
    if not d:
        return None
    if D == 1:
        return MC(r, f'{cap(d["b"])} {"starts from rest" if d["u"] == 0 else "has initial speed " + u3(d["u"]) + " " + MS} and constant acceleration {u3(d["a"])} {MS2}. Find its speed after {u3(d["t"])} s.', f'{u3(d["v"])} {MS}',
                  [f'{u3(d["u"] + d["a"])} {MS}', f'{u3(d["a"] * d["t"])} {MS}', f'{u3(d["u"] * d["a"] * d["t"])} {MS}', f'{u3(d["v"] + d["a"])} {MS}'], 'v = u + at.')
    if D == 2:
        return MC(r, f'{cap(d["b"])} {"starts from rest" if d["u"] == 0 else "has initial speed " + u3(d["u"]) + " " + MS} and constant acceleration {u3(d["a"])} {MS2}. Find the distance travelled in {u3(d["t"])} s.', f'{u3(d["s"])} m',
                  [f'{u3(d["u"] * d["t"] + d["a"] * d["t"] ** 2)} m', f'{u3(d["u"] * d["t"])} m', f'{u3(d["v"] * d["t"])} m', f'{u3(d["s"] + 1)} m'], 's = ut + (1/2)at².')
    if d['a'] == 0 or d['s'] <= 0:
        return None
    return MC(r, f'{cap(d["b"])} accelerates uniformly from {u3(d["u"])} {MS} to {u3(d["v"])} {MS} over a distance of {u3(d["s"])} m. Find the acceleration.', f'{u3(d["a"])} {MS2}',
              [f'{u3((d["v"] - d["u"]) / d["s"])} {MS2}', f'{u3((d["v"] ** 2 + d["u"] ** 2) / (2 * d["s"]))} {MS2}', f'{u3(d["a"] * 2)} {MS2}', f'{u3(d["a"] / 2)} {MS2}'], 'v² = u² + 2as.')


@k122.add('C2', (1, 2, 3, 4), 'explain')
def k122_err(r, D):
    nm = person(r)
    d = suvat(r, D)
    if not d:
        return None
    f = r.choice(['sign', 'half', 'units'])
    if f == 'sign' and d['a'] < 0:
        wrong = d['u'] * d['t'] - Fr(1, 2) * d['a'] * d['t'] ** 2
        return Q(f'{cap(d["b"])} decelerates at {u3(-d["a"])} {MS2} from {u3(d["u"])} {MS}. {nm} uses a = +{u3(-d["a"])} and finds the distance in {u3(d["t"])} s as {u3(wrong)} m. Explain the error and find the correct distance.',
                 f'A deceleration means a = −{u3(-d["a"])} {MS2}; s = ut + (1/2)at² = {u3(d["s"])} m.', 'B1 a negative; B1 correct distance')
    if f == 'half':
        wrong = d['u'] * d['t'] + d['a'] * d['t'] ** 2
        return Q(f'{nm} calculates the distance travelled by {d["b"]} with u = {u3(d["u"])} {MS}, a = {u3(d["a"])} {MS2}, t = {u3(d["t"])} s as s = ut + at² = {u3(wrong)} m. Explain the error and correct it.',
                 f'The formula is s = ut + (1/2)at², giving {u3(d["s"])} m.', 'B1 missing factor 1/2; B1 correct value')
    kmh = r.choice([36, 54, 72, 90, 108])
    return Q(f'{nm} is told that a car moving at {kmh} km h⁻¹ brakes uniformly to rest in {u3(d["t"])} s, and uses u = {kmh} in v = u + at. Explain the error and find the deceleration.',
             f'Speeds must be in m s⁻¹: {kmh} km h⁻¹ = {u3(Fr(kmh, Fr(18, 5)))} {MS}, so the deceleration is {u3(Fr(kmh, Fr(18, 5)) / d["t"])} {MS2}.', 'B1 converts units; B1 correct deceleration')


@k122.add('C3', (1, 2, 3, 4, 5), 'numerical')
def k122_calc(r, D):
    d = suvat(r, D)
    if not d:
        return None
    if D == 1:
        return Q(f'{cap(d["b"])} moves with constant acceleration {u3(d["a"])} {MS2}. {"It starts from rest." if d["u"] == 0 else "Its initial speed is " + u3(d["u"]) + " " + MS + "."} Find its speed after {u3(d["t"])} s and the distance it travels in this time.',
                 f'{u3(d["v"])} {MS}; {u3(d["s"])} m', 'M1 v = u + at; A1 speed; A1 distance')
    if D == 2:
        if d['s'] <= 0 or d['a'] == 0 or d['u'] == 0 or d['v'] == 0:
            return None
        return Q(f'{cap(d["b"])} moving in a straight line with constant acceleration passes a point A with speed {u3(d["u"])} {MS} and a point B, {u3(d["s"])} m further on, with speed {u3(d["v"])} {MS}. Find the acceleration and the time taken from A to B.',
                 f'{u3(d["a"])} {MS2}; {u3(d["t"])} s', 'M1 v² = u² + 2as; A1 acceleration; A1 time')
    if D == 3:
        if d['s'] <= 0 or d['v'] == 0:
            return None
        return Q(f'{cap(d["b"])} travels {u3(d["s"])} m in {u3(d["t"])} s with constant acceleration, reaching a speed of {u3(d["v"])} {MS}. Find its initial speed and its acceleration.',
                 f'u = {u3(d["u"])} {MS}; a = {u3(d["a"])} {MS2}', 'M1 s = (1/2)(u + v)t; A1 u; A1 a')
    # meeting problem: car from rest with acceleration a overtaken by... a vehicle at constant speed V from the same point
    a = r.choice([1, 2, Fr(1, 2), Fr(3, 2), 3])
    V = r.choice([10, 12, 15, 20, 24])
    if D == 4:
        tm = 2 * Fr(V) / a
        return Q(f'A car starts from rest at a point O and accelerates uniformly at {u3(a)} {MS2}. At the same instant a lorry passes O moving at a constant {V} {MS} in the same direction. Find the time at which the car overtakes the lorry and the distance from O at that time.',
                 f'{u3(tm)} s; {u3(V * tm)} m', 'M1 equates displacements; A1 time; A1 distance')
    delay = r.choice([2, 3, 4, 5])
    # car starts delay seconds after lorry passes: (1/2)a t² = V(t + delay)
    A_, B_, C_ = float(a) / 2, -V, -V * delay
    t = (-B_ + math.sqrt(B_ * B_ - 4 * A_ * C_)) / (2 * A_)
    if not ok(0.5 * float(a) * t * t, V * (t + delay), 'meet'):
        return None
    return Q(f'A lorry passes a point O at a constant {V} {MS}. {delay} s later a car starts from rest at O and accelerates uniformly at {u3(a)} {MS2} in the same direction. Find the time the car takes to catch the lorry.',
             f'{n3(t)} s after starting', 'M1 displacement expressions; M1 forms quadratic; A1 solves; A1 time')


def k122_c4(r, D):
    d = suvat(r, D)
    if not d or d['a'] <= 0:
        return None
    t2 = r.choice([10, 15, 20, 30])
    t3 = r.choice([4, 5, 8, 10])
    dec = d['v'] / t3
    s3 = d['v'] * t3 / 2
    tot = d['s'] + d['v'] * t2 + s3
    intro = f'{cap(d["b"])} passes a point A with speed {u3(d["u"])} {MS} and accelerates uniformly at {u3(d["a"])} {MS2} for {u3(d["t"])} s. It then travels at constant speed for {t2} s before decelerating uniformly to rest in {t3} s.'
    parts = [
        P('Find the maximum speed.', f'{u3(d["v"])} {MS}', 'M1 v = u + at; A1 speed'),
        P('Find the distance travelled while accelerating.', f'{u3(d["s"])} m', 'M1 s = ut + (1/2)at²; A1 distance'),
        P('Find the deceleration in the final stage.', f'{u3(dec)} {MS2}', 'B1 value'),
        P('Find the total distance from A to the point where it comes to rest.', f'{u3(tot)} m', 'M1 adds the three stages; A1 total'),
    ]
    return cmp_(r, intro, parts)


k122.add('C4', (2, 3, 4, 5))(k122_c4)


# ---------------------------------------------------------------- 12.3 vertical motion

def vert(r, D):
    u = r.choice([5, 8, 10, 12, 14, 15, 20, 25])
    h = r.choice([0, 0, 5, 10, 15, 20, 25, 30]) if D >= 3 else 0
    H = u * u / (2 * G)
    tt = u / G
    # time to reach ground: h + ut − 5t² = 0
    tg = (u + math.sqrt(u * u + 2 * G * h)) / G
    vg = math.sqrt(u * u + 2 * G * h)
    if not ok(h + u * tg - 0.5 * G * tg * tg, 0, 'vert'):
        return None
    return dict(u=u, h=h, H=H, tt=tt, tg=tg, vg=vg, obj=r.choice(FALLERS))


k123 = T('Vertical motion under gravity', 'vertical motion under gravity', 'projected vertically')
k123.fixed('C1', (1, 2), [
    ('A ball is thrown vertically upwards. What is its acceleration at the highest point (g = 10 m s⁻²)?', '10 m s⁻² downwards', 'Gravity acts throughout; only the velocity is zero there.', ['0', '10 m s⁻² upwards', 'it depends on the initial speed']),
    ('A stone is dropped from rest. How far does it fall in the first 2 s (g = 10 m s⁻²)?', '20 m', 's = (1/2)(10)(2²).', ['10 m', '40 m', '5 m']),
])
k123.fixed('C2', (2, 3), [
    ('Explain why, ignoring air resistance, a ball thrown upwards returns to its starting level with the same speed.', 'Under constant acceleration g the motion is symmetric: v² = u² − 2gs and s = 0 on return gives v² = u², so the speed is the same (direction reversed).', 'B1 v² = u² + 2as with s = 0; B1 same speed, opposite direction [2]'),
])


@k123.add('C1', (1, 2, 3))
def k123_c1(r, D):
    d = vert(r, D)
    if not d:
        return None
    if D == 1:
        return MC(r, f'{cap(d["obj"])} is projected vertically upwards with speed {d["u"]} {MS}. Find the time to reach its highest point.', f'{u3(d["tt"])} s',
                  [f'{u3(d["tt"] * 2)} s', f'{u3(d["u"] * G)} s', f'{u3(d["H"])} s', f'{u3(d["tt"] / 2)} s'], 't = u/g.')
    return MC(r, f'{cap(d["obj"])} is projected vertically upwards with speed {d["u"]} {MS}. Find the greatest height above the point of projection.', f'{u3(d["H"])} m',
              [f'{u3(d["H"] * 2)} m', f'{u3(d["u"] * d["u"] / G)} m', f'{u3(d["u"] / G)} m', f'{u3(d["H"] / 2)} m'], 'v² = u² − 2gs with v = 0.')


@k123.add('C2', (1, 2, 3, 4), 'explain')
def k123_err(r, D):
    nm = person(r)
    d = vert(r, max(3, D))
    if not d:
        return None
    f = r.choice(['sign', 'top', 'both'])
    if f == 'sign':
        wrong = d['u'] * 2 + 0.5 * G * 4
        return Q(f'{cap(d["obj"])} is thrown upwards at {d["u"]} {MS}. {nm} takes a = +10 {MS2} with upwards positive and finds the displacement after 2 s to be {u3(wrong)} m. Explain the error and find the correct displacement.',
                 f'With upwards positive, a = −10 {MS2}: s = {d["u"]}(2) − 5(4) = {u3(d["u"] * 2 - 20)} m.', 'B1 sign of g; B1 correct displacement')
    if f == 'top':
        return Q(f'{nm} says that a {d["obj"].split(" ", 1)[1]} thrown upwards at {d["u"]} {MS} has zero acceleration at its highest point because it is momentarily at rest. Explain why this is wrong.',
                 f'The velocity is zero at the top, but gravity still acts, so the acceleration is 10 {MS2} downwards throughout.', 'B1 velocity zero; B1 acceleration still g downwards')
    s = r.choice([x for x in (5, 10, 15, 20) if x < d['H']] or [None])
    if s is None:
        return None
    t1 = (d['u'] - math.sqrt(d['u'] ** 2 - 2 * G * s)) / G
    t2 = (d['u'] + math.sqrt(d['u'] ** 2 - 2 * G * s)) / G
    return Q(f'{cap(d["obj"])} is projected upwards at {d["u"]} {MS}. Solving {s} = {d["u"]}t − 5t² gives two values of t. Explain why both are valid and find them.',
             f'The particle passes the height {s} m on the way up and again on the way down: t = {n3(t1)} s and t = {n3(t2)} s.', 'B1 passes the height twice; B1 both times')


@k123.add('C3', (1, 2, 3, 4, 5), 'numerical')
def k123_calc(r, D):
    d = vert(r, D)
    if not d:
        return None
    if D <= 2:
        return Q(f'{cap(d["obj"])} is projected vertically upwards from ground level with speed {d["u"]} {MS}. Find the greatest height reached and the total time before it returns to the ground.', f'{u3(d["H"])} m; {u3(2 * d["tt"])} s',
                 'M1 v² = u² − 2gs; A1 height; A1 time')
    if d['h'] == 0:
        return None
    if D == 3:
        return Q(f'{cap(d["obj"])} is projected vertically upwards with speed {d["u"]} {MS} from a point {d["h"]} m above the ground. Find the time taken to reach the ground.', f'{n3(d["tg"])} s',
                 'M1 −' + str(d['h']) + ' = ut − 5t²; M1 solves the quadratic; A1 time')
    if D == 4:
        return Q(f'{cap(d["obj"])} is projected vertically upwards with speed {d["u"]} {MS} from a point {d["h"]} m above the ground. Find the speed with which it hits the ground.', f'{n3(d["vg"])} {MS}',
                 'M1 v² = u² + 2gs with s = ' + str(d['h']) + '; A1 speed')
    s = r.choice([x for x in (5, 10, 15) if x < d['H']] or [None])
    if s is None:
        return None
    dt = 2 * math.sqrt(d['u'] ** 2 - 2 * G * s) / G
    return Q(f'{cap(d["obj"])} is projected vertically upwards with speed {d["u"]} {MS}. Find the length of time for which it is at least {s} m above the point of projection.', f'{n3(dt)} s',
             'M1 sets up the quadratic; M1 solves; A1 difference of roots')


def k123_c4(r, D):
    d = vert(r, max(3, D))
    if not d or d['h'] == 0:
        return None
    intro = f'{cap(d["obj"])} is projected vertically upwards with speed {d["u"]} {MS} from a point A, which is {d["h"]} m above the ground.'
    parts = [
        P('Find the greatest height above the ground reached.', f'{u3(d["h"] + d["H"])} m', 'M1 v² = u² − 2gs; A1 height'),
        P('Find the time taken to reach the ground.', f'{n3(d["tg"])} s', 'M1 quadratic in t; A1 time'),
        P('Find the speed with which it reaches the ground.', f'{n3(d["vg"])} {MS}', 'M1 v² = u² + 2gs; A1 speed'),
        P('Find the time for which it is above A.', f'{u3(2 * d["tt"])} s', 'B1 value'),
    ]
    return cmp_(r, intro, parts)


k123.add('C4', (2, 3, 4, 5))(k123_c4)

CHAPTERS[12] = [k121, k122, k123]


# ================================================================ Chapter 13 Forces and Newton's laws in one dimension

f131 = T('Types of force: weight, normal contact, tension, thrust and friction and force diagrams', 'types of force', 'force diagrams', 'weight', 'normal contact force')
f131.fixed('C1', (1, 2), [
    ('What is the weight of a particle of mass 3 kg (g = 10 m s⁻²)?', '30 N', 'W = mg.', ['3 N', '0.3 N', '13 N']),
    ('In which direction does friction act on a block sliding across a rough floor?', 'opposite to the direction of motion', 'Friction opposes relative motion.', ['in the direction of motion', 'vertically upwards', 'perpendicular to the floor']),
    ('Which force can a light rod exert that a string cannot?', 'thrust', 'A string can only pull (tension); a rod can also push.', ['tension', 'weight', 'normal reaction']),
])
f131.fixed('C2', (2, 3), [
    ('Explain why the normal contact force on a book resting on a table is not the "reaction" to its weight in the sense of Newton\'s third law.', 'The weight is the Earth pulling the book; its third-law pair is the book pulling the Earth. The normal force is the table pushing the book; its pair is the book pushing the table. The two forces on the book balance by the first law.', 'B1 identifies the true pairs; B1 balance is Newton\'s first law [2]'),
    ('Explain what is meant by modelling an object as a particle.', 'Its size is ignored and its mass treated as concentrated at a point, so rotation and air resistance due to shape are neglected.', 'B1 dimensions ignored; B1 mass at a point [2]'),
])


def f131_case(r, D):
    m = r.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20])
    P_ = r.choice([5, 8, 10, 12, 15, 20, 25])
    kind = r.choice(['push', 'pull', 'hang'] if D >= 2 else ['push', 'pull'])
    if kind == 'push':
        R = m * G + P_
        txt = f'A box of mass {m} kg rests on a horizontal floor and a vertical force of {P_} N pushes down on it.'
    elif kind == 'pull':
        if P_ >= m * G:
            return None
        R = m * G - P_
        txt = f'A box of mass {m} kg rests on a horizontal floor and is pulled upwards by a vertical string with tension {P_} N, but does not leave the floor.'
    else:
        m2 = r.choice([1, 2, 3])
        R = (m + m2) * G
        txt = f'A box of mass {m} kg rests on a horizontal floor with a {m2} kg block resting on top of it.'
    return dict(m=m, P=P_, kind=kind, R=R, txt=txt)


@f131.add('C1', (1, 2, 3))
def f131_c1(r, D):
    d = f131_case(r, D)
    if not d:
        return None
    return MC(r, d['txt'] + ' Find the normal contact force from the floor on the box.', f'{u3(d["R"])} N',
              [f'{u3(d["m"] * G)} N', f'{u3(abs(d["m"] * G - (d["R"] - d["m"] * G)))} N' if d['kind'] != 'pull' else f'{u3(d["m"] * G + d["P"])} N', f'{u3(d["m"])} N', f'{u3(d["P"])} N'], 'Resolve vertically: forces balance.')


@f131.add('C2', (1, 2, 3, 4), 'explain')
def f131_err(r, D):
    nm = person(r)
    d = f131_case(r, D)
    if not d:
        return None
    f = r.choice(['Rmg', 'list', 'mass'])
    if f == 'Rmg' and d['kind'] != 'hang':
        return Q(f'{d["txt"]} {nm} says the normal contact force is {u3(d["m"] * G)} N because it always equals the weight. Explain the error and find the correct value.',
                 f'R balances all the other vertical forces, not just the weight: R = {d["m"] * G} {"+" if d["kind"] == "push" else "−"} {d["P"]} = {u3(d["R"])} N.', 'B1 R depends on all vertical forces; B1 correct value')
    if f == 'mass':
        return Q(f'{nm} says that a {d["m"]} kg box has a weight of {d["m"]} kg. Explain the error.', f'Weight is a force, measured in newtons: W = mg = {d["m"] * G} N; {d["m"]} kg is its mass.', 'B1 weight is a force; B1 W = mg value')
    return Q(f'{d["txt"]} List the forces acting on the box and state the direction of each.',
             {'push': f'weight {d["m"] * G} N down; applied force {d["P"]} N down; normal reaction {d["R"]} N up',
              'pull': f'weight {d["m"] * G} N down; tension {d["P"]} N up; normal reaction {d["R"]} N up',
              'hang': f'weight {d["m"] * G} N down; contact force from the block {d["R"] - d["m"] * G} N down; normal reaction {d["R"]} N up'}[d['kind']],
             'B1 all forces; B1 directions and values')


@f131.add('C3', (1, 2, 3, 4, 5), 'numerical')
def f131_calc(r, D):
    if D <= 2:
        d = f131_case(r, D)
        if not d:
            return None
        return Q(d['txt'] + ' Draw a force diagram and find the normal contact force on the box.', f'{u3(d["R"])} N', 'B1 diagram; M1 resolves vertically; A1 R')
    m = r.choice([800, 1000, 1200, 1500, 2000])
    Dv = r.choice([1500, 2000, 2500, 3000, 4000])
    Rv = r.choice([400, 500, 600, 800, 1000])
    if Rv >= Dv:
        return None
    if D == 3:
        return Q(f'A car of mass {m} kg has a driving force of {Dv} N and experiences a resistance of {Rv} N. Find the resultant force on the car and state its direction.', f'{Dv - Rv} N forwards', 'M1 resultant = D − R; A1 value and direction')
    if D == 4:
        T_ = r.choice([20, 30, 40, 50])
        m2 = r.choice([2, 3, 4])
        return Q(f'A particle of mass {m2} kg hangs in equilibrium from two vertical strings; one has tension {T_} N. Find the tension in the other string.', f'{u3(m2 * G - T_)} N' if m2 * G > T_ else 'impossible',
                 'M1 resolves vertically; A1 tension') if m2 * G > T_ else None
    k = r.choice([2, 3, 4])
    mm = r.choice([2, 3, 4, 5])
    return Q(f'{k} identical blocks, each of mass {mm} kg, are stacked on a horizontal table. Find the normal contact force between the bottom block and the table, and between the bottom block and the one above it.',
             f'{u3(k * mm * G)} N; {u3((k - 1) * mm * G)} N', 'M1 whole stack; A1 table force; A1 force between blocks')


def f131_c4(r, D):
    d = f131_case(r, max(2, D))
    if not d:
        return None
    intro = d['txt']
    parts = [
        P('Draw a diagram showing the forces acting on the box.', 'weight, normal reaction and the applied force/contact force shown with directions', 'B1 all forces; B1 directions'),
        P('Find the normal contact force exerted by the floor on the box.', f'{u3(d["R"])} N', 'M1 resolves; A1 value'),
        P('State the force exerted by the box on the floor, giving its direction.', f'{u3(d["R"])} N downwards (Newton\'s third law)', 'B1 value and direction'),
        P('State the mass of the box and its weight.', f'{d["m"]} kg; {d["m"] * G} N', 'B1'),
    ]
    return cmp_(r, intro, parts)


f131.add('C4', (2, 3, 4, 5))(f131_c4)


# ---------------------------------------------------------------- 13.2 F = ma

def fma_case(r, D):
    kind = r.choice(['car', 'smooth', 'lift_rope', 'brake'] if D >= 2 else ['car', 'smooth'])
    if kind == 'car':
        m = r.choice([800, 900, 1000, 1200, 1500])
        Dv = r.choice([1500, 2000, 2400, 3000])
        Rv = r.choice([300, 400, 500, 600, 900])
        a = Fr(Dv - Rv, m)
        txt = f'A car of mass {m} kg moves along a straight horizontal road. The driving force is {Dv} N and the resistance to motion is {Rv} N.'
        return dict(kind=kind, m=m, a=a, txt=txt, F=Dv - Rv, Dv=Dv, Rv=Rv)
    if kind == 'smooth':
        m = r.choice([2, 3, 4, 5, 8])
        P_ = r.choice([6, 10, 12, 15, 20])
        a = Fr(P_, m)
        txt = f'A particle of mass {m} kg is pulled along a smooth horizontal surface by a horizontal force of {P_} N.'
        return dict(kind=kind, m=m, a=a, txt=txt, F=P_)
    if kind == 'lift_rope':
        m = r.choice([5, 10, 20, 50])
        a = r.choice([Fr(1, 2), 1, 2, Fr(3, 2)])
        T_ = m * (G + a)
        txt = f'A load of mass {m} kg is raised vertically by a rope with tension {u3(T_)} N.'
        return dict(kind=kind, m=m, a=Fr(a), txt=txt, F=T_ - m * G, T=T_)
    m = r.choice([1000, 1200, 1500, 2000])
    B_ = r.choice([3000, 4000, 5000, 6000])
    a = Fr(-B_, m)
    u = r.choice([10, 15, 20, 25])
    txt = f'A car of mass {m} kg travelling at {u} {MS} brakes with a constant total braking force of {B_} N.'
    return dict(kind=kind, m=m, a=a, txt=txt, F=-B_, u=u, B=B_)


n132 = T("Newton's second law F = ma in one dimension", "newton's second law", 'f = ma')
n132.fixed('C1', (1, 2), [
    ('A resultant force of 12 N acts on a mass of 4 kg. What is the acceleration?', '3 m s⁻²', 'a = F/m.', ['48 m s⁻²', '0.33 m s⁻²', '16 m s⁻²']),
    ('A particle moves with constant velocity. What is the resultant force on it?', 'zero', "Newton's first law.", ['equal to its weight', 'in the direction of motion', 'equal to mv']),
])
n132.fixed('C2', (2, 3), [
    ('Explain why a car travelling at constant speed on a level road still needs a driving force.', 'Resistances act against the motion; for zero acceleration the resultant force must be zero, so the driving force must equal the resistance.', 'B1 resistance acts; B1 driving force balances it for zero resultant [2]'),
])


@n132.add('C1', (1, 2, 3))
def n132_c1(r, D):
    d = fma_case(r, D)
    if d['kind'] == 'lift_rope':
        return MC(r, d['txt'] + ' Find the acceleration of the load.', f'{u3(d["a"])} {MS2}', [f'{u3(d["T"] / d["m"])} {MS2}', f'{u3(d["a"] + G)} {MS2}', f'{u3(d["a"] * 2)} {MS2}', f'{u3(d["T"] / d["m"] - 2 * G)} {MS2}' if d['T'] / d['m'] - 2 * G > 0 else '0'],
                  'T − mg = ma.')
    return MC(r, d['txt'] + (' Find its deceleration.' if d['kind'] == 'brake' else ' Find the acceleration.'), f'{u3(abs(d["a"]))} {MS2}',
              [f'{u3(abs(d["a"]) * 2)} {MS2}', f'{u3(Fr(d["Dv"] + d["Rv"], d["m"]))} {MS2}' if d['kind'] == 'car' else f'{u3(abs(d["F"]) * d["m"])} {MS2}', f'{u3(Fr(d["m"], abs(d["F"])))} {MS2}', f'{u3(abs(d["a"]) + 1)} {MS2}'],
              'Resultant force = ma.')


@n132.add('C2', (1, 2, 3, 4), 'explain')
def n132_err(r, D):
    nm = person(r)
    d = fma_case(r, D)
    f = r.choice(['resist', 'weight', 'mass'])
    if d['kind'] == 'car' and f == 'resist':
        return Q(f'{d["txt"]} {nm} uses F = ma with F = {d["Dv"]} N. Explain the error and find the correct acceleration.',
                 f'F must be the resultant force, {d["Dv"]} − {d["Rv"]} = {d["F"]} N, so a = {u3(d["a"])} {MS2}.', 'B1 resultant force; B1 correct acceleration')
    if d['kind'] == 'lift_rope' and f == 'weight':
        return Q(f'{d["txt"]} {nm} writes {u3(d["T"])} = {d["m"]}a. Explain the error and find the acceleration.',
                 f'The weight {d["m"] * G} N also acts: T − mg = ma gives a = {u3(d["a"])} {MS2}.', 'B1 weight omitted; B1 correct acceleration')
    return Q(f'{d["txt"]} {nm} says that the acceleration would be the same if the mass were doubled. Explain why this is wrong.',
             f'a = F/m, so doubling the mass (with the same resultant force) halves the acceleration to {u3(abs(d["a"]) / 2)} {MS2}.', 'B1 a = F/m; B1 halves')


@n132.add('C3', (1, 2, 3, 4, 5), 'numerical')
def n132_calc(r, D):
    d = fma_case(r, D)
    if D <= 2 or d['kind'] in ('smooth', 'lift_rope'):
        t = r.choice([3, 4, 5, 6, 10])
        v = d['a'] * t
        return Q(d['txt'] + f' It starts from rest. Find its acceleration and its speed after {t} s.', f'{u3(d["a"])} {MS2}; {u3(v)} {MS}', 'M1 F = ma; A1 a; A1 speed')
    if d['kind'] == 'brake':
        s = Fr(d['u'] ** 2, 2) / (-d['a'])
        return Q(d['txt'] + ' Find the distance it travels before coming to rest.', f'{u3(s)} m', 'M1 F = ma; A1 deceleration; M1 v² = u² + 2as; A1 distance')
    # find resistance given acceleration
    t, v = r.choice([5, 8, 10, 20]), None
    v = d['a'] * t
    return Q(f'A car of mass {d["m"]} kg accelerates uniformly from rest to {u3(v)} {MS} in {t} s along a horizontal road. The driving force is {d["Dv"]} N. Find the resistance to motion.', f'{u3(d["Rv"])} N',
             'M1 a from suvat; A1 a; M1 D − R = ma; A1 resistance')


def n132_c4(r, D):
    d = fma_case(r, max(2, D))
    if d['kind'] != 'car':
        return None
    t1 = r.choice([5, 8, 10])
    v1 = d['a'] * t1
    B_ = r.choice([1500, 2000, 3000, 4000])
    dec = Fr(B_ + d['Rv'], d['m'])
    s2 = v1 * v1 / (2 * dec)
    intro = d['txt'] + f' It starts from rest. After {t1} s the driving force is removed and the brakes apply an additional force of {B_} N; the resistance is unchanged.'
    parts = [
        P('Find the acceleration of the car while the driving force acts.', f'{u3(d["a"])} {MS2}', 'M1 D − R = ma; A1 a'),
        P(f'Find the speed after {t1} s.', f'{u3(v1)} {MS}', 'B1 value'),
        P('Find the deceleration while braking.', f'{u3(dec)} {MS2}', 'M1 includes both resistance and braking force; A1 deceleration'),
        P('Find the distance travelled while braking to rest.', f'{u3(s2)} m', 'M1 speed when braking starts; M1 v² = u² + 2as; A1 distance'),
    ]
    return cmp_(r, intro, parts)


n132.add('C4', (2, 3, 4, 5))(n132_c4)


# ---------------------------------------------------------------- 13.3 lifts and Newton's third law

def lift_case(r):
    m = r.choice([50, 60, 65, 70, 75, 80])
    M = r.choice([300, 400, 500, 600, 800])
    a = r.choice([Fr(1, 2), 1, Fr(3, 2), 2, Fr(5, 2)])
    up = r.choice([True, False])
    sgn = 1 if up else -1
    R = m * (G + sgn * a)
    T_ = (M + m) * (G + sgn * a)
    return dict(m=m, M=M, a=Fr(a), up=up, R=R, T=T_, dirn='upwards' if up else 'downwards')


l133 = T("Motion in a lift and Newton's third law", 'motion in a lift', "newton's third law")
l133.fixed('C1', (1, 2), [
    ('A person stands in a lift accelerating upwards. How does the normal force from the floor compare with their weight?', 'it is greater than the weight', 'R − mg = ma with a > 0.', ['it equals the weight', 'it is less than the weight', 'it is zero']),
    ("By Newton's third law, if the floor pushes up on a person with 700 N, what force does the person exert on the floor?", '700 N downwards', 'Equal and opposite forces on different bodies.', ['700 N upwards', '0 N', '7000 N downwards']),
])
l133.fixed('C2', (2, 3), [
    ('Explain why a person in a lift moving upwards at constant speed feels their normal weight.', 'At constant speed the acceleration is zero, so R − mg = 0 and the floor pushes with a force equal to the weight.', 'B1 zero acceleration; B1 R = mg [2]'),
])


@l133.add('C1', (1, 2, 3))
def l133_c1(r, D):
    d = lift_case(r)
    return MC(r, f'A person of mass {d["m"]} kg stands in a lift that is accelerating {d["dirn"]} at {u3(d["a"])} {MS2}. Find the normal contact force on the person.', f'{u3(d["R"])} N',
              [f'{u3(d["m"] * G)} N', f'{u3(d["m"] * (G - d["a"]) if d["up"] else d["m"] * (G + d["a"]))} N', f'{u3(d["m"] * d["a"])} N', f'{u3(d["R"] + d["m"])} N'], f'R − mg = m × ({"+" if d["up"] else "−"}{u3(d["a"])}).')


@l133.add('C2', (1, 2, 3, 4), 'explain')
def l133_err(r, D):
    nm = person(r)
    d = lift_case(r)
    f = r.choice(['dir', 'pair', 'decel'])
    if f == 'dir':
        wrong = d['m'] * (G - d['a']) if d['up'] else d['m'] * (G + d['a'])
        return Q(f'A person of mass {d["m"]} kg is in a lift accelerating {d["dirn"]} at {u3(d["a"])} {MS2}. {nm} finds the normal force to be {u3(wrong)} N. Explain the error and correct it.',
                 f'The resultant force must be in the direction of the acceleration ({d["dirn"]}): R = m(g {"+" if d["up"] else "−"} a) = {u3(d["R"])} N.', 'B1 direction of resultant; B1 correct R')
    if f == 'pair':
        return Q(f"{nm} says that the weight of a person standing in a lift and the normal force from the floor form a Newton's third law pair. Explain why this is wrong.",
                 "Third-law pairs act on different bodies and are of the same type. The weight (Earth on person) pairs with the person pulling the Earth; the normal force (floor on person) pairs with the person pushing the floor.",
                 'B1 pairs act on different bodies; B1 correct pairs identified')
    return Q(f'A lift moving upwards decelerates at {u3(d["a"])} {MS2}. Explain whether a person of mass {d["m"]} kg in the lift feels heavier or lighter, and find the normal force.',
             f'Deceleration while moving up means the acceleration is downwards, so R = m(g − a) = {u3(d["m"] * (G - d["a"]))} N: lighter.', 'B1 acceleration downwards; B1 R and conclusion')


@l133.add('C3', (1, 2, 3, 4, 5), 'numerical')
def l133_calc(r, D):
    d = lift_case(r)
    if D <= 2:
        return Q(f'A lift of mass {d["M"]} kg carries a passenger of mass {d["m"]} kg and accelerates {d["dirn"]} at {u3(d["a"])} {MS2}. Find the tension in the lift cable.', f'{u3(d["T"])} N', 'M1 F = ma for lift and passenger together; A1 tension')
    if D <= 4:
        return Q(f'A lift of mass {d["M"]} kg carries a passenger of mass {d["m"]} kg. The tension in the cable is {u3(d["T"])} N. Find the acceleration of the lift and the force exerted by the passenger on the floor.',
                 f'{u3(d["a"])} {MS2} {d["dirn"]}; {u3(d["R"])} N downwards', 'M1 whole system; A1 a; M1 passenger alone; A1 force with direction')
    t1, t2, t3 = r.choice([2, 3, 4]), r.choice([5, 8, 10]), r.choice([2, 3, 4])
    V = d['a'] * t1
    a3 = V / t3
    R3 = d['m'] * (G - a3)
    return Q(f'A lift starts from rest and accelerates upwards at {u3(d["a"])} {MS2} for {t1} s, moves at constant speed for {t2} s and then decelerates uniformly to rest in {t3} s. A passenger of mass {d["m"]} kg stands in the lift. Find the normal force on the passenger in each stage.',
             f'{u3(d["m"] * (G + d["a"]))} N, {d["m"] * G} N, {u3(R3)} N', 'M1 each stage; A1 A1 A1')


def l133_c4(r, D):
    d = lift_case(r)
    t1 = r.choice([2, 3, 4])
    V = d['a'] * t1
    intro = f'A lift of mass {d["M"]} kg carries a crate of mass {d["m"]} kg on its floor. The lift starts from rest and accelerates {d["dirn"]} at {u3(d["a"])} {MS2} for {t1} s.'
    parts = [
        P('Find the tension in the lift cable during this stage.', f'{u3(d["T"])} N', 'M1 whole system; A1 tension'),
        P('Find the normal contact force between the crate and the floor of the lift.', f'{u3(d["R"])} N', 'M1 crate alone; A1 value'),
        P("State the force exerted by the crate on the floor, and name the law used.", f"{u3(d['R'])} N downwards, Newton's third law", 'B1 value and direction; B1 law'),
        P(f'Find the speed of the lift after {t1} s and the distance travelled.', f'{u3(V)} {MS}; {u3(V * t1 / 2)} m', 'M1 suvat; A1 both'),
    ]
    return cmp_(r, intro, parts)


l133.add('C4', (2, 3, 4, 5))(l133_c4)

CHAPTERS[13] = [f131, n132, l133]


# ================================================================ Chapter 14 Forces in two dimensions

def cosd(x):
    return math.cos(math.radians(x))


def sind(x):
    return math.sin(math.radians(x))


def force_set(r, n):
    """n forces as (magnitude, bearing angle from the positive x-axis, degrees)."""
    angs = r.sample([0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330], n)
    return [(r.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20]), a) for a in angs]


def resultant(fs):
    X = sum(m * cosd(a) for m, a in fs)
    Y = sum(m * sind(a) for m, a in fs)
    return X, Y, math.hypot(X, Y), math.degrees(math.atan2(Y, X))


def fdesc(m, a):
    if a == 0:
        return f'{m} N in the positive x-direction'
    if a == 90:
        return f'{m} N in the positive y-direction'
    if a == 180:
        return f'{m} N in the negative x-direction'
    if a == 270:
        return f'{m} N in the negative y-direction'
    return f'{m} N at {a}° anticlockwise from the positive x-direction'


r141 = T('Resolving forces into components and resultant forces', 'resolving forces', 'resultant force', 'components')
r141.fixed('C1', (1, 2), [
    ('A force of 10 N acts at 30° above the horizontal. What is its horizontal component?', '10 cos 30° = 8.66 N', 'Adjacent component uses cosine.', ['10 sin 30° = 5 N', '10 tan 30° = 5.77 N', '10 N']),
    ('Two perpendicular forces of 6 N and 8 N act at a point. What is the magnitude of their resultant?', '10 N', '√(36 + 64).', ['14 N', '2 N', '48 N']),
])
r141.fixed('C2', (2, 3), [
    ('Explain why resolving forces in two perpendicular directions is enough to find the resultant of several coplanar forces.', 'Each force can be replaced by perpendicular components; adding components in each direction gives the components of the resultant, which then give its magnitude and direction.', 'B1 components add independently; B1 combine with Pythagoras and tan [2]'),
])


@r141.add('C1', (1, 2, 3))
def r141_c1(r, D):
    m = r.choice([5, 8, 10, 12, 15, 20, 25, 30])
    a = r.choice([20, 25, 30, 35, 40, 50, 55, 60, 70])
    if D <= 2:
        comp = r.choice(['horizontal', 'vertical'])
        v = m * (cosd(a) if comp == 'horizontal' else sind(a))
        w = m * (sind(a) if comp == 'horizontal' else cosd(a))
        return MC(r, f'A force of {m} N acts at {a}° above the horizontal. Find its {comp} component.', f'{n3(v)} N', [f'{n3(w)} N', f'{n3(m * math.tan(math.radians(a)))} N', f'{n3(m / max(cosd(a), 0.1))} N', f'{m} N'],
                  f'{comp.capitalize()} component = {m} {"cos" if comp == "horizontal" else "sin"} {a}°.')
    p, q = r.choice([3, 5, 6, 7, 8, 9, 12]), r.choice([4, 5, 8, 10, 12, 15])
    R = math.hypot(p, q)
    return MC(r, f'Forces of {p} N and {q} N act at right angles. Find the magnitude of their resultant.', f'{u3(R)} N', [f'{p + q} N', f'{abs(q - p)} N' if q != p else '0 N', f'{p * q} N', f'{u3(math.sqrt(abs(q * q - p * p)))} N' if q != p else '1 N'], 'Pythagoras.')


@r141.add('C2', (1, 2, 3, 4), 'explain')
def r141_err(r, D):
    nm = person(r)
    m = r.choice([5, 8, 10, 12, 15, 20, 25])
    a = r.choice([20, 25, 35, 40, 50, 55, 65])
    f = r.choice(['sincos', 'add', 'angle'])
    if f == 'sincos':
        return Q(f'A force of {m} N acts at {a}° to the horizontal. {nm} gives its horizontal component as {m} sin {a}° = {n3(m * sind(a))} N. Explain the error.',
                 f'The horizontal component is adjacent to the {a}° angle, so it is {m} cos {a}° = {n3(m * cosd(a))} N.', 'B1 cosine for the adjacent side; B1 correct value')
    if f == 'add':
        p, q = r.choice([3, 5, 6, 8]), r.choice([4, 7, 10, 12])
        return Q(f'Two forces of {p} N and {q} N act at right angles. {nm} says the resultant is {p + q} N. Explain the error and find the resultant.',
                 f'Forces add as vectors, not as numbers: resultant = √({p}² + {q}²) = {u3(math.hypot(p, q))} N.', 'B1 vector addition; B1 correct value')
    X, Y = r.choice([3, 5, -4, -6, 8]), r.choice([4, -5, 6, -8, 2])
    th = math.degrees(math.atan2(Y, X))
    return Q(f'A resultant force has components {num(X)} N in the x-direction and {num(Y)} N in the y-direction. {nm} gives its direction as tan⁻¹({num(Y)}/{num(X)}) = {d1(math.degrees(math.atan(Y / X)))} from the positive x-axis. Explain why this may be wrong and give the correct direction.',
             f'tan⁻¹ ignores the quadrant: the force points into the {"first" if X > 0 and Y > 0 else "second" if X < 0 < Y else "third" if X < 0 and Y < 0 else "fourth"} quadrant, so the direction is {d1(th)} from the positive x-axis.',
             'B1 identifies the quadrant; B1 correct angle')


@r141.add('C3', (1, 2, 3, 4, 5), 'numerical')
def r141_calc(r, D):
    n = 2 if D <= 2 else 3 if D <= 4 else 4
    fs = force_set(r, n)
    X, Y, R, th = resultant(fs)
    if R < 0.5:
        return None
    desc = '; '.join(fdesc(m, a) for m, a in fs)
    if D == 1:
        return Q(f'Forces act on a particle: {desc}. Find the components of the resultant force in the x- and y-directions.', f'{n3(X)} N, {n3(Y)} N', 'M1 resolves each force; A1 x-component; A1 y-component')
    return Q(f'Forces act on a particle: {desc}. Find the magnitude of the resultant force and the angle it makes with the positive x-direction.', f'{n3(R)} N at {d1(th)}',
             'M1 resolves in two directions; A1 components; M1 Pythagoras; A1 magnitude and direction')


def r141_c4(r, D):
    fs = force_set(r, 3)
    X, Y, R, th = resultant(fs)
    if R < 0.5:
        return None
    m = r.choice([2, 3, 4, 5])
    intro = f'Three horizontal forces act on a particle of mass {m} kg resting on a smooth horizontal surface: ' + '; '.join(fdesc(mm, a) for mm, a in fs) + '.'
    parts = [
        P('Find the components of the resultant force.', f'{n3(X)} N and {n3(Y)} N', 'M1 resolves; A1 both'),
        P('Find the magnitude and direction of the resultant force.', f'{n3(R)} N at {d1(th)} to the positive x-direction', 'M1 Pythagoras; A1 magnitude; A1 direction'),
        P('Find the magnitude of the acceleration of the particle.', f'{n3(R / m)} {MS2}', 'M1 F = ma; A1 value'),
        P('State the fourth force that would keep the particle in equilibrium.', f'{n3(R)} N at {d1(th + 180 if th < 0 else th - 180)} to the positive x-direction', 'B1 equal and opposite to the resultant'),
    ]
    return cmp_(r, intro, parts)


r141.add('C4', (2, 3, 4, 5))(r141_c4)


# ---------------------------------------------------------------- 14.2 equilibrium

def two_string(r):
    W = r.choice([20, 30, 40, 50, 60, 80, 100])
    al, be = r.sample([20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70], 2)
    # T1 cos al = T2 cos be ; T1 sin al + T2 sin be = W (angles with the horizontal)
    T1 = W * cosd(be) / (sind(al) * cosd(be) + sind(be) * cosd(al))
    T2 = T1 * cosd(al) / cosd(be)
    if not ok(T1 * sind(al) + T2 * sind(be), W, 'two string'):
        return None
    return dict(W=W, al=al, be=be, T1=T1, T2=T2)


e142 = T('Equilibrium of a particle under coplanar forces', 'equilibrium of a particle', 'coplanar forces')
e142.fixed('C1', (1, 2), [
    ('A particle is in equilibrium under several forces. What is the resultant force?', 'zero', 'Equilibrium means no acceleration.', ['equal to the weight', 'equal to the largest force', 'it cannot be determined']),
    ('A particle in equilibrium is acted on by three forces. What can be said about the forces drawn nose to tail?', 'they form a closed triangle', 'Their vector sum is zero.', ['they form a straight line', 'they are all equal', 'they are perpendicular']),
])
e142.fixed('C2', (2, 3), [
    ('Explain why a particle hanging from two strings with one string vertical must have the other string slack.', 'The vertical string and weight have no horizontal components, so for horizontal equilibrium the other string must have zero horizontal component; if it is not vertical, its tension must be zero.', 'B1 horizontal resolution; B1 tension must be zero [2]'),
])


@e142.add('C1', (1, 2, 3))
def e142_c1(r, D):
    if D <= 2:
        m = r.choice([2, 3, 4, 5, 8])
        P_ = r.choice([10, 15, 20, 30])
        R = math.hypot(m * G, P_)
        ang = math.degrees(math.atan(P_ / (m * G)))
        return MC(r, f'A particle of mass {m} kg hangs from a string and is held in equilibrium by a horizontal force of {P_} N. Find the tension in the string.', f'{n3(R)} N',
                  [f'{m * G + P_} N', f'{n3(abs(m * G - P_))} N', f'{m * G} N', f'{n3(R / 2)} N'], 'Tension balances the weight and the horizontal force: T = √(W² + P²).')
    d = two_string(r)
    if not d:
        return None
    return MC(r, f'A particle of weight {d["W"]} N hangs from two strings making angles {d["al"]}° and {d["be"]}° with the horizontal. Which equation comes from resolving horizontally?', f'T₁ cos {d["al"]}° = T₂ cos {d["be"]}°',
              [f'T₁ sin {d["al"]}° = T₂ sin {d["be"]}°', f'T₁ cos {d["al"]}° + T₂ cos {d["be"]}° = {d["W"]}', f'T₁ + T₂ = {d["W"]}'], 'Horizontal components of the tensions balance.')


@e142.add('C2', (1, 2, 3, 4), 'explain')
def e142_err(r, D):
    nm = person(r)
    d = two_string(r)
    if not d:
        return None
    f = r.choice(['sum', 'show', 'triangle'])
    if f == 'sum':
        return Q(f'A particle of weight {d["W"]} N hangs in equilibrium from two strings inclined at {d["al"]}° and {d["be"]}° to the horizontal. {nm} assumes each string has tension {d["W"] // 2} N. Explain why this is wrong.',
                 f'Only the vertical components of the tensions support the weight, and the strings are at different angles; resolving gives T₁ = {n3(d["T1"])} N and T₂ = {n3(d["T2"])} N.', 'B1 components, not tensions, balance the weight; B1 correct tensions')
    if f == 'show':
        return Q(f'A particle of weight {d["W"]} N hangs in equilibrium from two strings inclined at {d["al"]}° and {d["be"]}° to the horizontal. Show that the tension in the first string is {n3(d["T1"])} N, correct to 3 significant figures.',
                 f'Resolving: T₁ cos {d["al"]}° = T₂ cos {d["be"]}° and T₁ sin {d["al"]}° + T₂ sin {d["be"]}° = {d["W"]}; solving gives T₁ = {n3(d["T1"])} N.', 'M1 resolves both ways; A1 solves to the given value')
    return Q(f'Explain why three forces acting on a particle in equilibrium can be represented by a closed triangle, and use this idea to explain how the tensions in two strings supporting a weight of {d["W"]} N can be found.',
             'The vector sum is zero, so drawn nose to tail they return to the start; the triangle has angles fixed by the string directions and one known side (the weight), so the sine rule gives the tensions.', 'B1 zero vector sum; B1 sine rule with the known side')


@e142.add('C3', (1, 2, 3, 4, 5), 'numerical')
def e142_calc(r, D):
    if D <= 2:
        m = r.choice([2, 3, 4, 5, 6])
        th = r.choice([20, 25, 30, 35, 40, 45])
        # string at th to vertical, horizontal force P
        P_ = m * G * math.tan(math.radians(th))
        T_ = m * G / cosd(th)
        return Q(f'A particle of mass {m} kg hangs from a light string. A horizontal force P N holds it in equilibrium with the string at {th}° to the vertical. Find P and the tension in the string.', f'P = {n3(P_)}; T = {n3(T_)} N',
                 'M1 resolves vertically; A1 T; M1 resolves horizontally; A1 P')
    if D <= 4:
        d = two_string(r)
        if not d:
            return None
        return Q(f'A particle of weight {d["W"]} N hangs in equilibrium from two light strings inclined at {d["al"]}° and {d["be"]}° to the horizontal. Find the tensions in the strings.', f'{n3(d["T1"])} N and {n3(d["T2"])} N',
                 'M1 resolves horizontally; M1 resolves vertically; M1 solves; A1 A1 tensions')
    # three forces: find unknown P and angle
    fs = force_set(r, 2)
    X, Y, R, th = resultant(fs)
    if R < 0.5:
        return None
    return Q(f'A particle is in equilibrium under three forces: {fdesc(*fs[0])}, {fdesc(*fs[1])}, and a force of magnitude F N. Find F and its direction.', f'F = {n3(R)} at {d1(th + 180 if th < 0 else th - 180)} to the positive x-direction',
             'M1 resolves; A1 components; M1 magnitude; A1 direction')


def e142_c4(r, D):
    m = r.choice([2, 3, 4, 5])
    th = r.choice([20, 25, 30, 35, 40])
    W = m * G
    # particle on a smooth plane at th, held by a horizontal force P
    P_ = W * math.tan(math.radians(th))
    R = W / cosd(th)
    if not ok(P_ * cosd(th), W * sind(th), 'plane horiz'):
        return None
    intro = f'A particle of mass {m} kg rests in equilibrium on a smooth plane inclined at {th}° to the horizontal, held by a horizontal force of magnitude P N acting in the vertical plane containing the line of greatest slope.'
    parts = [
        P('Draw a force diagram.', 'weight vertically down, normal reaction perpendicular to the plane, P horizontal', 'B1 all three forces'),
        P('By resolving parallel to the plane, find P.', f'P = {n3(P_)}', 'M1 P cos θ = mg sin θ; A1 P'),
        P('Find the normal reaction between the particle and the plane.', f'{n3(R)} N', 'M1 resolves perpendicular to the plane; A1 R'),
        P(f'P is now removed. Find the acceleration of the particle down the plane.', f'{n3(G * sind(th))} {MS2}', 'M1 mg sin θ = ma; A1 value'),
    ]
    return cmp_(r, intro, parts)


e142.add('C4', (2, 3, 4, 5))(e142_c4)


# ---------------------------------------------------------------- 14.3 inclined plane

def incline(r, D):
    m = r.choice([2, 3, 4, 5, 8, 10])
    if r.random() < 0.5:
        s, c = Fr(3, 5), Fr(4, 5)
        atxt = 'α, where sin α = 3/5'
        if r.random() < 0.5:
            s, c, atxt = Fr(7, 25), Fr(24, 25), 'α, where sin α = 7/25'
    else:
        a = r.choice([10, 15, 20, 25, 30, 35, 40])
        s, c, atxt = sind(a), cosd(a), f'{a}°'
    return dict(m=m, s=float(s), c=float(c), atxt=atxt)


i143 = T('Motion on an inclined plane', 'inclined plane', 'motion on an inclined plane')
i143.fixed('C1', (1, 2), [
    ('A particle of mass m slides down a smooth plane inclined at θ. What is its acceleration?', 'g sin θ', 'The component of the weight down the slope is mg sin θ.', ['g cos θ', 'g', 'g tan θ']),
    ('What is the normal reaction on a particle of mass m resting on a smooth plane inclined at θ (no other forces)?', 'mg cos θ', 'Resolve perpendicular to the plane.', ['mg sin θ', 'mg', 'mg/cos θ']),
])
i143.fixed('C2', (2, 3), [
    ('Explain why it is usually best to resolve forces parallel and perpendicular to an inclined plane.', 'The acceleration is along the plane, so resolving perpendicular gives an equilibrium equation and resolving parallel gives the F = ma equation; only the weight needs splitting into components.', 'B1 acceleration along the plane; B1 only weight resolved [2]'),
])


@i143.add('C1', (1, 2, 3))
def i143_c1(r, D):
    d = incline(r, D)
    if D == 1:
        return MC(r, f'A particle slides down a smooth plane inclined at {d["atxt"]}. Find its acceleration.', f'{n3(G * d["s"])} {MS2}', [f'{n3(G * d["c"])} {MS2}', f'{G} {MS2}', f'{n3(G * d["s"] / d["c"])} {MS2}'], 'a = g sin α.')
    return MC(r, f'A particle of mass {d["m"]} kg rests on a smooth plane inclined at {d["atxt"]}. Find the component of its weight down the plane.', f'{n3(d["m"] * G * d["s"])} N',
              [f'{n3(d["m"] * G * d["c"])} N', f'{d["m"] * G} N', f'{n3(d["m"] * d["s"])} N'], 'mg sin α.')


@i143.add('C2', (1, 2, 3, 4), 'explain')
def i143_err(r, D):
    nm = person(r)
    d = incline(r, D)
    f = r.choice(['cos', 'R', 'mass'])
    if f == 'cos':
        return Q(f'A particle slides down a smooth plane inclined at {d["atxt"]}. {nm} says its acceleration is g cos α = {n3(G * d["c"])} {MS2}. Explain the error.',
                 f'The component of the weight down the slope is mg sin α, so a = g sin α = {n3(G * d["s"])} {MS2}; g cos α is the perpendicular component.', 'B1 sin for the component along the slope; B1 correct value')
    if f == 'R':
        return Q(f'{nm} says that, for a particle of mass {d["m"]} kg on a smooth plane inclined at {d["atxt"]}, the normal reaction equals the weight, {d["m"] * G} N. Explain the error.',
                 f'Only the perpendicular component of the weight is balanced by R: R = mg cos α = {n3(d["m"] * G * d["c"])} N.', 'B1 resolves perpendicular to the plane; B1 correct R')
    return Q(f'{nm} says a heavier particle slides down a smooth slope inclined at {d["atxt"]} faster than a lighter one. Explain why this is wrong.',
             f'mg sin α = ma gives a = g sin α = {n3(G * d["s"])} {MS2}, independent of the mass.', 'B1 mass cancels; B1 acceleration value')


@i143.add('C3', (1, 2, 3, 4, 5), 'numerical')
def i143_calc(r, D):
    d = incline(r, D)
    m = d['m']
    if D <= 2:
        L = r.choice([2, 3, 4, 5, 8, 10])
        a = G * d['s']
        v = math.sqrt(2 * a * L)
        return Q(f'A particle is released from rest on a smooth plane inclined at {d["atxt"]}. Find its speed after it has travelled {L} m down the plane.', f'{n3(v)} {MS}', 'M1 a = g sin α; A1 a; M1 v² = 2as; A1 speed')
    if D <= 4:
        P_ = r.choice([20, 30, 40, 50, 60, 80])
        a = (P_ - m * G * d['s']) / m
        if a <= 0:
            return None
        return Q(f'A particle of mass {m} kg is pulled up a smooth plane inclined at {d["atxt"]} by a force of {P_} N acting up the line of greatest slope. Find its acceleration and the normal reaction.', f'{n3(a)} {MS2}; {n3(m * G * d["c"])} N',
                 'M1 P − mg sin α = ma; A1 a; B1 R')
    u = r.choice([4, 5, 6, 8, 10])
    a = G * d['s']
    s = u * u / (2 * a)
    t = 2 * u / a
    return Q(f'A particle is projected up a smooth plane inclined at {d["atxt"]} with speed {u} {MS}. Find the distance it travels up the plane before coming to rest and the total time until it returns to its starting point.', f'{n3(s)} m; {n3(t)} s',
             'M1 deceleration g sin α; A1 distance; M1 symmetry or suvat; A1 time')


def i143_c4(r, D):
    d = incline(r, D)
    m = d['m']
    P_ = r.choice([30, 40, 50, 60, 80, 100])
    a = (P_ - m * G * d['s']) / m
    if a <= 0:
        return None
    t = r.choice([2, 3, 4])
    v = a * t
    a2 = G * d['s']
    s2 = v * v / (2 * a2)
    intro = f'A particle of mass {m} kg is pulled from rest up a smooth plane inclined at {d["atxt"]} by a force of {P_} N parallel to the line of greatest slope. The force is removed after {t} s.'
    parts = [
        P('Find the acceleration of the particle while the force acts.', f'{n3(a)} {MS2}', 'M1 P − mg sin α = ma; A1 a'),
        P('Find the normal reaction.', f'{n3(m * G * d["c"])} N', 'B1 mg cos α'),
        P('Find the speed of the particle when the force is removed.', f'{n3(v)} {MS}', 'M1 a; A1 v = at'),
        P('Find the further distance the particle moves up the plane after the force is removed.', f'{n3(s2)} m', 'M1 speed at removal; M1 deceleration g sin α; A1 distance'),
    ]
    return cmp_(r, intro, parts)


i143.add('C4', (2, 3, 4, 5))(i143_c4)

CHAPTERS[14] = [r141, e142, i143]


# ================================================================ Chapter 15 Friction

MUS = [Fr(1, 10), Fr(1, 5), Fr(1, 4), Fr(3, 10), Fr(1, 3), Fr(2, 5), Fr(1, 2), Fr(3, 5), Fr(3, 4)]


def mus(r):
    return r.choice(MUS)


def rough_h(r, D):
    """Block on rough horizontal ground pulled by P at angle th above the horizontal."""
    m = r.choice([2, 3, 4, 5, 8, 10, 12])
    mu = mus(r)
    th = 0 if D <= 2 else r.choice([0, 15, 20, 25, 30, 35, 40])
    P_ = r.choice([5, 8, 10, 12, 15, 20, 25, 30, 40, 50])
    R = m * G - P_ * sind(th)
    if R <= 0:
        return None
    Fmax = float(mu) * R
    drive = P_ * cosd(th)
    moves = drive > Fmax + 1e-9
    a = (drive - Fmax) / m if moves else 0.0
    return dict(m=m, mu=mu, th=th, P=P_, R=R, Fmax=Fmax, drive=drive, moves=moves, a=a, F=Fmax if moves else drive)


def pull_txt(d):
    return f'a horizontal force of {d["P"]} N' if d['th'] == 0 else f'a force of {d["P"]} N at {d["th"]}° above the horizontal'


f151 = T('Limiting friction and the coefficient of friction F ≤ μR', 'limiting friction', 'coefficient of friction', 'f ≤ μr')
f151.fixed('C1', (1, 2), [
    ('A block is on the point of sliding. What is the friction force?', 'F = μR', 'Friction is limiting.', ['F < μR', 'F = 0', 'F = R']),
    ('A block of weight 40 N rests on rough horizontal ground with μ = 0.3 and no horizontal force applied. What is the friction force?', '0 N', 'Friction only acts to oppose a tendency to move.', ['12 N', '40 N', '13.3 N']),
    ('A force pulling a block at an angle above the horizontal has what effect on the normal reaction?', 'it reduces it', 'The upward component of the pull supports part of the weight.', ['it increases it', 'no effect', 'it makes it zero']),
])
f151.fixed('C2', (2, 3), [
    ('Explain why friction is not always equal to μR.', 'μR is the maximum (limiting) value; friction only takes the value needed to prevent motion, up to μR. When sliding or on the point of sliding, F = μR.', 'B1 F ≤ μR; B1 equality only when limiting or moving [2]'),
])


@f151.add('C1', (1, 2, 3))
def f151_c1(r, D):
    d = rough_h(r, D)
    if not d:
        return None
    if D == 1:
        return MC(r, f'A block of mass {d["m"]} kg rests on rough horizontal ground with coefficient of friction {u3(d["mu"])}. Find the maximum possible friction force.', f'{u3(d["mu"] * d["m"] * G)} N',
                  [f'{u3(d["m"] * G)} N', f'{u3(d["mu"] * d["m"])} N', f'{u3(d["m"] * G / d["mu"])} N', f'{u3(d["mu"] * d["m"] * G * 2)} N'], 'Fmax = μR = μmg.')
    return MC(r, f'A block of mass {d["m"]} kg on rough horizontal ground (μ = {u3(d["mu"])}) is pulled by {pull_txt(d)}. What happens?', 'it slides' if d['moves'] else 'it remains at rest',
              ['it remains at rest' if d['moves'] else 'it slides', 'it lifts off the ground', 'it moves at constant speed'], f'Compare {n3(d["drive"])} N with μR = {n3(d["Fmax"])} N.')


@f151.add('C2', (1, 2, 3, 4), 'explain')
def f151_err(r, D):
    nm = person(r)
    d = rough_h(r, max(3, D))
    if not d:
        return None
    f = r.choice(['always', 'Rmg', 'mu'])
    if f == 'always' and not d['moves']:
        return Q(f'A block of mass {d["m"]} kg rests on rough horizontal ground (μ = {u3(d["mu"])}) and is pulled by {pull_txt(d)}. It does not move. {nm} says the friction force is μR = {n3(d["Fmax"])} N. Explain the error.',
                 f'The block is not on the point of slipping necessarily; friction just balances the horizontal pull: F = {n3(d["drive"])} N ≤ μR = {n3(d["Fmax"])} N.', 'B1 F ≤ μR; B1 friction equals the horizontal component')
    if f == 'Rmg' and d['th']:
        return Q(f'A block of mass {d["m"]} kg on rough horizontal ground is pulled by {pull_txt(d)}. {nm} takes the normal reaction as {d["m"] * G} N. Explain the error.',
                 f'The pull has an upward component {d["P"]} sin {d["th"]}°, so R = {d["m"] * G} − {n3(d["P"] * sind(d["th"]))} = {n3(d["R"])} N.', 'B1 vertical component of the pull; B1 correct R')
    return Q(f'Explain why the coefficient of friction μ between a block and the ground has no units, and state what a larger value of μ means.', 'μ = F/R is a ratio of two forces, so it has no units; a larger μ means a rougher contact that can provide more friction for the same normal reaction.',
             'B1 ratio of forces; B1 rougher contact')


@f151.add('C3', (1, 2, 3, 4, 5), 'numerical')
def f151_calc(r, D):
    d = rough_h(r, D)
    if not d:
        return None
    if D <= 2:
        if not d['moves']:
            return Q(f'A block of mass {d["m"]} kg rests on rough horizontal ground with μ = {u3(d["mu"])}. A horizontal force of {d["P"]} N is applied. Determine whether the block moves and state the friction force.', f'does not move; friction {u3(d["P"])} N',
                     'M1 μR; A1 compares; A1 friction')
        return Q(f'A block of mass {d["m"]} kg is pulled along rough horizontal ground (μ = {u3(d["mu"])}) by a horizontal force of {d["P"]} N. Find its acceleration.', f'{n3(d["a"])} {MS2}', 'M1 R = mg; M1 F = μR; A1 a')
    if D == 3:
        # find mu for limiting equilibrium
        mu = d['drive'] / d['R']
        return Q(f'A block of mass {d["m"]} kg on rough horizontal ground is about to slide when pulled by {pull_txt(d)}. Find the coefficient of friction.', n3(mu), 'M1 resolves vertically; M1 resolves horizontally with F = μR; A1 μ')
    if not d['moves']:
        return None
    t = r.choice([2, 3, 4, 5])
    v = d['a'] * t
    return Q(f'A block of mass {d["m"]} kg starts from rest on rough horizontal ground (μ = {u3(d["mu"])}) and is pulled by {pull_txt(d)}. Find its speed after {t} s.', f'{n3(v)} {MS}',
             'M1 R; M1 F = μR; M1 N2L; A1 a; A1 speed')


def f151_c4(r, D):
    d = rough_h(r, 3)
    if not d or not d['moves'] or not d['th']:
        return None
    t = r.choice([2, 3, 4])
    v = d['a'] * t
    dec = float(d['mu']) * G
    s2 = v * v / (2 * dec)
    intro = f'A box of mass {d["m"]} kg on rough horizontal ground (μ = {u3(d["mu"])}) is pulled from rest by {pull_txt(d)}.'
    parts = [
        P('Find the normal reaction.', f'{n3(d["R"])} N', 'M1 resolves vertically; A1 R'),
        P('Find the acceleration of the box.', f'{n3(d["a"])} {MS2}', 'M1 F = μR; M1 N2L horizontally; A1 a'),
        P(f'The force is removed after {t} s. Find the further distance the box slides before coming to rest.', f'{n3(s2)} m', 'M1 new R = mg; M1 deceleration μg; A1 distance'),
    ]
    return cmp_(r, intro, parts)


f151.add('C4', (2, 3, 4, 5))(f151_c4)


# ---------------------------------------------------------------- 15.2 friction on slopes

def rough_slope(r, D):
    m = r.choice([2, 3, 4, 5, 8, 10])
    a = r.choice([15, 20, 25, 30, 35, 40, 45])
    mu = mus(r)
    s, c = sind(a), cosd(a)
    R = m * G * c
    Fmax = float(mu) * R
    down = m * G * s
    slides = down > Fmax + 1e-9
    acc = (down - Fmax) / m if slides else 0.0
    Pmin = max(0.0, down - Fmax)
    Pmax = down + Fmax
    return dict(m=m, al=a, mu=mu, R=R, Fmax=Fmax, down=down, slides=slides, acc=acc, Pmin=Pmin, Pmax=Pmax)


f152 = T('Equilibrium and motion with friction, including on rough slopes', 'rough slopes', 'friction on a slope', 'equilibrium with friction')
f152.fixed('C1', (1, 2), [
    ('A block rests on a rough slope inclined at α and is on the point of slipping down. What is the relationship between μ and α?', 'μ = tan α', 'mg sin α = μmg cos α.', ['μ = sin α', 'μ = cos α', 'μ = 1/tan α']),
    ('A block is pushed up a rough slope. In which direction does friction act?', 'down the slope', 'Friction opposes the motion.', ['up the slope', 'perpendicular to the slope', 'vertically upwards']),
])
f152.fixed('C2', (2, 3), [
    ('Explain why the force needed to push a block up a rough slope at constant speed is greater than the force needed to stop it sliding down.', 'Pushing up, friction acts down the slope with the weight component, so P = mg sin α + μR; holding it, friction helps, acting up the slope, so P = mg sin α − μR.', 'B1 friction direction reverses; B1 the two expressions [2]'),
])


@f152.add('C1', (1, 2, 3))
def f152_c1(r, D):
    d = rough_slope(r, D)
    if D == 1:
        return MC(r, f'A block of mass {d["m"]} kg rests on a rough plane inclined at {d["al"]}°. Find the normal reaction.', f'{n3(d["R"])} N', [f'{n3(d["down"])} N', f'{d["m"] * G} N', f'{n3(d["m"] * G / cosd(d["al"]))} N'], 'R = mg cos α.')
    if abs(math.tan(math.radians(d['al'])) - float(d['mu'])) < 1e-9:
        return None
    return MC(r, f'A block is placed at rest on a rough plane inclined at {d["al"]}° with μ = {u3(d["mu"])}. What happens?', 'it slides down' if d['slides'] else 'it stays at rest',
              ['it stays at rest' if d['slides'] else 'it slides down', 'it slides up', 'it is in limiting equilibrium'],
              f'Compare tan {d["al"]}° = {n3(math.tan(math.radians(d["al"])))} with μ.')


@f152.add('C2', (1, 2, 3, 4), 'explain')
def f152_err(r, D):
    nm = person(r)
    d = rough_slope(r, D)
    f = r.choice(['dir', 'R', 'mass'])
    if f == 'dir' and d['slides']:
        wrong = (d['down'] + d['Fmax']) / d['m']
        return Q(f'A block slides down a rough plane inclined at {d["al"]}° with μ = {u3(d["mu"])}. {nm} finds its acceleration as g(sin α + μ cos α) = {n3(wrong)} {MS2}. Explain the error.',
                 f'Friction opposes the motion, so it acts up the slope: a = g(sin α − μ cos α) = {n3(d["acc"])} {MS2}.', 'B1 friction up the slope; B1 correct acceleration')
    if f == 'R':
        return Q(f'{nm} uses R = mg = {d["m"] * G} N for a block of mass {d["m"]} kg on a rough slope inclined at {d["al"]}°. Explain the error and find the correct maximum friction for μ = {u3(d["mu"])}.',
                 f'R balances the perpendicular component only: R = mg cos α = {n3(d["R"])} N, so Fmax = μR = {n3(d["Fmax"])} N.', 'B1 R = mg cos α; B1 Fmax')
    return Q(f'Show that whether a block placed at rest on a rough slope inclined at {d["al"]}° slides does not depend on its mass, and decide whether it slides when μ = {u3(d["mu"])}.',
             f'It slides if mg sin α > μmg cos α, i.e. tan α > μ: m cancels. tan {d["al"]}° = {n3(math.tan(math.radians(d["al"])))}, so it {"slides" if d["slides"] else "does not slide"}.', 'M1 compares components; A1 m cancels and conclusion')


@f152.add('C3', (1, 2, 3, 4, 5), 'numerical')
def f152_calc(r, D):
    d = rough_slope(r, D)
    if D <= 2:
        if not d['slides']:
            return None
        return Q(f'A block of mass {d["m"]} kg is released from rest on a rough plane inclined at {d["al"]}° (μ = {u3(d["mu"])}). Find its acceleration down the plane.', f'{n3(d["acc"])} {MS2}', 'M1 R = mg cos α; M1 N2L; A1 a')
    if D == 3:
        return Q(f'A block of mass {d["m"]} kg rests on a rough plane inclined at {d["al"]}° (μ = {u3(d["mu"])}). Find the force P, parallel to the plane, needed to push the block up the plane at constant speed.', f'{n3(d["Pmax"])} N',
                 'M1 R; M1 friction down the slope; A1 P')
    if D == 4:
        return Q(f'A block of mass {d["m"]} kg rests on a rough plane inclined at {d["al"]}° (μ = {u3(d["mu"])}), held by a force P N acting up the line of greatest slope. Find the range of values of P for which the block remains in equilibrium.',
                 f'{n3(d["Pmin"])} ≤ P ≤ {n3(d["Pmax"])}' if d['Pmin'] > 0 else f'0 ≤ P ≤ {n3(d["Pmax"])}', 'M1 friction up (least P); M1 friction down (greatest P); A1 A1 bounds')
    u = r.choice([4, 5, 6, 8, 10])
    dec = (d['down'] + d['Fmax']) / d['m']
    s = u * u / (2 * dec)
    return Q(f'A block is projected up a rough plane inclined at {d["al"]}° (μ = {u3(d["mu"])}) with speed {u} {MS}. Find the distance it travels before coming to rest, and determine whether it then slides back down.',
             f'{n3(s)} m; {"slides back" if d["slides"] else "remains at rest"}', 'M1 deceleration g(sin α + μ cos α); A1 distance; B1 compares tan α with μ')


def f152_c4(r, D):
    d = rough_slope(r, D)
    if not d['slides']:
        return None
    u = r.choice([5, 6, 8, 10])
    dec = (d['down'] + d['Fmax']) / d['m']
    s = u * u / (2 * dec)
    v2 = math.sqrt(2 * d['acc'] * s)
    intro = f'A particle of mass {d["m"]} kg is projected up a line of greatest slope of a rough plane inclined at {d["al"]}° with speed {u} {MS}. The coefficient of friction is {u3(d["mu"])}.'
    parts = [
        P('Find the deceleration of the particle while it moves up the plane.', f'{n3(dec)} {MS2}', 'M1 R = mg cos α; M1 friction down the slope; A1 deceleration'),
        P('Find the distance it travels up the plane.', f'{n3(s)} m', 'M1 v² = u² + 2as; A1 distance'),
        P('Show that it slides back down and find its acceleration down the plane.', f'tan α > μ; {n3(d["acc"])} {MS2}', 'B1 condition; M1 friction up the slope; A1 a'),
        P('Find its speed when it returns to the point of projection.', f'{n3(v2)} {MS}', 'M1 v² = 2as; A1 speed'),
    ]
    return cmp_(r, intro, parts)


f152.add('C4', (2, 3, 4, 5))(f152_c4)


# ---------------------------------------------------------------- 15.3 modelling assumptions

m153 = T('Smooth and rough contact and modelling assumptions', 'modelling assumptions', 'smooth and rough contact')
m153.fixed('C1', (1, 2), [
    ('What does it mean to model a surface as smooth?', 'there is no friction between the surface and the object', 'Smooth: μ = 0.', ['the surface is horizontal', 'the object does not move', 'air resistance is ignored']),
    ('What does modelling a string as light mean?', 'its mass is negligible, so the tension is the same throughout', 'A light string has no weight.', ['it does not stretch', 'it is very short', 'it can push as well as pull']),
    ('What does modelling a string as inextensible mean?', 'it does not stretch, so connected particles have the same speed and acceleration', 'Inextensible means fixed length.', ['it has no mass', 'it cannot break', 'its tension is zero']),
])
m153.fixed('C2', (2, 3), [
    ('Explain the effect on the predicted acceleration of modelling a slope as smooth when in reality it is rough.', 'The smooth model ignores friction, which opposes motion, so it overestimates the acceleration down the slope.', 'B1 friction ignored; B1 overestimate [2]'),
    ('Explain why a model that treats a car as a particle might still give useful predictions.', 'For straight-line motion over large distances, the car\'s size and rotation are unimportant compared with its overall motion, so the particle model captures the main features.', 'B1 size small compared with distances; B1 main features captured [2]'),
])

ASSUME = [('the pulley is smooth', 'the tension is the same on both sides of the pulley'), ('the string is light', 'the tension is the same throughout the string'),
          ('the string is inextensible', 'both particles have the same magnitude of acceleration'), ('the block is a particle', 'all forces act at a single point and rotation is ignored'),
          ('air resistance is negligible', 'the only force during flight is the weight'), ('the surface is smooth', 'there is no friction force'),
          ('the rod is light', 'its weight can be ignored'), ('g is constant', 'the weight does not change with height')]


@m153.add('C1', (1, 2, 3))
def m153_c1(r, D):
    a, e = r.choice(ASSUME)
    others = [x[1] for x in ASSUME if x[1] != e]
    return MC(r, f'In a mechanics model it is assumed that {a}. Which consequence follows from this assumption?', e, r.sample(others, 3), f'{cap(a)}: {e}.')


@m153.add('C2', (1, 2, 3, 4), 'explain')
def m153_err(r, D):
    nm = person(r)
    d = rough_slope(r, D)
    f = r.choice(['compare', 'refine', 'assume'])
    if f == 'compare':
        a_s = G * sind(d['al'])
        return Q(f'A block slides down a plane inclined at {d["al"]}°. {nm} models the plane as smooth and predicts an acceleration of {n3(a_s)} {MS2}; the measured acceleration is {n3(d["acc"]) if d["slides"] else "0"} {MS2}. Explain the difference and state how the model should be refined.',
                 f'The real plane is rough; friction opposes the motion. Modelling it as rough with μ = {u3(d["mu"])} gives a = g(sin α − μ cos α) = {n3(d["acc"]) if d["slides"] else "0 (no sliding)"} {MS2}.',
                 'B1 friction ignored in the smooth model; B1 refined model with friction')
    if f == 'refine':
        return Q(f'{nm} models a cyclist freewheeling down a hill as a particle on a smooth slope inclined at {d["al"]}°. State two ways in which this model could be refined and the effect of each on the predicted speed.',
                 'Include air resistance; include friction/rolling resistance. Each opposes motion and reduces the predicted speed.', 'B1 air resistance; B1 friction; B1 both reduce speed')
    a, e = r.choice(ASSUME)
    return Q(f'In a problem about two particles connected over a pulley, {nm} assumes that {a}. Explain how this assumption is used in the solution.', f'Because {a}, {e}.', 'B1 consequence; B1 how it simplifies the equations')


@m153.add('C3', (1, 2, 3, 4, 5), 'numerical')
def m153_calc(r, D):
    d = rough_slope(r, D)
    L = r.choice([2, 3, 4, 5, 8])
    vs = math.sqrt(2 * G * sind(d['al']) * L)
    if not d['slides']:
        return Q(f'A block is released from rest on a plane inclined at {d["al"]}°. Find its speed after moving {L} m down the plane if the plane is smooth, and state what happens if the plane is rough with μ = {u3(d["mu"])}.',
                 f'{n3(vs)} {MS}; it does not move (tan α ≤ μ)', 'M1 a = g sin α; A1 speed; B1 compares tan α with μ')
    vr = math.sqrt(2 * d['acc'] * L)
    return Q(f'A block is released from rest on a plane inclined at {d["al"]}°. Find its speed after moving {L} m down the plane (a) if the plane is smooth, (b) if the plane is rough with μ = {u3(d["mu"])}.',
             f'(a) {n3(vs)} {MS} (b) {n3(vr)} {MS}', 'M1 smooth acceleration; A1 speed; M1 rough acceleration; A1 speed')


def m153_c4(r, D):
    d = rough_slope(r, D)
    if not d['slides']:
        return None
    L = r.choice([2, 4, 5, 8])
    vs = math.sqrt(2 * G * sind(d['al']) * L)
    vr = math.sqrt(2 * d['acc'] * L)
    intro = f'A sledge of mass {d["m"]} kg is released from rest at the top of a slope of length {L} m inclined at {d["al"]}° to the horizontal.'
    parts = [
        P('Modelling the slope as smooth and the sledge as a particle, find the speed at the bottom.', f'{n3(vs)} {MS}', 'M1 a = g sin α; A1 speed'),
        P(f'In a refined model the slope is rough with μ = {u3(d["mu"])}. Find the speed at the bottom.', f'{n3(vr)} {MS}', 'M1 friction; M1 acceleration; A1 speed'),
        P('State one further refinement to the model and its effect.', 'include air resistance, which would reduce the speed further', 'B1 refinement with effect'),
    ]
    return cmp_(r, intro, parts)


m153.add('C4', (2, 3, 4, 5))(m153_c4)

CHAPTERS[15] = [f151, f152, m153]


# ================================================================ Chapter 16 Connected particles

def tow_case(r, D):
    M = r.choice([800, 1000, 1200, 1500, 1800])
    m = r.choice([200, 300, 400, 500, 600])
    Dv = r.choice([2000, 2500, 3000, 3500, 4000, 5000])
    R1 = r.choice([200, 300, 400, 500])
    R2 = r.choice([100, 150, 200, 250])
    a = Fr(Dv - R1 - R2, M + m)
    if a <= 0:
        return None
    T_ = m * a + R2
    if not ok(float(Dv - R1 - T_), float(M * a), 'tow'):
        return None
    veh = r.choice([('car', 'trailer'), ('lorry', 'trailer'), ('tractor', 'cart'), ('locomotive', 'truck')])
    return dict(M=M, m=m, Dv=Dv, R1=R1, R2=R2, a=a, T=T_, veh=veh)


c161 = T('Particles connected by strings: tension and towing problems', 'connected particles', 'towing', 'tension')
c161.fixed('C1', (1, 2), [
    ('A car tows a trailer with a light rigid tow-bar. Which statement about their accelerations is true?', 'they have the same acceleration', 'They move together as one system.', ['the trailer has a smaller acceleration', 'the car has zero acceleration', 'the accelerations are in opposite directions']),
    ('When a car towing a trailer brakes, what force may the tow-bar exert on the trailer?', 'a thrust', 'A rigid bar can push, slowing the trailer.', ['a tension', 'no force', 'a friction force']),
])
c161.fixed('C2', (2, 3), [
    ('Explain why the tension in a tow-rope does not appear in the equation of motion for the whole car-and-trailer system.', 'The tension acts on the car and on the trailer in opposite directions (an internal force), so the two cancel when the system is treated as a whole.', 'B1 internal force; B1 equal and opposite forces cancel [2]'),
])


@c161.add('C1', (1, 2, 3))
def c161_c1(r, D):
    d = tow_case(r, D)
    if not d:
        return None
    A, B = d['veh']
    stem = f'A {A} of mass {d["M"]} kg tows a {B} of mass {d["m"]} kg along a level road. The driving force is {d["Dv"]} N and the resistances are {d["R1"]} N on the {A} and {d["R2"]} N on the {B}.'
    if D <= 2:
        return MC(r, stem + ' Find the acceleration.', f'{u3(d["a"])} {MS2}', [f'{u3(Fr(d["Dv"], d["M"] + d["m"]))} {MS2}', f'{u3(Fr(d["Dv"] - d["R1"], d["M"]))} {MS2}', f'{u3(Fr(d["Dv"] - d["R1"] - d["R2"], d["M"]))} {MS2}', f'{u3(d["a"] * 2)} {MS2}'],
                  'Whole system: D − R₁ − R₂ = (M + m)a.')
    return MC(r, stem + ' Find the tension in the tow-bar.', f'{u3(d["T"])} N', [f'{u3(d["m"] * d["a"])} N', f'{u3(d["Dv"] - d["R1"])} N', f'{u3(d["m"] * d["a"] - d["R2"])} N' if d['m'] * d['a'] - d['R2'] > 0 else f'{u3(d["T"] + d["R2"])} N', f'{u3(d["T"] * 2)} N'],
              f'For the {B}: T − R₂ = ma.')


@c161.add('C2', (1, 2, 3, 4), 'explain')
def c161_err(r, D):
    nm = person(r)
    d = tow_case(r, D)
    if not d:
        return None
    A, B = d['veh']
    f = r.choice(['tens', 'mass', 'brake'])
    stem = f'A {A} of mass {d["M"]} kg tows a {B} of mass {d["m"]} kg along a level road with driving force {d["Dv"]} N; resistances are {d["R1"]} N on the {A} and {d["R2"]} N on the {B}.'
    if f == 'tens':
        return Q(stem + f' {nm} says the tension in the tow-bar equals the driving force, {d["Dv"]} N. Explain the error and find the tension.',
                 f'The driving force accelerates both vehicles; for the {B} alone T − {d["R2"]} = {d["m"]}a with a = {u3(d["a"])} {MS2}, so T = {u3(d["T"])} N.', 'B1 considers the trailer alone; B1 correct tension')
    if f == 'mass':
        wrong = Fr(d['Dv'] - d['R1'] - d['R2'], d['M'])
        return Q(stem + f' {nm} finds the acceleration as ({d["Dv"]} − {d["R1"]} − {d["R2"]})/{d["M"]} = {u3(wrong)} {MS2}. Explain the error.',
                 f'For the whole system the mass is {d["M"]} + {d["m"]} = {d["M"] + d["m"]} kg, giving a = {u3(d["a"])} {MS2}.', 'B1 total mass; B1 correct acceleration')
    return Q(stem + f' The {A} then brakes. Explain why the tow-bar may now be in thrust rather than tension.',
             f'If the {A} decelerates more rapidly than resistance alone would decelerate the {B}, the bar must push back on the {B} to slow it: a thrust.', 'B1 trailer would otherwise decelerate less; B1 bar pushes: thrust')


@c161.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c161_calc(r, D):
    d = tow_case(r, D)
    if not d:
        return None
    A, B = d['veh']
    stem = f'A {A} of mass {d["M"]} kg tows a {B} of mass {d["m"]} kg along a straight level road by means of a light rigid tow-bar. The driving force is {d["Dv"]} N and the resistances to motion are {d["R1"]} N on the {A} and {d["R2"]} N on the {B}.'
    if D <= 3:
        return Q(stem + ' Find the acceleration and the tension in the tow-bar.', f'{u3(d["a"])} {MS2}; {u3(d["T"])} N', 'M1 whole system; A1 a; M1 trailer alone; A1 T')
    if D == 4:
        # given acceleration find driving force
        return Q(f'A {A} of mass {d["M"]} kg tows a {B} of mass {d["m"]} kg along a level road with acceleration {u3(d["a"])} {MS2}. The resistances are {d["R1"]} N and {d["R2"]} N respectively. Find the driving force and the tension in the tow-bar.',
                 f'{u3(d["Dv"])} N; {u3(d["T"])} N', 'M1 whole system; A1 D; M1 trailer; A1 T')
    # on a slope sin a = 1/20
    s = Fr(1, r.choice([10, 20, 25, 50]))
    a2 = (d['Dv'] - d['R1'] - d['R2'] - (d['M'] + d['m']) * G * s) / (d['M'] + d['m'])
    if a2 <= 0:
        return None
    T2 = d['m'] * a2 + d['R2'] + d['m'] * G * s
    return Q(stem.replace('straight level road', f'straight road inclined at α to the horizontal, where sin α = {num(s)}, up the slope') + ' Find the acceleration and the tension in the tow-bar.', f'a = {u3(a2)} {MS2}; T = {u3(T2)} N',
             'M1 includes weight components; A1 a; M1 trailer alone; A1 T')


def c161_c4(r, D):
    d = tow_case(r, D)
    if not d:
        return None
    A, B = d['veh']
    t = r.choice([5, 8, 10])
    v = d['a'] * t
    # rope breaks: trailer decelerates under R2
    dec = Fr(d['R2'], d['m'])
    s = v * v / (2 * dec)
    intro = f'A {A} of mass {d["M"]} kg tows a {B} of mass {d["m"]} kg from rest along a level road using a light horizontal tow-rope. The driving force is {d["Dv"]} N, and the resistances are {d["R1"]} N on the {A} and {d["R2"]} N on the {B}.'
    parts = [
        P('Find the acceleration of the system.', f'{u3(d["a"])} {MS2}', 'M1 whole system; A1 a'),
        P('Find the tension in the tow-rope.', f'{u3(d["T"])} N', 'M1 trailer alone; A1 T'),
        P(f'After {t} s the tow-rope breaks. Find the distance the {B} travels after the rope breaks before coming to rest.', f'{u3(s)} m', 'M1 speed at the break; M1 deceleration R₂/m; A1 distance'),
    ]
    return cmp_(r, intro, parts)


c161.add('C4', (2, 3, 4, 5))(c161_c4)


# ---------------------------------------------------------------- 16.2 pulleys

def pulley_v(r):
    m1, m2 = r.sample([1, 2, 3, 4, 5, 6, 7, 8], 2)
    if m1 < m2:
        m1, m2 = m2, m1
    a = Fr((m1 - m2) * G, m1 + m2)
    T_ = Fr(2 * m1 * m2 * G, m1 + m2)
    return dict(m1=m1, m2=m2, a=a, T=T_)


def pulley_t(r, rough=True):
    m1 = r.choice([2, 3, 4, 5, 6, 8])  # on table
    m2 = r.choice([1, 2, 3, 4, 5])  # hanging
    mu = mus(r) if rough else Fr(0)
    net = m2 * G - mu * m1 * G
    if net <= 0:
        return None
    a = net / (m1 + m2)
    T_ = m2 * (G - a)
    if not ok(float(T_ - mu * m1 * G), float(m1 * a), 'pulley table'):
        return None
    return dict(m1=m1, m2=m2, mu=mu, a=a, T=T_)


p162 = T('Pulley systems over smooth pegs and pulleys', 'pulley systems', 'smooth pulleys')
p162.fixed('C1', (1, 2), [
    ('Two particles hang over a smooth pulley connected by a light inextensible string. What can be said about the tensions on the two sides?', 'they are equal', 'Light string over a smooth pulley.', ['the heavier side has more tension', 'they add up to the total weight', 'the lighter side has zero tension']),
    ('Particles of masses 3 kg and 2 kg hang over a smooth pulley. What is the magnitude of their acceleration (g = 10)?', '2 m s⁻²', 'a = (3 − 2)(10)/5.', ['10 m s⁻²', '5 m s⁻²', '1 m s⁻²']),
])
p162.fixed('C2', (2, 3), [
    ('Explain why the tension in the string over a pulley is less than the weight of the heavier particle but more than the weight of the lighter one.', 'The heavier particle accelerates downwards, so its weight exceeds T; the lighter accelerates upwards, so T exceeds its weight.', 'B1 heavier: mg > T; B1 lighter: T > mg [2]'),
])


@p162.add('C1', (1, 2, 3))
def p162_c1(r, D):
    if D <= 2:
        d = pulley_v(r)
        return MC(r, f'Particles of masses {d["m1"]} kg and {d["m2"]} kg are connected by a light inextensible string over a smooth fixed pulley and released from rest. Find the magnitude of the acceleration.', f'{u3(d["a"])} {MS2}',
                  [f'{u3(Fr((d["m1"] - d["m2"]) * G, d["m1"]))} {MS2}', f'{u3(Fr((d["m1"] + d["m2"]) * G, d["m1"] - d["m2"]))} {MS2}', f'{G} {MS2}', f'{u3(d["a"] / 2)} {MS2}'], 'a = (m₁ − m₂)g/(m₁ + m₂).')
    d = pulley_t(r)
    if not d:
        return None
    return MC(r, f'A block of mass {d["m1"]} kg on a rough horizontal table (μ = {u3(d["mu"])}) is connected by a light string over a smooth pulley at the edge to a particle of mass {d["m2"]} kg hanging freely. Find the acceleration.', f'{u3(d["a"])} {MS2}',
              [f'{u3(Fr(d["m2"] * G, d["m1"] + d["m2"]))} {MS2}', f'{u3((d["m2"] * G - d["mu"] * d["m1"] * G) / d["m1"])} {MS2}', f'{u3((d["m2"] * G + d["mu"] * d["m1"] * G) / (d["m1"] + d["m2"]))} {MS2}', f'{u3(d["a"] * 2)} {MS2}'],
              'm₂g − μm₁g = (m₁ + m₂)a.')


@p162.add('C2', (1, 2, 3, 4), 'explain')
def p162_err(r, D):
    nm = person(r)
    d = pulley_v(r)
    f = r.choice(['Tw', 'sum', 'peg'])
    if f == 'Tw':
        return Q(f'Particles of masses {d["m1"]} kg and {d["m2"]} kg hang over a smooth pulley. {nm} says the tension in the string is {d["m2"] * G} N, the weight of the lighter particle. Explain the error and find the tension.',
                 f'The lighter particle accelerates upwards, so T > {d["m2"] * G}: T − {d["m2"] * G} = {d["m2"] if d["m2"] != 1 else ""}a with a = {u3(d["a"])}, giving T = {u3(d["T"])} N.', 'B1 particle accelerates so T ≠ weight; B1 correct T')
    if f == 'sum':
        return Q(f'For particles of masses {d["m1"]} kg and {d["m2"]} kg hanging over a smooth pulley, {nm} says the force on the pulley from the string is {(d["m1"] + d["m2"]) * G} N. Explain why this is wrong.',
                 f'The force on the pulley is 2T = {u3(2 * d["T"])} N, which is less than the total weight because the system is accelerating.', 'B1 force is 2T; B1 value')
    return Q(f'Explain the modelling assumptions made when particles of masses {d["m1"]} kg and {d["m2"]} kg hang over a smooth peg and the acceleration is found as {u3(d["a"])} {MS2}.',
             'The string is light and inextensible (same tension, same acceleration magnitude), the peg is smooth (tension the same on both sides), the particles are point masses, and air resistance is ignored.', 'B1 string assumptions; B1 smooth peg and particles')


@p162.add('C3', (1, 2, 3, 4, 5), 'numerical')
def p162_calc(r, D):
    if D <= 2:
        d = pulley_v(r)
        return Q(f'Particles A and B, of masses {d["m1"]} kg and {d["m2"]} kg, are connected by a light inextensible string passing over a smooth fixed pulley. The system is released from rest. Find the acceleration of the particles and the tension in the string.',
                 f'{u3(d["a"])} {MS2}; {u3(d["T"])} N', 'M1 N2L for each particle; A1 a; A1 T')
    d = pulley_t(r, D >= 4)
    if not d:
        return None
    rough = f'rough horizontal table (μ = {u3(d["mu"])})' if d['mu'] else 'smooth horizontal table'
    if D <= 4:
        return Q(f'A block of mass {d["m1"]} kg lies on a {rough} and is attached by a light inextensible string passing over a smooth pulley at the edge of the table to a particle of mass {d["m2"]} kg, which hangs freely. Find the acceleration and the tension.',
                 f'{u3(d["a"])} {MS2}; {u3(d["T"])} N', 'M1 N2L for the block; M1 N2L for the hanging particle; A1 a; A1 T')
    h = r.choice([1, 2, Fr(3, 2), Fr(1, 2)])
    v = math.sqrt(2 * float(d['a']) * float(h))
    return Q(f'A block of mass {d["m1"]} kg lies on a {rough}, attached by a light inextensible string over a smooth pulley at the edge to a particle of mass {d["m2"]} kg hanging {u3(h)} m above the floor. The system is released from rest. Find the speed of the particle when it hits the floor.',
             f'{n3(v)} {MS}', 'M1 equations of motion; A1 a; M1 v² = 2as; A1 speed')


def p162_c4(r, D):
    d = pulley_v(r)
    h = r.choice([1, 2, 3, Fr(1, 2), Fr(3, 2)])
    v = math.sqrt(2 * float(d['a']) * float(h))
    extra = v * v / (2 * G)
    intro = f'Particles A and B, of masses {d["m1"]} kg and {d["m2"]} kg, are attached to the ends of a light inextensible string passing over a smooth fixed pulley. A is {u3(h)} m above the ground, B is well below the pulley, and the system is released from rest with the string taut.'
    parts = [
        P('Find the acceleration of the particles.', f'{u3(d["a"])} {MS2}', 'M1 N2L for each; A1 a'),
        P('Find the tension in the string.', f'{u3(d["T"])} N', 'B1 T'),
        P('Find the speed of A when it reaches the ground.', f'{n3(v)} {MS}', 'M1 v² = 2as; A1 speed'),
        P('Find the force exerted on the pulley by the string.', f'{u3(2 * d["T"])} N', 'B1 2T'),
    ]
    return cmp_(r, intro, parts)


p162.add('C4', (2, 3, 4, 5))(p162_c4)


# ---------------------------------------------------------------- 16.3 string slack or broken

s163 = T('Motion after a string becomes slack or breaks', 'string becomes slack', 'string breaks')
s163.fixed('C1', (1, 2), [
    ('A string connecting two particles becomes slack. What is the tension?', 'zero', 'A slack string exerts no force.', ['unchanged', 'equal to the weight of the lighter particle', 'doubled']),
    ('After the hanging particle in a table-pulley system hits the floor, what happens to the block on the smooth table?', 'it continues at constant speed', 'No horizontal force acts once the string is slack.', ['it stops immediately', 'it decelerates at g', 'it accelerates at g']),
])
s163.fixed('C2', (2, 3), [
    ('Explain why, after the heavier particle in a pulley system hits the ground, the lighter particle continues to rise.', 'The string goes slack, so the lighter particle moves freely under gravity; it has upward velocity at that instant and decelerates at g until it stops.', 'B1 string slack; B1 moves freely under gravity with upward velocity [2]'),
])


@s163.add('C1', (1, 2, 3))
def s163_c1(r, D):
    d = pulley_v(r)
    h = r.choice([1, 2, 3, 4])
    v = math.sqrt(2 * float(d['a']) * h)
    if D <= 2:
        return MC(r, f'Particles of masses {d["m1"]} kg and {d["m2"]} kg hang over a smooth pulley. After the heavier one hits the ground, the lighter one is moving upwards at {n3(v)} {MS}. What is its acceleration now?', f'{G} {MS2} downwards',
                  [f'{u3(d["a"])} {MS2} downwards', 'zero', f'{u3(d["a"])} {MS2} upwards'], 'The string is slack; only gravity acts.')
    up = v * v / (2 * G)
    return MC(r, f'After a string becomes slack, a particle is moving vertically upwards at {n3(v)} {MS} under gravity alone. Find the further height it rises.', f'{n3(up)} m', [f'{n3(v / G)} m', f'{n3(2 * up)} m', f'{n3(up / 2)} m'], 'v² = u² − 2gs.')


@s163.add('C2', (1, 2, 3, 4), 'explain')
def s163_err(r, D):
    nm = person(r)
    d = pulley_t(r, False)
    if not d:
        return None
    h = r.choice([1, 2, Fr(1, 2)])
    v = math.sqrt(2 * float(d['a']) * float(h))
    f = r.choice(['stop', 'same', 'slackdown'])
    if f == 'stop':
        return Q(f'A block on a smooth table is pulled by a string over a pulley by a falling particle, which hits the floor after falling {u3(h)} m. {nm} says the block stops when the particle hits the floor. Explain the error.',
                 f'The string goes slack but the block has speed {n3(v)} {MS}; on a smooth table no horizontal force acts, so it continues at that speed.', 'B1 string slack, no force; B1 continues at constant speed')
    if f == 'same':
        return Q(f'In a pulley system the heavier particle hits the floor. {nm} assumes the lighter particle keeps the same acceleration {u3(d["a"])} {MS2} afterwards. Explain why this is wrong.',
                 'Once the string is slack the tension is zero, so the only force on the lighter particle is its weight: its acceleration is g downwards.', 'B1 tension zero; B1 acceleration g')
    return Q(f'Explain why, in a pulley problem, the string may become taut again some time after the heavier particle hits the floor.', 'The lighter particle rises freely and falls back; when it returns to the position where the string went slack, the string becomes taut again (a jerk occurs).',
             'B1 particle falls back; B1 string taut when it returns')


@s163.add('C3', (1, 2, 3, 4, 5), 'numerical')
def s163_calc(r, D):
    if D <= 2:
        d = pulley_v(r)
        h = r.choice([1, 2, 3, Fr(1, 2)])
        v = math.sqrt(2 * float(d['a']) * float(h))
        up = v * v / (2 * G)
        return Q(f'Particles of masses {d["m1"]} kg and {d["m2"]} kg are connected by a light string over a smooth pulley. The heavier particle starts {u3(h)} m above the ground and the system is released from rest. Find the greatest height of the lighter particle above its starting point (assume it does not reach the pulley).',
                 f'{n3(float(h) + up)} m', 'M1 acceleration; M1 speed when the string slackens; M1 further rise v²/2g; A1 total height')
    d = pulley_t(r, D >= 4)
    if not d:
        return None
    h = r.choice([1, 2, Fr(1, 2), Fr(3, 2)])
    v = math.sqrt(2 * float(d['a']) * float(h))
    if d['mu'] == 0:
        L = r.choice([2, 3, 4, 5])
        t = L / v
        return Q(f'A block of mass {d["m1"]} kg on a smooth horizontal table is connected by a light string over a smooth pulley at the edge to a particle of mass {d["m2"]} kg, which is {u3(h)} m above the floor. The block is initially {u3(float(h) + L)} m from the pulley. Find the time from when the particle hits the floor to when the block reaches the pulley.',
                 f'{n3(t)} s', 'M1 acceleration; M1 speed when the particle lands; M1 constant speed; A1 time')
    dec = float(d['mu']) * G
    s = v * v / (2 * dec)
    return Q(f'A block of mass {d["m1"]} kg on a rough horizontal table (μ = {u3(d["mu"])}) is connected by a light string over a smooth pulley at the edge to a particle of mass {d["m2"]} kg, which is {u3(h)} m above the floor. The system is released from rest and the block does not reach the pulley. Find the total distance moved by the block.',
             f'{n3(float(h) + s)} m', 'M1 acceleration; A1 speed when the particle lands; M1 deceleration μg; A1 total distance')


def s163_c4(r, D):
    d = pulley_t(r, True)
    if not d:
        return None
    h = r.choice([1, 2, Fr(1, 2), Fr(3, 2)])
    v = math.sqrt(2 * float(d['a']) * float(h))
    dec = float(d['mu']) * G
    s = v * v / (2 * dec)
    intro = f'A block of mass {d["m1"]} kg on a rough horizontal table (μ = {u3(d["mu"])}) is connected by a light inextensible string over a smooth pulley at the edge of the table to a particle of mass {d["m2"]} kg hanging {u3(h)} m above the floor. The system is released from rest.'
    parts = [
        P('Find the acceleration of the system and the tension in the string.', f'{u3(d["a"])} {MS2}; {u3(d["T"])} N', 'M1 N2L for each; A1 a; A1 T'),
        P('Find the speed of the particle when it hits the floor.', f'{n3(v)} {MS}', 'M1 v² = 2as; A1 speed'),
        P('Find the further distance the block travels before it comes to rest, assuming it does not reach the pulley.', f'{n3(s)} m', 'M1 deceleration μg; A1 distance'),
    ]
    return cmp_(r, intro, parts)


s163.add('C4', (2, 3, 4, 5))(s163_c4)

CHAPTERS[16] = [c161, p162, s163]


# ================================================================ Chapter 17 General motion in a straight line

def pint(p):
    """Antiderivative (high to low) with zero constant."""
    n = len(p)
    return ptrim([Fr(c) / (n - i) for i, c in enumerate(p)] + [Fr(0)])


def var_case(r, D):
    """v = k(t − p)(t − q) with 0 ≤ p < q; s(0) = s0."""
    k = r.choice([1, 2, 3, 6, -1, -2, -3, -6] if D >= 3 else [3, 6, -3, -6, 1, 2])
    p = r.choice([0, 1, 2]) if D <= 2 else r.choice([0, 1, 2, 3])
    q = p + r.choice([1, 2, 3, 4, 5])
    v = pmul([k], pmul([1, -p], [1, -q]))
    s0 = r.choice([0, 0, 2, 5]) if D >= 4 else 0
    s = padd(pint(v), [s0])
    a = deriv_p(v)
    f = lambda t: float(pval(s, Fr(t)))
    if not ok(ndiff(f, 1.3), float(pval(v, Fr(13, 10))), 'var s→v', 1e-5):
        return None
    return dict(k=k, p=p, q=q, v=v, s=s, a=a, s0=s0)


def pt_(p):
    return pstr(p, 't')


v171 = T('Variable acceleration: differentiating displacement and velocity with respect to time', 'variable acceleration', 'differentiating displacement')
v171.fixed('C1', (1, 2), [
    ('If s = t³ − 4t, what is the velocity v?', '3t² − 4', 'v = ds/dt.', ['t⁴/4 − 2t²', '6t', '3t² − 4t']),
    ('If v = 5t² + 2t, what is the acceleration a?', '10t + 2', 'a = dv/dt.', ['5t³/3 + t²', '10t', '5t + 2']),
    ('A particle has velocity v. When is it instantaneously at rest?', 'when v = 0', 'At rest means zero velocity.', ['when a = 0', 'when s = 0', 'when t = 0 only']),
])
v171.fixed('C2', (2, 3), [
    ('Explain why the suvat equations cannot be used when s = t³ − 6t².', 'The acceleration a = d²s/dt² = 6t − 12 is not constant, so the constant-acceleration equations do not apply; calculus must be used.', 'B1 a varies with t; B1 use calculus [2]'),
])


@v171.add('C1', (1, 2, 3))
def v171_c1(r, D):
    d = var_case(r, D)
    if not d:
        return None
    if D == 1:
        return MC(r, f'A particle moves in a straight line with displacement s = {pt_(d["s"])} m at time t s. Find an expression for its velocity.', f'v = {pt_(d["v"])}',
                  [f'v = {pt_(d["a"])}', f'v = {pt_(pint(d["s"]))}', f'v = {pt_(padd(d["v"], [0, 1, 0]))}' if len(d["v"]) == 3 else 'v = t'], 'v = ds/dt.')
    if D == 2:
        t = r.choice([1, 2, 3, 4])
        return MC(r, f'A particle has velocity v = {pt_(d["v"])} m s⁻¹ at time t s. Find its acceleration when t = {t}.', f'{num(pval(d["a"], t))} {MS2}',
                  [f'{num(pval(d["v"], t))} {MS2}', f'{num(pval(d["a"], t) + d["k"])} {MS2}', f'{num(pval(pint(d["v"]), t))} {MS2}', f'{num(-pval(d["a"], t))} {MS2}' if pval(d['a'], t) else '1 m s⁻²'],
                  'a = dv/dt, then substitute.')
    return MC(r, f'A particle has velocity v = {pt_(d["v"])} m s⁻¹ at time t s. At which times is it instantaneously at rest?', f't = {d["p"]} and t = {d["q"]}' if d['p'] else f't = 0 and t = {d["q"]}',
              [f't = {num(Fr(d["p"] + d["q"], 2))}', f't = {d["q"]} only', f't = {-d["q"]} and t = {-d["p"]}' if d['p'] else f't = {-d["q"]} and t = 0', f't = {d["p"] + d["q"]}'], 'Solve v = 0.')


@v171.add('C2', (1, 2, 3, 4), 'explain')
def v171_err(r, D):
    nm = person(r)
    d = var_case(r, max(2, D))
    if not d:
        return None
    f = r.choice(['suvat', 'arest', 'speed'])
    tm = Fr(d['p'] + d['q'], 2)
    if f == 'suvat':
        t = r.choice([2, 3, 4])
        return Q(f'A particle has velocity v = {pt_(d["v"])} m s⁻¹. {nm} uses v = u + at to find the acceleration over the first {t} s. Explain why this does not give the acceleration at t = {t}.',
                 f'The acceleration varies (a = {pt_(d["a"])}), so (v − u)/t gives only an average; at t = {t} the acceleration is {num(pval(d["a"], t))} {MS2}.', 'B1 acceleration not constant; B1 differentiates to find a at t')
    if f == 'arest':
        return Q(f'A particle has velocity v = {pt_(d["v"])} m s⁻¹. {nm} says the particle is at rest at t = {num(tm)} because the acceleration is zero then. Explain the error.',
                 f'a = 0 at t = {num(tm)} means the velocity is stationary (here the {"least" if d["k"] > 0 else "greatest"} velocity, {num(pval(d["v"], tm))} {MS}), not zero; it is at rest when v = 0, at t = {d["p"]} and t = {d["q"]}.',
                 'B1 a = 0 gives stationary velocity; B1 at rest when v = 0')
    t = r.choice([x for x in range(d['p'] + 1, d['q']) ] or [Fr(d['p'] + d['q'], 2)])
    return Q(f'A particle has velocity v = {pt_(d["v"])} m s⁻¹. Explain the difference between its velocity and its speed at t = {num(t)}.',
             f'v = {num(pval(d["v"], t))} {MS}: the sign gives the direction; the speed is the magnitude, {num(abs(pval(d["v"], t)))} {MS}.', 'B1 velocity value with sign; B1 speed is the magnitude')


@v171.add('C3', (1, 2, 3, 4, 5), 'numerical')
def v171_calc(r, D):
    d = var_case(r, D)
    if not d:
        return None
    if D <= 2:
        t = r.choice([1, 2, 3, 4, 5])
        return Q(f'A particle moves in a straight line so that its displacement from O at time t s is s = {pt_(d["s"])} m. Find its velocity and acceleration when t = {t}.', f'{num(pval(d["v"], t))} {MS}; {num(pval(d["a"], t))} {MS2}',
                 'M1 differentiates; A1 v; M1 differentiates again; A1 a')
    if D <= 4:
        return Q(f'A particle moves in a straight line so that its displacement from O at time t s is s = {pt_(d["s"])} m. Find the times when the particle is at rest and its acceleration at each of these times.',
                 f't = {d["p"]}: a = {num(pval(d["a"], d["p"]))} {MS2}; t = {d["q"]}: a = {num(pval(d["a"], d["q"]))} {MS2}', 'M1 v = ds/dt; M1 solves v = 0; A1 times; A1 accelerations')
    tm = Fr(d['p'] + d['q'], 2)
    return Q(f'A particle moves in a straight line with displacement s = {pt_(d["s"])} m at time t s. Find the {"minimum" if d["k"] > 0 else "maximum"} velocity of the particle and the displacement at that instant.',
             f'{num(pval(d["v"], tm))} {MS}; {u3(pval(d["s"], tm))} m', 'M1 a = 0; A1 time; A1 velocity; A1 displacement')


def v171_c4(r, D):
    d = var_case(r, D)
    if not d:
        return None
    tm = Fr(d['p'] + d['q'], 2)
    intro = f'A particle P moves in a straight line. Its displacement from a fixed point O at time t s is s = {pt_(d["s"])} m.'
    parts = [
        P('Find an expression for the velocity of P.', f'v = {pt_(d["v"])}', 'M1 differentiates; A1 v'),
        P('Find the values of t when P is instantaneously at rest.', f't = {d["p"]} and t = {d["q"]}', 'M1 v = 0; A1 both'),
        P('Find the acceleration of P at each instant when it is at rest.', f'{num(pval(d["a"], d["p"]))} {MS2} and {num(pval(d["a"], d["q"]))} {MS2}', 'M1 differentiates again; A1 both'),
        P(f'Find the displacement of P when t = {d["q"]}.', f'{u3(pval(d["s"], d["q"]))} m', 'B1 value'),
    ]
    return cmp_(r, intro, parts)


v171.add('C4', (2, 3, 4, 5))(v171_c4)


# ---------------------------------------------------------------- 17.2 integrating

i172 = T('Integrating acceleration and velocity and using initial conditions', 'integrating acceleration', 'initial conditions', 'integrating velocity')
i172.fixed('C1', (1, 2), [
    ('If a = 6t and v = 2 when t = 0, what is v?', '3t² + 2', 'v = ∫ a dt with the constant from v(0) = 2.', ['3t²', '6', '6t + 2']),
    ('Which expression gives the displacement between t = 1 and t = 3 when the velocity is v?', '∫₁³ v dt', 'Displacement is the integral of velocity.', ['v(3) − v(1)', '∫₁³ a dt', 'dv/dt at t = 3']),
])
i172.fixed('C2', (2, 3), [
    ('Explain why a constant of integration must be found when obtaining v from a.', 'Integration gives a family of velocity functions differing by a constant; the initial velocity selects the particular one.', 'B1 family of functions; B1 fixed by the initial condition [2]'),
])


def acc_case(r, D):
    a2 = r.choice([0, 0, 3, -3, 6]) if D >= 3 else 0
    a1 = r.choice([2, 4, 6, -2, -4, 1])
    a0 = r.randint(-5, 6)
    a = ptrim([a2, a1, a0])
    u = r.randint(0, 8)
    v = padd(pint(a), [u])
    s = pint(v)
    return dict(a=a, u=u, v=v, s=s)


@i172.add('C1', (1, 2, 3))
def i172_c1(r, D):
    d = acc_case(r, D)
    if D <= 2:
        return MC(r, f'A particle has acceleration a = {pt_(d["a"])} m s⁻² and initial velocity {d["u"]} {MS}. Find its velocity at time t.', f'v = {pt_(d["v"])}',
                  [f'v = {pt_(pint(d["a"]))}' if d['u'] else f'v = {pt_(padd(pint(d["a"]), [1]))}', f'v = {pt_(deriv_p(d["a"]))}' if len(d['a']) > 1 else 'v = 0', f'v = {pt_(padd(d["a"], [d["u"]]))}'], 'Integrate and use the initial velocity.')
    t = r.choice([1, 2, 3])
    return MC(r, f'A particle starts from O with velocity v = {pt_(d["v"])} m s⁻¹. Find its displacement from O when t = {t}.', f'{u3(pval(d["s"], t))} m',
              [f'{u3(pval(d["v"], t))} m', f'{u3(pval(d["a"], t))} m', f'{u3(pval(d["s"], t) + d["u"])} m' if d['u'] else f'{u3(pval(d["s"], t) + 1)} m', f'{u3(2 * pval(d["s"], t))} m'], 's = ∫ v dt with s(0) = 0.')


@i172.add('C2', (1, 2, 3, 4), 'explain')
def i172_err(r, D):
    nm = person(r)
    d = acc_case(r, D)
    f = r.choice(['noc', 'diff', 'limits'])
    if f == 'noc' and d['u']:
        return Q(f'A particle has acceleration a = {pt_(d["a"])} m s⁻² and starts with velocity {d["u"]} {MS}. {nm} writes v = {pt_(pint(d["a"]))}. Explain the error.',
                 f'{nm} has omitted the constant of integration; using v = {d["u"]} at t = 0 gives v = {pt_(d["v"])}.', 'B1 constant omitted; B1 correct v')
    if f == 'diff':
        return Q(f'A particle has velocity v = {pt_(d["v"])} m s⁻¹. To find its displacement, {nm} differentiates v. Explain the error.',
                 f'Differentiating v gives the acceleration; displacement is found by integrating: s = {pt_(d["s"])} (if s = 0 at t = 0).', 'B1 differentiation gives acceleration; B1 integrate for displacement')
    t1, t2 = 1, r.choice([2, 3, 4])
    return Q(f'Explain how to find the displacement of a particle with velocity v = {pt_(d["v"])} m s⁻¹ between t = {t1} and t = {t2}, and find it.',
             f'Integrate v between the limits: s = [{pt_(d["s"])}] from {t1} to {t2} = {u3(pval(d["s"], t2) - pval(d["s"], t1))} m.', 'M1 definite integral; A1 value')


@i172.add('C3', (1, 2, 3, 4, 5), 'numerical')
def i172_calc(r, D):
    d = acc_case(r, D)
    t = r.choice([2, 3, 4, 5])
    if D <= 2:
        return Q(f'A particle starts from O {"from rest" if d["u"] == 0 else "with velocity " + str(d["u"]) + " " + MS} and moves with acceleration a = {pt_(d["a"])} m s⁻² at time t s. Find its velocity when t = {t}.', f'{u3(pval(d["v"], t))} {MS}',
                 'M1 integrates; M1 uses the initial velocity; A1 value')
    if D <= 4:
        return Q(f'A particle starts from O {"from rest" if d["u"] == 0 else "with velocity " + str(d["u"]) + " " + MS} and moves with acceleration a = {pt_(d["a"])} m s⁻² at time t s. Find its displacement from O when t = {t}.', f'{u3(pval(d["s"], t))} m',
                 'M1 integrates a; A1 v; M1 integrates v; A1 s')
    # given v at a later time, find unknown initial velocity
    vt = pval(d['v'], t)
    return Q(f'A particle moves with acceleration a = {pt_(d["a"])} m s⁻² at time t s. Its velocity when t = {t} is {u3(vt)} {MS}. Find its initial velocity and its displacement from its starting point when t = {t}.',
             f'{d["u"]} {MS}; {u3(pval(d["s"], t))} m', 'M1 integrates with constant; A1 initial velocity; M1 integrates again; A1 displacement')


def i172_c4(r, D):
    d = acc_case(r, D)
    t = r.choice([2, 3, 4])
    intro = f'A particle P moves in a straight line, starting from O {"from rest" if d["u"] == 0 else "with velocity " + str(d["u"]) + " " + MS}. Its acceleration at time t s is a = {pt_(d["a"])} m s⁻².'
    parts = [
        P('Find an expression for the velocity of P.', f'v = {pt_(d["v"])}', 'M1 integrates; A1 v'),
        P(f'Find the velocity of P when t = {t}.', f'{u3(pval(d["v"], t))} {MS}', 'B1 value'),
        P('Find an expression for the displacement of P from O.', f's = {pt_(d["s"])}', 'M1 integrates; A1 s'),
        P(f'Find the displacement of P from O when t = {t}.', f'{u3(pval(d["s"], t))} m', 'B1 value'),
    ]
    return cmp_(r, intro, parts)


i172.add('C4', (2, 3, 4, 5))(i172_c4)


# ---------------------------------------------------------------- 17.3 maximum values and total distance

def tot_dist(v, a, b, roots):
    """∫ₐᵇ |v| dt exactly, given the real roots of v."""
    S = pint(v)
    pts_ = [Fr(a)] + sorted(Fr(x) for x in roots if a < x < b) + [Fr(b)]
    return float(sum(abs(pval(S, y) - pval(S, x)) for x, y in zip(pts_, pts_[1:])))


m173 = T('Maximum displacement, velocity and total distance travelled', 'maximum displacement', 'total distance travelled', 'maximum velocity')
m173.fixed('C1', (1, 2), [
    ('At the instant when a particle has its maximum displacement from O (not at an end point), what is its velocity?', 'zero', 'ds/dt = 0 at a stationary value of s.', ['a maximum', 'equal to its acceleration', 'negative']),
    ('At the instant when a particle has its maximum velocity, what is its acceleration?', 'zero', 'dv/dt = 0 at a stationary value of v.', ['a maximum', 'equal to g', 'the same as its velocity']),
])
m173.fixed('C2', (2, 3), [
    ('Explain why ∫₀ᵀ v dt may not give the distance travelled in the first T seconds.', 'If the particle changes direction, parts of the integral are negative and cancel; the distance requires integrating |v|, splitting at the times when v = 0.', 'B1 direction change makes the integral smaller; B1 split at v = 0 [2]'),
])


@m173.add('C1', (1, 2, 3))
def m173_c1(r, D):
    d = var_case(r, D + 1)
    if not d:
        return None
    if D <= 2:
        return MC(r, f'A particle has velocity v = {pt_(d["v"])} m s⁻¹. At what time does it have its {"least" if d["k"] > 0 else "greatest"} velocity?', f't = {num(Fr(d["p"] + d["q"], 2))}',
                  [f't = {d["q"]}', f't = {d["p"] + d["q"]}', f't = {num(Fr(d["q"], 2))}' if d['p'] else f't = {d["q"] * 2}', 't = 0' if d['p'] else f't = {d["q"] + 1}'], 'Solve a = dv/dt = 0.')
    return MC(r, f'A particle starts from O with velocity v = {pt_(d["v"])} m s⁻¹. At what time is its displacement from O stationary for the second time (t > 0)?', f't = {d["q"]}',
              [f't = {num(Fr(d["p"] + d["q"], 2))}', f't = {d["p"] + d["q"]}', f't = {d["q"] + 1}', f't = {num(Fr(3 * d["q"], 2))}'], 'Displacement is stationary when v = 0.') if d['p'] else None


@m173.add('C2', (1, 2, 3, 4), 'explain')
def m173_err(r, D):
    nm = person(r)
    d = var_case(r, max(2, D))
    if not d:
        return None
    T_ = d['q'] + r.choice([1, 2])
    net = pval(d['s'], T_) - pval(d['s'], 0)
    td = tot_dist(d['v'], 0, T_, (d['p'], d['q']))
    f = r.choice(['net', 'maxd'])
    if f == 'net' and abs(float(net) - td) > 1e-6:
        return Q(f'A particle has velocity v = {pt_(d["v"])} m s⁻¹. {nm} finds the distance travelled in the first {T_} s as ∫₀^{T_} v dt = {u3(net)} m. Explain the error and find the correct distance.',
                 f'The particle changes direction at t = {d["q"]}{" (and t = " + str(d["p"]) + ")" if d["p"] else ""}; splitting the integral there and adding magnitudes gives {u3(td)} m.', 'B1 direction change; M1 splits the integral; A1 distance')
    tm = d['q'] if d['k'] < 0 else d['p']
    return Q(f'A particle starts at O with velocity v = {pt_(d["v"])} m s⁻¹. Explain how to find the greatest displacement from O in the positive direction during the first {d["q"] + 2} s.',
             'Find s by integrating, find the times when v = 0, and compare s at those times and at the end points; the largest value is the greatest displacement.', 'B1 s at v = 0; B1 checks end points')


@m173.add('C3', (1, 2, 3, 4, 5), 'numerical')
def m173_calc(r, D):
    d = var_case(r, D)
    if not d:
        return None
    tm = Fr(d['p'] + d['q'], 2)
    if D <= 2:
        return Q(f'A particle has velocity v = {pt_(d["v"])} m s⁻¹ at time t s. Find the {"minimum" if d["k"] > 0 else "maximum"} value of v.', f'{u3(pval(d["v"], tm))} {MS}', 'M1 a = 0; A1 time; A1 value')
    if D == 3:
        return Q(f'A particle starts from O and has velocity v = {pt_(d["v"])} m s⁻¹ at time t s. Find the displacement of the particle from O at each instant when it is at rest.',
                 f't = {d["p"]}: {u3(pval(d["s"], d["p"]))} m; t = {d["q"]}: {u3(pval(d["s"], d["q"]))} m', 'M1 integrates; M1 v = 0; A1 A1')
    T_ = d['q'] + r.choice([1, 2])
    td = tot_dist(d['v'], 0, T_, (d['p'], d['q']))
    # numerical check
    if not ok(td, simpson(lambda t: abs(float(pval(d['v'], Fr(t)))), 0, T_, 4000), 'total distance', 1e-4):
        return None
    return Q(f'A particle starts from O and has velocity v = {pt_(d["v"])} m s⁻¹ at time t s. Find the total distance travelled in the first {T_} s.', f'{u3(td)} m',
             'M1 times when v = 0; M1 splits the integral; M1 integrates; A1 total distance')


def m173_c4(r, D):
    d = var_case(r, max(3, D))
    if not d or d['p'] == 0:
        return None
    T_ = d['q'] + 1
    td = tot_dist(d['v'], 0, T_, (d['p'], d['q']))
    tm = Fr(d['p'] + d['q'], 2)
    intro = f'A particle P starts from O and moves in a straight line with velocity v = {pt_(d["v"])} m s⁻¹ at time t s.'
    parts = [
        P('Find the times when P is instantaneously at rest.', f't = {d["p"]} and t = {d["q"]}', 'M1 v = 0; A1 both'),
        P(f'Find the {"minimum" if d["k"] > 0 else "maximum"} velocity of P.', f'{u3(pval(d["v"], tm))} {MS}', 'M1 a = 0; A1 value'),
        P(f'Find the displacement of P from O when t = {d["q"]}.', f'{u3(pval(d["s"], d["q"]))} m', 'M1 integrates; A1 value'),
        P(f'Find the total distance travelled by P in the first {T_} s.', f'{u3(td)} m', 'M1 splits at the turning points; A1 total'),
    ]
    return cmp_(r, intro, parts)


m173.add('C4', (2, 3, 4, 5))(m173_c4)

CHAPTERS[17] = [v171, i172, m173]


# ================================================================ Chapter 18 Momentum

MASSES = [Fr(1, 10), Fr(1, 5), Fr(1, 4), Fr(1, 2), 1, 2, 3, 4, 5, 6, 8]


def kg(m):
    return f'{u3(m)} kg'


def coll(r, D):
    """A (mA, uA) hits B (mB, uB); after: vA, vB (positive in A's original direction). Generated from a
    restitution coefficient so that kinetic energy never increases."""
    for _ in range(30):
        mA, mB = r.sample(MASSES[:9] if D >= 3 else [1, 2, 3, 4, 5, 6], 2)
        uA = r.choice([2, 3, 4, 5, 6, 8, 10])
        uB = r.choice([0, 0, 1, 2, -1, -2, -3]) if D >= 2 else 0
        if uB >= uA:
            continue
        e = r.choice([Fr(0), Fr(1, 4), Fr(1, 3), Fr(1, 2), Fr(2, 3), Fr(3, 4), Fr(1)])
        mA, mB = Fr(mA), Fr(mB)
        vA = (mA * uA + mB * uB - mB * e * (uA - uB)) / (mA + mB)
        vB = vA + e * (uA - uB)
        if (vA * 4).denominator != 1 or (vB * 4).denominator != 1 or e == 0:
            continue
        pin = mA * uA + mB * uB
        kin = Fr(1, 2) * (mA * uA ** 2 + mB * uB ** 2)
        kout = Fr(1, 2) * (mA * vA ** 2 + mB * vB ** 2)
        if kout > kin or not ok(float(mA * vA + mB * vB), float(pin), 'momentum'):
            continue
        return dict(mA=mA, mB=mB, uA=Fr(uA), uB=Fr(uB), vA=vA, vB=vB, loss=kin - kout)
    return None


def co(m):
    """Coefficient text: '' for 1."""
    return '' if m == 1 else u3(m)


def vel(v):
    return f'{u3(abs(v))} {MS}'


def dirn(v):
    return 'in its original direction' if v > 0 else ('at rest' if v == 0 else 'in the opposite direction')


mo181 = T('Momentum and impulse in one dimension', 'momentum', 'impulse')
mo181.fixed('C1', (1, 2), [
    ('What is the momentum of a 0.5 kg ball moving at 8 m s⁻¹?', '4 N s', 'Momentum = mv.', ['16 N s', '4 J', '0.0625 N s']),
    ('What are the units of impulse?', 'N s', 'Impulse = force × time = change in momentum.', ['N', 'J', 'N m']),
    ('A ball hits a wall and rebounds. Which quantity must change sign?', 'its velocity', 'Its direction reverses.', ['its mass', 'its speed', 'its kinetic energy']),
])
mo181.fixed('C2', (2, 3), [
    ('Explain why the impulse on a ball that rebounds from a wall is larger than the impulse on an identical ball that is brought to rest by the wall.', 'Impulse = change in momentum; reversing direction changes the momentum by m(v + u), while stopping changes it by only mu.', 'B1 impulse = change in momentum; B1 rebound has a larger change [2]'),
])


@mo181.add('C1', (1, 2, 3))
def mo181_c1(r, D):
    m = r.choice(MASSES)
    u = r.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20])
    if D == 1:
        return MC(r, f'Find the momentum of a particle of mass {kg(m)} moving at {u} {MS}.', f'{u3(m * u)} N s', [f'{u3(m * u * u / 2)} N s', f'{u3(Fr(u) / m)} N s', f'{u3(m + u)} N s', f'{u3(m * u * 2)} N s'], 'p = mv.')
    v = r.choice([1, 2, 3, 4, 5, 6])
    I_ = m * (u + v)
    return MC(r, f'A ball of mass {kg(m)} hits a wall at {u} {MS} and rebounds at {v} {MS}. Find the magnitude of the impulse on the ball.', f'{u3(I_)} N s',
              [f'{u3(m * abs(u - v))} N s' if u != v else f'{u3(m * u)} N s', f'{u3(m * u)} N s' if u != v else f'{u3(m * u * 3)} N s', f'{u3(m * (u * u - v * v) / 2)} N s' if u != v else f'{u3(m * 4 * u)} N s', f'{u3(2 * I_)} N s'], 'I = m(v − u) with the rebound velocity negative.')


@mo181.add('C2', (1, 2, 3, 4), 'explain')
def mo181_err(r, D):
    nm = person(r)
    m = r.choice(MASSES)
    u, v = r.choice([4, 5, 6, 8, 10]), r.choice([1, 2, 3, 4])
    f = r.choice(['sign', 'force', 'units'])
    if f == 'sign':
        return Q(f'A ball of mass {kg(m)} strikes a wall at {u} {MS} and rebounds at {v} {MS}. {nm} finds the impulse as {u3(m)} × ({u} − {v}) = {u3(m * (u - v))} N s. Explain the error.',
                 f'Velocities are vectors: taking the original direction as positive, the final velocity is −{v}, so the impulse is {co(m)}(−{v} − {u}) = −{u3(m * (u + v))} N s, magnitude {u3(m * (u + v))} N s.', 'B1 sign of the rebound velocity; B1 correct magnitude')
    if f == 'force':
        t = r.choice([Fr(1, 10), Fr(1, 20), Fr(1, 50), Fr(1, 100)])
        return Q(f'A ball of mass {kg(m)} hits a wall at {u} {MS} and rebounds at {v} {MS}, in contact for {u3(t)} s. Explain how to find the average force exerted by the wall and find it.',
                 f'Impulse = change in momentum = {u3(m * (u + v))} N s = F × {u3(t)}, so F = {u3(m * (u + v) / t)} N.', 'M1 impulse = Ft = change in momentum; A1 force')
    return Q(f'{nm} gives the momentum of a {kg(m)} particle moving at {u} {MS} as {u3(m * u)} J. Explain the error.', f'Momentum = mv is measured in N s (or kg m s⁻¹), not joules: {u3(m * u)} N s.', 'B1 correct unit; B1 joules are for energy')


@mo181.add('C3', (1, 2, 3, 4, 5), 'numerical')
def mo181_calc(r, D):
    m = r.choice(MASSES)
    if D <= 2:
        u = r.choice([2, 4, 5, 6, 8])
        I_ = r.choice([1, 2, 3, 4, 5, 6])
        v = u + Fr(I_) / m
        return Q(f'A particle of mass {kg(m)} moving at {u} {MS} receives an impulse of {I_} N s in its direction of motion. Find its new speed.', vel(v), 'M1 I = m(v − u); A1 speed')
    if D <= 4:
        I_ = r.choice([2, 3, 4, 5, 6])
        u = r.choice([2, 3, 4, 5])
        v = u - Fr(I_) / m
        return Q(f'A particle of mass {kg(m)} moving at {u} {MS} receives an impulse of magnitude {I_} N s opposite to its direction of motion. Find its velocity afterwards, stating its direction.', f'{vel(v)} {dirn(v)}', 'M1 I = m(v − u) with signs; A1 speed; A1 direction')
    h1, h2 = r.choice([5, 10, 20, Fr(5, 4)]), r.choice([Fr(5, 4), Fr(9, 5), Fr(16, 5), 5])
    u = math.sqrt(2 * G * float(h1))
    v = math.sqrt(2 * G * float(h2))
    if h2 >= h1:
        return None
    return Q(f'A ball of mass {kg(m)} is dropped from a height of {u3(h1)} m onto a horizontal floor and rebounds to a height of {u3(h2)} m. Find the magnitude of the impulse exerted by the floor.', f'{n3(float(m) * (u + v))} N s',
             'M1 speed before impact; M1 speed after impact; M1 impulse = change in momentum; A1 value')


def mo181_c4(r, D):
    m = r.choice([Fr(1, 10), Fr(1, 5), Fr(1, 2), Fr(1, 4)])
    h1 = r.choice([5, 10, 20])
    h2 = r.choice([Fr(5, 4), Fr(9, 5), Fr(16, 5), Fr(5, 2)])
    u = math.sqrt(2 * G * h1)
    v = math.sqrt(2 * G * float(h2))
    t = r.choice([Fr(1, 10), Fr(1, 20), Fr(1, 50)])
    I_ = float(m) * (u + v)
    intro = f'A ball of mass {kg(m)} is dropped from rest at a height of {h1} m above a horizontal floor. It rebounds vertically to a height of {u3(h2)} m.'
    parts = [
        P('Find the speed of the ball just before it hits the floor.', f'{n3(u)} {MS}', 'M1 v² = 2gh; A1 speed'),
        P('Find the speed of the ball just after it leaves the floor.', f'{n3(v)} {MS}', 'M1 uses the rebound height; A1 speed'),
        P('Find the magnitude of the impulse exerted on the ball by the floor.', f'{n3(I_)} N s', 'M1 change in momentum with signs; A1 value'),
        P(f'The ball is in contact with the floor for {u3(t)} s. Find the average force exerted by the floor (ignoring the weight during contact).', f'{n3(I_ / float(t))} N', 'M1 F = I/t; A1 force'),
    ]
    return cmp_(r, intro, parts)


mo181.add('C4', (2, 3, 4, 5))(mo181_c4)


# ---------------------------------------------------------------- 18.2 conservation of momentum

cm182 = T('Conservation of linear momentum in direct collisions', 'conservation of momentum', 'direct collisions')
cm182.fixed('C1', (1, 2), [
    ('In a collision between two particles with no external forces, which quantity is conserved?', 'total momentum', 'Internal forces are equal and opposite (third law).', ['total kinetic energy', 'each particle\'s momentum', 'each particle\'s speed']),
    ('In a collision the impulse on A is 6 N s to the right. What is the impulse on B?', '6 N s to the left', 'Newton\'s third law.', ['6 N s to the right', '0 N s', '12 N s to the left']),
])
cm182.fixed('C2', (2, 3), [
    ('Explain why momentum is conserved in a collision between two particles on a smooth surface but kinetic energy usually is not.', 'The impulses on the particles are equal and opposite, so total momentum is unchanged; some kinetic energy is converted to heat, sound or deformation, so it is usually lost.', 'B1 equal and opposite impulses; B1 energy converted to other forms [2]'),
])


@cm182.add('C1', (1, 2, 3))
def cm182_c1(r, D):
    d = coll(r, D)
    if not d:
        return None
    stem = f'A particle A of mass {kg(d["mA"])} moving at {u3(d["uA"])} {MS} collides directly with a particle B of mass {kg(d["mB"])}' + (' at rest' if d['uB'] == 0 else f' moving at {u3(abs(d["uB"]))} {MS} {"in the same direction" if d["uB"] > 0 else "towards A"}') + '.'
    return MC(r, stem + f' After the collision A moves at {u3(abs(d["vA"]))} {MS} {dirn(d["vA"]) if d["vA"] else ""}'.rstrip() + '. Find the speed of B after the collision.', vel(d['vB']),
              [vel((d['mA'] * d['uA'] + d['mB'] * d['uB'] + d['mA'] * d['vA']) / d['mB']), vel((d['mA'] * d['uA'] - d['mA'] * d['vA']) / d['mB']) if d['uB'] else vel(d['vB'] + 1), vel(d['uA'] - d['vA']), vel(d['vB'] * 2)],
              'Total momentum before = total momentum after.') if d['vA'] != 0 else MC(r, stem + ' A is brought to rest by the collision. Find the speed of B afterwards.', vel(d['vB']),
                                                                                     [vel(d['uA']), vel(d['mA'] * d['uA'] / (d['mA'] + d['mB'])), vel(d['vB'] * 2), vel(d['vB'] + 1)], 'Momentum is conserved.')


@cm182.add('C2', (1, 2, 3, 4), 'explain')
def cm182_err(r, D):
    nm = person(r)
    d = coll(r, max(2, D))
    if not d or d['uB'] >= 0:
        d = coll(r, 3)
    if not d:
        return None
    f = r.choice(['sign', 'ke', 'show'])
    if f == 'sign' and d['uB'] < 0:
        wrong = (d['mA'] * d['uA'] + d['mB'] * abs(d['uB']) - d['mA'] * d['vA']) / d['mB']
        return Q(f'A of mass {kg(d["mA"])} moving at {u3(d["uA"])} {MS} meets B of mass {kg(d["mB"])} moving at {u3(abs(d["uB"]))} {MS} towards A. {nm} writes the total momentum before as {u3(d["mA"] * d["uA"])} + {u3(d["mB"] * abs(d["uB"]))}. Explain the error.',
                 f'B moves in the opposite direction, so its velocity is −{u3(abs(d["uB"]))}; total momentum = {u3(d["mA"] * d["uA"])} − {u3(d["mB"] * abs(d["uB"]))} = {u3(d["mA"] * d["uA"] + d["mB"] * d["uB"])} N s.',
                 'B1 direction gives a negative velocity; B1 correct total')
    if f == 'ke':
        return Q(f'{nm} tries to find the velocities after a collision between A ({kg(d["mA"])}, {u3(d["uA"])} {MS}) and B ({kg(d["mB"])}, {"at rest" if d["uB"] == 0 else u3(d["uB"]) + " " + MS}) by assuming kinetic energy is conserved. Explain why this is usually not valid.',
                 f'Kinetic energy is generally lost in a collision (here {u3(d["loss"])} J would be lost if A moves at {u3(d["vA"])} {MS} afterwards); only momentum is conserved.', 'B1 KE not conserved in general; B1 only momentum')
    return Q(f'A of mass {kg(d["mA"])} moving at {u3(d["uA"])} {MS} collides with B of mass {kg(d["mB"])}' + (' at rest' if d['uB'] == 0 else f' moving at {u3(d["uB"])} {MS}') + f'. Afterwards A moves at {u3(d["vA"])} {MS}. Show that B then moves at {u3(d["vB"])} {MS}.',
             f'{u3(d["mA"] * d["uA"] + d["mB"] * d["uB"])} = {u3(d["mA"] * d["vA"])} + {co(d["mB"])}v, so v = {u3(d["vB"])}.', 'M1 conservation of momentum; A1 shown')


@cm182.add('C3', (1, 2, 3, 4, 5), 'numerical')
def cm182_calc(r, D):
    d = coll(r, D)
    if not d:
        return None
    stem = f'Particles A and B, of masses {kg(d["mA"])} and {kg(d["mB"])}, move along a straight line on a smooth horizontal surface. A moves at {u3(d["uA"])} {MS} and B ' + ('is at rest' if d['uB'] == 0 else f'moves at {u3(abs(d["uB"]))} {MS} {"in the same direction" if d["uB"] > 0 else "towards A"}') + '. They collide directly.'
    if D <= 2:
        return Q(stem + f' After the collision B moves at {u3(d["vB"])} {MS} in A\'s original direction. Find the velocity of A after the collision.', f'{vel(d["vA"])} {dirn(d["vA"])}' if d['vA'] else 'A is at rest', 'M1 conservation of momentum; A1 speed; A1 direction')
    if D <= 4:
        return Q((stem + f' After the collision A moves at {u3(abs(d["vA"]))} {MS} {dirn(d["vA"])}.' if d['vA'] else stem + ' A is at rest after the collision.') + ' Find the speed of B after the collision and the loss of kinetic energy.',
                            f'{vel(d["vB"])}; {u3(d["loss"])} J', 'M1 momentum; A1 B\'s speed; M1 KE before and after; A1 loss')
    # unknown mass
    return Q(f'A particle A of mass {kg(d["mA"])} moving at {u3(d["uA"])} {MS} collides with a particle B of mass m kg' + (' at rest' if d['uB'] == 0 else f' moving at {u3(abs(d["uB"]))} {MS} {"in the same direction" if d["uB"] > 0 else "towards A"}') +
             f'. After the collision A moves at {u3(abs(d["vA"]))} {MS} {dirn(d["vA"])} and B moves at {u3(d["vB"])} {MS} in A\'s original direction.'.replace(' at 0 m s⁻¹ at rest', ' is at rest').replace('A moves at 0 m s⁻¹ at rest', 'A is at rest') + ' Find m.',
             f'm = {u3(d["mB"])}', 'M1 momentum with m; A1 m') if d['vB'] != d['uB'] else None


def cm182_c4(r, D):
    d = coll(r, max(2, D))
    if not d:
        return None
    I_ = d['mB'] * (d['vB'] - d['uB'])
    intro = f'Particles A and B, of masses {kg(d["mA"])} and {kg(d["mB"])}, lie on a smooth horizontal surface. A is projected at {u3(d["uA"])} {MS} towards B, which ' + ('is at rest' if d['uB'] == 0 else f'moves at {u3(abs(d["uB"]))} {MS} {"away from A" if d["uB"] > 0 else "towards A"}') + f'. After the collision B moves at {u3(d["vB"])} {MS} in the direction A was originally moving.'
    parts = [
        P('Find the velocity of A after the collision.', f'{vel(d["vA"])} {dirn(d["vA"])}' if d['vA'] else 'A is at rest', 'M1 conservation of momentum; A1 velocity'),
        P('Find the magnitude of the impulse exerted on B by A.', f'{u3(abs(I_))} N s', 'M1 change in momentum of B; A1 value'),
        P('Find the loss of kinetic energy in the collision.', f'{u3(d["loss"])} J', 'M1 KE before and after; A1 loss'),
    ]
    return cmp_(r, intro, parts)


cm182.add('C4', (2, 3, 4, 5))(cm182_c4)


# ---------------------------------------------------------------- 18.3 coalescence and successive collisions

co183 = T('Coalescence and successive collisions', 'coalescence', 'successive collisions')
co183.fixed('C1', (1, 2), [
    ('Two particles coalesce in a collision. What does this mean?', 'they join and move together with a common velocity', 'They become a single combined particle.', ['they bounce apart with equal speeds', 'they both stop', 'they exchange velocities']),
    ('A 2 kg particle at 6 m s⁻¹ hits a 1 kg particle at rest and they coalesce. What is their common speed?', '4 m s⁻¹', '12 = 3v.', ['6 m s⁻¹', '3 m s⁻¹', '2 m s⁻¹']),
])
co183.fixed('C2', (2, 3), [
    ('Explain how to decide whether there will be a further collision between three particles in a line after two collisions.', 'Compare the final velocities: a further collision occurs if a particle behind is moving faster (in the positive direction) than the particle in front of it.', 'B1 compare velocities of adjacent particles; B1 faster behind means a collision [2]'),
])


@co183.add('C1', (1, 2, 3))
def co183_c1(r, D):
    mA, mB = r.sample([1, 2, 3, 4, 5, 6, Fr(1, 2)], 2)
    uA = r.choice([3, 4, 5, 6, 8, 10])
    uB = 0 if D <= 2 else r.choice([-1, -2, 1, 2])
    v = (mA * uA + mB * uB) / Fr(mA + mB)
    return MC(r, f'A particle of mass {kg(mA)} moving at {uA} {MS} collides with a particle of mass {kg(mB)}' + (' at rest' if uB == 0 else f' moving at {abs(uB)} {MS} {"in the same direction" if uB > 0 else "in the opposite direction"}') + '. They coalesce. Find their common speed.', vel(v),
              [vel(Fr(uA + uB, 2)), vel(Fr(mA * uA, mB)), vel((mA * uA - mB * uB) / Fr(mA + mB)) if uB else vel(Fr(uA)), vel(v * 2)], '(m₁u₁ + m₂u₂) = (m₁ + m₂)v.')


@co183.add('C2', (1, 2, 3, 4), 'explain')
def co183_err(r, D):
    nm = person(r)
    mA, mB = r.sample([1, 2, 3, 4, 5], 2)
    uA = r.choice([4, 5, 6, 8, 10])
    v = Fr(mA * uA, mA + mB)
    f = r.choice(['mass', 'ke', 'avg'])
    if f == 'mass' and mA > 1:
        return Q(f'A particle of mass {mA} kg moving at {uA} {MS} coalesces with a particle of mass {mB} kg at rest. {nm} writes {mA} × {uA} = {mA}v. Explain the error.',
                 f'After coalescing the combined mass is {mA + mB} kg: {mA * uA} = {mA + mB}v, v = {u3(v)} {MS}.', 'B1 combined mass; B1 correct speed')
    if f == 'avg':
        return Q(f'A particle of mass {mA} kg moving at {uA} {MS} coalesces with a particle of mass {mB} kg at rest. {nm} says the common speed is {u3(Fr(uA, 2))} {MS}, the average of the speeds. Explain the error.',
                 f'Momentum, not speed, is conserved: v = {mA * uA}/{mA + mB} = {u3(v)} {MS}.', 'B1 momentum conserved; B1 correct value')
    loss = Fr(1, 2) * mA * uA * uA - Fr(1, 2) * (mA + mB) * v * v
    return Q(f'A particle of mass {mA} kg moving at {uA} {MS} coalesces with a particle of mass {mB} kg at rest. Show that kinetic energy is lost and find the loss.',
             f'Common speed {u3(v)} {MS}; KE before {u3(Fr(1, 2) * mA * uA * uA)} J, after {u3(Fr(1, 2) * (mA + mB) * v * v)} J; loss {u3(loss)} J.', 'M1 common speed; M1 KE before and after; A1 loss')


def succ(r):
    """A hits B (at rest), A's velocity afterwards vA1 given; B then hits C (at rest) and coalesces."""
    mA, mB, mC = r.choice([1, 2, 3]), r.choice([1, 2, 3, 4]), r.choice([1, 2, 3, 4])
    uA = r.choice([4, 5, 6, 8, 10, 12])
    vA = r.choice([Fr(x, 2) for x in range(-4, uA)])
    vB = (mA * uA - mA * vA) / Fr(mB)
    if vB <= vA or vB <= 0:
        return None
    if Fr(1, 2) * mA * uA * uA < Fr(1, 2) * (mA * vA * vA + mB * vB * vB):
        return None
    vBC = mB * vB / Fr(mB + mC)
    again = vA > vBC
    return dict(mA=mA, mB=mB, mC=mC, uA=uA, vA=vA, vB=vB, vBC=vBC, again=again)


@co183.add('C3', (1, 2, 3, 4, 5), 'numerical')
def co183_calc(r, D):
    if D <= 2:
        mA, mB = r.sample([1, 2, 3, 4, 5, 6], 2)
        uA, uB = r.choice([4, 5, 6, 8]), r.choice([-2, -3, -4, 0, 1])
        v = (mA * uA + mB * uB) / Fr(mA + mB)
        loss = Fr(1, 2) * (mA * uA * uA + mB * uB * uB) - Fr(1, 2) * (mA + mB) * v * v
        return Q(f'Particles of masses {mA} kg and {mB} kg moving with velocities {uA} {MS} and {num(uB)} {MS} along the same line collide and coalesce. Find their common velocity and the loss of kinetic energy.',
                 f'{u3(v)} {MS}; {u3(loss)} J', 'M1 momentum; A1 velocity; M1 KE; A1 loss')
    d = succ(r)
    if not d:
        return None
    return Q(f'Three particles A, B and C, of masses {d["mA"]} kg, {d["mB"]} kg and {d["mC"]} kg, lie in that order on a smooth straight line. A is projected towards B at {d["uA"]} {MS}; after A hits B, A moves at {u3(abs(d["vA"]))} {MS} {dirn(d["vA"])}.'.replace(' at 0 m s⁻¹ at rest', ' is at rest') +
             ' B then hits C and they coalesce. Find the velocity of the combined particle and determine whether A collides with it again.',
             f'{u3(d["vBC"])} {MS}; {"yes" if d["again"] else "no"}, since A {"is faster" if d["again"] else "is slower or moves away"}', 'M1 first collision; A1 B\'s speed; M1 second collision; A1 combined velocity; B1 comparison')


def co183_c4(r, D):
    d = succ(r)
    if not d:
        return None
    intro = f'Three particles A, B and C, of masses {d["mA"]} kg, {d["mB"]} kg and {d["mC"]} kg, lie at rest in that order on a smooth straight horizontal groove. A is projected towards B with speed {d["uA"]} {MS}.'
    parts = [
        P(f'After A collides with B, A moves at {u3(abs(d["vA"]))} {MS} {dirn(d["vA"])}. Find the speed of B.'.replace(' at 0 m s⁻¹ at rest', ' is at rest'), vel(d['vB']), 'M1 momentum; A1 speed'),
        P(f'B (moving at {u3(d["vB"])} {MS}) then collides with C and they coalesce. Find the speed of the combined particle.', vel(d['vBC']), 'M1 momentum with combined mass; A1 speed'),
        P(f'Determine whether there is a further collision, given that A moves at {u3(d["vA"])} {MS} after the first collision.', 'yes' if d['again'] else 'no', 'M1 compares velocities; A1 conclusion'),
    ]
    return cmp_(r, intro, parts)


co183.add('C4', (2, 3, 4, 5))(co183_c4)

CHAPTERS[18] = [mo181, cm182, co183]


# ================================================================ Chapter 19 Work and energy

wk191 = T('Work done by a constant force including at an angle', 'work done', 'work done by a force at an angle')
wk191.fixed('C1', (1, 2), [
    ('A force of 20 N moves an object 5 m in the direction of the force. How much work is done?', '100 J', 'W = Fd.', ['4 J', '25 J', '100 N']),
    ('A force F acts at angle θ to the direction of motion over a distance d. What is the work done?', 'Fd cos θ', 'Only the component along the motion does work.', ['Fd sin θ', 'Fd', 'F cos θ / d']),
    ('How much work does the normal reaction do on a block sliding along a horizontal floor?', 'zero', 'It is perpendicular to the motion.', ['mgd', 'μmgd', 'Rd']),
])
wk191.fixed('C2', (2, 3), [
    ('Explain why a person carrying a heavy bag horizontally at constant speed does no work on the bag against gravity.', 'The force supporting the bag is vertical and the displacement is horizontal, so the angle is 90° and the work done, Fd cos 90°, is zero.', 'B1 force perpendicular to displacement; B1 cos 90° = 0 [2]'),
])


def work_case(r, D):
    F = r.choice([10, 12, 15, 20, 25, 30, 40, 50, 60, 80, 100])
    d = r.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20])
    th = 0 if D == 1 else r.choice([10, 15, 20, 25, 30, 35, 40, 45, 50, 60])
    return dict(F=F, d=d, th=th, W=F * d * cosd(th))


@wk191.add('C1', (1, 2, 3))
def wk191_c1(r, D):
    w = work_case(r, D)
    if D == 1:
        return MC(r, f'A horizontal force of {w["F"]} N pulls a box {w["d"]} m across a floor. Find the work done by the force.', f'{w["F"] * w["d"]} J',
                  [f'{u3(Fr(w["F"], w["d"]))} J', f'{w["F"] + w["d"]} J', f'{w["F"] * w["d"] * 2} J', f'{w["F"] * w["d"]} N'], 'W = Fd.')
    return MC(r, f'A force of {w["F"]} N acting at {w["th"]}° above the horizontal pulls a sledge {w["d"]} m along horizontal ground. Find the work done by the force.', f'{n3(w["W"])} J',
              [f'{n3(w["F"] * w["d"] * sind(w["th"]))} J', f'{w["F"] * w["d"]} J', f'{n3(w["F"] * cosd(w["th"]))} J'], 'W = Fd cos θ.')


@wk191.add('C2', (1, 2, 3, 4), 'explain')
def wk191_err(r, D):
    nm = person(r)
    w = work_case(r, max(2, D))
    f = r.choice(['sin', 'weight', 'friction'])
    if f == 'sin':
        return Q(f'A force of {w["F"]} N at {w["th"]}° to the horizontal pulls a box {w["d"]} m along horizontal ground. {nm} calculates the work done as {w["F"]} × {w["d"]} × sin {w["th"]}°. Explain the error.',
                 f'Only the component of the force along the displacement does work: W = Fd cos θ = {n3(w["W"])} J.', 'B1 component along the motion uses cosine; B1 correct value')
    if f == 'weight':
        m = r.choice([2, 5, 10, 20])
        return Q(f'A box of mass {m} kg is pulled {w["d"]} m along horizontal ground. {nm} says the work done against gravity is {m * G * w["d"]} J. Explain the error.',
                 'The weight is perpendicular to the horizontal displacement, so no work is done against gravity; work against gravity requires a change in height.', 'B1 perpendicular so zero; B1 needs vertical displacement')
    m = r.choice([2, 4, 5, 8, 10])
    mu = mus(r)
    R = m * G - w['F'] * sind(w['th'])
    if R < 1:
        return None
    return Q(f'A box of mass {m} kg is pulled {w["d"]} m across rough horizontal ground (μ = {u3(mu)}) by a force of {w["F"]} N at {w["th"]}° above the horizontal. {nm} uses R = {m * G} N to find the work done against friction. Explain the error and find the correct value.',
             f'The pull has an upward component, so R = {m * G} − {w["F"]} sin {w["th"]}° = {n3(R)} N; work against friction = μRd = {n3(float(mu) * R * w["d"])} J.', 'B1 R reduced by the vertical component; B1 correct work')


@wk191.add('C3', (1, 2, 3, 4, 5), 'numerical')
def wk191_calc(r, D):
    w = work_case(r, D)
    if D <= 2:
        return Q(f'A force of {w["F"]} N acting at {w["th"]}° to the horizontal moves a crate {w["d"]} m along a horizontal floor. Find the work done by the force.', f'{n3(w["W"])} J', 'M1 Fd cos θ; A1 value')
    m = r.choice([2, 5, 10, 20, 50])
    if D == 3:
        a = r.choice([10, 20, 30, 40])
        return Q(f'A particle of mass {m} kg moves {w["d"]} m up a line of greatest slope of a plane inclined at {a}°. Find the work done against gravity.', f'{n3(m * G * w["d"] * sind(a))} J', 'M1 height gained d sin α; A1 work mgh')
    mu = mus(r)
    R = m * G - w['F'] * sind(w['th'])
    if R < 1:
        return None
    Wf = float(mu) * R * w['d']
    return Q(f'A crate of mass {m} kg is pulled {w["d"]} m across rough horizontal ground (μ = {u3(mu)}) by a rope with tension {w["F"]} N at {w["th"]}° above the horizontal. Find the work done by the tension and the work done against friction.',
             f'{n3(w["W"])} J; {n3(Wf)} J', 'M1 Fd cos θ; A1 tension work; M1 R; M1 F = μR; A1 friction work')


def wk191_c4(r, D):
    w = work_case(r, max(2, D))
    m = r.choice([5, 8, 10, 15, 20])
    mu = mus(r)
    R = m * G - w['F'] * sind(w['th'])
    if R < 1:
        return None
    Wf = float(mu) * R * w['d']
    intro = f'A sledge of mass {m} kg is pulled {w["d"]} m across rough horizontal snow by a rope inclined at {w["th"]}° above the horizontal with tension {w["F"]} N. The coefficient of friction is {u3(mu)}.'
    parts = [
        P('Find the work done by the tension.', f'{n3(w["W"])} J', 'M1 Fd cos θ; A1 value'),
        P('Find the normal reaction.', f'{n3(R)} N', 'M1 resolves vertically; A1 R'),
        P('Find the work done against friction.', f'{n3(Wf)} J', 'M1 μRd; A1 value'),
        P('State the work done by the weight and by the normal reaction, giving a reason.', '0 J for each: both are perpendicular to the motion', 'B1 zero with reason'),
    ]
    return cmp_(r, intro, parts)


wk191.add('C4', (2, 3, 4, 5))(wk191_c4)


# ---------------------------------------------------------------- 19.2 KE and GPE

ke192 = T('Kinetic energy and gravitational potential energy', 'kinetic energy', 'gravitational potential energy')
ke192.fixed('C1', (1, 2), [
    ('What is the kinetic energy of a 2 kg mass moving at 3 m s⁻¹?', '9 J', 'KE = (1/2)mv².', ['6 J', '18 J', '3 J']),
    ('What is the gain in gravitational potential energy when a 5 kg mass is raised 4 m (g = 10)?', '200 J', 'GPE = mgh.', ['20 J', '50 J', '400 J']),
    ('If the speed of a particle doubles, what happens to its kinetic energy?', 'it is multiplied by 4', 'KE ∝ v².', ['it doubles', 'it halves', 'it is unchanged']),
])
ke192.fixed('C2', (2, 3), [
    ('Explain why the change in gravitational potential energy of a particle moving along a slope depends only on its change in height.', 'Gravity acts vertically, so only the vertical displacement contributes to the work done by the weight; mgh depends on the vertical height change, not the path.', 'B1 weight acts vertically; B1 only vertical displacement matters [2]'),
])


@ke192.add('C1', (1, 2, 3))
def ke192_c1(r, D):
    m = r.choice([Fr(1, 2), 1, 2, 3, 4, 5, 10, 50, 800, 1200])
    v = r.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20])
    if D <= 2:
        k = Fr(1, 2) * m * v * v
        return MC(r, f'Find the kinetic energy of a particle of mass {kg(m)} moving at {v} {MS}.', f'{u3(k)} J', [f'{u3(m * v)} J', f'{u3(m * v * v)} J', f'{u3(Fr(1, 2) * m * v)} J', f'{u3(k * 2 + 1)} J'], 'KE = (1/2)mv².')
    h = r.choice([2, 3, 5, 8, 10, 12, 20])
    a = r.choice([20, 30, 40, 50])
    gp = float(m) * G * h * sind(a)
    return MC(r, f'A particle of mass {kg(m)} moves {h} m up a slope inclined at {a}° to the horizontal. Find the gain in gravitational potential energy.', f'{n3(gp)} J',
              [f'{u3(m * G * h)} J', f'{n3(float(m) * G * h * cosd(a))} J', f'{n3(float(m) * h * sind(a))} J'], 'Height gained = d sin α.')


@ke192.add('C2', (1, 2, 3, 4), 'explain')
def ke192_err(r, D):
    nm = person(r)
    m = r.choice([2, 3, 4, 5, 10, 20])
    u, v = r.sample([2, 3, 4, 5, 6, 8, 10], 2)
    f = r.choice(['diff', 'half', 'vec'])
    if f == 'diff':
        right = Fr(1, 2) * m * (v * v - u * u)
        wrong = Fr(1, 2) * m * (v - u) ** 2
        return Q(f'The speed of a {m} kg particle changes from {u} {MS} to {v} {MS}. {nm} finds the change in kinetic energy as (1/2) × {m} × ({v} − {u})² = {u3(wrong)} J. Explain the error and correct it.',
                 f'Change in KE = (1/2)m(v² − u²) = (1/2) × {m} × ({v * v} − {u * u}) = {u3(right)} J, not (1/2)m(v − u)².', 'B1 difference of squares, not square of difference; B1 correct value')
    if f == 'half':
        return Q(f'{nm} calculates the kinetic energy of a {m} kg particle moving at {v} {MS} as {m * v * v} J. Explain the error.', f'KE = (1/2)mv² = {u3(Fr(m * v * v, 2))} J; the factor 1/2 is missing.', 'B1 factor 1/2; B1 correct value')
    return Q(f'Explain why the kinetic energy of a {m} kg particle moving at {v} {MS} is the same whether it moves left or right, while its momentum is not.',
             f'KE = (1/2)mv² depends on v², so the sign of v does not matter ({u3(Fr(m * v * v, 2))} J); momentum mv is a vector and changes sign ({"±"}{m * v} N s).', 'B1 KE scalar using v²; B1 momentum vector')


@ke192.add('C3', (1, 2, 3, 4, 5), 'numerical')
def ke192_calc(r, D):
    m = r.choice([2, 3, 4, 5, 10, 20, 50, 70])
    u, v = r.sample([2, 3, 4, 5, 6, 8, 10, 12], 2)
    if D <= 2:
        return Q(f'A particle of mass {m} kg changes speed from {u} {MS} to {v} {MS}. Find the change in kinetic energy, stating whether it is a gain or a loss.', f'{u3(abs(Fr(m, 2) * (v * v - u * u)))} J {"gain" if v > u else "loss"}', 'M1 (1/2)m(v² − u²); A1 value with gain/loss')
    h = r.choice([5, 8, 10, 15, 20, 30])
    if D <= 4:
        a = r.choice([10, 20, 25, 30, 35])
        L = r.choice([5, 10, 15, 20, 25])
        m = r.choice([60, 70, 80, 90, 100])
        dGPE = m * G * L * sind(a)
        dKE = Fr(m, 2) * (v * v - u * u)
        return Q(f'A cyclist and bicycle of total mass {m} kg move {L} m down a slope inclined at {a}°, and the speed changes from {u} {MS} to {v} {MS}. Find the loss in gravitational potential energy and the change in kinetic energy.',
                 f'{n3(dGPE)} J; {u3(abs(dKE))} J {"gain" if dKE > 0 else "loss"}', 'M1 height d sin α; A1 GPE loss; M1 KE change; A1 value')
    v2 = r.choice([1, 2, 3, 4])
    s = Fr(m * v * v, 2)
    vnew = math.sqrt(2 * float(s) / m * (1 / v2))
    return Q(f'A particle of mass {m} kg has kinetic energy {u3(s)} J. Find its speed, and the speed it would have if its kinetic energy were divided by {v2 + 1}.', f'{v} {MS}; {n3(v / math.sqrt(v2 + 1))} {MS}',
             'M1 (1/2)mv² = KE; A1 speed; M1 v ∝ √KE; A1 second speed')


def ke192_c4(r, D):
    m = r.choice([50, 60, 70, 80])
    h = r.choice([5, 10, 15, 20])
    a = r.choice([20, 25, 30, 35])
    L = h / sind(a)
    u, v = r.choice([2, 3, 4]), r.choice([8, 10, 12])
    gpe = m * G * h
    dke = Fr(m, 2) * (v * v - u * u)
    intro = f'A skier of mass {m} kg descends a slope inclined at {a}°, losing {h} m in height. Her speed increases from {u} {MS} to {v} {MS}.'
    parts = [
        P('Find the distance travelled along the slope.', f'{n3(L)} m', 'B1 h/sin α'),
        P('Find the loss in gravitational potential energy.', f'{gpe} J', 'B1 mgh'),
        P('Find the gain in kinetic energy.', f'{u3(dke)} J', 'M1 (1/2)m(v² − u²); A1 value'),
        P('Hence find the work done against resistance.', f'{u3(gpe - dke)} J' if gpe > dke else None, 'M1 difference; A1 value'),
    ]
    if gpe <= dke:
        return None
    return cmp_(r, intro, parts)


ke192.add('C4', (2, 3, 4, 5))(ke192_c4)


# ---------------------------------------------------------------- 19.3 conservation of mechanical energy

ce193 = T('Conservation of mechanical energy', 'conservation of mechanical energy', 'energy conservation')
ce193.fixed('C1', (1, 2), [
    ('When is mechanical energy (KE + GPE) conserved?', 'when no work is done by forces other than weight', 'e.g. smooth surfaces and no air resistance.', ['always', 'only on horizontal surfaces', 'only when the speed is constant']),
    ('A ball is dropped from 5 m (g = 10). Using energy, what is its speed on reaching the ground?', '10 m s⁻¹', '(1/2)v² = gh.', ['50 m s⁻¹', '5 m s⁻¹', '100 m s⁻¹']),
])
ce193.fixed('C2', (2, 3), [
    ('Explain why energy methods can find the speed of a particle at the bottom of a smooth curved slope when suvat cannot.', 'On a curved slope the acceleration is not constant, so suvat does not apply; but with no friction the total mechanical energy is conserved, so the speed follows from the height lost.', 'B1 acceleration varies; B1 energy depends only on height [2]'),
])


@ce193.add('C1', (1, 2, 3))
def ce193_c1(r, D):
    h = r.choice([Fr(5, 4), 5, Fr(45, 4), 20, Fr(16, 5), Fr(9, 5), 10, 15])
    u = r.choice([0, 0, 2, 3, 5]) if D >= 2 else 0
    v = math.sqrt(u * u + 2 * G * float(h))
    if D <= 2:
        return MC(r, f'A particle is released{" from rest" if u == 0 else " with speed " + str(u) + " " + MS} at the top of a smooth slope of vertical height {u3(h)} m. Find its speed at the bottom.', f'{u3(v)} {MS}',
                  [f'{u3(math.sqrt(G * float(h)))} {MS}', f'{u3(2 * G * float(h))} {MS}', f'{u3(math.sqrt(2 * G * float(h)) + u)} {MS}' if u else f'{u3(G * float(h))} {MS}'], '(1/2)mv² = (1/2)mu² + mgh.')
    return MC(r, f'A ball is thrown vertically upwards at {u3(v)} {MS}. Using energy, find the greatest height it reaches.', f'{u3(v * v / (2 * G))} m', [f'{u3(v * v / G)} m', f'{u3(v / G)} m', f'{u3(v / (2 * G))} m'], 'mgh = (1/2)mu².')


@ce193.add('C2', (1, 2, 3, 4), 'explain')
def ce193_err(r, D):
    nm = person(r)
    h = r.choice([5, 10, 15, 20, 30])
    m = r.choice([2, 5, 10])
    f = r.choice(['rough', 'mass', 'path'])
    if f == 'rough':
        return Q(f'A block slides down a rough slope of vertical height {h} m. {nm} finds its speed at the bottom using (1/2)mv² = mgh. Explain why this overestimates the speed.',
                 'On a rough slope friction does work against the motion, so some of the GPE is converted to heat; the KE gained is less than mgh.', 'B1 friction does work; B1 KE less than mgh')
    if f == 'mass':
        return Q(f'{nm} says a {m} kg ball and a {2 * m} kg ball released from rest at the same height of {h} m will reach the ground with different speeds. Use energy to explain why this is wrong (ignore air resistance).',
                 f'mgh = (1/2)mv² gives v = √(2gh) = {n3(math.sqrt(2 * G * h))} {MS}; m cancels.', 'M1 energy equation; A1 m cancels')
    return Q(f'Two smooth slides start at the same height {h} m above the ground, one straight and one curved. Explain why a child starting from rest reaches the bottom of each with the same speed.',
             f'Mechanical energy is conserved on smooth slides; the speed depends only on the height lost: v = √(2gh) = {n3(math.sqrt(2 * G * h))} {MS} for both.', 'B1 conservation of energy; B1 independent of path')


@ce193.add('C3', (1, 2, 3, 4, 5), 'numerical')
def ce193_calc(r, D):
    if D <= 2:
        h = r.choice([2, 3, 5, 8, 10, 20])
        u = r.choice([0, 2, 4, 5])
        v = math.sqrt(u * u + 2 * G * h)
        return Q(f'A particle is projected down a smooth curved track with speed {u} {MS} from a point {h} m above the bottom. Find its speed at the bottom.', f'{n3(v)} {MS}', 'M1 KE + PE conserved; A1 speed')
    if D <= 4:
        u = r.choice([5, 6, 8, 10, 12])
        h = r.choice([1, 2, 3])
        if u * u <= 2 * G * h:
            return None
        v = math.sqrt(u * u - 2 * G * h)
        return Q(f'A particle slides along a smooth track. At A, its speed is {u} {MS}; B is {h} m higher than A. Find the speed of the particle at B.', f'{n3(v)} {MS}', 'M1 energy equation; A1 speed')
    u = r.choice([8, 10, 12, 15, 20])
    h0 = r.choice([5, 10, 15, 20])
    a = r.choice([30, 45, 60])
    # projected from a cliff at an angle: speed when it hits the sea depends only on height
    v = math.sqrt(u * u + 2 * G * h0)
    return Q(f'A stone is thrown from the top of a cliff {h0} m above the sea with speed {u} {MS} at {a}° above the horizontal. Using energy, find the speed with which it hits the sea (ignore air resistance).', f'{n3(v)} {MS}',
             'M1 energy equation; B1 direction irrelevant; A1 speed')


def ce193_c4(r, D):
    m = r.choice([2, 5, 10, 20])
    hA, hB = r.choice([10, 12, 15, 20]), r.choice([2, 4, 5, 6])
    u = r.choice([0, 2, 3])
    vB = math.sqrt(u * u + 2 * G * (hA - hB))
    vC = math.sqrt(u * u + 2 * G * hA)
    intro = f'A particle of mass {m} kg moves along a smooth track. It starts at A, {hA} m above the ground, {"from rest" if u == 0 else "with speed " + str(u) + " " + MS}. B is a point on the track {hB} m above the ground and C is at ground level.'
    parts = [
        P('Find the kinetic energy of the particle at B.', f'{n3(0.5 * m * vB * vB)} J', 'M1 energy conservation; A1 KE'),
        P('Find the speed of the particle at B.', f'{n3(vB)} {MS}', 'B1 speed'),
        P('Find the speed of the particle at C.', f'{n3(vC)} {MS}', 'M1 energy; A1 speed'),
        P('State one modelling assumption you have made.', 'the track is smooth (no friction) and air resistance is ignored', 'B1'),
    ]
    return cmp_(r, intro, parts)


ce193.add('C4', (2, 3, 4, 5))(ce193_c4)

CHAPTERS[19] = [wk191, ke192, ce193]


# ================================================================ Chapter 20 Work-energy principle and power

we201 = T('The work-energy principle including work done against resistance', 'work-energy principle', 'work done against resistance')
we201.fixed('C1', (1, 2), [
    ('What does the work-energy principle state?', 'the work done by the resultant force equals the change in kinetic energy', 'Equivalently, initial energy + work in = final energy + work out.', ['kinetic energy is always conserved', 'work done equals the change in momentum', 'potential energy equals kinetic energy']),
    ('A 2 kg block slows from 5 m s⁻¹ to rest on a rough floor. How much work is done against friction?', '25 J', 'Loss in KE = (1/2)(2)(25).', ['10 J', '50 J', '5 J']),
])
we201.fixed('C2', (2, 3), [
    ('Explain why a car descending a hill at constant speed must be doing work against resistance.', 'Its KE is constant but it loses GPE; by the work-energy principle the lost GPE equals the work done against resistance (and braking).', 'B1 KE constant, GPE lost; B1 equals work against resistance [2]'),
])


def we_case(r, D):
    m = r.choice([2, 5, 10, 20, 50, 70, 80])
    a = r.choice([10, 15, 20, 25, 30])
    L = r.choice([5, 10, 15, 20, 25, 40])
    u = r.choice([0, 2, 3, 4, 5])
    R = r.choice([5, 10, 15, 20, 30, 40, 60, 80, 100])
    gain = m * G * L * sind(a) - R * L
    v2 = u * u + 2 * gain / m
    if v2 <= 0:
        return None
    return dict(m=m, a=a, L=L, u=u, R=R, v=math.sqrt(v2), gpe=m * G * L * sind(a), wr=R * L)


@we201.add('C1', (1, 2, 3))
def we201_c1(r, D):
    m = r.choice([2, 4, 5, 10, 20])
    u = r.choice([4, 5, 6, 8, 10])
    d = r.choice([2, 4, 5, 8, 10, 20])
    k = Fr(m * u * u, 2)
    F = k / d
    if D <= 2:
        return MC(r, f'A {m} kg block sliding at {u} {MS} comes to rest after {d} m on a rough horizontal floor. Find the work done against friction.', f'{u3(k)} J', [f'{u3(m * u)} J', f'{u3(m * u * u)} J', f'{u3(k / d)} J'], 'Loss of KE.')
    return MC(r, f'A {m} kg block sliding at {u} {MS} comes to rest after {d} m on a rough horizontal floor. Find the friction force, assumed constant.', f'{u3(F)} N', [f'{u3(k)} N', f'{u3(k * d)} N', f'{u3(Fr(m * u, d))} N'], 'F × d = loss of KE.')


@we201.add('C2', (1, 2, 3, 4), 'explain')
def we201_err(r, D):
    nm = person(r)
    d = we_case(r, D)
    if not d:
        return None
    f = r.choice(['forget', 'sign', 'height'])
    if f == 'forget':
        v0 = math.sqrt(d['u'] ** 2 + 2 * d['gpe'] / d['m'])
        return Q(f'A particle of mass {d["m"]} kg moves {d["L"]} m down a slope inclined at {d["a"]}°, starting at {d["u"]} {MS}, against a constant resistance of {d["R"]} N. {nm} finds its final speed as {n3(v0)} {MS}. Explain the error and correct it.',
                 f'{nm} has ignored the work done against the resistance ({d["wr"]} J); (1/2)mv² = (1/2)mu² + {n3(d["gpe"])} − {d["wr"]} gives v = {n3(d["v"])} {MS}.', 'B1 resistance work omitted; B1 correct speed')
    if f == 'height':
        return Q(f'A particle moves {d["L"]} m along a slope inclined at {d["a"]}°. {nm} uses mg × {d["L"]} for the change in GPE. Explain the error.',
                 f'GPE depends on the vertical height: h = {d["L"]} sin {d["a"]}° = {n3(d["L"] * sind(d["a"]))} m, so ΔGPE = mgh.', 'B1 vertical height needed; B1 h = d sin α')
    return Q(f'Explain how the work-energy principle is written for a particle moving down a slope against a resistance, and use it to find the final speed of a {d["m"]} kg particle starting at {d["u"]} {MS} and moving {d["L"]} m down a {d["a"]}° slope against {d["R"]} N.',
             f'Initial KE + loss of GPE − work against resistance = final KE: v = {n3(d["v"])} {MS}.', 'B1 statement; B1 speed')


@we201.add('C3', (1, 2, 3, 4, 5), 'numerical')
def we201_calc(r, D):
    d = we_case(r, D)
    if not d:
        return None
    if D <= 2:
        P_ = r.choice([20, 30, 40, 50, 60])
        m = r.choice([5, 10, 20])
        L = r.choice([5, 10, 20])
        R = r.choice([5, 10, 15, 20])
        if P_ <= R:
            return None
        v = math.sqrt(2 * (P_ - R) * L / m)
        return Q(f'A box of mass {m} kg is pulled from rest across a horizontal floor by a horizontal force of {P_} N against a resistance of {R} N. Use the work-energy principle to find its speed after {L} m.', f'{n3(v)} {MS}',
                 'M1 work done by the net force = KE gained; A1 speed')
    if D <= 4:
        return Q(f'A particle of mass {d["m"]} kg moves {d["L"]} m down a line of greatest slope of a plane inclined at {d["a"]}°. {"It starts from rest" if d["u"] == 0 else "Its initial speed is " + str(d["u"]) + " " + MS} and a constant resistance of {d["R"]} N acts. Use the work-energy principle to find its final speed.',
                 f'{n3(d["v"])} {MS}', 'M1 GPE lost; M1 work against resistance; M1 work-energy equation; A1 speed')
    # find the resistance given speeds
    return Q(f'A cyclist and bicycle of mass {d["m"]} kg freewheel {d["L"]} m down a hill inclined at {d["a"]}°, {"starting from rest and reaching a speed of " + n3(d["v"]) + " " + MS if d["u"] == 0 else "the speed increasing from " + str(d["u"]) + " " + MS + " to " + n3(d["v"]) + " " + MS}. Find the constant resistance to motion.', f'{n3(d["R"])} N',
             'M1 KE change; M1 GPE change; M1 work-energy equation; A1 resistance')


def we201_c4(r, D):
    d = we_case(r, D)
    if not d:
        return None
    ke0 = 0.5 * d['m'] * d['u'] ** 2
    ke1 = 0.5 * d['m'] * d['v'] ** 2
    intro = f'A particle of mass {d["m"]} kg moves {d["L"]} m down a line of greatest slope of a rough plane inclined at {d["a"]}°. {"It starts from rest at the top." if d["u"] == 0 else "Its speed at the top is " + str(d["u"]) + " " + MS + "."} The resistance to motion is constant at {d["R"]} N.'
    parts = [
        P('Find the loss in gravitational potential energy.', f'{n3(d["gpe"])} J', 'M1 mg × d sin α; A1 value'),
        P('Find the work done against the resistance.', f'{d["wr"]} J', 'B1 value'),
        P('Find the speed of the particle at the bottom.', f'{n3(d["v"])} {MS}', 'M1 work-energy equation; A1 speed'),
        P('Find the kinetic energy gained.', f'{n3(ke1 - ke0)} J', 'B1 value'),
    ]
    return cmp_(r, intro, parts)


we201.add('C4', (2, 3, 4, 5))(we201_c4)


# ---------------------------------------------------------------- 20.2 power

pw202 = T('Power as rate of doing work and P = Fv', 'power', 'p = fv', 'rate of doing work')
pw202.fixed('C1', (1, 2), [
    ('A car engine produces a driving force of 2000 N at 15 m s⁻¹. What is its power?', '30 kW', 'P = Fv.', ['133 W', '30 W', '2015 W']),
    ('A car travels at its maximum speed on a level road. What is its acceleration?', 'zero', 'At maximum speed the driving force equals the resistance.', ['g', 'P/v', 'it depends on the mass']),
    ('What is 1 watt equal to?', '1 joule per second', 'Power is the rate of doing work.', ['1 newton per second', '1 joule per metre', '1 newton metre']),
])
pw202.fixed('C2', (2, 3), [
    ('Explain why a car working at constant power has a smaller driving force at higher speeds.', 'P = Fv with P constant, so F = P/v decreases as v increases.', 'B1 P = Fv; B1 F inversely proportional to v [2]'),
])


def pw_case(r, D):
    m = r.choice([800, 1000, 1200, 1500, 2000])
    P_ = r.choice([20, 24, 30, 36, 40, 45, 50, 60]) * 1000
    R = r.choice([400, 500, 600, 750, 800, 1000, 1200, 1500])
    vmax = P_ / R
    v = r.choice([x for x in (8, 10, 12, 15, 20, 25) if x < vmax] or [None])
    if v is None:
        return None
    a = (P_ / v - R) / m
    return dict(m=m, P=P_, R=R, vmax=vmax, v=v, a=a, kW=P_ // 1000)


@pw202.add('C1', (1, 2, 3))
def pw202_c1(r, D):
    d = pw_case(r, D)
    if not d:
        return None
    if D == 1:
        F = r.choice([500, 800, 1000, 1500, 2000])
        v = r.choice([10, 12, 15, 20, 25])
        return MC(r, f'A car\'s driving force is {F} N when it moves at {v} {MS}. Find the power of the engine.', f'{u3(F * v / 1000)} kW', [f'{u3(Fr(F, v))} kW', f'{u3(F * v)} kW', f'{u3(F * v / 2000)} kW'], 'P = Fv.')
    if D == 2:
        return MC(r, f'A car with engine power {d["kW"]} kW moves on a level road against a constant resistance of {d["R"]} N. Find its maximum speed.', f'{u3(d["vmax"])} {MS}',
                  [f'{u3(d["P"] * d["R"] / 1e6)} {MS}', f'{u3(d["kW"] / d["R"] * 1000 / 2)} {MS}', f'{u3(d["R"] / d["kW"])} {MS}'], 'At maximum speed P/v = R.')
    return MC(r, f'A car of mass {d["m"]} kg works at {d["kW"]} kW against a resistance of {d["R"]} N. Find its acceleration at {d["v"]} {MS} on a level road.', f'{n3(d["a"])} {MS2}',
              [f'{n3(d["P"] / d["v"] / d["m"])} {MS2}', f'{n3((d["P"] / d["v"] + d["R"]) / d["m"])} {MS2}', f'{n3(d["P"] / d["m"])} {MS2}'], 'F = P/v; F − R = ma.')


@pw202.add('C2', (1, 2, 3, 4), 'explain')
def pw202_err(r, D):
    nm = person(r)
    d = pw_case(r, D)
    if not d:
        return None
    f = r.choice(['kw', 'force', 'max'])
    if f == 'kw':
        return Q(f'A car works at {d["kW"]} kW at a speed of {d["v"]} {MS}. {nm} finds the driving force as {d["kW"]}/{d["v"]} = {n3(d["kW"] / d["v"])} N. Explain the error.',
                 f'Power must be in watts: {d["P"]} W, so F = {d["P"]}/{d["v"]} = {n3(d["P"] / d["v"])} N.', 'B1 kW to W; B1 correct force')
    if f == 'force':
        return Q(f'A car of mass {d["m"]} kg works at a constant {d["kW"]} kW against a resistance of {d["R"]} N. {nm} says its acceleration is the same at all speeds. Explain why this is wrong.',
                 f'The driving force P/v decreases as v increases, so the resultant force (P/v − R) and hence a decrease: e.g. a = {n3(d["a"])} {MS2} at {d["v"]} {MS}, and a = 0 at {u3(d["vmax"])} {MS}.', 'B1 F = P/v decreases; B1 a decreases to zero at max speed')
    return Q(f'Explain why a car working at a constant power of {d["kW"]} kW against a constant resistance of {d["R"]} N has a maximum speed, and find it.',
             f'As speed increases the driving force P/v falls until it equals the resistance; then a = 0. v_max = {d["P"]}/{d["R"]} = {u3(d["vmax"])} {MS}.', 'B1 driving force equals resistance; B1 value')


@pw202.add('C3', (1, 2, 3, 4, 5), 'numerical')
def pw202_calc(r, D):
    d = pw_case(r, D)
    if not d:
        return None
    if D <= 2:
        return Q(f'A car of mass {d["m"]} kg has a maximum speed of {u3(d["vmax"])} {MS} on a level road against a constant resistance of {d["R"]} N. Find the power of the engine.', f'{u3(d["P"] / 1000)} kW', 'M1 at max speed F = R; A1 P = Fv')
    if D <= 4:
        return Q(f'A car of mass {d["m"]} kg moves along a level road with its engine working at {d["kW"]} kW. The resistance to motion is {d["R"]} N. Find the acceleration when the speed is {d["v"]} {MS}.', f'{n3(d["a"])} {MS2}',
                 'M1 F = P/v; M1 F − R = ma; A1 a')
    a = r.choice([Fr(1, 2), Fr(1, 4), 1, Fr(3, 4)])
    P_ = (d['R'] + d['m'] * float(a)) * d['v']
    return Q(f'A car of mass {d["m"]} kg moving along a level road against a resistance of {d["R"]} N has acceleration {u3(a)} {MS2} when its speed is {d["v"]} {MS}. Find the power at this instant.', f'{n3(P_ / 1000)} kW',
             'M1 F − R = ma; A1 F; M1 P = Fv; A1 power')


def pw202_c4(r, D):
    d = pw_case(r, D)
    if not d:
        return None
    intro = f'A car of mass {d["m"]} kg has an engine working at a constant {d["kW"]} kW. It moves along a straight level road against a constant resistance of {d["R"]} N.'
    v2 = r.choice([x for x in (5, 8, 10, 12, 15) if x < d['vmax'] and x != d['v']] or [None])
    if v2 is None:
        return None
    parts = [
        P(f'Find the driving force when the speed is {d["v"]} {MS}.', f'{n3(d["P"] / d["v"])} N', 'M1 P = Fv; A1 F'),
        P(f'Find the acceleration when the speed is {d["v"]} {MS}.', f'{n3(d["a"])} {MS2}', 'M1 N2L; A1 a'),
        P('Find the maximum speed of the car.', f'{u3(d["vmax"])} {MS}', 'M1 F = R; A1 speed'),
        P(f'Find the acceleration when the speed is {v2} {MS}.', f'{n3((d["P"] / v2 - d["R"]) / d["m"])} {MS2}', 'B1 value'),
    ]
    return cmp_(r, intro, parts)


pw202.add('C4', (2, 3, 4, 5))(pw202_c4)


# ---------------------------------------------------------------- 20.3 variable resistance and slopes

vr203 = T('Motion with variable resistance and power on slopes', 'variable resistance', 'power on slopes')
vr203.fixed('C1', (1, 2), [
    ('A car climbs a hill inclined at α at constant speed. Which force must the driving force balance, as well as the resistance?', 'mg sin α', 'The weight component down the slope.', ['mg cos α', 'mg', 'the normal reaction']),
    ('If the resistance is kv, what is the maximum speed of a car with power P on a level road?', '√(P/k)', 'P/v = kv at maximum speed.', ['P/k', 'P/(kv)', 'kP']),
])
vr203.fixed('C2', (2, 3), [
    ('Explain why a car working at the same power has a lower maximum speed going up a hill than on a level road.', 'Going uphill the driving force must balance the resistance and mg sin α, so the larger total force means P = Fv gives a smaller v.', 'B1 extra weight component; B1 larger F so smaller v [2]'),
])


def slope_pw(r, D):
    m = r.choice([800, 1000, 1200, 1500])
    P_ = r.choice([20, 24, 30, 36, 40, 50, 60]) * 1000
    R = r.choice([300, 400, 500, 600, 800])
    s = Fr(1, r.choice([10, 20, 25, 40, 50]))
    up = m * G * float(s)
    vmax_up = P_ / (R + up)
    vmax_down = P_ / (R - up) if R > up else None
    k = r.choice([Fr(1, 2), 1, 2, 3, 4])
    # resistance kv² on level: P/v = kv² → v = (P/k)^(1/3)
    vq = (P_ / float(k)) ** (1 / 3)
    if not ok(P_ / vq, float(k) * vq * vq, 'kv2', 1e-6 * P_):
        return None
    return dict(m=m, P=P_, R=R, s=s, up=up, vup=vmax_up, vdown=vmax_down, k=k, vq=vq, kW=P_ // 1000)


@vr203.add('C1', (1, 2, 3))
def vr203_c1(r, D):
    d = slope_pw(r, D)
    if not d:
        return None
    if D <= 2:
        return MC(r, f'A car of mass {d["m"]} kg climbs a hill inclined at α, where sin α = {num(d["s"])}. Find the component of its weight down the slope.', f'{u3(d["up"])} N',
                  [f'{u3(d["m"] * G)} N', f'{u3(d["m"] * float(d["s"]))} N', f'{u3(d["up"] * 2)} N'], 'mg sin α.')
    return MC(r, f'A car of mass {d["m"]} kg with power {d["kW"]} kW climbs a hill inclined at α, where sin α = {num(d["s"])}, against a resistance of {d["R"]} N. Find its maximum speed up the hill.', f'{n3(d["vup"])} {MS}',
              [f'{n3(d["P"] / d["R"])} {MS}', f'{n3(d["P"] / (d["R"] + d["m"] * G))} {MS}', f'{n3(d["vdown"])} {MS}' if d['vdown'] else f'{n3(d["vup"] * 2)} {MS}'], 'P/v = R + mg sin α.')


@vr203.add('C2', (1, 2, 3, 4), 'explain')
def vr203_err(r, D):
    nm = person(r)
    d = slope_pw(r, D)
    if not d:
        return None
    f = r.choice(['noslope', 'kv', 'down'])
    if f == 'noslope':
        return Q(f'A car of mass {d["m"]} kg with power {d["kW"]} kW climbs a hill (sin α = {num(d["s"])}) against a resistance of {d["R"]} N. {nm} gives the maximum speed as {d["P"]}/{d["R"]} = {n3(d["P"] / d["R"])} {MS}. Explain the error.',
                 f'Up the hill the driving force must also balance mg sin α = {u3(d["up"])} N: v = {d["P"]}/({d["R"]} + {u3(d["up"])}) = {n3(d["vup"])} {MS}.', 'B1 weight component omitted; B1 correct speed')
    if f == 'kv':
        return Q(f'A car with power {d["kW"]} kW moves on a level road against a resistance of {co(d["k"])}v² N, where v is the speed. {nm} says the maximum speed is {d["P"]}/{u3(d["k"])} = {u3(d["P"] / d["k"])} {MS}. Explain the error.',
                 f'At maximum speed P/v = kv², so v³ = P/k and v = {n3(d["vq"])} {MS}.', 'B1 P/v = kv²; B1 correct speed')
    if not d['vdown']:
        return None
    return Q(f'Explain why the same car (power {d["kW"]} kW, resistance {d["R"]} N, mass {d["m"]} kg) has a higher maximum speed down a hill with sin α = {num(d["s"])} than on the level, and find it.',
             f'Down the hill the weight component helps: P/v = R − mg sin α, so v = {d["P"]}/({d["R"]} − {u3(d["up"])}) = {n3(d["vdown"])} {MS}.', 'B1 weight component assists; B1 value')


@vr203.add('C3', (1, 2, 3, 4, 5), 'numerical')
def vr203_calc(r, D):
    d = slope_pw(r, D)
    if not d:
        return None
    if D <= 2:
        return Q(f'A car of mass {d["m"]} kg climbs a hill inclined at α, where sin α = {num(d["s"])}, against a constant resistance of {d["R"]} N. Its engine works at {d["kW"]} kW. Find its maximum speed up the hill.', f'{n3(d["vup"])} {MS}',
                 'M1 driving force = R + mg sin α; A1 force; A1 speed')
    if D == 3:
        v = r.choice([x for x in (5, 8, 10, 12, 15) if x < d['vup']] or [None])
        if v is None:
            return None
        a = (d['P'] / v - d['R'] - d['up']) / d['m']
        return Q(f'A car of mass {d["m"]} kg, with engine working at {d["kW"]} kW, climbs a hill inclined at α, where sin α = {num(d["s"])}, against a resistance of {d["R"]} N. Find its acceleration when its speed is {v} {MS}.', f'{n3(a)} {MS2}',
                 'M1 F = P/v; M1 N2L along the slope; A1 a')
    if D == 4:
        return Q(f'A car with engine power {d["kW"]} kW moves on a level road against a resistance of {co(d["k"])}v² N. Find its maximum speed.', f'{n3(d["vq"])} {MS}', 'M1 P/v = kv²; A1 v³; A1 speed')
    k = r.choice([10, 20, 25, 30, 40, 50])
    vk = math.sqrt(d['P'] / k)
    v = vk / 2
    a = (d['P'] / v - k * v) / d['m']
    return Q(f'A car of mass {d["m"]} kg with power {d["kW"]} kW moves on a level road against a resistance of {k}v N. Find its maximum speed and its acceleration when it is moving at half this speed.', f'{n3(vk)} {MS}; {n3(a)} {MS2}',
             'M1 P/v = kv; A1 v; M1 N2L at half speed; A1 a')


def vr203_c4(r, D):
    d = slope_pw(r, D)
    if not d:
        return None
    v = r.choice([x for x in (5, 8, 10, 12) if x < d['vup']] or [None])
    if v is None:
        return None
    a = (d['P'] / v - d['R'] - d['up']) / d['m']
    intro = f'A car of mass {d["m"]} kg has an engine of power {d["kW"]} kW. The resistance to motion is constant at {d["R"]} N. A hill is inclined at α to the horizontal, where sin α = {num(d["s"])}.'
    parts = [
        P('Find the maximum speed of the car on a level road.', f'{n3(d["P"] / d["R"])} {MS}', 'M1 P/v = R; A1 speed'),
        P('Find the maximum speed of the car up the hill.', f'{n3(d["vup"])} {MS}', 'M1 includes mg sin α; A1 speed'),
        P(f'Find the acceleration of the car up the hill at the instant its speed is {v} {MS}.', f'{n3(a)} {MS2}', 'M1 P/v − R − mg sin α = ma; A1 a'),
        P('Find the maximum speed of the car down the hill.', f'{n3(d["vdown"])} {MS}' if d['vdown'] else None, 'M1 P/v = R − mg sin α; A1 speed'),
    ]
    if not d['vdown']:
        parts = parts[:3]
    return cmp_(r, intro, parts)


vr203.add('C4', (2, 3, 4, 5))(vr203_c4)

CHAPTERS[20] = [we201, pw202, vr203]


_finalise()
