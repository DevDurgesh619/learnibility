"""CBSE class 12 Geography: numeric question families (practical work and population data).

Used through g12_hum_engine's `extra` hook: EXTRA maps a subtopic id to a list of qbank Family objects.
All data sets are generated (labelled districts, villages, stations), so no real statistic is asserted.
"""
from __future__ import annotations

import math
from statistics import median

from qbank import F, num, num_distractors, mcq

S = 'cbse-g12-geography-ch'
PLACES = ['District A', 'District B', 'District C', 'District D', 'District E', 'District F', 'District G']
TOWNS = ['Town P', 'Town Q', 'Town R', 'Town S', 'Town T', 'Town U', 'Town V', 'Town W']


def _ans(v: dict, answer: str, wrong: list[str]) -> dict:
    v['answer'] = answer
    v['distractors'] = [w for w in wrong if w != answer][:3]
    return v


# ---------------------------------------------------------------- population (ch02, ch09)

def density_mcq(r):
    area = r.choice([1200, 1500, 2000, 2500, 3000, 4000, 5000, 6000, 8000])
    d = r.choice(range(80, 1200, 10))
    pop = area * d
    stem = (f'{r.choice(PLACES)} has a population of {pop:,} and an area of {area:,} sq km. '
            'What is its density of population?')
    wrong = num_distractors(d, area / pop * 1000 if pop else 1, d * 10, d / 10, d + 100)
    return mcq(stem, f'{d} persons per sq km', [f'{w} persons per sq km' for w in wrong], f'Density = population ÷ area = {pop:,} ÷ {area:,} = {d} persons per sq km.', r)


def density_compare(r):
    a, b = r.sample(PLACES, 2)
    ar_, br = r.choice([1000, 2000, 2500, 4000]), r.choice([500, 1500, 3000, 5000])
    da, db = r.choice(range(100, 900, 20)), r.choice(range(100, 900, 20))
    if da == db:
        db += 40
    pa, pb = ar_ * da, br * db
    hi = a if da > db else b
    return {'stem': f'{a} has a population of {pa:,} on {ar_:,} sq km; {b} has {pb:,} people on {br:,} sq km. '
                    'Calculate the density of population of each and state which is more densely populated.',
            'answer': f'{a}: {da} persons per sq km; {b}: {db} persons per sq km; {hi} is more densely populated.',
            'key': f'3 marks: 1 for each density (population ÷ area = {da} and {db} persons per sq km), 1 for the comparison ({hi}).',
            'marks': 3, 'minutes': 5}


def growth_rate(r):
    p1 = r.choice(range(200, 900, 10)) * 1000
    g = r.choice([-4, -2, 5, 8, 10, 12, 15, 18, 20, 22, 25])
    p2 = p1 + p1 * g // 100
    stem = (f'The population of {r.choice(PLACES)} was {p1:,} in 2001 and {p2:,} in 2011. '
            'What was its percentage growth rate over the decade?')
    wrong = num_distractors(g, -g, g * 10, (p2 - p1) / p2 * 100 if p2 else 1, g + 5, dp=1)
    return mcq(stem, f'{num(g, 1)}%', [f'{w}%' for w in wrong],
               f'Growth rate = (P2 − P1) ÷ P1 × 100 = ({p2:,} − {p1:,}) ÷ {p1:,} × 100 = {num(g, 1)}%.', r)


def growth_explain(r):
    p1 = r.choice(range(300, 800, 20)) * 1000
    births, deaths = r.choice(range(9, 30)) * 1000, r.choice(range(4, 12)) * 1000
    inm, outm = r.choice(range(1, 8)) * 1000, r.choice(range(1, 10)) * 1000
    p2 = p1 + births - deaths + inm - outm
    nat = births - deaths
    return {'stem': f'In one year, a region with a population of {p1:,} recorded {births:,} births, {deaths:,} deaths, '
                    f'{inm:,} in-migrants and {outm:,} out-migrants. Calculate (a) the natural increase and (b) the population at the end of the year. '
                    'Name the three components of population change.',
            'answer': f'(a) Natural increase = births − deaths = {nat:,}. (b) Population = {p1:,} + {nat:,} + {inm:,} − {outm:,} = {p2:,}. Components: births, deaths and migration.',
            'key': '3 marks: 1 for natural increase, 1 for the final population, 1 for naming births, deaths and migration.',
            'marks': 3, 'minutes': 5}


