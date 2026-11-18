"""CBSE class 12 maths (NCERT Mathematics XII, 041) families, chapters 5-9 (calculus and differential equations).

Calculus variants carry private check data (keys starting with '_', dropped on write) so the accuracy
script can test every derivative, antiderivative, definite integral and ODE solution numerically:
    _d   = (f, f', x-sample)          derivative
    _i   = (integrand, antiderivative, x-sample)
    _v   = (callable returning the exact value as float, numeric estimate callable)
    _ode = (rhs(x, y), y(x), x-sample)
"""
from __future__ import annotations

import math
from fractions import Fraction as Fr

from qbank import F, mcq, ar, num, name, two_names, inr, num_distractors, CITIES
from g12_maths_h import Q, mcqbank, arbank, xbank, fn, fz, fpar, poly, term, pif, dist3, surd

S = 'cbse-g12-maths-ch'
SUPMAP = str.maketrans('0123456789+-−xtn()', '⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁻ˣᵗⁿ⁽⁾')


def supx(s: str) -> str:
    return s.translate(SUPMAP)


def co(c) -> str:
    """Coefficient in front of a symbol: 1 -> '', −1 -> '−', 3/2 -> '(3/2)'."""
    c = Fr(c)
    if c == 1:
        return ''
    if c == -1:
        return '−'
    if c.denominator != 1:
        return f'({fn(c)})'
    return fn(c)


def ex(a, b=0) -> str:
    """e^(ax + b) with superscripts, e.g. e³ˣ⁺¹."""
    return 'e' + supx(poly([a, b]).replace(' ', ''))


def opi(v) -> str:
    """v/π as text: 3 -> 3/π, 1/81 -> 1/(81π)."""
    v = Fr(v)
    return f'{fz(v)}/π' if v.denominator == 1 else f'{fz(v.numerator)}/({v.denominator}π)'


def lin(a, b, v='x') -> str:
    return poly([a, b], v)


def mono(c, n, v='x', first=False) -> str:
    """Signed term c·vⁿ written as 2x³/3, −x⁴/4, 5x, 7."""
    c = Fr(c)
    if c == 0:
        return ''
    sgn = '−' if c < 0 else '+'
    a = abs(c)
    p, q = a.numerator, a.denominator
    vv = '' if n == 0 else v + ('' if n == 1 else supx(str(n)))
    if n == 0:
        body = fn(a)
    else:
        body = ('' if p == 1 else str(p)) + vv + ('' if q == 1 else f'/{q}')
    if first:
        return ('−' if c < 0 else '') + body
    return f' {sgn} {body}'


def polyF(terms, v='x') -> str:
    """terms: list of (coefficient, power), highest power first."""
    s = ''
    for c, n in terms:
        s += mono(c, n, v, first=(s == ''))
    return s or '0'


def peval(terms, x):
    return sum(float(c) * x ** n for c, n in terms)


def simpson(f, a, b, n=2000):
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(a + i * h)
    return s * h / 3


def lnx(s):
    return f'log|{s}|'


# ======================================================================= ch05 Continuity and Differentiability

def c5s1_k_lin(r):
    while True:
        a = r.choice([-3, -2, -1, 1, 2, 3, 4, 5])
        p, q, s = r.randint(-6, 6), r.choice([-3, -2, 2, 3, 4, 5]), r.randint(-8, 8)
        k = Fr(q * a + s - p, a)
        if k.denominator <= 3:
            break
    f1 = f'kx{term(p, "")}' if p else 'kx'
    return Q(f'Find the value of k so that the function f(x) = {f1} for x ≤ {a}, and f(x) = {poly([q, s])} for x > {a}, is continuous at x = {a}.', f'k = {fz(k)}',
             f'LHL = f({a}) = {a}k {"+" if p >= 0 else "−"} {abs(p)}; RHL = {q}({a}) {"+" if s >= 0 else "−"} {abs(s)} = {q * a + s} (1 mark); equate ⇒ k = {fz(k)} (1 mark).',
             dist3(f'k = {fz(k)}', [f'k = {fz(-k)}' if k else 'k = 1', f'k = {fz(Fr(q * a + s + p, a))}', f'k = {fz(Fr(q * a + s - p, -a) + 1)}']))


def c5s1_k_quot(r):
    kind = r.randint(0, 2)
    if kind == 0:
        a, b = r.sample(range(-6, 8), 2)
        num_ = poly([1, -(a + b), a * b])
        k = a - b
        return Q(f'Find k if f(x) = ({num_})/({poly([1, -a])}) for x ≠ {a} and f({a}) = k is continuous at x = {a}.', f'k = {k}',
                 f'For x ≠ {a}, f(x) = {poly([1, -b])}; limit as x → {a} is {k} = k.', num_distractors(k, a + b, -k, a * b))
    if kind == 1:
        a, b = r.sample(range(1, 10), 2)
        k = Fr(a, b)
        return Q(f'Find k if f(x) = sin {a}x/({b}x) for x ≠ 0 and f(0) = k is continuous at x = 0.'.replace('sin 1x', 'sin x').replace('(1x)', 'x'), f'k = {fz(k)}',
                 f'lim sin {a}x/({b}x) = ({a}/{b}) lim sin {a}x/({a}x) = {fz(k)}.', dist3(f'k = {fz(k)}', [f'k = {fz(Fr(b, a))}', 'k = 1', f'k = {a * b}', 'k = 0']))
    a = r.randint(1, 6)
    k = Fr(a * a, 2)
    return Q(f'Find k if f(x) = (1 − cos {a}x)/x² for x ≠ 0 and f(0) = k is continuous at x = 0.'.replace('cos 1x', 'cos x'), f'k = {fz(k)}',
             f'1 − cos {a}x = 2 sin²({fz(Fr(a, 2))}x); limit = 2 × ({fz(Fr(a, 2))})² = {fz(k)}.', dist3(f'k = {fz(k)}', [f'k = {a * a}', f'k = {fz(Fr(a, 2))}', 'k = 0', 'k = 1/2']))


def c5s1_two(r):
    p, q = sorted(r.sample(range(-3, 12), 2))
    a = r.choice([-3, -2, -1, 1, 2, 3, 4])
    b = r.randint(-8, 8)
    L, R = a * p + b, a * q + b
    return Q(f'Find a and b such that f(x) = {L} for x ≤ {p}, f(x) = ax + b for {p} < x < {q}, and f(x) = {R} for x ≥ {q} is a continuous function.', f'a = {a}, b = {b}',
             f'Continuity at x = {p}: {p}a + b = {L} (1 mark); at x = {q}: {q}a + b = {R} (1 mark); solving, a = {a}, b = {b} (1 mark).',
             [f'a = {b}, b = {a}', f'a = {-a}, b = {b + 2 * a * p}', f'a = {a + 1}, b = {b - p}'])


def c5s1_check(r):
    c = r.randint(-4, 5)
    p, s = r.choice([-2, -1, 1, 2, 3]), r.randint(-5, 5)
    q = r.choice([-2, 1, 2, 3, 4])
    t = r.randint(-5, 5)
    left, right = p * c + s, q * c + t
    cont = left == right
    if r.random() < 0.5 and not cont:
        t += left - right
        right = left
        cont = True
    return Q(f'Is the function f(x) = {poly([p, s])} for x ≤ {c}, f(x) = {poly([q, t])} for x > {c} continuous at x = {c}? Justify.', 'Yes' if cont else 'No',
             f'LHL = f({c}) = {left}; RHL = {right}; ' + ('equal, so continuous.' if cont else 'unequal, so discontinuous.'),
             ['No' if cont else 'Yes', 'Only from the left', 'Cannot be decided'])


def c5s1_mcq(r):
    return mcqbank([
        ('The greatest integer function f(x) = [x] is discontinuous at …', 'every integer', ['x = 0 only', 'no point', 'every non-integer'], 'Left and right limits differ by 1 at each integer.'),
        ('The function f(x) = |x| is …', 'continuous everywhere', ['discontinuous at x = 0', 'continuous only for x > 0', 'discontinuous at every integer'], '|x| is continuous on R.'),
        ('The function f(x) = 1/x is …', 'continuous on its domain R − {0}', ['continuous on R', 'discontinuous at every point', 'not continuous at x = 1'], 'Quotient of continuous functions.'),
        ('The function tan x is discontinuous at …', 'odd multiples of π/2', ['multiples of π', 'x = 0', 'no point'], 'tan x is not defined where cos x = 0.'),
        ('Every polynomial function is …', 'continuous everywhere', ['continuous only at integers', 'discontinuous at its zeros', 'continuous only for x > 0'], 'Standard result.'),
        ('If f and g are continuous at x = c, which of the following may fail to be continuous at c?', 'f/g', ['f + g', 'f − g', 'fg'], 'f/g needs g(c) ≠ 0.'),
        ('The signum function is discontinuous at …', 'x = 0', ['x = 1', 'every integer', 'no point'], 'LHL = −1, RHL = 1 at 0.'),
    ])(r)


def c5s1_ar(r):
    a = r.randint(1, 9)
    return arbank([
        (f'f(x) = |x − {a}| is continuous at x = {a}.', 'The modulus function is continuous everywhere.', 'a', 'Composition of continuous functions.'),
        (f'f(x) = [x] is continuous at x = {a}.', 'The greatest integer function is discontinuous at every integer.', 'd', f'{a} is an integer, so A is false; R is true.'),
        (f'f(x) = sin x + x{supx(str(a))} is continuous on R.', 'The sum of two continuous functions is continuous.', 'a', 'sin x and the polynomial are continuous.'),
        (f'f(x) = 1/(x − {a}) is continuous at x = {a}.', 'A rational function is continuous at every point of its domain.', 'd', f'{a} is not in the domain, so A is false; R is true.'),
        ('f(x) = cos x is continuous everywhere.', 'cos x is differentiable everywhere.', 'a', 'Differentiability implies continuity.'),
    ])(r)


def c5s1_case(r):
    base = r.choice([25, 30, 40, 50])
    rate1, rate2 = r.choice([12, 14, 15, 16]), r.choice([10, 11, 12])
    c = r.choice([5, 8, 10])
    k = base + rate1 * c - rate2 * c
    city = r.choice(CITIES)
    return Q((f'An auto-rickshaw fare scheme in {city} charges f(x) = {base} + {rate1}x rupees for x ≤ {c} km and f(x) = k + {rate2}x rupees for x > {c} km. '
              f'(i) Find f({c}). (ii) Find the value of k for which the fare is a continuous function of distance. (iii) With this k, find the fare for a {c + 4} km ride and say whether the fare function is continuous at x = {c}.'),
             f'(i) ₹{base + rate1 * c} (ii) k = {k} (iii) ₹{k + rate2 * (c + 4)}; yes, continuous',
             f'(i) 1 mark (ii) RHL k + {rate2 * c} = {base + rate1 * c} (1 mark) (iii) fare and reason (2 marks).')


def c5s1_explain(r):
    return xbank([
        ('Show that the function f(x) = |x| is continuous at x = 0.', 'LHL = RHL = f(0) = 0.', 'lim(x→0⁻) (−x) = 0 and lim(x→0⁺) x = 0 equal f(0) = 0 (2 marks).'),
        ('Explain why f(x) = [x] is discontinuous at x = 2.', 'LHL = 1, RHL = 2.', 'Left limit 1 ≠ right limit 2 = f(2) (2 marks).'),
        ('Discuss the continuity of f(x) = sin x · cos x.', 'Continuous everywhere.', 'Product of two continuous functions (2 marks).'),
        ('Explain why a function continuous at a point need not be differentiable there, with an example.', 'f(x) = |x| at x = 0.', 'Continuous at 0, but left derivative −1 ≠ right derivative 1 (2 marks).'),
    ])(r)


# ---- st2 differentiability and chain rule

def _chain(r):
    a = r.choice([2, 3, 4, 5, -2, -3])
    b = r.randint(-5, 6)
    n = r.choice([3, 4, 5, 6, 7])
    k = r.randint(1, 5)
    L = lin(a, b)
    kind = r.randint(0, 9)
    if kind == 0:
        return (f'sin({poly([a, 0, b])})', f'{co(2 * a)}x cos({poly([a, 0, b])})', lambda x: math.sin(a * x * x + b), lambda x: 2 * a * x * math.cos(a * x * x + b))
    if kind == 1:
        return (f'cos({L})', f'{co(-a)}sin({L})', lambda x: math.cos(a * x + b), lambda x: -a * math.sin(a * x + b))
    if kind == 2:
        return (f'({L}){supx(str(n))}', f'{n * a}({L}){supx(str(n - 1))}', lambda x: (a * x + b) ** n, lambda x: n * a * (a * x + b) ** (n - 1))
    if kind == 3:
        aa = abs(a)
        bb = abs(b) + 1
        return (f'√({poly([aa, 0, bb])})', f'{co(aa)}x/√({poly([aa, 0, bb])})', lambda x: math.sqrt(aa * x * x + bb), lambda x: aa * x / math.sqrt(aa * x * x + bb))
    if kind == 4:
        return (f'tan({L})', f'{co(a)}sec²({L})', lambda x: math.tan(a * x + b), lambda x: a / math.cos(a * x + b) ** 2)
    if kind == 5:
        aa = abs(a)
        return (f'sin²({aa}x)', f'{co(aa)}sin({2 * aa}x)', lambda x: math.sin(aa * x) ** 2, lambda x: aa * math.sin(2 * aa * x))
    if kind == 6:
        return (f'sec({L})', f'{co(a)}sec({L}) tan({L})', lambda x: 1 / math.cos(a * x + b), lambda x: a * math.tan(a * x + b) / math.cos(a * x + b))
    if kind == 7:
        return (f'sin(x{supx(str(n))})', f'{n}x{supx(str(n - 1))} cos(x{supx(str(n))})', lambda x: math.sin(x ** n), lambda x: n * x ** (n - 1) * math.cos(x ** n))
    if kind == 8:
        return (f'cos²({lin(1, b) if b else "x"})'.replace('(x)', 'x'), f'−sin({lin(2, 2 * b)})' if b else '−sin 2x', lambda x: math.cos(x + b) ** 2, lambda x: -math.sin(2 * x + 2 * b))
    return (f'cos(√x)', '−sin(√x)/(2√x)', lambda x: math.cos(math.sqrt(x)), lambda x: -math.sin(math.sqrt(x)) / (2 * math.sqrt(x)))


def c5s2_chain(r):
    f, df, fx, dfx = _chain(r)
    w = df.replace('cos', 'sin', 1) if 'cos' in df else df.replace('sin', 'cos', 1) if 'sin' in df else df + ' + 1'
    w2 = ('−' + df) if not df.startswith('−') else df[1:]
    return Q(f'Differentiate {f} with respect to x.', df, f'Chain rule: d/dx [{f}] = {df}.', dist3(df, [w, w2, df + ' + C']), _d=(fx, dfx, 0.3))


def c5s2_diffab(r):
    c = r.randint(-3, 3)
    p = r.randint(-5, 5)
    m = 2 * c
    n = p - c * c
    return Q(f'Find a and b if f(x) = {poly([1, 0, p])} for x ≤ {c} and f(x) = ax + b for x > {c} is differentiable at x = {c}.', f'a = {m}, b = {n}',
             f'Continuity: {c * c + p} = {c}a + b (1 mark); equal derivatives: 2({c}) = a (1 mark) ⇒ a = {m}, b = {n} (1 mark).',
             [f'a = {n}, b = {m}', f'a = {m}, b = {n + c * c}', f'a = {c}, b = {c * c + p - c * c}'])


def c5s2_value(r):
    a, b = r.choice([2, 3, -2, 4]), r.randint(-4, 4)
    n = r.choice([2, 3, 4])
    x0 = r.randint(-2, 3)
    val = n * a * (a * x0 + b) ** (n - 1)
    return Q(f'If y = ({lin(a, b)}){supx(str(n))}, find dy/dx at x = {x0}.', fz(val), f'dy/dx = {n * a}({lin(a, b)}){supx(str(n - 1)) if n > 2 else ""}; at x = {x0}: {fz(val)}.',
             num_distractors(val, n * (a * x0 + b) ** (n - 1), val * 2, (a * x0 + b) ** n), _d=(lambda x: (a * x + b) ** n, lambda x: n * a * (a * x + b) ** (n - 1), x0 + 0.17))


def c5s2_mcq(r):
    return mcqbank([
        ('The function f(x) = |x| at x = 0 is …', 'continuous but not differentiable', ['differentiable but not continuous', 'neither continuous nor differentiable', 'both continuous and differentiable'], 'Corner at 0.'),
        ('If a function is differentiable at a point, then it is …', 'continuous at that point', ['discontinuous at that point', 'constant near that point', 'not defined at that point'], 'Differentiability ⇒ continuity.'),
        ('The derivative of sin(x²) with respect to x is …', '2x cos(x²)', ['cos(x²)', '2x sin(x²)', '−2x cos(x²)'], 'Chain rule.'),
        ('The function f(x) = |x − 3| is not differentiable at …', 'x = 3', ['x = 0', 'x = −3', 'any point'], 'Corner at x = 3.'),
        ('The greatest integer function f(x) = [x], 0 < x < 3, is not differentiable at …', 'x = 1 and x = 2', ['x = 1 only', 'no point', 'every point'], 'It is discontinuous there.'),
        ('d/dx [cos(sin x)] = …', '−sin(sin x) cos x', ['sin(sin x) cos x', '−cos(sin x) sin x', '−sin(cos x)'], 'Chain rule.'),
    ])(r)


def c5s2_ar(r):
    a = r.randint(1, 9)
    return arbank([
        (f'f(x) = |x − {a}| is not differentiable at x = {a}.', f'The left-hand derivative at x = {a} is −1 and the right-hand derivative is 1.', 'a', 'Unequal one-sided derivatives.'),
        (f'f(x) = |x − {a}| is continuous at x = {a}.', 'Every continuous function is differentiable.', 'c', 'A true; R false (|x| at 0).'),
        (f'd/dx (sin {a}x) = {a} cos {a}x.'.replace('sin 1x', 'sin x').replace('1 cos 1x', 'cos x'), 'If y = f(u) and u = g(x), then dy/dx = f′(u)·g′(x).', 'a', 'Chain rule.'),
        ('f(x) = x|x| is differentiable at x = 0.', '|x| is not differentiable at x = 0.', 'b', 'Both true: f′(0) = lim h|h|/h = 0; R is true but does not explain A.'),
    ])(r)


def c5s2_long(r):
    f, df, fx, dfx = _chain(r)
    g, dg, gx, dgx = _chain(r)
    if f == g:
        raise ValueError
    return Q(f'Differentiate with respect to x: (i) {f} (ii) {g}. Also show that f(x) = |x − {r.randint(1, 5)}| is continuous but not differentiable at its corner point.',
             f'(i) {df} (ii) {dg}; |x − c| has LHD −1 ≠ RHD 1 at x = c',
             '(i) chain rule (2 marks) (ii) chain rule (1 mark); continuity and unequal one-sided derivatives (2 marks).', _d=(fx, dfx, 0.4))


def c5s2_case(r):
    a, b = r.choice([2, 3, 4]), r.randint(1, 6)
    who = name(r)
    return Q((f'{who} models the height of a swing seat by h(t) = {b} + sin({a}t) metres, t in seconds. (i) Is h continuous for all t? (ii) Find h′(t). '
              f'(iii) Find h′(0) and h′(π/{2 * a}), and interpret the second value.'),
             f'(i) Yes (ii) h′(t) = {a} cos({a}t) (iii) h′(0) = {a} m/s, h′(π/{2 * a}) = 0: the seat is momentarily at rest (highest point)',
             '(i) sum of continuous functions (1 mark) (ii) chain rule (1 mark) (iii) values and meaning (2 marks).', _d=(lambda t: b + math.sin(a * t), lambda t: a * math.cos(a * t), 0.2))


# ---- st3 implicit and inverse trigonometric functions

def c5s3_implicit(r):
    while True:
        a, b, c = r.choice([1, 2, 3]), r.choice([-2, -1, 1, 2, 3]), r.choice([1, 2, 3])
        x0, y0 = r.randint(-3, 3), r.randint(-3, 3)
        k = a * x0 * x0 + b * x0 * y0 + c * y0 * y0
        den = b * x0 + 2 * c * y0
        if den != 0 and k > 0:
            break
    curve = (term(a, 'x', first=True, power=2) + term(b, 'xy') + term(c, 'y', power=2) + f' = {k}')
    val = Fr(-(2 * a * x0 + b * y0), den)
    dy = f'−({lin(2 * a, 0)} {"+" if b > 0 else "−"} {co(abs(b))}y)/({lin(b, 0)} + {co(2 * c)}y)'.replace(' 0)', ')')
    return Q(f'Find dy/dx at the point ({x0}, {y0}) for the curve {curve}.', fz(val),
             f'Differentiate: {2 * a}x + {b}(y + x dy/dx) + {2 * c}y dy/dx = 0 ⇒ dy/dx = −({2 * a}x + {b}y)/({b}x + {2 * c}y) (2 marks); at ({x0}, {y0}): {fz(val)} (1 mark).',
             dist3(fz(val), [fz(-val) if val else '1', fz(Fr(2 * a * x0 + b * y0, den) + 1), fz(Fr(den, 2 * a * x0 + b * y0)) if 2 * a * x0 + b * y0 else '2']))


def c5s3_implicit2(r):
    kind = r.randint(0, 3)
    a = r.randint(2, 9)
    if kind == 0:
        return Q(f'Find dy/dx if x² + xy + y² = {a * 10}.', 'dy/dx = −(2x + y)/(x + 2y)', '2x + y + x dy/dx + 2y dy/dx = 0.', ['dy/dx = (2x + y)/(x + 2y)', 'dy/dx = −(x + 2y)/(2x + y)', 'dy/dx = −2x/(2y)'])
    if kind == 1:
        return Q(
            f'Find dy/dx if xy + y² = tan x + {a}y.', f'(sec²x − y)/(x + 2y − {a})',
            f'y + x dy/dx + 2y dy/dx = sec²x + {a} dy/dx ⇒ dy/dx = (sec²x − y)/(x + 2y − {a}).', [f'(sec²x + y)/(x + 2y − {a})', f'(sec²x − y)/(x + 2y + {a})', f'(y − sec²x)/(x + 2y)'])
    if kind == 2:
        b = r.randint(2, 9)
        return Q(f'Find dy/dx if {a}x + {b}y = sin x.', f'(cos x − {a})/{b}', f'{a} + {b} dy/dx = cos x.', [f'(cos x + {a})/{b}', f'(sin x − {a})/{b}', f'({a} − cos x)/{b}'])
    return Q(f'Find dy/dx if sin²y + cos xy = {a}.'.replace(f'= {a}', 'k (a constant)'), 'y sin xy/(sin 2y − x sin xy)',
             '2 sin y cos y dy/dx − sin xy (y + x dy/dx) = 0.', ['−y sin xy/(sin 2y − x sin xy)', 'y sin xy/(sin 2y + x sin xy)', 'y cos xy/(sin 2y − x cos xy)'])


INV_D = [
    ('sin⁻¹(2x√(1 − x²)), −1/√2 < x < 1/√2', '2/√(1 − x²)', lambda x: math.asin(2 * x * math.sqrt(1 - x * x)), lambda x: 2 / math.sqrt(1 - x * x), 0.3),
    ('cos⁻¹((1 − x²)/(1 + x²)), 0 < x < 1', '2/(1 + x²)', lambda x: math.acos((1 - x * x) / (1 + x * x)), lambda x: 2 / (1 + x * x), 0.4),
    ('tan⁻¹((3x − x³)/(1 − 3x²)), −1/√3 < x < 1/√3', '3/(1 + x²)', lambda x: math.atan((3 * x - x ** 3) / (1 - 3 * x * x)), lambda x: 3 / (1 + x * x), 0.2),
    ('sin⁻¹((1 − x²)/(1 + x²)), 0 < x < 1', '−2/(1 + x²)', lambda x: math.asin((1 - x * x) / (1 + x * x)), lambda x: -2 / (1 + x * x), 0.5),
    ('sin⁻¹(2x/(1 + x²)), −1 < x < 1', '2/(1 + x²)', lambda x: math.asin(2 * x / (1 + x * x)), lambda x: 2 / (1 + x * x), 0.3),
    ('cos⁻¹(2x/(1 + x²)), −1 < x < 1', '−2/(1 + x²)', lambda x: math.acos(2 * x / (1 + x * x)), lambda x: -2 / (1 + x * x), 0.3),
    ('sin⁻¹(3x − 4x³), −1/2 < x < 1/2', '3/√(1 − x²)', lambda x: math.asin(3 * x - 4 * x ** 3), lambda x: 3 / math.sqrt(1 - x * x), 0.2),
    ('cos⁻¹(4x³ − 3x), 1/2 < x < 1', '−3/√(1 − x²)', lambda x: math.acos(4 * x ** 3 - 3 * x), lambda x: -3 / math.sqrt(1 - x * x), 0.7),
    ('tan⁻¹(2x/(1 − x²)), −1 < x < 1', '2/(1 + x²)', lambda x: math.atan(2 * x / (1 - x * x)), lambda x: 2 / (1 + x * x), 0.4),
    ('cos⁻¹(2x² − 1), 0 < x < 1', '−2/√(1 − x²)', lambda x: math.acos(2 * x * x - 1), lambda x: -2 / math.sqrt(1 - x * x), 0.6),
]


def c5s3_invsub(r):
    f, d, fx, dfx, x0 = r.choice(INV_D)
    w = [x for x in ['2/√(1 − x²)', '2/(1 + x²)', '3/(1 + x²)', '−2/(1 + x²)', '3/√(1 − x²)', '1/(1 + x²)', '−2/√(1 − x²)', '−3/√(1 − x²)'] if x != d]
    r.shuffle(w)
    return Q(f'Find dy/dx if y = {f}.', d, 'Use a trigonometric substitution (x = sin θ, cos θ or tan θ) to simplify y first, then differentiate.', w[:3], _d=(fx, dfx, x0))


