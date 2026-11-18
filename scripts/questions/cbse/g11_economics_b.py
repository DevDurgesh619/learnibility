"""CBSE class 11 Economics families: Statistics for Economics chapters 5-8 (answers computed in code)."""
from __future__ import annotations

import math
from fractions import Fraction

from qbank import mcq, ar, num, inr, name, two_names, num_distractors, CITIES
from g11_economics_lib import M, W, AR, G, pick_example, classify, cp, table, series, f2, rnd_mean_data

S = 'cbse-g11-economics-ch'


def d2(x):
    """2-decimal display, true minus."""
    return num(round(x, 2), 2)


def opts_num(ans, *c):
    return [d2(x) for x in c if d2(x) != d2(ans)][:3] + [d2(ans + 1.5), d2(ans - 2.25)]


WHO = [('marks', 'students'), ('daily wages (₹)', 'workers'), ('pocket money (₹ per week)', 'students'), ('runs scored', 'batsmen'), ('monthly sales (₹ thousand)', 'shops'),
       ('units of electricity used', 'households')]

# ====================================================================== ch05 st1 arithmetic mean


def am_ind(r):
    n = r.choice([5, 6, 7, 8])
    xs = rnd_mean_data(r, n, 10, 95)
    m = sum(xs) // n
    what, whom = r.choice(WHO)
    return {'stem': f'The {what} of {n} {whom} are {series(xs)}. Find the arithmetic mean.', 'answer': str(m),
            'key': f'Mean = Σx/N = {sum(xs)}/{n} = {m}.', 'distractors': num_distractors(m, sorted(xs)[n // 2], sum(xs) / (n - 1), m + 2)}


def am_assumed(r):
    n = r.choice([5, 6, 8])
    xs = rnd_mean_data(r, n, 120, 480, 5)
    A = r.choice(xs)
    d = [x - A for x in xs]
    m = A + Fraction(sum(d), n)
    return {'stem': f'Using the assumed mean method with A = {A}, find the mean of {series(xs)}.', 'answer': num(float(m)),
            'key': f'd = X − {A}: {series([num(x) for x in d])}; Σd = {num(sum(d))}; mean = A + Σd/N = {A} + ({num(sum(d))}/{n}) = {num(float(m))}.',
            'distractors': num_distractors(float(m), A, A + sum(d), float(m) + 5)}


def am_discrete(r):
    xs = sorted(r.sample(range(1, 11), 5))
    for _ in range(100):
        f = [r.randint(2, 12) for _ in xs]
        if (sum(a * b for a, b in zip(xs, f)) * 100) % sum(f) == 0:
            break
    m = sum(a * b for a, b in zip(xs, f)) / sum(f)
    what = r.choice(['children per family', 'rooms per house', 'members per household', 'vehicles per family'])
    return {'stem': f'Find the mean number of {what}:\n' + table(['X', *xs], [['f', *f]]), 'answer': d2(m),
            'key': f'Σf = {sum(f)}; Σfx = {sum(a * b for a, b in zip(xs, f))}; mean = Σfx/Σf = {d2(m)}.',
            'distractors': [d2(x) for x in (sum(xs) / 5, m + 0.5, m - 0.4)]}


def _cont(r, k=5):
    h = r.choice([10, 20])
    lo = h * r.randint(0, 3)
    f = [r.randint(3, 15) for _ in range(k)]
    cls = [(lo + i * h, lo + (i + 1) * h) for i in range(k)]
    return h, cls, f


def am_step(r):
    h, cls, f = _cont(r)
    mids = [(a + b) / 2 for a, b in cls]
    A = mids[2]
    dd = [(m - A) / h for m in mids]
    sfd = sum(x * y for x, y in zip(f, dd))
    mean = A + sfd / sum(f) * h
    return {'stem': 'Find the mean by the step-deviation method:\n' + table(['Class', *[f'{a}–{b}' for a, b in cls]], [['f', *f]]),
            'answer': d2(mean), 'key': f"Mid-values {series([num(m) for m in mids])}; A = {num(A)}, h = {h}; d' = (m − A)/h; Σf = {sum(f)}, Σfd' = {num(sfd)}; mean = A + (Σfd'/Σf) × h = {d2(mean)}.",
            'distractors': [d2(x) for x in (A + sfd / sum(f), A, mean + h / 2)]}


def am_missing(r):
    c0 = r.choice([5, 10])
    xs = [c0 * k for k in range(1, 6)]
    for _ in range(300):
        f = [r.randint(2, 12) for _ in xs]
        k = r.randrange(5)
        tot = sum(a * b for a, b in zip(xs, f))
        if (tot * 2) % sum(f) == 0:
            break
    else:
        raise ValueError('none')
    m = tot / sum(f)
    shown = [str(v) if i != k else 'p' for i, v in enumerate(f)]
    return {'stem': f'The mean of the following distribution is {num(m)}. Find the missing frequency p.\n' + table(['X', *xs], [['f', *shown]]),
            'answer': f'p = {f[k]}', 'key': f'Σf = {sum(f) - f[k]} + p; Σfx = {tot - xs[k] * f[k]} + {xs[k]}p; ({tot - xs[k] * f[k]} + {xs[k]}p)/({sum(f) - f[k]} + p) = {num(m)} ⇒ p = {f[k]}.'}


def am_weighted(r):
    who = name(r)
    subs = ['Economics', 'Accountancy', 'English', 'Mathematics']
    w = [r.randint(1, 4) for _ in subs]
    mk = [r.randint(55, 98) for _ in subs]
    wm = sum(a * b for a, b in zip(w, mk)) / sum(w)
    return {'stem': f'{who}\'s marks are ' + ', '.join(f'{s} {m}' for s, m in zip(subs, mk)) + '. The weights are ' + ', '.join(f'{s} {x}' for s, x in zip(subs, w)) + '. Find the weighted mean.',
            'answer': d2(wm), 'key': f'Weighted mean = Σwx/Σw = {sum(a * b for a, b in zip(w, mk))}/{sum(w)} = {d2(wm)}.', 'distractors': [d2(x) for x in (sum(mk) / 4, wm + 2, wm - 1.5)]}


def am_combined(r):
    n1, n2 = r.choice([20, 25, 30, 40]), r.choice([10, 15, 20, 50])
    m1, m2 = r.randint(40, 70), r.randint(45, 80)
    c = (n1 * m1 + n2 * m2) / (n1 + n2)
    return {'stem': f'Section A has {n1} students with mean marks {m1}; section B has {n2} students with mean marks {m2}. Find the combined mean marks.',
            'answer': d2(c), 'key': f'Combined mean = (n₁x̄₁ + n₂x̄₂)/(n₁ + n₂) = ({n1 * m1} + {n2 * m2})/{n1 + n2} = {d2(c)}.', 'distractors': [d2(x) for x in ((m1 + m2) / 2, c + 1, c - 1.2)]}


def am_corrected(r):
    n = r.choice([20, 25, 40, 50])
    m = r.randint(30, 60)
    wrong, right = r.sample(range(10, 90), 2)
    cm = (n * m - wrong + right) / n
    return {'stem': f'The mean of {n} observations was found to be {m}. Later it was discovered that one observation {right} was wrongly taken as {wrong}. Find the correct mean.',
            'answer': d2(cm), 'key': f'Correct Σx = {n} × {m} − {wrong} + {right} = {n * m - wrong + right}; correct mean = {n * m - wrong + right}/{n} = {d2(cm)}.',
            'distractors': [d2(x) for x in (m, (n * m + wrong - right) / n, cm + 1)]}


def am_shift(r):
    m = r.randint(20, 60)
    k = r.choice([2, 3, 5, 10])
    if r.random() < 0.5:
        return {'stem': f'The mean of a set of observations is {m}. If {k} is added to every observation, what is the new mean?', 'answer': str(m + k),
                'key': f'Adding a constant adds it to the mean: {m} + {k} = {m + k}.', 'distractors': num_distractors(m + k, m, m * k, m + 2 * k)}
    return {'stem': f'The mean of a set of observations is {m}. If every observation is multiplied by {k}, what is the new mean?', 'answer': str(m * k),
            'key': f'Multiplying by a constant multiplies the mean: {m} × {k} = {m * k}.', 'distractors': num_distractors(m * k, m, m + k, m * k + k)}


def ct_long(r):
    for _ in range(200):
        h, cls, f = _cont(r)
        k = f.index(max(f))
        if 0 < k < 4 and f.count(max(f)) == 1:
            break
    else:
        raise ValueError('no mode')
    N = sum(f)
    mids = [(a + b) / 2 for a, b in cls]
    mean = sum(m * x for m, x in zip(mids, f)) / N
    cf = [sum(f[:i + 1]) for i in range(5)]
    j = next(i for i, c in enumerate(cf) if c >= N / 2)
    c0 = cf[j - 1] if j else 0
    med = cls[j][0] + (N / 2 - c0) / f[j] * h
    D1, D2 = f[k] - f[k - 1], f[k] - f[k + 1]
    mo = cls[k][0] + D1 / (D1 + D2) * h
    return {'stem': 'For the following distribution, calculate the mean, the median and the mode. Comment on the shape of the distribution.\n' + table(['Class', *[f'{a}–{b}' for a, b in cls]], [['f', *f]]),
            'answer': f'Mean = {d2(mean)}; median = {d2(med)}; mode = {d2(mo)}; ' + ('mean > median > mode: positively skewed' if mean > med > mo else ('mean < median < mode: negatively skewed' if mean < med < mo else 'the averages are close / not in a strict skew order: roughly symmetrical or irregular')),
            'key': f'Mean: Σfm/N = {num(sum(m * x for m, x in zip(mids, f)))}/{N} = {d2(mean)} (2 marks). Median: N/2 = {num(N / 2)}, class {cls[j][0]}–{cls[j][1]}, = {cls[j][0]} + (({num(N / 2)} − {c0})/{f[j]}) × {h} = {d2(med)} (2 marks). '
                   f'Mode: class {cls[k][0]}–{cls[k][1]}, = {cls[k][0]} + {D1}/({D1} + {D2}) × {h} = {d2(mo)} (1½ marks). Comment ½ mark.'}


AM_FACT = [
    ('The sum of deviations of observations from their arithmetic mean is always', 'zero', ['one', 'minimum but not zero', 'equal to the mean'], 'Σ(X − X̄) = 0.'),
    ('The arithmetic mean is affected most by', 'extreme values', ['the middle value', 'the most frequent value', 'the number of classes'], 'All values enter the mean.'),
    ('In the step-deviation method, deviations are divided by', 'the common factor (class width) h', ['the number of items', 'the assumed mean', 'the total frequency'], "d' = (X − A)/h."),
    ('Which average cannot be calculated for open-ended classes without assumption?', 'Arithmetic mean', ['Median', 'Mode', 'Quartiles'], 'Mid-values of open classes are unknown.'),
]
AM_AR = [
    ('The arithmetic mean is affected by extreme values.', 'Every observation is used in computing the mean.', 'a', 'R explains A.'),
    ('The sum of deviations from the mean is zero.', 'Positive and negative deviations from the mean balance each other.', 'a', 'R explains A.'),
    ('The mean can be found for qualitative data such as honesty.', 'The mean uses the numerical value of every observation.', 'd', 'A is false; R is true.'),
    ('The assumed mean method gives a different answer from the direct method.', 'The assumed mean method only simplifies calculation.', 'd', 'A is false: same result; R is true.'),
]

# ====================================================================== st2 median


def med_ind(r):
    n = r.choice([7, 8, 9, 10, 11])
    xs = r.sample(range(10, 99), n)
    s = sorted(xs)
    med = s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
    what, whom = r.choice(WHO)
    return {'stem': f'Find the median of the {what} of {n} {whom}: {series(xs)}.', 'answer': num(med),
            'key': f'Arranged: {series(s)}; N = {n}; median = size of (N + 1)/2 = {num((n + 1) / 2)}th item = {num(med)}.',
            'distractors': num_distractors(med, xs[n // 2], sum(xs) / n, s[n // 2 - 1] if n % 2 else s[n // 2])}


def med_disc(r):
    xs = sorted(r.sample(range(10, 60, 5), 6))
    f = [r.randint(2, 14) for _ in xs]
    N = sum(f)
    cf = [sum(f[:i + 1]) for i in range(6)]
    pos = (N + 1) / 2
    med = next(x for x, c in zip(xs, cf) if c >= pos)
    return {'stem': 'Find the median of the following discrete series:\n' + table(['X', *xs], [['f', *f]]), 'answer': str(med),
            'key': f'cf: {series(cf)}; N = {N}; median = size of (N + 1)/2 = {num(pos)}th item; first cf ≥ {num(pos)} is at X = {med}.',
            'distractors': num_distractors(med, xs[f.index(max(f))], xs[2], xs[3])}


def med_cont(r):
    h, cls, f = _cont(r)
    N = sum(f)
    cf = [sum(f[:i + 1]) for i in range(5)]
    k = next(i for i, c in enumerate(cf) if c >= N / 2)
    L = cls[k][0]
    c0 = cf[k - 1] if k else 0
    med = L + (N / 2 - c0) / f[k] * h
    return {'stem': 'Calculate the median:\n' + table(['Class', *[f'{a}–{b}' for a, b in cls]], [['f', *f]]), 'answer': d2(med),
            'key': f'N/2 = {num(N / 2)}; median class {cls[k][0]}–{cls[k][1]}; L = {L}, cf = {c0}, f = {f[k]}, h = {h}; median = L + ((N/2 − cf)/f) × h = {d2(med)}.',
            'distractors': [d2(x) for x in (L + (N / 2 - c0) / f[k], (cls[k][0] + cls[k][1]) / 2, med + h / 4)]}


def quart(r):
    n = r.choice([7, 11, 15])
    xs = r.sample(range(10, 120), n)
    s = sorted(xs)
    q = r.choice([1, 3])
    pos = q * (n + 1) // 4
    v = s[pos - 1]
    return {'stem': f'Find the {"lower" if q == 1 else "upper"} quartile (Q{q}) of: {series(xs)}.', 'answer': str(v),
            'key': f'Arranged: {series(s)}; Q{q} = size of {q}(N + 1)/4 = {pos}th item = {v}.', 'distractors': num_distractors(v, s[pos], s[pos - 2], s[n // 2])}


MED_FACT = [
    ('The median divides a series into', 'two equal parts', ['four equal parts', 'ten equal parts', 'hundred equal parts'], 'Median = middle value.'),
    ('Quartiles divide a series into', 'four equal parts', ['two equal parts', 'ten equal parts', 'hundred equal parts'], 'Q1, Q2, Q3.'),
    ('The second quartile (Q2) is the same as the', 'median', ['mean', 'mode', 'range'], 'Q2 = P50 = median.'),
    ('The 25th percentile is equal to the', 'first quartile', ['median', 'third quartile', 'mode'], 'P25 = Q1.'),
    ('Percentiles divide a series into', 'hundred equal parts', ['ten equal parts', 'four equal parts', 'two equal parts'], 'P1 … P99.'),
    ('The median is not affected by', 'extreme values', ['the position of items', 'the number of items', 'arrangement in order'], 'Median depends on position only.'),
]
MED_AR = [
    ('The median is a positional average.', 'It is the value of the middle item when data are arranged in order.', 'a', 'R explains A.'),
    ('The median is greatly affected by extreme values.', 'The median depends on the middle position.', 'd', 'A is false; R is true.'),
    ('Q3 is greater than or equal to the median.', '75% of observations lie below Q3.', 'a', 'R explains A.'),
]

# ====================================================================== st3 mode


def mode_ind(r):
    base = r.sample(range(10, 60), 6)
    m = base[0]
    xs = base + [m, m] + [base[1]]
    r.shuffle(xs)
    return {'stem': f'Find the mode of: {series(xs)}.', 'answer': str(m), 'key': f'{m} occurs most often (3 times).', 'distractors': num_distractors(m, base[1], sorted(xs)[4], sum(xs) // len(xs))}


def mode_disc(r):
    xs = sorted(r.sample(range(2, 40, 2), 6))
    f = r.sample(range(2, 25), 6)
    m = xs[f.index(max(f))]
    return {'stem': 'Find the mode of the following series:\n' + table(['Size', *xs], [['f', *f]]), 'answer': str(m), 'key': f'Highest frequency {max(f)} is at size {m}.',
            'distractors': [str(x) for x in r.sample([x for x in xs if x != m], 3)]}


def mode_cont(r):
    for _ in range(200):
        h, cls, f = _cont(r)
        k = f.index(max(f))
        if 0 < k < 4 and f.count(max(f)) == 1:
            break
    else:
        raise ValueError('no mode')
    L = cls[k][0]
    D1, D2 = f[k] - f[k - 1], f[k] - f[k + 1]
    mo = L + D1 / (D1 + D2) * h
    return {'stem': 'Calculate the mode:\n' + table(['Class', *[f'{a}–{b}' for a, b in cls]], [['f', *f]]), 'answer': d2(mo),
            'key': f'Modal class {cls[k][0]}–{cls[k][1]}; L = {L}, D₁ = {f[k]} − {f[k - 1]} = {D1}, D₂ = {f[k]} − {f[k + 1]} = {D2}, h = {h}; mode = L + D₁/(D₁ + D₂) × h = {d2(mo)}.',
            'distractors': [d2(x) for x in ((cls[k][0] + cls[k][1]) / 2, L + D2 / (D1 + D2) * h, mo + h / 5)]}


def empirical(r):
    mean = r.randint(30, 80)
    med = mean + r.choice([-6, -4, -3, -2, 2, 3, 4, 6])
    mo = 3 * med - 2 * mean
    t = r.choice(['mode', 'median', 'mean'])
    if t == 'mode':
        return {'stem': f'In a moderately skewed distribution, the mean is {mean} and the median is {med}. Find the mode.', 'answer': str(mo),
                'key': f'Mode = 3 Median − 2 Mean = {3 * med} − {2 * mean} = {mo}.', 'distractors': num_distractors(mo, 3 * mean - 2 * med, (mean + med) / 2, 2 * med - mean)}
    if t == 'median':
        return {'stem': f'In a moderately skewed distribution, the mean is {mean} and the mode is {mo}. Find the median.', 'answer': num(med),
                'key': f'Median = (Mode + 2 Mean)/3 = ({mo} + {2 * mean})/3 = {num(med)}.', 'distractors': num_distractors(med, (mo + mean) / 2, 3 * mean - 2 * mo, med + 3)}
    return {'stem': f'In a moderately skewed distribution, the median is {med} and the mode is {mo}. Find the mean.', 'answer': num(mean),
            'key': f'Mean = (3 Median − Mode)/2 = ({3 * med} − {mo})/2 = {num(mean)}.', 'distractors': num_distractors(mean, (med + mo) / 2, 3 * med - 2 * mo, mean + 4)}


MODE_FACT = [
    ('The mode is the value that', 'occurs most frequently', ['lies in the middle', 'is the average of all values', 'divides the data into four parts'], 'Mode = most common value.'),
    ('A distribution with two modes is called', 'bimodal', ['unimodal', 'symmetrical', 'skewed'], 'Two modes → bimodal.'),
    ('Which average is most suitable for qualitative data such as the most popular colour?', 'Mode', ['Mean', 'Median', 'Weighted mean'], 'Mode works with attributes.'),
    ('In the formula Mode = L + D₁/(D₁ + D₂) × h, D₁ is', 'frequency of modal class minus frequency of the preceding class', ['frequency of modal class minus that of the next class',
     'total frequency', 'class width'], 'D₁ = f₁ − f₀.'),
]
MODE_AR = [
    ('A shoe-maker is most interested in the mode of shoe sizes.', 'The mode shows the size demanded by the largest number of customers.', 'a', 'R explains A.'),
    ('Every distribution has exactly one mode.', 'Some distributions are bimodal.', 'd', 'A is false; R is true.'),
    ('The mode is not affected by extreme values.', 'The mode depends only on the most frequent value.', 'a', 'R explains A.'),
]

# ====================================================================== st4 relative position
SUIT = [('A shoe company deciding which size to produce most', 'Mode'), ('Average intelligence of students ranked by teachers', 'Median'),
        ('Average income of a town where a few people are very rich', 'Median'), ('Total wage bill to be estimated from the average wage', 'Arithmetic mean'),
        ('A distribution with open-ended classes', 'Median'), ('The most common colour of cars sold', 'Mode'), ('Average marks of a class to compare with another class mathematically', 'Arithmetic mean')]
REL = [
    ('In a symmetrical distribution', 'mean = median = mode', ['mean > median > mode', 'mean < median < mode', 'median > mean > mode'], 'All coincide.'),
    ('In a positively skewed distribution', 'mean > median > mode', ['mean = median = mode', 'mode > median > mean', 'median > mean > mode'], 'Long tail to the right pulls the mean up.'),
    ('In a negatively skewed distribution', 'mean < median < mode', ['mean > median > mode', 'mean = median = mode', 'mode < mean < median'], 'Long tail to the left.'),
    ('Income distribution in India, with a few very high incomes, is', 'positively skewed', ['negatively skewed', 'symmetrical', 'bimodal by definition'], 'Few very rich → right tail.'),
]
REL_AR = [
    ('In a positively skewed distribution, the mean is greater than the median.', 'Extreme high values pull the mean upward.', 'a', 'R explains A.'),
    ('Median is the best average for data with extreme values.', 'Median is not affected by extreme values.', 'a', 'R explains A.'),
    ('Mean is the most suitable average for qualitative data.', 'Mean requires numerical values.', 'd', 'A is false; R is true.'),
]


def rel_skew(r):
    a, b, c = sorted(r.sample(range(30, 90), 3))
    kind = r.choice(['pos', 'neg'])
    if kind == 'pos':
        mean, med, mo = c, b, a
        ans = 'Positively skewed'
    else:
        mean, med, mo = a, b, c
        ans = 'Negatively skewed'
    return mcq(f'For a distribution, mean = {mean}, median = {med} and mode = {mo}. The distribution is', ans,
               [x for x in ['Positively skewed', 'Negatively skewed', 'Symmetrical', 'Uniform with no mode'] if x != ans],
               f'{"Mean > median > mode" if kind == "pos" else "Mean < median < mode"} ⇒ {ans.lower()}.', r)


def ct_case(r):
    who = name(r)
    city = r.choice(CITIES)
    inc = sorted(r.sample(range(12, 40), 6)) + [r.randint(180, 400)]
    s = sorted(inc)
    mean = sum(inc) / 7
    med = s[3]
    return {'stem': (f'{who} collected the monthly incomes (₹ thousand) of seven families in a {city} housing society: {series(inc)}.\n'
                     '(i) Find the mean income. (ii) Find the median income. (iii) Which average better represents a typical family here and why? (iv) What kind of skewness do these data show?'),
            'answer': f'(i) {d2(mean)} (ii) {med} (iii) median, because one very high income pulls the mean up (iv) positive skewness (mean > median)',
            'key': '1 mark each.'}


# ====================================================================== ch06 correlation
CORR_EX = [('Price of a good and the quantity demanded', 'Negative correlation'), ('Income and consumption expenditure', 'Positive correlation'),
           ('Hours of study and marks obtained', 'Positive correlation'), ('Temperature and sale of woollen clothes', 'Negative correlation'),
           ('Rainfall and crop yield (within normal range)', 'Positive correlation'), ('Height of students and their intelligence', 'No correlation'),
           ('Shoe size and monthly income of adults', 'No correlation'), ('Price of a good and its supply', 'Positive correlation'), ('Speed of a vehicle and time taken for a fixed distance', 'Negative correlation')]
CORR_FACT = [
    ('The value of the coefficient of correlation lies between', '−1 and +1', ['0 and 1', '−∞ and +∞', '0 and 100'], '−1 ≤ r ≤ 1.'),
    ('If all points of a scatter diagram lie on a straight line rising upward, r =', '+1', ['−1', '0', '0.5'], 'Perfect positive correlation.'),
    ('If r = 0, it means there is', 'no linear correlation', ['perfect correlation', 'perfect negative correlation', 'a very strong relationship'], 'r measures linear relationship.'),
    ('A scatter diagram shows', 'the nature of relationship between two variables visually', ['the exact value of r', 'the mean of the data', 'the median of the data'], 'Visual, not exact.'),
    ('Correlation between two variables', 'does not necessarily mean that one causes the other', ['always proves causation', 'is always positive', 'can exceed 1'],
     'Correlation ≠ causation.'),
    ('When the two variables move in opposite directions, the correlation is', 'negative', ['positive', 'zero', 'perfect positive'], 'Inverse movement.'),
]
CORR_AR = [
    ('Correlation does not imply causation.', 'Two variables may be correlated because both are affected by a third variable.', 'a', 'R explains A.'),
    ('The correlation between price and quantity demanded is negative.', 'By the law of demand, demand falls when price rises.', 'a', 'R explains A.'),
    ('r = 1.2 shows very strong positive correlation.', 'r always lies between −1 and +1.', 'd', 'A is false; R is true.'),
    ('A scatter diagram gives the exact degree of correlation.', 'A scatter diagram only shows the direction and rough closeness of the relation.', 'd', 'A is false; R is true.'),
]


def scatter_desc(r):
    rows = [('points cluster closely around a straight line rising from left to right', 'High positive correlation'),
            ('points cluster closely around a straight line falling from left to right', 'High negative correlation'),
            ('points are scattered with no visible pattern', 'No correlation'),
            ('points lie exactly on a straight line falling from left to right', 'Perfect negative correlation'),
            ('points lie exactly on a straight line rising from left to right', 'Perfect positive correlation')]
    d, t = cp('scat', r, rows)
    return mcq(f'In a scatter diagram, {d}. This shows', t, r.sample([x for _, x in rows if x != t], 3), f'{t}.', r)


def _corr_data(r, n):
    for _ in range(500):
        x = rnd_mean_data(r, n, 2, 30)
        b = r.choice([1, 2, -1, -2])
        y = [b * v + r.randint(-6, 6) + (40 if b > 0 else 70) for v in x]
        if sum(y) % n == 0 and len(set(y)) == n:
            return x, y
    raise ValueError('no corr data')


def pearson(r):
    n = r.choice([5, 6])
    x, y = _corr_data(r, n)
    mx, my = sum(x) // n, sum(y) // n
    dx = [a - mx for a in x]
    dy = [b - my for b in y]
    sxy = sum(a * b for a, b in zip(dx, dy))
    sx2 = sum(a * a for a in dx)
    sy2 = sum(b * b for b in dy)
    rr = sxy / math.sqrt(sx2 * sy2)
    return {'stem': 'Calculate Karl Pearson\'s coefficient of correlation:\n' + table(['X', *x], [['Y', *y]]), 'answer': f'r = {rr:.2f}'.replace('-', '−'),
            'key': f'X̄ = {mx}, Ȳ = {my}; with x = X − X̄, y = Y − Ȳ: Σxy = {num(sxy)}, Σx² = {sx2}, Σy² = {sy2}; r = Σxy/√(Σx²·Σy²) = {num(sxy)}/√({sx2} × {sy2}) = {rr:.2f}.'.replace('-', '−'),
            'distractors': [f'{v:.2f}'.replace('-', '−') for v in (-rr, rr / 2, min(0.99, abs(rr) + 0.1))]}


def pearson_sum(r):
    n = r.choice([8, 10, 12])
    x = [r.randint(1, 20) for _ in range(n)]
    sg, k = r.choice([1, -1]), r.randint(3, 12)
    y = [(2 * v if sg > 0 else 60 - 2 * v) + r.randint(-k, k) for v in x]
    SX, SY = sum(x), sum(y)
    SX2, SY2, SXY = sum(v * v for v in x), sum(v * v for v in y), sum(a * b for a, b in zip(x, y))
    num_ = n * SXY - SX * SY
    den = math.sqrt((n * SX2 - SX ** 2) * (n * SY2 - SY ** 2))
    if den == 0:
        raise ValueError('den')
    rr = num_ / den
    return {'stem': f'For {n} pairs of observations: ΣX = {SX}, ΣY = {SY}, ΣX² = {SX2}, ΣY² = {SY2}, ΣXY = {SXY}. Find the coefficient of correlation.',
            'answer': f'r = {rr:.2f}'.replace('-', '−'),
            'key': f'r = (NΣXY − ΣXΣY)/√[(NΣX² − (ΣX)²)(NΣY² − (ΣY)²)] = {num_}/√({n * SX2 - SX ** 2} × {n * SY2 - SY ** 2}) = {rr:.2f}.'.replace('-', '−')}


def corr_prop(r):
    rr = r.choice([0.45, 0.62, 0.78, -0.35, -0.56, 0.84])
    a, b = r.choice([3, 5, 10, 20]), r.choice([2, 4, 5])
    ans = f'{rr:.2f}'.replace('-', '−')
    return {'stem': f'The coefficient of correlation between X and Y is {ans}. If U = (X − {a * 10})/{b} and V = (Y − {a})/{b * 2}, what is the correlation between U and V?',
            'answer': ans, 'key': 'r is independent of change of origin and of scale (positive divisors), so r(U, V) = r(X, Y).',
            'distractors': [f'{v:.2f}'.replace('-', '−') for v in (rr / b, -rr, rr * b / 10)]}


def spearman(r):
    n = r.choice([5, 6, 7, 8])
    r1 = list(range(1, n + 1))
    r.shuffle(r1)
    r2 = r1[:]
    for _ in range(r.randint(1, 3)):
        i, j = r.sample(range(n), 2)
        r2[i], r2[j] = r2[j], r2[i]
    if r.random() < 0.3:
        r2 = [n + 1 - v for v in r2]
    d2s = sum((a - b) ** 2 for a, b in zip(r1, r2))
    rs = 1 - 6 * d2s / (n ** 3 - n)
    who = two_names(r)
    return {'stem': f'Two judges, {who[0]} and {who[1]}, ranked {n} entries in a debate competition:\n' + table(['Judge 1', *r1], [['Judge 2', *r2]]) + "\nFind Spearman's rank correlation coefficient.",
            'answer': f'rs = {rs:.2f}'.replace('-', '−'), 'key': f'Σd² = {d2s}; rs = 1 − 6Σd²/(n³ − n) = 1 − {6 * d2s}/{n ** 3 - n} = {rs:.2f}.'.replace('-', '−'),
            'distractors': [f'{v:.2f}'.replace('-', '−') for v in (1 - d2s / (n ** 3 - n), -rs if rs else 0.5, 1 - 6 * d2s / (n * n - 1))]}


def spearman_vals(r):
    n = r.choice([5, 6])
    x = r.sample(range(20, 90), n)
    y = [v + r.randint(-25, 25) for v in x]
    if len(set(y)) < n:
        raise ValueError('tie')
    rx = [sorted(x, reverse=True).index(v) + 1 for v in x]
    ry = [sorted(y, reverse=True).index(v) + 1 for v in y]
    d2s = sum((a - b) ** 2 for a, b in zip(rx, ry))
    rs = 1 - 6 * d2s / (n ** 3 - n)
    return {'stem': "Marks of students in Economics (X) and Statistics (Y) are given. Find Spearman's rank correlation (rank the highest as 1).\n" + table(['X', *x], [['Y', *y]]),
            'answer': f'rs = {rs:.2f}'.replace('-', '−'), 'key': f'Ranks X: {series(rx)}; ranks Y: {series(ry)}; Σd² = {d2s}; rs = 1 − 6Σd²/(n³ − n) = {rs:.2f}.'.replace('-', '−')}


def spearman_back(r):
    n = r.choice([6, 8, 10])
    d2s = r.randint(4, int((n ** 3 - n) / 6))
    rs = 1 - 6 * d2s / (n ** 3 - n)
    return {'stem': f"The rank correlation coefficient between two series of {n} items is {rs:.3f}. Find Σd².".replace('-', '−'), 'answer': str(d2s),
            'key': f'{rs:.3f} = 1 − 6Σd²/{n ** 3 - n} ⇒ Σd² = (1 − {rs:.3f}) × {n ** 3 - n}/6 = {d2s}.'.replace('-', '−'), 'distractors': num_distractors(d2s, d2s * 6, d2s // 2, d2s + n)}


def tie_rank(r):
    vals = sorted(r.sample(range(40, 95), 5), reverse=True)
    i = r.randrange(4)
    vals.insert(i + 1, vals[i])
    rank = i + 1.5
    return {'stem': f'Marks of six students are {series(vals)}. If the highest mark is ranked 1, what rank is given to each of the two students scoring {vals[i]}?',
            'answer': num(rank), 'key': f'They occupy ranks {i + 1} and {i + 2}; each gets the average ({i + 1} + {i + 2})/2 = {num(rank)}.',
            'distractors': num_distractors(rank, i + 1, i + 2, rank + 1)}


SPEAR_FACT = [
    ('Spearman\'s rank correlation is especially useful when', 'data are qualitative and can only be ranked (e.g. beauty, honesty)', ['data have no order', 'only means are known', 'data are in classes'],
     'Ranks suit qualitative attributes.'),
    ('The formula for rank correlation (no ties) is', 'rs = 1 − 6Σd²/(n³ − n)', ['rs = Σxy/√(Σx²Σy²)', 'rs = 1 + 6Σd²/(n³ − n)', 'rs = Σd/n'], 'Spearman\'s formula.'),
    ('If two series have identical ranks, Σd² equals', '0 and rs = +1', ['1 and rs = 0', 'n and rs = −1', '0 and rs = 0'], 'd = 0 for every pair.'),
    ('When ranks are tied, each tied item is given', 'the average of the ranks they would occupy', ['the highest rank', 'the lowest rank', 'rank zero'], 'Average rank.'),
]
SPEAR_AR = [
    ('Rank correlation can be used for qualitative data.', 'Qualitative items can be ranked even if they cannot be measured.', 'a', 'R explains A.'),
    ('If ranks of two series are exactly reversed, rs = −1.', 'Σd² takes its maximum value in that case.', 'a', 'Maximum Σd² gives rs = −1.'),
    ('Spearman\'s coefficient can be greater than 1.', 'rs lies between −1 and +1.', 'd', 'A is false; R is true.'),
]

# ====================================================================== ch07 index numbers
IDX_FACT = [
    ('An index number measures', 'relative change in a group of related variables over time or place', ['the absolute value of one item', 'the mean of a series', 'the correlation of two series'],
     'Index = relative change.'),
    ('The value of an index number for the base year is', '100', ['0', '1000', '50'], 'Base = 100.'),
    ('The base year should be', 'a normal year without unusual events like floods or wars', ['a year of war', 'the year of highest prices', 'any year chosen at random'], 'Normal base year.'),
    ('Weights in an index number indicate', 'the relative importance of items', ['the number of items', 'the base year', 'the price of the costliest item'], 'Weights = importance.'),
    ('Laspeyres\' price index uses as weights the', 'base-year quantities', ['current-year quantities', 'prices of the base year', 'average of both years\' quantities'], 'Σp₁q₀/Σp₀q₀.'),
    ('Paasche\'s price index uses as weights the', 'current-year quantities', ['base-year quantities', 'base-year prices', 'average prices'], 'Σp₁q₁/Σp₀q₁.'),
]
IDX_AR = [
    ('An index number for the base year is always 100.', 'The base year is the period of comparison.', 'a', 'Base values are taken as 100 for comparison.'),
    ('A simple aggregative index gives importance to items according to their use.', 'In a simple aggregative index, all items are treated as equally important.', 'd', 'A is false; R is true.'),
    ('Laspeyres\' index uses base-year quantities as weights.', 'Base-year quantities are fixed and known.', 'b', 'Both true; R is a convenience, not the definition.'),
    ('The base year should be a normal year.', 'Comparisons with an abnormal year mislead.', 'a', 'R explains A.'),
]
GOODS = [('Rice (kg)', 30, 60), ('Wheat (kg)', 20, 45), ('Milk (litre)', 40, 70), ('Sugar (kg)', 30, 50), ('Pulses (kg)', 70, 130), ('Cooking oil (litre)', 90, 180)]


def _basket(r, k=4):
    g = r.sample(GOODS, k)
    p0 = [r.randint(a, b) for _, a, b in g]
    p1 = [p + r.randint(-3, 25) for p in p0]
    return [x[0] for x in g], p0, p1


def idx_simple(r):
    names, p0, p1 = _basket(r)
    I = sum(p1) / sum(p0) * 100
    return {'stem': 'Construct the simple aggregative price index for 2024 with 2015 as base:\n' + table(['Item', *names], [['Price 2015 (₹)', *p0], ['Price 2024 (₹)', *p1]]),
            'answer': d2(I), 'key': f'P₀₁ = Σp₁/Σp₀ × 100 = {sum(p1)}/{sum(p0)} × 100 = {d2(I)}.', 'distractors': [d2(x) for x in (sum(p0) / sum(p1) * 100, I - 100, I + 5)]}


def idx_relatives(r):
    names, p0, p1 = _basket(r, 3)
    rel = [b / a * 100 for a, b in zip(p0, p1)]
    I = sum(rel) / 3
    return {'stem': 'Find the price index by the simple average of price relatives method:\n' + table(['Item', *names], [['Base-year price (₹)', *p0], ['Current-year price (₹)', *p1]]),
            'answer': d2(I), 'key': f'Price relatives (p₁/p₀ × 100): {series([d2(x) for x in rel])}; index = ΣR/N = {d2(I)}.', 'distractors': [d2(x) for x in (sum(p1) / sum(p0) * 100 + 1.37, I + 3, I - 4)]}


def idx_lasp(r):
    names, p0, p1 = _basket(r, 3)
    q0 = [r.randint(2, 12) for _ in names]
    q1 = [q + r.randint(-2, 3) for q in q0]
    q1 = [max(1, q) for q in q1]
    L = sum(a * b for a, b in zip(p1, q0)) / sum(a * b for a, b in zip(p0, q0)) * 100
    P = sum(a * b for a, b in zip(p1, q1)) / sum(a * b for a, b in zip(p0, q1)) * 100
    kind = r.choice(['Laspeyres', 'Paasche'])
    tbl = table(['Item', *names], [['p₀ (₹)', *p0], ['q₀', *q0], ['p₁ (₹)', *p1], ['q₁', *q1]])
    if kind == 'Laspeyres':
        return {'stem': "Calculate Laspeyres' price index:\n" + tbl, 'answer': d2(L),
                'key': f'Σp₁q₀ = {sum(a * b for a, b in zip(p1, q0))}, Σp₀q₀ = {sum(a * b for a, b in zip(p0, q0))}; index = Σp₁q₀/Σp₀q₀ × 100 = {d2(L)}.',
                'distractors': [d2(x) for x in (P if d2(P) != d2(L) else P + 1, L + 4, sum(p1) / sum(p0) * 100 + 0.73)]}
    return {'stem': "Calculate Paasche's price index:\n" + tbl, 'answer': d2(P),
            'key': f'Σp₁q₁ = {sum(a * b for a, b in zip(p1, q1))}, Σp₀q₁ = {sum(a * b for a, b in zip(p0, q1))}; index = Σp₁q₁/Σp₀q₁ × 100 = {d2(P)}.',
            'distractors': [d2(x) for x in (L if d2(P) != d2(L) else L + 1, P - 3, sum(p1) / sum(p0) * 100 + 0.61)]}


def idx_weighted_rel(r):
    heads = ['Food', 'Clothing', 'Fuel and light', 'House rent', 'Miscellaneous']
    w = [r.choice([20, 25, 30, 35, 40]), r.choice([10, 15]), r.choice([5, 10]), r.choice([15, 20]), r.choice([10, 15])]
    R = [r.randint(105, 180) for _ in heads]
    I = sum(a * b for a, b in zip(w, R)) / sum(w)
    return {'stem': 'Construct the consumer price index from the group indices and weights:\n' + table(['Group', *heads], [['Index (R)', *R], ['Weight (W)', *w]]),
            'answer': d2(I), 'key': f'CPI = ΣRW/ΣW = {sum(a * b for a, b in zip(w, R))}/{sum(w)} = {d2(I)}.', 'distractors': [d2(x) for x in (sum(R) / 5, I + 6, I - 5)]}


INDICES = [
    ('The Consumer Price Index (CPI) measures', 'changes in retail prices of a basket of goods and services bought by consumers', ['changes in wholesale prices of goods', 'changes in industrial output',
     'changes in share prices'], 'CPI = retail prices paid by consumers.'),
    ('The Wholesale Price Index (WPI) is based on prices of', 'goods traded in bulk (wholesale)', ['services only', 'retail prices of food only', 'shares on the stock exchange'],
     'WPI covers goods at the wholesale level.'),
    ('The current base year of India\'s Wholesale Price Index is', '2011–12', ['2004–05', '2015–16', '1993–94'], 'WPI base 2011–12.'),
    ('The Index of Industrial Production (IIP) measures', 'changes in the volume of industrial output', ['changes in prices of industrial goods', 'changes in wages', 'changes in exports'],
     'IIP = quantity index of industry.'),
    ('The SENSEX is the stock price index of the', 'Bombay Stock Exchange (BSE), based on 30 stocks', ['National Stock Exchange, based on 50 stocks', 'Reserve Bank of India',
     'National Sample Survey Office'], 'SENSEX = BSE 30.'),
    ('The base year of the SENSEX is', '1978–79', ['1991–92', '2004–05', '2011–12'], 'SENSEX base 1978–79 = 100.'),
    ('NIFTY 50 is the index of the', 'National Stock Exchange (NSE)', ['Bombay Stock Exchange', 'Reserve Bank of India', 'Central Statistics Office'], 'NSE index of 50 stocks.'),
    ('The index commonly used in India to measure inflation for wage adjustment and dearness allowance is the', 'Consumer Price Index', ['Index of Industrial Production', 'SENSEX', 'NIFTY'],
     'CPI reflects cost of living.'),
]
IND_AR = [
    ('CPI is used to measure the cost of living.', 'CPI is based on retail prices of goods and services bought by consumers.', 'a', 'R explains A.'),
    ('IIP is a price index.', 'IIP measures changes in the volume of industrial production.', 'd', 'A is false; IIP is a quantity index; R is true.'),
    ('A rising SENSEX reflects optimism in the share market.', 'SENSEX is based on share prices of 30 companies on the BSE.', 'a', 'R explains A.'),
]


def inflation(r):
    a = r.randint(120, 190)
    b = a + r.randint(2, 14) + r.random()
    b = round(b, 1)
    inf = (b - a) / a * 100
    y = r.randint(2018, 2023)
    return {'stem': f'The CPI was {a} in {y} and {num(b, 1)} in {y + 1}. Calculate the rate of inflation.', 'answer': f'{d2(inf)}%',
            'key': f'Inflation = (CPI₁ − CPI₀)/CPI₀ × 100 = ({num(b, 1)} − {a})/{a} × 100 = {d2(inf)}%.', 'distractors': [f'{d2(x)}%' for x in (b - a, (b - a) / b * 100, inf * 2)]}


def real_wage(r):
    who = name(r)
    w = r.choice([18000, 24000, 30000, 36000, 42000])
    cpi = r.choice([120, 125, 150, 160, 175, 200, 240])
    rw = w / cpi * 100
    return {'stem': f'{who}\'s monthly money wage is {inr(w)} and the consumer price index (base = 100) is {cpi}. Find the real wage.', 'answer': inr(round(rw, 2)),
            'key': f'Real wage = money wage/CPI × 100 = {w}/{cpi} × 100 = {inr(round(rw, 2))}.', 'distractors': [inr(round(x, 2)) for x in (w * cpi / 100, w - cpi, rw * 1.1)]}


def needed_wage(r):
    w0 = r.choice([15000, 20000, 25000, 30000])
    c0, c1 = 100, r.choice([118, 125, 132, 140, 150, 160])
    need = w0 * c1 / c0
    return {'stem': f'A worker earned {inr(w0)} per month when the CPI was {c0}. The CPI is now {c1}. What wage should she get now to keep the same standard of living?',
            'answer': inr(need), 'key': f'Required wage = {w0} × {c1}/{c0} = {inr(need)}.', 'distractors': [inr(x) for x in (w0 + c1, w0 * c0 / c1, need + 1000)]}


def purchasing(r):
    cpi = r.choice([125, 160, 200, 250, 400])
    pp = 100 / cpi
    return {'stem': f'If the consumer price index rises from 100 to {cpi}, what is the purchasing power of a rupee compared with the base year?', 'answer': f'₹{pp:.2f}',
            'key': f'Purchasing power = 100/CPI = 100/{cpi} = ₹{pp:.2f}.', 'distractors': [f'₹{x:.2f}' for x in (cpi / 100, 1 - pp, pp + 0.1)]}


USE_FACT = [
    ('Index numbers help the government to', 'adjust dearness allowance and frame price policy', ['count the population', 'collect primary data', 'draw pie diagrams'], 'Use in policy and wage adjustment.'),
    ('If money wages rise by 10% and prices rise by 15%, real wages', 'fall', ['rise', 'stay the same', 'double'], 'Real wage falls when prices rise faster.'),
    ('The purchasing power of money and the price level are', 'inversely related', ['directly related', 'unrelated', 'always equal'], 'Higher prices → lower purchasing power.'),
]
USE_AR = [
    ('Real wages fall when prices rise faster than money wages.', 'Real wage = money wage/price index × 100.', 'a', 'R explains A.'),
    ('Inflation increases the purchasing power of money.', 'Purchasing power = 100/price index.', 'd', 'A is false; R is true.'),
]

# ====================================================================== ch08 use of statistical tools
TOOLS = [('Share of different crops in total cultivated area', 'Pie diagram'), ('Change in petrol prices month by month over two years', 'Arithmetic line graph'),
         ('Whether hours of TV watching and marks are related', 'Coefficient of correlation'), ('The most popular brand of toothpaste in a locality', 'Mode'),
         ('Average monthly income of households with a few very rich families', 'Median'), ('Distribution of daily wages of workers in class intervals', 'Histogram'),
         ('Change in the cost of living of factory workers over years', 'Consumer price index')]
PROJECT_STEPS = ['Identify the problem', 'Choose the target group', 'Prepare the questionnaire', 'Collect the data', 'Organise and present the data', 'Analyse and interpret the data', 'Write the conclusion/report']
PROJ_FACT = [
    ('The first step in a statistical project is to', 'identify the problem or area of study', ['draw diagrams', 'calculate averages', 'write the conclusion'], 'Begin with the problem.'),
    ('The group of people about whom information is sought in a project is the', 'target group', ['sample error', 'control variable', 'class interval'], 'Target group = respondents.'),
    ('Data in a project should be presented with tables and diagrams because', 'they make the findings easy to understand and compare', ['they replace analysis', 'they remove errors',
     'they are compulsory for primary data only'], 'Presentation aids understanding.'),
    ('Before the main survey of a project, the questionnaire should be', 'pre-tested in a pilot survey', ['made longer', 'sent without checking', 'filled by the investigator himself'], 'Pilot survey.'),
    ('The final part of a project report usually contains', 'conclusions and suggestions', ['the raw questionnaires only', 'the title page only', 'tally marks'], 'Report ends with conclusions.'),
]
PROJ_AR = [
    ('A clear objective must be set before collecting data for a project.', 'The objective decides what data and which tools are needed.', 'a', 'R explains A.'),
    ('The conclusion of a project is written before collecting the data.', 'The conclusion depends on analysis of the data.', 'd', 'A is false; R is true.'),
    ('A pie diagram suits data on the share of expenditure heads.', 'A pie diagram shows the parts of a whole.', 'a', 'R explains A.'),
]


def tool_choose(r):
    d, t = cp('tool', r, TOOLS)
    return mcq(f'In a project, which statistical tool is most suitable for studying: {d}?', t, r.sample([x for _, x in TOOLS if x != t], 3), f'{t} suits this.', r)


def proj_order(r):
    idx = sorted(r.sample(range(len(PROJECT_STEPS)), 4))
    pick = [PROJECT_STEPS[i] for i in idx]
    sh = pick[:]
    while sh == pick:
        r.shuffle(sh)
    return {'stem': 'Arrange these steps of a statistical project in the correct order: ' + '; '.join(f'({i + 1}) {s}' for i, s in enumerate(sh)), 'answer': ' → '.join(pick),
            'key': '1 mark for correct order.'}


def proj_case(r):
    who = name(r)
    topic, tg = r.choice([('consumer awareness about food labels', 'shoppers at local grocery stores'), ('use of public transport', 'office-goers in the city'),
                          ('household waste segregation', 'families in two residential colonies'), ('screen time and sleep', 'students of Classes 9–12'),
                          ('use of digital payments', 'small shopkeepers in the market')])
    city = r.choice(CITIES)
    return {'stem': (f'{who} is doing a Class 11 project on "{topic}" in {city}. The target group is {tg}.\n'
                     '(i) State the objective in one line. (ii) Suggest the method of data collection and sample. (iii) Name two ways to present the data. (iv) Name one measure that could be used to analyse it.'),
            'answer': f'(i) e.g. "To study {topic} among {tg}" (ii) personal interviews with a questionnaire on a random sample of about 50–100 (iii) table, bar diagram/pie diagram '
                      '(iv) percentages, mean/median/mode, or correlation where two variables are measured',
            'key': '1 mark each.'}


def suit_pick(r):
    x, c = cp('suit', r, SUIT)
    return mcq(f'Which average is most suitable for: {x}?', c, [k for k in ['Arithmetic mean', 'Median', 'Mode', 'Weighted mean'] if k != c], f'{x}: {c}.', r)


# ====================================================================== FAMILIES
FAMILIES = {
    S + '05-st1': [M('C1', 'D1', AM_FACT[:2]), M('C1', 'D2', AM_FACT[2:]), G('C2', 'D2', 'numerical', am_shift, marks=1), G('C2', 'D3', 'numerical', am_corrected, marks=3, kinds=('q3',)),
                   AR('C2', 'D2', AM_AR), G('C3', 'D1', 'numerical', am_ind, marks=1), G('C3', 'D2', 'numerical', am_assumed, marks=3, kinds=('q3',)), G('C3', 'D2', 'numerical', am_discrete, marks=3),
                   G('C3', 'D3', 'numerical', am_step, marks=4, kinds=('q4',)), G('C3', 'D4', 'numerical', am_missing, marks=4, kinds=('q4',)),
                   G('C4', 'D3', 'numerical', am_weighted, marks=3, kinds=('q3',)), G('C4', 'D4', 'numerical', am_combined, marks=3), G('C4', 'D5', 'numerical', am_missing, marks=4)],
    S + '05-st2': [M('C1', 'D1', MED_FACT[:3]), M('C1', 'D2', MED_FACT[3:]), G('C2', 'D2', 'numerical', med_ind, marks=1), G('C2', 'D3', 'numerical', med_disc, marks=3, kinds=('q3',)),
                   AR('C2', 'D3', MED_AR), G('C3', 'D2', 'numerical', med_disc, marks=3), G('C3', 'D3', 'numerical', med_cont, marks=4, kinds=('q4',)), G('C3', 'D4', 'numerical', med_cont, marks=4),
                   G('C3', 'D1', 'numerical', med_ind, marks=1), G('C4', 'D3', 'numerical', quart, marks=3, kinds=('q3',)), G('C4', 'D4', 'numerical', quart, marks=3)],
    S + '05-st3': [M('C1', 'D1', MODE_FACT[:3]), M('C1', 'D2', MODE_FACT[2:]), G('C2', 'D2', 'numerical', mode_ind, marks=1), G('C2', 'D3', 'numerical', mode_disc, marks=1),
                   AR('C2', 'D2', MODE_AR), G('C3', 'D2', 'numerical', mode_cont, marks=4, kinds=('q4',)), G('C3', 'D3', 'numerical', mode_cont, marks=4), G('C3', 'D1', 'numerical', mode_disc, marks=1),
                   G('C4', 'D3', 'numerical', empirical, marks=3, kinds=('q3',)), G('C4', 'D4', 'numerical', empirical, marks=3)],
    S + '05-st4': [G('C4', 'D4', 'long', ct_long, marks=6), M('C1', 'D1', REL[:2]), M('C1', 'D2', REL[2:]), G('C2', 'D2', 'mcq', suit_pick),
                   G('C2', 'D3', 'mcq', rel_skew), AR('C2', 'D3', REL_AR), G('C3', 'D2', 'mcq', rel_skew), G('C3', 'D3', 'case', ct_case, marks=4, kinds=('case',)),
                   G('C3', 'D4', 'case', ct_case, marks=4, kinds=('case',)),
                   W('C4', 'D3', 'explain', [('Which average would you use for (i) the average size of readymade shirts to stock, (ii) average income of a village with a few landlords, (iii) average marks of a class for further calculations? Give reasons.',
                                              '(i) Mode: most demanded size (ii) median: not affected by extreme incomes (iii) mean: uses all values and is algebraically treatable.', '1 mark each (3 marks).'),
                                             ('Compare the mean, median and mode on any three points.', 'Mean uses all values and is affected by extremes; median is positional and unaffected by extremes; mode is the most frequent value and suits qualitative data; mean is algebraically treatable.',
                                              '1 mark each.')], marks=3, kinds=('q3',)),
                   W('C4', 'D4', 'long', [('Explain the relative position of mean, median and mode in symmetrical and skewed distributions. Which average is the most suitable in each of these cases: open-ended classes, qualitative data, extreme values?',
                                           'Symmetric: all equal; positive skew: mean > median > mode; negative skew: mean < median < mode; empirical relation Mode = 3 Median − 2 Mean; open-ended classes → median; qualitative → median/mode; extreme values → median.',
                                           '3 marks relative position; 3 marks suitability (6 marks).')], marks=6)],
    S + '06-st1': [M('C1', 'D1', CORR_FACT[:3]), M('C1', 'D2', CORR_FACT[3:]), G('C2', 'D2', 'mcq', scatter_desc),
                   G('C2', 'D3', 'mcq', lambda r: (lambda x, c: mcq(f'What type of correlation is expected between: {x}?', c,
                                                                    [k for k in ['Positive correlation', 'Negative correlation', 'No correlation', 'Perfect positive correlation'] if k != c][:3], f'{x}: {c}.', r))(*cp('corrx', r, CORR_EX))),
                   AR('C2', 'D2', CORR_AR), G('C3', 'D2', 'mcq', scatter_desc), G('C3', 'D3', 'mcq', lambda r: (lambda x, c: mcq(f'Identify the type of correlation: {x}.', c,
                                                                    [k for k in ['Positive correlation', 'Negative correlation', 'No correlation', 'Perfect negative correlation'] if k != c][:3], f'{x}: {c}.', r))(*cp('corrx2', r, CORR_EX))),
                   W('C4', 'D3', 'explain', [('"Correlation does not imply causation." Explain with an example.', 'Two variables may move together by chance or because of a third factor; e.g. ice-cream sales and drowning cases both rise in summer due to heat, not because one causes the other.',
                                              '1 mark meaning; 2 marks example.'),
                                             ('What is a scatter diagram? What can and cannot be learnt from it?', 'A graph of paired values as points; it shows the direction (positive/negative) and rough strength of relation, but not the exact degree of correlation.',
                                              '1 mark meaning; 2 marks uses and limitation.')], marks=3, kinds=('q3',)),
                   W('C4', 'D4', 'explain', [('Give one example each of positive, negative and zero correlation from economics and explain the reason for each.', 'Positive: income and consumption (higher income, more spending); negative: price and quantity demanded (law of demand); zero: shoe size and income (no relation).',
                                              '1 mark each with reason (3); 1 mark clarity (4 marks).')], marks=4, kinds=('q4',))],
    S + '06-st2': [M('C1', 'D1', CORR_FACT[:2]), M('C1', 'D2', CORR_FACT[4:]), G('C2', 'D2', 'numerical', corr_prop, marks=1), G('C2', 'D3', 'numerical', corr_prop, marks=1),
                   AR('C2', 'D3', CORR_AR[2:] + [('r is not affected by a change of origin.', 'Deviations from the mean remain unchanged when a constant is subtracted from every value.', 'a', 'R explains A.')]),
                   G('C3', 'D2', 'numerical', pearson, marks=4, kinds=('q4',)), G('C3', 'D3', 'numerical', pearson, marks=4), G('C3', 'D4', 'numerical', pearson_sum, marks=4, kinds=('q4',)),
                   G('C3', 'D1', 'numerical', corr_prop, marks=1), G('C4', 'D3', 'numerical', pearson_sum, marks=4), G('C4', 'D4', 'numerical', pearson, marks=6, kinds=('long',)),
                   W('C4', 'D5', 'long', [('State the properties of Karl Pearson\'s coefficient of correlation. Explain why r is independent of change of origin and scale.',
                                           'Properties: no unit, lies between −1 and +1, sign shows direction, r = 0 means no linear relation, independent of change of origin and scale; subtracting a constant does not change deviations; dividing both by positive constants cancels in the formula.',
                                           '4 marks properties; 2 marks explanation (6 marks).')], marks=6)],
    S + '06-st3': [M('C1', 'D1', SPEAR_FACT[:2]), M('C1', 'D2', SPEAR_FACT[2:]), G('C2', 'D2', 'numerical', tie_rank, marks=1), G('C2', 'D3', 'numerical', spearman_back, marks=3, kinds=('q3',)),
                   AR('C2', 'D2', SPEAR_AR), G('C3', 'D2', 'numerical', spearman, marks=3, kinds=('q3',)), G('C3', 'D3', 'numerical', spearman_vals, marks=4, kinds=('q4',)),
                   G('C3', 'D1', 'numerical', tie_rank, marks=1), G('C4', 'D3', 'numerical', spearman, marks=3), G('C4', 'D4', 'numerical', spearman_vals, marks=4)],
    S + '07-st1': [M('C1', 'D1', IDX_FACT[:2]), M('C1', 'D2', IDX_FACT[2:4]), M('C2', 'D2', IDX_FACT[4:]), AR('C2', 'D3', IDX_AR),
                   W('C2', 'D3', 'explain', [('What points should be kept in mind while constructing an index number?', 'Purpose, choice of base year (normal), choice of items (representative), choice of prices (retail/wholesale), choice of weights, choice of formula.',
                                              '½ mark each for any six (3 marks).'),
                                             ('Why should the base year be a normal year?', 'Abnormal years (war, drought) have unusual prices; comparing with them would exaggerate or understate change.', '3 marks.')], marks=3, kinds=('q3',)),
                   G('C3', 'D2', 'numerical', idx_simple, marks=3), G('C3', 'D3', 'numerical', idx_simple, marks=3, kinds=('q3',)), G('C3', 'D1', 'mcq', lambda r: mcq('An index number of 135 for 2024 with 2015 as base means prices have', 'risen by 35% since 2015', ['risen by 135%', 'fallen by 35%', 'risen by 13.5%'], '135 − 100 = 35% rise.', r) if r.random() < 0.5 else mcq('An index number of 92 means prices have', 'fallen by 8% compared with the base year', ['risen by 92%', 'risen by 8%', 'fallen by 92%'], '92 − 100 = −8%.', r)),
                   W('C4', 'D3', 'explain', [('Why are weights important in a price index for working-class families?', 'Items differ in importance in the budget (food more than entertainment); without weights a price rise in a minor item would affect the index as much as a major one.',
                                              '3 marks.')], marks=3, kinds=('q3',)),
                   W('C4', 'D4', 'long', [('Explain the problems faced in constructing an index number.', 'Purpose, base year, items, source of prices, weights, formula; with brief explanation of each.', '1 mark each (6 marks).')], marks=6)],
    S + '07-st2': [M('C1', 'D1', IDX_FACT[4:6]), M('C1', 'D2', [('In the simple aggregative method, the price index is', 'Σp₁/Σp₀ × 100', ['Σp₀/Σp₁ × 100', 'Σp₁q₀/Σp₀q₀ × 100', 'Σp₁q₁/Σp₀q₁ × 100'], 'Unweighted aggregate.'),
                                                                ('A weighted index of price relatives is calculated as', 'ΣRW/ΣW', ['ΣR/N', 'ΣW/ΣR', 'ΣR × ΣW'], 'R = price relative, W = weight.')]),
                   G('C2', 'D2', 'numerical', idx_relatives, marks=3), AR('C2', 'D3', IDX_AR[1:3]), G('C2', 'D3', 'numerical', idx_relatives, marks=3, kinds=('q3',)),
                   G('C3', 'D2', 'numerical', idx_simple, marks=3), G('C3', 'D3', 'numerical', idx_lasp, marks=4, kinds=('q4',)), G('C3', 'D4', 'numerical', idx_lasp, marks=4),
                   G('C3', 'D1', 'numerical', idx_relatives, marks=3), G('C4', 'D3', 'numerical', idx_weighted_rel, marks=4, kinds=('q4',)), G('C4', 'D4', 'numerical', idx_weighted_rel, marks=4),
                   G('C4', 'D5', 'numerical', idx_lasp, marks=6, kinds=('long',))],
    S + '07-st3': [M('C1', 'D1', INDICES[:3]), M('C1', 'D2', INDICES[3:6]), M('C2', 'D2', INDICES[6:] + INDICES[:1]), AR('C2', 'D3', IND_AR),
                   W('C2', 'D3', 'explain', [('Distinguish between CPI and WPI.', 'CPI: retail prices paid by consumers, includes services, measures cost of living. WPI: wholesale prices of goods, no services, measures general price level at the wholesale stage.',
                                              '1½ marks each.'),
                                             ('What does the SENSEX show? What does a rise in it indicate?', 'Index of share prices of 30 large companies on the BSE (base 1978–79 = 100); a rise shows rising share prices and investor optimism.', '3 marks.')],
                     marks=3, kinds=('q3',)),
                   M('C3', 'D2', [('To adjust dearness allowance of government employees, the most suitable index is the', 'Consumer Price Index', ['Wholesale Price Index', 'SENSEX', 'Index of Industrial Production'], 'CPI reflects cost of living.'),
                                  ('To study growth of factory output, the most suitable index is the', 'Index of Industrial Production', ['Consumer Price Index', 'SENSEX', 'Wholesale Price Index'], 'IIP measures output.'),
                                  ('To know how share prices of large companies changed, one looks at the', 'SENSEX or NIFTY', ['CPI', 'IIP', 'WPI'], 'Stock indices.')]),
                   G('C3', 'D3', 'numerical', idx_weighted_rel, marks=4), W('C4', 'D3', 'explain', [('Why does the CPI for an urban household differ from that of a rural household?', 'The basket and weights differ: urban households spend more on rent, transport and services; rural ones more on food; so price changes affect them differently.',
                                                                                                    '3 marks.')], marks=3, kinds=('q3',)),
                   G('C4', 'D4', 'numerical', idx_weighted_rel, marks=4, kinds=('q4',))],
    S + '07-st4': [M('C1', 'D1', USE_FACT[:1]), M('C1', 'D2', USE_FACT[1:]), G('C2', 'D2', 'numerical', purchasing, marks=1), AR('C2', 'D3', USE_AR),
                   G('C3', 'D2', 'numerical', inflation, marks=3, kinds=('q3',)), G('C3', 'D3', 'numerical', real_wage, marks=3), G('C3', 'D1', 'numerical', purchasing, marks=1),
                   G('C4', 'D3', 'numerical', needed_wage, marks=3, kinds=('q3',)), G('C4', 'D4', 'numerical', real_wage, marks=3)],
    S + '08-st1': [M('C1', 'D1', PROJ_FACT[:2]), M('C1', 'D2', PROJ_FACT[3:4] + PROJ_FACT[:1]), G('C2', 'D2', 'short', proj_order, marks=1), AR('C2', 'D3', PROJ_AR[:2]),
                   W('C2', 'D3', 'explain', [('Why is it important to identify the target group before collecting data for a project?', 'It decides whom to survey, the sample, the questions and the method; data from the wrong group would not answer the problem.', '3 marks.')], marks=3),
                   G('C3', 'D2', 'mcq', tool_choose), G('C3', 'D3', 'case', proj_case, marks=4, kinds=('case',)), G('C4', 'D3', 'case', proj_case, marks=4, kinds=('case',))],
    S + '08-st2': [M('C1', 'D1', PROJ_FACT[2:3] + PROJ_FACT[3:4]), M('C1', 'D2', PROJ_FACT[2:4]), G('C2', 'D2', 'mcq', tool_choose), AR('C2', 'D2', PROJ_AR[2:] + PROJ_AR[:1]),
                   G('C2', 'D3', 'mcq', tool_choose), G('C3', 'D2', 'mcq', tool_choose), G('C3', 'D3', 'numerical', lambda r: __import__('g11_economics_a').c13_pie(r), marks=1),
                   G('C4', 'D3', 'case', proj_case, marks=4), G('C4', 'D4', 'explain', lambda r: (lambda t: {'stem': f'For a project on "{t}", explain how you would organise and present the collected data.',
                                                                                                    'answer': 'Edit and code responses; classify; prepare frequency tables; choose suitable diagrams (bar/pie for categories, histogram for class intervals, line graph for time series); label tables with title, source.',
                                                                                                    'key': '2 marks organisation; 2 marks presentation (4 marks).'})(cp('projt', r, ['household savings', 'use of public libraries', 'mobile phone use by teenagers', 'electricity consumption', 'food wastage in hostels'])),
                                                             marks=4, kinds=('q4',))],
    S + '08-st3': [M('C1', 'D2', PROJ_FACT[4:] + PROJ_FACT[:1]), G('C2', 'D2', 'short', proj_order, marks=1), AR('C2', 'D2', PROJ_AR), G('C3', 'D2', 'mcq', tool_choose),
                   G('C4', 'D3', 'explain', lambda r: (lambda t: {'stem': f'A project finds that {t}. Write two lines of interpretation and one suggestion for the report.',
                                                                  'answer': 'Interpretation linked to the figures (what the pattern shows, which group differs); one practical suggestion following from it.',
                                                                  'key': '2 marks interpretation; 1 mark suggestion.'})(cp('projf', r, ['60% of households in a colony do not segregate waste', 'median daily screen time of students is 5 hours',
                                                                                                                                        'mean monthly savings of families is ₹3,200 but the median is ₹1,800', 'r between hours of study and marks is 0.72',
                                                                                                                                        '45% of shopkeepers accept digital payments'])), marks=3, kinds=('q3',))],
}
