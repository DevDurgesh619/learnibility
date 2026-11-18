"""CBSE class 11 Applied Mathematics (241) families, chapters 10-14 (correlation and regression, interest and
annuities, taxation, straight lines, circles and parabola). All answers are computed in code; where a tax
rate or tariff is needed it is given in the question, so no item depends on a particular year's rates."""
from __future__ import annotations

import math
from fractions import Fraction as Fr

from qbank import F, ar, mcq, num, sup, name, two_names, inr, CITIES  # noqa: F401
from g11_physics_util import pool_mcq, pool_ar, pool_txt, term_mcq, tf_mcq  # noqa: F401
from g11_applied_maths_a import Q, fs, lin, mixed, nd, reuse, S

# ======================================================== ch10 Correlation and regression


def _pairs(r, n=None, sign=None, nice=True):
    """Small bivariate data set with integer means."""
    for _ in range(400):
        n = n or r.choice([5, 6, 7])
        xs = r.sample(range(1, 20), n)
        b = r.choice([1, 2, -1, -2, 3]) if sign is None else sign * r.choice([1, 2, 3])
        a = r.randint(5, 30) if b > 0 else r.randint(45, 70)
        ys = [a + b * x + r.randint(-3, 3) for x in xs]
        if nice and (sum(xs) % n or sum(ys) % n):
            continue
        if len(set(ys)) < n or min(ys) <= 0:
            continue
        return xs, ys
    raise ValueError


def _stats(xs, ys):
    n = len(xs)
    mx, my = Fr(sum(xs), n), Fr(sum(ys), n)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    return mx, my, sxy, sxx, syy


def _rv(sxy, sxx, syy):
    return float(sxy) / math.sqrt(float(sxx) * float(syy))


def _tab(xs, ys, lx='X', ly='Y'):
    return f'{lx}: {", ".join(map(str, xs))}\n{ly}: {", ".join(map(str, ys))}'


c10s1_type = pool_mcq([
    ('If the points of a scatter diagram lie exactly on a straight line rising from left to right, the correlation is', 'perfect positive', ['perfect negative', 'zero', 'low positive'], 'r = +1.'),
    ('If the points of a scatter diagram lie exactly on a straight line falling from left to right, the correlation is', 'perfect negative', ['perfect positive', 'zero', 'high positive'], 'r = −1.'),
    ('If the points of a scatter diagram show no pattern at all, the correlation is', 'zero (no correlation)', ['perfect positive', 'perfect negative', 'high negative'], 'No linear relationship.'),
    ('The correlation between the price of a commodity and the quantity demanded is usually', 'negative', ['positive', 'zero', 'perfect positive'], 'Law of demand.'),
    ('The correlation between the height and the weight of children is usually', 'positive', ['negative', 'zero', 'perfect negative'], 'They tend to increase together.'),
    ('Points of a scatter diagram that cluster closely around a falling line indicate', 'high degree of negative correlation', ['high degree of positive correlation', 'no correlation', 'low positive correlation'], 'Close clustering ⇒ high degree.'),
])

c10s1_tf = tf_mcq('correlation and scatter diagrams', [
    'A scatter diagram gives a visual idea of the direction and closeness of a relationship.', 'Correlation measures the degree of linear relationship between two variables.',
    'Correlation does not by itself prove that one variable causes the other.', 'Bivariate data consist of pairs of observations on two variables.',
    'When both variables move in the same direction, the correlation is positive.'],
    ['A scatter diagram gives the exact value of the correlation coefficient.', 'High correlation always means one variable causes the other.',
     'When both variables move in the same direction, the correlation is negative.', 'Correlation can be found from data on only one variable.', 'Zero correlation means the variables are identical.'])

PAIRS_EX = [('the price of petrol', 'the demand for petrol', 'negative', 'higher prices reduce demand'), ('rainfall in a season', 'the sale of umbrellas', 'positive', 'more rain, more umbrellas sold'),
            ('the temperature in summer', 'the sale of ice cream', 'positive', 'hotter days increase demand'), ('the number of hours studied', 'marks obtained', 'positive', 'more study usually improves marks'),
            ('the speed of a vehicle', 'the time taken for a fixed journey', 'negative', 'time = distance/speed'), ('shoe size', 'IQ score of adults', 'zero', 'no logical relationship'),
            ('income of families', 'expenditure on luxuries', 'positive', 'higher income allows more luxury spending'), ('the age of a car', 'its resale value', 'negative', 'value falls as the car gets older'),
            ('the supply of a crop in a market', 'its price', 'negative', 'a bumper crop lowers the price')]


def c10s1_expect(r):
    a, b, t, why = r.choice(PAIRS_EX)
    return {'stem': f'State the type of correlation you would expect between {a} and {b}. Give a reason.', 'answer': f'{t.capitalize()} correlation: {why}.',
            'key': f'Type ({t}) (1); reason (1).', 'distractors': [x.capitalize() + ' correlation' for x in ('positive', 'negative', 'zero') if x != t] + ['Perfect positive correlation']}


def c10s1_dir(r):
    sg = r.choice([1, -1])
    xs, ys = _pairs(r, sign=sg, nice=False)
    mx, my, sxy, sxx, syy = _stats(xs, ys)
    t = 'positive' if sxy > 0 else 'negative'
    return Q(f'Plot a scatter diagram (mentally or on paper) for the data below and state the direction of correlation.\n{_tab(xs, ys)}', f'{t} correlation',
             f'As X increases, Y tends to {"increase" if sxy > 0 else "decrease"}; Σ(x − x̄)(y − ȳ) is {"positive" if sxy > 0 else "negative"}, so the correlation is {t}.',
             [f'{"negative" if t == "positive" else "positive"} correlation', 'zero correlation', 'perfect positive correlation' if t == 'negative' else 'perfect negative correlation'])


def c10s1_cov(r):
    xs, ys = _pairs(r, n=5)
    mx, my, sxy, _, _ = _stats(xs, ys)
    cov = sxy / 5
    return Q(f'Find the covariance between X and Y for the data\n{_tab(xs, ys)}', num(float(cov), 2),
             f'x̄ = {fs(mx)}, ȳ = {fs(my)}; Σ(x − x̄)(y − ȳ) = {fs(sxy)}; cov = {fs(sxy)}/5 = {num(float(cov), 2)}.', [num(float(sxy), 2), num(float(-cov), 2), num(float(cov) * 2, 2)])


def c10s1_ar(r):
    return pool_ar([
        ('A high correlation between ice-cream sales and drowning cases does not mean that ice cream causes drowning.', 'Correlation does not imply causation; both may depend on a third factor such as hot weather.', 'a', 'R explains A.'),
        ('A scatter diagram can show whether the relationship between two variables is linear or curved.', 'It plots each pair of observations as a point.', 'a', 'The pattern of the points reveals the shape.'),
        ('If the points of a scatter diagram rise from left to right, the correlation is negative.', 'Negative correlation means the variables move in opposite directions.', 'd', 'A is false: rising points show positive correlation. R is true.'),
    ])(r)


def c10s1_case(r):
    xs, ys = _pairs(r, n=6, sign=1)
    who = name(r)
    return {'stem': (f'{who}, a shop owner in {r.choice(CITIES)}, records the advertisement spend (X, in thousand ₹) and the sales (Y, in lakh ₹) for six months:\n{_tab(xs, ys)}\n'
                     f'(i) What kind of data is this? (1)\n(ii) What does a scatter diagram of these data suggest? (1)\n(iii) Can {who} conclude that advertising causes higher sales? Give one reason. (2)'),
            'answer': '(i) Bivariate data (ii) positive correlation – sales tend to rise with advertisement spend (iii) Not necessarily: correlation does not prove causation; festivals or seasons may affect both',
            'key': '(i) 1 (ii) direction from the pattern (1) (iii) correct conclusion (1) with reason (1).'}


# st2 Karl Pearson's coefficient

c10s2_formula = pool_mcq([
    ("Karl Pearson's coefficient of correlation r always lies between", '−1 and 1', ['0 and 1', '−∞ and ∞', '0 and ∞'], '|r| ≤ 1.'),
    ("Karl Pearson's coefficient r equals", 'cov(X, Y)/(σₓσᵧ)', ['σₓσᵧ/cov(X, Y)', 'cov(X, Y)/σₓ', 'σₓ/σᵧ'], 'Definition.'),
    ('If r = 0, the variables are', 'uncorrelated (no linear relationship)', ['perfectly correlated', 'independent in every case', 'negatively correlated'], 'r measures linear association only.'),
    ('The correlation coefficient is', 'independent of change of origin and scale (up to sign)', ['dependent on the units of measurement', 'affected by change of origin', 'always positive'], 'Standard property.'),
])


def c10s2_prop(r):
    r0 = Fr(r.choice([-9, -8, -7, -6, -5, -4, 3, 4, 5, 6, 7, 8, 9]), 10)
    a, c = r.choice([2, 3, -2, -3, 5, 4]), r.choice([2, -1, 3, -4, 5])
    b, d = r.randint(-9, 9), r.randint(-9, 9)
    v = r0 if a * c > 0 else -r0
    return Q(f'If the correlation coefficient between X and Y is {num(float(r0))}, find the correlation coefficient between U = {lin(a, b, "X")} and V = {lin(c, d, "Y")}.', num(float(v)),
             f'r is unchanged by change of origin and scale except for sign; the scale factors {a} and {c} have {"the same" if a * c > 0 else "opposite"} signs, so r(U, V) = {num(float(v))}.',
             nd(num(float(v)), [num(float(-v)), num(float(r0 * a * c)), num(float(r0 * a / c)) if abs(r0 * a / c) <= 1 else '0', '0']))


def c10s2_cov(r):
    sx, sy = r.choice([2, 3, 4, 5, 6, 8]), r.choice([2, 3, 4, 5, 6, 10])
    rv = Fr(r.choice([-9, -8, -6, -5, -4, 4, 5, 6, 8, 9]), 10)
    cov = rv * sx * sy
    return Q(f'For a bivariate data set, cov(X, Y) = {num(float(cov))}, σₓ = {sx} and σᵧ = {sy}. Find the correlation coefficient r.', num(float(rv)),
             f'r = cov/(σₓσᵧ) = {num(float(cov))}/({sx} × {sy}) = {num(float(rv))}.', nd(num(float(rv)), [num(float(-rv)), num(float(cov / sx), 2), num(float(cov / (sx + sy)), 2)]))


def c10s2_sums(r):
    xs, ys = _pairs(r, n=r.choice([5, 6, 8, 10]), nice=False)
    n = len(xs)
    Sx, Sy = sum(xs), sum(ys)
    Sxx, Syy, Sxy = sum(x * x for x in xs), sum(y * y for y in ys), sum(x * y for x, y in zip(xs, ys))
    num_ = n * Sxy - Sx * Sy
    den = math.sqrt((n * Sxx - Sx * Sx) * (n * Syy - Sy * Sy))
    v = num_ / den
    return Q(f'For {n} pairs of observations: Σx = {Sx}, Σy = {Sy}, Σx² = {Sxx}, Σy² = {Syy}, Σxy = {Sxy}. Find Karl Pearson\'s coefficient of correlation (to 3 decimal places).', f'{v:.3f}'.replace('-', '−'),
             f'r = (nΣxy − ΣxΣy)/√[(nΣx² − (Σx)²)(nΣy² − (Σy)²)] = {num_}/√({n * Sxx - Sx * Sx} × {n * Syy - Sy * Sy}) = {v:.3f}.'.replace('-', '−'),
             [f'{-v:.3f}'.replace('-', '−'), f'{v * 0.8:.3f}'.replace('-', '−'), f'{min(0.999, abs(v) + 0.1) * (1 if v > 0 else -1):.3f}'.replace('-', '−')])


def c10s2_data(r):
    xs, ys = _pairs(r, n=r.choice([5, 6, 7]))
    mx, my, sxy, sxx, syy = _stats(xs, ys)
    v = _rv(sxy, sxx, syy)
    return Q(f"Calculate Karl Pearson's coefficient of correlation for the data below and interpret it.\n{_tab(xs, ys)}", f'r = {v:.3f}'.replace('-', '−') + f' ({_interp(v)})',
             f'x̄ = {fs(mx)}, ȳ = {fs(my)} (1); Σdx dy = {fs(sxy)}, Σdx² = {fs(sxx)}, Σdy² = {fs(syy)} (2); r = Σdxdy/√(Σdx²Σdy²) = {v:.3f} (1); interpretation (1).'.replace('-', '−'),
             [f'r = {-v:.3f}'.replace('-', '−') + f' ({_interp(-v)})', f'r = {v * 0.7:.3f}'.replace('-', '−') + f' ({_interp(v * 0.7)})'])


def _interp(v):
    a = abs(v)
    d = 'perfect' if a > 0.999 else ('high degree of' if a >= 0.75 else ('moderate' if a >= 0.5 else ('low' if a > 0.1 else 'negligible')))
    return f'{d} {"positive" if v > 0 else "negative"} correlation' if a > 0.1 else 'practically no linear correlation'


def c10s2_interp(r):
    v = r.choice([0.92, 0.85, 0.8, 0.65, 0.55, 0.3, 0.2, -0.95, -0.88, -0.6, -0.52, -0.25, 1.0, -1.0])
    ans = _interp(v)
    others = list(dict.fromkeys(_interp(x) for x in [0.92, 0.6, 0.3, -0.92, -0.6, -0.3, 1.0, -1.0, 0.05] if _interp(x) != ans))
    return mcq(f'The coefficient of correlation between two variables is {num(v)}. This indicates', ans, r.sample(others, 3), f'|r| = {num(abs(v))} and its sign give: {ans}.', r)