def c5s3_inv(r):
    a = r.choice([2, 3, 4, 5])
    b = r.randint(-4, 4)
    kind = r.randint(0, 3)
    if kind == 0:
        return Q(f'Find dy/dx if y = sin⁻¹({a}x).', f'{a}/√(1 − {a * a}x²)', f'd/dx sin⁻¹u = u′/√(1 − u²) with u = {a}x.', [f'1/√(1 − {a * a}x²)', f'{a}/(1 + {a * a}x²)', f'−{a}/√(1 − {a * a}x²)'],
                 _d=(lambda x: math.asin(a * x), lambda x: a / math.sqrt(1 - a * a * x * x), 0.1))
    if kind == 1:
        L = lin(a, b)
        return Q(f'Find dy/dx if y = tan⁻¹({L}).', f'{a}/(1 + ({L})²)', f'd/dx tan⁻¹u = u′/(1 + u²).', [f'1/(1 + ({L})²)', f'{a}/√(1 − ({L})²)', f'−{a}/(1 + ({L})²)'],
                 _d=(lambda x: math.atan(a * x + b), lambda x: a / (1 + (a * x + b) ** 2), 0.3))
    if kind == 2:
        return Q('Find dy/dx if y = cos⁻¹(x²), 0 < x < 1.', '−2x/√(1 − x⁴)', 'd/dx cos⁻¹u = −u′/√(1 − u²).', ['2x/√(1 − x⁴)', '−1/√(1 − x⁴)', '−2x/(1 + x⁴)'],
                 _d=(lambda x: math.acos(x * x), lambda x: -2 * x / math.sqrt(1 - x ** 4), 0.5))
    return Q(f'Find dy/dx if y = sin⁻¹(x/{a}), −{a} < x < {a}.', f'1/√({a * a} − x²)', f'(1/{a})/√(1 − x²/{a * a}) = 1/√({a * a} − x²).', [f'{a}/√({a * a} − x²)', f'1/√(1 − x²)', f'1/({a * a} + x²)'],
             _d=(lambda x: math.asin(x / a), lambda x: 1 / math.sqrt(a * a - x * x), 0.5))


def c5s3_mcq(r):
    return mcqbank([
        ('If x² + y² = 25, then dy/dx = …', '−x/y', ['x/y', '−y/x', 'y/x'], '2x + 2y dy/dx = 0.'),
        ('d/dx (sin⁻¹x) = …', '1/√(1 − x²)', ['−1/√(1 − x²)', '1/(1 + x²)', '1/√(1 + x²)'], 'Standard derivative.'),
        ('d/dx (cos⁻¹x) = …', '−1/√(1 − x²)', ['1/√(1 − x²)', '−1/(1 + x²)', '1/(1 + x²)'], 'Standard derivative.'),
        ('d/dx (tan⁻¹x) = …', '1/(1 + x²)', ['−1/(1 + x²)', '1/√(1 − x²)', 'sec²x'], 'Standard derivative.'),
        ('If xy = 1, then dy/dx = …', '−y/x', ['y/x', '−x/y', '1/x'], 'y + x dy/dx = 0.'),
        ('d/dx (cot⁻¹x) = …', '−1/(1 + x²)', ['1/(1 + x²)', '−1/√(1 − x²)', '−cosec²x'], 'Standard derivative.'),
    ])(r)


def c5s3_ar(r):
    a = r.randint(2, 9)
    return arbank([
        (f'If x² + y² = {a * a}, then dy/dx = −x/y.', 'Differentiating both sides with respect to x gives 2x + 2y dy/dx = 0.', 'a', 'Implicit differentiation.'),
        ('d/dx [sin⁻¹(2x√(1 − x²))] = 2/√(1 − x²) for −1/√2 < x < 1/√2.', 'With x = sin θ, 2x√(1 − x²) = sin 2θ and 2θ ∈ (−π/2, π/2).', 'a', 'y = 2 sin⁻¹x on that interval.'),
        (f'd/dx [tan⁻¹({a}x)] = 1/(1 + {a * a}x²).', 'd/dx (tan⁻¹x) = 1/(1 + x²).', 'd', f'Chain rule gives {a}/(1 + {a * a}x²); A false, R true.'),
        ('If y = sin⁻¹x, then dy/dx = 1/√(1 − x²) for −1 < x < 1.', 'sin y = x and cos y > 0 for −π/2 < y < π/2.', 'a', 'dy/dx = 1/cos y = 1/√(1 − x²).'),
    ])(r)


def c5s3_case(r):
    rr = r.choice([5, 10, 13, 17, 25])
    pts = {5: (3, 4), 10: (6, 8), 13: (5, 12), 17: (8, 15), 25: (7, 24)}[rr]
    x0, y0 = pts if r.random() < 0.5 else (pts[1], pts[0])
    who = name(r)
    return Q((f'{who} designs a circular garden path given by x² + y² = {rr * rr} (units in metres). (i) Find dy/dx by implicit differentiation. (ii) Find the slope of the path at ({x0}, {y0}). '
              f'(iii) Find the slope of the radius to that point and show that the tangent is perpendicular to the radius.'),
             f'(i) −x/y (ii) {fz(Fr(-x0, y0))} (iii) {fz(Fr(y0, x0))}; product of slopes = −1',
             '(i) 1 mark (ii) 1 mark (iii) 2 marks.')


def c5s3_long(r):
    f, d, fx, dfx, x0 = r.choice(INV_D)
    a = r.randint(2, 6)
    return Q(f'(i) If y = {f}, find dy/dx using a suitable substitution. (ii) If x² + y² + {a}xy = 1, find dy/dx.', f'(i) {d} (ii) dy/dx = −(2x + {a}y)/(2y + {a}x)',
             '(i) substitution and simplification (2 marks), derivative (1 mark) (ii) implicit differentiation (2 marks).', _d=(fx, dfx, x0))


# ---- st4 exponential and logarithmic functions; logarithmic differentiation

def _expd(r):
    a = r.choice([2, 3, 4, 5, -2, -3])
    b = r.randint(-4, 5)
    k = r.choice([2, 3, 4, 5])
    kind = r.randint(0, 8)
    if kind == 0:
        return (ex(a, b), f'{co(a)}{ex(a, b)}', lambda x: math.exp(a * x + b), lambda x: a * math.exp(a * x + b))
    if kind == 1:
        aa = abs(a)
        return (f'log({lin(aa, abs(b) + 1)})', f'{aa}/({lin(aa, abs(b) + 1)})', lambda x: math.log(aa * x + abs(b) + 1), lambda x: aa / (aa * x + abs(b) + 1))
    if kind == 2:
        return ('log(sin x)', 'cot x', lambda x: math.log(math.sin(x)), lambda x: 1 / math.tan(x))
    if kind == 3:
        return ('e^(sin x)', 'cos x · e^(sin x)', lambda x: math.exp(math.sin(x)), lambda x: math.cos(x) * math.exp(math.sin(x)))
    if kind == 4:
        return ('log(log x), x > 1', '1/(x log x)', lambda x: math.log(math.log(x)), lambda x: 1 / (x * math.log(x)))
    if kind == 5:
        return (f'{ex(k)} sin x', f'{ex(k)}({k} sin x + cos x)', lambda x: math.exp(k * x) * math.sin(x), lambda x: math.exp(k * x) * (k * math.sin(x) + math.cos(x)))
    if kind == 6:
        return (f'{k}ˣ', f'{k}ˣ log {k}', lambda x: k ** x, lambda x: k ** x * math.log(k))
    if kind == 7:
        return (f'x{supx(str(k))} eˣ', f'x{supx(str(k - 1))}eˣ(x + {k})'.replace('x¹', 'x'), lambda x: x ** k * math.exp(x), lambda x: x ** (k - 1) * math.exp(x) * (x + k))
    return (f'e^(x²)', '2x e^(x²)', lambda x: math.exp(x * x), lambda x: 2 * x * math.exp(x * x))


def c5s4_diff(r):
    f, d, fx, dfx = _expd(r)
    x0 = 1.3
    w = [d + ' + C', ('−' + d) if not d.startswith('−') else d[1:], f]
    return Q(f'Differentiate {f} with respect to x.', d, f'Standard derivatives with the chain/product rule: {d}.', dist3(d, w), _d=(fx, dfx, x0))


def c5s4_xx(r):
    kind = r.randint(0, 4)
    if kind == 0:
        return Q('Find dy/dx if y = xˣ, x > 0.', 'xˣ(1 + log x)', 'log y = x log x ⇒ (1/y) dy/dx = log x + 1.', ['x·xˣ⁻¹', 'xˣ log x', 'xˣ(1 − log x)'], _d=(lambda x: x ** x, lambda x: x ** x * (1 + math.log(x)), 1.4))
    if kind == 1:
        return Q('Find dy/dx if y = x^(sin x), x > 0.', 'x^(sin x)(cos x log x + sin x/x)', 'log y = sin x log x; differentiate both sides.', ['sin x · x^(sin x − 1)', 'x^(sin x) cos x log x', 'x^(sin x)(sin x log x + cos x/x)'],
                 _d=(lambda x: x ** math.sin(x), lambda x: x ** math.sin(x) * (math.cos(x) * math.log(x) + math.sin(x) / x), 1.2))
    if kind == 2:
        return Q('Find dy/dx if y = (sin x)ˣ, 0 < x < π.', '(sin x)ˣ(log sin x + x cot x)', 'log y = x log sin x.', ['x(sin x)ˣ⁻¹ cos x', '(sin x)ˣ log sin x', '(sin x)ˣ(log sin x − x cot x)'],
                 _d=(lambda x: math.sin(x) ** x, lambda x: math.sin(x) ** x * (math.log(math.sin(x)) + x / math.tan(x)), 1.0))
    if kind == 3:
        return Q('Find dy/dx if y = (log x)ˣ, x > 1.', '(log x)ˣ(log(log x) + 1/log x)', 'log y = x log(log x).', ['x(log x)ˣ⁻¹/x', '(log x)ˣ log(log x)', '(log x)ˣ/(x log x)'],
                 _d=(lambda x: math.log(x) ** x, lambda x: math.log(x) ** x * (math.log(math.log(x)) + 1 / math.log(x)), 2.5))
    return Q('Find dy/dx if xʸ = e^(x − y).', 'log x/(1 + log x)²', 'y log x = x − y ⇒ y = x/(1 + log x); differentiate.', ['1/(1 + log x)', 'log x/(1 + log x)', '(1 + log x)/log x'],
             _d=(lambda x: x / (1 + math.log(x)), lambda x: math.log(x) / (1 + math.log(x)) ** 2, 2.0))


def c5s4_prod(r):
    a, b, c = r.sample(range(1, 7), 3)
    x0 = r.randint(0, 3)
    y0 = (x0 + a) * (x0 + b) * (x0 + c)
    s = Fr(1, x0 + a) + Fr(1, x0 + b) + Fr(1, x0 + c)
    val = y0 * s
    return Q(f'Using logarithmic differentiation, find dy/dx at x = {x0} for y = (x + {a})(x + {b})(x + {c}).', fz(val),
             f'log y = log(x + {a}) + log(x + {b}) + log(x + {c}) ⇒ dy/dx = y[1/(x + {a}) + 1/(x + {b}) + 1/(x + {c})] (2 marks); at x = {x0}: {y0} × {fz(s)} = {fz(val)} (1 mark).',
             num_distractors(float(val), y0, float(s), val + 1), _d=(lambda x: (x + a) * (x + b) * (x + c), lambda x: (x + b) * (x + c) + (x + a) * (x + c) + (x + a) * (x + b), x0 + 0.3))


def c5s4_mcq(r):
    return mcqbank([
        ('d/dx (eˣ) = …', 'eˣ', ['x eˣ⁻¹', 'e', 'log x'], 'Standard.'),
        ('d/dx (log x) = …, x > 0', '1/x', ['log x', 'x', 'eˣ'], 'Standard.'),
        ('d/dx (aˣ) = …', 'aˣ log a', ['x aˣ⁻¹', 'aˣ', 'aˣ/log a'], 'aˣ = e^(x log a).'),
        ('Logarithmic differentiation is most useful for functions of the form …', '[u(x)]^(v(x))', ['u(x) + v(x)', 'a polynomial', 'a constant'], 'Take logs to bring the exponent down.'),
        ('d/dx [log(sec x + tan x)] = …', 'sec x', ['tan x', 'sec x tan x', 'sec²x'], '(sec x tan x + sec²x)/(sec x + tan x) = sec x.'),
        ('d/dx (e^(3x)) = …', '3e^(3x)', ['e^(3x)', '3x e^(3x − 1)', 'e^(3x)/3'], 'Chain rule.'),
    ])(r)


def c5s4_ar(r):
    k = r.randint(2, 9)
    return arbank([
        (f'd/dx ({k}ˣ) = {k}ˣ log {k}.', f'{k}ˣ = e^(x log {k}).', 'a', 'Chain rule on e^(x log k).'),
        (f'd/dx ({k}ˣ) = x·{k}ˣ⁻¹.', 'd/dx (xⁿ) = n xⁿ⁻¹.', 'd', 'The power rule needs a constant exponent; A false, R true.'),
        ('d/dx (xˣ) = xˣ(1 + log x).', 'Taking logarithms, log y = x log x.', 'a', 'Logarithmic differentiation gives A.'),
        (f'd/dx [log({k}x)] = 1/x.', f'log({k}x) = log {k} + log x.', 'a', 'Derivative of the constant log k is 0.'),
    ])(r)


def c5s4_case(r):
    P0 = r.choice([1000, 2000, 5000, 500])
    k = r.choice([Fr(1, 10), Fr(1, 5), Fr(1, 20), Fr(3, 10)])
    t0 = r.choice([5, 10, 2])
    who = name(r)
    kt, kP = mono(k, 1, 't', first=True), mono(k, 1, 'P', first=True)
    e0 = 'e' if k * t0 == 1 else f'e^({fz(k * t0)})'
    return Q((f'{who} studies a bacteria culture whose size is P(t) = {P0}e^({kt}) after t hours. (i) Find dP/dt. (ii) Show that dP/dt = {kP}. '
              f'(iii) Find the rate of growth when t = {t0} hours, in terms of e.'),
             f'(i) {fn(P0 * k)}e^({kt}) (ii) dP/dt = {fpar(k)} × {P0}e^({kt}) = {kP} (iii) {fn(P0 * k)}{e0} per hour',
             '(i) 1 mark (ii) 1 mark (iii) 2 marks.')


def c5s4_long(r):
    kind = r.randint(0, 2)
    if kind == 0:
        return Q('Differentiate y = xˣ + (sin x)ˣ with respect to x, 0 < x < π.', 'xˣ(1 + log x) + (sin x)ˣ(log sin x + x cot x)',
                 'Split y = u + v; log u = x log x (2 marks); log v = x log sin x (2 marks); add (1 mark).',
                 _d=(lambda x: x ** x + math.sin(x) ** x, lambda x: x ** x * (1 + math.log(x)) + math.sin(x) ** x * (math.log(math.sin(x)) + x / math.tan(x)), 1.1))
    if kind == 1:
        return Q('If xʸ + yˣ = 1, find dy/dx.', 'dy/dx = −(y xʸ⁻¹ + yˣ log y)/(xʸ log x + x yˣ⁻¹)', 'd(xʸ) = xʸ(y/x + log x · y′); d(yˣ) = yˣ(log y + (x/y) y′) (3 marks); solve (2 marks).')
    a, b, c = r.sample(range(1, 6), 3)
    return Q(f'Differentiate y = √((x − {a})(x − {b})/((x − {c})(x − {a + b + c}))) for x > {a + b + c}.', f'(y/2)[1/(x − {a}) + 1/(x − {b}) − 1/(x − {c}) − 1/(x − {a + b + c})]',
             'Take logs: log y = ½[log(x − a) + log(x − b) − log(x − c) − log(x − d)] (2 marks); differentiate (3 marks).')


# ---- st5 parametric and second-order derivatives

def c5s5_param(r):
    kind = r.randint(0, 3)
    if kind == 0:
        p, q, s = r.choice([1, 2, 3, 4]), r.randint(-3, 3), r.choice([1, 2, 3, -2])
        t0 = r.choice([-2, -1, 1, 2, 3])
        val = Fr(3 * s * t0, 2 * p)
        return Q(f'If x = {mono(p, 2, "t", True)}{term(q, "")}, y = {mono(s, 3, "t", True)}, find dy/dx at t = {t0}.', fz(val),
                 f'dx/dt = {2 * p}t, dy/dt = {3 * s}t²; dy/dx = {mono(Fr(3 * s, 2 * p), 1, 't', first=True)}; at t = {t0}: {fz(val)}.', dist3(fz(val), [fz(Fr(2 * p, 3 * s * t0)), fz(val * t0), fz(-val), fz(val + 1)]))
    if kind == 1:
        a, b = r.sample(range(2, 9), 2)
        return Q(f'If x = {a} cos θ, y = {b} sin θ, find dy/dx at θ = π/4.', f'−{fz(Fr(b, a))}', f'dy/dx = ({b} cos θ)/(−{a} sin θ) = −({fz(Fr(b, a))}) cot θ; at π/4: −{fz(Fr(b, a))}.',
                 [fz(Fr(b, a)), f'−{fz(Fr(a, b))}', f'{fz(Fr(a, b))}'])
    if kind == 2:
        a = r.randint(2, 9)
        return Q(f'If x = {a}t², y = {2 * a}t, find dy/dx.', '1/t', f'dx/dt = {2 * a}t, dy/dt = {2 * a} ⇒ dy/dx = 1/t.', ['t', '2t', '−1/t'])
    a = r.randint(2, 6)
    return Q(f'If x = {a}(θ − sin θ), y = {a}(1 + cos θ), find dy/dx.', '−cot(θ/2)', '−sin θ/(1 − cos θ) = −2 sin(θ/2)cos(θ/2)/(2 sin²(θ/2)).', ['cot(θ/2)', '−tan(θ/2)', 'tan(θ/2)'])


def c5s5_second(r):
    kind = r.randint(0, 3)
    a = r.choice([2, 3, 4, 5])
    if kind == 0:
        m, n = r.sample([-3, -2, -1, 1, 2, 3, 4], 2)
        s, p = m + n, m * n
        eq = 'd²y/dx²' + (f' − {co(s)}dy/dx' if s > 0 else f' + {co(-s)}dy/dx' if s < 0 else '') + term(p, 'y') + ' = 0'
        return Q(f'If y = A{ex(m)} + B{ex(n)}, show that {eq}.', eq, f'dy/dx = {co(m)}A{ex(m)}{term(n, "B" + ex(n))}; d²y/dx² = {co(m * m)}A{ex(m)}{term(n * n, "B" + ex(n))} (2 marks); substitute (1 mark).')
    if kind == 1:
        A, B = r.randint(1, 6), r.randint(1, 6)
        return Q(f'If y = {A} cos {a}x + {B} sin {a}x, show that d²y/dx² + {a * a}y = 0.', f'd²y/dx² = −{a * a}y', f'y′ = −{A * a} sin {a}x + {B * a} cos {a}x; y″ = −{a * a}({A} cos {a}x + {B} sin {a}x) = −{a * a}y.')
    if kind == 2:
        A, B = r.randint(1, 6), r.randint(1, 6)
        return Q(f'If y = {A} cos(log x) + {B} sin(log x), show that x²y₂ + xy₁ + y = 0.', 'x²y₂ + xy₁ + y = 0', f'xy₁ = −{A} sin(log x) + {B} cos(log x); differentiate again: xy₂ + y₁ = −y/x.')
    return Q(f'If y = e^({a} cos⁻¹x), −1 < x < 1, show that (1 − x²)d²y/dx² − x dy/dx − {a * a}y = 0.', f'(1 − x²)y₂ − xy₁ − {a * a}y = 0',
             f'y₁ = −{a}y/√(1 − x²) ⇒ (1 − x²)y₁² = {a * a}y² (2 marks); differentiate and cancel 2y₁ (3 marks).')


def c5s5_d2(r):
    kind = r.randint(0, 3)
    a = r.choice([2, 3, 4, 5])
    if kind == 0:
        c = [r.randint(-4, 4) for _ in range(4)]
        c[0] = c[0] or 1
        terms = [(c[0], 3), (c[1], 2), (c[2], 1), (c[3], 0)]
        x0 = r.randint(-2, 2)
        v = 6 * c[0] * x0 + 2 * c[1]
        return Q(f'Find d²y/dx² at x = {x0} for y = {polyF(terms)}.', fz(v), f'y″ = {polyF([(6 * c[0], 1), (2 * c[1], 0)])}; at x = {x0}: {v}.', num_distractors(v, 3 * c[0] * x0 * x0 + 2 * c[1] * x0 + c[2], -v, v + 2))
    if kind == 1:
        return Q(f'Find d²y/dx² if y = {ex(a)}.', f'{a * a}{ex(a)}', f'y′ = {a}{ex(a)}, y″ = {a * a}{ex(a)}.', [f'{a}{ex(a)}', f'{2 * a}{ex(a)}', f'{ex(a)}'])
    if kind == 2:
        return Q(f'Find d²y/dx² if y = log({a}x), x > 0.', '−1/x²', 'y′ = 1/x, y″ = −1/x².', ['1/x²', f'−{a}/x²', f'{a}/x'])
    return Q(f'Find d²y/dx² if y = x sin {a}x.'.replace('sin 1x', 'sin x'), f'{2 * a} cos {a}x − {a * a}x sin {a}x', f'y′ = sin {a}x + {a}x cos {a}x; y″ = {a} cos {a}x + {a} cos {a}x − {a * a}x sin {a}x.',
             [f'{a} cos {a}x − {a * a}x sin {a}x', f'{2 * a} cos {a}x + {a * a}x sin {a}x', f'−{a * a}x sin {a}x'],
             _d=(lambda x: math.sin(a * x) + a * x * math.cos(a * x), lambda x: 2 * a * math.cos(a * x) - a * a * x * math.sin(a * x), 0.4))


def c5s5_mcq(r):
    return mcqbank([
        ('If x = at², y = 2at, then dy/dx = …', '1/t', ['t', '2t', '1/(2t)'], 'dy/dx = (dy/dt)/(dx/dt) = 2a/(2at).'),
        ('If x = a cos θ, y = a sin θ, then dy/dx = …', '−cot θ', ['cot θ', 'tan θ', '−tan θ'], 'a cos θ/(−a sin θ).'),
        ('If y = sin x, then d²y/dx² = …', '−y', ['y', 'cos x', '−cos x'], 'y″ = −sin x.'),
        ('If y = e^(2x), then d²y/dx² − 4y = …', '0', ['2y', '4y', 'e^(2x)'], 'y″ = 4e^(2x).'),
        ('If y = A sin x + B cos x, then …', 'd²y/dx² + y = 0', ['d²y/dx² − y = 0', 'dy/dx + y = 0', 'd²y/dx² = y'], 'y″ = −y.'),
    ])(r)


def c5s5_ar(r):
    a = r.randint(2, 6)
    return arbank([
        (f'If y = sin {a}x, then d²y/dx² = −{a * a}y.', 'd/dx (cos kx) = −k sin kx.', 'a', 'Differentiating twice gives −k²y.'),
        (f'If x = {a}t², y = {2 * a}t, then dy/dx = t.', 'For parametric forms, dy/dx = (dy/dt)/(dx/dt).', 'd', 'dy/dx = 1/t; A false, R true.'),
        ('If y = eˣ, then d²y/dx² = y.', 'Every derivative of eˣ is eˣ.', 'a', 'R explains A.'),
        ('If x = cos t, y = sin t, then dy/dx = −cot t.', 'x² + y² = 1 for all t.', 'b', 'Both true; A follows from dy/dt ÷ dx/dt (or from R by implicit differentiation, but R alone is not the derivative computation).'),
    ])(r)


def c5s5_case(r):
    u = r.choice([20, 30, 40, 50])
    g = 10
    who = name(r)
    return Q((f'{who} throws a ball from a rooftop; its position after t seconds is x = {u // 2}t, y = {u}t − 5t² (metres). (i) Find dx/dt and dy/dt. (ii) Find dy/dx in terms of t. '
              f'(iii) Find the time at which the ball is at its highest point and the value of d²y/dt² there.'),
             f'(i) {u // 2}, {u} − 10t (ii) ({u} − 10t)/{u // 2} (iii) t = {u // 10} s; d²y/dt² = −10',
             '(i) 1 mark (ii) 1 mark (iii) dy/dt = 0 (1 mark), second derivative (1 mark).')


# ======================================================================= ch06 Application of Derivatives

