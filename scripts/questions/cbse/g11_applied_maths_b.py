"""CBSE class 11 Applied Mathematics (241) families, chapters 5-9 (limits and continuity, differentiation,
permutations and combinations, probability, descriptive statistics). All answers are computed in code."""
from __future__ import annotations

import itertools
import math
from fractions import Fraction as Fr

from qbank import F, ar, mcq, num, sup, name, two_names, inr, CITIES, GIRLS  # noqa: F401
from g11_physics_util import pool_mcq, pool_ar, pool_txt, tf_mcq  # noqa: F401
from g11_applied_maths_a import Q, fs, poly, lin, mixed, nd, reuse, S, d1

# ======================================================== ch05 Limits and continuity
# st2 additions: standard limits and limits at infinity

c5s2_std = pool_mcq([
    ('lim(x→0) (eˣ − 1)/x equals', '1', ['0', 'e', 'does not exist'], 'Standard limit.'),
    ('lim(x→0) log(1 + x)/x equals', '1', ['0', 'e', 'log 2'], 'Standard limit (natural log).'),
    ('lim(x→0) (aˣ − 1)/x, a > 0, equals', 'log a', ['a', '1', 'a log a'], 'Standard limit: logₑ a.'),
    ('lim(x→0) (1 + x)^(1/x) equals', 'e', ['1', '0', '∞'], 'Standard limit defining e.'),
    ('lim(n→∞) (1 + 1/n)ⁿ equals', 'e', ['1', '2', '∞'], 'Standard limit defining e.'),
    ('lim(x→a) (xⁿ − aⁿ)/(x − a) equals', 'naⁿ⁻¹', ['aⁿ', 'naⁿ', 'n'], 'Standard limit.'),
])


def c5s2_ekx(r):
    a, b = r.choice([2, 3, 4, 5, 6, -2, -3]), r.choice([1, 2, 3, 4, 5, 6])
    kind = r.choice(['exp', 'log'])
    v = Fr(a, b)
    if kind == 'exp':
        e = f'(e^({a}x) − 1)/({b}x)' if b != 1 else f'(e^({a}x) − 1)/x'
        key = f'(e^({a}x) − 1)/({b}x) = ({a}/{b}) × (e^({a}x) − 1)/({a}x) → {fs(v)} × 1.'
    else:
        e = f'log(1 + {a}x)/({b}x)' if b != 1 else f'log(1 + {a}x)/x'
        key = f'log(1 + {a}x)/({b}x) = ({a}/{b}) × log(1 + {a}x)/({a}x) → {fs(v)} × 1.'
    return Q(f'Evaluate lim(x→0) {e}.', fs(v), key, [fs(Fr(b, a)), fs(Fr(a)), '1' if v != 1 else '0'])


def c5s2_ax(r):
    a, b = r.sample([2, 3, 5, 7, 4, 6], 2)
    return Q(f'Evaluate lim(x→0) ({a}ˣ − {b}ˣ)/x.', f'log ({a}/{b})', f'Write as ({a}ˣ − 1)/x − ({b}ˣ − 1)/x → log {a} − log {b} = log ({a}/{b}).',
             [f'log ({b}/{a})', f'log {a * b}', f'{a - b}'])


def c5s2_inf(r):
    a, d = r.choice([1, 2, 3, 4, 5, 6]), r.choice([1, 2, 3, 4, 5, 7])
    b, c, e = r.randint(-9, 9), r.randint(-9, 9), r.randint(1, 9)
    kind = r.choice(['same', 'lower', 'higher'])
    if kind == 'same':
        top, bot, v = poly([a, b, c]), poly([d, 0, e]), fs(Fr(a, d))
    elif kind == 'lower':
        top, bot, v = poly([a, b]), poly([d, 0, e]), '0'
    else:
        top, bot, v = poly([a, b, c]), poly([d, e]), '∞ (the limit does not exist as a finite number)'
    return Q(f'Evaluate lim(x→∞) ({top})/({bot}).', v, 'Divide numerator and denominator by the highest power of x in the denominator; terms like 1/x → 0.',
             nd(v, [fs(Fr(d, a)), '0' if v != '0' else fs(Fr(a, d)), '1', fs(Fr(c, e)) if e else '1']))


def c5s2_root(r):
    a = r.choice([1, 4, 9, 16, 25, 36, 49])
    s = int(a ** 0.5)
    return Q(f'Evaluate lim(x→{a}) (√x − {s})/(x − {a}) by rationalisation.', fs(Fr(1, 2 * s)),
             f'Multiply by (√x + {s}): (x − {a})/((x − {a})(√x + {s})) = 1/(√x + {s}) → 1/{2 * s}.', [fs(Fr(1, s)), str(2 * s), '0'])


def c5s2_ar(r):
    a = r.choice([2, 3, 4, 5])
    if r.random() < 0.5:
        return ar(f'lim(x→0) (e^({a}x) − 1)/x = {a}.', 'lim(y→0) (eʸ − 1)/y = 1.', 'a', f'Put y = {a}x: the limit is {a} × 1.')
    return ar(f'lim(x→0) (e^({a}x) − 1)/x = 1.', 'lim(y→0) (eʸ − 1)/y = 1.', 'd', f'A is false: the limit is {a}. R is true.')


# st3 continuity

def c5s3_check(r):
    a = r.randint(-3, 4)
    p, q = r.choice([1, 2, 3, -1]), r.randint(-5, 5)
    rr = r.choice([1, 2, -2, 3])
    cont = r.random() < 0.5
    s = p * a + q - rr * a if cont else p * a + q - rr * a + r.choice([1, 2, -1, 3])
    L, Rv = p * a + q, rr * a + s
    ans = 'continuous' if L == Rv else 'not continuous'
    return Q(f'Examine the continuity of f(x) = {lin(p, q)} for x < {a}, and f(x) = {lin(rr, s)} for x ≥ {a}, at x = {a}.', f'{ans} (LHL = {L}, RHL = f({a}) = {Rv})',
             f'LHL = {p}({a}) + {q} = {L}; RHL = f({a}) = {Rv}. {"Equal, so f is continuous" if L == Rv else "Unequal, so f is discontinuous"} at x = {a}.',
             [f'{"not continuous" if L == Rv else "continuous"} (LHL = {L}, RHL = f({a}) = {Rv})', f'{ans} (LHL = {Rv}, RHL = f({a}) = {L})' if L != Rv else f'not continuous (LHL = {L}, RHL = f({a}) = {Rv + 1})',
              f'continuous (LHL = {L + 1}, RHL = f({a}) = {L + 1})'])


def c5s3_k(r):
    a = r.choice([1, 2, 3, -1, -2])
    c = r.randint(-4, 6)
    k = Fr(a * a + c - 1, a)
    return Q(f'Find k so that f(x) = kx + 1 for x ≤ {a}, and f(x) = x² + {c} for x > {a}, is continuous at x = {a}.'.replace('+ -', '− '), f'k = {fs(k)}',
             f'f({a}) = {a}k + 1 must equal lim(x→{a}⁺) (x² + {c}) = {a * a + c}: {a}k = {a * a + c - 1} ⇒ k = {fs(k)}.',
             [f'k = {fs(k + 1)}', f'k = {fs(Fr(a * a + c, a))}', f'k = {fs(-k) if k else 1}'])


def c5s3_removable(r):
    a = r.choice([1, 2, 3, 4, 5, -2, -3])
    kind = r.choice(['sq', 'cube'])
    if kind == 'sq':
        v = 2 * a
        e = f'(x² − {a * a})/(x − {a})' if a > 0 else f'(x² − {a * a})/(x + {-a})'
    else:
        v = 3 * a * a
        e = f'(x³ − {a ** 3})/(x − {a})' if a > 0 else f'(x³ + {-a ** 3})/(x + {-a})'
    return Q(f'f(x) = {e} for x ≠ {a} and f({a}) = k. Find k so that f is continuous at x = {a}.', f'k = {v}',
             f'For x ≠ {a} the expression simplifies ({"x + " + str(a) if kind == "sq" else "x² + " + str(a) + "x + " + str(a * a)}); its limit at {a} is {v}, so k = {v}.'.replace('+ -', '− '),
             [f'k = {a}', f'k = {v + 1}', 'k = 0'])


def c5s3_count(r):
    p = Fr(r.randint(-7, 0), 2)
    q = Fr(r.randint(2, 9), 2)
    ints = [n for n in range(math.floor(p) - 1, math.ceil(q) + 2) if p < n < q]
    return Q(f'Find the number of points in the open interval ({num(float(p))}, {num(float(q))}) at which f(x) = [x], the greatest integer function, is discontinuous.', str(len(ints)),
             f'[x] jumps at every integer: {", ".join(map(str, ints))}, i.e. {len(ints)} points.', [str(len(ints) + 1), str(len(ints) - 1), '0'])


def c5s3_two(r):
    p, q = r.choice([(1, 3), (2, 4), (-1, 2), (0, 3), (1, 4), (2, 5)])
    a = r.choice([2, 3, 4, -2, 5])
    b = r.randint(-5, 5)
    c1, c2 = a * p + b, a * q + b
    return Q(f'Find a and b if f(x) = {c1} for x ≤ {p}; f(x) = ax + b for {p} < x < {q}; f(x) = {c2} for x ≥ {q} is continuous everywhere.',
             f'a = {a}, b = {b}', f'Continuity at {p}: {lin(p, 0, "a")} + b = {c1}; at {q}: {lin(q, 0, "a")} + b = {c2} (2). Subtract: {q - p}a = {c2 - c1} ⇒ a = {a}, b = {b} (2). Linear pieces are continuous elsewhere (1).',
             [f'a = {b}, b = {a}', f'a = {-a}, b = {b}', f'a = {a}, b = {-b if b else 1}'])


c5s3_def = pool_mcq([
    ('A function f is continuous at x = a if', 'lim(x→a) f(x) exists and equals f(a)', ['f(a) is defined', 'lim(x→a) f(x) exists', 'f is differentiable at a'], 'All three conditions: defined, limit exists, equal.'),
    ('The greatest integer function [x] is discontinuous at', 'every integer', ['every real number', 'x = 0 only', 'no point'], 'It jumps by 1 at each integer.'),
    ('f(x) = |x| at x = 0 is', 'continuous', ['discontinuous', 'not defined', 'continuous only from the right'], 'LHL = RHL = f(0) = 0.'),
    ('A polynomial function is', 'continuous at every real number', ['continuous only at integers', 'discontinuous at x = 0', 'continuous only for x > 0'], 'Polynomials are continuous on R.'),
    ('f(x) = 1/(x − 3) is discontinuous at', 'x = 3', ['x = 0', 'x = −3', 'no point'], 'Not defined at x = 3.'),
])

