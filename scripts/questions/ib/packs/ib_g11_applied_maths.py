"""IB DP Mathematics: Applications and Interpretation SL/HL (2019 guide), DP year 1 – ib-g11-applied-maths.

Topic 1 Number and algebra (SL 1.1-1.8, AHL 1.9-1.15), topic 2 Functions (SL 2.1-2.6, AHL 2.7-2.10)
and topic 4 Statistics and probability (SL 4.1-4.10, AHL 4.12-4.14, 4.17).

Every numerical item is parametric and computes its own answer (numpy / math, plus small numerical
routines for the normal, binomial and Poisson distributions, since a GDC is assumed on all papers).
Answers follow IB conventions: exact or correct to 3 significant figures; money to 2 decimal places;
angles in degrees to 1 d.p. Marking keys use markscheme notation: M1 method, A1 accuracy, R1 reasoning,
(M1)/(A1) implied marks, AG answer given, FT follow-through.

Mock = HL-style paper set (calculator throughout): Paper 1 short-response questions, Paper 2
extended-response questions and a Paper 3 extended problem; every mock carries the same marks.
"""
from __future__ import annotations

import math
import re

import numpy as np

from _common import F, Registry, T, mcq, name, two_names, sup, CITIES  # noqa: F401
from engine import Slot, DEFAULT_MARKS

CONFIG = {'minutesPerMark': 1.1, 'mcqMinutes': 1.5}

# HL: Paper 1 (2 h, 110 marks, short response), Paper 2 (2 h, 110 marks, extended response),
# Paper 3 (1 h, 55 marks, 2 extended problems). 23 items: 13 × 7 + 8 × 13 + 2 × 20 = 235 marks.
MOCK = [
    dict(section='Paper 1 – short-response questions (calculator)', count=13, c=['C3', 'C2', 'C3', 'C4'], d=[2, 3, 3, 4], type='multi_step', marks=7, style='p1'),
    dict(section='Paper 2 – extended-response questions (calculator)', count=8, c=['C3', 'C4'], d=[3, 4, 4], type='multi_step', marks=13, style='p2'),
    dict(section='Paper 3 – extended problem (HL)', count=2, c=['C4'], d=[4, 5], type='long', marks=20, style='p3'),
]

R = Registry()


def init(subject_id):
    pass


# =============================================================================================
# Helpers
# =============================================================================================
MINUS = '−'


def sf(x, n=3):
    """x correct to n significant figures, as text (IB style, unicode minus)."""
    x = float(x)
    if x == 0 or not math.isfinite(x):
        return '0'
    neg = x < 0
    x = abs(x)
    mag = math.floor(math.log10(x))
    r = round(x, n - 1 - mag)
    if r > 0 and math.floor(math.log10(r)) > mag:
        mag += 1
        r = round(x, n - 1 - mag)
    s = str(int(round(r))) if mag >= n - 1 else f'{r:.{n - 1 - mag}f}'
    return (MINUS if neg else '') + s


def sfv(x, n=3):
    """Numerical value of x rounded to n s.f. (for chaining displayed values)."""
    if x == 0:
        return 0.0
    return float(f'{x:.{n - 1}e}')


def sci(x, n=3):
    """a × 10^k with 1 ≤ a < 10, a to n s.f."""
    if x == 0:
        return '0'
    neg = x < 0
    x = abs(x)
    k = math.floor(math.log10(x))
    a = round(x / 10 ** k, n - 1)
    if a >= 10:
        a /= 10
        k += 1
    return (MINUS if neg else '') + f'{a:.{n - 1}f} × 10{sup(k)}'


def money(x, dp=2):
    s = f'{abs(x):,.{dp}f}'.replace(',', ' ')
    return (MINUS if x < 0 else '') + s


def m(s):
    """Replace ASCII minus signs in a number/expression string with the unicode minus."""
    return re.sub(r'(?<![\w)])-', MINUS, str(s)).replace('+ -', f'{MINUS} ').replace('+ ' + MINUS, MINUS + ' ')


def sgn(v, first=False, fmtf=None):
    """Format a signed coefficient: '+ 3' / '− 3' (or '3' / '−3' at the start)."""
    f = fmtf or (lambda z: sf(z) if isinstance(z, float) and not float(z).is_integer() else str(int(z)))
    if first:
        return (MINUS if v < 0 else '') + f(abs(v))
    return (f'{MINUS} ' if v < 0 else '+ ') + f(abs(v))


def poly(coefs, var='x'):
    """[a_n, ..., a_0] -> 'a_n xⁿ + ... + a_0' with integer coefficients."""
    n = len(coefs) - 1
    out = []
    for i, c in enumerate(coefs):
        p = n - i
        if c == 0:
            continue
        mag = abs(c)
        core = ('' if mag == 1 and p > 0 else (_num(mag) if isinstance(mag, float) and not float(mag).is_integer() else str(int(mag))))
        core += (var + (sup(p) if p > 1 else '')) if p > 0 else ''
        if not out:
            out.append((MINUS if c < 0 else '') + core)
        else:
            out.append((f'{MINUS} ' if c < 0 else '+ ') + core)
    return ' '.join(out) if out else '0'


def ret(stem, answer, key, marks=None, type='short', gap=None, **kw):
    d = dict(stem=stem, answer=answer, markingKey=key, type=type)
    if marks:
        d['marks'] = marks
    if gap:
        d['gap'] = gap
    d.update(kw)
    return d


def nmcq(rng, stem, v, wrongs, key, fmtf=sf):
    """Numerical MCQ: v correct, wrongs a list of numbers; formatted with fmtf."""
    c = fmtf(v)
    ws = []
    for w in wrongs:
        s = fmtf(w)
        if s != c and s not in ws:
            ws.append(s)
    if len(ws) < 3:
        return None
    return mcq(rng, stem, c, ws[:3], key)


def pick(rng, seq):
    return seq[rng.randrange(len(seq))]


CUR = [('USD', '$'), ('EUR', '€'), ('GBP', '£'), ('CHF', 'CHF'), ('SGD', 'S$'), ('CAD', 'C$'), ('AUD', 'A$'),
       ('JPY', '¥'), ('INR', '₹'), ('ZAR', 'R'), ('NZD', 'NZ$'), ('MXN', 'MX$')]


def cur(rng):
    return curm(rng)


def curm(rng):
    """A currency whose unit suits salaries/prices in the thousands."""
    return pick(rng, ['USD', 'EUR', 'GBP', 'CHF', 'CAD', 'AUD', 'SGD', 'NZD'])


CUR_CITIES = {'USD': ['Chicago', 'Boston', 'Denver'], 'EUR': ['Vienna', 'Lisbon', 'Dublin'], 'GBP': ['Manchester', 'Edinburgh', 'Bristol'],
              'CHF': ['Geneva', 'Zurich', 'Basel'], 'CAD': ['Toronto', 'Vancouver', 'Calgary'], 'AUD': ['Melbourne', 'Sydney', 'Perth'],
              'SGD': ['Singapore'], 'NZD': ['Auckland', 'Wellington', 'Christchurch']}


def city_for(rng, cc):
    """A city whose local currency is cc (falls back to the general list)."""
    return pick(rng, CUR_CITIES.get(cc, CITIES))


# ---- numerical routines (stand-in for the GDC) ----------------------------------------------
def ncdf(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def ninv(p):
    lo, hi = -10.0, 10.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if ncdf(mid) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def binpmf(n, p, k):
    return math.comb(n, k) * p ** k * (1 - p) ** (n - k)


def bincdf(n, p, k):
    return sum(binpmf(n, p, i) for i in range(0, k + 1))


def poipmf(lam, k):
    return math.exp(-lam) * lam ** k / math.factorial(k)


def poicdf(lam, k):
    return sum(poipmf(lam, i) for i in range(0, k + 1))


def bisect(f, lo, hi, it=200):
    flo = f(lo)
    for _ in range(it):
        mid = (lo + hi) / 2
        fm = f(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


def pearson(xs, ys):
    return float(np.corrcoef(xs, ys)[0, 1])


def ranks(v):
    """Average ranks (1 = largest), as IB GDC/Spearman tables usually rank highest = 1."""
    order = sorted(range(len(v)), key=lambda i: -v[i])
    r = [0.0] * len(v)
    i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and v[order[j + 1]] == v[order[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            r[order[k]] = avg
        i = j + 1
    return r


def spearman(xs, ys):
    return pearson(ranks(xs), ranks(ys))


def strength(r):
    a = abs(r)
    s = 'strong' if a >= 0.75 else 'moderate' if a >= 0.5 else 'weak' if a >= 0.25 else 'very weak / no'
    d = 'positive' if r > 0 else 'negative'
    return f'{s} {d}' if a >= 0.25 else 'very weak or no linear'


# ---- mocks: multi-part questions assembled from a subtopic's own templates --------------------
def _cs(t):
    return t.c if isinstance(t.c, tuple) else (t.c,)


FACT_NAMES = {'define', 'term_mcq', 'term_rev', 'fact_mcq', 'fact_short', 'evaluate', 'contrast'}


def _part(rng, tpls, c, d, used, slot):
    pool = [t for t in tpls if c in _cs(t) and t.style is None and (t.name, c) not in used and t.name not in FACT_NAMES
            and t.d[0] <= d <= t.d[1]]
    rng.shuffle(pool)
    # prefer templates not used at all yet, then other concept groups of a used template
    pool.sort(key=lambda t: any(n == t.name for n, _ in used))
    for t in pool[:8]:
        try:
            out = t.fn(rng, Slot(slot.subtopic, slot.chapter, c, d, set='part'))
        except IndexError:
            out = None
        if out and out.get('type') != 'mcq' and not out.get('options'):
            used.add((t.name, c))
            return out
    return None


ROMAN = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii']


def _sub(text):
    """Turn a part's own (a), (b) … into (i), (ii) … so it can sit inside a lettered part."""
    return re.sub(r'(?<![\w])\(([a-g])\)(?= )', lambda mm: '(' + ROMAN[ord(mm.group(1)) - 97] + ')', text)


def _fix_marks(key, m_):
    return re.sub(r'\(\d+ marks?:', f'({m_} marks:', key)


def _topic(st):
    n = re.sub(r'^(SL|AHL)\s+[\d.\-]+\s+', '', st['name'])
    return n[0].lower() + n[1:]


def _alloc(weights, total):
    w = [max(1, x) for x in weights]
    raw = [total * x / sum(w) for x in w]
    out = [max(1, int(r)) for r in raw]
    while sum(out) < total:
        i = max(range(len(w)), key=lambda k: raw[k] - out[k])
        out[i] += 1
    while sum(out) > total:
        i = max(range(len(w)), key=lambda k: out[k] - raw[k] if out[k] > 1 else -99)
        out[i] -= 1
    return out


def composite(st, tpls, spec, style, total):
    def fn(rng, slot):
        if slot.set != 'mock':
            return None
        used = set()
        parts = []
        for c, d in spec:
            p = _part(rng, tpls, c, d, used, slot)
            if p is None:
                return None
            parts.append(p)
        stems = [p['stem'] for p in parts]
        if len(set(stems)) < len(stems) or len({str(p['answer']) for p in parts}) < len(parts):
            return None
        nat = [p.get('marks') or DEFAULT_MARKS.get(c, {}).get(d, 3) for p, (c, d) in zip(parts, spec)]
        marks = _alloc(nat, slot.marks or total)
        if style == 'p3':
            intro = (f'Paper 3 extended problem: {_topic(st)}. Answer every part; you are expected to use your GDC '
                     f'and to show the mathematics that supports each conclusion.')
        else:
            intro = f'This question is about {_topic(st)}. Answers should be exact or correct to 3 significant figures.'
        L = 'abcdefg'
        stem = intro + '\n\n' + '\n\n'.join(f'({L[i]}) {_sub(p["stem"])} [{m_}]' for i, (p, m_) in enumerate(zip(parts, marks)))
        ans = ' '.join(f'({L[i]}) {_sub(p["answer"])}' for i, p in enumerate(parts))
        key = ' '.join(f'({L[i]}) [{m_} marks] {_sub(_fix_marks(p["markingKey"], m_))}' for i, (p, m_) in enumerate(zip(parts, marks)))
        return dict(stem=stem, answer=ans, markingKey=key, type='long' if style == 'p3' else 'multi_step',
                    marks=sum(marks), gap='G5')
    return fn


P1_SPECS = [[('C1', 2), ('C3', 3)], [('C3', 2), ('C2', 3)], [('C2', 2), ('C3', 3)], [('C3', 3), ('C4', 3)]]
P2_SPECS = [[('C1', 2), ('C3', 3), ('C4', 4)], [('C2', 2), ('C3', 3), ('C4', 4)], [('C3', 2), ('C2', 3), ('C4', 4)]]
P3_SPECS = [[('C1', 2), ('C3', 3), ('C2', 3), ('C4', 5)], [('C2', 2), ('C3', 3), ('C3', 4), ('C4', 5)]]

_CACHE: dict = {}


def templates(st):
    if st['id'] in _CACHE:
        return _CACHE[st['id']]
    base = R.build(st)
    out = list(base)
    for i, spec in enumerate(P1_SPECS):
        out.append(T(('C2', 'C3', 'C4'), (2, 5), composite(st, base, spec, 'p1', 7), 'multi_step', 'p1', f'p1_{i}'))
    for i, spec in enumerate(P2_SPECS):
        out.append(T(('C3', 'C4'), (3, 5), composite(st, base, spec, 'p2', 13), 'multi_step', 'p2', f'p2_{i}'))
    for i, spec in enumerate(P3_SPECS):
        out.append(T('C4', (4, 5), composite(st, base, spec, 'p3', 20), 'long', 'p3', f'p3_{i}'))
    _CACHE[st['id']] = out
    return out


ALL = ('C1', 'C2', 'C3', 'C4')

from decimal import Decimal, ROUND_HALF_UP


def dround(x, dp):
    """Round half-up (as taught) to dp decimal places; x may be str/float."""
    q = Decimal(1).scaleb(-dp) if dp > 0 else Decimal(1).scaleb(-dp)
    v = Decimal(str(x)).quantize(q, rounding=ROUND_HALF_UP) if dp >= 0 else \
        (Decimal(str(x)) / Decimal(10) ** (-dp)).quantize(Decimal(1), rounding=ROUND_HALF_UP) * Decimal(10) ** (-dp)
    return v


def dsf(x, n):
    d = Decimal(str(x))
    if d == 0:
        return '0'
    mag = d.copy_abs().adjusted()
    dp = n - 1 - mag
    v = dround(d, dp)
    if v.copy_abs().adjusted() > mag:  # carried into a new digit
        dp -= 1
        v = dround(d, dp)
    s = format(v, 'f') if dp > 0 else str(int(v))
    return s


def ordinary(mant, k):
    """Exact decimal string of mant × 10^k (mant given to ≤ 3 s.f.)."""
    v = Decimal(str(mant)).scaleb(k)
    s = format(v.normalize(), 'f')
    if '.' not in s and len(s) > 4:
        s = f'{int(s):,}'.replace(',', ' ')
    return s


# =============================================================================================
# ch01 Approximation and scientific notation
# =============================================================================================
R.facts('ch01-st1', F(
    terms=[('scientific notation (standard form)', 'writing a number as a × 10ᵏ where 1 ≤ a < 10 and k is an integer'),
           ('order of magnitude', 'the power of ten k when a number is written in the form a × 10ᵏ, used to compare sizes roughly'),
           ('mantissa (coefficient)', 'the number a, with 1 ≤ a < 10, that multiplies the power of ten in a × 10ᵏ')],
    facts=[('Which of the following is written in the form a × 10ᵏ, 1 ≤ a < 10, k ∈ ℤ?', '7.02 × 10⁻³', ['70.2 × 10⁻⁴', '0.702 × 10⁻²', '7.02 × 10^(1/2)'], 'Only 7.02 × 10⁻³ has 1 ≤ a < 10 and an integer power.'),
           ('A GDC displays 4.8E−6. What number does this represent?', '4.8 × 10⁻⁶', ['4.8⁻⁶', '4.8 × e⁻⁶', '−4.8 × 10⁶'], 'E stands for "× 10 to the power".'),
           ('Multiplying two numbers in scientific notation, what happens to the powers of ten?', 'They are added', ['They are multiplied', 'They are subtracted', 'They stay the same'], '10ᵐ × 10ⁿ = 10ᵐ⁺ⁿ; the coefficients are multiplied.')],
    why=[('Explain why scientific notation is useful when recording the masses of planets and of atoms.', 'The numbers are extremely large or small; a × 10ᵏ shows the size (order of magnitude) at a glance, avoids long strings of zeros and makes the number of significant figures clear.'),
         ('Explain why 25 × 10⁴ is not in scientific notation, and write it correctly.', 'The coefficient must satisfy 1 ≤ a < 10; 25 is too large. 25 × 10⁴ = 2.5 × 10 × 10⁴ = 2.5 × 10⁵.'),
         ('Explain why a number less than 1 has a negative power of ten in scientific notation.', 'To move from a (between 1 and 10) to a number less than 1 the decimal point moves left, i.e. a is divided by a power of ten: ÷ 10ⁿ = × 10⁻ⁿ.'),
         ('Explain why, after multiplying 6 × 10⁵ by 4 × 10³, the result 24 × 10⁸ must be adjusted.', 'The coefficient 24 is not between 1 and 10; 24 × 10⁸ = 2.4 × 10⁹.')],
    misc=[('3.0 × 10⁴ + 2.0 × 10³ = 5.0 × 10⁷ because you add the numbers and the powers.', 'Powers are only added when multiplying. For addition write both with the same power: 3.0 × 10⁴ + 0.2 × 10⁴ = 3.2 × 10⁴.'),
          ('5.6 × 10⁻³ is larger than 2.1 × 10⁻² because 5.6 is larger than 2.1.', 'Compare the powers first: 10⁻² is ten times 10⁻³, so 2.1 × 10⁻² = 0.021 > 0.0056.'),
          ('A negative power of ten makes the number negative, so 4 × 10⁻² is negative.', '10⁻² = 0.01 is positive; 4 × 10⁻² = 0.04 is a small positive number. A negative number has a minus sign in front of a.')],
))

SCI_CTX = [
    # (stem builder, value fn, unit, working)
    'gdp', 'light', 'cells', 'data', 'virus', 'ocean', 'grains', 'debt',
]


def _sci_context(rng, d):
    kind = pick(rng, SCI_CTX)
    if kind == 'gdp':
        country = pick(rng, ['Germany', 'Brazil', 'Indonesia', 'Nigeria', 'Canada', 'Japan', 'Mexico', 'Kenya', 'Vietnam'])
        g = round(rng.uniform(1.1, 9.8), 2) * 10 ** rng.randint(11, 13)
        p = round(rng.uniform(1.1, 9.8), 2) * 10 ** rng.randint(7, 8)
        v = g / p
        return (f'In one year the gross domestic product (GDP) of {country} was {sci(g)} US dollars and its population was {sci(p)}. '
                f'Calculate the GDP per person, giving your answer in the form a × 10ᵏ.', v, 'US dollars per person',
                f'{sci(g)} ÷ {sci(p)}')
    if kind == 'light':
        planet = pick(rng, ['Mars', 'Jupiter', 'Saturn', 'Neptune', 'a comet', 'a space probe'])
        dist = round(rng.uniform(1.1, 9.9), 2) * 10 ** rng.randint(7, 9)
        v = dist / 3.00e5
        return (f'Light travels at 3.00 × 10⁵ km s⁻¹. At one moment {planet} is {sci(dist)} km from Earth. Find the time, in seconds, '
                f'for a radio signal to travel this distance, giving your answer in the form a × 10ᵏ.', v, 's', f'{sci(dist)} ÷ (3.00 × 10⁵)')
    if kind == 'cells':
        n = round(rng.uniform(1.5, 9.5), 2) * 10 ** rng.randint(12, 14)
        mass = round(rng.uniform(1.1, 9.9), 1) * 10 ** -rng.randint(11, 13)
        v = n * mass
        return (f'A sample contains {sci(n)} cells and each cell has a mass of approximately {sci(mass, 2)} kg. Calculate the total mass '
                f'of the cells in kg, giving your answer in the form a × 10ᵏ.', v, 'kg', f'{sci(n)} × {sci(mass, 2)}')
    if kind == 'data':
        files = rng.randint(12, 980) * 10 ** rng.randint(3, 5)
        size = round(rng.uniform(1.2, 9.6), 1) * 10 ** rng.randint(5, 7)
        v = files * size
        return (f'A data centre in {pick(rng, CITIES)} stores {files:,} files, each of size {sci(size, 2)} bytes. Find the total storage in bytes, '
                f'giving your answer in the form a × 10ᵏ.'.replace(',', ' '), v, 'bytes', f'{files} × {sci(size, 2)}')
    if kind == 'virus':
        dia = round(rng.uniform(1.1, 9.5), 1) * 10 ** -rng.randint(7, 8)
        length = rng.choice([1, 2, 5, 10]) * 1e-3
        v = length / dia
        return (f'A virus particle has a diameter of {sci(dia, 2)} m. Calculate how many such particles, placed side by side, would span '
                f'{int(length * 1000)} mm. Give your answer in the form a × 10ᵏ.', v, 'particles', f'{length} ÷ {sci(dia, 2)}')
    if kind == 'ocean':
        vol = round(rng.uniform(1.1, 9.9), 2) * 10 ** rng.randint(3, 8)
        v = vol * 1e12
        return (f'A reservoir system holds {sci(vol)} km³ of water. Given 1 km³ = 10¹² litres, find the volume in litres in the form a × 10ᵏ.', v,
                'litres', f'{sci(vol)} × 10¹²')
    if kind == 'grains':
        mass = round(rng.uniform(1.1, 9.9), 2) * 10 ** rng.randint(3, 6)
        g = round(rng.uniform(1.1, 9.9), 1) * 10 ** -rng.randint(5, 6)
        v = mass / g
        return (f'A shipment of {sci(mass)} kg of rice is exported from {pick(rng, ["Thailand", "Vietnam", "India", "Pakistan"])}. One grain of rice '
                f'has a mass of about {sci(g, 2)} kg. Estimate the number of grains, in the form a × 10ᵏ.', v, 'grains', f'{sci(mass)} ÷ {sci(g, 2)}')
    debt = round(rng.uniform(1.1, 9.9), 2) * 10 ** rng.randint(11, 13)
    p = round(rng.uniform(1.1, 9.9), 2) * 10 ** rng.randint(6, 8)
    v = debt / p
    return (f'A government owes {sci(debt)} euros and the country has {sci(p)} citizens. Calculate the debt per citizen in the form a × 10ᵏ.', v,
            'euros', f'{sci(debt)} ÷ {sci(p)}')


@R.add('ch01-st1', ALL, (1, 5), 'short')
def sci_core(rng, slot):
    c, d = slot.c, slot.d
    if c == 'C1':
        a = round(rng.uniform(1.01, 9.99), rng.choice([1, 2]))
        k = rng.choice([-7, -6, -5, -4, -3, -2, 3, 4, 5, 6, 7, 8, 9])
        ordn = ordinary(a, k)
        if d <= 1 or rng.random() < 0.35:
            wr = [f'{a} × 10{sup(k + 1)}', f'{a} × 10{sup(-k)}', f'{round(a * 10, 1)} × 10{sup(k - 1)}']
            return mcq(rng, f'Which of the following is {ordn} written in the form a × 10ᵏ, where 1 ≤ a < 10 and k ∈ ℤ?',
                       f'{a} × 10{sup(k)}', wr, f'Move the decimal point {abs(k)} places; {ordn} = {a} × 10{sup(k)}.')
        if rng.random() < 0.5:
            return ret(f'Write {ordn} in the form a × 10ᵏ, where 1 ≤ a < 10 and k ∈ ℤ.', f'{a} × 10{sup(k)}',
                       f'{a} × 10{sup(k)} (A1 for a, A1 for k).', 2 if d >= 2 else 1)
        return ret(f'Write {a} × 10{sup(k)} as an ordinary number.', ordn, f'{ordn} (A1). Accept equivalent with correct place value only.', 1)
    if c == 'C2':
        v = rng.random()
        if v < 0.4:
            a = rng.randint(11, 99) + rng.choice([0, 0.5, 0.2])
            k = rng.randint(-6, 8)
            correct = sci(a * 10 ** k, 3 if a % 1 else 2)
            return ret(f'{name(rng)} writes a population estimate as {a:g} × 10{sup(k)} and says it is in scientific notation. Explain why this is not '
                       f'correct and write the number correctly in the form a × 10ᵏ.', correct,
                       f'R1 the coefficient {a:g} is not in the interval 1 ≤ a < 10; A1 {correct}.', 2, 'explain', gap='G2')
        if v < 0.75:
            a1, a2 = round(rng.uniform(1.1, 9.9), 1), round(rng.uniform(1.1, 9.9), 1)
            k1 = rng.randint(-8, 6)
            k2 = k1 - 1
            if a2 <= a1:
                a1, a2 = a2, a1
            big = f'{a1} × 10{sup(k1)}'
            return ret(f'Without converting to ordinary numbers, explain which is larger: {a1} × 10{sup(k1)} or {a2} × 10{sup(k2)}.', big,
                       f'R1 compare powers first: 10{sup(k1)} is ten times 10{sup(k2)}; since {a2} < 10 the number {a2} × 10{sup(k2)} < 1 × 10{sup(k1)} ≤ {big}. A1 {big} is larger.',
                       2, 'explain')
        a1, a2 = round(rng.uniform(1.1, 9.9), 1), round(rng.uniform(1.1, 9.9), 1)
        k1, k2 = rng.randint(2, 9), rng.randint(-6, 6)
        prod = a1 * a2
        right = sci(prod * 10 ** (k1 + k2), 3)
        return ret(f'{name(rng)} calculates ({a1} × 10{sup(k1)}) × ({a2} × 10{sup(k2)}) and writes {sf(prod)} × 10{sup(k1 + k2)}. '
                   f'Comment on the form of this answer and give it correctly in scientific notation.', right,
                   f'R1 {"the coefficient " + sf(prod) + " is not less than 10, so it must be adjusted" if prod >= 10 else "the answer is already in the correct form"}; A1 {right}.',
                   2, 'explain')
    stem, v, unit, work = _sci_context(rng, d)
    if c == 'C3':
        return ret(stem, f'{sci(v)} {unit}', f'{work} (M1) = {sci(v)} {unit} (A1)(A1 for correct form a × 10ᵏ). Answers not in the form a × 10ᵏ lose the final A1.', 3 if d >= 3 else 2,
                   'numerical')
    # C4: two-stage comparison in context
    if rng.random() < 0.5:
        c1, c2 = rng.sample(['Germany', 'Brazil', 'Indonesia', 'Nigeria', 'Canada', 'Japan', 'Mexico', 'Kenya', 'Vietnam', 'Peru', 'Norway'], 2)
        g1, g2 = [round(rng.uniform(1.1, 9.8), 2) * 10 ** rng.randint(11, 13) for _ in range(2)]
        p1, p2 = [round(rng.uniform(1.1, 9.8), 2) * 10 ** rng.randint(6, 8) for _ in range(2)]
        a1, a2 = g1 / p1, g2 / p2
        hi, lo = (c1, c2) if a1 > a2 else (c2, c1)
        return ret(f'In one year {c1} had a GDP of {sci(g1)} US dollars and a population of {sci(p1)}; {c2} had a GDP of {sci(g2)} US dollars and a population of {sci(p2)}. '
                   f'(a) Find the GDP per person of each country in the form a × 10ᵏ. (b) Find how many times greater the GDP per person of {hi} is than that of {lo}. '
                   f'(c) Find the combined GDP of the two countries in the form a × 10ᵏ.',
                   f'(a) {c1}: {sci(a1)}, {c2}: {sci(a2)} (b) {sf(max(a1, a2) / min(a1, a2))} (c) {sci(g1 + g2)}',
                   f'(a) {sci(g1)} ÷ {sci(p1)} = {sci(a1)}; {sci(g2)} ÷ {sci(p2)} = {sci(a2)} (M1 A1 A1). (b) {sf(max(a1, a2))} ÷ {sf(min(a1, a2))} (M1) = {sf(max(a1, a2) / min(a1, a2))} (A1). '
                   f'(c) rewrite with a common power of ten (M1): {sci(g1 + g2)} (A1).', 7 if d >= 4 else 6, 'multi_step', gap='G5')
    p1, p2 = rng.sample([('Mars', 0.546, 4.01), ('Jupiter', 5.88, 9.68), ('Saturn', 12.0, 16.6), ('Venus', 0.381, 2.61), ('Mercury', 0.770, 2.22)], 2)
    dmin = round(rng.uniform(p1[1], p1[2]), 2) * 1e8
    dmax = round(rng.uniform(p2[1], p2[2]), 2) * 1e8
    t1, t2 = dmin / 3.00e5, dmax / 3.00e5
    return ret(f'Radio signals travel at 3.00 × 10⁵ km s⁻¹. On a given day {p1[0]} is {sci(dmin)} km from Earth and {p2[0]} is {sci(dmax)} km from Earth. '
               f'(a) Find the time, in seconds, for a signal to reach each planet, in the form a × 10ᵏ. (b) A command is sent to a probe at {p2[0]} and the reply returns to Earth immediately. '
               f'Find the total time in minutes, correct to 3 s.f. (c) Find the difference between the one-way times, in the form a × 10ᵏ seconds.',
               f'(a) {sci(t1)} s, {sci(t2)} s (b) {sf(2 * t2 / 60)} min (c) {sci(abs(t2 - t1))} s',
               f'(a) time = distance ÷ speed (M1): {sci(t1)} s (A1), {sci(t2)} s (A1). (b) 2 × {sci(t2)} ÷ 60 (M1) = {sf(2 * t2 / 60)} min (A1). (c) {sci(abs(t2 - t1))} s (A1).',
               6, 'multi_step', gap='G5')


@R.add('ch01-st1', ('C2', 'C3'), (1, 4), 'short')
def sci_arith(rng, slot):
    a1, a2 = round(rng.uniform(1.1, 9.9), 2), round(rng.uniform(1.1, 9.9), 2)
    k1, k2 = rng.randint(-6, 9), rng.randint(-6, 9)
    x1, x2 = a1 * 10 ** k1, a2 * 10 ** k2
    op = pick(rng, ['×', '÷', '+', '−'] if slot.d >= 3 else ['×', '÷'])
    v = {'×': x1 * x2, '÷': x1 / x2, '+': x1 + x2, '−': x1 - x2}[op]
    if v == 0:
        return None
    if slot.c == 'C2':
        hint = {'×': 'multiply the coefficients and add the powers', '÷': 'divide the coefficients and subtract the powers',
                '+': 'rewrite both numbers with the same power of ten before adding', '−': 'rewrite both numbers with the same power of ten before subtracting'}[op]
        return ret(f'Describe the steps needed to calculate ({a1} × 10{sup(k1)}) {op} ({a2} × 10{sup(k2)}) without a calculator, and state the answer in the form a × 10ᵏ.',
                   sci(v), f'R1 {hint}; R1 adjust the coefficient so that 1 ≤ a < 10; A1 {sci(v)}.', 3, 'explain')
    return ret(f'Calculate ({a1} × 10{sup(k1)}) {op} ({a2} × 10{sup(k2)}), giving your answer in the form a × 10ᵏ, where 1 ≤ a < 10, k ∈ ℤ, with a correct to 3 significant figures.',
               sci(v), f'(M1) correct use of index laws or GDC; A1 {sci(v)}.', 2, 'numerical')


# ---- ch01-st2 approximation -------------------------------------------------------------------
R.facts('ch01-st2', F(
    terms=[('significant figures', 'the digits of a number that carry meaning about its precision, counted from the first non-zero digit'),
           ('decimal places', 'the number of digits written after the decimal point'),
           ('estimation', 'finding an approximate answer by rounding the numbers (often to 1 s.f.) before calculating, to check that a result is reasonable')],
    facts=[('How many significant figures does 0.004050 have?', '4', ['3', '6', '7'], 'Leading zeros are not significant; the trailing zero after the 5 is significant: 4, 0, 5, 0.'),
           ('Unless otherwise stated, to what accuracy should non-exact answers be given in IB Mathematics examinations?', '3 significant figures', ['2 decimal places', '1 decimal place', 'the full calculator display'], 'IB instructions: exact or correct to 3 s.f.; money usually to 2 d.p. when required.'),
           ('Which of the following is 0.0698 correct to 2 significant figures?', '0.070', ['0.07', '0.069', '0.0700'], 'The second significant digit 9 rounds up, giving 0.070 – the final zero is significant and must be shown.')],
    why=[('Explain why intermediate values in a calculation should not be rounded before the final answer.', 'Rounding early introduces errors that accumulate through later steps, so the final answer may be wrong at 3 s.f.; keep full GDC values and round only at the end.'),
         ('Explain why rounding 3 249 to 2 significant figures gives 3 200 and not 32.', 'Rounding must preserve place value; the zeros are place holders that keep the number in the thousands.'),
         ('Explain why an answer for the number of buses needed for a school trip should be rounded up rather than to the nearest whole number.', 'Every student needs a seat; rounding down would leave some students without a bus, so the context requires the next whole number.')],
    misc=[('0.00340 has 6 significant figures because it has 6 digits.', 'Leading zeros only fix the position of the decimal point; 0.00340 has 3 significant figures (3, 4 and the trailing 0).'),
          ('Rounding 2.96 to 1 decimal place gives 2.1.', 'The digit 9 in the first decimal place rounds up to 10, carrying into the units: 2.96 ≈ 3.0 (1 d.p.).'),
          ('An answer of 4.5 is the same as 4.50 when giving answers to 3 significant figures.', 'Their values are equal but 4.50 claims accuracy to the hundredths; to 3 s.f. the zero must be written: 4.50.')],
))


def _num_for_rounding(rng, d):
    k = rng.randint(-4, 5) if d >= 2 else rng.randint(-2, 3)
    digits = rng.randint(4, 7)
    mant = rng.randint(10 ** (digits - 1), 10 ** digits - 1)
    if rng.random() < 0.3:  # make a carry likely
        s = list(str(mant))
        s[1:3] = ['9', '9'] if len(s) > 3 else s[1:3]
        s[3] = str(rng.randint(5, 9)) if len(s) > 3 else s[-1]
        mant = int(''.join(s))
    return Decimal(mant).scaleb(k - digits + 1)


@R.add('ch01-st2', ALL, (1, 5), 'short')
def rounding_core(rng, slot):
    c, d = slot.c, slot.d
    x = _num_for_rounding(rng, d)
    xs = format(x.normalize(), 'f')
    if c == 'C1':
        n = rng.choice([1, 2, 3, 4])
        dp = rng.choice([1, 2, 3])
        a_sf = dsf(x, n)
        a_dp = format(dround(x, dp), 'f')
        if d <= 1:
            wr = [dsf(x, n + 1), format(dround(x, n), 'f'), a_sf.rstrip('0').rstrip('.') + ('1' if '.' in a_sf else '0')]
            return mcq(rng, f'Which of the following is {xs} correct to {n} significant figure{"s" if n > 1 else ""}?', a_sf, wr,
                       f'Count {n} digit{"s" if n > 1 else ""} from the first non-zero digit and round: {a_sf}.')
        return ret(f'Write {xs} correct to (i) {n} significant figure{"s" if n > 1 else ""}; (ii) {dp} decimal place{"s" if dp > 1 else ""}.',
                   f'(i) {a_sf} (ii) {a_dp}', f'(i) {a_sf} A1 (ii) {a_dp} A1. Zeros needed for place value or accuracy must be shown.', 2)
    if c == 'C2':
        n = rng.choice([2, 3])
        right = dsf(x, n)
        v = rng.random()
        if v < 0.5:
            # student drops place-holder zeros or counts leading zeros
            if x < 1:
                wrongv = format(dround(x, n), 'f')
                err = 'counted decimal places instead of significant figures (leading zeros are not significant)'
            else:
                wrongv = right.replace('.', '').lstrip('0')[:n] if x >= 10 ** n else format(dround(x, n), 'f')
                err = 'lost the place-value zeros, changing the size of the number' if x >= 10 ** n else 'rounded to decimal places instead of significant figures'
            if wrongv == right:
                return None
            return ret(f'{name(rng)} rounds {xs} to {n} significant figures and writes {wrongv}. Explain the error and give the correct answer.', right,
                       f'R1 {err}; A1 {right}.', 2, 'explain', gap='G2')
        y = round(rng.uniform(1.2, 9.8), 2)
        z = round(rng.uniform(1.2, 9.8), 2)
        early = float(dsf(y * z, 2)) ** 2
        late = (y * z) ** 2
        return ret(f'To evaluate ({y} × {z})², {name(rng)} first rounds {y} × {z} to 2 significant figures and then squares it. Show that this gives a '
                   f'different answer, correct to 3 significant figures, from evaluating the whole expression on a GDC, and explain why.',
                   f'{sf(early)} vs {sf(late)}',
                   f'Rounded first: {dsf(y * z, 2)}² = {sf(early)} (A1); GDC: {sf(late)} (A1); R1 early rounding introduces an error that is magnified by squaring.',
                   3, 'explain')
    if c == 'C3':
        a, b, cc = round(rng.uniform(10, 99), 1), round(rng.uniform(0.11, 0.99), 3), round(rng.uniform(1.1, 9.9), 2)
        form = rng.randint(0, 3)
        if form == 0:
            v = math.sqrt(a) * b / cc
            ex = f'√{a} × {b} ÷ {cc}'
        elif form == 1:
            v = (a + cc ** 2) / (b * 100)
            ex = f'({a} + {cc}²) ÷ ({b} × 100)'
        elif form == 2:
            v = a ** (1 / 3) + cc / b
            ex = f'∛{a} + {cc}/{b}'
        else:
            v = (a * b) ** 2 / cc
            ex = f'({a} × {b})² ÷ {cc}'
        full = f'{v:.9g}'
        if d <= 2:
            return ret(f'Use your GDC to evaluate {ex}. Write down (i) the full calculator display; (ii) the answer correct to 3 significant figures.',
                       f'(i) {full} (ii) {sf(v)}', f'(i) {full} (A1) (ii) {sf(v)} (A1).', 2, 'numerical')
        dp = rng.choice([1, 2])
        return ret(f'Evaluate {ex}, giving your answer (i) correct to 3 significant figures; (ii) correct to {dp} decimal place{"s" if dp > 1 else ""}; (iii) in the form a × 10ᵏ to 3 s.f.',
                   f'(i) {sf(v)} (ii) {format(dround(v, dp), "f")} (iii) {sci(v)}', f'(i) {sf(v)} A1 (ii) {format(dround(v, dp), "f")} A1 (iii) {sci(v)} A1.', 3, 'numerical')
    # C4: estimation and rounding in context
    v = rng.random()
    if v < 0.5:
        L, W, H = round(rng.uniform(4.1, 9.8), 2), round(rng.uniform(3.1, 7.9), 2), round(rng.uniform(2.4, 3.2), 2)
        cover = rng.choice([10, 12, 14, 15])
        coats = rng.choice([1, 2])
        area = 2 * (L + W) * H
        tins = math.ceil(area * coats / cover)
        est = 2 * (float(dsf(L, 1)) + float(dsf(W, 1))) * float(dsf(H, 1))
        return ret(f'A room in {pick(rng, CITIES)} is {L} m long, {W} m wide and {H} m high. The four walls are to be painted with {coats} coat{"s" if coats > 1 else ""}; one tin covers {cover} m². '
                   f'(a) Estimate the wall area by rounding each dimension to 1 significant figure. (b) Calculate the wall area, correct to 3 s.f. (c) Find the number of tins that must be bought, justifying your rounding.',
                   f'(a) {sf(est)} m² (b) {sf(area)} m² (c) {tins} tins',
                   f'(a) 2({dsf(L, 1)} + {dsf(W, 1)}) × {dsf(H, 1)} = {sf(est)} m² (M1 A1). (b) 2({L} + {W}) × {H} = {sf(area)} m² (M1 A1). '
                   f'(c) {coats} × {sf(area)} ÷ {cover} = {sf(area * coats / cover)} (M1); round UP since part of a tin cannot be bought and the walls must be covered: {tins} (A1 R1).',
                   7 if d >= 4 else 6, 'multi_step', gap='G5')
    people = rng.randint(140, 980)
    seats = rng.choice([45, 49, 52, 57, 60])
    cost = rng.randint(380, 950)
    buses = math.ceil(people / seats)
    per = cost * buses / people
    cc_ = cur(rng)
    return ret(f'{people} students from a school in {city_for(rng, cc_)} travel to a sports event. Each bus holds {seats} passengers and costs {cost} {cc_} to hire. '
               f'(a) Find the number of buses needed. (b) The total cost is shared equally; find the cost per student correct to 2 decimal places. (c) Explain why the answer to (a) is not found by rounding to the nearest integer.',
               f'(a) {buses} (b) {money(per)} (c) rounding to the nearest integer could leave students without seats',
               f'(a) {people} ÷ {seats} = {sf(people / seats)} (M1) → {buses} buses (A1). (b) {buses} × {cost} ÷ {people} = {money(per)} (M1 A1). (c) R1 all students must be seated, so always round up.',
               5, 'multi_step', gap='G5')


@R.add('ch01-st2', ('C2', 'C3'), (1, 4), 'short')
def estimate_check(rng, slot):
    a, b, cc = round(rng.uniform(11, 98), 1), round(rng.uniform(2.1, 9.8), 2), round(rng.uniform(0.21, 0.98), 2)
    est = float(dsf(a, 1)) * float(dsf(b, 1)) / float(dsf(cc, 1))
    v = a * b / cc
    if slot.c == 'C2':
        wrong = v * 10
        return ret(f'{name(rng)} uses a calculator to find ({a} × {b}) ÷ {cc} and obtains {sf(wrong)}. By rounding each number to 1 significant figure, '
                   f'explain whether this answer is reasonable.', f'Not reasonable: estimate ≈ {sf(est, 2)}, true value {sf(v)}',
                   f'M1 estimate ({dsf(a, 1)} × {dsf(b, 1)}) ÷ {dsf(cc, 1)} = {sf(est, 2)}; R1 {sf(wrong)} is about ten times too large, so a key was mis-entered (true value {sf(v)}).',
                   3, 'explain', gap='G2')
    return ret(f'(a) Estimate the value of ({a} × {b}) ÷ {cc} by rounding each number to 1 significant figure. (b) Use your GDC to find the exact value correct to 3 significant figures.',
               f'(a) {sf(est, 2)} (b) {sf(v)}', f'(a) ({dsf(a, 1)} × {dsf(b, 1)}) ÷ {dsf(cc, 1)} (M1) = {sf(est, 2)} (A1). (b) {sf(v)} (A1).', 3, 'numerical')


# ---- ch01-st3 bounds and percentage error ------------------------------------------------------
R.facts('ch01-st3', F(
    terms=[('upper bound', 'the largest value that a rounded measurement could have had before it was rounded (the boundary itself is not reached)'),
           ('lower bound', 'the smallest value that a rounded measurement could have had before it was rounded'),
           ('percentage error', 'ε = |v_A − v_E| / |v_E| × 100%, where v_A is the approximate value and v_E the exact value'),
           ('error interval', 'an inequality LB ≤ x < UB giving the range of possible values of a rounded measurement')],
    facts=[('A length is 8.4 cm to the nearest 0.1 cm. Which is its error interval?', '8.35 ≤ L < 8.45', ['8.3 ≤ L < 8.5', '8.35 < L ≤ 8.45', '8.40 ≤ L < 8.50'], 'Half a unit (0.05) either side of 8.4; the upper bound itself would round to 8.5.'),
           ('To find the upper bound of a − b, which combination is used?', 'upper bound of a − lower bound of b', ['upper bound of a − upper bound of b', 'lower bound of a − lower bound of b', 'lower bound of a − upper bound of b'], 'The difference is largest when a is as large and b as small as possible.'),
           ('To find the lower bound of a ÷ b, which combination is used?', 'lower bound of a ÷ upper bound of b', ['lower bound of a ÷ lower bound of b', 'upper bound of a ÷ upper bound of b', 'upper bound of a ÷ lower bound of b'], 'A quotient is smallest when the numerator is smallest and the denominator largest.')],
    why=[('Explain why the upper bound of a measurement of 12 cm (nearest cm) is 12.5 cm even though 12.5 would round to 13.', 'The upper bound is the boundary of the interval 11.5 ≤ x < 12.5; values arbitrarily close to 12.5 round to 12, so 12.5 is the least upper bound, although it is not itself included.'),
         ('Explain why the percentage error uses the absolute value of v_A − v_E.', 'Percentage error measures the size of the error relative to the exact value; whether the approximation is too big or too small does not matter, so the modulus is taken.'),
         ('Explain why a percentage error of 2% may be acceptable in one context but not in another.', 'Acceptability depends on purpose: 2% on the length of a garden fence is negligible, but 2% on a drug dose or engineering tolerance could be dangerous.')],
    misc=[('If a mass is 60 kg to the nearest 10 kg, its upper bound is 60.5 kg.', 'The bounds are half of the rounding unit either side: 55 ≤ m < 65 kg, so the upper bound is 65 kg.'),
          ('The upper bound of a difference is found by subtracting the two upper bounds.', 'Subtracting the upper bounds does not maximise a difference; use UB(first) − LB(second).'),
          ('Percentage error is (exact − approximate) ÷ approximate × 100%.', 'The denominator is the exact value: ε = |v_A − v_E| / |v_E| × 100%.')],
))


def _bound_meas(rng, d):
    unit_kind = rng.randint(0, 2)
    if unit_kind == 0:
        v = rng.randint(12, 95)
        return v, 1, 'to the nearest whole number', v - 0.5, v + 0.5
    if unit_kind == 1:
        v = round(rng.uniform(2.1, 19.9), 1)
        return v, 0.1, 'correct to 1 decimal place', round(v - 0.05, 2), round(v + 0.05, 2)
    v = rng.randint(2, 9) * 10 + rng.choice([0, 10, 20, 50])
    return v, 10, 'to the nearest 10', v - 5, v + 5


@R.add('ch01-st3', ALL, (1, 5), 'short')
def bounds_core(rng, slot):
    c, d = slot.c, slot.d
    if c == 'C1':
        v, u, phrase, lb, ub = _bound_meas(rng, d)
        thing = pick(rng, [('the length of a corridor', 'm'), ('the mass of a parcel', 'kg'), ('the time for a race', 's'), ('the volume of a tank', 'L')])
        if d <= 1:
            return mcq(rng, f'{thing[0][0].upper() + thing[0][1:]} is recorded as {v:g} {thing[1]}, {phrase}. What is its lower bound?', f'{lb:g} {thing[1]}',
                       [f'{(v - u):g} {thing[1]}', f'{ub:g} {thing[1]}', f'{(v - u / 10):g} {thing[1]}'], f'Lower bound = {v:g} − half of {u:g} = {lb:g}.')
        return ret(f'{thing[0][0].upper() + thing[0][1:]} is {v:g} {thing[1]}, {phrase}. Write down the error interval for this measurement.', f'{lb:g} ≤ x < {ub:g}',
                   f'A1 for {lb:g} and {ub:g}; A1 for correct inequality signs.', 2)
    if c == 'C2':
        a, b = rng.randint(30, 90), rng.randint(5, 25)
        ub = (a + 0.5) - (b - 0.5)
        wrong = (a + 0.5) - (b + 0.5)
        return ret(f'Two lengths are {a} cm and {b} cm, each to the nearest cm. {name(rng)} says the upper bound of their difference is ({a}.5 − {b}.5) = {wrong:g} cm. '
                   f'Explain why this is wrong and find the correct upper bound.', f'{ub:g} cm',
                   f'R1 the difference is greatest when the first length is largest and the second smallest; M1 {a + 0.5:g} − {b - 0.5:g}; A1 {ub:g} cm.', 3, 'explain', gap='G2')
    if c == 'C3':
        if rng.random() < 0.5:
            L, W = round(rng.uniform(3.1, 12.9), 1), round(rng.uniform(2.1, 8.9), 1)
            lo, hi = (L - 0.05) * (W - 0.05), (L + 0.05) * (W + 0.05)
            what = pick(rng, ['a classroom floor', 'a vegetable plot', 'a car-park bay row', 'a community garden bed', 'a school stage'])
            return ret(f'The length and width of {what} are {L} m and {W} m, each correct to 1 decimal place. Find the lower and upper bounds of its area.',
                       f'LB {sf(lo, 4)} m², UB {sf(hi, 4)} m²', f'Bounds {L - 0.05:.2f}, {L + 0.05:.2f} and {W - 0.05:.2f}, {W + 0.05:.2f} (A1); LB = {sf(lo, 4)} (M1 A1); UB = {sf(hi, 4)} (A1).',
                       4 if d >= 3 else 3, 'numerical')
        vE = rng.choice([math.pi, math.sqrt(2), math.e, math.sqrt(3), round(rng.uniform(10, 500), 2)])
        vA = float(dsf(vE, rng.choice([1, 2])))
        eps = abs(vA - vE) / abs(vE) * 100
        lab = {math.pi: 'π', math.sqrt(2): '√2', math.e: 'e', math.sqrt(3): '√3'}.get(vE, f'{vE}')
        return ret(f'{name(rng)} approximates {lab} by {vA:g}. Calculate the percentage error.', f'{sf(eps)}%',
                   f'ε = |{vA:g} − {lab}| ÷ {lab} × 100% (M1) = {sf(eps)}% (A1).', 2, 'numerical')
    # C4 speed from bounded distance and time / or max % error
    if rng.random() < 0.5:
        dist = rng.choice([100, 200, 400, 800, 1500])
        t = round(rng.uniform(dist / 9.5, dist / 6.0), 1)
        dlo, dhi = dist - 0.5, dist + 0.5
        tlo, thi = t - 0.05, t + 0.05
        vlo, vhi = dlo / thi, dhi / tlo
        who = name(rng)
        return ret(f'{who} runs {dist} m (to the nearest metre) in {t} s (to the nearest 0.1 s). (a) Find the upper and lower bounds of {who}\'s average speed. '
                   f'(b) {who} claims an average speed of at least {sf(vlo * 0.999, 3)} m s⁻¹. Determine whether the claim is certainly true, justifying your answer.',
                   f'(a) LB {sf(vlo, 4)} m s⁻¹, UB {sf(vhi, 4)} m s⁻¹ (b) yes, since LB > claim',
                   f'(a) LB = {dlo} ÷ {thi:.2f} (M1) = {sf(vlo, 4)} (A1); UB = {dhi} ÷ {tlo:.2f} (M1) = {sf(vhi, 4)} (A1). (b) R1 even the lower bound exceeds the claimed value, so the claim is certainly true.',
                   6, 'multi_step', gap='G5')
    r = round(rng.uniform(2.1, 9.9), 1)
    vE = math.pi * r ** 2
    vA = 3 * float(dsf(r, 1)) ** 2
    eps = abs(vA - vE) / vE * 100
    return ret(f'The radius of a circular pond is {r} m. {name(rng)} estimates its area using π ≈ 3 and the radius rounded to 1 significant figure. '
               f'(a) Find the estimate. (b) Find the exact area correct to 3 s.f. (c) Calculate the percentage error and comment on whether the estimate is suitable for ordering pond liner.',
               f'(a) {sf(vA)} m² (b) {sf(vE)} m² (c) {sf(eps)}%', f'(a) 3 × {dsf(r, 1)}² = {sf(vA)} (A1). (b) π × {r}² = {sf(vE)} (M1 A1). (c) |{sf(vA)} − {sf(vE)}| ÷ {sf(vE)} × 100 (M1) = {sf(eps)}% (A1); '
               f'R1 {"too large an error – an under-estimate would leave the pond uncovered" if vA < vE or eps > 5 else "acceptable but order a margin"}.', 6, 'multi_step', gap='G5')


@R.add('ch01-st3', ('C2', 'C3', 'C4'), (2, 5), 'short')
def bounds_quot(rng, slot):
    mass = rng.randint(120, 980)
    vol = rng.randint(20, 90)
    mat = pick(rng, ['a block of an unknown alloy', 'a sample of granite', 'a bar of soap', 'a piece of oak', 'a jar of honey'])
    dlo, dhi = (mass - 0.5) / (vol + 0.5), (mass + 0.5) / (vol - 0.5)
    if slot.c == 'C2':
        return ret(f'The mass of {mat} is {mass} g and its volume is {vol} cm³, both to the nearest whole number. Explain which bounds of mass and volume give the upper bound of its density, and find it.',
                   f'{sf(dhi, 4)} g cm⁻³', f'R1 density = mass ÷ volume is largest for the largest mass and smallest volume; M1 {mass + 0.5} ÷ {vol - 0.5}; A1 {sf(dhi, 4)} g cm⁻³.', 3, 'explain')
    if slot.c == 'C3':
        return ret(f'The mass of {mat} is {mass} g and its volume is {vol} cm³, both correct to the nearest whole number. Calculate the lower and upper bounds of its density.',
                   f'{sf(dlo, 4)} ≤ ρ < {sf(dhi, 4)} g cm⁻³', f'LB = {mass - 0.5} ÷ {vol + 0.5} (M1) = {sf(dlo, 4)} (A1); UB = {mass + 0.5} ÷ {vol - 0.5} (M1) = {sf(dhi, 4)} (A1).', 4, 'numerical')
    est = mass / vol
    return ret(f'The mass of {mat} is {mass} g and its volume is {vol} cm³, both to the nearest whole number. (a) Find the bounds of the density. (b) State the density to a suitable degree of accuracy, '
               f'justifying your choice. (c) Find the maximum percentage error in using {sf(est)} g cm⁻³ as the density.',
               f'(a) {sf(dlo, 4)} to {sf(dhi, 4)} (b) {dsf(dlo, 2) if dsf(dlo, 2) == dsf(dhi, 2) else dsf(dlo, 1)} g cm⁻³ (c) {sf(max(abs(est - dlo) / dlo, abs(est - dhi) / dhi) * 100)}%',
               f'(a) M1 A1 A1. (b) R1 give the most accurate value to which both bounds round the same. (c) largest |{sf(est)} − bound| ÷ bound × 100 (M1) = {sf(max(abs(est - dlo) / dlo, abs(est - dhi) / dhi) * 100)}% (A1).',
               6, 'multi_step', gap='G5')


# =============================================================================================
# ch02 Sequences and series
# =============================================================================================
def _seq_list(a, d, n=4, geo=False):
    vals = [a * d ** i if geo else a + i * d for i in range(n)]
    return ', '.join(sf(v, 4) if isinstance(v, float) and not float(v).is_integer() else str(int(v)) for v in vals)


R.facts('ch02-st1', F(
    terms=[('arithmetic sequence', 'a sequence in which each term is obtained from the previous one by adding a constant common difference d'),
           ('common difference', 'the constant d = uₙ₊₁ − uₙ between consecutive terms of an arithmetic sequence'),
           ('arithmetic series', 'the sum of the terms of an arithmetic sequence, Sₙ = n/2 (2u₁ + (n − 1)d) = n/2 (u₁ + uₙ)')],
    facts=[('Which formula gives the nth term of an arithmetic sequence?', 'uₙ = u₁ + (n − 1)d', ['uₙ = u₁ + nd', 'uₙ = u₁ rⁿ⁻¹', 'uₙ = n/2 (u₁ + d)'], 'There are n − 1 steps of size d from u₁ to uₙ.'),
           ('Which of these is an arithmetic sequence?', '12, 8.5, 5, 1.5, …', ['2, 4, 8, 16, …', '1, 4, 9, 16, …', '3, −3, 3, −3, …'], 'The difference is constantly −3.5.'),
           ('An arithmetic sequence has a negative common difference. What happens to its terms?', 'They decrease by the same amount each time', ['They decrease by the same percentage each time', 'They approach zero', 'They alternate in sign'], 'A constant negative difference gives a linear decrease.')],
    why=[('Explain why the graph of uₙ against n for an arithmetic sequence consists of points on a straight line.', 'uₙ = u₁ + (n − 1)d = dn + (u₁ − d) is linear in n with gradient d, so the points (n, uₙ) are collinear (but discrete).'),
         ('Explain the reasoning behind the formula Sₙ = n/2 (u₁ + uₙ).', 'Write the series forwards and backwards and add: each of the n pairs sums to u₁ + uₙ, so 2Sₙ = n(u₁ + uₙ).'),
         ('Explain why an arithmetic model of a person\'s savings may be unrealistic over a long period.', 'It assumes the same increase every period forever; in reality income, spending and interest change, and savings usually grow by percentages (geometric) rather than fixed amounts.')],
    misc=[('The 20th term of 5, 9, 13, … is 5 + 20 × 4 = 85.', 'There are only 19 steps from u₁ to u₂₀: u₂₀ = 5 + 19 × 4 = 81.'),
          ('In an arithmetic series, if uₙ is negative then Sₙ must also be negative.', 'Sₙ adds all terms; earlier positive terms can outweigh later negative terms, so Sₙ can still be positive.')],
))

AR_CTX = [
    ('theatre', 'The rows of seats in a theatre in {city} form an arithmetic sequence: the first row has {a} seats and each row has {d} more seats than the row in front.', 'row', 'seats',
     'the number of seats in row {n}', 'the total number of seats in the first {n} rows'),
    ('savings', '{who} saves {a} {cur} in the first month and increases the amount saved by {d} {cur} each month.', 'month', '{cur}',
     'the amount saved in month {n}', 'the total amount saved in the first {n} months'),
    ('training', 'In a training programme {who} runs {a} km in week 1 and increases the distance by {d} km each week.', 'week', 'km',
     'the distance run in week {n}', 'the total distance run in the first {n} weeks'),
    ('salary', 'A graduate engineer in {city} earns {a} {cur} in the first year, with a fixed annual increase of {d} {cur}.', 'year', '{cur}',
     'the salary in year {n}', 'the total earned in the first {n} years'),
    ('logs', 'Logs are stacked in layers; the bottom layer has {a} logs and each layer above has {d} fewer.', 'layer', 'logs',
     'the number of logs in layer {n} (counting from the bottom)', 'the total number of logs in the bottom {n} layers'),
    ('pages', '{who} reads {a} pages on day 1 of a reading challenge and {d} more pages each day than the day before.', 'day', 'pages',
     'the number of pages read on day {n}', 'the total number of pages read in the first {n} days'),
]


def _ar_ctx(rng, d):
    kind, tmpl, step, unit, tp, sp = pick(rng, AR_CTX)
    c = curm(rng)
    if kind == 'theatre':
        a, dd = rng.randint(14, 30), rng.randint(2, 4)
    elif kind == 'savings':
        a, dd = rng.randint(4, 30) * 5, rng.randint(1, 6) * 5
    elif kind == 'training':
        a, dd = round(rng.uniform(2, 6), 1), rng.choice([0.5, 0.4, 0.8, 1.2, 1.5])
    elif kind == 'salary':
        a, dd = rng.randint(30, 80) * 1000, rng.randint(8, 30) * 100
    elif kind == 'logs':
        a, dd = rng.randint(18, 40), -1
    else:
        a, dd = rng.randint(10, 30), rng.randint(2, 6)
    text = tmpl.format(city=city_for(rng, c), a=a, d=abs(dd), cur=c, who=name(rng))
    return kind, text, step, unit.format(cur=c), a, dd, tp, sp


def _num(v):
    v = float(v)
    if v.is_integer():
        return str(int(v))
    t = round(v, 4)
    if abs(t - v) < 1e-9:
        return f'{t:g}'
    return sf(v)


@R.add('ch02-st1', ALL, (1, 5), 'short')
def arith_core(rng, slot):
    c, d = slot.c, slot.d
    if c == 'C1':
        a, dd = rng.randint(-20, 40), rng.choice([-7, -5, -4, -3, 2, 3, 4, 6, 7, 9, 11, 2.5, 1.5])
        n = rng.randint(12, 60)
        un = a + (n - 1) * dd
        seq = _seq_list(a, dd)
        if d <= 1:
            return nmcq(rng, f'Find u{n} for the arithmetic sequence {m(seq)}, …', un, [a + n * dd, a + (n - 2) * dd, a * n + dd], f'u{n} = {a} + ({n} − 1)({m(dd)}) = {m(_num(un))}.', fmtf=lambda z: m(_num(z)))
        return ret(f'For the arithmetic sequence {m(seq)}, … write down the common difference and find u{n}.', f'd = {m(_num(dd))}, u{n} = {m(_num(un))}',
                   f'd = {m(_num(dd))} (A1); u{n} = {m(a)} + {n - 1}({m(_num(dd))}) (M1) = {m(_num(un))} (A1).', 3 if d >= 2 else 2)
    kind, text, step, unit, a, dd, tp, sp = _ar_ctx(rng, d)
    n = rng.randint(8, 30)
    if kind == 'logs':
        n = rng.randint(5, a - 3)
    un = a + (n - 1) * dd
    Sn = n / 2 * (2 * a + (n - 1) * dd)
    if c == 'C2':
        if rng.random() < 0.5:
            return ret(f'{text} Explain why the numbers of {unit} in successive {step}s form an arithmetic sequence, and interpret the values of u₁ and d in this context.',
                       f'Constant change of {_num(dd)} {unit} per {step}; u₁ = {a} {unit} in the first {step}, d = {_num(dd)}.',
                       f'R1 the same amount ({_num(abs(dd))} {unit}) is {"added" if dd > 0 else "subtracted"} each {step}, so the difference between consecutive terms is constant; '
                       f'A1 u₁ = {a} is the value for {step} 1; A1 d = {_num(dd)} is the change per {step}.', 3, 'explain')
        wrong = a + n * dd
        return ret(f'{text} {name(rng)} calculates the value for {step} {n} as {a} + {n} × {_num(dd)} = {_num(wrong)}. Explain the mistake and find the correct value.',
                   f'{_num(un)} {unit}', f'R1 there are {n - 1} differences between {step} 1 and {step} {n}, not {n}; M1 u{n} = {a} + {n - 1} × {_num(dd)}; A1 {_num(un)}.', 3, 'explain', gap='G2')
    if c == 'C3':
        return ret(f'{text} (a) Find {tp.format(n=n)}. (b) Find {sp.format(n=n)}.',
                   f'(a) {_num(un)} (b) {_num(Sn)}', f'(a) u{n} = {a} + ({n} − 1)({_num(dd)}) (M1) = {_num(un)} (A1). (b) S{n} = {n}/2 (2 × {a} + {n - 1} × {_num(dd)}) (M1) = {_num(Sn)} (A1).',
                   4 if d >= 3 else 3, 'numerical')
    # C4: first n for which the total passes a target
    if kind == 'logs':
        target = int(Sn) - rng.randint(1, 5)
    else:
        target = Sn * rng.uniform(1.3, 2.2)
        target = int(round(target, -max(0, len(str(int(target))) - 2)))
    k = 1
    while k * (2 * a + (k - 1) * dd) / 2 < target:
        k += 1
        if k > 500:
            return None
    Sk = k * (2 * a + (k - 1) * dd) / 2
    return ret(f'{text} (a) Write down an expression for the total after n {step}s. (b) Find the least number of {step}s needed for the total to reach at least {target} {unit}. '
               f'(c) For this number of {step}s, find {tp.format(n="n")}.', f'(a) Sₙ = n/2 (2 × {a} + (n − 1)({_num(dd)})) (b) {k} (c) {_num(a + (k - 1) * dd)} {unit}',
               f'(a) A1 correct Sₙ. (b) M1 Sₙ ≥ {target} (inequality or GDC table/graph); S{k - 1} = {_num((k - 1) * (2 * a + (k - 2) * dd) / 2)}, S{k} = {_num(Sk)} (A1); n = {k} (A1). '
               f'(c) u{k} = {a} + {k - 1} × {_num(dd)} (M1) = {_num(a + (k - 1) * dd)} (A1).', 6, 'multi_step', gap='G5')


@R.add('ch02-st1', ('C3', 'C4'), (2, 5), 'short')
def arith_two_terms(rng, slot):
    a, dd = rng.randint(-15, 30), rng.choice([-4, -3, -2, 2, 3, 5, 7, 1.5, 2.5])
    p, q = sorted(rng.sample(range(2, 15), 2))
    up, uq = a + (p - 1) * dd, a + (q - 1) * dd
    n = rng.randint(20, 50)
    Sn = n / 2 * (2 * a + (n - 1) * dd)
    if slot.c == 'C3':
        return ret(f'In an arithmetic sequence u{p} = {m(_num(up))} and u{q} = {m(_num(uq))}. Find the common difference and the first term.', f'd = {m(_num(dd))}, u₁ = {m(a)}',
                   f'Two equations u₁ + {p - 1}d = {m(_num(up))}, u₁ + {q - 1}d = {m(_num(uq))} (M1); d = {m(_num(dd))} (A1); u₁ = {m(a)} (A1).', 3, 'numerical')
    return ret(f'The {p}th term of an arithmetic sequence is {m(_num(up))} and the {q}th term is {m(_num(uq))}. (a) Find the common difference and the first term. (b) Find the sum of the first {n} terms. '
               f'(c) Find the first term of the sequence that is {"greater than 200" if dd > 0 else "less than −200"}.',
               f'(a) d = {m(_num(dd))}, u₁ = {m(a)} (b) {m(_num(Sn))} (c) see key',
               f'(a) simultaneous equations (M1) d = {m(_num(dd))}, u₁ = {m(a)} (A1 A1). (b) S{n} = {n}/2(2({m(a)}) + {n - 1}({m(_num(dd))})) (M1) = {m(_num(Sn))} (A1). '
               f'(c) solve {m(a)} + (n − 1)({m(_num(dd))}) {">" if dd > 0 else "<"} {200 if dd > 0 else "−200"} (M1): n = {math.floor((200 - a) / dd) + 2 if dd > 0 else math.floor((-200 - a) / dd) + 2}, '
               f'term = {m(_num(a + (math.floor((200 - a) / dd) + 1) * dd if dd > 0 else a + (math.floor((-200 - a) / dd) + 1) * dd))} (A1).',
               6, 'multi_step', gap='G5')


R.facts('ch02-st2', F(
    terms=[('geometric sequence', 'a sequence in which each term is obtained by multiplying the previous term by a constant common ratio r'),
           ('common ratio', 'the constant r = uₙ₊₁ ÷ uₙ of a geometric sequence'),
           ('geometric series', 'the sum of terms of a geometric sequence, Sₙ = u₁(rⁿ − 1)/(r − 1) for r ≠ 1')],
    facts=[('A population grows by 4% each year. What is the common ratio of the geometric sequence of yearly populations?', '1.04', ['0.04', '4', '1.4'], 'Each year the population is 100% + 4% = 104% of the previous one.'),
           ('A car loses 15% of its value each year. What is the common ratio?', '0.85', ['0.15', '1.15', '−0.15'], 'It keeps 85% of its value each year.'),
           ('Which formula gives the nth term of a geometric sequence?', 'uₙ = u₁rⁿ⁻¹', ['uₙ = u₁rⁿ', 'uₙ = u₁ + (n − 1)r', 'uₙ = (u₁r)ⁿ⁻¹'], 'There are n − 1 multiplications by r from u₁ to uₙ.')],
    why=[('Explain why repeated percentage increases produce a geometric sequence rather than an arithmetic one.', 'An increase of p% multiplies the current value by (1 + p/100); the same multiplier each step gives a constant ratio, so the amount added grows as the value grows.'),
         ('Explain why a geometric sequence with 0 < r < 1 has terms that decrease but never become negative.', 'Each term is a positive fraction of the one before; multiplying a positive number by a positive r < 1 makes it smaller but still positive, so the terms approach 0.'),
         ('Explain why logarithms (or a GDC table) are needed to find n when uₙ = u₁rⁿ⁻¹ is given.', 'n appears in the exponent; taking logarithms (or searching a table/graph) is the way to undo the exponential.')],
    misc=[('A value that increases by 5% per year for 10 years increases by 50% in total.', 'Growth compounds: 1.05¹⁰ = 1.63, an increase of about 63%, not 50%.'),
          ('If a sequence decreases by 20% each year then r = −0.2.', 'A 20% decrease keeps 80% of the value, so r = 0.8. A negative ratio would make the terms alternate in sign.')],
))

GEO_CTX = [
    ('pop', 'The population of a town in {country} was {a} at the start of 2020 and is increasing by {p}% per year.', 'year', 'people', 1),
    ('ball', 'A ball is dropped from a height of {a} m. After each bounce it rises to {p}% of its previous height.', 'bounce', 'm', -1),
    ('salary', '{who} is offered a starting salary of {a} {cur} with an increase of {p}% each year.', 'year', '{cur}', 1),
    ('bact', 'A bacteria culture has {a} cells and the number increases by {p}% every hour.', 'hour', 'cells', 1),
    ('views', 'A video receives {a} views on its first day; daily views then fall by {p}% each day.', 'day', 'views', -1),
    ('drug', 'A patient is given {a} mg of a medicine; each hour the amount in the bloodstream decreases by {p}%.', 'hour', 'mg', -1),
]


def _geo_ctx(rng, d):
    kind, tmpl, step, unit, sgn_ = pick(rng, GEO_CTX)
    c = curm(rng)
    if kind == 'pop':
        a, p = rng.randint(12, 95) * 1000, round(rng.uniform(1.2, 4.8), 1)
    elif kind == 'ball':
        a, p = rng.choice([1.5, 2, 2.4, 3, 4, 5]), rng.choice([55, 60, 65, 70, 75, 80])
    elif kind == 'salary':
        a, p = rng.randint(30, 75) * 1000, round(rng.uniform(2, 5.5), 1)
    elif kind == 'bact':
        a, p = rng.randint(2, 50) * 100, rng.choice([10, 12, 15, 20, 25, 30])
    elif kind == 'views':
        a, p = rng.randint(20, 90) * 1000, rng.choice([8, 10, 12, 15, 20])
    else:
        a, p = rng.choice([200, 250, 300, 400, 500]), rng.choice([10, 12, 15, 18, 20])
    r = 1 + sgn_ * p / 100 if kind != 'ball' else p / 100
    text = tmpl.format(country=pick(rng, ['Ghana', 'Peru', 'Malaysia', 'Portugal', 'Canada', 'Kenya', 'Chile']), a=a, p=p, who=name(rng), cur=c)
    return kind, text, step, unit.format(cur=c), a, r, p


@R.add('ch02-st2', ALL, (1, 5), 'short')
def geo_core(rng, slot):
    c, d = slot.c, slot.d
    if c == 'C1':
        a = rng.choice([2, 3, 4, 5, 6, 8, 10, 12, 16, 81, 64, 243])
        r = rng.choice([2, 3, -2, 0.5, 1.5, -3, 0.25] if a < 64 else [0.5, 1 / 3, -0.5, 0.25, 2])
        n = rng.randint(6, 12)
        un = a * r ** (n - 1)
        rs = {1 / 3: '1/3'}.get(r, m(_num(r)))
        seq = ', '.join(m(_num(a * r ** i)) for i in range(4))
        if d <= 1:
            return nmcq(rng, f'Find the common ratio of the geometric sequence {seq}, …', r, [1 / r if r not in (0, 1) else 2, -r, a * r - a],
                        f'r = u₂ ÷ u₁ = {rs}.', fmtf=lambda z: m(_num(z)))
        return ret(f'For the geometric sequence {seq}, … write down the common ratio and find u{n}.', f'r = {rs}, u{n} = {m(sf(un, 4) if abs(un) >= 1e4 or not float(un).is_integer() else _num(un))}',
                   f'r = {rs} (A1); u{n} = {a} × ({rs}){sup(n - 1)} (M1) = {m(sf(un))} (A1).', 3 if d >= 2 else 2)
    kind, text, step, unit, a, r, p = _geo_ctx(rng, d)
    n = rng.randint(5, 15)
    first = 'u₁' if kind != 'ball' else 'the height of the first bounce'
    if kind == 'ball':
        a1 = a * r
        un = a1 * r ** (n - 1)
    else:
        a1 = a
        un = a * r ** (n - 1) if kind not in ('pop', 'bact') else a * r ** n
    if c == 'C2':
        if rng.random() < 0.5:
            return ret(f'{text} Explain why the values form a geometric sequence and state the common ratio.', f'r = {_num(r)}',
                       f'R1 each value is the same percentage ({p}%) {"of" if kind == "ball" else "more/less than"} the previous one, i.e. multiplied by a constant; A1 r = {_num(r)}.', 2, 'explain')
        wr = (1 + p / 100) if r < 1 and kind != 'ball' else p / 100
        return ret(f'{text} {name(rng)} uses a common ratio of {_num(wr)} to model this situation. Explain whether this is correct.', f'No; r = {_num(r)}',
                   f'R1 {"a decrease of " + str(p) + "% leaves " + str(100 - p) + "% of the value" if r < 1 and kind != "ball" else ("each height is " + str(p) + "% of the previous height, so the multiplier is " + _num(r)) if kind == "ball" else "an increase of " + str(p) + "% means 100% + " + str(p) + "%"}; A1 r = {_num(r)}.',
                   2, 'explain', gap='G2')
    if c == 'C3':
        if kind in ('pop', 'bact'):
            return ret(f'{text} Find the {"population" if kind == "pop" else "number of cells"} after {n} {step}s, and the least number of complete {step}s after which it exceeds {sf(a * 2.5, 2)}.',
                       f'{sf(un)}; {math.floor(math.log(2.5) / math.log(r)) + 1} {step}s',
                       f'{a} × {_num(r)}{sup(n)} (M1) = {sf(un)} (A1); solve {a} × {_num(r)}ⁿ > {sf(a * 2.5, 2)} (M1) → n = {sf(math.log(2.5) / math.log(r), 3)}, so {math.floor(math.log(2.5) / math.log(r)) + 1} {step}s (A1).',
                       4, 'numerical')
        Sn = a1 * (r ** n - 1) / (r - 1)
        return ret(f'{text} (a) Find the value for {step} {n}. (b) Find the total over the first {n} {step}s.' if kind != 'ball' else
                   f'{text} (a) Find the height reached after the {n}th bounce. (b) Find the sum of the heights of the first {n} bounces.',
                   f'(a) {sf(un)} {unit} (b) {sf(Sn)} {unit}',
                   f'(a) u{n} = {sf(a1, 4)} × {_num(r)}{sup(n - 1)} (M1) = {sf(un)} (A1). (b) S{n} = {sf(a1, 4)}({_num(r)}{sup(n)} − 1)/({_num(r)} − 1) (M1) = {sf(Sn)} (A1).',
                   4 if d >= 3 else 3, 'numerical')
    # C4: compare with an arithmetic alternative
    c_ = curm(rng)
    s0 = rng.randint(35, 70) * 1000
    inc = rng.randint(15, 30) * 100
    pc = max(1.5, round(rng.uniform(0.55, 0.85) * inc / s0 * 100, 1))
    if s0 * pc / 100 >= inc:
        return None
    rr = 1 + pc / 100
    k = 1
    while s0 * rr ** (k - 1) <= s0 + (k - 1) * inc:
        k += 1
        if k > 200:
            return None
    yrs = rng.randint(8, 15)
    SA = yrs / 2 * (2 * s0 + (yrs - 1) * inc)
    SB = s0 * (rr ** yrs - 1) / (rr - 1)
    who = name(rng)
    return ret(f'{who} is offered two salary schemes, each starting at {s0} {c_} per year. Scheme A increases by {inc} {c_} each year; scheme B increases by {pc}% each year. '
               f'(a) Find the salary in year {yrs} under each scheme. (b) Find the total earned over {yrs} years under each scheme. (c) Find the first year in which scheme B pays more than scheme A, '
               f'and advise {who}, giving a reason.',
               f'(a) A {money(s0 + (yrs - 1) * inc)}, B {money(s0 * rr ** (yrs - 1))} (b) A {money(SA)}, B {money(SB)} (c) year {k}',
               f'(a) {s0} + {yrs - 1}({inc}) (M1 A1); {s0}({_num(rr)}){sup(yrs - 1)} (M1 A1). (b) Sₙ arithmetic = {money(SA)} (A1); geometric = {money(SB)} (A1). '
               f'(c) compare terms (GDC table) (M1): year {k} (A1); R1 choice depends on how long {who} expects to stay – B is better for a long career{" and already pays more in total" if SB > SA else ""}.',
               9 if d >= 5 else 8, 'multi_step', gap='G5')


R.facts('ch02-st3', F(
    terms=[('convergent series', 'an infinite series whose partial sums approach a finite limit'),
           ('sum to infinity', 'S∞ = u₁/(1 − r), the limit of Sₙ for a geometric series with |r| < 1')],
    facts=[('For which value of r does the geometric series with u₁ = 5 have a sum to infinity?', '−0.6', ['1.2', '−1', '2'], 'S∞ exists only when |r| < 1.'),
           ('What is the sum to infinity of 8 + 4 + 2 + 1 + …?', '16', ['15', '8', 'It does not exist'], 'S∞ = 8/(1 − 0.5) = 16.'),
           ('What happens to rⁿ as n → ∞ when |r| < 1?', 'It tends to 0', ['It tends to 1', 'It tends to infinity', 'It alternates between 1 and −1'], 'Repeated multiplication by a number of size less than 1 makes the result shrink towards 0.')],
    why=[('Explain why the formula S∞ = u₁/(1 − r) cannot be used when r = 1.5.', 'For |r| ≥ 1 the terms do not shrink, so the partial sums grow without limit (diverge); the formula only applies when |r| < 1.'),
         ('Explain how the formula S∞ = u₁/(1 − r) follows from Sₙ = u₁(1 − rⁿ)/(1 − r).', 'When |r| < 1, rⁿ → 0 as n → ∞, so Sₙ → u₁(1 − 0)/(1 − r).'),
         ('Explain why a bouncing ball model with a sum to infinity is only an approximation of reality.', 'The model predicts infinitely many bounces in a finite total distance; in reality the ball stops after a finite number of bounces because of energy loss and the ball\'s size.')],
    misc=[('Because the series 1 + 0.9 + 0.81 + … has infinitely many terms, its sum must be infinite.', 'Infinitely many terms can have a finite sum when they shrink fast enough: r = 0.9 gives S∞ = 1/(1 − 0.9) = 10.'),
          ('The series 4 − 2 + 1 − 0.5 + … has no sum to infinity because the terms change sign.', 'r = −0.5 and |r| < 1, so S∞ = 4/(1 + 0.5) = 8/3.')],
))


@R.add('ch02-st3', ALL, (1, 5), 'short')
def inf_core(rng, slot):
    c, d = slot.c, slot.d
    a = rng.choice([3, 4, 5, 6, 8, 9, 10, 12, 15, 18, 20, 24, 27, 30, 40, 48, 60, 64, 81, 100])
    r = rng.choice([0.5, 0.25, 0.2, 0.4, 0.6, 0.75, 0.8, 0.9, -0.5, -0.25, -0.4, 0.3, 0.1])
    S = a / (1 - r)
    seq = ', '.join(m(_num(a * r ** i)) for i in range(3))
    if c == 'C1':
        if d <= 1:
            return nmcq(rng, f'Find the sum to infinity of the geometric series {seq.replace(", ", " + ")} + …', S, [a / (1 + r), a / r, a * (1 - r)],
                        f'S∞ = {a}/(1 − ({m(r)})) = {m(sf(S))}.', fmtf=lambda z: m(sf(z)))
        return ret(f'A geometric series has first term {a} and common ratio {m(r)}. Explain why the series has a sum to infinity and find it.', m(sf(S)),
                   f'R1 |r| = {abs(r)} < 1; S∞ = {a}/(1 − ({m(r)})) (M1) = {m(sf(S))} (A1).', 3)
    if c == 'C2':
        r2 = rng.choice([1.2, 1.5, -1.1, 2, -2])
        if rng.random() < 0.5:
            return ret(f'{name(rng)} uses S∞ = u₁/(1 − r) with u₁ = {a} and r = {m(r2)} to claim the series has sum {m(sf(a / (1 - r2)))}. Explain why this is incorrect.',
                       'The series diverges; no sum to infinity', f'R1 |r| = {abs(r2)} ≥ 1, so rⁿ does not tend to 0; R1 the partial sums {"grow without bound" if r2 > 0 else "oscillate with growing size"}, so S∞ does not exist.', 2, 'explain', gap='G2')
        n = rng.randint(4, 9)
        Sn = a * (1 - r ** n) / (1 - r)
        return ret(f'For the series {seq.replace(", ", " + ")} + …, compare S{n} with S∞ and explain why the difference becomes smaller as n increases.',
                   f'S{n} = {m(sf(Sn))}, S∞ = {m(sf(S))}', f'S{n} = {m(sf(Sn))} (A1); S∞ = {m(sf(S))} (A1); R1 S∞ − Sₙ = u₁rⁿ/(1 − r) and rⁿ → 0.', 3, 'explain')
    if c == 'C3':
        v = rng.random()
        if v < 0.4:
            h = rng.choice([2, 2.5, 3, 4, 5, 6])
            p = rng.choice([0.5, 0.6, 0.64, 0.7, 0.75, 0.8])
            total = h + 2 * h * p / (1 - p)
            return ret(f'A ball is dropped from a height of {h} m and each time it bounces it rises to {int(p * 100)}% of the height from which it fell. Assuming it bounces indefinitely, find the total vertical distance travelled.',
                       f'{sf(total)} m', f'Down {h} m, then up-and-down 2 × ({h} × {p}) + 2 × ({h} × {p}²) + … (M1); S∞ = {sf(h * p)}/(1 − {p}) (M1); total = {h} + 2 × {sf(h * p / (1 - p))} = {sf(total)} m (A1).', 4, 'numerical')
        if v < 0.7:
            dig = rng.randint(1, 98)
            frac_s = f'0.{dig:02d}{dig:02d}{dig:02d}…'
            from fractions import Fraction
            fr = Fraction(dig, 99)
            return ret(f'Write the recurring decimal {frac_s} as an infinite geometric series and hence express it as a fraction in its simplest form.', f'{fr.numerator}/{fr.denominator}',
                       f'{dig / 100:g} + {dig / 10000:g} + … with u₁ = {dig / 100:g}, r = 0.01 (M1 A1); S∞ = {dig / 100:g}/0.99 = {fr.numerator}/{fr.denominator} (A1).', 3, 'numerical')
        dose = rng.choice([100, 200, 250, 400, 500])
        keep = rng.choice([0.2, 0.25, 0.3, 0.4, 0.5])
        lim = dose / (1 - keep)
        return ret(f'A patient takes {dose} mg of a medicine every 12 hours. Just before each new dose {int(keep * 100)}% of the previous amount remains in the body. Find the long-term amount in the body immediately after a dose.',
                   f'{sf(lim)} mg', f'Amount after nth dose = {dose}(1 + {keep} + {keep}² + … ) (M1); S∞ = {dose}/(1 − {keep}) (M1) = {sf(lim)} mg (A1).', 3, 'numerical')
    # C4
    rr = rng.choice([0.6, 0.7, 0.75, 0.8, 0.85, 0.9])
    a = rng.choice([20, 24, 30, 36, 40, 45, 50, 60])
    S = a / (1 - rr)
    pct = rng.choice([1, 2, 5])
    n = 1
    while S - a * (1 - rr ** n) / (1 - rr) >= pct / 100 * S:
        n += 1
    return ret(f'The sum to infinity of a geometric series is {sf(S)} and its first term is {a}. (a) Find the common ratio. (b) Find the least number of terms for which Sₙ is within {pct}% of S∞. '
               f'(c) Explain why a sum to infinity exists for this series.',
               f'(a) r = {rr} (b) n = {n} (c) |r| < 1', f'(a) {a}/(1 − r) = {sf(S)} (M1) → r = {rr} (A1). (b) S∞ − Sₙ < {pct / 100} × {sf(S)}, i.e. {sf(S)} × {rr}ⁿ < {sf(pct / 100 * S)} (M1) (GDC or logs) n = {n} (A1 A1). '
               f'(c) R1 |{rr}| < 1 so rⁿ → 0.', 6, 'multi_step', gap='G5')


R.facts('ch02-st4', F(
    terms=[('simple interest', 'interest calculated only on the original principal, I = Prn/100, so the value grows by a constant amount each year'),
           ('compound interest', 'interest calculated on the principal plus all interest already earned, so the value grows by a constant percentage each period')],
    facts=[('Which type of sequence models the value of an investment earning simple interest?', 'arithmetic', ['geometric', 'quadratic', 'exponential decay'], 'The same amount of interest is added each year.'),
           ('Which type of sequence models the value of an investment earning compound interest at a fixed rate?', 'geometric', ['arithmetic', 'linear', 'constant'], 'The value is multiplied by the same factor each period.')],
    why=[('Explain why compound interest eventually exceeds simple interest at the same annual rate.', 'Compound interest earns interest on previous interest, so the yearly increase itself grows; simple interest adds a constant amount, so the geometric growth overtakes the linear growth.'),
         ('Explain why simple and compound interest give the same value after exactly one year with annual compounding.', 'In the first year both calculate interest only on the principal: P(1 + r/100) = P + Pr/100.')],
    misc=[('At 5% simple interest a sum doubles in about 14 years, the same as with 5% compound interest.', 'Simple interest needs 20 years (100% ÷ 5%); compound interest at 5% doubles in log 2/log 1.05 ≈ 14.2 years.')],
))


@R.add('ch02-st4', ALL, (1, 5), 'short')
def simple_vs_compound(rng, slot):
    c, d = slot.c, slot.d
    P = rng.randint(10, 200) * 100
    r = round(rng.uniform(1.5, 7.5), 1)
    n = rng.randint(3, 15)
    cc = cur(rng)
    who = name(rng)
    SI = P * r * n / 100
    CI = P * (1 + r / 100) ** n
    if c == 'C1':
        if d <= 1:
            return nmcq(rng, f'{who} invests {P} {cc} at {r}% simple interest per year. How much interest is earned in {n} years?', SI,
                        [P * (1 + r / 100) ** n - P, P * r / 100, P + SI], f'I = Prn/100 = {P} × {r} × {n} ÷ 100 = {money(SI)}.', fmtf=money)
        return ret(f'{who} invests {P} {cc} at a simple interest rate of {r}% per annum. Write down the value of the investment after one year and after {n} years.',
                   f'{money(P * (1 + r / 100))} {cc}; {money(P + SI)} {cc}', f'{money(P * (1 + r / 100))} (A1); {P} + {P} × {r} × {n}/100 (M1) = {money(P + SI)} (A1).', 3)
    if c == 'C2':
        return ret(f'{who} invests {P} {cc} at {r}% per annum. Show that the yearly values form an arithmetic sequence under simple interest and a geometric sequence under annual compound interest, stating d and r in each case.',
                   f'd = {money(P * r / 100)}; ratio = {1 + r / 100:g}', f'Simple: value increases by {P} × {r}/100 = {money(P * r / 100)} each year (constant difference) (R1 A1). Compound: value multiplied by {1 + r / 100:g} each year (constant ratio) (R1 A1).',
                   4, 'explain')
    if c == 'C3':
        return ret(f'{P} {cc} is invested for {n} years at {r}% per annum. Calculate the value of the investment if interest is (a) simple; (b) compounded annually. Give answers to 2 decimal places.',
                   f'(a) {money(P + SI)} (b) {money(CI)}', f'(a) {P} + {P}×{r}×{n}/100 (M1) = {money(P + SI)} (A1). (b) {P}(1 + {r}/100){sup(n)} (M1) = {money(CI)} (A1).', 4, 'numerical')
    rs = round(r + rng.uniform(0.5, 2.5), 1)
    k = 1
    while P * (1 + r / 100) ** k <= P * (1 + rs * k / 100):
        k += 1
        if k > 400:
            return None
    return ret(f'Account A pays {rs}% simple interest per annum and account B pays {r}% interest compounded annually. {who} deposits {P} {cc} in each. '
               f'(a) Write down expressions for the value of each account after n years. (b) Find the number of complete years after which account B is first worth more than account A. (c) Comment on which account is better for a {n}-year saving plan.',
               f'(a) A = {P}(1 + {rs}n/100), B = {P}({1 + r / 100:g})ⁿ (b) {k} years (c) {"A" if k > n else "B"} is better over {n} years',
               f'(a) A1 A1. (b) GDC table/graph or solve {P}({1 + r / 100:g})ⁿ > {P}(1 + {rs / 100:g}n) (M1); n = {k} (A1). (c) after {n} years A = {money(P * (1 + rs * n / 100))}, B = {money(P * (1 + r / 100) ** n)} (M1); R1 {"A" if k > n else "B"} gives more.',
               7, 'multi_step', gap='G5')


# =============================================================================================
# ch03 Financial mathematics
# =============================================================================================
KN = {1: 'annually', 2: 'half-yearly', 4: 'quarterly', 12: 'monthly'}


def fv(pv, r, n, k=1):
    return pv * (1 + r / (100 * k)) ** (k * n)


def pmt(pv, r, n, k=12):
    i = r / (100 * k)
    N = int(round(n * k))
    return pv * i / (1 - (1 + i) ** -N)


def balance(pv, r, k, P, j):
    i = r / (100 * k)
    return pv * (1 + i) ** j - P * ((1 + i) ** j - 1) / i


def tvm_line(N, I, PV, PMT, FV, PY):
    return f'N = {N}, I% = {I}, PV = {PV}, PMT = {PMT}, FV = {FV}, P/Y = {PY}, C/Y = {PY}'


R.facts('ch03-st1', F(
    terms=[('compound interest', 'interest added to the principal at the end of each compounding period, so later interest is earned on earlier interest: FV = PV(1 + r/(100k))^(kn)'),
           ('depreciation', 'the decrease in value of an asset over time, modelled at a fixed annual rate r% by V = V₀(1 − r/100)ⁿ'),
           ('present value (PV)', 'the amount invested or borrowed now; in a TVM solver it is entered with the opposite sign to money received'),
           ('compounding period', 'the interval (year, half-year, quarter, month) at the end of which interest is added; k periods per year')],
    facts=[('On a GDC TVM solver, why is PV usually entered as a negative number for an investment?', 'Money paid out by the investor is negative and money received is positive', ['The interest rate is negative', 'The solver only accepts negative numbers', 'Because the value decreases over time'], 'The TVM solver uses a cash-flow sign convention.'),
           ('Which expression gives the value of 4000 invested for 5 years at 3% per annum compounded monthly?', '4000(1 + 0.03/12)⁶⁰', ['4000(1.03)⁶⁰', '4000(1 + 0.03/12)⁵', '4000(1 + 0.36)⁵'], 'k = 12, so the rate per period is 3%/12 and there are 12 × 5 = 60 periods.'),
           ('A laptop depreciates by 20% per year. What fraction of its value remains after 2 years?', '64%', ['60%', '40%', '36%'], '0.8² = 0.64.')],
    why=[('Explain why compounding monthly gives a larger final value than compounding annually at the same nominal annual rate.', 'Interest is added sooner, so each month\'s interest itself earns interest for the rest of the year; the effective annual rate (1 + r/1200)¹² − 1 exceeds r/100.'),
         ('Explain why a depreciation model V = V₀(0.85)ⁿ never reaches zero, and whether this is realistic.', 'Multiplying by 0.85 always leaves a positive amount, so V → 0 but never equals 0; in reality an asset may be scrapped or have a residual value, so the model is only reasonable for a limited time.')],
    misc=[('A car that depreciates by 10% per year loses 50% of its value in 5 years.', 'Depreciation compounds: 0.9⁵ = 0.590, so it loses 41.0%, not 50%.'),
          ('Interest of 6% per annum compounded monthly means 6% is added every month.', 'The nominal annual rate is shared between the periods: 6% ÷ 12 = 0.5% per month.')],
))


@R.add('ch03-st1', ALL, (1, 5), 'short')
def tvm_core(rng, slot):
    c, d = slot.c, slot.d
    P = rng.randint(20, 400) * 100
    r = round(rng.uniform(1.5, 7.8), 1)
    k = pick(rng, [1, 2, 4, 12])
    n = rng.randint(3, 20)
    cc = cur(rng)
    who = name(rng)
    bank = pick(rng, ['a bank in Zürich', 'an online bank', 'a credit union in Toronto', 'a savings bank in Singapore', 'a building society in Leeds', 'a bank in Melbourne'])
    F_ = fv(P, r, n, k)
    if c == 'C1':
        if d <= 1:
            return nmcq(rng, f'{who} invests {P} {cc} for {n} years at {r}% per annum compounded {KN[k]}. Find the value of the investment, to the nearest {cc}.', round(F_),
                        [round(P * (1 + r / 100 * n)), round(fv(P, r, n * k, 1)), round(fv(P, r, n, 1)) if k > 1 else round(fv(P, r, n, 12))],
                        f'FV = {P}(1 + {r}/{100 * k}){sup(k * n)} = {round(F_)}.', fmtf=lambda z: f'{int(z)} {cc}')
        return ret(f'{who} invests {P} {cc} with {bank} at {r}% per annum compounded {KN[k]}. Write down the values of N, I% and P/Y you would enter in a TVM solver to find the value after {n} years, and find this value.',
                   f'N = {n * k if k > 1 else n}, I% = {r}, P/Y = {k}; FV = {money(F_)} {cc}',
                   f'N = {k * n} (A1), I% = {r}, P/Y = C/Y = {k} (A1); FV = {money(F_)} (A1).' if k > 1 else f'N = {n} (A1), I% = {r}, P/Y = C/Y = 1 (A1); FV = {money(F_)} (A1).', 3)
    if c == 'C2':
        Fa = fv(P, r, n, 1)
        Fm = fv(P, r, n, 12)
        if rng.random() < 0.5:
            return ret(f'{P} {cc} is invested for {n} years at a nominal rate of {r}% per annum. Compare the final values when interest is compounded annually and monthly, and explain the difference.',
                       f'annual {money(Fa)}, monthly {money(Fm)}', f'Annual: {money(Fa)} (A1); monthly: {money(Fm)} (A1); R1 with monthly compounding interest is added earlier and itself earns interest (effective rate {sf(((1 + r / 1200) ** 12 - 1) * 100)}% > {r}%).',
                       3, 'explain')
        dep = rng.choice([8, 10, 12, 15, 18, 20, 25])
        yrs = rng.randint(3, 7)
        lost = (1 - (1 - dep / 100) ** yrs) * 100
        return ret(f'{who} says a machine that depreciates at {dep}% per year will have lost {dep * yrs}% of its value after {yrs} years. Explain why this is incorrect and find the actual percentage lost.',
                   f'{sf(lost)}%', f'R1 each year\'s depreciation is {dep}% of a smaller value, so the losses are not additive; M1 1 − {1 - dep / 100:g}{sup(yrs)}; A1 {sf(lost)}%.', 3, 'explain', gap='G2')
    if c == 'C3':
        v = rng.randint(0, 2)
        if v == 0:
            return ret(f'{who} deposits {P} {cc} with {bank} at {r}% per annum compounded {KN[k]}. Find the value of the deposit after {n} years, correct to 2 decimal places.', f'{money(F_)} {cc}',
                       f'FV = {P}(1 + {r}/({100} × {k})){sup(k * n)} (M1)(A1) = {money(F_)} (A1). TVM: {tvm_line(k * n, r, -P, 0, "?", k)}.', 3, 'numerical')
        if v == 1:
            target = round(P * rng.uniform(1.4, 2.6), -2)
            nn = math.log(target / P) / (k * math.log(1 + r / (100 * k)))
            yrs = math.ceil(nn)
            return ret(f'{who} invests {P} {cc} at {r}% per annum compounded {KN[k]}. Find the number of complete years needed for the investment to first exceed {int(target)} {cc}.',
                       f'{yrs} years', f'{P}(1 + {r}/{100 * k}){sup("12n" if k == 12 else (str(k) + "n") if k > 1 else "n")} > {int(target)} (M1); n = {sf(nn)} (A1); {yrs} complete years (A1).', 3, 'numerical')
        target = round(P * rng.uniform(1.3, 2.4), -2)
        rr = 100 * k * ((target / P) ** (1 / (k * n)) - 1)
        return ret(f'{who} wants {P} {cc} to grow to {int(target)} {cc} in {n} years, with interest compounded {KN[k]}. Find the minimum annual interest rate needed.',
                   f'{sf(rr)}%', f'{P}(1 + r/{100 * k}){sup(k * n)} = {int(target)} (M1)(A1); r = {sf(rr)}% (A1). TVM: N = {k * n}, PV = −{P}, FV = {int(target)}, solve I%.', 3, 'numerical')
    # C4: two accounts
    r2 = round(r + rng.uniform(-0.6, -0.1), 2)
    k2 = 12 if k != 12 else 1
    if k2 == 1:
        r2 = round(r + rng.uniform(0.05, 0.4), 2)
    F2 = fv(P, r2, n, k2)
    best = 'A' if F_ > F2 else 'B'
    target = round(P * 2, -2)
    nn = math.log(2) / (k * math.log(1 + r / (100 * k)))
    return ret(f'{who} has {P} {cc} to invest for {n} years. Account A pays {r}% per annum compounded {KN[k]}; account B pays {r2}% per annum compounded {KN[k2]}. '
               f'(a) Find the value of each account after {n} years. (b) State which account {who} should choose, giving a reason. (c) Find the time, to the nearest year, for the money to double in account A. '
               f'(d) Explain why the answer to (c) does not depend on the amount invested.',
               f'(a) A {money(F_)}, B {money(F2)} (b) {best} (c) {round(nn)} years (d) PV cancels',
               f'(a) {P}(1 + {r}/{100 * k}){sup(k * n)} = {money(F_)} (M1 A1); {P}(1 + {r2}/{100 * k2}){sup(k2 * n)} = {money(F2)} (M1 A1). (b) {best} gives the larger final value (R1). '
               f'(c) (1 + {r}/{100 * k}){sup(str(k) + "n" if k > 1 else "n")} = 2 (M1), n = {sf(nn)} ≈ {round(nn)} years (A1). (d) R1 dividing PV(1 + i)ᴺ = 2PV by PV removes PV.',
               9 if d >= 5 else 8, 'multi_step', gap='G5')


@R.add('ch03-st1', ('C2', 'C3', 'C4'), (1, 5), 'short')
def depreciation(rng, slot):
    item, v0 = pick(rng, [('a delivery van', rng.randint(25, 60) * 1000), ('a laptop', rng.randint(9, 30) * 100), ('an electric car', rng.randint(30, 80) * 1000),
                          ('a tractor', rng.randint(60, 150) * 1000), ('a 3D printer', rng.randint(15, 60) * 100), ('a fishing boat', rng.randint(40, 120) * 1000)])
    dep = round(rng.uniform(8, 28), 1)
    n = rng.randint(3, 9)
    cc = cur(rng)
    v = v0 * (1 - dep / 100) ** n
    if slot.c == 'C2':
        return ret(f'{item[0].upper() + item[1:]} bought for {v0} {cc} depreciates at {dep}% per year. Explain why the value after n years is given by {v0}({1 - dep / 100:g})ⁿ and interpret the number {1 - dep / 100:g}.',
                   f'Each year the value is multiplied by {1 - dep / 100:g}', f'R1 losing {dep}% leaves {100 - dep:g}% of the previous value each year; R1 repeated multiplication by {1 - dep / 100:g} gives the power n; {1 - dep / 100:g} is the proportion of value kept each year (A1).',
                   3, 'explain')
    if slot.c == 'C3':
        return ret(f'{item[0].upper() + item[1:]} is bought for {v0} {cc} and depreciates at {dep}% per annum. Find its value after {n} years.', f'{money(v)} {cc}',
                   f'{v0}(1 − {dep}/100){sup(n)} (M1)(A1) = {money(v)} (A1). TVM: N = {n}, I% = −{dep}, PV = −{v0}.', 3, 'numerical')
    half = math.log(0.5) / math.log(1 - dep / 100)
    sc = round(v0 * rng.uniform(0.15, 0.3), -2)
    ns = math.log(sc / v0) / math.log(1 - dep / 100)
    return ret(f'A company buys {item} for {v0} {cc}; it depreciates at {dep}% per annum. (a) Find its value after {n} years. (b) Find the total depreciation over these {n} years as a percentage of the original price. '
               f'(c) The company replaces the item when its value falls below {int(sc)} {cc}. Find after how many complete years this first happens.',
               f'(a) {money(v)} (b) {sf((1 - v / v0) * 100)}% (c) {math.ceil(ns)} years',
               f'(a) {v0}({1 - dep / 100:g}){sup(n)} (M1) = {money(v)} (A1). (b) ({v0} − {money(v)}) ÷ {v0} × 100 (M1) = {sf((1 - v / v0) * 100)}% (A1). '
               f'(c) {v0}({1 - dep / 100:g})ⁿ < {int(sc)} (M1); n = {sf(ns)} (A1) → {math.ceil(ns)} years (A1).', 7, 'multi_step', gap='G5')


R.facts('ch03-st2', F(
    terms=[('inflation', 'a general rise in prices over time, which reduces the purchasing power of money'),
           ('real value', 'the value of an amount of money measured in terms of what it can buy at a reference date, i.e. adjusted for inflation'),
           ('real interest rate', 'the growth in purchasing power of an investment; approximately the nominal interest rate minus the inflation rate')],
    facts=[('The inflation rate is 3% per year. Which expression gives the value today of 1000 USD received in 4 years?', '1000 ÷ 1.03⁴', ['1000 × 1.03⁴', '1000 × 0.97⁴', '1000 − 4 × 30'], 'Divide by the inflation factor for each year.'),
           ('An account pays 2% interest while inflation is 3%. What happens to the real value of the savings?', 'It decreases', ['It increases', 'It stays the same', 'It doubles'], 'Prices rise faster than the balance, so purchasing power falls.'),
           ('In the IB approach to a TVM solver with inflation, what is entered for I%?', 'the interest rate minus the inflation rate', ['the interest rate plus the inflation rate', 'the inflation rate only', 'the interest rate times the inflation rate'], 'I% = r − i gives the approximate real growth.')],
    why=[('Explain why a salary rise of 2% when inflation is 4% is a fall in real income.', 'Prices rise by 4% while pay rises by 2%, so the same salary buys about 2% less than before; the real value of the salary falls.'),
         ('Explain why using I% = r − i in a TVM solver gives only an approximate real value.', 'The exact real growth factor is (1 + r)/(1 + i), so the real rate is (r − i)/(1 + i), slightly less than r − i; the approximation is close when rates are small.')],
    misc=[('If inflation is 0%, prices must be falling.', 'Inflation of 0% means prices are, on average, unchanged; falling prices are deflation (negative inflation).')],
))


@R.add('ch03-st2', ALL, (1, 5), 'short')
def inflation_core(rng, slot):
    c, d = slot.c, slot.d
    inf = round(rng.uniform(1.5, 6.5), 1)
    n = rng.randint(3, 15)
    cc = cur(rng)
    who = name(rng)
    if c == 'C1':
        price = round(rng.uniform(2, 90), 2)
        item = pick(rng, ['a cinema ticket', 'a kilogram of coffee', 'a train fare', 'a school textbook', 'a litre of olive oil', 'a pair of trainers'])
        future = price * (1 + inf / 100) ** n
        if d <= 1:
            return nmcq(rng, f'{item[0].upper() + item[1:]} costs {price:.2f} {cc}. If prices rise with inflation of {inf}% per year, find the expected price in {n} years.', future,
                        [price * (1 + inf * n / 100), price / (1 + inf / 100) ** n, price * (1 + inf / 100) ** (n - 1)], f'{price:.2f} × {1 + inf / 100:g}{sup(n)} = {money(future)}.', fmtf=lambda z: f'{money(z)} {cc}')
        return ret(f'{item[0].upper() + item[1:]} costs {price:.2f} {cc} today. Assuming a constant inflation rate of {inf}% per annum, find its price in {n} years.', f'{money(future)} {cc}',
                   f'{price:.2f}(1 + {inf}/100){sup(n)} (M1) = {money(future)} (A1).', 2)
    if c == 'C2':
        rise = round(inf - rng.uniform(0.5, 2.5), 1)
        sal = rng.randint(30, 90) * 1000
        real = sal * (1 + rise / 100) / (1 + inf / 100)
        return ret(f'{who}\'s salary of {sal} {cc} rises by {rise}% while inflation over the same year is {inf}%. Explain, with a calculation, what happens to the real value of {who}\'s salary.',
                   f'Falls: real value ≈ {money(real)} {cc} in last year\'s money', f'New salary {money(sal * (1 + rise / 100))} (A1); in last year\'s prices {money(sal * (1 + rise / 100))} ÷ {1 + inf / 100:g} = {money(real)} (M1 A1); R1 this is less than {sal}, so purchasing power falls.',
                   4, 'explain')
    P = rng.randint(20, 300) * 100
    r = round(inf + rng.choice([-1, 1, 1, 1]) * rng.uniform(0.4, 3.0), 1)
    if abs(r - inf) < 0.3 or r <= 0.5:
        return None
    k = pick(rng, [1, 4, 12])
    nom = fv(P, r, n, k)
    real = nom / (1 + inf / 100) ** n
    approx = fv(P, r - inf, n, k)
    if c == 'C3':
        return ret(f'{who} invests {P} {cc} at {r}% per annum compounded {KN[k]}. Inflation is expected to be {inf}% per year. (a) Find the value of the investment after {n} years. '
                   f'(b) Find the real value of this amount in today\'s money, by adjusting for inflation.',
                   f'(a) {money(nom)} (b) {money(real)}', f'(a) {P}(1 + {r}/{100 * k}){sup(k * n)} (M1) = {money(nom)} (A1). (b) {money(nom)} ÷ {1 + inf / 100:g}{sup(n)} (M1) = {money(real)} (A1). '
                   f'Also accept the IB approximation using I% = {r} − {inf} = {r - inf:.1f}: {money(approx)}.', 4, 'numerical')
    goal = round(P * rng.uniform(1.1, 1.5), -2)
    # nominal annual rate (compounded k) needed so that real value reaches goal
    need = 100 * k * (((goal / P) * (1 + inf / 100) ** n) ** (1 / (k * n)) - 1)
    return ret(f'{who} invests {P} {cc} for {n} years at {r}% per annum compounded {KN[k]}, with inflation of {inf}% per year. (a) Find the real value of the investment after {n} years. '
               f'(b) Determine whether the investment has kept pace with inflation. (c) Find the minimum nominal annual rate (compounded {KN[k]}) that would give a real value of {int(goal)} {cc} after {n} years.',
               f'(a) {money(real)} (b) {"yes" if real > P else "no"} (c) {sf(need)}%',
               f'(a) nominal {money(nom)} (M1 A1); real = {money(nom)} ÷ {1 + inf / 100:g}{sup(n)} = {money(real)} (M1 A1). (b) R1 compare with {P}: {"real value has grown" if real > P else "real value has fallen"}. '
               f'(c) {P}(1 + x/{100 * k}){sup(k * n)} ÷ {1 + inf / 100:g}{sup(n)} = {int(goal)} (M1); x = {sf(need)}% (A1).', 7, 'multi_step', gap='G5')


R.facts('ch03-st3', F(
    terms=[('amortization', 'paying off a loan through regular equal payments, each covering the interest due and part of the outstanding principal'),
           ('annuity', 'a series of equal payments made at regular intervals, e.g. a pension paying a fixed amount each month'),
           ('outstanding balance', 'the amount of a loan still owed after a number of payments have been made')],
    facts=[('In a typical repayment loan, how do the interest and principal parts of each equal payment change over time?', 'The interest part decreases and the principal part increases', ['Both stay the same', 'The interest part increases', 'The principal part decreases'], 'Interest is charged on a shrinking balance.'),
           ('For a loan, which TVM entry is zero when the loan is fully repaid?', 'FV', ['PV', 'PMT', 'N'], 'Nothing remains at the end, so FV = 0.'),
           ('A loan of 12 000 is repaid monthly at 6% per annum. What is the interest in the first month?', '60', ['720', '600', '6'], '12 000 × 0.06/12 = 60.')],
    why=[('Explain why the interest part of each repayment decreases over the term of a loan.', 'Interest each period is charged on the outstanding balance; each payment reduces the balance, so subsequent interest charges are smaller and more of each fixed payment repays principal.'),
         ('Explain why a longer loan term reduces the monthly payment but increases the total interest paid.', 'The principal is spread over more payments, so each is smaller; but the balance stays high for longer, so more interest accrues in total.')],
    misc=[('A loan of 10 000 at 5% per annum for 4 years costs 10 000 × 0.05 × 4 = 2000 in interest.', 'That is simple interest on the full amount; with an amortized loan, interest is charged on the falling balance, so the total interest is less (≈ 1054 with monthly payments).')],
))


@R.add('ch03-st3', ALL, (1, 5), 'short')
def loan_core(rng, slot):
    c, d = slot.c, slot.d
    what = pick(rng, [('a car loan', 8000, 45000), ('a student loan', 10000, 60000), ('a mortgage', 150000, 600000), ('a loan for solar panels', 5000, 20000),
                      ('a business loan', 20000, 120000), ('a loan for a motorbike', 3000, 15000)])
    pv = round(rng.uniform(what[1], what[2]), -2 if what[2] < 100000 else -3)
    r = round(rng.uniform(2.5, 9.5), 1)
    yrs = rng.choice([3, 4, 5, 6, 8, 10]) if what[0] != 'a mortgage' else rng.choice([15, 20, 25, 30])
    k = 12
    P = pmt(pv, r, yrs, k)
    cc = cur(rng)
    who = name(rng)
    tot = P * yrs * k
    if c == 'C1':
        i1 = pv * r / 1200
        if d <= 1:
            return nmcq(rng, f'{who} takes {what[0]} of {int(pv)} {cc} at {r}% per annum, repaid monthly. Find the interest charged in the first month.', i1,
                        [pv * r / 100, pv * r / 1200 * 12 / 10, pv * r / 1200 + P], f'{int(pv)} × {r}/1200 = {money(i1)}.', fmtf=lambda z: f'{money(z)} {cc}')
        return ret(f'{who} repays {what[0]} with monthly payments of {money(P)} {cc} for {yrs} years. Find the total amount repaid.', f'{money(tot)} {cc}',
                   f'{money(P)} × {yrs * 12} (M1) = {money(tot)} (A1).', 2)
    if c == 'C2':
        i1 = pv * r / 1200
        b1 = pv + i1 - P
        i2 = b1 * r / 1200
        return ret(f'{who} borrows {int(pv)} {cc} at {r}% per annum, repaid by monthly payments of {money(P)} {cc}. Calculate the interest included in the first and second payments and explain why they differ.',
                   f'{money(i1)} and {money(i2)}', f'First: {int(pv)} × {r}/1200 = {money(i1)} (A1); balance {money(b1)} (M1); second: {money(i2)} (A1); R1 the balance has fallen, so less interest is charged.',
                   4, 'explain')
    if c == 'C3':
        if rng.random() < 0.5:
            return ret(f'{who} takes out {what[0]} of {int(pv)} {cc} at {r}% per annum compounded monthly, to be repaid over {yrs} years with equal monthly payments. Find (a) the monthly payment; (b) the total interest paid.',
                       f'(a) {money(P)} (b) {money(tot - pv)}', f'(a) TVM: {tvm_line(yrs * 12, r, int(pv), "?", 0, 12)} (M1)(A1); PMT = {money(P)} (A1). (b) {yrs * 12} × {money(P)} − {int(pv)} (M1) = {money(tot - pv)} (A1).',
                       5 if d >= 3 else 4, 'numerical')
        dep = rng.randint(100, 1500)
        yrs2 = rng.randint(5, 30)
        r2 = round(rng.uniform(2, 6.5), 1)
        A = dep * ((1 + r2 / 1200) ** (12 * yrs2) - 1) / (r2 / 1200)
        return ret(f'{who} pays {dep} {cc} into a pension fund at the end of every month for {yrs2} years. The fund earns {r2}% per annum compounded monthly. Find the value of the fund at the end of this time, and the interest earned.',
                   f'{money(A)}; interest {money(A - dep * 12 * yrs2)}', f'TVM: N = {12 * yrs2}, I% = {r2}, PV = 0, PMT = −{dep}, P/Y = C/Y = 12 (M1)(A1); FV = {money(A)} (A1); interest = {money(A)} − {dep * 12 * yrs2} = {money(A - dep * 12 * yrs2)} (A1).',
                       4, 'numerical')
    j = rng.randint(1, yrs - 1) * 12
    B = balance(pv, r, 12, P, j)
    Pn = pmt(B, r + 1.0, (yrs * 12 - j) / 12, 12)
    return ret(f'{who} takes {what[0]} of {int(pv)} {cc} at {r}% per annum compounded monthly over {yrs} years, with equal monthly repayments. (a) Find the monthly repayment. (b) Find the amount still owed after {j // 12} years. '
               f'(c) At that point the interest rate rises to {r + 1:.1f}%. Find the new monthly repayment needed to clear the loan on time and the increase in the total cost of the loan.',
               f'(a) {money(P)} (b) {money(B)} (c) {money(Pn)}; extra {money((Pn - P) * (yrs * 12 - j))}',
               f'(a) TVM: {tvm_line(yrs * 12, r, int(pv), "?", 0, 12)} (M1) PMT = {money(P)} (A1). (b) N = {j}, PMT = −{money(P)}, solve FV (M1): {money(B)} (A1). '
               f'(c) N = {yrs * 12 - j}, I% = {r + 1:.1f}, PV = {money(B)} (M1): PMT = {money(Pn)} (A1); extra cost = ({money(Pn)} − {money(P)}) × {yrs * 12 - j} (M1) = {money((Pn - P) * (yrs * 12 - j))} (A1).',
               9 if d >= 5 else 8, 'multi_step', gap='G5')


@R.add('ch03-st3', ('C3', 'C4'), (2, 5), 'short')
def amort_table(rng, slot):
    pv = rng.randint(30, 200) * 100
    r = round(rng.uniform(3, 9), 1)
    n = rng.choice([2, 3, 4, 5])
    P = pmt(pv, r, n, 1)
    cc = cur(rng)
    rows = []
    b = pv
    for yr in range(1, 4):
        it = b * r / 100
        pr = P - it
        b2 = b - pr
        rows.append((yr, b, it, pr, b2))
        b = b2
    if slot.c == 'C3':
        y, b0, it, pr, b2 = rows[0]
        return ret(f'A loan of {pv} {cc} is repaid with {n} equal annual payments of {money(P)} {cc}, interest {r}% per annum. Complete the first row of the amortization table: balance at start, interest, principal repaid, balance at end.',
                   f'{pv}; {money(it)}; {money(pr)}; {money(b2)}', f'Interest = {pv} × {r/100:g} = {money(it)} (A1); principal = {money(P)} − {money(it)} = {money(pr)} (M1 A1); balance = {money(b2)} (A1).', 4, 'numerical')
    t = '; '.join(f'year {y}: interest {money(it)}, principal {money(pr)}, end balance {money(abs(b2))}' for y, b0, it, pr, b2 in rows[:min(n, 3)])
    return ret(f'A small business borrows {pv} {cc} at {r}% per annum, to be repaid in {n} equal annual instalments. (a) Show that each instalment is {money(P)} {cc}, to 2 d.p. (b) Construct the amortization table for the first {min(n, 3)} years. '
               f'(c) Explain how the table shows that interest is charged on the outstanding balance.',
               f'(a) {money(P)} (b) {t} (c) interest falls as the balance falls',
               f'(a) TVM N = {n}, I% = {r}, PV = {pv}, FV = 0 (M1) → PMT = {money(P)} (AG A1). (b) {t} (M1 A1 A1 per correct row, FT). (c) R1 each interest entry = {r}% of that year\'s starting balance.',
               8, 'multi_step', gap='G5')


R.facts('ch03-st4', F(
    terms=[('total cost of a loan', 'the sum of all repayments, i.e. monthly payment × number of payments (plus any fees)'),
           ('annual percentage rate (APR)', 'the yearly cost of borrowing including interest and fees, used to compare loan offers fairly')],
    why=[('Explain why the loan with the lowest monthly payment is not necessarily the cheapest loan.', 'A low monthly payment may come from a longer term; more payments are made and interest accumulates for longer, so the total repaid can be larger.'),
         ('Explain why fees as well as interest rates should be considered when comparing loans.', 'An arrangement fee adds to the total cost; a loan with a slightly lower rate but a large fee can cost more overall – the APR captures both.')],
    misc=[('A 0% finance offer is always cheaper than paying cash.', 'Not necessarily: 0% deals often carry a higher purchase price, fees or a lost cash discount; compare the total amount paid.')],
))


@R.add('ch03-st4', ALL, (1, 5), 'short')
def compare_loans(rng, slot):
    c, d = slot.c, slot.d
    item, lo, hi = pick(rng, [('a car', 150, 450), ('a kitchen renovation', 120, 400), ('a heat pump system', 80, 200), ('a delivery van', 250, 600),
                              ('a grand piano', 150, 500), ('a home extension', 300, 900), ('a family motorhome', 400, 900)])
    price = rng.randint(lo, hi) * 100
    cc = cur(rng)
    who = name(rng)
    r1, y1 = round(rng.uniform(3, 7), 1), rng.choice([3, 4, 5])
    r2, y2 = round(r1 - rng.uniform(0.3, 1.5), 1), y1 + rng.choice([2, 3])
    fee = rng.randint(2, 8) * 100
    P1, P2 = pmt(price, r1, y1), pmt(price, r2, y2)
    T1, T2 = P1 * 12 * y1, P2 * 12 * y2 + fee
    if c == 'C1':
        return ret(f'Loan offer for {item}: monthly payments of {money(P1)} {cc} for {y1} years. Find the total amount repaid.', f'{money(T1)} {cc}', f'{money(P1)} × {12 * y1} (M1) = {money(T1)} (A1).', 2)
    if c == 'C2':
        return ret(f'For {item} costing {price} {cc}, offer A is {r1}% per annum over {y1} years; offer B is {r2}% per annum over {y2} years with a {fee} {cc} fee. {who} chooses B "because the interest rate is lower". '
                   f'Explain why this reasoning is incomplete.', f'B costs {money(T2)} vs A {money(T1)} in total',
                   f'R1 the longer term and fee also affect cost; M1 totals A = {money(T1)}, B = {money(T2)} (A1); R1 {"B is still cheaper overall" if T2 < T1 else "A is actually cheaper overall"} although B has lower monthly payments.',
                   4, 'explain')
    if c == 'C3':
        return ret(f'{who} borrows {price} {cc} for {item}. Offer A: {r1}% per annum compounded monthly over {y1} years. Offer B: {r2}% per annum compounded monthly over {y2} years plus a fee of {fee} {cc}. '
                   f'Find the monthly payment and the total cost for each offer.', f'A: {money(P1)}, {money(T1)}; B: {money(P2)}, {money(T2)}',
                   f'A: TVM N = {12 * y1}, I% = {r1} → {money(P1)} (M1 A1), total {money(T1)} (A1). B: N = {12 * y2}, I% = {r2} → {money(P2)} (A1), total {money(P2 * 12 * y2)} + {fee} = {money(T2)} (A1).',
                   5, 'numerical')
    save = rng.randint(3, 9) * 100
    r3 = round(rng.uniform(2, 4.5), 1)
    nmonths = math.log(1 + price * (r3 / 1200) / save) / math.log(1 + r3 / 1200)
    return ret(f'{who} wants to buy {item} costing {price} {cc}. Option 1: a loan at {r1}% per annum compounded monthly over {y1} years. Option 2: save {save} {cc} at the end of each month in an account paying {r3}% per annum compounded monthly, and buy when the savings reach the price. '
               f'(a) Find the total cost of option 1. (b) Find how many months option 2 takes. (c) Find the amount actually paid in by {who} under option 2. (d) Discuss one advantage of each option, assuming the price stays the same.',
               f'(a) {money(T1)} (b) {math.ceil(nmonths)} months (c) {money(save * math.ceil(nmonths))} (d) loan gives immediate use; saving is cheaper',
               f'(a) PMT = {money(P1)} (M1 A1), total {money(T1)} (A1). (b) TVM PV = 0, PMT = −{save}, FV = {price}, I% = {r3} (M1): N = {nmonths:.2f} → {math.ceil(nmonths)} months (A1). '
               f'(c) {save} × {math.ceil(nmonths)} = {money(save * math.ceil(nmonths))} (A1). (d) R1 loan: immediate use of {item}; R1 saving: costs less because interest is earned not paid (but price may rise with inflation).',
               9, 'multi_step', gap='G5')


# =============================================================================================
# ch04 Exponents, logarithms and systems of equations
# =============================================================================================
def _mono(c, e, v='x'):
    """c·v^e as text (integer exponent, may be negative or zero)."""
    cs = '' if c == 1 and e != 0 else (MINUS if c == -1 and e != 0 else (str(c) if c >= 0 else MINUS + str(-c)))
    if e == 0:
        return str(c) if c >= 0 else MINUS + str(-c)
    return f'{cs}{v}{sup(e) if e != 1 else ""}'


R.facts('ch04-st1', F(
    terms=[('logarithm', 'log_a b = c means a^c = b: the logarithm is the exponent to which the base must be raised'),
           ('natural logarithm', 'the logarithm with base e ≈ 2.718, written ln x = log_e x'),
           ('common logarithm', 'the logarithm with base 10, written log x = log₁₀ x')],
    facts=[('What is the value of log₁₀ 0.001?', '−3', ['3', '−2', '0.001'], '10⁻³ = 0.001.'),
           ('Which expression is equal to x⁻³?', '1/x³', ['−x³', '−3x', 'x^(1/3)'], 'A negative exponent means the reciprocal.'),
           ('Which value of x solves eˣ = 20?', 'ln 20', ['log 20', '20/e', 'e²⁰'], 'Take natural logarithms: x = ln 20 ≈ 3.00.'),
           ('What is a⁰ for any a ≠ 0?', '1', ['0', 'a', 'undefined'], 'aⁿ ÷ aⁿ = a⁰ = 1.')],
    why=[('Explain why log₁₀(−5) is undefined in the real numbers.', '10ˣ is positive for every real x, so no real power of 10 equals −5.'),
         ('Explain why log₁₀ 4500 lies between 3 and 4.', '10³ = 1000 < 4500 < 10 000 = 10⁴, and log is increasing, so 3 < log 4500 < 4.'),
         ('Explain why a⁻ⁿ = 1/aⁿ, using the laws of exponents.', 'aⁿ × a⁻ⁿ = a⁰ = 1, so a⁻ⁿ is the reciprocal of aⁿ.')],
    misc=[('(2x³)⁴ = 2x¹² because you multiply the powers.', 'The power applies to the coefficient too: (2x³)⁴ = 2⁴x¹² = 16x¹².'),
          ('x² × x⁵ = x¹⁰.', 'When multiplying powers of the same base, add exponents: x² × x⁵ = x⁷.')],
))


@R.add('ch04-st1', ALL, (1, 5), 'short')
def exp_core(rng, slot):
    c, d = slot.c, slot.d
    if c == 'C1':
        a, p, q = rng.randint(2, 5), rng.randint(2, 6), rng.randint(2, 4)
        b, s_ = rng.randint(2, 6), rng.randint(1, 9)
        coef = a ** q
        e = p * q - s_
        g = math.gcd(coef, b)
        if coef % b == 0:
            res = _mono(coef // b, e)
        else:
            res = f'{coef // g}{"x" + (sup(e) if e != 1 else "") if e > 0 else ""}/{b // g}' + (f'x{sup(-e) if -e != 1 else ""}' if e < 0 else '')
        if e == 0:
            res = f'{coef // g}/{b // g}' if coef % b else str(coef // b)
        wr = [_mono(a * q, e) if coef % b else _mono(coef // b + 1, e), _mono(coef // b if coef % b == 0 else coef, p + q - s_), _mono(coef // b if coef % b == 0 else a, p * q + s_)]
        stem = f'Simplify ({a}x{sup(p)}){sup(q)} ÷ ({b}x{sup(s_) if s_ > 1 else ""}).'
        if d <= 1:
            return mcq(rng, stem, res, wr, f'({a}x{sup(p)}){sup(q)} = {coef}x{sup(p * q)}; ÷ {b}x{sup(s_) if s_ > 1 else ""} gives {res}.')
        return ret(stem, res, f'{coef}x{sup(p * q)} (A1); divide and subtract exponents (M1); {res} (A1).', 3 if d >= 3 else 2)
    if c == 'C2':
        v = rng.random()
        if v < 0.5:
            nval = rng.choice([rng.randint(11, 99), rng.randint(101, 999), rng.randint(1001, 9999), round(rng.uniform(0.011, 0.099), 3), round(rng.uniform(0.11, 0.99), 2)])
            lo = math.floor(math.log10(nval))
            return ret(f'Without a calculator, explain between which two consecutive integers log₁₀ {nval} lies. Then use your GDC to find its value to 3 s.f.', f'{m(lo)} and {m(lo + 1)}; {m(sf(math.log10(nval)))}',
                       f'R1 10{sup(lo)} = {10 ** lo:g} < {nval} < {10 ** (lo + 1):g} = 10{sup(lo + 1)}; log is increasing (R1); A1 {m(sf(math.log10(nval)))}.', 3, 'explain')
        a, b = rng.randint(2, 9), rng.randint(2, 6)
        return ret(f'{name(rng)} writes ({a}x{sup(b)})² = {a}x{sup(b + 2)}. Identify two errors and give the correct simplification.', f'{a * a}x{sup(2 * b)}',
                   f'R1 the coefficient must also be squared ({a}² = {a * a}); R1 exponents are multiplied, not added ({b} × 2 = {2 * b}); A1 {a * a}x{sup(2 * b)}.', 3, 'explain', gap='G2')
    ctx = rng.randint(0, 3)
    if c == 'C3':
        if ctx == 0:
            h = round(rng.uniform(1.1, 9.9), 1) * 10 ** -rng.randint(2, 11)
            ph = -math.log10(h)
            liquid = pick(rng, ['a sample of rain water', 'lemon juice', 'sea water', 'a soil solution', 'a cleaning solution', 'black coffee'])
            return ret(f'The pH of a solution is pH = −log₁₀[H⁺], where [H⁺] is the hydrogen ion concentration in mol dm⁻³. For {liquid}, [H⁺] = {sci(h, 2)}. Find its pH.',
                       sf(ph), f'−log₁₀({sci(h, 2)}) (M1) = {sf(ph)} (A1).', 2, 'numerical')
        if ctx == 1:
            a_, k_ = rng.randint(50, 900), round(rng.uniform(0.02, 0.35), 3)
            tgt = round(a_ * rng.uniform(2, 6), -1)
            t = math.log(tgt / a_) / k_
            what = pick(rng, ['followers of a new social-media account', 'bacteria in a dish', 'downloads of an app', 'cases of a seasonal infection'])
            return ret(f'The number of {what} after t days is modelled by N = {a_}e^({k_}t). Find the value of t when N = {int(tgt)}.', f't = {sf(t)}',
                       f'e^({k_}t) = {int(tgt)}/{a_} (M1); {k_}t = ln({sf(tgt / a_)}) (M1); t = {sf(t)} days (A1).', 3, 'numerical')
        if ctx == 2:
            x = round(rng.uniform(0.2, 3.5), 2)
            return ret(f'Solve 10ˣ = {sf(10 ** x)}, giving x to 3 significant figures, and verify your answer.', f'x = {sf(math.log10(float(sf(10 ** x))))}',
                       f'x = log₁₀ {sf(10 ** x)} (M1) = {sf(math.log10(float(sf(10 ** x))))} (A1).', 2, 'numerical')
        I = round(rng.uniform(1.1, 9.9), 1) * 10 ** -rng.randint(3, 9)
        L = 10 * math.log10(I / 1e-12)
        src = pick(rng, ['a busy street', 'a lawn mower', 'a library', 'a rock concert', 'a dishwasher', 'a jet at take-off'])
        return ret(f'The loudness of a sound in decibels is L = 10 log₁₀(I/I₀), where I₀ = 10⁻¹² W m⁻². The intensity of the sound from {src} is {sci(I, 2)} W m⁻². Find its loudness.',
                   f'{sf(L)} dB', f'10 log₁₀({sci(I, 2)} ÷ 10⁻¹²) (M1) = {sf(L)} dB (A1).', 2, 'numerical')
    # C4
    if ctx % 2 == 0:
        p1, p2 = sorted([round(rng.uniform(2.0, 8.5), 1) for _ in range(2)])
        if p2 - p1 < 0.5:
            return None
        ratio = 10 ** (p2 - p1)
        a1, a2 = pick(rng, [('lemon juice', 'tomato juice'), ('vinegar', 'milk'), ('acid rain', 'tap water'), ('cola', 'coffee'), ('stomach acid', 'orange juice')])
        return ret(f'pH = −log₁₀[H⁺]. Sample A ({a1}) has pH {p1} and sample B ({a2}) has pH {p2}. (a) Find [H⁺] for each sample. (b) Find how many times more acidic (greater [H⁺]) sample A is than sample B. '
                   f'(c) Explain why a difference of 1 in pH always corresponds to the same ratio of concentrations.',
                   f'(a) A {sci(10 ** -p1)}, B {sci(10 ** -p2)} (b) {sf(ratio)} times (c) ratio = 10^(Δ pH)',
                   f'(a) [H⁺] = 10^(−pH) (M1): {sci(10 ** -p1)} (A1), {sci(10 ** -p2)} (A1). (b) {sci(10 ** -p1)} ÷ {sci(10 ** -p2)} = 10^{p2 - p1:.1f} (M1) = {sf(ratio)} (A1). (c) R1 [H⁺]_A/[H⁺]_B = 10^(pH_B − pH_A), depending only on the difference.',
                   7, 'multi_step', gap='G5')
    A, B = rng.randint(200, 900), rng.randint(1000, 4000)
    ka, kb = round(rng.uniform(0.08, 0.2), 3), round(rng.uniform(0.01, 0.06), 3)
    t = math.log(B / A) / (ka - kb)
    c1, c2 = rng.sample(['Ashgrove', 'Kilifi', 'Porto Novo', 'Tromsø', 'Cusco', 'Hoi An', 'Galway', 'Rotorua'], 2)
    return ret(f'The populations of two villages t years after 2020 are modelled by P_A = {A}e^({ka}t) for {c1} and P_B = {B}e^({kb}t) for {c2}. '
               f'(a) Find the population of each village in 2030. (b) Find the value of t when the populations are equal, using logarithms. (c) Comment on the validity of using these models for 50 years.',
               f'(a) {round(A * math.exp(10 * ka))}, {round(B * math.exp(10 * kb))} (b) t = {sf(t)} (c) unrealistic long-term exponential growth',
               f'(a) {round(A * math.exp(10 * ka))} (A1), {round(B * math.exp(10 * kb))} (A1). (b) {A}e^({ka}t) = {B}e^({kb}t) ⇒ e^({sf(ka - kb)}t) = {B}/{A} (M1); t = ln({sf(B / A)})/{sf(ka - kb)} (M1) = {sf(t)} (A1). '
               f'(c) R1 exponential models predict unlimited growth; resources, migration and policy limit populations.', 7, 'multi_step', gap='G5')


R.facts('ch04-st2', F(
    terms=[('system of linear equations', 'two or more linear equations in the same unknowns that must be satisfied simultaneously'),
           ('root of a polynomial equation', 'a value of x that makes the polynomial equal to zero; graphically an x-intercept of y = p(x)')],
    facts=[('How many solutions does the system 2x + 3y = 6, 4x + 6y = 12 have?', 'infinitely many', ['none', 'exactly one', 'exactly two'], 'The second equation is twice the first: the lines coincide.'),
           ('How many solutions does the system x + 2y = 4, x + 2y = 9 have?', 'none', ['one', 'two', 'infinitely many'], 'Parallel lines with different intercepts never meet.'),
           ('What is the maximum number of real roots of a cubic equation?', '3', ['2', '4', '1'], 'A polynomial of degree n has at most n real roots.')],
    why=[('Explain why a cubic equation with real coefficients always has at least one real root.', 'As x → ∞ and x → −∞ the cubic takes values of opposite signs, and its graph is continuous, so it must cross the x-axis at least once.'),
         ('Explain why three unknowns usually need three independent equations.', 'Each independent equation removes one degree of freedom; with fewer equations at least one unknown can be chosen freely, giving infinitely many solutions.')],
    misc=[('The equation x² + 4 = 0 has the solutions x = ±2.', 'x² = −4 has no real solutions; (±2)² = 4 ≠ −4. (Its solutions are the complex numbers ±2i.)')],
))


@R.add('ch04-st2', ALL, (1, 5), 'short')
def systems_core(rng, slot):
    c, d = slot.c, slot.d
    if c == 'C1':
        x, y = rng.randint(-6, 9), rng.randint(-5, 9)
        a, b, c_, d_ = rng.randint(1, 6), rng.choice([-4, -3, -2, -1, 1, 2, 3, 5]), rng.randint(1, 5), rng.choice([-3, -2, 1, 2, 4])
        if a * d_ - b * c_ == 0:
            return None
        e1, e2 = a * x + b * y, c_ * x + d_ * y
        stem = f'Solve the simultaneous equations {a if a > 1 else ""}x {sgn(b)}y = {m(e1)} and {c_ if c_ > 1 else ""}x {sgn(d_)}y = {m(e2)}.'.replace(' 1y', ' y')
        if d <= 1:
            return mcq(rng, stem, f'x = {m(x)}, y = {m(y)}', [f'x = {m(y)}, y = {m(x)}', f'x = {m(x + 1)}, y = {m(y - 1)}', f'x = {m(-x)}, y = {m(y)}' if x else f'x = 2, y = {m(y + 2)}'],
                       f'Check: {a}({m(x)}) + {b}({m(y)}) = {m(e1)} ✓.')
        return ret(stem, f'x = {m(x)}, y = {m(y)}', f'Elimination/substitution or GDC (M1); x = {m(x)} (A1), y = {m(y)} (A1).', 3)
    if c == 'C2':
        a, b = rng.randint(1, 5), rng.randint(1, 5)
        k = rng.randint(2, 4)
        e1 = rng.randint(3, 20)
        e2 = e1 * k + rng.choice([0, rng.randint(1, 9)])
        same = e2 == e1 * k
        return ret(f'Explain, without solving, how many solutions the system {a}x + {b}y = {e1}, {a * k}x + {b * k}y = {e2} has, and interpret this graphically.',
                   'infinitely many (same line)' if same else 'no solutions (parallel lines)',
                   f'R1 the second left-hand side is {k} × the first; R1 {"the right-hand side is also " + str(k) + " ×, so the equations describe the same line: infinitely many solutions" if same else "but the right-hand side is not " + str(k) + " × " + str(e1) + ", so the lines are parallel and distinct: no solution"}.',
                   2, 'explain')
    if c == 'C3':
        if rng.random() < 0.55:
            pa, pc, ps = rng.randint(12, 30), rng.randint(5, 11), rng.randint(8, 18)
            na1, nc1, ns1 = rng.randint(20, 90), rng.randint(10, 80), rng.randint(5, 40)
            na2, nc2, ns2 = rng.randint(20, 90), rng.randint(10, 80), rng.randint(5, 40)
            na3, nc3, ns3 = rng.randint(20, 90), rng.randint(10, 80), rng.randint(5, 40)
            M = np.array([[na1, nc1, ns1], [na2, nc2, ns2], [na3, nc3, ns3]], float)
            if abs(np.linalg.det(M)) < 50:
                return None
            r1, r2, r3 = M @ np.array([pa, pc, ps])
            venue = pick(rng, ['A zoo in Singapore', 'A museum in Vienna', 'A water park in Dubai', 'A theatre in Toronto', 'An aquarium in Lisbon'])
            cc = cur(rng)
            return ret(f'{venue} sells adult, child and senior tickets. On Friday {na1} adult, {nc1} child and {ns1} senior tickets raised {int(r1)} {cc}; on Saturday {na2}, {nc2} and {ns2} raised {int(r2)} {cc}; '
                       f'on Sunday {na3}, {nc3} and {ns3} raised {int(r3)} {cc}. Find the price of each type of ticket.', f'adult {pa}, child {pc}, senior {ps} {cc}',
                       f'{na1}a + {nc1}c + {ns1}s = {int(r1)}, … (M1 for setting up three equations) (A1); GDC: a = {pa}, c = {pc}, s = {ps} (A1 A1).', 4, 'numerical')
        roots = sorted(rng.sample([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 0.5, -0.5, 1.5], 3))
        lead = rng.choice([1, 2, -1])
        co = [lead * cf for cf in np.poly(roots)]
        if any(abs(c0 - round(c0)) > 1e-9 for c0 in co):
            return None
        co = [int(round(c0)) for c0 in co]
        return ret(f'Use technology to solve {poly(co)} = 0.', 'x = ' + ', '.join(m(_num(r_)) for r_ in roots),
                   f'GDC polynomial solver or graph (M1); x = ' + ', '.join(m(_num(r_)) for r_ in roots) + ' (A2 for all three, A1 for two).', 3, 'numerical')
    # C4: quadratic through three points (system) then use
    a, b, c0 = rng.choice([-0.5, -0.2, -0.1, -0.05, -0.02]), round(rng.uniform(0.4, 2.5), 2), round(rng.uniform(1, 12), 1)
    land0 = (-b - math.sqrt(b * b - 4 * a * c0)) / (2 * a)
    xs = sorted(rng.sample(range(1, max(5, int(land0 * 0.9))), 3))
    ys = [round(a * x ** 2 + b * x + c0, 4) for x in xs]
    ysd = [m(_num(y_)) for y_ in ys]
    xv = -b / (2 * a)
    yv = c0 - b * b / (4 * a)
    land = (-b - math.sqrt(b * b - 4 * a * c0)) / (2 * a)
    what = pick(rng, ['a ball kicked from a raised platform', 'water from a fountain jet', 'a javelin', 'a drone following a parabolic path', 'a ski jumper'])
    return ret(f'The height y metres of {what} at horizontal distance x metres is modelled by y = ax² + bx + c. It passes through ({xs[0]}, {ysd[0]}), ({xs[1]}, {ysd[1]}) and ({xs[2]}, {ysd[2]}). '
               f'(a) Write down a system of three equations in a, b and c. (b) Solve it to find a, b and c. (c) Find the maximum height and the horizontal distance at which y = 0.',
               f'(b) a = {m(_num(a))}, b = {_num(b)}, c = {_num(c0)} (c) max {sf(yv)} m at x = {sf(xv)}; lands at x = {sf(land)} m',
               f'(a) {xs[0] ** 2}a + {xs[0]}b + c = {ysd[0]}, … (A1 A1). (b) GDC (M1): a = {m(_num(a))}, b = {_num(b)}, c = {_num(c0)} (A1). (c) vertex x = −b/(2a) = {sf(xv)} (M1), max height {sf(yv)} m (A1); y = 0 at x = {sf(land)} m (A1) (reject negative root, R1).',
               8, 'multi_step', gap='G5')


R.facts('ch04-st3', F(
    terms=[('product law of logarithms', 'log_a(xy) = log_a x + log_a y'),
           ('quotient law of logarithms', 'log_a(x/y) = log_a x − log_a y'),
           ('power law of logarithms', 'log_a(xᵐ) = m log_a x'),
           ('change of base', 'log_a x = log_b x / log_b a, used to evaluate logs in any base with ln or log₁₀')],
    facts=[('Which expression is equal to log 12 − log 3?', 'log 4', ['log 9', 'log 36', 'log 12 / log 3'], 'Quotient law: log(12/3).'),
           ('What is log₂ 64?', '6', ['8', '32', '5'], '2⁶ = 64.'),
           ('Which expression is equal to 3 ln x + ln y?', 'ln(x³y)', ['ln(3xy)', '3 ln(xy)', 'ln(x³ + y)'], 'Power law then product law.')],
    why=[('Explain why log_a 1 = 0 for any valid base a.', 'a⁰ = 1, so the power of a giving 1 is 0.'),
         ('Explain how the change of base formula lets you evaluate log₇ 50 on a calculator.', 'Write log₇ 50 = ln 50/ln 7 (or log 50/log 7), both available on the calculator; this gives 2.01.'),
         ('Explain why log(x²) = 2 log x is valid only for x > 0 in the real numbers.', 'log x is undefined for x ≤ 0, whereas log(x²) is defined for all x ≠ 0; the identity holds only where both sides are defined.')],
    misc=[('log(a + b) = log a + log b.', 'The product law is log(ab) = log a + log b; there is no law for the log of a sum.'),
          ('log 8 / log 2 = log 4.', 'log 8 / log 2 = 3 log 2 / log 2 = 3 (it is log₂ 8), not log(8/2).')],
))


@R.add('ch04-st3', ALL, (1, 5), 'short')
def logs_core(rng, slot):
    c, d = slot.c, slot.d
    if c == 'C1':
        base = rng.choice([2, 3, 4, 5, 10])
        e = rng.randint(2, 5) if base < 10 else rng.randint(2, 6)
        v = base ** e
        if rng.random() < 0.5:
            return nmcq(rng, f'Find the exact value of log{"₁₀" if base == 10 else "_" + str(base)} {v}.', e, [e + 1, v / base, e - 1], f'{base}{sup(e)} = {v}.', fmtf=lambda z: _num(z))
        a, b = rng.randint(2, 9), rng.randint(2, 9)
        k = rng.randint(2, 4)
        return ret(f'Write {k} log x + log {a} − log {b} as a single logarithm.', f'log({a}x{sup(k)}/{b})', f'Power law (M1); product and quotient laws (M1); log({a}x{sup(k)}/{b}) (A1).', 3 if d >= 2 else 2)
    if c == 'C2':
        a, b = rng.randint(2, 20), rng.randint(2, 20)
        return ret(f'{name(rng)} claims that log({a} + {b}) = log {a} + log {b}. Use your GDC to show that this is false, and state the correct law that it confuses.',
                   f'log {a + b} = {sf(math.log10(a + b))} ≠ {sf(math.log10(a) + math.log10(b))}', f'A1 log {a + b} = {sf(math.log10(a + b))}; A1 log {a} + log {b} = {sf(math.log10(a * b))} = log {a * b}; R1 the product law log(ab) = log a + log b.',
                   3, 'explain', gap='G2')
    if c == 'C3':
        v = rng.randint(0, 2)
        if v == 0:
            a, b = rng.randint(2, 9), round(rng.uniform(10, 900), 1)
            x = math.log(b) / math.log(a)
            return ret(f'Solve {a}ˣ = {b}, giving your answer to 3 significant figures.', f'x = {sf(x)}', f'x log {a} = log {b} (M1); x = log {b}/log {a} (A1) = {sf(x)} (A1).', 3, 'numerical')
        if v == 1:
            base = rng.choice([2, 3, 10])
            k = rng.randint(1, 6)
            rhs = rng.randint(2, 4) if base != 10 else rng.randint(1, 2)
            # log(x) + log(x - k) = rhs  -> x(x-k) = base^rhs
            N = base ** rhs
            x = (k + math.sqrt(k * k + 4 * N)) / 2
            bs = '₁₀' if base == 10 else f'_{base}'
            return ret(f'Solve log{bs} x + log{bs}(x − {k}) = {rhs}.', f'x = {sf(x)}', f'log{bs}(x(x − {k})) = {rhs} (M1); x² − {k}x − {N} = 0 (A1); x = {sf(x)} (A1), rejecting the negative root since x > {k} (R1).', 4, 'numerical')
        p, q = rng.randint(2, 5), rng.randint(2, 5)
        return ret(f'Given that log a = p and log b = q, express log(a{sup(p)}√b / 10) in terms of p and q.', f'{p}p + q/2 − 1', f'{p} log a + ½ log b − log 10 (M1 M1); {p}p + q/2 − 1 (A1).', 3, 'numerical')
    a, b = rng.randint(2, 5), rng.randint(2, 7)
    if a == b:
        return None
    k1, k2 = rng.choice([1, 2, 3, 4, 5, 6]), rng.randint(1, 3)
    if k1 in (a, b):
        return None
    # k1 · a^x = b^(x + k2)  -> ln k1 + x ln a = (x + k2) ln b -> x = (k2 ln b − ln k1)/(ln a − ln b)
    x = (k2 * math.log(b) - math.log(k1)) / (math.log(a) - math.log(b))
    return ret(f'(a) Solve the equation {k1 if k1 > 1 else ""}{"·" if k1 > 1 else ""}{a}ˣ = {b}^(x + {k2}), giving the exact answer in terms of natural logarithms and its value to 3 s.f. '
               f'(b) Explain why taking logarithms is necessary here. (c) Verify your answer using a GDC graph or table.',
               f'(a) x = ({k2 if k2 > 1 else ""}{" " if k2 > 1 else ""}ln {b}{" − ln " + str(k1) if k1 > 1 else ""})/(ln {a} − ln {b}) = {m(sf(x))} (b) unknown in the exponents with different bases',
               f'(a) take ln of both sides (M1): {"ln " + str(k1) + " + " if k1 > 1 else ""}x ln {a} = (x + {k2}) ln {b} (A1); collect x terms (M1); x = {m(sf(x))} (A1). (b) R1 the bases cannot be made equal. (c) A1 intersection of the two graphs at x = {m(sf(x))}.',
               7, 'multi_step', gap='G5')


@R.add('ch04-st3', ('C3', 'C4'), (2, 5), 'multi_step')
def richter(rng, slot):
    M1_, M2_ = sorted([round(rng.uniform(3.0, 8.9), 1) for _ in range(2)])
    if M2_ - M1_ < 0.4:
        return None
    place1, place2 = rng.sample(['Chile', 'Japan', 'Nepal', 'Turkey', 'New Zealand', 'Mexico', 'Indonesia', 'Italy', 'Peru', 'Iceland'], 2)
    E1, E2 = 10 ** (4.8 + 1.5 * M1_), 10 ** (4.8 + 1.5 * M2_)
    A = 10 ** (M2_ - M1_)
    if slot.c == 'C3':
        return ret(f'The energy E joules released by an earthquake of magnitude M satisfies log₁₀ E = 4.8 + 1.5M. Find the energy released by an earthquake of magnitude {M2_} in {place2}.',
                   f'{sci(E2)} J', f'E = 10^(4.8 + 1.5 × {M2_}) (M1) = {sci(E2)} J (A1).', 2, 'numerical')
    return ret(f'For earthquakes, the magnitude M is related to the maximum amplitude A of the seismic wave by M = log₁₀(A/A₀) and the energy E (joules) by log₁₀ E = 4.8 + 1.5M. '
               f'An earthquake in {place1} had magnitude {M1_} and one in {place2} had magnitude {M2_}. (a) Find how many times greater the amplitude of the {place2} earthquake was. '
               f'(b) Find the ratio of the energies released. (c) Using the laws of logarithms, show that the energy ratio is (amplitude ratio)^1.5.',
               f'(a) {sf(A)} (b) {sf(E2 / E1)} (c) log(E₂/E₁) = 1.5(M₂ − M₁) = 1.5 log(A₂/A₁)',
               f'(a) A₂/A₁ = 10^({M2_} − {M1_}) (M1) = {sf(A)} (A1). (b) E₂/E₁ = 10^(1.5 × {M2_ - M1_:.1f}) (M1) = {sf(E2 / E1)} (A1). '
               f'(c) log E₂ − log E₁ = 1.5(M₂ − M₁) (M1) = 1.5 log(A₂/A₁) = log((A₂/A₁)^1.5) (M1) so E₂/E₁ = (A₂/A₁)^1.5 (AG R1).', 7, 'multi_step', gap='G5')


R.facts('ch04-st4', F(
    terms=[('rational exponent', 'an exponent of the form m/n, with x^(m/n) = (ⁿ√x)ᵐ'),
           ('nth root', 'x^(1/n): the number which, raised to the power n, gives x')],
    facts=[('What is 8^(2/3)?', '4', ['16/3', '2', '6'], '8^(1/3) = 2 and 2² = 4.'),
           ('What is 25^(−1/2)?', '1/5', ['−5', '−1/5', '5'], 'Negative exponent: reciprocal of √25.'),
           ('Which is equivalent to √(x³)?', 'x^(3/2)', ['x^(2/3)', 'x⁶', '3x/2'], 'Square root is the power ½.')],
    why=[('Explain why x^(1/2) is defined as √x.', 'Using (aᵐ)ⁿ = aᵐⁿ, (x^(1/2))² = x¹ = x, so x^(1/2) is the number whose square is x.'),
         ('Explain why 16^(3/4) can be evaluated by finding the fourth root first.', '16^(3/4) = (16^(1/4))³ = 2³ = 8; taking the root first keeps the numbers small.')],
    misc=[('9^(−1/2) = −3.', 'A negative exponent gives a reciprocal, not a negative: 9^(−1/2) = 1/√9 = 1/3.')],
))


@R.add('ch04-st4', ALL, (1, 5), 'short')
def ratexp_core(rng, slot):
    c, d = slot.c, slot.d
    base_root = rng.choice([(4, 2), (8, 3), (9, 2), (16, 4), (16, 2), (25, 2), (27, 3), (32, 5), (64, 3), (64, 2), (81, 4), (125, 3), (36, 2), (49, 2)])
    b, n = base_root
    root = round(b ** (1 / n))
    mm = rng.choice([1, 2, 3, -1, -2, -3])
    val_num = root ** abs(mm)
    vs = str(val_num) if mm > 0 else f'1/{val_num}'
    ex = f'{mm}/{n}' if mm > 0 else f'−{-mm}/{n}'
    if c == 'C1':
        if d <= 1:
            return mcq(rng, f'Find the exact value of {b}^({ex}).', vs, [str(b * mm // n) if mm > 0 else f'−{val_num}', f'{root ** (abs(mm) + 1)}' if mm > 0 else str(val_num), f'1/{val_num}' if mm > 0 else f'−1/{val_num}'],
                       f'{b}^(1/{n}) = {root}; then power {abs(mm)}{" and reciprocal" if mm < 0 else ""}: {vs}.')
        return ret(f'Without a calculator, find the value of {b}^({ex}).', vs, f'{b}^(1/{n}) = {root} (M1); {vs} (A1).', 2)
    if c == 'C2':
        return ret(f'{name(rng)} evaluates {b}^({ex}) by computing {b}{sup(abs(mm))} first and then taking the {["", "", "square", "cube", "fourth", "fifth"][n]} root. Explain why this gives the correct value but is less efficient than taking the root first.',
                   vs, f'R1 (b^m)^(1/n) = (b^(1/n))^m by the law (aᵖ)^q = a^(pq); R1 taking the root first ({root}) avoids large numbers like {b ** abs(mm)}; A1 {vs}.', 3, 'explain')
    if c == 'C3':
        v = rng.random()
        if v < 0.5:
            k = rng.choice([4, 9, 16, 25, 27, 8, 64])
            r_ = {4: 2, 9: 2, 16: 2, 25: 2, 27: 3, 8: 3, 64: 3}[k]
            e = rng.randint(2, 5) * r_
            pw = rng.choice([1, 2]) if r_ == 2 else 1
            co = round(k ** (pw / r_))
            return ret(f'Simplify ({k}x{sup(e)})^({pw}/{r_}).', f'{co}x{sup(e * pw // r_)}', f'{k}^({pw}/{r_}) = {co} (A1); (x{sup(e)})^({pw}/{r_}) = x{sup(e * pw // r_)} (A1).', 2, 'numerical')
        animal, lo, hi = pick(rng, [('a cat', 3, 6), ('a goat', 40, 80), ('a horse', 380, 600), ('a dolphin', 150, 300), ('a chimpanzee', 35, 65),
                                    ('a sheep', 45, 100), ('a red deer', 90, 190), ('a cow', 500, 800)])
        M = rng.randint(lo, hi)
        B = 70 * M ** 0.75
        return ret(f'Kleiber\'s law models the basal metabolic rate of a mammal as B = 70M^(3/4) kcal per day, where M is the mass in kg. Find B for {animal} of mass {M} kg.', f'{sf(B)} kcal per day',
                   f'70 × {M}^(0.75) (M1) = {sf(B)} (A1).', 2, 'numerical')
    M1_, M2_ = rng.randint(2, 60), rng.randint(200, 900)
    ratio_m = M2_ / M1_
    ratio_b = ratio_m ** 0.75
    T = rng.randint(800, 3000)
    Ms = (T / 70) ** (4 / 3)
    return ret(f'Kleiber\'s law: B = 70M^(3/4) (B in kcal per day, M in kg). (a) Find B for animals of mass {M1_} kg and {M2_} kg. (b) The heavier animal is {sf(ratio_m)} times as heavy; find how many times greater its metabolic rate is. '
               f'(c) Find the mass of an animal with B = {T} kcal per day. (d) Explain what the exponent 3/4 < 1 implies about the energy use per kilogram of large animals.',
               f'(a) {sf(70 * M1_ ** 0.75)}, {sf(70 * M2_ ** 0.75)} (b) {sf(ratio_b)} (c) {sf(Ms)} kg (d) less energy per kg',
               f'(a) (A1)(A1). (b) ({sf(ratio_m)})^(3/4) (M1) = {sf(ratio_b)} (A1). (c) M = ({T}/70)^(4/3) (M1) = {sf(Ms)} kg (A1). (d) R1 B/M = 70M^(−1/4) decreases as M increases.',
               7, 'multi_step', gap='G5')


# =============================================================================================
# ch05 Complex numbers
# =============================================================================================
def cx(z, exact=True):
    a, b = (z.real, z.imag) if isinstance(z, complex) else z
    fa = _num(a)
    fb = _num(abs(b))
    if abs(b) < 1e-12:
        return m(fa)
    bi = ('' if fb == '1' else fb) + 'i'
    if abs(a) < 1e-12:
        return (MINUS if b < 0 else '') + bi
    return f'{m(fa)} {"−" if b < 0 else "+"} {bi}'


def cxf(z):
    """complex as a + bi with fractions where exact."""
    from fractions import Fraction
    a, b = Fraction(z.real).limit_denominator(1000), Fraction(z.imag).limit_denominator(1000)

    def f(q):
        return str(q.numerator) if q.denominator == 1 else f'{q.numerator}/{q.denominator}'
    if b == 0:
        return m(f(a))
    bs = f(abs(b))
    bi = ('' if bs == '1' else bs) + 'i'
    if a == 0:
        return (MINUS if b < 0 else '') + bi
    return f'{m(f(a))} {"−" if b < 0 else "+"} {bi}'


def _rz(rng, lo=-6, hi=7, nz=True):
    while True:
        a, b = rng.randint(lo, hi), rng.randint(lo, hi)
        if not nz or (a != 0 and b != 0):
            return complex(a, b)


R.facts('ch05-st1', F(
    terms=[('imaginary unit', 'i, the number with i² = −1'),
           ('complex conjugate', 'for z = a + bi, z* = a − bi; z z* = a² + b² is real'),
           ('Argand diagram', 'a plane in which the complex number a + bi is represented by the point (a, b), real part horizontal and imaginary part vertical'),
           ('Cartesian form', 'the form z = a + bi with a = Re(z) and b = Im(z) real')],
    facts=[('What is i⁶?', '−1', ['1', 'i', '−i'], 'i⁶ = (i²)³ = (−1)³ = −1.'),
           ('Which is the conjugate of −3 + 4i?', '−3 − 4i', ['3 − 4i', '3 + 4i', '4 − 3i'], 'Change the sign of the imaginary part only.'),
           ('In which quadrant of the Argand diagram is −2 − 5i?', 'third', ['first', 'second', 'fourth'], 'Real part negative, imaginary part negative.')],
    why=[('Explain why the roots of a quadratic equation with real coefficients and a negative discriminant form a conjugate pair.', 'x = (−b ± √Δ)/(2a) with Δ < 0 gives (−b ± i√|Δ|)/(2a): same real part −b/(2a) and opposite imaginary parts.'),
         ('Explain why multiplying the numerator and denominator by the conjugate of the denominator allows a division to be written in the form a + bi.', 'The denominator becomes (c + di)(c − di) = c² + d², a real number, so the quotient splits into real and imaginary parts.')],
    misc=[('i² = 1 because i × i is a positive square.', 'By definition i² = −1; i is not a real number, so the rule "a square is non-negative" does not apply.'),
          ('(2 + 3i)² = 4 + 9i² = −5.', 'Use (a + b)² = a² + 2ab + b²: 4 + 12i + 9i² = −5 + 12i.')],
))


@R.add('ch05-st1', ALL, (1, 5), 'short')
def cart_core(rng, slot):
    c, d = slot.c, slot.d
    z1, z2 = _rz(rng), _rz(rng)
    if c == 'C1':
        op = pick(rng, ['+', '−', '×'])
        v = z1 + z2 if op == '+' else z1 - z2 if op == '−' else z1 * z2
        stem = f'Given z₁ = {cx(z1)} and z₂ = {cx(z2)}, find z₁ {op} z₂ in the form a + bi.'
        if d <= 1:
            wr = [cx(z1 * z2.conjugate()) if op == '×' else cx(z1 - z2 if op == '+' else z1 + z2), cx(complex(v.real, -v.imag)), cx(complex(z1.real * z2.real, z1.imag * z2.imag))]
            return mcq(rng, stem, cx(v), wr, f'z₁ {op} z₂ = {cx(v)}' + (' (using i² = −1).' if op == '×' else '.'))
        return ret(stem, cx(v), f'{"Expand, using i² = −1 (M1); " if op == "×" else ""}{cx(v)} (A1).', 2 if op == '×' else 1)
    if c == 'C2':
        b = rng.choice([2, 4, 6, -2, -4, -6, 8])
        cc_ = (b * b) // 4 + rng.randint(1, 30)
        disc = b * b - 4 * cc_
        re_, im_ = -b / 2, math.sqrt(-disc) / 2
        return ret(f'Explain why the equation z² {sgn(b)}z + {cc_} = 0 has no real roots, and find its roots, commenting on how they are related.',
                   f'z = {cx(complex(re_, im_), False)} and z = {cx(complex(re_, -im_), False)}; conjugate pair',
                   f'R1 Δ = {b}² − 4({cc_}) = {m(disc)} < 0; M1 quadratic formula with √({m(disc)}) = {sf(math.sqrt(-disc))}i; A1 roots {cx(complex(re_, im_), False)}, {cx(complex(re_, -im_), False)}; R1 they are complex conjugates.',
                   4, 'explain')
    if c == 'C3':
        v = z1 / z2
        if rng.random() < 0.5:
            return ret(f'Given z₁ = {cx(z1)} and z₂ = {cx(z2)}, express z₁/z₂ in the form a + bi, where a, b ∈ ℚ.', cxf(v),
                       f'Multiply by z₂* = {cx(z2.conjugate())} (M1); numerator {cx(z1 * z2.conjugate())} (A1), denominator {int(abs(z2) ** 2 + 0.5)} (A1); {cxf(v)} (A1).', 4, 'numerical')
        w = z1 * z2
        return ret(f'Let z = {cx(z1)} and w = {cx(z2)}. (a) Find zw and z − w*. (b) Plot z, w and zw on an Argand diagram and state the quadrant of zw.',
                   f'(a) zw = {cx(w)}, z − w* = {cx(z1 - z2.conjugate())} (b) quadrant {"first" if w.real > 0 and w.imag > 0 else "second" if w.real < 0 and w.imag > 0 else "third" if w.real < 0 and w.imag < 0 else "fourth" if w.real > 0 and w.imag < 0 else "on an axis"}',
                   f'(a) zw = {cx(w)} (M1 A1); z − w* = {cx(z1 - z2.conjugate())} (A1). (b) points ({_num(z1.real)}, {_num(z1.imag)}), ({_num(z2.real)}, {_num(z2.imag)}), ({_num(w.real)}, {_num(w.imag)}) plotted (A1); quadrant (A1).', 5, 'numerical')
    a_, b_ = rng.randint(-6, 6), rng.randint(-6, 6)
    p, q = rng.randint(2, 4), rng.choice([-3, -2, 2, 3])
    # z + p z* ... find z = a + bi with z + p z* = rhs?  z + p z* = (1 + p)a + (1 − p) b i
    rhs = complex((1 + p) * a_, (1 - p) * b_)
    w = complex(rng.randint(1, 5), q)
    return ret(f'(a) Find the complex number z = a + bi that satisfies z + {p}z* = {cx(rhs)}. (b) Hence find z × ({cx(w)}) and its modulus. (c) Verify your answer to (a) by substitution.',
               f'(a) z = {cx(complex(a_, b_))} (b) {cx(complex(a_, b_) * w)}, |·| = {sf(abs(complex(a_, b_) * w))}',
               f'(a) a + bi + {p}(a − bi) = {cx(rhs)} (M1); equate real parts {1 + p}a = {_num(rhs.real)} and imaginary parts {m(1 - p)}b = {m(_num(rhs.imag))} (M1); z = {cx(complex(a_, b_))} (A1 A1). '
               f'(b) {cx(complex(a_, b_) * w)} (A1); modulus √(({m(_num((complex(a_, b_) * w).real))})² + ({m(_num((complex(a_, b_) * w).imag))})²) = {sf(abs(complex(a_, b_) * w))} (A1). (c) R1 substitution checks.',
               7, 'multi_step', gap='G5')


R.facts('ch05-st2', F(
    terms=[('modulus', '|z| = r = √(a² + b²), the distance of z from the origin on the Argand diagram'),
           ('argument', 'arg z = θ, the angle from the positive real axis to the line joining 0 to z, usually −π < θ ≤ π'),
           ('modulus-argument form', 'z = r(cos θ + i sin θ) = r cis θ'),
           ('exponential form', 'z = re^(iθ), equivalent to r cis θ by Euler\'s formula')],
    facts=[('If z = 3e^(iπ/4) and w = 2e^(iπ/6), what is zw?', '6e^(5iπ/12)', ['5e^(5iπ/12)', '6e^(iπ/24)', '6e^(iπ²/24)'], 'Multiply moduli, add arguments.'),
           ('What is the modulus of 5 − 12i?', '13', ['7', '17', '√119'], '√(25 + 144) = 13.'),
           ('What is the argument of −4 (a negative real number)?', 'π', ['0', '−π/2', '4'], '−4 lies on the negative real axis.')],
    why=[('Explain why multiplying by i rotates a point on the Argand diagram by π/2 anticlockwise.', 'i = e^(iπ/2) has modulus 1 and argument π/2; multiplying multiplies moduli (by 1) and adds π/2 to the argument.'),
         ('Explain why arg(z/w) = arg z − arg w.', 'z/w = (r₁/r₂)e^(i(θ₁ − θ₂)) by the laws of exponents, so the arguments subtract.')],
    misc=[('arg(−1 − i) = arctan(−1/−1) = π/4.', '−1 − i lies in the third quadrant, so arg = −3π/4; arctan alone gives the wrong quadrant.')],
))


def _arg_str(t):
    from fractions import Fraction
    fr = Fraction(t / math.pi).limit_denominator(12)
    if abs(float(fr) * math.pi - t) < 1e-9:
        if fr == 0:
            return '0'
        num, den = fr.numerator, fr.denominator
        s = ('' if abs(num) == 1 else str(abs(num))) + 'π' + ('' if den == 1 else f'/{den}')
        return (MINUS if num < 0 else '') + s
    return m(sf(t))


@R.add('ch05-st2', ALL, (1, 5), 'short')
def polar_core(rng, slot):
    c, d = slot.c, slot.d
    nice = [(1, 1), (1, -1), (-1, 1), (-1, -1), (math.sqrt(3), 1), (1, math.sqrt(3)), (-math.sqrt(3), 1), (1, -math.sqrt(3)), (0, 1), (-1, 0)]
    if c == 'C1':
        z = _rz(rng)
        r, t = abs(z), math.atan2(z.imag, z.real)
        if d <= 1:
            return nmcq(rng, f'Find the modulus of z = {cx(z)}.', r, [abs(z.real) + abs(z.imag), z.real ** 2 + z.imag ** 2, abs(z.real - z.imag) + 0.5], f'|z| = √({_num(z.real)}² + {_num(z.imag)}²) = {sf(r)}.')
        return ret(f'For z = {cx(z)}, find |z| and arg z (in radians, −π < arg z ≤ π).', f'|z| = {sf(r)}, arg z = {m(sf(t))}',
                   f'|z| = √({_num(z.real ** 2 + z.imag ** 2)}) = {sf(r)} (A1); arg z = {m(sf(t))} (A1) – check quadrant.', 2)
    if c == 'C2':
        z = complex(-rng.randint(1, 6), -rng.randint(1, 6)) if rng.random() < 0.5 else complex(-rng.randint(1, 6), rng.randint(1, 6))
        t = math.atan2(z.imag, z.real)
        wrong = math.atan(z.imag / z.real)
        return ret(f'{name(rng)} finds the argument of z = {cx(z)} as arctan({_num(z.imag)}/{_num(z.real)}) = {m(sf(wrong))}. Explain why this is wrong and find the correct argument.', m(sf(t)),
                   f'R1 z lies in the {"third" if z.imag < 0 else "second"} quadrant, but arctan returns an angle in (−π/2, π/2); M1 adjust by {"−" if z.imag < 0 else "+"}π; A1 arg z = {m(sf(t))}.', 3, 'explain', gap='G2')
    r1, r2 = rng.randint(2, 6), rng.randint(2, 5)
    t1 = pick(rng, [math.pi / 6, math.pi / 4, math.pi / 3, math.pi / 2, 2 * math.pi / 3, 3 * math.pi / 4, 5 * math.pi / 6, -math.pi / 3, -math.pi / 4, -math.pi / 6])
    t2 = pick(rng, [math.pi / 6, math.pi / 4, math.pi / 3, -math.pi / 6, -math.pi / 2, math.pi / 12, 5 * math.pi / 12])
    if c == 'C3':
        v = rng.randint(0, 2)
        if v == 0:
            pt = pick(rng, nice)
            k = rng.randint(1, 4)
            z = complex(pt[0] * k, pt[1] * k)
            t = math.atan2(z.imag, z.real)
            zs = cx(z) if all(float(q).is_integer() for q in pt) else (f'{k}√3 {"+" if pt[1] > 0 else "−"} {k if k > 1 else ""}i' if abs(abs(pt[0]) - math.sqrt(3)) < 1e-9 and pt[0] > 0 else
                                                                       f'{MINUS}{k}√3 + {k if k > 1 else ""}i' if abs(abs(pt[0]) - math.sqrt(3)) < 1e-9 else f'{k if k > 1 else ""} {"+" if pt[1] > 0 else "−"} {k}√3i')
            rs_ = (f'{k if k > 1 else ""}√2' if abs(abs(pt[0]) - 1) < 1e-9 and abs(abs(pt[1]) - 1) < 1e-9 else str(2 * k) if abs(abs(pt[0]) - math.sqrt(3)) < 1e-9 or abs(abs(pt[1]) - math.sqrt(3)) < 1e-9 else str(k))
            return ret(f'Write z = {zs} in the form re^(iθ), giving exact values of r and θ.', ee(rs_, t),
                       f'r = {rs_} (A1); θ = {_arg_str(t)} (A1).', 2, 'numerical')
        if v == 1:
            op = pick(rng, ['×', '÷'])
            R_ = r1 * r2 if op == '×' else r1 / r2
            Tt = t1 + t2 if op == '×' else t1 - t2
            Tt = (Tt + math.pi) % (2 * math.pi) - math.pi
            if abs(Tt + math.pi) < 1e-9:
                Tt = math.pi
            Z = R_ * complex(math.cos(Tt), math.sin(Tt))
            return ret(f'Given z = {ee(r1, t1)} and w = {ee(r2, t2)}, find z {op} w in the form re^(iθ), −π < θ ≤ π, and in the form a + bi (3 s.f.).',
                       f'{ee(_num(R_), Tt)} = {cx(Z, False)}', f'{"multiply moduli, add" if op == "×" else "divide moduli, subtract"} arguments (M1); {ee(_num(R_), Tt)} (A1); {cx(Z, False)} (A1).', 3, 'numerical')
        n = rng.randint(3, 8)
        while r1 ** n > 1e5:
            n -= 1
        Rn = r1 ** n
        Tn = (n * t1 + math.pi) % (2 * math.pi) - math.pi
        Z = Rn * complex(math.cos(Tn), math.sin(Tn))
        return ret(f'Given z = {r1}(cos({_arg_str(t1)}) + i sin({_arg_str(t1)})), find z{sup(n)} in modulus-argument form and in the form a + bi.', f'{Rn} cis({_arg_str(Tn)}) = {cx(Z, False)}',
                   f'De Moivre: modulus {r1}{sup(n)} = {Rn} (A1); argument {n} × {_arg_str(t1)} reduced to {_arg_str(Tn)} (M1 A1); {cx(Z, False)} (A1).', 4, 'numerical')
    z = _rz(rng, -5, 6)
    w = complex(math.cos(t2), math.sin(t2)) * r2
    zw = z * w
    return ret(f'Let z = {cx(z)} and w = {ee(r2, t2)}. (a) Write z in exponential form (3 s.f.). (b) Find zw in exponential form. (c) Describe the geometric transformation on the Argand diagram that maps z to zw. '
               f'(d) Find the least positive integer n for which wⁿ is a positive real number.',
               f'(a) {sf(abs(z))}e^({m(sf(math.atan2(z.imag, z.real)))}i) (b) {sf(abs(zw))}e^({m(sf(math.atan2(zw.imag, zw.real)))}i) (c) enlargement scale factor {r2}, rotation {_arg_str(t2)} about 0 (d) n = {_least_n(t2)}',
               f'(a) r = {sf(abs(z))}, θ = {m(sf(math.atan2(z.imag, z.real)))} (A1 A1). (b) multiply moduli, add arguments (M1): {sf(abs(zw))}e^({m(sf(math.atan2(zw.imag, zw.real)))}i) (A1). '
               f'(c) enlargement ×{r2} (A1) and rotation through {_arg_str(t2)} about the origin ({'anticlockwise' if t2 > 0 else 'clockwise'} by {_arg_str(abs(t2))}) (A1). (d) n × {_arg_str(t2)} must be a multiple of 2π (M1): n = {_least_n(t2)} (A1).',
               8, 'multi_step', gap='G5')


def ee(r, t):
    """r e^(iθ) written IB-style, e.g. 2e^(−iπ/6)."""
    a = _arg_str(abs(t))
    return f'{r}e^({MINUS if t < 0 else ""}i{a})' if 'π' in a else f'{r}e^({m(sf(t))}i)'


def phs(t):
    """'+ π/3' or '− 0.5' for a phase inside sin(ωt …)."""
    return ('− ' if t < 0 else '+ ') + _arg_str(abs(t))


def _least_n(t):
    for n in range(1, 200):
        if abs((n * t / (2 * math.pi)) - round(n * t / (2 * math.pi))) < 1e-9:
            return n
    return 0


R.facts('ch05-st3', F(
    terms=[('impedance', 'the complex quantity Z = V/I describing the opposition of a circuit element to alternating current: R for a resistor, iωL for an inductor, 1/(iωC) for a capacitor'),
           ('phasor', 'a complex number Ae^(iφ) representing the amplitude and phase of a sinusoid A cos(ωt + φ)'),
           ('phase shift', 'the horizontal displacement φ of a sinusoid relative to a reference wave of the same frequency')],
    facts=[('Two sinusoidal voltages of the same frequency are added. What is true of the result?', 'It is a sinusoid with the same frequency', ['It has double the frequency', 'It is never sinusoidal', 'Its amplitude is always the sum of the amplitudes'], 'Adding phasors gives a single phasor at the same ω.'),
           ('In a series AC circuit, how are the impedances of the components combined?', 'They are added as complex numbers', ['Their moduli are added', 'They are multiplied', 'Their reciprocals are added'], 'Series: Z = Z₁ + Z₂ + … (complex sum).')],
    why=[('Explain why complex numbers simplify the addition of two sinusoidal voltages of the same frequency.', 'Each sinusoid A cos(ωt + φ) is the real part of Ae^(iφ)e^(iωt); adding them only requires adding the phasors Ae^(iφ), a single complex addition, then reading off the modulus (amplitude) and argument (phase).'),
         ('Explain why the amplitude of the sum of two sinusoids can be less than either amplitude.', 'If the phase difference is near π, the waves are nearly opposite, so they partly cancel: |A + Be^(iφ)| can be as small as |A − B|.')],
    misc=[('Adding 3 sin(ωt) and 4 sin(ωt + π/2) gives a wave of amplitude 7.', 'Amplitudes add as complex numbers: |3 + 4i| = 5, not 7, because the waves are out of phase.')],
))


@R.add('ch05-st3', ALL, (1, 5), 'short')
def ac_core(rng, slot):
    c, d = slot.c, slot.d
    A, B = rng.randint(2, 12), rng.randint(2, 12)
    phi = pick(rng, [math.pi / 6, math.pi / 4, math.pi / 3, math.pi / 2, 2 * math.pi / 3, 3 * math.pi / 4, -math.pi / 3, -math.pi / 4, round(rng.uniform(0.2, 2.8), 2)])
    w = rng.choice([50, 60, 100, 120, 314])
    S = A + B * complex(math.cos(phi), math.sin(phi))
    amp, ph = abs(S), math.atan2(S.imag, S.real)
    fn_ = pick(rng, ['sin', 'cos'])
    if c == 'C1':
        if rng.random() < 0.5:
            return ret(f'Write down the phasor (in the form Ae^(iφ)) that represents the voltage V = {B} {fn_}({w}t {phs(phi)}).', f'{ee(B, phi)}',
                       f'Amplitude {B} and phase {_arg_str(phi)} (A1 A1).', 2)
        Rr, Lw = rng.randint(5, 80), rng.randint(5, 80)
        Z = complex(Rr, Lw)
        return ret(f'A resistor of {Rr} Ω is in series with an inductor of reactance {Lw} Ω. Write down the total impedance in Cartesian form and find its modulus.', f'Z = {Rr} + {Lw}i Ω, |Z| = {sf(abs(Z))} Ω',
                   f'Z = {Rr} + {Lw}i (A1); |Z| = √({Rr}² + {Lw}²) = {sf(abs(Z))} Ω (A1).', 2)
    if c == 'C2':
        return ret(f'Explain why {A} {fn_}({w}t) + {B} {fn_}({w}t {phs(phi)}) can be written as a single wave R {fn_}({w}t + θ), and explain why R is not {A + B}.',
                   f'R = {sf(amp)}, θ = {m(sf(ph))}', f'R1 both are imaginary/real parts of phasors × e^({w}it), so the sum is (phasor sum) × e^({w}it) with the same frequency; '
                   f'R1 amplitudes combine as |{A} + {ee(B, phi)}| = {sf(amp)} (A1), equal to {A + B} only if the waves are in phase.', 3, 'explain')
    if c == 'C3':
        if rng.random() < 0.55:
            return ret(f'Two alternating voltages in a circuit are V₁ = {A} {fn_}({w}t) and V₂ = {B} {fn_}({w}t {phs(phi)}). Use complex numbers to write V₁ + V₂ in the form R {fn_}({w}t + θ), with θ in radians.',
                       f'{sf(amp)} {fn_}({w}t {"+" if ph >= 0 else "−"} {sf(abs(ph))})', f'Phasors {A} and {ee(B, phi)} (M1); sum {cx(S, False)} (A1); R = {sf(amp)} (A1); θ = {m(sf(ph))} (A1).', 4, 'numerical')
        V = rng.randint(10, 240)
        Rr, XL, XC = rng.randint(10, 90), rng.randint(10, 90), rng.randint(5, 60)
        Z = complex(Rr, XL - XC)
        I = V / Z
        return ret(f'A series circuit contains a resistor of {Rr} Ω, an inductor of reactance {XL} Ω and a capacitor of reactance {XC} Ω (impedance −{XC}i Ω). The supply voltage is represented by V = {V} V (phase 0). '
                   f'Find (a) the total impedance; (b) the current I = V/Z in the form re^(iθ).', f'(a) {cx(Z)} Ω (b) {sf(abs(I))}e^({m(sf(math.atan2(I.imag, I.real)))}i) A',
                   f'(a) Z = {Rr} + {XL}i − {XC}i = {cx(Z)} (A1). (b) I = {V}/({cx(Z)}) (M1); |I| = {sf(abs(I))} A (A1); arg I = {m(sf(math.atan2(I.imag, I.real)))} (A1).', 4, 'numerical')
    C_ = rng.randint(2, 10)
    phi2 = pick(rng, [math.pi / 2, -math.pi / 2, math.pi / 3, -2 * math.pi / 3, math.pi])
    S3 = S + C_ * complex(math.cos(phi2), math.sin(phi2))
    return ret(f'Three signals of the same frequency are combined: {A} sin({w}t), {B} sin({w}t {phs(phi)}) and {C_} sin({w}t {phs(phi2)}). '
               f'(a) Represent each as a complex number and find their sum in Cartesian form. (b) Hence write the combined signal as R sin({w}t + θ). (c) Find the first positive time t at which the combined signal reaches its maximum. '
               f'(d) Explain why the third signal reduces or increases the amplitude compared with the first two alone.',
               f'(a) {cx(S3, False)} (b) {sf(abs(S3))} sin({w}t {"+" if math.atan2(S3.imag, S3.real) >= 0 else "−"} {sf(abs(math.atan2(S3.imag, S3.real)))}) (c) t = {sf(((math.pi / 2 - math.atan2(S3.imag, S3.real)) % (2 * math.pi)) / w)}',
               f'(a) phasors {A}, {ee(B, phi)}, {ee(C_, phi2)} (M1); sum {cx(S3, False)} (A1 A1). (b) R = {sf(abs(S3))} (A1), θ = {m(sf(math.atan2(S3.imag, S3.real)))} (A1). '
               f'(c) {w}t + θ = π/2 (M1) ⇒ t = {sf(((math.pi / 2 - math.atan2(S3.imag, S3.real)) % (2 * math.pi)) / w)} (A1). (d) R1 compare {sf(abs(S3))} with {sf(amp)}: the third phasor {"partly cancels" if abs(S3) < amp else "reinforces"} the sum of the first two.',
               9, 'multi_step', gap='G5')


# =============================================================================================
# ch06 Matrices
# =============================================================================================
def mat(M):
    M = np.array(M)
    rows = []
    for r in M:
        rows.append(', '.join(m(_num(float(v))) for v in r))
    return '[' + '; '.join(rows) + ']'


R.facts('ch06-st1', F(
    terms=[('order of a matrix', 'the number of rows × the number of columns, m × n'),
           ('identity matrix', 'the square matrix I with 1s on the leading diagonal and 0s elsewhere, so AI = IA = A'),
           ('zero matrix', 'a matrix whose entries are all 0, the identity for matrix addition')],
    facts=[('A is 2 × 3 and B is 3 × 4. What is the order of AB?', '2 × 4', ['3 × 3', '4 × 2', 'AB is not defined'], 'Inner orders match (3); the result takes the outer orders.'),
           ('Which statement about matrix multiplication is true in general?', 'AB ≠ BA', ['AB = BA', 'AB is always defined if BA is', 'A(B + C) ≠ AB + AC'], 'Matrix multiplication is not commutative.'),
           ('Matrix A is 3 × 2. Which product is always defined?', 'AAᵀ (A times its transpose)', ['A²', 'A × A × A', 'A + Aᵀ'], 'A (3 × 2) × Aᵀ (2 × 3) is defined; A² needs a square matrix.')],
    why=[('Explain why a matrix product AB is only defined when the number of columns of A equals the number of rows of B.', 'Each entry of AB is the sum of products of a row of A with a column of B; this requires the row and column to have the same number of entries.'),
         ('Explain why matrices are useful for combining sales data with prices.', 'A quantities matrix multiplied by a price column computes every revenue total (sum of quantity × price) in a single operation.')],
    misc=[('To multiply two matrices you multiply corresponding entries.', 'That is the element-wise (Hadamard) product; matrix multiplication combines rows of the first with columns of the second.')],
))


def lin3(row, v=('x', 'y', 'z')):
    out = []
    for cf, var in zip(row, v):
        cf = int(cf)
        if cf == 0:
            continue
        mag = '' if abs(cf) == 1 else str(abs(cf))
        if not out:
            out.append((MINUS if cf < 0 else '') + mag + var)
        else:
            out.append(('− ' if cf < 0 else '+ ') + mag + var)
    return ' '.join(out) or '0'


def _rmat(rng, r, c, lo=-5, hi=9):
    return np.array([[rng.randint(lo, hi) for _ in range(c)] for _ in range(r)])


@R.add('ch06-st1', ALL, (1, 5), 'short')
def matops_core(rng, slot):
    c, d = slot.c, slot.d
    if c == 'C1':
        A, B = _rmat(rng, 2, 2), _rmat(rng, 2, 2)
        k = rng.randint(2, 5)
        if rng.random() < 0.5:
            V = A + k * B
            return ret(f'Given A = {mat(A)} and B = {mat(B)} (rows separated by semicolons), find A + {k}B.', mat(V), f'{k}B = {mat(k * B)} (M1); A + {k}B = {mat(V)} (A1).', 2)
        p, q, r = rng.randint(1, 4), rng.randint(1, 4), rng.randint(1, 4)
        ok = q == rng.choice([q, q, r])
        q2 = q if ok else r
        if q2 == q:
            return mcq(rng, f'A is a {p} × {q} matrix and B is a {q} × {r} matrix. What is the order of AB?', f'{p} × {r}', [f'{q} × {q}', f'{r} × {p}', f'{p} × {q}' if q != r else f'{p + 1} × {r}'],
                       'Number of rows of A by number of columns of B.')
        return None
    if c == 'C2':
        A, B = _rmat(rng, 2, 2, -3, 6), _rmat(rng, 2, 2, -3, 6)
        AB, BA = A @ B, B @ A
        return ret(f'For A = {mat(A)} and B = {mat(B)}, find AB and BA, and comment on what this shows about matrix multiplication.', f'AB = {mat(AB)}, BA = {mat(BA)}',
                   f'AB = {mat(AB)} (A1); BA = {mat(BA)} (A1); R1 {"AB ≠ BA: matrix multiplication is not commutative in general" if not np.array_equal(AB, BA) else "here AB = BA, but this is a special case; in general AB ≠ BA"}.', 3, 'explain')
    shops = rng.sample(['Lisbon', 'Porto', 'Faro', 'Braga', 'Coimbra'], 3) if rng.random() < 0.5 else rng.sample(['Kyoto', 'Osaka', 'Nagoya', 'Kobe', 'Sapporo'], 3)
    items = rng.sample(['coffee', 'tea', 'juice', 'smoothie', 'cake', 'sandwich'], 3)
    Q = _rmat(rng, 3, 3, 20, 120)
    P = np.array([round(rng.uniform(1.5, 6.5), 2) for _ in range(3)])
    Rv = Q @ P
    cc = cur(rng)
    if c == 'C3':
        return ret(f'A café chain records daily sales in shops in {", ".join(shops)} (rows) of {", ".join(items)} (columns) as Q = {mat(Q)}. The prices in {cc} are given by the column vector P = ({", ".join(f"{p:.2f}" for p in P)}). '
                   f'Find QP and interpret its entries.', 'QP = (' + ', '.join(money(v) for v in Rv) + ')',
                   f'Row × column products (M1); QP = (' + ', '.join(money(v) for v in Rv) + f') (A1 A1); R1 each entry is the daily revenue of one shop, in {cc}.', 4, 'numerical')
    cost = np.array([round(p * rng.uniform(0.3, 0.6), 2) for p in P])
    prof = Q @ (P - cost)
    days = rng.randint(5, 7)
    return ret(f'Daily sales of {", ".join(items)} (columns) in shops in {", ".join(shops)} (rows) are Q = {mat(Q)}. Selling prices are P = ({", ".join(f"{p:.2f}" for p in P)}) and costs C = ({", ".join(f"{p:.2f}" for p in cost)}) in {cc} per item. '
               f'(a) Find Q(P − C) and explain what it represents. (b) Find the total profit of the chain over {days} days. (c) Explain why Q(P − C) = QP − QC.',
               f'(a) (' + ', '.join(money(v) for v in prof) + f') (b) {money(days * prof.sum())} (c) distributive law',
               f'(a) P − C = ({", ".join(f"{p:.2f}" for p in P - cost)}) (A1); Q(P − C) (M1) = (' + ', '.join(money(v) for v in prof) + f') (A1); R1 daily profit of each shop. '
               f'(b) {days} × sum of entries (M1) = {money(days * prof.sum())} (A1). (c) R1 matrix multiplication distributes over addition/subtraction.', 7, 'multi_step', gap='G5')


R.facts('ch06-st2', F(
    terms=[('determinant', 'for A = [a, b; c, d], det A = ad − bc; it is zero exactly when A has no inverse'),
           ('inverse matrix', 'the matrix A⁻¹ with AA⁻¹ = A⁻¹A = I; for 2 × 2, A⁻¹ = (1/det A)[d, −b; −c, a]'),
           ('singular matrix', 'a square matrix with determinant 0, which has no inverse')],
    facts=[('What is the determinant of [4, 3; 2, 5]?', '14', ['26', '−14', '7'], '4 × 5 − 3 × 2 = 14.'),
           ('If AX = B and A is invertible, which is X?', 'A⁻¹B', ['BA⁻¹', 'B/A', 'AB⁻¹'], 'Pre-multiply both sides by A⁻¹; order matters.'),
           ('For which value of k is [k, 2; 3, 6] singular?', '1', ['2', '4', '0'], '6k − 6 = 0 ⇒ k = 1.')],
    why=[('Explain why a system of equations AX = B has a unique solution when det A ≠ 0.', 'If det A ≠ 0 then A⁻¹ exists and X = A⁻¹B is the only solution; geometrically the lines/planes meet at a single point.'),
         ('Explain why X = A⁻¹B and not X = BA⁻¹ when solving AX = B.', 'Matrix multiplication is not commutative; A⁻¹ must multiply from the left on both sides: A⁻¹AX = A⁻¹B gives IX = X.')],
    misc=[('If det A = 0 then A is the zero matrix.', 'Many non-zero matrices have determinant 0, e.g. [1, 2; 2, 4]; they are singular but not zero.')],
))


@R.add('ch06-st2', ALL, (1, 5), 'short')
def inverse_core(rng, slot):
    c, d = slot.c, slot.d
    A = _rmat(rng, 2, 2, -4, 9)
    det = int(round(np.linalg.det(A)))
    if det == 0:
        return None
    if c == 'C1':
        if d <= 1:
            return nmcq(rng, f'Find the determinant of the matrix {mat(A)}.', det, [A[0, 0] * A[1, 1] + A[0, 1] * A[1, 0], -det, A[0, 0] * A[0, 1] - A[1, 0] * A[1, 1]],
                        f'ad − bc = ({A[0, 0]})({A[1, 1]}) − ({A[0, 1]})({A[1, 0]}) = {det}.', fmtf=lambda z: m(_num(z)))
        adj = np.array([[A[1, 1], -A[0, 1]], [-A[1, 0], A[0, 0]]])
        return ret(f'Find the inverse of A = {mat(A)}.', f'(1/{m(det)}){mat(adj)}', f'det A = {m(det)} (A1); A⁻¹ = (1/{m(det)}){mat(adj)} (M1 A1).', 3)
    if c == 'C2':
        a, b, c0 = rng.randint(1, 6), rng.randint(-5, 6), rng.randint(1, 6)
        kk = a * c0 / b if b else None
        if not b or abs(kk - round(kk)) > 1e-9:
            return None
        kk = int(round(kk))
        return ret(f'The matrix M = [{a}, {m(b)}; k, {c0}]. Find the value of k for which M has no inverse, and explain what this means for the system M(x, y)ᵀ = (p, q)ᵀ.', f'k = {m(kk)}',
                   f'det M = {a * c0} − {b}k (M1) = 0 ⇒ k = {m(kk)} (A1); R1 the system then has either no solution or infinitely many (parallel or identical lines), never a unique solution.', 3, 'explain')
    if c == 'C3':
        Mx = _rmat(rng, 3, 3, -3, 6)
        if abs(np.linalg.det(Mx)) < 1:
            return None
        sol = np.array([rng.randint(-5, 8) for _ in range(3)])
        rhs = Mx @ sol
        eqs = '; '.join(lin3(Mx[r]) + f' = {m(rhs[r])}' for r in range(3))
        return ret(f'Write the system {eqs} in the form AX = B and use technology to solve it.', f'x = {m(sol[0])}, y = {m(sol[1])}, z = {m(sol[2])}',
                   f'A = {mat(Mx)}, B = ({", ".join(m(v_) for v_ in rhs)}) (A1); X = A⁻¹B (M1); x = {m(sol[0])}, y = {m(sol[1])}, z = {m(sol[2])} (A1 A1).', 4, 'numerical')
    # C4: coded messages / production planning
    prod = rng.sample(['tables', 'chairs', 'shelves', 'desks', 'cabinets'], 3)
    Mx = _rmat(rng, 3, 3, 1, 6)
    if abs(np.linalg.det(Mx)) < 1:
        return None
    sol = np.array([rng.randint(5, 40) for _ in range(3)])
    rhs = Mx @ sol
    return ret(f'A workshop in {pick(rng, CITIES)} makes {", ".join(prod)}. Each of the three products needs time in cutting, assembly and finishing, given by the matrix (rows: cutting, assembly, finishing; columns: {", ".join(prod)}, hours per item) '
               f'T = {mat(Mx)}. In one week {rhs[0]} h of cutting, {rhs[1]} h of assembly and {rhs[2]} h of finishing are used. (a) Write a matrix equation for the numbers of items made. (b) Find det T and explain why the equation has a unique solution. '
               f'(c) Find the number of each product made. (d) The workshop can increase finishing time by 10 h. Explain how T⁻¹ could be used to find the new production numbers.',
               f'(b) det T = {sf(np.linalg.det(Mx))} (c) {sol[0]} {prod[0]}, {sol[1]} {prod[1]}, {sol[2]} {prod[2]}',
               f'(a) T(a, b, c)ᵀ = ({rhs[0]}, {rhs[1]}, {rhs[2]})ᵀ (A1). (b) det T = {sf(np.linalg.det(Mx))} (A1) ≠ 0 so T⁻¹ exists (R1). (c) X = T⁻¹B (M1) = ({sol[0]}, {sol[1]}, {sol[2]}) (A1 A1). '
               f'(d) R1 new X = T⁻¹(B + (0, 0, 10)ᵀ), i.e. add 10 × (third column of T⁻¹) to the current solution.', 8, 'multi_step', gap='G5')


R.facts('ch06-st3', F(
    terms=[('eigenvalue', 'a scalar λ for which Av = λv has a non-zero solution v; found from det(A − λI) = 0'),
           ('eigenvector', 'a non-zero vector v whose direction is unchanged by A: Av = λv'),
           ('characteristic polynomial', 'det(A − λI), whose roots are the eigenvalues of A'),
           ('diagonalisation', 'writing A = PDP⁻¹ with D diagonal (eigenvalues) and P having eigenvectors as columns, so Aⁿ = PDⁿP⁻¹')],
    facts=[('If λ = 3 is an eigenvalue of A with eigenvector v, what is A²v?', '9v', ['3v', '6v', 'v'], 'A²v = A(3v) = 3Av = 9v.'),
           ('What is the sum of the eigenvalues of a 2 × 2 matrix equal to?', 'its trace (sum of the leading diagonal)', ['its determinant', '0', 'the sum of all entries'], 'For λ² − (tr A)λ + det A = 0 the roots sum to tr A.'),
           ('A transition matrix of a regular Markov chain always has which eigenvalue?', '1', ['0', '−1', '2'], 'The steady state is the eigenvector for λ = 1.')],
    why=[('Explain why diagonalisation makes it easy to compute a high power of a matrix.', 'If A = PDP⁻¹ then Aⁿ = PDⁿP⁻¹ because the inner P⁻¹P products cancel; Dⁿ is found by raising each diagonal entry to the power n.'),
         ('Explain why the long-term behaviour of xₙ = Aⁿx₀ is dominated by the eigenvalue with the largest modulus.', 'Writing x₀ as a combination of eigenvectors, Aⁿx₀ = c₁λ₁ⁿv₁ + c₂λ₂ⁿv₂; the term with the largest |λ| grows fastest (or decays slowest) and eventually dominates.')],
    misc=[('Any non-zero vector is an eigenvector of A because A times a vector gives a vector.', 'An eigenvector must satisfy Av = λv: its image is parallel to v. Most vectors change direction under A.')],
))


def _eig_matrix(rng):
    """2×2 integer matrix with distinct integer eigenvalues and integer eigenvectors."""
    for _ in range(50):
        l1, l2 = rng.sample([-3, -2, -1, 1, 2, 3, 4, 5, 6], 2)
        p = np.array([[1, rng.choice([1, 2, -1, 3])], [rng.choice([-2, -1, 0, 1, 2, 3]), 1]])
        if abs(round(np.linalg.det(p))) != 1:
            continue
        A = p @ np.diag([l1, l2]) @ np.linalg.inv(p)
        if np.allclose(A, np.round(A)):
            return np.round(A).astype(int), (l1, l2), p
    return None


@R.add('ch06-st3', ALL, (1, 5), 'short')
def eigen_core(rng, slot):
    c, d = slot.c, slot.d
    res = _eig_matrix(rng)
    if res is None:
        return None
    A, (l1, l2), P = res
    v1, v2 = P[:, 0], P[:, 1]
    tr, det = int(A[0, 0] + A[1, 1]), int(round(np.linalg.det(A)))
    cp = f'λ² {sgn(-tr)}λ {sgn(det)}'.replace(' 1λ', ' λ').replace('+ 0λ ', '')
    if c == 'C1':
        if d <= 1:
            return mcq(rng, f'Which is the characteristic polynomial of A = {mat(A)}?', cp, [f'λ² {sgn(tr)}λ {sgn(det)}'.replace(' 1λ', ' λ'), f'λ² {sgn(-tr)}λ {sgn(-det)}'.replace(' 1λ', ' λ'), f'λ² {sgn(-det)}λ {sgn(tr)}'.replace(' 1λ', ' λ')],
                       f'det(A − λI) = λ² − (trace)λ + det = {cp}.')
        return ret(f'Find the eigenvalues of A = {mat(A)}.', f'λ = {m(min(l1, l2))}, {m(max(l1, l2))}', f'det(A − λI) = {cp} = 0 (M1)(A1); λ = {m(min(l1, l2))}, {m(max(l1, l2))} (A1).', 3)
    if c == 'C2':
        return ret(f'Show that v = ({m(v1[0])}, {m(v1[1])})ᵀ is an eigenvector of A = {mat(A)} and state the corresponding eigenvalue. Explain the geometric meaning of this result.', f'λ = {m(l1)}',
                   f'Av = ({m(int(A[0] @ v1))}, {m(int(A[1] @ v1))})ᵀ (M1) = {m(l1)}v (A1); R1 A maps every point on the line through the origin in the direction of v to the same line, scaled by factor {m(l1)}.', 3, 'explain')
    if c == 'C3':
        return ret(f'For A = {mat(A)}, find the eigenvalues and a corresponding eigenvector for each.', f'λ = {m(l1)}: ({m(v1[0])}, {m(v1[1])})ᵀ; λ = {m(l2)}: ({m(v2[0])}, {m(v2[1])})ᵀ (or any non-zero multiples)',
                   f'{cp} = 0 (M1) ⇒ λ = {m(l1)}, {m(l2)} (A1); (A − {m(l1)}I)v = 0 gives ({m(v1[0])}, {m(v1[1])}) (A1); (A − {m(l2)}I)v = 0 gives ({m(v2[0])}, {m(v2[1])}) (A1).', 5, 'numerical')
    n = rng.randint(4, 8)
    An = np.round(np.linalg.matrix_power(A, n)).astype(int)
    D = np.diag([l1, l2])
    return ret(f'Let A = {mat(A)}. (a) Find the eigenvalues and corresponding eigenvectors of A. (b) Hence write A in the form PDP⁻¹, where D is diagonal. (c) Use your answer to find A{sup(n)}. '
               f'(d) Explain why A{sup(n)} = PD{sup(n)}P⁻¹.',
               f'(a) λ = {m(l1)}, ({m(v1[0])}, {m(v1[1])}); λ = {m(l2)}, ({m(v2[0])}, {m(v2[1])}) (b) P = {mat(P)}, D = {mat(D)} (c) {mat(An)}',
               f'(a) M1 A1 A1 A1. (b) P = {mat(P)}, D = {mat(D)}, P⁻¹ = {mat(np.round(np.linalg.inv(P)).astype(int))} (A1 A1). (c) PD{sup(n)}P⁻¹ with D{sup(n)} = {mat(np.diag([l1 ** n, l2 ** n]))} (M1) = {mat(An)} (A1). '
               f'(d) R1 Aⁿ = (PDP⁻¹)(PDP⁻¹)…(PDP⁻¹) and each P⁻¹P = I.', 10, 'multi_step', gap='G5')


@R.add('ch06-st3', ('C3', 'C4'), (2, 5), 'multi_step')
def eigen_pop(rng, slot):
    p = rng.choice([0.05, 0.08, 0.1, 0.12, 0.15, 0.2])
    q = rng.choice([0.04, 0.06, 0.1, 0.15, 0.25, 0.3])
    T = np.array([[1 - p, q], [p, 1 - q]])
    ss = np.array([q, p]) / (p + q)
    N = rng.randint(20, 90) * 100
    a0 = rng.randint(int(0.2 * N), int(0.8 * N))
    x0 = np.array([a0, N - a0])
    k = rng.randint(2, 6)
    xk = np.linalg.matrix_power(T, k) @ x0
    grp, A_, B_ = pick(rng, [('commuters', 'travel by bus', 'cycle'), ('shoppers', 'buy brand A', 'buy brand B'), ('students', 'live on the north campus', 'live on the south campus'),
                             ('residents', 'live in the city', 'live in the suburbs'), ('members', 'use the gym', 'use the pool')])
    l2 = 1 - p - q
    if slot.c == 'C3':
        return ret(f'Each year {int(p * 100)}% of {grp} who {A_} switch so that they {B_}, and {int(q * 100)}% of those who {B_} switch so that they {A_}. Initially {a0} {grp} {A_} and {N - a0} {B_}. '
                   f'Using the transition matrix T = {mat(T)}, find the numbers in each group after {k} years.', f'{sf(xk[0])} and {sf(xk[1])}',
                   f'T{sup(k)} × ({a0}, {N - a0})ᵀ (M1)(A1) = ({sf(xk[0])}, {sf(xk[1])}) (A1).', 3, 'numerical')
    return ret(f'Each year {int(p * 100)}% of {grp} who {A_} change so that they {B_}, and {int(q * 100)}% of those who {B_} change so that they {A_}; the total of {N} {grp} is constant. '
               f'(a) Write down the transition matrix T. (b) Show that the eigenvalues of T are 1 and {_num(l2)}. (c) Find the eigenvector for λ = 1 and hence the long-term numbers using each. '
               f'(d) Explain, using the second eigenvalue, why the numbers approach this steady state.',
               f'(a) {mat(T)} (c) ({sf(ss[0] * N)}, {sf(ss[1] * N)}) (d) |{_num(l2)}| < 1 so {_num(l2)}ⁿ → 0',
               f'(a) A1. (b) det(T − λI) = λ² − {_num(2 - p - q)}λ + {_num(1 - p - q)} (M1) = (λ − 1)(λ − {_num(l2)}) (A1, AG). (c) (T − I)v = 0 ⇒ v ∝ ({_num(q)}, {_num(p)}) (M1 A1); '
               f'scale to total {N}: ({sf(ss[0] * N)}, {sf(ss[1] * N)}) (A1). (d) R1 xₙ = c₁(1)ⁿv₁ + c₂({_num(l2)})ⁿv₂ and the second term decays to 0.', 9, 'multi_step', gap='G5')


# =============================================================================================
# ch07 Functions and linear models
# =============================================================================================
def frs(q):
    from fractions import Fraction
    q = Fraction(q).limit_denominator(1000)
    return m(str(q.numerator)) if q.denominator == 1 else m(f'{q.numerator}/{q.denominator}')


def line_eq(mg, c):
    """y = mx + c with fractions."""
    from fractions import Fraction
    mg, c = Fraction(mg).limit_denominator(1000), Fraction(c).limit_denominator(1000)
    ms = '' if mg == 1 else MINUS if mg == -1 else (frs(mg) if mg.denominator == 1 else f'({frs(mg)})')
    s = f'y = {ms}x' if mg != 0 else 'y = '
    if c != 0 or mg == 0:
        s += (f' {"−" if c < 0 else "+"} {frs(abs(c))}' if mg != 0 else frs(c))
    return s


R.facts('ch07-st1', F(
    terms=[('gradient', 'the rate of change of y with respect to x for a straight line, m = (y₂ − y₁)/(x₂ − x₁)'),
           ('y-intercept', 'the value of y where a graph crosses the y-axis, i.e. at x = 0'),
           ('perpendicular lines', 'lines meeting at right angles; their gradients satisfy m₁ × m₂ = −1'),
           ('general form of a line', 'ax + by + d = 0 with a, b, d integers')],
    facts=[('A line has gradient 2/3. What is the gradient of a line perpendicular to it?', '−3/2', ['3/2', '−2/3', '2/3'], 'Negative reciprocal.'),
           ('Which line is parallel to y = 4x − 7?', 'y = 4x + 2', ['y = −4x − 7', 'y = −x/4 + 1', 'y = 7x − 4'], 'Parallel lines have equal gradients.'),
           ('What is the gradient of the line 3x + 2y − 6 = 0?', '−3/2', ['3/2', '3', '−3'], 'Rearrange: y = −(3/2)x + 3.')],
    why=[('Explain why the gradients of two perpendicular lines (neither vertical) multiply to −1.', 'Rotating a line by 90° turns a run of 1 and rise of m into a run of −m and rise of 1, so the new gradient is −1/m.'),
         ('Explain why a vertical line has no gradient defined, using m = (y₂ − y₁)/(x₂ − x₁).', 'All points on a vertical line have the same x, so x₂ − x₁ = 0 and the division is undefined.')],
    misc=[('The gradient of the line through (2, 5) and (6, 3) is (6 − 2)/(3 − 5) = −2.', 'Gradient is change in y over change in x: (3 − 5)/(6 − 2) = −1/2.')],
))


@R.add('ch07-st1', ALL, (1, 5), 'short')
def lines_core(rng, slot):
    c, d = slot.c, slot.d
    x1, y1 = rng.randint(-6, 6), rng.randint(-6, 8)
    dx, dy = rng.choice([1, 2, 3, 4, -2, -3, 5]), rng.choice([-6, -4, -3, -2, -1, 1, 2, 3, 5, 6])
    x2, y2 = x1 + dx, y1 + dy
    from fractions import Fraction
    mg = Fraction(dy, dx)
    cc = Fraction(y1) - mg * x1
    if c == 'C1':
        if d <= 1:
            return mcq(rng, f'Find the gradient of the line through ({m(x1)}, {m(y1)}) and ({m(x2)}, {m(y2)}).', frs(mg), [frs(1 / mg), frs(-mg), frs(-1 / mg)] if abs(mg) != 1 else [frs(mg * 2), frs(-mg), '0'],
                       f'm = ({m(y2)} − {m(y1)})/({m(x2)} − {m(x1)}) = {frs(mg)}.')
        return ret(f'Find the equation of the line through ({m(x1)}, {m(y1)}) and ({m(x2)}, {m(y2)}) in the form y = mx + c.', line_eq(mg, cc),
                   f'm = {frs(mg)} (A1); substitute a point (M1); {line_eq(mg, cc)} (A1).', 3)
    if c == 'C2':
        mp = -1 / mg
        return ret(f'Line L₁ passes through ({m(x1)}, {m(y1)}) and ({m(x2)}, {m(y2)}). Line L₂ has gradient {frs(mp)}. Explain how you know that L₂ is perpendicular to L₁.', 'm₁ × m₂ = −1',
                   f'm₁ = {frs(mg)} (A1); {frs(mg)} × {frs(mp)} = −1 (M1); R1 gradients of perpendicular lines are negative reciprocals.', 3, 'explain')
    px, py = rng.randint(-5, 7), rng.randint(-5, 7)
    mp = -1 / mg
    cp = Fraction(py) - mp * px
    if c == 'C3':
        # perpendicular through point in general form
        a_, b_ = mp.denominator, -mp.numerator  # y = mp x + cp  ->  mp.num x − mp.den y + cp*den = 0
        A_, B_, D_ = mp.numerator, -mp.denominator, cp * mp.denominator
        if A_ < 0:
            A_, B_, D_ = -A_, -B_, -D_
        gen = f'{"" if A_ == 1 else A_}x {"−" if B_ < 0 else "+"} {"" if abs(B_) == 1 else abs(B_)}y {"−" if D_ < 0 else "+"} {frs(abs(D_))} = 0'.replace(' + 0 = 0', ' = 0').replace(' − 0 = 0', ' = 0')
        return ret(f'Find the equation of the line perpendicular to the line through ({m(x1)}, {m(y1)}) and ({m(x2)}, {m(y2)}) that passes through ({m(px)}, {m(py)}). Give your answer in the form ax + by + d = 0, where a, b, d ∈ ℤ.',
                   gen, f'm = {frs(mg)} (A1); perpendicular gradient {frs(mp)} (A1); y {sgn(-py)} = {frs(mp)}(x {sgn(-px)}) (M1); {gen} (A1).', 4, 'numerical')
    # C4: intersection of two lines in context (break-even) or triangle area
    fixed1, var1 = rng.randint(20, 80), round(rng.uniform(0.8, 3.5), 2)
    fixed2, var2 = rng.randint(0, 15), round(var1 + rng.uniform(0.6, 2.5), 2)
    xb = (fixed1 - fixed2) / (var2 - var1)
    cc_ = cur(rng)
    svc = pick(rng, [('a car-sharing club', 'km'), ('an electricity supplier', 'kWh × 10'), ('a printing service', 'pages × 10'), ('a mobile data plan', 'GB'), ('a bike-hire scheme', 'hours')])
    return ret(f'Two tariffs for {svc[0]}: Plan A costs {fixed1} {cc_} per month plus {var1:.2f} {cc_} per unit; Plan B costs {fixed2} {cc_} per month plus {var2:.2f} {cc_} per unit (units: {svc[1]}). '
               f'(a) Write down an equation for the monthly cost C of each plan in terms of the number of units x. (b) Find the value of x at which the plans cost the same. (c) Interpret the gradient of each line. '
               f'(d) Advise a customer who expects to use about {round(xb * rng.choice([0.5, 1.6]))} units per month.',
               f'(a) C_A = {var1:.2f}x + {fixed1}, C_B = {var2:.2f}x + {fixed2} (b) x = {sf(xb)} (c) cost per extra unit (d) see key',
               f'(a) A1 A1. (b) {var1:.2f}x + {fixed1} = {var2:.2f}x + {fixed2} (M1) ⇒ x = {sf(xb)} (A1). (c) R1 the gradient is the cost in {cc_} of each additional unit. '
               f'(d) R1 below {sf(xb)} units plan B is cheaper, above it plan A is cheaper.', 7, 'multi_step', gap='G5')


R.facts('ch07-st2', F(
    terms=[('domain', 'the set of input values x for which a function is defined (or which are allowed in the context)'),
           ('range', 'the set of output values f(x) produced by the domain'),
           ('inverse function', 'f⁻¹, the function that reverses f, so that f⁻¹(f(x)) = x; its graph is the reflection of y = f(x) in y = x'),
           ('mapping notation', 'writing a function as f : x ↦ f(x), e.g. f : x ↦ 3x − 1')],
    facts=[('The graph of y = f⁻¹(x) is a reflection of y = f(x) in which line?', 'y = x', ['y = −x', 'the x-axis', 'the y-axis'], 'Inverse swaps x and y.'),
           ('What is the domain of f(x) = √(x − 4)?', 'x ≥ 4', ['x > 4', 'x ≥ 0', 'all real x'], 'The square root needs a non-negative argument.'),
           ('What is the range of f(x) = x² + 3, x ∈ ℝ?', 'f(x) ≥ 3', ['f(x) > 3', 'f(x) ≥ 0', 'all real numbers'], 'x² ≥ 0 so x² + 3 ≥ 3.')],
    why=[('Explain why f(x) = x² with domain x ∈ ℝ has no inverse function, and how the domain can be restricted so that it does.', 'Two inputs (e.g. ±2) give the same output, so the reverse mapping is not a function (fails the horizontal line test); restricting to x ≥ 0 makes it one-to-one.'),
         ('Explain why the domain of a function in a real-life model is often smaller than the set of all real numbers.', 'Inputs such as time, length or number of items must be non-negative or whole numbers, and the model may only be valid for a limited range.')],
    misc=[('f⁻¹(x) means 1/f(x).', 'f⁻¹ denotes the inverse function, which undoes f; 1/f(x) is the reciprocal, written (f(x))⁻¹.')],
))


@R.add('ch07-st2', ALL, (1, 5), 'short')
def func_core(rng, slot):
    c, d = slot.c, slot.d
    a, b = rng.choice([2, 3, 4, 5, -2, -3, 0.5, 1.5]), rng.randint(-9, 12)
    k = rng.randint(-5, 8)
    if c == 'C1':
        fk = a * k + b
        if d <= 1:
            return nmcq(rng, f'Given f(x) = {_num(a) if a not in (1, -1) else ""}x {sgn(b)}, find f({m(k)}).', fk, [a + k + b, a * (k + b), a * k - b], f'f({m(k)}) = {_num(a)}({m(k)}) {sgn(b)} = {m(_num(fk))}.',
                        fmtf=lambda z: m(_num(z)))
        return ret(f'Given f : x ↦ {_num(a)}x {sgn(b)}, find f⁻¹(x) and f⁻¹({m(_num(fk))}).', f'f⁻¹(x) = (x {sgn(-b)})/{_num(a)}; f⁻¹({m(_num(fk))}) = {m(k)}',
                   f'Swap x and y and rearrange (M1); f⁻¹(x) = (x {sgn(-b)})/{_num(a)} (A1); {m(k)} (A1).', 3)
    if c == 'C2':
        h, kk = rng.randint(-4, 5), rng.randint(-6, 6)
        lo, hi = h - rng.randint(1, 4), h + rng.randint(1, 5)
        vals = [(x_ - h) ** 2 + kk for x_ in (lo, hi)]
        return ret(f'The function g(x) = (x {sgn(-h)})² {sgn(kk)} has domain {m(lo)} ≤ x ≤ {m(hi)}. Explain why the range is not simply found by substituting the end points, and find the range.',
                   f'{m(kk)} ≤ g(x) ≤ {m(max(vals))}', f'R1 the vertex ({m(h)}, {m(kk)}) lies inside the domain, so the minimum is {m(kk)}, not at an end point; g({m(lo)}) = {m(vals[0])}, g({m(hi)}) = {m(vals[1])} (A1); '
                   f'range {m(kk)} ≤ g(x) ≤ {m(max(vals))} (A1).', 3, 'explain')
    if c == 'C3':
        rate = round(rng.uniform(0.6, 1.6), 4)
        fee = rng.randint(2, 8)
        c1, c2 = rng.sample(['USD', 'EUR', 'GBP', 'CHF', 'CAD', 'SGD', 'AUD', 'NZD'], 2)
        amt = rng.randint(100, 900)
        got = rate * (amt - fee)
        return ret(f'A currency exchange in {pick(rng, CITIES)} converts {c1} to {c2}. It charges a fee of {fee} {c1}, then converts the rest at 1 {c1} = {rate} {c2}. (a) Write the amount received, R, as a function of the amount exchanged, x {c1}. '
                   f'(b) Find R({amt}). (c) Find R⁻¹(x) and explain what it represents.',
                   f'(a) R(x) = {rate}(x − {fee}) (b) {money(got)} {c2} (c) R⁻¹(x) = x/{rate} + {fee}',
                   f'(a) A1 A1. (b) {rate}({amt} − {fee}) = {money(got)} (A1). (c) M1 rearrange: R⁻¹(x) = x/{rate} + {fee} (A1); R1 the amount of {c1} needed to receive x {c2}.', 5, 'numerical')
    p, q = rng.randint(1, 6), rng.choice([1, 3, 4, 5, 6, 7, 8, 9])
    return ret(f'Let f(x) = {p}/(x − {q}) + 2, x ≠ {q}. (a) State the range of f. (b) Find f⁻¹(x) and state its domain. (c) Verify that f⁻¹(f({q + 2})) = {q + 2}. (d) Explain how the asymptotes of y = f(x) and y = f⁻¹(x) are related.',
               f'(a) y ≠ 2 (b) f⁻¹(x) = {p}/(x − 2) + {q}, x ≠ 2 (d) they are swapped (reflection in y = x)',
               f'(a) A1. (b) x = {p}/(y − {q}) + 2 (M1) ⇒ y = {p}/(x − 2) + {q} (A1), x ≠ 2 (A1). (c) f({q + 2}) = {_num(p / 2 + 2)} (A1), f⁻¹({_num(p / 2 + 2)}) = {q + 2} (A1). (d) R1 asymptotes x = {q}, y = 2 become x = 2, y = {q}.',
               7, 'multi_step', gap='G5')


@R.add('ch07-st2', ('C2', 'C3', 'C4'), (1, 5), 'short')
def func_ctx(rng, slot):
    kind = rng.randint(0, 3)
    if kind == 0:
        a, b = 100, round(rng.uniform(6, 15), 1)
        desc, var, out = f'The charge of a phone battery, B %, t hours after it is unplugged is modelled by B(t) = 100 − {b}t.', 't', 'B'
        f = lambda t: a - b * t
        top = a / b
        inv = f'B⁻¹(x) = (100 − x)/{b}'
        mean_inv = 'the time (hours) at which the charge is x %'
    elif kind == 1:
        v0, r = rng.randint(30, 80) * 1000, rng.randint(3, 8) * 500
        a, b = v0, r
        desc, var, out = f'The value of a machine t years after purchase is modelled by V(t) = {v0} − {r}t {cur(rng)}, until its value reaches zero.', 't', 'V'
        f = lambda t: v0 - r * t
        top = v0 / r
        inv = f'V⁻¹(x) = ({v0} − x)/{r}'
        mean_inv = 'the age (years) at which the machine is worth x'
    elif kind == 2:
        a, b = rng.randint(400, 900), rng.randint(15, 40)
        desc, var, out = f'A water tank holds {a} litres and is drained at {b} litres per minute, so the volume after t minutes is W(t) = {a} − {b}t.', 't', 'W'
        f = lambda t: a - b * t
        top = a / b
        inv = f'W⁻¹(x) = ({a} − x)/{b}'
        mean_inv = 'the time (minutes) at which x litres remain'
    else:
        a, b = rng.randint(5, 25), round(rng.uniform(0.8, 3.5), 2)
        top = rng.randint(20, 60)
        desc, var, out = f'A delivery company charges C(m) = {a} + {b:.2f}m {cur(rng)} to deliver a parcel of mass m kg, for parcels up to {top} kg.', 'm', 'C'
        f = lambda t: a + b * t
        inv = f'C⁻¹(x) = (x − {a})/{b:.2f}'
        mean_inv = 'the mass (kg) of a parcel whose delivery costs x'
    lo_r, hi_r = sorted([f(0), f(top)])
    if slot.c == 'C2':
        return ret(f'{desc} Explain why a suitable domain for this model is 0 ≤ {var} ≤ {sf(top)}, and state the corresponding range.', f'{sf(lo_r)} ≤ {out} ≤ {sf(hi_r)}',
                   f'R1 {var} cannot be negative{"; beyond " + sf(top) + " the model gives impossible (negative) values" if kind < 3 else "; the company only accepts parcels up to " + str(top) + " kg"}; A1 range {sf(lo_r)} ≤ {out} ≤ {sf(hi_r)}.', 2, 'explain')
    t0 = round(rng.uniform(0.2, 0.8) * top, 1)
    if slot.c == 'C3':
        return ret(f'{desc} (a) Find {out}({_num(t0)}). (b) State the domain and range of the model.', f'(a) {sf(f(t0), 4)} (b) 0 ≤ {var} ≤ {sf(top)}, {sf(lo_r)} ≤ {out} ≤ {sf(hi_r)}',
                   f'(a) {sf(f(t0), 4)} (A1). (b) domain (A1), range (A1).', 3, 'numerical')
    y0 = round(f(t0), 1)
    return ret(f'{desc} (a) State a suitable domain and the corresponding range. (b) Find the inverse function and explain what it represents. (c) Use the inverse to find {var} when {out} = {_num(y0)}. '
               f'(d) Sketch the function and its inverse on the same axes and describe their geometric relationship.',
               f'(a) 0 ≤ {var} ≤ {sf(top)}; {sf(lo_r)} ≤ {out} ≤ {sf(hi_r)} (b) {inv} (c) {sf((y0 - a) / b if kind == 3 else (a - y0) / b)} (d) reflections in y = x',
               f'(a) A1 A1. (b) M1 rearrange: {inv} (A1); R1 {mean_inv}. (c) A1 {sf((y0 - a) / b if kind == 3 else (a - y0) / b)}. (d) A1 both segments; R1 reflection in y = x, with domain and range interchanged.',
               8, 'multi_step', gap='G5')


R.facts('ch07-st3', F(
    terms=[('zero of a function', 'a value of x for which f(x) = 0; an x-intercept of the graph'),
           ('vertical asymptote', 'a line x = a which the graph approaches as y → ±∞'),
           ('local maximum', 'a point where the function value is greater than at all nearby points')],
    facts=[('To solve f(x) = g(x) with a GDC, what do you find?', 'the x-coordinates of the intersection points of y = f(x) and y = g(x)', ['the y-intercepts of both graphs', 'the zeros of f only', 'the maximum of f − g'], 'Equal y-values at the same x.'),
           ('What is the horizontal asymptote of y = 3 + 2/x?', 'y = 3', ['y = 2', 'x = 0', 'y = 0'], 'As x → ±∞, 2/x → 0.')],
    why=[('Explain why the solutions of f(x) = g(x) can be found as the zeros of h(x) = f(x) − g(x).', 'f(x) = g(x) exactly when f(x) − g(x) = 0, so the x-intercepts of h are the intersection x-values.'),
         ('Explain why an appropriate viewing window is important when sketching a graph with a GDC.', 'A poor window can hide intercepts, turning points or asymptotic behaviour; key features must be visible and labelled.')],
    misc=[('If a GDC graph appears to touch the x-axis then the function definitely has a zero there.', 'It may come very close without touching; zoom in or use the zero/solver function to confirm.')],
))


def _roots_num(f, lo, hi, n=4000):
    xs = np.linspace(lo, hi, n)
    ys = [f(x) for x in xs]
    out = []
    for i in range(n - 1):
        if ys[i] == 0:
            out.append(xs[i])
        elif ys[i] * ys[i + 1] < 0:
            out.append(bisect(f, xs[i], xs[i + 1], 80))
    return out


@R.add('ch07-st3', ALL, (1, 5), 'short')
def graph_core(rng, slot):
    c, d = slot.c, slot.d
    a, b, c0, e = rng.choice([1, -1, 0.5, 2, -0.5]), rng.randint(-4, 4), rng.randint(-6, 6), rng.randint(-8, 8)
    kind = rng.randint(0, 2)
    if kind == 0:
        f = lambda x: a * x ** 3 + b * x ** 2 + c0 * x + e
        fs = poly([a, b, c0, e])
    elif kind == 1:
        k_ = rng.randint(1, 3)
        f = lambda x: k_ * math.exp(0.5 * x) - rng_c if False else k_ * math.exp(0.5 * x) + b - 4
        fs = f'{k_ if k_ > 1 else ""}e^(0.5x) {sgn(b - 4)}' if b != 4 else f'{k_ if k_ > 1 else ""}e^(0.5x)'
    else:
        f = lambda x: 2 ** x - (c0 + 8) / (1 + x * x) if True else 0
        fs = f'2ˣ − {c0 + 8}/(1 + x²)' if c0 + 8 else '2ˣ'
    zs = _roots_num(f, -10, 10)
    if not zs:
        return None
    if c == 'C1':
        return ret(f'Use your GDC to find the zero{"s" if len(zs) > 1 else ""} of f(x) = {fs}, −10 ≤ x ≤ 10.', ', '.join(m(sf(z)) for z in zs),
                   f'x = ' + ', '.join(m(sf(z)) for z in zs) + ' (A1 for each; M1 for a correct graph/solver method).', 2)
    lin_a, lin_b = rng.choice([1, -1, 2, 0.5]), rng.randint(-5, 5)
    g = lambda x: lin_a * x + lin_b
    gs = f'{"" if lin_a == 1 else MINUS if lin_a == -1 else _num(lin_a)}x {sgn(lin_b)}' if lin_b else f'{"" if lin_a == 1 else MINUS if lin_a == -1 else _num(lin_a)}x'
    ints = _roots_num(lambda x: f(x) - g(x), -10, 10)
    if not ints:
        return None
    if c == 'C2':
        return ret(f'Explain how you would use a GDC to solve {fs} = {gs}, and state the number of solutions in −10 ≤ x ≤ 10.', f'{len(ints)} solution{"s" if len(ints) > 1 else ""}: x = ' + ', '.join(m(sf(z)) for z in ints),
                   f'R1 graph y = {fs} and y = {gs} (or y = {fs} − ({gs})) and find intersections (zeros); A1 number of solutions {len(ints)}; A1 values ' + ', '.join(m(sf(z)) for z in ints) + '.', 3, 'explain')
    if c == 'C3':
        return ret(f'Solve the equation {fs} = {gs} for −10 ≤ x ≤ 10, giving answers to 3 s.f.', ', '.join(m(sf(z)) for z in ints),
                   f'Intersection of graphs or solver (M1); x = ' + ', '.join(m(sf(z)) for z in ints) + ' (A1 each).', 2 + min(2, len(ints)), 'numerical')
    # C4 rational function features
    p, q, r_ = rng.randint(1, 6), rng.randint(-5, 5), rng.randint(-4, 4)
    while r_ == q or r_ == -q:
        r_ = rng.randint(-4, 4)
    hfun = lambda x: (p * x + r_) / (x - q)
    yint = r_ / -q if q else None
    xint = -r_ / p
    return ret(f'Let h(x) = ({p if p > 1 else ""}x {sgn(r_)})/(x {sgn(-q)}). (a) Write down the equations of the asymptotes of y = h(x). (b) Find the intercepts with the axes. (c) Sketch the graph for −10 ≤ x ≤ 10, labelling these features. '
               f'(d) Solve h(x) = {gs} for −10 ≤ x ≤ 10.'.replace('(x + 0)', 'x').replace('( x', '(x'),
               f'(a) x = {m(q)}, y = {p} (b) x-intercept {m(sf(xint))}' + (f', y-intercept {m(sf(yint))}' if q else '') + ' (d) ' + ', '.join(m(sf(z)) for z in _roots_num(lambda x: hfun(x) - g(x) if abs(x - q) > 1e-6 else 1e9, -10, 10) if abs(z - q) > 0.01),
               f'(a) x = {m(q)} (A1), y = {p} (A1). (b) ({m(sf(xint))}, 0) (A1)' + (f', (0, {m(sf(yint))}) (A1)' if q else '') + '. (c) correct shape in two branches (A1 A1). (d) GDC (M1): '
               + ', '.join(m(sf(z)) for z in _roots_num(lambda x: hfun(x) - g(x) if abs(x - q) > 1e-6 else 1e9, -10, 10) if abs(z - q) > 0.01) + ' (A1).', 8, 'multi_step', gap='G5')


R.facts('ch07-st4', F(
    terms=[('piecewise linear function', 'a function made of straight-line segments, each defined on its own interval of the domain'),
           ('rate of change', 'the change in the output per unit change in the input; for a linear model, its gradient, with units'),
           ('linear model', 'a function of the form f(x) = mx + c used to describe a quantity that changes at a constant rate')],
    facts=[('In the model C = 2.40 + 1.85d for a taxi fare C (EUR) and distance d (km), what does 1.85 represent?', 'the cost per kilometre, in EUR', ['the fixed starting charge', 'the total fare', 'the distance per euro'], 'The gradient is the rate: EUR per km.'),
           ('A piecewise model is continuous at a boundary x = a if…', 'both pieces give the same value at x = a', ['both pieces have the same gradient', 'one piece is horizontal', 'the domain excludes a'], 'The segments must meet.')],
    why=[('Explain why the units of the gradient of a distance-time graph are m s⁻¹.', 'Gradient = change in distance ÷ change in time, so its units are metres divided by seconds.'),
         ('Explain why income tax bands are modelled with a piecewise linear function.', 'Different rates apply to different portions of income; within each band tax grows at a constant rate, so the graph is linear on each interval with a different gradient.')],
    misc=[('Because a linear model fits data from 0 to 10 years, it can be used to predict the value after 50 years.', 'Extrapolating far outside the data range is unreliable; the rate of change may not stay constant.')],
))


@R.add('ch07-st4', ALL, (1, 5), 'short')
def piecewise_core(rng, slot):
    c, d = slot.c, slot.d
    cc = cur(rng)
    kind = rng.randint(0, 2)
    if kind == 0:  # water tariff
        b1, r1, r2 = rng.choice([10, 15, 20, 25]), round(rng.uniform(0.8, 2.0), 2), None
        r2 = round(r1 + rng.uniform(0.5, 2.0), 2)
        fixed = rng.randint(5, 20)
        desc = f'A water company in {city_for(rng, cc)} charges a fixed {fixed} {cc} per month, {r1:.2f} {cc} per m³ for the first {b1} m³, and {r2:.2f} {cc} per m³ for any further water.'
        f = lambda x: fixed + r1 * min(x, b1) + r2 * max(0, x - b1)
        unit, var = 'm³', 'w'
        piece = f'C(w) = {fixed} + {r1:.2f}w for 0 ≤ w ≤ {b1}; C(w) = {sf(fixed + r1 * b1, 4)} + {r2:.2f}(w − {b1}) for w > {b1}'
        bound = b1
        rates = (r1, r2)
    elif kind == 1:  # taxi
        flag, r1, b1, r2 = round(rng.uniform(2, 5), 2), round(rng.uniform(1.2, 2.5), 2), rng.choice([5, 8, 10]), None
        r2 = round(r1 - rng.uniform(0.2, 0.6), 2)
        desc = f'A taxi in {city_for(rng, cc)} charges {flag:.2f} {cc} plus {r1:.2f} {cc} per km for the first {b1} km and {r2:.2f} {cc} per km after that.'
        f = lambda x: flag + r1 * min(x, b1) + r2 * max(0, x - b1)
        unit, var = 'km', 'd'
        piece = f'C(d) = {flag:.2f} + {r1:.2f}d for 0 ≤ d ≤ {b1}; C(d) = {sf(flag + r1 * b1, 4)} + {r2:.2f}(d − {b1}) for d > {b1}'
        bound = b1
        rates = (r1, r2)
    else:  # tax
        allow, r1, b1, r2 = rng.randint(10, 15) * 1000, rng.choice([10, 15, 20]), rng.randint(40, 60) * 1000, rng.choice([30, 35, 40])
        desc = f'In a country, income up to {allow} {cc} is tax-free, income between {allow} and {b1} {cc} is taxed at {r1}%, and income above {b1} {cc} is taxed at {r2}%.'
        f = lambda x: r1 / 100 * max(0, min(x, b1) - allow) + r2 / 100 * max(0, x - b1)
        unit, var = cc, 'I'
        piece = f'T(I) = 0 for I ≤ {allow}; {r1 / 100:g}(I − {allow}) for {allow} < I ≤ {b1}; {sf(r1 / 100 * (b1 - allow), 5)} + {r2 / 100:g}(I − {b1}) for I > {b1}'
        bound = b1
        rates = (r1 / 100, r2 / 100)
    if kind == 2:
        x0 = rng.randint(b1 // 1000 + 5, b1 // 1000 + 60) * 1000
    else:
        x0 = rng.randint(bound + 1, bound * 3)
    fx = f(x0)
    if c == 'C1':
        x1 = rng.randint(1, bound) if kind != 2 else rng.randint(allow // 1000 + 1, b1 // 1000) * 1000
        return ret(f'{desc} Find the {"tax paid on an income" if kind == 2 else "cost"} of {x1} {unit if kind != 2 else cc}.', f'{money(f(x1))} {cc}',
                   f'Correct piece used (M1); {money(f(x1))} (A1).', 2)
    if c == 'C2':
        return ret(f'{desc} Explain why the graph of {"tax" if kind == 2 else "cost"} against {"income" if kind == 2 else "amount"} is piecewise linear, and interpret the gradient of each piece.',
                   f'gradients {rates[0]:g} and {rates[1]:g} {cc} per {unit if kind != 2 else cc}',
                   f'R1 within each band the {"tax" if kind == 2 else "charge"} increases at a constant rate; R1 the rate changes at {bound} {unit if kind != 2 else ""}; A1 gradients {rates[0]:g} and {rates[1]:g} are the extra {cc} per extra {unit if kind != 2 else cc}.', 3, 'explain')
    if c == 'C3':
        return ret(f'{desc} (a) Write down a piecewise function for the {"tax T" if kind == 2 else "cost C"}. (b) Find the {"tax on an income" if kind == 2 else "cost"} of {x0} {unit if kind != 2 else cc}.',
                   f'(a) {piece} (b) {money(fx)} {cc}', f'(a) A1 for each correct piece (A2). (b) correct piece (M1) = {money(fx)} (A1).', 4, 'numerical')
    target = fx
    return ret(f'{desc} (a) Write down a piecewise function for the {"tax" if kind == 2 else "cost"}. (b) Show that the function is continuous at {bound}. (c) A customer pays {money(target)} {cc}. Find the {["amount of water used", "distance travelled", "income"][kind]}. '
               f'(d) Find the average {"tax rate" if kind == 2 else "cost per unit"} for this customer and explain why it differs from the gradient of the final piece.',
               f'(a) {piece} (c) {x0} {unit if kind != 2 else cc} (d) {sf(fx / x0)} vs {rates[1]:g}',
               f'(a) A2. (b) R1 both pieces give {money(f(bound))} at the boundary. (c) set the second piece equal to {money(target)} (M1) ⇒ {x0} (A1). (d) {money(fx)} ÷ {x0} = {sf(fx / x0)} (A1); R1 the average includes the cheaper/fixed parts, whereas the gradient is the marginal rate.',
               8, 'multi_step', gap='G5')


# =============================================================================================
# ch08 Modelling with functions
# =============================================================================================
R.facts('ch08-st1', F(
    terms=[('direct variation', 'y varies directly as xⁿ when y = kxⁿ for a constant k > 0'),
           ('inverse variation', 'y varies inversely as xⁿ when y = k/xⁿ, so y decreases as x increases'),
           ('axis of symmetry', 'the vertical line x = −b/(2a) through the vertex of the parabola y = ax² + bx + c'),
           ('quadratic model', 'a model f(x) = ax² + bx + c, used when a quantity rises then falls (or falls then rises) symmetrically')],
    facts=[('If y varies inversely as x and x is doubled, what happens to y?', 'It is halved', ['It is doubled', 'It is squared', 'It is unchanged'], 'y = k/x, so y becomes k/(2x) = y/2.'),
           ('If A varies directly as r² and r is tripled, by what factor does A change?', '9', ['3', '6', '27'], '(3r)² = 9r².'),
           ('For h(t) = −4.9t² + 20t + 2, what does the constant 2 represent?', 'the initial height', ['the maximum height', 'the time of flight', 'the initial speed'], 'h(0) = 2.')],
    why=[('Explain why a quadratic model for the height of a ball is only valid between launch and landing.', 'Outside this interval the model gives negative heights (below ground) or times before the ball was thrown; the domain must be restricted to 0 ≤ t ≤ landing time.'),
         ('Explain why the maximum of h(t) = at² + bt + c with a < 0 occurs at t = −b/(2a).', 'The parabola is symmetric about its axis x = −b/(2a); with a < 0 it opens downwards, so the vertex on the axis is the maximum.')],
    misc=[('If y varies inversely as x, then y = x − k.', 'Inverse variation is multiplicative: y = k/x, so xy is constant.')],
))


@R.add('ch08-st1', ALL, (1, 5), 'short')
def quad_var_core(rng, slot):
    c, d = slot.c, slot.d
    kind = rng.randint(0, 1)
    if c in ('C1', 'C2') and kind == 0:
        n = rng.choice([1, 2, 3, -1, -2])
        x0, k = rng.randint(2, 6), rng.choice([0.5, 1.5, 2, 2.5, 3, 4, 12, 20, 36])
        y0 = k * x0 ** n
        x1 = rng.randint(2, 10)
        y1 = k * x1 ** n
        ctx = pick(rng, [('the braking distance', 'the speed'), ('the intensity of light', 'the distance from the source'), ('the cost', 'the number of items'),
                         ('the time to complete a job', 'the number of workers'), ('the power', 'the wind speed')])
        rel = f'directly as {"" if n == 1 else "the " + ("square" if n == 2 else "cube")}{" of " if n != 1 else ""}x' if n > 0 else f'inversely as {"" if n == -1 else "the square of "}x'
        if c == 'C1':
            return ret(f'y varies {rel}. When x = {x0}, y = {_num(y0)}. Find y when x = {x1}.', _num(y1) if float(y1).is_integer() or abs(y1) >= 0.01 else sf(y1),
                       f'y = kx{sup(n) if n != 1 else ""} (M1); k = {_num(k)} (A1); y = {sf(y1) if not float(y1).is_integer() else _num(y1)} (A1).', 3)
        return ret(f'In a model, {ctx[0]} y varies {rel}, where x is {ctx[1]}. Explain what happens to y when x is multiplied by 3, and justify your answer algebraically.',
                   f'y is multiplied by {_num(3 ** n) if n > 0 else "1/" + str(3 ** -n)}', f'R1 y = kx{sup(n) if n != 1 else ""} ⇒ k(3x){sup(n) if n != 1 else ""} = 3{sup(n) if n != 1 else ""}·kx{sup(n) if n != 1 else ""}; A1 factor {_num(3 ** n) if n > 0 else "1/" + str(3 ** -n)}.', 2, 'explain')
    v0, h0 = rng.randint(8, 30), round(rng.uniform(0.5, 3.0), 1)
    thing = pick(rng, ['a ball thrown upwards', 'a water rocket', 'a volleyball served upwards', 'a firework shell', 'a stone flicked from a catapult'])
    tmax = v0 / 9.8
    hmax = h0 + v0 * v0 / (2 * 9.8)
    tland = (v0 + math.sqrt(v0 * v0 + 4 * 4.9 * h0)) / 9.8
    desc = f'The height, h metres, of {thing} t seconds after launch is modelled by h(t) = −4.9t² + {v0}t + {h0}.'
    if c == 'C1':
        t1 = round(rng.uniform(0.3, tland * 0.9), 1)
        return ret(f'{desc} Find the height after {t1} seconds.', f'{sf(-4.9 * t1 ** 2 + v0 * t1 + h0)} m', f'h({t1}) = {sf(-4.9 * t1 ** 2 + v0 * t1 + h0)} m (A1)(M1 substitution).', 2)
    if c == 'C2':
        return ret(f'{desc} Explain why the maximum height occurs at t = {sf(tmax)} and state a suitable domain for this model.', f'max at t = {sf(tmax)}; 0 ≤ t ≤ {sf(tland)}',
                   f'R1 axis of symmetry t = −b/(2a) = {v0}/9.8 = {sf(tmax)} and a < 0 so the vertex is a maximum; A1 domain 0 ≤ t ≤ {sf(tland)} (h ≥ 0); R1 justification of the upper limit.', 3, 'explain')
    if c == 'C3':
        return ret(f'{desc} Find (a) the maximum height reached; (b) the time at which it hits the ground.', f'(a) {sf(hmax)} m (b) {sf(tland)} s',
                   f'(a) t = {sf(tmax)} (M1), h = {sf(hmax)} m (A1). (b) h(t) = 0 (M1), t = {sf(tland)} s (A1), rejecting the negative root (R1).', 5, 'numerical')
    H = round(hmax * rng.uniform(0.4, 0.85), 1)
    disc = v0 * v0 - 4 * 4.9 * (H - h0)
    t1, t2 = (v0 - math.sqrt(disc)) / 9.8, (v0 + math.sqrt(disc)) / 9.8
    return ret(f'{desc} (a) Find the maximum height. (b) Find the length of time for which it is above {H} m. (c) Find the time at which it reaches the ground. '
               f'(d) Suggest one reason why the model may not be accurate.',
               f'(a) {sf(hmax)} m (b) {sf(t2 - t1)} s (c) {sf(tland)} s (d) air resistance etc.',
               f'(a) {sf(hmax)} (M1 A1). (b) solve −4.9t² + {v0}t + {h0} = {H} (M1): t = {sf(t1)}, {sf(t2)} (A1); {sf(t2 - t1)} s (A1). (c) {sf(tland)} s (A1). (d) R1 air resistance/wind ignored, or object treated as a point.',
               8, 'multi_step', gap='G5')


R.facts('ch08-st2', F(
    terms=[('exponential growth model', 'f(x) = kaˣ + c (a > 1) or f(x) = ke^(rx) + c (r > 0), where the quantity grows by a constant factor in equal time intervals'),
           ('exponential decay model', 'f(x) = kaˣ + c with 0 < a < 1 (or ke^(−rx) + c), which approaches the horizontal asymptote y = c'),
           ('half-life', 'the time taken for a decaying quantity to fall to half of its value'),
           ('doubling time', 'the time taken for a growing quantity to double')],
    facts=[('In T(t) = 20 + 65e^(−0.04t) for the temperature of a cup of tea, what is the long-term temperature?', '20°C', ['85°C', '65°C', '0°C'], 'e^(−0.04t) → 0, so T → 20 (room temperature).'),
           ('A quantity halves every 6 hours. Which model fits?', 'Q = Q₀(0.5)^(t/6)', ['Q = Q₀(0.5)^(6t)', 'Q = Q₀ − 0.5t', 'Q = Q₀(2)^(t/6)'], 'Every 6 hours the exponent increases by 1, multiplying by 0.5.')],
    why=[('Explain why Newton\'s law of cooling is modelled by T = A + Be^(−kt) rather than by a linear function.', 'The rate of cooling is proportional to the temperature difference with the room, so cooling is fast at first and slows down; this gives exponential decay of the difference towards the asymptote T = A, not a constant rate.'),
         ('Explain why the half-life of an exponential decay model does not depend on the starting amount.', 'Q₀e^(−kt) = ½Q₀ gives e^(−kt) = ½, independent of Q₀, so t = ln 2/k.')],
    misc=[('An exponential decay model eventually reaches zero.', 'e^(−kt) is always positive, so the quantity approaches its asymptote but never reaches it.')],
))


@R.add('ch08-st2', ALL, (1, 5), 'short')
def exp_model_core(rng, slot):
    c, d = slot.c, slot.d
    kind = rng.randint(0, 2)
    if kind == 0:
        A, B, k = rng.randint(16, 24), rng.randint(50, 75), round(rng.uniform(0.02, 0.09), 3)
        drink = pick(rng, ['a cup of tea', 'a mug of coffee', 'a bowl of soup', 'a cup of hot chocolate'])
        desc = f'The temperature of {drink}, T °C, t minutes after it is made is modelled by T(t) = {A} + {B}e^(−{k}t).'
        f = lambda t: A + B * math.exp(-k * t)
        asym, start, var, unit = A, A + B, 'T', '°C'
        tgt = round(A + B * rng.uniform(0.2, 0.6))
        ttgt = -math.log((tgt - A) / B) / k
    elif kind == 1:
        Q0, hl = rng.choice([200, 400, 500, 800, 1000]), rng.choice([5.3, 8.0, 12.3, 28.8, 30.2, 6.0])
        iso = {5.3: 'cobalt-60 (half-life 5.3 years)', 8.0: 'iodine-131 (half-life 8.0 days)', 12.3: 'tritium (half-life 12.3 years)', 28.8: 'strontium-90 (half-life 28.8 years)',
               30.2: 'caesium-137 (half-life 30.2 years)', 6.0: 'technetium-99m (half-life 6.0 hours)'}[hl]
        k = math.log(2) / hl
        desc = f'A sample contains {Q0} mg of {iso}. The mass remaining after t {iso.split()[-1][:-1]} is M(t) = {Q0}e^(−kt).'
        f = lambda t: Q0 * math.exp(-k * t)
        asym, start, var, unit = 0, Q0, 'M', 'mg'
        tgt = round(Q0 * rng.uniform(0.05, 0.4))
        ttgt = -math.log(tgt / Q0) / k
    else:
        P0, g = rng.randint(2, 30) * 100, round(rng.uniform(1.03, 1.35), 2)
        org = pick(rng, ['an invasive plant species', 'a colony of ants', 'users of a new app', 'a yeast culture', 'rabbits on an island'])
        desc = f'The number of {org} after t weeks is modelled by N(t) = {P0}({g})ᵗ.'
        f = lambda t: P0 * g ** t
        k = math.log(g)
        asym, start, var, unit = None, P0, 'N', ''
        tgt = int(round(P0 * rng.uniform(2.5, 9), -1))
        ttgt = math.log(tgt / P0) / math.log(g)
    t1 = rng.randint(2, 20)
    if c == 'C1':
        if kind == 1:
            return ret(f'{desc} Show that k = {sf(k)} and find the mass remaining after {t1} {iso.split()[-1][:-1]}.', f'k = {sf(k)}; {sf(f(t1))} mg', f'½ = e^(−{hl}k) (M1) ⇒ k = ln2/{hl} = {sf(k)} (A1); M({t1}) = {sf(f(t1))} (A1).', 3)
        return ret(f'{desc} Find {var}({t1}).', f'{sf(f(t1))} {unit}'.strip(), f'Substitute t = {t1} (M1); {sf(f(t1))} (A1).', 2)
    if c == 'C2':
        if asym is None:
            return ret(f'{desc} Interpret the values {P0} and {g} in context, and explain why the model cannot be valid indefinitely.', f'{P0} initial number; growth factor {g} per week ({sf((g - 1) * 100)}% weekly increase)',
                       f'A1 {P0} = N(0), the initial number; A1 {g}: multiplied by {g} each week, i.e. {sf((g - 1) * 100)}% growth; R1 unlimited growth is impossible – resources/space are limited.', 3, 'explain')
        return ret(f'{desc} State the horizontal asymptote of the graph of {var} and explain its meaning in context.', f'{var} = {asym}',
                   f'A1 {var} = {asym}; R1 {"the drink cools towards room temperature " + str(asym) + " °C but never quite reaches it" if kind == 0 else "the mass approaches 0 but some radioactive material always remains in the model"}.', 2, 'explain')
    if c == 'C3':
        return ret(f'{desc} Find the time at which {var} = {tgt}.', f't = {sf(ttgt)}', f'Set {var}(t) = {tgt} (M1); logarithms or GDC (M1); t = {sf(ttgt)} (A1).', 3, 'numerical')
    t2 = t1 + rng.randint(3, 15)
    rate = (f(t2) - f(t1)) / (t2 - t1)
    return ret(f'{desc} (a) Write down the initial value of {var}. (b) Find the time at which {var} = {tgt}. (c) Find the average rate of change of {var} between t = {t1} and t = {t2}, with units. '
               f'(d) Comment on the suitability of the model for large values of t.',
               f'(a) {start} (b) {sf(ttgt)} (c) {m(sf(rate))} {["°C per minute", "mg per unit time", "per week"][kind]} (d) see key',
               f'(a) A1. (b) M1 A1 {sf(ttgt)}. (c) ({sf(f(t2))} − {sf(f(t1))})/({t2} − {t1}) (M1) = {m(sf(rate))} (A1). '
               f'(d) R1 {"realistic: approaches room temperature" if kind == 0 else "realistic: mass tends to 0" if kind == 1 else "unrealistic: unlimited growth"}.', 7, 'multi_step', gap='G5')


R.facts('ch08-st3', F(
    terms=[('amplitude', 'half the distance between the maximum and minimum values of a sinusoidal function; |a| in a sin(b(x − c)) + d'),
           ('period', 'the horizontal length of one complete cycle; 360°/b (or 2π/b) for a sin(bx)'),
           ('principal axis', 'the horizontal line y = d about which a sinusoidal graph oscillates'),
           ('cubic model', 'a model f(x) = ax³ + bx² + cx + d, which can have up to two turning points')],
    facts=[('For f(x) = 3 sin(2x) + 5 (degrees), what is the period?', '180°', ['360°', '720°', '90°'], '360°/2 = 180°.'),
           ('For f(x) = 4 cos(30x) − 1, what is the minimum value?', '−5', ['−1', '−4', '3'], 'Principal axis −1, amplitude 4.'),
           ('Which feature of a cubic model of a box\'s volume gives the maximum volume?', 'a local maximum point', ['the y-intercept', 'a zero', 'the point of inflection'], 'Use the GDC maximum feature.')],
    why=[('Explain why sinusoidal functions are suitable for modelling tides.', 'Tide heights rise and fall in a regular repeating cycle with a roughly constant period (about 12.4 h) and amplitude, matching the periodic shape of a sine curve.'),
         ('Explain why a cubic model for the volume of an open box made from a sheet has a restricted domain.', 'The cut-out size x must be positive and smaller than half the shorter side; outside this interval the dimensions would be negative.')],
    misc=[('In h(t) = 3 sin(30t) + 10 the amplitude is 10.', '10 is the principal axis (mean level); the amplitude is 3.')],
))


@R.add('ch08-st3', ALL, (1, 5), 'short')
def sin_cubic_core(rng, slot):
    c, d = slot.c, slot.d
    if rng.random() < 0.6 or c == 'C1':
        a, mean = round(rng.uniform(0.8, 4.5), 1), round(rng.uniform(3, 9), 1)
        per = rng.choice([12, 12.5, 24, 6, 8, 10])
        b = 360 / per
        shift = rng.choice([0, 1, 2, 3])
        kind = pick(rng, [('the depth of water in a harbour in {}', 'm', 'hours after midnight'), ('the height of a seat on a Ferris wheel in {}', 'm', 'minutes after the ride starts'),
                          ('the temperature in a greenhouse in {}', '°C', 'hours after 6 am')])
        place = pick(rng, ['Halifax', 'Saint-Malo', 'Mumbai', 'Lisbon', 'Auckland', 'Busan'])
        what = kind[0].format(place)
        if 'Ferris' in what:
            mean = round(a + rng.uniform(1, 3), 1)
        arg_ = f'{_num(b)}t' if shift == 0 else f'{_num(b)}(t − {shift})'
        desc = f'{what[0].upper() + what[1:]} is modelled by h(t) = {a} sin({arg_}) + {mean}, where t is {kind[2]} (angles in degrees).'
        hmax, hmin = mean + a, mean - a
        tmax = shift + per / 4
        if c == 'C1':
            return ret(f'{desc} Write down the amplitude, the period and the maximum value of h.', f'amplitude {a}, period {_num(per)}, max {_num(hmax)} {kind[1]}',
                       f'A1 amplitude {a}; A1 period 360/{_num(b)} = {_num(per)}; A1 max {mean} + {a} = {_num(hmax)}.', 3)
        if c == 'C2':
            return ret(f'{desc} Explain how the values {a} and {mean} determine the greatest and least values of h, and interpret {mean} in context.', f'{_num(hmax)} and {_num(hmin)}',
                       f'R1 sin varies between −1 and 1, so h varies between {mean} − {a} and {mean} + {a}; A1 {_num(hmin)} and {_num(hmax)} {kind[1]}; R1 {mean} is the mean level (principal axis).', 3, 'explain')
        lvl = round(mean + a * rng.uniform(-0.7, 0.7), 1)
        sols = [t for t in _roots_num(lambda t: a * math.sin(math.radians(b * (t - shift))) + mean - lvl, 0, per) if 0 <= t <= per]
        if c == 'C3':
            return ret(f'{desc} (a) Find the first time after t = 0 at which h is a maximum. (b) Find the values of t, 0 ≤ t ≤ {_num(per)}, for which h = {lvl}.', f'(a) {sf(tmax % per)} (b) ' + ', '.join(sf(x) for x in sols),
                       f'(a) {sf(tmax % per)} (A1). (b) GDC intersection (M1); ' + ', '.join(sf(x) for x in sols) + ' (A1 A1).', 4, 'numerical')
        above = [t for t in sols]
        return ret(f'{desc} A boat needs at least {lvl} {kind[1]} to {"enter the harbour" if "harbour" in what else "safely operate"}. (a) Find the maximum and minimum values. (b) Find the times in 0 ≤ t ≤ {_num(per)} when h = {lvl}. '
                   f'(c) Hence find the total length of time in one period for which h ≥ {lvl}. (d) Explain why the answer to (c) repeats every {_num(per)} {kind[2].split()[0]}.',
                   f'(a) {_num(hmax)}, {_num(hmin)} (b) ' + ', '.join(sf(x) for x in sols) + f' (c) {sf(_time_above(lambda t: a * math.sin(math.radians(b * (t - shift))) + mean, lvl, per))}',
                   f'(a) A1 A1. (b) M1 A1 A1. (c) R1 identify intervals where the curve is above the line; {sf(_time_above(lambda t: a * math.sin(math.radians(b * (t - shift))) + mean, lvl, per))} (A1). (d) R1 the function is periodic with period {_num(per)}.',
                   8, 'multi_step', gap='G5')
    L, W = rng.randint(20, 60), rng.randint(15, 45)
    if W > L:
        L, W = W, L
    V = lambda x: x * (L - 2 * x) * (W - 2 * x)
    xs = np.linspace(0, W / 2, 20001)
    vs = [V(x) for x in xs]
    i = int(np.argmax(vs))
    xm, vm = xs[i], vs[i]
    mat_ = pick(rng, ['card', 'sheet metal', 'cardboard', 'plywood'])
    desc = f'An open box is made from a {L} cm by {W} cm sheet of {mat_} by cutting squares of side x cm from each corner and folding up the sides.'
    if c == 'C2':
        return ret(f'{desc} Show that the volume is V(x) = x({L} − 2x)({W} − 2x) and explain why 0 < x < {_num(W / 2)}.', 'V = x(L − 2x)(W − 2x)',
                   f'R1 base {L} − 2x by {W} − 2x, height x; R1 lengths must be positive so x > 0 and {W} − 2x > 0.', 2, 'explain')
    if c == 'C3':
        return ret(f'{desc} Use technology to find the value of x that maximises the volume and the maximum volume.', f'x = {sf(xm)} cm, V = {sf(vm)} cm³',
                   f'V(x) = x({L} − 2x)({W} − 2x) (A1); GDC maximum (M1): x = {sf(xm)} (A1), V = {sf(vm)} cm³ (A1).', 4, 'numerical')
    target = round(vm * rng.uniform(0.4, 0.8), -1)
    xsol = [x for x in _roots_num(lambda x: V(x) - target, 0.001, W / 2 - 0.001)]
    return ret(f'{desc} (a) Write down V(x) and state its domain. (b) Find the maximum volume. (c) Find the values of x for which V = {int(target)} cm³. (d) Explain which value you would choose if the box must be as deep as possible.',
               f'(a) V = x({L} − 2x)({W} − 2x), 0 < x < {_num(W / 2)} (b) {sf(vm)} cm³ (c) ' + ', '.join(sf(x) for x in xsol) + f' (d) x = {sf(max(xsol)) if xsol else "—"}',
               f'(a) A1 A1. (b) GDC max (M1) {sf(vm)} (A1). (c) intersection with V = {int(target)} (M1): ' + ', '.join(sf(x) for x in xsol) + ' (A1 A1). (d) R1 larger x gives a deeper box.', 8, 'multi_step', gap='G5')


def _time_above(f, lvl, per, n=20000):
    xs = np.linspace(0, per, n + 1)
    return sum(1 for x in xs[:-1] if f(x) >= lvl) * per / n


R.facts('ch08-st4', F(
    terms=[('modelling cycle', 'pose a real-world problem → develop a model → test the model against data → reflect on and refine the model → use it to make predictions'),
           ('sum of square residuals (SSres)', 'Σ(yᵢ − f(xᵢ))², a measure of how well a model fits data; smaller is better'),
           ('residual', 'the difference between an observed value and the value predicted by the model, yᵢ − f(xᵢ)'),
           ('assumption', 'a simplifying condition accepted when building a model, e.g. constant growth rate or no air resistance')],
    facts=[('Which stage of the modelling cycle compares model predictions with new data?', 'testing the model', ['posing the problem', 'stating assumptions', 'choosing variables'], 'Testing checks predictions against observations.'),
           ('Two models fit the same data. Model A has SSres = 4.2 and model B has SSres = 11.8. Which fits better?', 'Model A', ['Model B', 'They fit equally well', 'It cannot be decided'], 'Smaller residuals mean predictions are closer to data.')],
    why=[('Explain why a model with a very small sum of squared residuals might still be a poor choice for predictions.', 'It may over-fit (e.g. a high-degree polynomial passing through every point) and behave unrealistically outside the data range; the model should also make sense in context.'),
         ('Explain why stating assumptions is an essential part of building a mathematical model.', 'Assumptions show the conditions under which the model is valid, make its limitations clear and indicate how the model can be refined.')],
    misc=[('If a model fits the data well, its predictions far outside the data range will also be accurate.', 'Good fit within the data does not guarantee valid extrapolation; conditions may change outside the observed range.')],
    evaluate=[('A mathematical model is only useful if its predictions are exactly correct.', ['inaccurate models can mislead decisions', 'testing against data is essential'], ['all models simplify reality ("all models are wrong, some are useful")', 'approximate models still guide decisions and reveal trends', 'models can be refined over the modelling cycle'],
               'Models are useful when their accuracy is adequate for their purpose and their limitations are understood; exactness is neither possible nor necessary.')],
))


@R.add('ch08-st4', ALL, (1, 5), 'short')
def model_cycle_core(rng, slot):
    c, d = slot.c, slot.d
    a_true, r_true = rng.randint(20, 200), round(rng.uniform(1.08, 1.4), 2)
    xs = list(range(0, rng.randint(5, 7)))
    ys = [round(a_true * r_true ** x * rng.uniform(0.94, 1.06)) for x in xs]
    m1, c1 = np.polyfit(xs, ys, 1)
    lin = lambda x: m1 * x + c1
    expm = lambda x: a_true * r_true ** x
    sse_l = sum((y - lin(x)) ** 2 for x, y in zip(xs, ys))
    sse_e = sum((y - expm(x)) ** 2 for x, y in zip(xs, ys))
    what = pick(rng, [('the number of electric cars registered in a town (hundreds)', 'year'), ('the number of subscribers to a podcast (thousands)', 'month'),
                      ('the area covered by algae in a lake (m²)', 'week'), ('the number of visitors to a new museum (hundreds)', 'month')])
    table = '; '.join(f'{x}: {y}' for x, y in zip(xs, ys))
    desc = f'The table shows {what[0]} t {what[1]}s after the start of a study (t: value): {table}.'
    if c == 'C1':
        return ret(f'{desc} Model A is L(t) = {sf(m1)}t + {sf(c1)}. Find the residual for t = {xs[-1]}.', m(sf(ys[-1] - lin(xs[-1]))),
                   f'residual = observed − predicted = {ys[-1]} − {sf(lin(xs[-1]), 4)} (M1) = {m(sf(ys[-1] - lin(xs[-1])))} (A1).', 2)
    if c == 'C2':
        return ret(f'{desc} {name(rng)} proposes a linear model. Explain, with reference to the data, why an exponential model may be more appropriate, and state one assumption that the exponential model makes.',
                   'Growth factors are roughly constant', f'R1 successive ratios ≈ ' + ', '.join(sf(ys[i + 1] / ys[i]) for i in range(min(3, len(ys) - 1))) + ' are nearly constant while the differences increase; '
                   f'R1 assumption: the growth rate stays constant (e.g. no saturation of the market/space).', 3, 'explain')
    if c == 'C3':
        return ret(f'{desc} Model A: L(t) = {sf(m1)}t + {sf(c1)}. Model B: E(t) = {a_true}({r_true})ᵗ. Calculate the sum of squared residuals for each model and state which model fits better.',
                   f'SSres A = {sf(sse_l)}, B = {sf(sse_e)}; {"B" if sse_e < sse_l else "A"} fits better', f'Residuals for each data point (M1); SSres(A) = {sf(sse_l)} (A1); SSres(B) = {sf(sse_e)} (A1); R1 smaller SSres: model {"B" if sse_e < sse_l else "A"}.',
                   5, 'numerical')
    tp = xs[-1] + rng.randint(3, 8)
    return ret(f'{desc} (a) Use technology to find the equation of the least-squares regression line, model A. (b) Model B is E(t) = {a_true}({r_true})ᵗ. Compare the models using the sum of squared residuals. '
               f'(c) Use each model to predict the value at t = {tp} and comment on the reliability of these predictions. (d) Describe how the model could be refined in the next stage of the modelling cycle.',
               f'(a) L = {sf(m1)}t + {sf(c1)} (b) SSres {sf(sse_l)} vs {sf(sse_e)} (c) {sf(lin(tp))}, {sf(expm(tp))} (d) collect more data / logistic model',
               f'(a) A1 A1. (b) SSres(A) = {sf(sse_l)} (A1), SSres(B) = {sf(sse_e)} (A1); R1 model {"B" if sse_e < sse_l else "A"} fits better. (c) L({tp}) = {sf(lin(tp))}, E({tp}) = {sf(expm(tp))} (A1 A1); '
               f'R1 extrapolation beyond the data, so unreliable; the models diverge. (d) R1 e.g. test against new data, consider a logistic model with a carrying capacity.', 10, 'multi_step', gap='G5')


# =============================================================================================
# ch09 Further functions and modelling (AHL)
# =============================================================================================
R.facts('ch09-st1', F(
    terms=[('composite function', '(f ∘ g)(x) = f(g(x)): apply g first, then f'),
           ('identity function', 'the function x ↦ x; (f ∘ f⁻¹)(x) = (f⁻¹ ∘ f)(x) = x'),
           ('one-to-one function', 'a function in which each output comes from exactly one input, so that an inverse function exists')],
    facts=[('If f(x) = 2x and g(x) = x + 3, what is (f ∘ g)(x)?', '2x + 6', ['2x + 3', '2x² + 6x', 'x + 6'], 'f(g(x)) = 2(x + 3).'),
           ('Which domain restriction makes f(x) = (x − 2)² one-to-one?', 'x ≥ 2', ['x ≥ 0', 'x ≤ 4', 'all real x'], 'Restrict to one side of the vertex x = 2.')],
    why=[('Explain why (f ∘ g)(x) is generally not equal to (g ∘ f)(x).', 'The order of operations matters: f(g(x)) applies g first, g(f(x)) applies f first; e.g. doubling then adding 3 differs from adding 3 then doubling.'),
         ('Explain why the domain of f ∘ g may be smaller than the domain of g.', 'g(x) must lie in the domain of f; any x for which g(x) is not an allowed input for f must be excluded.')],
    misc=[('(f ∘ g)(x) means f(x) × g(x).', 'It means f applied to g(x), i.e. substituting g(x) into f; the product is written (fg)(x).')],
))


@R.add('ch09-st1', ALL, (1, 5), 'short')
def composite_core(rng, slot):
    c, d = slot.c, slot.d
    a, b = rng.choice([2, 3, 4, -2, 5]), rng.randint(-7, 7)
    p, q = rng.choice([1, 2, -1]), rng.randint(-6, 6)
    fstr = f'{a}x {sgn(b)}' if b else f'{a}x'
    gstr = f'{"" if p == 1 else MINUS if p == -1 else p}x² {sgn(q)}' if q else f'{"" if p == 1 else MINUS if p == -1 else p}x²'
    f = lambda x: a * x + b
    g = lambda x: p * x * x + q
    k = rng.randint(-4, 5)
    if c == 'C1':
        v = f(g(k)) if rng.random() < 0.5 else None
        if v is not None:
            return nmcq(rng, f'Given f(x) = {fstr} and g(x) = {gstr}, find (f ∘ g)({m(k)}).', v, [g(f(k)), f(k) * g(k), f(k) + g(k)], f'g({m(k)}) = {m(g(k))}; f({m(g(k))}) = {m(v)}.', fmtf=lambda z: m(_num(z)))
        return ret(f'Given f(x) = {fstr} and g(x) = {gstr}, find (g ∘ f)({m(k)}).', m(g(f(k))), f'f({m(k)}) = {m(f(k))} (A1); g({m(f(k))}) = {m(g(f(k)))} (A1).', 2)
    if c == 'C2':
        fg = f'{a * p}x² {sgn(a * q + b)}'
        gf = f'{"" if p == 1 else MINUS if p == -1 else p}({fstr})² {sgn(q)}' if q else f'{"" if p == 1 else MINUS if p == -1 else p}({fstr})²'
        return ret(f'For f(x) = {fstr} and g(x) = {gstr}, find expressions for (f ∘ g)(x) and (g ∘ f)(x), and use them to explain why composition is not commutative.', f'(f∘g)(x) = {fg}; (g∘f)(x) = {gf}',
                   f'(f∘g)(x) = {a}({gstr}) {sgn(b)} = {fg} (A1); (g∘f)(x) = {gf} (A1); R1 e.g. at x = 1 they give {m(f(g(1)))} and {m(g(f(1)))}, which differ.', 3, 'explain')
    if c == 'C3':
        kind = rng.randint(0, 1)
        if kind == 0:
            r_ = round(rng.uniform(0.6, 1.5), 3)
            t = rng.choice([5, 8, 10, 12, 15, 20])
            c1, c2 = rng.sample(['USD', 'EUR', 'GBP', 'CAD', 'AUD', 'CHF'], 2)
            x0 = rng.randint(50, 600)
            res = (1 + t / 100) * r_ * x0
            return ret(f'A shop in {pick(rng, CITIES)} prices an item at x {c1}. Converting to {c2} uses c(x) = {r_}x and adding sales tax uses s(x) = {1 + t / 100:g}x. (a) Find (s ∘ c)(x). (b) Find the price in {c2} including tax of an item marked {x0} {c1}. '
                       f'(c) Find (s ∘ c)⁻¹(x) and interpret it.', f'(a) {sf((1 + t / 100) * r_, 4)}x (b) {money(res)} (c) x/{sf((1 + t / 100) * r_, 4)}',
                       f'(a) {1 + t / 100:g}({r_}x) = {sf((1 + t / 100) * r_, 4)}x (A1). (b) {money(res)} (A1). (c) x/{sf((1 + t / 100) * r_, 4)} (A1); R1 marked price in {c1} for a final price x in {c2}.', 4, 'numerical')
        h, kk = rng.randint(-5, 5), rng.randint(-6, 6)
        return ret(f'The function f(x) = (x {sgn(-h)})² {sgn(kk)} is defined for x ≥ {m(h)}. Find f⁻¹(x), stating its domain.', f'f⁻¹(x) = {m(h) + " + " if h else ""}√(x {sgn(-kk)}), x ≥ {m(kk)}'.replace('(x + 0)', '(x)'),
                   f'Swap x and y (M1); y = {m(h) + " + " if h else ""}√(x {sgn(-kk)}) (positive root since x ≥ {m(h)}) (A1 R1); domain x ≥ {m(kk)} (A1).', 4, 'numerical')
    # C4: temperature conversion chain
    t0 = rng.randint(-20, 40)
    return ret(f'Temperatures can be converted using F(C) = 1.8C + 32 (Celsius to Fahrenheit) and K(C) = C + 273.15 (Celsius to kelvin). (a) Find F⁻¹ and explain what it does. (b) Find (K ∘ F⁻¹)(x), the function converting Fahrenheit to kelvin. '
               f'(c) A weather station in {pick(rng, ["Anchorage", "Phoenix", "Winnipeg", "Houston", "Fairbanks", "Miami"])} records {_num(1.8 * t0 + 32)} °F. Find this temperature in kelvin. (d) Find the temperature at which the Fahrenheit and Celsius readings are equal.',
               f'(a) F⁻¹(x) = (x − 32)/1.8 (b) (x − 32)/1.8 + 273.15 (c) {_num(t0 + 273.15)} K (d) −40',
               f'(a) M1 A1; R1 converts °F to °C. (b) K(F⁻¹(x)) = (x − 32)/1.8 + 273.15 (M1 A1). (c) {_num(t0 + 273.15)} K (A1). (d) 1.8C + 32 = C (M1) ⇒ C = −40 (A1).', 8, 'multi_step', gap='G5')


R.facts('ch09-st2', F(
    terms=[('translation', 'y = f(x − h) + k shifts the graph h units right and k units up, the vector (h, k)'),
           ('vertical stretch', 'y = pf(x) stretches the graph parallel to the y-axis by scale factor p'),
           ('horizontal stretch', 'y = f(qx) stretches the graph parallel to the x-axis by scale factor 1/q'),
           ('reflection in the x-axis', 'y = −f(x) maps each point (x, y) to (x, −y)')],
    facts=[('Which transformation maps y = f(x) to y = f(x + 3)?', 'a translation 3 units to the left', ['a translation 3 units to the right', 'a translation 3 units up', 'a horizontal stretch by factor 3'], 'f(x − h) moves right by h; here h = −3.'),
           ('The point (4, 6) lies on y = f(x). Which point lies on y = f(2x)?', '(2, 6)', ['(8, 6)', '(4, 12)', '(4, 3)'], 'Horizontal stretch by factor ½ halves the x-coordinate.'),
           ('The point (2, 5) lies on y = f(x). Which point lies on y = −f(x)?', '(2, −5)', ['(−2, 5)', '(−2, −5)', '(5, 2)'], 'Reflection in the x-axis negates y.')],
    why=[('Explain why y = f(x − 2) moves the graph 2 units to the right, not to the left.', 'The new function takes at x the value f had at x − 2; every feature occurs 2 units later along the x-axis.'),
         ('Explain why the order of a vertical stretch and a vertical translation matters.', 'Stretching then translating gives pf(x) + k, but translating then stretching gives p(f(x) + k) = pf(x) + pk; the translation is also stretched in the second case.')],
    misc=[('The graph of y = 3f(x) is the graph of y = f(x) stretched horizontally by factor 3.', 'Multiplying outside the function stretches vertically: y-coordinates are tripled, x-coordinates unchanged.')],
))


@R.add('ch09-st2', ALL, (1, 5), 'short')
def transform_core(rng, slot):
    c, d = slot.c, slot.d
    px, py = rng.randint(-6, 6), rng.randint(-6, 8)
    a = rng.choice([2, 3, -1, -2, 0.5])
    b = rng.choice([1, 2, 0.5, 3])
    h, k = rng.randint(-5, 5), rng.randint(-6, 6)
    nx, ny = px / b + h, a * py + k
    inner = (f'x {sgn(-h)}' if b == 1 else f'{_num(b)}(x {sgn(-h)})') if h else (f'{_num(b)}x' if b != 1 else 'x')
    gx = f'{m(_num(a)) if a not in (1, -1) else ("−" if a == -1 else "")}f({inner})' + (f' {sgn(k)}' if k else '')
    if c == 'C1':
        if rng.random() < 0.5:
            return mcq(rng, f'The point ({m(px)}, {m(py)}) lies on y = f(x). Find the image of this point on y = f(x {sgn(-h)}) {sgn(k)}.' if h else f'The point ({m(px)}, {m(py)}) lies on y = f(x). Find the image of this point on y = f(x) {sgn(k)}.',
                       f'({m(_num(px + h))}, {m(_num(py + k))})', [f'({m(_num(px - h))}, {m(_num(py + k))})', f'({m(_num(px + h))}, {m(_num(py - k))})', f'({m(_num(px + k))}, {m(_num(py + h))})'],
                       f'Translation by ({m(h)}, {m(k)}).') if (h or k) else None
        return ret(f'Describe the transformation that maps y = f(x) to y = {_num(a)}f(x).', f'vertical stretch, scale factor {_num(abs(a))}' + (', and reflection in the x-axis' if a < 0 else ''),
                   f'A1 vertical stretch (parallel to y-axis) by factor {_num(abs(a))}' + (' A1 reflection in the x-axis' if a < 0 else ''), 2 if a < 0 else 1)
    if c == 'C2':
        k2 = rng.randint(1, 5)
        p_ = rng.choice([2, 3])
        return ret(f'{name(rng)} applies a vertical stretch with scale factor {p_} and then a translation of {k2} units up to y = f(x); {name(rng)} applies the translation first and then the stretch. Explain why they obtain different graphs, giving both equations.',
                   f'y = {p_}f(x) + {k2} and y = {p_}f(x) + {p_ * k2}', f'A1 stretch then translate: y = {p_}f(x) + {k2}; A1 translate then stretch: y = {p_}(f(x) + {k2}) = {p_}f(x) + {p_ * k2}; R1 the second stretches the translation as well.', 3, 'explain')
    if c == 'C3':
        return ret(f'The graph of y = f(x) passes through ({m(px)}, {m(py)}). The graph of y = g(x) is obtained by a horizontal stretch with scale factor {_num(1 / b)}, then a translation by the vector ({m(h)}, 0), then a vertical stretch with scale factor {_num(a)} and finally a translation by (0, {m(k)}). '
                   f'Write down g(x) in terms of f and find the image of ({m(px)}, {m(py)}).', f'g(x) = {gx}; ({m(_num(nx))}, {m(_num(ny))})',
                   f'g(x) = {gx} (A2, A1 for two correct parts); x: {m(px)} × {_num(1 / b)} {sgn(h)} = {m(_num(nx))} (A1); y: {_num(a)} × {m(py)} {sgn(k)} = {m(_num(ny))} (A1).', 4, 'numerical')
    base = pick(rng, [('x²', lambda x: x * x), ('√x', lambda x: math.sqrt(x) if x >= 0 else float('nan')), ('1/x', lambda x: 1 / x if x else float('nan')), ('2ˣ', lambda x: 2 ** x)])
    hh, kk = rng.randint(-4, 4), rng.randint(-5, 5)
    aa = rng.choice([2, 3, -1, -2])
    inn = f'x {sgn(-hh)}' if hh else 'x'
    co = m(_num(aa)) if aa not in (1, -1) else ('−' if aa == -1 else '')
    core = {'x²': f'{co}({inn})²' if hh else f'{co}x²', '√x': f'{co}√({inn})', '1/x': f'{m(_num(aa))}/({inn})' if hh else f'{m(_num(aa))}/x', '2ˣ': f'{co}×2^({inn})' if hh else f'{co}×2ˣ'}[base[0]]
    core = core.replace('−×', '−').replace('(×', '(') if core.startswith('×') is False else core[1:]
    if core.startswith('×'):
        core = core[1:]
    expr = core + (f' {sgn(kk)}' if kk else '')
    return ret(f'The graph of y = {base[0]} is transformed by a translation of {m(hh)} units parallel to the x-axis, then {"a reflection in the x-axis" if aa == -1 else "a vertical stretch with scale factor " + _num(abs(aa)) + (" followed by a reflection in the x-axis" if aa < 0 else "")}, then a translation of {m(kk)} units parallel to the y-axis. '
               f'(a) Write down the equation of the transformed graph. (b) State any asymptotes or the vertex of the new graph. (c) Explain why changing the order of the {"reflection" if aa == -1 else "vertical stretch"} and the final translation would change the equation.',
               f'(a) y = {expr} (c) the translation would also be {"reflected" if aa == -1 else "stretched"}',
               f'(a) A1 for each correct transformation (A3). (b) A1 A1 correct key features (e.g. {"vertex (" + m(hh) + ", " + m(kk) + ")" if base[0] == "x²" else "start point (" + m(hh) + ", " + m(kk) + ")" if base[0] == "√x" else "asymptotes x = " + m(hh) + ", y = " + m(kk) if base[0] == "1/x" else "asymptote y = " + m(kk)}). (c) R1 a(f + k) ≠ af + k.',
               6, 'multi_step', gap='G5')


@R.add('ch09-st2', ('C3', 'C4'), (2, 5), 'multi_step')
def transform_quad(rng, slot):
    p_, q_ = rng.randint(-4, 4), rng.randint(-5, 5)
    a, h, k = rng.choice([2, 3, -1, -2, 0.5]), rng.randint(-4, 4), rng.randint(-6, 6)
    # f(x) = (x − p)² + q ; g(x) = a f(x − h) + k → vertex (p + h, a q + k)
    fstr = poly([1, -2 * p_, p_ * p_ + q_])
    vx, vy = p_ + h, a * q_ + k
    g0 = a * ((0 - h - p_) ** 2 + q_) + k
    if slot.c == 'C3':
        return ret(f'Let f(x) = {fstr}. The graph of y = g(x) is the image of y = f(x) under a translation by ({m(h)}, {m(k)}). Find g(x) in the form ax² + bx + c and the coordinates of its vertex.',
                   f'g(x) = {poly([1, -2 * (p_ + h), (p_ + h) ** 2 + q_ + k])}; vertex ({m(p_ + h)}, {m(q_ + k)})', f'g(x) = f(x {sgn(-h)}) {sgn(k)} (M1); expand (A1); vertex ({m(p_ + h)}, {m(q_ + k)}) (A1).', 3, 'numerical')
    return ret(f'Let f(x) = {fstr}. (a) Write f(x) in the form (x − p)² + q and state its vertex. (b) The graph of g is obtained from f by a translation of {m(h)} units horizontally, then a vertical stretch with scale factor {_num(a)}, then a vertical translation of {m(k)}. Write down g(x). '
               f'(c) Find the vertex and the y-intercept of y = g(x). (d) State whether the vertex of g is a maximum or a minimum, with a reason.',
               f'(a) (x {sgn(-p_)})² {sgn(q_)}, vertex ({m(p_)}, {m(q_)}) (b) g(x) = {m(_num(a))}(x {sgn(-(p_ + h))})² {sgn(a * q_ + k, fmtf=_num)} (c) vertex ({m(vx)}, {m(_num(vy))}), y-intercept {m(_num(g0))} (d) {"minimum" if a > 0 else "maximum"}',
               f'(a) completing the square (M1 A1). (b) A1 A1. (c) ({m(vx)}, {m(_num(vy))}) (A1); g(0) = {m(_num(g0))} (A1). (d) R1 {"a > 0 opens upward" if a > 0 else "the reflection makes it open downward"}.', 7, 'multi_step', gap='G5')


@R.add('ch09-st1', ('C3', 'C4'), (2, 5), 'multi_step')
def composite_solve(rng, slot):
    a, b = rng.choice([2, 3, -2, 4]), rng.randint(-6, 6)
    p, q = rng.choice([2, 3, 4, 5]), rng.randint(1, 6)
    # f(x) = ax + b, g(x) = p/(x - q) ; (f∘g)(x) = a p/(x − q) + b
    t = rng.choice([v for v in range(-8, 12) if v != b])
    x_ = q + a * p / (t - b)
    fstr = f'{a}x {sgn(b)}' if b else f'{a}x'
    if slot.c == 'C3':
        return ret(f'Let f(x) = {fstr} and g(x) = {p}/(x − {q}), x ≠ {q}. Solve (f ∘ g)(x) = {m(t)}.', f'x = {m(sf(x_))}', f'(f∘g)(x) = {a * p}/(x − {q}) {sgn(b)} (A1); {a * p}/(x − {q}) = {m(t - b)} (M1); x = {m(sf(x_))} (A1).', 3, 'numerical')
    return ret(f'Let f(x) = {fstr} and g(x) = {p}/(x − {q}), x ≠ {q}. (a) Find (f ∘ g)(x) and state its range. (b) Solve (f ∘ g)(x) = {m(t)}. (c) Find g⁻¹(x) and f⁻¹(x). (d) Verify that (f ∘ g)⁻¹ = g⁻¹ ∘ f⁻¹ at x = {m(t)}.',
               f'(a) {a * p}/(x − {q}) {sgn(b)}, y ≠ {m(b)} (b) x = {m(sf(x_))} (c) g⁻¹(x) = {p}/x + {q}, f⁻¹(x) = (x {sgn(-b)})/{a} (d) both give {m(sf(x_))}',
               f'(a) A1, range A1. (b) M1 A1. (c) A1 A1. (d) f⁻¹({m(t)}) = {m(_num((t - b) / a))}, g⁻¹ of that = {m(sf(x_))} (M1 A1), equal to the answer in (b) (R1).', 9, 'multi_step', gap='G5')


R.facts('ch09-st3', F(
    terms=[('logistic model', 'f(x) = L/(1 + Ce^(−kx)), L, C, k > 0, describing growth that slows as it approaches a carrying capacity L'),
           ('carrying capacity', 'the upper limit L that a logistic model approaches, e.g. the maximum population an environment can support'),
           ('logarithmic model', 'f(x) = a + b ln x, x > 0, describing quantities that keep increasing but ever more slowly')],
    facts=[('For P(t) = 5000/(1 + 24e^(−0.3t)), what is the carrying capacity?', '5000', ['200', '24', '5024'], 'As t → ∞, e^(−0.3t) → 0 and P → 5000.'),
           ('For P(t) = 5000/(1 + 24e^(−0.3t)), what is P(0)?', '200', ['5000', '208.3', '0'], '5000/(1 + 24) = 200.'),
           ('At what population is a logistic model growing fastest?', 'half the carrying capacity', ['the carrying capacity', 'the initial population', 'zero'], 'The point of inflection is at L/2.')],
    why=[('Explain why a logistic model is often more realistic than an exponential model for a population of animals.', 'Growth slows as food and space become limited; the logistic model levels off at the carrying capacity instead of growing without bound.'),
         ('Explain why a logarithmic model is suitable for the growth of a child\'s vocabulary or the perceived loudness of sound.', 'These quantities keep increasing but each equal increase requires a multiplicative increase in the input – the rate of increase falls, as for ln x.')],
    misc=[('A logistic population eventually exceeds its carrying capacity because it never stops growing.', 'The population approaches L asymptotically from below; 1 + Ce^(−kt) > 1 so P < L for all t.')],
))


@R.add('ch09-st3', ALL, (1, 5), 'short')
def logistic_core(rng, slot):
    c, d = slot.c, slot.d
    L = rng.choice([800, 1200, 2500, 5000, 10000, 40000])
    P0 = int(L * rng.uniform(0.02, 0.15))
    C_ = (L - P0) / P0
    k = round(rng.uniform(0.15, 0.8), 2)
    C_r = round(C_, 1)
    P = lambda t: L / (1 + C_r * math.exp(-k * t))
    what = pick(rng, [('fish in a lake', 'years'), ('people who have heard a rumour in a town', 'days'), ('deer in a nature reserve', 'years'), ('households with solar panels in a region', 'years'),
                      ('cells in a tumour model', 'days'), ('smartphone owners in a village', 'months')])
    desc = f'The number of {what[0]} t {what[1]} after observations began is modelled by N(t) = {L}/(1 + {_num(C_r)}e^(−{k}t)).'
    t1 = rng.randint(2, 15)
    if c == 'C1':
        if d <= 1:
            return nmcq(rng, f'{desc} Write down the carrying capacity.', L, [L / (1 + C_r), C_r, L * k], 'As t → ∞, N → L.', fmtf=lambda z: _num(round(z, 1)))
        return ret(f'{desc} Find (a) the initial number; (b) N({t1}).', f'(a) {sf(L / (1 + C_r))} (b) {sf(P(t1))}', f'(a) {L}/(1 + {_num(C_r)}) = {sf(L / (1 + C_r))} (A1). (b) {sf(P(t1))} (A1).', 2)
    if c == 'C2':
        return ret(f'{desc} Explain what happens to N(t) as t becomes large and interpret this in context.', f'N → {L}', f'R1 e^(−{k}t) → 0, so N → {L}/1 = {L}; R1 {L} is the carrying capacity – the maximum number the environment/population can sustain.', 2, 'explain')
    frac_ = rng.choice([0.5, 0.75, 0.9, 0.95])
    tt = -math.log((1 / frac_ - 1) / C_r) / k
    if c == 'C3':
        if rng.random() < 0.6:
            return ret(f'{desc} Find the time at which N reaches {int(frac_ * 100)}% of its carrying capacity.', f't = {sf(tt)} {what[1]}', f'{L}/(1 + {_num(C_r)}e^(−{k}t)) = {_num(frac_ * L)} (M1); GDC or logs (M1); t = {sf(tt)} (A1).', 3, 'numerical')
        a_, b_ = round(rng.uniform(1, 20), 1), round(rng.uniform(2, 12), 1)
        x0 = rng.randint(2, 60)
        y0 = round(a_ + b_ * math.log(x0 * 1.7), 1)
        x1 = math.exp((y0 - a_) / b_)
        return ret(f'The height h cm of a sapling x weeks after planting is modelled by h(x) = {a_} + {b_} ln x, x ≥ 1. Find h({x0}) and the time when h = {y0} cm.', f'h({x0}) = {sf(a_ + b_ * math.log(x0))} cm; x = {sf(x1)} weeks',
                   f'h({x0}) = {sf(a_ + b_ * math.log(x0))} (A1); ln x = ({y0} − {a_})/{b_} (M1); x = {sf(x1)} (A1).', 3, 'numerical')
    tinf = math.log(C_r) / k
    return ret(f'{desc} (a) Find the initial number and the carrying capacity. (b) Find the time at which the number reaches {int(frac_ * 100)}% of the carrying capacity. (c) The growth rate is greatest when N = {L // 2}; find this time. '
               f'(d) Compare the logistic model with an exponential model N = {sf(L / (1 + C_r))}e^({k}t) for large t.',
               f'(a) {sf(L / (1 + C_r))}, {L} (b) {sf(tt)} (c) {sf(tinf)} (d) the exponential grows without bound',
               f'(a) A1 A1. (b) M1 A1 {sf(tt)}. (c) 1 + {_num(C_r)}e^(−{k}t) = 2 (M1) ⇒ t = ln({_num(C_r)})/{k} = {sf(tinf)} (A1). (d) R1 similar for small t; R1 the exponential model exceeds the carrying capacity, the logistic levels off.',
               8, 'multi_step', gap='G5')


R.facts('ch09-st4', F(
    terms=[('log-log graph', 'a graph of log y against log x; data following y = axⁿ lie on a straight line with gradient n and intercept log a'),
           ('semi-log graph', 'a graph of log y against x; data following y = abˣ lie on a straight line with gradient log b and intercept log a'),
           ('linearisation', 'transforming variables (e.g. taking logarithms) so that a non-linear relationship appears as a straight line')],
    facts=[('If ln y plotted against ln x gives a straight line with gradient 1.5, which model fits?', 'y = ax^1.5', ['y = a(1.5)ˣ', 'y = 1.5x + a', 'y = a e^(1.5x)'], 'ln y = ln a + 1.5 ln x.'),
           ('If ln y against x is a straight line with gradient 0.2 and intercept 3, what is y?', 'y = e³e^(0.2x)', ['y = 3x^0.2', 'y = 0.2x + 3', 'y = 3e^(0.2x)'], 'ln y = 3 + 0.2x ⇒ y = e^(3 + 0.2x).')],
    why=[('Explain why taking logarithms of y = axⁿ produces a linear relationship.', 'log y = log a + n log x by the laws of logarithms, which is of the form Y = c + mX with Y = log y and X = log x.'),
         ('Explain why logarithmic scales are used to display earthquake magnitudes or the sizes of planets and atoms.', 'The values span many orders of magnitude; a log scale spaces powers of 10 equally so that very small and very large values can be shown and compared on one axis.')],
    misc=[('If a graph of log y against log x is a straight line, then y is a linear function of x.', 'It shows a power relationship y = axⁿ; y is linear in x only when n = 1.')],
))


@R.add('ch09-st4', ALL, (1, 5), 'short')
def linearise_core(rng, slot):
    c, d = slot.c, slot.d
    power = rng.random() < 0.5
    if power:
        a, n = round(rng.uniform(0.5, 8), 2), rng.choice([0.5, 1.5, 2, 2.5, 3, -1, -0.5, 0.75])
        xs = sorted(rng.sample([1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20], 6))
        ys = [float(sf(a * x ** n * rng.uniform(0.97, 1.03))) for x in xs]
        X, Y = np.log(xs), np.log(ys)
        g, i = np.polyfit(X, Y, 1)
        A = math.exp(i)
        model = f'y = {sf(A)}x^{sf(g)}'
        what = pick(rng, ['the period of a pendulum (y s) and its length (x m)', 'the power output of a wind turbine (y kW) and the wind speed (x m s⁻¹)', 'the mass (y g) and length (x cm) of a species of fish',
                          'the cost of a project (y thousand EUR) and its size (x hundred m²)'])
        axes = 'ln y against ln x'
    else:
        a, b = round(rng.uniform(2, 60), 1), round(rng.uniform(1.1, 1.8), 2) if rng.random() < 0.6 else round(rng.uniform(0.55, 0.9), 2)
        xs = list(range(0, 12, rng.choice([1, 2])))[:6]
        ys = [float(sf(a * b ** x * rng.uniform(0.97, 1.03))) for x in xs]
        X, Y = np.array(xs, float), np.log(ys)
        g, i = np.polyfit(X, Y, 1)
        A, B = math.exp(i), math.exp(g)
        model = f'y = {sf(A)} × {sf(B)}ˣ'
        what = pick(rng, ['the number of bacteria (y thousands) after x hours', 'the value of a painting (y thousand USD) x years after it was bought', 'the concentration of a drug (y mg L⁻¹) x hours after injection',
                          'the number of online orders (y hundreds) in week x of a campaign'])
        axes = 'ln y against x'
    tab = '; '.join(f'({_num(x)}, {_num(y)})' for x, y in zip(xs, ys))
    desc = f'Data on {what} are (x, y): {tab}.'
    if c == 'C1':
        return mcq(rng, f'{desc} Which graph would you plot to test whether a model of the form {"y = axⁿ" if power else "y = abˣ"} is appropriate?', axes,
                   [o for o in ['ln y against ln x', 'ln y against x', 'y against ln x', 'y against x²'] if o != axes][:3], f'{"ln y = ln a + n ln x" if power else "ln y = ln a + x ln b"} is linear in {"ln x" if power else "x"}.')
    if c == 'C2':
        return ret(f'{desc} Explain why plotting {axes} is a sensible way to test whether a model of the form {"y = axⁿ" if power else "y = abˣ"} fits these data, and state what the gradient and intercept would represent.',
                   f'gradient {"n" if power else "ln b"}, intercept ln a', f'R1 taking logs gives {"ln y = ln a + n ln x" if power else "ln y = ln a + x ln b"}, a straight line; A1 gradient {"n" if power else "ln b"}; A1 intercept ln a.', 3, 'explain')
    if c == 'C3':
        return ret(f'{desc} By finding the regression line of {axes}, find a model of the form {"y = axⁿ" if power else "y = abˣ"}.', model,
                   f'Transform the data (M1); regression line {axes.split(" against ")[0]} = {sf(g)}{"·ln x" if power else "x"} {sgn(i, fmtf=lambda z: sf(z))} (A1); a = e^{sf(i)} = {sf(A)} (A1); {"n = " + sf(g) if power else "b = e^" + sf(g) + " = " + sf(B)} (A1).', 4, 'numerical')
    xp = xs[-1] * 1.5
    pred = A * xp ** g if power else A * B ** xp
    r = pearson(X, Y)
    return ret(f'{desc} (a) Calculate the values needed to plot {axes}. (b) Find the equation of the regression line for the transformed data and the value of Pearson\'s r. (c) Hence find a model for y in terms of x. '
               f'(d) Use your model to estimate y when x = {_num(xp)} and comment on the reliability of this estimate.',
               f'(b) gradient {sf(g)}, intercept {m(sf(i))}, r = {sf(r)} (c) {model} (d) {sf(pred)}',
               f'(a) A1 transformed values. (b) A1 A1; r = {sf(r)} (A1). (c) M1 undo logs: {model} (A1 A1). (d) {sf(pred)} (A1); R1 strong linear fit of transformed data but x = {_num(xp)} is an extrapolation.', 9, 'multi_step', gap='G5')


# =============================================================================================
# ch10 Descriptive statistics
# =============================================================================================
SAMPLING = {
    'simple random sampling': ['Each of the {N} members of a sports club is given a number and {n} numbers are chosen using a random number generator.',
                               'The names of all {N} employees of a firm in {city} are put into a computer and {n} are selected at random.'],
    'systematic sampling': ['From an alphabetical list of {N} students, a starting point is chosen at random and then every {k}th student is selected.',
                            'A quality inspector tests every {k}th bottle coming off a production line of {N} bottles, starting from a randomly chosen bottle.'],
    'stratified sampling': ['A school of {N} students selects {n} students so that each year group is represented in proportion to its size, choosing randomly within each year group.',
                            'A survey of {N} residents of {city} selects {n} people with the proportions of each age group matching the population, chosen at random within each group.'],
    'quota sampling': ['An interviewer in a shopping centre in {city} questions the first {a} men and the first {b} women who agree to take part.',
                       'A researcher stops people in the street until she has interviewed {a} people under 30 and {b} people aged 30 or over.'],
    'convenience sampling': ['A student surveys the {n} people sitting nearest to her in the school canteen.',
                             'A reporter asks the first {n} people leaving a train station in {city} for their opinion.'],
    'cluster sampling': ['A city with {k} districts randomly chooses 3 districts and surveys every household in those districts.',
                         'A country randomly selects {k} schools and tests every student in those schools.'],
}
SAMPLING_ISSUE = {
    'simple random sampling': 'requires a complete sampling frame and may by chance under-represent a subgroup',
    'systematic sampling': 'can be biased if there is a pattern in the list that matches the interval',
    'stratified sampling': 'requires knowledge of the population structure and the strata sizes',
    'quota sampling': 'is not random – the interviewer chooses who to ask, so the sample may be biased',
    'convenience sampling': 'is not random and is unlikely to be representative of the population',
    'cluster sampling': 'clusters may differ from one another, so the sample may not reflect the whole population',
}

R.facts('ch10-st1', F(
    terms=[('population', 'the entire group about which information is wanted'),
           ('sample', 'a subset of the population from which data are collected'),
           ('sampling frame', 'a list of all members of the population from which a sample can be drawn'),
           ('outlier', 'a data value more than 1.5 × IQR below Q₁ or above Q₃'),
           ('discrete data', 'data that can take only distinct values, usually counts'),
           ('continuous data', 'data that can take any value in an interval, usually measurements')],
    facts=[('Which of the following is continuous data?', 'the time taken to run 100 m', ['the number of goals scored', 'shoe size', 'the number of siblings'], 'Time is measured and can take any value in an interval.'),
           ('A data value lies above Q₃ + 1.5 × IQR. How is it classified?', 'an outlier', ['the median', 'a quartile', 'the range'], 'IB definition of an outlier.')],
    why=[('Explain why a sample, rather than a census, is usually used in statistical investigations.', 'A census is often too expensive, slow or impossible (e.g. destructive testing); a well-chosen sample gives reliable information about the population at much lower cost.'),
         ('Explain why outliers should not automatically be removed from a data set.', 'An outlier may be a genuine, important value; it should be removed only if it is shown to be an error (e.g. a recording mistake), otherwise conclusions may be distorted.')],
    misc=[('A large sample is always representative of the population.', 'Size reduces random error but not bias: a large convenience sample can still be unrepresentative.')],
))


@R.add('ch10-st1', ALL, (1, 5), 'short')
def sampling_core(rng, slot):
    c, d = slot.c, slot.d
    meth = pick(rng, list(SAMPLING))
    N, n = rng.randint(200, 1500), rng.randint(20, 80)
    desc = pick(rng, SAMPLING[meth]).format(N=N, n=n, k=max(2, N // n), a=rng.randint(10, 40), b=rng.randint(10, 40), city=pick(rng, CITIES))
    if c == 'C1':
        return mcq(rng, f'{desc} Which sampling technique is being used?', meth, rng.sample([x for x in SAMPLING if x != meth], 3), f'This describes {meth}.')
    if c == 'C2':
        return ret(f'{desc} Identify the sampling technique and explain one disadvantage of using it here.', meth, f'A1 {meth}; R1 it {SAMPLING_ISSUE[meth]}; R1 linked to this context.', 3, 'explain')
    groups = rng.sample(['Year 7', 'Year 8', 'Year 9', 'Year 10', 'Year 11', 'Year 12'], rng.randint(3, 4))
    sizes = [rng.randint(80, 260) for _ in groups]
    tot = sum(sizes)
    ns = rng.choice([30, 40, 50, 60, 80])
    alloc = [s * ns / tot for s in sizes]
    if c == 'C3':
        if rng.random() < 0.5:
            return ret(f'A school has ' + ', '.join(f'{s} students in {g}' for s, g in zip(sizes, groups)) + f'. A stratified sample of {ns} students is taken. Find the number of students chosen from each year group.',
                       ', '.join(f'{g}: {round(a)}' for g, a in zip(groups, alloc)), 'Proportion × sample size (M1): ' + ', '.join(f'{s}/{tot} × {ns} = {sf(a)} ≈ {round(a)}' for s, a in zip(sizes, alloc)) + ' (A2). Check total.', 3, 'numerical')
        q1, q3 = rng.randint(20, 50), None
        q3 = q1 + rng.randint(8, 30)
        iqr = q3 - q1
        lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        test = [round(hi + rng.uniform(1, 10)), round(lo - rng.uniform(1, 10)), round(rng.uniform(q1, q3))]
        rng.shuffle(test)
        out = [t for t in test if t > hi or t < lo]
        return ret(f'For a data set Q₁ = {q1} and Q₃ = {q3}. Determine which of the values {", ".join(map(str, test))} are outliers.', ', '.join(map(str, sorted(out))) or 'none',
                   f'IQR = {iqr} (A1); fences {_num(lo)} and {_num(hi)} (M1 A1); outliers: {", ".join(map(str, sorted(out)))} (A1).', 4, 'numerical')
    return ret(f'A head teacher wants to survey students about a new timetable. The school has ' + ', '.join(f'{s} students in {g}' for s, g in zip(sizes, groups)) + f'. '
               f'(a) Explain why a stratified sample would be appropriate. (b) Find how many students from each year should be in a stratified sample of {ns}. (c) Describe how the students within each year group should be chosen. '
               f'(d) Give one reason why the results might still be biased.',
               '(b) ' + ', '.join(f'{g}: {round(a)}' for g, a in zip(groups, alloc)),
               f'(a) R1 opinions may differ between year groups, so each should be represented in proportion. (b) M1 A2 (' + ', '.join(f'{sf(a)}' for a in alloc) + '). (c) R1 simple random sampling from a list of each year group. '
               f'(d) R1 non-response, or students giving answers they think are expected.', 7, 'multi_step', gap='G5')


R.facts('ch10-st2', F(
    terms=[('cumulative frequency', 'the running total of frequencies up to the upper boundary of each class'),
           ('frequency histogram', 'a bar chart of grouped continuous data with no gaps between bars, bar heights showing frequency for equal class widths'),
           ('box-and-whisker plot', 'a diagram showing the minimum, Q₁, median, Q₃ and maximum (with outliers marked separately)'),
           ('modal class', 'the class with the highest frequency')],
    facts=[('On a cumulative frequency curve for 80 values, at what cumulative frequency is the upper quartile read?', '60', ['20', '40', '75'], 'Q₃ is at 3n/4 = 60.'),
           ('What is the mid-interval value of the class 20 ≤ x < 30?', '25', ['20', '30', '10'], '(20 + 30)/2.')],
    why=[('Explain why the mean calculated from a grouped frequency table is only an estimate.', 'The exact values within each class are unknown; the mid-interval value is used for every value in the class, assuming they are evenly spread.'),
         ('Explain why the median is often preferred to the mean for data such as house prices.', 'House prices are skewed by a few very expensive properties; the median is not affected by extreme values, so it better represents a typical price.')],
    misc=[('The median of grouped data is the mid-interval value of the middle class.', 'The median is estimated from the cumulative frequency graph at n/2 (or by interpolation within the median class), not by taking a class midpoint.')],
))


def _grouped(rng):
    w = rng.choice([5, 10, 20])
    start = rng.choice([0, 10, 20, 40, 100]) if w > 5 else rng.choice([0, 10, 20, 30])
    k = rng.randint(4, 6)
    freqs = [rng.randint(2, 25) for _ in range(k)]
    classes = [(start + i * w, start + (i + 1) * w) for i in range(k)]
    return classes, freqs, w


@R.add('ch10-st2', ALL, (1, 5), 'short')
def grouped_core(rng, slot):
    c, d = slot.c, slot.d
    classes, freqs, w = _grouped(rng)
    what = pick(rng, [('the times, t minutes, taken by students to travel to school', 't'), ('the masses, m kg, of suitcases checked in at an airport', 'm'),
                      ('the lengths, l cm, of fish caught in a lake', 'l'), ('the daily rainfall, r mm, at a weather station', 'r'), ('the heights, h cm, of seedlings', 'h')])
    v = what[1]
    tab = '; '.join(f'{a} ≤ {v} < {b}: {f}' for (a, b), f in zip(classes, freqs))
    n = sum(freqs)
    mids = [(a + b) / 2 for a, b in classes]
    mean = sum(mi * f for mi, f in zip(mids, freqs)) / n
    desc = f'The table shows {what[0]} (class: frequency): {tab}.'
    cum = np.cumsum(freqs)
    if c == 'C1':
        mi = int(np.argmax(freqs))
        if freqs.count(max(freqs)) > 1:
            return ret(f'{desc} Write down the total frequency and the cumulative frequency for {v} < {classes[2][1]}.', f'{n}; {cum[2]}', f'A1 {n}; A1 {cum[2]}.', 2)
        return mcq(rng, f'{desc} What is the modal class?', f'{classes[mi][0]} ≤ {v} < {classes[mi][1]}', [f'{a} ≤ {v} < {b}' for (a, b) in classes if (a, b) != classes[mi]][:3], 'The class with the highest frequency.')
    if c == 'C2':
        return ret(f'{desc} Estimate the mean, and explain why your answer is an estimate rather than the exact mean.', f'{sf(mean)}',
                   f'Mid-interval values {", ".join(_num(x) for x in mids)} (M1); Σfx/Σf = {_num(sum(mi * f for mi, f in zip(mids, freqs)))}/{n} = {sf(mean)} (A1); R1 actual values in each class are unknown – midpoints are assumed.', 3, 'explain')
    # median by interpolation
    def q_at(pos):
        for i, cf in enumerate(cum):
            if cf >= pos:
                prev = cum[i - 1] if i else 0
                a, b = classes[i]
                return a + (pos - prev) / freqs[i] * w
        return classes[-1][1]
    med, q1, q3 = q_at(n / 2), q_at(n / 4), q_at(3 * n / 4)
    if c == 'C3':
        return ret(f'{desc} (a) Construct a cumulative frequency table. (b) Use linear interpolation to estimate the median and the interquartile range.',
                   f'(a) ' + ', '.join(f'{v} < {b}: {cf}' for (a, b), cf in zip(classes, cum)) + f' (b) median ≈ {sf(med)}, IQR ≈ {sf(q3 - q1)}',
                   f'(a) A1 cumulative totals. (b) median at {_num(n / 2)} (M1): {sf(med)} (A1); Q₁ ≈ {sf(q1)}, Q₃ ≈ {sf(q3)} (A1); IQR ≈ {sf(q3 - q1)} (A1).', 5, 'numerical')
    # C4: box plot comparison from raw data
    g1 = sorted(rng.randint(20, 70) for _ in range(rng.randint(11, 15)))
    g2 = sorted(rng.randint(30, 85) for _ in range(rng.randint(11, 15)))
    g2[-1] = g2[-1] + rng.choice([0, 30])

    def five(xs):
        a = np.array(xs, float)
        q1_, q2_, q3_ = _quart(xs)
        return a.min(), q1_, q2_, q3_, a.max()
    f1, f2 = five(g1), five(g2)
    iqr2 = f2[3] - f2[1]
    outs = [x for x in g2 if x > f2[3] + 1.5 * iqr2 or x < f2[1] - 1.5 * iqr2]
    who = pick(rng, [('two classes', 'scores in a quiz out of 100'), ('two branches of a café', 'numbers of customers per hour'), ('two cyclists', 'weekly training distances (km)'), ('two call centres', 'call waiting times (s)')])
    return ret(f'Data for {who[0]}, {who[1]}: Group A: {", ".join(map(str, g1))}. Group B: {", ".join(map(str, g2))}. (a) Find the five-number summary for each group. (b) Determine whether group B contains any outliers. '
               f'(c) Draw box-and-whisker plots on the same scale. (d) Compare the two distributions, referring to a measure of centre and a measure of spread.',
               f'(a) A: {", ".join(_num(x) for x in f1)}; B: {", ".join(_num(x) for x in f2)} (b) {", ".join(map(str, outs)) if outs else "no outliers"}',
               f'(a) GDC 1-Var Stats (M1) A1 A1. (b) fences {_num(f2[1] - 1.5 * iqr2)}, {_num(f2[3] + 1.5 * iqr2)} (M1) → {", ".join(map(str, outs)) if outs else "none"} (A1). (c) A1 A1. '
               f'(d) R1 median of {"B" if f2[2] > f1[2] else "A"} is higher; R1 IQR A = {_num(f1[3] - f1[1])}, B = {_num(f2[3] - f2[1])}, comment on consistency.', 9, 'multi_step', gap='G5')


def _quart(xs):
    """Quartiles as on a TI/Casio GDC (median of lower/upper halves, excluding the median for odd n)."""
    a = sorted(xs)
    n = len(a)
    med = float(np.median(a))
    lower = a[: n // 2]
    upper = a[(n + 1) // 2:]
    return float(np.median(lower)), med, float(np.median(upper))


R.facts('ch10-st3', F(
    terms=[('standard deviation', 'a measure of spread: the square root of the mean of the squared deviations from the mean (σ on the GDC)'),
           ('interquartile range', 'IQR = Q₃ − Q₁, the range of the middle 50% of the data'),
           ('variance', 'the square of the standard deviation'),
           ('median', 'the middle value of the ordered data (mean of the two middle values when n is even)')],
    facts=[('Every value in a data set is increased by 5. What happens to the standard deviation?', 'It is unchanged', ['It increases by 5', 'It is multiplied by 5', 'It increases by 25'], 'Adding a constant shifts the data without changing spread.'),
           ('Every value in a data set is multiplied by 3. What happens to the variance?', 'It is multiplied by 9', ['It is multiplied by 3', 'It is unchanged', 'It increases by 3'], 'σ is multiplied by 3, so σ² by 9.'),
           ('Which measure of spread is not affected by outliers?', 'interquartile range', ['range', 'standard deviation', 'variance'], 'It uses only the middle 50%.')],
    why=[('Explain why adding the same constant to every data value changes the mean but not the standard deviation.', 'Every value and the mean move by the same amount, so each deviation from the mean is unchanged; σ depends only on these deviations.'),
         ('Explain why the standard deviation is more affected by an outlier than the interquartile range.', 'σ uses every value and squares the deviations, so one extreme value adds a large squared term; the IQR depends only on the quartiles.')],
    misc=[('If two data sets have the same mean, they must have the same spread.', 'The mean gives the centre only; data can be tightly clustered or widely spread about the same mean.')],
))


@R.add('ch10-st3', ALL, (1, 5), 'short')
def stats_core(rng, slot):
    c, d = slot.c, slot.d
    n = rng.randint(7, 12)
    xs = [rng.randint(10, 60) for _ in range(n)]
    a = np.array(xs, float)
    mean, sd = a.mean(), a.std()
    q1, med, q3 = _quart(xs)
    what = pick(rng, ['the number of minutes a group of students spent on homework', 'the daily maximum temperatures (°C) in a city', 'the ages of members of a chess club',
                      'the scores of a basketball team in recent games', 'the number of customers per hour at a café'])
    data = ', '.join(map(str, xs))
    if c == 'C1':
        if d <= 1:
            return nmcq(rng, f'The data are {what}: {data}. Find the median.', med, [mean, (a.max() + a.min()) / 2, sorted(xs)[n // 2 - 1] if n % 2 else sorted(xs)[n // 2]],
                        f'Ordered data: {", ".join(map(str, sorted(xs)))}; median = {_num(med)}.', fmtf=_num)
        return ret(f'The data are {what}: {data}. Find the mean and the range.', f'mean = {sf(mean)}, range = {int(a.max() - a.min())}', f'Σx/n = {int(a.sum())}/{n} = {sf(mean)} (A1); range = {int(a.max())} − {int(a.min())} = {int(a.max() - a.min())} (A1).', 2)
    if c == 'C2':
        p, q = rng.choice([2, 3, 1.5, 0.5, 10]), rng.randint(-20, 30)
        return ret(f'A data set has mean {sf(mean)} and standard deviation {sf(sd)}. Each value is transformed by y = {_num(p)}x {sgn(q)}. Find the new mean and standard deviation, explaining why the constant {m(q)} affects only one of them.',
                   f'mean {sf(p * mean + q)}, sd {sf(p * sd)}', f'new mean = {_num(p)} × {sf(mean)} {sgn(q)} = {sf(p * mean + q)} (A1); new sd = {_num(p)} × {sf(sd)} = {sf(p * sd)} (A1); R1 adding {m(q)} shifts all values and the mean equally, leaving deviations unchanged.', 3, 'explain')
    if c == 'C3':
        return ret(f'The data are {what}: {data}. Use your GDC to find the mean, the standard deviation, the median and the interquartile range.', f'mean {sf(mean)}, σ {sf(sd)}, median {_num(med)}, IQR {_num(q3 - q1)}',
                   f'A1 mean {sf(mean)}; A1 σ = {sf(sd)}; A1 median {_num(med)}; A1 IQR = {_num(q3)} − {_num(q1)} = {_num(q3 - q1)}.', 4, 'numerical')
    # C4: combined means / missing value
    n1, n2 = rng.randint(12, 30), rng.randint(12, 30)
    m1, m2 = round(rng.uniform(50, 80), 1), round(rng.uniform(50, 80), 1)
    comb = (n1 * m1 + n2 * m2) / (n1 + n2)
    target = round(comb + rng.uniform(0.5, 2), 1)
    xnew = target * (n1 + n2 + 1) - (n1 * m1 + n2 * m2)
    return ret(f'In a mathematics test, class A ({n1} students) had a mean score of {m1} and class B ({n2} students) had a mean of {m2}. (a) Find the mean score of all {n1 + n2} students. '
               f'(b) A new student takes the test and the overall mean becomes {target}. Find the new student\'s score. (c) Explain why the overall mean is not simply ({m1} + {m2})/2. '
               f'(d) The teacher adds 5 marks to every score. State the effect on the mean and on the standard deviation.',
               f'(a) {sf(comb)} (b) {sf(xnew)} (c) classes differ in size (d) mean +5, sd unchanged',
               f'(a) ({n1} × {m1} + {n2} × {m2})/{n1 + n2} (M1) = {sf(comb)} (A1). (b) {target} × {n1 + n2 + 1} − {_num(n1 * m1 + n2 * m2)} (M1) = {sf(xnew)} (A1). (c) R1 weighted by class size. (d) A1 mean increases by 5; A1 sd unchanged.',
               7, 'multi_step', gap='G5')


@R.add('ch10-st3', ('C3', 'C4'), (1, 5), 'numerical')
def freq_table_stats(rng, slot):
    vals = sorted(rng.sample(range(0, 9), 5))
    fr = [rng.randint(2, 20) for _ in vals]
    a = np.repeat(vals, fr)
    mean, sd = a.mean(), a.std()
    what = pick(rng, ['the number of books read last month by students', 'the number of goals scored per match by a team', 'the number of people living in each house on a street', 'the number of emails received per hour'])
    tab = '; '.join(f'{v}: {f}' for v, f in zip(vals, fr))
    q1, med, q3 = _quart(list(a))
    if slot.c == 'C3':
        return ret(f'The table shows {what} (value: frequency): {tab}. Find the mean and standard deviation.', f'mean {sf(mean)}, σ {sf(sd)}', f'Σfx/Σf = {int(a.sum())}/{len(a)} (M1) = {sf(mean)} (A1); σ = {sf(sd)} (A1).', 3, 'numerical')
    k = rng.choice([2, 3])
    return ret(f'The table shows {what} (value: frequency): {tab}. (a) Find the mean, standard deviation, median and IQR. (b) Each value is multiplied by {k} and then 1 is added. Write down the new mean, standard deviation and IQR. '
               f'(c) Explain why the IQR and the standard deviation respond to the transformation in the same way.',
               f'(a) {sf(mean)}, {sf(sd)}, {_num(med)}, {_num(q3 - q1)} (b) {sf(k * mean + 1)}, {sf(k * sd)}, {_num(k * (q3 - q1))}',
               f'(a) A1 A1 A1 A1. (b) A1 {sf(k * mean + 1)}; A1 {sf(k * sd)}; A1 {_num(k * (q3 - q1))}. (c) R1 both measure spread and are scaled by |{k}| but not changed by adding a constant.', 8, 'multi_step', gap='G5')


R.facts('ch10-st4', F(
    terms=[('reliability', 'the extent to which a measurement or survey gives consistent results when repeated under the same conditions'),
           ('validity', 'the extent to which a test or survey measures what it is intended to measure'),
           ('test-retest reliability', 'checking reliability by giving the same test to the same group on two occasions and correlating the results'),
           ('parallel forms reliability', 'checking reliability by giving two equivalent versions of a test to the same group and correlating the results'),
           ('content validity', 'how well a test covers all aspects of what it is supposed to measure'),
           ('criterion-related validity', 'how well results agree with an established external measure (criterion) of the same thing')],
    facts=[('A teacher gives the same questionnaire to a class twice, two weeks apart, and correlates the scores. What is being assessed?', 'test-retest reliability', ['content validity', 'criterion-related validity', 'parallel forms reliability'], 'Same test, same people, two occasions.'),
           ('A new short fitness test is compared with results from a full laboratory test. What is being checked?', 'criterion-related validity', ['test-retest reliability', 'parallel forms reliability', 'content validity'], 'Agreement with an established criterion.'),
           ('Which is a reason to choose a discrete rather than a continuous variable in a survey?', 'the quantity is counted, such as the number of visits', ['the quantity is measured, such as height', 'it gives a larger sample', 'it removes bias'], 'Counts are discrete.')],
    why=[('Explain why a survey question such as "Don\'t you agree that the new park is a waste of money?" reduces the validity of the results.', 'It is a leading question that pushes respondents towards one answer, so responses reflect the wording rather than true opinions – the survey does not measure what it intends to.'),
         ('Explain the difference between reliability and validity, using a bathroom scale as an example.', 'A scale that always reads 2 kg too heavy is reliable (consistent) but not valid (inaccurate); a valid scale must give the true mass, and to be useful it must also be reliable.'),
         ('Explain why the number of classes chosen for grouped data affects how the data appear.', 'Too few classes hide the shape of the distribution; too many leave classes with very low frequencies and make the pattern noisy; typically 5–10 classes balance detail and clarity.')],
    misc=[('If a test is reliable then it must also be valid.', 'Reliability is consistency; a test can consistently measure the wrong thing (reliable but not valid).')],
    evaluate=[('Online surveys are the best way to collect data about the reading habits of teenagers.', ['cheap, fast and reach many teenagers', 'anonymity may encourage honest answers'], ['self-selection bias: keen readers more likely to respond', 'excludes those without internet access', 'cannot check who answers'],
               'Online surveys are convenient but likely biased; combining them with a stratified sample in schools would improve validity.')],
))


@R.add('ch10-st4', ALL, (1, 5), 'short')
def reliability_core(rng, slot):
    c, d = slot.c, slot.d
    n = rng.randint(8, 10)
    t1 = [rng.randint(40, 95) for _ in range(n)]
    noise = rng.choice([3, 6, 12, 20])
    t2 = [max(0, min(100, x + rng.randint(-noise, noise))) for x in t1]
    r = pearson(t1, t2)
    test = pick(rng, ['an anxiety questionnaire', 'a reading-speed test', 'a reaction-time app', 'a survey on attitudes to recycling', 'a short mathematics aptitude test'])
    if c == 'C1':
        kind = pick(rng, ['test-retest reliability', 'parallel forms reliability', 'content validity', 'criterion-related validity'])
        desc = {'test-retest reliability': f'The same {test} is given to the same {n} people one week apart and the scores are compared.',
                'parallel forms reliability': f'Two different but equivalent versions of {test} are given to the same {n} people and the scores are compared.',
                'content validity': f'Experts check whether the items of {test} cover every aspect of the topic it is meant to assess.',
                'criterion-related validity': f'Scores on {test} are compared with scores from a well-established measure of the same thing.'}[kind]
        return mcq(rng, f'{desc} What is being assessed?', kind, [k for k in ['test-retest reliability', 'parallel forms reliability', 'content validity', 'criterion-related validity'] if k != kind], f'This is {kind}.')
    if c == 'C2':
        return ret(f'To check {test}, a researcher gives it to {n} people and repeats it a week later; Pearson\'s r between the two sets of scores is {sf(r)}. Explain what this suggests about the reliability of the test.',
                   'reliable' if r > 0.8 else 'questionable reliability', f'R1 this is a test-retest check of reliability; R1 r = {sf(r)} indicates a {strength(r)} correlation, so the test {"gives consistent results" if r > 0.8 else "may not give consistent results"}.', 2, 'explain')
    tab = '; '.join(f'({a}, {b})' for a, b in zip(t1, t2))
    if c == 'C3':
        return ret(f'{n} people take {test} twice, one month apart. Their scores (first, second) are: {tab}. Calculate Pearson\'s r and state what kind of reliability is being tested.', f'r = {sf(r)}; test-retest reliability',
                   f'GDC (M1); r = {sf(r)} (A1); test-retest (A1).', 3, 'numerical')
    return ret(f'A psychologist designs {test}. {n} volunteers take it twice, one month apart; their scores (first, second) are: {tab}. (a) Calculate Pearson\'s r. (b) Comment on the reliability of the test. '
               f'(c) Suggest a way to assess the validity of the test. (d) Explain one reason why a high value of r does not, on its own, show that the test is useful.',
               f'(a) r = {sf(r)} (b) {strength(r)} correlation (c) criterion-related or content validity (d) consistent but may measure the wrong thing',
               f'(a) M1 A1. (b) R1 {strength(r)} ⇒ {"reliable" if r > 0.8 else "doubtful reliability"}. (c) R1 compare with an established measure (criterion) or have experts check content. (d) R1 reliability ≠ validity; small sample of {n}.',
               7, 'multi_step', gap='G5')


# =============================================================================================
# ch11 Correlation and regression
# =============================================================================================
BIV = [
    ('the hours of revision (x) and the test score (y) of students', (1, 15), (2.0, 5.0), (25, 45)),
    ('the outside temperature in °C (x) and the number of ice creams sold (y) at a kiosk', (12, 34), (4.0, 9.0), (-40, 10)),
    ('the engine size in litres (x) and the fuel consumption in km per litre (y) of cars', (1.0, 3.5), (-4.0, -2.0), (22, 26)),
    ('the age in years (x) and the price in thousands of EUR (y) of used cars', (1, 12), (-1.8, -0.9), (24, 32)),
    ('the arm span in cm (x) and the height in cm (y) of students', (150, 190), (0.8, 1.0), (10, 30)),
    ('the advertising spend in thousands of USD (x) and the monthly sales in thousands of USD (y) of a company', (5, 40), (2.5, 6.0), (30, 80)),
    ('the latitude in degrees (x) and the mean annual temperature in °C (y) of cities', (5, 60), (-0.7, -0.4), (28, 33)),
]


def _biv(rng, n=None, noise=None):
    desc, (lo, hi), (g1, g2), (c1, c2) = pick(rng, BIV)
    n = n or rng.randint(7, 10)
    grad, ic = rng.uniform(g1, g2), rng.uniform(c1, c2)
    dec = 1 if hi <= 5 else 0
    xs = set()
    for _ in range(200):
        xs.add(round(rng.uniform(lo, hi), dec))
        if len(xs) == n:
            break
    xs = sorted(xs)
    spread = (abs(grad) * (hi - lo)) * (noise if noise is not None else rng.choice([0.05, 0.1, 0.2, 0.35]))
    ys = [round(grad * x + ic + rng.gauss(0, spread), 1) for x in xs]
    if len(set(xs)) < n:
        return None
    return desc, xs, ys


def _fmt_pairs(xs, ys):
    return '; '.join(f'({m(_num(x))}, {m(_num(y))})' for x, y in zip(xs, ys))


R.facts('ch11-st1', F(
    terms=[('bivariate data', 'data with two variables recorded for each individual, displayed on a scatter diagram'),
           ("Pearson's product-moment correlation coefficient", 'r, −1 ≤ r ≤ 1, measuring the strength and direction of the linear relationship between two variables'),
           ('regression line of y on x', 'the least-squares line y = ax + b used to predict y from a given x'),
           ('mean point', '(x̄, ȳ), through which every least-squares regression line passes')],
    facts=[('A value of r = −0.92 indicates…', 'a strong negative linear correlation', ['a weak negative correlation', 'no correlation', 'a strong positive correlation'], '|r| close to 1, negative sign.'),
           ('Through which point does the regression line of y on x always pass?', '(x̄, ȳ)', ['(0, 0)', '(0, ȳ)', '(x̄, 0)'], 'Property of least squares.'),
           ('A strong correlation between two variables shows that…', 'they are linearly associated, not necessarily causally related', ['one causes the other', 'they are independent', 'the regression line passes through the origin'], 'Correlation does not imply causation.')],
    why=[('Explain why a strong correlation between ice-cream sales and drowning incidents does not mean that eating ice cream causes drowning.', 'Both increase with a third variable – hot weather – which leads to more ice-cream sales and more swimming; the correlation is not causal.'),
         ('Explain why the regression line of y on x should only be used to predict y from x and not x from y.', 'It minimises vertical (y) residuals; predicting x from y would require the line minimising horizontal residuals (x on y), which differs unless r = ±1.')],
    misc=[('r = 0 means there is no relationship between the variables.', 'r = 0 means no linear relationship; a strong non-linear (e.g. quadratic) relationship can still exist.')],
))


@R.add('ch11-st1', ALL, (1, 5), 'short')
def regression_core(rng, slot):
    c, d = slot.c, slot.d
    res = _biv(rng)
    if res is None:
        return None
    desc, xs, ys = res
    r = pearson(xs, ys)
    a, b = np.polyfit(xs, ys, 1)
    data = _fmt_pairs(xs, ys)
    stem0 = f'The table shows {desc}: {data}.'
    if c == 'C1':
        if d <= 1:
            return mcq(rng, f'{stem0} Pearson\'s r for these data is {sf(r)}. Which description is correct?', strength(r) + ' correlation',
                       [w + ' correlation' for w in ['strong positive', 'strong negative', 'weak positive', 'weak negative', 'moderate positive', 'moderate negative', 'very weak or no linear'] if w != strength(r)][:3],
                       f'|r| = {sf(abs(r))}: {strength(r)}.')
        return ret(f'{stem0} Use your GDC to find Pearson\'s product-moment correlation coefficient r and describe the correlation.', f'r = {sf(r)}; {strength(r)}', f'r = {sf(r)} (A1); {strength(r)} (A1).', 2)
    if c == 'C2':
        return ret(f'{stem0} The regression line of y on x is y = {sf(a)}x {sgn(b, fmtf=sf)}. Interpret the gradient and the y-intercept in context, and comment on whether the intercept is meaningful.',
                   f'gradient {sf(a)}: change in y per unit increase in x', f'R1 for each additional unit of x, y changes by {sf(a)} on average; R1 intercept {sf(b)} is the predicted y when x = 0; R1 {"x = 0 is outside the data, so the intercept has little practical meaning" if min(xs) > 0.2 * max(xs) else "x = 0 is close to the data range"}.',
                   3, 'explain')
    x0 = round(rng.uniform(min(xs), max(xs)), 1)
    if c == 'C3':
        return ret(f'{stem0} (a) Find the equation of the regression line of y on x. (b) Use it to estimate y when x = {_num(x0)}.', f'(a) y = {sf(a)}x {sgn(b, fmtf=sf)} (b) {sf(a * x0 + b)}',
                   f'(a) GDC (M1); a = {sf(a)}, b = {sf(b)} (A1 A1). (b) {sf(a)} × {_num(x0)} {sgn(b, fmtf=sf)} = {sf(a * x0 + b)} (A1). Accept answers from the unrounded line.', 4, 'numerical')
    xb, yb = float(np.mean(xs)), float(np.mean(ys))
    x1 = round(max(xs) * rng.uniform(1.6, 2.5), 1)
    return ret(f'{stem0} (a) Find the mean point (x̄, ȳ). (b) Find r and the equation of the regression line of y on x. (c) Show that the line passes through the mean point. (d) Estimate y when x = {_num(x0)} and when x = {_num(x1)}, and comment on the reliability of each estimate.',
               f'(a) ({sf(xb)}, {sf(yb)}) (b) r = {sf(r)}; y = {sf(a)}x {sgn(b, fmtf=sf)} (d) {sf(a * x0 + b)}; {sf(a * x1 + b)}',
               f'(a) A1 A1. (b) r = {sf(r)} (A1); line (A1 A1). (c) {sf(a)} × {sf(xb)} {sgn(b, fmtf=sf)} = {sf(a * xb + b)} ≈ ȳ (R1). (d) {sf(a * x0 + b)} (A1) reliable – interpolation with {strength(r)} correlation (R1); {sf(a * x1 + b)} (A1) unreliable – extrapolation (R1).',
               10, 'multi_step', gap='G5')


R.facts('ch11-st2', F(
    terms=[('interpolation', 'predicting a value within the range of the observed data'),
           ('extrapolation', 'predicting a value outside the range of the observed data, which is less reliable'),
           ('piecewise linear model', 'a model that uses different straight lines over different intervals of the data')],
    facts=[('Data on x were collected for 10 ≤ x ≤ 50. Predicting y at x = 70 is an example of…', 'extrapolation', ['interpolation', 'correlation', 'regression of x on y'], '70 lies outside the data range.'),
           ('Which prediction is most reliable?', 'interpolation with |r| close to 1', ['extrapolation with |r| close to 1', 'interpolation with r close to 0', 'extrapolation with r close to 0'], 'Strong correlation and within the data range.')],
    why=[('Explain why extrapolation can give unrealistic predictions even when r is close to 1.', 'The linear pattern is only observed within the data range; outside it the relationship may change (e.g. limits, saturation), so the model need not hold.'),
         ('Explain why a piecewise linear model may be better than a single regression line for some data.', 'If the rate of change clearly differs between two parts of the data (e.g. before and after a policy change), separate lines fit each part much better than one line.')],
    misc=[('A prediction is reliable as long as it is made with the regression line.', 'Reliability also depends on the strength of correlation and on whether the value lies within the data range.')],
))


@R.add('ch11-st2', ALL, (1, 5), 'short')
def interp_core(rng, slot):
    c, d = slot.c, slot.d
    res = _biv(rng)
    if res is None:
        return None
    desc, xs, ys = res
    r = pearson(xs, ys)
    a, b = np.polyfit(xs, ys, 1)
    lo, hi = min(xs), max(xs)
    xin = round(rng.uniform(lo, hi), 1)
    xout = round(hi + (hi - lo) * rng.uniform(0.5, 1.5), 1)
    line = f'y = {sf(a)}x {sgn(b, fmtf=sf)}'
    if c == 'C1':
        x0 = pick(rng, [xin, xout])
        kind = 'interpolation' if lo <= x0 <= hi else 'extrapolation'
        return mcq(rng, f'Data on {desc} were collected for {_num(lo)} ≤ x ≤ {_num(hi)}. Using the regression line to estimate y at x = {_num(x0)} is an example of what?', kind,
                   [k for k in ['interpolation', 'extrapolation', 'causation', 'stratification'] if k != kind], f'{_num(x0)} lies {"inside" if kind == "interpolation" else "outside"} the data range.')
    if c == 'C2':
        return ret(f'For {desc}, data were collected for {_num(lo)} ≤ x ≤ {_num(hi)}; r = {sf(r)} and the regression line is {line}. {name(rng)} uses it to predict y for x = {_num(xin)} and x = {_num(xout)}. Comment on the reliability of each prediction.',
                   f'{sf(a * xin + b)} fairly reliable; {sf(a * xout + b)} unreliable', f'A1 {sf(a * xin + b)}; R1 interpolation{" with " + strength(r) + " correlation" if abs(r) > 0.5 else " but correlation is weak"}; A1 {sf(a * xout + b)}; R1 extrapolation – unreliable.', 4, 'explain')
    # piecewise: two regimes
    x1 = list(range(0, 6))
    g1, g2 = round(rng.uniform(1.2, 3.0), 1), round(rng.uniform(4.0, 8.0), 1)
    c0 = rng.randint(10, 40)
    y1 = [round(c0 + g1 * x + rng.uniform(-0.6, 0.6), 1) for x in x1]
    x2 = list(range(5, 11))
    y2 = [round(c0 + g1 * 5 + g2 * (x - 5) + rng.uniform(-0.8, 0.8), 1) for x in x2]
    y2[0] = y1[-1]  # the x = 5 point is shared and shown once
    a1, b1 = np.polyfit(x1, y1, 1)
    a2, b2 = np.polyfit(x2, y2, 1)
    xs_all, ys_all = x1 + x2[1:], y1 + y2[1:]
    ctx = pick(rng, ['the number of subscribers (thousands) to a streaming service in each month of a year, before and after a price cut in month 5', 'the water level (cm) in a reservoir each week, before and after heavy rains began in week 5',
                     'the daily number of visitors (hundreds) to a museum before and after a new exhibition opened on day 5'])
    if c == 'C3':
        x0 = round(rng.uniform(6, 10), 1)
        return ret(f'The data show {ctx}: {_fmt_pairs(xs_all, ys_all)}. A piecewise linear model uses the regression line for 0 ≤ x ≤ 5 and a separate regression line for 5 ≤ x ≤ 10. Find both lines and use the model to estimate y at x = {_num(x0)}.',
                   f'y = {sf(a1)}x {sgn(b1, fmtf=sf)} (0 ≤ x ≤ 5); y = {sf(a2)}x {sgn(b2, fmtf=sf)} (5 ≤ x ≤ 10); {sf(a2 * x0 + b2)}',
                   f'First line (A1 A1); second line using points with x ≥ 5 (M1 A1); estimate {sf(a2 * x0 + b2)} (A1).', 5, 'numerical')
    aa, bb = np.polyfit(xs_all, ys_all, 1)
    sse1 = sum((y - (aa * x + bb)) ** 2 for x, y in zip(xs_all, ys_all))
    sse2 = sum((y - (a1 * x + b1)) ** 2 for x, y in zip(x1, y1)) + sum((y - (a2 * x + b2)) ** 2 for x, y in zip(x2[1:], y2[1:]))
    return ret(f'The data show {ctx}: {_fmt_pairs(xs_all, ys_all)}. (a) Find the regression line for all the data. (b) Find separate regression lines for 0 ≤ x ≤ 5 and 5 ≤ x ≤ 10. (c) Compare the two models using the sum of squared residuals. '
               f'(d) Interpret the change in gradient in context and explain which model should be used for a prediction at x = 12.',
               f'(a) y = {sf(aa)}x {sgn(bb, fmtf=sf)} (b) {sf(a1)}x {sgn(b1, fmtf=sf)}; {sf(a2)}x {sgn(b2, fmtf=sf)} (c) SSres {sf(sse1)} vs {sf(sse2)}',
               f'(a) A1 A1. (b) A1 A1. (c) SSres single = {sf(sse1)}, piecewise = {sf(sse2)} (M1 A1); R1 piecewise fits better. (d) R1 rate increased from {sf(a1)} to {sf(a2)} per unit; R1 use the second line, noting x = 12 is an extrapolation.',
               10, 'multi_step', gap='G5')


R.facts('ch11-st3', F(
    terms=[("Spearman's rank correlation coefficient", 'r_s, Pearson\'s r applied to the ranks of the data; it measures the strength of a monotonic relationship'),
           ('monotonic relationship', 'a relationship in which one variable always increases (or always decreases) as the other increases, not necessarily linearly'),
           ('tied ranks', 'equal data values, each given the mean of the ranks they would occupy')],
    facts=[('Two values tie for 3rd and 4th place. What rank does each receive?', '3.5', ['3', '4', '7'], 'Mean of 3 and 4.'),
           ('When is Spearman\'s r_s more appropriate than Pearson\'s r?', 'when the relationship is monotonic but not linear, or the data are ranks', ['when the data are exactly linear', 'when the sample is large', 'when there are no outliers'], 'r_s depends only on order.'),
           ('If r_s = 1, what must be true?', 'the ranks of x and y agree exactly', ['the points lie on a straight line', 'x = y for every point', 'r = 1'], 'Perfect agreement of rankings.')],
    why=[('Explain why Spearman\'s rank correlation is less affected by an outlier than Pearson\'s r.', 'An outlier only changes the rank by at most one place relative to its neighbours, whereas its actual value can greatly change the mean and Pearson\'s r.'),
         ('Explain why data following y = eˣ for x = 1, …, 6 give r_s = 1 but r < 1.', 'y always increases with x, so the rankings agree perfectly (r_s = 1), but the points lie on a curve, not a line, so r < 1.')],
    misc=[('Spearman\'s coefficient measures how close the points are to a straight line.', 'That is Pearson\'s r; Spearman\'s measures how consistently y increases (or decreases) with x.')],
))


@R.add('ch11-st3', ALL, (1, 5), 'short')
def spearman_core(rng, slot):
    c, d = slot.c, slot.d
    n = rng.randint(6, 9)
    judges = pick(rng, [('two judges scored the same {n} dancers in a competition', 'Judge A', 'Judge B'), ('the marks (%) of {n} students in a mock examination and in the final examination', 'Mock', 'Final'),
                        ('the price (EUR) and customer rating (out of 100) of {n} pairs of headphones', 'Price', 'Rating'), ('the distance from a factory (km) and lichen coverage (%) at {n} sites', 'Distance', 'Coverage')])
    base = sorted(rng.sample(range(10, 99), n))
    xs = [round(v, 0) for v in base]
    ys = [min(99, max(1, round(v * rng.uniform(0.6, 1.4) + rng.uniform(-15, 15), 0))) for v in base]
    if rng.random() < 0.4:
        ys[rng.randrange(n)] = ys[rng.randrange(n)]  # create a tie
    rs = spearman(xs, ys)
    rp = pearson(xs, ys)
    lab = judges[0].format(n=n)
    tab = '; '.join(f'({int(x)}, {int(y)})' for x, y in zip(xs, ys))
    rx, ry = ranks(xs), ranks(ys)
    if c == 'C1':
        vals = [int(y) for y in ys]
        return ret(f'Rank the following values from largest (rank 1) to smallest, giving tied values the mean rank: {", ".join(map(str, vals))}.', ', '.join(_num(r_) for r_ in ry),
                   f'Ranks: {", ".join(_num(r_) for r_ in ry)} (A2; A1 if one error or ties not averaged).', 2)
    if c == 'C2':
        return ret(f'The data show {lab} ({judges[1]}, {judges[2]}): {tab}. Here r = {sf(rp)} and r_s = {sf(rs)}. Explain what each coefficient measures and why they may differ.', f'r measures linear, r_s monotonic association',
                   f'R1 r measures the strength of the linear relationship; R1 r_s measures how well the rankings agree (monotonic relationship); R1 they differ because the relationship is not exactly linear/ranks ignore spacing.', 3, 'explain')
    if c == 'C3':
        return ret(f'The data show {lab} ({judges[1]}, {judges[2]}): {tab}. Calculate Spearman\'s rank correlation coefficient and interpret it.', f'r_s = {sf(rs)}; {strength(rs)} agreement',
                   f'Ranks x: {", ".join(_num(r_) for r_ in rx)}; ranks y: {", ".join(_num(r_) for r_ in ry)} (M1 A1); r_s = Pearson\'s r of the ranks = {sf(rs)} (A1); {strength(rs)} (R1).', 4, 'numerical')
    xs2 = list(range(1, n + 1))
    ys2 = [round(rng.choice([2, 3, 5]) * 1.6 ** x, 1) for x in xs2]
    ys2 = sorted(ys2)
    return ret(f'The data show {lab} ({judges[1]}, {judges[2]}): {tab}. (a) Calculate Spearman\'s rank correlation coefficient. (b) Calculate Pearson\'s r. (c) The data set (x, y): {_fmt_pairs(xs2, ys2)} follows an exponential pattern; find r and r_s for it. '
               f'(d) Explain which coefficient is more appropriate for the second data set.',
               f'(a) {sf(rs)} (b) {sf(rp)} (c) r = {sf(pearson(xs2, ys2))}, r_s = {sf(spearman(xs2, ys2))} (d) Spearman',
               f'(a) M1 A1. (b) A1. (c) A1 A1. (d) R1 the relationship is monotonic but not linear, so r_s (= 1) describes it fully while r underestimates it.', 7, 'multi_step', gap='G5')


R.facts('ch11-st4', F(
    terms=[('coefficient of determination', 'R², the proportion of the variation in y explained by the model, R² = 1 − SSres/SStot'),
           ('least-squares regression', 'choosing the parameters of a model to minimise the sum of squared residuals'),
           ('non-linear regression', 'fitting a curve (quadratic, cubic, exponential, power, sine) to bivariate data, usually with technology')],
    facts=[('A quadratic model has R² = 0.94. What does this mean?', '94% of the variation in y is explained by the model', ['the model is correct 94% of the time', 'r = 0.94', '94% of the points lie on the curve'], 'Definition of R².'),
           ('For a linear model, how is R² related to Pearson\'s r?', 'R² = r²', ['R² = r', 'R² = √r', 'R² = 1 − r'], 'For least-squares lines R² equals r².')],
    why=[('Explain why a cubic model will always have an R² at least as large as a quadratic model fitted to the same data.', 'A cubic includes every quadratic (with zero x³ coefficient) as a special case, so its least-squares fit can be no worse; this is why R² alone should not decide model choice.'),
         ('Explain why a model with a high R² may still be inappropriate for prediction.', 'It may fit the observed data well but behave unrealistically outside the data range or contradict the context (e.g. predicting negative sales).')],
    misc=[('R² = 0.81 means the correlation coefficient is 0.81.', 'For a linear model R² = r², so r = ±0.9; R² measures the proportion of variation explained.')],
))


@R.add('ch11-st4', ALL, (1, 5), 'short')
def nonlin_core(rng, slot):
    c, d = slot.c, slot.d
    kind = rng.randint(0, 1)
    if kind == 0:
        a, b, c0 = round(rng.uniform(-1.5, -0.2), 2), round(rng.uniform(4, 15), 1), round(rng.uniform(5, 40), 1)
        xs = list(range(1, rng.randint(8, 11)))
        ys = [round(a * x * x + b * x + c0 + rng.gauss(0, 1.5), 1) for x in xs]
        deg = 2
        ctx = pick(rng, ['the yield (kg) of a crop against the amount of fertiliser (x × 10 kg ha⁻¹)', 'the profit (thousand USD) of a firm against the price charged (x USD)', 'the height (m) of a drone x seconds after launch'])
    else:
        xs = list(range(0, rng.randint(7, 10)))
        a3, a2, a1, a0 = round(rng.uniform(0.05, 0.3), 2), round(rng.uniform(-3, -1), 1), round(rng.uniform(5, 12), 1), round(rng.uniform(10, 30), 1)
        ys = [round(a3 * x ** 3 + a2 * x ** 2 + a1 * x + a0 + rng.gauss(0, 1.2), 1) for x in xs]
        deg = 3
        ctx = pick(rng, ['the number of visitors (hundreds) to a park x hours after 8 am', 'the energy demand (GW) of a city x hours after midnight', 'the river flow (m³ s⁻¹) x days after a storm'])
    cf = np.polyfit(xs, ys, deg)
    fit = np.polyval(cf, xs)
    sst = sum((y - np.mean(ys)) ** 2 for y in ys)
    sse = sum((y - f) ** 2 for y, f in zip(ys, fit))
    R2 = 1 - sse / sst
    lcf = np.polyfit(xs, ys, 1)
    R2l = pearson(xs, ys) ** 2
    model = 'y = ' + poly([sfv(v) for v in cf])
    tab = _fmt_pairs(xs, ys)
    desc = f'The data show {ctx}: {tab}.'
    if c == 'C1':
        return mcq(rng, f'{desc} A {["", "", "quadratic", "cubic"][deg]} model gives R² = {sf(R2)}. Which statement is correct?', f'{sf(R2 * 100)}% of the variation in y is explained by the model',
                   [f'the model is correct {sf(R2 * 100)}% of the time', f'Pearson\'s r is {sf(R2)}', f'{sf(R2 * 100)}% of the points lie on the curve'], 'R² is the proportion of variation explained.')
    if c == 'C2':
        return ret(f'{desc} A linear model has R² = {sf(R2l)} and a {["", "", "quadratic", "cubic"][deg]} model has R² = {sf(R2)}. Explain which model is more appropriate, referring to both R² and the context.',
                   f'{["", "", "quadratic", "cubic"][deg]} model', f'R1 R² = {sf(R2)} > {sf(R2l)}: the {["", "", "quadratic", "cubic"][deg]} explains more variation; R1 the context shows a rise and fall/turning behaviour that a line cannot capture.', 3, 'explain')
    if c == 'C3':
        return ret(f'{desc} Use technology to find the {["", "", "quadratic", "cubic"][deg]} regression model and its coefficient of determination R².', f'{model}; R² = {sf(R2)}',
                   f'GDC {"QuadReg" if deg == 2 else "CubicReg"} (M1); coefficients (A2); R² = {sf(R2)} (A1).', 4, 'numerical')
    xp = xs[-1] + rng.randint(2, 5)
    return ret(f'{desc} (a) Find the linear regression model and its R². (b) Find the {["", "", "quadratic", "cubic"][deg]} model and its R². (c) Use the better model to predict y at x = {xs[len(xs) // 2]} and at x = {xp}. '
               f'(d) Discuss the validity of each prediction.',
               f'(a) y = {sf(lcf[0])}x {sgn(lcf[1], fmtf=sf)}, R² = {sf(R2l)} (b) {model}, R² = {sf(R2)} (c) {sf(np.polyval(cf, xs[len(xs) // 2]))}; {sf(np.polyval(cf, xp))}',
               f'(a) A1 A1. (b) A2 A1. (c) A1 A1. (d) R1 interpolation reliable given R² = {sf(R2)}; R1 extrapolation unreliable – polynomial models diverge quickly outside the data.', 9, 'multi_step', gap='G5')


# =============================================================================================
# ch12 Probability
# =============================================================================================
from fractions import Fraction as Fr


def fr(q):
    q = Fr(q).limit_denominator(100000)
    return str(q.numerator) if q.denominator == 1 else f'{q.numerator}/{q.denominator}'


def frd(q):
    """fraction and 3 s.f. decimal"""
    q = Fr(q)
    return fr(q) if q.denominator in (1, 2, 4, 5, 10) else f'{fr(q)} ({sf(float(q))})'


R.facts('ch12-st1', F(
    terms=[('sample space', 'the set U of all possible outcomes of an experiment'),
           ('relative frequency', 'the number of times an event occurs divided by the number of trials; it estimates the probability for many trials'),
           ('expected number of occurrences', 'n × P(A): the mean number of times event A is expected in n trials'),
           ('complementary event', "A′, the event that A does not occur; P(A′) = 1 − P(A)")],
    facts=[('A fair six-sided die is rolled 300 times. What is the expected number of sixes?', '50', ['6', '30', '60'], '300 × 1/6.'),
           ('What is P(A′) if P(A) = 0.35?', '0.65', ['0.35', '1.35', '0.065'], 'P(A′) = 1 − P(A).'),
           ('Which value cannot be a probability?', '1.2', ['0', '0.999', '1'], '0 ≤ P ≤ 1.')],
    why=[('Explain why relative frequency becomes a better estimate of probability as the number of trials increases.', 'Random variation averages out over many trials (law of large numbers), so the proportion of successes settles close to the true probability.'),
         ('Explain why the expected number of occurrences need not be a whole number.', 'It is a long-run average, n × P(A); e.g. 10 rolls give an expected 10/6 ≈ 1.67 sixes, even though any single run gives a whole number.')],
    misc=[('A coin has landed heads five times in a row, so tails is now more likely.', 'Coin tosses are independent; P(tails) remains 0.5 regardless of previous results (gambler\'s fallacy).')],
))


@R.add('ch12-st1', ALL, (1, 5), 'short')
def prob_basic_core(rng, slot):
    c, d = slot.c, slot.d
    kind = rng.randint(0, 2)
    if kind == 0:
        cols = rng.sample(['red', 'blue', 'green', 'yellow', 'white', 'black'], 3)
        nums = [rng.randint(2, 15) for _ in cols]
        tot = sum(nums)
        bag = ', '.join(f'{n} {c_}' for n, c_ in zip(nums, cols))
        ev, p = cols[0], Fr(nums[0], tot)
        desc = f'A bag contains {bag} counters. One counter is taken at random.'
        evs = f'it is {ev}'
    elif kind == 1:
        faces = rng.choice([6, 8, 10, 12, 20])
        k = rng.randint(2, faces // 2)
        p = Fr(faces - k + 1, faces)
        desc = f'A fair {faces}-sided die, numbered 1 to {faces}, is rolled.'
        evs = f'the score is at least {k}'
    else:
        p = Fr(rng.randint(3, 17), 20)
        desc = f'Records show that the probability that a flight from {pick(rng, CITIES)} departs on time is {float(p):g}.'
        evs = 'a given flight departs on time'
    n = rng.choice([40, 60, 120, 150, 200, 360, 500, 1000])
    if c == 'C1':
        if d <= 1:
            return mcq(rng, f'{desc} Find the probability that {evs}.', fr(p), [fr(1 - p), fr(p / 2), fr(min(Fr(1), p + Fr(1, 10)))] if p != Fr(1, 2) else [fr(Fr(1, 3)), fr(Fr(2, 3)), fr(Fr(1, 4))],
                       f'P = {fr(p)}.')
        return ret(f'{desc} Find the probability that {evs}, and the probability that it is not the case.', f'{fr(p)}; {fr(1 - p)}', f'A1 {fr(p)}; A1 1 − {fr(p)} = {fr(1 - p)}.', 2)
    if c == 'C2':
        obs = round(n * float(p) + rng.choice([-1, 1]) * rng.randint(2, max(3, n // 15)))
        return ret(f'{desc} The experiment is repeated {n} times and "{evs}" occurs {obs} times. Compare the relative frequency with the theoretical probability and explain why they differ.',
                   f'relative frequency {sf(obs / n)}, probability {sf(float(p))}', f'A1 relative frequency {obs}/{n} = {sf(obs / n)}; A1 theoretical {fr(p)} = {sf(float(p))}; R1 random variation – they are expected to be close for large n but not equal.', 3, 'explain')
    if c == 'C3':
        return ret(f'{desc} The experiment is carried out {n} times (with replacement where relevant). Find the expected number of times that {evs}.', _num(n * float(p)),
                   f'n × P = {n} × {fr(p)} (M1) = {_num(round(n * float(p), 4))} (A1).', 2, 'numerical')
    stake, win = rng.choice([1, 2, 5]), rng.randint(3, 25)
    pw = Fr(rng.randint(1, 5), rng.choice([10, 12, 20, 36]))
    ev = float(pw) * win - stake
    if ev >= 0:
        return None
    cc_ = cur(rng)
    plays = rng.choice([100, 200, 500])
    return ret(f'At a school fair a game costs {stake} {cc_} to play. A player wins a prize of {win} {cc_} (and does not get the stake back) with probability {fr(pw)}. '
               f'(a) Find the expected number of winners in {plays} games. (b) Find the expected profit for the organisers over {plays} games. (c) Find the prize that would make the game fair. (d) Comment on the use of relative frequency to check the probability {fr(pw)}.',
               f'(a) {_num(plays * float(pw))} (b) {sf(-ev * plays)} (c) {sf(stake / float(pw))}',
               f'(a) {plays} × {fr(pw)} (M1) = {sf(plays * float(pw))} (A1). (b) income {plays * stake} − prizes {sf(plays * float(pw) * win)} (M1) = {sf(-ev * plays)} (A1). (c) prize × {fr(pw)} = {stake} (M1) ⇒ {sf(stake / float(pw))} (A1). '
               f'(d) R1 a large number of trials is needed for the relative frequency to be a good estimate.', 7, 'multi_step', gap='G5')


R.facts('ch12-st2', F(
    terms=[('Venn diagram', 'a diagram of overlapping regions inside a rectangle U showing how events relate and how many outcomes lie in each region'),
           ('tree diagram', 'a branching diagram for successive events in which probabilities are multiplied along branches and added across outcomes'),
           ('sample space diagram', 'a grid listing all equally likely outcomes of two combined experiments, e.g. two dice'),
           ('intersection', 'A ∩ B, outcomes in both A and B')],
    facts=[('Two fair dice are rolled. What is the probability that the total is 7?', '1/6', ['7/36', '1/12', '1/36'], 'Six of the 36 outcomes give 7.'),
           ('On a tree diagram, probabilities along a path are…', 'multiplied', ['added', 'subtracted', 'averaged'], 'Successive events: multiply.'),
           ('In a Venn diagram, the region inside A but outside B represents…', 'A ∩ B′', ['A ∪ B', 'A′ ∩ B', 'A ∩ B'], 'In A and not in B.')],
    why=[('Explain why the branches leaving any point of a tree diagram must have probabilities summing to 1.', 'They show all the possible outcomes at that stage, which are mutually exclusive and exhaustive.'),
         ('Explain why the probabilities on the second set of branches change when sampling without replacement.', 'Removing the first item changes the number of each type left and the total, so the second-stage probabilities depend on the first outcome.')],
    misc=[('In a Venn diagram, n(A) is the number in the overlap.', 'n(A) is the whole of circle A, including the overlap with B; the overlap alone is n(A ∩ B).')],
))


@R.add('ch12-st2', ALL, (1, 5), 'short')
def venn_tree_core(rng, slot):
    c, d = slot.c, slot.d
    if rng.random() < 0.5:
        N = rng.randint(40, 120)
        both = rng.randint(3, 15)
        a_only, b_only = rng.randint(5, 30), rng.randint(5, 30)
        neither = N - both - a_only - b_only
        if neither < 0:
            return None
        A, B = pick(rng, [('play football', 'play basketball'), ('study French', 'study Spanish'), ('own a cat', 'own a dog'), ('walk to school', 'have a phone'), ('like coffee', 'like tea')])
        desc = f'In a group of {N} students, {a_only + both} {A}, {b_only + both} {B} and {neither} do neither.'
        if c == 'C1':
            return ret(f'{desc} Find the number of students who {A} and {B}.', str(both), f'n(A ∪ B) = {N} − {neither} = {N - neither} (M1); n(A ∩ B) = {a_only + both} + {b_only + both} − {N - neither} = {both} (A1).', 2)
        if c == 'C2':
            return ret(f'{desc} {name(rng)} says the probability a randomly chosen student does at least one activity is ({a_only + both} + {b_only + both})/{N}. Explain the error and find the correct probability.',
                       fr(Fr(N - neither, N)), f'R1 the {both} students in both groups are counted twice; M1 ({a_only + both} + {b_only + both} − {both})/{N}; A1 {fr(Fr(N - neither, N))}.', 3, 'explain', gap='G2')
        if c == 'C3':
            return ret(f'{desc} (a) Draw a Venn diagram. (b) Find the probability that a student chosen at random does exactly one of the two. (c) Find P(B | A).',
                       f'(b) {fr(Fr(a_only + b_only, N))} (c) {fr(Fr(both, a_only + both))}', f'(a) regions {a_only}, {both}, {b_only}, {neither} (A2). (b) ({a_only} + {b_only})/{N} = {fr(Fr(a_only + b_only, N))} (A1). (c) {both}/{a_only + both} = {fr(Fr(both, a_only + both))} (M1 A1).', 5, 'numerical')
        pa, pb, pab = Fr(a_only + both, N), Fr(b_only + both, N), Fr(both, N)
        return ret(f'{desc} (a) Complete a Venn diagram. (b) Find P(A ∪ B′). (c) Find the probability that two different students chosen at random both do neither activity. (d) Determine whether the events "{A}" and "{B}" are independent.',
                   f'(b) {fr(Fr(a_only + both + neither, N))} (c) {fr(Fr(neither * (neither - 1), N * (N - 1)))} (d) {"independent" if pab == pa * pb else "not independent"}',
                   f'(a) A2. (b) ({a_only} + {both} + {neither})/{N} (M1) = {fr(Fr(a_only + both + neither, N))} (A1). (c) {neither}/{N} × {neither - 1}/{N - 1} (M1) = {fr(Fr(neither * (neither - 1), N * (N - 1)))} (A1). '
                   f'(d) P(A)P(B) = {fr(pa * pb)} vs P(A ∩ B) = {fr(pab)} (M1) ⇒ {"independent" if pab == pa * pb else "not independent"} (R1).', 8, 'multi_step', gap='G5')
    r_, g_ = rng.randint(3, 9), rng.randint(2, 8)
    t = r_ + g_
    obj = pick(rng, [('red', 'green', 'sweets'), ('black', 'white', 'pens'), ('gold', 'silver', 'coins'), ('striped', 'plain', 'socks')])
    desc = f'A box contains {r_} {obj[0]} and {g_} {obj[1]} {obj[2]}. Two are taken at random without replacement.'
    p_same = Fr(r_ * (r_ - 1) + g_ * (g_ - 1), t * (t - 1))
    p_rr = Fr(r_ * (r_ - 1), t * (t - 1))
    p_diff = 1 - p_same
    if c == 'C1':
        return ret(f'{desc} Write down the probability that the first is {obj[0]} and the probability that the second is {obj[0]} given that the first was {obj[0]}.', f'{fr(Fr(r_, t))}; {fr(Fr(r_ - 1, t - 1))}',
                   f'A1 {r_}/{t}; A1 {r_ - 1}/{t - 1}.', 2)
    if c == 'C2':
        return ret(f'{desc} {name(rng)} calculates P(both {obj[0]}) = ({r_}/{t})². Explain why this is incorrect and find the correct probability.', fr(p_rr),
                   f'R1 without replacement the second probability is {r_ - 1}/{t - 1}, not {r_}/{t}; M1 {r_}/{t} × {r_ - 1}/{t - 1}; A1 {fr(p_rr)}.', 3, 'explain', gap='G2')
    if c == 'C3':
        return ret(f'{desc} Draw a tree diagram and find the probability that the two {obj[2]} are different colours.', fr(p_diff),
                   f'Tree with correct second-stage probabilities (M1 A1); {r_}/{t} × {g_}/{t - 1} + {g_}/{t} × {r_}/{t - 1} (M1) = {fr(p_diff)} (A1).', 4, 'numerical')
    p_r_given_same = p_rr / p_same
    return ret(f'{desc} (a) Draw a tree diagram. (b) Find the probability that both are the same colour. (c) Given that both are the same colour, find the probability that both are {obj[0]}. '
               f'(d) Find the probability of different colours if the first one is replaced before the second is taken, and explain why it differs.',
               f'(b) {fr(p_same)} (c) {fr(p_r_given_same)} (d) {fr(Fr(2 * r_ * g_, t * t))}',
               f'(a) A2. (b) {r_}·{r_ - 1} + {g_}·{g_ - 1} over {t}·{t - 1} (M1) = {fr(p_same)} (A1). (c) P(both {obj[0]})/P(same) (M1) = {fr(p_r_given_same)} (A1). (d) 2 × {r_}/{t} × {g_}/{t} = {fr(Fr(2 * r_ * g_, t * t))} (A1); R1 with replacement the events are independent.',
               9, 'multi_step', gap='G5')


@R.add('ch12-st2', ('C1', 'C3', 'C4'), (1, 5), 'short')
def dice_space(rng, slot):
    f1, f2 = rng.choice([4, 6, 8]), rng.choice([4, 6])
    op = pick(rng, ['sum', 'product', 'difference'])
    vals = [(a, b) for a in range(1, f1 + 1) for b in range(1, f2 + 1)]
    fn = {'sum': lambda a, b: a + b, 'product': lambda a, b: a * b, 'difference': lambda a, b: abs(a - b)}[op]
    res = [fn(a, b) for a, b in vals]
    k = pick(rng, sorted(set(res)))
    p_eq = Fr(sum(1 for r_ in res if r_ == k), len(res))
    thr = pick(rng, sorted(set(res))[1:-1] or [k])
    p_gt = Fr(sum(1 for r_ in res if r_ > thr), len(res))
    desc = f'A fair {f1}-sided die and a fair {f2}-sided die are rolled and the {op}{" (larger minus smaller)" if op == "difference" else ""} of the two scores is recorded.'
    if slot.c == 'C1':
        return ret(f'{desc} Write down the number of outcomes in the sample space and find P({op} = {k}).', f'{len(res)}; {fr(p_eq)}', f'A1 {f1} × {f2} = {len(res)}; A1 {fr(p_eq)}.', 2)
    if slot.c == 'C3':
        return ret(f'{desc} Draw a sample space diagram and find P({op} > {thr}).', fr(p_gt), f'Grid of {len(res)} outcomes (M1); count {sum(1 for r_ in res if r_ > thr)} (A1); {fr(p_gt)} (A1).', 3, 'numerical')
    ex = sum(res) / len(res)
    games = rng.choice([50, 100, 200])
    return ret(f'{desc} (a) Draw a sample space diagram. (b) Find P({op} > {thr}). (c) Find the expected {op}. (d) In {games} games a player wins whenever the {op} exceeds {thr}; find the expected number of wins.',
               f'(b) {fr(p_gt)} (c) {sf(ex)} (d) {sf(games * float(p_gt))}', f'(a) A2. (b) A1 {fr(p_gt)}. (c) Σ/{len(res)} (M1) = {sf(ex)} (A1). (d) {games} × {fr(p_gt)} = {sf(games * float(p_gt))} (A1).', 6, 'multi_step', gap='G5')


R.facts('ch12-st3', F(
    terms=[('mutually exclusive events', 'events that cannot happen together, so P(A ∩ B) = 0 and P(A ∪ B) = P(A) + P(B)'),
           ('independent events', 'events where the occurrence of one does not affect the probability of the other: P(A ∩ B) = P(A)P(B)'),
           ('conditional probability', 'P(A | B) = P(A ∩ B)/P(B), the probability of A given that B has occurred'),
           ('combined events formula', 'P(A ∪ B) = P(A) + P(B) − P(A ∩ B)')],
    facts=[('If A and B are mutually exclusive with P(A) = 0.3 and P(B) = 0.45, what is P(A ∪ B)?', '0.75', ['0.135', '0.615', '0.15'], 'Add when mutually exclusive.'),
           ('If A and B are independent with P(A) = 0.4 and P(B) = 0.5, what is P(A ∩ B)?', '0.2', ['0.9', '0.7', '0.1'], 'Multiply when independent.'),
           ('If P(A | B) = P(A), the events A and B are…', 'independent', ['mutually exclusive', 'complementary', 'impossible'], 'Knowing B does not change P(A).')],
    why=[('Explain why two events with non-zero probabilities cannot be both mutually exclusive and independent.', 'Mutually exclusive means P(A ∩ B) = 0, but independence requires P(A ∩ B) = P(A)P(B) > 0; both cannot hold.'),
         ('Explain why P(A | B) and P(B | A) are usually different.', 'They divide P(A ∩ B) by different probabilities, P(B) and P(A); they are equal only if P(A) = P(B).')],
    misc=[('If P(A) = 0.6 and P(B) = 0.7 then P(A ∪ B) = 1.3.', 'A probability cannot exceed 1; the events must overlap, and P(A ∪ B) = 0.6 + 0.7 − P(A ∩ B).')],
))


@R.add('ch12-st3', ALL, (1, 5), 'short')
def cond_core(rng, slot):
    c, d = slot.c, slot.d
    pa, pb = Fr(rng.randint(2, 8), 10), Fr(rng.randint(2, 8), 10)
    pab = Fr(rng.randint(1, int(min(pa, pb) * 20)), 20)
    if pa + pb - pab > 1:
        return None
    if c == 'C1':
        if d <= 1:
            return mcq(rng, f'P(A) = {float(pa):g}, P(B) = {float(pb):g} and P(A ∩ B) = {float(pab):g}. Find P(A ∪ B).', f'{float(pa + pb - pab):g}', [f'{float(pa + pb):g}', f'{float(pa * pb):g}', f'{float(pa + pb - 2 * pab):g}'],
                       'P(A ∪ B) = P(A) + P(B) − P(A ∩ B).')
        return ret(f'P(A) = {float(pa):g}, P(B) = {float(pb):g} and P(A ∩ B) = {float(pab):g}. Find P(A | B).', frd(pab / pb), f'P(A ∩ B)/P(B) (M1) = {frd(pab / pb)} (A1).', 2)
    if c == 'C2':
        ind = pab == pa * pb
        return ret(f'P(A) = {float(pa):g}, P(B) = {float(pb):g} and P(A ∩ B) = {float(pab):g}. Determine, with a reason, whether A and B are (a) mutually exclusive; (b) independent.',
                   f'(a) no (b) {"yes" if ind else "no"}', f'(a) R1 P(A ∩ B) = {float(pab):g} ≠ 0, so not mutually exclusive. (b) P(A)P(B) = {float(pa * pb):g} (M1); R1 {"equal to" if ind else "not equal to"} P(A ∩ B), so {"independent" if ind else "not independent"}.', 3, 'explain')
    if c == 'C3':
        rows = pick(rng, [('Year 11', 'Year 12'), ('under 25', '25 and over'), ('morning shift', 'evening shift')])
        cols = pick(rng, [('walks', 'cycles', 'takes the bus'), ('prefers tea', 'prefers coffee', 'prefers juice'), ('rated it good', 'rated it average', 'rated it poor')])
        M = [[rng.randint(5, 40) for _ in range(3)] for _ in range(2)]
        tot = sum(map(sum, M))
        i, j = rng.randint(0, 1), rng.randint(0, 2)
        col_tot = M[0][j] + M[1][j]
        tab = '; '.join(f'{rows[r]}: ' + ', '.join(f'{cols[k]} {M[r][k]}' for k in range(3)) for r in range(2))
        return ret(f'A survey gives the following counts — {tab}. One person is chosen at random. Find (a) P(the person {cols[j]}); (b) P(the person is {rows[i]} | the person {cols[j]}); (c) P(the person {cols[j]} | the person is {rows[i]}).',
                   f'(a) {fr(Fr(col_tot, tot))} (b) {fr(Fr(M[i][j], col_tot))} (c) {fr(Fr(M[i][j], sum(M[i])))}', f'(a) {col_tot}/{tot} (A1). (b) {M[i][j]}/{col_tot} (M1 A1). (c) {M[i][j]}/{sum(M[i])} (A1).', 4, 'numerical')
    prev = rng.choice([0.01, 0.02, 0.05, 0.1, 0.005])
    sens, spec = rng.choice([0.9, 0.95, 0.98, 0.99]), rng.choice([0.9, 0.95, 0.97, 0.99])
    ppos = prev * sens + (1 - prev) * (1 - spec)
    post = prev * sens / ppos
    cond = pick(rng, ['a rare disease', 'a food allergy', 'a viral infection', 'a genetic condition'])
    return ret(f'A screening test for {cond} affects {prev * 100:g}% of a population. The test is positive for {sens * 100:g}% of people with the condition and negative for {spec * 100:g}% of people without it. '
               f'(a) Draw a tree diagram. (b) Find the probability that a randomly chosen person tests positive. (c) Find the probability that a person who tests positive has the condition. (d) Comment on your answer to (c) in context.',
               f'(b) {sf(ppos)} (c) {sf(post)}', f'(a) A2. (b) {prev} × {sens} + {_num(1 - prev)} × {_num(round(1 - spec, 4))} (M1) = {sf(ppos)} (A1). (c) {sf(prev * sens)}/{sf(ppos)} (M1) = {sf(post)} (A1). '
               f'(d) R1 {"most positive results are false positives because the condition is rare – a second test is needed" if post < 0.5 else "a positive result is fairly reliable, but some false positives remain"}.', 7, 'multi_step', gap='G5')


@R.add('ch12-st3', ('C3', 'C4'), (2, 5), 'multi_step')
def cond_tree(rng, slot):
    A, B, A_, B_ = pick(rng, [('it rains', 'the bus is late', 'it does not rain', 'the bus is on time'), ('a student revises', 'the student passes', 'a student does not revise', 'the student fails'),
                              ('a customer is a member', 'the customer buys a coffee', 'a customer is not a member', 'no coffee is bought'),
                              ('the alarm goes off', 'Kenji is on time', 'the alarm does not go off', 'Kenji is late'), ('a seed is treated', 'the seed germinates', 'a seed is untreated', 'it does not germinate')])
    pa = Fr(rng.randint(2, 8), 10)
    pba, pbna = Fr(rng.randint(3, 9), 10), Fr(rng.randint(1, 7), 10)
    if pba == pbna:
        return None
    pb = pa * pba + (1 - pa) * pbna
    pab = pa * pba / pb
    if slot.c == 'C3':
        return ret(f'The probability that {A} is {float(pa):g}. If {A}, the probability that {B} is {float(pba):g}; otherwise it is {float(pbna):g}. Find the probability that {B}.', frd(pb),
                   f'Tree diagram (M1); {float(pa):g} × {float(pba):g} + {float(1 - pa):g} × {float(pbna):g} (M1) = {frd(pb)} (A1).', 3, 'numerical')
    return ret(f'The probability that {A} is {float(pa):g}. If {A}, the probability that {B} is {float(pba):g}; if {A_}, it is {float(pbna):g}. (a) Draw a tree diagram. (b) Find the probability that {B}. '
               f'(c) Given that {B}, find the probability that {A}. (d) Determine whether the events "{A}" and "{B}" are independent, giving a reason.',
               f'(b) {frd(pb)} (c) {frd(pab)} (d) not independent', f'(a) A2. (b) M1 A1 {frd(pb)}. (c) P(A ∩ B)/P(B) = {float(pa * pba):g}/{sf(float(pb))} (M1) = {frd(pab)} (A1). (d) R1 P(B | A) = {float(pba):g} ≠ P(B) = {frd(pb)}, so not independent.',
               7, 'multi_step', gap='G5')


# =============================================================================================
# ch13 Probability distributions
# =============================================================================================
R.facts('ch13-st1', F(
    terms=[('discrete random variable', 'a variable X taking countable values x₁, x₂, … with probabilities P(X = x) that sum to 1'),
           ('expected value', 'E(X) = Σ x P(X = x), the long-run mean value of X'),
           ('fair game', 'a game in which the expected gain of each player is zero')],
    facts=[('For a probability distribution, what must Σ P(X = x) equal?', '1', ['0', 'E(X)', 'the number of values'], 'Total probability is 1.'),
           ('A game has expected gain −0.50 USD per play for the player. What does this mean?', 'on average the player loses 0.50 USD per game in the long run', ['the player loses every time', 'the game is fair', 'the player wins 0.50 USD'], 'Expected value is a long-run average.')],
    why=[('Explain why E(X) need not be one of the values that X can take.', 'E(X) is a weighted average of the values; e.g. a fair die has E(X) = 3.5, which cannot be rolled.'),
         ('Explain why casino games are designed to have a negative expected gain for players.', 'Over many plays the casino earns the difference; a negative E(gain) for players guarantees profit in the long run.')],
    misc=[('If E(X) = 0 then X is always 0.', 'E(X) = 0 means positive and negative values balance on average; X can take non-zero values.')],
))


@R.add('ch13-st1', ALL, (1, 5), 'short')
def drv_core(rng, slot):
    c, d = slot.c, slot.d
    xs = sorted(rng.sample(range(0, 8), 4))
    w = [rng.randint(1, 6) for _ in xs]
    denom = sum(w)
    ps = [Fr(wi, denom) for wi in w]
    E = sum(x * p for x, p in zip(xs, ps))
    if c == 'C1':
        kx = [wi for wi in w]
        return ret(f'The random variable X has P(X = x) = kc where c takes the values {", ".join(map(str, kx))} for x = {", ".join(map(str, xs))} respectively. Find k.', f'k = 1/{denom}',
                   f'Σ P = 1 ⇒ k({" + ".join(map(str, kx))}) = 1 (M1) ⇒ k = 1/{denom} (A1).', 2)
    tab = '; '.join(f'P(X = {x}) = {fr(p)}' for x, p in zip(xs, ps))
    if c == 'C2':
        return ret(f'For the distribution {tab}, find E(X) and explain why it is not necessarily a value that X can take.', frd(E), f'Σ x P (M1) = {frd(E)} (A1); R1 E(X) is a weighted long-run average.', 3, 'explain')
    if c == 'C3':
        return ret(f'For the distribution {tab}, find E(X) and P(X > {xs[1]}).', f'E(X) = {frd(E)}; {fr(sum(ps[2:]))}', f'E(X) = Σ x P (M1) = {frd(E)} (A1); P(X > {xs[1]}) = {fr(ps[2])} + {fr(ps[3])} = {fr(sum(ps[2:]))} (A1).', 3, 'numerical')
    prizes = [0, rng.randint(2, 5), rng.randint(6, 12), rng.randint(15, 40)]
    pr = [Fr(rng.randint(10, 30), 100), Fr(rng.randint(5, 15), 100), Fr(rng.randint(1, 6), 100)]
    p0 = 1 - sum(pr)
    if p0 <= 0:
        return None
    probs = [p0] + pr
    cost = math.ceil(float(sum(Fr(pz) * p for pz, p in zip(prizes, probs))) + rng.uniform(0.2, 2))
    Eg = sum(Fr(pz) * p for pz, p in zip(prizes, probs)) - cost
    fair_cost = sum(Fr(pz) * p for pz, p in zip(prizes, probs))
    c_ = cur(rng)
    return ret(f'A charity game costs {cost} {c_} per play. The prizes are 0, {prizes[1]}, {prizes[2]} and {prizes[3]} {c_} with probabilities {fr(p0)}, {fr(pr[0])}, {fr(pr[1])} and {fr(pr[2])}. '
               f'(a) Let G be the player\'s gain (prize − cost). Write down the probability distribution of G. (b) Find E(G). (c) Determine whether the game is fair and find the cost that would make it fair. (d) Estimate the charity\'s profit from 500 plays.',
               f'(b) {sf(float(Eg))} (c) {"fair" if Eg == 0 else "not fair"}; fair cost {sf(float(fair_cost))} (d) {sf(-500 * float(Eg))}',
               f'(a) G = {", ".join(str(pz - cost) for pz in prizes)} with the given probabilities (A1). (b) Σ g P(g) (M1) = {sf(float(Eg))} (A1). (c) R1 E(G) ≠ 0 so not fair; cost = E(prize) = {sf(float(fair_cost))} (A1). (d) 500 × {sf(-float(Eg))} = {sf(-500 * float(Eg))} (A1).',
               7, 'multi_step', gap='G5')


R.facts('ch13-st2', F(
    terms=[('binomial distribution', 'X ~ B(n, p): the number of successes in n independent trials, each with the same probability p of success'),
           ('Bernoulli trial', 'a single trial with exactly two outcomes, success (probability p) or failure (probability 1 − p)')],
    facts=[('For X ~ B(20, 0.3), what is E(X)?', '6', ['0.3', '4.2', '14'], 'E(X) = np.'),
           ('For X ~ B(20, 0.3), what is Var(X)?', '4.2', ['6', '1.8', '2.05'], 'Var(X) = np(1 − p).'),
           ('Which condition is NOT required for a binomial model?', 'the outcomes must be equally likely', ['a fixed number of trials', 'independent trials', 'constant probability of success'], 'p need not be 0.5.')],
    why=[('Explain why the number of red cards when dealing 5 cards from a pack without replacement is not exactly binomial.', 'The probability of red changes after each card is removed, and the trials are not independent; the binomial model needs a constant p.'),
         ('Explain why P(X ≥ 1) is best found as 1 − P(X = 0) for a binomial variable.', 'It avoids adding many terms: the complement of "at least one" is "none", a single probability.')],
    misc=[('For X ~ B(10, 0.4), P(X > 3) = 1 − P(X ≤ 2).', 'P(X > 3) = 1 − P(X ≤ 3); the value 3 itself must be excluded from X > 3.')],
))

BIN_CTX = [('seeds', 'A packet of seeds has a germination rate of {p}%. {n} seeds are planted.', 'seeds germinate'),
           ('penalty', 'A footballer scores {p}% of penalties. She takes {n} penalties.', 'penalties are scored'),
           ('defect', 'A machine produces components of which {p}% are defective. A random sample of {n} is tested.', 'components are defective'),
           ('quiz', 'A multiple-choice quiz has {n} questions, each with 4 options; a student guesses every answer (p = 25%).', 'answers are correct'),
           ('flight', 'On a route, {p}% of passengers check in online. {n} passengers are selected at random.', 'passengers checked in online'),
           ('vaccine', 'A vaccine produces immunity in {p}% of people. {n} people are vaccinated.', 'people become immune')]


@R.add('ch13-st2', ALL, (1, 5), 'short')
def binom_core(rng, slot):
    c, d = slot.c, slot.d
    kind, tmpl, ev = pick(rng, BIN_CTX)
    n = rng.randint(8, 30)
    p = 0.25 if kind == 'quiz' else rng.choice([0.05, 0.1, 0.15, 0.2, 0.3, 0.35, 0.4, 0.6, 0.7, 0.8, 0.85, 0.9])
    desc = tmpl.format(p=_num(p * 100), n=n)
    r = max(0, min(n, round(n * p) + rng.randint(-2, 2)))
    if c == 'C1':
        if d <= 1:
            return nmcq(rng, f'{desc} Let X be the number of {ev.split()[0]} that {" ".join(ev.split()[1:])}. Find E(X).', n * p, [n * p * (1 - p), p, n * (1 - p)], f'E(X) = np = {n} × {p} = {_num(n * p)}.', fmtf=_num)
        return ret(f'{desc} Find the probability that exactly {r} {ev}.', sf(binpmf(n, p, r)), f'X ~ B({n}, {p}) (M1); P(X = {r}) = {sf(binpmf(n, p, r))} (A1).', 2)
    if c == 'C2':
        return ret(f'{desc} State two assumptions needed to model the number of {ev.split()[0]} that {" ".join(ev.split()[1:])} by B({n}, {p}), and comment on whether they are reasonable here.',
                   'independent trials; constant probability', f'R1 each trial is independent of the others; R1 the probability {p} is the same for every trial; R1 sensible comment on this context.', 3, 'explain')
    lo = max(0, r - 2)
    if c == 'C3':
        v = rng.random()
        if v < 0.5:
            return ret(f'{desc} Find the probability that (a) at most {r}; (b) at least {lo + 1} {ev}.', f'(a) {sf(bincdf(n, p, r))} (b) {sf(1 - bincdf(n, p, lo))}',
                       f'X ~ B({n}, {p}) (M1); (a) P(X ≤ {r}) = {sf(bincdf(n, p, r))} (A1); (b) 1 − P(X ≤ {lo}) (M1) = {sf(1 - bincdf(n, p, lo))} (A1).', 4, 'numerical')
        return ret(f'{desc} Find the mean and the standard deviation of the number of {ev.split()[0]} that {" ".join(ev.split()[1:])}, and P({lo} < X ≤ {r + 1}).', f'mean {_num(n * p)}, sd {sf(math.sqrt(n * p * (1 - p)))}; {sf(bincdf(n, p, r + 1) - bincdf(n, p, lo))}',
                   f'np = {_num(n * p)} (A1); √(np(1 − p)) = {sf(math.sqrt(n * p * (1 - p)))} (A1); P(X ≤ {r + 1}) − P(X ≤ {lo}) (M1) = {sf(bincdf(n, p, r + 1) - bincdf(n, p, lo))} (A1).', 4, 'numerical')
    target = rng.choice([0.9, 0.95, 0.99])
    nn = 1
    while 1 - (1 - p) ** nn < target:
        nn += 1
    days = rng.randint(3, 7)
    p_day = 1 - bincdf(n, p, r)
    return ret(f'{desc} (a) Find P(X > {r}). (b) This is repeated on {days} separate days. Find the probability that X > {r} on exactly 2 of the days. (c) Each individual independently has probability {p} of the outcome described. Find the least number of individuals that must be selected so that the probability that at least one of them has this outcome is more than {target}. '
               f'(d) Find the most likely value of X.',
               f'(a) {sf(p_day)} (b) {sf(binpmf(days, p_day, 2))} (c) {nn} (d) {max(range(n + 1), key=lambda k: binpmf(n, p, k))}',
               f'(a) 1 − P(X ≤ {r}) (M1) = {sf(p_day)} (A1). (b) B({days}, {sf(p_day)}) (M1): {sf(binpmf(days, p_day, 2))} (A1). (c) 1 − {_num(1 - p)}ⁿ > {target} (M1) ⇒ n = {nn} (A1). (d) mode from GDC table (A1).',
               8, 'multi_step', gap='G5')


R.facts('ch13-st3', F(
    terms=[('normal distribution', 'X ~ N(μ, σ²): a continuous, symmetric, bell-shaped distribution with mean μ and standard deviation σ'),
           ('standardised value', 'z = (x − μ)/σ, the number of standard deviations x is from the mean'),
           ('inverse normal calculation', 'finding the value x for which P(X < x) equals a given probability')],
    facts=[('Approximately what percentage of a normal distribution lies within one standard deviation of the mean?', '68%', ['95%', '50%', '99.7%'], '68–95–99.7 rule.'),
           ('For X ~ N(50, 16), what is the standard deviation?', '4', ['16', '256', '8'], 'σ² = 16.'),
           ('For a normal distribution, P(X = a) for a single value a is…', '0', ['1', '0.5', 'the height of the curve'], 'Continuous distribution: probability is area.')],
    why=[('Explain why a normal distribution can be a reasonable model for heights but not for the number of children in a family.', 'Heights are continuous and roughly symmetric about a mean; family sizes are discrete, small and skewed, so a normal model fits poorly.'),
         ('Explain why P(X < μ) = 0.5 for any normal distribution.', 'The curve is symmetric about μ, so exactly half of the area lies on each side.')],
    misc=[('If X ~ N(100, 15²), then about 95% of values lie between 85 and 115.', 'About 68% lie within one σ (85 to 115); about 95% lie within two σ (70 to 130).')],
))

NORM_CTX = [('the masses of apples from an orchard', 'g', (120, 220), (8, 25)), ('the heights of adult women in a country', 'cm', (158, 170), (5, 8)),
            ('the times taken to complete a 10 km race', 'minutes', (45, 70), (5, 12)), ('the lifetimes of a type of LED bulb', 'hours', (8000, 20000), (500, 2000)),
            ('the volumes of juice in cartons', 'ml', (995, 1010), (2, 6)), ('the daily volumes of water used by households in a town', 'litres', (250, 400), (30, 70))]


@R.add('ch13-st3', ALL, (1, 5), 'short')
def normal_core(rng, slot):
    c, d = slot.c, slot.d
    what, unit, (mlo, mhi), (slo, shi) = pick(rng, NORM_CTX)
    mu = rng.randint(mlo, mhi)
    sd = rng.randint(slo, shi) if shi > 20 else round(rng.uniform(slo, shi), 1)
    desc = f'{what[0].upper() + what[1:]} are normally distributed with mean {mu} {unit} and standard deviation {_num(sd)} {unit}.'
    a = round(mu - sd * rng.uniform(0.3, 2.0), 0 if sd >= 5 else 1)
    b = round(mu + sd * rng.uniform(0.3, 2.0), 0 if sd >= 5 else 1)
    P = lambda x: ncdf((x - mu) / sd)
    if c == 'C1':
        if d <= 1:
            return mcq(rng, f'{desc} Which value is closest to the percentage of values between {_num(mu - sd)} and {_num(mu + sd)} {unit}?', '68%', ['95%', '50%', '34%'], 'Within one standard deviation: about 68%.')
        return ret(f'{desc} Find the probability that a randomly chosen value is less than {_num(a)} {unit}.', sf(P(a)), f'normalcdf(−∞, {_num(a)}, {mu}, {_num(sd)}) (M1) = {sf(P(a))} (A1).', 2)
    if c == 'C2':
        return ret(f'{desc} Without a calculator, explain why P(X > {_num(mu + sd)}) is approximately 0.16, and then find its value with technology.', f'≈ 0.16; {sf(1 - P(mu + sd))}',
                   f'R1 about 68% lies within one σ, leaving 32% split equally in the two tails by symmetry; A1 {sf(1 - P(mu + sd))}.', 2, 'explain')
    pr = rng.choice([0.05, 0.1, 0.15, 0.2, 0.25, 0.8, 0.9, 0.95])
    xq = mu + sd * ninv(pr)
    if c == 'C3':
        if rng.random() < 0.5:
            return ret(f'{desc} Find (a) P({_num(a)} < X < {_num(b)}); (b) the value of x such that P(X < x) = {pr}.', f'(a) {sf(P(b) - P(a))} (b) {sf(xq, 4) if xq > 1000 else sf(xq)} {unit}',
                       f'(a) normalcdf (M1) = {sf(P(b) - P(a))} (A1). (b) invNorm({pr}, {mu}, {_num(sd)}) (M1) = {sf(xq, 4) if xq > 1000 else sf(xq)} (A1).', 4, 'numerical')
        n_ = rng.choice([200, 500, 1000, 1500])
        return ret(f'{desc} In a sample of {n_}, find the expected number of values greater than {_num(b)} {unit}.', sf(n_ * (1 - P(b))), f'P(X > {_num(b)}) = {sf(1 - P(b))} (M1 A1); × {n_} = {sf(n_ * (1 - P(b)))} (A1).', 3, 'numerical')
    # C4: find σ or μ from a probability
    if rng.random() < 0.5:
        p_ = rng.choice([0.1, 0.05, 0.2, 0.025])
        x0 = round(mu - sd * abs(ninv(p_)) * rng.uniform(0.8, 1.2), 0)
        sig = (mu - x0) / abs(ninv(p_))
        return ret(f'{what[0].upper() + what[1:]} are normally distributed with mean {mu} {unit}. {int(p_ * 100) if p_ * 100 >= 1 else p_ * 100}% of values are below {_num(x0)} {unit}. (a) Find the standard deviation. '
                   f'(b) Find the probability that a value lies within 1.5 standard deviations of the mean. (c) Two values are chosen independently; find the probability that both are below {_num(x0)} {unit}.',
                   f'(a) {sf(sig)} {unit} (b) {sf(ncdf(1.5) - ncdf(-1.5))} (c) {sf(p_ * p_)}',
                   f'(a) z = invNorm({p_}) = {sf(ninv(p_))} (M1); ({_num(x0)} − {mu})/σ = {sf(ninv(p_))} (M1) ⇒ σ = {sf(sig)} (A1). (b) {sf(ncdf(1.5) - ncdf(-1.5))} (A1). (c) {p_}² = {sf(p_ * p_)} (M1 A1).', 7, 'multi_step', gap='G5')
    top = rng.choice([0.05, 0.1, 0.15])
    cut = mu + sd * ninv(1 - top)
    return ret(f'{desc} (a) Find the probability that a randomly chosen value lies between {_num(a)} and {_num(b)} {unit}. (b) The top {int(top * 100)}% of values are classed as "large". Find the minimum value classed as large. '
               f'(c) Given that a value is greater than {_num(mu)} {unit}, find the probability that it is classed as large. (d) In a random sample of 10, find the probability that exactly 2 are large.',
               f'(a) {sf(P(b) - P(a))} (b) {sf(cut, 4) if cut > 1000 else sf(cut)} (c) {sf(top / 0.5)} (d) {sf(binpmf(10, top, 2))}',
               f'(a) M1 A1. (b) invNorm({_num(1 - top)}) (M1) = {sf(cut, 4) if cut > 1000 else sf(cut)} (A1). (c) {top}/0.5 (M1) = {sf(top / 0.5)} (A1). (d) B(10, {top}) (M1): {sf(binpmf(10, top, 2))} (A1).', 8, 'multi_step', gap='G5')


R.facts('ch13-st4', F(
    terms=[('unbiased estimate of the population mean', 'the sample mean x̄'),
           ('unbiased estimate of the population variance', 's²ₙ₋₁ = n/(n − 1) × s²ₙ = Σ(x − x̄)²/(n − 1)'),
           ('linear transformation of a random variable', 'Y = aX + b, with E(Y) = aE(X) + b and Var(Y) = a²Var(X)')],
    facts=[('If Var(X) = 4, what is Var(3X − 2)?', '36', ['12', '10', '34'], 'Var(aX + b) = a²Var(X).'),
           ('If E(X) = 10, what is E(5 − 2X)?', '−15', ['15', '−20', '25'], 'E(aX + b) = aE(X) + b.'),
           ('Why is n − 1 used instead of n when estimating the population variance from a sample?', 'it corrects the tendency of the sample variance to underestimate the population variance', ['it makes the calculation easier', 'it removes outliers', 'it is required only for small populations'], 'Unbiased estimator.')],
    why=[('Explain why adding a constant to a random variable does not change its variance.', 'Each value and the mean shift by the same amount, so the deviations from the mean, and hence the variance, are unchanged.'),
         ('Explain why s²ₙ (dividing by n) tends to underestimate the population variance.', 'Deviations are measured from the sample mean, which is closer to the sample values than the true mean is; the squared deviations are therefore systematically too small, and dividing by n − 1 compensates.')],
    misc=[('Var(X − Y) = Var(X) − Var(Y) for independent X and Y.', 'Variances add for both sums and differences: Var(X − Y) = Var(X) + Var(Y).')],
))


@R.add('ch13-st4', ALL, (1, 5), 'short')
def lintrans_core(rng, slot):
    c, d = slot.c, slot.d
    EX, VX = round(rng.uniform(5, 60), 1), round(rng.uniform(2, 30), 1)
    a, b = rng.choice([2, 3, 0.5, 1.5, -2, 1.8]), rng.randint(-20, 40)
    if c == 'C1':
        if d <= 1:
            return nmcq(rng, f'E(X) = {EX} and Var(X) = {VX}. Find Var({_num(a)}X {sgn(b)}).', a * a * VX, [a * VX, a * a * VX + b, a * VX + b], f'a²Var(X) = {_num(a * a)} × {VX} = {sf(a * a * VX)}.')
        return ret(f'E(X) = {EX} and Var(X) = {VX}. Find E({_num(a)}X {sgn(b)}) and Var({_num(a)}X {sgn(b)}).', f'{sf(a * EX + b)}; {sf(a * a * VX)}', f'A1 {_num(a)} × {EX} {sgn(b)} = {sf(a * EX + b)}; A1 {_num(a)}² × {VX} = {sf(a * a * VX)}.', 2)
    n = rng.randint(8, 12)
    xs = [round(rng.uniform(10, 40), 1) for _ in range(n)]
    arr = np.array(xs)
    s2n = arr.var()
    s2 = arr.var(ddof=1)
    what = pick(rng, ['the masses (kg) of a sample of parcels', 'the lengths (cm) of a sample of leaves', 'the reaction times (hundredths of a second) of a sample of drivers', 'the weekly screen time (hours) of a sample of teenagers'])
    if c == 'C2':
        return ret(f'For a random sample of {n} values the GDC gives σₓ = {sf(math.sqrt(s2n))} and sₓ = {sf(math.sqrt(s2))}. Explain which value should be used to estimate the population variance, and find the estimate.',
                   f's²ₙ₋₁ = {sf(s2)}', f'R1 sₓ (dividing by n − 1) gives an unbiased estimate of the population variance; A1 s²ₙ₋₁ = {sf(math.sqrt(s2))}² = {sf(s2)}; R1 σₓ² = {sf(s2n)} would underestimate it.', 3, 'explain')
    if c == 'C3':
        return ret(f'A random sample gives {what}: {", ".join(_num(x) for x in xs)}. Find unbiased estimates of the population mean and variance.', f'x̄ = {sf(arr.mean())}; s²ₙ₋₁ = {sf(s2)}',
                   f'x̄ = {sf(arr.mean())} (A1); s²ₙ₋₁ = {n}/{n - 1} × {sf(s2n)} (M1) = {sf(s2)} (A1).', 3, 'numerical')
    Sx, Sx2 = arr.sum(), (arr ** 2).sum()
    k1, k2 = rng.choice([(1.8, 32), (2.2, 15), (1.1, -5), (100, -40)])
    return ret(f'A sample of {n} values has Σx = {sf(Sx, 5)} and Σx² = {sf(Sx2, 6)}. (a) Find unbiased estimates of the population mean and variance. (b) Each value is converted using y = {k1}x {sgn(k2)}. Find unbiased estimates of the mean and variance of Y. '
               f'(c) Explain why the variance of Y does not depend on {m(k2)}.'.replace(' + 0.', '.').replace(' + 0 ', ' '),
               f'(a) {sf(Sx / n)}; {sf((Sx2 - Sx * Sx / n) / (n - 1))} (b) {sf(k1 * Sx / n + k2)}; {sf(k1 * k1 * (Sx2 - Sx * Sx / n) / (n - 1))}',
               f'(a) x̄ = {sf(Sx, 5)}/{n} = {sf(Sx / n)} (A1); s²ₙ₋₁ = (Σx² − (Σx)²/n)/(n − 1) (M1) = {sf((Sx2 - Sx * Sx / n) / (n - 1))} (A1). (b) {k1} × x̄ {sgn(k2)} = {sf(k1 * Sx / n + k2)} (A1); {k1}² × s² = {sf(k1 * k1 * (Sx2 - Sx * Sx / n) / (n - 1))} (A1). '
               f'(c) R1 adding a constant shifts all values equally.', 7, 'multi_step', gap='G5')


R.facts('ch13-st5', F(
    terms=[('Poisson distribution', 'X ~ Po(m): the number of events in a fixed interval when events occur randomly, independently and at a constant average rate m'),
           ('mean and variance of a Poisson variable', 'for X ~ Po(m), E(X) = Var(X) = m')],
    facts=[('If X ~ Po(3) and Y ~ Po(5) are independent, what is the distribution of X + Y?', 'Po(8)', ['Po(15)', 'Po(4)', 'B(8, 0.5)'], 'Sum of independent Poisson variables.'),
           ('A sample of counts has mean 4.1 and variance 9.8. Is a Poisson model suitable?', 'No – the mean and variance should be approximately equal', ['Yes – counts are always Poisson', 'Yes – the variance is larger', 'No – the mean must be an integer'], 'For Po(m), mean = variance.'),
           ('Calls arrive at 2 per minute. What is the mean number of calls in 5 minutes?', '10', ['2', '2.5', '7'], 'Scale the rate: 2 × 5.')],
    why=[('Explain why the Poisson distribution is appropriate for the number of emails arriving per hour.', 'Emails arrive singly, randomly and independently at a roughly constant average rate, and there is no fixed maximum number – the conditions of a Poisson process.'),
         ('Explain why the number of people entering a shop per minute may not follow a Poisson distribution at lunchtime.', 'The rate is not constant (there is a rush) and people may arrive in groups, so events are not independent and the rate varies.')],
    misc=[('If X ~ Po(4) then P(X = 4) = 0.5 because 4 is the mean.', 'P(X = 4) = e⁻⁴4⁴/4! = 0.195; the mean is not a 50% value.')],
))

POI_CTX = [('calls arrive at a help desk', 'per 10 minutes'), ('cars pass a checkpoint', 'per minute'), ('typing errors occur', 'per page'), ('meteors are seen', 'per hour'),
           ('customers arrive at a bakery', 'per 5 minutes'), ('earthquakes of magnitude 4+ occur in a region', 'per month'), ('goals are scored', 'per match')]


@R.add('ch13-st5', ALL, (1, 5), 'short')
def poisson_core(rng, slot):
    c, d = slot.c, slot.d
    ev, per = pick(rng, POI_CTX)
    lam = round(rng.uniform(0.8, 7.5), 1)
    k = max(0, round(lam) + rng.randint(-2, 2))
    desc = f'{ev[0].upper() + ev[1:]} at an average rate of {lam} {per}, and can be modelled by a Poisson distribution.'
    if c == 'C1':
        if d <= 1:
            return nmcq(rng, f'{desc} Let X be the number in one interval. Write down Var(X).', lam, [math.sqrt(lam), lam * lam, lam / 2], f'For Po(m), Var(X) = m = {lam}.', fmtf=_num)
        return ret(f'{desc} Find the probability of exactly {k} in one interval.', sf(poipmf(lam, k)), f'X ~ Po({lam}) (M1); P(X = {k}) = e^(−{lam}){lam}{sup(k)}/{k}! = {sf(poipmf(lam, k))} (A1).', 2)
    if c == 'C2':
        mean_, var_ = round(lam + rng.uniform(-0.3, 0.3), 2), round(lam * rng.choice([0.95, 1.05, 2.4, 0.4]), 2)
        ok = abs(var_ - mean_) / mean_ < 0.2
        return ret(f'Data on the number of times {ev} {per} over 50 intervals have mean {mean_} and variance {var_}. Explain whether a Poisson model is appropriate.', 'appropriate' if ok else 'not appropriate',
                   f'R1 for a Poisson distribution mean = variance; R1 here {mean_} and {var_} are {"close" if ok else "very different"}, so the model is {"reasonable" if ok else "not suitable"}.', 2, 'explain')
    if c == 'C3':
        mult = rng.choice([2, 3, 4, 6])
        return ret(f'{desc} Find the probability of (a) at most {k} in one interval; (b) more than {round(lam * mult)} in {mult} intervals.', f'(a) {sf(poicdf(lam, k))} (b) {sf(1 - poicdf(lam * mult, round(lam * mult)))}',
                   f'(a) P(X ≤ {k}) = {sf(poicdf(lam, k))} (A1). (b) Y ~ Po({_num(lam * mult)}) (M1); 1 − P(Y ≤ {round(lam * mult)}) (M1) = {sf(1 - poicdf(lam * mult, round(lam * mult)))} (A1).', 4, 'numerical')
    lam2 = round(rng.uniform(0.5, 4), 1)
    tot = lam + lam2
    k2 = round(tot)
    days = rng.randint(5, 10)
    p0 = poipmf(lam, 0)
    return ret(f'{desc} At a second, independent location the same events occur at an average rate of {lam2} {per}. (a) Find the probability of no events at the first location in an interval. (b) Find the probability of a total of exactly {k2} events at the two locations in an interval. '
               f'(c) Over {days} intervals, find the probability that there are no events at the first location in at least one of them. (d) State an assumption needed for the total to be Poisson.',
               f'(a) {sf(p0)} (b) {sf(poipmf(tot, k2))} (c) {sf(1 - (1 - p0) ** days)} (d) independence',
               f'(a) e^(−{lam}) = {sf(p0)} (A1). (b) X + Y ~ Po({_num(tot)}) (M1 A1); P = {sf(poipmf(tot, k2))} (A1). (c) 1 − (1 − {sf(p0)}){sup(days)} (M1) = {sf(1 - (1 - p0) ** days)} (A1). (d) R1 events at the two locations occur independently.',
               8, 'multi_step', gap='G5')


# ---- definitions that open with a symbol would be capitalised by the fact templates (d = … → D = …);
# ---- give them a word opening instead.
def _word_open(dfn):
    w = dfn.split(' ')[0]
    if dfn[0] == dfn[0].upper() or re.fullmatch(r"(a|an|[a-z][a-z'\-]+[,;:]?)", w):
        return dfn
    if re.match(r'^[a-z] (varies|is) ', dfn):
        return 'the relation in which ' + dfn
    if re.search(r'\) (shifts|maps|stretches) ', dfn):
        return 'the transformation ' + dfn
    if ' means ' in dfn.split(':')[0]:
        return 'the statement that ' + dfn
    head = re.split(r'[,:;]', dfn, 1)[0]
    if any(op in head for op in ('=', '±', '≤', '≥')):
        return 'given by ' + dfn
    return 'denoted ' + dfn


def fix_terms(reg):
    for f in reg.f.values():
        f.terms = [(t, _word_open(d)) for t, d in f.terms]


fix_terms(R)
