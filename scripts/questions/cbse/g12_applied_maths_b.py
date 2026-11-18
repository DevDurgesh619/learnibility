"""CBSE class 12 Applied Mathematics (241): families for ch04 (higher order derivatives and marginal analysis),
ch05 (integration and its applications), ch06 (differential equations and modelling) and ch13 (linear
programming). Calculus and LPP families of the 041 modules are re-used (trigonometric variants filtered out)
and business applications are added."""
from __future__ import annotations

import math
from fractions import Fraction as Fr

from g12_applied_maths_h import (F, Q, ar, mcqbank, arbank, xbank, fz, fpar, poly, term, dist3, name, inr, num, CITIES,
                                 rs, reuse, no_trig)
from g12_maths_b import mono, polyF, co, ex

S = 'cbse-g12-applied-maths-ch'


def _pv(terms, x):
    return sum(Fr(c) * Fr(x) ** n for c, n in terms)


def _d(terms):
    return [(c * n, n - 1) for c, n in terms if n > 0]


# ======================================================================= ch04 st1 higher-order derivatives

b4s1_mcq = mcqbank([
    ('If y = eˣ, then dⁿy/dxⁿ = …', 'eˣ', ['neˣ', 'eⁿˣ', 'xeˣ'], 'Every derivative of eˣ is eˣ.'),
    ('If y = x⁴, then d⁴y/dx⁴ = …', '24', ['4', '0', '24x'], '4 × 3 × 2 × 1.'),
    ('If y = log x, then d²y/dx² = …', '−1/x²', ['1/x²', '1/x', '−1/x'], 'd/dx(1/x) = −1/x².'),
    ('The second derivative of a linear function ax + b is …', '0', ['a', 'b', 'ax'], 'First derivative is a constant.'),
    ('If y = x³, then d³y/dx³ = …', '6', ['3x²', '6x', '0'], '3 × 2 × 1.'),
    ('If y = e^(2x), then d²y/dx² = …', '4e^(2x)', ['2e^(2x)', 'e^(2x)', 'e^(4x)'], 'Each differentiation multiplies by 2.'),
    ('If y = aˣ, then d²y/dx² = …', 'aˣ(log a)²', ['aˣ log a', 'x(x − 1)aˣ⁻²', 'aˣ'], 'd/dx aˣ = aˣ log a.'),
    ('For y = x⁵, the (n)th derivative is zero for …', 'n ≥ 6', ['n ≥ 5', 'n ≥ 4', 'no n'], 'Degree 5 polynomial.'),
])


def b4s1_poly(r):
    k = r.choice([2, 3])
    terms = [(r.choice([1, 2, 3, 4, 5, -1, -2]), n) for n in sorted(r.sample([5, 4, 3, 2, 1, 0], 4), reverse=True)]
    d = terms
    for _ in range(k):
        d = _d(d)
    a = r.randint(-2, 3)
    val = _pv(d, a)
    order = {2: 'd²y/dx²', 3: 'd³y/dx³'}[k]
    return Q(f'If y = {polyF(terms)}, find {order} at x = {a}.', fz(val), f'{order} = {polyF(d) if d else "0"}; at x = {a}: {fz(val)}.',
             dist3(fz(val), [fz(_pv(_d(terms), a)), fz(_pv(_d(d), a)) if _d(d) else '1', fz(val + 1), fz(-val) if val else '2']),
             _d=(lambda x: float(_pv(_d(terms) if k == 2 else _d(_d(terms)), x)), lambda x: float(_pv(d, x)), 0.7))


def b4s1_exp(r):
    k = r.randint(0, 2)
    sup = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
    if k == 0:
        a = r.choice([2, 3, -1, -2, 4])
        ans = f'e^({a}x)({fz(2 * a)} + {co(a * a)}x)'
        return Q(f'Find d²y/dx² if y = x e^({a}x).', ans,
                 f'y′ = e^({a}x) + {co(a)}x e^({a}x) (1 mark); y″ = {co(a)}e^({a}x) + {co(a)}e^({a}x) + {co(a * a)}x e^({a}x) = {ans} (2 marks).',
                 dist3(ans, [f'e^({a}x)(1 + {co(a)}x)', f'{co(a * a)}x e^({a}x)', f'e^({a}x)({fz(a)} + {co(a * a)}x)']),
                 _d=(lambda x: math.exp(a * x) * (1 + a * x), lambda x: math.exp(a * x) * (2 * a + a * a * x), 0.3))
    if k == 1:
        a, b = r.randint(2, 5), r.randint(1, 9)
        argt = f'{a}x + {b}'
        ans = f'−{a * a}/({argt})²'
        return Q(f'Find d²y/dx² if y = log({argt}), x > 0.', ans, f'y′ = {a}/({argt}) (1 mark); y″ = −{a * a}/({argt})² (1 mark).',
                 dist3(ans, [f'{a}/({argt})', f'{a * a}/({argt})²', f'−{a}/({argt})²']),
                 _d=(lambda x: a / (a * x + b), lambda x: -a * a / (a * x + b) ** 2, 0.2))
    n = r.randint(2, 6)
    pw = '' if n == 2 else ('x' if n == 3 else 'x' + str(n - 2).translate(sup))
    ans = f'{n * (n - 1)}{pw} log x + {2 * n - 1}{pw}'
    return Q(f'Find d²y/dx² if y = x{str(n).translate(sup)} log x, x > 0.', ans,
             f'y′ = {n}x{str(n - 1).translate(sup)} log x + x{str(n - 1).translate(sup)} (1 mark); y″ = {n * (n - 1)}{pw} log x + {n}{pw} + {n - 1}{pw} = {ans} (2 marks).'.replace('x¹', 'x'),
             dist3(ans, [f'{n * (n - 1)}{pw} log x', f'{n}{pw} log x + {n}{pw}', f'{n * (n - 1)}{pw} log x + {n}{pw}']),
             _d=(lambda x: n * x ** (n - 1) * math.log(x) + x ** (n - 1), lambda x: n * (n - 1) * x ** (n - 2) * math.log(x) + (2 * n - 1) * x ** (n - 2), 1.4))


def b4s1_show(r):
    m, n = r.sample([-3, -2, -1, 1, 2, 3, 4], 2)
    s, p = m + n, m * n
    eq = 'd²y/dx²' + (f' − {co(s)}dy/dx' if s > 0 else f' + {co(-s)}dy/dx' if s < 0 else '') + term(p, 'y') + ' = 0'
    return Q(f'If y = A{ex(m)} + B{ex(n)}, where A and B are constants, show that {eq}.', eq,
             f'dy/dx = {co(m)}A{ex(m)}{term(n, "B" + ex(n))}; d²y/dx² = {co(m * m)}A{ex(m)}{term(n * n, "B" + ex(n))} (2 marks); substitute (1 mark).')


def b4s1_ar(r):
    k = r.randint(0, 2)
    n = r.randint(3, 7)
    sup = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
    if k == 0:
        return ar(f'If y = x{str(n).translate(sup)}, then the {n + 1}th derivative of y is 0.', 'Each differentiation lowers the degree of a polynomial by 1.', 'a', f'The {n}th derivative is {math.factorial(n)}, a constant.')
    if k == 1:
        a = r.randint(2, 5)
        return ar(f'If y = e^({a}x), then d²y/dx² = {a * a}y.', f'd/dx e^({a}x) = {a}e^({a}x).', 'a', f'Differentiate twice: {a} × {a}.')
    return ar('If y = log x, then d²y/dx² = 1/x².', 'd/dx (1/x) = −1/x².', 'd', 'd²y/dx² = −1/x²; A false, R true.')


def b4s1_case(r):
    a, b, c = r.randint(1, 4), r.randint(2, 12), r.randint(5, 40)
    t0 = r.randint(1, 5)
    who = name(r)
    s = [(a, 3), (-b, 2), (c, 1)]
    v = _d(s)
    acc = _d(v)
    return Q((f'In a business simulation, {who} models the units sold after t months as s(t) = {polyF(s, "t")}. '
              f'(i) Find the rate of change of sales ds/dt. (ii) Find d²s/dt². (iii) Find both at t = {t0} and say whether the rate of sales is increasing or decreasing then.'),
             f'(i) {polyF(v, "t")} (ii) {polyF(acc, "t")} (iii) {fz(_pv(v, t0))} and {fz(_pv(acc, t0))}; {"increasing" if _pv(acc, t0) > 0 else "decreasing" if _pv(acc, t0) < 0 else "neither (zero)"}',
             '(i) 1 mark (ii) 1 mark (iii) values and sign of the second derivative (2 marks).')


# ======================================================================= ch04 st2 marginal cost and marginal revenue