c5s3_tf = tf_mcq('continuity', [
    'The sum of two continuous functions is continuous.', 'Every polynomial function is continuous on R.', 'A rational function is continuous wherever its denominator is non-zero.',
    'eˣ is continuous for every real x.', 'log x is continuous on (0, ∞).'],
    ['[x] is continuous at every integer.', 'If lim(x→a) f(x) exists, f must be continuous at a.', '1/x is continuous at x = 0.',
     'A function defined by two formulas can never be continuous.', 'A continuous function must be a polynomial.'])


def c5s3_explain(r):
    a = r.randint(1, 6)
    return {'stem': f'Explain why f(x) = |x − {a}| is continuous at x = {a}, using left-hand and right-hand limits.',
            'answer': f'LHL = lim(x→{a}⁻) ({a} − x) = 0; RHL = lim(x→{a}⁺) (x − {a}) = 0; f({a}) = 0. All equal, so f is continuous at {a}.',
            'key': 'LHL (½), RHL (½), f(a) (½), conclusion (½).'}


def c5s3_ar(r):
    a = r.randint(1, 5)
    if r.random() < 0.5:
        return ar(f'f(x) = (x² − {a * a})/(x − {a}) is discontinuous at x = {a}.', 'A function is continuous at a point only if it is defined there.', 'a', f'f({a}) is not defined, so R explains A.')
    return ar(f'f(x) = [x] is continuous at x = {a}.', 'The left-hand and right-hand limits of [x] at an integer are different.', 'd', f'A is false: LHL = {a - 1}, RHL = {a}. R is true.')


def c5s3_case(r):
    base, rate = r.choice([(40, 20), (30, 15), (50, 25), (20, 10)])
    h0 = r.choice([2, 3])
    jump = r.choice([0, 10, 20])
    return {'stem': (f'A mall parking in {r.choice(CITIES)} charges P(t) = {base} rupees for 0 < t ≤ {h0} hours and P(t) = {base + jump} + {rate}(t − {h0}) rupees for t > {h0} (t in hours, charged continuously).\n'
                     f'(i) Find P({h0}) and lim(t→{h0}⁺) P(t). (2)\n(ii) Is P continuous at t = {h0}? (1)\n(iii) Find the charge for {h0 + 2} hours. (1)'),
            'answer': f'(i) {base}; {base + jump} (ii) {"Yes" if jump == 0 else "No – there is a jump of ₹" + str(jump)} (iii) ₹{base + jump + 2 * rate}',
            'key': f'(i) value (1), right-hand limit (1). (ii) compare (1). (iii) {base + jump} + {rate} × 2 (1).'}


# ======================================================== ch06 Differentiation
# st1 additions

def c6s1_avg(r):
    a, b, c = r.randint(1, 4), r.randint(-6, 6), r.randint(0, 9)
    x1, x2 = sorted(r.sample(range(0, 8), 2))
    f = lambda x: a * x * x + b * x + c
    avg = Fr(f(x2) - f(x1), x2 - x1)
    return Q(f'For f(x) = {poly([a, b, c])}, find the average rate of change of f from x = {x1} to x = {x2}, and the instantaneous rate of change at x = {x1}.',
             f'{fs(avg)}; {2 * a * x1 + b}', f'Average = [f({x2}) − f({x1})]/({x2} − {x1}) = ({f(x2)} − {f(x1)})/{x2 - x1} = {fs(avg)}; f′(x) = {lin(2 * a, b)}, f′({x1}) = {2 * a * x1 + b}.',
             [f'{fs(avg)}; {2 * a * x2 + b}', f'{2 * a * x1 + b}; {fs(avg)}', f'{f(x2) - f(x1)}; {2 * a * x1 + b}'])


def c6s1_mc(r):
    a, b, c = r.choice([1, 2, 3]), r.choice([10, 20, 30, 40]), r.choice([500, 1000, 2000])
    x = r.choice([10, 15, 20, 25, 30])
    return Q(f'The total cost (₹) of producing x units is C(x) = {a}x² + {b}x + {c}. Find the marginal cost when {x} units are produced.', f'₹{2 * a * x + b}',
             f'MC = dC/dx = {2 * a}x + {b}; at x = {x}: ₹{2 * a * x + b}.', [f'₹{a * x * x + b * x + c}', f'₹{a * x + b}', f'₹{2 * a * x}'])


# st2 additions: chain rule and rules with polynomials

def c6s2_chain(r):
    a, b = r.choice([2, 3, 4, 5, -2]), r.randint(-6, 6)
    n = r.randint(2, 7)
    x0 = r.choice([0, 1, -1, 2])
    v = n * a * (a * x0 + b) ** (n - 1)
    return Q(f'Differentiate y = ({lin(a, b)}){sup(n)} with respect to x and find dy/dx at x = {x0}.', f'dy/dx = {n * a}({lin(a, b)}){sup(n - 1) if n > 2 else ""}; {v}',
             f'Chain rule: n(ax + b)ⁿ⁻¹ × a = {n}({lin(a, b)}){sup(n - 1) if n > 2 else ""} × {a} (1); at x = {x0}: {v} (1).',
             [f'dy/dx = {n}({lin(a, b)}){sup(n - 1) if n > 2 else ""}; {n * (a * x0 + b) ** (n - 1)}', f'dy/dx = {n * a}({lin(a, b)}){sup(n - 1) if n > 2 else ""}; {v + n * a}',
              f'dy/dx = {a}({lin(a, b)}){sup(n - 1) if n > 2 else ""}; {a * (a * x0 + b) ** (n - 1)}'])


def c6s2_root(r):
    a, b = r.choice([1, 2, 3, 4]), r.randint(1, 9)
    x0 = r.choice([x for x in range(0, 13) if int((a * x + b) ** 0.5) ** 2 == a * x + b] or [None])
    if x0 is None:
        raise ValueError
    s = int((a * x0 + b) ** 0.5)
    v = Fr(a, 2 * s)
    return Q(f'If y = √({lin(a, b)}), find dy/dx at x = {x0}.', fs(v), f'dy/dx = {a}/(2√({lin(a, b)})) (chain rule); at x = {x0}: {a}/(2 × {s}) = {fs(v)}.',
             [fs(Fr(1, 2 * s)), fs(Fr(a, s)), fs(Fr(2 * s, a))])


def c6s2_prodval(r):
    a, b, c, d = r.randint(1, 4), r.randint(-5, 5), r.randint(1, 3), r.randint(-5, 5)
    x0 = r.randint(-2, 3)
    u, v_ = a * x0 * x0 + b, c * x0 + d
    du, dv = 2 * a * x0, c
    val = du * v_ + u * dv
    return Q(f'Using the product rule, find the derivative of y = ({poly([a, 0, b])})({lin(c, d)}) at x = {x0}.', str(val),
             f'y′ = (2{"" if a == 1 else a}x)·({lin(c, d)}) + ({poly([a, 0, b])})·{c}'.replace('(21x)', '(2x)').replace('2x)', 'x)' if False else '2x)') + f'; at x = {x0}: {du}×{v_} + {u}×{dv} = {val}.',
             [str(du * dv), str(val + 1), str(du * v_)])


def c6s2_quotval(r):
    a, b, c, d = r.randint(1, 5), r.randint(-6, 6), r.randint(1, 4), r.randint(1, 6)
    x0 = r.randint(0, 3)
    den = c * x0 + d
    if den == 0 or a * d - b * c == 0:
        raise ValueError
    v = Fr(a * d - b * c, den * den)
    return Q(f'Differentiate y = ({lin(a, b)})/({lin(c, d)}) and find dy/dx at x = {x0}.', f'dy/dx = {a * d - b * c}/({lin(c, d)})²; {fs(v)}',
             f'Quotient rule: [{a}({lin(c, d)}) − {c}({lin(a, b)})]/({lin(c, d)})² = {a * d - b * c}/({lin(c, d)})² (2); at x = {x0}: {fs(v)} (1).',
             [f'dy/dx = {b * c - a * d}/({lin(c, d)})²; {fs(-v)}', f'dy/dx = {a}/{c}; {fs(Fr(a, c))}', f'dy/dx = {a * d - b * c}/({lin(c, d)}); {fs(Fr(a * d - b * c, den))}'])


def c6s2_ar(r):
    a, n = r.choice([2, 3, 5]), r.randint(2, 6)
    if r.random() < 0.5:
        return ar(f'd/dx ({a}x + 1){sup(n)} = {n * a}({a}x + 1){sup(n - 1) if n > 2 else ""}.', 'd/dx [f(g(x))] = f′(g(x)) · g′(x).', 'a', 'Chain rule gives the extra factor a.')
    return ar(f'd/dx ({a}x + 1){sup(n)} = {n}({a}x + 1){sup(n - 1) if n > 2 else ""}.', 'd/dx [f(g(x))] = f′(g(x)) · g′(x).', 'd', f'A is false: the factor {a} from the inner function is missing. R is true.')


c6s2_rules = pool_mcq([
    ('d/dx (uv) equals', 'u dv/dx + v du/dx', ['du/dx · dv/dx', 'u dv/dx − v du/dx', '(du/dx)/(dv/dx)'], 'Product rule.'),
    ('d/dx (u/v) equals', '(v du/dx − u dv/dx)/v²', ['(u dv/dx − v du/dx)/v²', '(du/dx)/(dv/dx)', '(v du/dx + u dv/dx)/v²'], 'Quotient rule.'),
    ('If y = f(u) and u = g(x), then dy/dx equals', '(dy/du)(du/dx)', ['(dy/du) + (du/dx)', '(dy/du)/(du/dx)', 'dy/du'], 'Chain rule.'),
    ('d/dx (xⁿ) equals', 'nxⁿ⁻¹', ['xⁿ⁻¹', 'nxⁿ', '(n − 1)xⁿ'], 'Power rule.'),
    ('The derivative of a constant is', '0', ['1', 'the constant itself', 'not defined'], 'A constant does not change.'),
])