def c6s1_circle(r):
    kind = r.randint(0, 3)
    if kind == 0:
        rr, dr = r.randint(3, 20), r.choice([Fr(1, 2), 1, 2, 3, Fr(3, 2), 4])
        v = 2 * rr * Fr(dr)
        return Q(f'The radius of a circular ripple increases at {fz(dr)} cm/s. Find the rate of increase of its area when the radius is {rr} cm.', f'{fz(v)}π cm²/s',
                 f'A = πr² ⇒ dA/dt = 2πr dr/dt = 2π({rr})({fz(dr)}) = {fz(v)}π cm²/s.', [f'{fz(v / 2)}π cm²/s', f'{fz(rr * rr * Fr(dr))}π cm²/s', f'{fz(v * 2)}π cm²/s'])
    if kind == 1:
        rr, dV = r.randint(3, 15), r.choice([100, 200, 300, 400, 900, 50])
        v = Fr(dV, 4 * rr * rr)
        return Q(f'Air is pumped into a spherical balloon at {dV} cm³/s. Find the rate at which its radius increases when the radius is {rr} cm.', f'{opi(v)} cm/s',
                 f'V = (4/3)πr³ ⇒ dV/dt = 4πr² dr/dt ⇒ dr/dt = {dV}/(4π × {rr * rr}) = {opi(v)} cm/s.', [f'{opi(v * 3)} cm/s', f'{opi(v * rr)} cm/s', f'{fz(v)}π cm/s'])
    if kind == 2:
        x, dx = r.randint(2, 15), r.choice([1, 2, 3, 4, 5])
        v = 3 * x * x * dx
        return Q(f'The edge of a cube increases at {dx} cm/s. How fast is its volume increasing when the edge is {x} cm long?', f'{v} cm³/s', f'V = x³ ⇒ dV/dt = 3x² dx/dt = 3({x})²({dx}) = {v} cm³/s.',
                 num_distractors(v, x ** 3 * dx, 12 * x * dx, 3 * x * dx))
    x, dx = r.randint(2, 15), r.choice([1, 2, 3, 4, 5])
    v = 12 * x * dx
    return Q(f'The edge of a cube increases at {dx} cm/s. How fast is its surface area increasing when the edge is {x} cm?', f'{v} cm²/s', f'S = 6x² ⇒ dS/dt = 12x dx/dt = {v} cm²/s.',
             num_distractors(v, 6 * x * dx, 3 * x * x * dx, 6 * x * x * dx))


def c6s1_ladder(r):
    a, b, c = r.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17), (12, 16, 20)])
    if r.random() < 0.5:
        a, b = b, a
    dx = r.choice([1, 2, 3, Fr(1, 2)])
    dy = -Fr(a, b) * dx
    who = name(r)
    return Q(f'A ladder {c} m long leans against a wall. Its foot is pulled along the ground away from the wall at {fz(dx)} m/s. How fast is its top sliding down the wall when the foot is {a} m from the wall?',
             f'{fz(-dy)} m/s', f'x² + y² = {c * c} ⇒ 2x dx/dt + 2y dy/dt = 0 (1 mark); at x = {a}, y = {b}: dy/dt = −({a}/{b})({fz(dx)}) = {fz(dy)} m/s, i.e. the top slides down at {fz(-dy)} m/s (2 marks).',
             [f'{fz(Fr(b, a) * dx)} m/s', f'{fz(dx)} m/s', f'{fz(-dy * 2)} m/s'])


def c6s1_marginal(r):
    a, b, c, d = r.choice([Fr(1, 100), Fr(3, 1000), Fr(1, 200)]), r.choice([Fr(1, 5), Fr(1, 10), 0]), r.randint(2, 30), r.randint(500, 8000)
    x0 = r.choice([10, 15, 20, 25, 30, 50])
    kind = r.randint(0, 1)
    if kind == 0:
        terms = [(a * 3 if a == Fr(1, 100) else a, 3), (-b, 2), (c, 1), (d, 0)]
        mc = sum(Fr(n) * cc * x0 ** (n - 1) for cc, n in terms if n > 0)
        return Q(f'The total cost (in ₹) of producing x units of an item is C(x) = {polyF(terms).replace("3x³/100", "0.03x³").replace("x³/100", "0.01x³").replace("3x³/1000", "0.003x³").replace("x³/200", "0.005x³").replace("x²/5", "0.2x²").replace("x²/10", "0.1x²")}. Find the marginal cost when {x0} units are produced.',
                 f'₹{fz(mc)}', f'MC = dC/dx = {polyF([(Fr(n) * cc, n - 1) for cc, n in terms if n > 0])}; at x = {x0}: ₹{fz(mc)}.', [f'₹{fz(peval(terms, x0))}', f'₹{fz(mc * 2)}', f'₹{fz(mc - c)}'])
    p, q = r.randint(2, 9), r.randint(10, 60)
    mr = 2 * p * x0 + q
    return Q(f'The total revenue (in ₹) from selling x units of a product is R(x) = {p}x² + {q}x + {r.randint(5, 50)}. Find the marginal revenue when x = {x0}.', f'₹{mr}',
             f'MR = dR/dx = {2 * p}x + {q}; at x = {x0}: ₹{mr}.', num_distractors(mr, p * x0 * x0 + q * x0, 2 * p * x0, mr + q))


def c6s1_mcq(r):
    return mcqbank([
        ('The rate of change of the area of a circle with respect to its radius r, when r = 6 cm, is …', '12π cm²/cm', ['36π cm²/cm', '6π cm²/cm', '24π cm²/cm'], 'dA/dr = 2πr.'),
        ('If y = f(x), then dy/dx at x = x₀ represents …', 'the rate of change of y with respect to x at x₀', ['the average value of y', 'the area under the curve', 'the value of y at x₀'], 'Meaning of the derivative.'),
        ('The marginal cost is the …', 'rate of change of total cost with respect to output', ['average cost per unit', 'total cost of production', 'fixed cost'], 'MC = dC/dx.'),
        ('If the radius of a sphere increases at a constant rate, its volume increases at a rate that is …', 'proportional to the square of the radius', ['constant', 'proportional to the radius', 'proportional to the cube of the radius'], 'dV/dt = 4πr² dr/dt.'),
        ('A balloon which always remains spherical has a variable radius. The rate of change of its volume with respect to its radius when r = 10 cm is …', '400π cm³/cm', ['100π cm³/cm', '4000π/3 cm³/cm', '40π cm³/cm'], 'dV/dr = 4πr².'),
    ])(r)


def c6s1_ar(r):
    rr = r.randint(2, 12)
    return arbank([
        (f'The rate of change of the area of a circle with respect to its radius at r = {rr} cm is {2 * rr}π cm²/cm.', 'dA/dr = 2πr.', 'a', 'Substitute r.'),
        (f'The rate of change of the volume of a cube with respect to its edge x at x = {rr} cm is {rr ** 3} cm³/cm.', 'dV/dx = 3x².', 'd', f'It is 3({rr})² = {3 * rr * rr}; A false, R true.'),
        ('If dy/dt > 0, then y increases as t increases.', 'A positive derivative means the function is increasing.', 'a', 'Sign of the rate.'),
    ])(r)


def c6s1_case(r):
    k = r.choice([2, 3, 4])
    h, dV = r.choice([4, 6, 8, 9, 12]), r.choice([6, 9, 12, 15, 24])
    v = Fr(dV * k * k, h * h)
    return Q((f'Sand is being poured from a pipe at {dV} cm³/s and forms a cone on the ground whose radius is always {k} times its height (r = {k}h). '
              f'(i) Express the volume V of the cone in terms of h. (ii) Find dV/dh. (iii) How fast is the height increasing when the height is {h} cm?'),
             f'(i) V = {fz(Fr(k * k, 3))}πh³ (ii) {k * k}πh² (iii) {opi(Fr(dV, k * k * h * h))} cm/s',
             '(i) V = (1/3)πr²h with r = kh (1 mark) (ii) 1 mark (iii) dh/dt = (dV/dt)/(dV/dh) (2 marks).')


def c6s1_long(r):
    a, b = r.randint(4, 12), r.randint(4, 12)
    da, db = r.choice([-5, -3, -2, 2, 3, 4]), r.choice([2, 3, 4, 5, -2])
    dP = 2 * (da + db)
    dA = a * db + b * da
    return Q(f'The length x of a rectangle is changing at {da} cm/min and the width y at {db} cm/min. When x = {a} cm and y = {b} cm, find the rates of change of (a) the perimeter and (b) the area of the rectangle, stating whether each is increasing or decreasing.',
             f'(a) {dP} cm/min ({"increasing" if dP > 0 else "decreasing" if dP < 0 else "constant"}) (b) {dA} cm²/min ({"increasing" if dA > 0 else "decreasing" if dA < 0 else "constant"})',
             f'P = 2(x + y) ⇒ dP/dt = 2({da} + {db}) = {dP} (2 marks); A = xy ⇒ dA/dt = x dy/dt + y dx/dt = {a}({db}) + {b}({da}) = {dA} (3 marks).')


# ---- st2 increasing and decreasing functions

def _cubic(r, sign=None):
    a, b = sorted(r.sample(range(-4, 6), 2))
    s = sign or r.choice([1, -1])
    c = r.randint(-9, 9)
    terms = [(2 * s, 3), (-3 * s * (a + b), 2), (6 * s * a * b, 1), (c, 0)]
    return a, b, s, terms


def c6s2_cubic(r):
    a, b, s, terms = _cubic(r)
    inc = f'(−∞, {a}) ∪ ({b}, ∞)' if s > 0 else f'({a}, {b})'
    dec = f'({a}, {b})' if s > 0 else f'(−∞, {a}) ∪ ({b}, ∞)'
    return Q(f'Find the intervals in which the function f(x) = {polyF(terms)} is (a) strictly increasing (b) strictly decreasing.', f'(a) {inc} (b) {dec}',
             f"f′(x) = {6 * s}(x − {a})(x − {b})".replace('− −', '+ ').replace('(x − 0)', 'x') + f' (1 mark); critical points x = {a}, {b} (1 mark); sign of f′ on each interval (1 mark).',
             [f'(a) {dec} (b) {inc}', f'(a) ({a}, ∞) (b) (−∞, {a})', f'(a) (−∞, {b}) (b) ({b}, ∞)'])


def c6s2_quad(r):
    a = r.choice([1, 2, 3, -1, -2])
    b = r.randint(-12, 12)
    c = r.randint(-9, 9)
    v = Fr(-b, 2 * a)
    inc, dec = (f'({fz(v)}, ∞)', f'(−∞, {fz(v)})') if a > 0 else (f'(−∞, {fz(v)})', f'({fz(v)}, ∞)')
    return Q(f'Find the intervals in which f(x) = {poly([a, b, c])} is strictly increasing or strictly decreasing.', f'increasing on {inc}, decreasing on {dec}',
             f'f′(x) = {poly([2 * a, b])} = 0 at x = {fz(v)}; f′ > 0 on {inc}.', [f'increasing on {dec}, decreasing on {inc}', f'increasing on ({fz(-v)}, ∞), decreasing on (−∞, {fz(-v)})' if v else 'increasing on (1, ∞), decreasing on (−∞, 1)', 'increasing on R'])


def c6s2_least(r):
    p, q = sorted(r.sample(range(-3, 6), 2))
    c = r.randint(-5, 5)
    kind = r.randint(0, 1)
    if kind == 0:
        return Q(f'Find the least value of a such that f(x) = x² + ax + {c} is strictly increasing on ({p}, {q}).'.replace('+ -', '− '), f'a = {-2 * p}',
                 f'f′(x) = 2x + a > 0 on ({p}, {q}) ⇔ 2({p}) + a ≥ 0 ⇔ a ≥ {-2 * p}.', num_distractors(-2 * p, -2 * q, 2 * p, -p))
    return Q(f'Show that f(x) = {r.choice([2, 3, 5, 7])}x {r.choice(["+", "−"])} {r.randint(1, 20)} is strictly increasing on R.', 'f′(x) > 0 for all x',
             'f′(x) is a positive constant, so f is strictly increasing on R.', ['f′(x) < 0 for all x', 'f is constant', 'f is increasing only for x > 0'])


def c6s2_mcq(r):
    return mcqbank([
        ('The function f(x) = eˣ is …', 'strictly increasing on R', ['strictly decreasing on R', 'neither increasing nor decreasing', 'increasing only for x > 0'], 'f′(x) = eˣ > 0.'),
        ('The function f(x) = log x is strictly increasing on …', '(0, ∞)', ['R', '(−∞, 0)', '(1, ∞) only'], 'f′(x) = 1/x > 0 for x > 0.'),
        ('The function f(x) = cos x is strictly decreasing on …', '(0, π)', ['(π, 2π)', '(−π/2, π/2)', '(0, 2π)'], 'f′(x) = −sin x < 0 on (0, π).'),
        ('The function f(x) = sin x is strictly increasing on …', '(0, π/2)', ['(π/2, π)', '(0, π)', '(π, 3π/2)'], 'cos x > 0 on (0, π/2).'),
        ('The function f(x) = x³ is …', 'strictly increasing on R', ['strictly decreasing on R', 'decreasing on (−∞, 0)', 'constant near 0'], 'f′(x) = 3x² ≥ 0, zero only at 0.'),
        ('f(x) = 7x − 3 is …', 'strictly increasing on R', ['strictly decreasing on R', 'constant', 'decreasing for x < 3/7'], 'f′(x) = 7 > 0.'),
        ('f(x) = 1/x is strictly decreasing on …', '(0, ∞) and on (−∞, 0) separately', ['R', '(0, ∞) only increasing', 'no interval'], 'f′(x) = −1/x² < 0.'),
    ])(r)


def c6s2_ar(r):
    a, b, s, terms = _cubic(r, 1)
    return arbank([
        (f'f(x) = {polyF(terms)} is strictly decreasing on ({a}, {b}).', f'f′(x) = 6(x − {a})(x − {b}) < 0 for {a} < x < {b}.'.replace('(x − 0)', 'x').replace('− −', '+ '), 'a', 'Negative derivative on the interval.'),
        (f'f(x) = {polyF(terms)} is strictly increasing on R.', f'f′(x) = 6(x − {a})(x − {b}).'.replace('(x − 0)', 'x').replace('− −', '+ '), 'd', f'f′ < 0 on ({a}, {b}); A false, R true.'),
        ('f(x) = x³ is strictly increasing on R.', 'f′(x) = 3x² > 0 for every real x.', 'c', 'A true; R false since f′(0) = 0.'),
        ('f(x) = eˣ is strictly increasing on R.', 'eˣ > 0 for every real x.', 'a', 'f′(x) = eˣ > 0.'),
    ])(r)


def c6s2_case(r):
    a, b = sorted(r.sample(range(2, 12), 2))
    s = -1
    c = r.randint(10, 90)
    terms = [(Fr(-1, 3), 3), (Fr(a + b, 2), 2), (-a * b, 1), (c, 0)]
    who = name(r)
    return Q((f'The monthly profit (in thousand ₹) of {who}\'s bakery, when x hundred cakes are made, is modelled by P(x) = {polyF(terms)} for 0 ≤ x ≤ {b + 3}. '
              f'(i) Find P′(x). (ii) Find the interval in which the profit is increasing. (iii) In which interval is the profit decreasing?'),
             f'(i) P′(x) = −(x − {a})(x − {b}) (ii) ({a}, {b}) (iii) [0, {a}) and ({b}, {b + 3}]',
             '(i) 1 mark (ii) 1 mark (iii) 2 marks.', _d=(lambda x: peval(terms, x), lambda x: -(x - a) * (x - b), a + 0.5))


def c6s2_explain(r):
    return xbank([
        ('Show that f(x) = x³ − 3x² + 3x − 100 is increasing on R.', "f′(x) = 3(x − 1)² ≥ 0, zero only at x = 1.", 'Derivative non-negative with an isolated zero (2 marks).'),
        ('Show that f(x) = log(sin x) is strictly increasing on (0, π/2) and strictly decreasing on (π/2, π).', 'f′(x) = cot x.', 'cot x > 0 on (0, π/2) and < 0 on (π/2, π) (2 marks).'),
        ('Explain why f(x) = x² is neither increasing nor decreasing on (−1, 1).', 'f′(x) = 2x changes sign at 0.', 'Decreasing on (−1, 0), increasing on (0, 1) (2 marks).'),
        ('Show that the function f(x) = 3x + 17 is strictly increasing on R.', "f′(x) = 3 > 0.", 'Positive derivative everywhere (2 marks).'),
    ])(r)


# ---- st3 local maxima and minima

def c6s3_cubic(r):
    a, b, s, terms = _cubic(r)
    fa, fb = peval(terms, a), peval(terms, b)
    mx, mn = (a, b) if s > 0 else (b, a)
    fmx, fmn = peval(terms, mx), peval(terms, mn)
    return Q(f'Find the points of local maxima and local minima, and the corresponding values, of f(x) = {polyF(terms)}.', f'local maximum at x = {mx} (value {num(fmx)}); local minimum at x = {mn} (value {num(fmn)})',
             f'f′(x) = {6 * s}(x − {a})(x − {b}) = 0 ⇒ x = {a}, {b} (1 mark); f″(x) = {polyF([(12 * s, 1), (-6 * s * (a + b), 0)])} (1 mark); f″({mx}) < 0 ⇒ max, f″({mn}) > 0 ⇒ min (1 mark).'.replace('− −', '+ ').replace('(x − 0)', 'x'),
             [f'local maximum at x = {mn} (value {num(fmn)}); local minimum at x = {mx} (value {num(fmx)})', f'local maximum at x = {mx} (value {num(fmn)}); local minimum at x = {mn} (value {num(fmx)})',
              f'local maximum at x = {-mx} (value {num(peval(terms, -mx))}); local minimum at x = {-mn} (value {num(peval(terms, -mn))})' if (mx or mn) else 'no local extremum'])


def c6s3_misc(r):
    kind = r.randint(0, 3)
    k = r.randint(2, 9)
    if kind == 0:
        return Q(f'Find the local minimum value of f(x) = x + {k * k}/x, x > 0.', str(2 * k), f'f′(x) = 1 − {k * k}/x² = 0 ⇒ x = {k}; f″({k}) = {fz(Fr(2 * k * k, k ** 3))} > 0; f({k}) = {2 * k}.',
                 num_distractors(2 * k, k, k * k, -2 * k))
    if kind == 1:
        return Q('Find the local maximum value of f(x) = sin x + cos x, 0 < x < π/2.', '√2', "f′(x) = cos x − sin x = 0 ⇒ x = π/4; f″(π/4) = −√2 < 0; f(π/4) = √2.", ['1', '2', '1/√2'])
    if kind == 2:
        return Q('Find the local minimum value of f(x) = x eˣ.', '−1/e', "f′(x) = eˣ(x + 1) = 0 ⇒ x = −1; f″(−1) = 1/e > 0; f(−1) = −1/e.", ['−e', '0', '1/e'])
    a = r.randint(1, 8)
    b = r.randint(-9, 9)
    return Q(f'Find the local minimum value of f(x) = (x − {a})² + {b}.'.replace('+ -', '− '), str(b), f'f′(x) = 2(x − {a}) = 0 ⇒ x = {a}; f″ = 2 > 0; f({a}) = {b}.', num_distractors(b, a, a + b, b - a))


def c6s3_mcq(r):
    return mcqbank([
        ('A point c in the domain of f at which f′(c) = 0 or f is not differentiable is called …', 'a critical point', ['a point of inflection only', 'a point of discontinuity', 'an end point'], 'Definition.'),
        ('If f′(c) = 0 and f″(c) > 0, then x = c is a point of …', 'local minimum', ['local maximum', 'inflection', 'discontinuity'], 'Second derivative test.'),
        ('If f′(c) = 0 and f″(c) < 0, then x = c is a point of …', 'local maximum', ['local minimum', 'inflection', 'discontinuity'], 'Second derivative test.'),
        ('If f′(c) = 0 and f″(c) = 0, the second derivative test …', 'fails', ['shows a maximum', 'shows a minimum', 'shows c is not critical'], 'Use the first derivative test.'),
        ('If f′ changes sign from positive to negative as x increases through c, then c is a point of …', 'local maximum', ['local minimum', 'inflection', 'neither'], 'First derivative test.'),
        ('The function f(x) = x³ at x = 0 has …', 'a point of inflection', ['a local maximum', 'a local minimum', 'a discontinuity'], 'f′ does not change sign.'),
    ])(r)


def c6s3_ar(r):
    k = r.randint(2, 9)
    return arbank([
        (f'f(x) = x + {k * k}/x (x > 0) has a local minimum at x = {k}.', f'f′({k}) = 0 and f″({k}) > 0.', 'a', 'Second derivative test.'),
        ('f(x) = x³ has a local extremum at x = 0.', "f′(0) = 0.", 'd', 'f′ does not change sign at 0: inflection, so A is false; R is true.'),
        ('Every local maximum value of a function is greater than every local minimum value.', 'A local maximum is the largest value only in a neighbourhood.', 'd', 'Local values are compared only nearby; A false, R true.'),
        (f'f(x) = |x − {k}| has a local minimum at x = {k}.', f'f(x) ≥ 0 = f({k}) for all x.', 'a', 'The minimum is attained at the corner even though f′ does not exist there.'),
    ])(r)


def c6s3_case(r):
    a, b, s, terms = _cubic(r, -1)
    if a < 0:
        a, b = a + 5, b + 5
        terms = [(-2, 3), (3 * (a + b), 2), (-6 * a * b, 1), (r.randint(50, 200), 0)]
    who = name(r)
    lo, hi = min(a, b), max(a, b)
    return Q((f'The temperature (in a suitable unit) inside {who}\'s greenhouse t hours after 6 a.m. is modelled by T(t) = {polyF(terms, "t")}. '
              f'(i) Find T′(t). (ii) Find the critical points. (iii) Using the second derivative test, decide at which critical point the temperature has a local maximum, and find that value.'),
             f'(i) T′(t) = −6(t − {lo})(t − {hi}) (ii) t = {lo}, {hi} (iii) local maximum at t = {hi}, T = {num(peval(terms, hi))}',
             '(i) 1 mark (ii) 1 mark (iii) 2 marks.')


def c6s3_long(r):
    a, b, s, terms = _cubic(r)
    mx, mn = (a, b) if s > 0 else (b, a)
    return Q(f'Find all points of local maxima and local minima of f(x) = {polyF(terms)} using the first derivative test, and verify using the second derivative test. Also find the local maximum and local minimum values.',
             f'local max at x = {mx}, value {num(peval(terms, mx))}; local min at x = {mn}, value {num(peval(terms, mn))}',
             f'f′(x) = {6 * s}(x − {a})(x − {b}) (1 mark); sign changes of f′ (2 marks); f″ at both points (1 mark); values (1 mark).'.replace('− −', '+ ').replace('(x − 0)', 'x'))


# ---- st4 absolute extrema and optimisation

def c6s4_abs(r):
    a, b, s, terms = _cubic(r)
    p = r.randint(min(a, b) - 2, min(a, b))
    q = r.randint(max(a, b), max(a, b) + 2)
    cands = {x: peval(terms, x) for x in {p, q, a, b} if p <= x <= q}
    xmax = max(cands, key=cands.get)
    xmin = min(cands, key=cands.get)
    return Q(f'Find the absolute maximum and absolute minimum values of f(x) = {polyF(terms)} on the interval [{p}, {q}].', f'absolute maximum {num(cands[xmax])} at x = {xmax}; absolute minimum {num(cands[xmin])} at x = {xmin}',
             f'Critical points x = {a}, {b} (1 mark); f at {", ".join(f"x = {x}: {num(v)}" for x, v in sorted(cands.items()))} (1 mark); compare (1 mark).',
             [f'absolute maximum {num(cands[xmin])} at x = {xmin}; absolute minimum {num(cands[xmax])} at x = {xmax}', f'absolute maximum {num(peval(terms, a))} at x = {a}; absolute minimum {num(peval(terms, b))} at x = {b}',
              f'absolute maximum {num(peval(terms, q))} at x = {q}; absolute minimum {num(peval(terms, p))} at x = {p}'])


BOXES = [(8, 3, Fr(2, 3)), (45, 24, Fr(5)), (16, 6, Fr(4, 3)), (15, 8, Fr(5, 3)), (24, 9, Fr(2)), (21, 16, Fr(3)), (40, 15, Fr(10, 3)), (30, 16, Fr(10, 3))]


def c6s4_box(r):
    kind = r.randint(0, 1)
    if kind == 0:
        s = 6 * r.randint(2, 10)
        x = s // 6
        V = x * (s - 2 * x) ** 2
        return Q(f'A square tin sheet of side {s} cm is to be made into an open box by cutting equal squares from the corners and folding up the flaps. What should be the side of the square cut off so that the volume of the box is maximum? Find the maximum volume.',
                 f'{x} cm; {V} cm³', f'V = x({s} − 2x)² (1 mark); V′ = ({s} − 2x)({s} − 6x) = 0 ⇒ x = {x} (2 marks); V″ < 0 there (1 mark); V = {V} cm³ (1 mark).')
    a, b, x = r.choice(BOXES)
    V = x * (a - 2 * x) * (b - 2 * x)
    return Q(f'A rectangular sheet of tin {a} cm × {b} cm is made into an open box by cutting equal squares from the corners and folding up the flaps. Find the side of the square to be cut so that the volume is maximum, and the maximum volume.',
             f'{fz(x)} cm; {fz(V)} cm³', f'V = x({a} − 2x)({b} − 2x) (1 mark); V′ = 12x² − {4 * (a + b)}x + {a * b} = 0 ⇒ x = {fz(x)} (the other root makes {b} − 2x < 0) (2 marks); V″ < 0 (1 mark); V = {fz(V)} cm³ (1 mark).')