b4s2_mcq = mcqbank([
    ('Marginal cost is …', 'the rate of change of total cost with respect to output, dC/dx', ['total cost divided by output', 'the fixed cost', 'the cost of the first unit'], 'Definition.'),
    ('Marginal revenue is …', 'dR/dx, the rate of change of total revenue with respect to quantity sold', ['R/x', 'the price of the first unit', 'total revenue minus cost'], 'Definition.'),
    ('If R(x) = px for a constant price p, then MR = …', 'p', ['px', 'p/x', '0'], 'Derivative of px.'),
    ('The marginal cost at x units approximately equals …', 'the cost of producing the (x + 1)th unit', ['the cost of x units', 'the average cost', 'the fixed cost'], 'Interpretation of marginal cost.'),
    ('If C(x) = 500 + 20x, the marginal cost is …', '₹20 per unit', ['₹500', '₹520', '₹20x'], 'dC/dx = 20.'),
    ('If the demand function is p = a − bx, the total revenue is …', 'R = ax − bx²', ['R = a − bx', 'R = ax + bx²', 'R = a − 2bx'], 'R = px.'),
    ('Fixed cost does not affect …', 'the marginal cost', ['the total cost', 'the average cost', 'the profit'], 'The derivative of a constant is 0.'),
    ('Marginal profit is …', 'MR − MC', ['MR + MC', 'R − C', 'MC − MR'], 'P = R − C ⇒ P′ = R′ − C′.'),
])


def _cost(r):
    a = Fr(r.choice([1, 2, 3, 1, Fr(1, 2), Fr(1, 3)]))
    b = r.randint(2, 20)
    c = r.randint(20, 200)
    d = r.choice(range(500, 5001, 100))
    terms = [(a, 3), (-b, 2), (c, 1), (d, 0)]
    if any(_pv(_d(terms), x) <= 0 for x in range(0, 40)):
        raise ValueError
    return terms


def b4s2_mc(r):
    terms = _cost(r)
    x0 = r.randint(3, 25)
    mc = _pv(_d(terms), x0)
    who = name(r)
    return Q(f'The total cost (in ₹) of producing x units of a product at {who}\'s unit is C(x) = {polyF(terms)}. Find the marginal cost when {x0} units are produced.', rs(mc),
             f'MC = C′(x) = {polyF(_d(terms))}; at x = {x0}: {rs(mc)}.', dist3(rs(mc), [rs(_pv(terms, x0)), rs(_pv(terms, x0) / x0), rs(_pv(_d(terms), x0 + 1)), rs(mc + terms[3][0])]),
             _d=(lambda x: float(_pv(terms, x)), lambda x: float(_pv(_d(terms), x)), 4.0))


def b4s2_mr(r):
    a, b = r.randint(50, 500), Fr(r.choice([1, 2, 3, 4, 5, Fr(1, 2)]))
    x0 = r.randint(2, 30)
    if a - 2 * b * x0 <= 0:
        raise ValueError
    kind = r.randint(0, 1)
    R = [(-b, 2), (a, 1)]
    mr = a - 2 * b * x0
    if kind == 0:
        stem = f'The demand function of a product is p = {a} − {co(b)}x, where p is the price (in ₹) and x the number of units demanded. Find the total revenue function and the marginal revenue when x = {x0}.'
        key = f'R = px = {polyF([(a, 1), (-b, 2)])} (1 mark); MR = dR/dx = {polyF(_d([(a, 1), (-b, 2)]))}; at x = {x0}: {rs(mr)} (2 marks).'
    else:
        stem = f'The total revenue (in ₹) from selling x units is R(x) = {polyF([(a, 1), (-b, 2)])}. Find the marginal revenue when x = {x0}.'
        key = f'MR = R′(x) = {polyF(_d([(a, 1), (-b, 2)]))}; at x = {x0}: {rs(mr)}.'
    ans = rs(mr) if kind else f'R = {polyF([(a, 1), (-b, 2)])}; MR = {rs(mr)}'
    alt = [rs(a - b * x0), rs(_pv(R, x0)), rs(a - 2 * b * x0 + b)] if kind else [f'R = {polyF([(a, 1), (-b, 2)])}; MR = {rs(a - b * x0)}', f'R = {a} − {co(b)}x; MR = {rs(-b)}', f'R = {polyF([(a, 1), (-b, 2)])}; MR = {rs(_pv(R, x0))}']
    return Q(stem, ans, key, dist3(ans, alt))


def b4s2_avg(r):
    terms = _cost(r)
    x0 = r.randint(4, 20)
    ac = _pv(terms, x0) / x0
    mc = _pv(_d(terms), x0)
    ans = f'AC = {rs(ac)}, MC = {rs(mc)}'
    return Q(f'For the cost function C(x) = {polyF(terms)}, find the average cost and the marginal cost when x = {x0}.', ans,
             f'AC = C(x)/x = {fz(_pv(terms, x0))}/{x0} (1 mark); MC = C′(x) = {polyF(_d(terms))} (1 mark); values (1 mark).',
             dist3(ans, [f'AC = {rs(mc)}, MC = {rs(ac)}', f'AC = {rs(_pv(terms, x0))}, MC = {rs(mc)}', f'AC = {rs(ac)}, MC = {rs(_pv(_d(terms), x0) / x0)}']))


def b4s2_mp(r):
    a, b = r.randint(100, 600), r.choice([1, 2, 3, 4])
    c, d = r.randint(10, 60), r.choice(range(500, 3001, 100))
    x0 = r.randint(3, 40)
    R = [(-b, 2), (a, 1)]
    C = [(c, 1), (d, 0)]
    P = [(-b, 2), (a - c, 1), (-d, 0)]
    mp = _pv(_d(P), x0)
    return Q(f'A firm\'s revenue and cost functions are R(x) = {polyF([(a, 1), (-b, 2)])} and C(x) = {polyF(C)} (in ₹). Find the profit function and the marginal profit at x = {x0}. Interpret the sign.',
             f'P(x) = {polyF(P)}; MP = {rs(mp)} ({"profit rises" if mp > 0 else "profit falls" if mp < 0 else "profit is stationary"} with one more unit)',
             f'P = R − C (1 mark); P′(x) = {polyF(_d(P))} (1 mark); value and interpretation (1 mark).')


def b4s2_explain(r):
    x0 = r.randint(10, 200)
    m = r.randint(10, 500)
    return xbank([
        (f'The marginal cost of a product is ₹{m} when {x0} units are produced. Interpret this.', f'Producing the {x0 + 1}th unit costs approximately ₹{m}.', 'MC ≈ C(x + 1) − C(x) (2 marks).'),
        ('Why does the fixed cost not appear in the marginal cost?', 'Fixed cost is a constant; its derivative is zero.', 'Derivative of a constant (2 marks).'),
        ('Explain why profit is maximum where MR = MC (with MR falling below MC after it).', 'P′ = MR − MC = 0 there and P′ changes from + to −.', 'First derivative test on P (2 marks).'),
    ])(r)


def b4s2_ar(r):
    k = r.randint(0, 2)
    c = r.randint(5, 80)
    d = r.choice(range(200, 2001, 100))
    if k == 0:
        return ar(f'For C(x) = {d} + {c}x, the marginal cost is ₹{c} at every level of output.', 'The derivative of a linear function is a constant.', 'a', f'C′(x) = {c}.')
    if k == 1:
        return ar(f'For C(x) = {d} + {c}x, the marginal cost is ₹{c + d}.', 'Marginal cost is the derivative of total cost.', 'd', f'MC = {c}; A false, R true.')
    a = r.randint(50, 200)
    return ar(f'If R(x) = {a}x − x², then MR is zero at x = {fz(Fr(a, 2))}.', 'MR = dR/dx.', 'a', f'MR = {a} − 2x = 0.')


def b4s2_case(r):
    a, b = r.randint(200, 800), r.choice([1, 2, 4, 5])
    c, d = r.randint(20, 100), r.choice(range(1000, 10001, 500))
    if a <= c:
        raise ValueError
    x0 = r.randint(5, 30)
    who = name(r)
    city = r.choice(CITIES)
    xm = Fr(a - c, 2 * b)
    return Q((f'{who} sells handmade bags in {city}. The price at which x bags can be sold is p = {a} − {co(b)}x (₹), and the cost is C(x) = {d} + {c}x (₹). '
              f'(i) Find the revenue function R(x). (ii) Find MR and MC at x = {x0}. (iii) For which x is MR = MC?'),
             f'(i) R(x) = {polyF([(a, 1), (-b, 2)])} (ii) MR = {rs(a - 2 * b * x0)}, MC = {rs(c)} (iii) x = {fz(xm)}',
             '(i) 1 mark (ii) 1 mark (iii) equate and solve (2 marks).')


def b4s2_long(r):
    terms = _cost(r)
    x0 = r.randint(5, 20)
    mc = _pv(_d(terms), x0)
    actual = _pv(terms, x0 + 1) - _pv(terms, x0)
    return Q(f'The total cost function of a firm is C(x) = {polyF(terms)} (₹). Find the marginal cost at x = {x0} and compare it with the actual cost of producing the {x0 + 1}th unit.',
             f'MC = {rs(mc)}; actual cost C({x0 + 1}) − C({x0}) = {rs(actual)}',
             f'C′(x) = {polyF(_d(terms))} (1 mark); MC({x0}) = {rs(mc)} (1 mark); C({x0 + 1}) = {fz(_pv(terms, x0 + 1))}, C({x0}) = {fz(_pv(terms, x0))} (2 marks); MC approximates the actual extra cost (1 mark).')


# ======================================================================= ch04 st4 optimisation in business