def sex_ratio(r):
    males = r.choice(range(400, 900, 5)) * 1000
    sr = r.choice(range(860, 1090, 3))
    females = males * sr // 1000
    stem = (f'{r.choice(PLACES)} has {males:,} males and {females:,} females. '
            'What is its sex ratio as defined in India?')
    sr_calc = round(females / males * 1000)
    wrong = num_distractors(sr_calc, round(males / females * 1000), round(females / (males + females) * 1000), sr_calc + 50)
    return mcq(stem, f'{sr_calc} females per 1000 males', [f'{w} females per 1000 males' for w in wrong],
               f'In India sex ratio = number of females per 1000 males = {females:,} ÷ {males:,} × 1000 ≈ {sr_calc}.', r)


def sex_ratio_explain(r):
    males = r.choice(range(300, 700, 5)) * 1000
    sr = r.choice(list(range(870, 960, 3)) + list(range(1010, 1080, 3)))
    females = males * sr // 1000
    sr_calc = round(females / males * 1000)
    view = 'favourable to females' if sr_calc > 1000 else 'unfavourable to females'
    return {'stem': f'A district has {males:,} males and {females:,} females. Calculate its sex ratio as used in India, state whether it is '
                    'favourable or unfavourable to females, and give one reason why sex ratio is unfavourable to females in many parts of India.',
            'answer': f'Sex ratio = {females:,} ÷ {males:,} × 1000 ≈ {sr_calc} females per 1000 males, which is {view}. '
                      'Reasons for low sex ratio: female foeticide, female infanticide, neglect of girls, domestic violence and low status of women.',
            'key': '3 marks: 1 for the calculation, 1 for the interpretation, 1 for a valid reason.', 'marks': 3, 'minutes': 5}


# ---------------------------------------------------------------- trade (ch08, ch16)

def balance_of_trade(r):
    ex = r.choice(range(150, 900, 5))
    im = r.choice(range(150, 900, 5))
    if ex == im:
        im += 25
    b = ex - im
    kind = 'favourable (positive)' if b > 0 else 'unfavourable (negative)'
    stem = (f'A country exported goods worth US$ {ex} billion and imported goods worth US$ {im} billion in a year. '
            'What is its balance of trade?')
    wrong = [f'US$ {abs(b)} billion, {"unfavourable" if b > 0 else "favourable"}', f'US$ {ex + im} billion, favourable',
             f'US$ {abs(b) + 50} billion, {"favourable" if b > 0 else "unfavourable"}']
    right = f'US$ {abs(b)} billion, {kind.split()[0]}'
    return mcq(stem, right, wrong, f'Balance of trade = exports − imports = {ex} − {im} = {b}; it is {kind}.', r)


def trade_explain(r):
    ex = r.choice(range(200, 600, 10))
    im = r.choice(range(300, 800, 10))
    if ex >= im:
        im = ex + r.choice([40, 80, 120])
    vol = ex + im
    b = ex - im
    return {'stem': f'A country\'s exports are worth ₹{ex} thousand crore and its imports ₹{im} thousand crore. Find (a) the volume of trade, '
                    '(b) the balance of trade, and (c) state one consequence of this kind of balance for the economy.',
            'answer': f'(a) Volume = {ex} + {im} = ₹{vol} thousand crore. (b) Balance = {ex} − {im} = −₹{abs(b)} thousand crore, a negative (unfavourable) balance. '
                      '(c) A negative balance can lead to depletion of financial reserves of the country.',
            'key': '3 marks: 1 for volume, 1 for balance with sign, 1 for the consequence.', 'marks': 3, 'minutes': 5}


# ---------------------------------------------------------------- frequency distribution (ch18)