# st3 exponential, logarithmic, implicit and parametric

c6s3_basic = pool_mcq([
    ('d/dx (eˣ) equals', 'eˣ', ['xeˣ⁻¹', 'eˣ⁻¹', 'e'], 'Standard derivative.'),
    ('d/dx (log x) equals (x > 0)', '1/x', ['log x', 'x', 'e/x'], 'Standard derivative.'),
    ('d/dx (aˣ) equals (a > 0)', 'aˣ log a', ['xaˣ⁻¹', 'aˣ', 'aˣ/log a'], 'Standard derivative.'),
    ('d/dx (e^(kx)) equals', 'ke^(kx)', ['e^(kx)', 'kxe^(kx − 1)', 'e^(kx)/k'], 'Chain rule.'),
    ('d/dx (log 5x) equals', '1/x', ['5/x', '1/(5x)', '5 log x'], 'log 5x = log 5 + log x.'),
    ('If x = at², y = 2at, then dy/dx equals', '1/t', ['t', '2t', '1/(2t)'], '(dy/dt)/(dx/dt) = 2a/(2at).'),
])


def c6s3_exp(r):
    p, k = r.choice([1, 2, 3, 4, 5]), r.choice([2, 3, -1, -2, 4])
    q = r.choice([2, 3, 5, 6, 7])
    kind = r.choice(['ek_log', 'ek_pow'])
    if kind == 'ek_log':
        y = f'{p if p != 1 else ""}e^({k}x) + {q} log x'
        d = f'{p * k}e^({k}x) + {q}/x'
    else:
        y = f'{p if p != 1 else ""}e^({k}x) + x{sup(q)}'
        d = f'{p * k}e^({k}x) + {q}x{sup(q - 1) if q > 2 else ""}'
    return Q(f'Differentiate y = {y} with respect to x.', f'dy/dx = {d}'.replace('+ -', '− '), f'Use d/dx e^(kx) = ke^(kx) and the standard rules term by term: {d}.'.replace('+ -', '− '),
             [f'dy/dx = {p}e^({k}x) + {q}/x', f'dy/dx = {p * k}e^({k - 1}x) + {q}/x', f'dy/dx = {p * k}e^({k}x) + {q}'])


def c6s3_xne(r):
    n = r.randint(2, 6)
    return Q(f'Differentiate y = x{sup(n)}eˣ.', f'dy/dx = xⁿ⁻¹eˣ(x + {n}) = x{sup(n - 1) if n > 2 else ""}eˣ(x + {n})',
             f'Product rule: x{sup(n)}eˣ + {n}x{sup(n - 1) if n > 2 else ""}eˣ = x{sup(n - 1) if n > 2 else ""}eˣ(x + {n}).',
             [f'dy/dx = {n}x{sup(n - 1) if n > 2 else ""}eˣ', f'dy/dx = x{sup(n)}eˣ', f'dy/dx = x{sup(n - 1) if n > 2 else ""}eˣ(x − {n})'])


def c6s3_log(r):
    a, b = r.randint(1, 5), r.randint(1, 9)
    x0 = r.randint(1, 3)
    v = Fr(2 * a * x0, a * x0 * x0 + b)
    return Q(f'If y = log ({poly([a, 0, b])}), find dy/dx at x = {x0}.', fs(v), f'dy/dx = {2 * a}x/({poly([a, 0, b])}) (chain rule) = {2 * a * x0}/{a * x0 * x0 + b} = {fs(v)}.',
             [fs(Fr(1, a * x0 * x0 + b)), fs(Fr(2 * a * x0)), fs(Fr(a * x0 * x0 + b, 2 * a * x0))])


TRIPLES = [(3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17), (9, 12, 15), (7, 24, 25)]


def c6s3_implicit(r):
    if r.random() < 0.5:
        a, b, c = r.choice(TRIPLES)
        x0, y0 = r.choice([(a, b), (b, a), (-a, b), (a, -b)])
        v = Fr(-x0, y0)
        return Q(f'Find dy/dx for the curve x² + y² = {c * c} at the point ({x0}, {y0}).', fs(v), f'2x + 2y dy/dx = 0 ⇒ dy/dx = −x/y = {fs(v)}.', [fs(-v), fs(Fr(y0, x0)), fs(Fr(-y0, x0))])
    x0, y0 = r.choice([(2, 3), (3, 4), (1, 6), (4, 5), (2, 7), (6, 2)])
    v = Fr(-y0, x0)
    return Q(f'Find dy/dx for the curve xy = {x0 * y0} at the point ({x0}, {y0}).', fs(v), f'x dy/dx + y = 0 ⇒ dy/dx = −y/x = {fs(v)}.', [fs(-v), fs(Fr(-x0, y0)), fs(Fr(x0, y0))])


def c6s3_implicit2(r):
    x0, y0 = r.randint(-3, 3), r.randint(1, 4)
    k = x0 * x0 + x0 * y0 + y0 * y0
    den = x0 + 2 * y0
    if den == 0:
        raise ValueError
    v = Fr(-(2 * x0 + y0), den)
    return Q(f'The point ({x0}, {y0}) lies on the curve x² + xy + y² = {k}. Find dy/dx at this point.', fs(v),
             f'2x + (x dy/dx + y) + 2y dy/dx = 0 ⇒ dy/dx = −(2x + y)/(x + 2y) (2); at ({x0}, {y0}): {fs(v)} (1).', [fs(-v), fs(Fr(-(x0 + 2 * y0), 2 * x0 + y0)) if 2 * x0 + y0 else '0', fs(v + 1)])


def c6s3_param(r):
    kind = r.choice(['at2', 'poly'])
    if kind == 'at2':
        a, t = r.randint(1, 6), r.choice([1, 2, 3, -1, -2, Fr(1, 2)])
        return Q(f'If x = {a}t² and y = {2 * a}t, find dy/dx at t = {fs(t)}.', fs(1 / Fr(t)), f'dx/dt = {2 * a}t, dy/dt = {2 * a}; dy/dx = 1/t = {fs(1 / Fr(t))}.',
                 [fs(Fr(t)), fs(2 * Fr(t)), fs(1 / (2 * Fr(t)))])
    p, q = r.randint(1, 3), r.randint(1, 4)
    t = r.choice([1, 2, -1, 3])
    dx, dy = 2 * p * t + q, 3 * t * t
    if dx == 0:
        raise ValueError
    v = Fr(dy, dx)
    return Q(f'If x = {poly([p, q, 0], "t")} and y = t³, find dy/dx at t = {t}.', fs(v), f'dx/dt = {lin(2 * p, q, "t")} = {dx}, dy/dt = 3t² = {dy} at t = {t}; dy/dx = {fs(v)}.',
             [fs(1 / v), fs(Fr(dy)), fs(v + 1)])


def c6s3_xx(r):
    x0 = r.choice([1, 2, 3])
    v = x0 ** x0
    ans = '1' if x0 == 1 else f'{v}(1 + log {x0})'
    return Q(f'Using logarithmic differentiation, find dy/dx for y = xˣ (x > 0), and its value at x = {x0}.', f'dy/dx = xˣ(1 + log x); {ans}',
             f'log y = x log x (1); (1/y) dy/dx = log x + 1 (2); dy/dx = xˣ(1 + log x) (1); at x = {x0}: {ans} (1).',
             [f'dy/dx = x·xˣ⁻¹; {x0 * x0 ** (x0 - 1)}', f'dy/dx = xˣ log x; {"0" if x0 == 1 else f"{v} log {x0}"}', f'dy/dx = xˣ; {v}'])


def c6s3_explain(r):
    a = r.choice([2, 3, 4])
    return {'stem': f'Explain when logarithmic differentiation is useful, and use it to differentiate y = {a}ˣ.',
            'answer': f'Useful when the variable is in the exponent or for products/quotients of many factors. log y = x log {a} ⇒ dy/dx = {a}ˣ log {a}.',
            'key': 'When to use (1); working and answer (1).'}


def c6s3_ar(r):
    a = r.choice([2, 3, 5, 10])
    if r.random() < 0.5:
        return ar(f'd/dx ({a}ˣ) = {a}ˣ log {a}.', f'{a}ˣ = e^(x log {a}).', 'a', f'Differentiate e^(x log {a}) by the chain rule; R explains A.')
    return ar(f'd/dx ({a}ˣ) = x·{a}ˣ⁻¹.', f'{a}ˣ = e^(x log {a}).', 'd', f'A is false: the power rule does not apply to a variable exponent; d/dx {a}ˣ = {a}ˣ log {a}. R is true.')


def c6s3_case(r):
    P0 = r.choice([1000, 2000, 5000])
    k = r.choice([Fr(1, 10), Fr(1, 20), Fr(1, 5)])
    t = r.choice([5, 10, 20])
    return {'stem': (f'The number of users of a new app in {r.choice(CITIES)} is modelled by N(t) = {P0}e^({fs(k)}t), where t is in weeks.\n'
                     f'(i) Find N(0). (1)\n(ii) Find dN/dt. (1)\n(iii) Show that dN/dt = {fs(k)} N and find the growth rate when t = {t}, leaving the answer in terms of e. (2)'),
            'answer': f'(i) {P0} (ii) {fs(P0 * k)}e^({fs(k)}t) (iii) dN/dt = {fs(k)} × {P0}e^({fs(k)}t) = {fs(k)}N; at t = {t}: {fs(P0 * k)}e^{fs(k * t)} users per week',
            'key': '(i) e⁰ = 1 (1). (ii) chain rule (1). (iii) relation (1), value (1).'}


# st4 second-order derivatives

def c6s4_poly(r):
    cs = [r.randint(1, 4), r.randint(-6, 6), r.randint(-9, 9), r.randint(-9, 9)]
    x0 = r.randint(-2, 3)
    v = 6 * cs[0] * x0 + 2 * cs[1]
    return Q(f'If y = {poly(cs)}, find d²y/dx² at x = {x0}.', str(v), f'dy/dx = {poly([3 * cs[0], 2 * cs[1], cs[2]])}; d²y/dx² = {lin(6 * cs[0], 2 * cs[1])} = {v} at x = {x0}.',
             [str(3 * cs[0] * x0 * x0 + 2 * cs[1] * x0 + cs[2]), str(v + 2 * cs[1] if cs[1] else v + 1), str(6 * cs[0] * x0)])