b4s4_mcq = mcqbank([
    ('Profit is maximum when …', 'MR = MC and the slope of MC exceeds the slope of MR', ['MR = 0', 'MC = 0', 'R = C'], 'Second-order condition.'),
    ('Average cost is minimum where …', 'AC = MC', ['MC = 0', 'AC = 0', 'C = 0'], 'MC cuts AC at its minimum.'),
    ('Total revenue is maximum where …', 'MR = 0', ['MR = MC', 'R = C', 'price is zero'], 'dR/dx = 0 and d²R/dx² < 0.'),
    ('The break-even point is where …', 'R(x) = C(x)', ['MR = MC', 'R(x) = 0', 'C(x) = 0'], 'No profit, no loss.'),
    ('A critical point x = c of f with f″(c) > 0 is a point of …', 'local minimum', ['local maximum', 'inflection', 'discontinuity'], 'Second derivative test.'),
])


def b4s4_mrmc(r):
    while True:
        a, b = r.randint(100, 800), r.choice([1, 2, 3, 4, 5])
        c, d = r.randint(10, 90), r.choice(range(500, 5001, 250))
        x = Fr(a - c, 2 * b)
        if x.denominator == 1 and x > 0:
            break
    P = -b * x * x + (a - c) * x - d
    if P <= 0:
        raise ValueError
    return Q(f'A company\'s revenue and cost functions are R(x) = {polyF([(a, 1), (-b, 2)])} and C(x) = {d} + {c}x (in ₹). Find the output that maximises profit and the maximum profit.', f'{fz(x)} units; {rs(P)}',
             f'P(x) = {polyF([(-b, 2), (a - c, 1), (-d, 0)])} (1 mark); P′(x) = {polyF([(-2 * b, 1), (a - c, 0)])} = 0 ⇒ x = {fz(x)} (2 marks); P″ = −{2 * b} < 0 ⇒ maximum (1 mark); P({fz(x)}) = {rs(P)} (1 mark).',
             dist3(f'{fz(x)} units; {rs(P)}', [f'{fz(Fr(a, 2 * b))} units; {rs(-b * Fr(a, 2 * b) ** 2 + (a - c) * Fr(a, 2 * b) - d)}', f'{fz(x)} units; {rs(P + d)}', f'{fz(2 * x)} units; {rs(-b * 4 * x * x + (a - c) * 2 * x - d)}']))


def b4s4_avg(r):
    a = r.choice([1, 2, 3, 4, 5, Fr(1, 2)])
    xm = r.randint(3, 30)
    c = Fr(a) * xm * xm
    if c.denominator != 1:
        raise ValueError
    b = r.randint(5, 60)
    ac = 2 * Fr(a) * xm + b
    return Q(f'The total cost of producing x units is C(x) = {polyF([(a, 2), (b, 1), (c, 0)])} (₹). Find the output at which the average cost is minimum, and the minimum average cost.', f'{xm} units; {rs(ac)}',
             f'AC = {co(a)}x + {b} + {fz(c)}/x (1 mark); d(AC)/dx = {fz(a)} − {fz(c)}/x² = 0 ⇒ x = {xm} (2 marks); second derivative {fz(2 * c)}/x³ > 0 (1 mark); AC({xm}) = {rs(ac)} (1 mark).',
             dist3(f'{xm} units; {rs(ac)}', [f'{xm * 2} units; {rs(Fr(a) * 2 * xm + b + c / (2 * xm))}', f'{xm} units; {rs(_pv([(a, 2), (b, 1), (c, 0)], xm))}', f'{fz(c / b)} units; {rs(ac + 1)}' if c % b == 0 else f'{xm + 1} units; {rs(Fr(a) * (xm + 1) + b + c / (xm + 1))}']))


def b4s4_price(r):
    while True:
        a, b = r.choice(range(200, 5001, 100)), r.choice([2, 4, 5, 10, 20, 25])
        p = Fr(a, 2 * b)
        if p.denominator == 1:
            break
    Rm = p * (a - b * p)
    who = name(r)
    return Q(f'The number of tickets sold for a show organised by {who} is x = {a} − {b}p when the price is ₹p. Find the price that maximises the revenue, and the maximum revenue.', f'₹{fz(p)}; {rs(Rm)}',
             f'R = p({a} − {b}p) = {a}p − {b}p² (1 mark); dR/dp = {a} − {2 * b}p = 0 ⇒ p = {fz(p)} (1 mark); d²R/dp² < 0, R = {rs(Rm)} (1 mark).',
             dist3(f'₹{fz(p)}; {rs(Rm)}', [f'₹{fz(Fr(a, b))}; ₹0', f'₹{fz(p)}; {rs(a * p)}', f'₹{fz(p * 2)}; {rs(2 * p * (a - 2 * b * p)) if a - 2 * b * p > 0 else "₹0"}']))