def _raw(r, n, lo, hi):
    return [r.randint(lo, hi) for _ in range(n)]


def freq_count(r):
    w = r.choice([5, 10])
    lo = r.choice([0, 10, 20]) if w == 10 else r.choice([0, 5, 10])
    data = _raw(r, 15, lo, lo + w * 5 - 1)
    a = lo + w * r.randint(1, 3)
    f = sum(1 for x in data if a <= x < a + w)
    stem = (f'Marks scored by 15 students are: {", ".join(map(str, data))}. Using exclusive class intervals of width {w}, '
            f'what is the frequency of the class {a}–{a + w}?')
    f_incl = sum(1 for x in data if a <= x <= a + w)
    wrong = num_distractors(f, f_incl, f + 1, f - 1 if f > 0 else 2, f + 2)
    return mcq(stem, str(f), wrong, f'In the exclusive method the upper limit is not counted in the class; values from {a} up to but not including {a + w}: {f}.', r)


def class_mark(r):
    w = r.choice([5, 10, 20, 50])
    a = w * r.randint(1, 20)
    m = a + w / 2
    stem = f'What is the class mark (mid-point) of the class interval {a}–{a + w}?'
    wrong = num_distractors(m, w, a + w, a, m + w / 2)
    return mcq(stem, num(m), wrong, f'Class mark = (lower limit + upper limit) ÷ 2 = ({a} + {a + w}) ÷ 2 = {num(m)}.', r)


def cumulative(r):
    w = 10
    lo = r.choice([0, 10, 20])
    fs = [r.randint(2, 12) for _ in range(5)]
    rows = [f'{lo + i * w}–{lo + (i + 1) * w}: {f}' for i, f in enumerate(fs)]
    cf = list(__import__('itertools').accumulate(fs))
    k = r.randint(2, 4)
    return {'stem': 'The frequency distribution of daily rainfall (mm) at a station is: ' + '; '.join(rows) +
                    f'. Prepare the cumulative frequency (less than type) column and state how many days had rainfall less than {lo + (k + 1) * w} mm.',
            'answer': f'Cumulative frequencies: {", ".join(map(str, cf))}. Days with rainfall less than {lo + (k + 1) * w} mm = {cf[k]}.',
            'key': '3 marks: 2 for the cumulative frequency column, 1 for reading the required value.', 'marks': 3, 'minutes': 5,
            'distractors': num_distractors(cf[k], cf[k - 1], fs[k], cf[k] + fs[k])}


def tally_explain(r):
    lo, w = r.choice([(0, 10), (20, 10), (10, 5)])
    data = _raw(r, 20, lo, lo + w * 4 - 1)
    fs = [sum(1 for x in data if lo + i * w <= x < lo + (i + 1) * w) for i in range(4)]
    rows = '; '.join(f'{lo + i * w}–{lo + (i + 1) * w}: {f}' for i, f in enumerate(fs))
    return {'stem': f'Group the following 20 values into a frequency distribution using exclusive class intervals of width {w} starting at {lo}: '
                    f'{", ".join(map(str, data))}. Why are tally marks used while grouping?',
            'answer': f'Frequencies – {rows} (total 20). Tally marks (in groups of five) make counting quick and reduce errors while grouping raw data.',
            'key': '3 marks: 2 for the correct frequencies, 1 for the use of tally marks.', 'marks': 3, 'minutes': 6}


# ---------------------------------------------------------------- central tendency, dispersion (ch19)

def mean_mcq(r):
    n = r.choice([5, 6, 7, 8])
    xs = [r.randint(10, 60) for _ in range(n)]
    s = sum(xs)
    if s % n:
        xs[0] += n - s % n
    m = sum(xs) / n
    stem = f'The monthly rainfall (cm) at a station over {n} months was {", ".join(map(str, xs))}. What is the mean rainfall?'
    wrong = num_distractors(m, median(xs), sum(xs) / (n - 1), max(xs) - min(xs), m + 2)
    return mcq(stem, f'{num(m)} cm', [f'{w} cm' for w in wrong], f'Mean = Σx ÷ N = {sum(xs)} ÷ {n} = {num(m)} cm.', r)