def c6s4_log(r):
    kind = r.choice(['log', 'xlog', 'ex'])
    x0 = r.randint(1, 5)
    if kind == 'log':
        return Q(f'If y = log x, find d²y/dx² at x = {x0}.', fs(Fr(-1, x0 * x0)), f'y′ = 1/x, y″ = −1/x² = {fs(Fr(-1, x0 * x0))}.', [fs(Fr(1, x0 * x0)), fs(Fr(1, x0)), fs(Fr(-1, x0))])
    if kind == 'xlog':
        return Q(f'If y = x log x, find d²y/dx² at x = {x0}.', fs(Fr(1, x0)), f'y′ = log x + 1, y″ = 1/x = {fs(Fr(1, x0))}.', [fs(Fr(-1, x0 * x0)), fs(Fr(x0)), '0' if x0 != 1 else '2'])
    k = r.choice([2, 3, -1, -2])
    return Q(f'If y = xe^({k}x), find d²y/dx².', f'e^({k}x)({k * k}x + {2 * k})'.replace('+ -', '− '), f'y′ = e^({k}x)(1 + {k}x); y″ = {k}e^({k}x)(1 + {k}x) + {k}e^({k}x) = e^({k}x)({k * k}x + {2 * k}).'.replace('+ -', '− '),
             [f'e^({k}x)({k}x + 1)'.replace('+ -', '− '), f'{k * k}xe^({k}x)', f'e^({k}x)({k * k}x + {k})'.replace('+ -', '− ')])


def c6s4_ode(r):
    p, q = r.sample([1, 2, 3, -1, -2, 4], 2)
    A, B = r.randint(1, 5), r.randint(1, 5)
    return {'stem': f'If y = {A}e^({p}x) + {B}e^({q}x), prove that d²y/dx² − ({p + q}) dy/dx + ({p * q})y = 0.',
            'answer': f'y′ = {A * p}e^({p}x) + {B * q}e^({q}x); y″ = {A * p * p}e^({p}x) + {B * q * q}e^({q}x). Then y″ − ({p + q})y′ + ({p * q})y: coefficient of e^({p}x) is {A}({p * p} − {(p + q) * p} + {p * q}) = 0 and of e^({q}x) is {B}({q * q} − {(p + q) * q} + {p * q}) = 0.',
            'key': 'y′ (1); y″ (1); substitution (2); simplification to 0 (1).'}


def c6s4_acc(r):
    a, b, c = r.randint(1, 3), r.randint(-9, 9), r.randint(1, 20)
    t = r.randint(1, 6)
    return {'stem': f'The distance (in m) moved by a particle in t seconds is s = {poly([a, b, c, 0], "t")}. Explain what d²s/dt² represents and find it at t = {t} s.',
            'answer': f'Acceleration; d²s/dt² = {lin(6 * a, 2 * b, "t")} = {6 * a * t + 2 * b} m/s² at t = {t}.', 'key': 'Meaning (rate of change of velocity) (1); value (1).'}


def c6s4_ar(r):
    k = r.choice([2, 3, 4, 5])
    if r.random() < 0.5:
        return ar(f'If y = e^({k}x), then d²y/dx² = {k * k}y.', f'Each differentiation of e^({k}x) multiplies it by {k}.', 'a', f'y″ = {k * k}e^({k}x) = {k * k}y; R explains A.')
    return ar(f'If y = x{sup(k)}, then d²y/dx² = {k}x{sup(k - 1)}.', 'd²y/dx² is the derivative of dy/dx.', 'd', f'A is false: d²y/dx² = {k * (k - 1)}x{sup(k - 2) if k > 3 else ""}{"" if k > 2 else ""}. R is true.')


c6s4_mcq = pool_mcq([
    ('If y = x³, then d²y/dx² equals', '6x', ['3x²', '6', 'x'], 'y′ = 3x², y″ = 6x.'),
    ('If y = eˣ, then d²y/dx² equals', 'eˣ', ['0', 'xeˣ', '2eˣ'], 'eˣ is its own derivative.'),
    ('If y = ax + b, then d²y/dx² equals', '0', ['a', 'b', '1'], 'y′ = a is constant.'),
    ('If s(t) gives position, then d²s/dt² gives', 'acceleration', ['velocity', 'distance', 'jerk'], 'Second derivative of position.'),
    ('If y = log x, then d²y/dx² equals', '−1/x²', ['1/x', '1/x²', '−1/x'], 'y′ = 1/x.'),
])

# ======================================================== ch07 Permutations and combinations (circular and repetition)