def c10s2_findsd(r):
    rv = Fr(r.choice([4, 5, 6, 8]), 10)
    sx = r.choice([2, 3, 4, 5])
    sy = r.choice([3, 4, 5, 6, 10])
    cov = rv * sx * sy
    return Q(f'If r = {num(float(rv))}, cov(X, Y) = {num(float(cov))} and the variance of X is {sx * sx}, find the standard deviation of Y.', str(sy),
             f'σₓ = √{sx * sx} = {sx}; σᵧ = cov/(rσₓ) = {num(float(cov))}/({num(float(rv))} × {sx}) = {sy}.', [str(sy * sy), str(sx), num(float(cov / sx))])


def c10s2_ar(r):
    return pool_ar([
        ('The correlation coefficient between X and 2X + 5 is 1.', 'Y = 2X + 5 is an exact increasing linear relation.', 'a', 'Perfect positive linear relation.'),
        ('A correlation coefficient of 1.2 shows a very strong relationship.', '−1 ≤ r ≤ 1 for any data.', 'd', 'A is false: r cannot exceed 1. R is true.'),
        ('r does not change if all values of X are converted from rupees to paise.', 'r is independent of change of scale.', 'a', 'Multiplying by 100 is a change of scale.'),
        ('r = 0 always means there is no relationship between X and Y.', 'r measures only the linear relationship.', 'd', 'A is false: a curved relationship may still exist. R is true.'),
    ])(r)


def c10s2_explain(r):
    v = r.choice([0.9, -0.8, 0.4, -0.3, 0.0])
    return {'stem': f'A researcher finds r = {num(v)} between hours of television watched per week and marks scored by students in a school. Interpret this value, and state one limitation of the conclusion.',
            'answer': f'{_interp(v).capitalize()}. Limitation: correlation does not prove causation; other factors may influence both, and r measures only linear association.',
            'key': 'Interpretation of sign and size (1); one valid limitation (1).'}


def c10s2_case(r):
    xs, ys = _pairs(r, n=5)
    mx, my, sxy, sxx, syy = _stats(xs, ys)
    v = _rv(sxy, sxx, syy)
    return {'stem': (f'The monthly rainfall (X, cm) and the yield of a crop (Y, quintals per hectare) recorded by a farmers\' cooperative are:\n{_tab(xs, ys)}\n'
                     f'(i) Find the means of X and Y. (1)\n(ii) Find Σ(x − x̄)(y − ȳ). (1)\n(iii) Find r and interpret it. (2)'),
            'answer': f'(i) x̄ = {fs(mx)}, ȳ = {fs(my)} (ii) {fs(sxy)} (iii) r = {v:.3f}, {_interp(v)}'.replace('-', '−'),
            'key': '(i) 1 (ii) 1 (iii) value (1), interpretation (1).'}


# st3 Spearman's rank correlation


def _rank(vals, desc=True):
    order = sorted(vals, reverse=desc)
    return [order.index(v) + 1 for v in vals]


def c10s3_ranks(r):
    n = r.randint(5, 9)
    R1 = list(range(1, n + 1))
    r.shuffle(R1)
    R2 = R1[:]
    for _ in range(r.randint(1, 3)):
        i, j = r.sample(range(n), 2)
        R2[i], R2[j] = R2[j], R2[i]
    if r.random() < 0.3:
        R2 = list(range(1, n + 1))
        r.shuffle(R2)
    D2 = sum((a - b) ** 2 for a, b in zip(R1, R2))
    v = 1 - Fr(6 * D2, n * (n * n - 1))
    return Q(f'Two judges ranked {n} contestants in a debate competition as follows:\nJudge I: {", ".join(map(str, R1))}\nJudge II: {", ".join(map(str, R2))}\nFind Spearman\'s rank correlation coefficient.',
             f'{fs(v)} ≈ {num(float(v), 3)}', f'ΣD² = {D2}; ρ = 1 − 6ΣD²/(n(n² − 1)) = 1 − {6 * D2}/{n * (n * n - 1)} = {fs(v)} ≈ {num(float(v), 3)}.',
             [num(float(1 - Fr(D2, n * (n * n - 1))), 3), num(float(-v), 3), num(float(1 - Fr(6 * D2, n * n * n)), 3)])


def c10s3_scores(r):
    n = r.randint(5, 8)
    xs = r.sample(range(30, 100), n)
    ys = r.sample(range(30, 100), n)
    if r.random() < 0.6:
        ys = sorted(ys, reverse=True)
        idx = sorted(range(n), key=lambda i: -xs[i])
        tmp = [0] * n
        for k_, i in enumerate(idx):
            tmp[i] = ys[k_]
        ys = tmp
        i, j = r.sample(range(n), 2)
        ys[i], ys[j] = ys[j], ys[i]
    Rx, Ry = _rank(xs), _rank(ys)
    D2 = sum((a - b) ** 2 for a, b in zip(Rx, Ry))
    v = 1 - Fr(6 * D2, n * (n * n - 1))
    return Q(f'Find the rank correlation coefficient between the marks in Accountancy (X) and Applied Mathematics (Y) of {n} students:\n{_tab(xs, ys, "X", "Y")}',
             f'{num(float(v), 3)}', f'Ranks of X: {", ".join(map(str, Rx))}; ranks of Y: {", ".join(map(str, Ry))} (2); ΣD² = {D2} (1); ρ = 1 − 6 × {D2}/({n}({n * n} − 1)) = {num(float(v), 3)} (2).',
             [num(float(-v), 3), num(float(1 - Fr(D2, n * (n * n - 1))), 3), num(float(v) / 2, 3)])