def median_mcq(r):
    n = r.choice([5, 7, 9, 6, 8])
    xs = r.sample(range(10, 90), n)
    md = median(xs)
    srt = sorted(xs)
    stem = f'Find the median of the following temperatures (°C): {", ".join(map(str, xs))}.'
    wrong = num_distractors(md, xs[n // 2], sum(xs) / n, srt[n // 2 - 1] if n % 2 else srt[n // 2 + 1], dp=1)
    return mcq(stem, num(md, 1), wrong, f'Arrange in order: {", ".join(map(str, srt))}; the middle value' +
               (' is ' if n % 2 else 's average to ') + f'{num(md, 1)}.', r)


def mode_mcq(r):
    base = r.sample(range(20, 60), 5)
    mo = base[0]
    xs = base + [mo, mo] + [base[1]]
    r.shuffle(xs)
    stem = f'What is the mode of the following daily attendance figures: {", ".join(map(str, xs))}?'
    wrong = num_distractors(mo, base[1], median(xs), max(xs))
    return mcq(stem, str(mo), wrong, f'The mode is the value that occurs most often: {mo} occurs 3 times.', r)


def grouped_mean(r):
    w = 10
    lo = r.choice([0, 10, 20, 30])
    fs = [r.randint(2, 10) for _ in range(4)]
    ms = [lo + w * i + w / 2 for i in range(4)]
    fx = [f * m for f, m in zip(fs, ms)]
    mean = sum(fx) / sum(fs)
    rows = '; '.join(f'{lo + i * w}–{lo + (i + 1) * w}: {f}' for i, f in enumerate(fs))
    return {'stem': f'Calculate the mean of the following grouped data (class: frequency) using the direct method: {rows}.',
            'answer': f'Class marks {", ".join(num(m) for m in ms)}; Σfx = {num(sum(fx))}; N = {sum(fs)}; mean = Σfx ÷ N = {num(mean)}.',
            'key': '3 marks: 1 for class marks, 1 for Σfx, 1 for the mean.', 'marks': 3, 'minutes': 6,
            'distractors': num_distractors(round(mean, 2), sum(ms) / 4, sum(fx) / 4, mean + w / 2)}


def range_mcq(r):
    xs = r.sample(range(5, 99), 8)
    rg = max(xs) - min(xs)
    stem = f'What is the range of the following values: {", ".join(map(str, xs))}?'
    wrong = num_distractors(rg, max(xs) + min(xs), max(xs), (max(xs) - min(xs)) / 2)
    return mcq(stem, str(rg), wrong, f'Range = largest − smallest = {max(xs)} − {min(xs)} = {rg}.', r)


def sd_item(r):
    while True:
        n = r.choice([5, 6])
        xs = [r.randint(2, 20) for _ in range(n)]
        if sum(xs) % n == 0 and len(set(xs)) > 2:
            break
    m = sum(xs) // n
    dev = [x - m for x in xs]
    var = sum(d * d for d in dev) / n
    sd = math.sqrt(var)
    return {'stem': f'Calculate the standard deviation of the following values: {", ".join(map(str, xs))}.',
            'answer': f'Mean = {m}; deviations {", ".join(num(d) for d in dev)}; Σd² = {sum(d * d for d in dev)}; '
                      f'σ = √(Σd² ÷ N) = √({num(var)}) ≈ {sd:.2f}.',
            'key': '3 marks: 1 for the mean, 1 for Σd², 1 for σ.', 'marks': 3, 'minutes': 6,
            'distractors': num_distractors(round(sd, 2), round(var, 2), round(math.sqrt(sum(d * d for d in dev) / (n - 1)), 2), round(sd + 1, 2))}


def mean_dev(r):
    while True:
        xs = [r.randint(5, 40) for _ in range(5)]
        if sum(xs) % 5 == 0:
            break
    m = sum(xs) // 5
    md = sum(abs(x - m) for x in xs) / 5
    stem = f'What is the mean deviation from the mean of: {", ".join(map(str, xs))}?'
    wrong = num_distractors(md, sum(abs(x - m) for x in xs), m, md + 1)
    return mcq(stem, num(md), wrong, f'Mean = {m}; Σ|d| = {sum(abs(x - m) for x in xs)}; mean deviation = Σ|d| ÷ N = {num(md)}.', r)


# ---------------------------------------------------------------- rank correlation (ch19)

def _ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: -xs[i])
    rk = [0] * len(xs)
    for pos, i in enumerate(order):
        rk[i] = pos + 1
    return rk


def _spearman_data(r, n):
    xs = r.sample(range(20, 99), n)
    mode = r.choice(['pos', 'neg', 'mix'])
    ys = []
    for x in xs:
        if mode == 'pos':
            ys.append(x + r.randint(-15, 15))
        elif mode == 'neg':
            ys.append(120 - x + r.randint(-15, 15))
        else:
            ys.append(r.randint(20, 99))
    if len(set(ys)) < n:
        raise ValueError('tie')
    rx, ry = _ranks(xs), _ranks(ys)
    d2 = sum((a - b) ** 2 for a, b in zip(rx, ry))
    rho = 1 - 6 * d2 / (n * (n * n - 1))
    return xs, ys, rx, ry, d2, rho


def _strength(rho):
    a = abs(rho)
    sign = 'positive' if rho > 0 else 'negative'
    if a == 1:
        return f'perfect {sign}'
    if a >= .75:
        return f'high {sign}'
    if a >= .4:
        return f'moderate {sign}'
    return f'low {sign}' if a > 0 else 'no'


def spearman_long(r):
    n = r.choice([5, 6, 7])
    xs, ys, rx, ry, d2, rho = _spearman_data(r, n)
    towns = TOWNS[:n]
    rows = '; '.join(f'{t}: {x}, {y}' for t, x, y in zip(towns, xs, ys))
    return {'stem': f'The literacy rate (%) and the percentage of workers in non-agricultural activities for {n} towns are given '
                    f'(town: literacy, non-agricultural workers): {rows}. Calculate Spearman\'s rank correlation coefficient and interpret the result.',
            'answer': f'Ranks (highest = 1) – X: {", ".join(map(str, rx))}; Y: {", ".join(map(str, ry))}. Σd² = {d2}. '
                      f'ρ = 1 − 6Σd² ÷ (N³ − N) = 1 − {6 * d2} ÷ {n ** 3 - n} = {num(round(rho, 2))}, a {_strength(rho)} correlation.',
            'key': '5 marks: 1 for ranks, 1 for d and d², 1 for the formula, 1 for ρ, 1 for interpretation.', 'marks': 5, 'minutes': 9}


def spearman_mcq(r):
    n = r.choice([5, 6, 7, 8, 10])
    d2 = r.randint(2, n * (n * n - 1) // 6 * 2 - 2)
    rho = 1 - 6 * d2 / (n * (n * n - 1))
    stem = f'For {n} pairs of ranks, Σd² = {d2}. What is Spearman\'s rank correlation coefficient?'
    wrong = num_distractors(round(rho, 2), round(6 * d2 / (n * (n * n - 1)), 2), round(1 - 6 * d2 / (n * n - 1), 2), round(-rho, 2) if rho else .5)
    return mcq(stem, num(round(rho, 2)), wrong, f'ρ = 1 − 6Σd² ÷ (N³ − N) = 1 − {6 * d2} ÷ {n ** 3 - n} = {num(round(rho, 2))}.', r)


def spearman_interpret(r):
    rho = r.choice([-1, -.92, -.81, -.55, -.12, .08, .35, .48, .66, .79, .9, 1])
    stem = f'A rank correlation coefficient of {num(rho)} indicates:'
    right = f'{_strength(rho)} correlation'
    allv = ['perfect positive correlation', 'perfect negative correlation', 'high positive correlation', 'high negative correlation',
            'moderate positive correlation', 'moderate negative correlation', 'low positive correlation', 'low negative correlation']
    wrong = r.sample([x for x in allv if x != right], 3)
    return mcq(stem, right, wrong, f'ρ = {num(rho)}: sign gives the direction; magnitude near 1 is strong, near 0 is weak – {right}.', r)


# ---------------------------------------------------------------- graphs (ch20)

def pie_angle(r):
    total = r.choice([200, 360, 400, 500, 600, 720, 800, 1000, 1200])
    share = r.choice([.05, .1, .125, .15, .2, .25, .3, .35, .4, .45])
    v = round(total * share)
    ang = v / total * 360
    item = r.choice(['wheat', 'rice', 'pulses', 'cotton', 'oilseeds', 'sugarcane'])
    stem = (f'In a pie diagram of land under crops totalling {total} hectares, {item} occupies {v} hectares. '
            'What angle should its segment have?')
    wrong = num_distractors(ang, v / total * 100, 360 - ang, ang / 2, ang + 18, dp=1)
    return mcq(stem, f'{num(ang, 1)}°', [f'{w}°' for w in wrong], f'Angle = value ÷ total × 360 = {v} ÷ {total} × 360 = {num(ang, 1)}°.', r)


def pie_explain(r):
    cats = r.sample(['agriculture', 'industry', 'services', 'mining', 'construction'], 3)
    shares = r.choice([(50, 30, 20), (45, 25, 30), (40, 35, 25), (60, 15, 25), (55, 20, 25)])
    angs = [s * 3.6 for s in shares]
    rows = '; '.join(f'{c}: {s}%' for c, s in zip(cats, shares))
    return {'stem': f'The share of workers in a district is {rows}. Calculate the angles for a pie diagram and state one rule for drawing it.',
            'answer': f'Angles = percentage × 3.6: {"; ".join(f"{c} {num(a)}°" for c, a in zip(cats, angs))} (total 360°). '
                      'Rule: draw segments in descending order of size, starting from the vertical radius, and give a title and legend.',
            'key': '3 marks: 2 for the angles, 1 for a correct rule.', 'marks': 3, 'minutes': 5}


def scale_item(r):
    cm = r.choice([1, 2, 5])
    unit = r.choice([10, 20, 25, 50, 100])
    v = r.choice(range(1, 10)) * unit
    bar = v / unit * cm
    stem = f'A bar diagram uses a scale of {cm} cm = {unit} thousand tonnes. How long should the bar for {v} thousand tonnes be?'
    wrong = num_distractors(bar, v / unit, v / cm, bar * 2, dp=1)
    return mcq(stem, f'{num(bar, 1)} cm', [f'{w} cm' for w in wrong], f'Length = {v} ÷ {unit} × {cm} = {num(bar, 1)} cm.', r)


def dot_value(r):
    per = r.choice([1000, 2000, 5000, 10000, 50000])
    pop = per * r.randint(5, 60)
    dots = pop // per
    stem = f'In a dot map where one dot represents {per:,} persons, how many dots should be placed for a district with {pop:,} people?'
    wrong = num_distractors(dots, dots * 10, dots / 10 if dots >= 10 else dots + 5, dots + 1)
    return mcq(stem, str(dots), wrong, f'Number of dots = {pop:,} ÷ {per:,} = {dots}.', r)


def choropleth(r):
    vals = {d: r.randint(150, 950) for d in PLACES[:6]}
    lo, hi = min(vals.values()), max(vals.values())
    step = math.ceil((hi - lo + 1) / 3)
    edges = [lo, lo + step, lo + 2 * step, lo + 3 * step]
    cls = {d: min(2, (v - lo) // step) for d, v in vals.items()}
    shade = ['low (lightest shade)', 'medium', 'high (darkest shade)']
    rows = '; '.join(f'{d}: {v}' for d, v in vals.items())
    groups = '; '.join(f'{edges[i]}–{edges[i + 1] - 1} {shade[i]}: ' + ', '.join(d for d, c in cls.items() if c == i) for i in range(3))
    return {'stem': f'Population density (persons per sq km) of six districts is: {rows}. Group the districts into three equal classes '
                    'for a choropleth map and state how each class will be shown.',
            'answer': f'Range {lo}–{hi}; class interval ≈ {step}. Classes – {groups}. Shades increase in darkness with value.',
            'key': '3 marks: 1 for class intervals, 1 for allocating districts, 1 for graded shading.', 'marks': 3, 'minutes': 6}


# ---------------------------------------------------------------- GIS (ch21)

def raster_cells(r):
    res = r.choice([10, 20, 30, 50, 100])
    w = r.choice([1, 2, 3, 5, 6]) * 1000
    h = r.choice([1, 2, 3, 4]) * 1000
    cells = (w // res) * (h // res)
    stem = f'An area {w // 1000} km × {h // 1000} km is stored as a raster with a cell size of {res} m × {res} m. How many cells does it contain?'
    wrong = [x for x in dict.fromkeys([cells // 10, (w + h) // res, cells * 2, w // res, cells + w // res]) if x != cells]
    return mcq(stem, f'{cells:,}', [f'{x:,}' for x in wrong],
               f'Cells = ({w} ÷ {res}) × ({h} ÷ {res}) = {w // res} × {h // res} = {cells:,}.', r)


def buffer_area(r):
    d = r.choice([100, 200, 300, 500, 1000])
    ha = 3.14 * d * d / 10000
    stem = f'In a GIS, a circular buffer of radius {d} m is drawn around a well. Taking π = 3.14, what is the area of the buffer zone?'
    wrong = num_distractors(ha, 2 * 3.14 * d / 100, d * d / 10000, ha * 2, ha / 2, dp=2)
    return mcq(stem, f'{num(ha)} hectares', [f'{w} hectares' for w in wrong],
               f'Area = πr² = 3.14 × {d}² = {num(3.14 * d * d)} m² = {num(ha)} hectares (1 hectare = 10,000 m²).', r)


# ---------------------------------------------------------------- registry

def _m(C, D, g):
    return F(C, D, 'mcq', g)


def _n(C, D, g, marks=3, minutes=5, typ='numerical'):
    return F(C, D, typ, g, marks=marks, minutes=minutes)


EXTRA = {
    S + '02-st1': [_m('C2', 'D2', density_mcq), _n('C3', 'D3', density_compare)],
    S + '02-st3': [_m('C2', 'D2', growth_rate), _n('C3', 'D3', growth_explain)],
    S + '08-st2': [_m('C2', 'D2', balance_of_trade), _n('C3', 'D3', trade_explain)],
    S + '09-st1': [_m('C2', 'D2', density_mcq)],
    S + '09-st2': [_m('C2', 'D3', growth_rate)],
    S + '09-st3': [_m('C2', 'D2', sex_ratio), _n('C4', 'D3', sex_ratio_explain)],
    S + '18-st3': [_m('C2', 'D2', freq_count), _m('C1', 'D2', class_mark), _n('C3', 'D3', cumulative), _n('C3', 'D4', tally_explain, minutes=6)],
    S + '19-st1': [_m('C2', 'D2', mean_mcq), _m('C2', 'D2', median_mcq), _m('C1', 'D2', mode_mcq), _n('C3', 'D3', grouped_mean, minutes=6)],
    S + '19-st2': [_m('C2', 'D2', range_mcq), _m('C3', 'D3', mean_dev), _n('C3', 'D4', sd_item, minutes=6)],
    S + '19-st3': [_m('C3', 'D3', spearman_mcq), _m('C3', 'D2', spearman_interpret),
                   F('C4', 'D4', 'long', spearman_long, marks=5, minutes=9, gap='G5')],
    S + '20-st2': [_m('C2', 'D2', pie_angle), _m('C2', 'D2', scale_item), _n('C3', 'D3', pie_explain)],
    S + '20-st3': [_m('C2', 'D2', dot_value), _n('C4', 'D4', choropleth, minutes=6)],
    S + '21-st1': [_m('C2', 'D3', raster_cells)],
    S + '21-st3': [_m('C3', 'D3', buffer_area)],
}