def c6s4_numbers(r):
    S = r.choice([6, 9, 12, 15, 18, 21, 24, 30, 36, 45, 60])
    kind = r.randint(0, 2)
    if kind == 0:
        return Q(f'Find two positive numbers whose sum is {S} and whose product is maximum.', f'{fz(Fr(S, 2))} and {fz(Fr(S, 2))}', f'P = x({S} − x); P′ = {S} − 2x = 0 ⇒ x = {fz(Fr(S, 2))}; P″ = −2 < 0.',
                 [f'{S - 1} and 1', f'{S // 3} and {S - S // 3}', f'{S} and 0'])
    if kind == 1:
        return Q(f'Find two positive numbers x and y such that x + y = {S} and xy² is maximum.', f'x = {S // 3}, y = {2 * S // 3}', f'f(y) = ({S} − y)y²; f′ = {2 * S}y − 3y² = 0 ⇒ y = {2 * S // 3}; f″ < 0 there.',
                 [f'x = {2 * S // 3}, y = {S // 3}', f'x = {fz(Fr(S, 2))}, y = {fz(Fr(S, 2))}', f'x = {S // 4 if S % 4 == 0 else S // 3 + 1}, y = {S - (S // 4 if S % 4 == 0 else S // 3 + 1)}'])
    P = (S // 3) ** 2
    return Q(f'Find two positive numbers whose product is {P} and whose sum is minimum.', f'{S // 3} and {S // 3}', f'Sum s = x + {P}/x; s′ = 1 − {P}/x² = 0 ⇒ x = {S // 3}; s″ > 0.',
             [f'1 and {P}', f'{S // 3 * 2} and {fz(Fr(P, S // 3 * 2))}', f'{P} and 1'])


def c6s4_fence(r):
    kind = r.randint(0, 2)
    if kind == 0:
        L = r.choice([40, 60, 80, 100, 120, 200])
        return Q(f'{name(r)} has {L} m of fencing to enclose a rectangular kitchen garden. Find the dimensions giving the maximum area.', f'{fz(Fr(L, 4))} m × {fz(Fr(L, 4))} m (a square)',
                 f'A = x({fz(Fr(L, 2))} − x); A′ = 0 ⇒ x = {fz(Fr(L, 4))}; A″ < 0.', [f'{fz(Fr(L, 2))} m × {fz(Fr(L, 2))} m', f'{fz(Fr(L, 3))} m × {fz(Fr(L, 6))} m', f'{fz(Fr(L, 8))} m × {fz(Fr(3 * L, 8))} m'])
    if kind == 1:
        L = r.choice([40, 60, 80, 100, 120, 200])
        return Q(f'A farmer has {L} m of fencing to enclose a rectangular field along a straight river; no fence is needed along the river. Find the dimensions for maximum area.',
                 f'{fz(Fr(L, 4))} m (perpendicular to river) × {fz(Fr(L, 2))} m (parallel), area {fz(Fr(L * L, 8))} m²',
                 f'A = x({L} − 2x); A′ = {L} − 4x = 0 ⇒ x = {fz(Fr(L, 4))}; A″ = −4 < 0.', [f'{fz(Fr(L, 3))} m × {fz(Fr(L, 3))} m', f'{fz(Fr(L, 2))} m × {fz(Fr(L, 4))} m (perpendicular first)', f'{fz(Fr(L, 4))} m × {fz(Fr(L, 4))} m'])
    a = r.choice([4, 9, 16, 25, 36, 49, 64, 100, 144])
    s = math.isqrt(a)
    return Q(f'Of all rectangles with area {a} m², find the one with the least perimeter.', f'a square of side {s} m (perimeter {4 * s} m)', f'P = 2(x + {a}/x); P′ = 0 ⇒ x = {s}; P″ > 0.',
             [f'{a} m × 1 m', f'{2 * s} m × {fz(Fr(s, 2))} m', f'a square of side {fz(Fr(a, 4))} m'])


def c6s4_profit(r):
    a = r.choice([1, 2, 3, 4, 5])
    xm = r.choice([10, 20, 25, 30, 40, 50])
    b = 2 * a * xm
    c = 10 * r.randint(5, max(6, a * xm * xm // 20))
    P = -a * xm * xm + b * xm - c
    return Q(f'A company\'s profit (in ₹ thousand) from selling x units is P(x) = −{a}x² + {b}x − {c}.'.replace('−1x²', '−x²') + ' How many units should it sell to maximise profit, and what is the maximum profit?',
             f'{xm} units; ₹{P} thousand', f'P′(x) = −{2 * a}x + {b} = 0 ⇒ x = {xm}; P″ = −{2 * a} < 0; P({xm}) = {P}.', [f'{xm * 2} units; ₹{-a * 4 * xm * xm + b * 2 * xm - c} thousand', f'{xm // 2} units; ₹{-a * (xm // 2) ** 2 + b * (xm // 2) - c} thousand', f'{xm} units; ₹{P + c} thousand'])


def c6s4_proof(r):
    return xbank([
        ('Show that of all the rectangles inscribed in a given fixed circle, the square has the maximum area.', 'A = 4r² sin θ cos θ = 2r² sin 2θ is maximum at θ = π/4: a square.',
         'Set up area with the diagonal as diameter (2 marks); differentiate and solve (2 marks); second derivative/conclusion (1 mark).'),
        ('Show that the right circular cylinder of given surface area and maximum volume is such that its height is equal to the diameter of the base.', 'h = 2r.',
         'S = 2πr² + 2πrh fixed ⇒ V = (Sr − 2πr³)/2 (2 marks); V′ = 0 ⇒ S = 6πr² ⇒ h = 2r (2 marks); V″ < 0 (1 mark).'),
        ('Show that the height of the cylinder of maximum volume that can be inscribed in a sphere of radius R is 2R/√3. Also find the maximum volume.', 'h = 2R/√3; V = 4πR³/(3√3).',
         'V = πh(R² − h²/4) (2 marks); V′ = 0 ⇒ h = 2R/√3 (2 marks); V″ < 0 and value (1 mark).'),
        ('Show that the semi-vertical angle of a right circular cone of given surface area and maximum volume is sin⁻¹(1/3).', 'sin α = 1/3.',
         'Express V² in terms of r with S fixed (2 marks); differentiate, get S = 4πr² so l = 3r (2 marks); sin α = r/l = 1/3 (1 mark).'),
        ('A window is in the form of a rectangle surmounted by a semicircular opening. The total perimeter of the window is 10 m. Find the dimensions of the window to admit maximum light through the whole opening.',
         'width 20/(π + 4) m, height of rectangle 10/(π + 4) m', 'Express area in terms of the radius r (2 marks); A′ = 0 ⇒ r = 10/(π + 4) (2 marks); A″ < 0 (1 mark).'),
        ('Show that the right circular cone of least curved surface area and given volume has an altitude equal to √2 times the radius of the base.', 'h = √2 r.',
         'Express S² in terms of r with V fixed (2 marks); differentiate to get h² = 2r² (2 marks); second derivative check (1 mark).'),
    ])(r)


def c6s4_mcq(r):
    return mcqbank([
        ('The maximum value of sin x cos x is …', '1/2', ['1', '√2', '2'], 'sin x cos x = (1/2) sin 2x.'),
        ('The absolute maximum of a continuous function on a closed interval [a, b] occurs …', 'at a critical point or at an end point', ['only at a critical point', 'only at an end point', 'only where f′ = 0'], 'Compare the values at critical points and ends.'),
        ('The minimum value of x² + 16/x² (x ≠ 0) is …', '8', ['4', '16', '0'], 'At x² = 4.'),
        ('The maximum value of f(x) = −x² + 6x − 5 is …', '4', ['5', '3', '9'], 'At x = 3.'),
        ('Of all rectangles with a fixed perimeter, the one with maximum area is …', 'a square', ['a rectangle with length twice the breadth', 'not unique', 'a very thin rectangle'], 'Standard result.'),
        ('The point on the curve x² = 2y nearest to (0, 5) is …', '(±2√2, 4)', ['(0, 0)', '(2, 2)', '(±√2, 1)'], 'Minimise x² + (y − 5)² = 2y + (y − 5)².'),
    ])(r)


def c6s4_ar(r):
    S = r.choice([10, 12, 16, 20, 24])
    return arbank([
        (f'The maximum value of x({S} − x) for real x is {S * S // 4}.', f'f′(x) = {S} − 2x vanishes at x = {S // 2} and f″ < 0.', 'a', 'Second derivative test.'),
        ('A continuous function on a closed interval attains an absolute maximum and minimum.', 'Absolute extrema occur only at critical points.', 'c', 'A true; R false (they can occur at end points).'),
        (f'The minimum value of x + {S * S // 4}/x for x > 0 is {S}.', f'At x = {S // 2}, f′(x) = 0 and f″(x) > 0.', 'a', f'f({S // 2}) = {S}.'),
        ('f(x) = x³ has no absolute maximum on R.', 'f is strictly increasing and unbounded above.', 'a', 'R explains A.'),
    ])(r)


def c6s4_case(r):
    a, b, x = r.choice(BOXES)
    V = x * (a - 2 * x) * (b - 2 * x)
    who = name(r)
    return Q((f'{who} runs a packaging unit in {r.choice(CITIES)} and makes open boxes from {a} cm × {b} cm cardboard sheets by cutting squares of side x cm from each corner. '
              f'(i) Write the volume V(x) and its domain. (ii) Find V′(x). (iii) Find x for maximum volume and the maximum volume.'),
             f'(i) V = x({a} − 2x)({b} − 2x), 0 < x < {fz(Fr(b, 2))} (ii) V′ = 12x² − {4 * (a + b)}x + {a * b} (iii) x = {fz(x)} cm, V = {fz(V)} cm³',
             '(i) 1 mark (ii) 1 mark (iii) 2 marks.')


# ======================================================================= ch07 Integrals

def c7s1_poly(r):
    k = r.randint(2, 3)
    pw = sorted(r.sample([-3, -2, 0, 1, 2, 3, 4, 5], k), reverse=True)
    cs = [r.choice([1, 2, 3, 4, 5, 6, -1, -2, -3]) for _ in pw]
    integ = ''
    for c, n in zip(cs, pw):
        if n >= 0:
            integ += mono(c, n, first=(integ == ''))
        else:
            t = f'{abs(c)}/x{supx(str(-n))}'.replace('1/', '1/') if abs(c) != 1 else f'1/x{supx(str(-n))}'
            integ += (('−' if c < 0 else '') + t) if integ == '' else ((' − ' if c < 0 else ' + ') + t)
    anti = ''
    for c, n in zip(cs, pw):
        cc = Fr(c, n + 1)
        if n >= 0:
            anti += mono(cc, n + 1, first=(anti == ''))
        else:
            m = -(n + 1)
            body = f'{abs(cc.numerator)}/({cc.denominator}x{supx(str(m)) if m > 1 else ""})' if cc.denominator != 1 else f'{abs(cc.numerator)}/x{supx(str(m)) if m > 1 else ""}'
            sgn = 1 if cc > 0 else -1
            anti += (('−' if sgn < 0 else '') + body) if anti == '' else ((' − ' if sgn < 0 else ' + ') + body)
    anti += ' + C'
    f = lambda x: sum(c * x ** n for c, n in zip(cs, pw))
    Fx = lambda x: sum(c / (n + 1) * x ** (n + 1) for c, n in zip(cs, pw))
    return Q(f'Find ∫ ({integ}) dx.', anti, 'Use ∫xⁿ dx = xⁿ⁺¹/(n + 1) + C, n ≠ −1, term by term.',
             dist3(anti, [integ + ' + C', anti.replace(' + C', ' + x + C'), ''.join(mono(c * (n if n else 1), n - 1 if n else 0, first=(i == 0)) for i, (c, n) in enumerate(zip(cs, pw)) if n > 0) + ' + C']), _i=(f, Fx, 1.3))


STD_I = [
    ('(2x − 3 cos x + eˣ)', 'x² − 3 sin x + eˣ + C', lambda x: 2 * x - 3 * math.cos(x) + math.exp(x), lambda x: x * x - 3 * math.sin(x) + math.exp(x)),
    ('(2x² + eˣ)', '2x³/3 + eˣ + C', lambda x: 2 * x * x + math.exp(x), lambda x: 2 * x ** 3 / 3 + math.exp(x)),
    ('(√x − 1/√x)', '(2/3)x^(3/2) − 2√x + C', lambda x: math.sqrt(x) - 1 / math.sqrt(x), lambda x: 2 / 3 * x ** 1.5 - 2 * math.sqrt(x)),
    ('sec x (sec x + tan x)', 'tan x + sec x + C', lambda x: (1 / math.cos(x)) * (1 / math.cos(x) + math.tan(x)), lambda x: math.tan(x) + 1 / math.cos(x)),
    ('(2 − 3 sin x)/cos²x', '2 tan x − 3 sec x + C', lambda x: (2 - 3 * math.sin(x)) / math.cos(x) ** 2, lambda x: 2 * math.tan(x) - 3 / math.cos(x)),
    ('(x³ − 1)/(x − 1), x ≠ 1', 'x³/3 + x²/2 + x + C', lambda x: (x ** 3 - 1) / (x - 1), lambda x: x ** 3 / 3 + x * x / 2 + x),
    ('(√x + 1/√x)²', 'x²/2 + 2x + log|x| + C', lambda x: (math.sqrt(x) + 1 / math.sqrt(x)) ** 2, lambda x: x * x / 2 + 2 * x + math.log(x)),
    ('(x³ + 5x² − 4)/x²', 'x²/2 + 5x + 4/x + C', lambda x: (x ** 3 + 5 * x * x - 4) / x ** 2, lambda x: x * x / 2 + 5 * x + 4 / x),
    ('sec²x/cosec²x', 'tan x − x + C', lambda x: math.tan(x) ** 2, lambda x: math.tan(x) - x),
    ('(1 − sin x)/cos²x', 'tan x − sec x + C', lambda x: (1 - math.sin(x)) / math.cos(x) ** 2, lambda x: math.tan(x) - 1 / math.cos(x)),
    ('(4eˣ + 3/x)', '4eˣ + 3 log|x| + C', lambda x: 4 * math.exp(x) + 3 / x, lambda x: 4 * math.exp(x) + 3 * math.log(x)),
    ('(ax² + bx + c)', 'ax³/3 + bx²/2 + cx + C', None, None),
    ('cosec x (cosec x − cot x)', '−cot x + cosec x + C', lambda x: (1 / math.sin(x)) * (1 / math.sin(x) - 1 / math.tan(x)), lambda x: -1 / math.tan(x) + 1 / math.sin(x)),
    ('(x⁴ + x² + 1)/x²', 'x³/3 + x − 1/x + C', lambda x: (x ** 4 + x * x + 1) / x ** 2, lambda x: x ** 3 / 3 + x - 1 / x),
]


def c7s1_std(r):
    i, a, f, Fx = r.choice(STD_I)
    others = [x[1] for x in STD_I if x[1] != a]
    r.shuffle(others)
    v = Q(f'Find ∫ {i} dx.', a, 'Simplify the integrand and integrate term by term using standard integrals.', others[:3])
    if f:
        v['_i'] = (f, Fx, 0.7)
    return v


def c7s1_ivp(r):
    a, b = r.randint(1, 6), r.randint(-6, 6)
    x0, y0 = r.randint(-2, 2), r.randint(-10, 10)
    # f'(x) = 3a x² + 2b x, f(x0) = y0  -> f = a x³ + b x² + C
    C = y0 - a * x0 ** 3 - b * x0 ** 2
    fx = polyF([(a, 3), (b, 2), (C, 0)])
    return Q(f'Find a function f such that f′(x) = {polyF([(3 * a, 2), (2 * b, 1)])} and f({x0}) = {y0}.', f'f(x) = {fx}',
             f'f(x) = ∫({polyF([(3 * a, 2), (2 * b, 1)])}) dx = {polyF([(a, 3), (b, 2)])} + C (1 mark); f({x0}) = {y0} ⇒ C = {C} (1 mark).',
             [f'f(x) = {polyF([(a, 3), (b, 2), (y0, 0)])}', f'f(x) = {polyF([(3 * a, 3), (2 * b, 2), (C, 0)])}', f'f(x) = {polyF([(a, 3), (b, 2), (-C, 0)])}'])


def c7s1_mcq(r):
    return mcqbank([
        ('∫ dx/x equals …', 'log|x| + C', ['1/x² + C', '−1/x² + C', 'x log x + C'], 'Standard integral.'),
        ('An antiderivative of cos x is …', 'sin x', ['−sin x', 'cos x', 'tan x'], 'd/dx sin x = cos x.'),
        ('∫ sec²x dx equals …', 'tan x + C', ['sec x + C', 'sec x tan x + C', '−cot x + C'], 'd/dx tan x = sec²x.'),
        ('∫ eˣ dx equals …', 'eˣ + C', ['x eˣ⁻¹ + C', 'eˣ⁺¹/(x + 1) + C', 'log x + C'], 'Standard.'),
        ('∫ 1/√(1 − x²) dx equals …', 'sin⁻¹x + C', ['cos⁻¹x + C', 'tan⁻¹x + C', 'log(1 − x²) + C'], 'Standard.'),
        ('∫ 1/(1 + x²) dx equals …', 'tan⁻¹x + C', ['log(1 + x²) + C', 'sin⁻¹x + C', 'cot⁻¹x + C'], 'Standard.'),
        ('If d/dx F(x) = f(x), then ∫ f(x) dx = …', 'F(x) + C', ['F′(x) + C', 'f′(x) + C', 'f(x) + C'], 'Definition of the indefinite integral.'),
    ])(r)


def c7s1_ar(r):
    n = r.randint(2, 7)
    return arbank([
        (f'∫ x{supx(str(n))} dx = x{supx(str(n + 1))}/{n + 1} + C.', 'd/dx (xⁿ⁺¹/(n + 1)) = xⁿ for n ≠ −1.', 'a', 'Integration reverses differentiation.'),
        ('∫ x⁻¹ dx = x⁰/0 + C.', '∫xⁿ dx = xⁿ⁺¹/(n + 1) + C holds only for n ≠ −1.', 'd', 'For n = −1 the integral is log|x| + C; A false, R true.'),
        ('Two antiderivatives of the same function differ by a constant.', 'The derivative of a constant is zero.', 'a', 'If F′ = G′ then (F − G)′ = 0.'),
        ('∫ (f(x) + g(x)) dx = ∫ f(x) dx + ∫ g(x) dx.', '∫ f(x)g(x) dx = ∫ f(x) dx · ∫ g(x) dx.', 'c', 'A true (linearity); R false.'),
    ])(r)


def c7s1_case(r):
    a, b = r.choice([2, 3, 4, 6]), r.randint(10, 60)
    c0 = r.choice([500, 1000, 1500, 2000])
    x0 = r.choice([10, 20, 30])
    C = Fr(a, 2) * x0 * x0 + b * x0 + c0
    who = name(r)
    return Q((f'{who}\'s workshop finds that the marginal cost of making x chairs is C′(x) = {a}x + {b} rupees, and the fixed cost is ₹{c0}. '
              f'(i) Find the total cost function C(x). (ii) Find the cost of making {x0} chairs. (iii) Find the extra cost of increasing output from {x0} to {x0 + 10} chairs.'),
             f'(i) C(x) = {polyF([(Fr(a, 2), 2), (b, 1), (c0, 0)])} (ii) ₹{fz(C)} (iii) ₹{fz(Fr(a, 2) * ((x0 + 10) ** 2 - x0 ** 2) + 10 * b)}',
             '(i) integrate and use C(0) (1 mark) (ii) 1 mark (iii) 2 marks.')


# ---- st2 substitution and trigonometric identities

def _subst(r):
    a = r.choice([2, 3, 4, 5])
    b = r.randint(1, 9)
    n = r.choice([2, 3, 4, 5])
    kind = r.randint(0, 13)
    if kind == 0:
        return (f'2x/(x² + {b})', f'log(x² + {b}) + C', lambda x: 2 * x / (x * x + b), lambda x: math.log(x * x + b))
    if kind == 1:
        return (f'x(x² + {b}){supx(str(n))}', f'(x² + {b}){supx(str(n + 1))}/{2 * (n + 1)} + C', lambda x: x * (x * x + b) ** n, lambda x: (x * x + b) ** (n + 1) / (2 * (n + 1)))
    if kind == 2:
        return (f'({lin(a, b)}){supx(str(n))}', f'({lin(a, b)}){supx(str(n + 1))}/{a * (n + 1)} + C', lambda x: (a * x + b) ** n, lambda x: (a * x + b) ** (n + 1) / (a * (n + 1)))
    if kind == 3:
        return (f'sin({lin(a, b)})', f'−cos({lin(a, b)})/{a} + C', lambda x: math.sin(a * x + b), lambda x: -math.cos(a * x + b) / a)
    if kind == 4:
        return (ex(a, b), f'{ex(a, b)}/{a} + C', lambda x: math.exp(a * x + b), lambda x: math.exp(a * x + b) / a)
    if kind == 5:
        return (f'(log x){supx(str(n))}/x', f'(log x){supx(str(n + 1))}/{n + 1} + C', lambda x: math.log(x) ** n / x, lambda x: math.log(x) ** (n + 1) / (n + 1))
    if kind == 6:
        return (f'sin²({a}x)', f'x/2 − sin({2 * a}x)/{4 * a} + C', lambda x: math.sin(a * x) ** 2, lambda x: x / 2 - math.sin(2 * a * x) / (4 * a))
    if kind == 7:
        return (f'cos²({a}x)', f'x/2 + sin({2 * a}x)/{4 * a} + C', lambda x: math.cos(a * x) ** 2, lambda x: x / 2 + math.sin(2 * a * x) / (4 * a))
    if kind == 8:
        return ('e^(tan⁻¹x)/(1 + x²)', 'e^(tan⁻¹x) + C', lambda x: math.exp(math.atan(x)) / (1 + x * x), lambda x: math.exp(math.atan(x)))
    if kind == 9:
        return ('cos³x', 'sin x − sin³x/3 + C', lambda x: math.cos(x) ** 3, lambda x: math.sin(x) - math.sin(x) ** 3 / 3)
    if kind == 10:
        return ('sin³x', '−cos x + cos³x/3 + C', lambda x: math.sin(x) ** 3, lambda x: -math.cos(x) + math.cos(x) ** 3 / 3)
    if kind == 11:
        p, q = r.sample(range(1, 7), 2)
        p, q = max(p, q), min(p, q)
        return (f'sin {p}x cos {q}x'.replace(' 1x', ' x'), f'−cos {p + q}x/{2 * (p + q)} − cos {p - q}x/{2 * (p - q)} + C'.replace(' 1x', ' x'),
                lambda x: math.sin(p * x) * math.cos(q * x), lambda x: -math.cos((p + q) * x) / (2 * (p + q)) - math.cos((p - q) * x) / (2 * (p - q)))
    if kind == 12:
        return ('1/(x log x)', 'log|log x| + C', lambda x: 1 / (x * math.log(x)), lambda x: math.log(abs(math.log(x))))
    return (f'sec²({lin(a, b)})', f'tan({lin(a, b)})/{a} + C', lambda x: 1 / math.cos(a * x + b) ** 2, lambda x: math.tan(a * x + b) / a)


def c7s2_sub(r):
    i, a, f, Fx = _subst(r)
    w = [a.replace('/', '×', 1) if '/' in a else '−' + a, a.replace(' + C', '') + ' × x + C', (('−' + a) if not a.startswith('−') else a[1:])]
    return Q(f'Find ∫ {i} dx.', a, 'Choose a substitution (or identity) that turns the integrand into a standard form, then integrate.', dist3(a, w), _i=(f, Fx, 1.7))


def c7s2_mcq(r):
    return mcqbank([
        ('∫ tan x dx equals …', 'log|sec x| + C', ['sec²x + C', 'log|cos x| + C', '−log|sec x| + C'], 'tan x = sin x/cos x; put t = cos x.'),
        ('∫ cot x dx equals …', 'log|sin x| + C', ['−log|sin x| + C', 'cosec²x + C', 'log|cos x| + C'], 'Put t = sin x.'),
        ('∫ sec x dx equals …', 'log|sec x + tan x| + C', ['sec x tan x + C', 'log|sec x| + C', 'tan x + C'], 'Standard result.'),
        ('∫ f′(x)/f(x) dx equals …', 'log|f(x)| + C', ['f(x)²/2 + C', 'f′(x) + C', '1/f(x) + C'], 'Put t = f(x).'),
        ('∫ sin 2x dx equals …', '−(1/2) cos 2x + C', ['(1/2) cos 2x + C', '−2 cos 2x + C', 'cos 2x + C'], 'Put t = 2x.'),
        ('∫ 2x eˣ² dx (i.e. 2x e^(x²)) equals …', 'e^(x²) + C', ['x²e^(x²) + C', '2e^(x²) + C', 'e^(2x) + C'], 'Put t = x².'),
    ])(r)


def c7s2_ar(r):
    b = r.randint(1, 9)
    return arbank([
        (f'∫ 2x/(x² + {b}) dx = log(x² + {b}) + C.', '∫ f′(x)/f(x) dx = log|f(x)| + C.', 'a', f'f(x) = x² + {b}.'),
        ('∫ sin²x dx = sin³x/3 + C.', 'sin²x = (1 − cos 2x)/2.', 'd', 'Using R, the integral is x/2 − sin 2x/4 + C; A false, R true.'),
        ('∫ tan x dx = log|sec x| + C.', 'd/dx (log|sec x|) = tan x.', 'a', 'Differentiation check.'),
        ('∫ e^(x²) · 2x dx = e^(x²) + C.', 'The substitution t = x² gives dt = 2x dx.', 'a', 'Integral becomes ∫ eᵗ dt.'),
    ])(r)


def c7s2_long(r):
    i1, a1, f1, F1 = _subst(r)
    i2, a2, f2, F2 = _subst(r)
    if i1 == i2:
        raise ValueError
    return Q(f'Evaluate: (i) ∫ {i1} dx (ii) ∫ {i2} dx.', f'(i) {a1} (ii) {a2}', '(i) substitution/identity and integration (3 marks) (ii) 2 marks.', _i=(f1, F1, 1.6))


def c7s2_case(r):
    i, a, f, Fx = _subst(r)
    who1, who2 = two_names(r)
    return Q((f'{who1} and {who2} are checking each other\'s homework on integration by substitution. The question is ∫ {i} dx. (i) Name a suitable substitution or identity. '
              f'(ii) Write the integral after the substitution. (iii) {who2}\'s answer is {a}. Verify it by differentiating.'),
             f'(i)–(ii) a substitution that reduces the integrand to a standard form (iii) d/dx [{a.replace(" + C", "")}] = {i}, so the answer {a} is correct',
             '(i) 1 mark (ii) 1 mark (iii) differentiation check (2 marks).', _i=(f, Fx, 1.4))


# ---- st3 partial fractions

def c7s3_two(r):
    a, b = r.sample(range(-5, 6), 2)
    p, q = r.randint(-4, 5), r.randint(-6, 6)
    if p == 0 and q == 0:
        q = 1
    A = Fr(p * a + q, a - b)
    B = Fr(p * b + q, b - a)
    if A == 0 or B == 0:
        raise ValueError
    num_ = f'({poly([p, q])})' if p else fz(q)
    den = '(' + ''.join(('x' if lin(1, -c) == 'x' else f'({lin(1, -c)})') for c in (a, b)) + ')'
    ans = f'{co(A)}log|{lin(1, -a)}|'.replace('(1)', '') + (' + ' if B > 0 else ' − ') + f'{co(abs(B))}log|{lin(1, -b)}|' + ' + C'
    ans = ans.replace('−log', '−log').replace('(−', '−(')
    if ans.startswith('−('):
        pass
    f = lambda x: (p * x + q) / ((x - a) * (x - b))
    Fx = lambda x: float(A) * math.log(abs(x - a)) + float(B) * math.log(abs(x - b))
    pa = f'{fpar(A)}/({lin(1, -a)})'
    pb = f'{fpar(abs(B))}/({lin(1, -b)})'
    return Q(f'Find ∫ {num_}/{den} dx.', ans,
             f'Partial fractions: {num_}/{den} = {pa} {"+" if B > 0 else "−"} {pb} (2 marks); integrate (1 mark).'.replace('/(x)', '/x'),
             dist3(ans, [f'{co(B)}log|{lin(1, -a)}| + {co(A)}log|{lin(1, -b)}| + C', f'{co(-A)}log|{lin(1, -a)}| + {co(-B)}log|{lin(1, -b)}| + C', f'log|({lin(1, -a)})({lin(1, -b)})| + C']), _i=(f, Fx, max(a, b) + 1.5))


def c7s3_one(r):
    a, b = r.sample(range(-6, 7), 2)
    k = Fr(1, a - b)
    ans = f'{co(k)}log|({lin(1, -a)})/({lin(1, -b)})| + C'
    return Q(f'Find ∫ dx/(({lin(1, -a)})({lin(1, -b)})).', ans, f'1/((x − a)(x − b)) = [1/(x − a) − 1/(x − b)]/(a − b) with a = {a}, b = {b}.',
             dist3(ans, [f'{co(-k)}log|({lin(1, -a)})/({lin(1, -b)})| + C', f'log|({lin(1, -a)})({lin(1, -b)})| + C', f'{co(k)}log|({lin(1, -b)})/({lin(1, -a)})| + C']),
             _i=(lambda x: 1 / ((x - a) * (x - b)), lambda x: float(k) * math.log(abs((x - a) / (x - b))), max(a, b) + 1.3))


def c7s3_three(r):
    a, b, c = r.sample(range(-4, 5), 3)
    kind = r.randint(0, 1)
    if kind == 0:
        A = Fr(a, (a - b) * (a - c))
        B = Fr(b, (b - a) * (b - c))
        Cc = Fr(c, (c - a) * (c - b))
        f = lambda x: x / ((x - a) * (x - b) * (x - c))
        Fx = lambda x: float(A) * math.log(abs(x - a)) + float(B) * math.log(abs(x - b)) + float(Cc) * math.log(abs(x - c))
        parts = [(A, a), (B, b), (Cc, c)]
        ans = ' '.join(f'{"+ " if i and k > 0 else "− " if i and k < 0 else "−" if k < 0 else ""}{co(abs(k))}log|{lin(1, -t)}|' for i, (k, t) in enumerate((k, t) for k, t in parts if k != 0)) + ' + C'
        return Q(f'Find ∫ x dx/(({lin(1, -a)})({lin(1, -b)})({lin(1, -c)})).', ans, f'x/((x − a)(x − b)(x − c)) = A/(x − a) + B/(x − b) + C/(x − c) with A = {fz(A)}, B = {fz(B)}, C = {fz(Cc)} (3 marks); integrate (2 marks).',
                 _i=(f, Fx, max(a, b, c) + 1.4))
    if a == b:
        raise ValueError
    Bq = Fr(a, a - b)
    Cq = Fr(b, (b - a) ** 2)
    Aq = -Cq
    f = lambda x: x / ((x - a) ** 2 * (x - b))
    Fx = lambda x: float(Aq) * math.log(abs(x - a)) - float(Bq) / (x - a) + float(Cq) * math.log(abs(x - b))
    ans = f'{co(Aq)}log|{lin(1, -a)}| {"−" if Bq > 0 else "+"} {fz(abs(Bq))}/({lin(1, -a)}) {"+" if Cq >= 0 else "−"} {co(abs(Cq))}log|{lin(1, -b)}| + C'
    return Q(f'Find ∫ x dx/(({lin(1, -a)})²({lin(1, -b)})).', ans, f'x/((x − a)²(x − b)) = A/(x − a) + B/(x − a)² + C/(x − b) with A = {fz(Aq)}, B = {fz(Bq)}, C = {fz(Cq)} (3 marks); integrate (2 marks).',
             _i=(f, Fx, max(a, b) + 1.4))


def c7s3_mcq(r):
    return mcqbank([
        ('The partial fraction form of (x + 1)/((x − 1)(x − 2)) is …', '−2/(x − 1) + 3/(x − 2)', ['2/(x − 1) − 3/(x − 2)', '1/(x − 1) + 1/(x − 2)', '3/(x − 1) − 2/(x − 2)'], 'x + 1 = A(x − 2) + B(x − 1): x = 1 ⇒ A = −2, x = 2 ⇒ B = 3.'),
        ('For partial fractions of a proper rational function with a repeated factor (x − a)², the terms needed are …', 'A/(x − a) + B/(x − a)²', ['A/(x − a)² only', 'A/(x − a)', '(Ax + B)/(x − a)'], 'Standard form.'),
        ('Before using partial fractions on P(x)/Q(x), we must ensure that …', 'the degree of P is less than the degree of Q', ['P and Q have the same degree', 'Q has no real roots', 'P is a constant'], 'Otherwise divide first.'),
        ('∫ dx/(x(x + 1)) equals …', 'log|x/(x + 1)| + C', ['log|x(x + 1)| + C', 'log|(x + 1)/x| + C', '1/(x(x + 1)) + C'], '1/x − 1/(x + 1).'),
        ('For (px + q)/((x − a)(x² + bx + c)) with an irreducible quadratic, the partial fraction form is …', 'A/(x − a) + (Bx + C)/(x² + bx + c)', ['A/(x − a) + B/(x² + bx + c)', 'A/(x − a) + B/(x − a)²', '(Ax + B)/(x − a)'], 'Linear numerator over the quadratic.'),
    ])(r)


def c7s3_ar(r):
    a, b = r.sample(range(1, 7), 2)
    return arbank([
        (f'∫ dx/((x − {a})(x − {b})) = {fz(Fr(1, a - b))} log|(x − {a})/(x − {b})| + C.', '1/((x − a)(x − b)) = (1/(a − b))[1/(x − a) − 1/(x − b)].', 'a', 'Partial fractions then integrate.'),
        ('(x² + 1)/(x² − 5x + 6) can be split directly into A/(x − 2) + B/(x − 3).', 'Partial fractions need a proper rational function.', 'd', 'The fraction is improper: divide first (it equals 1 + (5x − 5)/(x² − 5x + 6)). A false, R true.'),
        ('∫ dx/(x² − 1) = (1/2) log|(x − 1)/(x + 1)| + C.', '1/(x² − 1) = (1/2)[1/(x − 1) − 1/(x + 1)].', 'a', 'R gives the partial fractions.'),
    ])(r)


def c7s3_case(r):
    a, b = sorted(r.sample(range(1, 8), 2))
    who = name(r)
    A, B = Fr(1, b - a), Fr(-1, b - a)
    return Q((f'In a chemistry practical, {who} meets the integral ∫ dx/((x + {a})(x + {b})). (i) Write 1/((x + {a})(x + {b})) as partial fractions. (ii) Evaluate the integral. '
              f'(iii) Hence find ∫ (from 0 to 1) dx/((x + {a})(x + {b})) in terms of logarithms.'),
             f'(i) {fz(A)}[1/(x + {a}) − 1/(x + {b})] (ii) {fz(A)} log|(x + {a})/(x + {b})| + C (iii) {fz(A)} log({fz(Fr((1 + a) * b, a * (1 + b)))})',
             '(i) 1 mark (ii) 1 mark (iii) 2 marks.', _v=(lambda: float(A) * math.log((1 + a) * b / (a * (1 + b))), lambda: simpson(lambda x: 1 / ((x + a) * (x + b)), 0, 1)))


# ---- st4 integration by parts and special forms

def c7s4_parts(r):
    a = r.choice([1, 2, 3, 4])
    n = r.randint(1, 4)
    kind = r.randint(0, 6)
    if kind == 0:
        ans = f'{ex(a)}(x/{a} − 1/{a * a}) + C'.replace('x/1', 'x').replace('1/1)', '1)')
        return Q(f'Find ∫ x{ex(a)} dx.', ans, 'By parts with u = x, dv = e^(ax) dx.', [f'x{ex(a)}/{a} + C'.replace('/1 ', ' '), f'{ex(a)}(x + 1) + C', f'x²{ex(a)}/2 + C'],
                 _i=(lambda x: x * math.exp(a * x), lambda x: math.exp(a * x) * (x / a - 1 / a ** 2), 0.4))
    if kind == 1:
        ans = f'−x cos {a}x/{a} + sin {a}x/{a * a} + C'.replace(' 1x', ' x').replace('/1 ', ' ').replace('/1 +', ' +')
        return Q(f'Find ∫ x sin {a}x dx.'.replace('sin 1x', 'sin x'), ans, 'By parts with u = x.', [f'x cos {a}x/{a} + sin {a}x/{a * a} + C'.replace(' 1x', ' x'), f'−x cos {a}x + C'.replace(' 1x', ' x'), f'x² sin {a}x/2 + C'.replace(' 1x', ' x')],
                 _i=(lambda x: x * math.sin(a * x), lambda x: -x * math.cos(a * x) / a + math.sin(a * x) / a ** 2, 0.7))
    if kind == 2:
        ans = f'x sin {a}x/{a} + cos {a}x/{a * a} + C'.replace(' 1x', ' x').replace('/1 ', ' ')
        return Q(f'Find ∫ x cos {a}x dx.'.replace('cos 1x', 'cos x'), ans, 'By parts with u = x.', [f'x sin {a}x/{a} − cos {a}x/{a * a} + C'.replace(' 1x', ' x'), f'−x sin {a}x + C'.replace(' 1x', ' x'), f'x² cos {a}x/2 + C'.replace(' 1x', ' x')],
                 _i=(lambda x: x * math.cos(a * x), lambda x: x * math.sin(a * x) / a + math.cos(a * x) / a ** 2, 0.7))
    if kind == 3:
        ans = f'x{supx(str(n + 1))} log x/{n + 1} − x{supx(str(n + 1))}/{(n + 1) ** 2} + C'
        return Q(f'Find ∫ x{supx(str(n)) if n > 1 else ""} log x dx.', ans, 'By parts with u = log x, dv = xⁿ dx.', [f'x{supx(str(n + 1))} log x/{n + 1} + C', f'x{supx(str(n + 1))} log x/{n + 1} + x{supx(str(n + 1))}/{(n + 1) ** 2} + C', f'log x/x + C'],
                 _i=(lambda x: x ** n * math.log(x), lambda x: x ** (n + 1) * math.log(x) / (n + 1) - x ** (n + 1) / (n + 1) ** 2, 1.6))
    if kind == 4:
        return Q('Find ∫ log x dx.', 'x log x − x + C', 'By parts with u = log x, dv = dx.', ['1/x + C', 'x log x + C', '(log x)²/2 + C'], _i=(lambda x: math.log(x), lambda x: x * math.log(x) - x, 1.8))
    if kind == 5:
        return Q('Find ∫ x² eˣ dx.', 'eˣ(x² − 2x + 2) + C', 'By parts twice.', ['x²eˣ + C', 'eˣ(x² + 2x + 2) + C', 'x³eˣ/3 + C'], _i=(lambda x: x * x * math.exp(x), lambda x: math.exp(x) * (x * x - 2 * x + 2), 0.6))
    return Q('Find ∫ x tan⁻¹x dx.', '((x² + 1)/2) tan⁻¹x − x/2 + C', 'By parts with u = tan⁻¹x; x²/(1 + x²) = 1 − 1/(1 + x²).', ['(x²/2) tan⁻¹x + C', '((x² + 1)/2) tan⁻¹x + x/2 + C', 'x tan⁻¹x − log(1 + x²) + C'],
             _i=(lambda x: x * math.atan(x), lambda x: (x * x + 1) / 2 * math.atan(x) - x / 2, 0.9))


EXF = [
    ('eˣ(sin x + cos x)', 'eˣ sin x + C', lambda x: math.exp(x) * (math.sin(x) + math.cos(x)), lambda x: math.exp(x) * math.sin(x)),
    ('eˣ(1/x − 1/x²)', 'eˣ/x + C', lambda x: math.exp(x) * (1 / x - 1 / x ** 2), lambda x: math.exp(x) / x),
    ('eˣ(tan x + sec²x)', 'eˣ tan x + C', lambda x: math.exp(x) * (math.tan(x) + 1 / math.cos(x) ** 2), lambda x: math.exp(x) * math.tan(x)),
    ('eˣ(x + 1)', 'x eˣ + C', lambda x: math.exp(x) * (x + 1), lambda x: x * math.exp(x)),
    ('eˣ(x − 1)/x²', 'eˣ/x + C', lambda x: math.exp(x) * (x - 1) / x ** 2, lambda x: math.exp(x) / x),
    ('eˣ(1/x + log x)', 'eˣ log x + C', lambda x: math.exp(x) * (1 / x + math.log(x)), lambda x: math.exp(x) * math.log(x)),
    ('eˣ(sec x + sec x tan x)', 'eˣ sec x + C', lambda x: math.exp(x) * (1 / math.cos(x)) * (1 + math.tan(x)), lambda x: math.exp(x) / math.cos(x)),
    ('eˣ(1/(1 + x²) + tan⁻¹x)', 'eˣ tan⁻¹x + C', lambda x: math.exp(x) * (1 / (1 + x * x) + math.atan(x)), lambda x: math.exp(x) * math.atan(x)),
    ('eˣ(sin⁻¹x + 1/√(1 − x²))', 'eˣ sin⁻¹x + C', lambda x: math.exp(x) * (math.asin(x) + 1 / math.sqrt(1 - x * x)), lambda x: math.exp(x) * math.asin(x)),
    ('eˣ x/(1 + x)²', 'eˣ/(1 + x) + C', lambda x: math.exp(x) * x / (1 + x) ** 2, lambda x: math.exp(x) / (1 + x)),
]


def c7s4_exf(r):
    i, a, f, Fx = r.choice(EXF)
    w = [x[1] for x in EXF if x[1] != a]
    r.shuffle(w)
    return Q(f'Find ∫ {i} dx.', a, 'Use ∫ eˣ[f(x) + f′(x)] dx = eˣ f(x) + C.', w[:3], _i=(f, Fx, 0.5))


def c7s4_special(r):
    a = r.choice([1, 2, 3, 4, 5, 6])
    kind = r.randint(0, 5)
    a2 = a * a
    if kind == 0:
        ans = f'(1/{a}) tan⁻¹(x/{a}) + C'.replace('(1/1) ', '').replace('(x/1)', 'x')
        return Q(f'Find ∫ dx/(x² + {a2}).', ans, 'Standard form ∫ dx/(x² + a²) = (1/a) tan⁻¹(x/a) + C.', dist3(ans, [f'tan⁻¹(x/{a}) + C', f'(1/{2 * a}) log|(x − {a})/(x + {a})| + C', f'{a} tan⁻¹({a}x) + C']),
                 _i=(lambda x: 1 / (x * x + a2), lambda x: math.atan(x / a) / a, 0.6))
    if kind == 1:
        ans = f'(1/{2 * a}) log|(x − {a})/(x + {a})| + C'
        return Q(f'Find ∫ dx/(x² − {a2}).', ans, 'Standard form ∫ dx/(x² − a²) = (1/2a) log|(x − a)/(x + a)| + C.', dist3(ans, [f'(1/{2 * a}) log|(x + {a})/(x − {a})| + C', f'(1/{a}) tan⁻¹(x/{a}) + C', f'log|x² − {a2}| + C']),
                 _i=(lambda x: 1 / (x * x - a2), lambda x: math.log(abs((x - a) / (x + a))) / (2 * a), a + 1.5))
    if kind == 2:
        ans = f'sin⁻¹(x/{a}) + C'.replace('(x/1)', 'x')
        return Q(f'Find ∫ dx/√({a2} − x²).', ans, 'Standard form ∫ dx/√(a² − x²) = sin⁻¹(x/a) + C.', dist3(ans, [f'(1/{a}) sin⁻¹(x/{a}) + C', f'log|x + √(x² − {a2})| + C', f'cos⁻¹({a}x) + C']),
                 _i=(lambda x: 1 / math.sqrt(a2 - x * x), lambda x: math.asin(x / a), 0.5))
    if kind == 3:
        ans = f'log|x + √(x² + {a2})| + C'
        return Q(f'Find ∫ dx/√(x² + {a2}).', ans, 'Standard form ∫ dx/√(x² + a²) = log|x + √(x² + a²)| + C.', dist3(ans, [f'log|x + √(x² − {a2})| + C', f'sin⁻¹(x/{a}) + C', f'(1/{a}) tan⁻¹(x/{a}) + C']),
                 _i=(lambda x: 1 / math.sqrt(x * x + a2), lambda x: math.log(x + math.sqrt(x * x + a2)), 0.5))
    if kind == 4:
        ans = f'(x/2)√({a2} − x²) + ({fz(Fr(a2, 2))}) sin⁻¹(x/{a}) + C'.replace('(x/1)', 'x')
        return Q(f'Find ∫ √({a2} − x²) dx.', ans, 'Standard form ∫ √(a² − x²) dx = (x/2)√(a² − x²) + (a²/2) sin⁻¹(x/a) + C.',
                 dist3(ans, [f'(x/2)√({a2} − x²) − ({fz(Fr(a2, 2))}) sin⁻¹(x/{a}) + C', f'({a2} − x²)^(3/2) + C', f'(x/2)√({a2} − x²) + C']), _i=(lambda x: math.sqrt(a2 - x * x), lambda x: x / 2 * math.sqrt(a2 - x * x) + a2 / 2 * math.asin(x / a), 0.5))
    p = r.randint(-5, 5)
    k = r.choice([1, 2, 3, 4])
    q = p * p + k * k
    ans = f'(1/{k}) tan⁻¹(({lin(1, p)})/{k}) + C'.replace('(1/1) ', '').replace(f'/1)', ')')
    return Q(f'Find ∫ dx/(x² {"+" if 2 * p >= 0 else "−"} {abs(2 * p)}x + {q}).'.replace('+ 0x ', ''), ans, f'x² + {2 * p}x + {q} = ({lin(1, p)})² + {k * k}; standard form with a = {k}.',
             dist3(ans, [f'tan⁻¹({lin(1, p)}) + C', f'(1/{2 * k}) log|({lin(1, p - k)})/({lin(1, p + k)})| + C', f'log|x² + {2 * p}x + {q}| + C']), _i=(lambda x: 1 / (x * x + 2 * p * x + q), lambda x: math.atan((x + p) / k) / k, 0.3))


def c7s4_mcq(r):
    return mcqbank([
        ('In integration by parts, ∫ u v dx = …', 'u∫v dx − ∫(u′ ∫v dx) dx', ['u′∫v dx − ∫u v′ dx', '∫u dx · ∫v dx', 'u v − ∫u′ v′ dx'], 'Formula of integration by parts.'),
        ('∫ eˣ (f(x) + f′(x)) dx equals …', 'eˣ f(x) + C', ['eˣ f′(x) + C', 'f(x) + C', 'eˣ (f(x) − f′(x)) + C'], 'd/dx (eˣ f) = eˣ(f + f′).'),
        ('∫ dx/(x² + a²) equals …', '(1/a) tan⁻¹(x/a) + C', ['tan⁻¹(x/a) + C', 'a tan⁻¹(x/a) + C', '(1/2a) log|(x − a)/(x + a)| + C'], 'Standard form.'),
        ('∫ dx/√(a² − x²) equals …', 'sin⁻¹(x/a) + C', ['(1/a) sin⁻¹(x/a) + C', 'cos⁻¹(x/a) + C', 'log|x + √(a² − x²)| + C'], 'Standard form.'),
        ('For ∫ x eˣ dx by parts, the first function u should be …', 'x', ['eˣ', 'x eˣ', '1'], 'ILATE: algebraic before exponential.'),
        ('∫ log x dx equals …', 'x log x − x + C', ['1/x + C', 'x log x + C', 'log x/x + C'], 'By parts with 1 as the second function.'),
    ])(r)


def c7s4_ar(r):
    a = r.randint(2, 6)
    return arbank([
        ('∫ eˣ(sin x + cos x) dx = eˣ sin x + C.', 'd/dx (sin x) = cos x.', 'a', 'Form eˣ(f + f′) with f = sin x.'),
        (f'∫ x e^({a}x) dx = x e^({a}x)/{a} + C.', 'In integration by parts the second term ∫(u′∫v dx) dx cannot be omitted.', 'd', f'Correct answer e^({a}x)(x/{a} − 1/{a * a}) + C; A false, R true.'),
        (f'∫ dx/(x² + {a * a}) = (1/{a}) tan⁻¹(x/{a}) + C.', 'd/dx tan⁻¹(x/a) = a/(a² + x²).', 'a', 'Differentiate the answer.'),
        ('∫ log x dx = 1/x + C.', 'd/dx (log x) = 1/x.', 'd', 'That is the derivative, not the integral; ∫ log x dx = x log x − x + C. A false, R true.'),
    ])(r)


def c7s4_case(r):
    a = r.choice([1, 2, 3])
    who = name(r)
    return Q((f'{who} uses the ILATE rule to evaluate ∫ x e^({a}x) dx. (i) Which function should be taken as the first function, and why? (ii) Write the formula for integration by parts. '
              f'(iii) Evaluate the integral.').replace('e^(1x)', 'eˣ'), f'(i) x (algebraic before exponential) (ii) ∫uv dx = u∫v dx − ∫(u′∫v dx) dx (iii) {ex(a)}(x/{a} − 1/{a * a}) + C'.replace('x/1 ', 'x ').replace('1/1)', '1)'),
             '(i) 1 mark (ii) 1 mark (iii) 2 marks.', _i=(lambda x: x * math.exp(a * x), lambda x: math.exp(a * x) * (x / a - 1 / a ** 2), 0.3))


# ---- st5 definite integrals

def c7s5_poly(r):
    a, b = sorted(r.sample(range(-2, 5), 2))
    cs = [(r.randint(-3, 4), 2), (r.randint(-5, 5), 1), (r.randint(-6, 6), 0)]
    cs = [(c, n) for c, n in cs if c] or [(1, 2)]
    val = sum(Fr(c, n + 1) * (b ** (n + 1) - a ** (n + 1)) for c, n in cs)
    anti = polyF([(Fr(c, n + 1), n + 1) for c, n in cs])
    return Q(f'Evaluate ∫ from {a} to {b} of ({polyF(cs)}) dx.', fz(val), f'Antiderivative {anti}; value F({b}) − F({a}) = {fz(val)}.',
             dist3(fz(val), [fz(-val) if val else '1', fz(sum(Fr(c, n + 1) * b ** (n + 1) for c, n in cs)), fz(val + 1), fz(val * 2)]),
             _v=(lambda: float(val), lambda: simpson(lambda x: peval(cs, x), a, b)))


DEF_I = [
    ('∫ from 0 to π/2 of sin x/(sin x + cos x) dx', 'π/4', lambda: math.pi / 4, lambda: simpson(lambda x: math.sin(x) / (math.sin(x) + math.cos(x)), 0, math.pi / 2)),
    ('∫ from 0 to π/2 of √(sin x)/(√(sin x) + √(cos x)) dx', 'π/4', lambda: math.pi / 4, lambda: simpson(lambda x: math.sqrt(math.sin(x)) / (math.sqrt(math.sin(x)) + math.sqrt(math.cos(x))), 1e-9, math.pi / 2 - 1e-9, 20000)),
    ('∫ from 0 to π/2 of sin²x dx', 'π/4', lambda: math.pi / 4, lambda: simpson(lambda x: math.sin(x) ** 2, 0, math.pi / 2)),
    ('∫ from 0 to 1 of x eˣ dx', '1', lambda: 1.0, lambda: simpson(lambda x: x * math.exp(x), 0, 1)),
    ('∫ from 0 to π of x sin x dx', 'π', lambda: math.pi, lambda: simpson(lambda x: x * math.sin(x), 0, math.pi)),
    ('∫ from −π/2 to π/2 of sin⁷x dx', '0', lambda: 0.0, lambda: simpson(lambda x: math.sin(x) ** 7, -math.pi / 2, math.pi / 2)),
    ('∫ from −1 to 1 of x³ cos x dx', '0', lambda: 0.0, lambda: simpson(lambda x: x ** 3 * math.cos(x), -1, 1)),
    ('∫ from 0 to 1 of dx/(1 + x²)', 'π/4', lambda: math.pi / 4, lambda: simpson(lambda x: 1 / (1 + x * x), 0, 1)),
    ('∫ from 0 to π/4 of tan x dx', '(1/2) log 2', lambda: 0.5 * math.log(2), lambda: simpson(math.tan, 0, math.pi / 4)),
    ('∫ from 1 to e of log x dx', '1', lambda: 1.0, lambda: simpson(math.log, 1, math.e)),
    ('∫ from 0 to π/2 of cos²x dx', 'π/4', lambda: math.pi / 4, lambda: simpson(lambda x: math.cos(x) ** 2, 0, math.pi / 2)),
    ('∫ from 0 to 2π of |sin x| dx', '4', lambda: 4.0, lambda: simpson(lambda x: abs(math.sin(x)), 0, 2 * math.pi, 20000)),
    ('∫ from 0 to π/2 of log(tan x) dx', '0', lambda: 0.0, None),
    ('∫ from 0 to 1 of x(1 − x)⁵ dx', '1/42', lambda: 1 / 42, lambda: simpson(lambda x: x * (1 - x) ** 5, 0, 1)),
    ('∫ from 2 to 8 of √(10 − x)/(√x + √(10 − x)) dx', '3', lambda: 3.0, lambda: simpson(lambda x: math.sqrt(10 - x) / (math.sqrt(x) + math.sqrt(10 - x)), 2, 8)),
]


def c7s5_prop(r):
    s, a, fv, fn_ = r.choice(DEF_I)
    others = [x[1] for x in DEF_I if x[1] != a]
    others = list(dict.fromkeys(others + ['π/2', 'π/8', '2', 'log 2']))
    r.shuffle(others)
    v = Q(f'Evaluate {s}.', a, 'Use the properties of definite integrals (e.g. ∫ₐᵇ f(x) dx = ∫ₐᵇ f(a + b − x) dx, odd/even functions) or the fundamental theorem.', others[:3])
    if fn_:
        v['_v'] = (fv, fn_)
    return v


def c7s5_mod(r):
    c = r.randint(1, 5)
    a, b = r.randint(-2, 0), r.randint(c + 1, c + 4)
    val = Fr((c - a) ** 2 + (b - c) ** 2, 2)
    return Q(f'Evaluate ∫ from {a} to {b} of |x − {c}| dx.', fz(val), f'Split at x = {c}: ∫ from {a} to {c} of ({c} − x) dx + ∫ from {c} to {b} of (x − {c}) dx = {fz(Fr((c - a) ** 2, 2))} + {fz(Fr((b - c) ** 2, 2))} = {fz(val)}.',
             dist3(fz(val), [fz(Fr((b - c) ** 2 - (c - a) ** 2, 2)), fz(Fr((b - a) ** 2, 2)), fz(val + 1)]), _v=(lambda: float(val), lambda: simpson(lambda x: abs(x - c), a, b, 6000)))


def c7s5_log(r):
    a, b = sorted(r.sample([1, 2, 3, 4, 5, 6, 8, 9, 10, 12], 2))
    k = r.choice([1, 2, 3])
    ans = f'{"" if k == 1 else k} log({fz(Fr(b, a))})'.strip()
    return Q(f'Evaluate ∫ from {a} to {b} of {k}/x dx.'.replace(' 1/x', ' 1/x'), ans, f'{k}[log x] from {a} to {b} = {k} log({b}/{a}).'.replace('1[', '['),
             [f'{fz(Fr(k, a) - Fr(k, b))}', f'{k} log({b * a})'.replace('1 log', 'log'), f'{fz(Fr(k * (b * b - a * a), 2))}'], _v=(lambda: k * math.log(b / a), lambda: simpson(lambda x: k / x, a, b)))


def c7s5_mcq(r):
    return mcqbank([
        ('If f is an odd function, then ∫ from −a to a of f(x) dx = …', '0', ['2∫₀ᵃ f(x) dx', '∫₀ᵃ f(x) dx', 'a f(a)'], 'Property P6.'),
        ('If f is an even function, then ∫ from −a to a of f(x) dx = …', '2∫₀ᵃ f(x) dx', ['0', '∫₀ᵃ f(x) dx', '−2∫₀ᵃ f(x) dx'], 'Property P6.'),
        ('∫ₐᵇ f(x) dx = …', '∫ₐᵇ f(a + b − x) dx', ['∫ₐᵇ f(a − x) dx', '−∫ₐᵇ f(x) dx', '∫₀ᵇ f(x) dx'], 'Property P3.'),
        ('∫ₐᵃ f(x) dx = …', '0', ['f(a)', '2a', 'a f(a)'], 'Equal limits.'),
        ('∫ from 0 to π/2 of cos x/(sin x + cos x) dx = …', 'π/4', ['π/2', '1', '0'], 'Use P4 and add to the sin x version.'),
        ('The fundamental theorem of calculus states that ∫ₐᵇ f(x) dx = …', 'F(b) − F(a), where F′ = f', ['F(a) − F(b)', 'f(b) − f(a)', 'F(b) + F(a)'], 'Second fundamental theorem.'),
        ('∫ from 0 to 2a of f(x) dx = 2∫₀ᵃ f(x) dx if …', 'f(2a − x) = f(x)', ['f(2a − x) = −f(x)', 'f is odd', 'f(0) = 0'], 'Property P6 (second form).'),
    ])(r)


def c7s5_ar(r):
    n = r.choice([3, 5, 7, 9])
    return arbank([
        (f'∫ from −1 to 1 of x{supx(str(n))} dx = 0.', f'x{supx(str(n))} is an odd function.', 'a', 'Odd integrand over a symmetric interval.'),
        ('∫ from −1 to 1 of x² dx = 0.', 'x² is an even function.', 'd', 'The value is 2/3; A false, R true.'),
        ('∫ from 0 to π/2 of sin x/(sin x + cos x) dx = π/4.', '∫₀ᵃ f(x) dx = ∫₀ᵃ f(a − x) dx.', 'a', 'Add I to its P4 form: 2I = π/2.'),
        ('∫ from 0 to 2 of x dx = 2.', 'The definite integral gives the area between the curve and the x-axis over the interval.', 'b', 'Both true; A follows from the fundamental theorem (x²/2), the area statement does not compute it.'),
    ])(r)


def c7s5_long(r):
    kind = r.randint(0, 2)
    if kind == 0:
        return Q('Evaluate ∫ from 0 to π of x/(1 + sin x) dx.', 'π', 'I = ∫(π − x)/(1 + sin x) dx ⇒ 2I = π∫ dx/(1 + sin x) (2 marks); ∫₀^π dx/(1 + sin x) = [tan x − sec x]₀^π = 2 (2 marks); I = π (1 mark).',
                 _v=(lambda: math.pi, lambda: simpson(lambda x: x / (1 + math.sin(x)), 0, math.pi)))
    if kind == 1:
        return Q('Evaluate ∫ from 0 to π/2 of log(sin x) dx.', '−(π/2) log 2', 'I = ∫ log cos x dx (P4) (1 mark); 2I = ∫ log(sin 2x/2) dx (2 marks); evaluate to get I = −(π/2) log 2 (2 marks).')
    a = r.choice([2, 3, 4, 5])
    return Q(f'Evaluate ∫ from 0 to π of x sin x/(1 + cos²x) dx.', 'π²/4', 'I = ∫(π − x) sin x/(1 + cos²x) dx ⇒ 2I = π∫ sin x/(1 + cos²x) dx (2 marks); t = cos x gives π[tan⁻¹t] from −1 to 1 = π²/2 (2 marks); I = π²/4 (1 mark).',
             _v=(lambda: math.pi ** 2 / 4, lambda: simpson(lambda x: x * math.sin(x) / (1 + math.cos(x) ** 2), 0, math.pi)))


def c7s5_case(r):
    a, b, c = r.randint(1, 4), r.randint(0, 6), r.randint(5, 20)
    T = r.choice([2, 3, 4, 5])
    val = Fr(a, 3) * T ** 3 + Fr(b, 2) * T ** 2 + c * T
    who = name(r)
    return Q((f'Water flows into {who}\'s overhead tank at a rate of R(t) = {polyF([(a, 2), (b, 1), (c, 0)], "t")} litres per minute, t minutes after the pump is switched on. '
              f'(i) Write the definite integral that gives the water collected in the first {T} minutes. (ii) Evaluate it. (iii) Is the flow rate increasing? Give a reason.'),
             f'(i) ∫ from 0 to {T} of ({polyF([(a, 2), (b, 1), (c, 0)], "t")}) dt (ii) {fz(val)} litres (iii) Yes: R′(t) = {polyF([(2 * a, 1), (b, 0)], "t")} > 0 for t > 0',
             '(i) 1 mark (ii) 2 marks (iii) 1 mark.', _v=(lambda: float(val), lambda: simpson(lambda t: a * t * t + b * t + c, 0, T)))


# ======================================================================= ch08 Application of Integrals

def c8s1_parab(r):
    a = r.choice([1, 4, 9, Fr(1, 4)])
    c = r.choice([1, 4, 9, 16]) if a in (1, 4, 9) else r.choice([4, 16])
    # area = 2 ∫0^c 2√(a x) dx = (8/3)√a c^(3/2)
    # area = 2 ∫0^c 2√(a x) dx = (8/3)√a c^(3/2)
    sa = Fr(math.isqrt(int(a.numerator if isinstance(a, Fr) else a)), math.isqrt(a.denominator) if isinstance(a, Fr) else 1)
    sc = math.isqrt(c)
    A = Fr(8, 3) * sa * sc ** 3
    k = 4 * a
    return Q(f'Find the area of the region bounded by the parabola y² = {fz(k)}x and the line x = {c}.', f'{fz(A)} sq units',
             f'By symmetry, area = 2∫ from 0 to {c} of √({fz(k)}x) dx = 2 × {fz(2 * sa)} × (2/3)({c})^(3/2) = {fz(A)} sq units.',
             [f'{fz(A / 2)} sq units', f'{fz(A * 2)} sq units', f'{fz(A * 3 / 4)} sq units'], _v=(lambda: float(A), lambda: 2 * simpson(lambda x: math.sqrt(float(k) * x), 0, c)))


def c8s1_conic(r):
    kind = r.randint(0, 2)
    a, b = r.sample(range(2, 9), 2)
    if kind == 0:
        return Q(f'Find the area enclosed by the ellipse x²/{a * a} + y²/{b * b} = 1.', f'{a * b}π sq units', f'Area = 4∫ from 0 to {a} of {co(Fr(b, a))}√({a * a} − x²) dx = π({a})({b}) = {a * b}π.',
                 [f'{a * b} sq units', f'{fz(Fr(a * b, 4))}π sq units', f'{(a + b)}π sq units'], _v=(lambda: math.pi * a * b, lambda: 4 * simpson(lambda x: b / a * math.sqrt(max(a * a - x * x, 0)), 0, a, 20000)))
    if kind == 1:
        return Q(f'Find the area of the circle x² + y² = {a * a} using integration.', f'{a * a}π sq units', f'Area = 4∫ from 0 to {a} of √({a * a} − x²) dx = 4 × π({a})²/4 = {a * a}π.', [f'{2 * a}π sq units', f'{fz(Fr(a * a, 4))}π sq units', f'{a * a} sq units'])
    m, p, q = r.choice([1, 2, 3]), r.randint(0, 2), r.randint(3, 6)
    c0 = r.randint(0, 4)
    A = Fr(m, 2) * (q * q - p * p) + c0 * (q - p)
    return Q(f'Find the area of the region bounded by the line y = {poly([m, c0])}, the x-axis and the lines x = {p} and x = {q}.', f'{fz(A)} sq units',
             f'Area = ∫ from {p} to {q} of ({poly([m, c0])}) dx = {fz(A)} sq units.', num_distractors(float(A), A * 2, A - c0 * (q - p), A + 1), _v=(lambda: float(A), lambda: simpson(lambda x: m * x + c0, p, q)))


def c8s1_under(r):
    p, q = sorted(r.sample(range(0, 5), 2))
    k = r.choice([1, 2, 3])
    A = Fr(k * (q ** 3 - p ** 3), 3)
    return Q(f'Find the area of the region bounded by the curve y = {co(k)}x², the x-axis and the lines x = {p} and x = {q}.'.replace('lines x = 0 and', 'y-axis and the line').replace('the y-axis and the line', 'the y-axis and the line'),
             f'{fz(A)} sq units', f'Area = ∫ from {p} to {q} of {co(k)}x² dx = {fz(Fr(k, 3))}({q ** 3} − {p ** 3}) = {fz(A)}.', num_distractors(float(A), k * (q * q - p * p), A * 3, A / 2),
             _v=(lambda: float(A), lambda: simpson(lambda x: k * x * x, p, q)))


def c8s1_mcq(r):
    return mcqbank([
        ('The area of the region bounded by the curve y = f(x) (f ≥ 0), the x-axis and the lines x = a, x = b is …', '∫ₐᵇ f(x) dx', ['∫ₐᵇ x f(x) dx', 'f(b) − f(a)', '∫ₐᵇ f′(x) dx'], 'Definition of area under a curve.'),
        ('The area enclosed by the ellipse x²/a² + y²/b² = 1 is …', 'πab', ['π(a + b)', 'πa²b²', '2πab'], 'Standard result.'),
        ('The area of the circle x² + y² = a² is …', 'πa²', ['2πa', 'πa²/4', '4πa²'], 'Standard result.'),
        ('If the curve lies below the x-axis on [a, b], the area between it and the x-axis is …', '|∫ₐᵇ f(x) dx|', ['∫ₐᵇ f(x) dx', '−f(b)', '0'], 'The integral is negative.'),
        ('The area of the region bounded by y² = 4ax and its latus rectum is …', '8a²/3', ['4a²/3', '2a²', '16a²/3'], '2∫₀ᵃ 2√(ax) dx.'),
        ('The area bounded by the curve x = g(y), the y-axis and the lines y = c, y = d is …', '∫_c^d g(y) dy (for g ≥ 0)', ['∫_c^d y g(y) dy', 'g(d) − g(c)', '∫_c^d g′(y) dy'], 'Horizontal strips.'),
    ])(r)


def c8s1_ar(r):
    a, b = r.sample(range(2, 8), 2)
    return arbank([
        (f'The area of the ellipse x²/{a * a} + y²/{b * b} = 1 is {a * b}π sq units.', 'The area of the ellipse x²/a² + y²/b² = 1 is πab.', 'a', 'Direct use of R.'),
        (f'∫ from −{a} to {a} of x³ dx gives the area between y = x³, the x-axis and x = ±{a}.', 'x³ is an odd function.', 'd', 'The integral is 0 but the area is 2∫₀ᵃ x³ dx > 0; A false, R true.'),
        (f'The area under y = x² from x = 0 to x = {a} is {fz(Fr(a ** 3, 3))} sq units.', 'd/dx (x³/3) = x².', 'a', 'Fundamental theorem.'),
    ])(r)


def c8s1_case(r):
    a, b = r.sample([2, 3, 4, 5, 6, 7, 8, 10, 12], 2)
    cost = r.choice([20, 40, 50, 100])
    who = name(r)
    return Q((f'A park in {r.choice(CITIES)} has an elliptical lawn x²/{a * a} + y²/{b * b} = 1 (units in metres), designed by {who}. '
              f'(i) Write the integral for the area of the lawn in the first quadrant. (ii) Find the total area of the lawn. (iii) Find the cost of planting grass at ₹{cost} per m² (take π = 22/7).'),
             f'(i) ∫ from 0 to {a} of ({b}/{a})√({a * a} − x²) dx (ii) {a * b}π m² (iii) ₹{fz(Fr(22, 7) * a * b * cost)}'.replace(f'({b}/{a})', f'({fz(Fr(b, a))})'),
             '(i) 1 mark (ii) 1 mark (iii) 2 marks.', _v=(lambda: math.pi * a * b / 4, lambda: simpson(lambda x: b / a * math.sqrt(max(a * a - x * x, 0)), 0, a, 20000)))


# ---- st2 curve and line

def c8s2_parline(r):
    r1, r2 = sorted(r.sample(range(-3, 5), 2))
    p, q = r1 + r2, -r1 * r2
    A = Fr((r2 - r1) ** 3, 6)
    kind = r.randint(0, 1)
    if kind == 0:
        return Q(f'Find the area of the region bounded by the curve y = x² and the line y = {poly([p, q])}.', f'{fz(A)} sq units',
                 f'Intersection: x² = {poly([p, q])} ⇒ x = {r1}, {r2} (1 mark); area = ∫ from {r1} to {r2} of ({poly([p, q])} − x²) dx (1 mark) = {fz(A)} sq units (1 mark).',
                 num_distractors(float(A), A * 2, A / 2, (r2 - r1) ** 2), _v=(lambda: float(A), lambda: simpson(lambda x: p * x + q - x * x, r1, r2)))
    a = r.choice([1, 2])
    A2 = A / (4 * a)
    return Q(f'Find the area of the region bounded by the curve x² = {4 * a}y and the line {4 * a}y = {poly([p, q])}.', f'{fz(A2)} sq units',
             f'Intersection: x² = {poly([p, q])} ⇒ x = {r1}, {r2}; area = (1/{4 * a})∫ from {r1} to {r2} of ({poly([p, q])} − x²) dx = {fz(A2)}.',
             num_distractors(float(A2), A, A2 * 2, A2 + 1), _v=(lambda: float(A2), lambda: simpson(lambda x: (p * x + q - x * x) / (4 * a), r1, r2)))


def c8s2_line_par(r):
    kind = r.randint(0, 1)
    if kind == 0:
        k = r.randint(1, 6)
        A = Fr(k ** 3, 6)
        return Q(f'Find the area of the region bounded by the parabola y = x² and the line y = {k}x.'.replace('y = 1x', 'y = x'), f'{fz(A)} sq units',
                 f'Meet at x = 0, {k}; area = ∫ from 0 to {k} of ({k}x − x²) dx = {fz(A)}.', num_distractors(float(A), Fr(k ** 3, 2), Fr(k ** 3, 3), A * 2), _v=(lambda: float(A), lambda: simpson(lambda x: k * x - x * x, 0, k)))
    a, m = r.choice([1, 2, 3]), r.choice([1, 2])
    A = Fr(8 * a * a, 3 * m ** 3)
    return Q(f'Find the area of the region bounded by the parabola y² = {4 * a}x and the line y = {m}x.'.replace('y = 1x', 'y = x'), f'{fz(A)} sq units',
             f'Meet at x = 0 and x = {fz(Fr(4 * a, m * m))}; area = ∫ (2√({a}x) − {m}x) dx = {fz(A)}.'.replace('√(1x)', '√x'), num_distractors(float(A), A * 2, Fr(4 * a * a, 3 * m ** 3), A + 1),
             _v=(lambda: float(A), lambda: simpson(lambda x: 2 * math.sqrt(a * x) - m * x, 0, 4 * a / m ** 2)))


def c8s2_chord(r):
    kind = r.randint(0, 1)
    if kind == 0:
        a = r.randint(2, 8)
        return Q(f'Find the area of the smaller region bounded by the circle x² + y² = {a * a} and the line x + y = {a}.', f'{fz(Fr(a * a, 4))}(π − 2) sq units',
                 f'Quarter circle minus triangle: π({a})²/4 − ({a})²/2 = {fz(Fr(a * a, 4))}(π − 2) (area via ∫ from 0 to {a} of [√({a * a} − x²) − ({a} − x)] dx).',
                 [f'{fz(Fr(a * a, 4))}π sq units', f'{fz(Fr(a * a, 2))}(π − 2) sq units', f'{fz(Fr(a * a, 4))}(π + 2) sq units'],
                 _v=(lambda: a * a * (math.pi - 2) / 4, lambda: simpson(lambda x: math.sqrt(max(a * a - x * x, 0)) - (a - x), 0, a, 20000)))
    a, b = r.sample(range(2, 7), 2)
    return Q(f'Find the area of the smaller region bounded by the ellipse x²/{a * a} + y²/{b * b} = 1 and the line x/{a} + y/{b} = 1.', f'{fz(Fr(a * b, 4))}(π − 2) sq units',
             f'∫ from 0 to {a} of [({fz(Fr(b, a))})√({a * a} − x²) − ({fz(Fr(b, a))})({a} − x)] dx = {a * b}π/4 − {a * b}/2 = ({fz(Fr(a * b, 4))})(π − 2) (3 marks for integral set-up and evaluation, 2 for diagram and limits).',
             [f'{fz(Fr(a * b, 4))}π sq units', f'{fz(Fr(a * b, 2))}(π − 2) sq units', f'{a * b}(π − 2) sq units'],
             _v=(lambda: a * b * (math.pi - 2) / 4, lambda: simpson(lambda x: b / a * math.sqrt(max(a * a - x * x, 0)) - b / a * (a - x), 0, a, 20000)))


def c8s2_mcq(r):
    return mcqbank([
        ('The area of the region bounded by y = x² and y = x is …', '1/6', ['1/3', '1/2', '1'], '∫₀¹ (x − x²) dx.'),
        ('The area bounded by y = x², the x-axis and x = 1 is …', '1/3', ['1/2', '1', '2/3'], '∫₀¹ x² dx.'),
        ('The area of the smaller region between the circle x² + y² = 4 and the line x + y = 2 is …', 'π − 2', ['π + 2', '2π − 2', 'π/2 − 1'], 'Quarter circle minus triangle.'),
        ('The area between the parabola y² = 4x and its latus rectum x = 1 is …', '8/3', ['4/3', '2/3', '16/3'], '2∫₀¹ 2√x dx.'),
        ('To find the area between a curve and a line, the limits of integration are usually …', 'the x-coordinates of their points of intersection', ['0 and 1', 'the intercepts of the line', 'the vertex of the curve'], 'Solve the equations together.'),
    ])(r)


def c8s2_ar(r):
    k = r.randint(1, 5)
    return arbank([
        (f'The area bounded by y = x² and y = {k}x is {fz(Fr(k ** 3, 6))} sq units.'.replace('y = 1x', 'y = x'), f'The curves meet at x = 0 and x = {k}.', 'b', 'Both true; the limits are needed but the value comes from evaluating the integral.'),
        (f'The area bounded by y = x² and y = {k}x is ∫ from 0 to {k} of (x² − {k}x) dx.'.replace(' 1x', ' x'), f'On (0, {k}) the line lies above the parabola.', 'd', 'The integrand should be (line − parabola); A false, R true.'),
        ('The area between y = x and y = x² is 1/6 sq units.', 'For 0 < x < 1, x > x², so area = ∫₀¹ (x − x²) dx.', 'a', 'R gives the integral = 1/6.'),
    ])(r)


def c8s2_case(r):
    r1, r2 = 0, r.choice([2, 3, 4, 6])
    p = r2
    A = Fr(r2 ** 3, 6)
    who = name(r)
    return Q((f'{who}, an architect in {r.choice(CITIES)}, designs an arch window bounded by the curve y = {p}x − x² and the x-axis (units in metres). '
              f'(i) Find where the curve meets the x-axis. (ii) Write the integral for the area of the window. (iii) Find the area of the glass needed.'),
             f'(i) x = 0 and x = {r2} (ii) ∫ from 0 to {r2} of ({p}x − x²) dx (iii) {fz(A)} m²', '(i) 1 mark (ii) 1 mark (iii) 2 marks.',
             _v=(lambda: float(A), lambda: simpson(lambda x: p * x - x * x, 0, r2)))


# ---- st3 symmetry and strips

def c8s3_horiz(r):
    c = r.randint(1, 5)
    kind = r.randint(0, 1)
    if kind == 0:
        A = Fr(4 * c ** 3, 3)
        return Q(f'Find the area of the region bounded by the curve y = x² and the line y = {c * c}, using horizontal strips.', f'{fz(A)} sq units',
                 f'x = ±√y; area = 2∫ from 0 to {c * c} of √y dy = (4/3)({c})³ = {fz(A)}.', num_distractors(float(A), A / 2, Fr(c ** 3, 3), A * 2), _v=(lambda: float(A), lambda: 2 * simpson(math.sqrt, 0, c * c)))
    p, q = sorted(r.sample(range(0, 5), 2))
    A = Fr(q ** 3 - p ** 3, 3)
    return Q(f'Find the area of the region bounded by the curve x = y², the y-axis and the lines y = {p} and y = {q}.', f'{fz(A)} sq units', f'Area = ∫ from {p} to {q} of y² dy = {fz(A)}.',
             num_distractors(float(A), q * q - p * p, A * 2, A + 1), _v=(lambda: float(A), lambda: simpson(lambda y: y * y, p, q)))


def c8s3_sym(r):
    a = r.choice([1, 2, 3, 4, 5])
    kind = r.randint(0, 2)
    if kind == 0:
        A = Fr(8 * a * a, 3)
        return Q(f'Find the area of the region bounded by the parabola y² = {4 * a}x and its latus rectum.', f'{fz(A)} sq units', f'Latus rectum x = {a}; by symmetry, area = 2∫ from 0 to {a} of 2√({a}x) dx = {fz(A)}.'.replace('√(1x)', '√x'),
                 num_distractors(float(A), A / 2, 4 * a * a, A * 2), _v=(lambda: float(A), lambda: 2 * simpson(lambda x: 2 * math.sqrt(a * x), 0, a)))
    if kind == 1:
        return Q(f'Find the area bounded by the curve y = |x| and the line y = {a}.', f'{a * a} sq units', f'By symmetry about the y-axis: 2∫ from 0 to {a} of ({a} − x) dx = {a * a}.', num_distractors(a * a, Fr(a * a, 2), 2 * a * a, a))
    return Q(f'Using integration, find the area of the region in the first quadrant enclosed by the x-axis, the line y = x and the circle x² + y² = {2 * a * a}.', f'{fz(Fr(a * a, 4))}π sq units',
             f'They meet at ({a}, {a}); area = ∫ from 0 to {a} of x dx + ∫ from {a} to {a}√2 of √({2 * a * a} − x²) dx = {fz(Fr(a * a, 2))} + ({fz(Fr(a * a, 4))}π − {fz(Fr(a * a, 2))}) = {fz(Fr(a * a, 4))}π.',
             [f'{fz(Fr(a * a, 2))}π sq units', f'{a * a}π sq units', f'{fz(Fr(a * a, 4))}(π − 2) sq units'],
             _v=(lambda: a * a * math.pi / 4, lambda: simpson(lambda x: x, 0, a) + simpson(lambda x: math.sqrt(max(2 * a * a - x * x, 0)), a, a * math.sqrt(2), 20000)))


def c8s3_mcq(r):
    return mcqbank([
        ('For a region symmetric about the x-axis, its area can be found as …', 'twice the area of the part above the x-axis', ['half the area above the x-axis', 'the area above the x-axis only', 'zero'], 'Symmetry.'),
        ('For the area between x = g(y), the y-axis and y = c, y = d, we use …', 'horizontal strips', ['vertical strips', 'no strips', 'circular strips'], 'Integrate with respect to y.'),
        ('The area of the region bounded by y = |x| and y = 1 is …', '1', ['2', '1/2', '4'], '2 × ½ × 1 × 1.'),
        ('The ellipse x²/a² + y²/b² = 1 is symmetric about …', 'both coordinate axes', ['the x-axis only', 'the y-axis only', 'the line y = x only'], 'Replace x by −x or y by −y.'),
        ('The area of the circle x² + y² = 16 in the first quadrant is …', '4π', ['16π', '8π', '2π'], 'Quarter of 16π.'),
    ])(r)


def c8s3_ar(r):
    a = r.randint(2, 6)
    return arbank([
        (f'The area enclosed by the circle x² + y² = {a * a} is 4∫ from 0 to {a} of √({a * a} − x²) dx.', 'The circle is symmetric about both the coordinate axes.', 'a', 'Four equal quarters.'),
        (f'The area between y² = {4 * a}x and x = {a} is 2∫ from 0 to {a} of 2√({a}x) dx.'.replace('√(1x)', '√x'), 'The parabola y² = 4ax is symmetric about the y-axis.', 'c', 'A is true; R is false: it is symmetric about the x-axis.'),
        ('For the region bounded by x = y², the y-axis and y = 1, horizontal strips are convenient.', 'The curve is given as x as a function of y.', 'a', 'Integrate x = y² with respect to y.'),
    ])(r)


def c8s3_case(r):
    a = r.choice([2, 3, 4, 5, 6])
    who = name(r)
    A = Fr(8 * a * a, 3)
    return Q((f'A satellite dish used by {who}\'s school club has a cross-section shaped like the parabola y² = {4 * a}x, cut off by the line x = {a} (its latus rectum), units in decimetres. '
              f'(i) Is the region symmetric? About which line? (ii) Write the area as an integral using this symmetry. (iii) Find the area.'),
             f'(i) Yes, about the x-axis (ii) 2∫ from 0 to {a} of 2√({a}x) dx (iii) {fz(A)} dm²'.replace('√(1x)', '√x'), '(i) 1 mark (ii) 1 mark (iii) 2 marks.',
             _v=(lambda: float(A), lambda: 2 * simpson(lambda x: 2 * math.sqrt(a * x), 0, a)))


# ======================================================================= ch09 Differential Equations

def c9s1_od(r):
    o = r.choice([1, 2, 3])
    names = {1: 'dy/dx', 2: 'd²y/dx²', 3: 'd³y/dx³'}
    p = r.choice([1, 2, 3, 4])
    parts = [f'({names[o]}){supx(str(p))}' if p > 1 else names[o]]
    if o > 1:
        q = r.choice([1, 2, 3, 5])
        parts.append(f'({names[o - 1]}){supx(str(q))}' if q > 1 else names[o - 1])
    trans = r.random() < 0.3
    if trans:
        parts.append(r.choice([f'sin({names[o]})', f'e^({names[o]})', f'log({names[o]})']))
    extra = r.choice(['y', 'y²', 'xy', 'sin y', '3y', 'x²'])
    rhs = r.choice(['0', 'x', 'eˣ', 'cos x'])
    r.shuffle(parts)
    eq = ' + '.join(parts) + f' + {extra} = {rhs}'
    deg = 'not defined' if trans else str(p)
    ans = f'order {o}; degree {deg}'
    return Q(f'Find the order and degree (if defined) of the differential equation {eq}.', ans,
             'Order = highest order derivative present; degree = its highest power when the equation is a polynomial in the derivatives' + ('; here a derivative appears inside a transcendental function, so the degree is not defined.' if trans else '.'),
             dist3(ans, [f'order {p}; degree {o}', f'order {o}; degree {"1" if deg != "1" else "2"}', f'order {o + 1}; degree {deg}', f'order {o}; degree not defined' if not trans else f'order {o}; degree 1']))


def c9s1_mcq(r):
    return mcqbank([
        ('The number of arbitrary constants in the general solution of a differential equation of order 4 is …', '4', ['0', '2', '3'], 'Equal to the order.'),
        ('The number of arbitrary constants in a particular solution of a differential equation of order 3 is …', '0', ['3', '1', '2'], 'A particular solution has no arbitrary constants.'),
        ('The degree of the differential equation (d²y/dx²)³ + (dy/dx)² + sin(dy/dx) + 1 = 0 is …', 'not defined', ['3', '2', '1'], 'Not a polynomial in the derivatives.'),
        ('The order of the differential equation 2x² d²y/dx² − 3 dy/dx + y = 0 is …', '2', ['1', '0', 'not defined'], 'Highest derivative d²y/dx².'),
        ('A solution of a differential equation containing as many arbitrary constants as its order is called …', 'the general solution', ['a particular solution', 'a singular solution', 'an integrating factor'], 'Definition.'),
        ('The degree of the differential equation (dy/dx)⁴ + 3y d²y/dx² = 0 is …', '1', ['4', '2', 'not defined'], 'Highest order derivative d²y/dx² has power 1.'),
    ])(r)


def c9s1_verify(r):
    kind = r.randint(0, 3)
    a = r.randint(2, 6)
    if kind == 0:
        return Q(f'Verify that y = A cos {a}x + B sin {a}x is a solution of d²y/dx² + {a * a}y = 0.', 'Yes', f'y″ = −{a * a}(A cos {a}x + B sin {a}x) = −{a * a}y.', ['No', 'Only if A = B', 'Only for x = 0'])
    if kind == 1:
        return Q(f'Verify that y = {ex(a)} + {a} is a solution of dy/dx = {a}(y − {a}).', 'Yes', f'dy/dx = {a}{ex(a)} = {a}(y − {a}).', ['No', 'Only if x = 0', 'Only if a = 1'])
    if kind == 2:
        return Q(f'Verify that y = x² + {a}x + C is a solution of dy/dx = 2x + {a}.', 'Yes', f'Differentiating, dy/dx = 2x + {a}.', ['No', 'Only for C = 0', 'Only for x > 0'])
    return Q(f'Verify that y = √(1 + x²) is a solution of y′ = xy/(1 + x²).', 'Yes', 'y′ = x/√(1 + x²) = x√(1 + x²)/(1 + x²) = xy/(1 + x²).', ['No', 'Only for x > 0', 'Only at x = 0'])


def c9s1_ar(r):
    n = r.randint(2, 5)
    return arbank([
        (f'The general solution of a differential equation of order {n} contains {n} arbitrary constants.', 'The number of arbitrary constants in the general solution equals the order of the equation.', 'a', 'R states the rule.'),
        ('The degree of the differential equation d²y/dx² + sin(dy/dx) = 0 is 1.', 'The degree is defined only when the equation is a polynomial in its derivatives.', 'd', 'sin(dy/dx) makes the degree undefined; A false, R true.'),
        ('y = Ce^x is the general solution of dy/dx = y.', 'y = 2eˣ satisfies dy/dx = y.', 'b', 'Both true; R gives one particular solution, not the reason for A.'),
    ])(r)


def c9s1_case(r):
    o = r.choice([2, 3])
    p = r.choice([2, 3])
    who = name(r)
    return Q((f'In a class test, {who} is given the equation (d{supx(str(o))}y/dx{supx(str(o))}){supx(str(p))} + (dy/dx)⁵ + y = 0 and the equation y″ + e^(y′) = x. '
              f'(i) Find the order and degree of the first equation. (ii) Find the order of the second and explain why its degree is not defined. (iii) How many arbitrary constants would the general solution of the first equation have?'),
             f'(i) order {o}, degree {p} (ii) order 2; e^(y′) is not a polynomial in y′ (iii) {o}', '(i) 1 mark (ii) 2 marks (iii) 1 mark.')


# ---- st2 variables separable

def c9s2_power(r):
    n, m = r.randint(0, 3), r.randint(0, 2)
    k = r.choice([1, 2, 3])
    x0, y0 = r.choice([0, 1]), r.choice([1, 2, 3])
    C = Fr(y0 ** (m + 1), m + 1) - Fr(k * x0 ** (n + 1), n + 1)
    lhs = f'y{supx(str(m + 1))}/{m + 1}' if m else 'y'
    rhs = f'{mono(Fr(k, n + 1), n + 1, first=True)}{term(C, "") if C else ""}'
    de = f'dy/dx = {co(k)}x{supx(str(n)) if n > 1 else ""}' + (f'/y{supx(str(m)) if m > 1 else ""}' if m else '')
    de = de.replace('x⁰', '').replace('dy/dx = x/', 'dy/dx = x/')
    if n == 0:
        de = f'dy/dx = {k}' + (f'/y{supx(str(m)) if m > 1 else ""}' if m else '')
    ans = f'{lhs} = {rhs}'
    return Q(f'Find the particular solution of the differential equation {de}, given that y = {y0} when x = {x0}.', ans,
             f'Separate: y{supx(str(m)) if m > 1 else ""} dy = {k}x{supx(str(n)) if n > 1 else ""} dx'.replace('y⁰ ', '').replace('x⁰', '').replace(' y dy', ' y dy') + f' (1 mark); integrate (1 mark); y({x0}) = {y0} gives C = {fz(C)} (1 mark).',
             _ode=(lambda x, y: k * x ** n / (y ** m), lambda x: ((m + 1) * (k * x ** (n + 1) / (n + 1) + float(C))) ** (1 / (m + 1)), 0.6))


SEP = [
    ('dy/dx = (1 + y²)/(1 + x²)', 'tan⁻¹y = tan⁻¹x + C', 'dy/(1 + y²) = dx/(1 + x²).'),
    ('dy/dx = e^(x + y)', 'eˣ + e⁻ʸ = C', 'e⁻ʸ dy = eˣ dx ⇒ −e⁻ʸ = eˣ + K.'),
    ('dy/dx = (1 − cos x)/(1 + cos x)', 'y = 2 tan(x/2) − x + C', 'tan²(x/2) = sec²(x/2) − 1.'),
    ('dy/dx = √(4 − y²), −2 < y < 2', 'sin⁻¹(y/2) = x + C', 'dy/√(4 − y²) = dx.'),
    ('dy/dx + y = 1, y ≠ 1', 'y = 1 + Ae⁻ˣ', 'dy/(1 − y) = dx ⇒ −log|1 − y| = x + C.'),
    ('sec²x tan y dx + sec²y tan x dy = 0', 'tan x tan y = C', 'sec²x/tan x dx + sec²y/tan y dy = 0 ⇒ log|tan x| + log|tan y| = K.'),
    ('dy/dx = sin⁻¹x', 'y = x sin⁻¹x + √(1 − x²) + C', 'Integrate by parts.'),
    ('dy/dx = y tan x', 'y = C sec x', 'dy/y = tan x dx ⇒ log|y| = log|sec x| + K.'),
    ('x dy/dx = y', 'y = Cx', 'dy/y = dx/x.'),
    ('dy/dx = xy²', '−1/y = x²/2 + C', 'dy/y² = x dx.'),
    ('(eˣ + e⁻ˣ) dy − (eˣ − e⁻ˣ) dx = 0', 'y = log(eˣ + e⁻ˣ) + C', 'dy = (eˣ − e⁻ˣ)/(eˣ + e⁻ˣ) dx; numerator is the derivative of the denominator.'),
]


def c9s2_gen(r):
    de, a, k = r.choice(SEP)
    others = [x[1] for x in SEP if x[1] != a]
    r.shuffle(others)
    return Q(f'Find the general solution of the differential equation {de}.', a, f'Variables separable: {k}', others[:3])


def c9s2_exp(r):
    k = r.choice([2, 3, -2, Fr(1, 2), -1, 4])
    y0 = r.choice([1, 2, 3, 5, 10])
    ans = f'y = {y0}e^({mono(Fr(k, 2), 2, first=True)})'.replace('y = 1e', 'y = e')
    return Q(f'Solve dy/dx = {co(k)}xy, given that y = {y0} when x = 0.', ans, f'dy/y = {co(k)}x dx ⇒ log|y| = {mono(Fr(k, 2), 2, first=True)} + C; y(0) = {y0} ⇒ {ans}.',
             dist3(ans, [f'y = {y0}e^({fn(k)}x²)'.replace('y = 1e', 'y = e'), f'y = {y0}{mono(Fr(k, 2), 2)}', f'y = {y0}e^({fn(k)}x)'.replace('y = 1e', 'y = e')]),
             _ode=(lambda x, y: float(k) * x * y, lambda x: y0 * math.exp(float(k) / 2 * x * x), 0.5))


EVALS = {Fr(1, 5): 1.2214, Fr(1, 4): 1.2840, Fr(3, 10): 1.3499, Fr(2, 5): 1.4918, Fr(1, 2): 1.6487, Fr(3, 5): 1.8221, Fr(3, 4): 2.1170, Fr(4, 5): 2.2255, Fr(1): 2.7183}


def c9s2_growth(r):
    kind = r.randint(0, 1)
    if kind == 0:
        while True:
            rate, t = r.choice([2, 3, 4, 5, 6, 8, 10]), r.choice([5, 10, 15, 20, 25])
            e = Fr(rate * t, 100)
            if e in EVALS:
                break
        P0 = r.choice([1000, 2000, 5000, 10000, 500])
        val = round(P0 * EVALS[e], 2)
        return Q(f'In a bank, principal increases continuously at the rate of {rate}% per year. Find the worth of ₹{P0} deposited for {t} years (e^{fn(e)} = {EVALS[e]}).'.replace('e^1 ', 'e '),
                 inr(val), f'dP/dt = ({rate}/100)P ⇒ P = P₀e^({fn(Fr(rate, 100))}t) (2 marks); P = {P0}e^{fn(e)} = {P0} × {EVALS[e]} = {inr(val)} (1 mark).',
                 [inr(round(P0 * (1 + rate * t / 100), 2)), inr(round(P0 * EVALS[e] * 2, 2)), inr(round(P0 * (EVALS[e] - 1), 2))])
    p = r.choice([5, 10, 20, 25, 50])
    h = r.choice([1, 2, 3, 4])
    m = r.choice([2, 3])
    ans = f't = {h} log {m}/log({fz(Fr(100 + p, 100))}) hours'.replace('t = 1 log', 't = log')
    return Q(f'The number of bacteria in a culture grows at a rate proportional to the number present. It increases by {p}% in {h} hour{"s" if h > 1 else ""}. In how many hours will the count become {m} times the original?',
             ans, f'dN/dt = kN ⇒ N = N₀eᵏᵗ (1 mark); e^({h}k) = {fz(Fr(100 + p, 100))} ⇒ k = (1/{h}) log({fz(Fr(100 + p, 100))}) (1 mark); eᵏᵗ = {m} ⇒ {ans} (1 mark).'.replace('(1/1) ', ''),
             [f't = {h * m} hours', f't = {h} log({fz(Fr(100 + p, 100))})/log {m} hours'.replace('t = 1 log', 't = log'), f't = {fz(Fr(100 * h * (m - 1), p))} hours'])


def c9s2_mcq(r):
    return mcqbank([
        ('The general solution of dy/dx = e^(x − y) is …', 'eʸ = eˣ + C', ['e⁻ʸ = eˣ + C', 'eʸ = e⁻ˣ + C', 'y = x + C'], 'eʸ dy = eˣ dx.'),
        ('The general solution of dy/dx = y/x is …', 'y = Cx', ['y = C/x', 'y = x + C', 'xy = C'], 'dy/y = dx/x.'),
        ('The solution of dy/dx = −x/y is …', 'x² + y² = C', ['x² − y² = C', 'xy = C', 'y = Cx'], 'y dy = −x dx.'),
        ('A differential equation of the form dy/dx = g(x)h(y) is solved by …', 'separating the variables', ['an integrating factor', 'putting y = vx', 'partial fractions only'], 'Variable separable form.'),
        ('The general solution of dy/dx = 2x is …', 'y = x² + C', ['y = 2x² + C', 'y = x²', 'y = 2 + C'], 'Integrate.'),
    ])(r)


def c9s2_ar(r):
    k = r.randint(2, 6)
    return arbank([
        (f'The general solution of dy/dx = {k}y is y = Ce^({k}x).', 'dy/y = k dx integrates to log|y| = kx + c.', 'a', 'Variables separable.'),
        (f'dy/dx = x + y is in variable separable form.', 'An equation dy/dx = F(x, y) is variable separable if F(x, y) = g(x)h(y).', 'd', 'x + y cannot be written as g(x)h(y); A false, R true.'),
        ('The curve through (0, 1) with dy/dx = y is y = eˣ.', 'The general solution of dy/dx = y is y = Ceˣ.', 'a', 'C = 1 from the point.'),
    ])(r)


def c9s2_case(r):
    P0 = r.choice([5000, 10000, 20000, 50000])
    p = r.choice([10, 20, 25, 50])
    t1 = r.choice([2, 5, 10])
    city = r.choice(CITIES)
    return Q((f'The population of a town near {city} grows at a rate proportional to the population. It was {P0} in 2015 and increased by {p}% in {t1} years. '
              f'(i) Write the differential equation and its general solution. (ii) Find the constant of proportionality k in terms of logarithms. (iii) Write the population t years after 2015.'),
             f'(i) dP/dt = kP, P = Ceᵏᵗ (ii) k = (1/{t1}) log({fz(Fr(100 + p, 100))}) (iii) P = {P0}({fz(Fr(100 + p, 100))})^(t/{t1})',
             '(i) 1 mark (ii) 1 mark (iii) 2 marks.')


def c9s2_long(r):
    a, b = r.randint(1, 6), r.randint(1, 6)
    x0, y0 = r.randint(0, 2), r.randint(0, 3)
    C = y0 * y0 + b * y0 - x0 * x0 - a * x0
    ans = f'y² + {b}y = x² + {a}x {"+" if C >= 0 else "−"} {abs(C)}'.replace('1y', 'y').replace(' 1x', ' x')
    return Q(f'Find the equation of the curve passing through ({x0}, {y0}) whose slope at any point (x, y) is (2x + {a})/(2y + {b}).', ans,
             f'(2y + {b}) dy = (2x + {a}) dx (1 mark); integrate: y² + {b}y = x² + {a}x + C (2 marks); point gives C = {C} (2 marks).'.replace('1y', 'y').replace(' 1x', ' x'),
             _ode=(lambda x, y: (2 * x + a) / (2 * y + b), lambda x: (-b + math.sqrt(b * b + 4 * (x * x + a * x + C))) / 2, x0 + 0.3))


# ---- st3 homogeneous

def c9s3_solve(r):
    k = r.choice([1, 2, 3, 4, 5])
    kind = r.randint(0, 4)
    if kind == 0:
        ans = f'y = {co(k)}x log|x| + Cx'
        return Q(f'Solve the differential equation dy/dx = (y + {k}x)/x, x ≠ 0.'.replace('+ 1x', '+ x'), ans, f'Put y = vx: v + x dv/dx = v + {k} ⇒ dv = {k} dx/x ⇒ v = {k} log|x| + C.'.replace(' 1 dx', ' dx').replace('= 1 log', '= log'),
                 dist3(ans, [f'y = {k}x + C', f'y = log|x| + Cx', f'y = {co(k)}x² log|x| + C']), _ode=(lambda x, y: (y + k * x) / x, lambda x: k * x * math.log(x) + 2 * x, 1.7))
    if kind == 1:
        ans = f'y² = {2 * k}x² log|x| + Cx²'.replace('= 2x²', '= 2x²')
        return Q(f'Solve the differential equation dy/dx = y/x + {k}x/y, x > 0.'.replace('+ 1x/y', '+ x/y'), ans, f'y = vx: v + x dv/dx = v + {k}/v ⇒ v dv = {k} dx/x ⇒ v²/2 = {k} log|x| + C.',
                 dist3(ans, [f'y² = {k}x² log|x| + Cx²'.replace('= 1x²', '= x²'), f'y = {k}x log|x| + Cx', f'y² = {2 * k} log|x| + C']), _ode=(lambda x, y: y / x + k * x / y, lambda x: math.sqrt(2 * k * x * x * math.log(x) + 3 * x * x), 1.4))
    if kind == 2:
        ans = f'−x/y = {co(k)}log|x| + C'
        return Q(f'Solve the differential equation dy/dx = y/x + {k}y²/x², x ≠ 0.'.replace('+ 1y²', '+ y²'), ans, f'y = vx: x dv/dx = {k}v² ⇒ dv/v² = {k} dx/x ⇒ −1/v = {k} log|x| + C.'.replace(' 1 dx', ' dx').replace('= 1 log', '= log'),
                 dist3(ans, [f'x/y = {co(k)}log|x| + C', f'y = {co(k)}x log|x| + Cx', f'−y/x = {co(k)}log|x| + C']), _ode=(lambda x, y: y / x + k * y * y / x ** 2, lambda x: -x / (k * math.log(x) + 2), 1.5))
    if kind == 3:
        return Q('Solve the differential equation x dy/dx = y + x tan(y/x).', 'sin(y/x) = Cx', 'y = vx: x dv/dx = tan v ⇒ cot v dv = dx/x ⇒ log|sin v| = log|x| + log|C|.', ['tan(y/x) = Cx', 'cos(y/x) = Cx', 'sin(y/x) = log|x| + C'],
                 _ode=(lambda x, y: y / x + math.tan(y / x), lambda x: x * math.asin(0.3 * x), 1.2))
    return Q('Solve the differential equation x dy/dx = y + x e^(y/x)... in the form dy/dx = y/x + e^(y/x).'.replace('x dy/dx = y + x e^(y/x)... in the form ', ''), '−e^(−y/x) = log|x| + C',
             'y = vx: x dv/dx = eᵛ ⇒ e⁻ᵛ dv = dx/x ⇒ −e⁻ᵛ = log|x| + C.', ['e^(y/x) = log|x| + C', 'e^(−y/x) = log|x| + C', 'y = x eˣ + C'],
             _ode=(lambda x, y: y / x + math.exp(y / x), lambda x: -x * math.log(-(math.log(x)) + 2), 1.3))


def c9s3_pick(r):
    good = ['dy/dx = (x² + y²)/(xy)', 'dy/dx = (x + y)/(x − y)', 'dy/dx = (y/x) + sin(y/x)', '(x² − xy) dy = (x² + y²)... i.e. dy/dx = (x² + y²)/(x² − xy)', 'dy/dx = (x³ + y³)/(x²y)', 'x dy − y dx = √(x² + y²) dx']
    bad = ['dy/dx = x + y²', 'dy/dx = (x + 1)/(y + 1)', 'dy/dx = xy + 1', 'dy/dx = (x² + y)/x', 'dy/dx = sin x + cos y', 'dy/dx = y² + x³', 'dy/dx = (x + y + 1)/(x − y)', 'dy/dx = eˣ y']
    g = r.choice(good).split('... i.e. ')[-1]
    b = r.sample(bad, 3)
    return mcq('Which of the following differential equations is homogeneous?', g, b, 'F(λx, λy) = λ⁰F(x, y): both numerator and denominator have the same degree.', r)


def c9s3_part(r):
    k = r.choice([1, 2, 3])
    y0 = r.choice([1, 2, 3])
    ans = f'y² = {2 * k}x² log x + {y0 * y0}x²'
    return Q(f'Find the particular solution of dy/dx = y/x + {k}x/y, x > 0, given y = {y0} when x = 1.'.replace('+ 1x/y', '+ x/y'), ans,
             f'Put y = vx (1 mark); v dv = {k} dx/x ⇒ y²/x² = {2 * k} log x + C (2 marks); C = {y0 * y0} (1 mark); answer (1 mark).',
             _ode=(lambda x, y: y / x + k * x / y, lambda x: math.sqrt(2 * k * x * x * math.log(x) + y0 * y0 * x * x), 1.6))


def c9s3_mcq(r):
    return mcqbank([
        ('To solve a homogeneous differential equation dy/dx = F(x, y), we substitute …', 'y = vx', ['y = v + x', 'x = y + v', 'y = eᵛ'], 'Standard method.'),
        ('A function F(x, y) is homogeneous of degree n if …', 'F(λx, λy) = λⁿF(x, y)', ['F(λx, λy) = F(x, y) + λⁿ', 'F(x, y) = xⁿ + yⁿ', 'F(λx, λy) = nF(x, y)'], 'Definition.'),
        ('The function F(x, y) = (x² + y²)/(xy) is homogeneous of degree …', '0', ['1', '2', '−1'], 'Numerator and denominator both of degree 2.'),
        ('The function x² − xy + 3y² is homogeneous of degree …', '2', ['1', '3', '0'], 'Every term has degree 2.'),
        ('For dx/dy = G(x, y) homogeneous, the substitution is …', 'x = vy', ['y = vx', 'x = v + y', 'y = vx²'], 'Mirror form.'),
    ])(r)


def c9s3_ar(r):
    k = r.randint(2, 5)
    return arbank([
        (f'dy/dx = (x² + {k}y²)/(xy) is a homogeneous differential equation.', 'Both numerator and denominator are homogeneous of degree 2.', 'a', 'Quotient is of degree 0.'),
        ('dy/dx = (x + y)/x is homogeneous.', 'It can be written as dy/dx = g(y/x) with g(v) = 1 + v.', 'a', 'Form g(y/x).'),
        (f'x² + {k}xy is homogeneous of degree 2.', f'Each term of x² + {k}xy has total degree 2.', 'a', 'Definition.'),
        ('dy/dx = x² + y is homogeneous.', 'F(λx, λy) = λ²x² + λy.', 'd', 'It is not λⁿF(x, y), so A false; R is a true computation.'),
    ])(r)


def c9s3_case(r):
    k = r.choice([1, 2, 3])
    who = name(r)
    return Q((f'{who} is asked to solve dy/dx = (x² + {k}y²)/({k}xy)... rewritten as dy/dx = x/({k}y) + y/x, x > 0. (i) Show that the equation is homogeneous. (ii) Write the equation after the substitution y = vx. '
              f'(iii) Solve it.').replace(f'dy/dx = (x² + {k}y²)/({k}xy)... rewritten as ', '').replace('(1y)', 'y'),
             f'(i) RHS is a function of y/x (degree 0) (ii) x dv/dx = 1/({k}v) (iii) y² = {co(Fr(2, k))}x² log x + Cx²'.replace('(1v)', 'v'), '(i) 1 mark (ii) 1 mark (iii) 2 marks.',
             _ode=(lambda x, y: x / (k * y) + y / x, lambda x: math.sqrt(2 / k * x * x * math.log(x) + x * x), 1.5))


# ---- st4 linear

def c9s4_xpow(r):
    while True:
        k, m = r.randint(1, 4), r.randint(-1, 3)
        if m + k + 1 != 0:
            break
    d = m + k + 1
    rhs = f'x{supx(str(m))}' if m not in (0, 1) else ('1' if m == 0 else 'x')
    if m == -1:
        rhs = '1/x'
    ans = f'y = {mono(Fr(1, d), m + 1, first=True) if m + 1 else fz(Fr(1, d))} + C/x{supx(str(k)) if k > 1 else ""}'
    return Q(f'Solve the differential equation dy/dx + ({k}/x)y = {rhs}, x > 0.'.replace('(1/x)y', 'y/x'), ans,
             f'IF = e^(∫{k}/x dx) = x{supx(str(k)) if k > 1 else ""} (1 mark); d/dx (yx{supx(str(k)) if k > 1 else ""}) = x{supx(str(m + k)) if m + k != 1 else ""} (1 mark); integrate and divide (1 mark).'.replace('x⁰', '1'),
             dist3(ans, [f'y = {mono(Fr(1, d), m + k + 1, first=True)} + C', f'y = {mono(Fr(1, m + 2) if m + 2 else 1, m + 1, first=True)} + C/x{supx(str(k)) if k > 1 else ""}', f'y = {mono(Fr(1, d), m + 1, first=True) if m + 1 else fz(Fr(1, d))} + Cx{supx(str(k)) if k > 1 else ""}']),
             _ode=(lambda x, y: x ** m - k / x * y, lambda x: x ** (m + 1) / d + 2 / x ** k, 1.3))


def c9s4_exp(r):
    while True:
        a, b = r.choice([1, 2, 3, -1]), r.choice([-1, 1, 2, 3, -2])
        if a + b != 0:
            break
    ans = f'y = {ex(b)}/{a + b} + C{ex(-a)}'.replace('/1 ', ' ').replace('/−1 ', ' × (−1) ')
    if a + b == -1:
        ans = f'y = −{ex(b)} + C{ex(-a)}'
    elif a + b == 1:
        ans = f'y = {ex(b)} + C{ex(-a)}'
    return Q(f'Solve dy/dx {"+" if a > 0 else "−"} {abs(a) if abs(a) != 1 else ""}y = {ex(b)}.', ans,
             f'IF = {ex(a)} (1 mark); d/dx(y{ex(a)}) = {ex(a + b)} (1 mark); y{ex(a)} = {ex(a + b)}/{a + b} + C (1 mark).',
             dist3(ans, [f'y = {ex(b)}/{a + b} + C', f'y = {ex(b)}/{b} + C{ex(-a)}', f'y = {ex(b)}/{a - b if a - b else 2} + C{ex(a)}']),
             _ode=(lambda x, y: math.exp(b * x) - a * y, lambda x: math.exp(b * x) / (a + b) + 2 * math.exp(-a * x), 0.4))


def c9s4_lin(r):
    a = r.choice([1, 2, 3, 4])
    b, c = r.randint(1, 6), r.randint(-4, 6)
    p, q = Fr(b, a), Fr(c, a) - Fr(b, a * a)
    ans = f'y = {mono(p, 1, first=True)}{term(q, "") if q else ""} + C{ex(-a)}'
    return Q(f'Find the general solution of dy/dx + {a if a > 1 else ""}y = {poly([b, c])}.', ans,
             f'IF = {ex(a)} (1 mark); y{ex(a)} = ∫({poly([b, c])}){ex(a)} dx (by parts) (1 mark); simplify (1 mark).', dist3(ans, [f'y = {mono(p, 1, first=True)} + C{ex(-a)}', f'y = {mono(Fr(b, 2), 2, first=True)}{term(c, "x")} + C', f'y = {mono(p, 1, first=True)}{term(q, "") if q else ""} + C{ex(a)}']),
             _ode=(lambda x, y: b * x + c - a * y, lambda x: float(p) * x + float(q) + 1.5 * math.exp(-a * x), 0.5))


def c9s4_trig(r):
    kind = r.randint(0, 2)
    if kind == 0:
        return Q('Solve dy/dx + y tan x = sec x, 0 ≤ x < π/2.', 'y = sin x + C cos x', 'IF = sec x; d/dx(y sec x) = sec²x ⇒ y sec x = tan x + C.', ['y = tan x + C', 'y = cos x + C sin x', 'y = sec x + C'],
                 _ode=(lambda x, y: 1 / math.cos(x) - y * math.tan(x), lambda x: math.sin(x) + 2 * math.cos(x), 0.4))
    if kind == 1:
        return Q('Solve dy/dx + y = sin x.', 'y = (sin x − cos x)/2 + Ce⁻ˣ', 'IF = eˣ; ∫eˣ sin x dx = eˣ(sin x − cos x)/2.', ['y = sin x + Ce⁻ˣ', 'y = (sin x + cos x)/2 + Ce⁻ˣ', 'y = −cos x + Ce⁻ˣ'],
                 _ode=(lambda x, y: math.sin(x) - y, lambda x: (math.sin(x) - math.cos(x)) / 2 + 3 * math.exp(-x), 0.7))
    return Q('Solve x dy/dx + 2y = x² log x, x > 0.', 'y = (x²/4) log x − x²/16 + C/x²', 'IF = x²; d/dx(x²y) = x³ log x; integrate by parts.', ['y = x² log x + C', 'y = (x²/4) log x + C/x²', 'y = (x²/2) log x − x²/4 + C/x²'],
             _ode=(lambda x, y: x * math.log(x) - 2 * y / x, lambda x: x * x / 4 * math.log(x) - x * x / 16 + 1 / x ** 2, 1.5))


def c9s4_if(r):
    kind = r.randint(0, 4)
    k = r.randint(2, 6)
    if kind == 0:
        return Q(f'Find the integrating factor of x dy/dx − {k}y = x³.', f'1/x{supx(str(k))}',
                 f'Divide by x: dy/dx − ({k}/x)y = x²; IF = e^(−{k} log x) = x^(−{k}).', [f'x{supx(str(k))}', f'e^(−{k}x)', f'log x{supx(str(k))}'])
    if kind == 1:
        return Q(f'Find the integrating factor of dy/dx + {k}y = sin x.', ex(k), f'IF = e^(∫{k} dx) = {ex(k)}.', [ex(-k), f'{k}x', f'e^({k})'])
    if kind == 2:
        return Q('Find the integrating factor of dy/dx + y cot x = 2x.', 'sin x', 'IF = e^(∫cot x dx) = e^(log sin x) = sin x.', ['cos x', 'cosec x', 'log sin x'])
    if kind == 3:
        return Q('Find the integrating factor of (1 + x²) dy/dx + 2xy = 1/(1 + x²).', '1 + x²', 'P = 2x/(1 + x²); IF = e^(log(1 + x²)) = 1 + x².', ['1/(1 + x²)', 'e^(x²)', 'tan⁻¹x'])
    return Q('Find the integrating factor of y dx − (x + 2y²) dy = 0, treating x as the dependent variable.', '1/y', 'dx/dy − x/y = 2y; IF = e^(−∫dy/y) = 1/y.', ['y', 'e^y', '−y'])


def c9s4_ivp(r):
    a, c = r.choice([1, 2, 3, 4, 5]), r.randint(1, 12)
    y0 = r.randint(-5, 10)
    K = Fr(c, a)
    ans = f'y = {fz(K)} {"+" if y0 - K >= 0 else "−"} {co(abs(y0 - K))}{ex(-a)}'
    if y0 == K:
        raise ValueError
    return Q(f'Find the particular solution of dy/dx + {a if a > 1 else ""}y = {c}, given y = {y0} when x = 0.', ans,
             f'IF = {ex(a)} (1 mark); y{ex(a)} = {co(K)}{ex(a)} + C (2 marks); y(0) = {y0} ⇒ C = {fz(y0 - K)} (1 mark); answer (1 mark).',
             _ode=(lambda x, y: c - a * y, lambda x: float(K) + float(y0 - K) * math.exp(-a * x), 0.3))


def c9s4_mcq(r):
    return mcqbank([
        ('The integrating factor of dy/dx + Py = Q, where P and Q are functions of x, is …', 'e^(∫P dx)', ['e^(∫Q dx)', '∫P dx', 'e^(−∫P dx)'], 'Standard.'),
        ('The integrating factor of dy/dx − y = x is …', 'e⁻ˣ', ['eˣ', 'x', '−x'], 'P = −1.'),
        ('The integrating factor of x dy/dx + y = x² (x > 0) is …', 'x', ['1/x', 'eˣ', 'log x'], 'P = 1/x.'),
        ('The solution of dy/dx + Py = Q is …', 'y·(IF) = ∫Q·(IF) dx + C', ['y = ∫Q dx + C', 'y·(IF) = ∫P·(IF) dx + C', 'y = Q·(IF) + C'], 'Standard.'),
        ('The integrating factor of dy/dx + y/x = x³ is …', 'x', ['1/x', 'x³', 'eˣ'], 'e^(log x).'),
        ('For dx/dy + P₁x = Q₁ (P₁, Q₁ functions of y), the integrating factor is …', 'e^(∫P₁ dy)', ['e^(∫P₁ dx)', 'e^(∫Q₁ dy)', '∫P₁ dy'], 'Roles of x and y interchanged.'),
    ])(r)


def c9s4_ar(r):
    k = r.randint(2, 6)
    return arbank([
        (f'The integrating factor of dy/dx + {k}y = x is e^({k}x).', 'For dy/dx + Py = Q, IF = e^(∫P dx).', 'a', f'∫{k} dx = {k}x.'),
        (f'The integrating factor of dy/dx + (1/x)y = x is 1/x.', 'For dy/dx + Py = Q, IF = e^(∫P dx).', 'd', 'IF = e^(log x) = x; A false, R true.'),
        ('dy/dx + y = eˣ is a linear differential equation.', 'It is of the form dy/dx + Py = Q with P = 1 and Q = eˣ.', 'a', 'Standard linear form.'),
        ('dy/dx + y² = x is a linear differential equation.', 'In a linear equation y and dy/dx appear only to the first power.', 'd', 'The y² term makes it non-linear; A false, R true.'),
    ])(r)


def c9s4_case(r):
    k = r.choice([Fr(1, 10), Fr(1, 5), Fr(1, 20)])
    S0 = r.choice([20, 30, 40, 50])
    inflow = r.choice([2, 3, 4, 5])
    who = name(r)
    return Q((f'A tank in {who}\'s school lab contains salt solution. Salt enters at {inflow} g/min and leaves at a rate {mono(k, 1, 'S', first=True)} g/min, where S is the amount (in g) present at time t minutes, with S = {S0} at t = 0. '
              f'(i) Write the differential equation for S. (ii) Find its integrating factor. (iii) Solve for S(t).'),
             f'(i) dS/dt + {mono(k, 1, 'S', first=True)} = {inflow} (ii) e^({mono(k, 1, 't', first=True)}) (iii) S = {fz(inflow / k)} {"+" if S0 - inflow / k >= 0 else "−"} {fz(abs(S0 - inflow / k))}e^(−{mono(k, 1, 't', first=True)})',
             '(i) 1 mark (ii) 1 mark (iii) 2 marks.', _ode=(lambda t, s: inflow - float(k) * s, lambda t: float(inflow / k) + float(S0 - inflow / k) * math.exp(-float(k) * t), 1.0))


# ======================================================================= table

FAMILIES = {
    S + '05-st1': [F('C1', 'D2', 'mcq', c5s1_mcq), F('C1', 'D1', 'mcq', c5s1_check), F('C2', 'D2', 'explain', c5s1_explain), F('C2', 'D3', 'mcq', c5s1_ar, kinds=('ar',)),
                   F('C2', 'D2', 'short', c5s1_check), F('C3', 'D2', 'numerical', c5s1_k_lin), F('C3', 'D3', 'numerical', c5s1_k_quot), F('C3', 'D4', 'multi_step', c5s1_two),
                   F('C4', 'D3', 'case', c5s1_case, gap='G7'), F('C4', 'D4', 'multi_step', c5s1_two), F('C3', 'D1', 'numerical', c5s1_k_lin)],
    S + '05-st2': [F('C1', 'D2', 'mcq', c5s2_mcq), F('C1', 'D1', 'short', c5s2_chain), F('C2', 'D2', 'explain', c5s2_value), F('C2', 'D3', 'mcq', c5s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c5s2_chain), F('C3', 'D3', 'multi_step', c5s2_diffab), F('C3', 'D4', 'long', c5s2_long), F('C4', 'D3', 'case', c5s2_case),
                   F('C4', 'D4', 'multi_step', c5s2_diffab), F('C4', 'D5', 'long', c5s2_long), F('C3', 'D1', 'numerical', c5s2_value)],
    S + '05-st3': [F('C1', 'D2', 'mcq', c5s3_mcq), F('C1', 'D1', 'short', c5s3_inv), F('C2', 'D2', 'numerical', c5s3_implicit2), F('C2', 'D3', 'mcq', c5s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c5s3_inv), F('C3', 'D3', 'multi_step', c5s3_implicit), F('C3', 'D4', 'numerical', c5s3_invsub), F('C4', 'D3', 'case', c5s3_case),
                   F('C4', 'D4', 'long', c5s3_long), F('C3', 'D1', 'numerical', c5s3_implicit)],
    S + '05-st4': [F('C1', 'D2', 'mcq', c5s4_mcq), F('C1', 'D1', 'short', c5s4_diff), F('C2', 'D2', 'numerical', c5s4_diff), F('C2', 'D3', 'mcq', c5s4_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c5s4_xx), F('C3', 'D3', 'multi_step', c5s4_prod), F('C4', 'D3', 'case', c5s4_case, gap='G7'), F('C4', 'D4', 'long', c5s4_long),
                   F('C3', 'D4', 'multi_step', c5s4_prod), F('C3', 'D1', 'numerical', c5s4_diff)],
    S + '05-st5': [F('C1', 'D2', 'mcq', c5s5_mcq), F('C1', 'D1', 'short', c5s5_d2), F('C2', 'D2', 'numerical', c5s5_param), F('C2', 'D3', 'mcq', c5s5_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c5s5_d2), F('C3', 'D3', 'multi_step', c5s5_second), F('C4', 'D3', 'case', c5s5_case, gap='G7'), F('C4', 'D4', 'long', c5s5_second),
                   F('C3', 'D1', 'numerical', c5s5_param), F('C3', 'D4', 'numerical', c5s5_param)],
    S + '06-st1': [F('C1', 'D2', 'mcq', c6s1_mcq), F('C1', 'D1', 'short', c6s1_circle), F('C2', 'D2', 'numerical', c6s1_marginal), F('C2', 'D3', 'mcq', c6s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c6s1_circle, gap='G7'), F('C3', 'D3', 'multi_step', c6s1_ladder, gap='G7'), F('C4', 'D3', 'case', c6s1_case, gap='G7'), F('C4', 'D4', 'long', c6s1_long, gap='G7'),
                   F('C3', 'D4', 'multi_step', c6s1_ladder, gap='G7'), F('C3', 'D1', 'numerical', c6s1_marginal)],
    S + '06-st2': [F('C1', 'D2', 'mcq', c6s2_mcq), F('C1', 'D1', 'short', c6s2_quad), F('C2', 'D2', 'explain', c6s2_explain), F('C2', 'D3', 'mcq', c6s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c6s2_quad), F('C3', 'D3', 'multi_step', c6s2_cubic), F('C3', 'D4', 'numerical', c6s2_least), F('C4', 'D3', 'case', c6s2_case, gap='G7'),
                   F('C4', 'D4', 'multi_step', c6s2_cubic), F('C3', 'D1', 'numerical', c6s2_least)],
    S + '06-st3': [F('C1', 'D2', 'mcq', c6s3_mcq), F('C1', 'D1', 'short', c6s3_misc), F('C2', 'D2', 'numerical', c6s3_misc), F('C2', 'D3', 'mcq', c6s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c6s3_misc), F('C3', 'D3', 'multi_step', c6s3_cubic), F('C4', 'D3', 'case', c6s3_case, gap='G7'), F('C4', 'D4', 'long', c6s3_long),
                   F('C3', 'D4', 'multi_step', c6s3_cubic), F('C3', 'D1', 'numerical', c6s3_misc)],
    S + '06-st4': [F('C1', 'D2', 'mcq', c6s4_mcq), F('C1', 'D1', 'short', c6s4_numbers), F('C2', 'D2', 'numerical', c6s4_fence, gap='G7'), F('C2', 'D3', 'mcq', c6s4_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c6s4_numbers), F('C3', 'D3', 'multi_step', c6s4_abs), F('C3', 'D4', 'long', c6s4_box, gap='G7'), F('C4', 'D3', 'case', c6s4_case, gap='G7'),
                   F('C4', 'D4', 'long', c6s4_box, gap='G7'), F('C4', 'D5', 'long', c6s4_proof), F('C3', 'D3', 'numerical', c6s4_profit, gap='G7'), F('C3', 'D1', 'numerical', c6s4_profit, gap='G7')],
    S + '07-st1': [F('C1', 'D2', 'mcq', c7s1_mcq), F('C1', 'D1', 'short', c7s1_poly), F('C2', 'D2', 'numerical', c7s1_std), F('C2', 'D3', 'mcq', c7s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c7s1_poly), F('C3', 'D3', 'multi_step', c7s1_ivp), F('C4', 'D3', 'case', c7s1_case, gap='G7'), F('C3', 'D4', 'multi_step', c7s1_ivp), F('C3', 'D1', 'numerical', c7s1_std)],
    S + '07-st2': [F('C1', 'D2', 'mcq', c7s2_mcq), F('C1', 'D1', 'short', c7s2_sub), F('C2', 'D2', 'numerical', c7s2_sub), F('C2', 'D3', 'mcq', c7s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c7s2_sub), F('C3', 'D3', 'numerical', c7s2_sub), F('C4', 'D3', 'case', c7s2_case), F('C4', 'D4', 'long', c7s2_long), F('C3', 'D4', 'long', c7s2_long), F('C3', 'D1', 'numerical', c7s2_sub)],
    S + '07-st3': [F('C1', 'D2', 'mcq', c7s3_mcq), F('C1', 'D1', 'short', c7s3_one), F('C2', 'D2', 'numerical', c7s3_one), F('C2', 'D3', 'mcq', c7s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c7s3_two), F('C3', 'D3', 'multi_step', c7s3_two), F('C4', 'D3', 'case', c7s3_case), F('C4', 'D4', 'long', c7s3_three), F('C3', 'D4', 'long', c7s3_three), F('C4', 'D5', 'long', c7s3_three),
                   F('C3', 'D1', 'numerical', c7s3_one)],
    S + '07-st4': [F('C1', 'D2', 'mcq', c7s4_mcq), F('C1', 'D1', 'short', c7s4_special), F('C2', 'D2', 'numerical', c7s4_exf), F('C2', 'D3', 'mcq', c7s4_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c7s4_parts), F('C3', 'D3', 'numerical', c7s4_special), F('C4', 'D3', 'case', c7s4_case), F('C3', 'D4', 'multi_step', c7s4_parts), F('C4', 'D4', 'multi_step', c7s4_exf),
                   F('C3', 'D1', 'numerical', c7s4_special)],
    S + '07-st5': [F('C1', 'D2', 'mcq', c7s5_mcq), F('C1', 'D1', 'short', c7s5_log), F('C2', 'D2', 'numerical', c7s5_poly), F('C2', 'D3', 'mcq', c7s5_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c7s5_poly), F('C3', 'D3', 'numerical', c7s5_mod), F('C3', 'D4', 'numerical', c7s5_prop), F('C4', 'D3', 'case', c7s5_case, gap='G7'),
                   F('C4', 'D4', 'long', c7s5_long), F('C4', 'D5', 'long', c7s5_long), F('C3', 'D1', 'numerical', c7s5_log), F('C3', 'D3', 'numerical', c7s5_prop)],
    S + '08-st1': [F('C1', 'D2', 'mcq', c8s1_mcq), F('C1', 'D1', 'short', c8s1_under), F('C2', 'D2', 'numerical', c8s1_conic), F('C2', 'D3', 'mcq', c8s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c8s1_under), F('C3', 'D3', 'multi_step', c8s1_parab), F('C3', 'D4', 'multi_step', c8s1_conic), F('C4', 'D3', 'case', c8s1_case, gap='G7'),
                   F('C4', 'D4', 'long', c8s1_parab), F('C3', 'D1', 'numerical', c8s1_conic), F('C4', 'D5', 'long', c8s2_chord)],
    S + '08-st2': [F('C1', 'D2', 'mcq', c8s2_mcq), F('C1', 'D1', 'short', c8s2_line_par), F('C2', 'D2', 'numerical', c8s2_line_par), F('C2', 'D3', 'mcq', c8s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c8s2_parline), F('C3', 'D3', 'multi_step', c8s2_parline), F('C3', 'D4', 'long', c8s2_chord), F('C4', 'D3', 'case', c8s2_case, gap='G7'),
                   F('C4', 'D4', 'long', c8s2_chord), F('C3', 'D1', 'numerical', c8s2_line_par)],
    S + '08-st3': [F('C1', 'D2', 'mcq', c8s3_mcq), F('C2', 'D2', 'numerical', c8s3_sym), F('C2', 'D3', 'mcq', c8s3_ar, kinds=('ar',)), F('C3', 'D1', 'numerical', c8s3_horiz),
                   F('C3', 'D2', 'numerical', c8s3_horiz), F('C3', 'D3', 'multi_step', c8s3_sym), F('C4', 'D3', 'case', c8s3_case), F('C4', 'D4', 'long', c8s3_sym), F('C1', 'D1', 'mcq', c8s3_mcq)],
    S + '09-st1': [F('C1', 'D2', 'mcq', c9s1_mcq), F('C1', 'D1', 'short', c9s1_od), F('C2', 'D2', 'numerical', c9s1_od), F('C2', 'D3', 'mcq', c9s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'short', c9s1_verify), F('C3', 'D3', 'numerical', c9s1_od), F('C4', 'D3', 'case', c9s1_case), F('C3', 'D4', 'explain', c9s1_verify), F('C4', 'D4', 'explain', c9s1_verify), F('C3', 'D1', 'short', c9s1_od)],
    S + '09-st2': [F('C1', 'D2', 'mcq', c9s2_mcq), F('C1', 'D1', 'short', c9s2_exp), F('C2', 'D2', 'numerical', c9s2_gen), F('C2', 'D3', 'mcq', c9s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c9s2_exp), F('C3', 'D3', 'multi_step', c9s2_power), F('C3', 'D4', 'multi_step', c9s2_growth, gap='G7'), F('C4', 'D3', 'case', c9s2_case, gap='G7'),
                   F('C4', 'D4', 'long', c9s2_long), F('C4', 'D5', 'long', c9s2_long), F('C3', 'D1', 'numerical', c9s2_gen), F('C3', 'D3', 'multi_step', c9s2_growth, gap='G7')],
    S + '09-st3': [F('C1', 'D2', 'mcq', c9s3_mcq), F('C1', 'D1', 'mcq', c9s3_pick), F('C2', 'D2', 'mcq', c9s3_pick), F('C2', 'D3', 'mcq', c9s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c9s3_solve), F('C3', 'D3', 'numerical', c9s3_solve), F('C4', 'D3', 'case', c9s3_case), F('C4', 'D4', 'long', c9s3_part), F('C3', 'D4', 'long', c9s3_part), F('C3', 'D1', 'numerical', c9s3_solve)],
    S + '09-st4': [F('C1', 'D2', 'mcq', c9s4_mcq), F('C1', 'D1', 'short', c9s4_if), F('C2', 'D2', 'numerical', c9s4_if), F('C2', 'D3', 'mcq', c9s4_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c9s4_exp), F('C3', 'D3', 'multi_step', c9s4_lin), F('C3', 'D4', 'multi_step', c9s4_xpow), F('C4', 'D3', 'case', c9s4_case, gap='G7'),
                   F('C4', 'D4', 'long', c9s4_ivp), F('C4', 'D5', 'long', c9s4_trig), F('C3', 'D1', 'numerical', c9s4_exp), F('C3', 'D3', 'numerical', c9s4_xpow)],
}