def c10s3_d2(r):
    n = r.randint(6, 12)
    D2 = r.randint(4, n * (n * n - 1) // 6)
    v = 1 - Fr(6 * D2, n * (n * n - 1))
    if v.denominator > 60:
        raise ValueError
    return Q(f'The rank correlation coefficient for {n} pairs of ranks is {fs(v)}. Find the sum of the squares of the rank differences.', str(D2),
             f'{fs(v)} = 1 − 6ΣD²/({n} × {n * n - 1}) ⇒ ΣD² = (1 − {fs(v)}) × {n * (n * n - 1)}/6 = {D2}.', [str(D2 * 2), str(D2 + n), str(n * (n * n - 1) // 6)])


def c10s3_err(r):
    n = r.choice([8, 9, 10, 11])
    D2 = r.randint(30, n * (n * n - 1) // 6 - 10)
    w, c = r.sample([0, 1, 2, 3, 4, 5, 6, 7], 2)
    D2c = D2 - w * w + c * c
    v0 = 1 - Fr(6 * D2, n * (n * n - 1))
    v1 = 1 - Fr(6 * D2c, n * (n * n - 1))
    return Q(f'The rank correlation coefficient for {n} students was found to be {num(float(v0), 4)}. Later it was found that the difference in ranks for one student was wrongly taken as {w} instead of {c}. Find the correct rank correlation coefficient.',
             num(float(v1), 4), f'Original ΣD² = (1 − ρ)n(n² − 1)/6 = {D2} (2). Corrected ΣD² = {D2} − {w}² + {c}² = {D2c} (1). ρ = 1 − 6 × {D2c}/{n * (n * n - 1)} = {num(float(v1), 4)} (2).',
             [num(float(v0), 4), num(float(1 - Fr(6 * (D2 - w + c), n * (n * n - 1))), 4), num(float(-v1), 4)])


c10s3_formula = pool_mcq([
    ("Spearman's rank correlation coefficient (no ties) is", '1 − 6ΣD²/(n(n² − 1))', ['1 − ΣD²/(n(n² − 1))', '6ΣD²/(n(n² − 1))', '1 − 6ΣD/(n(n² − 1))'], 'D = difference of ranks.'),
    ('Rank correlation is most useful when the data are', 'qualitative attributes that can only be ranked, such as beauty or honesty', ['all equal', 'measured in the same units only', 'missing'], 'Ranks replace measurements.'),
    ('If two judges give identical ranks to all contestants, the rank correlation is', '1', ['0', '−1', '0.5'], 'ΣD² = 0.'),
    ('If the ranks given by two judges are in exactly reverse order, the rank correlation is', '−1', ['1', '0', '−0.5'], 'ΣD² is maximum.'),
])


def c10s3_ar(r):
    return pool_ar([
        ('Rank correlation can be used to compare judges in a beauty contest.', 'Qualities like beauty cannot be measured but can be ranked.', 'a', 'R explains A.'),
        ('ΣD in rank correlation is always 0.', 'The sum of ranks given by each judge is the same, n(n + 1)/2.', 'a', 'R explains A.'),
        ("Spearman's ρ can exceed 1 when judges agree strongly.", 'ρ lies between −1 and 1.', 'd', 'A is false. R is true.'),
    ])(r)


def c10s3_explain(r):
    n = r.choice([5, 6, 7, 8])
    return {'stem': f'Explain why ΣD must be zero when {n} items are ranked by two judges, and how this helps check your working.',
            'answer': f'Both judges use the ranks 1 to {n}, each summing to {n * (n + 1) // 2}, so ΣD = Σ(R₁ − R₂) = 0; a non-zero ΣD shows an error in ranking or subtraction.',
            'key': 'Reason (1); use as a check (1).'}


def c10s3_case(r):
    n = 6
    R1 = list(range(1, n + 1))
    r.shuffle(R1)
    R2 = R1[:]
    i, j = r.sample(range(n), 2)
    R2[i], R2[j] = R2[j], R2[i]
    D2 = sum((a - b) ** 2 for a, b in zip(R1, R2))
    v = 1 - Fr(6 * D2, n * (n * n - 1))
    return {'stem': (f'At an inter-school dance competition in {r.choice(CITIES)}, two judges ranked six teams:\nJudge A: {", ".join(map(str, R1))}\nJudge B: {", ".join(map(str, R2))}\n'
                     f'(i) Why is rank correlation suitable here? (1)\n(ii) Find ΣD². (1)\n(iii) Find ρ and comment on the agreement between the judges. (2)'),
            'answer': f'(i) Dance performance cannot be measured, only ranked (ii) {D2} (iii) ρ = {fs(v)} ≈ {num(float(v), 3)}; {_interp(float(v))}, the judges largely agree',
            'key': '(i) 1 (ii) 1 (iii) value (1) comment (1).'}


def c10s1_cov4(r):
    xs, ys = _pairs(r, n=5)
    mx, my, sxy, sxx, syy = _stats(xs, ys)
    v = _rv(sxy, sxx, syy)
    return Q(f'For the data below, find cov(X, Y) and the correlation coefficient r. What would the scatter diagram look like?\n{_tab(xs, ys)}',
             f'cov = {num(float(sxy / 5), 2)}; r = {v:.3f}; points {"rising" if v > 0 else "falling"} from left to right, {_interp(v)}'.replace('-', '−'),
             f'x̄ = {fs(mx)}, ȳ = {fs(my)} (1); cov = Σdxdy/n = {fs(sxy)}/5 (1); r = Σdxdy/√(Σdx²Σdy²) = {v:.3f} (1); description (1).'.replace('-', '−'))


def c10s2_combo(r):
    sx, sy = r.choice([(2, 3), (3, 4), (4, 5), (2, 5), (5, 6)])
    rv = Fr(r.choice([-8, -6, -5, 4, 5, 6, 8]), 10)
    cov = rv * sx * sy
    a, c = r.choice([2, 3, -2, 5]), r.choice([-1, 2, -3, 4])
    v2 = rv if a * c > 0 else -rv
    return Q(f'For two variables, cov(X, Y) = {num(float(cov), 2)}, var(X) = {sx * sx} and var(Y) = {sy * sy}. Find r(X, Y). Hence find the correlation coefficient between U = {lin(a, 7, "X")} and V = {lin(c, -4, "Y")}.',
             f'r(X, Y) = {num(float(rv))}; r(U, V) = {num(float(v2))}', f'r = cov/(σₓσᵧ) = {num(float(cov), 2)}/({sx} × {sy}) = {num(float(rv))} (2); change of origin and scale keeps |r|, sign changes if a·c < 0: {num(float(v2))} (1).',
             [f'r(X, Y) = {num(float(rv))}; r(U, V) = {num(float(-v2))}', f'r(X, Y) = {num(float(cov / (sx * sx * sy * sy)), 3)}; r(U, V) = {num(float(v2))}', f'r(X, Y) = {num(float(-rv))}; r(U, V) = {num(float(-v2))}'])


def c10s3_three(r):
    n = 6
    base = list(range(1, n + 1))
    r.shuffle(base)
    J = [base[:]]
    for sw in (1, 3):
        x = base[:]
        for _ in range(sw):
            i, j = r.sample(range(n), 2)
            x[i], x[j] = x[j], x[i]
        J.append(x)
    rho = {}
    for a, b in ((0, 1), (0, 2), (1, 2)):
        d2 = sum((p - q) ** 2 for p, q in zip(J[a], J[b]))
        rho[(a, b)] = 1 - Fr(6 * d2, n * (n * n - 1))
    best = max(rho, key=rho.get)
    if list(rho.values()).count(rho[best]) > 1:
        raise ValueError
    lab = ['I', 'II', 'III']
    return Q(f'Three judges ranked six entries in a science exhibition:\nJudge I: {", ".join(map(str, J[0]))}\nJudge II: {", ".join(map(str, J[1]))}\nJudge III: {", ".join(map(str, J[2]))}\n'
             f'Using rank correlation, find which pair of judges has the nearest approach to common judgement.',
             f'Judges {lab[best[0]]} and {lab[best[1]]} (ρ = {fs(rho[best])})', '; '.join(f'ρ({lab[a]}, {lab[b]}) = {fs(v)}' for (a, b), v in rho.items()) + ' (1 mark each); the largest ρ shows the closest agreement (1).',
             [f'Judges {lab[a]} and {lab[b]} (ρ = {fs(v)})' for (a, b), v in rho.items() if (a, b) != best])


# st4 regression


def c10s4_coef(r):
    rv = Fr(r.choice([4, 5, 6, 8, -6, -5, -8]), 10)
    sx, sy = r.choice([2, 3, 4, 5]), r.choice([3, 4, 6, 8, 10])
    which = r.choice(['yx', 'xy'])
    v = rv * sy / sx if which == 'yx' else rv * sx / sy
    return Q(f'Given r = {num(float(rv))}, σₓ = {sx} and σᵧ = {sy}, find the regression coefficient b{"ᵧₓ" if which == "yx" else "ₓᵧ"}.', num(float(v), 3),
             f'b{"ᵧₓ = rσᵧ/σₓ" if which == "yx" else "ₓᵧ = rσₓ/σᵧ"} = {num(float(rv))} × {sy if which == "yx" else sx}/{sx if which == "yx" else sy} = {num(float(v), 3)}.',
             nd(num(float(v), 3), [num(float(rv * sx / sy if which == 'yx' else rv * sy / sx), 3), num(float(-v), 3), num(float(rv * sx * sy), 3)]))


def c10s4_r(r):
    for _ in range(100):
        a, b = Fr(r.randint(1, 16), 10), Fr(r.randint(1, 16), 10)
        prod = a * b
        s = math.isqrt(prod.numerator * 100 // prod.denominator) if (prod * 100).denominator == 1 else None
        if s and s * s == prod * 100 and prod <= 1:
            break
    else:
        raise ValueError
    sg = r.choice([1, -1])
    rv = sg * Fr(s, 10)
    return Q(f'The two regression coefficients are bᵧₓ = {num(float(sg * a))} and bₓᵧ = {num(float(sg * b))}. Find the correlation coefficient.', num(float(rv)),
             f'r² = bᵧₓ × bₓᵧ = {num(float(prod), 3)}; r = {"+" if sg > 0 else "−"}√{num(float(prod), 3)} = {num(float(rv))} (r takes the common sign of the coefficients).',
             nd(num(float(rv)), [num(float(-rv)), num(float(prod), 3), num(float((a + b) / 2 * sg), 3)]))


def c10s4_means(r):
    mx, my = r.randint(2, 20), r.randint(2, 20)
    a1, b1 = r.choice([2, 3, 4, 5]), r.choice([1, 2, 3])
    a2, b2 = r.choice([1, 2, 3]), r.choice([4, 5, 6, 8])
    sg = r.choice([1, -1])
    c1 = a1 * mx + sg * b1 * my
    c2 = a2 * mx + sg * b2 * my
    if a1 * sg * b2 == a2 * sg * b1:
        raise ValueError
    e1 = f'{a1}x {"+" if sg > 0 else "−"} {b1 if b1 != 1 else ""}y = {c1}'
    e2 = f'{a2 if a2 != 1 else ""}x {"+" if sg > 0 else "−"} {b2}y = {c2}'
    return Q(f'The two lines of regression are {e1} and {e2}. Find the mean values of x and y.', f'x̄ = {mx}, ȳ = {my}',
             'Both regression lines pass through (x̄, ȳ); solve the two equations simultaneously.', [f'x̄ = {my}, ȳ = {mx}', f'x̄ = {mx + 1}, ȳ = {my - 1}', f'x̄ = {c1}, ȳ = {c2}'])


def c10s4_predict(r):
    mx, my = r.randint(10, 60), r.randint(20, 90)
    sx, sy = r.choice([2, 4, 5]), r.choice([4, 6, 8, 10])
    rv = Fr(r.choice([5, 6, 8, -5, -6, -8]), 10)
    b = rv * sy / sx
    x0 = mx + r.choice([-5, -4, -2, 2, 3, 4, 5])
    y0 = my + b * (x0 - mx)
    return Q(f'For two variables, x̄ = {mx}, ȳ = {my}, σₓ = {sx}, σᵧ = {sy} and r = {num(float(rv))}. Find the regression equation of y on x and estimate y when x = {x0}.',
             f'y − {my} = {num(float(b), 3)}(x − {mx}); y ≈ {num(float(y0), 2)}', f'bᵧₓ = rσᵧ/σₓ = {num(float(b), 3)} (1); line y − ȳ = bᵧₓ(x − x̄) (1); y({x0}) = {my} + {num(float(b), 3)} × {x0 - mx} = {num(float(y0), 2)} (1).',
             [f'y − {my} = {num(float(rv * sx / sy), 3)}(x − {mx}); y ≈ {num(float(my + rv * sx / sy * (x0 - mx)), 2)}', f'y − {mx} = {num(float(b), 3)}(x − {my}); y ≈ {num(float(mx + b * (x0 - my)), 2)}',
              f'y − {my} = {num(float(b), 3)}(x − {mx}); y ≈ {num(float(y0 + b), 2)}'])


def c10s4_data(r):
    xs, ys = _pairs(r, n=5)
    mx, my, sxy, sxx, syy = _stats(xs, ys)
    b = sxy / sxx
    x0 = max(xs) + r.randint(1, 4)
    y0 = my + b * (x0 - mx)
    return Q(f'From the data below find the regression equation of Y on X and estimate Y when X = {x0}.\n{_tab(xs, ys)}', f'y − {fs(my)} = {num(float(b), 3)}(x − {fs(mx)}); Y ≈ {num(float(y0), 2)}',
             f'x̄ = {fs(mx)}, ȳ = {fs(my)} (1); bᵧₓ = Σdxdy/Σdx² = {fs(sxy)}/{fs(sxx)} = {num(float(b), 3)} (2); equation (1); estimate {num(float(y0), 2)} (1).')


c10s4_formula = pool_mcq([
    ('The regression line of y on x is used to', 'estimate y for a given value of x', ['estimate x for a given value of y', 'find the correlation only', 'find the mean of x'], 'Dependent variable y.'),
    ('The two regression lines intersect at', '(x̄, ȳ)', ['(0, 0)', '(σₓ, σᵧ)', '(bᵧₓ, bₓᵧ)'], 'Both pass through the means.'),
    ('If r = 0, the two regression lines are', 'perpendicular to each other', ['coincident', 'parallel', 'both through the origin'], 'They become y = ȳ and x = x̄.'),
    ('If r = ±1, the two regression lines', 'coincide', ['are perpendicular', 'are parallel', 'do not meet'], 'Perfect linear relation.'),
    ('The regression coefficient bᵧₓ equals', 'rσᵧ/σₓ', ['rσₓ/σᵧ', 'σᵧ/σₓ', 'r/(σₓσᵧ)'], 'Definition.'),
])


def c10s4_ar(r):
    return pool_ar([
        ('If bᵧₓ = 1.6 and bₓᵧ = 0.4, then r = 0.8.', 'r is the geometric mean of the two regression coefficients.', 'a', '√(1.6 × 0.4) = 0.8.'),
        ('The regression coefficients can be 1.5 and 0.9.', 'The product of the regression coefficients equals r², which cannot exceed 1.', 'd', 'A is false: 1.5 × 0.9 = 1.35 > 1. R is true.'),
        ('Both regression coefficients have the same sign.', 'Both have the same sign as r.', 'a', 'bᵧₓ = rσᵧ/σₓ, bₓᵧ = rσₓ/σᵧ.'),
    ])(r)


def c10s4_explain(r):
    return pool_txt([
        ('Why are there two lines of regression? When do they coincide?', 'One estimates y from x, the other x from y; they minimise errors in different directions. They coincide when r = ±1.', '1 + 1 marks.'),
        ('Distinguish between correlation and regression.', 'Correlation measures the degree and direction of the linear relationship; regression gives an equation to estimate one variable from the other.', '1 + 1 marks.'),
        ('Explain why both regression coefficients must have the same sign as r.', 'bᵧₓ = rσᵧ/σₓ and bₓᵧ = rσₓ/σᵧ, and σₓ, σᵧ > 0, so each has the sign of r.', '2 marks.'),
    ])(r)


def c10s4_case(r):
    mx, my = r.choice([20, 25, 30]), r.choice([40, 50, 60])
    b = Fr(r.choice([12, 15, 18, 20]), 10)
    x0 = mx + r.choice([4, 5, 10])
    return {'stem': (f'A company in {r.choice(CITIES)} finds that the regression line of its monthly sales y (lakh ₹) on advertisement spend x (thousand ₹) is y = {num(float(my - b * mx), 2)} + {num(float(b))}x, '
                     f'and the average advertisement spend is ₹{mx} thousand.\n(i) Find the average sales. (1)\n(ii) Interpret the regression coefficient. (1)\n(iii) Estimate the sales when ₹{x0} thousand is spent, and state one caution in using the estimate. (2)'),
            'answer': f'(i) ₹{my} lakh (ii) each extra ₹1 thousand on advertising is associated with ₹{num(float(b))} lakh more sales on average (iii) ₹{num(float(my + b * (x0 - mx)), 2)} lakh; estimates far outside the observed range are unreliable',
            'key': '(i) line passes through means (1). (ii) 1 (iii) estimate (1), caution (1).'}


# ======================================================== ch11 Interest and annuities


def c11s1_si(r):
    P = r.choice([5000, 8000, 12000, 15000, 20000, 25000, 40000])
    R = r.choice([4, 5, 6, 7.5, 8, 9, 10, 12])
    T = r.choice([2, 3, 4, 5, 2.5])
    I = P * R * T / 100
    return Q(f'Find the simple interest on {inr(P)} at {num(R)}% per annum for {num(T)} years.', inr(I), f'SI = PRT/100 = {P} × {num(R)} × {num(T)}/100 = {inr(I)}.',
             [inr(P * (1 + R / 100) ** T - P), inr(I + P), inr(I / T)])


def c11s1_ci(r):
    P = r.choice([5000, 8000, 10000, 15000, 20000, 25000, 50000])
    R = r.choice([5, 8, 10, 12, 15, 20])
    n = r.choice([2, 3])
    A = Fr(P) * Fr(100 + R, 100) ** n
    return Q(f'Find the amount and the compound interest on {inr(P)} at {R}% per annum compounded annually for {n} years.', f'Amount {inr(float(A))}; CI {inr(float(A - P))}',
             f'A = P(1 + r/100)ⁿ = {P} × ({num(1 + R / 100)}){sup(n)} = {inr(float(A))}; CI = A − P = {inr(float(A - P))}.',
             [f'Amount {inr(P + P * R * n / 100)}; CI {inr(P * R * n / 100)}', f'Amount {inr(float(A + P * R / 100))}; CI {inr(float(A - P + P * R / 100))}', f'Amount {inr(float(A))}; CI {inr(float(A))}'])


def c11s1_freq(r):
    P = r.choice([10000, 16000, 20000, 40000, 80000])
    R = r.choice([8, 10, 12, 16, 20])
    m, lab = r.choice([(2, 'half-yearly'), (4, 'quarterly')])
    yrs = r.choice([1, 1.5, 2]) if m == 2 else r.choice([0.5, 0.75, 1])
    n = int(yrs * m)
    A = Fr(P) * (1 + Fr(R, 100 * m)) ** n
    return Q(f'Find the compound interest on {inr(P)} for {num(yrs)} year{"s" if yrs != 1 else ""} at {R}% per annum compounded {lab}.', inr(round(float(A - P), 2)),
             f'Rate per period i = {R}/{m} = {num(R / m)}%; periods n = {n}. A = {P}(1 + {num(R / m / 100, 4)}){sup(n)} = {inr(round(float(A), 2))}; CI = {inr(round(float(A - P), 2))}.',
             [inr(round(float(Fr(P) * (1 + Fr(R, 100)) ** yrs - P), 2)) if float(yrs).is_integer() else inr(P * R * yrs / 100), inr(P * R * yrs / 100 + 1), inr(round(float(A), 2))])


def c11s1_eff(r):
    R = r.choice([6, 8, 10, 12, 16, 20])
    m, lab = r.choice([(2, 'semi-annually'), (4, 'quarterly'), (12, 'monthly')])
    e = (1 + R / 100 / m) ** m - 1
    return Q(f'Find the effective rate of interest equivalent to a nominal rate of {R}% per annum compounded {lab}.', f'{e * 100:.2f}%',
             f'r_eff = (1 + i/m)ᵐ − 1 = (1 + {num(R / 100 / m, 4)}){sup(m)} − 1 = {e:.4f} = {e * 100:.2f}%.', [f'{R}.00%', f'{R / m:.2f}%', f'{e * 100 + 0.5:.2f}%'])


def c11s1_diff(r):
    R = r.choice([4, 5, 8, 10, 12, 15, 20])
    P = r.choice([5000, 8000, 10000, 12000, 20000, 25000])
    d = Fr(P) * Fr(R, 100) ** 2
    return Q(f'The difference between the compound interest (compounded annually) and the simple interest on a sum for 2 years at {R}% per annum is {inr(float(d))}. Find the sum.', inr(P),
             f'For 2 years, CI − SI = P(r/100)² ⇒ {inr(float(d))} = P × ({R}/100)² ⇒ P = {inr(P)}.', [inr(P * 2), inr(float(d * 100 / R)), inr(P // 2)])


def c11s1_rate(r):
    R = r.choice([5, 10, 20, 25])
    n = r.choice([2, 3])
    P = r.choice([1000, 4000, 8000, 16000, 64000])
    A = Fr(P) * Fr(100 + R, 100) ** n
    if A.denominator != 1:
        raise ValueError
    return Q(f'At what rate per cent per annum, compounded annually, will {inr(P)} amount to {inr(int(A))} in {n} years?', f'{R}%',
             f'({int(A)}/{P}) = (1 + r/100){sup(n)} ⇒ 1 + r/100 = {num(1 + R / 100)} ⇒ r = {R}%.', [f'{num(float((A - P) * 100 / (P * n)), 2)}%', f'{R * n}%', f'{R + 5}%'])


c11s1_mcq = pool_mcq([
    ('If the nominal rate is compounded more than once a year, the effective rate is', 'greater than the nominal rate', ['equal to the nominal rate', 'less than the nominal rate', 'always double the nominal rate'], 'Interest is earned on interest within the year.'),
    ('The amount after n years at compound interest is', 'P(1 + r/100)ⁿ', ['P(1 + nr/100)', 'Pnr/100', 'P(1 + r/100)/n'], 'Compound interest formula.'),
    ('For the same principal, rate and time (more than one year), compound interest is', 'more than simple interest', ['less than simple interest', 'equal to simple interest', 'always double simple interest'], 'Interest earns interest.'),
    ('When interest is compounded quarterly at 12% p.a., the rate per quarter is', '3%', ['12%', '4%', '1%'], '12/4.'),
])


def c11s1_ar(r):
    R = r.choice([8, 10, 12])
    e = (1 + R / 200) ** 2 - 1
    return pool_ar([
        (f'The effective rate for {R}% p.a. compounded half-yearly is {e * 100:.2f}%.', 'Interest credited after six months also earns interest for the second half-year.', 'a', 'R explains why the effective rate exceeds the nominal rate.'),
        ('Simple interest and compound interest are equal for the first year when compounding is annual.', 'Under annual compounding, interest is added to the principal only at the end of each year.', 'a', 'R explains A.'),
        ('Compound interest for 2 years is always double the compound interest for 1 year.', 'In compound interest, interest of each period is added to the principal.', 'd', 'A is false: the second year earns interest on the first year\'s interest. R is true.'),
    ])(r)


def c11s1_explain(r):
    R = r.choice([8, 10, 12])
    e = (1 + R / 400) ** 4 - 1
    return {'stem': f'A bank advertises {R}% per annum compounded quarterly. Explain the difference between the nominal and the effective rate, and find the effective rate.',
            'answer': f'Nominal {R}% is the stated annual rate; the effective rate is the actual annual growth when interest is compounded: (1 + {num(R / 400, 3)})⁴ − 1 = {e * 100:.2f}%.',
            'key': 'Distinction (1); value (1).'}


def c11s1_case(r):
    P = r.choice([50000, 100000, 200000])
    R1, R2 = r.choice([(8, 7.8), (10, 9.8), (9, 8.8), (12, 11.6)])
    e2 = (1 + R2 / 400) ** 4 - 1
    best = 'Bank B' if e2 * 100 > R1 else 'Bank A'
    return {'stem': (f'{name(r)} wants to deposit {inr(P)} for one year. Bank A offers {R1}% p.a. compounded annually; Bank B offers {R2}% p.a. compounded quarterly.\n'
                     f'(i) Find the interest from Bank A. (1)\n(ii) Find the effective rate offered by Bank B. (1)\n(iii) Which bank is better, and by how much interest? (2)'),
            'answer': f'(i) {inr(P * R1 / 100)} (ii) {e2 * 100:.2f}% (iii) {best}, by {inr(round(abs(P * e2 - P * R1 / 100), 2))}',
            'key': '(i) 1 (ii) (1 + i/4)⁴ − 1 (1) (iii) comparison (1) and difference (1).'}


# st2 present and future value


def c11s2_fv(r):
    P = r.choice([10000, 20000, 25000, 50000, 75000])
    i = r.choice([5, 6, 8, 10, 12])
    n = r.choice([2, 3, 4, 5])
    fac = round((1 + i / 100) ** n, 4)
    v = P * fac
    return Q(f'Find the future value of {inr(P)} invested for {n} years at {i}% per annum compounded annually. (Use (1.{i:02d}){sup(n)} = {fac:.4f}.)', inr(round(v, 2)),
             f'FV = PV(1 + i)ⁿ = {P} × {fac:.4f} = {inr(round(v, 2))}.', [inr(P * (1 + i * n / 100)), inr(round(P / fac, 2)), inr(round(v + P * i / 100, 2))])


def c11s2_pv(r):
    A = r.choice([50000, 100000, 200000, 150000, 500000])
    i = r.choice([5, 6, 8, 10, 12])
    n = r.choice([2, 3, 4, 5, 6])
    fac = round((1 + i / 100) ** n, 4)
    v = A / fac
    return Q(f'How much should be invested now at {i}% per annum compounded annually to have {inr(A)} after {n} years? (Use (1.{i:02d}){sup(n)} = {fac:.4f}.)', inr(round(v, 2)),
             f'PV = FV/(1 + i)ⁿ = {A}/{fac:.4f} = {inr(round(v, 2))}.', [inr(round(A * fac, 2)), inr(round(A / (1 + i * n / 100), 2)), inr(round(v - A * i / 100, 2))])


def c11s2_compare(r):
    now = r.choice([80000, 90000, 100000, 120000])
    i = r.choice([8, 10, 12])
    n = r.choice([2, 3])
    later = int(round(now * (1 + i / 100) ** n * r.choice([0.95, 0.97, 1.03, 1.05]), -3))
    fac = round((1 + i / 100) ** n, 4)
    pv = later / fac
    better = 'the cash offer now' if now > pv else f'the offer of {inr(later)} after {n} years'
    return Q(f'A buyer offers {inr(now)} cash now for a plot, or {inr(later)} after {n} years. Money can earn {i}% p.a. compounded annually. Which offer is better? (Use (1.{i:02d}){sup(n)} = {fac:.4f}.)',
             f'{better} (PV of the later payment = {inr(round(pv, 2))})', f'Compare present values: PV of {inr(later)} = {later}/{fac:.4f} = {inr(round(pv, 2))} (2); compare with {inr(now)} (1).',
             [f'{"the offer of " + inr(later) + " after " + str(n) + " years" if now > pv else "the cash offer now"} (PV of the later payment = {inr(round(pv, 2))})', 'both are equal', f'{better} (PV of the later payment = {inr(later)})'])


def c11s2_double(r):
    i = r.choice([6, 8, 9, 10, 12])
    n = math.log(2) / math.log(1 + i / 100)
    return Q(f'Using logarithms, find in how many years money doubles at {i}% per annum compounded annually (to one decimal place).', f'{n:.1f} years',
             f'2 = (1.{i:02d})ⁿ ⇒ n = log 2/log 1.{i:02d} = {n:.1f} years.', [f'{100 / i:.1f} years', f'{72 / i + 1:.1f} years', f'{n * 2:.1f} years'])


c11s2_mcq = pool_mcq([
    ('The present value of an amount A due after n years at rate i per period is', 'A(1 + i)⁻ⁿ', ['A(1 + i)ⁿ', 'A(1 + ni)', 'A/i'], 'Discounting.'),
    ('The idea that ₹100 today is worth more than ₹100 a year later is called', 'the time value of money', ['inflation accounting', 'depreciation', 'simple interest'], 'Money today can earn interest.'),
    ('As the interest rate increases, the present value of a fixed future amount', 'decreases', ['increases', 'stays the same', 'doubles'], 'Divide by a larger (1 + i)ⁿ.'),
])


def c11s2_ar(r):
    return pool_ar([
        ('A rupee received today is worth more than a rupee received after one year.', 'Money received today can be invested to earn interest.', 'a', 'R explains A.'),
        ('The present value of ₹10,000 due in 3 years is more than ₹10,000 when the interest rate is positive.', 'PV = FV/(1 + i)ⁿ.', 'd', 'A is false: PV is less than FV. R is true.'),
    ])(r)


def c11s2_explain(r):
    i = r.choice([6, 8, 10])
    return {'stem': f'Explain the terms present value and future value, using ₹1,000 and an interest rate of {i}% p.a. compounded annually for 2 years as an example.',
            'answer': f'FV of ₹1,000 after 2 years = 1000(1.{i:02d})² = {inr(round(1000 * (1 + i / 100) ** 2, 2))}; PV of that amount today is ₹1,000. PV is today\'s worth of a future sum; FV is what a present sum grows to.',
            'key': 'Both definitions (1); worked example (1).'}


def c11s2_case(r):
    goal = r.choice([500000, 800000, 1000000])
    i = r.choice([8, 10])
    n = r.choice([5, 6])
    fac = round((1 + i / 100) ** n, 4)
    return {'stem': (f'Parents of a class 6 student in {r.choice(CITIES)} want {inr(goal)} for college fees after {n} years. A fixed deposit gives {i}% p.a. compounded annually. (Use (1.{i:02d}){sup(n)} = {fac:.4f}.)\n'
                     f'(i) Is this a present-value or a future-value problem? (1)\n(ii) How much should they deposit now? (2)\n(iii) How much interest will the deposit earn? (1)'),
            'answer': f'(i) present value (ii) {inr(round(goal / fac, 2))} (iii) {inr(round(goal - goal / fac, 2))}',
            'key': '(i) 1 (ii) PV = FV/(1 + i)ⁿ (2) (iii) FV − PV (1).'}


# st3 annuities


def _fac(i, n, sign=1):
    return round((1 + i / 100) ** (sign * n), 4)


def c11s3_fv(r):
    R = r.choice([2000, 5000, 10000, 12000, 20000])
    i = r.choice([5, 6, 8, 10])
    n = r.choice([5, 6, 8, 10])
    fac = _fac(i, n)
    v = R * (fac - 1) / (i / 100)
    return Q(f'Find the future value of an ordinary annuity (annuity immediate) of {inr(R)} per year for {n} years at {i}% per annum compounded annually. (Use (1.{i:02d}){sup(n)} = {fac:.4f}.)',
             inr(round(v, 2)), f'FV = R[(1 + i)ⁿ − 1]/i = {R} × ({fac:.4f} − 1)/{num(i / 100)} = {inr(round(v, 2))}.', [inr(R * n), inr(round(v * (1 + i / 100), 2)), inr(round(R * fac, 2))])


def c11s3_pv(r):
    R = r.choice([5000, 10000, 15000, 25000])
    i = r.choice([5, 6, 8, 10, 12])
    n = r.choice([4, 5, 6, 8, 10])
    fac = _fac(i, n, -1)
    v = R * (1 - fac) / (i / 100)
    return Q(f'Find the present value of an annuity immediate of {inr(R)} per year for {n} years at {i}% per annum. (Use (1.{i:02d})^(−{n}) = {fac:.4f}.)',
             inr(round(v, 2)), f'PV = R[1 − (1 + i)⁻ⁿ]/i = {R} × (1 − {fac:.4f})/{num(i / 100)} = {inr(round(v, 2))}.', [inr(R * n), inr(round(v * (1 + i / 100), 2)), inr(round(R * fac, 2))])


def c11s3_due(r):
    R = r.choice([3000, 5000, 10000])
    i = r.choice([5, 8, 10])
    n = r.choice([4, 5, 6, 8])
    fac = _fac(i, n)
    imm = R * (fac - 1) / (i / 100)
    due = imm * (1 + i / 100)
    return Q(f'{name(r)} deposits {inr(R)} at the beginning of every year for {n} years in an account paying {i}% per annum compounded annually. Find the amount at the end of {n} years. (Use (1.{i:02d}){sup(n)} = {fac:.4f}.)',
             inr(round(due, 2)), f'Annuity due: FV = R[(1 + i)ⁿ − 1]/i × (1 + i) = {inr(round(imm, 2))} × {num(1 + i / 100)} = {inr(round(due, 2))}.',
             [inr(round(imm, 2)), inr(R * n), inr(round(due + R, 2))])


def c11s3_sink(r):
    A = r.choice([500000, 1000000, 300000, 800000])
    i = r.choice([6, 8, 10])
    n = r.choice([5, 8, 10])
    fac = _fac(i, n)
    R = A * (i / 100) / (fac - 1)
    return Q(f'A company wants to set up a sinking fund to replace a machine costing {inr(A)} after {n} years. How much should it set aside at the end of every year if the fund earns {i}% p.a. compounded annually? (Use (1.{i:02d}){sup(n)} = {fac:.4f}.)',
             inr(round(R, 2)), f'A = R[(1 + i)ⁿ − 1]/i (2) ⇒ R = {A} × {num(i / 100)}/({fac:.4f} − 1) (2) = {inr(round(R, 2))} (1).', [inr(round(A / n, 2)), inr(round(A * (i / 100) / fac, 2)), inr(round(R * 1.1, 2))])


def c11s3_perp(r):
    R = r.choice([5000, 12000, 24000, 50000, 60000])
    i = r.choice([4, 5, 6, 8, 10, 12])
    return Q(f'A trust wants to award a scholarship of {inr(R)} every year forever. How much must be invested now if money earns {i}% per annum?', inr(R * 100 / i),
             f'PV of a perpetuity = R/i = {R}/{num(i / 100)} = {inr(R * 100 / i)}.', [inr(R * i), inr(R * 100 / i / 2), inr(R * 10)])


c11s3_mcq = pool_mcq([
    ('An annuity whose payments are made at the end of each period is called', 'an annuity immediate (ordinary annuity)', ['an annuity due', 'a perpetuity', 'a deferred annuity'], 'Definition.'),
    ('An annuity whose payments are made at the beginning of each period is called', 'an annuity due', ['an annuity immediate', 'a sinking fund', 'a perpetuity'], 'Definition.'),
    ('An annuity that continues forever is called', 'a perpetuity', ['an annuity due', 'a contingent annuity', 'an ordinary annuity'], 'Definition.'),
    ('The future value of an annuity due is equal to the future value of the corresponding annuity immediate multiplied by', '(1 + i)', ['i', '(1 + i)ⁿ', 'n'], 'Each payment earns one extra period.'),
    ('A fund built by regular deposits to repay a known future liability is called', 'a sinking fund', ['a perpetuity', 'a provident fund only', 'a reserve'], 'Definition.'),
])


def c11s3_ar(r):
    return pool_ar([
        ('The future value of an annuity due is more than that of an annuity immediate with the same payment, rate and term.', 'In an annuity due, every payment earns interest for one more period.', 'a', 'R explains A.'),
        ('The present value of a perpetuity of ₹R per year at rate i is R/i.', 'Payments of a perpetuity never end, so its present value is infinite.', 'c', 'A is true; R is false: the discounted payments form a convergent series.'),
        ('Monthly SIP deposits in a recurring deposit form an annuity.', 'An annuity is a series of equal payments at equal intervals.', 'a', 'R explains A.'),
    ])(r)


def c11s3_explain(r):
    R = r.choice([1000, 2000, 5000])
    return {'stem': f'Distinguish between an annuity immediate and an annuity due, taking an example of a payment of {inr(R)} per year for 3 years.',
            'answer': f'Annuity immediate: {inr(R)} paid at the end of years 1, 2, 3. Annuity due: {inr(R)} paid at the beginning of years 1, 2, 3, so each payment earns interest for one more year.',
            'key': 'Timing difference (1); consequence for value with the example (1).'}


def c11s3_case(r):
    R = r.choice([2000, 3000, 5000])
    i = r.choice([6, 8])
    n = r.choice([5, 10])
    fac = _fac(i, n)
    imm = R * (fac - 1) / (i / 100)
    return {'stem': (f'{name(r)}, a young professional in {r.choice(CITIES)}, plans to save {inr(R)} at the end of every year for {n} years in a scheme paying {i}% p.a. compounded annually. (Use (1.{i:02d}){sup(n)} = {fac:.4f}.)\n'
                     f'(i) Which type of annuity is this? (1)\n(ii) Find the amount at the end of {n} years. (2)\n(iii) How much more would she get if she saved at the beginning of every year? (1)'),
            'answer': f'(i) annuity immediate (ordinary) (ii) {inr(round(imm, 2))} (iii) {inr(round(imm * i / 100, 2))} more ({inr(round(imm * (1 + i / 100), 2))} in all)',
            'key': '(i) 1 (ii) formula (1) value (1) (iii) × (1 + i) (1).'}


# ======================================================== ch12 Taxation
# st1 GST structure

GST_RATES = [5, 12, 18, 28]


def c12s1_split(r):
    V = r.choice([2400, 5000, 8500, 12000, 15600, 25000, 36000, 48000])
    g = r.choice(GST_RATES)
    c = V * g / 200
    st1, st2 = r.sample(['Maharashtra', 'Karnataka', 'Tamil Nadu', 'Gujarat', 'Rajasthan', 'Uttar Pradesh', 'West Bengal', 'Punjab', 'Kerala', 'Madhya Pradesh'], 2)
    if r.random() < 0.5:
        return Q(f'A dealer in {st1} sells goods worth {inr(V)} to a customer in {st1}. The GST rate is {g}%. Find the CGST and SGST charged and the total amount of the bill.',
                 f'CGST {inr(c)}, SGST {inr(c)}; total {inr(V + 2 * c)}', f'Intra-state supply: GST {g}% is split equally, CGST {num(g / 2)}% = {inr(c)} and SGST {num(g / 2)}% = {inr(c)}; bill = {inr(V)} + {inr(2 * c)} = {inr(V + 2 * c)}.',
                 [f'CGST {inr(2 * c)}, SGST {inr(2 * c)}; total {inr(V + 4 * c)}', f'IGST {inr(2 * c)}; total {inr(V + 2 * c)}', f'CGST {inr(c)}, SGST {inr(c)}; total {inr(V + c)}'])
    return Q(f'A dealer in {st1} sells goods worth {inr(V)} to a dealer in {st2}. The GST rate is {g}%. Which tax is charged and how much? Find the total amount of the invoice.',
             f'IGST {inr(2 * c)}; total {inr(V + 2 * c)}', f'Inter-state supply attracts IGST at the full rate {g}%: {inr(2 * c)}; invoice = {inr(V + 2 * c)}.',
             [f'CGST {inr(c)} and SGST {inr(c)}; total {inr(V + 2 * c)}', f'IGST {inr(c)}; total {inr(V + c)}', f'SGST {inr(2 * c)}; total {inr(V + 2 * c)}'])


def c12s1_which(r):
    st = r.sample(['Maharashtra', 'Karnataka', 'Gujarat', 'Rajasthan', 'Punjab', 'Kerala', 'Bihar', 'Odisha'], 2)
    ut = r.choice(['Chandigarh', 'Andaman and Nicobar Islands', 'Lakshadweep', 'Dadra and Nagar Haveli and Daman and Diu'])
    cases = [(f'a supply of goods from a dealer in {st[0]} to a consumer in {st[0]}', 'CGST and SGST'),
             (f'a supply of goods from a dealer in {st[0]} to a dealer in {st[1]}', 'IGST'),
             (f'a supply of goods within the Union Territory of {ut}', 'CGST and UTGST'),
             (f'goods imported into India from abroad', 'IGST')]
    t, a = r.choice(cases)
    opts = ['CGST and SGST', 'IGST', 'CGST and UTGST', 'SGST only']
    return mcq(f'Under GST, which tax(es) apply to {t}?', a, [o for o in opts if o != a], f'{a} applies: intra-state → CGST + SGST; inter-state and imports → IGST; within a UT without legislature → CGST + UTGST.', r)


c12s1_terms = term_mcq([
    ('GST', 'a comprehensive, destination-based indirect tax on the supply of goods and services'), ('CGST', 'the part of GST on an intra-state supply that is collected by the Central Government'),
    ('SGST', 'the part of GST on an intra-state supply that is collected by the State Government'), ('IGST', 'GST levied by the Centre on inter-state supplies and imports'),
    ('UTGST', 'the GST collected by a Union Territory (without its own legislature) on supplies within it'), ('input tax credit', 'the credit for GST paid on purchases that is set off against GST payable on sales'),
    ('HSN code', 'the internationally used code for classifying goods under GST'), ('GSTIN', 'the identification number given to a business registered under GST')],
    'Under GST, the term {a} means', 'Which term is described as {b}?', '{a}: {b}.')

c12s1_tf = tf_mcq('the Goods and Services Tax', [
    'GST came into force in India on 1 July 2017.', 'GST is an indirect tax.', 'On an intra-state supply, CGST and SGST are charged at equal rates.',
    'IGST is levied on inter-state supplies of goods and services.', 'GST replaced several indirect taxes such as VAT, central excise duty and service tax.',
    'The GST Council is chaired by the Union Finance Minister.'],
    ['GST is a direct tax on income.', 'On an inter-state supply, CGST and SGST are charged.', 'GST is collected only by State Governments.',
     'Under GST, a buyer can never get credit for tax paid on inputs.', 'GST came into force in India on 1 April 2010.'])


def c12s1_ar(r):
    return pool_ar([
        ('GST is called a destination-based tax.', 'The tax revenue goes to the State where the goods or services are consumed.', 'a', 'R explains A.'),
        ('On a sale within Rajasthan, the buyer pays CGST and SGST.', 'For intra-state supplies, GST is shared equally between the Centre and the State.', 'a', 'R explains A.'),
        ('GST is a direct tax.', 'The burden of GST is passed on to the final consumer.', 'd', 'A is false: GST is an indirect tax, as R indicates. R is true.'),
        ('Input tax credit avoids the cascading effect of taxes.', 'Under GST, tax is effectively paid only on the value added at each stage.', 'a', 'R explains A.'),
    ])(r)


def c12s1_explain(r):
    return pool_txt([
        ('Distinguish between direct and indirect taxes, with one example of each.', 'Direct tax: paid by the person on whom it is levied, burden cannot be shifted (income tax). Indirect tax: levied on goods and services, burden shifted to the consumer (GST).', '1 + 1 marks.'),
        ('What is meant by the cascading effect of taxes? How does GST remove it?', 'Tax on tax, when tax is charged on a price that already includes earlier tax. GST gives input tax credit, so tax is paid only on value added.', '1 + 1 marks.'),
        ('Why is GST described as "one nation, one tax"?', 'It replaced many central and state indirect taxes with a single tax with a uniform structure across States, levied at each stage of supply.', '2 marks.'),
    ])(r)


def c12s1_bill(r):
    items = r.sample([('school bag', 1200), ('water bottle', 350), ('geometry box', 180), ('calculator', 950), ('sports shoes', 2400), ('backpack', 1600), ('lunch box', 420)], 2)
    q1, q2 = r.randint(1, 3), r.randint(1, 4)
    g = r.choice([12, 18])
    disc = r.choice([0, 5, 10])
    sub = items[0][1] * q1 + items[1][1] * q2
    net = sub * (100 - disc) / 100
    tax = net * g / 100
    return Q(f'A shop in {r.choice(CITIES)} sells {q1} {items[0][0]}{"s" if q1 > 1 else ""} at {inr(items[0][1])} each and {q2} {items[1][0]}{"s" if q2 > 1 else ""} at {inr(items[1][1])} each'
             f'{f", allowing a discount of {disc}%" if disc else ""}. GST at {g}% is charged on the {"discounted " if disc else ""}value (intra-state sale). Find the CGST, SGST and the total bill.',
             f'CGST {inr(tax / 2)}, SGST {inr(tax / 2)}; total {inr(net + tax)}', f'Value {inr(sub)}{f", after discount {inr(net)}" if disc else ""} (1); CGST = SGST = {num(g / 2)}% = {inr(tax / 2)} each (1); total = {inr(net + tax)} (1).',
             [f'CGST {inr(tax)}, SGST {inr(tax)}; total {inr(net + 2 * tax)}', f'CGST {inr(sub * g / 200)}, SGST {inr(sub * g / 200)}; total {inr(sub + sub * g / 100)}' if disc else f'CGST {inr(tax / 2)}, SGST {inr(tax / 2)}; total {inr(net + tax / 2)}',
              f'CGST {inr(tax / 2)}, SGST {inr(tax / 2)}; total {inr(net)}'])


def c12s1_case(r):
    V = r.choice([20000, 35000, 50000])
    g = r.choice([12, 18, 28])
    st1, st2 = r.sample(['Delhi', 'Haryana', 'Uttar Pradesh', 'Maharashtra', 'Gujarat'], 2)
    return {'stem': (f'An electronics dealer in {st1} supplies goods worth {inr(V)} to a retailer in {st1} and goods of the same value to a retailer in {st2}. The GST rate is {g}%.\n'
                     f'(i) Name the taxes charged on each supply. (1)\n(ii) Find the tax charged on the supply within {st1}, showing each component. (1)\n'
                     f'(iii) Find the tax on the supply to {st2} and the total GST collected on both supplies. (2)'),
            'answer': f'(i) within {st1}: CGST + SGST; to {st2}: IGST (ii) CGST {inr(V * g / 200)} + SGST {inr(V * g / 200)} = {inr(V * g / 100)} (iii) IGST {inr(V * g / 100)}; total {inr(V * g / 50)}',
            'key': '(i) 1 (ii) equal split (1) (iii) IGST (1) total (1).'}


# st2 computing GST and ITC


def c12s2_itc(r):
    P = r.choice([10000, 20000, 25000, 40000, 50000])
    S_ = P + r.choice([2000, 4000, 5000, 8000, 10000])
    g = r.choice(GST_RATES)
    out, inp = S_ * g / 100, P * g / 100
    return Q(f'A trader buys goods for {inr(P)} (excluding GST) and sells them for {inr(S_)} (excluding GST) within the same State. The GST rate is {g}%. Find the net GST payable by the trader after input tax credit.',
             inr(out - inp), f'Output tax = {g}% of {inr(S_)} = {inr(out)}; input tax credit = {g}% of {inr(P)} = {inr(inp)}; net GST = {inr(out - inp)} (i.e. {g}% of the value added {inr(S_ - P)}).',
             [inr(out), inr(out + inp), inr((out - inp) / 2)])


def c12s2_chain(r):
    g = r.choice([5, 12, 18])
    p1 = r.choice([10000, 12000, 15000, 20000])
    p2 = p1 + r.choice([2000, 3000, 5000])
    p3 = p2 + r.choice([1000, 2000, 4000])
    t1, t2, t3 = p1 * g / 100, (p2 - p1) * g / 100, (p3 - p2) * g / 100
    return Q(f'A manufacturer sells an article to a wholesaler for {inr(p1)}. The wholesaler sells it to a retailer for {inr(p2)} and the retailer sells it to a consumer for {inr(p3)} (all prices excluding tax, all within one State). '
             f'GST is {g}%. Find the net GST paid to the Government by each of the manufacturer, wholesaler and retailer, and show that the total equals the GST paid by the consumer.',
             f'{inr(t1)}, {inr(t2)}, {inr(t3)}; total {inr(t1 + t2 + t3)} = {g}% of {inr(p3)}',
             f'Manufacturer: {g}% of {p1} = {inr(t1)} (1). Wholesaler: {inr(p2 * g / 100)} − {inr(t1)} = {inr(t2)} (1). Retailer: {inr(p3 * g / 100)} − {inr(p2 * g / 100)} = {inr(t3)} (1). Total {inr(t1 + t2 + t3)} = GST on {inr(p3)} (2).',
             [f'{inr(t1)}, {inr(p2 * g / 100)}, {inr(p3 * g / 100)}; total {inr((p1 + p2 + p3) * g / 100)}'])


def c12s2_incl(r):
    g = r.choice(GST_RATES)
    base = r.choice([500, 800, 1000, 1250, 2000, 2500, 4000, 5000])
    tot = base * (100 + g) / 100
    return Q(f'The price of an article including {g}% GST is {inr(tot)}. Find its price before GST and the amount of GST.', f'{inr(base)}; GST {inr(tot - base)}',
             f'Price before GST = {inr(tot)} × 100/{100 + g} = {inr(base)}; GST = {inr(tot - base)}.', [f'{inr(tot * (100 - g) / 100)}; GST {inr(tot * g / 100)}', f'{inr(base + 10)}; GST {inr(tot - base - 10)}', f'{inr(tot)}; GST {inr(tot * g / 100)}'])


def c12s2_inter(r):
    g = r.choice([12, 18])
    P = r.choice([30000, 40000, 50000, 60000])
    S_ = P + r.choice([5000, 10000, 15000])
    return Q(f'A dealer in Pune buys goods worth {inr(P)} from Ahmedabad (inter-state) and sells them in Mumbai for {inr(S_)} (intra-state). GST rate is {g}%. Find the IGST paid on purchase, the CGST and SGST collected on sale, and the net GST payable.',
             f'IGST {inr(P * g / 100)}; CGST {inr(S_ * g / 200)} and SGST {inr(S_ * g / 200)}; net {inr((S_ - P) * g / 100)}',
             f'IGST on purchase = {inr(P * g / 100)} (1); output CGST = SGST = {inr(S_ * g / 200)} (1); IGST credit is set off against output tax: net = {inr(S_ * g / 100)} − {inr(P * g / 100)} = {inr((S_ - P) * g / 100)} (1).',
             [f'IGST {inr(P * g / 100)}; CGST {inr(S_ * g / 100)} and SGST {inr(S_ * g / 100)}; net {inr(S_ * g / 50 - P * g / 100)}'])


def c12s2_disc(r):
    M = r.choice([2000, 4000, 5000, 8000, 12000, 15000])
    d = r.choice([5, 10, 15, 20, 25])
    g = r.choice(GST_RATES)
    sp = M * (100 - d) / 100
    tot = sp * (100 + g) / 100
    if r.random() < 0.5:
        return Q(f'The marked price of a washing machine is {inr(M)}. The shopkeeper gives a discount of {d}% and charges GST at {g}% on the discounted price. Find the amount paid by the customer.', inr(tot),
                 f'Discounted price = {inr(sp)}; GST = {g}% of it = {inr(sp * g / 100)}; amount = {inr(tot)}.', [inr(M * (100 + g - d) / 100), inr(M * (100 + g) / 100 * (100 - d) / 100 + 100), inr(sp)])
    return Q(f'A customer pays {inr(tot)} for an article, including GST at {g}%, after a discount of {d}% on the marked price. Find the marked price.', inr(M),
             f'Price before GST = {inr(tot)} × 100/{100 + g} = {inr(sp)}; marked price = {inr(sp)} × 100/{100 - d} = {inr(M)}.', [inr(tot * (100 - g + d) / 100), inr(sp), inr(M + 500)])


c12s2_mcq = pool_mcq([
    ('Input tax credit means', 'reducing the GST paid on purchases from the GST payable on sales', ['a loan given by the Government', 'a discount allowed to customers', 'tax paid on income'], 'Definition.'),
    ('Under GST, the total tax collected along a supply chain equals', 'the GST on the final selling price to the consumer', ['the sum of GST on all sale prices', 'zero', 'the GST on the first sale only'], 'ITC removes tax on tax.'),
    ('If a dealer buys goods for ₹8,000 and sells them for ₹10,000 with GST at 12%, the net GST payable is', '₹240', ['₹1,200', '₹960', '₹2,160'], '12% of ₹2,000.'),
])


def c12s2_ar(r):
    return pool_ar([
        ('With input tax credit, a dealer pays GST only on the value he adds.', 'GST paid on purchases is set off against GST collected on sales.', 'a', 'R explains A.'),
        ('The final consumer can claim input tax credit on goods bought for personal use.', 'Input tax credit is available to registered dealers on inputs used in the course of business.', 'd', 'A is false: the consumer bears the tax. R is true.'),
    ])(r)


def c12s2_explain(r):
    g = r.choice([5, 12, 18])
    a, b = r.choice([(1000, 1500), (2000, 2600), (5000, 6000)])
    return {'stem': f'Using a purchase at ₹{a} and a sale at ₹{b} (both before tax) with GST at {g}%, explain how input tax credit works.',
            'answer': f'Output GST {inr(b * g / 100)}; input GST paid {inr(a * g / 100)} is credited; net payable {inr((b - a) * g / 100)}, i.e. tax on the value added {inr(b - a)} only.',
            'key': 'Computation (1); explanation of avoiding tax on tax (1).'}


def c12s2_case(r):
    g = r.choice([12, 18])
    p1, p2, p3 = r.choice([(20000, 24000, 27000), (15000, 18000, 21000), (30000, 34000, 40000)])
    return {'stem': (f'A furniture maker in Jaipur sells a sofa set to a wholesaler in Jaipur for {inr(p1)}. The wholesaler sells it to a retailer in Jaipur for {inr(p2)}, who sells it to a customer for {inr(p3)}. GST is {g}% (prices exclude tax).\n'
                     f'(i) Which taxes are charged at each stage? (1)\n(ii) Find the net GST paid by the wholesaler. (1)\n(iii) Find the net GST paid by the retailer and the total tax received by the Government. (2)'),
            'answer': f'(i) CGST and SGST (intra-state) (ii) {inr((p2 - p1) * g / 100)} (iii) {inr((p3 - p2) * g / 100)}; total {inr(p3 * g / 100)}',
            'key': '(i) 1 (ii) output − input (1) (iii) retailer (1), total equals GST on final price (1).'}


# st3 income tax (slabs given in the question)

SLABS = [(300000, 0), (700000, 5), (1000000, 10), (1200000, 15), (1500000, 20), (None, 30)]
SLAB_TXT = ('Use these slab rates (given for this question): up to ₹3,00,000 – nil; ₹3,00,001 to ₹7,00,000 – 5%; ₹7,00,001 to ₹10,00,000 – 10%; '
            '₹10,00,001 to ₹12,00,000 – 15%; ₹12,00,001 to ₹15,00,000 – 20%; above ₹15,00,000 – 30%. Health and education cess is 4% of the tax. Ignore any rebate.')


def _tax(inc):
    t, lo, parts = 0, 0, []
    for hi, rate in SLABS:
        top = inc if hi is None else min(inc, hi)
        if top > lo:
            amt = (top - lo) * rate / 100
            t += amt
            if rate:
                parts.append(f'{rate}% of {inr(top - lo)} = {inr(amt)}')
        if hi is None or inc <= hi:
            break
        lo = hi
    return t, parts


def c12s3_tax(r):
    inc = r.randrange(450000, 1900000, 10000)
    t, parts = _tax(inc)
    tot = t * 1.04
    return Q(f'{SLAB_TXT}\nFind the income tax payable (including cess) on a taxable income of {inr(inc)}.', inr(round(tot)),
             f'{"; ".join(parts)}; tax = {inr(t)} (2); cess 4% = {inr(t * 0.04)} (½); total = {inr(round(tot))} (½).', [inr(round(t)), inr(round(inc * 0.3 * 1.04)), inr(round(tot + 5000))])


def c12s3_cess(r):
    t = r.randrange(10000, 250000, 500)
    return Q(f'The income tax on a person\'s income before cess is {inr(t)}. Health and education cess is charged at 4% of the tax. Find the total tax payable.', inr(t * 1.04),
             f'Cess = 4% of {inr(t)} = {inr(t * 0.04)}; total = {inr(t * 1.04)}.', [inr(t * 0.04), inr(t * 1.4), inr(t + 4)])


def c12s3_full(r):
    sal = r.randrange(60000, 160000, 5000)
    gross = sal * 12
    sd = 75000
    other = r.choice([0, 0, 20000, 50000])
    taxable = gross + other - sd
    t, parts = _tax(taxable)
    tot = round(t * 1.04)
    who = name(r)
    return Q(f'{who} earns a salary of {inr(sal)} per month{f" and interest income of {inr(other)} in the year" if other else ""}. A standard deduction of ₹75,000 is allowed (given for this question). {SLAB_TXT}\n'
             f'Find {who}\'s taxable income, the tax payable for the year and the average monthly tax deducted at source (TDS).', f'taxable {inr(taxable)}; tax {inr(tot)}; TDS ≈ {inr(round(tot / 12))} per month',
             f'Gross = {inr(gross)}{f" + {inr(other)}" if other else ""}; taxable = {inr(taxable)} (1). {"; ".join(parts)}; tax {inr(t)} (2); with cess {inr(tot)} (1); monthly TDS = {inr(tot)}/12 ≈ {inr(round(tot / 12))} (1).')


c12s3_mcq = pool_mcq([
    ('Income tax is', 'a direct tax', ['an indirect tax', 'a tax on goods', 'a tax collected by States'], 'Paid by the person on whom it is levied.'),
    ('In India, income tax is levied under', 'the Income-tax Act, 1961', ['the GST Act, 2017', 'the Companies Act, 2013', 'the Indian Contract Act, 1872'], 'Governing statute.'),
    ('Tax deducted by an employer from the salary before payment is called', 'TDS (tax deducted at source)', ['GST', 'cess', 'surcharge only'], 'Definition.'),
    ('A tax system in which the rate rises as income rises is called', 'progressive', ['regressive', 'proportional', 'indirect'], 'Slab rates increase with income.'),
    ('The cess on income tax that is mentioned as 4% is the', 'health and education cess', ['GST compensation cess', 'Swachh Bharat cess', 'road cess'], 'Charged on the amount of income tax.'),
])


def c12s3_ar(r):
    return pool_ar([
        ('Income tax is a progressive tax.', 'Higher slabs of income are taxed at higher rates.', 'a', 'R explains A.'),
        ('A person with a taxable income of ₹2,50,000 pays tax at 5% on the whole income under the given slabs.', 'Under the given slabs, income up to ₹3,00,000 is not taxed.', 'd', 'A is false: no tax is due. R is true.'),
        ('Two persons with incomes ₹8,00,000 and ₹16,00,000 pay tax in the ratio 1 : 2 under slab rates.', 'Under slab rates, each part of the income is taxed at the rate of its own slab.', 'd',
         'A is false: the higher income pays far more than double, because of higher slab rates. R is true.'),
    ])(r)


def c12s3_explain(r):
    inc = r.randrange(800000, 1400000, 50000)
    t, parts = _tax(inc)
    return {'stem': f'{SLAB_TXT}\nExplain why the tax on {inr(inc)} is not simply the top slab rate applied to the whole income. Find the tax before cess.',
            'answer': f'Slab rates apply only to the part of income falling in each slab: {"; ".join(parts)}; tax {inr(t)}.', 'key': 'Explanation (1); computation (1).'}


def c12s3_case(r):
    sal = r.randrange(80000, 140000, 5000)
    taxable = sal * 12 - 75000
    t, parts = _tax(taxable)
    return {'stem': (f'{name(r)} has a monthly salary of {inr(sal)}. A standard deduction of ₹75,000 is allowed (given for this question). {SLAB_TXT}\n'
                     f'(i) Find the annual taxable income. (1)\n(ii) Find the income tax before cess. (2)\n(iii) Find the total tax including cess. (1)'),
            'answer': f'(i) {inr(taxable)} (ii) {inr(t)} (iii) {inr(round(t * 1.04))}', 'key': f'(i) 12 × salary − 75,000 (1). (ii) {"; ".join(parts)} (2). (iii) + 4% cess (1).'}


# st4 utility bills

def _elec(u, slabs):
    cost, lo, parts = 0, 0, []
    for hi, rate in slabs:
        top = u if hi is None else min(u, hi)
        if top > lo:
            cost += (top - lo) * rate
            parts.append(f'{top - lo} × ₹{num(rate)} = {inr((top - lo) * rate)}')
        if hi is None or u <= hi:
            break
        lo = hi
    return cost, parts


ELEC = [[(100, 3), (200, 4.5), (400, 6), (None, 7.5)], [(50, 2.5), (150, 4), (300, 5.5), (None, 7)], [(100, 3.5), (300, 5), (None, 6.5)]]


def _elec_txt(sl):
    out, lo = [], 0
    for hi, rate in sl:
        out.append(f'{lo + 1}–{hi} units: ₹{num(rate)}/unit' if hi else f'above {lo} units: ₹{num(rate)}/unit')
        lo = hi or lo
    return '; '.join(out)


def c12s4_elec(r):
    sl = r.choice(ELEC)
    u = r.randint(120, 520)
    fixed = r.choice([50, 75, 100, 120])
    duty = r.choice([0, 5, 10])
    cost, parts = _elec(u, sl)
    tot = (cost + fixed) * (1 + duty / 100)
    return Q(f'An electricity board charges: {_elec_txt(sl)}; fixed charge ₹{fixed} per month{f"; electricity duty {duty}% on the total of energy and fixed charges" if duty else ""}. Find the bill for a month in which {u} units are consumed.',
             inr(round(tot, 2)), f'Energy charge: {"; ".join(parts)}; total {inr(cost)} (1); add fixed ₹{fixed} = {inr(cost + fixed)} (1){f"; duty {duty}% ⇒ {inr(round(tot, 2))}" if duty else ""} (1).',
             [inr(round(u * sl[-1][1] + fixed, 2)), inr(round(cost, 2)), inr(round(tot + fixed, 2))])


def c12s4_meter(r):
    prev = r.randint(1000, 9000)
    u = r.randint(150, 420)
    sl = r.choice(ELEC)
    cost, parts = _elec(u, sl)
    return Q(f'The previous and present meter readings of a house in {r.choice(CITIES)} are {prev} and {prev + u}. The tariff is {_elec_txt(sl)}. Find the units consumed and the energy charges.',
             f'{u} units; {inr(cost)}', f'Units = {prev + u} − {prev} = {u} (1); {"; ".join(parts)} (1); energy charge {inr(cost)} (1).', [f'{u} units; {inr(u * sl[0][1])}', f'{u + 1} units; {inr(cost)}', f'{u} units; {inr(u * sl[-1][1])}'])


def c12s4_water(r):
    kl = r.randint(12, 45)
    r1, r2 = r.choice([(4, 10), (5, 12), (6, 15)])
    lim = r.choice([10, 15, 20])
    sew = r.choice([30, 50, 60])
    fixed = r.choice([0, 50, 100])
    w = min(kl, lim) * r1 + max(0, kl - lim) * r2
    tot = w * (1 + sew / 100) + fixed
    return Q(f'A municipal corporation charges for water: ₹{r1} per kilolitre (kL) for the first {lim} kL and ₹{r2} per kL beyond that, plus a sewerage charge of {sew}% of the water charge{f" and a meter rent of ₹{fixed}" if fixed else ""}. Find the bill for {kl} kL.',
             inr(tot), f'Water charge = {min(kl, lim)} × {r1} + {max(0, kl - lim)} × {r2} = {inr(w)}; sewerage {sew}% = {inr(w * sew / 100)}{f"; meter rent ₹{fixed}" if fixed else ""}; total {inr(tot)}.',
             [inr(kl * r1 * (1 + sew / 100) + fixed), inr(w + fixed), inr(kl * r2 + fixed)])


c12s4_mcq = pool_mcq([
    ('In a telescopic (slab) tariff for electricity, units in a higher slab are charged', 'at a higher rate only for the units falling in that slab', ['at a higher rate for all units consumed', 'at a lower rate', 'free of cost'], 'Each slab has its own rate.'),
    ('One unit of electrical energy is', '1 kilowatt-hour', ['1 watt', '1 joule', '1 kilowatt'], '1 kWh.'),
    ('A 2 kW air conditioner used for 5 hours a day for 30 days consumes', '300 units', ['10 units', '150 units', '600 units'], '2 × 5 × 30 = 300 kWh.'),
    ('A fixed charge in a utility bill is paid', 'whatever the consumption in the month', ['only when consumption is zero', 'per unit consumed', 'only in summer'], 'Covers meter and service costs.'),
])


def c12s4_appl(r):
    W = r.choice([100, 200, 1000, 1500, 2000, 60, 40])
    h = r.choice([2, 4, 5, 6, 8])
    d = r.choice([30, 31])
    u = W * h * d / 1000
    rate = r.choice([5, 6, 7])
    return Q(f'A {W} W appliance is used {h} hours a day for {d} days. Find the units of electricity consumed and the cost at ₹{rate} per unit.', f'{num(u)} units; {inr(u * rate)}',
             f'Energy = {W} × {h} × {d}/1000 = {num(u)} kWh; cost = {num(u)} × {rate} = {inr(u * rate)}.', [f'{num(u * 1000)} units; {inr(u * 1000 * rate)}', f'{num(u / d)} units; {inr(u / d * rate)}', f'{num(u)} units; {inr(u * rate * 2)}'])


def c12s4_ar(r):
    return pool_ar([
        ('A family using 250 units pays less per unit on average than a family using 500 units under a slab tariff.', 'In a slab tariff, higher slabs carry higher rates.', 'a', 'R explains A.'),
        ('Doubling consumption always doubles the electricity bill under a slab tariff.', 'In a slab tariff, higher slabs carry higher rates.', 'd', 'A is false: the bill more than doubles (and fixed charges do not double). R is true.'),
    ])(r)


def c12s4_explain(r):
    return {'stem': r.choice(['Explain why electricity boards use slab (telescopic) tariffs that increase with consumption.', 'Explain why a family\'s electricity bill rises faster than its consumption in summer under a slab tariff.']),
            'answer': 'Higher slabs are charged at higher rates, so extra units cost more; this encourages saving electricity and keeps the rate low for small consumers.',
            'key': 'Slab mechanism (1); purpose / effect (1).'}


def c12s4_case(r):
    sl = r.choice(ELEC)
    u1, u2 = r.randint(120, 220), r.randint(320, 480)
    c1, _ = _elec(u1, sl)
    c2, _ = _elec(u2, sl)
    return {'stem': (f'A house in {r.choice(CITIES)} used {u1} units in January and {u2} units in May. The tariff is {_elec_txt(sl)}.\n'
                     f'(i) Find the energy charge for January. (1)\n(ii) Find the energy charge for May. (1)\n(iii) Find the average cost per unit in each month and explain the difference. (2)'),
            'answer': f'(i) {inr(c1)} (ii) {inr(c2)} (iii) ₹{c1 / u1:.2f} and ₹{c2 / u2:.2f} per unit; more units fall in higher-rate slabs in May',
            'key': '(i) 1 (ii) 1 (iii) averages (1), reason (1).'}


# ======================================================== ch13 Straight lines: business applications


def c13s3_cost(r):
    v = r.choice([20, 25, 30, 40, 45, 50, 60])
    Fx = r.choice([2000, 3000, 5000, 8000, 10000])
    x1, x2 = r.sample([50, 100, 150, 200, 250, 300], 2)
    return Q(f'The total cost of producing {x1} units is {inr(Fx + v * x1)} and of producing {x2} units is {inr(Fx + v * x2)}. Assuming the cost is linear, find the cost function, the fixed cost and the variable cost per unit.',
             f'C = {v}x + {Fx}; fixed cost {inr(Fx)}; variable cost ₹{v} per unit', f'Slope = ({Fx + v * x2} − {Fx + v * x1})/({x2} − {x1}) = {v} (1); C − {Fx + v * x1} = {v}(x − {x1}) ⇒ C = {v}x + {Fx} (1); interpret intercept and slope (1).',
             [f'C = {Fx}x + {v}; fixed cost ₹{v}; variable cost {inr(Fx)} per unit', f'C = {v}x + {Fx + v}; fixed cost {inr(Fx + v)}; variable cost ₹{v} per unit', f'C = {v + 5}x + {Fx}; fixed cost {inr(Fx)}; variable cost ₹{v + 5} per unit'])


def c13s3_be(r):
    v = r.choice([30, 40, 50, 60, 75])
    p = v + r.choice([20, 25, 30, 40, 50])
    Fx = (p - v) * r.choice([100, 120, 150, 200, 250, 300])
    q = Fx // (p - v)
    return Q(f'A firm\'s cost function is C(x) = {v}x + {Fx} and it sells each unit at ₹{p}. Find the break-even point. What is the profit when {q + 50} units are sold?',
             f'{q} units (revenue {inr(p * q)}); profit {inr((p - v) * 50)}', f'R(x) = {p}x; break-even when R = C: {p}x = {v}x + {Fx} ⇒ x = {q} (2); profit at {q + 50}: {p - v} × 50 = {inr((p - v) * 50)} (1).',
             [f'{q + 10} units (revenue {inr(p * (q + 10))}); profit {inr((p - v) * 40)}', f'{Fx // p} units (revenue {inr(p * (Fx // p))}); profit {inr((p - v) * 50)}', f'{q} units (revenue {inr(p * q)}); profit {inr(p * 50)}'])


def c13s3_eq(r):
    a, b = r.choice([(100, 2), (120, 3), (90, 1), (150, 5), (80, 2)])
    c, d = r.choice([(10, 1), (20, 2), (5, 1), (15, 3)])
    q = Fr(a - c, b + d)
    if q.denominator != 1 or q <= 0:
        raise ValueError
    p = a - b * q
    q1, q2 = 5, 15
    return Q(f'The demand for a product is 0 when the price is ₹{a} and {q2} units when the price is ₹{a - b * q2}; the supply function is p = {c} + {d if d != 1 else ""}q. '
             f'Assuming linear demand, find the demand function and the equilibrium price and quantity.', f'p = {a} − {b if b != 1 else ""}q; equilibrium q = {q}, p = ₹{p}',
             f'Demand line through (0, {a}) and ({q2}, {a - b * q2}): slope −{b}, p = {a} − {b}q (2). Equate with supply: {a} − {b}q = {c} + {d}q ⇒ q = {q} (2), p = {p} (1).',
             [f'p = {a} − {b}q; equilibrium q = {q + 2}, p = ₹{a - b * (q + 2)}', f'p = {a} + {b}q; equilibrium q = {q}, p = ₹{a + b * q}', f'p = {a} − {b}q; equilibrium q = {p}, p = ₹{q}'])


def c13s3_depr(r):
    C = r.choice([200000, 300000, 500000, 800000])
    life = r.choice([5, 8, 10])
    sv = r.choice([0, C // 10, C // 5])
    d = (C - sv) / life
    t = r.randint(2, life - 1)
    return Q(f'A machine costs {inr(C)} and has a scrap value of {inr(sv)} after {life} years. Using straight-line depreciation, write the value V as a linear function of time t (years) and find the value after {t} years.',
             f'V = {C} − {num(d)}t; {inr(C - d * t)}', f'Annual depreciation = ({C} − {sv})/{life} = {inr(d)} (1); V = {C} − {num(d)}t (1); V({t}) = {inr(C - d * t)} (1).',
             [f'V = {C} − {num(C / life)}t; {inr(C - C / life * t)}', f'V = {C} + {num(d)}t; {inr(C + d * t)}', f'V = {C} − {num(d)}t; {inr(C - d * (t + 1))}'])


def c13s3_ar(r):
    return pool_ar([
        ('In a linear cost function C = vx + F, the y-intercept F is the fixed cost.', 'When nothing is produced (x = 0), only the fixed cost is incurred.', 'a', 'R explains A.'),
        ('At the break-even point, profit is maximum.', 'At the break-even point, total revenue equals total cost.', 'd', 'A is false: profit is zero there. R is true.'),
        ('The slope of a linear demand curve is negative.', 'Quantity demanded falls as the price rises.', 'a', 'R explains A.'),
    ])(r)


# ======================================================== ch14 Applications of circles and parabolas


def c14s3_arch(r):
    span = r.choice([20, 24, 30, 40, 48, 60])
    h = r.choice([8, 9, 10, 12, 15, 16])
    d = r.choice([k for k in (2, 3, 4, 5, 6, 8, 10, 12) if k < span / 2])
    a = span / 2
    y = h * (1 - d * d / (a * a))
    return Q(f'A bridge has a parabolic arch {span} m wide at the base and {h} m high at the centre. Taking the vertex at (0, {h}) and the base on the x-axis, find the equation of the arch and its height at a point {d} m from the centre.',
             f'x² = −{fs(Fr(int(a * a), h))}(y − {h}); height {num(y, 2)} m', f'x² = −4p(y − {h}) passes through ({num(a)}, 0): 4p = {fs(Fr(int(a * a), h))} (2). At x = {d}: y = {h}(1 − {d}²/{num(a)}²) = {num(y, 2)} m (3).',
             [f'x² = −{fs(Fr(int(a * a), h))}(y − {h}); height {num(h - d * h / a, 2)} m', f'x² = {fs(Fr(int(a * a), h))}y; height {num(h * d * d / (a * a), 2)} m'])


def c14s3_dish(r):
    D = r.choice([60, 80, 100, 120, 160, 200, 240])
    dep = r.choice([10, 15, 20, 25, 30, 40])
    f = (D / 2) ** 2 / (4 * dep)
    return Q(f'A satellite dish has a parabolic cross-section {D} cm across and {dep} cm deep. Where should the receiver be placed (distance of the focus from the vertex)?', f'{num(f, 2)} cm from the vertex',
             f'Vertex at origin: y² = 4ax through ({dep}, {D // 2}) ⇒ {D // 2}² = 4a × {dep} ⇒ a = {num(f, 2)} cm; the receiver is at the focus.',
             [f'{num(f * 2, 2)} cm from the vertex', f'{num(D / 4, 2)} cm from the vertex', f'{num(dep, 2)} cm from the vertex'])


def c14s3_circle(r):
    h, k = r.randint(-5, 5), r.randint(-5, 5)
    rad = r.choice([5, 10, 13, 15, 25])
    px, py = h + r.randint(-rad - 3, rad + 3), k + r.randint(-rad - 3, rad + 3)
    d2 = (px - h) ** 2 + (py - k) ** 2
    pos = 'inside' if d2 < rad * rad else ('on' if d2 == rad * rad else 'outside')
    return Q(f'A mobile tower at ({h}, {k}) (units in km) covers a circular region of radius {rad} km. Write the equation of the boundary of the region and decide whether a village at ({px}, {py}) gets coverage.',
             f'(x {"−" if h >= 0 else "+"} {abs(h)})² + (y {"−" if k >= 0 else "+"} {abs(k)})² = {rad * rad}; the village is {pos} the circle ({"covered" if pos != "outside" else "not covered"})',
             f'Circle with centre ({h}, {k}), radius {rad} (1). Distance² from the tower = {d2} {"<" if d2 < rad * rad else ("=" if d2 == rad * rad else ">")} {rad * rad} (1).'.replace('− 0', '− 0'),
             [f'(x {"+" if h >= 0 else "−"} {abs(h)})² + (y {"+" if k >= 0 else "−"} {abs(k)})² = {rad * rad}; the village is {pos} the circle', f'x² + y² = {rad * rad}; the village is {pos} the circle'])


def c14s3_jet(r):
    a = r.choice([1, 2, 4])
    H = r.choice([4, 8, 9, 16])
    W = 2 * math.sqrt(4 * a * H)
    if abs(W - round(W)) > 1e-9:
        raise ValueError
    return Q(f'The water jet of a fountain follows the parabola x² = −{4 * a}(y − {H}) (in metres), with the ground along y = 0. Find the maximum height of the jet and the distance between the points where it meets the ground.',
             f'{H} m; {int(W)} m', f'Vertex (0, {H}) gives the maximum height {H} m (1). y = 0 ⇒ x² = {4 * a * H} ⇒ x = ±{int(W // 2)} (1); width {int(W)} m (1).', [f'{4 * a} m; {int(W)} m', f'{H} m; {int(W // 2)} m', f'{H} m; {4 * a * H} m'])


c14s3_mcq = pool_mcq([
    ('Rays parallel to the axis of a parabolic mirror, after reflection,', 'pass through the focus', ['pass through the vertex', 'become parallel to the directrix', 'pass through the centre of curvature only'], 'Reflective property of the parabola.'),
    ('The cross-section of a car headlight reflector is a', 'parabola', ['circle', 'ellipse', 'hyperbola'], 'A source at the focus gives a parallel beam.'),
    ('The path of a ball thrown obliquely (ignoring air resistance) is a', 'parabola', ['circle', 'straight line', 'ellipse'], 'Projectile motion.'),
    ('The locus of points at a fixed distance from a fixed point is a', 'circle', ['parabola', 'straight line', 'ellipse'], 'Definition of a circle.'),
])


def c14s3_ar(r):
    return pool_ar([
        ('The receiver of a dish antenna is placed at the focus of its parabolic surface.', 'Signals parallel to the axis are reflected through the focus of a parabola.', 'a', 'R explains A.'),
        ('A circular running track has all its points equidistant from its centre.', 'A circle is the set of points at a fixed distance from a fixed point.', 'a', 'R explains A.'),
        ('The cable of a suspension bridge carrying a uniform load hangs in the shape of a circle.', 'A cable carrying a load uniformly distributed along the horizontal takes the shape of a parabola.', 'd', 'A is false. R is true.'),
    ])(r)


def c14s3_explain(r):
    return pool_txt([
        ('Explain why the reflector of a torch is parabolic and where the bulb is placed.', 'Light from a source at the focus of a parabolic reflector is reflected parallel to the axis, giving a strong beam; the bulb is at the focus.', '2 marks.'),
        ('Give two real-life examples each of circles and parabolas.', 'Circles: wheels, circular tracks, ripples. Parabolas: dish antennas, headlight reflectors, path of a thrown ball, arches.', '1 + 1 marks.'),
    ])(r)


def c14s3_case(r):
    span = r.choice([40, 60, 80])
    sag = r.choice([10, 12, 15, 20])
    a = span / 2
    k = (a * a) / sag
    d = r.choice([5, 10, 15])
    y = d * d / k
    return {'stem': (f'The main cable of a suspension bridge hangs in a parabola. The towers are {span} m apart and the cable is {sag} m above its lowest point at the towers. Take the lowest point as the origin.\n'
                     f'(i) Write the form of the equation of the cable. (1)\n(ii) Find the equation of the cable. (1)\n(iii) Find the height of the cable above its lowest point at {d} m from the centre. (2)'),
            'answer': f'(i) x² = 4ay (ii) x² = {num(k, 2)}y (iii) {num(y, 2)} m', 'key': f'(i) vertex at origin, opening up (1). (ii) through ({num(a)}, {sag}) (1). (iii) y = {d}²/{num(k, 2)} (2).'}


def c12s1_mixed(r):
    st1, st2 = r.sample(['Maharashtra', 'Karnataka', 'Gujarat', 'Rajasthan', 'Punjab', 'Kerala', 'Bihar', 'Odisha', 'Assam'], 2)
    a, b = r.choice([12000, 18000, 25000, 40000]), r.choice([10000, 15000, 30000, 36000])
    g1, g2 = r.sample(GST_RATES, 2)
    t1, t2 = a * g1 / 100, b * g2 / 100
    return Q(f'A wholesaler in {st1} makes two sales in a month: goods worth {inr(a)} (GST {g1}%) to a shop in {st1}, and goods worth {inr(b)} (GST {g2}%) to a shop in {st2}. '
             f'Find the CGST, SGST and IGST collected, and the total tax. Which Government(s) finally receive each part?',
             f'CGST {inr(t1 / 2)}, SGST {inr(t1 / 2)}, IGST {inr(t2)}; total {inr(t1 + t2)}',
             f'Intra-state: CGST = SGST = {num(g1 / 2)}% of {inr(a)} = {inr(t1 / 2)} each (1); inter-state: IGST {g2}% of {inr(b)} = {inr(t2)} (1); total {inr(t1 + t2)} (½); '
             f'CGST to the Centre, SGST to {st1}, IGST collected by the Centre and the State share passed to the consuming State {st2} (1½).',
             [f'CGST {inr(t1 / 2)}, SGST {inr(t1 / 2)}, IGST {inr(t2 / 2)}; total {inr(t1 + t2 / 2)}', f'CGST {inr(t1)}, SGST {inr(t1)}, IGST {inr(t2)}; total {inr(2 * t1 + t2)}',
              f'IGST {inr(t1 + t2)}; total {inr(t1 + t2)}'])


def c13s1_par(r):
    m = r.choice([2, 3, -2, -3, 4, Fr(1, 2), Fr(-2, 3), Fr(3, 4), 5])
    m = Fr(m)
    kind = r.choice(['par', 'perp'])
    v = m if kind == 'par' else -1 / m
    return Q(f'A line has slope {fs(m)}. Find the slope of a line {"parallel" if kind == "par" else "perpendicular"} to it.', fs(v),
             f'{"Parallel lines have equal slopes" if kind == "par" else "Perpendicular lines have m₁m₂ = −1"}: {fs(v)}.', [fs(-m) if kind == 'par' else fs(m), fs(1 / m), fs(-1 / m) if kind == 'par' else fs(-m)])


def c13s1_coll(r):
    x1, y1 = r.randint(-5, 5), r.randint(-5, 5)
    dx, dy = r.choice([(1, 2), (2, 3), (1, -1), (3, 1), (2, -1)])
    k1, k2 = r.randint(1, 3), r.randint(4, 6)
    P, Qp, R = (x1, y1), (x1 + k1 * dx, y1 + k1 * dy), (x1 + k2 * dx, y1 + k2 * dy + r.choice([0, 0, 1]))
    m1, m2 = Fr(Qp[1] - P[1], Qp[0] - P[0]), Fr(R[1] - Qp[1], R[0] - Qp[0])
    ok = m1 == m2
    return {'stem': f'Using slopes, check whether the points A{P}, B{Qp} and C{R} are collinear. Explain your reasoning.',
            'answer': f'slope AB = {fs(m1)}, slope BC = {fs(m2)}; {"equal, so A, B, C are collinear" if ok else "unequal, so the points are not collinear"}.',
            'key': 'Both slopes (1); conclusion with reason that equal slopes through a common point B give one line (1).'}


def c13s1_ar(r):
    a, b = r.randint(1, 6), r.randint(1, 6)
    if r.random() < 0.5:
        return ar(f'The lines y = {a}x + 1 and y = {a}x − {b} are parallel.', 'Non-vertical lines are parallel if and only if their slopes are equal.', 'a', f'Both slopes are {a}; R explains A.')
    return ar(f'The lines y = {a}x + 1 and y = {fs(Fr(1, a))}x − {b} are perpendicular.', 'Two non-vertical lines are perpendicular if the product of their slopes is −1.', 'd',
              f'A is false: {a} × {fs(Fr(1, a))} = 1, not −1. R is true.')


# ======================================================== FAMILIES

FAMILIES = {
    S + '10-st1': [F('C1', 'D1', 'mcq', c10s1_type), F('C1', 'D2', 'mcq', c10s1_tf), F('C2', 'D2', 'explain', c10s1_expect), F('C2', 'D3', 'mcq', c10s1_ar, kinds=('ar',)),
                   F('C2', 'D2', 'short', c10s1_dir), F('C3', 'D2', 'numerical', c10s1_cov), F('C4', 'D3', 'multi_step', c10s1_cov4), F('C3', 'D3', 'case', c10s1_case, marks=4, minutes=6)],
    S + '10-st2': [F('C1', 'D1', 'mcq', c10s2_formula), F('C1', 'D2', 'mcq', c10s2_interp), F('C2', 'D2', 'explain', c10s2_explain), F('C2', 'D3', 'mcq', c10s2_ar, kinds=('ar',)),
                   F('C2', 'D2', 'short', c10s2_prop), F('C3', 'D1', 'short', c10s2_cov), F('C3', 'D3', 'numerical', c10s2_sums), F('C3', 'D4', 'numerical', c10s2_findsd),
                   F('C4', 'D4', 'long', c10s2_data, kinds=('long5',)), F('C4', 'D3', 'multi_step', c10s2_combo), F('C3', 'D3', 'case', c10s2_case, marks=4, minutes=6)],
    S + '10-st3': [F('C1', 'D1', 'mcq', c10s3_formula), F('C2', 'D2', 'explain', c10s3_explain), F('C2', 'D3', 'mcq', c10s3_ar, kinds=('ar',)), F('C2', 'D2', 'short', c10s3_d2),
                   F('C3', 'D2', 'numerical', c10s3_ranks), F('C3', 'D3', 'numerical', c10s3_scores), F('C4', 'D4', 'long', c10s3_err, kinds=('long5',)), F('C4', 'D4', 'multi_step', c10s3_three),
                   F('C3', 'D3', 'case', c10s3_case, marks=4, minutes=6)],
    S + '10-st4': [F('C1', 'D1', 'mcq', c10s4_formula), F('C2', 'D2', 'explain', c10s4_explain), F('C2', 'D3', 'mcq', c10s4_ar, kinds=('ar',)), F('C2', 'D2', 'short', c10s4_r),
                   F('C3', 'D1', 'short', c10s4_coef), F('C3', 'D2', 'numerical', c10s4_means), F('C3', 'D3', 'numerical', c10s4_predict), F('C4', 'D4', 'long', c10s4_data, kinds=('long5',)),
                   F('C3', 'D3', 'case', c10s4_case, marks=4, minutes=6)],
    S + '11-st1': [F('C1', 'D1', 'mcq', c11s1_mcq), F('C2', 'D2', 'explain', c11s1_explain), F('C2', 'D3', 'mcq', c11s1_ar, kinds=('ar',)), F('C2', 'D2', 'short', c11s1_eff),
                   F('C3', 'D1', 'short', c11s1_si), F('C3', 'D2', 'numerical', c11s1_ci), F('C3', 'D3', 'numerical', c11s1_freq), F('C3', 'D4', 'numerical', c11s1_diff),
                   F('C4', 'D3', 'multi_step', c11s1_rate), F('C3', 'D3', 'case', c11s1_case, marks=4, minutes=6)],
    S + '11-st2': [F('C1', 'D1', 'mcq', c11s2_mcq), F('C2', 'D2', 'explain', c11s2_explain), F('C2', 'D3', 'mcq', c11s2_ar, kinds=('ar',)), F('C3', 'D1', 'short', c11s2_fv),
                   F('C3', 'D2', 'numerical', c11s2_pv), F('C2', 'D2', 'short', c11s2_double), F('C4', 'D3', 'multi_step', c11s2_compare), F('C3', 'D3', 'case', c11s2_case, marks=4, minutes=6)],
    S + '11-st3': [F('C1', 'D1', 'mcq', c11s3_mcq), F('C2', 'D2', 'explain', c11s3_explain), F('C2', 'D3', 'mcq', c11s3_ar, kinds=('ar',)), F('C3', 'D1', 'short', c11s3_perp),
                   F('C3', 'D2', 'numerical', c11s3_fv), F('C3', 'D3', 'numerical', c11s3_pv), F('C4', 'D3', 'multi_step', c11s3_due), F('C4', 'D4', 'long', c11s3_sink, kinds=('long5',)),
                   F('C3', 'D3', 'case', c11s3_case, marks=4, minutes=6)],
    S + '12-st1': [F('C1', 'D1', 'mcq', c12s1_terms), F('C1', 'D2', 'mcq', c12s1_tf), F('C2', 'D2', 'explain', c12s1_explain), F('C2', 'D3', 'mcq', c12s1_ar, kinds=('ar',)),
                   F('C2', 'D2', 'mcq', c12s1_which), F('C3', 'D1', 'short', c12s1_split), F('C4', 'D3', 'multi_step', c12s1_mixed), F('C3', 'D3', 'numerical', c12s1_bill), F('C3', 'D3', 'case', c12s1_case, marks=4, minutes=6)],
    S + '12-st2': [F('C1', 'D2', 'mcq', c12s2_mcq), F('C2', 'D2', 'explain', c12s2_explain), F('C2', 'D3', 'mcq', c12s2_ar, kinds=('ar',)), F('C2', 'D2', 'short', c12s2_incl),
                   F('C3', 'D2', 'numerical', c12s2_itc), F('C3', 'D3', 'numerical', c12s2_disc), F('C3', 'D4', 'multi_step', c12s2_inter), F('C4', 'D4', 'long', c12s2_chain, kinds=('long5',)),
                   F('C3', 'D3', 'case', c12s2_case, marks=4, minutes=6)],
    S + '12-st3': [F('C1', 'D1', 'mcq', c12s3_mcq), F('C2', 'D2', 'explain', c12s3_explain), F('C2', 'D3', 'mcq', c12s3_ar, kinds=('ar',)), F('C3', 'D1', 'short', c12s3_cess),
                   F('C3', 'D3', 'numerical', c12s3_tax), F('C4', 'D4', 'long', c12s3_full, kinds=('long5',)), F('C3', 'D3', 'case', c12s3_case, marks=4, minutes=6)],
    S + '12-st4': [F('C1', 'D1', 'mcq', c12s4_mcq), F('C2', 'D2', 'explain', c12s4_explain), F('C2', 'D3', 'mcq', c12s4_ar, kinds=('ar',)), F('C2', 'D2', 'short', c12s4_appl),
                   F('C3', 'D1', 'short', c12s4_water), F('C3', 'D2', 'numerical', c12s4_meter), F('C4', 'D3', 'multi_step', c12s4_elec), F('C3', 'D3', 'case', c12s4_case, marks=4, minutes=6)],
    S + '13-st1': reuse('09-st1', skip=(0, 2, 3, 7)) + [F('C2', 'D2', 'short', c13s1_par), F('C2', 'D2', 'explain', c13s1_coll), F('C2', 'D3', 'mcq', c13s1_ar, kinds=('ar',))],
    S + '13-st2': reuse('09-st2') + reuse('09-st3', skip=(2, 5)),
    S + '13-st3': reuse('09-st4') + [F('C2', 'D3', 'mcq', c13s3_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c13s3_cost), F('C3', 'D3', 'numerical', c13s3_depr),
                                     F('C4', 'D3', 'multi_step', c13s3_be), F('C4', 'D4', 'long', c13s3_eq, kinds=('long5',))],
    S + '14-st1': reuse('10-st1', skip=(0,)),
    S + '14-st2': reuse('10-st2', skip=(7,)),
    S + '14-st3': [F('C1', 'D1', 'mcq', c14s3_mcq), F('C2', 'D2', 'explain', c14s3_explain), F('C2', 'D3', 'mcq', c14s3_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c14s3_circle),
                   F('C3', 'D3', 'numerical', c14s3_dish), F('C2', 'D2', 'short', c14s3_jet), F('C4', 'D4', 'long', c14s3_arch, kinds=('long5',)), F('C3', 'D3', 'case', c14s3_case, marks=4, minutes=6)],
}