def b4s4_breakeven(r):
    while True:
        F0 = r.choice(range(2000, 50001, 1000))
        v = r.randint(20, 300)
        p = v + r.randint(10, 200)
        x = Fr(F0, p - v)
        if x.denominator == 1:
            break
    return Q(f'A product has fixed costs of ₹{F0}, a variable cost of ₹{v} per unit and sells at ₹{p} per unit. Find the break-even output.', f'{fz(x)} units',
             f'R = {p}x, C = {F0} + {v}x; R = C ⇒ x = {F0}/{p - v} = {fz(x)}.', dist3(f'{fz(x)} units', [f'{F0 // p} units', f'{F0 // v} units' if F0 // v else '1 unit', f'{fz(x) if False else int(x) + 10} units']))


def b4s4_ar(r):
    k = r.randint(0, 2)
    a, b = r.randint(100, 400), r.choice([1, 2, 4])
    if k == 0:
        return ar(f'For R(x) = {a}x − {b}x², revenue is maximum at x = {fz(Fr(a, 2 * b))}.', 'At a maximum, dR/dx = 0 and d²R/dx² < 0.', 'a', f'R′ = {a} − {2 * b}x = 0, R″ = −{2 * b}.'.replace('−1x', '−x'))
    if k == 1:
        return ar('If P′(c) = 0, then P has a maximum at x = c.', 'A local maximum needs P″(c) < 0 (or a + to − change of sign of P′).', 'd', 'A stationary point may be a minimum or an inflection; A false, R true.')
    return ar('At the output where average cost is least, average cost equals marginal cost.', 'd(AC)/dx = (MC − AC)/x.', 'a', 'd(AC)/dx = 0 ⇒ MC = AC.')


def b4s4_case(r):
    while True:
        a, b = r.randint(200, 900), r.choice([1, 2, 5])
        c, d = r.randint(20, 120), r.choice(range(1000, 8001, 500))
        x = Fr(a - c, 2 * b)
        if x.denominator == 1 and x > 0 and -b * x * x + (a - c) * x - d > 0:
            break
    P = -b * x * x + (a - c) * x - d
    who = name(r)
    return Q((f'{who} runs a juice bar in {r.choice(CITIES)}. Daily revenue and cost (in ₹) for x glasses are R(x) = {polyF([(a, 1), (-b, 2)])} and C(x) = {d} + {c}x. '
              f'(i) Write the profit function. (ii) Find the number of glasses that maximises profit. (iii) Find the maximum profit.'),
             f'(i) P(x) = {polyF([(-b, 2), (a - c, 1), (-d, 0)])} (ii) {fz(x)} (iii) {rs(P)}', '(i) 1 mark (ii) P′ = 0 and P″ < 0 (2 marks) (iii) 1 mark.')


# ======================================================================= ch05 st4 consumer and producer surplus

b5s4_mcq = mcqbank([
    ('Consumer surplus at the market price p₀ (quantity x₀) for demand p = D(x) is …', '∫ from 0 to x₀ of D(x) dx − p₀x₀', ['p₀x₀ − ∫ from 0 to x₀ of D(x) dx', '∫ from 0 to p₀ of D(x) dx', 'D(x₀) − p₀'], 'Area between the demand curve and the price line.'),
    ('Producer surplus at price p₀ (quantity x₀) for supply p = S(x) is …', 'p₀x₀ − ∫ from 0 to x₀ of S(x) dx', ['∫ from 0 to x₀ of S(x) dx − p₀x₀', '∫ from 0 to x₀ of S(x) dx', 'p₀ − S(0)'], 'Area between the price line and the supply curve.'),
    ('Market equilibrium occurs where …', 'demand equals supply', ['demand is maximum', 'price is zero', 'supply is zero'], 'D(x) = S(x).'),
    ('Consumer surplus measures …', 'the benefit consumers get by paying less than they were willing to pay', ['the profit of producers', 'the total money spent', 'the tax collected'], 'Interpretation.'),
    ('Producer surplus measures …', 'the gain producers get by selling at a price higher than they were willing to accept', ['consumer savings', 'the cost of production', 'the total revenue'], 'Interpretation.'),
])


def _dem(r):
    a = r.choice(range(20, 201, 5))
    b = r.choice([1, 2, 3, 4, 5, Fr(1, 2)])
    return a, Fr(b)


def b5s4_cs(r):
    a, b = _dem(r)
    k = r.randint(0, 1)
    if k == 0:
        x0 = r.randint(2, 30)
        p0 = a - b * x0
        if p0 <= 0:
            raise ValueError
        cs = b * x0 * x0 / 2
        stem = f'The demand function for a product is p = {a} − {co(b)}x. Find the consumer surplus when the quantity demanded is {x0} units.'
        key = f'p₀ = {a} − {fpar(b)}({x0}) = {fz(p0)} (1 mark); CS = ∫ from 0 to {x0} of ({a} − {co(b)}x) dx − {fz(p0)} × {x0} = {fz(a * x0 - b * x0 * x0 / 2)} − {fz(p0 * x0)} = {fz(cs)} (2 marks).'
    else:
        c = r.choice([Fr(1, 2), 1, 2])
        x0 = r.randint(2, 8)
        p0 = a - Fr(c) * x0 * x0
        if p0 <= 0:
            raise ValueError
        cs = a * x0 - Fr(c) * x0 ** 3 / 3 - p0 * x0
        stem = f'The demand function for a product is p = {a} − {co(c)}x². Find the consumer surplus when the market price corresponds to x₀ = {x0} units.'
        key = f'p₀ = {fz(p0)} (1 mark); CS = ∫ from 0 to {x0} of ({a} − {co(c)}x²) dx − {fz(p0)} × {x0} = {fz(cs)} (2 marks).'
    return Q(stem, f'₹{fz(cs)}' if cs.denominator == 1 else f'₹{fz(cs)} ≈ {rs(cs)}', key, dist3(f'₹{fz(cs)}' if cs.denominator == 1 else f'₹{fz(cs)} ≈ {rs(cs)}', [f'₹{fz(cs * 2)}', f'₹{fz(p0 * x0)}', f'₹{fz(cs + p0)}']))


def b5s4_ps(r):
    c = r.randint(2, 40)
    d = Fr(r.choice([1, 2, 3, 4, Fr(1, 2)]))
    x0 = r.randint(2, 30)
    p0 = c + d * x0
    ps = d * x0 * x0 / 2
    return Q(f'The supply function of a commodity is p = {c} + {co(d)}x. Find the producer surplus when the quantity supplied is {x0} units.', f'₹{fz(ps)}',
             f'p₀ = {fz(p0)} (1 mark); PS = {fz(p0)} × {x0} − ∫ from 0 to {x0} of ({c} + {co(d)}x) dx = {fz(p0 * x0)} − {fz(c * x0 + d * x0 * x0 / 2)} = {fz(ps)} (2 marks).',
             dist3(f'₹{fz(ps)}', [f'₹{fz(ps * 2)}', f'₹{fz(p0 * x0)}', f'₹{fz(c * x0 + ps)}']))


def b5s4_eq(r):
    while True:
        a, b = _dem(r)
        c = r.randint(2, 30)
        d = Fr(r.choice([1, 2, 3, Fr(1, 2)]))
        x0 = (a - c) / (b + d)
        if x0.denominator == 1 and x0 > 0:
            break
    p0 = a - b * x0
    cs, ps = b * x0 * x0 / 2, d * x0 * x0 / 2
    ans = f'x₀ = {fz(x0)}, p₀ = ₹{fz(p0)}; CS = ₹{fz(cs)}, PS = ₹{fz(ps)}'
    return Q(f'The demand and supply functions are p = {a} − {co(b)}x and p = {c} + {co(d)}x. Find the equilibrium quantity and price, and the consumer and producer surplus at equilibrium.', ans,
             f'Equate: {a} − {co(b)}x = {c} + {co(d)}x ⇒ x₀ = {fz(x0)}, p₀ = {fz(p0)} (2 marks); CS = ∫(D − p₀) dx = {fz(cs)} (1.5 marks); PS = ∫(p₀ − S) dx = {fz(ps)} (1.5 marks).',
             dist3(ans, [f'x₀ = {fz(x0)}, p₀ = ₹{fz(p0)}; CS = ₹{fz(ps)}, PS = ₹{fz(cs)}', f'x₀ = {fz(x0)}, p₀ = ₹{fz(p0)}; CS = ₹{fz(2 * cs)}, PS = ₹{fz(2 * ps)}', f'x₀ = {fz(p0)}, p₀ = ₹{fz(x0)}; CS = ₹{fz(cs)}, PS = ₹{fz(ps)}']))


def b5s4_ar(r):
    a, b = _dem(r)
    x0 = r.randint(2, 20)
    if a - b * x0 <= 0:
        raise ValueError
    k = r.randint(0, 2)
    if k == 0:
        return ar(f'For the demand p = {a} − {co(b)}x, the consumer surplus at x₀ = {x0} is ₹{fz(b * x0 * x0 / 2)}.', 'For a linear demand, CS is the area of the triangle between the demand line and the price line.', 'a', f'½ × {x0} × {fz(b * x0)}.')
    if k == 1:
        return ar('Consumer surplus can be negative.', 'Consumers never pay more than the price they are willing to pay at the market quantity.', 'd', 'The demand curve lies above the price line up to x₀; A false, R true.')
    return ar('At equilibrium, consumer surplus and producer surplus are always equal.', 'Both are areas between a curve and the equilibrium price line.', 'd', 'They are equal only for special slopes; A false, R true.')


def b5s4_case(r):
    while True:
        a, b = _dem(r)
        c = r.randint(2, 30)
        d = Fr(r.choice([1, 2, 3]))
        x0 = (a - c) / (b + d)
        if x0.denominator == 1 and x0 > 0:
            break
    p0 = a - b * x0
    who = name(r)
    return Q((f'In {who}\'s economics project on the onion market in {r.choice(CITIES)}, demand is p = {a} − {co(b)}x and supply is p = {c} + {co(d)}x (p in ₹ per kg, x in quintals). '
              f'(i) Find the equilibrium quantity and price. (ii) Find the consumer surplus. (iii) Find the producer surplus.'),
             f'(i) x₀ = {fz(x0)}, p₀ = ₹{fz(p0)} (ii) ₹{fz(b * x0 * x0 / 2)} (iii) ₹{fz(d * x0 * x0 / 2)}', '(i) 1 mark (ii) 1.5 marks (iii) 1.5 marks.')


def b5s4_explain(r):
    return xbank([
        ('Explain, using a demand curve, what consumer surplus represents.', 'The area between the demand curve and the market price line from 0 to x₀.', 'Diagram/area description (2 marks).'),
        ('Why is producer surplus calculated as p₀x₀ − ∫ from 0 to x₀ of S(x) dx?', 'p₀x₀ is the revenue received; the integral is the minimum producers would accept.', 'Both parts explained (2 marks).'),
        ('What happens to consumer surplus if the market price rises (demand unchanged)?', 'It decreases, because the price line moves up and the area under the demand curve above it shrinks.', 'Direction with reason (2 marks).'),
    ])(r)


# ======================================================================= ch06 st1 formation of differential equations

def b6s1_form(r):
    k = r.randint(0, 6)
    a = r.randint(2, 6)
    if k == 0:
        return Q(f'Form the differential equation of the family y = Ae^({a}x), where A is an arbitrary constant.', f'dy/dx = {a}y', f'dy/dx = {a}Ae^({a}x) = {a}y (eliminate A).', [f'dy/dx = y', f'dy/dx = {a}x', f'd²y/dx² = {a}y'])
    if k == 1:
        return Q('Form the differential equation of the family of straight lines y = mx + c (m, c arbitrary).', 'd²y/dx² = 0', 'dy/dx = m, then d²y/dx² = 0 (two constants, so order 2).', ['dy/dx = 0', 'dy/dx = m', 'x dy/dx = y'])
    if k == 2:
        return Q('Form the differential equation of the family of lines through the origin, y = mx.', 'x dy/dx = y', 'dy/dx = m = y/x.', ['dy/dx = 0', 'd²y/dx² = 0', 'y dy/dx = x'])
    if k == 3:
        return Q(f'Form the differential equation of the family y = Ax{str(a).translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))}.', f'x dy/dx = {a}y', f'dy/dx = {a}Ax^{a - 1} = {a}y/x.', [f'dy/dx = {a}y', f'x dy/dx = y', f'dy/dx = {a}x'])
    if k == 4:
        m, n = r.sample([-3, -2, -1, 1, 2, 3], 2)
        s, p = m + n, m * n
        eq = 'd²y/dx²' + (f' − {co(s)}dy/dx' if s > 0 else f' + {co(-s)}dy/dx' if s < 0 else '') + term(p, 'y') + ' = 0'
        return Q(f'Form the differential equation of the family y = A{ex(m)} + B{ex(n)}.', eq, 'Differentiate twice and eliminate A and B (order 2).',
                 dist3(eq, [f'dy/dx{term(p, "y")} = 0', f'd²y/dx²{term(s, "dy/dx")}{term(p, "y")} = 0', f'd²y/dx²{term(-p, "y")} = 0', f'd²y/dx²{term(-s, "dy/dx")}{term(-p, "y")} = 0', f'd²y/dx²{term(p + 1, "y")} = 0']))
    if k == 5:
        return Q('Form the differential equation of the family of circles x² + y² = a² (a arbitrary).', 'x + y dy/dx = 0', '2x + 2y dy/dx = 0.', ['x − y dy/dx = 0', 'dy/dx = x/y', 'x² + y² = 0'])
    return Q('Form the differential equation of the family of parabolas y² = 4ax (a arbitrary).', '2x dy/dx = y', '2y dy/dx = 4a = y²/x ⇒ 2x dy/dx = y.', ['x dy/dx = 2y', 'y dy/dx = 2a', 'dy/dx = 2a'])


def b6s1_ar(r):
    k = r.randint(0, 1)
    n = r.randint(1, 3)
    if k == 0:
        return ar(f'The differential equation of a family of curves with {n} arbitrary constant{"s" if n > 1 else ""} has order {n}.', 'Each differentiation is used to eliminate one arbitrary constant.', 'a', 'Number of constants = order.')
    return ar('The family y = mx + c gives the differential equation dy/dx = m.', 'The equation of a family must not contain the arbitrary constants.', 'd', 'Eliminate m by differentiating again: d²y/dx² = 0; A false, R true.')


# ======================================================================= ch06 st3 growth and decay

def b6s3_mcq(r):
    return mcqbank([
        ('If a quantity grows at a rate proportional to itself, dP/dt = kP with k > 0, then P(t) = …', 'P₀eᵏᵗ', ['P₀ + kt', 'P₀e⁻ᵏᵗ', 'kP₀t'], 'Variables separable.'),
        ('In radioactive decay dN/dt = −λN, the half-life is …', '(log 2)/λ', ['λ log 2', '2/λ', 'λ/2'], 'N₀/2 = N₀e^(−λT).'),
        ('Money compounded continuously at r% p.a. satisfies …', 'dA/dt = (r/100)A', ['dA/dt = r', 'dA/dt = A/r', 'A = Pr t/100'], 'Rate proportional to the amount.'),
        ('In dP/dt = kP, a negative k represents …', 'decay', ['growth', 'a constant population', 'oscillation'], 'Sign of k.'),
        ('A population that doubles in T years under exponential growth has k = …', '(log 2)/T', ['2/T', 'T/log 2', 'log T'], '2 = e^(kT).'),
    ])(r)


def b6s3_ratio(r):
    P0 = r.choice(range(1000, 50001, 1000))
    m = r.choice([Fr(6, 5), Fr(5, 4), Fr(3, 2), Fr(2), Fr(11, 10), Fr(9, 8)])
    t = r.randint(2, 10)
    n = r.choice([2, 3])
    P1 = P0 * m
    if P1.denominator != 1:
        raise ValueError
    Pn = P0 * m ** n
    what = r.choice(['bacteria in a culture', 'members of a co-operative society', 'users of a payment app', 'trees in a plantation'])
    ans = f'{num(float(Pn), 1)}'
    return Q(f'The number of {what} grows at a rate proportional to the number present. It increases from {P0} to {fz(P1)} in {t} years. Find the number after {n * t} years.', ans,
             f'dP/dt = kP ⇒ P = {P0}eᵏᵗ (1 mark); e^({t}k) = {fz(m)} (1 mark); P({n * t}) = {P0}(e^({t}k))^{n} = {P0} × ({fz(m)})^{n} = {ans} (1 mark).',
             dist3(ans, [num(float(P0 + n * (P1 - P0)), 1), num(float(P0 * m * n), 1), num(float(P0 * m ** (n + 1)), 1)]))


def b6s3_half(r):
    T = r.choice([5, 8, 10, 12, 20, 25, 30, 50, 100, 1600])
    n = r.randint(2, 5)
    A = r.choice([64, 80, 96, 128, 160, 200, 256, 320, 400, 640])
    left = Fr(A, 2 ** n)
    sub = r.choice(['radium', 'a radioactive isotope', 'a medicine in the bloodstream', 'a pesticide in the soil'])
    return Q(f'{sub.capitalize()} decays at a rate proportional to the amount present, with a half-life of {T} years. If {A} g is present now, how much remains after {n * T} years?', f'{fz(left)} g',
             f'N = N₀e^(−λt) and e^(−λ{T}) = 1/2 (1 mark); after {n} half-lives N = {A} × (1/2)^{n} = {fz(left)} g (2 marks).'.replace('−λ' + str(T), '−' + str(T) + 'λ'),
             dist3(f'{fz(left)} g', [f'{fz(Fr(A, 2 * n))} g', f'{A - n * A // 4} g' if A - n * A // 4 > 0 else f'{A // 3} g', f'{fz(Fr(A, 2 ** (n + 1)))} g']))


def b6s3_double(r):
    k = r.choice([Fr(1, 20), Fr(1, 25), Fr(1, 10), Fr(1, 50), Fr(2, 25), Fr(1, 40), Fr(1, 5)])
    T = math.log(2) / float(k)
    return Q(f'A population grows according to dP/dt = {fz(k)}P (t in years). Find the time taken for it to double. (Use log 2 = 0.6931.)', f'{num(T, 2)} years',
             f'P = P₀e^({fz(k)}t); 2 = e^({fz(k)}t) ⇒ t = log 2/{fpar(k)} = 0.6931 × {fz(1 / k)} = {num(T, 2)} (3 marks).',
             dist3(f'{num(T, 2)} years', [f'{num(float(2 / k), 2)} years', f'{num(float(1 / k), 2)} years', f'{num(0.6931 * float(k), 4)} years']))


def b6s3_cont(r):
    P0 = r.choice(range(10000, 200001, 5000))
    rate, t = r.choice([(5, 4), (5, 6), (4, 5), (6, 5), (8, 5), (10, 5), (5, 10), (10, 3), (4, 10), (8, 10)])
    e = Fr(rate * t, 100)
    val = round(P0 * math.exp(float(e)), 2)
    ev = round(math.exp(float(e)), 4)
    return Q(f'{inr(P0)} is invested at {rate}% per annum compounded continuously. Form the differential equation and find the amount after {t} years. (Use e^{num(float(e))} = {ev}.)', rs(P0 * ev),
             f'dA/dt = ({rate}/100)A ⇒ A = {P0}e^({fz(Fr(rate, 100))}t) (2 marks); A({t}) = {P0} × {ev} = {rs(P0 * ev)} (1 mark).',
             dist3(rs(P0 * ev), [rs(P0 * (1 + rate * t / 100)), rs(P0 * (1 + rate / 100) ** t), rs(P0 * ev - P0)]))


def b6s3_ar(r):
    T = r.choice([5, 10, 20])
    k = r.randint(0, 2)
    if k == 0:
        return ar(f'A substance with half-life {T} years falls to one-quarter of its amount in {2 * T} years.', 'Exponential decay halves the amount in every half-life.', 'a', 'Two half-lives.')
    if k == 1:
        return ar(f'A population growing exponentially that doubles in {T} years will quadruple in {4 * T} years.', 'Exponential growth multiplies the population by the same factor in equal time intervals.', 'd', f'It quadruples in {2 * T} years; A false, R true.')
    return ar('The solution of dP/dt = kP is P = P₀eᵏᵗ.', 'Separating variables gives log P = kt + C.', 'a', 'Integrate and use P(0) = P₀.')


def b6s3_case(r):
    P0 = r.choice(range(2000, 20001, 1000))
    m = r.choice([Fr(3, 2), Fr(5, 4), Fr(6, 5), Fr(2)])
    t = r.choice([2, 3, 4, 5])
    P1 = P0 * m
    if P1.denominator != 1:
        raise ValueError
    who = name(r)
    return Q((f'{who} studies the number of registered start-ups in {r.choice(CITIES)}, which grows at a rate proportional to the number present. There were {P0} start-ups in 2020 and {fz(P1)} in {2020 + t}. '
              f'(i) Write the differential equation. (ii) Express the number t years after 2020. (iii) Estimate the number in {2020 + 2 * t}.'),
             f'(i) dP/dt = kP (ii) P = {P0}eᵏᵗ with eᵏ^{t} = {fz(m)}, i.e. P = {P0}({fz(m)})^(t/{t}) (iii) {num(float(P0 * m * m), 1)}',
             '(i) 1 mark (ii) 1 mark (iii) 2 marks.')


def b6s3_long(r):
    N0 = r.choice([100, 200, 400, 500, 800, 1000])
    p = r.choice([10, 20, 25, 50])
    h = r.choice([1, 2, 3, 5])
    rem = Fr(100 - p, 100)
    n = r.choice([2, 3])
    left = N0 * rem ** n
    return Q(f'A radioactive material loses {p}% of its mass every {h} year{"s" if h > 1 else ""}, the rate of decay being proportional to the mass present. Starting with {N0} mg, form and solve the differential equation, and find the mass left after {n * h} years.',
             f'{num(float(left), 3)} mg',
             f'dN/dt = −λN ⇒ N = {N0}e^(−λt) (2 marks); e^(−{h}λ) = {fz(rem)} (1 mark); N({n * h}) = {N0} × ({fz(rem)})^{n} = {num(float(left), 3)} mg (2 marks).'.replace('e^(−1λ)', 'e^(−λ)'),
             dist3(f'{num(float(left), 3)} mg', [f'{num(float(N0 * (1 - n * Fr(p, 100))), 3)} mg', f'{num(float(N0 * rem), 3)} mg', f'{num(float(N0 * rem ** (n + 1)), 3)} mg']))


# ======================================================================= ch05 additions (algebraic, exponential and logarithmic only)

b5s1_mcq = mcqbank([
    ('∫ eˣ dx = …', 'eˣ + C', ['xeˣ + C', 'eˣ⁺¹/(x + 1) + C', 'eˣ/x + C'], 'Standard integral.'),
    ('∫ (1/x) dx = …', 'log|x| + C', ['−1/x² + C', 'x⁰ + C', '1/x² + C'], 'Standard integral (x ≠ 0).'),
    ('∫ aˣ dx = …', 'aˣ/log a + C', ['aˣ log a + C', 'xaˣ⁻¹ + C', 'aˣ⁺¹/(x + 1) + C'], 'Standard integral (a > 0, a ≠ 1).'),
    ('∫ xⁿ dx = …, n ≠ −1', 'xⁿ⁺¹/(n + 1) + C', ['nxⁿ⁻¹ + C', 'xⁿ⁺¹ + C', 'xⁿ/(n + 1) + C'], 'Power rule.'),
    ('∫ k dx, k a constant, equals …', 'kx + C', ['k + C', '0', 'k²/2 + C'], 'Derivative of kx is k.'),
    ('∫ √x dx = …', '(2/3)x^(3/2) + C', ['(1/2)x^(−1/2) + C', '(3/2)x^(3/2) + C', '2√x + C'], 'n = 1/2.'),
    ('If d/dx F(x) = f(x), then ∫ f(x) dx = …', 'F(x) + C', ['F′(x) + C', 'f′(x) + C', 'xF(x) + C'], 'Integration is anti-differentiation.'),
])


def _term(r, used):
    k = r.choice([t for t in ('exp', 'inv', 'sqrt', 'ax', 'ekx', 'pow') if t not in used])
    c = r.choice([1, 2, 3, 4, 5, -2, -3])
    if k == 'exp':
        return k, f'{co(c)}eˣ', f'{co(c)}eˣ', (lambda x, c=c: c * math.exp(x)), (lambda x, c=c: c * math.exp(x))
    if k == 'inv':
        return k, f'{c}/x', f'{co(c)}log|x|', (lambda x, c=c: c / x), (lambda x, c=c: c * math.log(abs(x)))
    if k == 'sqrt':
        return k, f'{co(c)}√x', f'{co(Fr(2 * c, 3))}x^(3/2)', (lambda x, c=c: c * math.sqrt(x)), (lambda x, c=c: 2 * c / 3 * x ** 1.5)
    if k == 'ax':
        a = r.choice([2, 3, 5, 10])
        cc = co(c) + (' × ' if abs(c) != 1 else '')
        return k, f'{cc}{a}ˣ', f'{cc}{a}ˣ/log {a}', (lambda x, c=c, a=a: c * a ** x), (lambda x, c=c, a=a: c * a ** x / math.log(a))
    if k == 'ekx':
        a = r.choice([2, 3, -1, -2, 4])
        return k, f'{co(c)}{ex(a)}', f'{co(Fr(c, a))}{ex(a)}', (lambda x, c=c, a=a: c * math.exp(a * x)), (lambda x, c=c, a=a: c / a * math.exp(a * x))
    n = r.choice([2, 3, 4, 5])
    return k, mono(c, n, first=True), mono(Fr(c, n + 1), n + 1, first=True), (lambda x, c=c, n=n: c * x ** n), (lambda x, c=c, n=n: c / (n + 1) * x ** (n + 1))


def _join(parts):
    out = parts[0]
    for p in parts[1:]:
        out += (' − ' + p[1:]) if p.startswith('−') else (' + ' + p)
    return out


def b5s1_std(r):
    used, ts = set(), []
    for _ in range(r.choice([2, 3])):
        t = _term(r, used)
        used.add(t[0])
        ts.append(t)
    integ = _join([t[1] for t in ts])
    ans = _join([t[2] for t in ts]) + ' + C'
    f = lambda x: sum(t[3](x) for t in ts)
    Fx = lambda x: sum(t[4](x) for t in ts)
    return Q(f'Find ∫ ({integ}) dx.', ans, 'Integrate term by term using the standard integrals.',
             dist3(ans, [_join([t[1] for t in ts]) + ' + C', _join([t[2] for t in ts[:-1]] + [ts[-1][1]]) + ' + C', _join([t[2] for t in reversed(ts)]).replace('log|x|', '1/x²') + ' + C']), _i=(f, Fx, 1.3))


def b5s1_cost(r):
    a, b = r.randint(5, 60), Fr(r.choice([2, 4, 6, 1, 3]))
    c = Fr(r.choice([0, 3, 6, 1]))
    F0 = r.choice(range(500, 10001, 250))
    n = r.randint(5, 30)
    mc = [(c, 2), (b, 1), (a, 0)] if c else [(b, 1), (a, 0)]
    C = [(c / 3, 3), (b / 2, 2), (a, 1), (F0, 0)] if c else [(b / 2, 2), (a, 1), (F0, 0)]
    val = _pv(C, n)
    return Q(f'The marginal cost of producing x units is MC = {polyF(mc)} (₹ per unit) and the fixed cost is ₹{F0}. Find the total cost function and the cost of producing {n} units.', f'C(x) = {polyF(C)}; C({n}) = {rs(val)}',
             f'C(x) = ∫ MC dx = {polyF(C[:-1])} + K (1 mark); C(0) = {F0} ⇒ K = {F0} (1 mark); C({n}) = {rs(val)} (1 mark).',
             dist3(f'C(x) = {polyF(C)}; C({n}) = {rs(val)}', [f'C(x) = {polyF(C[:-1])}; C({n}) = {rs(val - F0)}', f'C(x) = {polyF(mc)} + {F0}; C({n}) = {rs(_pv(mc, n) + F0)}', f'C(x) = {polyF(C)}; C({n}) = {rs(val + F0)}']))


def b5s1_rev(r):
    a, b = r.randint(50, 400), r.choice([1, 2, 3, 4, 6])
    R = [(Fr(-b, 2), 2), (a, 1)]
    return Q(f'The marginal revenue function of a product is MR = {a} − {co(b)}x. Find the total revenue function and the demand function (R(0) = 0).', f'R(x) = {polyF([(a, 1), (Fr(-b, 2), 2)])}; p = {polyF([(a, 0), (Fr(-b, 2), 1)])}',
             f'R = ∫ MR dx = {polyF([(a, 1), (Fr(-b, 2), 2)])} + K, R(0) = 0 ⇒ K = 0 (2 marks); p = R/x (1 mark).',
             dist3(f'R(x) = {polyF([(a, 1), (Fr(-b, 2), 2)])}; p = {polyF([(a, 0), (Fr(-b, 2), 1)])}', [f'R(x) = {polyF([(a, 1), (-b, 2)])}; p = {polyF([(a, 0), (-b, 1)])}', f'R(x) = {polyF([(a, 1), (Fr(-b, 2), 2)])}; p = {a} − {co(b)}x', f'R(x) = {a} − {co(b)}x; p = {a}']))


def b5s1_ar(r):
    k = r.randint(0, 2)
    a = r.choice([2, 3, 4, 5])
    if k == 0:
        return ar(f'∫ e^({a}x) dx = e^({a}x)/{a} + C.', f'd/dx e^({a}x) = {a}e^({a}x).', 'a', 'Differentiate the answer.')
    if k == 1:
        return ar('∫ dx/x = log x + C for all x ≠ 0.', 'd/dx log|x| = 1/x for x ≠ 0.', 'd', 'For x < 0 we need log|x|; A false, R true.')
    return ar(f'The total cost is the integral of the marginal cost plus the fixed cost.', 'C′(x) = MC and C(0) is the fixed cost.', 'a', 'The constant of integration is the fixed cost.')


def b5s1_case(r):
    a, b = r.randint(10, 80), r.choice([2, 4, 6])
    F0 = r.choice(range(1000, 8001, 500))
    p = r.randint(a + 20, a + 200)
    n = r.randint(5, 25)
    C = [(Fr(b, 2), 2), (a, 1), (F0, 0)]
    who = name(r)
    return Q((f'{who}\'s workshop in {r.choice(CITIES)} has marginal cost MC = {a} + {b}x (₹) for x chairs, and a fixed cost of ₹{F0}. Each chair sells for ₹{p}. '
              f'(i) Find the total cost function. (ii) Find the cost of making {n} chairs. (iii) Find the profit on {n} chairs.'),
             f'(i) C(x) = {polyF(C)} (ii) {rs(_pv(C, n))} (iii) {rs(p * n - _pv(C, n))}', '(i) integrate and use C(0) (1 mark) (ii) 1 mark (iii) R − C (2 marks).')


b5s2_mcq = mcqbank([
    ('∫ f′(x)/f(x) dx = …', 'log|f(x)| + C', ['f(x) + C', '1/f(x) + C', 'log|f′(x)| + C'], 'Substitution t = f(x).'),
    ('In integration by parts, ∫ u v dx = …', 'u∫v dx − ∫(u′∫v dx) dx', ['u′∫v dx − ∫u v′ dx', '∫u dx ∫v dx', 'uv − ∫u′v′ dx'], 'Formula.'),
    ('By the ILATE rule, the first function in ∫ x eˣ dx is …', 'x', ['eˣ', 'either', 'dx'], 'Algebraic before exponential.'),
    ('∫ eˣ(f(x) + f′(x)) dx = …', 'eˣ f(x) + C', ['eˣ f′(x) + C', 'f(x) + C', 'eˣ + f(x) + C'], 'Standard result.'),
    ('To integrate 1/((x − a)(x − b)), a ≠ b, we use …', 'partial fractions', ['by parts', 'substitution x = a', 'a standard trigonometric form'], 'Proper rational function with distinct linear factors.'),
    ('∫ 2x/(x² + 1) dx = …', 'log(x² + 1) + C', ['2 log x + C', '1/(x² + 1) + C', 'x²/(x² + 1) + C'], 'Numerator is the derivative of the denominator.'),
])

b5s3_mcq = mcqbank([
    ('∫ from a to b of f(x) dx = …', '−∫ from b to a of f(x) dx', ['∫ from b to a of f(x) dx', '0', '2∫ from 0 to a of f(x) dx'], 'Interchanging the limits changes the sign.'),
    ('∫ from a to a of f(x) dx = …', '0', ['f(a)', '1', 'a'], 'Equal limits.'),
    ('∫ from 0 to a of f(x) dx = …', '∫ from 0 to a of f(a − x) dx', ['∫ from 0 to a of f(x − a) dx', '∫ from 0 to 2a of f(x) dx', '−∫ from 0 to a of f(x) dx'], 'Property P4.'),
    ('If F′(x) = f(x), then ∫ from a to b of f(x) dx = …', 'F(b) − F(a)', ['F(a) − F(b)', 'f(b) − f(a)', 'F(b) + F(a)'], 'Second fundamental theorem.'),
    ('∫ from 1 to e of (1/x) dx = …', '1', ['e', '0', 'e − 1'], 'log e − log 1.'),
    ('∫ from 0 to 1 of eˣ dx = …', 'e − 1', ['e', '1', 'e + 1'], 'e¹ − e⁰.'),
])


def b5s3_exp(r):
    k = r.randint(0, 2)
    if k == 0:
        a, b = sorted(r.sample(range(1, 10), 2))
        return Q(f'Evaluate ∫ from {a} to {b} of (1/x) dx.', f'log({fz(Fr(b, a))})', f'[log x] from {a} to {b} = log {b} − log {a} = log({fz(Fr(b, a))}).'.replace('log 1 ', '0 '),
                 [f'log {b - a}', f'{fz(Fr(1, a) - Fr(1, b))}', f'log({fz(Fr(a, b))})'], _v=(lambda: math.log(b / a), lambda: math.log(b) - math.log(a)))
    if k == 1:
        c = r.choice([1, 2, 3])
        ans = f'(e^{c} − 1)/{c}'.replace('e^1', 'e').replace('/1', '') if c > 1 else 'e − 1'
        return Q(f'Evaluate ∫ from 0 to 1 of e^({c}x) dx.'.replace('e^(1x)', 'eˣ'), ans, f'[e^({c}x)/{c}] from 0 to 1 = {ans}.'.replace('/1]', ']').replace('e^(1x)', 'eˣ'), [f'e^{c} − 1', f'{c}(e^{c} − 1)', f'e^{c}/{c}'] if c > 1 else ['e', '1', 'e + 1'])
    a, b = sorted(r.sample(range(0, 6), 2))
    c1, c2 = r.randint(1, 5), r.randint(1, 9)
    val = Fr(c1, 2) * (b * b - a * a) + c2 * (b - a)
    return Q(f'Evaluate ∫ from {a} to {b} of ({c1}x + {c2}) dx as the change in an antiderivative.'.replace('(1x', '(x'), fz(val),
             f'Antiderivative {mono(Fr(c1, 2), 2, first=True)} + {c2}x; F({b}) − F({a}) = {fz(val)}.', [fz(val + 1), fz(c1 * (b - a)), fz(val * 2)])


def b5s3_cost(r):
    a, b = r.randint(5, 80), r.choice([1, 2, 4, 6])
    x1 = r.randint(5, 40)
    x2 = x1 + r.randint(5, 40)
    inc = a * (x2 - x1) + Fr(b, 2) * (x2 * x2 - x1 * x1)
    return Q(f'The marginal cost of a product is MC = {a} + {co(b)}x (₹ per unit). Find the increase in total cost when output rises from {x1} to {x2} units.', rs(inc),
             f'Increase = ∫ from {x1} to {x2} of ({a} + {co(b)}x) dx (2 marks) = [{a}x + {co(Fr(b, 2))}x²] from {x1} to {x2} = {rs(inc)} (3 marks).',
             dist3(rs(inc), [rs(a + b * x2 - a - b * x1), rs(a * (x2 - x1)), rs(inc + a), rs(Fr(b, 2) * (x2 * x2 - x1 * x1))]))


def b5s3_ar(r):
    a, b = sorted(r.sample(range(1, 9), 2))
    k = r.randint(0, 1)
    if k == 0:
        return ar(f'∫ from {a} to {b} of 3x² dx = {b ** 3 - a ** 3}.', 'If F′ = f, then ∫ from a to b of f(x) dx = F(b) − F(a).', 'a', f'F = x³: {b ** 3} − {a ** 3}.')
    return ar(f'∫ from {b} to {a} of 2x dx = {b * b - a * a}.', 'Interchanging the limits of a definite integral changes its sign.', 'd', f'The value is {a * a - b * b}; A false, R true.')


def b5s3_case(r):
    a, b = r.randint(100, 500), r.choice([2, 4, 6])
    x1 = r.randint(5, 20)
    x2 = x1 + r.randint(5, 20)
    inc = a * (x2 - x1) - Fr(b, 2) * (x2 * x2 - x1 * x1)
    if inc <= 0 or a - b * x2 <= 0:
        raise ValueError
    who = name(r)
    return Q((f'For {who}\'s online store, the marginal revenue from selling x units is MR = {a} − {b}x (₹). '
              f'(i) Write the definite integral for the extra revenue when sales rise from {x1} to {x2} units. (ii) Evaluate it. (iii) Find the total revenue from the first {x1} units.'),
             f'(i) ∫ from {x1} to {x2} of ({a} − {b}x) dx (ii) {rs(inc)} (iii) {rs(a * x1 - Fr(b, 2) * x1 * x1)}', '(i) 1 mark (ii) 2 marks (iii) 1 mark.')


# ======================================================================= ch06 st2 additions (variable separable, no trigonometry)

b6s2_mcq = mcqbank([
    ('The general solution of dy/dx = y is …', 'y = Ceˣ', ['y = x + C', 'y = eˣ + C', 'y = Cx'], 'dy/y = dx.'),
    ('The equation dy/dx = f(x)g(y) is solved by …', 'separating the variables: dy/g(y) = f(x) dx', ['integrating factor', 'substituting y = vx', 'differentiating again'], 'Variable separable form.'),
    ('The general solution of dy/dx = x/y is …', 'y² − x² = C', ['y = x + C', 'xy = C', 'y² + x² = C'], 'y dy = x dx.'),
    ('The number of arbitrary constants in the general solution of a first-order differential equation is …', '1', ['0', '2', 'equal to the degree'], 'Order 1 ⇒ one constant.'),
    ('A particular solution is obtained from the general solution by …', 'giving particular values to the arbitrary constants using given conditions', ['differentiating it', 'adding a constant', 'squaring both sides'], 'Definition.'),
])


def b6s2_gen(r):
    k = r.randint(0, 3)
    if k == 0:
        a, b = r.randint(1, 6), r.randint(-5, 6)
        P = [(Fr(a, 2), 2), (b, 1)] if b else [(Fr(a, 2), 2)]
        ans = f'y = Ce^({polyF(P)})'
        return Q(f'Find the general solution of dy/dx = ({poly([a, b])})y.', ans, f'dy/y = ({poly([a, b])}) dx ⇒ log|y| = {polyF(P)} + K.',
                 dist3(ans, [f'y = {polyF(P)} + C', f'y = Ce^({poly([a, b])})', f'y = Ce^({polyF([(a, 2), (b, 1)] if b else [(a, 2)])})']),
                 _ode=(lambda x, y: (a * x + b) * y, lambda x: 2.0 * math.exp(float(_pv(P, x))), 0.4))
    if k == 1:
        n = r.choice([1, 2, 3])
        c = r.randint(1, 6)
        P = [(Fr(2 * c, n + 1), n + 1)]
        ans = f'y² = {polyF(P)} + C'
        xs = 'x' if n == 1 else 'x' + str(n).translate(str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹'))
        return Q(f'Find the general solution of y dy/dx = {co(c)}{xs}.', ans, f'y dy = {co(c)}{xs} dx ⇒ y²/2 = {polyF([(Fr(c, n + 1), n + 1)])} + K.',
                 dist3(ans, [f'y = {polyF([(Fr(c, n + 1), n + 1)])} + C', f'y² = {polyF([(Fr(c, n + 1), n + 1)])} + C', f'y² = {co(c * n)}x{"" if n - 1 <= 1 else str(n - 1).translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))} + C' if n > 1 else f'y² = {2 * c} + C']),
                 _ode=(lambda x, y: c * x ** n / y, lambda x: math.sqrt(float(_pv(P, x)) + 5), 0.7))
    if k == 2:
        a, b = r.randint(1, 4), r.randint(1, 4)
        ans = f'{co(Fr(1, a))}{ex(a)} + {co(Fr(1, b))}{ex(-b)} = C'
        return Q(f'Find the general solution of dy/dx = e^({a}x + {b}y).'.replace('(1x', '(x').replace('+ 1y', '+ y'), ans,
                 f'e^(−{b}y) dy = e^({a}x) dx (1 mark) ⇒ −{co(Fr(1, b))}e^(−{b}y) = {co(Fr(1, a))}e^({a}x) + K (1 mark).'.replace('(−1y)', '(−y)').replace('(1x)', '(x)'),
                 dist3(ans, [f'{ex(a)} + {ex(-b)} = C', f'{co(Fr(1, a))}{ex(a)} − {co(Fr(1, b))}{ex(-b)} = C', f'{ex(a)} = {ex(b)} + C']))
    n = r.choice([0, 1, 2])
    c = r.randint(1, 5)
    P = [(Fr(c, n + 1), n + 1)]
    ans = f'−1/y = {polyF(P)} + C'
    xs = '' if n == 0 else ('x' if n == 1 else 'x²')
    return Q(f'Find the general solution of dy/dx = {co(c) if xs else c}{xs}y².'.replace('= 1y²', '= y²'), ans, f'dy/y² = {co(c) if xs else c}{xs} dx ⇒ −1/y = {polyF(P)} + C.'.replace('= 1 dx', '= dx'),
             dist3(ans, [f'1/y = {polyF(P)} + C', f'y³/3 = {polyF(P)} + C', f'log|y| = {polyF(P)} + C']),
             _ode=(lambda x, y: c * x ** n * y * y, lambda x: -1 / (float(_pv(P, x)) - 9), 0.5))


def b6s2_part(r):
    a = r.choice([1, 2, 3, -1, -2])
    y0 = r.choice([1, 2, 3, 4, 5])
    ans = f'y = {y0}{ex(a)}'.replace('y = 1e', 'y = e')
    return Q(f'Find the particular solution of dy/dx = {co(a)}y, given y = {y0} when x = 0.', ans, f'log|y| = {co(a)}x + C (1 mark); y(0) = {y0} ⇒ C = log {y0} (1 mark); y = {y0}{ex(a)} (1 mark).'.replace('C = log 1', 'C = 0'),
             dist3(ans, [f'y = {y0} + {co(a)}x', f'y = {ex(a)} + {y0 - 1}' if y0 > 1 else f'y = {ex(-a)}', f'y = {y0}{ex(-a)}']),
             _ode=(lambda x, y: a * y, lambda x: y0 * math.exp(a * x), 0.3))


def b6s2_ar(r):
    k = r.randint(0, 1)
    a = r.randint(2, 6)
    if k == 0:
        return ar(f'y = Ce^({a}x) is the general solution of dy/dx = {a}y.', 'Separating variables gives log|y| = kx + c, i.e. y = Ceᵏˣ.', 'a', f'k = {a}.')
    return ar('The general solution of dy/dx = x/y is x² + y² = C.', 'y dy = x dx integrates to y² = x² + C.', 'd', 'The solution is y² − x² = C; A false, R true.')


# ======================================================================= table

NT = no_trig

FAMILIES = {
    S + '04-st1': reuse('05-st5', filt=NT, skip=('c5s5_second',)) + [F('C1', 'D2', 'mcq', b4s1_mcq), F('C2', 'D2', 'numerical', b4s1_poly), F('C3', 'D3', 'numerical', b4s1_exp), F('C2', 'D3', 'mcq', b4s1_ar, kinds=('ar',)),
                                                                     F('C3', 'D3', 'multi_step', b4s1_show), F('C4', 'D3', 'case', b4s1_case), F('C4', 'D4', 'multi_step', b4s1_exp), F('C1', 'D1', 'short', b4s1_poly)],
    S + '04-st2': [F('C1', 'D2', 'mcq', b4s2_mcq), F('C1', 'D1', 'short', b4s2_mc), F('C2', 'D2', 'explain', b4s2_explain), F('C2', 'D3', 'mcq', b4s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', b4s2_mr), F('C3', 'D3', 'multi_step', b4s2_avg), F('C3', 'D4', 'multi_step', b4s2_mp), F('C4', 'D3', 'case', b4s2_case),
                   F('C4', 'D4', 'long', b4s2_long), F('C4', 'D5', 'long', b4s2_long), F('C3', 'D1', 'numerical', b4s2_mc), F('C2', 'D2', 'numerical', b4s2_mr)],
    S + '04-st3': reuse('06-st2', filt=NT) + reuse('06-st3', filt=NT),
    S + '04-st4': [F('C1', 'D2', 'mcq', b4s4_mcq), F('C1', 'D1', 'short', b4s4_breakeven), F('C2', 'D2', 'numerical', b4s4_price), F('C2', 'D3', 'mcq', b4s4_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', b4s4_breakeven), F('C3', 'D3', 'multi_step', b4s4_price), F('C3', 'D4', 'long', b4s4_mrmc), F('C4', 'D3', 'case', b4s4_case),
                   F('C4', 'D4', 'long', b4s4_avg), F('C4', 'D5', 'long', b4s4_mrmc)] + reuse('06-st4', filt=NT, skip=('c6s4_proof', 'c6s4_mcq', 'c6s4_ar', 'c6s4_case', 'c6s4_abs')),
    S + '05-st1': reuse('07-st1', filt=NT) + [F('C1', 'D2', 'mcq', b5s1_mcq), F('C2', 'D2', 'numerical', b5s1_std), F('C2', 'D3', 'mcq', b5s1_ar, kinds=('ar',)), F('C3', 'D3', 'multi_step', b5s1_cost),
                                              F('C4', 'D3', 'case', b5s1_case), F('C4', 'D4', 'multi_step', b5s1_rev), F('C3', 'D2', 'numerical', b5s1_std), F('C4', 'D5', 'long', b5s1_cost, marks=5)],
    S + '05-st2': reuse('07-st2', filt=NT) + reuse('07-st3', filt=NT) + reuse('07-st4', filt=NT) + [F('C1', 'D2', 'mcq', b5s2_mcq)],
    S + '05-st3': reuse('07-st5', filt=NT) + [F('C1', 'D2', 'mcq', b5s3_mcq), F('C2', 'D2', 'numerical', b5s3_exp), F('C2', 'D3', 'mcq', b5s3_ar, kinds=('ar',)), F('C3', 'D4', 'long', b5s3_cost),
                                              F('C4', 'D4', 'long', b5s3_cost), F('C4', 'D3', 'case', b5s3_case), F('C3', 'D3', 'numerical', b5s3_exp), F('C4', 'D5', 'long', b5s3_cost)],
    S + '05-st4': [F('C1', 'D2', 'mcq', b5s4_mcq), F('C1', 'D1', 'short', b5s4_ps), F('C2', 'D2', 'explain', b5s4_explain), F('C2', 'D3', 'mcq', b5s4_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', b5s4_cs), F('C3', 'D3', 'multi_step', b5s4_cs), F('C3', 'D4', 'long', b5s4_eq), F('C4', 'D3', 'case', b5s4_case),
                   F('C4', 'D4', 'long', b5s4_eq), F('C4', 'D5', 'long', b5s4_eq), F('C3', 'D1', 'numerical', b5s4_ps), F('C2', 'D2', 'numerical', b5s4_ps)],
    S + '06-st1': reuse('09-st1', filt=NT) + [F('C1', 'D2', 'mcq', b6s2_mcq), F('C2', 'D2', 'numerical', b6s1_form), F('C3', 'D3', 'numerical', b6s1_form), F('C2', 'D3', 'mcq', b6s1_ar, kinds=('ar',)), F('C4', 'D4', 'numerical', b6s1_form)],
    S + '06-st2': reuse('09-st2', filt=NT) + [F('C1', 'D2', 'mcq', b6s2_mcq), F('C2', 'D2', 'numerical', b6s2_gen), F('C2', 'D3', 'mcq', b6s2_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', b6s2_part),
                                              F('C3', 'D3', 'numerical', b6s2_gen), F('C2', 'D2', 'numerical', b6s2_part)],
    S + '06-st3': [F('C1', 'D2', 'mcq', b6s3_mcq), F('C1', 'D1', 'short', b6s3_half), F('C2', 'D2', 'numerical', b6s3_double), F('C2', 'D3', 'mcq', b6s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', b6s3_ratio), F('C3', 'D3', 'multi_step', b6s3_cont), F('C3', 'D4', 'long', b6s3_long), F('C4', 'D3', 'case', b6s3_case),
                   F('C4', 'D4', 'long', b6s3_long), F('C4', 'D5', 'multi_step', b6s3_ratio), F('C3', 'D1', 'numerical', b6s3_half)],
    S + '13-st1': reuse('12-st1'),
    S + '13-st2': reuse('12-st2'),
    S + '13-st3': reuse('12-st3'),
}