def c7s2_circ(r):
    n = r.randint(4, 10)
    who = r.choice(['friends', 'delegates', 'family members', 'students'])
    return Q(f'In how many ways can {n} {who} be seated around a round table?', f'{math.factorial(n - 1):,}'.replace(',', ''),
             f'Fix one person to remove rotations: ({n} − 1)! = {math.factorial(n - 1)}.', [str(math.factorial(n)), str(math.factorial(n - 1) // 2), str(math.factorial(n - 2))])


def c7s2_neck(r):
    n = r.randint(5, 10)
    v = math.factorial(n - 1) // 2
    return Q(f'In how many ways can {n} different beads be arranged to form a necklace?', str(v),
             f'Circular arrangements ({n} − 1)! = {math.factorial(n - 1)}; clockwise and anticlockwise give the same necklace, so divide by 2: {v}.',
             [str(math.factorial(n - 1)), str(math.factorial(n)), str(math.factorial(n) // 2)])


def c7s2_together(r):
    n = r.randint(5, 9)
    A, B = two_names(r)
    tog = 2 * math.factorial(n - 2)
    never = math.factorial(n - 1) - tog
    if r.random() < 0.5:
        return Q(f'{n} people, including {A} and {B}, sit around a round table. In how many arrangements do {A} and {B} sit together?', str(tog),
                 f'Treat {A} and {B} as one unit: {n - 1} units round a table in ({n - 2})! ways; the pair can swap: 2 × {math.factorial(n - 2)} = {tog}.',
                 [str(math.factorial(n - 2)), str(2 * math.factorial(n - 1)), str(never)])
    return Q(f'{n} people, including {A} and {B}, sit around a round table. In how many arrangements do {A} and {B} NOT sit next to each other?', str(never),
             f'Total ({n} − 1)! = {math.factorial(n - 1)}; together 2 × ({n - 2})! = {tog}; not together = {never}.', [str(tog), str(math.factorial(n - 1)), str(math.factorial(n) - tog)])


def c7s2_rep(r):
    k, n = r.choice([(10, 4), (10, 3), (26, 2), (5, 4), (6, 3), (4, 5), (3, 6), (2, 8)])
    what = {10: 'digits 0–9', 26: 'English letters', 5: 'the digits 1, 2, 3, 4, 5', 6: 'the digits 1 to 6', 4: 'the letters A, B, C, D', 3: 'the symbols ★, ●, ■', 2: 'the bits 0 and 1'}[k]
    return Q(f'How many {n}-character codes can be formed from {what} if repetition is allowed?', str(k ** n), f'Each of the {n} places can be filled in {k} ways: {k}{sup(n)} = {k ** n}.',
             [str(math.perm(k, n)), str(n ** k), str(k * n)])


def c7s2_ar(r):
    n = r.randint(4, 8)
    if r.random() < 0.5:
        return ar(f'{n} people can sit around a round table in {math.factorial(n - 1)} ways.', 'Arrangements that differ only by a rotation are the same in a circle.', 'a', f'({n} − 1)! = {math.factorial(n - 1)}; R explains the division by {n}.')
    return ar(f'{n} people can sit around a round table in {math.factorial(n)} ways.', 'Arrangements that differ only by a rotation are the same in a circle.', 'd', f'A is false: the number is ({n} − 1)! = {math.factorial(n - 1)}. R is true.')


c7s2_mcq = pool_mcq([
    ('The number of circular arrangements of n distinct objects is', '(n − 1)!', ['n!', 'n!/2', '(n − 2)!'], 'Fix one object.'),
    ('The number of ways to make a garland of n different flowers is', '(n − 1)!/2', ['(n − 1)!', 'n!/2', 'n!'], 'Clockwise and anticlockwise are the same.'),
    ('The number of r-letter words from n letters with repetition allowed is', 'nʳ', ['ⁿPᵣ', 'rⁿ', 'ⁿCᵣ'], 'n choices for each place.'),
])

# ======================================================== ch08 Probability: conditional, independence, Bayes


def c8s3_basic(r):
    n = r.choice([10, 12, 20, 24, 30, 40])
    b = r.randint(3, n - 3)
    ab = r.randint(1, b - 1)
    a = r.randint(ab + 1, n - (b - ab))
    PA, PB, PAB = Fr(a, n), Fr(b, n), Fr(ab, n)
    which = r.choice(['A|B', 'B|A'])
    v = PAB / PB if which == 'A|B' else PAB / PA
    return Q(f'If P(A) = {fs(PA)}, P(B) = {fs(PB)} and P(A ∩ B) = {fs(PAB)}, find P({which}).', fs(v),
             f'P({which}) = P(A ∩ B)/P({which[2]}) = {fs(PAB)}/{fs(PB if which == "A|B" else PA)} = {fs(v)}.',
             [fs(PAB / PA if which == 'A|B' else PAB / PB), fs(PAB), fs(PA * PB)])


def c8s3_dice(r):
    k = r.randint(1, 6)
    s = r.randint(6, 10)
    out = [(i, j) for i in range(1, 7) for j in range(1, 7)]
    cond = [o for o in out if o[0] == k]
    good = [o for o in cond if sum(o) >= s]
    v = Fr(len(good), len(cond))
    return Q(f'Two fair dice are thrown. Find the probability that the sum is at least {s}, given that the first die shows {k}.', fs(v),
             f'Given first = {k}: 6 equally likely outcomes; second die must be ≥ {s - k}: {len(good)} outcomes. P = {len(good)}/6 = {fs(v)}.',
             nd(fs(v), [fs(Fr(len([o for o in out if sum(o) >= s]), 36)), fs(Fr(len(good), 36)), fs(v + Fr(1, 6)) if v < 1 else '1/2', fs(Fr(1, 6))]))


def c8s3_indep(r):
    PA, PB = Fr(r.randint(1, 9), 10), Fr(r.randint(1, 9), 10)
    which = r.choice(['and', 'or', 'neither'])
    if which == 'and':
        v, t = PA * PB, 'P(A ∩ B)'
    elif which == 'or':
        v, t = PA + PB - PA * PB, 'P(A ∪ B)'
    else:
        v, t = (1 - PA) * (1 - PB), 'P(neither A nor B)'
    return Q(f'A and B are independent events with P(A) = {num(float(PA))} and P(B) = {num(float(PB))}. Find {t}.', num(float(v), 3),
             f'Independence: P(A ∩ B) = P(A)P(B) = {num(float(PA * PB), 3)}. {t} = {num(float(v), 3)}.',
             nd(num(float(v), 3), [num(float(PA + PB), 3), num(float(PA * PB), 3), num(float(1 - PA * PB), 3), num(float(PA + PB - PA * PB), 3), num(float(1 - PA - PB + 2 * PA * PB), 3)]))


def c8s3_check(r):
    PA, PB = Fr(r.randint(1, 9), 10), Fr(r.randint(1, 9), 10)
    ind = r.random() < 0.5
    PAB = PA * PB if ind else PA * PB + Fr(r.choice([1, 2, -1]), 100)
    if PAB <= 0 or PAB > min(PA, PB):
        raise ValueError
    return Q(f'Given P(A) = {num(float(PA))}, P(B) = {num(float(PB))} and P(A ∩ B) = {num(float(PAB), 3)}, are A and B independent?',
             'Yes, independent' if ind else 'No, not independent', f'P(A)P(B) = {num(float(PA * PB), 3)} {"=" if ind else "≠"} P(A ∩ B) = {num(float(PAB), 3)}.',
             ['No, not independent' if ind else 'Yes, independent', 'Yes, they are mutually exclusive', 'Cannot be decided'])


RANKS = {'aces': 4, 'kings': 4, 'queens': 4, 'hearts': 13, 'spades': 13, 'red cards': 26, 'face cards': 12, 'black cards': 26}


def c8s3_cards(r):
    t = r.choice(list(RANKS))
    k = RANKS[t]
    v = Fr(k, 52) * Fr(k - 1, 51)
    return Q(f'Two cards are drawn one after the other without replacement from a well-shuffled pack of 52 cards. Find the probability that both are {t}.', fs(v),
             f'Multiplication theorem: P = ({k}/52) × ({k - 1}/51) = {fs(v)}.', [fs(Fr(k, 52) ** 2), fs(Fr(k, 52) * Fr(k - 1, 52)), fs(Fr(2 * k, 52))])


def c8s3_bag(r):
    R, B = r.randint(3, 9), r.randint(3, 9)
    T = R + B
    kind = r.choice(['RB', 'same', 'diff'])
    if kind == 'RB':
        v, t = Fr(R, T) * Fr(B, T - 1), 'the first is red and the second is black'
    elif kind == 'same':
        v, t = Fr(R, T) * Fr(R - 1, T - 1) + Fr(B, T) * Fr(B - 1, T - 1), 'both balls are of the same colour'
    else:
        v, t = 2 * Fr(R, T) * Fr(B, T - 1), 'the two balls are of different colours'
    return Q(f'A bag contains {R} red and {B} black balls. Two balls are drawn one after another without replacement. Find the probability that {t}.', fs(v),
             f'Use P(E ∩ F) = P(E)P(F|E) for each favourable order and add: {fs(v)}.', [fs(Fr(R, T) * Fr(B, T)), fs(1 - v), fs(Fr(R * B, T * T) * 2)])


def c8s3_solve(r):
    ps = [Fr(r.randint(1, 4), d) for d in r.sample([2, 3, 4, 5, 6], 3)]
    ps = [p for p in ps if 0 < p < 1]
    if len(ps) < 3:
        raise ValueError
    none = (1 - ps[0]) * (1 - ps[1]) * (1 - ps[2])
    v = 1 - none
    A, B, C = r.sample([n for n in GIRLS[:8]] + ['Kabir', 'Rohan', 'Arjun'], 3)
    return Q(f'A problem is given to {A}, {B} and {C}, whose chances of solving it independently are {fs(ps[0])}, {fs(ps[1])} and {fs(ps[2])}. Find the probability that the problem is solved.',
             fs(v), f'P(none solves) = (1 − {fs(ps[0])})(1 − {fs(ps[1])})(1 − {fs(ps[2])}) = {fs(none)} (2); P(solved) = 1 − {fs(none)} = {fs(v)} (1).',
             [fs(ps[0] * ps[1] * ps[2]), fs(none), fs(min(Fr(1), ps[0] + ps[1] + ps[2]))])


c8s3_formula = pool_mcq([
    ('P(A|B) equals (P(B) ≠ 0)', 'P(A ∩ B)/P(B)', ['P(A ∩ B)/P(A)', 'P(A)P(B)', 'P(A) + P(B)'], 'Definition of conditional probability.'),
    ('Events A and B are independent if', 'P(A ∩ B) = P(A)P(B)', ['P(A ∩ B) = 0', 'P(A ∪ B) = P(A) + P(B)', 'P(A|B) = P(B)'], 'Definition.'),
    ('If A and B are independent, then P(A|B) equals', 'P(A)', ['P(B)', 'P(A)P(B)', '0'], 'Knowing B does not change A.'),
    ('If A and B are mutually exclusive with P(A), P(B) > 0, then P(A|B) equals', '0', ['P(A)', '1', 'P(A)/P(B)'], 'A ∩ B = φ.'),
    ('P(A ∩ B) = P(A)P(B|A) is the', 'multiplication theorem of probability', ['addition theorem', "Bayes' theorem", 'theorem of total probability'], 'Rearranged definition.'),
])


def c8s3_explain(r):
    return pool_txt([
        ('Distinguish between mutually exclusive events and independent events, with one example of each.', 'Mutually exclusive: cannot occur together, P(A ∩ B) = 0 (e.g. getting 1 and 2 on one throw of a die). Independent: occurrence of one does not affect the other, P(A ∩ B) = P(A)P(B) (e.g. heads on a coin and 6 on a die).', '1 + 1 marks.'),
        ('Can two events with non-zero probabilities be both mutually exclusive and independent? Explain.', 'No: mutually exclusive gives P(A ∩ B) = 0, but independence needs P(A ∩ B) = P(A)P(B) > 0.', '2 marks.'),
        ('Explain, with an example, why P(A|B) need not equal P(B|A).', 'P(A|B) = P(A ∩ B)/P(B) and P(B|A) = P(A ∩ B)/P(A); they differ when P(A) ≠ P(B). E.g. die: A = "6", B = "even": P(A|B) = 1/3, P(B|A) = 1.', '2 marks.'),
    ])(r)


def c8s3_ar(r):
    PA, PB = Fr(r.randint(1, 9), 10), Fr(r.randint(1, 9), 10)
    if r.random() < 0.5:
        return ar(f'If A and B are independent with P(A) = {num(float(PA))} and P(B) = {num(float(PB))}, then P(A ∩ B) = {num(float(PA * PB), 3)}.', 'For independent events, P(A ∩ B) = P(A)P(B).', 'a', 'R gives A directly.')
    return ar(f'If A and B are independent with P(A) = {num(float(PA))} and P(B) = {num(float(PB))}, then P(A ∩ B) = 0.', 'For independent events, P(A ∩ B) = P(A)P(B).', 'd',
              f'A is false: P(A ∩ B) = {num(float(PA * PB), 3)}; zero would need mutually exclusive events. R is true.')


def c8s3_case(r):
    n = r.choice([100, 200, 50])
    pc = r.choice([40, 60, 30])
    pm = r.choice([30, 50, 45])
    both = r.choice([10, 15, 20])
    c, m, b = Fr(pc, 100), Fr(pm, 100), Fr(both, 100)
    return {'stem': (f'In a survey of {n} commerce students in {r.choice(CITIES)}, {pc}% study Applied Mathematics, {pm}% study Informatics Practices and {both}% study both. A student is chosen at random.\n'
                     f'(i) Find the probability that the student studies Informatics Practices, given that the student studies Applied Mathematics. (1)\n'
                     f'(ii) Find the probability that the student studies Applied Mathematics, given Informatics Practices. (1)\n(iii) Are the two choices independent? Justify. (2)'),
            'answer': f'(i) {fs(b / c)} (ii) {fs(b / m)} (iii) {"Yes" if b == c * m else "No"}: P(A)P(B) = {num(float(c * m), 3)} {"=" if b == c * m else "≠"} P(A ∩ B) = {num(float(b), 2)}',
            'key': '(i) P(A ∩ B)/P(A) (1). (ii) P(A ∩ B)/P(B) (1). (iii) compare P(A)P(B) with P(A ∩ B) (1) and conclude (1).'}


# st4 total probability and Bayes


def c8s4_total(r):
    r1, b1, r2, b2 = r.randint(2, 7), r.randint(2, 7), r.randint(2, 7), r.randint(2, 7)
    v = Fr(1, 2) * Fr(r1, r1 + b1) + Fr(1, 2) * Fr(r2, r2 + b2)
    return Q(f'Bag I contains {r1} red and {b1} black balls; Bag II contains {r2} red and {b2} black balls. A bag is chosen at random and a ball is drawn from it. Find the probability that the ball is red.',
             fs(v), f'Total probability: ½ × {r1}/{r1 + b1} + ½ × {r2}/{r2 + b2} = {fs(v)}.', [fs(Fr(r1 + r2, r1 + b1 + r2 + b2)), fs(Fr(r1, r1 + b1) * Fr(r2, r2 + b2)), fs(1 - v)])


def c8s4_bayes2(r):
    r1, b1, r2, b2 = r.randint(2, 7), r.randint(2, 7), r.randint(2, 7), r.randint(2, 7)
    p1, p2 = Fr(r1, r1 + b1), Fr(r2, r2 + b2)
    v = p1 / (p1 + p2)
    return Q(f'Bag I has {r1} red and {b1} black balls and Bag II has {r2} red and {b2} black balls. A bag is chosen at random and a ball drawn from it is red. Find the probability that it came from Bag I.',
             fs(v), f"Bayes' theorem: (½ × {fs(p1)})/(½ × {fs(p1)} + ½ × {fs(p2)}) = {fs(v)}.", [fs(p1), fs(Fr(1, 2)) if v != Fr(1, 2) else fs(p2), fs(1 - v)])


def c8s4_machines(r):
    shares = r.choice([(50, 30, 20), (25, 35, 40), (40, 40, 20), (30, 50, 20), (45, 35, 20), (60, 30, 10)])
    defs = r.choice([(2, 3, 4), (5, 4, 2), (1, 2, 3), (3, 2, 1), (4, 3, 2)])
    k = r.randrange(3)
    tot = sum(Fr(s, 100) * Fr(d, 100) for s, d in zip(shares, defs))
    v = Fr(shares[k], 100) * Fr(defs[k], 100) / tot
    lab = ['A', 'B', 'C']
    co = r.choice(['A bolt factory', 'A pen manufacturer', 'A biscuit factory', 'An LED bulb maker'])
    return Q(f'{co} has machines A, B and C producing {shares[0]}%, {shares[1]}% and {shares[2]}% of the output, of which {defs[0]}%, {defs[1]}% and {defs[2]}% respectively are defective. '
             f'An item drawn at random is found defective. Find the probability that it was produced by machine {lab[k]}.', fs(v),
             f"P(defective) = {' + '.join(f'{s}/100 × {d}/100' for s, d in zip(shares, defs))} = {fs(tot)} (2). Bayes: P({lab[k]}|D) = ({shares[k]}/100 × {defs[k]}/100)/{fs(tot)} = {fs(v)} (3).",
             [fs(Fr(shares[k], 100)), fs(Fr(defs[k], sum(defs))), fs(Fr(shares[k], 100) * Fr(defs[k], 100))])


def c8s4_test(r):
    prev = r.choice([Fr(1, 100), Fr(2, 100), Fr(5, 100), Fr(1, 1000), Fr(1, 50)])
    sens = r.choice([Fr(99, 100), Fr(95, 100), Fr(90, 100)])
    fp = r.choice([Fr(1, 100), Fr(5, 1000), Fr(2, 100), Fr(5, 100)])
    v = prev * sens / (prev * sens + (1 - prev) * fp)
    return Q(f'A blood test detects a disease with probability {num(float(sens), 3)} when the disease is present, but also gives a positive result for {num(float(fp * 100), 2)}% of healthy people. '
             f'If {num(float(prev * 100), 2)}% of the population has the disease, find the probability that a person who tests positive actually has the disease.', fs(v) + f' ≈ {num(float(v), 3)}',
             f"Bayes: ({num(float(prev), 4)} × {num(float(sens), 3)})/({num(float(prev), 4)} × {num(float(sens), 3)} + {num(float(1 - prev), 4)} × {num(float(fp), 4)}) = {fs(v)} ≈ {num(float(v), 3)} (5 marks: events defined, total probability, Bayes, value).",
             [num(float(sens), 3), num(float(prev), 4), num(float(1 - v), 3)])


c8s4_formula = pool_mcq([
    ("In Bayes' theorem, the probabilities P(Eᵢ) are called", 'prior probabilities', ['posterior probabilities', 'conditional probabilities of A', 'likelihoods of A'], 'Known before the event A is observed.'),
    ("In Bayes' theorem, the probabilities P(Eᵢ|A) are called", 'posterior probabilities', ['prior probabilities', 'marginal probabilities', 'joint probabilities'], 'Revised after A is observed.'),
    ('Events E₁, E₂, …, Eₙ form a partition of the sample space S if they are', 'pairwise disjoint, exhaustive and each has non-zero probability', ['independent', 'equally likely', 'pairwise disjoint only'], 'Definition of a partition.'),
    ('The theorem of total probability states P(A) =', 'Σ P(Eᵢ)P(A|Eᵢ)', ['Σ P(Eᵢ|A)', 'Π P(Eᵢ)P(A|Eᵢ)', 'Σ P(A)P(Eᵢ)'], 'Over a partition E₁, …, Eₙ.'),
])


def c8s4_explain(r):
    n = r.choice([2, 3])
    return {'stem': f"State Bayes' theorem for a partition of the sample space into {n} events and explain what is meant by prior and posterior probabilities.",
            'answer': 'P(Eᵢ|A) = P(Eᵢ)P(A|Eᵢ)/Σⱼ P(Eⱼ)P(A|Eⱼ). Prior: P(Eᵢ), known before A; posterior: P(Eᵢ|A), revised after A is observed.',
            'key': 'Statement with conditions (1); meanings (1).'}


def c8s4_ar(r):
    return pool_ar([
        ("In Bayes' theorem the denominator equals P(A).", 'By the theorem of total probability, P(A) = Σ P(Eᵢ)P(A|Eᵢ) for a partition E₁, …, Eₙ.', 'a', 'R explains the denominator.'),
        ('If a test is 99% accurate, a positive result means the person has the disease with probability 0.99.', "Bayes' theorem combines the prior probability with the test's accuracy.", 'd',
         'A is false: the posterior depends on how common the disease is and can be much lower. R is true.'),
        ('The posterior probabilities P(E₁|A), …, P(Eₙ|A) add up to 1.', 'E₁, …, Eₙ form a partition of the sample space.', 'a', 'Given A, exactly one Eᵢ occurs.'),
    ])(r)


def c8s4_case(r):
    n = [r.choice([2000, 3000, 4000]), r.choice([4000, 5000, 6000]), r.choice([1000, 2000, 6000])]
    p = r.choice([(Fr(1, 100), Fr(3, 100), Fr(15, 100)), (Fr(1, 100), Fr(2, 100), Fr(10, 100)), (Fr(2, 100), Fr(5, 100), Fr(10, 100))])
    T = sum(n)
    tot = sum(Fr(a, T) * b for a, b in zip(n, p))
    v = Fr(n[0], T) * p[0] / tot
    return {'stem': (f'An insurance company in {r.choice(CITIES)} insured {n[0]} scooter riders, {n[1]} car drivers and {n[2]} truck drivers. The probabilities of an accident for them are '
                     f'{num(float(p[0]), 2)}, {num(float(p[1]), 2)} and {num(float(p[2]), 2)} respectively. One of the insured persons meets with an accident.\n'
                     f'(i) Write the prior probabilities of the three groups. (1)\n(ii) Find the probability that an insured person meets with an accident. (1)\n(iii) Find the probability that the person is a scooter rider. (2)'),
            'answer': f'(i) {fs(Fr(n[0], T))}, {fs(Fr(n[1], T))}, {fs(Fr(n[2], T))} (ii) {fs(tot)} (iii) {fs(v)}',
            'key': '(i) group/total (1). (ii) total probability (1). (iii) Bayes (2).'}


# ======================================================== ch09 Descriptive statistics


def _classes(r, k=None):
    w = r.choice([5, 10, 20])
    start = r.choice([0, w, 2 * w])
    k = k or r.randint(5, 6)
    cls = [(start + i * w, start + (i + 1) * w) for i in range(k)]
    fq = [r.randint(2, 15) for _ in cls]
    return cls, fq, w


def _ctab(cls, fq, lab='Class'):
    return f'{lab}: ' + ', '.join(f'{a}–{b}' for a, b in cls) + '\nFrequency: ' + ', '.join(map(str, fq))


def c9s1_mark(r):
    a = r.randrange(0, 200, 5)
    w = r.choice([5, 10, 20, 25])
    return Q(f'Find the class mark and the class size of the class {a}–{a + w}.', f'{num((2 * a + w) / 2)}; {w}', f'Class mark = (lower + upper)/2 = {num((2 * a + w) / 2)}; class size = {w}.',
             [f'{a + w}; {w}', f'{num((2 * a + w) / 2)}; {2 * w}', f'{a}; {w}'])


def c9s1_cf(r):
    cls, fq, w = _classes(r)
    k = r.randint(2, len(cls) - 1)
    cf = sum(fq[:k])
    return Q(f'For the distribution\n{_ctab(cls, fq)}\nfind the "less than" cumulative frequency for the upper limit {cls[k - 1][1]}.', str(cf),
             f'Add the frequencies of the first {k} classes: {" + ".join(map(str, fq[:k]))} = {cf}.', [str(cf + fq[k]), str(fq[k - 1]), str(sum(fq) - cf)])


def c9s1_pie(r):
    items = r.sample(['Food', 'Rent', 'Education', 'Transport', 'Savings', 'Medical', 'Clothing', 'Others'], 5)
    while True:
        parts = [r.choice([5, 10, 15, 20, 25, 30]) for _ in items]
        if sum(parts) == 100:
            break
        parts[-1] = 100 - sum(parts[:-1])
        if 0 < parts[-1] <= 40:
            break
    k = r.randrange(5)
    inc = r.choice([20000, 30000, 40000, 50000, 60000])
    ang = Fr(parts[k] * 360, 100)
    return Q(f'A family in {r.choice(CITIES)} spends its monthly income of {inr(inc)} as follows: ' + ', '.join(f'{a} {p}%' for a, p in zip(items, parts)) +
             f'. In a pie chart, what is the central angle for {items[k]}, and how much is spent on it?', f'{mixed(ang)}°; {inr(inc * parts[k] / 100)}',
             f'Angle = {parts[k]}% of 360° = {mixed(ang)}°; amount = {parts[k]}% of {inr(inc)} = {inr(inc * parts[k] / 100)}.',
             [f'{parts[k]}°; {inr(inc * parts[k] / 100)}', f'{mixed(ang * 2)}°; {inr(inc * parts[k] / 50)}', f'{mixed(ang)}°; {inr(inc * parts[k] / 10)}'])


def c9s1_hist(r):
    cls = [(0, 10), (10, 20), (20, 40), (40, 70), (70, 80)] if r.random() < 0.5 else [(0, 5), (5, 10), (10, 20), (20, 30), (30, 50)]
    fq = [r.randint(4, 20) for _ in cls]
    m = min(b - a for a, b in cls)
    k = r.choice([i for i, (a, b) in enumerate(cls) if b - a != m])
    adj = Fr(fq[k] * m, cls[k][1] - cls[k][0])
    return Q(f'For a histogram of the distribution\n{_ctab(cls, fq)}\nthe classes are of unequal width. Taking the minimum class size {m} as standard, find the adjusted frequency (height of the bar) for the class {cls[k][0]}–{cls[k][1]}.',
             mixed(adj), f'Adjusted frequency = (minimum class size/class size) × frequency = ({m}/{cls[k][1] - cls[k][0]}) × {fq[k]} = {mixed(adj)}.',
             [str(fq[k]), mixed(Fr(fq[k] * (cls[k][1] - cls[k][0]), m)), mixed(adj + 1)])


def c9s1_inclusive(r):
    a = r.choice([10, 20, 30, 0])
    w = r.choice([10, 5])
    cls = [(a + i * w, a + (i + 1) * w - 1) for i in range(4)]
    out = [(num(x - 0.5), num(y + 0.5)) for x, y in cls]
    return {'stem': f'The classes {", ".join(f"{x}–{y}" for x, y in cls)} are in inclusive form. Explain why they must be converted before drawing a histogram, and convert them.',
            'answer': 'A histogram needs continuous classes with no gaps. Subtract 0.5 from each lower limit and add 0.5 to each upper limit: ' + ', '.join(f'{x}–{y}' for x, y in out) + '.',
            'key': 'Reason (gaps between classes) (1); correct exclusive classes (1).'}


def c9s1_median_class(r):
    cls, fq, w = _classes(r)
    N = sum(fq)
    cf = list(itertools.accumulate(fq))
    k = next(i for i, c in enumerate(cf) if c >= N / 2)
    return Q(f'Prepare the "less than" cumulative frequency table for\n{_ctab(cls, fq)}\nand identify the median class.', f'cf: {", ".join(map(str, cf))}; median class {cls[k][0]}–{cls[k][1]}',
             f'N = {N}, N/2 = {num(N / 2)} (1); cumulative frequencies {", ".join(map(str, cf))} (1); first cf ≥ N/2 is in {cls[k][0]}–{cls[k][1]} (1).',
             [f'cf: {", ".join(map(str, cf))}; median class {cls[k - 1][0]}–{cls[k - 1][1]}' if k else f'cf: {", ".join(map(str, cf))}; median class {cls[k + 1][0]}–{cls[k + 1][1]}'])


c9s1_tf = tf_mcq('frequency distributions and graphs', [
    'The class mark is the mid-point of a class.', 'A histogram is drawn for a continuous frequency distribution.', 'An ogive is the graph of a cumulative frequency distribution.',
    'In a histogram with unequal classes, the heights must be adjusted in proportion to class widths.', 'The total of all central angles in a pie chart is 360°.'],
    ['The class mark is the upper limit of a class.', 'A histogram has gaps between adjacent bars.', 'An ogive is drawn from simple (not cumulative) frequencies.',
     'In a pie chart the angles add up to 180°.', 'Bar graphs can only show continuous data.'])


def c9s1_ar(r):
    return pool_ar([
        ('The less-than ogive and the more-than ogive of a distribution intersect at the median.', 'At the median, the number of observations below equals the number above.', 'a', 'R explains A.'),
        ('In a histogram the bars are drawn without gaps.', 'A histogram represents a continuous distribution.', 'a', 'R explains A.'),
        ('A pie chart is suitable for showing how a whole is divided into parts.', 'The central angle of each sector is proportional to its share.', 'a', 'R explains A.'),
        ('A bar graph and a histogram are the same.', 'A histogram represents a continuous distribution.', 'd', 'A is false: bar graphs show discrete categories with gaps; histograms show continuous classes. R is true.'),
    ])(r)


def c9s1_case(r):
    cls, fq, w = _classes(r, 5)
    N = sum(fq)
    k = max(range(5), key=lambda i: fq[i])
    cf = list(itertools.accumulate(fq))
    return {'stem': (f'The daily sales (in thousand ₹) of {N} shops in a market of {r.choice(CITIES)} are:\n{_ctab(cls, fq, "Sales")}\n'
                     f'(i) How many shops had sales below {cls[2][1]}? (1)\n(ii) Which class has the highest frequency, and what is its class mark? (1)\n'
                     f'(iii) What percentage of shops had sales of at least {cls[3][0]}? Name the graph you would draw to show cumulative frequencies. (2)'),
            'answer': f'(i) {cf[2]} (ii) {cls[k][0]}–{cls[k][1]}, class mark {num((cls[k][0] + cls[k][1]) / 2)} (iii) {num((N - cf[2]) * 100 / N, 1)}%; an ogive',
            'key': '(i) cumulative frequency (1). (ii) modal class and mid-point (1). (iii) percentage (1), ogive (1).'}


# st2 additions: quartile deviation and coefficient of range


def c9s2_coefr(r):
    xs = r.sample(range(10, 99), r.randint(7, 10))
    L, Sm = max(xs), min(xs)
    v = Fr(L - Sm, L + Sm)
    return Q(f'Find the range and the coefficient of range of the data: {", ".join(map(str, xs))}.', f'{L - Sm}; {num(float(v), 3)}',
             f'Range = {L} − {Sm} = {L - Sm}; coefficient = (L − S)/(L + S) = {L - Sm}/{L + Sm} = {num(float(v), 3)}.',
             [f'{L - Sm}; {num(float(Fr(L - Sm, L)), 3)}', f'{L + Sm}; {num(float(v), 3)}', f'{L - Sm}; {num(float(Fr(L + Sm, L - Sm)), 3)}'])


def c9s2_qd(r):
    k = r.randint(2, 4)
    n = 4 * k + 3
    xs = sorted(r.sample(range(5, 99), n))
    q1, q3 = xs[k], xs[3 * k + 2]
    qd = Fr(q3 - q1, 2)
    cq = Fr(q3 - q1, q3 + q1)
    shown = xs[:]
    r.shuffle(shown)
    return Q(f'Find the quartile deviation and the coefficient of quartile deviation for the data: {", ".join(map(str, shown))}. (Use the ((n + 1)/4)th observation for Q₁.)',
             f'QD = {num(float(qd))}; coefficient = {num(float(cq), 3)}', f'Arrange in order; n = {n}. Q₁ = {k + 1}th value = {q1}; Q₃ = {3 * k + 3}th value = {q3}. QD = ({q3} − {q1})/2 = {num(float(qd))}; coefficient = ({q3} − {q1})/({q3} + {q1}) = {num(float(cq), 3)}.',
             [f'QD = {q3 - q1}; coefficient = {num(float(cq), 3)}', f'QD = {num(float(qd))}; coefficient = {num(float(Fr(q3 - q1, q3)), 3)}', f'QD = {num(float(qd) + 1)}; coefficient = {num(float(cq) + 0.05, 3)}'])


def c9s2_qdg(r):
    cls, fq, w = _classes(r, 6)
    N = sum(fq)
    if N % 4:
        fq[-1] += 4 - N % 4
        N = sum(fq)
    cf = list(itertools.accumulate(fq))

    def quart(p):
        target = Fr(p * N, 4)
        i = next(j for j, c in enumerate(cf) if c >= target)
        prev = cf[i - 1] if i else 0
        return Fr(cls[i][0]) + (target - prev) / fq[i] * w, i
    q1, i1 = quart(1)
    q3, i3 = quart(3)
    qd = (q3 - q1) / 2
    return Q(f'Calculate the quartile deviation for the distribution\n{_ctab(cls, fq)}', f'Q₁ = {num(float(q1))}, Q₃ = {num(float(q3))}, QD = {num(float(qd))}',
             f'N = {N}; Q₁ class {cls[i1][0]}–{cls[i1][1]} (N/4 = {N // 4}), Q₃ class {cls[i3][0]}–{cls[i3][1]} (3N/4 = {3 * N // 4}) (2). Qₖ = l + (kN/4 − cf)/f × h gives Q₁ = {num(float(q1))}, Q₃ = {num(float(q3))} (2). QD = (Q₃ − Q₁)/2 = {num(float(qd))} (1).')


def c9s2_ar(r):
    return pool_ar([
        ('Quartile deviation is not affected by extreme values.', 'Quartile deviation is based on the middle 50% of the observations.', 'a', 'R explains A.'),
        ('The range is a satisfactory measure of dispersion for data with outliers.', 'The range depends only on the largest and smallest values.', 'd', 'A is false: outliers distort the range. R is true.'),
        ('The coefficient of quartile deviation is a pure number.', 'It is a ratio of two quantities in the same units.', 'a', 'Units cancel, so R explains A.'),
    ])(r)


# st4 percentiles


def c9s4_pr(r):
    N = r.choice([40, 50, 60, 80, 120, 200, 250])
    below = r.randint(N // 5, N - 2)
    v = Fr(below * 100, N)
    who = name(r)
    return Q(f'In a class test taken by {N} students, {below} students scored less than {who}. Find the percentile rank of {who}.', f'{num(float(v), 2)}',
             f'PR = (number below/total) × 100 = {below}/{N} × 100 = {num(float(v), 2)}.', [num(float(Fr((below + 1) * 100, N)), 2), num(float(Fr((N - below) * 100, N)), 2), str(below)])


def c9s4_ung(r):
    k = r.choice([10, 20, 25, 30, 40, 60, 70, 75, 80, 90])
    for n in range(9, 40):
        if (k * (n + 1)) % 100 == 0:
            break
    else:
        raise ValueError
    if n > 25:
        raise ValueError
    xs = sorted(r.sample(range(10, 100), n))
    pos = k * (n + 1) // 100
    shown = xs[:]
    r.shuffle(shown)
    return Q(f'Find the {k}th percentile P{k} of the data: {", ".join(map(str, shown))}. (Use the (k(n + 1)/100)th observation.)', str(xs[pos - 1]),
             f'Arrange in ascending order; n = {n}; position = {k}({n + 1})/100 = {pos}; P{k} = {pos}th value = {xs[pos - 1]}.', [str(xs[pos]), str(xs[pos - 2]), str(xs[n // 2])])


def c9s4_grp(r):
    cls, fq, w = _classes(r, 5)
    N = sum(fq)
    k = r.choice([10, 20, 25, 30, 40, 60, 70, 75, 80, 90])
    target = Fr(k * N, 100)
    cf = list(itertools.accumulate(fq))
    i = next(j for j, c in enumerate(cf) if c >= target)
    prev = cf[i - 1] if i else 0
    v = Fr(cls[i][0]) + (target - prev) / fq[i] * w
    return Q(f'Find the {k}th percentile for the distribution\n{_ctab(cls, fq)}', num(float(v), 2),
             f'N = {N}; kN/100 = {num(float(target), 2)}; P{k} class {cls[i][0]}–{cls[i][1]} (cf before {prev}, f = {fq[i]}) (1). P{k} = l + (kN/100 − cf)/f × h = {cls[i][0]} + ({num(float(target), 2)} − {prev})/{fq[i]} × {w} = {num(float(v), 2)} (2).',
             [num(float(v) + w / 2, 2), num(float(Fr(cls[i][0]) + target / fq[i] * w), 2), str(cls[i][1])])


c9s4_mcq = pool_mcq([
    ('The first quartile Q₁ is the same as', 'P₂₅', ['P₁₀', 'P₅₀', 'D₂'], 'Q₁ divides off the lowest 25%.'),
    ('The median is the same as', 'P₅₀', ['P₂₅', 'P₇₅', 'D₄'], 'Half the data lie below the median.'),
    ('The 7th decile D₇ is the same as', 'P₇₀', ['P₇', 'Q₃', 'P₇₅'], 'Dₖ = P₁₀ₖ.'),
    ('The third quartile Q₃ is the same as', 'P₇₅', ['P₃₀', 'D₃', 'P₆₇'], 'Three-quarters of the data lie below Q₃.'),
    ('A percentile rank of 90 means that the candidate scored', 'more than 90% of the candidates', ['90% marks', '90 marks', 'less than 90% of the candidates'], 'Percentile rank is a relative position, not a percentage of marks.'),
])


def c9s4_explain(r):
    p = r.choice([85, 90, 95, 98])
    m = r.choice([60, 65, 70, 72])
    return {'stem': f'A student scored {m}% marks in an entrance test and was placed at the {p}th percentile. Explain the difference between these two figures.',
            'answer': f'{m}% is the share of total marks obtained; {p}th percentile means the student did better than about {p}% of the candidates (a relative position).',
            'key': 'Percentage of marks explained (1); percentile as position explained (1).'}


def c9s4_ar(r):
    return pool_ar([
        ('The 50th percentile of a data set is its median.', 'Half of the observations lie below the median.', 'a', 'R explains A.'),
        ('Percentiles divide an ordered data set into 100 equal parts.', 'There are 99 percentiles, P₁ to P₉₉.', 'b', 'Both true; R gives a count, not the reason.'),
        ('A percentile rank of 80 means the student scored 80% marks.', 'Percentile rank shows the percentage of candidates scoring below a given score.', 'd', 'A is false: it is a relative position. R is true.'),
    ])(r)


c9s4_tf = tf_mcq('percentiles and quartiles', [
    'There are 99 percentiles that divide the data into 100 equal parts.', 'Q₂, D₅ and P₅₀ are all equal to the median.', 'Percentiles are used to report scores in large competitive examinations.',
    'Data must be arranged in order before percentiles are found.', 'The interquartile range is Q₃ − Q₁.'],
    ['There are 100 percentiles.', 'P₂₅ is the same as the median.', 'Percentile rank is the same as percentage of marks.', 'Percentiles can be found without arranging the data.', 'D₁ is the same as P₁.'])


def c9s4_case(r):
    N = r.choice([100000, 200000, 150000])
    pr = r.choice([90, 95, 97, 99])
    who = name(r)
    return {'stem': (f'In a national entrance test taken by {N:,} candidates, scores are reported as percentile ranks. {who} has a percentile rank of {pr}.\n'
                     f'(i) What percentage of candidates scored below {who}? (1)\n(ii) Approximately how many candidates scored below {who}? (1)\n'
                     f'(iii) About how many candidates scored at or above {who}? Is {who}\'s percentage of marks necessarily {pr}%? (2)'),
            'answer': f'(i) {pr}% (ii) about {N * pr // 100:,} (iii) about {N - N * pr // 100:,}; no, a percentile rank is a relative position, not a percentage of marks',
            'key': '(i) meaning (1). (ii) pr% of N (1). (iii) remainder (1), distinction (1).'}


# ======================================================== FAMILIES

FAMILIES = {
    S + '05-st1': reuse('12-st1'),
    S + '05-st2': reuse('12-st2', skip=(6,)) + [F('C1', 'D1', 'mcq', c5s2_std), F('C2', 'D3', 'mcq', c5s2_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c5s2_ekx), F('C3', 'D3', 'numerical', c5s2_ax),
                                     F('C2', 'D2', 'short', c5s2_inf), F('C3', 'D2', 'numerical', c5s2_root)],
    S + '05-st3': [F('C1', 'D1', 'mcq', c5s3_def), F('C1', 'D2', 'mcq', c5s3_tf), F('C2', 'D2', 'explain', c5s3_explain), F('C2', 'D3', 'mcq', c5s3_ar, kinds=('ar',)),
                   F('C2', 'D2', 'short', c5s3_count), F('C3', 'D2', 'numerical', c5s3_check), F('C3', 'D3', 'numerical', c5s3_k), F('C4', 'D3', 'numerical', c5s3_removable),
                   F('C4', 'D4', 'long', c5s3_two, kinds=('long5',)), F('C3', 'D3', 'case', c5s3_case, marks=4, minutes=6)],
    S + '06-st1': reuse('12-st4', skip=(7,)) + [F('C3', 'D1', 'short', c6s1_avg), F('C2', 'D2', 'short', c6s1_mc)],
    S + '06-st2': reuse('12-st5', skip=(6,)) + [F('C1', 'D1', 'mcq', c6s2_rules), F('C2', 'D3', 'mcq', c6s2_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c6s2_chain),
                                                F('C3', 'D2', 'short', c6s2_root), F('C3', 'D3', 'numerical', c6s2_prodval), F('C4', 'D3', 'multi_step', c6s2_quotval)],
    S + '06-st3': [F('C1', 'D1', 'mcq', c6s3_basic), F('C2', 'D2', 'explain', c6s3_explain), F('C2', 'D3', 'mcq', c6s3_ar, kinds=('ar',)), F('C2', 'D2', 'short', c6s3_exp),
                   F('C3', 'D2', 'numerical', c6s3_xne), F('C3', 'D2', 'numerical', c6s3_log), F('C3', 'D3', 'numerical', c6s3_implicit), F('C3', 'D4', 'numerical', c6s3_param),
                   F('C4', 'D3', 'multi_step', c6s3_implicit2), F('C4', 'D4', 'long', c6s3_xx, kinds=('long5',)), F('C3', 'D3', 'case', c6s3_case, marks=4, minutes=6)],
    S + '06-st4': [F('C1', 'D1', 'mcq', c6s4_mcq), F('C2', 'D2', 'explain', c6s4_acc), F('C2', 'D3', 'mcq', c6s4_ar, kinds=('ar',)), F('C3', 'D1', 'short', c6s4_poly),
                   F('C3', 'D3', 'numerical', c6s4_log), F('C4', 'D4', 'long', c6s4_ode, kinds=('long5',))],
    S + '07-st1': reuse('06-st1') + reuse('06-st2'),
    S + '07-st2': reuse('06-st3') + [F('C1', 'D1', 'mcq', c7s2_mcq), F('C2', 'D3', 'mcq', c7s2_ar, kinds=('ar',)), F('C3', 'D1', 'short', c7s2_rep), F('C3', 'D2', 'numerical', c7s2_circ),
                                     F('C3', 'D3', 'numerical', c7s2_neck), F('C4', 'D4', 'multi_step', c7s2_together)],
    S + '07-st3': reuse('06-st4') + reuse('06-st5'),
    S + '08-st1': reuse('14-st1') + reuse('14-st2'),
    S + '08-st2': reuse('14-st3') + reuse('14-st4'),
    S + '08-st3': [F('C1', 'D1', 'mcq', c8s3_formula), F('C2', 'D2', 'explain', c8s3_explain), F('C2', 'D3', 'mcq', c8s3_ar, kinds=('ar',)), F('C2', 'D2', 'short', c8s3_check),
                   F('C3', 'D1', 'short', c8s3_basic), F('C3', 'D2', 'numerical', c8s3_indep), F('C3', 'D2', 'numerical', c8s3_dice), F('C3', 'D3', 'numerical', c8s3_cards),
                   F('C4', 'D3', 'numerical', c8s3_bag), F('C4', 'D4', 'multi_step', c8s3_solve, kinds=('long5',)), F('C3', 'D3', 'case', c8s3_case, marks=4, minutes=6)],
    S + '08-st4': [F('C1', 'D1', 'mcq', c8s4_formula), F('C2', 'D2', 'explain', c8s4_explain), F('C2', 'D3', 'mcq', c8s4_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c8s4_total),
                   F('C3', 'D3', 'numerical', c8s4_bayes2), F('C4', 'D4', 'long', c8s4_machines, kinds=('long5',)), F('C4', 'D5', 'long', c8s4_test, kinds=('long5',)),
                   F('C3', 'D3', 'case', c8s4_case, marks=4, minutes=6)],
    S + '09-st1': [F('C1', 'D1', 'mcq', c9s1_mark), F('C1', 'D2', 'mcq', c9s1_tf), F('C2', 'D2', 'explain', c9s1_inclusive), F('C2', 'D3', 'mcq', c9s1_ar, kinds=('ar',)),
                   F('C3', 'D1', 'short', c9s1_cf), F('C3', 'D2', 'numerical', c9s1_pie), F('C3', 'D3', 'numerical', c9s1_hist), F('C4', 'D3', 'multi_step', c9s1_median_class),
                   F('C3', 'D3', 'case', c9s1_case, marks=4, minutes=6)],
    S + '09-st2': reuse('13-st1') + reuse('13-st2') + [F('C2', 'D3', 'mcq', c9s2_ar, kinds=('ar',)), F('C3', 'D1', 'short', c9s2_coefr), F('C3', 'D3', 'numerical', c9s2_qd),
                                                       F('C4', 'D4', 'long', c9s2_qdg, kinds=('long5',))],
    S + '09-st3': reuse('13-st3') + reuse('13-st4'),
    S + '09-st4': [F('C1', 'D1', 'mcq', c9s4_mcq), F('C1', 'D2', 'mcq', c9s4_tf), F('C2', 'D2', 'explain', c9s4_explain), F('C2', 'D3', 'mcq', c9s4_ar, kinds=('ar',)),
                   F('C3', 'D1', 'short', c9s4_pr), F('C3', 'D2', 'numerical', c9s4_ung), F('C4', 'D3', 'multi_step', c9s4_grp), F('C3', 'D3', 'case', c9s4_case, marks=4, minutes=6)],
}
